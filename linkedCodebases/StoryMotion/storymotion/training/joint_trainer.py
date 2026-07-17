from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from pathlib import Path
import shutil
import tempfile

import torch
import torch.distributed as dist
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader

from storymotion.tokenizers.base import masked_mse_loss, masked_smooth_l1_loss


@dataclass
class JointTrainerConfig:
    log_dir: Path
    epochs: int = 1
    lr: float = 5.0e-5
    device: str = "cpu"
    log_every: int = 1
    val_every_steps: int = 2000
    eval_every_steps: int = 5000
    warmup_steps: int = 1000
    min_lr: float = 1.0e-6
    weight_decay: float = 0.0
    beta1: float = 0.9
    beta2: float = 0.999
    grad_clip: float = 1.0
    checkpoint_dir: Path | None = None
    checkpoint_prefix: str = "joint_tokenizer"
    save_every_steps: int = 25000
    keep_best_checkpoints: int = 3
    keep_step_checkpoints: int = 3
    is_main_process: bool = True


class JointHumanCameraTokenizerTrainer:
    def __init__(self, model: torch.nn.Module, config: JointTrainerConfig) -> None:
        self.model = model.to(config.device)
        self.config = config
        self.optim = torch.optim.AdamW(self.model.parameters(), lr=config.lr, betas=(config.beta1, config.beta2), weight_decay=config.weight_decay)
        self.writer = SummaryWriter(str(config.log_dir)) if config.is_main_process else None
        self.global_step = 0
        self.current_epoch = 0
        self.total_steps = 1
        self.best_val_loss = math.inf
        self.best_records: list[dict[str, float | int | Path]] = []

    def _base_model(self) -> torch.nn.Module:
        return self.model.module if hasattr(self.model, "module") else self.model

    def _should_run(self, every_steps: int) -> bool:
        return every_steps > 0 and self.global_step > 0 and self.global_step % every_steps == 0

    def _lr_scale(self) -> float:
        if self.config.warmup_steps > 0 and self.global_step < self.config.warmup_steps:
            return float(self.global_step + 1) / float(self.config.warmup_steps)
        decay_steps = max(1, self.total_steps - self.config.warmup_steps)
        progress = min(1.0, max(0.0, (self.global_step - self.config.warmup_steps) / decay_steps))
        min_scale = self.config.min_lr / self.config.lr if self.config.lr > 0 else 0.0
        return min_scale + (1.0 - min_scale) * 0.5 * (1.0 + math.cos(math.pi * progress))

    def _update_lr(self) -> None:
        scale = self._lr_scale()
        for group in self.optim.param_groups:
            group["lr"] = self.config.lr * scale
        if self.writer is not None and self.global_step % max(1, self.config.log_every) == 0:
            self.writer.add_scalar("train/lr", self.optim.param_groups[0]["lr"], self.global_step)

    def _frame_mask(self, batch: dict, human: torch.Tensor) -> torch.Tensor | None:
        lengths = batch.get("lengths")
        if lengths is None:
            return None
        lengths = lengths.to(human.device)
        frames = torch.arange(human.shape[1], device=human.device).unsqueeze(0)
        return frames < lengths.unsqueeze(1)

    def _reduce_scalars(self, scalars: dict[str, torch.Tensor]) -> dict[str, float]:
        values = {key: value.detach() for key, value in scalars.items()}
        if dist.is_available() and dist.is_initialized():
            for key, value in values.items():
                reduced = value.clone()
                dist.all_reduce(reduced, op=dist.ReduceOp.SUM)
                values[key] = reduced / dist.get_world_size()
        return {key: float(value.cpu()) for key, value in values.items()}

    def _metrics(self, human_recon: torch.Tensor, human: torch.Tensor, camera_recon: torch.Tensor, camera: torch.Tensor, mask: torch.Tensor | None) -> dict[str, torch.Tensor]:
        return {
            "metric_human_mse": masked_mse_loss(human_recon, human, mask),
            "metric_human_smooth_l1": masked_smooth_l1_loss(human_recon, human, mask),
            "metric_camera_mse": masked_mse_loss(camera_recon, camera, mask),
            "metric_camera_smooth_l1": masked_smooth_l1_loss(camera_recon, camera, mask),
        }

    def _step(self, batch: dict, split: str, train: bool) -> dict[str, torch.Tensor]:
        human = batch["human"].to(self.config.device)
        camera = batch["camera"].to(self.config.device)
        mask = self._frame_mask(batch, human)
        output = self.model(human, camera)
        losses = self._base_model().compute_loss(human, camera, output, mask=mask)
        metrics = self._metrics(output.human_recon.detach(), human.detach(), output.camera_recon.detach(), camera.detach(), mask)
        if train:
            self._update_lr()
            self.optim.zero_grad(set_to_none=True)
            losses["total_loss"].backward()
            if self.config.grad_clip > 0:
                grad_norm = torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.grad_clip)
                if self.writer is not None and self.global_step % max(1, self.config.log_every) == 0:
                    self.writer.add_scalar("train/grad_norm", float(grad_norm), self.global_step)
            self.optim.step()
        scalars = {**losses, **metrics}
        log_scalars = self._reduce_scalars(scalars)
        if self.writer is not None and (split != "train" or self.global_step % max(1, self.config.log_every) == 0):
            for key, value in log_scalars.items():
                self.writer.add_scalar(f"{split}/{key}", value, self.global_step)
        return scalars

    def _checkpoint_payload(self, extra: dict[str, float | int] | None = None) -> dict:
        config = asdict(self.config)
        config["log_dir"] = str(self.config.log_dir)
        config["checkpoint_dir"] = str(self.config.checkpoint_dir) if self.config.checkpoint_dir else ""
        return {
            "model": self._base_model().state_dict(),
            "stage1_model_contract": getattr(self._base_model(), "stage1_model_contract", {}),
            "optimizer": self.optim.state_dict(),
            "global_step": self.global_step,
            "epoch": self.current_epoch,
            "best_val_loss": self.best_val_loss,
            "config": config,
            **(extra or {}),
        }

    def _save_checkpoint_path(self, path: Path, extra: dict[str, float | int] | None = None) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.stem}.", suffix=".tmp", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            torch.save(self._checkpoint_payload(extra), tmp_path)
            tmp_path.replace(path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
        return path

    def _save_checkpoint(self, name: str, extra: dict[str, float | int] | None = None) -> Path | None:
        if self.config.checkpoint_dir is None or not self.config.is_main_process:
            return None
        return self._save_checkpoint_path(self.config.checkpoint_dir / f"{self.config.checkpoint_prefix}_{name}.pt", extra)

    def _copy_checkpoint(self, src: Path, dst: Path) -> None:
        tmp = dst.with_name(f".{dst.name}.tmp")
        try:
            shutil.copy2(src, tmp)
            tmp.replace(dst)
        finally:
            if tmp.exists():
                tmp.unlink()

    def _save_top_checkpoint(self, val_loss: float) -> None:
        if self.config.checkpoint_dir is None or not self.config.is_main_process or self.config.keep_best_checkpoints <= 0:
            return
        if len(self.best_records) >= self.config.keep_best_checkpoints and val_loss >= float(self.best_records[-1]["val_loss"]):
            return
        archive = self.config.checkpoint_dir / f"{self.config.checkpoint_prefix}_best_step_{self.global_step:08d}.pt"
        self._save_checkpoint_path(archive, {"best_val_loss": self.best_val_loss, "val_loss": val_loss})
        records = [*self.best_records, {"val_loss": float(val_loss), "global_step": int(self.global_step), "epoch": int(self.current_epoch), "path": archive}]
        records.sort(key=lambda record: (float(record["val_loss"]), int(record["global_step"])))
        keep = records[: self.config.keep_best_checkpoints]
        for record in records[self.config.keep_best_checkpoints :]:
            path = record.get("path")
            if isinstance(path, Path):
                path.unlink(missing_ok=True)
        self.best_records = keep
        for rank in range(1, self.config.keep_best_checkpoints + 1):
            stable = self.config.checkpoint_dir / f"{self.config.checkpoint_prefix}_best_top{rank}.pt"
            if rank <= len(self.best_records):
                src = self.best_records[rank - 1]["path"]
                if isinstance(src, Path):
                    self._copy_checkpoint(src, stable)
            else:
                stable.unlink(missing_ok=True)

    def _prune_step_checkpoints(self) -> None:
        if self.config.checkpoint_dir is None or self.config.keep_step_checkpoints <= 0:
            return
        pattern = f"{self.config.checkpoint_prefix}_step_*.pt"
        checkpoints = sorted(self.config.checkpoint_dir.glob(pattern), key=lambda path: path.stat().st_mtime)
        for path in checkpoints[: -self.config.keep_step_checkpoints]:
            path.unlink(missing_ok=True)

    def _validate_and_checkpoint(self, val_loader: DataLoader, val_split: str, *, write_scalars: bool, write_eval: bool, force_last: bool = False, save_periodic: bool = False) -> None:
        metrics = self.validate(val_loader, split=val_split, write_scalars=write_scalars, write_eval=write_eval)
        val_loss = metrics.get("total_loss")
        if val_loss is not None:
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
            self._save_top_checkpoint(float(val_loss))
        if force_last or self._should_run(self.config.save_every_steps):
            self._save_checkpoint("last", {"best_val_loss": self.best_val_loss})
        if save_periodic:
            self._save_checkpoint(f"step_{self.global_step:08d}", {"best_val_loss": self.best_val_loss})
            self._prune_step_checkpoints()

    @torch.no_grad()
    def validate(self, val_loader: DataLoader, split: str = "val", write_scalars: bool = True, write_eval: bool = True) -> dict[str, float]:
        self.model.eval()
        eval_model = self._base_model()
        eval_model.eval()
        totals: dict[str, float] = {}
        count = 0
        for batch in val_loader:
            human = batch["human"].to(self.config.device)
            camera = batch["camera"].to(self.config.device)
            mask = self._frame_mask(batch, human)
            output = eval_model(human, camera)
            scalars = {**eval_model.compute_loss(human, camera, output, mask=mask), **self._metrics(output.human_recon, human, output.camera_recon, camera, mask)}
            for key, value in scalars.items():
                totals[key] = totals.get(key, 0.0) + float(value.detach().cpu())
            count += 1
        averaged = {key: value / max(count, 1) for key, value in totals.items()}
        if self.writer is not None and write_scalars:
            for key, value in averaged.items():
                self.writer.add_scalar(f"{split}/{key}", value, self.global_step)
        if self.writer is not None and write_eval:
            for key, value in averaged.items():
                if key == "total_loss" or key.startswith("metric_"):
                    self.writer.add_scalar(f"eval/{key.removeprefix('metric_')}", value, self.global_step)
        if self.writer is not None:
            self.writer.flush()
        return averaged

    def fit(self, train_loader: DataLoader, val_loader: DataLoader | None = None, val_split: str = "val") -> None:
        self.total_steps = max(1, self.config.epochs * len(train_loader))
        if val_loader is not None and self.config.is_main_process:
            self._validate_and_checkpoint(val_loader, val_split, write_scalars=True, write_eval=True, force_last=True)
        for epoch in range(self.config.epochs):
            self.current_epoch = epoch + 1
            self.model.train()
            for batch in train_loader:
                self._step(batch, "train", train=True)
                self.global_step += 1
                if val_loader is not None:
                    run_val = self._should_run(self.config.val_every_steps)
                    run_eval = self._should_run(self.config.eval_every_steps)
                    run_save = self._should_run(self.config.save_every_steps)
                    is_final = self.global_step >= self.total_steps
                    should_validate = run_val or run_eval or run_save or is_final
                    if self.config.is_main_process and should_validate:
                        self._validate_and_checkpoint(val_loader, val_split, write_scalars=run_val or is_final, write_eval=run_eval or is_final, force_last=run_save or is_final, save_periodic=run_save)
            if val_loader is None and self.config.is_main_process:
                self._save_checkpoint("last", {"best_val_loss": self.best_val_loss})
        if self.writer is not None:
            self.writer.flush()
            self.writer.close()

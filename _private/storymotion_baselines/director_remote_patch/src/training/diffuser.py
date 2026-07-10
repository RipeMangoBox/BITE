from datetime import datetime
import functools
from omegaconf.dictconfig import DictConfig
from pathlib import Path
from typing import Any, List, Tuple
import warnings

from ema_pytorch import EMA
from evo.core.trajectory import PosePath3D
from evo.tools.plot import PlotCollection
import matplotlib.pyplot as plt
import numpy as np
import torch
from torchtyping import TensorType
import torch.nn as nn
import lightning as L

from utils.random_utils import StackedRandomGenerator
from utils.rotation_utils import project_so3
from utils.visualization import draw_trajectories
from src.metrics.callback import MetricCallback

# ------------------------------------------------------------------------------------- #

batch_size, num_samples = None, None
num_feats, num_rawfeats, num_cams = None, None, None
RawTrajectory = TensorType["num_samples", "num_rawfeats", "num_cams"]

# ------------------------------------------------------------------------------------- #


class Diffuser(L.LightningModule):
    def __init__(
        self,
        network: nn.Module,
        loss: nn.Module,
        optimizer: nn.Module,
        lr_scheduler: nn.Module,
        metric_callback: MetricCallback,
        log_wandb: bool,
        guidance_weight: float,
        ema_kwargs: DictConfig,
        sampling_kwargs: DictConfig,
        clatr: nn.Module = None,
        edm2_normalization: bool = True,
        sync_dist: bool = True,
        use_clatr_metrics: bool = True,
        clatr_required: bool = True,
        pulp_sanity_every_n_steps: int = 100,
        **kwargs,
    ):
        super().__init__()

        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log_wandb = log_wandb
        self.sync_dist = sync_dist

        # Network and EMA
        self.net = network
        self.ema = EMA(self.net, **ema_kwargs)
        self.guidance_weight = guidance_weight
        self.edm2_normalization = edm2_normalization

        # Optimizer and loss
        self.optimizer_fn = optimizer
        self.lr_scheduler_fn = lr_scheduler
        self.loss_fn = loss

        self.metric_callback = metric_callback
        self.clatr = clatr
        self.use_clatr_metrics = bool(use_clatr_metrics and clatr is not None)
        self.clatr_required = bool(clatr_required)
        self.pulp_sanity_every_n_steps = int(pulp_sanity_every_n_steps)
        if self.clatr is not None:
            self.clatr.eval()
        elif self.clatr_required:
            raise ValueError("CLaTr is required but diffuser.clatr is None")
        elif use_clatr_metrics:
            warnings.warn(
                "CLaTr metrics disabled because diffuser.clatr is None. "
                "Training and Pulp sanity metrics can still run.",
                RuntimeWarning,
            )

        # Sampling
        self.num_steps = sampling_kwargs.num_steps
        self.sigma_min = sampling_kwargs.sigma_min
        self.sigma_max = sampling_kwargs.sigma_max
        self.rho = sampling_kwargs.rho
        self.S_churn = sampling_kwargs.S_churn
        self.S_noise = sampling_kwargs.S_noise
        self.S_min = sampling_kwargs.S_min
        self.S_max = (
            sampling_kwargs.S_max
            if isinstance(sampling_kwargs.S_max, float)
            else float("inf")
        )

    # ---------------------------------------------------------------------------------- #

    def gather_list(self, input_list: List[torch.Tensor]):
        # Aggregate epoch level list
        input_tensor = torch.cat(input_list, dim=0)

        if self.trainer.world_size == 1:
            return input_tensor

        # Stack predictions from all the distributed processes on dim=0
        gather_tensor = self.all_gather(input_tensor)

        # Reshape to (dataset_size, *other_dims)
        gather_tensor = gather_tensor.view(-1, *gather_tensor.shape[2:])

        return gather_tensor

    # ---------------------------------------------------------------------------------- #

    def on_fit_start(self):
        eval_dataset = self.trainer.datamodule.eval_dataset
        self.modalities = list(eval_dataset.modality_datasets.keys())
        if self.use_clatr_metrics:
            self.metric_callback = self.metric_callback(device=self.device)
        else:
            self.metric_callback = None

        self.do_segment = False
        self.val_plot_samples = dict()

    def on_train_start(self):
        # ----------------------------------------------------------------------------- #
        # https://stackoverflow.com/questions/73095460/assertionerror-if-capturable-false-state-steps-should-not-be-cuda-tensors # Noqa
        if self.trainer.ckpt_path is not None and isinstance(
            self.optimizers().optimizer, torch.optim.AdamW
        ):
            self.optimizers().param_groups[0]["capturable"] = True
        # ----------------------------------------------------------------------------- #

    def configure_optimizers(self):
        optimizer = self.optimizer_fn(params=self.net.parameters())
        self.learning_rate = optimizer.param_groups[0]["lr"]

        total_steps = self.trainer.max_epochs * len(
            self.trainer.datamodule.train_dataloader()
        )
        scheduler = self.lr_scheduler_fn(optimizer=optimizer, total_steps=total_steps)

        return [optimizer], [{"scheduler": scheduler, "interval": "step"}]

    def lr_scheduler_step(self, scheduler, metric):
        scheduler.step(self.global_step)

    def optimizer_step(self, epoch, batch_idx, optimizer, optimizer_closure):
        if hasattr(self, "do_optimizer_step") and not self.do_optimizer_step:
            print("Skipping optimizer step")
            closure_result = optimizer_closure()
            if closure_result is not None:
                return closure_result
            else:
                return
        else:
            return super().optimizer_step(
                epoch, batch_idx, optimizer, optimizer_closure
            )

    # ---------------------------------------------------------------------------------- #

    def on_train_epoch_start(self):
        self.get_matrix = self.trainer.datamodule.train_dataset.get_matrix
        self.v_get_matrix = self.trainer.datamodule.eval_dataset.get_matrix

    def training_step(self, batch, batch_idx):
        data, mask = batch["traj_feat"], batch["padding_mask"]

        conds = dict()
        if len(self.modalities) > 0:
            cond_k = [x for x in batch.keys() if "traj" not in x and "feat" in x]
            cond_data = [batch[cond] for cond in cond_k]
            for cond in cond_k:
                cond_name = cond.replace("_feat", "")
                if isinstance(batch[f"{cond_name}_raw"], dict):
                    for cond_name_, x in batch[f"{cond_name}_raw"].items():
                        conds[cond_name_] = x
                else:
                    conds[cond_name] = batch[f"{cond_name}_raw"]
        else:
            cond_data = None

        # cf edm2 sigma_data normalization / https://arxiv.org/pdf/2312.02696.pdf
        if self.edm2_normalization:
            data *= self.loss_fn.sigma_data

        _loss = self.loss_fn(
            net=self.net, data=data, labels=cond_data, mask=~mask.to(bool)
        )
        loss = _loss.mean()

        # Log metrics
        self.log("train/loss", loss.item(), sync_dist=self.sync_dist)
        self.log_pulp_sanity("train", batch, data, mask, cond_data, loss)

        if not (
            not (self.trainer.current_epoch % self.trainer.check_val_every_n_epoch)
            and (self.trainer.current_epoch > 0)
        ):
            return loss
        if not self.use_clatr_metrics:
            return loss

        # Infer CLaTr features
        _, gen_data = self.sample(self.ema.ema_model, data, cond_data, mask)
        clip_seq = batch["caption_raw"]["clip_seq_caption"]
        clip_seq_mask = batch["caption_raw"]["clip_seq_mask"]
        with torch.autocast(device_type=data.device.type, dtype=data.dtype):
            with torch.no_grad():
                ref_clatr = self.clatr.encode(
                    {"x": data.permute(0, 2, 1), "mask": mask.to(bool)}
                )
                if clip_seq is not None:
                    text_clatr = self.clatr.encode(
                        {"x": clip_seq, "mask": clip_seq_mask.to(bool)}
                    )
                gen_clatr = self.clatr.encode(
                    {"x": gen_data.permute(0, 2, 1), "mask": mask.to(bool)}
                )

        # Update distribution metrics
        self.metric_callback.update_clatr_metrics(
            "train", gen_clatr, ref_clatr, text_clatr
        )

        # Update semantic metrics
        if "segments" in conds:
            self.do_segment = True
            gen_traj = torch.stack([self.get_matrix(x) for x in gen_data])
            ref_traj = torch.stack([self.v_get_matrix(x) for x in data])
            # Project on SO(3) (if not in SO(3))
            p_gen_traj = project_so3(gen_traj.reshape(-1, 4, 4)).reshape(
                *gen_traj.shape
            )
            self.metric_callback.update_caption_metrics(
                "train", p_gen_traj, conds["segments"], mask
            )

        return loss

    def log_pulp_sanity(self, split, batch, data, mask, cond_data, loss):
        if self.pulp_sanity_every_n_steps <= 0:
            return
        if split == "train" and (self.global_step % self.pulp_sanity_every_n_steps):
            return
        if "char_raw" not in batch or "char_centers" not in batch["char_raw"]:
            return

        with torch.no_grad():
            denoised = self.net(
                data,
                torch.full((data.shape[0],), self.loss_fn.sigma_data, device=data.device),
                y=cond_data,
                mask=~mask.to(bool),
            )
            if self.edm2_normalization:
                denoised = denoised / self.loss_fn.sigma_data
                ref_data = data / self.loss_fn.sigma_data
            else:
                ref_data = data
            gen_matrices = torch.stack(
                [self.get_matrix(x.detach().cpu()) for x in denoised.detach().cpu()]
            ).to(data.device)
            ref_matrices = torch.stack(
                [self.get_matrix(x.detach().cpu()) for x in ref_data.detach().cpu()]
            ).to(data.device)
            char_centers = batch["char_raw"]["char_centers"].to(data.device).permute(0, 2, 1)
            intrinsics = batch["intrinsics"].to(data.device)
            metrics = self.compute_pulp_root_sanity(
                gen_matrices, ref_matrices, char_centers, intrinsics, mask
            )
            for key, value in metrics.items():
                self.log(f"{split}/pulp_{key}", value, sync_dist=self.sync_dist)

    @staticmethod
    def compute_pulp_root_sanity(gen_matrices, ref_matrices, char_centers, intrinsics, mask):
        valid = mask.to(bool)
        gen_t = gen_matrices[:, :, :3, 3]
        ref_t = ref_matrices[:, :, :3, 3]
        valid_gen = gen_t[valid]
        valid_ref = ref_t[valid]
        metrics = {
            "camera_translation_absmax": valid_gen.abs().max(),
            "camera_translation_ref_absmax": valid_ref.abs().max(),
            "camera_translation_mae": (gen_t - ref_t).abs()[valid].mean(),
        }
        if valid.shape[1] > 1:
            valid_pair = valid[:, 1:] & valid[:, :-1]
            gen_vel = gen_t[:, 1:] - gen_t[:, :-1]
            ref_vel = ref_t[:, 1:] - ref_t[:, :-1]
            if valid_pair.any():
                metrics["camera_velocity_norm_mean"] = gen_vel[valid_pair].norm(dim=-1).mean()
                metrics["camera_velocity_ref_norm_mean"] = ref_vel[valid_pair].norm(dim=-1).mean()
                metrics["camera_static_frame_ratio"] = (
                    gen_vel[valid_pair].norm(dim=-1) < 1e-4
                ).float().mean()

        gen_proj = Diffuser.project_root_points(gen_matrices, char_centers)
        ref_proj = Diffuser.project_root_points(ref_matrices, char_centers)
        gen_frame = Diffuser.root_projection_metrics(gen_proj, intrinsics, valid)
        ref_frame = Diffuser.root_projection_metrics(ref_proj, intrinsics, valid)
        for key, value in gen_frame.items():
            metrics[f"root_{key}"] = value
        for key, value in ref_frame.items():
            metrics[f"root_ref_{key}"] = value
        metrics["root_in_frame_absdiff_vs_ref"] = (
            gen_frame["in_frame_ratio"] - ref_frame["in_frame_ratio"]
        ).abs()
        metrics["root_center_mae_vs_ref"] = (gen_proj[..., :2] - ref_proj[..., :2]).abs()[valid].mean()
        return metrics

    @staticmethod
    def project_root_points(camera_matrices, points_world):
        rot = camera_matrices[:, :, :3, :3]
        trans = camera_matrices[:, :, :3, 3]
        cam_points = torch.matmul(
            rot.transpose(-1, -2), (points_world - trans).unsqueeze(-1)
        ).squeeze(-1)
        z = cam_points[..., 2].clamp_min(1e-6)
        x = cam_points[..., 0] / z
        y = cam_points[..., 1] / z
        return torch.stack([x, y, cam_points[..., 2]], dim=-1)

    @staticmethod
    def root_projection_metrics(proj_norm, intrinsics, valid):
        fx, fy, cx, cy = [intrinsics[..., i] for i in range(4)]
        u = proj_norm[..., 0] * fx + cx
        v = proj_norm[..., 1] * fy + cy
        depth = proj_norm[..., 2]
        width = (2.0 * cx).clamp_min(1.0)
        height = (2.0 * cy).clamp_min(1.0)
        finite = torch.isfinite(u) & torch.isfinite(v) & torch.isfinite(depth)
        positive = depth > 0
        in_frame = finite & positive & (u >= 0) & (u <= width) & (v >= 0) & (v <= height)
        safe_valid = valid & finite
        if not safe_valid.any():
            zero = torch.zeros((), device=proj_norm.device)
            return {
                "in_frame_ratio": zero,
                "behind_camera_ratio": zero,
                "center_x_std": zero,
                "center_y_std": zero,
                "center_jitter_mean": zero,
            }
        u_norm = u / width.clamp_min(1.0)
        v_norm = v / height.clamp_min(1.0)
        valid_pair = safe_valid[:, 1:] & safe_valid[:, :-1]
        jitter = torch.zeros((), device=proj_norm.device)
        if valid_pair.any():
            center = torch.stack([u_norm, v_norm], dim=-1)
            jitter = (center[:, 1:] - center[:, :-1])[valid_pair].norm(dim=-1).mean()
        return {
            "in_frame_ratio": in_frame[valid].float().mean(),
            "behind_camera_ratio": ((~positive) & finite)[valid].float().mean(),
            "center_x_std": u_norm[safe_valid].std(unbiased=False),
            "center_y_std": v_norm[safe_valid].std(unbiased=False),
            "center_jitter_mean": jitter,
        }

    def on_after_backward(self):
        self.ema.update()

    def on_train_epoch_end(self):
        # Log metrics for same number of val batches each `check_val_every_n_epoch`
        if (
            # fmt: off
            not self.log_wandb
            or (self.trainer.current_epoch % self.trainer.check_val_every_n_epoch)
            or (self.trainer.current_epoch == 0)
            # fmt: on
        ):
            return

        # Compute distribution metrics
        metrics_dict = self.metric_callback.compute_clatr_metrics("train")

        # Compute semantic metrics
        if self.do_segment:
            metrics_dict.update(self.metric_callback.compute_caption_metrics("train"))

        for key, value in metrics_dict.items():
            self.log(f"train/{key}", value, sync_dist=self.sync_dist)

    # ---------------------------------------------------------------------------------- #

    def on_validation_epoch_start(self):
        self.get_matrix = self.trainer.datamodule.train_dataset.get_matrix
        self.v_get_matrix = self.trainer.datamodule.eval_dataset.get_matrix

    def validation_step(self, batch, batch_idx):
        data, mask = batch["traj_feat"], batch["padding_mask"]

        conds = dict()
        if len(self.modalities) > 0:
            cond_k = [x for x in batch.keys() if "traj" not in x and "feat" in x]
            cond_data = [batch[cond] for cond in cond_k]
            for cond in cond_k:
                cond_name = cond.replace("_feat", "")
                if isinstance(batch[f"{cond_name}_raw"], dict):
                    for cond_name_, x in batch[f"{cond_name}_raw"].items():
                        conds[cond_name_] = x
                else:
                    conds[cond_name] = batch[f"{cond_name}_raw"]
        else:
            cond_data = None

        # cf edm2 sigma_data normalization / https://arxiv.org/pdf/2312.02696.pdf
        if self.edm2_normalization:
            data *= self.loss_fn.sigma_data

        _loss = self.loss_fn(
            net=self.ema.ema_model, data=data, labels=cond_data, mask=~mask.to(bool)
        )
        loss = _loss.mean()
        self.log("val/loss", loss.item(), sync_dist=self.sync_dist)
        self.log_pulp_sanity("val", batch, data, mask, cond_data, loss)
        if not self.use_clatr_metrics:
            return loss

        # Infer CLaTr features
        _, gen_data = self.sample(self.ema.ema_model, data, cond_data, mask)
        clip_seq = batch["caption_raw"]["clip_seq_caption"]
        clip_seq_mask = batch["caption_raw"]["clip_seq_mask"]
        with torch.autocast(device_type=data.device.type, dtype=data.dtype):
            ref_clatr = self.clatr.encode(
                {"x": data.permute(0, 2, 1), "mask": mask.to(bool)}
            )
            if clip_seq is not None:
                text_clatr = self.clatr.encode(
                    {"x": clip_seq, "mask": clip_seq_mask.to(bool)}
                )
            gen_clatr = self.clatr.encode(
                {"x": gen_data.permute(0, 2, 1), "mask": mask.to(bool)}
            )

        # Update distribution metrics
        self.metric_callback.update_clatr_metrics(
            "val", gen_clatr, ref_clatr, text_clatr
        )

        # Update semantic metrics
        if "segments" in conds:
            self.do_segment = True
            ref_traj = torch.stack([self.v_get_matrix(x) for x in data])
            gen_traj = torch.stack([self.get_matrix(x) for x in gen_data])
            # Project on SO(3) (if not in SO(3))
            p_gen_traj = project_so3(gen_traj.reshape(-1, 4, 4)).reshape(
                *gen_traj.shape
            )
            self.metric_callback.update_caption_metrics(
                "val", p_gen_traj, conds["segments"], mask
            )

            # Keep sample for validation plots
            if "gen_traj" not in self.val_plot_samples:
                ref_traj_ = self.v_get_matrix(data[0])
                self.val_plot_samples["gen_traj"] = p_gen_traj[0].unsqueeze(0)
                self.val_plot_samples["ref_traj"] = ref_traj_.unsqueeze(0)
                self.val_plot_samples["mask"] = mask[0].unsqueeze(0)
                if "caption" in conds:
                    self.val_plot_samples["caption"] = conds["caption"][0]
                if "char_raw_feat" in conds:
                    char_feat = conds["char_raw_feat"][0].permute(1, 0)
                    self.val_plot_samples["char_feat"] = char_feat.unsqueeze(0)



    def on_validation_epoch_end(self):
        if not self.log_wandb:
            return

        # # Compute distribution metrics
        metrics_dict = self.metric_callback.compute_clatr_metrics("val")

        # Compute semantic metrics
        if self.do_segment:
            metrics_dict.update(self.metric_callback.compute_caption_metrics("val"))


        for key, value in metrics_dict.items():
            self.log(f"val/{key}", value, sync_dist=self.sync_dist)

        if "gen_traj" not in self.val_plot_samples:
            return

        if "char" in self.modalities and "char_feat" in self.val_plot_samples:
            modality = ("char_feat", self.val_plot_samples["char_feat"].cpu())
        else:
            modality = (None, [])

        plots = self.draw_plots(
            gen_matrices=self.val_plot_samples["gen_traj"].cpu(),
            ref_matrices=self.val_plot_samples["ref_traj"].cpu(),
            masks=self.val_plot_samples["mask"].cpu(),
            modality=modality,
        )
        for plot_name, raw_plot in plots[0].figures.items():
            raw_plot.canvas.draw_idle()
            plot_data = np.frombuffer(raw_plot.canvas.tostring_rgb(), dtype=np.uint8)
            plot_data = plot_data.reshape(
                raw_plot.canvas.get_width_height()[::-1] + (3,)
            )
            plt.close(raw_plot)
            log_args = dict(
                key=f"val/plots/{plot_name}",
                images=[plot_data],
                step=self.global_step,
                caption=[f"[Epoch {self.current_epoch}]"],
            )
            if "caption" in self.val_plot_samples:
                log_args["caption"][0] += " " + self.val_plot_samples["caption"]
            self.logger.log_image(**log_args)

    # --------------------------------------------------------------------------------- #

    def on_test_start(self):
        if isinstance(self.metric_callback, functools.partial):
            self.metric_callback = self.metric_callback(device=self.device)

    def on_test_epoch_start(self):
        if not hasattr(self, "metrics_to_compute"):
            self.metrics_to_compute = ["distribution", "semantic"]

    def test_step(self, batch, batch_idx):
        data, mask = batch["traj_feat"], batch["padding_mask"]

        conds = dict()
        if len(self.modalities) > 0:
            cond_k = [x for x in batch.keys() if "traj" not in x and "feat" in x]
            cond_data = [batch[cond] for cond in cond_k]
            for cond in cond_k:
                cond_name = cond.replace("_feat", "")
                if isinstance(batch[f"{cond_name}_raw"], dict):
                    for cond_name_, x in batch[f"{cond_name}_raw"].items():
                        conds[cond_name_] = x
                else:
                    conds[cond_name] = batch[f"{cond_name}_raw"]
        else:
            cond_data = None

        if "caption" in self.modalities:
            clip_seq = batch["caption_raw"]["clip_seq_caption"]
            clip_seq_mask = batch["caption_raw"]["clip_seq_mask"]
        else:
            clip_seq, clip_seq_mask = None, None

        # cf edm2 sigma_data normalization / https://arxiv.org/pdf/2312.02696.pdf
        if self.edm2_normalization:
            data *= self.loss_fn.sigma_data
        _, gen_data = self.sample(self.ema.ema_model, data, cond_data, mask)

        with torch.autocast(device_type=data.device.type, dtype=data.dtype):
            ref_clatr = self.clatr.encode(
                {"x": data.permute(0, 2, 1), "mask": mask.to(bool)}
            )
            if clip_seq is not None:
                text_clatr = self.clatr.encode(
                    {"x": clip_seq, "mask": clip_seq_mask.to(bool)}
                )
            gen_clatr = self.clatr.encode(
                {"x": gen_data.permute(0, 2, 1), "mask": mask.to(bool)}
            )

        # Update distribution metrics
        self.metric_callback.update_clatr_metrics(
            "test", gen_clatr, ref_clatr, text_clatr
        )

        # Update semantic metrics
        if "segments" in conds:
            self.do_segment = True
            # Convert samples to raw pose matrices
            gen_matrices = torch.stack([self.get_matrix(x) for x in gen_data])
            # Project on SO(3) (if not in SO(3))
            p_gen_matrices = project_so3(gen_matrices.reshape(-1, 4, 4)).reshape(
                *gen_matrices.shape
            )
            self.metric_callback.update_caption_metrics(
                "test", p_gen_matrices, conds["segments"], mask
            )

    def on_test_epoch_end(self):
        metrics_dict = {}
        # Compute distribution metrics
        if "distribution" in self.metrics_to_compute:
            metrics_dict.update(self.metric_callback.compute_clatr_metrics("test"))

        # Compute semantic metrics
        if self.do_segment and "semantic" in self.metrics_to_compute:
            metrics_dict.update(self.metric_callback.compute_caption_metrics("test"))

        for k, v in metrics_dict.items():
            if isinstance(v, torch.Tensor):
                metrics_dict[k] = [v.item()]
            else:
                metrics_dict[k] = [v]

        self.metrics_dict = metrics_dict

    # --------------------------------------------------------------------------------- #

    def on_predict_start(self):
        eval_dataset = self.trainer.datamodule.eval_dataset
        self.modalities = list(eval_dataset.modality_datasets.keys())

        self.get_matrix = self.trainer.datamodule.train_dataset.get_matrix
        self.v_get_matrix = self.trainer.datamodule.eval_dataset.get_matrix

    def predict_step(self, batch, batch_idx):
        ref_samples, mask = batch["traj_feat"], batch["padding_mask"]

        if len(self.modalities) > 0:
            cond_k = [x for x in batch.keys() if "traj" not in x and "feat" in x]
            cond_data = [batch[cond] for cond in cond_k]
            conds = {}
            for cond in cond_k:
                cond_name = cond.replace("_feat", "")
                if isinstance(batch[f"{cond_name}_raw"], dict):
                    for cond_name_, x in batch[f"{cond_name}_raw"].items():
                        conds[cond_name_] = x
                else:
                    conds[cond_name] = batch[f"{cond_name}_raw"]
            batch["conds"] = conds
        else:
            cond_data = None

        # cf edm2 sigma_data normalization / https://arxiv.org/pdf/2312.02696.pdf
        if self.edm2_normalization:
            ref_samples *= self.loss_fn.sigma_data
        _, gen_samples = self.sample(self.ema.ema_model, ref_samples, cond_data, mask)

        batch["ref_samples"] = torch.stack([self.v_get_matrix(x) for x in ref_samples])
        batch["gen_samples"] = torch.stack([self.get_matrix(x) for x in gen_samples])

        return batch

    # --------------------------------------------------------------------------------- #

    def sample(
        self,
        net: torch.nn.Module,
        traj_samples: RawTrajectory,
        cond_samples: TensorType["num_samples", "num_feats"],
        mask: TensorType["num_samples", "num_feats"],
        external_seeds: List[int] = None,
    ) -> Tuple[RawTrajectory, RawTrajectory]:
        # Pick latents
        num_samples = traj_samples.shape[0]
        seeds = self.gen_seeds if hasattr(self, "gen_seeds") else range(num_samples)
        rnd = StackedRandomGenerator(self.device, seeds)

        sz = [num_samples, self.net.num_feats, self.net.num_cams]
        latents = rnd.randn_rn(sz, device=self.device)
        # Generate trajectories.
        generations = self.edm_sampler(
            net,
            latents,
            class_labels=cond_samples,
            mask=mask,
            randn_like=rnd.randn_like,
            guidance_weight=self.guidance_weight,
            # ----------------------------------- #
            num_steps=self.num_steps,
            sigma_min=self.sigma_min,
            sigma_max=self.sigma_max,
            rho=self.rho,
            S_churn=self.S_churn,
            S_min=self.S_min,
            S_max=self.S_max,
            S_noise=self.S_noise,
        )

        return latents, generations

    @staticmethod
    def edm_sampler(
        net,
        latents,
        class_labels=None,
        mask=None,
        guidance_weight=2.0,
        randn_like=torch.randn_like,
        num_steps=18,
        sigma_min=0.002,
        sigma_max=80,
        rho=7,
        S_churn=0,
        S_min=0,
        S_max=float("inf"),
        S_noise=1,
    ):
        # Time step discretization.
        step_indices = torch.arange(num_steps, device=latents.device)
        t_steps = (
            sigma_max ** (1 / rho)
            + step_indices
            / (num_steps - 1)
            * (sigma_min ** (1 / rho) - sigma_max ** (1 / rho))
        ) ** rho
        t_steps = torch.cat(
            [torch.as_tensor(t_steps), torch.zeros_like(t_steps[:1])]
        )  # t_N = 0

        # Main sampling loop.
        bool_mask = ~mask.to(bool)
        x_next = latents * t_steps[0]
        bs = latents.shape[0]
        for i, (t_cur, t_next) in enumerate(
            zip(t_steps[:-1], t_steps[1:])
        ):  # 0, ..., N-1
            x_cur = x_next

            # Increase noise temporarily.
            gamma = (
                min(S_churn / num_steps, np.sqrt(2) - 1)
                if S_min <= t_cur <= S_max
                else 0
            )
            t_hat = torch.as_tensor(t_cur + gamma * t_cur)
            x_hat = x_cur + (t_hat**2 - t_cur**2).sqrt() * S_noise * randn_like(x_cur)

            # Euler step.
            if class_labels is not None:
                class_label_knot = [torch.zeros_like(label) for label in class_labels]
                x_hat_both = torch.cat([x_hat, x_hat], dim=0)
                y_label_both = [
                    torch.cat([y, y_knot], dim=0)
                    for y, y_knot in zip(class_labels, class_label_knot)
                ]

                bool_mask_both = torch.cat([bool_mask, bool_mask], dim=0)
                t_hat_both = torch.cat([t_hat.expand(bs), t_hat.expand(bs)], dim=0)
                cond_denoised, denoised = net(
                    x_hat_both, t_hat_both, y=y_label_both, mask=bool_mask_both
                ).chunk(2, dim=0)
                denoised = denoised + (cond_denoised - denoised) * guidance_weight
            else:
                denoised = net(x_hat, t_hat.expand(bs), mask=bool_mask)
            d_cur = (x_hat - denoised) / t_hat
            x_next = x_hat + (t_next - t_hat) * d_cur

            # Apply 2nd order correction.
            if i < num_steps - 1:
                if class_labels is not None:
                    class_label_knot = [
                        torch.zeros_like(label) for label in class_labels
                    ]
                    x_next_both = torch.cat([x_next, x_next], dim=0)
                    y_label_both = [
                        torch.cat([y, y_knot], dim=0)
                        for y, y_knot in zip(class_labels, class_label_knot)
                    ]
                    bool_mask_both = torch.cat([bool_mask, bool_mask], dim=0)
                    t_next_both = torch.cat(
                        [t_next.expand(bs), t_next.expand(bs)], dim=0
                    )
                    cond_denoised, denoised = net(
                        x_next_both, t_next_both, y=y_label_both, mask=bool_mask_both
                    ).chunk(2, dim=0)
                    denoised = denoised + (cond_denoised - denoised) * guidance_weight
                else:
                    denoised = net(x_next, t_next.expand(bs), mask=bool_mask)
                d_prime = (x_next - denoised) / t_next
                x_next = x_hat + (t_next - t_hat) * (0.5 * d_cur + 0.5 * d_prime)

        return x_next

    # ---------------------------------------------------------------------------------- #

    @staticmethod
    def draw_plots(
        gen_matrices: TensorType["batch_size", "num_cams", 4, 4],
        noisy_matrices: TensorType["batch_size", "num_cams", 4, 4] = None,
        ref_matrices: TensorType["batch_size", "num_cams", 4, 4] = None,
        masks: TensorType["batch_size", "num_cams"] = None,
        plot_dir: Path = None,
        modality: Tuple[str, List[Any]] = (None, [], []),
    ) -> List[PlotCollection]:
        modality_name, modality_raws = modality
        plots, colormaps = [], []
        for index in range(len(gen_matrices)):
            sample_dict = {}
            mask = masks[index].to(bool)
            gen_se3 = [x for x in gen_matrices[index][mask].numpy()]
            sample_dict["gen_sample"] = PosePath3D(poses_se3=gen_se3)
            colormaps.append("Blues")
            if ref_matrices is not None:
                ref_se3 = [x for x in ref_matrices[index][mask].numpy()]
                sample_dict["ref_sample"] = PosePath3D(poses_se3=ref_se3)
                colormaps.append("Reds")
            if noisy_matrices is not None:
                noisy_se3 = [x for x in noisy_matrices[index][mask].numpy()]
                sample_dict["noisy_sample"] = PosePath3D(poses_se3=noisy_se3)
                colormaps.append("Greys")

            if modality_name == "char_centers":
                char_se3 = []
                for x in modality_raws[index][mask].numpy():
                    se3 = np.eye(4)
                    se3[:3, 3] = x
                    char_se3.append(se3)
                sample_dict["char_sample"] = PosePath3D(poses_se3=char_se3)
                colormaps.append("Greens")

            plot = draw_trajectories(sample_dict, colormaps=colormaps)
            plots.append(plot)

        return plots

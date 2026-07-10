from copy import deepcopy
import json
import math
from typing import Optional

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf
from lightning.pytorch.loggers.logger import Logger
from lightning.pytorch.loggers import TensorBoardLogger, WandbLogger
from lightning.pytorch.callbacks import ModelCheckpoint, LearningRateMonitor
from lightning.fabric.utilities.rank_zero import rank_zero_only

from src.datasets.datamodule import Datamodule
from src.callbacks.fix_nans import FixNANinGrad
from utils.random_utils import set_random_seed
import torch

torch.set_float32_matmul_precision("medium")


class JsonlLogger(Logger):
    def __init__(self, save_dir: str, name: str = "metrics") -> None:
        super().__init__()
        self._save_dir = save_dir
        self._name = name
        self._version = "."
        from pathlib import Path

        self.log_dir_path = Path(save_dir) / name
        self.log_dir_path.mkdir(parents=True, exist_ok=True)
        self.metrics_path = self.log_dir_path / "metrics.jsonl"

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def log_dir(self):
        return str(self.log_dir_path)

    @rank_zero_only
    def log_hyperparams(self, params, *args, **kwargs):
        path = self.log_dir_path / "hparams.json"
        try:
            payload = OmegaConf.to_container(params, resolve=True)
        except ValueError:
            payload = params
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    @rank_zero_only
    def log_metrics(self, metrics, step=None):
        record = {"step": step}
        for key, value in metrics.items():
            if hasattr(value, "detach"):
                value = value.detach().cpu().item()
            if isinstance(value, (int, float)) and math.isfinite(float(value)):
                record[key] = float(value)
        if len(record) > 1:
            with self.metrics_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, sort_keys=True) + "\n")

    @rank_zero_only
    def save(self):
        return None

    @rank_zero_only
    def finalize(self, status):
        return None


@hydra.main(version_base="1.3", config_path="../configs", config_name="config.yaml")
def main(config: DictConfig) -> Optional[float]:
    OmegaConf.register_new_resolver("eval", eval)

    set_random_seed(config.seed)

    dict_config = OmegaConf.to_container(config, resolve=True)

    if config.log_wandb:
        logger = WandbLogger(
            entity=config.entity,
            project=config.project_name,
            name=config.xp_name,
            save_dir=config.log_dir,
        )
        logger._wandb_init.update({"config": dict_config})
    else:
        try:
            logger = TensorBoardLogger(
                save_dir=config.log_dir,
                name="tensorboard",
                version=".",
            )
        except ModuleNotFoundError:
            logger = JsonlLogger(save_dir=config.log_dir, name="metrics")

    checkpoint_callback = ModelCheckpoint(
        every_n_epochs=config.save_and_sample_every, save_top_k=-1
    )
    fix_nan = FixNANinGrad(monitor=["train/loss"])

    lr_monitor = LearningRateMonitor(logging_interval="step")

    callbacks = [checkpoint_callback, fix_nan, lr_monitor]

    trainer = instantiate(config.trainer)(logger=logger, callbacks=callbacks)

    diffuser = instantiate(config.diffuser)

    dataset = instantiate(config.dataset)
    datamodule = Datamodule(
        deepcopy(dataset).set_split("train"),
        deepcopy(dataset).set_split("test"),
        config.batch_size,
        config.compnode.num_workers,
    )

    trainer.fit(model=diffuser, datamodule=datamodule, ckpt_path=config.checkpoint_path)


if __name__ == "__main__":
    main()

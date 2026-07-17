__all__ = [
    "JointHumanCameraTokenizerTrainer",
    "JointTrainerConfig",
    "TokenizerTrainer",
    "TrainerConfig",
]


def __getattr__(name: str):
    # Keep data/statistics utilities importable without optional training loggers.
    if name in {"JointHumanCameraTokenizerTrainer", "JointTrainerConfig"}:
        from .joint_trainer import JointHumanCameraTokenizerTrainer, JointTrainerConfig

        return {
            "JointHumanCameraTokenizerTrainer": JointHumanCameraTokenizerTrainer,
            "JointTrainerConfig": JointTrainerConfig,
        }[name]
    if name in {"TokenizerTrainer", "TrainerConfig"}:
        from .trainer import TokenizerTrainer, TrainerConfig

        return {"TokenizerTrainer": TokenizerTrainer, "TrainerConfig": TrainerConfig}[name]
    raise AttributeError(name)

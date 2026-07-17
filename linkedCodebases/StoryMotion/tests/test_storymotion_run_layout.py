from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.storymotion_run_layout import init_run, run_paths


class StoryMotionRunLayoutTest(unittest.TestCase):
    def test_new_stage2_run_uses_functional_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            result = init_run("stage2", "v8_test", runs_root=runs)
            paths = run_paths("stage2", "v8_test", runs)

            self.assertEqual(paths["root"], runs / "train/stage2/v8_test")
            self.assertEqual(paths["train"], paths["root"])
            self.assertEqual(paths["cache"], paths["root"] / "cache")
            self.assertEqual(paths["eval"], runs / "eval/stage2/v8_test")
            self.assertEqual(paths["vis"], runs / "vis/stage2/v8_test")
            self.assertEqual(result["root"], str(paths["root"]))

            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            self.assertEqual(manifest["layout"], "functional_roots_v1")
            self.assertEqual(manifest["path_base"], "runs_root")
            self.assertEqual(manifest["paths"]["train"], "train/stage2/v8_test")
            self.assertEqual(manifest["paths"]["eval"], "eval/stage2/v8_test")
            self.assertEqual(manifest["paths"]["vis"], "vis/stage2/v8_test")

    def test_new_stage1_run_keeps_contract_with_training_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            paths = run_paths("stage1", "v8_test", runs)

            self.assertEqual(paths["root"], runs / "train/stage1/v8_test")
            self.assertEqual(paths["contract"], paths["root"] / "experiment_contract.json")
            self.assertEqual(paths["checkpoints"], paths["root"] / "checkpoints")
            self.assertEqual(paths["tensorboard"], paths["root"] / "tensorboard")
            self.assertEqual(paths["eval"], runs / "eval/stage1/v8_test")
            self.assertEqual(paths["vis"], runs / "vis/stage1/v8_test")

    def test_existing_atomic_run_remains_readable_during_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            old_root = runs / "stage2/legacy_run"
            (old_root / "train").mkdir(parents=True)
            (old_root / "eval").mkdir()
            (old_root / "vis").mkdir()
            (old_root / "cache").mkdir()

            paths = run_paths("stage2", "legacy_run", runs)

            self.assertEqual(paths["root"], old_root)
            self.assertEqual(paths["train"], old_root / "train")
            self.assertEqual(paths["eval"], old_root / "eval")

    def test_functional_run_wins_when_both_layouts_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            (runs / "stage1/v8_test").mkdir(parents=True)
            canonical = runs / "train/stage1/v8_test"
            canonical.mkdir(parents=True)

            self.assertEqual(run_paths("stage1", "v8_test", runs)["root"], canonical)


if __name__ == "__main__":
    unittest.main()

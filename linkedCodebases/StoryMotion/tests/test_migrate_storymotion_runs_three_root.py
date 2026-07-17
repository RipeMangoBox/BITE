from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.migrate_storymotion_runs_three_root import Migration


class StoryMotionRunsMigrationTest(unittest.TestCase):
    def test_splits_atomic_stage2_run_and_keeps_compatibility_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "runs/stage2/run_a"
            for child in ("train", "cache", "eval", "vis"):
                (old / child).mkdir(parents=True)
            (old / "train/last.pt").write_text("checkpoint", encoding="utf-8")
            (old / "eval/joint.json").write_text("{}", encoding="utf-8")
            (old / "vis/sample.mp4").write_bytes(b"video")
            (old / "experiment_contract.json").write_text("{}", encoding="utf-8")

            Migration(root, apply=True, protected=set()).run()

            train = root / "runs/train/stage2/run_a"
            self.assertEqual((train / "last.pt").read_text(encoding="utf-8"), "checkpoint")
            self.assertTrue((root / "runs/eval/stage2/run_a/joint.json").is_file())
            self.assertTrue((root / "runs/vis/stage2/run_a/sample.mp4").is_file())
            self.assertTrue((old / "eval/joint.json").is_file())
            self.assertTrue(old.is_symlink())

    def test_protected_run_is_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "runs/stage1/active"
            (old / "train").mkdir(parents=True)

            payload = Migration(root, apply=True, protected={"active"}).run()

            self.assertTrue(old.is_dir())
            self.assertFalse((root / "runs/train/stage1/active").exists())
            self.assertTrue(any(action["operation"] == "protect_run" for action in payload["actions"]))

    def test_moves_result_categories_and_operations_out_of_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "runs/quality/q").mkdir(parents=True)
            (root / "runs/semantic_keyframe_mvp/e").mkdir(parents=True)
            (root / "runs/launchers/l").mkdir(parents=True)
            (root / "runs/visualizations/stage1/v").mkdir(parents=True)

            Migration(root, apply=True, protected=set()).run()

            self.assertTrue((root / "runs/eval/quality/q").is_dir())
            self.assertTrue((root / "runs/eval/semantic_keyframe_mvp/e").is_dir())
            self.assertTrue((root / "ops/launchers/l").is_dir())
            self.assertTrue((root / "runs/vis/stage1/v").is_dir())
            self.assertEqual((root / "runs/visualizations").resolve(), (root / "runs/vis").resolve())

            Migration(root, apply=True, protected=set()).run()
            self.assertEqual((root / "runs/visualizations").resolve(), (root / "runs/vis").resolve())

    def test_classifies_legacy_visualization_and_preserves_old_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "runs/visualizations/v7_14_official_contract_stage1_20260710"
            old.mkdir(parents=True)
            (old / "summary.json").write_text("{}", encoding="utf-8")

            Migration(root, apply=True, protected=set()).run()

            destination = root / "runs/vis/stage1/v7_14_official_contract_stage1_20260710"
            self.assertTrue((destination / "summary.json").is_file())
            self.assertTrue((root / "runs/vis/v7_14_official_contract_stage1_20260710").is_symlink())
            self.assertTrue((root / "runs/visualizations/v7_14_official_contract_stage1_20260710/summary.json").is_file())

    def test_moves_render_subtree_out_of_eval_with_compatibility_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "runs/eval/stage2/v7_13_mainA_20260710/renders_official_ae_mixed_last"
            source.mkdir(parents=True)
            (source / "manifest.json").write_text("{}", encoding="utf-8")

            Migration(root, apply=True, protected=set()).run()

            destination = root / "runs/vis/stage2/v7_13_mainA_20260710/renders_official_ae_mixed_last"
            self.assertTrue((destination / "manifest.json").is_file())
            self.assertTrue(source.is_symlink())

    def test_splits_contract_assets_from_driver_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "runs/contracts/v7_contract"
            source.mkdir(parents=True)
            (source / "train.pt").write_bytes(b"stats")
            (source / "formal_eval_driver.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            (source / "device_policy.json").write_text("{}", encoding="utf-8")

            Migration(root, apply=True, protected=set()).run()

            train_contract = root / "runs/train/stage2/shared/contracts/v7_contract"
            self.assertTrue((train_contract / "train.pt").is_file())
            self.assertFalse((train_contract / "formal_eval_driver.sh").exists())
            self.assertTrue((root / "ops/drivers/contracts/v7_contract/formal_eval_driver.sh").is_file())
            self.assertTrue((root / "ops/drivers/contracts/v7_contract/device_policy.json").is_file())
            self.assertTrue((root / "runs/contracts").is_symlink())

    def test_non_identical_collision_stops(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "runs/quality/q/result.json"
            destination = root / "runs/eval/quality/q/result.json"
            source.parent.mkdir(parents=True)
            destination.parent.mkdir(parents=True)
            source.write_text("source", encoding="utf-8")
            destination.write_text("destination", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "non-identical migration collision"):
                Migration(root, apply=True, protected=set()).run()

    def test_dry_run_does_not_mutate_atomic_or_visualization_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            atomic = root / "runs/stage2/run_a"
            (atomic / "train").mkdir(parents=True)
            visual = root / "runs/visualizations/v7_14_official_contract_stage1_20260710"
            visual.mkdir(parents=True)

            payload = Migration(root, apply=False, protected=set()).run()

            self.assertEqual(payload["status"], "planned")
            self.assertTrue((atomic / "train").is_dir())
            self.assertTrue(visual.is_dir())
            self.assertFalse((root / "runs/train").exists())

    def test_migrates_through_legacy_root_links_used_on_4090(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / "runs/legacy"
            for name in ("train", "eval", "visualizations"):
                (legacy / name).mkdir(parents=True)
                (root / "runs" / name).symlink_to(Path("legacy") / name)
            atomic = root / "runs/stage2/run_a"
            (atomic / "train").mkdir(parents=True)
            (atomic / "train/last.pt").write_bytes(b"checkpoint")
            visual = legacy / "visualizations/v7_14_official_contract_stage1_20260710"
            visual.mkdir(parents=True)
            (visual / "summary.json").write_text("{}", encoding="utf-8")

            Migration(root, apply=True, protected=set()).run()

            self.assertTrue((root / "runs/train/stage2/run_a/last.pt").is_file())
            self.assertTrue((root / "runs/vis/stage1/v7_14_official_contract_stage1_20260710/summary.json").is_file())
            self.assertEqual((root / "runs/visualizations").resolve(), (root / "runs/vis").resolve())


if __name__ == "__main__":
    unittest.main()

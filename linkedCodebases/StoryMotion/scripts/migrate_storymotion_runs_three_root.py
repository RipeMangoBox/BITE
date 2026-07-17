#!/usr/bin/env python3
"""Migrate generated StoryMotion artifacts to train/eval/vis roots.

The migration is local to one StoryMotion checkout. It never copies artifacts
between hosts, never overwrites a non-identical destination, and skips run ids
explicitly protected by the caller.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGES = ("stage1", "stage2")
OPS_NAMES = ("launchers", "queues", "registry", "env_overlays")

LEGACY_VIS_STAGE1 = frozenset(
    {
        "v6_2_joint_stage1_20260701",
        "v7_12_correct_fast_stage1_bigtitle_20260709",
        "v7_13_joint_default_stage1_bigtitle_20260710",
        "v7_13_pulp_ae_official_selftrained_stage1_bigtitle_20260709",
        "v7_13_pulp_ae_official_selftrained_stage1_smoke_20260709",
        "v7_13_sixrow_pretrained_stage1_20260710",
        "v7_13_sixrow_stage1_20260710",
        "v7_14_official_contract_stage1_20260710",
        "v7_5_stage1_joint_separate_20260707",
        "v7_5_stage1_joint_separate_bigtitle_20260707",
        "v7_6_stage1_humanloss_joint_20260707",
        "v7_6_stage1_humanloss_joint_bigtitle_20260707",
        "v7_7_stage1_noncausal_vae_bigtitle_20260707",
        "v7_8_pulp_pretrained_ae_20260708",
        "v7_8_stage1_noncausal_fsq_humanloss_bigtitle_20260708",
    }
)
LEGACY_VIS_STAGE2 = frozenset(
    {
        "screen_projection_probe_20260625",
        "v6_2_joint_stage2_20260701",
        "v7_20_completed_20260713",
        "v7_4_paired_audit_20260706",
        "v7_5_clean_audit_20260707",
    }
)

# These directories are render products embedded in historical eval trees. The
# smallest complete subtree moves with its local manifest; a compatibility
# symlink preserves the old evidence path.
EVAL_VIS_MOVES = (
    (
        "runs/eval/stage1/vis",
        "runs/vis/stage1/legacy_eval_vis_20260717",
    ),
    (
        "runs/eval/stage1/molingo_pulp199_vae_fast_eval_20260629/test_recon_vis_128",
        "runs/vis/stage1/molingo_pulp199_vae_fast_eval_20260629/test_recon_vis_128",
    ),
    (
        "runs/eval/stage1/molingo_pulp199_vae_mixed_eval_20260629/test_recon_vis_128",
        "runs/vis/stage1/molingo_pulp199_vae_mixed_eval_20260629/test_recon_vis_128",
    ),
    (
        "runs/eval/stage2/v7_13_mainA_20260710/renders_official_ae_mixed_last",
        "runs/vis/stage2/v7_13_mainA_20260710/renders_official_ae_mixed_last",
    ),
    (
        "runs/eval/stage2/v7_13_mainA_20260710/renders_v7_13_joint_ae_pure4053_last",
        "runs/vis/stage2/v7_13_mainA_20260710/renders_v7_13_joint_ae_pure4053_last",
    ),
    (
        "runs/eval/stage2/v7_15_matched_sym_asym_20260711/renders_asymmetric",
        "runs/vis/stage2/v7_15_matched_sym_asym_20260711/renders_asymmetric",
    ),
    (
        "runs/eval/stage2/v7_15_matched_sym_asym_20260711/renders_symmetric",
        "runs/vis/stage2/v7_15_matched_sym_asym_20260711/renders_symmetric",
    ),
    (
        "runs/eval/stage2/bilateral_cfg_pulpmotion_fair_compare_20260615",
        "runs/vis/stage2/bilateral_cfg_pulpmotion_fair_compare_20260615",
    ),
    (
        "runs/eval/stage2/bilateral_cfg_renders_20260614",
        "runs/vis/stage2/bilateral_cfg_renders_20260614",
    ),
    (
        "runs/eval/stage2/gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616",
        "runs/vis/stage2/gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616",
    ),
    (
        "runs/eval/stage2/joint_channel_gated_pulpmotion_fair_compare_20260615",
        "runs/vis/stage2/joint_channel_gated_pulpmotion_fair_compare_20260615",
    ),
    (
        "runs/eval/stage2/native_projection_fair_compare_20260617",
        "runs/vis/stage2/native_projection_fair_compare_20260617",
    ),
    (
        "runs/eval/stage2/stage2_trimodal_latent_render_20260612",
        "runs/vis/stage2/stage2_trimodal_latent_render_20260612",
    ),
    (
        "runs/eval/stage2/v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare",
        "runs/vis/stage2/v3_closure_20260616/gpu1_humjoint_besteval_pulpmotion_fair_compare",
    ),
    (
        "runs/eval/stage2/v3_closure_20260616/gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare",
        "runs/vis/stage2/v3_closure_20260616/gpu3_jointheavy_h2_besteval_pulpmotion_fair_compare",
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Migration:
    def __init__(self, root: Path, *, apply: bool, protected: set[str]) -> None:
        self.root = root.resolve()
        self.runs = self.root / "runs"
        self.apply = apply
        self.protected = protected
        self.actions: list[dict[str, Any]] = []
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.planned_removed: set[Path] = set()

    def record(self, operation: str, source: Path | None, destination: Path | None, **extra: Any) -> None:
        payload: dict[str, Any] = {"operation": operation}
        if source is not None:
            payload["source"] = str(source)
        if destination is not None:
            payload["destination"] = str(destination)
        payload.update(extra)
        self.actions.append(payload)

    def ensure_dir(self, path: Path) -> None:
        if path.exists():
            if not path.is_dir():
                raise RuntimeError(f"expected directory: {path}")
            return
        self.record("mkdir", None, path)
        if self.apply:
            path.mkdir(parents=True)

    def move(self, source: Path, destination: Path) -> None:
        if not source.exists() and not source.is_symlink():
            return
        if destination.exists() or destination.is_symlink():
            self.merge(source, destination)
            return
        self.record("rename", source, destination)
        self.planned_removed.add(source)
        if self.apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)

    def merge(self, source: Path, destination: Path) -> None:
        if source.is_symlink() or destination.is_symlink():
            raise RuntimeError(f"refusing to merge through symlink: {source} -> {destination}")
        if source.is_dir() and destination.is_dir():
            for child in sorted(source.iterdir(), key=lambda item: item.name):
                self.move(child, destination / child.name)
            self.record("rmdir", source, None)
            self.planned_removed.add(source)
            if self.apply:
                source.rmdir()
            return
        if source.is_file() and destination.is_file():
            if source.stat().st_size == destination.stat().st_size and sha256_file(source) == sha256_file(destination):
                self.record("deduplicate_identical", source, destination)
                self.planned_removed.add(source)
                if self.apply:
                    source.unlink()
                return
        raise RuntimeError(f"non-identical migration collision: {source} -> {destination}")

    def symlink(self, link: Path, target: Path) -> None:
        relative_target = os.path.relpath(target, link.parent)
        if link in self.planned_removed:
            self.record("symlink", None, link, target=relative_target)
            if self.apply:
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(relative_target)
            return
        if link.is_symlink():
            if os.readlink(link) == relative_target:
                return
            raise RuntimeError(f"different compatibility symlink already exists: {link}")
        if link.exists():
            raise RuntimeError(f"cannot create compatibility symlink over path: {link}")
        self.record("symlink", None, link, target=relative_target)
        if self.apply:
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(relative_target)

    def split_atomic_run(self, stage: str, source: Path) -> None:
        run_id = source.name
        if run_id in self.protected:
            self.record("protect_run", source, None, run_id=run_id)
            return
        train_root = self.runs / "train" / stage / run_id
        eval_root = self.runs / "eval" / stage / run_id
        vis_root = self.runs / "vis" / stage / run_id
        if train_root.exists() or train_root.is_symlink():
            raise RuntimeError(f"train run collision: {source} -> {train_root}")

        source_train = source / "train"
        if source_train.exists():
            self.move(source_train, train_root)
        else:
            self.ensure_dir(train_root)

        for name, destination in (("eval", eval_root), ("vis", vis_root)):
            child = source / name
            if child.exists():
                self.move(child, destination)
            else:
                self.ensure_dir(destination)

        if stage == "stage2" and (source / "cache").exists():
            self.move(source / "cache", train_root / "cache")

        for child in sorted(source.iterdir(), key=lambda item: item.name):
            if child.name in {"train", "eval", "vis", "cache"}:
                continue
            self.move(child, train_root / child.name)
        self.record("rmdir", source, None)
        self.planned_removed.add(source)
        if self.apply:
            source.rmdir()

        self.symlink(train_root / "eval", eval_root)
        self.symlink(train_root / "vis", vis_root)
        self.symlink(source, train_root)

    def migrate_stage(self, stage: str) -> None:
        source_root = self.runs / stage
        if not source_root.exists() or source_root.is_symlink():
            return

        special: dict[str, Path] = {}
        if stage == "stage2":
            special = {
                "metrics": self.runs / "eval/stage2/legacy_runroot_metrics_20260717",
                "vis": self.runs / "vis/stage2/legacy_runroot_vis_20260717",
                "shared": self.runs / "train/stage2/shared/legacy_atomic_shared_20260717",
                "analysis": self.root / "archive/operations/stage2_runroot_legacy_20260717/analysis",
                "commands": self.root / "ops/drivers/stage2_runroot_legacy_20260717/commands",
            }
            for name, destination in special.items():
                self.move(source_root / name, destination)

        for child in sorted(source_root.iterdir(), key=lambda item: item.name):
            if child.name in special:
                continue
            if child.is_symlink():
                continue
            if child.is_dir():
                self.split_atomic_run(stage, child)
            else:
                self.move(child, self.root / "ops/legacy_stage_roots" / stage / child.name)

    def migrate_visualizations(self) -> None:
        source = self.runs / "visualizations"
        if not source.exists() and not source.is_symlink():
            return
        destination_root = self.runs / "vis"
        real_source = source.resolve() if source.is_symlink() else source
        if source.is_symlink() and real_source == destination_root.resolve():
            return
        for child in sorted(real_source.iterdir(), key=lambda item: item.name):
            if child.name in STAGES:
                destination = destination_root / child.name
                self.move(child, destination)
                continue
            if child.name in LEGACY_VIS_STAGE1:
                stage = "stage1"
            elif child.name in LEGACY_VIS_STAGE2:
                stage = "stage2"
            else:
                raise RuntimeError(f"unclassified legacy visualization subtree: {child}")
            destination = destination_root / stage / child.name
            self.move(child, destination)
            self.symlink(destination_root / child.name, destination)
        self.record("rmdir", real_source, None)
        self.planned_removed.add(real_source)
        if self.apply:
            real_source.rmdir()
        if source.is_symlink():
            self.record("unlink", source, None)
            self.planned_removed.add(source)
            if self.apply:
                source.unlink()
        self.symlink(source, self.runs / "vis")

    def migrate_contracts(self) -> None:
        source = self.runs / "contracts"
        if not source.exists() or source.is_symlink():
            return
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix == ".sh" or "policy" in path.name.lower():
                relative = path.relative_to(source)
                self.move(path, self.root / "ops/drivers/contracts" / relative)
        destination = self.runs / "train/stage2/shared/contracts"
        self.move(source, destination)
        self.symlink(source, destination)

    def migrate_eval_visualizations(self) -> None:
        for source_relative, destination_relative in EVAL_VIS_MOVES:
            source = self.root / source_relative
            destination = self.root / destination_relative
            if source.is_symlink() and source.resolve() == destination.resolve():
                continue
            if not source.exists() and not source.is_symlink():
                continue
            self.move(source, destination)
            self.symlink(source, destination)

    def migrate_categories(self) -> None:
        self.move(self.runs / "quality", self.runs / "eval/quality")
        self.move(self.runs / "semantic_keyframe_mvp", self.runs / "eval/semantic_keyframe_mvp")
        self.migrate_contracts()
        for name in OPS_NAMES:
            self.move(self.runs / name, self.root / "ops" / name)

        archive = self.runs / "archive"
        if archive.exists():
            for child in sorted(archive.glob("failed_start_*")):
                self.move(child, self.runs / "train/stage2/_failed" / child.name)
            self.move(archive, self.root / "archive/runs_legacy_20260717")

    def run(self) -> dict[str, Any]:
        for path in (self.runs / "train", self.runs / "eval", self.runs / "vis"):
            self.ensure_dir(path)
        self.migrate_categories()
        self.migrate_visualizations()
        for stage in STAGES:
            self.migrate_stage(stage)
        self.migrate_eval_visualizations()
        return self.payload(status="completed" if self.apply else "planned")

    def payload(self, *, status: str, error: str | None = None) -> dict[str, Any]:
        payload = {
            "schema_version": 1,
            "created_at": self.created_at,
            "root": str(self.root),
            "mode": "apply" if self.apply else "dry_run",
            "status": status,
            "protected_run_ids": sorted(self.protected),
            "actions": self.actions,
        }
        if error is not None:
            payload["error"] = error
        return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="StoryMotion project root")
    parser.add_argument("--apply", action="store_true", help="perform checked same-filesystem renames")
    parser.add_argument("--protect-run-id", action="append", default=[])
    parser.add_argument("--manifest", type=Path, help="write the action manifest as JSON")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    migration = Migration(args.root, apply=args.apply, protected=set(args.protect_run_id))
    try:
        payload = migration.run()
    except Exception as error:
        payload = migration.payload(status="failed", error=f"{type(error).__name__}: {error}")
        serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.manifest:
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            args.manifest.write_text(serialized, encoding="utf-8")
        print(serialized, end="")
        raise
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()

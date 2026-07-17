#!/usr/bin/env python3
"""Canonical Stage1/Stage2 experiment paths for StoryMotion.

New runs share one run id across the functional ``runs/train``, ``runs/eval``
and ``runs/vis`` roots. Existing atomic ``runs/stage1`` and ``runs/stage2``
bundles remain readable during migration.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS_ROOT = ROOT / "runs"
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def validate_run_id(run_id: str) -> str:
    if not _RUN_ID_RE.fullmatch(run_id):
        raise ValueError(
            "run_id must contain only letters, digits, '.', '_' or '-' and must not contain '/': "
            f"{run_id!r}"
        )
    return run_id


def _functional_run_paths(stage: str, run_id: str, runs_root: Path) -> dict[str, Path]:
    train_root = runs_root / "train" / stage / run_id
    paths: dict[str, Path] = {
        "root": train_root,
        "manifest": train_root / "manifest.json",
        "contract": train_root / "experiment_contract.json",
        "train": train_root,
        "eval": runs_root / "eval" / stage / run_id,
        "vis": runs_root / "vis" / stage / run_id,
    }
    if stage == "stage1":
        paths.update(
            {
                "checkpoints": train_root / "checkpoints",
                "tensorboard": train_root / "tensorboard",
            }
        )
    else:
        paths["cache"] = train_root / "cache"
    return paths


def _atomic_run_paths(stage: str, run_id: str, runs_root: Path) -> dict[str, Path]:
    root = runs_root / stage / run_id
    paths: dict[str, Path] = {
        "root": root,
        "manifest": root / "manifest.json",
        "contract": root / "experiment_contract.json",
        "train": root / "train",
        "eval": root / "eval",
        "vis": root / "vis",
    }
    if stage == "stage1":
        paths.update(
            {
                "checkpoints": root / "train" / "checkpoints",
                "tensorboard": root / "train" / "tensorboard",
            }
        )
    else:
        paths["cache"] = root / "cache"
    return paths


def run_paths(stage: str, run_id: str, runs_root: Path | None = None) -> dict[str, Path]:
    if stage not in {"stage1", "stage2"}:
        raise ValueError(f"stage must be 'stage1' or 'stage2', got {stage!r}")
    validate_run_id(run_id)
    root = runs_root or DEFAULT_RUNS_ROOT
    functional = _functional_run_paths(stage, run_id, root)
    atomic = _atomic_run_paths(stage, run_id, root)
    if atomic["root"].exists() and not functional["root"].exists():
        return atomic
    return functional


def init_run(
    stage: str,
    run_id: str,
    *,
    runs_root: Path | None = None,
    parent_stage1_run: str | None = None,
    description: str = "",
) -> dict[str, Any]:
    if stage == "stage2" and parent_stage1_run:
        validate_run_id(parent_stage1_run)
    root = runs_root or DEFAULT_RUNS_ROOT
    paths = run_paths(stage, run_id, root)
    paths["root"].mkdir(parents=True, exist_ok=False)
    for key, path in paths.items():
        if key not in {"root", "manifest", "contract"}:
            path.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "layout": "functional_roots_v1",
        "path_base": "runs_root",
        "stage": stage,
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": description,
        "parent_stage1_run": parent_stage1_run if stage == "stage2" else None,
        "paths": {key: str(path.relative_to(root)) for key, path in paths.items() if key not in {"root", "manifest"}},
        "status": "initialized",
    }
    paths["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"manifest": str(paths["manifest"]), **{key: str(path) for key, path in paths.items()}}


def inventory_legacy(runs_root: Path | None = None) -> dict[str, Any]:
    """List legacy top-level run families without walking large artifacts."""
    root = runs_root or DEFAULT_RUNS_ROOT
    families: dict[str, list[dict[str, Any]]] = {}
    for family in ("train", "eval", "visualizations", "audit", "quality", "smoke", "agent_logs", "tmp", "archive"):
        family_root = root / family
        if not family_root.exists():
            continue
        entries = []
        for entry in sorted(family_root.iterdir(), key=lambda value: value.name):
            entries.append(
                {
                    "path": str(entry.relative_to(root)),
                    "kind": "directory" if entry.is_dir() else "file",
                }
            )
        families[family] = entries
    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runs_root": str(root),
        "policy": "legacy paths are read-only; new runs share one run id across train, eval and vis",
        "families": families,
    }


def update_manifest(
    stage: str,
    run_id: str,
    *,
    runs_root: Path | None = None,
    status: str | None = None,
    artifacts: dict[str, str] | None = None,
) -> dict[str, Any]:
    manifest_path = run_paths(stage, run_id, runs_root)["manifest"]
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if status:
        manifest["status"] = status
    if artifacts:
        manifest.setdefault("artifacts", {}).update(artifacts)
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("init", "paths", "inventory", "update"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
        if command in {"init", "paths", "update"}:
            sub.add_argument("--stage", choices=["stage1", "stage2"], required=True)
            sub.add_argument("--run-id", required=True)
        if command == "init":
            sub.add_argument("--parent-stage1-run")
            sub.add_argument("--description", default="")
        if command == "inventory":
            sub.add_argument("--output", type=Path)
        if command == "update":
            sub.add_argument("--status")
            sub.add_argument("--artifact", action="append", default=[], metavar="KEY=VALUE")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "paths":
        print(json.dumps({key: str(value) for key, value in run_paths(args.stage, args.run_id, args.runs_root).items()}, indent=2, sort_keys=True))
        return
    if args.command == "inventory":
        payload = inventory_legacy(args.runs_root)
        serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(serialized, encoding="utf-8")
        print(serialized, end="")
        return
    if args.command == "update":
        artifacts = {}
        for item in args.artifact:
            if "=" not in item:
                raise ValueError(f"--artifact must be KEY=VALUE, got {item!r}")
            key, value = item.split("=", 1)
            artifacts[key] = value
        print(
            json.dumps(
                update_manifest(args.stage, args.run_id, runs_root=args.runs_root, status=args.status, artifacts=artifacts),
                indent=2,
                sort_keys=True,
            )
        )
        return
    result = init_run(
        args.stage,
        args.run_id,
        runs_root=args.runs_root,
        parent_stage1_run=args.parent_stage1_run,
        description=args.description,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

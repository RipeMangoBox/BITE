#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "configs/storymotion_v72_experiments.json"


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
    ids = [item["id"] for item in manifest["experiments"]]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate experiment ids in {path}")
    return manifest


def fmt(value: str, mapping: dict[str, str]) -> str:
    return value.format(**mapping)


def without_option(args: list[str], option: str) -> list[str]:
    out: list[str] = []
    idx = 0
    while idx < len(args):
        if args[idx] == option:
            idx += 2
            continue
        out.append(args[idx])
        idx += 1
    return out


def build_commands(manifest: dict[str, Any], exp: dict[str, Any], device: str | None) -> list[list[str]]:
    cache_dir = exp.get("cache_dir", manifest["cache_dir"])
    mapping = {
        "cache_dir": cache_dir,
        "output_dir": exp["output_dir"],
        "checkpoint": exp.get("checkpoint", ""),
        "base_checkpoint": exp.get("base_checkpoint", exp.get("resume_from", "")),
        "run_dir": exp.get("run_dir", ""),
    }
    if exp["kind"] == "train":
        command = ["python", "scripts/train_stage2_condmdi_pulp.py"]
        base_args = list(manifest["base_train_args"])
        if exp.get("steps"):
            base_args = without_option(base_args, "--steps")
        command.extend(base_args)
        command.extend(["--cache-dir", cache_dir, "--output-dir", exp["output_dir"]])
        if exp.get("steps"):
            command.extend(["--steps", str(exp["steps"])])
        base_checkpoint = exp.get("base_checkpoint", exp.get("resume_from"))
        if base_checkpoint:
            command.extend(["--resume", base_checkpoint])
        if device:
            command.extend(["--device", device])
        command.extend(exp.get("extra_args", []))
        return [command]
    if "commands" in exp:
        return [[fmt(str(part), mapping) for part in command] for command in exp["commands"]]
    if "command" not in exp:
        raise ValueError(f"experiment {exp['id']} has no command")
    return [[fmt(str(part), mapping) for part in exp["command"]]]


def output_path_for(exp: dict[str, Any]) -> Path:
    out = ROOT / exp["output_dir"]
    if exp["kind"] == "probe":
        return out
    return out


def ensure_no_conflict(exp: dict[str, Any], allow_existing: bool) -> None:
    out = output_path_for(exp)
    if allow_existing or not out.exists():
        return
    try:
        next(out.iterdir())
    except StopIteration:
        return
    raise FileExistsError(f"{exp['id']} output exists and is non-empty: {out}")


def validate_inputs(exp: dict[str, Any]) -> None:
    for key in ("base_checkpoint", "checkpoint", "run_dir"):
        value = exp.get(key)
        if value and not (ROOT / value).exists():
            raise FileNotFoundError(f"{exp['id']} {key} does not exist: {ROOT / value}")


def write_command_record(command_dir: Path, exp: dict[str, Any], commands: list[list[str]], execute: bool) -> Path:
    command_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "id": exp["id"],
        "kind": exp["kind"],
        "priority": exp.get("priority"),
        "description": exp.get("description"),
        "depends_on": exp.get("depends_on"),
        "output_dir": exp.get("output_dir"),
        "base_checkpoint": exp.get("base_checkpoint", exp.get("resume_from")),
        "checkpoint": exp.get("checkpoint"),
        "run_dir": exp.get("run_dir"),
        "v72_flags": [part for command in commands for part in command if part.startswith("--v72-")],
        "commands": commands,
        "shell": [" ".join(shlex.quote(part) for part in command) for command in commands],
        "execute": execute,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    path = command_dir / f"{exp['id'].lower()}_{exp['kind']}.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--experiment", action="append", help="Experiment id to emit. Defaults to all E0-E5.")
    parser.add_argument("--device", help="Training device override, for example cuda:0.")
    parser.add_argument("--execute", action="store_true", help="Run commands after writing command records.")
    parser.add_argument("--allow-existing", action="store_true", help="Allow non-empty output dirs.")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    wanted = set(args.experiment or [item["id"] for item in manifest["experiments"]])
    unknown = wanted - {item["id"] for item in manifest["experiments"]}
    if unknown:
        raise ValueError(f"unknown experiment ids: {sorted(unknown)}")

    command_dir = ROOT / "runs/train/stage2/v7_2/_commands"
    for exp in manifest["experiments"]:
        if exp["id"] not in wanted:
            continue
        ensure_no_conflict(exp, args.allow_existing)
        if args.execute:
            validate_inputs(exp)
        commands = build_commands(manifest, exp, args.device)
        record_path = write_command_record(command_dir, exp, commands, args.execute)
        shell = [" ".join(shlex.quote(part) for part in command) for command in commands]
        print(
            json.dumps(
                {
                    "id": exp["id"],
                    "kind": exp["kind"],
                    "output_dir": exp.get("output_dir"),
                    "depends_on": exp.get("depends_on"),
                    "base_checkpoint": exp.get("base_checkpoint", exp.get("resume_from")),
                    "checkpoint": exp.get("checkpoint"),
                    "record": str(record_path),
                    "commands": shell,
                },
                ensure_ascii=False,
            )
        )
        if args.execute:
            output_path_for(exp).mkdir(parents=True, exist_ok=True)
            for command in commands:
                subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()

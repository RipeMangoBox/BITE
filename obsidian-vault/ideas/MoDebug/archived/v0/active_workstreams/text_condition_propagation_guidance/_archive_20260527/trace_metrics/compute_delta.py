#!/usr/bin/env python3
"""Generate synthetic MoDebug forward traces for validator smoke tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def _compact_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _write_forward_npz(path: Path, signal: np.ndarray, meta: dict[str, Any], axis_names: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        signal=signal.astype(np.float32),
        valid_mask=np.ones(signal.shape, dtype=bool),
        meta_json=np.array(_compact_json(meta)),
        axis_names_json=np.array(json.dumps(axis_names, ensure_ascii=True)),
    )


def _signals(seed: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    base = rng.normal(loc=0.0, scale=0.15, size=(4, 6)).astype(np.float32)
    text_shift = np.array(
        [
            [0.80, 0.20, -0.10, -0.15, 0.05, -0.05],
            [0.10, 0.70, 0.10, -0.10, -0.05, -0.05],
            [-0.10, 0.00, 0.85, 0.20, -0.10, -0.05],
            [0.05, -0.05, 0.20, 0.75, -0.10, -0.05],
        ],
        dtype=np.float32,
    )
    counter_shift = np.array(
        [
            [-0.05, 0.10, 0.20, 0.75, -0.10, -0.05],
            [-0.10, 0.00, 0.85, 0.20, -0.10, -0.05],
            [0.10, 0.70, 0.10, -0.10, -0.05, -0.05],
            [0.80, 0.20, -0.10, -0.15, 0.05, -0.05],
        ],
        dtype=np.float32,
    )
    null_noise = rng.normal(loc=0.0, scale=0.03, size=base.shape).astype(np.float32)
    return {
        "text": base + text_shift,
        "null": base + null_noise,
        "counterfactual": base + counter_shift,
    }


def generate(output_dir: Path, run_id: str, seed: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "forward_manifest.jsonl"
    if manifest_path.exists():
        manifest_path.unlink()

    sample_id = "original100_dummy_000"
    common = {
        "run_id": run_id,
        "sample_id": sample_id,
        "model": "dummy_trace_model",
        "model_family": "synthetic",
        "z_kind": "synthetic_step",
        "z_id": "iter_00",
        "f_name": "token_logits",
        "f_space": "vocab_logits",
        "role": "diagnostic",
        "used_for": "observation",
        "limitations": "Synthetic dummy trace only; not a final evaluator.",
    }
    condition_texts = {
        "text": "a person walks forward then turns left",
        "null": "[NULL]",
        "counterfactual": "a person walks backward then turns right",
    }
    paired = {
        "text": "null",
        "null": "text",
        "counterfactual": "text",
    }
    axis_names = ["time_step", "vocab_index"]
    rows = []
    for condition_id, signal in _signals(seed).items():
        path = output_dir / f"{condition_id}.npz"
        meta = {
            **common,
            "condition_id": condition_id,
            "condition_text": condition_texts[condition_id],
            "paired_condition_id": paired[condition_id],
        }
        _write_forward_npz(path, signal, meta, axis_names)
        rows.append(
            {
                **common,
                "condition_id": condition_id,
                "condition_text": condition_texts[condition_id],
                "paired_condition_id": paired[condition_id],
                "forward_npz_path": str(path),
                "motion_artifact_path": f"dummy://synthetic_motion/{sample_id}",
            }
        )

    with manifest_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(_compact_json(row) + "\n")
    print(f"OK dummy-forward output_dir={output_dir} manifest={manifest_path} rows={len(rows)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--run-id", default="20260527_000000_agent_c_dummy")
    parser.add_argument("--seed", default=7, type=int)
    args = parser.parse_args()
    generate(args.output_dir, args.run_id, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

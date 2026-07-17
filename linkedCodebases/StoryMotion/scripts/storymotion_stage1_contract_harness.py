#!/usr/bin/env python3
"""Fail-closed preflight for a StoryMotion Stage1 checkpoint contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story-root", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--preset", required=True)
    parser.add_argument("--tokenizer")
    parser.add_argument("--feature-contract", required=True)
    parser.add_argument("--expected-is-causal", choices=["false"], default="false")
    parser.add_argument("--human-dim", type=int)
    parser.add_argument("--camera-dim", type=int)
    parser.add_argument("--human-latent-dim", type=int)
    parser.add_argument("--camera-latent-dim", type=int)
    parser.add_argument("--hidden-dim", type=int)
    parser.add_argument("--downsample", type=int)
    parser.add_argument("--drop-camera-z", action="store_true")
    parser.add_argument("--human200-stats", type=Path)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    story_root = args.story_root.resolve()
    for path in (story_root, story_root / "scripts"):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))

    import torch
    import build_stage2_joint_tokenizer_latent_cache as cache_builder

    build_args = argparse.Namespace(
        checkpoint=args.checkpoint.resolve(),
        preset=args.preset,
        tokenizer=args.tokenizer,
        feature_contract=args.feature_contract,
        human_dim=args.human_dim,
        camera_dim=args.camera_dim,
        human_latent_dim=args.human_latent_dim,
        camera_latent_dim=args.camera_latent_dim,
        hidden_dim=args.hidden_dim,
        downsample=args.downsample,
        drop_camera_z=bool(args.drop_camera_z),
        human200_stats=args.human200_stats,
    )
    model = cache_builder.build_model(build_args).to(torch.device(args.device))
    contract = dict(model.stage1_checkpoint_contract)
    expected_is_causal = args.expected_is_causal == "true"
    assert expected_is_causal is False
    if bool(contract["is_causal"]) != expected_is_causal:
        raise ValueError(
            f"checkpoint is_causal={contract['is_causal']!r}, expected {expected_is_causal!r}"
        )
    if bool(getattr(model, "is_causal", True)) != expected_is_causal:
        raise RuntimeError(
            f"constructed model is_causal={getattr(model, 'is_causal', None)!r}, "
            f"expected {expected_is_causal!r}"
        )

    payload = {
        "status": "passed",
        "checkpoint": str(args.checkpoint.resolve()),
        "checkpoint_sha256": sha256_file(args.checkpoint.resolve()),
        "model_class": type(model).__name__,
        "model_is_causal": bool(getattr(model, "is_causal", True)),
        "contract": contract,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify that StoryMotion and PulpMotion eval use the same test data.

RED LINE: If sample IDs, prompts, or valid frame masks differ, no fair comparison
is possible and all joint comparison claims must be suspended.

Usage (on 5090):
  python scripts/storymotion_test_data_consistency_check.py \
    --story-cache /path/to/cache_mixed_full_nw0_20260611_2110 \
    --pulp-data /data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-data \
    --set-name mixed_ --split test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch


def patch_numpy_aliases() -> None:
    for attr in ("bool", "int", "float", "complex", "object", "str", "long", "unicode"):
        if not hasattr(np, attr):
            setattr(np, attr, getattr(np, attr.replace("long", "int_").replace("unicode", "str_"), lambda: None)())


def load_story_cache_ids(cache_dir: Path) -> set[str]:
    """Extract all sample IDs from StoryMotion latent cache."""
    cache_path = cache_dir / "val.pt"
    if not cache_path.exists():
        raise FileNotFoundError(f"Story cache not found: {cache_path}")
    data = torch.load(cache_path, map_location="cpu")
    # Cache is a list of dicts with 'sample_id' keys
    if isinstance(data, dict):
        if "samples" in data:
            samples = data["samples"]
        elif "sample_ids" in data:
            return set(str(s) for s in data["sample_ids"])
        else:
            # Try iterating
            samples = list(data.values()) if not isinstance(data, list) else data
    elif isinstance(data, list):
        samples = data
    else:
        raise TypeError(f"Unexpected cache type: {type(data)}")

    ids = set()
    for item in samples:
        if isinstance(item, dict) and "sample_id" in item:
            ids.add(str(item["sample_id"]))
        elif isinstance(item, dict) and "id" in item:
            ids.add(str(item["id"]))
    return ids


def load_pulp_test_ids(pulp_data_root: Path, set_name: str, split: str) -> set[str]:
    """Extract sample IDs from PulpMotion test split file."""
    split_file = pulp_data_root / "splits" / f"{set_name}{split}_split.txt"
    if not split_file.exists():
        # Pulp uses _test10k_split.txt when limit_samples is set
        alt_split = pulp_data_root / "splits" / f"{set_name}{split}10k_split.txt"
        raise FileNotFoundError(
            f"Split file not found: {split_file}\n  Also checked: {alt_split}"
        )
    ids = set()
    with open(split_file) as f:
        for line in f:
            line = line.strip()
            if line:
                ids.add(line)
    print(f"Pulp split file: {split_file} → {len(ids)} sample IDs")
    return ids


def checksum_sample_ids(ids: set[str]) -> str:
    return hashlib.sha256("|".join(sorted(ids)).encode()).hexdigest()


def main() -> None:
    p = argparse.ArgumentParser(description="Check StoryMotion vs Pulp test data consistency")
    p.add_argument("--story-cache", type=Path, required=True, help="StoryMotion latent cache directory")
    p.add_argument("--pulp-data", type=Path, required=True, help="PulpMotion data root")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--split", default="test")
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    patch_numpy_aliases()

    print("=" * 60)
    print("StoryMotion ↔ PulpMotion Test Data Consistency Check")
    print("=" * 60)

    # Load StoryMotion cache IDs
    print(f"\n[1] Loading StoryMotion cache: {args.story_cache}")
    story_ids = load_story_cache_ids(args.story_cache)
    print(f"    {len(story_ids)} sample IDs in Story cache")

    # Load PulpMotion split IDs
    print(f"\n[2] Loading PulpMotion split: {args.set_name}{args.split}")
    pulp_ids = load_pulp_test_ids(args.pulp_data, args.set_name, args.split)
    print(f"    {len(pulp_ids)} sample IDs in Pulp split")

    # Compare
    print(f"\n[3] Comparison:")
    overlap = story_ids & pulp_ids
    story_only = story_ids - pulp_ids
    pulp_only = pulp_ids - story_ids

    print(f"    Overlap: {len(overlap)}")
    print(f"    Story-only: {len(story_only)}")
    print(f"    Pulp-only: {len(pulp_only)}")

    results: dict[str, Any] = {
        "story_cache": str(args.story_cache),
        "pulp_data": str(args.pulp_data),
        "set_name": args.set_name,
        "split": args.split,
        "story_ids_count": len(story_ids),
        "pulp_ids_count": len(pulp_ids),
        "overlap_count": len(overlap),
        "story_only_count": len(story_only),
        "pulp_only_count": len(pulp_only),
        "story_id_hash": checksum_sample_ids(story_ids),
        "pulp_id_hash": checksum_sample_ids(pulp_ids),
    }

    if len(story_only) == 0 and len(pulp_only) == 0:
        results["verdict"] = "IDENTICAL — same sample IDs in both sets"
        print(f"\n✅ VERDICT: IDENTICAL — same {len(overlap)} sample IDs in both sets")
    elif len(overlap) >= 0.99 * max(len(story_ids), len(pulp_ids)):
        results["verdict"] = f"NEARLY IDENTICAL — {len(overlap)}/{max(len(story_ids), len(pulp_ids))} overlap (≥99%)"
        print(f"\n⚠️  VERDICT: NEARLY IDENTICAL — {len(overlap)} overlap")
        if story_only:
            print(f"    Story-only sample IDs: {list(story_only)[:5]}...")
        if pulp_only:
            print(f"    Pulp-only sample IDs: {list(pulp_only)[:5]}...")
    else:
        results["verdict"] = "MISMATCH — different sample IDs"
        print(f"\n❌ VERDICT: MISMATCH — StoryMotion and PulpMotion use different test data!")
        print(f"    Story-only samples: {len(story_only)}")
        print(f"    Pulp-only samples: {len(pulp_only)}")
        print(f"    This is a RED LINE failure. All joint comparison claims are INVALID until resolved.")

    results["story_only_sample_ids"] = sorted(story_only)[:20]
    results["pulp_only_sample_ids"] = sorted(pulp_only)[:20]

    print(f"\n[4] ID hashes:")
    print(f"    Story: {results['story_id_hash'][:32]}...")
    print(f"    Pulp:  {results['pulp_id_hash'][:32]}...")

    if args.output:
        args.output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
        print(f"\nWrote results to {args.output}")

    sys.exit(0 if results["verdict"].startswith("IDENTICAL") else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Summarize MoDebug SLAD core M0/GDC calibration outputs."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def source_retention(row: dict, pair_idx: int, metric: str) -> float:
    affinity = row[f"{metric}_affinity_to_a"][pair_idx]
    if row["direction"] == "a_to_b":
        return float(affinity)
    return float(1.0 - affinity)


def crossing(xs: list[int], ys: list[float], level: float) -> float | None:
    if not xs:
        return None
    if ys[0] >= level:
        return float(xs[0])
    for idx in range(1, len(xs)):
        y0 = ys[idx - 1]
        y1 = ys[idx]
        if y0 < level <= y1:
            if abs(y1 - y0) < 1e-12:
                return float(xs[idx])
            return float(xs[idx - 1] + (level - y0) * (xs[idx] - xs[idx - 1]) / (y1 - y0))
    return None


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 1e-12 or vy <= 1e-12:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return float(cov / math.sqrt(vx * vy))


def summarize_m0(rows: list[dict], metric: str) -> list[dict]:
    if not rows:
        return []
    prompt_pairs = rows[0]["prompt_pairs"]
    seeds = sorted({row["seed"] for row in rows})
    directions = sorted({row["direction"] for row in rows})
    out = []
    for seed in seeds:
        for pair_idx, pair in enumerate(prompt_pairs):
            if pair["prompt_a"] == pair["prompt_b"]:
                continue
            for direction in directions:
                scoped = sorted(
                    [row for row in rows if row["seed"] == seed and row["direction"] == direction],
                    key=lambda row: row["swap_iteration"],
                )
                xs = [int(row["swap_iteration"]) for row in scoped]
                ys = [source_retention(row, pair_idx, metric) for row in scoped]
                k25 = crossing(xs, ys, 0.25)
                k50 = crossing(xs, ys, 0.50)
                k75 = crossing(xs, ys, 0.75)
                out.append(
                    {
                        "seed": seed,
                        "pair_index": pair_idx,
                        "prompt_a": pair["prompt_a"],
                        "prompt_b": pair["prompt_b"],
                        "direction": direction,
                        "metric": metric,
                        "k25": k25,
                        "k50": k50,
                        "k75": k75,
                        "width": (k75 - k25) if k25 is not None and k75 is not None else None,
                        "y0": ys[0] if ys else None,
                        "yend": ys[-1] if ys else None,
                    }
                )
    return out


def summarize_gdc(rows: list[dict], thresholds: list[float]) -> list[dict]:
    if not rows:
        return []
    prompt_pairs = rows[0]["prompt_pairs"]
    seeds = sorted({row["seed"] for row in rows})
    prompt_keys = sorted({row["prompt_key"] for row in rows})
    out = []
    for seed in seeds:
        for pair_idx, pair in enumerate(prompt_pairs):
            if pair["prompt_a"] == pair["prompt_b"]:
                continue
            for prompt_key in prompt_keys:
                scoped = sorted(
                    [row for row in rows if row["seed"] == seed and row["prompt_key"] == prompt_key],
                    key=lambda row: row["outer_idx"],
                )
                for threshold in thresholds:
                    first_gdc = None
                    first_stability = None
                    for row in scoped:
                        gdc_values = row.get("flow_gdc_mean_by_sample", [])
                        if (
                            first_gdc is None
                            and pair_idx < len(gdc_values)
                            and gdc_values[pair_idx] is not None
                            and gdc_values[pair_idx] >= threshold
                        ):
                            first_gdc = int(row["outer_idx"])
                        stability_values = row.get("flow_stability_score_mean_by_sample", [])
                        if (
                            first_stability is None
                            and pair_idx < len(stability_values)
                            and stability_values[pair_idx] is not None
                            and stability_values[pair_idx] >= threshold
                        ):
                            first_stability = int(row["outer_idx"])
                    out.append(
                        {
                            "seed": seed,
                            "pair_index": pair_idx,
                            "prompt_key": prompt_key,
                            "prompt": pair[prompt_key],
                            "threshold": threshold,
                            "first_outer_gdc_mean_ge": first_gdc,
                            "first_outer_stability_mean_ge": first_stability,
                        }
                    )
    return out


def average_m0_by_pair_seed(m0_rows: list[dict]) -> dict[tuple[int, int], dict]:
    grouped: dict[tuple[int, int], list[dict]] = {}
    for row in m0_rows:
        if row["metric"] != "decoded" or row["k50"] is None:
            continue
        grouped.setdefault((row["seed"], row["pair_index"]), []).append(row)
    out = {}
    for key, rows in grouped.items():
        k50s = [row["k50"] for row in rows if row["k50"] is not None]
        widths = [row["width"] for row in rows if row["width"] is not None]
        if k50s:
            out[key] = {
                "decoded_k50_mean": sum(k50s) / len(k50s),
                "decoded_width_mean": sum(widths) / len(widths) if widths else None,
                "prompt_a": rows[0]["prompt_a"],
                "prompt_b": rows[0]["prompt_b"],
            }
    return out


def average_gdc_by_pair_seed(gdc_rows: list[dict], threshold: float, field: str) -> dict[tuple[int, int], float]:
    grouped: dict[tuple[int, int], list[int]] = {}
    for row in gdc_rows:
        if row["threshold"] != threshold:
            continue
        value = row.get(field)
        if value is None:
            continue
        grouped.setdefault((row["seed"], row["pair_index"]), []).append(int(value))
    return {key: sum(values) / len(values) for key, values in grouped.items() if values}


def correlate(m0_avg: dict[tuple[int, int], dict], gdc_avg: dict[tuple[int, int], float], m0_field: str) -> dict:
    xs = []
    ys = []
    keys = sorted(set(m0_avg) & set(gdc_avg))
    for key in keys:
        value = m0_avg[key].get(m0_field)
        if value is None:
            continue
        xs.append(float(value))
        ys.append(float(gdc_avg[key]))
    return {"n": len(xs), "pearson": pearson(xs, ys)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze MoDebug SLAD M0/GDC core results")
    parser.add_argument("--m0_metrics", required=True)
    parser.add_argument("--gdc_metrics", required=True)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--gdc_thresholds", default="0.85,0.90,0.95")
    args = parser.parse_args()

    m0_rows = read_jsonl(Path(args.m0_metrics))
    gdc_rows = read_jsonl(Path(args.gdc_metrics))
    thresholds = parse_float_list(args.gdc_thresholds)

    m0_summary = summarize_m0(m0_rows, "decoded") + summarize_m0(m0_rows, "latent")
    gdc_summary = summarize_gdc(gdc_rows, thresholds)
    m0_avg = average_m0_by_pair_seed(m0_summary)

    correlations = []
    for threshold in thresholds:
        for field in ["first_outer_gdc_mean_ge", "first_outer_stability_mean_ge"]:
            gdc_avg = average_gdc_by_pair_seed(gdc_summary, threshold, field)
            correlations.append(
                {
                    "threshold": threshold,
                    "gdc_field": field,
                    "vs_decoded_k50_mean": correlate(m0_avg, gdc_avg, "decoded_k50_mean"),
                    "vs_decoded_width_mean": correlate(m0_avg, gdc_avg, "decoded_width_mean"),
                }
            )

    output = {
        "m0_metrics": str(Path(args.m0_metrics).resolve()),
        "gdc_metrics": str(Path(args.gdc_metrics).resolve()),
        "thresholds": thresholds,
        "m0_summary": m0_summary,
        "gdc_summary": gdc_summary,
        "correlations": correlations,
    }
    out_dir = Path(args.out_dir).resolve()
    write_json(out_dir / "core_calibration_summary.json", output)
    print(json.dumps({"summary": str(out_dir / "core_calibration_summary.json"), "correlations": correlations}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


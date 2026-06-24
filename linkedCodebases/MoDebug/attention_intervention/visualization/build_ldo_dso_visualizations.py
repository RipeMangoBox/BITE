#!/usr/bin/env python3
"""Generate CSV and SVG visualizations for LDO/DSO diagnostics.

This script keeps LDO/DSO diagnostics separate from full attention
intervention evaluator plots because MoLingo LDO is a decoded-array diagnostic
and MotionCLR DSO is a diffusion-step endpoint evaluation.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"
SOURCE_JSON = DATA_DIR / "source_ldo_dso_20260608.json"

DSO_COLOR = "#2563eb"
LDO_COLORS = {0: "#059669", 1: "#d97706"}


def load_source() -> dict:
    return json.loads(SOURCE_JSON.read_text(encoding="utf-8"))


def fmt(value: float | int | str | bool | None, digits: int = 4) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value
    return f"{value:.{digits}f}"


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def write_csvs(source: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    status_fields = ["baseline", "diagnostic", "paper_level_status", "formal_outputs", "reason"]
    with (DATA_DIR / "ldo_dso_status.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=status_fields)
        writer.writeheader()
        writer.writerows(source["status"])

    dso_fields = [
        "variant",
        "step",
        "step_of_10",
        "matching_score",
        "top1",
        "top2",
        "top3",
        "fid",
        "diversity",
        "multimodality",
    ]
    with (DATA_DIR / "motionclr_dso_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dso_fields)
        writer.writeheader()
        for row in source["motionclr_dso"]:
            writer.writerow({field: fmt(row.get(field)) for field in dso_fields})

    ldo_fields = [
        "seed",
        "block",
        "endpoint_layer",
        "layers",
        "l2_vs_baseline",
        "mean_abs_vs_baseline",
        "max_abs_vs_baseline",
        "allclose_vs_baseline",
    ]
    with (DATA_DIR / "molingo_ldo_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ldo_fields)
        writer.writeheader()
        for row in source["molingo_ldo"]:
            writer.writerow({field: fmt(row.get(field)) for field in ldo_fields})

    blocks = sorted({row["block"] for row in source["molingo_ldo"]}, key=["early", "middle", "late"].index)
    with (DATA_DIR / "molingo_ldo_block_summary.csv").open("w", newline="", encoding="utf-8") as f:
        fields = [
            "block",
            "endpoint_layer",
            "n",
            "l2_vs_baseline_mean",
            "mean_abs_vs_baseline_mean",
            "max_abs_vs_baseline_mean",
            "allclose_count",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for block in blocks:
            rows = [row for row in source["molingo_ldo"] if row["block"] == block]
            writer.writerow(
                {
                    "block": block,
                    "endpoint_layer": rows[0]["endpoint_layer"],
                    "n": len(rows),
                    "l2_vs_baseline_mean": fmt(mean([row["l2_vs_baseline"] for row in rows])),
                    "mean_abs_vs_baseline_mean": fmt(mean([row["mean_abs_vs_baseline"] for row in rows])),
                    "max_abs_vs_baseline_mean": fmt(mean([row["max_abs_vs_baseline"] for row in rows])),
                    "allclose_count": sum(1 for row in rows if row["allclose_vs_baseline"]),
                }
            )


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111827}.axis{stroke:#9ca3af;stroke-width:1}.grid{stroke:#e5e7eb;stroke-width:1}.title{font-size:20px;font-weight:700}.label{font-size:13px;fill:#374151}.tick{font-size:12px;fill:#4b5563}.legend{font-size:13px}</style>',
    ]


def text(x: float, y: float, content: str, cls: str = "", anchor: str = "start") -> str:
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{cls_attr}>{escape(content)}</text>'


def line_chart(path: Path, title: str, y_label: str, points: list[tuple[int, float]], color: str) -> None:
    width, height = 920, 500
    left, right, top, bottom = 78, 38, 70, 78
    plot_w = width - left - right
    plot_h = height - top - bottom
    x_min, x_max = min(x for x, _ in points), max(x for x, _ in points)
    y_values = [y for _, y in points]
    y_min, y_max = min(y_values), max(y_values)
    pad = (y_max - y_min) * 0.08 or 0.01
    y_min -= pad
    y_max += pad

    def sx(step: int) -> float:
        return left + ((step - x_min) / max(x_max - x_min, 1)) * plot_w

    def sy(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_h

    parts = svg_header(width, height)
    parts.append(text(left, 34, title, "title"))
    parts.append(text(left, 56, y_label, "label"))
    for i in range(5):
        y = top + (i / 4) * plot_h
        value = y_max - (i / 4) * (y_max - y_min)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(text(left - 10, y + 4, f"{value:.3g}", "tick", "end"))
    parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis"/>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    for step, _ in points:
        x = sx(step)
        parts.append(f'<line x1="{x:.1f}" y1="{height-bottom}" x2="{x:.1f}" y2="{height-bottom+5}" class="axis"/>')
        parts.append(text(x, height - bottom + 22, str(step), "tick", "middle"))
    parts.append(text(width / 2, height - 26, "Diffusion step endpoint", "label", "middle"))
    polyline = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in points)
    parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.8" points="{polyline}"/>')
    for step, value in points:
        parts.append(f'<circle cx="{sx(step):.1f}" cy="{sy(value):.1f}" r="3.5" fill="{color}"/>')
        parts.append(text(sx(step), sy(value) - 10, f"{value:.3g}", "tick", "middle"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def grouped_bar_chart(path: Path, title: str, y_label: str, rows: list[dict], metric: str) -> None:
    width, height = 900, 500
    left, right, top, bottom = 78, 38, 70, 90
    plot_w = width - left - right
    plot_h = height - top - bottom
    blocks = ["early", "middle", "late"]
    y_max = max(row[metric] for row in rows) * 1.15 or 1.0
    group_w = plot_w / len(blocks)
    bar_w = group_w / 4.2

    def sy(value: float) -> float:
        return top + (y_max - value) / y_max * plot_h

    parts = svg_header(width, height)
    parts.append(text(left, 34, title, "title"))
    parts.append(text(left, 56, y_label, "label"))
    for i in range(6):
        value = y_max * i / 5
        y = sy(value)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(text(left - 10, y + 4, f"{value:.3g}", "tick", "end"))
    parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis"/>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    for bi, block in enumerate(blocks):
        block_rows = sorted([row for row in rows if row["block"] == block], key=lambda row: row["seed"])
        group_x = left + bi * group_w
        parts.append(text(group_x + group_w / 2, height - bottom + 28, block, "label", "middle"))
        for ri, row in enumerate(block_rows):
            value = row[metric]
            color = LDO_COLORS[row["seed"]]
            x = group_x + bar_w * (ri + 1.2)
            y = sy(value)
            h = height - bottom - y
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w*0.8:.1f}" height="{h:.1f}" fill="{color}"/>')
            parts.append(text(x + bar_w * 0.4, y - 6, f"{value:.3g}", "tick", "middle"))
    legend_y = height - 36
    for idx, seed in enumerate(sorted(LDO_COLORS)):
        lx = left + idx * 110
        parts.append(f'<rect x="{lx}" y="{legend_y-13}" width="14" height="14" fill="{LDO_COLORS[seed]}"/>')
        parts.append(text(lx + 20, legend_y, f"seed {seed}", "legend"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def generate_figures(source: dict) -> None:
    dso_rows = [row for row in source["motionclr_dso"] if row["step"] is not None]
    for metric, label in [
        ("fid", "FID lower is better"),
        ("top1", "R-Precision Top1 higher is better"),
        ("top3", "R-Precision Top3 higher is better"),
        ("matching_score", "Matching score lower is better"),
        ("diversity", "Diversity higher is better"),
    ]:
        line_chart(
            FIG_DIR / f"motionclr_dso_{metric}.svg",
            f"MotionCLR DSO {metric.replace('_', ' ').title()} Formation",
            label,
            [(row["step"], row[metric]) for row in dso_rows],
            DSO_COLOR,
        )

    ldo_rows = source["molingo_ldo"]
    grouped_bar_chart(
        FIG_DIR / "molingo_ldo_l2_vs_baseline.svg",
        "MoLingo LDO Endpoint Difference",
        "L2 distance to baseline arrays; diagnostic only",
        ldo_rows,
        "l2_vs_baseline",
    )
    grouped_bar_chart(
        FIG_DIR / "molingo_ldo_mean_abs_vs_baseline.svg",
        "MoLingo LDO Mean Absolute Difference",
        "Mean absolute difference to baseline arrays; diagnostic only",
        ldo_rows,
        "mean_abs_vs_baseline",
    )


def main() -> None:
    source = load_source()
    write_csvs(source)
    generate_figures(source)
    for path in [
        DATA_DIR / "ldo_dso_status.csv",
        DATA_DIR / "motionclr_dso_metrics.csv",
        DATA_DIR / "molingo_ldo_metrics.csv",
        DATA_DIR / "molingo_ldo_block_summary.csv",
    ]:
        print(f"Wrote {path}")
    for path in sorted(FIG_DIR.glob("*dso*.svg")) + sorted(FIG_DIR.glob("*ldo*.svg")):
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

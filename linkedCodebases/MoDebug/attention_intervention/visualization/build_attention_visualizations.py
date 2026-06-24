#!/usr/bin/env python3
"""Generate CSV and SVG visualizations for attention intervention reports.

Inputs are the audited metric summaries exported to `data/source_metrics_*.json`.
The script intentionally uses only the Python standard library so it works in
the current environment without pandas/matplotlib.
"""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"
SOURCE_JSONS = [
    DATA_DIR / "source_metrics_20260605.json",
    DATA_DIR / "source_metrics_20260609_molingo.json",
]

FAMILY_ORDER = ["baseline", "SA", "CA", "CFG_SA", "CFG_CA"]
BASELINE_ORDER = ["MotionCLR", "MotionGPT", "MoLingo"]
FAMILY_COLORS = {
    "baseline": "#6b7280",
    "SA": "#2563eb",
    "CA": "#059669",
    "CFG_SA": "#d97706",
    "CFG_CA": "#dc2626",
}
RUNTIME_MEDIAN = {
    ("MotionCLR", "baseline"): 7.34,
    ("MotionCLR", "SA"): 7.18,
    ("MotionCLR", "CA"): 7.30,
    ("MotionCLR", "CFG_SA"): 7.18,
    ("MotionCLR", "CFG_CA"): 7.36,
    ("MotionGPT", "baseline"): 3.98,
    ("MotionGPT", "SA"): 3.82,
    ("MotionGPT", "CA"): 3.82,
    ("MoLingo", "baseline"): 95.84,
    ("MoLingo", "SA"): 95.07,
    ("MoLingo", "CA"): 80.09,
    ("MoLingo", "CFG_SA"): 78.85,
    ("MoLingo", "CFG_CA"): 79.04,
}
FID_METRIC = {"MotionCLR": "FID", "MotionGPT": "FID", "MoLingo": "FID_TMR"}
EXPECTED_COUNTS = {
    ("MotionCLR", "baseline"): 2,
    ("MotionCLR", "SA"): 18,
    ("MotionCLR", "CA"): 18,
    ("MotionCLR", "CFG_SA"): 18,
    ("MotionCLR", "CFG_CA"): 18,
    ("MotionGPT", "baseline"): 1,
    ("MotionGPT", "SA"): 12,
    ("MotionGPT", "CA"): 12,
    ("MoLingo", "baseline"): 1,
    ("MoLingo", "SA"): 3,
    ("MoLingo", "CA"): 3,
    ("MoLingo", "CFG_SA"): 3,
    ("MoLingo", "CFG_CA"): 3,
}
PENDING_NOTES = {
    ("MoLingo", "CFG_CA"): "partial_pending_layer_15",
}


def load_source() -> dict[str, list[dict]]:
    merged: dict[str, list[dict]] = {}
    for source_json in SOURCE_JSONS:
        if not source_json.exists():
            continue
        data = json.loads(source_json.read_text(encoding="utf-8"))
        for baseline, rows in data.items():
            merged.setdefault(baseline, []).extend(rows)
    return merged


def fmt(value: float | int | str | None, digits: int = 4) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.{digits}f}"


def mean(values: list[float | None]) -> float | None:
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def family_rows(source: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for baseline in BASELINE_ORDER:
        by_family: dict[str, list[dict]] = {}
        for row in source.get(baseline, []):
            by_family.setdefault(row["family"], []).append(row)
        for family in FAMILY_ORDER:
            members = by_family.get(family, [])
            if not members:
                status = "unsupported"
                if (baseline, family) in EXPECTED_COUNTS:
                    status = "missing"
                rows.append(
                    {
                        "baseline": baseline,
                        "family": family,
                        "n": 0,
                        "fid_metric": FID_METRIC[baseline],
                        "fid_mean": "",
                        "best_fid": "",
                        "best_fid_layer": "NA",
                        "top1_mean": "",
                        "top2_mean": "",
                        "top3_mean": "",
                        "best_top1": "",
                        "best_top1_layer": "NA",
                        "best_top2": "",
                        "best_top2_layer": "NA",
                        "best_top3": "",
                        "best_top3_layer": "NA",
                        "matching_mean": "",
                        "diversity_mean": "",
                        "multimodality_mean": "",
                        "median_min": "",
                        "status": status,
                    }
                )
                continue
            expected = EXPECTED_COUNTS.get((baseline, family))
            status = "complete"
            if expected is not None and len(members) < expected:
                status = PENDING_NOTES.get((baseline, family), f"partial_{len(members)}_of_{expected}")
            best_fid = min(members, key=lambda r: r["fid"])
            best_top1 = max(members, key=lambda r: r["top1"])
            best_top2 = max(members, key=lambda r: r["top2"])
            best_top3 = max(members, key=lambda r: r["top3"])
            rows.append(
                {
                    "baseline": baseline,
                    "family": family,
                    "n": len(members),
                    "fid_metric": FID_METRIC[baseline],
                    "fid_mean": fmt(mean([r["fid"] for r in members])),
                    "best_fid": fmt(best_fid["fid"]),
                    "best_fid_layer": "NA" if best_fid["layer"] is None else str(best_fid["layer"]),
                    "top1_mean": fmt(mean([r["top1"] for r in members])),
                    "top2_mean": fmt(mean([r["top2"] for r in members])),
                    "top3_mean": fmt(mean([r["top3"] for r in members])),
                    "best_top1": fmt(best_top1["top1"]),
                    "best_top1_layer": "NA" if best_top1["layer"] is None else str(best_top1["layer"]),
                    "best_top2": fmt(best_top2["top2"]),
                    "best_top2_layer": "NA" if best_top2["layer"] is None else str(best_top2["layer"]),
                    "best_top3": fmt(best_top3["top3"]),
                    "best_top3_layer": "NA" if best_top3["layer"] is None else str(best_top3["layer"]),
                    "matching_mean": fmt(mean([r["matching"] for r in members])),
                    "diversity_mean": fmt(mean([r["diversity"] for r in members])),
                    "multimodality_mean": fmt(mean([r["multimodality"] for r in members])),
                    "median_min": fmt(RUNTIME_MEDIAN.get((baseline, family)), 2),
                    "status": status,
                }
            )
    return rows


def write_csvs(source: dict[str, list[dict]], summary: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / "family_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    fields = [
        "baseline",
        "family",
        "layer",
        "fid_metric",
        "fid",
        "top1",
        "top2",
        "top3",
        "matching",
        "diversity",
        "multimodality",
        "metrics_summary",
    ]
    with (DATA_DIR / "layer_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for baseline in BASELINE_ORDER:
            for row in source[baseline]:
                out = dict(row)
                out["baseline"] = baseline
                out["fid_metric"] = FID_METRIC[baseline]
                out["layer"] = "NA" if row["layer"] is None else row["layer"]
                writer.writerow({k: out.get(k, "") for k in fields})


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111827}.axis{stroke:#9ca3af;stroke-width:1}.grid{stroke:#e5e7eb;stroke-width:1}.legend{font-size:13px}.tick{font-size:12px;fill:#4b5563}.title{font-size:20px;font-weight:700}.label{font-size:13px;fill:#374151}</style>',
    ]


def text(x: float, y: float, content: str, cls: str = "", anchor: str = "start") -> str:
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{cls_attr}>{escape(content)}</text>'


def line_chart(path: Path, title: str, y_label: str, series: dict[str, list[tuple[int, float]]]) -> None:
    width, height = 980, 520
    left, right, top, bottom = 78, 38, 70, 78
    plot_w = width - left - right
    plot_h = height - top - bottom
    layer_values = [layer for values in series.values() for layer, _ in values]
    y_values = [value for values in series.values() for _, value in values]
    x_min, x_max = min(layer_values), max(layer_values)
    y_min, y_max = min(y_values), max(y_values)
    pad = (y_max - y_min) * 0.08 or 0.01
    y_min -= pad
    y_max += pad

    def sx(layer: int) -> float:
        return left + ((layer - x_min) / max(x_max - x_min, 1)) * plot_w

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
    unique_layers = sorted(set(layer_values))
    if len(unique_layers) <= 10:
        tick_layers = unique_layers
    else:
        tick_layers = list(range(x_min, x_max + 1, 2))
        if x_max not in tick_layers:
            tick_layers.append(x_max)
    for layer in tick_layers:
        x = sx(layer)
        parts.append(f'<line x1="{x:.1f}" y1="{height-bottom}" x2="{x:.1f}" y2="{height-bottom+5}" class="axis"/>')
        parts.append(text(x, height - bottom + 22, str(layer), "tick", "middle"))
    parts.append(text(width / 2, height - 26, "Layer", "label", "middle"))

    for idx, (family, values) in enumerate(series.items()):
        color = FAMILY_COLORS[family]
        points = " ".join(f"{sx(layer):.1f},{sy(value):.1f}" for layer, value in values)
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.6" points="{points}"/>')
        for layer, value in values:
            parts.append(f'<circle cx="{sx(layer):.1f}" cy="{sy(value):.1f}" r="3" fill="{color}"/>')
        lx = left + idx * 120
        parts.append(f'<rect x="{lx}" y="{height-52}" width="14" height="14" fill="{color}"/>')
        parts.append(text(lx + 20, height - 40, family, "legend"))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def runtime_chart(summary: list[dict]) -> None:
    rows = [r for r in summary if r["status"] != "unsupported" and r["median_min"]]
    width, height = 1080, 560
    left, right, top, bottom = 80, 40, 70, 105
    plot_w = width - left - right
    plot_h = height - top - bottom
    y_max = max(float(r["median_min"]) for r in rows) * 1.15
    grouped = {(r["baseline"], r["family"]): float(r["median_min"]) for r in rows}
    group_w = plot_w / len(BASELINE_ORDER)
    bar_w = group_w / (len(FAMILY_ORDER) + 1.6)

    def sy(value: float) -> float:
        return top + (y_max - value) / y_max * plot_h

    parts = svg_header(width, height)
    parts.append(text(left, 34, "Median Runtime by Baseline and Family", "title"))
    parts.append(text(left, 56, "minutes per layer; lower is faster", "label"))
    for i in range(6):
        value = y_max * i / 5
        y = sy(value)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(text(left - 10, y + 4, f"{value:.0f}", "tick", "end"))
    parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis"/>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    for bi, baseline in enumerate(BASELINE_ORDER):
        group_x = left + bi * group_w
        parts.append(text(group_x + group_w / 2, height - bottom + 30, baseline, "label", "middle"))
        for fi, family in enumerate(FAMILY_ORDER):
            value = grouped.get((baseline, family))
            if value is None:
                continue
            x = group_x + bar_w * (fi + 0.8)
            y = sy(value)
            h = height - bottom - y
            color = FAMILY_COLORS[family]
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w*0.82:.1f}" height="{h:.1f}" fill="{color}"/>')
            parts.append(text(x + bar_w * 0.41, y - 6, f"{value:.1f}", "tick", "middle"))
    legend_y = height - 45
    for idx, family in enumerate(FAMILY_ORDER):
        lx = left + idx * 150
        parts.append(f'<rect x="{lx}" y="{legend_y-13}" width="14" height="14" fill="{FAMILY_COLORS[family]}"/>')
        parts.append(text(lx + 20, legend_y, family, "legend"))
    parts.append("</svg>")
    (FIG_DIR / "family_runtime_median.svg").write_text("\n".join(parts), encoding="utf-8")


def metric_series(source: dict[str, list[dict]], baseline: str, metric: str) -> dict[str, list[tuple[int, float]]]:
    series: dict[str, list[tuple[int, float]]] = {}
    for family in FAMILY_ORDER:
        members = [r for r in source[baseline] if r["family"] == family and r["layer"] is not None]
        if not members:
            continue
        members.sort(key=lambda r: r["layer"])
        series[family] = [(r["layer"], r[metric]) for r in members]
    return series


def generate_figures(source: dict[str, list[dict]], summary: list[dict]) -> None:
    runtime_chart(summary)
    for baseline in BASELINE_ORDER:
        slug = baseline.lower()
        fid_name = "fid_tmr" if FID_METRIC[baseline] == "FID_TMR" else "fid"
        fid_series = metric_series(source, baseline, "fid")
        if fid_series:
            line_chart(
                FIG_DIR / f"{slug}_{fid_name}.svg",
                f"{baseline} Layer {FID_METRIC[baseline]} Trend",
                f"{FID_METRIC[baseline]} lower is better",
                fid_series,
            )
        for metric in ("top1", "top2", "top3"):
            series = metric_series(source, baseline, metric)
            if series:
                line_chart(
                    FIG_DIR / f"{slug}_{metric}.svg",
                    f"{baseline} Layer R-Precision {metric.title()} Trend",
                    f"R-Precision {metric.title()} higher is better",
                    series,
                )


def main() -> None:
    source = load_source()
    summary = family_rows(source)
    write_csvs(source, summary)
    generate_figures(source, summary)
    print(f"Wrote {DATA_DIR / 'family_summary.csv'}")
    print(f"Wrote {DATA_DIR / 'layer_metrics.csv'}")
    for path in sorted(FIG_DIR.glob("*.svg")):
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

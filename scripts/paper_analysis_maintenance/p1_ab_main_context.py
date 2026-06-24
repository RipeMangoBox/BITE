#!/usr/bin/env python3
"""P1 A/B utilities for BITE main-context cost experiments."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import statistics
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE_RESULTS = REPO_ROOT / "obsidian-vault" / "batches" / "siggraph50_v05_20260624" / "results.jsonl"
DEFAULT_OUT_DIR = REPO_ROOT / "obsidian-vault" / "batches" / "p1_main_context_ab_20260624"
DEFAULT_BASELINE_ROOT = REPO_ROOT / "_private" / "local_analysis_runs"
DEFAULT_REVIEW_OUT = REPO_ROOT / "_private" / "p1_ab" / "core_retention_review_packet.json"
REQUIRED_SECTIONS = ["概要", "核心方法与创新机理", "实验与关键发现", "定位与知识库关联", "原文 PDF"]


@dataclass
class PaperRun:
    title: str
    row: dict[str, str]
    result: dict[str, Any]
    manifest_path: Path
    manifest: dict[str, Any]
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    select = sub.add_parser("select-sample", help="Select a 20-paper A/B sample and write CSV/JSON.")
    select.add_argument("--baseline-results", default=str(DEFAULT_BASELINE_RESULTS))
    select.add_argument("--baseline-output-root", default=str(DEFAULT_BASELINE_ROOT))
    select.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    select.add_argument("--sample-size", type=int, default=20)

    summarize = sub.add_parser("summarize", help="Summarize baseline and optional experiment runs.")
    summarize.add_argument("--sample-json", default=str(DEFAULT_OUT_DIR / "sample_20_selection.json"))
    summarize.add_argument("--experiment-results", default="")
    summarize.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    summarize.add_argument("--report-name", default="p1_main_context_ab_report.md")

    review = sub.add_parser("review-core", help="Create a 5-paper core-retention review packet.")
    review.add_argument("--sample-json", default=str(DEFAULT_OUT_DIR / "sample_20_selection.json"))
    review.add_argument("--experiment-results", required=True)
    review.add_argument("--out-json", default=str(DEFAULT_REVIEW_OUT))
    review.add_argument("--sample-size", type=int, default=5)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def command_value(command: list[Any], flag: str) -> str:
    parts = [str(item) for item in (command or [])]
    if flag not in parts:
        return ""
    index = parts.index(flag)
    if index + 1 >= len(parts):
        return ""
    return parts[index + 1]


def resolve_path(value: str, *, base: Path = REPO_ROOT) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else base / path


def result_manifest_path(record: dict[str, Any], baseline_output_root: Path) -> Path | None:
    command = record.get("command") or []
    task_id = command_value(command, "--task-id")
    output_root = command_value(command, "--output-root")
    if not task_id:
        return None
    root = resolve_path(output_root, base=REPO_ROOT) if output_root else baseline_output_root
    return root / task_id / "manifest.json"


def load_paper_runs(results_path: Path, *, baseline_output_root: Path) -> list[PaperRun]:
    runs: list[PaperRun] = []
    for record in read_jsonl(results_path):
        if record.get("status") != "done":
            continue
        manifest_path = result_manifest_path(record, baseline_output_root)
        if not manifest_path or not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") != "done":
            continue
        row = record.get("row") or {}
        title = str(row.get("paper_title") or row.get("title") or manifest.get("paper_title") or "").strip()
        if not title:
            title = str((manifest.get("vault_export") or {}).get("note_path") or manifest_path.parent.name)
        run = PaperRun(
            title=title,
            row={str(k): str(v) for k, v in row.items()},
            result=record,
            manifest_path=manifest_path,
            manifest=manifest,
        )
        run.metrics = collect_source_metrics(run)
        runs.append(run)
    return runs


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def parse_full_text(run: PaperRun) -> str:
    work_dir = Path(str(run.manifest.get("work_dir") or run.manifest_path.parent))
    return read_text(work_dir / "parse" / "full.md")


def note_text(run: PaperRun) -> str:
    note_path = Path(str((run.manifest.get("vault_export") or {}).get("note_path") or ""))
    return read_text(note_path) if note_path else ""


def usage(run: PaperRun) -> dict[str, Any]:
    value = run.manifest.get("usage") or {}
    return value if isinstance(value, dict) else {}


def token_budget(run: PaperRun) -> dict[str, Any]:
    value = run.manifest.get("token_budget") or {}
    return value if isinstance(value, dict) else {}


def metric_number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def collect_source_metrics(run: PaperRun) -> dict[str, Any]:
    text = parse_full_text(run)
    row = run.row
    figures = len(re.findall(r"\b(?:Fig\.?|Figure|Table)\s*\d+", text, flags=re.IGNORECASE))
    equations = (
        text.count("$$")
        + len(re.findall(r"\\tag\{?\d+", text))
        + len(re.findall(r"\\begin\{(?:equation|align|array|split)", text))
    )
    tables = (
        len(re.findall(r"<table\b", text, flags=re.IGNORECASE))
        + len(re.findall(r"\bTable\s+\d+", text, flags=re.IGNORECASE))
    )
    links = " ".join(str(row.get(key) or "") for key in ("paper_link", "project_link_or_github_link", "project_link", "github_link"))
    source_noise = len(re.findall(r"https?://", links))
    if re.search(r"github\.io|project|github\.com|gitlab|www\.", links, flags=re.IGNORECASE):
        source_noise += 2
    if not re.search(r"arxiv\.org|dl\.acm\.org|openaccess", links, flags=re.IGNORECASE):
        source_noise += 1
    budget = token_budget(run)
    return {
        "markdown_chars": int(metric_number(budget.get("markdown_chars"))),
        "chunk_count": int(metric_number(run.manifest.get("chunk_count") or budget.get("chunk_count"))),
        "note_chars": int(metric_number(((run.manifest.get("vault_export") or {}).get("validation") or {}).get("note_chars"))),
        "formula_hits": equations,
        "figure_table_caption_hits": figures,
        "table_hits": tables,
        "source_noise_score": source_noise,
        "api_cost_usd": metric_number(usage(run).get("estimated_cost_usd_api")),
        "prompt_tokens_api": int(metric_number(usage(run).get("prompt_tokens_api"))),
    }


def add_reason(run: PaperRun, reason: str) -> None:
    if reason not in run.reasons:
        run.reasons.append(reason)


def select_runs(runs: list[PaperRun], sample_size: int) -> list[PaperRun]:
    selected: list[PaperRun] = []

    def pick(sorted_runs: list[PaperRun], reason: str, count: int) -> None:
        for run in sorted_runs:
            add_reason(run, reason)
            if run not in selected:
                selected.append(run)
            if sum(reason in item.reasons for item in selected) >= count:
                break

    pick(sorted(runs, key=lambda r: r.metrics["markdown_chars"]), "short_paper", 4)
    pick(sorted(runs, key=lambda r: (r.metrics["markdown_chars"], r.metrics["chunk_count"]), reverse=True), "long_paper", 4)
    pick(sorted(runs, key=lambda r: r.metrics["formula_hits"], reverse=True), "formula_dense", 4)
    pick(sorted(runs, key=lambda r: (r.metrics["table_hits"], r.metrics["figure_table_caption_hits"]), reverse=True), "experiment_table_dense", 4)
    pick(sorted(runs, key=lambda r: r.metrics["source_noise_score"], reverse=True), "project_or_source_noise", 4)

    for run in sorted(runs, key=lambda r: (len(r.reasons), r.metrics["api_cost_usd"]), reverse=True):
        if len(selected) >= sample_size:
            break
        if run not in selected:
            add_reason(run, "cost_length_diversity_fill")
            selected.append(run)

    return selected[:sample_size]


def find_mineru_output_path(run: PaperRun) -> str:
    work_dir = Path(str(run.manifest.get("work_dir") or run.manifest_path.parent))
    raw_root = work_dir / "parse" / "mineru_raw"
    candidates = sorted(path.parent.parent for path in raw_root.rglob("auto/*.md") if path.is_file())
    if candidates:
        return candidates[0].relative_to(REPO_ROOT).as_posix() if candidates[0].is_relative_to(REPO_ROOT) else str(candidates[0])
    source_root = str((run.manifest.get("parse_info") or {}).get("source_root") or "")
    return source_root


def selection_row(run: PaperRun) -> dict[str, Any]:
    row = dict(run.row)
    row.pop("_csv_line", None)
    row["state"] = row.get("state") or "Downloaded"
    row["paper_title"] = row.get("paper_title") or run.title
    row["mineru_output_path"] = find_mineru_output_path(run)
    row["baseline_task_id"] = str(run.manifest.get("task_id") or run.manifest_path.parent.name)
    row["baseline_work_dir"] = str(run.manifest.get("work_dir") or run.manifest_path.parent)
    row["baseline_manifest_path"] = run.manifest_path.relative_to(REPO_ROOT).as_posix()
    row["selection_reasons"] = ";".join(run.reasons)
    for key, value in run.metrics.items():
        row[f"baseline_{key}"] = value
    return row


def write_selection(runs: list[PaperRun], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [selection_row(run) for run in runs]
    fieldnames: list[str] = []
    preferred = [
        "state", "importance", "paper_title", "venue", "project_link_or_github_link",
        "paper_link", "sort", "pdf_path", "mineru_output_path", "baseline_task_id",
        "baseline_work_dir", "baseline_manifest_path", "selection_reasons",
    ]
    for key in preferred:
        if any(key in row for row in rows) and key not in fieldnames:
            fieldnames.append(key)
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    csv_path = out_dir / "sample_20.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "selection_rule": (
            "Greedy coverage over completed v05 SIGGRAPH/SIGGRAPH Asia runs: "
            "4 shortest by markdown chars, 4 longest by markdown chars/chunks, "
            "4 formula-dense by equation markers, 4 experiment/table-dense by table/caption markers, "
            "4 project/source-noise-heavy by source links; fill remaining by reason count and baseline cost."
        ),
        "sample_size": len(rows),
        "csv_path": csv_path.relative_to(REPO_ROOT).as_posix(),
        "reason_counts": Counter(reason for run in runs for reason in run.reasons),
        "items": rows,
    }
    (out_dir / "sample_20_selection.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "sample_20_selection.md").write_text(render_selection_md(payload), encoding="utf-8")
    print(json.dumps({"csv": str(csv_path), "json": str(out_dir / "sample_20_selection.json"), "items": len(rows)}, ensure_ascii=False, indent=2))


def render_selection_md(payload: dict[str, Any]) -> str:
    lines = [
        "# P1 Main Context A/B Sample",
        "",
        f"- generated_at: `{payload['generated_at']}`",
        f"- sample_size: {payload['sample_size']}",
        f"- csv: `{payload['csv_path']}`",
        "",
        "## Selection Rule",
        "",
        payload["selection_rule"],
        "",
        "## Coverage",
        "",
    ]
    for reason, count in payload["reason_counts"].items():
        lines.append(f"- {reason}: {count}")
    lines.extend(["", "## Papers", "", "| # | Title | Reasons | Chars | Chunks | Cost |", "|---:|---|---|---:|---:|---:|"])
    for index, item in enumerate(payload["items"], 1):
        title = table_cell(item.get("paper_title"))
        reasons = table_cell(item.get("selection_reasons"))
        lines.append(
            f"| {index} | {title} | {reasons} | {item.get('baseline_markdown_chars', 0)} | "
            f"{item.get('baseline_chunk_count', 0)} | {float(item.get('baseline_api_cost_usd') or 0):.6f} |"
        )
    return "\n".join(lines) + "\n"


def table_cell(value: Any) -> str:
    return str(value or "").replace("|", "/").replace("\n", " ").strip()


def load_selection(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("items") or [])


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def manifest_from_selection_item(item: dict[str, Any]) -> dict[str, Any]:
    path = resolve_path(str(item.get("baseline_manifest_path") or ""))
    return json.loads(path.read_text(encoding="utf-8"))


def experiment_manifests(results_path: Path) -> dict[str, dict[str, Any]]:
    by_title: dict[str, dict[str, Any]] = {}
    for record in read_jsonl(results_path):
        command = record.get("command") or []
        task_id = command_value(command, "--task-id")
        output_root = command_value(command, "--output-root")
        title = str((record.get("row") or {}).get("paper_title") or command_value(command, "--paper-title") or "").strip()
        if not task_id or not output_root or not title:
            continue
        manifest_path = resolve_path(output_root) / task_id / "manifest.json"
        if manifest_path.exists():
            by_title[title_key(title)] = json.loads(manifest_path.read_text(encoding="utf-8"))
    return by_title


def note_path_from_manifest(manifest: dict[str, Any]) -> Path | None:
    path = str((manifest.get("vault_export") or {}).get("note_path") or "")
    return Path(path) if path else None


def note_validation(manifest: dict[str, Any]) -> dict[str, Any]:
    value = (manifest.get("vault_export") or {}).get("validation") or {}
    return value if isinstance(value, dict) else {}


def note_body(manifest: dict[str, Any]) -> str:
    path = note_path_from_manifest(manifest)
    return read_text(path) if path else ""


def image_embed_count(text: str) -> int:
    return len(re.findall(r"!\[\[assets/figures/papers/", text))


def structure_ok(text: str, manifest: dict[str, Any]) -> bool:
    validation = note_validation(manifest)
    if validation and validation.get("ok") is False:
        return False
    return all(f"## {section}" in text for section in REQUIRED_SECTIONS)


def run_metrics(manifest: dict[str, Any]) -> dict[str, Any]:
    usage_data = manifest.get("usage") or {}
    text = note_body(manifest)
    validation = note_validation(manifest)
    figure_cost = metric_number(usage_data.get("figure_placement_estimated_cost_usd")) + metric_number(usage_data.get("figure_visual_summary_estimated_cost_usd"))
    return {
        "status": manifest.get("status"),
        "api_cost_usd": metric_number(usage_data.get("estimated_cost_usd_api")),
        "prompt_tokens_api": int(metric_number(usage_data.get("prompt_tokens_api"))),
        "part_cost_usd": metric_number(usage_data.get("part_estimated_cost_usd_api")),
        "main_cost_usd": metric_number(usage_data.get("main_estimated_cost_usd_api")),
        "writer_cost_usd": metric_number(usage_data.get("writer_estimated_cost_usd_api")),
        "figure_cost_usd": figure_cost,
        "note_chars": int(metric_number(validation.get("note_chars") or len(text))),
        "image_embeds": image_embed_count(text),
        "supplement_heading": text.count("### 补充图表"),
        "structure_ok": structure_ok(text, manifest),
        "needs_fulltext": manifest.get("status") == "needs_fulltext",
        "main_context_mode": manifest.get("main_context_mode") or (manifest.get("token_budget") or {}).get("after", {}).get("main_context_mode"),
        "main_context_chars": (manifest.get("token_budget") or {}).get("after", {}).get("main_context_chars"),
    }


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * q
    low = int(index)
    high = min(low + 1, len(sorted_values) - 1)
    if low == high:
        return sorted_values[low]
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * (index - low)


def stats(values: list[float]) -> dict[str, float | None]:
    return {
        "n": len(values),
        "median": round(statistics.median(values), 6) if values else None,
        "mean": round(statistics.mean(values), 6) if values else None,
        "p75": round(percentile(values, 0.75), 6) if values else None,
    }


def aggregate(label: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "label": label,
        "count": len(rows),
        "api_cost_usd": stats([row["api_cost_usd"] for row in rows]),
        "part_cost_usd": stats([row["part_cost_usd"] for row in rows]),
        "main_cost_usd": stats([row["main_cost_usd"] for row in rows]),
        "writer_cost_usd": stats([row["writer_cost_usd"] for row in rows]),
        "figure_cost_usd": stats([row["figure_cost_usd"] for row in rows]),
        "prompt_tokens_api": stats([row["prompt_tokens_api"] for row in rows]),
        "note_chars": stats([row["note_chars"] for row in rows]),
        "image_embed_max": max((row["image_embeds"] for row in rows), default=0),
        "image_over_6_count": sum(row["image_embeds"] > 6 for row in rows),
        "supplement_heading_count": sum(row["supplement_heading"] for row in rows),
        "structure_complete_rate": round(sum(bool(row["structure_ok"]) for row in rows) / len(rows), 6) if rows else None,
        "needs_fulltext_count": sum(bool(row["needs_fulltext"]) for row in rows),
    }


def summarize(sample_json: Path, experiment_results: Path | None, out_dir: Path, report_name: str) -> None:
    items = load_selection(sample_json)
    experiment_by_title = experiment_manifests(experiment_results) if experiment_results else {}
    pair_rows: list[dict[str, Any]] = []
    baseline_rows: list[dict[str, Any]] = []
    experiment_rows: list[dict[str, Any]] = []
    for item in items:
        baseline_manifest = manifest_from_selection_item(item)
        base = run_metrics(baseline_manifest)
        baseline_rows.append(base)
        exp_manifest = experiment_by_title.get(title_key(str(item.get("paper_title") or "")))
        exp = run_metrics(exp_manifest) if exp_manifest else None
        if exp:
            experiment_rows.append(exp)
        pair_rows.append({"title": item.get("paper_title"), "selection_reasons": item.get("selection_reasons"), "baseline": base, "experiment": exp})

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sample_json": sample_json.relative_to(REPO_ROOT).as_posix() if sample_json.is_relative_to(REPO_ROOT) else str(sample_json),
        "experiment_results": str(experiment_results) if experiment_results else "",
        "baseline": aggregate("baseline_v05", baseline_rows),
        "experiment": aggregate("structured_main_context", experiment_rows) if experiment_rows else None,
        "pairs": pair_rows,
        "thresholds": {
            "structure_complete_rate": 1.0,
            "image_embed_max": 6,
            "supplement_heading_count": 0,
            "needs_fulltext_false_blocks": 0,
            "api_cost_median_drop_min": 0.10,
            "core_retention_min": 0.98,
        },
    }
    if experiment_rows:
        base_median = payload["baseline"]["api_cost_usd"]["median"] or 0
        exp_median = payload["experiment"]["api_cost_usd"]["median"] or 0
        payload["median_cost_drop"] = round((base_median - exp_median) / base_median, 6) if base_median else None
        payload["needs_fulltext_false_blocks"] = sum(
            bool(pair["experiment"] and pair["experiment"]["needs_fulltext"] and not pair["baseline"]["needs_fulltext"])
            for pair in pair_rows
        )
        payload["pass_fail"] = {
            "structure": payload["experiment"]["structure_complete_rate"] == 1.0,
            "images": payload["experiment"]["image_embed_max"] <= 6 and payload["experiment"]["image_over_6_count"] == 0,
            "supplement_heading": payload["experiment"]["supplement_heading_count"] == 0,
            "needs_fulltext": payload["needs_fulltext_false_blocks"] == 0,
            "cost_drop": (payload["median_cost_drop"] or 0) >= 0.10,
        }
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "p1_main_context_ab_summary.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = out_dir / report_name
    report_path.write_text(render_summary_md(payload), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "report": str(report_path)}, ensure_ascii=False, indent=2))


def render_stat_row(name: str, data: dict[str, Any], key: str) -> str:
    value = data[key]
    return f"| {name} | {value.get('median')} | {value.get('mean')} | {value.get('p75')} |"


def render_summary_md(payload: dict[str, Any]) -> str:
    lines = [
        "# P1 Main Context A/B Report",
        "",
        f"- generated_at: `{payload['generated_at']}`",
        f"- sample_json: `{payload['sample_json']}`",
        f"- experiment_results: `{payload.get('experiment_results') or 'pending'}`",
        "",
        "## Metrics",
        "",
        "### Baseline",
        "",
        "| Metric | Median | Mean | P75 |",
        "|---|---:|---:|---:|",
    ]
    for key, name in [
        ("api_cost_usd", "API cost"),
        ("part_cost_usd", "part cost"),
        ("main_cost_usd", "main cost"),
        ("writer_cost_usd", "writer cost"),
        ("figure_cost_usd", "figure cost"),
        ("prompt_tokens_api", "prompt tokens API"),
        ("note_chars", "note chars"),
    ]:
        lines.append(render_stat_row(name, payload["baseline"], key))
    lines.extend([
        "",
        f"- image_embed_max: {payload['baseline']['image_embed_max']}",
        f"- image_over_6_count: {payload['baseline']['image_over_6_count']}",
        f"- supplement_heading_count: {payload['baseline']['supplement_heading_count']}",
        f"- structure_complete_rate: {payload['baseline']['structure_complete_rate']}",
        f"- needs_fulltext_count: {payload['baseline']['needs_fulltext_count']}",
    ])
    if payload.get("experiment"):
        lines.extend([
            "",
            "### Experiment",
            "",
            "| Metric | Median | Mean | P75 |",
            "|---|---:|---:|---:|",
        ])
        for key, name in [
            ("api_cost_usd", "API cost"),
            ("part_cost_usd", "part cost"),
            ("main_cost_usd", "main cost"),
            ("writer_cost_usd", "writer cost"),
            ("figure_cost_usd", "figure cost"),
            ("prompt_tokens_api", "prompt tokens API"),
            ("note_chars", "note chars"),
        ]:
            lines.append(render_stat_row(name, payload["experiment"], key))
        lines.extend([
            "",
            f"- image_embed_max: {payload['experiment']['image_embed_max']}",
            f"- image_over_6_count: {payload['experiment']['image_over_6_count']}",
            f"- supplement_heading_count: {payload['experiment']['supplement_heading_count']}",
            f"- structure_complete_rate: {payload['experiment']['structure_complete_rate']}",
            f"- needs_fulltext_count: {payload['experiment']['needs_fulltext_count']}",
            f"- needs_fulltext_false_blocks: {payload.get('needs_fulltext_false_blocks')}",
            f"- median_cost_drop: {payload.get('median_cost_drop')}",
            "",
            "## Thresholds",
            "",
        ])
        for key, value in (payload.get("pass_fail") or {}).items():
            lines.append(f"- {key}: {'PASS' if value else 'FAIL'}")
    lines.extend(["", "## Per-paper Rows", "", "| Title | Reasons | Baseline cost | Experiment cost | Baseline prompt | Experiment prompt |", "|---|---|---:|---:|---:|---:|"])
    for pair in payload["pairs"]:
        exp = pair.get("experiment") or {}
        lines.append(
            f"| {table_cell(pair.get('title'))} | {table_cell(pair.get('selection_reasons'))} | "
            f"{pair['baseline'].get('api_cost_usd')} | {exp.get('api_cost_usd', '')} | "
            f"{pair['baseline'].get('prompt_tokens_api')} | {exp.get('prompt_tokens_api', '')} |"
        )
    return "\n".join(lines) + "\n"


def extract_field_text(analysis: dict[str, Any], category: str) -> str:
    if category == "contribution":
        value = {
            "analysis_truth": analysis.get("analysis_truth"),
            "changed_slots": (analysis.get("method") or {}).get("changed_slots"),
        }
    elif category == "method":
        value = {
            "method": analysis.get("method"),
            "formulas": analysis.get("formulas"),
        }
    elif category == "experiment":
        value = analysis.get("experiments")
    else:
        value = {
            "limitations": analysis.get("limitations"),
            "open_questions": analysis.get("open_questions"),
        }
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def similarity(a: str, b: str) -> float:
    if not a.strip() and not b.strip():
        return 1.0
    if not a.strip() or not b.strip():
        return 0.0
    return round(SequenceMatcher(None, a, b).ratio(), 6)


def analysis_json(manifest: dict[str, Any]) -> dict[str, Any]:
    work_dir = Path(str(manifest.get("work_dir") or ""))
    path = work_dir / "analysis" / "main_analysis.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def review_core(sample_json: Path, experiment_results: Path, out_json: Path, sample_size: int) -> None:
    items = load_selection(sample_json)
    experiment_by_title = experiment_manifests(experiment_results)
    pairs: list[dict[str, Any]] = []
    candidates: list[tuple[float, dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for item in items:
        base_manifest = manifest_from_selection_item(item)
        exp_manifest = experiment_by_title.get(title_key(str(item.get("paper_title") or "")))
        if not exp_manifest:
            continue
        base_cost = run_metrics(base_manifest)["api_cost_usd"]
        exp_cost = run_metrics(exp_manifest)["api_cost_usd"]
        candidates.append((abs(base_cost - exp_cost), item, base_manifest, exp_manifest))
    for _, item, base_manifest, exp_manifest in sorted(candidates, key=lambda x: x[0], reverse=True)[:sample_size]:
        base_analysis = analysis_json(base_manifest)
        exp_analysis = analysis_json(exp_manifest)
        category_scores = {
            category: similarity(extract_field_text(base_analysis, category), extract_field_text(exp_analysis, category))
            for category in ("contribution", "method", "experiment", "limitation")
        }
        pairs.append({
            "title": item.get("paper_title"),
            "selection_reasons": item.get("selection_reasons"),
            "baseline_manifest": str(resolve_path(str(item.get("baseline_manifest_path") or ""))),
            "experiment_manifest": str(Path(str(exp_manifest.get("work_dir") or "")) / "manifest.json"),
            "baseline_note": str(note_path_from_manifest(base_manifest) or ""),
            "experiment_note": str(note_path_from_manifest(exp_manifest) or ""),
            "category_similarity_proxy": category_scores,
            "llm_review_status": "pending",
        })
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": (
            "Proxy scores compare structured main_analysis JSON fields with SequenceMatcher. "
            "Use the note paths for manual or LLM review before claiming the 98% retention threshold."
        ),
        "items": pairs,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out_json": str(out_json), "items": len(pairs)}, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    if args.command == "select-sample":
        runs = load_paper_runs(
            resolve_path(args.baseline_results),
            baseline_output_root=resolve_path(args.baseline_output_root),
        )
        selected = select_runs(runs, args.sample_size)
        write_selection(selected, resolve_path(args.out_dir))
        return 0
    if args.command == "summarize":
        summarize(
            resolve_path(args.sample_json),
            resolve_path(args.experiment_results) if args.experiment_results else None,
            resolve_path(args.out_dir),
            args.report_name,
        )
        return 0
    if args.command == "review-core":
        review_core(
            resolve_path(args.sample_json),
            resolve_path(args.experiment_results),
            resolve_path(args.out_json),
            args.sample_size,
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())


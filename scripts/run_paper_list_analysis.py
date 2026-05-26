#!/usr/bin/env python3
"""Run formal analysis for rows in obsidian-vault/paper_list.csv.

This is a thin queue runner around scripts/run_local_paper_analysis.py. It keeps
paper_list.csv unchanged by default and writes per-paper results under
obsidian-vault/batches/<run_id>/.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "obsidian-vault" / "paper_list.csv"
DEFAULT_BATCH_ROOT = REPO_ROOT / "obsidian-vault" / "batches"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--state", default="Downloaded")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--shard-index", type=int, default=-1, help="Zero-based shard index for script-only parallel runs")
    parser.add_argument("--shard-count", type=int, default=0, help="Total shard count for script-only parallel runs")
    parser.add_argument("--jobs", type=int, default=1, help="Number of child analysis processes to run concurrently")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--analysis-output-root", default="", help="Output root passed to run_local_paper_analysis.py")
    parser.add_argument(
        "--vault-root",
        default="",
        help="Vault root passed to child runs. With named variants, each variant writes under <vault-root>/<variant>.",
    )
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mock-llm", action="store_true")
    parser.add_argument("--export-vault", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--conf-year", default="", help="Override venue/year folder. Defaults to venue column normalized as VENUE_YEAR.")
    parser.add_argument("--acceptance", default="unknown")
    parser.add_argument("--max-note-images", type=int, default=12)
    parser.add_argument("--mineru-output-root", default="")
    parser.add_argument("--mineru-batch-id", default="")
    parser.add_argument("--require-existing-mineru-output", action="store_true")
    parser.add_argument("--experiment-label", default="", help="Optional label passed to each child analysis run.")
    parser.add_argument(
        "--writer-reasoning-ab-efforts",
        default="",
        help="Comma-separated writer reasoning efforts for a controlled A/B run, e.g. max,medium. "
        "Each effort gets a distinct task id and output root. Pair with --extra-arg=--writer-thinking --extra-arg=enabled.",
    )
    parser.add_argument(
        "--variant",
        action="append",
        default=[],
        help="Named child-arg variant in NAME=ARGS form, e.g. current= or secw2='--section-workers 2'. Repeat for a matrix run.",
    )
    parser.add_argument("--extra-arg", action="append", default=[], help="Extra arg passed to run_local_paper_analysis.py; repeat as needed.")
    return parser.parse_args()


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def venue_to_conf_year(venue: str) -> str:
    parts = str(venue or "").strip().split()
    if len(parts) >= 2 and parts[-1].isdigit() and len(parts[-1]) == 4:
        return "_".join(parts[:-1] + [parts[-1]]).replace("-", "_")
    return ""


def row_matches_state(row: dict[str, str], state: str) -> bool:
    row_state = (row.get("state") or "").strip()
    if row_state:
        return row_state == state
    analysis_status = (row.get("analysis_status") or "").strip().lower()
    if analysis_status:
        requested = state.strip().lower()
        if requested in {"downloaded", "pending"}:
            return analysis_status != "completed" and (row.get("pdf_exists") or "True").strip().lower() == "true"
        return analysis_status == requested
    return not state


def selected_rows(source: Path, state: str) -> list[dict[str, str]]:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for index, row in enumerate(reader, start=2):
            if not row_matches_state(row, state):
                continue
            row["_csv_line"] = str(index)
            rows.append(row)
        return rows


def load_done(results_path: Path) -> set[tuple[str, str]]:
    done: set[tuple[str, str]] = set()
    if not results_path.exists():
        return done
    with results_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("status") == "done" and row.get("row_key"):
                variant_id = str(row.get("variant_id") or "")
                if not variant_id:
                    writer_effort = str(row.get("writer_reasoning_effort") or "")
                    variant_id = f"writer_{writer_effort}" if writer_effort else ""
                done.add((str(row["row_key"]), variant_id))
    return done


def row_value(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = str(row.get(name) or "").strip()
        if value:
            return value
    return ""


def row_key(row: dict[str, str]) -> str:
    return (
        paper_link_for_row(row)
        or row_value(row, "paper_title", "title")
        or row_value(row, "openreview_forum_id", "forum_id")
        or row.get("_csv_line", "")
    )


def row_task_id(row: dict[str, str], suffix: str = "") -> str:
    key = row_key(row) or "row"
    safe = "".join(ch if ch.isalnum() else "_" for ch in key).strip("_")
    safe = "_".join(part for part in safe.split("_") if part)
    base = f"paper_list_l{row.get('_csv_line', 'unknown')}_{safe[:72]}"
    return f"{base}_{suffix}" if suffix else base


def safe_variant(value: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in value).strip("_").lower()
    return "_".join(part for part in safe.split("_") if part) or "variant"


def parse_named_variants(items: list[str]) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        if "=" not in item:
            raise SystemExit(f"--variant must use NAME=ARGS form: {item}")
        raw_name, raw_args = item.split("=", 1)
        label = raw_name.strip()
        variant_id = safe_variant(label)
        if variant_id in seen:
            raise SystemExit(f"duplicate --variant name after normalization: {label}")
        seen.add(variant_id)
        variants.append({
            "id": variant_id,
            "label": label,
            "extra_args": shlex.split(raw_args),
            "writer_effort": "",
        })
    return variants


def resolve_pdf_path(row: dict[str, str]) -> Path:
    raw = row.get("pdf_path") or ""
    if not raw:
        raw = row.get("path") or ""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def paper_link_for_row(row: dict[str, str]) -> str:
    link = row_value(row, "paper_link", "pdf_url", "url")
    if link:
        return link
    forum_id = row_value(row, "openreview_forum_id", "forum_id")
    return f"https://openreview.net/forum?id={forum_id}" if forum_id else ""


def acceptance_for_row(args: argparse.Namespace, row: dict[str, str]) -> str:
    return row_value(row, "acceptance", "acceptance_type") or args.acceptance


def writer_effort_variants(args: argparse.Namespace) -> list[str]:
    efforts: list[str] = []
    for item in args.writer_reasoning_ab_efforts.split(","):
        effort = item.strip()
        if effort and effort not in efforts:
            efforts.append(effort)
    return efforts or [""]


def configured_variants(args: argparse.Namespace) -> list[dict[str, Any]]:
    named_variants = parse_named_variants(args.variant) or [{
        "id": "",
        "label": "",
        "extra_args": [],
        "writer_effort": "",
    }]
    writer_efforts = writer_effort_variants(args)
    variants: list[dict[str, Any]] = []
    seen: set[str] = set()
    for base_variant in named_variants:
        for writer_effort in writer_efforts:
            id_parts = [str(base_variant["id"])] if base_variant["id"] else []
            label_parts = [str(base_variant["label"])] if base_variant["label"] else []
            if writer_effort:
                id_parts.append(safe_variant(f"writer_{writer_effort}"))
                label_parts.append(f"writer_reasoning_{writer_effort}")
            variant_id = "_".join(id_parts)
            label = "+".join(label_parts)
            if variant_id in seen:
                raise SystemExit(f"duplicate variant id: {variant_id or '<default>'}")
            seen.add(variant_id)
            variants.append({
                "id": variant_id,
                "label": label,
                "extra_args": list(base_variant["extra_args"]),
                "writer_effort": writer_effort,
            })
    return variants


def command_for_row(args: argparse.Namespace, row: dict[str, str], *, variant: dict[str, Any] | None = None) -> list[str]:
    variant = variant or {"id": "", "label": "", "extra_args": [], "writer_effort": ""}
    pdf_path = resolve_pdf_path(row)
    conf_year = args.conf_year or venue_to_conf_year(row.get("venue", ""))
    variant_id = str(variant.get("id") or "")
    variant_extra_args = [str(item) for item in (variant.get("extra_args") or [])]
    writer_effort = str(variant.get("writer_effort") or "")
    experiment_label = args.experiment_label or ""
    if variant.get("label") and not experiment_label:
        experiment_label = str(variant["label"])
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "run_local_paper_analysis.py"),
        "--pdf", str(pdf_path),
        "--acceptance", acceptance_for_row(args, row),
        "--task-id", row_task_id(row, suffix=variant_id),
    ]
    paper_title = row_value(row, "paper_title", "title")
    if paper_title:
        cmd += ["--paper-title", paper_title]
    paper_link = paper_link_for_row(row)
    if paper_link:
        cmd += ["--paper-link", paper_link]
    openreview_forum_id = row_value(row, "openreview_forum_id", "forum_id")
    if openreview_forum_id:
        cmd += ["--openreview-forum-id", openreview_forum_id]
    if conf_year:
        cmd += ["--conf-year", conf_year]
    if args.export_vault:
        cmd.append("--export-vault")
    cmd += ["--max-note-images", str(args.max_note_images)]
    if args.mock_llm:
        cmd.append("--mock-llm")
    if args.mineru_output_root:
        cmd += ["--mineru-output-root", args.mineru_output_root]
    if args.mineru_batch_id:
        cmd += ["--mineru-batch-id", args.mineru_batch_id]
    if args.require_existing_mineru_output:
        cmd.append("--require-existing-mineru-output")
    if args.analysis_output_root:
        output_root = Path(args.analysis_output_root)
        if variant_id:
            output_root = output_root / variant_id
        cmd += ["--output-root", str(output_root)]
    if args.export_vault and args.vault_root:
        vault_root = Path(args.vault_root)
        if variant_id:
            vault_root = vault_root / variant_id
        cmd += ["--vault-root", str(vault_root)]
    if experiment_label:
        cmd += ["--experiment-label", experiment_label]
    if writer_effort:
        cmd += ["--writer-reasoning-effort", writer_effort]
    cmd.extend(args.extra_arg)
    cmd.extend(variant_extra_args)
    return cmd


def run_child(args: argparse.Namespace, row: dict[str, str], variant: dict[str, Any]) -> dict[str, Any]:
    key = row_key(row)
    pdf_path = resolve_pdf_path(row)
    started = time.monotonic()
    if not pdf_path.exists():
        record = {"row_key": key, "status": "failed", "error": f"missing pdf: {pdf_path}", "row": row}
    else:
        cmd = command_for_row(args, row, variant=variant)
        proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True)
        status = "done" if proc.returncode == 0 else "failed"
        record = {
            "row_key": key,
            "status": status,
            "returncode": proc.returncode,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
            "command": cmd,
            "row": row,
        }
    record["variant_id"] = str(variant.get("id") or "")
    record["variant_label"] = str(variant.get("label") or "")
    record["variant_extra_args"] = list(variant.get("extra_args") or [])
    record["writer_reasoning_effort"] = str(variant.get("writer_effort") or "") or None
    return record


def main() -> None:
    args = parse_args()
    args.jobs = max(1, args.jobs)
    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"paper list not found: {source}")

    run_id = args.run_id or now_id()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else DEFAULT_BATCH_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / "results.jsonl"
    summary_path = out_dir / "summary.json"

    rows = selected_rows(source, args.state)
    if (args.shard_index >= 0) or args.shard_count:
        if args.shard_count <= 0:
            raise SystemExit("--shard-count is required when --shard-index is set")
        if args.shard_index < 0 or args.shard_index >= args.shard_count:
            raise SystemExit("--shard-index must be in [0, shard-count)")
        rows = [row for idx, row in enumerate(rows) if idx % args.shard_count == args.shard_index]
    if args.offset:
        rows = rows[args.offset:]
    if args.limit:
        rows = rows[:args.limit]

    variants = configured_variants(args)
    completed = load_done(results_path) if args.resume else set()
    planned_items: list[tuple[dict[str, str], dict[str, Any]]] = []
    for row in rows:
        key = row_key(row)
        for variant in variants:
            if (key, str(variant.get("id") or "")) not in completed:
                planned_items.append((row, variant))
    planned_rows = {row_key(row) for row, _ in planned_items}

    manifest = {
        "run_id": run_id,
        "source": str(source),
        "state": args.state,
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "jobs": args.jobs,
        "selected": len(rows),
        "planned": len(planned_rows),
        "planned_child_runs": len(planned_items),
        "variants": variants,
        "out_dir": str(out_dir),
        "analysis_output_root": args.analysis_output_root,
        "vault_root": args.vault_root,
        "experiment_label": args.experiment_label,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.dry_run:
        for row, variant in planned_items:
            print(json.dumps({
                "row_key": row_key(row),
                "variant_id": variant.get("id") or None,
                "variant_label": variant.get("label") or None,
                "writer_reasoning_effort": variant.get("writer_effort") or None,
                "command": command_for_row(args, row, variant=variant),
            }, ensure_ascii=False))
        summary_path.write_text(json.dumps({**manifest, "status": "planned"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return

    counts = {"done": 0, "failed": 0, "skipped": 0}

    def write_record(handle: Any, record: dict[str, Any]) -> None:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()

    with results_path.open("a", encoding="utf-8") as results:
        if args.jobs == 1:
            for row, variant in planned_items:
                write_record(results, run_child(args, row, variant))
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
                futures = [
                    executor.submit(run_child, args, row, variant)
                    for row, variant in planned_items
                ]
                for future in concurrent.futures.as_completed(futures):
                    write_record(results, future.result())

    summary = {**manifest, **counts, "results_path": str(results_path), "finished_at": datetime.now(timezone.utc).isoformat()}
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

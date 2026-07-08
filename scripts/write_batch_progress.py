#!/usr/bin/env python3
"""Write a human-readable progress snapshot for a batch analysis run."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex
import subprocess
import time
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", help="Batch run directory under obsidian-vault/batches")
    parser.add_argument("--output-md", default="PROGRESS.md")
    parser.add_argument("--output-json", default="progress.json")
    return parser.parse_args()


def compact(value: str, limit: int = 96) -> str:
    text = " ".join(str(value or "").replace("|", "/").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append({"status": "json_error", "raw": line[:500]})
    return rows


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def row_matches_state(row: dict[str, str], state: str) -> bool:
    if not state:
        return True
    return (row.get("state") or "").strip() == state


def title_for_csv_line(rows: list[dict[str, str]], csv_line: int | None) -> str:
    if not csv_line:
        return ""
    index = csv_line - 2
    if index < 0 or index >= len(rows):
        return ""
    row = rows[index]
    return row.get("paper_title") or row.get("title") or row.get("paper_link") or ""


def read_manifest(run_dir: Path) -> dict[str, Any]:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def batch_run_ids(manifest: dict[str, Any], fallback_run_id: str) -> dict[int, str]:
    run_ids: dict[int, str] = {}
    for item in manifest.get("started_commands") or []:
        session = str(item.get("session") or "")
        match = re.search(r"_b(\d{4})$", session)
        if match:
            run_ids[int(match.group(1))] = session
            continue
        result_dir = str(item.get("result_dir") or "")
        match = re.search(r"batch_(\d{4})$", result_dir)
        if match and session:
            run_ids[int(match.group(1))] = session
    return run_ids or {number: f"{fallback_run_id}_b{number:04d}" for number in range(1, 9999)}


def batch_analysis_roots(manifest: dict[str, Any], repo_root: Path) -> dict[int, Path]:
    roots: dict[int, Path] = {}
    for item in manifest.get("started_commands") or []:
        session = str(item.get("session") or "")
        result_dir = str(item.get("result_dir") or "")
        batch_number: int | None = None
        match = re.search(r"_b(\d{4})$", session) or re.search(r"batch_(\d{4})$", result_dir)
        if match:
            batch_number = int(match.group(1))
        if batch_number is None:
            continue
        analysis_root = str(item.get("analysis_output_root") or "")
        if not analysis_root and item.get("command"):
            parts = shlex.split(str(item["command"]))
            if "--analysis-output-root" in parts:
                index = parts.index("--analysis-output-root")
                if index + 1 < len(parts):
                    analysis_root = parts[index + 1]
        if analysis_root:
            path = Path(analysis_root)
            roots[batch_number] = path if path.is_absolute() else repo_root / path
    return roots


def latest_progress(batch_run_id: str, repo_root: Path, analysis_root: Path | None = None) -> dict[str, Any]:
    root = analysis_root or repo_root / "_private" / "local_analysis_runs" / batch_run_id
    progress_files = [p for p in root.rglob("progress.jsonl") if p.is_file()] if root.exists() else []
    if not progress_files:
        return {}
    progress_path = max(progress_files, key=lambda p: p.stat().st_mtime)
    lines = [line for line in progress_path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    event: dict[str, Any] = {}
    if lines:
        try:
            event = json.loads(lines[-1])
        except json.JSONDecodeError:
            event = {"event": "json_error", "raw": lines[-1][:300]}
    task_id = progress_path.parent.name
    csv_line_match = re.search(r"paper_list_l(\d+)_", task_id)
    csv_line = int(csv_line_match.group(1)) if csv_line_match else None
    return {
        "task_id": task_id,
        "csv_line": csv_line,
        "path": str(progress_path),
        "mtime": progress_path.stat().st_mtime,
        "age_seconds": round(time.time() - progress_path.stat().st_mtime, 1),
        "last_event": event.get("event") or "",
        "last_event_at": event.get("at") or "",
    }


def recent_progress_events(root: Path, *, limit: int = 5) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    events: list[dict[str, Any]] = []
    for progress_path in root.rglob("progress.jsonl"):
        if not progress_path.is_file():
            continue
        lines = [line for line in progress_path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
        if not lines:
            continue
        try:
            event = json.loads(lines[-1])
        except json.JSONDecodeError:
            event = {"event": "json_error", "raw": lines[-1][:300]}
        task_id = progress_path.parent.name
        csv_line_match = re.search(r"paper_list_l(\d+)_", task_id)
        events.append(
            {
                "task_id": task_id,
                "csv_line": int(csv_line_match.group(1)) if csv_line_match else None,
                "path": str(progress_path),
                "mtime": progress_path.stat().st_mtime,
                "age_seconds": round(time.time() - progress_path.stat().st_mtime, 1),
                "last_event": event.get("event") or "",
                "last_event_at": event.get("at") or "",
            }
        )
    return sorted(events, key=lambda item: item["mtime"], reverse=True)[:limit]


def running_process_titles(batch_run_ids_by_number: dict[int, str]) -> dict[int, str]:
    try:
        proc = subprocess.run(
            ["ps", "-eo", "pid,ppid,cmd"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return {}
    titles: dict[int, str] = {}
    run_to_batch = {run_id: batch for batch, run_id in batch_run_ids_by_number.items()}
    for line in proc.stdout.splitlines():
        if "run_local_paper_analysis.py" not in line:
            continue
        matched_run_id = ""
        for run_id in run_to_batch:
            if run_id in line:
                matched_run_id = run_id
                break
        if not matched_run_id:
            continue
        batch_number = run_to_batch[matched_run_id]
        title_match = re.search(r"--paper-title\s+(.+?)\s+--paper-link\s+", line)
        if title_match:
            titles[batch_number] = title_match.group(1)
    return titles


def load_run_id(run_dir: Path, manifest: dict[str, Any]) -> str:
    if manifest.get("run_id"):
        return str(manifest["run_id"])
    return run_dir.name


def batch_number_from_path(path: Path) -> int | None:
    match = re.search(r"batch_(\d{4})\.csv$", path.name)
    return int(match.group(1)) if match else None


def build_script_snapshot(run_dir: Path, manifest: dict[str, Any], run_id: str, generated_at: str) -> dict[str, Any]:
    repo_root = Path.cwd()
    source = Path(str(manifest.get("source") or ""))
    if source and not source.is_absolute():
        source = repo_root / source
    state = str(manifest.get("state") or "")
    csv_rows = [row for row in read_csv_rows(source) if row_matches_state(row, state)]
    total = int(manifest.get("selected") or len(csv_rows))
    results_path = run_dir / "results.jsonl"
    results = read_jsonl(results_path)
    done = [row for row in results if row.get("status") == "done"]
    skipped = [row for row in results if row.get("status") == "skipped"]
    failed = [row for row in results if row.get("status") not in {"done", "skipped"}]
    analysis_root_raw = str(manifest.get("analysis_output_root") or "")
    analysis_root = Path(analysis_root_raw) if analysis_root_raw else repo_root / "_private" / "local_analysis_runs" / run_id
    if not analysis_root.is_absolute():
        analysis_root = repo_root / analysis_root
    progress_events = recent_progress_events(analysis_root, limit=5)
    process_titles = running_process_titles({1: run_id})
    active_title = process_titles.get(1) or ""
    if not active_title and progress_events:
        active_title = title_for_csv_line(csv_rows, progress_events[0].get("csv_line"))
    last_done = ""
    if done or skipped:
        row = (done or skipped)[-1].get("row") or {}
        last_done = row.get("paper_title") or row.get("title") or (done or skipped)[-1].get("row_key") or ""
    completed = len(done) + len(skipped)
    remaining = max(total - completed - len(failed), 0)
    return {
        "run_dir": str(run_dir),
        "run_id": run_id,
        "mode": "script",
        "generated_at": generated_at,
        "total": total,
        "done": len(done),
        "skipped": len(skipped),
        "failed": len(failed),
        "remaining": remaining,
        "percent_done": round((completed / total * 100) if total else 0.0, 1),
        "results_path": str(results_path),
        "active_title": active_title,
        "progress_events": progress_events,
        "last_completed_title": last_done,
        "batches": [
            {
                "batch": "script",
                "batch_number": 1,
                "total": total,
                "done": len(done),
                "skipped": len(skipped),
                "failed": len(failed),
                "remaining": remaining,
                "percent_done": round((completed / total * 100) if total else 0.0, 1),
                "active_title": active_title,
                "active_task_id": progress_events[0]["task_id"] if progress_events else "",
                "last_event": progress_events[0]["last_event"] if progress_events else "",
                "last_event_age_seconds": progress_events[0]["age_seconds"] if progress_events else None,
                "last_event_at": progress_events[0]["last_event_at"] if progress_events else "",
                "last_completed_title": last_done,
                "results_path": str(results_path),
            }
        ],
    }


def build_snapshot(run_dir: Path) -> dict[str, Any]:
    repo_root = Path.cwd()
    manifest = read_manifest(run_dir)
    run_id = load_run_id(run_dir, manifest)
    batch_run_ids_by_number = batch_run_ids(manifest, run_id)
    batch_analysis_roots_by_number = batch_analysis_roots(manifest, repo_root)
    process_titles = running_process_titles(batch_run_ids_by_number)
    generated_at = datetime.now(timezone.utc).isoformat()
    has_batch_csv = bool(list(run_dir.glob("batch_*.csv")))
    if (not has_batch_csv and (run_dir / "results.jsonl").exists()) or (not has_batch_csv and manifest.get("analysis_output_root")):
        return build_script_snapshot(run_dir, manifest, run_id, generated_at)
    batches: list[dict[str, Any]] = []
    total_rows = total_done = total_failed = 0

    for batch_csv in sorted(run_dir.glob("batch_*.csv")):
        batch_number = batch_number_from_path(batch_csv)
        if batch_number is None:
            continue
        csv_rows = read_csv_rows(batch_csv)
        results_path = run_dir / "results" / f"batch_{batch_number:04d}" / "results.jsonl"
        results = read_jsonl(results_path)
        done = [row for row in results if row.get("status") == "done"]
        failed = [row for row in results if row.get("status") not in {"done"}]
        batch_run_id = batch_run_ids_by_number.get(batch_number, f"{run_id}_b{batch_number:04d}")
        progress = latest_progress(batch_run_id, repo_root, batch_analysis_roots_by_number.get(batch_number))
        active_title = process_titles.get(batch_number) or title_for_csv_line(csv_rows, progress.get("csv_line"))
        last_done = ""
        if done:
            row = done[-1].get("row") or {}
            last_done = row.get("paper_title") or row.get("title") or done[-1].get("row_key") or ""
        batch_total = len(csv_rows)
        total_rows += batch_total
        total_done += len(done)
        total_failed += len(failed)
        batches.append(
            {
                "batch": f"batch_{batch_number:04d}",
                "batch_number": batch_number,
                "total": batch_total,
                "done": len(done),
                "failed": len(failed),
                "remaining": max(batch_total - len(done) - len(failed), 0),
                "percent_done": round((len(done) / batch_total * 100) if batch_total else 0.0, 1),
                "active_title": active_title,
                "active_task_id": progress.get("task_id") or "",
                "last_event": progress.get("last_event") or "",
                "last_event_age_seconds": progress.get("age_seconds"),
                "last_event_at": progress.get("last_event_at") or "",
                "last_completed_title": last_done,
                "results_path": str(results_path),
            }
        )
    return {
        "run_dir": str(run_dir),
        "run_id": run_id,
        "mode": "batch",
        "generated_at": generated_at,
        "total": total_rows,
        "done": total_done,
        "skipped": 0,
        "failed": total_failed,
        "remaining": max(total_rows - total_done - total_failed, 0),
        "percent_done": round((total_done / total_rows * 100) if total_rows else 0.0, 1),
        "batches": batches,
    }


def render_markdown(snapshot: dict[str, Any]) -> str:
    lines = [
        "# Batch Progress",
        "",
        f"- Run: `{snapshot['run_id']}`",
        f"- Mode: `{snapshot.get('mode', 'batch')}`",
        f"- Updated: `{snapshot['generated_at']}`",
        f"- Overall: `{snapshot['done']}/{snapshot['total']}` done (`{snapshot['percent_done']}%`), `{snapshot.get('skipped', 0)}` skipped, `{snapshot['failed']}` failed, `{snapshot['remaining']}` remaining",
        "",
        "| Unit | Done | Skipped | Failed | Active paper | Last event | Event age | Last completed |",
        "| --- | ---: | ---: | ---: | --- | --- | ---: | --- |",
    ]
    for batch in snapshot["batches"]:
        event_age = batch["last_event_age_seconds"]
        event_age_text = "" if event_age is None else f"{event_age}s"
        lines.append(
            "| {batch} | {done}/{total} ({percent}%) | {skipped} | {failed} | {active} | {event} | {age} | {last} |".format(
                batch=batch["batch"],
                done=batch["done"],
                total=batch["total"],
                percent=batch["percent_done"],
                skipped=batch.get("skipped", 0),
                failed=batch["failed"],
                active=compact(batch["active_title"], 78),
                event=compact(batch["last_event"], 32),
                age=event_age_text,
                last=compact(batch["last_completed_title"], 78),
            )
        )
    lines.extend(
        [
            "",
            "## Refresh",
            "",
            "Run this from the repository root to refresh the snapshot:",
            "",
            f"```bash\npython3 scripts/write_batch_progress.py {snapshot['run_dir']}\n```",
            "",
            "Detailed per-paper records remain in `results/batch_*/results.jsonl`; active per-paper stage events are under `_private/local_analysis_runs/<run_id>_b*/.../progress.jsonl`.",
            "",
        ]
    )
    if snapshot.get("mode") == "script":
        lines[-2] = "Detailed per-paper records remain in `results.jsonl`; active per-paper stage events are under the configured `analysis_output_root`."
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = Path.cwd() / run_dir
    run_dir = run_dir.resolve()
    snapshot = build_snapshot(run_dir)
    (run_dir / args.output_json).write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / args.output_md).write_text(render_markdown(snapshot), encoding="utf-8")
    print(run_dir / args.output_md)
    print(run_dir / args.output_json)


if __name__ == "__main__":
    main()

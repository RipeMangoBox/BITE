"""Run MinerU CLI for an ICLR 2026 PDF batch and preserve raw artifacts.

This script does not write PostgreSQL rows and does not run analysis/writer
agents. Its only durable target is the local raw MinerU output tree.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = REPO_ROOT / "_private" / "iclr26_batch" / "reports"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_private" / "iclr26_batch" / "mineru_outputs"
DEFAULT_MINERU_BIN = shutil.which("mineru") or "/home/ripemangobox/miniconda3/bin/mineru"


@dataclass(frozen=True)
class BatchRow:
    batch_id: str
    title: str
    openreview_forum_id: str
    sha256: str
    size_bytes: int
    path: str
    source: str
    manifest_paper_id: str
    theme_bucket: str


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def read_batch_manifest(path: Path) -> list[BatchRow]:
    rows: list[BatchRow] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            raw = json.loads(line)
            missing = [k for k in ("batch_id", "title", "openreview_forum_id", "sha256", "path") if not raw.get(k)]
            if missing:
                raise SystemExit(f"{path}:{line_no} missing required field(s): {missing}")
            rows.append(BatchRow(
                batch_id=raw["batch_id"],
                title=raw["title"],
                openreview_forum_id=raw["openreview_forum_id"],
                sha256=raw["sha256"],
                size_bytes=int(raw.get("size_bytes") or 0),
                path=raw["path"],
                source=raw.get("source") or "unknown",
                manifest_paper_id=raw.get("manifest_paper_id") or raw["openreview_forum_id"],
                theme_bucket=raw.get("theme_bucket") or "other",
            ))
    return rows


def append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")


def artifact_status(output_dir: Path) -> dict[str, Any]:
    md_files = sorted(output_dir.rglob("*.md")) if output_dir.exists() else []
    content_files = (
        sorted(output_dir.rglob("*content_list_v2.json"))
        or sorted(output_dir.rglob("*content_list.json"))
        if output_dir.exists()
        else []
    )
    middle_files = sorted(output_dir.rglob("*_middle.json")) if output_dir.exists() else []
    model_files = sorted(output_dir.rglob("*_model.json")) if output_dir.exists() else []
    layout_pdfs = sorted(output_dir.rglob("*_layout.pdf")) if output_dir.exists() else []
    images = []
    if output_dir.exists():
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            images.extend(output_dir.rglob(ext))
    ok = bool(md_files) and bool(content_files)
    return {
        "ok": ok,
        "output_dir": _rel(output_dir),
        "markdown_count": len(md_files),
        "content_list_count": len(content_files),
        "middle_json_count": len(middle_files),
        "model_json_count": len(model_files),
        "layout_pdf_count": len(layout_pdfs),
        "image_count": len(images),
        "sample_files": [_rel(p) for p in (md_files[:2] + content_files[:2] + images[:2])],
    }


def run_one(
    row: BatchRow,
    *,
    mineru_bin: str,
    output_root: Path,
    backend: str,
    timeout: int,
    dry_run: bool,
    resume: bool,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    pdf_path = (REPO_ROOT / row.path).resolve()
    output_dir = output_root / row.batch_id / row.openreview_forum_id
    status_before = artifact_status(output_dir)
    result: dict[str, Any] = {
        "batch_id": row.batch_id,
        "title": row.title,
        "openreview_forum_id": row.openreview_forum_id,
        "pdf_path": row.path,
        "raw_output_dir": _rel(output_dir),
        "started_at": started.isoformat(),
    }

    if not pdf_path.exists():
        result.update({"status": "failed", "problems": ["missing_pdf"]})
        return result

    command = [mineru_bin, "-p", str(pdf_path), "-o", str(output_dir), "-b", backend]
    result["command"] = command

    if resume and status_before["ok"]:
        completed = datetime.now(timezone.utc)
        result.update({
            "status": "succeeded",
            "skipped": True,
            "completed_at": completed.isoformat(),
            "duration_seconds": round((completed - started).total_seconds(), 3),
            "artifacts": status_before,
        })
        return result

    if dry_run:
        result.update({
            "status": "planned",
            "artifacts": status_before,
        })
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        (output_dir / "mineru_stdout.log").write_text(exc.stdout or "", encoding="utf-8", errors="ignore")
        (output_dir / "mineru_stderr.log").write_text(exc.stderr or "", encoding="utf-8", errors="ignore")
        completed = datetime.now(timezone.utc)
        result.update({
            "status": "failed",
            "completed_at": completed.isoformat(),
            "duration_seconds": round((completed - started).total_seconds(), 3),
            "problems": [f"mineru_timeout_after_{timeout}s"],
            "artifacts": artifact_status(output_dir),
        })
        return result

    (output_dir / "mineru_stdout.log").write_text(proc.stdout or "", encoding="utf-8", errors="ignore")
    (output_dir / "mineru_stderr.log").write_text(proc.stderr or "", encoding="utf-8", errors="ignore")
    completed = datetime.now(timezone.utc)
    artifacts = artifact_status(output_dir)
    problems: list[str] = []
    if proc.returncode != 0:
        problems.append(f"mineru_exit_{proc.returncode}")
    if not artifacts["ok"]:
        if artifacts["markdown_count"] == 0:
            problems.append("missing_markdown")
        if artifacts["content_list_count"] == 0:
            problems.append("missing_content_list_json")

    result.update({
        "status": "failed" if problems else "succeeded",
        "completed_at": completed.isoformat(),
        "duration_seconds": round((completed - started).total_seconds(), 3),
        "returncode": proc.returncode,
        "artifacts": artifacts,
    })
    if problems:
        result["problems"] = problems
        result["stderr_tail"] = (proc.stderr or "")[-1000:]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-manifest", required=True)
    parser.add_argument("--batch-id", default="")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--mineru-bin", default=DEFAULT_MINERU_BIN)
    parser.add_argument("--backend", default="pipeline")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = Path(args.batch_manifest)
    rows = read_batch_manifest(manifest)
    if not rows:
        raise SystemExit(f"No rows in {manifest}")
    batch_id = args.batch_id or rows[0].batch_id
    if any(row.batch_id != batch_id for row in rows):
        raise SystemExit("Manifest contains multiple batch_id values; pass the matching --batch-id explicitly")

    mineru_bin = args.mineru_bin
    if not args.dry_run and not mineru_bin:
        raise SystemExit("MinerU binary not found; pass --mineru-bin")
    if not args.dry_run and not Path(mineru_bin).exists():
        resolved = shutil.which(mineru_bin)
        if resolved:
            mineru_bin = resolved
        else:
            raise SystemExit(f"MinerU binary not found: {mineru_bin}")

    report_dir = Path(args.report_dir)
    suffix = batch_id.rsplit("_", 1)[-1]
    progress_path = report_dir / f"mineru_raw_batch_{suffix}_progress.jsonl"
    summary_path = report_dir / f"mineru_raw_batch_{suffix}_summary.json"
    if not args.resume and not args.dry_run:
        progress_path.parent.mkdir(parents=True, exist_ok=True)
        progress_path.write_text("", encoding="utf-8")

    completed_ids: set[str] = set()
    if args.resume and progress_path.exists():
        with progress_path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                raw = json.loads(line)
                if raw.get("status") == "succeeded" and raw.get("openreview_forum_id"):
                    completed_ids.add(raw["openreview_forum_id"])

    output_root = Path(args.output_root)
    for index, row in enumerate(rows, 1):
        if row.openreview_forum_id in completed_ids:
            print(f"[{index}/{len(rows)}] SKIP {row.openreview_forum_id} {row.title[:80]}", flush=True)
            continue
        print(f"[{index}/{len(rows)}] MinerU raw {row.openreview_forum_id} {row.title[:80]}", flush=True)
        result = run_one(
            row,
            mineru_bin=mineru_bin,
            output_root=output_root,
            backend=args.backend,
            timeout=args.timeout,
            dry_run=args.dry_run,
            resume=args.resume,
        )
        if not args.dry_run:
            append_jsonl(progress_path, result)
        print(f"  status={result['status']} output={result['raw_output_dir']}", flush=True)

    all_progress: list[dict[str, Any]] = []
    if not args.dry_run and progress_path.exists():
        with progress_path.open(encoding="utf-8") as f:
            all_progress = [json.loads(line) for line in f if line.strip()]
    succeeded = [r for r in all_progress if r.get("status") == "succeeded"]
    failed = [r for r in all_progress if r.get("status") == "failed"]
    planned = [r for r in all_progress if r.get("status") == "planned"]
    summary = {
        "batch_id": batch_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "batch_manifest": _rel(manifest),
        "raw_output_root": _rel(output_root),
        "selected_count": len(rows),
        "processed_count": len(rows) if args.dry_run else len(all_progress),
        "succeeded_count": 0 if args.dry_run else len(succeeded),
        "failed_count": 0 if args.dry_run else len(failed),
        "planned_count": len(rows) if args.dry_run else len(planned),
        "progress_path": _rel(progress_path),
        "failed": failed,
    }
    if args.dry_run:
        summary["summary_path_if_executed"] = _rel(summary_path)
    else:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()

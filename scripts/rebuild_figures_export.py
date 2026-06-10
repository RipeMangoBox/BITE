#!/usr/bin/env python3
"""Rebuild figure summaries, figure placement, and vault export for completed runs.

This recovery tool reuses existing parse/main-analysis/report artifacts. It does
not rerun MinerU, part analysis, main analysis, or section writers.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import run_local_paper_analysis as runner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work_dirs", nargs="+", help="Completed per-paper work directories")
    parser.add_argument("--env-file", default=str(runner.DEFAULT_ENV_FILE))
    parser.add_argument("--vault-root", default=str(runner.DEFAULT_VAULT_ROOT))
    parser.add_argument("--vault-note-dir", default="")
    parser.add_argument("--vault-asset-root", default="")
    parser.add_argument("--figure-provider", choices=["none", "deepseek", "openai", "kimi"], default="deepseek")
    parser.add_argument("--figure-model", default="")
    parser.add_argument("--figure-base-url", default="")
    parser.add_argument("--figure-api-key-env", default="")
    parser.add_argument("--figure-temperature", type=float, default=0.1)
    parser.add_argument("--figure-visual-summary-max-items", type=int, default=8)
    parser.add_argument("--figure-visual-summary-max-tokens", type=int, default=1024)
    parser.add_argument("--figure-placement-max-tokens", type=int, default=4096)
    parser.add_argument("--max-note-images", type=int, default=12)
    parser.add_argument("--force", action="store_true", help="Overwrite existing figure/export artifacts")
    parser.add_argument("--continue-on-error", action="store_true", help="Record per-run failures instead of aborting the whole batch")
    parser.add_argument("--jobs", type=int, default=1)
    return parser.parse_args()


def _manifest_value(manifest: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(manifest.get(key) or "").strip()
        if value:
            return value
    return ""


def build_runner_args(args: argparse.Namespace, work_dir: Path, manifest: dict[str, Any]) -> argparse.Namespace:
    inputs = manifest.get("inputs") or {}
    vault_export = manifest.get("vault_export") if isinstance(manifest.get("vault_export"), dict) else {}
    pdf = str(inputs.get("pdf") or "")
    paper_pdf = str(inputs.get("paper_pdf") or "")
    if not paper_pdf:
        resolution = inputs.get("paper_pdf_resolution") or {}
        paper_pdf = str(resolution.get("resolved") or "")
    ns = argparse.Namespace(
        mock_llm=False,
        resume=not args.force,
        force=args.force,
        figure_provider=args.figure_provider,
        figure_model=args.figure_model,
        figure_base_url=args.figure_base_url,
        figure_api_key_env=args.figure_api_key_env,
        figure_temperature=args.figure_temperature,
        figure_visual_summary_max_items=args.figure_visual_summary_max_items,
        figure_visual_summary_max_tokens=args.figure_visual_summary_max_tokens,
        figure_placement_max_tokens=args.figure_placement_max_tokens,
        max_note_images=args.max_note_images,
        vault_root=args.vault_root,
        vault_note_dir=args.vault_note_dir,
        vault_note_path=str(vault_export.get("note_path") or ""),
        vault_asset_root=args.vault_asset_root,
        paper_pdf=paper_pdf,
        pdf=pdf,
        conf_year=_manifest_value(manifest, "conf_year"),
        paper_link=_manifest_value(manifest, "paper_link"),
        acceptance=_manifest_value(manifest, "acceptance"),
        openreview_forum_id=_manifest_value(manifest, "openreview_forum_id"),
        topic_assignments=_manifest_value(manifest, "topic_assignments"),
        theme_bucket=_manifest_value(manifest, "theme_bucket"),
        output_root=str(work_dir.parent),
        env_file=args.env_file,
    )
    if not ns.vault_asset_root:
        ns.vault_asset_root = str(Path(ns.vault_root).expanduser().resolve() / "assets" / "figures" / "papers")
    runner.resolve_figure_llm_config(ns)
    return ns


async def rebuild_one(args: argparse.Namespace, work_dir: Path) -> dict[str, Any]:
    manifest_path = work_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_args = build_runner_args(args, work_dir, manifest)
    progress_path = work_dir / "progress.jsonl"
    task_id = str(manifest.get("task_id") or work_dir.name)

    figures_path = work_dir / "parse" / "figures_tables.json"
    analysis_path = work_dir / "analysis" / "main_analysis.json"
    report_path = work_dir / "report" / "final_report.md"
    for path in (figures_path, analysis_path, report_path):
        if not path.exists():
            raise FileNotFoundError(f"missing required artifact: {path}")

    if args.force:
        mineru_raw = work_dir / "parse" / "mineru_raw"
        try:
            artifacts = runner.find_mineru_artifacts(mineru_raw)
            figures_tables = runner.extract_figures_tables(
                artifacts.content_list_path,
                source_root=artifacts.root,
            )
            runner.atomic_write_json(figures_path, figures_tables)
        except Exception:  # noqa: BLE001
            figures_tables = json.loads(figures_path.read_text(encoding="utf-8"))
    else:
        figures_tables = json.loads(figures_path.read_text(encoding="utf-8"))
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    report = report_path.read_text(encoding="utf-8")
    title = str((analysis.get("paper_metadata") or {}).get("title") or manifest.get("paper_title") or task_id)

    previous_resume = run_args.resume
    if args.force:
        for stale in (
            work_dir / "parse" / "figure_visual_summaries.json",
            work_dir / "report" / "figure_placements.json",
        ):
            if stale.exists():
                stale.unlink()
    figures_tables, visual_usage = await runner.enrich_figure_visual_summaries(
        run_args,
        figures_tables=figures_tables,
        work_dir=work_dir,
        progress_path=progress_path,
    )
    run_args.resume = previous_resume
    copied_figures = runner.copy_vault_figures(
        figures_tables,
        task_id=task_id,
        asset_root=Path(run_args.vault_asset_root).expanduser().resolve(),
    )
    placements, placement_usage = await runner.run_figure_placement(
        run_args,
        analysis=analysis,
        report=report,
        copied_figures=copied_figures,
        work_dir=work_dir,
        progress_path=progress_path,
    )
    export = runner.export_to_vault(
        run_args,
        task_id=task_id,
        title=title,
        work_dir=work_dir,
        analysis=analysis,
        report=report,
        figures_tables=figures_tables,
        figure_placements=placements,
        progress_path=progress_path,
    )
    runner.append_jsonl(progress_path, {
        "event": "figure_export_rebuilt",
        "at": runner.now_iso(),
        "figure_provider": run_args.figure_provider,
        "visual_summary_usage": visual_usage,
        "figure_placement_usage": placement_usage,
        "validation_ok": (export.get("validation") or {}).get("ok"),
    })
    return {
        "work_dir": str(work_dir),
        "note_path": export.get("note_path"),
        "validation_ok": (export.get("validation") or {}).get("ok"),
        "image_embed_count": ((export.get("validation") or {}).get("image_embed_count")),
        "figure_provider": run_args.figure_provider,
    }


async def main_async() -> None:
    args = parse_args()
    runner.load_env_file(Path(args.env_file))
    work_dirs = [Path(item).expanduser().resolve() for item in args.work_dirs]
    sem = asyncio.Semaphore(max(1, args.jobs))

    async def one(path: Path) -> dict[str, Any]:
        async with sem:
            try:
                result = await rebuild_one(args, path)
                result["status"] = "done"
                return result
            except Exception as exc:  # noqa: BLE001
                if not args.continue_on_error:
                    raise
                return {
                    "work_dir": str(path),
                    "status": "failed",
                    "validation_ok": False,
                    "error": str(exc),
                }

    results = await asyncio.gather(*(one(path) for path in work_dirs))
    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

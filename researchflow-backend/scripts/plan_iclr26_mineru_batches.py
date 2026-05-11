"""Plan ICLR 2026 MinerU-only raw artifact batches.

This script reads the verified discovery manifest plus the existing batch_0001
contract and writes batch PDF manifests/contracts/prompts for agents that first
preserve raw MinerU CLI artifacts under _private/.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DISCOVERY = REPO_ROOT / "_private" / "iclr26_batch" / "manifests" / "discovered_pdfs.jsonl"
DEFAULT_CONTRACT_DIR = REPO_ROOT / "_private" / "iclr26_batch" / "contracts"
DEFAULT_MANIFEST_DIR = REPO_ROOT / "_private" / "iclr26_batch" / "manifests"
DEFAULT_PROMPT_DIR = REPO_ROOT / "prompt"
DEFAULT_RAW_OUTPUT_ROOT = REPO_ROOT / "_private" / "iclr26_batch" / "mineru_outputs"

THEME_ORDER = [
    "llm_rl_agent",
    "benchmark_safety",
    "science_tabular_graph",
    "vision_3d",
    "optimization_training",
    "other",
]

CANARY_TITLES = {
    "Opponent Shaping in LLM Agents",
    "How NOT to benchmark your SITE metric: Beyond Static Leaderboards and Towards Realistic Evaluation.",
    "Flock: A Knowledge Graph Foundation Model via Learning on Random Walks",
    "3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis",
    "DiffusionBlocks: Block-wise Neural Network Training via Diffusion Interpretation",
}


@dataclass(frozen=True)
class PaperRow:
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


def _theme_bucket(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ("reinforcement learning", "rlhf", "reasoning", "language model", "agent", "llm")):
        return "llm_rl_agent"
    if any(k in t for k in ("benchmark", "security", "safety", "alignment", "leaderboard")):
        return "benchmark_safety"
    if any(k in t for k in ("molecular", "protein", "graph", "tabular", "bayesian", "knowledge graph", "conformation")):
        return "science_tabular_graph"
    if any(k in t for k in ("vision", "image", "video", "gaussian", "3d", "point cloud", "camera")):
        return "vision_3d"
    if any(k in t for k in ("optimization", "training", "gradient", "adam", "sgd", "diffusion")):
        return "optimization_training"
    return "other"


def read_discovery(path: Path) -> list[PaperRow]:
    rows: list[PaperRow] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            raw = json.loads(line)
            if raw.get("conf_year") != "ICLR_2026":
                continue
            if not raw.get("openreview_forum_id"):
                continue
            title = raw.get("title_guess") or ""
            pdf_path = raw.get("path") or ""
            sha = raw.get("sha256") or ""
            if not title or not pdf_path or not sha:
                continue
            if not (REPO_ROOT / pdf_path).exists():
                continue
            rows.append(PaperRow(
                title=title,
                openreview_forum_id=raw.get("openreview_forum_id") or "",
                sha256=sha,
                size_bytes=int(raw.get("size_bytes") or 0),
                path=pdf_path,
                source=raw.get("source") or "unknown",
                manifest_paper_id=raw.get("manifest_paper_id") or "",
                theme_bucket=_theme_bucket(title),
            ))
    return rows


def contract_ids(path: Path) -> list[str]:
    ids: list[str] = []
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.search(r"\|\s*\d+\s*\|.*\|\s*\[([^\]]+)\]\(https://openreview\.net/forum\?id=", line)
        if match:
            ids.append(match.group(1))
    return ids


def select_next_batch(rows: Iterable[PaperRow], used_forum_ids: set[str], limit: int) -> list[PaperRow]:
    eligible = [
        r for r in rows
        if r.openreview_forum_id not in used_forum_ids
        and r.title not in CANARY_TITLES
    ]
    selected: list[PaperRow] = []
    used_sha: set[str] = set()

    per_bucket = max(1, limit // len(THEME_ORDER))
    for bucket in THEME_ORDER:
        bucket_rows = sorted(
            [r for r in eligible if r.theme_bucket == bucket and r.sha256 not in used_sha],
            key=lambda r: (
                0 if 1_500_000 <= r.size_bytes <= 12_000_000 else 1,
                r.size_bytes,
                r.title.lower(),
            ),
        )
        for row in bucket_rows[:per_bucket]:
            selected.append(row)
            used_sha.add(row.sha256)
            if len(selected) >= limit:
                return selected

    fallback = sorted(
        [r for r in eligible if r.sha256 not in used_sha],
        key=lambda r: (
            THEME_ORDER.index(r.theme_bucket) if r.theme_bucket in THEME_ORDER else 99,
            0 if 1_500_000 <= r.size_bytes <= 12_000_000 else 1,
            r.size_bytes,
            r.title.lower(),
        ),
    )
    for row in fallback:
        selected.append(row)
        used_sha.add(row.sha256)
        if len(selected) >= limit:
            break
    return selected


def rows_by_id(rows: Iterable[PaperRow]) -> dict[str, PaperRow]:
    return {r.openreview_forum_id: r for r in rows}


def write_jsonl(rows: list[PaperRow], batch_id: int, out_dir: Path) -> Path:
    path = out_dir / f"batch_{batch_id:04d}_pdfs.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps({
                "batch_id": f"iclr26_{batch_id:04d}",
                "title": row.title,
                "openreview_forum_id": row.openreview_forum_id,
                "sha256": row.sha256,
                "size_bytes": row.size_bytes,
                "path": row.path,
                "source": row.source,
                "manifest_paper_id": row.manifest_paper_id,
                "theme_bucket": row.theme_bucket,
                "conf_year": "ICLR_2026",
            }, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def write_contract(rows: list[PaperRow], batch_id: int, manifest_path: Path, contract_dir: Path) -> Path:
    path = contract_dir / f"batch_{batch_id:04d}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# ICLR 2026 Batch {batch_id:04d} Contract",
        "",
        f"- batch_id: `iclr26_{batch_id:04d}`",
        f"- generated_at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- source_manifest: `{_rel(DEFAULT_DISCOVERY)}`",
        f"- batch_pdf_manifest: `{_rel(manifest_path)}`",
        "- selection_rule: verified ICLR_2026 PDFs with OpenReview id, excluding canary papers and earlier planned batches, theme-bucket interleaving, 25 papers",
        f"- selected_count: `{len(rows)}`",
        f"- raw_artifact_target: `{_rel(DEFAULT_RAW_OUTPUT_ROOT / f'iclr26_{batch_id:04d}')}`",
        "- db_index_target: optional current L2 `paper_analyses` rows and `paper_figures`; not the raw artifact store",
        "- primary_preprocess_command: `researchflow-backend/scripts/run_iclr26_mineru_raw_batch.py`",
        "- L2_policy: MinerU-only; `model_name=mineru_only`, `parsers_used=['mineru']`, `formula_source=mineru`",
        "- forbidden_in_preprocess: DeepSeek/OpenAI analysis agents, writer agent, L4/report/export, batch analysis runner",
        "- review_policy: preprocessing agent writes progress/summary and stops",
        "",
        "## Selected Papers",
        "",
        "| # | Theme | Title | OpenReview | SHA256 | Size | PDF path |",
        "|---|-------|-------|------------|--------|------|----------|",
    ]
    for i, row in enumerate(rows, 1):
        link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
        lines.append(
            f"| {i} | {row.theme_bucket} | {row.title.replace('|', '/')} | "
            f"[{row.openreview_forum_id}]({link}) | `{row.sha256}` | {row.size_bytes} | `{row.path}` |"
        )
    lines += [
        "",
        "## MinerU Raw Artifact Gate",
        "",
        "- per-paper raw output directory exists under the declared `raw_artifact_target`.",
        "- directory contains at least one `.md` file.",
        "- directory contains `*content_list_v2.json` or `*content_list.json`.",
        "- logs are preserved as `mineru_stdout.log` and `mineru_stderr.log`.",
        "- optional DB index, if run later, must remain MinerU-only.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_prompt(batch_ids: list[int], prompt_dir: Path) -> Path:
    path = prompt_dir / "iclr26_mineru_preprocess_handoff_prompt.md"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ICLR 2026 MinerU Raw Artifact Handoff Prompt",
        "",
        "你正在接力 ResearchFlow 的 ICLR 2026 PDF 预处理任务。目标是运行 MinerU CLI 并保存原始产物；不要把 PostgreSQL 当成 MinerU 原始产物存储。",
        "",
        "## Hard Constraints",
        "",
        "- 原始 MinerU 产物写入 `_private/iclr26_batch/mineru_outputs/<batch_id>/<openreview_forum_id>/`。",
        "- PostgreSQL 只允许作为后续可选索引/状态层；它不是 `.md`、`content_list.json`、布局 PDF、图片等原始产物的存储位置。",
        "- `paperAnalysis/`、`paperCollection/`、`obsidian-vault/` 是导出视角，不要写它们。",
        "- 只能运行 `researchflow-backend/scripts/run_iclr26_mineru_raw_batch.py` 做本任务。",
        "- 不要运行 `researchflow-backend/scripts/preprocess_iclr26_mineru_batch.py`，除非人工明确要求追加 DB L2 索引。",
        "- 禁止运行 `researchflow-backend/scripts/run_iclr26_batch.py`。",
        "- 禁止运行 `IngestWorkflow.run_for_existing_paper()`、analysis_agent、writer_agent、export_vault。",
        "- 如果后续人工要求 DB L2 索引，L2 必须是 MinerU-only：`model_name=mineru_only`、`parsers_used=['mineru']`、`formula_source=mineru`。",
        "- `ALLOW_LLM_IMAGE_UPLOAD=false`。",
        "- 每个 agent 只处理分配给自己的一个 batch，避免并发写同一批 paper。",
        "",
        "## Common Command Template",
        "",
        "```bash",
        "cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend",
        "",
        "ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \\",
        "conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py \\",
        "  --batch-manifest ../_private/iclr26_batch/manifests/batch_000X_pdfs.jsonl \\",
        "  --batch-id iclr26_000X \\",
        "  --output-root ../_private/iclr26_batch/mineru_outputs \\",
        "  --resume",
        "```",
        "",
        "将 `000X` 替换为你的 batch 编号。",
        "",
        "## Batch Assignments",
        "",
    ]
    for batch_id in batch_ids:
        lines += [
            f"### batch_{batch_id:04d}",
            "",
            f"- contract: `_private/iclr26_batch/contracts/batch_{batch_id:04d}.md`",
            f"- manifest: `_private/iclr26_batch/manifests/batch_{batch_id:04d}_pdfs.jsonl`",
            f"- raw artifact output: `_private/iclr26_batch/mineru_outputs/iclr26_{batch_id:04d}/`",
            f"- progress output: `_private/iclr26_batch/reports/mineru_raw_batch_{batch_id:04d}_progress.jsonl`",
            f"- summary output: `_private/iclr26_batch/reports/mineru_raw_batch_{batch_id:04d}_summary.json`",
            "",
            "Command:",
            "",
            "```bash",
            "cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend",
            "",
            "ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \\",
            f"conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py --batch-manifest ../_private/iclr26_batch/manifests/batch_{batch_id:04d}_pdfs.jsonl --batch-id iclr26_{batch_id:04d} --output-root ../_private/iclr26_batch/mineru_outputs --resume",
            "```",
            "",
        ]
    lines += [
        "## Success Criteria",
        "",
        "- summary JSON has `failed_count = 0` or every failure is explicitly listed with reason.",
        "- each successful paper has raw MinerU artifacts under `_private/iclr26_batch/mineru_outputs/<batch_id>/<openreview_forum_id>/`.",
        "- each successful paper has at least one `.md` and one `*content_list*.json` in that raw output directory.",
        "- no `run_iclr26_batch.py` process was started.",
        "- no L4/report/export was generated by this preprocessing task.",
        "",
        "If a PDF cannot produce valid raw MinerU artifacts after one retry, leave it in the summary as failed and stop that paper; do not use PyMuPDF fallback.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--discovery-manifest", default=str(DEFAULT_DISCOVERY))
    parser.add_argument("--contract-dir", default=str(DEFAULT_CONTRACT_DIR))
    parser.add_argument("--manifest-dir", default=str(DEFAULT_MANIFEST_DIR))
    parser.add_argument("--prompt-dir", default=str(DEFAULT_PROMPT_DIR))
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--batch-count", type=int, default=4)
    args = parser.parse_args()

    discovery = Path(args.discovery_manifest)
    contract_dir = Path(args.contract_dir)
    manifest_dir = Path(args.manifest_dir)
    prompt_dir = Path(args.prompt_dir)

    rows = read_discovery(discovery)
    by_forum_id = rows_by_id(rows)
    used_ids: set[str] = set()
    planned: dict[int, list[PaperRow]] = {}

    batch1_contract = contract_dir / "batch_0001.md"
    existing_batch1_ids = contract_ids(batch1_contract)
    if existing_batch1_ids:
        missing = [fid for fid in existing_batch1_ids if fid not in by_forum_id]
        if missing:
            raise SystemExit(f"Existing batch_0001 contract references ids missing from discovery manifest: {missing}")
        planned[1] = [by_forum_id[fid] for fid in existing_batch1_ids]
        used_ids.update(existing_batch1_ids)

    for batch_id in range(1, args.batch_count + 1):
        if batch_id not in planned:
            selected = select_next_batch(rows, used_ids, args.batch_size)
            if len(selected) != args.batch_size:
                raise SystemExit(f"Only selected {len(selected)} rows for batch_{batch_id:04d}")
            planned[batch_id] = selected
            used_ids.update(r.openreview_forum_id for r in selected)

    manifest_paths = {}
    contract_paths = {}
    for batch_id in range(1, args.batch_count + 1):
        manifest_paths[batch_id] = write_jsonl(planned[batch_id], batch_id, manifest_dir)
        contract_paths[batch_id] = write_contract(planned[batch_id], batch_id, manifest_paths[batch_id], contract_dir)

    prompt_path = write_prompt(list(range(1, args.batch_count + 1)), prompt_dir)
    print(json.dumps({
        "batch_count": args.batch_count,
        "batch_size": args.batch_size,
        "contracts": {f"batch_{k:04d}": _rel(v) for k, v in contract_paths.items()},
        "manifests": {f"batch_{k:04d}": _rel(v) for k, v in manifest_paths.items()},
        "prompt": _rel(prompt_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

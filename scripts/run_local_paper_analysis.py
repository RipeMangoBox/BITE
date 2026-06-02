"""Run a local, file-backed paper analysis pipeline.

This runner intentionally does not import the database layer and does not write
PostgreSQL. A single paper is processed into a self-contained work directory:

    .state
    manifest.json
    parse/full.md
    parse/chunks/part_*.md
    parse/figures_tables.json
    part_analysis/part_*.json
    analysis/main_analysis.json
    report/final_report.md
    report/vault_export.json

Inputs can be a PDF, an existing MinerU output directory, or a markdown file.
The markdown option is mainly for tests and recovery work.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import ssl
import subprocess
import sys
import time
import traceback
import uuid
from typing import Any

import certifi
import httpx

try:
    import fitz
except ImportError:  # pragma: no cover - optional dependency
    fitz = None


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.researchflow_local.topic_tags import (
    format_topic_tags,
    topic_tags_from_assignment,
)
from scripts.researchflow_local.venue_slug import normalize_conf_year_slug

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_private" / "local_analysis_runs"
DEFAULT_MINERU_LOCK = REPO_ROOT / "_private" / "local_analysis_runs" / "locks" / "mineru_parse.lock"
DEFAULT_ENV_FILE = REPO_ROOT / ".env"
PRIVATE_ENV_FILE = REPO_ROOT / "_private" / "local_analysis" / ".env"
DEFAULT_VAULT_ROOT = REPO_ROOT / "obsidian-vault"
DEFAULT_ASSET_ROOT = DEFAULT_VAULT_ROOT / "assets" / "figures" / "papers"
DEFAULT_MINERU_BIN = shutil.which("mineru") or "mineru"
DEFAULT_MINERU_CONFIG = REPO_ROOT / "_private" / "mineru_local" / "mineru.json"
DEFAULT_MINERU_HF_CACHE = Path.home() / ".cache" / "huggingface" / "hub"
MINERU_PIPELINE_CACHE = DEFAULT_MINERU_HF_CACHE / "models--opendatalab--PDF-Extract-Kit-1.0"
DEFAULT_MINERU_CONTENT_COORD_SIZE = (1000.0, 1000.0)
DEFAULT_CONF_YEAR = ""
DEFAULT_TOPIC_ASSIGNMENTS = os.environ.get("RF_TOPIC_ASSIGNMENTS", "").strip()
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"
KIMI_DEFAULT_BASE_URL = "https://api.moonshot.ai/v1"
KIMI_DEFAULT_TEMPERATURE = 0.6
DEFAULT_KIMI_MODEL = "kimi-k2.6"
DEFAULT_OPENAI_FIGURE_MODEL = "gpt-5.4"
SECTION_SPECS: tuple[tuple[str, str], ...] = (
    ("概述", "概括问题、核心结论、方法定位与主要结果，不要展开细节。"),
    ("背景与动机", "说明问题背景、现有方法缺口、本文动机。"),
    ("核心创新", "聚焦相对 baseline 的关键创新与 changed slots。"),
    ("整体框架", "描述整体 pipeline、模块关系、输入输出流。"),
    ("核心模块与公式推导", "只写关键模块、关键公式、公式变量含义，禁止猜公式。"),
    ("实验与分析", "写主结果、消融、失败模式、重要图表结论。"),
    (
        "方法谱系与知识库定位",
        "写与 baseline/follow-up 的关系、适用边界、局限与开放问题；若提到具体基线工作，保留或补充论文中可验证的作者、会议和年份，例如 **MPGD** (He et al., CVPR 2023)。",
    ),
)

DISCOUNTED_PRICES_PER_MTOKEN_USD: dict[str, dict[str, float]] = {
    "deepseek-v4-pro": {"input": 0.435, "input_cache_hit": 0.003625, "output": 0.87},
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.14, "output": 0.28},
}

THINKING_CHOICES = ("enabled", "disabled")


@dataclass(frozen=True)
class LLMCallResult:
    text: str
    usage: dict[str, Any]
    diagnostics: dict[str, Any] | None = None


def estimate_tokens(text: str) -> int:
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    other = max(0, len(text) - cjk)
    return int(round(cjk * 0.6 + other * 0.3))


def estimate_cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float | None:
    price = DISCOUNTED_PRICES_PER_MTOKEN_USD.get(model)
    if not price:
        return None
    return round(
        prompt_tokens * (price["input"] / 1_000_000)
        + completion_tokens * (price["output"] / 1_000_000),
        6,
    )


def estimate_cost_usd_from_usage(model: str, usage: dict[str, Any]) -> float | None:
    price = DISCOUNTED_PRICES_PER_MTOKEN_USD.get(model)
    if not price:
        return None
    prompt_tokens = int(usage.get("prompt_tokens") or usage.get("prompt_tokens_est") or 0)
    completion_tokens = int(usage.get("completion_tokens") or usage.get("completion_tokens_est") or 0)
    cache_hit = int(usage.get("prompt_cache_hit_tokens") or 0)
    cache_miss = int(usage.get("prompt_cache_miss_tokens") or 0)
    if cache_hit or cache_miss:
        if not cache_miss:
            cache_miss = max(0, prompt_tokens - cache_hit)
        input_cost = (
            cache_hit * (price.get("input_cache_hit", price["input"]) / 1_000_000)
            + cache_miss * (price["input"] / 1_000_000)
        )
    else:
        input_cost = prompt_tokens * (price["input"] / 1_000_000)
    return round(
        input_cost + completion_tokens * (price["output"] / 1_000_000),
        6,
    )


def usage_to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    return {}


def normalized_api_usage(value: Any) -> dict[str, Any]:
    raw = usage_to_dict(value)
    if not raw:
        return {}
    prompt_details = usage_to_dict(raw.get("prompt_tokens_details"))
    completion_details = usage_to_dict(raw.get("completion_tokens_details"))
    prompt_tokens = int(raw.get("prompt_tokens") or 0)
    cached_tokens = int(prompt_details.get("cached_tokens") or 0)
    reasoning_tokens = int(completion_details.get("reasoning_tokens") or 0)
    cache_hit = int(raw.get("prompt_cache_hit_tokens") or cached_tokens or 0)
    cache_miss = int(raw.get("prompt_cache_miss_tokens") or 0)
    if cache_hit and not cache_miss:
        cache_miss = max(0, prompt_tokens - cache_hit)
    return {
        "prompt_tokens_api": prompt_tokens,
        "completion_tokens_api": int(raw.get("completion_tokens") or 0),
        "total_tokens_api": int(raw.get("total_tokens") or 0),
        "reasoning_tokens_api": reasoning_tokens,
        "prompt_cache_hit_tokens": cache_hit,
        "prompt_cache_miss_tokens": cache_miss,
        "cached_tokens_api": cached_tokens,
        "api_usage_raw": raw,
    }


def merge_usage_totals(base: dict[str, Any], extra: dict[str, Any], *, cost_basis: str) -> dict[str, Any]:
    merged = dict(base)
    for key in [
        "prompt_tokens_est",
        "completion_tokens_est",
        "reasoning_tokens_est",
        "total_tokens_est",
        "total_with_reasoning_tokens_est",
        "prompt_tokens_api",
        "completion_tokens_api",
        "reasoning_tokens_api",
        "total_tokens_api",
        "prompt_cache_hit_tokens",
        "prompt_cache_miss_tokens",
        "cached_tokens_api",
    ]:
        merged[key] = int(base.get(key) or 0) + int(extra.get(key) or 0)
    merged["estimated_cost_usd"] = round(
        float(base.get("estimated_cost_usd") or 0.0)
        + float(extra.get("estimated_cost_usd") or 0.0),
        6,
    )
    if base.get("estimated_cost_usd_api") is not None or extra.get("estimated_cost_usd_api") is not None:
        merged["estimated_cost_usd_api"] = round(
            float(base.get("estimated_cost_usd_api") or 0.0)
            + float(extra.get("estimated_cost_usd_api") or 0.0),
            6,
        )
    merged["cost_basis"] = cost_basis
    return merged


def cache_hit_rate(hit_tokens: int, miss_tokens: int) -> float | None:
    total = hit_tokens + miss_tokens
    if total <= 0:
        return None
    return round(hit_tokens / total, 6)


def usage_from_result(result: LLMCallResult) -> dict[str, Any]:
    usage = dict(result.usage)
    if result.diagnostics:
        usage["stream_diagnostics"] = result.diagnostics
    return usage


def usage_finish_reasons(usage: dict[str, Any]) -> list[str]:
    diagnostics = usage.get("stream_diagnostics") or {}
    reasons = diagnostics.get("finish_reasons") or []
    if not isinstance(reasons, list):
        reasons = [reasons]
    if diagnostics.get("finish_reason"):
        reasons.append(diagnostics["finish_reason"])
    return [str(reason) for reason in reasons if str(reason)]


def usage_has_finish_reason(usage: dict[str, Any], reason: str) -> bool:
    return reason in usage_finish_reasons(usage)

PART_ANALYSIS_SYSTEM = """Extract anchors from ONE paper chunk. Do not summarize the paper.

Copy short, directly visible anchors only. Use exact section, formula, figure,
and table labels when visible. Do not infer from missing sections.

Return JSON only:
{
  "part_id": str,
  "section_role": str,
  "method_evidence": [{"claim": str, "section": str, "anchor": str, "confidence": float}],
  "experiment_evidence": [{"claim": str, "table_or_figure": str, "metric": str, "value": str, "confidence": float}],
  "formula_evidence": [{"name": str, "latex": str, "meaning": str, "section": str, "confidence": float}],
  "figure_table_roles": [{"label": str, "role_hint": str, "caption": str, "confidence": float}],
  "open_questions": [str]
}

Rules:
1. Keep each evidence list at 5 items or fewer.
2. Prefer copied anchors over explanation.
3. If the chunk has visible headings, formulas, figures, tables, or result
   sentences, do not return an all-empty evidence object.
4. Use [] only when that evidence type is absent.
5. Output no markdown fences, no prose, no reference list."""

PART_ANALYSIS_PROMPT_CONTRACT = """Fixed task contract for prompt-cache reuse.

Task: extract grounded anchors from one chunk of one paper. The variable paper
title, chunk id, character span, and chunk text appear after this fixed contract.

Return JSON only:
{
  "part_id": str,
  "section_role": str,
  "method_evidence": [{"claim": str, "section": str, "anchor": str, "confidence": float}],
  "experiment_evidence": [{"claim": str, "table_or_figure": str, "metric": str, "value": str, "confidence": float}],
  "formula_evidence": [{"name": str, "latex": str, "meaning": str, "section": str, "confidence": float}],
  "figure_table_roles": [{"label": str, "role_hint": str, "caption": str, "confidence": float}],
  "open_questions": [str]
}

Rules:
1. Keep each evidence list at 5 items or fewer.
2. Prefer copied anchors over explanation.
3. If the chunk has visible headings, formulas, figures, tables, or result
   sentences, do not return an all-empty evidence object.
4. Use [] only when that evidence type is absent.
5. Output no markdown fences, no prose, no reference list."""

MAIN_ANALYSIS_SYSTEM = """You are ResearchFlow's local main analysis agent.

Merge the part-analysis JSON files with the compact paper context. Produce a
verified analysis object for local file output. 正文/分析内容必须使用简体中文：
translate generated explanatory fields into Chinese, while preserving original
caption text, formulas, symbols, code identifiers, exact evidence anchors, and
method, dataset, metric, paper names.

Return exactly one valid JSON object:
{
  "paper_metadata": {"title": str, "title_zh": str, "venue": str | null, "year": int | null},
  "analysis_truth": {
    "real_bottleneck": str,
    "causal_knob": str,
    "core_insight": str,
    "decisive_evidence": [{"claim": str, "anchor": str, "confidence": float}]
  },
  "method": {
    "proposed_method_name": str,
    "baseline_methods": [{"name": str, "role": str, "citation": str | null}],
    "changed_slots": [{"slot_name": str, "baseline_value": str, "proposed_value": str, "evidence_anchor": str, "confidence": float}],
    "pipeline_modules": [{"name": str, "role": str, "evidence_anchor": str}]
  },
  "experiments": {
    "main_results": [{"benchmark": str, "metric": str, "proposed": str, "baseline": str, "delta": str, "anchor": str, "confidence": float}],
    "ablations": [{"claim": str, "anchor": str, "confidence": float}],
    "fairness_notes": [str]
  },
  "formulas": [{"name": str, "latex": str, "meaning": str, "anchor": str}],
  "figures_tables": [{"label": str, "role": str, "caption": str}],
  "limitations": [str],
  "open_questions": [str]
}

Rules:
1. Do not add unsupported claims.
2. Resolve conflicts by preferring directly anchored evidence.
3. If evidence is weak or absent, keep the field empty or use open_questions.
4. Set paper_metadata.title to the original paper title. Set
   paper_metadata.title_zh to a concise Chinese title when a faithful
   translation is possible; otherwise repeat the original title.
5. Natural-language explanations MUST be Simplified Chinese. Keep the original
   language only for caption text, formulas, symbols, code identifiers, exact
   anchors, and method, dataset, metric, paper names.
6. For each concrete baseline method, fill citation when the paper provides
   verifiable author/year/venue metadata, e.g. "He et al., CVPR 2023"; otherwise
   use null instead of guessing.
7. Output ONLY valid JSON, with no markdown fences."""

MAIN_ANALYSIS_PROMPT_CONTRACT = """Fixed merge contract for prompt-cache reuse.

Task: merge chunk-level anchors, compact paper context, and figure/table
metadata into one verified ResearchFlow analysis object. The variable paper
payload appears after this fixed contract.

正文/分析内容必须使用简体中文：translate generated explanatory fields into Chinese,
while preserving original caption text, formulas, symbols, code identifiers,
exact evidence anchors, and method, dataset, metric, paper names.

Return exactly one valid JSON object:
{
  "paper_metadata": {"title": str, "title_zh": str, "venue": str | null, "year": int | null},
  "analysis_truth": {
    "real_bottleneck": str,
    "causal_knob": str,
    "core_insight": str,
    "decisive_evidence": [{"claim": str, "anchor": str, "confidence": float}]
  },
  "method": {
    "proposed_method_name": str,
    "baseline_methods": [{"name": str, "role": str, "citation": str | null}],
    "changed_slots": [{"slot_name": str, "baseline_value": str, "proposed_value": str, "evidence_anchor": str, "confidence": float}],
    "pipeline_modules": [{"name": str, "role": str, "evidence_anchor": str}]
  },
  "experiments": {
    "main_results": [{"benchmark": str, "metric": str, "proposed": str, "baseline": str, "delta": str, "anchor": str, "confidence": float}],
    "ablations": [{"claim": str, "anchor": str, "confidence": float}],
    "fairness_notes": [str]
  },
  "formulas": [{"name": str, "latex": str, "meaning": str, "anchor": str}],
  "figures_tables": [{"label": str, "role": str, "caption": str}],
  "limitations": [str],
  "open_questions": [str]
}

Rules:
1. Do not add unsupported claims.
2. Resolve conflicts by preferring directly anchored evidence.
3. If evidence is weak or absent, keep the field empty or use open_questions.
4. Set paper_metadata.title to the original paper title. Set
   paper_metadata.title_zh to a concise Chinese title when a faithful
   translation is possible; otherwise repeat the original title.
5. Natural-language explanations MUST be Simplified Chinese. Keep the original
   language only for caption text, formulas, symbols, code identifiers, exact
   anchors, and method, dataset, metric, paper names.
6. For each concrete baseline method, fill citation when the paper provides
   verifiable author/year/venue metadata, e.g. "He et al., CVPR 2023"; otherwise
   use null instead of guessing.
7. Output ONLY valid JSON, with no markdown fences."""

WRITER_SYSTEM = """You are ResearchFlow's local writer agent.

Write the final paper report from the verified local analysis JSON, part
evidence, and figure/table metadata only. Do not invent claims. 正文内容必须使用
简体中文：translate all generated paragraphs, bullets, and table cells into
Chinese. Preserve original language only for captions, formulas, symbols, code
identifiers, URLs/citations, exact quoted evidence, and method, dataset, metric,
paper names.

Return Markdown only, with these sections:
1. 概述
2. 背景与动机
3. 核心创新
4. 整体框架
5. 核心模块与公式推导
6. 实验与分析
7. 方法谱系与知识库定位

Use exact table, figure, and equation labels when available. Do not embed
images yourself; the deterministic vault exporter will insert local MinerU
figure/table images. Use `$...$` for inline LaTeX and `$$...$$` for block
LaTeX; do not use `\\(...\\)` or `\\[...\\]`. In 方法谱系与知识库定位, when
you mention a concrete baseline work, include verified author/year/venue
metadata if supplied by the analysis or source context, e.g. **MPGD** (He et
al., CVPR 2023); omit the citation rather than guessing. Do not output JSON or
markdown fences around the whole report."""

SECTION_WRITER_SYSTEM = """You are ResearchFlow's local section writer.

Write ONLY the requested report section in Simplified Chinese from verified
analysis JSON, part evidence, and the supplied paper context. Do not invent
claims. Preserve original language only for captions, formulas, symbols, code
identifiers, exact anchors, and method, dataset, metric, paper names.

Write analytical synthesis, not a paper-like paraphrase. Compress source
details into bottlenecks, causal mechanisms, evidence strength, and failure
modes. Avoid copying long caption/body prose unless it is an exact short anchor.

Rules:
1. Output Markdown only for the requested section body. Do not include the H1 title.
2. Start with `## <section title>`.
3. Do not embed images; the assembler/exporter handles that deterministically.
4. If evidence is weak, explicitly say the point needs manual verification instead of guessing.
5. For formulas, preserve exact LaTeX if provided. Use `$...$` for inline
   formulas and `$$...$$` for block formulas; do not use `\\(...\\)` or
   `\\[...\\]`. Do not derive unseen formulas.
6. In 方法谱系与知识库定位, when you mention a concrete baseline work, include
   verified author/year/venue metadata if supplied by the analysis or source
   context, e.g. **MPGD** (He et al., CVPR 2023); omit the citation rather than
   guessing.
"""

FIGURE_PLACEMENT_SYSTEM = """You are ResearchFlow's local note image placement reviewer.

Choose which local MinerU figure/table images should be inserted into the
exported Obsidian note. Use the verified analysis, report text, and captions.
Prefer method diagrams cited by the report and summary tables or result plots
that directly support the note section.
Do not place sample-only dataset images as the framework image. If no real
framework/pipeline/method diagram exists, leave 整体框架 empty.

Return JSON only:
{
  "placements": [
    {"item_id": str, "section": "整体框架" | "核心模块与公式推导" | "实验与分析", "reason": str}
  ]
}

Rules:
1. Select at most the requested image budget.
2. Use only supplied item_id values.
3. Do not duplicate the same item_id.
4. When the report explicitly cites Figure N / Table N and the candidate
   exists, include that image unless it is sample-only or decorative.
5. Put overall pipeline/architecture diagrams in 整体框架; put tokenizer,
   masking, denoising, sampling, guidance, or other method-module diagrams in
   核心模块与公式推导.
6. Prefer Table 1 / benchmark summary tables and decisive result plots over
   decorative or example-only images."""

FIGURE_VISUAL_SUMMARY_SYSTEM = """You are ResearchFlow's local figure/table visual summarizer.

Look at the supplied paper figure/table image and caption. Return JSON only:
{
  "visual_summary": str,
  "visual_type": str,
  "is_sample_only": bool,
  "key_visible_elements": [str],
  "supports_claims": [str],
  "placement_hint": "整体框架" | "实验与分析" | "skip",
  "confidence": float
}

Keep the summary short and grounded in visible content. If the image is just
dataset examples or decorative samples, set is_sample_only=true and
placement_hint=\"skip\" unless it is explicitly needed for an experiment."""

KIMI_NOTE_CHECK_REPAIR_SYSTEM = """You are ResearchFlow's final note quality checker.

Check and lightly repair an Obsidian paper note for:
1. Markdown/frontmatter formatting
2. duplicated figure/table captions
3. figure/table placement mismatch
4. broken JSON-like or malformed table text
5. LaTeX delimiter style: inline math must use `$...$`, display math must use
   `$$...$$`, and `\\(...\\)` / `\\[...\\]` must not remain
6. Image embeds must use Obsidian wikilinks like `![[assets/...]]`, never
   Markdown image links or `../../assets/...` prefixes
7. ResearchFlow frontmatter schema: keep `aliases` as short English/model
   aliases; do not add `category`, `modalities`, or `frontier`

Do not rewrite analytical claims, do not add new claims, and do not make the
style more paper-like. Preserve the DeepSeek analysis content unless a local
format or image-caption mismatch is obvious from the supplied placement data.

Return Markdown only."""

PART_ANALYSIS_REPAIR_SYSTEM = """Repair a malformed part-analysis response into JSON.

You will receive:
1. the required JSON schema description
2. the raw model output
3. a source chunk excerpt

Return JSON only. If the raw output has no usable JSON, extract a few directly
visible anchors from the source excerpt. Do not return an all-empty object when
the excerpt contains headings, formulas, figures, tables, or result sentences.
"""

MAIN_ANALYSIS_REPAIR_SYSTEM = """Repair a malformed ResearchFlow main-analysis response into JSON.

Return JSON only. Preserve any supported fields from the raw output. If the raw
output is missing late fields because it was truncated, keep the complete
earlier fields and use empty arrays for missing list fields. Do not invent new
claims.
"""


@dataclass(frozen=True)
class Chunk:
    index: int
    total: int
    start: int
    end: int
    text: str


@dataclass(frozen=True)
class MinerUArtifacts:
    markdown_path: Path
    content_list_path: Path | None
    root: Path


@dataclass(frozen=True)
class MinerUSidecarArtifacts:
    origin_pdf_path: Path | None
    middle_json_path: Path | None
    model_json_path: Path | None


class RunLock:
    def __init__(self, path: Path):
        self.path = path
        self.fd: int | None = None

    def __enter__(self) -> "RunLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._clear_stale_lock()
        try:
            self.fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise SystemExit(f"Another local analysis run owns {self.path}") from exc
        payload = {
            "pid": os.getpid(),
            "created_at": now_iso(),
        }
        os.write(self.fd, json.dumps(payload).encode("utf-8"))
        os.close(self.fd)
        self.fd = None
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is not None:
            os.close(self.fd)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass

    def _clear_stale_lock(self) -> None:
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            pid = int(payload.get("pid") or 0)
        except (OSError, ValueError, json.JSONDecodeError, TypeError):
            return
        if pid <= 0:
            return
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            self.path.unlink(missing_ok=True)
        except PermissionError:
            return


class BlockingFileLock:
    def __init__(self, path: Path):
        self.path = path
        self.fd: int | None = None

    def __enter__(self) -> "BlockingFileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(self.path), os.O_CREAT | os.O_RDWR)
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        os.ftruncate(self.fd, 0)
        os.write(self.fd, json.dumps({"pid": os.getpid(), "created_at": now_iso()}).encode("utf-8"))
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is None:
            return
        try:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
        finally:
            os.close(self.fd)
            self.fd = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def safe_slug(value: str, *, max_len: int = 80) -> str:
    value = re.sub(r"[^\w\s.-]+", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "_", value.strip())
    value = value.strip("._")
    return (value or "paper")[:max_len]


def note_file_stem(title: str) -> str:
    return safe_slug(title.replace(":", " "), max_len=160)


def yaml_scalar(value: Any) -> str:
    text = str(value or "")
    if not text:
        return '""'
    if re.search(r"[:#\n\r\[\]{}]|^\s|\s$|^[*&!%@`>|]", text):
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return text


def infer_conf_parts(conf_year: str) -> tuple[str, int | None]:
    match = re.match(r"(.+?)_(\d{4})$", conf_year or "")
    if not match:
        return conf_year or "Unknown", None
    venue = match.group(1).replace("_", " ")
    if venue.lower() == "arxiv":
        venue = "arXiv"
    return venue, int(match.group(2))


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.tmp.{os.getpid()}.{uuid.uuid4().hex}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n")


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, ensure_ascii=False, default=str) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        os.write(fd, payload)
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            pass
        os.close(fd)


def build_async_openai_client(client_cls: Any, **client_kwargs: Any) -> tuple[Any, httpx.AsyncClient]:
    cert_path = Path(certifi.where())
    verify = str(cert_path) if cert_path.exists() else ssl.create_default_context()
    http_client = httpx.AsyncClient(verify=verify, trust_env=False)
    client_kwargs["http_client"] = http_client
    return client_cls(**client_kwargs), http_client


def load_env_file(path: Path) -> None:
    if path == DEFAULT_ENV_FILE and not path.exists() and PRIVATE_ENV_FILE.exists():
        path = PRIVATE_ENV_FILE
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def file_sha12(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()[:12]


def default_task_id(args: argparse.Namespace) -> str:
    source = Path(args.source_md or args.pdf or args.mineru_output)
    suffix = file_sha12(source) if source.is_file() else hashlib.sha256(str(source).encode()).hexdigest()[:12]
    return f"{safe_slug(source.stem)}_{suffix}"


def infer_conf_year_from_pdf_path(pdf_path: str) -> str:
    if not pdf_path:
        return ""
    for part in reversed(Path(pdf_path).parts):
        if re.match(r"^[A-Za-z][A-Za-z0-9-]*_\d{4}$", part):
            return normalize_conf_year_slug(part)
    return ""


def pdf_search_roots_from_env() -> list[Path]:
    raw = os.environ.get("RF_PDF_SEARCH_ROOTS", "").strip()
    if not raw:
        return []
    return [
        Path(item).expanduser()
        for item in raw.split(os.pathsep)
        if item.strip()
    ]


def pdf_search_roots_from_args(args: argparse.Namespace) -> list[Path]:
    roots = getattr(args, "pdf_search_root", []) or []
    return [Path(item).expanduser() for item in roots if str(item).strip()]


def resolve_existing_pdf_path(
    path_value: str,
    *,
    conf_year: str = "",
    search_roots: list[Path] | None = None,
) -> tuple[Path | None, dict[str, Any]]:
    raw = str(path_value or "").strip()
    attempts: list[str] = []
    if not raw:
        return None, {"input": raw, "attempts": attempts}

    path = Path(raw).expanduser()
    candidates: list[Path] = []
    if path.is_absolute():
        candidates.append(path)
    else:
        candidates.extend([Path.cwd() / path, REPO_ROOT / path])

    filename = path.name
    configured_roots = list(search_roots or []) + pdf_search_roots_from_env()
    configured_roots.append(REPO_ROOT / "obsidian-vault" / "paperPDFs")
    if filename:
        for root in configured_roots:
            if conf_year:
                candidates.append(root / conf_year / filename)
            if root.exists():
                candidates.extend(root.rglob(filename))

    seen: set[str] = set()
    unique_candidates: list[Path] = []
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            unique_candidates.append(candidate)

    for candidate in unique_candidates:
        attempts.append(str(candidate))
        if candidate.is_file():
            return candidate.resolve(), {
                "input": raw,
                "resolved": str(candidate.resolve()),
                "attempts": attempts,
            }
    return None, {"input": raw, "attempts": attempts}


def resolved_conf_year(args: argparse.Namespace) -> str:
    conf_year = (args.conf_year or "").strip()
    if conf_year:
        return normalize_conf_year_slug(conf_year)
    inferred = infer_conf_year_from_pdf_path(args.paper_pdf or args.pdf or "")
    if inferred:
        return inferred
    if args.export_vault:
        raise ValueError("Pass --conf-year for vault export when it cannot be inferred from the PDF path")
    return "Unknown"


def parse_json_object(text: str, *, label: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        cleaned = cleaned[first_newline + 1:] if first_newline != -1 else cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].rstrip()
    candidates = balanced_json_candidates(cleaned)
    if not candidates and cleaned:
        candidates = [cleaned]

    last_error: json.JSONDecodeError | None = None
    best: dict[str, Any] | None = None
    best_score = -1
    for obj_text in candidates:
        latex_protected = protect_latex_escapes(obj_text)
        for candidate in (
            latex_protected,
            obj_text,
            fix_invalid_escapes(latex_protected),
            fix_invalid_escapes(obj_text),
            repair_common_json_issues(latex_protected),
            repair_common_json_issues(obj_text),
            close_truncated_json(latex_protected),
            close_truncated_json(obj_text),
        ):
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    score = json_object_schema_score(parsed)
                    if score > best_score:
                        best = parsed
                        best_score = score
            except json.JSONDecodeError as exc:
                last_error = exc
                continue

    if best is not None:
        return best

    if last_error is not None:
        raise ValueError(f"{label} returned invalid JSON: {last_error}") from last_error
    raise ValueError(f"{label} returned no JSON object")


def json_object_schema_score(value: dict[str, Any]) -> int:
    key_set = set(value)
    score = len(key_set)
    for group in (
        {"paper_metadata", "analysis_truth", "method", "experiments"},
        {"part_id", "section_role", "method_evidence", "experiment_evidence"},
        {"placements"},
    ):
        score += 20 * len(key_set & group)
        if group <= key_set:
            score += 100
    for nested_key in ("formulas", "figures_tables", "limitations", "open_questions", "formula_evidence", "figure_table_roles"):
        if nested_key in key_set:
            score += 5
    return score


def part_schema() -> dict[str, Any]:
    return {
        "part_id": "str",
        "section_role": "str",
        "method_evidence": [{"claim": "str", "section": "str", "anchor": "str", "confidence": "float"}],
        "experiment_evidence": [{"claim": "str", "table_or_figure": "str", "metric": "str", "value": "str", "confidence": "float"}],
        "formula_evidence": [{"name": "str", "latex": "str", "meaning": "str", "section": "str", "confidence": "float"}],
        "figure_table_roles": [{"label": "str", "role_hint": "str", "caption": "str", "confidence": "float"}],
        "open_questions": ["str"],
    }


def normalize_part_analysis(part_id: str, parsed: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "part_id": part_id,
        "section_role": str(parsed.get("section_role") or ""),
    }
    for key in ["method_evidence", "experiment_evidence", "formula_evidence", "figure_table_roles", "open_questions"]:
        value = parsed.get(key)
        normalized[key] = value if isinstance(value, list) else []
    return normalized


def part_analysis_has_content(parsed: dict[str, Any]) -> bool:
    if str(parsed.get("section_role") or "").strip():
        return True
    return any(
        parsed.get(key)
        for key in ["method_evidence", "experiment_evidence", "formula_evidence", "figure_table_roles", "open_questions"]
    )


def chunk_section_role(text: str) -> str:
    headings = [
        line.strip("# ").strip()
        for line in text.splitlines()
        if re.match(r"^#{1,4}\s+\S", line.strip())
    ]
    if headings:
        return "; ".join(headings[:4])
    return "chunk_without_visible_heading"


def sentence_snippets(text: str, pattern: str, *, max_items: int = 3, max_len: int = 240) -> list[str]:
    normalized = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", normalized)
    out: list[str] = []
    for sentence in sentences:
        if re.search(pattern, sentence, flags=re.IGNORECASE):
            out.append(compact_text(sentence, max_len=max_len))
        if len(out) >= max_items:
            break
    return out


def figure_caption_entries(chunk_text: str, *, max_items: int = 5) -> list[dict[str, Any]]:
    entries = []
    for match in re.finditer(r"\b(Figure|Table)\s+([0-9]+[A-Za-z]?)\s*:\s*([^\n]+)", chunk_text, flags=re.IGNORECASE):
        kind = "Table" if match.group(1).lower().startswith("table") else "Figure"
        label = f"{kind} {match.group(2)}"
        caption = compact_text(match.group(3), max_len=300)
        entries.append({
            "label": label,
            "role_hint": "visible chunk figure/table caption",
            "caption": caption,
            "confidence": 0.4,
        })
        if len(entries) >= max_items:
            break
    return entries


def formula_entries(chunk_text: str, *, max_items: int = 3) -> list[dict[str, Any]]:
    formulas = []
    for index, match in enumerate(re.finditer(r"\$\$(.+?)\$\$|\$([^$\n]{5,200})\$", chunk_text, flags=re.DOTALL), 1):
        latex = re.sub(r"\s+", " ", match.group(1) or match.group(2) or "").strip()
        if not latex:
            continue
        formulas.append({
            "name": f"visible_formula_{index}",
            "latex": latex,
            "meaning": "",
            "section": chunk_section_role(chunk_text),
            "confidence": 0.35,
        })
        if len(formulas) >= max_items:
            break
    return formulas


def is_appendix_figure_table_chunk(chunk_text: str) -> bool:
    headings = chunk_section_role(chunk_text).lower()
    caption_count = len(re.findall(r"\b(?:Figure|Table)\s+[0-9]+[A-Za-z]?\s*:", chunk_text, flags=re.IGNORECASE))
    image_count = chunk_text.count("![](")
    return ("appendix" in headings or re.search(r"\bb\.\d+", headings)) and caption_count >= 4 and image_count >= 4


def local_anchor_part_analysis(part_id: str, chunk_text: str) -> dict[str, Any]:
    figures = figure_caption_entries(chunk_text, max_items=5)
    return {
        "part_id": part_id,
        "section_role": chunk_section_role(chunk_text),
        "method_evidence": [
            {
                "claim": snippet,
                "section": chunk_section_role(chunk_text),
                "anchor": snippet,
                "confidence": 0.45,
            }
            for snippet in sentence_snippets(
                chunk_text,
                r"\b(method|algorithm|dataset|manifold|transform|estimate|LID|ESS|LIDL|NB|FLIPD|IDR|MS|ranked)\b",
                max_items=3,
            )
        ],
        "experiment_evidence": [
            {
                "claim": item["caption"],
                "table_or_figure": item["label"],
                "metric": "",
                "value": "",
                "confidence": 0.45,
            }
            for item in figures
        ],
        "formula_evidence": formula_entries(chunk_text, max_items=3),
        "figure_table_roles": figures,
        "open_questions": [],
    }


def fallback_part_analysis_from_chunk(part_id: str, chunk_text: str, raw_text: str, error: str) -> dict[str, Any]:
    method_terms = r"\b(method|algorithm|dataset|manifold|transform|estimate|LID|ESS|LIDL|NB|FLIPD|IDR|MS)\b"
    experiment_terms = r"\b(result|results|Table|Figure|MAE|estimate|performance|ranked|error|variance|baseline)\b"
    method_evidence = [
        {
            "claim": snippet,
            "section": chunk_section_role(chunk_text),
            "anchor": snippet,
            "confidence": 0.35,
        }
        for snippet in sentence_snippets(chunk_text, method_terms, max_items=3)
    ]
    experiment_evidence = [
        {
            "claim": snippet,
            "table_or_figure": "",
            "metric": "",
            "value": "",
            "confidence": 0.35,
        }
        for snippet in sentence_snippets(chunk_text, experiment_terms, max_items=3)
    ]

    raw_snippet = compact_text(raw_text, max_len=300)
    return {
        "part_id": part_id,
        "section_role": chunk_section_role(chunk_text),
        "method_evidence": method_evidence,
        "experiment_evidence": experiment_evidence,
        "formula_evidence": formula_entries(chunk_text, max_items=3),
        "figure_table_roles": figure_caption_entries(chunk_text, max_items=5),
        "open_questions": [
            f"{part_id} LLM 输出未能形成可用 part JSON，已从 chunk 文本保底抽取锚点。",
            f"解析/质量问题: {error}",
            f"原始输出片段: {raw_snippet}",
        ],
    }


def part_analysis_fallback(part_id: str, raw_text: str, error: str, chunk_text: str = "") -> dict[str, Any]:
    if chunk_text:
        return fallback_part_analysis_from_chunk(part_id, chunk_text, raw_text, error)
    snippet = compact_text(raw_text, max_len=400)
    return {
        "part_id": part_id,
        "section_role": "fallback_unparsed_chunk",
        "method_evidence": [],
        "experiment_evidence": [],
        "formula_evidence": [],
        "figure_table_roles": [],
        "open_questions": [
            f"{part_id} 原始输出未能解析为结构化 JSON，需要人工复核。",
            f"解析错误: {error}",
            f"原始输出片段: {snippet}",
        ],
    }


def part_repair_prompt(part_id: str, raw_text: str, chunk_text: str) -> str:
    payload = {
        "part_id": part_id,
        "schema": part_schema(),
        "raw_output": raw_text,
        "source_excerpt": compact_text(chunk_text, max_len=7000),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def repair_attempt_summary(provider: str, usage: dict[str, Any] | None = None, error: Exception | None = None) -> dict[str, Any]:
    summary: dict[str, Any] = {"provider": provider}
    if usage:
        summary["stream_diagnostics"] = usage.get("stream_diagnostics") or {}
    if error is not None:
        summary["error"] = compact_text(str(error), max_len=300)
    return summary


async def repair_part_with_kimi(
    args: argparse.Namespace,
    *,
    part_id: str,
    raw_text: str,
    chunk_text: str,
    max_tokens: int,
) -> LLMCallResult:
    return await kimi_llm_text(
        args,
        system=PART_ANALYSIS_REPAIR_SYSTEM,
        prompt=part_repair_prompt(part_id, raw_text, chunk_text),
        max_tokens=max_tokens,
    )


def main_repair_prompt(raw_text: str) -> str:
    schema = {
        "paper_metadata": {"title": "str", "title_zh": "str", "venue": "str|null", "year": "int|null"},
        "analysis_truth": {
            "real_bottleneck": "str",
            "causal_knob": "str",
            "core_insight": "str",
            "decisive_evidence": [{"claim": "str", "anchor": "str", "confidence": "float"}],
        },
        "method": {
            "proposed_method_name": "str",
            "baseline_methods": [{"name": "str", "role": "str"}],
            "changed_slots": [{"slot_name": "str", "baseline_value": "str", "proposed_value": "str", "evidence_anchor": "str", "confidence": "float"}],
            "pipeline_modules": [{"name": "str", "role": "str", "evidence_anchor": "str"}],
        },
        "experiments": {
            "main_results": [{"benchmark": "str", "metric": "str", "proposed": "str", "baseline": "str", "delta": "str", "anchor": "str", "confidence": "float"}],
            "ablations": [{"claim": "str", "anchor": "str", "confidence": "float"}],
            "fairness_notes": ["str"],
        },
        "formulas": [{"name": "str", "latex": "str", "meaning": "str", "anchor": "str"}],
        "figures_tables": [{"label": "str", "role": "str", "caption": "str"}],
        "limitations": ["str"],
        "open_questions": ["str"],
    }
    return json.dumps({"schema": schema, "raw_output": raw_text}, ensure_ascii=False, indent=2)


def normalize_main_analysis(title: str, parsed: dict[str, Any], *, source_links: list[dict[str, str]] | None = None) -> dict[str, Any]:
    normalized = dict(parsed)
    metadata = normalized.get("paper_metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    metadata.setdefault("title", title)
    metadata.setdefault("title_zh", title)
    metadata.setdefault("venue", None)
    metadata.setdefault("year", None)
    normalized["paper_metadata"] = metadata

    for key, default in {
        "analysis_truth": {
            "real_bottleneck": "",
            "causal_knob": "",
            "core_insight": "",
            "decisive_evidence": [],
        },
        "method": {
            "proposed_method_name": "",
            "baseline_methods": [],
            "changed_slots": [],
            "pipeline_modules": [],
        },
        "experiments": {
            "main_results": [],
            "ablations": [],
            "fairness_notes": [],
        },
    }.items():
        if not isinstance(normalized.get(key), dict):
            normalized[key] = default
    for key in ["formulas", "figures_tables", "limitations", "open_questions"]:
        if not isinstance(normalized.get(key), list):
            normalized[key] = []
    if source_links is not None:
        normalized["source_links"] = source_links
    elif not isinstance(normalized.get("source_links"), list):
        normalized["source_links"] = []
    return normalized


def main_analysis_fallback(
    title: str,
    part_results: list[dict[str, Any]],
    figures_tables: list[dict[str, Any]],
    error: str,
    raw_text: str,
) -> dict[str, Any]:
    method_evidence: list[dict[str, Any]] = []
    experiment_evidence: list[dict[str, Any]] = []
    formulas: list[dict[str, Any]] = []
    open_questions: list[str] = []

    for part in part_results:
        part_id = str(part.get("part_id") or "")
        for item in part.get("method_evidence") or []:
            if isinstance(item, dict):
                claim = compact_text(item.get("claim"), max_len=220)
                if claim:
                    method_evidence.append({
                        "claim": claim,
                        "anchor": compact_text(item.get("anchor") or item.get("section") or part_id, max_len=220),
                        "confidence": item.get("confidence", 0.35),
                    })
        for item in part.get("experiment_evidence") or []:
            if isinstance(item, dict):
                claim = compact_text(item.get("claim"), max_len=220)
                if claim:
                    experiment_evidence.append({
                        "claim": claim,
                        "anchor": compact_text(item.get("table_or_figure") or part_id, max_len=120),
                        "confidence": item.get("confidence", 0.35),
                    })
        for item in part.get("formula_evidence") or []:
            if isinstance(item, dict):
                latex = compact_text(item.get("latex"), max_len=300)
                if latex:
                    formulas.append({
                        "name": compact_text(item.get("name") or part_id, max_len=120),
                        "latex": latex,
                        "meaning": compact_text(item.get("meaning"), max_len=220),
                        "anchor": compact_text(item.get("section") or part_id, max_len=120),
                    })
        for question in part.get("open_questions") or []:
            text = compact_text(question, max_len=220)
            if text:
                open_questions.append(text)

    primary_claim = method_evidence[0]["claim"] if method_evidence else ""
    return {
        "paper_metadata": {"title": title, "title_zh": title, "venue": None, "year": None},
        "analysis_truth": {
            "real_bottleneck": "",
            "causal_knob": "",
            "core_insight": primary_claim,
            "decisive_evidence": method_evidence[:5],
        },
        "method": {
            "proposed_method_name": "",
            "baseline_methods": [],
            "changed_slots": [],
            "pipeline_modules": [
                {"name": item["claim"], "role": "part-analysis fallback evidence", "evidence_anchor": item["anchor"]}
                for item in method_evidence[:6]
            ],
        },
        "experiments": {
            "main_results": [
                {
                    "benchmark": "",
                    "metric": "",
                    "proposed": item["claim"],
                    "baseline": "",
                    "delta": "",
                    "anchor": item["anchor"],
                    "confidence": item["confidence"],
                }
                for item in experiment_evidence[:6]
            ],
            "ablations": [],
            "fairness_notes": [],
        },
        "formulas": formulas[:8],
        "figures_tables": [
            {
                "label": str(item.get("label") or ""),
                "role": compact_text(item.get("visual_summary") or item.get("type") or "", max_len=180),
                "caption": compact_text(item.get("caption"), max_len=300),
            }
            for item in figures_tables[:12]
        ],
        "limitations": ["主分析输出未能解析为完整 JSON，本 note 基于 part-analysis 和本地锚点保底生成。"],
        "open_questions": [
            f"main_analysis 解析/修复失败，需要人工复核: {compact_text(error, max_len=300)}",
            f"原始主分析输出片段: {compact_text(raw_text, max_len=500)}",
            *open_questions[:6],
        ],
    }


def repair_common_json_issues(text: str) -> str:
    repaired = re.sub(r",(\s*[}\]])", r"\1", text)
    repaired = re.sub(r'(")\s+(")', r"\1,\n\2", repaired)
    repaired = re.sub(r"([}\]])\s+(\")", r"\1,\n\2", repaired)
    repaired = re.sub(r'(")\s+(\{)', r"\1,\n\2", repaired)
    repaired = re.sub(r"([}\]])\s+(\{)", r"\1,\n\2", repaired)
    return repaired


def balanced_json_object_prefix(text: str) -> str:
    if not text.startswith("{"):
        return text
    depth = 0
    in_string = False
    escape_next = False
    for index, ch in enumerate(text):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[:index + 1]
    return text


def balanced_json_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    for start, ch in enumerate(text):
        if ch != "{":
            continue
        candidate = balanced_json_object_prefix(text[start:])
        if candidate.startswith("{"):
            candidates.append(candidate)
    return candidates


def fix_invalid_escapes(text: str) -> str:
    return re.sub(
        r'\\([^"\\/bfnrtu])',
        lambda m: "\\\\" + m.group(1),
        text,
    )


def protect_latex_escapes(text: str) -> str:
    """Double backslashes for common LaTeX commands before json.loads.

    Some commands start with valid JSON escapes, e.g. ``\beta`` is parsed as a
    backspace plus ``eta`` unless protected before decoding.
    """
    latex_commands = {
        "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta",
        "eta", "theta", "vartheta", "iota", "kappa", "lambda", "mu", "nu",
        "xi", "pi", "rho", "sigma", "tau", "upsilon", "phi", "varphi",
        "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda", "Xi",
        "Pi", "Sigma", "Phi", "Psi", "Omega", "frac", "dfrac", "tfrac",
        "sqrt", "sum", "prod", "int", "lim", "log", "ln", "exp", "min",
        "max", "argmin", "argmax", "text", "mathrm", "mathbf", "mathit",
        "mathcal", "operatorname", "left", "right", "leq", "geq", "neq",
        "approx", "times", "cdot", "infty", "nabla", "partial", "begin",
        "end", "label", "ref", "eqref", "hat", "bar", "tilde", "dot",
        "ddot", "overline", "underline",
    }

    def repl(match: re.Match[str]) -> str:
        command = match.group(1)
        if command in latex_commands:
            return "\\\\" + command
        return match.group(0)

    return re.sub(r"(?<!\\)\\([A-Za-z]+)", repl, text)


def close_truncated_json(text: str) -> str:
    stack: list[str] = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            stack.append("}")
        elif ch == "}":
            if stack and stack[-1] == "}":
                stack.pop()
        elif ch == "[":
            stack.append("]")
        elif ch == "]":
            if stack and stack[-1] == "]":
                stack.pop()
    repaired = text.rstrip()
    if in_string:
        repaired += '"'
    removed_trailing_object = False
    if stack:
        if re.search(r",\s*\{\s*\"[^\"]+\"\s*:\s*$", repaired):
            repaired = re.sub(r",\s*\{\s*\"[^\"]+\"\s*:\s*$", "", repaired)
            removed_trailing_object = True
        else:
            repaired = re.sub(r",\s*\"[^\"]+\"\s*:\s*$", "", repaired)
            repaired = re.sub(r"\{\s*\"[^\"]+\"\s*:\s*$", "{", repaired)
        closer = stack[-1]
        repaired = re.sub(r",\s*$", "", repaired)
        repaired = re.sub(r",\s*([}\]])\s*$", r"\1", repaired)
        if closer in "]}":
            repaired = re.sub(r",(\s*" + re.escape(closer) + r")$", r"\1", repaired)
    closers = list(reversed(stack))
    if removed_trailing_object and "}" in closers:
        closers.remove("}")
    repaired += "".join(closers)
    return repaired


def split_markdown(text: str, *, max_chars: int, overlap_chars: int) -> list[Chunk]:
    text = (text or "").strip()
    if not text:
        return []
    if max_chars < 1000:
        raise ValueError("max_chars must be at least 1000")
    if overlap_chars < 0 or overlap_chars >= max_chars // 2:
        raise ValueError("overlap_chars must be non-negative and less than half max_chars")

    spans: list[tuple[int, int, str]] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            lower_bound = start + max_chars // 2
            split_at = text.rfind("\n# ", start, end)
            if split_at <= lower_bound:
                split_at = text.rfind("\n## ", start, end)
            if split_at <= lower_bound:
                split_at = text.rfind("\n\n", start, end)
            if split_at > lower_bound:
                end = split_at
        chunk = text[start:end].strip()
        if chunk:
            spans.append((start, end, chunk))
        if end >= len(text):
            break
        start = max(end - overlap_chars, start + 1)

    total = len(spans)
    return [
        Chunk(index=i, total=total, start=start, end=end, text=chunk)
        for i, (start, end, chunk) in enumerate(spans, 1)
    ]


def page_count_from_content_list(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    pages: set[int] = set()
    stack = [data]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            for key in ("page_idx", "page", "page_num"):
                value = item.get(key)
                if isinstance(value, int):
                    pages.add(value)
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return len(pages) if pages else None


def apply_adaptive_token_budget(
    args: argparse.Namespace,
    *,
    markdown_chars: int,
    chunk_count: int,
    page_count: int | None,
) -> dict[str, Any]:
    chars_per_page = (markdown_chars / page_count) if page_count else None
    long_doc = (
        chunk_count >= args.adaptive_long_chunk_count
        or markdown_chars >= args.adaptive_long_markdown_chars
        or (chars_per_page is not None and chars_per_page >= args.adaptive_long_chars_per_page)
    )
    extreme_doc = (
        chunk_count >= args.adaptive_extreme_chunk_count
        or markdown_chars >= args.adaptive_extreme_markdown_chars
        or (page_count is not None and page_count >= args.adaptive_extreme_pages)
    )
    before = {
        "part_max_tokens": args.part_max_tokens,
        "main_max_tokens": args.main_max_tokens,
        "writer_max_tokens": args.writer_max_tokens,
        "main_context_chars": args.main_context_chars,
    }
    profile = "default"
    if args.adaptive_tokens and extreme_doc:
        profile = "extreme"
        args.part_max_tokens = max(args.part_max_tokens, args.adaptive_long_part_max_tokens)
        args.main_max_tokens = max(args.main_max_tokens, args.adaptive_extreme_main_max_tokens)
        args.main_context_chars = max(args.main_context_chars, args.adaptive_long_main_context_chars)
    elif args.adaptive_tokens and long_doc:
        profile = "long"
        args.part_max_tokens = max(args.part_max_tokens, args.adaptive_long_part_max_tokens)
        args.main_max_tokens = max(args.main_max_tokens, args.adaptive_long_main_max_tokens)
        args.main_context_chars = max(args.main_context_chars, args.adaptive_long_main_context_chars)
    after = {
        "part_max_tokens": args.part_max_tokens,
        "main_max_tokens": args.main_max_tokens,
        "writer_max_tokens": args.writer_max_tokens,
        "main_context_chars": args.main_context_chars,
    }
    return {
        "enabled": bool(args.adaptive_tokens),
        "profile": profile,
        "markdown_chars": markdown_chars,
        "chunk_count": chunk_count,
        "page_count": page_count,
        "chars_per_page": round(chars_per_page, 3) if chars_per_page is not None else None,
        "before": before,
        "after": after,
        "criteria": {
            "long_chunk_count": args.adaptive_long_chunk_count,
            "long_markdown_chars": args.adaptive_long_markdown_chars,
            "long_chars_per_page": args.adaptive_long_chars_per_page,
            "extreme_chunk_count": args.adaptive_extreme_chunk_count,
            "extreme_markdown_chars": args.adaptive_extreme_markdown_chars,
            "extreme_pages": args.adaptive_extreme_pages,
        },
    }


def find_mineru_artifacts_in_dir(root: Path, artifact_dir: Path) -> MinerUArtifacts:
    md_files = sorted(
        artifact_dir.glob("*.md"),
        key=lambda p: p.stat().st_size if p.exists() else 0,
        reverse=True,
    )
    if not md_files:
        raise FileNotFoundError(f"No markdown file found under {artifact_dir}")
    content_files = (
        sorted(artifact_dir.glob("*content_list_v2.json"))
        or sorted(artifact_dir.glob("*content_list.json"))
    )
    return MinerUArtifacts(
        markdown_path=md_files[0],
        content_list_path=content_files[0] if content_files else None,
        root=root,
    )


def find_mineru_artifacts(root: Path) -> MinerUArtifacts:
    if root.is_file() and root.suffix.lower() == ".md":
        return MinerUArtifacts(markdown_path=root, content_list_path=None, root=root.parent)
    if not root.exists():
        raise FileNotFoundError(f"MinerU output not found: {root}")

    if (root / "auto").is_dir():
        return find_mineru_artifacts_in_dir(root, root / "auto")
    if list(root.glob("*.md")):
        return find_mineru_artifacts_in_dir(root, root)

    auto_dirs = sorted(
        path for path in root.rglob("auto")
        if path.is_dir() and list(path.glob("*.md"))
    )
    if len(auto_dirs) == 1:
        return find_mineru_artifacts_in_dir(auto_dirs[0].parent, auto_dirs[0])
    if len(auto_dirs) > 1:
        raise FileNotFoundError(
            f"Multiple MinerU document outputs found under {root}; pass one paper directory."
        )

    md_parents = sorted({path.parent for path in root.rglob("*.md")})
    if len(md_parents) == 1:
        return find_mineru_artifacts_in_dir(md_parents[0], md_parents[0])
    if len(md_parents) > 1:
        raise FileNotFoundError(
            f"Multiple markdown outputs found under {root}; pass one paper directory."
        )
    raise FileNotFoundError(f"No markdown file found under {root}")


def mineru_match_key(value: str) -> str:
    value = re.sub(r"__[0-9a-f]{12}$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return value.strip("_")


def complete_mineru_output(path: Path) -> bool:
    try:
        artifacts = find_mineru_artifacts(path)
    except FileNotFoundError:
        return False
    return (
        artifacts.markdown_path.exists()
        and artifacts.content_list_path is not None
        and artifacts.content_list_path.exists()
    )


def discover_mineru_output(args: argparse.Namespace, pdf_path: Path) -> Path | None:
    if not args.mineru_output_root:
        return None
    root = Path(args.mineru_output_root).expanduser().resolve()
    if not root.exists():
        return None

    search_roots = []
    if args.mineru_batch_id:
        search_roots.append(root / args.mineru_batch_id)
    search_roots.append(root)

    stems = [pdf_path.stem]
    if args.paper_title:
        stems.append(note_file_stem(args.paper_title))

    direct_candidates = [base / stem for base in search_roots for stem in stems]
    valid_direct = sorted({path.resolve() for path in direct_candidates if complete_mineru_output(path)})
    if len(valid_direct) == 1:
        return valid_direct[0]
    if len(valid_direct) > 1:
        raise RuntimeError(f"Multiple direct MinerU outputs matched {pdf_path}: {valid_direct}")

    keys = {mineru_match_key(stem) for stem in stems if mineru_match_key(stem)}
    matches: list[Path] = []
    for base in search_roots:
        if not base.exists():
            continue
        for child in sorted(path for path in base.iterdir() if path.is_dir()):
            child_key = mineru_match_key(child.name)
            if child_key in keys or any(child_key.startswith(key) or key.startswith(child_key) for key in keys):
                if complete_mineru_output(child):
                    matches.append(child.resolve())

    unique_matches = sorted(set(matches))
    if len(unique_matches) == 1:
        return unique_matches[0]
    if len(unique_matches) > 1:
        raise RuntimeError(f"Multiple MinerU outputs matched {pdf_path}: {unique_matches}")
    return None


def run_mineru_cli(
    *,
    pdf_path: Path,
    output_dir: Path,
    mineru_bin: str,
    backend: str,
    timeout: int,
    model_source: str,
    config_path: Path,
) -> MinerUArtifacts:
    with BlockingFileLock(DEFAULT_MINERU_LOCK):
        output_dir.mkdir(parents=True, exist_ok=True)
        command = [mineru_bin, "-p", str(pdf_path), "-o", str(output_dir), "-b", backend]
        env = os.environ.copy()
        if model_source:
            env["MINERU_MODEL_SOURCE"] = model_source
        if config_path:
            env["MINERU_TOOLS_CONFIG_JSON"] = str(config_path)
        env.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
        started = time.monotonic()
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired as exc:
            atomic_write_text(output_dir / "mineru_stdout.log", exc.stdout or "")
            atomic_write_text(output_dir / "mineru_stderr.log", exc.stderr or "")
            raise RuntimeError(f"MinerU timed out after {timeout}s") from exc
        atomic_write_text(output_dir / "mineru_stdout.log", proc.stdout or "")
        atomic_write_text(output_dir / "mineru_stderr.log", proc.stderr or "")
        atomic_write_json(output_dir / "mineru_command.json", {
            "command": command,
            "env": {
                "MINERU_MODEL_SOURCE": env.get("MINERU_MODEL_SOURCE"),
                "MINERU_TOOLS_CONFIG_JSON": env.get("MINERU_TOOLS_CONFIG_JSON"),
                "PYTORCH_CUDA_ALLOC_CONF": env.get("PYTORCH_CUDA_ALLOC_CONF"),
            },
            "returncode": proc.returncode,
            "duration_seconds": round(time.monotonic() - started, 3),
        })
        if proc.returncode != 0:
            raise RuntimeError(f"MinerU failed with exit code {proc.returncode}: {(proc.stderr or '')[-500:]}")
    return find_mineru_artifacts(output_dir)


def latest_hf_snapshot(cache_root: Path) -> Path | None:
    snapshots_dir = cache_root / "snapshots"
    if not snapshots_dir.exists():
        return None
    snapshots = [path for path in snapshots_dir.iterdir() if path.is_dir()]
    if not snapshots:
        return None
    return max(snapshots, key=lambda path: path.stat().st_mtime)


def ensure_mineru_local_config(args: argparse.Namespace) -> Path:
    config_path = Path(args.mineru_config).expanduser().resolve()
    if config_path.exists():
        return config_path
    if args.mineru_model_source != "local":
        return config_path

    pipeline_root = latest_hf_snapshot(Path(args.mineru_pipeline_cache).expanduser())
    if pipeline_root is None:
        raise FileNotFoundError(
            "MinerU local model source requested, but no local pipeline snapshot was found under "
            f"{args.mineru_pipeline_cache}"
        )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(config_path, {
        "models-dir": {
            "pipeline": str(pipeline_root),
        }
    })
    return config_path


def flatten_content_items(payload: Any) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        if isinstance(payload.get("content"), list):
            return flatten_content_items(payload["content"])
        return [payload]
    if isinstance(payload, list):
        for entry in payload:
            if isinstance(entry, list):
                items.extend(flatten_content_items(entry))
            elif isinstance(entry, dict):
                items.append(entry)
    return items


PAGE_INDEX_KEYS = ("page_idx", "page", "page_num")


def parse_page_index(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def item_page_index(item: dict[str, Any], *, fallback: int | None = None) -> int | None:
    for key in PAGE_INDEX_KEYS:
        parsed = parse_page_index(item.get(key))
        if parsed is not None:
            return parsed
    return fallback


def iter_content_items_with_page(
    payload: Any,
    *,
    page_hint: int | None = None,
    top_level: bool = False,
):
    if isinstance(payload, dict):
        local_page = item_page_index(payload, fallback=page_hint)
        if isinstance(payload.get("content"), list):
            yield from iter_content_items_with_page(payload["content"], page_hint=local_page, top_level=False)
            return
        item = dict(payload)
        if local_page is not None and item_page_index(item) is None:
            item["page_idx"] = local_page
        yield item
        return
    if isinstance(payload, list):
        if top_level and payload and all(isinstance(entry, list) for entry in payload):
            for index, entry in enumerate(payload):
                yield from iter_content_items_with_page(entry, page_hint=index, top_level=False)
            return
        for entry in payload:
            yield from iter_content_items_with_page(entry, page_hint=page_hint, top_level=False)


def caption_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(str(item.get("content") or item.get("text") or ""))
            elif isinstance(item, str):
                parts.append(item)
        return " ".join(part.strip() for part in parts if part and part.strip()).strip()
    return ""


def explicit_label_from_caption(caption: str) -> str:
    match = re.search(r"\b(Figure|Fig\.?|Table)\s*([0-9]+[A-Za-z]?)", caption, flags=re.IGNORECASE)
    if match:
        kind = "Table" if match.group(1).lower().startswith("table") else "Figure"
        return f"{kind} {match.group(2)}"
    return ""


def extract_label(caption: str, fallback_type: str, index: int) -> str:
    explicit = explicit_label_from_caption(caption)
    if explicit:
        return explicit
    return f"{fallback_type.title()} {index}"


def find_mineru_sidecar_artifacts(content_path: Path | None, *, source_root: Path) -> MinerUSidecarArtifacts:
    if content_path is None:
        return MinerUSidecarArtifacts(origin_pdf_path=None, middle_json_path=None, model_json_path=None)

    content_file = content_path.resolve()
    search_dirs: list[Path] = []
    for candidate in [content_file.parent, source_root.resolve(), source_root.resolve() / "auto"]:
        if candidate.exists() and candidate not in search_dirs:
            search_dirs.append(candidate)

    base_name = content_file.name
    suffixes = ("_content_list_v2.json", "_content_list.json")
    stem = base_name
    for suffix in suffixes:
        if base_name.endswith(suffix):
            stem = base_name[: -len(suffix)]
            break

    def first_existing(paths: list[Path]) -> Path | None:
        for path in paths:
            if path.exists():
                return path
        return None

    origin_candidates: list[Path] = []
    middle_candidates: list[Path] = []
    model_candidates: list[Path] = []
    for directory in search_dirs:
        origin_candidates.extend([
            directory / f"{stem}_origin.pdf",
            directory / f"{content_file.stem}_origin.pdf",
        ])
        middle_candidates.extend([
            directory / f"{stem}_middle.json",
            directory / f"{content_file.stem}_middle.json",
        ])
        model_candidates.extend([
            directory / f"{stem}_model.json",
            directory / f"{content_file.stem}_model.json",
        ])
        if not stem:
            continue
        origin_candidates.extend(sorted(directory.glob("*_origin.pdf")))
        middle_candidates.extend(sorted(directory.glob("*_middle.json")))
        model_candidates.extend(sorted(directory.glob("*_model.json")))

    return MinerUSidecarArtifacts(
        origin_pdf_path=first_existing(origin_candidates),
        middle_json_path=first_existing(middle_candidates),
        model_json_path=first_existing(model_candidates),
    )


def load_json_file(path: Path | None) -> Any:
    if path is None or not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except json.JSONDecodeError:
        return None


def resolve_sidecar_page_info(payload: Any) -> dict[int, dict[str, Any]]:
    pages: dict[int, dict[str, Any]] = {}
    if isinstance(payload, list):
        for index, page in enumerate(payload):
            if isinstance(page, dict):
                pages[index] = page
        return pages
    if not isinstance(payload, dict):
        return pages
    pdf_info = payload.get("pdf_info")
    if not isinstance(pdf_info, list):
        return pages
    for index, page in enumerate(pdf_info):
        if not isinstance(page, dict):
            continue
        pages[index] = page
    return pages


def page_pdf_size(middle_page: dict[str, Any] | None) -> tuple[float, float] | None:
    if isinstance(middle_page, dict):
        page_size = middle_page.get("page_size")
        if isinstance(page_size, (list, tuple)) and len(page_size) == 2:
            try:
                width = float(page_size[0])
                height = float(page_size[1])
            except (TypeError, ValueError):
                width = height = 0.0
            if width > 0.0 and height > 0.0:
                return width, height
    return None


def page_render_size(model_page: dict[str, Any] | None) -> tuple[float, float] | None:
    if not isinstance(model_page, dict):
        return None
    page_info = model_page.get("page_info")
    if not isinstance(page_info, dict):
        return None
    try:
        width = float(page_info.get("width") or 0.0)
        height = float(page_info.get("height") or 0.0)
    except (TypeError, ValueError):
        return None
    if width <= 0.0 or height <= 0.0:
        return None
    return width, height


def infer_content_page_size(
    *,
    content_extent: list[float] | None,
    model_page: dict[str, Any] | None,
    pdf_page_size: tuple[float, float] | None,
) -> tuple[float, float] | None:
    if content_extent is not None:
        right = float(content_extent[2])
        bottom = float(content_extent[3])
        if right <= DEFAULT_MINERU_CONTENT_COORD_SIZE[0] * 1.08 and bottom <= DEFAULT_MINERU_CONTENT_COORD_SIZE[1] * 1.08:
            return DEFAULT_MINERU_CONTENT_COORD_SIZE
    render_size = page_render_size(model_page)
    if render_size is not None and content_extent is not None:
        if content_extent[2] <= render_size[0] * 1.05 and content_extent[3] <= render_size[1] * 1.05:
            return render_size
    if pdf_page_size is not None and content_extent is not None:
        if content_extent[2] <= pdf_page_size[0] * 1.05 and content_extent[3] <= pdf_page_size[1] * 1.05:
            return pdf_page_size
    return DEFAULT_MINERU_CONTENT_COORD_SIZE


def scale_bbox_between_spaces(
    bbox: tuple[float, float, float, float] | None,
    *,
    from_size: tuple[float, float] | None,
    to_size: tuple[float, float] | None,
) -> tuple[float, float, float, float] | None:
    if bbox is None:
        return None
    if from_size is None or to_size is None:
        return bbox
    from_width, from_height = from_size
    to_width, to_height = to_size
    if from_width <= 0.0 or from_height <= 0.0 or to_width <= 0.0 or to_height <= 0.0:
        return bbox
    scale_x = to_width / from_width
    scale_y = to_height / from_height
    return (
        bbox[0] * scale_x,
        bbox[1] * scale_y,
        bbox[2] * scale_x,
        bbox[3] * scale_y,
    )


def padded_bbox(
    bbox: tuple[float, float, float, float],
    *,
    page_size: tuple[float, float] | None,
) -> tuple[float, float, float, float]:
    if page_size is None:
        pad_x = pad_y = 8.0
        page_width = page_height = None
    else:
        page_width, page_height = page_size
        pad_x = max(4.0, page_width * 0.008)
        pad_y = max(4.0, page_height * 0.006)
    left = bbox[0] - pad_x
    top = bbox[1] - pad_y
    right = bbox[2] + pad_x
    bottom = bbox[3] + pad_y
    if page_width is not None and page_height is not None:
        left = max(0.0, left)
        top = max(0.0, top)
        right = min(page_width, right)
        bottom = min(page_height, bottom)
    return left, top, right, bottom


def bbox_iou(first: tuple[float, float, float, float] | None, second: tuple[float, float, float, float] | None) -> float:
    if first is None or second is None:
        return 0.0
    left = max(first[0], second[0])
    top = max(first[1], second[1])
    right = min(first[2], second[2])
    bottom = min(first[3], second[3])
    if right <= left or bottom <= top:
        return 0.0
    intersection = (right - left) * (bottom - top)
    union = bbox_area(first) + bbox_area(second) - intersection
    if union <= 0.0:
        return 0.0
    return intersection / union


def middle_visual_blocks_by_page(
    middle_payload: Any,
    *,
    source_root: Path,
) -> dict[int, list[dict[str, Any]]]:
    pages = resolve_sidecar_page_info(middle_payload)
    blocks_by_page: dict[int, list[dict[str, Any]]] = {}
    for page_index, page in pages.items():
        para_blocks = page.get("para_blocks")
        if not isinstance(para_blocks, list):
            continue
        page_blocks: list[dict[str, Any]] = []
        for block in para_blocks:
            if not isinstance(block, dict):
                continue
            block_type = str(block.get("type") or block.get("block_type") or "").lower()
            if block_type not in {"image", "chart", "table"}:
                continue
            bbox = normalize_bbox(block.get("bbox"))
            if bbox is None:
                continue
            source_candidates = [
                block.get("image_path"),
                block.get("img_path"),
                block.get("path"),
            ]
            source_path = ""
            for candidate in source_candidates:
                if not candidate:
                    continue
                resolved = (source_root / str(candidate)).resolve()
                source_path = str(resolved if resolved.exists() else candidate)
                break
            page_blocks.append({
                "page": page_index,
                "type": block_type,
                "bbox": [round(value, 3) for value in bbox],
                "caption": caption_text(block.get("caption")),
                "source_path": source_path,
            })
        if page_blocks:
            blocks_by_page[page_index] = page_blocks
    return blocks_by_page


def figure_table_item_size(payload: Any) -> tuple[float, float] | None:
    if not isinstance(payload, dict):
        return None
    page_info = payload.get("page_info")
    if not isinstance(page_info, dict):
        return None
    try:
        width = float(page_info.get("width") or 0.0)
        height = float(page_info.get("height") or 0.0)
    except (TypeError, ValueError):
        return None
    if width <= 0.0 or height <= 0.0:
        return None
    return width, height


def crop_box_for_cluster(
    cluster_bbox: tuple[float, float, float, float] | None,
    *,
    page_rect: Any,
    content_page_size: tuple[float, float] | None,
    pdf_page_size: tuple[float, float] | None,
) -> Any:
    if fitz is None or cluster_bbox is None or page_rect is None:
        return None
    cluster_bbox = padded_bbox(cluster_bbox, page_size=content_page_size)
    scaled = scale_bbox_between_spaces(
        cluster_bbox,
        from_size=content_page_size,
        to_size=pdf_page_size,
    )
    if scaled is None:
        return None
    crop = fitz.Rect(*scaled)
    page_bounds = fitz.Rect(page_rect)
    crop = crop & page_bounds
    if crop.is_empty or crop.width <= 1 or crop.height <= 1:
        return None
    return crop


def write_full_region_crop(
    *,
    doc: Any,
    image_root: Path,
    page_index: int,
    crop_box: Any,
    cluster_kind: str,
    cluster_label: str,
    cluster_bbox: list[float],
    pdf_page_size: tuple[float, float] | None,
    render_page_size: tuple[float, float] | None,
) -> Path | None:
    if fitz is None:
        return None
    output_dir = image_root / "images" / "rf_full_regions"
    output_dir.mkdir(parents=True, exist_ok=True)
    digest_input = "|".join([
        str(getattr(doc, "name", "") or ""),
        str(page_index),
        json.dumps(cluster_bbox),
        json.dumps([round(value, 3) for value in crop_box]),
        cluster_kind,
        cluster_label,
    ])
    digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()[:12]
    filename = f"page_{page_index + 1:03d}_{safe_slug(cluster_label or cluster_kind, max_len=40)}_{digest}.jpg"
    out_path = output_dir / filename
    if out_path.exists():
        return out_path
    if page_index < 0 or page_index >= len(doc):
        return None
    page = doc.load_page(page_index)
    if (
        pdf_page_size is not None
        and render_page_size is not None
        and pdf_page_size[0] > 0.0
        and pdf_page_size[1] > 0.0
        and render_page_size[0] > 0.0
        and render_page_size[1] > 0.0
    ):
        matrix = fitz.Matrix(render_page_size[0] / pdf_page_size[0], render_page_size[1] / pdf_page_size[1])
    else:
        matrix = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=matrix, clip=crop_box, alpha=False)
    pix.save(out_path)
    return out_path


def full_region_cluster_key(cluster: dict[str, Any]) -> tuple[Any, ...] | None:
    page = item_page_index(cluster)
    cluster_bbox = normalize_bbox(cluster.get("cluster_bbox") or cluster.get("bbox"))
    if page is None or cluster_bbox is None:
        return None
    source_paths = tuple(sorted(str(path) for path in cluster.get("source_paths") or [] if str(path)))
    return (
        page,
        str(cluster.get("type") or ""),
        tuple(round(value, 3) for value in cluster_bbox),
        source_paths,
    )


def full_region_caption(records: list[dict[str, Any]]) -> str:
    captions: list[str] = []
    raw_items = records[0].get("raw_items") if records and isinstance(records[0].get("raw_items"), list) else []
    for item in raw_items:
        caption = str(item.get("caption") or "").strip()
        if caption and caption not in captions:
            captions.append(caption)
    for record in records:
        caption = str(record.get("caption") or "").strip()
        if caption and caption not in captions:
            captions.append(caption)
    explicit = [caption for caption in captions if explicit_label_from_caption(caption)]
    if explicit:
        return max(explicit, key=len)
    if len(captions) <= 4:
        return " ".join(captions)
    return max(captions, key=len) if captions else ""


def full_region_label(records: list[dict[str, Any]], fallback: str) -> str:
    for record in records:
        label = str(record.get("label") or "").strip()
        if explicit_label_from_caption(label):
            return label
    caption = full_region_caption(records)
    explicit = explicit_label_from_caption(caption)
    if explicit:
        return explicit
    return fallback


def maybe_replace_clusters_with_full_region_crops(
    figures_tables: list[dict[str, Any]],
    *,
    content_path: Path | None,
    source_root: Path,
) -> list[dict[str, Any]]:
    if not figures_tables or content_path is None or fitz is None:
        return figures_tables
    sidecars = find_mineru_sidecar_artifacts(content_path, source_root=source_root)
    if sidecars.origin_pdf_path is None or sidecars.middle_json_path is None:
        return figures_tables

    middle_payload = load_json_file(sidecars.middle_json_path)
    model_payload = load_json_file(sidecars.model_json_path)
    middle_pages = resolve_sidecar_page_info(middle_payload)
    model_pages = resolve_sidecar_page_info(model_payload)
    image_root = content_path.parent
    middle_blocks = middle_visual_blocks_by_page(middle_payload, source_root=image_root)

    content_payload = load_json_file(content_path)
    content_items = list(iter_content_items_with_page(content_payload, top_level=True)) if content_payload is not None else []
    content_page_sizes: dict[int, tuple[float, float]] = {}
    content_page_extents: dict[int, list[float]] = {}
    for item in content_items:
        page = item_page_index(item)
        if page is None:
            continue
        if page not in content_page_sizes:
            size = figure_table_item_size(item)
            if size is not None:
                content_page_sizes[page] = size
        bbox = normalize_bbox(item.get("bbox"))
        if bbox is not None:
            extent = content_page_extents.setdefault(page, [bbox[0], bbox[1], bbox[2], bbox[3]])
            extent[0] = min(extent[0], bbox[0])
            extent[1] = min(extent[1], bbox[1])
            extent[2] = max(extent[2], bbox[2])
            extent[3] = max(extent[3], bbox[3])

    try:
        with fitz.open(sidecars.origin_pdf_path) as doc:
            crop_cache: dict[tuple[Any, ...], tuple[Path, list[dict[str, Any]], list[float]]] = {}
            pending_by_key: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
            ungrouped: list[dict[str, Any]] = []
            for cluster in figures_tables:
                cluster_key = full_region_cluster_key(cluster)
                if cluster_key is None:
                    ungrouped.append(cluster)
                    continue
                pending_by_key.setdefault(cluster_key, []).append(cluster)

            rewritten: list[dict[str, Any]] = list(ungrouped)
            for cluster_key, cluster_records in pending_by_key.items():
                cluster = cluster_records[0]
                cluster_size = int(cluster.get("cluster_size") or 0)
                source_paths = [str(path) for path in cluster.get("source_paths") or [] if str(path)]
                page = item_page_index(cluster)
                cluster_bbox_list = cluster.get("cluster_bbox") or cluster.get("bbox")
                cluster_bbox = normalize_bbox(cluster_bbox_list)
                if page is None or page < 0 or page >= len(doc) or cluster_bbox is None:
                    rewritten.extend(cluster_records)
                    continue
                if cluster_size <= 1:
                    rewritten.extend(cluster_records)
                    continue

                page_middle = middle_pages.get(page)
                page_model = model_pages.get(page)
                pdf_page_size = page_pdf_size(page_middle) or (
                    float(doc[page].rect.width),
                    float(doc[page].rect.height),
                )
                content_page_size = content_page_sizes.get(page) or infer_content_page_size(
                    content_extent=content_page_extents.get(page),
                    model_page=page_model,
                    pdf_page_size=pdf_page_size,
                )
                page_rect = doc[page].rect
                crop_box = crop_box_for_cluster(
                    cluster_bbox,
                    page_rect=page_rect,
                    content_page_size=content_page_size,
                    pdf_page_size=pdf_page_size,
                )
                if crop_box is None:
                    rewritten.extend(cluster_records)
                    continue

                raw_items = cluster.get("raw_items") if isinstance(cluster.get("raw_items"), list) else []
                if cluster_key in crop_cache:
                    crop_path, matched_middle, crop_box_list = crop_cache[cluster_key]
                else:
                    crop_box_list = [round(value, 3) for value in crop_box]
                    crop_box_pdf = normalize_bbox(crop_box_list)
                    matched_middle = []
                    for block in middle_blocks.get(page, []):
                        block_bbox = normalize_bbox(block.get("bbox"))
                        if bbox_iou(block_bbox, crop_box_pdf) > 0:
                            matched_middle.append(block)
                    crop_path = write_full_region_crop(
                        doc=doc,
                        image_root=image_root,
                        page_index=page,
                        crop_box=crop_box,
                        cluster_kind=str(cluster.get("type") or "figure"),
                        cluster_label=str(next(
                            (str(item.get("label") or "").strip() for item in raw_items if str(item.get("label") or "").strip()),
                            str(cluster.get("label") or ""),
                        )),
                        cluster_bbox=[round(value, 3) for value in cluster_bbox],
                        pdf_page_size=pdf_page_size,
                        render_page_size=page_render_size(page_model),
                    )
                    if crop_path is None:
                        rewritten.extend(cluster_records)
                        continue
                    crop_cache[cluster_key] = (crop_path, matched_middle, crop_box_list)

                updated = dict(cluster)
                updated["caption"] = full_region_caption(cluster_records) or str(cluster.get("caption") or "")
                updated["label"] = full_region_label(cluster_records, str(cluster.get("label") or ""))
                updated["source_path"] = str(crop_path.resolve())
                updated["bbox"] = [round(value, 3) for value in cluster_bbox]
                updated["full_region_source"] = "pdf_crop"
                updated["full_region_origin_pdf"] = str(sidecars.origin_pdf_path.resolve())
                updated["full_region_bbox_pdf"] = crop_box_list
                updated["full_region_bbox_content"] = [round(value, 3) for value in cluster_bbox]
                if raw_items:
                    updated["raw_items"] = raw_items
                if matched_middle:
                    updated["middle_visual_blocks"] = matched_middle
                rewritten.append(updated)
            return sorted(
                rewritten,
                key=lambda item: (
                    item.get("page") is None,
                    item.get("page") if item.get("page") is not None else 10**9,
                    (item.get("bbox") or [0.0, 0.0])[1],
                    (item.get("bbox") or [0.0, 0.0])[0],
                    str(item.get("label") or ""),
                ),
            )
    except Exception:  # noqa: BLE001
        return figures_tables


def markdown_image_ref_candidates(source_path: str, *, source_root: Path) -> set[str]:
    if not source_path:
        return set()
    path = Path(source_path)
    candidates = {str(source_path).replace("\\", "/")}
    if path.is_absolute():
        try:
            candidates.add(path.resolve().relative_to(source_root.resolve()).as_posix())
        except ValueError:
            pass
    else:
        candidates.add(path.as_posix())
    if path.name:
        candidates.add(path.name)
        candidates.add(f"images/{path.name}")
    return {candidate for candidate in candidates if candidate}


def full_region_markdown_ref(source_path: str, *, source_root: Path) -> str | None:
    if not source_path:
        return None
    path = Path(source_path)
    if not path.exists():
        return None
    try:
        return path.resolve().relative_to(source_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_markdown_full_region_image_refs(
    markdown: str,
    figures_tables: list[dict[str, Any]],
    *,
    source_root: Path,
) -> str:
    ref_to_group: dict[str, str] = {}
    group_to_full_ref: dict[str, str] = {}
    group_to_anchor_texts: dict[str, list[str]] = {}
    for index, item in enumerate(figures_tables):
        if item.get("full_region_source") != "pdf_crop":
            continue
        full_ref = full_region_markdown_ref(str(item.get("source_path") or ""), source_root=source_root)
        if not full_ref:
            continue
        source_paths = [str(path) for path in item.get("source_paths") or [] if str(path)]
        if not source_paths:
            continue
        group_id = f"full_region_{index}"
        group_to_full_ref[group_id] = full_ref
        anchors: list[str] = []
        for raw_item in item.get("raw_items") or []:
            if not isinstance(raw_item, dict):
                continue
            caption = compact_text(raw_item.get("caption"), max_len=180)
            if len(caption) >= 8 and caption not in anchors:
                anchors.append(caption)
        caption = compact_text(item.get("caption"), max_len=220)
        if len(caption) >= 8 and caption not in anchors:
            anchors.append(caption)
        group_to_anchor_texts[group_id] = anchors
        for source_path in source_paths:
            for candidate in markdown_image_ref_candidates(source_path, source_root=source_root):
                ref_to_group[candidate] = group_id

    if not group_to_full_ref:
        return markdown

    seen_groups = {
        group_id
        for group_id, full_ref in group_to_full_ref.items()
        if full_ref in markdown
    }
    out_lines: list[str] = []
    image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for line in markdown.splitlines():
        replacements: list[tuple[int, int, str]] = []
        for match in image_pattern.finditer(line):
            target = match.group(1).strip().replace("\\", "/")
            group_id = ref_to_group.get(target) or ref_to_group.get(Path(target).name)
            if group_id:
                replacement = ""
                if group_id not in seen_groups:
                    replacement = f"![]({group_to_full_ref[group_id]})"
                    seen_groups.add(group_id)
                replacements.append((match.start(), match.end(), replacement))
        if not replacements:
            out_lines.append(line)
            continue
        new_line = line
        for start, end, replacement in reversed(replacements):
            new_line = new_line[:start] + replacement + new_line[end:]
        if new_line.strip():
            out_lines.append(new_line)
    for group_id, full_ref in group_to_full_ref.items():
        if group_id in seen_groups:
            continue
        block = f"![]({full_ref})"
        anchors = group_to_anchor_texts.get(group_id) or []
        inserted = False
        for line_index, line in enumerate(out_lines):
            if any(anchor and anchor in line for anchor in anchors):
                out_lines.insert(line_index, block)
                inserted = True
                break
        if not inserted:
            if out_lines and out_lines[-1].strip():
                out_lines.append("")
            out_lines.append(block)
        seen_groups.add(group_id)
    return "\n".join(out_lines) + ("\n" if markdown.endswith("\n") else "")


def extract_figures_tables(content_path: Path | None, *, source_root: Path) -> list[dict[str, Any]]:
    if not content_path or not content_path.exists():
        return []
    try:
        payload = json.loads(content_path.read_text(encoding="utf-8", errors="ignore"))
    except json.JSONDecodeError:
        return []
    all_items = list(iter_content_items_with_page(payload, top_level=True))
    page_extents: dict[int, list[float]] = {}
    for item in all_items:
        page = item_page_index(item)
        bbox = normalize_bbox(item.get("bbox"))
        if page is None or bbox is None:
            continue
        extent = page_extents.setdefault(page, [bbox[0], bbox[1], bbox[2], bbox[3]])
        extent[0] = min(extent[0], bbox[0])
        extent[1] = min(extent[1], bbox[1])
        extent[2] = max(extent[2], bbox[2])
        extent[3] = max(extent[3], bbox[3])

    figure_items: list[dict[str, Any]] = []
    for order, item in enumerate(all_items):
        item_type = str(item.get("type") or "").lower()
        content = item.get("content") if isinstance(item.get("content"), dict) else {}
        if item_type in {"image", "chart", "figure"}:
            kind = "figure"
            caption = (
                caption_text(content.get("image_caption"))
                or caption_text(item.get("image_caption"))
                or caption_text(content.get("chart_caption"))
                or caption_text(item.get("chart_caption"))
                or caption_text(item.get("caption"))
            )
        elif item_type == "table":
            kind = "table"
            caption = (
                caption_text(content.get("table_caption"))
                or caption_text(item.get("table_caption"))
                or caption_text(item.get("caption"))
            )
        else:
            continue

        image_source = content.get("image_source") if isinstance(content.get("image_source"), dict) else {}
        src = item.get("img_path") or image_source.get("path") or item.get("image_path")
        src_path = None
        if src:
            candidate = (content_path.parent / src).resolve()
            if not candidate.exists():
                candidate = (source_root / src).resolve()
            if candidate.exists():
                src_path = candidate
        figure_items.append({
            "kind": kind,
            "item_type": item_type,
            "caption": caption,
            "explicit_label": explicit_label_from_caption(caption),
            "source_path": str(src_path) if src_path else str(src or ""),
            "page": item_page_index(item),
            "bbox": normalize_bbox(item.get("bbox")),
            "order": order,
        })

    figures_tables = cluster_figure_table_items(figure_items, page_extents=page_extents)
    return maybe_replace_clusters_with_full_region_crops(
        figures_tables,
        content_path=content_path,
        source_root=source_root,
    )


def normalize_bbox(value: Any) -> tuple[float, float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        return None
    try:
        x0, y0, x1, y1 = (float(part) for part in value)
    except (TypeError, ValueError):
        return None
    left, right = sorted((x0, x1))
    top, bottom = sorted((y0, y1))
    return left, top, right, bottom


def bbox_width(bbox: tuple[float, float, float, float] | None) -> float:
    if bbox is None:
        return 0.0
    return max(0.0, bbox[2] - bbox[0])


def bbox_height(bbox: tuple[float, float, float, float] | None) -> float:
    if bbox is None:
        return 0.0
    return max(0.0, bbox[3] - bbox[1])


def bbox_area(bbox: tuple[float, float, float, float] | None) -> float:
    return bbox_width(bbox) * bbox_height(bbox)


def bbox_center(bbox: tuple[float, float, float, float] | None) -> tuple[float, float]:
    if bbox is None:
        return 0.0, 0.0
    return (bbox[0] + bbox[2]) / 2.0, (bbox[1] + bbox[3]) / 2.0


def bbox_union(items: list[dict[str, Any]]) -> list[float] | None:
    boxes = [item.get("bbox") for item in items if item.get("bbox") is not None]
    if not boxes:
        return None
    left = min(box[0] for box in boxes)
    top = min(box[1] for box in boxes)
    right = max(box[2] for box in boxes)
    bottom = max(box[3] for box in boxes)
    return [round(left, 3), round(top, 3), round(right, 3), round(bottom, 3)]


def axis_gap(a0: float, a1: float, b0: float, b1: float) -> float:
    if a1 < b0:
        return b0 - a1
    if b1 < a0:
        return a0 - b1
    return 0.0


def axis_overlap(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def bboxes_are_connected(
    first: tuple[float, float, float, float] | None,
    second: tuple[float, float, float, float] | None,
    *,
    page_extent: list[float] | None,
) -> bool:
    if first is None or second is None:
        return False
    x_gap = axis_gap(first[0], first[2], second[0], second[2])
    y_gap = axis_gap(first[1], first[3], second[1], second[3])
    x_overlap = axis_overlap(first[0], first[2], second[0], second[2])
    y_overlap = axis_overlap(first[1], first[3], second[1], second[3])
    min_width = max(1.0, min(bbox_width(first), bbox_width(second)))
    min_height = max(1.0, min(bbox_height(first), bbox_height(second)))
    page_width = max(1.0, (page_extent[2] - page_extent[0]) if page_extent else max(first[2], second[2]))
    page_height = max(1.0, (page_extent[3] - page_extent[1]) if page_extent else max(first[3], second[3]))
    horizontal_gap_limit = max(24.0, min_width * 0.16, page_width * 0.03)
    vertical_gap_limit = max(28.0, min_height * 0.28, page_height * 0.06)
    vertical_overlap_ratio = y_overlap / min_height
    horizontal_overlap_ratio = x_overlap / min_width
    if x_gap == 0.0 and y_gap == 0.0:
        return True
    if vertical_overlap_ratio >= 0.45 and x_gap <= horizontal_gap_limit:
        return True
    if horizontal_overlap_ratio >= 0.55 and y_gap <= vertical_gap_limit:
        return True
    return False


def connected_components_for_visual_items(
    items: list[dict[str, Any]],
    *,
    page_extent: list[float] | None,
) -> list[list[dict[str, Any]]]:
    if not items:
        return []
    remaining = list(items)
    components: list[list[dict[str, Any]]] = []
    while remaining:
        seed = remaining.pop(0)
        component = [seed]
        stack = [seed]
        while stack:
            current = stack.pop()
            next_remaining: list[dict[str, Any]] = []
            for candidate in remaining:
                if bboxes_are_connected(current.get("bbox"), candidate.get("bbox"), page_extent=page_extent):
                    component.append(candidate)
                    stack.append(candidate)
                else:
                    next_remaining.append(candidate)
            remaining = next_remaining
        components.append(sorted(component, key=lambda item: item.get("order", 0)))
    return components


def component_anchor_bbox(items: list[dict[str, Any]]) -> tuple[float, float, float, float] | None:
    cluster_bbox = bbox_union(items)
    return normalize_bbox(cluster_bbox)


def split_component_by_labels(items: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    labels: list[str] = []
    anchors_by_label: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        label = str(item.get("explicit_label") or "").strip()
        if not label:
            continue
        if label not in anchors_by_label:
            labels.append(label)
            anchors_by_label[label] = []
        anchors_by_label[label].append(item)
    if len(labels) <= 1:
        return [items]

    anchor_boxes = {
        label: component_anchor_bbox(anchor_items)
        for label, anchor_items in anchors_by_label.items()
    }
    assigned: dict[str, list[dict[str, Any]]] = {label: [] for label in labels}
    for item in items:
        if str(item.get("explicit_label") or "").strip() in assigned:
            assigned[str(item.get("explicit_label") or "").strip()].append(item)
            continue
        best_label = labels[0]
        best_score: float | None = None
        item_bbox = item.get("bbox")
        item_center = bbox_center(item_bbox)
        for label in labels:
            anchor_bbox = anchor_boxes.get(label)
            anchor_center = bbox_center(anchor_bbox)
            x_gap = axis_gap(item_bbox[0], item_bbox[2], anchor_bbox[0], anchor_bbox[2]) if item_bbox and anchor_bbox else 0.0
            y_gap = axis_gap(item_bbox[1], item_bbox[3], anchor_bbox[1], anchor_bbox[3]) if item_bbox and anchor_bbox else 0.0
            center_score = ((item_center[0] - anchor_center[0]) ** 2 + (item_center[1] - anchor_center[1]) ** 2) ** 0.5
            score = x_gap * 2.0 + y_gap * 2.0 + center_score
            if best_score is None or score < best_score:
                best_label = label
                best_score = score
        assigned[best_label].append(item)
    return [
        sorted(cluster, key=lambda item: item.get("order", 0))
        for label, cluster in assigned.items()
        if cluster
    ]


def cluster_primary_caption(items: list[dict[str, Any]]) -> str:
    captions = [str(item.get("caption") or "").strip() for item in items if str(item.get("caption") or "").strip()]
    if not captions:
        return ""
    explicit_captions = [caption for caption in captions if explicit_label_from_caption(caption)]
    if explicit_captions:
        return max(explicit_captions, key=len)
    return max(captions, key=lambda caption: (len(caption) >= 24, len(caption)))


def generic_cluster_label(kind: str) -> str:
    return "Table" if kind == "table" else "Figure"


def representative_source_path(items: list[dict[str, Any]]) -> str:
    ranked = sorted(
        items,
        key=lambda item: (
            0 if item.get("explicit_label") else 1,
            -bbox_area(item.get("bbox")),
            item.get("order", 0),
        ),
    )
    for item in ranked:
        source_path = str(item.get("source_path") or "")
        if source_path:
            return source_path
    return ""


def cluster_item_label(item: dict[str, Any], *, kind: str, cluster_label: str) -> str:
    explicit = str(item.get("explicit_label") or "").strip()
    if explicit:
        return explicit
    return generic_cluster_label(kind)


def source_preserving_cluster_records(
    *,
    kind: str,
    page: int | None,
    cluster_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    cluster_caption = cluster_primary_caption(cluster_items)
    cluster_label = next(
        (str(item.get("explicit_label") or "").strip() for item in cluster_items if str(item.get("explicit_label") or "").strip()),
        "",
    ) or generic_cluster_label(kind)
    source_paths: list[str] = []
    for item in cluster_items:
        source_path = str(item.get("source_path") or "")
        if source_path and source_path not in source_paths:
            source_paths.append(source_path)
    raw_items = [
        {
            "type": str(item.get("item_type") or ""),
            "page": item.get("page"),
            "bbox": [round(value, 3) for value in item["bbox"]] if item.get("bbox") is not None else None,
            "caption": str(item.get("caption") or ""),
            "label": str(item.get("explicit_label") or ""),
            "source_path": str(item.get("source_path") or ""),
        }
        for item in cluster_items
    ]
    cluster_bbox = bbox_union(cluster_items)
    shared = {
        "source_paths": source_paths,
        "page": page,
        "cluster_size": len(cluster_items),
        "raw_items": raw_items,
    }
    if len(source_paths) <= 1:
        return [{
            "label": cluster_label,
            "type": kind,
            "caption": cluster_caption,
            "source_path": representative_source_path(cluster_items),
            "bbox": cluster_bbox,
            **shared,
        }]

    records: list[dict[str, Any]] = []
    for item in cluster_items:
        source_path = str(item.get("source_path") or "")
        if not source_path:
            continue
        item_bbox = bbox_union([item])
        records.append({
            "label": cluster_item_label(item, kind=kind, cluster_label=cluster_label),
            "type": kind,
            "caption": str(item.get("caption") or "").strip(),
            "source_path": source_path,
            "bbox": item_bbox,
            "cluster_bbox": cluster_bbox,
            **shared,
        })
    return records


def cluster_figure_table_items(
    items: list[dict[str, Any]],
    *,
    page_extents: dict[int, list[float]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, int | None], list[dict[str, Any]]] = {}
    for item in items:
        page = item.get("page")
        key = (
            str(item.get("kind") or ""),
            page,
            item.get("order") if page is None else None,
        )
        grouped.setdefault(key, []).append(item)

    clusters: list[dict[str, Any]] = []
    for (kind, page, _), group_items in grouped.items():
        page_extent = page_extents.get(page) if page is not None else None
        for component in connected_components_for_visual_items(
            sorted(group_items, key=lambda item: item.get("order", 0)),
            page_extent=page_extent,
        ):
            for cluster_items in split_component_by_labels(component):
                clusters.extend(source_preserving_cluster_records(
                    kind=kind,
                    page=page,
                    cluster_items=cluster_items,
                ))

    return sorted(
        clusters,
        key=lambda item: (
            item.get("page") is None,
            item.get("page") if item.get("page") is not None else 10**9,
            (item.get("bbox") or [0.0, 0.0])[1],
            (item.get("bbox") or [0.0, 0.0])[0],
            str(item.get("label") or ""),
        ),
    )


def table_cell(value: Any) -> str:
    return str(value or "").replace("\n", " ").replace("|", "/").strip()


def markdown_link(label: str, url: str) -> str:
    return f"[{table_cell(label)}]({table_cell(url)})"


def normalize_extracted_url(url: str) -> str:
    text = str(url or "").strip().strip("<>")
    while text and text[-1] in ".,;:)]}":
        text = text[:-1]
    return text


def classify_link(label: str, url: str) -> str:
    label_l = label.lower()
    url_l = url.lower()
    if "project" in label_l or "project" in url_l or "github.io" in url_l:
        return "Project"
    if "code" in label_l or "github" in label_l or "github.com" in url_l or "gitlab" in url_l:
        return "Code"
    if "arxiv" in label_l or "arxiv.org" in url_l:
        return "arXiv"
    return ""


def extract_source_links(*texts: Any) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(label: str, url: str) -> None:
        clean_url = normalize_extracted_url(url)
        if not clean_url.startswith(("http://", "https://")):
            return
        clean_label = label or classify_link(label, clean_url) or "link"
        key = (clean_label.lower(), clean_url)
        if key in seen:
            return
        seen.add(key)
        links.append({"label": clean_label, "url": clean_url})

    for value in texts:
        text = str(value or "")
        if not text:
            continue
        for label, url in re.findall(r"\[([^\]]{1,80})\]\((https?://[^)\s]+)\)", text):
            add(classify_link(label, url) or label.strip(), url)
        for label, url in re.findall(r"(?i)\b(project\s+page|project|code|github)\s*[:：]\s*(https?://\S+)", text):
            add(classify_link(label, url) or label, url)
        for url in re.findall(r"https?://\S+", text):
            inferred = classify_link("", url)
            if inferred:
                add(inferred, url)
    return links


def link_is_paper_url(url: str, paper_link: str, openreview_forum_id: str) -> bool:
    clean = normalize_extracted_url(url)
    if paper_link and clean == normalize_extracted_url(paper_link):
        return True
    if openreview_forum_id and openreview_forum_id in clean and "openreview.net" in clean:
        return True
    return False


def compact_text(value: Any, *, max_len: int = 260) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) <= max_len:
        return text
    return text[: max(0, max_len - 1)].rstrip() + "..."


def dedupe_caption_prefix(label: str, caption: str) -> str:
    text = re.sub(r"\s+", " ", str(caption or "")).strip()
    if not text:
        return ""
    if label:
        text = re.sub(rf"^(?:{re.escape(label)}\s*[:.\-–—]?\s*)+", "", text, flags=re.IGNORECASE)
        embedded = re.search(rf"\b{re.escape(label)}\s*[:.\-–—]\s*", text, flags=re.IGNORECASE)
        if embedded and embedded.start() < 80:
            text = text[embedded.end():]
    text = re.sub(r"^(?:(?:Figure|Fig\.|Table)\s*\d+[A-Za-z]?\s*[:.\-–—]?\s*)+", "", text, flags=re.IGNORECASE)
    return text.strip(" \t\r\n-:;,.")


def canonical_name_key(value: str) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = re.sub(r"\s*\([^)]*\)", "", text).strip()
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def display_name(value: str) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    parenthetical = re.match(r"^([^()]+?)\s*\([^)]*\)\s*$", text)
    return parenthetical.group(1).strip() if parenthetical else text


def list_names(items: list[dict[str, Any]], key: str, *, max_items: int = 5) -> str:
    names = []
    seen: set[str] = set()
    for item in items:
        value = item.get(key)
        name = display_name(str(value or ""))
        name_key = canonical_name_key(name)
        if name and name_key and name_key not in seen:
            names.append(name)
            seen.add(name_key)
        if len(names) >= max_items:
            break
    return ", ".join(names)


@lru_cache(maxsize=8)
def load_topic_assignments(path_value: str = "") -> dict[str, dict[str, str]]:
    mapping: dict[str, dict[str, str]] = {}
    path_raw = (path_value or DEFAULT_TOPIC_ASSIGNMENTS).strip()
    if not path_raw:
        return mapping
    path = Path(path_raw).expanduser()
    if not path.is_file():
        return mapping
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            fid = str(obj.get("openreview_forum_id") or "").strip()
            if not fid:
                continue
            mapping[fid] = {
                "root_id": str(obj.get("root_id") or "").strip(),
                "root_label": str(obj.get("root_label") or "").strip(),
                "subtopic_id": str(obj.get("subtopic_id") or "").strip(),
                "subtopic_label": str(obj.get("subtopic_label") or "").strip(),
            }
    return mapping


def default_topic_assignments_path(conf_year: str) -> str:
    if normalize_conf_year_slug(conf_year) != "ICLR_2026":
        return ""
    candidates = [
        REPO_ROOT / "_private" / "topic_priority" / "subtopic_batches" / "iclr26_fine_assignments.jsonl",
        REPO_ROOT / "_private" / "topic_priority" / "iclr26_topic_assignments.jsonl",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return ""


def topic_text_for_note(openreview_forum_id: str, conf_year: str, topic_assignments: str = "") -> str:
    assignments_path = topic_assignments or DEFAULT_TOPIC_ASSIGNMENTS or default_topic_assignments_path(conf_year)
    info = load_topic_assignments(assignments_path).get(openreview_forum_id or "", {})
    tags = topic_tags_from_assignment(info)
    return format_topic_tags(tags) if tags else ""


def venue_year_tag(conf_year: str) -> str:
    slug = normalize_conf_year_slug(conf_year)
    match = re.fullmatch(r"(.+?)_((?:19|20)\d{2})", slug)
    if not match:
        return safe_slug(slug or conf_year).upper()
    venue, year = match.groups()
    venue = "arxiv" if venue.lower() == "arxiv" else venue.upper()
    return f"{venue}_{year}"


def is_venue_year_topic_tag(tag: str) -> bool:
    text = str(tag or "").strip().removeprefix("#")
    return bool(re.fullmatch(r"topic/[^/\s]+_((?:19|20)\d{2})", text))


def topic_tags_from_text(topic_text: str | None) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for raw in re.findall(r"#topic/[^\s,;|]+", topic_text or ""):
        tag = raw.strip().removeprefix("#").strip()
        if not tag or is_venue_year_topic_tag(tag) or tag in seen:
            continue
        seen.add(tag)
        tags.append(tag)
    return tags


def format_topic_text_for_table(topic_text: str | None) -> str:
    tags = topic_tags_from_text(topic_text)
    return " ".join(f"#{tag}" for tag in tags)


def topic_tags_for_frontmatter(topic_text: str | None, conf_year: str) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for tag in [venue_year_tag(conf_year), *topic_tags_from_text(topic_text)]:
        if not tag or tag in seen:
            continue
        seen.add(tag)
        tags.append(tag)
        if len(tags) >= 5:
            break
    return tags


def frontmatter_tags_from_note(note: str) -> list[str]:
    in_tags = False
    tags: list[str] = []
    for line in note.splitlines():
        if line.strip() == "tags:":
            in_tags = True
            continue
        if in_tags:
            if line.startswith("- "):
                tag = line[2:].strip().strip("'\"").removeprefix("#")
                if tag:
                    tags.append(tag)
                continue
            if line and not line.startswith((" ", "\t")):
                break
    return tags


def topic_text_from_existing_note(note_path: Path) -> str:
    if not note_path.exists():
        return ""
    try:
        note = note_path.read_text(encoding="utf-8")
    except OSError:
        return ""
    tags = [tag for tag in frontmatter_tags_from_note(note) if tag.startswith("topic/") and not is_venue_year_topic_tag(tag)]
    if not tags:
        return ""
    return " ".join(f"#{tag}" for tag in tags[:4])


def analysis_topic_fallback_text(title: str, analysis: dict[str, Any], conf_year: str) -> str:
    """Derive topic tags for non-OpenReview papers without prior note metadata."""
    metadata = frontmatter_metadata_values(title, analysis)
    method = (analysis.get("method") or {}).get("proposed_method_name") or ""
    experiments = analysis.get("experiments") or {}
    datasets = list_names(experiments.get("main_results") or [], "benchmark", max_items=6)
    source = " ".join(
        str(part or "")
        for part in [
            title,
            method,
            metadata.get("core_operator"),
            metadata.get("primary_logic"),
            datasets,
            conf_year,
        ]
    ).lower()
    rules: list[tuple[str, tuple[str, ...]]] = [
        (
            "topic/vision_multimodal_applications",
            (
                "vision",
                "visual",
                "image",
                "video",
                "storyboard",
                "sketch",
                "cartoon",
                "character",
                "human",
                "motion",
                "pose",
                "keyframe",
                "3d",
                "camera",
                "render",
                "reconstruction",
            ),
        ),
        (
            "topic/vision_multimodal_applications/image_and_video_generation",
            (
                "video generation",
                "text-to-video",
                "image-to-video",
                "storyboard",
                "multi-shot",
                "cartoon video",
                "motion video",
                "reenactment",
                "animation",
            ),
        ),
        (
            "topic/vision_multimodal_applications/3d_rendering_reconstruction",
            (
                "3d",
                "skeleton",
                "human motion",
                "motion capture",
                "mocap",
                "pose",
                "keyframe",
                "root trajectory",
                "in-betweening",
                "rendering",
                "reconstruction",
            ),
        ),
        (
            "topic/generative_models_diffusion",
            (
                "diffusion",
                "flow matching",
                "rectified flow",
                "denoise",
                "generative",
                "generation",
                "latent",
                "score",
            ),
        ),
        (
            "topic/generative_models_diffusion/diffusion_image_video",
            (
                "video diffusion",
                "image-to-video",
                "text-to-video",
                "diffusion model",
                "latent diffusion",
                "mmdm",
                "motion diffusion",
            ),
        ),
        (
            "topic/representation_self_supervised_transfer",
            (
                "representation",
                "embedding",
                "self-supervised",
                "transfer",
                "adapter",
                "disentangle",
                "alignment",
                "feature",
            ),
        ),
        (
            "topic/benchmarks_datasets_evaluation",
            (
                "benchmark",
                "dataset",
                "evaluation",
                "metric",
                "user study",
                "leaderboard",
            ),
        ),
    ]
    tags: list[str] = []
    for tag, keywords in rules:
        if any(keyword in source for keyword in keywords) and tag not in tags:
            tags.append(tag)
    if not tags:
        tags.append("topic/other_unclear")
    return " ".join(f"#{tag}" for tag in tags[:4])


def title_aliases(title: str, method: str) -> list[str]:
    aliases: list[str] = []
    for value in (method, title):
        value = compact_text(value, max_len=120)
        if not value:
            continue
        match = re.match(r"^\s*([A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*)\s*[:：]", value)
        if match:
            aliases.append(match.group(1))
            continue
        tokens = re.findall(r"[A-Za-z0-9]+", value)
        acronym = "".join(token[0].upper() for token in tokens if token and token.lower() not in {"a", "an", "the", "of", "for", "to", "and", "with", "via", "in", "on"})
        if 2 <= len(acronym) <= 12:
            aliases.append(acronym)
    out: list[str] = []
    for alias in aliases:
        if alias and alias.lower() not in title.lower() or alias in title:
            if alias not in out and len(alias) <= 32 and not re.search(r"[\u4e00-\u9fff]", alias):
                out.append(alias)
    return out[:3] or [safe_slug(title, max_len=16)]


def claims_for_frontmatter(analysis: dict[str, Any], *, max_items: int = 4, fallback: str = "") -> list[str]:
    claims: list[str] = []
    truth = analysis.get("analysis_truth") or {}
    for item in truth.get("decisive_evidence") or []:
        if isinstance(item, dict):
            claim = compact_text(item.get("claim"), max_len=180)
            if claim and claim not in claims:
                claims.append(claim)
    for item in (analysis.get("experiments") or {}).get("main_results") or []:
        benchmark = compact_text(item.get("benchmark"), max_len=80)
        metric = compact_text(item.get("metric"), max_len=60)
        proposed = compact_text(item.get("proposed"), max_len=60)
        if benchmark and metric and proposed:
            claim = f"{benchmark} 上 {metric} = {proposed}"
            if claim not in claims:
                claims.append(claim)
    core = compact_text(truth.get("core_insight"), max_len=180)
    if core and core not in claims:
        claims.append(core)
    fallback_claim = compact_text(fallback, max_len=180)
    if fallback_claim and fallback_claim not in claims:
        claims.append(fallback_claim)
    return claims[:max_items]


def first_sentence(text: str, *, max_len: int = 220) -> str:
    text = compact_text(text, max_len=max_len * 2)
    if not text:
        return ""
    match = re.search(r"(.+?[。.!?])(?:\s|$)", text)
    return compact_text(match.group(1) if match else text, max_len=max_len)


def fallback_method_name(title: str, analysis: dict[str, Any]) -> str:
    metadata = analysis.get("paper_metadata") or {}
    source = compact_text(metadata.get("title") or title, max_len=180)
    if ":" in source:
        prefix = source.split(":", 1)[0].strip()
        if 2 <= len(prefix) <= 80:
            return prefix
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9-]*", source)
    for token in tokens:
        if 2 <= len(token) <= 32 and any(ch.isupper() for ch in token):
            return token
    return source


def frontmatter_metadata_values(title: str, analysis: dict[str, Any]) -> dict[str, str]:
    method = compact_text((analysis.get("method") or {}).get("proposed_method_name"), max_len=180)
    method = method or fallback_method_name(title, analysis)
    truth = analysis.get("analysis_truth") or {}
    core = compact_text(truth.get("core_insight"), max_len=420)
    causal_knob = compact_text(truth.get("causal_knob"), max_len=180)
    real_bottleneck = compact_text(truth.get("real_bottleneck"), max_len=260)
    claims = claims_for_frontmatter(analysis)
    claim_sentence = first_sentence(claims[0], max_len=180) if claims else ""
    core_operator = compact_text(causal_knob or method or claim_sentence or title, max_len=180)
    primary_logic = compact_text(core or real_bottleneck or method or claim_sentence or title, max_len=420)
    return {
        "method": method,
        "core_operator": core_operator,
        "primary_logic": primary_logic,
    }


def preferred_chinese_title(title: str, analysis: dict[str, Any]) -> str:
    paper_metadata = analysis.get("paper_metadata") or {}
    title_zh = compact_text(paper_metadata.get("title_zh"), max_len=500)
    if title_zh:
        return title_zh
    return title


def canonical_metric_from_part_analyses(
    part_results: list[dict[str, Any]],
    benchmark: str,
    proposed: str,
    baseline: str,
    delta: str,
) -> str:
    benchmark = str(benchmark or "").strip()
    proposed = str(proposed or "").strip()
    baseline = str(baseline or "").strip()
    delta = str(delta or "").strip()
    for part in part_results:
        for item in part.get("experiment_evidence") or []:
            item_benchmark = str(item.get("claim") or "")
            item_metric = str(item.get("metric") or "").strip()
            item_value = str(item.get("value") or "").strip()
            if not item_metric:
                continue
            if delta and item_value and item_value != delta:
                continue
            haystacks = [item_benchmark, str(item.get("table_or_figure") or "")]
            if benchmark and not any(benchmark in hay for hay in haystacks):
                continue
            claim = str(item.get("claim") or "")
            if proposed and proposed not in claim:
                continue
            if baseline and baseline not in claim:
                continue
            return item_metric
    return ""


def preserve_core_metric_terms(
    analysis: dict[str, Any],
    part_results: list[dict[str, Any]],
) -> dict[str, Any]:
    experiments = analysis.get("experiments")
    if not isinstance(experiments, dict):
        return analysis
    main_results = experiments.get("main_results")
    if not isinstance(main_results, list):
        return analysis
    updated_results: list[dict[str, Any]] = []
    for item in main_results:
        if not isinstance(item, dict):
            updated_results.append(item)
            continue
        updated = dict(item)
        canonical_metric = canonical_metric_from_part_analyses(
            part_results,
            benchmark=str(item.get("benchmark") or ""),
            proposed=str(item.get("proposed") or ""),
            baseline=str(item.get("baseline") or ""),
            delta=str(item.get("delta") or ""),
        )
        if canonical_metric:
            updated["metric"] = canonical_metric
        updated_results.append(updated)
    experiments["main_results"] = updated_results
    analysis["experiments"] = experiments
    return analysis


def load_json_if_exists(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def normalize_latex_delimiters(markdown: str) -> str:
    def block_repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        return f"\n$$\n{inner}\n$$\n"

    def inline_repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        return f"${inner}$"

    markdown = re.sub(r"\\{1,2}\(([^$\n]*?)\$", inline_repl, markdown)
    markdown = re.sub(r"\$([^\\\n]*?)\\{1,2}\)", inline_repl, markdown)
    markdown = re.sub(r"\\{1,2}\[(.*?)\\{1,2}\]", block_repl, markdown, flags=re.DOTALL)
    markdown = re.sub(r"\\{1,2}\((.*?)\\{1,2}\)", inline_repl, markdown, flags=re.DOTALL)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def normalize_report_markdown(report: str) -> str:
    report = re.sub(r"<!--.*?-->\s*", "", report, flags=re.DOTALL).strip()
    report = re.sub(r"^# .+?\n+", "", report)
    replacements = {
        "Overview": "概述",
        "Background and Motivation": "背景与动机",
        "Core Innovation": "核心创新",
        "Framework": "整体框架",
        "Key Modules and Formulas": "核心模块与公式推导",
        "Experiments and Analysis": "实验与分析",
        "Lineage and Knowledge Positioning": "方法谱系与知识库定位",
    }
    for english, chinese in replacements.items():
        report = re.sub(
            rf"^##\s*(?:\d+\.\s*)?{re.escape(english)}\s*$",
            f"## {chinese}",
            report,
            flags=re.MULTILINE,
        )
    report = re.sub(r"^##\s*(\d+)\.\s*", "## ", report, flags=re.MULTILINE)
    report = normalize_latex_delimiters(report)
    return report.strip()


def section_keywords(section_title: str) -> tuple[str, ...]:
    mapping = {
        "概述": ("abstract", "introduction", "conclusion", "summary", "overview", "benchmark", "result"),
        "背景与动机": ("abstract", "introduction", "motivation", "related", "background", "benchmark", "dataset"),
        "核心创新": ("method", "algorithm", "benchmark", "dataset", "propose", "new", "lid", "idr", "ms"),
        "整体框架": ("method", "framework", "pipeline", "overview", "algorithm", "dataset", "benchmark"),
        "核心模块与公式推导": ("method", "algorithm", "formula", "equation", "manifold", "transform", "lid", "ess", "lidl", "flipd"),
        "实验与分析": ("experiment", "result", "table", "figure", "benchmark", "mae", "performance", "estimate", "ablation"),
        "方法谱系与知识库定位": ("limitation", "future", "related", "discussion", "conclusion", "open", "baseline"),
    }
    return mapping.get(section_title, ())


def compact_evidence_item(item: Any, *, max_len: int = 220) -> Any:
    if not isinstance(item, dict):
        return item
    return {
        key: compact_text(value, max_len=max_len) if isinstance(value, str) else value
        for key, value in item.items()
        if key not in {"_meta", "_aggregate"}
    }


def slim_part_analysis(part: dict[str, Any], *, max_items: int = 3) -> dict[str, Any]:
    slim = {
        "part_id": part.get("part_id") or part.get("_meta", {}).get("part_id") or "",
        "section_role": compact_text(part.get("section_role"), max_len=240),
    }
    for key in ["method_evidence", "experiment_evidence", "formula_evidence", "figure_table_roles", "open_questions"]:
        value = part.get(key)
        if isinstance(value, list):
            slim[key] = [compact_evidence_item(item) for item in value[:max_items]]
        else:
            slim[key] = []
    return slim


def part_matches_section(part: dict[str, Any], section_title: str) -> bool:
    if section_title == "实验与分析" and (part.get("experiment_evidence") or part.get("figure_table_roles")):
        return True
    if section_title == "核心模块与公式推导" and (part.get("formula_evidence") or part.get("method_evidence")):
        return True
    keywords = section_keywords(section_title)
    if not keywords:
        return True
    text = json.dumps(slim_part_analysis(part), ensure_ascii=False).lower()
    return any(keyword in text for keyword in keywords)


def focused_part_analyses(
    section_title: str,
    part_results: list[dict[str, Any]],
    *,
    max_parts: int = 6,
    max_evidence_items: int = 2,
) -> list[dict[str, Any]]:
    selected = [part for part in part_results if part_matches_section(part, section_title)]
    if section_title == "概述":
        selected = (part_results[:4] + part_results[-2:]) if len(part_results) > 6 else part_results
    if not selected:
        selected = part_results[:max_parts]
    return [slim_part_analysis(part, max_items=max_evidence_items) for part in selected[:max_parts]]


def source_extension(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        return suffix
    return ".jpg"


def image_mime_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    if suffix == ".webp":
        return "image/webp"
    return "image/jpeg"


def copy_vault_figures(
    figures_tables: list[dict[str, Any]],
    *,
    task_id: str,
    asset_root: Path,
) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    target_dir = asset_root / task_id / "figures"
    source_paths = {
        Path(str(item.get("source_path"))).expanduser().resolve()
        for item in figures_tables
        if item.get("source_path")
    }
    if target_dir.exists():
        for stale in target_dir.iterdir():
            if (
                stale.is_file()
                and stale.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
                and stale.resolve() not in source_paths
            ):
                stale.unlink()
    for index, item in enumerate(figures_tables, 1):
        source_value = item.get("source_path") or ""
        if not source_value:
            continue
        source = Path(str(source_value))
        if not source.exists() or not source.is_file():
            continue
        label = safe_slug(str(item.get("label") or item.get("type") or "figure"), max_len=48)
        filename = f"{index:03d}_{label}{source_extension(source)}"
        target = target_dir / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
        copied_item = dict(item)
        copied_item["item_id"] = str(item.get("item_id") or f"item_{index:03d}")
        copied_item["vault_asset_path"] = target.resolve()
        copied_item["note_image_path"] = format_note_image_path(task_id, filename)
        copied.append(copied_item)
    return copied


def format_note_image_path(task_id: str, filename: str) -> str:
    return f"assets/figures/papers/{task_id}/figures/{filename}"


def format_obsidian_image_embed(path: str) -> str:
    return f"![[{path}]]"


def image_block(item: dict[str, Any]) -> str:
    label = str(item.get("label") or "Figure")
    caption = compact_text(dedupe_caption_prefix(label, str(item.get("caption") or "")), max_len=700)
    path = str(item.get("note_image_path") or "")
    if not path:
        return ""
    if caption:
        return f"{format_obsidian_image_embed(path)}\n*{label}: {caption}*"
    return format_obsidian_image_embed(path)


def placement_candidates(figures_tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = []
    for index, item in enumerate(figures_tables, 1):
        try:
            cluster_size = int(item.get("cluster_size") or 0)
        except (TypeError, ValueError):
            cluster_size = 0
        full_region_source = str(item.get("full_region_source") or "")
        candidates.append({
            "item_id": str(item.get("item_id") or f"item_{index:03d}"),
            "label": str(item.get("label") or ""),
            "type": str(item.get("type") or ""),
            "caption": compact_text(dedupe_caption_prefix(str(item.get("label") or ""), str(item.get("caption") or "")), max_len=260),
            "visual_summary": compact_text(item.get("visual_summary"), max_len=260),
            "visual_type": str(item.get("visual_type") or ""),
            "placement_hint": str(item.get("placement_hint") or ""),
            "is_sample_only": bool(item.get("is_sample_only")),
            "cluster_size": cluster_size,
            "full_region_source": full_region_source,
            "is_full_region": full_region_source == "pdf_crop" and cluster_size > 1,
        })
    return candidates


def sample_only_figure(item: dict[str, Any]) -> bool:
    if str(item.get("type") or "").lower() != "figure":
        return False
    text = f"{item.get('label') or ''} {item.get('caption') or ''}".lower()
    sample_words = ("sample", "samples", "few samples", "dataset")
    result_words = ("result", "estimate", "performance", "accuracy", "plot")
    return any(word in text for word in sample_words) and not any(word in text for word in result_words)


METHOD_FIGURE_PATTERN = re.compile(
    r"\b("
    r"framework|pipeline|architecture|overview|method|module|model|tokenizer|"
    r"representation|mask|masking|denois\w*|sampling|guidance|diffusion|"
    r"latent|training|train|encoder|decoder|quantiz\w*|hfsq|fsq|blc|ldcfg"
    r")\b",
    flags=re.IGNORECASE,
)

FRAMEWORK_FIGURE_PATTERN = re.compile(
    r"\b(framework|pipeline|architecture|overall|system)\b",
    flags=re.IGNORECASE,
)

EXPERIMENT_FIGURE_PATTERN = re.compile(
    r"\b(result|estimate|estimation|performance|experiment|benchmark|ablation|study|comparison|metric|jitter|fid|mae|mpjpe|lid)\b",
    flags=re.IGNORECASE,
)

ALLOWED_FIGURE_PLACEMENT_SECTIONS = {"整体框架", "核心模块与公式推导", "实验与分析"}


def placement_text(item: dict[str, Any]) -> str:
    return f"{item.get('label') or ''} {item.get('caption') or ''} {item.get('visual_summary') or ''}"


def method_figure_section(item: dict[str, Any]) -> str:
    text = placement_text(item)
    return "整体框架" if FRAMEWORK_FIGURE_PATTERN.search(text) else "核心模块与公式推导"


def fallback_figure_placements(figures_tables: list[dict[str, Any]], *, max_images: int) -> list[dict[str, str]]:
    if max_images <= 0:
        return []
    candidates = placement_candidates(figures_tables)
    by_id = {item["item_id"]: item for item in candidates}
    placements: list[dict[str, str]] = []
    used: set[str] = set()
    method_image_budget = min(max_images, 4)

    full_region_candidates = [item for item in candidates if item.get("is_full_region")]
    full_region_candidates.sort(key=lambda item: (sample_only_figure(item), item["item_id"]))
    for item in full_region_candidates:
        if len(placements) >= max_images:
            break
        text = placement_text(item)
        section = (
            method_figure_section(item)
            if item.get("type", "").lower() == "figure"
            and METHOD_FIGURE_PATTERN.search(text)
            else "实验与分析"
        )
        placements.append({
            "item_id": item["item_id"],
            "section": section,
            "reason": "complete multi-panel crop from MinerU PDF recrop",
        })
        used.add(item["item_id"])

    for item in candidates:
        if len(placements) >= max_images:
            break
        method_count = sum(1 for placement in placements if placement.get("section") in {"整体框架", "核心模块与公式推导"})
        if method_count >= method_image_budget:
            break
        text = placement_text(item)
        if item["item_id"] in used:
            continue
        if sample_only_figure(item):
            continue
        if item.get("type", "").lower() == "figure" and METHOD_FIGURE_PATTERN.search(text):
            placements.append({
                "item_id": item["item_id"],
                "section": method_figure_section(item),
                "reason": "caption indicates a framework or method-module diagram",
            })
            used.add(item["item_id"])

    experiment_candidates = [
        item for item in candidates
        if item["item_id"] not in used
        and not sample_only_figure(item)
        and (
            item.get("type", "").lower() == "table"
            or EXPERIMENT_FIGURE_PATTERN.search(placement_text(item))
        )
    ]
    experiment_candidates.sort(key=lambda item: (0 if item.get("type", "").lower() == "table" else 1, item["item_id"]))
    for item in experiment_candidates:
        if len(placements) >= max_images:
            break
        if item["item_id"] not in by_id:
            continue
        placements.append({"item_id": item["item_id"], "section": "实验与分析", "reason": "caption indicates a table or result plot"})
        used.add(item["item_id"])
    return placements[:max_images]


def normalize_figure_placements(
    parsed: dict[str, Any],
    figures_tables: list[dict[str, Any]],
    *,
    max_images: int,
) -> list[dict[str, str]]:
    valid_ids = {item["item_id"] for item in placement_candidates(figures_tables)}
    raw_items = parsed.get("placements")
    if not isinstance(raw_items, list):
        return []
    placements: list[dict[str, str]] = []
    used: set[str] = set()
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("item_id") or "")
        section = str(item.get("section") or "")
        if item_id not in valid_ids or item_id in used or section not in ALLOWED_FIGURE_PLACEMENT_SECTIONS:
            continue
        placements.append({
            "item_id": item_id,
            "section": section,
            "reason": compact_text(item.get("reason"), max_len=180),
        })
        used.add(item_id)
        if len(placements) >= max_images:
            break
    return placements


def figure_items_with_ids(figures_tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for index, item in enumerate(figures_tables, 1):
        copied = dict(item)
        copied["item_id"] = str(copied.get("item_id") or f"item_{index:03d}")
        out.append(copied)
    return out


def visual_summary_candidates(figures_tables: list[dict[str, Any]], *, max_items: int) -> list[dict[str, Any]]:
    if max_items <= 0:
        return []
    scored: list[tuple[int, int, dict[str, Any]]] = []
    for index, item in enumerate(figures_tables, 1):
        text = f"{item.get('label') or ''} {item.get('caption') or ''}".lower()
        score = 0
        if str(item.get("type") or "").lower() == "table":
            score += 4
        if re.search(r"\b(result|estimate|estimation|performance|experiment|benchmark|lid|summary|mae)\b", text):
            score += 5
        if re.search(r"\b(framework|pipeline|architecture|overview|method)\b", text):
            score += 3
        if sample_only_figure(item):
            score -= 5
        if score > 0:
            scored.append((-score, index, item))
    scored.sort()
    return [item for _, _, item in scored[:max_items]]


def focused_figures_tables(section_title: str, figures_tables: list[dict[str, Any]], *, max_items: int = 10) -> list[dict[str, Any]]:
    candidates = placement_candidates(figures_tables)
    if section_title == "整体框架":
        filtered = [
            item for item in candidates
            if item.get("placement_hint") == "整体框架"
            or re.search(r"\b(framework|pipeline|architecture|overview|method)\b", f"{item.get('label') or ''} {item.get('caption') or ''} {item.get('visual_summary') or ''}".lower())
        ]
    elif section_title == "实验与分析":
        filtered = [
            item for item in candidates
            if item.get("placement_hint") == "实验与分析"
            or item.get("type", "").lower() == "table"
            or re.search(r"\b(result|estimate|estimation|performance|experiment|benchmark|mae|lid)\b", f"{item.get('label') or ''} {item.get('caption') or ''} {item.get('visual_summary') or ''}".lower())
        ]
    else:
        filtered = candidates
    if not filtered:
        filtered = candidates
    return filtered[:max_items]


def normalize_visual_summary(parsed: dict[str, Any]) -> dict[str, Any]:
    summary = compact_text(parsed.get("visual_summary"), max_len=500)
    visual_type = compact_text(parsed.get("visual_type"), max_len=80)
    elements = parsed.get("key_visible_elements")
    claims = parsed.get("supports_claims")
    hint = str(parsed.get("placement_hint") or "")
    if hint not in {"整体框架", "实验与分析", "skip"}:
        hint = ""
    confidence = parsed.get("confidence")
    try:
        confidence_value = float(confidence)
    except (TypeError, ValueError):
        confidence_value = 0.0
    return {
        "visual_summary": summary,
        "visual_type": visual_type,
        "is_sample_only": bool(parsed.get("is_sample_only")),
        "key_visible_elements": [compact_text(item, max_len=120) for item in elements[:6]] if isinstance(elements, list) else [],
        "supports_claims": [compact_text(item, max_len=160) for item in claims[:4]] if isinstance(claims, list) else [],
        "placement_hint": hint,
        "visual_confidence": confidence_value,
    }


def caption_only_visual_summary(item: dict[str, Any]) -> dict[str, Any]:
    label = str(item.get("label") or "")
    caption = compact_text(dedupe_caption_prefix(label, str(item.get("caption") or "")), max_len=500)
    hint = "skip" if sample_only_figure(item) else ("实验与分析" if str(item.get("type") or "").lower() == "table" else "")
    return {
        "visual_summary": caption,
        "visual_type": str(item.get("type") or ""),
        "is_sample_only": sample_only_figure(item),
        "key_visible_elements": [],
        "supports_claims": [],
        "placement_hint": hint,
        "visual_confidence": 0.25 if caption else 0.0,
        "visual_summary_provider": "caption_fallback",
    }


async def figure_visual_summary_llm(
    args: argparse.Namespace,
    *,
    item: dict[str, Any],
) -> LLMCallResult:
    from openai import AsyncOpenAI

    if args.figure_provider == "none":
        raise RuntimeError("figure provider is disabled")
    api_key = os.environ.get(args.figure_api_key_env, "")
    if not api_key:
        raise RuntimeError(f"Missing API key env var: {args.figure_api_key_env}")
    source = Path(str(item.get("source_path") or ""))
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"figure image not found: {source}")
    client_kwargs: dict[str, Any] = {"api_key": api_key}
    if args.figure_base_url:
        client_kwargs["base_url"] = args.figure_base_url
    if args.figure_provider == "kimi":
        client_kwargs["default_headers"] = {"User-Agent": "claude-code/1.0"}
    client, http_client = build_async_openai_client(AsyncOpenAI, **client_kwargs)
    try:
        encoded = base64.b64encode(source.read_bytes()).decode("ascii")
        label = str(item.get("label") or "")
        caption = str(item.get("caption") or "")
        prompt = (
            f"Label: {label}\n"
            f"Type: {item.get('type') or ''}\n"
            f"Caption: {caption}\n\n"
            "Return the requested JSON."
        )
        messages = [
            {"role": "system", "content": FIGURE_VISUAL_SUMMARY_SYSTEM},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_mime_type(source)};base64,{encoded}",
                        },
                    },
                ],
            },
        ]
        request: dict[str, Any] = {
            "model": args.figure_model,
            "messages": messages,
            "max_tokens": args.figure_visual_summary_max_tokens,
            "temperature": args.figure_temperature,
            "stream": True,
        }
        if args.figure_provider == "kimi":
            request["extra_body"] = {"thinking": {"type": "disabled"}}
        else:
            request["stream_options"] = {"include_usage": True}
        stream = await client.chat.completions.create(**request)
        chunks: list[str] = []
        finish_reasons: list[str] = []
        stream_chunk_count = 0
        api_usage: dict[str, Any] = {}
        async for chunk in stream:
            stream_chunk_count += 1
            if getattr(chunk, "usage", None) is not None:
                api_usage = normalized_api_usage(getattr(chunk, "usage", None))
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            content = getattr(choice.delta, "content", None)
            if content:
                chunks.append(content)
            if choice.finish_reason:
                finish_reasons.append(choice.finish_reason)
    finally:
        await client.close()
        await http_client.aclose()
    text = "".join(chunks)
    prompt_tokens = estimate_tokens(FIGURE_VISUAL_SUMMARY_SYSTEM) + estimate_tokens(prompt)
    completion_tokens = estimate_tokens(text)
    usage = {
        "provider": args.figure_provider,
        "model": args.figure_model,
        "prompt_tokens_est": prompt_tokens,
        "completion_tokens_est": completion_tokens,
        "reasoning_tokens_est": 0,
        "total_tokens_est": prompt_tokens + completion_tokens,
        "total_with_reasoning_tokens_est": prompt_tokens + completion_tokens,
        "estimated_cost_usd": estimate_cost_usd(args.figure_model, prompt_tokens, completion_tokens),
        "cost_basis": "discounted_estimate_from_local_text_lengths",
    }
    if api_usage:
        usage.update(api_usage)
        api_cost = estimate_cost_usd_from_usage(args.figure_model, {
            "prompt_tokens": api_usage.get("prompt_tokens_api"),
            "completion_tokens": api_usage.get("completion_tokens_api"),
            "prompt_cache_hit_tokens": api_usage.get("prompt_cache_hit_tokens"),
            "prompt_cache_miss_tokens": api_usage.get("prompt_cache_miss_tokens"),
        })
        if api_cost is not None:
            usage["estimated_cost_usd_api"] = api_cost
            usage["cost_basis_api"] = "discounted_estimate_from_api_usage_with_prompt_cache"
    diagnostics = {
        "content_chars": len(text),
        "reasoning_chars": 0,
        "finish_reason": finish_reasons[-1] if finish_reasons else "",
        "finish_reasons": finish_reasons,
        "stream_chunk_count": stream_chunk_count,
        "api_usage_present": bool(api_usage),
    }
    return LLMCallResult(text=text, usage=usage, diagnostics=diagnostics)


async def enrich_figure_visual_summaries(
    args: argparse.Namespace,
    *,
    figures_tables: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    out_path = work_dir / "parse" / "figure_visual_summaries.json"
    raw_dir = work_dir / "parse" / "figure_visual_summaries"
    if args.resume and out_path.exists() and not args.force:
        cached = json.loads(out_path.read_text(encoding="utf-8"))
        return cached.get("figures_tables", figures_tables), cached.get("usage", {})
    items = figure_items_with_ids(figures_tables)
    if args.mock_llm or args.figure_visual_summary_max_items <= 0 or args.figure_provider == "none":
        enriched = []
        for item in items:
            copied = dict(item)
            copied.update(caption_only_visual_summary(copied))
            enriched.append(copied)
        usage = {
            "provider": "none" if args.figure_provider == "none" else "mock",
            "model": "",
            "prompt_tokens_est": 0,
            "completion_tokens_est": 0,
            "reasoning_tokens_est": 0,
            "total_tokens_est": 0,
            "total_with_reasoning_tokens_est": 0,
            "estimated_cost_usd": 0.0,
            "cost_basis": "caption_only_no_llm",
        }
        atomic_write_json(out_path, {"figures_tables": enriched, "usage": usage})
        append_jsonl(progress_path, {"event": "figure_visual_summaries_skipped", "at": now_iso(), "provider": usage["provider"]})
        return enriched, usage

    by_id = {item["item_id"]: item for item in items}
    usage_totals = {
        "provider": args.figure_provider,
        "model": args.figure_model,
        "prompt_tokens_est": 0,
        "completion_tokens_est": 0,
        "reasoning_tokens_est": 0,
        "total_tokens_est": 0,
        "total_with_reasoning_tokens_est": 0,
        "prompt_tokens_api": 0,
        "completion_tokens_api": 0,
        "reasoning_tokens_api": 0,
        "total_tokens_api": 0,
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 0,
        "estimated_cost_usd": 0.0,
        "cost_basis": "sum_of_visual_summary_estimates",
    }
    for item in visual_summary_candidates(items, max_items=args.figure_visual_summary_max_items):
        item_id = item["item_id"]
        raw_path = raw_dir / f"{item_id}.raw.txt"
        try:
            result = await figure_visual_summary_llm(args, item=item)
            atomic_write_text(raw_path, result.text)
            parsed = parse_json_object(result.text, label=f"visual_summary_{item_id}")
            summary = normalize_visual_summary(parsed)
            summary["visual_summary_provider"] = args.figure_provider
            summary["visual_stream_diagnostics"] = result.diagnostics or {}
            by_id[item_id].update(summary)
            usage = result.usage
            for key in [
                "prompt_tokens_est",
                "completion_tokens_est",
                "reasoning_tokens_est",
                "total_tokens_est",
                "total_with_reasoning_tokens_est",
                "prompt_tokens_api",
                "completion_tokens_api",
                "reasoning_tokens_api",
                "total_tokens_api",
                "prompt_cache_hit_tokens",
                "prompt_cache_miss_tokens",
            ]:
                usage_totals[key] += int(usage.get(key) or 0)
            usage_totals["estimated_cost_usd"] += float(usage.get("estimated_cost_usd") or 0.0)
            usage_totals["estimated_cost_usd_api"] = usage_totals.get("estimated_cost_usd_api", 0.0) + float(usage.get("estimated_cost_usd_api") or 0.0)
        except Exception as exc:  # noqa: BLE001
            by_id[item_id].update(caption_only_visual_summary(item))
            by_id[item_id]["visual_summary_error"] = str(exc)
            append_jsonl(progress_path, {"event": "figure_visual_summary_fallback", "at": now_iso(), "item_id": item_id, "error": str(exc)})
    usage_totals["estimated_cost_usd"] = round(usage_totals["estimated_cost_usd"], 6)
    if "estimated_cost_usd_api" in usage_totals:
        usage_totals["estimated_cost_usd_api"] = round(float(usage_totals["estimated_cost_usd_api"]), 6)
        usage_totals["cost_basis_api"] = "sum_of_visual_summary_api_usage_with_prompt_cache"
    enriched = [by_id[item["item_id"]] for item in items]
    atomic_write_json(out_path, {"figures_tables": enriched, "usage": usage_totals})
    append_jsonl(progress_path, {"event": "figure_visual_summaries_done", "at": now_iso(), "count": len([item for item in enriched if item.get("visual_summary")]), "usage": usage_totals})
    return enriched, usage_totals


def inject_after_heading(markdown: str, heading: str, blocks: list[str]) -> str:
    blocks = [block for block in blocks if block.strip()]
    if not blocks:
        return markdown
    injection = "\n\n" + "\n\n".join(blocks) + "\n"
    pattern = re.compile(rf"(^##\s+{re.escape(heading)}\s*$)", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return markdown + f"\n\n## {heading}{injection}"
    insert_at = match.end()
    return markdown[:insert_at] + injection + markdown[insert_at:]


def figure_reference_patterns(item: dict[str, Any]) -> list[re.Pattern[str]]:
    text = f"{item.get('label') or ''} {item.get('caption') or ''}"
    patterns: list[re.Pattern[str]] = []
    seen: set[str] = set()
    for match in re.finditer(r"\b(Fig(?:ure)?\.?|Table)\s*([A-Za-z0-9]+)", text, flags=re.IGNORECASE):
        kind = match.group(1).lower()
        number = match.group(2)
        key = f"{kind}:{number.lower()}"
        if key in seen:
            continue
        seen.add(key)
        if kind.startswith("fig"):
            patterns.append(re.compile(rf"\b(?:Fig\.?|Figure)\s*{re.escape(number)}\b", flags=re.IGNORECASE))
        else:
            patterns.append(re.compile(rf"\bTable\s*{re.escape(number)}\b", flags=re.IGNORECASE))
    return patterns


def figure_reference_keys_for_item(item: dict[str, Any]) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    text = f"{item.get('label') or ''} {item.get('caption') or ''}"
    for match in re.finditer(r"\b(Fig(?:ure)?\.?|Table)\s*([A-Za-z0-9]+)", text, flags=re.IGNORECASE):
        kind = "figure" if match.group(1).lower().startswith("fig") else "table"
        keys.add((kind, match.group(2).lower()))
    return keys


def referenced_figure_table_keys(markdown: str) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for match in re.finditer(r"(?<![A-Za-z])(?:Fig\.?|Figure)\s*([0-9]+[A-Za-z]?)\b", markdown, flags=re.IGNORECASE):
        keys.add(("figure", match.group(1).lower()))
    for match in re.finditer(r"(?<![A-Za-z])Table\s*([0-9]+[A-Za-z]?)\b", markdown, flags=re.IGNORECASE):
        keys.add(("table", match.group(1).lower()))
    return keys


def section_for_referenced_item(markdown: str, item: dict[str, Any]) -> str:
    lines = markdown.splitlines()
    current = ""
    for line in lines:
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip()
        if any(pattern.search(line) for pattern in figure_reference_patterns(item)):
            if current in ALLOWED_FIGURE_PLACEMENT_SECTIONS:
                return current
            break
    if str(item.get("type") or "").lower() == "table":
        return "实验与分析"
    if METHOD_FIGURE_PATTERN.search(placement_text(item)) and not sample_only_figure(item):
        return method_figure_section(item)
    return "实验与分析"


def ensure_referenced_figure_placements(
    placements: list[dict[str, str]],
    *,
    report: str,
    copied_figures: list[dict[str, Any]],
    max_images: int,
) -> list[dict[str, str]]:
    if max_images <= 0:
        return []
    normalized_report = normalize_report_markdown(report)
    referenced = referenced_figure_table_keys(normalized_report)
    if not referenced:
        return placements[:max_images]
    by_id = {str(item.get("item_id") or f"item_{index:03d}"): item for index, item in enumerate(copied_figures, 1)}
    referenced_item_ids = {
        item_id for item_id, item in by_id.items()
        if figure_reference_keys_for_item(item).intersection(referenced)
    }
    used = {str(item.get("item_id") or "") for item in placements}
    merged = [
        placement for placement in placements
        if str(placement.get("item_id") or "") in by_id
    ]
    if len(merged) > max_images:
        referenced_existing = [
            placement for placement in merged
            if str(placement.get("item_id") or "") in referenced_item_ids
        ]
        other_existing = [
            placement for placement in merged
            if str(placement.get("item_id") or "") not in referenced_item_ids
        ]
        merged = (referenced_existing + other_existing)[:max_images]
        used = {str(item.get("item_id") or "") for item in merged}
    for index, item in enumerate(copied_figures, 1):
        item_id = str(item.get("item_id") or f"item_{index:03d}")
        if item_id in used or item_id not in by_id:
            continue
        item_keys = figure_reference_keys_for_item(item)
        if not item_keys.intersection(referenced):
            continue
        if sample_only_figure(item) and str(item.get("type") or "").lower() == "figure":
            continue
        merged.append({
            "item_id": item_id,
            "section": section_for_referenced_item(normalized_report, item),
            "reason": "report explicitly references this figure/table",
        })
        if len(merged) > max_images:
            drop_index = next(
                (
                    idx for idx in range(len(merged) - 1, -1, -1)
                    if str(merged[idx].get("item_id") or "") not in referenced_item_ids
                ),
                None,
            )
            if drop_index is None:
                merged.pop()
            else:
                merged.pop(drop_index)
        used.add(item_id)
    return merged[:max_images]


def section_line_bounds(lines: list[str], heading: str) -> tuple[int, int] | None:
    start = -1
    for index, line in enumerate(lines):
        if re.match(rf"^##\s+{re.escape(heading)}\s*$", line):
            start = index
            break
    if start < 0:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.match(r"^##\s+\S", lines[index]):
            end = index
            break
    return start, end


def block_insert_lines(block: str) -> list[str]:
    return ["", *block.strip().splitlines(), ""]


def find_reference_insert_index(lines: list[str], start: int, end: int, item: dict[str, Any]) -> int | None:
    patterns = figure_reference_patterns(item)
    if not patterns:
        return None
    for index in range(start + 1, end):
        stripped = lines[index].strip()
        if not stripped or stripped.startswith("*") or "![[assets/figures" in stripped:
            continue
        if not any(pattern.search(lines[index]) for pattern in patterns):
            continue
        insert_at = index + 1
        while insert_at < end and lines[insert_at].strip() and not re.match(r"^#{2,6}\s+\S", lines[insert_at]):
            insert_at += 1
        return insert_at
    return None


def inject_figure_items(markdown: str, heading: str, items: list[dict[str, Any]]) -> str:
    items = [item for item in items if str(item.get("note_image_path") or "")]
    if not items:
        return markdown
    lines = markdown.splitlines()
    bounds = section_line_bounds(lines, heading)
    if not bounds:
        blocks = [image_block(item) for item in items]
        return inject_after_heading(markdown, heading, blocks)

    start, end = bounds
    matched: dict[int, list[dict[str, Any]]] = {}
    unmatched: list[dict[str, Any]] = []
    for item in items:
        path = str(item.get("note_image_path") or "")
        if path and any(path in line for line in lines):
            continue
        insert_at = find_reference_insert_index(lines, start, end, item)
        if insert_at is None:
            unmatched.append(item)
            continue
        matched.setdefault(insert_at, []).append(item)

    for insert_at in sorted(matched, reverse=True):
        block_lines: list[str] = []
        for item in matched[insert_at]:
            block = image_block(item)
            if block.strip():
                block_lines.extend(block_insert_lines(block))
        if block_lines:
            lines[insert_at:insert_at] = block_lines

    if unmatched:
        bounds = section_line_bounds(lines, heading)
        if bounds:
            _, end = bounds
            blocks = [image_block(item) for item in unmatched if image_block(item).strip()]
            if blocks:
                supplement = ["", "### 补充图表", "", *("\n\n".join(blocks)).splitlines(), ""]
                lines[end:end] = supplement
    return "\n".join(lines)


def figure_items_for_note(
    copied: list[dict[str, Any]],
    *,
    max_images: int,
    placements: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    if max_images <= 0:
        return {}
    selected = placements if placements is not None else fallback_figure_placements(copied, max_images=max_images)
    by_id = {str(item.get("item_id") or f"item_{index:03d}"): item for index, item in enumerate(copied, 1)}
    items_by_section: dict[str, list[dict[str, Any]]] = {section: [] for section in ALLOWED_FIGURE_PLACEMENT_SECTIONS}
    used: set[str] = set()
    for placement in selected:
        item_id = str(placement.get("item_id") or "")
        if item_id in used or item_id not in by_id:
            continue
        section = str(placement.get("section") or "")
        if section not in ALLOWED_FIGURE_PLACEMENT_SECTIONS:
            section = "实验与分析"
        items_by_section.setdefault(section, []).append(by_id[item_id])
        used.add(item_id)
        if len(used) >= max_images:
            break
    return {section: items for section, items in items_by_section.items() if items}


def render_frontmatter(
    *,
    title: str,
    conf_year: str,
    pdf_ref: str,
    analysis: dict[str, Any],
    theme_bucket: str,
    acceptance: str,
    openreview_forum_id: str = "",
    topic_text: str | None = None,
) -> str:
    venue, year = infer_conf_parts(conf_year)
    metadata = frontmatter_metadata_values(title, analysis)
    method = metadata["method"]
    tags = topic_tags_for_frontmatter(topic_text, conf_year)
    claims = claims_for_frontmatter(analysis, fallback=metadata["primary_logic"] or title)
    aliases = title_aliases(title, method)
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        "type: paper",
        "paper_level: A",
        f"venue: {yaml_scalar(venue)}",
        f"year: {year if year is not None else 'null'}",
        f"pdf_ref: {yaml_scalar(pdf_ref)}",
        "aliases:",
    ]
    lines.extend(f"- {yaml_scalar(alias)}" for alias in aliases)
    lines.extend([
        "tags:",
    ])
    lines.extend(f"- {yaml_scalar(tag)}" for tag in tags)
    if openreview_forum_id:
        lines.append(f"openreview_forum_id: {yaml_scalar(openreview_forum_id)}")
    lines.extend([
        f"core_operator: {yaml_scalar(metadata['core_operator'])}",
        f"primary_logic: {yaml_scalar(metadata['primary_logic'])}",
        "claims:",
    ])
    lines.extend(f"- {yaml_scalar(claim)}" for claim in claims)
    lines.extend([
        "---",
        "",
    ])
    return "\n".join(lines)


def normalize_acceptance(acceptance: str) -> str:
    value = str(acceptance or "").strip()
    normalized = value.lower().replace("_", "-")
    if normalized in {"", "unknown", "accepted", "accept", "main", "conference", "regular", "arxiv"}:
        return ""
    return value


def render_info_table(
    *,
    title: str,
    conf_year: str,
    openreview_forum_id: str,
    paper_link: str,
    acceptance: str,
    analysis: dict[str, Any],
    report: str = "",
    topic_text: str | None = None,
) -> str:
    venue, year = infer_conf_parts(conf_year)
    method = (analysis.get("method") or {}).get("proposed_method_name") or ""
    experiments = analysis.get("experiments") or {}
    datasets = list_names(experiments.get("main_results") or [], "benchmark", max_items=4)
    title_zh = preferred_chinese_title(title, analysis)
    links: list[str] = []
    if paper_link:
        links.append(markdown_link("paper", paper_link))
    elif openreview_forum_id:
        links.append(markdown_link("paper", f"https://openreview.net/forum?id={openreview_forum_id}"))
    all_extra_links = [
        *(analysis.get("source_links") or []),
        *extract_source_links(report, json.dumps(analysis, ensure_ascii=False)),
    ]
    seen_labels: set[str] = {"paper"} if links else set()
    seen_urls: set[str] = {
        normalize_extracted_url(url)
        for url in [paper_link, f"https://openreview.net/forum?id={openreview_forum_id}" if openreview_forum_id else ""]
        if url
    }
    for item in all_extra_links:
        if not isinstance(item, dict):
            continue
        url = normalize_extracted_url(str(item.get("url") or ""))
        label = classify_link(str(item.get("label") or ""), url) or str(item.get("label") or "").strip()
        if label not in {"Project", "Code", "arXiv"}:
            continue
        if not url or url in seen_urls or link_is_paper_url(url, paper_link, openreview_forum_id):
            continue
        if label.lower() in seen_labels:
            continue
        seen_urls.add(url)
        seen_labels.add(label.lower())
        links.append(markdown_link(label, url))
    link = " · ".join(links)
    topic = format_topic_text_for_table(topic_text or topic_text_for_note(openreview_forum_id, conf_year))
    venue_text = f"{venue} {year}" if year else venue
    acceptance_label = acceptance_info_table_label(acceptance)
    if acceptance_label and venue_text:
        venue_text = f"{venue_text} ({acceptance_label})"
    rows = [
        ("中文题名", title_zh),
        ("英文题名", title),
        ("会议/期刊", venue_text),
        ("Links", link),
        ("Topic", topic),
        ("Method", method),
        ("Dataset", datasets),
    ]
    out = ["| 字段 | 内容 |", "|------|------|"]
    out.extend(f"| {table_cell(key)} | {table_cell(value)} |" for key, value in rows)
    return "\n".join(out)


def acceptance_info_table_label(acceptance: str) -> str:
    value = str(acceptance or "").strip()
    if not value:
        return ""
    normalized = value.lower().replace("_", "-")
    if normalized in {"unknown", "accepted", "accept", "main", "conference"}:
        return ""
    special = {
        "oral",
        "poster",
        "highlight",
        "spotlight",
        "notable",
        "award",
        "best-paper",
        "honorable-mention",
    }
    return value if normalized in special else ""


def render_effect_callout(analysis: dict[str, Any]) -> str:
    lines = ["> [!tip] 效果简介"]
    grouped: dict[str, list[str]] = {}
    for item in (analysis.get("experiments") or {}).get("main_results") or []:
        benchmark = compact_text(item.get("benchmark"), max_len=80)
        metric = compact_text(item.get("metric"), max_len=80)
        proposed = compact_text(item.get("proposed"), max_len=80)
        if not benchmark or not metric or not proposed:
            continue
        baseline = compact_text(item.get("baseline"), max_len=80)
        delta = compact_text(item.get("delta"), max_len=80)
        metric_text = f"{metric} {proposed}"
        if baseline:
            metric_text += f" vs {baseline}"
        if delta:
            metric_text += f" ({delta})"
        grouped.setdefault(benchmark, []).append(metric_text)
        if len(grouped) >= 3:
            break
    for benchmark, metrics in grouped.items():
        lines.append(f"> - {benchmark} 上，" + "；".join(metrics[:3]) + "。")
    if len(lines) > 1:
        return "\n".join(lines)
    claim_pattern = re.compile(
        r"\d|提升|提高|改善|下降|降低|优于|超过|metric|score|accuracy|precision|recall|f1|auc|ap|psnr|ssim|fid|mse|mae",
        flags=re.IGNORECASE,
    )
    for item in (analysis.get("analysis_truth") or {}).get("decisive_evidence") or []:
        if not isinstance(item, dict):
            continue
        claim = compact_text(item.get("claim"), max_len=220)
        if claim and claim_pattern.search(claim):
            lines.append(f"> - {claim}")
        if len(lines) >= 4:
            break
    return "\n".join(lines) if len(lines) > 1 else ""


def compose_vault_note(
    *,
    title: str,
    conf_year: str,
    pdf_ref: str,
    openreview_forum_id: str,
    paper_link: str,
    acceptance: str,
    theme_bucket: str,
    analysis: dict[str, Any],
    report: str,
    copied_figures: list[dict[str, Any]],
    max_images: int,
    topic_text: str | None = None,
    figure_placements: list[dict[str, Any]] | None = None,
) -> str:
    acceptance = normalize_acceptance(acceptance)
    core = compact_text((analysis.get("analysis_truth") or {}).get("core_insight"), max_len=900)
    if not core:
        core = frontmatter_metadata_values(title, analysis)["primary_logic"]
    body = normalize_report_markdown(report)
    figure_items_by_section = figure_items_for_note(
        copied_figures,
        max_images=max_images,
        placements=figure_placements,
    )
    for section in ("整体框架", "核心模块与公式推导", "实验与分析"):
        body = inject_figure_items(body, section, figure_items_by_section.get(section, []))
    parts = [
        render_frontmatter(
            title=title,
            conf_year=conf_year,
            pdf_ref=pdf_ref,
            openreview_forum_id=openreview_forum_id,
            analysis=analysis,
            theme_bucket=theme_bucket,
            acceptance=acceptance,
            topic_text=topic_text,
        ),
        f"# {title}",
        "",
        "> [!tip] 核心洞察",
        f"> {core}",
        "",
        render_info_table(
            title=title,
            conf_year=conf_year,
            openreview_forum_id=openreview_forum_id,
            paper_link=paper_link,
            acceptance=acceptance,
            analysis=analysis,
            report=report,
            topic_text=topic_text,
        ),
    ]
    effect = render_effect_callout(analysis)
    if effect:
        parts.extend(["", effect])
    if body:
        parts.extend(["", body])
    if pdf_ref:
        parts.extend(["", "## 原文 PDF", "", f"![[{pdf_ref}]]", ""])
    return normalize_latex_delimiters("\n".join(parts))


def parse_frontmatter_block(note: str) -> tuple[dict[str, str], bool]:
    if not note.startswith("---\n"):
        return {}, False
    end = note.find("\n---", 4)
    if end == -1:
        return {}, False
    frontmatter = note[4:end].strip("\n")
    values: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values, True


def table_rows_with_aliased_wikilinks(note: str) -> list[int]:
    rows: list[int] = []
    for line_no, line in enumerate(note.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and re.search(r"\[\[[^\]]+\|[^\]]+\]\]", stripped):
            rows.append(line_no)
    return rows


def incomplete_effect_callout_lines(note: str) -> list[int]:
    lines = note.splitlines()
    bad: list[int] = []
    in_effect = False
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("> [!tip]"):
            in_effect = "效果简介" in stripped
            continue
        if in_effect:
            if not stripped:
                continue
            if not stripped.startswith(">"):
                break
            if re.search(r"\s为\s*(?:[。。，；;]|,(?!\d)|\.(?!\d)|$)", stripped):
                bad.append(line_no)
    return bad


def strip_figure_caption_lines(note: str) -> str:
    return "\n".join(
        line
        for line in note.splitlines()
        if not (
            line.startswith("*")
            and re.search(r"^\*(?:Figure|Fig\.?|Table)\s+\d+", line, flags=re.IGNORECASE)
        )
    )


def dangling_numeric_refs(note: str, *, max_items: int | None = 12) -> list[str]:
    scan = re.sub(r"`[^`\n]*`", "", note)
    scan = re.sub(r"\$\$.*?\$\$", "", scan, flags=re.DOTALL)
    scan = re.sub(r"\$[^$\n]*\$", "", scan)
    scan = strip_figure_caption_lines(scan)
    refs = sorted(
        set(match.group(1) for match in re.finditer(r"(?<![\w\}'!\]])\[(\d{1,3})\](?!\()", scan)),
        key=lambda value: int(value),
    )
    if not refs:
        return []
    defined = set(re.findall(r"^\s*\[(\d{1,3})\]:", scan, flags=re.MULTILINE))
    bibliography = set(re.findall(r"^\s*\[(\d{1,3})\]\s+", scan, flags=re.MULTILINE))
    dangling = [ref for ref in refs if ref not in defined and ref not in bibliography]
    return dangling if max_items is None else dangling[:max_items]


def remove_dangling_numeric_refs_from_segment(
    segment: str,
    refs: set[str],
    counts: dict[str, int],
) -> str:
    if not refs:
        return segment

    def ref_repl(match: re.Match[str]) -> str:
        ref = match.group(1)
        if ref not in refs:
            return match.group(0)
        counts[ref] = counts.get(ref, 0) + 1
        return ""

    cleaned = re.sub(r"(?<![\w\}'!\]])\[(\d{1,3})\](?!\()", ref_repl, segment)
    if cleaned != segment:
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
        cleaned = re.sub(r"\s+([,.;:，。；：])", r"\1", cleaned)
        cleaned = re.sub(r"([（(])\s*([）)])", "", cleaned)
    return cleaned


def sanitize_dangling_numeric_refs(note: str) -> tuple[str, dict[str, Any]]:
    refs = set(dangling_numeric_refs(note, max_items=None))
    counts: dict[str, int] = {}
    if not refs:
        return note, {"changed": False, "removed_refs": [], "removed_count": 0}

    sanitized_lines: list[str] = []
    in_fence = False
    in_math_block = False
    for line in note.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("```"):
            sanitized_lines.append(line)
            in_fence = not in_fence
            continue
        if stripped == "$$":
            sanitized_lines.append(line)
            in_math_block = not in_math_block
            continue
        if in_fence or in_math_block or (
            line.startswith("*")
            and re.search(r"^\*(?:Figure|Fig\.?|Table)\s+\d+", line, flags=re.IGNORECASE)
        ):
            sanitized_lines.append(line)
            continue

        parts = re.split(r"(`[^`\n]*`|\$[^$\n]*\$)", line)
        sanitized_lines.append(
            "".join(
                part
                if part.startswith(("`", "$"))
                else remove_dangling_numeric_refs_from_segment(part, refs, counts)
                for part in parts
            )
        )

    sanitized = "".join(sanitized_lines)
    removed_refs = sorted(counts, key=lambda value: int(value))
    return sanitized, {
        "changed": sanitized != note,
        "removed_refs": removed_refs,
        "removed_count": sum(counts.values()),
    }


def validate_vault_note(
    note: str,
    *,
    pdf_ref: str,
    openreview_forum_id: str = "",
    copied_figures: list[dict[str, Any]],
    figure_placements: list[dict[str, Any]] | None = None,
    max_images: int = 0,
) -> dict[str, Any]:
    frontmatter, has_frontmatter = parse_frontmatter_block(note)
    required_frontmatter = [
        "title",
        "type",
        "paper_level",
        "venue",
        "year",
        "pdf_ref",
        "tags",
        "core_operator",
        "primary_logic",
        "claims",
    ]
    required_sections = [title for title, _ in SECTION_SPECS] + ["原文 PDF"]
    headings = set(re.findall(r"^##\s+(.+?)\s*$", note, flags=re.MULTILINE))
    missing_frontmatter = [key for key in required_frontmatter if key not in frontmatter]
    missing_sections = [section for section in required_sections if section not in headings]
    expected_pdf_embed = f"![[{pdf_ref}]]" if pdf_ref else ""
    selected = figure_placements if figure_placements is not None else fallback_figure_placements(copied_figures, max_images=max_images)
    by_id = {str(item.get("item_id") or f"item_{index:03d}"): item for index, item in enumerate(copied_figures, 1)}
    note_image_paths: list[str] = []
    for placement in selected:
        item = by_id.get(str(placement.get("item_id") or ""))
        image_path = str((item or {}).get("note_image_path") or "")
        if image_path:
            note_image_paths.append(image_path)
        if max_images > 0 and len(note_image_paths) >= max_images:
            break
    expected_image_embeds = [format_obsidian_image_embed(path) for path in note_image_paths]
    missing_images = [
        path for path, embed in zip(note_image_paths, expected_image_embeds, strict=False)
        if embed not in note
    ]
    referenced_keys = referenced_figure_table_keys(note)
    referenced_assets: list[dict[str, str]] = []
    for index, item in enumerate(copied_figures, 1):
        if not figure_reference_keys_for_item(item).intersection(referenced_keys):
            continue
        image_path = str(item.get("note_image_path") or "")
        if image_path:
            referenced_assets.append({
                "label": str(item.get("label") or ""),
                "path": image_path,
            })
    missing_referenced_images = [
        item for item in referenced_assets
        if format_obsidian_image_embed(item["path"]) not in note
    ]
    legacy_markdown_image_links = re.findall(r"!\[[^\]]*\]\((?:\.\./\.\./)?assets/[^)]+\)", note)
    legacy_relative_wikilink_images = re.findall(r"!\[\[\.\./\.\./assets/[^\]]+\]\]", note)
    scalar_metadata_keys = set(required_frontmatter) - {"aliases", "tags", "claims"}
    fallback_frontmatter_values = {}
    for key, value in frontmatter.items():
        if key not in scalar_metadata_keys:
            continue
        if value in {"", '""', "null"} or "待人工" in value:
            fallback_frontmatter_values[key] = value
        elif value in {"unknown", "Unknown"}:
            fallback_frontmatter_values[key] = value
    fallback_markers = [
        f"{key}: {value}"
        for key, value in fallback_frontmatter_values.items()
    ]
    fallback_markers.extend(
        f"line {line_no}: {line.strip()}"
        for line_no, line in enumerate(note.splitlines()[:80], 1)
        if "待人工复核" in line
    )
    forum_id_value = frontmatter.get("openreview_forum_id", "").strip().strip("\"'")
    forum_id_ok = not openreview_forum_id or forum_id_value == openreview_forum_id
    frontmatter_tags = frontmatter_tags_from_note(note)
    expected_venue_tag = venue_year_tag(pdf_ref.split("/")[-2] if "/" in pdf_ref else "")
    venue_tag_ok = not expected_venue_tag or expected_venue_tag in frontmatter_tags
    legacy_venue_topic_tags = [tag for tag in frontmatter_tags if is_venue_year_topic_tag(tag)]
    missing_referenced_images_blocking = (
        missing_referenced_images
        and max_images > 0
        and len(note_image_paths) < max_images
    )
    checks = {
        "frontmatter_valid": has_frontmatter and not missing_frontmatter,
        "openreview_forum_id_present": forum_id_ok,
        "required_sections_present": not missing_sections,
        "pdf_embed_present": not pdf_ref or expected_pdf_embed in note,
        "image_embeds_present": not note_image_paths or not missing_images,
        "referenced_image_embeds_present": not missing_referenced_images_blocking,
        "no_legacy_markdown_image_links": not legacy_markdown_image_links and not legacy_relative_wikilink_images,
        "no_pdf_file_label": "PDF 文件：" not in note,
        "no_table_cell_aliased_wikilinks": not table_rows_with_aliased_wikilinks(note),
        "no_fallback_metadata_markers": not fallback_markers,
        "no_dangling_numeric_refs": not dangling_numeric_refs(note),
        "no_incomplete_effect_callout": not incomplete_effect_callout_lines(note),
        "venue_year_tag_present": venue_tag_ok,
        "no_legacy_venue_topic_tags": not legacy_venue_topic_tags,
        "note_length_ok": len(note.strip()) >= 1000,
    }
    return {
        "ok": all(checks.values()),
        "checks": checks,
        "note_chars": len(note),
        "missing_frontmatter": missing_frontmatter,
        "expected_openreview_forum_id": openreview_forum_id,
        "openreview_forum_id": forum_id_value,
        "missing_sections": missing_sections,
        "pdf_ref": pdf_ref,
        "image_embed_count": len(re.findall(r"!\[\[assets/figures/papers/[^\]]+\]\]", note)),
        "expected_image_count": len(note_image_paths),
        "missing_image_paths": missing_images[:12],
        "missing_referenced_images": missing_referenced_images[:12],
        "legacy_markdown_image_links": legacy_markdown_image_links[:12],
        "legacy_relative_wikilink_images": legacy_relative_wikilink_images[:12],
        "pdf_file_label_count": note.count("PDF 文件："),
        "table_cell_aliased_wikilink_lines": table_rows_with_aliased_wikilinks(note),
        "fallback_markers": fallback_markers,
        "dangling_numeric_refs": dangling_numeric_refs(note),
        "incomplete_effect_callout_lines": incomplete_effect_callout_lines(note),
        "expected_venue_year_tag": expected_venue_tag,
        "frontmatter_tags": frontmatter_tags,
        "legacy_venue_topic_tags": legacy_venue_topic_tags,
    }


def note_check_repair_prompt(
    *,
    note: str,
    figure_placements: list[dict[str, Any]] | None,
    copied_figures: list[dict[str, Any]],
) -> str:
    prompt_obj = {
        "note_markdown": note,
        "figure_placements": figure_placements or [],
        "placed_figure_table_metadata": [
            {
                "item_id": str(item.get("item_id") or ""),
                "label": str(item.get("label") or ""),
                "type": str(item.get("type") or ""),
                "caption": compact_text(dedupe_caption_prefix(str(item.get("label") or ""), str(item.get("caption") or "")), max_len=500),
                "visual_summary": compact_text(item.get("visual_summary"), max_len=500),
                "placement_hint": str(item.get("placement_hint") or ""),
                "is_sample_only": bool(item.get("is_sample_only")),
                "note_image_path": str(item.get("note_image_path") or ""),
            }
            for item in copied_figures
            if any(str(item.get("item_id") or "") == str(placement.get("item_id") or "") for placement in (figure_placements or []))
        ],
        "repair_scope": "Only fix Markdown formatting, duplicated captions, broken table syntax, and obvious image-placement mismatch.",
        "frontmatter_schema_guard": "Do not add category, modalities, or frontier. Keep aliases as short English/model aliases.",
    }
    return json.dumps(prompt_obj, ensure_ascii=False, indent=2)


async def maybe_kimi_check_repair_note(
    args: argparse.Namespace,
    *,
    note: str,
    figure_placements: list[dict[str, Any]] | None,
    copied_figures: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> tuple[str, dict[str, Any]]:
    if args.mock_llm or not args.kimi_check_repair:
        return note, {}
    prompt = note_check_repair_prompt(
        note=note,
        figure_placements=figure_placements,
        copied_figures=copied_figures,
    )
    atomic_write_text(work_dir / "prompts" / "kimi_note_check_repair.prompt.txt", prompt)
    try:
        result = await kimi_llm_text(
            args,
            system=KIMI_NOTE_CHECK_REPAIR_SYSTEM,
            prompt=prompt,
            max_tokens=args.kimi_check_repair_max_tokens,
        )
        raw = result.text.strip()
        atomic_write_text(work_dir / "report" / "kimi_note_check_repair.raw.md", raw)
        if raw.startswith("```"):
            first_newline = raw.find("\n")
            raw = raw[first_newline + 1:] if first_newline != -1 else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3].rstrip()
        repaired = raw.strip()
        if repaired.startswith("---") and "# " in repaired and len(repaired) > len(note) * 0.6:
            usage = usage_from_result(result)
            append_jsonl(progress_path, {"event": "kimi_note_check_repair_done", "at": now_iso(), "usage": usage})
            return repaired + "\n", usage
        append_jsonl(progress_path, {"event": "kimi_note_check_repair_rejected", "at": now_iso(), "reason": "repaired note failed basic shape check"})
    except Exception as exc:  # noqa: BLE001
        append_jsonl(progress_path, {"event": "kimi_note_check_repair_fallback", "at": now_iso(), "error": str(exc)})
    return note, {}


def export_to_vault(
    args: argparse.Namespace,
    *,
    task_id: str,
    title: str,
    work_dir: Path,
    analysis: dict[str, Any],
    report: str,
    figures_tables: list[dict[str, Any]],
    figure_placements: list[dict[str, Any]] | None = None,
    progress_path: Path,
) -> dict[str, Any]:
    vault_root = Path(args.vault_root).expanduser().resolve()
    conf_year = resolved_conf_year(args)
    paper_dir = (
        Path(args.vault_note_dir).expanduser().resolve()
        if args.vault_note_dir
        else vault_root / "analysis" / conf_year
    )
    pdf_dir = vault_root / "paperPDFs" / conf_year
    asset_root = Path(args.vault_asset_root).expanduser().resolve()
    stem = note_file_stem(title)
    note_path = paper_dir / f"{stem}.md"
    source_pdf_arg = args.paper_pdf or args.pdf
    source_pdf, pdf_resolution = resolve_existing_pdf_path(
        source_pdf_arg,
        conf_year=conf_year,
        search_roots=pdf_search_roots_from_args(args),
    )
    if not source_pdf:
        raise FileNotFoundError(
            "Vault export requires an existing PDF. "
            f"input={source_pdf_arg!r}; attempts={pdf_resolution.get('attempts') or []}"
        )
    pdf_target = pdf_dir / f"{stem}.pdf"
    pdf_target.parent.mkdir(parents=True, exist_ok=True)
    if not (pdf_target.exists() and source_pdf.samefile(pdf_target)):
        shutil.copy2(source_pdf, pdf_target)
    pdf_ref = f"paperPDFs/{conf_year}/{pdf_target.name}"

    copied_figures = copy_vault_figures(
        figures_tables,
        task_id=task_id,
        asset_root=asset_root,
    )
    effective_placements = ensure_referenced_figure_placements(
        figure_placements or [],
        report=report,
        copied_figures=copied_figures,
        max_images=args.max_note_images,
    )
    if not analysis.get("source_links"):
        parse_markdown = work_dir / "parse" / "full.md"
        if parse_markdown.exists():
            analysis = dict(analysis)
            analysis["source_links"] = extract_source_links(parse_markdown.read_text(encoding="utf-8"))
    topic_text = topic_text_for_note(args.openreview_forum_id, conf_year, args.topic_assignments)
    if not topic_text:
        topic_text = topic_text_from_existing_note(note_path)
    if not topic_text:
        topic_text = analysis_topic_fallback_text(title, analysis, conf_year)
        append_jsonl(
            progress_path,
            {
                "event": "topic_fallback_applied",
                "at": now_iso(),
                "topic_text": topic_text,
            },
        )
    note = compose_vault_note(
        title=title,
        conf_year=conf_year,
        pdf_ref=pdf_ref,
        openreview_forum_id=args.openreview_forum_id,
        paper_link=args.paper_link,
        acceptance=args.acceptance,
        theme_bucket=args.theme_bucket,
        analysis=analysis,
        report=report,
        copied_figures=copied_figures,
        max_images=args.max_note_images,
        topic_text=topic_text,
        figure_placements=effective_placements,
    )
    note, numeric_ref_sanitizer = sanitize_dangling_numeric_refs(note)
    atomic_write_text(note_path, note)
    validation = validate_vault_note(
        note,
        pdf_ref=pdf_ref,
        openreview_forum_id=args.openreview_forum_id,
        copied_figures=copied_figures,
        figure_placements=effective_placements,
        max_images=args.max_note_images,
    )
    export_info = {
        "note_path": str(note_path),
        "pdf_ref": pdf_ref,
        "acceptance": normalize_acceptance(args.acceptance),
        "source_pdf": str(source_pdf),
        "source_pdf_resolution": pdf_resolution,
        "figure_count": len(copied_figures),
        "figure_placements": effective_placements,
        "asset_root": str(asset_root),
        "numeric_ref_sanitizer": numeric_ref_sanitizer,
        "validation": validation,
    }
    atomic_write_json(work_dir / "report" / "vault_export.json", export_info)
    if not validation.get("ok"):
        raise RuntimeError(f"vault note validation failed: {validation}")
    return export_info


def prepare_parse(args: argparse.Namespace, work_dir: Path) -> dict[str, Any]:
    started = time.monotonic()
    parse_dir = work_dir / "parse"
    parse_dir.mkdir(parents=True, exist_ok=True)

    cached_full = parse_dir / "full.md"
    cached_figures = parse_dir / "figures_tables.json"
    if args.resume and not args.force and cached_full.exists() and cached_figures.exists():
        figures_tables = json.loads(cached_figures.read_text(encoding="utf-8"))
        markdown = cached_full.read_text(encoding="utf-8", errors="ignore")
        return {
            "source_type": "cached_parse",
            "source_markdown": str(cached_full),
            "source_root": str(parse_dir),
            "markdown_chars": len(markdown),
            "figures_tables": figures_tables if isinstance(figures_tables, list) else [],
            "duration_seconds": 0.0,
        }

    if args.source_md:
        source = Path(args.source_md).resolve()
        markdown = source.read_text(encoding="utf-8", errors="ignore")
        content_path = None
        source_root = source.parent
        source_type = "markdown"
    elif args.mineru_output:
        artifacts = find_mineru_artifacts(Path(args.mineru_output).resolve())
        source = artifacts.markdown_path
        markdown = source.read_text(encoding="utf-8", errors="ignore")
        content_path = artifacts.content_list_path
        source_root = artifacts.root
        source_type = "mineru_output"
        if content_path:
            shutil.copy2(content_path, parse_dir / "content_list.json")
    elif args.pdf:
        pdf_path = Path(args.pdf).resolve()
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        cached_output = discover_mineru_output(args, pdf_path)
        if cached_output:
            artifacts = find_mineru_artifacts(cached_output)
            source_type = "mineru_output"
        elif args.require_existing_mineru_output:
            raise FileNotFoundError(f"No existing MinerU output found for PDF: {pdf_path}")
        else:
            artifacts = run_mineru_cli(
                pdf_path=pdf_path,
                output_dir=parse_dir / "mineru_raw",
                mineru_bin=args.mineru_bin,
                backend=args.mineru_backend,
                timeout=args.mineru_timeout,
                model_source=args.mineru_model_source,
                config_path=ensure_mineru_local_config(args),
            )
            source_type = "pdf_mineru"
        source = artifacts.markdown_path
        markdown = source.read_text(encoding="utf-8", errors="ignore")
        content_path = artifacts.content_list_path
        source_root = artifacts.root
        if content_path:
            shutil.copy2(content_path, parse_dir / "content_list.json")
    else:
        raise ValueError("Pass exactly one of --pdf, --mineru-output, or --source-md")

    figures_tables = extract_figures_tables(content_path, source_root=source_root)
    markdown = normalize_markdown_full_region_image_refs(markdown, figures_tables, source_root=source_root)
    atomic_write_text(parse_dir / "full.md", markdown)
    atomic_write_json(parse_dir / "figures_tables.json", figures_tables)
    return {
        "source_type": source_type,
        "source_markdown": str(source),
        "source_root": str(source_root),
        "markdown_chars": len(markdown),
        "figures_tables": figures_tables,
        "duration_seconds": round(time.monotonic() - started, 3),
    }


def resolved_title(args: argparse.Namespace, markdown: str, fallback: str) -> str:
    return args.paper_title.strip() or infer_title(markdown, fallback=fallback)


def write_chunks(chunks: list[Chunk], work_dir: Path) -> None:
    chunk_dir = work_dir / "parse" / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    for chunk in chunks:
        header = (
            f"<!-- part {chunk.index}/{chunk.total} "
            f"chars {chunk.start}-{chunk.end} -->\n\n"
        )
        atomic_write_text(chunk_dir / f"part_{chunk.index:03d}.md", header + chunk.text)
    atomic_write_json(chunk_dir / "index.json", [
        {
            "part_id": f"part_{chunk.index:03d}",
            "index": chunk.index,
            "total": chunk.total,
            "start": chunk.start,
            "end": chunk.end,
            "chars": len(chunk.text),
        }
        for chunk in chunks
    ])


def mock_json(kind: str, *, part_id: str = "") -> dict[str, Any]:
    if kind == "part":
        return {
            "part_id": part_id,
            "section_role": "mock_chunk",
            "method_evidence": [
                {
                    "claim": "Mock method claim from this chunk.",
                    "section": "chunk",
                    "anchor": part_id,
                    "confidence": 0.8,
                }
            ],
            "experiment_evidence": [],
            "formula_evidence": [],
            "figure_table_roles": [],
            "open_questions": [],
        }
    return {
        "paper_metadata": {"title": "Mock Paper", "title_zh": "模拟论文", "venue": None, "year": None},
        "analysis_truth": {
            "real_bottleneck": "Mock bottleneck.",
            "causal_knob": "Mock causal knob.",
            "core_insight": "Mock core insight.",
            "decisive_evidence": [{"claim": "Mock evidence.", "anchor": "part_001", "confidence": 0.8}],
        },
        "method": {
            "proposed_method_name": "MockMethod",
            "baseline_methods": [],
            "changed_slots": [],
            "pipeline_modules": [],
        },
        "experiments": {"main_results": [], "ablations": [], "fairness_notes": []},
        "formulas": [],
        "figures_tables": [],
        "limitations": [],
        "open_questions": [],
    }


def mock_report() -> str:
    return (
        "# Mock Paper\n\n"
        "## Overview\n\n"
        "This is a mock local report generated without an LLM call.\n\n"
        "## Background and Motivation\n\nMock background.\n\n"
        "## Core Innovation\n\nMock innovation.\n\n"
        "## Framework\n\nMock framework.\n\n"
        "## Key Modules and Formulas\n\nMock modules.\n\n"
        "## Experiments and Analysis\n\nMock experiments.\n\n"
        "## Lineage and Knowledge Positioning\n\nMock positioning.\n"
    )


def deepseek_uses_reasoning(model: str) -> bool:
    lowered = model.lower()
    return "reasoner" in lowered or "v4" in lowered


async def call_openai_compatible(
    *,
    system: str,
    prompt: str,
    provider: str,
    model: str,
    base_url: str,
    api_key: str,
    max_tokens: int,
    temperature: float,
    reasoning_effort: str,
    thinking: str,
) -> LLMCallResult:
    from openai import AsyncOpenAI

    client_kwargs: dict[str, Any] = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    if provider == "kimi":
        client_kwargs["default_headers"] = {"User-Agent": "claude-code/1.0"}
    client, http_client = build_async_openai_client(AsyncOpenAI, **client_kwargs)
    try:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
        request: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
        }
        if provider == "kimi":
            request["temperature"] = temperature
            request["extra_body"] = {"thinking": {"type": "disabled"}}
        else:
            request["temperature"] = temperature
            request["stream_options"] = {"include_usage": True}
            if deepseek_uses_reasoning(model):
                request["extra_body"] = {"thinking": {"type": thinking}}
                if thinking == "enabled" and reasoning_effort:
                    request["reasoning_effort"] = reasoning_effort
        stream = await client.chat.completions.create(**request)
        chunks: list[str] = []
        reasoning_chunks: list[str] = []
        finish_reasons: list[str] = []
        stream_chunk_count = 0
        api_usage: dict[str, Any] = {}
        async for chunk in stream:
            stream_chunk_count += 1
            if getattr(chunk, "usage", None) is not None:
                api_usage = normalized_api_usage(getattr(chunk, "usage", None))
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            delta = choice.delta
            content = getattr(delta, "content", None)
            reasoning_content = getattr(delta, "reasoning_content", None)
            if content:
                chunks.append(content)
            if reasoning_content:
                reasoning_chunks.append(reasoning_content)
            if choice.finish_reason:
                finish_reasons.append(choice.finish_reason)
    finally:
        await client.close()
        await http_client.aclose()
    text = "".join(chunks)
    reasoning_text = "".join(reasoning_chunks)
    prompt_tokens = estimate_tokens(system) + estimate_tokens(prompt)
    completion_tokens = estimate_tokens(text)
    reasoning_tokens = estimate_tokens(reasoning_text)
    usage = {
        "provider": provider,
        "model": model,
        "thinking": thinking if provider != "kimi" and deepseek_uses_reasoning(model) else "disabled",
        "reasoning_effort": reasoning_effort if provider != "kimi" and deepseek_uses_reasoning(model) and thinking == "enabled" else "",
        "prompt_tokens_est": prompt_tokens,
        "completion_tokens_est": completion_tokens,
        "reasoning_tokens_est": reasoning_tokens,
        "total_tokens_est": prompt_tokens + completion_tokens,
        "total_with_reasoning_tokens_est": prompt_tokens + completion_tokens + reasoning_tokens,
        "estimated_cost_usd": estimate_cost_usd(model, prompt_tokens, completion_tokens),
        "cost_basis": "discounted_estimate_from_local_text_lengths",
    }
    if api_usage:
        usage.update(api_usage)
        api_cost = estimate_cost_usd_from_usage(model, {
            "prompt_tokens": api_usage.get("prompt_tokens_api"),
            "completion_tokens": api_usage.get("completion_tokens_api"),
            "prompt_cache_hit_tokens": api_usage.get("prompt_cache_hit_tokens"),
            "prompt_cache_miss_tokens": api_usage.get("prompt_cache_miss_tokens"),
        })
        if api_cost is not None:
            usage["estimated_cost_usd_api"] = api_cost
            usage["cost_basis_api"] = "discounted_estimate_from_api_usage_with_prompt_cache"
    diagnostics = {
        "content_chars": len(text),
        "reasoning_chars": len(reasoning_text),
        "finish_reason": finish_reasons[-1] if finish_reasons else "",
        "finish_reasons": finish_reasons,
        "stream_chunk_count": stream_chunk_count,
        "api_usage_present": bool(api_usage),
    }
    return LLMCallResult(text=text, usage=usage, diagnostics=diagnostics)


async def llm_text_with_config(
    *,
    system: str,
    prompt: str,
    provider: str,
    model: str,
    base_url: str,
    api_key_env: str,
    max_tokens: int,
    temperature: float,
    reasoning_effort: str,
    thinking: str,
) -> LLMCallResult:
    api_key = os.environ.get(api_key_env, "")
    if not api_key:
        raise RuntimeError(f"Missing API key env var: {api_key_env}")
    return await call_openai_compatible(
        system=system,
        prompt=prompt,
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        reasoning_effort=reasoning_effort,
        thinking=thinking,
    )


async def llm_text(
    args: argparse.Namespace,
    *,
    system: str,
    prompt: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
    thinking: str | None = None,
) -> LLMCallResult:
    if args.mock_llm:
        raise RuntimeError("mock_llm should be handled by the caller")
    return await llm_text_with_config(
        system=system,
        prompt=prompt,
        provider=args.provider,
        model=args.model,
        base_url=args.base_url,
        api_key_env=args.api_key_env,
        max_tokens=max_tokens,
        temperature=args.temperature,
        reasoning_effort=reasoning_effort if reasoning_effort is not None else args.reasoning_effort,
        thinking=thinking if thinking is not None else args.thinking,
    )


async def writer_llm_text(args: argparse.Namespace, *, system: str, prompt: str, max_tokens: int) -> LLMCallResult:
    if args.mock_llm:
        raise RuntimeError("mock_llm should be handled by the caller")
    return await llm_text_with_config(
        system=system,
        prompt=prompt,
        provider=args.writer_provider,
        model=args.writer_model,
        base_url=args.writer_base_url,
        api_key_env=args.writer_api_key_env,
        max_tokens=max_tokens,
        temperature=args.writer_temperature,
        reasoning_effort=args.writer_reasoning_effort,
        thinking=args.writer_thinking,
    )


async def kimi_llm_text(args: argparse.Namespace, *, system: str, prompt: str, max_tokens: int) -> LLMCallResult:
    if args.mock_llm:
        raise RuntimeError("mock_llm should be handled by the caller")
    return await llm_text_with_config(
        system=system,
        prompt=prompt,
        provider="kimi",
        model=args.kimi_model,
        base_url=args.kimi_base_url,
        api_key_env=args.kimi_api_key_env,
        max_tokens=max_tokens,
        temperature=args.kimi_temperature,
        reasoning_effort="",
        thinking="disabled",
    )


def first_env(names: list[str]) -> tuple[str, str]:
    for name in names:
        value = os.environ.get(name, "")
        if value:
            return name, value
    return "", ""


def normalize_provider_base_url(provider: str, base_url: str) -> str:
    if provider != "kimi" or not base_url:
        return base_url
    normalized = base_url.rstrip("/")
    if not normalized.endswith("/v1"):
        normalized += "/v1"
    return normalized


def resolve_llm_config(args: argparse.Namespace) -> None:
    if not args.part_reasoning_effort:
        args.part_reasoning_effort = args.reasoning_effort
    if args.section_workers <= 0:
        args.section_workers = args.part_workers
    if args.provider == "kimi":
        api_key_env, _ = first_env(["KIMI_API_KEY", "MOONSHOT_API_KEY", "KIMI_AUTH_TOKEN"])
        _, model = first_env(["KIMI_MODEL", "MOONSHOT_MODEL"])
        _, base_url = first_env(["KIMI_BASE_URL", "MOONSHOT_BASE_URL"])
        args.api_key_env = args.api_key_env or api_key_env or "KIMI_API_KEY"
        args.model = args.model or model or "kimi-k2.6"
        args.base_url = normalize_provider_base_url(
            args.provider,
            args.base_url or base_url or KIMI_DEFAULT_BASE_URL,
        )
        if args.temperature == 0.1:
            args.temperature = KIMI_DEFAULT_TEMPERATURE
        return

    _, model = first_env(["DEEPSEEK_MODEL"])
    _, base_url = first_env(["DEEPSEEK_BASE_URL"])
    api_key_env, _ = first_env(["DEEPSEEK_API_KEY", "OPENAI_API_KEY"])
    args.api_key_env = args.api_key_env or api_key_env or "DEEPSEEK_API_KEY"
    args.model = args.model or model or DEFAULT_DEEPSEEK_MODEL
    args.base_url = args.base_url or base_url or "https://api.deepseek.com/v1"


def resolve_mineru_config(args: argparse.Namespace) -> None:
    mineru_cli_path = os.environ.get("MINERU_CLI_PATH", "").strip()
    if mineru_cli_path and args.mineru_bin == "mineru":
        args.mineru_bin = mineru_cli_path
        return
    if args.mineru_bin != "mineru":
        return
    discovered = shutil.which("mineru")
    if discovered:
        args.mineru_bin = discovered
        return
    for candidate in (
        Path.home() / "miniconda3" / "bin" / "mineru",
        Path.home() / ".local" / "bin" / "mineru",
    ):
        if candidate.exists() and candidate.is_file():
            args.mineru_bin = str(candidate)
            return


def resolve_writer_llm_config(args: argparse.Namespace) -> None:
    provider = args.writer_provider or "deepseek"
    args.writer_provider = provider
    if provider == "kimi":
        api_key_env, _ = first_env(["KIMI_API_KEY", "MOONSHOT_API_KEY", "KIMI_AUTH_TOKEN"])
        _, model = first_env(["KIMI_MODEL", "MOONSHOT_MODEL"])
        _, base_url = first_env(["KIMI_BASE_URL", "MOONSHOT_BASE_URL"])
        args.writer_api_key_env = args.writer_api_key_env or api_key_env or "KIMI_API_KEY"
        args.writer_model = args.writer_model or model or "kimi-k2.6"
        args.writer_base_url = normalize_provider_base_url(
            provider,
            args.writer_base_url or base_url or KIMI_DEFAULT_BASE_URL,
        )
        return

    _, model = first_env(["DEEPSEEK_MODEL"])
    _, base_url = first_env(["DEEPSEEK_BASE_URL"])
    api_key_env, _ = first_env(["DEEPSEEK_API_KEY", "OPENAI_API_KEY"])
    args.writer_api_key_env = args.writer_api_key_env or api_key_env or "DEEPSEEK_API_KEY"
    args.writer_model = args.writer_model or model or DEFAULT_DEEPSEEK_MODEL
    args.writer_base_url = args.writer_base_url or base_url or "https://api.deepseek.com/v1"


def resolve_kimi_llm_config(args: argparse.Namespace) -> None:
    api_key_env, _ = first_env(["KIMI_API_KEY", "MOONSHOT_API_KEY", "KIMI_AUTH_TOKEN"])
    _, model = first_env(["KIMI_MODEL", "MOONSHOT_MODEL"])
    _, base_url = first_env(["KIMI_BASE_URL", "MOONSHOT_BASE_URL"])
    args.kimi_api_key_env = args.kimi_api_key_env or api_key_env or "KIMI_API_KEY"
    args.kimi_model = args.kimi_model or model or DEFAULT_KIMI_MODEL
    args.kimi_base_url = normalize_provider_base_url("kimi", args.kimi_base_url or base_url or KIMI_DEFAULT_BASE_URL)


def resolve_figure_llm_config(args: argparse.Namespace) -> None:
    provider = args.figure_provider or "none"
    args.figure_provider = provider
    if provider == "none":
        args.figure_model = ""
        args.figure_base_url = ""
        args.figure_api_key_env = ""
        return
    if provider == "kimi":
        api_key_env, _ = first_env(["KIMI_API_KEY", "MOONSHOT_API_KEY", "KIMI_AUTH_TOKEN"])
        _, model = first_env(["KIMI_MODEL", "MOONSHOT_MODEL"])
        _, base_url = first_env(["KIMI_BASE_URL", "MOONSHOT_BASE_URL"])
        args.figure_api_key_env = args.figure_api_key_env or api_key_env or "KIMI_API_KEY"
        args.figure_model = args.figure_model or model or DEFAULT_KIMI_MODEL
        args.figure_base_url = normalize_provider_base_url("kimi", args.figure_base_url or base_url or KIMI_DEFAULT_BASE_URL)
        if args.figure_temperature == 0.1:
            args.figure_temperature = KIMI_DEFAULT_TEMPERATURE
        return

    api_key_env, _ = first_env(["GPT_API_KEY", "gpt_OPENAI_API_KEY", "OPENAI_API_KEY"])
    _, model = first_env(["GPT_MODEL", "gpt_OPENAI_MODEL", "OPENAI_MODEL"])
    _, base_url = first_env(["GPT_BASE_URL", "gpt_OPENAI_BASE_URL", "OPENAI_BASE_URL"])
    args.figure_api_key_env = args.figure_api_key_env or api_key_env or "OPENAI_API_KEY"
    args.figure_model = args.figure_model or model or DEFAULT_OPENAI_FIGURE_MODEL
    args.figure_base_url = args.figure_base_url or base_url


def part_prompt(chunk: Chunk, title: str) -> str:
    return (
        f"{PART_ANALYSIS_PROMPT_CONTRACT}\n\n"
        "=== VARIABLE PART PAYLOAD ===\n"
        f"Paper title: {title}\n"
        f"Part: {chunk.index}/{chunk.total}\n"
        f"Character span: {chunk.start}-{chunk.end}\n\n"
        "=== PART CONTENT ===\n"
        f"{chunk.text}"
    )


async def run_part_analysis(
    args: argparse.Namespace,
    *,
    chunk: Chunk,
    title: str,
    work_dir: Path,
    progress_path: Path,
) -> dict[str, Any]:
    part_id = f"part_{chunk.index:03d}"
    out_path = work_dir / "part_analysis" / f"{part_id}.json"
    raw_path = work_dir / "part_analysis" / f"{part_id}.raw.txt"
    repair_raw_path = work_dir / "part_analysis" / f"{part_id}.repair.raw.txt"
    prompt_path = work_dir / "prompts" / f"{part_id}.prompt.txt"
    if args.resume and out_path.exists() and not args.force:
        return json.loads(out_path.read_text(encoding="utf-8"))

    prompt = part_prompt(chunk, title)
    atomic_write_text(prompt_path, prompt)
    started = time.monotonic()
    usage: dict[str, Any] = {}
    if args.mock_llm:
        parsed = mock_json("part", part_id=part_id)
        raw = json.dumps(parsed, ensure_ascii=False)
    elif is_appendix_figure_table_chunk(chunk.text):
        parsed = local_anchor_part_analysis(part_id, chunk.text)
        raw = json.dumps(parsed, ensure_ascii=False)
        usage = {
            "provider": "local",
            "model": "deterministic_anchor_extractor",
            "prompt_tokens_est": 0,
            "completion_tokens_est": estimate_tokens(raw),
            "total_tokens_est": estimate_tokens(raw),
            "estimated_cost_usd": 0.0,
            "cost_basis": "local_appendix_figure_table_anchor_extraction",
        }
    else:
        llm_result = await llm_text(
            args,
            system=PART_ANALYSIS_SYSTEM,
            prompt=prompt,
            max_tokens=args.part_max_tokens,
            reasoning_effort=args.part_reasoning_effort,
            thinking=args.part_thinking,
        )
        raw = llm_result.text
        usage = usage_from_result(llm_result)
        if usage_has_finish_reason(usage, "length"):
            primary_length_raw_path = work_dir / "part_analysis" / f"{part_id}.primary_length.raw.txt"
            atomic_write_text(primary_length_raw_path, raw)
            if args.part_max_tokens >= args.adaptive_long_part_max_tokens:
                usage["length_output_accepted"] = True
                append_jsonl(progress_path, {"event": "part_analysis_length_accepted", "part_id": part_id, "at": now_iso(), "usage": usage})
            else:
                retry_tokens = args.adaptive_long_part_max_tokens
                retry_result = await llm_text(
                    args,
                    system=PART_ANALYSIS_SYSTEM,
                    prompt=prompt,
                    max_tokens=retry_tokens,
                    reasoning_effort=args.part_reasoning_effort,
                    thinking=args.part_thinking,
                )
                retry_raw_path = work_dir / "part_analysis" / f"{part_id}.length_retry.raw.txt"
                atomic_write_text(retry_raw_path, retry_result.text)
                retry_usage = usage_from_result(retry_result)
                usage = merge_usage_totals(usage, retry_usage, cost_basis="part_plus_length_retry_estimate")
                usage["length_retry_used"] = True
                usage["length_retry_max_tokens"] = retry_tokens
                usage["primary_stream_diagnostics"] = llm_result.diagnostics or {}
                usage["length_retry_stream_diagnostics"] = retry_usage.get("stream_diagnostics") or {}
                raw = retry_result.text
                if usage_has_finish_reason(retry_usage, "length"):
                    usage["length_retry_output_accepted"] = True
                    append_jsonl(progress_path, {"event": "part_analysis_length_retry_accepted", "part_id": part_id, "at": now_iso(), "usage": usage})
        atomic_write_text(raw_path, raw)
        try:
            parsed = parse_json_object(raw, label=part_id)
        except Exception as first_exc:  # noqa: BLE001
            repair_raw = raw
            repair_errors: list[str] = []
            repair_attempts: list[dict[str, Any]] = []
            parsed = None
            if args.kimi_repair and not args.mock_llm:
                kimi_repair_path = work_dir / "part_analysis" / f"{part_id}.kimi_repair.raw.txt"
                try:
                    kimi_repair = await repair_part_with_kimi(
                        args,
                        part_id=part_id,
                        raw_text=raw,
                        chunk_text=chunk.text,
                        max_tokens=min(args.part_max_tokens, 8192),
                    )
                    repair_raw = kimi_repair.text
                    atomic_write_text(kimi_repair_path, repair_raw)
                    kimi_usage = usage_from_result(kimi_repair)
                    usage = merge_usage_totals(usage, kimi_usage, cost_basis="part_plus_kimi_repair_estimate")
                    usage["kimi_repair_used"] = True
                    usage["repair_used"] = True
                    usage["kimi_repair_usage"] = kimi_usage
                    repair_attempts.append(repair_attempt_summary("kimi", kimi_usage))
                    parsed = parse_json_object(repair_raw, label=f"{part_id}_kimi_repair")
                except Exception as kimi_exc:  # noqa: BLE001
                    repair_errors.append(f"kimi repair: {kimi_exc}")
                    repair_attempts.append(repair_attempt_summary("kimi", usage.get("kimi_repair_usage"), kimi_exc))
            try:
                if parsed is None:
                    repair_prompt = part_repair_prompt(part_id, raw, chunk.text)
                    repair_result = await llm_text(
                        args,
                        system=PART_ANALYSIS_REPAIR_SYSTEM,
                        prompt=repair_prompt,
                        max_tokens=min(args.part_max_tokens, 4096),
                        reasoning_effort=args.part_reasoning_effort,
                        thinking=args.part_thinking,
                    )
                    repair_raw = repair_result.text
                    atomic_write_text(repair_raw_path, repair_raw)
                    repair_usage = usage_from_result(repair_result)
                    usage = merge_usage_totals(usage, repair_usage, cost_basis="part_plus_repair_estimate")
                    usage["repair_used"] = True
                    usage["primary_stream_diagnostics"] = llm_result.diagnostics or {}
                    usage["repair_stream_diagnostics"] = repair_usage.get("stream_diagnostics") or {}
                    repair_attempts.append(repair_attempt_summary(args.provider, repair_usage))
                    parsed = parse_json_object(repair_raw, label=f"{part_id}_repair")
            except Exception as second_exc:  # noqa: BLE001
                repair_errors.append(f"deepseek repair: {second_exc}")
                repair_attempts.append(repair_attempt_summary(args.provider, usage.get("repair_usage"), second_exc))
                usage["repair_used"] = True
                usage["repair_failed"] = True
                usage["repair_errors"] = repair_errors
                usage["repair_attempts"] = repair_attempts
                parsed = part_analysis_fallback(part_id, raw, f"{first_exc}; {'; '.join(repair_errors)}", chunk.text)
            usage["repair_attempts"] = repair_attempts
        parsed = normalize_part_analysis(part_id, parsed)
        if not part_analysis_has_content(parsed):
            usage["empty_part_fallback_used"] = True
            parsed = part_analysis_fallback(part_id, raw, "empty part-analysis JSON", chunk.text)
    parsed.setdefault("part_id", part_id)
    parsed["_meta"] = {
        "part_id": part_id,
        "part_index": chunk.index,
        "part_count": chunk.total,
        "chunk_chars": len(chunk.text),
        "latency_seconds": round(time.monotonic() - started, 3),
        "usage": usage,
    }
    if args.mock_llm:
        atomic_write_text(raw_path, raw)
    elif is_appendix_figure_table_chunk(chunk.text):
        atomic_write_text(raw_path, raw)
    atomic_write_json(out_path, parsed)
    append_jsonl(progress_path, {"event": "part_analysis_done", "part_id": part_id, "at": now_iso(), "usage": usage})
    return parsed


async def run_all_part_analyses(
    args: argparse.Namespace,
    *,
    chunks: list[Chunk],
    title: str,
    work_dir: Path,
    progress_path: Path,
) -> list[dict[str, Any]]:
    sem = asyncio.Semaphore(max(1, args.part_workers))

    async def one(chunk: Chunk) -> dict[str, Any]:
        async with sem:
            return await run_part_analysis(
                args,
                chunk=chunk,
                title=title,
                work_dir=work_dir,
                progress_path=progress_path,
            )

    started = time.monotonic()
    results = await asyncio.gather(*(one(chunk) for chunk in chunks))
    sorted_results = sorted(results, key=lambda item: item.get("_meta", {}).get("part_index", 0))
    total_latency = sum(
        float(item.get("_meta", {}).get("latency_seconds") or 0.0)
        for item in sorted_results
    )
    for item in sorted_results:
        item.setdefault("_aggregate", {})
        item["_aggregate"].update({
            "part_wall_seconds": round(time.monotonic() - started, 3),
            "part_total_llm_seconds": round(total_latency, 3),
        })
    return sorted_results


def compact_paper_context(markdown: str, *, max_chars: int) -> str:
    markdown = markdown.strip()
    if len(markdown) <= max_chars:
        return markdown
    head = max_chars * 2 // 3
    tail = max_chars - head
    return (
        markdown[:head]
        + "\n\n[... middle omitted in main merge prompt; see parse/full.md and part analyses ...]\n\n"
        + markdown[-tail:]
    )


def infer_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines()[:80]:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("#").strip()
    return fallback


async def run_main_analysis(
    args: argparse.Namespace,
    *,
    title: str,
    markdown: str,
    part_results: list[dict[str, Any]],
    figures_tables: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> dict[str, Any]:
    out_path = work_dir / "analysis" / "main_analysis.json"
    raw_path = work_dir / "analysis" / "main_analysis.raw.txt"
    prompt_path = work_dir / "prompts" / "main_analysis.prompt.txt"
    if args.resume and out_path.exists() and not args.force:
        return json.loads(out_path.read_text(encoding="utf-8"))

    prompt_payload = {
        "paper_title": title,
        "paper_context": compact_paper_context(markdown, max_chars=args.main_context_chars),
        "part_analyses": part_results,
        "figures_tables": figures_tables,
    }
    prompt = (
        f"{MAIN_ANALYSIS_PROMPT_CONTRACT}\n\n"
        "=== VARIABLE PAPER PAYLOAD ===\n"
        f"{json.dumps(prompt_payload, ensure_ascii=False, indent=2)}"
    )
    atomic_write_text(prompt_path, prompt)
    started = time.monotonic()
    usage: dict[str, Any] = {}
    if args.mock_llm:
        parsed = mock_json("main")
        parsed["paper_metadata"]["title"] = title
        raw = json.dumps(parsed, ensure_ascii=False)
    else:
        llm_result = await llm_text(
            args,
            system=MAIN_ANALYSIS_SYSTEM,
            prompt=prompt,
            max_tokens=args.main_max_tokens,
            reasoning_effort=args.reasoning_effort,
            thinking=args.thinking,
        )
        raw = llm_result.text
        usage = usage_from_result(llm_result)
        if usage_has_finish_reason(usage, "length") and args.main_length_retry_max_tokens > args.main_max_tokens:
            atomic_write_text(work_dir / "analysis" / "main_analysis.primary_length.raw.txt", raw)
            retry_result = await llm_text(
                args,
                system=MAIN_ANALYSIS_SYSTEM,
                prompt=prompt,
                max_tokens=args.main_length_retry_max_tokens,
                reasoning_effort=args.main_length_retry_reasoning_effort,
                thinking=args.main_length_retry_thinking,
            )
            retry_usage = usage_from_result(retry_result)
            usage = merge_usage_totals(usage, retry_usage, cost_basis="main_plus_length_retry_estimate")
            usage["length_retry_used"] = True
            usage["length_retry_max_tokens"] = args.main_length_retry_max_tokens
            usage["length_retry_reasoning_effort"] = args.main_length_retry_reasoning_effort
            usage["primary_stream_diagnostics"] = llm_result.diagnostics or {}
            usage["length_retry_stream_diagnostics"] = retry_usage.get("stream_diagnostics") or {}
            raw = retry_result.text
            atomic_write_text(work_dir / "analysis" / "main_analysis.length_retry.raw.txt", raw)
        atomic_write_text(raw_path, raw)
        try:
            parsed = parse_json_object(raw, label="main_analysis")
        except Exception as first_exc:  # noqa: BLE001
            repair_result = await llm_text(
                args,
                system=MAIN_ANALYSIS_REPAIR_SYSTEM,
                prompt=main_repair_prompt(raw),
                max_tokens=min(args.main_max_tokens, 4096),
                reasoning_effort=args.reasoning_effort,
                thinking=args.thinking,
            )
            repair_raw = repair_result.text
            atomic_write_text(work_dir / "analysis" / "main_analysis.repair.raw.txt", repair_raw)
            repair_usage = usage_from_result(repair_result)
            usage = merge_usage_totals(usage, repair_usage, cost_basis="main_plus_repair_estimate")
            usage["repair_used"] = True
            usage["primary_stream_diagnostics"] = llm_result.diagnostics or {}
            usage["repair_stream_diagnostics"] = repair_usage.get("stream_diagnostics") or {}
            try:
                parsed = parse_json_object(repair_raw, label="main_analysis_repair")
            except Exception as second_exc:  # noqa: BLE001
                usage["repair_failed"] = True
                usage["fallback_used"] = True
                error = f"main_analysis repair failed: {first_exc}; repair: {second_exc}"
                append_jsonl(progress_path, {"event": "main_analysis_fallback", "at": now_iso(), "error": error, "usage": usage})
                parsed = main_analysis_fallback(title, part_results, figures_tables, error, raw)
    parsed = normalize_main_analysis(title, parsed, source_links=extract_source_links(markdown))
    parsed["_meta"] = {
        "part_count": len(part_results),
        "latency_seconds": round(time.monotonic() - started, 3),
        "created_at": now_iso(),
        "usage": usage,
    }
    parsed = preserve_core_metric_terms(parsed, part_results)
    atomic_write_text(raw_path, raw)
    atomic_write_json(out_path, parsed)
    append_jsonl(progress_path, {"event": "main_analysis_done", "at": now_iso(), "usage": usage})
    return parsed


async def run_writer(
    args: argparse.Namespace,
    *,
    analysis: dict[str, Any],
    part_results: list[dict[str, Any]],
    figures_tables: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> tuple[str, float]:
    out_path = work_dir / "report" / "final_report.md"
    raw_path = work_dir / "report" / "writer.raw.md"
    prompt_path = work_dir / "prompts" / "writer.prompt.txt"
    if args.resume and out_path.exists() and not args.force:
        return out_path.read_text(encoding="utf-8"), 0.0

    prompt_obj = {
        "main_analysis": analysis,
        "part_analyses": part_results,
        "figures_tables": figures_tables,
    }
    prompt = json.dumps(prompt_obj, ensure_ascii=False, indent=2)
    atomic_write_text(prompt_path, prompt)
    started = time.monotonic()
    if args.mock_llm:
        report = mock_report()
    else:
        llm_result = await writer_llm_text(args, system=WRITER_SYSTEM, prompt=prompt, max_tokens=args.writer_max_tokens)
        report = llm_result.text
    if not report.strip():
        raise RuntimeError("writer returned empty report")
    report = normalize_latex_delimiters(report)
    writer_seconds = round(time.monotonic() - started, 3)
    header = (
        "<!-- generated_by: run_local_paper_analysis.py -->\n"
        f"<!-- generated_at: {now_iso()} -->\n"
        f"<!-- writer_latency_seconds: {writer_seconds} -->\n\n"
    )
    atomic_write_text(raw_path, report)
    atomic_write_text(out_path, header + report.strip() + "\n")
    append_jsonl(progress_path, {"event": "writer_done", "at": now_iso()})
    return header + report.strip() + "\n", writer_seconds


def build_section_prompt(
    *,
    section_title: str,
    section_goal: str,
    analysis: dict[str, Any],
    part_results: list[dict[str, Any]],
    figures_tables: list[dict[str, Any]],
    max_part_contexts: int = 6,
    max_evidence_items: int = 2,
    max_figure_contexts: int = 10,
) -> str:
    focused_parts = focused_part_analyses(
        section_title,
        part_results,
        max_parts=max(1, max_part_contexts),
        max_evidence_items=max(1, max_evidence_items),
    )
    focused_figures = focused_figures_tables(
        section_title,
        figures_tables,
        max_items=max(1, max_figure_contexts),
    )
    prompt_obj = {
        "verified_analysis": analysis,
        "focused_part_analyses": focused_parts,
        "focused_figures_tables": focused_figures,
        "context_note": "Part and figure/table context is filtered for this section; use verified_analysis for global facts.",
        "section_title": section_title,
        "section_goal": section_goal,
    }
    return json.dumps(prompt_obj, ensure_ascii=False, indent=2)


def build_figure_placement_prompt(
    *,
    analysis: dict[str, Any],
    report: str,
    figures_tables: list[dict[str, Any]],
    max_images: int,
) -> str:
    prompt_obj = {
        "image_budget": max_images,
        "verified_analysis": analysis,
        "report_excerpt": compact_text(normalize_report_markdown(report), max_len=12000),
        "figure_table_candidates": placement_candidates(figures_tables),
    }
    return json.dumps(prompt_obj, ensure_ascii=False, indent=2)


async def run_figure_placement(
    args: argparse.Namespace,
    *,
    analysis: dict[str, Any],
    report: str,
    copied_figures: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    out_path = work_dir / "report" / "figure_placements.json"
    raw_path = work_dir / "report" / "figure_placements.raw.txt"
    prompt_path = work_dir / "prompts" / "figure_placement.prompt.txt"
    if args.resume and out_path.exists() and not args.force:
        cached = json.loads(out_path.read_text(encoding="utf-8"))
        placements = cached.get("placements") if isinstance(cached, dict) else []
        if isinstance(placements, list):
            placements = ensure_referenced_figure_placements(
                placements,
                report=report,
                copied_figures=copied_figures,
                max_images=args.max_note_images,
            )
        else:
            placements = []
        return placements, cached.get("usage", {}) if isinstance(cached, dict) else {}

    if args.max_note_images <= 0:
        atomic_write_json(out_path, {"placements": [], "usage": {}})
        return [], {}

    prompt = build_figure_placement_prompt(
        analysis=analysis,
        report=report,
        figures_tables=copied_figures,
        max_images=args.max_note_images,
    )
    atomic_write_text(prompt_path, prompt)
    raw = ""
    usage: dict[str, Any] = {}
    placements: list[dict[str, str]] = []
    if args.mock_llm or args.figure_provider == "none":
        placements = fallback_figure_placements(copied_figures, max_images=args.max_note_images)
    else:
        try:
            llm_result = await llm_text_with_config(
                system=FIGURE_PLACEMENT_SYSTEM,
                prompt=prompt,
                provider=args.figure_provider,
                model=args.figure_model,
                base_url=args.figure_base_url,
                api_key_env=args.figure_api_key_env,
                max_tokens=args.figure_placement_max_tokens,
                temperature=args.figure_temperature,
                reasoning_effort="",
                thinking="disabled",
            )
            raw = llm_result.text
            usage = usage_from_result(llm_result)
            atomic_write_text(raw_path, raw)
            parsed = parse_json_object(raw, label="figure_placement")
            placements = normalize_figure_placements(parsed, copied_figures, max_images=args.max_note_images)
        except Exception as exc:
            append_jsonl(progress_path, {"event": "figure_placement_fallback", "at": now_iso(), "error": str(exc)})
    if not placements:
        placements = fallback_figure_placements(copied_figures, max_images=args.max_note_images)
    placements = ensure_referenced_figure_placements(
        placements,
        report=report,
        copied_figures=copied_figures,
        max_images=args.max_note_images,
    )
    atomic_write_json(out_path, {"placements": placements, "usage": usage})
    append_jsonl(progress_path, {"event": "figure_placement_done", "at": now_iso(), "count": len(placements), "usage": usage})
    return placements, usage


async def run_section_writer(
    args: argparse.Namespace,
    *,
    section_title: str,
    section_goal: str,
    analysis: dict[str, Any],
    part_results: list[dict[str, Any]],
    figures_tables: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> tuple[str, float, dict[str, Any]]:
    section_id = safe_slug(section_title, max_len=48)
    out_path = work_dir / "report" / "sections" / f"{section_id}.md"
    raw_path = work_dir / "report" / "sections" / f"{section_id}.raw.md"
    prompt_path = work_dir / "prompts" / f"writer_{section_id}.prompt.txt"
    if args.resume and out_path.exists() and not args.force:
        return out_path.read_text(encoding="utf-8"), 0.0, {}

    prompt = build_section_prompt(
        section_title=section_title,
        section_goal=section_goal,
        analysis=analysis,
        part_results=part_results,
        figures_tables=figures_tables,
        max_part_contexts=args.writer_context_max_parts,
        max_evidence_items=args.writer_context_max_items,
        max_figure_contexts=args.writer_figure_context_max_items,
    )
    atomic_write_text(prompt_path, prompt)
    started = time.monotonic()
    usage: dict[str, Any] = {}
    if args.mock_llm:
        text = f"## {section_title}\n\n待人工补充。\n"
    else:
        llm_result = await writer_llm_text(args, system=SECTION_WRITER_SYSTEM, prompt=prompt, max_tokens=args.writer_max_tokens)
        text = llm_result.text
        usage = usage_from_result(llm_result)
        if not text.strip() and args.kimi_repair and args.writer_provider != "kimi":
            append_jsonl(progress_path, {
                "event": "section_writer_empty_retry",
                "section": section_title,
                "at": now_iso(),
                "provider": args.writer_provider,
                "usage": usage,
            })
            kimi_result = await kimi_llm_text(
                args,
                system=SECTION_WRITER_SYSTEM,
                prompt=prompt,
                max_tokens=args.writer_max_tokens,
            )
            kimi_usage = usage_from_result(kimi_result)
            usage = merge_usage_totals(usage, kimi_usage, cost_basis="section_writer_plus_kimi_retry_estimate")
            usage["kimi_retry_used"] = True
            usage["kimi_retry_usage"] = kimi_usage
            text = kimi_result.text
    if not text.strip():
        raise RuntimeError(f"section writer returned empty output: {section_title}")
    elapsed = round(time.monotonic() - started, 3)
    atomic_write_text(raw_path, text)
    atomic_write_text(out_path, text.strip() + "\n")
    append_jsonl(progress_path, {"event": "section_writer_done", "section": section_title, "at": now_iso(), "usage": usage})
    return out_path.read_text(encoding="utf-8"), elapsed, usage


async def run_section_writers(
    args: argparse.Namespace,
    *,
    analysis: dict[str, Any],
    part_results: list[dict[str, Any]],
    figures_tables: list[dict[str, Any]],
    work_dir: Path,
    progress_path: Path,
) -> tuple[list[str], float, float, dict[str, Any]]:
    sem = asyncio.Semaphore(max(1, args.section_workers))

    async def one(spec: tuple[str, str]) -> tuple[str, float, dict[str, Any]]:
        title, goal = spec
        async with sem:
            return await run_section_writer(
                args,
                section_title=title,
                section_goal=goal,
                analysis=analysis,
                part_results=part_results,
                figures_tables=figures_tables,
                work_dir=work_dir,
                progress_path=progress_path,
            )

    started = time.monotonic()
    results = await asyncio.gather(*(one(spec) for spec in SECTION_SPECS))
    sections = [text for text, _, _ in results]
    total_llm = round(sum(seconds for _, seconds, _ in results), 3)
    wall = round(time.monotonic() - started, 3)
    usage_rollup = {
        "provider": args.writer_provider,
        "model": args.writer_model,
        "prompt_tokens_est": sum((usage.get("prompt_tokens_est") or 0) for _, _, usage in results),
        "completion_tokens_est": sum((usage.get("completion_tokens_est") or 0) for _, _, usage in results),
        "reasoning_tokens_est": sum((usage.get("reasoning_tokens_est") or 0) for _, _, usage in results),
        "total_tokens_est": sum((usage.get("total_tokens_est") or 0) for _, _, usage in results),
        "total_with_reasoning_tokens_est": sum((usage.get("total_with_reasoning_tokens_est") or 0) for _, _, usage in results),
        "prompt_tokens_api": sum((usage.get("prompt_tokens_api") or 0) for _, _, usage in results),
        "completion_tokens_api": sum((usage.get("completion_tokens_api") or 0) for _, _, usage in results),
        "reasoning_tokens_api": sum((usage.get("reasoning_tokens_api") or 0) for _, _, usage in results),
        "total_tokens_api": sum((usage.get("total_tokens_api") or 0) for _, _, usage in results),
        "prompt_cache_hit_tokens": sum((usage.get("prompt_cache_hit_tokens") or 0) for _, _, usage in results),
        "prompt_cache_miss_tokens": sum((usage.get("prompt_cache_miss_tokens") or 0) for _, _, usage in results),
        "cached_tokens_api": sum((usage.get("cached_tokens_api") or 0) for _, _, usage in results),
        "estimated_cost_usd": round(sum((usage.get("estimated_cost_usd") or 0.0) for _, _, usage in results), 6),
        "cost_basis": "sum_of_section_writer_estimates",
    }
    if any(usage.get("estimated_cost_usd_api") is not None for _, _, usage in results):
        usage_rollup["estimated_cost_usd_api"] = round(
            sum((usage.get("estimated_cost_usd_api") or 0.0) for _, _, usage in results),
            6,
        )
        usage_rollup["cost_basis_api"] = "sum_of_section_writer_api_usage_with_prompt_cache"
    rate = cache_hit_rate(
        int(usage_rollup["prompt_cache_hit_tokens"]),
        int(usage_rollup["prompt_cache_miss_tokens"]),
    )
    if rate is not None:
        usage_rollup["prompt_cache_hit_rate"] = rate
    return sections, wall, total_llm, usage_rollup


def assemble_section_report(sections: list[str]) -> str:
    cleaned = []
    for section in sections:
        text = section.strip()
        if not text:
            continue
        cleaned.append(text)
    if not cleaned:
        raise RuntimeError("no section content to assemble")
    return normalize_latex_delimiters("\n\n".join(cleaned)) + "\n"


async def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    total_started = time.monotonic()
    load_env_file(Path(args.env_file))
    resolve_mineru_config(args)
    resolve_llm_config(args)
    resolve_writer_llm_config(args)
    resolve_kimi_llm_config(args)
    resolve_figure_llm_config(args)

    if sum(bool(x) for x in (args.pdf, args.mineru_output, args.source_md)) != 1:
        raise SystemExit("Pass exactly one of --pdf, --mineru-output, or --source-md")

    pdf_preflight: dict[str, Any] = {}
    if args.export_vault:
        source_pdf_arg = args.paper_pdf or args.pdf
        source_pdf, pdf_preflight = resolve_existing_pdf_path(
            source_pdf_arg,
            conf_year=resolved_conf_year(args),
            search_roots=pdf_search_roots_from_args(args),
        )
        if not source_pdf:
            raise FileNotFoundError(
                "Vault export requires an existing PDF before LLM analysis starts. "
                f"input={source_pdf_arg!r}; attempts={pdf_preflight.get('attempts') or []}"
            )

    task_id = safe_slug(args.task_id or default_task_id(args), max_len=96)
    work_dir = Path(args.output_root).resolve() / task_id
    progress_path = work_dir / "progress.jsonl"
    work_dir.mkdir(parents=True, exist_ok=True)

    with RunLock(work_dir / ".lock"):
        atomic_write_text(work_dir / ".state", "RUNNING\n")
        manifest = {
            "task_id": task_id,
            "started_at": now_iso(),
            "work_dir": str(work_dir),
            "inputs": {
                "pdf": args.pdf,
                "mineru_output": args.mineru_output,
                "source_md": args.source_md,
                "paper_pdf": args.paper_pdf,
                "paper_pdf_resolution": pdf_preflight,
            },
            "model": "mock" if args.mock_llm else args.model,
            "provider": "mock" if args.mock_llm else args.provider,
            "writer_model": "mock" if args.mock_llm else args.writer_model,
            "writer_provider": "mock" if args.mock_llm else args.writer_provider,
            "kimi_model": "mock" if args.mock_llm else args.kimi_model,
            "figure_provider": "mock" if args.mock_llm else args.figure_provider,
            "figure_model": "mock" if args.mock_llm else args.figure_model,
            "reasoning_effort": "mock" if args.mock_llm else args.reasoning_effort,
            "base_url": "" if args.mock_llm else args.base_url,
            "writer_base_url": "" if args.mock_llm else args.writer_base_url,
            "kimi_base_url": "" if args.mock_llm else args.kimi_base_url,
            "figure_base_url": "" if args.mock_llm else args.figure_base_url,
            "thinking": "mock" if args.mock_llm else args.thinking,
            "part_thinking": "mock" if args.mock_llm else args.part_thinking,
            "part_reasoning_effort": "mock" if args.mock_llm else args.part_reasoning_effort,
            "writer_thinking": "mock" if args.mock_llm else args.writer_thinking,
            "writer_reasoning_effort": "mock" if args.mock_llm else args.writer_reasoning_effort,
            "mineru_model_source": args.mineru_model_source,
            "mineru_config": str(Path(args.mineru_config).expanduser()),
            "conf_year": resolved_conf_year(args),
            "paper_link": args.paper_link,
            "acceptance": args.acceptance,
            "openreview_forum_id": args.openreview_forum_id,
            "topic_assignments": args.topic_assignments,
            "mineru_output_root": args.mineru_output_root,
            "mineru_batch_id": args.mineru_batch_id,
            "theme_bucket": args.theme_bucket,
            "experiment_label": args.experiment_label,
        }
        atomic_write_json(work_dir / "manifest.json", manifest)
        append_jsonl(progress_path, {"event": "started", "at": now_iso(), "task_id": task_id})
        try:
            parse_info = prepare_parse(args, work_dir)
            markdown = (work_dir / "parse" / "full.md").read_text(encoding="utf-8")
            title = resolved_title(args, markdown, fallback=task_id)
            chunks = split_markdown(markdown, max_chars=args.chunk_chars, overlap_chars=args.overlap_chars)
            if not chunks:
                raise RuntimeError("no chunks produced from markdown")
            token_budget = apply_adaptive_token_budget(
                args,
                markdown_chars=len(markdown),
                chunk_count=len(chunks),
                page_count=page_count_from_content_list(work_dir / "parse" / "content_list.json"),
            )
            chunk_started = time.monotonic()
            write_chunks(chunks, work_dir)
            chunk_duration = round(time.monotonic() - chunk_started, 3)
            append_jsonl(progress_path, {
                "event": "parse_done",
                "at": now_iso(),
                "markdown_chars": len(markdown),
                "chunk_count": len(chunks),
                "parse_seconds": parse_info["duration_seconds"],
            })
            append_jsonl(progress_path, {"event": "token_budget_selected", "at": now_iso(), **token_budget})
            if args.dry_run:
                atomic_write_text(work_dir / ".state", "PLANNED\n")
                return {
                    "status": "planned",
                    "task_id": task_id,
                    "work_dir": str(work_dir),
                    "chunk_count": len(chunks),
                    "token_budget": token_budget,
                }

            part_results = await run_all_part_analyses(
                args,
                chunks=chunks,
                title=title,
                work_dir=work_dir,
                progress_path=progress_path,
            )
            part_wall_seconds = (
                part_results[0].get("_aggregate", {}).get("part_wall_seconds")
                if part_results else 0.0
            )
            part_total_llm_seconds = (
                part_results[0].get("_aggregate", {}).get("part_total_llm_seconds")
                if part_results else 0.0
            )
            figures_tables, visual_summary_usage = await enrich_figure_visual_summaries(
                args,
                figures_tables=parse_info["figures_tables"],
                work_dir=work_dir,
                progress_path=progress_path,
            )
            parse_info["figures_tables"] = figures_tables
            analysis = await run_main_analysis(
                args,
                title=title,
                markdown=markdown,
                part_results=part_results,
                figures_tables=figures_tables,
                work_dir=work_dir,
                progress_path=progress_path,
            )
            sections, section_wall_seconds, section_total_llm_seconds, writer_usage = await run_section_writers(
                args,
                analysis=analysis,
                part_results=part_results,
                figures_tables=figures_tables,
                work_dir=work_dir,
                progress_path=progress_path,
            )
            report = assemble_section_report(sections)
            writer_seconds = section_wall_seconds
            atomic_write_text(
                work_dir / "report" / "writer.raw.md",
                "\n\n".join(section.strip() for section in sections if section.strip()) + "\n",
            )
            atomic_write_text(
                work_dir / "report" / "final_report.md",
                (
                    "<!-- generated_by: run_local_paper_analysis.py -->\n"
                    f"<!-- generated_at: {now_iso()} -->\n"
                    f"<!-- writer_latency_seconds: {writer_seconds} -->\n\n"
                    + report
                ),
            )
            append_jsonl(progress_path, {"event": "writer_done", "at": now_iso()})
            vault_export = None
            figure_placements: list[dict[str, str]] = []
            figure_placement_usage: dict[str, Any] = {}
            if args.export_vault:
                copied_figures = copy_vault_figures(
                    figures_tables,
                    task_id=task_id,
                    asset_root=Path(args.vault_asset_root).expanduser().resolve(),
                )
                figure_placements, figure_placement_usage = await run_figure_placement(
                    args,
                    analysis=analysis,
                    report=report,
                    copied_figures=copied_figures,
                    work_dir=work_dir,
                    progress_path=progress_path,
                )
                vault_export = export_to_vault(
                    args,
                    task_id=task_id,
                    title=title,
                    work_dir=work_dir,
                    analysis=analysis,
                    report=report,
                    figures_tables=figures_tables,
                    figure_placements=figure_placements,
                    progress_path=progress_path,
                )
                copied_figures = copy_vault_figures(
                    figures_tables,
                    task_id=task_id,
                    asset_root=Path(args.vault_asset_root).expanduser().resolve(),
                )
                note_path = Path(str(vault_export.get("note_path") or ""))
                if note_path.exists() and args.kimi_check_repair:
                    repaired_note, kimi_check_repair_usage = await maybe_kimi_check_repair_note(
                        args,
                        note=note_path.read_text(encoding="utf-8"),
                        figure_placements=vault_export.get("figure_placements") or figure_placements,
                        copied_figures=copied_figures,
                        work_dir=work_dir,
                        progress_path=progress_path,
                    )
                    if kimi_check_repair_usage:
                        atomic_write_text(note_path, normalize_latex_delimiters(repaired_note) + "\n")
                        vault_export["kimi_check_repair_usage"] = kimi_check_repair_usage
                        repaired_validation = validate_vault_note(
                            note_path.read_text(encoding="utf-8"),
                            pdf_ref=str(vault_export.get("pdf_ref") or ""),
                            openreview_forum_id=args.openreview_forum_id,
                            copied_figures=copied_figures,
                            figure_placements=vault_export.get("figure_placements") or figure_placements,
                            max_images=args.max_note_images,
                        )
                        vault_export["validation"] = repaired_validation
                        atomic_write_json(work_dir / "report" / "vault_export.json", vault_export)
                validation = vault_export.get("validation") if isinstance(vault_export, dict) else None
                if validation:
                    append_jsonl(progress_path, {
                        "event": "vault_note_validated",
                        "at": now_iso(),
                        "ok": validation.get("ok"),
                        "checks": validation.get("checks"),
                        "note_path": vault_export.get("note_path"),
                    })
                append_jsonl(progress_path, {
                    "event": "vault_export_done",
                    "at": now_iso(),
                    "note_path": vault_export.get("note_path"),
                    "figure_count": vault_export.get("figure_count"),
                    "validation_ok": validation.get("ok") if validation else None,
                })
            part_prompt_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("prompt_tokens_est") or 0) for item in part_results)
            part_completion_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("completion_tokens_est") or 0) for item in part_results)
            part_reasoning_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("reasoning_tokens_est") or 0) for item in part_results)
            part_total_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("total_tokens_est") or 0) for item in part_results)
            part_cost = round(sum(float(item.get("_meta", {}).get("usage", {}).get("estimated_cost_usd") or 0.0) for item in part_results), 6)
            part_prompt_tokens_api = sum(int(item.get("_meta", {}).get("usage", {}).get("prompt_tokens_api") or 0) for item in part_results)
            part_completion_tokens_api = sum(int(item.get("_meta", {}).get("usage", {}).get("completion_tokens_api") or 0) for item in part_results)
            part_reasoning_tokens_api = sum(int(item.get("_meta", {}).get("usage", {}).get("reasoning_tokens_api") or 0) for item in part_results)
            part_cache_hit_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("prompt_cache_hit_tokens") or 0) for item in part_results)
            part_cache_miss_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("prompt_cache_miss_tokens") or 0) for item in part_results)
            part_cost_api = round(sum(float(item.get("_meta", {}).get("usage", {}).get("estimated_cost_usd_api") or 0.0) for item in part_results), 6)
            main_usage = analysis.get("_meta", {}).get("usage", {}) if isinstance(analysis.get("_meta"), dict) else {}
            usage_summary = {
                "provider": args.provider,
                "model": args.model,
                "part_prompt_tokens_est": part_prompt_tokens,
                "part_completion_tokens_est": part_completion_tokens,
                "part_reasoning_tokens_est": part_reasoning_tokens,
                "part_total_tokens_est": part_total_tokens,
                "part_estimated_cost_usd": part_cost,
                "part_prompt_tokens_api": part_prompt_tokens_api,
                "part_completion_tokens_api": part_completion_tokens_api,
                "part_reasoning_tokens_api": part_reasoning_tokens_api,
                "part_prompt_cache_hit_tokens": part_cache_hit_tokens,
                "part_prompt_cache_miss_tokens": part_cache_miss_tokens,
                "part_estimated_cost_usd_api": part_cost_api,
                "main_prompt_tokens_est": int(main_usage.get("prompt_tokens_est") or 0),
                "main_completion_tokens_est": int(main_usage.get("completion_tokens_est") or 0),
                "main_reasoning_tokens_est": int(main_usage.get("reasoning_tokens_est") or 0),
                "main_total_tokens_est": int(main_usage.get("total_tokens_est") or 0),
                "main_estimated_cost_usd": float(main_usage.get("estimated_cost_usd") or 0.0),
                "main_prompt_tokens_api": int(main_usage.get("prompt_tokens_api") or 0),
                "main_completion_tokens_api": int(main_usage.get("completion_tokens_api") or 0),
                "main_reasoning_tokens_api": int(main_usage.get("reasoning_tokens_api") or 0),
                "main_prompt_cache_hit_tokens": int(main_usage.get("prompt_cache_hit_tokens") or 0),
                "main_prompt_cache_miss_tokens": int(main_usage.get("prompt_cache_miss_tokens") or 0),
                "main_estimated_cost_usd_api": float(main_usage.get("estimated_cost_usd_api") or 0.0),
                "writer_prompt_tokens_est": int(writer_usage.get("prompt_tokens_est") or 0),
                "writer_completion_tokens_est": int(writer_usage.get("completion_tokens_est") or 0),
                "writer_reasoning_tokens_est": int(writer_usage.get("reasoning_tokens_est") or 0),
                "writer_total_tokens_est": int(writer_usage.get("total_tokens_est") or 0),
                "writer_estimated_cost_usd": float(writer_usage.get("estimated_cost_usd") or 0.0),
                "writer_prompt_tokens_api": int(writer_usage.get("prompt_tokens_api") or 0),
                "writer_completion_tokens_api": int(writer_usage.get("completion_tokens_api") or 0),
                "writer_reasoning_tokens_api": int(writer_usage.get("reasoning_tokens_api") or 0),
                "writer_prompt_cache_hit_tokens": int(writer_usage.get("prompt_cache_hit_tokens") or 0),
                "writer_prompt_cache_miss_tokens": int(writer_usage.get("prompt_cache_miss_tokens") or 0),
                "writer_estimated_cost_usd_api": float(writer_usage.get("estimated_cost_usd_api") or 0.0),
                "figure_placement_prompt_tokens_est": int(figure_placement_usage.get("prompt_tokens_est") or 0),
                "figure_placement_completion_tokens_est": int(figure_placement_usage.get("completion_tokens_est") or 0),
                "figure_placement_total_tokens_est": int(figure_placement_usage.get("total_tokens_est") or 0),
                "figure_placement_estimated_cost_usd": float(figure_placement_usage.get("estimated_cost_usd") or 0.0),
                "figure_visual_summary_prompt_tokens_est": int(visual_summary_usage.get("prompt_tokens_est") or 0),
                "figure_visual_summary_completion_tokens_est": int(visual_summary_usage.get("completion_tokens_est") or 0),
                "figure_visual_summary_total_tokens_est": int(visual_summary_usage.get("total_tokens_est") or 0),
                "figure_visual_summary_estimated_cost_usd": float(visual_summary_usage.get("estimated_cost_usd") or 0.0),
            }
            usage_summary["prompt_tokens_api"] = (
                usage_summary["part_prompt_tokens_api"]
                + usage_summary["main_prompt_tokens_api"]
                + usage_summary["writer_prompt_tokens_api"]
            )
            usage_summary["completion_tokens_api"] = (
                usage_summary["part_completion_tokens_api"]
                + usage_summary["main_completion_tokens_api"]
                + usage_summary["writer_completion_tokens_api"]
            )
            usage_summary["reasoning_tokens_api"] = (
                usage_summary["part_reasoning_tokens_api"]
                + usage_summary["main_reasoning_tokens_api"]
                + usage_summary["writer_reasoning_tokens_api"]
            )
            usage_summary["prompt_cache_hit_tokens"] = (
                usage_summary["part_prompt_cache_hit_tokens"]
                + usage_summary["main_prompt_cache_hit_tokens"]
                + usage_summary["writer_prompt_cache_hit_tokens"]
            )
            usage_summary["prompt_cache_miss_tokens"] = (
                usage_summary["part_prompt_cache_miss_tokens"]
                + usage_summary["main_prompt_cache_miss_tokens"]
                + usage_summary["writer_prompt_cache_miss_tokens"]
            )
            usage_summary["estimated_cost_usd_api"] = round(
                usage_summary["part_estimated_cost_usd_api"]
                + usage_summary["main_estimated_cost_usd_api"]
                + usage_summary["writer_estimated_cost_usd_api"],
                6,
            )
            usage_summary["cost_basis_api"] = "sum_of_stage_api_usage_with_prompt_cache"
            for stage in ("part", "main", "writer"):
                rate = cache_hit_rate(
                    int(usage_summary.get(f"{stage}_prompt_cache_hit_tokens") or 0),
                    int(usage_summary.get(f"{stage}_prompt_cache_miss_tokens") or 0),
                )
                if rate is not None:
                    usage_summary[f"{stage}_prompt_cache_hit_rate"] = rate
            overall_cache_rate = cache_hit_rate(
                int(usage_summary["prompt_cache_hit_tokens"]),
                int(usage_summary["prompt_cache_miss_tokens"]),
            )
            if overall_cache_rate is not None:
                usage_summary["prompt_cache_hit_rate"] = overall_cache_rate
            usage_summary["prompt_tokens_est"] = (
                usage_summary["part_prompt_tokens_est"]
                + usage_summary["main_prompt_tokens_est"]
                + usage_summary["writer_prompt_tokens_est"]
                + usage_summary["figure_placement_prompt_tokens_est"]
                + usage_summary["figure_visual_summary_prompt_tokens_est"]
            )
            usage_summary["completion_tokens_est"] = (
                usage_summary["part_completion_tokens_est"]
                + usage_summary["main_completion_tokens_est"]
                + usage_summary["writer_completion_tokens_est"]
                + usage_summary["figure_placement_completion_tokens_est"]
                + usage_summary["figure_visual_summary_completion_tokens_est"]
            )
            usage_summary["reasoning_tokens_est"] = (
                usage_summary["part_reasoning_tokens_est"]
                + usage_summary["main_reasoning_tokens_est"]
                + usage_summary["writer_reasoning_tokens_est"]
            )
            usage_summary["total_tokens_est"] = (
                usage_summary["part_total_tokens_est"]
                + usage_summary["main_total_tokens_est"]
                + usage_summary["writer_total_tokens_est"]
                + usage_summary["figure_placement_total_tokens_est"]
                + usage_summary["figure_visual_summary_total_tokens_est"]
            )
            usage_summary["total_tokens_api"] = (
                usage_summary["prompt_tokens_api"]
                + usage_summary["completion_tokens_api"]
            )
            usage_summary["estimated_cost_usd"] = round(
                usage_summary["part_estimated_cost_usd"]
                + usage_summary["main_estimated_cost_usd"]
                + usage_summary["writer_estimated_cost_usd"]
                + usage_summary["figure_placement_estimated_cost_usd"]
                + usage_summary["figure_visual_summary_estimated_cost_usd"],
                6,
            )
            usage_summary["cost_basis"] = "sum_of_stage_estimates"
            completed = {
                "status": "done",
                "task_id": task_id,
                "work_dir": str(work_dir),
                "chunk_count": len(chunks),
                "part_analysis_count": len(part_results),
                "report_chars": len(report),
                "vault_export": vault_export,
                "token_budget": token_budget,
                "experiment_label": args.experiment_label,
                "usage": usage_summary,
                "timing": {
                    "parse_seconds": parse_info["duration_seconds"],
                    "chunk_write_seconds": max(0.0, chunk_duration),
                    "part_wall_seconds": part_wall_seconds,
                    "part_total_llm_seconds": part_total_llm_seconds,
                    "main_analysis_seconds": analysis.get("_meta", {}).get("latency_seconds"),
                    "writer_seconds": writer_seconds,
                    "section_total_llm_seconds": section_total_llm_seconds,
                    "total_seconds": round(time.monotonic() - total_started, 3),
                },
                "completed_at": now_iso(),
            }
            manifest.update(completed)
            atomic_write_json(work_dir / "manifest.json", manifest)
            atomic_write_text(work_dir / ".state", "DONE\n")
            append_jsonl(progress_path, {"event": "done", "at": now_iso()})
            return completed
        except Exception as exc:
            error_info = {
                "event": "failed",
                "at": now_iso(),
                "error": str(exc),
                "error_type": type(exc).__name__,
                "traceback": traceback.format_exc(),
            }
            atomic_write_text(work_dir / ".state", "FAILED\n")
            append_jsonl(progress_path, error_info)
            raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pdf", help="PDF to parse with local MinerU CLI")
    source.add_argument("--mineru-output", help="Existing MinerU output directory")
    source.add_argument("--source-md", help="Existing markdown source, mainly for tests/recovery")
    parser.add_argument("--paper-pdf", default="", help="Original PDF to copy into vault when input is not --pdf")
    parser.add_argument(
        "--pdf-search-root",
        action="append",
        default=[],
        help="Extra root for resolving legacy/external PDF paths; repeat as needed. RF_PDF_SEARCH_ROOTS also works.",
    )
    parser.add_argument("--task-id", default="", help="Stable task id under output root")
    parser.add_argument("--paper-title", default="", help="Canonical paper title for vault export")
    parser.add_argument("--conf-year", default=DEFAULT_CONF_YEAR, help="Vault venue/year folder, e.g. CVPR_2026")
    parser.add_argument("--paper-link", default="", help="Canonical paper URL for note metadata")
    parser.add_argument("--acceptance", default="", help="Optional presentation/status metadata, e.g. oral, poster, spotlight")
    parser.add_argument("--openreview-forum-id", default="", help="OpenReview forum id for note metadata")
    parser.add_argument("--topic-assignments", default="", help="Optional JSONL topic assignment file keyed by OpenReview forum id")
    parser.add_argument("--theme-bucket", default="", help="Manifest theme bucket for lightweight metadata")
    parser.add_argument("--experiment-label", default="", help="Optional label for controlled analysis-chain experiments.")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--mineru-bin", default=DEFAULT_MINERU_BIN)
    parser.add_argument("--mineru-backend", default="pipeline")
    parser.add_argument("--mineru-timeout", type=int, default=1800)
    parser.add_argument("--mineru-model-source", choices=["local", "huggingface", "modelscope"], default="local")
    parser.add_argument("--mineru-config", default=str(DEFAULT_MINERU_CONFIG))
    parser.add_argument("--mineru-pipeline-cache", default=str(MINERU_PIPELINE_CACHE))
    parser.add_argument("--mineru-output-root", default="", help="Optional root for normalized existing MinerU outputs")
    parser.add_argument("--mineru-batch-id", default="", help="Optional batch id under --mineru-output-root")
    parser.add_argument("--require-existing-mineru-output", action="store_true", help="Fail instead of running MinerU when --pdf has no cached MinerU output")
    parser.add_argument("--chunk-chars", type=int, default=8_000)
    parser.add_argument("--overlap-chars", type=int, default=800)
    parser.add_argument("--part-workers", type=int, default=2)
    parser.add_argument("--section-workers", type=int, default=1, help="Concurrent section writers. Default 1 preserves prefix-cache reuse; raise only for latency/cost A/B tests.")
    parser.add_argument(
        "--provider",
        choices=["deepseek", "kimi"],
        default="deepseek",
        help="LLM provider. DeepSeek is the default; Kimi is used only when explicitly selected.",
    )
    parser.add_argument("--model", default="")
    parser.add_argument("--thinking", choices=THINKING_CHOICES, default="enabled", help="DeepSeek thinking mode for main analysis and repairs.")
    parser.add_argument("--reasoning-effort", default="max", help="Reasoning effort for compatible providers.")
    parser.add_argument("--part-thinking", choices=THINKING_CHOICES, default="disabled", help="DeepSeek thinking mode for chunk-level anchor extraction.")
    parser.add_argument("--part-reasoning-effort", default="", help="Reasoning effort for part analysis. Defaults to --reasoning-effort.")
    parser.add_argument("--base-url", default="")
    parser.add_argument("--api-key-env", default="")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument(
        "--writer-provider",
        choices=["deepseek", "kimi"],
        default="deepseek",
        help="Writer provider. Defaults to DeepSeek; Kimi is reserved for visual/check-repair stages.",
    )
    parser.add_argument("--writer-model", default="")
    parser.add_argument("--writer-base-url", default="")
    parser.add_argument("--writer-api-key-env", default="")
    parser.add_argument("--writer-temperature", type=float, default=KIMI_DEFAULT_TEMPERATURE)
    parser.add_argument("--writer-thinking", choices=THINKING_CHOICES, default="disabled", help="DeepSeek thinking mode for section writers.")
    parser.add_argument("--writer-reasoning-effort", default="max")
    parser.add_argument("--kimi-model", default="")
    parser.add_argument("--kimi-base-url", default="")
    parser.add_argument("--kimi-api-key-env", default="")
    parser.add_argument("--kimi-temperature", type=float, default=KIMI_DEFAULT_TEMPERATURE)
    parser.add_argument("--no-kimi-repair", dest="kimi_repair", action="store_false", help="Disable Kimi JSON repair fallback")
    parser.add_argument("--kimi-check-repair", dest="kimi_check_repair", action="store_true", help="Opt into final Kimi note check/repair after mechanical validation")
    parser.add_argument("--no-kimi-check-repair", dest="kimi_check_repair", action="store_false", help="Disable final Kimi note check/repair")
    parser.add_argument("--kimi-check-repair-max-tokens", type=int, default=16384)
    parser.add_argument(
        "--figure-provider",
        choices=["none", "openai", "kimi"],
        default="none",
        help="Optional figure/table visual-summary and placement LLM. Default none uses deterministic caption/placement fallback.",
    )
    parser.add_argument("--figure-model", default="")
    parser.add_argument("--figure-base-url", default="")
    parser.add_argument("--figure-api-key-env", default="")
    parser.add_argument("--figure-temperature", type=float, default=0.1)
    parser.add_argument("--part-max-tokens", type=int, default=16384)
    parser.add_argument("--main-max-tokens", type=int, default=16384)
    parser.add_argument("--main-length-retry-max-tokens", type=int, default=32768)
    parser.add_argument("--main-length-retry-reasoning-effort", default="medium")
    parser.add_argument("--main-length-retry-thinking", choices=THINKING_CHOICES, default="enabled")
    parser.add_argument("--writer-max-tokens", type=int, default=4096)
    parser.add_argument("--writer-context-max-parts", type=int, default=6)
    parser.add_argument("--writer-context-max-items", type=int, default=2)
    parser.add_argument("--writer-figure-context-max-items", type=int, default=10)
    parser.add_argument("--figure-placement-max-tokens", type=int, default=4096)
    parser.add_argument("--figure-visual-summary-max-items", type=int, default=8)
    parser.add_argument("--figure-visual-summary-max-tokens", type=int, default=1024)
    parser.add_argument("--main-context-chars", type=int, default=36_000)
    parser.add_argument("--adaptive-tokens", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--adaptive-long-chunk-count", type=int, default=11)
    parser.add_argument("--adaptive-long-markdown-chars", type=int, default=144_000)
    parser.add_argument("--adaptive-long-chars-per-page", type=int, default=4_500)
    parser.add_argument("--adaptive-long-part-max-tokens", type=int, default=8192)
    parser.add_argument("--adaptive-long-main-max-tokens", type=int, default=12288)
    parser.add_argument("--adaptive-long-main-context-chars", type=int, default=54_000)
    parser.add_argument("--adaptive-extreme-chunk-count", type=int, default=15)
    parser.add_argument("--adaptive-extreme-markdown-chars", type=int, default=216_000)
    parser.add_argument("--adaptive-extreme-pages", type=int, default=45)
    parser.add_argument("--adaptive-extreme-main-max-tokens", type=int, default=16384)
    parser.add_argument("--export-vault", action="store_true", help="Copy PDF/assets and write Obsidian note")
    parser.add_argument("--vault-root", default=str(DEFAULT_VAULT_ROOT))
    parser.add_argument("--vault-note-dir", default="", help="Override output directory for exported Markdown notes")
    parser.add_argument(
        "--vault-asset-root",
        default="",
        help="Override figure/table asset root. Defaults to <vault-root>/assets/figures/papers.",
    )
    parser.add_argument("--max-note-images", type=int, default=12)
    parser.add_argument("--mock-llm", action="store_true", help="Use deterministic local mock outputs")
    parser.add_argument("--dry-run", action="store_true", help="Parse and chunk only")
    parser.add_argument("--force", action="store_true", help="Overwrite existing stage outputs")
    parser.add_argument("--no-resume", dest="resume", action="store_false", help="Do not reuse existing stage outputs")
    parser.set_defaults(resume=True, kimi_repair=False, kimi_check_repair=False)
    return parser


def normalize_vault_args(args: argparse.Namespace) -> argparse.Namespace:
    args.acceptance = normalize_acceptance(args.acceptance)
    if not args.vault_asset_root:
        args.vault_asset_root = str(Path(args.vault_root).expanduser().resolve() / "assets" / "figures" / "papers")
    return args


def main() -> None:
    args = normalize_vault_args(build_parser().parse_args())
    result = asyncio.run(run_pipeline(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

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


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.researchflow_local.topic_tags import (
    format_topic_tags,
    topic_tags_from_assignment,
    topic_tags_from_names,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_private" / "local_analysis_runs"
DEFAULT_ENV_FILE = REPO_ROOT / ".env"
LEGACY_PRIVATE_ENV_FILE = REPO_ROOT / "_private" / "researchflow-backend-local" / ".env"
DEFAULT_VAULT_ROOT = REPO_ROOT / "obsidian-vault"
DEFAULT_ASSET_ROOT = DEFAULT_VAULT_ROOT / "assets" / "figures" / "papers"
DEFAULT_MINERU_BIN = shutil.which("mineru") or "mineru"
DEFAULT_MINERU_CONFIG = REPO_ROOT / "_private" / "mineru_local" / "mineru.json"
DEFAULT_MINERU_HF_CACHE = Path.home() / ".cache" / "huggingface" / "hub"
MINERU_PIPELINE_CACHE = DEFAULT_MINERU_HF_CACHE / "models--opendatalab--PDF-Extract-Kit-1.0"
DEFAULT_CONF_YEAR = ""
DEFAULT_TOPIC_ASSIGNMENTS = os.environ.get("RF_TOPIC_ASSIGNMENTS", "").strip()
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"
KIMI_DEFAULT_BASE_URL = "https://api.moonshot.ai/v1"
KIMI_DEFAULT_TEMPERATURE = 0.6
DEFAULT_KIMI_MODEL = "kimi-k2.6"
SECTION_SPECS: tuple[tuple[str, str], ...] = (
    ("概述", "概括问题、核心结论、方法定位与主要结果，不要展开细节。"),
    ("背景与动机", "说明问题背景、现有方法缺口、本文动机。"),
    ("核心创新", "聚焦相对 baseline 的关键创新与 changed slots。"),
    ("整体框架", "描述整体 pipeline、模块关系、输入输出流。"),
    ("核心模块与公式推导", "只写关键模块、关键公式、公式变量含义，禁止猜公式。"),
    ("实验与分析", "写主结果、消融、失败模式、重要图表结论。"),
    ("方法谱系与知识库定位", "写与 baseline/follow-up 的关系、适用边界、局限与开放问题。"),
)

DISCOUNTED_PRICES_PER_MTOKEN_USD: dict[str, dict[str, float]] = {
    "deepseek-v4-pro": {"input": 0.435, "output": 0.87},
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.14, "output": 0.28},
}


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


def merge_usage_totals(base: dict[str, Any], extra: dict[str, Any], *, cost_basis: str) -> dict[str, Any]:
    merged = dict(base)
    for key in [
        "prompt_tokens_est",
        "completion_tokens_est",
        "reasoning_tokens_est",
        "total_tokens_est",
        "total_with_reasoning_tokens_est",
    ]:
        merged[key] = int(base.get(key) or 0) + int(extra.get(key) or 0)
    merged["estimated_cost_usd"] = round(
        float(base.get("estimated_cost_usd") or 0.0)
        + float(extra.get("estimated_cost_usd") or 0.0),
        6,
    )
    merged["cost_basis"] = cost_basis
    return merged


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
    "baseline_methods": [{"name": str, "role": str}],
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
6. Output ONLY valid JSON, with no markdown fences."""

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
LaTeX; do not use `\\(...\\)` or `\\[...\\]`. Do not output JSON or markdown
fences around the whole report."""

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
"""

FIGURE_PLACEMENT_SYSTEM = """You are ResearchFlow's local note image placement reviewer.

Choose which local MinerU figure/table images should be inserted into the
exported Obsidian note. Use the verified analysis, report text, and captions.
Prefer summary tables or result plots that directly support the note section.
Do not place sample-only dataset images as the framework image. If no real
framework/pipeline/method diagram exists, leave 整体框架 empty.

Return JSON only:
{
  "placements": [
    {"item_id": str, "section": "整体框架" | "实验与分析", "reason": str}
  ]
}

Rules:
1. Select at most the requested image budget.
2. Use only supplied item_id values.
3. Do not duplicate the same item_id.
4. Prefer Table 1 / benchmark summary tables and decisive result plots over
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
6. ResearchFlow frontmatter schema: keep `aliases` as short English/model
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
    match = re.match(r"([A-Za-z]+)_(\d{4})$", conf_year or "")
    if not match:
        return conf_year or "Unknown", None
    return match.group(1), int(match.group(2))


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
    if path == DEFAULT_ENV_FILE and not path.exists() and LEGACY_PRIVATE_ENV_FILE.exists():
        path = LEGACY_PRIVATE_ENV_FILE
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
            return part
    return ""


def resolved_conf_year(args: argparse.Namespace) -> str:
    conf_year = (args.conf_year or "").strip()
    if conf_year:
        return conf_year
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


def normalize_main_analysis(title: str, parsed: dict[str, Any]) -> dict[str, Any]:
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
    valid_direct = [path.resolve() for path in direct_candidates if complete_mineru_output(path)]
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
    output_dir.mkdir(parents=True, exist_ok=True)
    command = [mineru_bin, "-p", str(pdf_path), "-o", str(output_dir), "-b", backend]
    env = os.environ.copy()
    if model_source:
        env["MINERU_MODEL_SOURCE"] = model_source
    if config_path:
        env["MINERU_TOOLS_CONFIG_JSON"] = str(config_path)
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


def extract_label(caption: str, fallback_type: str, index: int) -> str:
    match = re.search(r"\b(Figure|Fig\.?|Table)\s*([0-9]+[A-Za-z]?)", caption, flags=re.IGNORECASE)
    if match:
        kind = "Table" if match.group(1).lower().startswith("table") else "Figure"
        return f"{kind} {match.group(2)}"
    return f"{fallback_type.title()} {index}"


def extract_figures_tables(content_path: Path | None, *, source_root: Path) -> list[dict[str, Any]]:
    if not content_path or not content_path.exists():
        return []
    try:
        payload = json.loads(content_path.read_text(encoding="utf-8", errors="ignore"))
    except json.JSONDecodeError:
        return []
    out: list[dict[str, Any]] = []
    counters = {"figure": 0, "table": 0}
    for item in flatten_content_items(payload):
        item_type = str(item.get("type") or "").lower()
        content = item.get("content") if isinstance(item.get("content"), dict) else {}
        if item_type in {"image", "chart", "figure"}:
            kind = "figure"
            caption = (
                caption_text(content.get("image_caption"))
                or caption_text(content.get("chart_caption"))
                or caption_text(item.get("caption"))
            )
        elif item_type == "table":
            kind = "table"
            caption = caption_text(content.get("table_caption")) or caption_text(item.get("caption"))
        else:
            continue

        counters[kind] += 1
        image_source = content.get("image_source") if isinstance(content.get("image_source"), dict) else {}
        src = item.get("img_path") or image_source.get("path") or item.get("image_path")
        src_path = None
        if src:
            candidate = (content_path.parent / src).resolve()
            if not candidate.exists():
                candidate = (source_root / src).resolve()
            if candidate.exists():
                src_path = candidate
        out.append({
            "label": extract_label(caption, kind, counters[kind]),
            "type": kind,
            "caption": caption,
            "source_path": str(src_path) if src_path else str(src or ""),
            "page": item.get("page_idx") or item.get("page") or item.get("page_num"),
            "bbox": item.get("bbox"),
        })
    return out


def table_cell(value: Any) -> str:
    return str(value or "").replace("\n", " ").replace("|", "/").strip()


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


def list_names(items: list[dict[str, Any]], key: str, *, max_items: int = 5) -> str:
    names = []
    for item in items:
        value = item.get(key)
        if value:
            names.append(str(value))
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


def topic_text_for_note(openreview_forum_id: str, conf_year: str, topic_assignments: str = "") -> str:
    info = load_topic_assignments(topic_assignments).get(openreview_forum_id or "", {})
    tags = topic_tags_from_assignment(info)
    if not tags:
        tags = topic_tags_from_names([conf_year])
    return format_topic_tags(tags)


def topic_tags_for_frontmatter(topic_text: str | None, conf_year: str) -> list[str]:
    tags = [tag.removeprefix("#") for tag in (topic_text or "").split() if tag.startswith("#")]
    return tags[:5] if tags else [f"topic/{safe_slug(conf_year).lower()}"]


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


def claims_for_frontmatter(analysis: dict[str, Any], *, max_items: int = 4) -> list[str]:
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
    return claims[:max_items] or ["待人工复核。"]


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


def focused_part_analyses(section_title: str, part_results: list[dict[str, Any]], *, max_parts: int = 8) -> list[dict[str, Any]]:
    selected = [part for part in part_results if part_matches_section(part, section_title)]
    if section_title == "概述":
        selected = (part_results[:4] + part_results[-2:]) if len(part_results) > 6 else part_results
    if not selected:
        selected = part_results[:max_parts]
    return [slim_part_analysis(part) for part in selected[:max_parts]]


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
        shutil.copy2(source, target)
        copied_item = dict(item)
        copied_item["item_id"] = str(item.get("item_id") or f"item_{index:03d}")
        copied_item["vault_asset_path"] = target.resolve()
        copied_item["note_image_path"] = f"../../assets/figures/papers/{task_id}/figures/{filename}"
        copied.append(copied_item)
    return copied


def image_block(item: dict[str, Any]) -> str:
    label = str(item.get("label") or "Figure")
    caption = compact_text(dedupe_caption_prefix(label, str(item.get("caption") or "")), max_len=700)
    path = str(item.get("note_image_path") or "")
    if not path:
        return ""
    if caption:
        return f"![{label}]({path})\n*{label}: {caption}*"
    return f"![{label}]({path})"


def placement_candidates(figures_tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = []
    for index, item in enumerate(figures_tables, 1):
        candidates.append({
            "item_id": str(item.get("item_id") or f"item_{index:03d}"),
            "label": str(item.get("label") or ""),
            "type": str(item.get("type") or ""),
            "caption": compact_text(dedupe_caption_prefix(str(item.get("label") or ""), str(item.get("caption") or "")), max_len=260),
            "visual_summary": compact_text(item.get("visual_summary"), max_len=260),
            "visual_type": str(item.get("visual_type") or ""),
            "placement_hint": str(item.get("placement_hint") or ""),
            "is_sample_only": bool(item.get("is_sample_only")),
        })
    return candidates


def sample_only_figure(item: dict[str, Any]) -> bool:
    if str(item.get("type") or "").lower() != "figure":
        return False
    text = f"{item.get('label') or ''} {item.get('caption') or ''}".lower()
    sample_words = ("sample", "samples", "few samples", "dataset")
    result_words = ("result", "estimate", "performance", "accuracy", "plot")
    return any(word in text for word in sample_words) and not any(word in text for word in result_words)


def fallback_figure_placements(figures_tables: list[dict[str, Any]], *, max_images: int) -> list[dict[str, str]]:
    if max_images <= 0:
        return []
    candidates = placement_candidates(figures_tables)
    by_id = {item["item_id"]: item for item in candidates}
    placements: list[dict[str, str]] = []
    used: set[str] = set()

    for item in candidates:
        text = f"{item.get('label') or ''} {item.get('caption') or ''}".lower()
        if sample_only_figure(item):
            continue
        if item.get("type", "").lower() == "figure" and re.search(r"\b(framework|pipeline|architecture|overview|method)\b", text):
            placements.append({"item_id": item["item_id"], "section": "整体框架", "reason": "caption indicates a framework or method overview"})
            used.add(item["item_id"])
            break

    experiment_candidates = [
        item for item in candidates
        if item["item_id"] not in used
        and not sample_only_figure(item)
        and (
            item.get("type", "").lower() == "table"
            or re.search(r"\b(result|estimate|estimation|performance|experiment|benchmark|lid)\b", f"{item.get('label') or ''} {item.get('caption') or ''}".lower())
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
        if item_id not in valid_ids or item_id in used or section not in {"整体框架", "实验与分析"}:
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


def focused_figures_tables(section_title: str, figures_tables: list[dict[str, Any]], *, max_items: int = 16) -> list[dict[str, Any]]:
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


async def kimi_visual_summary(
    args: argparse.Namespace,
    *,
    item: dict[str, Any],
) -> LLMCallResult:
    from openai import AsyncOpenAI

    api_key = os.environ.get(args.kimi_api_key_env, "")
    if not api_key:
        raise RuntimeError(f"Missing API key env var: {args.kimi_api_key_env}")
    source = Path(str(item.get("source_path") or ""))
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"figure image not found: {source}")
    client_kwargs: dict[str, Any] = {"api_key": api_key}
    if args.kimi_base_url:
        client_kwargs["base_url"] = args.kimi_base_url
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
        stream = await client.chat.completions.create(
            model=args.kimi_model,
            messages=messages,
            max_tokens=args.figure_visual_summary_max_tokens,
            temperature=args.kimi_temperature,
            stream=True,
            extra_body={"thinking": {"type": "disabled"}},
        )
        chunks: list[str] = []
        finish_reasons: list[str] = []
        stream_chunk_count = 0
        async for chunk in stream:
            stream_chunk_count += 1
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
        "provider": "kimi",
        "model": args.kimi_model,
        "prompt_tokens_est": prompt_tokens,
        "completion_tokens_est": completion_tokens,
        "reasoning_tokens_est": 0,
        "total_tokens_est": prompt_tokens + completion_tokens,
        "total_with_reasoning_tokens_est": prompt_tokens + completion_tokens,
        "estimated_cost_usd": estimate_cost_usd(args.kimi_model, prompt_tokens, completion_tokens),
        "cost_basis": "discounted_estimate_from_local_text_lengths",
    }
    diagnostics = {
        "content_chars": len(text),
        "reasoning_chars": 0,
        "finish_reason": finish_reasons[-1] if finish_reasons else "",
        "finish_reasons": finish_reasons,
        "stream_chunk_count": stream_chunk_count,
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
    if args.mock_llm or args.figure_visual_summary_max_items <= 0:
        atomic_write_json(out_path, {"figures_tables": items, "usage": {}})
        return items, {}

    by_id = {item["item_id"]: item for item in items}
    usage_totals = {
        "provider": "kimi",
        "model": args.kimi_model,
        "prompt_tokens_est": 0,
        "completion_tokens_est": 0,
        "reasoning_tokens_est": 0,
        "total_tokens_est": 0,
        "total_with_reasoning_tokens_est": 0,
        "estimated_cost_usd": 0.0,
        "cost_basis": "sum_of_visual_summary_estimates",
    }
    for item in visual_summary_candidates(items, max_items=args.figure_visual_summary_max_items):
        item_id = item["item_id"]
        raw_path = raw_dir / f"{item_id}.raw.txt"
        try:
            result = await kimi_visual_summary(args, item=item)
            atomic_write_text(raw_path, result.text)
            parsed = parse_json_object(result.text, label=f"visual_summary_{item_id}")
            summary = normalize_visual_summary(parsed)
            summary["visual_summary_provider"] = "kimi"
            summary["visual_stream_diagnostics"] = result.diagnostics or {}
            by_id[item_id].update(summary)
            usage = result.usage
            for key in ["prompt_tokens_est", "completion_tokens_est", "reasoning_tokens_est", "total_tokens_est", "total_with_reasoning_tokens_est"]:
                usage_totals[key] += int(usage.get(key) or 0)
            usage_totals["estimated_cost_usd"] += float(usage.get("estimated_cost_usd") or 0.0)
        except Exception as exc:  # noqa: BLE001
            by_id[item_id].update(caption_only_visual_summary(item))
            by_id[item_id]["visual_summary_error"] = str(exc)
            append_jsonl(progress_path, {"event": "figure_visual_summary_fallback", "at": now_iso(), "item_id": item_id, "error": str(exc)})
    usage_totals["estimated_cost_usd"] = round(usage_totals["estimated_cost_usd"], 6)
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


def figure_blocks_for_note(
    copied: list[dict[str, Any]],
    *,
    max_images: int,
    placements: list[dict[str, Any]] | None = None,
) -> tuple[list[str], list[str]]:
    if max_images <= 0:
        return [], []
    selected = placements if placements is not None else fallback_figure_placements(copied, max_images=max_images)
    by_id = {str(item.get("item_id") or f"item_{index:03d}"): item for index, item in enumerate(copied, 1)}
    framework_items: list[dict[str, Any]] = []
    experiment_items: list[dict[str, Any]] = []
    used: set[str] = set()
    for placement in selected:
        item_id = str(placement.get("item_id") or "")
        if item_id in used or item_id not in by_id:
            continue
        target = framework_items if placement.get("section") == "整体框架" else experiment_items
        target.append(by_id[item_id])
        used.add(item_id)
        if len(used) >= max_images:
            break
    return (
        [image_block(item) for item in framework_items],
        [image_block(item) for item in experiment_items],
    )


def render_frontmatter(
    *,
    title: str,
    conf_year: str,
    pdf_ref: str,
    analysis: dict[str, Any],
    theme_bucket: str,
    acceptance: str,
    topic_text: str | None = None,
) -> str:
    venue, year = infer_conf_parts(conf_year)
    method = (analysis.get("method") or {}).get("proposed_method_name") or ""
    truth = analysis.get("analysis_truth") or {}
    core = truth.get("core_insight") or ""
    causal_knob = truth.get("causal_knob") or ""
    real_bottleneck = truth.get("real_bottleneck") or ""
    primary_logic = compact_text(core or real_bottleneck or method, max_len=420)
    tags = topic_tags_for_frontmatter(topic_text, conf_year)
    claims = claims_for_frontmatter(analysis)
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
        f"acceptance: {yaml_scalar(acceptance or 'unknown')}",
        "tags:",
    ])
    lines.extend(f"- {yaml_scalar(tag)}" for tag in tags)
    lines.extend([
        f"core_operator: {yaml_scalar(compact_text(causal_knob or method or core, max_len=180))}",
        f"primary_logic: {yaml_scalar(primary_logic)}",
        "claims:",
    ])
    lines.extend(f"- {yaml_scalar(claim)}" for claim in claims)
    lines.extend([
        f"paradigm: {yaml_scalar(compact_text(core or method, max_len=180))}",
        "---",
        "",
    ])
    return "\n".join(lines)


def render_info_table(
    *,
    title: str,
    conf_year: str,
    openreview_forum_id: str,
    paper_link: str,
    acceptance: str,
    analysis: dict[str, Any],
    topic_text: str | None = None,
) -> str:
    venue, year = infer_conf_parts(conf_year)
    method = (analysis.get("method") or {}).get("proposed_method_name") or ""
    experiments = analysis.get("experiments") or {}
    datasets = list_names(experiments.get("main_results") or [], "benchmark", max_items=4)
    title_zh = preferred_chinese_title(title, analysis)
    link = f"[paper]({paper_link})" if paper_link else (
        f"[paper](https://openreview.net/forum?id={openreview_forum_id})"
        if openreview_forum_id else ""
    )
    topic = topic_text or topic_text_for_note(openreview_forum_id, conf_year)
    rows = [
        ("中文题名", title_zh),
        ("英文题名", title),
        ("会议/期刊", f"{venue} {year} ({acceptance})" if year and acceptance else f"{venue} {year}" if year else venue),
        ("Links", link),
        ("Topic", topic),
        ("Method", method),
        ("Dataset", datasets),
    ]
    out = ["| 字段 | 内容 |", "|------|------|"]
    out.extend(f"| {table_cell(key)} | {table_cell(value)} |" for key, value in rows)
    return "\n".join(out)


def render_effect_callout(analysis: dict[str, Any]) -> str:
    results = ((analysis.get("experiments") or {}).get("main_results") or [])[:3]
    if not results:
        return ""
    lines = ["> [!tip] 效果简介"]
    for item in results:
        benchmark = compact_text(item.get("benchmark"), max_len=80)
        metric = item.get("metric") or "metric"
        proposed = item.get("proposed") or ""
        baseline = item.get("baseline") or ""
        delta = item.get("delta") or ""
        sentence = f"{benchmark} 上，{metric} 为 {proposed}"
        if baseline:
            sentence += f"，对比 {baseline}"
        if delta:
            sentence += f"，变化 {delta}"
        lines.append(f"> - {sentence}。")
    return "\n".join(lines)


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
    core = compact_text((analysis.get("analysis_truth") or {}).get("core_insight"), max_len=900)
    body = normalize_report_markdown(report)
    framework_blocks, experiment_blocks = figure_blocks_for_note(
        copied_figures,
        max_images=max_images,
        placements=figure_placements,
    )
    body = inject_after_heading(body, "整体框架", framework_blocks)
    body = inject_after_heading(body, "实验与分析", experiment_blocks)
    parts = [
        render_frontmatter(
            title=title,
            conf_year=conf_year,
            pdf_ref=pdf_ref,
            analysis=analysis,
            theme_bucket=theme_bucket,
            acceptance=acceptance,
            topic_text=topic_text,
        ),
        f"# {title}",
        "",
        "> [!tip] 核心洞察",
        f"> {core or '待人工复核。'}",
        "",
        render_info_table(
            title=title,
            conf_year=conf_year,
            openreview_forum_id=openreview_forum_id,
            paper_link=paper_link,
            acceptance=acceptance,
            analysis=analysis,
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


def dangling_numeric_refs(note: str, *, max_items: int = 12) -> list[str]:
    scan = re.sub(r"`[^`\n]*`", "", note)
    refs = sorted(
        set(match.group(1) for match in re.finditer(r"(?<![\w\)'!\]])\[(\d{1,3})\]", scan)),
        key=lambda value: int(value),
    )
    if not refs:
        return []
    defined = set(re.findall(r"^\s*\[(\d{1,3})\]:", scan, flags=re.MULTILINE))
    bibliography = set(re.findall(r"^\s*\[(\d{1,3})\]\s+", scan, flags=re.MULTILINE))
    return [ref for ref in refs if ref not in defined and ref not in bibliography][:max_items]


def validate_vault_note(
    note: str,
    *,
    pdf_ref: str,
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
        "acceptance",
        "tags",
        "core_operator",
        "primary_logic",
        "claims",
        "paradigm",
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
    missing_images = [path for path in note_image_paths if path not in note]
    scalar_metadata_keys = set(required_frontmatter) - {"aliases", "tags", "claims"}
    fallback_frontmatter_values = {
        key: value
        for key, value in frontmatter.items()
        if key in scalar_metadata_keys
        if value in {"", '""', "null", "unknown", "Unknown"} or "待人工" in value
    }
    fallback_markers = [
        f"{key}: {value}"
        for key, value in fallback_frontmatter_values.items()
    ]
    checks = {
        "frontmatter_valid": has_frontmatter and not missing_frontmatter,
        "required_sections_present": not missing_sections,
        "pdf_embed_present": not pdf_ref or expected_pdf_embed in note,
        "image_embeds_present": not note_image_paths or not missing_images,
        "no_pdf_file_label": "PDF 文件：" not in note,
        "no_table_cell_aliased_wikilinks": not table_rows_with_aliased_wikilinks(note),
        "no_fallback_metadata_markers": not fallback_markers,
        "no_dangling_numeric_refs": not dangling_numeric_refs(note),
        "note_length_ok": len(note.strip()) >= 1000,
    }
    return {
        "ok": all(checks.values()),
        "checks": checks,
        "note_chars": len(note),
        "missing_frontmatter": missing_frontmatter,
        "missing_sections": missing_sections,
        "pdf_ref": pdf_ref,
        "image_embed_count": len(re.findall(r"!\[[^\]]*\]\([^)]+\)", note)),
        "expected_image_count": len(note_image_paths),
        "missing_image_paths": missing_images[:12],
        "pdf_file_label_count": note.count("PDF 文件："),
        "table_cell_aliased_wikilink_lines": table_rows_with_aliased_wikilinks(note),
        "fallback_markers": fallback_markers,
        "dangling_numeric_refs": dangling_numeric_refs(note),
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
    pdf_ref = ""
    source_pdf_arg = args.paper_pdf or args.pdf
    source_pdf = Path(source_pdf_arg).resolve() if source_pdf_arg else None
    if source_pdf and source_pdf.exists():
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
        topic_text=topic_text_for_note(args.openreview_forum_id, conf_year, args.topic_assignments),
        figure_placements=figure_placements,
    )
    atomic_write_text(note_path, note)
    validation = validate_vault_note(
        note,
        pdf_ref=pdf_ref,
        copied_figures=copied_figures,
        figure_placements=figure_placements,
        max_images=args.max_note_images,
    )
    export_info = {
        "note_path": str(note_path),
        "pdf_ref": pdf_ref,
        "figure_count": len(copied_figures),
        "figure_placements": figure_placements or [],
        "asset_root": str(asset_root),
        "validation": validation,
    }
    atomic_write_json(work_dir / "report" / "vault_export.json", export_info)
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

    atomic_write_text(parse_dir / "full.md", markdown)
    figures_tables = extract_figures_tables(content_path, source_root=source_root)
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
            if deepseek_uses_reasoning(model):
                request["reasoning_effort"] = reasoning_effort
                request["extra_body"] = {"thinking": {"type": "enabled"}}
        stream = await client.chat.completions.create(**request)
        chunks: list[str] = []
        reasoning_chunks: list[str] = []
        finish_reasons: list[str] = []
        stream_chunk_count = 0
        async for chunk in stream:
            stream_chunk_count += 1
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
        "prompt_tokens_est": prompt_tokens,
        "completion_tokens_est": completion_tokens,
        "reasoning_tokens_est": reasoning_tokens,
        "total_tokens_est": prompt_tokens + completion_tokens,
        "total_with_reasoning_tokens_est": prompt_tokens + completion_tokens + reasoning_tokens,
        "estimated_cost_usd": estimate_cost_usd(model, prompt_tokens, completion_tokens),
        "cost_basis": "discounted_estimate_from_local_text_lengths",
    }
    diagnostics = {
        "content_chars": len(text),
        "reasoning_chars": len(reasoning_text),
        "finish_reason": finish_reasons[-1] if finish_reasons else "",
        "finish_reasons": finish_reasons,
        "stream_chunk_count": stream_chunk_count,
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
    )


async def llm_text(args: argparse.Namespace, *, system: str, prompt: str, max_tokens: int) -> LLMCallResult:
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
        reasoning_effort=args.reasoning_effort,
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


def part_prompt(chunk: Chunk, title: str) -> str:
    return (
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
        llm_result = await llm_text(args, system=PART_ANALYSIS_SYSTEM, prompt=prompt, max_tokens=args.part_max_tokens)
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
                retry_result = await llm_text(args, system=PART_ANALYSIS_SYSTEM, prompt=prompt, max_tokens=retry_tokens)
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

    prompt_obj = {
        "paper_title": title,
        "paper_context": compact_paper_context(markdown, max_chars=args.main_context_chars),
        "part_analyses": part_results,
        "figures_tables": figures_tables,
    }
    prompt = json.dumps(prompt_obj, ensure_ascii=False, indent=2)
    atomic_write_text(prompt_path, prompt)
    started = time.monotonic()
    usage: dict[str, Any] = {}
    if args.mock_llm:
        parsed = mock_json("main")
        parsed["paper_metadata"]["title"] = title
        raw = json.dumps(parsed, ensure_ascii=False)
    else:
        llm_result = await llm_text(args, system=MAIN_ANALYSIS_SYSTEM, prompt=prompt, max_tokens=args.main_max_tokens)
        raw = llm_result.text
        usage = usage_from_result(llm_result)
        atomic_write_text(raw_path, raw)
        try:
            parsed = parse_json_object(raw, label="main_analysis")
        except Exception as first_exc:  # noqa: BLE001
            repair_result = await llm_text(
                args,
                system=MAIN_ANALYSIS_REPAIR_SYSTEM,
                prompt=main_repair_prompt(raw),
                max_tokens=min(args.main_max_tokens, 4096),
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
    parsed = normalize_main_analysis(title, parsed)
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
) -> str:
    focused_parts = focused_part_analyses(section_title, part_results)
    focused_figures = focused_figures_tables(section_title, figures_tables)
    prompt_obj = {
        "section_title": section_title,
        "section_goal": section_goal,
        "verified_analysis": analysis,
        "focused_part_analyses": focused_parts,
        "focused_figures_tables": focused_figures,
        "context_note": "Part and figure/table context is filtered for this section; use verified_analysis for global facts.",
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
        return placements if isinstance(placements, list) else [], cached.get("usage", {}) if isinstance(cached, dict) else {}

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
    if args.mock_llm:
        placements = fallback_figure_placements(copied_figures, max_images=args.max_note_images)
    else:
        try:
            llm_result = await kimi_llm_text(
                args,
                system=FIGURE_PLACEMENT_SYSTEM,
                prompt=prompt,
                max_tokens=args.figure_placement_max_tokens,
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
    sem = asyncio.Semaphore(max(1, args.part_workers))

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
        "total_tokens_est": sum((usage.get("total_tokens_est") or 0) for _, _, usage in results),
        "estimated_cost_usd": round(sum((usage.get("estimated_cost_usd") or 0.0) for _, _, usage in results), 6),
        "cost_basis": "sum_of_section_writer_estimates",
    }
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

    if sum(bool(x) for x in (args.pdf, args.mineru_output, args.source_md)) != 1:
        raise SystemExit("Pass exactly one of --pdf, --mineru-output, or --source-md")

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
            },
            "model": "mock" if args.mock_llm else args.model,
            "provider": "mock" if args.mock_llm else args.provider,
            "writer_model": "mock" if args.mock_llm else args.writer_model,
            "writer_provider": "mock" if args.mock_llm else args.writer_provider,
            "kimi_model": "mock" if args.mock_llm else args.kimi_model,
            "reasoning_effort": "mock" if args.mock_llm else args.reasoning_effort,
            "base_url": "" if args.mock_llm else args.base_url,
            "writer_base_url": "" if args.mock_llm else args.writer_base_url,
            "kimi_base_url": "" if args.mock_llm else args.kimi_base_url,
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
                        figure_placements=figure_placements,
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
                            copied_figures=copied_figures,
                            figure_placements=figure_placements,
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
            part_total_tokens = sum(int(item.get("_meta", {}).get("usage", {}).get("total_tokens_est") or 0) for item in part_results)
            part_cost = round(sum(float(item.get("_meta", {}).get("usage", {}).get("estimated_cost_usd") or 0.0) for item in part_results), 6)
            main_usage = analysis.get("_meta", {}).get("usage", {}) if isinstance(analysis.get("_meta"), dict) else {}
            usage_summary = {
                "provider": args.provider,
                "model": args.model,
                "part_prompt_tokens_est": part_prompt_tokens,
                "part_completion_tokens_est": part_completion_tokens,
                "part_total_tokens_est": part_total_tokens,
                "part_estimated_cost_usd": part_cost,
                "main_prompt_tokens_est": int(main_usage.get("prompt_tokens_est") or 0),
                "main_completion_tokens_est": int(main_usage.get("completion_tokens_est") or 0),
                "main_total_tokens_est": int(main_usage.get("total_tokens_est") or 0),
                "main_estimated_cost_usd": float(main_usage.get("estimated_cost_usd") or 0.0),
                "writer_prompt_tokens_est": int(writer_usage.get("prompt_tokens_est") or 0),
                "writer_completion_tokens_est": int(writer_usage.get("completion_tokens_est") or 0),
                "writer_total_tokens_est": int(writer_usage.get("total_tokens_est") or 0),
                "writer_estimated_cost_usd": float(writer_usage.get("estimated_cost_usd") or 0.0),
                "figure_placement_prompt_tokens_est": int(figure_placement_usage.get("prompt_tokens_est") or 0),
                "figure_placement_completion_tokens_est": int(figure_placement_usage.get("completion_tokens_est") or 0),
                "figure_placement_total_tokens_est": int(figure_placement_usage.get("total_tokens_est") or 0),
                "figure_placement_estimated_cost_usd": float(figure_placement_usage.get("estimated_cost_usd") or 0.0),
                "figure_visual_summary_prompt_tokens_est": int(visual_summary_usage.get("prompt_tokens_est") or 0),
                "figure_visual_summary_completion_tokens_est": int(visual_summary_usage.get("completion_tokens_est") or 0),
                "figure_visual_summary_total_tokens_est": int(visual_summary_usage.get("total_tokens_est") or 0),
                "figure_visual_summary_estimated_cost_usd": float(visual_summary_usage.get("estimated_cost_usd") or 0.0),
            }
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
            usage_summary["total_tokens_est"] = (
                usage_summary["part_total_tokens_est"]
                + usage_summary["main_total_tokens_est"]
                + usage_summary["writer_total_tokens_est"]
                + usage_summary["figure_placement_total_tokens_est"]
                + usage_summary["figure_visual_summary_total_tokens_est"]
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
    parser.add_argument("--task-id", default="", help="Stable task id under output root")
    parser.add_argument("--paper-title", default="", help="Canonical paper title for vault export")
    parser.add_argument("--conf-year", default=DEFAULT_CONF_YEAR, help="Vault venue/year folder, e.g. CVPR_2026")
    parser.add_argument("--paper-link", default="", help="Canonical paper URL for note metadata")
    parser.add_argument("--acceptance", default="unknown", help="Acceptance/status metadata, e.g. accepted, workshop, arxiv, unknown")
    parser.add_argument("--openreview-forum-id", default="", help="OpenReview forum id for note metadata")
    parser.add_argument("--topic-assignments", default="", help="Optional JSONL topic assignment file keyed by OpenReview forum id")
    parser.add_argument("--theme-bucket", default="", help="Manifest theme bucket for lightweight metadata")
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
    parser.add_argument(
        "--provider",
        choices=["deepseek", "kimi"],
        default="deepseek",
        help="LLM provider. DeepSeek is the default; Kimi is used only when explicitly selected.",
    )
    parser.add_argument("--model", default="")
    parser.add_argument("--reasoning-effort", default="max", help="Reasoning effort for compatible providers.")
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
    parser.add_argument("--writer-reasoning-effort", default="max")
    parser.add_argument("--kimi-model", default="")
    parser.add_argument("--kimi-base-url", default="")
    parser.add_argument("--kimi-api-key-env", default="")
    parser.add_argument("--kimi-temperature", type=float, default=KIMI_DEFAULT_TEMPERATURE)
    parser.add_argument("--no-kimi-repair", dest="kimi_repair", action="store_false", help="Disable Kimi JSON repair fallback")
    parser.add_argument("--kimi-check-repair", dest="kimi_check_repair", action="store_true", help="Opt into final Kimi note check/repair after mechanical validation")
    parser.add_argument("--no-kimi-check-repair", dest="kimi_check_repair", action="store_false", help="Disable final Kimi note check/repair")
    parser.add_argument("--kimi-check-repair-max-tokens", type=int, default=16384)
    parser.add_argument("--part-max-tokens", type=int, default=16384)
    parser.add_argument("--main-max-tokens", type=int, default=16384)
    parser.add_argument("--writer-max-tokens", type=int, default=16384)
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
    parser.add_argument("--vault-asset-root", default=str(DEFAULT_ASSET_ROOT))
    parser.add_argument("--max-note-images", type=int, default=6)
    parser.add_argument("--mock-llm", action="store_true", help="Use deterministic local mock outputs")
    parser.add_argument("--dry-run", action="store_true", help="Parse and chunk only")
    parser.add_argument("--force", action="store_true", help="Overwrite existing stage outputs")
    parser.add_argument("--no-resume", dest="resume", action="store_false", help="Do not reuse existing stage outputs")
    parser.set_defaults(resume=True, kimi_repair=True, kimi_check_repair=False)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = asyncio.run(run_pipeline(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

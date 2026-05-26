#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize sharded analysis-chain audit reports.")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--metadata-report", default="")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def short_reason(reason: str) -> str:
    if reason.startswith("missing frontmatter keys:"):
        return "missing frontmatter keys"
    if reason.startswith("missing required sections:"):
        return "missing required sections"
    if reason.startswith("pdf_ref target missing:"):
        return "pdf_ref target missing"
    if reason.startswith("placeholder or unresolved marker remains:"):
        return "placeholder or unresolved marker remains"
    if reason.startswith("dangling numeric references:"):
        return "dangling numeric references"
    if reason.startswith("aliased wikilinks inside markdown table rows:"):
        return "aliased wikilinks inside markdown table rows"
    if reason.startswith("note appears truncated:"):
        return "note appears truncated"
    return reason


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Analysis Chain Audit Report",
        "",
        f"- generated: {payload['generated']}",
        f"- analysis_dir: `{payload['analysis_dir']}`",
        f"- worker_shards: {summary['shards']}",
        f"- checked_notes: {summary['checked_notes']}",
        f"- passed: {summary['passed']}",
        f"- failed: {summary['failed']}",
        f"- pass_rate: {summary['pass_rate']:.2%}",
        f"- warnings: {summary['warnings']}",
        f"- metadata_baseline_report: `{payload['metadata_report']}`" if payload.get("metadata_report") else "- metadata_baseline_report: none",
        "",
        "## 判定口径",
        "",
        "本报告只判定可确定的正式分析链导出完整性，不证明论文解读语义完全正确。",
        "检查项来自 `docs/formal-analysis-chain.md`、`rf-obsidian-markdown` 和正式 runner 的 vault note validation 逻辑：frontmatter、正文结构、PDF 引用与 embed、核心洞察 callout、元数据表、占位符残留、Obsidian 表格规则、旧式图片链接、悬空数字引用和明显截断。",
        "",
        "## Failure Reasons",
        "",
    ]
    if not summary["failure_reasons"]:
        lines.append("- none")
    else:
        for reason, count in summary["failure_reasons"]:
            lines.append(f"- {count}: {reason}")
    lines.extend(["", "## Failed Notes", ""])
    failed = [item for item in payload["results"] if not item["ok"]]
    if not failed:
        lines.append("- none")
    else:
        for item in failed:
            lines.append(f"- `{item['path']}`")
            for reason in item["failures"]:
                lines.append(f"  - {reason}")
    lines.extend(["", "## Warnings", ""])
    warned = [item for item in payload["results"] if item["warnings"]]
    if not warned:
        lines.append("- none")
    else:
        for item in warned[:100]:
            lines.append(f"- `{item['path']}`: {'; '.join(item['warnings'])}")
        if len(warned) > 100:
            lines.append(f"- ... {len(warned) - 100} more")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    inputs = [Path(item) for item in args.inputs]
    shard_payloads = [load_json(path) for path in inputs]
    results = [item for payload in shard_payloads for item in payload["results"]]
    results.sort(key=lambda item: item["path"])

    duplicate_paths = [path for path, count in Counter(item["path"] for item in results).items() if count > 1]
    failure_counter = Counter(short_reason(reason) for item in results for reason in item["failures"])
    passed = sum(1 for item in results if item["ok"])
    failed = len(results) - passed
    payload = {
        "generated": datetime.now().isoformat(timespec="minutes"),
        "analysis_dir": shard_payloads[0].get("analysis_dir", "obsidian-vault/analysis") if shard_payloads else "obsidian-vault/analysis",
        "metadata_report": args.metadata_report,
        "summary": {
            "shards": len(shard_payloads),
            "checked_notes": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / len(results) if results else 0,
            "warnings": sum(len(item["warnings"]) for item in results),
            "failure_reasons": failure_counter.most_common(),
            "duplicate_paths": duplicate_paths,
        },
        "shard_summaries": [
            {
                "input": repo_rel(path) if path.is_absolute() else path.as_posix(),
                "shard_index": payload.get("shard_index"),
                "checked_notes": payload.get("summary", {}).get("checked_notes"),
                "passed": payload.get("summary", {}).get("passed"),
                "failed": payload.get("summary", {}).get("failed"),
            }
            for path, payload in zip(inputs, shard_payloads, strict=False)
        ],
        "results": results,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(payload), encoding="utf-8")

    print(f"[OK] checked {len(results)} notes: {passed} passed, {failed} failed")
    print(f"[OK] report: {out_md}")
    print(f"[OK] json: {out_json}")
    if duplicate_paths:
        print(f"[WARN] duplicate paths: {len(duplicate_paths)}")
    return 0 if not duplicate_paths else 1


if __name__ == "__main__":
    raise SystemExit(main())

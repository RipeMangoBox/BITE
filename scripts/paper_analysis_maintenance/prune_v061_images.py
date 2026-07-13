#!/usr/bin/env python3
"""Prune overfull v06.1 figure sets using conservative evidence roles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "obsidian-vault" / "analysis"
EMBED_RE = re.compile(r"^!\[\[([^\]]+)\]\]\s*$")
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
CAPTION_RE = re.compile(r"^\s*(?:\*[^*].*\*|(?:Figure|Fig\.?|Table|图|表)\s*\w*\s*[:：].*)\s*$", re.I)
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
SUPPLEMENT = ("补充图", "补充表", "补充材料", "supplement", "additional figure")
LOW_VALUE = ("additional", "more examples", "more results", "supplementary", "extra", "更多样例", "更多结果", "补充结果")
ROLE_WORDS = {
    "method_overview": ("overview", "pipeline", "framework", "architecture", "method overview", "approach overview", "流程", "框架", "架构", "方法概览", "整体方法"),
    "main_result": ("main result", "quantitative result", "comparison", "benchmark", "state-of-the-art", "sota", "主结果", "定量结果", "基准", "性能对比"),
    "ablation": ("ablation", "ablations", "消融"),
    "representative_qualitative": ("qualitative", "visual comparison", "visualization", "case study", "定性", "可视化对比", "代表性样例"),
}
ROLE_ORDER = tuple(ROLE_WORDS)


@dataclass
class Image:
    index: int
    start: int
    end: int
    target: str
    caption: str
    h2: str
    h3: str
    role: str = "other"
    score: int = 0
    reasons: list[str] = field(default_factory=list)


@dataclass
class Record:
    path: str
    status: str
    image_count_before: int
    image_count_after: int
    confidence: str
    before_sha256: str
    after_sha256: str
    selected: list[dict[str, object]] = field(default_factory=list)
    removed: list[dict[str, object]] = field(default_factory=list)
    manual_review: list[str] = field(default_factory=list)
    backup: str = ""


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--paths-file", type=Path, help="One repo-relative or absolute note path per line.")
    p.add_argument("--repo-root", type=Path, default=ROOT)
    p.add_argument("--run-dir", type=Path, help="Required new directory in write mode.")
    p.add_argument("--report", type=Path, help="Dry-run JSON report path; stdout by default.")
    p.add_argument("--write", action="store_true")
    return p.parse_args()


def paths(root: Path, path_file: Path | None) -> list[Path]:
    if path_file is None:
        return sorted((root / "obsidian-vault" / "analysis").glob("*/*.md"))
    result = []
    for raw in path_file.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        path = Path(value)
        path = path if path.is_absolute() else root / path
        path = path.resolve()
        if not path.is_relative_to((root / "obsidian-vault" / "analysis").resolve()) or path.parent.parent != (root / "obsidian-vault" / "analysis").resolve():
            raise ValueError(f"not a top-level analysis note: {value}")
        result.append(path)
    return result


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def images(lines: list[str]) -> list[Image]:
    found: list[Image] = []
    h2 = h3 = ""
    for i, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if heading:
            if heading.group(1) == "##":
                h2, h3 = heading.group(2), ""
            else:
                h3 = heading.group(2)
        embed = EMBED_RE.match(line)
        if not embed:
            continue
        target = re.split(r"[#|]", embed.group(1), 1)[0]
        if not target.lower().endswith(IMAGE_EXTS):
            continue
        end = i + 1
        caption = ""
        if end < len(lines) and CAPTION_RE.match(lines[end]):
            caption, end = lines[end], end + 1
        elif end + 1 < len(lines) and not lines[end].strip() and CAPTION_RE.match(lines[end + 1]):
            # Some legacy notes separate an embed and its caption with one
            # blank line. Treat all three lines as one block so pruning cannot
            # leave the caption behind.
            caption, end = lines[end + 1], end + 2
        found.append(Image(len(found) + 1, i, end, embed.group(1), caption, h2, h3))
    return found


def classify(item: Image) -> None:
    context = f"{item.h2} {item.h3} {item.target} {item.caption}".lower()
    supplemental = any(word in f"{item.h2} {item.h3}".lower() for word in SUPPLEMENT)
    matched = [role for role, words in ROLE_WORDS.items() if any(word in context for word in words)]
    item.role = matched[0] if matched else "other"
    if matched:
        item.score += 50
        item.reasons.append(f"role:{item.role}")
    if not supplemental:
        item.score += 25
        item.reasons.append("non_supplemental_section")
    else:
        item.score -= 20
        item.reasons.append("supplemental_section")
    if item.caption:
        item.score += 10
        item.reasons.append("has_caption")
    if any(word in context for word in LOW_VALUE):
        item.score -= 35
        item.reasons.append("explicit_additional_or_more")
    if item.role == "other" and "table" in context:
        item.score += 5
        item.reasons.append("unclassified_table")


def choose(items: list[Image]) -> tuple[set[int], str, list[str]]:
    for item in items:
        classify(item)
    captioned = sum(bool(item.caption) for item in items)
    roles = {item.role for item in items if item.role != "other"}
    problems = []
    if captioned < max(4, (len(items) + 1) // 2):
        problems.append(f"caption coverage too low: {captioned}/{len(items)}")
    if len(roles) < 2:
        problems.append(f"insufficient role coverage: {sorted(roles)}")
    if problems:
        return set(), "low", problems
    selected: list[int] = []
    for role in ROLE_ORDER:
        candidates = [item for item in items if item.role == role]
        if candidates:
            selected.append(max(candidates, key=lambda x: (x.score, -x.index)).index)
    for item in sorted(items, key=lambda x: (-x.score, x.index)):
        if len(selected) == 6:
            break
        if item.index not in selected:
            selected.append(item.index)
    # If the boundary is tied and would arbitrarily split equally supported
    # images, defer to manual review instead of relying on source order.
    kept_scores = sorted((item.score for item in items if item.index in selected))
    removed_scores = sorted((item.score for item in items if item.index not in selected), reverse=True)
    if kept_scores and removed_scores and kept_scores[0] == removed_scores[0]:
        return set(), "medium", [f"selection boundary tied at score {kept_scores[0]}"]
    return set(selected), "high", []


def empty_supplemental_headings(lines: list[str]) -> set[int]:
    remove: set[int] = set()
    for i, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if not heading or not any(word in heading.group(2).lower() for word in SUPPLEMENT):
            continue
        j = i + 1
        while j < len(lines) and not HEADING_RE.match(lines[j]):
            if lines[j].strip():
                break
            j += 1
        else:
            remove.add(i)
            continue
        if j == len(lines) or HEADING_RE.match(lines[j]):
            remove.add(i)
    return remove


def transform(text: str) -> tuple[str, list[Image], set[int], str, list[str]]:
    lines = text.splitlines()
    found = images(lines)
    if len(found) <= 6:
        return text, found, {item.index for item in found}, "not_applicable", []
    keep, confidence, review = choose(found)
    if review:
        return text, found, set(), confidence, review
    removed_lines = {line for item in found if item.index not in keep for line in range(item.start, item.end)}
    interim = [line for i, line in enumerate(lines) if i not in removed_lines]
    empty = empty_supplemental_headings(interim)
    output = [line for i, line in enumerate(interim) if i not in empty]
    updated = re.sub(r"\n{3,}", "\n\n", "\n".join(output)) + ("\n" if text.endswith("\n") else "")
    return updated, found, keep, confidence, []


def atomic_write(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, path.stat().st_mode)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def main() -> int:
    opt = args()
    root = opt.repo_root.resolve()
    run = None
    if opt.write:
        if not opt.run_dir:
            raise SystemExit("--write requires --run-dir")
        run = opt.run_dir if opt.run_dir.is_absolute() else root / opt.run_dir
        if run.exists():
            raise SystemExit(f"--run-dir must not exist: {run}")
        run.mkdir(parents=True)
    records = []
    for path in paths(root, opt.paths_file):
        old = path.read_text(encoding="utf-8")
        new, found, keep, confidence, review = transform(old)
        changed = new != old
        status = "manual_review" if review else ("would_write" if changed and not opt.write else "written" if changed else "skip")
        selected = [{"target": x.target, "role": x.role, "score": x.score, "reasons": x.reasons} for x in found if x.index in keep]
        removed = [{"target": x.target, "role": x.role, "score": x.score, "reasons": x.reasons} for x in found if keep and x.index not in keep]
        rec = Record(path.relative_to(root).as_posix(), status, len(found), 6 if changed else len(found), confidence, sha(old), sha(new), selected, removed, review)
        if opt.write and changed:
            assert run
            backup = run / "backups" / path.relative_to(root)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
            rec.backup = backup.relative_to(run).as_posix()
            atomic_write(path, new)
            if sha(path.read_text(encoding="utf-8")) != rec.after_sha256:
                shutil.copy2(backup, path)
                raise RuntimeError(f"hash validation failed; restored {path}")
        records.append(asdict(rec))
    summary = {
        "mode": "write" if opt.write else "dry-run",
        "notes_scanned": len(records),
        "status_counts": {status: sum(r["status"] == status for r in records) for status in sorted({r["status"] for r in records})},
        "images_before": sum(r["image_count_before"] for r in records),
        "images_after": sum(r["image_count_after"] for r in records),
        "notes": records,
    }
    rendered = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if opt.write:
        assert run
        (run / "report.json").write_text(rendered, encoding="utf-8")
    elif opt.report:
        report = opt.report if opt.report.is_absolute() else root / opt.report
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

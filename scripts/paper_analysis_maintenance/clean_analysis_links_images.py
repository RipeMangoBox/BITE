#!/usr/bin/env python3
"""Conservatively clean links and embeds in BITE analysis notes.

The default mode is a dry run.  This script deliberately does not impose an
image count limit: it only removes redundant, low-value supplemental image
blocks when the evidence is deterministic enough to automate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


DEFAULT_ROOT = Path(__file__).resolve().parents[2]
EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
LINKS_ROW_RE = re.compile(r"^(\|\s*Links\s*\|\s*)(.*?)(\s*\|\s*)$", re.MULTILINE | re.IGNORECASE)
HEADING_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$")
CAPTION_RE = re.compile(r"^\s*(?:\*[^*].*\*|(?:Figure|Fig\.?|Table|图|表)\s*\d+\s*[:：].*)\s*$", re.IGNORECASE)
NUMBER_RE = re.compile(r"\b(?:figure|fig\.?|table)\s*([a-z]?\d+[a-z]?)\b|(?:图|表)\s*([a-z]?\d+[a-z]?)", re.IGNORECASE)
SUPPLEMENTAL_WORDS = ("补充图", "补充表", "补充材料", "supplement", "additional figures")
CORE_METHOD_WORDS = ("overview", "pipeline", "framework", "architecture", "method", "approach", "流程", "框架", "架构", "方法")
MAIN_RESULT_WORDS = ("main result", "comparison", "benchmark", "state-of-the-art", "sota", "主结果", "对比", "基准")
ABLATION_WORDS = ("ablation", "消融")
QUALITATIVE_WORDS = ("qualitative", "visual comparison", "可视化对比", "定性")
LOW_VALUE_WORDS = ("additional", "more examples", "more results", "supplementary", "extra", "更多样例", "更多结果", "补充结果")


@dataclass
class ChangeLog:
    path: str
    changed: bool = False
    embed_prefix_fixed: int = 0
    embed_unique_fixed: int = 0
    links_deduplicated: int = 0
    arxiv_labels_renamed: int = 0
    frontmatter_fields_added: int = 0
    images_removed: int = 0
    before_hash: str = ""
    after_hash: str = ""
    backup: str = ""
    unresolved: list[dict[str, object]] = field(default_factory=list)
    manual_review: list[dict[str, str]] = field(default_factory=list)
    removed_images: list[dict[str, str]] = field(default_factory=list)


@dataclass
class ImageBlock:
    start: int
    end: int
    target: str
    caption: str
    section: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths-file", type=Path, help="One repo-relative or absolute Markdown path per line.")
    parser.add_argument("--exclude-paths-file", type=Path, help="Notes to skip, one path per line.")
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--report", type=Path, help="Write the JSON report here (stdout otherwise).")
    parser.add_argument("--run-dir", type=Path, help="New run directory for write report and per-note backups.")
    parser.add_argument("--write", action="store_true", help="Apply changes; default is dry-run.")
    return parser.parse_args()


def selected_paths(root: Path, paths_file: Path | None) -> list[Path]:
    if paths_file is None:
        return sorted((root / "obsidian-vault" / "analysis").glob("*/*.md"))
    paths: list[Path] = []
    for raw in paths_file.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        path = Path(value)
        paths.append(path if path.is_absolute() else root / path)
    return paths


def path_set(root: Path, paths_file: Path | None) -> set[Path]:
    return {path.resolve() for path in selected_paths(root, paths_file)} if paths_file else set()


def asset_index(vault: Path) -> tuple[set[str], dict[str, list[str]]]:
    relative: set[str] = set()
    by_name: dict[str, list[str]] = defaultdict(list)
    for base in (vault / "assets", vault / "paperPDFs"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                rel = path.relative_to(vault).as_posix()
                relative.add(rel)
                by_name[path.name.lower()].append(rel)
    return relative, by_name


def split_embed_target(value: str) -> tuple[str, str]:
    """Return the file component and Obsidian suffix (#page / |width)."""
    positions = [pos for marker in ("#", "|") if (pos := value.find(marker)) >= 0]
    split = min(positions) if positions else len(value)
    return value[:split].strip(), value[split:]


def strip_vault_prefix(target: str) -> str:
    normalized = target.replace("\\", "/")
    while normalized.startswith("../"):
        normalized = normalized[3:]
    normalized = normalized.removeprefix("./")
    normalized = normalized.removeprefix("obsidian-vault/")
    return normalized


def fix_embeds(text: str, relative: set[str], by_name: dict[str, list[str]], log: ChangeLog) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = match.group(1)
        file_part, suffix = split_embed_target(raw)
        cleaned = strip_vault_prefix(file_part)
        candidate = cleaned
        prefix_changed = candidate != file_part
        if candidate not in relative:
            matches = by_name.get(PurePosixPath(candidate).name.lower(), [])
            if len(matches) == 1:
                candidate = matches[0]
                log.embed_unique_fixed += 1
            else:
                log.unresolved.append({
                    "kind": "missing_embed",
                    "target": raw,
                    "candidates": matches,
                })
                return match.group(0)
        if prefix_changed:
            log.embed_prefix_fixed += 1
        rewritten = f"![[{candidate}{suffix}]]"
        return rewritten

    return EMBED_RE.sub(replace, text)


def normalized_url(url: str) -> str:
    return url.strip().rstrip("/")


def fix_links(text: str, log: ChangeLog) -> str:
    def rewrite_row(match: re.Match[str]) -> str:
        links = LINK_RE.findall(match.group(2))
        if not links:
            return match.group(0)
        output: list[tuple[str, str]] = []
        seen: set[str] = set()
        for label, url in links:
            clean_label = label.strip()
            if clean_label.lower() == "arxiv":
                clean_label = "paper"
                log.arxiv_labels_renamed += 1
            key = normalized_url(url)
            if key in seen:
                log.links_deduplicated += 1
                continue
            seen.add(key)
            output.append((clean_label, url.strip()))
        content = " · ".join(f"[{label}]({url})" for label, url in output)
        return f"{match.group(1)}{content}{match.group(3)}"

    text = LINKS_ROW_RE.sub(rewrite_row, text)

    def rename_arxiv(match: re.Match[str]) -> str:
        if match.group(1).strip().lower() != "arxiv":
            return match.group(0)
        log.arxiv_labels_renamed += 1
        return f"[paper]({match.group(2)})"

    return LINK_RE.sub(rename_arxiv, text)


def add_missing_link_frontmatter(text: str, log: ChangeLog) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return text
    keys = {
        match.group(1)
        for line in lines[1:end]
        if (match := re.match(r"^([A-Za-z0-9_-]+):(?:\s|$)", line))
    }
    missing = [key for key in ("project_link", "code_link") if key not in keys]
    if not missing:
        return text
    links_match = LINKS_ROW_RE.search(text)
    links = LINK_RE.findall(links_match.group(2)) if links_match else []
    by_label = {label.strip().lower(): url.strip() for label, url in links}
    values = {
        "project_link": by_label.get("project") or "null",
        "code_link": by_label.get("code") or by_label.get("github") or "null",
    }
    insert_at = next(
        (index + 1 for index in range(1, end) if lines[index].startswith("pdf_ref:")),
        end,
    )
    for key in reversed(missing):
        lines.insert(insert_at, f"{key}: {values[key]}")
        log.frontmatter_fields_added += 1
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def collect_image_blocks(lines: list[str]) -> list[ImageBlock]:
    blocks: list[ImageBlock] = []
    section = ""
    for index, line in enumerate(lines):
        heading = HEADING_RE.match(line)
        if heading:
            section = heading.group(1).strip()
        embed = EMBED_RE.fullmatch(line.strip())
        if not embed:
            continue
        file_part, _ = split_embed_target(embed.group(1))
        if not file_part.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
            continue
        end = index + 1
        caption = ""
        if end < len(lines) and CAPTION_RE.match(lines[end]):
            caption = lines[end]
            end += 1
        blocks.append(ImageBlock(index, end, embed.group(1), caption, section))
    return blocks


def evidence_role(block: ImageBlock) -> str:
    content = f"{block.target} {block.caption}".lower()
    for role, words in (
        ("method", CORE_METHOD_WORDS),
        ("ablation", ABLATION_WORDS),
        ("main_result", MAIN_RESULT_WORDS),
        ("qualitative", QUALITATIVE_WORDS),
    ):
        if any(word in content for word in words):
            return role
    return "other"


def figure_key(block: ImageBlock) -> str:
    # A repeated Figure/Table number can legitimately refer to distinct crops
    # or panels.  Only an identical resolved asset is deterministic enough for
    # automatic deletion; looser semantic repetition remains manual-review
    # territory.
    return split_embed_target(block.target)[0].lower()


def figure_number(block: ImageBlock) -> str:
    match = NUMBER_RE.search(f"{block.target} {block.caption}")
    return (match.group(1) or match.group(2)).lower() if match else ""


def clean_redundant_supplemental_images(text: str, log: ChangeLog) -> str:
    lines = text.splitlines()
    blocks = collect_image_blocks(lines)
    seen_keys: dict[str, ImageBlock] = {}
    seen_numbers: dict[str, ImageBlock] = {}
    seen_roles: set[str] = set()
    remove: dict[int, tuple[ImageBlock, str]] = {}

    for block in blocks:
        key = figure_key(block)
        number = figure_number(block)
        role = evidence_role(block)
        supplemental = any(word in block.section.lower() for word in SUPPLEMENTAL_WORDS)
        content = f"{block.target} {block.caption}".lower()
        if supplemental and key in seen_keys:
            remove[block.start] = (block, "duplicate figure/table signature")
        elif supplemental and role == "other" and any(word in content for word in LOW_VALUE_WORDS) and seen_roles:
            remove[block.start] = (block, "explicit low-value supplemental example")
        else:
            if supplemental and number and number in seen_numbers and key != figure_key(seen_numbers[number]):
                log.manual_review.append({
                    "kind": "same_figure_number_distinct_assets",
                    "target": block.target,
                    "reason": f"shares Figure/Table {number}; may be distinct crop or panel",
                })
            seen_keys[key] = block
            if number:
                seen_numbers[number] = block
            if role != "other":
                seen_roles.add(role)

    if not remove:
        return text
    remove_lines: set[int] = set()
    for block, reason in remove.values():
        remove_lines.update(range(block.start, block.end))
        log.images_removed += 1
        log.removed_images.append({"target": block.target, "reason": reason})
    output = [line for index, line in enumerate(lines) if index not in remove_lines]
    # Collapse only blank lines made excessive by removing a complete block.
    return re.sub(r"\n{3,}", "\n\n", "\n".join(output)) + ("\n" if text.endswith("\n") else "")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_updated(text: str, relative: set[str]) -> list[dict[str, object]]:
    problems: list[dict[str, object]] = []
    for raw in EMBED_RE.findall(text):
        file_part, _ = split_embed_target(raw)
        if file_part.startswith(("../", "./", "obsidian-vault/")):
            problems.append({"kind": "invalid_embed_prefix", "target": raw})
        elif file_part.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif")) and file_part not in relative:
            problems.append({"kind": "missing_embed_after_change", "target": raw})
    return problems


def backup_path(path: Path, root: Path, run_dir: Path) -> Path:
    if path.is_relative_to(root):
        relative = path.relative_to(root)
    else:
        digest = hashlib.sha256(str(path).encode()).hexdigest()[:12]
        relative = Path("external") / f"{digest}_{path.name}"
    return run_dir / "backups" / relative


def atomic_write(path: Path, text: str) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, path.stat().st_mode)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def process(
    path: Path,
    root: Path,
    relative: set[str],
    by_name: dict[str, list[str]],
    write: bool,
    run_dir: Path | None,
) -> ChangeLog:
    display = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
    log = ChangeLog(path=display)
    if not path.is_file():
        log.unresolved.append({"kind": "missing_note", "target": str(path)})
        return log
    original = path.read_text(encoding="utf-8")
    log.before_hash = sha256(original)
    updated = add_missing_link_frontmatter(original, log)
    updated = fix_embeds(updated, relative, by_name, log)
    updated = fix_links(updated, log)
    updated = clean_redundant_supplemental_images(updated, log)
    log.changed = updated != original
    log.after_hash = sha256(updated)
    if write and log.changed:
        validation = validate_updated(updated, relative)
        if validation:
            log.unresolved.extend(validation)
            log.changed = False
            log.after_hash = log.before_hash
            return log
        assert run_dir is not None
        backup = backup_path(path, root, run_dir)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        log.backup = backup.relative_to(run_dir).as_posix()
        atomic_write(path, updated)
        if sha256(path.read_text(encoding="utf-8")) != log.after_hash:
            shutil.copy2(backup, path)
            raise RuntimeError(f"post-write hash validation failed; restored {path}")
    return log


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    run_dir: Path | None = None
    if args.write:
        if args.run_dir is None:
            raise SystemExit("--write requires --run-dir")
        run_dir = args.run_dir if args.run_dir.is_absolute() else root / args.run_dir
        if run_dir.exists():
            raise SystemExit(f"--run-dir must not already exist: {run_dir}")
        run_dir.mkdir(parents=True)
    relative, by_name = asset_index(root / "obsidian-vault")
    excluded = path_set(root, args.exclude_paths_file)
    paths = [path.resolve() for path in selected_paths(root, args.paths_file)]
    logs = [process(path, root, relative, by_name, args.write, run_dir) for path in paths if path not in excluded]
    report = {
        "mode": "write" if args.write else "dry-run",
        "notes_scanned": len(logs),
        "notes_excluded": sum(path in excluded for path in paths),
        "notes_changed": sum(log.changed for log in logs),
        "notes_with_unresolved": sum(bool(log.unresolved) for log in logs),
        "notes_with_manual_review": sum(bool(log.manual_review) for log in logs),
        "totals": {
            key: sum(getattr(log, key) for log in logs)
            for key in ("embed_prefix_fixed", "embed_unique_fixed", "links_deduplicated", "arxiv_labels_renamed", "frontmatter_fields_added", "images_removed")
        },
        "notes": [log.__dict__ for log in logs if log.changed or log.unresolved or log.manual_review],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        assert run_dir is not None
        report_path = run_dir / "report.json"
        report_path.write_text(rendered, encoding="utf-8")
    elif args.report:
        report_path = args.report if args.report.is_absolute() else root / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

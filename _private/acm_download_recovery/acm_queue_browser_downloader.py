#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "obsidian-vault/batches/wait_pdf_unified_queue_20260630/edge_acm_download_queue_20260630.csv"
DOWNLOAD_DIR = Path.home() / "Downloads/acm_sig_auto"
REPORT_DIR = ROOT / "_private/acm_download_recovery/reports"
SKIP_FILE = REPORT_DIR / "acm_queue_skip_suffixes_20260630.txt"


@dataclass
class Item:
    row: dict[str, str]
    title: str
    venue: str
    url: str
    doi_suffix: str
    target: Path


def compact(text: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", (text or "").lower())


def doi_suffix_from_url(url: str) -> str:
    match = re.search(r"/doi/pdf/10\.1145/([^?#]+)", url)
    return match.group(1) if match else ""


def is_pdf(path: Path) -> tuple[bool, str, int]:
    if not path.exists() or not path.is_file():
        return False, "missing", 0
    try:
        with path.open("rb") as handle:
            if not handle.read(8).startswith(b"%PDF"):
                return False, "not_pdf_magic", 0
        with fitz.open(path) as doc:
            pages = doc.page_count
        if pages < 1:
            return False, "zero_pages", pages
        return True, "ok", pages
    except Exception as exc:
        return False, f"{type(exc).__name__}:{exc}", 0


def title_match(path: Path, title: str) -> tuple[bool, str]:
    expected = compact(title)
    if not expected:
        return False, "empty_title"
    chunks: list[str] = []
    try:
        with fitz.open(path) as doc:
            metadata_title = (doc.metadata or {}).get("title") or ""
            if metadata_title:
                chunks.append(metadata_title)
            for i in range(min(2, doc.page_count)):
                chunks.append(doc.load_page(i).get_text("text") or "")
    except Exception as exc:
        return False, f"text_error:{type(exc).__name__}:{exc}"
    observed = compact("\n".join(chunks))
    if expected in observed:
        return True, "compact_title_exact"
    tokens = [tok for tok in re.split(r"[^0-9A-Za-z]+", title.lower()) if len(tok) >= 3]
    if not tokens:
        return False, "no_title_tokens"
    present = sum(1 for tok in tokens if compact(tok) in observed)
    ratio = present / len(tokens)
    if ratio >= 0.72:
        return True, f"token_overlap:{ratio:.2f}"
    return False, f"title_mismatch:{ratio:.2f}"


def load_skip_suffixes() -> set[str]:
    if not SKIP_FILE.exists():
        return set()
    return {line.strip() for line in SKIP_FILE.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}


def record_skip(item: Item, note: str) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_skip_suffixes()
    if item.doi_suffix in existing:
        return
    with SKIP_FILE.open("a", encoding="utf-8") as handle:
        handle.write(f"{item.doi_suffix}\t{item.title}\t{note}\n")


def load_items(limit: int = 0) -> list[Item]:
    rows = list(csv.DictReader(QUEUE.open(encoding="utf-8")))
    skip_suffixes = {line.split("\t", 1)[0] for line in load_skip_suffixes()}
    items: list[Item] = []
    for row in rows:
        url = row.get("resolved_pdf_url") or ""
        suffix = doi_suffix_from_url(url)
        target_value = row.get("target_pdf_path") or ""
        if not suffix or not target_value:
            continue
        if suffix in skip_suffixes:
            continue
        target = ROOT / target_value
        ok, _, _ = is_pdf(target)
        if ok:
            continue
        items.append(
            Item(
                row=row,
                title=row.get("paper_title") or "",
                venue=row.get("venue") or "",
                url=url,
                doi_suffix=suffix,
                target=target,
            )
        )
        if limit and len(items) >= limit:
            break
    return items


def expected_names(item: Item) -> set[str]:
    suffix = item.doi_suffix
    return {
        f"{suffix}.pdf",
        f"{suffix}.pdf.crdownload",
        f"{suffix}.pdf.part",
    }


def find_download_for(item: Item) -> Path | None:
    exact = DOWNLOAD_DIR / f"{item.doi_suffix}.pdf"
    if exact.exists():
        return exact
    escaped = re.escape(item.doi_suffix)
    pattern = re.compile(rf"^{escaped}(?: \(\d+\))?\.pdf$")
    matches = [p for p in DOWNLOAD_DIR.glob("*.pdf") if pattern.match(p.name)]
    if matches:
        return sorted(matches, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    return None


def partial_exists(item: Item) -> bool:
    suffix = item.doi_suffix
    escaped = re.escape(suffix)
    pattern = re.compile(rf"^{escaped}(?: \(\d+\))?\.pdf\.(?:crdownload|part)$")
    return any(pattern.match(path.name) for path in DOWNLOAD_DIR.iterdir() if path.is_file())


def import_item(item: Item, source: Path, dry_run: bool) -> dict[str, object]:
    ok, why, pages = is_pdf(source)
    if not ok:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        quarantine = REPORT_DIR / "invalid_pdfs_20260630"
        quarantine.mkdir(parents=True, exist_ok=True)
        dest = quarantine / source.name
        if not dry_run:
            if dest.exists():
                dest = quarantine / f"{source.stem}_{int(time.time())}{source.suffix}"
            shutil.move(str(source), dest)
        return {"ok": False, "title": item.title, "url": item.url, "source": str(source), "quarantine": str(dest), "note": why}
    matched, reason = title_match(source, item.title)
    if not matched:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        quarantine = REPORT_DIR / "unmatched_pdfs_20260630"
        quarantine.mkdir(parents=True, exist_ok=True)
        dest = quarantine / source.name
        if not dry_run:
            shutil.move(str(source), dest)
        return {
            "ok": False,
            "title": item.title,
            "url": item.url,
            "source": str(source),
            "quarantine": str(dest),
            "note": reason,
            "pages": pages,
        }
    if not dry_run:
        item.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), item.target)
    return {
        "ok": True,
        "title": item.title,
        "venue": item.venue,
        "url": item.url,
        "source": str(source),
        "target": str(item.target.relative_to(ROOT)),
        "pages": pages,
        "match": reason,
    }


def stash_preexisting() -> None:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    files = [p for p in DOWNLOAD_DIR.iterdir() if p.is_file()]
    if not files:
        return
    stash = REPORT_DIR / "preexisting_acm_sig_auto_20260630"
    stash.mkdir(parents=True, exist_ok=True)
    for path in files:
        if path.name.startswith("_codex_"):
            continue
        dest = stash / path.name
        if dest.exists():
            dest = stash / f"{path.stem}_{int(time.time())}{path.suffix}"
        shutil.move(str(path), dest)
    print(json.dumps({"event": "stashed_preexisting", "files": len(files), "stash": str(stash.relative_to(ROOT))}, ensure_ascii=False), flush=True)


def import_existing_downloads(dry_run: bool) -> tuple[int, int]:
    items = load_items(limit=0)
    by_suffix = {item.doi_suffix: item for item in items}
    ok_count = 0
    fail_count = 0
    for source in sorted(DOWNLOAD_DIR.glob("*.pdf")):
        item = by_suffix.get(source.stem)
        if not item:
            continue
        result = import_item(item, source, dry_run=dry_run)
        if result.get("ok"):
            ok_count += 1
        else:
            fail_count += 1
            record_skip(item, str(result.get("note", "import_failed")))
        print(
            json.dumps(
                {
                    "event": "existing_imported" if result.get("ok") else "existing_import_failed",
                    "ok_existing": ok_count,
                    "fail_existing": fail_count,
                    "title": item.title[:120],
                    "note": result.get("note", result.get("match", "")),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    return ok_count, fail_count


def run(args: argparse.Namespace) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if args.stash_preexisting:
        stash_preexisting()
    if args.import_existing_first:
        imported, failed = import_existing_downloads(dry_run=args.import_dry_run)
        if imported or failed:
            print(json.dumps({"event": "existing_import_complete", "imported": imported, "failed": failed}, ensure_ascii=False), flush=True)
    all_items = load_items(limit=args.total_limit)
    print(json.dumps({"event": "planned", "remaining": len(all_items), "batch_size": args.batch_size}, ensure_ascii=False), flush=True)
    if args.dry_run:
        for item in all_items[: min(20, len(all_items))]:
            print(json.dumps({"title": item.title, "url": item.url, "target": str(item.target.relative_to(ROOT))}, ensure_ascii=False))
        return

    browser = args.browser or shutil.which("microsoft-edge") or shutil.which("microsoft-edge-stable")
    if not browser:
        raise SystemExit("microsoft-edge not found")

    results: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    batch_index = 0
    while True:
        items = load_items(limit=args.batch_size)
        if not items:
            break
        batch_index += 1
        print(json.dumps({"event": "batch_start", "batch": batch_index, "items": len(items)}, ensure_ascii=False), flush=True)
        for i, item in enumerate(items, 1):
            subprocess.Popen(
                [browser, "--profile-directory=Profile 1", "--new-tab", item.url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(json.dumps({"event": "opened", "batch": batch_index, "done": i, "total": len(items), "title": item.title[:120], "url": item.url}, ensure_ascii=False), flush=True)
            time.sleep(args.delay)

        deadline = time.time() + args.wait
        imported: set[str] = set()
        while time.time() < deadline and len(imported) < len(items):
            for item in items:
                if item.doi_suffix in imported:
                    continue
                source = find_download_for(item)
                if not source or partial_exists(item):
                    continue
                try:
                    size1 = source.stat().st_size
                    time.sleep(0.2)
                    size2 = source.stat().st_size
                except FileNotFoundError:
                    continue
                if size1 != size2 or size2 <= 1000:
                    continue
                result = import_item(item, source, dry_run=args.import_dry_run)
                results.append(result)
                if not result.get("ok"):
                    failures.append(result)
                    record_skip(item, str(result.get("note", "import_failed")))
                imported.add(item.doi_suffix)
                print(json.dumps({"event": "imported" if result.get("ok") else "import_failed", "batch": batch_index, "ok_total": sum(1 for r in results if r.get("ok")), "fail_total": len(failures), "title": item.title[:120], "note": result.get("note", result.get("match", ""))}, ensure_ascii=False), flush=True)
            time.sleep(args.poll)

        missing = [item for item in items if item.doi_suffix not in imported]
        for item in missing:
            failures.append({"ok": False, "title": item.title, "url": item.url, "target": str(item.target.relative_to(ROOT)), "note": "download_timeout"})
        print(json.dumps({"event": "batch_complete", "batch": batch_index, "ok_total": sum(1 for r in results if r.get("ok")), "fail_total": len(failures), "timeouts": len(missing)}, ensure_ascii=False), flush=True)
        if args.max_batches and batch_index >= args.max_batches:
            break
        if missing and args.stop_on_timeout:
            break

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report = REPORT_DIR / f"acm_queue_browser_download_{timestamp}.json"
    report.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "queue": str(QUEUE.relative_to(ROOT)),
                "download_dir": str(DOWNLOAD_DIR),
                "ok": sum(1 for r in results if r.get("ok")),
                "failed": len(failures),
                "results": results,
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    remaining = len(load_items())
    print(json.dumps({"event": "complete", "ok": sum(1 for r in results if r.get("ok")), "failed": len(failures), "remaining": remaining, "report": str(report.relative_to(ROOT))}, ensure_ascii=False), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--delay", type=float, default=3.0)
    parser.add_argument("--wait", type=int, default=240)
    parser.add_argument("--poll", type=float, default=1.5)
    parser.add_argument("--max-batches", type=int, default=0)
    parser.add_argument("--total-limit", type=int, default=0)
    parser.add_argument("--browser", default="")
    parser.add_argument("--stash-preexisting", action="store_true")
    parser.add_argument("--import-existing-first", action="store_true")
    parser.add_argument("--stop-on-timeout", action="store_true")
    parser.add_argument("--import-dry-run", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()

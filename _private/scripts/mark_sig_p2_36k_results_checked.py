#!/usr/bin/env python3
"""Mark verified successful SIGGRAPH P2/36K analyses as checked."""

from __future__ import annotations

import csv
import json
from pathlib import Path


RESULTS = [
    Path("obsidian-vault/batches/sig_p2_36k_direct_20260627/run/results.jsonl"),
    Path("obsidian-vault/batches/sig_p2_36k_topup_20260627/run/results.jsonl"),
]
PAPER_LIST = Path("obsidian-vault/paper_list.csv")


def real_success_pdfs() -> set[str]:
    pdfs: set[str] = set()
    for path in RESULTS:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            tail = item.get("stdout_tail") or ""
            if item.get("status") == "done" and '"status": "skipped"' not in tail:
                pdfs.add(item["pdf_path"])
    return pdfs


def main() -> None:
    pdfs = real_success_pdfs()
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    changed: list[str] = []
    for row in rows:
        if row.get("pdf_path") in pdfs and row.get("state") == "Downloaded":
            row["state"] = "checked"
            changed.append(row.get("paper_title", ""))

    with PAPER_LIST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({"success_pdfs": len(pdfs), "updated": len(changed), "titles": changed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

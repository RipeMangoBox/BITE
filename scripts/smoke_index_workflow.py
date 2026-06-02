#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = REPO_ROOT / ".claude/skills/papers-build-index/scripts/build_paper_index.py"
WORKFLOW_SCRIPT = REPO_ROOT / ".claude/skills/research-workflow/scripts/research_workflow/research_workflow_entry.py"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@contextmanager
def temporary_argv(argv: list[str]):
    old = sys.argv
    sys.argv = argv
    try:
        yield
    finally:
        sys.argv = old


def patch_build_module(module: ModuleType, root: Path) -> None:
    module.REPO_ROOT = root
    module.VAULT_DIR = root / "obsidian-vault"
    module.ANALYSIS_DIR = module.VAULT_DIR / "analysis"
    module.PAPER_LIST_CSV = module.VAULT_DIR / "paper_list.csv"
    module.INDEX_DIR = module.VAULT_DIR / "index"


def patch_workflow_module(module: ModuleType, root: Path) -> None:
    module.REPO_ROOT = root
    module.PAPER_ANALYSIS = root / "obsidian-vault/analysis"
    module.PAPER_COLLECTION = root / "obsidian-vault/index"
    module.PAPER_PDFS = root / "obsidian-vault/paperPDFs"
    module.PAPER_LIST_CSV = root / "obsidian-vault/paper_list.csv"


def make_placeholder_vault(root: Path) -> None:
    vault = root / "obsidian-vault"
    for rel in ("analysis", "index", "paperPDFs", "ideas"):
        (vault / rel).mkdir(parents=True, exist_ok=True)
        (vault / rel / "README.md").write_text(f"# {rel}\n", encoding="utf-8")
    (vault / "paper_list.csv").write_text(
        "state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path\n",
        encoding="utf-8",
    )


def run_build(module: ModuleType) -> None:
    with temporary_argv(["build_paper_index.py"]):
        rc = module.main()
    if rc != 0:
        raise AssertionError(f"build_paper_index.py returned {rc}")


def assert_stage(module: ModuleType, expected: str, label: str) -> None:
    got = module.detect_stage(None)
    if got != expected:
        raise AssertionError(f"{label}: expected stage {expected!r}, got {got!r}")
    print(f"[OK] {label}: {got}")


def write_sample_note(root: Path, rel_path: str, title: str) -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                f'title: "{title}"',
                "type: paper",
                "venue: ICLR",
                "year: 2026",
                "pdf_ref: paperPDFs/ICLR_2026/sample.pdf",
                "tags:",
                "  - topic/smoke",
                "  - topic/iclr_2026",
                "core_operator: smoke operator",
                "primary_logic: smoke logic",
                "---",
                "",
                f"# {title}",
                "",
                "| Field | Value |",
                "|---|---|",
                "| Method | SmokeMethod |",
                "| Dataset | SmokeDataset (seed=1, V=128), SmokeDataset (LDA α'=0.25), OtherDataset, OtherDataset，干预层级中等难度, SyntheticData:20个变量,n=2000 |",
                "",
                "[paper](https://example.com/paper)",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_multiterm_venue_note(root: Path) -> None:
    path = root / "obsidian-vault/analysis/SIGGRAPH_Asia_2024/Multiword_Venue.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                'title: "Multiword Venue"',
                "type: paper",
                "venue: SIGGRAPH Asia",
                "year: 2024",
                "pdf_ref: paperPDFs/SIGGRAPH_Asia_2024/multiword.pdf",
                "tags:",
                "  - SIGGRAPH_ASIA_2024",
                "  - topic/smoke",
                "core_operator: smoke operator",
                "primary_logic: smoke logic",
                "---",
                "",
                "# Multiword Venue",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    build = load_module("rf_smoke_build_index", BUILD_SCRIPT)
    workflow = load_module("rf_smoke_research_workflow", WORKFLOW_SCRIPT)

    with tempfile.TemporaryDirectory(prefix="rf-index-smoke-") as tmp:
        root = Path(tmp)
        make_placeholder_vault(root)
        patch_build_module(build, root)
        patch_workflow_module(workflow, root)

        readme_before = (root / "obsidian-vault/index/README.md").read_text(encoding="utf-8")
        assert_stage(workflow, "collect", "placeholder vault")
        run_build(build)
        index_text = (root / "obsidian-vault/index/index.jsonl").read_text(encoding="utf-8")
        if index_text:
            raise AssertionError("placeholder vault should generate an empty index.jsonl")
        readme_after = (root / "obsidian-vault/index/README.md").read_text(encoding="utf-8")
        if readme_after != readme_before:
            raise AssertionError("build must not overwrite obsidian-vault/index/README.md")
        print("[OK] placeholder build: 0 papers, README preserved")

        pdf = root / "obsidian-vault/paperPDFs/ICLR_2026/sample.pdf"
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.write_bytes(b"%PDF-1.4\n")
        assert_stage(workflow, "import-local-pdfs", "local PDF only")
        pdf.unlink()

        csv_path = root / "obsidian-vault/paper_list.csv"
        for state, expected in (("Wait", "download"), ("Downloaded", "analyze"), ("checked", "query")):
            csv_path.write_text(f"title,state,pdf_ref\nSample,{state},paperPDFs/ICLR_2026/sample.pdf\n", encoding="utf-8")
            assert_stage(workflow, expected, f"CSV state {state}")
        csv_path.write_text(
            "state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path\n",
            encoding="utf-8",
        )
        csv_path.write_text(
            "\n".join(
                [
                    "state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path",
                    "checked,A,CSV Title Variant,ICLR 2026,N/A,https://example.com/csv,smoke,obsidian-vault/paperPDFs/ICLR_2026/sample.pdf",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        write_sample_note(root, "obsidian-vault/analysis/ICLR_2026/Sample_Paper.md", "Sample Paper")
        write_sample_note(root, "obsidian-vault/analysis/test/Test_Paper.md", "Test Paper")
        write_multiterm_venue_note(root)
        assert_stage(workflow, "query", "analysis note present")
        run_build(build)
        rows = [
            json.loads(line)
            for line in (root / "obsidian-vault/index/index.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        by_title = {row["title"]: row for row in rows}
        if set(by_title) != {"CSV Title Variant", "Multiword Venue"}:
            raise AssertionError(f"expected CSV Title Variant and Multiword Venue in index, got {rows!r}")
        sample = by_title["CSV Title Variant"]
        multiword = by_title["Multiword Venue"]
        if sample.get("methods") != ["SmokeMethod"]:
            raise AssertionError(f"expected exact method name to remain in index.jsonl, got {sample!r}")
        if sample.get("method_groups") != ["Other Method Family"]:
            raise AssertionError(f"expected by_method to use method family labels, got {sample!r}")
        if sample.get("venue_year") != "ICLR_2026":
            raise AssertionError(f"expected venue_year field to merge venue/year, got {sample!r}")
        if multiword.get("venue_year") != "SIGGRAPH_ASIA_2024":
            raise AssertionError(f"expected multi-word venue/year to be preserved, got {multiword!r}")
        if "Iclr 2026" in sample.get("topics", []):
            raise AssertionError(f"venue_year tags should not become research topics, got {sample!r}")
        if not (root / "obsidian-vault/index/paper_index.md").exists():
            raise AssertionError("build should generate obsidian-vault/index/paper_index.md")
        if not (root / "obsidian-vault/index/by_venue_year/venue_year_index.md").exists():
            raise AssertionError("build should generate obsidian-vault/index/by_venue_year/venue_year_index.md")
        if (root / "obsidian-vault/index/by_venue/venue_index.md").exists():
            raise AssertionError("build should not generate standalone by_venue navigation")
        if (root / "obsidian-vault/index/by_year/year_index.md").exists():
            raise AssertionError("build should not generate standalone by_year navigation")
        if (root / "obsidian-vault/index/by_method/SmokeMethod.md").exists():
            raise AssertionError("exact method names should not get standalone method navigation pages")
        if sample.get("datasets") != ["SmokeDataset", "OtherDataset", "SyntheticData"]:
            raise AssertionError(f"expected dataset details to be stripped, got {sample!r}")
        all_papers = (root / "obsidian-vault/index/_AllPapers.md").read_text(encoding="utf-8")
        if " · " in all_papers:
            raise AssertionError("paper index entries should use nested list lines, not middle-dot separators")
        if "\n\t- [[obsidian-vault/paperPDFs/ICLR_2026/sample.pdf|PDF]]" not in all_papers:
            raise AssertionError("paper index entries should render PDF links as nested list items")
        if "\n\t- datasets: SmokeDataset, OtherDataset" not in all_papers:
            raise AssertionError("paper index entries should render cleaned datasets as nested list items")
        if (root / "obsidian-vault/index/by_dataset/SmokeDataset.md").exists():
            raise AssertionError("single-paper dataset slices should not get standalone navigation pages")
        print("[OK] analysis build: 2 papers, test directory excluded")

    print("[OK] index/workflow smoke completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

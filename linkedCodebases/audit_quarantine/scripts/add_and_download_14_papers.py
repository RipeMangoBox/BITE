#!/usr/bin/env python3
"""Add 14 reference papers to paper_list.csv and download their PDFs."""

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER_LIST = REPO_ROOT / "obsidian-vault" / "paper_list.csv"
PDF_ROOT = REPO_ROOT / "obsidian-vault" / "paperPDFs"

# The 14 papers from references_to_add.md
PAPERS = [
    {
        "paper_title": "Lance: Unified Multimodal Modeling by Multi-Task Synergy",
        "venue": "arXiv 2026",
        "paper_link": "https://arxiv.org/abs/2605.18678",
        "project_link_or_github_link": "https://github.com/bytedance/Lance",
        "sort": "Unified Multimodal",
        "importance": "A",
    },
    {
        "paper_title": "EVA01: Unified Native 3D Understanding and Generation via Mixture-of-Transformers",
        "venue": "arXiv 2026",
        "paper_link": "https://arxiv.org/abs/2605.16745",
        "project_link_or_github_link": "https://www.seeles.ai/research/pages/EVA01",
        "sort": "Unified Multimodal",
        "importance": "A",
    },
    {
        "paper_title": "OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation",
        "venue": "arXiv 2025",
        "paper_link": "https://arxiv.org/abs/2510.19789",
        "project_link_or_github_link": "",
        "sort": "Multimodal Motion",
        "importance": "A",
    },
    {
        "paper_title": "OmniMotion: Multimodal Motion Generation with Continuous Masked Autoregression",
        "venue": "arXiv 2025",
        "paper_link": "https://arxiv.org/abs/2510.14954",
        "project_link_or_github_link": "",
        "sort": "Multimodal Motion",
        "importance": "A",
    },
    {
        "paper_title": "Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory",
        "venue": "arXiv 2026",
        "paper_link": "https://arxiv.org/abs/2604.08995",
        "project_link_or_github_link": "",
        "sort": "Interactive World Model",
        "importance": "A",
    },
    {
        "paper_title": "Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model",
        "venue": "arXiv 2025",
        "paper_link": "https://arxiv.org/abs/2508.13009",
        "project_link_or_github_link": "",
        "sort": "Interactive World Model",
        "importance": "B",
    },
    {
        "paper_title": "FlowAct-R1: Towards Interactive Humanoid Video Generation",
        "venue": "arXiv 2026",
        "paper_link": "https://arxiv.org/abs/2601.10103",
        "project_link_or_github_link": "",
        "sort": "Interactive Humanoid",
        "importance": "A",
    },
    {
        "paper_title": "FLAME: Adaptive Mixture-of-Experts for Continual Multimodal Multi-Task Learning",
        "venue": "arXiv 2026",
        "paper_link": "https://arxiv.org/abs/2605.09355",
        "project_link_or_github_link": "",
        "sort": "Continual Learning",
        "importance": "B",
    },
    {
        "paper_title": "SAMP: Stochastic Scene-Aware Motion Prediction",
        "venue": "ICCV 2021",
        "paper_link": "https://arxiv.org/abs/2108.08284",
        "project_link_or_github_link": "https://samp.is.tue.mpg.de",
        "sort": "Scene-Aware Motion",
        "importance": "A",
    },
    {
        "paper_title": "SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes",
        "venue": "CVPR 2023",
        "paper_link": "https://arxiv.org/abs/2301.06015",
        "project_link_or_github_link": "https://github.com/scenediffuser/Scene-Diffuser",
        "sort": "Scene-Aware Motion",
        "importance": "A",
    },
    {
        "paper_title": "HUMANISE: Language-conditioned Human Motion Generation in 3D Scenes",
        "venue": "NeurIPS 2022",
        "paper_link": "https://arxiv.org/abs/2210.09729",
        "project_link_or_github_link": "https://silverster98.github.io/HUMANISE/",
        "sort": "Scene-Aware Motion",
        "importance": "A",
    },
    {
        "paper_title": "PriorMDM: Human Motion Diffusion as a Generative Prior",
        "venue": "ICLR 2024",
        "paper_link": "https://arxiv.org/abs/2303.01418",
        "project_link_or_github_link": "https://priormdm.github.io/priorMDM-page/",
        "sort": "Human Interaction Motion",
        "importance": "B",
    },
    {
        "paper_title": "InterDiff: Generating 3D Human-Object Interactions with Physics-Informed Diffusion",
        "venue": "ICCV 2023",
        "paper_link": "https://arxiv.org/abs/2308.16905",
        "project_link_or_github_link": "https://sirui-xu.github.io/InterDiff/",
        "sort": "Human Interaction Motion",
        "importance": "B",
    },
    {
        "paper_title": "GTA-Human: Playing for 3D Human Recovery",
        "venue": "TPAMI 2024",
        "paper_link": "https://arxiv.org/abs/2110.07588",
        "project_link_or_github_link": "http://caizhongang.com/projects/GTA-Human/",
        "sort": "Dataset",
        "importance": "A",
    },
]


def arxiv_id_from_link(link: str) -> str:
    """Extract arxiv ID from link."""
    for part in link.split("/"):
        if part.startswith("2") and len(part) > 7:
            return part
    return ""


def venue_to_dir_name(venue: str) -> str:
    """Convert venue string to PDF directory name."""
    # arXiv YYYY -> arxiv_YYYY
    if venue.lower().startswith("arxiv"):
        parts = venue.split()
        if len(parts) == 2:
            return f"arxiv_{parts[1]}"
    return venue.replace(" ", "_")


def main():
    # 1. Append papers to paper_list.csv
    arxiv_ids_seen = set()

    # Read existing arxiv IDs
    with open(PAPER_LIST, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aid = arxiv_id_from_link(row.get("paper_link", ""))
            if aid:
                arxiv_ids_seen.add(aid)

    new_rows = []
    for p in PAPERS:
        aid = arxiv_id_from_link(p["paper_link"])
        if aid in arxiv_ids_seen:
            print(f"SKIP (already in CSV): {p['paper_title']}")
            continue
        arxiv_ids_seen.add(aid)

        venue_dir = venue_to_dir_name(p["venue"])
        # Sanitize filename
        safe_title = p["paper_title"].replace(":", " -").replace("/", "_").replace("?", "")
        pdf_path = f"obsidian-vault/paperPDFs/{venue_dir}/{safe_title}.pdf"

        row = {
            "state": "Wait",
            "importance": p["importance"],
            "paper_title": p["paper_title"],
            "venue": p["venue"],
            "project_link_or_github_link": p["project_link_or_github_link"],
            "paper_link": p["paper_link"],
            "sort": p["sort"],
            "pdf_path": pdf_path,
        }
        new_rows.append(row)
        print(f"ADD: {p['paper_title']}")

    if not new_rows:
        print("No new papers to add.")
        return

    # Append to CSV
    with open(PAPER_LIST, "a", newline="") as f:
        fieldnames = ["state", "importance", "paper_title", "venue",
                      "project_link_or_github_link", "paper_link", "sort", "pdf_path"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(new_rows)

    print(f"\nAdded {len(new_rows)} papers to {PAPER_LIST}")
    print("\nNow run download:")
    print(f"  python3 scripts/download_paper_list_wait.py --source {PAPER_LIST} --out-root {PDF_ROOT}")


if __name__ == "__main__":
    main()

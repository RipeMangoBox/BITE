#!/usr/bin/env python3
from pathlib import Path
from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parent
api = HfApi()
api.upload_folder(
    repo_id="RipeMangoBox/PaperBite-Assets",
    repo_type="dataset",
    folder_path=ROOT,
    commit_message="Keep PaperBite assets ICLR26-only",
    commit_description=(
        "Keep only the already-uploaded ICLR_2026 PaperBite text and figure assets. "
        "Replace the text shard/manifests and delete old non-ICLR26 asset shards."
    ),
    allow_patterns=[
        "manifests/paperbite_text_shards_manifest.jsonl",
        "manifests/paperbite_assets_manifest.jsonl",
        "manifests/paperbite_asset_shards_manifest.jsonl",
        "media/text_shards/bite_text.tar",
        "media/assets_shards/assets_iclr26.tar",
    ],
    delete_patterns=[
        "media/assets_shards/assets_icon.tar",
        "media/assets_shards/assets_papers_*.tar",
        "media/assets_shards/assets_papers_reactdance_20260602.tar",
        "manifests/paperbite_assets_summary.json",
    ],
)
print("uploaded ICLR26-only PaperBite assets")

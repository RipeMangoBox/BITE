#!/usr/bin/env python3
import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_private" / "iclr26_selection"
STATUS = ROOT / "_private" / "iclr26_batch" / "status" / "iclr26_all_papers_status.jsonl"
TOPICS = ROOT / "_private" / "topic_priority" / "iclr26_topic_assignments.jsonl"
ACCEPTED = ROOT / "_private" / "huggingface" / "resmax" / "accepted_index.csv"
CLIPPING = Path("/data/Life Me/ResearchWY Vault/Clippings/2026 ICLR 5000余篇论文分类统计图文总结.md")

CAP = 1200
LONGTAIL_PER_DIRECTION = 15


DIRECTIONS = {
    "agentic": {
        "topic_ids": set(),
        "topic_contains": ["agent", "tool use", "tool-aware"],
        "terms": [
            "agent", "agents", "agentic", "multi-agent", "multi agent", "tool use",
            "tool-use", "tool learning", "tool-aware", "tool aware", "function calling",
            "agent workflow", "planner", "planning agent", "long-horizon", "long horizon",
            "智能体", "agent-to-agent",
        ],
    },
    "rl": {
        "topic_ids": {"reinforcement_learning"},
        "topic_contains": ["reinforcement learning", "deep rl", "offline rl", "online rl"],
        "terms": [
            "reinforcement learning", "rl", "deep rl", "offline rl", "online rl",
            "policy optimization", "reward model", "reward modeling", "bandit",
            "actor-critic", "q-learning", "ppo", "dpo", "preference optimization",
            "reinforcement finetuning", "reinforcement fine-tuning", "强化学习",
        ],
    },
    "mllm_llm": {
        "topic_ids": {"llm_reasoning_agents", "multimodal_vlm", "efficient_llm_systems"},
        "topic_contains": ["language", "vision-language", "multimodal", "llm", "vlm"],
        "terms": [
            "llm", "llms", "large language model", "large language models",
            "language model", "language models", "foundation model", "mllm", "mllms",
            "multimodal", "multi-modal", "vision-language", "vision language",
            "vlm", "vlms", "lvlm", "lvlms", "video-language", "大语言模型",
            "多模态", "llm reasoning", "multimodal reasoning", "推理",
        ],
    },
    "animation_human_motion": {
        "topic_ids": set(),
        "topic_contains": ["motion", "animation", "robotics"],
        "terms": [
            "animation", "motion", "human motion", "human animation", "human-object",
            "pose", "gesture", "avatar", "humanoid", "character", "skeleton",
            "body", "talking head", "facial", "motion generation", "motion synthesis",
            "motion capture", "mocap", "动作", "人体", "动画",
        ],
    },
    "3dgs_nerf_4dgs": {
        "topic_ids": set(),
        "topic_contains": ["3d rendering", "3d reconstruction"],
        "terms": [
            "3dgs", "4dgs", "gaussian splatting", "gaussian splat", "3d gaussian",
            "4d gaussian", "nerf", "neural radiance field", "radiance field",
            "view synthesis", "novel view", "3d rendering", "3d reconstruction",
            "scene reconstruction", "camera pose", "slam", "point cloud",
        ],
    },
    "generative_model": {
        "topic_ids": {"diffusion_generation"},
        "topic_contains": ["generative", "diffusion", "image and video generation"],
        "terms": [
            "generative model", "generative models",
            "diffusion", "diffusion model", "diffusion models", "flow matching",
            "score-based", "score based", "denoising", "autoencoder", "vae",
            "video generation", "image generation", "text-to-video", "text to video",
            "text-to-image", "text to image", "生成", "扩散模型",
        ],
    },
    "efficient_inference_training": {
        "topic_ids": {"efficient_llm_systems"},
        "topic_contains": ["efficient", "systems", "scaling"],
        "terms": [
            "efficient inference", "inference acceleration", "accelerating inference",
            "efficient training", "training efficiency", "serving", "llm serving",
            "scaling law", "quantization", "pruning", "model compression",
            "distillation", "kv cache", "throughput", "latency", "高效推理", "高效训练",
        ],
    },
    "safety_robust_alignment": {
        "topic_ids": {"alignment_safety", "robustness_ood", "privacy_security"},
        "topic_contains": ["alignment", "safety", "robust", "trustworthy", "privacy", "security"],
        "terms": [
            "alignment", "align", "safety", "safe", "robust", "robustness",
            "trustworthy", "security", "privacy", "jailbreak", "red-team",
            "red team", "attack", "adversarial", "ood", "out-of-distribution",
            "preference optimization", "dpo", "rlhf", "安全", "鲁棒", "对齐",
        ],
    },
    "video": {
        "topic_ids": set(),
        "topic_contains": ["video"],
        "terms": [
            "video", "videos", "text-to-video", "video generation", "video understanding",
            "video question answering", "temporal", "spatio-temporal", "spatiotemporal",
            "action recognition", "video frame", "视频理解", "视频生成",
        ],
    },
}


CORE_DIRECTIONS = [
    "agentic",
    "rl",
    "mllm_llm",
    "animation_human_motion",
    "3dgs_nerf_4dgs",
    "generative_model",
]

PRIMARY_DIRECTION_ORDER = [
    "3dgs_nerf_4dgs",
    "animation_human_motion",
    "video",
    "rl",
    "generative_model",
    "agentic",
    "mllm_llm",
    "efficient_inference_training",
    "safety_robust_alignment",
]

BIG_LABS = [
    "google", "deepmind", "openai", "anthropic", "meta", "fair", "microsoft",
    "nvidia", "apple", "amazon", "aws", "adobe", "ibm", "salesforce", "bytedance",
    "tiktok", "alibaba", "tencent", "baidu", "huawei", "stanford", "mit",
    "carnegie mellon", "cmu", "berkeley", "uc berkeley", "princeton", "harvard",
    "oxford", "cambridge", "tsinghua", "peking university", "pku", "ustc",
    "university of toronto", "nyu", "cornell", "uiuc", "eth", "epfl",
    "kaist", "seoul national", "max planck", "inria",
]


def load_jsonl(path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def norm_text(*parts):
    return " ".join(str(p or "") for p in parts).lower()


def clean_title(title):
    return re.sub(r"\s+", " ", title or "").strip()


def as_float(value, default=0.0):
    try:
        if value in ("", None):
            return default
        return float(value)
    except ValueError:
        return default


def as_int(value, default=0):
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except ValueError:
        return default


def id_or_title_key(row):
    oid = row.get("openreview_forum_id") or ""
    if oid:
        return ("id", oid)
    return ("title", clean_title(row.get("title", "")).lower())


def term_hits(text, terms):
    hits = []
    for term in terms:
        needle = term.lower()
        if re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", text):
            hits.append(term)
    return hits


def direction_matches(paper):
    primary = paper.get("primary_topic") or {}
    secondary = paper.get("secondary_topics") or []
    topic_ids = {primary.get("topic_id", "")}
    topic_ids.update(t.get("topic_id", "") for t in secondary)
    topic_labels = " ".join([primary.get("label", "")] + [t.get("label", "") for t in secondary])
    resmax_topic = paper.get("topic", "")
    text = norm_text(
        paper.get("title"),
        paper.get("abstract_raw"),
        paper.get("abstract_excerpt"),
        paper.get("snippet_excerpt"),
        resmax_topic,
        topic_labels,
    )
    matches = {}
    for direction, spec in DIRECTIONS.items():
        hits = term_hits(text, spec["terms"])
        by_topic_id = bool(topic_ids & spec["topic_ids"])
        topic_text = norm_text(topic_labels, resmax_topic)
        by_topic_name = any(x in topic_text for x in spec["topic_contains"])
        if hits or by_topic_id or by_topic_name:
            matches[direction] = {
                "terms": hits[:20],
                "topic_id_match": sorted(topic_ids & spec["topic_ids"]),
                "topic_name_match": by_topic_name,
            }
    return matches


def priority_score(paper):
    review = as_float(paper.get("review_score_mean"))
    topic_score = as_float((paper.get("primary_topic") or {}).get("score"))
    stars = as_int(paper.get("code_stars"))
    citations = as_int(paper.get("citation_count"))
    code_url = paper.get("code_url") or ""
    code_real = str(paper.get("code_is_real") or "").lower() == "yes"
    has_code = bool(code_url)
    lab_hit = any(lab in norm_text(paper.get("authors"), paper.get("source_url"), paper.get("landing_url")) for lab in BIG_LABS)
    complete_open = code_real or (has_code and any(x in code_url.lower() for x in ["github.com", "gitlab.com", "huggingface.co"]))
    score = 0.0
    score += review * 12.0
    score += topic_score
    score += min(math.log1p(stars) * 6.0, 45.0)
    score += min(math.log1p(citations) * 4.0, 25.0)
    score += 18.0 if complete_open else (8.0 if has_code else 0.0)
    score += 8.0 if lab_hit else 0.0
    score += 6.0 if paper.get("analysis_status") == "completed" else 0.0
    score += 3.0 if paper.get("pdf_exists") else 0.0
    if paper.get("acceptance_type") == "Oral":
        score += 10000.0
    return round(score, 4), {
        "review_score_mean": review,
        "primary_topic_score": topic_score,
        "code_url_present": has_code,
        "code_is_real": code_real,
        "complete_open_source_signal": complete_open,
        "code_stars": stars,
        "citation_count": citations,
        "big_lab_signal": lab_hit,
        "analysis_completed": paper.get("analysis_status") == "completed",
    }


def primary_direction(matches):
    for direction in PRIMARY_DIRECTION_ORDER:
        if direction in matches:
            return direction
    return sorted(matches)[0] if matches else "forced_without_direction"


def allocate_direction_caps(posters, slots):
    by_direction = defaultdict(list)
    for paper in posters:
        by_direction[paper["primary_selection_direction"]].append(paper)
    if slots <= 0 or not by_direction:
        return {}

    min_floor = min(20, max(1, slots // max(1, len(by_direction)) // 3))
    caps = {}
    remaining = slots
    for direction, items in sorted(by_direction.items()):
        floor = min(len(items), min_floor if direction in CORE_DIRECTIONS else 5)
        caps[direction] = floor
        remaining -= floor

    if remaining <= 0:
        return caps

    weights = {
        direction: len(items)
        for direction, items in by_direction.items()
        if len(items) > caps.get(direction, 0)
    }
    total = sum(weights.values())
    remainders = []
    for direction, weight in weights.items():
        raw = remaining * weight / total if total else 0
        extra = min(len(by_direction[direction]) - caps[direction], int(raw))
        caps[direction] += extra
        remainders.append((raw - int(raw), len(by_direction[direction]), direction))

    assigned = sum(caps.values())
    for _, _, direction in sorted(remainders, reverse=True):
        if assigned >= slots:
            break
        if caps[direction] < len(by_direction[direction]):
            caps[direction] += 1
            assigned += 1
    return caps


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    status = {}
    for row in load_jsonl(STATUS):
        status[id_or_title_key(row)] = row

    topic_rows = {}
    for row in load_jsonl(TOPICS):
        topic_rows[id_or_title_key(row)] = row

    accepted_by_key = {}
    accepted_iclr = 0
    local_oral_ids = set()
    best_ids = set()
    with ACCEPTED.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("conf_year") != "ICLR_2026":
                continue
            accepted_iclr += 1
            key = id_or_title_key(row)
            accepted_by_key[key] = row
            fields = norm_text(row.get("decision"), row.get("acceptance_type"), row.get("session"), row.get("eventtype"), row.get("event_type"))
            oid = row.get("openreview_forum_id") or ""
            if oid and "oral" in fields:
                local_oral_ids.add(oid)
            if oid and ("best paper" in fields or row.get("acceptance_type", "").lower() in {"best", "best paper"}):
                best_ids.add(oid)

    papers = []
    missing_accepted = 0
    missing_topic = 0
    for key, base in status.items():
        paper = dict(base)
        topic = topic_rows.get(key, {})
        acc = accepted_by_key.get(key, {})
        if not topic:
            missing_topic += 1
        if not acc:
            missing_accepted += 1
        paper.update({
            "abstract_excerpt": topic.get("abstract_excerpt", ""),
            "snippet_excerpt": topic.get("snippet_excerpt", ""),
            "primary_topic": topic.get("primary_topic", {}),
            "secondary_topics": topic.get("secondary_topics", []),
            "all_topic_scores": topic.get("all_topic_scores", []),
            "authors": acc.get("authors", ""),
            "abstract_raw": acc.get("abstract_raw", ""),
            "decision": acc.get("decision", ""),
            "acceptance_type": acc.get("acceptance_type", ""),
            "resmax_topic": acc.get("topic", ""),
            "topic": acc.get("topic", ""),
            "code_url": acc.get("code_url", ""),
            "code_is_real": acc.get("code_is_real", ""),
            "code_stars": acc.get("code_stars", ""),
            "citation_count": acc.get("citation_count", ""),
            "review_score_mean": acc.get("review_score_mean", ""),
            "review_scores": acc.get("review_scores", ""),
            "review_available": acc.get("review_available", ""),
            "paper_url": acc.get("paper_url", ""),
            "virtualsite_url": acc.get("virtualsite_url", ""),
            "session": acc.get("session", ""),
            "eventtype": acc.get("eventtype", ""),
            "event_type": acc.get("event_type", ""),
        })
        matches = direction_matches(paper)
        score, signals = priority_score(paper)
        paper["matched_directions"] = matches
        paper["selection_score"] = score
        paper["priority_signals"] = signals
        paper["presentation_forced"] = paper.get("openreview_forum_id") in local_oral_ids
        paper["best_paper_forced"] = paper.get("openreview_forum_id") in best_ids
        paper["eligible_by_direction"] = bool(matches)
        paper["primary_selection_direction"] = primary_direction(matches)
        papers.append(paper)

    eligible = [p for p in papers if p["eligible_by_direction"] or p["presentation_forced"] or p["best_paper_forced"]]
    forced = [p for p in eligible if p["presentation_forced"] or p["best_paper_forced"]]
    posters = [p for p in eligible if not (p["presentation_forced"] or p["best_paper_forced"])]
    poster_slots = max(0, CAP - len(forced))
    direction_caps = allocate_direction_caps(posters, poster_slots)
    posters_by_direction = defaultdict(list)
    for paper in posters:
        posters_by_direction[paper["primary_selection_direction"]].append(paper)
    selected_posters = []
    for direction, items in posters_by_direction.items():
        items.sort(key=lambda p: (-p["selection_score"], p.get("index", 10**9), p.get("title", "")))
        selected_posters.extend(items[:direction_caps.get(direction, 0)])
    selected = forced + selected_posters
    selected.sort(key=lambda p: (not (p["presentation_forced"] or p["best_paper_forced"]), p["primary_selection_direction"], -p["selection_score"], p.get("index", 10**9)))
    selected_keys = {id_or_title_key(p) for p in selected}
    excluded = [p for p in eligible if id_or_title_key(p) not in selected_keys]

    longtail = []
    seen = set()
    for direction in DIRECTIONS:
        candidates = [p for p in excluded if direction in p["matched_directions"]]
        candidates.sort(key=lambda p: (-p["selection_score"], p.get("index", 10**9), p.get("title", "")))
        for p in candidates[:LONGTAIL_PER_DIRECTION]:
            key = id_or_title_key(p)
            if key in seen:
                continue
            seen.add(key)
            longtail.append({
                "openreview_forum_id": p.get("openreview_forum_id", ""),
                "title": p.get("title", ""),
                "directions": sorted(p["matched_directions"].keys()),
                "selection_score": p["selection_score"],
                "priority_signals": p["priority_signals"],
                "reason": "excluded by 1200 cap but retained in long-tail top15 for at least one matched direction",
            })

    def compact(p, rank, selected_flag=True):
        primary = p.get("primary_topic") or {}
        return {
            "selection_rank": rank,
            "selected": selected_flag,
            "openreview_forum_id": p.get("openreview_forum_id", ""),
            "title": p.get("title", ""),
            "authors": p.get("authors", ""),
            "conf_year": p.get("conf_year", "ICLR_2026"),
            "path": p.get("path", ""),
            "pdf_exists": p.get("pdf_exists", False),
            "analysis_status": p.get("analysis_status", ""),
            "decision": p.get("decision", ""),
            "acceptance_type": p.get("acceptance_type", ""),
            "session": p.get("session", ""),
            "topic": p.get("topic", ""),
            "primary_topic_id": primary.get("topic_id", ""),
            "primary_topic_label": primary.get("label", ""),
            "primary_topic_score": primary.get("score", 0),
            "matched_directions": sorted(p["matched_directions"].keys()),
            "primary_selection_direction": p["primary_selection_direction"],
            "match_evidence": p["matched_directions"],
            "selection_score": p["selection_score"],
            "priority_signals": p["priority_signals"],
            "force_include_reason": (
                "best_paper" if p["best_paper_forced"] else
                "oral" if p["presentation_forced"] else
                ""
            ),
            "code_url": p.get("code_url", ""),
            "paper_url": p.get("paper_url", ""),
            "abstract_excerpt": (p.get("abstract_raw") or p.get("abstract_excerpt") or "")[:1000],
        }

    with (OUT / "iclr26_selected_1200.jsonl").open("w", encoding="utf-8") as f:
        for i, p in enumerate(selected, 1):
            f.write(json.dumps(compact(p, i), ensure_ascii=False, sort_keys=True) + "\n")

    selected_direction_counts = Counter()
    eligible_direction_counts = Counter()
    excluded_direction_counts = Counter()
    for p in selected:
        for d in p["matched_directions"]:
            selected_direction_counts[d] += 1
    for p in eligible:
        for d in p["matched_directions"]:
            eligible_direction_counts[d] += 1
    for p in excluded:
        for d in p["matched_directions"]:
            excluded_direction_counts[d] += 1

    selected_primary_direction = Counter()
    eligible_primary_direction = Counter()
    excluded_primary_direction = Counter()
    for p in selected:
        selected_primary_direction[p["primary_selection_direction"]] += 1
    for p in eligible:
        eligible_primary_direction[p["primary_selection_direction"]] += 1
    for p in excluded:
        excluded_primary_direction[p["primary_selection_direction"]] += 1

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent": "agent_1",
        "cap": CAP,
        "input_files": {
            "status": str(STATUS.relative_to(ROOT)),
            "topic_assignments": str(TOPICS.relative_to(ROOT)),
            "accepted_index": str(ACCEPTED.relative_to(ROOT)),
            "icml26_direction_clipping_reference": str(CLIPPING),
        },
        "candidate_pool_status_count": len(status),
        "topic_assignment_count": len(topic_rows),
        "accepted_index_iclr2026_count": accepted_iclr,
        "eligible_after_direction_or_forced_count": len(eligible),
        "selected_count": len(selected),
        "excluded_by_cap_count": len(excluded),
        "longtail_high_value_supplement_count": len(longtail),
        "forced_oral_found_count": len(local_oral_ids),
        "forced_oral_selected_count": sum(1 for p in selected if p["presentation_forced"]),
        "forced_best_paper_found_count": len(best_ids),
        "forced_best_paper_selected_count": sum(1 for p in selected if p["best_paper_forced"]),
        "best_paper_data_status": "not_found_in_local_fields",
        "missing_accepted_metadata_for_status_count": missing_accepted,
        "missing_topic_assignment_for_status_count": missing_topic,
        "selected_direction_counts_multi_label": dict(sorted(selected_direction_counts.items())),
        "eligible_direction_counts_multi_label": dict(sorted(eligible_direction_counts.items())),
        "excluded_direction_counts_multi_label": dict(sorted(excluded_direction_counts.items())),
        "selected_primary_direction_counts": dict(sorted(selected_primary_direction.items())),
        "eligible_primary_direction_counts": dict(sorted(eligible_primary_direction.items())),
        "excluded_primary_direction_counts": dict(sorted(excluded_primary_direction.items())),
        "core_direction_coverage": {d: selected_direction_counts.get(d, 0) for d in CORE_DIRECTIONS},
        "clipping_terms_used_as_vocabulary_only": [
            "LLM", "大语言模型", "高效推理/训练", "Reasoning/推理", "Agent/智能体",
            "Diffusion Models", "多模态", "安全/鲁棒性", "强化学习",
            "Alignment/对齐", "视频理解/生成",
        ],
        "ranking_signal_order": [
            "force include local Best Paper/Oral",
            "primary direction assignment and per-direction poster caps",
            "review_score_mean",
            "topic match score",
            "complete open-source signal/code URL/code stars",
            "citation_count if present",
            "big lab/group string signal",
            "analysis completed/PDF available",
            "stable original index tie-break",
        ],
        "poster_slots_after_forced": poster_slots,
        "poster_direction_caps": dict(sorted(direction_caps.items())),
    }
    (OUT / "selection_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rules = f"""# ICLR 2026 Selection Rules

Generated: {summary['generated_at']}

## Scope

This selection uses only local files. The candidate universe is `_private/iclr26_batch/status/iclr26_all_papers_status.jsonl` ({len(status)} rows), enriched with `_private/topic_priority/iclr26_topic_assignments.jsonl` and `_private/huggingface/resmax/accepted_index.csv`.

The Xiaohongshu/ICML26-derived clipping at `{CLIPPING}` is used only as a vocabulary reference. Its category proportions are not used for quota allocation.

## Direction Filter

First-pass inclusion requires at least one target direction match in title, abstract, topic assignment, or accepted-index topic. Required directions are covered:

- `agentic`: agent, tool use, planning, long-horizon, multi-agent, 智能体.
- `rl`: reinforcement learning, offline/online/deep RL, reward modeling, policy optimization, preference optimization, 强化学习.
- `mllm_llm`: LLM, large language model, MLLM, VLM, multimodal, vision-language, reasoning, 大语言模型, 多模态.
- `animation_human_motion`: animation, human motion, pose, avatar, talking head, skeleton, motion generation.
- `3dgs_nerf_4dgs`: 3DGS, 4DGS, Gaussian splatting, NeRF, neural radiance field, view synthesis, 3D reconstruction.
- `generative_model`: diffusion, generative model, flow matching, denoising, image/video/text-to-image/text-to-video generation.

Additional user-specified vocabulary is included through `efficient_inference_training`, `safety_robust_alignment`, and `video`.

## Forced Inclusion

All locally identifiable oral papers are forced into the selected set before poster trimming. Local data contains {len(local_oral_ids)} Oral papers, all with OpenReview IDs in the status pool. No Best Paper field or local Best Paper label was found in the inspected files, so no Best Paper force-inclusion could be applied. Required data source: official ICLR 2026 awards/best-paper list with OpenReview forum IDs or exact titles.

## Priority Score

Poster trimming is performed inside a deterministic primary direction class. If a paper matches multiple directions, primary class is assigned in this order: `{', '.join(PRIMARY_DIRECTION_ORDER)}`. This keeps narrow target classes such as 3DGS/NeRF/4DGS and animation/human motion from being swallowed by broad LLM or generative matches.

Poster priority inside each class is deterministic:

1. Review score mean, if available.
2. Local topic match score.
3. Complete open-source signal: real code, GitHub/GitLab/HuggingFace URL, and code stars.
4. Citation count, if present.
5. Large company or major lab string signal in local metadata.
6. Existing completed analysis and local PDF availability.
7. Original status index/title as stable tie-breakers.

The score is used only for ordering within the matched candidate pool. It is not a claim of paper quality beyond the available local metadata.

## Cap and Long Tail

If eligible papers exceed {CAP}, forced papers are kept and ordinary posters are trimmed inside their primary direction class. Poster slots are allocated from the current local ICLR26 eligible pool, with a small floor for core directions and proportional remainder by local class size. This does not use the ICML26 clipping proportions. Excluded posters are then sorted within each matched direction; top {LONGTAIL_PER_DIRECTION} per direction are recorded in the audit as long-tail high-value supplements, prioritizing the same citation/open-source/lab/review signals. Other excluded papers are only judged from local title/abstract/topic metadata.
"""
    (OUT / "selection_rules.md").write_text(rules, encoding="utf-8")

    top_excluded = sorted(excluded, key=lambda p: (-p["selection_score"], p.get("index", 10**9)))[:50]
    audit_lines = [
        "# ICLR 2026 Selection Audit",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Counts",
        "",
        f"- Status candidate pool: {len(status)}",
        f"- Topic assignments: {len(topic_rows)}",
        f"- Accepted-index ICLR 2026 rows: {accepted_iclr}",
        f"- Eligible after direction or forced inclusion: {len(eligible)}",
        f"- Selected: {len(selected)}",
        f"- Excluded by 1200 cap: {len(excluded)}",
        f"- Oral papers found locally: {len(local_oral_ids)}; selected: {summary['forced_oral_selected_count']}",
        f"- Best Paper labels found locally: {len(best_ids)}",
        f"- Poster slots after forced papers: {poster_slots}",
        "",
        "## Poster Direction Caps",
        "",
        "| Primary direction | Cap |",
        "|---|---:|",
    ]
    for d, c in sorted(direction_caps.items()):
        audit_lines.append(f"| {d} | {c} |")
    audit_lines += [
        "",
        "## Direction Counts",
        "",
        "| Direction | Eligible | Selected | Excluded |",
        "|---|---:|---:|---:|",
    ]
    for d in sorted(DIRECTIONS):
        audit_lines.append(f"| {d} | {eligible_direction_counts.get(d, 0)} | {selected_direction_counts.get(d, 0)} | {excluded_direction_counts.get(d, 0)} |")
    audit_lines += [
        "",
        "## Long-Tail High-Value Supplements",
        "",
        "These are not in `iclr26_selected_1200.jsonl`; they are retained here for optional manual add-back after capacity changes.",
        "",
    ]
    for item in longtail:
        audit_lines.append(f"- `{item['openreview_forum_id']}` {item['title']} | directions={','.join(item['directions'])} | score={item['selection_score']}")
    audit_lines += [
        "",
        "## Highest-Scoring Excluded Posters",
        "",
    ]
    for p in top_excluded:
        audit_lines.append(
            f"- `{p.get('openreview_forum_id','')}` {p.get('title','')} | directions={','.join(sorted(p['matched_directions']))} | score={p['selection_score']} | review={p['priority_signals']['review_score_mean']} | code={p['priority_signals']['code_url_present']}"
        )
    audit_lines += [
        "",
        "## Risks and Gaps",
        "",
        "- Best Paper data was not discoverable in local fields inspected here; official award metadata is needed for guaranteed inclusion.",
        f"- Status/topic pool has {len(status)} rows, while accepted_index has {accepted_iclr} ICLR_2026 rows; the output intentionally uses the current status pool as the candidate universe.",
        "- Large-lab detection is string-based from local metadata and is therefore conservative.",
        "- Citation counts are mostly absent in the local ICLR 2026 rows; score relies more on review/topic/code signals.",
        "- Direction matching is lexical/topic-based and can miss papers whose abstract uses indirect terminology.",
    ]
    (OUT / "selection_audit.md").write_text("\n".join(audit_lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

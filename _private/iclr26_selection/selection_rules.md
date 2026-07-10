# ICLR 2026 Selection Rules

Generated: 2026-05-15T13:03:28.807290+00:00

## Scope

This selection uses only local files. The candidate universe is `_private/iclr26_batch/status/iclr26_all_papers_status.jsonl` (5348 rows), enriched with `_private/topic_priority/iclr26_topic_assignments.jsonl` and `_private/huggingface/resmax/accepted_index.csv`.

The Xiaohongshu/ICML26-derived clipping at `/data/Life Me/ResearchWY Vault/Clippings/2026 ICLR 5000余篇论文分类统计图文总结.md` is used only as a vocabulary reference. Its category proportions are not used for quota allocation.

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

All locally identifiable oral papers are forced into the selected set before poster trimming. Local data contains 225 Oral papers, all with OpenReview IDs in the status pool. No Best Paper field or local Best Paper label was found in the inspected files, so no Best Paper force-inclusion could be applied. Required data source: official ICLR 2026 awards/best-paper list with OpenReview forum IDs or exact titles.

## Priority Score

Poster trimming is performed inside a deterministic primary direction class. If a paper matches multiple directions, primary class is assigned in this order: `3dgs_nerf_4dgs, animation_human_motion, video, rl, generative_model, agentic, mllm_llm, efficient_inference_training, safety_robust_alignment`. This keeps narrow target classes such as 3DGS/NeRF/4DGS and animation/human motion from being swallowed by broad LLM or generative matches.

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

If eligible papers exceed 1200, forced papers are kept and ordinary posters are trimmed inside their primary direction class. Poster slots are allocated from the current local ICLR26 eligible pool, with a small floor for core directions and proportional remainder by local class size. This does not use the ICML26 clipping proportions. Excluded posters are then sorted within each matched direction; top 15 per direction are recorded in the audit as long-tail high-value supplements, prioritizing the same citation/open-source/lab/review signals. Other excluded papers are only judged from local title/abstract/topic metadata.

# Fine-Grained Taxonomy Design

- generated_at: `2026-05-12`
- scope: `ICLR 2026`, `CVPR 2026`, `NeurIPS 2025`, `ICML 2026`
- goal: replace the current coarse topic buckets with a finer taxonomy that has explicit provenance

## Short Answers

### 1. Does `resmax` already contain paper-level classification?

No, not in a useful paper-level topic sense.

- `_private/resmax_downloads/manifest.jsonl` has download metadata such as `conf_year`, `openreview_forum_id`, `title`, `output_pdf`, `output_meta`.
- `_private/resmax_downloads/meta/ICLR_2026/*.json` also only stores lightweight download metadata like `title`, `sha256`, `size_bytes`, `candidate_urls`.
- There is no stable paper-level `topic`, `keywords`, `primary_area`, or official taxonomy field in the current `resmax` outputs.
- The earlier `theme_bucket` logic in batch scripts is a local title-keyword heuristic, not a `resmax` classification.

Conclusion:

- `resmax` is a source of PDF identity and paths.
- `resmax` is not a source of reliable paper-topic labels.

### 2. Do official sources already have classification?

Yes, but unevenly across conferences.

#### ICLR 2026

- OpenReview accepted notes expose `primary_area` and `keywords`.
- Official virtual data exposes a two-level `topic` field like:
  - `Computer Vision->Vision Models & Multimodal`
  - `Applications->Language, Speech and Dialog`
  - `Deep Learning->Generative Models and Autoencoders`
- In the public virtual dump I counted `58` unique leaf topics under `9` root buckets.

#### NeurIPS 2025

- OpenReview accepted notes expose `primary_area` and `keywords`.
- Official virtual data exposes a similar two-level `topic` field.
- In the public virtual dump I counted `60` unique leaf topics under `11` root buckets.

#### ICML 2026

- Official virtual data exposes a two-level `topic` field.
- In the public virtual dump I counted `77` unique leaf topics under `9` root buckets.
- But coverage is weak: `Unlabeled` dominates, so official taxonomy is present but sparse.

#### CVPR 2026

- I did not recover a reliable official structured topic dump comparable to ICLR / NeurIPS / ICML.
- The official virtual pages expose papers and orals, but I did not find a stable official public topic taxonomy endpoint in this pass.

Conclusion:

- `ICLR 2026` and `NeurIPS 2025` have the best official classification anchors.
- `ICML 2026` has official topics, but many papers are unlabeled.
- `CVPR 2026` currently needs a non-official supplement if you want fine-grained categories.

### 3. Are there reliable / high-recognition GitHub repos that classify these conference years?

There are some useful repos, but they are not equally reliable and they do not cover all four conference/year pairs in a single authoritative way.

#### Strongest GitHub source for `ICLR`

- `berenslab/iclr-dataset`
- This is the best GitHub source I found for structured ICLR labeling.
- It is an academic dataset repo, not just a community paper list.
- It states that version `26v1` contains `55,906` ICLR submissions from `2017` to `2026`.
- It also documents evolving label classes such as `safety`, `alignment`, `code generation`, `autonomous driving`, `knowledge graph`, `neuroscience`.
- Limitation: it only covers ICLR, not CVPR / NeurIPS / ICML.

#### Strongest GitHub source for `CVPR`

- `amusi/CVPR2026-Papers-with-Code`
- This is a very high-visibility community repo with `22.5k` stars at the time I checked.
- It does have explicit sections such as `3DGS`, `MLLM`, `LLM`, `Diffusion Models`, `Object Detection`, `Vision-Language`, `Medical Image Segmentation`, `Autonomous Driving`, `3D Reconstruction`, `Video Compression`.
- Limitation: community-curated, not official, category granularity is uneven, and coverage quality varies by section.

#### Strong subdomain GitHub source across multiple venues

- `Songwxuan/Embodied-AI-Paper-TopConf`
- High value if you care about embodied AI specifically.
- It spans `ICLR 2026`, `NeurIPS 2025`, and multiple other top venues.
- It has explicit subcategories such as `Vision-Language-Action Models`, `World Models`, `Planning and Reasoning`, `Navigation`, `Humanoid`, `3D Vision`, `Policy`, `Dexterous Manipulation`, `Tactile`, `Benchmark and Dataset`.
- Limitation: only embodied AI, not full-conference coverage.

#### What I did **not** find

- I did not find a single widely recognized GitHub repo that gives authoritative, fine-grained, conference-wide classification for all of:
  - `ICLR 2026`
  - `CVPR 2026`
  - `NeurIPS 2025`
  - `ICML 2026`

Conclusion:

- For `ICLR`, `berenslab/iclr-dataset` is the strongest structured GitHub source.
- For `CVPR`, `amusi/CVPR2026-Papers-with-Code` is the strongest community classification source.
- For embodied-AI slices across conferences, `Songwxuan/Embodied-AI-Paper-TopConf` is strong.
- There is no single fully authoritative GitHub taxonomy covering all four targets.

## Recommended Fine-Grained Standard

Do **not** use a single flat label space.

Use a **4-layer taxonomy**:

### Layer 0: Venue-specific provenance

Every paper keeps:

- `conference`
- `year`
- `openreview_forum_id`
- `official_primary_area` if available
- `official_topic_root` if available
- `official_topic_leaf` if available
- `official_keywords` if available
- `source_of_label`

This makes later auditing possible.

### Layer 1: Unified root domain

Map all conferences into a shared root taxonomy:

1. `foundation_models_llm`
2. `multimodal_vlm_mllm`
3. `vision_image_video_3d`
4. `generative_models_diffusion`
5. `reinforcement_learning_planning_agents`
6. `representation_self_supervised_transfer`
7. `optimization_theory_probabilistic`
8. `graph_geometric_learning`
9. `scientific_bio_medical_ml`
10. `safety_alignment_fairness_privacy`
11. `systems_efficiency_scaling`
12. `benchmarks_datasets_evaluation`
13. `robotics_embodied_autonomy`
14. `time_series_dynamical_systems`
15. `other_unclear`

This layer is for batching and coverage control.

### Layer 2: Fine-grained subtopic

This should mostly come from official conference taxonomies when possible.

Recommended leaf set should be a union of:

- official ICLR / NeurIPS / ICML `topic` leaves
- OpenReview `primary_area`
- a small number of manually added CVPR leaves

Examples:

- `vision_models_and_multimodal`
- `image_and_video_generation`
- `3d_rendering_and_reconstruction`
- `classification_and_understanding`
- `language_speech_and_dialog`
- `robotics`
- `chemistry_and_drug_discovery`
- `physics`
- `time_series`
- `generative_models_and_autoencoders`
- `attention_mechanisms`
- `algorithms`
- `graph_neural_networks`
- `representation_learning`
- `transfer_multitask_meta_learning`
- `probabilistic_methods`
- `deep_rl`
- `multi_agent_rl`
- `learning_theory`
- `online_learning_and_bandits`
- `trustworthy_machine_learning`
- `fairness_equity_justice_safety`
- `accountability_transparency_interpretability`
- `privacy`
- `security`
- `alignment`
- `evaluation`
- `datasets_and_benchmarks`

For CVPR-specific manual leaves, add:

- `object_detection`
- `instance_segmentation`
- `semantic_segmentation`
- `video_understanding`
- `tracking`
- `ocr_document_ai`
- `autonomous_driving`
- `medical_image_analysis`
- `remote_sensing`
- `gaussian_splatting`
- `nerf_and_novel_view_synthesis`

### Layer 3: Cross-cutting facets

A paper should also get multiple facets, not just one topic:

- `task_facet`
  - e.g. `reasoning`, `captioning`, `retrieval`, `forecasting`, `segmentation`, `policy_learning`
- `method_facet`
  - e.g. `diffusion`, `autoregressive`, `moe`, `test_time_scaling`, `rlhf`, `preference_optimization`, `world_model`, `neural_operator`
- `object_facet`
  - e.g. `llm`, `vlm`, `video`, `3d`, `graph`, `molecule`, `robot`, `time_series`
- `evaluation_facet`
  - e.g. `benchmark`, `dataset`, `theory`, `systems`, `safety_eval`

This is the layer your current classifier is missing.

## Concrete Classification Policy

For each paper:

1. If official `topic` exists, use it as the main anchor.
2. If official `primary_area` exists, use it to validate or override the root domain.
3. Use `keywords` to assign `task_facet`, `method_facet`, and `object_facet`.
4. Only fall back to PDF-text heuristics when the official fields are absent.
5. Keep both:
   - `official_label`
   - `normalized_internal_label`

That avoids losing provenance.

## What I Recommend You Do Next

Instead of replacing the current heuristic classifier with a single finer flat taxonomy, rebuild it into:

1. `official-first normalization`
   - pull OpenReview `primary_area` and `keywords`
   - pull official virtual `topic` where available
2. `conference-specific leaf mapping`
   - normalize `ICLR / NeurIPS / ICML` official leaves into a shared layer-2 leaf space
   - fill `CVPR` with community or custom leaves
3. `multi-facet enrichment`
   - add task/method/object facets from title + abstract + official keywords
4. `priority logic`
   - batch by Layer 1 root first
   - then stratify within each root using Layer 2 leaves and Layer 3 facets

That will be materially better than the current one-label heuristic.

## Sources

- `berenslab/iclr-dataset`: `https://github.com/berenslab/iclr-dataset`
- `amusi/CVPR2026-Papers-with-Code`: `https://github.com/amusi/CVPR2026-Papers-with-Code`
- `Songwxuan/Embodied-AI-Paper-TopConf`: `https://github.com/Songwxuan/Embodied-AI-Paper-TopConf`
- ICLR 2026 virtual data: `https://iclr.cc/static/virtual/data/iclr-2026-orals-posters.json`
- NeurIPS 2025 virtual data: `https://neurips.cc/static/virtual/data/neurips-2025-orals-posters.json`
- ICML 2026 virtual data: `https://icml.cc/static/virtual/data/icml-2026-orals-posters.json`
- ICLR 2026 OpenReview accepted notes: `https://api2.openreview.net/notes?content.venueid=ICLR.cc/2026/Conference`
- NeurIPS 2025 OpenReview accepted notes: `https://api2.openreview.net/notes?content.venueid=NeurIPS.cc/2025/Conference`

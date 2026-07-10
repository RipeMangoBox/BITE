# Conference Hot Topics Report

- generated_at: `2026-05-12T17:30:00+08:00`
- scope: `ICLR 2026`, `CVPR 2026`, `NeurIPS 2025`, `ICML 2026`
- note: accepted counts prefer official retrospective/fact-sheet text when available; oral/topic breakdowns use official virtual-site public data when available.

## Summary


| Conference   | accepted   | oral       | spotlight  | poster_or_regular | accepted_source_type                           | notes                                                                                                                                                                              |
| ------------ | ---------- | ---------- | ---------- | ----------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ICLR 2026    | 5355       | 223        | 0          | 5201              | official retrospective + official virtual data | Retrospective gives the accepted total; virtual data undercounts visible papers relative to the retrospective by a small margin.                                                   |
| CVPR 2026    | not_public | 141        | not_public | 4070              | official virtual pages only                    | No official accepted-total / oral-total summary located as of `2026-05-12`; oral and paper counts here are page counts from the official virtual site, not chair-published totals. |
| NeurIPS 2025 | 5290       | 87         | 0          | 5678              | official fact sheet + official virtual data    | Fact sheet gives accepted and oral totals; virtual data exposes topic fields.                                                                                                      |
| ICML 2026    | 6352       | not_public | 536        | 5816              | official virtual data                          | No chair-published acceptance-rate summary located as of `2026-05-12`; accepted and spotlight/regular counts come from official virtual data deduping by source id.                |


## Hot Topic Proxies

These are public topic fields from the official virtual data, so they are useful as popularity proxies, not authoritative chair summaries.

### ICLR 2026

- all accepted proxy top topics: `Applications (1037)`, `Computer Vision (911)`, `Unlabeled (892)`, `Deep Learning (840)`, `Social Aspects (434)`, `General Machine Learning (412)`, `Reinforcement Learning (395)`
- oral proxy top topics: `Unlabeled (145)`, `Applications (14)`, `Deep Learning (13)`, `General Machine Learning (12)`, `Computer Vision (12)`, `Social Aspects (8)`, `Theory (8)`
- interpretation: public topic labels are fairly coarse, but the oral pool still concentrates around general foundation-model, application, and vision-heavy work.

### CVPR 2026

- accepted_total: not publicly confirmed from an official chair summary as of `2026-05-12`
- oral_total from official virtual oral page count: `141`
- paper page count from official virtual papers page: `4070`
- hot-topic proxy: not computed robustly because no official public structured topic dump was recovered in this pass

### NeurIPS 2025

- all accepted proxy top topics: `Computer Vision (1080)`, `Applications (1055)`, `Deep Learning (951)`, `Social Aspects (496)`, `Theory (443)`, `Unlabeled (401)`, `General Machine Learning (392)`
- oral proxy top topics: `Unlabeled (65)`, `Computer Vision (6)`, `Applications (5)`, `Deep Learning (5)`, `Theory (2)`, `Reinforcement Learning (2)`
- interpretation: the accepted pool remained broad, but the visible oral pool still skewed to vision, deep learning, and application-heavy papers.

### ICML 2026

- all accepted proxy top topics: `Unlabeled (5070)`, `Deep Learning (488)`, `Applications (339)`, `General Machine Learning (161)`, `Social Aspects (159)`, `Theory (113)`, `Reinforcement Learning (93)`
- spotlight proxy top topics: not separated further here because the public dump exposes `Spotlight` but most topic labels are unlabeled
- interpretation: the public topic taxonomy is sparse, but the non-unlabeled portion still points to deep learning, applications, and general ML as the largest visible buckets.

## Practical Takeaways

- The only clearly repeat-large direction across the available official data is foundation-model-centric work, especially LLM, multimodal, and generative/model-scaling adjacent topics.
- Vision-heavy and application-heavy work remain large in ICLR, NeurIPS, and CVPR-visible pools.
- Coarse public topic tags are too weak for fine-grained local batching, so the local ICLR26 prioritization should rely on the repo-side PDF classification outputs in this directory rather than conference-level public tags alone.

## Sources

- ICLR 2026 retrospective: `https://blog.iclr.cc/2026/03/31/a-retrospective-on-the-iclr-2026-review-process/`
- ICLR 2026 papers: `https://iclr.cc/virtual/2026/papers.html`
- ICLR 2026 virtual data: `https://iclr.cc/static/virtual/data/iclr-2026-orals-posters.json`
- NeurIPS 2025 fact sheet: `https://media.neurips.cc/Conferences/NeurIPS2025/press/NeurIPS2025-Fact_Sheet.pdf`
- NeurIPS 2025 chairs retrospective: `https://blog.neurips.cc/2025/09/30/reflections-on-the-2025-review-process-from-the-program-committee-chairs/`
- NeurIPS 2025 papers: `https://neurips.cc/virtual/2025/papers.html`
- NeurIPS 2025 virtual data: `https://neurips.cc/static/virtual/data/neurips-2025-orals-posters.json`
- ICML 2026 lay summaries post: `https://blog.icml.cc/2026/05/07/icml-2026-lay-summaries/`
- ICML 2026 papers: `https://icml.cc/virtual/2026/papers.html`
- ICML 2026 virtual data: `https://icml.cc/static/virtual/data/icml-2026-orals-posters.json`
- CVPR 2026 conference site: `https://cvpr.thecvf.com/Conferences/2026`
- CVPR 2026 papers: `https://cvpr.thecvf.com/virtual/2026/papers.html`
- CVPR 2026 orals: `https://cvpr.thecvf.com/virtual/2026/events/oral`


# ICLR26 Priority Recommendation

- generated_at: `2026-05-12T17:30:00+08:00`
- basis: `_private/topic_priority/iclr26_topic_summary.csv`
- total_local_iclr26_papers: `5348`

## Recommended Priority Order

Use primary-topic counts as the first-pass batching order:

1. `llm_reasoning_agents` — `1854` papers — cumulative coverage `34.67%`
2. `diffusion_generation` — `732` papers — cumulative coverage `48.35%`
3. `optimization_theory` — `452` papers — cumulative coverage `56.81%`
4. `efficient_llm_systems` — `431` papers — cumulative coverage `64.87%`
5. `reinforcement_learning` — `350` papers — cumulative coverage `71.41%`
6. `robustness_ood` — `347` papers — cumulative coverage `77.90%`
7. `multimodal_vlm` — `289` papers — cumulative coverage `83.30%`
8. `alignment_safety` — `263` papers — cumulative coverage `88.22%`
9. `time_series_sequential` — `243` papers — cumulative coverage `92.76%`
10. `privacy_security` — `122` papers — cumulative coverage `95.04%`

## Suggested Batch Policy

- If you want a very aggressive hot-topic-first pass, process only the top `2` topics first.
  Coverage: about `48.35%` of local ICLR26.
- If you want a broader but still selective pass, process the top `5` topics first.
  Coverage: about `71.41%` of local ICLR26.
- If you want to cover most visibly hot directions before long-tail theory/science/graph work, process the top `8` topics first.
  Coverage: about `88.22%` of local ICLR26.

## Important Caveats

- This is a document-only heuristic taxonomy, not a semantic gold label set.
- Primary-topic counts are useful for triage and prioritization, but some papers in `optimization_theory` and `efficient_llm_systems` are likely cross-listed with LLM/generative work.
- For actual analysis batching, combine `primary_topic` with `secondary_topics` so that high-value multimodal/alignment papers inside another primary bucket are not dropped.

## Next Practical Move

- Use `iclr26_topic_assignments.jsonl` to filter rows whose `primary_topic.topic_id` is in the top `5` or top `8` buckets.
- Then rebuild batch manifests from those filtered rows instead of from the full pending pool.

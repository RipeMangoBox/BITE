---
title: "Analysis Scheme B"
updated: 2026-05-10
tags:
  - researchflow
  - analysis_pipeline
  - iclr2026
---

# Analysis Scheme B

Scheme B is the planned alternative to Scheme A. Scheme A remains the current
production path: `analysis_agent` reads the full paper context, emits one large
JSON object, and `writer_agent` writes the report after DB materialization.

Scheme B keeps full-paper understanding, but removes the large-JSON single
failure point.

## Core Idea

Use a main reader agent to read the full paper and create a compact reading map.
Specialist agents then read focused original paper slices together with that
reading map and emit small JSON fragments. Final assembly is deterministic code,
not another large LLM JSON generation step.

## Topology

```text
MinerU parsed paper
  -> main_reader_agent
       reads full paper context
       outputs compact reading_map / SIR only
  -> specialist agents
       core_delta_agent
       method_formula_agent
       experiment_evidence_agent
       reference_role_agent
  -> deterministic combiner + schema validator
  -> DeltaCard / EvidenceUnit / GraphAssertion materialization
  -> writer_agent
```

## Specialist Agents

- `core_delta_agent`
  - Reads: abstract, introduction, method sections, and `reading_map`.
  - Outputs: `paper_essence` and `method_delta`.

- `method_formula_agent`
  - Reads: method, algorithms, formula contexts, and `reading_map`.
  - Outputs: `deep_analysis.method` and `deep_analysis.formulas`.

- `experiment_evidence_agent`
  - Reads: result tables, experiment section, ablation section, and `reading_map`.
  - Outputs: `deep_analysis.experiment`, `main_results`, `ablations`, and evidence candidates.

- `reference_role_agent`
  - Reads: reference list, citation contexts, and `reading_map`.
  - Outputs: `reference_role_map`.

- `graph_candidate` / `kb_profile`
  - Deferred post-processing.
  - Not a hard gate for core DeltaCard/report generation.

## Non-Negotiable Constraint

Do not ask a final LLM combiner to output the complete large JSON again. That
recreates the Scheme A failure mode. The final combiner should be deterministic
Python code that merges validated fragments and reports missing fields.

## Gates

- `reading_map` gate: must contain method thesis, claimed delta, key sections,
  key tables/figures, baseline hints, and risk notes.
- `core_delta` gate: every changed slot must include slot name, baseline value,
  proposed value, change type, and source anchor.
- `experiment_evidence` gate: each key result or ablation must have a table,
  figure, or section anchor.
- `reference_role` gate: direct baselines and method sources must be separated
  from background citations.
- materialization gate: `paper_essence`, `method_delta`, and `deep_analysis`
  are required; graph candidates and KB profiles are optional/deferred.

## Concurrency

- `main_reader_agent` runs first.
- `core_delta_agent`, `method_formula_agent`, `experiment_evidence_agent`, and
  `reference_role_agent` can run concurrently after the reading map is valid.
- DB writes remain centralized in the deterministic combiner/materializer.
- Per-paper specialist concurrency should be capped to avoid API rate limits.

## DeltaCard Target

Scheme B should make DeltaCard generation more complete and more auditable by
requiring source anchors on method deltas and evidence units before DB
materialization. It should not claim absolute perfection; the engineering target
is no silent dirty writes: missing or conflicting fields become explicit repair
items.

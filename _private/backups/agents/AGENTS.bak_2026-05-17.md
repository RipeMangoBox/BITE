# Agent Guide

Public agent-facing usage starts from [README.md](README.md) and
[.claude/skills/README.md](.claude/skills/README.md). Internal architecture and
deployment notes live under `_private/`.

## Data Boundaries

ResearchFlow supports two operating modes:

- **Local skill workflow**: skills may read and write the local vault layout when
  that skill explicitly owns the output path.
- **Service mode**: data-changing operations should go through the backend API
  or the pipeline scripts that persist through the service layer.

Local vault areas:
- `obsidian-vault/paperPDFs/` stores source PDFs for local analysis.
- `obsidian-vault/analysis/` stores structured local analysis notes.
- `obsidian-vault/collection/` stores generated indexes and Obsidian navigation.
- `obsidian-vault/ideas/` stores local idea, focus, and review notes.

When the service is available, prefer `/api/v1/search/*` for lookup and
retrieval. Local file reads are still valid for local-only skill workflows,
export-only tasks, and debugging generated vault artifacts.

## Architecture: 4 Layers

```
Layer A: Faceted Taxonomy DAG
  taxonomy_nodes (domain/task/dataset/benchmark/modality/...)
  taxonomy_edges (is_a / part_of / uses)
  paper_facets (paper ↔ taxonomy_node with role)

Layer B: Method Evolution DAG
  method_nodes (algorithm/recipe/model_family/mechanism_family)
  method_edges (extends/modifies_slot/replaces/combines_with)
  method_applications (paper uses method with role)

Layer C: Paper Layer
  papers → delta_cards → evidence_units → graph_assertions
  Paper is the container; DeltaCard records the structured "what changed"

Layer D: Cross-paper Abstraction (Phase 2)
  canonical_ideas, bottlenecks, lineage
```

## 2-Agent Pipeline

```
Candidate → import_and_score()
    ↓ (DiscoveryScore ≥ 75 → analysis)

Analysis Phase (1 LLM call):
  1. analysis_agent → analysis_truth + paper_essence + method_delta +
     reference_role_map + deep_analysis + graph_candidates + kb_profiles
    ↓ (deterministic DeepIngestScore / graph scoring)

Writer Phase (1 LLM call):
  2. writer_agent → 7-section structured report from verified truth only

Materialization (backend/pipeline):
  _materialize_to_graph() → DeltaCard + EvidenceUnit + GraphAssertion
  link_to_parent_baselines() → DeltaCardLineage
  synthesize_concepts() → MethodNode + CanonicalIdea
  reconcile_neighbors() → same_family updates
```

## Rules

1. In service mode, write through the backend API or service pipeline scripts; do not edit generated Markdown exports as canonical service data.
2. In local skill workflow, writes to `obsidian-vault/analysis/`, `obsidian-vault/collection/`, `obsidian-vault/paperPDFs/`, and `obsidian-vault/ideas/` are allowed only when the invoked skill owns that output.
3. Prefer `/api/v1/search/*` for lookup and retrieval when the service is available.
4. Analysis language defaults to `zh` unless the request overrides it.
5. Pipeline steps are idempotent; already-completed steps should be skipped.
6. Metadata observations are append-only; canonical resolution chooses the active value.
7. Planned analysis batches must declare goal, source, selection rule, budget, and output target before agents run.
8. Agents must consume only declared context and preserve source anchors in blackboard/DB outputs.
9. Deep analysis runs only after deterministic DeepIngestScore promotion; graph candidates must pass node/edge score gates.
10. Reports and profiles must be generated from verified blackboard items, not new unsupported claims.
11. In Markdown tables, do not use aliased Obsidian wikilinks such as `[[full/path|abbr]]`; use plain text inside table cells and place full wikilinks in surrounding prose or frontmatter.
12. Generated exports, snapshots, backups, local storage, and symlinks stay out of Git.

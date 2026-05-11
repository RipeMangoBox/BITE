# Agent Guide

> Architecture & data model: [ARCHITECTURE.md](researchflow-backend/ARCHITECTURE.md)
> Deployment: [DEPLOY.md](researchflow-backend/DEPLOY.md)
> Analysis plan & execution contract: [analysis_plan.md](docs/analysis_plan.md)

## Source of truth

**PostgreSQL is the only write target.** `paperAnalysis/`, `paperCollection/`, `obsidian-vault/` are read-only exports. For queries, use `/api/v1/search/*`, not local files.

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
  Paper is the container; DeltaCard is the structured "what changed"

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

Materialization (pure DB):
  _materialize_to_graph() → DeltaCard + EvidenceUnit + GraphAssertion
  link_to_parent_baselines() → DeltaCardLineage
  synthesize_concepts() → MethodNode + CanonicalIdea
  reconcile_neighbors() → same_family updates
```

`shallow_extract`, `reference_role_map`, `deep_analysis`, `graph_candidates`,
and `kb_profiles` may still appear as blackboard item types. They are
compatibility projections written by `analysis_agent`, not separate active
semantic agent calls in the main ingest workflow.

## What each Agent needs

| Agent | Input | Output | Token Budget |
|-------|-------|--------|-------------|
| analysis_agent | parse text + MinerU reading order + formulas/tables + references + graph schemas | verified analysis truth and compatibility projections | 80K |
| writer_agent | verified analysis truth + selected evidence + figure metadata | 7-section report | 80K |

## DB Tables (40 tables)

### Core pipeline writes to:
- `papers` — metadata + state
- `paper_analyses` — L2/L3 extraction results
- `delta_cards` — structured "what changed" (truth layer)
- `evidence_units` — atomic evidence with confidence
- `graph_nodes` + `graph_assertions` — knowledge graph
- `method_nodes` — method/mechanism entities
- `agent_runs` + `agent_blackboard_items` — agent tracking
- `paper_facets` — taxonomy links
- `kb_node_profiles` + `kb_edge_profiles` — wiki pages

### Unchanged:
- `metadata_observations` — multi-source metadata ledger
- `paper_candidates` + `candidate_scores` — discovery pipeline
- `delta_card_lineage` — method evolution DAG

## Rules

1. All writes go to backend API, never edit Markdown files as source
2. For queries, prefer `/api/v1/search/*` over reading local files
3. Analysis language default: `zh` (override per request)
4. Pipeline steps are idempotent — already-completed steps are auto-skipped
5. Metadata observations are append-only — canonical resolver picks best value
6. DeltaCard publish gate: evidence_refs ≥ 2
7. Planned analysis batches must declare goal, source, selection rule, budget, and output target before agents run
8. Agents must consume only declared context and preserve source anchors in blackboard/DB outputs
9. Deep analysis runs only after deterministic DeepIngestScore promotion; graph candidates must pass node/edge score gates
10. Paper reports and profiles must be generated from verified blackboard items, not from new unsupported claims
11. Generated exports, snapshots, backups, local storage, and symlinks stay out of Git

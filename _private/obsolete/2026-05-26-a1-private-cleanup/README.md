# 2026-05-26 A1 Private Cleanup

This bundle was created while cleaning `_private/` for ResearchFlow relevance.

Moved here:

- `local_notes/`: personal/local research notes, XHS landscape notes, motion
  research notes, and old local agent guidance. These are not part of the
  current ResearchFlow paper-analysis chain, batch provenance, deployment
  instructions, or maintenance workflow, but may retain historical context.
- `discord/`: generated Discord banner scripts and image candidates. These are
  brand/community artifacts rather than analysis-chain or batch-maintenance
  evidence.

Deleted as temporary or rebuildable:

- `local_notes/T_Math_Reasoning.md`: zero-byte placeholder.
- `_private/local_runtime/`: local virtualenv and pycache repair shell; no
  durable ResearchFlow evidence after cache removal.
- `_private/prompt_archive/`: empty archive shell.
- `_private/researchflow-backend-local/exports/`: empty local export shell.
- Python `__pycache__`, `.pyc`, and `.pytest_cache` directories under
  `_private/`.

Explicitly retained outside this bundle:

- `_private/version_analysis_chain/`: historical and current analysis-chain
  version descriptions.
- `_private/analysis_chain_eval/`: validation runs for analysis-chain variants.
- `_private/iclr26_batch/`, `_private/local_analysis_runs/`,
  `_private/resmax_downloads/`, and `_private/topic_priority/`: batch
  manifests, run outputs, source PDFs, and topic/provenance data.
- `_private/.archives/`: historical handoffs and retired route bundles.
- `_private/deploy_archive/`, `_private/researchflow-backend-docs/`, and
  `_private/researchflow-backend-env/`: deployment and backend reference
  material, including sensitive env files.


# Agent 1 Branch Merge / Privacy Audit

Branch audited: `experiment/analysis-chain-batch-eval`

Scope: classify current branch changes for merge to public `main`; quarantine clearly private/local or StoryMotion-related files from public paths. Did not touch `/home/ripemangobox/Coding/Github/OpenSource/On_Process/BITE_Main`.

## Moved files

Moved into `linkedCodebases/audit_quarantine/`, preserving original path shape where practical:

- `0614.xmind` -> `linkedCodebases/audit_quarantine/0614.xmind`
- `_hf_stage/` -> `linkedCodebases/audit_quarantine/_hf_stage/`
- `drafts/` -> `linkedCodebases/audit_quarantine/drafts/`
- `orders.md` -> `linkedCodebases/audit_quarantine/orders.md`
- `reports/` -> `linkedCodebases/audit_quarantine/reports/`
- `scripts/__pycache__/` -> `linkedCodebases/audit_quarantine/scripts/__pycache__/`
- `scripts/paper_analysis_maintenance/__pycache__/` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/__pycache__/`
- `scripts/researchflow_local/__pycache__/` -> `linkedCodebases/audit_quarantine/scripts/researchflow_local/__pycache__/`
- `scripts/add_and_download_14_papers.py` -> `linkedCodebases/audit_quarantine/scripts/add_and_download_14_papers.py`
- `scripts/collect_cvpr2026_full_classification.py` -> `linkedCodebases/audit_quarantine/scripts/collect_cvpr2026_full_classification.py`
- `scripts/build_stage2_joint_tokenizer_latent_cache.py` -> `linkedCodebases/audit_quarantine/scripts/build_stage2_joint_tokenizer_latent_cache.py`
- `scripts/paper_analysis_maintenance/audit_mineru_coverage_for_notes.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/audit_mineru_coverage_for_notes.py`
- `scripts/paper_analysis_maintenance/complete_paper_list_links.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/complete_paper_list_links.py`
- `scripts/paper_analysis_maintenance/plan_figure_caption_rebuild_batches.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/plan_figure_caption_rebuild_batches.py`
- `scripts/paper_analysis_maintenance/run_mineru_only_queue.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/run_mineru_only_queue.py`
- `scripts/pulpmotion_official_baseline_eval.py` -> `linkedCodebases/audit_quarantine/scripts/pulpmotion_official_baseline_eval.py`
- `scripts/run_storymotion_official_full_eval_5090.sh` -> `linkedCodebases/audit_quarantine/scripts/run_storymotion_official_full_eval_5090.sh`
- `scripts/run_storymotion_p0_diag_5090.sh` -> `linkedCodebases/audit_quarantine/scripts/run_storymotion_p0_diag_5090.sh`
- `scripts/start_stage2_tensorboard.sh` -> `linkedCodebases/audit_quarantine/scripts/start_stage2_tensorboard.sh`
- `scripts/start_storymotion_all_tensorboard.sh` -> `linkedCodebases/audit_quarantine/scripts/start_storymotion_all_tensorboard.sh`
- `scripts/storymotion_experiment_status.py` -> `linkedCodebases/audit_quarantine/scripts/storymotion_experiment_status.py`
- `scripts/storymotion_official_bridge_smoke.py` -> `linkedCodebases/audit_quarantine/scripts/storymotion_official_bridge_smoke.py`
- `scripts/storymotion_official_full_eval.py` -> `linkedCodebases/audit_quarantine/scripts/storymotion_official_full_eval.py`
- `scripts/storymotion_stage2_gated_eval.py` -> `linkedCodebases/audit_quarantine/scripts/storymotion_stage2_gated_eval.py`
- `scripts/storymotion_test_data_consistency_check.py` -> `linkedCodebases/audit_quarantine/scripts/storymotion_test_data_consistency_check.py`

Note: some moved StoryMotion/PulpMotion files were tracked branch additions, so the current worktree now shows deletions at their original `scripts/` paths. That is intentional audit quarantine, not a revert.

## Recommended for merge

Public ResearchFlow/BITE improvements that appear appropriate for `main` after normal review:

- `.claude/skills/notes-export-share-version/reference.md`
- `.claude/skills/papers-audit-metadata-consistency/SKILL.md`
- `.claude/skills/papers-audit-metadata-consistency/scripts/audit_metadata_consistency.py`
- `.claude/skills/papers-build-index/scripts/build_paper_index.py`
- `.claude/skills/papers-query-knowledge-base/SKILL.md`
- `.claude/skills/papers-query-knowledge-base/references/structure.md`
- `.claude/skills/research-brainstorm-from-kb/SKILL.md`
- `.claude/skills/research-workflow/SKILL.md`
- `.claude/skills/research-workflow/scripts/research_workflow/research_workflow_entry.py`
- `.claude/skills/rf-obsidian-markdown/SKILL.md`
- `.gitignore` changes that ignore `linkedCodebases/`, `obsidian-vault/ideas/`, `artifacts/`, and generated batch/export state.
- `docs/formal-analysis-chain.md` public description of DeepSeek figure/table placement and caption validation, subject to main-agent doc editing.
- `scripts/README.md` updates for renamed/changed analysis-chain scripts, subject to main-agent doc editing.
- `scripts/audit_knowledge_batch.py`
- `scripts/fix_analysis_md_issues.py`
- `scripts/paper_analysis_maintenance/audit_analysis_chain.py`
- `scripts/paper_analysis_maintenance/check_analysis_sections.py` rename from `check_part_sections.py`
- `scripts/paper_analysis_maintenance/salad_format_audit.py`
- `scripts/rebuild_figures_export.py`
- `scripts/researchflow_local/paper_list_queue.py`
- `scripts/researchflow_local/venue_slug.py`
- `scripts/review_analysis_mismatch.py`
- `scripts/run_local_paper_analysis.py`, limited to formal analysis-chain / figure-caption fixes. It has both committed branch changes and current local edits; review the final diff before merging.
- `scripts/smoke_index_workflow.py`

Remaining untracked public-looking utilities that may be worth adding after review:

- `scripts/download_paper_list_wait.py`
- `scripts/paper_analysis_maintenance/fill_project_links_from_pdf_first_page.py`
- `scripts/paper_analysis_maintenance/fix_analysis_note_tags.py`
- `scripts/sync_paper_list_state.py`

## Recommended to exclude

Do not merge these into public `main`:

- All files moved under `linkedCodebases/audit_quarantine/`.
- Original public-path StoryMotion/PulpMotion/5090 files now showing as deleted locally:
  - `scripts/pulpmotion_official_baseline_eval.py`
  - `scripts/run_storymotion_official_full_eval_5090.sh`
  - `scripts/run_storymotion_p0_diag_5090.sh`
  - `scripts/start_stage2_tensorboard.sh`
  - `scripts/storymotion_official_bridge_smoke.py`
  - `scripts/storymotion_official_full_eval.py`
  - `scripts/storymotion_stage2_gated_eval.py`
  - `scripts/storymotion_test_data_consistency_check.py`
- `WECHAT.md`: current local edit contains a machine/network-specific `rsync` rescue command with host, port, account, and absolute destination path. I did not edit or move it because docs are reserved for the main agent.
- `README_CN.md` deletion: local uncommitted deletion, likely unrelated to this audit unless the main agent intentionally removes it.
- `obsidian-vault/paper_list.csv` bulk data churn until the merge owner confirms the public dataset/state policy.
- `linkedCodebases/README.md` deletion from the branch should not be blindly merged unless `main` accepts full ignore of `linkedCodebases/`.
- `obsidian-vault/ideas/README.md` deletion from the branch should not be blindly merged unless `main` accepts making all ideas private.

## Uncertain / needs user decision

- `AGENTS.md` changes are branch-specific per the file itself. Do not blindly merge; port only public-safe rule changes into the public `main` agent guide if desired.
- `.gitignore` change from "keep linkedCodebases README" to ignoring all `linkedCodebases/` is privacy-positive, but conflicts with the existing tracked `linkedCodebases/README.md` public placeholder. Decide whether public `main` should keep a placeholder or fully ignore the directory.
- `obsidian-vault/ideas/README.md` removal and ignoring all `obsidian-vault/ideas/` is privacy-positive, but removes the public explanation placeholder. Decide public policy.
- `obsidian-vault/paper_list.csv` has large committed and local modifications, including many new rows and state/path changes. Treat as a data release decision, not a code merge.
- `scripts/run_paper_list_analysis.py` has local uncommitted changes but is not in the branch diff against `main`; review separately before merging.
- `scripts/sync_assets_from_hf.py` has a local uncommitted public-looking change adding `paper-list` sync support. It is not in the committed branch diff against `main`; review separately before merging.
- During final verification, additional concurrent README/doc edits were present in `.claude/skills/README.md`, `README.md`, `README_EN.md`, `docs/formal-analysis-chain.md`, and `scripts/README.md`. I did not author or edit those docs; main agent should own their final classification and wording.
- Public docs (`docs/formal-analysis-chain.md`, `scripts/README.md`, README-family docs) were only classified here. Main agent should own final wording and any doc edits.

## Current worktree notes

Observed with `git status --short --branch` after quarantine:

- Branch is ahead of origin by 1 commit.
- Local uncommitted edits remain in `.claude/skills/README.md`, `.claude/skills/papers-build-index/scripts/build_paper_index.py`, `AGENTS.md`, `README.md`, `README_EN.md`, `WECHAT.md`, `docs/formal-analysis-chain.md`, `obsidian-vault/paper_list.csv`, `scripts/README.md`, `scripts/run_local_paper_analysis.py`, `scripts/run_paper_list_analysis.py`, and `scripts/sync_assets_from_hf.py`.
- Local deletions remain for quarantined tracked StoryMotion/PulpMotion files under `scripts/`.
- Remaining untracked public-path scripts are listed above under "may be worth adding after review".

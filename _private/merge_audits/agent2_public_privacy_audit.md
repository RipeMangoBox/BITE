# Agent 2 Public Privacy Audit

Date: 2026-06-22

Scope:
- Process branch: `/home/ripemangobox/Coding/Github/OpenSource/On_Process/BITE_Process`
- Main worktree: `/home/ripemangobox/Coding/Github/OpenSource/On_Process/BITE_Main`

Commands used:
- `git status --short`
- `git ls-files`
- `git ls-files --others --exclude-standard`
- `git ls-files --others --ignored --exclude-standard`
- focused `rg` scans for API key names, private-key blocks, hardcoded local paths, StoryMotion/PulpMotion references, `_private`, `.obsidian`, `_hf_stage`, `5090`, and `tensorboard`

## Summary

- No literal API tokens, private-key blocks, AWS access-key IDs, or `sk-...` / `hf_...` token strings were found in the scanned tracked plus non-ignored untracked public surfaces.
- `BITE_Process` still contains several candidate-public privacy/publication issues that need follow-up, mostly because this branch is actively being cleaned by multiple agents.
- `BITE_Main` is clean in git status, but tracked public content includes candidate privacy/publication decisions: a personal-looking image, local provider defaults, and StoryMotion provenance tags in the public paper list.
- I did not edit README/docs. Per instruction, doc findings are reported only.

## Process Branch Findings

### High Confidence Public-Path Leaks

1. `WECHAT.md:14` contains a hardcoded rescue command with user/host/path details:
   - remote user/host-like target: `ripemangobox@172.23.148.106`
   - port: `59374`
   - path: `/data/public/ripemangobox/rescue/5090-data-rescue-20260617-user/data-root/`
   - I did not edit this doc because README/docs cleanup is assigned to the main agent.

2. Tracked StoryMotion/PulpMotion experiment scripts are currently deleted from `scripts/`:
   - `scripts/pulpmotion_official_baseline_eval.py`
   - `scripts/run_storymotion_official_full_eval_5090.sh`
   - `scripts/run_storymotion_p0_diag_5090.sh`
   - `scripts/start_stage2_tensorboard.sh`
   - `scripts/storymotion_official_bridge_smoke.py`
   - `scripts/storymotion_official_full_eval.py`
   - `scripts/storymotion_stage2_gated_eval.py`
   - `scripts/storymotion_test_data_consistency_check.py`

   These deletions appeared while the audit was running. I did not restore or revert them. Matching files are now visible under ignored `linkedCodebases/audit_quarantine/scripts/` and/or `linkedCodebases/StoryMotion/`, which is consistent with the requested public-path quarantine direction.

3. `obsidian-vault/paper_list.csv` contains hardcoded old local paths in row metadata:
   - line 1793 includes `wrong_pdf_was=/data/Life Me/ResearchWY Vault/...`
   - line 1906 includes `wrong_pdf_was=/data/Life Me/ResearchWY Vault/...`

4. `scripts/run_local_paper_analysis.py` has local/provider defaults that may be too opinionated for public release:
   - defaults to `DEEPSEEK_API_KEY` for main/writer/figure providers when present or unspecified
   - uses `KIMI_API_KEY`, `MOONSHOT_API_KEY`, and `KIMI_AUTH_TOKEN` discovery paths
   - no secret values were found, but public release should decide whether provider defaults are acceptable.

### Candidate-Public / Uncertain Items

1. Remaining untracked scripts under public `scripts/`:
   - `scripts/download_paper_list_wait.py`
   - `scripts/paper_analysis_maintenance/fill_project_links_from_pdf_first_page.py`
   - `scripts/paper_analysis_maintenance/fix_analysis_note_tags.py`
   - `scripts/sync_paper_list_state.py`

   I left these in place because they appear generic enough for maintenance use and did not contain hardcoded personal paths or secrets in the inspected portions. They still need owner decision before public merge because they are untracked.

2. Public paper-list provenance still contains many `StoryMotion_...` and `Pulp Motion` source tags. These are not secrets, but may be unrelated/private experiment provenance and should be normalized or intentionally kept.

3. Tracked skill/docs references to `_private/local_analysis_runs` and `.obsidian` appear to be instructions about local workflow rather than leaks. They are public-policy choices, not token/path secrets.

4. `environment/.env.example` contains `OPENAI_API_KEY=` as an empty placeholder only. This is not a leak.

### Ignored/Local Material Observed

Ignored local/private material exists in the Process worktree, including:
- `_private/` archives, notes, keys, backups, local runs
- `.obsidian/` runtime state and plugins
- `.codex/`
- `platform/`
- `paperSources/`
- `artifacts/`
- `batches/`
- `storage/`
- `linkedCodebases/`

These are ignored by git in the Process branch. I did not inspect every ignored file exhaustively because the public leak risk is primarily tracked plus non-ignored untracked content, but their presence confirms why `.gitignore` coverage matters.

## Process Moved Files

I moved these remaining local-repair planning scripts from public `scripts/paper_analysis_maintenance/` into ignored quarantine:

- `scripts/paper_analysis_maintenance/audit_mineru_coverage_for_notes.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/audit_mineru_coverage_for_notes.py`
- `scripts/paper_analysis_maintenance/complete_paper_list_links.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/complete_paper_list_links.py`
- `scripts/paper_analysis_maintenance/plan_figure_caption_rebuild_batches.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/plan_figure_caption_rebuild_batches.py`
- `scripts/paper_analysis_maintenance/run_mineru_only_queue.py` -> `linkedCodebases/audit_quarantine/scripts/paper_analysis_maintenance/run_mineru_only_queue.py`

Reason: these scripts directly depend on `_private/local_analysis_runs`, `_private/mineru_only_runs`, or generated artifact batch paths and are local repair workflow material.

Concurrent cleanup observed before/during my moves placed additional files under `linkedCodebases/audit_quarantine/`, including:
- `0614.xmind`
- `_hf_stage/cvpr26_nonmotion/**`
- `drafts/ai-video-ecommerce-guide.md`
- `orders.md`
- `reports/maintenance/cvpr26_hf_candidate_*`
- `scripts/add_and_download_14_papers.py`
- `scripts/build_stage2_joint_tokenizer_latent_cache.py`
- `scripts/collect_cvpr2026_full_classification.py`
- StoryMotion/PulpMotion scripts and related `__pycache__` files

I did not claim these as my own moves because they were already gone or changed while I was inspecting.

## Main Worktree Findings

### High Confidence Public-Path Leaks

No literal API tokens, private-key blocks, AWS access-key IDs, or `sk-...` / `hf_...` token strings were found in tracked public content.

### Candidate-Public / Uncertain Items

1. `image/me.jpg` is tracked in `BITE_Main`.
   - File type: JPEG, 1108x1512, 139K.
   - This looks personal by filename and should be explicitly approved for public release or removed/replaced by the main agent/user.

2. `scripts/run_local_paper_analysis.py` has local/provider defaults similar to Process:
   - defaults to `DEEPSEEK_API_KEY`
   - recognizes `KIMI_API_KEY`, `MOONSHOT_API_KEY`, `KIMI_AUTH_TOKEN`, and OpenAI key env vars
   - no secret values were found, but public default-provider policy needs a decision.

3. `obsidian-vault/paper_list.csv` contains StoryMotion provenance rows, for example `StoryMotion_20260601`, `StoryMotion_20260602`, and related source tags. These are not secrets, but may expose private experiment organization.

4. `obsidian-vault/analysis/ICLR_2026/3DGEER_3D_Gaussian_Rendering_Made_Exact_and_Efficient_for_Generic_Cameras.md` mentions RTX 4090/5090 in quoted benchmark context. This appears to come from paper content, not local infrastructure, and is low risk.

5. `environment/.env.example` contains `OPENAI_API_KEY=` as an empty placeholder only. This is not a leak.

## User/Main-Agent Decisions Needed

1. Remove or sanitize `WECHAT.md:14` in Process before public merge.
2. Decide whether `wrong_pdf_was=/data/Life Me/ResearchWY Vault/...` metadata in `obsidian-vault/paper_list.csv` should be scrubbed.
3. Decide whether provider defaults in `scripts/run_local_paper_analysis.py` should become provider-neutral for public release.
4. Decide whether StoryMotion/PulpMotion provenance tags in public `paper_list.csv` should be normalized.
5. Decide whether `BITE_Main/image/me.jpg` is intentionally public.
6. Decide whether the remaining untracked Process maintenance scripts are public utilities or should also be quarantined.


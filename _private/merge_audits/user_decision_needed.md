# User Decisions Needed Before Public Merge

Date: 2026-06-22

This note collects items that are not clear-cut privacy leaks but still need a
repository-owner decision before merging the process branch into public `main`.

## Decisions

1. `image/me.jpg` in `BITE_Main`
   - Status: tracked in public `main`.
   - Question: keep it as the intentional WeChat contact image, or replace it
     with a non-personal/community QR asset?

2. `obsidian-vault/paper_list.csv`
   - Status: process branch has large paper-list churn, including ICLR/CVPR
     public evidence rows and local analysis state changes.
   - Already cleaned: two `wrong_pdf_was=/data/Life Me/...` local paths were
     replaced with `wrong_pdf_was=<private-local-path>`.
   - Question: should the public repo keep only a lightweight seed
     `paper_list.csv`, or should it include the full current public PaperBite
     list? The HF dataset already carries the canonical 1706-row public list.

3. StoryMotion/PulpMotion provenance tags in `paper_list.csv`
   - Status: not secrets, but they may reveal private experiment organization.
   - Question: normalize source tags before merging the public paper list, or
     keep them as historical provenance?

4. Provider defaults in `scripts/run_local_paper_analysis.py`
   - Status: no secret values found, but public defaults prefer DeepSeek when
     provider settings are omitted and include Kimi/OpenAI-compatible env names.
   - Question: keep opinionated defaults for smoother local use, or make the
     public runner provider-neutral and require explicit provider/env selection?

5. `linkedCodebases/README.md` and `obsidian-vault/ideas/README.md`
   - Status: current branch deletes these placeholders and ignores the whole
     corresponding directories for privacy.
   - Question: keep placeholder READMEs in public `main`, or fully ignore these
     local/private folders?

6. Remaining untracked generic maintenance scripts
   - Current candidates:
     - `scripts/download_paper_list_wait.py`
     - `scripts/paper_analysis_maintenance/fill_project_links_from_pdf_first_page.py`
     - `scripts/paper_analysis_maintenance/fix_analysis_note_tags.py`
     - `scripts/sync_paper_list_state.py`
   - Question: add them as public maintenance utilities after review, or keep
     them local/private?

## Completed Cleanups

- Hugging Face token was written to local HF cache per request.
- HF remote `PaperBite-Assets` was synced and verified.
- `WECHAT.md` rescue command containing host, port, account, and absolute path
  was removed.
- StoryMotion/PulpMotion/5090 scripts and other private/local artifacts were
  quarantined under ignored `linkedCodebases/audit_quarantine/`.
- Four local MinerU/maintenance planning scripts were also quarantined under
  ignored `linkedCodebases/audit_quarantine/`.


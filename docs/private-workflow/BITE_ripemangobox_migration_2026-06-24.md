# BITE_ripemangobox migration note

Date: 2026-06-24

This worktree was converted from a branch of `RipeMangoBox/BITE` into a standalone personal repository:

- New root git remote: `https://github.com/RipeMangoBox/BITE_ripemangobox.git`
- New root branch: `main`
- The root repository now owns personal/local working surfaces that were previously excluded or nested:
  - `scripts/` analysis-chain code
  - `obsidian-vault/analysis/`
  - `obsidian-vault/ideas/`
  - `obsidian-vault/social/`
  - `linkedCodebases/`

Nested repositories removed from the working tree:

- `linkedCodebases/.git`
- `obsidian-vault/ideas/.git`

Old git metadata was archived before removal under `_private/BITE_versions/v05/git_unification_20260624/`:

- `root_git_before_reinit.tar.zst`
- `linkedCodebases_git_before_unify.tar.zst`
- `ideas_git_before_unify.tar.zst`
- `subrepo_git_state_before_unify.txt`
- `gitignore.before`
- `git_info_exclude.before`

Large/generated/local runtime surfaces remain ignored by default, including `_private/`, `obsidian-vault/paperPDFs/`, `obsidian-vault/assets/`, `obsidian-vault/batches/`, and Obsidian runtime state.

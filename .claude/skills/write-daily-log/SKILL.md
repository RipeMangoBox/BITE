---
name: write-daily-log
description: Generates or updates a structured daily research log by collecting evidence from git diffs, artifacts, and conversation context, then compressing into a decision-oriented summary. Use when the user says "写日志", "write daily log", "日报", "update daily summary", or asks to summarize today's research progress.
---

# write-daily-log — Evidence-Driven Daily Research Log

Write a daily research log that captures facts which change future decisions, not a chronological activity dump.

## Core Principle

> Find evidence that changes future judgment → compress into log structure.

Only write content that satisfies at least one:
- Changes route/decision
- Changes experiment calibration or comparability
- Affects reproducibility
- Produces a concrete next action
- Is the day's most important quantitative result

## Trigger

- User says "写日志", "日报", "write daily log", "update daily summary"
- User specifies a target file (e.g. `DailySummary/2026-04-15.md`)
- End of a long research session when user asks to wrap up

## Procedure

### Phase 1: Determine Target File

1. If user specifies a file path → use it
2. Else → `DailySummary/<today's date>.md`
3. Read the target file if it exists; inherit its structure, tone, field names, and granularity
4. If file doesn't exist → use [TEMPLATE.md](TEMPLATE.md) as skeleton

### Phase 2: Collect Evidence

Evidence comes from two channels: **conversation context** and **local persistent changes**.

#### A. Conversation Context (current session)

Scan in priority order:
1. User's explicit goals and requests this session
2. Upper-level docs read this session (roadmap, experiment spec, prior summaries)
3. New artifacts produced (eval yamls, metrics, new code, new docs)
4. Key numbers verified or computed
5. Engineering issues exposed or fixed
6. Unresolved items and risks

#### B. Local Persistent Changes (cross-session)

Since the agent cannot access other sessions' history, use git and filesystem signals:

```bash
# 1. Find all git repos under the workspace
find <workspace_root> -maxdepth 3 -name ".git" -type d 2>/dev/null

# 2. For each repo, collect today's changes
git -C <repo> log --oneline --since="<today> 00:00" --until="<tomorrow> 00:00" --all
git -C <repo> diff --stat HEAD~5          # recent diff summary
git -C <repo> diff --name-only HEAD~5     # changed file list

# 3. Check uncommitted work
git -C <repo> status --short

# 4. Find today's new/modified artifacts
find <workspace_root> -name "*.yaml" -o -name "*.md" -o -name "*.csv" -o -name "*.log" | \
  xargs ls -lt 2>/dev/null | head -30
```

Adapt `HEAD~5` and `--since/--until` to the actual date range. The goal is to surface:
- What code was changed and why
- What experiments were run (new checkpoint dirs, eval outputs)
- What documents were created or updated

### Phase 3: Filter

For each collected item, apply the gate:

| Keep? | Criterion |
|-------|-----------|
| YES | Changes a route decision |
| YES | Changes experiment calibration or comparability |
| YES | Affects reproducibility |
| YES | Produces a concrete next action |
| YES | Is the day's key quantitative result |
| YES | Exposes a new risk or uncertainty |
| NO | Routine search / browsing with no outcome |
| NO | Commands that produced no lasting result |
| NO | Trial-and-error that left no artifact |
| NO | Chat-only context with no decision value |

### Phase 4: Map to Log Structure

Map filtered evidence into these sections (match the existing file's field names if updating):

```yaml
# frontmatter
created: <date>
updated: <date>
tags: [daily-summary, ...]
source:
  - <only files that serve as key evidence, not everything opened>
```

```markdown
# <date> 日报

## 今日进展
# Group by topic, not by chronological order.
# Each item: what was done + outcome.

## 核心结论
# Short, hard, actionable judgments that guide next steps.
# Each conclusion must trace to evidence in 今日进展.

## 问题与思考
# Boundaries of conclusions, risks, uncertainties.
# Especially: environment differences, incomparable baselines, coverage gaps.

## 明日任务
# Each task must logically follow from 核心结论 or 问题与思考.
# No generic TODOs — every item needs a "because..." reason.
```

### Phase 5: Consistency Check

Before finalizing, verify:

- [ ] Every number cites a specific file or artifact
- [ ] Old-env and new-env results are never mixed in the same comparison
- [ ] `source` covers all major evidence files (not all opened files)
- [ ] 明日任务 items are deducible from 核心结论 + 问题与思考
- [ ] No section is a copy-paste of conversation text — all content is compressed
- [ ] Language matches user preference (default: zh)

## Prohibited Content

- Activity logs ("I ran command X, then Y, then Z")
- Unfiltered command output
- Explanations of how the log was written
- Speculative conclusions without evidence
- Numbers from mixed evaluation environments without explicit annotation

## Notes

- If the existing file already has content, merge new findings — do not overwrite unless user asks
- Prefer appending to existing sections over restructuring
- When uncertain whether an item passes the filter, err on the side of including it with a `[待确认]` tag
- Match the user's language (Chinese by default for this project)

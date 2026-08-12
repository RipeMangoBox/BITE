# Table source contract

Formal table cells must come from complete audited rows in the canonical StoryMotion metric
ledger. Every mixed-version table requires a non-empty `version / run` value in every row.
Never combine best fields from different checkpoints, decoders, caches, samplers, or artifacts.

Table schemas and row-selection rules are defined in
`obsidian-vault/ideas/StoryMotion/StoryMotion-iclr-ready.md`.

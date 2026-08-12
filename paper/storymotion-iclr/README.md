# StoryMotion ICLR paper scaffold

This directory is a neutral, compilable paper source scaffold. The repository does not
currently contain the official ICLR style files, so `main.tex` intentionally uses the standard
`article` class. Replace only the document class and conference metadata after the official
template is added.

The canonical paper-facing claim, table, figure, limitation, and reviewer-answer owner is
`obsidian-vault/ideas/StoryMotion/StoryMotion-iclr-ready.md`. Formal metrics, confidence
intervals, run identities, and artifact hashes remain owned by
`obsidian-vault/ideas/StoryMotion/StoryMotion-valid-metric-ledger.md`.

Do not type formal numbers independently into this scaffold. Select a complete audited row from
the metric ledger, record its non-empty `version / run` identity in the table source, and retain
the corresponding artifact reference.

Build the neutral draft with:

```bash
cd paper/storymotion-iclr
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated PDF and LaTeX auxiliary files are ignored by Git.

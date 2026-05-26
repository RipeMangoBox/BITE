# Repository Layout

```text
ResearchFlow/
├── .claude/skills/                 maintained agent skill library
├── assets/                         public logo and README assets
├── docs/                           focused architecture and workflow docs
├── environment/                    conda, dotenv, and local environment files
├── linkedCodebases/                optional links to related local codebases
├── obsidian-vault/
│   ├── paperPDFs/                  source PDFs
│   ├── analysis/                   structured per-paper analysis notes
│   ├── index/                      generated JSONL index and navigation pages
│   └── ideas/                      ideas, plans, reviews, and logs
├── scripts/                        setup, maintenance, and audit utilities
├── AGENTS.md                       agent-facing local workflow rules
├── README.md                       English entry point
└── README_CN.md                    Chinese entry point
```

Generated corpora, private notes, local credentials, caches, and large
research artifacts should stay out of Git.

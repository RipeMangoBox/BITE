PYTHON ?= conda run -n researchflow python

.PHONY: check-index smoke-analysis

check-index:
	$(PYTHON) .claude/skills/papers-build-index/scripts/build_paper_index.py

smoke-analysis:
	$(PYTHON) -m py_compile scripts/run_local_paper_analysis.py

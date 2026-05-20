PYTHON ?= conda run -n researchflow python

.PHONY: check-index smoke-analysis smoke-index-workflow

check-index:
	$(PYTHON) .claude/skills/papers-build-index/scripts/build_paper_index.py

smoke-analysis:
	$(PYTHON) -m py_compile scripts/run_local_paper_analysis.py

smoke-index-workflow:
	$(PYTHON) scripts/smoke_index_workflow.py

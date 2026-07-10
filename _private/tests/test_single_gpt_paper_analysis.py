import importlib.util
import json
from argparse import Namespace
from pathlib import Path
import sys


TOOL_ROOT = Path(__file__).resolve().parents[1] / "iclr26_batch" / "tools"

SCRIPT_PATH = TOOL_ROOT / "run_single_gpt_paper_analysis.py"
LOCAL_SCRIPT_PATH = TOOL_ROOT / "run_local_paper_analysis.py"

LOCAL_SPEC = importlib.util.spec_from_file_location("run_local_paper_analysis", LOCAL_SCRIPT_PATH)
local_analysis = importlib.util.module_from_spec(LOCAL_SPEC)
assert LOCAL_SPEC and LOCAL_SPEC.loader
sys.modules[LOCAL_SPEC.name] = local_analysis
LOCAL_SPEC.loader.exec_module(local_analysis)

SPEC = importlib.util.spec_from_file_location("run_single_gpt_paper_analysis", SCRIPT_PATH)
single_gpt = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = single_gpt
SPEC.loader.exec_module(single_gpt)


def test_build_single_gpt_prompt_contains_full_markdown_and_candidates():
    prompt = single_gpt.build_single_gpt_prompt(
        title="T",
        conf_year="ICLR_2026",
        openreview_forum_id="abc",
        markdown="# T\n\nBody",
        figures_tables=[
            {
                "item_id": "item_001",
                "label": "Table 1",
                "type": "table",
                "caption": "Table 1: Result | with pipe",
                "page": 0,
            }
        ],
        max_note_images=3,
    )

    obj = json.loads(prompt)
    assert obj["paper_markdown"] == "# T\n\nBody"
    assert obj["figure_image_budget"] == 3
    assert obj["figure_table_candidates"][0]["item_id"] == "item_001"
    assert "Result | with pipe" in obj["figure_table_candidates"][0]["caption"]


def test_normalize_single_output_uses_fallback_placements():
    parsed = single_gpt.mock_single_gpt_result("T")
    parsed["figure_placements"] = []
    figures = local_analysis.figure_items_with_ids([
        {"label": "Table 1", "type": "table", "caption": "Table 1: Summary", "source_path": ""}
    ])

    analysis, report, placements = single_gpt.normalize_single_output("T", parsed, figures, 1)

    assert analysis["paper_metadata"]["title"] == "T"
    assert "## 概述" in report
    assert placements == [{"item_id": "item_001", "section": "实验与分析", "reason": "caption indicates a table or result plot"}]


def test_single_gpt_parser_defaults_to_official_openai_endpoint():
    parser = single_gpt.build_parser()
    args = parser.parse_args(["--source-md", "paper.md"])

    assert args.model == ""
    assert args.base_url is None
    assert args.stream is True


def test_response_text_reads_output_text_property():
    class Response:
        output_text = "ok"

    assert single_gpt.response_text(Response()) == "ok"


def test_parse_single_output_prefers_outer_object():
    raw = json.dumps(single_gpt.mock_single_gpt_result("T"), ensure_ascii=False)

    parsed = single_gpt.parse_single_output(raw)

    assert "analysis" in parsed
    assert "report_md" in parsed

from types import SimpleNamespace

from scripts import run_paper_list_analysis as runner


def _args(**overrides):
    values = {
        "conf_year": "",
        "acceptance": "",
        "export_vault": True,
        "max_note_images": 6,
        "mock_llm": False,
        "mineru_output_root": "",
        "mineru_batch_id": "",
        "require_existing_mineru_output": False,
        "analysis_output_root": "",
        "pdf_search_root": [],
        "vault_root": "",
        "experiment_label": "",
        "extra_arg": [],
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_command_for_row_uses_row_mineru_output_path_with_paper_pdf():
    row = {
        "_csv_line": "12",
        "state": "Downloaded",
        "paper_title": "Paper One",
        "venue": "SIGGRAPH 2022",
        "pdf_path": "obsidian-vault/paperPDFs/SIGGRAPH_2022/Paper_One.pdf",
        "mineru_output_path": "_private/local_analysis_runs/paper_one/parse/mineru_raw/Paper_One",
    }

    cmd = runner.command_for_row(_args(), row)

    assert "--mineru-output" in cmd
    assert "--paper-pdf" in cmd
    assert "--pdf" not in cmd
    assert cmd[cmd.index("--paper-pdf") + 1].endswith("obsidian-vault/paperPDFs/SIGGRAPH_2022/Paper_One.pdf")
    assert cmd[cmd.index("--mineru-output") + 1].endswith("_private/local_analysis_runs/paper_one/parse/mineru_raw/Paper_One")

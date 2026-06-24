from scripts.researchflow_local.paper_list_queue import venue_to_conf_year
from scripts.researchflow_local.venue_slug import normalize_conf_year_slug


def test_arxiv_conf_year_slug_is_lowercase():
    assert venue_to_conf_year("arXiv 2025") == "arxiv_2025"
    assert venue_to_conf_year("Arxiv 2026") == "arxiv_2026"
    assert normalize_conf_year_slug("arXiv_2024") == "arxiv_2024"


def test_non_arxiv_conf_year_slug_uppercases_venue():
    assert venue_to_conf_year("ICLR 2026") == "ICLR_2026"
    assert venue_to_conf_year("iclr 2026") == "ICLR_2026"
    assert normalize_conf_year_slug("SIGGRAPH_Asia_2025") == "SIGGRAPH_ASIA_2025"


def test_workshop_conf_year_slug_uses_main_venue_w_suffix():
    assert venue_to_conf_year("CVPR_Workshop 2024") == "CVPRW_2024"
    assert venue_to_conf_year("ICCV Workshop 2025") == "ICCVW_2025"
    assert normalize_conf_year_slug("CVPR_Workshops_2024") == "CVPRW_2024"
    assert normalize_conf_year_slug("CVPRW_2024") == "CVPRW_2024"

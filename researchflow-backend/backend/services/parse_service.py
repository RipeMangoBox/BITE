"""L2 parse service — extract structured content from PDF.

Parser Ensemble:
  1. GROBID → structured metadata (title, authors, affiliations, refs)
  2. PyMuPDF → text, sections, figure images (fast fallback)
  3. MinerU → formulas, tables, reading order (when API key configured)
  4. VLM → precise figure extraction, formula OCR, table content
     (only when ALLOW_LLM_IMAGE_UPLOAD=true)

Results are merged with conflict marking.
"""

import logging
from dataclasses import asdict
from pathlib import Path
import re
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.models.analysis import PaperAnalysis
from backend.models.enums import AnalysisLevel, PaperState
from backend.models.paper import Paper
from backend.services.object_storage import get_storage
from backend.utils.grobid_client import GrobidClient
from backend.utils.pdf_extract import parse_pdf, _extract_figure_captions
from backend.utils.mineru_client import MinerUClient, MinerUResult, get_mineru_client

logger = logging.getLogger(__name__)


def _mineru_text_parts(value) -> list[str]:
    """Extract text from MinerU content blocks without depending on one schema."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(_mineru_text_parts(item))
        return out
    if isinstance(value, dict):
        if isinstance(value.get("content"), str):
            return [value["content"]]
        out: list[str] = []
        for key in ("text", "title", "title_content", "table_caption", "image_caption", "chart_caption"):
            if key in value:
                out.extend(_mineru_text_parts(value.get(key)))
        return out
    return []


def _mineru_caption(content: dict, key: str) -> str:
    return " ".join(_mineru_text_parts(content.get(key))).strip()


def _mineru_table_index(caption: str, fallback: int) -> int:
    match = re.match(r"^\s*(?:Table|Tab\.)\s*(\d+)", caption, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return fallback


def _mineru_caption_label(caption: str, item_type: str, fallback: int) -> str:
    match = re.match(r"^\s*(Figure|Fig\.?|Table)\s*(\d+)", caption or "", flags=re.IGNORECASE)
    if match:
        kind = "Table" if match.group(1).lower().startswith("table") else "Figure"
        return f"{kind} {match.group(2)}"
    return f"{'Table' if item_type == 'table' else 'Figure'} {fallback}"


def _figure_key_slug(label: str, fallback: str) -> str:
    raw = label or fallback
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", raw.strip()).strip("._-")
    return slug or fallback


def _should_force_mineru(paper: Paper) -> bool:
    """Any paper that has entered scoring / analysis prioritization should use MinerU.

    In current pipeline terms, this means papers that already have keep_score or
    analysis_priority assigned, or have at least reached downloaded/L1/L2 states.
    """
    if paper.keep_score is not None or paper.analysis_priority is not None:
        return True
    return paper.state in (
        PaperState.DOWNLOADED,
        PaperState.L1_METADATA,
        PaperState.L2_PARSED,
        PaperState.L3_SKIMMED,
        PaperState.L4_DEEP,
        PaperState.CHECKED,
    )


async def _parse_with_local_mineru(pdf_path: str) -> MinerUResult | None:
    """Local MinerU CLI fallback when cloud MinerU API is unavailable."""
    try:
        import json
        import shutil
        import subprocess
        import tempfile
        from backend.utils.mineru_client import MinerUTable, MinerUFormula

        mineru_bin = shutil.which("mineru") or "/home/ripemangobox/miniconda3/bin/mineru"
        if not mineru_bin:
            return None

        with tempfile.TemporaryDirectory(prefix="rf_mineru_") as tmpdir:
            cmd = [mineru_bin, "-p", pdf_path, "-o", tmpdir, "-b", "pipeline"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            if proc.returncode != 0:
                logger.debug("Local mineru CLI failed for %s: %s", pdf_path, proc.stderr[:300])
                return None

            out_root = Path(tmpdir)
            md_candidates = list(out_root.rglob("*.md"))
            json_candidates = (
                list(out_root.rglob("*content_list_v2.json"))
                or list(out_root.rglob("*content_list.json"))
            )
            if not md_candidates:
                return None

            md_text = md_candidates[0].read_text(errors="ignore")
            result = MinerUResult(
                success=True,
                markdown=md_text,
                reading_order=[],
                metadata={"source": "local_mineru_cli"},
            )

            content = []
            json_base = out_root
            if json_candidates:
                try:
                    json_path = json_candidates[0]
                    json_base = json_path.parent
                    content = json.loads(json_path.read_text())
                except Exception:
                    content = []

            blocks = []
            for page in content:
                if isinstance(page, list):
                    blocks.extend(page)
                elif isinstance(page, dict):
                    blocks.append(page)

            preserved_root = Path(tempfile.mkdtemp(prefix="rf_mineru_preserve_"))
            preserved_images = preserved_root / "images"
            preserved_images.mkdir(parents=True, exist_ok=True)
            copied_paths: dict[str, str] = {}

            def _preserve_image(rel_path: str) -> str:
                if rel_path in copied_paths:
                    return copied_paths[rel_path]
                src = json_base / rel_path
                if not src.exists():
                    src = out_root / rel_path
                if not src.exists() or not src.is_file():
                    return ""
                dst = preserved_images / Path(rel_path).name
                shutil.copy2(src, dst)
                copied_paths[rel_path] = str(dst)
                return str(dst)

            for item in blocks:
                if not isinstance(item, dict):
                    continue
                if item.get("type") != "table":
                    continue
                c = item.get("content") or {}
                caption = _mineru_caption(c, "table_caption")
                result.tables.append(MinerUTable(
                    caption=caption,
                    table_index=_mineru_table_index(caption, len(result.tables) + 1),
                    page_num=item.get("page_idx", 0) or 0,
                    html=c.get("html", ""),
                    csv=c.get("csv", ""),
                    confidence=0.8,
                ))

            seen_formulas = set()
            for f in re.finditer(r"\$\$(.+?)\$\$", result.markdown, re.DOTALL):
                latex = f.group(1).strip()
                if not latex or latex in seen_formulas:
                    continue
                seen_formulas.add(latex)
                result.formulas.append(MinerUFormula(
                    latex=latex,
                    page_num=0,
                    location="display",
                    confidence=0.8,
                ))
            for item in blocks:
                if not isinstance(item, dict):
                    continue
                if item.get("type") not in {"equation_interline", "equation_inline", "inline_equation"}:
                    continue
                c = item.get("content") or {}
                latex = (c.get("math_content") or c.get("latex") or c.get("content") or "").strip()
                if not latex or latex in seen_formulas:
                    continue
                seen_formulas.add(latex)
                result.formulas.append(MinerUFormula(
                    latex=latex,
                    page_num=item.get("page_idx", 0) or 0,
                    location="display" if item.get("type") == "equation_interline" else "inline",
                    confidence=0.8,
                ))

            figure_paths = []
            type_counts = {"figure": 0, "table": 0}
            for item in blocks:
                if not isinstance(item, dict) or item.get("type") not in {"image", "table", "chart"}:
                    continue
                content_obj = item.get("content") or {}
                img_source = content_obj.get("image_source") or {}
                rel_path = img_source.get("path")
                if not rel_path:
                    continue
                abs_path = _preserve_image(rel_path)
                if not abs_path:
                    continue
                item_type = "table" if item.get("type") == "table" else "figure"
                type_counts[item_type] += 1
                cap_key = "table_caption" if item.get("type") == "table" else "image_caption"
                if item.get("type") == "chart":
                    cap_key = "chart_caption"
                caption = _mineru_caption(content_obj, cap_key)
                label = _mineru_caption_label(caption, item_type, type_counts[item_type])
                figure_paths.append({
                    "path": abs_path,
                    "caption": caption,
                    "page": item.get("page_idx", -1),
                    "bbox": item.get("bbox"),
                    "label": label,
                    "type": item_type,
                    "source_path": rel_path,
                })
            result.figures = figure_paths
            result.metadata["figure_paths"] = figure_paths
            return result
    except Exception as e:
        logger.debug("Local MinerU CLI unavailable for %s: %s", pdf_path, e)
        return None


async def parse_paper_pdf(session: AsyncSession, paper_id: UUID) -> PaperAnalysis | None:
    """Run L2 parse on a paper's PDF using parser ensemble.

    1. Try GROBID for structured metadata + references
    2. Use PyMuPDF for text extraction + figure images
    3. Merge results, preferring GROBID for metadata
    """
    paper = await session.get(Paper, paper_id)
    if not paper:
        return None

    # Find the PDF path
    pdf_path = await _resolve_pdf_path(paper)
    if not pdf_path:
        logger.warning(f"No PDF found for paper {paper_id}")
        return None

    # ── Parser Ensemble ──────────────────────────────────────────

    # 0. arXiv TeX source (highest fidelity for formulas/citations/figures)
    tex_result = None
    if paper.arxiv_id:
        try:
            from backend.services.tex_extraction_service import extract_all_from_tex
            tex_result = extract_all_from_tex(paper.arxiv_id)
            if tex_result:
                logger.info(
                    f"TeX extraction for {paper_id}: "
                    f"{len(tex_result['formulas'])} formulas, "
                    f"{len(tex_result['bibkeys'])} bibkeys, "
                    f"{len(tex_result['figures'])} figures"
                )
        except Exception as e:
            logger.debug(f"TeX extraction failed for {paper_id}: {e}")

    # 1. PyMuPDF (always available, fast fallback)
    pymupdf_result = parse_pdf(pdf_path)

    # 2. GROBID (structured metadata + references)
    grobid_result = None
    grobid_refs = []
    grobid_authors = []
    grobid_client = GrobidClient(settings.grobid_url)

    if await grobid_client.is_alive():
        try:
            grobid_result = await grobid_client.parse_fulltext(pdf_path)
            if grobid_result.references:
                grobid_refs = [
                    {
                        "ref_id": r.ref_id,
                        "title": r.title,
                        "authors": r.authors,
                        "venue": r.venue,
                        "year": r.year,
                        "doi": r.doi,
                        "arxiv_id": r.arxiv_id,
                    }
                    for r in grobid_result.references
                    if r.title  # skip empty refs
                ]
            if grobid_result.authors:
                grobid_authors = [
                    {
                        "name": a.name,
                        "given_name": a.given_name,
                        "surname": a.surname,
                        "affiliation": a.affiliation,
                        "email": a.email,
                        "orcid": a.orcid,
                    }
                    for a in grobid_result.authors
                ]
            logger.info(
                f"GROBID parsed {paper_id}: "
                f"{len(grobid_refs)} refs, {len(grobid_authors)} authors"
            )
        except Exception as e:
            logger.warning(f"GROBID parse failed for {paper_id}: {e}")
    else:
        logger.info("GROBID not available, using PyMuPDF only")

    # ── 3. MinerU: deep table + formula extraction ──────────────────
    mineru_result: MinerUResult | None = None
    force_mineru = _should_force_mineru(paper)
    mineru_client = get_mineru_client()
    if pdf_path and (mineru_client or force_mineru):
        try:
            if mineru_client:
                mineru_result = await mineru_client.parse_pdf(pdf_path)
            if (not mineru_result or not mineru_result.success) and force_mineru:
                mineru_result = await _parse_with_local_mineru(pdf_path)

            if mineru_result and mineru_result.success:
                logger.info(
                    "MinerU parsed %s: %d tables, %d formulas",
                    paper_id,
                    len(mineru_result.tables),
                    len(mineru_result.formulas),
                )
            elif mineru_result:
                logger.debug("MinerU parse skipped for %s: %s", paper_id, mineru_result.error)
        except Exception as e:
            logger.debug("MinerU unavailable for %s: %s", paper_id, e)

    # ── S2 fallback for refs + authors when GROBID fails ─────────
    if not grobid_refs:
        try:
            import httpx
            from backend.services.enrich_service import _s2_headers, _build_s2_id, _titles_similar
            S2_API = "https://api.semanticscholar.org/graph/v1"
            # Build S2 ID: arxiv_id → DOI → openreview URL → title search
            s2_id = _build_s2_id(paper) if hasattr(paper, 'doi') else (
                f"ARXIV:{paper.arxiv_id}" if paper.arxiv_id else None
            )
            async with httpx.AsyncClient(timeout=30) as client:
                # Title-based search fallback when no structured ID
                if not s2_id and paper.title:
                    from backend.utils.api_clients import limiters as _lim
                    await _lim["s2"].acquire()
                    search_resp = await client.get(
                        f"{S2_API}/paper/search",
                        params={"query": paper.title[:200], "limit": "1",
                                "fields": "title,externalIds"},
                        headers=_s2_headers(),
                    )
                    if search_resp.status_code == 200:
                        hits = search_resp.json().get("data", [])
                        if hits and _titles_similar(paper.title, hits[0].get("title", "")):
                            s2_id = hits[0].get("paperId")

                if not s2_id:
                    raise ValueError("No S2 paper ID found")
                # Fetch references
                resp = await client.get(
                    f"{S2_API}/paper/{s2_id}/references",
                    params={"fields": "title,year,venue,externalIds,authors", "limit": "100"},
                    headers=_s2_headers(),
                )
                if resp.status_code == 200:
                    for ref in resp.json().get("data", []):
                        cp = ref.get("citedPaper", {})
                        if cp.get("title"):
                            eids = cp.get("externalIds", {}) or {}
                            grobid_refs.append({
                                "ref_id": "", "title": cp["title"],
                                "authors": [a.get("name","") for a in (cp.get("authors") or [])[:5]],
                                "venue": cp.get("venue", ""), "year": str(cp.get("year", "")),
                                "doi": eids.get("DOI", ""), "arxiv_id": eids.get("ArXiv", ""),
                            })
                    logger.info(f"S2 fallback refs for {paper_id}: {len(grobid_refs)}")

                # Fetch detailed author info
                from backend.utils.api_clients import limiters
                await limiters["s2"].acquire()
                resp2 = await client.get(
                    f"{S2_API}/paper/{s2_id}/authors",
                    params={"fields": "name,affiliations,hIndex"},
                    headers=_s2_headers(),
                )
                if resp2.status_code == 200:
                    for a in resp2.json().get("data", []):
                        grobid_authors.append({
                            "name": a.get("name", ""), "given_name": "", "surname": "",
                            "affiliation": (a.get("affiliations") or [""])[0] if a.get("affiliations") else "",
                            "email": "", "orcid": "",
                        })
                    logger.info(f"S2 fallback authors for {paper_id}: {len(grobid_authors)}")
        except Exception as e:
            logger.debug(f"S2 fallback failed for {paper_id}: {e}")

    # ── Merge sections ───────────────────────────────────────────
    # Prefer GROBID sections if available (better structure), fall back to PyMuPDF
    def _clean_text(text: str) -> str:
        """Remove null bytes that PostgreSQL text columns cannot store."""
        return text.replace("\x00", "") if text else text

    def _deep_clean_nulls(obj):
        """Recursively strip \\x00 from every string in a nested dict/list.
        PostgreSQL JSONB rejects \\u0000; some PDFs leak NULL bytes into
        extracted text. Apply to evidence_spans / extracted_figure_images /
        figure_captions before INSERT."""
        if obj is None:
            return None
        if isinstance(obj, str):
            return obj.replace("\x00", "")
        if isinstance(obj, list):
            return [_deep_clean_nulls(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _deep_clean_nulls(v) for k, v in obj.items()}
        return obj

    merged_sections = {}
    if grobid_result and grobid_result.sections:
        merged_sections = {k: _clean_text(v[:5000]) for k, v in grobid_result.sections.items()}
        for k, v in pymupdf_result.sections.items():
            if k not in merged_sections:
                merged_sections[k] = _clean_text(v[:5000])
    else:
        merged_sections = {k: _clean_text(v[:5000]) for k, v in pymupdf_result.sections.items()}

    # ── Merge figure captions ────────────────────────────────────
    figure_captions = pymupdf_result.figure_captions
    if grobid_result and grobid_result.figure_captions:
        # GROBID captions may have better text; merge by checking overlap
        grobid_caps = grobid_result.figure_captions
        if len(grobid_caps) > len(figure_captions):
            figure_captions = grobid_caps

    # ── Merge table captions ─────────────────────────────────────
    table_captions = pymupdf_result.tables
    if grobid_result and grobid_result.table_captions:
        grobid_tabs = grobid_result.table_captions
        if len(grobid_tabs) > len(table_captions):
            table_captions = grobid_tabs

    # ── Supersede old L2 ─────────────────────────────────────────
    existing = await session.execute(
        select(PaperAnalysis).where(
            PaperAnalysis.paper_id == paper_id,
            PaperAnalysis.level == AnalysisLevel.L2_PARSE,
            PaperAnalysis.is_current.is_(True),
        )
    )
    old_analysis = existing.scalar_one_or_none()
    if old_analysis:
        old_analysis.is_current = False

    # ── Extract and upload figures ────────────────────────────────
    # Primary: VLM-guided precise extraction (1 API call)
    # Fallback: PyMuPDF heuristic extraction (free, CPU only)
    figure_image_records = []
    image_vlm_enabled = bool(
        settings.allow_llm_image_upload
        and (settings.anthropic_api_key or settings.openai_api_key)
    )

    if image_vlm_enabled and pdf_path:
        try:
            from backend.services.figure_extraction_service import extract_figures_precise
            figure_image_records = await extract_figures_precise(
                pdf_path=pdf_path,
                paper_id=paper_id,
                paper_title=paper.title,
                session=session,
            )
            if figure_image_records:
                logger.info(f"VLM figure extraction: {len(figure_image_records)} figures for {paper_id}")
        except Exception as e:
            logger.warning(f"VLM figure extraction failed, falling back to heuristic: {e}")

    # Fallback: heuristic extraction if VLM didn't produce results
    if not figure_image_records:
        figure_image_records = await _upload_figure_images(
            paper_id, pymupdf_result.figure_images, figure_captions
        )

    # ── Formula extraction ──────────────────────────────────────
    # Priority: TeX source (zero error) → VLM page scan → PyMuPDF regex
    extracted_formulas = pymupdf_result.formulas  # PyMuPDF regex as baseline
    grobid_formula_data = []
    formula_source = "pymupdf"

    if grobid_result and grobid_result.formulas:
        grobid_formula_data = [
            {"text": f.text, "label": f.label, "page": f.page, "bbox": f.bbox}
            for f in grobid_result.formulas
            if f.text
        ]

    # Priority 1: TeX source formulas (exact LaTeX, zero OCR error)
    if tex_result and tex_result.get("formulas"):
        extracted_formulas = [f["latex"] for f in tex_result["formulas"] if f.get("latex")]
        formula_source = "arxiv_tex"
        logger.info(f"Using TeX source formulas for {paper_id}: {len(extracted_formulas)} formulas (zero OCR error)")
    # Priority 2: VLM page scan (when no TeX available)
    elif pdf_path and image_vlm_enabled:
        try:
            from backend.services.formula_extraction_service import extract_formulas
            vlm_formulas = await extract_formulas(
                pdf_path=pdf_path,
                paper_id=paper_id,
                grobid_formulas=grobid_formula_data if grobid_formula_data else None,
                session=session,
            )
            if vlm_formulas:
                extracted_formulas = [f["latex"] for f in vlm_formulas if f.get("latex")]
                formula_source = "vlm"
                logger.info(f"Formula extraction: {len(vlm_formulas)} formulas via VLM for {paper_id}")
        except Exception as e:
            logger.warning(f"Formula extraction failed for {paper_id}: {e}")

    # ── Table content extraction (VLM → Markdown) ────────────────
    table_regions = [r for r in (figure_image_records or []) if r.get("type") == "table"]

    # Fallback: if VLM didn't tag any tables but PyMuPDF found table captions,
    # render table regions from PDF using figure_images that overlap with table captions
    if not table_regions and table_captions and pdf_path:
        try:
            import fitz as _fitz
            _doc = _fitz.open(pdf_path)
            for tc in table_captions[:8]:
                # Find a figure_image_record on a nearby page, or render a heuristic region
                # Simple approach: render the full-width region on the page where the caption is likely at
                for fig_rec in (figure_image_records or []):
                    cap_text = tc.get("caption", "").lower()
                    fig_label = (fig_rec.get("label") or "").lower()
                    if f"table {tc.get('table_num', -1)}" in fig_label or f"table {tc.get('table_num', -1)}" in (fig_rec.get("caption") or "").lower():
                        table_regions.append({**fig_rec, "type": "table", "table_num": tc.get("table_num")})
                        break
            _doc.close()
        except Exception as e:
            logger.debug(f"Table region fallback failed: {e}")

    if table_regions and image_vlm_enabled:
        try:
            from backend.services.vlm_extraction_service import extract_table_content
            table_contents = await extract_table_content(
                table_images=table_regions,
                paper_id=paper_id,
                session=session,
            )
            # Merge structured content into table_captions
            for tc in table_contents:
                for existing in table_captions:
                    if existing.get("table_num") == tc.get("table_num"):
                        existing["markdown"] = tc.get("markdown", "")
                        existing["headers"] = tc.get("headers", [])
                        existing["rows"] = tc.get("rows", [])
                        break
                else:
                    table_captions.append(tc)
            logger.info(f"Table content extraction: {len(table_contents)} tables for {paper_id}")
        except Exception as e:
            logger.warning(f"Table content extraction failed for {paper_id}: {e}")

    # ── MinerU merge: tables → table_captions ──────────────────────
    if mineru_result and mineru_result.tables:
        for mt in mineru_result.tables:
            # Match to existing caption entry by table_index or caption text
            matched = False
            for existing in table_captions:
                if existing.get("table_num") == mt.table_index:
                    if mt.html:
                        existing["html"] = mt.html
                    if mt.csv:
                        existing["csv"] = mt.csv
                    existing["mineru_confidence"] = mt.confidence
                    matched = True
                    break
            if not matched:
                # Try matching by caption substring
                for existing in table_captions:
                    cap = existing.get("caption", "")
                    if cap and mt.caption and (
                        cap[:30] in mt.caption or mt.caption[:30] in cap
                    ):
                        if mt.html:
                            existing["html"] = mt.html
                        if mt.csv:
                            existing["csv"] = mt.csv
                        existing["mineru_confidence"] = mt.confidence
                        matched = True
                        break
            if not matched and (mt.html or mt.caption):
                table_captions.append({
                    "table_num": mt.table_index,
                    "caption": mt.caption,
                    "html": mt.html,
                    "csv": mt.csv,
                    "mineru_confidence": mt.confidence,
                })
        logger.info(
            "MinerU tables merged: %d into %d existing for %s",
            len(mineru_result.tables), len(table_captions), paper_id,
        )

    # ── MinerU merge: formulas (supplement, lower priority than TeX) ─
    if mineru_result and mineru_result.formulas:
        if formula_source in ("pymupdf",):  # Only supplement when no better source
            mineru_latex = [f.latex for f in mineru_result.formulas if f.latex]
            if mineru_latex:
                extracted_formulas = list(dict.fromkeys(
                    list(extracted_formulas) + mineru_latex
                ))  # Deduplicate preserving order
                formula_source = "mineru"
                logger.info(
                    "MinerU formulas supplement: %d added to %d existing for %s",
                    len(mineru_latex), len(extracted_formulas), paper_id,
                )

    # ── Build parse metadata ─────────────────────────────────────
    parse_metadata = {
        "parsers_used": ["pymupdf"],
        "grobid_available": grobid_result is not None,
        "tex_available": tex_result is not None,
        "formula_source": formula_source,
        "grobid_ref_count": len(grobid_refs),
        "grobid_author_count": len(grobid_authors),
        "pymupdf_section_count": len(pymupdf_result.sections),
        "pymupdf_formula_count": len(pymupdf_result.formulas),
        "grobid_formula_count": len(grobid_formula_data),
        "tex_formula_count": len(tex_result["formulas"]) if tex_result else 0,
        "tex_bibkey_count": len(tex_result["bibkeys"]) if tex_result else 0,
        "tex_figure_count": len(tex_result["figures"]) if tex_result else 0,
        "final_formula_count": len(extracted_formulas),
        "pymupdf_figure_count": len(pymupdf_result.figure_captions),
        "llm_image_upload_enabled": settings.allow_llm_image_upload,
        "vlm_available": image_vlm_enabled,
        "mineru_available": mineru_result is not None and mineru_result.success,
        "mineru_table_count": len(mineru_result.tables) if mineru_result else 0,
        "mineru_formula_count": len(mineru_result.formulas) if mineru_result else 0,
    }
    if tex_result:
        parse_metadata["parsers_used"].append("arxiv_tex")
    if grobid_result:
        parse_metadata["parsers_used"].append("grobid")
    if mineru_result and mineru_result.success:
        parse_metadata["parsers_used"].append("mineru")

    # ── Create L2 analysis ───────────────────────────────────────
    # Apply NULL-byte scrubber to ALL JSONB fields and the formulas array,
    # in addition to the section-level _clean_text. Some PDFs leak \x00
    # which PostgreSQL JSONB outright rejects.
    analysis = PaperAnalysis(
        paper_id=paper_id,
        level=AnalysisLevel.L2_PARSE,
        model_provider="local",
        model_name="ensemble_pymupdf_grobid",
        prompt_version="v2",
        schema_version="v2",
        confidence=1.0,
        extracted_sections=_deep_clean_nulls(merged_sections),
        extracted_formulas=[_clean_text(f) for f in extracted_formulas] if extracted_formulas else extracted_formulas,
        extracted_tables=_deep_clean_nulls(table_captions),
        figure_captions=_deep_clean_nulls(figure_captions),
        extracted_figure_images=_deep_clean_nulls(figure_image_records) if figure_image_records else None,
        # Store GROBID-specific results in evidence_spans (repurposed for L2)
        evidence_spans=_deep_clean_nulls({
            "grobid_references": grobid_refs,
            "grobid_authors": grobid_authors,
            "grobid_abstract": grobid_result.abstract if grobid_result else None,
            "grobid_keywords": grobid_result.keywords if grobid_result else [],
            "tex_bibkeys": tex_result["bibkeys"] if tex_result else [],
            "tex_figures": tex_result["figures"][:20] if tex_result else [],
            "tex_urls": tex_result["urls"] if tex_result else {},
            "tex_formulas_labeled": [
                {"latex": f["latex"], "label": f["label"], "env": f["env_type"]}
                for f in (tex_result["formulas"] if tex_result else [])
                if f.get("label")
            ][:30],
            "parse_metadata": parse_metadata,
            "section_hierarchy": pymupdf_result.sections_hierarchy if pymupdf_result else [],
            "citation_contexts": pymupdf_result.citation_contexts[:100] if pymupdf_result else [],
            "dataset_mentions": pymupdf_result.dataset_mentions if pymupdf_result else [],
            # MinerU output (for downstream deep_ingest table/formula enhancement)
            "mineru_markdown": mineru_result.markdown[:10000] if mineru_result and mineru_result.markdown else "",
            "mineru_reading_order": mineru_result.reading_order if mineru_result else [],
            "mineru_doc_metadata": mineru_result.metadata if mineru_result else {},
        }),
        is_current=True,
    )
    session.add(analysis)

    # ── Update paper with GROBID metadata ────────────────────────
    if grobid_result:
        # Only fill missing fields (don't overwrite existing)
        if not paper.abstract and grobid_result.abstract:
            paper.abstract = grobid_result.abstract
        if not paper.authors and grobid_authors:
            paper.authors = grobid_authors
        if not paper.keywords and grobid_result.keywords:
            paper.keywords = grobid_result.keywords

        # Store references text for downstream analysis
        if not pymupdf_result.references_text and "references" in merged_sections:
            pymupdf_result.references_text = merged_sections.get("references", "")

    # Update paper state
    if paper.state in (PaperState.WAIT, PaperState.DOWNLOADED, PaperState.L1_METADATA,
                       PaperState.ENRICHED, PaperState.CANONICALIZED):
        paper.state = PaperState.L2_PARSED

    await session.flush()
    await session.refresh(analysis)

    return analysis


async def _resolve_pdf_path(paper: Paper) -> str | None:
    """Resolve the PDF file path from object storage or local path."""
    storage = get_storage()

    if paper.pdf_object_key:
        local_path = storage.get_local_path(paper.pdf_object_key)
        if local_path:
            return local_path

    if paper.pdf_path_local:
        import os
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        candidate = os.path.join(project_root, paper.pdf_path_local)
        if os.path.exists(candidate):
            return candidate

    return None


async def _upload_figure_images(
    paper_id: UUID,
    figure_images: list[dict],
    figure_captions: list[dict] | None = None,
) -> list[dict]:
    """Upload extracted figure images to object storage.

    Each figure gets:
      - Stored at papers/{paper_id}/figures/fig_001.png
      - public_url for CDN/Obsidian remote reference
      - Matched caption from GROBID/PyMuPDF
      - bbox and extraction_method metadata
    """
    if not figure_images:
        return []

    storage = get_storage()
    records = []
    captions = figure_captions or []

    for i, fig in enumerate(figure_images):
        ext = fig.get("ext", "png")
        object_key = f"papers/{paper_id}/figures/fig_{i+1:03d}.{ext}"
        try:
            await storage.put(object_key, fig["image_bytes"])
            record = {
                "figure_num": i + 1,
                "object_key": object_key,
                "page_num": fig.get("page_num", -1),
                "width": fig.get("width", 0),
                "height": fig.get("height", 0),
                "size_bytes": fig.get("size_bytes", 0),
                "extraction_method": fig.get("extraction_method", "unknown"),
                "bbox": fig.get("bbox"),
            }

            # Add public URL for report embedding
            public_url = storage.get_public_url(object_key)
            if public_url:
                record["public_url"] = public_url

            # Match caption by page proximity
            best_caption = _match_caption_to_figure(fig, captions, i)
            if best_caption:
                record["caption"] = best_caption.get("caption", "")
                record["caption_label"] = best_caption.get("label") or f"Figure {best_caption.get('figure_num', i+1)}"

            records.append(record)
        except Exception as e:
            logger.warning(f"Failed to store figure {i+1} for {paper_id}: {e}")

    return records


async def _upload_mineru_figure_images(
    paper_id: UUID,
    mineru_result: MinerUResult,
    figure_captions: list[dict] | None = None,
) -> list[dict]:
    """Upload MinerU-produced figure files into object storage."""
    if not mineru_result or not getattr(mineru_result, "metadata", None):
        return []

    figure_paths = (mineru_result.metadata or {}).get("figure_paths") or []
    figure_captions = figure_captions or []
    storage = get_storage()
    records = []

    for i, item in enumerate(figure_paths, start=1):
        path = Path(item.get("path") or "")
        if not path.exists() or not path.is_file():
            continue
        ext = path.suffix.lower().lstrip(".") or "png"
        label = item.get("label") or f"{'Table' if item.get('type') == 'table' else 'Figure'} {i}"
        key_label = _figure_key_slug(label, f"fig_{i:03d}")
        object_key = f"papers/{paper_id}/figures/{i:03d}_{key_label}.{ext}"
        try:
            data = path.read_bytes()
            await storage.put(object_key, data)
            record = {
                "figure_num": i,
                "object_key": object_key,
                "page_num": item.get("page", -1),
                "width": item.get("width", 0),
                "height": item.get("height", 0),
                "size_bytes": len(data),
                "extraction_method": "mineru",
                "bbox": item.get("bbox"),
                "caption": item.get("caption", ""),
                "source_path": item.get("source_path") or str(path),
                "label": label,
                "caption_label": label,
                "type": item.get("type", "figure"),
            }
            public_url = storage.get_public_url(object_key)
            if public_url:
                record["public_url"] = public_url
            if not record.get("caption"):
                best_caption = _match_caption_to_figure(record, figure_captions, i - 1)
                if best_caption:
                    record["caption"] = best_caption.get("caption", "")
                    record["caption_label"] = best_caption.get("label") or f"Figure {i}"
            records.append(record)
        except Exception as e:
            logger.warning("Failed to store MinerU figure %s for %s: %s", path, paper_id, e)

    return records


def _match_caption_to_figure(
    fig: dict,
    captions: list[dict],
    fig_index: int,
) -> dict | None:
    """Match a figure image to its caption by page number or index."""
    fig_page = fig.get("page_num", -1)

    # Try matching by page number (captions near the figure)
    page_captions = [c for c in captions if c.get("page_num") == fig_page]
    if page_captions:
        return page_captions[0]

    # Fallback: match by figure_num index
    for cap in captions:
        if cap.get("figure_num") == fig_index + 1:
            return cap

    # Fallback: match by order
    if fig_index < len(captions):
        return captions[fig_index]

    return None


async def parse_all_unprocessed(session: AsyncSession, limit: int = 10) -> list[dict]:
    """Parse PDFs for papers that have a PDF but no L2 analysis."""
    result = await session.execute(
        select(Paper)
        .where(
            Paper.pdf_path_local.isnot(None),
            Paper.state.in_([
                PaperState.WAIT, PaperState.DOWNLOADED,
                PaperState.L1_METADATA, PaperState.ENRICHED,
            ]),
        )
        .order_by(Paper.analysis_priority.desc().nullsfirst())
        .limit(limit)
    )
    papers = list(result.scalars().all())

    results = []
    for paper in papers:
        try:
            analysis = await parse_paper_pdf(session, paper.id)
            if analysis:
                section_names = list(analysis.extracted_sections.keys()) if analysis.extracted_sections else []
                grobid_data = analysis.evidence_spans or {}
                results.append({
                    "paper_id": str(paper.id),
                    "title": paper.title[:60],
                    "status": "parsed",
                    "sections": section_names,
                    "formulas": len(analysis.extracted_formulas or []),
                    "figures": len(analysis.figure_captions or []),
                    "tables": len(analysis.extracted_tables or []),
                    "grobid_refs": len(grobid_data.get("grobid_references", [])),
                    "grobid_authors": len(grobid_data.get("grobid_authors", [])),
                })
            else:
                results.append({
                    "paper_id": str(paper.id),
                    "title": paper.title[:60],
                    "status": "no_pdf",
                })
        except Exception as e:
            logger.error(f"Parse error for {paper.id}: {e}")
            results.append({
                "paper_id": str(paper.id),
                "title": paper.title[:60],
                "status": "error",
                "message": str(e)[:100],
            })

    await session.flush()
    return results


async def parse_paper_pdf_mineru_only(session: AsyncSession, paper_id: UUID) -> PaperAnalysis | None:
    """Formal MinerU-only L2 parse used by the clean ICLR26 rebuild path."""
    paper = await session.get(Paper, paper_id)
    if not paper:
        return None

    pdf_path = await _resolve_pdf_path(paper)
    if not pdf_path:
        logger.warning("No PDF found for paper %s", paper_id)
        return None

    mineru_result: MinerUResult | None = None
    mineru_client = get_mineru_client()
    if mineru_client:
        mineru_result = await mineru_client.parse_pdf(pdf_path)
    if not mineru_result or not mineru_result.success:
        mineru_result = await _parse_with_local_mineru(pdf_path)
    if not mineru_result or not mineru_result.success:
        try:
            from backend.utils import mineru_adapter
            adapter_result = mineru_adapter.parse_pdf(pdf_path)
            if adapter_result and adapter_result.success:
                mineru_result = MinerUResult(
                    success=True,
                    markdown=adapter_result.markdown_text,
                    tables=[],
                    formulas=[
                        MinerUFormula(
                            latex=f.get("latex", ""),
                            page_num=f.get("page", 0),
                            location=f.get("type", "display"),
                            confidence=1.0,
                        )
                        for f in (adapter_result.formulas or [])
                    ],
                    figures=adapter_result.figures or [],
                    reading_order=[],
                    metadata=adapter_result.metadata or {},
                )
        except Exception as e:
            logger.warning("MinerU adapter fallback failed for %s: %s", paper_id, e)
    if not mineru_result or not mineru_result.success:
        logger.warning("MinerU-only parse failed for %s", paper_id)
        return None

    def _clean_text(text: str) -> str:
        return text.replace("\x00", "") if text else text

    def _deep_clean_nulls(obj):
        if obj is None:
            return None
        if isinstance(obj, str):
            return obj.replace("\x00", "")
        if isinstance(obj, list):
            return [_deep_clean_nulls(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _deep_clean_nulls(v) for k, v in obj.items()}
        return obj

    merged_sections = _extract_sections_from_mineru_markdown(mineru_result.markdown)

    figure_captions = _extract_figure_captions(mineru_result.markdown or "")
    table_captions = normalize_mineru_tables(mineru_result)
    figure_image_records = await _upload_mineru_figure_images(
        paper_id, mineru_result, figure_captions,
    )
    extracted_formulas = [f.latex for f in mineru_result.formulas if f.latex]

    existing = await session.execute(
        select(PaperAnalysis).where(
            PaperAnalysis.paper_id == paper_id,
            PaperAnalysis.level == AnalysisLevel.L2_PARSE,
            PaperAnalysis.is_current.is_(True),
        )
    )
    old_analysis = existing.scalar_one_or_none()
    if old_analysis:
        old_analysis.is_current = False

    parse_metadata = {
        "parsers_used": ["mineru"],
        "grobid_available": False,
        "tex_available": False,
        "formula_source": "mineru",
        "grobid_ref_count": 0,
        "grobid_author_count": 0,
        "pymupdf_section_count": 0,
        "pymupdf_formula_count": 0,
        "grobid_formula_count": 0,
        "tex_formula_count": 0,
        "tex_bibkey_count": 0,
        "tex_figure_count": 0,
        "final_formula_count": len(extracted_formulas),
        "pymupdf_figure_count": 0,
        "llm_image_upload_enabled": False,
        "vlm_available": False,
        "mineru_available": True,
        "mineru_table_count": len(mineru_result.tables),
        "mineru_formula_count": len(mineru_result.formulas),
    }

    analysis = PaperAnalysis(
        paper_id=paper_id,
        level=AnalysisLevel.L2_PARSE,
        model_provider="local",
        model_name="mineru_only",
        prompt_version="v3_mineru_only",
        schema_version="v3",
        confidence=1.0,
        extracted_sections=_deep_clean_nulls(merged_sections),
        extracted_formulas=[_clean_text(f) for f in extracted_formulas] if extracted_formulas else [],
        extracted_tables=_deep_clean_nulls(table_captions),
        figure_captions=_deep_clean_nulls(figure_captions),
        extracted_figure_images=_deep_clean_nulls(figure_image_records) if figure_image_records else None,
        evidence_spans=_deep_clean_nulls({
            "grobid_references": [],
            "grobid_authors": [],
            "grobid_abstract": None,
            "grobid_keywords": [],
            "parse_metadata": parse_metadata,
            "section_hierarchy": [],
            "citation_contexts": [],
            "dataset_mentions": [],
            "mineru_markdown": (mineru_result.markdown or "")[:10000],
            "mineru_reading_order": mineru_result.reading_order or [],
            "mineru_doc_metadata": mineru_result.metadata or {},
        }),
        is_current=True,
    )
    session.add(analysis)

    if paper.state in (
        PaperState.WAIT, PaperState.DOWNLOADED, PaperState.L1_METADATA,
        PaperState.ENRICHED, PaperState.CANONICALIZED,
    ):
        paper.state = PaperState.L2_PARSED

    await session.flush()
    await session.refresh(analysis)
    return analysis


def normalize_mineru_tables(mineru_result: MinerUResult) -> list[dict]:
    tables = []
    for table in mineru_result.tables or []:
        tables.append({
            "table_num": table.table_index,
            "caption": table.caption,
            "html": table.html,
            "csv": table.csv,
            "mineru_confidence": table.confidence,
        })
    return tables


def _extract_sections_from_mineru_markdown(markdown_text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    if not markdown_text:
        return sections
    lines = markdown_text.splitlines()
    current = "preamble"
    buf: list[str] = []
    mapping = {
        "abstract": "abstract",
        "introduction": "introduction",
        "related work": "related_work",
        "background": "introduction",
        "method": "method",
        "approach": "method",
        "framework": "method",
        "experiment": "experiments",
        "evaluation": "experiments",
        "results": "experiments",
        "ablation": "ablation",
        "conclusion": "conclusion",
        "discussion": "conclusion",
        "references": "references",
    }
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = re.sub(r"^#+\s*", "", stripped).strip().lower()
            matched = None
            for key, value in mapping.items():
                if key in heading:
                    matched = value
                    break
            if matched:
                content = "\n".join(buf).strip()
                if content:
                    sections[current] = content[:5000]
                current = matched
                buf = []
                continue
        buf.append(line)
    content = "\n".join(buf).strip()
    if content:
        sections[current] = content[:5000]
    return sections

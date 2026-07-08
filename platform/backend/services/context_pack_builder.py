"""Context Pack Builder — assembles tailored context for each agent.

4 context layers: Global → Domain → Paper → Run
Each agent gets a different subset with a token budget.
"""

import logging
from uuid import UUID

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.agent import AgentBlackboardItem
from backend.models.analysis import PaperAnalysis
from backend.models.domain import DomainSpec
from backend.models.evidence import EvidenceUnit
from backend.models.method import MethodNode
from backend.models.taxonomy import TaxonomyNode

logger = logging.getLogger(__name__)


class ContextPackBuilder:
    """Builds context packs for agents from 4 layers: global, domain, paper, run."""

    # ── Global Schema Constants ──────────────────────────────────────────

    GLOBAL_NODE_TYPES = (
        "Node types: T__Task, M__Method, C__Mechanism, P__Paper, "
        "D__Dataset, L__Lineage, Lab__Team"
    )
    GLOBAL_RELATION_TYPES = (
        "Relation types: proposes_method, evaluates_on, uses_dataset, "
        "compares_against, modifies_slot, extends_method, cites_as_baseline, "
        "belongs_to_task, part_of_lineage, produced_by_lab"
    )
    GLOBAL_REFERENCE_ROLE_DEFS = """Reference roles:
- direct_baseline: paper method section explicitly builds on this
- method_source: core algorithmic idea comes from this
- formula_source: key equations derived from this
- dataset_source: introduces dataset used in experiments
- benchmark_source: introduces benchmark used for evaluation
- comparison_baseline: appears in main experiment table as comparison
- same_task_prior_work: prior work on same task
- survey_or_taxonomy: survey/overview paper
- background_citation: general background reference
- implementation_reference: used for implementation details
- unimportant_related_work: not directly relevant"""

    GLOBAL_SLOT_TYPES = (
        "Slot types: architecture, objective, data_pipeline, "
        "inference_strategy, training_recipe, reward_design, "
        "credit_assignment, exploration_strategy"
    )
    GLOBAL_EDGE_RULES = """Edge creation rules:
- proposes_method: paper introduces a new method node
- evaluates_on: paper runs experiments on a dataset/benchmark
- uses_dataset: paper uses dataset for training/fine-tuning
- compares_against: paper compares with a baseline in experiment tables
- modifies_slot: paper changes a specific slot in an existing method
- extends_method: paper extends an existing method without replacing it
- cites_as_baseline: paper cites another as its baseline method
- belongs_to_task: paper addresses a specific task
- part_of_lineage: method belongs to a lineage chain
- produced_by_lab: paper/method produced by a research team"""

    GLOBAL_EXPERIMENT_SCHEMA = """Experiment schema:
- benchmark_name: str — name of the benchmark
- dataset_name: str — dataset used
- metric_name: str — evaluation metric
- proposed_value: float — result of proposed method
- baseline_values: dict[str, float] — baseline name → value
- delta_abs: float — absolute improvement
- delta_pct: float — percentage improvement
- is_sota: bool — claims state-of-the-art
- ablation_rows: list[dict] — ablation study rows"""

    GLOBAL_SCORE_SIGNAL_DEFS = """Score signal definitions:
- is_direct_baseline: bool — this paper is a direct baseline for the anchor
- in_experiment_table: bool — appears in experiment comparison tables
- same_primary_task: bool — addresses the same primary task
- has_changed_slots: bool — modifies one or more method slots
- has_ablation: bool — includes ablation study
- has_code: bool — code is publicly available
- has_new_dataset: bool — introduces a new dataset
- citation_density: float — how often cited in the paper body (0-1)
- method_novelty: float — degree of method novelty (0-1)
- evidence_quality: float — strength of experimental evidence (0-1)"""

    GLOBAL_PROFILE_SCHEMA = """Node profile schema:
- name: str — canonical name
- type: str — node type (Task/Method/Mechanism/...)
- aliases: list[str] — alternative names
- description: str — concise description
- key_papers: list[str] — representative paper titles
- connected_tasks: list[str] — related tasks
- connected_methods: list[str] — related methods
- evolution_stage: str — seed/emerging/established
- summary_stats: dict — paper count, citation count, etc."""

    GLOBAL_EDGE_PROFILE_SCHEMA = """Edge profile schema:
- source_node: str — source node name
- target_node: str — target node name
- relation_type: str — edge type
- evidence_count: int — number of supporting evidence units
- confidence: float — aggregate confidence
- representative_papers: list[str] — papers supporting this edge
- description: str — natural language description of the relation"""

    GLOBAL_REPORT_SECTION_SCHEMA = """Report section schema:
- metadata_overview: paper metadata table plus `> [!tip] 效果简介` callout.
- background_motivation: concrete problem, named baselines, and their bottleneck.
- core_innovation: one causal insight, not a TL;DR or contribution list.
- framework_overview: system skeleton and module responsibilities.
- module_formulas: 2-3 key modules with formula intuition and evidence.
- experiment_analysis: original table/figure markers plus numeric prose summary.
- lineage_positioning: deterministic method family, parent/baseline relations,
  changed slots, facets, and follow-up positioning."""

    _GLOBAL_ITEMS = {
        "node_types": GLOBAL_NODE_TYPES,
        "relation_types": GLOBAL_RELATION_TYPES,
        "reference_role_definitions": GLOBAL_REFERENCE_ROLE_DEFS,
        "slot_types": GLOBAL_SLOT_TYPES,
        "edge_rules": GLOBAL_EDGE_RULES,
        "experiment_schema": GLOBAL_EXPERIMENT_SCHEMA,
        "score_signal_definitions": GLOBAL_SCORE_SIGNAL_DEFS,
        "profile_schema": GLOBAL_PROFILE_SCHEMA,
        "edge_profile_schema": GLOBAL_EDGE_PROFILE_SCHEMA,
        "report_section_schema": GLOBAL_REPORT_SECTION_SCHEMA,
    }

    # ── Pack Configurations ──────────────────────────────────────────────

    PACK_CONFIGS = {
        "analysis_agent": {
            "global": [
                "node_types", "relation_types", "slot_types",
                "reference_role_definitions", "experiment_schema",
                "edge_rules", "profile_schema", "edge_profile_schema",
            ],
            "domain": [
                "scope", "existing_tasks_summary", "existing_methods_summary",
                "baselines", "known_benchmarks", "graph_summary",
                "task_hierarchy", "method_hierarchy",
            ],
            "paper": [
                "abstract", "introduction_excerpt", "method_section_full",
                "algorithm_blocks", "all_formula_contexts", "result_tables",
                "experiment_section", "ablation_section", "reference_list",
                "citation_contexts", "figure_image_metadata",
                "mineru_markdown_excerpt",
            ],
            "run": [],
            "token_budget": 80_000,
        },

        "writer_agent": {
            "global": ["report_section_schema"],
            "domain": [],
            "paper": [
                "selected_evidence", "figure_image_metadata",
                "lineage_positioning_context",
            ],
            "run": ["ALL_VERIFIED"],
            "token_budget": 80_000,
        },

        # ── Shallow Phase (merged) ──
        "shallow_extractor": {
            "global": ["node_types", "relation_types", "slot_types"],
            "domain": ["scope", "existing_tasks_summary", "existing_methods_summary", "baselines"],
            "paper": [
                "abstract", "introduction_excerpt", "method_excerpt",
                "experiment_excerpt", "figure_table_captions",
                "algorithm_blocks", "formula_contexts",
            ],
            "run": [],
            "token_budget": 18_000,
        },
        "reference_role": {
            "global": ["reference_role_definitions"],
            "domain": ["anchor_paper_titles"],
            "paper": ["reference_list", "citation_contexts"],
            "run": [],
            "token_budget": 30_000,
        },

        # ── Deep Phase (merged) ──
        "deep_analyzer": {
            "global": ["slot_types", "relation_types", "experiment_schema"],
            "domain": ["method_profiles", "baseline_profiles", "known_benchmarks"],
            "paper": [
                "method_section_full", "algorithm_blocks", "all_formula_contexts",
                "result_tables", "experiment_section", "ablation_section",
                "mineru_markdown_excerpt",
            ],
            "run": ["shallow_extract", "reference_role_map"],
            "token_budget": 40_000,
        },
        "graph_candidate": {
            "global": ["node_types", "relation_types", "edge_rules"],
            "domain": ["graph_summary", "task_hierarchy", "method_hierarchy"],
            "paper": [],
            "run": [
                "shallow_extract", "deep_analysis",
                "reference_role_map",
            ],
            "token_budget": 20_000,
        },

        # ── Profile Phase (merged) ──
        "kb_profiler": {
            "global": ["profile_schema", "edge_profile_schema"],
            "domain": [],
            "paper": [],
            "run": ["graph_candidates"],
            "token_budget": 20_000,
        },

        # ── Report Phase ──
        "paper_report": {
            "global": ["report_section_schema"],
            "domain": [],
            "paper": ["selected_evidence", "figure_image_metadata"],
            "run": ["ALL_VERIFIED"],
            "token_budget": 80_000,
        },

    }

    LEGACY_PACK_CONFIGS = PACK_CONFIGS.copy()
    LEGACY_PACK_CONFIGS.pop("analysis_agent", None)
    LEGACY_PACK_CONFIGS.pop("writer_agent", None)
    PACK_CONFIGS = {
        "analysis_agent": PACK_CONFIGS["analysis_agent"],
        "writer_agent": PACK_CONFIGS["writer_agent"],
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def build(
        self,
        pack_name: str,
        *,
        paper_id: UUID | None = None,
        candidate_id: UUID | None = None,
        domain_id: UUID | None = None,
        run_items: dict | None = None,
    ) -> dict:
        """Build a context pack for the given agent.

        Returns dict with keys: system_prompt, user_content, token_budget, metadata.
        """
        if pack_name not in self.PACK_CONFIGS:
            raise ValueError(f"Unknown pack: {pack_name!r}. "
                             f"Available: {list(self.PACK_CONFIGS.keys())}")

        config = self.PACK_CONFIGS[pack_name]
        budget = config["token_budget"]

        # Assemble layers
        parts: list[str] = []

        # Layer 1: Global
        if config["global"]:
            global_text = await self._load_global_context(config["global"])
            if global_text:
                parts.append(f"=== GLOBAL SCHEMA ===\n{global_text}")

        # Layer 2: Domain
        if config["domain"] and domain_id:
            domain_text = await self._load_domain_context(domain_id, config["domain"])
            if domain_text:
                parts.append(f"=== DOMAIN CONTEXT ===\n{domain_text}")

        # Layer 3: Paper
        if config["paper"] and paper_id:
            paper_text = await self._load_paper_context(paper_id, config["paper"])
            if paper_text:
                parts.append(f"=== PAPER CONTEXT ===\n{paper_text}")

        # Layer 4: Run (blackboard items)
        if config["run"]:
            run_text = await self._load_run_context(
                paper_id, candidate_id, config["run"], run_items,
            )
            if run_text:
                parts.append(f"=== RUN CONTEXT ===\n{run_text}")

        user_content = "\n\n".join(parts)
        user_content = self._truncate_to_budget(user_content, budget)

        return {
            "system_prompt": f"You are the {pack_name} agent.",
            "user_content": user_content,
            "token_budget": budget,
            "metadata": {
                "pack_name": pack_name,
                "paper_id": str(paper_id) if paper_id else None,
                "candidate_id": str(candidate_id) if candidate_id else None,
                "domain_id": str(domain_id) if domain_id else None,
                "layers_included": [
                    layer for layer in ("global", "domain", "paper", "run")
                    if config[layer]
                ],
            },
        }

    # ── Layer Loaders ────────────────────────────────────────────────────

    async def _load_global_context(self, items: list[str]) -> str:
        """Return static schema definitions for the requested global items."""
        sections: list[str] = []
        for item in items:
            content = self._GLOBAL_ITEMS.get(item)
            if content:
                sections.append(content)
            else:
                logger.warning("Unknown global context item: %s", item)
        return "\n\n".join(sections)

    async def _load_domain_context(self, domain_id: UUID, items: list[str]) -> str:
        """Query DB for domain-level context."""
        sections: list[str] = []

        # Load DomainSpec for scope-related items
        domain = (
            await self.session.execute(
                select(DomainSpec).where(DomainSpec.id == domain_id)
            )
        ).scalar_one_or_none()

        if not domain:
            logger.warning("Domain %s not found", domain_id)
            return ""

        for item in items:
            if item == "scope":
                scope_parts = []
                if domain.scope_tasks:
                    scope_parts.append(f"Tasks: {', '.join(domain.scope_tasks)}")
                if domain.scope_modalities:
                    scope_parts.append(f"Modalities: {', '.join(domain.scope_modalities)}")
                if domain.scope_paradigms:
                    scope_parts.append(f"Paradigms: {', '.join(domain.scope_paradigms)}")
                if domain.negative_scope:
                    scope_parts.append(f"Excluded: {', '.join(domain.negative_scope)}")
                if scope_parts:
                    sections.append(f"[Domain Scope]\n" + "\n".join(scope_parts))

            elif item == "anchor_paper_titles":
                if domain.seed_paper_ids:
                    # Return seed paper IDs as anchors (titles resolved at query time)
                    sections.append(
                        f"[Anchor Papers]\n"
                        f"Seed paper IDs: {', '.join(str(pid) for pid in domain.seed_paper_ids)}"
                    )

            elif item in ("existing_tasks_summary", "task_hierarchy"):
                rows = (
                    await self.session.execute(
                        select(TaxonomyNode.name, TaxonomyNode.description)
                        .where(TaxonomyNode.dimension == "task")
                        .order_by(TaxonomyNode.sort_order)
                        .limit(50)
                    )
                ).all()
                if rows:
                    lines = [f"- {r.name}: {r.description or '(no desc)'}" for r in rows]
                    sections.append(f"[Existing Tasks]\n" + "\n".join(lines))

            elif item in ("existing_methods_summary", "existing_methods_with_slots",
                          "method_profiles", "method_hierarchy"):
                rows = (
                    await self.session.execute(
                        select(MethodNode.name, MethodNode.type, MethodNode.maturity,
                               MethodNode.description)
                        .order_by(MethodNode.downstream_count.desc())
                        .limit(50)
                    )
                ).all()
                if rows:
                    lines = []
                    for r in rows:
                        line = f"- {r.name} ({r.type}, {r.maturity})"
                        if r.description:
                            line += f": {r.description[:120]}"
                        lines.append(line)
                    sections.append(f"[Existing Methods]\n" + "\n".join(lines))

                # For items requesting slots, load from paradigm_templates.slots JSONB
                if item in ("existing_methods_with_slots", "method_profiles"):
                    from backend.models.analysis import ParadigmTemplate
                    pt_rows = (
                        await self.session.execute(
                            select(ParadigmTemplate.name, ParadigmTemplate.slots).limit(10)
                        )
                    ).all()
                    slot_lines = []
                    for pt in pt_rows:
                        if pt.slots and isinstance(pt.slots, dict):
                            for sname, sinfo in pt.slots.items():
                                desc = sinfo.get("description", "") if isinstance(sinfo, dict) else ""
                                slot_lines.append(f"  - {pt.name}/{sname}: {desc}")
                    if slot_lines:
                        sections.append(f"[Method Slots]\n" + "\n".join(slot_lines))

            elif item in ("baselines", "baseline_profiles", "known_baselines"):
                rows = (
                    await self.session.execute(
                        select(MethodNode.name, MethodNode.description)
                        .where(MethodNode.maturity == "established_baseline")
                        .limit(30)
                    )
                ).all()
                if rows:
                    lines = [f"- {r.name}: {r.description or ''}" for r in rows]
                    sections.append(f"[Known Baselines]\n" + "\n".join(lines))

            elif item == "known_benchmarks":
                rows = (
                    await self.session.execute(
                        select(TaxonomyNode.name, TaxonomyNode.description)
                        .where(TaxonomyNode.dimension.in_(["benchmark", "dataset"]))
                        .limit(30)
                    )
                ).all()
                if rows:
                    lines = [f"- {r.name}: {r.description or ''}" for r in rows]
                    sections.append(f"[Known Benchmarks]\n" + "\n".join(lines))

            elif item == "graph_summary":
                # Count nodes by dimension
                rows = (
                    await self.session.execute(
                        select(TaxonomyNode.dimension,
                               func.count(TaxonomyNode.id).label("cnt"))
                        .group_by(TaxonomyNode.dimension)
                    )
                ).all()
                if rows:
                    lines = [f"- {r.dimension}: {r.cnt} nodes" for r in rows]
                    sections.append(f"[Graph Summary]\n" + "\n".join(lines))

            else:
                logger.debug("Unhandled domain context item: %s", item)

        return "\n\n".join(sections)

    async def _load_paper_context(self, paper_id: UUID, items: list[str]) -> str:
        """Query DB for paper-level context (sections, evidence).

        Loads L2 parse for extracted_sections (text/formulas/tables),
        and adds paper metadata header for all agents.
        """
        sections: list[str] = []

        # ── Paper metadata header (Fix 4: available to all agents) ──
        from backend.models.paper import Paper
        paper = await self.session.get(Paper, paper_id)
        if paper:
            sections.append(
                f"[Paper Metadata]\n"
                f"Title: {paper.title}\n"
                f"Venue: {paper.venue or 'N/A'} {paper.year or ''}\n"
                f"Cited by: {paper.cited_by_count or 0}\n"
                f"Acceptance: {paper.acceptance_type or 'unknown'}\n"
                f"Code: {paper.code_url or 'N/A'}\n"
                f"Category: {paper.category}\n"
                f"Tags: {', '.join(paper.tags or [])}\n"
                f"Method family: {paper.method_family or 'N/A'}"
            )

        # ── Fix 3: explicitly load L2 parse for extracted_sections ──
        from backend.models.enums import AnalysisLevel
        l2_analysis = (
            await self.session.execute(
                select(PaperAnalysis)
                .where(
                    PaperAnalysis.paper_id == paper_id,
                    PaperAnalysis.level == AnalysisLevel.L2_PARSE,
                    PaperAnalysis.is_current.is_(True),
                )
                .limit(1)
            )
        ).scalar_one_or_none()

        extracted = l2_analysis.extracted_sections if l2_analysis else {}
        if not isinstance(extracted, dict):
            extracted = {}
        # Use L2 analysis for formulas/tables/figures (these only exist on L2)
        analysis = l2_analysis

        for item in items:
            if item == "abstract":
                content = extracted.get("abstract", "")
                if content:
                    sections.append(f"[Abstract]\n{content}")

            elif item in ("introduction_excerpt",):
                content = extracted.get("introduction", "")
                if content:
                    # Excerpt: first 2000 chars
                    sections.append(f"[Introduction Excerpt]\n{content[:2000]}")

            elif item in ("method_excerpt", "method_section"):
                content = extracted.get("method", "") or extracted.get("methodology", "")
                if content:
                    sections.append(f"[Method Section]\n{content[:4000]}")

            elif item == "method_section_full":
                content = extracted.get("method", "") or extracted.get("methodology", "")
                if content:
                    sections.append(f"[Method Section (Full)]\n{content}")

            elif item in ("experiment_excerpt", "experiment_section"):
                content = extracted.get("experiments", "") or extracted.get("results", "")
                if content:
                    sections.append(f"[Experiment Section]\n{content[:4000]}")

            elif item == "ablation_section":
                content = extracted.get("ablation", "") or extracted.get("ablation_study", "")
                if content:
                    sections.append(f"[Ablation Section]\n{content}")

            elif item == "figure_table_captions":
                captions = analysis.figure_captions if analysis else None
                if captions:
                    import json
                    sections.append(
                        f"[Figure/Table Captions]\n{json.dumps(captions, ensure_ascii=False, indent=1)}"
                    )

            elif item == "result_tables":
                tables = analysis.extracted_tables if analysis else None
                if tables:
                    import json
                    sections.append(
                        f"[Result Tables]\n{json.dumps(tables, ensure_ascii=False, indent=1)}"
                    )

            elif item in ("algorithm_blocks",):
                content = extracted.get("algorithm", "") or extracted.get("algorithms", "")
                if content:
                    sections.append(f"[Algorithm Blocks]\n{content}")

            elif item in ("formula_contexts", "all_formula_contexts"):
                formulas = analysis.extracted_formulas if analysis else None
                if formulas:
                    sections.append(f"[Formulas]\n" + "\n".join(formulas))

            elif item == "mineru_markdown_excerpt":
                mineru_md = ""
                if analysis and analysis.evidence_spans:
                    mineru_md = analysis.evidence_spans.get("mineru_markdown", "") or ""
                if mineru_md:
                    sections.append(
                        "[MinerU Markdown Excerpt]\n"
                        "Use this for reading order, table/formula context, and dense method text.\n"
                        f"{mineru_md[:12000]}"
                    )

            elif item == "reference_list":
                content = extracted.get("references", "")
                if content:
                    sections.append(f"[Reference List]\n{content}")

            elif item == "citation_contexts":
                content = extracted.get("citation_contexts", "")
                if content:
                    sections.append(f"[Citation Contexts]\n{content}")

            elif item == "selected_evidence":
                evidence_rows = (
                    await self.session.execute(
                        select(EvidenceUnit.atom_type, EvidenceUnit.claim,
                               EvidenceUnit.confidence, EvidenceUnit.source_section)
                        .where(EvidenceUnit.paper_id == paper_id)
                        .limit(50)
                    )
                ).all()
                if evidence_rows:
                    lines = [
                        f"- [{e.atom_type}] {e.claim} "
                        f"(conf={e.confidence or 'N/A'}, sec={e.source_section or '?'})"
                        for e in evidence_rows
                    ]
                    sections.append(f"[Selected Evidence]\n" + "\n".join(lines))

            elif item == "figure_image_metadata":
                # Text-only figure metadata for report placement. Do not pass
                # image URLs/object keys to LLM agents.
                l2_figs = l2_analysis.extracted_figure_images if l2_analysis else None
                if l2_figs and isinstance(l2_figs, list):
                    lines = []
                    for fig in l2_figs:
                        lines.append(
                            f"- {fig.get('label', 'Unknown')} (page {fig.get('page_num', '?')}): "
                            f"role={fig.get('semantic_role', 'unknown')}, "
                            f"type={fig.get('type', 'figure')}, "
                            f"caption={fig.get('caption', '')[:120]}"
                        )
                    sections.append(f"[Available Figures ({len(l2_figs)})]\n" + "\n".join(lines))

            elif item == "lineage_positioning_context":
                parts = []
                rel_rows = (await self.session.execute(text("""
                    SELECT pr.relation_type, pr.confidence, pr.evidence,
                           pr.ref_title_raw, tp.title AS target_title,
                           tp.method_family AS target_method
                    FROM paper_relations pr
                    LEFT JOIN papers tp ON tp.id = pr.target_paper_id
                    WHERE pr.source_paper_id = :pid
                    ORDER BY pr.relation_type, pr.confidence DESC NULLS LAST
                    LIMIT 20
                """), {"pid": paper_id})).fetchall()
                if rel_rows:
                    parts.append("Paper relations already materialized:")
                    for r in rel_rows:
                        target = r.target_title or r.ref_title_raw or "unknown target"
                        method = f" / method={r.target_method}" if r.target_method else ""
                        conf = f" / conf={r.confidence}" if r.confidence is not None else ""
                        evidence = f" / evidence={(r.evidence or '')[:120]}" if r.evidence else ""
                        parts.append(f"- {r.relation_type}: {target}{method}{conf}{evidence}")

                facet_rows = (await self.session.execute(text("""
                    SELECT tn.dimension, tn.name, pf.facet_role, pf.confidence
                    FROM paper_facets pf
                    JOIN taxonomy_nodes tn ON tn.id = pf.node_id
                    WHERE pf.paper_id = :pid
                    ORDER BY tn.dimension, pf.facet_role, tn.name
                    LIMIT 40
                """), {"pid": paper_id})).fetchall()
                if facet_rows:
                    parts.append("Paper facets:")
                    for r in facet_rows:
                        parts.append(
                            f"- {r.dimension}/{r.facet_role}: {r.name}"
                            f" (conf={r.confidence})"
                        )

                method_rows = []
                if paper and paper.method_family:
                    method_rows = (await self.session.execute(text("""
                        SELECT m.id, m.name, m.type, m.maturity, m.domain,
                               m.description, parent.name AS parent_name,
                               kp.one_liner, kp.short_intro_md
                        FROM method_nodes m
                        LEFT JOIN method_nodes parent ON parent.id = m.parent_method_id
                        LEFT JOIN kb_node_profiles kp
                          ON kp.entity_type = 'method_node'
                         AND kp.entity_id = m.id
                         AND kp.lang = 'zh'
                        WHERE lower(m.name) = lower(:method)
                           OR EXISTS (
                               SELECT 1
                               FROM unnest(coalesce(m.aliases, ARRAY[]::text[])) AS a(alias_value)
                               WHERE lower(a.alias_value) = lower(:method)
                           )
                        ORDER BY m.downstream_count DESC NULLS LAST, m.updated_at DESC NULLS LAST
                        LIMIT 5
                    """), {"method": paper.method_family})).fetchall()
                if method_rows:
                    parts.append("Method node/profile matches:")
                    for r in method_rows:
                        desc = r.one_liner or r.description or r.short_intro_md or ""
                        parent = f" / parent={r.parent_name}" if r.parent_name else ""
                        parts.append(
                            f"- {r.name} ({r.type}, {r.maturity})"
                            f"{parent}: {desc[:180]}"
                        )
                elif paper and paper.method_family:
                    parts.append(
                        "Method node/profile matches: none verified; use the "
                        f"paper method_family only: {paper.method_family}"
                    )

                if parts:
                    sections.append("[Lineage Positioning Context]\n" + "\n".join(parts))

            else:
                logger.debug("Unhandled paper context item: %s", item)

        return "\n\n".join(sections)

    async def _load_run_context(
        self,
        paper_id: UUID | None,
        candidate_id: UUID | None,
        items: list[str],
        run_items: dict | None,
    ) -> str:
        """Load blackboard items or use provided run_items dict."""
        import json

        sections: list[str] = []

        # If run_items dict is provided directly, use it
        if run_items:
            for item in items:
                if item == "ALL_VERIFIED":
                    # Include all provided items
                    for key, value in run_items.items():
                        val_str = json.dumps(value, ensure_ascii=False, indent=1) if isinstance(value, (dict, list)) else str(value)
                        sections.append(f"[{key}]\n{val_str}")
                    break
                value = run_items.get(item)
                if value is not None:
                    val_str = json.dumps(value, ensure_ascii=False, indent=1) if isinstance(value, (dict, list)) else str(value)
                    sections.append(f"[{item}]\n{val_str}")
            return "\n\n".join(sections)

        # Otherwise query the blackboard
        if not paper_id and not candidate_id:
            return ""

        # Build filter conditions
        conditions = []
        if paper_id:
            conditions.append(AgentBlackboardItem.paper_id == paper_id)
        if candidate_id:
            conditions.append(AgentBlackboardItem.candidate_id == candidate_id)

        for item in items:
            if item == "ALL_VERIFIED":
                # Load all verified blackboard items
                rows = (
                    await self.session.execute(
                        select(AgentBlackboardItem.item_type,
                               AgentBlackboardItem.value_json)
                        .where(
                            *conditions,
                            AgentBlackboardItem.is_verified.is_(True),
                        )
                        .order_by(AgentBlackboardItem.created_at.desc())
                    )
                ).all()
                seen_item_types: set[str] = set()
                for r in rows:
                    if r.item_type in seen_item_types:
                        continue
                    seen_item_types.add(r.item_type)
                    val_str = json.dumps(r.value_json, ensure_ascii=False, indent=1)
                    sections.append(f"[{r.item_type}]\n{val_str}")
                break

            rows = (
                await self.session.execute(
                    select(AgentBlackboardItem.value_json)
                    .where(
                        *conditions,
                        AgentBlackboardItem.item_type == item,
                    )
                    .order_by(AgentBlackboardItem.created_at.desc())
                    .limit(1)
                )
            ).scalar_one_or_none()
            if rows is not None:
                val_str = json.dumps(rows, ensure_ascii=False, indent=1)
                sections.append(f"[{item}]\n{val_str}")

        return "\n\n".join(sections)

    def _truncate_to_budget(self, text: str, budget: int) -> str:
        """Truncate text to fit within token budget (4 chars ~ 1 token)."""
        char_limit = budget * 4
        if len(text) <= char_limit:
            return text
        logger.info(
            "Truncating context from %d to %d chars (budget=%d tokens)",
            len(text), char_limit, budget,
        )
        return text[:char_limit] + "\n\n... [truncated to fit token budget]"

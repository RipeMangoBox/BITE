# Reanalysis Comparison V2

本轮最终核验快照：

- L2 后快照：`_private/archives/2026-05-08-rf-unresolved-fixes/snapshots/verify_after_l2.json`
- 最终快照：`_private/archives/2026-05-08-rf-unresolved-fixes/snapshots/verify_final.json`
- report 重跑进度：`_private/archives/2026-05-08-rf-unresolved-fixes/snapshots/report_regen_progress.json`
- 执行日志：`_private/archives/2026-05-08-rf-unresolved-fixes/logs/`

## 1. 旧路线 vs 新路线

| Item | Old route behavior | V2 behavior verified in this run |
|------|--------------------|----------------------------------|
| Runtime env | `.venv`/host env 混用 | 构建并使用 conda env `RF`，`PYTHONNOUSERSITE=1` |
| DB URL | 容易误用容器 hostname `postgres` | 显式使用 `127.0.0.1:5432/researchflow` |
| Image to LLM | 有 API key 时 VLM figure/formula/table 可能上传图片 | 默认 `ALLOW_LLM_IMAGE_UPLOAD=false`；图片不传给 DeepSeek/LLM agent |
| Parse source | PyMuPDF/TeX first，MinerU 可选或后处理 | 5 篇 L2 重新执行并强制尝试 MinerU；最终 L2 回灌离线 MinerU markdown/tables/formulas/figures |
| Analysis context | deep/report 可能看不到 MinerU reading order/table/formula | context 已包含 MinerU markdown excerpt；figure context 仅传文字 metadata |
| Report structure | 历史 report section 叠加，查询容易混入旧版本 | 5 篇 current report 均为 version 3，且每篇只有一个 current report |
| Part II / core innovation | 方法概述与直觉冗余，常像贡献列表 | writer prompt 强制 `核心创新` 为 causal knob；`整体框架` 只讲 skeleton |
| Top insight | 旧 exporter 直接用 DeltaCard delta statement，偏 TL;DR | exporter 优先用 current `core_innovation` 第一因果句生成顶部 `核心洞察` |
| Figure export | legacy no-marker report 可能末尾堆图 | 每页当前内联 3 个 MinerU 图表资产，无未解析 `{{FIG/TBL}}` marker |

## 2. Five-paper final state

| Paper | Formulas | Tables | Figure rows | parsers_used | formula_source | Report current version | Report sections | Export path |
|-------|----------|--------|-------------|--------------|----------------|------------------------|-----------------|-------------|
| AIREAI | 11 | 15 | 22 | pymupdf, arxiv_tex, mineru | mineru | 3 | 7 | `paper/ICLR_2025/P__自适应迭代推理视频帧选择_AIREAI.md` |
| 3DGEER | 64 | 16 | 12 | pymupdf, arxiv_tex, mineru | mineru | 3 | 7 | `paper/ICLR_2025/P__通用相机精确高效3D高斯渲染_GRMEEG.md` |
| ADEPT | 45 | 27 | 36 | pymupdf, mineru | mineru | 3 | 7 | `paper/Unknown_Unknown/P__持续预训练的自适应扩展与解耦调优_ACPAED.md` |
| ACE | 30 | 19 | 25 | pymupdf, mineru | mineru | 3 | 7 | `paper/Unknown_Unknown/P__多跳知识编辑的归因控制Q-V路径_AACKEM.md` |
| AC-Sampler | 80 | 27 | 33 | pymupdf, mineru | mineru | 3 | 7 | `paper/Unknown_Unknown/P__扩散采样的加速与校正_AACDSM.md` |

Notes:

- Direct L2 rerun first produced TeX as formula source for AIREAI/3DGEER where arXiv TeX existed. The final state intentionally uses offline MinerU bridge output for all 5 so tables/formulas/figure assets are traceably aligned to the same MinerU source.
- `llm_image_upload_enabled=false` for all 5 current L2 rows.
- Current reports all have section sequence: `metadata_overview`, `background_motivation`, `core_innovation`, `framework_overview`, `module_formulas`, `experiment_analysis`, `lineage_positioning`.

## 3. Part II / report content changes

Each `core_innovation` now starts with a method-level causal sentence rather than a result-only TL;DR:

- AIREAI: 将 VLM 深度语义分析嵌入轻量迭代循环，而不是一次性处理所有帧。
- 3DGEER: 用精确投影积分替代局部仿射近似，以处理宽视场投影非线性。
- ADEPT: 利用层/单元重要性差异，只扩展和快速适配低重要性部分。
- ACE: 将多跳事实回忆建模为跨层 Q-V neuron path，而不是单点记忆读取。
- AC-Sampler: 在中间扩散时间步估计 density ratio 并写入 MH 接受概率。

`framework_overview` 与 `core_innovation` 的职责已经分开：前者讲 pipeline skeleton，后者讲 decisive causal knob。

## 4. Export verification

Checked pages:

- `researchflow-backend/exports/obsidian-vault/paper/ICLR_2025/P__自适应迭代推理视频帧选择_AIREAI.md`
- `researchflow-backend/exports/obsidian-vault/paper/ICLR_2025/P__通用相机精确高效3D高斯渲染_GRMEEG.md`
- `researchflow-backend/exports/obsidian-vault/paper/Unknown_Unknown/P__持续预训练的自适应扩展与解耦调优_ACPAED.md`
- `researchflow-backend/exports/obsidian-vault/paper/Unknown_Unknown/P__多跳知识编辑的归因控制Q-V路径_AACKEM.md`
- `researchflow-backend/exports/obsidian-vault/paper/Unknown_Unknown/P__扩散采样的加速与校正_AACDSM.md`

Results:

- All 5 files exist after final export.
- All 5 pages contain top `> [!tip] 核心洞察` from current `core_innovation`, not raw DeltaCard.
- All 5 pages have 3 inline MinerU figure/table assets under `assets/figures/papers/<paper_id>/figures/...`.
- No checked page has unresolved `{{FIG:...}}` / `{{TBL:...}}` marker.

## 5. 尚未解决的问题

- Full 2-agent architecture is not complete; current code still contains old semantic agents.
- MinerU figure asset integration is still script-mediated for this 5-paper run (`bridge_mineru_local_outputs.py`), not yet fully inside generic `parse_service.py`.
- `paper_report_sections` history is preserved intentionally. Callers must filter `paper_reports.review_status='current'`; known exporter/comparison paths have been fixed, but remaining ad hoc queries may still need review.
- Final L2 formula source is `mineru` even when TeX is available for AIREAI/3DGEER. This was chosen for source alignment in this run, but future generic policy should prefer TeX for exact formulas while still preserving MinerU formula context separately.

# v4 分析链找回与最小优化记录

记录时间：2026-06-28

## Git 定位

当前仓库没有 `v4` tag 或 branch。通过 `git reflog --date=iso` 找到旧工作线：

- `0d020a9`：`Initial BITE ripemangobox workspace`，保留 v4 质量基线候选脚本。
- `63d5c49`：`Add structured main analysis context mode`，在 v4 基线上加入 structured main context。
- `45cb761`：`P1 main-context A/B: structured mode, prompt-cache contracts, low-value chunk filter`，加入 overlap 350、reference/acknowledgement 低价值 chunk 本地化、writer/figure prompt-cache contract。

本次采用策略：以 `0d020a9` 的输出风格为基线，只保留不改变 note 结构的必要修复和 token 优化。

## 本次保留

- 保留 v4 的四段 section writer 输出形态。
- 保留 `main_context_chars = 36_000`。
- 默认 `main_context_mode = structured`，但不是压到 12K；而是在 36K 预算内按结构抽正文。
- structured main context 会排除 `references`、`bibliography`、`acknowledgement(s)`、`appendix`、`supplementary` 标题段。
- 保留 `overlap_chars = 350`，降低 chunk overlap 重复输入。
- 保留 `references`、`acknowledgement(s)`、纯引文 chunk 的本地零成本抽取。
- 保留 appendix figure/table chunk 的本地锚点抽取。

## 本次回退/不默认启用

- 不默认使用 v05/P1 的 12K main context。
- 不改变 36K main context 预算。
- 不保留 writer/figure 的新增 prompt-cache contract 前缀，避免改变 v4 section writer 和 figure placement 的输入风格。
- 不把 P2 变体作为默认链路。

## 关于 reference/acknowledgement 低价值 chunk 本地化

作用位置：`scripts/run_local_paper_analysis.py::run_part_analysis`。

它只影响 part 阶段。`split_markdown` 切出的 chunk 如果被 `is_low_value_citation_chunk` 判定为 reference、acknowledgement 或纯引文块，就不调用 LLM，而是调用 `local_anchor_part_analysis` 生成一个零成本锚点 JSON，并清空 method/experiment/formula/figure evidence。这样 main 和 writer 不会把参考文献条目当作论文贡献证据。

这类内容不会明显出现在最终 v4 分析结果中是正常的：它的目标是减少无效输入和防止污染，而不是把 reference/acknowledgement 写进 note。

## 验证

- `python3 -m py_compile scripts/run_local_paper_analysis.py` 通过。
- `PYTHONPATH=platform conda run -n BITE python -m pytest tests/test_run_local_paper_analysis_export.py -q` 通过：32 passed。

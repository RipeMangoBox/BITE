# BITE v06 最新分析链说明

- created: 2026-07-03
- status: current-local-analysis-chain
- scope: `obsidian-vault/analysis/*/*.md` 顶层 paper notes
- primary implementation: `scripts/run_local_paper_analysis.py`
- public reference: `docs/formal-analysis-chain.md`

## 版本边界

从文件修改时间和正文结构看，`2026-06-25` 起主流输出切换到当前四段式正式分析链。`2026-06-24` 是混排过渡日，不宜直接并入旧链或新链。

本次审计口径：

- 顶层 paper note 总数：5291
- `2026-06-24` 前旧 note：3322
- `2026-06-24` 后新 note：约 1969
- 子目录中的 MinerU parse/report 中间文件不作为最终 note 修复对象

## 当前正式链

正式 runner 支持 PDF、已有 MinerU 输出目录或 Markdown 源输入，默认链路是：

```text
PDF / MinerU parse
  -> Markdown chunking
  -> chunk-level anchor extraction
  -> main analysis JSON
  -> section writers
  -> figure/table visual summary and placement
  -> vault export
  -> deterministic validation
```

当前 canonical note 结构：

- YAML frontmatter
- H1 paper title
- `> [!tip] 核心洞察`
- 元数据表，含 `Links`
- `> [!tip] 效果简介`
- `## 概要`
- `## 核心方法与创新机理`
- `## 实验与关键发现`
- `## 定位与知识库关联`
- `## 原文 PDF`
- `![[paperPDFs/...]]`

当前 canonical frontmatter：

- 必备字段：`title`, `type`, `paper_level`, `venue`, `year`, `pdf_ref`, `project_link`, `code_link`, `aliases`, `tags`, `core_operator`, `primary_logic`, `claims`
- `project_link` / `code_link` 缺值时写 `null`，不省略字段
- `pdf_ref` 使用相对 vault 路径，例如 `paperPDFs/CVPR_2026/Title.pdf`
- 不再使用旧链中的 `created` / `updated`

当前 embed 规则：

- PDF embed：`![[paperPDFs/...]]`
- figure/table embed：`![[assets/figures/papers/...]]`
- 默认目标是最多 6 个核心图表，避免旧链的 11-12 图表堆叠
- 图表应服务于核心方法、主结果、关键消融或代表性定性对比

代表样本：

- `obsidian-vault/analysis/SIGGRAPH_2026/CasLayout_Cascaded_3D_Layout_Diffusion_for_Indoor_Scene_Synthesis_with_Implicit_Relation_Modeling.md`
- `obsidian-vault/analysis/SIGGRAPH_ASIA_2022/Efficient_Drone_Exploration_in_Real_Unknown_Environments.md`

## 旧链差异

旧链主流正文是七段式：

- `## 概述`
- `## 背景与动机`
- `## 核心创新`
- `## 整体框架`
- `## 核心模块与公式推导`
- `## 实验与分析`
- `## 方法谱系与知识库定位`
- `## 原文 PDF`

旧链常见迁移问题：

- `Links` 行同时出现 `paper` 和 `arXiv`，且二者 URL 经常不一致
- 使用 `[arXiv](...)` 作为显示标签；当前约定统一显示为 `[paper](...)`
- 图表数量模板化偏多，中位数约 11，新链中位数约 6
- table 过密，大量补充实验表直接贴入顶层 note
- 英文原 caption 过长，常见 `Figure N:` / `Table N:` 原文直贴
- 少量旧 note 存在旧式 PDF 前缀、`Local Reading`、`TL;DR` 等历史模板残留

旧链样本：

- `obsidian-vault/analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions.md`
- `obsidian-vault/analysis/CVPR_2024/DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance.md`

## 本次自动修复

新增脚本：

- `scripts/paper_analysis_maintenance/modernize_analysis_notes.py`

修复规则：

- 只处理顶层 `obsidian-vault/analysis/*/*.md`
- 优先用 `obsidian-vault/paper_list.csv` 的 `paper_link` 重写 `Links` 行里的 paper URL
- 删除 `Links` 行中的 `arXiv` 显示项，保留统一 `[paper](...)`
- 去重 paper/arXiv URL 共存问题
- 将图表 embed 上限收敛到 6 个
- 对 `2026-06-24` 前旧 note 压缩过长 caption 到 360 字符以内
- 对全库补充清理时只修 Links 和超 6 图表，不继续改写新链 caption

执行报告：

- dry-run 旧 note：`_private/BITE_versions/v06/modernize_analysis_notes_2026-07-03_150455.md`
- write 旧 note：`_private/BITE_versions/v06/modernize_analysis_notes_2026-07-03_150521.md`
- dry-run 全量保守补丁：`_private/BITE_versions/v06/modernize_analysis_notes_2026-07-03_150623.md`
- write 全量保守补丁：`_private/BITE_versions/v06/modernize_analysis_notes_2026-07-03_150642.md`
- final dry-run：`_private/BITE_versions/v06/modernize_analysis_notes_2026-07-03_150841.md`

最终结构验证：

- 顶层 note：5291
- image embed 数量：min 0 / p50 6 / p90 6 / max 6
- `[arXiv](...)` 标签残留：0
- `Links` 行中 `[paper]` 与 `[arXiv]` 共存：0
- 脚本 final dry-run changed：0

仍需 LLM/人工处理的问题：

- 仍有部分新链 note 的英文原 caption 较长；这类属于语义压缩，不适合在没有逐篇判断时全库脚本改写
- 若要进一步提升阅读质量，建议按 batch 让 LLM 只做 caption 中文短标签化和重复解释合并，不改论文事实

## HF 私有仓库同步

新增脚本：

- `scripts/upload_bite_hf_private.py`

建议创建私有 Hugging Face dataset repo，而不是 model repo。上传对象：

- `obsidian-vault/analysis/`
- `obsidian-vault/assets/`
- `obsidian-vault/paper_list.csv`

当前本机 HF token 已失效，`hf auth whoami` 返回 invalid token，因此本次未创建远端仓库、未上传数据。

重新登录后可执行：

```bash
hf auth login
python3 scripts/upload_bite_hf_private.py \
  --repo-id <org-or-user>/<private-dataset-name>
```

脚本默认 `private=True`，会创建/更新 dataset repo，并用 `upload_large_folder` 只上传 `analysis/**`、`assets/**` 和 `paper_list.csv`。

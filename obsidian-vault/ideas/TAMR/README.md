# TAMR 项目索引

> Temporal-Aware Motion-text Retrieval

## 当前状态

**Phase 1 待启动**：MotionPatches 主线仍用 `pos66 + DistilBERT` 验证核心假设（structured matching > global matching）。
`vanilla TMR + HumanML3D-E-MP` 的 6-way motion rep eval 已完成：`kimodo261` 最强，`pos66 / hml272 / hy201` 为第二梯队，`smpl135` 已淘汰。

如果当前问题改成“要不要继续把 MotionPatches 当 temporal-semantic evaluator”，最新收敛结论见：

- [2026-04-28_tamr-core-materials-and-temporal-semantic-evaluator-review.md](/data/Life%20Me/ResearchWY%20Vault/paperIDEAs/TAMR/2026-04-28_tamr-core-materials-and-temporal-semantic-evaluator-review.md)
  当前明确结论：`AToM > ChroAccRet > MG-MotionLLM > ZOMG`；没有单一开源低成本候选能完整替代 MotionPatches。

## 文件导航

| 文件 | 作用 | 状态 |
|------|------|------|
| `2026-04-28_tamr-core-materials-and-temporal-semantic-evaluator-review.md` | 当前问题的收拢结论：核心材料、候选 evaluator、推荐顺序 | 🟢 活跃 |
| `ROADMAP.md` | 唯一活跃路线图（Phase 0→3 + smoke gate） | 🟢 活跃 |
| `EXPERIMENTS.md` | 所有实验记录与结论 | 🟢 活跃 |
| `METRICS.md` | 指标释义、公式、协议口径统一说明 | 🟢 活跃 |
| `2026-04-20_时序数据集盘点与TAMR子模块化转向.md` | TAMR pivot / temporal 资产替代判断的主笔记 | 🟢 活跃 |
| `2026-04-21_vanilla_tmr_humanml3de_mp_motion_rep_eval_summary.md` | 6 种 motion rep 在 vanilla TMR / HumanML3D-E-MP 下的统一 eval + 总结 | 🟢 活跃 |
| `2026-04-19_roadmap-existing-experiment-verification.md` | 最新路线与已有实验的核对结论 | 🟢 活跃 |
| `2026-04-19_ripemangobox_roadmap.md` | 个人思路原稿（Data/Pipeline/Training 三层 + 事前验尸） | 🟢 活跃 |

## archived/ 分类

| 目录 | 内容 | 文件数 |
|------|------|-----:|
| `roadmap_history/` | 历史 roadmap、架构设计、phase 规划、experiment spec | 8 |
| `eval_results/` | 各阶段 eval 闭环总结（Stage 1→4.1 + fair baseline + REF00） | 7 |
| `motion_repr_text_encoder/` | motion repr 消融 + text encoder 探针 + ClipModel prompt（⚠️ 非 MP 原生架构） | 3 |
| `temporal_alignment/` | TMR 机制探针 D0-D2b 设计与结果 | 9 |
| `execution_plans/` | 已完成/弃用的执行 prompt | 2 |

详细索引见 `archived/README.md`。

## 关键数字速查

| 指标 | 值 | 来源 |
|------|------|------|
| plain00_s42 PrimaryScore | 43.8275 | fair anchor |
| S2E-v2 fair PrimaryScore | 44.4487 | 当前最强 global event-aware |
| R1 smoke gate | >44.5 或 K>=2 子集 CAR/TAR >+3pp | ROADMAP.md |
| K=1 样本占比 | ~50.7% | HumanML3D-E 数据统计 |

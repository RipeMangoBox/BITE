---
updated: 2026-04-19
title: TAMR Archived Notes Index
---
# TAMR Archived Notes

已归档文档按作用分为 5 类。根目录的 `ROADMAP.md` / `EXPERIMENTS.md` / `2026-04-19_ripemangobox_roadmap.md` 是当前活跃文档，本目录只保留历史证据与参考资料。

## 目录结构

```
archived/
├── motion_repr_text_encoder/   # Motion repr 消融 + text encoder 探针（⚠️ 非 MP 原生架构）
├── roadmap_history/            # 旧 roadmap、phase 设计、hybrid plan、architecture QA
├── eval_results/               # 各阶段实验闭环总结
├── execution_plans/            # 执行 prompt / session 交接文档
└── temporal_alignment/         # TMR 机制探针（D0-D2b）设计与结果
```

---
## motion_repr_text_encoder/

> ⚠️ 本目录所有实验均基于 `MotionReprBaseline`（2 层轻量 Transformer，~9MB checkpoint），**非 MotionPatches 原生 ClipModel 架构**，结论不可直接迁移。

| 文件 | 内容 |
|------|------|
| `2026-04-18_motion-repr-ablation-summary.md` | 5 种 motion repr 消融结果（kimodo_like_261 / pos66 / guo263 / hy201_recon / smpl_d135_recon） |
| `phase0.5_motion_repr_clipmodel.md` | Phase 0.5 任务 prompt：在完整 ClipModel 下训练非 pos66 表示（**已降低优先级**，等 R1 有正信号后再做） |

---
## roadmap_history/

历史 roadmap 与设计文档，按时间顺序记录了从 Phase 1 到 Pivot 的演化。当前活跃 roadmap 已外提为根目录 `ROADMAP.md`。

| 文件 | 内容 | 状态 |
|------|------|------|
| `2026-04-05_tamr-motionpatches-harness-design.md` | TAMR 总纲与 canonical design（Phase 1 框架基础） | 历史参考 |
| `2026-04-06_tamr-v3-event-abstraction-centered-design.md` | 高层 stepwise roadmap，阶段切分与主线约束 | 历史参考 |
| `2026-04-11_tamr-architecture-qa.md` | 关键架构疑问与解答（backbone 定义、head 作用等） | 历史参考 |
| `2026-04-11_tamr-roadmap-phase1-vs-phase2.md` | Phase 1（TMR 机制验证）vs Phase 2（MP 正式实验）的 roadmap | 历史参考 |
| `2026-04-13_tamr-phase2b-hybrid-plan.md` | Phase 2b Hybrid Strategy（Event CLIP + Temporal Grounding） | 已完成，结论并入 EXPERIMENTS.md |
| `2026-04-15_tamr-experiment-spec.yaml` | 实验规格 YAML（Phase 2b 时期） | 历史参考 |
| `2026-04-15_tamr-status-and-roadmap.md` | TAMR 现状全景 & ICLR Roadmap（含详细根因分析） | **核心参考**，被 pivot-roadmap 取代但根因分析仍有价值 |
| `2026-04-17_tamr-pivot-roadmap.md` | Pivot Roadmap（Event-Grounded Fine-Grained Matching）— 已外提为根目录 `ROADMAP.md` | 同步副本 |

---
## eval_results/

各阶段实验的闭环总结，与实际 checkpoint / metric artifact 对应。

| 文件 | 内容 |
|------|------|
| `2026-04-06_tamr-motionpatches-stage1-closure-summary.md` | Stage 1 闭环 |
| `2026-04-09_tamr-motionpatches-stage2-closure-summary.md` | Stage 2 闭环 |
| `2026-04-10_tamr-motionpatches-stage4-first-pass-eval-summary.md` | Stage 4 首轮评测 |
| `2026-04-11_tamr-stage4-1-closure-summary.md` | Stage 4.1 闭环（D2b winner，Go Phase 2） |
| `2026-04-17_tamr-fair-baseline-eval-summary.md` | Fair baseline 评测（REF00 4-seed） |
| `ref00_two_seed_eval_summary_2026-04-15.md` | REF00 2-seed 评测（seed 方差参考） |
| `ref00_extended_eval_summary_2026-04-15.md` | REF00 扩展评测（legacy 口径，仅供方差审计） |

---
## execution_plans/

执行 prompt 与 session 交接文档，用于跨 session 恢复上下文。

| 文件 | 内容 |
|------|------|
| `2026-04-17_motion-repr-exploration.md` | Motion repr 探索 session prompt |
| `2026-04-18_motion-repr-ablation_next-session-prompt.md` | Motion repr 消融下一 session 交接 prompt |

---
## temporal_alignment/

TMR 机制探针（D0-D2b）的设计文档与实验结果，对应 `EXPERIMENTS.md` Section 1。

| 文件 | 内容 |
|------|------|
| `2026-04-10_temporal-alignment-scheme-evolution.md` | Stage 4.1 从 alignment-first 到 V4 narrow scope 的收敛总结 |
| `2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v3.md` | BASMA+ full blueprint（保留作完整机制假设） |
| `2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v4-narrow-scope-execution.md` | Stage 4.1 唯一执行稿 |
| `2026-04-11_tamr-stage4-1-d0-humanml3de-event-statistics-result.md` | D0 数据统计结果 |
| `2026-04-11_tamr-stage4-1-d1-frozen-minimal-head-execution.md` | D1 实现记录 |
| `2026-04-11_tamr-stage4-1-d1-evaluation.md` | D1 frozen head 评测 |
| `2026-04-11_tamr-stage4-1-d1.5-evaluation.md` | D1.5 uniform pooling 控制实验 |
| `2026-04-11_tamr-stage4-1-d2a-evaluation.md` | D2a partial unfreeze 评测 |
| `2026-04-11_tamr-stage4-1-d2b-evaluation.md` | D2b full unfreeze 评测（Stage 4.1 winner） |

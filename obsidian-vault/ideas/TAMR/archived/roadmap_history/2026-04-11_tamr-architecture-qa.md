---
created: 2026-04-11
updated: 2026-04-11
status: living-doc
title: TAMR 架构与实验 QA
tags:
  - tamr
  - qa
  - architecture
  - motionpatches
  - tmr
---
# TAMR 架构与实验 QA

本文档记录项目推进过程中产生的关键疑问与解答，防止后续重复困惑。

---
## Q1. 为什么 D2a 要对 TMR 的 motion encoder 做解冻测试？我们不是基于 MotionPatches 的表征吗？

**背景：** TAMR v3 roadmap 选定 MotionPatches 作为最终 backbone，但 Stage4.1 的 D0→D2 实验链全部跑在 TMR 原始的 ACTOR-style encoder 上。

**回答：**

1. 当前代码库里只有一个 motion encoder——TMR 的 `ACTORStyleEncoder`（`src/model/actor.py`）。它接收 263-dim guoh3d motion features，通过 Transformer encoder 输出 256-dim latent。D1/D2a 里冻结和解冻的都是这个 encoder。

2. MotionPatches 在当前实验路径里**没有被直接用作 motion encoder**。它的角色是：
   - 上游设计灵感来源（`14 × 5` patch token grid 提供天然时空结构）
   - 后续 backbone 升级的目标

3. D1→D2 的实验目的不是"调出最终模型"，而是回答一个诊断性问题：
   > "event-level temporal alignment loss 作为 auxiliary signal，能否通过梯度回传改善 shared encoder 的表征质量，而不伤害 global retrieval？"

4. 这个问题和具体用哪个 backbone 无关。如果在 TMR ACTOR encoder 上验证了"partial unfreeze + minimal event head 有正信号"，那后续切换到 MotionPatches backbone 时，同样的策略大概率也能 work——而且 MotionPatches 的 patch token 结构天然更适合 event-time alignment。

**结论：** 当前不存在"两种 motion encoder 同时工作"的情况。只有 TMR 的 ACTOR encoder 在跑，MotionPatches 是后续升级路径。参见 roadmap 文档的 Phase 划分。

---
## Q2. Backbone 具体指哪个部分？添加的 head 是什么，作用是什么？

**Backbone（D1/D2 中冻结或部分解冻的部分）：**

| 模块 | 类 | 作用 | D1 状态 | D2a 状态 |
|---|---|---|---|---|
| `motion_encoder` | `ACTORStyleEncoder` | motion 序列 → 256-dim latent + temporal hidden states | 全冻结 | last-2 blocks 解冻 |
| `text_encoder` | `TextToEmb` + `ACTORStyleEncoder` | 文本 tokens → 256-dim latent | 全冻结 | 全冻结 |
| `motion_decoder` | `ACTORStyleDecoder` | VAE 解码器，D1/D2 不使用 | 全冻结 | 全冻结 |

**添加的 Head（始终可训练）：**

| 模块 | 定义 | 作用 |
|---|---|---|
| `event_proj_t` | `nn.Linear(256, 128)` | 把 motion encoder 的 temporal hidden states 投影到 128-dim 对齐空间 |
| `event_proj_e` | `nn.Linear(256, 128)` | 把 text encoder 的 event latent 投影到同一个 128-dim 对齐空间 |

**工作流程：**

1. frozen/partial-unfrozen motion encoder 输出：global latent（用于检索）+ temporal hidden states `[B, T, 256]`
2. frozen text encoder 对每条 event text 编码出 event latent `[N_events, 256]`
3. `event_proj_t` 和 `event_proj_e` 投影到 128-dim
4. 在投影空间里，用 event latent 对 temporal hidden states 做 attention pooling
5. masked InfoNCE 对比学习：正例 = 同一 event 的 text-motion pair，负例 = 跨样本 event

---
## Q3. Stage4 首轮 No-Go 和 D2a Go 的区别是什么？

| 维度 | Stage4 首轮 | D2a |
|---|---|---|
| 解冻范围 | 全部 motion encoder | 仅 last-2 Transformer blocks |
| auxiliary branch | 重型 temporal adapter（多个 loss + adapter 模块） | minimal event head（2 个线性层 + 1 个 masked InfoNCE） |
| 结果 | 主表征退化（EVT-nsim TAR01: 33→23） | 主表征显著提升（normal t2m R@1: 9.46→13.51） |
| 根因 | 解冻范围过大 + auxiliary branch 过重 → 表示漂移 | 解冻范围受控 + auxiliary 极简 → 梯度信号有益 |

**结论：** 问题不在"解冻 backbone"本身，而在"解冻范围 × auxiliary 复杂度"的组合。

---
## Q4. HumanML3D-E 的 nsim 评测是怎么做的？

原始 HumanML3D-E 没有独立的 `nsim_test` split。当前做法是从 test set 内按文本相似度筛选 100 条构成 nsim-like hard subset。

注意事项：
- `len=148`（normal）和 `len=100`（nsim-like）的 R@K 不可与完整 HumanML3D `len=4384` 直接横向比较
- D1/D1.5/D2a/D2b 之间的纵向比较是有效的，因为用的是同一个 subset

---
## Q5. D1.5 的 retrieval 指标为什么和 D1 完全一致？

因为 D1 和 D1.5 都是 frozen backbone，`retrieval.py` 走的是 global text/motion latent，event head 不参与推理。两者的区别只在 event pooling 方式（attention vs uniform），这只影响 `val_evt_align_acc`，不影响 retrieval。

D2 是第一个有可能改变（也有可能伤害）retrieval 指标的实验。

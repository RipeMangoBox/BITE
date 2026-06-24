---
created: 2026-04-11
updated: 2026-04-11
status: living-doc
title: TAMR Roadmap — TMR 验证阶段 vs MotionPatches 正式阶段
tags:
  - tamr
  - roadmap
  - motionpatches
  - tmr
  - backbone-migration
---
# TAMR Roadmap

## 核心原则

TAMR 项目分为两个 Phase，使用不同的 backbone。Phase 1 已闭环，当前准备进入 Phase 2。

- Phase 1 的所有实验结论是**机制验证**，不是最终数值
- Phase 2 的 backbone 切换是独立工程任务，不改变已验证的机制设计
- 两个 Phase 之间不应产生指标混淆

---
## Phase 1: TMR ACTOR Encoder 上的机制验证（当前）

**Backbone:** TMR `ACTORStyleEncoder`（263-dim guoh3d features → 256-dim latent）

**目标:** 用最简单的 backbone 验证 temporal alignment 机制的可行性，回答以下问题：

1. ✅ frozen feature 中是否存在 event-time signal？（D1: Yes）
2. ✅ attention pooling 是否比 uniform pooling 有实质增益？（D1.5: Yes, +22.82pp）
3. ✅ partial unfreeze 是否能改善主表征而不退化？（D2a: Yes, retrieval 显著提升）
4. ✅ 全解冻是否优于 partial unfreeze？（D2b: Yes, 全面优于 D2a，无退化）
5. ✅ Stage4.1 闭环总结（D3: 完成，winner = D2b，Go Phase 2）

**Phase 1 产出:**
- 已验证的机制：minimal event-time head + masked InfoNCE + full motion encoder unfreeze（D2b winner）
- 已验证的训练策略：warm-start from pretrained → D1 frozen head → D2b full unfreeze
- 已验证的评测体系：normal / nsim-like / guo / threshold_0.95
- 可迁移的代码模块：`tmr_d1.py`, `tmr_d2a.py`, `tmr_d2b.py`, `humanml3de_event.py`, `collate.py`
- 闭环总结：`eval_summary/2026-04-11_tamr-stage4-1-closure-summary.md`

**Phase 1 不产出:**
- 最终论文数值（test set 太小，backbone 不是最终版）
- 与其他方法的正式对比（需要在同一 backbone 上做）

---
## Phase 2: MotionPatches Backbone 上的正式实验（后续）

**Backbone:** MotionPatches（`14 × 5` patch token grid，每个 patch 有明确的时间位置和身体部位语义）

**前置条件:**
- Phase 1 的 D3 闭环完成，机制可行性确认
- MotionPatches 的 motion encoder 接入 TAMR 训练框架
- HumanML3D-E 的 motion features 转换为 MotionPatches 输入格式

**切换时需要改的:**

| 组件 | Phase 1（当前） | Phase 2（目标） |
|---|---|---|
| motion encoder | `ACTORStyleEncoder` | MotionPatches ViT encoder |
| motion input | 263-dim guoh3d features | patch tokens from `14 × 5` grid |
| temporal hidden states | Transformer encoder 中间层输出 `[B, T, 256]` | patch token 序列 `[B, 14, 5, D]` 或 `[B, 70, D]` |
| `event_proj_t` input dim | 256 | MotionPatches latent dim |
| text encoder | TMR `TextToEmb` + ACTOR | 可沿用或升级 |
| 评测 test set | HumanML3D-E (148 samples) | 完整 HumanML3D (4384 samples) |

**切换时不需要改的:**
- masked InfoNCE 的 loss 定义和 mask 策略
- event text 解析逻辑（`parse_decomposed_events`）
- collate 逻辑（`collate_text_motion_event`）
- partial unfreeze 策略（last-N blocks）
- 评测 protocol 定义（normal / nsim / guo / threshold）

**Phase 2 的关键风险:**
- MotionPatches 的 patch token 维度和语义与 ACTOR hidden states 不同，`event_proj_t` 可能需要重新调参
- MotionPatches 的 `14 × 5` grid 天然有 patch-level 空间结构，Phase 1 没有利用这个结构（因为 ACTOR 没有），Phase 2 可以引入 patch support 机制（V3 BASMA+ 的设计在此时才真正适用）
- 完整 HumanML3D test set 上的 retrieval 数值会与 Phase 1 不可比

---
## 阶段关系图

```
Phase 1 (当前)                          Phase 2 (后续)
TMR ACTOR encoder                       MotionPatches encoder
HumanML3D-E (small)                     HumanML3D (full)
                                        
Stage 0-2: event contrastive ──────────► 沿用
Stage 4.1:                              
  D0: 数据统计 ✅                        
  D1: frozen head ✅ ──────────────────► 迁移 event head 到 MP
  D1.5: uniform control ✅              
  D2a: partial unfreeze ✅ ────────────► 迁移 partial unfreeze 策略
  D2b: full unfreeze ⬜                 
  D3: 闭环总结 ⬜ ─────────────────────► Phase 2 启动门
                                        
                                        Step 5: evidence head (在 MP 上做)
                                        Step 6: 正式对比实验
                                        Step 7: 论文写作
```

---
## 防混淆规则

1. **不要用 Phase 1 的 R@K 数值与任何已发表方法对比。** Phase 1 的 test set 只有 148 条，R@K 数值不可比。
2. **不要把 Phase 1 的 ACTOR encoder 结论直接写进论文的 method section。** 论文的 method 应该描述 Phase 2 的 MotionPatches 架构。Phase 1 的结论可以放在 ablation / pilot study 里。
3. **Phase 2 启动时，所有实验从 MotionPatches pretrained weights 重新 warm-start。** 不要从 Phase 1 的 ACTOR weights 继续训练。
4. **Phase 1 的代码模块（`tmr_d1.py` 等）在 Phase 2 中应该被重构为通用版本**，而不是同时维护两套。

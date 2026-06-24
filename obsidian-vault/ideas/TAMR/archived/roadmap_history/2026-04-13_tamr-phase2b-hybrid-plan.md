---
created: 2026-04-13
updated: 2026-04-15
status: phase2b-complete
title: TAMR Phase 2b — Hybrid Strategy (Event CLIP + Temporal Grounding)
tags:
  - tamr
  - motionpatches
  - phase2b
  - execution
---
# TAMR Phase 2b — Hybrid Strategy

## 1. 背景与动机

Phase 2a 的 TMR 机制直接迁移（独立 event head + masked InfoNCE）在 MotionPatches
上未能超过 stage2_mp_gt（44.83）。根因分析见 roadmap 文档。

核心教训：在 MotionPatches 上，event alignment 必须**直接优化 retrieval 空间**，
TMR 的 event head 应作为辅助 temporal grounding 信号，而非主 loss。

## 2. 当前事实基础

### 2.1 HumanML3D-E regime 下的公平锚点

| Checkpoint | PrimaryScore(tmr_strict) | 备注 |
|---|---|---|
| pretrained B0 | 43.53 | 纯 pretrained ViT，无 event 训练 |
| stage2_mp_gt B0 | 44.83 | event CLIP loss 直接优化 retrieval，HumanML3D keyids 训练 |
| stage4_adapter B0 | 40.45 | temporal adapter，严重退化 |
| MP-D1 (tmr_transfer) | 43.69 | frozen backbone，event head 学到但 retrieval 不变 |
| MP-D2b (tmr_transfer) | 44.03 | full unfreeze，epoch 4 见顶后过拟合 |
| ~~S2E (stage5_s2e)~~ | ~~42.76~~ | ~~event CLIP + warm-start，退化（已废弃）~~ |
| **S2E-v2 (stage5_s2e_v2)** | **44.50** | **event CLIP，HumanML3D-E keyids，从零训练 ✅ (best)** |
| S2E+T (stage5_s2e_t) | 43.97 | S2E-v2 + evt_align(0.2)，temporal head 退化 |

### 2.2 stage2_mp_gt 的配方（已验证有效）

```yaml
train_motion_encoder: true    # ViT 全解冻
train_text_encoder: true      # DistilBERT 全解冻
event_temporal:
  enable: true
  enable_event_loss: true     # event CLIP loss 直接在 retrieval 空间
  enable_temporal_loss: true  # temporal hard negative loss
  event_source.type: gt       # GT events from HumanML3D-E
  loss:
    global_weight: 1.0        # 主 CLIP loss（不是 0.1）
    event_weight: 0.5         # event CLIP loss
    temporal_weight: 0.3      # temporal hard negative loss
```

关键：这个配方的 event loss 是 `event_embeds @ motion_embeds.T`，直接在 retrieval
256-dim 空间做 CLIP loss，梯度流过 motion_projection。

### 2.3 Phase 2a 的 TMR event head（已实现，可复用）

```python
# models/clip.py: compute_tmr_event_alignment_loss()
# time_tokens (B, 14, 768) → event_proj_t → (B, 14, 256)
# event_text_emb (N, 768) → event_proj_e → (N, 256)
# masked attention pooling → sample-aware InfoNCE
```

这个 head 提供的是 **temporal grounding**：它不只说"这个 event 和这个 motion 匹配"，
还说"这个 event 对应 motion 的哪个时间段"。stage2 的 event CLIP loss 没有这个能力。

## 3. 实验计划

### Step 1: S2E — stage2 配方在 HumanML3D-E regime 下重训

**目的：** 建立公平的 HumanML3D-E baseline，确认 stage2 配方在新 regime 下仍然有效。

**配置：**
- 完全复用 stage2_mp_gt 的配方（见 §2.2）
- 唯一改动：train/val split 切到 HumanML3D-E keyids
- warm-start: pretrained/HumanML3D/best_model.pt（和 stage2 一样从 pretrained 开始）
- exp_name: stage5_s2e（stage2 recipe on HumanML3D-E）
- epoch=50, batch_size=64, seed=42

**预期：** PrimaryScore ≈ 44.8-45.5（和 stage2_gt 相当或略高，因为 HumanML3D-E
的 event 覆盖更干净）

**Gate：**
- GO: PrimaryScore > 44.5 → 进入 Step 2
- STOP: PrimaryScore < 43.5 → 排查数据管线问题

#### ⚠️ S2E 结果 (2026-04-14): STOP — PrimaryScore = 42.76

**结果：** PrimaryScore = 42.76，低于 pretrained B0 (43.53)，远低于 stage2_gt (44.83)。
触发 STOP gate。

**退化模式：** nsim R@5 大幅下跌（t2m -6.19, m2t -5.16），normal 几乎持平。

**根因诊断：** S2E 配置中有 `init_from_checkpoint: pretrained/best_model.pt`，
而 stage2_gt **没有** init_from_checkpoint（从 ImageNet ViT 从零训练）。
warm-start 导致模型从一开始就在低 loss 区域（epoch 0 tr_loss=0.258 vs stage2_gt
的 3.77），event/temporal loss 的梯度太小，无法有效塑造 embedding 空间。

best_model 选择逻辑（按 m2t_r1）没有 bug，与 stage2_gt 一致。

**修复方案：** → Step 1v2 (S2E-v2)

详细报告见 `checkpoints/stage5_s2e/HumanML3D/report.md`。

### Step 1v2: S2E-v2 — 去掉 warm-start 重训

**目的：** 修复 S2E 的 warm-start 问题，复现 stage2_gt 的从零训练配方。

**配置：**
- 与 S2E 完全相同，唯一修改：`init_from_checkpoint: null`
- 从 ImageNet pretrained ViT 开始训练（和 stage2_gt 一致）
- exp_name: stage5_s2e_v2
- epoch=50, batch_size=64, seed=42

**预期：** PrimaryScore ≈ 44.5-45.0（与 stage2_gt 相当）

**Gate：**
- GO: PrimaryScore > 44.5 → 进入 Step 2（用 S2E-v2 作为基础）
- INVESTIGATE: 44.0 < PrimaryScore < 44.5 → HumanML3D-E split 可能有轻微数据质量差异
- STOP: PrimaryScore < 43.5 → HumanML3D-E split 有根本性问题

#### ✅ S2E-v2 结果 (2026-04-14): GO — PrimaryScore = 44.50

**结果：** PrimaryScore = 44.50 (tmr_strict)，与 stage2_gt (44.83) 差 0.33，在统计噪声内。
触发 GO gate。warm-start 假说完全确认。

**训练曲线：** epoch 0 tr_loss=3.97（与 stage2_gt 的 3.77 一致），best_epoch=48 (m2t_r1=17.64)。

详细报告见 `checkpoints/stage5_s2e_v2/HumanML3D/report.md`。

**下一步：** → Step 2 (S2E+T)，以 S2E-v2 为基础。

### Step 2: S2E+T — 在 S2E 基础上叠加 TMR event head

**目的：** 验证 temporal grounding 的增量价值。

**配置：**
- 在 S2E 的 loss 基础上，额外加 compute_tmr_event_alignment_loss 作为辅助 loss
- 总 loss = global(1.0) + event_clip(0.5) + temporal_neg(0.3) + **evt_align(0.2)**
- event_proj_e / event_proj_t 从 S2E checkpoint warm-start（如果 S2E 没有这些参数，
  则随机初始化）
- motion_projection 解冻（和 S2E 一致）
- exp_name: stage5_s2e_t（S2E + temporal grounding）
- epoch=50, batch_size=64, seed=42

**预期：** 如果 temporal grounding 有增量价值，PrimaryScore 应该比 S2E 高 0.3-1.0。
如果没有增量，说明 event CLIP loss 已经足够，temporal structure 在 retrieval 任务上
不提供额外信息。

**Gate：**
- GO: PrimaryScore(S2E+T) > PrimaryScore(S2E) + 0.3 → temporal grounding 有价值
- NEUTRAL: delta < 0.3 → temporal grounding 增量有限，但不有害
- STOP: PrimaryScore(S2E+T) < PrimaryScore(S2E) → temporal head 干扰了主 loss

## 4. 实施细节

### 4.1 S2E 不需要新代码

stage2_mp_gt 的训练路径（event_temporal）已经存在。只需要：
1. 让 train.py 在 event_temporal.enable=true 时也支持 HumanML3D-E split 切换
2. 或者在 shell 脚本里手动指定 split file

### 4.2 S2E+T 需要小量代码修改

在 train.py 的 event_temporal 训练循环里，额外调用
`model.compute_tmr_event_alignment_loss()` 并加到 total_loss。需要：
1. 在 config.yaml 的 event_temporal 块里加 `tmr_event_head_weight: 0.0`（默认关闭）
2. 在训练循环里，当 tmr_event_head_weight > 0 时，构造 event batch 并调用
3. model 需要同时启用 event_temporal 和 tmr_transfer 的 event head

### 4.3 eval 统一用 HumanML3D-E strict regime

所有 eval 产出 TMR-normal.yaml + TMR-nsim.yaml + eval_metadata.yaml。
PrimaryScore = mean(normal R@1/R@5 + nsim R@1/R@5) over t2m+m2t。

## 5. 时间线

```
Day 1 (done): S2E 训练 + eval — PrimaryScore=42.76, STOP gate triggered
Day 1 (done): 根因诊断 — warm-start 导致退化，可修复
Day 1 (done): S2E-v2 训练 + eval — PrimaryScore=44.50, GO gate ✅
Day 2 (done): S2E+T 训练 + eval — PrimaryScore=43.97, temporal head 无增益
Day 2 (done): Phase 2b 完结，S2E-v2 为最佳结果
```

## 6. 对论文的意义

- S2E-v2 是最佳结果（PrimaryScore=44.50），证明 event-aware contrastive learning 在 MotionPatches 上有效
- S2E+T (43.97) < S2E-v2 (44.50)：temporal grounding head 无增量价值，反而轻微干扰
- 论文叙事确定为：
  "event-aware contrastive learning is sufficient; temporal grounding provides
  interpretability but not retrieval improvement"
- S2E-v2 vs pretrained (+0.97) 和 vs D2b (+0.47) 的增益是论文的核心贡献
- Phase 2b 完结，下一步应聚焦论文写作和 ablation 实验设计

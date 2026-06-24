---
created: 2026-04-11
updated: 2026-04-11
status: summary
title: TAMR Stage4.1 Closure Summary
tags:
  - tamr
  - stage4.1
  - closure
  - summary
  - tmr
  - motionpatches
source:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d0-humanml3de-event-statistics-result.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d1-evaluation.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d1.5-evaluation.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d2a-evaluation.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d2b-evaluation.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-11_tamr-roadmap-phase1-vs-phase2.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/RUN_DIR/stage4_1_d1/contrastive_metrics/normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/TMR/RUN_DIR/stage4_1_d1/contrastive_metrics/nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/TMR/RUN_DIR/stage4_1_d2a/contrastive_metrics/normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/TMR/RUN_DIR/stage4_1_d2a/contrastive_metrics/nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/TMR/RUN_DIR/stage4_1_d2b/contrastive_metrics/normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/TMR/RUN_DIR/stage4_1_d2b/contrastive_metrics/nsim.yaml
---
# TAMR Stage4.1 Closure Summary

## 1. Executive Summary

Stage4.1 的最小诊断链已经闭环完成：

`D0 -> D1 -> D1.5 -> D2a -> D2b`

本轮闭环回答了四个核心问题：

1. HumanML3D-E 是否足够支持 event-time auxiliary 诊断；
2. frozen backbone 下是否真的存在可学习的 event-time signal；
3. attention pooling 是否比 uniform pooling 更有效；
4. motion backbone 解冻时，retrieval 退化到底来自“解冻本身”，还是来自“重型 auxiliary branch”。

最终结论：

- **Stage4.1 已完成闭环。**
- **Stage4 首轮 No-Go 的根因不是 full unfreeze 本身，而是 `过重 auxiliary branch + 过大解冻范围` 的组合。**
- **在 minimal event-time head + masked InfoNCE 的极简配方下，partial unfreeze 和 full unfreeze 都是安全的。**
- **D2b 是 Stage4.1 winner。**
- **下一步应进入 Phase 2（MotionPatches backbone 迁移），而不是先做 Step 5 evidence head。**

一句话总结：

> Phase 1 已经完成“temporal auxiliary branch 是否值得存在、以及是否会伤主表征”的机制验证；结论是值得存在，且在极简配方下不伤主表征，因此现在应把同样思路迁移到 MotionPatches backbone，而不是继续在 ACTOR/TMR 上扩写更重机制。

## 2. Terminology Note

需要说明一个命名口径变化：

- `Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v4-narrow-scope-execution.md` 中，`D3` 原本指向 `BASMA-lite`。
- `2026-04-11_tamr-roadmap-phase1-vs-phase2.md` 中，`D3` 已被收敛为 **Stage4.1 闭环总结 / Phase 2 启动门**。

本文件遵循 **较新的 roadmap 口径**，将 D3 视为闭环总结，而不是再在 TMR ACTOR backbone 上追加一轮 `BASMA-lite` 训练。

## 3. What Each Step Established

### 3.1 D0: Data Gate

- `K>=2` 占比：`70.58%`
- `K=1` 占比：`29.42%`
- overlap 规则占比：`4.48%`

结论：

- D0 三个 quantitative gate 都未触发；
- HumanML3D-E 足以支撑 Stage4.1 的最小 event-time 诊断；
- Stage4.1 主线可以合法进入 D1。

### 3.2 D1: Frozen Minimal Head

关键结果：

- `val_evt_align_acc`: `0.1118 -> 0.3587`，best `0.3960`
- retrieval 在 frozen 设定下基本不变

结论：

- frozen feature 中确实存在可提取的 event-time signal；
- minimal event-time head 不是空转，它能学到时序对齐信号；
- 但 D1 还不能回答 attention 是否必要，也不能回答 unfreeze 是否安全。

### 3.3 D1.5: Uniform Pooling Control

关键结果：

- `val_evt_align_acc` best: `39.60% (D1)` vs `16.77% (D1.5)`
- best gap: `+22.82pp`
- retrieval 与 D1 完全一致

结论：

- attention pooling 不是 cosmetic choice，而是实质性组件；
- retrieval 不变说明这个控制组是干净的；
- 因而 D2 继续沿用 attention pooling 是有充分依据的。

### 3.4 D2a: Partial Unfreeze

关键结果：

- normal t2m R@1: `9.46 -> 13.51`
- normal m2t R@1: `2.70 -> 16.22`
- nsim t2m R@1: `13.00 -> 17.00`
- nsim m2t R@1: `3.00 -> 26.00`

结论：

- `partial unfreeze + minimal head` 不但没有伤害主表征，反而显著改善 retrieval；
- 这已经推翻了“auxiliary branch 一解冻 backbone 就必然伤主表征”的强假设；
- Stage4 首轮 No-Go 的根因被收缩到：更可能是 heavy branch，而不是 unfreeze 本身。

### 3.5 D2b: Full Unfreeze

关键结果：

- normal t2m R@1: `13.51 -> 15.54`（vs D2a `+2.03`）
- normal m2t R@1: `16.22 -> 22.30`（vs D2a `+6.08`）
- nsim t2m R@1: `17.00 -> 22.00`（vs D2a `+5.00`）
- nsim m2t R@1: `26.00 -> 33.00`（vs D2a `+7.00`）
- `val_evt_align_acc` best: `0.4061 -> 0.4332`

结论：

- D2b 没有复现 Stage4 首轮的退化；
- full motion unfreeze 在 minimal head 配方下仍然安全；
- D2b 全面优于 D2a，因此成为 Stage4.1 winner。

## 4. Retrieval-First Gate Table

### 4.1 normal

| Metric | D1 | D2a | D2b |
| --- | ---: | ---: | ---: |
| t2m R@1 | 9.46 | 13.51 | 15.54 |
| t2m R@5 | 22.97 | 37.16 | 43.92 |
| t2m R@10 | 27.70 | 52.03 | 60.14 |
| m2t R@1 | 2.70 | 16.22 | 22.30 |
| m2t R@5 | 13.51 | 37.84 | 47.97 |
| m2t R@10 | 14.19 | 48.65 | 54.05 |

### 4.2 nsim

| Metric | D1 | D2a | D2b |
| --- | ---: | ---: | ---: |
| t2m R@1 | 13.00 | 17.00 | 22.00 |
| t2m R@5 | 29.00 | 46.00 | 53.00 |
| t2m R@10 | 37.00 | 61.00 | 67.00 |
| m2t R@1 | 3.00 | 26.00 | 33.00 |
| m2t R@5 | 12.00 | 49.00 | 54.00 |
| m2t R@10 | 18.00 | 56.00 | 63.00 |

### 4.3 Interpretation

有三个关键信号：

1. D2a 已经证明“partial unfreeze + minimal head”不会伤害主表征；
2. D2b 进一步证明“full unfreeze”在同一极简 auxiliary 配方下同样不会复现 Stage4 首轮退化；
3. D2b 在 `normal` 和 `nsim` 的核心 retrieval 指标上全面高于 D2a，因此不存在 No-Go 条件。

## 5. Final Stage4.1 Conclusion

Stage4.1 的最终闭环结论如下：

1. **temporal auxiliary branch 值得存在。**
   - D1 证明 frozen feature 中存在可学习的 event-time signal。
2. **attention pooling 值得保留。**
   - D1.5 证明 uniform pooling 会大幅削弱 event alignment。
3. **minimal head 比重型 temporal adapter 更稳定。**
   - Stage4 首轮 No-Go 的失败模式没有在 D2a / D2b 中出现。
4. **解冻 backbone 本身不是问题。**
   - partial 和 full unfreeze 都没有伤 retrieval，反而改善 retrieval。
5. **Stage4 首轮失败的主因是 heavy auxiliary branch，不是 full unfreeze 本身。**

因此，Stage4.1 的最重要产出不是一组最终数值，而是一个经过验证的机制结论：

> `minimal event-time head + attention pooling + masked InfoNCE + warm-start from D1 + motion backbone unfreeze`
>
> 是一个可训练、可解释、且不会伤害主检索表征的 temporal auxiliary recipe。

## 6. Winner and Next Step

### 6.1 Stage4.1 Winner

- **Winner: D2b**

理由：

- 相比 D2a，D2b 在 `normal` 和 `nsim` 上都给出更强 retrieval；
- 相比 D1，D2b 证明 auxiliary branch 不仅可学，而且能反向改善 backbone 表征；
- D2b 因而是当前 Phase 1 最值得迁移到 MotionPatches backbone 的配置。

### 6.2 What Not To Do Next

当前**不建议**先做以下事项：

- 不建议先在 ACTOR/TMR backbone 上继续扩写 `BASMA-lite`
- 不建议先启动 Step 5 evidence head
- 不建议把 Phase 1 的小 test set 数值直接当成最终论文结果

原因：

- Phase 1 的目标已经完成，是机制验证，不是最终数值追逐；
- Step 5 evidence head 属于更上层的输出结构，应放在最终 backbone 上评估；
- MotionPatches 才真正具备 `14 x 5` patch token 结构，后续 patch-support / richer temporal structure 也更有意义。

### 6.3 Recommended Next Step

- **Go Phase 2 with D2b**

Phase 2 的默认建议顺序：

1. 把 D2b 的 minimal event-time recipe 迁移到 MotionPatches backbone；
2. 保留 masked InfoNCE、event parsing、collate 与 retrieval protocol；
3. 在 MotionPatches 上重新 warm-start，不继承 Phase 1 ACTOR weights；
4. 等 MotionPatches 版 D2b recipe 跑通后，再决定是否进入 Step 5 evidence head。

## 7. Final Verdict

**D3 完成。**

**Stage4.1 已闭环。**

**Final verdict: Go Phase 2 with D2b.**

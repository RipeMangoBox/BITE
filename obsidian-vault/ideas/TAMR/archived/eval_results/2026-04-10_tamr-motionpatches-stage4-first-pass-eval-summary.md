---
## created: 2026-04-10

updated: 2026-04-10T01:20
source:

- /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-06_tamr-v3-event-abstraction-centered-design.md
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter/HumanML3D/train.log
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/TMR-normal.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/TMR-nsim.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/EVT-normal.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/EVT-nsim.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval/HumanML3D/contrastive_metrics/TMR-normal.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval/HumanML3D/contrastive_metrics/TMR-nsim.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval/HumanML3D/contrastive_metrics/EVT-normal.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval/HumanML3D/contrastive_metrics/EVT-nsim.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval_noinfer/HumanML3D/contrastive_metrics/TMR-normal.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval_noinfer/HumanML3D/contrastive_metrics/TMR-nsim.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval_noinfer/HumanML3D/contrastive_metrics/EVT-normal.yaml
- /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage4_mp_gt_adapter_eval_noinfer/HumanML3D/contrastive_metrics/EVT-nsim.yaml
tags:
- tamr
- motionpatches
- stage4
- eval
- summary
- temporal-adapter
status: summary
title: "TAMR MotionPatches Stage-4 First-Pass Eval: Token Adapter No-Go"
model_name: TAMR

# TAMR MotionPatches Stage-4 First-Pass Eval: Token Adapter No-Go

## 1. Executive Summary

本次 Stage 4（token-level temporal adapter）已完成首轮 full eval。

结论：

1. **不符合预期**：Stage 4 没有形成“稳定 temporal gain + 不伤主检索”的闭环。
2. **当前不应 go on 到 Step 5**：应判定为 **No-Go**。
3. **需要先进入 Step 4.1 问题定位迭代**：先恢复 hard temporal slice 指标，再讨论 coarse evidence head。

---
## 2. Evaluation Scope

本次使用独立 eval 输出目录，避免覆盖已有结果：

- Stage 2 对照：`checkpoints/stage2_mp_gt_step3diag/HumanML3D/contrastive_metrics/`
- Stage 4（adapter inference ON）：`checkpoints/stage4_mp_gt_adapter_eval/HumanML3D/contrastive_metrics/`
- Stage 4 诊断消融（同一 checkpoint，`eval.temporal_adapter.use_inference=false`）：`checkpoints/stage4_mp_gt_adapter_eval_noinfer/HumanML3D/contrastive_metrics/`

评测范围：

- `TMR-normal / TMR-nsim`
- `EVT-normal / EVT-nsim`
- Step 3 诊断维度：`ordering / before / after / negation / duration / existence`

---
## 3. Key Results

### 3.1 Retrieval + Temporal 主指标


| Metric               | Stage2 GT | Stage4 (inf ON) | Delta      |
| -------------------- | --------- | --------------- | ---------- |
| `TMR-normal t2m/R01` | 6.84      | 7.07            | +0.23      |
| `TMR-normal m2t/R01` | 10.47     | 10.52           | +0.05      |
| `TMR-nsim t2m/R01`   | 57.00     | 46.00           | **-11.00** |
| `TMR-nsim m2t/R01`   | 55.00     | 51.00           | -4.00      |
| `EVT-normal CAR01`   | 7.91      | 8.04            | +0.13      |
| `EVT-normal TAR01`   | 4.79      | 4.47            | -0.32      |
| `EVT-normal TAR10`   | 24.18     | 22.58           | -1.60      |
| `EVT-nsim CAR01`     | 66.67     | 56.25           | **-10.42** |
| `EVT-nsim TAR01`     | 33.00     | 23.00           | **-10.00** |
| `EVT-nsim TAR10`     | 51.00     | 44.00           | -7.00      |


判读：

- `normal` 上仅有轻微 R@1 改善；
- `hard temporal`（`nsim`）出现显著退化，这是当前 Step4 go/no-go 的关键负信号。

### 3.2 Step 3 诊断维度（`EVT-nsim` R@1）


| DIAG dimension | Stage2 GT | Stage4 (inf ON) | Delta  |
| -------------- | --------- | --------------- | ------ |
| `ordering`     | 47.92     | 39.58           | -8.34  |
| `before`       | 64.58     | 56.25           | -8.33  |
| `after`        | 64.58     | 54.17           | -10.41 |
| `negation`     | 57.00     | 46.00           | -11.00 |
| `duration`     | 37.00     | 27.00           | -10.00 |
| `existence`    | 50.00     | 45.00           | -5.00  |


判读：

- 退化不是单一维度，而是 across-dimension 的系统性回撤。

---
## 4. Targeted Diagnosis

### 4.1 训练过程信号

`train.log` 中 50 个 epoch 的 quick retrieval 指标显示：

- `t2m_r1`：epoch0 `14.23` -> epoch49 `14.44`，最佳 `15.74`（epoch19）
- `m2t_r1`：epoch0 `15.31` -> epoch49 `15.85`，最佳 `16.67`（epoch35）

整体特征是震荡平台而非持续抬升，这和你观察到的现象一致。

### 4.2 关闭 adapter 推理分支的消融（同一 checkpoint）

`eval.temporal_adapter.use_inference=false` 后（仅作诊断）：

- `EVT-nsim CAR01`: `56.25 -> 60.42`（+4.17）
- `EVT-nsim TAR01`: `23.00 -> 26.00`（+3.00）
- `TMR-nsim t2m/R01`: `46.00 -> 47.00`（+1.00）

这说明：

1. 推理时直接切到 adapter motion embedding 会进一步放大退化；
2. 但即使关掉 adapter 推理，仍明显低于 Stage2；
3. 问题不仅是 inference path，也包含 training phase 的表示漂移。

---
## 5. Go/No-Go Decision and Next Actions

### 5.1 Decision

- **Stage 4 首轮：No-Go**
- **Step 5：暂不启动**

### 5.2 Stage 4.1 最小阻塞解除方案

建议下一轮优先做最小改动验证，不扩架构：

1. 先固定推理主路径：默认 `eval.temporal_adapter.use_inference=false`，只把 adapter 当训练辅助分支。
2. 下调 adapter auxiliary 权重（例如 `0.2/0.1/0.1 -> 0.05/0.02/0.02`）验证是否减少对 hard temporal slice 的伤害。
3. 增加“冻结 backbone 仅训 adapter+projection”的对照，区分“适配器收益”与“全模型漂移”。
4. 继续沿 Step 3 的 `DIAG_`* 维度做验收门槛，满足门槛前不进入 Step 5。


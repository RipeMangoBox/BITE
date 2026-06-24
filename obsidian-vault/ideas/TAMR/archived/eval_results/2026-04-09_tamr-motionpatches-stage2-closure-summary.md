---
## created: 2026-04-09
updated: 2026-04-09T19:05
source:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-05_tamr-motionpatches-harness-design.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-06_tamr-v3-event-abstraction-centered-design.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/eval_summary/2026-04-06_tamr-motionpatches-stage1-closure-summary.md
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/generation_metrics/EVT-native_normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/generation_metrics/EVT-native_normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/.hydra/config.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/train.log
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/generation_metrics/EVT-native_normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/.hydra/config.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/train.log
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage2_mp_gt/HumanML3D/generation_metrics/EVT-native_normal.yaml
tags:
  - tamr
  - motionpatches
  - stage2
  - closure
  - summary
  - humanml3d-e-only
status: summary
title: "TAMR MotionPatches Stage-2 Closure: HumanML3D-E-Only GT Event-Aware Retrieval"
model_name: TAMR

# TAMR MotionPatches Stage-2 Closure: HumanML3D-E-Only GT Event-Aware Retrieval

## 1. Executive Summary

本轮 Stage 2 闭环回答四个问题：

1. 当前 Stage 2 是否已经完成 train、eval 和 summary；
2. `baseline / rule / stage1_gt / stage2_gt` 四组在统一口径下分别表现如何；
3. `HumanML3D-E-only + GT events` 主线是否已经足以继续推进；
4. 下一步到底应该推进到哪里，是否需要修改 roadmap。

结论先写在前面：

- **Stage 2 现在已经完成 train + eval + summary**。
- **当前证据继续支持 `HumanML3D-E-only + GT events` 主线**：temporal retrieval 仍明显优于 baseline。
- **Stage 2 不是“所有指标全面变好”**：它更像是把 GT 主线进一步推向了更强的 hard temporal slice 与更好的 generation proxy，同时在 `normal` strict retrieval 上仍保留 trade-off。
- **下一步应进入 Step 3，而不是直接上 Step 4**：也就是先补能力诊断与分关系诊断视图，再决定是否要上 token-level temporal adapter。

如果用一句话总结：

> Stage 2 已经证明 `HumanML3D-E-only` 主线在 aggregate-level 上是有效且可继续推进的，但它还没有完成 `H2/H3` 的细粒度能力闭环，因此当前默认下一步应是 Step 3，而不是更重的 motion-side architecture。

---
## 2. Artifact Scope and Important Caveats

### 2.1 本文采用哪一版数值

本文统一使用当前 `checkpoints/*` 目录下实际存在的 metric YAML 作为 ground truth。

这意味着：

- 如果个别数值与 `eval_summary/2026-04-06_tamr-motionpatches-stage1-closure-summary.md` 略有差异；
- 应以当前 checkpoint-local YAML 为准；
- 本文更关注“当前仓库现状下 Stage 2 的闭环判断”。

### 2.2 当前 Stage 2 应如何理解

这里先补一个重要更正：

- 当前工作区里的 `checkpoints/stage1_mp_gt/HumanML3D/.hydra/config.yaml` 曾被误覆盖；
- 因此不能再用“当前工作区直接 diff 出来的 config 差异”去判断 Stage 1 和 Stage 2 的真实配置差别；
- 应以 git 历史中的保存版本为准。

按 git 历史可恢复的保存版本看：

1. `stage1_mp_gt` 与 `stage2_mp_gt` **并非同一份 config**；
2. `stage2_mp_gt/HumanML3D/train.log` 的日志前缀仍打印 `Stage-1 event source=gt`；
3. 因此，**当前 Stage 2 更应被理解为同一条 GT-only 轻量 scaffold 的继续稳定化 / 再闭环**，而不是“已经引入一个全新大模块”的阶段。

这里第 3 条是结合现有 artifact 与训练产物做出的整体判断，但不再基于“两个 config 几乎相同”这个前提。

### 2.3 本文如何解读不同指标

需要先固定三个读数原则：

1. **`TAR` 比 `CAR` 更适合作为跨 setting 的主对比指标**
  - 因为 `TAR_queries` 在同一 protocol 下保持一致；
  - 而 `CAR_queries` 会随 event decomposition source 改变，特别是 `rule` 与 `gt` 不完全同口径。
2. **generation proxy 不是完全等 query 集**
  - `num_eval_queries` 会随 retrieval top1 变化而变化；
  - 因此 generation proxy 更适合看方向性，不适合被解读为绝对同集对比。
3. **Stage 2 是否成立，优先看 aggregate temporal gain 与主线可持续性**
  - per-relation `before / after / negation / duration / existence` 细分诊断仍属于 Step 3 要补的内容。

---
## 3. Unified Comparison Tables

### 3.1 Retrieval: `TMR-normal`

| Setting | R@1 | R@5 | R@10 | MedR |
| --- | --- | --- | --- | --- |
| baseline | 7.30 | 25.75 | 38.09 | 19 |
| rule | 7.62 | 25.41 | 38.25 | 18 |
| stage1_gt | 6.93 | 26.80 | 38.28 | 18 |
| stage2_gt | 6.84 | 25.55 | 38.80 | 18 |

相对 baseline：

- stage2_gt: `R@1 -0.46`, `R@5 -0.20`, `R@10 +0.71`, `MedR -1`

相对 stage1_gt：

- stage2_gt: `R@1 -0.09`, `R@5 -1.25`, `R@10 +0.52`, `MedR 0`

结论：

- `stage2_gt` 在 `normal` strict retrieval 上**没有形成全面提升**；
- 它基本延续了 GT 主线在 normal 协议上的 trade-off 特征；
- 因此 Stage 2 的成立，不能靠 `TMR-normal` 单独支撑。

### 3.2 Retrieval: `TMR-nsim`

| Setting | R@1 | R@5 | R@10 | MedR |
| --- | --- | --- | --- | --- |
| baseline | 51.00 | 87.00 | 90.00 | 1 |
| rule | 48.00 | 86.00 | 90.00 | 2 |
| stage1_gt | 55.00 | 86.00 | 88.00 | 1 |
| stage2_gt | 57.00 | 84.00 | 93.00 | 1 |

相对 baseline：

- stage2_gt: `R@1 +6.00`, `R@5 -3.00`, `R@10 +3.00`, `MedR 0`

相对 stage1_gt：

- stage2_gt: `R@1 +2.00`, `R@5 -2.00`, `R@10 +5.00`, `MedR 0`

结论：

- `stage2_gt` 在 hard temporal slice 的 `R@1` 上是当前四组里最强；
- 这说明 GT 主线继续往“更强时序辨别”方向推进是成立的；
- 但它仍不是所有 cutoff 都占优，所以更准确的表述是：**更偏向 hard temporal discrimination 的增强，而不是全面 semantic retrieval 增益**。

### 3.3 Temporal: `EVT-normal`

| Setting | CAR@1 | CAR@5 | CAR@10 | TAR@1 | TAR@5 | TAR@10 |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 6.14 | 21.47 | 30.27 | 3.95 | 12.84 | 18.11 |
| rule | 9.50 | 30.11 | 43.02 | 5.27 | 16.86 | 25.05 |
| stage1_gt | 6.65 | 27.61 | 38.57 | 4.79 | 17.50 | 24.61 |
| stage2_gt | 7.09 | 27.11 | 40.34 | 4.79 | 16.33 | 24.18 |

相对 baseline：

- stage2_gt: `CAR@1 +0.95`, `TAR@5 +3.49`, `TAR@10 +6.07`

相对 stage1_gt：

- stage2_gt: `CAR@1 +0.44`, `TAR@5 -1.17`, `TAR@10 -0.43`

结论：

- `stage2_gt` 相比 baseline 仍然明显更强；
- 但相对 `stage1_gt`，它在 `normal` temporal retrieval 上是**轻微回撤**；
- 因此 current Stage 2 的核心收益不在 `EVT-normal`，而更集中在 harder slice 与 generation proxy。

### 3.4 Temporal: `EVT-nsim`

| Setting | CAR@1 | CAR@5 | CAR@10 | TAR@1 | TAR@5 | TAR@10 |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 48.48 | 75.76 | 75.76 | 19.00 | 34.00 | 35.00 |
| rule | 54.17 | 91.67 | 93.75 | 27.00 | 48.00 | 51.00 |
| stage1_gt | 60.61 | 87.88 | 93.94 | 31.00 | 45.00 | 46.00 |
| stage2_gt | 66.67 | 87.88 | 93.94 | 33.00 | 46.00 | 51.00 |

相对 baseline：

- stage2_gt: `CAR@1 +18.19`, `TAR@5 +12.00`, `TAR@10 +16.00`

相对 stage1_gt：

- stage2_gt: `CAR@1 +6.06`, `TAR@5 +1.00`, `TAR@10 +5.00`

结论：

- 这是当前 Stage 2 最强的一组证据；
- `stage2_gt` 在 `EVT-nsim` 上相对 baseline 仍显著更好；
- 相对 `stage1_gt`，`TAR@10` 再提升 `+5`，说明 GT 主线在 hard temporal following 上继续增强。

### 3.5 Generation Proxy: `EVT-native_normal`

说明：

- `Matching_score` 越低越好；
- `R_precision_top_k` 越高越好；
- `FID` 越低越好；
- `num_eval_queries` 不是完全相同，因此更适合看方向性。

| Setting | Matching | R@1 | R@2 | R@3 | FID | Diversity | num_eval_queries |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 2.8596 | 0.5269 | 0.7280 | 0.8190 | 0.0508 | 9.1520 | 4146 |
| rule | 2.7907 | 0.5439 | 0.7373 | 0.8274 | 0.0609 | 9.4977 | 4110 |
| stage1_gt | 2.8938 | 0.5271 | 0.7214 | 0.8101 | 0.0470 | 9.0106 | 4126 |
| stage2_gt | 2.8473 | 0.5334 | 0.7310 | 0.8179 | 0.0364 | 9.1308 | 4116 |

相对 baseline：

- stage2_gt: `Matching -0.0123`, `R@1 +0.0066`, `FID -0.0145`

相对 stage1_gt：

- stage2_gt: `Matching -0.0465`, `R@1 +0.0063`, `FID -0.0107`

结论：

- `stage2_gt` 是当前 GT 主线里 generation proxy 最平衡的一次结果；
- 它相对 baseline 同时改善了 `Matching`、`R@1` 和 `FID`；
- 相对 `rule`，它依然没有拿到最好的 `Matching/R@1`，但 `FID` 明显更强。

---
## 4. What Improved and What Did Not

### 4.1 Relative to Baseline

相对原始 MotionPatches baseline，`stage2_gt` 的结论可以拆成三层：

1. **strict retrieval**
  - `TMR-normal` 没有明显变好；
  - `TMR-nsim R@1` 明显更强。
2. **temporal retrieval**
  - `EVT-normal TAR@5/10` 分别提升 `+3.49 / +6.07`；
  - `EVT-nsim TAR@5/10` 分别提升 `+12 / +16`。
3. **generation proxy**
  - `Matching` 更低；
  - `R_precision_top_1` 更高；
  - `FID` 更低。

因此：

> Stage 2 已经足以说明 GT event 主线不是只在“挪动指标”，而是在 hard temporal slice 与 generation proxy 上都给出可见增益。

### 4.2 Relative to Rule

相对 `rule`：

- `stage2_gt` 在 `TMR-normal` 上并不占优；
- 在 `TMR-nsim R@1` 上明显更强；
- 在 `EVT-normal` 上略弱于 `rule`；
- 在 `EVT-nsim TAR@10` 与 `rule` 打平，在 `CAR@1` 上更强；
- 在 generation proxy 上 `FID` 明显更好，但 `Matching/R@1` 仍不如 `rule`。

因此：

> `stage2_gt` 仍然不是“全指标压过 rule”，但它比 `rule` 更符合 TAMR 当前要强调的主线：`HumanML3D-E-only`、GT-supervised、偏 hard temporal discrimination。

### 4.3 Relative to Stage 1 GT

相对 `stage1_gt`：

- `TMR-normal` 略退；
- `TMR-nsim` 变强；
- `EVT-normal` 略退；
- `EVT-nsim` 变强；
- generation proxy 明显变强。

也就是说：

- Stage 2 **不是** “Stage 1 GT 的单调加强版”；
- 它更像是把 GT 主线继续推向：
  - 更强的 harder temporal slice；
  - 更好的 generation proxy；
  - 但在 `normal` slice 上保留一定 trade-off。

---
## 5. Stage-2 Goal Check Against Canonical Design

canonical Stage 2 的核心要求有三条：

1. `H2-H3` 指标进一步提升；
2. 在 `GT-event-only` 设定下也能观察到稳定 temporal gain；
3. 如果这一阶段已经足够支撑论文主张，则继续沿这条主线推进。

### 5.1 条件 1：`H2-H3` 指标进一步提升

结论：**部分达成，且目前是 aggregate-level 达成。**

原因是：

- 从 aggregate temporal metrics 看，`stage2_gt` 在 `EVT-nsim` 上相对 `stage1_gt` 继续提升；
- 相对 baseline，`EVT-normal` 与 `EVT-nsim` 都仍明显更强；
- 但当前还没有 per-relation `before / after / negation / duration / existence` 面板，因此不能把这个结论直接写成“完整 H3 已闭环”。

### 5.2 条件 2：在 `GT-event-only` 设定下也能观察到稳定 temporal gain

结论：**已达成。**

原因是：

- 当前 `stage2_gt` 仍然是 `HumanML3D-E-only + GT events` 主线；
- temporal gain 依然成立。

### 5.3 条件 3：是否继续沿当前主线推进

结论：**需要继续沿当前主线推进。**

更稳的说法是：

- 现有证据已经足以支持继续沿 GT event 主线走到 Step 3；
- 当前 roadmap 不需要再保留额外动作侧时间锚点分支；
- 后续实验应直接围绕 GT event 主线继续补诊断与回归证据。

---
## 6. Final Decision and Roadmap Update

### 6.1 当前 go / no-go 判断

最终判断：

- **对 Stage 2 本身：go**
  - 训练、eval、summary 都已完成；
  - aggregate-level temporal gain 成立；
  - `HumanML3D-E-only` 主线可继续。
- **对 Step 4 / Step 5：暂时 no-go**
  - 现在直接上 token-level adapter 还太早；
  - 先补 Step 3 才能知道后续 architecture 增益到底来自哪里。

### 6.2 下一步默认动作

下一步默认动作应固定为：

1. 进入 Step 3，补齐诊断视图：
  - ordering
  - before / after
  - negation
  - duration
  - existence
2. 在 Step 3 中把 `H1/H2/H3` 的边界拆开报告；
3. 只有在 Step 3 之后，才决定是否进入 Step 4 的 token-level temporal adapter。

### 6.3 对 roadmap 的实际修改

结合当前 Stage 2 结果，roadmap 的执行顺序应明确改成：

1. **Step 0-2 已闭环到足以继续决策**
2. **当前默认进入 Step 3**
3. **后续实验固定沿 GT event 主线推进**
4. **如需更强证据，优先补 seed-level stability / checkpoint sensitivity，而不是先堆新模块**

其中第 4 条的原因是：

- Stage 1 与 Stage 2 的当前工作区 config 已不适合直接做可靠差分；
- 但从已保存指标看，不同 run 之间仍然出现了不小幅度的移动；
- 这说明在进入更重 architecture 之前，补一点 run stability 证据会更稳。

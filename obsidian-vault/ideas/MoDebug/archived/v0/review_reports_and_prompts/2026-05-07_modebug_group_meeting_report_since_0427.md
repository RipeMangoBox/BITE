---
created: 2026-05-07T18:00:00+08:00
updated: 2026-05-07T21:20:00+08:00
title: MoDebug 0427 组会后进度汇报
status: active
tags:
  - MoDebug
  - group_meeting
  - progress_report
source:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]"
  - "[[2026-05-01_modebug-unified-ideas-progress]]"
  - "[[2026-05-01_modebug-eventt2m-retrain-sanity-plan]]"
  - "[[2026-05-05_modebug-s7-component-eval-summary]]"
  - "[[artifacts/modebug_motiongpt/motiongpt_setup_eval_report_20260507]]"
  - "[[artifacts/modebug_motiongpt/motiongpt_remote_retrain_20260507]]"
  - "[[artifacts/modebug_backbone_audit/backbone_position_decision_20260507]]"
  - "[[artifacts/modebug_backbone_audit/mogents/result_summary_20260507]]"
---

# MoDebug 0427 组会后进度汇报

> [!abstract] Canonical Name
> **MoDebug** = **Mechanistic Motion Debugging**.
>
> Current full name: **MoDebug: Mechanistic Motion Debugging for Cross-Generator Event-Level Text-to-Motion Failures**. `Mo` means motion, not MotionGPT; MotionGPT is only the first mechanism-probe generator.

汇报范围：2026-04-27 组会后至 2026-05-07，重点关注 MoDebug。整体进展可以概括为：先完成 EventT2M 旧路线的复现、评估器和 reward probe 资产建设，再通过 generated-motion scale audit 发现 EventT2M 不适合作为当前 backbone，随后将 active 路线迁移到以 MotionGPT 为第一机制探针、并面向多类 pretrained generator 的 failure mechanism diagnosis 框架。

## 1. 当前一句话结论

MoDebug 已从“基于 EventT2M 输出做 post-hoc failure/repair”转为“发现多事件 motion generator 的 event-level failure 内部机制，并在多类 pretrained generator 上验证 original vs original+MoDebug”。EventT2M 相关结果保留为 historical provenance / diagnostic inventory，不再作为 active backbone 或 evaluator；MotionGPT base 已通过官方源码、资产、pretrained smoke、clean eval 和 remote stage2 DDP smoke 的基础可靠性检查，是第一机制探针。下一步关键门槛是 M1 trace instrumentation、MoMask / MoGenTS 的同协议 P0 生成与 evidence export、M2 cross-generator failure search，以及判断 failure signature 是否能支持 targeted intervention。

## 2. 原路线与新路线对比

| 维度 | 原路线：基于 EventT2M 输出做诊断 / 修复 | 新路线：跨 generator 的失败内因与干预 | 为什么调整 |
| --- | --- | --- | --- |
| 核心问题 | 生成动作里哪些子事件缺失、顺序错误或语义不对 | 失败在生成过程中何时出现，能否在多个 pretrained generator 中形成共享 failure family | 研究问题从“错了多少”收缩到“为什么会错、能否跨模型干预” |
| MotionGPT 的角色 | 不适用；原路线依赖 EventT2M 输出 | 第一机制显微镜：优先导出 motion token、logits、entropy、hidden states；不是新的 generator 贡献本身 | MotionGPT 的价值在内部 trace 可导出，但不应限定 MoDebug 上限 |
| MoMask / MoGenTS 的角色 | 不适用或只作 baseline | P0 pretrained generator 候选，用同一 prompt protocol 做 `original` vs `original+MoDebug` | 支撑至少三类 generator 的泛化论证 |
| 主要证据 | 生成动作、视频、人审、外部打分器 | 生成动作 + generator-specific evidence：MotionGPT trace、MoMask mask/token confidence、MoGenTS joint-time evidence | 新路线能建立 failure signature，而不只是事后判别 |
| 当前能说明什么 | EventT2M paper-native 指标基本可复现；reward / evaluator 资产有诊断价值 | MotionGPT 工程链路已跑通；MoMask / MoGenTS 是下一批 P0 候选 | 目前仍不能声称最终 failure rate、方法提升或新 generator |
| 当前最大问题 | 生成骨架出现明显数值爆炸，不能继续作为主线证据 | 稳定 trace / evidence 尚未导出；还没有跨 generator 复现的 event-level failure family | 旧路线卡在输出可信度，新路线卡在机制证据采集 |
| 方法发展方式 | 倾向于先设计 reward / guidance，再看是否改善结果 | 先找到可预测的 failure signature，再按 generator 设计最小 targeted intervention | 避免在机制证据不足时把 MoDebug 包装成方法或 generator |
| 对外表述 | EventT2M 结果作为历史复现和问题暴露，不再作为当前主线 backbone | MoDebug 是 pretrained motion generator failure 的机制诊断与干预框架，不是新 motion generator | 避开 Motion-R1 / MoRL / AToM / ReAlign 等拥挤赛道的正面冲突，同时保留可验证上限 |
| 下一步 | 除非修复数值范围问题，否则不继续扩 EventT2M 主线实验 | 跑共享 prompt 组，导出 MotionGPT trace 与 MoMask / MoGenTS evidence，寻找共享 failure signature，并做最小干预验证 | 优先闭合“机制签名 -> 失败预测 -> original+MoDebug 改善”链路 |

## 3. 0427 后完成的主要工作

### 3.1 旧 EventT2M 路线：完成复现与边界确认

1. 完成 EventT2M clean retrain 与 paper-native full-level sanity：
   - 训练使用官方 README-style HumanML3D 2-GPU 设置，约 15.1 小时完成。
   - Released pretrained 在 HumanML3D native eval 中接近论文 Table 1：本地 FID `0.048`、R@3 `0.842`、matching `2.715`；论文报告 FID `0.056±.002`、R@3 `0.842±.002`、MM-Dist `2.711±.005`。
   - clean retrain 也做过 sanity check，但组会展示只保留 released pretrained 与论文指标的直接对比。
   - 结论边界：这只证明 full-level / paper-native reproducibility，不证明 event-level correctness，也不证明当前 generated motion 可用。

**EventT2M HumanML3D standard eval vs paper Table 1：**

| Source | Checkpoint | FID↓ | R@1↑ | R@2↑ | R@3↑ | Matching / MM-Dist↓ | Diversity |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Paper Table 1 | Event-T2M | `0.056±0.002` | - | - | `0.842±0.002` | `2.711±0.005` | - |
| Local native eval | released `hml3d.ckpt` | `0.048` | `0.555` | `0.752` | `0.842` | `2.715` | `9.575` |

**EventT2M HumanML3D-E condition eval vs paper Table 3：**

| Condition | Source | Checkpoint | FID↓ | R@1↑ | R@2↑ | R@3↑ | Matching / MM-Dist↓ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| C2 | Paper Table 3 | Event-T2M | `0.079` | `0.536` | `0.732` | `0.824` | `2.836` |
| C2 | Local condition eval | released `hml3d.ckpt` | `0.079` | `0.533` | `0.730` | `0.824` | `2.823` |
| C3 | Paper Table 3 | Event-T2M | `0.137` | `0.487` | `0.687` | `0.790` | `2.928` |
| C3 | Local condition eval | released `hml3d.ckpt` | `0.144` | `0.509` | `0.696` | `0.787` | `2.919` |
| C4 | Paper Table 3 | Event-T2M | `0.265` | `0.466` | `0.660` | `0.767` | `3.063` |
| C4 | Local condition eval | released `hml3d.ckpt` | `0.262` | `0.481` | `0.664` | `0.758` | `3.008` |

这些表的用途是说明 EventT2M 的 paper-native eval / condition eval 基本可复现；它们不能抵消 5/6 generated-motion skeleton scale audit 的 blocker。

2. 补齐 EventT2M / TMR / ChronAccRet 的 diagnostic inventory：
   - native TMR omission dataset eval：`n=3799`，`full_text vs drop_text` paired accuracy `0.7044`，`full_text vs replace_text` paired accuracy `0.8363`，role=`side_signal`。
   - ChronAccRet HumanML3D-E adapter：ordering CAR 约 `0.6579` 到 `0.6725`，role 为 ordering side evidence / sanity，不是 held-out final evaluator。
   - TMR 与 ChronAccRet 的 safe-drop agreement `0.7332`，5plus bucket agreement `0.6375`；aligned-replace agreement `0.8165`。
   - hard-replace lexical pilot 中 TMR `full_text vs replace_text` paired accuracy 降到 `0.6523`，说明 easy-negative inflation 风险真实存在。

3. 完成 reward probe 的 full split 训练和 go/no-go 检查：
   - S2b full split single-seed reward probe 的 best epoch 为 `32`。
   - same-protocol val 上 cosine `full_text vs drop_text` paired accuracy `0.6936`，MLP reward 为 `0.9288`，提升 `+0.2352`，满足 single-seed 2pp rule。
   - test observation 中 reward `full_text vs drop_text` paired accuracy `0.9016`，但 `replace_text` 和 `shuffle_text` 分别只有 `0.6489` 和 `0.5333`。
   - 结论边界：presence / omission reward signal 成立，但这仍是 `dev_metric` / observation，不能写成 final generation improvement，也不能证明 ordering 或 replacement 已解决。

### 3.2 关键转折：EventT2M generated-motion backbone 被暂停

5/6 对 EventT2M generated motion 做静态骨架量纲审计后，发现 paper-native full-level 指标接近并不能保证生成骨架正常：

| Motion source | `joints_abs_mean` | Range | 角色 |
| --- | ---: | --- | --- |
| GT sample `003245` | `0.484` | `[-0.302, 1.658]` | sanity reference |
| EventT2M `epoch_135` upstream-like entry | `22.658` | `[-193.971, 84.029]` | diagnostic blocker |
| EventT2M `epoch_135` full-events | `29.865` | `[-239.366, 73.679]` | diagnostic blocker |
| EventT2M `epoch_135` all-blank | `28.322` | `[-237.707, 101.004]` | diagnostic blocker |

小 scheduler 对照也不能修复：`epoch135_ddim_10` 的 `joints_abs_mean=14.540`，`epoch135_unipc_50` 的 `joints_abs_mean=17.246`。因此当前决策是：EventT2M 不再作为 active MoDebug backbone / evaluator / fallback；相关文档迁入 `blocked/legacy_eventt2m/`，只作为 historical provenance、diagnostic schema 和 blocker evidence 使用。

**生成骨架数值范围 / scale sanity 对比：**

> [!warning]
> 下表只比较 generated joints 的数值量级是否在 HumanML3D-style scale 内，不比较语义质量。EventT2M 行来自 `003245` 单样本审计；MotionGPT 和 MoGenTS 行来自各自 smoke / battery，不是同 prompt、同 seed、同模型质量协议。

| Source | Protocol / sample | Shape | Finite rate | `joints_abs_mean` | Overall range | Scale vs GT `003245` | 判断 |
| --- | --- | --- | ---: | ---: | --- | ---: | --- |
| HumanML3D-E GT | sample `003245` | `(T,22,3)` | `1.0` | `0.484` | `[-0.302, 1.658]` | `1.0x` | 正常参考 |
| EventT2M `epoch_135` | upstream-like entry, sample `003245` | `(T,22,3)` | `1.0` | `22.658` | `[-193.971, 84.029]` | `46.8x` | 数值爆炸 |
| EventT2M `epoch_135` | full-events, sample `003245` | `(T,22,3)` | `1.0` | `29.865` | `[-239.366, 73.679]` | `61.7x` | 数值爆炸 |
| EventT2M `epoch_135` | all-blank, sample `003245` | `(T,22,3)` | `1.0` | `28.322` | `[-237.707, 101.004]` | `58.5x` | 数值爆炸 |
| EventT2M `epoch_135` | DDIM 10-step scheduler check | `(T,22,3)` | `1.0` | `14.540` | `[-118.748, 40.782]` | `30.0x` | 仍异常 |
| EventT2M `epoch_135` | UniPC 50-step scheduler check | `(T,22,3)` | `1.0` | `17.246` | `[-61.167, 99.296]` | `35.6x` | 仍异常 |
| MotionGPT base | local official demo smoke | `(1,116,22,3)` | `1.0` | `0.984` | `[-0.298, 2.425]` | `2.0x` | HumanML3D-scale |
| MotionGPT base | remote official demo smoke | `(1,116,22,3)` | `1.0` | `0.984` | `[-0.298, 2.425]` | `2.0x` | HumanML3D-scale |
| MoGenTS | 6-prompt non-IK battery | `(196,22,3)` | `1.0` | `0.493` to `1.105` | `[-2.490, 3.312]` | `1.0x` to `2.3x` | HumanML3D-scale |

这个对比说明：EventT2M 的问题不是 NaN 或 eval 指标不复现，而是 decoded/generated joints 的绝对量级比正常 HumanML3D 骨架大约 `30x` 到 `62x`；MotionGPT 和 MoGenTS 的 smoke 输出则仍在 `1x` 到 `2.3x` 的正常量级范围内。因此 5/6 后暂停 EventT2M 是 backbone hygiene 决策，不是单纯的模型偏好切换。

### 3.3 Probe 迁移与新定位

迁移后，MoDebug 的 active thesis 改为：

```text
counterfactual text -> internal representation comparison -> failure mechanism signature -> targeted process-time intervention
```

核心变化：

1. 不再把主路线写成 generated-motion slicing、local artifact recognition 和 post-hoc repair。
2. 改用 `full_text / drop_text / replace_text / shuffle_text` 构造配对输入，比较不同 generator 的 generator-specific evidence：MotionGPT trace、MoMask mask/token confidence、MoGenTS joint-time evidence 或 candidate evidence。
3. EventProbe 负责机制诊断；PerceptGuide 只有在 failure signature 能预测并干预失败后，才升级为 process-time correction 方法分支。

当前 active 路线不再固定为 MotionGPT-only。MotionGPT base 是第一机制探针；MoMask 和 MoGenTS 是 P0 pretrained-generator 候选，用于后续同协议 `original` vs `original+MoDebug` 验证。TMR 与 ChronAccRet 只作为 side signals。

### 3.4 MotionGPT 官方链路已打通

MotionGPT 已完成以下基础 gate：

1. 官方源码与资产 preflight：
   - 本地与 remote4090 均使用 OpenMotionLab 官方 MotionGPT clone，HEAD `001aaca8d0ee218fc17f8265d11ac124044fe42f`。
   - active checkpoint 为官方 HF `OpenMotionLab/MotionGPT-base`。
   - active T5 为完整 seq2seq `google/flan-t5-base`，preflight 检查到 `encoder=110`、`decoder=170`、`lm_head=1`、`shared=1`。
   - checkpoint、T2M evaluator、GloVe、canonical HumanML3D 和 symlink 规则均通过检查。

2. pretrained demo smoke：
   - local output shape `(1,116,22,3)`，finite rate `1.0`，range `[-0.298064, 2.424644]`，abs mean `0.983714`。
   - remote output shape `(1,116,22,3)`，finite rate `1.0`，range `[-0.298070, 2.424532]`，abs mean `0.983732`。
   - 结论：没有 EventT2M 式 skeleton explosion，MotionGPT pretrained output 在 HumanML3D-scale 内。

3. clean-assets single-rep eval：
   - `Metrics/FID/mean = 0.211052`
   - `Metrics/R_precision_top_3/mean = 0.664009`
   - `Metrics/Matching_score/mean = 3.991370`
   - `Metrics/Diversity/mean = 9.460489`
   - `Metrics/MultiModality/mean = 3.445228`
   - 与论文 pre-trained row 相比，FID / Diversity / MultiModality 同量级，但 R-Precision 较弱、MMDist 较高。该结果是 checkpoint-environment parity / backbone sanity，不是 paper-level 20-run reproduction。

4. remote4090 stage2 DDP smoke / short retrain：
   - 生成了 `datasets/humanml3d/TOKENS`，`train.txt=23384` ids，写出 token files `22326`，length filter skip `1058`，missing motion files `0`，failed encodes `0`。
   - stage2 DDP 训练正常完成 1 epoch，log 显示 `Trainer.fit stopped: max_epochs=1 reached.` 和 `Training ends!`，wrapper exit code `0`。
   - 产出 checkpoint `experiments/mgpt/MoDebug_Pretrain_HumanML3D_DDP_Smoke_20260507/checkpoints/last.ckpt`，约 `3.2 GB`，metadata `epoch=1`、`global_step=4620`。
   - 结论：官方 MotionGPT 前半段训练链路在 remote4090 上可运行；这不是 convergence 结果，但足以说明 stage2 training chain、token cache 和 DDP 路径可用。

### 3.5 MoGenTS 作为 baseline/fallback 的初筛结果

MoGenTS 完成第一轮 backbone reliability gate：

1. pretrained generation 本地可运行，生成 6 个 non-IK 样本和 6 个 IK 样本。
2. non-IK 输出均为 `(196,22,3)`，finite rate `1.0`。
3. `joints_abs_mean` 范围 `0.493075` 到 `1.105252`，不是 EventT2M 式爆炸量纲。
4. training entry smoke 可启动，写入 log / opt / code snapshot，加载 evaluator、model 和 dataset，并使用 CUDA。

当前定位：MoGenTS 可保留为 structural temporal baseline / fallback，但由于其文本条件主要是 CLIP global conditioning，不适合作为 MotionGPT 式 token-level event attribution 主 backbone。

## 4. 当前核心判断

1. **EventT2M 的问题不是“论文 full-level 指标没复现”，而是“当前 generated motion scale 不可信”。** 因此旧路线不能继续用 EventT2M 输出闭合 S7/S8/S10。

2. **MoDebug 的主贡献应收缩到 failure mechanism-first。** 先证明 event-level failure 有可复现的内部机制签名，再决定 PerceptGuide 是否有足够证据升级为 targeted intervention；不能先把 reward-side 信号包装成最终 improvement，也不能把当前路线写成新 motion generator。

3. **MotionGPT 是当前最合适的机制探针入口。** 它有文本 token 和 motion token 的条件生成结构，适合做 counterfactual trace comparison；但 attention、hidden states、logits、entropy 还没有导出，必须通过 M1 instrumentation 后才能写任何内部机制结论。

4. **automatic evaluator 只能分角色使用。** TMR 是 semantic compatibility side signal，ChronAccRet 是 ordering side signal；human calibration 前不能把任何 automatic score 写成真实 failure rate 或 held-out final evaluator。

## 5. 尚未完成 / 风险

1. MotionGPT M1 trace instrumentation 尚未完成：当前官方 demo / eval 路径不直接导出 `output_attentions`、`output_hidden_states`、`output_scores`、entropy 或可对齐的 generated motion token trace。
2. M2 counterfactual failure search 尚未开始：还没有在 MotionGPT 上闭合 `full_text / drop_text / replace_text / shuffle_text` 的 paired output + internal trace 证据。
3. clean eval 是 single replication sanity，不是论文 20-run protocol；如果后续需要严肃 benchmark 对齐，要单独安排重跑。
4. MotionGPT stage2 smoke 已过，但 stage3 / finetune / adapter 路径还没证明；当前不能写训练收敛、方法效果，或新 generator claim。
5. EventT2M 的 reward probe 只能保留为历史 dev_metric / baseline 资产；不能迁移成 MotionGPT 最终结论。

## 6. 下一步计划

1. **M0 扩展**：用 event/temporal prompt battery 在 MotionGPT 上跑 batch generation，保存 joints、features、prompt、output text、static plots 和 manifest。
2. **M1 instrumentation**：写独立 debug wrapper 或最小补丁，导出 text tokens、motion token IDs、sequence scores/logits、entropy、hidden states，以及可行时的 attention / cross-attention。
3. **M2 failure search**：构造 `full_text / drop_text / replace_text / shuffle_text` paired prompt groups，先单 seed 可解释，再扩 multi-seed；failure label 必须同时有 output-level 和 trace-level 证据。
4. **M4 side-signal calibration 准备**：在 MotionGPT 输出可稳定生成后，接 TMR / ChronAccRet side signals，并准备小样本人审 anchor；不把 automatic scorer 当 final judge。
5. **PerceptGuide gate**：只有 M2 指向可预测、可干预的失败机制后，再决定是 logit / entropy guidance、attention regularization、counterfactual reranking，还是 lightweight adapter / finetune；否则 MoDebug 只保留为诊断资产。

## 7. 组会可讲版本

过去两周我把 MoDebug 从旧的 EventT2M 依赖路线推进到一个更稳的机制诊断路线。首先，我完成了 EventT2M 的 full-level 复现和评估器 / reward probe 资产建设，确认论文 native metrics 和 reward-side omission signal 是能跑通的。但进一步审计 generated motion 后发现，EventT2M 虽然 FID / R-Precision 接近论文，实际生成骨架在样本上出现 20 到 30 量级的 scale explosion，因此不能继续作为 MoDebug 的 active backbone。

基于这个结果，我把 EventT2M-era 文档全部降级为 blocked / historical provenance，并重新定义 MoDebug：不再做 post-hoc repair，也不把目标写成新的 motion generator，而是用 MotionGPT 作为可检查入口，寻找多事件 motion generation failure 的内部机制。MotionGPT 官方源码、checkpoint、HumanML3D、T5 和 evaluator 资产已经在本地和 remote4090 通过 preflight；pretrained smoke 输出正常，clean eval 没有 skeleton collapse；stage2 DDP smoke 也在 remote4090 正常完成并写出 checkpoint。下一步核心工作是导出 MotionGPT 的 token / logits / entropy / hidden-state / attention trace，然后用 full/drop/replace/shuffle prompt 找可复现的 event-level failure signature，并决定是否有足够机制证据推进 trace-based reranking / guidance / adapter 这类最小 targeted intervention。

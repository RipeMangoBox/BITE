---
created: 2026-04-29T22:47
updated: 2026-05-01T16:05:43+08:00
title: MoDebug Roadmap：双论文框架（EventProbe + PerceptGuide）
status: active
tags:
  - MoDebug
  - roadmap
  - EventT2M
  - HumanML3D-E
  - evaluator
  - generation
  - dual-paper
related_notes:
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
  - "[[2026-04-30_modebug-paper-a-eventprobe-plan]]"
  - "[[2026-04-30_modebug-paper-b-perceptguide-plan]]"
  - "[[2026-05-01_modebug-eventt2m-retrain-sanity-plan]]"
---

# MoDebug Roadmap：双论文框架（EventProbe + PerceptGuide）

> [!abstract] **Canonical TL;DR**
> - MoDebug 拆分为两篇独立论文：**Paper A (EventProbe)** human-calibrated diagnostic benchmark + evaluation methodology；**Paper B (PerceptGuide)** event-marginal reward + inference-time correction。
> - 两篇可并行推进、各自独立成文。A 侧重 event-counterfactual diagnostic protocol、human calibration、modern baseline failure atlas；B 侧重 masked-event perception loss、event-marginal reward learning、inference-time gradient injection。
> - 共享基础设施：`Event-T2M + HumanML3D-E`、counterfactual corruption protocol、TMR/ChronAccRet scoring pipeline，但 EventT2M retrain sanity 和 ChronAccRet coverage fairness 是 P0 gates。
> - 详细 plan 见 [[2026-04-30_modebug-paper-a-eventprobe-plan|Paper A Plan]] 和 [[2026-04-30_modebug-paper-b-perceptguide-plan|Paper B Plan]]。
> - 当前不自建 evaluator，不引入 MotionPatches，不把 `TMR Phase 1` / `PAPO-lite` debug、raw attention 或 MLLM sidecar 写成正式 judge。

## 1. Active Root Notes

`paperIDEAs/MoDebug/` 根目录只保留当前还会被继续维护的 active 入口：

1. [[ideas/MoDebug/README|README]]
   - 当前唯一总入口，固定术语、指标命名、禁写表述和读取顺序。
2. [[2026-04-29_modebug-roadmap|Roadmap]]
   - 当前最权威的路线、边界、gate 与双线并行关系。
3. [[2026-04-29_modebug-exec-plan|Exec Plan]]
   - 统一放置 generation exec 与 evaluator exec，分章节推进。
4. [[2026-04-29_modebug-evaluator-status-summary|Evaluator Status Summary]]
   - 记录当前正式 evaluator 证据、数值、artifact 与解释边界。
5. [[2026-05-01_modebug-eventt2m-retrain-sanity-plan|EventT2M Retrain Sanity Plan]]
   - P0 clean retrain 命令、时长估计、pretrained/retrain 比较协议。
6. [[2026-04-29_modebug-heldout-eval-policy|Held-Out Eval Policy]]
   - 固定 reward scorer/protocol 与 final main-table evaluator/protocol 必须分离的硬规则。
7. [[2026-04-30_modebug-paper-a-eventprobe-plan|Paper A EventProbe Plan]]
   - Paper A 的定位、贡献、实验和禁写边界。
8. [[2026-04-30_modebug-paper-b-perceptguide-plan|Paper B PerceptGuide Plan]]
   - Paper B 的方法定位、实验和与 Paper A 的边界。

概念解释、attention feasibility、MLLM sidecar feasibility、旧 `Plan B`、PAPO-lite、continuation prompt、review prompt、RL primer、临时 PDF / JSON 支撑材料已归档到 `paperIDEAs/MoDebug/archived/`。归档内容只作历史或实现支撑，不是 active source of truth。

## 2. Fixed Scope

当前双主线并行推进：

> **Paper A (EventProbe)**：human-calibrated event-counterfactual diagnostic benchmark，用 `drop / hard-replace / shuffle`、human calibration 与 modern baseline failure atlas 系统诊断多事件运动生成的 event-level failures。
> **Paper B (PerceptGuide)**：event-marginal reward model + masked-event perception loss + inference-time gradient injection，用于改善 omission / ordering。
> 两篇共享 `Event-T2M + HumanML3D-E` 基础设施和 corruption family，各自独立成文。

写死的边界：

1. generation backbone 暂以 `Event-T2M` 为候选，但必须先通过 retrain sanity：用 clean upstream repo 复现训练，并比较 retrain checkpoint 与官方 `hml3d.ckpt` 的 native eval 指标。
2. 主数据源固定为 `HumanML3D-E`。
3. `ChronAccRet event_texts` 只作为 runner-side input，不替代 HumanML3D-E 主数据口径；进入主表前必须报告 coverage、bucket 分布和 uncovered rows。
4. `MotionPatches` 不参与任何正式 eval / scorer / judge 链路。
5. `TMR Phase 1` / `PAPO-lite` 只保留为历史 debug，不作为正式 evaluator。
6. `AToM` 当前只记录 MotionGPT native generation metrics，不进入当前主 judge。
7. 当前不自建 evaluator；只有 native TMR 与 ChronAccRet omission 都失败后才重新讨论。

## 2.1 P0 Risk Gates

这三项必须先于 A/B 的主实验结论闭合：

1. **P0-G1 EventT2M retrain sanity**
   - 风险：eval lane 和 generation lane 都高度依赖 pretrained `hml3d.ckpt`。若 clean retrain 指标与 pretrained 差异过大，说明 backbone reliability 未闭合，两条 lane 的结论都只能写 provisional。
   - 标准：使用 official upstream `tjswodud/EventT2M-codes` clean checkout，按 README 训练 HumanML3D，保存训练命令、commit、数据 hash、GPU、wall time；用同一 eval command 比较 pretrained vs retrain 的 FID、R-Precision、matching score、retrieval YAML。
   - 当前硬件估计：本机 1×RTX 3090 24GB；官方 README 使用 `trainer.devices="0,1"`、batch `128`、repeat_dataset `5`、600 epochs。若单卡 3090 训练，应先尝试 `data.batch_size=64` 或 gradient accumulation，并预期比 2×RTX4090 明显更慢。
2. **P0-G2 ChronAccRet coverage fairness**
   - 风险：ChronAccRet 有自己的 `event_texts` / `humanml3d_subset`，而 MoDebug 主数据是 `HumanML3D-E`。如果直接交叉验证，coverage 与 bucket 分布会影响公平性。
   - 标准：报告 HumanML3D-E test rows、ChronAccRet evaluable rows、safe_drop_join rows 的 overlap、uncovered rows、event-count bucket 分布；主表只在共同可比集合或经过明确重采样/加权后报告。
3. **P0-G3 Reward-metric fairness**
   - 风险：用与 metric 高度相似的 reward 做训练或 inference-time enhancement，本身不是公平 final comparison。
   - 标准：held-out separation 降级为实验卫生；reward-side metric 只能报告为 development result，final claim 必须来自未参与 tuning/selection/reward 的 evaluator 或 human calibration。

## 3. Current Evidence

### 3.1 Backbone Sanity

Event-T2M self eval 已闭合：

1. `HumanML3D-E overall`
   - `FID = 0.049708280712366104`
   - `R_precision_top_3 = 0.8366379141807556`
2. `HumanML3D-E condition3`
   - `FID = 0.13672851026058197`
   - `R_precision_top_3 = 0.7912946939468384`
3. `HumanML3D official reference`
   - `FID = 0.049953218549489975`
   - `R_precision_top_3 = 0.8469827771186829`

结论：官方 Event-T2M pretrained backbone 接到 HumanML3D-E 后没有数量级崩坏，但这只说明 released checkpoint 在当前 eval command 下可用。clean retrain sanity 未闭合前，不能排除 pretrained/retrain gap，不能把 Event-T2M 当无条件可信根基。

### 3.2 Omission Evidence

native TMR omission dataset eval：

1. 数据：`HumanML3D-E data_test.npy`
2. 样本：multi-event annotation-level `N = 3799`
3. artifact：`linkedCodebases/EventT2M-codes-main/logs/planb_tmr_native_omission_dataset_eval/summary.json`
4. `tmr_gt_pres_full_vs_drop_paired_acc = 0.7043958936562253`
5. `tmr_gt_pres_full_vs_replace_paired_acc = 0.836272703342985`
6. `5plus` bucket 更弱：`tmr_gt_pres_full_vs_drop_paired_acc = 0.6610878661087866`，`tmr_gt_pres_full_vs_replace_paired_acc = 0.7573221757322176`

ChronAccRet omission protocol：

1. artifact：`linkedCodebases/ChronAccRet/output/bert_orig/omission_eval/omission_event.yaml`
2. rows：`linkedCodebases/ChronAccRet/output/bert_orig/omission_eval/omission_rows.jsonl`
3. `N = 2333`
4. `chron_subset_pres_full_vs_drop_paired_acc = 0.7299614230604372`
5. `chron_subset_pres_full_vs_replace_paired_acc = 0.8551221603086155`

结论：omission 现在有两条 retrieval-side signal，可以支撑 side evidence 与 reward 设计前的 consistency check，但不能把任意一条写成 standalone final judge。ChronAccRet 侧还必须补 coverage fairness audit，尤其是 HumanML3D-E test split 与 ChronAccRet subset 的覆盖差异。

### 3.3.1 Safe-Drop Consistency Status

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/join_diagnostics.json`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/summary.json`
3. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/disagreement_cases.jsonl`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/top_cases.md`

当前 consistency 只支持 safe-drop comparable rows：

1. join key：`sample_id/keyid + target_idx + event_count + dropped_event + full_text + drop_text`
2. comparable rows：`1608`
3. overall agreement：`1179 / 1608 = 73.32%`
4. `5plus` agreement：`51 / 80 = 63.75%`
5. safe-drop coverage：vs TMR `42.33%`，vs ChronAccRet `68.92%`

### 3.3.2 Aligned-Replace Consistency Status

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_manifest.jsonl`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/tmr_aligned_replace_summary.json`
3. `linkedCodebases/ChronAccRet/output/bert_orig/aligned_replace_eval/chronaccret_aligned_replace_event.yaml`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_consistency_summary.json`

当前 aligned-replace consistency 使用同一 deterministic replacement manifest：

1. manifest rows：`1608`
2. `tmr_safe_subset_pres_full_vs_aligned_replace_paired_acc = 0.835820895522388`
3. `chron_subset_pres_full_vs_aligned_replace_paired_acc = 0.8538557213930348`
4. row-level agreement：`1313 / 1608 = 0.8165422885572139`
5. `5plus` agreement：`63 / 80 = 0.7875`

限制：

1. aligned-replace consistency 只在 TMR 与 ChronAccRet safe-drop 交集上成立：`1608 / 3799 = 42.33%` TMR rows，`1608 / 2333 = 68.92%` ChronAccRet rows。
2. deterministic replacement 是 evaluator-side cross-check，不是最终 omission judge，也不能外推到 TMR 独有的 `57.67%` rows。

结论：原先 replacement mismatch 缺口已补齐。aligned-replace 仍只是 evaluator-side cross-check，不是 standalone final judge。

### 3.3.3 Lexical Hard-Replace Pilot

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/hard_replace_manifest_summary.json`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_summary.json`
3. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_rows.jsonl`

当前 hard-replace pilot 使用 lexical overlap hard-negative manifest：

1. manifest rows：`512`
2. candidate backend：`lexical`
3. `tmr_gt_pres_hard_replace_lexical_paired_acc = 0.65234375`
4. old `tmr_safe_subset_pres_full_vs_aligned_replace_paired_acc = 0.835820895522388`
5. delta：`-0.18347714552238803`
6. `5plus` hard-replace bucket：`15 / 27 = 0.5555555555555556`

结论：当前 aligned-replace 的高分有 easy-negative 膨胀风险。该 pilot 只是 512-row lexical hard-negative diagnostic；下一步若要写强结论，需要跑 TMR embedding hard-negative 或 ChronAccRet hard-replace cross-check。

### 3.4 Ordering Evidence

ChronAccRet ordering full eval：

1. artifact：`linkedCodebases/ChronAccRet/output/bert_orig/subset_eval/shuffle_event.yaml`
2. full4068 `CAR = 0.6473616473616474`
3. evaluable `2331 / 2333`
4. skipped degenerate `2`
5. subset256 `CAR = 0.673202614379085`

结论：formal ordering evidence 已闭合，当前不扩 ordering。

### 3.5 Generation Observation Artifacts

已完成 artifact：

1. observation pool manifest：`linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/manifest.jsonl`
2. observation pool summary：`linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/summary.json`
3. generation observation schema：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/schema.yaml`
4. schema README：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/README.md`
5. archived feasibility note：[[2026-04-29_modebug-attention-extraction-feasibility]]
6. condition manifest：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/condition_manifest.jsonl`
7. G1/G2 observation：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/observations.jsonl`
8. G1/G2 analysis：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/g1g2_observation_analysis_summary.json`
9. G1/G2 filtering analysis：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/head_filtering_analysis.json`
10. archived MLLM sidecar feasibility：[[2026-04-30_modebug-render-video-mllm-sidecar-feasibility]]

状态：G0 pool 已固定为 `64` 条 HumanML3D-E test split `>=3 events` 样本，包含固定 seed `004965 / 008463 / 001969 / 003245`，其中 `5plus` 高风险 bucket 为 `28` 条。G1/G2 已完成 `256` 条 condition row、`10240` 条 attention metric record；raw cross-attention finite 但偏 diffuse，full normalized entropy mean `0.9962925080675632`，condition-order peak match `0.05234375`。后续 filtering 发现 `observations.jsonl` 没有 `head` / `head_idx` / per-head metric，只有 shape `[2, 8, 25, 11]` 和 head-averaged summary；因此现有 artifact 无法判断少数可用 head subset，G1/G2 当前只能保留为 observation / routing evidence，不进入 reward。

## 4. Roadmap

### 4.1 Evaluator Lane

目标：冻结 external judges，补上 consistency 与 reward/final eval 分离，不继续扩张 evaluator 体系。

1. **E0: Status freeze**
   - 状态：done。
   - 输出：[[2026-04-29_modebug-evaluator-status-summary|Evaluator Status Summary]]。
2. **E1: Join diagnostics + safe-drop consistency**
   - 状态：done。
   - 输出：`linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/join_diagnostics.json`、`summary.json`、`disagreement_cases.jsonl`、`top_cases.md`。
   - 结论：safe-drop comparable rows `1608`，agreement `1179 / 1608 = 73.32%`，`5plus` agreement `51 / 80 = 63.75%`；coverage vs TMR `42.33%`，vs ChronAccRet `68.92%`。
   - 限制：这是 safe-drop consistency，不覆盖 replace corruption。
3. **E2: Held-out eval policy**
   - 状态：done。
   - 输出：[[2026-04-29_modebug-heldout-eval-policy|Held-Out Eval Policy]]。
   - 规则：被用作 reward 的 scorer/protocol 不能同时作为 final main-table evaluator/protocol。
4. **E3: Aligned-replace consistency**
   - 状态：done。
   - 输出：`linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_consistency_summary.json`。
   - 结论：joined rows `1608`，agreement `1313 / 1608 = 81.65%`，`5plus` agreement `63 / 80 = 78.75%`。
   - 限制：这是 replacement corruption 的 evaluator-side cross-check，不是 standalone final judge；coverage 只覆盖 TMR rows 的 `42.33%`。
5. **E3b: Hard-replace stress pilot**
   - 状态：done for lexical 512-row pilot；TMR-embedding hard negative pending。
   - 输出：`linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_summary.json`。
   - 结论：`tmr_gt_pres_hard_replace_lexical_paired_acc = 0.65234375`，比 aligned-replace `0.835820895522388` 低 `0.18347714552238803`；`5plus = 0.5555555555555556`。
   - 限制：只说明 easy-negative 风险成立，不替代正式 evaluator；强结论需 TMR embedding hard-negative 或 ChronAccRet hard-replace。
6. **E4: Full-level safety post-G4**
   - 状态：pending after G4。
   - 规则：G4 产物必须再跑 Event-T2M self eval 作 full-level safety；Event-T2M self eval 不能写成 event-level final judge。

### 4.2 Generation Lane

目标：不等待 eval 侧全部完结，但 generation 侧先做不依赖 reward 的可观测性实验。

1. **G0: Backbone and seed pool**
   - 状态：done。
   - 使用 Event-T2M 官方 checkpoint 与 HumanML3D-E 多事件样本。
   - 输出：`linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/manifest.jsonl` 与 `summary.json`。
2. **G1: Attention observation**
   - 状态：instrumentation + 256-row logging done。
   - 输出：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/observations.jsonl`。
   - 结论：attention weights 可 opt-in 提取，shape 语义为 `[batch, head, motion_patch, event_token]`；但现有落盘 metric 已按 head 聚合，无法做 per-head subset，raw attention entropy 高，暂不适合直接作为 reward feature。
3. **G2: Denoising trajectory observation**
   - 状态：step10 logging done。
   - 输出：同 G1 observation artifact。
   - 结论：已记录 `10` 个 sampling step 的 layer-level cross-attention summary；当前 filtering verdict 为 `blocked_no_per_head_artifact`。若继续内部 attention path，先改 logging 保存 per-head metric，再小规模重跑。
4. **G3: Gradient sensitivity observation**
   - 状态：feasibility confirmed via code analysis；frozen-forward diagnostic implementation pending。
   - 只计算 event condition 对 motion frames 的梯度分布，不更新模型。
   - 限制：默认 `sample_motion()` 被 `@torch.no_grad()` 包住，必须在窄作用域 frozen forward 中局部启用 gradient。
5. **G4: Inference-time guidance MVP**
   - 状态：blocked by G3 and G1/G2 signal filtering。
   - 限制：MVP 先限制在 `3-4` event 样本；`5plus` safe-drop agreement `63.75%`、hard-replace TMR `55.56%`，不足以支撑 reward guidance。
   - 先只接小权重 `R_pres`，`R_ord` 只有在 safety 与 held-out rule 清楚后再接。

### 4.3 Documentation Lane

目标：根目录不再有多份互相竞争的旧路线入口。

1. active docs 只保留 README、roadmap、exec、EventT2M retrain sanity plan、evaluator summary、held-out policy、Paper A plan、Paper B plan。
2. 旧 `Plan B`、PAPO-lite、continuation prompt、review prompt、attention feasibility、MLLM sidecar feasibility、RL primer 进入 `archived/`。
3. active docs 不再引用 archived 文件作为正式入口。

## 5. Go / No-Go Gates

| Gate                  | 必须满足                                                                                                                                                                                                                                     | 不满足时                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| EventT2M retrain sanity | clean upstream retrain 与 official pretrained 在同一 eval command 下差距可解释；记录 command、commit、data hash、GPU、wall time | 两条 lane 暂停 paper-level claim，只保留 pretrained checkpoint diagnostic |
| ChronAccRet fairness | 报告 HumanML3D-E vs ChronAccRet event_texts 的 overlap、uncovered rows、bucket distribution；主表只用共同可比集合或重采样/加权结果 | ChronAccRet 只能作 limited side signal，不能作主表 final evaluator |
| evaluator consistency | E1 safe-drop comparable rows 已报告：`1179 / 1608 = 73.32%`，`5plus = 51 / 80 = 63.75%`；E3 aligned-replace agreement `1313 / 1608 = 81.65%`，`5plus = 63 / 80 = 78.75%`；E3b lexical hard-replace TMR `0.65234375`，`5plus = 0.5555555555555556` | omission 只保留 side evidence；G4 MVP 不进入 `5plus` reward guidance |
| full-level safety     | guidance 后 Event-T2M self eval 的 FID / R-Precision 不显著退化                                                                                                                                                                                 | 降低 reward 权重或回退到 observation-only                             |
| attention sensitivity | G1/G2 raw attention 已完成 `256` condition rows，但 filtering verdict 为 `blocked_no_per_head_artifact`；需 per-head logging 小重跑或 sidecar pilot 后再判断                                                                                             | attention 只做 logging，不做 reward feature                        |
| reward-metric fairness | reward scorer 与 final evaluator 分离；held-out 只作为实验卫生，不写成贡献点 | 不能写成最终主表，只能写 development metric |

## 6. Paper-Safe Claims

### Paper A (EventProbe) 当前可写：

> EventProbe is a human-calibrated diagnostic benchmark for event-level failures in multi-event motion generation. It uses difficulty-controlled event counterfactuals (`drop / hard-replace / shuffle`), targeted human calibration, and a modern baseline failure atlas to show that full-level metrics can miss omission, ordering violation, and hard-negative semantic collapse.

### Paper B (PerceptGuide) 当前可写：

> PerceptGuide is a generation method whose novelty lies in event-marginal reward sensitivity and inference-time diffusion correction. A masked-event perception loss makes the reward depend on individual sub-events, and held-out final evaluation checks whether reward-side gains become real omission / ordering improvements.

### 两篇共同的不可写：

1. 不写“已有完美 event-level evaluator”。
2. 不写“AToM 已作为 MoDebug temporal judge 闭合”。
3. 不写“MotionPatches 是当前 scorer / judge”。
4. 不写“duration 已覆盖”。
5. 不写“MoDebug 是单一 reward guidance 工作”（已拆分为双论文）。

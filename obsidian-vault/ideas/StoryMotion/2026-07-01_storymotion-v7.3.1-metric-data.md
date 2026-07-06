---
title: "StoryMotion Metric Data"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - metric
  - data
  - status/active
aliases:
  - StoryMotion-v6.2-Metric-Data
  - StoryMotion-v7.2-Metric-Data
  - StoryMotion-v7.3.1-Metric-Data
  - StoryMotion-v7.4-Metric-Data
source_notes:
  - "[[2026-06-10_pulp-stage1-continuous-stage2-generator-formal]]"
  - "[[2026-06-29_storymotion-v6.2]]"
  - "[[2026-06-30_storymotion-experiment-metric-comparison]]"
  - "[[2026-07-03_storymotion-v7.3.1]]"
created: 2026-07-01T02:47:56+0800
updated: 2026-07-06T20:35:00+0800
---

## 0. Fair Comparison Rules

> [!abstract] Ledger Scope
> 本页是 StoryMotion v7.3.1 的证据账本，不是设计叙事页。它保留历史 full eval、diagnostic、training-loss 和 evidence-path 记录；是否进入正式最终版由 §0.3 的 evidence role classification 决定。

本页是数据独立页，结论页只应通过 Obsidian 引用这里的表格。表内不使用 aliased wikilink，避免 `|` 破坏 Markdown table。

| group                    | fair comparison                                                              | do not mix as direct ranking                  | use                                       |
| ------------------------ | ---------------------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------- |
| full mixed official      | mixed split `10549` samples、Pulp/StoryMotion official callback、bs64、seed17   | mixed-subset `3279`、pure `4053`、training loss | 主性能、外部 baseline、recent v6/v6.2 对照         |
| pure official            | pure split `4053` samples、同 callback                                         | mixed full                                    | 判断 pure 场景，不外推到 mixed                     |
| tokenizer-cache official | pure `4053` 或旧 mixed-subset `3279`、source-tokenizer-aware cache              | full mixed official 主表                        | 判断新 tokenizer 进入 Stage2 是否可用              |
| Stage1 reconstruction    | frozen Stage1 reconstruction decoded 后跑 official metrics，或 feature-space MSE | Stage2 generated quality                      | 判断 tokenizer upper bound / 表示质量           |
| reliability eval         | 同 run、同 split，只改变 observed human/root condition source 或 noise               | clean-only main table                         | 判断 branch coupling / reliability mismatch |

旧 mixed-subset 不是“只在 eval 阶段没有 formal test”。复查结果是旧 paired camera manifest 只导出 `29779/3279` rows，导致训练 cache、Stage2 train 和 eval 都在 subset 上；full camera manifest 已补到 `94050/10549`，对应 full train / full eval 行已记录在本页。

### 0.1 Experiment Group Index

本节只说明实验目的、setting、核心实现差异和可读结论；具体数值仍以各节原表为准。

| group | sections | comparison purpose | shared setting | core conclusion |
| --- | --- | --- | --- | --- |
| G1 main baselines | §1-§2 | 建立 full mixed / pure 的公平性能锚点，区分 Stage1 upper bound、Stage2 generated quality、external camera completion baseline | official callback；full mixed `10549` 或 pure `4053`；bs64 / seed17 优先 | Stage1 recon 很强；v6 clean completion 强；joint generation 和 generated-source camera reliability 仍弱 |
| G2 Stage1 / tokenizer | §3 | 判断失败是否主要来自 tokenizer reconstruction 上界或 feature MSE | Stage1 recon / tokenizer-aware cache；不与 generated Stage2 直接排名 | 多个 tokenizer 有可用 recon 或低 MSE，但 Stage2 仍 collapse，问题不只是 Stage1 MSE |
| G3 full tokenizer Stage2 | §4-§5 | 复查旧 mixed-subset 结论在 full mixed train/eval 下是否成立 | 5090；full mixed `10549`；source-tokenizer-aware eval；bs64 / seed17 | MoLingo human-only、separate AE/VAE、joint VAE/GRFSQ full train 都不能 promoted |
| G4 branch coupling / reliability | §6 | 验证 observed branch 是否被使用，以及 clean condition 能否外推到 noisy/generated condition | 同 run / 同 split 改 observed source；含 P2a/P2b 和 latent diagnostics | branch 被使用，但 reliability mismatch 与 sampler mismatch 仍存在 |
| G5 visualization | §7 | 用 qualitative render 检查 Stage1/Stage2 joint tokenizer 与生成结果是否有明显视觉失败 | 2026-07-01 joint tokenizer / Stage2 vis manifest | 已有少量 Stage1/Stage2 joint 可视化，但缺少 v7.2 / H2C / MoLingo / CP 组间对比闭环 |
| G6 v7.2 E0-E6 | §8.1-§8.3 | 检验 TextRoleRouter、SoftSource、TrustGate、Reliability FT、RelationSurrogate、camera-safe FT 是否修复 v6.4 clean/noise/text 问题 | isolated `StoryMotion_v72_20260702`；full mixed `10549`；official camera/human/joint rows | E4/E6 推动 tradeoff，但 clean camera 远弱于 E0；TrustGate 有作用但近饱和，不能说明问题解决 |
| G7 clean-preserving CP | §8.4-§8.5 | 从 E0 clean anchor 或 E4 tradeoff 出发，检验 clean-preserving reliability finetune 是否形成 Pareto improvement | full mixed `10549`；camera clean 与 observed noise `0.15` | CP1/CP2 保住 clean 但 noisy 不改善；CP3 回拉 clean 但损失 E4 noisy gain |
| G8 asymmetric H2C / RF | §9 | 检验非对称 H2C contract 和 MoLingo FullRF H2C 是否比 v7.2 局部补丁更有前景 | 4090；full mixed `10549`；official camera callback；bs64 / seed17 | H2C matched condition 很强；FullRF+p2b 是当前最好 clean/noisy 折中，但 generated replay 仍未验证 |
| G9 CondMDI RF process ablation | §10 | 检验只把 CondMDI process 从 diffusion 换成 RF 后三模式是否保持 | 5090；full mixed `10549`；official callbacks；bs64 / seed17；50-step RF Euler | clean camera/human completion 保持强；joint generation 明显退化，不能替代 diffusion baseline |
| G10 v7.3.1 task/source schedule | §11 | 检验 CLIP task instruction、one-hot task、clean source、reliability schedule 的四组组合是否解决 StoryMotion 核心问题 | 5090；CondMDI + diffusion；full mixed `10549`；official callbacks；bs64 / seed20260613 | one-hot reliability 有 joint / framing 改进信号，但仍弱于旧 clean unified baseline；核心问题未解决 |
| G11 v7.4 causal asymmetry | §13 | 检验 raw camera latent dependency、最小 asymmetric human-input shuffle 修法、以及 stronger asymmetry closed-loop smoke | 5090；full mixed `10549` for rejected shuffle；32-sample official smoke for `human_text` / composed JOINT | minimal shuffle repair rejected; explicit `H=P(H|text_h), C=P(C|H,text_c)` path now passes execution smoke but still needs real human-text long training |

### 0.2 Per-Experiment Purpose Tables

#### G1 Main Baselines

| experiment | target question | key implementation / setting | core readout |
| --- | --- | --- | --- |
| GT human | official metric reference | GT human decoded through official evaluator | human oracle, not a generated model |
| Pulp Stage1 recon | Stage1 AE upper bound | frozen official Stage1 reconstruction decoded then evaluated | human/camera upper bound strong |
| StoryMotion v6 unified | current clean completion and joint generated anchor | branch-mask Stage2 on Pulp latent contract | clean completion strong; joint weaker |
| Human / camera specialists | single-task capacity control | specialist Stage2 rows | specialists are strong clean controls |
| PulpMotion Stage2 no-Aux / Aux | external generated joint baseline | Pulp official Stage2 rerun | generated joint baseline, not completion |
| E.T./DIRECTOR root-only / replay | camera completion external diagnostic | GT/root condition vs generated-human replay | clean condition strong; generated-source replay collapses |

#### G2 Stage1 / Tokenizer

| experiment | target question | key implementation / setting | core readout |
| --- | --- | --- | --- |
| Pulp Stage1 three-mode recon | official AE upper bound | human/camera/joint recon on pure and mixed | Pulp latent contract itself is strong |
| source tokenizer recon upper bounds | whether new tokenizers can preserve decoded geometry | separate AE/VAE, MoLingo VAE, HFSQ/GRFSQ; some no-z GT diagnostic | recon can look usable while Stage2 still fails |
| feature-space MSE / loss auxiliary | whether low train loss predicts official quality | train/val feature losses and KL/code usage | MSE is insufficient for generated quality claims |

#### G3 Full Tokenizer Stage2

| experiment | target question | key implementation / setting | core readout |
| --- | --- | --- | --- |
| MoLingo human-only | whether MoLingo source tokenizer rescues human Stage2 | full mixed train/eval | negative |
| separate AE no-z | whether deterministic separate tokenizer helps | full mixed train/eval with GT-z diagnostic context | negative |
| separate VAE with-z | whether native 9D separate VAE helps | full mixed train/eval | negative |
| joint VAE / joint GRFSQ with-z | whether corrected joint tokenizer improves Stage2 generation | full mixed train/eval | negative; GRFSQ slightly better but still far from valid |

#### G4 Branch Coupling / Reliability

| experiment | target question | key implementation / setting | core readout |
| --- | --- | --- | --- |
| P2a matched noise | can matched additive noise improve observed-source robustness | camera/human completion with noise grid | improves matched condition but not general reliability |
| P2b reliability attempts | can reliability-aware training preserve clean and improve corrupted source | generated replay / missing / noise controls | no stable Pareto improvement |
| latent diagnostics | does Stage2 use observed branch and where does sampler fail | branch swap, visible shuffle, one-step vs recursive sampler | observed branch matters; recursive sampler mismatch is real |

#### G6 v7.2 E0-E6

| experiment | specific goal | core implementation / modification | core conclusion |
| --- | --- | --- | --- |
| E0 baseline | reproduce v6.4 clean anchor and noisy failure | no new model change; camera P2b retry | clean strong, noisy source collapse reproduced |
| E1 TextRoleRouter | test whether camera/human text role separation increases text sensitivity without killing clean | task/text router + task embedding | clean camera regresses; text intervention remains weak |
| E2 SoftSource+TrustGate | test soft observed conditioning plus source metadata gate | soft replacement + TrustGate/source metadata | cleaner than E1 but still far below E0 |
| E3 Reliability FT | test corruption schedule for source reliability | E2 checkpoint + source corruption finetune | noise improves modestly; framing/clean still weak |
| E4 RelationSurrogate | test explicit relation conditioning | source pooled relation condition / surrogate probe | best v7.2 tradeoff, still not enough |
| E5 TrustGate probe | test whether metadata gate is used or decorative | correct / wrong / missing tag probes across timestep and sigma | measurable but near-saturated gate |
| E6 camera-safe FT | test whether camera-heavy finetune can recover clean while keeping E4 gains | E4/E-series finetune with camera-safe emphasis | joint slightly improves, camera clean worse than E4 |

#### G7 Clean-Preserving CP

| experiment | specific goal | core implementation / modification | core conclusion |
| --- | --- | --- | --- |
| CP1 low-rel | preserve E0 clean while adding weak reliability path | low-strength soft source / trust / relation, camera-only | clean preserved, noisy unchanged |
| CP2 mid-rel | increase self-condition/reliability strength from E0 | stronger schedule, camera-only | clean preserved, noisy still E0-level collapse |
| CP3 clean-heavy | pull E4 back toward clean | E4 checkpoint + clean-heavy training | improves clean relative to E4 but loses noisy gain |

#### G8 Asymmetric H2C / RF

| experiment | specific goal | core implementation / modification | core conclusion |
| --- | --- | --- | --- |
| H2C minimal clean | test whether fixed human source to camera-only generator can match clean anchor | fixed human latent condition, predict camera latent only, clean source | strong matched clean |
| H2C minimal noisy015 | test whether same H2C contract can learn matched noisy source | fixed noisy human source, predict camera latent only | strong matched noisy but clean collapses |
| MoLingo FullRF clean | test whether RF + MoLingo-style backbone improves clean H2C | rectified-flow H2C with MoLingo-style transformer | clean strong, noisy collapse remains |
| MoLingo FullRF noisy015 | test matched noisy RF H2C | noisy source training | matched noisy works, clean collapses |
| MoLingo FullRF p2b | test clean/noisy mixture compromise | reliability mixture training under FullRF H2C | best current Pareto, still not generated-replay proof |

#### G9 CondMDI RF Process Ablation

| experiment | specific goal | core implementation / modification | core conclusion |
| --- | --- | --- | --- |
| CondMDI + RF clean | isolate diffusion vs RF while keeping CondMDI backbone | `rectified_flow` process, 50-step RF Euler, same full mixed official eval tasks | preserves clean camera/human completion but damages joint generation |

### 0.3 Evidence Role Classification For v7.3.1

本节用于区分“正式最终版证据”和“诊断证据”。后续 StoryMotion 正式版实验只应从 `formal baseline`、`formal ablation`、`candidate core` 三类继续推进；`diagnostic` 只用于解释失败和缩小搜索空间。

| evidence group | role for next paper | keep / stop | reason |
| --- | --- | --- | --- |
| StoryMotion v6 / CondMDI + diffusion full mixed three-mode | formal baseline | keep | full `10549` official eval，覆盖 `JOINT / H2C / C2H`，也是当前最自然 edit baseline |
| v7.3.1 e3 one-hot reliability full three-mode | improvement signal | keep as candidate, not promoted | full `10549` official eval；相对 e2 clean one-hot 改善 joint FDCLaTr / F1 / Out，但仍显著弱于 StoryMotion v6 clean unified baseline |
| v7.4 asym human-input shuffle | negative core repair | reject as method, keep as mechanism evidence | full `10549` official eval；camera completion improves but JOINT FDTMR / FDCLaTr / F1 all regress vs e3 |
| v7.3.1 e2 one-hot clean full three-mode | clean-source ablation | keep | full `10549` official eval；clean H2C 强于 e3，但 joint 仍弱于 v6 baseline，证明 clean completion 不能代表 StoryMotion core |
| v7.3.1 e0/e1 CLIP instruction full three-mode | negative ablation | stop naive CLIP route | full `10549` official eval；naive CLIP projection regresses against one-hot under both clean and reliability schedules |
| CondMDI + RF full mixed three-mode | formal ablation | keep as ablation | full `10549` official eval，isolates process swap；结论是 RF 保 completion 但伤 joint |
| MoLingo FullRF p2b H2C | candidate core | keep for H2C robustness | clean/noisy Gaussian H2C Pareto 最好，但还缺 generated replay 和三模式 |
| H2C minimal clean/noisy specialists | diagnostic | stop as method, keep as proof | 证明 H2C contract learnable；cross-source collapse 排除 single-source specialist |
| v7.2 E1-E6 | diagnostic | stop local patch line | gate/router/relation 能移动 tradeoff，但 clean anchor 与 noisy robustness 都未闭合 |
| CP1/CP2/CP3 | diagnostic | stop local patch line | clean-preserving FT 保 clean 但不修 noisy；从 E4 回拉 clean 会丢 noisy gain |
| Stage1 / tokenizer / feature-loss sweeps | diagnostic | stop broad tokenizer sweep | 解释 loss / reconstruction 与 Stage2 generation 脱钩；不直接产生正式方法 |
| E.T./DIRECTOR clean/replay | external diagnostic | keep for motivation only | 支持 clean oracle camera completion 不能外推到 generated-source condition |
| generated replay source train/eval | missing core | must add | final robustness claim 的必要证据 |
| edit span train/eval | missing core | must add | StoryMotion 作为可编辑生成框架的必要证据 |

### 0.4 Backbone / Process Four-Quadrant Status

| backbone | process | training metric status | official metric status | v7.3.1 decision |
| --- | --- | --- | --- | --- |
| CondMDI | diffusion | final train loss `0.0148`; camera `0.00049`, human `0.00356`, joint `0.04029` | full three-mode `10549`; camera FDCLaTr `14.50`, F1 `0.638`; joint FDTMR `155.73`, FDCLaTr `85.70`, F1 `0.374`, Out `7.9%` | current unified / edit baseline |
| CondMDI | RF | final train loss around `0.063`; camera `0.015`, human `0.030`, joint `0.146` | full three-mode `10549`; camera FDCLaTr `11.99`, F1 `0.637`; joint FDTMR `206.89`, FDCLaTr `219.36`, F1 `0.159`, Out `10.4%` | process ablation only |
| MoLingo-style H2C | diffusion | no valid H2C diffusion run in current ledger / remote train dirs | missing | optional only for disentanglement |
| MoLingo-style H2C | RF | p2b final one-step flow MSE around `0.0575`; validation clean MSE `0.0532`, noisy `0.15` MSE `0.0648` | H2C only `10549`; p2b clean FDCLaTr `22.67`, F1 `0.590`; noisy `0.15` FDCLaTr `40.41`, F1 `0.452` | H2C robustness candidate, not unified final |

## 1. Full Mixed Main Comparison

口径：full mixed test `10549` samples；Pulp/StoryMotion official callback；bs64；seed17。E.T./DIRECTOR 只作为 camera completion external baseline：GT/root condition 行与 clean camera completion 可比，generated-human replay 行是 reliability 诊断，不是完整 joint generation baseline。

| model                        | phase               | split | task   | samples | FDTMR↓ |  TMR↑ |  HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ |   F1↑ |  Out↓ | RootFrame↑ | MPJPE↓ | verdict                                              |
| ---------------------------- | ------------------- | ----- | ------ | ------: | -----: | ----: | -----: | -------: | -----: | ----: | ----: | ----: | ---------: | -----: | ---------------------------------------------------- |
| GT human                     | reference           | mixed | human  |   10549 |  -0.00 | 17.71 | 100.0% |        - |      - |     - |     - |     - |          - |      - | oracle human reference                               |
| Pulp official Stage1 recon   | upper-bound         | mixed | human  |   10549 | 124.46 | 18.17 |  85.4% |        - |      - |     - |     - |     - |          - |      - | frozen AE reconstruction upper bound                 |
| Pulp official Stage1 recon   | upper-bound         | mixed | camera |   10549 |      - |     - |      - |    15.51 |  58.10 | 87.2% | 0.670 |     - |          - |      - | frozen AE reconstruction upper bound                 |
| Pulp official Stage1 recon   | upper-bound         | mixed | joint  |   10549 | 124.46 | 18.17 |  85.4% |    15.51 |  58.10 | 87.2% | 0.670 |  4.6% |          - |      - | Stage1 upper bound, not generated Stage2             |
| StoryMotion v6 unified       | recent-main         | mixed | human  |   10549 | 126.71 | 18.17 |  84.6% |        - |      - |     - |     - |     - |          - |  0.088 | valid clean completion row                           |
| StoryMotion v6 unified       | recent-main         | mixed | camera |   10549 |      - |     - |      - |    14.50 |  54.85 | 87.1% | 0.638 |     - |          - |  0.085 | valid clean completion row                           |
| StoryMotion v6 unified       | recent-main         | mixed | joint  |   10549 | 155.73 | 23.95 |  36.4% |    85.70 |  33.52 | 62.8% | 0.374 |  7.9% |          - |  0.194 | joint weaker than clean completion                   |
| Human specialist             | recent-main         | mixed | human  |   10549 | 125.28 | 18.24 |  84.8% |        - |      - |     - |     - |     - |          - |  0.087 | single-task human baseline                           |
| Camera specialist            | recent-main         | mixed | camera |   10549 |      - |     - |      - |    14.33 |  57.03 | 86.6% | 0.659 |     - |          - |  0.085 | single-task camera baseline                          |
| PulpMotion Stage2 no-Aux wz0 | baseline            | mixed | joint  |   10549 | 377.36 | 23.36 |  10.4% |    88.42 |  31.31 | 50.5% | 0.350 | 26.6% |          - |      - | Pulp official no-Aux rerun; generated joint baseline |
| PulpMotion Stage2 wz2 probe  | inference-probe     | mixed | joint  |   10549 | 709.60 | 22.11 |   2.5% |   440.27 |  15.15 |  9.5% | 0.162 |  9.4% |          - |      - | projection CFG probe, not promoted                   |
| E.T./DIRECTOR root-only      | external            | mixed | camera |   10549 |      - |     - |      - |    14.51 |  54.84 | 87.0% | 0.638 |     - |      81.5% |  0.085 | clean GT/root condition strong                       |
| E.T./DIRECTOR replay         | external-diagnostic | mixed | camera |   10549 |      - |     - |      - |    92.24 |  33.31 | 62.8% | 0.375 |     - |      27.3% |  0.194 | generated-human condition collapses                  |

读数：

- Pulp official Stage1 reconstruction 的 mixed joint upper bound 是 FDTMR `124.46`、FDCLaTr `15.51`、Out `4.6%`；它说明官方 AE 表示很强，但不是 generated Stage2。
- StoryMotion v6 clean human/camera completion 接近 Pulp official Stage1 upper bound；joint generation 明显弱于 completion，尤其 camera FDCLaTr `85.70`、F1 `0.374`。
- E.T./DIRECTOR clean GT/root camera 行与 StoryMotion clean camera 行同量级，但同样的 external camera baseline 在 generated-human replay 下退化到 FDCLaTr `92.24`、RootFrame `27.3%`。这支持 branch reliability 问题，不支持“clean camera completion 可外推到 generated-human condition”。

## 2. Pure Official Rows

Pure split 只与 pure 行比较，不与 full mixed 主表直接排名。

| model | phase | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | MPJPE↓ | verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Pulp official Stage1 recon | upper-bound | pure | human | 4053 | 109.34 | 15.94 | 92.4% | - | - | - | - | - | - | pure Stage1 upper bound |
| Pulp official Stage1 recon | upper-bound | pure | camera | 4053 | - | - | - | 17.66 | 60.53 | 84.5% | 0.776 | - | - | pure Stage1 upper bound |
| Pulp official Stage1 recon | upper-bound | pure | joint | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% | - | pure Stage1 upper bound |
| StoryMotion v6 unified | recent-main | pure | human | 4053 | 111.14 | 16.00 | 91.9% | - | - | - | - | - | 0.082 | pure completion strong |
| StoryMotion v6 unified | recent-main | pure | camera | 4053 | - | - | - | 23.36 | 58.41 | 83.6% | 0.763 | - | 0.079 | pure completion strong |
| StoryMotion v6 unified | recent-main | pure | joint | 4053 | 137.12 | 21.25 | 46.4% | 91.47 | 44.46 | 61.3% | 0.594 | 6.9% | 0.195 | joint still weaker |
| PulpMotion Stage2 no-Aux | baseline | pure | joint | 4053 | 377.55 | 20.60 | 15.0% | 93.02 | 36.55 | 49.8% | 0.489 | 38.4% | - | generated joint baseline |
| PulpMotion Stage2 Aux | baseline | pure | joint | 4053 | 419.24 | 21.69 | 14.6% | 90.62 | 38.90 | 44.8% | 0.520 | 27.1% | - | generated joint baseline |

## 3. Stage1 Reconstruction And Ablation

### 3.1 Pulp Official Stage1 Three-Mode Reconstruction

口径：`runs/eval/pulpmotion_core_bs64_20260625/stage1/*_reconstruction_bs64.json`，frozen official autoencoder reconstruction decoded 后跑 official metrics。它是 Stage1 upper bound，不是 Stage2 generation。

| tokenizer | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | readout |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Pulp official Stage1 recon | pure | human | 4053 | 109.34 | 15.94 | 92.4% | - | - | - | - | - | human reconstruction strong |
| Pulp official Stage1 recon | pure | camera | 4053 | - | - | - | 17.66 | 60.53 | 84.5% | 0.776 | - | camera reconstruction strong |
| Pulp official Stage1 recon | pure | joint | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% | three-mode upper bound strong |
| Pulp official Stage1 recon | mixed | human | 10549 | 124.46 | 18.17 | 85.4% | - | - | - | - | - | human reconstruction strong |
| Pulp official Stage1 recon | mixed | camera | 10549 | - | - | - | 15.51 | 58.10 | 87.2% | 0.670 | - | camera reconstruction strong |
| Pulp official Stage1 recon | mixed | joint | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% | three-mode upper bound strong |

### 3.2 Source Tokenizer Official Reconstruction Upper Bounds

这些是 frozen Stage1 reconstruction 的 official metric，不是 Stage2 generated rows。no-z camera/joint 行使用 GT-z passthrough diagnostic，因此能读 camera semantic/framing upper bound，但不能说明 tokenizer 自己学会 z-depth。

| tokenizer | split | samples | task | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | F1↑ | Out↓ | z policy | Stage2 result |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| separate AE no-z | mixed-subset | 3279 | joint | 1360.39 | 10.524 | 2.71 | 66.26 | 0.878 | 20.3% | GT-z diagnostic | full mixed Stage2 still collapses |
| separate AE no-z | mixed-subset | 3279 | human | 1360.39 | 10.524 | - | - | - | - | GT-z diagnostic | full mixed Stage2 human weak |
| separate AE no-z | mixed-subset | 3279 | camera | - | - | 2.71 | 66.26 | 0.878 | - | GT-z diagnostic | full mixed Stage2 camera weak |
| separate VAE with-z | mixed-subset | 3279 | joint | 1364.23 | 10.505 | 4.75 | 64.87 | 0.842 | 20.0% | native 9D | full mixed Stage2 collapses |
| separate VAE with-z | mixed-subset | 3279 | human | 1364.23 | 10.505 | - | - | - | - | native 9D | full mixed Stage2 human weak |
| separate VAE with-z | mixed-subset | 3279 | camera | - | - | 4.75 | 64.87 | 0.842 | - | native 9D | full mixed Stage2 camera weak |
| MoLingo VAE no-z | mixed-subset | 3279 | joint | 1366.94 | 10.409 | 11.51 | 63.85 | 0.813 | 20.5% | GT-z diagnostic | human-only Stage2 weak |
| HFSQ wscale no-z | mixed-subset | 3279 | joint | 1467.92 | 6.690 | 67.60 | 47.73 | 0.585 | 18.9% | GT-z diagnostic | Stage2 weak |
| GRFSQ bs128 no-z | mixed-subset | 3279 | joint | 1359.42 | 8.309 | 140.01 | 45.10 | 0.592 | 19.8% | GT-z diagnostic | Stage2 weak |

### 3.3 Feature-Space MSE / Loss Auxiliary

MSE/loss 只能做辅助诊断。它解释“训练 loss 看起来收敛”为什么不能直接等同 official metric：loss 在 normalized feature space 内，official metric 是 decoded human/camera 后的 TMR/CLaTr/projection/caption score。

| tokenizer                    | split        | samples |   step |   total↓ | human MSE↓ | camera MSE↓ | joint MSE↓ | KL / code usage             | readout                                                    |
| ---------------------------- | ------------ | ------: | -----: | -------: | ---------: | ----------: | ---------: | --------------------------- | ---------------------------------------------------------- |
| separate VAE no-z            | mixed-subset |    3279 | 200000 | 0.001170 |   0.001486 |    0.000854 |          - | -                           | feature MSE strong; not enough for Stage2                  |
| separate AE no-z             | mixed-subset |    3279 | 116500 | 0.002174 |   0.001469 |    0.000933 |          - | -                           | deterministic separate AE reconstructs, Stage2 still fails |
| separate VAE with-z          | mixed-subset |    3279 | 116500 |    0.004 |      0.002 |       0.002 |          - | KL `2.696`                  | official upper bound strong; Stage2 still weak             |
| Pulp joint VAE with-z KL     | mixed-subset |    3279 | 110000 | 0.007822 |   0.003893 |    0.008252 |          - | KL `3.689679`               | KL joint recon weaker than deterministic AE                |
| Pulp joint VAE with-z KL     | mixed-subset |    3279 | 116500 | 0.007844 |   0.003877 |    0.008260 |          - | KL `3.894135`               | last similar to best                                       |
| corrected joint VAE with-z   | mixed full   |   10549 | 144000 | 0.003617 |   0.001752 |    0.005145 |   0.003448 | KL `29.66`                  | Stage1 recon usable; Stage2 collapses                      |
| corrected joint GRFSQ with-z | mixed full   |   10549 | 245000 | 0.009264 |   0.004162 |    0.292299 |   0.148231 | active `1000`, ppl `144.28` | mixed camera recon weak; Stage2 negative                   |
| corrected joint VAE with-z   | pure         |    4053 | 142000 | 0.001932 |   0.002537 |    0.000338 |   0.001438 | KL `3.05`                   | pure Stage1 clean                                          |
| corrected joint GRFSQ with-z | pure         |    4053 | 140000 | 0.003852 |   0.003944 |    0.002418 |   0.003181 | active `1000`, ppl `83.48`  | pure Stage1 clean enough                                   |
| separate GRFSQ longtrain     | mixed-subset |    3279 | 406000 | 0.601149 |   0.007874 |    1.194424 |          - | -                           | mixed camera feature MSE very weak                         |
| separate HFSQ                | mixed-subset |    3279 | 115000 | 0.813651 |   0.022907 |    1.604395 |          - | -                           | mixed camera feature MSE worse                             |

读数：

- `separate AE no-z` 同时有低 feature MSE 和很强 official reconstruction upper bound，但 Stage2 full mixed 仍 collapse；因此“loss 收敛”不能解释 Stage2 可生成。
- `corrected joint VAE with-z` mixed full Stage1 feature reconstruction 不差，但 Stage2 full mixed TMR 归零、Out 接近 `100%`；这指向 Stage2 对 latent geometry/contract 的适配失败，而不是单纯 Stage1 MSE 不收敛。
- `corrected joint GRFSQ with-z` pure Stage1 可用，但 mixed full camera MSE `0.292299` 明显偏高；它的 Stage2 比 joint VAE 略好，仍远离有效 camera/joint rows。

## 4. Full Mixed Official Eval 2026-07-01

口径：5090 上使用 `scripts/storymotion_official_full_eval.py` / source-tokenizer-aware eval，`batch_size=64`、`seed=17`、`num_steps=50`、`cfg_scale=1.0`、`eta=0.0`，full mixed test `10549` samples。

| model               | phase      | split | task   | samples |  FDTMR↓ |   TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ |   F1↑ |   Out↓ | RootFrame↑ | MPJPE↓ | verdict                                                 |
| ------------------- | ---------- | ----- | ------ | ------: | ------: | -----: | ----: | -------: | -----: | ----: | ----: | -----: | ---------: | -----: | ------------------------------------------------------- |
| MoLingo human-only  | full-train | mixed | human  |   10549 | 2396.07 |  4.112 | 0.04% |        - |      - |     - |     - |      - |      12.1% |  0.344 | negative; full train does not rescue human baseline     |
| separate AE no-z    | full-train | mixed | human  |   10549 | 2147.78 |  5.547 | 0.03% |        - |      - |     - |     - |      - |       6.0% |  0.385 | negative                                                |
| separate AE no-z    | full-train | mixed | camera |   10549 |       - |      - |     - |   676.56 |  2.794 | 1.00% | 0.084 |      - |       6.2% |  0.384 | negative                                                |
| separate AE no-z    | full-train | mixed | joint  |   10549 | 2157.12 |  5.669 | 0.00% |   662.84 |  3.074 | 1.11% | 0.094 |  95.5% |       6.9% |  0.387 | negative; joint generation collapses                    |
| separate VAE with-z | full-train | mixed | human  |   10549 | 1823.40 |  0.000 | 0.05% |        - |      - |     - |     - |      - |       8.2% |  0.294 | negative; TMR score collapsed                           |
| separate VAE with-z | full-train | mixed | camera |   10549 |       - |      - |     - |   841.65 |  3.884 | 0.69% | 0.099 |      - |       7.5% |  0.295 | negative                                                |
| separate VAE with-z | full-train | mixed | joint  |   10549 | 1863.90 |  0.000 | 0.00% |   885.36 |  3.785 | 0.39% | 0.057 |  99.0% |       7.9% |  0.297 | negative; worse than mixed-subset trend                 |
| joint VAE with-z    | full-train | mixed | human  |   10549 | 2176.30 |  0.000 | 0.06% |        - |      - |     - |     - |      - |       1.9% |  0.237 | negative; Stage2 human collapsed                        |
| joint VAE with-z    | full-train | mixed | camera |   10549 |       - |      - |     - |   959.07 |  3.108 | 0.05% | 0.075 |      - |       1.9% |  0.236 | negative; camera collapsed                              |
| joint VAE with-z    | full-train | mixed | joint  |   10549 | 2250.73 |  0.000 | 0.00% |   989.53 |  3.016 | 0.01% | 0.052 | 100.0% |       1.9% |  0.235 | negative; worst joint row                               |
| joint GRFSQ with-z  | full-train | mixed | human  |   10549 | 1598.73 |  9.887 | 0.02% |        - |      - |     - |     - |      - |      16.5% |  0.218 | negative; better than joint VAE but still weak          |
| joint GRFSQ with-z  | full-train | mixed | camera |   10549 |       - |      - |     - |   580.22 |  5.846 | 3.24% | 0.091 |      - |      16.4% |  0.218 | negative                                                |
| joint GRFSQ with-z  | full-train | mixed | joint  |   10549 | 1648.84 | 10.164 | 0.01% |   663.60 |  5.790 | 2.15% | 0.086 |  99.6% |      16.2% |  0.218 | negative; does not rescue joint source-tokenizer Stage2 |

## 5. Mixed-Subset To Full Readout

这张表只比较同一实验族的趋势，不把 subset 与 full 当作公平排名。结论是：旧 mixed-subset 结果不是“eval 少跑 formal test”造成的偶然缺口；补 full train/full eval 后，MoLingo、separate AE no-z、separate VAE with-z 仍不能 promoted。

| experiment                 | old mixed-subset row                                           | full mixed row                                                  | readout                                      |
| -------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------- |
| MoLingo human-only human   | `3279` samples, FDTMR `2353.96`, TMR `4.466`, HCov `0.1%`      | `10549` samples, FDTMR `2396.07`, TMR `4.112`, HCov `0.04%`     | full train does not improve baseline quality |
| separate AE no-z human     | `3279` samples, FDTMR `2018.28`, TMR `4.450`, HCov `0.1%`      | `10549` samples, FDTMR `2147.78`, TMR `5.547`, HCov `0.03%`     | still negative                               |
| separate AE no-z camera    | `3279` samples, FDCLaTr `623.87`, CLaTr `8.476`, F1 `0.074`    | `10549` samples, FDCLaTr `676.56`, CLaTr `2.794`, F1 `0.084`    | still far from valid camera rows             |
| separate AE no-z joint     | `3279` samples, FDTMR `2031.69`, FDCLaTr `583.11`, Out `93.7%` | `10549` samples, FDTMR `2157.12`, FDCLaTr `662.84`, Out `95.5%` | joint remains collapsed                      |
| separate VAE with-z human  | `3279` samples, FDTMR `1274.72`, TMR `7.076`, HCov `0.6%`      | `10549` samples, FDTMR `1823.40`, TMR `0.000`, HCov `0.05%`     | full mixed is worse                          |
| separate VAE with-z camera | `3279` samples, FDCLaTr `118.77`, CLaTr `38.08`, F1 `0.472`    | `10549` samples, FDCLaTr `841.65`, CLaTr `3.884`, F1 `0.099`    | subset optimism does not transfer            |
| separate VAE with-z joint  | `3279` samples, FDTMR `1316.47`, FDCLaTr `133.95`, Out `39.4%` | `10549` samples, FDTMR `1863.90`, FDCLaTr `885.36`, Out `99.0%` | full joint fails decisively                  |

## 6. Stage2 Branch Coupling Evidence

### 6.1 P2a Matched Noise

口径：StoryMotion v6 P0 clean camera completion 与 matched additive-noise eval；同 mixed full `10549`，只改变 observed human/root noise。human completion 对 observed camera noise 的退化远小于 camera completion 对 observed human/root noise 的退化，因此耦合方向是不对称的。

| observed human/root noise std | camera FDCLaTr↓ | camera CLaTr↑ | camera CCov↑ | camera F1↑ |
| ---: | ---: | ---: | ---: | ---: |
| 0.00 | 14.50 | 54.85 | 87.1% | 0.638 |
| 0.05 | 22.02 | 53.15 | 85.6% | 0.625 |
| 0.10 | 51.89 | 48.66 | 80.2% | 0.573 |
| 0.15 | 96.87 | 43.54 | 70.1% | 0.503 |
| 0.30 | 216.79 | 32.96 | 46.7% | 0.360 |
| 0.50 | 303.00 | 25.68 | 31.0% | 0.278 |

### 6.2 P2b Reliability Attempts

P2b v1 对 noisy condition 有效，但 clean condition 退化；P2b v2 clean-preserve 部分修复 clean drop，但仍未回到 P0 clean。

| model | condition | samples | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | RootFrame↑ | MPJPE↓ | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| P0 neutral | clean GT human/root | 10549 | 14.50 | 54.85 | 87.1% | 0.638 | - | 0.085 | clean baseline |
| P0 noise 0.15 | observed human/root noisy | 10549 | 96.87 | 43.54 | 70.1% | 0.503 | 78.1% | 0.086 | camera fragile |
| P0 noise 0.30 | observed human/root noisy | 10549 | 216.79 | 32.96 | 46.7% | 0.360 | 73.1% | 0.088 | camera fragile |
| P2b v1 clean | clean GT human/root | 10549 | 88.84 | 27.82 | 62.2% | 0.327 | 39.7% | 0.085 | clean drop too large |
| P2b v1 noise 0.15 | observed human/root noisy | 10549 | 30.36 | 40.73 | 77.7% | 0.458 | 68.9% | 0.086 | noisy condition improved |
| P2b v1 noise 0.30 | observed human/root noisy | 10549 | 46.84 | 38.96 | 75.0% | 0.442 | 64.6% | 0.088 | noisy condition improved |
| P2b v2 clean-preserve | clean GT human/root | 10549 | 46.08 | 43.74 | 75.7% | 0.499 | 72.8% | 0.085 | better than v1 clean, still below P0 |

### 6.3 Latent Diagnostic Evidence

这些是 early Stage2 latent diagnostics，不是 official metric；它们用来证明分支条件被使用、sampler 与 one-step 训练目标有 mismatch。

| diagnostic | sample scope | key numbers | readout |
| --- | ---: | --- | --- |
| cross-swap nearest-source | Stage1 branch controllability | pass rate `1.000`; self A/B MPJPE `0.1979 / 0.2511` | Stage1 branch 可控，但不等于 Stage2 generated quality |
| visible-branch reliance | mixed visible shuffle | camera delta `+1.1016`; human delta `+1.3672` | completion 不是只靠 text shortcut |
| Mode B camera-latent causal gate | `4096` samples | base human median `0.003662`; camera zero / shuffle / matched-noise median `0.216638 / 0.314891 / 0.774336` | Mode B 依赖 camera latent；未分解 distance / motion 子切片 |
| joint sampler re-eval | `1024` samples | teacher-forced `0.016472`; 1-step `0.292046`; 20-step `0.617884`; 50-step `0.740053` | one-step x0 objective 与 recursive sampler 存在 mismatch |
| full generated eval | `10549` records per job | `branch_jh6ft` joint: r_fpd `0.450`, Out `7.48%`, TMR `18.72`, CLaTr `23.70`, F1 `0.284` | generated eval 可跑通；joint 语义仍弱 |

## 7. Joint Branch Visualization 2026-07-01

| scope | manifest | samples | outputs | note |
| --- | --- | ---: | ---: | --- |
| Stage1 joint tokenizer recon | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1/v6_2_joint_stage1_20260701_rerun/manifest.json` | 4 | 61 files | mixed/pure 各 2 个 sample；GT、joint VAE、joint GRFSQ；fixed/orbit/camera projection + concat |
| Stage2 joint VAE qualitative vis | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_vae_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 | 6 videos | source-tokenizer-aware 4x3 qualitative vis；`joint` / `human_completion` / `camera_completion` |
| Stage2 joint GRFSQ qualitative vis | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_grfsq_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 | 6 videos | source-tokenizer-aware 4x3 qualitative vis；probe `failed=0` |

### 7.1 Visualization Gap / Gradio Update 2026-07-03

缺口：

| group | visualization status | required next step |
| --- | --- | --- |
| v7.2 E1/E2/E3/E4/E6 | no v7.2 visualization manifest found on 5090 StoryMotion root | generate matched sample manifests for E-series joint/completion comparison |
| v7.2 vs v6.2 joint VAE/GRFSQ | v6.2 baselines exist; v7.2 side missing | render shared sample IDs, then register both groups |
| H2C minimal | no qualitative manifest registered | render clean/noisy H2C camera completion cases |
| MoLingo FullRF H2C | no qualitative manifest registered | render clean/noisy/p2b H2C cases |
| CP clean-preserving | no qualitative manifest registered | optional; useful only if comparing clean/noise tradeoff visually |

Gradio update：

- `scripts/storymotion_gradio_render.py` now has a `Compare Runs` tab that aligns selected runs by `sample_id`, uses selected runs as columns, and supports mode/split/view filtering.
- The script and `configs/storymotion_gradio_registry.yaml` were installed on 5090 under `/data/public/ripemangobox/Motion/StoryMotion`.
- 5090 validate can load the current 4 registered runs, but video probing reports `ffprobe not found`; this is an environment-tooling limitation, not a manifest parsing failure.
- Current registry still contains only Stage1 tokenizer and v6.2 Stage2 joint VAE/GRFSQ manifests. Do not claim v7.2 qualitative comparison is closed until new v7.2/H2C/MoLingo manifests are generated and registered.

## 8. StoryMotion v7.2 Official Eval 2026-07-02

口径：`StoryMotion_v72_20260702` isolated run dir；full mixed test `10549` samples；Pulp/StoryMotion official callback；E0/E1 在 4090 `director` 环境，E2-E6 在 5090 `storymotion-director-cu128` 环境。E6 joint 使用并行 joint-only eval 目录取数，避免等待顺序 official eval 重复跑 joint。

### 8.1 Camera Clean / Text / Noise Probe

`text delta` 是 text shuffle 后 `F1_shuffle - F1_clean`。数值越接近 `0`，说明 camera text intervention 越弱。`noise` 使用 `--observed-latent-intervention noise_matched`。

| model | checkpoint / condition | clean FDCLaTr↓ | clean F1↑ | text FDCLaTr↓ | text F1↑ | text delta | noise FDCLaTr↓ | noise F1↑ | clean RootFrame↑ | noise RootFrame↑ | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E0 baseline | v6.4 camera P2b retry | 15.01 | 0.629 | 15.66 | 0.617 | -0.012 | 533.45 | 0.095 | 81.6% | 26.0% | clean anchor; noise collapse reproduced |
| E1 TextRoleRouter | E1 best official | 159.06 | 0.320 | 158.06 | 0.309 | -0.011 | 464.00 | 0.110 | 52.1% | 21.2% | clean camera badly regressed; text still weak |
| E2 SoftSource+TrustGate | E2 best official | 102.35 | 0.366 | 104.02 | 0.350 | -0.016 | 478.31 | 0.113 | 56.7% | 15.9% | better than E1 clean, still far below E0 |
| E3 Reliability FT | E3 best official | 98.53 | 0.344 | 103.18 | 0.303 | -0.041 | 380.25 | 0.133 | 37.8% | 23.0% | improves noise vs E2, hurts framing |
| E4 RelationSurrogate | E4 best official | 77.08 | 0.381 | 81.28 | 0.343 | -0.039 | 375.45 | 0.135 | 43.9% | 25.2% | best v7.2 camera clean/noise, not enough |
| E6 camera-safe FT | E6 camera-heavy FT | 92.24 | 0.368 | 96.65 | 0.335 | -0.033 | 378.47 | 0.131 | 45.2% | 25.1% | camera-safe FT did not beat E4 camera |

读数：

- E4 是 v7.2 系列里最好的 camera clean row，但仍明显弱于 E0/v6.4 clean anchor：FDCLaTr `77.08` vs `15.01`，F1 `0.381` vs `0.629`。
- E3/E4 将 observed-noise collapse 从 E0 的 FDCLaTr `533.45` 降到约 `375-380`，但仍不是可靠 H2C。
- E1-E6 的 text shuffle 退化都不大；dominant camera text 仍没有形成足够强的控制信号。
- E6 camera-heavy finetune 没有修复 clean camera；它不应作为主线提升，只作为反证：简单调 task sampling / corruption strength 不足以恢复 v6.4 clean quality。

### 8.2 Three-Task Official Rows

| model | camera FDCLaTr↓ | camera F1↑ | human FDTMR↓ | human TMR↑ | HCov↑ | joint FDTMR↓ | joint FDCLaTr↓ | joint F1↑ | Out↓ | verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E0 baseline | 15.01 | 0.629 | - | - | - | - | - | - | - | v6.4 camera anchor only |
| E1 TextRoleRouter | 159.06 | 0.320 | 470.73 | 10.23 | 9.4% | 203.82 | 190.84 | 0.208 | 6.9% | failed clean camera gate |
| E2 SoftSource+TrustGate | 102.35 | 0.366 | 601.45 | 9.42 | 6.7% | 208.81 | 147.53 | 0.228 | 11.6% | camera improves vs E1, human weak |
| E3 Reliability FT | 98.53 | 0.344 | 279.23 | 12.54 | 19.4% | 216.77 | 156.19 | 0.224 | 13.5% | human improves, camera framing regresses |
| E4 RelationSurrogate | 77.08 | 0.381 | 211.90 | 14.95 | 26.7% | 199.29 | 106.45 | 0.272 | 14.0% | best v7.2 tradeoff, still below clean anchor |
| E6 camera-safe FT | 92.24 | 0.368 | 260.93 | 13.89 | 22.5% | 188.83 | 104.75 | 0.283 | 13.3% | slightly better joint, worse camera than E4 |

读数：

- E4 improves the v7.2 Pareto front over E1-E3 on camera clean, human clean, and joint camera semantics, but not enough to replace the v6.4 clean H2C path.
- E6 slightly improves joint FDTMR/F1 over E4 (`188.83 / 0.283` vs `199.29 / 0.272`) but worsens camera clean (`92.24 / 0.368` vs `77.08 / 0.381`), so it is not a promoted camera-safe fix.
- Out rate remains worse than earlier v6 joint rows and should not be used alone as a success criterion.

### 8.3 E5 TrustGate Probe

口径：`3 timesteps x 3 sigmas x 2 tasks`，checkpoint `E4 best_eval.pt`。

| task   | mean loss missing-correct | mean loss wrong-correct | gate correct mean | gate missing mean | gate wrong mean | readout                                           |
| ------ | ------------------------: | ----------------------: | ----------------: | ----------------: | --------------: | ------------------------------------------------- |
| camera |                  0.001142 |                0.000607 |          0.999878 |          0.961564 |        0.987759 | gate has measurable effect but is near-saturated  |
| human  |                  0.006210 |                0.005141 |          0.999867 |          0.958916 |        0.986745 | effect stronger than camera, still near-saturated |

读数：

- E5 supports that `source_type/sigma` metadata is not a completely dead variable.
- The gate is numerically saturated close to `1.0`, so E5 alone cannot justify claiming TrustGate solved source reliability.
- Official camera noise probes remain the stronger evidence; they show partial improvement, not resolution.

### 8.4 Clean-Preserving CP Follow-up 2026-07-02

口径：`StoryMotion_v72_20260702` isolated run dir；full mixed test `10549` samples；Pulp/StoryMotion official callback；`camera clean` 与 `observed human/root noise=0.15`。CP1/CP2 从 E0 clean anchor 接续，CP3 从 E4 接续。它们是对 “clean-preserving source conditioning” 的核心验证。

| model                | origin            | training intent                                           | clean FDCLaTr↓ | clean F1↑ | noise 0.15 FDCLaTr↓ | noise 0.15 F1↑ | readout                                          |
| -------------------- | ----------------- | --------------------------------------------------------- | -------------: | --------: | ------------------: | -------------: | ------------------------------------------------ |
| E0 baseline          | v6.4 camera P2b   | clean anchor                                              |          15.01 |     0.629 |              533.45 |          0.095 | clean strong, source noise collapses             |
| E4 RelationSurrogate | v7.2 E4           | best previous v7.2 tradeoff                               |          77.08 |     0.381 |              375.45 |          0.135 | partial noise improvement, clean too weak        |
| CP1 low-rel          | E0 `last.pt`      | low-strength soft source / trust / relation, camera-only  |          15.75 |     0.646 |              547.39 |          0.100 | preserves clean, does not improve noise          |
| CP2 mid-rel          | E0 `last.pt`      | stronger self-condition/reliability schedule, camera-only |          15.50 |     0.634 |              553.73 |          0.098 | preserves clean, noise remains E0-level collapse |
| CP3 clean-heavy      | E4 `best_eval.pt` | pull E4 back toward clean-heavy training                  |          31.55 |     0.497 |              432.89 |          0.120 | recovers some clean, loses much of E4 noise gain |

补充读数：

| model | clean CLaTr↑ | clean precision | clean recall | clean camera-distance error↓ | noise CLaTr↑ | noise precision | noise recall | noise camera-distance error↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CP1 low-rel | 55.92 | 0.941 | 0.780 | 0.222 | 8.60 | 0.150 | 0.273 | 1.279 |
| CP2 mid-rel | 54.84 | 0.940 | 0.767 | 0.229 | 8.77 | 0.150 | 0.288 | 1.215 |
| CP3 clean-heavy | 42.62 | 0.906 | 0.634 | 0.457 | 10.77 | 0.213 | 0.368 | 1.156 |

读数：

- CP1/CP2 证明从 E0 clean anchor 做低/中强度 reliability finetune 可以基本保住 clean H2C：FDCLaTr 仍在 `15-16`，F1 约 `0.63-0.65`。
- CP1/CP2 同时证明这些局部改动没有解决 source reliability：noise `0.15` 仍在 FDCLaTr `547-554`、F1 `0.098-0.100`，与 E0 collapse 同量级。
- CP3 证明从 E4 回拉 clean 可以把 clean 从 `77.08 / 0.381` 改到 `31.55 / 0.497`，但它没有回到 E0/CP1/CP2 clean，且 noise 从 E4 `375.45 / 0.135` 退到 `432.89 / 0.120`。
- 因此 clean-preserving follow-up 没有找到 Pareto improvement。当前实验链支持“核心问题仍未解决”，不支持“v7.2/CP 系列已经形成可 promoted 方法”。

Eval caveat：

- 当前 official eval sampler 没有显式传入 v7.2 `task` / `source_meta`，因此 `TextRoleRouter` 与 `TrustGate/source_meta_mlp` 在 full official eval 中没有按训练时的 source reliability metadata 完整激活。
- 这不影响这些 JSON 作为“当前 checkpoint 在现有 official protocol 下的实际表现”读数；但它削弱了对具体模块机制的因果归因。
- 结论应写成：Stage2 conditioning contract 需要重做；不能写成当前 TrustGate/RelationSurrogate 版本有效。

### 8.5 v7.2 / CP Decision

Current decision:

- Do not promote E1/E2/E3/E4/E6/CP1/CP2/CP3 as the final method.
- Keep E0/CP1/CP2 as clean H2C anchors; keep E4/CP3 only as ablation checkpoints for studying the clean/noise tradeoff.
- The completed experiments support a negative conclusion: local Stage2 patches can move along the clean/noise tradeoff, but have not solved the core StoryMotion problem.
- Do not prioritize task-text CLIP latent, Rectified Flow, or another tokenizer sweep as the next immediate path. The repeated failure is the human-source-to-camera conditioning contract under imperfect source.
- The next research decision is whether to redesign Stage2 conditioning more fundamentally, or pivot the StoryMotion claim away from robust generated-source camera control.

### 8.6 4090 / 5090 v7.2 Joint Rerun Status 2026-07-03

目的：按用户要求把 v7.2 E2/E3/E4/E6 ckpt 同步到 4090 后重新跑 `joint` full official eval，避免只依赖 5090 既有 JSON。

状态：

| run | 4090 bs64 status | effective fair result | note |
| --- | --- | --- | --- |
| E2 SoftSource+TrustGate | OOM at about `4928` records | 5090 `e2_official_20260703/joint.json` | fair bs64, `10549` samples |
| E3 Reliability FT | OOM at about `4928` records | 5090 `e3_official_20260703/joint.json` | fair bs64, `10549` samples |
| E4 RelationSurrogate | not rerun on 4090 after E2/E3 OOM | 5090 `e4_official_20260703/joint.json` | fair bs64, `10549` samples |
| E6 camera-safe FT | not rerun on 4090 after E2/E3 OOM | 5090 `e6_official_joint_parallel_20260702/joint.json` | fair bs64, `10549` samples |

Fairness caveat：

- 4090 `batch_size=64` did not satisfy the requested fair-bs setting for E2/E3 joint eval; the failure mode is CUDA OOM, not metric completion.
- 4090 bs32 partial reruns were stopped and removed after 5090 became free; they are not used as evidence.
- Effective v7.2 E2/E3/E4/E6 joint rows are the existing 5090 fair bs64 full `10549` JSONs, already synced to 4090 as a valid copy.

## 9. Stage2 H2C / MoLingo FullRF Official Eval 2026-07-03

口径：4090 full mixed test `10549` samples；Pulp/StoryMotion official callback；`batch_size=64`、`seed=17`、`num_workers=0`。5090 曾短暂启动 4 条 eval，但按用户要求停止，未产生有效 records；最终有效结果全部来自 4090。4090 与 5090 已同步关键代码与配置，5090 的 MoLingo FullRF ckpt 已 scp 到 4090 后评估。

### 9.1 Minimal H2C

| model                | train source | eval source  | samples | FDCLaTr↓ | CLaTr↑ | CCov↑ |   F1↑ | readout                                               |
| -------------------- | ------------ | ------------ | ------: | -------: | -----: | ----: | ----: | ----------------------------------------------------- |
| H2C minimal clean    | clean        | clean        |   10549 |    15.20 |  57.42 | 0.868 | 0.665 | clean anchor stronger than E0                         |
| H2C minimal clean    | clean        | noisy `0.15` |   10549 |   824.33 |   4.61 | 0.001 | 0.048 | noisy source collapse                                 |
| H2C minimal noisy015 | noisy `0.15` | clean        |   10549 |  1022.65 |   0.00 | 0.002 | 0.055 | clean source collapse                                 |
| H2C minimal noisy015 | noisy `0.15` | noisy `0.15` |   10549 |    26.71 |  51.83 | 0.775 | 0.587 | noisy-specific model works only in matched corruption |

读数：

- Minimal H2C 证明“固定 human source，只预测 camera latent”可以得到很强的 matched-condition camera completion。
- 但 clean-trained 与 noisy-trained 两个模型完全分裂：clean model 在 noisy `0.15` 下 FDCLaTr `824.33`，noisy model 在 clean 下 FDCLaTr `1022.65`。
- 因此 H2C 非对称本身不足以解决 source reliability；它只是把问题暴露得更清楚。

### 9.2 MoLingo FullRF H2C

| model                   | train source | eval source  | samples | FDCLaTr↓ | CLaTr↑ | CCov↑ |   F1↑ | readout                                    |
| ----------------------- | ------------ | ------------ | ------: | -------: | -----: | ----: | ----: | ------------------------------------------ |
| MoLingo FullRF clean    | clean        | clean        |   10549 |    18.59 |  55.85 | 0.845 | 0.651 | clean strong, close to minimal clean       |
| MoLingo FullRF clean    | clean        | noisy `0.15` |   10549 |   625.57 |   4.42 | 0.007 | 0.124 | noisy collapse remains                     |
| MoLingo FullRF noisy015 | noisy `0.15` | clean        |   10549 |   611.09 |   4.01 | 0.007 | 0.101 | clean collapse remains                     |
| MoLingo FullRF noisy015 | noisy `0.15` | noisy `0.15` |   10549 |    31.05 |  41.20 | 0.771 | 0.490 | matched noisy condition works              |
| MoLingo FullRF p2b      | mixed p2b    | clean        |   10549 |    22.67 |  50.49 | 0.807 | 0.590 | best clean/noisy compromise                |
| MoLingo FullRF p2b      | mixed p2b    | noisy `0.15` |   10549 |    40.41 |  37.60 | 0.755 | 0.452 | robust but weaker than matched noisy model |

读数：

- 换成 MoLingo-style FullRF backbone 后，matched clean/noisy 能跑通，但 clean/noisy 分裂仍存在。
- `p2b` 是当前最好的折中：clean FDCLaTr `22.67`、F1 `0.590`，noisy `0.15` FDCLaTr `40.41`、F1 `0.452`。
- `p2b` 相比 clean-only 明显改善 noisy robustness，但相对 clean anchor 仍丢 clean quality；相比 noisy-only 又丢 noisy matched quality。
- 结论应写成：FullRF + p2b 是可保留的下一轮候选 ablation，不足以直接宣称解决 robust generated-source camera control。

### 9.3 2026-07-03 Decision

- Do not claim that replacing Stage2 backbone with MoLingo FullRF alone solves source reliability.
- Keep `stage2_molingo_fullrf_h2c_v64_p2b_20260703` as the current best clean/noisy Pareto checkpoint.
- Treat clean-only and noisy-only models as diagnostic anchors, not final methods.
- Next required evidence is generated-replay source eval, not more Gaussian-noise-only full eval.

### 9.4 Asymmetric Architecture Value Judgement

这里的“非对称架构”指 source human 与 target camera 分工明确的 H2C contract，不等同于 MoLingo、CondMDI 或某一个具体 denoiser。

当前 4090 eval 支持一个谨慎的正结论：

- 有价值：H2C minimal clean 达到 FDCLaTr `15.20` / F1 `0.665`，接近或略强于 E0 clean anchor；H2C minimal noisy015 在 matched noisy 下达到 FDCLaTr `26.71` / F1 `0.587`。这说明“human source 固定、camera 作为主生成目标”的任务定义本身是可学习的。
- 有前景但未解决：MoLingo FullRF p2b 同时保住 clean FDCLaTr `22.67` / F1 `0.590` 与 noisy `0.15` FDCLaTr `40.41` / F1 `0.452`，比 clean-only / noisy-only 的单分布模型更接近可用 Pareto。
- 关键缺口：clean-only 与 noisy-only 的交叉评估仍灾难性 collapse，说明非对称 contract 只是消除了 joint denoiser 中 human/camera 同权竞争的一部分问题，没有自动解决 source reliability 分布迁移。
- 因此路线判断应写成：继续推进非对称架构值得做，但下一轮必须引入 generated replay source 和统一的 clean/noisy/replay source schedule；不能把 H2C 或 FullRF matched-noise 结果直接当成 robust generated-source camera control。

## 10. CondMDI + RF Three-Mode Official Eval 2026-07-04

口径：5090 full mixed test `10549` samples；Pulp/StoryMotion official callbacks；`batch_size=64`、`seed=17`、50-step RF Euler velocity sampler。Checkpoint: `runs/train/stage2/condmdi_stage2_rf_clean_20260703/last.pt` at step `42000`。Eval root: `runs/eval/stage2/condmdi_stage2_rf_clean_20260704_full`。

### 10.1 Three-Mode Summary

| model | samples | camera FDCLaTr↓ | camera CLaTr↑ | camera CCov↑ | camera F1↑ | human FDTMR↓ | human TMR↑ | HCov↑ | joint FDTMR↓ | joint FDCLaTr↓ | joint CLaTr↑ | joint F1↑ | Out↓ | readout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| CondMDI + diffusion | 10549 | 14.50 | 54.85 | 87.1% | 0.638 | 126.71 | 18.17 | 84.6% | 155.73 | 85.70 | 33.52 | 0.374 | 7.9% | old clean unified baseline |
| CondMDI + RF | 10549 | 11.99 | 55.69 | 87.8% | 0.637 | 129.13 | 18.15 | 83.8% | 206.89 | 219.36 | 13.65 | 0.159 | 10.4% | completion preserved, joint regresses |

### 10.2 Per-Task JSON Metrics

| task | evaluated samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | source JSON |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| camera | 10549 | - | - | - | 11.99 | 55.69 | 87.8% | 0.637 | - | `camera/camera.json` |
| human | 10549 | 129.13 | 18.15 | 83.8% | - | - | - | - | - | `human/human.json` |
| joint | 10549 | 206.89 | 14.57 | 29.6% | 219.36 | 13.65 | 42.6% | 0.159 | 10.4% | `joint/joint.json` |

### 10.3 Readout

- RF process is not the bottleneck for clean completion: `CondMDI + RF` camera completion is at least as strong as `CondMDI + diffusion` on FDCLaTr and essentially tied on F1.
- RF process currently hurts joint generation: joint FDTMR, joint FDCLaTr, joint CLaTr, HCov, and F1 all regress materially.
- The follow-up baseline should therefore remain `CondMDI + diffusion` for unified `JOINT / H2C / C2H / edit` experiments.
- `CondMDI + RF` should be retained only as a process ablation unless a later RF training/sampler variant restores joint quality.
- This result supports the claim that edit-oriented StoryMotion should prefer the CondMDI mask/inpainting backbone, but does not support switching the default process from diffusion to RF.

## 11. CondMDI + Diffusion Task / Source Schedule Eval 2026-07-05

口径：5090 full mixed test `10549` samples；Pulp/StoryMotion official callbacks；`batch_size=64`、`seed=20260613`、`num_steps=50`、`cfg_scale=1.0`、`eta=0.0`。训练口径：同一 cache、同一 training steps `82688`、训练 batch `512`、seed `17`、task probs `4/2/3`。四个 run 均有 `train_log.jsonl`、`meta.json`、`last.pt`、`best_eval.pt` 和 TensorBoard event。Eval root: `runs/eval/stage2/v7_3_1/full_10549_last_defaultcfg_20260705`。

e0/e1/e3 的 joint final JSON 来自同 batch `64`、同 seed、同采样配置下的 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 重跑；这只改变 PyTorch allocator 策略，不改变模型、数据、seed、batch 或 sampling。旧 e2 joint 有一次 allocator OOM，最终 e2 joint 已同 allocator setting 重跑完成。

### 11.1 Full Three-Mode Summary With Clean Baseline

| model | task semantic | source schedule | samples | camera FDCLaTr↓ | camera F1↑ | human FDTMR↓ | joint FDTMR↓ | joint FDCLaTr↓ | joint F1↑ | Out↓ | readout |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| StoryMotion v6 / CondMDI + diffusion | legacy task | clean unified | 10549 | 14.50 | 0.638 | 126.71 | 155.73 | 85.70 | 0.374 | 7.9% | old clean unified baseline; still strongest joint among CondMDI diffusion rows |
| e0 | CLIP instruction | clean source | 10549 | 92.38 | 0.414 | 128.81 | 200.87 | 226.06 | 0.164 | 22.4% | naive CLIP clean regresses heavily |
| e1 | CLIP instruction | reliability schedule | 10549 | 34.36 | 0.515 | 182.77 | 249.64 | 204.71 | 0.183 | 12.5% | CLIP + reliability helps camera vs e0 but hurts human/joint |
| e2 | one-hot task | clean source | 10549 | 20.61 | 0.620 | 132.28 | 208.81 | 147.53 | 0.228 | 11.6% | strongest new clean H2C, but joint still far below v6 |
| e3 | one-hot task | reliability schedule | 10549 | 34.62 | 0.512 | 147.60 | 195.85 | 126.91 | 0.253 | 9.0% | best new joint/framing row; improvement signal but not solved |
| CondMDI + RF | legacy task | clean unified | 10549 | 11.99 | 0.637 | 129.13 | 206.89 | 219.36 | 0.159 | 10.4% | RF preserves completion but damages joint |

### 11.2 Delta Against Baselines

| comparison | camera FDCLaTr change | camera F1 change | joint FDCLaTr change | joint F1 change | Out change | conclusion |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| e3 vs e2 | `+14.01` worse | `-0.108` worse | `-20.62` better | `+0.025` better | `-2.6pp` better | reliability schedule gives real joint/framing signal under one-hot |
| e3 vs StoryMotion v6 clean | `+20.12` worse | `-0.126` worse | `+41.21` worse | `-0.121` worse | `+1.1pp` worse | current best v7.3.1 still does not recover old clean unified baseline |
| e2 vs StoryMotion v6 clean | `+6.11` worse | `-0.018` worse | `+61.83` worse | `-0.146` worse | `+3.7pp` worse | clean one-hot preserves H2C moderately, but joint is not solved |
| e3 vs CondMDI + RF | `+22.63` worse | `-0.125` worse | `-92.45` better | `+0.094` better | `-1.4pp` better | diffusion + reliability is better than RF for joint, but worse for clean H2C |

### 11.3 Core Problem Status

- 核心问题没有解决。若以 StoryMotion v6 clean unified baseline 作为同口径 clean reference，e3 的 joint FDCLaTr `126.91` 仍明显弱于 `85.70`，joint F1 `0.253` 仍弱于 `0.374`，Out `9.0%` 仍弱于 `7.9%`。
- 找到了明确但局部的改进信号：在 one-hot task route 下，reliability schedule 把 e2 joint FDCLaTr `147.53` 改到 e3 `126.91`，F1 `0.228` 改到 `0.253`，Out `11.6%` 改到 `9.0%`。
- CLIP task instruction 当前不是改进信号。e0/e1 在 clean 和 reliability schedule 下均弱于 one-hot 对应组，说明 naive CLIP projection 没有形成有效 task control。
- clean H2C 仍不是核心指标代理。e2 的 clean camera FDCLaTr `20.61` / F1 `0.620` 是新四组最好，但 joint 明显弱于 e3，也弱于 v6 clean baseline。
- 下一步不应写成小修。更准确的判断是：保留 `CondMDI + diffusion` 和 edit-compatible mask contract，但需要继续做 source-condition-target contract 的中等偏大改，包括 generated replay bucket、edit-aware mask eval、source-quality curriculum 与机制 audit。只调 CLIP scale、task prompt 或 allocator 不足以解决核心问题。

## 12. Evidence Paths

- session log: `/home/ripemangobox/.codex/sessions/2026/06/30/rollout-2026-06-30T13-49-11-019f1713-09e8-7712-8d35-bffba1f1b25c.jsonl`
- Pulp Stage1 official recon: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/stage1`
- Pulp Stage2 official rerun: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/pulpmotion_official_baseline_20260613` and `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/stage2`
- StoryMotion v6 native baseline: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p0_native_20260625`
- StoryMotion v6 pure baseline: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_pure_dualcol_20260625`
- seed17 tokenizer / E.T. eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_seed17_eval_20260630`
- Stage1 official recon eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_stage1_official_recon_20260630`
- full mixed official eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701`
- joint full mixed official eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_joint_fulltrain_eval_20260701`
- joint Stage1 posthoc eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_joint_stage1_recon_eval_20260701`
- Stage1 ablation eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_resume_20260629/pulp_stage1_ablation_eval`
- P2a matched noise eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2a_matched_noise_20260625`
- P2b reliability eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2b_robustness_20260628` and `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2b_v2_clean_preserve_20260628`
- Stage1 tokenizer visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1/stage1_tokenizers_20260701_rerun`
- H2C minimal full official eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/stage2_h2c_minimal_20260703/full`
- MoLingo FullRF H2C full official eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/stage2_molingo_fullrf_h2c_20260703/full`
- CondMDI + RF full official eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/condmdi_stage2_rf_clean_20260704_full`
- joint Stage1 visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1/v6_2_joint_stage1_20260701_rerun`
- joint Stage2 visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun`
- full camera manifests: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_*_manifest_full_20260630.jsonl`
- v7.2 isolated eval root: `/data/public/ripemangobox/Motion/StoryMotion_v72_20260702/runs/eval/stage2/v7_2`
- v7.2 E0 baseline retry: `runs/eval/stage2/v7_2/e0_baseline_retry_b16_20260703`
- v7.2 E1 official and probes: `runs/eval/stage2/v7_2/e1_official_20260703`, `runs/eval/stage2/v7_2/e1_camera_probes_20260702`
- v7.2 E2 official and probes: `runs/eval/stage2/v7_2/e2_official_20260703`, `runs/eval/stage2/v7_2/e2_camera_probes_20260702`
- v7.2 E3 official and probes: `runs/eval/stage2/v7_2/e3_official_20260703`, `runs/eval/stage2/v7_2/e3_camera_probes_20260702`
- v7.2 E4 official and probes: `runs/eval/stage2/v7_2/e4_official_20260703`, `runs/eval/stage2/v7_2/e4_camera_probes_20260702`
- v7.2 E5 TrustGate probe: `runs/eval/stage2/v7_2/e5_trust_ablation_20260702/trust_probe.json`
- v7.2 E6 camera-safe finetune official and probes: `runs/eval/stage2/v7_2/e6_official_20260702`, `runs/eval/stage2/v7_2/e6_official_joint_parallel_20260702`, `runs/eval/stage2/v7_2/e6_camera_probes_20260702`
- v7.2 training checkpoints: `runs/train/stage2/v7_2/e1_text_role_router_20260702`, `e2_soft_trust_clean_20260702`, `e3_reliability_ft_20260702`, `e4_relation_surrogate_20260702`, `e6_camera_safe_ft_20260702`
- v7.3 clean-preserving CP official eval: `/data/public/ripemangobox/Motion/StoryMotion_v72_20260702/runs/eval/v7_3_core_official_20260702`
- v7.3 clean-preserving CP checkpoints: `/data/public/ripemangobox/Motion/StoryMotion_v72_20260702/runs/train/stage2/v7_3_core/cp1_anchor_last_camera_lowrel_20260702`, `cp2_anchor_last_camera_midrel_20260702`, `cp3_e4_cleanheavy_20260702`
- v7.3.1 e0-e3 train root: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_3_1`
- v7.3.1 e0-e3 full official eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_3_1/full_10549_last_defaultcfg_20260705`
- v7.4 causal asymmetry train root: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_4_core_20260706/asym_human_input_shuffle_e3`
- v7.4 causal asymmetry full official eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_4/asym_human_input_20260706/full_10549_last`
- v7.4 clean human completion reference: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_4/asym_human_input_20260706/baselines/e3_human_completion_1024.json`
- v7.4 stronger asymmetry smoke train root: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_4_core_20260706/human_text_smoke_20step`
- v7.4 stronger asymmetry smoke eval root: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_4/strong_asym_smoke_20260706`
- v7.4 stronger asymmetry first long train: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_4_core_20260706/human_text_full_e3like_82688`
- v7.4 stronger asymmetry human-text gate eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_4/strong_asym_human_text_gates_20260706`
- v7.4 paired render audit: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_4_paired_audit_20260706`
- v7.4 generated-source H2C replay cache: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_4_core_20260706/human_text_replay_cache_final_full_50step`
- v7.4 generated-source H2C replay fine-tune: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_4_core_20260706/h2c_generated_replay_final_ft20k_from_p2b`
- v7.4 generated-source H2C replay eval: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_4/strong_asym_h2c_replay_ft_20260706`

## 13. v7.4 Causal Asymmetry Core Eval 2026-07-06

口径：5090 full mixed test `10549` samples；Pulp/StoryMotion official callbacks；`num_steps=50`、`cfg_scale=1.0`、`eta=0.0`。训练 root: `runs/train/stage2/v7_4_core_20260706/asym_human_input_shuffle_e3`。Eval root: `runs/eval/stage2/v7_4/asym_human_input_20260706/full_10549_last`。

训练改动：`--joint-human-camera-input-mode shuffle`。JOINT camera loss 使用正常 forward；JOINT human loss 使用第二次 forward，其中 camera input channels 在 batch 内 shuffle。Eval/render 合同保持一致：JOINT camera prediction 来自正常 forward，JOINT human prediction 来自 camera-input-shuffled forward，再按 channel 合并。

执行备注：第一次 JOINT eval 使用 batch `64` 时在 `8960/10549` 的 SMPL decode 阶段 OOM，未产生 final JSON。最终有效 JOINT 行来自 batch `32` 完整重跑，输出 `asym_shuffle_joint_full10549_last_bs32.json`。camera/human 行使用 batch `64`。

### 13.1 Full Three-Mode Summary

| model | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | source JSON |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| e3 one-hot reliability | camera | 10549 | - | - | - | 34.62 | 44.97 | 78.2% | 0.512 | - | `e3_onehot_reliability_5090_camera_full10549_last.json` |
| asym human-input shuffle | camera | 10549 | - | - | - | 23.74 | 47.35 | 78.9% | 0.556 | - | `asym_shuffle_camera_full10549_last.json` |
| e3 one-hot reliability | human | 10549 | 147.60 | 18.15 | 76.2% | - | - | - | - | - | `e3_onehot_reliability_5090_human_full10549_last.json` |
| asym human-input shuffle | human | 10549 | 148.18 | 18.83 | 74.5% | - | - | - | - | - | `asym_shuffle_human_full10549_last.json` |
| e3 one-hot reliability | joint | 10549 | 195.85 | 17.96 | 31.6% | 126.91 | 21.08 | 57.5% | 0.253 | 9.0% | `e3_onehot_reliability_5090_joint_full10549_last.json` |
| asym human-input shuffle | joint | 10549 | 204.07 | 17.28 | 25.2% | 143.70 | 17.25 | 45.5% | 0.221 | 10.2% | `asym_shuffle_joint_full10549_last_bs32.json` |

### 13.2 Delta Against e3

| comparison | FDTMR change | HCov change | FDCLaTr change | CCov change | F1 change | Out change | readout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| asym camera vs e3 camera | - | - | `-10.88` better | `+0.7pp` better | `+0.044` better | - | camera completion improves materially |
| asym human vs e3 human | `+0.58` worse | `-1.8pp` worse | - | - | - | - | human completion roughly holds, but no clear recovery |
| asym joint vs e3 joint | `+8.21` worse | `-6.4pp` worse | `+16.79` worse | `-12.0pp` worse | `-0.032` worse | `+1.2pp` worse | JOINT degrades; repair rejected |

### 13.3 Readout

- `asym_human_input_shuffle_e3` is not a valid v7.4 repair. It improves camera completion but worsens JOINT, where the core problem is defined.
- The v7.4 human veto triggers: JOINT TMR coverage decreases from `31.6%` to `25.2%`, FDTMR worsens from `195.85` to `204.07`, and CLaTr FCD worsens from `126.91` to `143.70`.
- The camera/framing hard Out veto does not trigger (`9.0%` to `10.2%`, below the `13.5%` threshold), but the full JOINT row is still worse by TMR, CLaTr, caption F1, and coverage.
- Mechanistic conclusion: the problem is not fixed by a second forward pass that denies instance-matched camera state to the human-loss channel while sharing the same denoiser. The next serious route should be stronger structural asymmetry: human-first / root-first generation or branch-separated denoisers with explicit `H -> C` conditioning.

### 13.4 Stronger Asymmetry Closed-Loop Smoke

口径：5090 GPU0；official callbacks；`samples=32`、`batch_size=8`、`num_steps=8`、seed `20260613`。这组不是质量评估，而是代码闭环与 DS max gate 证据。`human_text` 使用 20-step smoke checkpoint，因此 generated-source composed JOINT 的质量 collapse 不作为方法否决，只说明必须先长训 human generator。

| condition | source JSON | samples | TMR FTD↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `human_text` official human metric | `human_text_smoke32.json` | 32 | 2266.95 | 3.44 | 0.0% | - | - | - | - | - | pass execution; undertrained quality |
| composed GT human + H2C clean | `composed_gt_human_h2c_clean_smoke32.json` | 32 | 439.83 | 15.71 | 100.0% | 110.77 | - | 97.1% | 0.557 | 6.0% | pass compose / decode / metric path |
| composed generated human + H2C replay | `composed_generated_human_h2c_replay_smoke32.json` | 32 | 2266.28 | 3.55 | 0.0% | 1024.98 | - | 0.0% | 0.017 | 15.4% | pass execution; quality dominated by 20-step human generator |

Implementation gates also passed on both remote boxes:

- 5090 and 4090 `py_compile` passed for `train_stage2_condmdi_pulp.py`, `storymotion_official_full_eval.py`, `storymotion_official_bridge_smoke.py`, and `render_bilateral_results.py`.
- 5090 and 4090 four-task mask check passed with `--task-probs 0 0 0 1`; `human_text` observes no latent and trains only human channels.
- old e3 three-task checkpoint compatibility smoke passed on 5090 and 4090 after limiting smoke tasks to the checkpoint's `num_task_embeddings`.

Decision: proceed to the first real long training only: `human_text` text-to-human. Do not yet start generated-source H2C long training, because generated-source stress is currently confounded by the deliberately tiny 20-step human generator.

Long-training deployment after DS max PASS:

| run | machine / GPU | start time | config summary | status |
| --- | --- | --- | --- | --- |
| `human_text_full_e3like_82688` | 5090 GPU0 | 2026-07-06 16:00 +0800 | `steps=82688`, `batch=512`, `width=384`, `dim_mults=1 2 2`, `task_probs=0 0 0 1`, `selection_metric=human_text_loss` | running |

DS max gate summary: pass for `human_text` long training only. 10k and 30k official `human_text` evals are required before any generated-source H2C training is justified.

First official gate result:

| checkpoint step | task | samples | FDTMR↓ | TMR↑ | HCov↑ | precision | recall | source JSON | decision |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 12000 | `human_text` | 1024 | 409.20 | 19.34 | 22.85% | 0.327 | 0.663 | `human_text_step12000_1024.json` | passes DS 10k-neighborhood gate |

Note: the first attempted `step_10000` snapshot was invalid because `last.pt` was copied while the 5090 training process was writing it. The accepted gate uses a stable frozen checkpoint whose internal metadata is step `12000`. The 30k watcher was updated to freeze and verify the checkpoint on 5090 before scp.

Paired render audit artifacts:

| artifact group | samples | path | purpose |
| --- | ---: | --- | --- |
| e3 human completion vs JOINT | 12 | `runs/visualizations/v7_4_paired_audit_20260706/e3_human_vs_joint` | visual audit of user-observed human degradation |
| e3 JOINT camera latent zero / shuffle / noise | 12 each | `runs/visualizations/v7_4_paired_audit_20260706/e3_joint_camera_latent_interventions` | visual counterpart to numeric raw-camera-state dependency |

Manual audit viewer is running on 5090 session `v74_paired_audit_gradio`, port `7862`.

## 14. v7.4 Generated-Source H2C Replay Adaptation 2026-07-06

口径：stronger asymmetry composed JOINT；human generator is `human_text_full_e3like_82688` final `last.pt`; H2C camera generator is MoLingo FullRF p2b baseline or replay fine-tuned checkpoint. Official composed eval uses `samples=1024`, `num_steps=50`, `cfg_scale=1.0`, `eta=0.0`, seed `17`.

### 14.1 Source-Shift Diagnosis

| condition | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | source JSON |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT human + H2C clean | 1024 | 150.04 | 18.54 | 93.94% | 24.35 | - | 90.92% | 0.626 | 5.40% | `composed_gt_human_h2c_clean_1024.json` |
| generated human + original H2C replay | 1024 | 376.06 | 18.13 | 27.83% | 500.95 | - | 14.94% | 0.108 | 38.65% | `composed_final_last_generated_h2c_replay_1024.json` |

Readout: GT-human composition proves the H2C clean upper bound is strong. The generated-human row collapses mainly in CLaTr / caption / Out, so the next bottleneck is generated-source H2C domain shift rather than another shared JOINT denoiser.

### 14.2 Replay Cache And Latent H2C Gates

Replay cache construction:

| artifact | train samples | val samples | generator | status |
| --- | ---: | ---: | --- | --- |
| `human_text_replay_cache_final_full_50step` | 94050 | 10549 | `human_text_full_e3like_82688` final `last.pt`, `num_steps=50` | built on 5090 GPU0; synced to 4090 |

Full-val original p2b latent baseline:

| run | eval samples | cache-replay MSE↓ | clean MSE↓ | cache-replay clean gap | source JSON |
| --- | ---: | ---: | ---: | ---: | --- |
| original p2b H2C | 10549 | 1.2192 | 0.8994 | 0.3555 | `h2c_generated_replay_final_full_50step_p2b_baseline_val.json` |

Fine-tune config: `--train-source cache-replay`, `--eval-sources cache-replay clean`, `--selection-metric cache_replay_camera_mse`, `--init-run-dir stage2_molingo_fullrf_h2c_v64_p2b_20260703`, `lr=2e-5`, planned `20000` steps.

| checkpoint | eval samples | cache-replay MSE↓ | clean MSE↓ | cache-replay clean gap | readout |
| ---: | ---: | ---: | ---: | ---: | --- |
| step 1000 | 2048 | 0.5617 | 0.6094 | -0.0783 | replay adapts and clean guard improves |
| step 2000 | 2048 | 0.3982 | 0.5353 | -0.2561 | continued improvement |
| step 3000 | 2048 | 0.3635 | 0.4915 | -0.2604 | first composed official eval checkpoint |
| step 4000 | 2048 | 0.3425 | 0.4661 | -0.2651 | still improving |
| step 5000 | 2048 | 0.3307 | 0.4487 | -0.2629 | latent gate still improves |

### 14.3 Step3000 Composed Closed Loop

| condition | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | source JSON |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| generated human + original H2C replay | 1024 | 376.06 | 18.13 | 27.83% | 500.95 | - | 14.94% | 0.108 | 38.65% | `composed_final_last_generated_h2c_replay_1024.json` |
| generated human + replay-ft H2C step3000 | 1024 | 386.38 | 18.70 | 25.39% | 112.67 | 20.97 | 58.89% | 0.238 | 20.51% | `composed_step3000_generated_h2c_replay_1024.json` |
| generated human + replay-ft H2C step5000 | 1024 | 386.38 | 18.70 | 25.39% | 141.44 | - | 60.55% | 0.236 | 18.64% | `composed_step5000_generated_h2c_replay_1024.json` |

Delta against generated-source baseline:

| metric | baseline | step3000 | change | readout |
| --- | ---: | ---: | ---: | --- |
| FDCLaTr↓ | 500.95 | 112.67 | -388.28 | large camera / semantic recovery |
| CCov↑ | 14.94% | 58.89% | +43.95pp | generated-source camera no longer collapsed |
| F1↑ | 0.108 | 0.238 | +0.130 | caption alignment improves but remains below GT-human upper bound |
| Out↓ | 38.65% | 20.51% | -18.14pp | framing improves but still not solved |
| FDTMR↓ | 376.06 | 386.38 | +10.32 | human-side distribution not improved by H2C, as expected |

Step5000 note: latent MSE continues to improve, CLaTr coverage and Out improve vs step3000, but CLaTr FCD regresses from `112.67` to `141.44`. Therefore latent `cache_replay_camera_mse` is not a sufficient checkpoint selector.

Decision: DS max reviewed the step3000 closed loop and passed continuation. Continue the same 20k run; do not switch to clean/replay mixing while clean MSE is improving. Preserve step3000, step5000, final, and best-latent checkpoints for official eval / visual audit.

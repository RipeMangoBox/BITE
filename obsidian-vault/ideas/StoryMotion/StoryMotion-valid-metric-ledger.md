---
title: "StoryMotion Valid Metric Ledger"
status: active
hypothesis: |
  StoryMotion decisions require evaluator-contract-verified evidence separated
  by Stage, task profile, budget, representation owner, split, and evidence tier.
tags:
  - StoryMotion
  - Motion_Generation
  - metric
  - evidence
  - status/active
aliases:
  - StoryMotion-Valid-Metrics
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
created: 2026-07-12T12:15:00+08:00
updated: 2026-07-21T15:42:04+08:00
---

# StoryMotion Valid Metric Ledger

> [!abstract] Canonical contract
> 本页只拥有已经审计的数值、比较边界和 artifact hashes。Stage1 reconstruction、Stage2 generation、30K diagnostic screen 与 105K formal evidence 分区记录；除明确标为 diagnostic 的 N64/short rows 外，正式表均为 official pure 4,053。当前裁决见 [[current]]，版本名称与完成 step 见 [[version_family]]，指标定义见 [[StoryMotion-metric-computation-io]]。

> [!important] C3-25 当前证据边界
> v8.1C C3-25 seed17/seed23 都完成了 Stage1 636K 与 pure4053 reconstruction audit。seed17 的 Stage2 continuous `0→105K` run **已全部完成**：`30K` 与 `105K` 两处 immutable checkpoint 均完成 Direct-H、Direct-C、joint parallel 三项 formal audit。**`105K` Direct-H TMR `14.389` / FTD `222.12` 均击败 former mainline v7.38 L0（`13.294 / 333.88`）；Direct-C CLaTr `59.539` / FCD `25.09` 均击败 v7.38 L0（`55.64 / 33.29`）；joint parallel 无 broad regression。** global-slope 现为非阻塞 diagnostic pass，C3-25 seed17 正式成为 Stage1/Stage2 mainline。历史 contract 的 `promotion_eligible=false` 保留为 provenance。Stage2 seed23 三路结果已写出但 audit pending，不进入本账本的 formal multi-seed claim。

## 1. 如何读表

### 1.1 Evidence tier

| tier | 含义 | 可以得出的结论 |
| --- | --- | --- |
| reference | GT identity / paired target | 仅作 evaluator 上界或零误差锚点；不是 one-to-many generator |
| mainline | 当前 StoryMotion Stage owner | 可作为同 Stage 的默认 comparator |
| A | same implementation、task-exposure matched | 可做 shared-vs-specialist 或同实现归因 |
| B | corrected v7.14 representation 上的 external operator | 可做 representation-matched system comparison |
| C | 方法原生 representation、decoder、objective 或 sampler | 只能做 native-system baseline |
| S | formal evaluator 可比，但至少一条 mutable training boundary 未闭合 | 只能做 audited system control |
| diagnostic | short、subset 或 read-only attribution | 不能晋级、不能替代 formal ranking |

### 1.2 Canonical anchors

| version / run | Stage / budget | profile | samples | role |
| --- | --- | --- | ---: | --- |
| GT identity / pure4053 | reference | reconstruction/paired target | 4,053 | evaluator 上界，不是 generator |
| Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 pretrained | reconstruction | 4,053 | native released Stage1 baseline |
| v7.14 / joint AE official r2 | Stage1 636K | reconstruction | 4,053 | former implementation mainline comparator |
| v7.38 L0 / clean 105K | Stage2 105K | Direct-H、Direct-C、parallel | 4,053 | former formal mainline comparator |
| v7.47 / official-AE Unified 105K | Stage2 105K | Direct-H、Direct-C、parallel | 4,053 | S-tier system control |
| MoMask-Pulp / native seed17 | Stage2 native VQ159K + Mask/Residual240K | Direct-H | 4,053 | C-tier native-system baseline |
| PulpMotion / official DiT-xy step92950 | Stage2 native endpoint | joint | 4,053 | C-tier native-system baseline |
| v7.36 A30 vs v8.1A G3 | Stage2 30K | Direct-H、Direct-C、parallel | 4,053 | matched generatability screen，不与 105K 排名混合 |
| v8.1C C3-25 / seed17 step30000 | Stage2 30K historical diagnostic | Direct-H、Direct-C、parallel | 4,053 | formal screen passed；同一进程继续至 105K |
| v8.1C C3-25 / seed17 step105000 | Stage2 105K mainline | Direct-H、Direct-C、parallel | 4,053 | formal mainline selection evidence；历史 diagnostic contract 不回写 |

除下述 PulpMotion native rows 外，全表 formal ordered-ID SHA256 为 a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。PulpMotion 两条 official DiT-xy rows 使用相同 4,053 identity set，但保留 native order `16d73df1916048dc44d407191bea9d3589113b55e22281b1acd574b16b9a8196`；因此它们是 C-tier system rows，不是 order-matched ablation。

## 2. Stage1 reconstruction

### 2.1 Semantic/distribution anchors

| version / run | Stage / budget | tier | samples | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GT identity / pure4053 | reference | reference | 4,053 | 0.00 | 16.47 | 100.0% | 0.00 | 70.24 | 100.0% | 0.945 | 0.7% |
| Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 pretrained | C | 4,053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |
| v7.14 / joint AE official r2 | Stage1 636K | former mainline | 4,053 | 31.10 | 14.99 | 97.9% | 0.48 | 69.46 | 99.5% | 0.927 | 5.1% |
| v7.14 / joint VAE official r2 | Stage1 636K | control | 4,053 | 69.61 | 13.77 | 93.1% | 2.28 | 68.45 | 97.7% | 0.914 | 7.9% |

GT 与 reconstruction rows 可直接解释 paired reconstruction；它们不能在 Stage2 one-to-many generation 表中被当成可训练方法的胜者。

### 2.2 Overall geometry

距离为 mm，角度为 degree。v7.14 与全部 v8 rows 使用同一 v8-schema evaluator、true length、pure4053 ordered IDs；Pulp official 与 MotionStreamer 保留各自 owning decoder，属于 system-level baseline。

| version / run | Stage / budget | tier | RA / global MPJPE ↓ | root ADE / FDE ↓ | yaw ↓ | Cam-ADE / FDE ↓ | rotation ↓ | RA / global slope per 100f | gate / status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | 0 / 0 | 0 / 0 | 0 | 0 / 0 | 0 | 0 / 0 | reference only |
| Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 pretrained | C | 80.254 / 181.053 | 150.145 / 595.955 | — | 137.449 / 277.227 | 1.792 | −7.000 / −10.340 | native baseline |
| MotionStreamer-Pulp / 500ep seed17 | Stage1 native 500 epochs | C | 79.937 / 281.524 | — | — | — | — | — | standalone causal baseline only |
| v7.14 / joint AE official r2 | Stage1 636K | former mainline | 80.731 / 212.735 | 169.640 / 415.430 | 21.640 | 41.760 / 51.500 | 0.619 | +29.020 / +145.300 | former implementation mainline |
| v8.1A / yaw001-root003 seed17 | Stage1 636K | candidate | 24.700 / 71.180 | 60.188 / 150.914 | 5.113 | 47.693 / 56.039 | 0.717 | +2.888 / +31.103 | global-slope diagnostic above former threshold；Stage2 broad Camera regression |
| v8.1C C2 / center100 seed17 | Stage1 636K | treatment | 25.927 / 74.406 | 62.688 / 158.011 | 5.360 | 31.956 / 41.183 | 0.859 | +4.641 / +38.799 | global-slope/rotation diagnostics above former thresholds；not selected |
| v8.1C C3-25 / seed17 selected | Stage1 636K | mainline | 24.570 / 69.243 | 58.252 / 148.365 | 4.947 | 39.486 / 48.270 | 0.705 | +1.148 / +26.302 | global-slope non-blocking diagnostic pass；current mainline |
| v8.1C C3-25 / seed23 robustness | Stage1 636K | robustness | 24.699 / 70.804 | 59.797 / 142.732 | 4.957 | 39.053 / 46.705 | 0.776 | +0.444 / +27.594 | global-slope non-blocking diagnostic pass；rotation limitation；robustness only |
| v8.1C C3-50 / seed17 exploratory | Stage1 636K | diagnostic | 25.593 / 73.166 | 61.678 / 154.323 | 5.194 | 36.412 / 45.116 | 0.718 | +3.079 / +36.214 | Human horizon worse；no Stage2 |
| v8.1B / residual AE seed17 | Stage1 636K | architecture control | 28.245 / 76.655 | 62.513 / 186.141 | 6.311 | 50.705 / 65.467 | 1.170 | −8.070 / −1.124 | Camera severe regression；no Stage2 |
| v8.2 / human200 seed17 | Stage1 636K | representation control | 12.999 / 68.706 | 65.847 / 242.966 | 1.275 | 53.028 / 61.554 | 0.569 | −4.518 / −17.269 | Camera center fail；no Stage2 |

### 2.3 Geometry by valid length

同一 valid length 的 rows 放在一起，按 1–64、65–128、129–192、193+ 递增。RA/global 与 Camera 距离均为 mm。Pulp/MotionStreamer 的 Camera 分 bin 未在对应 native artifact 中审计，因此保持为空，不能用 overall 值补写。

| valid length | n | version / run | Stage / tier | RA / global MPJPE ↓ | Cam-ADE / FDE ↓ | rotation ↓ |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| 1–64 | 1,805 | GT identity / pure4053 | reference | 0 / 0 | 0 / 0 | 0 |
| 1–64 | 1,805 | Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 C | 85.429 / 194.473 | — | — |
| 1–64 | 1,805 | MotionStreamer-Pulp / 500ep seed17 | Stage1 C | 80.658 / 219.311 | — | — |
| 1–64 | 1,805 | v7.14 / joint AE official r2 | Stage1 former mainline | 70.806 / 146.844 | 43.220 / 50.651 | 0.825 |
| 1–64 | 1,805 | v8.1A / yaw001-root003 seed17 | Stage1 candidate | 25.537 / 60.410 | 48.971 / 55.828 | 0.955 |
| 1–64 | 1,805 | v8.1C C2 / center100 seed17 | Stage1 treatment | 26.046 / 61.894 | 34.112 / 42.474 | 0.974 |
| 1–64 | 1,805 | v8.1C C3-25 / seed17 selected | Stage1 candidate | 26.010 / 60.819 | 41.423 / 48.946 | 0.936 |
| 1–64 | 1,805 | v8.1C C3-25 / seed23 robustness | Stage1 robustness | 26.189 / 60.784 | 41.738 / 49.013 | 0.842 |
| 1–64 | 1,805 | v8.1C C3-50 / seed17 exploratory | Stage1 diagnostic | 26.322 / 60.754 | 38.562 / 46.166 | 0.958 |
| 1–64 | 1,805 | v8.1B / residual AE seed17 | Stage1 control | 34.720 / 78.674 | 58.691 / 75.239 | 1.637 |
| 1–64 | 1,805 | v8.2 / human200 seed17 | Stage1 control | 16.055 / 80.783 | 55.419 / 63.316 | 0.756 |
| 65–128 | 1,411 | GT identity / pure4053 | reference | 0 / 0 | 0 / 0 | 0 |
| 65–128 | 1,411 | Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 C | 78.527 / 168.342 | — | — |
| 65–128 | 1,411 | MotionStreamer-Pulp / 500ep seed17 | Stage1 C | 75.063 / 299.147 | — | — |
| 65–128 | 1,411 | v7.14 / joint AE official r2 | Stage1 former mainline | 77.327 / 208.582 | 39.165 / 47.671 | 0.517 |
| 65–128 | 1,411 | v8.1A / yaw001-root003 seed17 | Stage1 candidate | 21.882 / 65.795 | 46.122 / 53.208 | 0.598 |
| 65–128 | 1,411 | v8.1C C2 / center100 seed17 | Stage1 treatment | 23.001 / 67.188 | 29.826 / 37.667 | 0.604 |
| 65–128 | 1,411 | v8.1C C3-25 / seed17 selected | Stage1 candidate | 22.131 / 64.623 | 37.711 / 44.948 | 0.592 |
| 65–128 | 1,411 | v8.1C C3-25 / seed23 robustness | Stage1 robustness | 22.691 / 67.824 | 36.266 / 42.004 | 0.551 |
| 65–128 | 1,411 | v8.1C C3-50 / seed17 exploratory | Stage1 diagnostic | 22.999 / 67.821 | 34.568 / 41.874 | 0.598 |
| 65–128 | 1,411 | v8.1B / residual AE seed17 | Stage1 control | 24.337 / 76.215 | 47.227 / 59.378 | 0.945 |
| 65–128 | 1,411 | v8.2 / human200 seed17 | Stage1 control | 11.657 / 63.289 | 50.628 / 57.811 | 0.483 |
| 129–192 | 456 | GT identity / pure4053 | reference | 0 / 0 | 0 / 0 | 0 |
| 129–192 | 456 | Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 C | 66.967 / 162.589 | — | — |
| 129–192 | 456 | MotionStreamer-Pulp / 500ep seed17 | Stage1 C | 78.304 / 362.423 | — | — |
| 129–192 | 456 | v7.14 / joint AE official r2 | Stage1 former mainline | 87.527 / 305.344 | 39.103 / 54.846 | 0.363 |
| 129–192 | 456 | v8.1A / yaw001-root003 seed17 | Stage1 candidate | 22.586 / 92.037 | 43.831 / 57.340 | 0.421 |
| 129–192 | 456 | v8.1C C2 / center100 seed17 | Stage1 treatment | 24.214 / 89.011 | 27.508 / 40.450 | 0.871 |
| 129–192 | 456 | v8.1C C3-25 / seed17 selected | Stage1 candidate | 21.415 / 83.650 | 34.343 / 47.512 | 0.418 |
| 129–192 | 456 | v8.1C C3-25 / seed23 robustness | Stage1 robustness | 20.709 / 84.617 | 34.676 / 44.955 | 0.854 |
| 129–192 | 456 | v8.1C C3-50 / seed17 exploratory | Stage1 diagnostic | 21.824 / 85.048 | 31.703 / 45.057 | 0.424 |
| 129–192 | 456 | v8.1B / residual AE seed17 | Stage1 control | 18.746 / 67.647 | 37.042 / 53.023 | 0.565 |
| 129–192 | 456 | v8.2 / human200 seed17 | Stage1 control | 8.424 / 51.237 | 48.775 / 61.402 | 0.334 |
| 193+ | 381 | GT identity / pure4053 | reference | 0 / 0 | 0 / 0 | 0 |
| 193+ | 381 | Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 C | 78.034 / 186.646 | — | — |
| 193+ | 381 | MotionStreamer-Pulp / 500ep seed17 | Stage1 C | 96.527 / 414.168 | — | — |
| 193+ | 381 | v7.14 / joint AE official r2 | Stage1 former mainline | 132.220 / 429.428 | 47.637 / 65.692 | 0.326 |
| 193+ | 381 | v8.1A / yaw001-root003 seed17 | Stage1 candidate | 33.705 / 117.184 | 52.082 / 65.968 | 0.385 |
| 193+ | 381 | v8.1C C2 / center100 seed17 | Stage1 treatment | 38.251 / 142.931 | 34.958 / 48.965 | 1.239 |
| 193+ | 381 | v8.1C C3-25 / seed17 selected | Stage1 candidate | 30.557 / 109.017 | 43.044 / 58.277 | 0.371 |
| 193+ | 381 | v8.1C C3-25 / seed23 robustness | Stage1 robustness | 29.853 / 112.779 | 41.893 / 55.279 | 1.208 |
| 193+ | 381 | v8.1C C3-50 / seed17 exploratory | Stage1 diagnostic | 36.261 / 137.542 | 38.685 / 52.219 | 0.376 |
| 193+ | 381 | v8.1B / residual AE seed17 | Stage1 control | 23.405 / 79.499 | 42.105 / 56.616 | 0.514 |
| 193+ | 381 | v8.2 / human200 seed17 | Stage1 control | 8.967 / 52.462 | 55.677 / 67.253 | 0.284 |

### 2.4 v8.1C dose、short screen 与 read-only diagnostics

Dose 是 auxiliary loss 的 shared-encoder gradient target，不是数据比例、训练比例或完成度。

| version / run | Stage / budget | center weight | raw-center gradient target | overall global / 193+ global ↓ | overall Cam-ADE / rotation ↓ | decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| v8.1A A10 / matched short | Stage1 10,176 | 0 | 0% | 786.574 / 1,082.338 mm | 596.584 mm / 7.414° | comparator |
| v8.1C C1 / center100 short | Stage1 10,176 | 0.00406677828128799 | 5.0% | 782.681 / 1,090.549 mm | 499.052 mm / 7.477° | structural pass；只授权 C2 |
| v8.1C C3-25 / selected short | Stage1 10,176 | 0.0010166945703219975 | 1.25% | 785.469 / 1,081.209 mm | 540.647 mm / 7.421° | pass；selected full arm |
| v8.1C C3-50 / exploratory short | Stage1 10,176 | 0.002033389140643995 | 2.5% | 783.117 / 1,056.305 mm | 518.521 mm / 7.441° | pass；higher-dose control |
| v8.1C C4-H / horizon short | Stage1 10,176 | C3-25 fixed | center 1.25% + horizon 1.25% | 788.762 / 1,094.129 mm | 540.427 mm / 7.424° | target fail；no full |

#### C5-B fresh multi-horizon matched screen

下表使用同一 pure4053 fixed-max source；`target Δ` 为相对同 seed control 的改善，guard 为 overall Human RA/global/root ADE/FDE/yaw 与 Camera ADE/FDE/rotation 中最大回退。seed17 只有 dose1.0 同时通过两个 target 与八项 guard；该 dose 在 seed23 上八项 guard 仍全过，但两个 target 都未达门槛。因此 two-seed screen fail，C5-B 停止且不授权 full。

| seed | version / run | Stage / budget | multi-horizon weight | global slope ↓ | slope target Δ | `193+` global ↓ | long target Δ | max guard regression | decision |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 17 | C3-25 control / `v8_1c_c3_25_matched_screen10176_seed17_5090g0_20260719` | Stage1 10,176 | 0 | 272.350 mm/100f | reference | 1,098.976 mm | reference | reference | matched comparator |
| 17 | C5-B dose0.5 / `v8_1c_c5b_mh_dose050_screen10176_seed17_5090g1_20260719` | Stage1 10,176 | 0.020651266983901972 | 269.141 mm/100f | +1.178% | 1,110.845 mm | −1.080% | +1.199% | fail both targets |
| 17 | C5-B dose1.0 / `v8_1c_c5b_mh_dose100_screen10176_seed17_5090g0_20260719` | Stage1 10,176 | 0.041302533967803944 | 251.348 mm/100f | +7.711% | 1,060.993 mm | +3.456% | +0.669% | pass；selected for seed23 confirmation |
| 23 | C3-25 control / `v8_1c_c3_25_matched_screen10176_seed23_4090g1_20260719` | Stage1 10,176 | 0 | 263.239 mm/100f | reference | 1,093.450 mm | reference | reference | matched comparator |
| 23 | C5-B dose1.0 / `v8_1c_c5b_mh_dose100_screen10176_seed23_4090g1_20260719` | Stage1 10,176 | 0.041302533967803944 | 264.770 mm/100f | −0.582% | 1,083.929 mm | +0.871% | +0.818% | fail both targets；stop |

| version / run | Stage / type | diagnostic | key audited result | authorization |
| --- | --- | --- | --- | --- |
| C0 / gradient calibration | Stage1 read-only | Camera-center unit gradient | C1 weight 0.00406677828128799 = raw-center target 5% | only freezes C1 scale |
| C4 / gradient calibration | Stage1 read-only | rotation vs horizon | cosine −0.00624；C4-R weight 0.00008010673098572695；C4-H weight 0.018266197084257824 | C4-R not run；C4-H short only |
| C5-A / pure4053 alignment | Stage1 read-only | last-valid vs four-anchor multi-horizon | global-MPJPE Spearman all 0.67580→0.77947；193+ 0.70027→0.75837 | only supports a future preregistration；no training |
| C5-B / fresh calibration seed17/23 | Stage1 read-only train-distribution | four-anchor multi-horizon unit gradient vs C3 parent | recommendations 0.04087558783454605 / 0.041733939559882145；max/min 1.020999；frozen base 0.041302533967803944 | freezes dose0.5=0.020651266983901972 and dose1.0=0.041302533967803944 for matched shorts only |

C5-A 的 trained-endpoint estimated weight 0.008456624012361412 不是 fresh-init training dose。pure4053 已参与 mainline 选择；后续论文级外推 claim 必须另冻结 sealed audit set。

## 3. Stage2 formal 105K evidence

### 3.1 v7.38 matched five-arm family

L0–L4 都从 v7.36 A30 恢复 optimizer，到 Stage2 step 105,000；共享 seed17、batch512、v7.14 non-causal cache/decoder、train-only full-cov stats、pure4053 与 DDIM50/CFG1/eta0。它们彼此可作 same-family matched comparison。

| version / run | Stage / budget | Direct-H FDTMR / TMR / HCov | Direct-C FDCLaTr / CLaTr / CCov / F1 | decision |
| --- | --- | ---: | ---: | --- |
| v7.38 L0 / clean | Stage2 105K | 333.88 / 13.294 / 40.54% | 33.29 / 55.640 / 73.23% / 0.715 | former formal mainline |
| v7.38 L1 / noisy-H | Stage2 105K | 319.80 / 13.087 / 41.4% | 63.98 / 51.339 / 68.5% / 0.677 | camera regression |
| v7.38 L2 / human curriculum | Stage2 105K | 296.32 / 13.163 / 47.0% | 50.60 / 52.792 / 70.1% / 0.681 | Human/cascade Pareto；not mainline |
| v7.38 L3 / camera temporal | Stage2 105K | 307.50 / 12.388 / 45.4% | 82.26 / 48.699 / 61.7% / 0.660 | camera forgetting |
| v7.38 L4 / unified temporal | Stage2 105K | 290.37 / 13.287 / 46.5% | 85.40 / 47.682 / 61.8% / 0.632 | camera forgetting |

| version / run | Stage / budget | parallel H FDTMR / TMR / HCov | parallel C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.38 L0 / clean | Stage2 105K | 282.37 / 14.420 / 48.98% | 58.96 / 47.129 / 65.68% / 0.569 | 21.69% | former formal mainline |
| v7.38 L1 / noisy-H | Stage2 105K | 285.35 / 11.820 / 48.5% | 94.48 / 43.392 / 60.1% / 0.544 | 21.0% | camera regression |
| v7.38 L2 / human curriculum | Stage2 105K | 288.45 / 11.571 / 47.6% | 80.17 / 43.933 / 62.9% / 0.540 | 24.3% | not mainline |
| v7.38 L3 / camera temporal | Stage2 105K | 275.54 / 11.728 / 47.9% | 101.96 / 39.857 / 55.0% / 0.494 | 24.7% | camera forgetting |
| v7.38 L4 / unified temporal | Stage2 105K | 298.53 / 10.725 / 45.1% | 120.40 / 37.184 / 48.8% / 0.444 | 29.7% | camera forgetting |

### 3.2 Direct-H fair system table

Human completion contract：human text → H。GT 是 identity reference；观察 Camera latent 的 symmetric control 不在本表。

| version / run | Stage / budget | tier | FDTMR ↓ | TMR ↑ | HCov ↑ | RA / global MPJPE ↓ | root ADE / FDE ↓ | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | 0 | 16.47 | 100% | 0 / 0 mm | 0 / 0 mm | not a generator |
| v7.38 L0 / clean | Stage2 105K | former mainline | 333.880 | 13.294 | 40.54% | 250.364 / 863.112 mm | 769.275 / 1,280.066 mm | formal comparator |
| v7.47 / official-AE Unified | Stage2 105K | S | 228.966 | 18.424 | 33.31% | 196.083 / 807.756 mm | 740.720 / 1,301.127 mm | formal；strict isolation not established |
| v7.42 / same-impl Human specialist | Stage2 task-exposure matched | A | 328.620 | 13.438 | 42.22% | — | — | formal |
| v7.45 / MoLingo human | Stage2 240K human-only | B | 149.163 | 17.729 | 49.86% | 242.502 / 1,249.134 mm | 1,164.249 / 2,007.279 mm | semantic signal；geometry no-promotion |
| MotionLab-MFT / v7.14 latent | Stage2 30K human-only | B | 156.350 | 18.172 | 59.19% | 250.782 / 951.380 mm | 857.640 / 1,436.396 mm | formal system peer |
| MoMask-Pulp / native seed17 | Stage2 native VQ159K + Mask/Residual240K | C | 219.553 | 27.347 | 45.50% | 316.113 / 1,160.494 mm | 998.888 / 1,610.472 mm | formal native baseline；full replay byte-exact；system boundaries differ |
| v8.1C C3-25 / seed17 step105000 | Stage2 105K mainline | mainline | 222.120 | 14.389 | 52.75% | — / — mm | — / — mm | current mainline；TMR/FTD/coverage 均击败 v7.38 L0；Direct-H decoded geometry pending |

### 3.3 Direct-C fair system table

Camera completion contract：observed/GT H + camera text → C。

| version / run | Stage / budget | tier | human condition | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Cam-ADE / FDE ↓ | rotation ↓ | status |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | GT-H | 0 | 70.24 | 100% | 0.945 | 0 / 0 m | 0° | not a generator |
| v7.38 L0 / clean | Stage2 105K | former mainline | GT-H latent | 33.290 | 55.640 | 73.23% | 0.715 | 1.512 / 1.606 m | 32.926° | formal comparator |
| v7.47 / official-AE Unified | Stage2 105K | S | GT-H in official basis | 17.876 | 60.158 | 83.69% | 0.774 | 0.152 / 0.256 m | 2.084° | formal；strict isolation not established |
| v7.42 / same-impl Camera specialist | Stage2 task-exposure matched | A | GT-H latent | 33.060 | 58.334 | 76.63% | 0.750 | — | — | formal |
| Director-C / native | Stage2 15.299M exposures | C | GT pelvis trajectory | 32.437 | 52.662 | 81.49% | 0.688 | — | — | semantic/distribution formal；decoded geometry re-eval required |
| CCD-Pulp / v7.14 latent | Stage2 60K × 256 | B | GT-H latent | 101.027 | 33.095 | 59.91% | 0.442 | — | — | semantic/distribution formal；decoded geometry re-eval required |
| v8.1C C3-25 / seed17 step105000 | Stage2 105K mainline | mainline | GT-H latent | 25.091 | 59.539 | 75.03% | 0.764 | — / — m | —° | current mainline；FCD/CLaTr/F1 均击败 v7.38 L0；Direct-C decoded geometry pending |

### 3.4 Joint parallel fair system table

Active joint profile 是 directed parallel。PulpMotion rows 使用 released AE 与 native sampler，属于 C-tier；它们不能解释为 StoryMotion representation ablation。

| version / run | Stage / budget | tier | H FDTMR / TMR / HCov | C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | H RA / global ↓ | Cam-ADE / FDE / rotation ↓ | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | 0 / 16.47 / 100% | 0 / 70.24 / 100% / 0.945 | 0.7% | 0 / 0 mm | 0 / 0 m / 0° | not a generator |
| v7.38 L0 / clean | Stage2 105K | former mainline | 282.370 / 14.420 / 48.98% | 58.960 / 47.129 / 65.68% / 0.569 | 21.69% | 252.670 / 842.297 mm | 2.912 / 3.026 m / 72.928° | formal comparator |
| v7.47 / official-AE Unified | Stage2 105K | S | 205.336 / 17.303 / 37.75% | 156.755 / 24.563 / 47.00% / 0.239 | 7.96% | 199.053 / 890.543 mm | 2.960 / 3.063 m / 69.212° | Human signal；Camera broad regression |
| v7.42 / same-impl joint specialist | Stage2 task-exposure matched | A | 300.470 / 12.605 / 45.03% | 66.810 / 45.029 / 63.76% / 0.570 | 19.33% | — | — | formal |
| PulpMotion / official DiT-xy no-Aux step92950 | Stage2 native endpoint | C | 375.015 / 20.532 / 14.90% | 94.842 / 35.691 / 48.33% / 0.491 | 39.54% | — | — | semantic/distribution formal；native order；decoded geometry re-eval required |
| PulpMotion / official DiT-xy Aux step92950 | Stage2 native endpoint | C | 414.796 / 21.657 / 13.82% | 93.269 / 37.777 / 44.81% / 0.513 | 28.47% | — | — | semantic/distribution formal；native order；decoded geometry re-eval required |
| v8.1C C3-25 / seed17 step105000 | Stage2 105K mainline | mainline | 227.189 / 13.691 / 53.27% | 70.580 / 46.720 / 60.57% / 0.599 | 18.35% | — / — mm | — / — m / —° | current mainline；joint parallel no broad regression；decoded geometry pending |

Cascade 不再是 active score/gate；只保留同 checkpoint 历史归因：

| version / run | Stage / budget | historical profile | H FDTMR / TMR / HCov | C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | status |
| --- | --- | --- | ---: | ---: | ---: | --- |
| v7.38 L0 / clean | Stage2 105K | human-first cascade | 346.730 / 13.115 / 39.45% | 48.540 / 53.746 / 64.47% / 0.671 | 13.95% | historical attribution only |
| v7.47 / official-AE Unified | Stage2 105K | human-first cascade | 1,974.947 / 1.734 / 0.05% | 607.124 / 8.157 / 4.81% / 0.052 | 81.44% | decisive failure；historical only |

### 3.5 Stage2 105K geometry by valid length

#### Direct-H

同一 valid length 放在一起并递增。距离为 mm。

| valid length | n | version / run | Stage / tier | RA / global MPJPE ↓ | root ADE / FDE ↓ |
| --- | ---: | --- | --- | ---: | ---: |
| 1–64 | 1,805 | v7.38 L0 / clean | Stage2 105K former mainline | 253.586 / 677.934 | — |
| 1–64 | 1,805 | v7.47 / official-AE Unified | Stage2 105K S | 212.067 / 638.744 | 554.517 / 958.293 |
| 1–64 | 1,805 | v7.45 / MoLingo human | Stage2 B | 251.390 / 842.422 | 741.395 / 1,257.738 |
| 1–64 | 1,805 | MotionLab-MFT / v7.14 latent | Stage2 B | 260.438 / 752.649 | 644.684 / 1,058.347 |
| 1–64 | 1,805 | MoMask-Pulp / native seed17 | Stage2 C | 324.008 / 852.930 | 674.854 / 1,083.558 |
| 1–64 | 1,805 | v8.1C C3-25 / seed17 step105000 | Stage2 105K diagnostic | 245.048 / 659.947 | 557.421 / 906.060 |
| 65–128 | 1,411 | v7.38 L0 / clean | Stage2 105K former mainline | 249.884 / 895.589 | — |
| 65–128 | 1,411 | v7.47 / official-AE Unified | Stage2 105K S | 188.249 / 851.014 | 792.751 / 1,407.208 |
| 65–128 | 1,411 | v7.45 / MoLingo human | Stage2 B | 235.229 / 1,310.340 | 1,233.567 / 2,109.151 |
| 65–128 | 1,411 | MotionLab-MFT / v7.14 latent | Stage2 B | 241.908 / 991.529 | 907.651 / 1,525.572 |
| 65–128 | 1,411 | MoMask-Pulp / native seed17 | Stage2 C | 311.172 / 1,248.485 | 1,092.817 / 1,796.358 |
| 65–128 | 1,411 | v8.1C C3-25 / seed17 step105000 | Stage2 105K diagnostic | 238.500 / 873.600 | 786.500 / 1,328.500 |
| 129–192 | 456 | v7.38 L0 / clean | Stage2 105K former mainline | 234.630 / 1,135.359 | — |
| 129–192 | 456 | v7.47 / official-AE Unified | Stage2 105K S | 166.025 / 1,062.929 | 1,017.026 / 1,843.047 |
| 129–192 | 456 | v7.45 / MoLingo human | Stage2 B | 221.093 / 1,697.425 | 1,636.947 / 2,885.096 |
| 129–192 | 456 | MotionLab-MFT / v7.14 latent | Stage2 B | 231.113 / 1,242.231 | 1,164.639 / 2,032.365 |
| 129–192 | 456 | MoMask-Pulp / native seed17 | Stage2 C | 294.303 / 1,469.573 | 1,333.195 / 2,193.523 |
| 129–192 | 456 | v8.1C C3-25 / seed17 step105000 | Stage2 105K diagnostic | 227.500 / 1,119.100 | 1,044.200 / 1,847.700 |
| 193+ | 381 | v7.38 L0 / clean | Stage2 105K former mainline | 255.706 / 1,294.288 | — |
| 193+ | 381 | v7.47 / official-AE Unified | Stage2 105K S | 185.344 / 1,142.850 | 1,099.478 / 1,883.859 |
| 193+ | 381 | v7.45 / MoLingo human | Stage2 B | 252.949 / 2,412.741 | 2,345.070 / 4,130.365 |
| 193+ | 381 | MotionLab-MFT / v7.14 latent | Stage2 B | 261.443 / 1,396.085 | 1,313.889 / 2,183.871 |
| 193+ | 381 | MoMask-Pulp / native seed17 | Stage2 C | 323.113 / 1,921.798 | 1,786.035 / 2,720.502 |
| 193+ | 381 | v8.1C C3-25 / seed17 step105000 | Stage2 105K diagnostic | 252.400 / 1,293.300 | 1,216.000 / 2,144.600 |

#### Direct-C and joint parallel

距离为 m，rotation 为 degree。

| valid length | n | version / run | Stage / profile | H RA / global ↓ | Cam-ADE / FDE ↓ | rotation ↓ |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| 1–64 | 1,805 | v7.38 L0 / clean | Stage2 105K Direct-C | — | 1.520 / 1.568 | 35.081 |
| 1–64 | 1,805 | v7.47 / official-AE Unified | Stage2 105K Direct-C | — | 0.145 / 0.235 | 2.554 |
| 1–64 | 1,805 | v7.38 L0 / clean | Stage2 105K parallel | — | 2.793 / 2.861 | 73.947 |
| 1–64 | 1,805 | v7.47 / official-AE Unified | Stage2 105K parallel | 0.215 / 0.676 m | 2.678 / 2.729 | 68.617 |
| 65–128 | 1,411 | v7.38 L0 / clean | Stage2 105K Direct-C | — | 1.486 / 1.582 | 31.637 |
| 65–128 | 1,411 | v7.47 / official-AE Unified | Stage2 105K Direct-C | — | 0.148 / 0.242 | 1.791 |
| 65–128 | 1,411 | v7.38 L0 / clean | Stage2 105K parallel | — | 2.897 / 3.014 | 72.269 |
| 65–128 | 1,411 | v7.47 / official-AE Unified | Stage2 105K parallel | 0.191 / 0.948 m | 3.068 / 3.186 | 70.145 |
| 129–192 | 456 | v7.38 L0 / clean | Stage2 105K Direct-C | — | 1.491 / 1.640 | 31.809 |
| 129–192 | 456 | v7.47 / official-AE Unified | Stage2 105K Direct-C | — | 0.155 / 0.278 | 1.470 |
| 129–192 | 456 | v7.38 L0 / clean | Stage2 105K parallel | — | 3.096 / 3.266 | 72.999 |
| 129–192 | 456 | v7.47 / official-AE Unified | Stage2 105K parallel | 0.173 / 1.208 m | 3.267 / 3.420 | 68.369 |
| 193+ | 381 | v7.38 L0 / clean | Stage2 105K Direct-C | — | 1.602 / 1.834 | 28.832 |
| 193+ | 381 | v7.47 / official-AE Unified | Stage2 105K Direct-C | — | 0.197 / 0.383 | 1.670 |
| 193+ | 381 | v7.38 L0 / clean | Stage2 105K parallel | — | 3.311 / 3.566 | 70.458 |
| 193+ | 381 | v7.47 / official-AE Unified | Stage2 105K parallel | 0.187 / 1.317 m | 3.533 / 3.765 | 69.583 |

### 3.6 Baseline secondary metrics and completeness audit

以下仍是同一 official pure4053 evaluator artifact 的字段，不是第二次评测。主表已拥有 FDTMR/FDCLaTr、TMR/CLaTr、coverage、caption F1 与 decoded geometry；这里补齐 retrieval、PRDC、MM distance、caption precision/recall 和 projection residual fields。

| version / run | Stage / tier | H R1 / R2 / R3 ↑ | H precision / recall ↑ | H density ↑ | H MM distance ↓ |
| --- | --- | ---: | ---: | ---: | ---: |
| v7.45 / MoLingo human | Stage2 B | 0.105 / 0.183 / 0.242 | 0.620 / 0.720 | 0.436 | 49.438 |
| MotionLab-MFT / v7.14 latent | Stage2 B | 0.411 / 0.621 / 0.747 | 0.731 / 0.651 | 0.606 | 49.475 |
| MoMask-Pulp / native seed17 | Stage2 C | 0.224 / 0.346 / 0.445 | 0.548 / 0.729 | 0.367 | 46.914 |
| v8.1C C3-25 / seed17 step105000 | Stage2 diagnostic | 0.229 / 0.383 / 0.493 | 0.709 / 0.576 | 0.540 | 50.575 |

| version / run | Stage / tier | C R1 / R2 / R3 ↑ | C precision / recall ↑ | C density ↑ | C MM distance ↓ | caption precision / recall ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Director-C / native | Stage2 C | 0.128 / 0.229 / 0.310 | 0.900 / 0.570 | 1.051 | 24.206 | 0.753 / 0.647 |
| CCD-Pulp / v7.14 latent | Stage2 B | 0.222 / 0.365 / 0.473 | 0.829 / 0.393 | 0.867 | 29.522 | 0.562 / 0.370 |
| v8.1C C3-25 / seed17 step105000 | Stage2 diagnostic | 0.372 / 0.592 / 0.717 | 0.877 / 0.575 | 0.899 | 22.615 | 0.817 / 0.719 |

| version / run | Stage / tier | H R1 / R2 / R3 ↑ | H precision / recall / density ↑ | H MM distance ↓ | C R1 / R2 / R3 ↑ | C precision / recall / density ↑ | C MM distance ↓ | caption precision / recall ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PulpMotion / official DiT-xy no-Aux step92950 | Stage2 C | 0.035 / 0.071 / 0.103 | 0.210 / 0.607 / 0.100 | 48.705 | 0.041 / 0.079 / 0.116 | 0.674 / 0.443 / 0.513 | 28.947 | 0.575 / 0.436 |
| PulpMotion / official DiT-xy Aux step92950 | Stage2 C | 0.038 / 0.075 / 0.105 | 0.216 / 0.616 / 0.095 | 48.404 | 0.048 / 0.085 / 0.123 | 0.644 / 0.475 / 0.475 | 28.422 | 0.588 / 0.465 |

| version / run | Stage / tier | r-FPD ↓ | projection precision / recall / density / coverage | g-FPD / error |
| --- | --- | ---: | ---: | ---: |
| PulpMotion / official DiT-xy no-Aux step92950 | Stage2 C | 7.404 | 0 / 0 / 0 / 0 | 0 / 0 |
| PulpMotion / official DiT-xy Aux step92950 | Stage2 C | 5.893 | 0 / 0 / 0 / 0 | 0 / 0 |

projection 中的 `0` 是 native evaluator artifact 实际发出的字段，不是本页补值；它不能替代 decoded geometry，也不能解释为物理误差为零。

适配与完整性审计的最窄结论如下：

| version / run | adapter audit | identity / decoder boundary | metric completeness | required next action |
| --- | --- | --- | --- | --- |
| MoMask-Pulp / native seed17 | pass：Pulp human199 official normalization；valid-length tail masked；RVQ、MaskTransformer、ResidualTransformer 与 owning VQ decoder 均 non-causal | train `a0981b…1dc9`；eval `a0d762…6b93`；native decoder | emitted TMR + paired Human geometry complete；integrated-yaw 与 no-reference physical 尚未生成 | 不重训；只有需要新增 yaw/physical 维度时重评 |
| v7.45 / MoLingo human | pass：corrected v7.14 latent/decoder；offline bidirectional masked RF；不作 streaming claim | 64 条 batch records 内含 4,053 unique IDs，聚合顺序 SHA 为 `a0d762…6b93` | emitted TMR + paired Human geometry complete；integrated-yaw 与 no-reference physical 缺失 | 不重训；新增 evaluator 维度时重评 |
| MotionLab-MFT / v7.14 latent | pass：corrected v7.14 human latent slice 与 owning decoder；human text-only | 4,053 records；顺序 SHA `a0d762…6b93` | emitted TMR + paired Human geometry complete；integrated-yaw 与 no-reference physical 缺失 | 不重训；新增 evaluator 维度时重评 |
| Director-C / native | pass：Pulp camera caption、GT pelvis trajectory、train-only standardization、native direct 9D C2W output | pure4053 canonical order；no tokenizer/decoder | CLaTr/caption/PRDC complete；Cam-ADE/FDE/rotation 缺失 | 不重训；只需 decoded-camera re-eval |
| CCD-Pulp / v7.14 latent | pass：GT-H latent + camera text；v7.14 cache/decoder hash 与 non-causal contract 已绑定 | pure4053 canonical order；owning decoder `91248bf4…7ce1` | CLaTr/caption/PRDC complete；Cam-ADE/FDE/rotation 缺失 | 不重训；只需 owning-decoder geometry re-eval |
| PulpMotion / official DiT-xy step92950 | native-system boundary valid；released AE 与 sampler 保持原样 | same 4,053 set；native order `16d73d…8196` | H/C semantics、PRDC 与 projection fields complete；decoded H/C geometry、integrated-yaw 与 no-reference physical 缺失 | 不重训；只需 native owning-decoder re-eval |
| MotionStreamer-Pulp / 500ep seed17 | pass within the standalone native-system exception：causal tokenizer、owning decoder 与 representation 均只属于 MotionStreamer；不消费 StoryMotion cache/checkpoint | native Stage1 artifact；不得与 StoryMotion Stage1/Stage2 causal boundary混用 | 已审计 RA/global overall + length bins；root/yaw/Camera 与 Stage2 formal generation artifact 缺失 | 不重训；如需完整 system row，按 native decoder 新做 formal re-eval |

这里的“完整”只指 artifact 已经发出的字段。按当前 experiment contract，缺失的 decoded geometry、integrated-yaw 或 no-reference physical 不能被 `—` 解释为通过；在这些维度补齐前，Director-C、CCD-Pulp、PulpMotion 与 MotionStreamer 的 system artifact 仍不完整。

## 4. Stage2 30K matched generatability screen

v7.36 A30、v8.1A G3 与 v8.1C C3-25 共享 Unified-3 implementation、optimizer、batch、task probabilities、seed17、pure4053、DDIM50、CFG1、eta0 与 evaluator。必然不同的 Stage1 checkpoint、owning decoder、cache 和 train-only stats 被显式绑定，因此它回答 representation-system generatability。C3-25 的三项 formal audit 均通过；结合 Stage1 Pareto 与非阻塞 global-slope diagnostic pass，该 endpoint 现为 mainline。历史 contract 的 diagnostic 字段不回写。

### 4.1 Primary metrics plus overall geometry

| version / run | Stage / budget | Direct-H FDTMR / TMR / HCov | RA / global MPJPE ↓ | root ADE / FDE ↓ | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.36 A30 / matched control | Stage2 30K | 399.729 / 11.391 / 33.11% | 0.260 / 0.924 m | 0.826 / 1.348 m | comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K | 272.434 / 11.841 / 47.99% | 0.268 / 0.884 m | 0.781 / 1.299 m | Human signal |
| v8.1C C3-25 / seed17 step30000 | Stage2 30K diagnostic | 359.176 / 11.526 / 39.28% | 0.254 / 0.860 m | 0.764 / 1.271 m | passes Direct-H comparison；continue 105K |

| version / run | Stage / budget | Direct-C FDCLaTr / CLaTr / CCov / F1 | Cam-ADE / FDE ↓ | rotation ↓ | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.36 A30 / matched control | Stage2 30K | 114.568 / 35.067 / 61.56% / 0.463 | 1.994 / 2.147 m | 44.847° | comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K | 178.234 / 25.219 / 46.51% / 0.254 | 2.022 / 2.145 m | 46.974° | broad Camera regression |
| v8.1C C3-25 / seed17 step30000 | Stage2 30K diagnostic | 96.166 / 36.846 / 62.97% / 0.480 | 1.982 / 2.105 m | 45.046° | passes Direct-C comparison；no decoder-aware short |

| version / run | Stage / budget | parallel H FDTMR / TMR / HCov | parallel C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | H RA / global ↓ | Cam-ADE / FDE / rotation ↓ | decision |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| v7.36 A30 / matched control | Stage2 30K | 348.889 / 12.450 / 39.18% | 110.360 / 29.933 / 58.97% / 0.366 | 31.93% | 0.267 / 0.894 m | 3.243 / 3.342 m / 81.092° | comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K | 245.886 / 12.439 / 50.41% | 195.453 / 21.856 / 44.88% / 0.223 | 34.59% | 0.269 / 0.877 m | 2.797 / 2.920 m / 72.151° | Camera semantic/distribution regression |
| v8.1C C3-25 / seed17 step30000 | Stage2 30K diagnostic | 336.130 / 12.439 / 41.82% | 90.664 / 31.617 / 58.60% / 0.367 | 20.03% | 0.259 / 0.845 m | 3.226 / 3.325 m / 77.008° | passes joint comparison；continue 105K |

G3 status：stop_30k_broad_camera_regression，v8.1A 不续 105K。C3-25 的历史 G3 status 为 pass_30k_active_profiles_continue_105k，随后 `105K` formal 闭合并晋升为 mainline；Direct-C 没有 broad regression，因此按预注册 D4.3 分支不启动 decoder-aware auxiliary short。

### 4.2 Geometry by valid length

同一 valid length 放在一起并递增；距离为 m。

| valid length | n | version / run | Stage / profile | H RA / global ↓ | H root ADE / FDE ↓ | Cam-ADE / FDE ↓ | rotation ↓ |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| 1–64 | 1,805 | v7.36 A30 | Stage2 30K Direct-H | 0.266 / 0.726 | 0.616 / 0.985 | — | — |
| 1–64 | 1,805 | v8.1A G3 | Stage2 30K Direct-H | 0.275 / 0.698 | 0.581 / 0.936 | — | — |
| 1–64 | 1,805 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-H | 0.261 / 0.682 | 0.572 / 0.924 | — | — |
| 1–64 | 1,805 | v7.36 A30 | Stage2 30K Direct-C | — | — | 1.995 / 2.084 | 47.937 |
| 1–64 | 1,805 | v8.1A G3 | Stage2 30K Direct-C | — | — | 1.994 / 2.048 | 49.231 |
| 1–64 | 1,805 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-C | — | — | 1.970 / 2.048 | 46.403 |
| 1–64 | 1,805 | v7.36 A30 | Stage2 30K parallel | 0.276 / 0.711 | 0.593 / 0.948 | 3.115 / 3.179 | 80.874 |
| 1–64 | 1,805 | v8.1A G3 | Stage2 30K parallel | 0.276 / 0.697 | 0.577 / 0.928 | 2.652 / 2.720 | 71.199 |
| 1–64 | 1,805 | v8.1C C3-25 / seed17 step30000 | Stage2 30K parallel | 0.267 / 0.679 | 0.563 / 0.894 | 3.102 / 3.157 | 75.862 |
| 65–128 | 1,411 | v7.36 A30 | Stage2 30K Direct-H | 0.257 / 0.965 | 0.873 / 1.441 | — | — |
| 65–128 | 1,411 | v8.1A G3 | Stage2 30K Direct-H | 0.264 / 0.926 | 0.830 / 1.376 | — | — |
| 65–128 | 1,411 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-H | 0.250 / 0.902 | 0.811 / 1.345 | — | — |
| 65–128 | 1,411 | v7.36 A30 | Stage2 30K Direct-C | — | — | 1.950 / 2.113 | 42.608 |
| 65–128 | 1,411 | v8.1A G3 | Stage2 30K Direct-C | — | — | 2.029 / 2.161 | 46.317 |
| 65–128 | 1,411 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-C | — | — | 1.989 / 2.113 | 44.753 |
| 65–128 | 1,411 | v7.36 A30 | Stage2 30K parallel | 0.261 / 0.935 | 0.840 / 1.409 | 3.217 / 3.320 | 80.361 |
| 65–128 | 1,411 | v8.1A G3 | Stage2 30K parallel | 0.265 / 0.907 | 0.810 / 1.362 | 2.839 / 2.976 | 73.252 |
| 65–128 | 1,411 | v8.1C C3-25 / seed17 step30000 | Stage2 30K parallel | 0.254 / 0.893 | 0.798 / 1.328 | 3.264 / 3.370 | 77.688 |
| 129–192 | 456 | v7.36 A30 | Stage2 30K Direct-H | 0.244 / 1.219 | 1.137 / 1.912 | — | — |
| 129–192 | 456 | v8.1A G3 | Stage2 30K Direct-H | 0.252 / 1.123 | 1.041 / 1.830 | — | — |
| 129–192 | 456 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-H | 0.236 / 1.119 | 1.043 / 1.821 | — | — |
| 129–192 | 456 | v7.36 A30 | Stage2 30K Direct-C | — | — | 1.989 / 2.234 | 42.647 |
| 129–192 | 456 | v8.1A G3 | Stage2 30K Direct-C | — | — | 2.028 / 2.220 | 45.477 |
| 129–192 | 456 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-C | — | — | 1.935 / 2.096 | 43.473 |
| 129–192 | 456 | v7.36 A30 | Stage2 30K parallel | 0.248 / 1.175 | 1.093 / 1.887 | 3.431 / 3.551 | 82.321 |
| 129–192 | 456 | v8.1A G3 | Stage2 30K parallel | 0.250 / 1.133 | 1.048 / 1.833 | 2.976 / 3.159 | 75.284 |
| 129–192 | 456 | v8.1C C3-25 / seed17 step30000 | Stage2 30K parallel | 0.239 / 1.088 | 1.006 / 1.765 | 3.377 / 3.520 | 79.161 |
| 193+ | 381 | v7.36 A30 | Stage2 30K Direct-H | 0.261 / 1.353 | 1.273 / 2.047 | — | — |
| 193+ | 381 | v8.1A G3 | Stage2 30K Direct-H | 0.269 / 1.319 | 1.237 / 2.093 | — | — |
| 193+ | 381 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-H | 0.258 / 1.244 | 1.165 / 1.987 | — | — |
| 193+ | 381 | v7.36 A30 | Stage2 30K Direct-C | — | — | 2.153 / 2.463 | 41.128 |
| 193+ | 381 | v8.1A G3 | Stage2 30K Direct-C | — | — | 2.121 / 2.454 | 40.509 |
| 193+ | 381 | v8.1C C3-25 / seed17 step30000 | Stage2 30K Direct-C | — | — | 2.062 / 2.358 | 41.592 |
| 193+ | 381 | v7.36 A30 | Stage2 30K parallel | 0.267 / 1.279 | 1.199 / 2.014 | 3.727 / 3.939 | 83.363 |
| 193+ | 381 | v8.1A G3 | Stage2 30K parallel | 0.268 / 1.308 | 1.230 / 2.067 | 3.114 / 3.370 | 68.826 |
| 193+ | 381 | v8.1C C3-25 / seed17 step30000 | Stage2 30K parallel | 0.259 / 1.169 | 1.083 / 1.852 | 3.485 / 3.718 | 77.342 |

### 4.3 C3-25 step30000 secondary metrics

以下字段与第 4.1–4.2 节来自同一批 pure4053 formal artifacts；这里只补齐 retrieval、PRDC、MM distance、caption precision/recall 与 projection fields。v7.36 的 secondary fields 没有在本轮重提取，因此不能把缺少 matched row 写成改善。

| version / run | profile | H R1 / R2 / R3 ↑ | H precision / recall / density ↑ | H MM distance ↓ |
| --- | --- | ---: | ---: | ---: |
| v8.1C C3-25 / seed17 step30000 | Direct-H | 0.196 / 0.333 / 0.433 | 0.596 / 0.523 / 0.419 | 51.267 |
| v8.1C C3-25 / seed17 step30000 | joint parallel | 0.205 / 0.335 / 0.445 | 0.711 / 0.535 / 0.538 | 51.029 |

| version / run | profile | C R1 / R2 / R3 ↑ | C precision / recall / density ↑ | C MM distance ↓ | caption precision / recall ↑ |
| --- | --- | ---: | ---: | ---: | ---: |
| v8.1C C3-25 / seed17 step30000 | Direct-C | 0.247 / 0.399 / 0.512 | 0.906 / 0.377 / 1.046 | 28.535 | 0.578 / 0.414 |
| v8.1C C3-25 / seed17 step30000 | joint parallel | 0.196 / 0.328 / 0.428 | 0.886 / 0.354 / 0.901 | 29.992 | 0.429 / 0.323 |

| version / run | profile | r-FPD ↓ | projection precision / recall / density / coverage | g-FPD / error |
| --- | --- | ---: | ---: | ---: |
| v8.1C C3-25 / seed17 step30000 | joint parallel | 2.396 | 0 / 0 / 0 / 0 | 0 / 0 |

这里的 projection `0` 同样只作 emitted-field completeness 记录，不作为“完美投影/物理质量”结论。

## 5. Read-only diagnostics

### 5.0 C3 D1 cache geometry

D1 使用 exact C3 train/eval cache 与 train-only full-cov stats；train split 估计统计，eval split 只作冻结报告。effective rank 为坐标系内诊断，不是生成质量分数。

| version / run | split | samples | raw H / C effective rank | normalized H / C effective rank | dead H / C channels | raw H-C corr mean / max | normalized H-C corr mean / max |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v8.1C C3-25 D1 / continuous diagnostic | train | 162,760 | 45.074 / 9.719 | 128.000 / 64.000 | 0 / 0 | 0.0657 / 0.3525 | 0.0504 / 0.2923 |
| v8.1C C3-25 D1 / continuous diagnostic | eval frozen report | 4,053 | 47.423 / 11.512 | 113.786 / 55.721 | 0 / 0 | 0.0629 / 0.3593 | 0.0563 / 0.3170 |

valid length 相同的 train/eval 行放在一起，length 递增：

| valid length | split | n | raw H / C effective rank | normalized H / C effective rank | raw / normalized mean \|H-C corr\| |
| --- | --- | ---: | ---: | ---: | ---: |
| 1–64 | train | 39,634 | 41.466 / 9.406 | 111.132 / 60.072 | 0.0771 / 0.0566 |
| 1–64 | eval | 1,805 | 45.414 / 12.406 | 94.760 / 47.267 | 0.0708 / 0.0639 |
| 65–128 | train | 62,141 | 42.262 / 9.746 | 125.009 / 63.470 | 0.0681 / 0.0515 |
| 65–128 | eval | 1,411 | 45.369 / 11.148 | 109.588 / 55.160 | 0.0646 / 0.0588 |
| 129–192 | train | 34,518 | 44.262 / 9.512 | 124.311 / 63.403 | 0.0654 / 0.0522 |
| 129–192 | eval | 456 | 42.966 / 9.932 | 113.117 / 58.378 | 0.0650 / 0.0583 |
| 193+ | train | 26,467 | 41.982 / 9.161 | 117.133 / 61.001 | 0.0682 / 0.0563 |
| 193+ | eval | 381 | 40.072 / 9.435 | 106.546 / 56.015 | 0.0750 / 0.0678 |

最窄结论：没有 dead-channel 或 branch-marginal collapse；raw Camera latent 的有效秩明显低于 Human，train-only whitening 按定义恢复 marginal scale，但 H-C 依赖仍存在。该结果只排除明显 cache health failure，不预测 `30K/105K` 生成质量。

### D4 family：Stage2 30K frozen diagnostics

原始 D4/D4.2/D4.3 是 v8.1A G3 的 N64 read-only diagnostics；C3-25 在自己的 `30K` formal 启动后只读复用了 D4.3 matched protocol。t=50/500/950 是 diffusion timestep，不是训练 step。它们不训练、不写 cache，也不单独授权新长训。

### 5.1 D4 residual propagation

表中 ratio 均为 v8.1A / v7.36。

| version / run | diffusion t | whitened RMS | decoder-input RMS | Cam-ADE | Cam-FDE | narrow reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| v8.1A D4 vs v7.36 D4 | 50 | 1.084× | 1.214× | 1.550× | 1.604× | low-noise mismatch strongest |
| v8.1A D4 vs v7.36 D4 | 500 | 1.022× | 1.147× | 1.207× | 1.248× | weaker same-direction chain |
| v8.1A D4 vs v7.36 D4 | 950 | 1.037× | 1.094× | 1.054× | 1.062× | no global all-noise amplification claim |

### 5.2 D4.2 Camera-text reliance

唯一 intervention 是 aligned Camera-text embedding 改为循环错位；human-text、noise 与 x_t 保持相同。

| version / run | diffusion t | decoder-input condition-effect RMS v8.1A / v7.36 | conclusion |
| --- | ---: | ---: | --- |
| v8.1A D4.2 vs v7.36 D4.2 | 50 | 1.133× | aligned text 有正平均 advantage |
| v8.1A D4.2 vs v7.36 D4.2 | 500 | 1.108× | 不支持 simple condition neglect |
| v8.1A D4.2 vs v7.36 D4.2 | 950 | 1.225× | text 被使用，但不证明 semantic mapping 正确 |

### 5.3 D4.3 owning-decoder direction sensitivity

| version / run | diffusion t | center actual baseline→candidate | center cand/base | center actual/random | rotation actual baseline→candidate | rotation cand/base | rotation actual/random | preregistered rule |
| --- | ---: | --- | ---: | ---: | --- | ---: | ---: | --- |
| v8.1A D4.3 r3 vs v7.36 r3 | 50 | 2.740→3.417 | 1.247× | 2.470× | 46.652→52.504 | 1.125× | 2.360× | center + rotation pass |
| v8.1A D4.3 r3 vs v7.36 r3 | 500 | 3.079→3.290 | 1.069× | 2.287× | 57.817→53.394 | 0.923× | 2.449× | cand/base fail |
| v8.1A D4.3 r3 vs v7.36 r3 | 950 | 3.460→3.073 | 0.888× | 1.958× | 68.347→71.821 | 1.051× | 3.096× | outside rule；cand/base fail |
| v8.1C C3-25 D4.3 vs v7.36 r3 | 50 | 2.740→3.099 | 1.131× | 2.197× | 46.652→45.991 | 0.986× | 2.186× | center only pass |
| v8.1C C3-25 D4.3 vs v7.36 r3 | 500 | 3.079→3.088 | 1.003× | 2.227× | 57.817→55.374 | 0.958× | 2.567× | cand/base fail |
| v8.1C C3-25 D4.3 vs v7.36 r3 | 950 | 3.460→2.829 | 0.818× | 1.841× | 68.347→74.099 | 1.084× | 3.270× | outside rule；cand/base fail |

最窄结论：v8.1A 的 near-manifold 低噪 residual 更集中命中 owning decoder 的 Camera-center/rotation 高敏方向；C3-25 只保留较弱的 `t=50` center signature，rotation 不复现。由于 C3-25 `30K` Direct-C formal 没有 broad regression，预注册分支裁决为保留 attribution、不开 decoder-aware auxiliary short。两组 D4.3 都是 Stage1 manifold/decoder × Stage2 residual 的 system comparison，不能单独归给某一 Stage。

> [!warning] D4.3 stats uncertainty
> v8.1A parent contract 的 expected pre-resume stats SHA256 为 605049fa…71feb，当前文件为 94805397…5adc4，embedded train-cache 为 3b55223d…bd22。旧 serialization 已不存在，无法 tensor-by-tensor 追溯；r3 仅在显式记录三者后运行。因此 D4.3 永久是 diagnostic-only。

## 6. Provenance registry

### 6.1 Stage1 core artifacts

| version / run | Stage / status | checkpoint / owning-decoder SHA256 | geometry SHA256 | contract / audit SHA256 |
| --- | --- | --- | --- | --- |
| v7.14 / joint AE official r2 | Stage1 former mainline | 91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1 | abac845f8eac2b3c6da9beeabc02d26058e17b2007fa93d60dda54e7c3ee5248 | evaluator a52aba4d6260aeefac4e5891fbe510322bf6eaf12ce98e3d0bda16ffbc8ddf5e |
| v8.1A / yaw001-root003 seed17 | Stage1 full | ac47c2191c44d6368a5468510975cefcf0efd1338b03ace50266830c344151f1 | same-script evaluator above | owning checkpoint verified |
| v8.1C C2 / center100 seed17 | Stage1 full no-promotion | f16fb879eb7feebbebba10d24c6039cfec4fbc7812492fadedd9cb5c9c73530e | 0f4cddf17fd15a4b73afeff17c2b489702f237928b099d9d699340eba2f31d96 | contract 904ae14866b0a62fed37cc0b09de5f6bf9d177f81cfcfea760fb96247bdcdac8 |
| v8.1C C3-25 / seed17 selected | Stage1 full；exact Stage2 diagnostic parent | d0abb3268b14c19aada48fd2b9242fbbb03e9d808959539cac47f33448e4788a | 8b0ab3ba82f85192adeb066d99ce6a07f0fe645b2e916300c96e16b4aad43f4d | contract 80fbf5743aab7517acbfe9bcff6cde4311ce9257cd477e7af5baa658c2de6e73；audit 75d2daf8cd39d91affae8181cfb1365efb3a52bfbc85f50a1cdc6b7d90cf9b15 |
| v8.1C C3-25 / seed23 robustness | Stage1 full no-Stage2 | c73027b8f4c114c1c2ba54994c576592cb3f223dd7117fac7188dba9a7b0d3ad | 8e5a44cb586eeba1cbaeca82ee2b731badfa4dab4f15c40f11ccb7140f3a1b34 | contract 32ce7f8d1a91c75afe821659a2235d3ed05f8878380b79a7c7dd44a4e20bb4c1 |
| v8.1C C3-50 / seed17 exploratory | Stage1 full no-Stage2 | 4c9b51778104aef3e85f2664086a22802988a9a23833181026c6facdab608d98 | c0bb55bb244011ebffad5911d9ba43a7b4ba1b28bcc031a6df58e0f2158f89fc | contract 98a5aa0c00c14b30bb23c6a4ac1fe80a4397216f408f3ef3d48196c92edca8c3 |
| v8.1C C5-B / fresh calibration seed17/23 | Stage1 read-only；doses frozen | no checkpoint | seed17 c5755cf277da27fb62bba9518239af2a55eb9156acd994b196d1e665860832d5；seed23 561b1c4f43f59a06012b1585c49a58729d02d0a3382db5fc86e6d434137cf0c7；frozen doses 9042aa679a97c41b75fd9b2eb8b7854f141bc55c5df8a5bc4d0a153f3d6ab720 | contract c735a9c4aa7c7bcc8a56924bf2266d93333244d5f1f232b8114930e18b3b32c0 |
| v8.1C C5-B / seed17 control | Stage1 `10,176` matched comparator | 49b4e71ea0225ad299dbfd2b9c8590c372deaab1b8ae03044a0c5d7138f825fa | c74393c248b016237ba183ff904e83a23ef962191b4b7dfa90e47f643200d043 | contract 523f187c3baa687b93c5292e86bb043ce2194225f5a4a3595853aac351e3051b；shared gate 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766 |
| v8.1C C5-B / seed17 dose0.5 | Stage1 `10,176` target fail | eba485badc38c762bb55bb639dc1e83b675daa3d3b1f4483ad573c55832298f3 | b8291f8675c13972cfd859cd7f5eb5b186bb9acbb20ff8a739d4b483a7567a54 | contract 0e6cf69d6be78e47c86abd229b9bc8a7ac5272c48b5a4dddf3733923066623b1；shared gate 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766 |
| v8.1C C5-B / seed17 dose1.0 | Stage1 `10,176` selected for confirmation | ad6e32dbf4865db68b205c0aadcf3e640641d063e37d2b8a77a93405d825a05b | e765454a74c4c25d867cef602fab42a8f20b3b01a2f161a51fdf6ab300471edc | contract e9a430428c22efd804e41691454f8a7df7123529d1d18c3421272f462ed8092a；shared gate 0260192649bd0eaaa179fb5d39fa8d62a42f4db7744e2d28bd9974aed7b6b766 |
| v8.1C C5-B / seed23 control | Stage1 `10,176` matched comparator | f15ada53e469f43ad209531edde505083b7b3881538f2aee2cb16ccf5fa5a984 | 00a7eb840b42dee68caf16b81c3af881c766a6f7f4a4e3a155dcaca8f225535f | contract 32a5c5fa5d1d0eccdcb5ccc7e87448491afd9f904721ff26c1b44244114a2d23；shared gate 6bed0bc8957c691f7f448165d30fe5703ebf35ee7bb515eec90b7e818a43ce88 |
| v8.1C C5-B / seed23 dose1.0 | Stage1 `10,176` confirmation fail | e1cb80a10420ad0ffd703da1060a93630bd7afb9252c18c72783da27cdef36d6 | 189996bfcf5d3fa85a4d13b4c2586546baa2a0b9005939b86075565dae091c42 | contract d1731adeeae99dbf1edb56628067f83f845d5689869be556d3011ef0f023ec21；shared gate 6bed0bc8957c691f7f448165d30fe5703ebf35ee7bb515eec90b7e818a43ce88 |

Stage1 train/eval ordered-ID SHA256：a0981b6c6223409d656ad8c43cfcf95cae6ec9a28640143b87b6322292c51dc9 / a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。

### 6.2 Stage2 core artifacts

| version / run | Stage / status | checkpoint SHA256 | owning decoder / cache boundary | contract / audit |
| --- | --- | --- | --- | --- |
| v7.38 L0 / clean | Stage2 105K former mainline | ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35 | v7.14 owning decoder | 20/20 family artifacts audited |
| v7.47 / official-AE Unified | Stage2 105K S-control | b8c06913a5efdbaa0c178e452998352033174614aa0a60ad96920fe14a8acbb2 | decoder e0ff0a66129d77eb27a18d0034b23f692aaec3ef53afd540097d8d9544a73e52；train/eval cache 1924c632…d1e8 / c642f7c7…d1d3 | contract 37d61e28076735979731e47712500cee016365a4e9e2eb7753d93a10416dee51 |
| v7.36 A30 / matched control | Stage2 30K | 7dcf3b1911af144ea9ef2b30017dd07472d62f655fd04c1dc9263581e3382c0b | v7.14 decoder 91248bf4…7ce1；cache f7a00a48…a5983 / 6f13816c…9b25 | matched comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K stopped | becc2c11051bfd7857acb0602f61c755cd664969f34acef1f0232711feee5bb8 | v8.1A decoder ac47c219…151f；cache 3b55223d…bd22 / 1050748f…541d | contract c841fda54b8611d27b59aeaa3ca3c74c26865eee100428828df8c1e73ca5ab59 |
| v8.1C C3-25 / current mainline；historical diagnostic contract | Stage2 `0→105K` completed；30K/105K formal passed | 3533a4216b441b8fba0d6a791408d60a8708dc9a44e47b93d3187217ee83e226 | C3-25 decoder d0abb326…4788a；train/eval cache bc8c847e…3fa9 / 39485590…f5d6；full-cov stats 0c97d247…3400 | step contract 963327e766cf5acb168dc668616f7098df94c4df50b2a160299bcfcd2d2fe066；contract audit 6182d01d6f3ff4179b8c4f7b8d543d78f3fa4cce60b3db296f10e461e2daf597；H/C/J results c35566ed…b84b4 / accaa2c5…c5ea / 1606e328…9e5b；records 9e34e94d…d07c / e8ae3261…9dfb / 375e9ec5…b772；audits 11afdefc…7df6 / d7733761…8b90 / b6b747ec…925a；historical flags retained |
| MoMask-Pulp / native seed17 | Stage2 native formal Direct-H | VQ e21d42684e4441b67782b8951e1a5e6c9e5c25bbd1bc460aa7fda138ea348664；Mask 037871329eaf980e320961445f5492c7a79ad85d60e9e2b79640678dfabeff3c；Residual 89faab30ffb62d185a789a814ae7c061ed5f5375f9ce5128dc4764756c43e0b1 | native non-causal RVQ + MaskTransformer + ResidualTransformer + owning VQ decoder | eval contract 94a217f900e26212e523dd1f0444fbbba5e6392a7c424e0441bab19c02238901；result 3a133b834bfac8203a9bfb92cea55e0127f50369bc51c68a53bb3b0d877baf70；records 6545ab1a4e17bc13b73663aafd983b439ccae664b016251640dcc22a0e067ed8；formal audit 71bd4b1d31409a8e70e991715ee7a09ee1706384df39831ea575e9f4a2ff3232；byte-exact replay audit 0d7d549e64ff863da2f4815245c18ecb03d997ecc1cef3f423ae817c90f28c2e |
| v7.45 / MoLingo human | Stage2 240K formal Direct-H | 4669a56fb6c9a4adafc2cfedef39b27c060cd00949a7407c86c68cc9fa30200d | corrected v7.14 latent + owning decoder；offline bidirectional masked RF | contract 34544e1588a5af63614a1b04c50e2481c6f73ed97e21cfc3ab93ba657a2d163a；result 445695958ba86c11831cbc8f931939c71f72135453b21ca6b6d5e2f170b6f685；records 6edb7d5f9e54a61540b175028cad6911d5b573d4290e7dc95edc7e6fce122a9c |
| MotionLab-MFT / v7.14 latent | Stage2 30K formal Direct-H | 45477134830f25c58b6db2ea54cfdce4cadd8f0e84c0e9312f1ead73bce468dd | corrected v7.14 latent + owning decoder | contract a2f4d063bad486075084d9a66d06084a430f012d28356f42a4b161f8eaef8002；result f1a45654d740d8937152c96b75f88a53a765bc37977719d6628ccef6c36d79ba；records 2b6d42544e75ad330e01091e4a3a294a67e02f2fe0db17ba14fc12e5afdca765 |
| Director-C / native | Stage2 native formal Direct-C | ad27564052465ff11f5264c5606473f2daacaaf74abbf45adc7b563328b5e823 | native direct 9D C2W；GT pelvis trajectory；no StoryMotion tokenizer | contract 3a3635be17fa1c6cc155fa8e5ad7339d46e446c55195ec9ca1b350390addcaa1；result f9693592d62780dd2a4ed330dc2b102b88b775a839e459c6adefc6eb2bd97b15；records e0734d76e316dc5f66149214e2daf7cbdd42adaeec17c796a1897e88dfaf2e4a |
| CCD-Pulp / v7.14 latent | Stage2 60K formal Direct-C | 8014b120c218a7ce8bd7d6f6c3e381cc009939950926da847c4dc2597f6603da | v7.14 cache + owning decoder；GT-H latent | contract bb1818fb9703035d34bc691bdbffe82a3c9447c9c68a3b6010cd3387e5b93039；result f016ba46250c1bb4895aed14b447088852658c9ca025f2118244b0ff9a144e5b；records 19354e7949d004af4057269f432b47b6f33392a8ceb1da376b1e2a05c64ba9c0 |
| PulpMotion / official DiT-xy step92950 | Stage2 native formal joint | 7c11cb59d5f51b9090abc1448e76329d157459fc30485031f5a79a7a119660d9 | released Pulp AE + native sampler；same 4,053 IDs in native order | no-Aux result 499db08e4f957f178cebc9b8c5f07dbe53ed680bf1bce657c2b5438e1ebdbbf9；Aux result 5be1e1e30213e6415c0a057eca2a444af31c30614fea1517cbd2f2f3b637961d；no per-sample records artifact |

v7.47 official pure4053 ordered records SHA256：a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。v7.47 training script 与 L0 historical training script SHA256 分别为 71a9a2a3b700d4f0a699fda5f28bf8da72f563c20871e1c1cfb5d4d4cae0ac08 / f207c840fa363afc13e308047ddbe3900683f048366c10e9c135b49a2da886c8，因此 strict representation isolation 未建立。

### 6.3 Diagnostic artifacts

| version / run | diagnostic | artifact / comparison SHA256 |
| --- | --- | --- |
| v8.1C C3-25 D1 / continuous diagnostic | full train estimate + frozen eval cache geometry | artifact 2f5a64315d8cca23d3d432bb872bec55ba72fdb775ace37b26019c78c05002b1；script 98121fae2392aa0909b5847ac46c917d4f91751bc325cc42c3ffcfe51f593d50 |
| v8.1A D4 vs v7.36 D4 | raw residual propagation | candidate 142614050c5d94ae8e0e680327129a7893d64afcd0cc3ff0070aaf3b1a02274f；baseline d22a13b9c0974c7610f7142c3b73ac6876ed5fb368ca0cb8ee8808550519469a；comparison 13f9715b446a33d32181a231b2a4eb7bd17eddcb2044b8c2228cda8cd4e20727 |
| v8.1A D4.2 vs v7.36 D4.2 | Camera-text reliance | candidate 134195504286677d0a77c0da6ee7e8a897008525337a908b91506a301dedc795；baseline e8064825521865a74081c79f40b8d5481c72df1969521fd762eb27177ddf4148；comparison 8d98765900ee9f9683e84b3e2de309b66ae92733de41ce49490d9b149f5baed9 |
| v8.1A D4.3 r3 vs v7.36 r3 | decoder direction sensitivity | candidate 58b6f62c6004e2ef24f94bd831790058e0e799e29650f1622a0a44e9eee19d7f；baseline 370e30d190deb63e66e675defc26265c103fe1c62a860a982e577597ad8e5c07；comparison ff0df9c541f351827ae234700b25cf5f9f355ec369b0c9f7c8525de0ab7ef7ae |
| v8.1C C3-25 D4.3 vs v7.36 r3 | step30000 decoder direction sensitivity | contract 2c8294f034d1911900f308a11e183122900878b979964fa438b0ce5c163f1fa9；raw residual b82e1f6abc805237d7d702fb18ccb42f65142470eb7bce989ea973a0768689b2；candidate 88188b5459ed4835dea1d3c38039b6b3e5ca336aff9cbac218ec381855c8eaf6；comparison ff15128b9d36d79e718ef4556c26c157d1404e3932be165546b31005d32b7393 |

### 6.4 Evidence roots

    runs/eval/stage1/v7_14_official_contract_20260710/joint_ae_v8_schema_reaudit_20260718/
    runs/stage1/v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717/
    runs/stage1/v8_1c_center25pct_full636k_seed17_4090g0_20260719/
    runs/stage1/v8_1c_center25pct_full636k_seed23_5090g0_20260719/
    runs/stage1/v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719/
    runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/
    runs/train/stage2/v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719/
    runs/eval/stage2/v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719/
    runs/eval/stage2/v8_1c_c3_25_d43_decoder_sensitivity_n64_seed17_5090g0_20260719/
    runs/stage2/v7_47_official_ae_unified_matched_seed17_5090g0_20260717/eval/official_pure4053/
    runs/legacy/eval/stage2/v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714/
    runs/legacy/eval/stage2/v8_1a_diag_unified3_30k_seed17_4090g0_20260718/
    runs/legacy/eval/stage2/v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717/
    runs/legacy/eval/stage2/baseline_motionlab_mft_v714_human_seed17_4090g0_20260716/
    baselines/runs/momask_pulp_human_native_seed17_5090g3_stage1matched_20260716/
    baselines/runs/director_c_pure_matched_seed17_5090g3_20260716/
    baselines/runs/ccd_pulp_camera_completion_v714_seed17_4090g1_20260716/
    runs/eval/stage2/pulpmotion_official_matrix_20260616/full/

旧 v7.17–v7.35 collapse/condition diagnostics、v7.39–v7.45 operator screens 与 invalidation provenance 仍由原 run artifacts 保存；它们不再复制成第二套 current ranking。版本族中的已闭合 milestone 与 bug 入口见 [[version_family]]。

## C3-25 completion → joint 条件暴露归因（2026-07-21）

同一 C3-25 seed17 Unified-3 `105K` checkpoint；Pulp `pure_` test，`N=4053`，ordered IDs SHA256 `a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，seed17，DDIM50，CFG1，eta0，eval batch32，decode batch16。composition 是同 checkpoint 的非 gating root-cause attribution，不替代 active joint-parallel score。

### Camera 转化链

| version / run | profile | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | caption F1 ↑ | Out ↓ | Cam-ADE ↓ | Cam-FDE ↓ | Rot. deg ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Direct-C, clean GT-H | 25.091 | 59.539 | 0.7503 | 0.7645 | n/a | 1.591 | 1.668 | 35.298 |
| v8.1C C3-25 / `p0_c3_joint_conversion_seed17_4090g1_20260721` | GT-H replay | 25.207 | 59.475 | 0.7530 | 0.7652 | 0.1463 | 1.599 | 1.675 | 35.614 |
| v8.1C C3-25 / `p0_c3_joint_conversion_seed17_4090g1_20260721` | generated-H replay | 32.849 | 60.191 | 0.6546 | 0.7565 | 0.1516 | 2.788 | 2.875 | 68.655 |
| v8.1C C3-25 / `p0_c3_joint_conversion_seed17_4090g1_20260721` | shuffled generated-H replay | 39.674 | 59.652 | 0.6393 | 0.7554 | 0.1607 | 2.923 | 3.018 | 71.288 |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | joint-parallel | 70.580 | 46.720 | 0.6057 | 0.5988 | 0.1835 | 2.904 | 3.003 | 70.849 |

### Human carry-over

| version / run | profile | FDTMR ↓ | TMR ↑ | HCov ↑ | global MPJPE ↓ | root-aligned MPJPE ↓ | root ADE ↓ | root FDE ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Direct-H | 222.120 | 14.389 | 0.5275 | 0.846 | 0.241 | 0.754 | 1.275 |
| v8.1C C3-25 / `p0_c3_joint_conversion_seed17_4090g1_20260721` | generated-H replay | 217.883 | 14.408 | 0.5263 | 0.857 | 0.241 | 0.767 | 1.302 |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | joint-parallel | 227.189 | 13.691 | 0.5327 | 0.864 | 0.253 | 0.765 | 1.294 |

**审计结论**：GT-H replay 与 Direct-C 对齐，验证 composition evaluator 边界。generated-H replay 保留 Human completion 的大部分质量与 Camera text semantics，但 Camera coverage 和 paired geometry 显著退化，支持 clean-H → generated-H condition exposure gap。generated-H replay 又明显优于 joint-parallel 的 Camera distribution/semantics/caption，说明 parallel 中 evolving/noisy self-generated H 与 joint task 路由构成第二段损失。shuffled-H 的进一步退化确认 Camera head 实际使用 Human 条件。

**证据边界**：paired geometry 对 one-to-many free generation 是 mandatory diagnostic，不是单独 hard gate；本结论为单 seed、同 checkpoint root-cause attribution。shuffled-H 的 Human text/GT 配对被故意打乱，其 Human TMR 不解释为模型回归。v8.1A-105K budget control 与 matched full single-step 尚未闭合，不在本节给出结论。

### Artifact identity

- C3-25 `105K` checkpoint SHA256：`689201d2bc0ba215648a7272c932806f78fe7d4f450f2bd85534b27e8479ca27`
- Source contract SHA256：`7af1bf9a49a92609dcab1a1d176fee622b9ac844fc2add053982ed036e667851`
- Direct-H result / records：`704180110482a4db774e2d5deeb015873024f7ca54951af9c5e4f1c9f081216e` / `712020076d9eecfcb76d5ebc853b0d86f824d87c5349302864c4563f247d7a99`
- Direct-C result / records：`f713043df6f43cd4474b78968b4ce9a6ea1455b50b93d1ffbf0766bea075cc05` / `5ed0778004fa4972a23ad26cf395f31b3dc06272531a30dad19b58a8c60a3895`
- joint-parallel result / records：`b0d8f936aca06d89caf980f0ae482ef177ea571086f9d6791d89ef935cbbf2eb` / `81945ad3cbe533ac7fdf6893b1b3c33352466f15f744f5df1a36998d659cd725`
- GT-H replay result / records / audit：`6eceb3430eede08eb5ac5a49015932e03131bc762ef89ee98e494c6eae711c9a` / `f80f54f8092f1a3521eeaf1f846cd41f30f9a64dd19ecec2fe79ffb084c3d16b` / `19da362eba46c020ebb890a3285f28a934952aae5a31e0045e465a3b40546f04`
- generated-H replay result / records / audit：`9d92edd0900eb694e55a0a82bd895142dcf50933b780fee167246ad0b9896a7e` / `3c6cc3ae8c395c31f7e2569060e30c49366b8498a7aa416c892e82973f284d95` / `efeb2c49200d9c76ecec1421462c44558d708272b46005314775824e53a411d4`
- shuffled generated-H replay result / records / audit：`2e6805faa59b4c291a7407734cd2ed5a5070f2f7aff36f6acda24be5ba65ad49` / `456a60f3a846337478d5941d41e2b56232b765444bf8b9a8363dd94d17f69f8c` / `79214c0065cd2d4e1804b92f8eb013d8d4ef5bd14170a020330f540b3f88ac20`

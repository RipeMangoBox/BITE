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
updated: 2026-07-19T20:16:00+08:00
---

# StoryMotion Valid Metric Ledger

> [!abstract] Canonical contract
> 本页只拥有已经审计的数值、比较边界和 artifact hashes。Stage1 reconstruction、Stage2 generation、30K diagnostic screen 与 105K formal evidence 分区记录；除明确标为 diagnostic 的 N64/short rows 外，正式表均为 official pure 4,053。当前裁决见 [[current]]，版本名称与完成 step 见 [[version_family]]，指标定义见 [[StoryMotion-metric-computation-io]]。

> [!important] C3-25 当前证据边界
> v8.1C C3-25 seed17/seed23 都完成了 Stage1 636K 与 pure4053 reconstruction audit。seed17 此后按用户授权建立了独立、审计通过的 diagnostic-only Stage2 cache，并启动 continuous `0→105K` run；当前尚无 C3 的 Stage2 `30K/105K` 正式结果，因此本页不提前填分。seed23 仍只有 Stage1。下文已有的 Stage2 30K 数值仍只属于父候选 v8.1A。

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
| v7.14 / joint AE official r2 | Stage1 636K | reconstruction | 4,053 | current implementation mainline |
| v7.38 L0 / clean 105K | Stage2 105K | Direct-H、Direct-C、parallel | 4,053 | current formal mainline |
| v7.47 / official-AE Unified 105K | Stage2 105K | Direct-H、Direct-C、parallel | 4,053 | S-tier system control |
| PulpMotion / official DiT-xy step92950 | Stage2 native endpoint | joint | 4,053 | C-tier native-system baseline |
| v7.36 A30 vs v8.1A G3 | Stage2 30K | Direct-H、Direct-C、parallel | 4,053 | matched generatability screen，不与 105K 排名混合 |

全表 formal ordered-ID SHA256：a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。

## 2. Stage1 reconstruction

### 2.1 Semantic/distribution anchors

| version / run | Stage / budget | tier | samples | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GT identity / pure4053 | reference | reference | 4,053 | 0.00 | 16.47 | 100.0% | 0.00 | 70.24 | 100.0% | 0.945 | 0.7% |
| Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 pretrained | C | 4,053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |
| v7.14 / joint AE official r2 | Stage1 636K | mainline | 4,053 | 31.10 | 14.99 | 97.9% | 0.48 | 69.46 | 99.5% | 0.927 | 5.1% |
| v7.14 / joint VAE official r2 | Stage1 636K | control | 4,053 | 69.61 | 13.77 | 93.1% | 2.28 | 68.45 | 97.7% | 0.914 | 7.9% |

GT 与 reconstruction rows 可直接解释 paired reconstruction；它们不能在 Stage2 one-to-many generation 表中被当成可训练方法的胜者。

### 2.2 Overall geometry

距离为 mm，角度为 degree。v7.14 与全部 v8 rows 使用同一 v8-schema evaluator、true length、pure4053 ordered IDs；Pulp official 与 MotionStreamer 保留各自 owning decoder，属于 system-level baseline。

| version / run | Stage / budget | tier | RA / global MPJPE ↓ | root ADE / FDE ↓ | yaw ↓ | Cam-ADE / FDE ↓ | rotation ↓ | RA / global slope per 100f | gate / status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | 0 / 0 | 0 / 0 | 0 | 0 / 0 | 0 | 0 / 0 | reference only |
| Pulp official AE / aemmardm-xgmj0yjj-325 | Stage1 pretrained | C | 80.254 / 181.053 | 150.145 / 595.955 | — | 137.449 / 277.227 | 1.792 | −7.000 / −10.340 | native baseline |
| MotionStreamer-Pulp / 500ep seed17 | Stage1 native 500 epochs | C | 79.937 / 281.524 | — | — | — | — | — | standalone causal baseline only |
| v7.14 / joint AE official r2 | Stage1 636K | mainline | 80.731 / 212.735 | 169.640 / 415.430 | 21.640 | 41.760 / 51.500 | 0.619 | +29.020 / +145.300 | implementation mainline |
| v8.1A / yaw001-root003 seed17 | Stage1 636K | candidate | 24.700 / 71.180 | 60.188 / 150.914 | 5.113 | 47.693 / 56.039 | 0.717 | +2.888 / +31.103 | global slope fail；no promotion |
| v8.1C C2 / center100 seed17 | Stage1 636K | treatment | 25.927 / 74.406 | 62.688 / 158.011 | 5.360 | 31.956 / 41.183 | 0.859 | +4.641 / +38.799 | global slope + rotation fail |
| v8.1C C3-25 / seed17 selected | Stage1 636K | candidate | 24.570 / 69.243 | 58.252 / 148.365 | 4.947 | 39.486 / 48.270 | 0.705 | +1.148 / +26.302 | only global slope fail；exact non-promotion Stage2 diagnostic parent |
| v8.1C C3-25 / seed23 robustness | Stage1 636K | robustness | 24.699 / 70.804 | 59.797 / 142.732 | 4.957 | 39.053 / 46.705 | 0.776 | +0.444 / +27.594 | global slope + rotation fail；no Stage2 |
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
| 1–64 | 1,805 | v7.14 / joint AE official r2 | Stage1 mainline | 70.806 / 146.844 | 43.220 / 50.651 | 0.825 |
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
| 65–128 | 1,411 | v7.14 / joint AE official r2 | Stage1 mainline | 77.327 / 208.582 | 39.165 / 47.671 | 0.517 |
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
| 129–192 | 456 | v7.14 / joint AE official r2 | Stage1 mainline | 87.527 / 305.344 | 39.103 / 54.846 | 0.363 |
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
| 193+ | 381 | v7.14 / joint AE official r2 | Stage1 mainline | 132.220 / 429.428 | 47.637 / 65.692 | 0.326 |
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

| version / run | Stage / type | diagnostic | key audited result | authorization |
| --- | --- | --- | --- | --- |
| C0 / gradient calibration | Stage1 read-only | Camera-center unit gradient | C1 weight 0.00406677828128799 = raw-center target 5% | only freezes C1 scale |
| C4 / gradient calibration | Stage1 read-only | rotation vs horizon | cosine −0.00624；C4-R weight 0.00008010673098572695；C4-H weight 0.018266197084257824 | C4-R not run；C4-H short only |
| C5-A / pure4053 alignment | Stage1 read-only | last-valid vs four-anchor multi-horizon | global-MPJPE Spearman all 0.67580→0.77947；193+ 0.70027→0.75837 | only supports a future preregistration；no training |
| C5-B / fresh calibration seed17/23 | Stage1 read-only train-distribution | four-anchor multi-horizon unit gradient vs C3 parent | recommendations 0.04087558783454605 / 0.041733939559882145；max/min 1.020999；frozen base 0.041302533967803944 | freezes dose0.5=0.020651266983901972 and dose1.0=0.041302533967803944 for matched shorts only |

C5-A 的 trained-endpoint estimated weight 0.008456624012361412 不是 fresh-init training dose。pure4053 已参与候选选择，后续 promotion 必须另冻结 sealed audit set。

## 3. Stage2 formal 105K evidence

### 3.1 v7.38 matched five-arm family

L0–L4 都从 v7.36 A30 恢复 optimizer，到 Stage2 step 105,000；共享 seed17、batch512、v7.14 non-causal cache/decoder、train-only full-cov stats、pure4053 与 DDIM50/CFG1/eta0。它们彼此可作 same-family matched comparison。

| version / run | Stage / budget | Direct-H FDTMR / TMR / HCov | Direct-C FDCLaTr / CLaTr / CCov / F1 | decision |
| --- | --- | ---: | ---: | --- |
| v7.38 L0 / clean | Stage2 105K | 333.88 / 13.294 / 40.54% | 33.29 / 55.640 / 73.23% / 0.715 | formal mainline |
| v7.38 L1 / noisy-H | Stage2 105K | 319.80 / 13.087 / 41.4% | 63.98 / 51.339 / 68.5% / 0.677 | camera regression |
| v7.38 L2 / human curriculum | Stage2 105K | 296.32 / 13.163 / 47.0% | 50.60 / 52.792 / 70.1% / 0.681 | Human/cascade Pareto；not mainline |
| v7.38 L3 / camera temporal | Stage2 105K | 307.50 / 12.388 / 45.4% | 82.26 / 48.699 / 61.7% / 0.660 | camera forgetting |
| v7.38 L4 / unified temporal | Stage2 105K | 290.37 / 13.287 / 46.5% | 85.40 / 47.682 / 61.8% / 0.632 | camera forgetting |

| version / run | Stage / budget | parallel H FDTMR / TMR / HCov | parallel C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.38 L0 / clean | Stage2 105K | 282.37 / 14.420 / 48.98% | 58.96 / 47.129 / 65.68% / 0.569 | 21.69% | formal mainline |
| v7.38 L1 / noisy-H | Stage2 105K | 285.35 / 11.820 / 48.5% | 94.48 / 43.392 / 60.1% / 0.544 | 21.0% | camera regression |
| v7.38 L2 / human curriculum | Stage2 105K | 288.45 / 11.571 / 47.6% | 80.17 / 43.933 / 62.9% / 0.540 | 24.3% | not mainline |
| v7.38 L3 / camera temporal | Stage2 105K | 275.54 / 11.728 / 47.9% | 101.96 / 39.857 / 55.0% / 0.494 | 24.7% | camera forgetting |
| v7.38 L4 / unified temporal | Stage2 105K | 298.53 / 10.725 / 45.1% | 120.40 / 37.184 / 48.8% / 0.444 | 29.7% | camera forgetting |

### 3.2 Direct-H fair system table

Human completion contract：human text → H。GT 是 identity reference；观察 Camera latent 的 symmetric control 不在本表。

| version / run | Stage / budget | tier | FDTMR ↓ | TMR ↑ | HCov ↑ | RA / global MPJPE ↓ | root ADE / FDE ↓ | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | 0 | 16.47 | 100% | 0 / 0 mm | 0 / 0 mm | not a generator |
| v7.38 L0 / clean | Stage2 105K | mainline | 333.880 | 13.294 | 40.54% | 250.364 / 863.112 mm | 769.275 / 1,280.066 mm | formal |
| v7.47 / official-AE Unified | Stage2 105K | S | 228.966 | 18.424 | 33.31% | 196.083 / 807.756 mm | 740.720 / 1,301.127 mm | formal；strict isolation not established |
| v7.42 / same-impl Human specialist | Stage2 task-exposure matched | A | 328.620 | 13.438 | 42.22% | — | — | formal |
| v7.45 / MoLingo human | Stage2 240K human-only | B | 149.163 | 17.729 | 49.86% | 242.502 / 1,249.134 mm | 1,164.249 / 2,007.279 mm | semantic signal；geometry no-promotion |
| MotionLab-MFT / v7.14 latent | Stage2 30K human-only | B | 156.350 | 18.172 | 59.19% | 250.782 / 951.380 mm | 857.640 / 1,436.396 mm | formal system peer |
| MoMask-Pulp / native | Stage2 native training complete | C | — | — | — | — | — | VQ/Mask/Residual complete；formal adapter/eval pending |

### 3.3 Direct-C fair system table

Camera completion contract：observed/GT H + camera text → C。

| version / run | Stage / budget | tier | human condition | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Cam-ADE / FDE ↓ | rotation ↓ | status |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | GT-H | 0 | 70.24 | 100% | 0.945 | 0 / 0 m | 0° | not a generator |
| v7.38 L0 / clean | Stage2 105K | mainline | GT-H latent | 33.290 | 55.640 | 73.23% | 0.715 | 1.512 / 1.606 m | 32.926° | formal |
| v7.47 / official-AE Unified | Stage2 105K | S | GT-H in official basis | 17.876 | 60.158 | 83.69% | 0.774 | 0.152 / 0.256 m | 2.084° | formal；strict isolation not established |
| v7.42 / same-impl Camera specialist | Stage2 task-exposure matched | A | GT-H latent | 33.060 | 58.334 | 76.63% | 0.750 | — | — | formal |
| Director-C / native | Stage2 15.299M exposures | C | GT pelvis trajectory | 32.440 | 52.662 | 81.49% | 0.688 | — | — | formal native-system peer |
| CCD-Pulp / v7.14 latent | Stage2 60K × 256 | B | GT-H latent | 101.030 | 33.095 | 59.91% | 0.442 | — | — | formal；L0 dominates primary metrics |

### 3.4 Joint parallel fair system table

Active joint profile 是 directed parallel。PulpMotion rows 使用 released AE 与 native sampler，属于 C-tier；它们不能解释为 StoryMotion representation ablation。

| version / run | Stage / budget | tier | H FDTMR / TMR / HCov | C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | H RA / global ↓ | Cam-ADE / FDE / rotation ↓ | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| GT identity / pure4053 | reference | reference | 0 / 16.47 / 100% | 0 / 70.24 / 100% / 0.945 | 0.7% | 0 / 0 mm | 0 / 0 m / 0° | not a generator |
| v7.38 L0 / clean | Stage2 105K | mainline | 282.370 / 14.420 / 48.98% | 58.960 / 47.129 / 65.68% / 0.569 | 21.69% | 252.670 / 842.297 mm | 2.912 / 3.026 m / 72.928° | formal mainline |
| v7.47 / official-AE Unified | Stage2 105K | S | 205.336 / 17.303 / 37.75% | 156.755 / 24.563 / 47.00% / 0.239 | 7.96% | 199.053 / 890.543 mm | 2.960 / 3.063 m / 69.212° | Human signal；Camera broad regression |
| v7.42 / same-impl joint specialist | Stage2 task-exposure matched | A | 300.470 / 12.605 / 45.03% | 66.810 / 45.029 / 63.76% / 0.570 | 19.33% | — | — | formal |
| PulpMotion / official DiT-xy no-Aux step92950 | Stage2 native endpoint | C | 375.010 / 20.532 / 14.90% | 94.840 / 35.691 / 48.33% / 0.491 | 39.54% | — | — | formal native baseline |
| PulpMotion / official DiT-xy Aux step92950 | Stage2 native endpoint | C | 414.800 / 21.657 / 13.82% | 93.270 / 37.777 / 44.81% / 0.513 | 28.47% | — | — | formal native baseline |

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
| 1–64 | 1,805 | v7.38 L0 / clean | Stage2 105K mainline | 253.586 / 677.934 | — |
| 1–64 | 1,805 | v7.47 / official-AE Unified | Stage2 105K S | 212.067 / 638.744 | 554.517 / 958.293 |
| 1–64 | 1,805 | v7.45 / MoLingo human | Stage2 B | 251.390 / 842.422 | — |
| 1–64 | 1,805 | MotionLab-MFT / v7.14 latent | Stage2 B | 260.438 / 752.649 | — |
| 65–128 | 1,411 | v7.38 L0 / clean | Stage2 105K mainline | 249.884 / 895.589 | — |
| 65–128 | 1,411 | v7.47 / official-AE Unified | Stage2 105K S | 188.249 / 851.014 | 792.751 / 1,407.208 |
| 65–128 | 1,411 | v7.45 / MoLingo human | Stage2 B | 235.229 / 1,310.340 | — |
| 65–128 | 1,411 | MotionLab-MFT / v7.14 latent | Stage2 B | 241.908 / 991.529 | — |
| 129–192 | 456 | v7.38 L0 / clean | Stage2 105K mainline | 234.630 / 1,135.359 | — |
| 129–192 | 456 | v7.47 / official-AE Unified | Stage2 105K S | 166.025 / 1,062.929 | 1,017.026 / 1,843.047 |
| 129–192 | 456 | v7.45 / MoLingo human | Stage2 B | 221.093 / 1,697.425 | — |
| 129–192 | 456 | MotionLab-MFT / v7.14 latent | Stage2 B | 231.113 / 1,242.231 | — |
| 193+ | 381 | v7.38 L0 / clean | Stage2 105K mainline | 255.706 / 1,294.288 | — |
| 193+ | 381 | v7.47 / official-AE Unified | Stage2 105K S | 185.344 / 1,142.850 | 1,099.478 / 1,883.859 |
| 193+ | 381 | v7.45 / MoLingo human | Stage2 B | 252.949 / 2,412.741 | — |
| 193+ | 381 | MotionLab-MFT / v7.14 latent | Stage2 B | 261.443 / 1,396.085 | — |

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

## 4. Stage2 30K matched generatability screen

v7.36 A30 与 v8.1A G3 共享 Unified-3 implementation、optimizer、batch、task probabilities、seed17、pure4053、DDIM50、CFG1、eta0 与 evaluator。必然不同的 Stage1 checkpoint、owning decoder、cache 和 train-only stats 被显式绑定，因此它回答 representation-system generatability，不是 Stage1 promotion。

### 4.1 Primary metrics plus overall geometry

| version / run | Stage / budget | Direct-H FDTMR / TMR / HCov | RA / global MPJPE ↓ | root ADE / FDE ↓ | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.36 A30 / matched control | Stage2 30K | 399.729 / 11.391 / 33.11% | 0.260 / 0.924 m | 0.826 / 1.348 m | comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K | 272.434 / 11.841 / 47.99% | 0.268 / 0.884 m | 0.781 / 1.299 m | Human signal |

| version / run | Stage / budget | Direct-C FDCLaTr / CLaTr / CCov / F1 | Cam-ADE / FDE ↓ | rotation ↓ | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.36 A30 / matched control | Stage2 30K | 114.568 / 35.067 / 61.56% / 0.463 | 1.994 / 2.147 m | 44.847° | comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K | 178.234 / 25.219 / 46.51% / 0.254 | 2.022 / 2.145 m | 46.974° | broad Camera regression |

| version / run | Stage / budget | parallel H FDTMR / TMR / HCov | parallel C FDCLaTr / CLaTr / CCov / F1 | Out ↓ | H RA / global ↓ | Cam-ADE / FDE / rotation ↓ | decision |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| v7.36 A30 / matched control | Stage2 30K | 348.889 / 12.450 / 39.18% | 110.360 / 29.933 / 58.97% / 0.366 | 31.93% | 0.267 / 0.894 m | 3.243 / 3.342 m / 81.092° | comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K | 245.886 / 12.439 / 50.41% | 195.453 / 21.856 / 44.88% / 0.223 | 34.59% | 0.269 / 0.877 m | 2.797 / 2.920 m / 72.151° | Camera semantic/distribution regression |

G3 status：stop_30k_broad_camera_regression。v8.1A 不续 105K；该结果也不能转移给 C3-25。

### 4.2 Geometry by valid length

同一 valid length 放在一起并递增；距离为 m。

| valid length | n | version / run | Stage / profile | H RA / global ↓ | Cam-ADE / FDE ↓ | rotation ↓ |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| 1–64 | 1,805 | v7.36 A30 | Stage2 30K Direct-H | 0.266 / 0.726 | — | — |
| 1–64 | 1,805 | v8.1A G3 | Stage2 30K Direct-H | 0.275 / 0.698 | — | — |
| 1–64 | 1,805 | v7.36 A30 | Stage2 30K Direct-C | — | 1.995 / 2.084 | 47.937 |
| 1–64 | 1,805 | v8.1A G3 | Stage2 30K Direct-C | — | 1.994 / 2.048 | 49.231 |
| 1–64 | 1,805 | v7.36 A30 | Stage2 30K parallel | 0.276 / 0.711 | 3.115 / 3.179 | 80.874 |
| 1–64 | 1,805 | v8.1A G3 | Stage2 30K parallel | 0.276 / 0.697 | 2.652 / 2.720 | 71.199 |
| 65–128 | 1,411 | v7.36 A30 | Stage2 30K Direct-H | 0.257 / 0.965 | — | — |
| 65–128 | 1,411 | v8.1A G3 | Stage2 30K Direct-H | 0.264 / 0.926 | — | — |
| 65–128 | 1,411 | v7.36 A30 | Stage2 30K Direct-C | — | 1.950 / 2.113 | 42.608 |
| 65–128 | 1,411 | v8.1A G3 | Stage2 30K Direct-C | — | 2.029 / 2.161 | 46.317 |
| 65–128 | 1,411 | v7.36 A30 | Stage2 30K parallel | 0.261 / 0.935 | 3.217 / 3.320 | 80.361 |
| 65–128 | 1,411 | v8.1A G3 | Stage2 30K parallel | 0.265 / 0.907 | 2.839 / 2.976 | 73.252 |
| 129–192 | 456 | v7.36 A30 | Stage2 30K Direct-H | 0.244 / 1.219 | — | — |
| 129–192 | 456 | v8.1A G3 | Stage2 30K Direct-H | 0.252 / 1.123 | — | — |
| 129–192 | 456 | v7.36 A30 | Stage2 30K Direct-C | — | 1.989 / 2.234 | 42.647 |
| 129–192 | 456 | v8.1A G3 | Stage2 30K Direct-C | — | 2.028 / 2.220 | 45.477 |
| 129–192 | 456 | v7.36 A30 | Stage2 30K parallel | 0.248 / 1.175 | 3.431 / 3.551 | 82.321 |
| 129–192 | 456 | v8.1A G3 | Stage2 30K parallel | 0.250 / 1.133 | 2.976 / 3.159 | 75.284 |
| 193+ | 381 | v7.36 A30 | Stage2 30K Direct-H | 0.261 / 1.353 | — | — |
| 193+ | 381 | v8.1A G3 | Stage2 30K Direct-H | 0.269 / 1.319 | — | — |
| 193+ | 381 | v7.36 A30 | Stage2 30K Direct-C | — | 2.153 / 2.463 | 41.128 |
| 193+ | 381 | v8.1A G3 | Stage2 30K Direct-C | — | 2.121 / 2.454 | 40.509 |
| 193+ | 381 | v7.36 A30 | Stage2 30K parallel | 0.267 / 1.279 | 3.727 / 3.939 | 83.363 |
| 193+ | 381 | v8.1A G3 | Stage2 30K parallel | 0.268 / 1.308 | 3.114 / 3.370 | 68.826 |

## 5. D4 family：Stage2 30K frozen diagnostics

D4/D4.2/D4.3 都是 v8.1A G3 的 N64 read-only diagnostics；t=50/500/950 是 diffusion timestep，不是训练 step。它们不训练、不写 cache、不授权 105K。

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

| version / run | diffusion t | center actual v7.36→v8.1A | center cand/base | center actual/random | rotation actual v7.36→v8.1A | rotation cand/base | rotation actual/random | preregistered rule |
| --- | ---: | --- | ---: | ---: | --- | ---: | ---: | --- |
| v8.1A D4.3 r3 vs v7.36 r3 | 50 | 2.740→3.417 | 1.247× | 2.470× | 46.652→52.504 | 1.125× | 2.360× | center + rotation pass |
| v8.1A D4.3 r3 vs v7.36 r3 | 500 | 3.079→3.290 | 1.069× | 2.287× | 57.817→53.394 | 0.923× | 2.449× | cand/base fail |
| v8.1A D4.3 r3 vs v7.36 r3 | 950 | 3.460→3.073 | 0.888× | 1.958× | 68.347→71.821 | 1.051× | 3.096× | outside rule；cand/base fail |

最窄结论：Camera text 被使用，但 near-manifold 的低噪 residual 更集中命中 v8.1A owning decoder 的 Camera 高敏方向。责任是 Stage1 manifold/decoder 与 Stage2 objective/response 的 cross-stage calibration mismatch，不能单独归给某一 Stage。

> [!warning] D4.3 stats uncertainty
> v8.1A parent contract 的 expected pre-resume stats SHA256 为 605049fa…71feb，当前文件为 94805397…5adc4，embedded train-cache 为 3b55223d…bd22。旧 serialization 已不存在，无法 tensor-by-tensor 追溯；r3 仅在显式记录三者后运行。因此 D4.3 永久是 diagnostic-only。

## 6. Provenance registry

### 6.1 Stage1 core artifacts

| version / run | Stage / status | checkpoint / owning-decoder SHA256 | geometry SHA256 | contract / audit SHA256 |
| --- | --- | --- | --- | --- |
| v7.14 / joint AE official r2 | Stage1 mainline | 91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1 | abac845f8eac2b3c6da9beeabc02d26058e17b2007fa93d60dda54e7c3ee5248 | evaluator a52aba4d6260aeefac4e5891fbe510322bf6eaf12ce98e3d0bda16ffbc8ddf5e |
| v8.1A / yaw001-root003 seed17 | Stage1 full | ac47c2191c44d6368a5468510975cefcf0efd1338b03ace50266830c344151f1 | same-script evaluator above | owning checkpoint verified |
| v8.1C C2 / center100 seed17 | Stage1 full no-promotion | f16fb879eb7feebbebba10d24c6039cfec4fbc7812492fadedd9cb5c9c73530e | 0f4cddf17fd15a4b73afeff17c2b489702f237928b099d9d699340eba2f31d96 | contract 904ae14866b0a62fed37cc0b09de5f6bf9d177f81cfcfea760fb96247bdcdac8 |
| v8.1C C3-25 / seed17 selected | Stage1 full；exact Stage2 diagnostic parent | d0abb3268b14c19aada48fd2b9242fbbb03e9d808959539cac47f33448e4788a | 8b0ab3ba82f85192adeb066d99ce6a07f0fe645b2e916300c96e16b4aad43f4d | contract 80fbf5743aab7517acbfe9bcff6cde4311ce9257cd477e7af5baa658c2de6e73；audit 75d2daf8cd39d91affae8181cfb1365efb3a52bfbc85f50a1cdc6b7d90cf9b15 |
| v8.1C C3-25 / seed23 robustness | Stage1 full no-Stage2 | c73027b8f4c114c1c2ba54994c576592cb3f223dd7117fac7188dba9a7b0d3ad | 8e5a44cb586eeba1cbaeca82ee2b731badfa4dab4f15c40f11ccb7140f3a1b34 | contract 32ce7f8d1a91c75afe821659a2235d3ed05f8878380b79a7c7dd44a4e20bb4c1 |
| v8.1C C3-50 / seed17 exploratory | Stage1 full no-Stage2 | 4c9b51778104aef3e85f2664086a22802988a9a23833181026c6facdab608d98 | c0bb55bb244011ebffad5911d9ba43a7b4ba1b28bcc031a6df58e0f2158f89fc | contract 98a5aa0c00c14b30bb23c6a4ac1fe80a4397216f408f3ef3d48196c92edca8c3 |
| v8.1C C5-B / fresh calibration seed17/23 | Stage1 read-only；doses frozen | no checkpoint | seed17 c5755cf277da27fb62bba9518239af2a55eb9156acd994b196d1e665860832d5；seed23 561b1c4f43f59a06012b1585c49a58729d02d0a3382db5fc86e6d434137cf0c7；frozen doses 9042aa679a97c41b75fd9b2eb8b7854f141bc55c5df8a5bc4d0a153f3d6ab720 | contract c735a9c4aa7c7bcc8a56924bf2266d93333244d5f1f232b8114930e18b3b32c0 |

Stage1 train/eval ordered-ID SHA256：a0981b6c6223409d656ad8c43cfcf95cae6ec9a28640143b87b6322292c51dc9 / a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。

### 6.2 Stage2 core artifacts

| version / run | Stage / status | checkpoint SHA256 | owning decoder / cache boundary | contract / audit |
| --- | --- | --- | --- | --- |
| v7.38 L0 / clean | Stage2 105K mainline | ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35 | v7.14 owning decoder | 20/20 family artifacts audited |
| v7.47 / official-AE Unified | Stage2 105K S-control | b8c06913a5efdbaa0c178e452998352033174614aa0a60ad96920fe14a8acbb2 | decoder e0ff0a66129d77eb27a18d0034b23f692aaec3ef53afd540097d8d9544a73e52；train/eval cache 1924c632…d1e8 / c642f7c7…d1d3 | contract 37d61e28076735979731e47712500cee016365a4e9e2eb7753d93a10416dee51 |
| v7.36 A30 / matched control | Stage2 30K | 7dcf3b1911af144ea9ef2b30017dd07472d62f655fd04c1dc9263581e3382c0b | v7.14 decoder 91248bf4…7ce1；cache f7a00a48…a5983 / 6f13816c…9b25 | matched comparator |
| v8.1A G3 / diagnostic Unified | Stage2 30K stopped | becc2c11051bfd7857acb0602f61c755cd664969f34acef1f0232711feee5bb8 | v8.1A decoder ac47c219…151f；cache 3b55223d…bd22 / 1050748f…541d | contract c841fda54b8611d27b59aeaa3ca3c74c26865eee100428828df8c1e73ca5ab59 |
| v8.1C C3-25 / continuous diagnostic | Stage2 `0→105K` active；no metric row yet | pending 30K/105K immutable checkpoints | C3-25 decoder d0abb326…4788a；train/eval cache bc8c847e…3fa9 / 39485590…f5d6；full-cov stats 0c97d247…3400 | contract 2351a6f0…877；audit eb28815a…1fb；diagnostic-only |

v7.47 official pure4053 ordered records SHA256：a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93。v7.47 training script 与 L0 historical training script SHA256 分别为 71a9a2a3b700d4f0a699fda5f28bf8da72f563c20871e1c1cfb5d4d4cae0ac08 / f207c840fa363afc13e308047ddbe3900683f048366c10e9c135b49a2da886c8，因此 strict representation isolation 未建立。

### 6.3 D4 artifacts

| version / run | diagnostic | artifact / comparison SHA256 |
| --- | --- | --- |
| v8.1A D4 vs v7.36 D4 | raw residual propagation | candidate 142614050c5d94ae8e0e680327129a7893d64afcd0cc3ff0070aaf3b1a02274f；baseline d22a13b9c0974c7610f7142c3b73ac6876ed5fb368ca0cb8ee8808550519469a；comparison 13f9715b446a33d32181a231b2a4eb7bd17eddcb2044b8c2228cda8cd4e20727 |
| v8.1A D4.2 vs v7.36 D4.2 | Camera-text reliance | candidate 134195504286677d0a77c0da6ee7e8a897008525337a908b91506a301dedc795；baseline e8064825521865a74081c79f40b8d5481c72df1969521fd762eb27177ddf4148；comparison 8d98765900ee9f9683e84b3e2de309b66ae92733de41ce49490d9b149f5baed9 |
| v8.1A D4.3 r3 vs v7.36 r3 | decoder direction sensitivity | candidate 58b6f62c6004e2ef24f94bd831790058e0e799e29650f1622a0a44e9eee19d7f；baseline 370e30d190deb63e66e675defc26265c103fe1c62a860a982e577597ad8e5c07；comparison ff0df9c541f351827ae234700b25cf5f9f355ec369b0c9f7c8525de0ab7ef7ae |

### 6.4 Evidence roots

    runs/eval/stage1/v7_14_official_contract_20260710/joint_ae_v8_schema_reaudit_20260718/
    runs/stage1/v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717/
    runs/stage1/v8_1c_center25pct_full636k_seed17_4090g0_20260719/
    runs/stage1/v8_1c_center25pct_full636k_seed23_5090g0_20260719/
    runs/stage1/v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719/
    runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/
    runs/stage2/v7_47_official_ae_unified_matched_seed17_5090g0_20260717/eval/official_pure4053/
    runs/legacy/eval/stage2/v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714/
    runs/legacy/eval/stage2/v8_1a_diag_unified3_30k_seed17_4090g0_20260718/

旧 v7.17–v7.35 collapse/condition diagnostics、v7.39–v7.45 operator screens 与 invalidation provenance 仍由原 run artifacts 保存；它们不再复制成第二套 current ranking。版本族中的已闭合 milestone 与 bug 入口见 [[version_family]]。

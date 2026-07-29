---
title: "StoryMotion Valid Metric Ledger"
status: active
hypothesis: |
  StoryMotion decisions require decoded numeric evidence separated by stage,
  generation mode, representation owner, cohort, sampler, and eligibility.
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
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
  - "[[2026-07-29_full_re]]"
created: 2026-07-12T12:15:00+08:00
updated: 2026-07-29T15:38:19+08:00
---

# StoryMotion Valid Metric Ledger

> [!abstract] Canonical numeric owner
> 本页只拥有审计数值、公平对比与不可比边界。所有 checkpoint、cache、contract、result、records、ordered-ID、visual 与 implementation SHA256 集中在 [[Storymotion-exp-sha]]；当前决策见 [[current]]。Stage1 reconstruction 与 Stage2 generation 分区，不把 diagnostic-only 结果写成 promotion evidence。

## 1. Evidence contract

- 数值必须来自完整 sampler 输出经 owning decoder 解码后的机器可读结果；手工观察只作为 visual verdict。
- 所有 StoryMotion Stage1/Stage2 活动路径要求 is_causal=false。
- mixed-version 表逐行给出非空 version / run；若 cohort、sampler、decoder 或 representation 不同，紧邻表格声明限制。
- Direct-H 是 Human text-only；Direct-C 是 observed Human latent + Camera text；joint parallel 是同 checkpoint 自由生成 Human 与 Camera。
- cascade 只作历史归因，不是 active score 或 promotion gate。
- paired geometry 是 one-to-many generation 诊断，不独立作为 hard gate；root-aligned MPJPE 移除 root translation 但不移除 heading。
- 所有身份与产物边界只见 [[Storymotion-exp-sha]]，本页不再混排 SHA 行、列或表。

## 2. Canonical decoded-generation schema

| branch | family | primary fields | boundary |
| --- | --- | --- | --- |
| Human | semantic/retrieval | FDTMR、TMR、coverage、density、precision、recall、R1/R2/R3、MM distance | FDTMR 与 MM distance↓；其余↑ |
| Human | paired geometry | global MPJPE、root-aligned MPJPE、root ADE/FDE、integrated yaw | paired diagnostic；root-aligned 仍含 heading |
| Human | physical/kinematic | bone CV、joint/root speed/acceleration/jerk、contact/skate heuristic | 与同 cohort reference 对照；contact 未标定 ground |
| Camera | semantic/retrieval | FDCLaTr、CLaTr、coverage、density、precision、recall、R1/R2/R3、MM distance | FDCLaTr 与 MM distance↓；其余↑ |
| Camera | caption/geometry | caption P/R/F1、Cam ADE/FDE、rotation | ↓或↑方向见表头 |
| Camera | projection/framing | r-FPD、Out | ↓；禁用 callback 产生的恒零字段不进入结果 |
| joint parallel | Human + Camera | 同 checkpoint 同时报告上述两分支与 generated-H projective fields | 不与 observed-H Direct-C 混写 |

## 3. Stage2 fair comparison and v9 redesign evidence

### 3.1 Comparison boundary

- pure4053 formal rows 使用完整 Pulp pure-test cohort，并继续拥有 promotion evidence。
- first512 matched rows 使用完全相同的 ordered cohort。只有这些 rows 可以直接做 cohort-matched C3 与 v9 对照。
- v9 使用 redesign Pulp-only representation、shifted-sigma Euler50、CFG3 与 phased Camera schedule；C3 使用 C3-25 representation、DDIM50、CFG1 与原 Unified schedule。因此这是 system/representation comparison，不是单变量 backbone ablation。
- v9 合约明确 diagnostic-only / not promotion-eligible。全部 identity 见 [[Storymotion-exp-sha]]。

### 3.2 Direct-H fair table

| version / run | cohort | mode | FDTMR ↓ | TMR ↑ | HCov ↑ | density ↑ | precision ↑ | recall ↑ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| v8.1C C3-25 / v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719 | pure4053 formal | Direct-H | 222.120 | 14.389 | 0.5275 | 0.5403 | 0.7091 | 0.5764 | 0.8455 / 0.2415 | 0.7538 / 1.2755 | promotion mainline |
| v8.1C C3-25 / canonical512 r2 | first512 matched | Direct-H | 290.136 | 15.350 | 0.6662 | 0.6270 | 0.7814 | 0.7326 | 0.7924 / 0.2411 | 0.7020 / 1.1539 | matched comparator |
| C3-MARDM-H105K / canonical512 r3 | first512 matched | Direct-H | 159.708 | 16.602 | 0.7967 | 0.8430 | 0.8707 | 0.8224 | 0.9021 / 0.2378 | 0.8146 / 1.3489 | Human-only system diagnostic |
| C3-ViMoGen-CLIP-H105K / canonical512 r2 | first512 matched | Direct-H | 154.626 | 19.788 | 0.7988 | 0.8581 | 0.9021 | 0.7738 | 0.8103 / 0.2373 | 0.7229 / 1.1551 | Human-only system diagnostic |
| C3-ViMoGen-UMT5-H105K / canonical512 r3 | first512 matched | Direct-H | 164.958 | 18.334 | 0.8144 | 0.8514 | 0.8671 | 0.7757 | 0.8519 / 0.2398 | 0.7627 / 1.2242 | Human-only system diagnostic |
| v9 redesign protected-H ViMoGen / v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727 | first512 matched | Human teacher105K / Unified210K Direct-H | 156.576 | 19.097 | 0.8317 | 0.9142 | 0.9140 | 0.7676 | 0.8615 / 0.2373 | 0.7729 / 1.2616 | diagnostic-only；not promotion-eligible |

### 3.3 Direct-C fair table

| version / run | cohort | human condition | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | density ↑ | precision ↑ | recall ↑ | caption F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ | status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| v8.1C C3-25 / formal105K | pure4053 formal | observed Human | 25.091 | 59.539 | 0.7503 | 0.8989 | 0.8769 | 0.5751 | 0.7645 | 1.5910 / 1.6684 | 35.298 | 1.4777 / 0.1485 | promotion mainline |
| v8.1C C3-25 / canonical512 r2 | first512 matched | observed Human | 34.077 | 60.287 | 0.8969 | 0.9996 | 0.9182 | 0.7108 | 0.7661 | 1.5922 / 1.6652 | 32.635 | 1.5335 / 0.1514 | matched comparator |
| v9 redesign protected-H ViMoGen / v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727 | first512 matched | observed Human | 232.175 | 36.430 | 0.5819 | 0.4836 | 0.6193 | 0.5434 | 0.4103 | 2.6251 / 2.9110 | 57.564 | 9.8580 / 0.5000 | diagnostic-only；Camera fail |

### 3.4 Joint-parallel fair table

| version / run | cohort | H FDTMR / TMR / HCov | C FDCLaTr / CLaTr / CCov | caption F1 ↑ | r-FPD / Out ↓ | H global / root-aligned ↓ m | Cam ADE / FDE / rotation ↓ | status |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| v8.1C C3-25 / formal105K | pure4053 formal | 227.189 / 13.691 / 0.5327 | 70.580 / 46.720 / 0.6057 | 0.5988 | 2.3848 / 0.1835 | 0.8638 / 0.2533 | 2.9042 / 3.0032 / 70.849° | promotion mainline |
| v8.1C C3-25 / canonical512 r2 | first512 matched | 299.989 / 14.130 / 0.6196 | 75.232 / 48.185 / 0.7773 | 0.6175 | 2.6582 / 0.1931 | 0.8031 / 0.2517 | 2.8724 / 2.9238 / 68.904° | matched comparator |
| v9 redesign protected-H ViMoGen / v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727 | first512 matched | 156.576 / 19.097 / 0.8317 | 181.666 / 48.619 / 0.6735 | 0.4965 | 4.6425 / 0.3157 | 0.8615 / 0.2373 | 3.3122 / 3.4160 / 69.886° | diagnostic-only；Human exact；Camera fail |

matched first512 上，v9 Human 明显更强；Camera 除 joint CLaTr 略高外在 distribution、coverage、caption、framing 与 geometry 上总体退化，因此不是 Pareto improvement。

### 3.5 v9 complete N=512 Direct-H and joint Human

Human teacher105K、Unified210K Direct-H 与 joint Human 生成数值完全一致；Direct-H exact-regression max abs 为 0.0。

| version / run | mode | R1 / R2 / R3 ↑ | MM dist ↓ | FDTMR ↓ | TMR ↑ | HCov / density / precision / recall ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v9 redesign protected-H ViMoGen / same run | Direct-H and joint Human | 0.1797 / 0.3027 / 0.3926 | 49.2351 | 156.5765 | 19.0970 | 0.8317 / 0.9142 / 0.9140 / 0.7676 |

| version / run | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v9 redesign protected-H ViMoGen / same run | Direct-H and joint Human | 512 | 0.861482 | 0.237316 | 0.772902 | 1.261602 |

### 3.6 v9 complete N=512 Direct-C

| version / run | mode | R1 / R2 / R3 ↑ | MM dist ↓ | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v9 redesign protected-H ViMoGen / same run | Direct-C observed-Human | 0.1758 / 0.2852 / 0.3691 | 28.3481 | 232.1747 | 36.4296 | 0.5819 / 0.4836 / 0.6193 / 0.5434 |

| version / run | mode | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD ↓ | Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v9 redesign protected-H ViMoGen / same run | Direct-C observed-Human | 0.3762 / 0.4568 / 0.4103 | 2.6251 / 2.9110 | 57.5638 | 9.8580 | 0.5000 |

Direct-C results 中 joint callback 的 Human 数值来自 observed GT-H evaluator side effect，不是 free joint generation，不能进入 joint Human 表。

### 3.7 v9 complete N=512 joint parallel

| version / run | mode | Camera R1 / R2 / R3 ↑ | Camera MM dist ↓ | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v9 redesign protected-H ViMoGen / same run | joint parallel Camera | 0.2266 / 0.3613 / 0.4551 | 25.1743 | 181.6659 | 48.6188 | 0.6735 / 0.5157 / 0.6644 / 0.6602 |

| version / run | mode | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD ↓ | Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v9 redesign protected-H ViMoGen / same run | joint parallel Camera | 0.4493 / 0.5584 / 0.4965 | 3.3122 / 3.4160 | 69.8862 | 4.6425 | 0.3157 |

### 3.7.1 v9 intermediate Camera snapshots

`140K`、`175K`、`189K` 与 final `210K` 使用同一 first-512 ordered cohort（SHA-256 `6b9c92a5…d8df`）、seed `17`、eval batch `32`、decode batch `1`、Euler `50`、当前 CFG 及同一 redesign owning decoder。以下六个 intermediate eval 的 contract、checkpoint、records、fixed-sample 与结果 SHA 均重新计算一致；Human parameter／固定噪声输出 max-abs regression 均为 `0.0`。

| version / run | fixed-loss context | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | caption F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v9 protected-H / `unified_140k_direct_c_n512_r2_20260728` | Direct-C specialist boundary | 48.0474 | 66.9878 | 0.8300 / 0.9489 / 0.9017 / 0.7483 | 0.7399 | 1.9457 / 2.1948 | 38.7467 | 2.5793 / 0.2114 |
| v9 protected-H / `unified_175k_direct_c_n512_r2_20260728` | HC-only boundary | 55.1964 | 60.1675 | 0.8142 / 0.9298 / 0.9002 / 0.6840 | 0.7349 | 2.0300 / 2.1332 | 46.7105 | 2.9990 / 0.2144 |
| v9 protected-H / `unified_189k_direct_c_n512_r2_20260728` | early alternating compromise | 40.0755 | 66.5019 | 0.7732 / 0.8332 / 0.8846 / 0.7386 | 0.8220 | 2.1345 / 2.2985 | 44.7531 | 2.2245 / 0.1931 |

| version / run | fixed-loss context | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | caption F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v9 protected-H / `unified_140k_joint_parallel_n512_r2_20260728` | Direct-C specialist boundary | 56.4664 | 69.0385 | 0.7032 / 0.8223 / 0.8201 / 0.7775 | 0.7874 | 3.1592 / 3.4022 | 77.2374 | 3.4550 / 0.2511 |
| v9 protected-H / `unified_175k_joint_parallel_n512_r2_20260728` | HC-only boundary | 37.3668 | 69.2943 | 0.8004 / 0.8509 / 0.7949 / 0.7538 | 0.8871 | 3.1717 / 3.3725 | 72.0712 | 2.7012 / 0.2104 |
| v9 protected-H / `unified_189k_joint_parallel_n512_r2_20260728` | early alternating compromise | 47.6112 | 66.3515 | 0.7690 / 0.8365 / 0.8165 / 0.7344 | 0.8162 | 3.1041 / 3.2865 | 72.8453 | 2.6771 / 0.2107 |

`140K` 是明显优于 final 的 Direct-C endpoint；`175K` 的 joint semantic／caption 改善与 Direct-C 回退共同支持 HC 改善伴随 Direct-C 遗忘；`189K` 在两路均避开 final collapse，是折中点而非逐字段支配点。decoded 排序与各 route fixed-EMA loss 大体同向，但 geometry、coverage 与 semantic 字段并非严格单调，因此 checkpoint 仍须保留两路 Pareto，不能以单一 loss 或平均分替代。

### 3.8 v9 decoded Human physical and kinematic

每个 cell 是 mean / median / p90；teacher、final Direct-H 与 joint Human 相同。contact/skate 使用 own-motion floor heuristic，不是 calibrated ground metric。

| version / run | mode | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: |
| Pulp dataset reference / first512 | reference | 2.345e-7 / 2.182e-7 / 3.083e-7 | 0.034658 / 0.020612 / 0.079158 | 0.026925 / 0.014944 / 0.063652 | 0.041451 / 0.022679 / 0.095851 |
| v9 redesign protected-H ViMoGen / same run | Direct-H and joint Human | 2.388e-7 / 2.215e-7 / 2.798e-7 | 0.032723 / 0.019709 / 0.075231 | 0.030252 / 0.019129 / 0.068611 | 0.047994 / 0.029909 / 0.108956 |

| version / run | mode | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / first512 | reference | 0.028661 / 0.015640 / 0.066596 | 0.016989 / 0.008874 / 0.039195 | 0.022698 / 0.012218 / 0.051730 | 0.497621 / 0.457800 / 1.000000 | 0.038117 / 0.021029 / 0.076822 |
| v9 redesign protected-H ViMoGen / same run | Direct-H and joint Human | 0.023027 / 0.010557 / 0.053804 | 0.015529 / 0.007894 / 0.036855 | 0.022105 / 0.011301 / 0.050672 | 0.553772 / 0.516507 / 1.000000 | 0.039224 / 0.021468 / 0.086670 |

> [!warning] Invalid zero fields
> Camera evaluator 发出的 g_fpd、projection precision/recall/density/coverage 与 error 恒为零，因为对应 update 未启用；这些值不进入比较表，也不是成功证据。

## 4. C3-25 seed17 Unified-3 105K formal

完整新评测 root：

`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v8_1c_c3_25_unified3_105k_eval_r2_canonical4053_seed17_4090g1_20260727/`

### 4.1 Protocol

| version / run | mode | N / ordered IDs | sampler | evaluator | representation / owning decoder |
| --- | --- | --- | --- | --- | --- |
| C3-25 / canonical4053 r2 | Direct-H | 4,053 / [[Storymotion-exp-sha]] | DDIM50, `START_X`, CFG=1, eta=0, seed17, eval batch32, decode batch16 | official full evaluator [[Storymotion-exp-sha]] | v8.1C C3-25 non-causal joint AE; normalized Human199 + camera14; H128+C64 / decoder [[Storymotion-exp-sha]] |
| C3-25 / canonical4053 r2 | Direct-C observed-Human completion | 4,053 / [[Storymotion-exp-sha]] | DDIM50, `START_X`, CFG=1, eta=0, seed17, eval batch32, decode batch16 | official full evaluator [[Storymotion-exp-sha]] | same checkpoint, cache and owning decoder |
| C3-25 / canonical4053 r2 | joint parallel | 4,053 / [[Storymotion-exp-sha]] | DDIM50, `START_X`, CFG=1, eta=0, seed17, eval batch32, decode batch16 | official full evaluator [[Storymotion-exp-sha]] | same checkpoint, cache and owning decoder |

Formal checkpoint 是 immutable `step_105000.pt`，identity [[Storymotion-exp-sha]]。train/eval cache 分别为 [[Storymotion-exp-sha]] / [[Storymotion-exp-sha]]；train-only full-cov stats 为 [[Storymotion-exp-sha]]。三模式 contract 显式 `is_causal=false`。

官方 C3 evaluator 是 streaming replay，不生成 `fixed_samples.pt`；每个 profile 保存完整 evaluator JSON、逐样本 `records.jsonl`，joint 另有 per-sample-quality JSON。补字段时固定 checkpoint/cache/ordered IDs/seed/sampler/batch 并写新 root；不得把 C3-MARDM-H105K 或 C3-ViMoGen Human-only 的 fixed samples 当作 C3 artifact。

### 4.2 Direct-H complete semantic and paired geometry

| version / run | mode | N | FDTMR ↓ | TMR ↑ | HCov ↑ | density ↑ | precision ↑ | recall ↑ | R1 ↑ | R2 ↑ | R3 ↑ | MM dist ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | Direct-H | 4,053 | 222.120 | 14.389 | 0.5275 | 0.5403 | 0.7091 | 0.5764 | 0.2290 | 0.3827 | 0.4930 | 50.5755 |

| version / run | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | Direct-H | 4,053 | 0.845517 | 0.241475 | 0.753813 | 1.275453 | 56.831 | 73.614 | 266.729 |

### 4.3 Direct-C complete Camera and observed-Human projective

| version / run | mode | N | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | density ↑ | precision ↑ | recall ↑ | R1 ↑ | R2 ↑ | R3 ↑ | MM dist ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | Direct-C observed-Human completion | 4,053 | 25.091 | 59.539 | 0.7503 | 0.8989 | 0.8769 | 0.5751 | 0.3723 | 0.5917 | 0.7168 | 22.6149 |

| version / run | mode | N | caption P ↑ | caption R ↑ | caption F1 ↑ | Cam ADE ↓ m | Cam FDE ↓ m | rotation ↓ degree |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | Direct-C observed-Human completion | 4,053 | 0.8174 | 0.7186 | 0.7645 | 1.590954 | 1.668443 | 35.2983 |

| version / run | mode | N | observed-Human r_fpd ↓ | observed-Human Out ↓ |
| --- | --- | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | Direct-C observed-Human completion | 4,053 | 1.4777 | 0.1485 |

### 4.4 Joint parallel complete semantic and paired geometry

| version / run | mode | branch | N | F-distance ↓ | alignment ↑ | coverage ↑ | density ↑ | precision ↑ | recall ↑ | R1 ↑ | R2 ↑ | R3 ↑ | MM dist ↓ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | joint parallel | Human / TMR | 4,053 | 227.189 | 13.691 | 0.5327 | 0.5755 | 0.7207 | 0.5719 | 0.2176 | 0.3602 | 0.4717 | 50.7605 |
| C3-25 / canonical4053 r2 | joint parallel | Camera / CLaTr | 4,053 | 70.580 | 46.720 | 0.6057 | 0.8092 | 0.8596 | 0.4204 | 0.2976 | 0.4801 | 0.6035 | 26.2249 |

| version / run | mode | N | caption P ↑ | caption R ↑ | caption F1 ↑ | r_fpd ↓ | Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | joint parallel | 4,053 | 0.6612 | 0.5614 | 0.5988 | 2.3848 | 0.1835 |

| version / run | mode | N | H global ↓ m | H root-aligned ↓ m | H root ADE / FDE ↓ m | Cam ADE / FDE ↓ m | Cam rotation ↓ degree |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | joint parallel | 4,053 | 0.863815 | 0.253348 | 0.764885 / 1.293826 | 2.904159 / 3.003201 | 70.8486 |

| version / run | mode | N | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: |
| C3-25 / canonical4053 r2 | joint parallel | 4,053 | 62.657 | 77.660 | 238.154 |

### 4.5 Complete decoded Human physical/kinematic summary

每个 cell 是 `mean / median / p90`。dynamics 单位为 decoded coordinate / frameⁿ；contact 为 fraction；bone CV 无量纲。reference、Direct-H 与 joint parallel 使用同一 pure4,053 ordered cohort。

| version / run | mode | N | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / pure4053 | reference | 4,053 | 2.414e-7 / 2.193e-7 / 3.084e-7 | 0.035336 / 0.021716 / 0.080298 | 0.026611 / 0.015280 / 0.060480 | 0.041110 / 0.023375 / 0.093897 |
| C3-25 / canonical4053 r2 | Direct-H | 4,053 | 2.264e-7 / 2.190e-7 / 2.576e-7 | 0.027972 / 0.022078 / 0.053804 | 0.027271 / 0.021220 / 0.053265 | 0.044272 / 0.033932 / 0.086549 |
| C3-25 / canonical4053 r2 | joint parallel | 4,053 | 2.247e-7 / 2.200e-7 / 2.580e-7 | 0.028783 / 0.023133 / 0.054559 | 0.028268 / 0.022292 / 0.054515 | 0.046397 / 0.036023 / 0.090378 |

| version / run | mode | N | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / pure4053 | reference | 4,053 | 0.029456 / 0.016709 / 0.067934 | 0.017055 / 0.009513 / 0.039636 | 0.023314 / 0.013070 / 0.053262 | 0.489381 / 0.425000 / 1.000000 | 0.039985 / 0.021858 / 0.080741 |
| C3-25 / canonical4053 r2 | Direct-H | 4,053 | 0.018211 / 0.012742 / 0.036883 | 0.012263 / 0.008977 / 0.024315 | 0.016964 / 0.012203 / 0.034109 | 0.545804 / 0.515464 / 1.000000 | 0.031481 / 0.023102 / 0.061442 |
| C3-25 / canonical4053 r2 | joint parallel | 4,053 | 0.018947 / 0.013675 / 0.038914 | 0.012712 / 0.009584 / 0.025197 | 0.017640 / 0.013166 / 0.035787 | 0.523592 / 0.480315 / 1.000000 | 0.032405 / 0.024154 / 0.062830 |

这些字段与同 cohort reference 对照解释，不单独设 hard gate。calibrated ground penetration/floating 尚未实现，不能由 own-motion contact heuristic 推断。

## 5. First-512 matched Human-only comparison

### 5.1 Protocol and provenance

| version / run | mode | N / ordered IDs | sampler | evaluator | generated representation / owning decoder |
| --- | --- | --- | --- | --- | --- |
| C3-25 / canonical512 r2 | Direct-H | 512 / [[Storymotion-exp-sha]] | DDIM50, `START_X`, CFG=1, eta=0, seed17 | official full [[Storymotion-exp-sha]] | C3 Human128 via Unified-3; decoder [[Storymotion-exp-sha]] |
| C3-MARDM-H105K / canonical512 r3 | Direct-H | 512 / [[Storymotion-exp-sha]] | MAR18 + native adaptive Dopri5 SiT ODE, seed17 | MARDM-SiT evaluator [[Storymotion-exp-sha]] | C3 Human128; frozen C3 decoder [[Storymotion-exp-sha]] |
| C3-ViMoGen-CLIP-H105K / canonical512 r2 | Direct-H | 512 / [[Storymotion-exp-sha]] | deterministic shifted-sigma Euler50, seed17 | ViMoGen-light evaluator [[Storymotion-exp-sha]] | C3 Human128; frozen C3 decoder [[Storymotion-exp-sha]] |
| C3-ViMoGen-UMT5-H105K / canonical512 r3 | Direct-H | 512 / [[Storymotion-exp-sha]] | deterministic shifted-sigma Euler50, seed17 | ViMoGen-light evaluator [[Storymotion-exp-sha]] | C3 Human128; frozen C3 decoder [[Storymotion-exp-sha]] |
| v9 Phase-C Human teacher CFG1 / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | Direct-H CFG sensitivity diagnostic | 512 / [[Storymotion-exp-sha]] | deterministic shifted-sigma Euler50, CFG=1 explicit override, seed17 | v9 ViMoGen-light evaluator [[Storymotion-exp-sha]] | Pulp-only Phase-C Human128；frozen Phase-C owning decoder [[Storymotion-exp-sha]] |
| v10 Phase-A Human teacher CFG1 / `v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729` | Direct-H prerequisite diagnostic | 512 / [[Storymotion-exp-sha]] | deterministic shifted-sigma Euler50, CFG=1, seed17 | v10 ViMoGen-light evaluator [[Storymotion-exp-sha]] | Pulp-only Phase-A Human128；frozen Phase-A owning decoder [[Storymotion-exp-sha]] |
| v10 Phase-A Human teacher CFG3 / `v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729` | Direct-H CFG sensitivity diagnostic | 512 / [[Storymotion-exp-sha]] | deterministic shifted-sigma Euler50, CFG=3 explicit override, seed17 | v10 ViMoGen-light evaluator [[Storymotion-exp-sha]] | same checkpoint、cohort与owning decoder as v10 CFG1 [[Storymotion-exp-sha]] |

Exact eval roots：

- C3：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v8_1c_c3_25_unified3_105k_eval_r2_canonical512_seed17_4090g1_20260727/`
- C3-MARDM-H105K：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/e5_c3_mardm_sit_xl_human128_105k_eval_r3_canonical512_mar18_seed17_4090g1_20260727/`
- C3-ViMoGen-CLIP-H105K：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/e6_c3_vimogen_light_clipseq_h_105k_eval_r2_canonical512_euler50_seed17_4090g1_20260727/`
- C3-ViMoGen-UMT5-H105K：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/e6_c3_vimogen_light_umt5base_h_105k_eval_r3_canonical512_euler50_seed17_5090g3_20260727/`
- v9 Phase-C Human teacher CFG1：`/data/public/ripemangobox/Motion/StoryMotion/runs/legacy/eval/stage2/v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727/human_teacher_105k_direct_h_cfg1_n512_20260729/`
- v10 Phase-A Human teacher CFG1：`/data/public/ripemangobox/Motion/StoryMotion/runs/legacy/eval/stage2/v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729/direct_h_teacher105k_n512/`
- v10 Phase-A Human teacher CFG3：`/data/public/ripemangobox/Motion/StoryMotion/runs/legacy/eval/stage2/v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729/direct_h_teacher105k_cfg3_n512_20260729/`

C3 row 使用 `last.pt` identity [[Storymotion-exp-sha]]，与 `step_105000.pt` 是不同 immutable file；recursive `torch.load` audit 证明两者的 `meta/model/opt/raw_model/step` 全部 exact equal，但本页仍不把 first-512 row 与 `4` full-cohort row 混成同一 artifact。MARDM、CLIP、UMT5、v9 CFG1 与两条v10 CFG eval identity均见 [[Storymotion-exp-sha]]。七条evaluation contract均显式`is_causal=false`。

MARDM 与 C3 同时改变 topology、prediction objective 与 sampler；ViMoGen-light 相对 C3 同时改变 topology、flow objective、sampler 与 condition interface。C3-ViMoGen CLIP/UMT5 两条 topology/objective/sampler matched，但仍是 single-seed system comparison。

v10 CFG1与C3-ViMoGen-CLIP使用相同`ViMoGenLightFlow` branch family、shifted-flow objective、Euler50、CFG1与first-512 ordered cohort；它改用Pulp-only Phase-A Human128、对应decoder/cache/statistics，并重新fresh训练。该行因此可用于Human representation-owner诊断，但不是只改单个tensor的严格causal ablation，也不产生Camera／joint evidence。v9 CFG1与v10 CFG1使用相同sampler／cohort／CFG，但Human latent owner分别为Phase-C `636K`与Phase-A `210K`；v9原CFG3正式结果只见§3.5与§3.8，本节不重复登记同一结果。

### 5.2 Complete Human semantic/distribution/retrieval

| version / run | mode | N | FDTMR ↓ | TMR ↑ | HCov ↑ | density ↑ | precision ↑ | recall ↑ | R1 ↑ | R2 ↑ | R3 ↑ | MM dist ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical512 r2 | Direct-H | 512 | 290.136 | 15.350 | 0.6662 | 0.6270 | 0.7814 | 0.7326 | 0.2500 | 0.3867 | 0.4941 | 50.3143 |
| C3-MARDM-H105K / canonical512 r3 | Direct-H | 512 | 159.708 | 16.602 | 0.7967 | 0.8430 | 0.8707 | 0.8224 | 0.1562 | 0.2715 | 0.3477 | 49.8598 |
| C3-ViMoGen-CLIP-H105K / canonical512 r2 | Direct-H | 512 | 154.626 | 19.788 | 0.7988 | 0.8581 | 0.9021 | 0.7738 | 0.1934 | 0.3203 | 0.3867 | 49.0686 |
| C3-ViMoGen-UMT5-H105K / canonical512 r3 | Direct-H | 512 | 164.958 | 18.334 | 0.8144 | 0.8514 | 0.8671 | 0.7757 | 0.1680 | 0.2754 | 0.3613 | 49.5388 |
| v9 Phase-C Human teacher / teacher105K CFG1 N512 | Direct-H CFG sensitivity diagnostic | 512 | 165.403 | 17.967 | 0.8205 | 0.9157 | 0.9042 | 0.7677 | 0.1777 | 0.2832 | 0.3574 | 49.6630 |
| v10 Phase-A Human teacher / teacher105K CFG1 N512 | Direct-H prerequisite diagnostic | 512 | 149.537 | 17.454 | 0.8323 | 0.9139 | 0.9022 | 0.7911 | 0.1445 | 0.2461 | 0.3223 | 49.8109 |
| v10 Phase-A Human teacher / teacher105K CFG3 N512 | Direct-H CFG sensitivity diagnostic | 512 | 159.831 | 18.424 | 0.8144 | 0.8502 | 0.8942 | 0.7855 | 0.1641 | 0.2754 | 0.3574 | 49.5155 |

### 5.3 Complete paired Human geometry and heading

| version / run | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 / canonical512 r2 | Direct-H | 512 | 0.792383 | 0.241148 | 0.701976 | 1.153926 | 55.326 | 72.653 | 263.099 |
| C3-MARDM-H105K / canonical512 r3 | Direct-H | 512 | 0.902127 | 0.237796 | 0.814602 | 1.348928 | 44.255 | 60.046 | 307.520 |
| C3-ViMoGen-CLIP-H105K / canonical512 r2 | Direct-H | 512 | 0.810265 | 0.237323 | 0.722932 | 1.155074 | 46.054 | 63.804 | 226.072 |
| C3-ViMoGen-UMT5-H105K / canonical512 r3 | Direct-H | 512 | 0.851943 | 0.239837 | 0.762705 | 1.224177 | 49.393 | 69.645 | 225.130 |
| v9 Phase-C Human teacher / teacher105K CFG1 N512 | Direct-H CFG sensitivity diagnostic | 512 | 0.754439 | 0.228783 | 0.668006 | 1.087862 | — | — | — |
| v10 Phase-A Human teacher / teacher105K CFG1 N512 | Direct-H prerequisite diagnostic | 512 | 0.771814 | 0.228721 | 0.688200 | 1.112087 | 45.190 | 63.036 | 222.395 |
| v10 Phase-A Human teacher / teacher105K CFG3 N512 | Direct-H CFG sensitivity diagnostic | 512 | 0.895121 | 0.237473 | 0.806082 | 1.272041 | 48.297 | 64.876 | 221.635 |

v9 CFG1的原生diagnostic evaluator没有发出integrated-heading字段；本页以`—`保留未测边界，不从其他CFG结果插值。

### 5.4 Complete decoded physical/kinematic summary

每个 cell 是 `mean / median / p90`。dynamics 单位为 decoded coordinate / frameⁿ；contact 为 fraction；bone CV 无量纲。dataset-reference 与五条 generated rows 使用同一 ordered cohort。

| version / run | mode | N | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / first512 | reference | 512 | 2.343e-7 / 2.187e-7 / 3.048e-7 | 0.034658 / 0.020612 / 0.079158 | 0.026925 / 0.014944 / 0.063652 | 0.041451 / 0.022679 / 0.095851 |
| C3-25 / canonical512 r2 | Direct-H | 512 | 2.257e-7 / 2.177e-7 / 2.551e-7 | 0.027198 / 0.021670 / 0.050224 | 0.026468 / 0.021019 / 0.053643 | 0.042875 / 0.033058 / 0.085271 |
| C3-MARDM-H105K / canonical512 r3 | Direct-H | 512 | 2.422e-7 / 2.233e-7 / 2.950e-7 | 0.042034 / 0.027827 / 0.089874 | 0.039298 / 0.027808 / 0.085038 | 0.060070 / 0.042005 / 0.134992 |
| C3-ViMoGen-CLIP-H105K / canonical512 r2 | Direct-H | 512 | 2.313e-7 / 2.221e-7 / 2.822e-7 | 0.029460 / 0.018917 / 0.065730 | 0.027301 / 0.018601 / 0.061080 | 0.042986 / 0.029204 / 0.094918 |
| C3-ViMoGen-UMT5-H105K / canonical512 r3 | Direct-H | 512 | 2.324e-7 / 2.234e-7 / 2.910e-7 | 0.030458 / 0.019430 / 0.066888 | 0.027200 / 0.019434 / 0.059705 | 0.042626 / 0.030828 / 0.093294 |
| v9 Phase-C Human teacher / teacher105K CFG1 N512 | Direct-H CFG sensitivity diagnostic | 512 | 2.262e-7 / 2.223e-7 / 2.564e-7 | 0.025094 / 0.017577 / 0.048235 | 0.023343 / 0.016249 / 0.049878 | 0.037049 / 0.025995 / 0.077083 |
| v10 Phase-A Human teacher / teacher105K CFG1 N512 | Direct-H prerequisite diagnostic | 512 | 2.257e-7 / 2.222e-7 / 2.588e-7 | 0.024636 / 0.017231 / 0.050659 | 0.022439 / 0.015976 / 0.047735 | 0.035409 / 0.024407 / 0.074972 |
| v10 Phase-A Human teacher / teacher105K CFG3 N512 | Direct-H CFG sensitivity diagnostic | 512 | 2.402e-7 / 2.231e-7 / 2.807e-7 | 0.031826 / 0.019872 / 0.070881 | 0.028951 / 0.018758 / 0.062491 | 0.045656 / 0.029573 / 0.097504 |

| version / run | mode | N | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / first512 | reference | 512 | 0.028661 / 0.015640 / 0.066596 | 0.016989 / 0.008874 / 0.039195 | 0.022698 / 0.012218 / 0.051730 | 0.497621 / 0.457800 / 1.000000 | 0.038117 / 0.021029 / 0.076822 |
| C3-25 / canonical512 r2 | Direct-H | 512 | 0.017717 / 0.012430 / 0.032804 | 0.011997 / 0.008857 / 0.022418 | 0.016548 / 0.011878 / 0.031716 | 0.542112 / 0.511508 / 1.000000 | 0.031218 / 0.022912 / 0.058264 |
| C3-MARDM-H105K / canonical512 r3 | Direct-H | 512 | 0.030144 / 0.016704 / 0.067830 | 0.022084 / 0.013787 / 0.048597 | 0.030165 / 0.018065 / 0.066401 | 0.488636 / 0.413978 / 0.989865 | 0.048887 / 0.029925 / 0.114799 |
| C3-ViMoGen-CLIP-H105K / canonical512 r2 | Direct-H | 512 | 0.020384 / 0.010274 / 0.048074 | 0.013834 / 0.007622 / 0.033119 | 0.019253 / 0.010106 / 0.045108 | 0.546928 / 0.520635 / 1.000000 | 0.036976 / 0.021689 / 0.088252 |
| C3-ViMoGen-UMT5-H105K / canonical512 r3 | Direct-H | 512 | 0.021825 / 0.010390 / 0.057426 | 0.014478 / 0.007390 / 0.036443 | 0.020057 / 0.009710 / 0.051936 | 0.558481 / 0.514816 / 1.000000 | 0.036683 / 0.020551 / 0.086135 |
| v9 Phase-C Human teacher / teacher105K CFG1 N512 | Direct-H CFG sensitivity diagnostic | 512 | 0.017266 / 0.010841 / 0.038113 | 0.011710 / 0.007781 / 0.023365 | 0.016463 / 0.010838 / 0.032693 | 0.579715 / 0.571429 / 1.000000 | 0.031240 / 0.019439 / 0.066754 |
| v10 Phase-A Human teacher / teacher105K CFG1 N512 | Direct-H prerequisite diagnostic | 512 | 0.017132 / 0.009958 / 0.039592 | 0.011532 / 0.007324 / 0.024253 | 0.016065 / 0.009713 / 0.034386 | 0.573741 / 0.547164 / 1.000000 | 0.030612 / 0.019471 / 0.062823 |
| v10 Phase-A Human teacher / teacher105K CFG3 N512 | Direct-H CFG sensitivity diagnostic | 512 | 0.022480 / 0.011068 / 0.057164 | 0.015050 / 0.007974 / 0.033820 | 0.021309 / 0.010915 / 0.049186 | 0.538918 / 0.500000 / 1.000000 | 0.037895 / 0.023146 / 0.089874 |

这些 physical/kinematic 字段未校准为独立 hard gate。它们显示 C3-MARDM-H105K 的 joint dynamics、jerk 与 foot-skate 尾部高于 reference；CLIP/UMT5 更接近 reference，但不能据此宣称严格 physical pass。视觉与盲评仍需单独闭合。

### 5.5 Auditable decision

- MARDM、CLIP、UMT5 都在适用的 Human-only mode 显示比 matched C3 row 更强的部分 semantic/distribution signal；它们不产生 Camera 或 joint 证据。
- 本次 C3-ViMoGen Human-only 对照中 CLIP 是综合较强 endpoint；UMT5 只在 HCov 高于 CLIP，不能据此宣称 UMT5 更优。
- v10 Phase-A Human teacher在matched first-512上形成清晰非塌缩signal；CFG1相对C3-ViMoGen-CLIP的FDTMR、coverage与paired geometry更好而TMR／retrieval更弱。fixed8盲样本仍出现速度、加速度和单帧尖峰，所以只判定Human prerequisite可用，不判strict physical pass。
- v10同checkpoint从CFG1改为CFG3后，TMR、R1/R2/R3与运动幅度上升，但FDTMR、HCov、density、precision及paired geometry回退；这不是单调改善，不能用CFG3掩盖owner差异。
- matched CFG1下，v9在retrieval与global/root geometry略优，v10在FDTMR、HCov、recall略优，结论是混合trade-off；matched CFG3下，§3.5／§3.8的v9结果在多数semantic、retrieval与geometry字段优于本节v10 CFG3，只有recall等少数字段不占优。fixed8视觉支持v9更自然，但8个样本不能替代N=512结论。
- 三条外部 Human system 的 strict physical-quality gate 均未通过；没有证据支持“Human blocker 已解决”。
- topology、objective、sampler 或 condition interface 并非全部 matched；不能把差异归因为 pure backbone 容量，也不能宣称 Stage2 backbone 已达到或未达到能力上限。
- C3-25 seed17 `105K` Unified-3 仍是 mainline。

### 5.6 v9／v10 Human teacher owner非等价审计

两条teacher的`ViMoGenLightFlow`拓扑、71,870,080参数规模、shifted-flow objective、batch128、AdamW、LR schedule、EMA与`105K`预算相同；本表只审计它们是否拥有同一个Human latent坐标系。cohort为相同ordered pure-test first128，比较raw Human128有效元素。

| version / run | N | Human state changed tensors | fixed latent exact | nonzero / valid elements | mean abs | max abs | decision |
| --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| v9 Phase-C636K ↔ v10 Phase-A210K / `phase_a210k_vs_phase_c636k_human` | 128 | 10 / 10 | false | 371,712 / 371,712 | 0.216329 | 2.286326 | raw cache与train-only statistics不等价；v10 teacher必须fresh训练 |

这证明“同为Human128”只代表shape相同。v9 teacher属于Phase-C `636K` owner；v10属于exact Phase-A `210K` owner。flow权重在各自whitened坐标中训练，禁止跨owner复用；checkpoint、cache与statistics身份见 [[Storymotion-exp-sha]]。

## 6. Canonical Stage1 true-length paired reconstruction

本节是 Stage1 deterministic encoder–decoder round trip，**不是** text-conditioned generation。所有样本先裁到自身 exact valid length，再进入 non-causal tokenizer；不存在固定首 `64` 帧裁切，也不让 future batch padding 进入 encoder。Pulp 与 HumanML3D 使用不同 cohort、观测字段和 reference distribution，禁止跨表排名。

### 6.1 Schema and protocol

| family | machine-readable keys | unit | direction / boundary |
| --- | --- | --- | --- |
| paired Human geometry | `human_global_mpjpe_m`, `human_root_aligned_mpjpe_m`, `human_root_ade_m`, `human_root_fde_m` | meter | ↓；root-aligned 仍保留 heading error |
| integrated heading | `human_wrapped_yaw_mean_deg`, `human_wrapped_yaw_final_deg`, `human_unwrapped_yaw_final_error_deg` | degree | ↓ |
| Camera trajectory | `camera_joint_center_ade_m`, `camera_joint_center_fde_m`, `camera_gt_human_anchor_center_ade_m`, `camera_gt_human_anchor_center_fde_m`, `camera_rotation_mean_deg`, `camera_fov_h_mean_abs_deg`, `camera_fov_w_mean_abs_deg` | meter / degree | ↓；GT-H anchor 行隔离 Human-root decode coupling |
| Human–Camera projective | `projective_joint_uv_l2_mean`, `projective_center_l2_mean`, `projective_log_scale_abs_mean`, `projective_out_ratio_abs_mean`, visible-joint fraction与 zero-visible frame rate | normalized screen / fraction | error、out、zero-visible ↓；visible fraction与 reference 对照 |
| decoded physical/kinematic | bone CV、joint/root speed/acceleration/jerk、foot contact/skate heuristic | decoded coordinate / frameⁿ / fraction | 每项均报告 `mean / median / p90`；只与同 cohort reference 对照 |

| version / run | mode | N / ordered IDs | sampler | evaluator | representation / owning decoder |
| --- | --- | --- | --- | --- | --- |
| C3-25 Stage1 / `v8_1c_c3_25_stage1_636k_eval_r1_canonical_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；decode batch1 | C3 canonical Stage1 [[Storymotion-exp-sha]] | official normalized Human199 + Camera14；C3-25 H128+C64 non-causal checkpoint/decoder [[Storymotion-exp-sha]] |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；decode batch1 | redesign Pulp [[Storymotion-exp-sha]] | `human_anchor_interaction_residual_199_14_128_16_48_v1`；owning decoder [[Storymotion-exp-sha]] |
| v10 Human-relative Camera old-3-loss Phase B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | historical `210K` Camera-only paired reconstruction diagnostic | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；GT Human supplies inverse-relative reference | v10 native + canonical historical Stage1 endpoint evaluator [[Storymotion-exp-sha]] | frozen Phase-A Human128 owner + independent relative-Camera48 encoder/decoder；missing framing backprop；non-causal [[Storymotion-exp-sha]] |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；decode batch1 | redesign Pulp [[Storymotion-exp-sha]] | same redesigned architecture；owning decoder [[Storymotion-exp-sha]] |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D Human-only root/local paired reconstruction diagnostic | 1,460 / [[Storymotion-exp-sha]] | deterministic exact-length owning Human encoder–decoder round trip；decode batch1 | redesign HumanML [[Storymotion-exp-sha]] | converted HML root/local under Pulp normalization；rot6D `4:136` prohibited mean-imputed/unobserved；decoder [[Storymotion-exp-sha]] |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D Human-only root/local paired reconstruction diagnostic | 1,460 / [[Storymotion-exp-sha]] | deterministic exact-length owning Human encoder–decoder round trip；decode batch1 | redesign HumanML [[Storymotion-exp-sha]] | converted HML root/local under Pulp normalization；rot6D `4:136` prohibited mean-imputed/unobserved；decoder [[Storymotion-exp-sha]] |

所有六条 contract 与 checkpoint 均显式 `is_causal=false`。历史 machine field `pose6d_policy` 是旧命名，实际指 Human199 channels `4:136` 的 joint rot6D；本页统一使用 **rot6D**。2026-07-27 的 policy correction 判定无显式 missingness 的 Pulp-mean填充为禁止的伪观测：上表 HML rows只保留已解码 root/local diagnostic 数值，mixed checkpoint不得进入正式 Stage2。

### 6.2 Pulp pure4,053 complete Human reconstruction

| version / run | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.068967 | 0.024190 | 0.058252 | 0.148365 | 4.947 | 9.309 | 10.633 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.120708 | 0.042136 | 0.100757 | 0.248722 | 10.434 | 18.751 | 20.757 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.133869 | 0.044779 | 0.112616 | 0.279547 | 11.897 | 21.218 | 23.622 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.718084 | 0.212668 | 0.614757 | 1.136651 | 82.011 | 91.159 | 418.094 |

### 6.3 Pulp pure4,053 complete Camera and projective reconstruction

| version / run | mode | N | joint Cam ADE ↓ m | joint Cam FDE ↓ m | GT-H Cam ADE ↓ m | GT-H Cam FDE ↓ m | rotation ↓ deg | FOV-H ↓ deg | FOV-W ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.039486 | 0.048270 | 0.036252 | 0.045599 | 0.704710 | 0.232809 | 0.253795 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.037654 | 0.043840 | 0.026146 | 0.033668 | 0.575890 | 0.204003 | 0.262347 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.121757 | 0.377332 | 0.021567 | 0.173423 | 0.617630 | 2.265990 | 1.462458 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.052681 | 0.058489 | 0.026317 | 0.034576 | 0.598872 | 0.197493 | 0.269706 |

| version / run | mode | N | joint UV L2 ↓ | center L2 ↓ | log-scale abs ↓ | out-ratio abs ↓ | visible recon / ref | zero-visible recon / ref ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.120701 | 0.077910 | 0.024236 | 0.032460 | 0.491548 / 0.497732 | 0.016594 / 0.007547 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.160790 | 0.096190 | 0.029678 | 0.039550 | 0.484065 / 0.497732 | 0.023921 / 0.007547 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.353564 | 0.107943 | 0.066030 | 0.041602 | 0.497488 / 0.497732 | 0.012102 / 0.007547 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.848923 | 0.343268 | 0.132111 | 0.122139 | 0.435095 / 0.497732 | 0.118101 / 0.007547 |

### 6.4 Pulp pure4,053 complete decoded physical/kinematic summary

每个 cell 是 `mean / median / p90`。这些是 reconstruction output，不是 free generation；contact/skate 使用 own-motion floor heuristic，不是 calibrated ground metric。

| version / run | mode | N | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / pure4053 | reference | 4,053 | 2.677e-7 / 2.376e-7 / 3.423e-7 | 0.034022 / 0.020797 / 0.078097 | 0.024906 / 0.014389 / 0.056310 | 0.038199 / 0.021969 / 0.087722 |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.025068 / 0.018822 / 0.049072 | 0.035164 / 0.022071 / 0.078341 | 0.027056 / 0.016760 / 0.058918 | 0.040600 / 0.025336 / 0.087586 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.026000 / 0.020484 / 0.050117 | 0.035668 / 0.022309 / 0.079710 | 0.028277 / 0.017335 / 0.062101 | 0.043172 / 0.026360 / 0.094611 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.021380 / 0.016591 / 0.041141 | 0.035518 / 0.022162 / 0.079693 | 0.027760 / 0.016814 / 0.061350 | 0.042220 / 0.025519 / 0.093351 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.037738 / 0.030727 / 0.069701 | 0.052227 / 0.038916 / 0.104918 | 0.037689 / 0.025133 / 0.080011 | 0.052494 / 0.034237 / 0.111604 |

| version / run | mode | N | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / pure4053 | reference | 4,053 | 0.029456 / 0.016709 / 0.067934 | 0.017055 / 0.009513 / 0.039636 | 0.023314 / 0.013070 / 0.053262 | 0.492193 / 0.428571 / 1.000000 | 0.039121 / 0.021590 / 0.079352 |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.030193 / 0.017489 / 0.069621 | 0.019302 / 0.011327 / 0.043122 | 0.026765 / 0.015810 / 0.059673 | 0.485486 / 0.423729 / 0.991597 | 0.038878 / 0.023307 / 0.081541 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069146 | 0.019719 / 0.011587 / 0.043854 | 0.027753 / 0.016438 / 0.061139 | 0.484022 / 0.421053 / 0.999598 | 0.039454 / 0.023312 / 0.082005 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.030211 / 0.017454 / 0.069245 | 0.019525 / 0.011400 / 0.043384 | 0.027378 / 0.016122 / 0.060866 | 0.496643 / 0.443182 / 1.000000 | 0.039378 / 0.023089 / 0.082767 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.030462 / 0.017899 / 0.069392 | 0.021257 / 0.012494 / 0.046893 | 0.029491 / 0.017673 / 0.063758 | 0.480031 / 0.415730 / 0.986771 | 0.061342 / 0.042012 / 0.127044 |

### 6.5 HumanML3D val1,460 root/local-only reconstruction

| version / run | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Redesign Pulp-only / true HML-val1460 r2 | HumanML3D Human-only root/local paired reconstruction | 1,460 | 0.574393 | 0.149483 | 0.517497 | 1.071561 | 55.832 | 84.710 | 143.700 |
| Redesign HML+Pulp / true HML-val1460 r2 | HumanML3D Human-only root/local paired reconstruction | 1,460 | 0.331579 | 0.092409 | 0.290735 | 0.649514 | 32.143 | 53.331 | 72.026 |

| version / run | mode | N | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| HumanML3D dataset reference / val1460 | reference root/local | 1,460 | 0.000794 / 0.000466 / 0.001590 | 0.014993 / 0.012136 / 0.029385 | 0.003272 / 0.002418 / 0.006597 | 0.002765 / 0.001784 / 0.006036 |
| Redesign Pulp-only / true HML-val1460 r2 | HumanML3D Human-only root/local paired reconstruction | 1,460 | 0.042560 / 0.033873 / 0.079708 | 0.017251 / 0.015355 / 0.029707 | 0.008569 / 0.007140 / 0.015094 | 0.012686 / 0.010405 / 0.022517 |
| Redesign HML+Pulp / true HML-val1460 r2 | HumanML3D Human-only root/local paired reconstruction | 1,460 | 0.019349 / 0.016611 / 0.033617 | 0.016423 / 0.014186 / 0.030485 | 0.006398 / 0.005159 / 0.011716 | 0.008647 / 0.006802 / 0.015565 |

| version / run | mode | N | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| HumanML3D dataset reference / val1460 | reference root/local | 1,460 | 0.012584 / 0.009123 / 0.026568 | 0.002045 / 0.001406 / 0.004280 | 0.001724 / 0.001090 / 0.003729 | 0.820654 / 0.887859 / 1.000000 | 0.006708 / 0.004156 / 0.015894 |
| Redesign Pulp-only / true HML-val1460 r2 | HumanML3D Human-only root/local paired reconstruction | 1,460 | 0.013882 / 0.010994 / 0.026940 | 0.004950 / 0.003835 / 0.009347 | 0.006917 / 0.005278 / 0.012809 | 0.742016 / 0.804305 / 1.000000 | 0.013125 / 0.011596 / 0.022239 |
| Redesign HML+Pulp / true HML-val1460 r2 | HumanML3D Human-only root/local paired reconstruction | 1,460 | 0.012870 / 0.009734 / 0.026400 | 0.003631 / 0.002723 / 0.007403 | 0.004798 / 0.003530 / 0.009552 | 0.804340 / 0.863234 / 1.000000 | 0.009766 / 0.007469 / 0.018527 |

### 6.6 v10 final endpoint 与历史 Stage1 综合对比

旧 `110K / 184K / 207K / 209K` 训练进度表已从 active ledger 撤下；其 immutable artifacts仍由 run root与 [[Storymotion-exp-sha]] 保存。旧v10 `210K`同样只保留为缺少framing反传的历史diagnostic，不再是cache候选；修正版尚无formal endpoint。下表全部为 Pulp pure4,053 true-length Stage1 reconstruction，但Pulp official使用owning native evaluator，v7/v8使用历史v8-schema，C3/v9/v10使用当前canonical审计；因此它是version-lineage综合表，不是严格单代码版本ablation。

| version / run | endpoint / boundary | N | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean ↓ deg | joint Cam ADE / FDE ↓ m | GT-H Cam ADE / FDE ↓ m | rotation ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | native pretrained Stage1 | 4,053 | 0.181053 / 0.080254 | 0.150145 / 0.595955 | — | 0.137449 / 0.277227 | — | 1.792 |
| v7.14 / joint AE official r2 | Stage1 `636K` former mainline | 4,053 | 0.212735 / 0.080731 | 0.169640 / 0.415430 | 21.640 | 0.041760 / 0.051500 | — | 0.619 |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` candidate | 4,053 | 0.071180 / 0.024700 | 0.060188 / 0.150914 | 5.113 | 0.047693 / 0.056039 | — | 0.717 |
| v8.1C C2 / center100 seed17 | Stage1 `636K` treatment | 4,053 | 0.074406 / 0.025927 | 0.062688 / 0.158011 | 5.360 | 0.031956 / 0.041183 | — | 0.859 |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | Stage1 `636K` current mainline | 4,053 | 0.068967 / 0.024190 | 0.058252 / 0.148365 | 4.947 | 0.039486 / 0.048270 | 0.036252 / 0.045599 | 0.704710 |
| v8.1C C3-50 / center50 seed17 | Stage1 `636K` exploratory | 4,053 | 0.073166 / 0.025593 | 0.061678 / 0.154323 | 5.194 | 0.036412 / 0.045116 | — | 0.718 |
| v8.1B / residual AE seed17 | Stage1 `636K` architecture control | 4,053 | 0.076655 / 0.028245 | 0.062513 / 0.186141 | 6.311 | 0.050705 / 0.065467 | — | 1.170 |
| v8.2 / human200 seed17 | Stage1 `636K` representation control | 4,053 | 0.068706 / 0.012999 | 0.065847 / 0.242966 | 1.275 | 0.053028 / 0.061554 | — | 0.569 |
| v9 redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | Phase A/B/C `636K` control | 4,053 | 0.120708 / 0.042136 | 0.100757 / 0.248722 | 10.434 | 0.037654 / 0.043840 | 0.026146 / 0.033668 | 0.575890 |
| v10 HREL-C old-3-loss / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | Phase A `210K` + frozen-H Phase B `210K` historical diagnostic | 4,053 | 0.133869 / 0.044779 | 0.112616 / 0.279547 | 11.897 | 0.121757 / 0.377332 | 0.021567 / 0.173423 | 0.617630 |

只有C3、v9与v10已在当前canonical projective schema下完整复核；更早版本不以缺失字段补造结果。`raw joint-out occupancy`是描述性占比，不能与paired Out error或Stage2的zero-visible `Out`混用。

| version / run | projective joint UV L2 ↓ | center L2 ↓ | log-scale abs ↓ | paired Out error ↓ | raw joint-out occupancy | visible recon / ref | zero-visible recon / ref ↓ | eligibility boundary |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| v8.1C C3-25 / canonical true4053 r1 | 0.120701 | 0.077910 | 0.024236 | 0.032460 | — | 0.491548 / 0.497732 | 0.016594 / 0.007547 | current mainline |
| v9 redesign Pulp-only / canonical true4053 r4 | 0.160790 | 0.096190 | 0.029678 | 0.039550 | — | 0.484065 / 0.497732 | 0.023921 / 0.007547 | architecture control |
| v10 HREL-C old-3-loss / final210K diagnostic | 0.353564 | 0.107943 | 0.066030 | 0.041602 | 0.500543 native recon | 0.497488 / 0.497732 | 0.012102 / 0.007547 | historical diagnostic；no cache／promotion |

> [!warning] `Out≈0.50` 的语义修正
> v10旧表的 `projective_outscreen≈0.50` 是**重建结果中逐帧、逐关节的原始出框占比**，不是 reconstruction-versus-GT误差，也不应作为lower-is-better选点轴。canonical reference本身只有约`0.497732`关节可见，即原始出框占比本来就约为`0.502268`。因此“Out误差约50%”是字段命名与方向解释错误；真正的paired Out error是`0.041602`。

剩余 `4.16%` paired Out误差略高于v9的`3.96%`和C3-25的`3.25%`。当前证据支持三个机制，而不是单一已证明根因：

1. 该旧v10 Phase-B objective只优化relative reconstruction、relative temporal与rotation geodesic；FOV、screen center/scale与projective framing只记录不反传。对应地，旧run的FOV与UV/log-scale误差明显高于v9/C3；这支持补回framing supervision，但修正版尚无formal数值，不能提前宣称已改善。
2. `Phi^-1`必须使用冻结Phase-A Human root/heading。v10 joint Camera ADE为`0.121757 m`，而替换为GT Human anchor后为`0.021567 m`；这说明Human root/heading reconstruction coupling是joint world/projective误差的重要来源，但不能据此把全部projective残差都归给Human。
3. visibility是屏幕边界上的离散阈值。FOV、center、scale和Human root的连续小误差在边缘构图样本上会被放大为joint in/out翻转。

尚未单独补算GT-H projective全套分解，因此“FOV是唯一根因”或“全部来自Human”都不成立。历史`207K`选择artifact继续保留provenance，但其framing轴把raw occupancy当作可最小化误差；它不再拥有当前endpoint决策权。旧final `210K`只保留历史diagnostic，修正版通过长训与formal审计前没有v10 cache候选；C3-25 mainline不变。

### 6.7 Matched interpretation

- Pulp `N=4,053` 测试的是 Pulp TRAM/SMPL + Camera14 域；HumanML `N=1,460` 测试的是 converted 20→30 fps root/local-only 域。优势反转首先是 **source-domain specialization**，不是 sample count 本身造成的 evaluator 反转。
- 两条 redesign arm 的 architecture、objective、phase lengths、optimizer steps 与 role exposure matched；唯一训练数据轴是 anchor source。mixed arm 直接见过 HML root/local，却以 partial supervision 替换大量 matched Pulp anchor exposure；当前 replay ratio 与 rot6D 伪缺失输入都是 setting boundary。后者已使该 mixed setting 对 promotion/Stage2 不合规。
- Pulp 上两臂的 GT-H Camera ADE 几乎相同（`0.026146` vs `0.026317 m`），而 Human/root/projective error 大幅分离；因此 mixed 的主要 Pulp 回退不是 standalone Camera decoder failure。
- Pulp/HML 数值反转只保留为 retrospective domain diagnostic / no promotion；不得把 HML partial result 写成完整 Human199、Camera、Stage2 或 generation 能力。

## 7. Task-sliced mechanism evidence

### 7.1 C3-MARDM-H105K fixed-8 root/body interchange

Evidence root：

`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/e5_c3_mardm_h_root_body_swap_fixed8_r1_20260726/`

该 probe 对同一 fixed-8 decoded cohort 交换 generated/GT 的 body 与 root/heading，不重采样，不产生 population metric。允许的结论严格限定为：

- A = generated body + GT root/heading 后，全局质量显著恢复。
- B = GT body + generated root/heading 后，全局轨迹仍明显失真。
- 这支持 root/heading 是该 fixed-8 cohort 的主要全局误差放大器。
- `N=8` 不能外推为 population-level 根因，也不能断言 MARDM topology 必然造成 root drift。

### 7.2 Numerical ownership boundary

旧 diagnostic 表中的 teacher-forced、one-step、gradient、latent-space 与 optimizer-process 数值不再出现在活动 ledger。对应 experiment contract、checkpoint、TensorBoard、records 与 artifact identity 仍在 [[Storymotion-exp-sha]]、run root 或只读 archive；删除的是它们作为生成质量 metric/排名的地位，不是源 artifact。唯一活动 reconstruction 数值是本页的 canonical true-length Stage1 paired table。


## 8. Uncertainty, missing fields, and incomparable items

| version / run | boundary | consequence |
| --- | --- | --- |
| C3-25 / canonical4053 r2 | pure full cohort；`step_105000.pt`；three modes share checkpoint/cache/decoder | mainline formal owner；不得与 first-512 row 当作同一 sample count |
| C3-25 / canonical512 r2 | first-512 subset；`last.pt` byte identity differs from formal checkpoint file | 只用于同 cohort Human system comparison；不替换 pure4,053 formal |
| Direct-C / all rows | decoded observed Human latent + Camera text | Camera/projective result属于 observed-Human completion；不是 free joint generation |
| joint parallel / C3 | Human 与 Camera 由同 checkpoint 自由生成 | 只在该 mode 解释 Human–Camera projective geometry；cascade 不进入 active gate |
| C3-MARDM-H105K / canonical512 r3 | same IDs/C3 owner，但 topology、objective 与 sampler 同时变化 | 支持 system-level Human generation；不能隔离 pure backbone、替换 mainline或外推 Camera/joint |
| C3-MARDM-H105K root/body interchange / fixed8 | 同一生成样本的 oracle 通道交换；无重采样、无 population metric | 可定位该 cohort 的 root/heading amplification；不能估计 prevalence 或断言 topology 根因 |
| C3-ViMoGen CLIP/UMT5 / canonical512 | topology/objective/sampler matched；condition encoder不同；single seed | 可排序本次 ViMoGen-light endpoint；不能外推文本编码器普遍优劣或 Camera/joint 能力 |
| v9 redesign protected-H / paired Human | 本轮 evaluator 没有写出 integrated-yaw fields | 已完整登记该 evaluator 实际发出的 Human semantic、global/root geometry 与 physical fields；不得补造或与 C3 yaw 直接比较 |
| Human physical / current evaluator | own-motion floor/contact heuristic，未标定统一 ground plane | calibrated penetration/floating 尚未计算；不得用 raw-GT curation scorer补位 |
| Camera trajectory / current evaluator | 只输出 center ADE/FDE 与 rotation；没有独立速度/加速度分布字段 | 这些 Camera dynamics 尚未计算；不得从 caption segment 或 optimizer过程推断 |
| projection callback / current evaluator | `g_fpd`、`error` 与 PRDC updates禁用并发出零值 | 零值不进入表、不作成功或失败证据 |
| C3 root-aligned MPJPE / all rows | removes root translation, not heading | 不得称为 local-pose error；必须与 yaw-aware attribution并列解释 |
| failed canonical512/formal r1 | 均在采样前 fail-close；旧 root不复用 | failure contract/log/manifest保留；只有新 root 的完整 artifacts进入结果表 |
| H-anchor true-length final gate | Pulp pure4,053 与 HumanML val1,460 是不同 cohort；HumanML rot6D 无显式 missingness 且被禁止地均值填充；Stage1 reconstruction only | root/local 数值只作 retrospective diagnostic；mixed checkpoint invalid for Stage2；不得合并 cohort、替换 C3-25 或外推 generation |
| historical Stage1/diagnostic rows | reconstruction、teacher-forced、oracle、gradient 与 architecture probe | 数值只在只读 archive/run artifacts；活动 ledger不再复制或排名 |

当前仍缺的 canonical 项是 v9 的 **integrated yaw**、evaluator 尚未实现的 **calibrated Human ground penetration/floating** 与 **独立 Camera velocity/acceleration/jerk distribution**。除此之外，本任务适用且由 evaluator 实际发出的 Human、Camera、observed-Human projective 与 joint-parallel fields 均已从 machine-readable results/records 补齐。
## 9. Retired-detail anchor index

以下标题只为旧 inbound links 保持可达；数字与 artifact identity 不在活动页重复。

### 4. Stage2 30K matched generatability screen

已闭合的 30K formal screen 见归档 ledger snapshot；当前版本事件见 [[version_family]]。

### 5.1 D4 residual propagation

D4 raw residual 链与 artifact identity 见归档 ledger snapshot。

### 5.2 D4.2 Camera-text reliance

D4.2 aligned/misaligned text 诊断与 artifact identity 见归档 ledger snapshot。

### 5.3 D4.3 owning-decoder direction sensitivity

D4.3 JVP/VJP 与 direction-sensitivity 诊断见归档 ledger snapshot。

### 5.4 Architecture-view consistency 四臂 N=512 screen

旧四臂 architecture-view screen 只保留于 immutable run artifacts；活动系统端点改见本页 [[#5. First-512 matched Human-only comparison]]，身份见 [[Storymotion-exp-sha]]。

### 5.5 C3-25 原生 Direct-H Human-only 学习曲线 N=512 screen

旧 snapshot learning-curve screen 只保留于 immutable run artifacts；正式 endpoint 与 first-512 对照改见本页 [[#4. C3-25 seed17 Unified-3 105K formal]] 和 [[#5. First-512 matched Human-only comparison]]。

### 4.10 v9 external long-run N=512 screens

已闭合的 external-backbone long-run 中，当前可比较的 C3-MARDM-H105K、C3-ViMoGen-CLIP-H105K 与 C3-ViMoGen-UMT5-H105K 见本页 [[#5. First-512 matched Human-only comparison]]；其余 stopped-arm identity 见 [[Storymotion-exp-sha]] 与原 run artifacts。

### C5-B fresh multi-horizon matched screen

C5-B two-seed short-screen 与 frozen-dose provenance 见归档 ledger snapshot。

### C3-25 completion → joint 条件暴露归因（2026-07-21）

同 checkpoint 的 GT-H、generated-H、shuffled-H 与 joint-parallel 归因见归档 ledger snapshot。

### 7.8 Stage1 Human-anchor residual control

Stage1 true-length paired 数值已归并到本页 [[#6. Canonical Stage1 true-length paired reconstruction]]；checkpoint、contract、result、records 与 visual identity 见 [[Storymotion-exp-sha]]。

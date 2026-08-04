---
title: "StoryMotion Repository Valid Metric Ledger"
status: active
hypothesis: |
  The single StoryMotion repository requires one numeric owner with explicit
  Paper A StoryMotion, Paper B DIRECT, or shared-baseline claim identity in
  addition to stage, mode, representation owner, cohort, sampler, and eligibility.
tags:
  - StoryMotion
  - DIRECT
  - Motion_Generation
  - metric
  - evidence
  - status/active
aliases:
  - StoryMotion-Valid-Metrics
source_notes:
  - "[[StoryMotion/current]]"
  - "[[DIRECT/current]]"
  - "[[version_family]]"
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
  - "[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]"
  - "[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]"
  - "[[paper-boundary]]"
  - "[[2026-07-29_full_re]]"
created: 2026-07-12T12:15:00+08:00
updated: 2026-08-04T11:42:15+08:00
---

# StoryMotion Repository Valid Metric Ledger

> [!abstract] Canonical numeric owner
> 本页拥有审计数值、公平对比、不可比边界，以及与正式结果直接绑定的checkpoint／result／records／audit SHA256。非metric运行身份与visual索引见[[Storymotion-exp-sha]]；Paper A当前决策见[[StoryMotion/current]]，Paper B见[[DIRECT/current]]。Stage1 reconstruction与Stage2 generation分区，不把diagnostic-only结果写成promotion evidence。

> [!important] 单仓库双论文记账
> 本页继续作为唯一正式数字owner，不为DIRECT创建第二份ledger。新正式结果必须标明
> `Paper A StoryMotion`、`Paper B DIRECT`或`shared baseline`身份；同一artifact可以被两篇
> 引用，但贡献解释必须分开。现有`Actor–Director` screen与Human-text结果保持历史run身份，
> 不自动升级为DIRECT evidence；DIRECT只有在其source reconstruction、positive定义和
> formal audit合同分别闭合后，才新增独立结果分区。

## 1. Evidence contract

- 数值必须来自完整 sampler 输出经 owning decoder 解码后的机器可读结果；手工观察只作为 visual verdict。
- 新增或修改的正式结果必须声明paper identity；不得让一行数值同时默认为两篇论文的promotion evidence。
- 所有 StoryMotion Stage1/Stage2 活动路径要求 is_causal=false。
- mixed-version 表逐行给出非空 version / run；若 cohort、sampler、decoder 或 representation 不同，紧邻表格声明限制。
- Direct-H 是 Human text-only；Direct-C 是 observed Human latent + Camera text。v11 mainline 的 formal joint 是 sequential Human→Camera；C3/v9 历史系统报告 joint parallel。
- cascade 只作历史归因，不是 active score 或 promotion gate。
- paired geometry 是 one-to-many generation 诊断，不独立作为 hard gate；root-aligned MPJPE 移除 root translation 但不移除 heading。
- 正式数值所依赖的checkpoint、result、records与cross-arm audit SHA与结果共置；其余运行身份与visual只见[[Storymotion-exp-sha]]。

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
| sequential joint | Human→Camera | 先自由生成Human，再以fixed generated-final-H生成Camera | 与joint parallel不同；v11 formal joint只使用本模式 |

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

### 3.9 v11 four-arm `30K` first-512 audited confirmation

正式cross-arm audit root：

`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v11_four_arm_30k_first512_audit_20260730/`

四臂均使用EMA `30K`、first-512 ordered pure-test IDs（SHA-256 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`）、official input SHA-256 `20efffb3ec8c6e9eb9b329486f14cafcf96465e1df709f6ef63366b19a821663`、seed17、eval batch32、shifted-sigma explicit Euler50、Human CFG1且无Camera CFG。只评测Direct-C与formal sequential Human→Camera；`joint_parallel=false`。训练implementation composite SHA-256为`48241c9041c653557f5ce12421a8593097afa2ddbcef4db9bdcf6ec7f9d1b487`，Stage1／owning-decoder SHA-256为`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`；四臂均通过non-causal、contract、cache／stats／teacher、sample identity与artifact hash审计。

| version / run | EMA `30K` SHA-256 | result SHA-256 | records SHA-256 |
| --- | --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_gt30k_seed17_5090g2_r2_20260729` | `a3f4379aee3e298bd90bf0ec877715549c3cdc6f4f3243fae0ca063653a1f2fb` | `791fbb955ec66bd09a4750cca2293e6af939642488948ab7fadaf31dbb02b55c` | `4fa2e0dbed2b8c60ef2e829ec023b4235fa2fee5f8b0bec9a10ed8ddebc6dbeb` |
| v11 / `v11_c0_geo_fixedh_gt30k_seed17_5090g3_r2_20260729` | `d0c863a88b612b9af36b09d15c8ff22aa5af9a8270cb2a0620e49ff534210057` | `7b29c5c04124bd81ce46f0540d8f37983afacb3d92956c0ee7f95615d9fdfb6a` | `7e916f927da7bd89146dd5cf09d01cfdb8e626e44afb2027598ff86b9a0acab2` |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_30k_seed17_4090g0_r2_20260729` | `e4c263a8d1adfeedee1331bf529b1e39b9c737ba82eaf1a3f7e9f0a86307325e` | `aa18f89fe08f37d0d259fa3b532c7983de25940c3484fc4efda229396b6b5ae2` | `251646052f08d56c9a1cd9b8dd755d9bdf27392969563a35d53cf4ffe8105f73` |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_30k_seed17_4090g1_r2_20260729` | `715825a1b0a300d6e9e3a2834f10ad09b56433f7b136209c30900122a4bc87a5` | `82786a6f4cb1fd580d1be151856c5622f717571fcd4b42a915fa1f668c19d5a1` | `d157f02b9715686627e935e097ced7fef7473e0f92e7f03262e209c7e0559bd4` |
| v9 / `v9_p3l_balanced64x2_lr1e4_full105k_postgate_seed17_4090g0_20260728` Camera phase `30K` | `da06991d42853ee888c5f1e02313aa2df2ba2b9d04ed42a031aba677d19b8c4e` | `f7fe46d5deb6d0f78e0371396317287bac813365bb1fbe3f88a142f07f36f1a0` | `68187cee75d3a83156e9ad56c39344fb90019dadf9730757939e6cba85969da5` |

cross-arm `matrix_audit.json` SHA-256为`92c9a378dac804403807ed3dc0b2d4604fdc8561b711e3eb15060a5dddfcd458`；audit implementation SHA-256为`5a5c5484634c419b0c31a458141711b9b16379118b2013b40b46721d26d227b3`，evaluation implementation SHA-256为`0c7fa0d3ec99af3b2ed6eb8b928805d1ae72fbd9f93e75cb2d53ef7e912bfc81`。

v9公平对照不是历史三阶段run缺失的Camera-only `30K`，而是P3L same-step full run的精确Camera phase-step `30K`／global-step `135K` EMA。它与v11共享Stage1／owning decoder、Human teacher、train／eval cache、train-only stats、teacher-final cache、ordered first-512、noise、sampler、batch与评测实现；v9 Camera EMA只补入全零source embedding，GT-H与teacher-final-H forward max-abs均为`0.0`。训练conditional dropout、Human-context构造与source identity仍是声明的系统差异，不把此表称为单变量ablation。v9 checkpoint SHA-256为`e70fc3660023d3b64b6fbc307ab97898aa6e6a57702f0127fbbc732d89ab8a89`；comparison contract／evaluation contract SHA-256分别为`f6abbbad9db0185bc6116c3baffc6a11213149b95b4c2400aa9d886d77f9f139`／`b29f1426f167f78a89dc905c6990db270b41c36bd30691057497f594b2996585`。matched audit SHA-256为`39348783937b383d8ff8a6cb2f34bee92dc817774453630a01b29f0ccd28e9cd`，evaluator／auditor SHA-256分别为`272748041b40b4817e5341b3e28d7461f30095f9690d36bdaf20caef7e33e3ec`／`c36bb3d5aa4c5046899d8af471c88b0c25d70185d64252fcc85aceb1274264ba`。

#### Direct-C complete Camera and observed-Human projective

| version / run | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM dist ↓ | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| v11 / C0-LAT `5090g2` | 55.4405 | 56.3304 | 0.8947 / 1.1240 / 0.9629 / 0.6333 | 0.2520 / 0.4102 / 0.5293 | 23.7074 | 0.7485 / 0.6225 / 0.6330 | 1.9218 / 1.9635 | 37.3415 | 1.4302 / 0.1395 |
| v11 / C0-GEO `5090g3` | 54.6225 | 55.3576 | 0.8771 / 1.1489 / 0.9727 / 0.6197 | 0.2363 / 0.3945 / 0.5000 | 23.9725 | 0.7391 / 0.6037 / 0.6184 | 1.8349 / 1.8897 | 36.4895 | 1.5989 / 0.1538 |
| v11 / C1-LAT `4090g0` | 61.6231 | 54.5264 | 0.8417 / 1.0295 / 0.9491 / 0.5900 | 0.2266 / 0.3945 / 0.4961 | 24.1853 | 0.7045 / 0.5761 / 0.5730 | 2.2274 / 2.2707 | 45.3606 | 1.8276 / 0.1567 |
| v11 / C1-GEO `4090g1` | 57.8809 | 54.8004 | 0.8555 / 1.0436 / 0.9512 / 0.6080 | 0.2344 / 0.3984 / 0.4941 | 24.1363 | 0.7304 / 0.5966 / 0.6134 | 2.1988 / 2.2425 | 44.7946 | 1.7526 / 0.1556 |
| v9 / P3L exact Camera-phase30K `4090g0` | 50.7030 | 53.4126 | 0.8808 / 1.1107 / 0.9550 / 0.6021 | 0.2246 / 0.3711 / 0.4883 | 24.4799 | 0.7168 / 0.5872 / 0.6034 | 2.0545 / 2.1104 | 41.3500 | 2.0882 / 0.1818 |

#### Sequential Human→Camera complete Camera branch

| version / run | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM dist ↓ | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| v11 / C0-LAT `5090g2` | 53.2543 | 58.2831 | 0.8165 / 0.8958 / 0.9062 / 0.6038 | 0.2344 / 0.3984 / 0.5176 | 23.2999 | 0.7215 / 0.6219 / 0.6274 | 2.9968 / 3.0600 | 72.2022 | 0.8316 / 0.0979 |
| v11 / C0-GEO `5090g3` | 55.4678 | 56.4752 | 0.8380 / 0.9728 / 0.9239 / 0.5722 | 0.2383 / 0.3770 / 0.4980 | 23.7773 | 0.7184 / 0.6180 / 0.6365 | 2.9558 / 3.0262 | 70.8416 | 0.8984 / 0.1072 |
| v11 / C1-LAT `4090g0` | 70.1628 | 52.5517 | 0.8108 / 0.9883 / 0.9509 / 0.5454 | 0.2109 / 0.3691 / 0.4805 | 24.8494 | 0.6822 / 0.5321 / 0.5359 | 3.0969 / 3.1431 | 70.3144 | 1.7505 / 0.1472 |
| v11 / C1-GEO `4090g1` | 69.6554 | 51.7098 | 0.8109 / 1.0192 / 0.9356 / 0.5510 | 0.2031 / 0.3496 / 0.4707 | 25.0152 | 0.6855 / 0.5293 / 0.5495 | 3.0791 / 3.1262 | 69.4968 | 1.5606 / 0.1398 |
| v9 / P3L exact Camera-phase30K `4090g0` | 53.2733 | 55.4703 | 0.8183 / 0.9377 / 0.9316 / 0.5745 | 0.2383 / 0.3730 / 0.4805 | 24.0376 | 0.7080 / 0.5993 / 0.6205 | 2.8839 / 2.9554 | 69.1413 | 1.1209 / 0.1197 |

#### Sequential Human branch

| version / run | FDTMR ↓ | TMR ↑ | HCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM dist ↓ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m |
| --- | ---: | ---: | --- | --- | ---: | --- | --- |
| v11 / C0-LAT `5090g2` | 157.9365 | 18.2417 | 0.8065 / 0.8850 / 0.9100 / 0.7737 | 0.1563 / 0.2852 / 0.3652 | 49.5793 | 0.7846 / 0.2268 | 0.7034 / 1.1511 |
| v11 / C0-GEO `5090g3` | 157.9365 | 18.2417 | 0.8065 / 0.8850 / 0.9100 / 0.7737 | 0.1563 / 0.2852 / 0.3652 | 49.5793 | 0.7846 / 0.2268 | 0.7034 / 1.1511 |
| v11 / C1-LAT `4090g0` | 157.9412 | 18.2401 | 0.8065 / 0.8856 / 0.9100 / 0.7737 | 0.1563 / 0.2852 / 0.3652 | 49.5800 | 0.7846 / 0.2268 | 0.7034 / 1.1511 |
| v11 / C1-GEO `4090g1` | 157.9412 | 18.2401 | 0.8065 / 0.8856 / 0.9100 / 0.7737 | 0.1563 / 0.2852 / 0.3652 | 49.5800 | 0.7846 / 0.2268 | 0.7034 / 1.1511 |
| v9 / P3L exact Camera-phase30K `4090g0` | 157.9184 | 18.2411 | 0.8065 / 0.8850 / 0.9100 / 0.7737 | 0.1563 / 0.2852 / 0.3652 | 49.5797 | 0.7846 / 0.2268 | 0.7034 / 1.1511 |

Human结果在同一训练主机内逐项一致，5090／4090之间只剩极小数值差；四臂均没有Human更新。Camera geometry的paired bootstrap使用matched sample为单位、10,000次resample、seed `260730`：

| version / comparison | mode | Δ ADE m（95% CI） | Δ FDE m（95% CI） | Δ rotation deg（95% CI） |
| --- | --- | --- | --- | --- |
| v11 / C0-GEO − C0-LAT | Direct-C | -0.0869 [-0.1928, 0.0041] | -0.0738 [-0.1837, 0.0248] | -0.8520 [-3.0419, 1.3336] |
| v11 / C0-GEO − C0-LAT | sequential | -0.0410 [-0.1033, 0.0202] | -0.0337 [-0.0987, 0.0279] | -1.3606 [-3.6207, 0.8076] |
| v11 / C1-GEO − C1-LAT | Direct-C | -0.0286 [-0.1155, 0.0558] | -0.0282 [-0.1161, 0.0589] | -0.5660 [-2.5290, 1.4097] |
| v11 / C1-GEO − C1-LAT | sequential | -0.0178 [-0.0629, 0.0290] | -0.0169 [-0.0616, 0.0294] | -0.8176 [-2.3851, 0.6501] |
| v11 / C1-LAT − C0-LAT | Direct-C | +0.3056 [0.1950, 0.4221] | +0.3072 [0.1883, 0.4338] | +8.0191 [5.2978, 10.8647] |
| v11 / C1-LAT − C0-LAT | sequential | +0.1001 [-0.0402, 0.2410] | +0.0831 [-0.0559, 0.2250] | -1.8878 [-5.6383, 1.8261] |
| v11 / C1-GEO − C0-GEO | Direct-C | +0.3639 [0.2354, 0.5111] | +0.3528 [0.2203, 0.4969] | +8.3051 [5.6190, 11.1650] |
| v11 / C1-GEO − C0-GEO | sequential | +0.1233 [-0.0077, 0.2591] | +0.1000 [-0.0346, 0.2346] | -1.3448 [-5.0881, 2.4603] |
| v11-v9 / C0-LAT − v9 P3L exact30K | Direct-C | -0.1327 [-0.2218, -0.0399] | -0.1468 [-0.2370, -0.0564] | -4.0085 [-6.5535, -1.4887] |
| v11-v9 / C0-LAT − v9 P3L exact30K | sequential | +0.1129 [0.0386, 0.1855] | +0.1046 [0.0252, 0.1826] | +3.0608 [0.8512, 5.3603] |

审计裁决（2026-07-30 `30K` screen 当时状态；后续 `105K` 与2026-07-31 selection只覆盖决策，不改写本表数字）：

- C0-LAT在semantic、coverage、retrieval与framing上最平衡，选为v11诊断端点；C0-GEO所有paired geometry 95% CI均跨零，且semantic／framing字段混合，故只保留为Pareto alternate。
- C1两臂相对matched C0的Direct-C geometry显著退化，Direct-C与sequential semantic／framing也广泛回退；这支持schedule-associated same-step teacher-final negative transfer。由于C0只在5090、C1只在4090训练，严格因果归因仍需swapped-host replay。
- 相对精确同cohort的v9 P3L Camera-phase30K，C0-LAT Direct-C除FDCLaTr外的表内semantic／coverage／retrieval／framing均改善，三项paired geometry也显著改善；sequential则是混合Pareto：C0-LAT的CLaTr、recall、caption、r-FPD与Out更好，但v9的coverage／density／precision与三项geometry更好。C0-LAT因此仍是v11诊断端点，不是跨模式支配v9的promotion endpoint。
- 当时四臂停止于`30K`且尚无`105K` continuation；随后用户独立授权的续训、pure4,053 audit与共同mainline selection见[[#3.11 v11 four-arm `105K` pure4,053 formal audit]]。

#### C3-25 `30K`对照边界

C3-25有immutable `step_30000.pt`（SHA-256 `3533a4216b441b8fba0d6a791408d60a8708dc9a44e47b93d3187217ee83e226`）和pure4,053 formal，但它与v11／v9 first-512在representation／decoder、cache／stats、cohort、DDIM `START_X` sampler以及formal joint mode上都不同；C3报告joint parallel，v11只允许sequential。其`30K` Direct-C为FDCLaTr `96.166`、CLaTr `36.846`、coverage `0.6297`、caption F1 `0.480`、ADE／FDE `1.982 / 2.105 m`、rotation `45.046°`；joint-parallel Camera为FDCLaTr `90.664`、CLaTr `31.617`、coverage `0.5860`、caption F1 `0.367`、ADE／FDE `3.226 / 3.325 m`、rotation `77.008°`、Out `0.2003`。Camera／joint result SHA-256分别为`accaa2c54fd749068e11e39cdd4de028845461ca66540feb6d50e21c8acfc5ea`／`1606e3280407a69b133584c0fdf079339eeeadf555cb9a939ddad9e817569e5b`。

这组C3数值只能作为same-step跨系统边界，不能进入v11-v9 matched排名；aggregate指标也不能反驳人工观察到的“无意义平均”生成。精确C3 first-512重跑因历史contract声明的原始stats bytes `0c97d247…3400`已不存在、当前只剩semantic-equivalent重存bytes `7decc3dd…42af`而fail-close；没有静默改写旧contract。

### 3.10 v11 four-arm `105K` first-512 audited confirmation

正式cross-arm audit root：

`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v11_four_arm_105k_first512_audit_20260730/`

四臂均从各自immutable full-state `35K`恢复子run训练到Camera optimizer step `105K`；其父run保存`30K→35K`真实TensorBoard与checkpoint，恢复子run保存`35K→105K`，因此两段共同覆盖用户授权的`30K→105K`，没有回填`0→30K`。正式评测统一使用EMA `105K`、first-512 ordered pure-test IDs（SHA-256 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`）、official input SHA-256 `20efffb3ec8c6e9eb9b329486f14cafcf96465e1df709f6ef63366b19a821663`、seed17、eval batch32、shifted-sigma explicit Euler50、Human CFG1且无Camera CFG。只评测Direct-C与formal sequential Human→Camera；`joint_parallel=false`。训练implementation composite SHA-256为`33eef1048cc19335fc25e6b8025eadc40fc5a12af88b95d62ed581bf00d83552`，evaluation implementation SHA-256为`ac2f4e89d701faede7172785a764bb853a5110d4d94850958375a09eb36e36cc`。

| version / run | EMA `105K` SHA-256 | result SHA-256 | records SHA-256 |
| --- | --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | `b7759ea686ddc8bd9abc2db2b3a6f74421bf3f6033274863d715f58b0d66b96a` | `2518548a21590600e18e7f7167a4b5dcfb1e0abb9b7e69cd7790e483c71f6e19` | `801c822ccddc2afecd7d7ea5a73fe55850775092285852a0c6346c10465b53b7` |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | `3cd135b0105e32cab9da877926a16d712ed480648176f909ac9044c51e7670c7` | `98d1282ea52487675af8bc9b8fe5c14e157b27d3b9291abdb694f8d68ff76a28` | `b139f346dbb1ccb647c07288d66c6f9f9ec45c00f728f001c80913fa13e81280` |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | `2fcd0092348cb8aa0403f28b0e0af3f4f62c07569c68806d62ac141f45b385e8` | `a35ead91f344709c5b74bde440b128971843a6703675391cf4c2b462aa73ba32` | `26c892db3c8d49097d35870fafcfb6c170b49ff3c9d9a479791a64d84b516692` |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | `1cef5404de4a334021034372358dd946a1e91b0728ddf8340888e4cfaeff236a` | `525e02cb27845f2874d96adc8ee2b56871baf246f7b443c1bbc4a83f9c3b7f36` | `3a7637b6f0ddddf2c91cc91d1aac6dec1b10b1b4a4c926ce74329bfe02298494` |

cross-arm `matrix_audit.json` SHA-256为`7c088d8ff3f362e28a394dd6c2962e89015987340b5bb84b437f058494311b8c`；audit implementation SHA-256为`a1ea4e3086dafeec6366cd0cbd39e8cd31981cd15cb34d12d504c518f677ad07`。四臂均通过non-causal、contract、cache／stats／teacher、sample identity、official input与artifact hash审计。

#### Direct-C complete Camera and observed-Human projective

| version / run | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM dist ↓ | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| v11 / C0-LAT `105K 5090g2` | 29.212 | 57.410 | 0.9296 / 1.2232 / 0.9609 / 0.6584 | 0.2148 / 0.4004 / 0.5020 | 23.2982 | 0.7801 / 0.6892 / 0.7290 | 1.4358 / 1.4999 | 28.435 | 0.7796 / 0.1007 |
| v11 / C0-GEO `105K 5090g3` | 29.940 | 57.941 | 0.9159 / 1.1725 / 0.9472 / 0.6955 | 0.2305 / 0.4043 / 0.5020 | 23.1844 | 0.7754 / 0.6977 / 0.7327 | 1.4324 / 1.4991 | 29.020 | 0.8741 / 0.0986 |
| v11 / C1-LAT `105K 4090g0` | 26.560 | 58.230 | 0.9041 / 1.2032 / 0.9592 / 0.6779 | 0.2285 / 0.4180 / 0.5020 | 23.0575 | 0.7702 / 0.6942 / 0.7266 | 1.7533 / 1.7937 | 34.983 | 1.1866 / 0.1225 |
| v11 / C1-GEO `105K 4090g1` | 31.127 | 57.168 | 0.9082 / 1.1844 / 0.9453 / 0.6547 | 0.2207 / 0.3848 / 0.5000 | 23.3457 | 0.7643 / 0.6883 / 0.7184 | 1.6465 / 1.7047 | 33.267 | 1.3859 / 0.1368 |

#### Sequential Human→Camera complete Camera branch

| version / run | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM dist ↓ | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| v11 / C0-LAT `105K 5090g2` | 32.832 | 57.497 | 0.8966 / 1.1213 / 0.9612 / 0.6484 | 0.2344 / 0.3848 / 0.4941 | 23.2482 | 0.7469 / 0.6787 / 0.7042 | 2.9009 / 2.9735 | 69.689 | 0.4795 / 0.0775 |
| v11 / C0-GEO `105K 5090g3` | 31.313 | 57.731 | 0.8829 / 1.1237 / 0.9377 / 0.6662 | 0.2363 / 0.3770 / 0.4844 | 23.2080 | 0.7717 / 0.6945 / 0.7244 | 2.8597 / 2.9325 | 70.339 | 0.5347 / 0.0799 |
| v11 / C1-LAT `105K 4090g0` | 48.303 | 52.668 | 0.8635 / 1.1543 / 0.9532 / 0.6096 | 0.2285 / 0.3535 / 0.4609 | 24.6792 | 0.7145 / 0.6119 / 0.6516 | 3.1129 / 3.1776 | 71.614 | 1.4256 / 0.1364 |
| v11 / C1-GEO `105K 4090g1` | 50.162 | 54.070 | 0.8338 / 1.0104 / 0.9395 / 0.5920 | 0.2188 / 0.3574 / 0.4688 | 24.3386 | 0.7242 / 0.6267 / 0.6657 | 3.1266 / 3.1796 | 71.885 | 1.4207 / 0.1337 |

sequential Human branch仍由冻结的同一teacher生成：C0两臂为FDTMR `157.9365`、TMR `18.2417`，C1两臂为`157.9412 / 18.2401`；HCov／precision／recall均为`0.8065 / 0.9100 / 0.7737`，R1／R2／R3均为`0.1563 / 0.2852 / 0.3652`。两台主机之间只有官方callback的极小数值差，Camera续训没有打开Human optimizer。

Camera geometry的paired bootstrap使用matched sample为单位、10,000次resample、seed `260730`：

| version / comparison | mode | Δ ADE m（95% CI） | Δ FDE m（95% CI） | Δ rotation deg（95% CI） |
| --- | --- | --- | --- | --- |
| v11 / C0-GEO − C0-LAT | Direct-C | -0.0033 [-0.1181, 0.1089] | -0.0008 [-0.1115, 0.1059] | +0.5851 [-2.0678, 3.3456] |
| v11 / C0-GEO − C0-LAT | sequential | -0.0412 [-0.1221, 0.0353] | -0.0410 [-0.1235, 0.0397] | +0.6498 [-2.2223, 3.5865] |
| v11 / C1-GEO − C1-LAT | Direct-C | -0.1068 [-0.2404, 0.0127] | -0.0890 [-0.2180, 0.0310] | -1.7157 [-4.0168, 0.5630] |
| v11 / C1-GEO − C1-LAT | sequential | +0.0137 [-0.0649, 0.0900] | +0.0020 [-0.0800, 0.0857] | +0.2717 [-2.0543, 2.4234] |
| v11 / C1-LAT − C0-LAT | Direct-C | +0.3176 [0.1795, 0.4645] | +0.2938 [0.1565, 0.4381] | +6.5481 [3.3618, 9.7548] |
| v11 / C1-LAT − C0-LAT | sequential | +0.2120 [0.0463, 0.3742] | +0.2041 [0.0326, 0.3737] | +1.9245 [-2.7081, 6.5675] |
| v11 / C1-GEO − C0-GEO | Direct-C | +0.2141 [0.0915, 0.3402] | +0.2056 [0.0801, 0.3272] | +4.2473 [1.3992, 7.1755] |
| v11 / C1-GEO − C0-GEO | sequential | +0.2669 [0.1129, 0.4246] | +0.2471 [0.0833, 0.4099] | +1.5464 [-3.0177, 6.0883] |

#### Budget／system comparison boundary

下面只比较共同的observed-Human Direct-C；每行都有non-empty `version / run`。v11与C3同为Camera optimizer `105K`，但representation／decoder／sampler不同；v9 final也是Camera phase `105K`，但训练schedule与formal joint定义不同。v9 P3L exact30K只保留同owner／cohort／sampler的较短预算锚点。该表是system边界，不是单变量ablation。

| version / run | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | caption F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | ---: | ---: | --- | ---: | --- | ---: | --- |
| v11 / C0-LAT `105K 5090g2` | 29.212 | 57.410 | 0.9296 / 1.2232 / 0.9609 / 0.6584 | 0.7290 | 1.4358 / 1.4999 | 28.435 | 0.7796 / 0.1007 |
| v11 / C0-GEO `105K 5090g3` | 29.940 | 57.941 | 0.9159 / 1.1725 / 0.9472 / 0.6955 | 0.7327 | 1.4324 / 1.4991 | 29.020 | 0.8741 / 0.0986 |
| v8.1C C3-25 / canonical512 r2 `105K` | 34.077 | 60.287 | 0.8969 / 0.9996 / 0.9182 / 0.7108 | 0.7661 | 1.5922 / 1.6652 | 32.635 | 1.5335 / 0.1514 |
| v9 P3L exact Camera-phase30K / `v9_p3l_balanced64x2_lr1e4_full105k_postgate_seed17_4090g0_20260728` | 50.703 | 53.413 | 0.8808 / 1.1107 / 0.9550 / 0.6021 | 0.6034 | 2.0545 / 2.1104 | 41.350 | 2.0882 / 0.1818 |
| v9 redesign final Camera-phase105K / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | 232.175 | 36.430 | 0.5819 / 0.4836 / 0.6193 / 0.5434 | 0.4103 | 2.6251 / 2.9110 | 57.564 | 9.8580 / 0.5000 |

审计裁决：

- `30K→105K`对C0两臂是广泛成熟增益：Direct-C与sequential的distribution、semantic、caption、geometry与framing总体同时改善，说明`30K`不是Camera endpoint。
- C0-LAT与C0-GEO在`105K`是混合Pareto；六个跨objective geometry 95% CI全部跨零。first-512本身不负责promotion；后续pure4,053 evidence支持两者共同mainline，不宣称geometry objective已产生稳健净增益。
- C1-LAT的Direct-C semantic恢复到四臂最强局部区间，但Direct-C geometry显著弱于C0-LAT，formal sequential又在semantic、caption、geometry与framing上显著回退。因而`64 GT + 64 teacher-final`不是广泛失败，而是更明确的route trade-off；它不适合作为当前sequential system endpoint。C0／C1与训练主机仍完全混杂，严格schedule归因仍需swapped-host replay。
- 相对同first-512的C3-25 `105K`，C0在FDCLaTr、coverage／density／precision、Camera geometry与projective framing上更好，但C3在CLaTr、recall与caption F1上更好；两者是跨representation／sampler Pareto，不能用aggregate指标否定C3视觉上的“无意义平均”问题，也不能据此把v11直接晋升为mainline。
- 相对更重要的v9边界，C0 `105K`在共同Direct-C字段上广泛优于v9 exact Camera-phase30K与v9 final Camera-phase105K。v9 final没有在当前合同下补跑sequential，所以不伪造同模式排名；已有exact30K sequential对照中，C0 `105K`在semantic／framing上广泛改善，geometry接近而非全面支配。
- 当时v11仍是diagnostic-only；其预设的pure4,053三模式合同后来已经闭合并触发2026-07-31 selection。v11第三模式仍只能是formal sequential，不能补写joint-parallel。

### 3.11 v11 four-arm `105K` pure4,053 formal audit

正式cross-arm audit root位于4090：

`/data/public/ripemangobox/Motion/StoryMotion/runs/legacy/eval/stage2/v11_four_arm_105k_pure4053_audit_20260730/`

四臂均评测完整Pulp pure-test `N=4,053`，ordered-ID SHA-256为`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，official-input SHA-256为`6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`。统一使用EMA Camera step `105K`、seed17、eval batch32、shifted-sigma explicit Euler50、Human CFG1、无Camera CFG；模式为Direct-H、Direct-C与formal sequential Human→Camera，`joint_parallel=false`。implementation composite SHA-256为`33eef1048cc19335fc25e6b8025eadc40fc5a12af88b95d62ed581bf00d83552`；evaluator SHA-256为`a14f1bc1e1257e6e1967bef44d0974f5bf037aafb6326f2043c55bacf1cd39fd`。

cross-arm `matrix_audit.json` SHA-256为`96464d35fbb69dc6befa5121153543e64b29f399d5feeb0c7a5c90d30c9927fb`；audit implementation SHA-256为`858bcdb4148d0efcf96beefd5a54b93bf33d8f3f1bf06b730a48b5a32e7f121d`。审计逐臂验证contract、non-causal、checkpoint／cache／stats／decoder、4,053个唯一ID、official input、三模式字段和artifact hash，并对全部paired geometry与decoded-Human physical字段执行10,000次matched-sample bootstrap。跨主机Direct-H replay使用显式unit-specific单样本最大值与cohort均值双阈值；同5090的C0-LAT／GEO逐字段exact，5090↔4090的最大yaw差`0.2259°`、最大root FDE差`0.00555 m`及孤立contact阈值翻转均通过相应均值守卫。

| version / run | EMA `105K` SHA-256 | pure contract SHA-256 | result SHA-256 | records SHA-256 |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | `b7759ea686ddc8bd9abc2db2b3a6f74421bf3f6033274863d715f58b0d66b96a` | `390d1cda9e1636460ff6cc641cb67cf08e530448b04748adab4c7b3dc4e5d832` | `d7cd9fc63139fea2c716de279e11ee009d6775da37ff49604eefa3bc3eca22da` | `00fdb6e4538b8a8864827f0237d824c6fde3e859862d6513564396c8ad064b8f` |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | `3cd135b0105e32cab9da877926a16d712ed480648176f909ac9044c51e7670c7` | `b4a96b57a11751113a76ad2b28345c103ba7a42ad63337ef124faaef59edd24c` | `85d26a1705f0bb96af83b679ac7e7921c94115cbc22e603350deabc62e5f1ba1` | `1e08feb85f8c0e61dc0ebdf6d39b68af27e69cb5889da6b0677929710980475e` |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | `2fcd0092348cb8aa0403f28b0e0af3f4f62c07569c68806d62ac141f45b385e8` | `1a5d8e9b6efe4da47c28c1f8cf6ffd18e36dcfdf4d3f0b10d4ee82db9f8e6044` | `adc0c95639484fd41ee6abcc29960eded70655b4191bdc0203a476eb4a8f89e3` | `a9b38100c025407f6d13bdc7666e505fb30c9f6851511975bdfa904f3ff8ec92` |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | `1cef5404de4a334021034372358dd946a1e91b0728ddf8340888e4cfaeff236a` | `99503b531c1e4b90d0ac587d7a18a62c26ac396eb8bc70985504c79b7dd2cb3c` | `f0dddfde464719e92d9dc096c03bfa6daab4e1323cfd34420374299791ea8f5d` | `3954af44654c471c8852553197dd742e9ecb7938b911a72d2290e92d9ecfdae4` |

#### Direct-H complete semantic and paired geometry

四臂使用同一冻结Human teacher；5090两臂逐字段exact，跨4090只有受审计约束的GPU roundoff。root-aligned MPJPE只去除root translation，仍保留heading error。

| version / run | N | FDTMR ↓ | TMR ↑ | HCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean / final / unwrapped final ↓ deg |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| v11 / C0-LAT `105K 5090g2` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6531 | 0.1559 / 0.2556 / 0.3388 | 0.842760 / 0.228751 | 0.758772 / 1.283039 | 47.239 / 66.123 / 239.357 |
| v11 / C0-GEO `105K 5090g3` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6531 | 0.1559 / 0.2556 / 0.3388 | 0.842760 / 0.228751 | 0.758772 / 1.283039 | 47.239 / 66.123 / 239.357 |
| v11 / C1-LAT `105K 4090g0` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |
| v11 / C1-GEO `105K 4090g1` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |

#### Direct-C complete Camera and observed-Human geometry

Direct-C的Human列是GT-H经v9 owning decoder的重建诊断，不是自由Human生成。

| version / run | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ | observed-H global / root-aligned MPJPE ↓ m |
| --- | ---: | ---: | --- | --- | --- | ---: | --- | --- |
| v11 / C0-LAT `105K 5090g2` | 21.171 | 56.933 | 0.8303 / 1.0932 / 0.9156 / 0.5566 | 0.7857 / 0.7000 / 0.7372 | 1.4125 / 1.4985 | 29.922 | 0.8465 / 0.1052 | 0.125466 / 0.048796 |
| v11 / C0-GEO `105K 5090g3` | 20.540 | 57.574 | 0.8236 / 1.0604 / 0.9062 / 0.5589 | 0.7900 / 0.7075 / 0.7442 | 1.3860 / 1.4711 | 29.800 | 0.8514 / 0.1017 | 0.125466 / 0.048796 |
| v11 / C1-LAT `105K 4090g0` | 22.461 | 56.689 | 0.8209 / 1.0991 / 0.9127 / 0.5453 | 0.7770 / 0.6941 / 0.7293 | 1.6756 / 1.7706 | 35.250 | 1.1141 / 0.1245 | 0.125455 / 0.048795 |
| v11 / C1-GEO `105K 4090g1` | 23.863 | 56.687 | 0.8083 / 1.0625 / 0.9080 / 0.5401 | 0.7782 / 0.6959 / 0.7306 | 1.6176 / 1.7137 | 33.777 | 1.1380 / 0.1243 | 0.125455 / 0.048795 |

#### Formal sequential Human→Camera complete joint system

| version / run | Camera FDCLaTr ↓ / CLaTr ↑ | Camera coverage / density / precision / recall ↑ | caption F1 ↑ | r-FPD / Out ↓ | H global / root-aligned MPJPE ↓ m | Cam ADE / FDE ↓ m | Cam rotation ↓ deg |
| --- | --- | --- | ---: | --- | --- | --- | ---: |
| v11 / C0-LAT `105K 5090g2` | 28.754 / 55.579 | 0.7735 / 1.0100 / 0.8949 / 0.5241 | 0.6935 | 0.5082 / 0.0773 | 0.842760 / 0.228751 | 2.9428 / 3.0422 | 71.435 |
| v11 / C0-GEO `105K 5090g3` | 29.505 / 56.103 | 0.7626 / 1.0042 / 0.8939 / 0.5164 | 0.7007 | 0.5098 / 0.0768 | 0.842760 / 0.228751 | 2.9368 / 3.0395 | 71.507 |
| v11 / C1-LAT `105K 4090g0` | 35.242 / 53.235 | 0.7464 / 1.0124 / 0.8863 / 0.4880 | 0.6779 | 1.2577 / 0.1384 | 0.842762 / 0.228751 | 3.0448 / 3.1537 | 72.838 |
| v11 / C1-GEO `105K 4090g1` | 37.466 / 53.405 | 0.7311 / 0.9650 / 0.8732 / 0.4863 | 0.6839 | 1.2113 / 0.1349 | 0.842762 / 0.228751 | 3.0497 / 3.1511 | 72.398 |

#### Complete decoded-Human physical/kinematic diagnostics

每个cell是`mean / median / p90`。单位与[[StoryMotion-metric-computation-io]]一致；bone CV无量纲，dynamics为decoded coordinate / frameⁿ，contact为fraction。它们是no-reference heuristic diagnostics，不是calibrated physical-validity或ground penetration／floating指标。Direct-H与sequential共享同一冻结Human输出；Direct-C是observed-H reconstruction。

| version / run | mode | N | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / v11 pure4053 | reference | 4,053 | 2.414e-7 / 2.194e-7 / 3.085e-7 | 0.035336 / 0.021716 / 0.080298 | 0.026611 / 0.015280 / 0.060480 | 0.041110 / 0.023375 / 0.093897 |
| v11 / C0-LAT + C0-GEO `5090` | Direct-H = sequential Human | 4,053 | 2.280e-7 / 2.220e-7 / 2.622e-7 | 0.025358 / 0.017674 / 0.053936 | 0.023125 / 0.016563 / 0.048184 | 0.036800 / 0.026027 / 0.076142 |
| v11 / C1-LAT + C1-GEO `4090` | Direct-H = sequential Human | 4,053 | 2.279e-7 / 2.220e-7 / 2.626e-7 | 0.025358 / 0.017675 / 0.053936 | 0.023125 / 0.016568 / 0.048186 | 0.036800 / 0.026036 / 0.076142 |
| v11 / C0-LAT + C0-GEO `5090` | Direct-C observed-H reconstruction | 4,053 | 2.468e-7 / 2.253e-7 / 3.127e-7 | 0.037159 / 0.023331 / 0.083145 | 0.030219 / 0.018391 / 0.066288 | 0.046381 / 0.027816 / 0.099293 |
| v11 / C1-LAT + C1-GEO `4090` | Direct-C observed-H reconstruction | 4,053 | 2.467e-7 / 2.250e-7 / 3.131e-7 | 0.037159 / 0.023330 / 0.083141 | 0.030219 / 0.018382 / 0.066291 | 0.046381 / 0.027812 / 0.099302 |

| version / run | mode | N | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / v11 pure4053 | reference | 4,053 | 0.029456 / 0.016709 / 0.067934 | 0.017055 / 0.009513 / 0.039636 | 0.023314 / 0.013070 / 0.053262 | 0.489381 / 0.425000 / 1.000000 | 0.039985 / 0.021858 / 0.080741 |
| v11 / C0-LAT + C0-GEO `5090` | Direct-H = sequential Human | 4,053 | 0.017803 / 0.010156 / 0.041565 | 0.011937 / 0.007418 / 0.026801 | 0.016892 / 0.010376 / 0.037602 | 0.596160 / 0.595745 / 1.000000 | 0.030608 / 0.019470 / 0.063224 |
| v11 / C1-LAT + C1-GEO `4090` | Direct-H = sequential Human | 4,053 | 0.017803 / 0.010157 / 0.041564 | 0.011937 / 0.007417 / 0.026799 | 0.016892 / 0.010380 / 0.037599 | 0.596170 / 0.595745 / 1.000000 | 0.030611 / 0.019465 / 0.063216 |
| v11 / C0-LAT + C0-GEO `5090` | Direct-C observed-H reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011575 / 0.043850 | 0.027753 / 0.016435 / 0.061084 | 0.491982 / 0.437500 / 1.000000 | 0.041858 / 0.024370 / 0.085571 |
| v11 / C1-LAT + C1-GEO `4090` | Direct-C observed-H reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011576 / 0.043855 | 0.027753 / 0.016443 / 0.061077 | 0.491997 / 0.437500 / 1.000000 | 0.041857 / 0.024370 / 0.085574 |

#### Four-arm paired geometry bootstrap

10,000次resample，seed `260730`，unit为matched sample；差值均为前者减后者。

| version / comparison | mode | Δ ADE m（95% CI） | Δ FDE m（95% CI） | Δ rotation deg（95% CI） |
| --- | --- | --- | --- | --- |
| v11 / C0-GEO − C0-LAT | Direct-C | -0.0265 [-0.0651, 0.0121] | -0.0274 [-0.0667, 0.0113] | -0.1218 [-1.0660, 0.8289] |
| v11 / C0-GEO − C0-LAT | sequential | -0.0060 [-0.0362, 0.0231] | -0.0027 [-0.0333, 0.0271] | +0.0725 [-0.9431, 1.0655] |
| v11 / C1-GEO − C1-LAT | Direct-C | -0.0580 [-0.0965, -0.0203] | -0.0569 [-0.0960, -0.0189] | -1.4732 [-2.3643, -0.5822] |
| v11 / C1-GEO − C1-LAT | sequential | +0.0049 [-0.0244, 0.0347] | -0.0026 [-0.0328, 0.0280] | -0.4395 [-1.2353, 0.3416] |
| v11 / C1-LAT − C0-LAT | Direct-C | +0.2631 [0.2208, 0.3054] | +0.2721 [0.2285, 0.3156] | +5.3279 [4.2681, 6.3547] |
| v11 / C1-LAT − C0-LAT | sequential | +0.1020 [0.0433, 0.1618] | +0.1115 [0.0522, 0.1718] | +1.4030 [-0.2920, 3.0632] |
| v11 / C1-GEO − C0-GEO | Direct-C | +0.2316 [0.1936, 0.2705] | +0.2426 [0.2037, 0.2823] | +3.9765 [2.9520, 4.9841] |
| v11 / C1-GEO − C0-GEO | sequential | +0.1129 [0.0552, 0.1713] | +0.1116 [0.0534, 0.1709] | +0.8910 [-0.7611, 2.5541] |

#### Co-mainline three-mode system boundary

下表是当前C0共同mainline与C3-25、v9 final和PulpMotion native baseline的统一索引。C0与C3／Pulp使用Pulp pure-test `N=4,053`；v9只有first-512。各系统的representation、owning decoder、sampler与formal joint定义不同，因此这是system boundary，不是单变量ablation。v11只报告sequential；C3/v9只报告joint parallel；Pulp没有StoryMotion Direct-C或当前decoded-geometry artifact。Pulp数值源`render_summary.json` SHA-256为`44dfa0a9a18fdc6eed492dc220cfae9606bc9f31832462699c3453ccb7e3bc57`；v9三路result SHA-256依次为`9dae46d216b91d4744b722591748b05917d9bba06432a3751f20669cda2abd73`、`fac9c33295ba7273537834f6c0c13451c150d5c76a0d33bc043532ebccc780fa`、`1c6bda40946f92585a032653fb3f694630ddccd607ae9aaa6b7849ba676f8c7d`。

| version / run | mode | N | F-distance ↓ / alignment ↑ | coverage / precision / recall ↑ | caption F1 ↑ | H global / root-aligned MPJPE ↓ m | Cam ADE / FDE ↓ m | Cam rotation ↓ deg | r-FPD / Out ↓ |
| --- | --- | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| v11 / C0-LAT `105K 5090g2` | Direct-H | 4,053 | 99.391 / 17.608 | 0.7158 / 0.8283 / 0.6531 | — | 0.842760 / 0.228751 | — | — | — |
| v11 / C0-GEO `105K 5090g3` | Direct-H | 4,053 | 99.391 / 17.608 | 0.7158 / 0.8283 / 0.6531 | — | 0.842760 / 0.228751 | — | — | — |
| v8.1C C3-25 / canonical4053 r2 | Direct-H | 4,053 | 222.120 / 14.389 | 0.5275 / 0.7091 / 0.5764 | — | 0.845517 / 0.241475 | — | — | — |
| v9 / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | Direct-H | 512 | 156.576 / 19.097 | 0.8317 / 0.9140 / 0.7676 | — | 0.8615 / 0.2373 | — | — | — |
| v11 / C0-LAT `105K 5090g2` | Direct-C observed-H | 4,053 | 21.171 / 56.933 | 0.8303 / 0.9156 / 0.5566 | 0.7372 | — | 1.4125 / 1.4985 | 29.922 | 0.8465 / 0.1052 |
| v11 / C0-GEO `105K 5090g3` | Direct-C observed-H | 4,053 | 20.540 / 57.574 | 0.8236 / 0.9062 / 0.5589 | 0.7442 | — | 1.3860 / 1.4711 | 29.800 | 0.8514 / 0.1017 |
| v8.1C C3-25 / canonical4053 r2 | Direct-C observed-H | 4,053 | 25.091 / 59.539 | 0.7503 / 0.8769 / 0.5751 | 0.7645 | — | 1.5910 / 1.6684 | 35.298 | 1.4777 / 0.1485 |
| v9 / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | Direct-C observed-H | 512 | 232.175 / 36.430 | 0.5819 / 0.6193 / 0.5434 | 0.4103 | — | 2.6251 / 2.9110 | 57.564 | 9.8580 / 0.5000 |
| v11 / C0-LAT `105K 5090g2` | formal sequential | 4,053 | 28.754 / 55.579 | 0.7735 / 0.8949 / 0.5241 | 0.6935 | 0.842760 / 0.228751 | 2.9428 / 3.0422 | 71.435 | 0.5082 / 0.0773 |
| v11 / C0-GEO `105K 5090g3` | formal sequential | 4,053 | 29.505 / 56.103 | 0.7626 / 0.8939 / 0.5164 | 0.7007 | 0.842760 / 0.228751 | 2.9368 / 3.0395 | 71.507 | 0.5098 / 0.0768 |
| v8.1C C3-25 / canonical4053 r2 | joint parallel | 4,053 | 70.580 / 46.720 | 0.6057 / 0.8596 / 0.4204 | 0.5988 | 0.863815 / 0.253348 | 2.9042 / 3.0032 | 70.849 | 2.3848 / 0.1835 |
| v9 / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | joint parallel | 512 | 181.666 / 48.619 | 0.6735 / 0.6644 / 0.6602 | 0.4965 | 0.8615 / 0.2373 | 3.3122 / 3.4160 | 69.886 | 4.6425 / 0.3157 |
| PulpMotion official / `dit-xy-ddpm-p2ee3dj7 step92,950` | native joint no-aux | 4,053 | 94.842 / 35.691 | 0.4833 / 0.6740 / 0.4431 | 0.4905 | — | — | — | 7.4040 / 0.3954 |
| PulpMotion official / `dit-xy-ddpm-p2ee3dj7 step92,950` | native joint aux | 4,053 | 93.269 / 37.777 | 0.4481 / 0.6442 / 0.4752 | 0.5127 | — | — | — | 5.8933 / 0.2847 |

审计裁决：

- C0-LAT与C0-GEO在pure4,053是混合Pareto；两模式共六项Camera geometry 95% CI全部跨零。2026-07-31 selection event将两者共同晋升为mainline，不把任一raw均值趋势写成稳健objective胜出。
- C1相对matched C0的Direct-C ADE／FDE／rotation全部显著回退，sequential ADE／FDE也显著回退；完整cohort确认teacher-final same-step混合route不适合作为当前系统端点。由于C0／C1与训练主机仍混杂，严格schedule因果仍需另行授权swapped-host replay。
- 相对C3 pure4,053，v11 C0-LAT Direct-H在semantic／distribution、root-aligned MPJPE与yaw上更好，root ADE／FDE近似；Direct-C在FDCLaTr、coverage／density／precision、Camera geometry与framing上更好，但C3保留CLaTr、recall与caption F1优势。
- v11 sequential相对C3 joint-parallel在Human／Camera semantic、coverage与framing上广泛更好，Camera paired ADE／FDE／rotation则非常接近且C3略低；两者formal solver不同，不能写成matched joint支配。
- v11自由Human的speed／acceleration／jerk与root dynamics整体低于reference；C3对应Direct-H／joint physical rows多数更接近reference。该结果是“v11 semantic／framing改善与偏低动态幅度并存”的真实trade-off，不能由heuristic contact／skate宣称physical validity已通过。
- 四臂pure4,053三模式promotion evidence已经闭合。2026-07-31显式promotion selection将C0-LAT与C0-GEO共同设为mainline；C3-25保留former-mainline baseline身份。joint protocol与physical trade-off仍按本节边界明示。

### 3.12 v11 explicit framing-control `30K` pure4,053 formal

本节只比较 exact C0-GEO parent 与其 frozen-Camera 上的 zero-init CF-4 framing
adapter。两行使用相同 pure-test `N=4,053` ordered IDs、official inputs、Euler50、
seed17、eval batch `32`、noise schedule、non-causal Stage1／decoder／stats 与
Human owner；唯一变化是 framing adapter。Direct-H exact 继承 parent，未重复生成；
`joint_parallel=false`。N64 screen 的 batch `8` 不用于 formal 数值。

| version / run | role | N / identity | formal modes | claim boundary |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | C0-GEO co-mainline parent | 4,053 / `a0d7627e…6b93` | Direct-C；sequential H→C | 无 explicit numeric framing condition |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | explicit-control diagnostic | 4,053 / `a0d7627e…6b93` | target Direct-C；target sequential H→C；swapped Direct-C diagnostic | swap 不以原 GT 计算官方语义指标；不得晋升 |

#### Formal system quality

| version / run | mode | N | FDCLaTr ↓ | CLaTr ↑ | coverage ↑ | caption F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C parent | 4,053 | 20.540 | 57.574 | 0.8236 | 0.7442 | 1.3860 / 1.4711 | 29.800 | 0.8514 / 0.1017 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | Direct-C target | 4,053 | 36.615 | 52.910 | 0.7693 | 0.6781 | 1.4318 / 1.5194 | 28.939 | 1.6116 / 0.1575 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential H→C parent | 4,053 | 29.505 | 56.103 | 0.7626 | 0.7007 | 2.9368 / 3.0395 | 71.507 | 0.5098 / 0.0768 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | sequential H→C target | 4,053 | 42.732 | 51.487 | 0.6992 | 0.6424 | 2.8785 / 2.9857 | 68.084 | 1.1446 / 0.1313 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | Direct-C swapped diagnostic | 4,053 | — | — | — | — | 1.6752 / 1.7503 | 32.631 | — |

#### Explicit-control adherence

下表的字段是 decoded true-length sequence-mean framing4 MAE。N64 只用于同机制
endpoint screen；N4,053 才是完整 cohort。swapped rows 是控制响应诊断，不是对原 GT
的语义质量排名。

| version / run | evidence role | N | screen-x ↓ | screen-y ↓ | log-scale ↓ | out-of-frame ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | parent → own target | 64 | 0.2630 | 0.3548 | 0.1092 | 0.0631 |
| v11 / `v11_f_cf4_framing_screen2k_seed17_4090g1_20260731` | 2K target condition | 64 | 0.1854 | 0.2492 | 0.0780 | 0.0490 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | 30K target condition | 64 | 0.2021 | 0.2354 | 0.0769 | 0.0505 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | parent → swapped target | 64 | 0.4612 | 1.2159 | 0.4355 | 0.2785 |
| v11 / `v11_f_cf4_framing_screen2k_seed17_4090g1_20260731` | 2K swapped condition | 64 | 0.2110 | 0.5168 | 0.2140 | 0.1385 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | 30K swapped condition | 64 | 0.2224 | 0.3914 | 0.1860 | 0.1177 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal target Direct-C | 4,053 | 0.2149 | 0.2723 | 0.0867 | 0.0595 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal target sequential H→C | 4,053 | 0.2142 | 0.3466 | 0.1280 | 0.0877 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal swapped Direct-C diagnostic | 4,053 | 0.2315 | 0.4634 | 0.1794 | 0.1113 |

`30K` N64 gate 为 target `4/4`、swap `4/4`、direction `4/4`；absent-control
Euler50 sampler max-abs 为 `0.0`。这证明 adapter 可控且没有破坏 absent path，但不
抵消 formal system quality 的多字段回退。

#### Artifact and visual identity

| version / run | artifact | SHA256 |
| --- | --- | --- |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | adapter weights | `b403794ed105974e0bb84ea68cf9f1b61790dce80e6afb4acab51d2efc010bbc` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | owning decoder | `51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | evaluator | `eecb9222b6a46c59d4275cbc87e223bacf780b941a366d90e5572cbb00a2a6eb` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal results / records / fixed8 source | `46972fc3eabe870afb20035c61bad2c2c0380c9e6d32fd7ff9ebe05e2c7ca60d` / `cd22cf47a70281e97130246f8f83238808f2e38f35b7c20106134c12c3242e5b` / `c1ca00bfc43afdc493e2b794b559e715e124762403beaacce8f8c60344f78ab7` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | visual manifest / renderer / base renderer / contact sheet | `f4659c6c64247c49a6e535158b249f392a276cb287b0745c75a246dc3bea76ef` / `7359708f940fbfb725e7f9dbef9230ea8ac3845bb0503ec70792b2b30e337441` / `b1dd9cc3c20fbe281e1b293bce529875a92c6b04e24b19c5b66ee5c0a8ab5635` / `01dbf4914585af263e83039da42d1d956a45c4a446db69378cab50179933ea99` |

formal official-input SHA256 为
`6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`；
ordered-ID SHA256 为
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`。
fixed8 与 parent 的 8 个 sample IDs 完全一致；8 个展示视频均为 H.264
`1800×736@30fps`，右侧顺序固定为 GT／target Direct-C／swapped Direct-C／target
sequential H→C。

审计裁决：显式 condition adherence 成立，且 Direct-C rotation、sequential
ADE／FDE／rotation 的 raw mean 局部改善；但 Direct-C 与 sequential 的
FDCLaTr、CLaTr、coverage、caption F1、r-FPD 与 Out 均回退。该多字段系统质量
退化触发 endpoint rejection；不晋升、不追加 seed，v11 C0-LAT 与 C0-GEO
co-mainline 不变。

### 3.13 v11 Human-text Camera fresh `105K` pure4,053 formal audit

本节比较exact matched C0-GEO与三种Human-text Camera注入设计。三条处理臂都从与
C0-GEO相同的Camera初始状态fresh训练完整Camera分支与对应Human-text模块到optimizer
step `105K`；四臂共享Pulp factual训练流、batch顺序、噪声／dropout trace、GEO目标、
Stage1、owning decoder、冻结Human teacher、seed17与EMA合同。正式评测统一使用
pure-test `N=4,053`、ordered-ID SHA256
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、official-input
SHA256 `6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`与Euler50；
模式为Direct-H、Direct-C与formal sequential Human→Camera，`joint_parallel=false`。

| version / run | role | EMA `105K` SHA256 | result SHA256 | records SHA256 |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | exact无Human-text baseline | `3cd135b0105e32cab9da877926a16d712ed480648176f909ac9044c51e7670c7` | `85d26a1705f0bb96af83b679ac7e7921c94115cbc22e603350deabc62e5f1ba1` | `1e08feb85f8c0e61dc0ebdf6d39b68af27e69cb5889da6b0677929710980475e` |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | pooled scale／shift Human observation | `750c8f394a8e8eedd363691ee588d4c203fcb58ee0b8ac5704fd6cc52395f4bf` | `697a9930d6f784c74e36e5ea2547e289e72be48eb7cc94cb2365ff8d1a0e5bb8` | `3faec2c4b722baa1980a6541c45dc204790df8dae6e71ff53d63b7ccf4a9706a` |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | temporal Human-token cross-attention | `efc44816b31fe497128c3418d6f742925ce31e5ce09b488f46a5d165f3126489` | `5a6d933ce6768c7116b356275471bc5fc0062f41642018b1bb3f9ecc1cbf7f14` | `2b69b44510f160fc3069e0d3c10e0b3849ae3f6d96c2bfc128e7346713e680dc` |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | direct Camera-velocity residual | `d817b5cb5a635972054405f1bb6ae8dfe15ae1b4036ed9a8536d57ed2c585a77` | `3416b84c064116775b782402f3cf1d5544bf0fb55384fa23bf80d42aeb64852f` | `57dee6f9362037034aa8d361a03e2d85fefa77b2d73960c4829371d87caef9f9` |

#### Direct-H frozen-owner replay

| version / run | FDTMR ↓ | TMR ↑ | coverage ↑ | root-aligned MPJPE ↓ m | global MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842760 | 0.758772 / 1.283039 | 47.239 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842762 | 0.758774 / 1.283042 | 47.239 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842762 | 0.758774 / 1.283042 | 47.239 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842762 | 0.758774 / 1.283042 | 47.239 |

三条处理臂的Direct-H逐样本replay都通过预注册的unit-specific tolerance；差异只来自
跨主机GPU kernel roundoff与少量contact阈值翻转。root-aligned MPJPE仅移除root
translation而保留heading，不能解释成local-pose error。

#### Direct-C observed-Human Camera

| version / run | FDCLaTr ↓ | CLaTr ↑ | coverage ↑ | caption F1 ↑ | r-FPD ↓ | Out ↓ | Camera ADE / FDE ↓ m | rotation ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 20.540 | 57.574 | 0.8236 | 0.7442 | 0.8514 | 0.1017 | 1.385987 / 1.471145 | 29.800 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 19.353 | 57.252 | 0.8275 | 0.7514 | 0.7930 | 0.1000 | 1.354679 / 1.446069 | 28.489 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 19.399 | 57.419 | 0.8372 | 0.7468 | 0.7846 | 0.0988 | 1.346459 / 1.438749 | 28.014 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 17.586 | 58.840 | 0.8377 | 0.7711 | 0.8699 | 0.1075 | 1.414115 / 1.501362 | 29.572 |

#### Formal sequential Human→Camera

| version / run | FDCLaTr ↓ | CLaTr ↑ | caption F1 ↑ | FDTMR / TMR | r-FPD / Out ↓ | Human global / root ADE ↓ m | Camera ADE / FDE ↓ m | rotation ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 29.505 | 56.103 | 0.7007 | 99.391 / 17.608 | 0.5098 / 0.0768 | 0.842760 / 0.758772 | 2.936792 / 3.039527 | 71.507 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 32.106 | 56.089 | 0.7128 | 99.391 / 17.608 | 0.4794 / 0.0729 | 0.842762 / 0.758774 | 2.774063 / 2.874111 | 69.890 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 43.644 | 54.055 | 0.6810 | 99.391 / 17.608 | 0.5129 / 0.0725 | 0.842762 / 0.758774 | 2.704729 / 2.805182 | 70.217 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 24.564 | 58.145 | 0.7436 | 99.391 / 17.608 | 0.4943 / 0.0781 | 0.842762 / 0.758774 | 2.945997 / 3.047307 | 71.162 |

#### Decoded-Human physical and kinematic diagnostics

| mode | version / run | Bone CV | Joint speed | Joint accel | Joint jerk | Root speed | Root accel | Root jerk | Contact† | Skate† |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Direct-H | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 2.28027e-07 | 0.025358 | 0.0231249 | 0.0368002 | 0.0178026 | 0.0119371 | 0.0168918 | 0.59616 | 0.030608 |
| Direct-H | v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Direct-H | v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Direct-H | v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Direct-C | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 2.46848e-07 | 0.0371589 | 0.0302190 | 0.0463807 | 0.0302918 | 0.0197196 | 0.0277530 | 0.491982 | 0.0418580 |
| Direct-C | v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 2.46669e-07 | 0.0371589 | 0.0302189 | 0.0463805 | 0.0302918 | 0.0197196 | 0.0277529 | 0.491997 | 0.0418569 |
| Direct-C | v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 2.46669e-07 | 0.0371589 | 0.0302189 | 0.0463805 | 0.0302918 | 0.0197196 | 0.0277529 | 0.491997 | 0.0418569 |
| Direct-C | v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 2.46669e-07 | 0.0371589 | 0.0302189 | 0.0463805 | 0.0302918 | 0.0197196 | 0.0277529 | 0.491997 | 0.0418569 |
| Sequential | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 2.28027e-07 | 0.025358 | 0.0231249 | 0.0368002 | 0.0178026 | 0.0119371 | 0.0168918 | 0.59616 | 0.030608 |
| Sequential | v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Sequential | v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Sequential | v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| factual reference | Pulp / pure-test-4,053 | 2.41667e-07 | 0.0353356 | 0.0266111 | 0.0411097 | 0.0294563 | 0.0170548 | 0.0233141 | 0.489381 | 0.0399853 |

† Contact与skate是未校准heuristic，不是physical-validity pass。四臂的Human来源相同，
因此本表只验证冻结Human owner与解码链没有被Camera设计改变，不用于给Human-text设计排名。

#### Matched Camera geometry bootstrap against C0-GEO

下表是处理臂减C0-GEO，单位依次为米／米／度；负值表示误差降低。每个cell给出
`mean delta [95% CI]`，重采样单位为相同sample，seed `260802`，共`10,000`次。

| version / run comparison | mode | Camera ADE delta | Camera FDE delta | rotation delta |
| --- | --- | ---: | ---: | ---: |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | -0.03131 [-0.06971, +0.00596] | -0.02508 [-0.06355, +0.01295] | -1.31122 [-2.26411, -0.37093] |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | -0.16273 [-0.19543, -0.13000] | -0.16542 [-0.19839, -0.13229] | -1.61680 [-2.64821, -0.59007] |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | -0.03953 [-0.07561, -0.00189] | -0.03240 [-0.06981, +0.00569] | -1.78586 [-2.73627, -0.81166] |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | -0.23206 [-0.26523, -0.19831] | -0.23435 [-0.26847, -0.19979] | -1.28961 [-2.39623, -0.18125] |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | +0.02813 [-0.00824, +0.06345] | +0.03022 [-0.00732, +0.06676] | -0.22866 [-1.16223, +0.68281] |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | +0.00920 [-0.02168, +0.03949] | +0.00778 [-0.02402, +0.03946] | -0.34554 [-1.34676, +0.62894] |

审计SHA256为`3f410e70f870dc9b0c012bcc8e69a09f9c0823b3606f0d5e1776e129f87e12be`；
audit implementation为`a43b51ce7c322e0076a34b2aff7abf579d60b3cb3a0d9faef0a2811f2a2010bf`；
fresh evaluator为`306e5d3e503195d9273521a26b29fec41ca553fa95645bcf48d77d8cf816c632`。
固定8例覆盖两种Camera模式与Pulp／C0-GEO／三个处理臂共`80`个cell，visual manifest
SHA256为`eeeff66c6e91d998e88213e582778a9e2c0a2a8125b2cf3dad67f0a997914edc`。

审计裁决：三臂形成明确Pareto。HT-HX的Camera geometry最强，但sequential语义与
caption明显回退；HT-DR的Direct-C与sequential Camera semantic／caption最强，但相对
C0-GEO的六项Camera geometry CI全跨零，且Direct-C r-FPD／Out回退；HT-FILM在
sequential geometry、caption与projective framing上较均衡，但FDCLaTr不占优。因此不选
单一全胜设计，也不改变C0-LAT／C0-GEO共同mainline。该formal只评测matching Human text；
没有同endpoint的HT0／HTS完整cohort，故不能把全部增益归因于正确Human语义，更不能外推
为multi-pair Director、event grounding或Rect证据。

### 3.14 v11 C0 seed23 `105K` pure4,053 matched repeat

两臂均以训练seed `23`从零启动，在各自fresh parent的full-state `30K`边界恢复并连续训练
至Camera optimizer step `105K`；恢复包含model、optimizer、scheduler与RNG state，不是
只载入权重。两臂共享exact v9 Pulp-only non-causal Stage1 owner、冻结Human teacher、
cache／stats／sample identities与训练exposure，唯一臂间变量为Camera objective。正式评测
固定使用eval seed `17`、EMA `105K`、pure-test `N=4,053`、ordered-ID SHA256
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、official-input
SHA256 `6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`、batch `32`与
shifted-sigma Euler50；模式为Direct-H、Direct-C与formal sequential Human→Camera，
`joint_parallel=false`。

正式repeat audit位于
`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v11_c0_seed17_seed23_repeat_audit_20260803/`。
`seed_repeat_audit.json` SHA256为
`b87872ef96af20afaf385c54cae5ea5c754208c405b6dd2328de86730d4fb2a4`；audit implementation
SHA256为`846a5b4d19f76697d58a22fdd8dd300cbd1f9b18cb27427a84e61da93414e05f`。
审计逐臂验证training contract、Stage1 owner、non-causal边界、checkpoint／cache／stats／
decoder、ordered IDs、sampler、evaluator与artifact hash，并执行10,000次matched-sample
bootstrap。LAT／GEO的`fixed_samples.pt` SHA256分别为
`36dfe34cd13a752c3ba2590d0a335b20856e5ea07b1b48944455d54c8f47d9ca`与
`256778c38332c00af84a08c493d44bb9f8a9467b86251fc0c3d95504e55868d5`。

| version / run | EMA `105K` SHA256 | input contract SHA256 | evaluation contract SHA256 | result SHA256 | records SHA256 |
| --- | --- | --- | --- | --- | --- |
| v11 / `paperA_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | `076dad8276da2283086ace6701f93433e541fa7e6d72ebef54a16d0b082c8d24` | `51f16a54220064d22a16489a59ccc2401b09bc09a1900fa0e358b9bfdaabd67d` | `eed9fef9316fddc8c2114b886f38b2f433d5c0d472bd7d8861c359503dc2b39f` | `d13109ebc2e157d3acf8ac4ce8c60148d7a71236a13ade0fed8f97414eeb4ab1` | `510beb24b148ab2f15ba4ee7f9c95a2f20cb76f414e085abf439b30f3571fdd0` |
| v11 / `paperA_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | `ded0e06947bf5dd9b100c485acce59e7e14eb4995023cd0f5bc250627d5740379` | `7be6d444cb9fe14b819b925a4fb326a2e9561995023cd0f5bc250627d5740379` | `08e8516d05e6145e9f59d34a305fcb0a2d2c13d90fa98cb579d623e00a339b8a` | `8bf54167a73fa8e38dc304ae0de576c94cbb48ad1f8571a9380fdd6761544ddd` | `fad420b9bd910e894b964f332c31398d9044c3985bfd2674c9c32410d38b5641` |

#### Direct-H frozen-owner replay

两臂的Direct-H official metrics与paired geometry逐字段一致，并与seed17 owner replay通过
预注册的逐样本／cohort守卫。root-aligned MPJPE只移除root translation，仍保留heading。

| version / run | N | FDTMR ↓ / TMR ↑ | coverage / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM distance ↓ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean / final / unwrapped final ↓ deg |
| --- | ---: | --- | --- | --- | ---: | --- | --- | --- |
| v11 / seed23 C0-LAT + C0-GEO `105K` | 4,053 | 99.391 / 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 49.705 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |

#### Direct-C observed-Human Camera

| version / run | FDCLaTr ↓ / CLaTr ↑ | coverage / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM distance ↓ | caption P / R / F1 ↑ | r-FPD / Out ↓ | Camera ADE / FDE ↓ m | rotation ↓ deg | observed-H global / root-aligned MPJPE ↓ m |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | --- |
| v11 / seed23 C0-LAT `105K 4090g0` | 20.852 / 56.931 | 0.8278 / 1.0895 / 0.9134 / 0.5581 | 0.2297 / 0.3943 / 0.5105 | 23.409 | 0.7801 / 0.6984 / 0.7339 | 0.8139 / 0.1010 | 1.398343 / 1.489706 | 29.922 | 0.125455 / 0.048795 |
| v11 / seed23 C0-GEO `105K 4090g1` | 20.303 / 58.058 | 0.8362 / 1.0620 / 0.9050 / 0.5690 | 0.2388 / 0.3997 / 0.5191 | 23.085 | 0.7952 / 0.7151 / 0.7509 | 0.8586 / 0.1035 | 1.384952 / 1.471736 | 29.255 | 0.125455 / 0.048795 |

#### Formal sequential Human→Camera

| version / run | FDCLaTr ↓ / CLaTr ↑ | coverage / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM distance ↓ | caption P / R / F1 ↑ | r-FPD / Out ↓ | H FDTMR / TMR | H global / root-aligned MPJPE ↓ m | Camera ADE / FDE ↓ m | rotation ↓ deg |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | ---: |
| v11 / seed23 C0-LAT `105K 4090g0` | 28.333 / 56.174 | 0.7752 / 0.9994 / 0.8868 / 0.5283 | 0.2189 / 0.3795 / 0.4999 | 23.636 | 0.7618 / 0.6783 / 0.7074 | 0.5130 / 0.0773 | 99.391 / 17.608 | 0.842762 / 0.228751 | 2.929020 / 3.029515 | 71.339 |
| v11 / seed23 C0-GEO `105K 4090g1` | 27.449 / 57.057 | 0.7804 / 0.9928 / 0.8934 / 0.5260 | 0.2226 / 0.3847 / 0.5078 | 23.378 | 0.7712 / 0.6877 / 0.7170 | 0.4826 / 0.0758 | 99.391 / 17.608 | 0.842762 / 0.228751 | 2.934441 / 3.035767 | 71.202 |

#### Complete decoded-Human physical／kinematic diagnostics

每个cell是`mean / median / p90`。这些字段是decoded-Human no-reference heuristics，不是
Camera physical metric，也不能解释成ground penetration／floating等calibrated validity。
Direct-H与sequential共享同一冻结Human输出；Direct-C是observed-H reconstruction。两条
Camera objective的Human物理字段逐字段一致。

| version / run | mode | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | --- | --- | --- | --- |
| v11 / seed23 C0-LAT + C0-GEO `105K` | Direct-H = sequential Human | 2.279e-7 / 2.220e-7 / 2.626e-7 | 0.025358 / 0.017675 / 0.053936 | 0.023125 / 0.016568 / 0.048186 | 0.036800 / 0.026036 / 0.076142 |
| v11 / seed23 C0-LAT + C0-GEO `105K` | Direct-C observed-H reconstruction | 2.467e-7 / 2.250e-7 / 3.131e-7 | 0.037159 / 0.023330 / 0.083141 | 0.030219 / 0.018382 / 0.066291 | 0.046381 / 0.027812 / 0.099302 |

| version / run | mode | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | --- | --- | --- | --- | --- |
| v11 / seed23 C0-LAT + C0-GEO `105K` | Direct-H = sequential Human | 0.017803 / 0.010157 / 0.041564 | 0.011937 / 0.007417 / 0.026799 | 0.016892 / 0.010380 / 0.037599 | 0.596170 / 0.595745 / 1.000000 | 0.030611 / 0.019465 / 0.063216 |
| v11 / seed23 C0-LAT + C0-GEO `105K` | Direct-C observed-H reconstruction | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011576 / 0.043855 | 0.027753 / 0.016443 / 0.061077 | 0.491997 / 0.437500 / 1.000000 | 0.041857 / 0.024370 / 0.085574 |

#### Two-seed matched Camera geometry bootstrap

下表差值均为前者减后者；每个cell为`mean delta [95% CI]`，使用相同sample执行10,000次
paired resample。八个mode-level comparison共24个Camera geometry CI，全部跨零。

| version / comparison | mode | Δ ADE m（95% CI） | Δ FDE m（95% CI） | Δ rotation deg（95% CI） |
| --- | --- | --- | --- | --- |
| v11 / seed17 C0-GEO − C0-LAT | Direct-C | -0.02648 [-0.06529, +0.01245] | -0.02738 [-0.06681, +0.01240] | -0.12178 [-1.08853, +0.80951] |
| v11 / seed17 C0-GEO − C0-LAT | sequential | -0.00600 [-0.03600, +0.02330] | -0.00266 [-0.03219, +0.02676] | +0.07250 [-0.91249, +1.08543] |
| v11 / seed23 C0-GEO − C0-LAT | Direct-C | -0.01339 [-0.04775, +0.02179] | -0.01797 [-0.05326, +0.01793] | -0.66706 [-1.55837, +0.26073] |
| v11 / seed23 C0-GEO − C0-LAT | sequential | +0.00542 [-0.02912, +0.04100] | +0.00625 [-0.02959, +0.04338] | -0.13707 [-1.15967, +0.90620] |
| v11 / C0-LAT seed23 − seed17 | Direct-C | -0.01413 [-0.05520, +0.02500] | -0.00882 [-0.05031, +0.03073] | -0.00046 [-0.94181, +0.95590] |
| v11 / C0-LAT seed23 − seed17 | sequential | -0.01378 [-0.04625, +0.01881] | -0.01267 [-0.04572, +0.01995] | -0.09554 [-1.07293, +0.90480] |
| v11 / C0-GEO seed23 − seed17 | Direct-C | -0.00104 [-0.03533, +0.03391] | +0.00059 [-0.03497, +0.03697] | -0.54573 [-1.43111, +0.35788] |
| v11 / C0-GEO seed23 − seed17 | sequential | -0.00235 [-0.03332, +0.02887] | -0.00376 [-0.03487, +0.02825] | -0.30511 [-1.29920, +0.67211] |

审计裁决：seed23重现了冻结Human owner的逐样本保持，并未产生稳健Camera geometry
objective胜者。seed23的GEO在两种Camera模式的多数raw semantic／caption均值上高于LAT，
但seed17是混合Pareto，且当前official semantic evaluator没有对应的逐样本bootstrap单位；
因此只作描述，不把raw均值趋势升级为显著性结论。C0-LAT与C0-GEO继续共同mainline；本轮
关闭独立训练seed缺口，但不替代后续sealed audit、视觉失败分层或matched cascade。

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
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 / ordered SHA `a0d7627e…6b93` | deterministic exact-length owning encoder–decoder round trip；decode batch1 | Paper A representation evaluator SHA `e6c8fb08…5eb0` | H128＋C48；显式I16删除；owning `D_h/D_c/D_f`；non-causal |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 / ordered SHA `a0d7627e…6b93` | deterministic exact-length owning encoder–decoder round trip；decode batch1 | Paper A representation evaluator SHA `e6c8fb08…5eb0` | H128＋I16＋C1REL-C48；owning `D_h/D_c/D_f`恢复world Camera14；non-causal |
| v10 Human-relative Camera old-3-loss Phase B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | historical `210K` Camera-only paired reconstruction diagnostic | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；GT Human supplies inverse-relative reference | v10 native + canonical historical Stage1 endpoint evaluator [[Storymotion-exp-sha]] | frozen Phase-A Human128 owner + independent relative-Camera48 encoder/decoder；missing framing backprop；non-causal [[Storymotion-exp-sha]] |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；decode batch1 | redesign Pulp [[Storymotion-exp-sha]] | same redesigned architecture；owning decoder [[Storymotion-exp-sha]] |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D Human-only root/local paired reconstruction diagnostic | 1,460 / [[Storymotion-exp-sha]] | deterministic exact-length owning Human encoder–decoder round trip；decode batch1 | redesign HumanML [[Storymotion-exp-sha]] | converted HML root/local under Pulp normalization；rot6D `4:136` prohibited mean-imputed/unobserved；decoder [[Storymotion-exp-sha]] |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D Human-only root/local paired reconstruction diagnostic | 1,460 / [[Storymotion-exp-sha]] | deterministic exact-length owning Human encoder–decoder round trip；decode batch1 | redesign HumanML [[Storymotion-exp-sha]] | converted HML root/local under Pulp normalization；rot6D `4:136` prohibited mean-imputed/unobserved；decoder [[Storymotion-exp-sha]] |

以上八条 contract 与 checkpoint 均显式 `is_causal=false`。历史 machine field `pose6d_policy` 是旧命名，实际指 Human199 channels `4:136` 的 joint rot6D；本页统一使用 **rot6D**。2026-07-27 的 policy correction 判定无显式 missingness 的 Pulp-mean填充为禁止的伪观测：上表 HML rows只保留已解码 root/local diagnostic 数值，mixed checkpoint不得进入正式 Stage2。

### 6.2 Pulp pure4,053 complete Human reconstruction

| version / run | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.068967 | 0.024190 | 0.058252 | 0.148365 | 4.947 | 9.309 | 10.633 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.120708 | 0.042136 | 0.100757 | 0.248722 | 10.434 | 18.751 | 20.757 |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.120919 | 0.042175 | 0.100965 | 0.249442 | 10.447 | 18.775 | 20.786 |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.120705 | 0.042187 | 0.100737 | 0.248654 | 10.452 | 18.877 | 20.897 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.133869 | 0.044779 | 0.112616 | 0.279547 | 11.897 | 21.218 | 23.622 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.718084 | 0.212668 | 0.614757 | 1.136651 | 82.011 | 91.159 | 418.094 |

### 6.3 Pulp pure4,053 complete Camera and projective reconstruction

| version / run | mode | N | joint Cam ADE ↓ m | joint Cam FDE ↓ m | GT-H Cam ADE ↓ m | GT-H Cam FDE ↓ m | rotation ↓ deg | FOV-H ↓ deg | FOV-W ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.039486 | 0.048270 | 0.036252 | 0.045599 | 0.704710 | 0.232809 | 0.253795 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.037654 | 0.043840 | 0.026146 | 0.033668 | 0.575890 | 0.204003 | 0.262347 |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.047452 | 0.067396 | 0.037331 | 0.059294 | 0.736642 | 0.230362 | 0.294394 |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.044945 | 0.057538 | 0.035511 | 0.049641 | 0.820222 | 0.186437 | 0.307167 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.121757 | 0.377332 | 0.021567 | 0.173423 | 0.617630 | 2.265990 | 1.462458 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.052681 | 0.058489 | 0.026317 | 0.034576 | 0.598872 | 0.197493 | 0.269706 |

| version / run | mode | N | joint UV L2 ↓ | center L2 ↓ | log-scale abs ↓ | out-ratio abs ↓ | visible recon / ref | zero-visible recon / ref ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.120701 | 0.077910 | 0.024236 | 0.032460 | 0.491548 / 0.497732 | 0.016594 / 0.007547 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.160790 | 0.096190 | 0.029678 | 0.039550 | 0.484065 / 0.497732 | 0.023921 / 0.007547 |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.180547 | 0.101843 | 0.031005 | 0.041164 | 0.484226 / 0.497732 | 0.023734 / 0.007547 |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.157706 | 0.101260 | 0.029883 | 0.040497 | 0.485306 / 0.497732 | 0.024223 / 0.007547 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.353564 | 0.107943 | 0.066030 | 0.041602 | 0.497488 / 0.497732 | 0.012102 / 0.007547 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.848923 | 0.343268 | 0.132111 | 0.122139 | 0.435095 / 0.497732 | 0.118101 / 0.007547 |

### 6.4 Pulp pure4,053 complete decoded physical/kinematic summary

每个 cell 是 `mean / median / p90`。这些是 reconstruction output，不是 free generation；contact/skate 使用 own-motion floor heuristic，不是 calibrated ground metric。

| version / run | mode | N | bone CV | joint speed | joint acceleration | joint jerk |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / pure4053 | reference | 4,053 | 2.677e-7 / 2.376e-7 / 3.423e-7 | 0.034022 / 0.020797 / 0.078097 | 0.024906 / 0.014389 / 0.056310 | 0.038199 / 0.021969 / 0.087722 |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.025068 / 0.018822 / 0.049072 | 0.035164 / 0.022071 / 0.078341 | 0.027056 / 0.016760 / 0.058918 | 0.040600 / 0.025336 / 0.087586 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.026000 / 0.020484 / 0.050117 | 0.035668 / 0.022309 / 0.079710 | 0.028277 / 0.017335 / 0.062101 | 0.043172 / 0.026360 / 0.094611 |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.026001 / 0.020474 / 0.050088 | 0.035671 / 0.022296 / 0.079721 | 0.028280 / 0.017332 / 0.062071 | 0.043178 / 0.026340 / 0.094728 |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.026002 / 0.020492 / 0.050089 | 0.035668 / 0.022325 / 0.079727 | 0.028276 / 0.017322 / 0.062056 | 0.043168 / 0.026369 / 0.094644 |
| v10 HREL-C old-3-loss Phase-B / final210K diagnostic | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.021380 / 0.016591 / 0.041141 | 0.035518 / 0.022162 / 0.079693 | 0.027760 / 0.016814 / 0.061350 | 0.042220 / 0.025519 / 0.093351 |
| Redesign HML+Pulp / true4053 r4 | joint paired reconstruction | 4,053 | 0.037738 / 0.030727 / 0.069701 | 0.052227 / 0.038916 / 0.104918 | 0.037689 / 0.025133 / 0.080011 | 0.052494 / 0.034237 / 0.111604 |

| version / run | mode | N | root speed | root acceleration | root jerk | contact heuristic | foot skate heuristic |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / pure4053 | reference | 4,053 | 0.029456 / 0.016709 / 0.067934 | 0.017055 / 0.009513 / 0.039636 | 0.023314 / 0.013070 / 0.053262 | 0.492193 / 0.428571 / 1.000000 | 0.039121 / 0.021590 / 0.079352 |
| C3-25 Stage1 / canonical true4053 r1 | joint paired reconstruction | 4,053 | 0.030193 / 0.017489 / 0.069621 | 0.019302 / 0.011327 / 0.043122 | 0.026765 / 0.015810 / 0.059673 | 0.485486 / 0.423729 / 0.991597 | 0.038878 / 0.023307 / 0.081541 |
| Redesign Pulp-only / true4053 r4 | joint paired reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069146 | 0.019719 / 0.011587 / 0.043854 | 0.027753 / 0.016438 / 0.061139 | 0.484022 / 0.421053 / 0.999598 | 0.039454 / 0.023312 / 0.082005 |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.030293 / 0.017522 / 0.069152 | 0.019722 / 0.011590 / 0.043833 | 0.027757 / 0.016450 / 0.061155 | 0.483933 / 0.421429 / 0.999598 | 0.039482 / 0.023321 / 0.081861 |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.030291 / 0.017520 / 0.069149 | 0.019718 / 0.011575 / 0.043866 | 0.027746 / 0.016434 / 0.061189 | 0.483900 / 0.420455 / 0.999598 | 0.039503 / 0.023321 / 0.081758 |
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
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | Stage1 `636K` former-mainline baseline | 4,053 | 0.068967 / 0.024190 | 0.058252 / 0.148365 | 4.947 | 0.039486 / 0.048270 | 0.036252 / 0.045599 | 0.704710 |
| v8.1C C3-50 / center50 seed17 | Stage1 `636K` exploratory | 4,053 | 0.073166 / 0.025593 | 0.061678 / 0.154323 | 5.194 | 0.036412 / 0.045116 | — | 0.718 |
| v8.1B / residual AE seed17 | Stage1 `636K` architecture control | 4,053 | 0.076655 / 0.028245 | 0.062513 / 0.186141 | 6.311 | 0.050705 / 0.065467 | — | 1.170 |
| v8.2 / human200 seed17 | Stage1 `636K` representation control | 4,053 | 0.068706 / 0.012999 | 0.065847 / 0.242966 | 1.275 | 0.053028 / 0.061554 | — | 0.569 |
| v9 redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | Phase A/B/C `636K`；current C0 shared Stage1 owner | 4,053 | 0.120708 / 0.042136 | 0.100757 / 0.248722 | 10.434 | 0.037654 / 0.043840 | 0.026146 / 0.033668 | 0.575890 |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched Phase A/B/C `636K` representation ablation | 4,053 | 0.120919 / 0.042175 | 0.100965 / 0.249442 | 10.447 | 0.047452 / 0.067396 | 0.037331 / 0.059294 | 0.736642 |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | parameter-matched Phase A/B/C `636K` representation arm | 4,053 | 0.120705 / 0.042187 | 0.100737 / 0.248654 | 10.452 | 0.044945 / 0.057538 | 0.035511 / 0.049641 | 0.820222 |
| v10 HREL-C old-3-loss / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | Phase A `210K` + frozen-H Phase B `210K` historical diagnostic | 4,053 | 0.133869 / 0.044779 | 0.112616 / 0.279547 | 11.897 | 0.121757 / 0.377332 | 0.021567 / 0.173423 | 0.617630 |

只有C3、v9与v10已在当前canonical projective schema下完整复核；更早版本不以缺失字段补造结果。`raw joint-out occupancy`是描述性占比，不能与paired Out error或Stage2的zero-visible `Out`混用。

| version / run | projective joint UV L2 ↓ | center L2 ↓ | log-scale abs ↓ | paired Out error ↓ | raw joint-out occupancy | visible recon / ref | zero-visible recon / ref ↓ | eligibility boundary |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| v8.1C C3-25 / canonical true4053 r1 | 0.120701 | 0.077910 | 0.024236 | 0.032460 | — | 0.491548 / 0.497732 | 0.016594 / 0.007547 | former-mainline baseline |
| v9 redesign Pulp-only / canonical true4053 r4 | 0.160790 | 0.096190 | 0.029678 | 0.039550 | — | 0.484065 / 0.497732 | 0.023921 / 0.007547 | current C0 shared Stage1 owner |
| Paper A NoInt-HREL / formal true4053 | 0.180547 | 0.101843 | 0.031005 | 0.041164 | — | 0.484226 / 0.497732 | 0.023734 / 0.007547 | Stage1 ablation；Stage2未授权 |
| Paper A C1REL / formal true4053 | 0.157706 | 0.101260 | 0.029883 | 0.040497 | — | 0.485306 / 0.497732 | 0.024223 / 0.007547 | Stage1 representation arm；未晋升 |
| v10 HREL-C old-3-loss / final210K diagnostic | 0.353564 | 0.107943 | 0.066030 | 0.041602 | 0.500543 native recon | 0.497488 / 0.497732 | 0.012102 / 0.007547 | historical diagnostic；no cache／promotion |

> [!warning] `Out≈0.50` 的语义修正
> v10旧表的 `projective_outscreen≈0.50` 是**重建结果中逐帧、逐关节的原始出框占比**，不是 reconstruction-versus-GT误差，也不应作为lower-is-better选点轴。canonical reference本身只有约`0.497732`关节可见，即原始出框占比本来就约为`0.502268`。因此“Out误差约50%”是字段命名与方向解释错误；真正的paired Out error是`0.041602`。

剩余 `4.16%` paired Out误差略高于v9的`3.96%`和C3-25的`3.25%`。当前证据支持三个机制，而不是单一已证明根因：

1. 该旧v10 Phase-B objective只优化relative reconstruction、relative temporal与rotation geodesic；FOV、screen center/scale与projective framing只记录不反传。对应地，旧run的FOV与UV/log-scale误差明显高于v9/C3；这支持补回framing supervision，但修正版尚无formal数值，不能提前宣称已改善。
2. `Phi^-1`必须使用冻结Phase-A Human root/heading。v10 joint Camera ADE为`0.121757 m`，而替换为GT Human anchor后为`0.021567 m`；这说明Human root/heading reconstruction coupling是joint world/projective误差的重要来源，但不能据此把全部projective残差都归给Human。
3. visibility是屏幕边界上的离散阈值。FOV、center、scale和Human root的连续小误差在边缘构图样本上会被放大为joint in/out翻转。

尚未单独补算GT-H projective全套分解，因此“FOV是唯一根因”或“全部来自Human”都不成立。历史`207K`选择artifact继续保留provenance，但其framing轴把raw occupancy当作可最小化误差；它不再拥有当前endpoint决策权。旧final `210K`只保留历史diagnostic，修正版通过长训与formal审计前没有v10 cache候选；该v10边界不影响已完成的v11 C0共同mainline selection。

### 6.7 Matched interpretation

- Pulp `N=4,053` 测试的是 Pulp TRAM/SMPL + Camera14 域；HumanML `N=1,460` 测试的是 converted 20→30 fps root/local-only 域。优势反转首先是 **source-domain specialization**，不是 sample count 本身造成的 evaluator 反转。
- 两条 redesign arm 的 architecture、objective、phase lengths、optimizer steps 与 role exposure matched；唯一训练数据轴是 anchor source。mixed arm 直接见过 HML root/local，却以 partial supervision 替换大量 matched Pulp anchor exposure；当前 replay ratio 与 rot6D 伪缺失输入都是 setting boundary。后者已使该 mixed setting 对 promotion/Stage2 不合规。
- Pulp 上两臂的 GT-H Camera ADE 几乎相同（`0.026146` vs `0.026317 m`），而 Human/root/projective error 大幅分离；因此 mixed 的主要 Pulp 回退不是 standalone Camera decoder failure。
- Pulp/HML 数值反转只保留为 retrospective domain diagnostic / no promotion；不得把 HML partial result 写成完整 Human199、Camera、Stage2 或 generation 能力。

### 6.8 Paper A NoInt-HREL／C1REL matched Stage1 audit

本节身份是 **Paper A StoryMotion**。reference、NoInt-HREL与C1REL使用相同Pulp pure4,053 ordered IDs、
真实有效长度、seed17、non-causal边界、deterministic owning encoder–decoder round trip和canonical
Camera14 raw bridge。paired bootstrap以sample为单位做10,000次重采样，seed `17`；下表cell均为
`arm − HREL reference [95% CI]`。误差项正值表示回退。

| version / run | global MPJPE m | root-aligned MPJPE m | root ADE m | root FDE m |
| --- | ---: | ---: | ---: | ---: |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | 0.000211 [-0.000072, 0.000513] | 0.000039 [-0.000010, 0.000086] | 0.000208 [-0.000077, 0.000506] | 0.000720 [0.000005, 0.001454] |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | -0.000002 [-0.000886, 0.000759] | 0.000052 [-0.000072, 0.000170] | -0.000020 [-0.000896, 0.000733] | -0.000069 [-0.002813, 0.002382] |

| version / run | joint Cam ADE m | joint Cam FDE m | GT-H Cam ADE m | GT-H Cam FDE m | rotation deg |
| --- | ---: | ---: | ---: | ---: | ---: |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | 0.009798 [0.008764, 0.010824] | 0.023556 [0.021871, 0.025231] | 0.011186 [0.010050, 0.012295] | 0.025626 [0.023850, 0.027372] | 0.160751 [0.134838, 0.196613] |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | 0.007291 [0.006396, 0.008184] | 0.013697 [0.012359, 0.015063] | 0.009365 [0.008420, 0.010329] | 0.015973 [0.014574, 0.017384] | 0.244332 [0.182620, 0.326526] |

| version / run | joint UV L2 | center L2 | log-scale abs | paired Out error |
| --- | ---: | ---: | ---: | ---: |
| Paper A NoInt-HREL / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | 0.019756 [0.001759, 0.041305] | 0.005653 [0.003732, 0.007953] | 0.001327 [0.000812, 0.001889] | 0.001613 [0.000936, 0.002308] |
| Paper A C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | -0.003085 [-0.025255, 0.018458] | 0.005069 [0.003204, 0.007278] | 0.000205 [-0.000615, 0.000989] | 0.000947 [0.000379, 0.001525] |

NoInt-HREL的Human均值基本保持，只有root FDE出现极小的正差；五项Camera geometry和四项projective
error的CI均在零上方。因此本Stage1证据支持“删除显式I16会损害owning reconstruction／framing”，
但不单独证明Stage2 generation中的I16必要，更不能扩写为Camera不依赖Human。C1REL同样守住Human，
但五项Camera geometry均回退，projective center／Out也回退，joint UV与scale没有稳健差异；它没有
形成可晋升的稳定Pareto。Stage1不消费Camera text，不能从本artifact声称C1REL text adherence改善。

预声明只写了“严重退化可降级”，没有冻结数值阈值；因此本次不事后发明binary severe gate，不授权
Stage2，也不把C1REL直接判为最终失败。HREL继续保持当前representation owner；是否还值得为C1REL
支付Stage2预算，只能在canonical Camera text冻结后按新的最小合同明确裁决。

NoInt-HREL checkpoint／training contract／evaluation contract／result／records／fixed-samples／eval-manifest
SHA256依次为`968133147d7e1b1202e5bf9ff5e046ae8ff0c592573361821804a1823562ef75`、
`599faf76f1b019d9d64160cab6e6d3c292a4befb5e1165d4bb54e35979877f66`、
`368f4dd1c8641766dcc8ff952af25881b316aee4218992f0e9e44cb145175078`、
`f946e0f29246143258d2bc5d0359b7a8950c9c2509584fb6fb604c2fcb542045`、
`56256318aff641496ddf0d699595c13b92ece7b641f5085fca14aa44c38036c9`、
`bad0e437eeeb8d2ed967d014cd164113592233c231d07efa7475a96164a14150`、
`7f5502be47864471f3ef92de803521f64a6fcb92831efd061fc38c59aa64eb2e`。

C1REL对应SHA256依次为`5af7317fcaea0694b457cecf7a106b5ecd26e8acdfbe47a7bd6571cebc0017f0`、
`745ff16cc853ce20de6c86690dcc8a9569c2cf4a9a1ce8cb8ab12f959fd0e9c2`、
`e5679b14d9e997bdafc28638796a19ce9c5ba98a8661ea3f43558b44503f50dd`、
`dd3c0ac1cea438659a2071679275e4225ba7bde96aa92bbc3c8cd3841f92b267`、
`b5685a7ee650e248c7da05893e6f73b5c39fba65487463478e454c1ab1cc71d0`、
`c36afd833e5823cea22e179027763ed0b641af0c738aeca518dcafb089c01e69`、
`cecf75f6f527cfb39907df7f5d02e1d2e60daebaa7f471af3cab9d5f2d2453b1`。
cross-arm comparison／manifest SHA256为
`b6fe50d255cd574385f8dcb75bc1eb7692371f8c770bb780674cb84b3afc2bed`／
`dd89f88bb4fb08dc4cb0bb2dd8d2b126025e33117c983d6e7a20557c9700d254`；formal evaluator与
comparison evaluator SHA256为`e6c8fb08f830b24dd2d36bedd4a3942065e807029149d073a67e14fb5e625eb0`／
`c577b1d81d00200cdc24964994c15e7c1a62c53f49a43bf2dbbdfbc273c83e95`。

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
| v11 C0-LAT / pure4053 | pure full cohort；Camera EMA `105K`；formal sequential | co-mainline；与GEO并列，不从raw mean选单臂 |
| v11 C0-GEO / pure4053 | pure full cohort；Camera EMA `105K`；formal sequential | co-mainline；与LAT并列，不把跨零CI写成稳健增益 |
| C3-25 / canonical4053 r2 | pure full cohort；`step_105000.pt`；three modes share checkpoint/cache/decoder | former-mainline formal baseline；不得与 first-512 row 当作同一 sample count |
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

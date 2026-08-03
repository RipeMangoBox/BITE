---
title: "StoryMotion v8.2333 Data Quality, Pool, and Training Allocation Contract"
status: quality_gradient_v1_research_complete_v2_required_no_training_authorization
archived: 2026-08-03
hypothesis: |
  在冻结 C3-25 representation、owning decoder 与 Unified Stage2 实现后，
  只改变可逆、task-aware 的训练资格与抽样分布，可以检验物理质量、
  Human 文本对齐和 Human-Camera 条件质量对生成可靠性的因果影响。
tags:
  - StoryMotion
  - data-curation
  - stage1
  - stage2
  - sft
  - status/active
aliases:
  - StoryMotion-v8.2333-Curation-Plan
  - StoryMotion-SFT-Data-Prepare
source_notes:
  - "[[current]]"
  - "[[archived/superseded-design/2026-07-22_storymotion-sft-data-prepare-premerge]]"
created: 2026-07-17T17:35:00+08:00
updated: 2026-07-23T16:55:00+08:00
---

# StoryMotion v8.2333 Data Quality, Pool, and Training Allocation Contract

> [!abstract] 当前裁决
> 本页是 v8.2333 数据质量、pool 定义、分档结果、nested volume 和未来训练分配的唯一正式 Markdown owner。全量 `162,760` motion 的 quality table 与五类 `8K / 16K / 32K / 64K` v1 research controls 已完成；只有 `D_H` 能按当前 available Human 轴物化为 candidate。实现复核又发现 v1 的 `q_H` stratum 混入 Camera dynamics，因此 v1 只能保留为已审计 research provenance，必须在新 immutable root 生成 axis-pure v2。`q_C`、完整 `q_HC` 与 `q_CT` 尚未闭合，因此 `D_AE`、`D_C`、`D_J` 只能叫 partial eligibility，不能叫 clean dataset，也不能训练。所有新产物均为 immutable/reversible manifest，`manual_labels=0`、`source_deleted=false`、`training_authorized=false`。

> [!info] 文档合并
> 原 `sft-data-prepare.md` 的有效训练分配合同已合并到本页；合并前原稿移至 [[archived/superseded-design/2026-07-22_storymotion-sft-data-prepare-premerge]]，只保留 provenance，不再维护第二套 active contract。

## 1. 当前进度与授权边界

| 工作项 | 状态 | 已完成结果 | 当前边界 |
| --- | --- | --- | --- |
| raw lock | complete | 162,760 joint motions；326,144 role rows | 不删除、不回写 parent |
| Physical-v2 full scores | complete | 162,760/162,760 per-sample rows | 未提供的物理维度记 `unresolved` |
| Human TMR-v4 full scores | complete | 162,760/162,760；singleton replay exact | 只支持 `q_HT`，不支持 `q_CT` |
| full quality table | complete v1 provenance | 162,760 rows；每维 raw/rank/bin/status/reason/scorer hash | axis impurity/min-n blocker；不能当最终 rank |
| `D_H` nested research pools | complete v1 provenance | 五类 control × 四个 nested sizes | research only；不授权 continuation |
| `q_C` | partial | center/rotation 的部分 dynamics 已计算 | path、rotation jerk/discontinuity 未闭合 |
| `q_HC` | partial | valid-length synchronization 已计算 | projection/framing/Out/center/scale/margin 未闭合 |
| `q_CT` | unresolved | 0 个 verified Camera semantic score | 不能构造 `D_C` 或 `D_J` |
| matched curation ablation | not started | 0 training runs | 必须另立 `training_authorized=true` contract |

本轮不训练 scorer、不训练 Stage1/Stage2、不做人工标注，也不删除 source。旧 binary lattice 保留，但不再承担最终分档。

## 2. 数据单位与 pool 定义

### 2.1 计数单位

| 单位 | 数量 | 精确定义 |
| --- | ---: | --- |
| joint motion record | 162,760 | 同步 Human motion、Camera trajectory 与文本文件的 clip；联合样本基数 |
| Human role row | 162,760 | `(motion_id, human, caption_index)` |
| Camera role row | 163,384 | `(motion_id, camera, caption_index)`；107 个文件含多个 Camera captions |
| role-aware rows | 326,144 | 两类 role rows 之和；不是 joint pair 数 |

Camera 比 motion 多 `624` 行只表示多 caption 条件。任何训练或 coverage 表都必须分别报告 unique motions、role rows 与 task conditions，不能把 `326,144` 写成 joint sample 数。

### 2.2 五个独立质量轴

| axis | 含义 | 当前证据状态 |
| --- | --- | --- |
| `q_H` | Human motion quality | available dimensions 已分解；缺失维度显式 unresolved |
| `q_C` | Camera trajectory quality | 部分 dynamics available；整体未闭合 |
| `q_HC` | Human-Camera geometry/framing quality | 仅 length synchronization available |
| `q_HT` | Human text-motion alignment | TMR cosine 与 latent L2 连续梯度 available |
| `q_CT` | Camera text-trajectory alignment | 无 verified scorer，全部 unresolved |

pool 合同固定为：

- `D_AE = q_H ∧ q_C ∧ q_HC`
- `D_H = q_H ∧ q_HT`
- `D_C = q_H ∧ q_C ∧ q_HC ∧ q_CT`
- `D_J = q_H ∧ q_C ∧ q_HC ∧ q_HT ∧ q_CT`

`unresolved` 不是 pass，也不能由其他高分维度补偿。当前唯一可物化的是按已声明 Human 轴构造的 `D_H candidate`；这里的 candidate 仍不等于经过训练因果验证的 clean set。

## 3. 正式分档标准

### 3.1 从 raw score 到 rank/bin

下列是已经物化的 **v1** 规则，只用于解释 v1 counts/artifacts；由于 §3.6 的跨轴污染
与小组尾门不可达，它不再是新 artifact 的正式通用标准。每个 available dimension
独立保存 raw score，并按以下确定性规则转成坏度百分位：

1. 计算全局 midrank bad percentile `p_global`。Physical 当前所有分数均为越高越坏；`q_HT.cosine` 为越低越坏；`q_HT.latent_l2` 为越高越坏。
2. 在对应 stratum 内用同一 tie-aware midrank 计算 `p_stratum`。相同 raw value 得到相同 midrank，不按输入顺序随意拆 tie。
3. 取 `p_eff = max(p_global, p_stratum)`。样本只要在全局或同层内任一视角进入坏尾部，就按更差者处理。
4. 保存十档 `B0…B9`，其中 `Bk` 表示 `k/10 ≤ p_eff < (k+1)/10`；`B9` 覆盖 `[0.9,1.0]`。

Physical rank stratum 为 `capture_source_proxy + duration + dynamics`。duration 固定为 `1–64 / 65–128 / 129–192 / 193+`；dynamics 是 Human root speed、Human articulation velocity、Camera center speed 各自四分位的 `4×4×4=64` 个组合。TMR rank stratum 为 `capture_source_proxy + duration + caption-length`，caption-length 固定为 `1–8 / 9–16 / 17–32 / 33+` tokens。

> [!warning] proxy 边界
> `capture_source_proxy` 当前是拍摄年份代理；action 是 caption 的首个非停用 content token，低频 token 再按固定 hash 汇入 32 个 rare buckets。它们用于 coverage 诊断，不得写成 verified source/action taxonomy。

v2 的 axis-pure stratum 与 deterministic backoff 合同冻结为：

| axis / use | full stratum | backoff chain |
| --- | --- | --- |
| `q_H` | source proxy + Human duration + H-root-speed quartile + H-articulation-velocity quartile | full → source+duration → duration → global |
| `q_C` | source proxy + Camera duration + C-center-speed quartile | full → source+duration → duration → global |
| `q_HC` | 当前只做 length-synchronization hard gate | 保存 H/C duration 与 length delta；不伪造 percentile |
| `q_HT` | source proxy + Human duration + caption length | full → source+duration → duration → global |
| `D_H` coverage | action + Human duration + Human dynamics + language + source | Camera dynamics 只作 metadata，不得进入 ordering |

每个用途选择满足最小样本量的最具体层：rank/bin 与 L2 `p995` 要求 `n≥100`；
quality catastrophe `p9995` 要求 `n≥1000`；coverage catastrophe `p9999`
要求 `n≥5000`；没有合格 conditional group 时只使用 global percentile。每行必须
保存 full key/count、实际 rank key/count/level、catastrophe key/count/level，并让
每个 dimension 分别记录 raw、global percentile、conditional percentile 与最终
`p_eff`。v2 metadata/manifest 必须内嵌 builder SHA、raw/Physical/TMR parent SHA、
exact backoff thresholds 和 `training_authorized=false`；不能只靠本页补 provenance。

### 3.2 status gate 与 no-compensation

当前阈值是 research operating point，不是已冻结的最终阈值：

| dimension role | pass candidate | dimension fail candidate | catastrophe candidate | 是否进入 L2 gate |
| --- | --- | --- | --- | --- |
| Physical `quality_gate` | `p_eff < 0.995` | `0.995 ≤ p_eff < 0.9995` | `p_eff ≥ 0.9995` | 是 |
| Physical `coverage_and_catastrophe` | `p_eff < 0.9999` | 不设普通 fail；保留作 dynamics coverage | `p_eff ≥ 0.9999` | 仅 catastrophe |
| `q_HT.cosine` | `p_eff < 0.995` | `p_eff ≥ 0.995` | 不另设可补偿档 | 是，独立 gate |
| `q_HT.latent_l2` | `p_eff < 0.995` | `p_eff ≥ 0.995` | 不另设可补偿档 | 是，独立 gate |

Human/Camera hard validity 要求 `0 < valid_frames ≤ 300` 且所有已使用 scalar finite。catastrophe 是 any-dimension hard gate：任一 mandatory dimension catastrophic 即失败，其他维度再好也不能抵消。L2 同样要求所有 available `quality_gate` 独立通过；没有单一加权总分。

Physical-only/union 排序按各维 bin 从最坏到次坏做 lexicographic minimization，再比较高坏度维度数量、完整 bin 序列、Pareto rank 与 seeded hash。TMR 的 cosine/L2 独立分档，并另存二维 non-dominated Pareto depth；Pareto depth 用于排序，不替代两个独立 gate。

### 3.3 已计算 Physical 维度与逐维结果

下表计数单位均为 162,760 motions。Physical 的 `dimension fail` 不含同维 catastrophe；同一样本可在多个维度命中，因此各行不得相加推导 unique failures。

| axis | dimension / raw statistic | role | pass | dimension fail | catastrophe |
| --- | --- | --- | ---: | ---: | ---: |
| `q_H` | bone length extreme / relative deviation max | quality gate | 161,431 | 1,248 | 81 |
| `q_H` | bone length variance / relative deviation p95 | quality gate | 161,437 | 1,242 | 81 |
| `q_H` | articulation velocity / angular velocity p95 | coverage + catastrophe | 162,744 | — | 16 |
| `q_H` | articulation acceleration / angular acceleration p95 | quality gate | 161,433 | 1,246 | 81 |
| `q_H` | root speed p95 | coverage + catastrophe | 162,744 | — | 16 |
| `q_H` | root acceleration p95 | quality gate | 161,429 | 1,250 | 81 |
| `q_H` | root jerk p95 | quality gate | 161,430 | 1,249 | 81 |
| `q_H` | yaw velocity p95 | coverage + catastrophe | 162,744 | — | 16 |
| `q_H` | yaw acceleration p95 | quality gate | 161,481 | 1,197 | 82 |
| `q_C` | center speed p95 | coverage + catastrophe | 162,744 | — | 16 |
| `q_C` | center acceleration p95 | quality gate | 161,396 | 1,283 | 81 |
| `q_C` | center jerk p95 | quality gate | 161,391 | 1,288 | 81 |
| `q_C` | rotation angular speed p95 | coverage + catastrophe | 162,744 | — | 16 |
| `q_C` | rotation angular acceleration p95 | quality gate | 161,467 | 1,212 | 81 |
| `q_C` | rotation orthogonality Frobenius max | quality gate | 161,608 | 1,070 | 82 |
| `q_C` | rotation determinant absolute error max | quality gate | 161,632 | 1,046 | 82 |

hard-valid 检查中 Human 与 Camera 均为 `162,760` pass、`0` invalid；这只说明 length/finite 输入有效，不代表其他质量轴通过。

### 3.4 TMR 与 H-C 结果

| axis / dimension | 方向与独立 gate | pass | fail |
| --- | --- | ---: | ---: |
| `q_HT.cosine` | low is bad；`p_eff < 0.995` | 161,845 | 915 |
| `q_HT.latent_l2` | high is bad；`p_eff < 0.995` | 161,869 | 891 |
| `q_HT` 两维联合 | 两维都必须 pass；不做加权补偿 | 161,446 | 1,314 |
| `q_HC.valid_length_synchronization` | Human/Camera length delta 必须为 0 | 162,759 | 1 |

TMR 同时保存 cosine/L2 的 raw value、global/stratum percentile、bin，以及二维 Pareto depth。`1,314` 是两类 fail 的去重并集；`915 + 891` 不能直接当 unique count。

### 3.5 unresolved 维度

| axis | unresolved dimensions | 原因与处理 |
| --- | --- | --- |
| `q_H` | articulation position/jerk；root path；yaw jerk | completed Physical-v2 未导出；`unresolved_not_pass` |
| `q_H` | foot contact/skating；ground penetration | 无 calibrated contact state/ground plane；不得用现有 foot position 冒充 pass |
| `q_C` | center path；rotation angular jerk/discontinuity | completed score 未导出或无 verified event field |
| `q_HC` | projection validity；geometric Out；screen center；shot scale；frame margin | Physical-v2 未读取/导出，但 raw parent 与 verified fast replica 有 trajectory/intrinsics，可复用 official projection；occlusion/true visibility 仍不可用 |
| `q_CT` | Camera caption ↔ trajectory 全部语义维度 | 无 verified Camera text-trajectory scorer |

Physical-v2 的 per-sample JSONL 只有聚合 `p50/p95/max`，不能反演 yaw/articulation
jerk、root/Camera path 或 SO(3) angular jerk。补这些量必须从原始
`smpl_rifke/traj/intrinsics` 时序重新导出一个独立 immutable Physical-v3 score
artifact，但不需要重新训练 scorer。rotation max-step 可由已有 max rate 构造 proxy，
仍不能冒充经阈值校准的 discontinuity event。q_HC projection 可复用
`storymotion/eval/screen_projection.py`；在没有 occlusion/visibility mask 时只能叫
geometric in-frame/out-of-frame，不能叫 true visibility。

### 3.6 v1 task-purity 复核与 v2 blocker

v1 builder 在 `q_H` 与 `q_C` 的 `p_stratum` 中共用了
`source + duration + dynamics`，其中 dynamics 是 Human root speed、Human
articulation velocity 与 Camera center speed 的联合 `4×4×4` strata。由于
`p_eff=max(p_global,p_stratum)`，Camera center dynamics 会改变 `q_H` rank，
进而影响 `D_H` 的 Physical-only/union/Pareto+coverage ordering。它不改变 raw
score、global rank 或已发布 artifacts 的 provenance，但违反“每个 q axis 独立
no-compensation”的任务纯度。

只读敏感性复算只移除跨轴变量、保持原 score 与 dynamics 定义时，`q_H` L2 membership
改变 `2,777`、catastrophe membership 改变 `67`；`q_C` L2 改变 `2,028`、
catastrophe 改变 `279`。因此这是实际 gate/subset membership 变化，不能靠重命名 v1
来修复。

v1 另有 `2,090` 个 Physical strata，中位 `n=46`，共 `52,218` 个样本处于
`n<100` 的组。midrank 下 `p995/p9995/p9999` 分别至少需要
`n=100/1000/5000` 才可能命中；大量 v1 conditional tail gate 因而数学上不可达。
v2 必须使用 §3.1 的用途特定 min-n/backoff，并逐行记录采用层级和 group size。

v2 必须：

- `q_H` strata 只使用 Human duration/dynamics；
- `q_C` strata 只使用 Camera duration/dynamics；
- `q_HC` 才允许联合 H/C geometry strata；
- Camera dynamics 可保留为 `D_H` coverage metadata，但不得进入 `q_H` gate/rank；
- `D_H` Pareto+coverage 不得包含 joint Camera dynamics；
- 按用途采用固定 min-n/backoff，禁止小组静默退化为“永远 pass”；
- 所有 v2 outputs 写入新 immutable root，v1 不原地补写、不删除。

此外，year 只是 source proxy，caption 首个 content token 只是 action proxy；相对坏尾
percentile 表示“稀有/异常候选”，不自动等于物理错误。高转向、长时长与高动态样本应
优先作为 coverage strata，不能因为稀有就被 quarantine。

## 4. L0–L4 分层结果与 pool eligibility

### 4.1 质量层结果

| level | 数量 | 精确定义 |
| --- | ---: | --- |
| L0 raw immutable | 162,760 | 全量 ordered motions |
| L1 hard-valid + `q_H` catastrophe pass | 162,405 | 355 个 unique `q_H` catastrophe candidates 被挡在 L1 外 |
| L2 Human modality quality pass | 156,888 | L1 内再有 5,517 个 unique dimension-wise fail；所有 available mandatory `q_H` gates 必须通过 |
| L3 `D_H candidate` | 155,647 | L2 且 `q_HT.cosine`、`q_HT.latent_l2` 分别通过 |
| L4 nested research subsets | 8K/16K/32K/64K | 五类 deterministic nested controls；不是新的 pass gate，也不授权训练 |

`q_C` 的 available dimensions 有 158,225 pass、4,535 fail，其中 294 个命中任一 `q_C` catastrophe；由于还有 unresolved Camera 维度，这些计数只能用于 partial feasibility。

### 4.2 数据池结果

| pool | 当前数量 | 状态 | 缺口 |
| --- | ---: | --- | --- |
| `D_AE` | 153,055 | partial eligibility | `q_C` 与完整 `q_HC` 未闭合 |
| `D_H` | 155,647 | candidate research universe | 当前 Human 轴可物化；threshold 尚未经 matched training 验证 |
| `D_C` | 153,055 | partial eligibility | 在 `D_AE` 缺口外还缺 `q_CT`；当前数字不是真实 `D_C` 基数 |
| `D_J` | 151,858 | partial eligibility | 还缺完整 Camera/framing/semantic axes；当前数字不是真实 `D_J` 基数 |

`D_AE / D_C / D_J` 的数字只回答“已计算轴下最多还剩多少”，不得当作 clean pool、训练 manifest 或完成率。

## 5. L4 nested volume controls

固定 seed 为 `170722`。每个 control 的 selection order 只生成一次，`8K / 16K / 32K / 64K` 都是该 order 的前缀，因此逐项验证 `8K ⊂ 16K ⊂ 32K ⊂ 64K`。最终 tie 由 `SHA256(seed, motion_id)` 后接原始 order index 确定。

| control | universe | selection rule |
| --- | --- | --- |
| random | L1，162,405 | seeded SHA order |
| Physical-only | L1，162,405 | 仅按 `q_H` 最坏维优先的 lexicographic rank；无 weighted sum |
| TMR-only | L1，162,405 | cosine/L2 独立 bins，再用二维 Pareto depth 与 seeded tie |
| union | `D_H candidate`，155,647 | 先排除任一 `q_H/q_HT` gate fail，再对全部 Human 质量轴做 lexicographic order |
| Pareto+coverage | `D_H candidate`，155,647 | 从 union quality order 出发，确定性调度 duration/source/dynamics/language/action 的边际覆盖 |

random、Physical-only、TMR-only 是隔离诊断，因此允许包含非 `D_H` candidate；union 与 Pareto+coverage 的每个 member 都属于 `D_H candidate`。

### 5.1 四档实际结果

所有格子都达到目标 unique motions，role rows 与 Direct-H task conditions 均等于目标 size，duplicate rows 为 0；由于 Camera 轴未闭合，Direct-C conditions 与 joint conditions 均明确为 0。

| control | 8K 中 `D_H` members | 16K 中 `D_H` members | 32K 中 `D_H` members | 64K 中 `D_H` members |
| --- | ---: | ---: | ---: | ---: |
| random | 7,671 | 15,362 | 30,722 | 61,418 |
| Physical-only | 7,981 | 15,956 | 31,890 | 63,656 |
| TMR-only | 7,831 | 15,606 | 31,144 | 62,261 |
| union | 8,000 | 16,000 | 32,000 | 64,000 |
| Pareto+coverage | 8,000 | 16,000 | 32,000 | 64,000 |

这张表是 membership audit，不是模型效果排名。Physical-only/TMR-only 较 random 的 membership enrichment 不能替代后续 matched continuation。

### 5.2 64K coverage audit

下表为“subset 覆盖 strata 数 / 对应 control universe strata 数”。完整每档 counts 与最大分布偏差保存在各自 `.meta.json`。

| control | duration | source proxy | dynamics | language | action-token proxy |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 4/4 | 9/9 | 64/64 | 9/10 | 89/89 |
| Physical-only | 4/4 | 9/9 | 64/64 | 10/10 | 89/89 |
| TMR-only | 4/4 | 9/9 | 64/64 | 8/10 | 89/89 |
| union | 4/4 | 9/9 | 64/64 | 10/10 | 89/89 |
| Pareto+coverage | 4/4 | 9/9 | 64/64 | 10/10 | 89/89 |

Pareto+coverage 的含义是 deterministic coverage-aware order，不是说所有 strata 被强制成等比例，也不是 quality 与 coverage 的加权总分。

## 6. 历史 binary lattice provenance

> [!warning] 已被正式分档取代
> 以下 artifacts 不删除、不回写。它们只把旧 candidate threshold 转成 binary exclusion，没有全量连续向量、dimension-wise no-compensation、Pareto rank、固定体量或 coverage constraint，不能称为“清洗完成”。

旧 Physical 规则在 length mismatch、bone extreme，或至少两个 dynamics families 进入 tail 且其中至少一个进入 extreme 时触发；旧 TMR 规则要求 low cosine 与 high latent-L2 同时触发。三档 operating point 与 candidate 数如下：

| branch | broad / loose | proposed | catastrophe / strict |
| --- | ---: | ---: | ---: |
| Physical total | 427 | 362 | 128 |
| Human-physical | 426 | 361 | 127 |
| H-C length relation | 1 | 1 | 1 |
| TMR | 991 | 450 | 87 |

Physical 的 loose/proposed/strict tail/extreme 分别为 `p99/p99.9`、`p99.5/p99.9`、`p99.9/p99.95`；TMR 三档分别使用 `p99`、`p99.5`、`p99.9` 的联合坏尾。它们是历史阈值，不应与新合同的 `p_eff` dimension gates 混用。

| historical level | Direct-H | Direct-C | joint |
| --- | ---: | ---: | ---: |
| broad exclusion | 161,344 | 162,333 | 161,343 |
| proposed | 161,949 | 162,398 | 161,948 |
| catastrophe only | 162,546 | 162,632 | 162,545 |

对应只读目录：

- `curation_manifests/v8_2333_quality_lattice_broad_exclusion_20260722/`
- `curation_manifests/v8_2333_quality_lattice_proposed_20260722/`
- `curation_manifests/v8_2333_quality_lattice_catastrophe_only_20260722/`

早期 task-aware candidate v1 也只保留 provenance：`sft_candidates/task_aware_sft_candidate_v1_20260722/`。它的 proposed/proposed eligibility 为 Direct-H `161,948` motions、Direct-C `162,398` motions/`163,022` Camera conditions、joint `161,948` motions/`162,560` Human×Camera conditions，仍未获训练授权。

## 7. 训练分配合同

### 7.1 任务到 pool

| training target | 所需 pool | 当前是否可训练 |
| --- | --- | --- |
| Stage1 joint AE | `D_AE`；Human/Camera/geometry losses 还应按各自 available quality mask 分开 | 否；`q_C/q_HC` 未闭合 |
| Stage2 Direct-H | `D_H` | 否；只有 research candidate，threshold 未验证 |
| Stage2 Direct-C | `D_C`；Human TMR 不得作为 Camera target filter | 否；`q_C/q_HC/q_CT` 未闭合 |
| Stage2 joint parallel | `D_J` | 否；Camera/framing/semantic axes 未闭合 |

Stage1 representation、Stage2 condition exposure 与数据质量是三条独立因果轴。未来 curation ablation 必须冻结 C3-25 representation、owning decoder、cache builder、Unified implementation、task probabilities、optimizer、LR、sampler、eval IDs 与 seed；不能同时修改 Stage1/backbone 来解释数据效果。

### 7.2 获得授权后的 matched controls

每个 `8K / 16K / 32K / 64K` 规模必须同时运行 random、Physical-only、TMR-only、union、Pareto+coverage，主比较固定 optimizer steps/sample exposures，而不是按 epoch 对齐。每个 run 记录 unique motion exposure、role/task-condition exposure、重复率与 coverage。

小池另设 raw replay `90/10` 与 `80/20` controls，防止 diversity、语言覆盖、长序列和高动态长尾坍缩。评估必须同时覆盖 Direct-H、Direct-C、joint parallel 的 semantic/distribution/coverage、F1、Out、paired geometry、no-reference physical 与 diversity；质量分上升但 entropy、duration 或 dynamics range 坍缩不算有效收益。

任何训练都需要新的 immutable run contract 显式写入 `training_authorized=true`。不得修改本轮只读 manifests 来追授权限。

### 7.3 分层重训 curriculum 候选

以下只预注册阶段分工，不授权训练，也不替代 `8K/16K/32K/64K` matched matrix。

1. **quality relevance audit。** 在训练前先检验各 q dimension/bin 是否预测
   Stage1 owning-decoder floor、Stage2 `t=799` excess 与 full-sampling failure。
   duration/source/dynamics 必须配平，避免把“稀有动作”误判成“坏动作”。
2. **只有 `D_H` ready 时。** 最多做 Direct-H curation research ablation；
   Direct-C/joint 仍从 raw sampler 取样，C3-25 representation、task probability
   `1:1:1`、optimizer 与总 exposure 不变。不得命名为 clean Unified SFT。
3. **Stage1 只有 `D_AE` 闭合后。** Human reconstruction loss 用 `q_H` ownership，
   Camera loss 用 `q_C`，relative/framing loss 用 `q_H∧q_C∧q_HC`。候选课程是
   `60% L1 broad → 30% 50:50 L1 replay/D_AE-Pareto64K → 10% 20:80 replay/D_AE`，
   并保留 matched raw/random 与双 seed；比例必须先短 pilot，不能写成既定最优值。
4. **Stage2 全部轴闭合后。** Direct-H←`D_H`、Direct-C←`D_C`、joint←`D_J`，
   每个 task 内独立执行 broad→selected+replay；全局 task probability 保持
   `1:1:1`，固定 optimizer steps 与 branch sample exposure。Human TMR 不能过滤
   Direct-C target。
5. **volume 与 replay。** 先用 64K 做低预算 feasibility 只允许决定是否值得跑完整
   matrix；正式体量结论仍需五类 controls × 四档 sizes × replay controls。

heading coverage 另存为 duration、net yaw、cumulative `abs(yaw)`、turn count、
yaw speed/acceleration/jerk 与 root-path curvature。straight 与 high-turn 是 coverage
bins，不是质量优劣标签；不得通过裁掉长序列或高转向来制造更低平均误差。

### 7.4 augmentation 的启动判据

数据增广不是当前数据缺口的替代品。只有以下条件同时满足才进入独立 contract：

1. 已用 Stage1 floor、decoded oracle、padding-invariance 排除实现/decoder 主因；
2. sealed long/high-turn 或稀缺语义 strata 仍显著失败；
3. size curve 显示增加有效样本有收益，或小 clean subset 因重复而过拟合且 raw replay
   不能恢复；
4. 外部/合成样本通过相应 q axis、representation compatibility 与 source-heldout
   gate。

首选的是对同一 Human-Camera pair 施加联合 SE(2) yaw/translation 变换，以保持相对
几何并直接检验 heading equivariance；必须同步变换 Human root、Camera pose 与所有
几何 evaluator inputs。mirror、time-reverse、time-scale 会改变左右、动作方向或文本
语义，不得 naive 使用。

HumanML3D fixed-camera 目前只能视为潜在 Direct-H 外部源：现有 8 个 test clips 的
joints round-trip 可通过，但其 Pulp normalized pose `max|z|≈102.8` 明显 OOD；
synthetic fixed/follow camera 也不是真实 `q_C/q_HC/q_CT`。未来只有在 train-only
retarget、`q_H/q_HT`、Stage1 recon/latent-distribution gates 通过后，才能做
`0/5/10/20%` fixed-exposure、source-heldout Direct-H dose screen；不得用于当前
Stage1 joint、Direct-C 或 joint training。

## 8. Immutable artifact registry

canonical complete evidence 在 5090：
`runs/data_curation/storymotion_v8_2333_data_curation_20260717/`。4090 的同名
curation root 当前不是完整冗余，不能用来声称双机 artifact equality。

| artifact | records / role | SHA256 |
| --- | --- | --- |
| immutable raw | 162,760 motions | `49d53029c42ad6ee275172fd9d3e5d56e98f1142ae9daf5dcc0988faa2a9c458` |
| Physical-v2 scores | 162,760 | `ffd3f6639cd50d8992388e0d6092d5bd6ec77060932ce21c9ae2f9c43db09b76` |
| Physical-v2 scorer | code | `b274773a34604ac79c5387d6b637df353bd22bf05820611508f7a7a41be2b960` |
| Human TMR-v4 scores | 162,760 | `766e4522ab6a34f0c34b59635e20ae295a6ff06dcd8a9fd78084103292d8a4b0` |
| Human TMR-v4 scorer | code | `526b7807f439f6f605a2a32ac90c891120873305bf3c6af8be619d99c0d85e99` |
| quality-gradient builder | externally retained code snapshot；v1 metadata 未内嵌此 SHA | `f8d3d1a9cf62fd769783747184c5e6f288af77d6869b4739623de1671b61cb11` |
| curation dispatcher | code at materialization | `cfa11413b091367a5105c375870dbfbbfe2c31fbdbe3c1e1b7566f61408fe064` |
| `quality_table.jsonl` | 162,760 rows；1,852,807,932 bytes | `13c1f28b7c2c359b06ab7c6b0ff4762e56ab8d56052cb19cc51c705342bd9d81` |
| `metadata.json` | thresholds/counts/scorers/unresolved | `7aab0aadaa5b3c076e8e70400fbc3ebf35a5f1d53d6e8a8041a031b425e10f1d` |
| `manifest.json` | 全部 nested JSONL/meta/ordered-ID hashes | `18247d4e39da6cc4d4c8809f92d455a225f756d0004d50a675670aa2151cad60` |

quality-gradient root：`quality_gradients/v8_2333_full_quality_gradients_nested_v1_20260722/`。20 个 subset JSONL 已通过行数、零重复与 nested-prefix 外部复核；全部输出为只读 `0444`。v1 builder SHA 只在外部 registry 中重建，未被 v1 metadata 自证；v2 必须修复。现有 artifact 不因该 provenance 缺口而被补写。本轮没有覆盖任何历史 run/artifact，也没有重新训练 scorer。

## 9. 下一 gate

1. **Axis-purity v2。** 新建 sibling builder，先只读 dry-run counts/change matrix；
   冻结 §3.1 backoff 与 schema 后，才在新 immutable root 重建 ranks/pools。不得修改
   v1 code/artifact，也不得同时加入新 Physical 维度。
2. **Physical-v3 enrichment。** 从 raw 时序独立导出 Human yaw/articulation jerk、
   root path/curvature、Camera center path 与 SO(3) angular jerk/discontinuity；
   绑定 fast-replica/source content manifest，不与 axis-purity 修复混成一个 causal
   change。
3. **q_HC projection。** 复用 verified trajectory/intrinsics 与 official projection，
   闭合 projection validity、geometric Out、center、scale、margin；visibility/occlusion
   继续标 unresolved。
4. 建立并验证 `q_CT` Camera text-trajectory scorer；不能借用 Human TMR 代替。
5. 先做 q-stratified no-update relevance audit，再生成五类 nested controls；不得原地
   补写 v1 artifact。
6. 预注册固定 C3-25、固定 exposure 的 matched curation ablation，验证 operating
   point、volume 与 replay。
7. 只有完整质量轴和 matched ablation 同时支持后，才冻结 threshold、生成正式可逆
   quarantine/clean manifest，并单独授权训练。

Axis-purity、Physical-v3 与 q_HC 都是短 CPU/SSD 作业，但新 immutable root 不可补写。
在 schema/code review 完成前不 materialize；代码冻结后也优先避开 105K checkpoint
I/O 时段，以低优先级运行。v2 未生成前本页不登记虚构 counts/hash。

HumanML3D fixed-camera augmentation 是“创造新 pair”的独立数据增广轴，不属于本清洗合同；其启动条件见 §7.4。

---
title: "StoryMotion Task-aware SFT Data Preparation"
status: candidate_builder_ready_no_training_authorization
tags:
  - StoryMotion
  - stage2
  - data-curation
  - sft
  - status/active
aliases:
  - StoryMotion-SFT-Data-Prepare
source_notes:
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[current]]"
created: 2026-07-22T14:30:00+08:00
updated: 2026-07-22T14:30:00+08:00
---

# StoryMotion Task-aware SFT Data Preparation

> [!abstract] 判断
> 从完整 PulpMotion 中筛高质量数据再续训是合理方向，但更准确的名称是 **high-quality continuation / annealing**。固定 32K、双分数硬求交、直接删除、依赖人工标注，以及把 Human/Camera role rows 当同一种 pair 的部分不执行。先落实可逆 task-aware eligibility，再补 Camera semantic 与覆盖特征，最后决定 8K/16K/32K/64K。

## 1. 接受与拒绝

接受：

- 高质量阶段可以复用预训练见过的 motion。
- 固定 optimizer steps/sample exposures，避免把子集大小与计算量混淆。
- 保留 random、Physical-only、TMR-only、union 与 Pareto+coverage controls。
- 小集合需要 raw replay control，防止 diversity 与长尾覆盖坍缩。
- 同时报告质量、覆盖、长度、速度、稀有动作与语言属性分布。

不直接执行：

- 不把 `32K / 20%` 当成先验最优。
- 不用 Human TMR 与 Physical 的加权和定义全系统质量。
- 不把双高硬交集作为唯一 SFT 集。
- 不伪造尚不存在的 Camera semantic、fine-align、rarity/complexity 分数。
- 不删除 raw 数据；输出必须 immutable、可逆。
- 本阶段不引入人工标签。

## 2. Task-aware 单位

基础是 162,760 joint motion records；326,144 是 162,760 Human role rows 与 163,384 Camera role rows 之和。

| task | target / condition | 自动清洗作用域 |
| --- | --- | --- |
| Direct-H | Human text → Human | clip Physical + Human TMR |
| Direct-C | observed Human + Camera text → Camera | clip Physical；Human TMR 不适用；Camera semantic unresolved |
| joint | Human text + Camera text → Human + Camera | clip Physical + Human TMR；Camera semantic unresolved |

proposed/proposed 预期得到 Direct-H `161948`、Direct-C `162398`、joint `161948` 个 eligible joint clips。`324970` 只是 retained role rows 的审计和。

## 3. S0：Task-aware candidate

实现：`scripts/storymotion_sft_task_aware_manifest.py`。

输入：immutable raw、Physical `proposed_p995_x999`、Human TMR `proposed_p995`。

输出目录：`runs/data_curation/storymotion_v8_2333_data_curation_20260717/sft_candidates/task_aware_sft_candidate_v1_20260722/`。

输出 `eligibility.jsonl`、`direct_h.jsonl`、`direct_c.jsonl`、`joint.jsonl`、`metadata.json` 与 `manifest.json`。状态只能是 `complete_candidate_only_not_training_authorized`；Camera 记录必须保留 `camera_semantic_status=unresolved_no_verified_scorer`。

## 4. S1：Pareto + coverage，暂不物化

生成 nested `8K / 16K / 32K / 64K` 前必须具备：Human TMR、分解 Physical、Camera semantic、duration/source/dynamics/caption coverage、可验证语言复杂度与 train-only rarity。

选择规则：

1. catastrophe candidate 只做可逆 exclusion mask。
2. 其余样本做多维 Pareto rank，不允许极差维度被另一维抵消。
3. 在 duration/source/dynamics/language strata 内 deterministic sampling。
4. 四个规模必须 nested，固定 seed 与 parent hash。
5. 同规模提供 random、Physical-only、TMR-only、union、Pareto+coverage controls。

Camera semantic 缺失时，只能构造 Human-only research screen，不得命名为 Unified/joint SFT dataset。

## 5. S2：Matched continuation

固定 C3-25 representation、owning decoder、cache builder、Unified implementation、seed、task probabilities、optimizer、LR、steps/exposures、sampler 与 eval IDs。

| arm | 数据策略 |
| --- | --- |
| raw continuation | 原始 task sampler |
| random-size control | 与候选集同规模随机采样 |
| task-aware candidate | S0 task-specific eligibility |
| Pareto+coverage | S1 nested subset |
| Pareto+coverage + raw replay | 90/10 与 80/20 |

主比较固定 optimizer steps，并报告 unique condition exposure、重复率与 task exposure；不能按相同 epoch 比较不同规模。

评估统一报告 Direct-H、Direct-C、joint parallel 的 semantic/distribution/coverage、F1、Out、paired geometry、no-reference physical、diversity、长尾/长序列/高动态/组合文本 coverage。指标上升若伴随 entropy、长度或动态范围坍缩，不算有效收益。

## 6. 当前边界

允许物化并审计 S0 candidate、设计 Camera semantic/coverage，以及做不训练的 subset feasibility。

禁止冻结 proposed threshold、直接启动 32K SFT、用 Human TMR 过滤 Direct-C、在 Camera semantic 缺失时声称 joint 已清洗、同时修改 Stage1/backbone/sampler，或不可逆删除 raw。


## 实施结果：task-aware candidate v1（2026-07-22）

判断结论：高质量 continuation、固定 exposure、matched control、Pareto+coverage 与 replay 原则合理；固定写死 `32K`、破坏性删除、伪造不可用特征、用 Human TMR 过滤 Direct-C Camera target，以及当前阶段引入人工标注均不合理。实现因此只生成候选清单，不授予训练权限。

| task | eligible unit | 数量 | 当前限制 |
| --- | --- | ---: | --- |
| Direct-H | motion/Human row | 161,948 | proposed Physical + TMR exclusion |
| Direct-C | motion | 162,398 | 不施加 Human-TMR target filter |
| Direct-C | Camera-condition row | 163,022 | 多 Camera captions 展开 |
| joint | motion | 161,948 | Physical/TMR motion-level union |
| joint | Human×Camera combination | 162,560 | 多 Camera captions 展开 |

原始基数为 `162,760` joint motions、`162,760` Human rows、`163,384` Camera rows。`326,144` 仅是两个 caption roles 的行数之和，不是 joint pair 数。当前候选为 Physical `362` motions、TMR `450` Human rows，人工标签数为 `0`。

状态：

- `complete_candidate_only_not_training_authorized`
- Camera semantic scorer：unresolved
- LaMP：unresolved
- threshold/coverage gate：not frozen
- artifact：`runs/data_curation/storymotion_v8_2333_data_curation_20260717/sft_candidates/task_aware_sft_candidate_v1_20260722/`
- builder commit：`aed514788f3e8bc6ad76193b105baa4a8c714399`

输出哈希：

| 文件 | SHA256 |
| --- | --- |
| `eligibility.jsonl` | `9de1264495ec70a36efdc4e9628e45cbe5bd6eb42a77b3a05084c8b4d1ac853f` |
| `direct_h.jsonl` | `ac855a7228efc49724c1efe98209ab09429879874957c1261ad987bda563f375` |
| `direct_c.jsonl` | `bcf89f9a6528dad7615ce9808ce2a86e63e9f990635cc196ed2e3ec15edf80cb` |
| `joint.jsonl` | `cce4f29392c0d9caf13e8dcfd67b5d3bb6ee8093ae7341177a877b0c604fcce1` |

下一步不是直接 SFT。必须先闭合 Camera semantic/人物-镜头匹配度自动 scorer，并冻结多阈值下的 retained coverage；之后再从候选池预注册固定 exposure 的 clean-control 与 SFT arm。

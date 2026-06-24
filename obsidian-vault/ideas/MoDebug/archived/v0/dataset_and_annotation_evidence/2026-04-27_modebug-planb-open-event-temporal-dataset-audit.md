---
created: 2026-04-27T20:55
updated: 2026-04-27T20:55
title: MoDebug Plan B：Open Event / Temporal Annotation Dataset Audit
status: archived
tags:
  - MoDebug
  - plan-b
  - dataset-audit
  - event-level
  - temporal-annotation
  - motion-generation
source_papers:
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing|FineMotion]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_FineMoGen_Fine_Grained_Spatio_Temporal_Motion_Generation_and_Editing|FineMoGen]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2025/2025_TM_Mamba_Text_Controlled_Motion_Mamba_Text_Instructed_Temporal_Grounding|TM-Mamba]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]"
  - "[[paperAnalysis/Motion_Generation/ECCV_2024/2024_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models|ChroAccRet]]"
related_notes:
  - "[[2026-04-27_modebug-planb-ordering-omission-manifest]]"
  - "[[2026-04-27_modebug-planb-finemotion-weak-supervision-audit]]"
  - "[[2026-04-27_modebug-planb-hard-negative-seed-pool]]"
---

# MoDebug Plan B：Open Event / Temporal Annotation Dataset Audit

## 0. 结论先行

如果“event 划分数据集”严格指：

- `prompt -> ordered event list`
- 可直接服务 `R_pres / R_ord / R_dur`
- 语义单元接近 `HumanML3D-E`

那么当前 KB 里**没有第二个和 `HumanML3D-E` 同型、且已明确开放的替代 benchmark**。

如果把范围放宽到：

- snippet-level temporal annotation
- frame-level action plan
- part-level temporally-aware annotation

那么当前 KB 里确实还有几条相关线，但它们多数**不是 sequence-level ordered event list**，更适合作 sidecar 或 future expansion，而不是直接替换 `HumanML3D-E`。

## 1. 审计口径

本次只把工作算作“正样本”，当且仅当满足以下至少一项：

1. 论文/KB 明确说自己构建了新的 temporal / event annotation asset
2. 官方 repo / dataset page 给出可下载的 annotation 入口
3. 当前本机 workspace 已能看到对应 annotation 文件

同时明确区分三层：

1. **same-shape event benchmark**
   - 最像 `HumanML3D-E`
   - 关注 ordered events
2. **open temporal annotation asset**
   - 有时序片段/部位/帧级标注
   - 但 schema 不一定是 ordered event list
3. **method-only / probe-only**
   - 用到了 temporal semantics
   - 但没有释放成可复用的数据资产

## 2. 统计结论

下面统计默认**不把 Event-T2M / HumanML3D-E 本身算进“其他工作”**。

| Bucket | Count |
| --- | ---: |
| 额外检查的候选工作 | 6 |
| 额外的 same-shape ordered-event dataset | 0 |
| 确认有开放 temporal annotation asset | 3 |
| 仅 partial open asset | 1 |
| benchmark 提出但未确认开放数据 | 1 |
| method/probe 但不是 dataset release | 1 |

对应关系：

- confirmed open temporal annotation asset:
  - FineMotion
  - FineMoGen / HuMMan-MoGen
  - FrankenMotion / Frankenstein Dataset
- partial open asset:
  - ActionPlan
- benchmark proposed but release unclear:
  - TM-Mamba / BABEL-Grounding
- method/probe only:
  - ChroAccRet

## 3. Anchor：当前主参考仍是 HumanML3D-E

参考笔记：[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]

当前最重要的结论不变：

- `HumanML3D-E` 仍然是当前最像 Plan B 主任务的数据源
- 它是 `prompt -> ordered events` 的 clean event decomposition cache
- 本机已落地：
  - `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_train.json`
  - `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_val.json`
  - `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_test.json`
  - `linkedCodebases/datasets/HumanML3D-E/data_test_condition2.npy`
  - `linkedCodebases/datasets/HumanML3D-E/data_test_condition3.npy`
  - `linkedCodebases/datasets/HumanML3D-E/data_test_condition4.npy`

当前本机 cache 统计：

- test prompt entries: `12515`
- test split median events per prompt: `2`
- p90 events: `3`
- max events: `10`

一句话：**如果要直接做 `R_pres / R_ord / R_dur`，`HumanML3D-E` 仍然没有被别的 open asset 正面替代。**

## 4. 其他候选工作逐项判断

下表只列 “其他工作”。

| Work | Asset | 粒度 | 开源情况 | 本机状态 | 对 Plan B 的结论 |
| --- | --- | --- | --- | --- | --- |
| FineMotion | BPMSD / BPMP | 0.5s snippet + paragraph + body-part | confirmed open | local ready | 最强 sidecar，但不是 ordered event list |
| FineMoGen | HuMMan-MoGen | stage-level + body-part | confirmed open | local absent | 历史前驱，可参考，不适合直接替代 HumanML3D-E |
| FrankenMotion | Frankenstein Dataset | part-level + action-level + sequence-level + temporal boundaries | confirmed open | local absent | 很强的 future expansion 候选，但 part-centric 且依赖 AMASS |
| ActionPlan | humanml3d_actionplan_merged | frame-level action-plan asset | partial open | local partial ready | 可做 sidecar，不是 clean event benchmark |
| TM-Mamba | BABEL-Grounding | text-span temporal grounding | release unclear | local absent | 不算 confirmed open dataset |
| ChroAccRet | CAR negatives | shuffled temporal negatives | method-only | local absent | 不算 dataset release |

## 5. 逐项证据

### 5.1 FineMotion

参考笔记：[[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing|FineMotion]]

为什么算 positive：

- KB 明确写它是 `dataset and benchmark`
- 官方 repo 明确开放 FineMotion 文本描述资产
- 本机已经有可直接读取的 json

官方 release 口径：

- 官方 README 说明：
  - motion sequences 仍来自 `HumanML3D`
  - FineMotion 自己开放的是 fine-grained textual descriptions
- release 形式本质上是**annotation-layer release**，不是把原始 motion 一起打包重发

当前本机已落地：

- `linkedCodebases/datasets/FineMotion/BPMSD_auto.json`
- `linkedCodebases/datasets/FineMotion/BPMSD_human.json`
- `linkedCodebases/datasets/FineMotion/BPMP_auto.json`
- `linkedCodebases/datasets/FineMotion/BPMP_human.json`

当前本机 quick stats：

- `BPMSD_auto.json`: `29230` sequences
- `BPMSD_human.json`: `1500` sequences
- `BPMP_auto.json`: `29226` sequences
- `BPMP_human.json`: `1500` sequences
- snippet 粒度上，median snippets per sequence = `15`
- median non-empty snippets per sequence = `12`

需要特别注意的一点：

- `linkedCodebases/FineMotion_release/README.md` 里对 human annotations 仍写着 `Coming Soon`
- 但当前本机 mirror 已经有 `BPMSD_human.json` / `BPMP_human.json`
- 所以对我们来说，它已经不是 “paper-only”，而是**本机可读 sidecar asset**

对 Plan B 的判断：

- 它最适合做 `R_pres` sidecar、body-part weak supervision、local evidence text
- 但它不是 `prompt -> ordered events`
- 所以不能当 `HumanML3D-E` 替代品，只能当 sidecar

### 5.2 FineMoGen / HuMMan-MoGen

参考笔记：[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_FineMoGen_Fine_Grained_Spatio_Temporal_Motion_Generation_and_Editing|FineMoGen]]

为什么算 positive：

- KB 明确记了它贡献 `HuMMan-MoGen`
- note 中给出数据规模：`2968 videos`、`102,336 annotations`
- 官方 GitHub 公开了代码，并要求从 Google Drive 下载数据文件

但为什么不把它当主替代：

- 它的 schema 是 `body-part x action stage`
- 监督方式比 `HumanML3D-E` 更重
- 更像 fine-grained control benchmark，而不是 event-level reward benchmark

当前状态判断：

- official code: yes
- official data bundle: yes
- standalone local mirror in current workspace: no

对 Plan B 的判断：

- 它是 `FineMotion` 之前的重要前驱
- 但更适合作为“历史来源 + schema 对比”，不适合作当前主数据源

### 5.3 FrankenMotion / Frankenstein Dataset

参考笔记：[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]

为什么算 positive：

- 官方 project page 和 code repo 都明确给出 dataset 入口
- 官方 repo 明确写：
  - `The Frankenstein Dataset is now available on HuggingFace`
  - annotation 下载方式为 `git clone` 或 `snapshot_download`
- 它显式开放的是 annotation dataset，底层 motion 需要用户自行下载 `AMASS`

当前官方口径：

- dataset size: `10978` motion sequences
- annotation granularity:
  - sequence-level
  - action-level
  - part-level
  - temporal boundaries
- 7 个 body parts 独立文本描述

关键限制：

- `AMASS` motion data cannot be redistributed
- 所以它和 FineMotion 一样，本质也是 **annotation-layer open, base motion separate**

当前状态判断：

- official code: yes
- official annotation dataset: yes
- local mirror in current workspace: no

对 Plan B 的判断：

- 这是一个很值得后续扩展的候选
- 但它是 **part-centric hierarchical annotation**
- 和 `HumanML3D-E` 的 ordered event list 不是同型

### 5.4 ActionPlan

参考笔记：[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]

为什么只算 partial：

- 官方 repo 已公开
- 官方 README 明确：
  - `Inference Code`: released
  - `Model Weights`: released
  - `Training Code`: pending
  - `Evaluation Code`: pending
- 同时 repo 通过 `prepare/download_dependencies.py` 下载 annotations / embeddings / stats

当前本机已落地：

- `linkedCodebases/ActionPlan-Code/datasets/annotations/humanml3d_actionplan_merged/annotations.json`
- `linkedCodebases/ActionPlan-Code/datasets/motions/t2m_latent_frame_text_aligned/`

当前本机 quick stats：

- annotation json sequences: `26845`
- avg annotations per sequence: `2.99`
- median unique temporal segments per sequence: `1`
- multi-segment sequences: `2058`
- `2058 / 26845 ≈ 7.7%`

这意味着什么：

- 它确实开放了 frame-level / segment-aware training assets
- 但其中大量条目仍更像 caption merge / aligned text asset
- 它不是一个 clean 的、强多事件导向的 ordered-event benchmark

对 Plan B 的判断：

- 可作为 partial sidecar
- 尤其适合“frame-level semantic anchor”方向的扩展阅读
- 不适合作当前 `R_ord` 主 benchmark 替代

### 5.5 TM-Mamba / BABEL-Grounding

参考笔记：[[paperAnalysis/Motion_Generation/arXiv_2025/2025_TM_Mamba_Text_Controlled_Motion_Mamba_Text_Instructed_Temporal_Grounding|TM-Mamba]]

为什么不算 confirmed open dataset：

- KB note 只明确说它构建了 `BABEL-Grounding`
- note 中给出规模：`~10K motion-text-time-span triplets`
- 但本 note 里没有 code/data link
- 本轮 targeted search 也没有找到明确的官方 code repo 或 dataset page

所以当前更稳的说法是：

- `BABEL-Grounding` 是 **benchmark proposed**
- 但以当前 KB + 本轮检索证据，不足以把它记为 **confirmed open reusable dataset**

### 5.6 ChroAccRet

参考笔记：[[paperAnalysis/Motion_Generation/ECCV_2024/2024_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models|ChroAccRet]]

为什么不算 dataset release：

- 它有 GitHub code
- 但它做的是：
  - LLM event decomposition
  - shuffled temporal negatives
  - CAR probe / fine-tuning
- 这些 temporal negatives 是从现有数据上在线或离线构造出来的
- 不是单独释放的 benchmark dataset

因此：

- 它很重要
- 但它是 **method/probe asset**
- 不是 “还有一个 open event dataset”

## 6. 对 Plan B 的直接意义

### 6.1 现在最重要的负结论

当前没有第二个数据源能直接替换这句话：

> `HumanML3D-E` 是 Event-T2M / Plan B 当前最自然的 ordered-event 主 benchmark。

也就是说：

- 不要为了找“第二套 event 数据”而提前把主线切走
- 现阶段最稳的主线仍然是：
  - Event-T2M
  - HumanML3D-E
  - `R_pres / R_ord / R_dur`

### 6.2 现在最有价值的 sidecar

如果只从“额外 open temporal annotation asset”里挑一个最值得马上挂 sidecar 的，仍然是：

> **FineMotion**

原因：

1. 本机已落地
2. 读取成本低
3. 时序切片明确
4. 可直接服务 body-part / local interval 文字证据

### 6.3 最值得后续扩展但不该现在转线的

如果后续要找更强的 fine-grained temporal supervision 扩展方向：

1. `FrankenMotion / Frankenstein Dataset`
2. `FineMoGen / HuMMan-MoGen`

但它们的问题也很明显：

1. schema 更偏 part-centric hierarchical control
2. 底层 motion source 和当前主链不一致
3. 不适合现在直接拿来替代 `HumanML3D-E`

## 7. 一句话收口

当前 KB 里**确实还有其他 motion 工作开放了 temporal / snippet / part-level annotation asset**，但：

- **没有第二个和 `HumanML3D-E` 同型的 ordered-event benchmark**
- **最实用的额外 sidecar 仍然是 FineMotion**
- **FrankenMotion / FineMoGen 值得记账，但更像 future expansion**
- **ActionPlan / TM-Mamba 不能被误写成已经现成可替代的 event benchmark**


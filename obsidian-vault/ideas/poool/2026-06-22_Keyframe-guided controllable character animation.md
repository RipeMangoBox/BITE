---
title: "Weakly Supervised Semantic Keyframes for Controllable Character Animation"
status: idea/reframed-after-mvp
hypothesis: "运动学峰值只能提供物理显著关键帧；真正可攻的问题是从可靠的语义时间锚点中学习 motion event/key-window localization。当前 synthetic 显示 query-conditioned scorer 在干净监督下可学，BABEL 只给出弱阳性；下一步应转向非 text-to-motion 的动作检测/手势识别/动作预测任务，而不是继续从文本或能量规则批量构造语义关键帧。"
source_papers:
  - "[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]"
  - "[[analysis/arxiv_2026/ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos|ExpertEdit]]"
  - "[[analysis/arxiv_2026/MaxSim_Fine_grained_Motion_Retrieval_via_Joint_Angle_Motion_Images_and_Token_Patch_Late_Interaction|MaxSim]]"
  - "[[analysis/CVPR_2026/MoVie_Broaden_Your_Views_with_Human_Motion_for_Action_Detection.md|MoVie]]"
  - "[[analysis/CVPR_2026/OMG_Bench_A_New_Challenging_Benchmark_for_Skeleton_based_Online_Micro_Hand_Gesture_Recognition.md|OMG-Bench]]"
  - "[[analysis/ICLR_2026/Action_Guided_Attention_for_Video_Action_Anticipation.md|Action-Guided Attention]]"
  - "[[analysis/SIGGRAPH_2022/ASE_Large_Scale_Reusable_Adversarial_Skill_Embeddings_for_Physically_Simulated_Characters.md|ASE]]"
  - "[[analysis/ICLR_2024/FLD_Fourier_Latent_Dynamics_for_Structured_Motion_Representation_and_Learning.md|FLD]]"
  - "[[analysis/ICCV_2025/PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Synthesis_in_Human_Motion_Tasks.md|PUMPS]]"
created: 2026-06-22T22:10:00+08:00
updated: 2026-06-23T16:20:35+08:00
tags:
  - motion_generation
  - keyframe_control
  - weak_supervision
  - semantic_keyframe
  - idea/research
---

# Weakly Supervised Semantic Keyframes for Controllable Character Animation

> [!abstract] Current Judgment
> 这篇 idea 的核心已从“直接做 keyframe-guided controllable generator”收敛为一个更靠前、可证伪的问题：**现有数据能否提供可信的 semantic temporal anchors，让模型学会给定 motion 和语义 query 时定位对应 event window/key window？** 2026-06-23 的 4090 实验表明：synthetic 干净监督下 query-conditioned scorer 可学；BABEL 真实 frame annotation 上只有弱阳性；HumanML3D 文本切分和 camera surrogate 都不能作为核心证据。因此下一阶段不应继续从物理/能量规则或 T2M 文本里硬造“语义关键帧”，而应转向非 T2M 的动作检测、手势识别、动作预测等天然带时间语义锚点的任务。

> [!新想法]
> 核心：
> 1. 如何寻找到符合语义的关键帧。比如给定一段动作和对应的文本，关键帧可能有多个（比如文本有多个 event，每个 event 具体需要几个帧也不固定）。因此，一个新的问题是，如何在一段动作中找到对应的高语义契合的帧，而不是整段进行 motion-text 匹配（不同于 TMR 等现有所有 retrieval 方法）。
> 2. 关键帧除了动态能量角度，还需要兼顾语义角度。设计的识别器需要在同一套架构中能够充分支持生成和理解的统一，不要将理解（识别）和生成分割，统一模型能够兼顾理解和生成任务，从而 latent 表示能够具备更充分的语义信息，相当于强关联任务的互补。

## 1. 研究目标

### 1.1 最终目标

最终希望得到一个可用于角色动画控制的语义关键帧接口：

- 输入：一段 motion，以及一个语义 query 或事件标签。
- 输出：与该 query 对齐的 sparse key windows / key frames。
- 下游用途：这些关键帧可作为 Kimodo/MDM/CMC 类生成器的稀疏控制点，用于生成、补全、编辑或压缩重建。

这不是整段 motion-text retrieval。整段 retrieval 只判断“这段 motion 和这句文本是否匹配”；本任务需要判断“文本里的某个 event 对应 motion 的哪几个时间窗口”。

### 1.2 当前最小问题

当前不直接训练生成器，而是先验证前置监督是否成立：

> 给定 motion sequence 和语义 query，模型能否从滑动窗口候选中找出对应 event window，并显著优于 uniform、kinematic peak、shuffled-query 和 no-query baselines？

如果这个问题不成立，后续 keyframe-guided generator 没有可信控制点，直接训练生成器只会把失败原因混在一起。

### 1.3 关键边界

- **物理关键帧**：速度、加速度、能量、接触变化、关节极值等局部显著点。它们可自动批量构造，但只说明“这里运动变化大”。
- **语义关键帧**：与某个动作事件、交互目标、手势类别、阶段边界或任务意图对齐的时间锚点。它需要来自任务定义或可靠标注的语义时间信号。
- 当前判断：自动物理/能量规则不足以批量构造语义关键帧；它们只能作为候选或 baseline。

## 2. 规划

### 2.1 原始规划

原始路线是：

1. 从 HumanML3D / OpenT2M 里筛多 event motion-text pair。
2. 尝试从文本中解析 event。
3. 通过局部 motion-text scorer 找 event windows。
4. 再把发现的 keyframes 接入生成/编辑。

这个规划的问题是：T2M 文本通常是整段描述，不提供可靠子事件边界；如果用 LLM 或物理峰值自动推断帧号，容易把“物理显著点”包装成“语义关键帧”。

### 2.2 2026-06-23 后的新规划

经过 4090 MVP 后，路线改为：

1. 先把 semantic keyframe discovery 定义为 **query-conditioned temporal event/window localization**。
2. synthetic 只作为 controlled sanity check：检查模型和评估脚本能否区分 query-aware 与 query-agnostic。
3. BABEL 作为真实 action segment 诊断：检验真实 frame annotations 是否足够强。
4. 如果 BABEL/T2M 文本信号弱，就转向非 T2M 任务：
   - action detection：天然有 action class + temporal segment；
   - online gesture recognition：天然有 gesture class + start/end；
   - action anticipation：action distribution 可作为语义时间状态；
   - interaction/contact tasks：目标接触帧、交互开始/结束帧可作为语义锚点；
   - unsupervised skill/phase learning：作为非人类命名的 latent keyframe baseline。

### 2.3 止损标准

- 如果 normal query 与 shuffled/no_query 差距很小，说明 query 没被可靠使用。
- 如果 kinematic peak 接近 learned scorer，说明任务主要是物理显著点，不是语义发现。
- 如果 top-k 都扎堆在同一高能窗口，multi-event keyframe discovery 失败。
- 如果真实数据上 effect size 长期低于 0.05，暂不进入生成器训练。
- 如果标注本身无法稳定定义 event window，先换数据/任务，不训练更大模型。

## 3. 已执行实验

### 3.1 Synthetic Controlled Event-Window Localization

#### 目标

验证一个最小命题：

> 在干净、可控、有真实 event window 的数据上，query-conditioned scorer 是否能学会根据 query 找对应窗口，而不是只找运动能量峰值？

这个实验不验证真实人类语义，只验证模型/评估管线在控制条件下是否能工作。

#### 代码与运行

- 远端代码库：`/data/public/ripemangobox/Motion/StoryMotion`
- 主脚本：`scripts/semantic_keyframe_mvp.py`
- 聚合脚本：`scripts/aggregate_semkey.py`
- Python 环境：`/home/ripemangobox/miniconda3/envs/director/bin/python`
- 输出聚合：`runs/semantic_keyframe_mvp/20260623_combined_report_final/summary.md`
- combined records：348

#### 数据生成流程

每条 synthetic sequence 是一段 motion-like feature sequence，不是渲染后的人体骨架。它用于控制变量。

1. **事件采样**
   - 每条序列包含 2-4 个 event。
   - 每个 event 有 `event_id`、`start_frame`、`end_frame`。
   - event windows 随机放置，难度越高，event 间隔越小。

2. **motif 注入**
   - 每个 `event_id` 对应一个固定 motif 向量。
   - 关键修正：加入固定 `--motif-seed`，保证 train/test 中同一个 `event_id` 映射到同一个 motif。
   - 修正前，如果 train/test 的 motif 随 seed 改变，模型学到的 query-event 对应关系会无效。

3. **窗口内部扰动**
   - 在 event window 内注入正弦 envelope 形式的 motif。
   - 同时对局部维度加入扰动，使 event 不只是全局均值偏移。

4. **噪声与 distractor**
   - easy/medium/hard 通过噪声、motif 强度、distractor 数量、event gap 控制。
   - distractor 是高能但不对应当前 query 的窗口，用来防止模型只靠能量选帧。

#### 窗口化与特征

- `window_size = 16`
- `stride = 4`
- 先从 frame sequence 构造 `raw frame + velocity + acceleration`。
- 每个窗口汇总为：
  - mean
  - std
  - last minus first
  - energy
- 这些拼接成 `window_features`。

#### 标签构造

- 对每个 event，计算每个 candidate window 与 GT event window 的 IoU。
- IoU 不低于 0.5 的窗口标为正样本。
- 如果没有窗口达到 0.5，则取 IoU 最大的窗口作为 fallback 正样本，避免无正样本事件。

#### Query 构造

- `event_id` 映射到独立的 query embedding table。
- 注意：query embedding 不是 motif 向量本身。motif 是数据生成中的事件模式；query 是独立语义索引向量；二者只通过 `event_id` 对齐。

#### 模型与 baseline

| 模型 | 输入 | 作用 |
|---|---|---|
| kinematic | window energy | 纯物理峰值 baseline，不使用 query |
| prototype | event prototype 与 window feature 相似度 | 弱模板匹配 baseline |
| mlp | concat(window feature, query) | 主 query-conditioned scorer |
| late | normalized window/query late interaction + feature bias | token interaction 风格 scorer |

#### Query Ablation

每个模型都在三种 query 设置下评估：

| 设置 | 含义 | 验证目的 |
|---|---|---|
| normal | 正确 event query | 应该最高 |
| shuffled | 错配 query | 检查模型是否依赖 query-event 对应 |
| no_query | 零 query | 检查模型只靠 motion 本身能做到多少 |

关键判断逻辑：

- 如果 `normal > shuffled`，说明 query-event 对应有用。
- 如果 `normal > no_query`，说明 query 带来的信息超过纯 motion prior。
- 如果 kinematic 三种 query 完全一致，说明它只是物理峰值 baseline。
- duplicate penalty 用来检查 top candidates 是否重复落到同一个高能窗口。
- multi-event coverage 用来检查多事件是否都被覆盖，而不是只选一个显著片段。

#### 结果

主指标为 `R@3`，命中条件是 top-3 预测窗口中至少一个与 GT event window 的 IoU 不低于 0.5。

| setting | MLP normal | MLP shuffled | MLP no_query | late normal | kinematic |
|---|---:|---:|---:|---:|---:|
| synthetic easy | 0.981 | 0.475 | 0.680 | 0.836 | 0.417 |
| synthetic medium | 0.901 | 0.458 | 0.607 | 0.771 | 0.233 |
| synthetic hard | 0.721 | 0.392 | 0.485 | 0.676 | 0.217 |

关键观察：

- MLP normal 在三个难度上都明显高于 shuffled 和 no_query。
- kinematic 在 normal/shuffled/no_query 下完全一致，说明它不具备语义 query 条件化能力。
- hard setting 下 no_query 仍有 0.485，说明 motion 本身已有可利用结构；但 normal 进一步到 0.721，说明 query 确实提供额外信息。
- hard setting 下 duplicate 也支持这一点：`MLP normal` duplicate 约 0.175，而 `MLP no_query` 约 0.641；无 query 时 top candidates 更容易重复落到同一类高能窗口。

#### Synthetic 结论

synthetic 实验可以支持的 claim：

> 在固定事件类别和干净 event-window 监督下，query-conditioned local scorer 能够学习 event-specific window localization，并显著优于 shuffled-query、no-query 和 kinematic baselines。

synthetic 实验不能支持的 claim：

- 不能说解决了真实 weakly supervised semantic keyframe discovery。
- 不能说模型理解了开放文本语义。
- 不能说能直接提升生成/编辑质量。
- 不能说物理/能量规则能自动批量构造语义关键帧。

### 3.2 BABEL Frame Annotation Real-Data Experiment

#### 目标

验证 synthetic 中的 query-conditioned localization 是否能迁移到真实 action segment：

> 使用 BABEL frame_ann 的人工动作起止时间作为真实 temporal action segments，测试 normal query 是否明显优于 shuffled/no_query。

#### 代码与数据

- 脚本：`scripts/semantic_keyframe_babel_mvp.py`
- 聚合脚本：`scripts/aggregate_babel_semkey.py`
- 标注：`/data/public/ripemangobox/Motion/PriorMDM/data_loaders/babel-teach/train.json` 与 `val.json`
- motion features：`/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D/motion_data`
- 输出：`runs/semantic_keyframe_mvp/20260623_babel_frame_ann_combined_core/summary.md`
- total records：144

#### 设置

- 两个真实数据配置：
  - `frac0.45_center_w24`
  - `frac0.65_center_w24`
- 各 6 seeds。
- 与 synthetic 一致比较 `normal`、`shuffled`、`no_query`。
- 主指标：
  - `center@3`
  - `R@3 IoU0.3`
  - `R@3 IoU0.5`
  - duplicate

#### 核心结果

| setting | model | query | center@3 | R@3 IoU0.3 | R@3 IoU0.5 |
|---|---|---|---:|---:|---:|
| frac0.45_center_w24 | mlp | normal | 0.279 | 0.251 | 0.123 |
| frac0.45_center_w24 | mlp | shuffled | 0.268 | 0.241 | 0.115 |
| frac0.45_center_w24 | mlp | no_query | 0.271 | 0.244 | 0.117 |
| frac0.65_center_w24 | mlp | normal | 0.301 | 0.260 | 0.122 |
| frac0.65_center_w24 | mlp | shuffled | 0.283 | 0.232 | 0.109 |
| frac0.65_center_w24 | mlp | no_query | 0.289 | 0.241 | 0.111 |

Query ablation 关键数值：

- `frac0.45` MLP `center@3` normal vs shuffled delta = 0.011，approx p = 0.0697。
- `frac0.45` MLP `center@3` normal vs no_query delta = 0.008，approx p = 0.0096。
- `frac0.65` MLP `center@3` normal vs shuffled delta = 0.018，approx p = 0.0085。
- `frac0.65` MLP `R@3 IoU0.3` normal vs shuffled delta = 0.028，approx p approximately 0。
- kinematic 无 query effect。
- prototype 基本无有效 query gain。

#### BABEL 结论

BABEL 结果是**弱阳性**：

- frac0.65 下 normal query 有小幅统计信号；这里的 p 值来自当前聚合脚本的配对近似检验，只作为实验诊断，不作为严格统计结论。
- 但绝对提升只有 0.02-0.03 量级。
- 最佳 `center@3` 也只有 0.301，no_query 已达 0.289。

因此可以说：

> BABEL real action-window localization 说明 query-conditioned local scorer 在真实 action segment 上存在小幅 signal，但目前 effect size 太弱，不足以支撑真实 semantic keyframe discovery 成立。

不能说：

- 不能说 BABEL 已证明真实语义关键帧可可靠发现。
- 不能说可以进入生成器训练。
- 不能说 text-to-motion 弱监督足够。

### 3.3 HumanML3D From/To Smoke

曾尝试从 HumanML3D 文本中解析 `from/to` 或多阶段描述，把文本片段当作子事件窗口监督。但该路线被降级为 smoke：

- HumanML3D 文本主要是整段描述，不稳定提供子事件起止。
- `from/to` 并不可靠对应 motion 内部 frame segment。
- 自动解析容易引入无法验证的伪语义标签。

结论：HumanML3D `texts/*.txt` 不应作为当前核心 event-window supervision。

### 3.4 Camera Surrogate Negative Diagnostic

`20260623_camera_p1` 使用 PulpMotion camera segment labels 作为 real timeline surrogate。

结果：

- 所有 model/query variant 的 `R@1/3/5` 全为 0。

解释：

- 这不是 human semantic keyframe 证据。
- Camera GT segment 与短 window IoU 口径不匹配。
- Camera label 不是人体动作语义。
- 可用 multi-event 序列极小。

结论：camera surrogate 只能作为负诊断，不能作为 storyboard-key-shot idea 的有效实验，也不能证明 human semantic keyframe discovery 失败或成功。

## 4. 综合结论

### 4.1 已经成立的部分

- Query-conditioned local scorer 在干净 synthetic event-window 监督下可学。
- `normal/shuffled/no_query` ablation 能有效区分 query-aware 与 query-agnostic。
- kinematic peak 是必要 baseline，因为它清楚代表物理关键帧上限。
- BABEL frame_ann 能提供一点真实 action-window query signal。

### 4.2 没有成立的部分

- 真实弱监督语义关键帧发现尚未成立。
- T2M 文本不能直接当作可靠子事件监督。
- 物理/能量规则不能批量构造可信语义标签。
- Camera surrogate 不适合作为人体语义事件监督。
- 当前没有任何生成/编辑质量提升实验。

### 4.3 DS Max 重构草稿后的复核修正

DS Max 给出的重构方向是正确的：必须把本 note 分成规划、实验、结论和下一步，并把 BABEL 降级为弱阳性。

我复核后修正了两点事实边界：

- synthetic 的 query embedding 不是 motif 向量本身，而是独立 event query table；motif 是数据生成中的事件模式，二者通过 `event_id` 对齐。
- BABEL frac0.65 不是完全无效，而是当前聚合脚本下有小幅配对近似检验信号但 effect size 弱；合理表述是“弱阳性”，不是“失败”或“成立”。

## 5. 下一步方向

### 5.1 核心转向

下一步不应继续扩大 synthetic，也不应继续从 HumanML3D 文本里硬解析子事件。

新的核心问题：

> 在非 text-to-motion 任务中，哪些 motion 数据天然带有 semantic temporal anchors，能够作为语义关键帧发现的可靠监督或评估基准？

### 5.2 优先数据/任务

#### Action Detection

相关笔记：[[analysis/CVPR_2026/MoVie_Broaden_Your_Views_with_Human_Motion_for_Action_Detection.md|MoVie]]

优点：

- action class + start/end 本身就是语义 temporal segment。
- 可以直接评估 `class query -> action window`。
- 比 BABEL 的弱标签更接近标准 temporal detection。

候选：

- TSU-CS
- Multi-THUMOS
- Charades

#### Online Gesture Recognition

相关笔记：[[analysis/CVPR_2026/OMG_Bench_A_New_Challenging_Benchmark_for_Skeleton_based_Online_Micro_Hand_Gesture_Recognition.md|OMG-Bench]]

优点：

- 连续 skeleton stream。
- 13,948 个手势实例，40 类。
- gesture 实例短、边界清晰、类别语义明确。
- 适合作为“非文本语义 key window”的最小真实任务。

限制：

- 是手势域，不是全身角色动作。
- 但它比 BABEL 更适合验证 semantic temporal anchors 是否能被学到。

#### Action Anticipation / Action-Distribution Anchors

相关笔记：[[analysis/ICLR_2026/Action_Guided_Attention_for_Video_Action_Anticipation.md|Action-Guided Attention]]

优点：

- action distribution 可作为高层时间状态。
- 不依赖开放文本。
- 可测试“语义状态变化点”是否对应 keyframe。

#### Unsupervised Skill / Phase Baselines

相关笔记：

- [[analysis/SIGGRAPH_2022/ASE_Large_Scale_Reusable_Adversarial_Skill_Embeddings_for_Physically_Simulated_Characters.md|ASE]]
- [[analysis/ICLR_2024/FLD_Fourier_Latent_Dynamics_for_Structured_Motion_Representation_and_Learning.md|FLD]]
- [[analysis/ICCV_2025/PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Synthesis_in_Human_Motion_Tasks.md|PUMPS]]

定位：

- ASE 可发现 latent skills，但不是人类命名语义。
- FLD 可发现 phase/periodic structure，更适合 locomotion。
- PUMPS 是 motion prior / keyframe interpolation prior，不提供语义标签。

这些适合作为无文本/无监督 baseline，而不是主 claim 证据。

### 5.3 下一轮 MVP

优先做 **非 T2M semantic temporal anchor benchmark**：

1. 选一个有明确 temporal action/gesture boundary 的数据集。
2. 统一成与当前脚本兼容的格式：
   - `sequence_id`
   - `class_id`
   - `start_frame`
   - `end_frame`
   - `motion_features`
3. 复用 synthetic/BABEL 的 `normal/shuffled/no_query/kinematic` 评估。
4. 判断：
   - normal vs shuffled/no_query 的 margin 是否大于 BABEL；
   - kinematic 是否被明显拉开；
   - multi-event coverage 是否成立；
   - 是否能从 window segment 进一步抽 representative keyframe。

如果 action/gesture 数据上仍只有 0.02-0.03 的小幅 gain，则停止把它写成 semantic keyframe discovery，改为 physical/phase/key-event detection。

## 6. Evidence Layer

### 控制接口证据

[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 支持关键帧/轨迹作为强控制接口，但它不自动发现语义关键帧。因此本 idea 的机会不在“更会满足用户给定约束”，而在“自动找到哪些帧值得成为约束”。

### 物理关键相位证据

[[analysis/arxiv_2026/ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos|ExpertEdit]] 使用速度/加速度等运动学峰值发现技能关键相位，支持物理关键点对编辑有用。但它也说明：运动学关键相位不等于开放语义关键帧。

### 局部对齐证据

[[analysis/arxiv_2026/MaxSim_Fine_grained_Motion_Retrieval_via_Joint_Angle_Motion_Images_and_Token_Patch_Late_Interaction|MaxSim]] 说明局部 token-patch 对齐优于整段池化 retrieval。本 idea 可借鉴其局部 late interaction，但任务不同：MaxSim 排整段 motion，本任务定位 event window/keyframe。

### 非 T2M 语义时间锚点证据

[[analysis/CVPR_2026/MoVie_Broaden_Your_Views_with_Human_Motion_for_Action_Detection.md|MoVie]] 说明 skeleton motion 可作为结构化动作检测先验；动作检测任务天然有 class + temporal segment。

[[analysis/CVPR_2026/OMG_Bench_A_New_Challenging_Benchmark_for_Skeleton_based_Online_Micro_Hand_Gesture_Recognition.md|OMG-Bench]] 提供连续 skeleton 流中的 gesture instance boundary，是比 T2M 文本更干净的非文本语义窗口数据。

[[analysis/ICLR_2026/Action_Guided_Attention_for_Video_Action_Anticipation.md|Action-Guided Attention]] 说明 action prediction distribution 本身可作为高层语义时序状态，支持将 closed-set action label/distribution 用作 temporal query。

### 无监督 baseline 证据

[[analysis/SIGGRAPH_2022/ASE_Large_Scale_Reusable_Adversarial_Skill_Embeddings_for_Physically_Simulated_Characters.md|ASE]]、[[analysis/ICLR_2024/FLD_Fourier_Latent_Dynamics_for_Structured_Motion_Representation_and_Learning.md|FLD]]、[[analysis/ICCV_2025/PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Synthesis_in_Human_Motion_Tasks.md|PUMPS]] 可提供 skill/phase/motion prior baseline，但它们默认不提供人类命名语义关键帧。

## 7. Suggested Claim

当前能写的 claim：

> 在 controlled synthetic event-window setting 中，query-conditioned local scorers 能够显著优于 shuffled-query、no-query 和 kinematic baselines，说明 semantic key-window localization 的模型形式可行；但 BABEL real action segments 只显示弱 query gain，提示当前 T2M/BABEL 式弱监督不足以直接支撑真实语义关键帧发现。下一步应转向 action detection、gesture recognition、action anticipation 等非 T2M 任务中的天然语义时间锚点。

不能写的 claim：

- 不能说 weakly supervised semantic keyframe discovery 已解决。
- 不能说自动物理规则能构造语义关键帧标签。
- 不能说 BABEL 已充分证明真实语义关键帧可学。
- 不能说已提升 motion generation/editing。

## 8. 适合的论文定位

较强版本：

> Semantic temporal anchor discovery for controllable character animation.

贡献重点：

- 从整段 retrieval 转向 event/window localization。
- 系统区分物理 keyframes 与语义 temporal anchors。
- 评估非 T2M 任务中是否存在更可靠的语义时间监督。
- 再验证这些 anchors 作为 keyframe constraints 的生成/编辑价值。

较弱版本：

> Query-conditioned event-window localization for motion control.

风险：

- 如果真实数据 margin 仍然太小，会被认为只是动作检测/局部 retrieval 的变体。
- 如果没有生成/编辑下游收益，很难支撑 controllable animation 方向的贡献。

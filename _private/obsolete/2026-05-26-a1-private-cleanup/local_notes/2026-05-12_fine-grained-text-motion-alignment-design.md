---
created: 2026-05-12T21:41:28+08:00
updated: 2026-05-12T23:29:21+08:00
title: "Fine-Grained Text-Motion Alignment: Chunk-Part Grounded Design"
status: draft
hypothesis: "真正可落地的细粒度 text-to-motion 对齐，需要同步处理 text event、motion temporal chunk、body-part latent 三者，而不是只做文本侧事件分解或只做 motion autoencoder 语义化。"
tags:
  - research-idea
  - Motion_Generation
  - text-to-motion
  - fine-grained-alignment
  - body-part-control
  - temporal-grounding
source_papers:
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing]]"
  - "[[paperAnalysis/Motion_Generation_Text_Speech_Music_Driven/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_Move_in_2D_2D_Conditioned_Human_Motion_Generation]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2025/2025_TM_Mamba_Text_Controlled_Motion_Mamba_Text_Instructed_Temporal_Grounding]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis]]"
external_sources:
  - "https://nvlabs.github.io/motionbricks/"
  - "https://nvlabs.github.io/GR00T-WholeBodyControl/user_guide/training_data.html"
  - "https://nvlabs.github.io/GR00T-WholeBodyControl/references/motion_reference.html"
  - "/home/ripemangobox/Downloads/LM-Dispersion.pdf"
  - "https://research.nvidia.com/labs/gear/motionbricks/pdfs/motionbricks_siggraph_2026.pdf"
  - "https://github.com/abhinanda-punnakkal/BABEL"
  - "https://arxiv.org/abs/2404.11375"
  - "https://github.com/BizhuWu/FineMotion"
  - "https://github.com/EricGuo5513/HumanML3D"
  - "https://pjyazdian.github.io/MotionScript/"
---
# Fine-Grained Text-Motion Alignment: Chunk-Part Grounded Design

> [!abstract] TL;DR
> 当前最稳的论文切口不是“首次在 motion representation 中加入语义对齐”。这个点已经被 MoLingo 的 SAE 和 COME 的 MoCMAE 明确占据。
>
> 更可守的主张是：**在已有 motion 表征之上，显式学习 text event ↔ temporal chunk ↔ body part 的三方对齐，并把它接入生成、编辑与 segment-level evaluation。**
>
> 建议主线：`Chunk-Part Grounded Alignment (CPGA)`。

## 1. Boundary: 什么不能再 claim

以下主张风险很高，不建议作为 novelty：

1. **“motion autoencoder 阶段引入语义对齐是空白”**  
   [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]] 已经用帧级文本标签和 soft cosine loss 训练语义对齐自编码器；[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]] 已经用 contrastive masked autoencoder 改造连续潜空间。

2. **“全局 CLIP/T5 换一个更强文本编码器就是细粒度对齐”**  
   [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]] 已经明确指出 CLIP 的图像-语言空间和 motion 动态语义不匹配。文本编码器替换只能是条件，不是贡献本身。

3. **“FineMotion/Kimodo 已经解决同步切分，所以问题结束”**  
   [[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing|FineMotion]] 给了 0.5s × body-part 的公开强监督，但覆盖仍偏 HumanML3D 分布；[[paperAnalysis/Motion_Generation_Text_Speech_Music_Driven/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 是强工业系统但关键数据闭源，不适合作为可复现实验核心。

4. **“视觉 prior 直接接入就能解决 text-to-motion”**  
   SkeletonLLM、Move-in-2D、MTVCraft 证明视觉/视频 prior 有价值，但也提示风险：容易变成 text-to-video、静态 CLIP 对齐，或 motion-to-video 控制，而不是 3D motion 细粒度生成。

## 2. Data Position

真正有价值的数据不是“文本被切了”或“动作被切了”，而是二者在时间和身体结构上可以互相校验。

| 资源 | 粒度 | 适合用途 | 边界 |
| --- | --- | --- | --- |
| FineMotion | 0.5s × body-part | 主监督、局部 span、部位控制 | HumanML3D 分布内为主，自动标注非完美 |
| BABEL | action segment / frame-aligned action labels | duration、overlap、长序列动作段 | 有 motion-side 时间段，但不是 HumanML3D-E 式 ordered text event list |
| TEACH | text-duration segments | 多段编排、composition | 更像任务集，不是部位级语义 |
| FineMoGen | stage × body-part | 手工边界部位控制 | 规模和泛化弱于 BABEL |
| Motion-X | frame / pose text | frame-level 补充、whole-body expressive | 许可和格式对接成本较高 |
| HumanML3D | mostly sequence-level captions + sparse start/end fields | 原始主数据、少量子段 caption | 多数 caption 是 whole-sequence，不足以构成 event benchmark |
| HumanML3D-E | event benchmark | multi-event 顺序评估 | motion 仍多来自 full sequence，不能单独支撑跨模态局部对齐 |
| BABEL-Grounding / TM-Mamba | text query → motion span | 训练/校准 temporal grounding | 基于 BABEL，单查询单段，规模有限；不等价于 full caption ordered events |
| MG-MotionLLM scripts | 0.5s script / localization | script prior、弱定位模型 | scripts 多由 LLM 构造，需防止自举标签当真值 |
| MotionScript | automatic fine-grained motion captioning | script generator / segmentation prior | 更像生成工具，不是已确认的标准 timestamped event-span benchmark |
| FrankenMotion / CompMo / OpenT2M | part/action/segment 或 dense caption | future expansion、外部 stress test | 公开完整性和 schema 需逐项核验，不能默认替代 HumanML3D-E |
| Kimodo / BONES-SEED | timeline / constraints / robotics | 工业上限、表征和控制接口参考 | Kimodo 核心数据闭源；BONES-SEED 很接近但更偏 humanoid robotics，需二次核对文本与分段一一对应 |

### 2.1 开源同步边界资产的分级结论

这轮用本地 KB、Web、Kimi、DeepSeek 和 GPT-5.4 子任务交叉查了一遍。DeepSeek 的一次短答把 HumanML3D-E / FineMotion / Motion-X 的同步性说得过强，不能直接采信；以下以本地论文笔记和可核到的项目页为准。

结论不是“完全没有”，而是要分三档：

1. **有同步 motion span，但不是 HumanML3D-E 同型 ordered events**：BABEL、TEACH、BABEL-Grounding、FineMotion、FineMoGen、MG-MotionLLM scripts。
2. **有 text event list，但 motion-side event span 缺失或隐式**：HumanML3D-E / Event-T2M、ChroAccRet 式 event decomposition。
3. **可能很相关但不能直接当现成主数据**：FrankenMotion、CompMo、OpenT2M、Motion-X、MotionScript、BONES-SEED。它们可能有 part/action/segment/dense caption 或工具链资产，但 schema、开放状态、许可和与 HumanML3D-E 的同型性需要单独核验。

补充边界：HumanML3D 原始文本文件确实有 start/end 字段，但多数 caption 是 `0.0 / 0.0` 的整段描述，只有少量复杂动作提供子段时间，覆盖率不足以替代 HumanML3D-E 的 ordered-event benchmark。

因此，当前真正的 gap 更精确地说是：

```text
There are open temporal motion-language assets,
but no confirmed open dataset that simultaneously gives
HumanML3D-E-style ordered text events
and verified motion-side event timestamps
for the same HumanML3D motion-caption pairs.
```

这个 gap 正好支持一个实在的数据贡献：在 HumanML3D-E 的 ordered text events 上补 motion-side event timestamps。

### 2.2 Kimodo 的 timestamp / atomic action 边界

Kimodo 的关键启发不是“提出了一个 motion event segmentation 算法”，而是**数据生产阶段已经有多粒度文本和 sub-clip 边界**。

论文 Sec.3 的表述是：

1. 每个 mocap sequence 有整段 `overview description`。
2. 每个 clip 被拆成更细的 `atomic action sub-clips`。
3. 每个 atomic sub-clip 有自己的文本描述。
4. 训练时会混合 full clips、single / combined action sub-clips、stitched clips、原始描述和 Qwen3-32B paraphrases。

但论文没有公开说明：

```text
motion signal → automatic event boundary detector → timestamped atomic action
```

也没有说 Qwen3-32B 负责发现时间边界。Qwen3-32B 的角色更像是 paraphrase / prompt normalization，而不是 motion-side timestamp segmentation。

因此最稳证据边界是：

```text
Kimodo has real interval-level sub-clips.
The paper does not disclose a reusable motion-side event segmentation algorithm.
The most plausible source is Bones Rigplay annotation / authoring metadata,
but this remains an inference rather than an exposed dataset recipe.
```

这对当前路线有一个直接约束：不能把 Kimodo 当作 HumanML3D-E 缺失 motion event 切分的公开解决方案。它只能作为“高质量数据应该同时保留 overview、atomic segment、paraphrase、constraint metadata”的系统参考。

### 2.3 FineMotion / HumanML3D-E 的格式冲突

FineMotion 和 HumanML3D-E 不能直接拼成一个干净的统一监督集：

1. FineMotion 按秒级时间戳 / 固定片段生成 body-part 描述，粒度偏 `time interval × body part`。
2. HumanML3D-E 偏 event decomposition / multi-event benchmark，motion 侧仍是原 HumanML3D full sequence，缺少对应 event motion span。
3. FineMotion 对 HumanML3D 的保留和筛选与 HumanML3D-E 不同，样本集合不能默认一一对齐。

如果只能保留一个主格式，当前更推荐保留 **event 格式作为文本/任务接口**，但需要承认：

```text
event format gives better semantic structure,
but does not automatically provide motion-side event spans.
```

因此主问题应改成：如何从 event 文本出发，得到可信的 weak / verified motion spans，而不是假设已有 event timestamp。

### 2.4 新数据贡献：Event-Guided Motion Timestamping

可以把你的想法收成一个明确贡献点：

```text
Given HumanML3D-E ordered text events and the original full motion,
recover event-level motion timestamps by querying fine-grained rendered slices
with event-conditioned VQA / motion-language judging.
```

核心不是“让 MLLM 看一整段视频打分”，而是做 **event-conditioned boundary search**：

```text
HumanML3D-E caption
→ ordered events e_1...e_K
→ render full GT motion into overlapping fine slices
→ for each event e_i, ask VQA / motion-language judge:
   is this event present, absent, starting, ending, or transitional?
→ aggregate slice scores under monotonicity and coverage constraints
→ output timestamped event-motion alignment
```

这能直接补上 HumanML3D-E 的关键短板：它有 text event 边界，但没有 motion event 边界。补齐后得到的不是另一个 global retrieval benchmark，而是：

```text
HumanML3D-E-Timestamped:
caption → ordered events → motion intervals → optional body-part evidence
```

这个贡献比“再设计一个 alignment loss”更稳，因为它解决的是公共数据接口缺失。后续 CPGA、temporal grounding、event-conditioned generation、segment-level evaluation 都可以建立在这个资产上。

证据边界要写清：

1. 这些 timestamps 初版是 **pseudo-label / weak verified labels**，不能直接宣称人工真值。
2. VQA / MLLM 不能作为最终 evaluator；它只是 proposal generator 或 cross-check。
3. 最终可信度来自 human audit、BABEL-Grounding / FineMotion / BABEL 交叉校准、以及下游 heldout segment 指标。

最低可行 pipeline：

1. 先取 HumanML3D-E 中 `K>=3` 的 100-200 条 GT motion。
2. 每段 motion 渲染为 0.5s 或 1.0s sliding slices，stride 0.25s / 0.5s。
3. 对每个 `(event, slice)` 生成 `present / absent / transition / ambiguous` 标签和置信度。
4. 用单调 DP 或 OT 把事件分配到连续时间区间，允许相邻 event 共享 transition。
5. 人工盲审 50-100 个 event spans，报告 boundary IoU、start/end error、coverage、ambiguous rate。
6. 用 BABEL-Grounding 或 FineMotion 的已知 span 做外部 sanity calibration，不把它们和 HumanML3D-E 强行合并。

若这个 pipeline 成立，后续路线应从 `FineMotion-only chunk-part alignment head` 调整为：

```text
Stage 0: HumanML3D-E event-to-motion timestamping
Stage 1: CPGA on timestamped event spans + FineMotion chunk-part side supervision
Stage 2: generation/editing/evaluation with event-time-body-part grounding
```

外部核对：

- [GR00T WholeBodyControl training data](https://nvlabs.github.io/GR00T-WholeBodyControl/user_guide/training_data.html) 记录 BONES-SEED 有自然语言描述、temporal segmentation 和 SOMA / Unitree G1 格式，是值得关注的开放机器人动作资产。
- [GR00T motion reference format](https://nvlabs.github.io/GR00T-WholeBodyControl/references/motion_reference.html) 给出 joint position、velocity、body pose、SMPL 等部署格式，适合作为 motion representation 到机器人控制的落地桥。
- BABEL 官方 repo 提供 AMASS motion 的 action / frame-level language annotation，可作为 duration 和 temporal grounding 校准源。
- TM-Mamba 的 BABEL-Grounding 定义了 text query 到 motion span 的 THMG 任务，适合作外部 calibration，但不是 HumanML3D-E 同型的 ordered-event benchmark。

## 3. Representation Design

### 3.1 Text Representation

目标不是把整句编码得更强，而是把文本变成可对齐的结构：

```text
global caption
→ ordered events
→ event × body-part hints
→ optional duration / phase / frequency attributes
→ event embeddings with dispersion regularization
```

建议采用三层文本特征：

1. **Global text embedding**：保留整体语义，避免局部描述把全局动作带偏。
2. **Event embedding**：从 caption / script 中抽取有序 event，负责顺序与完整性。
3. **Part-aware phrase embedding**：捕捉 “left arm raises”“torso bends” 这类 body-part 语义。

LM-Dispersion 的迁移方式应很克制：不是 claim 新损失，而是把它作为 **text event 去稠密化正则**。具体目标是防止多个 event token 在 encoder 后塌到近似方向，使 “walk / turn / wave / crouch” 在下游 alignment head 中更可分。

最低实现：

```text
L_text_disp = logsumexp(-angular_distance(e_i, e_j) / tau)
```

只在 event / part phrase embedding 上加，避免破坏全局句向量。

### 3.2 Motion Representation

MotionBricks 前 10 页给出的最有用启发不是“用它替代 T2M”，而是表征分工：

1. **显式 motion state**：root、pose、joint velocity、contact 都保留，不把所有信息压进一个黑盒 latent。
2. **multi-head tokenizer**：让 motion latent 有多个 codebook head，降低单个 token 错误导致全身崩坏的风险。
3. **root / pose / decoder 分治**：先处理全局 root，再处理 body pose，最后解码和精修。
4. **smart primitive as constraint interface**：高层任务不要直接改所有 latent，而是生成 keyframe / root / object proxy constraints。

对 CPGA 的具体建议：

```text
motion M
→ 0.5s temporal chunks
→ body-part groups
→ chunk-part tokens z[t, part]
→ optional root/body/contact channels
→ global sequence token
```

这比单纯 sequence token 更适合 FineMotion，也能兼容 Kimodo-like raw feature：

```text
root position + root heading + joint position + joint velocity + joint rotation + foot contact
```

若直接训练 representation 风险过高，MVP 只需冻结已有 motion encoder，训练一个 chunk-part projection / alignment head。

## 4. Recommended Route: CPGA + Timestamping

### One-Sentence Claim

```text
We first recover event-level motion timestamps for HumanML3D-E
through event-conditioned fine-slice VQA and monotonic boundary search,
then use chunk-part grounded alignment to connect text events,
temporal motion spans, and body-part motion tokens.
```

### Pipeline

```text
HumanML3D-E text events
→ fine-slice render / motion-language judging
→ monotonic event-to-motion timestamping
→ timestamped event spans

FineMotion / BABEL / BABEL-Grounding side assets
→ event parser / script normalizer
→ event and part-phrase embeddings
→ event dispersion regularization

motion sequence
→ chunking by recovered event spans + 0.5s local chunks
→ body-part grouped motion tokens
→ chunk-part projection

alignment
→ soft OT / InfoNCE / monotonic matching between event tokens and chunk-part tokens
→ optional late-interaction score like PST
→ generator condition gate or editor mask
```

### Why this is not just MoLingo / COME

MoLingo and COME primarily reshape the **latent space** so generation is easier. CPGA instead focuses on the **correspondence structure**:

```text
which text event
matches which temporal chunk
and which body part
```

That correspondence can supervise:

1. generation conditioning,
2. zero-shot editing masks,
3. controllable generation masks,
4. segment-level evaluation.

## 5. Candidate Routes

| Route | Main idea | Priority | Why |
| --- | --- | --- | --- |
| A. Event-guided motion timestamping | HumanML3D-E events + fine-slice VQA + monotonic boundary search | 1 | 直接补公共数据接口缺口，贡献更实 |
| B. CPGA supervised alignment | timestamped event spans + FineMotion chunk-part tokens + event dispersion + OT/InfoNCE matching | 2 | 在新数据资产上做对齐模型 |
| C. CPGA + reward-gated refinement | 用 uncertainty / attention high-ambiguity cases 做局部 rerank 或 refinement | 3 | 有潜力，但不适合作 MVP 主训练 |
| D. Visual-prior sidecar | Skeleton rendering / DINO video prior 辅助 verifier 或 pseudo-label | 4 | 现在变成 Stage 0 的工具，不应抢主贡献 |

Kimi 的建议偏向 Route A：先做 latent event dispersion + temporal-part pyramid。DeepSeek 的补充更保守：不要把 dispersion 说成新 latent structure，MVP 应先做 frozen encoder + 轻量 alignment head，RL 只做后续闭环。

## 6. RL Role

RL 不建议作为第一版主贡献。更稳的角色是 **data selection and local refinement**：

1. 用 chunk-part alignment uncertainty 找到高歧义训练样本。
2. 对 high-uncertainty chunks 做重采样、rerank 或局部 refinement。
3. 只在已有 supervised alignment head 稳定后，再考虑 DPO / GRPO。

可迁移原则：

- Perception-R1：RL 对高不确定性感知任务更有效。迁移到 motion：只对 body-part ambiguity、order conflict、duration conflict 这类高困惑样本启用。
- APPO：attention 可以当关键帧/关键 chunk 侧信号。迁移到 motion：用 cross-attention peak 找可能的 event span，但不能把 attention 当最终证据。
- PAPO 类视觉损坏对比：可迁移为 “full motion vs masked part / corrupted chunk” 的 implicit dependence test。

角色边界：

```text
RL signal = reward / mining / rerank side signal
not final evaluator
not first-stage training backbone
```

## 7. Visual Prior Role

视觉 prior 的稳妥定位：

1. **Verifier**：把 skeleton 渲染为图像/视频，让 MLLM 判断 body-part event 是否出现。
2. **Pseudo-label aid**：对 FineMotion 之外的数据生成弱部位/动作线索。
3. **Structure prior**：DINO / video encoder 只辅助局部空间布局或时序显著性，不直接替代 motion encoder。

不建议：

```text
text → visual embedding → motion
```

作为主路线。这个链条容易被 LaMP 攻击为静态视觉语义错配，也容易被 MTVCraft / TokenMotion 归入 video generation 邻近工作。

更好的写法：

```text
visual/video prior is a sidecar verifier and weak-label generator
for hard-to-label chunk-part alignment,
while the primary output and training target remain 3D motion.
```

## 8. Two-Week MVP

目标：先证明 HumanML3D-E 的 text event 可以被补成可审计的 motion timestamps，再证明这些 timestamps 能提升 `event × chunk × part` 对齐。

### Week 1

1. 选 HumanML3D-E 小子集：`K>=3` 的 100-200 条 GT motion。
2. 渲染 motion fine slices：0.5s / 1.0s window，0.25s / 0.5s stride。
3. 对每个 `(event, slice)` 跑 VQA / motion-language judge，输出 presence、transition、confidence。
4. 用单调 DP / OT 生成 event motion spans。
5. 抽 50-100 个 spans 做人工盲审，报告 boundary IoU、start/end error、coverage、ambiguous rate。

### Week 2

1. 消融：
   - VQA-only vs motion-encoder score-only vs fused score；
   - no monotonic constraint；
   - equal-duration baseline；
   - global-only retrieval baseline。
2. 评估：
   - human-audited span quality；
   - BABEL-Grounding / FineMotion 外部校准；
   - event order consistency；
   - timestamped span 是否优于 equal split。
3. 对齐侧最小接入：
   - 冻结 text encoder 和 motion encoder；
   - 只训练轻量 event-span / chunk-part projection head；
   - 不急着重训完整 generator。

成功标准：

```text
VQA+monotonic timestamps 明显优于 equal-duration baseline；
人工审计显示多数 event spans 可解释；
BABEL-Grounding / FineMotion 校准不暴露系统性偏移；
timestamped spans 能提升 event-to-motion local retrieval 或 localization。
```

## 9. Metrics and Evidence Roles

任何 metric 记录都要写清：

```text
date / artifact_path / evaluator / protocol / motion_source / condition_pair /
n/evaluable / coverage / role / used_for / limitations
```

建议角色：

| Metric | Role | Used for |
| --- | --- | --- |
| HumanML3D-E timestamp boundary IoU | dev_metric | timestamp proposal tuning |
| Human audit of event spans | heldout_final_evaluator | dataset quality claim |
| Equal-duration split baseline | cross_check | timestamp sanity |
| BABEL-Grounding calibration | cross_check | external temporal grounding sanity |
| FineMotion chunk-part localization | dev_metric | tuning / selection |
| Global retrieval | cross_check | regression check |
| Ordering consistency | cross_check | ordering check |
| Soft chunk mask | dev_metric | span proposal |
| MLLM rendered skeleton judge | cross_check | qualitative calibration |
| Human review | heldout_final_evaluator | final small-sample claim |

不要把 attention、MLLM sidecar、retrieval score 或 ordering score 单独升级成 final evaluator。

## 10. Reviewer Attacks

| Attack | Why dangerous | Repair |
| --- | --- | --- |
| “这只是 FineMotion supervised overfit” | FineMotion 标注强，泛化会被质疑 | 加 BABEL / HumanML3D-E / Motion-X zero-shot 或 weak-label 退化实验 |
| “BABEL-Grounding / MG-MotionLLM 已经做 temporal grounding” | novelty 被压缩 | 强调本文补的是 HumanML3D-E ordered event list 的 motion timestamps，不是单查询 grounding 模型 |
| “VQA 伪标签不可信” | 数据贡献可能被攻击 | 人工盲审、外部校准、等长 baseline、ambiguity 标签和 coverage 报告必须齐 |
| “MoLingo/COME 已经做语义表征” | novelty 被压缩 | 明确本文贡献是 correspondence / grounding，不是 autoencoder semantic latent |
| “Dispersion 只是 contrastive variant” | LM-Dispersion 迁移不够新 | 把 dispersion 降为 text event regularizer；主贡献放在 chunk-part matching |
| “RL/visual prior 太散” | 容易像 proposal soup | MVP 不启用 RL；visual prior 只做 verifier / pseudo-label sidecar |
| “自动指标不可信” | motion-text 细粒度评估常被攻击 | 小规模 human heldout + segment-level audit；自动指标只做 cross-check |

## 11. Next Concrete Decision

我建议当前路线收成：

```text
MVP = HumanML3D-E event-guided motion timestamping
Backbone = frozen text/motion encoders
Novelty = ordered text events + recovered motion event spans
Stage-2 novelty = event × chunk × body-part correspondence
Regularizer = optional text event dispersion
Checks = human audit / BABEL-Grounding calibration / equal-split baseline
Future = CPGA training + RL-gated local refinement
```

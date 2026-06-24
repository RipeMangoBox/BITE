---
title: Multi-Level Pivot Alignment for Text-Motion Generation
created: 2026-05-18T20:36:00+08:00
updated: 2026-05-20T01:00:00+08:00
status: draft
hypothesis: 提高生成动作的 text-motion alignment，关键不只是换更强文本编码器或单次 event decomposition，而是把 frame labels、events、part phrases、temporal chunks 与 body-part motion tokens 组织成多级 pivot，先粗定位再细匹配，并把 correspondence 作为可验证的中间层。
tags:
  - research-idea
  - Motion_Generation
  - text-motion-alignment
  - fine-grained-alignment
  - event-grounding
  - body-part-control
  - late-interaction
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]]"
  - "[[paperAnalysis/Motion_Generation/AAAI_2026/2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text|FineXtrol]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference|LaMoGen]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]"
  - "[[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoCHA_Denoising_Caption_Supervision_Motion_Text_Retrieval|MoCHA]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing|FineMotion]]"
  - "[[paperAnalysis/Motion_Generation/ECCV_2024/2024_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models|ChroAccRet]]"
related_notes:
  - "[[ideas/fine-grained-alignment/roadmap|MLPA current roadmap]]"
  - "[[ideas/fine-grained-alignment/mechanism_transfer/README|MLPA mechanism transfer notes]]"
  - "[[gates|MLPA experimental gates]]"
  - "[[2026-05-12_fine-grained-text-motion-alignment-design|CPGA reference]]"
  - "[[2026-05-18_text_motion_alignment_2025_2026_map|2025-2026 alignment map]]"
  - "[[2026-05-19_multi-agent-consultation-and-molingo-audit|multi-agent consultation and MoLingo audit]]"
  - "[[ideas/TAMR/ROADMAP|TAMR Roadmap]]"
  - "[[paperIDEAs/MoDebug/experiments/p1_event_transfer_20260516/results/task1_summary|MoDebug P1 task1 summary]]"
external_sources:
  - "BABEL official data page: https://babel.is.tue.mpg.de/data.html"
  - /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/obsidian-vault/analysis/ICLR_2026/A.I.R._Enabling_Adaptive_Iterative_and_Reasoning-based_Frame_Selection_For_Video_Question_Answering.md
  - /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/obsidian-vault/analysis/ICLR_2026/A_Hidden_Semantic_Bottleneck_in_Conditional_Embeddings_of_Diffusion_Transformers.md
  - /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/obsidian-vault/analysis/ICLR_2026/ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text_to_Image_Diffusion_Personalization.md
  - /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/obsidian-vault/analysis/ICLR_2026/A2D_Any_Order_Any_Step_Safety_Alignment_for_Diffusion_Language_Models.md
---
# Multi-Level Pivot Alignment for Text-Motion Generation

> [!warning] 2026-05-20 Active Override
> 本文件保留为 MLPA 的早期主笔记和 related-work/novelty 边界资料。当前 canonical 路线改为 [[ideas/fine-grained-alignment/roadmap|MLPA Current Roadmap]]：从 3DGS / triplane / MLLM / bottleneck 等跨领域机制中抽象出 motion-specific `event-time-body correspondence layer`，先做 timestamping 和 frozen rerank gate，不把 MLPA 写成 MoDebug 的 text embedding 或 event completion failure 分支。

> [!abstract] TL;DR
> 你的直觉可以收成一个更稳的研究框架：**把 MoLingo 的 frame-level label 从单个语义锚点升级为多级 pivot system**。
>
> 不是 claim “首次在 representation 阶段做语义对齐”，因为 [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]] 和 [[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]] 已经占住这个位置。
>
> 更稳的 claim 是：**现有方法已经证明 semantic latent、event condition、frame action plan、part control 各自有效，但缺少一个可审计的 correspondence layer 来说明哪个 text event / part phrase 对应 motion 的哪个 time chunk / body part。**
>
> 建议命名：**MLPA: Multi-Level Pivot Alignment**。第一版不要重训 generator，先做 frozen encoder + lightweight alignment head / structured rerank / event-span timestamping。

## 1. 重新表述问题

当前 text-to-motion alignment 的核心瓶颈不是“文本编码器不够强”这么简单，而是三类压缩同时发生：

1. **Text side compression**：复杂 prompt 被压成 fixed token 或 pooled embedding，多事件、顺序、频率、身体部位信息互相挤压。
2. **Motion side compression**：长 motion 被压成 sequence latent 或 code tokens，时间段、身体部位、root/contact 等结构不一定显式可检索。
3. **Correspondence compression**：即使 text 与 motion 在全局 embedding 上接近，也不知道哪个 text span 对应哪个 motion segment。

因此，这个方向的更精确目标应是：

```text
从 global text-motion matching
升级为 text event / phrase ↔ temporal chunk / body-part token 的可审计 correspondence。
```

这里的关键不是再提出一个 abstract “planner”，而是建立一组中间锚点：

```text
frame label
→ event span
→ part phrase
→ body-part temporal chunk
→ contact / root / trajectory cue
```

这些锚点像“大头钉”，把 text space 与 motion space 的若干关键点先 pin 住，再用 late interaction、monotonic DP 或 soft OT 做更细粒度的局部匹配。

## 2. 为什么这个问题有支撑

### 2.1 MoLingo 证明了 frame label pivot 有效，但也暴露了上限

[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]] 的 `core_operator` 是 SAE + 多 token cross-attention + masked auto-regressive rectified flow。它最关键的事实是：motion representation 阶段不再只做重建，而是用 BABEL frame-level text labels / class tokens 做 soft cosine alignment，使 latent space 具有语义聚类结构。

这直接支持你的观点：

```text
representation stage 可以引入语义对齐；
frame-level label 可以作为 motion/text space 的 pivot。
```

但 MoLingo 的 pivot 仍然偏粗：

1. 单个 frame label 往往只描述主动作，不足以覆盖全身多部位行为。
2. frame label 可能给出动作类别，但不直接给出 text event ↔ motion segment 的完整对应关系。
3. 对复杂 prompt，label pivot 不能单独表达顺序、频率、持续时间、左右身体部位、并行动作。

所以更自然的下一步不是否定 MoLingo，而是把它的 frame label 从单层锚点扩成多级锚点。

### 2.2 ActionPlan 证明“干净中间语义层”能降低生成难度

[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]] 的核心不是简单多阶段，而是：

```text
先生成逐帧语义 Action Plan
再用干净 Action Plan 条件生成 motion。
```

它的消融显示，两阶段 Action Plan 比文本和 motion 联合生成更好。这个证据支持一个重要原则：

```text
semantic intermediate 如果足够干净，可以让 motion generation 少承担“同时理解语义与合成动作”的压力。
```

对 MLPA 的启发是：多级 pivot 不一定一开始就进入完整训练。它也可以先作为：

1. 训练前的数据审计层；
2. rerank / verifier 层；
3. generation candidate 的 local refinement 条件；
4. 后续才接入 representation 或 diffusion training。

### 2.3 Event-T2M 证明 event 是合理粒度，但 motion-side timestamp 仍是空缺

[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]] 把复杂 prompt 分解成最小语义自包含事件，再做 event-level cross-attention。它证明“一个 prompt 一个 embedding”会在多事件场景下信息坍缩。

但它仍留下一个关键缺口：

```text
event condition 是显式的；
event 在 motion 时间轴上的 allocation 仍然主要是隐式学习的。
```

这正是 MLPA 可以切入的地方：把 text events 和 motion temporal chunks 的对应关系显式建模出来，而不是只把 event embeddings 交给扩散模型自己学。

### 2.4 FineXtrol / FrankenMotion / LaMoGen 说明空间已经拥挤，必须收窄 claim

[[paperAnalysis/Motion_Generation/AAAI_2026/2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text|FineXtrol]] 已经把 control signal 做成 `body part × temporal interval` 的 fine-grained text，并训练层级对比 text encoder。

[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]] 已经利用 LLM 构建时序感知的部位级标注，并训练三级文本条件化 diffusion。

[[paperAnalysis/Motion_Generation/CVPR_2026/2026_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference|LaMoGen]] 已经把 text → symbolic body-part plan → motion 解码做成两阶段。

因此不能 claim：

```text
首次提出 body-part plan；
首次提出 event plan；
首次提出 temporal interval text control；
首次提出 semantic representation。
```

更稳的 claim 是：

```text
已有工作分别做了 semantic latent、event condition、part control、symbolic plan；
但这些中间层大多缺少统一的 event-time-part correspondence verification，
也很少作为 frozen rerank / timestamp / alignment head 先独立验证。
```

## 3. BABEL frame-level label 到底是什么

根据 BABEL 官方 data page，dense annotations 包括 `train.json`、`val.json`、`test.json`。每个 sequence 有一个 sequence label，并且 zero or one set of frame labels；frame labels 通常在 sequence 含有多个 action 时提供。官方说明 `frame_ann` 是 precise start/end action segment labels，字段包括 `raw_label`、`proc_label`、`act_cat`、`start_t`、`end_t`。Extra annotations 还可能有 zero or more sets of frame labels。

这意味着：

```text
BABEL frame-level labels 更准确地说是 action segment labels with start/end timestamps。
```

它们不是每一帧都有一个完整自然语言句子，也不是 HumanML3D-E 式 ordered text event list。它们适合作为：

1. frame / segment semantic pivot；
2. duration calibration；
3. event boundary sanity source；
4. action category anchor；

但不应被误写成：

```text
BABEL provides complete full-body natural-language frame captions for every frame.
```

这一点对 MLPA 很重要：BABEL 支持 frame/segment-level anchor，但如果目标是 full prompt 的 multi-event alignment，仍需 HumanML3D-E / FineMotion / BABEL-Grounding / 自建 timestamping 共同补齐。

## 4. Cross-Domain 启发

### 4.1 A.I.R.: query-aware evidence acquisition

外部 ICLR_2026 note `A.I.R.` 的核心是自适应初始采样 + 迭代 VLM 验证 + 局部密度采样。它不直接做 motion，但给 MLPA 一个清晰范式：

```text
不要平均分析整段 motion；
按 text query / event 动态选择高价值时间段；
用强 judge 只验证小批候选；
再在邻域扩展。
```

迁移到 motion：

```text
full caption → events
motion render / motion tokens → candidate chunks
event-conditioned judge → verify present / absent / transition
localized chunk expansion → refine boundaries
monotonic DP / OT → output event spans
```

这比“让 MLLM 看完整 skeleton video 打总分”更有价值，因为它把成本集中在 event-relevant chunks。【问题：但motion sequence除了event chunk，就是过渡片段。为了获得event-relevant chunks正需要MLLM看完整序列，或者一帧帧看。这个假设循环依赖了】

### 4.2 Hidden Semantic Bottleneck: global condition 不可靠

【新想法：能否】

外部 ICLR_2026 note `A Hidden Semantic Bottleneck in Conditional Embeddings of Diffusion Transformers` 发现 DiT 条件嵌入存在极端对齐和稀疏有效维度。虽然该论文主要是图像/连续条件扩散分析，但它支持一个保守判断：

```text
仅靠一个 global condition vector 注入复杂语义，可能存在结构性瓶颈。
```

这与 MoLingo / COME 中 cross-attention 优于 AdaLN 的观察一致。对 T2M 来说，复杂 prompt 不应只变成一个全局向量，而应保留：

1. event tokens；
2. phrase / part tokens；
3. chunk-wise motion tokens；
4. token-patch late interaction。

### 4.3 ACCORD: alignment 可以写成 dependence regularization

外部 ICLR_2026 note `ACCORD` 把 T2I personalization 的概念耦合形式化为统计依赖偏差，并在 denoising steps 上约束依赖变化。

对 MLPA 的迁移不是照搬公式，而是借鉴问题形式：

```text
text event 与 wrong chunk / wrong body part 的虚假依赖，
可以被定义为 alignment dependence bias。
```

后续可以设计诊断：

1. event 与对应 chunk 的依赖应高于非对应 chunk；
2. event 与错误 body part 的依赖不应随 denoising 放大；
3. drop / replace / shuffle counterfactual 不应被 global embedding 洗掉。

这能把“对齐不好”从主观描述变成可度量的 dependence / counterfactual probe。

### 4.4 A2D: alignment signal 应下沉到 token/span 级

外部 ICLR_2026 note `A2D` 的直接任务是 dLLM safety alignment，但它的泛化启发很强：response-level alignment 太浅，token/span-level target 更稳。

迁移到 T2M：

```text
sequence-level text-motion alignment 太浅；
event / phrase / chunk / part-level alignment 才能覆盖任意位置的局部失败。
```

这支持把 alignment 从 full sequence score 下沉到：

1. event span；
2. body-part phrase；
3. time chunk；
4. contact / root cue；
5. counterfactual local replacement。

## 5. 当前本库诊断如何支撑

### 5.1 TAMR 的负结果很关键

[[ideas/TAMR/ROADMAP|TAMR Roadmap]] 已经记录：training-time event alignment 路线基本证伪，`evt_align loss` 与 global retrieval loss 存在梯度冲突，当前转向 inference-time structured rerank。

这对 MLPA 是强约束：

```text
MVP 不应一上来把 event alignment loss 塞进 generator 或 retrieval backbone。
```

更合适的顺序是：

1. 冻结 text / motion encoder；
2. 训练轻量 alignment head；
3. 做 structured rerank；
4. 只在 rerank / timestamping 有正信号后，再考虑 representation training 或 generator tuning。

### 5.2 MoDebug P1 是诊断压力轴，不是最终证据

[[paperIDEAs/MoDebug/experiments/p1_event_transfer_20260516/results/task1_summary|MoDebug P1 task1 summary]] 记录：

1. P1 覆盖 10 个 sample、30 个 decomposed event、30 条 single-event prompt。
2. CLIP 文本侧 full-vs-single distance 随 event_count 增大：event_count 1 均值 `0.0022`，event_count 5 均值 `0.1223`。
3. DistilBERT / T5 / FLAN-T5 复查也支持 event_count 增加会增大文本侧压力的弱趋势。
4. Qwen3-32B mean pooling coverage 不足，不能作为主排序证据。
5. 所有这些结果角色都是 `diagnostic` 或 `cross_check`，用途是 `observation`。

因此这组结果只能支持：

```text
multi-event prompt 确实给 pooled text embedding 造成可观压力；
event_count 可作为后续 alignment stress axis。
```

不能支持：

```text
某个 generator 一定保留或丢失了 event；
event embedding 已经在 motion 中被正确执行；
CLIP/T5 distance 可以当 final evaluator。
```

## 6. 方法框架：MLPA

### 6.1 One-Sentence Claim

```text
We propose Multi-Level Pivot Alignment, a frozen-encoder correspondence layer
that uses frame labels, text events, part phrases, and motion chunk-part tokens
as pivots to localize and score text-motion alignment before generator retraining.
```

中文表述：

```text
MLPA 不是新的 motion generator，而是一个先于或外挂于 generator 的多级 correspondence layer；
它把 frame label / event / part phrase / chunk-part motion token 作为多级 pivot，
先做可审计的局部对齐，再决定 rerank、timestamping 或局部修正。
```

### 6.2 输入输出

输入：

```text
full caption
generated or GT motion
optional candidate set
optional BABEL / FineMotion / HumanML3D-E side labels
```

中间结构：

```text
text:
  global caption embedding
  event embeddings
  part phrase embeddings
  duration / frequency / order attributes

motion:
  global sequence token
  temporal chunk tokens
  body-part grouped tokens
  root / contact / velocity channels

pivots:
  BABEL action segment labels
  HumanML3D-E decomposed events
  FineMotion time-part descriptions
  generated pseudo event spans
```

输出：

```text
event ↔ chunk alignment matrix
phrase ↔ body-part chunk alignment matrix
monotonic event path
span confidence / ambiguity
rerank score or timestamp proposal
```

### 6.3 两种 MVP 形态

**MVP-A: Event-Guided Motion Timestamping**

```text
HumanML3D-E ordered text events
→ render / slice GT motion
→ event-conditioned judge gives present / absent / transition scores
→ monotonic DP / soft OT outputs event spans
→ human audit + BABEL/FineMotion calibration
```

优点：贡献像数据接口，不依赖 generator 改造；能直接补 HumanML3D-E 的 motion-side span 缺口。

**MVP-B: Frozen MLPA Rerank**

```text
generator outputs K candidates
→ frozen text/motion encoder extracts event and chunk-part tokens
→ late interaction + monotonic path scoring
→ rerank candidates
→ compare with global score rerank and equal-split baseline
```

优点：工程成本低，能直接验证“多级 correspondence 是否比 global score 有用”。

我更建议先做 MVP-A，再接 MVP-B。原因是：如果 motion-side event timestamp 都不可靠，rerank score 的解释性会很脆弱。

## 7. 对齐算子设计

### 7.1 粗定位

目标：快速找 event 可能出现在哪些 motion chunks。

候选实现：

1. equal-duration split baseline；
2. CLIP/TMR/LaMP text-motion chunk similarity；
3. rendered skeleton VLM judge；
4. A.I.R.-style adaptive threshold + local expansion；
5. root/contact heuristic for locomotion / stop-go / jump / turn。

粗定位只产生 candidates，不直接当证据。

### 7.2 细匹配

目标：在候选 chunks 内做 event / phrase / part token 局部匹配。

可选算子：

```text
event × chunk cosine matrix
part_phrase × body_part_chunk matrix
MaxSim token-patch late interaction
soft OT for event-to-time mass allocation
monotonic DP for ordered events
parallel-aware relaxation for overlap cues
```

这里的直接证据来自 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]] 和 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]。它们说明 retrieval 侧的 joint/segment/global pyramid 和 token-patch late interaction 已经比 global embedding 更适合细粒度匹配。

### 7.3 约束

```text
ordered events → monotonic path
parallel events → relaxed overlap or shared chunk
duration attributes → span length prior
frequency attributes → repeated subspan count prior
body-part phrases → sparse body group prior
root/contact verbs → root/contact channel prior
```

注意：这些都是 prior，不是 final evaluator。

## 8. DeepSeek Max 评审摘要

后续又把同一想法交给 5 个顾问视角，完整保存在 [[2026-05-19_multi-agent-consultation-and-molingo-audit|multi-agent consultation and MoLingo audit]]。这里保留对主线有影响的收敛结论。

五个顾问的共同点：

1. L1 不应写成字面 shared latent space，更稳的表述是 `shared semantic factors + modality-private residuals`。
2. pivot 不应写成几何点，而应是 `event × temporal span × body part × attribute/contact` 的局部结构。
3. 第一版不要做大生成器或 3DGS / tri-plane 类比主线；先做 local verifier / timestamping / rerank / guidance。
4. 现有工作已经占住 semantic latent、frame-level plan、part-time control、symbolic plan、PST / MaxSim late interaction，因此 novelty 必须落在 generation-oriented correspondence layer 和验证协议上。

这次与 DeepSeek Max 做了两次交流：

1. 第一次完整长 prompt 调用 120 秒超时，没有返回可用内容。
2. 第二次压缩 prompt 返回了 novelty / gate 评审。

DeepSeek 的核心意见：

1. 最强支撑是 MoLingo 提供 pivot 原型、ActionPlan/FineXtrol 等证明分层结构有效、TAMR/PST/MaxSim 支持 frozen rerank 而不是早期 training-time loss。
2. 不能 claim 新生成范式、不能 claim 标签免费、不能 claim DP/OT/MaxSim 算子原创、不能 claim 解决全部 T2M alignment。
3. 推荐命名 `Multi-Level Pivot Alignment for Text-Motion Rerank`，最小贡献是冻结 T2M 编码器上的多级 pivot alignment head / rerank。
4. 优先 gate 包括 rerank Recall@K、部位短语 probe、冻结编码器假设检验、后续 generator 微调回归、OOD 弱监督迁移。
5. 最危险句子是“解决 text-to-motion alignment 并直接生成高质量运动”；替换为“在不重新训练生成器的前提下，提升已有模型候选的文本-运动语义一致性”。

我采纳其中两点作为硬边界：

```text
MLPA first = rerank / timestamp / correspondence layer
MLPA later = generator conditioning or reward-guided local refinement
```

MoLingo 4090 配置审计也记录在 companion note 中。2026-05-20 更新后，`HumanML3D_272` 已从 4090 的 datasets 目录软链接到 MoLingo 默认数据路径，`babel_272_annotation_t5` 已由本地 zip 上传并解压到同一数据根目录。272D dataset loader、1-prompt generation smoke、`Text2MotionDatasetMSBabel` train/val loader smoke 已通过；但 SAE retraining 和 standard full benchmark eval 尚未运行，只能说入口、checkpoint、evaluator 配置、dataset loader、SAE 数据前置条件和 diagnostic generation smoke 已验证。

## 9. 实验 Gate

### Gate 1: Text event 是否比 full prompt 更适合局部匹配

问题：

```text
event embedding 与对应 motion chunk 是否比 full caption embedding 更能区分局部动作？
```

验证：

1. BABEL / FineMotion / HumanML3D-E timestamped subset；
2. event ↔ chunk positive vs negative similarity；
3. correct order vs shuffled order；
4. equal split vs recovered span。

通过标准：

```text
event-to-correct-chunk AUC / R@K 明显高于 global-caption-to-chunk baseline；
reverse / shuffle order sanity 显著低于 correct order。
```

### Gate 2: Body-part phrase 是否真的定位到对应 body-part token

问题：

```text
“left arm raises” 是否定位到 left arm chunks，而不是全身平均变化？
```

验证：

1. FineMotion 的 `body part × temporal interval` 标注；
2. FrankenMotion-style part labels 作为 side check；
3. part phrase ↔ body group score matrix；
4. mask wrong body group / corrupt correct body group 反事实。

通过标准：

```text
correct part group score > wrong group score；
mask correct part 的 score drop 大于 mask irrelevant part。
```

### Gate 3: Timestamping 是否优于 equal-duration split

问题：

```text
从 HumanML3D-E ordered events 恢复的 motion spans 是否比等长切分更可信？
```

验证：

1. 100-200 条 K>=3 HumanML3D-E GT motion；
2. 0.5s / 1.0s sliding slice；
3. VLM / motion-language judge 打 present / transition / absent；
4. monotonic DP / OT 输出 span；
5. 人工审计 50-100 个 event spans。

通过标准：

```text
boundary IoU / start-end error / coverage / ambiguous rate
优于 equal split 和 score-only baseline。
```

### Gate 4: Frozen rerank 是否提升 candidate selection

问题：

```text
不重训 generator，只 rerank K candidates，能否提升 human-audited alignment？
```

验证：

1. 选择 MoMask / Event-T2M / MoLingo candidates；
2. global retrieval score rerank；
3. MLPA structured score rerank；
4. human pairwise preference 或 heldout event satisfaction audit。

通过标准：

```text
MLPA rerank 的 event satisfaction / order correctness 高于 global rerank；
FID / diversity 不显著退化。
```

### Gate 5: Training-time loss 是否真的不应提前进入

问题：

```text
alignment loss 会不会复现 TAMR 中的 global retrieval conflict？
```

验证：

1. frozen head；
2. partial fine-tune；
3. generator alignment fine-tune；
4. 同时监控 global retrieval、structured score、FID、diversity、human/event audit。

通过标准：

```text
只有当 frozen / partial 都有稳定正信号时，才允许 generator training；
若 global score 或 FID 明显退化，退回 rerank。
```

## 10. Novelty 边界

### 可以 claim

1. **多级 pivot framing**：把 frame labels、events、part phrases、chunk-part tokens 统一为 correspondence pivots。
2. **可审计 correspondence layer**：输出 event ↔ chunk、phrase ↔ body-part 的 alignment，而不是只给全局分数。
3. **HumanML3D-E event timestamping**：若做成，可补 ordered text events 的 motion-side span 缺口。
4. **frozen-first protocol**：先验证 correspondence / rerank，避免把未验证 alignment loss 塞进 generator。
5. **cross-domain query-aware evidence acquisition**：把 A.I.R.-style iterative verification 用于 motion event span discovery。

### 不能 claim

1. 不能说首次在 motion representation 注入语义。
2. 不能说首次提出 event-level motion generation。
3. 不能说首次提出 body-part temporal control。
4. 不能说 frame labels 能完整描述全身动作。
5. 不能说 MLLM / CLIP / T5 diagnostic 是 final evaluator。
6. 不能说无监督或标签免费。
7. 不能说 DP / OT / MaxSim 是新算法。
8. 不能说 rerank 等价于 generator 本身 alignment 被解决。

## 11. 推荐写法

危险写法：

```text
We solve text-motion alignment by introducing multi-level semantic pivots into motion generation.
```

替换写法：

```text
We introduce a multi-level pivot correspondence layer that localizes
which text events and body-part phrases are supported by which motion chunks.
In the first stage, we use it for timestamping and reranking without retraining the generator;
only after this correspondence layer is validated do we consider generation-time conditioning or refinement.
```

中文写法：

```text
本文不直接声称解决整个 text-to-motion alignment，
而是先补上一个缺失的中间层：
text event / part phrase 到 motion chunk / body-part token 的可审计对应关系。
```

## 12. 最小路线建议

### Week 1: Timestamping

```text
Data:
  HumanML3D-E K>=3 GT motions, 100-200 samples

Processing:
  render sliding slices
  event-conditioned present / absent / transition judge
  monotonic DP / soft OT span assignment

Baselines:
  equal split
  global TMR/T5 score only
  no monotonic constraint

Outputs:
  event span TSV
  ambiguity labels
  audit sheet
```

### Week 2: Frozen MLPA Rerank

```text
Input:
  generated candidate motions from existing models

Score:
  global score
  event-chunk score
  part-phrase-body score
  monotonic path score

Evaluation:
  human heldout pairwise preference
  event satisfaction audit
  order correctness
  no regression on FID / diversity
```

### Stop Conditions

停止或降级路线的条件：

1. timestamp span 不优于 equal split；
2. body-part phrase 无法定位对应 body group；
3. MLPA rerank 不优于 global score；
4. frozen head 完全无效且 partial fine-tune 过拟合；
5. human audit 与 automatic score 大幅不一致。

## 13. 当前结论

你的想法可以成立，但需要从“再发明一个更强 generator”降维成：

```text
先建立 text-motion 的多级 correspondence layer。
```

最稳主线：

```text
MoLingo 的 frame-level label pivot
→ Event-T2M 的 event condition
→ FineXtrol / FrankenMotion 的 part-time supervision
→ PST / MaxSim / TAMR 的 late interaction and structured matching
→ A.I.R.-style query-aware verification
→ MLPA: event-time-part correspondence layer
```

它的价值不在于每个组件单独新，而在于把这些组件放进一个可验证的 staged alignment protocol：

```text
Stage 0: timestamp / pseudo-span discovery
Stage 1: frozen correspondence head
Stage 2: structured rerank
Stage 3: optional generator conditioning / local refinement
```

如果第一阶段能证明 HumanML3D-E 的 ordered events 可以被补成可信 motion timestamps，并且 frozen MLPA score 能优于 global rerank，那么这个方向就有足够强的后续扩展空间。

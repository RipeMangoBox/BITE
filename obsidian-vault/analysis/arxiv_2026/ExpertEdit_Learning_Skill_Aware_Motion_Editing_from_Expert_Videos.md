---
title: "ExpertEdit: Learning Skill-Aware Motion Editing from Expert Videos"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos.pdf
project_link: https://vision.cs
code_link: null
aliases:
- ExpertEdit
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入运动学掩码的上下文运动填充：仅在无配对专家视频上训练带掩码的运动语言模型，学习在技能关键时刻恢复被掩盖的专家运动片段；推理时，自动发现新手运动的技能关键时刻并掩码，由同一模型填充专家化的关节旋转，从而实现无编辑指导的局部技能提升。
primary_logic: 将技能精炼转化为上下文运动填充任务，利用运动学峰值（速度/加速度等）自动发现技能关键时刻。通过掩码语言建模（MLM）仅学习重建被掩盖的专家运动片段，模型习得专家运动流形；推理时，仅需将新手运动的相应相位投影到该流形，即可在完全保留运动路径和节奏的前提下生成专家级的关节旋转。
claims:
- ExpertEdit仅从无配对专家视频训练，无需配对监督或显式编辑指导，推理时自动确定编辑时机和方式。
- 在Ego-Exo4D和Kyokushin Karate的8种技术中，ExpertEdit在运动真实性和专家质量（P和F指标）上显著优于TMED、SimMotionEdit和FLAME等监督基线。
- 通过运动学掩码和双向Transformer的MLM训练，模型能够有效填充专家运动的关键技能片段，习得专家运动先验。
- 仅使用30%的专家数据训练时性能仍有正增益，随无配对专家数据量增加，编辑性能持续提升。
---

# ExpertEdit: Learning Skill-Aware Motion Editing from Expert Videos

> [!tip] 核心洞察
> 将技能精炼转化为上下文运动填充任务，利用运动学峰值（速度/加速度等）自动发现技能关键时刻。通过掩码语言建模（MLM）仅学习重建被掩盖的专家运动片段，模型习得专家运动流形；推理时，仅需将新手运动的相应相位投影到该流形，即可在完全保留运动路径和节奏的前提下生成专家级的关节旋转。

| 字段 | 内容 |
|------|------|
| 中文题名 | ExpertEdit：从专家视频中学习技能感知的运动编辑 |
| 英文题名 | ExpertEdit: Learning Skill-Aware Motion Editing from Expert Videos |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10466) · [Project](https://vision.cs) · [paper](https://arxiv.org/abs/2408) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ExpertEdit |
| Dataset | Penalty Kick, Front Kick |

> [!tip] 效果简介
> - Penalty Kick (Ego-Exo4D) 上，FID Improvement (F) 9.14% vs 3.46% (FLAME) (+5.68 percentage points)。
> - Front Kick (Kyokushin Karate) 上，FID Improvement (F) 9.73% vs 4.32% (TMED) (+5.41 percentage points)。

## 概要

**问题瓶颈**：现有运动编辑方法依赖配对的新手–专家数据或显式的文本/参考编辑指导，无法在无配对监督下自动将新手运动精炼为专家级表现；同时，技能领域缺乏大规模配对的新手–专家运动数据和专家标注。

**核心思路**：ExpertEdit 将技能精炼转化为**上下文运动填充**任务。训练时，仅在无配对专家视频上使用掩码语言建模（MLM）学习重建被掩盖的专家运动片段，使模型习得专家运动流形；推理时，通过运动学峰值自动发现新手运动的技能关键时刻并掩码，由同一模型填充专家化的关节旋转，在完全保留原始运动路径和节奏的前提下实现局部技能提升。

**方法定位**：ExpertEdit 属于**无配对监督、无编辑指导的运动编辑方法**，与依赖文本条件或参考运动的监督基线（如 TMED、SimMotionEdit、FLAME）形成根本差异。其核心机制是双向 Transformer 的上下文运动填充，而非扩散去噪或文本条件生成。

**主要结果**：在 Ego-Exo4D（篮球、足球）和 Kyokushin Karate 的 8 种运动技术上，ExpertEdit 在运动真实性和专家质量（P 和 F 指标）上显著优于所有监督基线。例如，点球（Penalty Kick）的 FID 改善达 9.14%，约为最佳基线 FLAME（3.46%）的 2.6 倍；前踢（Front Kick）的 FID 改善达 9.73%，而 TMED 和 SimMotionEdit 分别为 4.32% 和 6.11%。消融实验表明，编辑性能随无配对专家数据量增加而持续提升。

### 问题背景：从新手到专家的运动技能鸿沟

在体育训练、康复医疗和技能学习等应用中，运动编辑技术旨在将非专业人士（新手）的3D人体运动序列自动精炼为更接近专家水准的表现。这一任务的核心挑战在于：**技能差异往往高度局部化**——新手与专家的整体运动路径和节奏可能相似，但在关键动作阶段（如篮球投篮的出手瞬间、空手道踢击的发力点）的姿态精准度和力学效率存在显著差距。因此，理想的运动编辑方法应当能够在保留原始运动路径和节奏的前提下，仅对技能关键时刻的关节旋转进行局部优化，生成既保持个人执行特征又具备专家品质的运动序列。

### 现有方法的瓶颈：对配对监督和显式编辑指导的依赖

当前主流的运动编辑方法面临两个根本性限制：

**第一，对配对监督的强依赖。** 现有方法（如**TMED**、**SimMotionEdit**、**FLAME**）通常需要在配对的新手-专家运动数据上进行训练或微调。然而，在真实技能学习场景中，大规模获取高质量的新手-专家配对数据极其困难：需要同一动作由新手和专家分别执行，并通过时间对齐建立帧级对应关系。这一数据获取成本限制了方法在多样化运动技能上的可扩展性。

**第二，对显式编辑指导的依赖。** 现有方法在推理时需要文本提示或参考运动来指定编辑意图（例如“让投篮动作更流畅”），这要求用户具备明确的编辑知识，且文本描述往往难以精确刻画技能改进的细微姿态调整。此外，文本条件方法在技能编辑任务上的性能高度依赖提示词设计——实验证据表明，直接要求“expert-like motion”的提示反而比鼓励“smoothness and control”的通用提示表现更差（见Suppl. Table 3），揭示了文本指导与技能精炼目标之间的语义鸿沟。

### 核心动机：从专家观察中隐式学习技能先验

ExpertEdit的提出基于一个关键观察：**人类通过观察专家示范即可理解技能的关键要素，无需显式的对比标注或语言指导**。这一认知启发我们重新思考运动编辑的学习范式——能否仅从无配对的专家运动视频中学习专家运动流形，并在推理时自动发现新手运动中的技能缺陷并进行修复？

这一思路将运动技能编辑转化为一个**上下文运动填充（contextual motion infilling）**问题：训练阶段，模型在专家运动序列上学习重建被掩码的技能关键片段，从而隐式习得专家运动的先验分布；推理阶段，模型自动识别新手运动的技能关键时刻并将其掩码，然后利用学到的专家先验填充出专家化的关节旋转。整个过程无需配对监督、无需文本或参考运动指导，实现了从“被动接受编辑指令”到“主动发现并修复技能缺陷”的范式转变。

## 核心方法与创新机理

ExpertEdit 的核心创新在于将**运动技能精炼**重新定义为**上下文运动填充**任务，从而彻底绕过了现有方法对配对监督和显式编辑指导的依赖。这一范式转换通过三个相互耦合的机制实现，形成了从数据需求到推理方式的系统性改变。

### 从配对监督到无配对专家学习的范式转换

现有运动编辑方法（如 **TMED**、**SimMotionEdit**、**FLAME**）均依赖某种形式的配对监督：TMED 和 SimMotionEdit 需要在目标数据集上使用约 16k 对齐的新手-专家伪对进行微调，FLAME 则需要文本描述或参考运动作为编辑条件。ExpertEdit 从根本上改变了这一数据范式——**训练仅使用无配对的专家运动片段**，无需任何新手-专家对应关系或人工标注的编辑指导。这一改变的深层原因在于：技能领域天然缺乏大规模配对数据，而专家视频相对容易获取（Ego-Exo4D 数据集包含超过 24k 专家视频片段）。通过仅在专家运动上训练，模型习得的是专家运动的流形先验，而非从新手到专家的显式映射函数。

### 从显式编辑指导到自动技能关键时刻发现

推理阶段的编辑指导是另一个关键差异点。基线方法需要文本提示（如“Make the motion smoother and more controlled”）或参考运动来指定编辑目标和位置，而 ExpertEdit 通过**运动学掩码**实现了完全自动的编辑时机确定。其核心机制是计算运动学信号 $h(t)$（基于速度、加速度等物理量），并选取其峰值帧作为技能关键时刻：

$$t^{*} = \arg\max_{t\in\{1,\dots,T\}} h(t)$$

推理时，模型自动以 $t^*$ 为中心掩码新手运动的关键片段，由训练好的 MotionInfiller 填充专家化的关节旋转，其余帧完全保留原始运动。这意味着**编辑的位置和方式均由模型自主决定**，无需任何形式的文本、提示或参考输入。

### 从条件生成到掩码语言建模的编辑机制

编辑机制本身也发生了根本变化。基线方法采用文本条件的扩散去噪或编码器-解码器变换，而 ExpertEdit 使用**双向 Transformer 的掩码语言建模**来填充被掩码的运动片段。训练目标为交叉熵损失：

$$\mathcal{L}_{\mathrm{MLM}} = -\sum_{i=t^*-h}^{t^*+h} \log p_\theta(k_i^{\mathrm{exp}} \mid \mathbf{k}_{\setminus[t^*-h:t^*+h]}^{\mathrm{exp}})$$

这一设计的关键优势在于：模型必须根据未掩码的上下文（即运动的前后阶段）推断出被掩码的技能关键片段，从而学习到**上下文一致的专家运动先验**。推理时，仅需将新手运动的相应相位投影到该专家流形，即可在完全保留原始运动路径和节奏的前提下生成专家级的关节旋转——编辑后的每帧由复制的根平移与根方向以及精炼后的关节旋转组成：

$$\mathbf{X}_t^{\mathrm{edit}} = ( \mathbf{r}_t, \mathbf{o}_t, \hat{\mathbf{p}}_t )$$

### 创新点的协同效应

上述三个 changed slots 并非孤立存在，而是形成了因果链条：无配对专家学习使得模型能够习得纯粹的专家运动先验；运动学掩码提供了无需外部指导的技能关键相位定位；MLM 填充机制则将技能精炼转化为上下文一致的流形投影问题。这一协同效应在实验中得到验证：ExpertEdit 在仅使用 30% 专家数据训练时仍保持正增益，且性能随无配对专家数据量增加持续提升，而基线方法即使获得额外的配对监督微调，在所有 8 种技术上的运动真实性和专家质量指标上仍被 ExpertEdit 显著超越（例如罚球技术上 FID 改善达 9.14%，约为最佳基线 FLAME 的 2-4 倍）。

ExpertEdit 将技能驱动的运动编辑重新定义为一个**上下文运动填充（contextual motion infilling）**问题，其核心洞察是：专家与新手之间的技能差异主要集中在动作的特定关键时刻，而非整个运动序列。基于此，整个 pipeline 围绕“发现关键时刻 → 掩码 → 专家化填充”的范式构建。

### 输入输出约定

系统接受从单目视频中提取的 3D 人体运动序列作为输入，序列由 $T$ 帧组成，每帧表示为：

$$\mathbf{X} = \{ ( \mathbf{r}_t, \mathbf{o}_t, \mathbf{p}_t ) \}_{t=1}^T$$

其中 $\mathbf{r}_t$ 为全局平移，$\mathbf{o}_t$ 为根关节朝向，$\mathbf{p}_t$ 为关节旋转。编辑过程仅对关节旋转 $\mathbf{p}_{1:T}$ 进行精炼，**完整保留**原始序列的全局运动路径（$\mathbf{r}_t$）和身体朝向（$\mathbf{o}_t$），从而确保编辑后的运动在空间轨迹和节奏上与原始执行保持一致。编辑后的帧构造为：

$$\mathbf{X}_t^{\mathrm{edit}} = ( \mathbf{r}_t, \mathbf{o}_t, \hat{\mathbf{p}}_t )$$

其中 $\hat{\mathbf{p}}_t$ 为精炼后的关节旋转。

### Pipeline 三大模块

ExpertEdit 由三个核心模块串联构成，如 Fig. 2 所示：

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2604_10466/figures/002_Figure_2.jpg]]
*Figure 2: ExpertEdit approach. We tokenize expert pose motion sequences and mask the key action phase as determined by task-specific kinematic criteria. We train a bi-directional transformer, MotionInfiller, to predict the expert pose tokens at the masked positions. At inference, we mask skill-critical action phases in a novice motion (see Sec. 4) and infill these regions with expert-like motion*

**1. Pose Tokenizer（姿态分词器）**  
采用基于 Transformer 的因果 VQ-VAE，将连续的专家运动帧编码为离散的运动令牌（motion tokens）。编码器以因果自注意力机制处理历史帧，生成当前帧的潜在向量 $\mathbf{z}_t$：

$$\mathbf{z}_t = E_\phi(\mathbf{x}_{\leq t}^{\exp}) = f_{\mathrm{enc}}(\mathbf{x}_t^{\exp}, \mathrm{Attn}_{\mathrm{causal}}(\mathbf{x}_{<t}^{\exp}))$$

随后通过最近邻查找将 $\mathbf{z}_t$ 量化为码本条目 $\mathbf{e}_{k_t^*}$，再由因果解码器重建帧。该模块将连续运动转化为离散符号序列，为后续的掩码语言建模提供统一的令牌空间。

**2. Kinematic Phase Selector（运动学相位选择器）**  
该模块负责**自动发现技能关键时刻**，无需人工标注。它计算一个标量运动学信号 $h(t)$（如关节速度或加速度的聚合值），并选取其峰值帧作为掩码中心：

$$t^{*} = \arg\max_{t\in\{1,\dots,T\}} h(t)$$

这一设计的因果逻辑是：运动学峰值（速度/加速度极值点）往往对应动作中力量爆发、姿态转换等技能敏感相位——例如投篮时的出手瞬间、踢球时的触球帧。以 $t^*$ 为中心，向两侧扩展固定窗口形成掩码区间。

**3. MotionInfiller（运动填充器）**  
这是一个双向 Transformer（BERT 架构），以掩码语言建模（MLM）目标进行训练。训练时，模型接收被掩码的专家运动令牌序列，仅根据未掩码的上下文预测被掩盖的技能关键片段：

$$\mathcal{L}_{\mathrm{MLM}} = -\sum_{i=t^*-h}^{t^*+h} \log p_\theta(k_i^{\exp} \mid \mathbf{k}_{\setminus[t^*-h:t^*+h]}^{\exp})$$

这一交叉熵损失迫使模型学习专家运动的流形先验——在给定动作前后文的情况下，推断出符合专家水平的关节旋转过渡。训练**仅使用无配对的专家视频**，无需任何新手-专家对齐数据。

### 推理流程

推理时，系统将训练好的 Pose Tokenizer 和 MotionInfiller 串联使用：

1. **分词**：将新手运动序列通过 Pose Tokenizer 转化为离散令牌序列。
2. **自动掩码**：由 Kinematic Phase Selector 计算运动学信号，确定技能关键时刻 $t^*$，掩码该时刻附近的令牌。
3. **专家化填充**：将部分掩码的令牌序列输入 MotionInfiller，模型基于习得的专家运动先验，在掩码位置生成专家水平的关节旋转令牌。
4. **重建**：将填充后的令牌序列解码为连续关节旋转 $\hat{\mathbf{p}}_{1:T}$，并与原始 $\mathbf{r}_t$、$\mathbf{o}_t$ 组合，得到编辑后的运动序列。

整个过程**无需文本提示、参考运动或任何显式编辑指导**——模型自动决定“在哪里编辑”（运动学峰值检测）和“如何编辑”（上下文填充）。值得注意的是，系统为每种运动技术（如罚球、回环上篮、前踢等）**独立训练** Pose Tokenizer 和 MotionInfiller，以学习技术特定的专家运动先验，这是当前方法的一个结构性限制。

ExpertEdit 将技能驱动的运动编辑形式化为**上下文运动填充**任务，其核心架构由三个紧密协作的模块构成：姿态分词器、运动填充器与运动学相位选择器。图2展示了整体流程：训练时，专家运动序列经分词器离散化后，在运动学峰值周围进行掩码，由双向Transformer学习重建被掩码的专家令牌；推理时，新手运动的技能关键相位被自动掩码，同一模型填充专家化的关节旋转。

### 3.1 姿态分词器（Pose Tokenizer）

姿态分词器采用基于Transformer的VQ-VAE架构，将连续的运动姿态编码为离散的专家运动令牌，为后续的掩码语言建模提供离散化基础。

**输入表示**：运动序列表示为每帧的全局平移、根方向与关节旋转的组合：
$$\mathbf{X} = \{ ( \mathbf{r}_t, \mathbf{o}_t, \mathbf{p}_t ) \}_{t=1}^T$$
其中 $\mathbf{r}_t \in \mathbb{R}^3$ 为全局平移，$\mathbf{o}_t \in \mathbb{R}^6$ 为根方向（6D连续表示），$\mathbf{p}_t \in \mathbb{R}^{3J}$ 为 $J$ 个关节的旋转向量，$T$ 为总帧数。

**编辑映射**：ExpertEdit 学习一个从输入关节旋转到精炼关节旋转的映射函数，仅编辑关节旋转而保留原始运动路径与根方向：
$$\mathcal{F}_{\boldsymbol{\theta}} : \mathbb{R}^{T \times 3J} \to \mathbb{R}^{T \times 3J}, \quad \hat{\mathbf{p}}_{1:T} = \mathcal{F}_{\boldsymbol{\theta}}(\mathbf{p}_{1:T})$$
编辑后的每帧由复制的根平移、根方向与精炼后的关节旋转组成：
$$\mathbf{X}_t^{\mathrm{edit}} = ( \mathbf{r}_t, \mathbf{o}_t, \hat{\mathbf{p}}_t )$$

**因果编码器**：编码器 $E_\phi$ 采用因果自注意力机制，仅基于当前及历史帧生成潜在向量，保证时序因果性：
$$\mathbf{z}_t = E_\phi(\mathbf{x}_{\leq t}^{\exp}) = f_{\mathrm{enc}}(\mathbf{x}_t^{\exp}, \mathrm{Attn}_{\mathrm{causal}}(\mathbf{x}_{<t}^{\exp}))$$

**量化与重建**：潜在向量 $\mathbf{z}_t$ 通过最近邻查找映射到可学习的码本 $\{\mathbf{e}_k\}_{k=1}^K$ 中的最近条目，再由因果解码器 $D_\phi$ 重建帧：
$$k_t^* = \arg\min_k \|\mathbf{z}_t - \mathbf{e}_k\|_2^2, \quad \hat{\mathbf{x}}_t = D_\phi(\mathbf{e}_{k_t^*})$$

**VQ-VAE损失**：训练目标为标准VQ-VAE的三项损失之和——重构损失、码本损失与承诺损失：
$$\mathcal{L}_{\mathrm{VQ}} = \|\mathbf{x}_t^{\mathrm{exp}} - \hat{\mathbf{x}}_t\|_2^2 + \|\mathrm{sg}[E_\phi(\mathbf{x}_{\leq t}^{\mathrm{exp}})] - \mathbf{e}_{k_t^*}\|_2^2 + \beta\|E_\phi(\mathbf{x}_{\leq t}^{\mathrm{exp}}) - \mathrm{sg}[\mathbf{e}_{k_t^*}]\|_2^2$$
其中 $\mathrm{sg}[\cdot]$ 为停止梯度算子，$\beta$ 为承诺损失权重。

### 3.2 运动填充器（MotionInfiller）

运动填充器是一个BERT风格的双向Transformer，通过掩码语言建模目标学习在技能关键时刻恢复被掩盖的专家运动片段。其核心机制如下：

**运动学掩码策略**：与自然语言处理中的随机掩码不同，ExpertEdit 将掩码窗口精确地以运动学峰值帧为中心。给定一个运动学信号 $h(t)$（如速度或加速度的范数），技能关键时刻定义为该信号的峰值帧索引：
$$t^{*} = \arg\max_{t\in\{1,\dots,T\}} h(t)$$
以 $t^*$ 为中心，掩码一个宽度为 $2h$ 的窗口 $[t^*-h, t^*+h]$ 内的所有令牌。这种策略确保模型专注于学习技能执行最关键的相位（如投篮出手瞬间、踢球触球点等），而非无关的过渡帧。

**MLM训练目标**：运动填充器 $\theta$ 以交叉熵损失学习根据未掩码的上下文令牌 $\mathbf{k}_{\setminus[t^*-h:t^*+h]}^{\exp}$ 预测被掩码的专家运动令牌：
$$\mathcal{L}_{\mathrm{MLM}} = -\sum_{i=t^*-h}^{t^*+h} \log p_\theta(k_i^{\mathrm{exp}} \mid \mathbf{k}_{\setminus[t^*-h:t^*+h]}^{\mathrm{exp}})$$
该损失鼓励网络推断上下文一致的运动，生成平滑且生物力学上有效的过渡，从而习得特定技术的专家运动流形。

**技术特定训练**：为每种运动技术（如反身上篮、点球等）单独训练姿态分词器与运动填充器，以学习特定技术的强专家运动先验。这一设计选择源于不同技术的运动学特征和技能关键相位存在显著差异。

### 3.3 推理时的技能编辑

推理时，ExpertEdit 无需任何文本提示、参考运动或配对监督。给定一段新手运动序列，系统自动计算其运动学信号 $h(t)$ 并定位技能关键时刻 $t^*$，在该时刻周围掩码相应的令牌窗口。运动填充器基于未掩码的上下文（即新手运动的非关键帧）预测被掩码位置的专家级运动令牌，再由姿态分词器的解码器重建为连续的关节旋转。最终，编辑后的关节旋转与原始根平移、根方向组合，生成完整的编辑运动序列。这一过程将新手运动的技能关键相位“投影”到专家运动流形上，在完全保留原始运动路径和节奏的前提下实现局部技能提升。

### 补充图表

## 实验与关键发现

### 核心实验设置

ExpertEdit 在三个运动类别、八种技术动作上进行了系统评估，覆盖 **Ego-Exo4D** 数据集（篮球：Mikan 上篮、Reverse 上篮、Jump Shot 跳投；足球：Penalty Kick 点球）和 **Kyokushin Karate** 数据集（Front Kick 前踢、Roundhouse Kick 回旋踢、Spin Back Kick 后旋踢、Side Kick 侧踢）。评估的关键在于构造高质量的**时间对齐的新手-专家测试对**：对每个裁剪后的新手片段，通过元数据相似度检索 $k=3$ 个同技术专家片段，经 DTW 对齐后由领域专家人工校验，最终保留率分别为篮球 83% 和足球 77%，确保评估的可靠性。

两个核心评估指标从不同维度衡量编辑质量：
- **Pose Improvement (P)**：相对 PA-MPJPE 改善率，$$P(\%) = \frac{\text{PA-MPJPE}_{\text{novice}} - \text{PA-MPJPE}_{\text{gen}}}{\text{PA-MPJPE}_{\text{novice}}} \times 100$$，衡量编辑后姿态与专家参考在 Procrustes 对齐下的几何接近程度；
- **FID Improvement (F)**：相对 FID 改善率，衡量编辑后运动的分布与专家运动分布的对齐程度，反映运动真实性和专家质量。

基线方法包括三类代表性运动编辑模型：**TMED**（基于 Diffusion Transformer，在 MotionFix 上训练，需文本条件和配对微调）、**SimMotionEdit**（文本条件运动编辑模型，在新手-专家伪对上微调）和 **FLAME**（基于扩散的推理时运动编辑模型，以源运动和文本为条件，不做微调直接评估）。值得注意的是，TMED 和 SimMotionEdit 在目标数据集上使用约 16k 对齐的新手-专家伪对进行微调，获得了额外监督，而 ExpertEdit **仅使用无配对的专家视频训练，推理时无需任何文本提示或参考运动**。

### 主实验结果

**篮球与足球技术（Table 1）**：ExpertEdit 在所有四项技术上一致取得最优的 P 和 F 指标。以 Penalty Kick 为例，ExpertEdit 的 FID 改善率达到 **9.14%**，约为最佳基线 FLAME（3.46%）的 2.6 倍，领先幅度达 +5.68 个百分点。在 Jump Shot 上，ExpertEdit 的 P 指标为 **6.09%**，而 TMED 仅 2.57%，SimMotionEdit 为 3.21%。整体而言，ExpertEdit 在篮球和足球技术上的平均 P 和 F 显著优于所有监督基线，且无需任何配对监督或编辑指导。

**空手道技术（Table 2）**：在 Kyokushin Karate 的四项技术上，ExpertEdit 同样全面领先。Front Kick 上 F 指标达到 **9.73%**，对比 TMED 的 4.32% 和 SimMotionEdit 的 6.11%，领先 +5.41 个百分点。Roundhouse Kick 上 P 指标为 **7.18%**，远超 FLAME（3.01%）和 TMED（2.89%）。值得注意的是，空手道动作速度更快、幅度更大，对编辑精度要求更高，ExpertEdit 在此场景下依然保持稳定优势，验证了运动学掩码策略在不同运动特性下的鲁棒性。

**定性结果（Fig. 3）**：可视化分析揭示了 ExpertEdit 编辑的精细特性——编辑仅作用于技能关键时刻的关节旋转，完全保留原始运动的全局路径和节奏。在 Mikan 和 Reverse 上篮中，编辑提升了投篮手侧膝盖的高度；在 Spin Back Kick 和 Roundhouse Kick 中，踢腿伸展更充分；在 Jump Shot 中，投篮手更稳定地置于球下；在 Penalty Kick 中，踢球腿的跟随动作更完整。这些改进均体现为局部姿态的微调，而非整体运动轨迹的改变。

### 消融与分析

**训练数据量的影响（Suppl. Fig. 1）**：ExpertEdit 的性能随无配对专家训练数据量的增加而持续提升。当仅使用 30% 的专家数据训练时，P 和 F 指标仍保持正增益；随着数据量从 30% 增长到 100%，两项指标均稳步上升，未出现饱和迹象。这表明 ExpertEdit 的上下文运动填充框架能够有效利用更大规模的无配对专家数据，具有良好的数据扩展性。

**文本提示词对基线的影响（Suppl. Table 3）**：对文本条件基线方法的提示词消融揭示了重要发现——使用鼓励“平滑和控制”的通用提示（如 “Make the <TECHNIQUE_NAME> motion smoother and more controlled”）获得的技能编辑性能，**优于**直接要求 “expert-like motion” 的提示。在提示中加入具体技术名称可进一步提升性能。这一发现从侧面印证了 ExpertEdit 设计动机的合理性：显式的文本编辑指导难以精确捕捉技能精炼的微妙需求，而基于运动学掩码的隐式编辑机制能更自然地习得专家运动先验。

### 方法对比的关键差异

与监督基线相比，ExpertEdit 的核心优势源于三个关键设计选择：
1. **训练数据**：仅需无配对专家视频，消除了对昂贵的新手-专家配对数据的依赖；
2. **推理机制**：通过运动学峰值自动发现技能关键时刻并掩码，无需文本提示或参考运动；
3. **编辑方式**：双向 Transformer 的上下文运动填充，仅重建被掩码的专家运动片段，习得的是专家运动流形而非简单的映射函数。

这些设计使 ExpertEdit 在完全保留运动路径和节奏的前提下，实现了更精准的局部技能提升。基线方法依赖文本条件或配对监督，往往难以精确定位需要编辑的技能关键时刻，且容易过度编辑非关键帧，导致运动失真。

### 失败模式与局限性

尽管 ExpertEdit 在主实验中表现优异，分析揭示了几个值得关注的局限：

1. **技术特异性**：当前方法需要为每种运动技术单独训练 Pose Tokenizer 和 MotionInfiller，无法在技术间共享或泛化。扩展到未知动作时需要重新训练整个流程，限制了实际部署的灵活性。

2. **编辑范围受限**：编辑仅作用于关节旋转，保留原始全局运动路径和节奏。对于需要根本改变整体执行轨迹的技能缺陷（如完全错误的起跳方向或身体朝向），ExpertEdit 的编辑能力有限。这源于设计选择——保留根平移 $\mathbf{r}_t$ 和根方向 $\mathbf{o}_t$ 不变。

3. **运动学峰值假设**：技能关键时刻的检测依赖运动学信号 $h(t)$ 的峰值，对于非规范或高度个性化的动作，峰值检测可能不够准确。此外，不同技术的运动学信号定义需要领域知识来设计。

4. **场景上下文缺失**：仅使用 3D 骨架运动，忽略场景上下文（如球的位置、与目标的相对距离），可能限制在复杂场景中的编辑真实性。例如，在篮球跳投中，与篮筐的距离和角度会影响理想的出手姿态，但当前方法无法利用此类信息。

5. **评估的固有挑战**：尽管测试对经过 DTW 对齐和人工校验，运动编辑的“质量”评估仍存在主观性。P 和 F 指标分别衡量几何精度和分布对齐，但无法完全捕捉编辑是否保留了个人风格或是否引入了不自然的伪影。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2604_10466/figures/003_Figure_3.jpg]]
*Figure 3: ExpertEdit sequence visualization: We show novice source pose (blue) and edited pose (orange) at several frames for all techniques. ExpertEdit makes subtle pose refinements that improve form at skill-critical action moments, including raising the knee on the shooting hand-side higher during layups (Mikan, reverse), extending legs further on kicks (spin back, roundhouse), moving the shooting hand under the ball during jumpshots, and improving follow through from the kicking leg on penalty kicks*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2604_10466/figures/004_Table_1.jpg]]
*Table 1: Results on basketball and soccer techniques. M and F represent relative improvement in PA-MPJPE and alignment with the expert distribution respectively over the source motion. Higher is better for both (↑).*Indicates no access to paired supervision for training. PA-MPJPE is averaged over k = 3 expert reference pairs to account for natural variation in expert behavior*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2604_10466/figures/005_Table_2.jpg]]
*Table 2: Results on Kyokushin Karate Dataset. P denotes relative improvement in PA-MPJPE. F denotes relative improvement in FID over novice motion. Higher is better for both (↑)*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2604_10466/figures/006_Figure_1.jpg]]
*Figure 1: ExpertEdit performance as a function of training data. We report Pose Improvement (P ) and FID Improvement (F ) metrics averaged across all techniques as a function of train set size. ExpertEdit performance scales well as it observes more unpaired expert video during training*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2604_10466/figures/007_Table_3.jpg]]
*Table 3: Effect of different text-edit prompts on baseline motion editing performance. We train and evaluate a representative motion-editing baseline [29] with different text-edit prompts. P and F denote relative improvement in PA-MPJPE and alignment with the expert distribution, respectively, over the source motion. Prompts encouraging general improvements in smoothness and control led to better performance than explicitly requesting expert-like motion, and adding the technique name to the prompt led to further gains*

## 定位与知识库关联

### 技能编辑的范式转换：从配对监督到上下文运动填充

现有运动编辑方法普遍依赖**配对数据**和**显式的文本/参考编辑指导**。**TMED** 基于 Diffusion Transformer，在 MotionFix 数据集上训练，需要文本条件输入和配对微调；**SimMotionEdit** 引入辅助时序引导的文本条件编辑模型，在“新手-专家”伪对上微调；**FLAME** 则是在推理时以源运动和文本为条件的扩散编辑模型。这些方法的共同瓶颈在于：技能领域缺乏大规模配对的新手-专家运动数据和专家标注，使得监督范式难以规模化。

ExpertEdit 的核心转向在于**将技能精炼重新定义为上下文运动填充任务**。训练时仅使用无配对的专家运动片段，通过掩码语言建模（MLM）目标学习重建被掩盖的专家运动片段；推理时，自动发现新手运动的技能关键时刻并掩码，由同一模型填充专家化的关节旋转。这一设计彻底消除了对配对监督和编辑指导的依赖。

三个关键槽位的变化构成了方法差异的本质：

| 设计槽位 | 基线方法 | ExpertEdit |
|----------|----------|------------|
| 训练数据类型 | 配对新手-专家运动或运动-文本对 | 仅无配对专家运动片段 |
| 推理时的编辑指导 | 文本提示或参考运动 | 自动运动学峰值掩码，无需文本/提示/参考 |
| 编辑机制 | 文本条件去噪或代码级 Transformer | 双向 Transformer 填充以运动学峰值为中心的掩码运动片段 |

### 方法谱系中的定位

ExpertEdit 处于**自监督运动先验学习**与**运动编辑**的交叉点。其技术路线可追溯至两条线索：

1. **运动生成与先验学习**：采用 Transformer-based VQ-VAE（Pose Tokenizer）将运动离散化为令牌序列，这与 T2M-GPT、MoMask 等运动生成工作的离散表示一脉相承。但 ExpertEdit 的 VQ-VAE 使用因果自注意力编码器，确保编码仅依赖历史帧，为后续的上下文填充保留了时序一致性约束。

2. **掩码语言建模的迁移**：MotionInfiller 采用 BERT 风格的**双向 Transformer**，将 MLM 目标从文本域迁移到运动域。与随机掩码不同，ExpertEdit 的关键创新在于**运动学掩码策略**——掩码窗口始终以运动学信号 $h(t)$ 的峰值帧 $t^{*} = \arg\max_{t\in\{1,\dots,T\}} h(t)$ 为中心，强制模型学习技能关键时刻的专家运动流形。这一设计使得模型在训练时即建立了“技能关键时刻”与“专家运动重建”之间的因果关联。

### 适用边界与局限

**技术特异性约束**：当前方法需要为每种运动技术（如正手上篮、反手上篮、点球等）单独训练 Pose Tokenizer 和 MotionInfiller。模型无法在技术之间共享或泛化，扩展到未知动作时需重新训练。这一约束源于“强技术特定先验”的设计选择，而非架构层面的根本限制。

**编辑作用域限制**：编辑仅作用于关节旋转 $\hat{\mathbf{p}}_{1:T} = \mathcal{F}_{\boldsymbol{\theta}}(\mathbf{p}_{1:T})$，保留原始全局运动路径 $\mathbf{r}_t$ 和根方向 $\mathbf{o}_t$。这意味着 ExpertEdit 擅长在**保持执行轨迹和节奏**的前提下提升局部姿态质量（如踢腿时伸展更充分、投篮时手部位置更合理），但对于需要根本改变整体执行轨迹的技能缺陷（如完全错误的起跳方向或助跑路径），编辑能力有限。

**运动学峰值检测的鲁棒性**：技能关键时刻的自动发现依赖运动学信号 $h(t)$ 的峰值检测。对于动作规范、节奏明确的运动技术（如空手道前踢、篮球跳投），峰值检测准确可靠；但对于非规范或高度个性化的动作变体，单峰假设可能失效，导致编辑窗口定位偏差。

**场景上下文的缺失**：当前方法仅使用 3D 骨架运动，忽略场景上下文（如篮球与篮筐的相对位置、足球与球门的距离）。在需要精确物理交互的技能编辑中（如调整投篮出手点以适应防守距离），这一缺失可能限制编辑的真实性和实用性。

### 开放问题

1. **跨技术泛化**：能否设计统一的 ExpertEdit 架构，利用单一模型处理多种运动技能？可能的路径包括技术条件嵌入（technique-conditioned embedding）或元学习框架，使模型在观察到少量新技术样本后快速适应。

2. **场景感知编辑**：如何将场景上下文（如篮球与篮筐/足球与球门的距离、对手位置等）融入编辑过程，使生成的专家运动更符合实际物理交互约束？这可能需要将场景特征作为额外的条件信号注入 MotionInfiller。

3. **个性化保持的量化**：如何定义和量化编辑后运动与原始运动在“个人身份”上的保持程度？当前指标（P 和 F）衡量的是与专家分布的接近度，但缺乏对“过度编辑导致失去个性化特征”的惩罚机制。

4. **实时交互应用**：能否将方法压缩或蒸馏为轻量级模型，支持实时或交互式应用，为运动训练提供即时反馈？这涉及推理延迟的优化和流式编辑架构的设计。

5. **小样本/冷门运动扩展**：在缺乏充足专家视频的稀疏技术或冷门运动中，如何利用少量样本达成有效的技能编辑？可能的方案包括从富数据技术迁移运动先验，或利用人体运动的基础模型进行微调。

> **注意**：以上局限与开放问题均来自论文自身的讨论与实验限制。部分开放问题（如跨技术泛化的具体架构设计、场景感知编辑的实现路径）在原文中未给出实验验证，属于推断性扩展，需后续工作确认可行性。

## 原文 PDF

![[paperPDFs/arxiv_2026/ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos.pdf]]

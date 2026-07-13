---
title: "MusicInfuser: Making Video Diffusion Listen and Dance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MusicInfuser_Making_Video_Diffusion_Listen_and_Dance.pdf
project_link: null
code_link: "https://github.com/genmoai/models"
aliases:
- MusicInfuser
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 在预训练文本到视频扩散模型的内部 DiT 块中选择性地注入音乐条件（零初始化交叉注意力 + LoRA），并通过基于引导影响函数的层适应性准则仅调制关键层，从而在数据稀少的情况下对齐音乐与舞蹈，同时保留先验知识。
primary_logic: 预训练的文本到视频扩散模型已内化复杂的人体舞蹈知识和运动规律，只需轻量且精确的音乐适配器（ZICA、LoRA、分层选择、Beta‑Uniform 噪声调度）即可实现高效的音乐驱动视频生成，无需动作捕捉数据。
claims:
- 层适应性选择策略在整体评分上超越所有层的交叉注意力以及均匀分布层策略，证实了选择性适配的重要性。
- MusicInfuser 在 AIST++ 基准上取得的舞蹈质量平均分 (7.95) 接近真实视频 (8.01)，表明音乐同步能力接近自然水平。
- 人类评估显示 MusicInfuser 在整体满意度和创意诠释上均显著优于纯文本‑视频基线模型 Mochi，验证了音乐条件注入的有效性。
- AIST++ Dance Quality (LLM‑based) 上 Dance Quality Average = 7.95
---

# MusicInfuser: Making Video Diffusion Listen and Dance

> [!tip] 核心洞察
> 预训练的文本到视频扩散模型已内化复杂的人体舞蹈知识和运动规律，只需轻量且精确的音乐适配器（ZICA、LoRA、分层选择、Beta‑Uniform 噪声调度）即可实现高效的音乐驱动视频生成，无需动作捕捉数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | MusicInfuser：让视频扩散模型聆听并起舞 |
| 英文题名 | MusicInfuser: Making Video Diffusion Listen and Dance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hong_MusicInfuser_Making_Video_Diffusion_Listen_and_Dance_CVPR_2026_paper.html) · [Code](https://github.com/genmoai/models) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | MusicInfuser |
| Dataset | AIST++ Dance Quality, User Study / Prompt Alignment |

> [!tip] 效果简介
> - AIST++ Dance Quality (LLM‑based) 上，Dance Quality Average 7.95 vs 8.01 (Ground Truth) (-0.06)。
> - User Study / Prompt Alignment 上，Overall Satisfaction 9.80 vs 9.55 (Mochi) (+0.25)；Creative Interpretation 9.27 vs 9.04 (Mochi) (+0.23)。

## 概要

**问题瓶颈**：现有文本到视频扩散模型无法根据指定音乐生成同步且细节丰富的舞蹈视频。直接训练音频‑视频生成模型受限于舞蹈数据稀缺，质量欠佳；骨骼动画方法则缺乏躯体曲线、旋转、手指、头发和服装等细腻运动（参见 Figure 2）。

**核心洞察**：预训练的文本到视频扩散模型已内化复杂的人体舞蹈知识和运动规律，只需轻量且精确的音乐适配器即可实现高效的音乐驱动视频生成，无需动作捕捉数据。

**方法定位**：MusicInfuser 在预训练文本到视频扩散模型（**Mochi**，Genmo Team, 2024）的内部 DiT 块中选择性地注入音乐条件，通过零初始化交叉注意力（ZICA）与高秩 LoRA（秩 64）实现轻量适配，并基于引导影响函数的层适应性准则仅调制关键层，从而在数据稀少的情况下对齐音乐与舞蹈，同时保留先验知识。

**主要结果**：
- 在 AIST++ 基准上，MusicInfuser 的舞蹈质量平均分（7.95）接近真实视频（8.01），表明音乐同步能力接近自然水平（Table 2）。
- 人类评估显示，MusicInfuser 在整体满意度（9.80 vs. 9.55）和创意诠释（9.27 vs. 9.04）上均显著优于纯文本‑视频基线 Mochi，验证了音乐条件注入的有效性（Table 4 / Figure 9）。
- 消融实验证实，层适应性选择策略在整体评分上超越所有层的交叉注意力（8.14 vs. 7.80）以及均匀分布层策略（7.62），证明了选择性适配的重要性（Table 1）。

**方法谱系与知识库定位**：MusicInfuser 属于“预训练视频扩散模型 + 轻量跨模态适配”范式，区别于直接联合音视频生成的 **MM-Diffusion**（Ruan et al., CVPR 2023）和基于 VQ 的音乐驱动 3D 舞蹈生成方法如 **AI Choreographer**（Li et al., ICCV 2021）与 **Bailando**（Siyao et al., CVPR 2022）。其关键创新在于将适配负担从全模型微调转移至选择性层注入与零初始化交叉注意力，在极低数据预算下实现高保真音乐‑视频对齐。

### 问题背景：从文本到视频到音乐驱动的舞蹈生成

近年来，文本到视频扩散模型取得了显著进展，能够根据自然语言描述生成高质量的视频内容。然而，这些模型在设计上仅接受文本作为条件输入，无法直接响应音乐信号。在舞蹈生成这一特定领域，音乐与视觉动作的同步性是核心需求——观众期望视频中舞者的肢体动作、节奏韵律与背景音乐高度一致。现有的文本到视频模型虽然能生成“一个人在跳舞”的视频，但无法保证其动作与指定的音乐同步，这构成了一个明确的能力缺口。

### 现有方法的局限

当前音乐驱动舞蹈生成的主流方法可归纳为三条技术路线，各自存在瓶颈：

**骨骼动画方法**是最早探索的方向，代表性工作包括 **AI Choreographer**（Li et al., ICCV 2021）、**Bailando**（Siyao et al., CVPR 2022）和 **EDGE**（Tseng et al., CVPR 2023）。这些方法将人体运动抽象为稀疏的骨骼关键点序列，通过学习音乐到骨骼运动的映射来生成舞蹈。然而，如 Figure 2 所示，骨骼表示天然缺失了躯干弯曲、轴向旋转、手指关节、头发飘动和衣物褶皱等细腻运动细节，导致生成的舞蹈在视觉丰富度和表现力上存在天花板。

**联合音视频生成方法**试图直接从音乐合成视频帧，例如 **MM-Diffusion**（Ruan et al., CVPR 2023）。但这类方法面临一个根本性困境：高质量的音乐-舞蹈配对视频数据极为稀缺。直接从头训练音频-视频生成模型，受限于数据规模和多样性，生成质量往往难以与大规模预训练的文本-视频模型匹敌。

**文本-视频预训练模型的直接适配**尚处于空白状态。以 **Mochi**（Genmo Team, 2024）为代表的大规模预训练视频扩散模型已内化了丰富的人体运动先验和舞蹈知识，但这些知识被“锁”在文本条件接口之后，缺乏将音乐信号引入的机制。

### 核心洞察与动机

本文的核心洞察在于：预训练的文本到视频扩散模型已经学会了“如何跳舞”——它们理解人体运动规律、舞蹈动作的连贯性和视觉表现力。真正缺失的不是舞蹈生成能力，而是一个将音乐信号“接入”已有舞蹈知识的轻量级适配机制。

基于这一洞察，MusicInfuser 的动机可以概括为三点：

1. **保留先验，而非从头学习**：与其在稀缺的舞蹈数据上训练全新的音视频生成模型，不如充分利用预训练模型中已有的运动知识，仅需教会模型“聆听”音乐。
2. **轻量适配，精确注入**：音乐条件应以最小侵入性的方式注入扩散模型的去噪过程，避免破坏预训练权重中存储的视觉质量。
3. **超越骨骼，直接生成视频**：绕过骨骼中间表示，直接在像素空间生成包含完整视觉细节的舞蹈视频，从根本上解决骨骼方法的表达能力瓶颈。

这一思路将问题从“如何从音乐生成舞蹈”重新定义为“如何让一个已经会跳舞的模型学会听音乐”，从而在数据效率、生成质量和音乐同步性之间找到了新的平衡点。

## 核心方法与创新机理

MusicInfuser 的核心创新在于提出了一套**轻量、先验保持的音乐适配框架**，使预训练的文本到视频扩散模型无需从头训练即可生成音乐同步的高质量舞蹈视频。与现有方法（如骨骼动画生成 **EDGE** (Tseng et al., CVPR 2023)、联合音视频生成 **MM-Diffusion** (Ruan et al., CVPR 2023)）相比，MusicInfuser 直接利用预训练视频模型内化的复杂人体运动知识，仅通过选择性注入音乐条件来实现跨模态对齐，避免了舞蹈数据稀缺导致的生成质量瓶颈。

### 关键创新点（Changed Slots）

**1. 零初始化交叉注意力（ZICA）+ 高秩 LoRA 的音乐条件注入**

基线模型 **Mochi**（Genmo Team, 2024）仅接受文本条件，不具备音乐感知能力。MusicInfuser 在 DiT 块中引入零初始化交叉注意力（ZICA），将音频特征逐步注入去噪过程。ZICA 的核心机制是将输出投影矩阵初始化为零，使交叉注意力块在训练初期表现为恒等映射，从而保护预训练先验不被破坏（Eq. 6）。同时，采用秩 64 的高秩 LoRA 适配器对自注意力权重进行低秩更新，为视频 Transformer 提供足够容量来捕捉复杂的时序舞蹈运动——这显著高于图像模型中常用的秩 8–16 设置。

**2. 基于引导影响函数的层适应性选择策略**

并非所有 DiT 层都适合注入音乐条件：全层交叉注意力会损害去噪能力（Table 1 中 All Layers 整体评分 7.80），而均匀分布或仅选首/尾层的直觉策略也会降低视频质量。MusicInfuser 提出通过**引导影响函数**（Eq. 4）计算每层的适应性——即跳过某层时对去噪输出的影响梯度——仅选择高适应性层进行适配。这一策略使整体评分达到 8.14，显著优于所有基线层选择方案（Evenly Distributed 7.62、Middle Layers 7.77、Last Layers 7.83）。

**3. Beta-Uniform 噪声调度**

标准扩散训练使用均匀噪声分布，但舞蹈视频生成对低噪声阶段的细节重建要求更高。MusicInfuser 采用 Beta-Uniform 调度：训练初期从 Beta(1, β=3) 分布采样噪声（集中于低噪声水平），随后以指数衰减平滑过渡到 Uniform(0,1) 分布。消融实验表明，移除该调度后舞蹈质量平均分从 8.22 降至 8.01，证实其对人体表示和动作真实感的改善作用。

### 创新价值总结

上述三个 changed slots 共同构成了“先验保持 + 精准适配”的技术路线：ZICA 和 LoRA 保证新模态的平滑注入，层适应性选择避免冗余调制对先验的破坏，Beta-Uniform 调度则优化了舞蹈细节的生成过程。整套框架训练仅需单 GPU 一天内完成，在数据极度受限的条件下实现了与真实视频接近的舞蹈质量（AIST++ 基准上 7.95 vs. Ground Truth 8.01）。

MusicInfuser 的整体设计遵循“轻量适配、先验保留”的原则，将预训练文本到视频扩散模型改造为音乐驱动的舞蹈视频生成器。其核心思路是：冻结预训练 DiT 骨干的绝大部分权重，仅在选定层注入音乐条件，从而在数据稀少的情况下高效对齐音频与视频运动，同时避免灾难性遗忘。

### 输入输出流

系统接收三类输入：
1. **文本提示**：通过文本编码器编码为条件 token，控制舞蹈的风格、场景和主体外观。
2. **音乐音频**：经音频编码器（Wav2Vec 2.0）提取特征，再由音频投影器（MLP + 下采样）映射为与视频 token 长度对齐的音频表示。
3. **初始噪声**：从 Beta‑Uniform 调度中采样噪声水平，作为扩散过程的起点。

输出为一段与输入音乐节奏同步、且符合文本描述的舞蹈视频帧序列。

### 模块关系与数据流

整个 pipeline 由以下模块串联构成：

- **文本编码器**：将文本提示转化为条件 token，注入去噪 DiT 骨干的自注意力层，提供全局风格与场景控制。
- **去噪 DiT 骨干**：预训练的视频扩散 Transformer，负责逐步去噪生成视频帧。其权重在训练中冻结，仅通过 LoRA 适配器和 ZICA 模块接受音乐条件。
- **音频编码器（Wav2Vec 2.0）**：提取输入音频的特征表示，作为音乐条件的原始来源。
- **音频投影器（MLP + 下采样）**：将音频特征投影到与视频 token 兼容的维度，并通过下采样对齐时间长度。
- **ZICA 模块**：零初始化交叉注意力层，插入到 DiT 骨干的选定层中。其输出投影矩阵初始为零，使得交叉注意力在训练初期表现为恒等映射，从而平稳地逐步融合音频特征。公式为：
  $$
  \mathbf { Z } = \mathbf { V } + \mathbf { W } _ { O } \operatorname { s o f t m a x } \left( \frac { \mathbf { V } \mathbf { W } _ { Q } ( \mathbf { A W } _ { K } ) ^ { \top } } { \sqrt { d } } \right) \mathbf { A W } _ { V }
  $$
  其中 $\mathbf{W}_O$ 初始化为零矩阵。
- **LoRA 适配器**：在 DiT 骨干的自注意力权重上施加低秩更新（秩 64），为音乐条件的注入提供额外容量，同时保持参数效率。

### 关键设计决策

1. **层适应性选择**：并非在所有 DiT 层中添加交叉注意力，而是通过基于引导影响函数的层适应性准则，仅在高适应性层中插入 ZICA 模块。消融实验（Table 1）表明，这种选择性策略在整体评分上显著优于全层适配（8.14 vs. 7.80）和均匀分布层适配（8.14 vs. 7.62），验证了精准层选择的重要性。

2. **Beta‑Uniform 噪声调度**：训练噪声分布从 Beta(1, β=3) 指数衰减至 Uniform(0,1)，使模型在训练初期集中于低噪声水平的去噪，有助于保留预训练模型的人体表示能力。移除该调度后，舞蹈质量平均分从 8.22 降至 8.01（Table 1）。

3. **零初始化交叉注意力**：ZICA 的输出投影初始为零，确保训练初期交叉注意力块等价于恒等映射，从而保护预训练先验。若不进行零初始化，视频/成像质量平均分从 8.02 降至 7.82（Table 1）。

整个训练可在单 GPU 上一天内完成，体现了方法的资源效率。

MusicInfuser 的核心设计围绕一个关键命题展开：**预训练的文本到视频扩散模型已经内化了复杂的人体舞蹈知识和运动规律，只需轻量且精确的音乐适配即可实现高效的音频驱动视频生成**。本节拆解支撑该命题的三个关键模块——层适应性准则、Beta‑Uniform 噪声调度和零初始化交叉注意力适配器——并给出其数学表述。

### 层适应性准则：基于引导影响函数的关键层选择

将交叉注意力模块插入 DiT 的所有层会损害去噪能力，尤其在低数据场景下（Table 1，“All Layers” 整体评分 7.80 vs. Ours 8.14）。MusicInfuser 引入一种**基于引导的构造性影响函数**来量化每一层对条件生成的贡献，从而仅适配高适应性层。

具体地，对于 DiT 的第 $l$ 层，定义隐式能量函数 $\mathcal{G}_l$，其梯度通过跳过该层的引导信号计算：

$$
\nabla_{\mathbf{x}} \mathcal{G}_l = \frac{D_\theta^L(\mathbf{x}|\mathbf{c};\sigma) - D_\theta^{L\setminus\{l\}}(\mathbf{x}|\mathbf{c};\sigma)}{\sigma}
$$

其中：
- $D_\theta^L$ 表示完整 $L$ 层 DiT 的条件去噪输出；
- $D_\theta^{L\setminus\{l\}}$ 表示跳过第 $l$ 层后的去噪输出；
- $\mathbf{x}$ 为当前噪声样本，$\mathbf{c}$ 为文本条件，$\sigma$ 为噪声水平。

该梯度的大小反映了第 $l$ 层对条件生成的影响程度：**梯度越大，该层对条件信号的响应越强，适应性越高**。MusicInfuser 据此对所有 DiT 层排序，仅在前 $k$ 个高适应性层中插入 ZICA 模块。消融实验证实，这一策略显著优于均匀分布层（7.62）、仅首层（7.99）、仅中层（7.77）和仅末层（7.83）等直观基线（Table 1）。

### Beta‑Uniform 噪声调度：从低频结构到高频细节的渐进学习

标准扩散训练在均匀噪声分布 $\sigma \sim \mathcal{U}(0,1)$ 下进行，但视频生成中人体结构和运动连贯性对低噪声阶段（即低频结构）的建模质量高度敏感。MusicInfuser 提出 **Beta‑Uniform 调度**，使训练噪声分布从集中于低噪声水平的 Beta 分布逐步演化至均匀分布：

$$
f(x;\alpha=1,\beta) = \frac{(1-x)^{\beta-1}}{B(1,\beta)}, \quad 0 \le x \le 1
$$

其中 $\beta$ 控制分布形态：$\beta > 1$ 时概率质量向 $x=0$（低噪声）集中。训练过程中，$\beta$ 从初始值 $\beta=3$ 指数衰减至 $\beta=1$（此时 Beta(1,1) 退化为均匀分布），使模型**先学习人体结构和运动的大尺度模式，再逐步细化高频纹理和细节**。Table 1 显示，移除 Beta‑Uniform 调度后舞蹈质量平均分从 8.22 降至 8.01，证实了该调度对动作真实感和人体表示质量的改善。

### 零初始化交叉注意力与 LoRA 适配器

音乐条件通过**零初始化交叉注意力（ZICA）**注入 DiT 层。设视频特征为 $\mathbf{V}$，音频特征为 $\mathbf{A}$，ZICA 的计算为：

$$
\mathbf{Z} = \mathbf{V} + \mathbf{W}_O \operatorname{softmax}\left(\frac{\mathbf{V}\mathbf{W}_Q (\mathbf{A}\mathbf{W}_K)^\top}{\sqrt{d}}\right) \mathbf{A}\mathbf{W}_V
$$

关键设计在于输出投影矩阵 $\mathbf{W}_O$ **初始化为零矩阵**。训练初期，交叉注意力分支输出为零，ZICA 退化为恒等映射 $\mathbf{Z}=\mathbf{V}$，完全不干扰预训练模型的先验知识；随着训练推进，$\mathbf{W}_O$ 逐步学习融合音频特征，实现平滑的条件注入。Table 1 消融显示，不进行零初始化导致视频质量平均分从 8.02 降至 7.82，验证了该策略对保护预训练能力的关键作用。

此外，MusicInfuser 在自注意力权重上施加**高秩 LoRA（秩 64）**，以增强对新模态的适应容量。与图像模型中常用的秩 8–16 不同，视频 Transformer 需要更高秩来捕捉复杂的时序舞蹈运动（Sec. 5.1）。LoRA 更新仅作用于适配参数 $\phi$，与冻结的基模型参数 $\theta$ 协同，构成最终的条件去噪器 $D_{\theta,\phi}(\mathbf{x}|\mathbf{c},\mathbf{a};\sigma)$。

## 实验与关键发现

### 核心性能对比

MusicInfuser 在 AIST++ 基准上的舞蹈质量平均分达到 **7.95**，与真实视频的 **8.01** 仅差 0.06（Table 2），表明音乐驱动的舞蹈同步能力已接近自然水平。在视频质量维度，MusicInfuser 取得 **8.95** 的平均分（Table 3），证明了先验保持策略在引入新模态条件时未牺牲生成质量。

![[assets/figures/papers/paper_list_l996_https_openaccess_thecvf_com_content_CVPR2026_html_Hong_MusicInfuser_Maki/figures/009_Table_2.jpg]]
*Table 2: Dance quality metrics comparing different models. A, V, and T denote audio, video, and text input modalities, respectively. For the models that have text input modality, we report an average of scores using a predefined benchmark of prompts*

![[assets/figures/papers/paper_list_l996_https_openaccess_thecvf_com_content_CVPR2026_html_Hong_MusicInfuser_Maki/figures/010_Table_3.jpg]]
*Table 3: Video quality metrics comparing different models. For the models that have text input modality, we report an average of scores using a predefined benchmark of prompts*

人类评估进一步验证了方法的实际效果：在整体满意度上，MusicInfuser 以 **9.80** 显著优于纯文本‑视频基线 Mochi 的 **9.55**；在创意诠释维度上，以 **9.27** 对比 **9.04** 同样取得领先（Table 4, Figure 9）。这一差异的因果链路在于：Mochi 仅依赖文本提示生成舞蹈，无法感知音乐节拍和旋律结构，而 MusicInfuser 通过 ZICA + LoRA 的轻量适配将音乐信号精确注入去噪过程，使运动节奏与音频特征对齐。

![[assets/figures/papers/paper_list_l996_https_openaccess_thecvf_com_content_CVPR2026_html_Hong_MusicInfuser_Maki/figures/011_Table_4.jpg]]
*Table 4: Prompt alignment metrics comparing different models*

![[assets/figures/papers/paper_list_l996_https_openaccess_thecvf_com_content_CVPR2026_html_Hong_MusicInfuser_Maki/figures/013_Figure_9.jpg]]
*Figure 9: Human evaluation*

### 消融实验：层选择策略是核心瓶颈

Table 1 的消融结果揭示了层适应性选择策略的决定性作用。基于引导影响函数（Eq. 4）计算各层适应性后选择性注入交叉注意力的方案（Ours），在综合评分上取得 **8.14**，而全层注入（All Layers）仅得 **7.80**，均匀分布层策略（Evenly Distributed Layers）更低至 **7.62**。这一现象的根本原因在于：全层注入在数据稀少场景下会破坏预训练 DiT 骨干的去噪能力，而仅首层（First Layers, 7.99）、仅中层（Middle Layers, 7.77）、仅末层（Last Layers, 7.83）等直觉性选择均无法精准定位对音乐条件最敏感的层，导致适配不足或过度。

**Beta‑Uniform 噪声调度**的移除使舞蹈质量平均分从 8.22 降至 8.01（Table 1），验证了从 Beta(1, β=3) 指数衰减至均匀分布的策略能有效改善人体表示和动作真实感。其机理在于：训练初期集中于低噪声水平，使模型优先学习粗粒度的人体结构和运动模式；后期引入均匀分布则覆盖全噪声范围，确保生成多样性。

**零初始化交叉注意力（ZICA）** 的消融结果同样关键：不进行零初始化时，视频质量平均分从 8.02 降至 7.82（Table 1）。ZICA 将输出投影 $W_O$ 初始化为零矩阵，使交叉注意力块在训练起始阶段等效于恒等映射（Eq. 6），从而避免随机初始化的音频特征干扰预训练权重，实现平滑的条件融合。

### 数据与训练设置的影响

Table 4 的消融显示，**开放域数据（in‑the‑wild data）** 的缺失严重损害提示对齐能力：提示对齐平均分从 8.96 降至 7.96，风格捕捉更是从 8.42 骤降至 6.80。这表明 AIST++ 数据集虽然提供了高质量的音乐‑舞蹈配对，但其舞蹈风格和场景多样性有限，开放域数据的补充对于文本可控的风格化生成不可或缺。

在训练效率方面，MusicInfuser 的所有训练在**单 GPU 上一天内完成**，体现了方法的高资源效率。这一效率得益于仅训练新增的 ZICA 模块和 LoRA 适配器（秩 64），冻结预训练的 DiT 骨干和文本编码器。LoRA 秩的选择也经过验证：视频 Transformer 需要秩 64 才能提供足够容量捕捉复杂的时序舞蹈运动，常规图像模型常用的秩 8–16 不足以胜任（Sec. 5.1）。

### 定性分析：泛化与控制能力

Figure 6 展示了 MusicInfuser 在**音乐长度和类型上的泛化能力**：模型可生成长度数倍于训练视频的舞蹈序列，且能处理训练中未见过的 K‑pop 音乐类型。Figure 7 的**速度控制实验**表明，将音频输入减速至 0.75× 或加速至 1.25× 后，生成的舞蹈速度相应变化，同时音乐音调的改变也带来动态特征的调整，验证了音乐条件注入的因果性而非相关性。

![[assets/figures/papers/paper_list_l996_https_openaccess_thecvf_com_content_CVPR2026_html_Hong_MusicInfuser_Maki/figures/006_Figure_6.jpg]]
*Figure 6: Generalization capabilities in terms of music length and type. MusicInfuser can generate multiple times longer dance videos that are multiple times longer than the videos used for training. For each row, we use synthetic in-the-wild music tracks with a keyword “K-pop,” a type of music not existing in AIST [48], and use a prompt “a professional female dancer dancing*

Figure 3 和 Figure 4 分别展示了向**未见动物主体**（土拨鼠、兔子、狗）的泛化以及**多人群舞**的生成能力，说明预训练基模型已内化的运动知识可通过轻量适配迁移到新主体和新场景。Figure 8 的多样性实验表明，通过改变随机种子，同一音乐和文本可产生风格各异的舞蹈，满足创意生成的需求。

![[assets/figures/papers/paper_list_l996_https_openaccess_thecvf_com_content_CVPR2026_html_Hong_MusicInfuser_Maki/figures/003_Figure_3.jpg]]
*Figure 3: Using prompts such as “a {marmot, rabbit, dog (top to bottom rows)} dancing ...,” our method generalizes to unseen dancing subjects*

### 失败模式与局限

尽管整体表现优异，MusicInfuser 存在以下可识别的失败模式：

1. **基模型依赖**：舞蹈质量高度依赖预训练 Mochi 模型的能力。若基模型在罕见舞蹈类型或复杂动作（如高难度旋转、地板动作）上表现不佳，适配效果可能受限。这一推断来源于方法设计本身——MusicInfuser 仅添加轻量适配器，未修改基模型权重。

2. **数据覆盖不足**：训练所用的 AIST++ 数据集以标准舞蹈动作为主，可能无法覆盖所有舞蹈流派和文化风格。Table 4 中开放域数据消融的结果间接支持了这一点。

3. **长视频时域连贯性未充分验证**：虽然 Figure 6 展示了长度泛化，但极端长度条件下的时域一致性和动作退化程度未在量化实验中测试。

4. **多人复杂交互未深入分析**：Figure 4 展示了群舞生成，但未评估多人之间的协调配合质量（如双人舞中的接触、同步转向等），该点需要手动验证。

## 定位与知识库关联

### 任务定位与核心瓶颈

MusicInfuser 解决的是**音乐驱动的视频舞蹈生成**任务：给定一段音乐和文本描述，生成与之同步、细节丰富的舞蹈视频。该任务处于文本到视频生成、音频-视觉跨模态学习与人体运动生成的交叉地带。现有方法面临三重困境：

1. **骨骼动画方法的“骨架化”局限**：以 **EDGE** (Tseng et al., CVPR 2023)、**Bailando** (Siyao et al., CVPR 2022) 和 **AI Choreographer** (Li et al., ICCV 2021) 为代表的舞蹈生成方法输出 3D 骨骼序列，再通过渲染或动作迁移生成视频。这类管线天然缺失躯干弯曲、轴向旋转、手指关节、头发飘动和衣物褶皱等细腻运动维度（见 Figure 2 动机示例），导致舞蹈表现力受限。

2. **联合音视频生成的训练数据瓶颈**：**MM-Diffusion** (Ruan et al., CVPR 2023) 等模型试图直接学习从音频到视频的映射，但高质量音视频舞蹈配对数据极为稀缺（主流数据集仅 AIST++ 等少数可控来源），模型难以学到鲁棒的舞蹈-音乐对齐，生成质量欠佳。

3. **纯文本-视频模型的模态盲区**：预训练文本-视频扩散模型（如 **Mochi**，Genmo Team, 2024）虽已内化复杂的人体舞蹈知识和运动规律，但其条件接口仅接受文本，无法感知音乐节拍、旋律和情感线索，因而无法生成与音乐同步的动作。

MusicInfuser 的因果杠杆在于：**不重新训练视频生成能力，而是在预训练模型中精准注入音乐条件**。这绕过了数据稀缺问题——模型只需学习“音乐-运动对齐”这一轻量映射，而非从零学习视频生成。

### 方法谱系中的位置

从技术路线看，MusicInfuser 属于**预训练模型适配（adapter-based adaptation）**范式，其设计决策与以下工作形成对比或继承关系：

| 维度 | 骨骼动画路线 | 联合生成路线 | MusicInfuser（本文） |
|------|------------|------------|-------------------|
| 输出形式 | 3D 骨骼序列 | 视频帧 | 视频帧 |
| 数据需求 | 动作捕捉数据 | 音视频配对数据 | 音视频配对 + 预训练视频模型 |
| 运动细节 | 缺失躯体曲线、手指等 | 受限于数据质量 | 继承预训练模型的丰富先验 |
| 文本可控性 | 有限 | 有限 | 通过文本提示控制风格/场景 |
| 训练开销 | 中等 | 高 | 单 GPU 一天内完成 |

具体而言，MusicInfuser 的技术贡献可映射到以下知识节点：

- **零初始化交叉注意力（ZICA）**：继承自扩散模型适配中的“零初始化”思想（如 ControlNet 对图像扩散模型的适配），但将其首次应用于视频 DiT 的音频条件注入。ZICA 将交叉注意力的输出投影矩阵初始化为零，使模块在训练初期表现为恒等映射，从而保护预训练先验不被随机初始化破坏（Eq. 6）。

- **高秩 LoRA 适配**：与图像模型中常用的低秩设置（rank 8–16）不同，MusicInfuser 在视频 Transformer 的自注意力层上使用 rank 64 的 LoRA。这是因为时序舞蹈运动涉及复杂的时空相关性，低秩瓶颈不足以捕捉这些模式（Sec. 5.1）。

- **基于引导影响函数的层适应性准则**：这是 MusicInfuser 的核心方法论创新。传统适配策略（均匀分布层、仅前几层、所有层）缺乏对“哪些层对音乐条件最敏感”的理论指导。MusicInfuser 通过计算层跳过引导（layer-skip guidance）的梯度范数（Eq. 4），量化每层对条件信号的适应性，仅在高适应性层注入 ZICA 模块。消融实验（Table 1）证实该策略在整体评分（8.14）上显著优于全层适配（7.80）和均匀分布（7.62）。

- **Beta-Uniform 噪声调度**：从 Beta(1, β=3) 指数衰减至 Uniform(0,1) 的调度策略，使训练初期集中于低噪声水平（更关注语义结构），后期逐步覆盖全噪声范围（改善细节生成）。该策略的移除导致舞蹈质量平均分从 8.22 降至 8.01（Table 1）。

### 适用边界与局限

MusicInfuser 的适用边界受以下因素制约，部分已在论文中验证，部分需进一步确认：

1. **对预训练基模型的强依赖**：舞蹈质量高度依赖于 Mochi 模型的先验知识。若基模型在罕见舞蹈类型（如特定民族舞蹈）或复杂动作（如地板动作）上表现不佳，适配效果可能受限。论文未在不同基模型上进行对比实验，这一点需要手动验证。

2. **训练数据的覆盖范围**：尽管方法在 AIST++ 基准上取得了接近真实视频的舞蹈质量（7.95 vs. 8.01，Table 2），但 AIST++ 主要涵盖标准舞种。论文展示了向 K-pop 等未见音乐类型的泛化（Figure 6），但未系统评估所有舞蹈流派的覆盖度。

3. **长视频时域连贯性**：Figure 6 展示了比训练视频更长序列的生成能力，但未在极端长度（如数分钟）条件下进行定量评估。长视频可能面临动作重复、漂移或风格退化等问题。

4. **多人复杂交互**：Figure 4 展示了群舞生成，但未深入分析多人之间的协调与配合质量（如双人舞中的接触、同步和空间关系）。该能力边界需要进一步研究。

5. **推理速度与实时性**：论文未报告推理延迟。在实际部署中，扩散模型的多步采样可能限制实时或交互式应用场景。

### 开放问题

1. **跨基模型泛化性**：层适应性准则是否适用于其他视频扩散模型架构（如基于 UNet 的模型）？引导影响函数的计算是否依赖于特定的 DiT 设计？

2. **细粒度音乐对齐的量化**：当前评估使用 LLM 评分（Qwen3-Omni），但缺乏对“节拍级”或“音符级”同步精度的客观度量。如何设计更细粒度的音乐-运动对齐指标仍是一个开放问题。

3. **伦理与安全审查**：论文未讨论模型是否可能生成不安全或不当的舞蹈内容（如过度暴露、暴力动作等）。在开放域部署中，内容审核机制的设计是必要的后续工作。

4. **多模态条件的冲突与协调**：当文本提示与音乐风格不一致时（如文本要求“芭蕾”而音乐是“嘻哈”），模型如何协调冲突？该场景下的行为模式尚未被系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/MusicInfuser_Making_Video_Diffusion_Listen_and_Dance.pdf]]

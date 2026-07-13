---
title: "OneHOI: Unifying Human-Object Interaction Generation and Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OneHOI_Unifying_Human_Object_Interaction_Generation_and_Editing.pdf
project_link: "https://jiuntian.github.io/OneHOI/"
code_link: null
aliases:
- OneHOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过动词中介的注意力拓扑（Structured HOI Attention）、角色/实例感知的HOI Token注入（HOI Encoder）和交互实例专属的位置编码（HOI RoPE）显式建模交互结构。
primary_logic: HOI生成与编辑本质上是同一条件去噪过程的两种视图，通过共享结构化交互表示并联合训练，生成学到的丰富交互语义可反哺编辑，反之亦然，实现单一框架内灵活的多条件统一控制。
claims:
- 在无布局编辑任务上，OneHOI的Editability-Identity（0.638）和HOI Editability（0.596）分别较最强先前工作提升10.0%和16.0%。
- 联合训练统一模型在匹配算力下生成任务HOI准确率提升26.4%，无布局编辑HOI编辑成功率提升21.1%。
- 结构化HOI注意力（Structured HOI Attention）的添加使HOI准确率和编辑一致性出现第二次显著跃升，证实动词拓扑约束的关键作用。
- IEBench (Layout-free HOI Editing) 上 Editability-Identity = 0.638
---

# OneHOI: Unifying Human-Object Interaction Generation and Editing

> [!tip] 核心洞察
> HOI生成与编辑本质上是同一条件去噪过程的两种视图，通过共享结构化交互表示并联合训练，生成学到的丰富交互语义可反哺编辑，反之亦然，实现单一框架内灵活的多条件统一控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | OneHOI: 统一人体-物体交互生成与编辑 |
| 英文题名 | OneHOI: Unifying Human-Object Interaction Generation and Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.14062) · [Project](https://jiuntian.github.io/OneHOI/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OneHOI |
| Dataset | IEBench, MultiHOIEdit, HICO-DET |

> [!tip] 效果简介
> - IEBench (Layout-free HOI Editing) 上，Editability-Identity 0.638 vs 0.580 (Qwen Image Edit), 0.573 (InteractEdit) (+10.0% over best prior)；HOI Editability 0.596 vs 0.514 (InteractEdit) (+16.0%)。
> - IEBench (Layout-guided Single-HOI Editing) 上，Spatial Score (mIoU) 0.822 vs 0.749 (InteractEdit+InteractDiffusion) (+9.7%)。
> - MultiHOIEdit (Layout-guided Multi-HOI Editing) 上，Spatial Score / Editability-Identity 0.675 / 0.435 vs N/A (first baseline) (-)。

## 概要

现有的人体-物体交互（HOI）生成与编辑方法长期处于分裂状态：生成模型依赖布局条件但缺乏灵活控制，编辑模型则难以解耦姿态与接触，且无法扩展到多交互场景。更深层的问题是，主流扩散Transformer（DiT）架构缺少显式的交互关系建模，导致生成的交互仅停留在对象并置的浅层语义。OneHOI 的核心洞察在于，HOI 生成与编辑本质上是同一条件去噪过程的两种视图——通过共享结构化交互表示并联合训练，生成学到的丰富交互语义可以反哺编辑，反之亦然。

基于此，OneHOI 提出了一种统一的 DiT 框架，将 HOI 生成与编辑整合为单一条件去噪流程。其核心是关系型扩散Transformer（R-DiT），通过三个关键模块显式建模交互结构：**HOI Encoder** 注入角色与实例身份线索以防止角色混淆；**Structured HOI Attention** 强制动词中介的注意力拓扑，阻断主体与客体的直接连接，并将 HOI token 的空间关注约束到对应区域；**HOI RoPE** 为每个交互实例分配独立的位置编码槽位，降低多实例场景中的特征串扰。这些设计共同构成了从“对象并置”到“关系理解”的因果杠杆。

实验表明，统一框架带来了显著的协同效应：在匹配算力下，联合训练使生成任务的 HOI 准确率提升 26.4%，无布局编辑的 HOI 编辑成功率提升 21.1%。在 IEBench 基准上，OneHOI 的无布局编辑 Editability-Identity（0.638）和 HOI Editability（0.596）分别较最强先前工作提升 10.0% 和 16.0%，同时首次建立了布局引导的多交互编辑基线。消融研究进一步揭示，Structured HOI Attention 是提升交互正确性的最关键模块，验证了动词拓扑约束在关系建模中的核心作用。

### 问题背景

人体-物体交互（Human-Object Interaction, HOI）理解是视觉生成领域的核心挑战之一。与单纯将人和物体放置在场景中不同，HOI生成要求模型具备对**交互关系**的深层语义理解——不仅要知道“谁”对“什么”做了“什么动作”，还要在像素空间中忠实地呈现这种关系的几何与物理约束。然而，现有方法在这一目标上存在根本性的**任务割裂**：HOI生成和HOI编辑被当作两个独立问题分别解决，缺乏统一的建模框架。

具体而言，HOI生成模型（如**InteractDiffusion**）通常依赖布局（layout）作为空间条件，能够合成符合空间位置的交互场景，但缺乏对交互语义的灵活控制能力——一旦布局给定，用户难以对交互动作进行细粒度的文本引导调整。另一方面，HOI编辑模型（如**InteractEdit**、**HOIEdit**）虽然支持通过文本指令修改交互动作，却普遍面临两大瓶颈：(1) **姿态与接触解耦困难**——编辑时难以在改变交互动作的同时保持人物身份和场景一致性；(2) **多交互扩展受限**——现有编辑方法几乎无法处理包含多个交互实例的复杂场景。

### 深层瓶颈：扩散Transformer缺少显式交互关系建模

上述任务割裂的背后，隐藏着一个更深层的架构缺陷。当前主流的扩散Transformer（Diffusion Transformer, DiT）在条件注入时，通常将HOI信息简单地转化为文本Token或布局嵌入，**缺少对交互关系本身的显式结构化表示**。这导致两个直接后果：

- **关系浅层化**：模型倾向于将交互简化为“人+物体共现”，而非真正理解“人正在对物体执行某个动作”的语义。生成结果中常见的问题是：人和物体位置正确，但交互姿态错误或物理上不可行。
- **多实例混淆**：当场景中存在多个交互时，不同交互实例的HOI Token在自注意力机制中相互干扰，导致动作与主体/客体的对应关系发生错乱。

### 核心洞察与本文动机

OneHOI的核心洞察在于：**HOI生成与编辑本质上是同一条件去噪过程的两种视图**。生成任务是从噪声出发、在交互条件下合成图像；编辑任务是从源图像出发、在交互条件下修改特定区域。两者共享对“交互关系”的结构化理解需求——生成模型学到的丰富交互语义可以反哺编辑任务，而编辑任务对身份保持的严格要求也能约束生成模型更精确地建模交互边界。

基于这一洞察，OneHOI提出将HOI生成与编辑统一到单一DiT框架中，通过三个关键设计显式建模交互结构：

1. **动词中介的注意力拓扑（Structured HOI Attention）**：强制主体（Subject）和客体（Object）Token之间不直接通信，必须通过动作（Action）Token作为中介，从而在注意力层面编码“动词约束交互”的归纳偏置。
2. **角色/实例感知的HOI Token注入（HOI Encoder）**：为每个HOI Token显式注入角色标签（主体/客体/动作）、实例索引和空间框编码，防止角色混淆和多实例混合。
3. **交互实例专属的位置编码（HOI RoPE）**：为不同交互实例分配独立的RoPE位置槽位，降低多HOI场景中的特征串扰。

这一统一框架使得单一模型能够同时支持文本引导的无布局编辑、布局引导的单/多交互编辑，以及从文本、布局、任意形状掩码或混合条件出发的HOI生成，首次实现了HOI生成与编辑的灵活多条件统一控制。

## 核心方法与创新机理

OneHOI的核心创新在于将HOI生成与编辑统一到单一扩散Transformer框架内，并通过四个协同的“变更槽位”（changed slots）显式建模交互结构，解决了现有方法中生成与编辑割裂、交互关系建模浅层化两大瓶颈。

### 从割裂到统一：共享结构化交互表示

现有HOI模型分裂为两个独立分支：生成模型（如**InteractDiffusion**）依赖布局但缺乏灵活控制，编辑模型（如**InteractEdit**、**HOIEdit**）无法解耦姿态与接触、难以扩展到多交互场景。OneHOI的核心洞察是：HOI生成与编辑本质上是同一条件去噪过程的两种视图——生成学到的丰富交互语义（接触模式、动词-物体几何关系）可反哺编辑，反之亦然。通过共享结构化交互表示并联合训练（交替生成与编辑batch，配合模态丢弃），单一模型在匹配算力下生成任务HOI准确率提升26.4%，无布局编辑HOI编辑成功率提升21.1%（Table 5），验证了统一框架的协同效应。

### 四个关键变更槽位：从浅层关联到深层交互建模

OneHOI在扩散Transformer（DiT）骨干上引入了四项结构性创新，每一项都针对现有方法的明确缺陷：

**1. 动作区域定义（Action Grounding）：从“Between”到“Union”**

**基线方法**（如InteractDiffusion）将动作区域定义为主体框与物体框之间的“Between”区域。**OneHOI**将其重新定义为二者的并集（$R_n^a = R_n^s \cup R_n^o$）。这一变更源于对注意力热力图的分析：动作Token的实际注意力分布覆盖主体和物体的完整区域，而非仅限二者之间（Figure 4）。并集区域更准确地匹配了交互的语义空间，为后续结构化注意力提供了正确的基础空间约束。

**2. HOI Token身份注入（HOI Encoder）：从无身份信号到显式角色/实例编码**

**基线方法**中，HOI Token缺少显式的角色（主体/物体）和实例身份信号，导致多交互场景中角色混淆和特征混合。**OneHOI**通过HOI Encoder注入紧凑的显式身份线索：将HOI token与可学习的角色嵌入、正弦实例索引和Fourier框编码拼接后经小型MLP处理（$\tilde{h}_n^r = \mathrm{MLP}([\mathrm{LN}(h_n^r); e_{\mathrm{box}}(b_n^r); e_{\mathrm{role}}(r); e_{\mathrm{inst}}(n)])$），再通过可学习的门控残差连接（$\tilde{h}_n^r = h_n^r + \tanh(\lambda) \cdot \tilde{h}_n^r$）缓慢引入条件信息，稳定训练过程。消融实验表明，该模块显著提升感知质量（ImageReward显著增加），为后续注意力拓扑约束提供了必要的身份基础。

**3. 结构化HOI注意力（Structured HOI Attention）：从全连接注意力到动词中介拓扑**

这是OneHOI最关键的创新。**基线方法**采用标准稠密注意力，HOI Token之间及HOI Token与图像Token之间无约束地交互，无法显式建模交互结构。**OneHOI**引入结构化注意力掩码（Figure 5），施加两层约束：
- **动词中介拓扑**：阻断主体Token与物体Token之间的直接连接（$S_n \leftrightarrow O_n$），强制所有交互信息经由动作Token（$A_n$）流动，显式建模“主体-动词-物体”的三元关系结构。
- **空间接地约束**：限制HOI Token仅关注其对应的空间区域——主体Token仅关注$R_n^s$，物体Token仅关注$R_n^o$，动作Token关注并集$R_n^a$（$M_{\mathcal{HT}}(q,k)$）。

消融实验（Table 4）证实，结构化HOI注意力的添加使HOI准确率和编辑一致性（Editability-Identity）出现第二次显著跃升，是提升交互正确性的最关键模块，验证了动词拓扑约束在关系建模中的核心作用。

**4. HOI RoPE：从共享位置编码到实例专属位置索引**

**基线方法**中，原始RoPE为所有交互实例分配共享的3D位置，导致多HOI场景中实例特征串扰。**OneHOI**提出HOI RoPE，为每个交互实例分配独立的位置槽位（$z_{\mathrm{HOI}}(n) = (0, T+n, T+n)$，其中$T = \max(H, W)$），在RoPE空间中有效分离不同交互实例的特征表示。消融实验表明，该模块在多HOI场景中进一步改善感知质量和编辑一致性，是完整模型性能的最后一步精化。

### 创新协同：从组件叠加到系统性突破

四个变更槽位并非孤立改进，而是形成递进式的系统创新链条：Action Grounding提供正确的空间语义基础 → HOI Encoder注入实例身份信号 → Structured HOI Attention在此基础上施加动词拓扑约束和空间接地 → HOI RoPE在多实例场景中分离特征。消融实验的定性可视化（Figure 10）直观展示了这一递进过程：逐步追加组件使交互的合理性持续提升，仅完整模型（包含全部四个模块）成功渲染出复杂的双手动作（同时“holding”和“petting”）。

### 方法边界与待验证问题

尽管创新显著，以下方面需要手动验证或进一步研究：
- 结构化注意力机制和HOI RoPE的设计能否推广到视频HOI编辑或三维场景，尚待验证。
- 联合训练中模态丢弃的最优概率组合（$p_{\mathrm{layout}}=0.25$、$p_{\mathrm{hoi}}=0.25$、$p_{\mathrm{txt}}=0.30$）对统一框架鲁棒性的影响，论文未做系统消融。
- HOI RoPE作为实例分离机制的通用性，是否适用于其他需要多实体分离的生成任务，仍为开放问题。

OneHOI 将 HOI 生成与编辑统一为**单一条件去噪过程**，其核心是一个称为 **Relational Diffusion Transformer（R-DiT）** 的 DiT 骨干网络。该框架的总体流水线如 Figure 3 所示，输入侧接收混合条件（文本提示、布局框、HOI 三元组标签），输出侧生成或编辑后的图像。整个框架由四个关键模块串联构成，形成“空间接地 → 身份注入 → 拓扑约束 → 实例分离”的递进式交互建模链。

![[assets/figures/papers/paper_list_l997_https_arxiv_org_abs_2604_14062/figures/004_Figure_3.jpg]]
*Figure 3: (a) OneHOI unifies HOI editing and generation tasks on a DiT backbone. The pipeline features an HOI Encoder to inject role and instance cues, and Structured HOI Attention to enforce verb-mediated topology and spatial grounding. (b, c) To separate instances, in contrast to the Original RoPE (b), HOI RoPE (c) provides unique positional indices for each interaction*

### 输入输出流

**输入**：对于一次前向传播，模型接收三类可选条件信号（训练时以随机丢弃实现多任务统一）：
- **全局文本提示**：描述场景语义，以 $p_{\mathrm{txt}}=0.30$ 的概率丢弃；
- **布局框**：为主体 $b_n^s$ 和客体 $b_n^o$ 提供空间位置，以 $p_{\mathrm{layout}}=0.25$ 的概率丢弃；
- **HOI 三元组标签**：每个交互实例 $n$ 包含动词 $a_n$、主体角色 $s$、客体角色 $o$，以 $p_{\mathrm{hoi}}=0.25$ 的概率丢弃。

**输出**：经 $28$ 步去噪采样后生成的图像，满足输入条件指定的交互语义和空间约束。

### 模块关系与数据流

四个核心模块按以下顺序作用于 HOI token 流，逐步构建结构化的交互表示：

1. **Action Grounding（AG，第 3.1 节）**  
   为每个交互实例引入动词语义 token $\mathcal{A}_n$ 和空间动作区域 $R_n^a$。动作区域定义为主体区域与客体区域的**并集**（$R_n^a = R_n^s \cup R_n^o$），而非先前工作（如 InteractDiffusion）使用的“Between”区域。Figure 4 的注意力热力图证实，Union 区域比 Between 区域更好地匹配动作 token 的实际注意力分布，为后续模块提供更准确的空间线索。

2. **HOI Encoder（Enc，第 3.2 节）**  
   向 HOI token 注入**角色感知**和**实例感知**的身份线索：通过可学习的角色嵌入 $e_{\mathrm{role}}(r)$ 区分主体/客体，通过正弦实例索引 $e_{\mathrm{inst}}(n)$ 区分不同交互实例，通过傅里叶框编码 $e_{\mathrm{box}}(b_n^r)$ 注入空间信息。三者拼接后经小型 MLP 得到增强表示 $\tilde{h}_n^r$，再通过可学习的门控残差连接 $\tilde{h}_n^r = h_n^r + \tanh(\lambda) \cdot \tilde{h}_n^r$ 缓慢引入条件信息以稳定训练。该模块解决了多交互场景中的角色混淆和实例混合问题。

3. **Structured HOI Attention（Attn，第 3.3 节）**  
   通过注意力掩码 $\mathcal{M}$ 强制执行两类结构约束（Figure 5）：
   - **HOI↔HOI 拓扑**：阻断主体 $S_n$ 与客体 $O_n$ 之间的直接注意力链路，强制信息必须经过动词 token $\mathcal{A}_n$ 中介传递，形成“主语→动词→宾语”的显式关系拓扑；
   - **HOI↔Image 空间接地**：约束 $S_n$、$O_n$、$\mathcal{A}_n$ 仅能关注图像中各自对应的空间区域（$R_n^s$、$R_n^o$、$R_n^a$），掩码公式为 $M_{\mathcal{HT}}(q,k)$，最终注意力计算为 $\mathrm{Attn}(Q,K,V,\mathcal{M}) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d}} + \mathcal{M}\right)V$。

4. **HOI RoPE（HRoPE，第 3.4 节）**  
   为每个交互实例 $n$ 分配独立的 RoPE 位置槽位 $z_{\mathrm{HOI}}(n) = (0, T+n, T+n)$，其中 $T = \max(H, W)$。与原始 RoPE 中所有 HOI token 共享位置索引不同，HRoPE 在 3D 位置空间中为不同交互实例创建隔离的表示子空间，有效降低多 HOI 场景中的特征串扰（Figure 3b vs. 3c）。

### 统一训练策略

OneHOI 基于 **Flux.1 Kontext** 的 MM-DiT 骨干进行 LoRA 微调（可调参数约 3.5 亿），训练 10K 步、batch size 16、使用 8-bit AdamW 优化器。批次在生成任务和编辑任务之间交替采样，并通过随机丢弃输入模态实现多条件统一——这种联合训练策略使生成任务学到的丰富交互语义（接触模式、动词-物体几何关系）能够反哺编辑任务，反之亦然，产生显著的协同效应（Table 5 证实统一模型在匹配算力下全面优于独立任务模型）。

OneHOI的核心创新在于将人体-物体交互（HOI）的结构化先验显式注入扩散Transformer（DiT）的去噪过程。该方法围绕四个关键模块构建，形成一个从空间接地到拓扑约束的递进式交互建模管线。

### 3.1 动作接地（Action Grounding）

动作接地的首要问题是**动作区域的合理定义**。先前工作**InteractDiffusion**采用主体框与物体框之间的“Between”区域作为动作的作用范围，但注意力热力图分析（Figure 4）表明，动作Token的实际注意力分布远超该狭窄区间，更倾向于覆盖主体和物体的整体区域。

基于这一观察，OneHOI将动作区域重新定义为**主体区域与物体区域的并集**：

$$R_n^a = R_n^s \cup R_n^o$$

其中 $R_n^s$、$R_n^o$ 和 $R_n^a$ 分别表示第 $n$ 个交互实例的主体、物体和动作的空间区域。这一简单修改使动作Token的注意力掩码与真实的注意力足迹更好对齐，为后续结构化建模提供了可靠的空间基础。

### 3.2 HOI编码器（HOI Encoder）

在原生DiT中，HOI Token缺乏显式的角色身份和实例归属信息，导致多交互场景中角色混淆或特征混合。HOI编码器通过向HOI Token流 $\mathbf{H}$ 注入紧凑的显式身份线索来解决这一问题。

具体而言，对于第 $n$ 个交互实例中角色为 $r \in \{\text{subject}, \text{object}, \text{action}\}$ 的HOI Token $h_n^r$，编码器首先将其与三类条件信息拼接后通过小型MLP进行增强：

$$\tilde{h}_n^r = \mathrm{MLP}([\mathrm{LN}(h_n^r); e_{\mathrm{box}}(b_n^r); e_{\mathrm{role}}(r); e_{\mathrm{inst}}(n)])$$

其中：
- $\mathrm{LN}(\cdot)$ 为层归一化；
- $e_{\mathrm{box}}(b_n^r)$ 为对应边界框的傅里叶位置编码；
- $e_{\mathrm{role}}(r)$ 为可学习的角色嵌入（区分主体/物体/动作）；
- $e_{\mathrm{inst}}(n)$ 为正弦实例索引嵌入（区分不同交互实例）。

为稳定训练初期的条件注入，增强后的Token通过**可学习门控残差**与原Token融合：

$$\tilde{h}_n^r = h_n^r + \tanh(\lambda) \cdot \tilde{h}_n^r$$

其中 $\lambda$ 为可学习标量，初始化为较小值，使条件信息缓慢引入，避免破坏预训练DiT的特征空间。

### 3.3 结构化HOI注意力（Structured HOI Attention）

这是OneHOI最核心的设计——通过**注意力掩码**显式约束Token间的信息流，强制实现动词中介的交互拓扑和空间接地。

**HOI-HOI拓扑约束**：在HOI Token内部，直接阻断主体Token（$\mathcal{S}_n$）与物体Token（$\mathcal{O}_n$）之间的注意力通路，强制所有主体-物体信息交换必须经由动作Token（$\mathcal{A}_n$）中转。这一设计显式编码了“动词中介”的交互结构——主体通过动作作用于物体。

**HOI-Image接地约束**：HOI Token与图像Token之间的注意力被限制在各自对应的空间区域内：

$$M_{\mathcal{HT}}(q,k) = \begin{cases} 0, & q \in \mathcal{S}_n \text{ and } k \in R_n^s, \\ 0, & q \in \mathcal{O}_n \text{ and } k \in R_n^o, \\ 0, & q \in \mathcal{A}_n \text{ and } k \in R_n^a, \\ -\infty, & \text{otherwise}. \end{cases}$$

该掩码确保主体Token仅关注主体区域内的图像特征，物体Token仅关注物体区域，动作Token则关注整个并集区域 $R_n^a$。被屏蔽位置赋值为 $-\infty$，经softmax后注意力权重归零。

最终的注意力计算将结构化掩码 $\mathcal{M}$ 注入标准缩放点积注意力：

$$\mathrm{Attn}(Q,K,V,\mathcal{M}) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d}} + \mathcal{M}\right)V$$

消融实验证实，结构化HOI注意力是提升交互正确性（HOI准确率和编辑一致性）的**最关键模块**，其添加带来了第二次显著性能跃升（Section 4.7）。

### 3.4 HOI RoPE

原始DiT的3D RoPE为所有Token分配统一的连续位置索引，在多交互场景中不同实例的HOI Token共享相近位置编码，导致特征串扰。HOI RoPE为每个交互实例分配**独立的位置槽位**：

$$z_{\mathrm{HOI}}(n) = (0, T+n, T+n), \quad \mathrm{where} \quad T = \max(H, W)$$

其中 $H$、$W$ 为图像潜空间的高和宽。第 $n$ 个交互实例的所有HOI Token（主体、物体、动作）共享同一位置索引 $(0, T+n, T+n)$，而不同实例之间被有效分离。这一设计使RoPE的频率基能够自然区分不同交互实例，在多HOI场景中显著改善感知质量和编辑一致性。

## 实验与关键发现

### 核心实验设计

OneHOI 在三个任务维度上接受评估：**无布局 HOI 编辑**（IEBench 基准）、**布局引导 HOI 编辑**（含单交互与多交互）以及 **HOI 生成**（HICO-DET 基准）。评估指标覆盖空间可控性、交互正确性、身份保持与感知质量四个层面。空间可控性通过 PViC 检测器计算预测框与目标框的平均交并比 $ \mathrm{mIoU} = \frac{1}{2} \big( \mathrm{IoU}(b^s, \hat{b}^s) + \mathrm{IoU}(b^o, \hat{b}^o) \big) $ 衡量；交互正确性通过 HOI Accuracy（PViC 在指定区域内检测到目标交互即记为成功）和 HOI Editability 衡量；身份保持与编辑质量的综合指标为 Editability-Identity（EI），定义为 $ \mathrm{EI} = \frac{2 \times \mathrm{HOI Editability} \times \mathrm{Identity Consistency}}{\mathrm{HOI Editability} + \mathrm{Identity Consistency}} $ 的调和平均。

对比基线覆盖三类方法：(1) HOI 编辑方法 **InteractEdit**、**HOIEdit**；(2) 通用编辑方法 **Flux.1 Kontext**（Black Forest Labs, 2024）、**Qwen Image Edit**；(3) 布局条件生成方法 **GLIGEN**（Li et al., 2023）、**InstanceDiffusion**、**MIGC++** 以及 HOI 感知生成方法 **InteractDiffusion**。闭源模型（如 Nano Banana）单独列出。

### 无布局 HOI 编辑：交互语义解耦与身份保持

在 IEBench 的无布局编辑任务上，OneHOI 在所有指标上均显著超越先前方法（Table 1）。**Editability-Identity 达到 0.638，较最强先前方法 Qwen Image Edit（0.580）提升 10.0%；HOI Editability 达到 0.596，较 InteractEdit（0.514）提升 16.0%**。这一优势源于结构化 HOI 注意力机制对动词拓扑的强制约束——模型在编辑交互时必须通过动词 Token 中介主体与客体的信息流，从而避免编辑过程中角色错位或身份丢失。定性对比（Figure 6）显示，基线方法常出现姿态未改变、主体身份丢失或生成伪影等问题，而 OneHOI 能在保持人物身份的前提下准确渲染新交互。

![[assets/figures/papers/paper_list_l997_https_arxiv_org_abs_2604_14062/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison for layout-free HOI editing on IEBench benchmark. Our method significantly outperforms others across all metrics for editing and image quality. Best results are in bold, second best are underlined. Final row shows the closed-source baseline*

![[assets/figures/papers/paper_list_l997_https_arxiv_org_abs_2604_14062/figures/012_Figure_6.jpg]]
*Figure 6: Qualitative comparison for layout-free HOI editing. Our method successfully renders the new interaction while preserving identity. In contrast, baseline methods often produce artifacts, fail to change the pose, or lose the subject’s identity*

### 布局引导编辑：空间精度与多交互扩展

布局引导的单交互编辑任务中，OneHOI 的 Spatial Score（mIoU）达到 0.822，较 InteractEdit+InteractDiffusion 组合（0.749）提升 9.7%（Table 2），验证了 Action Grounding 中 Union 区域定义和 HOI↔Image 接地掩码对空间对齐的增强作用。在多交互编辑基准 MultiHOIEdit 上，OneHOI 作为首个基线取得 Spatial Score 0.675 和 Editability-Identity 0.435，证明 HOI RoPE 通过为每个交互实例分配独立位置索引 $ z_{\mathrm{HOI}}(n) = (0, T+n, T+n) $ 有效降低了多实例间的特征串扰。

![[assets/figures/papers/paper_list_l997_https_arxiv_org_abs_2604_14062/figures/009_Table_2.jpg]]
*Table 2: Quantitative results for our novel layout-guided HOI editing tasks. We report strong performance for both single- and multi-HOI editing, establishing the first baseline for these new capabilities*

### HOI 生成：从物体放置到关系理解

在 HICO-DET 生成任务上，OneHOI 在空间可控性和感知质量上均优于现有方法（Table 3）。Spatial Score 达到 0.6104（vs. InteractDiffusion 0.5768，提升 5.8%），ImageReward 达到 0.5224（vs. Eligen 0.3921，提升 33.2%）。值得注意的是，HOI Accuracy 仅微弱领先（0.4528 vs. 0.4505），但定性分析（Figure 7）揭示了更深层的差异：物体级方法虽能正确放置实体，却无法合成指定的交互关系，而 OneHOI 生成的交互在语义和几何上均保持一致性，体现了动词拓扑约束带来的关系理解能力。

![[assets/figures/papers/paper_list_l997_https_arxiv_org_abs_2604_14062/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison for HOI generation task. Our method outperforms leading layout-conditioned and HOI-aware models on both controllability and image quality metrics*

### 消融实验：模块贡献的因果链

Table 4 的逐模块消融揭示了从基础空间感知到深层关系建模的递进因果链：

![[assets/figures/papers/paper_list_l997_https_arxiv_org_abs_2604_14062/figures/015_Table_4.jpg]]
*Table 4: Ablation study on core components. AG: Action Grounding, Enc: HOI Encoder, Attn: HOI Attention, HRoPE: HOI RoPE, EI: Editability-Identity, IR: ImageReward*

1. **Action Grounding（AG）** 是理解交互的基石。引入 AG 后，生成和编辑指标均出现大幅跃升，验证了 Union 区域 $ R_n^a = R_n^s \cup R_n^o $ 比 InteractDiffusion 的 “Between” 区域更准确捕捉动作注意力的分布（Figure 4 的热力图对比提供了直接证据）。

2. **HOI Encoder（Enc）** 通过注入角色嵌入、实例索引和框编码，显著提升感知质量（ImageReward 增加），防止多实例场景中的角色混淆。

3. **Structured HOI Attention（Attn）** 是提升交互正确性的最关键模块。添加该模块后，HOI Accuracy 和 Editability-Identity 出现第二次显著跃升，直接证实了动词中介拓扑约束对关系建模的核心作用——阻止主体↔客体直连、强制经动词 Token 路由信息流，使模型学到结构化的交互语义。

4. **HOI RoPE（HRoPE）** 提供最后的精炼步骤，通过实例专属位置编码进一步解耦多交互特征，提升感知质量和编辑一致性。

定性消融可视化（Figure 10）直观展示了模块叠加效果：仅基础模型无法渲染复杂双手动作（如同时“holding”和“petting”），逐步添加 AG→Enc→Attn→HRoPE 后，交互的物理合理性逐步增强，完整模型成功合成该复杂场景。

### 统一训练 vs. 单任务训练：跨任务协同效应

Table 5 的对比实验验证了统一框架的核心主张——HOI 生成与编辑本质上是同一条件去噪过程的两种视图。**在匹配算力下，统一模型较独立任务模型在生成任务上 HOI Accuracy 提升 26.4%（0.224 vs. 0.177），在无布局编辑任务上 HOI Editability 提升 21.1%（0.562 vs. 0.464）**。这一协同效应的机制在于：生成任务中学到的接触模式、动词-物体几何关系等丰富交互语义，通过共享的结构化交互表示迁移到编辑任务中；反之，编辑任务对交互细节的精确控制需求也反哺了生成质量。

### 失败模式与边界条件

尽管整体性能领先，OneHOI 存在以下已知边界：

- **检测器偏差传导**：HOI-Edit-44K 数据集构建依赖 PViC 检测器和 DINOv2 相似度过滤，约 90% 候选对被丢弃。这意味着模型学到的“正确交互”定义受限于检测器的判别能力，在检测器失败的场景（如严重遮挡、罕见视角）可能出现系统性偏差。
- **真实编辑对匮乏**：训练数据中合成图像占比大，虽引入 HICO-DET 真实图像联合训练，但对真实场景编辑的泛化能力仍需独立验证。
- **多交互编辑基准局限**：MultiHOIEdit 仅含 200 个编辑任务且由论文自行提出，缺乏外部基准交叉验证，多交互编辑的评估结论需要后续工作确认。
- **计算成本**：基于 Flux.1 Kontext（12B）的 DiT 架构进行 LoRA 微调，推理需 28 步采样，不适合实时应用场景。

### 数据集构建与分布

HOI-Edit-44K 数据集覆盖丰富的交互对象和动作类别。附录中的 Treemap 可视化（Figure 16、17）展示了对象类别（如运动器材、乐器、餐具等）和动作类别（如 hold、ride、eat 等）的频率分布，MultiHOIEdit 基准的 Sankey 图（Figure 21）则呈现了源动作到目标动作的编辑转移全貌。这些分布信息对理解模型的能力覆盖范围和潜在长尾盲区具有参考价值。

## 定位与知识库关联

### 1. 问题定位：从分裂的生成/编辑到统一交互建模

人体-物体交互（HOI）的视觉生成与编辑长期处于分裂状态。生成模型依赖布局条件实现空间可控性，但缺乏对交互语义的深层理解；编辑模型虽能响应文本指令，却难以解耦姿态、接触与身份保持，且几乎无法扩展到多交互场景。OneHOI 的核心判断是：这一分裂并非任务本质所致，而是现有扩散 Transformer（DiT）架构缺少显式的交互关系建模机制。通过将 HOI 生成与编辑统一为同一条件去噪过程的两种视图，并设计一套共享的结构化交互表示，OneHOI 试图在单一框架内同时解决两个方向的控制瓶颈。

### 2. 与现有基线的结构性差异

OneHOI 的方法谱系可从三个维度定位：架构基础、HOI 感知机制、任务统一性。

**架构基础：从对象级 DiT 到关系 DiT。** OneHOI 以 **Flux.1 Kontext**（Black Forest Labs, 2024）的 MM-DiT 骨干为起点，通过 LoRA 进行参数高效微调（可调参数约 3.5 亿）。这一选择继承了 DiT 在图像生成中的强先验，但原生 DiT 仅具备对象级别的接地能力（如 **GLIGEN** (Li et al., 2023)、**Eligen** (Li et al., 2024)），无法建模“主体-动作-客体”的三元交互结构。OneHOI 在此基础上引入 Relational Diffusion Transformer（R-DiT），将 DiT 从对象接地升级为关系接地。

**HOI 感知机制：从隐式到显式结构化。** 现有 HOI 感知方法存在两个关键设计缺陷：

- **动作区域定义**：**InteractDiffusion** 使用主体框与物体框之间的“Between”区域作为动作的注意力范围。OneHOI 通过注意力热力图分析（Figure 4）揭示，实际的动作 token 注意力分布更接近主体区域与物体区域的并集（$R_n^a = R_n^s \cup R_n^o$），而非两者之间的狭长地带。这一发现构成了 Action Grounding 模块的设计依据。

- **交互拓扑建模**：现有方法（如 **InteractEdit**、**HOIEdit**）将 HOI 视为各角色 token 的独立编码，缺乏对交互结构的显式约束。OneHOI 的结构化 HOI 注意力（Structured HOI Attention）直接切断了主体与客体 token 之间的直接注意力链路，强制信息通过动词 token 中介流动，从而在注意力拓扑层面编码了“主体-动词-客体”的三元关系。同时，HOI↔图像注意力被约束在各自的空间区域内（$M_{\mathcal{HT}}$ 掩码），防止 token 关注无关区域。

- **多实例分离**：在标准 RoPE 下，多个交互实例的 HOI token 共享相同的位置槽位，导致特征串扰。HOI RoPE 为每个交互实例分配独立的位置索引 $z_{\mathrm{HOI}}(n) = (0, T+n, T+n)$，从位置编码层面实现实例解耦。

**任务统一性：从独立训练到联合训练。** 与 **InteractDiffusion**（仅生成）和 **InteractEdit**（仅编辑）的任务特定设计不同，OneHOI 通过模态丢弃策略（以 $p=0.25$ 丢弃布局、$p=0.25$ 丢弃 HOI 标签、$p=0.30$ 丢弃文本提示）实现生成与编辑的联合训练。消融实验（Table 5）证实，统一模型在相同训练量下，生成任务的 HOI 准确率较任务特定模型提升 26.4%（0.224 vs 0.177），无布局编辑的 HOI Editability 提升 21.1%（0.562 vs 0.464），表明生成任务中学到的接触模式与动词-物体几何关系可正向迁移至编辑任务，反之亦然。

### 3. 适用边界与局限

**数据依赖与检测器偏差。** OneHOI 的训练数据 HOI-Edit-44K 的构建严重依赖现有 HOI 检测器 PViC 和身份相似度模型 DINOv2 的自动过滤——约 90% 的候选编辑对被丢弃。这一流程虽保证了数据质量，但可能将检测器的系统性偏差编码进训练分布，使模型对 PViC 检测失败或 DINOv2 评分模糊的交互类型表现不稳定。此外，训练数据中 Flux.1 生成的合成图像占比大，尽管引入 HICO-DET 真实图像进行联合训练，真实编辑对的缺乏仍可能限制在自然图像上的泛化能力。

**多交互编辑的基准局限。** MultiHOIEdit 基准仅包含 200 个编辑任务，且由论文自行提出，缺乏外部独立验证。目前尚无其他多交互编辑基线可供对比，OneHOI 在该基准上的结果（Spatial Score 0.675, Editability-Identity 0.435）仅能作为首个参考点，其绝对性能水平仍需更大规模和更多样化的基准来校准。

**架构与计算约束。** 模型基于 Flux.1 Kontext（约 12B 参数）进行 LoRA 微调，实际可调参数量约 3.5 亿，未对完整 DiT 架构做从零训练。这一设计虽降低了训练成本，但也意味着模型性能受限于基座模型的能力上限。推理需 28 步采样，结合 12B 参数规模，计算成本较高，不适合实时或资源受限的应用场景。

**长尾交互的未知泛化性。** 训练数据覆盖的交互类别有限，对于未在训练集中出现的动作-物体组合（长尾或零样本交互），结构化注意力机制和 HOI Encoder 能否正确泛化尚未得到验证。动词拓扑约束的有效性可能依赖于训练期间见过的交互模式。

### 4. 开放问题

1. **跨模态与跨场景推广**：结构化 HOI 注意力和 HOI RoPE 的设计原理——动词中介的拓扑约束与实例级位置分离——是否可推广到视频 HOI 编辑或三维场景中的交互生成？视频中的时序一致性和三维空间中的多视角一致性对注意力掩码和位置编码提出了不同要求。

2. **弱监督与数据效率**：HOI-Edit-44K 的构建依赖大量自动化过滤，能否通过弱监督或自监督方式（如利用未配对的 HOI 图像与文本描述）减少对配对编辑数据的依赖？联合训练中的模态丢弃策略已暗示了某种形式的弱监督潜力，但尚未被系统探索。

3. **HOI RoPE 的通用性**：HOI RoPE 为每个交互实例分配独立位置槽位的设计，本质上是一种通用的多实体分离策略。这一机制是否适用于其他需要实例级解耦的生成任务（如多人物场景生成、多物体关系生成），值得进一步验证。

4. **模态丢弃的最优策略**：联合训练中布局、HOI 标签和文本提示的丢弃概率（0.25/0.25/0.30）是经验设定的。这些概率的最优组合及其对统一框架在不同任务上鲁棒性的影响，尚未通过系统消融确定。

5. **真实场景的编辑鲁棒性**：当前评估主要基于 IEBench 和自建的 MultiHOIEdit，两者均以合成或受控场景为主。模型在真实用户拍摄的复杂背景、遮挡严重或光照极端的照片上的编辑鲁棒性，仍需更大规模的真实场景用户研究来验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/OneHOI_Unifying_Human_Object_Interaction_Generation_and_Editing.pdf]]

---
title: "PriorMDM: Human Motion Diffusion as a Generative Prior"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: "paperPDFs/ICLR_2024/PriorMDM:_Human_Motion_Diffusion_as_a_Generative_Prior.pdf"
project_link: https://priormdm.github.io/priorMDM-page/
code_link: https://github.com/priorMDM/priorMDM
aliases:
- PCMDCD
- PriorMDM
tags:
- ICLR_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将预训练的运动扩散模型（MDM）固定为生成先验，通过设计推理时的组合策略（顺序拼接、并行协调、模型混合）以零样本或少样本突破数据局限。
primary_logic: 预训练的运动扩散模型已编码丰富的动态先验；关键不再是收集更多数据，而是经济地组合利用已有先验，通过冻结或微调前置模型并引入轻量通信或混合机制，实现超出训练分布的运动合成。
claims:
- DoubleTake在BABEL长序列生成上取得FID 1.04，显著优于TEACH的1.12；过渡FID (70帧) 仅1.88，远低于TEACH的3.86。
- ComMDM在3DPW两人前缀完成的用户研究中，所有三项评估（合理性、连贯性、交互质量）均优于MRT和MDM。
- 在HumanML3D关节控制任务中，DiffusionBlending组合左腕+轨迹的FID仅为0.22，而MDM inpainting为1.18。
- DoubleTake在HumanML3D上的最佳配置FID 0.60，消融实验证实软遮罩与过渡嵌入对过渡质量至关重要。
---

# PriorMDM: Human Motion Diffusion as a Generative Prior

> [!tip] 核心洞察
> 预训练的运动扩散模型已编码丰富的动态先验；关键不再是收集更多数据，而是经济地组合利用已有先验，通过冻结或微调前置模型并引入轻量通信或混合机制，实现超出训练分布的运动合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | PriorMDM：以人体运动扩散作为生成先验 |
| 英文题名 | PriorMDM: Human Motion Diffusion as a Generative Prior |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://arxiv.org/abs/2303.01418) · [Project](https://priormdm.github.io/priorMDM-page/) · [Code](https://github.com/priorMDM/priorMDM) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PriorMDM Composition Methods (DoubleTake, ComMDM, DiffusionBlending) |
| Dataset | BABEL, 3DPW, HumanML3D |

> [!tip] 效果简介
> - BABEL (长序列生成) 上，FID (↓) DoubleTake 1.04 vs TEACH 1.12 (-0.08 (better))。
> - BABEL (过渡质量, 70帧) 上，Transition FID (↓) DoubleTake 1.88 vs TEACH 3.86 (-1.98 (better))。
> - 3DPW (两人前缀完成, 3秒) 上，Root Error (m ↓) ComMDM 0.30 vs MDM (no Com) 0.54 (-0.24 (better))。

## 概要

高质量人体运动数据的捕捉与标注成本极高，导致现有生成模型大多局限于单人、短时序（≤10秒）的运动合成，难以应对**长序列生成、多人交互协调以及关节级精细控制**等复杂任务。PriorMDM 提出一种系统性的“先验组合”范式：将预训练的**运动扩散模型（MDM）**固定为生成先验，通过设计三类推理时或轻量微调的组合策略，以零样本或少样本方式突破数据分布的限制。

核心思路不再是收集更多标注数据，而是**经济地复用已编码的丰富动态先验**——冻结或微调前置模型，并引入轻量通信或混合机制，实现超出训练分布的运动合成。具体而言，PriorMDM 包含三种互补的组合方法：

- **DoubleTake**：面向任意长度序列生成，通过双阶段推理（批量生成+过渡精炼）与软遮罩机制，在不重新训练的情况下实现连贯的长动画合成。
- **ComMDM**：在冻结的 MDM Transformer 层间插入单层通信模块，以极少样本学习两人交互的协调，支持文本驱动的双人生成与前缀补全。
- **DiffusionBlending**：微调专用控制模型并在采样时线性混合多个模型的去噪预测，实现对多关节与轨迹的灵活、精确组合控制。

实验结果表明，该方法在多个基准上均取得显著提升：
- 在 BABEL 长序列生成中，DoubleTake 的 FID 达到 **1.04**（TEACH 为 1.12），过渡段 FID 仅为 **1.88**（TEACH 为 3.86）。
- 在 3DPW 两人前缀补全中，ComMDM 的 Root Error 降至 **0.30 m**（MDM 为 0.54 m），用户研究在合理性、连贯性与交互质量上全面优于 MRT 与 MDM。
- 在 HumanML3D 关节控制任务中，DiffusionBlending 组合左腕+轨迹的 FID 仅为 **0.22**（MDM Inpainting 为 1.18），微调策略亦使轨迹控制 FID 从 0.98 降至 **0.54**。

消融研究进一步验证了各组件的关键作用：软遮罩与过渡嵌入是 DoubleTake 过渡质量的核心保障；ComMDM 的通信层置于 Transformer 高层且仅需一层即可达到最优；微调专用控制模型相比直接 Inpainting 在保真度与多样性上均有质的飞跃。

该工作的局限性在于：长序列中远距离区间可能出现语义不一致；两人交互对未见交互类型的泛化有限，且未保证真实物理接触；三种组合方法的跨领域适用性尚待验证。



### 问题背景

人体运动生成是计算机视觉与图形学中的核心任务，其应用涵盖动画制作、虚拟现实、人机交互等领域。近年来，扩散模型在运动生成中展现出强大的能力，能够产生高质量、多样化的运动序列。然而，现有方法面临一个根本性瓶颈：**高质量运动数据的捕捉与标注成本极为高昂**。这导致当前生成模型普遍受限于单人短序列（通常不超过10秒），难以处理以下三类复杂任务：

- **长序列生成**：生成跨越多段语义的任意长度运动，并保证段间过渡的自然流畅。
- **多人交互运动**：生成两人协同的运动，需要捕捉人物间的空间协调与语义关联。
- **关节级精细控制**：对特定身体部位（如手腕、脚踝）或全局轨迹施加精确约束，同时保持整体运动的合理性。

这些任务的共同难点在于，直接收集覆盖所有场景的训练数据在经济上不可行，迫使研究者寻找超越数据规模限制的解决方案。

### 现有方法缺口

针对上述任务，已有工作尝试了不同的技术路线，但均存在显著局限：

- **长序列生成**：**TEACH**（Athanasiou et al., 3DV 2022）采用顺序组合策略，将多个短片段拼接为长序列。然而，其过渡处理较为粗糙，生成的片段间衔接生硬，且容易出现滑步等物理不合理现象。
- **多人运动预测**：**MRT**（Wang et al., NeurIPS 2021）等基线方法为每个人物独立生成运动，完全忽略了人物间的交互协调，导致生成结果缺乏语义一致性和空间配合。
- **关节/轨迹控制**：**MDM Inpainting**（Tevet et al., ICLR 2023）通过在采样过程中直接填入给定的控制信号来实现运动修复。但当控制约束较为复杂（如同时控制手腕位置和全局轨迹）时，该方法生成的运动会严重偏离自然分布，甚至完全忽略输入特征。

这些方法的共同缺陷在于，它们要么需要针对特定任务重新训练模型，要么在推理时采用简单的拼接或填充策略，未能有效利用预训练模型中已编码的丰富运动先验。

### 核心动机与洞察

本文的核心洞察是：**预训练的运动扩散模型（MDM）已经编码了丰富的动态先验，关键不再是收集更多数据，而是如何经济地组合利用这些已有先验。** 基于这一思想，PriorMDM提出将预训练MDM固定为生成先验，通过设计三种推理时的组合策略，以零样本或少样本的方式突破数据局限：

1. **DoubleTake**：针对长序列生成，通过双阶段推理（批量生成 + 过渡精炼）与软遮罩机制，在无需额外训练的条件下实现任意长度运动的平滑拼接。
2. **ComMDM**：针对两人交互，在冻结的MDM之间插入轻量通信模块，仅需极少量样本即可学习人物间的协调关系。
3. **DiffusionBlending**：针对多关节组合控制，通过微调专用控制模型并在采样时线性混合，实现灵活且精确的复合控制。

这一思路的优越性在于其**经济性**与**通用性**：冻结或微调前置模型、引入轻量通信或混合机制，即可在多个任务上实现超出训练分布的运动合成，避免了为每个新任务从头收集数据和训练模型的高昂成本。



## 核心方法与创新机理

PriorMDM的核心创新不在于提出新的生成模型架构，而在于**将预训练的运动扩散模型（MDM）视为不可变动的生成先验**，通过三种推理时或轻量微调的**组合策略**，突破原始模型在数据规模与任务复杂度上的固有限制。这一范式的关键洞察是：预训练模型已编码丰富的动态先验，瓶颈并非收集更多数据，而是如何经济地组合利用已有先验。

### 从“单次生成”到“任意长度序列”：DoubleTake的双阶段推理

基线方法（如**TEACH**, Athanasiou et al., 3DV 2022）受限于MDM的单次生成长度上限（≤10秒），且缺乏对区间过渡的显式处理。DoubleTake通过**双阶段推理**改变了这一局面：

- **第一take（批量生成与handshake）**：将所有文本提示对应的运动区间在单批次中并行生成。在每一步去噪过程中，通过强制相邻区间的重叠段相等（handshake override），确保全局一致性。其核心操作为：

$$\tau_i = (1 - \vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$$

即对前序运动后缀与当前运动前缀进行逐帧线性加权，使两者共享同一过渡段。

- **第二take（过渡精炼）**：对第一take生成的过渡区域施加部分噪声，并引入**软遮罩（soft blending mask）**与**过渡嵌入（transition embedding）**。软遮罩在硬遮罩与软遮罩之间线性渐变，允许模型在去噪时适度修正过渡帧，而非强制覆盖；过渡嵌入则作为可学习的位置编码，指示当前帧是否属于过渡段，提升模型对过渡区域的感知能力。

这一设计将长序列生成从“逐段拼接”的串行范式转变为“批量生成+过渡精炼”的并行范式，实现了任意长度的零样本运动合成。

### 从“独立生成”到“交互协调”：ComMDM的单层通信块

多人运动生成的基线方法（如**MRT**, Wang et al., NeurIPS 2021）通常独立为每个人生成运动，忽略人物间的交互。ComMDM的解决方案极为轻量：在**两个冻结的MDM模型**之间插入**单层transformer通信块**。该模块接收两个MDM在特定transformer层（实验表明第8层最优）的中间激活作为输入，输出一个校正项加回原激活，从而协调两人的运动生成。此外，ComMDM可选择性预测两人的初始姿态，进一步增强交互的物理合理性。

关键创新在于**最小化可训练参数**——仅训练一个单层通信块，而非微调整个模型，使得在极少量两人运动样本上即可学习交互模式。

### 从“单一控制”到“灵活组合”：微调控制模型与DiffusionBlending

基线方法直接使用MDM的inpainting采样实现关节或轨迹控制（**MDM Inpainting**, Tevet et al., ICLR 2023），但对复杂控制信号表现不佳——例如轨迹控制中产生大量足部滑动，手部控制中手部不自然地弯向背后。

PriorMDM的改进分为两步：
1. **微调专用控制模型**：在训练时遮蔽控制特征（如左腕位置、根轨迹）对应的噪声，使模型学会精确遵循控制信号。
2. **DiffusionBlending采样混合**：在推理时，通过线性插值混合多个微调模型的输出：

$$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$$

其中$G^a$和$G^b$是分别针对不同控制信号微调的扩散模型，$s$控制混合权重。这一机制将classifier-free guidance的思想推广到任意两个“对齐”的扩散模型之间，使得“左腕+轨迹”等复合控制信号可以灵活组合，而无需为每种组合重新训练模型。

### 创新总结

三种方法的共同特征在于**对预训练先验的零侵入或微侵入利用**：DoubleTake完全冻结MDM，仅在推理时引入handshake与软遮罩；ComMDM冻结两个MDM，仅训练单层通信块；DiffusionBlending微调多个小型控制模型，在采样时混合。这一设计哲学使得PriorMDM能够以极低的额外成本，将单人短序列生成模型扩展至长序列、多人交互、精细关节控制等超出训练分布的下游任务。



PriorMDM 并非重新训练一个通用模型，而是将预训练的运动扩散模型（MDM）固化为生成先验，在其上构建三种互补的组合策略，以零样本或少量样本的方式突破原始模型的分布边界。整体框架由三个独立但共享同一基座模型的模块构成：

- **DoubleTake**：面向任意长度序列生成的推理时组合方法，无需额外训练。
- **ComMDM**：面向两人交互运动生成的轻量通信模块，仅需少量样本训练。
- **DiffusionBlending**：面向多关节/轨迹灵活控制的模型混合方法，结合微调与采样时插值。

三个模块共享的核心基座是 **MDM**（Tevet et al., ICLR 2023），一个基于 DDPM 框架的文本驱动运动扩散模型。其前向加噪过程为：

$$q(X_t | X_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} X_{t-1}, (1 - \alpha_t) I)$$

MDM 建模逆向去噪过程：给定噪声运动 $X_t$、噪声步长 $t$ 和文本条件 $c$（经 CLIP 编码），预测干净运动 $\hat{X}_0$。所有组合方法均以该固定或微调的 MDM 为生成先验，通过不同的输入组织与模型交互方式实现功能扩展。

### DoubleTake：长序列生成的推理时流水线

DoubleTake 采用双阶段推理（two-take）实现任意长度的运动序列生成。给定一组文本提示序列 $\{c_1, c_2, ..., c_k\}$ 及其对应的时间区间，该方法在单批次内并行生成所有区间，并通过以下机制保证区间间的连贯性：

1. **第一 take（批量生成与握手）**：同时为每个区间采样运动片段 $S_i$，并在相邻区间之间维护长度为 $h$ 的握手（handshake）重叠段。每一步去噪时，握手区域被强制覆盖为前序片段后缀与当前片段前缀的帧级线性加权平均：

   $$\tau_i = (1 - \vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$$

   其中 $\vec{\alpha}$ 为线性权重向量，$\odot$ 表示逐元素乘法。这一强制约束使得相邻片段在重叠区域达成一致，拼接后形成初步的长序列。

2. **第二 take（过渡精炼）**：对第一 take 生成的握手区域施加部分噪声，然后以相邻区间为条件重新去噪。关键设计是**软遮罩（soft blending mask）**：在硬遮罩 $\mathbf{M}_{hard}$ 与软遮罩 $\mathbf{M}_{soft}$ 之间设置 $b$ 帧的线性过渡带，使得每一步去噪时，原始生成的运动部分帧得以适度修正以适配过渡。这一机制在保持原有运动内容的同时，显著提升过渡的自然度。

3. **过渡嵌入（Transition Embedding）**：可学习的嵌入向量，指示每一帧是否属于过渡段，注入 MDM 的 transformer 层以增强模型对过渡区域的感知能力。

### ComMDM：两人交互的通信协调

ComMDM 在冻结的两个 MDM 实例之间插入一个单层 transformer 通信块，以协调两人的运动生成。该模块接收两个 MDM 在第 $L_n$ 层 transformer 的中间激活作为输入，输出对应的修正项，加回原激活以校正运动表征。此外，ComMDM 可选地预测两人的初始姿态 $D^i$，为生成提供空间参照。由于仅训练通信块而冻结基座模型，该方法在极少训练样本下即可习得交互模式。

### DiffusionBlending：多控制信号的模型混合

对于关节级精细控制，PriorMDM 首先针对特定控制信号（如左腕轨迹、根轨迹）微调专用 MDM 实例（训练时遮蔽控制特征对应的噪声），然后在采样时通过线性混合实现多信号的任意组合。给定两个对齐的扩散模型 $G^a$ 和 $G^b$（分别条件于控制信号 $c_a$ 和 $c_b$），DiffusionBlending 的采样公式为：

$$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$$

其中 $s$ 为混合权重。这一机制将 classifier-free guidance 的思想泛化至任意两个对齐扩散模型的组合，使生成运动同时满足多个控制约束（如同时控制左腕轨迹和根轨迹），而无需为每种组合重新训练模型。

三个模块的输入输出关系清晰：DoubleTake 输入文本序列与区间划分，输出拼接后的长序列运动；ComMDM 输入两人文本描述，输出同步的两人运动；DiffusionBlending 输入控制信号（关节位置/轨迹）及文本条件，输出受控运动。所有输出均为人体运动序列表示，可直接用于下游动画或分析任务。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/001_Figure_1.jpg]]
*Figure 1: We suggest three novel motion composition methods, all based on the recent Motion Diffusion Model (MDM). (Left) Sequential composition generating an arbitrary long motion with text control over each time interval. (Middle) Parallel composition generating two-person motion from text. A different color represents a different person - both are generated simultaneously given the text prompt. (Right) Model composition achieving accurate and flexible control by blending models with different control signals - here writing “hello" in mid-air*



PriorMDM 的核心架构并非重新训练一个全新模型，而是将预训练的运动扩散模型 MDM（Tevet et al., ICLR 2023）固定为生成先验，在其上构建三种互补的组合策略。以下逐一剖析各模块的机制与关键公式。

### 3.1 基座模型：MDM 扩散先验

MDM 是一个基于 DDPM 框架的去噪扩散模型。其前向加噪过程为：

$$q(X_t | X_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} X_{t-1}, (1 - \alpha_t) I)$$

其中 $X_t$ 表示第 $t$ 步加噪后的运动序列，$\alpha_t$ 为噪声调度参数。模型学习的是反向去噪过程：给定加噪运动 $X_t$、噪声步长 $t$ 以及文本条件 $c$（经 CLIP 编码），预测干净运动 $\hat{X}_0$。这一预训练先验编码了丰富的短序列运动动态，是后续所有组合方法的基础。

### 3.2 DoubleTake：长序列零样本生成

DoubleTake 是推理时的双阶段方法，旨在突破 MDM 仅能生成 10 秒以内短序列的限制。其核心瓶颈在于：直接拼接多个独立生成的短序列会导致过渡段生硬、不自然。DoubleTake 通过“握手”机制与软遮罩精炼两步解决此问题。

**第一 Take：批量生成与握手约束。** 将长序列按文本提示划分为多个区间，在单批次内并行生成所有区间。为保证相邻区间在重叠段的一致性，引入握手强制机制：

$$\tau_i = (1 - \vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$$

其中 $S_{i-1}[-h:]$ 为前一区间的后缀 $h$ 帧，$S_i[:h]$ 为当前区间的前缀 $h$ 帧，$\vec{\alpha}$ 为线性权重向量。在每一步去噪迭代中，将握手帧强制替换为前后缀的帧级平均，从而在生成过程中即保证重叠段的一致性。

**第二 Take：过渡精炼。** 第一 Take 产生的过渡段虽已对齐，但可能缺乏自然度。第二 Take 对握手区域重新加噪，并以相邻区间为条件进行去噪。关键设计是**软遮罩**：在硬遮罩 $\mathbf{M}_{hard}$（完全保护上下文帧）与软遮罩 $\mathbf{M}_{soft}$（允许适度修改）之间设置 $b$ 帧长的线性渐变区，使过渡帧在去噪过程中既能保留第一 Take 的结构，又能被上下文信息精炼。此外，引入**过渡嵌入**作为可学习的帧级标记，指示哪些帧属于过渡段，增强模型对过渡区域的感知。

### 3.3 ComMDM：两人交互协调

ComMDM 解决的是双人运动生成中的交互一致性问题。其设计理念极为轻量：冻结两个 MDM 模型，仅在 Transformer 的特定层间插入一个**单层通信块**。

该通信块接收两个 MDM 在第 $L_n$ 层 Transformer 的中间激活，输出一个修正项，分别加回两个模型的对应激活中。这一机制使两个原本独立生成的运动在特征层面相互校正，从而产生协调的交互行为。ComMDM 还可选地预测两人的初始姿态 $D$，以增强生成的一致性。消融实验表明，将通信块置于 Transformer 高层（第 8 层）且层数为 1 时性能最优——层数增加或置于低层反而损害效果，说明高层语义特征的交互协调更为关键。

### 3.4 DiffusionBlending：多控制信号组合

为实现精确的关节级与轨迹级控制，PriorMDM 采用“微调专用控制模型 + 采样时混合”的策略。

**微调阶段**：针对特定控制信号（如左腕位置、根轨迹）微调 MDM。训练时，对控制特征对应的运动分量注入噪声，迫使模型学习从噪声中恢复受控关节的运动，从而获得对该控制信号的强响应能力。

**采样阶段**：DiffusionBlending 将两个对齐的微调模型 $G^a$ 与 $G^b$ 在采样时线性混合：

$$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$$

其中 $c_a$、$c_b$ 为两个不同的控制条件（如左腕轨迹与根轨迹），$s$ 为混合权重。该方法本质上是将 classifier-free guidance 的思想泛化到任意两个对齐扩散模型之间，使得单一采样过程即可同时满足多个控制约束，而无需重新训练联合控制模型。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/003_Figure_3.jpg]]
*Figure 3: DoubleTake overview. We generate arbitrarily-long sequences with text control per interval using a fixed motion diffusion prior. At the first take, we generate each interval as a single sample handshaking neighboring samples. At each denoising iteration, the handshakes are forced to be equal to eventually compose one long sequence. To refine the transition between intervals, the second take partially noise the handshakes and clean them conditioned on the neighboring intervals using a soft mask. Solid frames mark generation or refinement; Dashed frames mark input motion to the take*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/004_Figure_4.jpg]]
*Figure 4: ComMDM overview. Using two fixed MDM models, we train a slim communication block (ComMDM) for two-person motion generation. ComMDM gets as input the activations of transformer layer*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/002_Figure_2.jpg]]
*Figure 2: Soft blending overview. We allow b frames long linear masking between*



## 实验与关键发现

### 核心实验设计逻辑

PriorMDM的实验体系围绕一个统一命题展开：**冻结的预训练运动扩散模型是否可以作为生成先验，通过推理时组合或轻量微调，在零样本/少样本条件下突破其原始训练分布的限制？** 为此，作者针对三种不同的运动生成瓶颈——长序列生成、多人交互、关节级精细控制——分别设计了DoubleTake、ComMDM和DiffusionBlending三种组合策略，并在BABEL、HumanML3D和3DPW三个标准基准上进行系统验证。所有实验均运行10次取平均，使用公开可用的基线模型，确保比较的公平性。

### 长序列生成：DoubleTake主结果与消融

**Table 1（BABEL测试集）** 展示了DoubleTake在长序列生成任务上的核心性能。在整体运动质量（FID）上，DoubleTake达到**1.04**，优于TEACH的1.12，更关键的是过渡质量指标：在70帧过渡窗口上，DoubleTake的Transition FID仅为**1.88**，而TEACH高达3.86，降幅达1.98。这一差距直接验证了DoubleTake双阶段推理中“软遮罩+过渡嵌入”机制的有效性——TEACH的序列拼接方法在过渡区域产生明显的不自然衔接，而DoubleTake的第二take通过重噪-去噪精炼过程，使过渡帧在保持与上下文一致性的同时获得更高的运动真实性。

**Table 2（HumanML3D测试集）** 进一步通过消融实验揭示了各组件的作用。完整DoubleTake配置（1秒handshake、软遮罩、过渡嵌入）取得FID **0.60**的最优结果。去除软遮罩后FID升至0.83，去除过渡嵌入后FID升至0.92，两者同时去除则退化至0.95。这一递进式退化表明：过渡嵌入提供了模型对“哪些帧属于过渡段”的结构性感知，而软遮罩则允许第二take在硬约束（完全保留原始生成）与软约束（完全重生成）之间进行线性渐变，从而在保持区间内部运动质量的同时精细修整过渡边界。定性结果**Fig. 5**直观展示了第二take对过渡帧的平滑效果。

### 多人交互：ComMDM主结果与通信层消融

**Table 3（3DPW前缀完成）** 报告了两人交互生成的核心指标。给定1秒前缀、预测3秒完成的设定下，ComMDM在3秒全局根节点误差（Root Error）上仅为**0.30m**，相比无通信模块的MDM（0.54m）降低44%，相比MRT（0.42m）亦有显著优势。逐秒分解来看，ComMDM的优势随时间窗口扩大而愈发明显（第3秒Joint Mean Error: ComMDM 0.38 vs MDM 0.62），说明通信模块有效防止了长时预测中的姿态漂移与交互语义丢失。

消融实验揭示了ComMDM通信层的两个关键设计选择：
- **层数**：单层transformer通信块性能最优，增加层数反而导致性能下降，说明过强的通信能力可能引入冗余信息或过拟合训练集中的特定交互模式。
- **层位置**：将通信块置于MDM transformer的第8层（共8层）时效果最佳，置于低层则性能显著退化。这表明高层激活编码了更抽象的语义特征，在此层级进行跨人物信息交换能更有效地协调两人的运动意图。

用户研究（**Fig. 8**）从感知层面提供了互补证据：在合理性、连贯性和交互质量三项评估中，ComMDM均显著优于MRT和MDM基线，且在与真实运动（Ground Truth）的对比中展现出竞争力。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/010_Figure_8.jpg]]
*Figure 8: 3DPW two-person prefix completion user study. We asked users to compare our ComMDM to the original MDM, MRT model, and ground truth in a side-by-side view. The dashed line marks 50%. ComMDM outperforms both MRT and MDM in all three aspects of generation*

### 关节/轨迹控制：DiffusionBlending主结果

**Table 4（HumanML3D测试集）** 对比了微调专用控制模型+DiffusionBlending与原始MDM inpainting在关节/轨迹控制任务上的表现。单一控制信号下，微调模型已展现出明显优势：轨迹控制的FID从MDM inpainting的0.98降至**0.54**，左腕控制的FID从1.04降至**0.67**。这表明微调策略（训练时遮蔽控制特征噪声）使模型学会尊重控制信号，而非像MDM inpainting那样在采样时强行覆盖部分帧，导致运动不自然。

当组合两种控制信号（左腕+轨迹）时，DiffusionBlending通过线性混合两个微调模型，取得FID **0.22**的显著最优结果，而MDM inpainting为1.18。这一差距揭示了DiffusionBlending的核心机制优势：在采样每一步通过公式$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$混合两个模型的去噪预测，实现了控制信号的“软融合”，避免了硬性约束导致的运动失真。定性结果**Fig. 9**显示，MDM inpainting在轨迹控制中产生大量脚部滑动，在手部控制中手部不自然地弯折到背后，而微调模型生成的挥杆动作语义正确且物理合理。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/012_Figure_9.jpg]]
*Figure 9: Fine-tuned Motion Control (unconditioned on text). We can see that MDM [Tevet et al. 2023] generates motions that completely ignore the input features: In trajectory control - MDM generates massive foot sliding, and in the hand control, the hand unrealistically bends behind the back. Our finetuned models generate natural motions that semantically and physically match the input features: In trajectory control - we generate a walking motion that fits the trajectory and in hand control, the model recognizes the swinging motion and generates a golf swing*

### 失败模式与局限性

尽管三种组合方法在各自任务上取得显著提升，实验和消融也揭示了若干结构性局限：
1. **长序列的长期一致性不足**：DoubleTake通过handshake机制保证了相邻区间的局部一致性，但当序列极长且区间语义差异大时，相距较远的区间之间可能出现运动风格漂移或语义不连贯。Table 2中即使最优配置的FID（0.60）仍高于真实分布，说明存在系统性差距。
2. **两人交互的物理接触缺失**：ComMDM通过高层特征通信协调两人运动，但未显式建模物理接触约束（如握手、拥抱时的接触力），因此生成的交互运动可能出现“接近但不接触”的伪交互现象。Table 3中第3秒的Joint Mean Error（0.38m）仍显著高于第1秒（0.14m），表明长时交互预测的精度衰减问题尚未完全解决。
3. **控制信号冲突时的退化**：DiffusionBlending假设两个控制信号可线性组合，但当信号存在物理冲突（如同时控制左手和右手执行相反方向的快速运动）时，线性插值可能产生不符合运动学约束的结果。Table 4未报告此类极端组合的测试，需人工验证。

### 证据强度总结

| 任务 | 核心指标 | PriorMDM | 最强基线 | 提升幅度 | 证据等级 |
|------|---------|----------|---------|---------|---------|
| 长序列生成 (BABEL) | FID ↓ | 1.04 | TEACH 1.12 | 7.1% | 强（Table 1） |
| 过渡质量 (BABEL, 70帧) | Transition FID ↓ | 1.88 | TEACH 3.86 | 51.3% | 强（Table 1） |
| 两人交互 (3DPW, 3秒) | Root Error ↓ | 0.30m | MDM 0.54m | 44.4% | 强（Table 3 + 用户研究） |
| 关节组合控制 (HumanML3D) | FID ↓ | 0.22 | MDM Inpaint 1.18 | 81.4% | 强（Table 4） |
| 消融：软遮罩作用 | FID ↑ | +0.23 | — | — | 中等（Table 2，单数据集） |
| 消融：通信层位置 | Root Error ↑ | 置于低层时退化 | — | — | 中等（Table 3，单任务） |

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/009_Table_2.jpg]]
*Table 2: Quantitative results on the HumanML3D [2022] test set. All methods use the real motion length from the ground truth. ‘→’ means results are better if the metric is closer to the real distribution. We run all the evaluations 10 times. Bold indicates best result, ?????????????????? indicates second best result. R-precision reported is top-3, Div. stands for diversity and M.-Dist for Multi-modal distance*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/011_Table_3.jpg]]
*Table 3: 3DPW prefix completion L2 error. Given a 1-second long prefix, all models predict a 3-second long motion completion. We report the root error and the joint’s mean error relative to the root for the first 1, 2, and 3 seconds. Bold indicates best result, underline indicates second best. We introduce two ablation studies, the first is for the number of layers constructing ComMDM (ours is 1), and the second is in which layer of MDM it is placed (ours is in the 8th). Observe that the communication block performs better when placed in higher layers of the transformer and constructed from fewer layers*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/013_Table_4.jpg]]
*Table 4: Joints control with fine-tuned models and DiffusionBlending. We compare our joints control method with the motion inpainting method suggested by Tevet et al. [2023]. We conduct the evaluation on HumanML3D [2022] test set. ′+′ sign represents a blending of two fine-tuned models with our DiffusionBlending method*

整体而言，PriorMDM在三个任务上的核心结论均有可靠的定量与定性证据支撑，消融实验清晰揭示了各组件的因果贡献。主要局限在于长期语义连贯性和物理交互真实性，这些方向仍需后续工作探索。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/005_Figure_5.jpg]]
*Figure 5: DoubleTake transition refinement. The second take refines the transitions generated in the first take to be more smooth and more realistic. Orange are subsequent transition frames and Blue are context intervals*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01418/figures/007_Figure_6.jpg]]
*Figure 6: Two-Person Prefix Completion. MRT [Wang et al. 2021] tends to fixate on the prefix pose whereas our ComMDM provides lively and semantically correct completions. Blue figures are the input prefix frames, provided to both models. The red and orange figures are MRT and our completions correspondingly*



## 定位与知识库关联

### 1. 问题瓶颈与核心思路

高质量人体运动数据的捕捉与标注成本极高，导致现有生成模型普遍受限于单人、短序列（通常≤10秒）场景。面对多人交互、超长序列生成、关节级精细控制等复杂下游任务，传统的“收集更多数据、训练更大模型”路径在经济上不可行。PriorMDM的核心洞察在于：预训练的运动扩散模型（MDM）已经编码了丰富的动态先验，瓶颈并非数据规模，而是如何经济地“组合利用”已有先验。为此，该工作提出三条互补的推理时与少样本组合策略，将固定的MDM作为生成先验，在不改变或仅微调前置模型的前提下，突破训练分布的限制。

### 2. 方法谱系与基线对比

PriorMDM的三条技术路线分别针对长序列生成、多人交互和精细控制，各自对标领域内代表性基线。

**长序列生成：DoubleTake vs. TEACH**

- **TEACH** (Athanasiou et al., 3DV 2022) 采用顺序组合策略生成超长运动，但缺乏显式的过渡精炼机制，导致片段衔接处常出现滑步或语义断裂。
- **DoubleTake** 提出双阶段并行推理：第一take批量生成各文本区间并维护handshake约束（通过相邻片段后缀与前缀的线性加权强制重叠段一致）；第二take对过渡区域施加可控重噪，并用软遮罩（soft blending mask）在硬约束与自由生成之间线性渐变，辅以可学习的过渡嵌入（Transition Embedding）指示帧是否属于过渡段。这一设计将过渡FID从TEACH的3.86降至1.88（BABEL，70帧），整体FID从1.12降至1.04。消融实验证实，去除软遮罩或过渡嵌入会使HumanML3D上的FID从0.60分别升至0.83和0.92，表明两者对过渡质量至关重要。

**多人交互：ComMDM vs. MRT与独立MDM**

- **MRT** (Wang et al., NeurIPS 2021) 是多人运动预测的基线方法，但在前缀完成任务中倾向于“固化”前缀姿态，缺乏语义合理的交互完成。
- **独立MDM** 为两人分别生成运动，完全忽略交互协调。
- **ComMDM** 在两个冻结MDM的Transformer高层（第8层）之间插入单层通信块，通过校正中间激活来协调两人运动，并可选择预测初始姿态。在3DPW两人前缀完成任务上，ComMDM的根节点误差为0.30 m，显著优于独立MDM的0.54 m；用户研究中，ComMDM在合理性、连贯性和交互质量三项评估上均优于MRT和MDM。消融显示，通信层置于Transformer高层且层数为1时性能最佳——增加层数或置于低层反而降低效果，说明轻量高层语义协调比深层特征融合更有效。

**关节/轨迹控制：微调+DiffusionBlending vs. MDM Inpainting**

- **MDM Inpainting** (Tevet et al., ICLR 2023) 在采样时直接将给定控制信号填入运动序列，但对复杂控制（如同时约束左手腕和全身轨迹）表现不佳，常产生忽略控制信号或物理不合理的运动（如严重滑步、手部异常弯折）。
- PriorMDM的方案分两步：首先针对特定控制信号微调专用MDM（训练时遮蔽控制特征对应的噪声），然后通过**DiffusionBlending**在采样时线性混合多个微调模型：$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$。这一机制将分类器自由引导推广到任意两个对齐扩散模型的混合。在HumanML3D上，单独轨迹控制的FID从MDM Inpainting的0.98降至微调模型的0.54；左腕+轨迹组合控制中，DiffusionBlending的FID仅为0.22，而MDM Inpainting高达1.18，差距近一个数量级。

### 3. 适用边界与局限

尽管三种组合方法在各自任务上表现突出，其适用边界和潜在失效模式值得关注：

1. **长序列的长期语义连贯性**：DoubleTake通过局部handshake和过渡精炼保证了相邻区间的平滑衔接，但相距较远的区间之间缺乏显式的全局一致性约束。当文本序列包含跨越多个区间的宏观语义（如“先走向桌子，绕一圈，再坐下”）时，后期运动可能与前期的空间位置或朝向不匹配。该问题在论文中被列为已知局限，需人工验证实际退化程度。

2. **两人交互的物理真实性与泛化**：ComMDM仅用少量样本学习通信块，虽能产生语义合理的交互，但无法保证真实的物理接触（如握手时手部精确重合）。对新交互类型的泛化受限于通信块的训练数据分布——论文明确指出，当前方法未能建模人物间的物理约束，这是一个开放挑战。

3. **跨领域迁移未验证**：三种组合策略均在人体运动域验证，其在图像、音频等其他扩散模型生成领域的适用性尚待探索。DiffusionBlending的对齐假设（两个模型共享相同架构与噪声调度）在跨领域场景中可能不成立。

4. **计算开销累积**：多次推理组合（如DoubleTake的双take、DiffusionBlending的多模型混合）会线性增加采样步数，对实时交互应用构成压力。论文未提供推理延迟数据，该点需在部署时评估。

### 4. 开放问题

- **自适应混合权重**：DiffusionBlending目前使用固定标量$s$控制模型混合比例，是否可以设计学习机制，根据上下文或控制信号的重要性动态调整$s$，以更智能地融合多控制信号？
- **多模态先验融合**：当前仅利用文本作为条件，是否可引入图像、语音等模态的先验，进一步增强控制精度与数据效率？
- **物理仿真耦合**：在两人交互生成中，是否可将轻量物理仿真作为后处理或训练约束，以弥补ComMDM对物理接触建模的不足？
- **推理效率优化**：是否存在蒸馏或一步采样策略，将多次组合推理的计算开销压缩至接近单次生成的水平？



## 原文 PDF

![[paperPDFs/ICLR_2024/PriorMDM:_Human_Motion_Diffusion_as_a_Generative_Prior.pdf]]

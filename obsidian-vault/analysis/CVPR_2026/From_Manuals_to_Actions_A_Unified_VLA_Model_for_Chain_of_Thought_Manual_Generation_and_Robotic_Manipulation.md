---
title: "From Manuals to Actions: A Unified VLA Model for Chain-of-Thought Manual Generation and Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain_of_Thought_Manual_Generation_and_Robotic_Manipulation.pdf
project_link: "https://sites.google.com/view/maunalvla"
code_link: null
aliases:
- FMAUVMCTMGRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入规划专家（Planning Expert）生成多模态手册（文本、坐标、子目标图像），并通过Manual Chain-of-Thought（ManualCoT）将手册作为显式视觉提示与隐式潜在特征同时注入动作专家，实现从“结果”到“过程”的推理与执行协同。
primary_logic: 模仿人类从最终目标反推中间步骤的能力，采用Mixture-of-Transformers架构分离规划与动作专家，并通过ManualCoT将手册信息同时以显式（位置掩码）和隐式（交叉注意力特征）的方式传递给动作专家，使长程任务分解为可精确执行的条件化子目标序列。
claims:
- "ManualVLA在三个长程任务的最终成功率上相比最强分层基线提升15%-30%（2D LEGO: 0.85 vs 0.60; 3D LEGO: 0.65 vs 0.35; Object Rearrangement: 0.65 vs 0.50）"
- ManualVLA生成的子目标图像和位置坐标具有高PSNR（29.01/28.68/28.11）和低MAE（3.23/3.58/6.21像素），证明规划专家能可靠地还原中间状态
- 消融实验显示，同时使用显式与隐式ManualCoT以及MoT架构是取得高性能的关键（见Figure 6 b/c）
- 面对背景、物体形状和光照变化时，ManualVLA仍保持一定泛化能力，但形状变化导致成功率从0.85下降至0.60（-29%）
---

# From Manuals to Actions: A Unified VLA Model for Chain-of-Thought Manual Generation and Robotic Manipulation

> [!tip] 核心洞察
> 模仿人类从最终目标反推中间步骤的能力，采用Mixture-of-Transformers架构分离规划与动作专家，并通过ManualCoT将手册信息同时以显式（位置掩码）和隐式（交叉注意力特征）的方式传递给动作专家，使长程任务分解为可精确执行的条件化子目标序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从手册到行动：面向思维链手册生成与机器人操作的统一VLA模型 |
| 英文题名 | From Manuals to Actions: A Unified VLA Model for Chain-of-Thought Manual Generation and Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gu_From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain-of-Thought_CVPR_2026_paper.html) · [Project](https://sites.google.com/view/maunalvla) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ManualVLA |
| Dataset | 2D LEGO Assembly, 3D LEGO Assembly, Object Rearrangement |

> [!tip] 效果简介
> - 2D LEGO Assembly 上，Success Rate (complete task) 0.85 vs 0.60 (VLM+π0.5) (+0.25 (+41.7%))。
> - 3D LEGO Assembly 上，Success Rate (complete task) 0.65 vs 0.35 (VLM+π0.5) (+0.30 (+85.7%))。
> - Object Rearrangement 上，Success Rate (complete task) 0.65 vs 0.50 (VLM+π0.5) (+0.15 (+30.0%))。

## 概述

现有视觉-语言-动作（VLA）模型在长程操作任务中面临一个根本瓶颈：它们擅长将感知直接映射为动作，却缺乏推断中间过程的能力。当任务需要将预定义的目标状态（如“将乐高拼成特定形状”或“将物体按指定布局摆放”）分解为可执行的子目标与精确操作步骤时，端到端模型往往无法可靠地完成推理，导致成功率骤降。

ManualVLA 针对这一问题提出了一个关键思路——模仿人类从最终目标反推中间步骤的能力。其核心机制是引入一个**规划专家（Planning Expert）**，在给定当前观测与最终目标图像后，生成一份多模态“手册”（Manual），包含子目标图像、目标物体的二维坐标以及文本描述。这份手册随后通过**Manual Chain-of-Thought（ManualCoT）**机制同时以显式（位置掩码作为视觉提示）和隐式（交叉注意力中的潜在特征）两种方式注入动作专家，使长程任务被分解为一系列有条件引导的精确子目标执行。

架构上，ManualVLA 基于 **Mixture-of-Transformers（MoT）** 设计，将规划专家与动作专家分离为独立的 Transformer 模块，并通过跨任务共享注意力实现两者的协同。这一设计使得模型能够在统一的框架内完成“手册生成”与“动作执行”两个阶段，而非简单地将它们串联。

在三个具有代表性的长程任务——2D 乐高装配、3D 乐高装配和物体重排——上，ManualVLA 的最终成功率分别达到 **0.85、0.65 和 0.65**，相比最强分层基线（VLM + π0.5）分别提升了 **25%、30% 和 15%**。消融实验进一步确认，手册信息的丰富程度、显式与隐式思维链的联合使用、以及 MoT 架构的分离设计，是取得高性能的关键因素。此外，模型仅需约 100 条下游任务演示即可实现泛化操控，展现了较强的数据效率。

## 背景与动机

### 长程操作任务的瓶颈：从“结果”到“过程”的缺失

在机器人操作领域，LEGO装配、物体重排等长程任务要求机器人不仅理解最终目标状态，还需推断并执行一系列精确的中间步骤。然而，现有视觉-语言-动作（VLA）模型普遍采用端到端映射范式——直接从当前观测映射到动作序列，缺乏对中间过程的显式推理能力。这一结构性缺陷在需要精确空间定位和子目标拆解的任务中尤为致命：模型无法将预定义的最终目标状态转化为可执行的子目标与精确操作步骤，导致长程任务成功率骤降。

### 现有VLA方法的局限性

当前主流VLA方法可归为两类。第一类为端到端VLA模型，如 **π0**（Black et al., arXiv 2024）及其高效变体 **π0.5**，以及 **FAST**（Pertsch et al., arXiv 2025），它们直接将感知映射到动作，缺乏中间推理环节。第二类为分层方法，如 **VLM + π0.5**，先由视觉语言模型生成高层提示，再由动作模型执行。尽管分层方法引入了规划与执行的分离，但规划与动作模型之间缺乏紧密耦合——规划器生成的文本或图像提示仅作为显式输入，无法通过共享特征空间实现深层引导。**CoT-VLA**（Zhao et al., CVPR 2025）虽引入了视觉思维链，但其推理与动作仍共享统一Transformer，未针对规划与执行的不同需求进行架构级分离。

### 核心洞察：模仿人类的“反推”能力

人类的操作能力源于一种关键的认知机制：从最终目标反推中间步骤。面对“将红色积木放在蓝色积木右侧”的指令，人类会先在脑海中生成子目标图像、定位目标位置、规划移动路径，然后才执行动作。这一“想象-执行”的协同过程正是现有VLA模型所缺失的。本文的核心洞察在于：**将规划与执行解耦为两个专家模块，并通过多模态手册作为桥梁实现二者的协同**——规划专家负责“想象”中间状态（生成子目标图像、目标坐标和文本描述），动作专家则在这些手册信息的显式与隐式双重引导下执行精确操作。

## 核心创新

ManualVLA 的核心创新在于将长程机器人操作任务从“端到端感知-动作映射”重构为“先规划后执行”的两阶段生成范式，并通过三项紧密耦合的机制设计实现这一转变。

### 1. 推理范式转变：从直接映射到 Manual Chain-of-Thought

现有 VLA 模型（如 **π0** (Black et al., arXiv 2024)、**FAST** (Pertsch et al., arXiv 2025)）采用端到端映射，直接从观测预测动作，缺乏对中间过程的显式推理能力。当面对预定义目标状态的长程任务时，模型必须隐式推断所有中间步骤，导致成功率骤降。

ManualVLA 引入 **Manual Chain-of-Thought (ManualCoT)** 范式，模仿人类从最终目标反推中间步骤的能力。具体而言，模型首先生成多模态手册（包含子目标图像、目标 2D 坐标和文本描述），再以该手册为条件生成精确动作。这一转变将复杂的长程任务分解为可精确执行的条件化子目标序列——从“预测结果”变为“生成过程”。

形式化地，ManualVLA 将策略分解为两步：

- **手册生成**：$\pi_{\theta}(\mathcal{T}_t^{\mathrm{subgoal}}, p_t, \hat{l}_t \mid \mathcal{T}^{\mathrm{goal}}, \mathcal{T}_t^{\mathrm{current}}, l)$
- **动作生成**：$\pi_{\theta}(a_{t:t+h} \mid s_t, \mathcal{T}_t^{\mathrm{prompt}}, \mathcal{F}_t^{\mathrm{subgoal}}, \mathcal{F}_t^{p}, \mathcal{F}_t^{\hat{l}})$

### 2. 架构创新：Mixture-of-Transformers 分离规划与行动

为支持上述两阶段范式，ManualVLA 将标准 Transformer VLA 扩展为 **Mixture-of-Transformers (MoT)** 架构，包含独立的**规划专家 (Planning Expert)** 与**动作专家 (Action Expert)**。每个 token 根据其任务类别使用不同的 FFN 和注意力参数：

$$\mathrm{MoT}_{\Theta}(x) = x + \mathcal{N}_{\mathrm{ffn}}^{t(\cdot)}\Big(\Phi_{\mathrm{ffn}}^{t(\cdot)}\big(x + \mathcal{N}_{\mathrm{attn}}^{t(\cdot)}(\Phi_{\mathrm{attn}}(x))\big)\Big)$$

这一设计的关键优势在于：规划专家专注于语义理解与子目标生成，动作专家专注于精确操控，二者通过共享注意力机制协同而非相互干扰。消融实验（Figure 6c）证实，分离的 MoT 架构显著优于共享参数的统一 Transformer。

### 3. 条件输入创新：显式与隐式 ManualCoT 双重引导

ManualVLA 将生成的手册信息通过两条路径同时注入动作专家：

- **显式路径**：利用预测的 (U, V) 坐标在场景图像上叠加目标位置掩码，形成视觉提示 $\mathcal{T}_t^{\mathrm{prompt}}$，使动作专家“看到”目标位置。
- **隐式路径**：通过跨任务共享注意力机制，使动作专家能够关注规划专家生成的手册 token 中的潜在特征 $\mathcal{F}_t^{\mathrm{subgoal}}, \mathcal{F}_t^{p}, \mathcal{F}_t^{\hat{l}}$，实现深层语义引导。

消融实验（Figure 6b）表明，同时使用显式与隐式 ManualCoT 对成功率至关重要，缺少任一路径均导致性能显著下降。

### 4. 数据生成创新：基于 3DGS 的数字孪生自动合成

传统 VLA 依赖人工遥操作采集示范数据，成本高昂且难以覆盖多样化的中间状态。ManualVLA 开发了基于 3D Gaussian Splatting 的数字孪生工具，自动生成包含子目标图像、坐标和文本的手册训练数据，仅需约 100 条下游任务演示即可实现泛化操控。

**与最接近基线 CoT-VLA 的区别**：**CoT-VLA** (Zhao et al., CVPR 2025) 虽也预测子目标图像，但其采用统一的 Transformer 架构，缺乏规划-行动分离和显式位置提示机制，在长程任务上成功率显著低于 ManualVLA（Table 2）。

## 整体框架

ManualVLA 的整体 pipeline 围绕一个核心洞察构建：**长程操作任务的成功不仅需要最终目标状态的感知，更需要将目标分解为可精确执行的中间步骤**。为此，ManualVLA 采用 Mixture-of-Transformers（MoT）架构，将系统划分为两个协同工作的专家——规划专家（Planning Expert）与动作专家（Action Expert）——并通过 Manual Chain-of-Thought（ManualCoT）机制在两者之间建立显式与隐式的双重信息通道。

### 输入输出流

系统的输入由三部分组成：**语言指令** $l$（如“将红色积木放在蓝色积木右侧”）、**当前观测图像** $\mathcal{T}_t^{\mathrm{current}}$ 以及**最终目标状态图像** $\mathcal{T}^{\mathrm{goal}}$。整个 pipeline 分两个阶段运行：

**阶段一：多模态手册生成。** 规划专家接收上述三个输入，生成一份多模态手册，包含三个互补的信息维度：
- **文本描述** $\hat{l}_t$：对当前子任务的语义描述，提供高层推理线索；
- **目标 2D 坐标** $p_t$：待操作物体的精确像素位置，用于构造显式视觉提示；
- **子目标图像** $\mathcal{T}_t^{\mathrm{subgoal}}$：预测的中间状态渲染图，提供语义丰富的条件信息。

这一过程可形式化为条件分布：
$$\pi_{\theta}(\mathcal{T}_t^{\mathrm{subgoal}}, p_t, \hat{l}_t \mid \mathcal{T}^{\mathrm{goal}}, \mathcal{T}_t^{\mathrm{current}}, l)$$

**阶段二：条件化动作生成。** 动作专家接收机器人本体状态 $s_t$，并同时获得来自手册的三条信息通道：
- **显式 ManualCoT**：利用预测的坐标 $p_t$ 在当前观测图像上叠加目标位置掩码，构造提示图像 $\mathcal{T}_t^{\mathrm{prompt}}$；
- **隐式 ManualCoT**：通过跨任务共享注意力机制，使动作专家直接关注规划专家在生成手册过程中产生的潜在特征 $\mathcal{F}_t^{\mathrm{subgoal}}$、$\mathcal{F}_t^{p}$、$\mathcal{F}_t^{\hat{l}}$。

动作专家最终输出一个动作块 $a_{t:t+h}$，其条件分布为：
$$\pi_{\theta}(a_{t:t+h} \mid s_t, \mathcal{T}_t^{\mathrm{prompt}}, \mathcal{F}_t^{\mathrm{subgoal}}, \mathcal{F}_t^{p}, \mathcal{F}_t^{\hat{l}})$$

### 模块关系与架构设计

Figure 2 完整展示了 ManualVLA 的框架结构，其核心模块关系如下：

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/002_Figure_2.jpg]]
*Figure 2: Framework of ManualVLA. (a) To accomplish long-horizon tasks with defined goal states, we propose ManualVLA, a unified VLA model built upon a MoT architecture. The framework consists of two experts: a planning expert responsible for generating multimodal manuals, and an action expert responsible for predicting precise actions. The planning expert processes human instructions, the current image, and the final goal image to generate intermediate manuals that combine next-step images, positions, and sub-task instructions. We introduce an explicit CoT reasoning process, where each positional indicator serves as a visual prompt embedded into the observation of the action expert. (b) Along with t...*

**视觉编码双通道。** 系统维护两条并行的视觉处理路径：VQ-GAN Vision Tokenizer 将图像转化为离散 token，服务于规划专家的子目标图像生成；SigLIP-Large Vision Encoder 提取连续视觉特征，为动作专家提供感知输入。这种双通道设计使得规划和执行可以各自获得最适合其特征空间的视觉表示。

**MoT 层实现参数级任务分离。** ManualVLA 以 Janus-Pro 作为基础 VLM 模型，并将其扩展为 MoT 架构。在每一层 MoT 中，每个 token 根据其所属任务类别（规划或动作）使用不同的 FFN 和注意力投影参数：
$$\mathrm{MoT}_{\Theta}(x) = x + \mathcal{N}_{\mathrm{ffn}}^{t(\cdot)}\Big(\Phi_{\mathrm{ffn}}^{t(\cdot)}\big(x + \mathcal{N}_{\mathrm{attn}}^{t(\cdot)}(\Phi_{\mathrm{attn}}(x))\big)\Big)$$
其中 $t(\cdot)$ 为 token 级任务路由函数，决定使用哪组参数。注意力计算同样按任务类别选取投影矩阵：
$$Q = X W_Q^{t(\cdot)}, \; K = X W_K^{t(\cdot)}, \; V = X W_V^{t(\cdot)}$$

**跨任务共享注意力实现隐式 ManualCoT。** 虽然 FFN 和注意力投影按任务分离，但注意力计算本身是全局的——动作专家的 token 可以直接关注规划专家生成的手册 token。这一机制构成了隐式 ManualCoT 的核心：手册生成过程中积累的潜在特征（子目标图像 token、坐标编码、文本嵌入）作为条件信号，通过交叉注意力持续引导动作专家的每一步预测。

**扩散动作头。** 动作专家采用扩散策略（Diffusion Policy）范式生成动作块，而非自回归生成。噪声编码器将动作块加噪，动作专家预测噪声 $\hat{\epsilon}^i$，损失函数为预测噪声与真实噪声的均方误差：
$$\mathcal{L}_{\mathrm{action}} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,1), i} \| \hat{\epsilon}^i - \epsilon \|_2^2$$
消融实验（Figure 6d）证实，扩散生成在该任务中优于自回归范式。

**联合训练目标。** 最终损失为手册生成交叉熵损失与动作预测 MSE 损失之和：
$$\mathcal{L}_{\mathrm{final}} = \mathcal{L}_{\mathrm{manual}} + \mathcal{L}_{\mathrm{action}}$$

### 数据流与训练策略

训练数据通过基于 3D Gaussian Splatting 的数字孪生工具自动合成（Figure 3）。该工具重建场景的 3DGS 表示，将其分解为操作台面和独立物体，然后通过迭代放置物体自动生成中间目标状态的图像、坐标和文本描述。规划专家在超过 10K 帧/任务的手册数据上预训练，动作专家在超过 400K 轨迹样本上预训练。下游任务仅需约 100 条遥操作示范即可实现泛化操控。

三阶段训练策略（Figure 2c）依次对齐规划与动作专家：第一阶段独立预训练各专家，第二阶段联合训练建立跨任务注意力连接，第三阶段在下游任务数据上微调。

### 补充图表

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/001_Figure_1.jpg]]
*Figure 1: Overview. (a) Long-horizon tasks with predefined goal states, such as LEGO assembly or object rearrangement, pose a significant challenge for intelligent robots, as they require not only imagining procedural manuals but also executing precise manipulations based on them. (b) We address such tasks by introducing ManualVLA, a unified VLA model built upon a MoT architecture, which enables coherent collaboration between multimodal manual and action generation via a designed Manual Chain-of-Thought*

## 核心模块与公式推导

### 问题形式化与两阶段生成

ManualVLA将长程操作任务形式化为两阶段生成问题。给定语言指令 $l$、当前状态图像 $\mathcal{T}_t^{\mathrm{current}}$ 和目标状态图像 $\mathcal{T}^{\mathrm{goal}}$，系统首先生成多模态手册，再基于手册条件生成动作序列。

**阶段一：手册生成。** 规划专家建模如下分布（Eq. 1）：

$$\pi_{\theta}(\mathcal{T}_t^{\mathrm{subgoal}}, p_t, \hat{l}_t \mid \mathcal{T}^{\mathrm{goal}}, \mathcal{T}_t^{\mathrm{current}}, l)$$

其中 $\mathcal{T}_t^{\mathrm{subgoal}}$ 为子目标图像，$p_t$ 为目标物体的2D坐标 $(U, V)$，$\hat{l}_t$ 为子任务文本描述。手册的三种模态分别提供语义推理线索（文本）、丰富视觉条件（子目标图像）和精确操作引导（位置坐标）。

**阶段二：动作生成。** 动作专家建模如下分布（Eq. 2）：

$$\pi_{\theta}(a_{t:t+h} \mid s_t, \mathcal{T}_t^{\mathrm{prompt}}, \mathcal{F}_t^{\mathrm{subgoal}}, \mathcal{F}_t^{p}, \mathcal{F}_t^{\hat{l}})$$

其中 $s_t$ 为机器人本体状态，$\mathcal{T}_t^{\mathrm{prompt}}$ 为叠加了位置掩码的提示图像（显式思维链），$\mathcal{F}_t^{\mathrm{subgoal}}$、$\mathcal{F}_t^{p}$、$\mathcal{F}_t^{\hat{l}}$ 分别为手册生成过程中存储的子目标图像、位置和文本对应的潜在特征（隐式思维链）。动作块 $a_{t:t+h}$ 通过扩散策略生成，预测未来 $h$ 步动作。

### Mixture-of-Transformers 架构

ManualVLA以 **Janus-Pro** 为基础模型，将其扩展为Mixture-of-Transformers（MoT）架构，形成统一的VLA模型。MoT的核心思想是：不同任务类别的token使用不同的前馈网络（FFN）和注意力投影参数，实现规划专家与动作专家的参数化分离。

**MoT层定义（Eq. 3）：**

$$\mathrm{MoT}_{\Theta}(x) = x + \mathcal{N}_{\mathrm{ffn}}^{t(\cdot)}\Big(\Phi_{\mathrm{ffn}}^{t(\cdot)}\big(x + \mathcal{N}_{\mathrm{attn}}^{t(\cdot)}(\Phi_{\mathrm{attn}}(x))\big)\Big)$$

其中 $t(\cdot)$ 为token的任务类别映射函数，$\mathcal{N}_{\mathrm{attn}}$ 和 $\mathcal{N}_{\mathrm{ffn}}$ 分别为注意力层和FFN层的归一化，$\Phi_{\mathrm{attn}}$ 和 $\Phi_{\mathrm{ffn}}$ 为对应的变换函数。每个token根据其任务标签选择不同的参数子集，使得规划token和动作token在同一序列中协同处理，但使用各自专用的计算路径。

**全局注意力计算（Eq. 4）：**

$$Q = X W_Q^{t(\cdot)}, \quad K = X W_K^{t(\cdot)}, \quad V = X W_V^{t(\cdot)}$$

$$A = \mathrm{softmax}\big(\frac{QK^\top}{\sqrt{d_k}}\big), \quad \Phi_{\mathrm{attn}}(x) = (AV) W_O^{t(\cdot)}$$

注意力机制为全局注意力，但查询、键、值和输出的投影矩阵 $W_Q$、$W_K$、$W_V$、$W_O$ 均按token任务类别选取。这使动作专家能够通过注意力机制关注规划专家生成的手册token，实现隐式思维链引导。

### ManualCoT：显式与隐式思维链

ManualCoT是连接规划与动作专家的核心机制，包含两条并行的信息通路：

- **显式思维链**：利用预测的 $(U, V)$ 坐标在当前观测图像上叠加目标位置掩码，构造 $\mathcal{T}_t^{\mathrm{prompt}}$ 作为动作专家的视觉输入。这使得动作专家在像素空间中获得精确的位置引导。

- **隐式思维链**：通过跨任务共享注意力机制，动作专家直接关注规划专家生成的手册token（子目标图像token、位置token、文本token），获取 $\mathcal{F}_t^{\mathrm{subgoal}}$、$\mathcal{F}_t^{p}$、$\mathcal{F}_t^{\hat{l}}$ 作为条件特征。消融实验（Figure 6b）表明，同时使用显式与隐式ManualCoT对成功率至关重要。

### 训练目标

**手册生成损失** $\mathcal{L}_{\mathrm{manual}}$：对子目标图像token和文本token使用标准交叉熵损失，对 $(U, V)$ 坐标使用均方误差损失。

**动作生成损失** $\mathcal{L}_{\mathrm{action}}$（扩散策略）：

$$\mathcal{L}_{\mathrm{action}} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,1), i} \| \hat{\epsilon}^i - \epsilon \|_2^2$$

其中 $\epsilon$ 为真实噪声，$\hat{\epsilon}^i$ 为扩散去噪网络在第 $i$ 步的预测噪声。动作专家采用扩散策略而非自回归生成，消融实验（Figure 6d）验证了该选择在长程操作任务中的优势。

**联合训练损失：**

$$\mathcal{L}_{\mathrm{final}} = \mathcal{L}_{\mathrm{manual}} + \mathcal{L}_{\mathrm{action}}$$

训练采用三阶段策略：首先在大规模动作数据集（超400K轨迹样本）上预训练动作专家，然后在数字孪生合成数据（每任务超10K帧）上预训练规划专家，最后在下游任务的约100条遥操作示范上联合微调两个专家。

### 补充图表

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/003_Figure_3.jpg]]
*Figure 3: Digital-twin example. (a) We reconstruct 3D Gaussian Splatting representations, which are then decomposed into the LEGO board and individual bricks. (b) We iteratively place the bricks on the board or objects on the box*

## 实验与分析

### 手册生成质量评估

ManualVLA 的规划专家需要在视觉和空间层面精确还原中间状态。表 1 报告了三个长程任务上子目标图像生成与坐标预测的定量结果。手册生成质量整体稳定：PSNR 保持在 28.11–29.01 dB，MAE 低至 3.23–6.21 像素。其中 2D LEGO 任务表现最优（PSNR 29.01, MAE 3.23），而 Object Rearrangement 因场景复杂度更高导致 MAE 略有上升（6.21 像素），但 FID 反而最低（24.46），说明生成图像在语义分布上仍与真实子目标高度一致。这些结果表明规划专家能够可靠地从目标状态反推中间步骤的视觉与空间信息，为后续动作执行提供高质量条件信号。

### 长程操作成功率对比

表 2 报告了 ManualVLA 与各基线在 20 个未见测试目标状态下的完整任务成功率及关键中间步骤成功率。核心发现如下：

- **端到端 VLA 基线（π0, π0.5, FAST）在长程任务上几乎完全失败**，最终成功率为 0.00–0.05。这些模型缺乏显式的中间状态推理能力，无法将远距离目标分解为可执行的子任务序列。
- **CoT-VLA** 虽引入了视觉思维链，但仅将子目标图像作为隐式条件，最终成功率同样极低（2D LEGO 0.10, 3D LEGO 0.00），表明单纯预测未来帧不足以指导精确操作。
- **分层基线 VLM + π0.5** 表现最强（2D LEGO 0.60, 3D LEGO 0.35, Object Rearrangement 0.50），但其规划与执行完全分离，规划错误无法在执行阶段纠正。
- **ManualVLA 在所有任务上显著超越最强分层基线**：2D LEGO 提升 25 个百分点（0.85 vs 0.60），3D LEGO 提升 30 个百分点（0.65 vs 0.35），Object Rearrangement 提升 15 个百分点（0.65 vs 0.50）。关键中间步骤的成功率也呈现一致优势，验证了 ManualCoT 机制在子目标级别的引导有效性。

这一差距的本质在于：ManualVLA 通过 MoT 架构实现了规划与执行的协同优化——规划专家生成的手册不仅提供显式位置掩码作为视觉提示，还通过跨任务共享注意力将手册生成过程中的隐式特征注入动作专家，使动作预测能够感知规划的中间表征。

### 消融实验

Figure 6 系统拆解了 ManualVLA 各设计要素的贡献：

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/008_Figure_6.jpg]]
*Figure 6: Ablation study. We investigate the impact of (a) the information contained in the generated manuals, (b) explicit and implicit CoT reasoning, (c) the MoT architecture design, and (d) the action generation paradigm on long-horizon manipulation success rates*

**(a) 手册信息丰富度**：逐步增加手册中的信息维度（仅文本 → 文本+坐标 → 文本+坐标+子目标图像），操作成功率单调递增。完整的三种模态组合带来最高成功率，证明多模态手册之间存在互补增益——文本提供语义锚定，坐标提供空间精度，子目标图像提供视觉上下文。

**(b) 显式与隐式 ManualCoT**：单独使用显式 CoT（位置掩码）或隐式 CoT（跨任务注意力特征）均能提升成功率，但两者联合使用时性能最优。这表明显式提示与隐式特征条件化分别作用于动作专家的不同处理阶段，形成互补引导。

**(c) MoT 架构**：将规划与动作专家分离的 MoT 设计显著优于共享参数的统一 Transformer。分离架构允许两个专家各自专注于不同粒度的任务（规划侧重全局语义推理，动作侧重局部精确控制），同时通过跨任务注意力保持信息流动。

**(d) 动作生成范式**：扩散策略优于自回归生成范式。扩散模型在连续动作空间中的多模态分布建模能力更适合精确操作任务，而自回归方法在长序列动作预测中累积误差更为严重。

### 泛化性能与失效模式

表 3 报告了 ManualVLA 在背景、物体形状和光照三种分布外变化下的泛化表现。三类扰动均导致成功率下降，但影响程度差异显著：

- **形状变化**对性能冲击最大，2D LEGO 成功率从 0.85 降至 0.60（-29%），3D LEGO 从 0.65 降至 0.40（-38%）。这说明数字孪生合成的训练数据难以覆盖真实世界中物体几何的多样性，规划专家生成的子目标坐标在未见形状上出现偏差，进而导致动作执行失败。
- **背景变化**影响次之（-21% 至 -23%），表明模型对视觉域迁移具有一定鲁棒性，但场景纹理的剧烈变化仍会干扰规划与动作专家的特征提取。
- **光照变化**影响最小（-15% 至 -17%），得益于训练数据合成时的光照随机化策略。

这些结果揭示了 ManualVLA 的核心瓶颈：**数字孪生数据的覆盖度直接决定了泛化边界**。当真实环境中的物体形状与合成数据分布偏离较大时，手册生成的空间精度下降，ManualCoT 的引导信号随之劣化。此外，论文仅需约 100 条下游任务演示即可实现泛化操控，但尚不能完全摆脱对真实动作数据的依赖，在极端分布外场景下仍需额外微调。

### 补充图表

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of ManualVLA in generating subgoal images and (U, V ) coordinates across the three downstream tasks*

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/005_Table_2.jpg]]
*Table 2: Comparison of ManualVLA and baselines. We report the manipulation success rate (S.R.) for the complete long-horizon tasks using 20 unseen test goal states, and additionally report the success rate of key intermediate steps*

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/009_Table_3.jpg]]
*Table 3: Generalization. We report the mean success rate and performance degradation ratio for each task over 20 rollouts under variations in background, object shape, and lighting*

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/006_Figure_4.jpg]]
*Figure 4: For each task, we visualize three components: (1) manual ground truth (GT), (2) manual predictions (Pred.) generated by ManualVLA, and (3) the final goal image*

![[assets/figures/papers/paper_list_l2168_https_openaccess_thecvf_com_content_CVPR2026_html_Gu_From_Manuals_to_Act/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of real-world experiments on Franka Research 3 dual-arm robots, executed from left to right*

## 方法谱系与知识库定位

### 与现有VLA方法的谱系关系

ManualVLA 的核心突破在于将“规划”与“执行”从耦合的端到端映射中解耦，形成两阶段推理范式。在现有VLA谱系中，**π0**（Black et al., arXiv 2024）和 **π0.5** 代表标准端到端VLA，直接将感知映射为动作，缺乏对中间过程的显式建模；**FAST**（Pertsch et al., arXiv 2025）通过高效动作分词提升了VLA效率，但推理范式仍为一步映射；**CoT-VLA**（Zhao et al., CVPR 2025）引入了视觉思维链，通过预测子目标图像辅助决策，但其规划与动作仍共享统一模型参数，未能实现专家级分离。ManualVLA 在 CoT-VLA 的基础上向前推进一步：不仅预测子目标图像，还生成文本描述与精确2D坐标，构成完整的“多模态手册”；更重要的是，通过 Mixture-of-Transformers（MoT）架构将规划专家与动作专家分离，使两者各司其职——规划专家专注于理解目标状态并生成可执行的中间步骤，动作专家则专注于将手册信息转化为精确动作。

与分层基线 **VLM + π0.5** 相比，ManualVLA 的关键差异在于“统一性”与“协同性”。VLM + π0.5 将规划（VLM生成提示）与执行（π0.5预测动作）割裂为两个独立模型，规划信息仅以文本形式单向传递，缺乏对动作空间的细粒度引导。ManualVLA 则通过 Manual Chain-of-Thought（ManualCoT）实现了规划与动作的双向协同：显式层面，预测的2D坐标被渲染为位置掩码叠加在观测图像上，形成视觉提示；隐式层面，动作专家通过跨任务共享注意力直接关注规划专家生成的手册token，使高层语义与底层动作特征在潜空间中交互。这一设计使 ManualVLA 在三个长程任务上的最终成功率相比 VLM + π0.5 提升15%-30%（Table 2），充分验证了统一MoT架构与双重CoT机制的优势。

### 适用边界与关键假设

ManualVLA 的设计建立在以下关键假设之上，这些假设界定了其适用边界：

1. **目标状态可预定义且可视觉化**：任务必须提供明确的目标状态图像（如LEGO装配的最终结构图、物体重排的目标布局图），这是规划专家生成手册的必要条件。对于目标状态难以用单张图像描述的任务（如“将桌面清理干净”这类开放式指令），ManualVLA 的规划能力可能受限。

2. **任务可分解为离散子目标序列**：ManualCoT 机制假设长程任务可被分解为一系列空间上可定位的子目标（如“将红色积木放置在坐标(120, 340)”）。对于需要连续力控或动态交互的任务（如绳索操作、柔性物体装配），离散的2D坐标提示可能不足以捕捉操作约束。

3. **数字孪生数据可覆盖任务分布**：训练依赖基于3D Gaussian Splatting的数字孪生工具自动合成手册数据（Figure 3）。当真实环境中物体的几何形状、纹理或物理特性与数字孪生显著偏离时，规划专家生成的子目标图像和坐标可能不准确。Table 3 的泛化实验证实了这一点：形状变化导致成功率从0.85降至0.60（-29%），是影响最大的干扰因素。

4. **约100条真实演示的微调依赖**：尽管数字孪生大幅降低了数据需求，ManualVLA 仍需要约100条下游任务遥操作演示进行微调，尚不能实现零样本迁移。

### 局限性与失效模式分析

从实验证据和架构设计出发，可识别以下局限性与潜在失效模式：

**形状泛化脆弱性（-29%）** 是当前最显著的失效模式。Table 3 显示，在物体形状变化下，2D LEGO任务成功率从0.85骤降至0.60，退化幅度远超背景变化（-18%）和光照变化（-17%）。这表明规划专家生成的2D坐标和子目标图像对物体几何特征敏感，数字孪生合成的训练数据未能充分覆盖形状变异。在3D LEGO和物体重排任务中，形状变化同样导致最大退化，说明该问题具有跨任务一致性。

**物理可行性盲区**：手册生成仅基于视觉与文本信息，缺乏力学和物理约束推理。在复杂3D结构中，规划专家可能生成几何上看似合理但物理上不可执行的子目标（如积木悬空放置、物体穿透）。当前实验未报告此类失效的定量统计，但这是多模态手册方法的内在局限，需要人工验证。

**单步错误累积**：ManualVLA 采用自回归式手册生成——当前子目标依赖于上一步的执行结果。若某一步的坐标预测存在偏差（Table 1中物体重排任务的MAE为6.21像素，高于2D LEGO的3.23像素），该误差可能沿任务链传播，导致后续步骤的条件分布偏移。Table 2中关键中间步骤的成功率普遍高于最终任务成功率（如3D LEGO中间步骤0.80 vs 最终0.65），暗示错误累积确实存在。

**架构计算开销**：MoT架构虽带来性能提升，但增加了模型参数量和推理复杂度。消融实验（Figure 6c）证实MoT优于共享参数Transformer，但论文未讨论推理延迟或计算成本，这对于实际部署至关重要。

### 开放问题与未来方向

基于上述分析，以下开放问题值得关注：

1. **跨任务泛化能力验证**：当前实验仅在三个结构相似的长程操作任务上验证。在大规模多任务数据集上联合训练后，ManualVLA 的规划专家是否能生成适用于新任务的通用手册？MoT架构是否支持任务层面的参数扩展？这需要更广泛的基准测试。

2. **显式与隐式CoT的贡献解耦**：Figure 6b 表明同时使用显式（位置掩码）和隐式（跨任务注意力）CoT对成功率至关重要，但两者的相对贡献和交互机制尚不明确。通过梯度归因或消融分析解耦这两种机制，可能指导更高效的架构设计。

3. **减少真实数据依赖**：能否通过更逼真的数字孪生（如引入物理仿真、域随机化）或元学习方法，进一步降低甚至消除对100条真实演示的需求，实现少样本或零样本的规划能力？

4. **扩展到动态与接触丰富任务**：将 ManualVLA 应用于绳索操作、柔性物体装配或需要力控的任务，需要手册生成纳入力学约束，动作专家可能需要力/力矩预测能力，这对当前框架构成根本性挑战。

5. **论文出版信息待确认**：当前分析基于arXiv版本，论文未明确标注发表会议与年份（项目页面和部分引用路径暗示可能投稿CVPR 2026），正式版本中需补充完整出版信息。

## 原文 PDF

![[paperPDFs/CVPR_2026/From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain_of_Thought_Manual_Generation_and_Robotic_Manipulation.pdf]]
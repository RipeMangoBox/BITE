---
title: "MotionPrompt: Optical-Flow Guided Prompt Optimization for Coherent Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- MotionPrompt
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "基于光流的判别器损失：该损失在采样过程中通过仅对部分帧计算梯度来优化可学习的提示词元嵌入，从而间接地控制整个视频的时间一致性。"
primary_logic: "利用提示优化作为视频扩散模型的一种计算高效的引导机制：通过在提示中追加可学习的词元，并利用经过光流训练的判别器对这些词元进行优化，可以间接提升生成视频的时间连贯性，而无需对整个视频序列进行逐帧梯度计算。"
claims:
- "MotionPrompt 通过推理时的语义提示优化提升时间一致性和运动连贯性，无需重新训练模型或为每一帧计算梯度。"
- "光流判别器用于区分真实与生成的光流，并引导提示优化，从而强制实现时间一致性。"
- "在 Lavie、AnimateDiff 和 VideoCrafter2 上，MotionPrompt 提升了物体一致性、减少了时间闪烁并增强了运动平滑度。"
- "VBench 上 Subject Consistency (↑) = 0.9646"
---

# MotionPrompt: Optical-Flow Guided Prompt Optimization for Coherent Video Generation

> [!tip] 核心洞察
> 利用提示优化作为视频扩散模型的一种计算高效的引导机制：通过在提示中追加可学习的词元，并利用经过光流训练的判别器对这些词元进行优化，可以间接提升生成视频的时间连贯性，而无需对整个视频序列进行逐帧梯度计算。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionPrompt：基于光流引导的提示优化实现连贯视频生成 |
| 英文题名 | MotionPrompt: Optical-Flow Guided Prompt Optimization for Coherent Video Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2411.15540) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionPrompt |
| Dataset | VBench |

> [!tip] 效果简介
> - VBench 上，Subject Consistency (↑) 为 0.9646，对比 0.9599，变化 +0.0047。
> - VBench 上，Temporal Flickering (↑) 为 0.9625，对比 0.9487，变化 +0.0138。
> - VBench 上，Motion Smoothness (↑) 为 0.9765，对比 0.9690，变化 +0.0075。

## 概要

### 问题瓶颈

现有的文本到视频（T2V）扩散模型在生成视频时面临两大核心瓶颈：**时间一致性不足**与**运动连贯性缺失**。尽管扩散模型在图像生成上取得了显著成功，但将其扩展至视频域时，逐帧生成往往导致物体闪烁、背景抖动和运动不自然等问题。更关键的是，将 DPS 等传统引导方法直接应用于视频扩散模型，需要在所有帧上进行反向传播梯度计算，这不仅计算成本高昂，而且在数值上不稳定。

### 核心方法：MotionPrompt

本文提出 **MotionPrompt**——一种在推理时通过**语义提示优化**来增强视频生成时间一致性的新方法。其核心思想是：将视频生成的时间一致性约束转化为对提示词元嵌入的优化问题，从而避免对整个视频潜变量序列进行逐帧梯度计算。具体而言，MotionPrompt 在原始文本提示后追加可学习的词元嵌入，并利用一个基于光流的判别器来引导这些词元的优化。该判别器预先训练用于区分真实视频与生成视频中随机帧对之间的光流模式，在采样过程中，仅需对部分帧计算光流梯度，即可间接控制整个视频的时间连贯性。

### 方法定位

MotionPrompt 属于**推理时引导**方法，与需要重新训练模型或修改模型架构的方案正交。它可以即插即用地应用于多种 T2V 扩散模型（如 Lavie、AnimateDiff、VideoCrafter2），无需改变底层模型参数。与 FreeInit（Wu et al., ECCV 2024）等正交方法组合时，MotionPrompt 能在单次噪声初始化后提升时间质量，同时缓解多次 FreeInit 导致的细节损失和饱和度问题。

### 主要结果

在 VBench 基准上，MotionPrompt 在多个基线上均取得了一致性指标的提升：
- 在 **Lavie** 上，主体一致性（Subject Consistency）提升至 0.9646，时间闪烁（Temporal Flickering）提升至 0.9625，运动平滑度（Motion Smoothness）提升至 0.9765。
- 在 **AnimateDiff** 上，主体一致性从 0.9488 提升至 0.9528，运动平滑度从 0.9578 提升至 0.9599。
- 在 **VideoCrafter2** 上，背景一致性（Background Consistency）从 0.9559 显著提升至 0.9774（+0.0215）。

用户研究进一步验证了方法的有效性：在双盲 A/B 测试中，MotionPrompt 分别以 66.5%、55.1% 和 53.0% 的胜率优于 AnimateDiff、Lavie 和 VideoCrafter2。消融实验表明，判别器损失、TV 平滑正则化以及优化时间范围（3 < t < 15）是方法有效的关键因素，优化迭代次数设置为 3 时达到最佳平衡。

### 局限与开放问题

该方法存在以下局限：（1）未施加物理约束，当目标函数与物理规律不一致时可能生成不符合物理规则的视频；（2）引入光流判别器和提示优化后，GPU 显存占用从 11.38 GiB 升至 35.60 GiB，单段视频生成时间从 18.94 秒增至 50.94 秒，计算成本显著增加；（3）方法效果依赖于光流估计的准确性。开放问题包括：如何结合物理合理性评估来保证生成结果的物理可行性，以及判别器跨数据集泛化能力的上限探索。



文本到视频（Text-to-Video, T2V）扩散模型近年来取得了显著进展，但其生成结果仍普遍存在**时间不一致性**与**运动不连贯**的问题。具体表现为视频序列中的物体外观突变、背景闪烁以及帧间过渡不自然，这严重制约了生成视频的实用性与观感质量。

现有的视频生成改进策略主要沿两条路径展开。一类方法通过注入时序注意力层或微调模型架构来增强时间建模能力，但这通常需要重新训练扩散模型，成本高昂且泛化性受限。另一类方法借鉴图像领域的引导技术，如在采样过程中施加额外的损失函数以约束生成方向。然而，将 DPS 等引导方法直接迁移至视频扩散模型面临根本性困难：视频的潜变量张量维度远高于单帧图像，若对每一帧计算梯度并进行反向传播，**计算开销极大且数值不稳定**。这一瓶颈使得高效的视频级引导机制成为亟待填补的研究缺口。

本文的核心动机在于探索一种**计算高效且无需重训练**的视频引导范式。直觉上，文本提示作为扩散模型的条件信号，对生成内容具有全局性的语义控制力——若能通过优化提示来间接调控视频潜变量，就有可能绕开逐帧梯度计算的困境。同时，视频的时间一致性本质上体现为帧间运动的自然性，而**光流（Optical Flow）** 正是刻画帧间运动模式的直接载体。一个自然的思路是：利用判别器评估生成视频的光流是否接近真实运动分布，并将该信号反馈至提示优化过程，从而在语义层面强制模型生成时序连贯的视频。这一思路将提示优化与光流判别相结合，构成了 MotionPrompt 方法的设计原点。



## 核心方法与创新机理

MotionPrompt 的核心创新在于**将推理时的提示优化（Prompt Optimization）作为视频扩散模型的一种计算高效的引导机制**，从而绕开了现有方法在视频生成中面临的两个关键瓶颈：时间一致性与运动连贯性不足，以及逐帧梯度计算带来的高计算成本和不稳定性。

### 瓶颈与因果开关

当前文本到视频扩散模型（如 Lavie、AnimateDiff、VideoCrafter2）在生成视频时普遍存在时间闪烁（temporal flickering）和运动不连贯的问题。将 DPS 等传统引导方法直接应用于视频扩散模型需要在所有帧上进行反向传播以计算潜变量梯度，这不仅大幅增加了计算开销，还容易导致采样过程不稳定。

MotionPrompt 的因果开关（causal knob）是一个**基于光流的判别器损失**。该方法并非直接优化视频潜变量，而是通过在提示词末尾追加少量可学习词元（learnable token embeddings），并利用一个预训练的光流判别器对这些词元进行梯度优化，从而间接地调控整个视频序列的时间一致性。由于判别器损失仅需对部分帧计算光流和梯度，该方法实现了“轻量级”的引导——无需为每一帧计算梯度，也无需重新训练扩散模型本身。

### 三个关键 changed slots

相对于基线模型，MotionPrompt 在以下三个维度上做出了明确的机制性改变：

1. **提示词结构（prompt slot）**：基线模型使用原始文本提示 $P$ 作为条件输入；MotionPrompt 将其扩展为 $P + S$，其中 $S$ 为附加的可学习词元。这些词元在推理过程中被持续优化，而原始提示的语义得以保留。词元初始化采用“authentic”等有助于提升视频质量的词汇。

2. **引导机制（guidance mechanism）**：基线模型仅依赖无分类器引导（classifier-free guidance）；MotionPrompt 在此基础上引入了一个**光流判别器引导的提示优化**过程。该判别器基于 ViT 架构，经过训练后能够区分真实视频与生成视频的光流。在采样过程中，判别器对去噪估计帧的光流输出“真实性”概率，其负对数作为损失函数的一部分，驱动可学习词元的优化，从而强制生成视频的光流趋向真实运动模式。

3. **潜变量优化策略（latent optimization）**：传统方法（如 DPS）直接对潜变量求梯度，需要所有帧参与计算；MotionPrompt 将优化目标从潜变量转移至文本嵌入空间，通过文本编码器对视频生成的全局影响力，仅利用部分帧的光流梯度即可间接控制整个视频潜变量，大幅降低了计算图规模。

### 损失函数设计

提示优化的总损失由三项加权构成：

$$\ell_{\mathrm{total}}(z_t, \mathcal{T}) := \lambda_1 \ell_{\mathrm{disc}}(z_t, c(\mathcal{T})) + \lambda_2 \ell_{\mathrm{TV}}(z_t, c(\mathcal{T})) + \lambda_3 ||\mathcal{T} - \mathcal{T}_0||_2^2$$

其中 $\ell_{\mathrm{disc}}$ 为判别器损失，鼓励生成视频的光流被判别器分类为真实；$\ell_{\mathrm{TV}}$ 为光流的总变差损失，施加空间平滑正则化；第三项为词元嵌入的 $L_2$ 正则化，防止优化后的嵌入偏离初始值过远。三项损失的协同作用使得 MotionPrompt 能够在提升时间一致性和运动平滑度的同时，保持对文本提示的语义对齐。

### 与正交方法的组合能力

MotionPrompt 的设计具有高度的即插即用特性。它不仅可以直接应用于多种文本到视频扩散模型（Lavie、AnimateDiff、VideoCrafter2），还能与正交方法组合使用。例如，与 FreeInit（Wu et al., ECCV 2024）组合时，仅需单次噪声初始化后应用 MotionPrompt，即可在提升时间质量的同时避免多次 FreeInit 导致的细节损失和饱和度问题。此外，该方法还被成功扩展至图像到视频模型 DynamiCrafter，验证了其跨任务泛化能力。



![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of video results generated by the vanilla DynamiCrafter model and our method*

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of MotionPrompt. MotionPrompt enhances temporal consistency in text-to-video diffusion models by combining prompt optimization with an optical flow-based discriminator. Leveraging gradients from a subset of frames and aligning optical flow with real-world motion patterns, MotionPrompt efficiently generates videos with smooth, realistic motion and strong contextual coherence*

MotionPrompt 的整体流程围绕一个核心洞察展开：**通过在文本提示中追加少量可学习词元，并利用光流判别器在采样过程中对这些词元进行优化，可以间接且高效地控制整个视频序列的时间一致性**，而无需对扩散模型的参数进行重新训练，也无需为每一帧计算梯度。

### 框架总览

如图 2 所示，MotionPrompt 的 pipeline 由五个关键模块串联而成，形成一个“编码—去噪—解码—判别—反馈优化”的闭环。

1. **文本编码（Text Encoder）**：将原始文本提示 $P$ 与附加的可学习词元 $S$ 拼接，编码为条件嵌入 $\mathbf{c} = E_{\text{text}}(P+S)$。可学习词元初始化为“authentic”等有助于提升视频质量的词汇嵌入，并在后续步骤中被持续优化。

2. **扩散模型去噪（Diffusion Model $\epsilon_\theta$）**：在标准 DDIM 逆扩散采样框架下，利用文本条件 $\mathbf{c}$ 对噪声潜变量 $\mathbf{z}_t$ 进行逐步去噪，生成去噪潜变量估计 $\hat{\mathbf{z}}_t$。

3. **光流估计（RAFT Optical Flow Estimator）**：将去噪潜变量解码为帧序列 $\hat{\mathbf{x}}_t$ 后，使用预训练的 **RAFT**（Teed & Deng, ECCV 2020）提取帧间光流 $\mathbf{f}(\hat{\mathbf{x}}_t)$。这一步是连接生成内容与运动质量评估的桥梁。

4. **光流判别器（ViT-based Optical Flow Discriminator）**：一个基于 Vision Transformer 的判别器 $\phi_{\theta^*}$，经过训练以区分真实视频的光流与生成视频的光流。它接收 RAFT 输出的光流图，输出一个判别信号，用于评估当前生成视频的运动是否“真实”。

5. **提示优化模块（Prompt Optimization Module）**：在每个优化的时间步，计算包含三个组件的总损失：
   $$ \ell_{\text{total}}(\mathbf{z}_t, \mathcal{T}) = \lambda_1 \ell_{\text{disc}} + \lambda_2 \ell_{\text{TV}} + \lambda_3 \|\mathcal{T} - \mathcal{T}_0\|_2^2 $$
   其中 $\ell_{\text{disc}}$ 鼓励生成光流被判别器分类为真实，$\ell_{\text{TV}}$ 对光流场施加空间平滑正则化，最后一项则防止可学习词元 $\mathcal{T}$ 偏离初始嵌入 $\mathcal{T}_0$ 过远。该损失仅通过可学习词元的梯度反向传播来更新 $\mathcal{T}$，从而间接修正后续采样步中的潜变量。

### 输入输出流

- **输入**：用户提供的文本提示 $P$，以及一个随机初始化的噪声潜变量 $\mathbf{z}_T$。
- **中间状态**：在每个优化时间步 $t$，系统生成去噪估计 $\hat{\mathbf{x}}_t$ 并计算其光流，判别器据此产生损失信号，驱动可学习词元 $\mathcal{T}$ 的更新。
- **输出**：经过完整 DDIM 采样链后解码得到的视频帧序列，其时间一致性和运动平滑度由优化后的提示条件间接保证。

### 关键设计决策

**为什么是提示优化而非潜变量优化？**  
直接将 DPS 等引导方法应用于视频扩散模型需要在所有帧上反向传播梯度，计算成本极高且数值不稳定。MotionPrompt 改为优化文本嵌入——由于文本条件对扩散模型的全局影响，仅需对部分帧计算光流梯度，即可间接控制整个视频的生成质量。这一策略在保持较低计算开销的同时，有效规避了逐帧优化的不稳定性。

**为什么是光流判别器？**  
光流天然编码了帧间的运动信息。通过训练一个判别器来区分真实光流与生成光流，MotionPrompt 将“运动是否自然”这一抽象目标转化为一个可微分的损失函数。判别器在完整干净视频的光流上训练，而在推理时处理去噪估计的光流，这种“训练-推理域差异”通过提示优化的迭代反馈被逐步弥合。

### 与正交方法的组合

MotionPrompt 的设计具有即插即用的特性，可与现有的噪声初始化优化方法（如 **FreeInit**，Wu et al., ECCV 2024）组合使用。实验表明，在 FreeInit 单次噪声初始化后应用 MotionPrompt，既能提升时间质量，又可避免多次 FreeInit 迭代导致的细节损失和饱和度问题（见 Figure 6 及 Table 7）。



MotionPrompt 的核心机制在于将**光流判别器引导**与**提示优化**相结合，在推理时通过仅对部分帧计算梯度来间接控制整个视频的时间一致性。其技术路线可分解为三个关键模块：视频扩散模型基础、提示优化引导机制、以及光流判别器损失设计。

### 视频扩散模型基础

MotionPrompt 建立在标准文本到视频扩散模型之上。给定干净视频潜变量 $\mathbf{z}_0$，前向扩散过程逐步添加高斯噪声：

$$q(\mathbf{z}_t | \mathbf{z}_0) = \mathcal{N}(\mathbf{z}_t; \sqrt{1 - \bar{\alpha}_t} \mathbf{z}_0, \bar{\alpha}_t \mathbf{I})$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数。训练目标为最小化噪声预测误差：

$$\mathbb{E}_{\mathbf{z}_0, \epsilon, t, \mathbf{c}} \left[ \| \epsilon - \epsilon_\theta(\mathbf{z}_t, t, \mathbf{c}) \|^2 \right]$$

推理时采用 DDIM 逆扩散采样，利用 Tweedie 公式估计去噪潜变量 $\hat{\mathbf{z}}_t$：

$$\hat{\mathbf{z}}_t = \frac{1}{\sqrt{\bar{\alpha}_t}} \left( \mathbf{z}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\mathbf{z}_t, t, \mathbf{c}) \right)$$

随后通过无分类器引导修正噪声预测：

$$\epsilon_\theta^w(\mathbf{z}_t, t, \mathbf{c}) = \epsilon_\theta(\mathbf{z}_t, t, \emptyset) + w \left[ \epsilon_\theta(\mathbf{z}_t, t, \mathbf{c}) - \epsilon_\theta(\mathbf{z}_t, t, \emptyset) \right]$$

其中 $w$ 为引导尺度。最终采样步骤为：

$$\mathbf{z}_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \hat{\mathbf{z}}_t + \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon_\theta(\mathbf{z}_t, t, \mathbf{c})$$

### 提示优化引导机制

MotionPrompt 的核心创新在于将**提示优化**作为视频扩散模型的引导手段。具体而言，在原始文本提示 $P$ 后追加可学习词元 $S$，形成扩展提示 $P+S$，并仅对 $S$ 的嵌入进行优化。这一设计的关键优势在于：通过文本嵌入的梯度间接控制视频潜变量，仅需对部分帧计算光流梯度，而无需像 DPS 等方法那样对所有帧进行反向传播。

在每个优化的时间步 $t$，求解以下嵌入优化问题：

$$\hat{\mathbf{c}}_t = \arg\min_{\mathbf{c}} \ell(\mathbf{z}_t, \mathbf{c})$$

优化后的文本嵌入 $\hat{\mathbf{c}}_t$ 用于计算去噪估计：

$$\hat{\mathbf{z}}_t(\hat{\mathbf{c}}_t) = \frac{\mathbf{z}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\mathbf{z}_t, t, \hat{\mathbf{c}}_t)}{\sqrt{\bar{\alpha}_t}}$$

随后执行简化的逆扩散步骤：

$$\mathbf{z}_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \hat{\mathbf{z}}_t(\hat{\mathbf{c}}_t) + \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon_\theta(\mathbf{z}_t, t, \hat{\mathbf{c}}_t)$$

### 光流判别器损失设计

提示优化的总损失函数由三项加权构成：

$$\ell_{\text{total}}(\mathbf{z}_t, \mathcal{T}) := \lambda_1 \ell_{\text{disc}}(\mathbf{z}_t, c(\mathcal{T})) + \lambda_2 \ell_{\text{TV}}(\mathbf{z}_t, c(\mathcal{T})) + \lambda_3 \|\mathcal{T} - \mathcal{T}_0\|_2^2$$

**判别器损失** $\ell_{\text{disc}}$ 是核心驱动力。首先训练一个基于 ViT 的光流判别器 $\phi_{\theta^*}$，其目标为区分真实视频与生成视频的光流：

$$\min_\theta -\mathbb{E}_{\mathbf{f}_r, \mathbf{f}_f} \left[ \log \phi_\theta(\mathbf{f}_r) + \log(1 - \phi_\theta(\mathbf{f}_f)) \right]$$

其中 $\mathbf{f}_r$ 为真实光流，$\mathbf{f}_f$ 为生成光流。训练完成后，在采样过程中利用判别器引导提示优化，鼓励生成视频的光流被分类为真实：

$$\ell_{\text{disc}}(\mathbf{z}_t, c(\mathcal{T})) := \log(1 - \phi_{\theta^*}(\mathbf{f}(\hat{\mathbf{x}}_t(c(\mathcal{T})))))$$

其中 $\hat{\mathbf{x}}_t$ 为去噪潜变量解码后的估计帧，$\mathbf{f}(\cdot)$ 为 RAFT 光流估计器提取的光流场。

**光流总变差损失** $\ell_{\text{TV}}$ 对估计的光流场施加空间平滑正则化，确保光流场满足平滑假设：

$$\ell_{\text{TV}}(\mathbf{z}_t, c(\mathcal{T})) := \sum_{i=1}^{H} \sum_{j=1}^{W} \left( |\mathbf{f}_{i,j} - \mathbf{f}_{i+1,j}| + |\mathbf{f}_{i,j} - \mathbf{f}_{i,j+1}| \right)$$

**词元正则化项** $\|\mathcal{T} - \mathcal{T}_0\|_2^2$ 约束可学习词元 $\mathcal{T}$ 不偏离其初始嵌入 $\mathcal{T}_0$ 过远，以保持原始提示的语义内容。

### 模块交互逻辑

整个流程的核心因果链条为：光流判别器提供时间一致性的监督信号 → 该信号通过梯度反向传播至可学习提示词元 → 优化后的词元嵌入引导扩散模型生成更连贯的视频帧。这一设计的关键瓶颈在于：判别器是在完整干净视频的光流上训练的，而推理时处理的是去噪估计帧的光流，两者之间存在分布偏移。此外，优化仅在特定时间步范围（$3 < t < 15$）内进行，过早或过晚均会降低性能，说明早期噪声过大而后期结构已基本固定的特性限制了引导的有效窗口。



## 实验与关键发现

### 主实验设置

MotionPrompt 在三个主流文本到视频扩散模型上进行验证：**Lavie**（Wang et al., arXiv 2023）、**AnimateDiff**（Guo et al., ICLR 2024）和 **VideoCrafter2**。评估采用 VBench 基准，涵盖主体一致性（Subject Consistency）、背景一致性（Background Consistency）、时间闪烁（Temporal Flickering）、运动平滑度（Motion Smoothness）、动态程度（Dynamic Degree）和整体一致性（Overall Consistency）六项指标。光流判别器基于 ViT 编码器构建，添加投影层将双通道光流适配为 ViT 输入，并使用三层 MLP 作为分类头；训练时使用完整干净视频的光流，推理时则处理去噪估计帧的光流。

### 定量结果

**表 1** 汇总了三个基线与 MotionPrompt 组合后的 VBench 指标。核心发现如下：

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation of text-to-video generation. Bold: Best*

- **Lavie + MotionPrompt**：主体一致性从 0.9599 提升至 0.9646（+0.0047），时间闪烁从 0.9487 提升至 0.9625（+0.0138），运动平滑度从 0.9690 提升至 0.9765（+0.0075）。文本对齐指标（如美学质量、图像质量）几乎未受影响，表明方法在提升时间质量的同时保持了内容保真度。
- **AnimateDiff + MotionPrompt**：主体一致性提升 0.0040（0.9488 → 0.9528），运动平滑度提升 0.0021（0.9578 → 0.9599），背景一致性亦有改善。
- **VideoCrafter2 + MotionPrompt**：背景一致性提升最为显著，从 0.9559 升至 0.9774（+0.0215），主体一致性和时间闪烁也分别改善至 0.9745 和 0.9588。

值得注意的是，所有基线的动态程度（Dynamic Degree）在加入 MotionPrompt 后仅有微小下降，说明方法未以牺牲运动幅度为代价换取一致性。

### 用户研究

**表 2** 展示了通过 Prolific 平台招募的 100 名参与者在双盲 A/B 测试中的偏好分布，每位参与者评估 90 对视频。MotionPrompt 在所有对比中均获得显著偏好：
- 对比 AnimateDiff：胜率 66.5%
- 对比 Lavie：胜率 55.1%
- 对比 VideoCrafter2：胜率 53.0%

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/005_Table_2.jpg]]
*Table 2: User study results*

用户偏好与 VBench 自动化指标的趋势一致，验证了方法在主观感知层面的有效性。

### 消融实验

**表 3** 系统分析了三个关键超参数的影响（以 AnimateDiff 为基线）：

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/006_Table_3.jpg]]
*Table 3: VBench metrics by hyperparameter. t = 0 represents the inital noise. The highlighted row shows the final hyperparameter configuration, yielding well-balanced results. Bold: Best, Underline: Second Best*

**损失权重消融**（行 a–d）：
- 仅使用可学习词元优化（无判别器损失 ℓ_disc，行 a）时，主体一致性为 0.9504；引入 ℓ_disc（行 c）后提升至 0.9528，证明光流判别器损失是时间质量提升的关键驱动因素。
- 增加光流 TV 平滑损失权重 λ₂（行 b → d）可进一步提升运动平滑度（0.9648 → 0.9658），但动态程度从 0.4232 降至 0.4072，揭示了平滑性与运动幅度之间的固有权衡。最终配置选择中等权重以平衡二者。

**优化迭代次数消融**：
- 迭代 3 次达到最佳平衡点：运动平滑度 0.9599，动态程度 0.4125，整体一致性 0.2529。迭代次数过少（1 次）引导不足，过多（5 次）则导致动态程度下降且计算成本增加。

**优化时间步范围消融**：
- 在 3 < t < 15 的时间步范围内应用提示优化效果最优。过早优化（噪声过大时）缺乏有意义的帧结构信息，过晚优化（接近干净帧时）潜变量已趋于稳定，引导空间受限。

**补充消融**（**表 6**）：
- 将可学习词元数量从默认的 1 个增加至 3 个，可略微提升时间质量指标，但动态程度和整体一致性有所下降，表明过多可学习参数可能引入冗余。
- 将词元放置在提示前端或使用 "the" 初始化，均未带来一致的性能增益，验证了默认设置（末端放置、"authentic" 等词初始化）的合理性。

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/011_Table_6.jpg]]
*Table 6: Ablation results comparing the baseline, default setting, increased token count (3 tokens), tokens placed at the front, and tokens initialized with the word ‘the’. Evaluation metrics are reported for subject consistency, background consistency, temporal flickering, motion smoothness, dynamic degree, and overall consistency*

### 与正交方法的组合

MotionPrompt 与噪声初始化方法 **FreeInit**（Wu et al., ECCV 2024）进行了组合实验（**表 7**）。单独使用 FreeInit 进行多次噪声初始化（如 5 步）会引入视频细节损失和饱和度问题；而将 MotionPrompt 与单次 FreeInit 初始化结合，可在提升时间质量的同时相对保持视频质量，表明两者具有互补性。

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/012_Table_7.jpg]]
*Table 7: Quantitative results of FreeInit and FreeInit combined with our method. FI denotes FreeInit, and the number in parentheses indicates the number of noise initialization steps performed. Bold: Best, Underline: Second Best*

### 跨数据集泛化

**表 4** 展示了判别器跨数据集训练的泛化能力。使用 Lavie 和 VideoCrafter2 生成视频训练的判别器，在 AnimateDiff 上推理时仍能带来性能提升，说明光流判别器学到的是相对通用的真实运动模式，而非特定于单一模型的伪影。但跨模型泛化的上限尚未被严格界定。

### 计算成本

**图 8** 报告了计算开销。以 AnimateDiff 为例，加入 MotionPrompt 后 GPU 显存占用从 11.38 GiB 升至 35.60 GiB，单段视频生成时间从 18.94 秒增至 50.94 秒。成本增加主要源于：1）每个优化时间步需通过 RAFT 提取光流；2）判别器前向传播；3）多步梯度反传更新词元嵌入。这是该方法的主要实用瓶颈。

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/014_Figure_8.jpg]]
*Figure 8: Computational cost*

### 可学习词元的动态分析

**图 4** 展示了可学习词元与初始嵌入之间的余弦相似度随去噪时间步 t 的变化。相似度随 t 减小而降低，表明优化过程确实在推动词元嵌入偏离初始语义。对于初始主体一致性较低的视频，嵌入变化幅度更大，暗示方法能自适应地根据生成质量调整引导强度。

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/008_Figure_4.jpg]]
*Figure 4: Cosine similarity between learnable and initial token embeddings. The cosine similarity decreases over time t, with more variation in embeddings observed for videos that initially exhibit lower subject consistency. Table 4. Quantitative results obtained using a discriminator trained on a different dataset. AD and VC2 denote AnimateDiff and VideoCrafter 2, respectively*

### 失败模式与局限

1. **物理合理性缺失**：方法未施加物理约束，当判别器引导的目标与物理规律不一致时，可能生成不符合物理规则的视频（如物体运动轨迹违反动量守恒）。
2. **光流估计依赖**：引导效果受限于 RAFT 光流估计的准确性；在遮挡严重或纹理稀疏的场景中，光流误差可能误导判别器，从而降低引导质量。
3. **计算开销显著**：如前述，显存和推理时间均有约 2.5–3 倍的增加，限制了实时或大规模部署的可行性。

### 关键图表索引

- **表 1**：主实验定量结果，展示三个基线与 MotionPrompt 组合后的 VBench 指标变化。
- **表 2**：用户研究偏好分布。
- **表 3**：损失权重、优化迭代次数、优化时间步范围的消融分析。
- **表 6**：词元数量、位置和初始化词的补充消融。
- **表 7**：与 FreeInit 组合的定量结果。
- **图 4**：可学习词元嵌入的余弦相似度动态变化。
- **图 8**：计算成本对比。

### 补充图表

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/001_Figure.jpg]]
*Figure: Ours "Time lapse video of a farm during sunset."*

![[assets/figures/papers/paper_list_l16_MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video/figures/010_Table_5.jpg]]
*Table 5: Evaluation hyperparameters used for each model*



## 定位与知识库关联

### 1. 与现有方法的继承与分叉关系

MotionPrompt 的核心技术路径建立在两条主线的交叉点上：**扩散模型的推理时引导**与**文本提示优化**。

**提示优化的继承。** 该方法直接延续了 Um 和 Ye（2023）提出的“推理时提示调优”范式——在原始文本提示末尾追加可学习词元嵌入，并在采样过程中仅优化这些嵌入而非整个模型参数。MotionPrompt 将这一范式从图像扩散模型首次迁移至视频扩散模型，关键分叉在于：视频场景下，损失函数的梯度仅需从部分帧的光流计算，而非对所有帧进行反向传播。这一设计使得提示优化成为视频扩散模型的一种计算上可承受的引导手段。

**扩散模型引导的对比。** 传统的扩散模型引导方法（如 DPS，Chung et al.，2023）直接对潜变量求梯度，在视频场景下需要在所有帧上执行反向传播，计算成本高且数值不稳定。MotionPrompt 通过文本嵌入这一“瓶颈”间接控制整个视频序列，规避了逐帧梯度计算的困境。与 FreeInit（Wu et al.，ECCV 2024）等正交方法不同——后者通过迭代噪声初始化改善时间一致性——MotionPrompt 在语义层面进行干预，两者可叠加使用。

**光流判别器的定位。** 方法训练了一个基于 ViT 的光流判别器，用于区分真实视频与生成视频的光流。这一设计在概念上与 GAN 判别器引导（如 StyleGAN 的投影方法）同源，但将其应用于扩散模型采样的中间步骤，且判别对象是光流而非原始像素。判别器损失与光流总变差（TV）损失、词元正则化损失共同构成提示优化的总目标函数。

### 2. 适用的基线模型与组合方式

MotionPrompt 被设计为模型无关的即插即用模块，已在三类文本到视频扩散模型上验证：
- **Lavie**（Wang et al.，arXiv 2023）：基于级联扩散的 T2V 模型。
- **AnimateDiff**（Guo et al.，ICLR 2024）：在预训练 T2I 模型上插入时序注意力层的方案。
- **VideoCrafter2**：开源 T2V 扩散模型。

此外，方法被扩展至图像到视频模型 **DynamiCrafter**，表明其适用边界不限于纯文本条件生成。与 FreeInit 的组合实验显示，在单次噪声初始化后应用 MotionPrompt，可在提升时间质量的同时避免多次 FreeInit 迭代导致的细节损失和色彩饱和问题。

### 3. 适用边界与核心局限

**计算成本。** 引入光流判别器和提示优化后，GPU 显存占用从约 11.38 GiB 升至 35.60 GiB，单段视频生成时间从约 18.94 秒增至 50.94 秒（Figure 8）。这一增加主要来自 RAFT 光流估计和判别器推理的额外开销。

**物理合理性未约束。** 方法的核心损失函数仅基于光流判别器的“真实/生成”二分类信号和光流平滑正则化，未施加任何物理约束。当目标函数与物理规律不一致时，可能生成不符合物理规则的视频——例如，物体运动轨迹违反动量守恒，或形变超出材料弹性极限。论文在开放问题中明确提出，未来可结合评估物理合理性的基础模型（如利用光流或点对应）来缓解这一局限。

**光流质量的依赖。** 引导效果高度依赖 RAFT 光流估计的准确性。在纹理稀疏、运动模糊或遮挡严重的场景下，光流误差可能直接传导至判别器损失，进而误导提示优化的方向。论文未对光流估计失败模式进行系统分析，这一点的稳健性证据较弱，需在实际应用中手动验证。

**判别器的跨模型泛化。** 论文主要使用“配对”判别器——即生成假数据所用的模型与推理时所用模型一致。跨数据集/跨模型的泛化实验（Table 4）显示，使用 Lavie 和 VideoCrafter2 生成的视频训练判别器，在 AnimateDiff 上推理时仍能带来一定提升，但泛化上限尚未被严格界定。

### 4. 开放问题

1. **物理可行性评估。** 如何通过结合评估物理合理性的基础模型（如利用光流或点对应的预训练模型）来保证生成结果在物理上的可行性？这是论文明确指出的未来方向，但目前尚无具体方案。

2. **优化时间步范围的最优性。** 论文通过消融实验确定优化应在 $3 < t < 15$ 的时间步范围内进行（Table 3），并指出过早或过晚均会降低性能。然而，这一范围的最优性仅在 AnimateDiff 上验证，且未给出理论解释——例如，是否与扩散过程的信噪比（SNR）分布或光流判别器的训练-推理分布偏移有关，尚待进一步研究。

3. **判别器泛化的上限。** 跨数据集实验（Table 4）初步表明判别器具有一定泛化能力，但泛化性能的上限在哪里？能否通过对抗训练、数据增强或元学习策略进一步提升跨模型泛化能力？这些问题尚未被系统探索。

4. **多模态引导的扩展。** 当前方法仅使用光流作为运动表征。能否将判别器扩展至其他运动表征（如场景流、轨迹、点对应），或结合多个判别器进行多模态引导，仍有待研究。



## 原文 PDF

![[paperPDFs/CVPR_2025/MotionPrompt_Optical_Flow_Guided_Prompt_Optimization_for_Coherent_Video_Generation.pdf]]

---
title: SemanticWM
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/SemanticWM.pdf
aliases:
- SLDWMSVAWDH
tags:
- arxiv_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 在保持DiT转移模型、动作条件、训练数据和超参数严格不变的前提下，仅切换不同的冻结预训练编码器及其配套的解码/适配器路径（即控制“潜空间种类”这一个变量），从而直接归因不同编码器引发的世界模型性能差异。
primary_logic: 语义对齐的预训练视觉表征（如V-JEPA 2.1、Web-DINO、SigLIP 2）能够天然保留动作引起的变化和任务完成信号，使世界模型在动作恢复（IDM/CEM）、任务成功分类和OpenVLA策略闭环推理中一致且统计显著地优于以像素重建为目标的传统潜空间；视觉保真度不能替代动作与任务语义的保留，因此世界模型的潜空间选择应优先考虑动作与任务结构，而非纯粹的像素重建质量。
claims:
- 语义编码器在VLA共识成功率上显著更高：V-JEPA 2.1达0.344，而VAE仅0.169；语义家族平均高出9.8个百分点（p=0.0129）。
- 语义编码器大幅降低CEM动作规划误差：SigLIP 2的单步误差为0.082，VAE为0.111；语义家族平均降低0.0266（p=0.00015）。
- 语义编码器在逆动力学模型（IDM）中保留更多动作信息：V-JEPA 2.1在编码器潜特征上的Pearson r达0.829（k=1），而VAE仅0.507，且该优势在世界模型生成后仍保持。
- 语义潜空间在任务成功分类探针上精度更高且退化更小：SigLIP 2在世界模型生成潜特征上的准确率为0.823，而VAE为0.716。
---

# SemanticWM

> [!tip] 核心洞察
> 语义对齐的预训练视觉表征（如V-JEPA 2.1、Web-DINO、SigLIP 2）能够天然保留动作引起的变化和任务完成信号，使世界模型在动作恢复（IDM/CEM）、任务成功分类和OpenVLA策略闭环推理中一致且统计显著地优于以像素重建为目标的传统潜空间；视觉保真度不能替代动作与任务语义的保留，因此世界模型的潜空间选择应优先考虑动作与任务结构，而非纯粹的像素重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重建还是语义？什么让潜空间对机器人世界模型有用 |
| 英文题名 | SemanticWM |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.06388) · [Project](https://hskalin.github.io/semantic-wm/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Semantic Latent Diffusion World Model (with S-VAE adapter / wide DDT head) |
| Dataset | BridgeV2, SOAR |

> [!tip] 效果简介
> - BridgeV2 上，VLA Consensus SR (↑) 0.344 (V-JEPA 2.1) vs 0.169 (VAE) (+0.175)；CEM Error k=1 (↓) 0.082 (SigLIP 2) vs 0.111 (VAE) (-0.029)；IDM Pearson r k=1 (↑, WM latents) 0.781 (V-JEPA 2.1) vs 0.476 (VAE) (+0.305)。
> - SOAR 上，Task-success classifier accuracy (↑, WM latents) 0.823 (SigLIP 2) vs 0.716 (VAE) (+0.107)。

## 概述

**核心问题**：机器人世界模型需要同时支持高质量的视觉预测和精确的动作/任务动态建模。当前主流方法普遍采用以像素重建为目标的潜空间（如 VAE），这些潜空间虽擅长图像生成，却未显式编码与操控相关的语义、接触和几何信息。一个关键但未被充分回答的问题是：**重建对齐的潜空间与语义对齐的潜空间，究竟哪一种对下游规划与策略评估更有效？**

**核心发现**：本文通过严格的控制变量实验证明，**语义对齐的预训练视觉表征（V-JEPA 2.1、Web-DINO、SigLIP 2）在动作恢复、任务成功分类和策略闭环推理中一致且统计显著地优于以像素重建为目标的传统潜空间**。视觉保真度不能替代动作与任务语义的保留——世界模型的潜空间选择应优先考虑动作与任务结构，而非纯粹的像素重建质量。

**方法定位**：本文并非提出新的世界模型架构，而是系统性诊断“潜空间种类”这一单一变量对世界模型效用的影响。研究固定 DiT 转移模型、动作条件、训练数据（BridgeV2）和超参数，仅切换不同的冻结预训练编码器及其配套的解码/适配器路径，从而直接归因不同编码器引发的性能差异。对比家族涵盖重建对齐编码器（SD3 VAE、VA-VAE、Cosmos）和语义对齐编码器（V-JEPA 2.1、Web-DINO、SigLIP 2），其中高维语义编码器通过 S-VAE 适配器压缩至 d=96 后接入 DiT。

**主要结果**：
- **策略性能**：语义编码器在 VLA 共识成功率上显著领先——V-JEPA 2.1 达 0.344，而 VAE 仅 0.169；语义家族平均高出 9.8 个百分点（p=0.0129）（Table 1, Table 12）。
- **动作规划**：语义编码器大幅降低 CEM 动作规划误差——SigLIP 2 的单步误差为 0.082，VAE 为 0.111；语义家族平均降低 0.0266（p=0.00015）（Table 1, Table 12）。
- **动作信息保留**：V-JEPA 2.1 在编码器潜特征上的逆动力学模型（IDM）Pearson r 达 0.829（k=1），而 VAE 仅 0.507；该优势在世界模型生成后仍保持（Table 2, Table 13）。
- **任务语义保留**：SigLIP 2 在世界模型生成潜特征上的任务成功分类准确率为 0.823，VAE 为 0.716（Table 14）。
- **鲁棒性**：在 VLA–OOD 平面上，语义编码器更靠近右上角（高成功率 + 高鲁棒性），而重建编码器落在左下角（Figure 3c）。

**方法谱系与知识库定位**：本文工作处于**视觉表征学习 × 机器人世界模型**的交叉点。在表征端，它比较了以 **SD3 VAE**（Esser et al., 2024）、**Cosmos**（Agarwal et al., 2025）为代表的重建对齐自编码器与以 **V-JEPA 2.1**（Bardes et al., 2025）、**Web-DINO**（Darcet et al., 2025，改编自 DINOv2）、**SigLIP 2**（Zhai et al., 2024）为代表的语义对齐方法。在世界模型端，它基于动作条件 DiT 转移模型和流匹配训练范式，与近期扩散世界模型（如 Genie、DINO-WM）共享技术基础，但明确聚焦于潜空间选择这一上游决策对下游规划与策略闭环评估的因果效应，填补了该方向的系统性诊断空白。

## 背景与动机

### 机器人世界模型的核心诉求

机器人世界模型旨在从历史观测和动作序列中预测未来的视觉状态，其形式化目标为学习一个动作条件的预测分布：

$$p ( o_{t+1:t+K} \mid o_{t-H:t}, a_{t-H:t+K-1} )$$

给定过去 $H$ 帧观测和未来 $K$ 步动作，模型需生成未来 $K$ 帧的图像。这一能力是视觉规划、策略评估和模型基强化学习的基石。近年来，基于潜扩散模型（Latent Diffusion Models, LDMs）的世界模型因其在高维视觉生成上的可扩展性和稳定性而受到广泛关注。

### 潜空间选择的盲区

在典型的LDM世界模型管线中，视觉编码器将原始观测映射为潜变量 $z_t = f_{\phi}(o_t)$，扩散转移模型再在潜空间中建模动态。然而，现有工作在选择编码器时，几乎不加审视地沿用为图像重建优化的自编码器（如Stable Diffusion 3 VAE, Esser et al., 2024），其设计目标是最小化像素级重建误差。这隐含了一个未经检验的假设：**擅长像素重建的潜空间，也天然适合建模机器人的动作与任务动态。**

### 重建与语义的潜在张力

这一假设存在根本性张力。重建对齐的潜空间被训练以保留精细纹理、光照和几何细节，但未必编码与操控任务相关的抽象信息——物体的可供性、接触状态、任务进度、动作引起的视觉变化模式。相反，语义对齐的视觉表征（如V-JEPA 2.1、Web-DINO、SigLIP 2）通过大规模自监督或视觉-语言预训练，习得了对场景语义和动作相关变化的敏感性，但其在像素重建上的能力通常弱于专用自编码器。

**核心问题由此浮现：对于机器人世界模型，潜空间究竟应该优先服务于像素重建，还是优先保留动作与任务语义？**

### 本文的切入策略

本文通过严格的变量控制实验来回答这一问题。在保持DiT转移模型架构、动作条件机制、训练数据（BridgeV2）、优化器和训练超参数完全不变的前提下，仅切换不同的冻结预训练编码器及其配套的解码/适配器路径，从而将性能差异直接归因于“潜空间种类”这一个控制变量。这一设计使得对重建对齐家族（VAE、VA-VAE、Cosmos）与语义对齐家族（V-JEPA 2.1、Web-DINO、SigLIP 2）的系统性对比成为可能。

研究从三个维度评估世界模型的效用：(1) 潜空间本身对动作和任务信息的保留能力；(2) 生成视频的视觉质量；(3) 下游策略闭环评估中的任务成功率与行为鲁棒性。这一多维评估框架旨在揭示：当视觉保真度与动作语义保留发生冲突时，哪一个维度对世界模型的实际效用更具决定性。

## 核心创新

本文的核心创新并非提出一种全新的世界模型架构，而是通过严格控制变量实验，揭示了一个此前被忽视的关键设计选择：**机器人世界模型的潜空间类型（重建对齐 vs. 语义对齐）对下游规划与策略性能具有决定性影响**。在保持DiT转移模型、动作条件、训练数据和超参数完全一致的前提下，仅切换冻结的预训练编码器，语义对齐潜空间在动作恢复、任务成功预测和策略闭环评估中系统性地优于以像素重建为目标的传统潜空间。

### 变量控制：潜空间作为唯一因果旋钮

研究的关键方法论创新在于实现了**单变量因果归因**。所有世界模型共享相同的DiT骨干网络、BridgeV2训练数据集、优化器、历史长度和动作条件协议；唯一变化的“changed slot”是编码器及其配套的解码/适配器路径：

- **重建对齐编码器**：Stable Diffusion 3 VAE（Esser et al., 2024）、VA-VAE、Cosmos（Agarwal et al., 2025），产生低维像素优化潜变量，直接馈入DiT。
- **语义对齐编码器**：V-JEPA 2.1（Bardes et al., 2025）、Web-DINO（基于DINOv2，Darcet et al., 2025）、SigLIP 2（Zhai et al., 2024），可选地通过S-VAE适配器压缩至d=96维后馈入DiT，或以原生高维形式配合宽DDT头使用。

这种设计使得性能差异可以直接归因于潜空间的信息结构，而非模型容量或训练协议的差异。

### 核心洞察：视觉保真度不能替代动作与任务语义

实验揭示了一个反直觉的发现：**像素重建质量高的潜空间并不等同于对机器人控制有用的潜空间**。重建对齐编码器虽然在图像级指标（如FID、SSIM）上具有竞争力，但其潜空间中编码的动作信息和任务完成信号显著弱于语义编码器。具体证据链包括：

- **动作信息保留**：在冻结编码器潜特征上训练的逆动力学模型（IDM）显示，V-JEPA 2.1的Pearson r达0.829（k=1），而VAE仅为0.507（Table 2）。这一优势在世界模型生成后仍然保持（DiT-S规模下V-JEPA 2.1为0.781，VAE为0.476，Table 13）。
- **任务语义保留**：在SOAR数据集上训练的任务成功分类探针表明，SigLIP 2在世界模型生成潜特征上的准确率为0.823，而VAE仅为0.716（Table 14, DiT-S）。
- **策略闭环性能**：语义编码器在VLA共识成功率上显著更高——V-JEPA 2.1达0.344，VAE仅0.169；语义家族平均高出9.8个百分点（p=0.0129, Table 1, Table 12）。在VLA–OOD鲁棒性平面上，语义编码器更靠近右上角（高成功率+高鲁棒性），而重建编码器落在左下角（Figure 3c）。

### 适配器设计：弥合语义空间与扩散训练的鸿沟

语义编码器通常产生高维潜变量（如Web-DINO原生1024维），直接用于扩散训练面临计算和优化挑战。本文引入的**S-VAE适配器**将高维语义潜变量压缩至d=96维，在保持语义信息的同时提升扩散训练的便利性。消融实验表明，适配器压缩维度d=96提供了最优权衡：Web-DINO的VLA成功率从原生1024维的0.181提升至0.269（Table 16）。然而，适配器也引入了代价——压缩后的潜空间在CEM动作规划误差和PCK覆盖率上弱于原生语义潜空间，表明适配器可能损害了细粒度动作控制信息（Section 4.6）。

### 方法谱系与知识库定位

本工作位于**语义世界模型**与**潜空间扩散模型**的交叉点。与传统的重建对齐世界模型（如Dreamer系列、基于VAE的扩散世界模型）不同，本文证明预训练的语义视觉表征（来自JEPA、DINO、SigLIP家族）天然保留了动作引起的变化和任务完成信号。与纯语义预测器（如DINO-WM、V-JEPA 2-AC）相比，本文保留了扩散模型的视觉生成能力，同时通过潜空间选择而非架构修改来提升下游任务性能。这一发现对机器人世界模型的设计具有直接的工程指导意义：**潜空间选择应优先考虑动作与任务结构，而非纯粹的像素重建质量**。

## 整体框架

本研究构建了一个动作条件潜扩散世界模型（action-conditioned latent diffusion world model），其核心目标是回答一个根本性问题：**对于机器人世界模型而言，什么样的潜空间是“好”的？** 为此，作者设计了一套高度可控的对比框架——在固定所有其他组件的前提下，仅切换编码器定义的潜空间接口，从而直接归因不同视觉表征对下游规划与策略性能的因果效应。

### 模块架构与数据流

整体 pipeline 由四个模块串联构成，其中仅过渡模型参与训练，其余模块保持冻结：

1. **冻结视觉编码器** $f_\phi$  
   将单帧观测 $o_t$ 映射为空间潜变量 $z_t = f_\phi(o_t) \in \mathbb{R}^{N \times D}$，其中 $N$ 为 token 数，$D$ 为通道维数。这是整个框架唯一的变量——作者在此位置插入了重建对齐编码器（如 Stable Diffusion 3 VAE、VA-VAE、Cosmos）和语义对齐编码器（如 V-JEPA 2.1、Web-DINO、SigLIP 2），从而形成不同的潜空间接口。

2. **冻结适配器** $\alpha_\psi$（可选）  
   当语义编码器输出的潜变量维度过高时（如 Web-DINO 的 1024 维），通过 S-VAE 适配器将其压缩至低维扩散友好空间：$\tilde{z}_t = \alpha_\psi(z_t) \in \mathbb{R}^{N \times d}$，其中 $d = 96$。对于原生低维语义变体，则跳过适配器，直接使用宽头 DDT 解码器。

3. **动作条件 DiT 过渡模型** $p_\theta$  
   这是唯一可训练的模块。给定历史潜变量序列 $\tilde{z}_{t-H:t}$ 和动作序列 $a_{t-H:t+K-1}$，通过流匹配（flow matching）学习预测未来 $K$ 帧的潜轨迹：
   $$\tilde{z}_{t+1:t+K} \sim p_\theta(\cdot \mid \tilde{z}_{t-H:t}, a_{t-H:t+K-1})$$
   所有 DiT 变体共享相同的骨干架构、训练数据集（BridgeV2）、优化器和历史长度，确保唯一的差异来源是上游编码器定义的潜空间。

4. **冻结解码器**  
   将预测的潜变量 $\tilde{z}_{t+1:t+K}$ 映射回像素图像 $\widehat{o}_{t+1:t+K}$，用于视觉质量评估。对于适配器路径，使用适配器自带的像素解码器；对于原生路径，使用编码器配套的解码器。

### 训练与评估协议

- **训练**：仅更新 DiT 过渡模型参数，采用基于最优传输的流匹配损失（详见附录 B.2）。所有模型在 BridgeV2 数据集上训练，动作条件方案保持一致。
- **评估**：从三个维度系统评估世界模型质量——**潜空间效用**（逆动力学动作恢复 IDM、任务成功分类探针、CEM 动作规划误差）、**视觉效用**（SSIM、LPIPS、FID、视频质量指标）以及**闭环策略性能**（通过 InternVL3.5-14B 和 Qwen3.6-27B 双 VLM 裁判的共识成功率与 Borda 排名）。

### 关键控制变量

为建立因果推断，作者严格固定了以下因素：DiT 架构、训练数据、历史帧数、动作条件协议、优化器与训练调度。唯一变动的槽位是**编码器选择及配套的解码/适配器路径**。对于高维语义原生变体，通过浅层宽头 DDT 头保持 DiT token 数固定为每帧 256，确保可比的计算量（参见 Table 4）。

这一框架使得“重建 vs. 语义”的对比具有高度可信的因果归因——任何性能差异均可追溯至编码器所定义的潜空间特性，而非架构或训练协议的混杂效应。

## 核心模块与公式推导

### 问题形式化

机器人世界模型的核心目标是学习一个动作条件的预测分布：

$$p ( o_{t+1:t+K} \mid o_{t-H:t}, a_{t-H:t+K-1} )$$

给定长度为 $H$ 的历史观测序列 $o_{t-H:t}$ 和未来 $K$ 步的动作序列 $a_{t-H:t+K-1}$，模型需要预测未来 $K$ 帧的观测 $o_{t+1:t+K}$。这一形式化将世界模型的任务明确为：在动作信号的驱动下，从历史视觉上下文中推断未来的视觉状态演化。

### 模块化架构设计

整个世界模型由四个功能模块组成，其中**仅转移模型参与训练**，其余模块保持冻结。这种设计使得潜空间的属性完全由编码器的选择决定，从而实现对“潜空间种类”这一变量的严格控制。

**冻结视觉编码器 $f_{\phi}$**  
将单帧观测映射为空间潜变量：

$$z_t = f_{\phi}(o_t) \in \mathbb{R}^{N \times D}$$

其中 $N$ 为空间 token 数量，$D$ 为通道维度。不同编码器在此处定义了截然不同的潜空间——重建对齐编码器（如 Stable Diffusion 3 VAE，Esser et al., 2024）产生面向像素重建的低维潜码，而语义对齐编码器（如 V-JEPA 2.1，Bardes et al., 2025；SigLIP 2，Zhai et al., 2024）则输出保留动作与任务语义的高维表征。

**冻结 S-VAE 适配器 $\alpha_{\psi}$（可选）**  
将高维语义潜变量压缩至扩散友好的低维空间：

$$\tilde{z}_t = \alpha_{\psi}(z_t) \in \mathbb{R}^{N \times d}$$

适配器将语义编码器的高维输出（如 Web-DINO 的 1024 维）压缩至 $d=96$ 维，在保持 DiT token 数量固定为每帧 256 的前提下，确保扩散训练的计算可行性。消融实验表明 $d=96$ 在 VLA 成功率上达到最优权衡（Web-DINO 的 VLA SR 为 0.269，而原生 1024 维仅 0.181）。

**动作条件 DiT 转移模型 $p_{\theta}$**  
从潜空间历史与动作序列中采样未来潜轨迹：

$$\tilde{z}_{t+1:t+K} \sim p_{\theta}(\cdot \mid \tilde{z}_{t-H:t}, a_{t-H:t+K-1})$$

转移模型是唯一可训练模块，采用基于最优传输的流匹配损失进行训练：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\tilde{z}, \epsilon, \tau} \left[ \sum_{i=H}^{T-1} \lVert v_{\theta}(\tilde{z}_{\tau, i}, \tau_i, a_{0:T-1}, \ell) - (\epsilon_i - \tilde{z}_i) \rVert_2^2 \right]$$

其中 $v_{\theta}$ 是速度场预测网络，$\tau$ 为扩散时间步，$\epsilon$ 为噪声样本，$\ell$ 为可选的条件标签。所有世界模型共享相同的 DiT 骨干、训练数据（BridgeV2）、优化器和动作条件协议，仅编码器/适配器/解码器路径不同。

**冻结解码器**  
将预测的潜变量映射回像素图像：

$$\widehat{o}_{t+1:t+K} = \mathrm{Dec}(\tilde{z}_{t+1:t+K})$$

对于重建对齐编码器，使用其原生像素解码器；对于语义编码器，使用适配器配套的像素解码器或原生解码路径。解码器仅用于视觉质量评估，不参与转移模型的训练。

### 关键设计决策

**潜空间隔离**：通过冻结编码器与解码器、仅训练转移模型，确保世界模型性能差异唯一归因于编码器定义的潜空间属性，而非架构或训练协议的变动。

**适配器的双重角色**：适配器在压缩维度的同时，也引入了对细粒度动作信息的潜在损害——语义编码器的原生高维变体在 CEM 动作规划误差和 OOD 鲁棒性上通常优于适配器压缩版本，但在扩散训练的便利性和多数策略指标上适配器版本表现更强。这揭示了压缩与动作信息保留之间的根本张力。

### 补充图表

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/003_Figure_3.jpg]]
*Figure 3: Latent space effect overview: each point is a DiT-S world model trained by varying only the encoder and the associated decoder path. (a) Upper-right is favorable. Latent space metrics show that semantic encoders improve action recoverability, task-success separability, and action planning error (CEM) relative to reconstruction-aligned encoders. (b) Lower-right is favorable. Visual utility metrics show that pixel fidelity alone does not explain downstream performance: reconstruction-aligned spaces remain competitive on low-level image quality, while semantic spaces often improve video and motion quality. (c) Upper-right is favorable. Closed-loop evaluations show that semantic spaces generall...*

## 实验与分析

### 核心结果：语义潜空间在策略与动作恢复上系统性占优

在保持DiT转移模型、动作条件、训练数据（BridgeV2）和超参数完全一致的前提下，仅切换冻结编码器及其配套解码/适配器路径，语义对齐编码器在策略闭环评估和动作恢复指标上一致且统计显著地优于重建对齐编码器。

**VLA共识成功率**方面，V-JEPA 2.1达到0.344，而VAE仅为0.169，语义家族平均高出重建家族9.8个百分点（p=0.0129，Table 12）。**CEM动作规划误差**方面，SigLIP 2的单步误差为0.082，VAE为0.111，语义家族平均降低0.0266（p=0.00015）。**逆动力学模型（IDM）**的Pearson相关系数进一步揭示了根因：V-JEPA 2.1在编码器潜特征上的r达0.829（k=1），VAE仅0.507，且在DiT-S世界模型生成后，语义家族仍保持0.781 vs. 0.476的显著优势（Table 13）。这表明语义潜空间天然保留了更多动作引起的变化信息，使世界模型更容易学习动作到状态转移的映射。

在**VLA–OOD鲁棒性平面**上（Figure 3c），语义编码器更靠近右上角（高成功率+高鲁棒性），而重建编码器落在左下角，说明语义潜空间不仅提升分布内性能，还增强了策略对指令扰动的鲁棒性。

### 视觉质量：重建空间的局部优势与语义空间的视频级领先

在图像级重建指标上，重建对齐编码器保持竞争力。VAE在FID上取得17.43（DiT-S），优于多数语义编码器。然而，在视频级感知质量上，语义编码器开始显现优势：V-JEPA 2.1在FVD上达到102.3，显著低于VAE的145.6（Table 3），说明语义潜空间生成的视频序列在时序一致性上更优。

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/009_Table_3.jpg]]
*Table 3: Visual realism quality for DiT-S and L. Best and runner-up within each size group*

值得注意的是，**语义编码器在自回归外推中展现出更长的有效预测视野**。在45步滚动期间，语义编码器的SSIM差距增长更慢，PCK覆盖率更高（Figure 9），表明其预测的潜轨迹在更长时序上保持与真实轨迹的结构对齐。

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/016_Figure_9.jpg]]
*Figure 9: SSIM gap, LPIPS gap, and PCK coverage over 45 rollout steps. While all encoders show a strictly increasing SSIM/LPIPS gap over the full rollout due to compounding errors (each autoregressive step feeds back slightly corrupted predictions as context), semantic latent spaces from SigLIP2, V-JEPA 2.1 and Web-DINO remain particularly competitive when forced to extrapolate beyond the 10-frame horizon length seen during training. Conversely, PCK coverage remains the highest for semantic encoders*

### 适配器与维度消融：压缩的收益与代价

S-VAE适配器将高维语义潜变量压缩至d=96，显著改善了扩散训练的便利性。Web-DINO在适配器压缩后的VLA成功率达到0.269，而原生1024维仅0.181（Table 16），说明适配器压缩在策略评估维度上是有效的。

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/026_Table_16.jpg]]
*Table 16: Adapter dim. d ablation for Web-DINO DiT-S. Best and runner-up highlighted per row*

然而，适配器压缩并非无代价。在CEM动作误差和PCK覆盖率上，原生高维语义变体（使用wide DDT head）往往表现更好，表明适配器压缩可能损害了细粒度动作控制信息。这一权衡在Figure 6中得到直观展示：适配器提升了VLA成功率和视觉质量，但在动作恢复精度上出现了退化。

### 缩放分析：DiT规模与多视图训练的影响

**DiT规模扩展**（S→B→L）缩小了重建与语义编码器在VLA成功率上的差距，但CEM和IDM的差距仍然存在（Table 10, Table 13）。这表明更大的转移模型可以部分弥补潜空间质量的不足，但无法完全替代动作相关信息的先天保留。

**多视图训练**（Table 15）对动作恢复有显著帮助：VAE在多视图下的CEM误差从0.111降至0.047，但视觉质量出现退化（FID从17.43升至22.03），揭示了动作恢复与视觉保真度之间的张力。

### 失败模式与局限性

语义潜空间在精细几何和接触细节上可出现失真。例如，在抽屉开合任务中，语义编码器生成的图像可能出现抽屉位置不够精确、物体形状变形等问题（详见论文定性示例）。这意味着在需要精确物理交互的操控任务中，纯语义潜空间可能不足以提供足够的几何精度。

此外，当前实验局限于BridgeV2单机器人场景，尚未拓展到其他机器人平台或更复杂的仿真环境。策略闭环评估依赖两个VLM裁判（InternVL3.5-14B和Qwen3.6-27B），其标准可能引入人类偏好偏差。

### 关键图表结论汇总

- **Table 1**：DiT-S规模下，语义编码器在VLA共识成功率、CEM误差和交互质量上全面领先重建编码器。
- **Table 2**：语义编码器在IDM动作恢复和任务成功分类探针上保留更多信息，且该优势在世界模型生成后仍保持。
- **Table 3**：重建编码器在图像级FID上占优，语义编码器在视频级FVD上领先。
- **Figure 3**：在潜空间效用、视觉效用和策略性能三个轴上，语义编码器整体更靠近有利区域。
- **Figure 5**：多视图训练提升动作恢复但损害视觉质量；DiT规模扩展缩小策略差距但未消除动作恢复差距。
- **Figure 9**：语义编码器在45步自回归外推中保持更低的SSIM/LPIPS差距和更高的PCK覆盖率。

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/007_Figure_5.jpg]]
*Figure 5: Scaling camera views (left) and DiT sizes (right)*

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/004_Table_1.jpg]]
*Table 1: DiT-S policy and behavioral metrics. Best and runner-up per column. In-distribution (ID) SR and Out-of-Distribution (OOD) SR are calculated on a subset of 10 episodes with InternVL 3.5. Consenus SR and Borda rank aggregate InternVL3.5-14B and Qwen3.6-27B rankings. Interaction quality measures the plausibility of robot-object contact. PCK coverage measures point tracking recall (Appx. C). Muted ± terms show one standard deviation error averaged over episodes*

### 补充图表

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/011_Table_4.jpg]]
*Table 4: Architecture size and compute. Adapter-based semantic encoders are marked with ^ { 9 6 } and use the S-VAE adapter with d=96. Native semantic rows do not use adapter in the DiT and use a shallow-wide DDT head. All DiT parameter counts are for DiT-L. Note that the extra DiT parameters are due to the shallow-wide head, which does not contribute much to the depth of the DiT. For DiTs using high-dimensional latents of V-JEPA 2.1, Web-DINO, and SigLIP, decoding uses the adapter’s pixel decoder as the surrogate*

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/019_Table_10.jpg]]
*Table 10: Policy and behavioral metrics for different DiT sizes: small (S), base (B), and large (L). Best and runner-up within each size group. In-distribution (ID) SR: InternVL3.5 on the 10 episodes shared with OOD evaluations. OOD SR: InternVL3.5 only. Borda rank (lower = better) aggregates InternVL3.5-14B, and Qwen3.6-27B rankings. Muted ± terms show one standard deviation averaged over episode for SR and CEM metrics*

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/021_Table_12.jpg]]
*Table 12: Uncertainty estimates for policy-facing metrics. Cells show means with 95% bootstrap confidence intervals. VLA SR uses consensus VLM success; OOD SR pools distractor and instruction shifts; CEM is one-step controllability error. Family-level rows compare semantic encoders against reconstruction encoders. Best and runner-up are scoped per column*

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/022_Table_13.jpg]]
*Table 13: Inverse Dynamics Model action-recovery (Pearson r averaged over action dimensions) for horizons k=1 and k=4. Real = on encoded GT latents (the encoder ceiling); WM = on world-model rollouts. Best and runner-up per column*

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/023_Table_14.jpg]]
*Table 14: Trajectory success-probe accuracy across DiT sizes. Enc. Acc/AUC is computed on encoded ground-truth latents (the probe ceiling); per-DiT columns are accuracy on world-model rollouts and the absolute Drop from the encoder ceiling (lower is better). Best and runner-up per column. Dashed rule separates VAE-like and SSL encoders*

![[assets/figures/papers/SemanticWM_2605.06388_ae409282f58b/figures/025_Table_15.jpg]]
*Table 15: DiT-S single-view vs multi-view. Each cell for PSNR and LPIPS shows the WM value with the gap to its encoder’s reconstruction ceiling in parentheses (smaller = closer to ceiling). Best and runner-up per column across all rows; the WM value and gap are highlighted independently. The two adapter pairs (V-JEPA $2 _ { 9 6 } , \mathrm { W e b – D I N O _ { 9 6 } }$ ) only have multi-view data for CEM. Best within each column*

## 方法谱系与知识库定位

### 1. 问题定位：从“重建保真度”到“任务效用”的范式转换

机器人世界模型（World Model）的核心功能是在潜空间中模拟环境动态，以支撑规划、策略评估与行为合成。长期以来，该领域的主流实践是将视觉重建对齐的潜空间——特别是基于变分自编码器（VAE）或其变体——作为世界模型的默认表示层。这一选择的隐含假设是：更高的像素重建质量意味着更丰富、更可用的内部表征。

本文对该假设发起了系统性挑战。作者将问题精确地表述为：**在保持扩散转移模型、动作条件、训练数据和训练协议完全不变的前提下，仅切换冻结的预训练编码器及其配套的解码/适配器路径，不同的潜空间类型（重建对齐 vs. 语义对齐）会如何影响世界模型在下游任务中的表现？** 这一受控实验设计将“潜空间种类”确立为唯一的因果变量，使得性能差异可以直接归因于编码器所诱导的表示结构，而非模型容量或训练配方的差异。

### 2. 方法谱系：重建对齐与语义对齐的编码器家族

本文构建了一个清晰的编码器谱系，将对比对象分为两大阵营：

**重建对齐编码器（Reconstruction-aligned）** 以像素级自编码为目标，追求低失真压缩。本文纳入的基线包括：
- **Stable Diffusion 3 VAE**（Esser et al., 2024）：当前扩散模型社区最广泛使用的潜空间标准，将图像压缩至低维连续表示。
- **VA-VAE**：另一种重建导向的变分自编码器变体。
- **Cosmos**（Agarwal et al., 2025）：面向物理世界建模的重建对齐编码器。

**语义对齐编码器（Semantics-aligned）** 通过自监督或视觉-语言对比预训练获取对任务语义、物体类别和动作变化敏感的表征。本文纳入的代表性编码器包括：
- **V-JEPA 2.1**（Bardes et al., 2025）：基于联合嵌入预测架构（JEPA）的语义编码器，在视频预测任务中学习动作相关的不变性。
- **Web-DINO**（Darcet et al., 2025）：从DINOv2演化而来的大规模自监督视觉编码器，擅长捕获细粒度语义对应。
- **SigLIP 2**（Zhai et al., 2024）：基于Sigmoid损失的视觉-语言对比编码器，在跨模态对齐任务中表现优异。

两类编码器的关键差异在于**优化目标所塑造的表示几何**。重建编码器将容量分配给高频纹理和精确像素值，而语义编码器将容量分配给对任务完成和动作执行具有判别力的抽象特征。Figure 2的诊断可视化直接揭示了这一差异：语义编码器诱导的潜空间轨迹在动作相关方向上呈现出更清晰、更可分离的几何结构，其逆动力学模型（IDM）特征与真实动作之间的典型相关系数和聚合动作对齐度量显著更高。

### 3. 技术适配：将语义潜空间接入扩散世界模型框架

直接将高维语义编码器接入潜扩散模型面临两个工程挑战：（1）语义编码器通常输出高维特征（如Web-DINO的1024维），增加了扩散模型的训练难度；（2）语义编码器缺乏原生像素解码器，无法将预测潜变量映射回图像空间进行视觉评估。

本文通过两条技术路径解决上述问题：
- **S-VAE适配器路径**：引入一个冻结的轻量适配器 $\alpha_{\psi}$，将高维语义潜变量 $z_t \in \mathbb{R}^{N \times D}$ 压缩至紧凑的扩散友好特征 $\tilde{z}_t \in \mathbb{R}^{N \times d}$（$d=96$），同时提供配套的像素解码器。这一设计借鉴了RAE的宽头（wide-head）和调度偏移（schedule-shift）配方。
- **原生宽DDT头路径**：对于不使用适配器的语义编码器，采用宽DDT头直接将DiT输出映射回像素空间，保持DiT的token数固定为每帧256个，确保计算量可比。

所有世界模型共享相同的DiT转移模型 $p_{\theta}$、流匹配训练损失 $\mathcal{L}_{\mathrm{FM}}$、BridgeV2数据集、历史长度（$H$帧）和动作条件协议。转移模型的训练目标为：

$$p ( o_{t+1:t+K} \mid o_{t-H:t}, a_{t-H:t+K-1} )$$

其中编码器 $f_{\phi}$ 将观测映射为潜变量，适配器（可选）进行压缩，DiT从历史潜变量和动作序列中采样未来潜轨迹，解码器最终将预测潜变量映射回像素图像。**只有转移模型参与训练，编码器、适配器和解码器始终冻结**——这一设计确保性能差异完全归因于潜空间本身的结构特性，而非联合微调带来的混杂效应。

### 4. 知识库定位：与相关工作的关系

**相对于重建对齐世界模型**：本文的结论对以像素生成为核心评价标准的传统范式构成了直接挑战。实验表明，VAE在图像级指标（如FID）上保持竞争力，但在动作恢复（CEM误差）、任务成功分类和策略闭环评估中系统性地落后于语义编码器。这意味着**视觉保真度不能替代动作与任务语义的保留**，世界模型的潜空间选择应优先考虑任务结构而非纯粹的像素重建质量。

**相对于语义世界模型**：本文与DINO-WM、V-JEPA 2-AC等非扩散语义世界模型形成互补。这些工作证明了语义表征在规划和控制中的价值，但未在统一的扩散框架内进行严格的编码器消融。本文通过固定扩散架构，将语义空间的贡献与扩散模型本身的优势进行了解耦分析。然而，一个重要的开放问题是：**扩散架构的迭代采样能力与语义空间的判别能力之间是否存在协同效应，以及如何量化这种效应？**

**相对于多模态基础模型**：本文的策略评估采用了两个独立的视觉-语言模型（InternVL3.5-14B和Qwen3.6-27B）作为裁判，通过共识成功率（Consensus SR）和Borda排名来缓解单一评判偏差。这一设计将世界模型研究置于当前VLA（Vision-Language-Action）评估的前沿，但也引入了新的方法论问题：VLM裁判的标准可能引入人类偏好偏差，对不同任务的敏感度不完全一致。

### 5. 适用边界与关键局限

本文的结论建立在严格的实验条件之上，其适用边界需要谨慎界定：

**数据与平台局限**：所有实验均在BridgeV2数据集上进行，该数据集主要包含单臂桌面操控任务。作者明确指出尚未拓展到其他机器人平台（如ALOHA双臂、Franka）或更复杂的仿真环境（如RoboCasa）。语义潜空间在多平台、多任务场景下的泛化性仍需验证。

**几何精度与语义保留的权衡**：尽管语义潜空间在任务语义上更优，但在精细几何和接触细节上可出现失真（如抽屉开合不够、物体形状变形）。Figure 9的45步自回归外推分析显示，语义编码器在SSIM差距和LPIPS差距的增长上更缓慢，PCK覆盖率更高，表明其有效预测视野更长。但在需要精确物理交互的操控任务中，几何失真可能成为瓶颈。**如何联合优化语义潜空间的几何精度和任务语义保留，是当前方法的核心局限。**

**适配器的双刃剑效应**：适配器压缩（$d=96$）改善了扩散训练的便利性（Table 16显示Web-DINO在适配器路径下VLA SR=0.269 vs. 原生1024维的0.181），但似乎损害了细粒度动作控制信息——适配器变体在CEM动作误差和PCK覆盖率上通常弱于原生语义变体。**是否存在自适应维度或条件压缩方法，可以在高精度动作规划和高质量视觉生成之间取得更好的平衡？**

**评估体系的可靠性**：策略闭环评估依赖两个VLM裁判，其评估标准可能随任务类型而变化。引入更客观的物理接触检测或仿真反馈，可能是提高策略评价可靠性的必要步骤。

### 6. 开放问题与未来方向

本文揭示的“语义优先”原则为机器人世界模型研究开辟了若干关键方向：

1. **联合优化框架**：如何设计端到端的训练目标，同时保留语义编码器的任务判别力和重建编码器的几何精度？这可能需要超越当前的冻结编码器范式，探索条件适配或解耦表示学习。

2. **规模化效应**：DiT从S扩展到L时，重建编码器与语义编码器在VLA成功率上的差距缩小，但CEM和IDM的差距依然显著。在更大规模、更多视角和更多样化的机器人数据上，语义潜空间的优势是否会进一步扩大，还是存在一个“表示饱和”的上限？

3. **与非扩散语义世界模型的融合**：如何将语义潜空间扩散世界模型与JEPA预测器等非扩散方法结合，实现更高效且更具解释性的规划？这涉及扩散采样的计算成本与语义空间判别效率之间的权衡。

4. **任务感知的表示选择**：不同下游任务（如视觉伺服、力控装配、长序列任务规划）可能偏好不同类型的语义信息。是否存在一种“表示选择策略”，能够根据任务需求动态调整潜空间的使用方式？

## 原文 PDF

![[paperPDFs/arxiv_2026/SemanticWM.pdf]]
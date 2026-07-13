---
title: "DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DriveVLA_W0_World_Models_Amplify_Data_Scaling_Law_in_Autonomous_Driving_1311ad3bd77a.pdf
project_link: null
code_link: "https://github.com/BraveGroup/DriveVLA-W0"
aliases:
- DW
- DriveVLA-W0
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入世界建模作为密集的自监督目标，迫使模型预测未来图像，从而学习环境的底层动态和丰富的预测性世界表示。
primary_logic: 通过预测未来图像提供密集的视觉监督，世界建模将数据扩展规律从饱和转为持续提升，使得VLA模型能够更好地利用大规模数据，从而在扩展数据时大幅超越仅动作监督的基线。
claims:
- 在70M帧规模数据集上，添加世界建模使VQ模型的ADE降低28.8%，ViT模型的碰撞率降低15.9%，而仅动作监督的基线趋于饱和。
- 世界建模将预训练从有害（导致负迁移）变为有益，在跨域迁移中显著提升PDMS（VLA-W0-VQ从68.7提升至85.6），表明学习了可迁移的视觉表示。
- 世界建模使DriveVLA-W0在单目相机输入下超越多相机+LiDAR的方法，在NAVSIM v1/v2上达到最先进水平。
- NAVSIM v1 上 PDMS = 93.0 (DriveVLA-W0‡, 1x Cam)
---

# DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving

> [!tip] 核心洞察
> 通过预测未来图像提供密集的视觉监督，世界建模将数据扩展规律从饱和转为持续提升，使得VLA模型能够更好地利用大规模数据，从而在扩展数据时大幅超越仅动作监督的基线。

| 字段 | 内容 |
|------|------|
| 中文题名 | DriveVLA-W0：世界模型放大了自动驾驶中的数据扩展规律 |
| 英文题名 | DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=plrGn3RdzN) · [Code](https://github.com/BraveGroup/DriveVLA-W0) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | DriveVLA-W0 |
| Dataset | NAVSIM v1, NAVSIM v2, In-house 70M frames |

> [!tip] 效果简介
> - NAVSIM v1 上，PDMS 93.0 (DriveVLA-W0‡, 1x Cam) vs 92.1 (AutoVLA‡, 3x Cam) (+0.9 (且使用更少的输入))。
> - NAVSIM v2 上，EPDMS 86.1 (DriveVLA-W0, 1x Cam) vs 84.5 (DiffusionDrive, 3x Cam + L) (+1.6)。
> - In-house 70M frames 上，ADE (m) 1.0563 (VLA-VQ + World Model) vs 1.4829 (VLA-VQ, action-only) (-28.8%)。

## 概要

### 核心问题：VLA模型的“监督赤字”瓶颈

大型视觉-语言-动作（VLA）模型在自动驾驶中展现出巨大潜力，但其面临一个根本性瓶颈——**监督赤字**：模型容量庞大（可达7-8B参数），却仅由稀疏的低维动作信号（如转向角、速度）进行监督。这种稀疏监督导致模型的大量表示能力未被充分利用，无法学习丰富的世界表示。实验表明，仅使用动作监督的VLA基线在数据规模增长时性能迅速趋于饱和（Table 3），揭示了单纯扩展模型容量或数据量无法突破这一瓶颈。

### 核心洞察：世界建模放大数据扩展规律

DriveVLA-W0的核心洞察是**将世界建模作为密集的自监督目标引入VLA训练**，迫使模型预测未来图像，从而学习环境的底层动态和丰富的预测性世界表示。这一设计将数据扩展规律从饱和转为持续提升：在70M帧规模数据集上，添加世界建模使VQ模型的ADE降低28.8%，ViT模型的碰撞率降低15.9%，而仅动作监督的基线已趋于平台期（Table 3）。更关键的是，世界建模将跨域预训练从有害（导致负迁移）变为有益——VLA-W0-VQ的PDMS从68.7提升至85.6（Figure 4, Table 7），表明模型学到了可迁移的视觉表示。

### 方法定位

DriveVLA-W0并非一个全新的模型架构，而是一种**训练范式**，其核心改动体现在三个层面：

1. **监督信号扩展**：在传统动作监督基础上，增加密集的世界建模自监督信号——通过自回归预测离散视觉令牌（AR World Model）或扩散模型预测未来图像（Diffusion World Model），为VLA骨干提供丰富的学习目标。

2. **联合训练目标**：优化目标从单纯的$\mathcal{L}_{\mathrm{Action}}$扩展为$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \alpha \mathcal{L}_{\mathrm{WM-AR}}$（AR变体）或$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \beta \mathcal{L}_{\mathrm{WM-Diff}}$（扩散变体）。

3. **高效推理架构**：引入Mixture-of-Experts设计，将大型VLA Expert与轻量级Action Expert（500M）通过Joint Attention融合，动作专家负责高效解码，将推理延迟降至基线的63.1%（Figure 6）。

### 主要结果

在NAVSIM v1上，DriveVLA-W0以**单目相机输入**达到PDMS 93.0，超越使用3相机输入的AutoVLA（92.1）；在NAVSIM v2上，EPDMS达到86.1，超越使用3相机+LiDAR的DiffusionDrive（84.5），在传感器输入更少的情况下实现了最先进水平（Table 1, Table 2）。在70M帧规模的自有数据集上，世界建模带来的性能增益随数据量增长而持续放大，验证了数据扩展规律的突破。

### 方法谱系与知识库定位

DriveVLA-W0处于**VLA自动驾驶与世界模型**的交叉点。与BEV-based方法（如**UniAD** (Hu et al., CVPR 2023)、**TransFuser** (Prakash et al., TPAMI 2023)、**Hydra-MDP** (Li et al., arXiv 2024)）不同，它直接使用前视图图像作为VLA输入，无需显式BEV转换或多视图融合。与现有VLA方法（如**AutoVLA** (Zhou et al., NeurIPS 2025)、**ReCogDrive** (Li et al., arXiv 2025)）相比，其关键区别在于引入世界建模作为辅助训练目标，而非仅依赖动作监督。在世界模型方面，该方法借鉴了自回归视觉生成和潜在扩散模型的思想，但将其重新定位为VLA训练的密集监督源，而非独立的生成任务。

### 自动驾驶VLA模型的“监督赤字”困境

视觉-语言-动作（VLA）模型已成为端到端自动驾驶的核心范式。这类模型将语言指令、前视图像和过去动作序列交织为多模态输入序列，通过大规模骨干网络（如Emu3 8B或Qwen2.5-VL 7B）直接输出驾驶动作。然而，当前VLA模型面临一个根本性瓶颈：**监督赤字**。模型容量巨大，参数量可达数十亿，但监督信号仅来自稀疏的低维动作标签——通常只是几个轨迹路点的坐标值。这种稀疏的动作监督导致模型的大量表示能力未被利用，无法学习丰富的世界表示，使得数据扩展的收益迅速饱和。

### 世界建模：从稀疏到密集的监督范式转变

DriveVLA-W0的核心洞察在于将世界建模引入VLA训练框架，从根本上改变监督信号的密度。传统VLA仅最小化动作预测的交叉熵损失 $\mathcal{L}_{\mathrm{Action}}$，而DriveVLA-W0联合优化动作预测损失与世界模型损失——即迫使模型预测未来图像。这一范式转变的关键在于：**预测未来图像提供了密集的视觉监督**，迫使模型学习环境的底层动态和丰富的预测性世界表示，而非仅仅拟合动作标签。

具体而言，对于离散视觉令牌VLA（VQ变体），采用自回归世界模型预测未来图像的离散视觉令牌序列，其损失为：

$$\mathcal{L}_{\mathrm{WM-AR}} = - \sum_{i=1}^{N} \log P(v_i | S_{<V_t}, v_{<i})$$

对于连续视觉特征VLA（ViT变体），采用扩散世界模型在潜在空间中重建未来图像，其损失为：

$$\mathcal{L}_{\mathrm{WM-Diff}} = \mathbb{E}_{z_{t+1}, \epsilon, k} [\| \epsilon - \hat{\epsilon}(z_{t+1,k}, k, F_t^V, F_t^A) \|^2]$$

总训练目标为 $\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \alpha \mathcal{L}_{\mathrm{WM-AR}}$（AR变体）或 $\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \beta \mathcal{L}_{\mathrm{WM-Diff}}$（扩散变体）。

### 世界建模放大数据扩展律

世界建模带来的最深远影响在于**改变了数据扩展律的形态**。如Figure 1所示，仅使用动作监督的VLA基线在数据量增长时性能迅速趋于饱和，而加入世界建模后，模型性能随数据规模持续提升。在70M帧规模的自建数据集上，VLA-VQ+世界模型相比仅动作监督基线，ADE降低28.8%（从1.4829降至1.0563），碰撞率降低19.7%（从0.0488降至0.0392），而基线模型在该数据规模下已无明显提升（Table 3）。

更关键的是，世界建模将预训练从“有害”转变为“有益”。Figure 4和Table 7显示，仅动作监督的VLA在跨域迁移中遭受负迁移（VLA-VQ的PDMS从68.7下降），而加入世界建模后，同一模型在跨域迁移中PDMS大幅提升至85.6。这表明世界建模使模型学到了可迁移的视觉表示，而非仅仅记忆特定动作分布。

### 推理效率的架构创新

为在引入世界建模的同时保持实时推理能力，DriveVLA-W0采用Mixture-of-Experts架构：大型VLA Expert负责世界建模和深层理解，轻量级Action Expert（500M参数）通过Joint Attention与VLA Expert融合特征，高效解码驾驶动作。Joint Attention的查询、键、值拼接为：

$$Q = [Q_{\mathrm{VLA}}; Q_{\mathrm{AE}}], \quad K = [K_{\mathrm{VLA}}; K_{\mathrm{AE}}], \quad V = [V_{\mathrm{VLA}}; V_{\mathrm{AE}}]$$

这一设计使推理延迟大幅降低：查询式专家延迟约74ms（仅为基线的63.1%），自回归专家在NAVSIM平均5.6 tokens时仅95ms（基线118ms）。世界建模本身在推理时被跳过以保证实时性，但其在训练中建立的丰富表示已内化到模型参数中。

综上，DriveVLA-W0通过世界建模解决了VLA模型的监督赤字问题，将数据扩展律从饱和转为持续提升，并在仅使用单目相机输入的条件下，在NAVSIM v1/v2上超越了使用多相机+LiDAR的方法，达到最先进水平。

## 核心方法与创新机理

### 动机：VLA的“监督赤字”瓶颈

当前自动驾驶视觉-语言-动作（VLA）模型面临一个根本性瓶颈：**监督赤字**。VLA主干网络（如Emu3 8B或Qwen2.5-VL 7B）拥有巨大的表示容量，但其训练仅由稀疏的低维动作信号（如轨迹路点坐标）监督。这种稀疏监督导致模型的大量表示能力未被利用，无法学习丰富的世界表示，从而在数据规模扩展时迅速饱和——即**数据扩展规律失效**。

### 创新1：世界建模作为密集自监督信号

DriveVLA-W0的核心创新在于**将世界建模引入VLA训练**，通过预测未来图像提供密集的视觉监督信号，迫使模型学习环境的底层动态和预测性世界表示。具体而言，模型在预测驾驶动作的同时，额外承担预测未来视觉场景的任务（Figure 1a）。

这一设计将VLA的训练目标从单一的稀疏动作监督转变为**动作监督 + 密集世界建模自监督**的联合优化。世界建模提供两种实现方式：

- **自回归世界模型（AR World Model）**：针对将图像表示为离散视觉令牌的VLA（如基于Emu3的VLA-VQ），通过自回归生成未来图像的离散视觉令牌序列，损失函数为：

$$\mathcal{L}_{\mathrm{WM-AR}} = - \sum_{i=1}^{N} \log P(v_i | S_{<V_t}, v_{<i})$$

- **扩散世界模型（Diffusion World Model）**：针对使用连续视觉特征的VLA（如基于Qwen2.5-VL的VLA-ViT），通过潜在扩散模型在VLA输出特征的条件下生成未来图像，损失函数为：

$$\mathcal{L}_{\mathrm{WM-Diff}} = \mathbb{E}_{z_{t+1}, \epsilon, k} [\| \epsilon - \hat{\epsilon}(z_{t+1,k}, k, F_t^V, F_t^A) \|^2]$$

总训练目标为动作预测损失与世界模型损失的加权联合优化：

$$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \alpha \mathcal{L}_{\mathrm{WM-AR}} \quad \text{或} \quad \mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \beta \mathcal{L}_{\mathrm{WM-Diff}}$$

**关键因果机制**：世界建模提供的密集视觉监督使模型在预训练阶段被迫学习场景几何、物体动态和交通参与者的未来状态，从而建立起可迁移的预测性世界表示。这一表示在后续的规划任务中直接转化为性能增益——当数据规模扩大时，世界建模使得性能持续提升，而仅动作监督的基线趋于饱和（Figure 1b）。

### 创新2：MoE推理架构实现高效动作解码

为缓解大VLA骨干直接生成动作带来的高推理延迟，DriveVLA-W0引入**混合专家（Mixture-of-Experts, MoE）架构**：保留完整VLA骨干作为“VLA Expert”负责多模态理解与世界建模，同时引入一个轻量级“Action Expert”（约500M参数）专门负责动作解码。

两个专家通过**联合注意力（Joint Attention）**机制融合：

$$Q = [Q_{\mathrm{VLA}}; Q_{\mathrm{AE}}], \quad K = [K_{\mathrm{VLA}}; K_{\mathrm{AE}}], \quad V = [V_{\mathrm{VLA}}; V_{\mathrm{AE}}]$$

该架构将推理延迟降至基线的约63.1%（查询式专家约74ms），同时保持了大规模VLA的表示能力。Action Expert支持三种解码策略——查询式、自回归和流匹配——为不同数据规模下的精度-效率权衡提供了灵活选择。

### 创新3：改变预训练的性质——从负迁移到正迁移

世界建模带来的最深刻变化在于**改变了预训练的本质**。在仅动作监督的设置下，跨域预训练往往导致**负迁移**（性能下降），因为模型在稀疏信号下学到的表示过度拟合源域的动作分布。而加入世界建模后，预训练转变为**正迁移**：在视觉分布相似但动作分布不同的数据集之间，世界建模使模型学习到可迁移的视觉世界表示，从而在目标域上显著提升性能（Figure 4，VLA-W0-VQ的PDMS从68.7提升至85.6）。

### 与基线方法的本质差异

相较于现有VLA方法（如**AutoVLA** (Zhou et al., NeurIPS 2025)、**ReCogDrive** (Li et al., arXiv 2025)）仅依赖稀疏动作监督，以及BEV方法（如**UniAD** (Hu et al., CVPR 2023)、**DiffusionDrive** (Liao et al., CVPR 2025)）依赖多传感器融合，DriveVLA-W0的差异化优势在于：

| 维度 | 基线方法 | DriveVLA-W0 |
|------|----------|-------------|
| 监督信号 | 仅动作监督（稀疏） | 动作监督 + 世界建模自监督（密集） |
| 数据扩展律 | 快速饱和 | 持续提升 |
| 预训练迁移 | 可能负迁移 | 正迁移 |
| 传感器需求 | 多相机+LiDAR | 仅单目相机 |
| 推理效率 | 大模型直接解码（延迟高） | MoE架构（延迟降低约37%） |

这一创新组合使得DriveVLA-W0在仅使用单目相机输入的条件下，超越了使用多相机和激光雷达的SOTA方法，在NAVSIM v1上达到PDMS 93.0，在NAVSIM v2上达到EPDMS 86.1。

DriveVLA-W0 的整体训练范式围绕一个核心洞察展开：**通过世界建模提供密集自监督信号，放大视觉-语言-动作（VLA）模型在大规模数据上的扩展规律**。传统 VLA 方法仅依赖稀疏的动作标签作为监督，导致模型容量巨大但表示能力未被充分利用。DriveVLA-W0 在动作监督的基础上，引入预测未来图像的世界建模任务，迫使模型学习环境的底层动态和丰富的预测性世界表示。

### 输入与标记化

模型接收三类输入：语言导航指令 $L_t$、单目前视图像 $V_t$ 以及历史动作序列 $A_{t-1}$。这些多模态信息按时间步拼接为统一序列：

$$S_t = [L_{t-H}, V_{t-H}, A_{t-H-1}, \dots, L_t, V_t, A_{t-1}]$$

其中 $H$ 为历史窗口长度。对于图像，模型支持两种表示方式：离散视觉令牌（用于 VQ-VLA 变体）和连续视觉特征（用于 ViT-VLA 变体）。

### VLA 骨干

VLA 骨干采用大规模视觉-语言模型（如 Emu3 8B 或 Qwen2.5-VL 7B）处理上述多模态序列，输出隐藏状态特征。基线 VLA 仅通过最小化动作预测的交叉熵损失进行训练：

$$\mathcal{L}_{\text{Action}} = - \sum_{i=1}^{L} \log P(a_i | S_t, a_{<i})$$

这一稀疏监督范式在数据规模增大时趋于饱和，限制了模型从大规模数据中获益的能力。

### 世界建模模块

世界建模是 DriveVLA-W0 的核心创新，提供两种实现方式（见 Figure 2）：

- **自回归世界模型（AR World Model）**：针对离散视觉令牌 VLA，以自回归方式预测未来图像的离散视觉令牌序列，损失函数为：

$$\mathcal{L}_{\text{WM-AR}} = - \sum_{i=1}^{N} \log P(v_i | S_{<V_t}, v_{<i})$$

- **扩散世界模型（Diffusion World Model）**：针对连续特征 VLA，训练一个潜在扩散模型，以 VLA 输出的多模态特征为条件，去噪生成未来图像，损失函数为：

$$\mathcal{L}_{\text{WM-Diff}} = \mathbb{E}_{z_{t+1}, \epsilon, k} [\| \epsilon - \hat{\epsilon}(z_{t+1,k}, k, F_t^V, F_t^A) \|^2]$$

最终训练目标为动作预测损失与世界模型损失的联合优化：

$$\mathcal{L}_{\text{Total}} = \mathcal{L}_{\text{Action}} + \alpha \mathcal{L}_{\text{WM-AR}} \quad \text{或} \quad \mathcal{L}_{\text{Total}} = \mathcal{L}_{\text{Action}} + \beta \mathcal{L}_{\text{WM-Diff}}$$

### MoE 动作专家

为解决大 VLA 骨干直接生成动作带来的高推理延迟问题，DriveVLA-W0 采用混合专家（Mixture-of-Experts, MoE）架构（见 Figure 3）。一个轻量级动作专家（Action Expert，约 500M 参数）与大 VLA Expert 并行工作，通过联合注意力（Joint Attention）机制进行特征融合：

$$Q = [Q_{\text{VLA}}; Q_{\text{AE}}], \quad K = [K_{\text{VLA}}; K_{\text{AE}}], \quad V = [V_{\text{VLA}}; V_{\text{AE}}]$$

动作专家支持三种解码策略：查询式（query-based）、自回归（autoregressive）和流匹配（flow matching），最终通过规划头将动作输出转换为 3 秒、6 个路点的连续轨迹。

### 两阶段训练范式

模型采用两阶段训练：第一阶段使用 6VA 序列配置预训练 VLA 骨干，联合优化世界模型损失和动作损失；第二阶段集成动作专家，使用 2VA 输入，仅通过动作损失进行监督。在推理时，世界模型模块被跳过以保证实时性，仅保留动作专家进行高效解码。

DriveVLA-W0 的核心架构围绕一个关键洞察展开：**通过预测未来图像提供密集自监督信号，解决大型 VLA 模型的“监督赤字”问题**。传统 VLA 仅由稀疏的低维动作信号监督，大量表示能力未被利用；DriveVLA-W0 引入世界建模作为补充训练目标，迫使模型学习环境的底层动态和丰富的预测性世界表示。

### 输入标记化与 VLA 骨干

模型输入为多模态序列的交织拼接。给定语言指令 $L_t$、前视图图像 $V_t$ 和过去动作 $A_{t-1}$，在 $H$ 步历史窗口内形成输入序列：

$$S_t = [L_{t-H}, V_{t-H}, A_{t-H-1}, \ldots, L_t, V_t, A_{t-1}]$$

VLA 骨干（Emu3 8B 或 Qwen2.5-VL 7B）处理该序列并输出隐藏状态特征。对于将图像表示为离散视觉令牌的变体（VLA-VQ），图像经 MoVQGAN 编码为离散令牌序列；对于连续特征变体（VLA-ViT），图像经 ViT 编码为连续特征。

### 世界建模模块

世界建模是方法的核心创新，提供两种实现方式：

**自回归世界模型（AR World Model）**：将未来图像预测建模为离散视觉令牌的自回归生成任务。模型以过去观测和动作为条件，逐令牌预测未来图像的离散视觉令牌序列。其损失函数为标准的下一个令牌预测交叉熵损失：

$$\mathcal{L}_{\mathrm{WM-AR}} = - \sum_{i=1}^{N} \log P(v_i | S_{<V_t}, v_{<i})$$

其中 $v_i$ 为未来图像的第 $i$ 个离散视觉令牌，$S_{<V_t}$ 为当前图像之前的所有多模态上下文序列，$N$ 为总令牌数。

**扩散世界模型（Diffusion World Model）**：以 VLA 输出的视觉特征 $F_t^V$ 和动作特征 $F_t^A$ 为条件，训练一个潜在扩散模型来去噪生成未来图像的潜在表示。其损失函数为标准的扩散 MSE 损失：

$$\mathcal{L}_{\mathrm{WM-Diff}} = \mathbb{E}_{z_{t+1}, \epsilon, k} [\| \epsilon - \hat{\epsilon}(z_{t+1,k}, k, F_t^V, F_t^A) \|^2]$$

其中 $z_{t+1}$ 为未来图像的潜在表示，$\epsilon$ 为随机噪声，$k$ 为噪声步数，$\hat{\epsilon}$ 为去噪网络预测的噪声。

### 联合训练目标

世界建模与动作预测联合优化，形成统一的训练目标。对于 AR 变体：

$$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \alpha \mathcal{L}_{\mathrm{WM-AR}}$$

对于扩散变体：

$$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Action}} + \beta \mathcal{L}_{\mathrm{WM-Diff}}$$

其中动作预测损失为标准交叉熵损失：

$$\mathcal{L}_{\mathrm{Action}} = - \sum_{i=1}^{L} \log P(a_i | S_t, a_{<i})$$

$\alpha$ 和 $\beta$ 为平衡系数，控制世界建模损失与动作损失的相对权重。

### MoE 动作专家与联合注意力

为解决大 VLA 骨干直接进行动作解码导致的高延迟问题，方法引入 Mixture-of-Experts 架构。轻量级 Action Expert（500M 参数）与完整 VLA Expert 并行工作，通过 Joint Attention 机制融合特征：

$$Q = [Q_{\mathrm{VLA}}; Q_{\mathrm{AE}}], \quad K = [K_{\mathrm{VLA}}; K_{\mathrm{AE}}], \quad V = [V_{\mathrm{VLA}}; V_{\mathrm{AE}}]$$

其中 $Q_{\mathrm{VLA}}, K_{\mathrm{VLA}}, V_{\mathrm{VLA}}$ 来自 VLA Expert 的隐藏状态，$Q_{\mathrm{AE}}, K_{\mathrm{AE}}, V_{\mathrm{AE}}$ 来自 Action Expert。拼接后的查询、键、值矩阵送入联合注意力层，使 Action Expert 能够高效利用 VLA 骨干的丰富表示进行动作解码。

动作专家支持三种解码策略：**查询式（query-based）**直接预测固定数量轨迹锚点的偏移量；**自回归式（autoregressive）**逐令牌生成动作序列；**流匹配式（flow matching）**通过预测向量场将简单分布映射到目标轨迹分布。实验表明，在大规模数据下自回归专家表现最优，揭示了模型容量与精度的权衡。

### 两阶段训练流程

训练采用两阶段范式：第一阶段使用 6VA 序列配置（6 步交错的视觉-动作历史）预训练 VLA 骨干，联合优化世界模型损失和动作损失；第二阶段集成 Action Expert，使用 2VA 输入，仅由动作损失监督。世界建模模块在推理时被跳过以保证实时性，其生成的密集监督信号仅在训练阶段发挥作用。

![[assets/figures/papers/paper_list_l68_https_openreview_net_forum_id_plrGn3RdzN/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of DriveVLA-W0, which achieves world modeling in two ways: (a) an AR World Model that predicts discrete visual tokens, and (b) a Diffusion World Model that denoises latent representations conditioned on multimodal inputs*

![[assets/figures/papers/paper_list_l68_https_openreview_net_forum_id_plrGn3RdzN/figures/003_Figure_3.jpg]]
*Figure 3: (a) Our Mixture-of-Experts (MoE) architecture pairs a large VLA Expert with a lightweight Action Expert for efficient inference. (b-d) This framework serves as a testbed for comparing three action decoding schemes: query-based, autoregressive, and flow matching*

## 实验与关键发现

### 核心实验设置

实验在两个公开基准和一个大规模内部数据集上展开。**NAVSIM v1** 与 **v2** 是端到端规划评测基准，分别采用 PDMS 和 EPDMS 作为综合评分，其计算公式为：

$$
\mathrm{PDMS} = \mathrm{NC} \times \mathrm{DAC} \times \frac{5 \times \mathrm{EP} + 5 \times \mathrm{TTC} + 2 \times \mathrm{C.}}{12}
$$

$$
\mathrm{EPDMS} = \mathrm{NC} \times \mathrm{DAC} \times \mathrm{DDC} \times \mathrm{TLC} \times \frac{5 \times \mathrm{EP} + 5 \times \mathrm{TTC} + 2 \times \mathrm{LK} + 2 \times \mathrm{HC} + 2 \times \mathrm{EC}}{16}
$$

内部数据集包含 70M 帧驾驶数据，用于验证数据扩展规律。模型采用两阶段训练：第一阶段用 6VA 序列（6 步交织视觉-动作）联合优化动作损失与世界模型损失预训练 VLA 骨干；第二阶段集成动作专家，以 2VA 输入仅用动作损失监督。公平性方面，所有内部实验使用相同的训练/评估流程与数据量，NAVSIM 上各变体均经过 NuPlan 预训练再微调。

### 主要结果：单目相机下的 SOTA 性能

在仅使用**单目前视相机**的条件下，DriveVLA-W0 在两个基准上均取得最优。

**NAVSIM v1 结果（Table 1）**：DriveVLA-W0‡ 以 PDMS 93.0 超越使用 3 相机的 AutoVLA‡（92.1）和 WoTE（91.6），在更少传感器输入下实现 +0.9 的领先。DriveVLA-W0† 的 PDMS 为 88.4，同样优于多相机+LiDAR 的 DiffusionDrive（88.2）和 Hydra-MDP（87.5）。

**NAVSIM v2 结果（Table 2）**：DriveVLA-W0 取得 EPDMS 86.1，超越 DiffusionDrive（84.5，3 相机+LiDAR）和 AutoVLA（84.1，3 相机），领先幅度 +1.6。这表明世界建模使单目 VLA 具备超越多传感器 BEV 方法的规划能力。

### 数据扩展实验：世界建模放大扩展规律

这是论文的核心验证实验（Table 3）。在 70M 帧内部数据集上，**仅动作监督的基线随数据增长趋于饱和**，而加入世界建模后性能持续提升：

![[assets/figures/papers/paper_list_l68_https_openreview_net_forum_id_plrGn3RdzN/figures/007_Table_3.jpg]]
*Table 3: World modeling outperforms action-only supervision with data scaling. Unlike baseline models that plateau early under sparse supervision, our VLA-W0 models show consistent improvement*

- **VLA-VQ 变体**：仅动作监督的 ADE 为 1.4829m，加入 AR World Model 后降至 1.0563m，降幅 28.8%；碰撞率从 0.0488% 降至 0.0392%，降幅 19.7%。
- **VLA-ViT 变体**：加入 Diffusion World Model 后，ADE 从 1.1019m 降至 0.9763m（-11.4%），碰撞率从 0.0453% 降至 0.0381%（-15.9%）。

该结果直接验证了论文的核心主张：**世界建模提供的密集视觉监督将数据扩展规律从饱和转为持续提升**，使得大容量 VLA 模型能够真正利用大规模数据。

### 跨域泛化：从负迁移到正迁移

Figure 4 和 Table 7 揭示了一个关键现象：在仅动作监督下，预训练反而导致负迁移（PDMS 下降），而加入世界建模后预训练变为有益。具体而言，VLA-W0-VQ 的 PDMS 从 68.7 提升至 85.6（+16.9），VLA-W0-ViT 从 78.2 提升至 85.0（+6.8）。这表明世界建模迫使模型学习可迁移的视觉世界表示，而非过拟合特定动作分布。

![[assets/figures/papers/paper_list_l68_https_openreview_net_forum_id_plrGn3RdzN/figures/011_Table_7.jpg]]
*Table 7: World model enhances generalization to new action distributions. This table presents the detailed result of Figure 4*

### 动作专家性能反转

Table 4 展示了一个值得注意的现象：在小规模数据上表现最优的查询式（query-based）动作专家，在 70M 帧大规模数据上被自回归（AR）专家超越。AR 专家在 70M 帧上达到 ADE 1.0069，优于查询式专家的 1.0563。这一反转揭示了**模型容量与精度的权衡**：简单的 AR 解码在大数据下受益于更强的序列建模能力，而查询式专家可能在小数据下因其归纳偏置更有效。

### 消融实验

**预训练序列设计（Table 5）**：使用交织视觉-动作序列（6VA）预训练优于仅视觉序列（6V），PDMS 从 84.1 升至 85.6，表明动作信息对世界建模至关重要。

**时间上下文长度（Table 6）**：更长序列（6VA，PDMS 85.6）优于短序列（VA 82.9，2VA 84.1），验证了时间上下文对世界建模的价值。

**世界模型时间间隔（Table 9）**：输入间隔 1 秒最优（PDMS 85.6），仅当前帧（VA）为 82.9，间隔 4 秒为 84.3。过短缺乏时间上下文，过长引入过度场景变化。

**生成质量与规划性能正相关（Table 8）**：6VA 预训练模型具有更低 FID（4.610 vs 2VA 的 9.847）和更高规划 PDMS（85.6 vs 84.1），表明世界模型的生成保真度与规划能力呈正相关。

### 推理效率

MoE 动作专家大幅降低推理延迟（Figure 6）：查询式专家延迟约 74ms（基线的 63.1%），自回归专家在 NAVSIM 平均生成 5.6 tokens 时仅 95ms（基线 118ms）。流匹配和查询式专家延迟恒定，而 AR 专家和 VLA 基线延迟随生成 token 数线性增长。

### 失败模式分析

论文通过 Figure 11 和 Figure 12 展示了两个典型失败模式：

1. **导航指令歧义**：在 Y 形路口，粗糙的“直行”指令无法明确指向左或右分支，导致模型犹豫并驶入岔口区域。这暴露了当前 NAVSIM 离散指令集（仅左转/直行/右转）在复杂道路拓扑中的粒度不足。

2. **动态物体预测困难**：世界模型在复杂交叉路口未能预测对面来车的出现，导致规划器在不知潜在冲突的情况下错误执行左转。这指出了精细动态物体建模是未来研究的重要方向。

![[assets/figures/papers/paper_list_l68_https_openreview_net_forum_id_plrGn3RdzN/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on the NAVSIM v1. NC: no at-fault collision. DAC: drivable area compliance. TTC: time-to-collision. C.: comfort. EP: ego progress. PDMS: the predictive driver model score. Abbreviations: 1x Cam (single front-view camera), Nx Cam (surroundview cameras), L (LiDAR). ∗: Using the query-based action expert. †: Using the query-based action expert with multiple trajectory anchors following Li et al. (2024b). ‡: Using the AR action expert with the best-of-N (N=6) strategy following Zhou et al. (2025d)*

![[assets/figures/papers/paper_list_l68_https_openreview_net_forum_id_plrGn3RdzN/figures/009_Table_5.jpg]]
*Table 5: Ablation study on vision-only vs*

## 定位与知识库关联

### 1. 方法谱系：从稀疏动作监督到密集世界建模

DriveVLA-W0 的核心贡献在于将 VLA（Vision-Language-Action）模型的训练范式从“仅动作监督”推向了“动作监督 + 密集世界建模自监督”的联合优化。其方法谱系可沿两条线索梳理：**BEV-based 基线**和**VLA-based 基线**。

#### 1.1 与 BEV-based 方法的关系

BEV（Bird's-Eye-View）方法是自动驾驶规划的主流范式，通常依赖多相机环视输入和/或激光雷达点云来构建显式的鸟瞰图表示。代表性工作包括：

- **UniAD**（Hu et al., CVPR 2023）：端到端自动驾驶框架，在 BEV 空间统一感知、预测和规划。
- **TransFuser**（Prakash et al., TPAMI 2023）：基于 Transformer 的多模态融合方法，将图像和激光雷达特征在 BEV 空间融合。
- **Hydra-MDP**（Li et al., arXiv 2024）：多目标蒸馏框架，在 BEV 空间学习多模态驾驶策略。
- **DiffusionDrive**（Liao et al., CVPR 2025）：基于扩散模型的规划方法，在 BEV 空间生成轨迹。
- **WoTE**（Li et al., ICCV 2025）：基于世界模型的 BEV 规划方法，利用预测未来 BEV 表示来辅助决策。

**关键差异**：DriveVLA-W0 在**仅使用单目前视相机（1x Cam）** 的条件下，在 NAVSIM v1 上达到 PDMS 93.0，在 NAVSIM v2 上达到 EPDMS 86.1，均超越了使用多相机+激光雷达的 BEV 方法（如 DiffusionDrive 在 NAVSIM v2 上为 84.5，使用 3x Cam + LiDAR）。这表明世界建模学到的丰富视觉表示在某种程度上弥补了传感器输入的不足。但需注意，DriveVLA-W0 并未直接与 BEV 方法在架构层面竞争——它走的是 VLA 路线，依赖大规模预训练 VLM 骨干（Emu3 8B / Qwen2.5-VL 7B），而 BEV 方法通常使用较小的专用骨干。

#### 1.2 与 VLA-based 方法的关系

VLA 方法将视觉-语言模型（VLM）扩展到动作预测，是近年来自动驾驶的新兴方向。代表性基线包括：

- **AutoVLA**（Zhou et al., NeurIPS 2025）：典型的 VLA 基线，仅使用动作监督训练，在 NAVSIM v1 上使用 3x Cam 达到 PDMS 92.1。
- **ReCogDrive**（Li et al., arXiv 2025）：另一 VLA 基线，同样依赖稀疏动作监督。

**DriveVLA-W0 的突破**：在相同 VLA 范式下，DriveVLA-W0 通过引入世界建模，将 VLA 的训练目标从单纯的 $\mathcal{L}_{\mathrm{Action}}$ 扩展为联合优化 $\mathcal{L}_{\mathrm{Action}} + \alpha \mathcal{L}_{\mathrm{WM-AR}}$（AR 变体）或 $\mathcal{L}_{\mathrm{Action}} + \beta \mathcal{L}_{\mathrm{WM-Diff}}$（扩散变体）。这一改动带来的效果是决定性的：在 70M 帧规模的 in-house 数据集上，VLA-VQ + World Model 的 ADE 较 action-only 基线降低 28.8%，碰撞率降低 19.7%（Table 3）。而 action-only 基线在此规模下已趋于饱和——这直接验证了论文的核心主张：**世界建模放大了数据扩展规律**。

#### 1.3 方法谱系中的“监督信号”转变

从方法论角度，DriveVLA-W0 的关键创新在于将 VLA 训练的**监督信号**从稀疏的动作标签扩展为密集的未来图像预测。这一思路与自监督表示学习（如 MAE、DINO）有哲学上的亲缘关系，但将其嵌入到 VLA 的端到端训练中，并直接验证了其对下游规划性能的因果影响。具体而言：

- **AR World Model**：在离散视觉令牌空间中自回归预测未来图像，损失函数为 $\mathcal{L}_{\mathrm{WM-AR}} = - \sum_{i=1}^{N} \log P(v_i | S_{<V_t}, v_{<i})$。
- **Diffusion World Model**：在连续潜在空间中通过扩散模型去噪未来图像，损失函数为 $\mathcal{L}_{\mathrm{WM-Diff}} = \mathbb{E}_{z_{t+1}, \epsilon, k} [\| \epsilon - \hat{\epsilon}(z_{t+1,k}, k, F_t^V, F_t^A) \|^2]$。

### 2. 适用边界与关键局限

尽管 DriveVLA-W0 在多个基准上取得了最先进的结果，其适用边界和局限同样值得关注。

#### 2.1 动态物体预测的不足

论文明确指出了世界模型在预测复杂交叉路口的**精细动态物体**（如对面来车）方面存在困难。Figure 12 的失败案例显示，世界模型未能预测到未来帧中出现的对向来车，导致规划器在不知情的情况下错误执行左转。这一局限的根源可能在于：世界模型以图像重建为目标，对动态物体的细粒度运动建模缺乏显式约束，且 VLA 骨干的视觉编码器可能未针对动态物体跟踪进行优化。

#### 2.2 导航指令的粒度问题

当前 NAVSIM 基准的导航指令集仅限于简单的“直行/左转/右转”，在复杂道路拓扑（如 Y 形路口）中会引起指令歧义。Figure 11 的失败案例展示了这一问题：模型收到“直行”指令，但由于分叉路口的结构，该指令无法明确对应左支或右支，导致模型犹豫并驶入分叉区域。这是基准本身的局限，但也指出了 VLA 方法在语言-视觉-动作对齐上的一个开放挑战。

#### 2.3 世界模型生成能力的推理时利用

论文的两阶段训练范式（第一阶段联合训练世界模型和动作预测，第二阶段仅用动作损失微调 Action Expert）意味着**世界模型在推理时被跳过**以保持实时性。虽然这保证了低延迟（查询式专家约 74ms，自回归专家在平均 5.6 tokens 时约 95ms），但也意味着世界模型学到的丰富预测性表示无法直接用于在线决策。论文将此列为未来方向：探索生成信息在推理中的利用。

#### 2.4 传感器模态的扩展性

当前 DriveVLA-W0 仅使用单目前视相机。尽管其性能已超越多相机+激光雷达的方法，但如何将世界建模范式扩展到多相机或激光雷达输入，同时保持世界建模的效率和优势，仍是一个开放问题。直接增加输入模态可能导致世界建模的计算开销显著增加。

### 3. 开放问题

基于论文的分析和局限，以下开放问题值得后续研究关注：

1. **精细动态物体建模**：如何改进世界模型对动态物体的预测能力？可能的路径包括引入光流监督、物体级预测头，或结合 BEV 空间的动态预测。

2. **细粒度导航语言指令**：如何设计更细粒度的导航指令集，以解决复杂路口的歧义问题？这涉及语言-空间推理的更深层对齐。

3. **动作专家性能反转的理论解释**：Table 4 揭示了在大规模数据下，简单的自回归动作专家（ADE 1.0069）优于更复杂的查询式专家（ADE 1.0563）和流匹配专家（ADE 1.0291）。这一“反转现象”的理论解释是什么？是否与模型容量、优化难度或表示瓶颈有关？

4. **世界模型生成信息的在线利用**：世界模型生成的未来图像是否可以直接作为额外的输入信息来辅助实时规划？这需要在推理延迟和额外信息收益之间找到平衡。

5. **多模态世界建模的扩展**：如何将 DriveVLA-W0 的世界建模范式扩展到多相机或 LiDAR 输入？是否需要为不同模态设计不同的世界建模目标？

## 原文 PDF

![[paperPDFs/ICLR_2026/DriveVLA_W0_World_Models_Amplify_Data_Scaling_Law_in_Autonomous_Driving_1311ad3bd77a.pdf]]

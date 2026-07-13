---
title: Towards Decompositional Human Motion Generation with Energy-Based Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Decompositional_Human_Motion_Generation_with_Energy_Based_Diffusion_Models.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Towards_Decompositional_Human_Motion_Generation_with_Energy-Based_Diffusion_Models_CVPR_2026_paper.html
project_link: https://jiro-zhang.github.io/DeMoGen/
code_link: null
aliases:
- DDMG
- TDHMGEBDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过基于能量的扩散模型，将每个动作概念建模为独立的能量函数（潜变量感知EBM通过去噪网络输出，语义感知EBM通过分解式交叉注意力），并通过对K个概念的能量分布进行平均聚合来组合训练，使模型能够自主发现动作中的概念级分解。
primary_logic: 扩散模型的去噪网络可被解释为能量函数（∇_x E_θ(x) ∝ ε_θ(x)），因此可以通过对K个概念分别计算能量（噪声预测）并求平均，或通过将交叉注意力拆分为K个并行分支并聚合输出（分解式交叉注意力 DCA），来实现从整体动作中分解出多个语义可解释的动作概念。这种能量组合训练范式使模型在无需分解动作真值的情况下学习概念级分解。
claims:
- DEMOGEN将每个动作概念表示为一个能量分数，通过组合训练发现动作的分解结构，无需分解动作真值。
- 潜变量感知EBM通过对K个概念的去噪网络输出求平均来捕获组合能量分布。
- 语义感知EBM通过分解式交叉注意力（DCA）将交叉注意力拆分为K个并行分支并聚合输出。
- 三种变体在HumanML3D上一致提升文本-动作匹配精度，表明分解训练范式的有效性。
---

# Towards Decompositional Human Motion Generation with Energy-Based Diffusion Models

> [!tip] 核心洞察
> 扩散模型的去噪网络可被解释为能量函数（∇_x E_θ(x) ∝ ε_θ(x)），因此可以通过对K个概念分别计算能量（噪声预测）并求平均，或通过将交叉注意力拆分为K个并行分支并聚合输出（分解式交叉注意力 DCA），来实现从整体动作中分解出多个语义可解释的动作概念。这种能量组合训练范式使模型在无需分解动作真值的情况下学习概念级分解。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于能量扩散模型的分解式人体动作生成 |
| 英文题名 | Towards Decompositional Human Motion Generation with Energy-Based Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Towards_Decompositional_Human_Motion_Generation_with_Energy-Based_Diffusion_Models_CVPR_2026_paper.html) · [Project](https://jiro-zhang.github.io/DeMoGen/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DEMOGEN (Decompositional Motion Generation) |
| Dataset | HumanML3D, MTT |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 ↑ 0.588 (DEMOGEN-OSS, latent-aware) vs 0.581 (SALAD) (+0.007)；R-Precision Top-3 ↑ 0.863 (DEMOGEN-EXP, semantic-aware) vs 0.815 (EnergyMoGen) (+0.048)；FID ↓ 0.078 (DEMOGEN-EXP, latent-aware) vs 0.076 (SALAD) (+0.002 (接近最优))。
> - MTT (multi-concept) 上，R@1 ↑ 14.9 (DEMOGEN-OSSt, latent-aware) vs 先前最优 (EnergyMoGen/STMC) (显著提升)。
> - MTT (compositional) 上，R@1 ↑ 16.2 (DEMOGEN-Expt, latent-aware) vs 先前最优 (EnergyMoGen/STMC) (显著提升)。

## 概要

### 问题背景与核心瓶颈

文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列。近年来，扩散模型在这一领域取得了显著进展，催生了**MDM**（Tevet et al., arXiv 2022）、**MLD**（Chen et al., arXiv 2022）、**ReMoDiffusion**（Zhang et al., arXiv 2023）等一系列代表性工作。然而，现有方法普遍将动作视为一个不可分割的整体序列进行建模，缺乏对动作内部结构化组合的理解。

这一设计存在根本性局限：人类动作天然具有**组合性**——"一边走路一边挥手"由"走路"和"挥手"两个运动原语复合而成。将动作建模为单一整体，意味着模型无法像人类一样推理和重组动作概念，这限制了其在复杂组合生成、细粒度运动编辑等场景中的表现。尽管**EnergyMoGen**（Zhang et al., CVPR 2025）和**STMC**（Petrovich et al., CVPRW 2024）等近期工作开始探索组合式动作生成，但它们仍依赖于预定义的概念边界或外部组合策略，未能实现从整体动作中自主发现概念级分解。

### 核心方法：DEMOGEN

针对上述瓶颈，本文提出**DEMOGEN**（Decompositional Motion Generation），一种基于能量扩散模型的**分解式动作生成范式**。其核心思想源自扩散模型与能量模型之间的内在联系——扩散模型的去噪网络输出可解释为能量函数的梯度（$\epsilon_\theta(x,t) \propto \nabla_x E_\theta(x)$）。基于这一洞见，DEMOGEN 将每个动作概念建模为一个独立的能量函数，并通过**组合训练**使模型自主发现动作中的概念级分解，而无需分解动作真值。

具体而言，DEMOGEN 将整体动作分解为 $K$ 个语义可解释的运动概念，并通过两种互补的方式聚合这些概念的能量分布：

- **潜变量感知 EBM**：对 $K$ 个概念分别通过去噪网络预测噪声，取平均后作为整体噪声预测，训练目标为 $\mathcal{L}_{\mathrm{MSE}} = \Vert \epsilon - \frac{1}{K} \sum_{k=1}^{K} \epsilon_{\theta}(z_t, c_k, t) \Vert^{2}$。
- **语义感知 EBM**：通过**分解式交叉注意力**（Decompositional Cross-Attention, DCA）将标准交叉注意力拆分为 $K$ 个并行分支，每个分支以不同概念的键值对计算注意力后聚合输出，即 $\mathrm{DCA}(z_t, C) = \frac{1}{K} \sum_{k=1}^{K} \mathrm{CA}(z_t, c_k)$。

为获得分解概念嵌入 $C = \{c_k\}_{k=1}^K$，DEMOGEN 探索了三种监督策略：**显式监督**（EXP，使用分解文本标注）、**正交自监督**（OSS，通过文本嵌入分区与正交损失 $\mathcal{L}_{\mathrm{Ortho}}$ 促进解耦）和**语义一致性监督**（SC，在 OSS 基础上增加语义对齐损失 $\mathcal{L}_{\mathrm{SC}}$）。

### 方法谱系与知识库定位

DEMOGEN 在方法谱系中处于**扩散模型**与**能量模型**的交叉地带，同时与**组合式生成**和**解耦表示学习**两条研究脉络深度关联。

在扩散模型脉络中，DEMOGEN 以**SALAD**（骨架感知潜在扩散）为骨干架构，继承了其 VAE 编码器-解码器框架和潜在空间扩散机制，但在去噪过程的核心建模方式上做出了根本性改变：将单一整体能量分数替换为 $K$ 个概念能量分数的平均聚合（潜变量感知）或 $K$ 路并行交叉注意力聚合（语义感知）。这一设计与**EnergyMoGen**（Zhang et al., CVPR 2025）共享能量组合的思想基础，但 DEMOGEN 的创新在于将组合机制**内化到训练范式**中，使模型在训练阶段即学习概念级分解，而非仅在推理时施加外部组合约束。

在解耦表示学习脉络中，DEMOGEN 的正交损失和语义一致性损失借鉴了变分自编码器中 $\beta$-VAE 等工作的解耦思想，但将其适配到扩散模型的能量组合框架中。与**STMC**（Petrovich et al., CVPRW 2024）的多轨时间线组合控制相比，DEMOGEN 不依赖预定义的时间线结构，而是通过能量聚合实现更灵活的概念组合。

### 主要结果概览

在**HumanML3D**标准基准上，DEMOGEN 的三个变体在潜变量感知和语义感知两种设置下均展现出竞争力：潜变量感知的 DEMOGEN-OSS 在 R-Precision Top-1 上达到 **0.588**，超越 SALAD 的 0.581；语义感知的 DEMOGEN-EXP 在 Top-3 上达到 **0.863**，显著优于 EnergyMoGen 的 0.815。在**MTT**基准的组合与多概念生成任务上，DEMOGEN 较先前最优方法取得了显著提升（多概念 R@1 达 14.9，组合 R@1 达 16.2）。此外，在专门构建的分解标注数据集**DeCompML**上，微调 SALAD 使 FID 降低约 21%，验证了分解训练范式的辅助价值。

### 局限与开放问题

DEMOGEN 的当前设计存在若干局限：分解概念数量 $K$ 固定为 2，无法自适应处理具有不同概念数量的复杂动作；显式监督变体依赖大语言模型标注的分解文本，对领域外动作的标注质量存疑；仅在通用人体动作数据集上验证，对专业运动、舞蹈、交互动作等场景的泛化能力尚不明确；分解质量的评估主要依赖定性可视化，缺乏定量分解质量指标。这些局限也指向了一系列开放问题，包括变长 $K$ 的自动确定、层次化分解的扩展、以及分解概念的可解释语义验证等。

### 问题背景：文本驱动的整体式动作生成

文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型在该任务上取得了显著进展，涌现出 **MDM**（Tevet et al., arXiv 2022）、**MLD**（Chen et al., arXiv 2022）、**ReMoDiffusion**（Zhang et al., arXiv 2023）等一系列代表性工作。这些方法将动作视为一个整体序列进行建模，通过单一文本嵌入条件化去噪过程，在 HumanML3D 等标准基准上取得了优异的生成质量。

### 核心瓶颈：缺乏结构化组合理解

然而，现有方法的根本局限在于**缺乏对动作内部结构化组合的理解**。人类的复杂动作本质上是由多个语义概念原语组合而成的——例如"一个人边走边挥手"可以分解为"行走"和"挥手"两个独立的概念。现有整体式建模范式将动作与文本描述之间建立一对一的映射关系，无法像人类一样推理和重组这些动作概念。这一缺陷直接限制了模型在以下场景中的表现：

- **多概念动作生成**：需要同时表达多个独立语义概念（如"边跑边跳"）
- **组合动作生成**：需要将来自不同动作的概念重新组合（如将"踢腿"与"转身"组合）
- **动作分解与编辑**：需要从已有动作中分离并替换特定概念

尽管 **EnergyMoGen**（Zhang et al., CVPR 2025）和 **STMC**（Petrovich et al., CVPRW 2024）等近期工作尝试通过多轨时间线或组合策略实现部分概念级控制，但它们仍然依赖预定义的概念边界或外部组合机制，未能从根本上让模型自主学习动作的分解结构。

### 本文动机：从能量视角实现分解式动作生成

本文的核心动机在于：**能否让扩散模型在训练过程中自主发现动作的概念级分解，而无需分解动作的真值标注？**

这一动机的可行性建立在一个关键的观察之上：扩散模型的去噪网络可以被解释为能量函数（Energy-Based Model, EBM）的梯度——即 $\epsilon_\theta(x,t) \propto \nabla_x E_\theta(x)$。基于这一对应关系，每个动作概念可以自然地表示为一个独立的能量分数，而多个概念的能量分布可以通过聚合操作（如平均）组合为整体动作的能量分布。这种**能量组合训练范式**使得模型能够在仅给定整体动作监督的条件下，学习将动作分解为多个语义可解释的概念原语。

为了验证这一范式的有效性，本文提出了 **DEMOGEN**（Decompositional Motion Generation），在三种监督粒度下探索分解式动作生成：显式分解监督（DEMOGEN-EXP）、正交自监督（DEMOGEN-OSS）和语义一致性监督（DEMOGEN-SC），从完全依赖分解标注到完全自监督，逐步验证能量组合训练在动作分解上的能力边界。

## 核心方法与创新机理

### 问题瓶颈：从整体建模到概念级分解

现有文本驱动动作生成方法（如 **MDM** (Tevet et al., arXiv 2022)、**MLD** (Chen et al., arXiv 2022)、**ReMoDiffusion** (Zhang et al., arXiv 2023)）将人体动作视为不可分割的整体序列进行建模，缺乏对动作内部结构化组合的理解。这种“整体式”范式忽略了人体动作本质上的组合性——一个复杂动作（如“边走边挥手”）可以自然地分解为多个语义概念原语（“行走”+“挥手”）的组合。当模型无法像人类一样推理和重组这些动作概念时，其在需要概念组合与迁移的场景（如多概念动作生成、动作编辑）中表现受限。

### 核心洞察：扩散模型即能量函数的组合

DEMOGEN的核心洞察建立在一个关键的理论对应关系上：扩散模型的去噪网络输出可被解释为能量函数的梯度，即 $\epsilon_\theta(x,t) \propto \nabla_x E_\theta(x)$（§3.1, Equation 2）。基于这一联系，模型对每个动作概念的建模可以转化为对相应能量函数的学习，而多个概念的组合则自然地体现为能量分布的聚合。具体而言，通过对 $K$ 个概念分别计算能量（噪声预测）并求平均，或通过将交叉注意力拆分为 $K$ 个并行分支并聚合输出，模型能够从整体动作中自主发现概念级的分解结构——**无需任何分解动作的真值标注**。

### 关键创新：Changed Slots 深度解析

#### 1. 能量建模方式：从单一整体到多概念聚合

| 维度 | 基线方法 | DEMOGEN |
|------|---------|---------|
| 能量粒度 | 单一整体能量分数（动作级别） | $K$ 个概念能量分数的平均聚合 |
| 实现方式 | 标准去噪网络单次前向 | 潜变量感知：$\frac{1}{K}\sum_{k=1}^K \epsilon_\theta(z_t, c_k, t)$ |
|  |  | 语义感知：$\frac{1}{K}\sum_{k=1}^K \text{CA}(z_t, c_k)$ |

这是 DEMOGEN 最根本的架构变更。传统扩散模型对每个动作样本仅计算一个整体能量分数，而 DEMOGEN 将能量建模提升到概念级别。在**潜变量感知 EBM**（Latent-aware EBM）中，去噪网络对每个概念 $c_k$ 独立预测噪声，$K$ 个输出取平均后作为最终噪声预测 $\epsilon_{\text{pred}}$，训练目标为：

$$\mathcal{L}_{\mathrm{MSE}} = \left\| \epsilon - \frac{1}{K} \sum_{k=1}^{K} \epsilon_{\theta}(z_t, c_k, t) \right\|^2$$

在**语义感知 EBM**（Semantic-aware EBM）中，能量函数通过交叉注意力模块参数化，提出**分解式交叉注意力**（Decompositional Cross-Attention, DCA）：

$$\mathrm{DCA}(z_t, C) = \frac{1}{K} \sum_{k=1}^{K} \mathrm{CA}(z_t, c_k)$$

DCA 将标准交叉注意力拆分为 $K$ 个并行分支，每个分支使用不同概念的键值对计算注意力，最后平均聚合所有输出。这种设计强制模型在注意力层面进行概念级因式分解。

#### 2. 文本监督粒度：三种分解监督策略

DEMOGEN 探索了从显式监督到完全自监督的三种文本分解策略，覆盖不同的标注可用性场景：

- **DEMOGEN-EXP（显式监督）**：直接使用分解文本描述 $C = C^P$，明确指示整体动作与分解文本之间的对应关系。依赖 DeCompML 数据集提供的分解标注。
- **DEMOGEN-OSS（正交自监督）**：将整体文本嵌入分割为 $K$ 段，通过正交损失 $\mathcal{L}_{\mathrm{Ortho}}$ 促进各段之间的正交性，鼓励概念解耦，无需分解文本标注。
- **DEMOGEN-SC（语义一致性监督）**：在 OSS 基础上引入两层 Transformer 处理分割后的嵌入段，通过语义一致性损失 $\mathcal{L}_{\mathrm{SC}}$ 对齐分区嵌入与分解文本嵌入，在无显式标注的情况下提升分解的语义可解释性。

三种策略共享一个关键的**文本混合训练机制**：在每个训练批次中，$\tau \times 100\%$ 的样本使用原始整体文本描述训练（$\tau=0.7$），有效解决了纯分解文本训练可能导致的文本-动作映射不准确问题。

#### 3. 辅助损失函数：正交与语义一致性约束

DEMOGEN 的训练目标在标准 MSE 损失基础上引入了两项关键正则化：

- **正交损失** $\mathcal{L}_{\mathrm{Ortho}}$：通过约束文本嵌入分割段之间的正交性（$\|\hat{\mathbf{Z}}_l \hat{\mathbf{Z}}_l^\top - \mathbf{I}_K\|_F^2$），避免不同概念嵌入的信息重叠，是 OSS 和 SC 变体实现无监督分解的核心机制。
- **语义一致性损失** $\mathcal{L}_{\mathrm{SC}}$（仅 SC 变体）：对齐分区嵌入段与两层 Transformer 输出的分解文本嵌入，增强分解概念的语义可解释性。

总损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{MSE}} + \alpha_o \mathcal{L}_{\mathrm{Ortho}} + \alpha_{sc} \mathcal{L}_{\mathrm{SC}}$$

其中 $\alpha_o$ 在潜变量感知训练中设为 2.0，语义感知训练中设为 1.0；$\alpha_{sc}$ 统一设为 1.0。消融实验（§4.5, DeCompML）验证了两项损失均有效提升了分解质量。

### 方法谱系与知识库定位

DEMOGEN 处于**文本驱动人体动作生成**与**基于能量的组合建模**的交叉点。其直接技术继承包括：

- **扩散动作生成骨干**：基于 **SALAD** 的骨架感知潜在扩散架构（VAE 编码器-解码器 + 潜在空间扩散），继承了其在 HumanML3D 上的强基线性能（FID 0.076）。
- **能量组合范式**：受 **EnergyMoGen**（Zhang et al., CVPR 2025）启发，但将其从动作级别的能量组合推进到概念级别的分解式能量建模。EnergyMoGen 对整体动作进行组合，而 DEMOGEN 在动作内部进行概念原语的分解与重组。
- **多轨时间线控制**：与 **STMC**（Petrovich et al., CVPRW 2024）的多概念生成任务形成对比——STMC 依赖显式的时间线标注，而 DEMOGEN 通过能量组合隐式学习概念分解。

DEMOGEN 的独特贡献在于：**首次将扩散模型的能量函数视角与动作概念分解相结合**，通过组合训练范式在无需分解真值的情况下实现了概念级动作理解，填补了整体式动作生成与组合式动作推理之间的方法空白。

### 需要人工验证的要点

1. **DCA 的计算开销**：论文未提供 DCA（$K$ 路并行交叉注意力）与标准交叉注意力的计算复杂度对比。当 $K>2$ 时，注意力计算的线性增长是否构成实际部署瓶颈，需查阅补充材料或进行实测验证。
2. **K=2 的泛化性**：当前所有实验固定 $K=2$，对于包含三个及以上独立概念的动作（如“边走边挥手边转头”），模型能否通过两个概念的组合隐式表达更复杂的语义，尚缺乏定量分析。
3. **DeCompML 标注质量**：显式监督变体依赖 GPT-4.1 自动标注的分解文本，其标注可靠性缺乏人工评估的量化报告，可能影响 DEMOGEN-EXP 结果的可复现性。

DEMOGEN 的核心思想是将人体动作生成重新表述为**组合式能量建模**问题：将整体动作分解为 $K$ 个语义可解释的动作概念，每个概念对应一个独立的能量函数，通过对 $K$ 个能量分布进行聚合来引导扩散模型的去噪过程。

### 方法总览

整个框架由四个关键阶段构成：

1. **VAE 潜在编码**：运动编码器 $E$ 将整体动作 $x \in \mathbb{R}^{L \times d_m}$ 变分编码为潜在表示 $z$，降低扩散过程的计算维度。生成时，解码器 $D$ 将去噪后的潜在表示映射回动作空间。

2. **文本嵌入分解**：根据监督策略的不同，整体文本描述被分解为 $K$ 个概念文本嵌入 $C = \{c_k\}_{k=1}^K$。三种变体分别采用显式分解文本（DEMOGEN-EXP）、正交自监督分割（DEMOGEN-OSS）和语义一致性监督（DEMOGEN-SC）来获取概念嵌入。

3. **组合能量聚合**：这是框架的核心创新。扩散模型的去噪网络可被解释为能量函数的梯度（$\nabla_x E_\theta(x) \propto \epsilon_\theta(x)$），因此通过对 $K$ 个概念分别计算能量并聚合，即可实现组合式建模。具体提供两种实现方式：
   - **潜变量感知 EBM**：直接对 $K$ 个概念的去噪网络输出求平均，损失函数为 $\mathcal{L}_{\mathrm{MSE}} = \Vert \epsilon - \frac{1}{K} \sum_{k=1}^{K} \epsilon_\theta(z_t, c_k, t) \Vert^2$。
   - **语义感知 EBM**：通过分解式交叉注意力（DCA）实现，将标准交叉注意力拆分为 $K$ 个并行分支，每个分支以不同概念的键值对计算注意力后平均聚合：$\mathrm{DCA}(z_t, C) = \frac{1}{K} \sum_{k=1}^{K} \mathrm{CA}(z_t, c_k)$。

4. **扩散去噪与解码**：聚合后的噪声预测 $\epsilon_{\text{pred}}$ 引导反向扩散过程，逐步从纯噪声恢复潜在表示 $z_0$，再经解码器 $D$ 生成最终动作序列。

### 关键设计决策

**概念数量固定**：框架设定 $K=2$，将每个整体动作建模为两个动作概念的组合。这一选择在实验中表现良好，但也构成了方法的核心局限——无法自适应处理具有不同概念数量的复杂动作。

**文本混合训练**：为避免分解文本与动作映射不准确的问题，训练时以 $\tau=0.7$ 的比例混合使用分解文本和原始整体文本，即 70% 的样本使用分解文本训练，30% 使用原始文本。这一策略有效平衡了分解学习与整体语义保持。

**辅助损失**：根据变体不同，训练目标在 MSE 损失基础上增加正交损失 $\mathcal{L}_{\mathrm{Ortho}}$（促进文本嵌入段之间的正交性，鼓励概念解耦）和语义一致性损失 $\mathcal{L}_{\mathrm{SC}}$（对齐分区嵌入与分解文本嵌入）。正交损失权重在潜变量感知训练中设为 2.0，语义感知训练中设为 1.0。

### 输入输出流

- **训练阶段**：输入为整体动作序列 $x$ 及其文本描述（整体 + 分解），输出为训练好的去噪网络 $\epsilon_\theta$（潜变量感知）或含 DCA 的 Transformer 骨干（语义感知）。
- **推理阶段**：输入为整体文本描述或分解概念文本，模型先推理动作概念，再通过能量聚合组合生成匹配文本的整体动作序列。在无分解文本的情况下（OSS/SC 变体），模型自主发现动作概念，无需分解标注。

整体框架的设计使得 DEMOGEN 在无需分解动作真值的情况下，通过能量组合训练范式学习概念级分解，为动作生成提供了结构化的语义理解和重组能力。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Towards_Decompos/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach. We propose DEMOGEN, a compositional training paradigm that facilitates decompositional motion generation via an energy-based diffusion model. We learn to decompose the holistic motion into K concepts. The energy functions of these concepts are aggregated to form the*

### 3.1 扩散模型与能量函数的等价关系

DEMOGEN 的核心洞察在于利用扩散模型与能量模型（EBM）之间的内在联系。标准扩散模型的反向去噪步骤可表述为：

$$ \pmb { x } _ { t - 1 } = \pmb { x } _ { t } - \epsilon _ { \theta } ( \pmb { x } _ { t } , t ) + \mathcal { N } ( 0 , \tilde { \beta } _ { t } I ) \tag{1} $$

从能量函数的视角，该过程等价于对能量函数 $E_\theta(\pmb{x})$ 执行梯度下降：

$$ \pmb { x } _ { t - 1 } = \pmb { x } _ { t } - \eta \nabla _ { \pmb { x } } E _ { \theta } ( \pmb { x } ) + \mathcal { N } ( 0 , \tilde { \beta } _ { t } I ) \tag{2} $$

由此建立了关键对应关系：$\epsilon_\theta(\pmb{x}, t) \propto \nabla_{\pmb{x}} E_\theta(\pmb{x})$，即去噪网络的输出可解释为能量函数的梯度。这一关系构成了 DEMOGEN 将每个动作概念建模为独立能量分数的理论基础（§3.1）。

### 3.2 组合训练范式：双路能量聚合

DEMOGEN 的组合训练范式（Algorithm 1）将整体动作分解为 $K$ 个概念，通过对 $K$ 个能量函数进行聚合来引导去噪过程。模型首先通过 VAE 编码器 $E$ 将整体动作 $\pmb{x} \in \mathbb{R}^{L \times d_m}$ 变分编码为潜在表示 $z$，在潜在空间中执行扩散与去噪，最后通过解码器 $D$ 映射回动作空间。能量聚合通过两种互补机制实现（§3.2）：

**潜变量感知 EBM（Latent-aware EBM）** 直接通过去噪网络 $\epsilon_\theta$ 对每个概念 $c_k$ 预测噪声，并对 $K$ 个输出取平均作为最终噪声预测，训练目标为：

$$ \mathcal { L } _ { \mathrm { M S E } } = \Vert \epsilon - \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \epsilon _ { \theta } ( z _ { t } , c _ { k } , t ) \Vert ^ { 2 } \tag{3} $$

该损失函数强制去噪网络捕获 $K$ 个概念能量分布的组合，使每个 $c_k$ 对应独立的噪声预测分支。

**语义感知 EBM（Semantic-aware EBM）** 通过交叉注意力模块参数化能量函数，提出分解式交叉注意力（Decompositional Cross-Attention, DCA）：

$$ \mathrm { D C A } ( z _ { t } , C ) = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \mathrm { C A } ( z _ { t } , c _ { k } ) \tag{4} $$

DCA 将标准交叉注意力拆分为 $K$ 个并行分支，每个分支以不同概念嵌入 $c_k$ 对应的键值对计算注意力，最后平均聚合所有输出。与潜变量感知 EBM 不同，语义感知 EBM 在注意力层面实现概念级分解，使不同概念在特征空间中显式分离。

两种 EBM 机制可独立或联合使用，对应不同的监督策略变体。

### 3.3 三种监督策略与文本处理

针对概念嵌入 $C = \{c_k\}_{k=1}^K$ 的获取方式，DEMOGEN 提出三种监督策略（§3.3-3.4）：

- **DEMOGEN-EXP（显式监督）**：直接使用分解文本标注 $C = C^P$，其中 $C^P$ 为人工或 LLM 标注的分解文本嵌入。该变体依赖 DeCompML 数据集提供的分解标注。

- **DEMOGEN-OSS（正交自监督）**：将整体文本嵌入分割为 $K$ 段，通过文本嵌入分区器获得初始概念嵌入，并引入正交损失促进各段之间的解耦：

$$ \mathcal { L } _ { \mathrm { O r t h o } } = \mathbb { E } _ { l \sim L _ { c } } \Big [ \frac { 1 } { K ^ { 2 } } \big \| \hat { \mathbf { Z } } _ { l } \hat { \mathbf { Z } } _ { l } ^ { \top } - \mathbf { I } _ { K } \big \| _ { F } ^ { 2 } \Big ] \tag{5} $$

训练目标为 $\mathcal{L} = \mathcal{L}_{\mathrm{MSE}} + \alpha_o \mathcal{L}_{\mathrm{Ortho}}$，其中 $\alpha_o$ 在潜变量感知训练中设为 2.0，语义感知训练中设为 1.0。

- **DEMOGEN-SC（语义一致性监督）**：在 OSS 基础上增加两层 Transformer 处理分割后的文本嵌入段，并引入语义一致性损失 $\mathcal{L}_{\mathrm{SC}}$ 对齐分区嵌入段与分解文本嵌入，训练目标为 $\mathcal{L} = \mathcal{L}_{\mathrm{MSE}} + \alpha_{sc} \mathcal{L}_{\mathrm{SC}} + \alpha_o \mathcal{L}_{\mathrm{Ortho}}$，其中 $\alpha_{sc} = 1.0$。

### 3.4 文本混合策略

为解决分解文本与原始文本之间的映射不准确问题，DEMOGEN 采用文本混合策略：在每个训练批次中，$\tau \times 100\%$ 的动作样本使用原始整体文本描述训练，其余使用分解文本。实验确定 $\tau = 0.7$ 为最优设置（§3.3, §4.2）。这一策略有效平衡了分解能力与文本-动作对齐精度。

### 3.5 关键配置参数

- **概念数量**：$K = 2$，每个整体动作建模为两个运动概念的组合（§4.2）。
- **正交损失权重**：潜变量感知训练 $\alpha_o = 2.0$，语义感知训练 $\alpha_o = 1.0$（§4.2）。
- **语义一致性损失权重**：$\alpha_{sc} = 1.0$（§4.2）。
- **文本替换率**：$\tau = 0.7$（§4.2）。

## 实验与关键发现

### 核心实验设置

DEMOGEN基于骨架感知潜在扩散模型**SALAD**的骨干架构，在**HumanML3D**和**MTT**两个标准基准上进行评估。所有指标均采用Guo等人提供的预训练评估模型计算，评估协议与先前工作保持一致。实验涵盖三种监督变体：**DEMOGEN-EXP**（显式分解文本监督）、**DEMOGEN-OSS**（正交自监督）和**DEMOGEN-SC**（语义一致性监督），每种变体均支持潜变量感知和语义感知两种能量建模方式。关键超参数配置为：分解概念数$K=2$，文本混合率$\tau=0.7$（70%样本使用分解文本训练，30%使用原始整体文本），正交损失权重$\alpha_o$在潜变量感知训练中设为2.0、语义感知训练中设为1.0，语义一致性损失权重$\alpha_{sc}$设为1.0。所有结果以三次运行的平均值±标准差报告。

### 文本到动作生成主结果

Table 1（见插图）展示了在HumanML3D测试集上与SOTA扩散模型的定量对比。**潜变量感知设置下**，DEMOGEN-OSS取得最优R-Precision Top-1 **0.588**（vs SALAD 0.581）和Top-2 **0.778**，同时FID **0.078**接近SALAD的最优值0.076，表明分解训练在提升文本-动作匹配精度的同时未牺牲生成质量。**语义感知设置下**，DEMOGEN-EXP取得最优R-Precision Top-3 **0.863**（vs EnergyMoGen 0.815，提升+0.048）和最优MM-Dist **2.623**（vs SALAD 2.649），验证了分解式交叉注意力（DCA）在语义对齐上的显著优势。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Towards_Decompos/figures/003_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art diffusion models on the test set of HumanML3D [18]. We quantitatively evaluate our approach across three variants under both latent-aware and semantic-aware settings. All metrics are obtained via a pretrained evaluation model from Guo et al. [18]. Bold and underlined denote the best and second-best results, respectively*

值得注意的是，三种变体在R-Precision指标上一致超越各自基线，这一跨设置的一致性提升构成了分解训练范式有效性的**强证据**——无论是通过去噪网络输出平均（潜变量感知EBM，公式3）还是通过DCA聚合（语义感知EBM，公式4），将动作建模为K个概念能量的组合均能增强模型对文本语义的细粒度理解。

### 多概念与组合动作生成

Table 2（见插图）展示了在MTT基准上的组合与多概念生成结果。在**多概念生成**任务上，DEMOGEN-OSSt（潜变量感知）取得R@1 **14.9**、R@3 **29.5**，显著优于先前最优方法。在**组合生成**任务上，DEMOGEN-Expt（潜变量感知）取得R@1 **16.2**、R@3 **31.9**，同样大幅领先。这一结果表明：显式分解监督（DEMOGEN-EXP）在需要精确概念重组的组合生成场景中更具优势，而正交自监督（DEMOGEN-OSS）在无需分解标注的多概念生成中表现最佳——两种变体形成了互补的能力分布。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Towards_Decompos/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on MTT [46]. The metrics are computed following STMC [46] and EnergyMoGen (EMG) [71]. † indicates the latent-aware setting. The results of the semanticaware model are provided in the supplementary material*

### 分解标注数据的辅助训练价值

Table 3和Table 4（见插图）展示了在DeCompML数据集（扩展的HumanML3D，包含分解文本标注）上的评估结果。在DeCompML上微调SALAD使FID降低约**21%**（Table 4），验证了分解标注数据对生成质量的显著提升作用。同时，消融实验证实$\mathcal{L}_{SC}$（语义一致性损失）和$\mathcal{L}_{Ortho}$（正交损失）两个损失项均有效提升了分解质量，为自监督变体的设计提供了消融支撑。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Towards_Decompos/figures/008_Table_4.jpg]]
*Table 4: Text-to-motion evaluation on extended HumanML3D. ∗ indicates the finetuned model. Additional metrics and results of other methods are provided in the supplementary material*

### 定性分析

Figure 3（见插图）展示了文本到动作生成中的分解理解能力：在仅给定整体文本描述（如"a person walks forward then sits down"）时，模型首先推理出运动概念（如"walk forward"和"sit down"），再组合生成与文本匹配的整体动作序列。DEMOGEN-OSS和DEMOGEN-SC在**无分解文本辅助**的条件下自主发现了运动概念，证明了能量组合训练范式能够从整体动作中涌现概念级分解能力。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Towards_Decompos/figures/004_Figure_3.jpg]]
*Figure 3: Text-to-motion generation with decompositional understanding. Given a complete textual description (in italics above the result), our approach first infers the motion concepts and further composes them to synthesize the holistic motion that matches the text. Notably, DEMOGEN-OSS and DEMOGEN-SC discover motion concepts without the aid of decomposed text. However, for clarity, we manually annotate each concept in bold. More visual results can be found on the project page*

Figure 4（见插图）进一步展示了动作分解与重组能力：模型在不同分解文本提示下从同一复杂动作序列中推理出多样化的运动概念，并能将推理概念与其他概念重组生成新颖动作，体现了分解结构在运动编辑和生成多样性方面的实用价值。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Towards_Decompos/figures/005_Figure_4.jpg]]
*Figure 4: Motion decomposition and recombination. We demonstrate that our method can infer diverse motion concepts from a complex motion sequence, conditioned on different decompositional text prompts. Our approach also exhibits the ability to recombine the inferred concepts with others to generate novel motions*

### 失败模式与局限性

尽管DEMOGEN在多个基准上取得了显著提升，仍存在以下局限需要关注：

1. **固定K值的限制**：分解概念数$K=2$是固定预设的，无法自适应处理具有不同概念数量的复杂动作。对于包含三个及以上独立语义概念的动作（如"边走边挥手同时转头"），双概念分解可能不足以捕获完整的语义结构。如何实现变长K的自适应分解仍是一个开放问题。

2. **显式监督变体的标注依赖**：DEMOGEN-EXP依赖DeCompML数据集的分解文本标注，该标注通过GPT-4.1等大语言模型自动生成。对于领域外动作类型（如专业体育动作、舞蹈编排），自动标注的质量可能不足，限制了显式监督变体的泛化范围。标注可靠性的量化评估目前缺失。

3. **泛化范围有限**：当前验证仅限于HumanML3D和MTT两个通用人体动作数据集，对更广泛运动类型（如双人交互、物体操控、四足动物运动）的泛化能力尚不明确。

4. **分解质量缺乏定量指标**：分解效果的评估主要依赖定性可视化（Figure 3、Figure 4），缺少定量分解质量指标（如概念分离度、重组一致性、概念可解释性评分等），使得不同变体间的分解能力难以进行严格的量化比较。

5. **计算开销未讨论**：DCA的K路并行注意力机制相比标准交叉注意力引入了额外的计算开销，特别是在$K>2$时开销随K线性增长。论文未提供推理延迟或显存占用的对比数据，实际部署效率需要进一步评估。

## 定位与知识库关联

### 1. 方法沿革与基线关系

DEMOGEN 的核心贡献在于将**组合式能量建模**引入人体动作生成，其方法谱系可沿三条主线追溯：扩散动作生成、基于能量的组合建模、以及动作分解表示。

**扩散动作生成基线。** 在文本到动作生成领域，扩散模型已成为主流范式。**MDM** (Tevet et al., arXiv 2022) 率先将扩散模型应用于动作生成，直接在原始动作空间进行去噪；**MLD** (Chen et al., arXiv 2022) 引入潜在扩散以降低计算开销；**ReMoDiffusion** (Zhang et al., arXiv 2023) 通过检索增强机制提升文本-动作对齐精度；**FineMoGen** (Zhang et al., NeurIPS 2023) 则聚焦于细粒度时空生成与编辑。DEMOGEN 选择 **SALAD**（骨架感知潜在扩散模型）作为骨干架构，在潜在空间中构建组合训练范式，而非从头设计新的扩散架构——这一选择使其能够将能量组合机制与现有高效潜在扩散模型解耦，便于方法迁移。

**基于能量的组合建模。** 与 DEMOGEN 最直接相关的前驱工作是 **EnergyMoGen** (Zhang et al., CVPR 2025)，该工作首次将扩散模型与能量模型（EBM）的对应关系引入动作生成，但 EnergyMoGen 的能量函数作用于**整体动作级别**，不涉及动作内部的概念分解。DEMOGEN 的关键突破在于将单一整体能量分布替换为 **K 个概念能量函数的平均聚合**，从而将组合性从“动作间拼接”下沉到“动作内分解”。这一范式转变使模型能够自主发现动作的语义原语，而无需分解动作真值。

**多轨组合控制基线。** **STMC (Multi-Track Timeline)** (Petrovich et al., CVPRW 2024) 通过多轨时间线实现组合控制，但其组合发生在时间轴层面，需要显式的时间分割边界。DEMOGEN 的组合则发生在**语义概念层面**，不依赖时间分割，且支持无监督的概念发现（OSS/SC 变体）。

### 2. 关键设计决策与适用边界

DEMOGEN 的方法设计包含三个关键决策，各自划定了适用边界：

**固定概念数 K=2。** 当前实现将每个整体动作建模为恰好两个概念的能量聚合（§4.2）。这一简化假设使训练稳定且分解可解释，但限制了模型处理具有更多语义原语的复杂动作（如“边跑边挥手边跳跃”）的能力。对于概念数未知或变长的动作类型，该方法需要人工预设 K 值，无法自适应调整。

**三种监督策略的梯度覆盖。** DEMOGEN 提供了从强到弱的监督谱系：EXP（显式分解文本监督）→ SC（语义一致性自监督）→ OSS（正交自监督）。EXP 需要分解文本标注（依赖 LLM 辅助构建的 DeCompML 数据集），在领域外动作类型上标注质量可能不足；OSS 完全不依赖分解标注，但分解语义的可解释性依赖于正交损失的隐式正则化，可能产生语义模糊的概念划分。

**能量聚合的两种实现路径。** 潜变量感知 EBM（通过去噪网络输出平均）和语义感知 EBM（通过分解式交叉注意力 DCA）提供了不同的建模粒度。潜变量感知路径计算开销更低，但概念间的交互仅通过损失函数间接发生；语义感知路径通过 K 路并行注意力显式建模概念与动作特征的对应关系，但 DCA 的计算开销随 K 线性增长（§3.2 Equation 4），且当 K>2 时，并行分支的内存占用可能成为瓶颈。

### 3. 局限与开放问题

**计算可扩展性。** 当前 K=2 的设置下，DCA 的 K 路并行注意力开销尚可接受，但论文未报告 K 增大时的计算开销曲线。对于需要细粒度分解的应用场景（如 K=5 或 10），DCA 的线性增长是否仍可接受，以及是否存在更高效的实现（如分组注意力或低秩近似），是实际部署前需要回答的问题。

**分解质量的量化评估。** 论文对分解效果的评估主要依赖定性可视化（Figure 3、Figure 4），缺乏定量分解质量指标。概念分离度（如不同概念嵌入的互信息）、重组一致性（如分解-重组后的动作与原始动作的相似度）等指标尚未建立。这使得不同监督策略（EXP/OSS/SC）之间的分解质量对比缺乏客观尺度，该点需要手动验证。

**泛化边界。** 所有实验均在 HumanML3D 和 MTT 两个通用人体动作数据集上进行。对于专业运动（如体操、武术套路）、双人交互动作（如双人舞、搏击）、以及非人体运动域（如四足动物、群体行为），该方法的概念分解假设是否仍然成立，尚不明确。DeCompML 数据集的分解文本由 GPT-4.1 自动标注，其标注可靠性缺乏量化评估，可能引入系统性偏差。

**层次化分解的可能性。** 当前方法仅支持一级分解（整体动作→K 个概念），但人类动作天然具有层次结构（整体动作→子动作→关节级原语）。能否将能量组合范式扩展为层次化能量聚合（如递归地将每个概念进一步分解为子概念），以实现更细粒度的运动理解和编辑，是一个值得探索的方向。

**概念嵌入的语义可解释性。** 虽然论文展示了分解概念的可视化结果，但分解后的概念嵌入是否具有稳定的语义含义（如可通过文本检索验证概念对应关系），以及能否支持零样本概念迁移（将从一个动作类型学到的概念原语组合到全新动作类型中），仍有待研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Decompositional_Human_Motion_Generation_with_Energy_Based_Diffusion_Models.pdf]]

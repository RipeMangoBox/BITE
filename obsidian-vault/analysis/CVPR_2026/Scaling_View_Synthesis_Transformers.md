---
title: Scaling View Synthesis Transformers
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scaling_View_Synthesis_Transformers.pdf
project_link: "https://www.evn.kim/research/svsm"
code_link: null
aliases:
- SVSMS
- SVST
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "有效批量大小 $B_{\\mathrm{eff}} = B \\cdot V_T$ 决定了训练性能和计算最优折衷，而非单独的 $B$ 或 $V_T$。"
primary_logic: 通过定义有效批量大小并采用相对相机注意力(PRoPE)，Encoder-Decoder架构可达到与Decoder-only相同的可扩展性，同时显著节省训练和推理计算。
claims:
- SVSM的Pareto前沿比LVSM左移3倍，在相同性能下所需训练计算量仅1/3。
- 相同有效批量大小的不同B与V_T组合产生几乎相同的测试PSNR和训练损失。
- 引入PRoPE相对相机注意力后，SVSM在多视图(V_C>2)设置中恢复了与LVSM等同的缩放趋势。
- PRoPE消融表明相对嵌入是关键，而非对极几何或额外位姿信息流。
---

# Scaling View Synthesis Transformers

> [!tip] 核心洞察
> 通过定义有效批量大小并采用相对相机注意力(PRoPE)，Encoder-Decoder架构可达到与Decoder-only相同的可扩展性，同时显著节省训练和推理计算。

| 字段 | 内容 |
|------|------|
| 中文题名 | 缩放视图合成Transformer |
| 英文题名 | Scaling View Synthesis Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21341) · [Project](https://www.evn.kim/research/svsm) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Scalable View Synthesis Model (SVSM) |
| Dataset | RealEstate10K, DL3DV, RealEstate10K (V_C=2) 缩放Pareto, DL3DV (V_C=4) 缩放Pareto |

> [!tip] 效果简介
> - RealEstate10K (V_C=2) 上，PSNR / SSIM / LPIPS 30.01 / 0.910 / 0.096 (SVSM 416M, Pareto-optimal) vs 29.67 / 0.906 / 0.098 (LVSM decoder-only 171M) (+0.34 PSNR, -0.002 LPIPS, 且使用约一半训练FLOPs)；PSNR (对比先前SOTA) 30.01 vs 28.10 (GS-LRM) (+1.91 PSNR)。
> - DL3DV (V_C=4) 上，PSNR / SSIM / LPIPS 26.87 / 0.853 / 0.129 (SVSM 400M, Pareto-optimal) vs 26.19 / 0.830 / 0.145 (LVSM decoder-only + PRoPE 171M) (+0.68 PSNR, -0.016 LPIPS)。
> - RealEstate10K (V_C=2) 缩放Pareto 上，训练计算量-性能Pareto前沿 SVSM前沿左移约3x vs LVSM前沿 (相同性能下训练计算量减少约3倍)。

## 概要

视图合成（Novel View Synthesis）旨在从稀疏的上下文图像中渲染新视角场景。近年来，基于Transformer的通用视图合成模型——如**LVSM**（Large View Synthesis Model）——取得了显著进展，但其decoder-only架构存在根本性效率瓶颈：每个目标视图都需要重新处理全部上下文视图，导致计算量随目标视图数 $V_T$ 和上下文视图数 $V_C$ 呈 $V_T(V_C+1)$ 增长。这使得模型在缩放训练和推理时面临严重的计算效率问题。

本文提出**可缩放视图合成模型（SVSM）**，核心思想是通过**encoder-decoder架构**实现场景表征的一次编码、多次解码，将计算复杂度从 $V_T(V_C+1)$ 降至 $V_T+V_C$。在此基础上，作者揭示了视图合成Transformer缩放的一个关键因果机制：**有效批量大小** $B_{\mathrm{eff}} = B \cdot V_T$ 决定了训练性能和计算最优折衷，而非单独的 $B$ 或 $V_T$。利用这一发现，SVSM可通过增大 $V_T$ 并减小 $B$ 来显著降低训练计算量，同时保持相同性能。

为应对多视图（$V_C > 2$）场景中位姿信息在encoder-decoder瓶颈中的丢失问题，SVSM引入**PRoPE（Projected Rotary Position Embedding）**——一种相对相机旋转位置编码，在编码器和解码器的注意力层中将特征规范化至目标坐标系，确保位姿信息在深层网络中得以保持。

**核心结论：**
- **计算效率提升约3倍**：在RealEstate10K数据集上，SVSM的Pareto前沿相比LVSM左移约3倍，相同性能下所需训练计算量仅1/3。
- **有效批量假设验证**：相同 $B_{\mathrm{eff}}$ 下，不同 $(B, V_T)$ 组合的测试PSNR差异仅±0.2，训练损失几乎重合。
- **多视图缩放恢复**：引入PRoPE后，SVSM在 $V_C=4$ 的DL3DV数据集上恢复与LVSM等同的缩放趋势，且Pareto前沿更优（+0.68 PSNR，推理速度快4倍）。
- **PRoPE消融证实**：相对嵌入是关键，对极几何或额外位姿信息流非必需。

SVSM在RealEstate10K和DL3DV上均取得新SOTA，且推理速度显著优于LVSM，为视图合成Transformer的高效缩放提供了新范式。



### 问题背景：视图合成中的计算瓶颈

新视图合成（Novel View Synthesis, NVS）的目标是从一组已知相机姿态的上下文图像 $\mathfrak{C}$ 中，渲染出任意目标视角下的场景外观：

$$\tilde{I}_T = \mathrm{Render}[\mathfrak{C}, g_T, K_T]$$

其中 $g_T$ 为目标相机位姿，$K_T$ 为目标相机内参。近年来，基于Transformer的纯学习式视图合成方法——尤其是大规模视图合成模型（Large View Synthesis Model, LVSM）——展现出强大的泛化能力和缩放潜力，成为该领域的前沿范式。

然而，现有SOTA的LVSM采用**decoder-only架构**：将全部上下文视图与目标视图配置一并输入一个双向自注意力的ViT解码器，逐目标地渲染每个新视图。这一设计带来了根本性的计算效率问题：

1. **每目标重复编码**：每个目标视图都需要重新处理全部上下文视图，MLP计算量与 $V_T(V_C+1)$ 成正比，注意力计算量更与 $V_T(V_C+1)^2$ 成正比（$V_T$ 为目标视图数，$V_C$ 为上下文视图数）。当需要渲染多个目标视图时，计算开销随目标数量线性甚至超线性增长。
2. **缺乏对有效批量的理解**：训练时，模型同时处理多个场景（批量大小 $B$）和每个场景的多个目标视图（$V_T$），但此前工作未系统分析这两者如何共同影响训练效率和模型性能，导致训练资源配置缺乏理论指导。

### 现有方法缺口

LVSM decoder-only架构虽然在双目重建（$V_C=2$）上达到了领先性能，但其计算效率瓶颈限制了进一步缩放：

- **推理效率低下**：对于需要渲染多个目标视图的应用场景（如视频生成、自由视点导航），decoder-only模型必须为每个目标视图重新计算全部上下文，无法复用场景信息。
- **训练计算浪费**：由于缺乏对 $B$ 与 $V_T$ 关系的理解，训练时无法通过调整批量构成来优化计算-性能折衷。LVSM的训练计算量 $\chi^{\mathrm{(LVSM)}} \propto B_{\mathrm{eff}}(V_C+1)$，其中有效批量 $B_{\mathrm{eff}} \equiv B \cdot V_T$。这意味着在固定 $B_{\mathrm{eff}}$ 的前提下，单纯增大 $V_T$ 并不能节省训练计算——这是decoder-only架构的固有缺陷。
- **缩放行为不明**：视图合成Transformer的缩放定律此前未被系统研究，模型大小、数据量、计算预算之间的最优关系缺乏定量刻画。

### 本文动机与核心洞察

本文的核心动机是**在不牺牲缩放能力的前提下，从根本上提升视图合成Transformer的计算效率**。作者提出的关键洞察是：

> 通过将架构从decoder-only转变为**encoder-decoder**，并定义**有效批量大小** $B_{\mathrm{eff}} = B \cdot V_T$ 作为训练性能的决定性变量，可以在保持相同缩放趋势的同时，将Pareto前沿的计算成本降低约3倍。

具体而言，encoder-decoder架构（SVSM）将场景编码与目标解码解耦：
- **编码器**：一次性处理全部上下文视图，通过双向自注意力生成场景表征（一组图像块token集合），无需固定大小的瓶颈。
- **解码器**：通过交叉注意力从场景表征中单向提取信息，并行渲染多个目标视图。

这一设计使得SVSM的训练计算量变为 $\chi^{\mathrm{(SVSM)}} \propto B_{\mathrm{eff}} + B V_C$。与LVSM的关键区别在于：**SVSM可以通过增大 $V_T$ 并减小 $B$ 来降低总训练计算量，同时保持 $B_{\mathrm{eff}}$ 和模型性能不变**。这一“计算最优折衷”策略是LVSM decoder-only架构无法实现的。

此外，针对多视图场景（$V_C > 2$），本文进一步引入**PRoPE（Projected Rotary Position Embedding）相对相机注意力机制**，通过在注意力计算前将特征规范化到目标坐标系，确保相机位姿信息在深层编码器-解码器瓶颈中不丢失，从而使SVSM在多视图设置中恢复与LVSM等同的缩放能力。

Figure 1 直观展示了核心动机的实现结果：在RealEstate10K数据集上，SVSM的Pareto前沿相比LVSM左移约3倍——即在相同渲染质量下，所需训练计算量仅为原来的1/3，同时保持几乎相同的缩放曲线斜率与曲率。



## 核心方法与创新机理

本文的核心创新并非引入全新的网络模块，而是通过**架构范式转换**（decoder-only → encoder-decoder）与**训练效率认知**（有效批量大小）的协同，在保持缩放能力的前提下大幅降低视图合成Transformer的计算成本。以下从三个递进的维度剖析其创新机理。

### 架构范式转换：从重复编码到一次编码、并行解码

当前视图合成Transformer的SOTA架构LVSM采用**decoder-only**设计：所有上下文视图与目标视图的token被拼接后送入统一的双向自注意力模块。其根本缺陷在于，每渲染一个目标视图，模型必须重新处理全部上下文视图token——这形成了一个“无持久场景表征”的计算瓶颈。

SVSM将架构重构为**encoder-decoder**范式（Figure 2）：
- **编码器**对上下文视图集执行一次双向自注意力，输出一组图像块token作为**场景隐表征**；
- **解码器**以目标相机配置为查询，通过交叉注意力从场景表征中单向提取信息，实现**多个目标视图的并行渲染**。

这一转换带来了计算复杂度的结构性变化。设 $V_C$ 为上下文视图数，$V_T$ 为目标视图数，LVSM的MLP与注意力FLOPs分别与 $V_T(V_C+1)$ 和 $V_T(V_C+1)^2$ 成正比；而SVSM的对应复杂度降至 $V_T + V_C$（MLP）与 $V_C(V_T+V_C)$（注意力）。在MLP主导的计算区域（本文设置下MLP FLOPs约为注意力的4倍），SVSM实现了从 $O(V_T V_C)$ 到 $O(V_T+V_C)$ 的降阶。

### 有效批量大小：训练效率的“因果旋钮”

架构转换带来的计算节省本身并不保证性能优势——若简单将节省的算力用于增大模型或数据量，缩放行为可能劣化。本文的关键洞察在于识别出训练效率的**因果旋钮**：有效批量大小 $B_{\mathrm{eff}} \equiv B \cdot V_T$。

实验证据（Figure 3）表明，在相同 $B_{\mathrm{eff}}$ 下，不同 $(B, V_T)$ 组合的训练损失曲线和测试PSNR几乎完全重合（差异≤±0.2 PSNR）。这意味着**决定训练性能的是 $B_{\mathrm{eff}}$，而非单独的 $B$ 或 $V_T$**。

这一发现直接解锁了SVSM的计算最优策略。LVSM的训练计算量 $\chi \propto B V_T (V_C+1) = B_{\mathrm{eff}} (V_C+1)$，与 $V_T$ 的选择无关——增大 $V_T$ 不会降低总计算。而SVSM的训练计算量 $\chi \propto B(V_C + V_T) = B_{\mathrm{eff}} + B V_C$，可通过**增大 $V_T$ 并减小 $B$** 来保持 $B_{\mathrm{eff}}$ 不变的同时降低 $B V_C$ 项，从而减少总训练FLOPs。这正是SVSM的Pareto前沿比LVSM左移约3倍（Figure 1）的根本原因：在相同性能下，SVSM仅需约1/3的训练计算量。

### 相对相机注意力：多视图扩展的使能器

encoder-decoder架构在双目（$V_C=2$）设置下表现优异，但在多视图（$V_C>2$）场景中，若不加特殊处理，SVSM的缩放行为会迅速饱和（Figure 7a），性能反而不及decoder-only模型。瓶颈在于：编码器输出的场景表征是**坐标系无关**的，而位姿信息在通过编码器-解码器瓶颈时逐渐丢失。

本文引入**PRoPE（Projected Rotary Position Embedding）** 相对相机注意力机制来解决此问题（Figure 6）。其核心操作是：在编码器和解码器的每次注意力计算前，利用相对相机位姿 $g_{ij} = g_i^{-1} g_j$ 将特征变换到统一坐标系，再施加旋转位置编码。这使得位姿信息在深层网络中持续保持，而非仅在输入层一次性注入。

消融实验（Table 10）揭示了PRoPE的关键组分：
- **相对嵌入是核心**：仅在解码器中应用PRoPE即可接近全加PRoPE的性能；
- **对极几何非必需**：将PRoPE替换为不依赖对极约束的GTA（Global Transformer Attention）方法，效果相当；
- **额外位姿连接无效**：在注意力层外添加位姿信息流并未带来增益。

加入PRoPE后，SVSM在多视图设置中恢复了与LVSM等同的缩放趋势，同时保持了encoder-decoder的计算效率优势（Figure 7b），在DL3DV数据集上以更低的训练FLOPs取得了26.87 PSNR，超越LVSM+PRoPE的26.19 PSNR（Table 4）。

### 辅助创新：深度稳定的残差缩放

为支持不同深度模型的公平缩放比较，SVSM在每个残差分支上乘以 $1/\sqrt{L}$（$L$ 为层数），以抑制深层网络的梯度/激活方差膨胀。该设计并非性能提升的关键来源，但保证了缩放实验中不同深度配置的训练稳定性，是缩放定律可靠拟合的技术前提。



本文提出**可缩放视图合成模型（Scalable View Synthesis Model, SVSM）**，一种面向新视图合成（Novel View Synthesis, NVS）的编码器-解码器Transformer架构。其核心设计目标是在保持与现有decoder-only方法相同缩放行为的前提下，显著降低训练和推理的计算成本。

### 问题形式化

给定一组上下文视图 $\mathfrak{C} = \{(I_i, g_i, K_i)\}_{i=1}^{V_C}$（包含图像、相机外参和内参），以及目标相机配置 $(g_T, K_T)$，视图合成的目标是渲染目标视角图像：

$$\tilde{I}_T = \mathrm{Render}[\mathfrak{C}, g_T, K_T]$$

### 架构总览

SVSM将上述渲染过程分解为两个阶段，对应Figure 2(b)所示的编码器-解码器结构：

1. **Transformer编码器（Encoder）**：接收全部上下文视图 $\mathfrak{C}$，通过双向自注意力（bidirectional self-attention）将多视图信息融合为一组图像块级别的隐式token集合 $\mathbf{z} = \mathcal{E}[\mathfrak{C}]$，作为**场景表征（scene representation）**。该表征无固定大小瓶颈，其token数量随上下文视图数线性增长。

2. **交叉注意力解码器（Cross-Attention Decoder）**：以目标相机配置为查询（query），对编码器输出的场景表征施加单向交叉注意力（unidirectional cross-attention），从中提取目标视图所需信息。解码器可**并行渲染多个目标视图** $V_T$，无需为每个新视图重新处理上下文。

### 与基线架构的关键差异

基线方法**LVSM（Large View Synthesis Model）**采用纯decoder-only设计（Figure 2a）：所有上下文视图token与目标视图token拼接后，通过标准ViT层的双向自注意力统一处理。这导致两个根本性效率瓶颈：

- **推理冗余**：每渲染一个新目标视图，必须重新对全部上下文token执行自注意力计算。
- **训练计算膨胀**：训练时MLP计算量与 $V_T(V_C+1)$ 成正比，注意力计算量与 $V_T(V_C+1)^2$ 成正比（见公式2）。

相比之下，SVSM通过将场景编码与目标解码解耦，实现了计算复杂度的结构性降低：

$$\chi_{\mathrm{MLP}}^{\mathrm{(SVSM)}} \propto V_T + V_C, \quad \chi_{\mathrm{Attn}}^{\mathrm{(SVSM)}} \propto V_C(V_T + V_C)$$

MLP计算量从乘积关系降为加和关系，注意力计算量也从二次项中剥离了 $V_T$ 的主导因子（见公式4）。这为后续通过调整有效批量大小实现计算最优折衷奠定了基础。

### 关键设计选择

- **无瓶颈场景表征**：编码器输出的token集合大小直接随 $V_C$ 缩放，避免固定大小隐变量带来的信息瓶颈（消融实验证实固定瓶颈设计的缩放效率远低于无瓶颈设计，见Figure 9b）。
- **残差缩放（$1/\sqrt{L}$）**：每个残差分支乘以 $1/\sqrt{L}$（$L$ 为层数），保证不同深度模型的训练稳定性。
- **PRoPE相对相机注意力**：在编码器和解码器的注意力层中引入投影旋转位置编码（Projected Rotary Position Embedding），利用相对相机位姿将特征规范化至统一坐标系。该模块是多视图场景（$V_C > 2$）下恢复缩放能力的关键（详见方法谱系部分）。

### 输入输出流

| 阶段 | 输入 | 输出 |
|------|------|------|
| 编码器 | $V_C$ 个上下文视图（图像块token + 相机参数嵌入） | 场景表征 $\mathbf{z}$（图像块token集合） |
| 解码器 | 场景表征 $\mathbf{z}$ + $V_T$ 个目标相机配置 | $V_T$ 个渲染视图 $\tilde{I}_T$ |

训练损失为MSE与感知损失的加权和：$\mathcal{L} = \mathbf{MSE}(I_T, \tilde{I}_T) + \lambda \cdot \mathbf{Perceptual}(I_T, \tilde{I}_T)$，其中 $\lambda = 0.5$。

### 补充图表

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/002_Figure_2.jpg]]
*Figure 2: Architectures of the current SOTA, the decoder-only LVSM [10] (a) and SVSM (ours, b). Our cross-attention based decoder enables parallel rendering of multiple target views after a single scene encoding. Each target view is decoded independently given the shared scene representation, but the cross-attention allows these independent decodings to be executed in parallel*



### 3.1 新视图合成问题的形式化

给定一组上下文视图 $\mathfrak{C} = \{(I_i, g_i, K_i)\}_{i=1}^{V_C}$，其中 $I_i$ 为图像、$g_i$ 为相机外参、$K_i$ 为内参，新视图合成任务可表述为：

$$\tilde{I}_T = \mathrm{Render}[\mathfrak{C}, g_T, K_T] \tag{1}$$

即根据上下文视图和目标相机位姿 $(g_T, K_T)$ 渲染目标视图 $\tilde{I}_T$。本文的核心问题是：**如何设计该 Render 函数的架构，使其在计算预算增长时保持最优的缩放行为？**

### 3.2 基线架构：Decoder-only LVSM 及其计算瓶颈

当前 SOTA 的 **LVSM**（Large View Synthesis Model）采用纯 decoder-only 设计——一个标准的 ViT 模块对拼接后的上下文视图和目标视图 token 施加双向自注意力。其计算复杂度为：

$$\chi_{\mathrm{MLP}}^{\mathrm{(LVSM)}} \propto V_T (V_C + 1), \qquad \chi_{\mathrm{Attn}}^{\mathrm{(LVSM)}} \propto V_T (V_C + 1)^2 \tag{2}$$

**关键瓶颈**：MLP 计算量与 $V_T(V_C+1)$ 成正比，注意力计算量更与 $(V_C+1)^2$ 成正比。这意味着每增加一个目标视图，就需要重新处理全部上下文 token，无法复用场景信息。从训练角度看，总计算量由式 (5) 给出：

$$\chi^{\mathrm{(LVSM)}} \propto B V_T (V_C+1) = B_{\mathrm{eff}} (V_C+1) \tag{5}$$

其中 $B$ 为场景批量数，$V_T$ 为每场景目标视图数。**LVSM 的训练计算量与 $V_T$ 线性耦合——增大 $V_T$ 无法节省任何计算，因为 $B_{\mathrm{eff}}(V_C+1)$ 中 $V_C+1$ 是固定因子。**

### 3.3 SVSM 架构：Encoder-Decoder 与场景表征复用

**SVSM**（Scalable View Synthesis Model）将渲染过程拆分为两个阶段：

1. **Transformer Encoder $\mathcal{E}$**：对上下文视图集 $\mathfrak{C}$ 施加双向自注意力，生成场景表征 $\mathbf{z} = \mathcal{E}[\mathfrak{C}]$——一组图像块 token 的集合，**无固定大小瓶颈**。
2. **Cross-Attention Decoder $\mathcal{D}$**：以目标相机配置为查询，通过交叉注意力从 $\mathbf{z}$ 中单向提取信息，并行渲染多个目标视图。

复杂度分析揭示了根本性差异：

$$\chi_{\mathrm{MLP}}^{\mathrm{(SVSM)}} \propto V_T + V_C, \qquad \chi_{\mathrm{Attn}}^{\mathrm{(SVSM)}} \propto V_C (V_T + V_C) \tag{4}$$

MLP 计算量仅与 $V_T+V_C$ 的**和**成正比（而非乘积），注意力计算量也仅线性依赖于 $V_T$。这带来训练计算的根本性改变：

$$\chi^{\mathrm{(SVSM)}} \propto B (V_C + V_T) = B_{\mathrm{eff}} + B V_C \tag{6}$$

**因果杠杆**：在保持 $B_{\mathrm{eff}} = B \cdot V_T$ 不变的前提下，可通过增大 $V_T$ 并减小 $B$ 来压缩 $B V_C$ 项，从而**在同等性能下降低总训练计算量**。这正是 SVSM 的 Pareto 前沿比 LVSM 左移约 3 倍的根本原因（Figure 1）。

### 3.4 有效批量大小假设

定义有效批量大小：

$$B_{\mathrm{eff}} \equiv B \cdot V_T$$

**核心发现**（Figure 3）：在相同 $B_{\mathrm{eff}}$ 下，不同的 $(B, V_T)$ 组合产生几乎相同的训练损失和测试 PSNR（差异 ≤ ±0.2 PSNR）。这意味着 **$B_{\mathrm{eff}}$ 而非单独的 $B$ 或 $V_T$ 决定了模型的统计学习效率**。该假设是 SVSM 通过调节 $V_T$ 实现计算最优折衷的理论基础。

### 3.5 PRoPE：投影旋转位置编码

在多视图场景（$V_C > 2$）中，位姿信息在 encoder-decoder 瓶颈处会逐渐丢失，导致 SVSM 的缩放趋势饱和（Figure 7a）。**PRoPE**（Projected Rotary Position Embedding）通过以下机制解决该问题：

- 利用相对相机位姿 $g_{ij} = g_i^{-1} g_j$，在每次注意力计算前将特征变换到统一的相机坐标系；
- 相对旋转嵌入作用于编码器的自注意力和解码器的交叉注意力层，确保深层仍能感知空间关系。

消融实验（Table 10）表明：**仅对解码器施加 PRoPE 即可接近全加 PRoPE 的性能**，而替换为对极几何方法（GTA）效果相当——说明**相对嵌入本身是关键，对极几何并非必需**。

### 3.6 训练稳定性：残差缩放

为支持不同深度模型的稳定训练，SVSM 在每个残差分支上乘以缩放因子 $1/\sqrt{L}$（$L$ 为层数）。该设计保证了梯度在深层网络中的方差稳定，是缩放实验中不同规模模型收敛的前提（Supplementary 10.1）。

### 3.7 损失函数

$$\mathcal{L} = \mathbf{MSE}(I_T, \tilde{I}_T) + \lambda \cdot \mathbf{Perceptual}(I_T, \tilde{I}_T)$$

其中 $\lambda = 0.5$，感知损失用于提升渲染纹理质量。

---

**公式体系小结**：SVSM 的核心创新不在于引入新的数学形式，而在于通过架构重构（encoder-decoder + 交叉注意力）改变了计算复杂度对 $V_T$ 的依赖关系——从 LVSM 的乘积耦合 $\propto V_T(V_C+1)$ 降为加法耦合 $\propto V_T + V_C$，从而释放了通过调节 $V_T$ 实现计算最优缩放的自由度。

### 补充图表

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/009_Figure_6.jpg]]
*Figure 6: Multiview PRoPE. We find that multiview projective RoPE embeddings [13, 14, 18] are critical for our model to scale with compute and data in the multiview setting*



## 实验与关键发现

### 核心缩放定律验证

本文在RealEstate10K和DL3DV两个数据集上系统验证了SVSM的缩放行为。图1展示了最核心的发现：**SVSM的Pareto前沿相比LVSM decoder-only左移约3倍**，这意味着在相同渲染质量下，SVSM所需的训练计算量仅为LVSM的约1/3。两模型的Pareto前沿具有几乎相同的斜率和曲率，表明SVSM保留了同等的缩放行为，同时实现了显著的计算效率提升。

这一计算优势的根源在于架构差异带来的训练成本公式不同。LVSM的训练计算量与有效批量大小和上下文视图数成正比：$\chi^{\mathrm{(LVSM)}} \propto B_{\mathrm{eff}}(V_C+1)$，调整$V_T$无法降低总计算量。而SVSM的训练计算量为$\chi^{\mathrm{(SVSM)}} \propto B(V_C + V_T) = B_{\mathrm{eff}} + B V_C$，通过增大$V_T$并减小$B$，可在保持有效批量大小和性能不变的同时降低总计算成本。

### 有效批量大小假设

有效批量大小$B_{\mathrm{eff}} \equiv B \cdot V_T$是本文的核心因果旋钮。图3的实验直接验证了这一假设：在相同$B_{\mathrm{eff}}$下，不同的$(B, V_T)$组合产生的训练损失曲线和测试PSNR几乎完全重合。对于$V_C=8$的设置，测试PSNR差异在±0.1以内；对于$V_C=2$，差异在±0.2以内。这一发现表明$B_{\mathrm{eff}}$是决定训练性能和计算最优折衷的关键变量，而非单独的$B$或$V_T$。

### 双目重建结果

表1展示了在RealEstate10K数据集上$V_C=2$设置下的最终结果。SVSM（416M参数，Pareto最优配置）取得了30.01 PSNR / 0.910 SSIM / 0.096 LPIPS，优于LVSM decoder-only（171M参数）的29.67 / 0.906 / 0.098，且仅使用了约一半的训练FLOPs。与先前基于显式几何的方法相比（表2），SVSM以30.01 PSNR大幅领先GS-LRM的28.10，提升达+1.91 PSNR。

### 多视图缩放与PRoPE

在多视图设置（$V_C > 2$）中，不加PRoPE的SVSM出现性能快速饱和，缩放趋势被打断（图7a）。引入PRoPE相对相机注意力后，SVSM恢复了与LVSM等同的缩放趋势，并保持了Pareto前沿的计算效率优势（图7b）。

表4展示了DL3DV数据集上$V_C=4$的最终结果。SVSM（400M参数，Pareto最优）取得26.87 PSNR / 0.853 SSIM / 0.129 LPIPS，优于LVSM decoder-only + PRoPE（171M参数）的26.19 / 0.830 / 0.145，提升+0.68 PSNR，LPIPS降低0.016。值得注意的是，SVSM的推理FPS是LVSM的约4倍（在$V_T=1$设定下测试），当$V_T$增大时加速比将更为显著。

### PRoPE消融分析

表10的消融实验揭示了PRoPE中各组件的相对重要性。仅在解码器中应用PRoPE即可接近全加PRoPE的性能，表明相对嵌入是关键因素。将PRoPE替换为基于对极几何的GTA方法效果相当，说明对极几何并非必需。额外的位姿信息跳跃连接影响微小，进一步确认相对相机旋转位置编码本身足以维持多视图缩放能力。

### 参数与数据缩放系数

表3展示了由Chinchilla缩放定律拟合得到的参数与数据缩放系数。LVSM的系数为$a=0.65, b=0.33$，呈现$a \neq b$的不对称性；而SVSM的系数为$a=0.52, b=0.47$，近似满足$a \approx b$。这一差异可能反映了两种架构在计算最优分配上的根本差异，但具体机制仍需进一步研究。

### 固定瓶颈设计的局限性

图9b展示了固定大小隐变量瓶颈场景表征的缩放实验。结果表明，固定瓶颈设计的缩放效率远低于无瓶颈设计，该架构路径的潜力有限。这验证了SVSM采用无固定大小瓶颈的编码器输出token集合作为场景表征的设计选择。

### 训练稳定性与残差缩放

为支持不同深度模型的稳定训练，SVSM引入了$1/\sqrt{L}$残差缩放机制，为每个残差分支乘以$1/\sqrt{L}$（$L$为层数）。消融实验表明该设计保证了从浅层到深层模型的训练稳定性（补充材料10.1节），但该结论置信度略低（0.85），建议结合补充材料进一步验证。

### 公平性说明

所有模型均在$256\times256$分辨率下训练，使用相同的优化器配置和学习率调度。SVSM模型实际训练FLOPs仅为LVSM基线的一半（RealEstate10K）或约75%（DL3DV），但通过缩放定律预测可在更低计算预算下匹敌或超越。训练数据集存在场景重复采样，文中承认这与标准缩放实践（单epoch训练）不同，但未观察到明显过拟合。推理FPS测试使用batch size=64以规避硬件瓶颈。

### 失败模式与局限

当前缩放定律建立在相对较小的姿态标注数据集上，训练样本包含场景重复，尚不清楚在更大规模、无重复数据上的缩放行为是否会改变。未对编码器与解码器的参数分配比例进行详尽研究，不同上下文视图数下可能存在更优的编解码器宽度/深度配置。主要测试于室内/室外静态场景，未在动态场景或需要处理反射、透明等复杂效果的场景上验证缩放定律。

### 补充图表

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/001_Figure_1.jpg]]
*Figure 1: Scaling Laws for View Synthesis Transformers. Evaluated on RealEstate10K [34], our SVSM exhibits a 3× more compute-optimal Pareto frontier than LVSM while retaining the same scaling behavior (similar slope and curvature everywhere)*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/003_Figure_3.jpg]]
*Figure 3: Effective Batch Size. Training loss (smoothed with a rolling-average) and test PSNR measured throughout training across various paired B and*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/005_Table_1.jpg]]
*Table 1: Stereo*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/010_Figure_7.jpg]]
*Figure 7: Multiview Scaling Behavior. Conducted on DL3DV [15]. (a) For*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/011_Table_4.jpg]]
*Table 4: Multiview*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/021_Table_10.jpg]]
*Table 10: PRoPE ablations. We vary where we apply PRoPE, try a different relative attention method (GTA), and also test pose information flow. GTA varies negligibly from PRoPE, indicating that epipolar geometry is not crucial, and the skip pose connection also has negligible impact, indicating that pose information flow is not responsible*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/007_Table_3.jpg]]
*Table 3: Parameter and Data Scaling Coefficients. As regressed from the plots in Fig. 4, we find power law coefficients for scaling models and data with respect to compute*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/013_Figure_9.jpg]]
*Figure 9: Fixed-size Latent Scaling Experiments. Conducted on Objaverse [4]. (a) For VC =8, SVSM and LVSM decoder-only scale equally while SVSM’s frontier is shifted by 5× on the compute axis. (b) When a fixed latent bottleneck is used, SVSM-fixed and LVSM encoder-decoder scale equally, but significantly worse than the unbottlenecked designs. SVSM again maintains a superior pareto frontier*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/004_Figure_4.jpg]]
*Figure 4: Data and Model Scaling Plots. While our model (blue) is optimal when sufficient data is available, decoderonly LVSM (red) performs better with less data. The Pareto frontier analysis shows that our model is more data-hungry. Our model is also less parameter-efficient, although the gap closes as we increase the training compute. However, with sufficient data and compute, our model (blue) is overall superior in terms of training compute-optimality and rendering speed*

![[assets/figures/papers/paper_list_l2586_https_arxiv_org_abs_2602_21341/figures/017_Figure_10.jpg]]
*Figure 10: Linear Power Scaling Laws. We fit scaling laws onto sections of the Pareto-frontiers of the model families. We see that both models have approximately the same slope in each of their corresponding sections, indicating equal scaling*



## 定位与知识库关联

### 1. 架构范式：从Decoder-Only到Encoder-Decoder的缩放重构

本工作提出的**Scalable View Synthesis Model (SVSM)** 直接对标当前视图合成Transformer的SOTA基线——**LVSM**（Large View Synthesis Model）的decoder-only架构。LVSM采用纯双向自注意力的ViT层堆叠，每次渲染一个目标视图时需将全部上下文视图连同目标token一并输入，其计算复杂度为：

$$
\chi_{\mathrm{MLP}}^{\mathrm{(LVSM)}} \propto V_T (V_C+1), \qquad \chi_{\mathrm{Attn}}^{\mathrm{(LVSM)}} \propto V_T (V_C+1)^2
$$

这意味着每增加一个目标视图，MLP和注意力计算量分别以线性与平方关系增长。SVSM将这一范式重构为encoder-decoder：编码器通过双向自注意力一次性处理上下文视图集，生成场景表征（图像块token集合）；解码器则通过交叉注意力单向地从场景表征中提取信息，并行渲染多个目标视图。其复杂度降为：

$$
\chi_{\mathrm{MLP}}^{\mathrm{(SVSM)}} \propto V_T + V_C, \qquad \chi_{\mathrm{Attn}}^{\mathrm{(SVSM)}} \propto V_C (V_T + V_C)
$$

这一结构性差异构成了SVSM计算效率优势的根本来源：MLP主导的计算区域中，SVSM的FLOPs仅与 $V_T+V_C$ 成正比，而LVSM与 $V_T(V_C+1)$ 成正比。

### 2. 有效批量大小：连接架构与缩放定律的关键机制

SVSM的核心因果调控变量是**有效批量大小** $B_{\mathrm{eff}} \equiv B \cdot V_T$——即训练场景数 $B$ 与每场景目标视图数 $V_T$ 的乘积。该发现揭示了：决定训练性能和计算最优折衷的是 $B_{\mathrm{eff}}$，而非单独的 $B$ 或 $V_T$。

这一机制直接区分了两类架构的缩放行为：
- **LVSM**的训练计算量 $\chi^{\mathrm{(LVSM)}} \propto B_{\mathrm{eff}} (V_C+1)$，与有效批量和上下文视图数成正比，调整 $V_T$ 无法获得算力优势。
- **SVSM**的训练计算量 $\chi^{\mathrm{(SVSM)}} \propto B_{\mathrm{eff}} + B V_C$，可通过增大 $V_T$ 并减小 $B$ 来降低总计算量，同时保持 $B_{\mathrm{eff}}$ 及性能不变。

实验证据（Figure 3）表明：相同 $B_{\mathrm{eff}}$ 的不同 $(B, V_T)$ 组合，训练损失和测试PSNR几乎重合（差异≤±0.2 PSNR），验证了该假设的稳健性。

### 3. 相对相机注意力：多视图扩展的使能技术

在多视图（$V_C>2$）设置中，朴素SVSM的缩放趋势迅速饱和。本工作引入**PRoPE**（Projected Rotary Position Embedding）——一种相对相机旋转位置编码，在编码器与解码器的注意力层中将特征规范化至目标坐标系，确保位姿信息在深层中得以保持。

PRoPE的消融实验（Table 10）揭示了两个关键结论：
- **相对嵌入是核心**：仅对解码器施加PRoPE即可接近全加PRoPE的性能，表明相对位置编码而非对极几何是视图数可扩展的关键。
- **对极几何非必需**：将PRoPE替换为GTA（Global Transformer Attention）效果相当，进一步排除了额外位姿信息流的必要性。

添加PRoPE后，SVSM在多视图设置中恢复了与LVSM等同的缩放趋势，且保持Pareto前沿的计算效率优势（Figure 7）。

### 4. 与显式几何方法的定位关系

SVSM属于**纯学习型视图合成**路线，与依赖显式几何先验的方法形成对比。在RealEstate10K基准上，SVSM（416M参数量）以30.01 PSNR超越此前基于3D高斯泼溅的方法：
- **GS-LRM**（Zhang et al., ECCV 2024）：28.10 PSNR
- **pixelSplat**（Charatan et al., CVPR 2024）：基于显式3D高斯
- **MVSplat**（Chen et al., ECCV 2024）：基于高斯的视图合成
- **pixelNeRF**（Yu et al., CVPR 2021）：基于NeRF的通用视图合成

SVSM的优势在于无需显式几何重建，通过缩放Transformer即可隐式学习场景几何与外观，这使其在训练计算效率上具有根本性优势。

### 5. 适用边界与局限

**当前验证范围**：
- 主要测试于室内/室外静态场景（RealEstate10K、DL3DV、Objaverse），未涉及动态场景或反射、透明等复杂效果。
- 缩放定律建立在相对较小的姿态标注数据集上，训练样本存在场景重复；文中承认这与标准缩放实践（单epoch训练）不同，但未观察到明显过拟合。

**架构层面的开放问题**：
- 未对编码器与解码器的参数分配比例进行详尽研究；不同 $V_C$ 下可能存在更优的编解码器宽度/深度配置。
- 固定大小瓶颈场景表征的缩放性能显著劣于无瓶颈设计（Figure 9b），该架构路径的潜力有限。

**缩放行为的未解之谜**：
- LVSM decoder-only的Chinchilla缩放系数呈现 $a \neq b$（$a=0.65, b=0.33$），而SVSM的 $a \approx b$（0.52 vs 0.47），这一差异是否反映了架构的根本特性尚待解释。
- PRoPE阻止位姿信息在encoder-decoder瓶颈中丢失的具体机制，以及相对注意力与交叉注意力的协同工作原理仍需深入探究。
- 在更多上下文视图（如 $V_C=16$ 或更多）及更长序列下，SVSM的线性成本优势能否持续保持，缩放定律是否仍成立，尚无实验验证。

### 6. 知识库定位总结

SVSM的核心贡献在于将视图合成Transformer的缩放问题从“如何设计更好的单视图渲染器”重构为“如何定义有效批量并利用encoder-decoder架构实现计算最优缩放”。其方法谱系可定位为：

| 维度 | 基线（LVSM decoder-only） | 本工作（SVSM） |
|------|--------------------------|----------------|
| 架构范式 | decoder-only，双向自注意力 | encoder-decoder，交叉注意力解码 |
| 场景表征 | 无持久表征，每目标重新处理上下文 | 编码器输出图像块token集合 |
| 计算复杂度 | $\propto V_T(V_C+1)$ | $\propto V_T+V_C$ |
| 批量定义 | 隐式使用多目标视图 | 显式定义 $B_{\mathrm{eff}} = B \cdot V_T$ |
| 多视图扩展 | 需PRoPE辅助 | 需PRoPE恢复缩放趋势 |
| 缩放系数 | $a \neq b$ | $a \approx b$ |

该工作为视图合成Transformer的缩放研究建立了可复现的基准和理论框架，但其缩放定律的普适性——尤其是在更大规模、无重复数据上的表现——仍需后续工作验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Scaling_View_Synthesis_Transformers.pdf]]

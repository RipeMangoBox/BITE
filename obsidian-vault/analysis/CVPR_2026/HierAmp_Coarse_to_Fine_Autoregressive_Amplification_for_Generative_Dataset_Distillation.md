---
title: "HierAmp: Coarse-to-Fine Autoregressive Amplification for Generative Dataset Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HierAmp_Coarse_to_Fine_Autoregressive_Amplification_for_Generative_Dataset_Distillation.pdf
project_link: null
code_link: "https://github.com/Oshikaka/HIERAMP"
aliases:
- HierAmp
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过在不同VAR尺度上注入可学习的类别令牌，并利用其产生的显著性图对自回归生成过程中的注意力进行正偏置放大（即各尺度的注意力放大强度β_n与Top-ρ选取比例），从而引导模型聚焦于语义重要区域。
primary_logic: VAR模型的由粗到细生成天然对齐物体语义层次：早期尺度构建整体布局，后期尺度补充细节。在各尺度对语义显著区域施加注意力放大，粗尺度使令牌分布更均匀多样，细尺度使注意力更集中，从而在不显式优化全局分布相似度的情况下显著提升蒸馏数据的下游分类性能。
claims:
- HIERAMP在ImageNet-1K IPC=10上ResNet-18达到47.6%准确率，超越此前最佳方法CaO2 1.5%。
- 粗尺度放大增加令牌多样性，细尺度放大集中注意力，消融证实粗尺度放大对性能提升贡献最大。
- 引入类别令牌并基于其注意力图放大显著提升判别性，且FID与VAR基线接近，不牺牲生成保真度。
- CIFAR-10 上 Top-1 Acc (ResNet-18) = 44.3 ± 0.6 (IPC=10)
---

# HierAmp: Coarse-to-Fine Autoregressive Amplification for Generative Dataset Distillation

> [!tip] 核心洞察
> VAR模型的由粗到细生成天然对齐物体语义层次：早期尺度构建整体布局，后期尺度补充细节。在各尺度对语义显著区域施加注意力放大，粗尺度使令牌分布更均匀多样，细尺度使注意力更集中，从而在不显式优化全局分布相似度的情况下显著提升蒸馏数据的下游分类性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | HierAmp：面向生成式数据集蒸馏的由粗到细自回归放大方法 |
| 英文题名 | HierAmp: Coarse-to-Fine Autoregressive Amplification for Generative Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.06932) · [Code](https://github.com/Oshikaka/HIERAMP) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HIERAMP |
| Dataset | CIFAR-10, ImageNet-1K |

> [!tip] 效果简介
> - CIFAR-10 上，Top-1 Acc (ResNet-18) 44.3 ± 0.6 (IPC=10) vs D3HR 41.3 ± 0.1 (+3.0)。
> - ImageNet-1K 上，Top-1 Acc (ResNet-18) 47.6 ± 0.1 (IPC=10) vs CaO2 46.1 ± 0.2 (+1.5)；Top-1 Acc (ResNet-101) 66.4 ± 0.3 (IPC=50) vs CaO2 66.2 ± 0.1 (+0.2)。
> - ImageNet-1K (Cross-Arch) 上，Top-1 Acc (EfficientNet-B0 student) 28.7 ± 0.4 (IPC=10) vs D3HR 28.1 ± 0.1 (+0.6)。

## 概要

当前数据集蒸馏的主流范式聚焦于使合成数据的全局分布逼近原始数据分布，但这一视角忽略了一个关键瓶颈：**对象语义天然具有层次性**——从粗粒度的整体布局到细粒度的部件细节，而现有方法未能显式捕捉这种层次化判别语义，导致蒸馏数据在下游分类任务中缺乏关键的判别能力。

针对上述瓶颈，本文提出 **HIERAMP**（Hierarchical Autoregressive Amplification），一种面向生成式数据集蒸馏的由粗到细自回归放大方法。其核心洞察在于：视觉自回归（VAR）模型的由粗到细生成过程天然对齐了物体语义层次——早期尺度构建整体布局，后期尺度补充细节。HIERAMP 在各 VAR 尺度上注入可学习的类别令牌，利用其产生的显著性图识别语义重要区域，并通过正偏置放大这些区域的注意力权重，从而在不显式优化全局分布相似度的前提下，引导模型聚焦于判别性语义特征。

在方法谱系上，HIERAMP 属于基于生成模型的数据集蒸馏路线，与此前基于扩散模型的方法（如 **Minimax**、**D3HR**、**CaO2**）以及基于真实图像补丁裁剪的方法（**RDED**）形成对比。HIERAMP 的独特之处在于首次将 VAR 的层次化生成特性与语义引导的注意力放大相结合，实现了从“匹配全局分布”到“增强判别语义”的范式转换。

主要实验结果验证了该方法的有效性：在 ImageNet-1K IPC=10 设置下，HIERAMP 在 ResNet-18 上达到 **47.6%** 的 Top-1 准确率，超越此前最佳方法 CaO2 约 1.5 个百分点；在 CIFAR-10 上达到 **44.3%**，超越 D3HR 约 3.0 个百分点。消融实验进一步揭示：粗尺度放大增加了令牌多样性与覆盖率，细尺度放大则使注意力更集中——这种阶段特异性的放大机制是性能提升的关键。此外，HIERAMP 在保持生成保真度（FID 与 VAR 基线接近）的同时，仅引入极小的计算开销（延迟增加约 0.008 s/img），且具备良好的跨架构泛化能力。

数据集蒸馏旨在将大规模数据集压缩为极少量合成样本，使下游模型在这些样本上训练后能逼近在全量数据上的性能。近年来，基于生成模型的数据集蒸馏方法取得了显著进展，其核心思路是利用预训练生成器合成信息密度更高的蒸馏图像。然而，现有方法普遍存在一个关键瓶颈：**它们仅关注蒸馏数据与真实数据在全局分布层面的相似性，未能捕捉对象语义的层次性**——从粗粒度的整体布局到细粒度的部件细节。这一缺失导致蒸馏数据缺乏对下游分类任务至关重要的判别性语义，限制了性能的进一步提升。

视觉自回归模型（Visual Autoregressive Model, VAR）提供了一种天然契合语义层次结构的生成范式。如图 1 顶部所示，VAR 的生成过程从粗到细逐步构建图像：早期尺度（粗尺度）负责建立场景的整体结构与布局，后期尺度（细尺度）则补充纹理、边缘等局部细节。这一过程与人类视觉认知中"先整体后局部"的层次化理解高度一致。然而，标准 VAR 模型在自回归解码时对所有空间位置一视同仁，并未显式利用这种层次化语义特性来增强生成样本的判别力。

HIERAMP 的核心洞察在于：**如果能在 VAR 各尺度上识别语义显著区域，并在自回归生成过程中对这些区域施加注意力放大，就能引导模型聚焦于对分类更有意义的语义特征，从而在不显式优化全局分布相似度的前提下，显著提升蒸馏数据的下游分类性能**。具体而言，粗尺度的注意力放大使令牌分布更均匀多样，增加了合成样本的全局结构变化；细尺度的注意力放大则使注意力更集中，强化了局部判别性细节。这种由粗到细的层次化放大策略，将 VAR 的生成结构优势转化为数据集蒸馏的性能增益。

## 核心方法与创新机理

HIERAMP的核心创新在于首次将视觉自回归（VAR）模型的由粗到细生成特性与数据集蒸馏的语义需求对齐，通过**层次化语义放大**机制解决现有方法仅关注全局分布相似性而忽略对象语义层次性的瓶颈。具体而言，该方法在三个关键维度上对标准VAR生成管线进行了改造：

### 1. 尺度特定类别令牌注入

标准VAR自回归生成过程仅依赖类别嵌入 $s$ 作为初始条件，各尺度解码器缺乏对类别语义的直接感知。HIERAMP在每一尺度 $n$ 引入可学习的类别令牌 $[c]_n$，并通过**尺度限制注意力掩码** $m_{n,\mathrm{cls}}^{(h)}$ 强制其仅关注当前尺度的图像令牌，阻断跨尺度交互。该设计的因果机制在于：不同尺度承载不同粒度的语义——粗尺度编码整体布局，细尺度编码纹理细节——因此每个尺度需要独立的语义总结器。类别令牌通过分类损失 $\mathcal{L}_{\mathrm{cls}}$ 训练，产生尺度特定的显著性图 $M_n \in \mathbb{R}^{h_n \times w_n}$，为后续放大提供精确的语义引导信号。

### 2. 语义引导的注意力放大

这是HIERAMP最核心的机制创新。在每个尺度的自注意力计算中，方法首先根据类别令牌的注意力图 $m_n$ 选取 $\text{Top-}\rho_n\%$ 的显著位置，生成二进制掩码 $a_n$；随后在所有查询的注意力logits中，为这些显著键添加正偏置 $\beta_n$：

$$\tilde{L}_n^{(h)} = L_n^{(h)} + \beta_n \mathbf{1}_{L_k^n+1} a_n^{\top}$$

这一操作的因果效应是**将注意力概率质量向语义重要区域集中**，使模型在解码时优先关注对分类判别性至关重要的特征。该偏置作用于所有查询，包括图像令牌间的自注意力和类别令牌的交叉注意力，从而在全局范围内重塑信息流动。

### 3. 阶段感知放大调度

HIERAMP并非对所有尺度施加统一的放大强度，而是将9个尺度划分为**粗（1-3）、中（4-6）、细（7-9）**三组，分别配置不同的 $\rho_n$ 和 $\beta_n$ 参数。消融实验（Table 4）揭示了一个关键发现：粗和中尺度放大通过增加码书令牌的熵和覆盖率来**提升多样性**，而细尺度放大则使注意力**更集中**于局部判别性细节。最优配置（粗-中-细放大数 = 5-5-0.5）在ImageNet-1K IPC=10上达到46.8%，验证了“粗尺度构建多样全局结构、细尺度精炼关键细节”这一分工的有效性。该调度策略是HIERAMP性能超越CaO2等基线方法的关键因素——粗尺度放大的贡献最大，而细尺度过度放大反而会损害性能。

值得注意的是，类别令牌本身对准确率无显著增益（Table 7：有类别令牌45.9% vs 无类别令牌45.6%），其价值纯粹在于**为放大提供语义引导信号**。这一消融结果证实HIERAMP的性能提升完全来自注意力放大机制对语义层次性的利用，而非模型容量的简单增加。

HIERAMP 的整体 pipeline 围绕一个预训练的视觉自回归模型（VAR）构建，通过注入可学习的类别令牌并对其产生的语义显著性图进行注意力放大，实现由粗到细的层次化语义增强。整个框架由三个核心模块串联而成，形成“语义感知→显著性定位→注意力引导生成”的闭环。

**输入与输出流**：给定目标类别标签，系统首先将其映射为类别嵌入 $s$，作为 VAR 逐尺度自回归生成的起始条件。VAR 按照从粗到细的 $N$ 个尺度依次生成图像令牌序列 $r_1, r_2, \dots, r_N$，每个尺度 $n$ 的令牌 $r_n$ 通过 VQ-VAE 的码书与解码器最终还原为图像。HIERAMP 在此生成过程中插入语义引导，输出的蒸馏图像在保持生成保真度的同时，显著增强了判别性语义特征。

**模块关系与数据流**：

1. **预训练 VAR 生成器**（Section 3.1）：作为基础骨干，VAR 以由粗到细的方式预测整个令牌图的下一尺度，而非逐令牌自回归。其联合概率分布为 $P = \prod_{n=1}^{N} p_{\boldsymbol{\theta}}(r_n \mid r_1, \dots, r_{n-1})$，推理时从类别嵌入 $s$ 开始逐尺度采样。各尺度特征通过残差更新 $r_n = r_n + \mathcal{U}_{(n-1) \to n}(r_{n-1})$ 实现跨尺度信息融合。该模块提供了层次化生成的结构基础，其天然的多尺度特性是后续语义放大的前提。

2. **尺度受限类别令牌注意力**（Section 3.3，Figure 2-left）：在每个尺度 $n$ 引入一个可学习的类别令牌 $[c]_n$，并通过尺度限制注意力掩码 $m_{n,\mathrm{cls}}^{(h)}$ 强制其仅关注同一尺度的图像令牌，阻断跨尺度交互。类别令牌的注意力图 $\alpha_{n,\mathrm{cls}}^{(h)}$ 经多头平均和空间重塑后，形成该尺度的语义显著性图 $M_n \in \mathbb{R}^{h_n \times w_n}$。该模块的作用是为后续放大提供精准的语义定位信号——$M_n$ 中高响应区域对应物体语义的关键部位。

![[assets/figures/papers/paper_list_l2684_https_arxiv_org_abs_2603_06932/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the HIERAMP framework. Left: Scale-Restricted Class Token Attention Mask. The class token attends only to image tokens from the corresponding scale, with grey regions indicating blocked attention, producing a scale-specific semantic summary. Right: Multi-Scale Semantic Feature Amplification. The Amplify Algorithm selects the top attention positions from the class-token map at each scale and amplifies them via a positive logit bias, guiding the model to focus on semantically important features during decoding*

3. **由粗到细自回归放大**（Section 3.4，Figure 2-right，Algorithm 1）：在每个尺度的自回归解码过程中，从显著性图 $m_n$ 中选取 Top-$\rho_n\%$ 的显著位置构成集合 $S_n$，生成二进制掩码 $a_n$。随后，在所有查询对该尺度键的注意力 logits 中，为 $S_n$ 中的位置施加正偏置 $\beta_n$：$\tilde{L}_n^{(h)} = L_n^{(h)} + \beta_n \mathbf{1}_{L_k^n+1} a_n^{\top}$。这一操作将注意力概率质量向语义重要区域集中，引导解码器聚焦于判别性特征的生成。放大调度按阶段分组——粗尺度（1-3）强调全局物体布局，中尺度（4-6）补充结构信息，细尺度（7-9）细化纹理细节——各阶段使用不同的 $(\rho_n, \beta_n)$ 参数配置。

三个模块的协同机制可概括为：VAR 提供层次化生成骨架，类别令牌在各尺度捕获语义显著性，放大模块利用该显著性信号偏置自回归解码的注意力分布，从而在不修改生成模型结构、不显式优化全局分布相似度的前提下，显著提升蒸馏数据的下游分类性能。Figure 2 完整展示了这一框架的左右两翼——左侧为尺度受限的类别令牌注意力掩码设计，右侧为多尺度语义特征放大的执行流程。

### 整体框架

HIERAMP在预训练VAR（Visual Autoregressive Model）的由粗到细生成过程中，注入可学习的类别令牌并利用其产生的显著性图对各尺度注意力施加正偏置放大，从而引导模型聚焦于语义重要区域。框架包含三个核心模块：预训练VAR生成器、尺度受限类别令牌注意力、以及由粗到细自回归放大（Figure 2）。

### 模块一：预训练VAR生成器

VAR以由粗到细的方式生成图像令牌。给定初始类别嵌入 $s$，VAR将图像令牌序列划分为 $N$ 个尺度，每个尺度 $n$ 的令牌图分辨率为 $h_n \times w_n$。其联合概率为各尺度条件概率的乘积：

$$P = \prod_{n=1}^{N} p_{\boldsymbol{\theta}}(r_n \mid r_1, \dots, r_{n-1}) \quad (1)$$

推断时，VAR逐尺度自回归采样：

$$\begin{array}{l} r_1 \sim p_{\theta}(r_1 \mid s), \\ r_2 \sim p_{\theta}(r_2 \mid r_1), \\ \quad \cdot \cdot \\ r_N \sim p_{\theta}(r_N \mid r_1, \ldots, r_{N-1}), \end{array} \quad (2)$$

各尺度特征通过上采样前一尺度并与当前尺度相加实现跨尺度信息融合：

$$r_n = r_n + \mathcal{U}_{(n-1) \to n}(r_{n-1}) \quad (3)$$

由于模型在离散令牌空间运行，VAR使用VQ-VAE通过码书去量化解码将令牌特征映射回图像空间。该模块是HIERAMP的基础生成引擎，其由粗到细的生成过程天然对齐物体语义层次：早期尺度构建整体布局，后期尺度补充细节。

### 模块二：尺度受限类别令牌注意力

为捕获各尺度的语义信息，在每个尺度 $n$ 引入可学习类别令牌 $[c]_n$。设尺度 $n$ 的输入嵌入为 $\tilde{X}_n \in \mathbb{R}^{(L_k^n+1) \times d}$，其中 $L_k^n = h_n \times w_n$ 为图像令牌数，末尾位置为类别令牌。多头注意力的投影为：

$$Q_n^{(h)} = \tilde{X}_n W_Q^{(n)}, \quad K_n^{(h)} = \tilde{X}_n W_K^{(n)}, \quad V_n^{(h)} = \tilde{X}_n W_V^{(n)} \quad (4)$$

关键设计在于尺度限制注意力掩码 $m_{n,\mathrm{cls}}^{(h)}$：类别令牌仅关注同一尺度的图像令牌，阻断跨尺度交互。其注意力图计算如下：

$$\alpha_{n,\mathrm{cls}}^{(h)} = \mathrm{softmax}\left( \frac{Q_n^{(h)}[:,-1] (K_n^{(h)})^{\top}}{\sqrt{d_h}} + m_{n,\mathrm{cls}}^{(h)} \right) \quad (5)$$

其中 $Q_n^{(h)}[:,-1]$ 为类别令牌的查询向量。随后对多头注意力取平均并重塑为空间网格，得到尺度 $n$ 的语义显著性图：

$$m_n = \frac{1}{H} \sum_{h=1}^{H} \alpha_{n,\mathrm{cls}}^{(h)}, \quad M_n = \mathrm{R}_{h_n \times w_n}(m_n) \in \mathbb{R}^{h_n \times w_n} \quad (7)$$

该显著性图标识了当前尺度下与类别语义最相关的空间区域，为后续放大提供引导信号。

### 模块三：由粗到细自回归放大

基于显著性图 $m_n$，选取Top-$\rho_n\%$ 的显著位置作为放大目标：

$$S_n = \mathrm{Top}\text{-}\rho_n(m_n) \quad (8)$$

据此生成二进制掩码 $a_n \in \{0,1\}^{L_k^n}$，显著位置标记为1。在自回归解码时，对所有查询的注意力logits施加正偏置 $\beta_n$：

$$\tilde{L}_n^{(h)} = L_n^{(h)} + \beta_n \mathbf{1}_{L_k^n+1} a_n^{\top} \quad (10)$$

其中 $\mathbf{1}_{L_k^n+1}$ 为全1向量，$L_n^{(h)}$ 为原始注意力logits矩阵。该操作使所有查询对显著键的注意力权重增加 $\beta_n$，将概率质量向语义重要区域集中。

放大采用阶段感知调度：将9个尺度分为粗（1-3）、中（4-6）、细（7-9）三组，分别设置不同的Top-$\rho$ 和 $\beta$ 参数。粗尺度强调全局物体区域，使令牌分布更均匀多样；细尺度聚焦纹理细节，使注意力更集中。消融实验证实，粗尺度放大对性能提升贡献最大（Table 3），平衡配置（粗-中-细=5-5-0.5）达到最优46.8%（Table 4）。

### 关键公式变量说明

| 符号 | 含义 |
|------|------|
| $r_n$ | 尺度 $n$ 的令牌特征 |
| $s$ | 初始类别嵌入 |
| $[c]_n$ | 尺度 $n$ 的可学习类别令牌 |
| $m_{n,\mathrm{cls}}^{(h)}$ | 尺度限制注意力掩码 |
| $\alpha_{n,\mathrm{cls}}^{(h)}$ | 类别令牌在头 $h$ 的注意力分布 |
| $M_n$ | 尺度 $n$ 的语义显著性图 |
| $\rho_n$ | 尺度 $n$ 选取的显著位置比例 |
| $\beta_n$ | 尺度 $n$ 的注意力放大强度 |
| $a_n$ | 显著位置二进制掩码 |
| $\tilde{L}_n^{(h)}$ | 放大后的注意力logits |

## 实验与关键发现

### 核心性能对比

HIERAMP 在多个数据集和 IPC 设置下实现了最优或接近最优的下游分类准确率，验证了层次化语义放大策略的有效性。

**Table 1** 汇总了 HIERAMP 与四个代表性 SOTA 方法——**Minimax**（基于扩散模型）、**D3HR**（高分辨率 DDIM 逆过程）、**RDED**（真实补丁选择与裁剪）和 **CaO2**（扩散驱动概率采样与隐码精炼）——在 CIFAR-10、CIFAR-100、ImageNet-100、ImageNet-Woof 及 ImageNet-1K 上的 Top-1 准确率。所有方法均以 ResNet-18 为教师网络，在 ResNet-18 和 ResNet-101 上评估。

| 数据集 | IPC | HIERAMP (ResNet-18) | 最强基线 | 提升 |
|--------|-----|---------------------|----------|------|
| CIFAR-10 | 10 | **44.3 ± 0.6** | D3HR 41.3 ± 0.1 | +3.0 |
| CIFAR-10 | 50 | **72.0 ± 0.3** | D3HR 71.6 ± 0.1 | +0.4 |
| ImageNet-1K | 10 | **47.6 ± 0.1** | CaO2 46.1 ± 0.2 | +1.5 |
| ImageNet-1K | 50 | **66.4 ± 0.3** (ResNet-101) | CaO2 66.2 ± 0.1 | +0.2 |

关键发现：
- **中低 IPC 场景增益显著**：在 ImageNet-1K IPC=10 上，HIERAMP 以 47.6% 超越此前最佳方法 CaO2 1.5 个百分点，表明在数据极度稀缺时，层次化语义引导的生成能更有效地保留判别性信息。
- **高 IPC 场景增益收窄**：在 CIFAR-100 IPC=50 等设置下，提升幅度有限。这与方法的设计逻辑一致——当合成样本数量充足时，全局分布匹配方法已能较好地覆盖类别特征，层次化放大的边际收益递减。
- **大模型评估稳健**：在 ResNet-101 上同样取得最优，说明蒸馏数据对不同容量网络均有效。

### 交叉架构泛化

**Table 2** 展示了 ImageNet-1K IPC=10 下不同教师-学生网络对的交叉架构性能。HIERAMP 在 ResNet-18→EfficientNet-B0 上达到 28.7 ± 0.4，超越 D3HR 的 28.1 ± 0.1。在 MobileNet-V2 和 ShuffleNet-V2 等轻量架构上同样保持领先，证实蒸馏数据具备较强的架构迁移能力，未对特定网络结构过拟合。

### 消融实验：放大阶段与强度

HIERAMP 的核心设计空间在于**放大阶段的选择**和**各阶段放大强度的分配**。

**Table 3** 系统消融了不同阶段组合的放大效果（ImageNet-1K, IPC=10）。在固定 Top-ρ=50% 的条件下：
- 仅放大粗尺度（1-3 阶段）即可达到 45.8%，显著高于无放大的基线；
- 全阶段放大（1-9）配合 5 个放大区域取得最佳 47.6%；
- 仅放大细尺度（7-9）效果最弱，说明早期全局语义结构的引导比后期纹理细节更为关键。

**Table 4** 进一步探究阶段间放大强度分配（粗-中-细 = C-M-F）。在 5-5-0.5 的配置下达到最优 46.8%，验证了“粗/中阶段承担全局物体区域引导、细阶段适度补充纹理”的直觉。过度放大细阶段（如 5-5-5）反而导致精度下降，可能因为强制聚焦局部纹理破坏了生成多样性。

### 机制分析：令牌熵与覆盖率

**Figure 3** 揭示了放大策略影响下游性能的内在机制。在 ImageNet-1K IPC=50 上，统计各类别码书令牌的熵（公式 $H = -\sum_{i=1}^{N} p_i \log p_i$）和覆盖率（公式 $\mathrm{Coverage} = \frac{N_{\mathrm{used}}}{N_{\mathrm{total}}}$）变化：
- **粗和中尺度放大**使多数类别的令牌熵和覆盖率上升，即令牌使用更均匀、多样性增加；
- **细尺度放大**则使注意力更集中，覆盖率下降，表明模型聚焦于少量高判别性局部特征。

这解释了 HIERAMP 的因果机制：粗尺度放大促进全局布局多样性，防止模式坍塌；细尺度放大强化局部判别细节，提升分类精度。两者协同实现了“不显式优化全局分布相似度却显著提升下游性能”的效果。

### 生成质量与效率

**Table 6** 的 FID 对比表明，HIERAMP 在 ImageNet-1K IPC=10 上 FID 为 17.3，与基础 VAR 的 17.5 几乎持平，且优于 Minimax 和 D3HR。这意味着语义放大未牺牲生成保真度——模型并未通过生成失真图像来“欺骗”分类器。

**Table 8** 和 **Table 9** 分别报告了推理延迟和资源开销。HIERAMP 的单张图像生成延迟仅从 0.139 s 增至 0.147 s，显存从 1.77 GB 增至 1.84 GB，增量极小。相比之下，基于 DDIM 的方法需数十秒级别，HIERAMP 在效率上具有数量级优势。

### 类别令牌的角色

**Table 7** 的消融显示，去除类别令牌后准确率几乎不变（45.9 vs 45.6），表明类别令牌本身不提升性能。其核心价值在于**为放大提供语义引导信号**——无类别令牌则无法定位显著区域，放大策略失效。这证实了 HIERAMP 的增益纯粹来自语义引导的注意力调整，而非额外的可学习参数容量。

### DiT 骨干泛化

**Table 5** 和 **Figure 6** 展示了 HIERAMP 在 DiT（Diffusion Transformer）骨干上的初步泛化。加入层次化放大后，DiT 生成的蒸馏数据在下游分类上取得一致提升，且定性结果显示物体更突出、语义结构更清晰。这暗示由粗到细的语义放大思想可能超越 VAR 架构，适用于更广泛的生成模型家族，但需注意目前仅在 DiT 上验证，大规模扩散 UNet 实验尚缺。

![[assets/figures/papers/paper_list_l2684_https_arxiv_org_abs_2603_06932/figures/003_Table_1.jpg]]
*Table 1: Top-1 accuracy comparison with four SOTA methods. As in RDED [40], all methods adopt ResNet-18 as the teacher and are trained on both ResNet-18 and ResNet-101. ‘–’ denotes missing results in the original paper*

![[assets/figures/papers/paper_list_l2684_https_arxiv_org_abs_2603_06932/figures/004_Table_4.jpg]]
*Table 4: Ablation on amplification strength across stages on ImageNet-1K, IPC=10. Each row shows a different setting of Coarse-Mid-Fine (C-M-F) amplification numbers and accuracy*

![[assets/figures/papers/paper_list_l2684_https_arxiv_org_abs_2603_06932/figures/005_Table_2.jpg]]
*Table 2: Cross-architecture performance on ImageNet-1K, IPC=10*

![[assets/figures/papers/paper_list_l2684_https_arxiv_org_abs_2603_06932/figures/010_Table_5.jpg]]
*Table 5: Quantitative comparison of the DiT backbone before and after applying HIERAMP*

![[assets/figures/papers/paper_list_l2684_https_arxiv_org_abs_2603_06932/figures/011_Table_8.jpg]]
*Table 8: Inference latency comparison with DDIM-based method on ImageNet-Woof*

## 定位与知识库关联

### 1. 在数据集蒸馏领域中的位置

HIERAMP 属于**生成式数据集蒸馏**（Generative Dataset Distillation）这一子方向。与传统的基于元学习或梯度匹配的蒸馏方法不同，生成式方法的核心思路是先训练一个生成模型来捕获原始数据分布，再从中采样合成蒸馏数据集，用于下游分类器训练。HIERAMP 延续了这一范式，但其独特贡献在于首次将**视觉自回归模型**（Visual Autoregressive Model, VAR）引入蒸馏流程，并利用其由粗到细的生成特性来实现**层次化语义放大**。

### 2. 与现有基线方法的关系

#### 2.1 基于扩散模型的方法

- **Minimax**：基于扩散模型的早期生成式蒸馏方法，通过极小极大优化选择最具信息量的合成样本。其局限在于仅关注全局分布相似性，忽略了对象语义的层次结构。HIERAMP 在 ImageNet-1K IPC=10 上以 47.6% 的准确率显著超越 Minimax（具体数值见 Table 1，需手动核实原文），且 FID 更优（17.3 vs. Minimax 的更高值，Table 6）。

- **D3HR**：利用 DDIM 逆过程实现高分辨率数据集蒸馏。该方法在 CIFAR-10 IPC=10 上达到 41.3%，而 HIERAMP 达到 44.3%（+3.0%），且推理延迟显著更低（Table 8）。D3HR 的瓶颈在于 DDIM 逆过程计算开销大，且同样缺乏对语义层次性的显式建模。

- **CaO2**：扩散驱动、结合概率采样与隐码精炼的最新方法，在 ImageNet-1K IPC=10 上此前以 46.1% 保持最优。HIERAMP 以 47.6% 超越 CaO2 1.5 个百分点，且在 IPC=50 的 ResNet-101 上达到 66.4%（vs. CaO2 66.2%）。CaO2 仍基于扩散模型，未利用 VAR 的由粗到细结构。

#### 2.2 基于真实图像补丁的方法

- **RDED**：通过选择和裁剪真实图像补丁来构建蒸馏数据集，不依赖生成模型。该方法在部分设置下表现强劲，但其本质是数据筛选而非生成，因此无法创造训练分布之外的新样本，泛化性受限于原始数据的覆盖范围。HIERAMP 的生成式路线在交叉架构泛化实验（Table 2）中展现了更强的迁移能力。

### 3. 方法适用边界与局限

#### 3.1 对预训练 VAR 模型的依赖

HIERAMP 的核心机制建立在 VAR 模型的由粗到细生成特性之上。这意味着：
- **生成质量上限**受限于预训练 VAR 的能力。若目标域与 VAR 训练数据（ImageNet）分布差异较大（如医学影像、遥感图像），可能需要重新微调或训练 VAR，增加了部署成本。
- **模型架构绑定**：当前验证仅在 VAR 和 DiT 上进行（Table 5 显示 DiT 上亦有增益），但未在纯扩散 UNet 等其他生成模型家族上大规模实验。方法的通用性尚待进一步验证。

#### 3.2 性能增益的场景依赖性

- **中低 IPC 场景增益更明显**：在 CIFAR-100 IPC=50 等小规模高 IPC 设置上，相比最强基线的提升有限。这表明当每类合成样本数已经较多时，层次化语义放大带来的额外判别性增益趋于饱和。
- **放大超参数需手动设置**：放大强度 β_n 和选取比例 ρ_n 需要分阶段手动配置。消融实验（Table 3、Table 4）给出了推荐配置（如粗中细=5-5-0.5 达到最优 46.8%），但自适应学习这些超参数可能更鲁棒。

#### 3.3 计算开销与效率

虽然 HIERAMP 的额外开销极小（延迟仅增加 0.139→0.147 s/img，显存增加 1.77→1.84 GB，Table 9），且显著快于基于 DDIM 的方法，但其本质上仍需要完整的 VAR 前向过程，无法像某些免生成的方法那样完全规避生成模型的推理成本。

### 4. 开放问题与未来方向

1. **跨生成模型泛化**：如何在更多类型的生成模型（如扩散 UNet、GAN）上高效实现层次化语义放大，并保持生成多样性与保真度？当前仅在 DiT 上进行了初步验证（Table 5），尚未形成系统性结论。

2. **自适应放大调度**：能否让模型自适应学习各尺度的放大强度与比例，代替手动分阶段调度？这可以通过元学习或基于下游任务反馈的强化学习来实现。

3. **非自然图像域的迁移**：对于细粒度分类、医学影像、遥感图像等非自然图像任务，层次化放大是否依然有效？这些领域的语义层次结构可能与自然图像有本质差异。

4. **理论形式化**：粗尺度放大增加令牌多样性、细尺度放大集中注意力的机制（Figure 3），目前主要基于经验观察（令牌熵和覆盖率指标）。是否可以通过信息论或注意力流的角度进行更深入的理论分析？

5. **与提示工程/条件生成的结合**：类别令牌的设计本质上是一种隐式条件注入。未来可探索将文本描述、属性标签等多模态条件与层次化放大结合，进一步提升蒸馏数据的可控性和判别性。

## 原文 PDF

![[paperPDFs/CVPR_2026/HierAmp_Coarse_to_Fine_Autoregressive_Amplification_for_Generative_Dataset_Distillation.pdf]]

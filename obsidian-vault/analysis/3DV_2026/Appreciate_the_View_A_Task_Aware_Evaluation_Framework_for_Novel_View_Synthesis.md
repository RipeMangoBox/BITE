---
title: "Appreciate the View: A Task-Aware Evaluation Framework for Novel View Synthesis"
type: paper
paper_level: A
venue: 3DV
year: 2026
pdf_ref: paperPDFs/3DV_2026/Appreciate_the_View_A_Task_Aware_Evaluation_Framework_for_Novel_View_Synthesis.pdf
project_link: https://saarst.github.io/appreciate-the-view-website/
code_link: null
aliases:
- PMDM
- AVTAEFNVS
tags:
- 3DV_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "从NVS基础模型（Zero123）提取的扩散特征与对比学习微调：通过三元组（源、目标、姿态）感知嵌入，在VIEWMATCH数据集上训练轻量投影头，使嵌入空间能区分合理与不合理的生成结果。"
primary_logic: "扩散模型的中间特征天然编码视角相关的几何和外观信息；利用对比学习将这些特征精炼为紧凑的L2归一化嵌入，可同时支持全参考（DPRISM）和无参考（MMDPRISM）两种评估模式，且与人类判断高度一致。"
claims:
- "原始扩散特征在VIEWMATCH上的线性分类AUC达到0.90，远优于CLIP（0.73）和DINOv2（0.68）。"
- "无参考MMDPRISM能明确区分正样本（0.691）和负样本（0.984），而FID（102.360 vs 107.240）等传统分布指标无法区分。"
- "DPRISM在与人类判断的相关性上优于所有基线，例如图像质量(IQ)的Pearson相关系数为0.394，而PSNR为-0.323。"
- "VIEWMATCH 上 AUC (linear classifier) = 0.90 (Diffusion t=0)"
---

# Appreciate the View: A Task-Aware Evaluation Framework for Novel View Synthesis

> [!tip] 核心洞察
> 扩散模型的中间特征天然编码视角相关的几何和外观信息；利用对比学习将这些特征精炼为紧凑的L2归一化嵌入，可同时支持全参考（DPRISM）和无参考（MMDPRISM）两种评估模式，且与人类判断高度一致。

| 字段 | 内容 |
| ------- | ------------------------------------------------------------------------------- |
| 中文题名 | 欣赏视角：一种面向新视角合成的任务感知评估框架 |
| 英文题名 | Appreciate the View: A Task-Aware Evaluation Framework for Novel View Synthesis |
| 会议/期刊 | 3DV 2026 |
| Links | [paper](https://arxiv.org/abs/2511.12675) · [Project](https://saarst.github.io/appreciate-the-view-website/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | PRISM (Metrics: DPRISM / MMDPRISM) |
| Dataset | VIEWMATCH, GSO (User Study), Toys4K |

> [!tip] 效果简介
> - VIEWMATCH 上，AUC (linear classifier) 为 0.90 (Diffusion t=0)，对比 0.73 (CLIP-CAT-Angle)，变化 +0.17。
> - VIEWMATCH 上，MMDPRISM (Positive vs Negative) 为 0.691 / 0.984，对比 FID 102.360 / 107.240 (no separation)，变化 clear separation vs. flat。
> - GSO (User Study) 上，Pearson correlation (Image Quality) 为 0.394 (DPRISM)，对比 -0.323 (PSNR)，变化 +0.717。

## 概要

新视角合成（Novel View Synthesis, NVS）旨在从有限观测中重建三维场景的任意视角图像。随着扩散模型等生成式方法的快速发展，NVS 模型生成的图像在视觉质量上已相当逼真，但**如何可靠地评估这些生成结果**仍是一个悬而未决的瓶颈。

现有评估指标——无论是全参考的 PSNR、SSIM、LPIPS，还是无参考的 FID、CMMD——均未捕捉 NVS 任务的核心结构：**源图像、目标视角与生成结果之间的三元关系**。这导致两类系统性失效：其一，全参考指标常对合理的视角变化施加错误惩罚；其二，无参考分布指标对视角一致性完全不敏感，无法区分生成质量的高低。图 1 给出了定性证据：PSNR、SSIM、LPIPS 和 CLIP-S 在多个案例中错误地偏好明显不合理的生成结果。

本文提出 **PRISM**，一种面向 NVS 的任务感知评估框架。其核心洞察在于：**扩散式 NVS 模型（Zero123）的中间特征天然编码了视角相关的几何与外观信息**。通过在三元组（源图像、目标图像、相机姿态）上提取多尺度扩散特征，并经轻量对比学习微调为紧凑的 L2 归一化嵌入，PRISM 同时支持两种互补的评估模式：

- **DPRISM**（全参考）：度量预测三元组与真实三元组嵌入之间的距离；
- **MMDPRISM**（无参考）：计算生成图像集与锚定真实图像集嵌入间的最大均值差异（MMD）。

为训练和验证该框架，作者构建了 **VIEWMATCH** 数据集，通过可见性掩码与修复技术生成保持/破坏视角一致性的正负样本对。

主要实验结果确立了 PRISM 的有效性：

| 证据维度   | 核心发现                                                                 | 锚点                |
| ------ | -------------------------------------------------------------------- | ----------------- |
| 特征判别力  | 原始扩散特征在 VIEWMATCH 上的线性分类 AUC 达 0.90，远超 CLIP（0.73）和 DINOv2（0.68）      | Table 1           |
| 无参考敏感性 | MMDPRISM 明确区分正样本（0.691）与负样本（0.984），而 FID 等分布指标几乎平坦（102.36 vs 107.24） | Table 2           |
| 人类判断对齐 | DPRISM 在图像质量维度上与人类偏好的 Pearson 相关系数为 0.394，而 PSNR 为 -0.323            | Table 3           |
| 模型排名   | 在 Toys4K、GSO、OmniObject3D 三个数据集上，MMDPRISM 给出清晰且一致的 NVS 模型排名，无模型偏向性   | Table 4, 5, 9, 10 |

消融实验进一步揭示：扩散时间步 $t=0$（即干净图像输入）的特征判别力最强（AUC 0.90），随噪声步数增加而单调下降至 $t=999$ 的 0.66；DPRISM 对高斯模糊、色调偏移、噪声等常见退化保持单调敏感性；MMDPRISM 对视角偏移呈现 M 形响应曲线，与全参考指标趋势一致，而无参考基线几乎平坦。

**方法定位**：PRISM 并非提出新的 NVS 生成模型，而是为 NVS 领域提供一套通用的评估基础设施。其设计具有模块化特征——特征提取骨干可替换为其他 NVS 基础模型，投影头可针对不同骨干重新训练。当前局限在于仅验证于物体级单视角设定，且依赖 Zero123-XL 作为特征提取器；向场景级、多视角及真实拍摄场景的扩展是重要的开放问题。

新视角合成（Novel View Synthesis, NVS）旨在从有限观测中重建三维场景的任意视角图像，其评估长期以来依赖于PSNR、SSIM、LPIPS等通用图像质量指标。然而，这些指标的设计初衷并非面向NVS这一特定任务，其根本性缺陷在于：它们仅度量生成图像与单一参考图像之间的像素级或特征级差异，完全忽略了NVS任务中**源图像、目标视角与生成结果之间不可分割的三元关系**。

这一结构性盲区导致了两类典型的评估失效。其一，标准指标常对合理的生成变化施加错误惩罚——当生成视角与参考视角存在合理的光照变化、遮挡关系调整或纹理细节差异时，PSNR等指标会给出较低的评分，尽管生成结果在几何和语义上完全正确。其二，这些指标对视角一致性的破坏缺乏敏感性——当生成结果出现严重的几何畸变或语义错误时，标准指标可能因局部纹理匹配而给出虚高的分数。如**Figure 1**所示，PSNR、SSIM、LPIPS、CLIP-S等指标在多组对比中均偏向了明显错误的生成结果，而本文提出的DPRISM则准确惩罚了这些错误输出。

从更宏观的视角看，现有NVS评估体系存在三个层面的缺失：

1. **任务感知缺失**：通用指标未将相机姿态变换作为评估条件，无法区分“因视角变化导致的合理差异”与“因模型能力不足导致的生成错误”。
2. **三元关系缺失**：评估应同时考虑源图像、目标视角和生成结果三者的联合一致性，而非仅比较生成结果与真值的逐像素距离。
3. **分布级评估缺失**：无参考场景下，FID、CMMD等分布度量仅比较生成集与真实集的整体统计特征，对视角偏移、几何畸变等NVS特有退化模式几乎无响应。

为填补上述缺口，本文提出PRISM（Perceptual Reference-based Image Synthesis Metric）评估框架。该框架的核心洞察在于：**扩散式NVS基础模型（如Zero123）的中间层特征天然编码了与视角相关的几何和外观信息**，通过对比学习将这些特征精炼为紧凑的L2归一化嵌入，可同时支持全参考（DPRISM）和无参考（MMDPRISM）两种评估模式。这一设计使得评估指标能够感知源-目标-姿态三元组的内在一致性，从而在模型排名、人类判断对齐和退化敏感性等关键维度上显著超越现有基线。

## 核心方法与创新机理

### 1. 从通用视觉特征到NVS扩散模型特征：重新定义评估骨干

现有NVS评估指标普遍依赖通用视觉特征提取器，如CLIP（Hila et al., 2021）或DINOv2，这些特征虽然具备一定的语义感知能力，但**完全忽略了源图像、目标视角与生成结果之间的三元几何关系**。这使得它们难以区分“合理的视角变化”与“违反多视角一致性的错误生成”——例如，PSNR可能对纹理偏移过度敏感，而FID（Heusel et al., NeurIPS 2017）则对视角偏移几乎不响应。

本工作的核心洞察在于：**扩散模型在去噪过程中天然编码了与视角相关的几何和外观信息**。具体而言，PRISM框架使用Zero123作为特征提取骨干，将源图像、目标图像和相机位姿构成的三元组输入扩散U-Net，在去噪早期（t=0）提取多尺度中间层激活。这些激活图经过逐像素L2归一化和空间平均池化后拼接为全局特征向量，再通过一个轻量两层ReLU MLP投影至2048维L2归一化嵌入空间，最终形成 $f_{\mathrm{PRISM}}(I_{\mathrm{src}}, I_{\mathrm{tgt}}, \pi)$。

这一设计的关键证据来自VIEWMATCH数据集上的线性分类实验：原始扩散特征（t=0）在区分正样本（视角一致的生成）和负样本（视角不一致的生成）时，AUC达到**0.90**，显著优于CLIP-CAT-Angle（0.73）和DINO-CAT-Angle（0.68）（Table 1, right）。这表明扩散模型中间层已经蕴含了强判别性的视角一致性信息，仅需轻量微调即可释放其评估潜力。

### 2. 从单一评估范式到三元组感知的双模评估框架

传统评估指标在范式上存在根本性局限：全参考指标（如PSNR、SSIM、LPIPS（Zhang et al., CVPR 2018））要求生成图像与真实目标图像逐像素或逐块配对，但NVS任务中**真实目标图像在推理时通常不可得**；无参考分布指标（如FID、CMMD（Jayasumana et al., 2024））则完全丢弃了源图像和位姿信息，仅比较生成集与真实集的全局分布，无法感知单次生成的视角一致性。

PRISM通过**三元组感知嵌入**统一了两种评估模式：

- **全参考模式（DPRISM）**：计算预测三元组嵌入与真实三元组嵌入的L2距离并归一化至[0,1]：
  $$\mathrm{D}_{\mathrm{PRISM}} = \frac{1}{2} \left\| f_{\mathrm{PRISM}}(I_{\mathrm{src}}, \tilde{I}_{\mathrm{tgt}}, \pi) - f_{\mathrm{PRISM}}(I_{\mathrm{src}}, I_{\mathrm{tgt}}, \pi) \right\|_2$$
  该度量仅在真实目标可用时使用，直接衡量生成结果在给定源和位姿条件下的偏离程度。

- **无参考模式（MMDPRISM）**：计算生成三元组集合 $\mathcal{F}_{\mathrm{gen}}$ 与锚定真实三元组集合 $\mathcal{F}_{\mathrm{anch}}$ 的PRISM嵌入之间的最大均值差异（MMD）：
  $$\mathbf{MMD}_{\mathrm{PRISM}} = \mathbf{MMD}(\mathcal{F}_{\mathrm{gen}}, \mathcal{F}_{\mathrm{anch}})$$
  锚定集可从训练数据中预构建，使评估无需目标真值即可进行。

这一双模设计的优势在VIEWMATCH无参考验证中得到充分体现：MMDPRISM对正样本得分为**0.691**，对负样本得分为**0.984**，形成清晰分离；而FID对正负样本的得分分别为102.360和107.240，几乎无法区分（Table 2）。这表明PRISM嵌入空间成功编码了视角一致性信息，使得即使在没有目标真值的情况下，也能通过分布差异有效识别生成质量。

### 3. 从直接特征到对比微调：VIEWMATCH驱动的嵌入精炼

直接使用扩散模型提取的特征虽然已具备一定判别力，但未经任务适配的特征空间并非最优。PRISM的关键创新在于通过**对比三元组微调**将特征精炼为紧凑的评估嵌入。

具体训练流程如下：利用VIEWMATCH数据集构建三元组——锚点（真实目标三元组）、正样本（视角一致的生成或真实目标）、负样本（视角不一致的修复目标或错误位姿下的目标）。通过margin-based三元组损失优化轻量MLP投影头：
$$\mathcal{L}(a,p,n) = \max\left(\|a - p\|_2 - \|a - n\|_2 + m, 0\right)$$
其中margin $m=1$。这一设计有三个关键优势：

1. **仅微调投影头**：冻结扩散模型骨干，仅训练两层MLP，参数量极小，避免了灾难性遗忘和过拟合风险。
2. **负样本多样性**：VIEWMATCH通过可见性掩码、不可见性掩码和极线掩码的组合修复生成负样本，覆盖了几何不一致、纹理错误、形状变化等多种失败模式（Figure 3）。
3. **嵌入紧凑性**：L2归一化嵌入使DPRISM和MMDPRISM的计算仅依赖余弦距离或欧氏距离，无需复杂后处理。

### 4. 创新总结：changed slots 一览

| 设计维度 | 基线方法 | PRISM 方案 | 关键证据 |
|---------|---------|-----------|---------|
| 特征提取骨干 | 通用视觉特征（CLIP, DINOv2） | NVS扩散模型特征（Zero123） | 线性分类AUC: 0.90 vs 0.73 (Table 1) |
| 评估范式 | 忽略视角关系或依赖真值配对 | 三元组感知嵌入，支持全参考和无参考 | MMDPRISM清晰分离正负样本 (Table 2) |
| 特征适应 | 直接使用提取特征 | 对比微调轻量MLP投影头 | DPRISM与人类判断Pearson相关系数: 0.394 (IQ) vs PSNR: -0.323 (Table 3) |

### 5. 局限与开放问题

尽管PRISM在物体级单视角NVS评估上展现出显著优势，其创新仍存在边界：

- **骨干依赖性**：当前实现绑定Zero123-XL，虽框架理论上可迁移至其他NVS扩散模型，但需为每个新骨干重新训练投影头，增加了部署成本。论文未提供跨骨干迁移的实验验证。
- **场景局限性**：评估范围限于物体级单视角NVS，尚未扩展至场景级、多视角或视频NVS设置。在这些更复杂场景中，扩散特征是否仍能编码有效的视角一致性信息有待验证。
- **锚定集开销**：无参考MMDPRISM需要预构建锚定集，其大小和存储开销在大规模部署时可能成为瓶颈。如何进一步压缩锚定集而不损失评估可靠性是实用化方向。
- **真实数据泛化**：VIEWMATCH基于合成渲染数据构建，用户研究虽独立于训练集，但整体评估仍限于渲染域。在真实拍摄图像上的泛化能力未经检验。

PRISM 框架的核心设计理念是：将新视角合成（NVS）的评估建模为对**三元组（源视图、目标视图、相机姿态）**的语义理解问题，而非简单的像素级或分布级比较。如图 Figure 2 所示，整个框架由两个阶段构成：**特征提取流水线**和**双模式评估**。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2511_12675/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. (Left) Feature extraction: given source, target, and camera transformation, we noise the target image and extract features from a diffusion-based NVS model. These are pooled and tuned into fPRISM. (Right) Evaluation framework: Full-Reference: measure distance between fPRISM of a predicted triplet and its ground-truth counterpart. No-Reference: compute MMD between fPRISM from generated triplets and an anchor set of real triplets*

### 2.1 特征提取流水线

给定一个三元组 $(I_{\text{src}}, I_{\text{tgt}}, \pi)$，特征提取过程如下：

1. **目标视图加噪**：将目标视图 $I_{\text{tgt}}$ 编码为潜变量 $z_0$，通过扩散前向过程添加噪声，得到带噪潜变量 $z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$（Eq. 3）。这一操作使模型能在统一的扩散先验空间中处理任意输入。

2. **多尺度特征提取**：以源视图 $I_{\text{src}}$ 和相机姿态 $\pi$ 为条件，对 $z_t$ 执行单步去噪，从 Zero123 的 U-Net 各块提取中间激活图 $F_b = f_{\theta_b}(z_t, t; I_{\text{src}}, \pi) \in \mathbb{R}^{H_b \times W_b \times C_b}$（Eq. 4）。这些多尺度特征天然编码了视角相关的几何和外观信息。

3. **空间池化与拼接**：对每块激活图进行逐像素 L2 归一化后空间平均池化 $v_b = \frac{1}{H_b W_b} \sum_{i,j} \frac{F_b[i,j,:]}{\lVert F_b[i,j,:] \rVert}$（Eq. 5），然后将所有块的特征向量拼接为全局表示 $v = \text{Concat}(v_1, \ldots, v_B) \in \mathbb{R}^C$（Eq. 6）。

4. **投影与归一化**：通过一个轻量级的两层 ReLU MLP 投影头 $h(\cdot)$ 将拼接特征压缩至 2048 维，并进行 L2 归一化，得到最终的 PRISM 嵌入 $f_{\text{PRISM}} = \frac{h(v)}{\lVert h(v) \rVert}$（Eq. 7）。

这一流水线的关键洞察在于：**扩散模型的中间特征天然编码视角相关的几何和外观信息**。Table 1（右）的线性分类实验证实了这一点——原始扩散特征（$t=0$）在 VIEWMATCH 数据集上的线性分类 AUC 达到 0.90，远优于 CLIP（0.73）和 DINOv2（0.68），说明这些特征本身已具备强大的视角一致性判别能力。

### 2.2 对比学习微调

为进一步增强嵌入空间的判别力，PRISM 在 VIEWMATCH 数据集上对投影头进行对比微调。训练采用三元组损失：

$$\mathcal{L}(a,p,n) = \max(\lVert a - p \rVert_2 - \lVert a - n \rVert_2 + m, 0)$$

其中锚点 $a$ 为真实三元组的嵌入，正样本 $p$ 为合理合成视图的嵌入，负样本 $n$ 来自 VIEWMATCH 中通过可见性掩码修复生成的不一致视图，或姿态偏移的错误视角。间隔 $m$ 设为 1。

这一微调步骤是框架的**因果调节旋钮**：它不改变特征提取骨干，仅通过轻量投影头将原始扩散特征精炼为紧凑的 L2 归一化嵌入，使嵌入空间能明确区分合理与不合理的生成结果。

### 2.3 双模式评估

基于 PRISM 嵌入，框架支持两种互补的评估模式：

- **全参考模式（DPRISM）**：计算预测三元组与真实三元组嵌入间的 L2 距离，并归一化至 $[0,1]$：
  $$\mathrm{D}_{\mathrm{PRISM}} = \frac{1}{2} \left\lVert f_{\mathrm{PRISM}}(I_{\mathrm{src}}, \tilde{I}_{\mathrm{tgt}}, \pi) - f_{\mathrm{PRISM}}(I_{\mathrm{src}}, I_{\mathrm{tgt}}, \pi) \right\rVert_2$$
  该指标直接量化生成结果与真值在 PRISM 空间中的偏差。

- **无参考模式（MMDPRISM）**：计算生成三元组集合 $\mathcal{F}_{\text{gen}}$ 与锚定真实三元组集合 $\mathcal{F}_{\text{anch}}$ 的 PRISM 嵌入间的最大均值差异（MMD）：
  $$\mathbf{MMD}_{\mathrm{PRISM}} = \mathbf{MMD}(\mathcal{F}_{\text{gen}}, \mathcal{F}_{\text{anch}})$$
  该指标无需逐样本真值配对，适用于只有生成结果集的场景。

两种模式共享同一嵌入空间，形成了从逐样本精确评估到集合级分布评估的完整能力谱系。

### 整体流水线

PRISM 框架的核心是将一个 NVS 三元组（源图像 $I_{\mathrm{src}}$、目标图像 $I_{\mathrm{tgt}}$、相机位姿变换 $\pi$）编码为一个紧凑的 L2 归一化嵌入向量 $f_{\mathrm{PRISM}}$，使该嵌入空间能够区分合理与不合理的生成结果。整个流水线包含五个关键模块：

1. **扩散特征提取**：利用 NVS 基础模型 Zero123 的 U-Net 作为特征骨干，对带噪目标视图执行单步去噪，提取各块的中间激活图。
2. **空间池化与拼接**：对激活图进行逐像素 L2 归一化后空间平均池化，拼接为全局特征向量。
3. **轻量 MLP 投影**：通过两层 ReLU MLP 将原始特征压缩至 2048 维，并 L2 归一化为最终 PRISM 嵌入。
4. **对比三元组训练**：基于 VIEWMATCH 数据集，使用三元组损失微调投影头。
5. **双模式评估**：全参考模式（DPRISM）计算预测三元组与真值三元组嵌入间的距离；无参考模式（MMDPRISM）计算生成集与锚定集嵌入间的最大均值差异。

### 关键公式与变量含义

#### 扩散前向过程

$$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$$

其中 $z_0$ 为干净潜变量，$\bar{\alpha}_t$ 为噪声调度参数，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。该式定义了向目标视图潜变量逐步添加噪声的过程。

#### U-Net 块激活提取

$$F_b = f_{\theta_b}(z_t, t; I_{\mathrm{src}}, \pi) \in \mathbb{R}^{H_b \times W_b \times C_b}$$

对带噪目标视图 $z_t$ 执行单步去噪，以源图像 $I_{\mathrm{src}}$ 和相机位姿 $\pi$ 为条件，提取 U-Net 第 $b$ 个块的中间激活图 $F_b$，其空间维度为 $H_b \times W_b$，通道数为 $C_b$。

#### 空间池化

$$v_b = \frac{1}{H_b W_b} \sum_{i,j} \frac{F_b[i,j,:]}{\lVert F_b[i,j,:] \rVert}$$

先对每个空间位置的通道向量进行 L2 归一化，再进行空间平均池化，得到第 $b$ 块的特征向量 $v_b$。

#### 特征拼接

$$v = \mathrm{Concat}(v_1, \ldots, v_B) \in \mathbb{R}^C$$

将所有 $B$ 个块的特征向量拼接为全局表示 $v$，总维度 $C = \sum_{b=1}^B C_b$。

#### PRISM 嵌入

$$f_{\mathrm{PRISM}} = \frac{h(v)}{\lVert h(v) \rVert}$$

其中 $h(\cdot)$ 为两层 ReLU MLP 投影头，输出经 L2 归一化后得到最终 PRISM 嵌入。该嵌入位于单位超球面上，便于余弦距离计算。

#### 对比三元组损失

$$\mathcal{L}(a,p,n) = \max(\lVert a - p \rVert_2 - \lVert a - n \rVert_2 + m, 0)$$

其中 $a$ 为锚点嵌入（真值三元组），$p$ 为正样本嵌入（合理生成），$n$ 为负样本嵌入（不合理生成），margin $m=1$。该损失迫使锚点与正样本的距离比与负样本的距离至少小 $m$。

#### 全参考度量：DPRISM 距离

$$\mathrm{D}_{\mathrm{PRISM}} = \frac{1}{2} \left\| f_{\mathrm{PRISM}}(I_{\mathrm{src}}, \tilde{I}_{\mathrm{tgt}}, \pi) - f_{\mathrm{PRISM}}(I_{\mathrm{src}}, I_{\mathrm{tgt}}, \pi) \right\|_2$$

其中 $\tilde{I}_{\mathrm{tgt}}$ 为模型生成的预测目标视图，$I_{\mathrm{tgt}}$ 为真实目标视图。该式计算预测三元组与真值三元组 PRISM 嵌入间的 L2 距离，并归一化至 $[0,1]$。由于嵌入已 L2 归一化，该距离等价于余弦距离的一半。

#### 无参考度量：MMDPRISM

$$\mathbf{MMD}_{\mathrm{PRISM}} = \mathbf{MMD}(\mathcal{F}_{\mathrm{gen}}, \mathcal{F}_{\mathrm{anch}})$$

其中 $\mathcal{F}_{\mathrm{gen}}$ 为生成三元组的 PRISM 嵌入集合，$\mathcal{F}_{\mathrm{anch}}$ 为锚定真实三元组的嵌入集合。MMD 的具体计算基于核嵌入分布差异：

$$d_{\mathrm{MMD}}^2(P,Q) = \mathbb{E}_{x,x'\sim P}[k(x,x')] + \mathbb{E}_{y,y'\sim Q}[k(y,y')] - 2\mathbb{E}_{x\sim P, y\sim Q}[k(x,y)]$$

该度量无需逐样本真值配对，仅通过比较生成分布与真实分布的嵌入统计差异来评估整体质量。

### 模块间因果依赖

特征提取骨干的选择是整个框架的**核心因果旋钮**：原始扩散特征在 VIEWMATCH 上的线性分类 AUC 达到 0.90，远优于 CLIP（0.73）和 DINOv2（0.68），这表明扩散模型的中间特征天然编码了视角相关的几何和外观信息。对比微调投影头进一步将这些特征精炼为紧凑嵌入，使 DPRISM 和 MMDPRISM 均能有效捕捉标准指标（PSNR、SSIM、LPIPS）无法区分的视角一致性问题。

## 实验与关键发现

### 核心实验设置

PRISM框架的评估围绕三个层次展开：**(1) 点级区分能力**——在VIEWMATCH数据集上验证指标能否区分合理与不合理的生成三元组；**(2) 分布级无参考验证**——检验MMDPRISM在无真值条件下能否分离正负样本集；**(3) 人类判断对齐**——通过用户研究衡量指标与人类偏好的相关性。评估涵盖多类NVS模型，包括基于扩散的Zero123-XL、回归式OpenLRM、多视图聚合SyncDreamer等（Table 8），确保排名实验覆盖不同技术范式。

---

### 点级区分能力：标准指标为何失败

Table 1（左）揭示了传统全参考指标的致命缺陷：在正样本（保持视角一致性）和负样本（引入语义/几何错误）上，PSNR、SSIM、LPIPS、CLIP-S等指标的得分几乎无法区分。以PSNR为例，正样本均值18.18 dB，负样本均值18.69 dB——负样本反而略高，说明PSNR将合理的视角变化误判为失真。这一现象的根本原因在于：标准指标仅比较像素或特征层面的图像相似度，完全忽略了源图像、目标视角与生成结果之间的三元几何约束。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2511_12675/figures/005_Table_1.jpg]]
*Table 1: Comparison of standard metrics and linear classifiers on VIEWMATCH. Left: average scores for pointwise evaluation metrics on positive (P) and negative (N) samples. Right: AUC scores for linear classifiers trained to distinguish positive from negative triplets*

Table 1（右）的线性分类器实验进一步验证了特征空间的判别力。从Zero123扩散模型提取的原始特征（t=0时间步）无需任何微调，仅训练线性分类器即可达到**AUC 0.90**，远超CLIP特征（0.73）和DINOv2特征（0.68）的同类设置。这表明扩散模型的中间激活天然编码了视角相关的几何和外观信息，为后续PRISM嵌入的精炼提供了高质量起点。

---

### 无参考验证：MMDPRISM的分布级分离

Table 2展示了无参考评估的核心结果。MMDPRISM在正样本集上得分为**0.691**，负样本集上为**0.984**，形成清晰分离。相比之下，FID（102.360 vs 107.240）、CMMD等传统分布指标在正负样本集间几乎持平，无法提供有意义的区分信号。即使引入源图像作为联合分布参考的JFID和JCMMD，分离度也远不及MMDPRISM。

这一差异的因果机制在于：FID等指标基于Inception或CLIP特征空间计算分布距离，这些特征空间未针对NVS任务中的视角一致性进行优化；而MMDPRISM使用经过对比三元组微调的PRISM嵌入，其L2归一化空间明确编码了“源-目标-姿态”的三元关系，因此对生成结果是否违反视角一致性高度敏感。

---

### 人类判断对齐：DPRISM的感知相关性

用户研究在GSO数据集的40个物体上进行，参与者从四个维度评估生成视图：**视角准确性（VP）**、**共享区域一致性（SC）**、**新区域合理性（PL）** 和**图像质量（IQ）**。Table 3汇报了各指标预测与人类判断的Pearson相关系数。

DPRISM在所有四个维度上均取得正向相关性，其中图像质量（IQ）维度达到**0.394**，位列所有指标之首。相比之下，PSNR在IQ维度上出现**-0.323**的负相关——即PSNR认为更好的图像，人类反而认为更差。LPIPS在IQ上仅为-0.071，同样无法捕捉人类的质量感知。在共享区域一致性（SC）维度，DPRISM的0.352也显著优于MEt3R（0.239）和LPIPS（0.207）。

Figure 13的定性案例进一步印证了这一趋势：当生成视图在新区域出现几何扭曲或语义不一致时，PSNR、SSIM、LPIPS、CLIP-S等指标常错误地偏好这些不正确输出，而DPRISM始终与人类偏好保持一致。这归因于PRISM嵌入在对比训练中学习到的判别特征——它惩罚的是违反视角一致性的语义和几何错误，而非像素级差异。

---

### NVS模型排名：无参考评估的实用性

Table 4和Table 5展示了MMDPRISM在Toys4K、GSO、OmniObject3D三个数据集上的模型排名能力。以Toys4K为例（Table 4），MMDPRISM给出SEVA最低分**0.1978**（最优），Zero123-XL为0.2693，OpenLRM为0.8017，形成清晰的性能梯度。而FID将所有模型压缩在156.2至193.7的狭窄区间内，难以区分中游模型；CMMD和FDD同样缺乏区分度。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2511_12675/figures/009_Table_4.jpg]]
*Table 4: Toys4K benchmark. Comparison of reference-free metrics for ranking NVS models. Lower is better*

值得注意的是，尽管PRISM的特征提取骨干基于Zero123-XL，但排名结果并未偏向Zero123系列——SEVA和SyncDreamer在多个数据集上优于Zero123-XL，证明了评估框架的无偏性。这一特性源于对比训练的目标是学习“什么是好的NVS输出”而非“哪个模型生成了该输出”。

---

### 消融与敏感性分析

**扩散时间步的影响**（Table 7）：线性分类器AUC在t=0时达到峰值0.90，随扩散步数增加而单调下降（t=999时降至0.66）。这表明早期去噪阶段的特征包含最强的视角一致性判别信息，因为此时U-Net主要依赖条件信号（源图像和姿态）来预测目标视图的结构。

**感知质量退化敏感性**（Figure 5, 9–11）：DPRISM对高斯模糊、色调偏移、高斯噪声和椒盐噪声均表现出单调递增的响应曲线——退化强度越大，DPRISM距离越大。这验证了PRISM嵌入保持了感知质量敏感性，不会因特征空间的语义压缩而丢失对低层退化的检测能力。

**视角偏移响应**（Figure 6, Figure 12）：MMDPRISM随方位角偏移呈现**M形曲线**，在0°和360°处达到最低（完美对齐），在180°附近出现次低点（对向视角），在90°和270°附近达到峰值。这一模式与全参考指标（PSNR等）的响应趋势一致，而FID、JFID等无参考基线几乎保持平坦——它们无法感知视角偏移带来的分布变化。

---

### 失败模式与局限性

1. **骨干依赖性**：当前PRISM完全基于Zero123-XL提取特征。虽然框架设计上可迁移至其他NVS扩散模型，但缺乏实验验证。不同骨干的中间特征分布差异可能导致投影头需要重新训练，增加部署成本。

2. **场景级扩展未验证**：所有实验均在物体级单视角设置下进行。对于场景级NVS或多视角聚合评估，PRISM嵌入是否仍能保持相同的判别力和人类对齐度，尚需进一步研究。

3. **真实图像泛化未知**：VIEWMATCH和评估数据集均基于合成渲染。在真实拍摄图像（存在光照变化、遮挡、传感器噪声等）上的性能未经检验，这一点的验证需要手动收集真实多视角数据集。

4. **锚定集存储开销**：MMDPRISM需要维护真实三元组的锚定嵌入集。虽然当前实验表明中等规模锚定集即可提供稳定估计，但在大规模部署场景下的存储和计算优化仍需探索。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2511_12675/figures/006_Table_2.jpg]]
*Table 2: No-reference validation on VIEWMATCH. Lower is better*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2511_12675/figures/020_Table_9.jpg]]
*Table 9: Ranking on GSO dataset. Comparison of reference-free metrics for ranking NVS models. Lower is better*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2511_12675/figures/021_Table_10.jpg]]
*Table 10: Ranking on OmniObject3D dataset. Comparison of erence-free metrics for NVS models. Lower is better*

## 定位与知识库关联

### 1. 基线谱系与核心差异

PRISM 的提出根植于对现有评估范式系统性缺陷的诊断。传统指标可沿两条轴线分类：**全参考（Full-Reference）** 与 **无参考（Reference-Free）**，以及 **逐点（Pointwise）** 与 **分布（Distributional）**。PRISM 在两个维度上均实现了范式跃迁。

**全参考基线**方面，PSNR 与 **SSIM**（Wang et al., 2004）作为经典信号保真度指标，在 VIEWMATCH 上对正负样本几乎无区分力——PSNR 在正样本上为 18.18，负样本上为 18.69，甚至出现负样本得分更高的倒挂现象（Table 1 左栏）。**LPIPS**（Zhang et al., CVPR 2018）作为深度感知度量虽有改进，但正负样本差距仅 0.015（0.163 vs 0.178），远不足以支撑可靠决策。CLIP-S（Hila et al., 2021）将语义相似度引入评估，但 CLIP 特征本身缺乏视角几何编码能力，其线性分类 AUC 仅为 0.73，与扩散特征的 0.90 存在显著差距（Table 1 右栏）。MEt3R 等多视角一致性度量同样未能捕捉三元组内的因果依赖。

**无参考基线**方面，**FID**（Heusel et al., NeurIPS 2017）和 **CMMD**（Jayasumana et al., 2024）等分布度量在 VIEWMATCH 上完全失效：FID 对正样本集为 102.360，对负样本集为 107.240，差值仅约 5 个点，无法提供有意义的区分信号（Table 2）。JFID/JCMMD/JFDD 等联合源-目标分布度量虽试图引入源图像信息，但在视角偏移实验中仍呈平坦响应，未能反映视角变化对生成质量的影响（Figure 6）。

PRISM 的核心差异体现在三个**关键设计槽位**的替换：

| 设计槽位 | 基线方案 | PRISM 方案 | 证据锚点 |
|---------|---------|-----------|---------|
| 特征提取骨干 | 通用视觉特征（CLIP, DINOv2） | NVS 扩散模型特征（Zero123） | Section 3.1, Table 1 |
| 评估范式 | 忽略视角关系或依赖真值配对 | 三元组感知嵌入，支持全参考和无参考双模式 | Section 3, Eq. (1)-(2) |
| 特征适应 | 直接使用提取特征 | 对比微调轻量 MLP 投影头 | Section 3.3, Eq. (7)-(8) |

### 2. 方法谱系中的定位

PRISM 在知识谱系上横跨三个领域，形成了独特的交叉定位：

**扩散模型表征学习**。PRISM 的核心洞察——扩散 U-Net 中间层特征天然编码视角相关的几何与外观信息——与近期利用扩散特征进行语义分割、对应匹配等下游任务的工作一脉相承。但 PRISM 首次将这些特征系统性地迁移至 NVS 评估场景，并证明在去噪时间步 $t=0$（即无噪声输入）时提取的特征具有最强的判别力（AUC 0.90），随 $t$ 增加至 999 时 AUC 降至 0.66（Table 7）。这一发现揭示了早期去噪阶段特征对视角一致性的敏感编码。

**对比度量学习**。PRISM 的投影头训练采用标准三元组损失（margin $m=1$），但与通用对比学习工作不同，其训练数据来自专为 NVS 评估构建的 VIEWMATCH 数据集。该数据集通过可见性掩码、不可见性掩码与极线掩码的组合，利用修复模型生成保留结构一致性（正样本）或引入几何/外观冲突（负样本）的合成目标视图（Figure 3），从而将评估知识注入嵌入空间。

**生成模型评估**。在评估范式层面，DPRISM 的全参考模式可视为将传统逐点距离度量（如 LPIPS）推广至三元组空间——不仅比较图像对，还显式编码了源-目标-姿态的因果结构。MMDPRISM 的无参考模式则继承了 FID/CMMD 的分布比较思想，但将特征空间从通用视觉特征替换为任务感知的 PRISM 嵌入，从而获得了对视角变化的敏感性（Figure 6 中的 M 形响应曲线）。

### 3. 适用边界与局限

PRISM 的适用边界由以下约束定义：

**骨干依赖**。当前实现绑定于 Zero123-XL 作为特征提取器。虽然框架设计上可迁移至其他 NVS 扩散模型（如基于 DiT 架构的模型或回归式模型），但论文未进行跨骨干验证。更换骨干需要重新训练投影头，增加了部署成本。这一依赖也意味着 PRISM 的性能上限受限于所选骨干对 NVS 任务的表征质量。

**任务范围**。VIEWMATCH 数据集和所有实验均聚焦于**物体级单视角新视角合成**——即给定单张源图像和目标相机姿态，生成新视角下的物体外观。PRISM 尚未扩展至：(1) 场景级 NVS（如室内/室外大场景的自由视角渲染）；(2) 多视角条件 NVS（输入多张源图像）；(3) 视频 NVS（时态一致的新视角序列）。在这些设置下，源-目标-姿态三元组的定义需要重新设计。

**数据域限制**。实验所用数据集（GSO、OmniObject3D、Toys4K）均为合成渲染的 3D 物体，具有完美的几何和光照一致性。在真实环境捕获的图像（如手持拍摄、非受控光照、背景杂乱）上，PRISM 的泛化能力未经检验。VIEWMATCH 的负样本生成依赖修复模型，其合成伪影可能与真实 NVS 模型的失败模式存在分布差异。

**用户研究规模**。人类判断对齐实验涉及 40 名参与者、500 余次比较，样本量适中。四个评估维度（视角准确性 VP、共享区域一致性 SC、新区域合理性 PL、图像质量 IQ）中，DPRISM 在 IQ 上表现最强（Pearson $r=0.394$），在 PL 上相对较弱（$r=0.205$），这可能反映嵌入空间对纹理/几何冲突的敏感度高于对语义合理性的判断。

### 4. 开放问题

以下问题指向 PRISM 框架的下一步演进方向，目前均缺乏实验证据支持：

1. **跨骨干泛化**：PRISM 嵌入是否可迁移至其他 NVS 骨干（如基于回归的模型、基于 DiT 的扩散模型）而不大幅牺牲性能？投影头重训练的成本与数据需求如何？

2. **场景级与多视角扩展**：如何将三元组定义从单源图像推广至多源图像条件？场景级 NVS 中，源-目标视角可能跨越极大的基线距离，此时扩散特征的判别力是否依然保持？

3. **真实域迁移**：在非合成数据集（如真实拍摄的物体或场景）上，PRISM 能否保持相同的敏感性和可靠性？VIEWMATCH 式合成数据的训练策略是否需要域适应补充？

4. **训练过程集成**：PRISM 嵌入是否可作为 NVS 模型训练中的可微分损失或自适应学习信号？这需要验证嵌入空间在训练动态中的稳定性。

5. **锚定集效率**：MMDPRISM 的无参考评估依赖锚定真实图像集的 PRISM 嵌入。如何最小化锚定集的大小和存储开销，同时保持排名可靠性？当前实验中锚定集的规模与选择策略需进一步优化。

## 原文 PDF

![[paperPDFs/3DV_2026/Appreciate_the_View_A_Task_Aware_Evaluation_Framework_for_Novel_View_Synthesis.pdf]]

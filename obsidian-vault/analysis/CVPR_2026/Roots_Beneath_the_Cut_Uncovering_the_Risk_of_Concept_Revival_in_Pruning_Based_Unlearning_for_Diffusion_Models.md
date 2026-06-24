---
title: "Roots Beneath the Cut: Uncovering the Risk of Concept Revival in Pruning-Based Unlearning for Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Roots_Beneath_the_Cut_Uncovering_the_Risk_of_Concept_Revival_in_Pruning_Based_Unlearning_for_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/Brankozz/Roots-Beneath-the-Cut"
aliases:
- RBCURCRPBUDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 剪枝权重的正负号（Sign）是概念恢复的主要因果杠杆：准确恢复符号（即使幅度不精确）就能大幅复活被擦除的概念；通过矩阵补全近似恢复权重符号，并保留高置信度的Top-K符号，再以神经元最大幅值缩放，即可成功发起概念复活攻击。
primary_logic: 权重符号的正确性远大于权重大小的重要性；低秩矩阵补全虽不能完美重建幅度，却能以高准确率恢复大部分符号，使得在无数据、无训练的设定下，攻击者能够用极简的后续步骤复活被概念剪枝擦除的内容。
claims:
- 攻击框架恢复了超过70%的剪枝权重符号，并在七分钟内将擦除概念的平均分类准确率从约8%提升至54%，整个过程无需任何数据或重训练。
- 在理想实验中，即使仅恢复符号并随机赋值幅度，也比恢复幅度而随机符号更能复活概念；神经元最大缩放策略在所有对比幅度赋值策略中取得最佳复活性能。
- ImageNet subset (12 classes) 上 Top-1 Accuracy (Erased Class) = 0.54
- ImageNet subset (12 classes) 上 Top-1 Accuracy (Preserved Class) = 0.91
---

# Roots Beneath the Cut: Uncovering the Risk of Concept Revival in Pruning-Based Unlearning for Diffusion Models

> [!tip] 核心洞察
> 权重符号的正确性远大于权重大小的重要性；低秩矩阵补全虽不能完美重建幅度，却能以高准确率恢复大部分符号，使得在无数据、无训练的设定下，攻击者能够用极简的后续步骤复活被概念剪枝擦除的内容。

| 字段 | 内容 |
|------|------|
| 中文题名 | 剪枝之下的根：揭示基于剪枝的扩散模型遗忘中概念复苏的风险 |
| 英文题名 | Roots Beneath the Cut: Uncovering the Risk of Concept Revival in Pruning-Based Unlearning for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.06640) · [Code](https://github.com/Brankozz/Roots-Beneath-the-Cut) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NMS Attack Framework (Low-rank Matrix Completion + Top-K Sign Retention + Neuron-Max Scaling) |
| Dataset | ImageNet subset, Artist style unlearning, COCO-30K, NSFW unlearning |

> [!tip] 效果简介
> - ImageNet subset (12 classes) 上，Top-1 Accuracy (Erased Class) 0.54 vs 0.08 (+0.46)；Top-1 Accuracy (Preserved Class) 0.91 vs — (—)。
> - Artist style unlearning (5 artists) 上，CLIP similarity (Artist style) 0.30 (NMS average) vs 0.25 (Concept Prune) / 0.31 (SD-v1.5) (relative increase vs Concept Prune)。
> - COCO-30K 上，FID 18.93 (NMS average) vs 21.45 (Concept Prune) / 18.4 (SD-v1.5) (improvement vs Concept Prune)。

## 概述

扩散模型剪枝遗忘方法通过将概念相关权重置零来擦除目标概念，但这一过程在权重空间中留下了精确的剪枝位置信息。本文揭示了一个根本性风险：**剪枝位置本身构成了可被利用的侧信道**，泄露了被遗忘概念的关键参数分布信息。攻击者无需任何训练数据或模型重训练，仅凭剪枝权重的符号信息即可有效复活被擦除的视觉概念。

核心发现是**权重符号的正确性远大于权重大小的重要性**。在理想实验中，仅恢复符号并随机赋值幅度，其概念复活效果远优于恢复幅度而随机赋值符号。基于这一洞察，本文提出了**NMS攻击框架**，通过三个模块实现高效的概念复活：

- **低秩矩阵补全**：利用SoftImpute算法从剪枝后的权重矩阵中近似重建权重符号，为后续步骤提供高质量的符号估计。
- **Top-K符号保留**：根据重构权重的幅度选择保留高置信度的Top-K符号，滤除低置信噪声。
- **神经元最大缩放**：对保留符号的权重赋予其所在神经元剩余连接的最大幅度，放大关键激活模式以最大化复活效果。

在防御侧，本文提出了**高斯模糊防御**：用零均值高斯噪声替换剪枝的零权重，隐藏剪枝位置痕迹，从而在遗忘效果与抗攻击能力之间建立可控的权衡。

实验结果表明，NMS攻击在**七分钟内**将被擦除概念的平均分类准确率从约**8%恢复至54%**，同时成功恢复了超过**70%的剪枝权重符号**。该攻击对多种基于权重定位的遗忘方法（ConceptPrune、Scissorhands、SalUn）均表现出泛化有效性，覆盖物体擦除、艺术风格遗忘和NSFW内容过滤等场景。高斯模糊防御则通过调节方差参数σM，在维持遗忘效果的同时显著降低了攻击成功率。

## 背景与动机

### 扩散模型的概念遗忘与剪枝路径

随着扩散模型在文本到图像生成中的大规模部署，移除模型中受版权保护的艺术风格、不安全的视觉内容或特定物体概念的需求日益迫切。机器遗忘（machine unlearning）为此提供了一条技术路径，其目标是在不重新训练整个模型的前提下，定向擦除目标概念的知识。在众多遗忘方法中，基于权重剪枝的策略因其简洁性和高效性而受到关注：这类方法首先定位与目标概念强相关的模型权重，随后将这些权重直接置零，从而阻断概念的表达通路。

然而，剪枝遗忘在“擦除”概念时，是否真正实现了安全的遗忘？剪枝操作在权重空间中留下了不可忽视的痕迹——被置零的位置本身构成了一个二值掩码，精确标记了哪些参数曾与目标概念深度绑定。这一侧信道信号的存在，意味着攻击者有可能利用剪枝位置信息，逆向推断甚至恢复已被擦除的概念知识。

### 现有方法的缺口

当前针对扩散模型遗忘的攻击研究尚处于早期阶段。已有的训练无关攻击方法（如 **Quant Recover**）试图通过权重量化重建来恢复被遗忘的概念，但其恢复能力有限，且未系统性地利用剪枝掩码所泄露的结构信息。另一方面，遗忘方法的设计者通常仅关注遗忘效果（即目标概念是否被成功抑制），而忽略了剪枝位置本身可能构成的安全脆弱性。这一攻防视角的缺失，使得剪枝遗忘在实际部署中面临被“概念复活”（concept revival）的潜在风险。

### 本文的核心动机

本文旨在揭示剪枝遗忘中这一被忽视的根本脆弱性：**剪枝权重的位置信息本身就是一个强大的侧信道，可被攻击者利用来复活被擦除的概念**。我们提出一个系统性的攻击框架，在不依赖任何训练数据、不进行模型重训练的条件下，仅通过分析剪枝掩码的结构，即可有效恢复被遗忘的概念表达。同时，我们也探索了相应的防御策略，以期为安全的机器遗忘提供更全面的理解。

## 核心创新

本文的核心创新在于**首次揭示并系统性地利用了剪枝遗忘中权重位置泄露这一根本脆弱性**，并围绕该发现构建了一套完整的攻击与防御框架。相较于现有工作仅关注遗忘效果本身，本文从攻击者视角重新审视了剪枝遗忘的安全性，提出了三个关键的 changed slots：

### 1. 从“置零遗忘”到“符号复活”：剪枝权重恢复策略

**Baseline 状态**：现有剪枝遗忘方法（如 ConceptPrune、Scissorhands、SalUn）通过将概念相关权重精确置零来擦除目标概念。这些零值位置被视为“已删除”信息，模型对外表现为遗忘成功。

**核心发现**：权重置零的位置本身构成了一个**侧信道**（side channel），泄露了被遗忘概念的关键参数分布信息。具体而言，剪枝掩码精确标记了哪些权重对目标概念至关重要，攻击者可以利用这一位置信息重建被擦除的概念。

**创新机制**：本文提出的 NMS 攻击框架通过三个模块化的步骤实现无数据、无训练的概念复活：

- **低秩矩阵补全（Low-rank Matrix Completion）**：利用 SoftImpute 算法（公式 1-3），以核范数正则化从剩余的未剪枝权重中估计被置零权重的近似值。关键洞察在于，矩阵补全虽不能完美重建权重的精确幅度，却能以超过 70% 的准确率恢复权重符号（sign），而符号正是概念复活的核心因果杠杆。
- **Top-K 符号保留（Top-K Sign Retention）**：根据重构权重的幅度大小，仅保留 K 个最大幅度权重对应的符号，其余置零。这一步骤有效滤除了矩阵补全引入的低置信度噪声符号，实验表明最优 K 值通常在 0.6 附近。
- **神经元最大缩放（Neuron-Max Scaling）**：对保留符号的权重，赋予其所在神经元剩余连接中的最大幅度值。这一策略在所有对比的幅度赋值方式（随机幅度、神经元均值、神经元采样）中取得了最佳的复活性能，验证了“权重符号的正确性远大于权重大小的重要性”这一核心洞察。

### 2. 因果机制的实证验证：符号 vs. 幅度的非对称重要性

本文通过精心设计的理想实验（Figure 2）揭示了概念复活中的因果杠杆：

- **精确符号 + 随机幅度** 的组合能够大幅复活被擦除概念，而 **精确幅度 + 随机符号** 则几乎无法恢复概念。
- 这一发现表明，**剪枝权重的正负号是概念恢复的主要因果控制变量**——准确恢复符号（即使幅度不精确）就能有效复活被擦除的视觉概念。

该因果分析为攻击框架的设计提供了理论支撑，解释了为何低秩矩阵补全（擅长恢复符号但幅度不精确）配合 Top-K 符号保留和神经元最大缩放能够取得显著攻击效果。

### 3. 防御机制：高斯模糊重写剪枝足迹

**Baseline 状态**：剪枝遗忘方法直接将权重置零，暴露了清晰的剪枝位置信息。

**创新防御**：本文提出用零均值高斯噪声 $\mathcal{N}(0, \sigma_M^2)$ 填充被剪枝的权重位置，以隐藏剪枝足迹。该防御的核心权衡通过公式 (7) 量化：

$$p(w) = \frac{\alpha \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_M}\big)}{\alpha \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_M}\big) + (1-\alpha) \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_U}\big)}$$

该公式刻画了在零均值高斯假设下，区间 $[-w, w]$ 内权重来自模糊化过程的概率，揭示了安全性与效用之间的根本权衡：$\sigma_M$ 越小，遗忘效果越好但剪枝位置越容易被检测；$\sigma_M$ 越大，隐藏效果越好但生成质量下降。这一形式化分析为防御参数的选择提供了理论指导。

## 整体框架

本文提出的概念复活攻击框架（NMS Attack Framework）针对基于剪枝的扩散模型遗忘方法，利用剪枝操作遗留的权重位置信息作为侧信道，在无需任何训练数据或模型重训练的条件下恢复被擦除的视觉概念。整体框架由三个核心模块串联构成：**低秩矩阵补全（Low-rank Matrix Completion）**、**Top-K 符号保留（Top-K Sign Retention）** 和 **神经元最大缩放（Neuron-Max Scaling）**，其结构如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/003_Figure_3.jpg]]
*Figure 3: Overview of sparsity driven unlearning and our proposed revival framework*

### 攻击流水线

**输入**：经概念剪枝遗忘处理后的扩散模型权重矩阵，其中与被遗忘概念相关的权重被置零，其余权重保持不变。攻击者假设能够获取完整的剪枝掩码（白盒访问权重位置）。

**模块一：低秩矩阵补全**
利用 SoftImpute 算法对剪枝后的权重矩阵进行低秩重建。该模块以核范数正则化为目标函数（公式 1），通过迭代软阈值 SVD（公式 2-3）估计缺失位置的权重值。矩阵补全虽无法精确恢复权重的原始幅度，却能以超过 70% 的准确率恢复剪枝权重的符号——这正是概念复活的关键信息。

**模块二：Top-K 符号保留**
基于矩阵补全输出的重建权重，按幅度大小选择保留 Top-K 比例的权重符号，其余位置置零。该步骤滤除了低置信度的符号估计，仅保留最可靠的激活模式信息。实验表明，最优 K 值通常在 0.6 附近：K 过低会过滤有效激活通道，过高则引入噪声信号。

**模块三：神经元最大缩放（NMS）**
对保留符号的权重，赋予其所在神经元（即权重矩阵的同一行或列）中未被剪枝连接的最大幅度值。这一策略放大了关键激活模式，在所有幅度赋值策略中取得最佳的概念复活性能。对比策略包括 Neuron Average（使用神经元剩余连接的平均幅度）和 Neuron Sample（从剩余幅度经验分布中采样）。

**输出**：经上述三步处理后的权重矩阵，可直接替换原剪枝权重，使扩散模型恢复对被擦除概念的生成能力。

### 防御扩展：高斯模糊防御

作为攻击框架的对应防御方案，本文提出将剪枝后的零权重替换为从零均值高斯分布 $\mathcal{N}(0, \sigma_M^2)$ 中采样的随机值，从而隐藏剪枝位置足迹。该防御在遗忘效果与抗攻击能力之间引入可控权衡：$\sigma_M$ 越小，遗忘效果越好但剪枝位置越易被检测；$\sigma_M$ 越大，隐藏效果越好但生成质量可能下降。此权衡关系可通过公式 (4) 和公式 (7) 中的条件概率进行量化分析。

### 关键因果机制

整个攻击框架的有效性根植于一个核心洞察：**权重符号的正确性远大于权重大小的重要性**。理想实验表明，即使仅恢复符号并随机赋值幅度，其概念复活效果也远超恢复幅度而随机符号的策略。低秩矩阵补全恰好能以高准确率恢复大部分符号，而 NMS 策略则进一步放大了这些关键激活模式，使得在无数据、无训练的设定下，攻击者能在七分钟内将擦除概念的平均分类准确率从约 8% 提升至 54%。

## 核心模块与公式推导

### 3.1 攻击框架总览

本文提出的概念复活攻击框架（NMS Attack）由三个级联模块构成，如 Figure 3 所示：**低秩矩阵补全**（Low-rank Matrix Completion）、**Top-K 符号保留**（Top-K Sign Retention）与**神经元最大缩放**（Neuron-Max Scaling）。三个模块协同完成从剪枝权重位置信息到概念复活的全流程，无需任何训练数据或模型重训练。

### 3.2 低秩矩阵补全

剪枝遗忘操作将概念相关权重置零，在权重矩阵中形成结构化的缺失模式。攻击者利用这一侧信道信息，通过矩阵补全技术近似重建被剪枝权重的符号。

矩阵补全的目标函数采用核范数正则化形式：

$$
\operatorname*{min}_{M} \frac{1}{2} \| P_{\Omega}(X) - P_{\Omega}(M) \|_{F}^{2} + \lambda \| M \|_{*}
$$

其中 $X$ 为观测到的部分权重矩阵（含剪枝留下的零值位置信息），$\Omega$ 为未剪枝权重的索引集，$P_{\Omega}$ 为投影算子，$\| \cdot \|_{F}$ 为 Frobenius 范数，$\| \cdot \|_{*}$ 为核范数（矩阵奇异值之和），$\lambda$ 为正则化系数。核范数项强制补全矩阵 $M$ 具有低秩结构，这与神经网络权重矩阵通常呈现的低秩特性相吻合。

优化过程采用 SoftImpute 算法，核心操作为软阈值 SVD：

$$
S_{\lambda}(Y) = U \operatorname{diag}((\sigma_i - \lambda)_{+}) V^{\top}
$$

其中 $Y$ 的 SVD 分解为 $U \operatorname{diag}(\sigma_i) V^{\top}$，$(\sigma_i - \lambda)_{+} = \max(\sigma_i - \lambda, 0)$ 将小于阈值 $\lambda$ 的奇异值收缩至零，从而强制低秩性。SoftImpute 的迭代插补步骤为：

$$
\boldsymbol{Z}^{(t)} = P_{\Omega}(\boldsymbol{X}) + P_{\Omega^{c}}(\boldsymbol{M}^{(t)})
$$

即保留观测值不变，用当前低秩估计 $\boldsymbol{M}^{(t)}$ 填充缺失项（$\Omega^{c}$ 为剪枝位置索引集），再对 $\boldsymbol{Z}^{(t)}$ 施加 $S_{\lambda}$ 得到下一轮估计 $\boldsymbol{M}^{(t+1)}$。

**核心发现**：矩阵补全虽无法完美重建权重的精确幅度，却能以超过 70% 的准确率恢复大部分权重的**符号**（正/负），而符号正是决定神经元激活模式的关键因果杠杆（见 Figure 2 的实证验证）。

### 3.3 Top-K 符号保留

矩阵补全输出的重建权重中，并非所有符号都同等可靠。实验表明，补全权重中**幅度较大者**的符号准确率显著高于幅度较小者（见 Table 6）。因此，本模块按重建权重的绝对值降序排列，仅保留前 $K$ 比例的权重对应符号，其余位置置零。这一操作滤除了低置信度的符号噪声，为后续幅度赋值提供干净的方向信号。

消融实验（Table 3, Table 8–10）表明，最优 $K$ 值通常在 0.6 附近：$K$ 过低会过滤过多有效激活通道导致恢复性能下降，$K$ 过高则引入噪声符号同样损害性能。

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/017_Table_8.jpg]]
*Table 8: Effect of Top-K and magnitudes on parachute revival*

### 3.4 神经元最大缩放

保留符号后，需为这些位置赋予合适的幅度以激活概念相关通路。本文提出**神经元最大缩放**（Neuron-Max Scaling, NMS）：对每个神经元，取其未被剪枝的剩余连接中权重的最大绝对值，赋给该神经元上所有保留符号的剪枝权重。

形式化地，对于神经元 $j$ 上保留符号的剪枝权重 $w_{ij}$，赋值规则为：

$$
w_{ij} \leftarrow \operatorname{sign}(\hat{w}_{ij}) \cdot \max_{k \notin \mathcal{P}_j} |w_{kj}|
$$

其中 $\hat{w}_{ij}$ 为矩阵补全重建的权重符号，$\mathcal{P}_j$ 为神经元 $j$ 上被剪枝的连接索引集。这一策略的直觉在于：神经元的最大权重通常主导其输出激活的尺度，以最大幅度放大保留符号能最大化概念复活效果。Table 1 的对比实验证实，NMS 在所有幅度赋值策略（Neuron Average、Neuron Sample）中取得最佳复活性能。

### 3.5 高斯模糊防御

针对上述攻击，本文提出一种防御策略：将剪枝后的零权重替换为从零均值高斯分布 $\mathcal{N}(0, \sigma_M^2)$ 采样的随机值，从而隐藏剪枝位置足迹。

防御的安全性可通过条件概率量化。假设未修改权重服从 $\mathcal{N}(0, \sigma_U^2)$，修改权重服从 $\mathcal{N}(0, \sigma_M^2)$，修改比例为 $\alpha$，则在区间 $I = [-w, w]$ 内的值来自修改分布的概率为：

$$
p_I = \frac{\alpha \int_{\ell}^{u} f_M(x) dx}{\alpha \int_{\ell}^{u} f_M(x) dx + (1 - \alpha) \int_{\ell}^{u} f_U(x) dx}
$$

在零均值高斯假设下，该概率可进一步写为：

$$
p(w) = \frac{\alpha \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_M}\big)}{\alpha \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_M}\big) + (1 - \alpha) \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_U}\big)}
$$

其中 $\mathrm{erf}(\cdot)$ 为误差函数。该公式揭示了安全性与效用之间的根本权衡：$\sigma_M$ 越小，修改权重集中在零附近，遗忘效果好但剪枝位置易于被检测；$\sigma_M$ 越大，修改权重与未修改权重分布重叠增加，隐藏效果好但生成质量下降。Figure 6 和 Figure 7 分别展示了 $\sigma_M$ 对遗忘效果的影响及条件概率曲面，为实际部署中的参数选择提供指导。

### 补充图表

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/002_Figure_2.jpg]]
*Figure 2: Restored accuracy on erased concept class*

## 实验与分析

### 核心发现：符号恢复是关键杠杆

本工作的实验体系围绕一个核心洞察展开：在剪枝遗忘的扩散模型中，**权重符号的准确性远比权重大小重要**。Table 1（理想实验）直接验证了这一点——若仅恢复符号但随机赋值幅度（Precise signs + random magnitudes），被擦除概念的平均Top-1分类准确率可达0.34；反之，若恢复幅度但随机符号（Random signs + precise magnitudes），准确率仅0.09，与ConceptPrune基线（0.08）几乎无异。这表明，剪枝遗忘的脆弱性根植于权重符号信息的泄露，而NMS攻击框架正是通过矩阵补全精确捕捉这一信号。

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/004_Table_1.jpg]]
*Table 1: Top-1 classification accuracy of erased and preserved objects, using a pre-trained ResNet-50. All neuron methods are based on Top-0.6 Sign Retention*

### 主实验结果

#### 物体概念擦除与复活

Table 1汇总了12类ImageNet子集上的核心结果。ConceptPrune将擦除类的平均Top-1准确率从预训练模型的0.95压至0.08，但NMS攻击在**七分钟内**将其提升至0.54，增幅达0.46。同时，保留类的准确率维持在0.91，与预训练模型（0.92）基本持平，表明攻击并未破坏模型对其他概念的生成能力。对比基线Quant Recover仅恢复到0.13，凸显了符号驱动恢复策略的显著优势。

在幅度赋值策略的消融中，Neuron-Max Scaling（NMS）在所有Top-K设定下均优于Neuron Average和Neuron Sample。以K=0.6为例，NMS的擦除类准确率为0.54，Neuron Average为0.42，Neuron Sample为0.37，验证了“以神经元最大幅值放大关键激活模式”策略的有效性。

#### 艺术风格遗忘与复活

Table 2展示了5位艺术家风格遗忘的定量对比。ConceptPrune将艺术家风格的CLIP相似度从SD-v1.5的0.31降至0.25，NMS攻击平均恢复至0.30，接近原始模型水平。在COCO-30K上，NMS的FID为18.93，优于ConceptPrune的21.45，且CLIP Score（0.51）与SD-v1.5（0.51）持平，证明复活操作未损害整体生成质量。Figure 4的定性结果进一步显示，NMS能有效恢复被擦除的笔触、色调等风格特征，而Quant Recover的恢复效果明显更弱。

#### NSFW内容复活

在安全敏感场景下，攻击的有效性同样显著。ConceptPrune将I2P数据集上的裸体检测数从预训练模型的151降至74，NMS攻击在最优K设定下恢复至118；在MMA和Ring-A-Bell数据集上，检测数分别从57恢复至172、从22恢复至57（Table 7）。这揭示了剪枝遗忘在内容审核场景中的严重安全隐患。

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/015_Table_7.jpg]]
*Table 7: Nudity revival performance across I2P, MMA and Ring-A-Bell datasets under different Top-K settings*

### 消融实验

#### Top-K符号保留的敏感性

Table 3（高尔夫球）、Table 8（降落伞）、Table 9（教堂）、Table 10（加油泵）系统消融了Top-K比例与幅度赋值策略的交互。一致结论是：**最优K值通常位于0.6附近**。当K过低时，过多有效激活通道被过滤，恢复性能下降；K过高时引入噪声符号，性能亦非最优。例如，在高尔夫球复活中，K=0.6时NMS准确率为0.69，K=0.2时降至0.51，K=1.0时降至0.57。

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/010_Table_3.jpg]]
*Table 3: Effect of Top-K and magnitudes on golf ball revival*

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/014_Table_9.jpg]]
*Table 9: Effect of Top-K and magnitudes on church revival*

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/016_Table_10.jpg]]
*Table 10: Effect of Top-K and magnitudes on gas pump revival*

#### 符号恢复准确率的验证

Table 6揭示了攻击有效的深层原因：矩阵补全恢复的权重中，**Top-K组的符号准确率显著高于其余部分**。以高尔夫球概念为例，Top-0.2组的符号准确率达0.82，而剩余部分仅0.58。这解释了Top-K保留策略为何能有效滤除低置信符号、保留高置信符号，从而最大化复活效果。Table 5进一步显示，恢复的权重组（R1–R5）与预训练组（P1–P5）在幅值排序上高度对齐，证明矩阵补全虽不能完美重建幅度，却能准确捕捉权重的相对重要性结构。

### 攻击泛化性

Table 4（亦为Table 11）将NMS攻击应用于Scissorhands和SalUn两种不同的剪枝遗忘方法。在Scissorhands上，NMS将平均擦除准确率从0.21恢复至0.66；在SalUn上，从0.21恢复至0.69。这表明，**只要遗忘方法依赖权重剪枝，NMS攻击的符号恢复策略就具有跨方法的泛化能力**，因为剪枝位置信息始终构成可利用的侧信道。

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/012_Table_4.jpg]]
*Table 4: NMS Attack on Scissorhands and SalUn*

### 防御评估

Figure 6展示了高斯模糊防御中方差σ_M对遗忘效果的影响。σ_M越小，剪枝位置越容易被检测（防御失效）；σ_M越大，隐藏效果越好，但生成质量下降，擦除准确率回升。Table 12的扩展结果显示，σ_M=0.01时防御对攻击的抵抗最强，但部分类别的遗忘效果已开始退化，验证了公式(7)所刻画的安全-效用权衡。Figure 7的条件概率曲面为σ_M的选择提供了可视化指导。

### 局限与待验证点

需注意，所有攻击实验均假设白盒访问剪枝掩码。在纯黑盒场景（仅API输出）下，攻击有效性未经评估，此点需手动验证。此外，高斯模糊防御的σ_M选择目前依赖经验阈值，缺乏自适应机制。多概念同时遗忘的交互影响、以及对抗动态重掩码策略的鲁棒性，亦未在实验中覆盖。

### 补充图表

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/013_Table_6.jpg]]
*Table 6: Sign accuracy of recovered weights as a function of magnitude: Top-K groups consistently exhibit higher correctness than the Rest*

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/008_Figure_6.jpg]]
*Figure 6: Effect of Gaussian obfuscation variance on unlearning performance*

![[assets/figures/papers/paper_list_l2732_https_arxiv_org_abs_2603_06640/figures/009_Figure_7.jpg]]
*Figure 7: The conditional probability*

## 方法谱系与知识库定位

### 攻击视角：剪枝遗忘的逆向脆弱性

本工作在概念遗忘领域开辟了**攻击者视角**的新维度。现有剪枝遗忘方法（如 **ConceptPrune**、**Scissorhands**、**SalUn**）均聚焦于如何有效地定位并移除与目标概念相关的权重，其安全性假设建立在“权重置零即信息销毁”的直觉之上。本工作首次系统性地揭示：**剪枝位置本身构成可被利用的侧信道**——零值权重的位置分布泄露了被遗忘概念的关键参数结构信息，使得攻击者无需访问原始训练数据或进行重训练即可恢复被擦除的概念。

这一发现将剪枝遗忘的安全性问题从“遗忘是否充分”重新定义为“遗忘是否可逆”，为整个基于稀疏化的遗忘范式引入了根本性的威胁模型。

### 方法边界与适用条件

**攻击框架的适用前提**：
- **白盒权重访问**：攻击者需获取完整的剪枝掩码（哪些权重被置零），这在模型公开发布或权重可获取的场景下成立。纯黑盒场景（仅API访问）下攻击有效性未经评估，属于明确的适用边界。
- **结构化剪枝遗忘**：攻击针对的是通过权重置零实现的剪枝遗忘。对于基于微调、蒸馏或对抗训练的遗忘方法，本攻击框架不直接适用。
- **单概念擦除**：实验验证集中在单一概念擦除场景。多概念同时遗忘时的交互效应和攻击策略尚未系统研究。

**防御机制（高斯模糊）的适用边界**：
- 防御通过将置零权重替换为 $\mathcal{N}(0, \sigma_M^2)$ 的高斯噪声来隐藏剪枝足迹。$\sigma_M$ 的选择构成**安全-效用权衡**：$\sigma_M$ 越小，遗忘效果保持越好，但剪枝位置越容易被检测；$\sigma_M$ 越大，隐藏效果越好，但生成质量和遗忘效果下降。
- 当前防御依赖手动调节 $\sigma_M$，缺乏自适应的层间差异化配置机制。

### 与基线方法的关系

**相对于遗忘方法的定位**：
- **ConceptPrune**：作为攻击的起点和主要对比对象，其剪枝权重是本攻击框架的输入。攻击成功将ConceptPrune擦除概念的平均分类准确率从约8%恢复至54%。
- **Scissorhands** 和 **SalUn**：作为额外验证目标，证明攻击并非针对特定剪枝策略的特例。在这两种方法上，攻击仍能将平均遗忘准确率从21%恢复至66%以上，表明脆弱性源于“权重置零”这一共性操作，而非特定剪枝准则。
- **Quant Recover**：作为训练无关的遗忘攻击基线，本攻击框架在所有评估维度上均显著优于该基线。

**防御机制的定位**：
- 高斯模糊防御属于**后处理式防御**，在剪枝完成后对零值权重进行混淆填充。这与训练中动态重掩码、对抗性剪枝等防御策略形成互补但未被覆盖的防御空间。
- 防御的理论基础建立在公式 $p(w) = \frac{\alpha \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_M}\big)}{\alpha \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_M}\big) + (1-\alpha) \ \mathrm{erf}\big(\frac{w}{\sqrt{2}\sigma_U}\big)}$ 所描述的检测概率分析之上，为防御参数选择提供了量化依据。

### 局限性与开放问题

**已识别的局限**：
1. 攻击依赖白盒剪枝掩码，在仅提供API输出的黑盒场景下攻击能力受限。
2. 高斯模糊防御需手动调节 $\sigma_M$，缺乏自动化配置策略。
3. 多概念同时遗忘的交互攻击策略未被探索。
4. 对动态剪枝（训练中重掩码）或对抗性剪枝场景的攻击有效性未经评估。

**开放问题**：
- **黑盒攻击可能性**：能否仅通过API输出的生成结果推断被遗忘概念或恢复概念？这涉及从生成样本反推权重结构的更广义逆问题。
- **自适应防御设计**：能否根据各层权重的统计分布自动选择最优 $\sigma_M$，实现层间差异化的安全-效用平衡？
- **博弈形式化**：攻击与防御的对抗是否可形式化为极小极大优化问题 $\min_{\text{defense}} \max_{\text{attack}} \mathcal{L}_{\text{revival}}$，从而导出更稳健的剪枝遗忘策略？
- **跨架构泛化**：此类权重位置泄露风险是否同样存在于扩散模型以外的生成模型（如自回归模型、流匹配模型）？剪枝位置作为侧信道的现象是否具有更广泛的根本性？
- **密码学防护**：能否结合差分隐私或安全多方计算技术，在保护剪枝位置信息的同时保持遗忘效果，从根本上阻断侧信道泄露？

### 知识库贡献定位

本工作的核心贡献在于**揭示并验证了剪枝遗忘中“权重位置作为侧信道”这一根本脆弱性**，并提供了完整的攻击-防御分析框架。这一发现对基于稀疏化的模型编辑和遗忘方法具有普遍警示意义：任何通过选择性参数修改实现的遗忘，其修改位置本身可能构成信息泄露通道，需要纳入安全性评估体系。

## 原文 PDF

![[paperPDFs/CVPR_2026/Roots_Beneath_the_Cut_Uncovering_the_Risk_of_Concept_Revival_in_Pruning_Based_Unlearning_for_Diffusion_Models.pdf]]
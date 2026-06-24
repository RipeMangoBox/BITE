---
title: Black-box Membership Inference Attacks on the Pre-training Data of Image-generation Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Black_box_Membership_Inference_Attacks_on_the_Pre_training_Data_of_Image_generation_Models.pdf
project_link: null
code_link: "https://github.com/wanghl21/SD-MIA"
aliases:
- SM
- BBMIAPTDIGM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过在多视角文本指令上施加控制性扰动，探测模型在成员样本上表现出的表征区域塌缩（representation-region collapse），即小幅度文本扰动仍能保持稳定生成，而非成员样本则产生明显发散。
primary_logic: 将成员推断从图像空间扰动转向文本空间扰动，利用扩散模型对文本条件始终保持无噪影响的特性，设计多视图文本扰动策略，并通过最大化跨模态相关性估计来量化并放大成员与非成员样本在生成概率曲率上的差异，从而在黑盒条件下可靠地检测预训练数据。
claims:
- 实验表明图像扰动产生的成员与非成员分布几乎重叠，而文本扰动产生显著可分离的分布差异
- SD-MIA在Stable Diffusion v1-2等多个模型上取得最佳AUC和TPR@5%FPR，优于包括需要内部特征的灰盒方法DRC
- 成员样本在文本表征空间中存在梯度近乎为零的塌缩区域，而非成员不存在（公式推导）
- 消融实验证实三种文本扰动视图（token、style、semantic）相互补充，集成后性能最优
---

# Black-box Membership Inference Attacks on the Pre-training Data of Image-generation Models

> [!tip] 核心洞察
> 将成员推断从图像空间扰动转向文本空间扰动，利用扩散模型对文本条件始终保持无噪影响的特性，设计多视图文本扰动策略，并通过最大化跨模态相关性估计来量化并放大成员与非成员样本在生成概率曲率上的差异，从而在黑盒条件下可靠地检测预训练数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | 针对图像生成模型预训练数据的黑盒成员推断攻击 |
| 英文题名 | Black-box Membership Inference Attacks on the Pre-training Data of Image-generation Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qi_Black-box_Membership_Inference_Attacks_on_the_Pre-training_Data_of_Image-generation_CVPR_2026_paper.html) · [Code](https://github.com/wanghl21/SD-MIA) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SD-MIA |
| Dataset | Stable Diffusion v1-2, Stable Diffusion v3.5, Stable Diffusion v1-5, DALL-E 3 |

> [!tip] 效果简介
> - Stable Diffusion v1-2 (LAION-mi, balanced) 上，AUC 66.28 ± 1.47 vs best baseline (DRC, not given exact value) (improves up to 10% over DRC)；TPR@5%FPR 16.73 ± 2.98 vs best baseline (significantly higher)。
> - Stable Diffusion v3.5 (LAION-mi, balanced) 上，AUC 66.93 ± 0.53 vs DRC (significantly higher)。
> - Stable Diffusion v1-5 (1:10 imbalanced) 上，AUC 66.22 ± 5.79 vs DRC (significantly higher)。

## 概述

**问题背景**：扩散模型（如Stable Diffusion）的大规模预训练依赖于从互联网爬取的海量图像-文本对，其中不可避免地包含隐私敏感数据。成员推断攻击（Membership Inference Attack, MIA）旨在检测特定样本是否被用于模型训练，是评估预训练数据隐私泄露风险的核心手段。现有方法主要沿袭针对微调数据设计的范式，通过在图像空间施加扰动并观测去噪重建损失或内部特征差异来推断成员身份。然而，这些方法在预训练场景下普遍失效。

**核心瓶颈**：图像扰动方法失效的根本原因在于双重信号压缩——VAE编码器对精细结构的局部收缩性使得图像空间扰动在潜在空间中大幅衰减，而扩散过程固有的随机性进一步淹没了本就微弱的扰动信号。两者叠加导致成员与非成员样本的重建行为分布高度重叠，无法形成有效的检测信号（Figure 2）。

**核心发现**：与图像模态不同，文本条件在扩散生成过程中始终保持不失噪状态。更重要的是，预训练样本在文本表征空间中存在**表征区域塌缩**（representation-region collapse）现象——模型对成员样本的文本条件附近梯度近似为零，意味着小幅文本扰动仍能保持稳定生成；而非成员样本则表现出明显的生成发散。这一结构性不对称提供了可区分的成员信号。

**提出方法**：SD-MIA（Stable Diffusion Membership Inference Attack）是一个纯黑盒的预训练成员推断框架，仅需文本到图像的查询访问。其核心设计包括三个关键组件：
1. **多视角文本扰动**：利用大型语言模型对原始文本进行token、风格、语义三个层次的受控改写，在保持指令连贯性的前提下引入结构化的文本表征位移；
2. **跨模态相关性估计**：通过视觉与文本编码器提取目标图像与生成图像的联合嵌入，以余弦相似度作为生成概率的替代信号；
3. **最大化相关性池化**：对多次随机生成的前K%最高相关性得分进行均值池化，抑制扩散随机性，放大成员/非成员信号差异。

**主要结果**：SD-MIA在Stable Diffusion v1-2、v3.5等多个模型上取得显著优于现有基线的AUC和TPR@5%FPR，包括需要访问内部特征的灰盒方法DRC（Fu et al., TIFS 2025）。在闭源模型（DALL-E 3、Gemini、GPT-4o）上同样表现优异，验证了方法的通用性。集合级评估中，当集合大小L=30时AUC超过95%。消融实验证实三种文本扰动视图相互补充，集成后性能最优。

**方法定位**：SD-MIA将成员推断的扰动空间从图像模态转向文本模态，利用扩散模型对文本条件无噪影响的特性，在黑盒约束下实现了对预训练数据的可靠检测。该方法为图像生成模型的隐私审计提供了新的技术路径。

## 背景与动机

### 扩散模型预训练数据隐私与成员推断

文本到图像扩散模型（如 Stable Diffusion、DALL-E 系列）在训练过程中记忆了大量预训练数据，这使得模型可能泄露训练样本的隐私信息。成员推断攻击（Membership Inference Attack, MIA）旨在判定一个给定样本是否被用于训练目标模型，是衡量模型隐私泄露风险的核心工具。然而，现有成员推断方法主要针对分类模型或微调数据设计，将其直接扩展到扩散模型的预训练数据检测时面临根本性困难。

### 现有方法的瓶颈：图像扰动的失效

当前针对扩散模型的黑盒成员推断方法，如 **Reconstruction**（Pang and Wang, NDSS 2025），通常采用图像空间扰动策略——对输入图像添加扰动后查询模型去噪重建，通过比较重建损失或相似度来判别成员身份。这类方法背后的假设是：成员样本在生成概率曲面上处于局部极小值，扰动会引起显著的生成概率变化，从而与非成员样本形成可区分的信号差异。

然而，这一假设在扩散模型的预训练数据检测中并不成立。根本原因在于两个结构性障碍：

1. **VAE 编码器的局部收缩性**：扩散模型通常使用 VAE 编码器 $f_v$ 将图像映射到潜在空间。该编码器对精细结构具有压缩效应，其对输入扰动的响应受雅可比矩阵范数约束：

   $$\| {\delta \mathbf{z}} \|_{2} = \| {f_{v}(x + \delta x) - f_{v}(x)} \|_{2} \lesssim \| {J_{f_{v}}(x)} \|_{2} \| {\delta x} \|_{2}$$

   由于 VAE 编码器是局部收缩的（$\|J_{f_{v}}(x)\| < \xi$），图像空间的扰动在潜在空间中被显著压缩，导致实际影响生成过程的信号强度大幅衰减。

2. **扩散随机性的淹没效应**：扩散模型的去噪过程本身包含大量随机采样步骤，这些随机性进一步淹没了已经衰减的扰动信号，使得成员与非成员样本的重建行为差异在统计上不可区分。

上述两个因素共同导致图像扰动引起的生成概率变化在成员和非成员之间趋于一致：

$$| \delta_{x} p(x_{m}) - \delta_{x} p(x_{n}) | \approx \xi \cdot \delta x \to 0, \quad |J_{f_{v}}(x)| < \xi$$

实验分布对比（Figure 2）直观地验证了这一结论：图像扰动方法产生的成员与非成员得分分布几乎完全重叠，无法形成有效的检测信号。

### 文本模态的结构性优势

与图像模态不同，文本条件在扩散模型的生成过程中始终保持无噪状态——文本嵌入直接注入交叉注意力层，不经过任何加噪或去噪处理。这意味着文本扰动可以绕过 VAE 压缩和扩散随机性的双重障碍，直接作用于生成概率曲面的条件维度。

更关键的是，该工作揭示了一个核心现象：**表征区域塌缩（representation-region collapse）**。预训练样本在其文本表征空间中存在梯度近似为零的平坦区域，即小幅文本扰动仍能保持稳定生成；而非成员样本则缺乏这种过拟合结构，文本扰动会导致生成结果明显发散。这一结构性不对称提供了检测成员身份的理论基础：

$$| \delta_{c} p(\boldsymbol{x}_{m}) - \delta_{c} p(\boldsymbol{x}_{n}) | \approx \left. \nabla_{\mathbf{c}} p(\mathbf{z}_{n}, \mathbf{c}_{n}; \boldsymbol{\theta}^{*}) \cdot \delta \mathbf{c}_{n} \right._{2} \gg 0$$

### 本文动机与核心思路

基于上述分析，该工作的核心动机是：**将成员推断的攻击面从图像空间转移到文本空间**，利用文本模态不受扩散噪声影响的特性，设计多视图文本扰动策略来探测表征区域塌缩现象，从而在黑盒条件下可靠地检测扩散模型的预训练数据。

具体而言，SD-MIA 框架通过以下三个关键设计实现这一目标：（1）利用大语言模型对原始文本描述进行 token、风格、语义三个视图的受控改写，产生多视角文本表征位移；（2）设计跨模态相关性估计器，以目标图像与生成图像在视觉-文本联合嵌入空间中的相似度作为生成概率的替代信号；（3）采用最大化相关性池化策略，对多次随机生成的高相关性得分取均值，抑制扩散随机性并放大成员/非成员信号差异。

## 核心创新

SD-MIA 的核心创新在于**将成员推断的攻击面从图像空间迁移至文本空间**，并围绕这一范式转移构建了三个紧密耦合的 changed slots，从根本上解决了现有方法在预训练数据检测上的失效问题。

### 动机：图像扰动为何失效

现有黑盒方法（如 **Reconstruction** (Pang and Wang, NDSS 2025)）通过在图像上施加扰动并观察去噪重建差异来推断成员身份。然而，这一策略在扩散模型的预训练数据检测中几乎无效。Figure 2 的分布对比直观地揭示了这一现象：图像扰动下成员与非成员样本的相似度分布几乎完全重叠，无法形成可区分的检测信号。

论文从理论上将这一失效归因于两个结构性的信号衰减机制：

1. **VAE 编码器的局部收缩性**：图像扰动 $\delta x$ 经 VAE 编码器映射到潜在空间后，其扰动范数被编码器雅可比矩阵的范数所压缩：
   $$\| {\delta \mathbf{z}} \|_{2} = \| {f_{v}(x + \delta x) - f_{v}(x)} \|_{2} \lesssim \| {J_{f_{v}}(x)} \|_{2} \| {\delta x} \|_{2}$$
   由于 VAE 编码器对精细结构具有局部收缩性（$|J_{f_{v}}(x)| < \xi$），图像空间的扰动在潜在空间中被显著削弱。

2. **扩散随机性的淹没效应**：即使潜在扰动得以保留，扩散模型在去噪过程中的随机采样也会进一步淹没扰动信号，使得成员与非成员样本在生成概率曲率上的差异趋近于零：
   $$| \delta_{x} p(x_{m}) - \delta_{x} p(x_{n}) | \approx \xi \cdot \delta x \to 0$$

这两重衰减机制构成了现有图像扰动方法的**根本瓶颈**：扰动信号在到达生成概率曲率之前已被压缩至不可区分的水平。

### Changed Slot 1：扰动模态——从图像空间到文本空间多视角扰动

SD-MIA 的核心突破在于认识到**文本条件在整个扩散生成过程中始终保持无噪状态**，不受 VAE 编码和扩散随机性的影响。基于此，SD-MIA 将扰动模态从图像空间（baseline 做法）切换为**文本空间的多视角扰动**。

具体而言，SD-MIA 使用大型语言模型对原始文本描述 $c$ 在三个视角上生成受控扰动：

- **Token-view**：在 token 级别进行替换或重组，产生 $\{\hat{c}_{i}^{t}\}$
- **Style-view**：改变文本的表达风格，产生 $\{\hat{c}_{i}^{s}\}$
- **Semantic-view**：在保持核心语义的前提下进行同义改写，产生 $\{\hat{c}_{i}^{c}\}$

这三种视角的扰动共同构成了一个结构化的文本表征位移探测机制。其理论基础在于：文本扰动引起的生成概率变化仅受文本梯度范数和文本扰动范数的约束，完全绕开了 VAE 编码器的收缩效应：
$$\delta_{c} p \approx \left| \nabla_{\mathbf{c}} p(\mathbf{z}, \mathbf{c}; \theta^{*}) \cdot \delta \mathbf{c} \right| \lesssim \left\| \nabla_{\mathbf{c}} p(\mathbf{z}, \mathbf{c}; \theta^{*}) \right\|_{2} \cdot \left\| \delta \mathbf{c} \right\|_{2}$$

### Changed Slot 2：成员信号——从重建损失到“表征区域塌缩”探测

文本扰动不仅绕开了信号衰减，更揭示了一个关键的**结构性不对称**：预训练过程中的成员样本在文本表征空间中存在**表征区域塌缩（representation-region collapse）**现象——即模型对成员样本的文本条件形成了局部过拟合，使得小幅度的文本扰动几乎不会改变生成行为，表现为梯度近似为零的平坦区域。而非成员样本则不具备这种塌缩特性，文本扰动会导致明显的生成发散。

这一差异在理论上表现为：
$$| \delta_{c} p(\boldsymbol{x}_{m}) - \delta_{c} p(\boldsymbol{x}_{n}) | \approx \left. \nabla_{\mathbf{c}} p(\mathbf{z}_{n}, \mathbf{c}_{n}; \boldsymbol{\theta}^{*}) \cdot \delta \mathbf{c}_{n} \right._{2} \gg 0$$

即成员样本因梯度近似为零，其文本扰动引起的概率变化远小于非成员样本。SD-MIA 正是通过**探测这一表征区域塌缩现象**来构建成员信号，而非依赖传统的去噪重建损失或内部特征（如 DRC (Fu et al., TIFS 2025) 和 Kong et al. (ICLR 2024) 等灰盒方法）。

为实现黑盒条件下的可计算性，SD-MIA 设计了**跨模态相关性估计器**作为生成概率的替代信号：
$$s(x, \hat{c}) = \big( h_{v}(x) \oplus h_{t}(d_{x}) \big) \cdot \big( h_{v}(\hat{x}) \oplus h_{t}(d_{\hat{x}}) \big)$$
该公式将目标图像与生成图像的视觉嵌入和文本嵌入分别提取并拼接，通过点积计算联合相关性。在此基础上，**最大化相关性池化**对多次随机生成的前 $K\%$ 最高相关性得分进行均值池化，有效抑制扩散随机性带来的方差：
$$s^{t} = \frac{1}{n} \textstyle \sum_{j=1}^{n} s \bigl( \boldsymbol{x}, \hat{c}_{{R_{j}}}^{t} \bigr), \quad n = \lfloor N \cdot K\% \rfloor$$

最终的成员分数定义为扰动后的最大相关性与原始相关性之差：差值越小，表明样本对文本扰动越不敏感，越可能是成员样本。

### Changed Slot 3：访问假设——从灰盒到纯黑盒

与需要访问内部特征（如潜在空间表示或中间噪声预测）的灰盒方法（DRC、Kong et al.、Zhai et al. (NeurIPS 2024)）不同，SD-MIA 在**纯黑盒查询**的设定下运行：攻击者仅能通过文本到图像的生成 API 与模型交互，无需任何内部信息。这一 changed slot 使得 SD-MIA 不仅适用于开源模型（如 Stable Diffusion 系列），也能直接迁移至闭源商业模型（如 DALL-E 3、Gemini、GPT-4o），如 Figure 5 所示，SD-MIA 在这些闭源模型上同样取得了显著的检测性能。

### 创新总结

三个 changed slots 形成了从“为什么现有方法失败”到“如何系统性解决”的完整逻辑链：文本空间扰动绕开了 VAE 收缩和扩散随机性的双重衰减（Slot 1），表征区域塌缩探测利用了预训练过拟合的结构性痕迹（Slot 2），而纯黑盒设计保证了方法的通用性和实用性（Slot 3）。消融实验（Figure 7）进一步证实，三种文本扰动视图相互补充，集成后性能最优，验证了多视图机制的必要性。

## 整体框架

SD-MIA 是一个纯黑盒的预训练数据成员推断框架，其核心设计围绕一个关键观察展开：**图像空间扰动无法有效揭示成员与非成员样本在生成概率曲率上的差异，而文本空间扰动则能产生显著可分离的信号**。基于此，SD-MIA 将攻击从传统的图像扰动范式转向文本扰动范式，利用扩散模型对文本条件始终保持无噪影响的特性，构建了一个多视角文本扰动驱动的检测流程。

### 框架总览

整个框架由四个顺序耦合的模块构成，数据流从原始图像-文本对出发，经多视角扰动、跨模态相关性估计、最大化池化，最终输出成员分数：

1.  **多视角文本扰动生成**：以目标样本的原始文本描述为输入，利用大型语言模型在 token、style、semantic 三个视图上产生受控的文本表征位移，生成多组扰动后的文本指令。
2.  **交叉模态相关性估计**：将原始图像与扰动文本送入目标扩散模型生成重建图像，随后对原始图像和生成图像分别提取视觉嵌入与文本嵌入，拼接后计算余弦相似度，作为生成概率的替代信号。
3.  **最大化相关性池化**：对多次随机生成的结果取 top-K% 相关性得分的均值，抑制扩散过程中的随机噪声，放大成员/非成员样本间的信号差异。
4.  **成员分数计算**：计算扰动后最大相关性与原始相关性之差，差值越小表明样本对文本扰动越不敏感（即处于“表征区域塌缩”状态），越可能是预训练成员。

### 设计动机

传统的基于图像扰动的成员推断方法（如去噪重建相似度）在预训练数据检测上表现不佳，其根本原因在于 VAE 编码器对精细结构的压缩效应和扩散过程中的随机性共同淹没了扰动信号。具体而言，图像扰动引起的生成概率变化被 VAE 编码器的局部收缩性（雅可比矩阵范数有界）和潜在空间扰动范数双重限制，导致成员与非成员的概率变化差异趋于零，分布几乎完全重叠（见 Figure 2）。

相比之下，文本扰动在生成过程中保持不失噪，且预训练样本在文本表征空间中存在“表征区域塌缩”现象——成员样本的生成概率对文本扰动的梯度近似为零，小幅文本扰动仍能保持稳定生成；而非成员样本则因缺乏这种过拟合，对同等扰动产生明显的生成发散。这一结构性不对称构成了 SD-MIA 检测信号的理论基础。

### 模块间的因果连接

多视角文本扰动模块是整个框架的“因果旋钮”（causal knob）：它通过 token 级替换、风格迁移和语义改写三种策略，在文本嵌入空间中产生不同方向的位移向量。这些位移向量经文本编码器映射后，直接作用于扩散模型的交叉注意力层，影响生成过程。交叉模态相关性估计模块则充当“信号放大器”，将生成概率的微小曲率变化转化为可量化的相似度差异。最大化相关性池化进一步抑制了扩散随机性带来的方差，使得成员/非成员信号在统计上显著可分离。最终，成员分数计算将多视图信号整合为单一标量，实现黑盒条件下的可靠检测。

### 补充图表

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/001_Figure_1.jpg]]
*Figure 1: Methodology insights and framework. (A) Visual perturbation struggles to reveal the generation probability curvature gap between member and non-member, resulting in insignificant detection signals. (B) SD-MIA addresses this via a multi-view text perturbation mechanism, enabling precise measurement of curvature shifts and reliable detection of pre-training data in diffusion models*

## 核心模块与公式推导

### 方法动机：为何图像扰动失效

SD-MIA的核心动机源于对扩散模型生成机制的深入分析。现有基于图像扰动的成员推断方法（如**Reconstruction**（Pang & Wang, NDSS 2025））试图通过在目标图像上施加微小扰动，观察模型重建行为的变化来推断成员身份。然而，这一策略在预训练数据检测场景下面临根本性困难。

给定一个训练好的扩散模型 $\mathcal{M}_{\theta^*}$，其生成概率 $p(\mathbf{x}, \mathbf{c}; \theta^*)$ 在图像空间扰动 $\delta x$ 下的变化可表达为：

$$\delta_{x} p \approx \left| \nabla_{\mathbf{z}} p(\mathbf{z}, \mathbf{c}; \theta^{*}) \cdot \delta \mathbf{z} \right| \lesssim \left\| \nabla_{\mathbf{z}} p(\mathbf{z}, \mathbf{c}; \theta^{*}) \right\|_{2} \cdot \left\| \delta \mathbf{z} \right\|_{2}$$

其中 $\delta \mathbf{z}$ 是图像扰动经VAE编码器映射到潜在空间后的变化。VAE编码器 $f_v$ 具有局部收缩性，其对扰动的响应受雅可比矩阵范数约束：

$$\left\| {\delta \mathbf{z}} \right\|_{2} = \left\| {f_{v}(x + \delta x) - f_{v}(x)} \right\|_{2} \lesssim \left\| {J_{f_{v}}(x)} \right\|_{2} \left\| {\delta x} \right\|_{2}$$

当 $|J_{f_{v}}(x)| < \xi$（即编码器在局部具有强收缩性）时，成员与非成员样本在图像扰动下的概率变化差异趋于消失：

$$| \delta_{x} p(x_{m}) - \delta_{x} p(x_{n}) | \approx \xi \cdot \delta x \to 0$$

这意味着**图像扰动无法有效揭示成员与非成员样本在生成概率曲率上的差异**，其根本原因在于VAE编码器对精细结构的压缩和扩散过程中的随机性淹没了扰动信号。

### 核心洞察：文本空间扰动与表征区域塌缩

SD-MIA的关键洞察是将扰动从图像空间转向文本空间。由于扩散模型中的文本条件 $\mathbf{c}$ 在生成过程中始终保持无噪状态，文本扰动 $\delta \mathbf{c}$ 引起的生成概率变化不受VAE压缩效应的制约：

$$\delta_{c} p \approx \left| \nabla_{\mathbf{c}} p(\mathbf{z}, \mathbf{c}; \theta^{*}) \cdot \delta \mathbf{c} \right| \lesssim \left\| \nabla_{\mathbf{c}} p(\mathbf{z}, \mathbf{c}; \theta^{*}) \right\|_{2} \cdot \left\| \delta \mathbf{c} \right\|_{2}$$

更重要的是，预训练样本在文本表征空间中存在**表征区域塌缩**（representation-region collapse）现象：成员样本的梯度 $\nabla_{\mathbf{c}} p(\mathbf{z}_m, \mathbf{c}_m; \theta^*)$ 近似为零，即模型在该区域对文本条件变化不敏感。因此，成员与非成员在文本扰动下的概率变化差异显著：

$$| \delta_{c} p(\boldsymbol{x}_{m}) - \delta_{c} p(\boldsymbol{x}_{n}) | \approx \left. \nabla_{\mathbf{c}} p(\mathbf{z}_{n}, \mathbf{c}_{n}; \boldsymbol{\theta}^{*}) \cdot \delta \mathbf{c}_{n} \right._{2} \gg 0$$

这一结构性不对称构成了SD-MIA检测预训练数据的理论基础（见Figure 1和Figure 2的分布对比验证）。

### 多视角文本扰动生成

基于上述理论分析，SD-MIA设计了**多视角文本扰动生成模块**，通过大型语言模型对原始文本描述进行三个维度的受控改写：

- **Token视图**：对文本进行词汇级别的替换，保持语义基本不变；
- **Style视图**：改变文本的表达风格（如正式/口语化），保持核心语义；
- **Semantic视图**：在语义等价范围内进行重述，引入细微的语义位移。

该模块为每个目标样本生成一组扰动后的文本描述 $\{ \hat{c}_{i}^{t}, \hat{c}_{i}^{s}, \hat{c}_{i}^{c} \}_{i=1}^{N}$，在保持指令连贯性的前提下，诱导受控的文本表征位移。

### 跨模态相关性估计

由于黑盒条件下无法直接获取生成概率 $p(\mathbf{x}, \hat{\mathbf{c}} | \theta^*)$，SD-MIA设计了**跨模态相关性评分函数**作为替代估计。对目标图像 $x$ 及其文本描述 $d_x$，以及扰动文本 $\hat{c}$ 下的生成图像 $\hat{x}$ 及其描述 $d_{\hat{x}}$，评分函数定义为：

$$s(x, \hat{c}) = \big( h_{v}(x) \oplus h_{t}(d_{x}) \big) \cdot \big( h_{v}(\hat{x}) \oplus h_{t}(d_{\hat{x}}) \big)$$

其中 $h_v$ 和 $h_t$ 分别为预训练的视觉和文本编码器，$\oplus$ 表示特征拼接。该评分通过计算目标图像与生成图像在联合视觉-文本嵌入空间中的余弦相似度，为生成概率提供了稳定的替代信号。

### 最大化相关性池化

为抑制扩散模型随机生成带来的方差，SD-MIA采用**最大化相关性池化**策略。以token视图为例，对 $N$ 次随机生成的相关性得分取前 $K\%$ 最高值的均值：

$$s^{t} = \frac{1}{n} \textstyle \sum_{j=1}^{n} s \bigl( \boldsymbol{x}, \hat{c}_{{R_{j}}}^{t} \bigr), \quad n = \lfloor N \cdot K\% \rfloor$$

其中 $R_j$ 为得分排序后的索引。该策略通过聚焦高相关性生成结果，有效放大了成员与非成员样本在生成概率曲率上的差异。

### 成员分数计算

最终的成员分数定义为扰动后的最大相关性与原始相关性之差：

$$s_f = s_f(x, \hat{c}) - s_f(x, c)$$

根据表征区域塌缩理论，成员样本由于梯度近似为零，文本扰动引起的相关性变化较小（$s_f$ 接近零）；而非成员样本则表现出明显的相关性下降。这一差值作为 $\delta_c p$ 的经验近似，直接用于成员身份判别。

### 补充图表

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/002_Figure_2.jpg]]
*Figure 2: Distributional comparison between visual-perturbation method and text-perturbation black-box method SD-MIA*

## 实验与分析

### 4.1 实验设置与基准

实验采用**LAION‑mi**基准，该基准通过嵌入空间分布匹配确保成员与非成员样本在语义分布上一致，从而避免域偏移对攻击评估的干扰。目标模型涵盖Stable Diffusion v1‑2、v1‑4、v1‑5、v3.5等多个版本，并同时考虑**平衡（1:1）与不平衡（1:10）**两种成员/非成员比例。评估指标采用**AUC**与**TPR@5%FPR**，所有结果均报告三次运行的均值与标准差。

对比基线包括：
- **Reconstruction**（Pang & Wang, NDSS 2025）：基于图像扰动的黑盒方法，使用去噪重建相似度作为成员信号；
- **DRC**（Fu et al., TIFS 2025）：利用潜在空间生成先验的灰盒方法，需访问内部特征；
- **Kong et al.**（ICLR 2024）：利用扩散过程中间噪声预测的灰盒方法；
- **Zhai et al.**（NeurIPS 2024）：基于条件似然差异的灰盒方法。

其中DRC、Kong et al.和Zhai et al.均需要内部特征，而SD‑MIA仅使用黑盒查询，对比设置公平。

### 4.2 主实验结果

**Table 1** 展示了SD‑MIA与各基线在不同扩散模型上的对比结果。在Stable Diffusion v1‑2（平衡）上，SD‑MIA取得**AUC 66.28 ± 1.47**，较最优灰盒基线DRC提升约10个百分点；**TPR@5%FPR**达到**16.73 ± 2.98**，显著高于所有对比方法。在Stable Diffusion v3.5上，SD‑MIA的AUC为**66.93 ± 0.53**，同样大幅领先DRC。在不平衡设置（1:10）下，SD‑MIA在Stable Diffusion v1‑5上仍保持**AUC 66.22 ± 5.79**，鲁棒性明显优于依赖内部特征的灰盒方法。

**Figure 4** 进一步展示了集合级攻击效果：当集合大小L=30时，SD‑MIA在Stable Diffusion v1‑4上的AUC超过95%，较单样本攻击有质的提升，对应的p值也随L增大而快速下降，验证了多样本聚合的有效性。

### 4.3 闭源模型上的泛化性

**Figure 5** 展示了SD‑MIA在三个闭源商业模型——**DALL‑E 3**、**Gemini**和**GPT‑4o**——上的攻击表现。在完全黑盒、无法获取任何内部特征的条件下，SD‑MIA在所有三个模型上均显著优于基于图像扰动的Reconstruction基线，证明了其跨模型、跨架构的通用性。这一结果尤为关键，因为它表明SD‑MIA不依赖于特定模型的结构假设或特征访问，仅利用文本‑图像生成接口即可实施有效攻击。

### 4.4 鲁棒性分析

**Figure 6** 评估了SD‑MIA在四种训练数据失真下的鲁棒性：图像模糊、高斯噪声、亮度调整和剪切变换。各子图中失真强度从左向右递增。实验表明，SD‑MIA在多数失真类型下仍保持可观的检测能力，尤其在轻度至中度失真下性能下降有限。这得益于其核心机制不依赖于图像像素级别的精细结构，而是利用文本空间中的表征区域塌缩信号。

### 4.5 消融实验

**Figure 7(A)** 对三种文本扰动视图进行了消融分析。结果表明，**token‑view**、**style‑view**和**semantic‑view**对攻击性能均有正向贡献，其中token‑view在部分模型上表现尤为突出。三者集成后性能达到最优，证实了多视图扰动机制的必要性——不同视图捕捉了文本表征空间不同维度的塌缩信号，相互补充形成更强的判别力。

**Figure 7(B)** 检验了当无法获取原始配对文本描述时的替代策略。实验显示，即使使用替代描述（如通用模板或自动生成的描述），SD‑MIA仍能显著优于仅使用图像特征的DRC基线。这进一步验证了文本空间扰动信号本身的有效性，而非仅依赖精确的原始文本。

### 4.6 失败模式与局限

尽管SD‑MIA在多数设置下表现优异，仍存在若干值得注意的边界情况：
- **极端失真**：在Figure 6的高强度失真条件下，攻击性能出现明显下降，表明严重破坏图像语义内容会削弱文本‑图像相关性的估计精度；
- **文本描述质量依赖**：当替代文本描述与原始图像语义严重偏离时，攻击信号减弱，但Figure 7(B)表明即使如此仍优于纯图像基线；
- **生成随机性**：扩散模型固有的随机性使得单次查询的判别信号不稳定，SD‑MIA通过最大化相关性池化（top‑K%均值）部分缓解了这一问题，但在极端情况下仍可能出现方差较大现象，如Table 1中部分模型上TPR@5%FPR的标准差较高。

### 4.7 核心实验结论

综合实验结果，以下结论具有充分证据支持：

1. **文本扰动优于图像扰动**：Figure 2的分布对比与Table 1的定量结果一致表明，图像扰动产生的成员/非成员分布几乎重叠，而文本扰动产生显著可分离的分布差异，这是SD‑MIA有效性的根本原因。

2. **黑盒条件下超越灰盒方法**：SD‑MIA在仅使用查询接口的条件下，AUC和TPR@5%FPR均显著优于需要内部特征的DRC等方法，证明了文本空间扰动信号比潜在空间特征更具判别力。

3. **多视图扰动互补**：消融实验确认三种扰动视图相互补充，集成后性能最优，多视图机制是SD‑MIA设计的必要组件。

4. **闭源模型可迁移**：在DALL‑E 3等闭源商业模型上的成功验证了攻击的通用性，这对预训练数据隐私保护提出了更广泛的安全警示。

### 补充图表

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/003_Table_1.jpg]]
*Table 1: Membership inference performance across different diffusion-based image generation models. We consider balanced and imbalanced (1:10) proportion of member to non-member, and report the AUC and the true positive rate under a false positive rate*

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/005_Figure_4.jpg]]
*Figure 4: Set-level MIA performance: (A) AUC results at different set sizes L; (B) corresponding p-values for sd v1–4 across L*

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/006_Figure_5.jpg]]
*Figure 5: Membership inference attack performance against closed-source image generation models (dall-e-3, gemini-2.0, gpt-4o)*

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/008_Figure_6.jpg]]
*Figure 6: Robustness evaluation under four training-data distortion settings, image blur, Gaussian noise, brightness adjustment, and shear transformation. Within each sub-plot, the distortion intensity increases from left to right*

![[assets/figures/papers/paper_list_l2069_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Black_box_Membershi/figures/009_Figure_7.jpg]]
*Figure 7: Ablation study of SD-MIA, including: (A) perturbation view of textual input, and (B) paired textual description (PD)*

## 方法谱系与知识库定位

### 1. 与现有成员推断方法的定位关系

SD-MIA 在扩散模型预训练数据成员推断任务中，同时突破了**扰动模态**、**成员信号构造**和**访问假设**三个维度的既有范式。下图按这三个维度将 SD-MIA 与代表性基线方法进行定位对比：

| 维度 | 基线方法 | 基线取值 | SD-MIA 取值 |
|------|----------|----------|-------------|
| **扰动模态** | Reconstruction (Pang & Wang, NDSS 2025) | 图像空间扰动 | 文本空间多视角扰动 |
| **成员信号** | DRC (Fu et al., TIFS 2025); Kong et al. (ICLR 2024) | 潜在空间先验 / 中间噪声预测 | 跨模态相关性估计 + 最大化池化 |
| **访问假设** | DRC, Kong et al., Zhai et al. (NeurIPS 2024) | 灰盒（需内部特征或似然） | 纯黑盒查询 |

具体而言，SD-MIA 与以下四类代表性工作的差异体现在：

- **基于图像扰动的黑盒方法**（Pang & Wang, NDSS 2025）：该类方法通过向目标图像添加扰动后观察去噪重建相似度来推断成员身份。SD-MIA 的理论分析（Eq. 1–3）揭示了其根本瓶颈——VAE 编码器的局部收缩性使得图像扰动在潜在空间中衰减，导致成员与非成员的生成概率变化差异趋于零（Figure 2 的分布重叠验证了这一点）。SD-MIA 将扰动从图像空间迁移到文本空间，从根本上避开了 VAE 收缩性的限制。

- **利用潜在空间生成先验的灰盒方法**（DRC, Fu et al., TIFS 2025）：DRC 需要访问模型的潜在空间特征来计算生成先验，属于灰盒设定。SD-MIA 在纯黑盒约束下（仅能通过文本生成图像查询），在 Stable Diffusion v1-2 等模型上 AUC 超越 DRC 最高达 10%（Table 1），证明了文本扰动信号的有效性甚至优于需要内部特征的灰盒方法。

- **利用扩散过程中间噪声预测的灰盒方法**（Kong et al., ICLR 2024）：该类方法依赖去噪过程中间步骤的噪声预测差异，需要访问模型内部状态。SD-MIA 不需要任何中间特征，仅通过最终生成结果与目标图像的跨模态相关性即可构造判别信号。

- **基于条件似然差异的灰盒方法**（Zhai et al., NeurIPS 2024）：该类方法通过比较不同条件下的生成似然来推断成员身份，同样需要模型内部概率输出。SD-MIA 使用 CLIP 等外部编码器构造的跨模态相关性评分函数（Eq. 6）作为生成概率的替代估计，实现了完全黑盒的成员推断。

### 2. 适用边界

SD-MIA 的适用性受以下条件约束：

1. **文本条件依赖**：SD-MIA 要求目标模型接受文本条件输入（text-to-image 范式）。对于无条件生成模型或仅支持图像条件（如 image-to-image、inpainting）的模型，文本扰动机制无法直接应用。消融实验（Figure 7B）表明，当无法获取原始配对文本描述时，SD-MIA 使用替代描述仍能显著优于仅用图像的 DRC 基线，但性能有所下降，说明文本描述的质量和相关性对攻击效果存在影响。

2. **查询预算**：SD-MIA 的多视角扰动策略需要为每个目标样本生成 N 条扰动文本并执行 N 次生成查询，再通过最大化相关性池化（取 top-K%）抑制扩散随机性。集合级评估（Figure 4）显示，当集合大小 L=30 时 AUC 可超过 95%，但单样本级别的 AUC 在 66% 左右，表明该方法在单样本场景下信号有限，更适合批量或集合级推断。

3. **模型架构假设**：SD-MIA 的理论推导基于扩散模型去噪过程中文本条件不受噪声影响的特性。对于非扩散架构的图像生成模型（如 GAN、自回归模型），该理论基础不直接成立，需要进一步验证。

### 3. 局限与开放问题

**已识别的局限**：

- **单样本推断精度有限**：在 LAION-mi 平衡基准上，SD-MIA 的单样本 AUC 约为 66%（Table 1），TPR@5%FPR 仅为 16.73%。这意味着在实际应用中，单张图像的成员身份判定存在较高的误判风险，更适合作为筛选或聚合分析的前置步骤。

- **文本扰动质量依赖 LLM**：多视角文本扰动（token-view、style-view、semantic-view）依赖大型语言模型生成受控改写。LLM 本身的生成质量和指令遵循能力会影响扰动的有效性和一致性，这在跨语言或低资源场景下可能成为瓶颈。

**开放问题**：

- **防御机制的对抗**：Figure 6 展示了 SD-MIA 对图像模糊、高斯噪声、亮度调整和剪切变换等训练数据失真的鲁棒性，但尚未评估针对文本扰动机制的主动防御策略（如文本条件正则化、对抗性文本过滤等）对攻击效果的影响。

- **跨模态信号的理论紧致性**：Eq. 6 定义的跨模态相关性评分函数作为生成概率的替代估计，其与真实生成概率之间的偏差上界尚未给出理论分析。这限制了在极端分布外场景下对攻击可靠性的先验判断。

- **扩展到其他生成范式**：SD-MIA 的核心洞察——利用不受噪声影响的模态条件进行扰动探测——是否可推广到视频生成（文本+时序条件）、3D 生成（文本+几何条件）等多模态生成场景，仍有待探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Black_box_Membership_Inference_Attacks_on_the_Pre_training_Data_of_Image_generation_Models.pdf]]

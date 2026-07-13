---
title: "Seeing Through the Brain: New Insights from Decoding Visual Stimuli with fMRI"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Seeing_Through_the_Brain_New_Insights_from_Decoding_Visual_Stimuli_with_fMRI.pdf
project_link: null
code_link: https://github.com/GraphmindDartmouth/PRISM
openreview_forum_id: 88ZLp7xYxw
aliases:
- STBNIFDVSF
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "采用结构化文本描述作为中间表示，将fMRI信号映射到语言模型空间，并通过对象中心扩散和优化的属性/关系提示显式建模组合结构。"
primary_logic: "fMRI信号与纯语言模型文本空间的对齐度最高，优于视觉-语言和纯视觉空间；重建质量可通过适配文本空间和生成模型以捕获组合、关系性得到进一步提升。"
claims:
- "fMRI信号与T5文本空间在所有对齐指标（CKA、泛化差距、CCA）上均优于视觉和视觉-语言模型。"
- "PRISM在NSD数据集上将LPIPS降低约6%，显著优于现有最佳方法Mindeye2。"
- "移除对象交叉注意力模块导致所有重建指标下降，无法通过提示优化恢复。"
- "仅使用文本空间作为中间表示在所有指标上均优于CLIP文本和LDM视觉空间。"
---

# Seeing Through the Brain: New Insights from Decoding Visual Stimuli with fMRI

> [!tip] 核心洞察
> fMRI信号与纯语言模型文本空间的对齐度最高，优于视觉-语言和纯视觉空间；重建质量可通过适配文本空间和生成模型以捕获组合、关系性得到进一步提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 透视大脑：从fMRI解码视觉刺激的新见解 |
| 英文题名 | Seeing Through the Brain: New Insights from Decoding Visual Stimuli with fMRI |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=88ZLp7xYxw) · [GitHub](https://github.com/GraphmindDartmouth/PRISM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | PRISM |
| Dataset | NSD, BOLD5000, GOD |

> [!tip] 效果简介
> - NSD 上，LPIPS ↓ 为 0.5963，对比 0.6338 (Mindeye2)，变化 −0.0375 (~6% 相对降低)。
> - NSD 上，PixCorr ↑ 为 0.3404，对比 0.3160 (Mindeye2)，变化 +0.0244。
> - BOLD5000 上，SSIM ↑ 为 0.5341，对比 0.5164 (Mindeye2)，变化 +0.0177。

## 概要

从功能性磁共振成像（fMRI）信号中重建人类所视图像，是计算神经科学与人工智能交叉领域的核心挑战。现有方法普遍遵循一条隐含假设：将fMRI信号映射到视觉或视觉-语言模型的嵌入空间，再以此驱动生成模型完成重建。然而，该假设存在两个关键瓶颈：其一，fMRI信号与纯视觉空间的语义对齐并不充分；其二，端到端的全局生成策略无法显式捕获视觉场景中“对象-属性-关系”的组合结构，导致生成图像出现对象绑定错误（如将“灰底虎纹猫”错误生成为“灰色老虎”，见Figure 3）。

**PRISM**（*Projecting fMRI sIgnals into a Structured text space as an interMediate representation*）从上述瓶颈出发，提出了一个视角转换：将fMRI信号映射到纯语言模型的文本空间，而非视觉空间。其核心洞察在于——fMRI信号与T5文本嵌入的对齐度在所有指标（CKA、泛化差距、CCA）上均显著优于CLIP视觉-语言空间和LDM纯视觉空间（Table 1）。基于此，PRISM通过三个关键模块构建了对象中心的组合式重建框架：

- **属性/关系搜索模块**：利用ε-greedy搜索自动发现与神经活动最匹配的属性/关系关键词，引导视觉语言模型（VLM）为每张训练图像生成结构化的对象级文本描述。
- **fMRI编码器与语言模型**：为每个对象分配独立的MLP编码器，从fMRI信号中提取对象特异性特征，再通过微调的T5模型生成预测的结构化描述。
- **对象中心扩散模块**：推理时根据预测的对象描述和位置信息，通过交叉注意力机制逐对象独立生成潜变量，并按空间位置拼接融合为最终图像。

在NSD、BOLD5000和GOD三个数据集上，PRISM在多项指标上超越了现有方法。相较于此前最优方法Mindeye2，PRISM在NSD上将LPIPS降低了约6%（从0.6338降至0.5963），PixCorr从0.3160提升至0.3404（Table 2）。消融实验进一步验证了各模块的必要性：移除对象交叉注意力后LPIPS回升至0.6111（Table 5），而将中间表示从文本空间切换至CLIP文本或LDM视觉空间均导致性能全面下降（Table 7）。

PRISM的贡献不在于提出新的生成模型架构，而在于揭示并利用了fMRI信号与文本空间之间被忽视的对齐优势，并通过对象中心的组合生成策略，为神经信号解码提供了一条结构化、可解释的新路径。



从神经信号中解码视觉体验是计算神经科学的核心挑战之一。功能性磁共振成像（fMRI）因其非侵入性和高空间分辨率，成为研究大脑视觉表征的主要工具。近年来，基于深度生成模型的fMRI-to-image重建方法取得了显著进展，使从大脑活动中恢复人类所见的自然图像成为可能。

然而，现有方法普遍存在两个深层瓶颈。**第一，中间表示空间的选择存在根本性偏差。** 当前主流方法——包括将fMRI映射到CLIP图像嵌入空间的**MindEye**、通过VAE潜变量进行重建的**Takagi & Nishimoto**、以及利用多层CLIP视觉特征引导扩散的**NeuralDiffuser**——均隐含假设视觉空间或视觉-语言联合空间是fMRI信号的最佳对齐目标。但这一假设是否成立，此前缺乏系统的实证检验。

**第二，生成模型未能捕获视觉刺激的组合结构。** 现有方法通常将整幅图像作为单一实体进行端到端生成，忽略了自然场景固有的对象中心组合性。这导致了两个典型失败模式：属性绑定错误（如Figure 3所示，模型将“灰虎纹猫”错误生成为“灰虎”）和关键对象遗漏。即便是当前最优方法**MindEye2**，在重建中也常常忽略场景中的重要对象。

本文的核心动机源于一个关键发现：**fMRI信号与纯语言模型文本空间的对齐度，在多项指标上系统性地优于视觉空间和视觉-语言空间。** 如Table 1所示，T5文本嵌入在CKA（0.5580）、泛化差距（0.1132）和CCA（0.8344）上均显著优于CLIP视觉嵌入和LDM潜变量。这一发现从根本上挑战了“视觉空间是视觉解码的必要中间表示”这一既有假设，并提示我们：**文本空间可能是fMRI视觉解码的更优中间表示**。

基于上述洞察，本文提出PRISM（Projecting fMRI Signals into a Structured text space as an interMediate representation），通过两个核心机制解决现有方法的瓶颈：（1）将fMRI信号映射到结构化文本描述空间，而非视觉嵌入空间；（2）采用对象中心扩散策略，显式建模场景的组合结构，逐对象生成并基于预测位置融合为最终图像。



## 核心方法与创新机理

PRISM的核心创新在于从根本上挑战了fMRI-to-image重建领域的两个默认假设，并提出了相应的解决方案。

**1. 中间表示空间的范式转换：从视觉嵌入到结构化文本**

现有方法（如MindEye、NeuralDiffuser）普遍将fMRI信号映射到视觉嵌入空间（如CLIP图像嵌入或LDM潜变量），隐含地假设视觉空间表示对于重建是必需的。PRISM通过系统性的表示对齐分析（Table 1）证明：**fMRI信号与纯语言模型文本空间（T5）的对齐度最高**，在CKA（0.5580）、泛化差距（0.1132）和CCA（0.8344）三项指标上均显著优于视觉-语言模型（如CLIP）和纯视觉模型。这一发现直接推翻了“视觉空间最优”的假设。

基于此，PRISM将中间表示从视觉嵌入（baseline）替换为**结构化文本描述嵌入**（proposed），使用T5模型作为编码目标。消融实验（Table 7）进一步证实：仅使用文本空间作为中间表示，在所有重建指标上均优于CLIP文本和LDM视觉空间。

**2. 生成模型的组合结构建模：从端到端全局生成到对象中心扩散**

现有方法的生成模型采用端到端的全局图像生成策略，无法显式捕获视觉刺激的**对象中心组合结构**，导致常见的属性绑定错误（如Figure 3所示：“灰虎纹猫”被错误生成为“灰虎”）。

PRISM将生成策略替换为**对象中心扩散**：
- **训练阶段**：通过属性/关系搜索模块，利用VLM自动发现与神经活动最对齐的关键词，生成结构化描述 $D_i^a = [(o_1 : d_1 : \mathrm{loc}_1), (o_2 : d_2 : \mathrm{loc}_2), \ldots, bg_i]$（Section 3.2.1）。
- **推理阶段**：为每个对象独立生成图像，通过对象交叉注意力机制在扩散U-Net中基于预测位置进行空间感知组合（Section 3.3），最终通过混合参数 $\beta$ 融合对象组合潜变量和全局上下文潜变量。

消融实验（Table 5）表明：移除对象交叉注意力模块（w/o ObjC.）导致LPIPS从0.5963升至0.6111，且该性能下降**无法通过提示优化恢复**，证明对象中心建模是不可替代的核心机制。

**3. 监督信号的自动化构建：从现成嵌入到最优提示搜索**

现有方法直接使用现成的图像嵌入或简单标题作为训练监督，未考虑其与神经活动的对齐程度。PRISM引入**属性/关系搜索模块**，通过ε-greedy搜索策略自动发现最优的关键词（Algorithm 1），以最大化重建相似度 $\sum S(\mathbf{Y}_i, \mathrm{Diff}(\mathrm{VLM}(\mathbf{Y}_i, \mathcal{P}(a))))$，同时约束fMRI与文本嵌入的CKA高于阈值 $\beta$（Section 3.2.1）。搜索结果显示，最优关键词持续收敛到空间关系相关术语（如“Spatial Layout”、“Relative Position”），揭示了大脑对空间关系编码的偏好。

**关键证据强度**：上述三个changed slots均有高置信度消融实验支撑（Table 1/5/7，置信度0.95），且PRISM在NSD数据集上将LPIPS降低约6%（0.5963 vs. Mindeye2的0.6338），构成因果性验证闭环。



![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/001_Figure_1.jpg]]
*Figure 1: Framework Overview: PRISM generates structured text descriptions for each training image using a VLM to iteratively extract brain-aligned object attributes and relationships. These descriptions capture the image’s compositional and relational content and serve as supervision to train an encoder and fine-tune a language model to map fMRI signals into the text space. During inference, the model predicts descriptions from fMRI signals, which then guide a pre-trained diffusion model for object-centric image reconstruction*

PRISM（**P**rojecting f**R**I **S**ignals into a structured text space as an inter**M**ediate representation）的整体流程由三个核心阶段构成，其设计根植于一个关键发现：fMRI信号与纯语言模型文本空间的对齐度显著优于视觉-语言模型和纯视觉模型空间（**Table 1**，T5的CKA达0.5580，CCA达0.8344）。这一发现直接挑战了现有方法隐含的假设——即视觉空间表示对于重建是必需的，并构成了PRISM选择文本作为中间表示的根本动机。

### 训练阶段：结构化描述生成与fMRI-文本映射

训练阶段的目标是为每张训练图像生成与大脑活动高度对齐的结构化文本描述，并学习从fMRI信号到该文本空间的映射。

**属性/关系搜索模块**（Section 3.2.1）负责自动发现最优的关键词，用于指导视觉语言模型（VLM）生成描述。给定图像 $\mathbf{Y}_i$ 和关键词 $a$，VLM根据提示 $\mathcal{P}(a)$ 生成结构化描述：

$$D_i^a = \operatorname{VLM}(\mathbf{Y}_i, \mathcal{P}(a))$$

描述采用对象中心的组合格式，显式编码图像中的对象、属性和空间关系：

$$D_i^a = [(o_1 : d_1 : \mathrm{loc}_1), (o_2 : d_2 : \mathrm{loc}_2), \ldots, (o_m : d_m : \mathrm{loc}_m), bg_i]$$

关键词 $a$ 的优化通过 $\varepsilon$-greedy搜索策略完成，目标是在约束fMRI与文本嵌入的CKA高于阈值 $\beta$ 的前提下，最大化重建图像与原始图像的相似度：

$$\max_{a} \sum_{i=1}^{N} \mathcal{S}\left(\mathbf{Y}_i, \mathrm{Diff}(\mathrm{VLM}(\mathbf{Y}_i, \mathcal{P}(a)))\right) \quad \mathrm{s.t.} \quad \mathrm{CKA}(\mathbf{X}, \mathbf{K}^a) > \beta$$

其中评分函数 $\mathcal{S}(\mathbf{Y}_1, \mathbf{Y}_2) = 1 - \mathrm{LPIPS}(\mathbf{Y}_1, \mathbf{Y}_2)$。搜索结果表明，最优关键词持续收敛到空间关系相关的词汇（如"Spatial Layout"、"Relative Position"），这暗示大脑在视觉处理中对空间组合信息存在偏好（**Table 6**）。

**fMRI编码器与语言模型**（Section 3.2.2）负责学习从fMRI信号到文本空间的映射。每个对象的信息通过独立的MLP从fMRI信号 $\mathbf{x}_i$ 中编码：

$$\mathbf{f}_j = \mathbf{MLP}_j(\mathbf{x}_i), \quad j = 1, \ldots, m$$

拼接后的对象特征通过语言模型（T5）生成预测的结构化描述：

$$\hat{D}_i^a = \mathbf{LM}(\mathbf{MLP}_g(\mathrm{Concat}(\mathbf{f}_1, \dots, \mathbf{f}_m)))$$

训练损失覆盖所有 $m$ 个对象描述的负对数似然：

$$\mathcal{L}_{\mathrm{LM}} = -\sum_{j=1}^{m} \sum_{t'=1}^{T'} \log p(y_{t'} \mid y_{<t'}, \mathbf{f}_j)$$

### 推理阶段：对象中心扩散重建

推理阶段分为两步（Section 3.3）：首先从fMRI信号预测结构化描述，然后通过对象中心扩散模块生成最终图像。该模块的核心创新在于将图像生成分解为多个对象的独立生成与空间组合，而非端到端地生成整张图像。

具体而言，扩散模型的U-Net在去噪过程中，通过交叉注意力机制以预测的对象描述为条件：

$$\mathrm{CrossAttention}(\mathbf{H}_t, \mathbf{C}) = \mathrm{softmax}\left(\frac{\phi(\mathbf{H}_t) \cdot \mathbf{W}_Q \cdot (\varphi(\mathbf{C}) \cdot \mathbf{W}_K)^{\top}}{\sqrt{d_k}}\right) \varphi(\mathbf{C}) \cdot \mathbf{W}_V$$

每个对象 $j$ 在时间步 $t-1$ 的隐状态 $\mathbf{H}_{t-1}^j$ 按其预测位置 $\hat{\mathrm{loc}}_j$ 进行缩放和空间感知拼接：

$$\mathbf{H}_{t-1}^{\mathrm{cat}} = \Psi(\{\mathbf{H}_{t-1}^j, \hat{\mathrm{loc}}_j\}_{j=1}^{m})$$

最终通过超参数 $\beta$ 混合对象组合潜变量和全局上下文潜变量，以实现平滑融合：

$$\mathbf{H}_{t-1} = \beta \cdot \mathbf{H}_{t-1}^{\mathrm{cat}} + (1 - \beta) \cdot \mathbf{H}_{t-1}^0$$

### 模块间的因果依赖

消融实验（**Table 5**）揭示了各模块之间的因果依赖关系：移除对象交叉注意力模块（w/o ObjC.）导致LPIPS从0.5963升至0.6111，且这种性能下降无法通过提示优化恢复，表明对象中心的生成策略是框架中不可替代的瓶颈组件。同时，绕过属性/关系搜索而直接使用最优初始属性也会降低性能（Section 4.4），验证了搜索过程对于发现与大脑活动对齐的关键词是必要的。对象数量的消融（**Table 8**）进一步表明，固定两个对象的设置在各项指标上均优于一个或四个对象，过少对象无法充分捕获场景信息，过多对象则可能引入噪声或遗漏关键对象。



### 3.1 表示空间对齐分析

PRISM的设计起点是对fMRI信号与不同模型表示空间对齐程度的系统评估。给定一组fMRI样本 $\mathbf{X}$ 和模型潜表示 $\mathbf{K}$，采用希尔伯特-施密特独立性准则（HSIC）度量二者间的统计依赖性：

$$\mathrm{HSIC}(\mathbf{X}, \mathbf{K}) = \frac{1}{(N-1)^2} \operatorname{tr}(\mathcal{K}(\mathbf{X}) \cdot \hat{\mathcal{K}(\mathbf{K})})$$

其中 $N$ 为样本数，$\mathcal{K}(\cdot)$ 为中心化的核矩阵。基于HSIC，中心核对齐（CKA）给出归一化的空间相似度：

$$\mathrm{CKA}(\mathbf{X}, \mathbf{K}) = \frac{\mathrm{HSIC}(\mathbf{X}, \mathbf{K})}{\sqrt{\mathrm{HSIC}(\mathbf{X}, \mathbf{X}) \cdot \mathrm{HSIC}(\mathbf{K}, \mathbf{K})}}$$

此外，第一典型相关系数 $\rho$ 反映脑活动与模型空间之间最强的线性对齐程度：

$$\rho = \operatorname{corr}(\mathbf{u}, \mathbf{v}) = \operatorname{corr}(\mathbf{p}_1^{\top} \mathbf{X}, \mathbf{p}_2^{\top} \mathbf{K})$$

**Table 1** 的结果表明：纯语言模型T5的文本空间在所有指标上（CKA 0.5580、泛化差距 0.1132、CCA 0.8344）均优于视觉模型（如CLIP视觉、LDM潜空间）和视觉-语言模型（如CLIP文本），这一发现直接驱动了PRISM选择文本空间作为中间表示的核心决策。

### 3.2 结构化文本描述生成

训练阶段的核心任务是为每张图像生成对象中心的结构化文本描述，作为fMRI编码器的监督信号。

**属性/关系搜索模块（Section 3.2.1）** 通过关键词优化自动发现与神经活动最对齐的属性和关系词。给定图像 $\mathbf{Y}_i$ 和关键词 $a$，构造提示 $\mathcal{P}(a)$ 引导VLM生成结构化描述：

$$D_i^a = \operatorname{VLM}(\mathbf{Y}_i, \mathcal{P}(a))$$

描述遵循固定的组合格式：

$$D_i^a = [(o_1 : d_1 : \mathrm{loc}_1), (o_2 : d_2 : \mathrm{loc}_2), \ldots, (o_m : d_m : \mathrm{loc}_m), bg_i]$$

每个元组包含对象名 $o_j$、属性描述 $d_j$ 和空间位置 $\mathrm{loc}_j$，外加背景信息 $bg_i$。

关键词 $a$ 的优化问题形式化为：

$$\max_{a} \sum_{i=1}^{N} S\left(\mathbf{Y}_i, \mathrm{Diff}(\mathrm{VLM}(\mathbf{Y}_i, \mathcal{P}(a)))\right) \ \mathrm{s.t.} \ \mathrm{CKA}(\mathbf{X}, \mathbf{K}^a) > \beta$$

其中 $S(\mathbf{Y}_1, \mathbf{Y}_2) = 1 - \mathrm{LPIPS}(\mathbf{Y}_1, \mathbf{Y}_2)$ 为图像相似度评分，$\mathbf{K}^a$ 为关键词 $a$ 对应的文本嵌入，约束项确保fMRI与文本空间的对齐度不低于阈值 $\beta$。搜索采用ε-greedy策略：以概率 $1-\varepsilon$ 从当前最优关键词出发扩展语义关联词，以概率 $\varepsilon$ 随机探索，逐步收敛到空间关系类关键词（如“Spatial Layout”、“Relative Position”）。

**fMRI编码器与语言模型（Section 3.2.2）** 将每个对象的fMRI信息独立编码后送入微调的语言模型。对于 $m$ 个对象，各自通过独立MLP编码：

$$\mathbf{f}_j = \mathbf{MLP}_j(\mathbf{x}_i), \ j = 1, \ldots, m$$

拼接所有对象特征后，由全局MLP和语言模型生成预测的结构化描述：

$$\hat{D}_i^a = \mathbf{LM}(\mathbf{MLP}_g(\mathrm{Concat}(\mathbf{f}_1, \dots, \mathbf{f}_m)))$$

微调损失为覆盖所有对象描述的负对数似然：

$$\mathcal{L}_{\mathrm{LM}} = -\sum_{j=1}^{m} \sum_{t'=1}^{T'} \log p(y_{t'} \mid y_{<t'}, \mathbf{f}_j)$$

### 3.3 对象中心扩散模块

推理阶段，PRISM依据预测的 $m$ 个对象描述和位置，通过对象中心扩散生成最终图像。扩散模型U-Net中的交叉注意力机制以潜表示 $\mathbf{H}_t$ 为查询、条件 $\mathbf{C}$ 为键和值：

$$\mathrm { C r o s s A t t e n t i o n } ( \mathbf { H } _ { t } , \mathbf { C } ) = \mathrm { s o f t m a x } \left( \frac { \phi ( \mathbf { H } _ { t } ) \cdot \mathbf { W } _ { Q } \cdot ( \varphi ( \mathbf { C } ) \cdot \mathbf { W } _ { K } ) ^ { \top } } { \sqrt { d _ { k } } } \right) \varphi ( \mathbf { C } ) \cdot \mathbf { W } _ { V }$$

每个对象独立经历去噪过程，生成各自的潜表示 $\mathbf{H}_{t-1}^j$。随后按预测位置 $\hat{\mathrm{loc}}_j$ 进行空间感知拼接：

$$\mathbf{H}_{t-1}^{\mathrm{cat}} = \Psi(\{ \mathbf{H}_{t-1}^j, \hat{\mathrm{loc}}_j \}_{j=1}^{m})$$

为平滑融合对象组合与全局上下文，引入超参数 $\beta$ 进行混合：

$$\mathbf{H}_{t-1} = \beta \cdot \mathbf{H}_{t-1}^{\mathrm{cat}} + (1 - \beta) \cdot \mathbf{H}_{t-1}^0$$

其中 $\mathbf{H}_{t-1}^0$ 为全局背景的潜表示。消融实验（**Table 5**）表明，移除对象交叉注意力（即取消独立的对象生成与拼接）导致LPIPS从0.5963升至0.6111，且无法通过提示优化恢复，验证了该模块的关键作用。



## 实验与关键发现

### 核心发现：文本空间作为最优中间表示

PRISM的设计起点是一个反直觉的实证发现：fMRI信号与纯文本语言模型空间的表示对齐度，显著优于视觉-语言模型（如CLIP）和纯视觉模型（如LDM）的空间。Table 1的量化结果显示，T5文本空间在三个关键对齐指标上全面领先——CKA达到0.5580，泛化差距仅0.1132，CCA高达0.8344，均优于CLIP文本和LDM视觉空间。这一发现直接挑战了此前fMRI-to-image重建方法默认使用视觉嵌入作为中间表示的假设，构成了PRISM选择结构化文本描述作为中间表示的经验基础。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/002_Table_1.jpg]]
*Table 1: Alignment results between model representations and fMRI data, evaluated using CKA, Generalization Gap, and CCA. The best result is highlighted in red. ↑ denotes higher is better; ↓ denotes lower is better*

### 主实验结果：跨数据集与跨指标的全面优势

Table 2汇总了PRISM在NSD、BOLD5000和GOD三个数据集上与现有SOTA方法的全面比较。所有方法统一使用Stable Diffusion 2.1作为生成骨架（除标注+SDXL的变体外），并应用相同的负提示策略，确保比较的公平性。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/003_Table_2.jpg]]
*Table 2: Comparison of our framework with state-of-the-art methods on three datasets. All methods use Stable Diffusion 2.1 as the backbone unless otherwise specified (+SDXL). Results are reported using PixCorr, SSIM, LPIPS, CLIP and Inception V3 metrics. The best result using the same backbone in each column is highlighted in red. ↑ indicates higher is better and ↓ indicates lower is better*

在NSD数据集上，PRISM将LPIPS从Mindeye2的0.6338降至0.5963，相对降低约6%（置信度0.95）；PixCorr从0.3160提升至0.3404。在BOLD5000上，SSIM从0.5164提升至0.5341。在GOD数据集上，Inception V3得分从LDM的0.7484跃升至0.8428，提升幅度达0.0944。值得注意的是，PRISM+SDXL变体在NSD上取得了0.9765的Inception V3得分，进一步验证了框架与更强生成骨架的兼容性。

定性结果（Figure 2）揭示了更深层的差异：基线方法如Mindeye2经常忽略或丢失场景中的关键对象，而PRISM成功重建了所有对象。这一优势源于其对象中心生成策略——每个对象独立编码并生成，而非依赖全局潜变量的一次性解码。

### 消融实验：两个核心模块的因果贡献

**对象交叉注意力模块的不可替代性**（Table 5）：移除对象交叉注意力（w/o ObjC.）导致LPIPS从0.5963恶化至0.6111，SSIM从0.4640降至0.4299，PixCorr从0.3404降至0.3291。更关键的是，这一性能下降无法通过后续的提示优化恢复——这说明对象中心的生成结构本身提供了提示优化无法补偿的归纳偏置。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/008_Table_5.jpg]]
*Table 5: Effectiveness of the object-centric diffusion module and attribute/relationship search module on NSD data. The best result is highlighted in red*

**属性/关系搜索模块的增量价值**（Table 5-6）：绕过搜索优化直接使用最优初始属性，性能低于完整搜索方法，证实了ε-greedy搜索策略的有效性。Table 6展示了搜索过程的动态收敛：初始关键词得分分散，经过30轮搜索后，前5名关键词稳定收敛于空间关系相关的词（如"Spatial Layout"、"Relative Position"），且得分显著提升。这一收敛模式本身具有神经科学含义——搜索过程自发地发现空间关系是与fMRI信号对齐度最高的视觉属性。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/009_Table_6.jpg]]
*Table 6: Top-5 keywords scored by 1 − LPIPS before searching and after 10, 20, 30 search steps. The top-5 results remain unchanged after 30 search rounds. The search results indicate a clear preference for keywords related to spatial and positional relations, with most of the top-performing keywords in the final results containing the term ’spatial’*

**中间表示空间的因果验证**（Table 7）：将中间表示从T5文本空间替换为CLIP文本或LDM视觉空间，所有重建指标均下降。这一结果排除了"任何文本空间均可"的替代解释，确认了纯语言模型文本空间的特异性优势。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/012_Table_7.jpg]]
*Table 7: Reconstruction performance across three latent spaces. The best result in each column is highlighted in red. ↑ indicates higher is better and ↓ indicates lower is better. F CASE STUDY ON OBJECT-LEVEL DESCRIPTIONS FOR IMAGE RECONSTRUCTION*

### 对象数量的影响与失败模式

Table 8的系统比较表明，固定两个对象的设置在所有指标上均优于一个或四个对象。对象过少（一个）导致组合信息丢失，对象过多（四个）则引入生成负担，导致某些对象被遗漏或生成质量下降（Figure 5-6）。这一发现暴露了当前框架的一个重要局限：对于对象数目变化较大的复杂场景，固定对象数量的设计可能无法自适应地捕获所有必要信息。该点需要手动验证其在实际部署中的影响程度。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/014_Table_8.jpg]]
*Table 8: Comparison of the number of objects in our framework. Results are reported using PixCorr, SSIM, LPIPS, CLIP, and Inception V3 metrics. The best result in each column is highlighted in red. ↑ indicates higher is better and ↓ indicates lower is better*

### 神经科学的初步验证

梯度可解释性分析发现，PreS脑区对空间关键词的平均体素激活强度（0.0080）显著高于VMV1（0.0028），提示PreS可能在空间关系编码中扮演关键角色。这一发现尚需独立的神经科学实验进一步验证，但为未来的跨学科研究提供了可检验的假设。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/004_Table_3.jpg]]

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/005_Table_4.jpg]]

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/007_Table_4.jpg]]
*Table 4: Reconstruction performance across three latent spaces. The best result in each column is highlighted in red. ↑ indicates higher is better and ↓ indicates lower is better*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/017_Table_9.jpg]]
*Table 9: Top-5 discovered keywords across search rounds*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_88ZLp7xYxw/figures/018_Table_11.jpg]]



## 定位与知识库关联

### 与现有方法的关系

PRISM 的提出建立在对当前 fMRI-to-image 重建范式的两个关键诊断之上：其一，现有方法普遍假设视觉空间表示（如 CLIP 图像嵌入或 LDM 潜变量）是重建的必要中间层；其二，主流生成模型缺乏对视觉刺激中对象中心组合结构的显式建模。这两个瓶颈共同导致了对齐不佳和对象绑定错误——例如在 Figure 3 中展示的“灰虎纹猫”被错误生成为“灰虎”的语义扭曲现象。

从方法谱系看，PRISM 与以下基线工作构成了清晰的演进关系：

- **Takagi & Nishimoto** 作为早期基线，使用线性回归将 fMRI 映射到 VAE 潜空间和 CLIP 文本嵌入，开创了从脑信号到生成模型潜空间的直接映射范式，但其线性映射能力和表示空间选择均受限于当时的技术条件。
- **Mindvis** 通过掩码建模学习 fMRI 表示并微调扩散模型，引入了更强的 fMRI 编码器设计，但未触及中间表示空间的根本选择问题。
- **Mindeye** 和 **Mindeye2** 代表了对比学习对齐范式的高峰：前者通过对比学习对齐 fMRI 与 CLIP 图像空间，再通过扩散先验重建；后者进一步引入多主体共享表示和扩散先验，成为 PRISM 之前的最强基线（SOTA）。PRISM 在 NSD 数据集上将 LPIPS 从 Mindeye2 的 0.6338 降至 0.5963（约 6% 相对降低），直接验证了文本空间替代视觉空间的优势。
- **MindBridge** 关注跨主体对齐问题，使用余弦相似度进行重建，与 PRISM 的主体内编码器设计形成互补。
- **NeuralDiffuser** 解码多层 CLIP 视觉特征并作为梯度引导扩散，代表了多层级视觉特征利用的路线，但同样受限于视觉空间的对齐瓶颈。

PRISM 的核心突破在于三个“槽位”的系统性改变：中间表示空间从视觉嵌入切换为结构化文本描述嵌入（T5 模型），生成策略从端到端全局生成转变为对象中心扩散，训练监督从现成图像嵌入升级为通过属性/关系搜索模块自动学习的最优提示。Table 1 的对齐实验为这一转变提供了决定性证据：T5 文本空间在所有对齐指标（CKA 0.5580、泛化差距 0.1132、CCA 0.8344）上均显著优于视觉-语言模型（如 CLIP）和纯视觉模型（如 LDM）。Table 7 进一步确认，仅使用文本空间作为中间表示在所有重建指标上均优于 CLIP 文本和 LDM 视觉空间。

### 适用边界与局限

PRISM 的设计包含若干显式和隐式的适用边界：

1. **固定对象数量的假设**：框架当前固定每幅图像为两个对象，这一设置在 Table 8 的消融实验中显示为最优（优于一个或四个对象）。但该设计对复杂场景中对象数目变化较大的情况可能不适用——Figure 5 和 Figure 6 的可视化表明，四个对象设置可能导致对象遗漏。对于包含大量重叠对象的密集场景，两个对象的容量是否足以捕获所有必要信息仍是一个开放问题。

2. **属性/关系搜索的计算开销**：搜索模块依赖额外的 VLM 和 LLM 评估，采用 ε-greedy 策略在语义链接空间中迭代搜索最优关键词。虽然 Table 6 显示搜索过程在约 30 轮后收敛（Top-5 关键词趋于稳定），但该过程增加了显著的离线计算开销，且搜索空间可能未穷尽所有相关词汇。Table 9 的鲁棒性验证表明，即使从排除空间关键词的初始集出发，搜索过程仍能重新发现空间相关关键词，但如何更高效地优化搜索以减少对大型语言模型的查询次数，仍需进一步研究。

3. **生成质量的继承性限制**：所有方法均使用 Stable Diffusion 2.1 作为生成骨架（除特别标注 +SDXL 的变体外），PRISM 的重建质量因此受限于该预训练扩散模型的能力边界，可能继承其偏差和局限性。能否将对象中心的生成思想与更强大的潜扩散架构（如基于 Transformer 的扩散模型）结合以进一步提升图像质量，是值得探索的方向。

4. **模态与任务的泛化性**：当前验证仅覆盖 fMRI 视觉刺激重建任务（NSD、BOLD5000、GOD 三个数据集），泛化到其他神经信号模态（如 EEG、MEG）或任务类型（如语言解码、运动想象）仍需独立研究。PRISM 框架是否可以直接应用于视频刺激重建或连续神经信号解码，目前尚无实验证据。

5. **神经科学解释的独立验证需求**：消融实验中关于 PreS 脑区对空间关键词激活的发现（PreS 平均体素强度 0.0080 vs. VMV1 的 0.0028），是基于梯度可解释性分析得出的相关性结论，尚需独立的神经科学实验进一步验证其因果性和可复现性。

### 开放问题

PRISM 揭示的发现和遗留的空白指向若干值得深入的方向：

- **对象数量的自适应机制**：当前固定两个对象的设置在部分场景下可能不足或冗余，如何设计自适应的对象数量选择机制（例如基于 fMRI 信号本身预测场景复杂度）是一个自然的改进方向。
- **跨主体泛化的增强**：PRISM 的编码器目前采用主体内训练范式，在跨主体泛化方面是否能通过域适应技术（如对抗训练或多主体共享表示学习）进一步提高性能，值得探索。
- **搜索策略的效率优化**：当前的 ε-greedy 搜索虽然有效，但效率较低。能否引入贝叶斯优化或基于梯度的提示优化方法，在保持搜索质量的同时大幅减少 VLM/LLM 的查询次数？
- **神经科学假设的可验证性**：所发现的 PreS 脑区对空间关系的关键作用是否能形成可检验的神经科学假设（例如通过经颅磁刺激 TMS 干预 PreS 区域后观察重建质量变化），可为脑-行为因果关系研究提供新路径。
- **与更大规模生成模型的结合**：随着扩散模型架构的快速演进（如基于 Transformer 的潜扩散模型），PRISM 的对象中心生成模块是否能与这些新架构无缝结合，以进一步提升图像质量和语义保真度？



## 原文 PDF

![[paperPDFs/ICLR_2026/Seeing_Through_the_Brain_New_Insights_from_Decoding_Visual_Stimuli_with_fMRI.pdf]]

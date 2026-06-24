---
title: Next-Scale Autoregressive Models for Text-to-Motion Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Next_Scale_Autoregressive_Models_for_Text_to_Motion_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Zheng_Next-Scale_Autoregressive_Models_for_Text-to-Motion_Generation_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- NSAMTMG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 层次化从粗到细的next-scale自回归预测，在粗尺度强制模型依赖文本语义规划全局动作组织，消除局部动态可预测性带来的短视学习捷径，引导模型学习长程语义依赖。
primary_logic: 通过从粗到细的层次化因果生成提供全局语义支架，克服了此前方法在有限数据下难以捕捉长程语义的瓶颈；粗尺度先锁定整体结构，精细尺度逐步细化，实现了文本到运动对齐的根本性改善。
claims:
- MoScale能够准确捕捉文本描述中的全局语义结构（如‘两个jumping jacks’、序列动作），而先前方法无法对齐文本。
- 消融实验表明，层次化精炼（HR）将Top-1从基础模型的0.481提升至0.534，结合时序精炼后达到0.540，是文本对齐提升的主要驱动力。
- MoScale在HumanML3D上取得最佳Top-1准确率0.540和最低MM-Dist 2.830，达到SOTA性能。
- 用户研究中，MoScale在文本对齐（71.5%）和运动质量（73.3%）上均显著优于先前方法。
---

# Next-Scale Autoregressive Models for Text-to-Motion Generation

> [!tip] 核心洞察
> 通过从粗到细的层次化因果生成提供全局语义支架，克服了此前方法在有限数据下难以捕捉长程语义的瓶颈；粗尺度先锁定整体结构，精细尺度逐步细化，实现了文本到运动对齐的根本性改善。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于文本到运动生成的下一尺度自回归模型 |
| 英文题名 | Next-Scale Autoregressive Models for Text-to-Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zheng_Next-Scale_Autoregressive_Models_for_Text-to-Motion_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | MoScale |
| Dataset | HumanML3D, KIT-ML, User Study, Zero-shot Tasks |

> [!tip] 效果简介
> - HumanML3D 上，Top-1 ↑ 0.540 (best)；MM-Dist ↓ 2.830 (best)；FID ↓ 0.049 (S=4) (best)。
> - KIT-ML 上，Top-1 ↑ 0.442 (best)；Top-3 ↑ 0.791 (best)。
> - User Study (text-to-motion) 上，文本对齐偏好率 71.5%。

## 概述

文本到运动生成的核心挑战在于，模型必须在生成运动序列的初期就建立可靠的**全局语义结构**——例如动作的重复次数、顺序动作模式等。现有方法（扩散模型、掩码Transformer、下一token自回归）在生成初期缺乏对长程语义的显式规划能力，导致全局一致性缺失，且这一缺陷无法通过后续局部精炼来弥补。

针对这一瓶颈，**MoScale** 提出**下一尺度自回归**（next-scale autoregression）框架，将生成过程从传统的“左到右逐token预测”转变为“从粗到细层次化因果预测”。其核心洞察在于：粗尺度的生成强制模型依赖文本语义来规划全局动作组织，从而消除局部动态可预测性带来的短视学习捷径，引导模型真正学习长程语义依赖。粗尺度锁定整体结构后，精细尺度逐步细化，实现了文本到运动对齐的根本性改善。

在方法谱系中，MoScale 区别于以下主流范式：

- **下一token自回归方法**（如 **T2M-GPT** [Zhang et al., CVPR 2023]、**AttT2M** [Zhong et al., ICCV 2023]、**ParCo** [Zou et al., ECCV 2024]）采用严格的左到右因果顺序，缺乏对全局语义结构的显式建模。
- **掩码Transformer方法**（如 **MMM** [Pinyoanuntapong et al., CVPR 2024]、**MoMask** [Guo et al., CVPR 2024]）通过双向注意力进行迭代精炼，但生成初期同样缺少层次化的语义支架。
- **扩散模型方法**（如 **MDM** [Tevet et al., 2022]、**MotionDiffuse** [Zhang et al., TPAMI 2024]、**ReMoDiffuse** [Zhang et al., ICCV 2023]）以去噪方式生成运动，虽具备一定的全局性，但在有限数据下捕捉长程语义的能力仍受限制。

MoScale 通过三项关键设计实现突破：（1）**层次化尺度间因果掩码**，防止高尺度信息泄露，确保粗尺度独立承担语义规划职责；（2）**跨尺度层次化精炼**，训练时扰动粗尺度预测，迫使精细尺度学习从错误中恢复；（3）**尺度内时序精炼**，通过选择性掩码重预测迭代优化每尺度内的token质量。

在标准基准上，MoScale 取得了领先性能：HumanML3D 上 Top-1 准确率达到 **0.540**，MM-Dist 降至 **2.830**；KIT-ML 上 Top-1 和 Top-3 分别达到 **0.442** 和 **0.791**。用户研究中，MoScale 在文本对齐（71.5%）和运动质量（73.3%）上均显著优于先前方法。消融实验证实，层次化精炼是文本对齐提升的主要驱动力——仅此一项便将 Top-1 从基础模型的 0.481 提升至 0.534。

## 背景与动机

### 文本到运动生成的核心挑战

文本到运动生成（text-to-motion generation）旨在根据自然语言描述合成逼真的三维人体运动序列。该任务的核心难点在于，文本描述往往蕴含丰富的**长程语义结构**——例如动作的重复次数（“两个jumping jacks”）、顺序动作组合（“转身→捡东西→转身”）以及动作间的时序依赖关系——这些语义需要在生成的运动序列中得到精确体现。

### 现有方法的瓶颈

当前主流的文本到运动生成方法可归纳为三类范式：

- **扩散模型**（如 **MDM** (Tevet et al., 2022)、**MotionDiffuse** (Zhang et al., TPAMI 2024)、**ReMoDiffuse** (Zhang et al., ICCV 2023)）通过迭代去噪生成运动，但在长序列的全局结构一致性上缺乏显式建模。
- **掩码Transformer**（如 **MMM** (Pinyoanuntapong et al., CVPR 2024)、**MoMask** (Guo et al., CVPR 2024)）通过并行掩码预测生成运动token，但掩码模式的随机性使其难以可靠地捕获跨时间步的因果依赖。
- **下一token自回归模型**（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**AttT2M** (Zhong et al., ICCV 2023)、**ParCo** (Zou et al., ECCV 2024)）采用左到右的逐token预测，虽具备天然的因果结构，但在生成初期缺乏对未来运动全局结构的可靠规划。

这些方法的共同瓶颈在于：**在生成初期未能可靠建立全局语义结构**。对于下一token自回归模型，其严格的左到右因果顺序使早期token的生成仅依赖局部上下文，模型容易习得“短视”的局部动态可预测性捷径，而忽略文本中需要跨长程才能体现的语义约束。一旦初始阶段的全局一致性缺失，后续的局部精炼难以从根本上纠偏——这正是Figure 1所揭示的现象：先前方法无法准确捕捉“两个jumping jacks”或“转身→捡东西→转身”这类全局语义结构。

### 本文动机：从下一token到下一尺度

针对上述瓶颈，本文提出**MoScale**，一种**下一尺度自回归（next-scale autoregressive）**框架。其核心动机是：通过从粗到细的层次化因果生成，强制模型在粗尺度阶段依赖文本语义规划全局动作组织，从而消除局部动态可预测性带来的短视学习捷径。粗尺度先锁定整体结构（如动作的阶段划分、重复次数），精细尺度再逐步细化运动细节，以此实现文本到运动对齐的根本性改善。

这一设计的关键洞察在于：**层次化因果生成提供了全局语义支架**，使模型在有限数据条件下也能可靠地捕捉长程语义依赖，克服了此前方法在长程文本-运动对齐上的根本瓶颈。

## 核心创新

### 问题根源：全局语义支架的缺失

现有文本到运动生成方法——无论是基于扩散的**MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., TPAMI 2024），基于掩码Transformer的**MMM**（Pinyoanuntapong et al., CVPR 2024）、**MoMask**（Guo et al., CVPR 2024），还是基于下一token自回归的**T2M-GPT**（Zhang et al., CVPR 2023）、**AttT2M**（Zhong et al., ICCV 2023）、**ParCo**（Zou et al., ECCV 2024）——在生成初期均未能可靠建立全局语义结构。这导致长程语义（如动作重复次数、顺序动作模式）难以准确生成，且初始阶段缺失的全局一致性无法通过后续局部精炼纠偏。如图1所示，对于“两个jumping jacks”或“转身-拾物-转身”等需要全局规划的文本描述，先前方法普遍无法对齐文本语义。

### 核心因果机制：下一尺度自回归

MoScale的根本创新在于将生成范式从**下一token自回归**转向**下一尺度自回归**。传统下一token预测将运动序列的联合概率分解为严格的左到右因果顺序：

$$p ( x _ { 1 } , \ldots , x _ { N } ) = \prod _ { n = 1 } ^ { N } p ( x _ { n } \mid x _ { 1 } , \ldots , x _ { n - 1 } , \mathbf { c } )$$

而MoScale将生成重新组织为从粗到细的层次化因果预测，每一尺度生成该尺度的全部token：

$$p ( \mathbf { z } _ { 1 } , \ldots , \mathbf { z } _ { K } ) = \prod _ { k = 1 } ^ { K } p ( \mathbf { z } _ { k } \mid \mathbf { z } _ { 1 } , \ldots , \mathbf { z } _ { k - 1 } , \mathbf { c } )$$

这一范式转换的因果作用在于：粗尺度token以极低时间分辨率（如6帧）编码运动的全局骨架，模型在生成这些token时**必须依赖文本语义来规划整体动作组织**，无法通过局部动态的可预测性走“短视学习捷径”。精细尺度则在全局支架已锁定的前提下逐步细化局部细节，从而实现了文本到运动对齐的根本性改善。

### 三大关键技术组件

**1. 层次化尺度间因果掩码**

MoScale在自注意力中施加尺度间因果掩码，严格防止高尺度（精细）信息泄露到低尺度（粗粒度）生成过程。尺度内部则采用双向注意力，允许当前尺度token之间充分交互。这一设计从架构层面强制模型遵循从粗到细的因果生成顺序。

**2. 跨尺度层次化精炼**

训练时，MoScale对粗尺度预测的token引入扰动，并动态调整精细尺度的学习目标，使其学习从错误中恢复。具体而言，对于尺度k，先扰动尺度k-1的预测特征：

$$\tilde{\hat{\mathbf{f}}}_{:k-1} = \sum_{i=1}^{k-2} \hat{\mathbf{f}}_i + \tilde{\hat{\mathbf{f}}}_{k-1}$$

随后计算扰动条件下的目标残差：

$$\tilde{\mathbf{f}}_k = \mathsf{down}\left(\mathbf{f} - \tilde{\hat{\mathbf{f}}}_{:k-1}, L_k\right)$$

这一机制使得模型在推理时即使粗尺度预测不够完美，精细尺度也能有效纠正，显著提升了运动质量。

**3. 尺度内时序精炼**

在每个尺度内部，MoScale采用选择性掩码重预测策略：识别不确定的token并迭代精炼，增强时序一致性。这不同于传统自回归方法的一次性前向预测，通过多步迭代在局部尺度内进一步优化生成质量。

### 消融实验揭示的关键贡献

消融实验（Table 4）明确量化了各组件的贡献：基础模型（纯下一尺度自回归，无精炼）Top-1准确率仅为0.481，FID为0.176；加入**层次化精炼**后，Top-1跃升至0.534，FID降至0.090，是性能提升的主要驱动力；进一步结合**时序精炼**后，Top-1达到0.540，FID降至0.046，MM-Dist降至2.830，取得最优综合得分。VLM对齐得分也印证了这一结论：全模型2.14，仅层次化精炼2.09，仅时序精炼1.92，无精炼1.89，表明层次化精炼是对齐文本语义的核心贡献者。

### 与现有方法的本质差异

| 维度 | 先前方法 | MoScale |
|------|---------|---------|
| 生成范式 | 下一token自回归（左到右） | 下一尺度自回归（粗到细层次化因果预测） |
| 跨尺度精炼 | 无扰动或直接预测残差 | 训练时扰动粗尺度预测，精细尺度学习从错误中恢复 |
| 尺度内精炼 | 单次前向预测 | 选择性掩码重预测迭代精炼 |
| 因果掩码策略 | 单向时间因果掩码 | 层次化尺度间因果掩码（防高尺度泄露），尺度内双向注意力 |

这些创新共同构成了MoScale的核心竞争力：通过层次化因果生成提供全局语义支架，克服了此前方法在有限数据下难以捕捉长程语义的瓶颈，在HumanML3D和KIT-ML两个标准基准上均取得SOTA性能，并在用户研究中以71.5%的文本对齐偏好率和73.3%的运动质量偏好率显著优于先前方法。

## 整体框架

MoScale 提出了一种从粗到细的层次化自回归生成范式，其核心思想在于：**先锁定全局语义结构，再逐步细化局部细节**。与传统的下一token自回归（逐帧左到右预测）不同，MoScale 将运动序列建模为多个时间尺度的离散token组，按尺度由粗到细依次生成，从而在生成初期就强制模型依赖文本语义进行全局运动规划。

### Pipeline 总览

整个框架由四个关键模块串联构成，形成“编码—生成—精炼—解码”的完整链路：

1. **残差VQ-VAE编码器**：将原始运动序列压缩为多尺度离散token表示。第一层（最粗尺度）直接对运动下采样并量化，后续各层则对前序尺度的重建残差进行下采样和量化，形成从粗到细的层次化token序列 $(\mathbf{z}_1, \mathbf{z}_2, \ldots, \mathbf{z}_K)$。这一设计确保粗尺度token承载运动的全局轮廓，精细尺度token则编码局部高频细节。

2. **Next-Scale因果Transformer**：以尺度间因果注意力机制自回归地生成各尺度token。生成顺序为 $\mathbf{z}_1 \to \mathbf{z}_2 \to \cdots \to \mathbf{z}_K$，每个尺度 $\mathbf{z}_k$ 的生成以所有前序粗尺度token和T5编码的文本条件为上下文。关键在于**尺度间因果掩码**——自注意力中严格阻止精细尺度信息向粗尺度泄露，确保生成过程的因果层次性；而在同一尺度内部，则采用双向注意力以充分利用时序上下文。

3. **跨尺度层次化精炼**（训练策略）：训练时对粗尺度的预测token引入随机扰动（corruption），并动态调整精细尺度的学习目标——使其学习从被“破坏”的粗尺度草稿中恢复正确的运动残差。这一机制迫使模型学会纠错，显著提升了生成鲁棒性和文本对齐能力。

4. **尺度内时序精炼**（推理策略）：在每个尺度生成完成后，通过选择性掩码-重预测（selective mask-and-repredict）进行迭代优化：识别当前尺度中置信度较低的token，将其掩码并基于上下文重新预测，以增强尺度内部的时序一致性。

整个pipeline的输入为自然语言文本描述，经预训练T5编码器提取全局语义嵌入后，作为条件注入Transformer的交叉注意力层；输出为多尺度离散token序列，最终通过VQ-VAE解码器重建为连续运动序列。

### 核心公式

下一尺度自回归的联合概率分解为：

$$p(\mathbf{z}_1, \ldots, \mathbf{z}_K) = \prod_{k=1}^{K} p(\mathbf{z}_k \mid \mathbf{z}_1, \ldots, \mathbf{z}_{k-1}, \mathbf{c})$$

其中 $\mathbf{c}$ 为文本条件。这与传统下一token预测形成鲜明对比——后者将序列逐帧分解为 $p(x_n \mid x_1, \ldots, x_{n-1}, \mathbf{c})$，缺乏对全局结构的显式建模。

跨尺度精炼的核心机制体现在扰动累积特征和动态目标残差的计算：

$$\tilde{\hat{\mathbf{f}}}_{:k-1} = \sum_{i=1}^{k-2} \hat{\mathbf{f}}_i + \tilde{\hat{\mathbf{f}}}_{k-1}$$

$$\tilde{\mathbf{f}}_k = \mathsf{down}\left(\mathbf{f} - \tilde{\hat{\mathbf{f}}}_{:k-1}, L_k\right)$$

其中 $\tilde{\hat{\mathbf{f}}}_{k-1}$ 为被扰动的尺度 $k-1$ 重建特征，$\tilde{\mathbf{f}}_k$ 为调整后的尺度 $k$ 学习目标。这一设计使精细尺度学会从粗尺度的错误中恢复，而非简单拟合确定性残差。

### 关键设计决策与证据

消融实验（Table 4）揭示了各模块的贡献权重：**层次化精炼（HR）是性能提升的主要驱动力**，将Top-1准确率从基础模型的0.481提升至0.534，FID从0.176降至0.090；结合时序精炼（TR）后进一步达到Top-1 0.540、FID 0.046的SOTA水平。VLM对齐得分也印证了这一结论：全模型2.14，仅层次化精炼2.09，仅时序精炼1.92，无精炼1.89。

Figure 1的定性对比直观展示了框架优势：MoScale能准确捕捉“两个jumping jacks”中的重复次数语义，以及“转身—捡东西—转身”的顺序动作模式，而先前方法（如T2M-GPT、MoMask等）在这些长程语义上出现明显偏差。这验证了“粗尺度先锁定全局结构”这一核心设计理念的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MoScale. (a) MoScale encodes motion sequences into discrete tokens from coarse to fine through multi-scale quantization. (b) It autoregressively predicts tokens at the next scale, conditioned on the prefix and text inputs, using hierarchical scalewise causal attention. (c) Within each scale, MoScale performs temporal refinement to further improve token quality and consistency*

## 核心模块与公式推导

### 问题形式化：从下一Token到下一尺度

传统下一token自回归（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**AttT2M** (Zhong et al., ICCV 2023)）将运动序列的离散token按时间顺序逐帧生成，其联合概率分解为严格的左到右因果链：

$$p ( x _ { 1 } , \ldots , x _ { N } ) = \prod _ { n = 1 } ^ { N } p ( x _ { n } \mid x _ { 1 } , \ldots , x _ { n - 1 } , \mathbf { c } )$$

其中 $\mathbf{c}$ 为文本条件。这种范式在生成初期仅依赖少数已生成token，缺乏全局语义约束，模型容易学习局部动态可预测性带来的“短视捷径”，导致长程文本语义（如动作重复次数、顺序动作模式）难以准确生成。

MoScale将生成范式从“下一token”转变为**下一尺度**（next-scale），将运动序列按时间分辨率从粗到细组织为 $K$ 个尺度组 $\mathbf{z}_1, \ldots, \mathbf{z}_K$，其联合概率分解为：

$$p ( \mathbf { z } _ { 1 } , \ldots , \mathbf { z } _ { K } ) = \prod _ { k = 1 } ^ { K } p ( \mathbf { z } _ { k } \mid \mathbf { z } _ { 1 } , \ldots , \mathbf { z } _ { k - 1 } , \mathbf { c } )$$

**核心区别**：每个尺度 $\mathbf{z}_k$ 包含该时间分辨率下的**全部token**，生成时以所有更粗尺度的完整token组为条件。粗尺度token数量少但覆盖全时序，强制模型在生成初期依赖文本语义规划全局动作组织，为后续精细尺度提供语义支架。

---

### 模块一：残差VQ-VAE与多尺度量化

运动序列首先经过残差VQ-VAE编码为多尺度离散token。设原始运动特征为 $\mathbf{f}$，尺度 $k$ 的目标特征 $\mathbf{f}_k$ 通过下采样前序尺度的残差计算：

$$\mathbf { f } _ { k } = { \left\{ \begin{array} { l l } { \operatorname { d o w n } ( \mathbf { f } , L _ { 1 } ) , } & { { \mathrm { i f ~ } } k = 1 , } \\ { \operatorname { d o w n } \Bigl ( \mathbf { f } - { \hat { \mathbf { f } } } _ { : k - 1 } , L _ { k } \Bigr ) , } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }$$

其中 $\hat{\mathbf{f}}_{:k-1}$ 为前 $k-1$ 个尺度的累积重建特征，$\operatorname{down}(\cdot, L_k)$ 表示下采样到长度 $L_k$。随后通过向量量化将连续特征映射到共享码本中的最近邻索引：

$$\mathbf { z } _ { k } = \arg \operatorname* { m i n } _ { v \in \left[ V \right] } \| \mathbf { f } _ { k } - \mathbf { Z } _ { v } \| _ { 2 } ^ { 2 }$$

解码时通过码本查找和上采样重建各尺度特征：

$$\hat { \mathbf { f } } _ { k } = \mathrm { u p } ( \mathrm { l o o k u p } ( \mathbf { z } _ { k } ) , T / l )$$

通过残差设计，粗尺度捕获运动全局结构（低频成分），精细尺度逐步补充高频细节，形成从粗到细的层次化表示。具体配置为：码本大小 $512\times512$，4个层次尺度，序列长度分别为 $(6, 12, 24, 49)$（适配HumanML3D和KIT-ML数据集）。

---

### 模块二：Next-Scale因果Transformer

生成器采用 $M$ 层Transformer，每层包含自注意力和交叉注意力。文本条件通过预训练T5编码器提取为固定长度嵌入，经交叉注意力注入各层。

**尺度间因果掩码**是保证层次化因果生成的关键：自注意力中施加尺度级因果掩码（scalewise causal mask），使尺度 $k$ 的token仅能关注尺度 $1$ 到 $k$ 的token，**禁止从更高（更精细）尺度获取信息**。这确保了粗尺度生成时不受精细尺度信息泄露，真正实现从粗到细的因果生成。尺度内部则使用双向注意力，允许同尺度token充分交互。

---

### 模块三：跨尺度层次化精炼训练

标准teacher forcing训练中，精细尺度总以完美的粗尺度token为条件，推理时粗尺度的微小错误可能被逐级放大。为解决这一暴露偏差，MoScale在训练时对粗尺度token引入扰动，动态调整精细尺度的学习目标。

具体而言，对尺度 $k-1$ 的token以一定比例随机替换为码本中其他token，得到扰动后的重建特征 $\tilde{\hat{\mathbf{f}}}_{k-1}$，累积特征为：

$$\tilde{\hat{\mathbf{f}}}_{:k-1} = \sum_{i=1}^{k-2} \hat{\mathbf{f}}_i + \tilde{\hat{\mathbf{f}}}_{k-1}$$

基于扰动后的累积特征重新计算尺度 $k$ 的目标残差：

$$\tilde{\mathbf{f}}_k = \mathsf{down}\left(\mathbf{f} - \tilde{\hat{\mathbf{f}}}_{:k-1}, L_k\right)$$

模型被强制学习从“不完美的粗尺度草稿”中恢复正确的精细结构。消融实验证实，该层次化精炼（HR）是文本对齐提升的主要驱动力：将Top-1准确率从基础模型的0.481提升至0.534，FID从0.176降至0.090。

---

### 模块四：尺度内时序精炼

每个尺度内，MoScale采用选择性掩码重预测策略进行迭代精炼。具体流程为：

1. 在当前尺度完成一次前向预测后，识别置信度较低的token（通过预测概率阈值判定）；
2. 将这些token掩码，以剩余高置信度token为条件重新预测；
3. 重复上述过程若干迭代步。

各尺度迭代步数设为 $(1, 2, 5, 10)$，消融实验表明该配置已接近饱和，继续加倍几乎无额外收益。结合层次化精炼和时序精炼（HR&TR）后，模型达到最优综合性能：Top-1 0.540，FID 0.046，MM-Dist 2.830。

---

### 训练与推理要点

训练采用标准teacher forcing，以预测token $\hat{\mathbf{z}}_k$ 与真实token $\mathbf{z}_k$ 之间的交叉熵损失优化。同时施加无分类器引导（CFG），训练时以10%概率随机丢弃文本条件，推理时CFG尺度设为5以获得最佳整体性能。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/001_Figure_1.jpg]]
*Figure 1: MoScale accurately captures global semantic structure in text descriptions, such as two jumping jacks and sequential actions including turn around, pick things up, and turn around, where prior methods fail to align with the text. Our next-scale autoregressive design with hierarchical causality enables MoScale to preserve these long-range semantics while maintaining realistic motion*

## 实验与分析

### 主实验结果

MoScale在标准文本到运动生成基准HumanML3D和KIT-ML上均取得最优性能。Table 1展示了HumanML3D测试集上的综合对比，所有结果基于20次随机运行平均并报告95%置信区间。

在文本-运动对齐指标上，MoScale（S=18配置）取得**Top-1准确率0.540**和**MM-Dist 2.830**，均优于对比方法。具体而言，相较于基于掩码Transformer的**MoMask**（Guo et al., CVPR 2024）和**MMM**（Pinyoanuntapong et al., CVPR 2024），以及基于扩散的**MotionDiffuse**（Zhang et al., TPAMI 2024）和**ReMoDiffuse**（Zhang et al., ICCV 2023），MoScale在Top-1上分别有显著提升。在运动质量指标上，MoScale取得FID 0.049（S=4配置），Diversity指标同样达到最优。

Table 2展示了KIT-ML测试集上的结果，MoScale取得**Top-1 0.442**和**Top-3 0.791**，进一步验证了方法的跨数据集泛化能力。

用户研究进一步确认了量化指标的可靠性：在文本对齐方面，MoScale获得**71.5%**的偏好率；在运动质量方面，获得**73.3%**的偏好率，均显著优于先前方法。在零样本任务（运动编辑、运动预测）的用户研究中，MoScale同样取得**82.0%**的文本对齐偏好率和**78.4%**的运动质量偏好率。

### 消融实验分析

Table 4系统消融了MoScale的核心设计组件。

**层次化精炼（HR）是文本对齐提升的主要驱动力。** 基础模型（无任何精炼）的Top-1为0.481，FID为0.176。单独添加层次化精炼后，Top-1跃升至**0.534**（+0.053），FID降至0.090（-0.086）。这表明训练时扰动粗尺度预测、强制精细尺度学习纠错，有效引导模型建立了全局语义支架。

**时序精炼（TR）进一步提升了运动质量。** 在层次化精炼基础上叠加时序精炼（HR&TR），Top-1达到**0.540**，FID进一步降至**0.046**，MM-Dist降至**2.830**。单独使用时序精炼（无HR）仅将Top-1从0.481提升至0.505，增益远小于层次化精炼，印证了“先建立全局结构、再局部精炼”的设计逻辑。

VLM对齐得分提供了独立验证：全模型得分2.14，仅层次化精炼2.09，仅时序精炼1.92，无精炼1.89，再次确认层次化精炼是语义对齐的核心贡献。

**Transformer深度**方面，性能随层数增加而单调提升，16层配置取得最优结果，验证了模型容量对层次化生成任务的重要性。

**精炼迭代步数**（Table 5）的消融显示，各尺度迭代步数设为(1,2,5,10)时性能已接近饱和，进一步加倍几乎无额外收益，表明当前配置在精度与效率之间取得了良好平衡。

**无分类器引导（CFG）**尺度分析（Fig. 5）表明，CFG尺度设为5时获得最佳整体性能，过高或过低的引导强度均会导致性能下降。

### 关键定性结论

Figure 1的定性对比直观展示了MoScale的核心优势：对于“two jumping jacks”这类需要精确捕捉重复次数的文本，以及“turn around, pick things up, and turn around”这类序列动作描述，先前方法（包括扩散模型和下一token自回归方法）无法可靠对齐文本语义，而MoScale能够准确生成符合全局语义结构的运动序列。这验证了next-scale层次化因果框架在长程语义建模上的根本性改进。

### 失败模式与局限性

尽管整体性能优异，MoScale仍存在以下已知局限：

1. **物理合理性**：模型未显式建模物理约束，生成长序列时可能产生轻微滑步等物理不合理现象。
2. **数据依赖性**：训练仍依赖有限量的文本-运动对，可能无法充分覆盖长尾或极端复杂文本描述。
3. **泛化边界**：目前仅在HumanML3D和KIT-ML两个标准基准上验证，更大规模、更多样化数据集上的表现有待探索。
4. **超长文本**：未探索对段落级动作描写的扩展能力。

### 实验设置公平性说明

所有主实验结果基于20次随机运行平均并报告95%置信区间，确保统计可靠性。对比方法均使用官方发布模型或论文报告的复现配置。用户研究采用盲测设计，参与者在无标签条件下比较不同方法生成的运动，保证了主观评估的公正性。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/003_Table_1.jpg]]
*Table 1: Performance on HumanML3D. We report the average result over 20 runs with 95% confidence interval. Bold for the best and underline for the second. → indicates that values closer to real motion correspond to better results. S is the total steps across all scales*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/004_Table_2.jpg]]
*Table 2: Performance on KIT-ML test set. Bold for the best result and underline for the second best*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/007_Table_4.jpg]]
*Table 4: Ablation studies. 1) hierarchical and temporal refinement (HR and TR), 2) corruption rate, and 3) transformer depth*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/008_Table_5.jpg]]
*Table 5: Iteration study*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/006_Figure_4.jpg]]
*Figure 4: Motion editing results. MoScale achieves better instruction adherence and retains unedited motion (shown in gray)*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_Next_Scale_Autor/figures/005_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 生成范式迁移：从下一token到下一尺度

MoScale的核心贡献在于将文本到运动生成的因果范式从“下一token预测”迁移至“下一尺度预测”。传统自回归方法——如**T2M-GPT** (Zhang et al., CVPR 2023)、**AttT2M** (Zhong et al., ICCV 2023) 和 **ParCo** (Zou et al., ECCV 2024)——遵循严格的左到右因果顺序，将运动序列的联合概率因子分解为单帧token的条件概率乘积：

$$p ( x _ { 1 } , \ldots , x _ { N } ) = \prod _ { n = 1 } ^ { N } p ( x _ { n } \mid x _ { 1 } , \ldots , x _ { n - 1 } , \mathbf { c } )$$

这类范式在生成初期仅能依赖极有限的上下文（前几帧），模型容易习得“局部动态可预测性”这一短视学习捷径，而忽略对全局语义结构（如动作重复次数、顺序动作模式）的规划。扩散模型（如**MDM** (Tevet et al., 2022)、**MotionDiffuse** (Zhang et al., TPAMI 2024)、**ReMoDiffuse** (Zhang et al., ICCV 2023)）和掩码Transformer（如**MMM** (Pinyoanuntapong et al., CVPR 2024)、**MoMask** (Guo et al., CVPR 2024)）虽然避免了严格的单向因果约束，但由于生成初期缺乏可靠的全局语义支架，同样难以可靠捕捉长程文本-运动对齐。

MoScale将因子分解的单元从单token提升为整个尺度的token组：

$$p ( \mathbf { z } _ { 1 } , \ldots , \mathbf { z } _ { K } ) = \prod _ { k = 1 } ^ { K } p ( \mathbf { z } _ { k } \mid \mathbf { z } _ { 1 } , \ldots , \mathbf { z } _ { k - 1 } , \mathbf { c } )$$

粗尺度（如6帧长度的token组）先行生成，为精细尺度提供全局语义支架，从根本上改变了模型对文本条件的依赖方式。这一设计的关键在于：粗尺度分辨率极低，局部动态信息被大幅压缩，模型被迫依赖文本语义来规划整体动作组织，从而消除短视学习捷径。

### 2. 精炼机制与现有方法的差异

MoScale引入了两个互补的精炼机制，与现有方法的“单次前向预测”形成鲜明对比：

**跨尺度层次化精炼（HR）**：训练时对粗尺度预测引入扰动，动态调整精细尺度的学习目标，使模型学会从粗尺度的错误中恢复。消融实验表明，仅加入HR即可将Top-1准确率从基础模型的0.481提升至0.534，FID从0.176降至0.090（Table 4），是文本对齐提升的主要驱动力。这一机制使得模型在推理时即使粗尺度预测不完美，精细尺度也能有效纠偏。

**尺度内时序精炼（TR）**：在每个尺度内部，通过选择性掩码重预测策略对不确定token进行迭代优化。结合HR与TR后，模型达到Top-1 0.540和FID 0.046的最优综合性能。精炼迭代步数设为(1,2,5,10)时性能已接近饱和，继续加倍几乎无额外收益（Table 5）。

值得注意的是，MoScale的层次化因果掩码策略与现有自回归方法的单向时间因果掩码有本质区别：尺度间采用因果掩码防止高尺度信息泄露，而尺度内部允许双向注意力，兼顾了因果生成的一致性和局部上下文的充分建模。

### 3. 适用边界与局限

**数据规模边界**：MoScale目前仅在HumanML3D和KIT-ML两个标准基准上验证，训练依赖于有限量的文本-运动对（HumanML3D约14,000个序列）。在更大规模、更多样化的文本-运动数据集上的泛化性有待探索，尤其对于长尾或极端复杂的文本描述可能覆盖不足。

**物理合理性边界**：模型未显式建模物理约束（如足部接触、关节限制），生成长序列时可能产生轻微滑步等物理不合理现象。这是当前文本到运动生成领域的共性局限，MoScale的精炼机制并未直接解决该问题。

**文本长度边界**：当前设计未探索对超长文本（如段落级动作描写）的扩展能力。随着文本长度增加，单一全局T5嵌入可能不足以编码细粒度的时序约束。

**任务边界**：MoScale的层次化因果框架目前仅针对单人运动生成设计，尚未推广到多人物交互和带物体交互的运动生成场景。

### 4. 开放问题

1. **框架泛化性**：层次化因果结构是否适用于其他条件序列生成任务（如视频生成、语音驱动运动）？粗到细的生成范式在这些领域中是否同样能提供全局语义支架？

2. **缩放行为**：在百万级文本-运动数据规模下，next-scale自回归与扩散模型的性能对比如何？两者的缩放行为是否存在本质差异？当前最优性能（Top-1 0.540）是否已接近HumanML3D评估协议的上限？

3. **自适应精炼策略**：跨尺度精炼中的腐蚀比例和迭代步数当前采用固定设置，是否存在基于文本复杂度或中间预测置信度的自适应最优调度策略？

4. **数量词精确遵循**：尽管MoScale在全局语义捕捉上显著优于先前方法，但对数量词（如“两个”、“三次”）的精确遵循能力仍有提升空间。这是否需要引入显式的计数监督或结构化语义解析？

5. **物理约束集成**：将物理合理性约束（如足部滑动惩罚、接触一致性）融入层次化精炼过程，能否在不牺牲文本对齐质量的前提下提升运动真实性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Next_Scale_Autoregressive_Models_for_Text_to_Motion_Generation.pdf]]
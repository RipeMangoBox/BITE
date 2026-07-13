---
title: Neighbor-Aware Localized Concept Erasure in Text-to-Image Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Neighbor_Aware_Localized_Concept_Erasure_in_Text_to_Image_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/alirezafarashah/NLCE.git"
aliases:
- NNALCE
- NALCETIDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过谱加权嵌入调制衰减目标子空间方向，同时利用CLIP引导的低秩重注入增强邻居语义，再结合注意力引导的空间门控和硬擦除，实现对目标概念的精确局部抑制而不损害相关邻居。
primary_logic: 概念擦除不仅是目标抑制问题，还需显式维护语义邻居结构。通过将表示空间调制、空间注意力门控和硬擦除组合成由粗到精的流程，可以在不降低整体生成质量的前提下，实现更满足实际应用需求的局部概念移除。
claims:
- NLCE在Oxford Flowers和Stanford Dogs数据集上，在目标擦除的同时，获得了最高的Retain Accuracy和Harmonic Mean (H_o)，明显优于GLoCE等基线。
- 在名人身份擦除中，NLCE达到了最佳综合性能，LPIPSu低于SLD且在三个目标中优于GLoCE，证明了良好的局部保真度。
- 在I2P数据集上，NLCE的NudeNet检出数低于所有基线，同时保持较高的CLIP Score（29.70），优于RECE。
- 消融实验证明三个阶段的递进组合有效：Stage 1提供最佳CS，加入Stage 2和3提升Acc_t和H_o，且不影响生成质量。
---

# Neighbor-Aware Localized Concept Erasure in Text-to-Image Diffusion Models

> [!tip] 核心洞察
> 概念擦除不仅是目标抑制问题，还需显式维护语义邻居结构。通过将表示空间调制、空间注意力门控和硬擦除组合成由粗到精的流程，可以在不降低整体生成质量的前提下，实现更满足实际应用需求的局部概念移除。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文本到图像扩散模型中的邻居感知局部概念擦除 |
| 英文题名 | Neighbor-Aware Localized Concept Erasure in Text-to-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25994) · [Code](https://github.com/alirezafarashah/NLCE.git) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NLCE (Neighbor-Aware Localized Concept Erasure) |
| Dataset | Oxford Flowers, Stanford Dogs, Celebrity Erasure, I2P |

> [!tip] 效果简介
> - Oxford Flowers (Alpine Sea Holly) 上，Acc_t (↓) / Acc_r (↑) / H_o (↑) / CLIP Score (↑) / KID (↓) 0.00 / 82.06 / 90.15 / 32.18 / 0.03 vs GLoCE: 32.00 / 78.91 / 73.05 / 32.17 / 0.22 (Acc_t -32.00, Acc_r +3.15, H_o +17.10, CS +0.01, KID -0.19)。
> - Stanford Dogs (Bluetick) 上，Acc_t (↓) / Acc_r (↑) / H_o (↑) / CLIP Score (↑) / KID (↓) 0.00 / 75.91 / 86.31 / 34.75 / 0.06 vs SLD: 8.00 / 66.62 / 77.28 / 34.69 / 0.48 (综合最优) (Acc_t -8.00, Acc_r +9.29, H_o +9.03, CS +0.06, KID -0.42)。
> - Celebrity Erasure (Anna Kendrick) 上，Acc_t (↓) / Acc_r (↑) / H_o (↑) 0.00 / 94.00 / 96.91 vs GLoCE: 1.33 / 94.67 / 96.63 (Acc_t -1.33, Acc_r -0.67, H_o +0.28 (擦除更强，保留接近))。

## 概要

文本到图像（T2I）扩散模型在生成逼真图像方面取得了显著进展，但也带来了概念滥用的风险——例如生成特定名人肖像、受版权保护的艺术风格或不适宜的内容。概念擦除（concept erasure）旨在从预训练模型中移除特定概念的生成能力，同时保持整体生成质量。现有方法大致分为两类：**训练式方法**（如 ESD、MACE、SPM）通过微调模型参数实现擦除，但计算开销大且可能损害模型通用性；**免训练方法**（如 UCE、RECE、SLD、GLoCE）通过编辑注意力机制或潜变量实现擦除，效率更高，但普遍存在一个关键瓶颈——**邻居间隙（neighbor gap）**：在抑制目标概念时，会无意中削弱语义相邻概念，导致细粒度领域保真度下降。例如，擦除“Alpine Sea Holly”这一花卉类别时，现有方法往往连“Rose”等相邻花卉的生成质量也一并损害。

针对上述问题，本文提出 **NLCE（Neighbor-Aware Localized Concept Erasure）**，一种免训练的邻居感知局部概念擦除框架。其核心洞察是：**概念擦除不仅是目标抑制问题，还需显式维护语义邻居结构**。NLCE 通过三阶段由粗到精的流水线实现这一目标：

1. **表示空间调制（Stage 1）**：在词元嵌入层面，通过谱加权投影算子衰减目标概念子空间方向，同时利用 CLIP 引导的低秩重注入增强邻居语义，从根源上抑制目标并保护邻居。
2. **注意力引导的空间门控（Stage 2）**：利用交叉注意力图定位残余概念激活区域，生成空间门并抑制目标 token 的注意力流，实现空间局部化。
3. **门控硬擦除（Stage 3）**：在门控区域内对潜在特征执行置零操作，不可逆地消除残余痕迹。

为支撑邻居感知机制，NLCE 在预处理阶段从外部语料库（Wikipedia 标题）中挖掘语义邻居：通过余弦相似度检索、具体性过滤和 CLIP 视觉重排序，构建高质量的邻居子空间。

实验覆盖五个基准场景——**细粒度花卉擦除**（Oxford Flowers）、**犬种擦除**（Stanford Dogs）、**名人身份擦除**（Celebrity）、**显式内容擦除**（I2P）和**艺术风格擦除**（Artistic），并对比了 MACE、SPM、ESD、UCE、RECE、SLD、AdaVD、GLoCE 等主流基线。主要结果如下：

- 在 Oxford Flowers 的 Alpine Sea Holly 擦除中，NLCE 实现目标准确率 Acc_t = 0.00、保留准确率 Acc_r = 82.06、调和均值 H_o = 90.15，显著优于 GLoCE（Acc_t 32.00, Acc_r 78.91, H_o 73.05），且 CLIP Score 和 KID 均保持最优水平。
- 在名人擦除中，NLCE 在三个目标上达到 Acc_t 接近 0 的同时，保留准确率与 GLoCE 持平，非目标区域 LPIPS 值低于 SLD，证明局部保真度更优。
- 在 I2P 显式内容擦除中，NLCE 的 NudeNet 检出总数低于所有基线，同时 CLIP Score 达 29.70，优于擦除强度相近的 RECE（29.41）。
- 消融实验证实三阶段递进组合的有效性：Stage 1 提供最佳生成质量，Stage 2 和 Stage 3 进一步提升擦除强度而不损害非目标内容。

方法也存在已知局限：邻居挖掘依赖外部语料和预训练模型，当目标概念存在歧义时（如“Chow”），会导致无效擦除；多概念擦除中个别概念失败会影响整体效果；显式内容擦除在平衡超参数下可能无法完全消除裸露内容。尽管如此，NLCE 为免训练局部概念擦除建立了邻居感知的新范式，在擦除强度、邻居保留和生成质量三者间取得了当前最优的平衡。

文本到图像（T2I）扩散模型在生成逼真且多样化的视觉内容方面展现了卓越能力，但其对大规模互联网数据的无差别学习也使得模型能够复现受版权保护的艺术风格、生成名人肖像或产生显式内容，引发了版权、隐私与安全等多重伦理和法律风险。概念擦除（concept erasure）应运而生，旨在从预训练模型中移除特定概念的生成能力，同时尽可能保持模型在其他概念上的生成质量。

### 现有方法的缺口：邻居间隙

当前的概念擦除方法大致可分为**训练式**与**免训练**两类。训练式方法如 **ESD-x / ESD-u**、**SPM**、**MACE** 通过微调模型参数来抑制目标概念，但计算开销大且可能损害模型整体生成能力。免训练方法如 **UCE**、**RECE**、**SLD**、**AdaVD** 则通过修改交叉注意力或推理过程实现擦除，效率更高，但大多采用全局抑制策略，缺乏对空间定位和语义结构的精细控制。

一个关键但长期被忽视的问题是**邻居间隙（neighbor gap）**：当擦除一个细粒度目标概念时，其语义相邻概念往往被无差别地削弱。例如，擦除“Alpine Sea Holly”这一花卉品种时，现有方法会显著降低“Rose”或“Spring Crocus”等近邻品种的生成质量。**GLoCE** 虽引入了门控低秩适配器以实现局部擦除，但仍缺乏对语义邻居结构的显式建模，导致细粒度领域的保真度下降。这一缺口揭示了概念擦除的核心瓶颈：**擦除不仅是目标抑制问题，还需显式维护语义邻居结构**，否则将在实际应用中造成不可接受的附带损害。

### 本文动机

为填补上述缺口，本文提出 **NLCE（Neighbor-Aware Localized Concept Erasure）**，一种免训练的邻居感知局部概念擦除框架。NLCE 的核心洞察在于：通过将**表示空间调制**、**空间注意力门控**和**硬擦除**组合成一个由粗到精的三阶段流水线，可以在不降低整体生成质量的前提下，精确抑制目标概念并主动保护其语义邻居。该方法旨在为细粒度概念擦除、名人身份保护、显式内容过滤和艺术风格移除等场景提供更满足实际需求的解决方案。

## 核心方法与创新机理

NLCE的核心创新在于将概念擦除从“全局抑制”重构为“局部、邻居感知”的编辑问题，通过三个递进阶段的协同设计，解决了现有方法在擦除目标概念时不可避免的**邻居间隙**（neighbor gap）问题。其关键创新体现在以下三个维度的机制变革。

### 从全局擦除到邻居感知的表示空间调制

现有免训练方法（如UCE、RECE）通常直接编辑交叉注意力投影矩阵以抑制目标概念，但缺乏对语义相邻概念的显式保护，导致擦除一个概念时整个细粒度类别（如特定犬种或花卉）的生成质量下降。NLCE在表示层面引入了**邻居感知的谱加权调制**，将问题分解为目标抑制与邻居增强两个互补操作。

具体而言，方法首先对目标概念嵌入进行低秩SVD分解 $X_{F_c} = U_{F_c} \Sigma_{F_c} V_{F_c}^{\top}$，获得目标子空间的正交基 $U_{F_c}$。随后引入基于奇异值相对重要性的谱调制系数：

$$\lambda_i^{(F_c)} = \frac{\alpha_{\mathrm{target}} \cdot r_i^{(F_c)}}{(\alpha_{\mathrm{target}} - 1) \cdot r_i^{(F_c)} + 1}, \quad r_i^{(F_c)} = \frac{s_i^2}{\sum_j s_j^2}$$

该系数对主导语义方向施加更强的衰减，而对次要方向保持相对完整，实现**选择性抑制**而非粗暴删除。与之对称，方法从外部语料库（Wikipedia标题）中挖掘语义邻居，通过余弦相似度、具体性过滤和CLIP重排序构建邻居子空间，并构建类似的谱加权投影算子 $P_{\mathcal{N}_c}$ 用于增强保留。最终调制算子为：

$$P_c = (I - \beta P_{F_c}) + \gamma P_{\mathcal{N}_c} P_{F_c}$$

其中 $\beta$ 和 $\gamma$ 分别控制目标抑制和邻居增强的强度。该算子随后应用于UNet交叉注意力的Key/Value投影矩阵（$W_K' = P_c W_K$, $W_V' = P_c W_V$），实现全局但语义精准的概念重写。这一设计与GLoCE的门控低秩适配器形成根本差异：GLoCE仅在特定层插入适配器进行局部抑制，而NLCE在表示层面同时完成抑制与增强，为后续空间定位奠定语义基础。

### 从无空间意识到注意力引导的空间门控

表示空间调制虽能大幅削弱目标概念，但无法完全消除残余激活——尤其在目标概念与邻居共享视觉特征时。现有方法（如GLoCE）缺乏对残余激活的空间定位能力，只能依赖固定的门控区域。NLCE引入**注意力引导的空间门控**，利用交叉注意力图本身作为定位信号。

方法在去噪过程的特定时间步提取目标token的交叉注意力图，求和得到空间门：

$$G_t(x,y) = \sum_{j \in F_{c,\mathrm{live}}} A_t^\ell(x,y,j)$$

该门控图指示了目标概念在空间中的残余激活区域。在第二次前向传递中，方法根据该门控图抑制目标token的注意力流：

$$A^\ell(x,y,j) \gets (1 - G_t(x,y)) \cdot A^\ell(x,y,j), \quad \text{if } j \in F_{c,\mathrm{live}}$$

这一设计的巧妙之处在于：门控信号源自模型自身的注意力机制，无需外部检测器或分割模型，实现了**自监督的空间定位**。消融实验（Figure 9）表明，在Stage 1基础上添加Stage 2可显著提升目标擦除准确率（Acc_t）和调和平均（H_o），同时不损害非目标内容的生成质量。

### 从软抑制到门控硬擦除的不可逆移除

即使经过表示调制和注意力抑制，目标概念的痕迹仍可能以微弱特征形式残留在潜在表示中。NLCE的第三阶段引入**门控硬擦除**，在空间门控区域内将特征直接置零，实现不可逆的概念移除。

方法将空间门上采样至特征图分辨率并阈值化，生成二值掩码：

$$\mathbf{1}_t^\ell(x,y) = \begin{cases} 1, & G_t^\ell(x,y) \geq \delta_{\mathrm{scrub}} \\ 0, & \text{otherwise} \end{cases}$$

随后在门控区域内执行硬擦除：

$$h_t^\ell(x,y) \gets \begin{cases} \mathbf{0}, & \mathbf{1}_t^\ell(x,y)=1 \\ h_t^\ell(x,y), & \text{otherwise} \end{cases}$$

这一由粗到精的三阶段设计形成了清晰的因果链条：**表示调制提供全局语义基础，注意力门控实现空间定位，硬擦除完成不可逆清除**。消融实验证实，完整三阶段流水线在四个数据集上均取得最佳的综合性能，且生成质量（CLIP Score、KID）未因擦除强度增加而退化。

### 方法谱系与知识库定位

NLCE在概念擦除方法谱系中占据独特位置。相较于训练式方法（如**ESD-x**、**MACE**、**SPM**）需要针对每个目标概念进行微调，NLCE保持了免训练的灵活性，仅需预计算投影算子（约480秒）。相较于免训练的全局方法（如**UCE**、**RECE**），NLCE首次将邻居感知引入表示空间调制。相较于同为免训练局部方法的**GLoCE**，NLCE通过三阶段递进设计实现了更强的擦除-保留平衡：在Oxford Flowers的Alpine Sea Holly概念上，NLCE的Acc_t为0.00（完全擦除）而Acc_r达82.06，H_o为90.15，显著优于GLoCE的Acc_t 32.00、Acc_r 78.91和H_o 73.05（Table 1）。在名人身份擦除中，NLCE在保持最高Acc_r的同时实现了最低的Acc_t（Table 2），且非目标区域的LPIPS值低于SLD（Figure 4），证明了其空间定位的精确性。

NLCE的邻居挖掘机制依赖于外部语料库和预训练CLIP模型，当目标概念存在文本歧义时（如“Chow”既可指犬种也可指食物），邻居识别失败会导致擦除效果下降（Figure 13）。这一局限揭示了当前方法的边界：邻居感知的有效性高度依赖于概念在嵌入空间中的语义清晰度。

NLCE 是一个**免训练**的三阶段概念擦除框架，其核心设计思路是将擦除问题从“全局抑制”重构为“邻居感知的局部移除”。整体流水线如图2所示，三个阶段的递进关系遵循由粗到精的定位逻辑：

**阶段一：表示空间调制 (Representation-Space Modulation)** —— 在词元嵌入层面进行谱加权投影，衰减目标概念子空间方向，同时通过低秩重注入增强语义邻居子空间。该阶段输出修改后的交叉注意力投影矩阵 $W_K', W_V'$，为后续阶段提供全局概念抑制基础。

**阶段二：注意力引导空间门控 (Attention-Guided Spatial Gating)** —— 利用交叉注意力图定位残余概念激活的空间区域，生成连续空间门 $G_t(x,y)$，并对目标token的注意力流进行抑制。该阶段将全局调制无法完全消除的局部激活标记出来。

**阶段三：门控特征清理 (Gated Feature Clean-up)** —— 将空间门阈值化为二值掩码 $\mathbf{1}_t^\ell(x,y)$，在门控区域内对潜在特征执行硬擦除（置零），实现不可逆的局部概念移除。

三个阶段的组合是递进且互补的：消融实验（图9）表明，仅使用阶段一即可在Oxford Flowers上获得最高的CLIP Score（32.18），说明表示调制是保留整体生成质量的关键；加入阶段二和阶段三后，目标擦除准确率（Acc_t）和调和平均（H_o）进一步提升，且未损害非目标内容的生成质量。这种“先全局抑制、再空间定位、最后硬擦除”的流水线设计，使得NLCE在不同粒度的擦除任务上均能自适应调节：对于简单案例早期阶段已足够，而完整流水线则在不牺牲生成质量的前提下强化擦除效果。

**邻居挖掘预处理模块** 作为流水线的前置步骤，从外部语料库（Wikipedia标题）中通过余弦相似度检索、具体性过滤和CLIP重排序，为每个目标概念构建语义邻居子空间 $P_{\mathcal{N}_c}$。该模块的输出直接嵌入阶段一的调制算子 $P_c = (I - \beta P_{F_c}) + \gamma P_{\mathcal{N}_c} P_{F_c}$ 中，是“邻居感知”特性的关键支撑。

NLCE 的核心由**邻居感知的表示空间调制**、**注意力引导的空间门控**和**门控硬擦除**三个阶段构成，形成由粗到精的概念擦除流程。

### 邻居概念挖掘（预处理）

在擦除目标概念 $F_c$ 之前，NLCE 首先从外部语料库（如 Wikipedia 标题）中挖掘其语义邻居集合 $\mathcal{N}_c$。具体流程为：计算候选词元与目标概念的余弦相似度，经具体性过滤后，利用 CLIP 重排序筛选出与目标概念语义相近但非同一实体的邻居概念。这些邻居随后被用于构建增强保留的子空间（详见附录 Table 8 的各概念 Top-10 邻居列表）。该步骤为后续表示调制提供了必要的邻居结构信息。

### Stage 1：表示空间调制

第一阶段在词元表示层面操作，目标是在抑制目标概念语义的同时，稳定并增强邻居概念的表示。

**目标子空间分解**：对目标概念 $F_c$ 的嵌入矩阵进行低秩 SVD 分解：

$$X_{F_c} = U_{F_c} \Sigma_{F_c} V_{F_c}^{\top}, \quad U_{F_c} \in \mathbb{R}^{d \times r}$$

其中 $U_{F_c}$ 是 $d \times r$ 的正交矩阵，张成目标概念的 $r$ 维语义子空间。

**谱加权调制**：根据奇异值的相对重要性计算调制系数，对主导语义方向施加更强的抑制：

$$\lambda_i^{(F_c)} = \frac{\alpha_{\mathrm{target}} \cdot r_i^{(F_c)}}{(\alpha_{\mathrm{target}} - 1) \cdot r_i^{(F_c)} + 1}, \quad r_i^{(F_c)} = \frac{s_i^2}{\sum_j s_j^2}$$

其中 $s_i$ 为第 $i$ 个奇异值，$r_i^{(F_c)}$ 衡量该方向的相对能量占比，$\alpha_{\mathrm{target}} \in [0,1]$ 控制整体抑制强度（$\alpha_{\mathrm{target}}=0$ 表示完全抑制，$\alpha_{\mathrm{target}}=1$ 表示不抑制）。

**投影算子构建**：利用调制系数构建谱加权投影算子：

$$P_{F_c} = U_{F_c} \Lambda_{F_c} U_{F_c}^{\top}, \quad \Lambda_{F_c} = \operatorname{diag}(\lambda_1^{(F_c)}, \dots, \lambda_r^{(F_c)})$$

对邻居概念 $\mathcal{N}_c$ 同理构建增强投影算子 $P_{\mathcal{N}_c}$。

**最终调制算子**：将目标抑制与邻居增强组合为统一的调制算子：

$$P_c = (I - \beta P_{F_c}) + \gamma P_{\mathcal{N}_c} P_{F_c}$$

其中 $\beta$ 控制目标擦除强度，$\gamma$ 控制邻居增强强度。交叉项 $P_{\mathcal{N}_c} P_{F_c}$ 确保增强操作仅作用于已被抑制的目标子空间方向，避免对无关语义的干扰。

**交叉注意力重写**：将调制算子应用于 UNet 交叉注意力层的键（Key）和值（Value）投影矩阵，实现全局一致的概念移除：

$$W_K' = P_c W_K, \quad W_V' = P_c W_V$$

**多概念组合**：对于多概念擦除场景，通过组合各检测概念的算子实现：

$$P_{\mathrm{multi}} = \prod_{c \in \mathcal{A}} P_c$$

### Stage 2：注意力引导的空间门控

第一阶段在表示层面进行全局调制后，残差概念激活可能仍存在于特定空间区域。第二阶段利用交叉注意力图定位这些残余区域。

**空间门生成**：对 UNet 第 $\ell$ 层，求和所有存活目标词元的注意力图，得到空间门：

$$G_t(x,y) = \sum_{j \in F_{c,\mathrm{live}}} A_t^\ell(x,y,j)$$

其中 $F_{c,\mathrm{live}}$ 为当前仍激活的目标词元集合，$A_t^\ell(x,y,j)$ 为时间步 $t$ 时位置 $(x,y)$ 对词元 $j$ 的注意力权重。

**注意力抑制**：在第二次前向传递中，根据空间门抑制目标词元的注意力流：

$$A^\ell(x,y,j) \gets (1 - G_t(x,y)) \cdot A^\ell(x,y,j), \quad \text{if } j \in F_{c,\mathrm{live}}$$

这一定位机制使擦除操作聚焦于目标概念实际激活的空间区域，避免对非目标区域的误伤。

### Stage 3：门控硬擦除

为确保不可逆的概念移除，第三阶段在潜在特征空间执行硬擦除。

**二值掩码生成**：将空间门上采样至特征图分辨率后，通过阈值化生成二值掩码：

$$\mathbf{1}_t^\ell(x,y) = \begin{cases} 1, & G_t^\ell(x,y) \geq \delta_{\mathrm{scrub}} \\ 0, & \text{otherwise} \end{cases}$$

其中 $\delta_{\mathrm{scrub}}$ 为擦除阈值，控制硬擦除的激进程度。

**特征置零**：在门控区域内将特征向量置为零：

$$h_t^\ell(x,y) \gets \begin{cases} \mathbf{0}, & \mathbf{1}_t^\ell(x,y)=1 \\ h_t^\ell(x,y), & \text{otherwise} \end{cases}$$

这一操作不可逆地消除了残余概念激活，确保擦除的彻底性。

### 三阶段递进机理

三个阶段形成由粗到精的递进关系：Stage 1 在全局表示层面进行语义调制，是保留生成质量的关键（消融实验表明仅 Stage 1 即可获得最高 CLIP Score）；Stage 2 引入空间定位能力，将擦除聚焦于目标区域；Stage 3 执行不可逆的硬擦除，消除前两阶段可能遗漏的残余痕迹。消融实验（Figure 9）证实，完整三阶段流水线在目标擦除（Acc_t）和综合指标（H_o）上均优于部分阶段组合，且不损害非目标内容的生成质量。

## 实验与关键发现

### 核心瓶颈与设计逻辑

现有局部概念擦除方法（如 **GLoCE**）在抑制目标概念时，会无意中削弱语义相邻概念——即产生“邻居间隙”（neighbor gap），导致细粒度领域的保真度显著下降。NLCE 的设计逻辑正是围绕这一瓶颈展开：概念擦除不仅是目标抑制问题，还需**显式维护语义邻居结构**。通过将表示空间调制、空间注意力门控和硬擦除组合为由粗到精的三阶段流程，NLCE 在不降低整体生成质量的前提下，实现了更满足实际应用需求的局部概念移除。

### 主实验结果

#### 细粒度类别擦除：Oxford Flowers 与 Stanford Dogs

Table 1 给出了在 Oxford Flowers 和 Stanford Dogs 两个细粒度数据集上的定量对比。NLCE 在所有目标概念上均实现了最优或接近最优的平衡。

![[assets/figures/papers/paper_list_l2329_https_arxiv_org_abs_2603_25994/figures/003_Table_1.jpg]]
*Table 1: Quantitative Comparison of Oxford Flowers and Stanford Dogs Erasure. Our NLCE achieves a superior balance between the target erasure and neighbor concepts preservation while maintain the quality*

- **Oxford Flowers - Alpine Sea Holly**：NLCE 将目标准确率 Acc$_t$ 降至 **0.00**，同时保留准确率 Acc$_r$ 达到 **82.06**，调和平均 H$_o$ 高达 **90.15**，CLIP Score 为 32.18，KID 仅 0.03。相比之下，GLoCE 的 Acc$_t$ 为 32.00，Acc$_r$ 为 78.91，H$_o$ 仅 73.05。NLCE 在完全擦除目标的同时，将 H$_o$ 提升了 **+17.10**，且生成分布偏移（KID）显著更低。
- **Stanford Dogs - Bluetick**：NLCE 的 Acc$_t$ 为 **0.00**，Acc$_r$ 为 **75.91**，H$_o$ 为 **86.31**。最强基线 SLD 的 Acc$_t$ 为 8.00，Acc$_r$ 为 66.62，H$_o$ 为 77.28。NLCE 在擦除更彻底的前提下，保留率高出 **+9.29**，H$_o$ 提升 **+9.03**。

Figure 3 的定性对比进一步验证：NLCE 在移除 “Alpine Sea Holly” 后，生成的图像自然转向 “Rose” 或 “Spring Crocus” 等邻居类别，而非产生语义混乱的输出；在 Stanford Dogs 上，擦除 “Bluetick” 后仍能保持 “Beagle” 等视觉相似犬种的正常生成。

![[assets/figures/papers/paper_list_l2329_https_arxiv_org_abs_2603_25994/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of Oxford Flowers and Stanford Dogs Erasure. Top: Oxford Flowers — NLCE effectively removes the target concept ’Alpine Sea*

#### 名人身份擦除

Table 2 展示了名人身份擦除的定量结果。以 Anna Kendrick 为例，NLCE 的 Acc$_t$ 为 **0.00**，Acc$_r$ 为 **94.00**，H$_o$ 为 **96.91**。GLoCE 的 Acc$_t$ 为 1.33，Acc$_r$ 为 94.67，H$_o$ 为 96.63。NLCE 在擦除更彻底的同时，保留率几乎持平（-0.67），综合指标 H$_o$ 略优（+0.28）。

![[assets/figures/papers/paper_list_l2329_https_arxiv_org_abs_2603_25994/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of Celebrity Erasure. NLCE provides a balanced trade-off between effective target-identity removal and preservation of remaining celebrities*

Figure 4 进一步从局部保真度角度提供了关键证据：NLCE 在非目标区域的 LPIPS 值低于 SLD，且在三个目标名人中优于 GLoCE，证明其**空间局部化擦除**有效降低了对非目标区域的感知损伤。

#### 显式内容擦除（I2P 数据集）

Figure 6 给出了 I2P 数据集上各方法的 NudeNet 检出数对比。NLCE 的总检出数（81）低于所有基线方法，在多数类别上实现了最强的擦除效果。同时，NLCE 保持了 **29.70** 的 CLIP Score，高于同等擦除强度的 RECE（29.41），表明其在抑制显式内容的同时更好地保留了非敏感内容的生成质量。Figure 7 的定性样本显示，NLCE 在 I2P 提示和 COCO Captions 正常提示上均能生成合理图像。

![[assets/figures/papers/paper_list_l2329_https_arxiv_org_abs_2603_25994/figures/008_Figure_6.jpg]]
*Figure 6: Quantitative Comparison on I2P Dataset. The number following each category represents the number of nude items generated by original SD, while each bar illustrates the success rate of erasing the corresponding nude items for each method. NLCE outperforms other baselines in most of categories and in total number of detected items*

#### 艺术风格擦除

Appendix G 的 Table 10 报告了 Van Gogh 风格擦除的 LPIPS 和 QA 指标。NLCE 的 LPIPS$_t$（目标区域感知变化）为 0.45，LPIPS$_r$（保留区域）仅 0.06，Acc$_t$ 为 0.55，Acc$_r$ 为 0.97。相比之下，ESD-x 的 LPIPS$_t$ 为 0.40，LPIPS$_r$ 却高达 0.26。NLCE 在风格去除更彻底（Acc$_t$ 低 0.20）的同时，对非目标风格的保留显著更优（LPIPS$_r$ 低 0.20）。Figure 8 的定性对比直观展示了 NLCE 在擦除 Van Gogh 风格后仍能完好保留 Picasso 和 Warhol 风格。

#### 多概念擦除

Table 3 报告了 10 类狗/花的多概念擦除结果。NLCE 的 Acc$_t$ 为 26.80，Acc$_r$ 为 **91.90**，H$_o$ 为 **81.49**，CLIP Score 为 34.94，KID 仅 0.02。虽然 MACE 的 Acc$_t$ 达到 0.00，但其 Acc$_r$ 仅 42.58，H$_o$ 仅 59.73，KID 高达 0.96——说明 MACE 以严重损害非目标内容为代价实现擦除。NLCE 在擦除大部分目标概念的同时，保留率高出 MACE **+49.32**，H$_o$ 提升 **+21.76**，且生成分布几乎无偏移。

### 消融实验

Figure 9 展示了在四个数据集上对 NLCE 三阶段的递进消融。

![[assets/figures/papers/paper_list_l2329_https_arxiv_org_abs_2603_25994/figures/011_Figure_9.jpg]]
*Figure 9: Ablation study on the four datasets across model stages (Stage 1, Stage 1+2, and Stage 1+2+3). Our NLCE adapts to each dataset: early stages suffice for easier cases, while full pipeline strengthens erasure without harming non-target content as well as generative quality*

- **Stage 1 单独使用**：在 Oxford Flowers 上获得最高的 CLIP Score，表明表示空间调制是保留整体生成质量的核心模块。
- **加入 Stage 2 和 Stage 3**：随着注意力门控和硬擦除的加入，Acc$_t$ 持续改善，H$_o$ 同步提升，且未损害非目标内容的生成质量。这验证了由粗到精的流水线设计：表示调制奠定基础，空间门控定位残余，硬擦除实现不可逆消除。

参数敏感性方面，Table 5 和 Table 6 分别报告了 $(\beta, \gamma)$ 在细粒度数据集和 Celebrity 数据集上的影响。在 Celebrity 上，$\beta=1, \gamma=0.9$ 时取得最优平衡（Mean Acc$_t$ 0.44, Mean Acc$_r$ 94.67, H$_o$ 97.05）；降低 $\gamma$ 会降低保留率，增加 $\gamma$ 则减弱擦除强度。Table 7 表明在 I2P 数据集上，$\delta_{\mathrm{token}}$ 有助于过滤非目标 token，但需与 $\gamma$ 协同调节以平衡擦除强度与生成质量。

### 失败模式与局限性

NLCE 并非在所有场景下都有效。Figure 13 展示了一个典型失败案例：目标概念 “Chow” 因文本歧义（可指犬种或食物），导致邻居挖掘阶段无法识别合适的语义邻居集合，最终擦除无效。这暴露了方法对文本嵌入模型和外部语料库的依赖——当目标概念存在歧义或属于低资源领域时，邻居子空间构建可能失败。

![[assets/figures/papers/paper_list_l2329_https_arxiv_org_abs_2603_25994/figures/026_Figure_13.jpg]]
*Figure 13: Qualitative Example of Ineffective Erasure. Due to textual ambiguity, NLCE has difficulty identifying an appropriate neighborhood set, resulting in ineffective erasure of the target concept*

在多概念擦除中，个别概念的邻居识别失败会拖累整体效果。例如 “Chow” 概念导致 Acc$_t$ 出现 0.1 的残留。

显式内容擦除场景下，在平衡超参数下可能无法完全消除裸露内容——需要调整 $\beta$ 和 $\gamma$ 以获得更强擦除，但这会牺牲生成质量。

此外，方法虽为免训练，但需为每个目标概念预计算投影算子（准备时间约 480 秒），对实时交互式场景仍有延迟。邻居挖掘过程依赖 Wikipedia 语料和预训练 CLIP 模型，可能未涵盖所有领域概念。

### 鲁棒性评估

Table 11 报告了 Ring-A-Bell 攻击下的擦除成功率。NLCE 展现出较强的抗攻击能力，攻击成功率低于多数基线，表明其硬擦除机制（Stage 3 的置零操作）对对抗性提示具有较好的鲁棒性。

### 计算开销

Table 9 给出了 10 概念擦除的时间消耗对比。NLCE 使用单张 NVIDIA A100 GPU，擦除一个概念并生成 10 张图像的总时间在可接受范围内。预计算投影算子的开销（约 480 秒）是主要瓶颈，但这是一次性成本，后续推理无额外训练开销。

## 定位与知识库关联

### 概念擦除的范式定位

NLCE属于**免训练（training-free）局部概念擦除**方法，其核心区别于现有工作之处在于显式建模并保护**语义邻居结构**。现有概念擦除方法可沿两个维度划分：

**训练式 vs 免训练**。训练式方法通过微调模型参数实现概念遗忘，典型代表包括：**ESD**（单概念/多概念变体ESD-x/ESD-u）通过梯度反转引导模型远离目标概念；**SPM**在频谱域调制参数以抑制特定语义；**MACE**支持多维概念擦除，但训练开销大且容易损害全局生成能力。免训练方法则直接操作推理过程或模型权重，避免重训练成本：**UCE**通过编辑交叉注意力图实现概念抑制；**RECE**采用闭式权重编辑公式；**SLD**在潜空间施加安全约束；**AdaVD**自适应调整视觉方向。NLCE继承免训练路线的轻量优势，但通过三阶段流水线实现了更精细的控制粒度。

**全局擦除 vs 局部擦除**。早期方法（ESD、UCE等）多为全局擦除，即一旦激活擦除机制，整个生成过程均受影响，容易误伤非目标内容。**GLoCE**首次引入局部擦除思想，通过门控低秩适配器在空间上限制擦除范围。NLCE在此基础上进一步指出：仅做空间局部化是不够的——即使擦除区域精确，若在表示层面不保护语义邻居，仍会导致“邻居间隙”（neighbor gap），即擦除“阿尔卑斯海冬青”会连带削弱“玫瑰”等相近花卉的生成质量。这一洞察构成了NLCE的方法学贡献边界。

### 核心机制对比

NLCE的三阶段设计在机制层面与现有方法形成清晰对照：

| 机制维度 | 代表基线 | NLCE对应设计 | 关键差异 |
|---------|---------|-------------|---------|
| 表示层抑制 | RECE（闭式权重编辑） | Stage 1：谱加权嵌入调制 | RECE仅抑制目标方向；NLCE同时构建邻居子空间投影 $P_{\mathcal{N}_c}$ 进行增强保留 |
| 空间定位 | GLoCE（门控低秩适配器） | Stage 2：注意力引导空间门 $G_t$ | GLoCE使用单一适配器门控；NLCE利用交叉注意力图动态定位残余激活，更精确 |
| 不可逆擦除 | SLD（潜空间安全约束） | Stage 3：门控硬擦除（特征置零） | SLD施加软约束可能被绕过；NLCE在门控区域内执行硬置零，消除残留痕迹 |

关键公式体现了NLCE的组合创新。最终调制算子 $P_c = (I - \beta P_{F_c}) + \gamma P_{\mathcal{N}_c} P_{F_c}$ 将目标抑制（通过谱加权投影 $P_{F_c}$）与邻居增强（通过 $P_{\mathcal{N}_c}$）统一在一个线性算子中，然后直接作用于交叉注意力的Key/Value投影矩阵 $W_K' = P_c W_K, W_V' = P_c W_V$。这种设计避免了额外推理开销，且与多概念擦除自然兼容：$P_{\mathrm{multi}} = \prod_{c \in \mathcal{A}} P_c$。

### 适用边界与局限

**适用场景**。NLCE在以下条件下表现最优：（1）目标概念与邻居概念在语义嵌入空间中具有清晰边界（如Oxford Flowers中的不同花卉品种）；（2）邻居概念可通过外部语料库（Wikipedia标题）可靠挖掘；（3）擦除需求为细粒度局部擦除而非全局概念移除。

**已知局限**。

1. **语义歧义敏感性**。当目标概念存在文本歧义时，邻居挖掘失效。如“Chow”既可指犬种也可指食物，导致邻居集合不匹配，擦除效果显著下降（多概念擦除中该概念的Acc_t出现异常值）。Figure 13展示了这一失效案例。

2. **外部依赖瓶颈**。邻居挖掘依赖Wikipedia语料和CLIP重排序，对低资源概念或领域外概念覆盖不足。预计算投影算子约需480秒（Table 9），限制了实时交互式应用。

3. **超参数权衡**。在显式内容擦除（I2P）场景中，$\beta$和$\gamma$的平衡尤为敏感：增强擦除强度（提高$\beta$）会降低CLIP Score；增强保留（提高$\gamma$）则可能残留裸露内容。Table 7展示了这一权衡。

4. **多概念擦除的累积效应**。当擦除10个狗类概念时，NLCE的Acc_t为26.80（Table 3），表明部分目标未被完全擦除。这源于个别概念的邻居识别失败会通过算子组合 $P_{\mathrm{multi}}$ 传播影响。

5. **对抗鲁棒性未充分验证**。Table 11显示Ring-A-Bell攻击下的成功率，但更广泛的对抗攻击（如提示注入、图像扰动）的鲁棒性尚不明确。

### 开放问题

1. **邻居挖掘的自动化与去外部化**。当前方法依赖Wikipedia和CLIP重排序，能否直接从T2I模型的嵌入空间或生成统计中自动发现语义邻居，消除外部知识库依赖？

2. **实时擦除与动态概念管理**。预计算开销（~480秒/概念）限制了交互式场景。能否通过缓存共享子空间、增量SVD更新或轻量化邻居表示来支持动态添加/移除擦除目标？

3. **跨架构迁移性**。NLCE在Stable Diffusion 1.4上验证，其对DiT、SDXL、SD3等不同架构（特别是非UNet backbone）的迁移性尚未探索。交叉注意力重写策略能否直接适配？

4. **邻居边界的理论界定**。当前邻居选择基于余弦相似度和具体性过滤，缺乏形式化标准。如何界定“足够近以需保护”与“足够远以可牺牲”之间的边界，避免过度保护导致擦除不彻底？

5. **邻居感知范式的拓展**。邻居保护的思想能否迁移到其他模型编辑任务？例如知识编辑中保护相关知识、去偏中保护相关属性、或连续学习中的灾难性遗忘缓解。

6. **极端细粒度场景**。对于视觉高度相似的概念（如犬种的亚型、花卉的变种），现有基于文本嵌入的邻居挖掘可能无法区分。是否需要引入视觉特征辅助邻居识别？

## 原文 PDF

![[paperPDFs/CVPR_2026/Neighbor_Aware_Localized_Concept_Erasure_in_Text_to_Image_Diffusion_Models.pdf]]

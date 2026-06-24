---
title: Cross-Hand Latent Representation for Vision-Language-Action Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Cross_Hand_Latent_Representation_for_Vision_Language_Action_Models.pdf
project_link: "https://xl-vla.github.io"
code_link: null
aliases:
- XV
- CHLRVLAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入一个共享的隐式动作空间，通过无监督的跨手型自编码器学习与手型无关的动作表示，使得VLA模型在统一的隐空间中操作，无需为每个手型单独训练或重定向。
primary_logic: 利用多头的VAE框架，结合关节重建损失、基于指尖可微正运动学的pinch几何对齐损失，以及KL正则化，完全通过自监督方式学习一个平滑对齐的跨手型隐空间；无需任何配对数据即可实现隐式动作在不同手型之间的交换和重用。
claims:
- 在四个灵巧手、10个任务的跨手型训练中，XL-VLA平均成功率从π0的0.32提升到0.72，相对提升约125%。
- 在零样本任务泛化实验中，XL-VLA在所有手型-任务组合中都一致超越基于运动学重定向的π0+RT基线。
- 在G1人形机器人跨手型实验中，XL-VLA成功率达到0.825，显著优于π0的0.525（提升57%）。
- 多灵巧手（Ability, Inspire, Paxini, X-Hand）多任务（10 tasks） 上 Mean Success Rate = 0.72
---

# Cross-Hand Latent Representation for Vision-Language-Action Models

> [!tip] 核心洞察
> 利用多头的VAE框架，结合关节重建损失、基于指尖可微正运动学的pinch几何对齐损失，以及KL正则化，完全通过自监督方式学习一个平滑对齐的跨手型隐空间；无需任何配对数据即可实现隐式动作在不同手型之间的交换和重用。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于视觉-语言-动作模型的跨手型隐式表征 |
| 英文题名 | Cross-Hand Latent Representation for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10158) · [Project](https://xl-vla.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | XL-VLA |
| Dataset | 多灵巧手（Ability, Inspire, Paxini, X-Hand）多任务（10 tasks）, G1 人形机器人（4 tasks: PF, HB, PS, PoS） |

> [!tip] 效果简介
> - 多灵巧手（Ability, Inspire, Paxini, X-Hand）多任务（10 tasks） 上，Mean Success Rate 0.72 vs 0.32 (π0) (+0.40 (+125%))。
> - G1 人形机器人（4 tasks: PF, HB, PS, PoS） 上，Mean Success Rate 0.825 vs 0.525 (π0) (+0.30 (+57%))。
> - 零样本任务泛化 (unseen task-hand combinations) 上，Success Rate (SR) / Partial Success Rate (PSR) 在所有组合中显著优于 π0+RT vs π0+RT (大幅领先（无具体数字）)。

## 概述

**核心问题。** 灵巧手在抓取与操作任务中展现出巨大潜力，但不同手型之间关节数量、运动学结构和动作空间差异极大。直接在原始关节空间上训练统一的视觉-语言-动作（VLA）模型极为困难：模型必须同时适应异构的动作维度，且难以将一种手型上学到的技能迁移到另一种手型，更无法泛化到全新出现的机械手。现有的运动学重定向方案依赖手工设计的映射规则，通用性差且无法利用多手型数据联合训练。

**本文方案。** 论文引入 **XL-VLA**，一个基于跨手型隐式表征的视觉-语言-动作框架。其核心思路是：在 VLA 模型与具体手型之间插入一个**共享的隐式动作空间**，通过无监督的跨手型自编码器学习与手型无关的动作表示。具体而言，为每种手型训练一对编码器 $E_h$ 和解码器 $D_h$，将异构的关节动作块映射到统一的 32 维隐向量 $\mathbf{z}$，再由 VLA 模型在该隐空间中完成感知、推理与动作预测。训练时，隐空间自编码器通过三项损失联合优化：关节重建损失 $L_1$、基于可微正运动学的指尖夹持几何对齐损失 $L_2$，以及 KL 正则化损失 $L_3$。整个对齐过程完全自监督，无需任何配对数据。

**方法定位。** 与直接操作原始关节空间的 **π0** 基线相比，XL-VLA 的关键差异在于动作表示层：将 VLA 的输入/输出从手型特定的关节 token 替换为跨手型共享的隐式 token，并在 VLA 微调期间冻结预训练好的编码器/解码器。在跨手型隐空间方法中，XL-VLA 区别于需要监督数据的 **LAD**（Latent Action Diffusion），实现了完全无监督的隐空间对齐。

**主要结果。** 在四种灵巧手（Ability、Inspire、Paxini、X-Hand）与 10 个任务的跨手型训练中，XL-VLA 平均成功率达到 **0.72**，相比 π0 的 0.32 相对提升约 **125%**（Table 2）。在零样本任务泛化实验中，XL-VLA 在所有手型-任务组合中一致超越基于运动学重定向的 π0+RT 基线（Figure 4）。在 G1 人形机器人跨手型实验中，XL-VLA 成功率达到 **0.825**，显著优于 π0 的 0.525（Table 6）。消融实验进一步验证了 32 维隐空间在重建精度、重定向误差和插值平滑性上的综合最优性（Table 5）。

## 背景与动机

### 问题背景：灵巧手异构性带来的跨手型控制瓶颈

视觉-语言-动作（VLA）模型在通用机器人操控中展现出巨大潜力，但其应用主要集中在单一机械臂或固定末端执行器上。当面对**灵巧手（dexterous hands）**时，一个根本性瓶颈浮现：不同灵巧手具有**异构的动作空间**——关节数量、自由度、运动学结构各不相同（如Table 3所示，Ability Hand、Inspire Hand、Paxini DexH13、X-Hand等手的指节数和自由度差异显著）。这使得训练一个统一的VLA模型来控制多种手型变得极为困难。

现有方法的典型做法是为每种手型独立训练策略，或依赖**运动学重定向（kinematic retargeting）**将一种手的动作映射到另一种手。然而，独立训练忽略了跨手型的数据共享潜力，而运动学重定向则需要手工设计的映射规则，且在面对运动学差异较大的手型时往往产生不自然或不可执行的动作。更关键的是，这两种范式都难以**零样本扩展到新出现的机械手**——每当引入一种新末端执行器，就需要重新训练或重新设计重定向规则。

### 现有方法缺口：缺乏统一的跨手型动作表示

近年来，跨具身（cross-embodiment）学习的研究尝试通过共享表示来连接不同机器人形态。Table 1总结了相关工作在数据来源、部署设置和输入/输出能力上的对比。这些工作大多聚焦于不同机械臂之间的迁移，或使用监督式配对数据进行隐空间对齐。但在灵巧手领域，存在两个关键缺口：

1. **无配对数据的跨手型对齐**：不同灵巧手之间通常不存在一一对应的动作配对数据，监督式对齐方法难以适用。
2. **与VLA管线的深度集成**：现有的隐空间方法多为独立的动作编码-解码模块，未与视觉、语言模态在统一的VLA框架内联合优化。

基线方法 **π0** 直接在不同长度的原始关节空间中操作，通过调整序列长度来适应不同手型，但其跨手型泛化能力有限。**π0+RT** 在单一手型上训练π0，再通过运动学重定向迁移到其他手型，但重定向精度和泛化性受限于手工规则。监督式隐空间方法如 **LAD（Latent Action Diffusion）** 需要配对数据进行隐空间对齐，在实际多手型场景中难以规模化。

### 本文动机：无监督跨手型隐空间与VLA的融合

本文的核心动机是回答一个关键问题：**能否学习一个与手型无关的共享动作表示，使VLA模型在统一的隐空间中操作，从而天然具备跨手型泛化能力？**

为此，本文提出 **XL-VLA**，核心思路是引入一个**无监督的跨手型自编码器框架**，通过纯粹的自监督学习，将所有异构手型的关节动作映射到一个共享的平滑隐空间。该隐空间的设计目标有三：一是保证同一隐向量在不同手型上解码出**几何语义一致**的抓取姿态（通过基于指尖可微正运动学的pinch几何对齐损失实现）；二是保证隐空间的**连续性和可采样性**（通过KL正则化）；三是**无需任何配对数据**即可完成对齐，使得隐式动作可以在不同手型之间自由交换和重用。

在此基础上，XL-VLA将VLA模型的输入和输出从原始关节空间迁移到该共享隐空间：VLA主干（基于π0）接收由手型编码器生成的隐式token序列，预测未来的隐式动作块，再由手型解码器还原为具体关节命令。这种设计使得VLA模型的训练和推理完全与具体手型解耦，为跨手型训练和零样本泛化奠定了基础。

## 核心创新

XL-VLA 的核心创新在于引入了一个**共享的隐式动作空间**，将异构灵巧手的动作统一表示，从而解决了跨手型视觉-语言-动作模型训练中的根本瓶颈。

### 问题本质与因果机制

不同灵巧手具有异构的动作空间——关节数量、运动学结构各不相同。传统 VLA 模型（如 π0）直接在原始关节位置空间中操作，虽然可以通过调整序列长度适应不同手型，但缺乏跨手型的语义对齐，导致训练效率低下且难以泛化。基于运动学重定向的 π0+RT 基线同样面临困境：重定向过程本身引入误差，且需要针对每对手型设计映射规则。

XL-VLA 的核心洞察是：**将动作空间从“手型相关”的关节位置提升为“手型无关”的隐式表征**。通过无监督的跨手型自编码器框架，模型学习到一个平滑对齐的隐空间，使得 VLA 模型可以完全在统一空间中操作，无需为每个手型单独训练或重定向。

### 关键 Changed Slots

| 设计维度 | 基线方法（π0 / π0+RT） | XL-VLA 方案 |
|---------|----------------------|------------|
| **动作表示** | 每种手型独立的原始关节位置空间 | 所有手型共享的 32 维隐式向量 z |
| **VLA 模型输入** | 直接堆叠的关节状态 token | 由手型编码器 E_h 生成的隐式 token 序列 |
| **策略输出与解码** | 直接预测下一关节动作块 | 预测下一隐式动作块，再由手型解码器 D_h 还原为关节命令 |
| **手型对齐机制** | 无（直接操作不同长度关节序列）或依赖运动学重定向 | 通过冻结的 E_h/D_h 对隐空间进行统一，无需配对数据即可对齐 |

### 隐空间构建的三重约束

XL-VLA 的隐空间质量由三个损失函数联合保证：

- **重建损失 L1**：确保每个手型的编码-解码循环保持关节精度，MSE 在所有手型上取平均。
- **重定向损失 L2**：通过可微正运动学计算指尖夹持几何，对齐源手和目标手之间的 pinch 距离和方向，使隐式动作在不同手型上产生语义一致的抓取姿态。
- **KL 正则化损失 L3**：迫使隐空间分布接近标准正态，保证平滑性和可采样性。

三者联合训练目标为：

$$L_{\mathrm{latent}} = L_1 + L_2 + \beta L_3$$

所有手型的编码器和解码器通过一次反向传播联合优化，无需任何配对数据或监督标签。训练完成后，编码器 E_h 和解码器 D_h 被冻结，VLA 骨干网络在隐空间中进行微调。

### 与相关工作的本质区别

Table 1 对比了 XL-VLA 与现有基于隐空间的跨形态方法。关键差异在于：XL-VLA 是首个将**无监督隐式动作对齐**与**完整的 VLA 流水线**结合的工作，同时支持视觉、语言和本体感知的多模态输入，并具备零样本迁移到未见手型-任务组合的能力。相比之下，LAD 等监督式隐空间方法需要配对数据进行重定向训练，限制了其可扩展性。

## 整体框架

XL‑VLA 的核心设计是将异构灵巧手的动作空间统一到一个**共享的隐式动作空间**中，使视觉‑语言‑动作模型（VLA）无需感知底层手型的运动学差异即可进行跨手型推理。整个框架由两条解耦但协同的流水线构成：**隐空间自编码器预训练**与**VLA 策略训练**。

**模块组成与数据流**  
如 Figure 2 所示，系统包含以下关键模块：

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/003_Figure_2.jpg]]
*Figure 2: Model Pipeline. XL-VLA builds on π0 [6] with vision and language encoders paired with an action expert that operates in a shared latent action space for cross-embodiment control. During VLA training, the action expert is finetuned while the pretrained latent encoders and decoders remain frozen*

1. **多模态编码器**：视觉编码器接收相机图像观测，语言编码器编码自然语言指令，二者为 VLA 主干提供场景与任务语义。
2. **手型特定编码器** $E_h$ 与**解码器** $D_h$：每个灵巧手 $h$ 对应一对 MLP 自编码器。编码器将手型 $h$ 的关节动作块 $\mathbf{q}^{(h)}$ 映射为共享隐向量 $\mathbf{z}$（维度 32）；解码器则将 $\mathbf{z}$ 还原为该手型的关节命令 $\hat{\mathbf{q}}^{(h)}$。编码器输出高斯后验参数 $(\boldsymbol{\mu}^{(h)}, \boldsymbol{\sigma}^{(h)})$，通过重参数化采样得到 $\mathbf{z}$。
3. **VLA 主干（基于 π0）**：动作专家（Action Expert）以自回归方式工作——它读取一段隐式历史 token 序列（由 $E_h$ 对历史关节块编码得到），融合视觉与语言 token，预测下一隐式动作块 $\hat{\mathbf{z}}_{t+1}$。
4. **冻结的编解码器**：在 VLA 微调阶段，所有 $E_h$ 和 $D_h$ 保持冻结。策略仅需学习在隐空间中生成动作，预测的 $\hat{\mathbf{z}}_{t+1}$ 再由对应手型的 $D_h$ 实时解码为可执行的关节命令。

**输入‑输出流**  
- **输入**：当前时刻的相机图像 $\mathbf{V}$、语言指令 $\mathbf{T}$，以及由 $E_h$ 编码得到的隐式历史 token。
- **输出**：下一时刻的隐式动作块 $\hat{\mathbf{z}}_{t+1}$，经 $D_h$ 解码后得到目标手型的关节动作块 $\hat{\mathbf{q}}_{t+1}^{(h)}$，直接下发执行。

**预训练对齐机制**  
隐空间的跨手型对齐完全通过**无监督**方式完成（Figure 3）。预训练阶段联合优化三项损失：
- **重建损失** $L_1$：保证各手型自编码的关节重建精度。
- **重定向损失** $L_2$：基于可微正运动学提取指尖 pinch 点对，约束源‑目标手型之间指尖夹持距离和方向的一致性，使同一隐向量在不同手型上产生几何对齐的抓取姿态。
- **KL 正则化** $L_3$：迫使隐分布接近标准正态，保证隐空间的平滑性与可采样性。

总损失 $L_{\text{latent}} = L_1 + L_2 + \beta L_3$ 在所有手型上聚合后统一反向传播，因此所有 $E_h$ 和 $D_h$ 被联合优化，无需任何配对演示数据即可实现跨手型隐式动作的交换与重用。

**与基线的关键差异**  
相比直接在原始关节空间操作的 π0，以及依赖运动学重定向的 π0+RT 基线，XL‑VLA 将 VLA 策略的输入/输出空间从“变长、异构的关节序列”替换为“固定维度、手型无关的隐式 token 序列”。这一设计使得同一策略模型可以无缝控制多种灵巧手，且在新手型出现时只需额外训练该手型的编解码器对，而无需重新训练整个 VLA 策略。

### 补充图表

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/001_Figure_1.jpg]]
*Figure 1: Overview. XL-VLA enables direct decoding of a single latent action into multiple dexterous hand embodiments. Shown above, an action prediction can be instantiated on the Ability hand, Paxini DexH13 hand, X-Hand1, and Inspire hand for languageguided manipulation. We show our experiment settings on the right figure with collected objects and DexHands*

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/020_Figure_15.jpg]]
*Figure 15: G1 Teleoperation System. We build the G1 upperbody teleoperation system from HOMIE [4]. We use a pair of MANUS Mocap glove to track the human hand pose*

## 核心模块与公式推导

### 3.1 跨手型隐式VLA流水线

XL-VLA的核心架构建立在π0的视觉-语言-动作主干之上，通过引入**跨手型隐式动作空间**实现多灵巧手的统一控制。整体流水线包含以下关键模块：

**VLA主干网络（基于π0）**：融合视觉与语言模态，基于隐式历史预测未来的隐式动作块。具体而言，模型以短历史的隐式token序列、视觉token和语言token为条件，预测下一隐式动作块 $\hat{\mathbf{z}}_{t+1}$。

**视觉编码器（Vision Encoder）**：编码相机图像观测 $\mathbf{V}$，生成视觉token。

**语言编码器（Language Encoder）**：编码自然语言指令 $\mathbf{T}$，生成语言token。

**动作专家（Action Expert）**：自回归生成下一隐式动作块，是VLA训练阶段唯一微调的模块。

**手型特定编码器 $E_h$**：将手型 $h$ 的关节动作块 $\mathbf{q}^{(h)}$ 映射到共享隐空间，输出高斯后验参数 $(\boldsymbol{\mu}^{(h)}, \boldsymbol{\sigma}^{(h)})$。

**手型特定解码器 $D_h$**：将共享隐向量 $\mathbf{z}$ 解码还原为手型 $h$ 的关节动作块 $\hat{\mathbf{q}}^{(h)}$。

在VLA微调阶段，所有手型编码器 $E_h$ 和解码器 $D_h$ 保持冻结，仅动作专家参与训练。这一设计确保了隐空间的稳定性和跨手型一致性。

### 3.2 隐空间预训练的关键公式

隐空间的预训练通过三个损失函数联合优化，无需任何配对数据即可实现跨手型对齐。

#### 3.2.1 编码器后验与隐向量采样

对于每个手型 $h$，编码器 $E_h$ 将关节位置映射为高斯分布的参数：

$$(\boldsymbol{\mu}^{(h)}, \boldsymbol{\sigma}^{(h)}) = E_h(\mathbf{q}^{(h)})$$

通过重参数化技巧从近似后验中采样隐向量 $\mathbf{z}$：

$$q(\mathbf{z} \mid \mathbf{q}^{(h)}) = \mathcal{N}(\boldsymbol{\mu}^{(h)}, \mathrm{diag}((\boldsymbol{\sigma}^{(h)})^2))$$

#### 3.2.2 重建损失 $L_1$

重建损失确保每个手型的编码-解码循环能够还原原始关节配置，是所有手型上的均方误差：

$$L_1 = \mathcal{L}_{\mathrm{rec}} = \frac{1}{|\mathcal{H}|} \sum_{h \in \mathcal{H}} \mathrm{MSE}(\hat{\mathbf{q}}^{(h)}, \mathbf{q}^{(h)})$$

其中 $\mathcal{H}$ 为所有手型集合，$\hat{\mathbf{q}}^{(h)}$ 为解码器 $D_h$ 从隐向量 $\mathbf{z}$ 重建的关节位置。

#### 3.2.3 重定向损失 $L_2$

重定向损失是实现**无监督跨手型对齐的核心机制**。它通过可微正运动学计算指尖间的夹持几何（pinch geometry），强制不同手型在隐空间中保持一致的指尖相对关系：

$$L_2 = \frac{1}{|\mathcal{H}|(|\mathcal{H}|-1)|\mathcal{P}|} \sum_{s \neq t} \sum_{(i,j) \in \mathcal{P}} w_{ij}^{(s)} \left[ \lambda_{\mathrm{dis}} \left( \|\boldsymbol{\delta}_{ij}^{(s)}\|_2 - \|\hat{\boldsymbol{\delta}}_{ij}^{(t)}\|_2 \right)^2 + \lambda_{\mathrm{dir}} (1 - c_{ij}^{(s,t)}) \right]$$

**变量含义**：
- $s, t$：分别表示源手型和目标手型
- $\mathcal{P}$：指尖对集合（如拇指-食指、拇指-中指等）
- $\boldsymbol{\delta}_{ij}^{(s)}$：源手型上指尖 $i$ 与 $j$ 之间的三维向量
- $\hat{\boldsymbol{\delta}}_{ij}^{(t)}$：目标手型上通过隐空间重定向后的对应指尖向量
- $w_{ij}^{(s)}$：源手型上指尖对的权重系数
- $c_{ij}^{(s,t)}$：源手和目标手之间指尖方向向量的余弦相似度
- $\lambda_{\mathrm{dis}}, \lambda_{\mathrm{dir}}$：距离项和方向项的平衡系数

该损失同时惩罚指尖距离差异和方向不一致，使得同一隐向量在不同手型上解码出几何一致的抓取姿态。

#### 3.2.4 隐空间正则化损失 $L_3$

KL散度损失迫使隐空间分布接近标准正态分布，保证隐空间的平滑性和可采样性：

$$L_3 = \mathcal{L}_{\mathrm{KL}} = \mathbb{E}_{\mathbf{q}} \left[ \mathrm{KL}\left(q(\mathbf{z} \mid \mathbf{q}) \| \mathcal{N}(\mathbf{0}, \mathbf{I})\right) \right]$$

#### 3.2.5 总隐空间训练损失

三个损失联合优化，所有手型的损失聚合后进行单次反向传播，实现所有编码器和解码器的同步训练：

$$L_{\mathrm{latent}} = L_1 + L_2 + \beta L_3$$

其中 $\beta$ 为KL正则化系数，平衡重建精度与隐空间规范性。

### 3.3 动作预测公式

VLA模型根据前一块动作、视觉和语言指令预测下一块动作：

$$\mathbf{q}_{t+1}^{(h)} = F(\mathbf{q}_{t}^{(h)}, \mathbf{V}, \mathbf{T})$$

在XL-VLA中，该过程在隐空间中完成：动作专家预测 $\hat{\mathbf{z}}_{t+1}$，再由手型解码器 $D_h$ 还原为关节命令 $\hat{\mathbf{q}}_{t+1}^{(h)}$。

### 补充图表

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/004_Figure_3.jpg]]
*Figure 3: Latent space pretraining pipeline. For each hand type, joint positions*

## 实验与分析

### 核心瓶颈与实验动机

灵巧手的跨手型（cross-embodiment）控制面临一个根本性瓶颈：不同机械手具有异构的动作空间——关节数量、运动学结构、驱动方式各不相同。这使得训练一个统一的视觉-语言-动作（VLA）模型极为困难，传统方法要么为每个手型单独训练策略，要么依赖运动学重定向（kinematic retargeting）将单一手型的策略迁移到其他手型，但重定向往往引入几何失真和接触不稳定。XL-VLA 的核心假设是：如果能学习一个与手型无关的共享隐式动作空间，VLA 模型就可以在该空间中统一操作，从根本上规避异构动作空间的冲突。

实验设计围绕三个递进层次展开：（1）多手型多任务策略学习的绝对性能提升；（2）零样本任务-手型组合泛化能力；（3）隐空间本身的质量评估与消融分析。所有实验均在真实硬件上执行，每项设置重复 10 次，物体随机初始化，关节初始状态保持一致。

### 主要结果：跨手型 VLA 性能

**Table 2** 给出了核心对比结果。在四种灵巧手（Ability、Inspire、Paxini、X-Hand）和 10 个操作任务上，XL-VLA 的平均成功率达到 **0.72**，而直接操作原始关节空间的 π0 基线仅为 **0.32**，相对提升约 **125%**。这一差距在所有手型-任务组合中一致出现，表明隐空间统一带来的收益是系统性的，而非个别手型的特例。

从手型维度看，Ability Hand 的整体成功率从 0.37 提升至 0.73，Inspire Hand 从 0.30 提升至 0.68，Paxini DexH13 从 0.28 提升至 0.70，X-Hand 从 0.33 提升至 0.77。值得注意的是，π0 本身已具备通过调整序列长度来处理不同手型的能力，但其在关节空间中的跨手型泛化极为有限。XL-VLA 的增益来自一个关键设计：VLA 主干在冻结的隐式编解码器之上微调，动作专家（Action Expert）始终在统一的 32 维隐空间中自回归生成动作块，而非直接预测关节位置。

**Figure 4** 展示了更具挑战性的零样本任务泛化实验。对于每种手型，随机选择部分任务作为未见任务（其数据完全从训练集中剔除），然后测试模型在这些未见任务上的表现。XL-VLA 在所有手型-任务组合中一致超越基于运动学重定向的 π0+RT 基线，且在多个组合上领先幅度显著。论文同时报告了部分成功率（PSR），用于衡量双臂任务中仅一只手臂完成任务的情况，XL-VLA 在该指标上同样占优。这一结果表明，对齐良好的隐空间不仅提升了同分布任务的表现，还赋予了模型对未见任务-手型组合的泛化能力。

### G1 人形机器人跨形态实验

为进一步验证隐空间方法在更广泛形态上的适用性，论文在 G1 人形机器人上进行了跨形态共训练实验（**Table 6**，**Figure 5**）。G1 实验涉及 4 个任务（PF、HB、PS、PoS），比较了使用隐空间共训练（联合 xArm 和人形机器人数据）与使用原始关节动作训练的性能差异。XL-VLA 在 G1 上的平均成功率达到 **0.825**，而 π0 仅为 **0.525**，提升 **57%**。Figure 5 直观展示了这一增益：隐空间共训练使 G1 在多个任务上的成功率曲线显著上移，表明从单臂灵巧手到双臂人形机器人的形态迁移同样受益于隐式动作空间的统一。

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/022_Table_6.jpg]]
*Table 6: G1 Policy Performances*

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/008_Figure_5.jpg]]
*Figure 5: G1 Cross-Robot Performance. Co-training with latent xArm and humanoid data outperforms using raw actions*

### 隐空间质量评估与消融

隐空间本身的质量是 XL-VLA 性能的基础。**Table 4** 通过“隐空间重放”（Latent Replay）实验直接评估跨手型隐空间的一致性：将源手型上采集的遥操作轨迹编码到隐空间，再解码到目标手型，并在真实硬件上回放。如果回放过程中不发生接触断裂或自碰撞，则视为成功。在两个手型对（Ability+Inspire 和 Paxini+X-Hand）上，XL-VLA 的平均重放成功率分别为 **0.82** 和 **0.81**，显著高于监督式隐空间重定向基线 LAD（Latent Action Diffusion）的 **0.60** 和 **0.61**。值得注意的是，XL-VLA 完全通过无监督方式实现这一对齐，而 LAD 需要监督数据。

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/010_Table_4.jpg]]
*Table 4: Latent replay comparison. We compare our latent space with Latent Action Diffusion (LAD) [3]. For each hand combination, teleoperated trajectories collected on one source hand are encoded into the latent space, decoded onto the target hand, and replayed on real hardware. A replay is counted as successful if the encoded–decoded sequence can be executed without breaking contact or causing self-collisions. Higher replay success indicates better cross-embodiment consistency of the latent representation*

**Table 5** 的消融实验系统考察了架构选择与损失函数设计对隐空间质量的影响。评估维度包括重建精度、跨手型重定向误差、隐空间连续性以及插值平滑性。最终配置（架构 H_64^{128 64}，隐维度 32）在这些指标上取得综合最优。关键发现包括：
- 移除重定向损失 L₂ 会导致跨手型对齐显著退化，指尖几何一致性丧失；
- 过大的隐空间维度（如 64 维）虽然能提升重建精度，但会损害泛化能力和插值平滑性，表明适度的信息瓶颈对学习解耦且可迁移的表示至关重要；
- KL 正则化（L₃）对隐空间的连续性和可采样性贡献明显，移除后隐空间出现不连续区域，影响 VLA 策略的稳定预测。

### 失败模式与局限性

尽管 XL-VLA 在实验中表现突出，论文明确指出若干局限性：
1. **手型扩展仍需训练**：对于全新手型，仍需训练对应的编码器 E_h 和解码器 D_h，虽然无需配对数据，但无法实现完全的零样本手型迁移。
2. **隐维度未充分泛化探索**：当前 32 维隐空间是在四种特定手型上优化的，其对更多、更异质手型（如具有显著不同手指拓扑的机械手）的泛化能力尚未验证。
3. **复杂接触任务鲁棒性未知**：未研究隐空间在需要高精度接触力控制的双手协调任务中的表现，这类任务对几何对齐的精度要求远高于抓取和放置任务。

### 关键图表结论总结

- **Table 2**：XL-VLA 在四种手型、10 个任务上平均成功率 0.72 vs π0 的 0.32，相对提升 125%。
- **Figure 4**：零样本任务泛化中，XL-VLA 在所有手型-任务组合上一致超越 π0+RT 重定向基线。
- **Table 6 / Figure 5**：G1 人形机器人上 XL-VLA 成功率 0.825 vs π0 的 0.525，隐空间共训练带来 57% 的跨形态增益。
- **Table 4**：隐空间重放成功率 0.82/0.81 vs LAD 的 0.60/0.61，验证无监督对齐的优越性。
- **Table 5**：消融证实重定向损失 L₂ 和适度隐维度（32）对跨手型一致性与泛化至关重要。

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/005_Table_2.jpg]]
*Table 2: Vision-Language-Action Modeling. We compare XL-VLA with*

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/006_Figure_4.jpg]]
*Figure 4: Zero-shot Unseen Tasks Generalization. For each hand, we randomly select some tasks as unseen tasks, whose data are held out from the training dataset. Then we test the unseen tasks with model trained on other data. Results show that by training with an aligned latent action space, XL-VLA gets the ability to generalize to novel hand-task combination in a zero-shot manner. PSR stands for “Partial Success Rate”, where policy is rewarded with half success if only one arm finishes its task*

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/011_Table_5.jpg]]
*Table 5: Ablations. Ablation results comparing reconstruction accuracy, cross-embodiment retargeting, latent-space continuity, and interpolation smoothness. Exp denotes model variants: removing losses*

### 补充图表

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/002_Table_1.jpg]]
*Table 1: Related Work Summary. Summary of related work comparing data sources, deployment settings, and input/output capabilities for latent-based cross-embodiment methods. Data indicates the training modalities used in each work. Deployment specifies the robot embodiments evaluated and whether cross–end-effector transfer is supported. Input denotes which modalities (vision, language, proprioception) are used for training. Output reports whether a method includes a cross-embodiment decoder and whether it enables zero-shot transfer to unseen embodiments*

![[assets/figures/papers/paper_list_l2164_https_arxiv_org_abs_2603_10158/figures/007_Table_3.jpg]]
*Table 3: Dexterous Hand Comparison*

## 方法谱系与知识库定位

### 1. 基线方法的关系与差异化

XL‑VLA 的核心技术路线是在**视觉‑语言‑动作（VLA）框架中引入共享隐式动作空间**，以此解决多灵巧手异构动作空间下的统一建模问题。与此相对的基线方法可分为三类，各自代表了不同的跨手型策略思路。

**π0（原始关节空间 VLA）**  
π0 是 XL‑VLA 的直接构建基础（Figure 2 明确标注“builds on π0”），其原始设计直接在每种手型的独立关节位置空间中预测动作块。当面对不同手型时，π0 通过调整输入/输出的关节序列长度来适配，但不同手型的动作语义完全隔离，无法共享控制知识。在跨手型联合训练中，π0 的平均成功率仅为 0.32（Table 2），而 XL‑VLA 达到 0.72，相对提升约 125%。这一巨大差距揭示了**异构动作空间直接混合训练**的根本瓶颈：模型缺乏将“抓取”“移动”等高层操作语义与关节级命令解耦的机制。

**π0+RT（运动学重定向基线）**  
π0+RT 是一种工程化的折中方案：先在单一手型（X‑Hand）上训练 π0，再通过运动学重定向将输出的关节命令映射到其他目标手型上。其优势在于无需修改 VLA 模型本身，但重定向过程依赖于人工设计的指尖对应规则，且无法保证不同手型在运动学约束下的动作可行性。在零样本任务泛化实验中（Figure 4），XL‑VLA 在所有手型‑任务组合上一致超越 π0+RT，表明**无监督隐式对齐**在泛化到未见任务‑手型组合时具有系统性优势，而重定向方案受限于固定映射规则，难以适应新场景。

**LAD（Latent Action Diffusion，监督式隐空间重定向基线）**  
LAD 同样使用了隐空间重放的思路，但其隐空间训练依赖**监督数据**（即配对的手型‑动作对应关系）。在跨手型潜空间重放对比中（Table 4），XL‑VLA 在两个手型对上的平均成功率分别为 0.82 和 0.81，显著高于 LAD 的 0.60 和 0.61。关键差异在于：XL‑VLA 的隐空间完全通过**无监督自编码器**学习，仅利用关节重建损失、基于指尖可微正运动学的几何对齐损失和 KL 正则化，无需任何配对演示数据即可实现跨手型动作的语义一致映射。这一特性使得 XL‑VLA 在扩展到新手型时只需训练对应的编码器‑解码器对，而无需收集昂贵的配对遥操作数据。

### 2. 适用边界与关键约束

XL‑VLA 的设计假设和实验验证共同划定了其当前适用边界：

**手型覆盖范围**  
当前工作验证了四种灵巧手（Ability、Inspire、Paxini DexH13、X‑Hand1）以及 G1 人形机器人的跨手型控制。这四种手型在手指数量、自由度和运动学结构上存在显著差异（Table 3），但均属于拟人化多指手型范畴。对于运动学差异极大的非拟人手型（如吸盘、平行夹爪），隐空间的对齐能力尚未得到验证。

**隐空间维度的选择**  
消融实验表明（Table 5），最终采用的隐维度 32 在重建精度、重定向误差、连续性和插值平滑性上达到综合最优。过大的隐空间（如 64 维）反而会损害泛化性能。这一发现暗示**隐空间的紧凑性**对于跨手型泛化至关重要，但该维度是在特定四种手型组合上优化的，其最优值可能依赖于手型集合的异质性程度。

**任务复杂度**  
实验覆盖了 10 个操作任务（包括抓取、放置、推动等），以及 G1 人形机器人的 4 个任务。所有任务均为单臂操作，未涉及双手协调或高精度接触式操作。在更复杂的任务场景下，隐空间能否保持足够的表达精度和时序一致性仍需进一步验证。

**训练数据规模**  
所有方法在相同的多手型多任务数据集上训练，每任务每手型仅 50 条演示。这一数据规模相对较小，但 XL‑VLA 仍表现出显著的性能提升，说明隐式动作空间的引入有效提升了数据效率。然而，当手型数量进一步增加时，隐空间预训练所需的数据量和优化难度可能呈超线性增长。

### 3. 局限性与开放问题

**当前局限**

1. **新手型仍需训练**：虽然 XL‑VLA 无需配对数据，但对于完全未见的手型，仍需训练对应的编码器 E_h 和解码器 D_h。这意味着系统尚不具备真正的“零样本手型迁移”能力——新加入的手型必须参与隐空间预训练过程。

2. **隐维度未自适应**：隐空间维度（32）是固定的超参数，未探索其对手型集合规模的自动适应机制。当手型异质性显著增大时，固定维度可能成为信息瓶颈或冗余源。

3. **双手协调与精细操作未覆盖**：当前实验均为单臂任务，隐空间在双手协调场景下能否保持跨手型的一致性，以及在高精度接触式操作中能否保留足够的力/位信息，仍是未解问题。

**开放问题**

1. **完全零样本手型扩展**：能否设计一种机制，使得隐空间可以无缝接纳运动学差异极大的新手型，而无需任何额外训练？这可能需要引入手型结构的图神经网络编码或基于基础模型的运动学理解能力。

2. **隐维度的自适应选择**：潜在维度对跨手型泛化性能的影响阈值在哪里？能否根据手型集合的异质性自动选择最优维度？信息瓶颈理论可能为这一问题提供理论指导。

3. **无监督对齐与少量配对数据的结合**：当前方法完全依赖无监督对齐，但少量配对数据（如关键抓取姿态的跨手型对应）是否能显著提升隐空间质量？半监督隐空间学习是一个值得探索的方向。

4. **向全身人形机器人的扩展**：G1 实验初步验证了隐空间在手臂‑手型组合上的有效性，但该方法能否扩展到腿足运动、全身协调操控等更广泛的人形机器人形态？这涉及隐空间对周期性运动、接触约束和全身动力学的表达能力。

### 4. 知识库定位

XL‑VLA 在跨手型机器人学习领域占据了一个独特的位置：它是**首个将无监督跨手型隐式动作空间与完整 VLA 流水线深度整合**的工作。与此前方法相比：

- 相对于**运动学重定向方法**（如 π0+RT），XL‑VLA 将手型对齐从后处理步骤提升为模型的核心表示层，使 VLA 模型本身具备了跨手型泛化能力。
- 相对于**监督式隐空间方法**（如 LAD），XL‑VLA 完全消除了对配对数据的依赖，大幅降低了扩展到新手型的成本。
- 相对于**通用跨形态策略方法**（如基于 Transformer 的直接多形态训练），XL‑VLA 通过显式的隐空间对齐机制，在数据效率上具有明显优势——仅需每任务每手型 50 条演示即可实现 0.72 的平均成功率。

该方法的核心贡献在于证明了**通过无监督几何对齐（指尖距离与方向约束）可以在完全不同的关节空间中诱导出语义一致的隐式表示**，这一洞察对于更广泛的跨形态机器人学习具有启发意义。其技术路线——冻结的隐空间编码器/解码器 + 在隐空间中微调的 VLA 主干——也为后续工作提供了一个清晰的模块化范式。

## 原文 PDF

![[paperPDFs/CVPR_2026/Cross_Hand_Latent_Representation_for_Vision_Language_Action_Models.pdf]]

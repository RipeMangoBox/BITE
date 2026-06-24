---
title: "Move as You Say, Interact as You Can: Language-guided Human Motion Generation with Scene Affordance"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generation_with_Scene_Affordance.pdf
aliases:
- TSADFAA
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入场景可供性图（affordance map）作为中间表示，并构建两阶段扩散模型框架（ADM + AMDM），首先预测语言引导的可供性图，再将其与语言描述一起用于运动生成。
primary_logic: 基于人体骨骼关节与场景表面点之间距离场构建的可供性图，能够精确提供语言描述的空间定位和场景几何信息，从而降低多模态条件联合建模的难度，并在有限训练数据下有效提升模型的语义一致性和跨场景泛化能力。
claims:
- 所提出的两阶段模型在HumanML3D和HUMANISE两个标准基准上均显著优于所有基线方法。
- 引入可供性图作为中间表示，显著改善了语言描述的空间定位准确性和生成运动的物理合理性。
- 在仅包含有限语言-场景-运动配对数据的训练条件下，模型对新场景和未见描述的泛化能力突出。
- Perceiver结构在可供性图生成中由于能有效融合点云和语言特征而优于MLP和Point Transformer。
---

# Move as You Say, Interact as You Can: Language-guided Human Motion Generation with Scene Affordance

> [!tip] 核心洞察
> 基于人体骨骼关节与场景表面点之间距离场构建的可供性图，能够精确提供语言描述的空间定位和场景几何信息，从而降低多模态条件联合建模的难度，并在有限训练数据下有效提升模型的语义一致性和跨场景泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 即说即动，随境交互：基于场景可供性的语言引导人体运动生成 |
| 英文题名 | Move as You Say, Interact as You Can: Language-guided Human Motion Generation with Scene Affordance |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://afford-motion.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Two-stage Affordance Diffusion Framework (ADM + AMDM) |
| Dataset | HumanML3D, HUMANISE, Novel Evaluation Set |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.352 vs 0.544 (MDM) (降低0.192)。
> - HUMANISE 上，goal dist. 0.156 vs 0.326 (one-stage @ Enc) (降低0.170)；contact (%) 96.04 vs 76.11 (one-stage @ Enc) (+19.93)。
> - Novel Evaluation Set 上，FID 7.887 vs 14.698 (one-stage) (降低6.811)。

## 概述

**核心问题**：在语言、3D 场景与人体运动三个模态之间进行联合建模，要求生成的运动既准确贴合语言语义，又在物理上合理地定位于场景几何中。然而，大规模语言-场景-运动配对数据极度稀缺，直接端到端学习极易导致语义漂移、空间定位失败与物理穿透。

**核心方法**：本文提出**两阶段可供性扩散框架（ADM + AMDM）**，将**场景可供性图（affordance map）**作为中间表示。第一阶段 **Affordance Diffusion Model（ADM）** 以场景点云和语言描述为条件，利用 Perceiver 架构预测可供性图；第二阶段 **Affordance-to-Motion Diffusion Model（AMDM）** 以预测的可供性图、场景点云和语言描述为条件，通过 Point Transformer 编码器与 Transformer 主干生成人体运动序列。可供性图本质上是人体骨骼关节到场景表面点的广义距离场，经时间维度最大池化得到，能够精确传递语言描述的空间定位信息与场景几何约束。

**方法定位**：该方法属于**两阶段扩散生成**范式，通过显式中间表示解耦多模态条件建模。相较于直接融合场景点云的单阶段扩散基线（如 MDM 的场景扩展变体），以及 cVAE（Wang et al., NeurIPS 2022）等语言条件的人-场景交互方法，本框架将空间定位与运动生成分而治之，显著降低联合建模难度。

**主要结果**：
- 在 **HumanML3D** 基准上，FID 达到 0.352，较 MDM（0.544）降低 0.192（Table 1）。
- 在 **HUMANISE** 基准上，目标距离（goal dist.）降至 0.156，接触分数（contact）达到 96.04%，相比单阶段基线分别改善 0.170 和 +19.93 个百分点（Table 2）。
- 在**新场景泛化评估集**上，FID 为 7.887，远优于单阶段模型的 14.698，验证了可供性图中间表示对跨场景泛化的关键作用（Table 4）。

**局限性**：面对完全陌生的人-场景交互类别或过于复杂的语言描述时仍会失败（Figure 5）；两阶段扩散推理速度较慢，难以满足实时需求；泛化能力仍受限于训练数据的场景与动作分布覆盖范围。

## 背景与动机

**核心瓶颈** 语言引导的3D场景人体运动生成任务，本质上是语言、3D场景几何和人体运动三个模态的联合建模问题。现有方法面临的根本性瓶颈在于：缺乏大规模、高质量的语言-场景-运动配对数据，加之三模态联合建模的内在复杂性，导致生成的运动难以同时满足语义描述的准确性、3D场景中的物理合理性以及精确的空间定位要求。

**现有方法的缺口** 当前主流方法可分为两类：一是纯文本到运动生成（text-to-motion）方法，如 **T2M**（Guo et al., CVPR 2022）和 **MDM**（Tevet et al., CVPR 2023），它们完全不考虑3D场景约束，生成的运动无法与具体场景交互；二是语言条件的人-场景交互生成方法，如基于cVAE的方案（Wang et al., NeurIPS 2022），这些方法尝试直接将场景点云特征与运动生成器融合，但由于三模态联合映射的高度非线性，在有限数据下难以学到稳健的语义-空间对应关系。

**本文动机与核心思路** 针对上述瓶颈，本文提出将**场景可供性图（affordance map）**作为中间表示，将困难的三模态联合建模分解为两个更可控的子问题。场景可供性图定义为人体骨骼关节与3D场景表面点之间基于距离场的广义可供性表示——离关节越近的场景点权重越高，从而精确编码了语言描述所隐含的空间定位信息（如“坐在椅子上”意味着骨盆关节应靠近椅子表面）。通过先预测语言引导的可供性图，再将其作为条件输入运动生成模型，该方法在有限训练数据下有效提升了语义一致性和跨场景泛化能力。

## 核心创新

### 1. 核心瓶颈与因果调控

该工作瞄准的核心瓶颈在于：**语言描述、3D场景几何与人体运动三种异构模态的联合建模高度复杂**，且大规模、高质量的语言-场景-运动配对数据严重匮乏。现有方法（如直接将场景点云特征注入运动生成器的单阶段模型）难以同时满足语义对齐、空间定位准确和物理合理性三重要求，尤其在跨场景泛化时表现脆弱。

针对这一瓶颈，论文引入的因果调控旋钮是**场景可供性图（affordance map）作为中间表示**，并据此构建了**两阶段扩散模型框架**。其核心调控逻辑为：将多模态条件联合建模的难题分解为“语言→可供性图”和“可供性图+语言→运动”两个子问题，通过可供性图这一显式空间表示来承载语言描述中的空间定位语义与场景几何信息，从而降低第二阶段运动生成的条件复杂度。

### 2. 核心洞察

本文的关键洞察可概括为：

> **基于人体骨骼关节与场景表面点之间距离场构建的可供性图，能够精确编码语言描述所隐含的空间定位信息与场景几何约束，从而在有限训练数据条件下有效提升模型的语义一致性和跨场景泛化能力。**

具体而言，可供性图通过以下机制发挥作用：
- **空间定位的显式化**：将“走到桌子旁坐下”这类语言描述中的空间目标，转化为特定关节（如骨盆、脚部）与场景表面点之间的归一化距离场，使生成模型无需隐式学习语言-空间映射。
- **场景几何的结构化编码**：可供性图以逐点权重形式保留了场景表面几何信息，为运动生成器提供了关于可交互区域（如可坐平面、可行走地面）的强先验。
- **模态解耦与数据效率**：将三模态联合建模拆分为两个条件更简单的子任务，使得每个子任务可以在相对有限的数据下有效训练，缓解了配对数据稀缺带来的过拟合风险。

### 3. 相对基线的关键创新（Changed Slots）

与现有基线方法相比，本工作在以下三个维度上做出了实质性改变：

#### 3.1 中间表示：从“无中间表示”到“基于距离场的可供性图”

| 维度 | 基线方案 | 本工作方案 |
|------|----------|------------|
| **中间表示** | 无中间表示，直接学习场景+语言到运动的端到端映射 | 基于距离场的场景可供性图作为显式中间表示 |

基线方法（如 **cVAE**（Wang et al., NeurIPS 2022）及本文实现的单阶段扩散模型变体）将场景点云特征与语言特征直接融合后输入运动解码器。这种设计迫使模型在单一阶段内隐式学习语言-空间对应关系，在数据有限时容易产生空间定位错误和物理不合理的结果。

本工作将可供性图定义为：

$$ \mathbf{c}(n,j) = \exp\left(-\frac{1}{2}\frac{\mathbf{d}(n,j)}{\sigma^2}\right) $$

其中 $\mathbf{d}(n,j)$ 为场景表面点 $n$ 到人体关节 $j$ 的距离。通过对时间维度进行最大池化得到最终可供性图：

$$ \mathbf{C} = \mathtt{max-pool}(\mathbf{c}_1, \mathbf{c}_2, \ldots, \mathbf{c}_F) $$

这一显式中间表示将语言中的空间语义（如“坐在椅子上”）转化为可监督的空间定位信号，显著降低了后续运动生成的难度。

#### 3.2 场景条件策略：从“直接融合”到“两阶段级联生成”

| 维度 | 基线方案 | 本工作方案 |
|------|----------|------------|
| **场景条件策略** | 直接将场景点云特征与运动生成器融合 | 第一阶段ADM预测语言引导的可供性图，第二阶段AMDM以可供性图为条件生成运动 |

本工作的两阶段框架（**Figure 2**）由以下模块组成：
- **Affordance Diffusion Model (ADM)**：以3D场景点云 $\mathcal{S}$ 和语言描述 $\mathcal{L}$ 为条件，通过扩散过程生成可供性图 $\mathbf{C}$：

$$ p_{\theta}(\mathbf{C}_{0:T} \mid \mathcal{S}, \mathcal{L}) = p(\mathbf{C}_T) \prod_{t=1}^{T} p_{\theta}(\mathbf{C}_{t-1} \mid \mathbf{C}_t, \mathcal{S}, \mathcal{L}) $$

- **Affordance-to-Motion Diffusion Model (AMDM)**：以生成的可供性图 $\mathbf{C}$、场景 $\mathcal{S}$ 和语言 $\mathcal{L}$ 为条件，生成人体运动序列 $\mathbf{X}$：

$$ p_{\phi}(\mathbf{X}_{0:T} \mid \mathbf{C}, \mathcal{S}, \mathcal{L}) = p(\mathbf{X}_T) \prod_{t=1}^{T} p_{\phi}(\mathbf{X}_{t-1} \mid \mathbf{X}_t, \mathbf{C}, \mathcal{S}, \mathcal{L}) $$

这一级联设计的优势在于：ADM专注于空间定位任务，AMDM专注于运动质量和物理合理性，两个子任务各司其职，有效降低了单个模型的负担。

#### 3.3 多模态融合架构：从“单阶段统一融合”到“两阶段分工架构”

| 维度 | 基线方案 | 本工作方案 |
|------|----------|------------|
| **多模态融合架构** | 单阶段自注意力或交叉注意力直接融合三种模态 | ADM采用Perceiver架构预测可供性图；AMDM采用Point Transformer + Transformer backbone融合可供性、语言与运动特征 |

在ADM中，**Perceiver架构**通过Encode/Process/Decode块利用交叉注意力高效融合点云和语言特征，在可供性图生成任务中显著优于MLP和Point Transformer变体（**Table 3**：Perceiver min dist. 0.756 vs MLP 0.904）。

在AMDM中，**Affordance Encoder**（基于Point Transformer）从可供性图中提取多尺度特征，随后**Transformer Backbone**通过自注意力和交叉注意力融合语言特征、可供性特征和带噪运动序列，最终生成符合语义且物理合理的运动。

### 4. 创新点的证据强度

上述创新点的有效性在实验中得到了充分验证：

- **两阶段 vs 单阶段**：在HUMANISE数据集上，本方法在目标距离（goal dist. 0.156 vs 单阶段 0.326）和接触分数（contact 96.04% vs 单阶段 76.11%）上均大幅领先（**Table 2**），直接证明了可供性图中间表示的必要性。
- **跨场景泛化**：在新评估集上，本方法的FID为7.887，远优于单阶段模型的14.698（**Table 4**），验证了两阶段设计在有限训练数据下的泛化优势。
- **架构选择的合理性**：Perceiver在可供性图生成中的优越表现（**Table 3**）和AMDM架构消融实验（**Table 5**）共同支撑了多模态融合架构设计的有效性。

### 5. 局限与待解决问题

尽管创新点明确且验证充分，该方法仍存在以下局限：

- **推理效率**：两阶段扩散模型导致推理速度较慢，难以满足实时应用需求。
- **未知交互的泛化**：模型在面对完全陌生的人-场景交互类别或过于复杂的语言描述时容易失败（**Figure 5**）。
- **数据依赖性**：虽然可供性图有助于缓解数据稀缺问题，但模型的泛化能力仍受限于训练覆盖的场景/动作分布。

待解决的开放问题包括：如何实现完全未见过的人-场景交互类别的零样本生成（zero-shot HSI），如何通过更高效的生成架构（如一致性模型、潜在扩散）缩短推理时间，以及如何利用少量标注数据在更多样的真实3D场景中进行半监督或自监督训练。

## 整体框架

本文提出一个**两阶段扩散框架**，核心思路是将**场景可供性图（affordance map）**作为语言、3D场景与人体运动三者之间的中间表示，以降低多模态联合建模的难度。整体流程如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. To generate language-guided human motions in 3D scenes, our framework first predicts the scene affordance map in accordance with the language description using Affordance Diffusion Model (ADM). Next, it generates interactive human motions with Affordance-to-Motion Diffusion Model (AMDM) conditioned on the predicted affordance map*

### 第一阶段：可供性扩散模型（ADM）

**Affordance Diffusion Model（ADM）**负责从3D场景点云和语言描述中预测语言引导的可供性图。其输入为场景点云 $\mathcal{S}$ 和语言描述 $\mathcal{L}$，输出为可供性图 $\mathbf{C}$。ADM 采用 **Perceiver 架构** 作为骨干网络，通过 Encode/Process/Decode 三个模块利用交叉注意力高效融合点云特征与语言特征，并在扩散过程中以场景和语言为条件逐步去噪生成可供性图。训练时，ADM 使用均方误差损失直接预测原始信号而非噪声：

$$L_{\mathrm{MSE}} = \mathbb{E}_{\mathbf{C}_0, t}\left[\|\mathbf{C}_0 - G_{\theta}(\mathbf{C}_t, t, \mathcal{S}, \mathcal{L})\|_2^2\right]$$

其中可供性图 $\mathbf{C}$ 由各帧距离场经时间维度的最大池化得到：

$$\mathbf{C} = \mathtt{max-pool}(\mathbf{c}_1, \mathbf{c}_2, \ldots, \mathbf{c}_F)$$

而每帧的距离权重通过归一化距离场计算，离关节越近的场景表面点权重越高：

$$\mathbf{c}(n,j) = \exp\left(-\frac{1}{2}\frac{\mathbf{d}(n,j)}{\sigma^2}\right)$$

### 第二阶段：可供性到运动扩散模型（AMDM）

**Affordance-to-Motion Diffusion Model（AMDM）**以第一阶段预测的可供性图 $\mathbf{C}$、场景点云 $\mathcal{S}$ 和语言描述 $\mathcal{L}$ 为条件，生成人体运动序列 $\mathbf{X}$。AMDM 内部包含两个关键模块：

- **可供性编码器（Affordance Encoder）**：采用 **Point Transformer** 从可供性图中提取多尺度空间特征。
- **Transformer 骨干网络**：通过自注意力和交叉注意力机制融合语言特征、可供性特征与带噪运动序列，实现多模态条件建模。

AMDM 的训练同样采用信号预测范式的均方误差损失：

$$L_{\mathrm{MSE}} = \mathbb{E}_{\mathbf{X}_0, t}\left[\|\mathbf{X}_0 - G_{\phi}(\mathbf{X}_t, t, \mathbf{C}, \mathcal{S}, \mathcal{L})\|_2^2\right]$$

### 设计动机与模块关系

该两阶段设计的核心洞察在于：**直接学习“语言+场景→运动”的端到端映射面临严重的多模态对齐困难**，尤其在语言-场景-运动配对数据稀缺的条件下。引入可供性图作为中间表示，将问题分解为两个相对独立的子任务——先预测“在哪里交互”（可供性图），再生成“如何运动”（运动序列）——显著降低了联合建模的复杂度。可供性图基于人体骨骼关节与场景表面点之间的距离场构建，能够精确编码语言描述所隐含的空间定位信息（如“坐在椅子上”时臀部与椅面的接触区域），同时提供场景几何约束，从而在有限训练数据下有效提升语义一致性和跨场景泛化能力。

## 核心模块与公式推导

### 可供性图的定义与构建

本方法的核心创新在于将**场景可供性图（affordance map）** 作为语言、3D场景与人体运动之间的中间表示。该可供性图被重新定义为人体骨骼关节与3D场景表面点之间的**广义距离场**，其构建过程分为两步：

**第一步：逐帧归一化距离权重。** 对于第$n$个场景表面点与第$j$个人体关节，其距离$\mathbf{d}(n,j)$通过高斯核转换为归一化权重：

$$\mathbf{c}(n,j) = \exp\left(-\frac{1}{2}\frac{\mathbf{d}(n,j)}{\sigma^2}\right)$$

其中$\sigma$控制距离衰减的敏感度。该公式使得离关节越近的场景点获得越高的权重值，从而为训练提供稳定的梯度信号。

**第二步：时序最大池化聚合。** 将运动序列所有$F$帧的逐帧距离场沿时间维度进行最大池化，得到单一的可供性图：

$$\mathbf{C} = \mathtt{max-pool}(\mathbf{c}_1, \mathbf{c}_2, \ldots, \mathbf{c}_F)$$

该操作保留了整个运动过程中每个场景点与人体骨骼的最小距离信息，从而在紧凑的中间表示中编码了人-场景交互的空间定位关系。

---

### 第一阶段：可供性扩散模型（ADM）

ADM负责以3D场景点云$\mathcal{S}$和语言描述$\mathcal{L}$为条件，生成语言引导的可供性图。其扩散过程定义为：

$$p_{\theta}(\mathbf{C}_{0:T} \mid \mathcal{S}, \mathcal{L}) = p(\mathbf{C}_T) \prod_{t=1}^{T} p_{\theta}(\mathbf{C}_{t-1} \mid \mathbf{C}_t, \mathcal{S}, \mathcal{L})$$

其中$\mathbf{C}_T \sim \mathcal{N}(0, \mathbf{I})$为标准高斯噪声，$T$为扩散步数。ADM的训练采用**信号预测范式**（即直接预测原始信号$\mathbf{C}_0$而非噪声），损失函数为均方误差：

$$L_{\mathrm{MSE}} = \mathbb{E}_{\mathbf{C}_0, t}\left[\|\mathbf{C}_0 - G_{\theta}(\mathbf{C}_t, t, \mathcal{S}, \mathcal{L})\|_2^2\right]$$

ADM的骨干网络采用**Perceiver架构**，其核心机制是通过Encode-Process-Decode块中的交叉注意力高效融合场景点云特征与语言特征。消融实验表明（Table 3），Perceiver在可供性图生成的落地点距离指标上（min dist. 0.756）显著优于MLP（0.904）和Point Transformer变体，验证了该架构在多模态条件融合中的有效性。

---

### 第二阶段：可供性到运动扩散模型（AMDM）

AMDM以第一阶段生成的可供性图$\mathbf{C}$、场景点云$\mathcal{S}$和语言描述$\mathcal{L}$为联合条件，生成人体运动序列$\mathbf{X}_{0:T}$。其扩散过程为：

$$p_{\phi}(\mathbf{X}_{0:T} \mid \mathbf{C}, \mathcal{S}, \mathcal{L}) = p(\mathbf{X}_T) \prod_{t=1}^{T} p_{\phi}(\mathbf{X}_{t-1} \mid \mathbf{X}_t, \mathbf{C}, \mathcal{S}, \mathcal{L})$$

AMDM同样采用信号预测范式的MSE损失进行训练：

$$L_{\mathrm{MSE}} = \mathbb{E}_{\mathbf{X}_0, t}\left[\|\mathbf{X}_0 - G_{\phi}(\mathbf{X}_t, t, \mathbf{C}, \mathcal{S}, \mathcal{L})\|_2^2\right]$$

AMDM的架构由两个关键模块组成：
- **可供性编码器（Point Transformer）**：从可供性图中提取多尺度空间特征，为后续Transformer主干提供场景交互的结构化信息。
- **Transformer主干**：通过自注意力与交叉注意力机制融合语言特征、可供性特征和带噪运动序列，实现多模态条件下的运动生成。

---

### 两阶段设计的因果逻辑

该两阶段框架的核心因果机制在于**解耦多模态联合建模的复杂性**：ADM先将语言描述的空间定位意图转化为可供性图这一显式几何表示，AMDM再基于该表示生成物理合理的运动。这种设计使得模型在有限的训练数据下（仅含少量语言-场景-运动配对）仍能有效学习语义一致性映射，并通过可供性图作为信息瓶颈来提升跨场景的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/012_Figure.jpg]]
*Figure: A1. Illustration of the decoder and encoder variants’ architectures. The left part depicts the architecture of the decoder variant, which stacks self-attention and cross-attention layers alternately to fuse multi-modal conditions effectively. The right part showcases the design of the encoder variant, employing self-attention layers to fuse the language features, affordance features, and noisy motion sequences*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/013_Figure.jpg]]
*Figure: (b) Point Transformer variant Figure A2. Illustration of MLP and Point Transformer variants of ADM*

## 实验与分析

### 核心实验设置

为系统评估所提方法的有效性，作者在两个标准基准上进行了实验：**HumanML3D**（Guo et al., CVPR 2022）用于评估文本到运动生成的质量，以及 **HUMANISE**（Wang et al., NeurIPS 2022）用于评估语言引导的人-场景交互运动生成。此外，作者还构建了一个**新颖评估集**，包含16个来自ScanNet、PROX、Replica和Matterport3D等不同来源的场景，以及80条由人工标注的HSI描述，用于测试模型的跨场景泛化能力。训练数据整合了HumanML3D、HUMANISE和PROX三个数据集，以建立语言、3D场景和运动之间的配对关系。

为保证评估公平性，所有指标计算均在一致的特征空间下进行——作者按照Guo等人的方法重新训练了运动和文本特征提取器，并对所有评估重复5次并报告95%置信区间。

---

### HumanML3D 上的文本到运动生成

Table 1展示了在HumanML3D上的定量结果。本文模型（采用Perceiver作为ADM、编码器变体作为AMDM）在**FID**指标上达到**0.352**，显著优于最强基线MDM（Tevet et al., CVPR 2023）的0.544，降幅达0.192。在R-Precision和Multimodal Dist等语义匹配指标上，模型同样表现优异，表明引入可供性图并未损害文本-运动语义对齐能力，反而通过空间信息的显式建模增强了生成质量。

值得注意的是，部分指标（如Diversity）上本文模型与Real分布存在一定差距，但整体趋势表明两阶段框架在保持运动多样性的同时，大幅提升了生成逼真度。

---

### HUMANISE 上的语言引导场景交互运动生成

Table 2报告了HUMANISE数据集上的核心结果。本文模型在**目标距离（goal dist.）**上达到**0.156**，较单阶段扩散模型（编码器变体）的0.326降低0.170；在**接触分数（contact %）**上达到**96.04%**，较单阶段模型的76.11%提升近20个百分点。这直接验证了可供性图作为中间表示在空间定位和物理合理性方面的关键作用。

与cVAE（Wang et al., NeurIPS 2022）等专门设计的HSI生成方法相比，本文模型在所有指标上均取得最优，证明了通用两阶段扩散框架在该任务上的优势。Figure 3的定性对比进一步显示，基线方法常出现定位失败（人物远离目标物体）和身体穿透场景的问题，而本文方法生成的交互运动在空间准确性和物理合理性上均有明显改善。

---

### 可供性图生成质量评估

Table 3专门评估了ADM生成的可供性图质量，采用三种距离指标衡量落地精度。**Perceiver架构**取得最小距离**0.756**，与真值可供性图的0.736最为接近，而MLP变体为0.904，Point Transformer变体表现居中。这验证了Perceiver通过交叉注意力高效融合点云和语言特征的设计优势。

---

### 泛化能力评估

Table 4报告了在新颖评估集上的泛化性能。本文模型取得**FID 7.887**，远优于单阶段模型的14.698（降幅6.811），且在R-Precision Top-1上达到0.253（单阶段为0.180）。Figure 4的定性对比展示了典型场景：单阶段模型生成的运动会忽略场景约束（如人物远离水槽洗手），而本文模型能准确定位并生成自然交互。这证实了可供性图有效降低了多模态条件联合建模的难度，使模型在有限训练数据下仍具备较强的跨场景泛化能力。

---

### 关键消融实验

**ADM架构选择**：Table 3已证实Perceiver在可供性图生成中优于MLP和Point Transformer。Table 5进一步表明，在AMDM中使用Perceiver架构在目标距离和接触分数上略优于Point Transformer。

**真值/预测可供性比例**：Table A1展示了在HumanML3D上训练时替换不同比例真值可供性图的影响。**50%替换比例取得最佳FID（0.352）**，优于全真值训练（0.248）和全预测训练（0.537）。这表明混合训练策略能有效缓解ADM预测误差在AMDM中的累积效应，同时保持对真实分布的良好拟合。然而，在新颖评估集上（Table A2），50%预测训练的接触分数仅为30.54%，远低于全真值训练的71.98%，提示在强泛化场景下仍需更精确的可供性图预测。

---

### 失败模式与局限性

Figure 5展示了典型失败案例。当面对**完全陌生的人-场景交互类别**（如训练中未见过的动作-物体组合）或**过于复杂的语言描述**（如“一个人从一张床起身并躺在另一张床上”这类多阶段指令）时，模型生成的运动可能出现定位偏差或动作语义不完整。此外，两阶段扩散模型的推理速度较慢，难以满足实时应用需求，且模型泛化能力仍受限于训练数据覆盖的场景和动作分布。

### 补充图表

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/003_Table_1.jpg]]
*Table 1: Quantitative results of generation on HumanML3D. “Real” denotes the results computed with GT motions. “Ñ” indicates metrics that are better when closer to “Real” distribution. Our model uses Perceiver in ADM and encoder-based architecture in AMDM*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/004_Table_2.jpg]]
*Table 2: Quantitative results of human motion generation on HUMANISE dataset. Bold indicates the best result*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/006_Table_3.jpg]]
*Table 3: Quantitative results of affordance map generation. We report the three distance metrics to evaluate the grounding accuracy*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/007_Table_4.jpg]]
*Table 4: Qualitative results on our novel evaluation set. “Real” indicates that we compute these metrics as a reference using the languagemotion pairs within the test set of HumanML3D. Of note, our novel evaluation set does not contain ground truth motions*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/011_Table_5.jpg]]
*Table 5: Ablation of the architectures of AMDM. The Perceiver architecture slightly outperforms the Point Transformer in the metrics of goal dist. and contact score*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results on HUMANISE dataset. The bottom-right figure provides a top-down view. Zoom in for better visualization*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative comparisons on generalization evaluation set. The first row is generated by the one-stage diffusion model and the second row is generated by our model. Our method can generate natural and accurately grounded human motions in unseen 3D scenes*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/010_Figure_5.jpg]]
*Figure 5: Failure cases. Our model fails while facing entirely unfamiliar HSIs or too complex descriptions*

![[assets/figures/papers/paper_list_l1722_Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generat/figures/015_Table.jpg]]
*Table: A2. Ablation of the proportion about replacing ground truth affordance with predicted ones on our novel evaluation set. The proportion ranges from 0.0 to 0.5. We use the Perceiver in the first stage and the encoder-based variant in the second stage*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

本工作处于**语言引导的3D场景人体运动生成**这一交叉领域，其技术谱系可追溯至两条主线：文本到运动生成（text-to-motion）与场景感知的人体运动合成。

**文本到运动生成基线。** 早期的 **Language2Pose**（Ahuja et al., 3DV 2019）建立了从语言到人体姿态的映射，但局限于单帧姿态且不考虑场景约束。**T2M**（Guo et al., CVPR 2022）和 **MDM**（Tevet et al., CVPR 2023）将这一范式推进到序列运动生成，其中MDM首次将扩散模型引入该任务，在HumanML3D上取得了FID 0.544的当时最佳结果。然而，这些方法均**忽略了3D场景信息**，无法保证生成运动在物理空间中的合理性和准确定位。本文在HumanML3D基准上与MDM直接对比，FID从0.544降至0.352（Table 1），证明即使在不涉及场景的纯运动质量指标上，两阶段框架也因可供性图带来的结构化条件而显著受益。

**场景感知的交互生成基线。** **cVAE**（Wang et al., NeurIPS 2022）是语言条件的人-场景交互生成的早期尝试，但其变分自编码器框架难以同时保持语义一致性和物理合理性。本文自行实现的**单阶段扩散模型变体**（one-stage diffusion model）则代表了直接融合三种模态的端到端方案——该变体将场景点云特征直接注入扩散去噪网络，跳过了可供性图生成。在HUMANISE数据集上，单阶段编码器变体的goal distance为0.326，接触分数仅76.11%；而本文方法将这两个指标分别提升至0.156和96.04%（Table 2），揭示了**中间表示在降低多模态联合建模难度上的关键作用**。

**方法定位的关键差异。** 与上述基线相比，本文的核心创新不在于提出全新的生成范式或网络模块，而在于**在场景与运动之间插入可供性图这一中间层**，将原本的三模态直接耦合问题分解为两个条件更清晰的子问题：场景+语言→可供性图，以及可供性图+语言→运动。这一设计使得模型能够在有限训练数据下更有效地学习语义到空间的映射，从而在跨场景泛化（Table 4, FID 7.887 vs 14.698）和定位精度上获得显著增益。

### 2. 适用边界与泛化能力

**训练数据覆盖范围。** 模型的训练集由HumanML3D、HUMANISE和PROX三个数据集拼接而成，覆盖了室内场景中的常见人-物交互（坐椅子、躺床、靠近桌子等）。在此分布内，模型表现出稳定的生成质量和定位精度。然而，这种覆盖是有限的——训练数据中的场景几何、物体类别和动作语义的组合空间远小于真实世界的多样性。

**泛化能力与失效模式。** 在新评估集（16个来自ScanNet、PROX、Replica和Matterport3D的未见场景，80条人工标注描述）上，本文方法在FID（7.887）和R-Precision Top-1（0.253）上均显著优于单阶段基线（14.698和0.180），表明可供性图作为中间表示**有效提升了模型对未见场景几何的适应能力**。但这一泛化并非无边界：当面临**完全陌生的人-场景交互类别**（如训练中未出现的动作-物体组合）或**过于复杂的语言描述**（如“一个人从一张床上起身，然后躺到另一张床上”）时，模型容易产生定位错误或动作语义丢失（Figure 5）。这说明可供性图虽然降低了空间定位的学习难度，但并未从根本上解决组合泛化的挑战——模型仍然依赖训练分布中相似样本的存在。

**推理效率的约束。** 两阶段扩散模型的设计导致推理需要依次运行ADM和AMDM两个扩散过程，耗时显著高于单阶段方法。这限制了模型在实时交互场景（如VR/AR应用、游戏引擎中的动态角色控制）中的直接部署，需要进一步借助蒸馏、一致性模型或潜在扩散等技术进行加速。

### 3. 局限与开放问题

**已知局限。**
1. **陌生交互的失效：** 面对训练分布外的动作-物体组合，可供性图的预测质量下降，进而导致下游运动生成偏离语义（Figure 5）。
2. **复杂描述的分解困难：** 包含多个子任务或长时序依赖的语言描述（如连续切换多个交互目标）难以被单一可供性图有效表征，模型缺乏显式的运动规划或任务分解机制。
3. **推理速度：** 两阶段扩散过程无法满足实时需求，这是扩散模型在该领域的共性瓶颈。
4. **数据规模限制：** 尽管可供性图缓解了数据稀缺的影响，但真实的语言-场景-运动三元组数据仍然有限，模型对场景几何和物理约束的隐式学习受限于训练数据的多样性。

**开放问题。**
1. **零样本人-场景交互（Zero-shot HSI）：** 如何使模型在完全未见过的动作-物体组合上仍然生成合理的运动？这可能需要引入外部知识（如物体功能先验、物理仿真约束）或更强的组合泛化机制。
2. **高效生成架构：** 能否用一致性模型、流匹配或潜在扩散替代当前的DDPM范式，在保持生成质量的同时将推理速度提升至实时？
3. **弱监督与自监督训练：** 如何利用大量无标注的3D场景数据和少量语言-运动配对数据进行半监督训练，以扩展模型对真实场景多样性的覆盖？
4. **复杂语义的运动规划：** 对于包含时序逻辑和多个子目标的语言描述，如何将高层语义自动分解为可供性图序列或运动基元序列，实现从“单步映射”到“规划式生成”的跨越？

## 原文 PDF

![[paperPDFs/CVPR_2024/Move_as_You_Say_Interact_as_You_Can_Language_guided_Human_Motion_Generation_with_Scene_Affordance.pdf]]
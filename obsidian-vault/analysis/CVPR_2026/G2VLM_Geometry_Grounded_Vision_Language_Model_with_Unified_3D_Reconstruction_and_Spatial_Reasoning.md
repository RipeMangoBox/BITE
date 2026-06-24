---
title: "G$^2$VLM: Geometry Grounded Vision Language Model with Unified 3D Reconstruction and Spatial Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/G_2_VLM_Geometry_Grounded_Vision_Language_Model_with_Unified_3D_Reconstruction_and_Spatial_Reasoning.pdf
project_link: null
code_link: "https://huggingface.co/remyxai/SpaceQwen2.5-VL-3B-Instruct"
aliases:
- G2
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入几何感知专家（Geometric Perception Expert），并与语义感知专家通过共享自注意力进行交互，使模型能够显式预测3D属性（深度、点云、相机姿态），并将这些几何特征用于空间推理。
primary_logic: 模仿人类认知的“双流假说”，通过双专家混合架构，将3D视觉几何学习与多模态语义理解统一在一个模型中，利用共享自注意力促进两个任务相互增强。
claims:
- G^2VLM在Sintel数据集上的单目深度估计绝对相对误差从VGGT的0.335降至0.297。
- G^2VLM-SR在SPAR-Bench上超越GPT-4o达18.5分，并在所有空间推理基准上取得最佳或可比结果。
- 消融实验表明双编码器设计（DINO用于几何，CLIP用于语义）比单编码器在两项任务上均有显著提升。
- 全局注意力机制在几何感知专家训练中显著优于帧注意力和混合注意力。
---

# G$^2$VLM: Geometry Grounded Vision Language Model with Unified 3D Reconstruction and Spatial Reasoning

> [!tip] 核心洞察
> 模仿人类认知的“双流假说”，通过双专家混合架构，将3D视觉几何学习与多模态语义理解统一在一个模型中，利用共享自注意力促进两个任务相互增强。

| 字段 | 内容 |
|------|------|
| 中文题名 | G²VLM: 几何基底的视觉语言模型，统一三维重建与空间推理 |
| 英文题名 | G$^2$VLM: Geometry Grounded Vision Language Model with Unified 3D Reconstruction and Spatial Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21688) · [HuggingFace](https://huggingface.co/remyxai/SpaceQwen2.5-VL-3B-Instruct) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | G^2VLM |
| Dataset | Sintel, Co3Dv2, 7Scenes, SPAR-Bench |

> [!tip] 效果简介
> - Sintel (Monocular Depth) 上，Abs Rel ↓ 0.297 (G^2VLM) vs 0.335 (VGGT) (-0.038)。
> - Co3Dv2 (Camera Pose) 上，AUC@30 ↑ 74.81 (G^2VLM) vs 88.59 (VGGT) (-13.78)。
> - 7Scenes (Point Map) 上，Completion ↓ 0.029 (G^2VLM) vs 0.026 (VGGT) (+0.003)。

## 概述

**问题瓶颈**：当前视觉语言模型（VLMs）仅依赖非结构化的2D图像-文本数据进行训练，缺乏从2D图像显式重建3D空间的视觉几何学习过程，导致空间理解与推理能力存在根本性不足。

**核心思想**：本文提出 **G²VLM**（Geometry Grounded Vision-Language Model），受人类认知的“双流假说”（two-streams hypothesis）启发，设计了一种双专家混合架构（Mixture-of-Transformer-Experts, MoT）：几何感知专家（“where pathway”）负责从2D图像中显式学习3D几何属性（深度、点云、相机姿态），语义感知专家（“what pathway”）负责多模态理解与空间推理；两者通过**共享自注意力**机制进行交互，使几何学习与语义理解相互增强。

**方法定位**：G²VLM 并非单纯在现有VLM上嫁接3D输出头，而是从架构层面将3D视觉几何学习内化为模型的一等公民能力。其关键设计包括：双视觉编码器（DINOv2提取低层几何特征，Qwen2 Vision Encoder提取语义特征）、几何专家采用全局注意力机制、以及额外的几何头（局部点云头、全局点云头、相机姿态头）将隐藏状态解码为显式3D表示。

**主要结果**：
- **视觉几何**：在Sintel数据集上，单目深度估计的绝对相对误差从VGGT的0.335降至**0.297**（Table 1a）。
- **空间推理**：G²VLM-SR在SPAR-Bench上超越GPT-4o达**18.5分**（54.87 vs 36.39），并在所有空间推理基准上取得最佳或可比结果（Table 1b, Table 3）。
- **消融验证**：双编码器设计相比单语义编码器在两项任务上均有显著提升（Figure 6a）；全局注意力在几何专家训练中显著优于帧注意力和混合注意力（Figure 6b）；VG + CE联合损失策略验证了几何与语义监督的互利性（Figure 4）。

## 背景与动机

### 视觉语言模型的空间推理瓶颈

当前主流视觉语言模型（VLMs）在空间理解和推理任务上表现不足，其根本瓶颈在于：这些模型仅依赖非结构化的2D图像-文本数据进行训练，缺乏从2D图像显式重建3D空间的视觉几何学习过程。由于模型从未学习过深度、点云、相机姿态等3D属性，其对物体相对位置、遮挡关系、视角变换等空间概念的理解停留在浅层语义层面，而非基于真实的几何结构。

这一瓶颈在多模态基准测试中已充分暴露。例如，在SPAR-Bench空间推理综合基准上，专有模型GPT-4o仅获得36.39分的平均成绩；在OST-Bench等需要丰富知识储备的任务上，即便是72B参数的大模型也存在明显的能力边界。这表明，单纯扩大模型规模或增加语义训练数据，无法从根本上弥补几何感知能力的缺失。

### 现有方法的缺口：几何学习与语义理解的割裂

现有工作在处理视觉几何与空间理解时呈现出明显的割裂状态：

- **前馈3D重建方法**（如**VGGT**、**π³**）专注于从多帧图像预测深度图、点云和相机姿态，在视觉几何任务上表现优异，但它们不具备语言理解和空间推理能力，无法回答“物体A是否在物体B的左侧”这类需要几何知识的自然语言问题。
- **视觉语言模型**（如**Qwen2-VL-2B**、**GPT-4o**）在多模态理解和文本生成上能力强大，但缺乏显式的3D几何感知模块，空间推理仅依赖2D视觉特征和语言先验，精度和泛化性受限。
- 少数尝试将3D信息引入VLM的工作（如**VLM3R-7B**）虽然取得一定进展，但通常将几何学习作为辅助任务或后处理步骤，未能实现几何感知与语义理解的深层统一和相互增强。

### 核心动机：从“双流假说”到统一架构

本文的核心动机源自认知神经科学中的**双流假说**（two-streams hypothesis）：人类视觉系统包含两条通路——“where通路”处理空间位置和几何关系，“what通路”负责物体识别和语义理解，两者通过交互共同支撑完整的空间认知。

受此启发，G²VLM提出一个根本性问题：**能否在单一模型中同时实现显式的3D视觉几何学习和多模态语义理解，并使两者通过深层交互相互增强？** 这一思路的关键洞察在于：几何感知为空间推理提供精确的结构约束，而语义理解则为几何重建提供上下文先验——两者的结合有望突破现有方法的各自天花板。

## 核心创新

G²VLM 的核心创新在于将**三维视觉几何学习**显式地嵌入到视觉语言模型的架构中，打破了当前 VLM 仅依赖非结构化 2D 图像-文本数据训练的范式。其关键设计可归纳为以下四个“changed slots”，共同构成一个统一的几何基底多模态框架。

### 1. 双专家混合架构（Mixture-of-Transformer-Experts）

G²VLM 采用 MoT 架构，包含两个功能分化的 Transformer 专家：**几何感知专家**（Geometric Perception Expert）和**语义感知专家**（Semantic Perception Expert）。这一设计直接对应人类认知的“双流假说”——几何专家作为“where通路”学习视觉几何，语义专家作为“what通路”负责多模态理解。两者通过**共享自注意力**（shared self-attention）进行令牌级交互，使几何特征与语义特征相互增强（§3.1, Figure 3）。这与传统 VLM 仅依赖单一语义解码器的范式形成根本区别。

### 2. 双视觉编码器设计

模型采用两套视觉编码器分别服务于不同专家：**DINOv2** 提取低层几何视觉特征，注入几何感知专家；**Qwen2 Vision Encoder**（含 M-RoPE）提取动态分辨率的多模态语义特征，服务于语义感知专家。消融实验证实，这一双编码器设计在视觉几何和空间理解两项任务上均显著优于仅使用单一语义编码器（如 CLIP）的方案（Figure 6a, §4.3）。

### 3. 全局注意力机制

几何感知专家内部采用**全局注意力**（global attention），使所有帧的令牌能够相互关注，而非使用常见的因果注意力或帧内注意力。消融实验显示，全局注意力在几何感知专家训练中的损失始终低于帧注意力和混合注意力变体，是视觉几何学习的关键使能因素（Figure 6b, §4.3）。

### 4. 专用几何输出头

在标准语言建模头之外，G²VLM 额外增加了三个轻量几何头（局部点云头、全局点云头、相机姿态头），由轻量 Transformer 解码器实现。这些几何头将几何专家的隐藏状态直接映射为结构化的 3D 输出——每帧的相机姿态 $T_i$ 和像素对齐的 3D 点云 $X_i$，如公式所示：

$$f \left( ( h _ { i } ) _ { i = 1 } ^ { N } \right) = ( T _ { i } , X _ { i } , ) _ { i = 1 } ^ { N }$$

这一设计使模型能够从 2D 观测中端到端地预测显式 3D 几何，并将这些几何特征用于下游空间推理，实现了“重建即理解”的闭环（§3.1, Eq. 1）。

### 创新协同效应

上述四个 changed slots 并非孤立改进，而是通过**联合训练策略**产生协同效应。实验表明，同时施加视觉几何损失（$\mathcal{L}_{VG}$）和交叉熵语言损失（CE Loss）的 VG+CE 联合训练方案，在视觉几何精度和空间推理能力上均优于单独训练或交替训练策略（Figure 4, §3.3）。这验证了几何监督与语义监督之间的互利关系——更强的几何感知直接转化为更强的空间推理能力，反之亦然。

## 整体框架

G²VLM 的整体设计遵循一个核心洞察：将人类视觉认知的“双流假说”映射为模型架构——几何感知专家（“where通路”）负责从2D图像显式重建3D空间，语义感知专家（“what通路”）负责多模态理解与空间推理，二者通过共享自注意力实现双向交互，使几何学习与语义理解相互增强（Figure 2, Figure 3）。

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/002_Figure_2.jpg]]
*Figure 2: Our model*

### 宏观 Pipeline

模型的输入为一组多视图图像（可包含文本查询），输出分为两条并行的信息流：

1. **视觉几何流**：从输入图像中预测每帧的相机姿态、像素对齐的局部3D点云以及全局点云。
2. **语义推理流**：基于图像和文本输入进行空间理解、问答与推理，输出自然语言答案。

两条信息流并非独立运行，而是在 Transformer 层内部通过共享自注意力持续交换特征，使几何令牌与语义令牌能够相互感知。

### 模块构成与数据流

G²VLM 采用 Mixture-of-Transformer-Experts (MoT) 架构，包含以下核心模块（Figure 3）：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **DINOv2 视觉编码器** | 提取低层几何视觉特征（纹理、边缘、深度线索） | 多视图图像 | 几何视觉令牌 |
| **Qwen2 视觉编码器** | 提取动态分辨率的多模态语义特征（含 M-RoPE 位置编码） | 多视图图像 | 语义视觉令牌 |
| **几何感知专家**（LLM Transformer 层） | 通过全局注意力处理几何令牌，推理 3D 感知的隐藏状态 | DINOv2 输出令牌 | 几何隐藏状态 $h_i$ |
| **语义感知专家**（LLM Transformer 层） | 处理语义视觉令牌与文本令牌，进行多模态理解与空间推理 | Qwen2 输出令牌 + 文本令牌 | 语义隐藏状态 |
| **几何头**（轻量 Transformer 解码器） | 将几何隐藏状态解码为显式 3D 输出 | 几何隐藏状态 $h_i$ | 相机姿态 $T_i$、局部点云 $X_i$、全局点云 |
| **共享自注意力** | 实现几何与语义令牌之间的跨专家信息交互 | 两路令牌拼接 | 双向增强的隐藏状态 |

### 关键设计决策

**双编码器分工**：消融实验证实，使用 DINOv2 处理几何特征、CLIP/Qwen2 编码器处理语义特征的双编码器设计，在视觉几何和空间理解两项任务上均显著优于单一编码器方案（Figure 6a）。这验证了低层几何特征与高层语义特征需要不同的视觉表征提取路径。

**全局注意力机制**：几何感知专家内部采用全局注意力（所有帧共享），而非帧注意力或混合注意力。消融实验的训练损失曲线表明，全局注意力在几何感知训练中始终是最优变体（Figure 6b）。

**几何头映射**：几何隐藏状态到显式 3D 输出的映射遵循公式 (1)：

$$f \left( ( h _ { i } ) _ { i = 1 } ^ { N } \right) = ( T _ { i } , X _ { i } ) _ { i = 1 } ^ { N }$$

其中 $T_i$ 为第 $i$ 帧的相机姿态，$X_i$ 为像素对齐的 3D 点云。

**训练策略**：联合训练阶段采用 VG（视觉几何损失）+ CE（交叉熵语言损失）的组合监督策略，在 Figure 4 的对比实验中显著优于仅使用 VG 损失或仅使用 CE 损失的方案，证实了几何监督与语义监督的互利性。

### 与基线架构的本质差异

相较于标准 VLM（如 **Qwen2-VL-2B**）的单一解码器设计，G²VLM 的核心改动在于：

- **架构层面**：从单专家变为双专家 MoT，新增独立的几何感知 Transformer 分支。
- **编码器层面**：从仅语义编码器变为几何+语义双编码器。
- **输出层面**：在语言建模头之外增加几何头（局部点云头、全局点云头、相机姿态头）。
- **注意力层面**：几何专家采用全局注意力替代常用的因果/帧注意力。

值得注意的是，G²VLM 不使用 **VGGT** 中的相机令牌（camera tokens）这一强先验，也不依赖预训练权重的微调（如 **π³** 的做法），却能在深度估计等任务上取得可比甚至更优的结果，体现了架构设计本身的效率。

### 补充图表

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/001_Figure_1.jpg]]
*Figure 1: We present G2VLM, a geometry grounded vision-language model proficient in both spatial 3D reconstruction and spatial understanding tasks. For spatial reasoning questions, G2VLM can directly predict 3D geometry and employ interleaved reasoning for an answer*

## 核心模块与公式推导

G²VLM 的核心架构建立在**混合Transformer专家（Mixture-of-Transformer-Experts, MoT）** 设计之上，包含两个功能分化的专家模块，并通过共享自注意力机制实现跨专家交互。以下详述各关键模块及其数学形式化。

### 3.1 双专家架构与视觉编码

G²VLM 包含两个 Transformer 专家（Figure 3）：

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/003_Figure_3.jpg]]
*Figure 3: We present G2VLM, a unified model that integrates both a geometric perception expert for 3D reconstruction and a semantic perception expert for multimodal understanding and spatial reasoning tasks. All tokens can do shared multi-modal self attention in each transformer block*

- **几何感知专家（Geometric Perception Expert）**：作为“where通路”，负责从2D图像中显式学习3D视觉几何。该专家采用 **DINOv2 视觉编码器**注入底层视觉信息，随后通过 LLM 层的**全局注意力（global attention）** 推理3D感知的隐藏状态。全局注意力的选择经过消融验证（Figure 6b），相比帧注意力和混合注意力具有最低的训练损失。

- **语义感知专家（Semantic Perception Expert）**：作为“what通路”，负责多模态语义理解与空间推理。该专家基于 **Qwen2 Vision Encoder**（含 M-RoPE）提取动态分辨率的多模态语义特征，以 Qwen2-VL-2B 作为基础 VLM 初始化。

两个专家的令牌在每一层 Transformer 块中通过**共享自注意力**进行交互，使得几何特征与语义特征能够相互增强。

### 3.2 几何头映射

几何感知专家输出的隐藏状态通过三个轻量级 Transformer 解码器头映射为显式3D属性。给定 $N$ 帧图像的视觉几何隐藏状态 $(h_i)_{i=1}^N$，几何头映射函数为：

$$f\left((h_i)_{i=1}^N\right) = (T_i, X_i)_{i=1}^N \quad \text{(Eq. 1)}$$

其中：
- $T_i$：第 $i$ 帧的相机姿态（包含旋转与平移参数）
- $X_i$：第 $i$ 帧像素对齐的3D点云（point map）

三个几何头分别为：
- **局部点云头**：预测每帧像素对齐的局部3D点云
- **全局点云头**：预测全局坐标系下的统一3D点云
- **相机姿态头**：预测帧间相对相机姿态

### 3.3 视觉几何损失函数

视觉几何训练的总损失为三项损失的加权和：

$$\mathcal{L}_{VG} = \mathcal{L}_{\mathrm{points}} + \lambda_{\mathrm{cam}}\mathcal{L}_{\mathrm{cam}} + \lambda_{\mathrm{normal}}\mathcal{L}_{\mathrm{normal}} \quad \text{(Eq. 2)}$$

#### 点云重建损失

点云损失采用逆深度加权的 L1 距离，通过最优尺度 $s^*$ 将预测点云与真值点云对齐：

$$\mathcal{L}_{\mathrm{points}} = \frac{1}{3NHW}\sum_{i=1}^{N}\sum_{j=1}^{H \times W}\frac{1}{z_{i,j}}\left\|s^{*}\hat{\mathbf{x}}_{i,j} - \mathbf{x}_{i,j}\right\|_1 \quad \text{(Eq. 3)}$$

其中 $z_{i,j}$ 为深度值，$\hat{\mathbf{x}}_{i,j}$ 和 $\mathbf{x}_{i,j}$ 分别为预测和真值3D点，$s^*$ 为最小化对齐误差的最优尺度因子。逆深度加权确保远距离点的误差贡献被适当抑制。

#### 相机姿态损失

相机损失在所有视图对上计算旋转与平移误差的均值：

$$\mathcal{L}_{\mathrm{cam}} = \frac{1}{N(N-1)}\sum_{i \neq j}\left(\mathcal{L}_{\mathrm{rot}}(i,j) + \lambda_{trans}\mathcal{L}_{\mathrm{trans}}(i,j)\right) \quad \text{(Eq. 4)}$$

**旋转损失**采用测地线距离（角度制）：

$$\mathcal{L}_{\mathrm{rot}}(i,j) = \operatorname{arccos}\left(\frac{\mathrm{Tr}((R_{ij})^{\top}\hat{R}_{ij}) - 1}{2}\right) \quad \text{(Eq. 5)}$$

其中 $R_{ij}$ 和 $\hat{R}_{ij}$ 分别为真值和预测的相对旋转矩阵，该损失度量两个旋转矩阵之间的最小角度差。

**平移损失**采用 Huber 损失，在缩放后计算：

$$\mathcal{L}_{\mathrm{trans}}(i,j) = \mathcal{H}_{\delta}(s^{*}\hat{t}_{ij} - t_{ij}) \quad \text{(Eq. 6)}$$

其中 $\hat{t}_{ij}$ 和 $t_{ij}$ 为预测和真值相对平移向量，$\mathcal{H}_{\delta}$ 为 Huber 损失函数（参数 $\delta$），$s^*$ 为与点云损失共享的最优尺度。

#### 法线损失

为促进平滑表面重建，引入法线角度损失：

$$\mathcal{L}_{\mathrm{normal}} = \sum_{i=1}^{N}\sum_{j=1}^{H \times W}\operatorname{arccos}\left(\hat{n}_{i,j} \cdot n_{i,j}\right) \quad \text{(Eq. 7)}$$

其中 $\hat{n}_{i,j}$ 和 $n_{i,j}$ 分别为预测和真值表面法线，损失累积所有像素的法线夹角。

### 3.4 联合训练策略

联合训练阶段同时优化视觉几何损失 $\mathcal{L}_{VG}$ 和语义理解的交叉熵损失 $\mathcal{L}_{CE}$。消融实验（Figure 4）对比了三种监督策略：
- 仅 $\mathcal{L}_{VG}$
- 仅 $\mathcal{L}_{CE}$
- **$\mathcal{L}_{VG} + \mathcal{L}_{CE}$ 联合损失**

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of three different loss supervision mechanisms for the joint-training stage. Note that for visual geometry scores, lower is better. The VG + CE Loss approach yields the best performance, demonstrating that combining visual geometry and spatial understanding supervision mutually benefits spatial reasoning tasks*

结果表明，**VG + CE Loss** 联合训练在视觉几何精度和空间推理能力上均取得最优效果，证实了几何监督与语义监督之间的互利关系。为缓解大规模3D标注数据的需求，联合训练阶段采用冻结几何感知专家的策略，但这也可能限制了跨任务协同提升的上限。训练过程中需依赖损失裁剪和梯度范数裁剪来维持稳定性。

## 实验与分析

### 视觉几何重建：与 SOTA 前馈方法的对比

G²VLM 在三个核心视觉几何任务上与主流前馈重建方法进行了系统对比（Table 1a）。

**单目深度估计**方面，模型在 Sintel 数据集上取得了 **0.297** 的绝对相对误差（Abs Rel），显著优于最强基线 VGGT 的 0.335（Δ = −0.038）。这一提升尤为值得注意，因为 G²VLM 采用了更简单的全局注意力机制，且未使用 VGGT 中提供强相机先验的相机令牌（camera tokens）。

**点云估计**方面，在 7Scenes 基准上，G²VLM 的 Completion 指标为 0.029，与 VGGT 的 0.026 基本持平。Accuracy 指标也取得了可比结果，表明模型在 3D 结构重建精度上达到了前馈方法的一线水平。

**相机姿态估计**方面，模型在 Co3Dv2 上的 AUC@30 达到 74.81，虽低于 VGGT 的 88.59（Δ = −13.78），但考虑到 G²VLM 无需从预训练权重微调（如 π³ 的做法），这一差距是可以理解的。相机姿态仍是视觉几何任务中相对薄弱的环节。

Table 1a 的整体结果表明，G²VLM 作为一个同时兼顾语义理解的统一模型，在纯几何重建任务上已能与专用前馈方法竞争，验证了几何感知专家设计的有效性。

### 空间推理：全面超越专有与开源模型

在空间推理能力评估上，G²VLM-SR 展现出显著优势（Table 1b, Table 3）。

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/010_Table_3.jpg]]
*Table 3: Performance of different models on SPAR-Bench The highest, second-highest, and third-highest scores in each category are highlighted with light red , light orange , and light yellow , respectively. SPAR-Bench (tiny) refers to a subset of the full benchmark, where 50 questions are sampled per task. Our model, G2VLM-SR, demonstrate the best performance consistently across all tasks. Notably, it surpasses human performance in low category*

**SPAR-Bench** 是该领域最具综合性的基准。G²VLM-SR 以 **54.87** 的平均分大幅领先 GPT-4o 的 36.39（Δ = +18.48），并在所有子任务上取得最佳或次佳成绩。值得注意的是，在 SPAR-Bench 的低难度类别中，模型甚至超越了人类表现（Table 3）。

**MindCube** 基准上，G²VLM-SR 达到 56.51，超越专用空间专家模型 VLM3R-7B 的 51.18（Δ = +5.33），证明几何感知专家的 3D 理解对空间推理任务有直接增益。

**OST-Bench** 上，模型得分约 36，落后于 Qwen2.5-VL-72B 的 47.13。这一差距主要源于模型规模限制（2B vs 72B），OST-Bench 对知识存储量的高需求使小模型的劣势被放大。该结果表明，在知识密集型空间任务上，扩展模型规模仍是必要的后续方向。

### 消融实验：关键设计选择验证

#### 双编码器设计的必要性

Figure 6(a) 对比了三种编码器配置：仅 CLIP 语义编码器、仅 DINO 几何编码器、以及 DINO + Qwen2 语义的双编码器。结果显示，双编码器设计在视觉几何和空间理解两项任务上均取得最优性能。单一语义编码器因缺乏低层几何特征导致重建精度下降，单一几何编码器则削弱了多模态语义理解能力。这验证了“双流假说”的核心主张——几何与语义需要专门的感知通路。

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/009_Figure_6.jpg]]
*Figure 6: Experimental study results. (a) The dual encoder design, with both a semantic-rich CLIP encoder and a low-level vision DINO encoder, yields the best performance on both visual geometry and spatial understanding tasks. (b) Training loss curves for three different attention mechanisms during geometric perception expert training; global attention is consistently the best variant*

#### 注意力机制的选择

Figure 6(b) 展示了三种注意力机制在几何感知专家训练中的损失曲线：全局注意力（global attention）、帧注意力（frame attention）和混合注意力（hybrid attention）。全局注意力在所有训练阶段均保持最低损失，收敛速度最快。帧注意力因限制了跨帧信息交互而表现最差。这一结果说明，3D 几何推理本质上需要全局上下文，帧间信息隔离会严重损害深度和姿态估计精度。

#### 几何专家的贡献

Table 2 的消融显示，完整的 G²VLM-SR（含几何感知专家）在 SPAR-Bench 上达到 54.87，而仅微调基础模型 Qwen2-VL-2B 的得分为 48.93（Δ = +5.94）。移除几何专家后性能显著下降，证实了几何表示对空间推理的因果性贡献。更重要的是，随着几何专家性能的提升，空间推理得分同步增长，揭示了两种表示之间的正向互促关系。

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the design choices for*

#### 联合训练策略的比较

Figure 4 对比了三种损失监督机制：仅视觉几何损失（VG Loss）、仅交叉熵损失（CE Loss）、以及两者结合（VG + CE Loss）。VG + CE Loss 在两项任务上均取得最佳效果，证明几何监督和语义监督的联合训练不仅不会相互干扰，反而能通过共享自注意力实现互利增强。这一发现为多任务统一训练提供了有力的经验支撑。

### 定性结果与泛化能力

Figure 5 展示了 G²VLM 在开放域图像上的重建结果，涵盖物体级、结构级、室内和室外场景，包括动态和静态内容。模型在未见过的场景类型上仍能生成合理的 3D 点云和深度图，表明几何感知专家学到的是可迁移的 3D 理解能力，而非对训练分布的简单记忆。

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of our model*

### 失败模式与局限

1. **相机姿态估计精度不足**：在 Co3Dv2 上与 VGGT 差距明显，可能源于未使用相机令牌提供的强先验。对于需要精确相机位姿的下游应用（如 SLAM），当前精度尚不充分。

2. **模型规模瓶颈**：2B 参数限制了知识密集型任务（如 OST-Bench）的表现。框架能否线性扩展到更大规模而不出现几何精度退化，仍需验证。

3. **训练稳定性问题**：论文提到训练过程需依赖损失裁剪和梯度范数裁剪来维持稳定，暗示双专家联合训练存在优化难点。冻结几何专家的折中策略虽缓解了数据需求，但可能限制了跨任务的进一步协同提升。

4. **长序列处理的效率**：全局注意力在长帧序列上的计算和内存消耗问题尚未解决，可能限制其在视频级 3D 重建场景中的应用。

### 补充图表

![[assets/figures/papers/paper_list_l2169_https_arxiv_org_abs_2511_21688/figures/005_Table_1.jpg]]
*Table 1: Comparison with mainstream feed-forward 3D reconstruction methods on visual geometry tasks and with representative VLMs on spatial understanding and reasoning tasks. Our model demonstrates proficient performance in both aspects of spatial tasks, demonstrating its universality and effectiveness*

## 方法谱系与知识库定位

### 与基线方法的关系

G²VLM的架构设计直接回应了当前视觉语言模型（VLMs）在空间理解上的根本瓶颈：仅依赖非结构化的2D图像-文本数据训练，缺乏从2D图像显式重建3D空间的视觉几何学习过程。这一洞察将G²VLM置于两条研究脉络的交汇点上。

**相对于前馈3D重建方法。** 在视觉几何任务上，G²VLM的主要竞争基线是**VGGT**——当前前馈3D重建的最强方法。G²VLM在Sintel数据集上的单目深度估计将绝对相对误差（Abs Rel）从VGGT的0.335降至0.297（Table 1a），在点云重建的完成度指标上也达到可比水平。值得注意的是，这一优势是在不使用VGGT所依赖的相机令牌（camera tokens）这一强先验、且采用更简单的全局注意力机制的条件下取得的——这暗示几何感知专家的设计本身具有更强的特征提取效率。然而，在相机姿态估计任务（Co3Dv2, AUC@30）上，G²VLM（74.81）仍明显落后于VGGT（88.59），表明前馈方法在显式相机推理上仍有结构性优势。另一个基线**π³**同样在点云和相机姿态任务上提供了对比参照，但G²VLM未依赖其预训练权重微调策略。

**相对于空间推理VLM。** 在空间推理维度，G²VLM-SR的定位更为独特。与专有模型**GPT-4o**相比，G²VLM-SR在SPAR-Bench上取得了54.87 vs. 36.39的显著优势（+18.5分），在所有子任务上均保持领先（Table 3），甚至在部分子任务上超越人类表现。与空间专家模型**VLM3R-7B**相比，G²VLM-SR在MindCube上以56.51 vs. 51.18领先，验证了几何感知专家带来的空间推理增益。但G²VLM的边界同样清晰：在需要大量知识存储的任务（如OST-Bench）上，其约36分的表现远落后于**Qwen2.5-VL-72B**的47.13分，说明2B参数规模的语义知识容量仍是硬约束。

**相对于基础VLM。** 消融实验（Table 2）揭示了G²VLM设计的净增益：完整G²VLM-SR在SPAR-Bench上达到54.87，而仅对基础模型**Qwen2-VL-2B**进行微调只能达到48.93。这一近6分的提升直接归因于几何感知专家的引入，证实了几何与语义表征之间存在正向交互——几何专家性能的提升会同步改善空间推理能力。

### 适用边界与局限

G²VLM的适用边界由以下四个维度定义：

**数据依赖性。** 几何感知专家的训练依赖大规模3D标注数据。联合训练阶段采用冻结几何专家的策略虽可缓解数据需求，但也限制了跨任务的进一步协同提升——这是当前架构的一个折中瓶颈。在不依赖大规模3D标注的条件下，通过自监督或半监督方法扩展几何学习能力仍是开放问题。

**计算资源与训练稳定性。** 模型训练需要多卡A800运行数天，且训练过程存在不稳定性，需依赖损失裁剪和梯度范数裁剪来维持收敛。这限制了该方法在资源受限场景下的可复现性和快速迭代能力。

**模型规模上限。** 当前2B参数规模在需要大量知识存储的任务上表现受限（如OST-Bench落后于72B模型）。将G²VLM架构扩展到7B乃至72B参数时，性能提升能否保持——特别是视觉几何精度是否会出现退化——尚待验证。冻结几何专家这一策略的上限同样未知。

**任务覆盖范围。** 当前框架尚未探索在3D场景编辑或更广泛的具身AI任务（如机器人操作、导航）中的应用。全局注意力机制在处理超长帧序列时的计算效率和内存消耗问题也未解决。

### 核心创新定位

G²VLM的核心创新可概括为三个相互关联的设计选择，每个选择都有明确的消融证据支撑：

1. **双专家混合架构（MoT）**：将几何感知专家与语义感知专家通过共享自注意力耦合，模仿人类认知的“双流假说”（Figure 2, Figure 3）。消融实验（Figure 6a）表明，双编码器设计（DINOv2用于几何，CLIP用于语义）相比单一语义编码器在视觉几何和空间理解两项任务上均有显著提升。

2. **全局注意力机制**：在几何感知专家训练中，全局注意力相比帧注意力和混合注意力始终取得更低的训练损失（Figure 6b），验证了跨帧全局上下文对3D推理的关键作用。

3. **联合训练策略**：VG + CE损失（视觉几何损失 + 交叉熵语言建模损失）的联合监督在两项任务上均取得最佳效果（Figure 4），证明了几何监督与语义监督的互利性——这是连接两条研究脉络的核心因果机制。

### 开放问题

基于上述分析，G²VLM框架面临的关键开放问题包括：能否在不依赖大规模3D标注的条件下通过自监督或半监督方法提升几何感知专家的学习能力；扩展至更大参数规模时视觉几何精度是否会退化；是否存在比冻结几何专家更优的联合训练策略；以及该统一框架能否与具身AI任务无缝集成并带来实际增益。这些问题的回答将决定G²VLM是否能从当前的概念验证走向更广泛的实际部署。

## 原文 PDF

![[paperPDFs/CVPR_2026/G_2_VLM_Geometry_Grounded_Vision_Language_Model_with_Unified_3D_Reconstruction_and_Spatial_Reasoning.pdf]]
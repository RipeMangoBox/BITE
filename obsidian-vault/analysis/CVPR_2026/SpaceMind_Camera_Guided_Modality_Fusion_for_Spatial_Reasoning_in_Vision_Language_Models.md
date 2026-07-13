---
title: "SpaceMind: Camera-Guided Modality Fusion for Spatial Reasoning in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpaceMind_Camera_Guided_Modality_Fusion_for_Spatial_Reasoning_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- SpaceMind
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将相机表示从被动元数据提升为独立的主动引导模态，通过相机条件调控空间特征的融合，实现视点感知的空间推理。
primary_logic: 相机信息应作为主动引导信号而非被动辅助数据，用来定向地控制空间特征向视觉特征的注入，从而显著增强VLMs的3D空间推理能力。
claims:
- 在VSI-Bench上，SpaceMind的平均得分达到69.6，比之前的最佳方法（如Spatial-MLLM的60.9）提升超过8.7个百分点，并在所有子任务上均超越先前模型。
- 消融实验表明，逐步添加VGGT空间标记、token权重MLP（twMLP）、几何MLP（geoMLP）和SwiGLU门控，平均准确率从63.07持续提升至69.58，验证了相机引导融合各组件的有效性。
- 在SQA3D和SPBench上也取得最优结果，证明该设计具有良好的跨数据集泛化能力，且仅使用RGB视频输入即可超越依赖深度或点云等额外模态的方法。
- VSI-Bench (8 subtasks) 上 Average Accuracy = 69.6
---

# SpaceMind: Camera-Guided Modality Fusion for Spatial Reasoning in Vision-Language Models

> [!tip] 核心洞察
> 相机信息应作为主动引导信号而非被动辅助数据，用来定向地控制空间特征向视觉特征的注入，从而显著增强VLMs的3D空间推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpaceMind：基于相机引导模态融合的空间推理视觉语言模型 |
| 英文题名 | SpaceMind: Camera-Guided Modality Fusion for Spatial Reasoning in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.23075) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SpaceMind |
| Dataset | VSI-Bench, SPBench |

> [!tip] 效果简介
> - VSI-Bench (8 subtasks) 上，Average Accuracy 69.6 vs 60.9 (prior best, Spatial-MLLM) (+8.7)。
> - SPBench 上，Overall Accuracy 67.3 vs best prior (all listed models) (outperforms all)。

## 概要

现有视觉语言模型（VLM）在3D空间推理任务中面临一个关键瓶颈：**相机（视点）特征与场景（内容）特征在融合过程中被混为一谈，缺乏对视点与场景之间差异的显式建模**。这一设计缺陷使得模型难以稳定地理解物体间的空间关系、相对方向与距离，在需要精确几何推理的场景中表现受限。

针对上述问题，SpaceMind 提出了一个核心洞察：**相机信息不应仅作为被动元数据附加于输入，而应被提升为独立的主动引导模态**。通过让相机标记显式地调控空间特征向视觉特征的注入过程，模型能够实现视点感知的空间推理，从而显著增强3D场景理解能力。

在方法层面，SpaceMind 采用双编码器架构，将视觉编码器（InternViT）与空间编码器（VGGT）并行提取的特征通过一个轻量级的**相机引导模态融合模块（Camera-Guided Modality Fusion, CGMF）**进行整合。CGMF 的核心创新在于三个相机引导机制：(1) 相机条件偏置，用于调制空间键值对；(2) 查询无关的空间标记重要性加权，反映几何预测的可靠性；(3) 相机条件门控（SwiGLU），实现视点感知的融合特征调制。这一设计使融合后的标记保持与原始视觉标记相同的形状，可无缝接入任意标准 VLM 架构的 LLM 主干，且仅需 RGB 视频输入，无需深度或点云等额外模态。

实验结果表明，SpaceMind 在 VSI-Bench 上取得了 **69.6 的平均准确率**，较先前最佳方法 Spatial-MLLM（60.9）提升超过 **8.7 个百分点**，并在所有子任务上均超越已有模型。在 SQA3D 和 SPBench 上同样取得最优结果，验证了其跨数据集的泛化能力。消融实验进一步证实，从浅层交叉注意力到完整的相机引导融合，每个组件的逐步添加均带来一致的性能增益（63.07 → 66.77 → 68.60 → 69.00 → 69.58），充分验证了相机作为主动引导模态这一设计理念的有效性。



视觉语言模型（VLMs）在图像描述、视觉问答等二维理解任务上取得了显著进展，但在三维空间推理方面仍面临根本性挑战。当任务涉及物体相对位置判断、绝对距离估计、路径规划或空间关系推理时，现有模型的表现往往远低于人类水平。这一瓶颈的核心在于，空间推理不仅需要理解场景中“有什么”（内容特征），更需要精确把握“从何处看”（视点特征）——而这两类信息在现有VLM的融合机制中常常被混为一谈。

当前具备空间感知能力的VLM，如 **Spatial-MLLM**（Wu et al., NeurIPS 2025）和 **VLM-3R**，通常采用双编码器架构：一个视觉编码器提取语义丰富的二维外观特征，另一个几何编码器（或深度估计器）从图像序列中重建三维几何信息。然而，这些方法在融合视觉与空间特征时，普遍采用浅层交叉注意力或简单的MLP投影，将相机标记（反映视点位姿）与空间标记（反映场景几何）拼接后统一处理。这种做法的隐含假设是，相机信息只是另一种“辅助数据”，而非具有独立控制能力的引导信号。其后果是，模型难以区分“物体本身的位置”与“观察者相对于物体的位置”，导致在需要视点感知的空间推理任务上表现不稳定。

SpaceMind 的核心动机源于一个关键洞察：**相机信息应被提升为主动引导模态，而非被动辅助数据**。在三维场景理解中，同一场景从不同视点观察会产生截然不同的二维投影，但物体的真实空间关系保持不变。因此，有效的空间推理要求模型能够以相机条件的方式调控空间特征向视觉特征的注入——即让“从哪看”显式地指导“看到了什么”的几何解释。现有方法恰恰缺失了这种视点感知的融合控制机制，这正是 SpaceMind 试图解决的核心瓶颈。



## 核心方法与创新机理

### 问题瓶颈：视点与场景特征的混淆

现有具备空间推理能力的视觉语言模型（VLM）普遍存在一个深层缺陷：它们将相机（视点）特征与场景（内容）特征混为一谈。无论是**Spatial-MLLM**（Wu et al., NeurIPS 2025）采用的几何编码器，还是**VLM-3R**、**SpaceR**等模型，其融合机制本质上都是将相机标记作为辅助嵌入附加到输入中，或隐式地混合在融合层内，缺乏对视点与场景之间差异的显式建模。这种“被动元数据”式的处理方式，使得模型难以理解“从何处看”与“看到了什么”之间的因果关系，从根本上限制了3D空间推理能力的上限。

### 核心洞察：将相机提升为主动引导模态

SpaceMind的核心创新在于一个关键的认知转向：**相机信息不应是被动的辅助数据，而应作为独立的主动引导信号**，定向地控制空间特征向视觉特征的注入过程。这一设计理念将“相机”从传统VLM中的附属角色提升为模态融合的“控制器”，使模型能够显式地建模视点变化对空间理解的因果影响。

### 关键创新点：相机引导模态融合（CGMF）

为实现上述理念，SpaceMind设计了**相机引导模态融合（Camera-Guided Modality Fusion, CGMF）**模块，通过三个递进的机制实现视点感知的空间推理：

**1. 相机条件空间偏置（Camera-Conditioned Spatial Bias）**

与基线方法将相机标记与空间/视觉标记拼接后统一处理不同，CGMF通过拼接空间与相机标记后经MLP生成相机条件的空间偏置 $B_g$，用于调制空间键 $K$ 和值 $V$：

$$B_g = \operatorname{MLP}([f_s, f_c])$$

这使得空间特征的表达直接受相机视点调控，而非被动地与视觉特征混合。

**2. 查询无关的空间重要性加权（Token Weight MLP）**

现有方法未显式估计空间标记的置信度，而CGMF引入轻量级**token权重MLP（twMLP）**，仅从空间分支预测每个空间标记的重要性权重 $W_t$：

$$W_t = \sigma(\operatorname{MLP}(f_s))$$

该权重通过sigmoid输出，反映几何预测的可靠性，并用于重新缩放值向量。这一设计使模型能够自适应地抑制不可靠的空间预测，尤其在遮挡或远距离场景中效果显著。

**3. 相机条件门控融合（SwiGLU Gating）**

最终，CGMF采用SwiGLU机制对相机嵌入进行双分支变换后逐元素相乘，形成相机条件门控信号 $g$，用于调制融合特征：

$$g = \operatorname{Swish}(u) \odot v$$

$$f_{\mathrm{fused}} = P_L(f_{\mathrm{proj}}) \odot g[:,\mathrm{None},:] + f_v$$

这种门控设计确保只有与当前视点相关的空间信息被注入视觉流，而无关的几何噪声被有效过滤。

### 与基线方法的本质差异

| 设计维度 | 基线方法 | SpaceMind |
|---------|---------|-----------|
| **相机标记角色** | 被动辅助嵌入，隐式混合 | 独立控制模态，主动引导融合 |
| **融合机制** | 浅层交叉注意力或简单MLP投影 | 相机条件偏置 + 重要性加权 + 条件门控 |
| **空间置信度** | 未显式建模 | twMLP预测查询无关的标记重要性 |
| **训练策略** | 通常冻结视觉编码器或完全微调 | 冻结视觉/空间编码器，完全训练CGMF，LLM主干用LoRA（秩256） |

### 创新验证：消融实验的证据链

消融实验（Table 4）清晰地展示了CGMF各组件的因果贡献：以纯InternVL3-8B为基线（VSI-Bench平均准确率63.07），逐步添加VGGT空间标记（+3.70）、twMLP（+1.83）、geoMLP（+0.40）和SwiGLU门控（+0.58），最终达到69.58。每一组件的增益均具有统计显著性，且在不同子任务上呈现一致的提升趋势，验证了相机引导融合设计的有效性。

这一创新使SpaceMind在仅使用RGB视频输入的条件下，在VSI-Bench上以69.6的平均得分超越先前最佳方法**Spatial-MLLM**（60.9）达8.7个百分点，并在SQA3D和SPBench上均取得最优结果，证明了视点感知融合范式的跨数据集泛化能力。



SpaceMind 的整体设计遵循“双编码器 + 相机引导融合 + 语言模型”的三段式流水线，目标是将3D空间推理能力注入标准视觉语言模型，同时保持与现有VLM架构的兼容性。其核心思路是 **将相机表示从被动元数据提升为独立的主动引导模态**，通过相机条件显式调控空间特征向视觉特征的注入过程。

### 输入与双编码器

系统接收一个文本提示 $T$ 和一个图像序列 $\mathcal{S} = \{ I_i \}_{i=1}^{N}$，其中每帧 $I_i \in \mathbb{R}^{\tilde{H} \times W \times 3}$ 代表场景的一个视点。两股并行的编码器分别处理该序列：

- **视觉编码器** $e_v$（InternViT）：从图像序列中提取语义视觉标记 $f_v \in \mathbb{R}^{N \times M_v \times d_v}$，提供丰富的2D外观表示。
- **空间编码器** $e_s$（VGGT）：从同一图像序列中提取几何感知的空间标记 $f_s \in \mathbb{R}^{N \times M_s \times d_s}$、每帧相机标记 $f_c \in \mathbb{R}^{N \times 1 \times d_s}$ 以及寄存器标记 $f_{\text{register}}$。寄存器标记在后续处理中被直接丢弃，相机标记则作为独立的控制信号保留。

上述双编码器设计的关键在于 **视点与内容的解耦**：视觉编码器负责“场景长什么样”，空间编码器负责“场景在哪里、从哪个角度看”。相机标记 $f_c$ 正是视点信息的显式载体，为后续的相机引导融合提供了操作对象。

### 相机引导模态融合（CGMF）

两股编码器输出在进入语言模型之前，先经过SpaceMind的核心创新模块——**相机引导模态融合**（Camera-Guided Modality Fusion, CGMF）。该模块接收三路输入（视觉标记 $f_v$、空间标记 $f_s$、相机标记 $f_c$），输出形状与 $f_v$ 完全相同的融合标记 $f_{\text{fused}}$，从而无缝对接下游LLM的输入接口。

CGMF 通过三个递进的机制实现相机引导的融合：

1. **相机条件空间偏置**：将空间标记与相机标记拼接后通过MLP生成偏置 $B_g$，用于调制空间分支的键 $K$ 和值 $V$，使空间特征的表达依赖于当前视点。
2. **查询无关的空间重要性加权**：通过轻量级 token 权重 MLP（twMLP）从空间标记 $f_s$ 预测每个空间patch的重要性权重 $W_t$，经 sigmoid 后重新缩放值向量，反映几何预测的可靠性。
3. **相机条件门控融合**：采用 SwiGLU 机制对相机嵌入进行双分支变换后生成门控信号 $g$，用以调制投影后的融合特征，最终与原始视觉特征残差相加。

这三步的递进关系在消融实验中得到验证：逐步添加 VGGT 空间标记、twMLP、geoMLP 和 SwiGLU 门控，VSI-Bench 平均准确率从 63.07 持续提升至 69.58（Table 4），证明相机引导融合各组件的有效性。

### 语言模型推理

融合后的标记 $f_{\text{fused}}$ 与文本提示 $T$ 一同送入 LLM 骨干 $g$（InternVL3-8B，底层为 Qwen2-7B），生成最终的空间推理回答 $R$。训练时冻结视觉和空间编码器，完全训练 CGMF 模块，并对 LLM 主干应用秩为256的 LoRA 适配，保证训练高效且不破坏预训练知识。

整体而言，SpaceMind 的流水线设计实现了 **仅使用RGB视频输入即可超越依赖深度或点云等额外模态的方法**（Table 2、Table 3），在 VSI-Bench 上平均得分达 69.6，较先前最优方法 Spatial-MLLM（60.9）提升超过 8.7 个百分点，并在所有子任务上均取得领先（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of SpaceMind. Given a text prompt and an image sequence, a visual encoder produces semantic visual tokens, while a spatial encoder produces geometry-aware tokens together with per-frame camera tokens that summarize viewpoint information. The proposed Camera-Guided Modality Fusion (CGMF) module takes these three streams as input: it uses camera tokens to modulate spatial tokens, estimates their relative importance, and injects the resulting spatial cues into the visual tokens. The fused, view-aware visual tokens preserve the original token shape expected by the multimodal LLM, enabling SpaceMind to be trained end-to-end on RGB-only data while remaining compatible with standa...*



### 3.1 整体架构

SpaceMind 采用双编码器架构，将视觉语义理解与几何空间感知解耦为两个独立的前馈编码器，并在二者与语言模型之间插入一个轻量级的**相机引导模态融合**（Camera-Guided Modality Fusion, CGMF）模块。给定一段由 $N$ 张图像构成的观测序列 $\mathcal{S} = \{ I_i \}_{i=1}^{N}$，其中每张图像 $I_i \in \mathbb{R}^{\tilde{H} \times W \times 3}$，系统按以下流程处理：

**视觉编码器** $e_v$（InternViT）提取语义视觉标记：

$$f_v = e_v(\{I_i\}_{i=1}^N)$$

其中 $f_v \in \mathbb{R}^{N \times M_v \times d_v}$，$M_v$ 为每帧视觉标记数，$d_v$ 为特征维度。视觉编码器提供丰富的 2D 外观表示。

**空间编码器** $e_s$（VGGT）同步提取几何感知的空间标记与相机标记：

$$f_s, f_c, f_{\mathrm{register}} = e_s(\{I_i\}_{i=1}^N)$$

其中 $f_s \in \mathbb{R}^{N \times M_s \times d_s}$ 为空间标记，$f_c \in \mathbb{R}^{N \times 1 \times d_s}$ 为每帧的相机标记（概括视点信息），$f_{\mathrm{register}}$ 为寄存器标记，后续被丢弃。

**相机引导模态融合**模块 $F$ 将三股特征流融合为保持视觉标记形状的融合特征：

$$f_{\mathrm{fused}} = F(f_v, f_s, f_c)$$

其中 $f_{\mathrm{fused}}$ 与 $f_v$ 形状相同，确保与下游多模态 LLM 的输入接口兼容。

**语言模型** $g$（InternVL3-8B 骨干，基于 Qwen2-7B LLM）在融合特征与文本提示 $T$ 上生成最终回答：

$$R = g(f_{\mathrm{fused}}, T)$$

### 3.2 相机引导模态融合（CGMF）

CGMF 的核心设计理念是将相机标记从被动辅助数据提升为**主动控制模态**，通过三个机制实现视点感知的空间特征注入：相机条件空间偏置、查询无关的空间重要性加权、以及相机条件门控融合。

#### 3.2.1 共享注意力空间投影

首先将视觉、空间和相机特征投影到维度为 $d_a$ 的共享注意力空间：

$$Q = P_Q(\mathrm{LN}(f_v)), \quad K = P_K(\mathrm{LN}(f_s)), \quad V = P_V(\mathrm{LN}(f_s)), \quad C = P_C(f_c)$$

其中 $P_Q, P_K, P_V, P_C$ 为线性投影层，$\mathrm{LN}$ 为层归一化。$Q$ 来自视觉分支，$K, V$ 来自空间分支，$C$ 为投影后的相机嵌入。

#### 3.2.2 相机条件空间偏置

为使空间键值对感知当前视点，将空间标记与相机标记拼接后通过 MLP 生成相机条件偏置：

$$B_g = \operatorname{MLP}([f_s, f_c])$$

该偏置 $B_g$ 用于调制空间键 $K$ 和值 $V$，使空间特征的表达依赖于观测视角。这与现有方法将相机标记简单拼接或隐式混合的做法形成本质区别——相机在此作为**条件信号**而非普通输入。

#### 3.2.3 查询无关的空间重要性加权

空间编码器对不同区域的几何预测置信度不同（如遮挡区域、远距离区域的不确定性更高）。CGMF 通过轻量级 token 权重 MLP（twMLP）预测查询无关的每个空间标记的重要性权重：

$$W_t = \sigma(\operatorname{MLP}(f_s))$$

其中 $\sigma$ 为 sigmoid 函数，$W_t$ 反映各空间标记的几何可靠性。该权重用于重新缩放值向量，使模型自动抑制不可靠的几何信号。

#### 3.2.4 相机条件门控融合（SwiGLU）

相机嵌入 $C$ 经过 SwiGLU 机制生成门控信号：

$$g = \operatorname{Swish}(u) \odot v$$

其中 $u, v$ 为相机嵌入的两个线性投影分支，$\operatorname{Swish}$ 为激活函数，$\odot$ 为逐元素乘法。最终，门控信号 $g$ 调制投影后的融合特征并与原始视觉特征相加：

$$f_{\mathrm{fused}} = P_L(f_{\mathrm{proj}}) \odot g[:,\mathrm{None},:] + f_v$$

其中 $P_L$ 为输出线性投影，$f_{\mathrm{proj}}$ 为经过交叉注意力融合的中间特征。残差连接 $+ f_v$ 保留了视觉编码器的原始语义，门控机制确保空间信息的注入强度由相机条件自适应控制。

### 3.3 设计要点总结

CGMF 的三个组件协同工作，形成了完整的相机引导融合范式：

- **相机条件偏置**使空间键值对视点敏感，解决了视点与场景特征混淆的问题；
- **twMLP 权重**提供查询无关的几何置信度估计，抑制不可靠空间信号；
- **SwiGLU 门控**实现相机条件下的自适应特征混合，避免空间信息过度注入或不足。

消融实验（Table 4）验证了这一设计的有效性：从纯 InternVL3-8B 基线的 63.07 平均准确率开始，逐步添加 VGGT 空间标记（+3.70）、twMLP（+1.83）、geoMLP（+0.40）和 SwiGLU 门控（+0.58），最终达到 69.58，每个组件均带来一致的性能提升。

### 补充图表

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of the CGMF module. CGMF takes visual tokens*



## 实验与关键发现

### 主实验结果

SpaceMind 在三个空间推理基准上均取得了最优性能，且仅使用 RGB 视频输入，无需深度或点云等额外模态。

**VSI-Bench 结果**。VSI-Bench 涵盖 8 个子任务，评估模型的 3D 空间推理能力。SpaceMind 的平均准确率达到 **69.6**，比此前最佳方法 **Spatial-MLLM**（Wu et al., NeurIPS 2025）的 60.9 高出 **+8.7 个百分点**，并在所有子任务上均超越先前模型（Table 1）。该基准测试的强基线还包括 **VLM-3R** 和 **SpaceR** 等具备空间感知能力的 VLM，但 SpaceMind 的相机引导融合机制带来了显著的性能跃升。

**SQA3D 结果**。SQA3D 测试集要求模型基于场景理解回答空间相关问题。SpaceMind 在 EM@1 上达到 **61.1**，在 EM@R1 上达到 **63.8**，在大多数问题类型上均取得最佳表现（Table 2）。值得注意的是，部分基线方法（如 LLAVA-3D、Scene-LLM）使用了深度或点云等额外模态，而 SpaceMind 仅以视频作为输入便超越了这些方法。

**SPBench 结果**。SPBench 包含单图像（SPBench-SI）和多视图（SPBench-MV）两个子集。所有模型均未使用 SPBench 训练数据进行评估，确保比较公平。SpaceMind 在两个子集上均取得最优，整体准确率达到 **67.3**，显著超越通用 VLM 和先前的空间模型（Table 3）。

### 消融实验

为验证各组件贡献，论文在 VSI-Bench 上进行了逐步消融实验（Table 4），以 **InternVL3-8B** 作为基础 VLM 起点：

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/007_Table_4.jpg]]
*Table 4: Ablation Study on VSI-Bench. We analyze the contribution of each component in SpaceMind: (1) adding VGGT spatial tokens via a shallow cross-attention fusion layer, (2) incorporating the token weight MLP (twMLP), and (3) further introducing the geometric MLP (geoMLP). Performance improves consistently as each module is added, and the full SpaceMind architecture achieves the highest accuracy not only on average, but also across all numerical and most multiple-choice subtasks, demonstrating the effectiveness of our model design*

1. **基础 VLM（无空间编码器）**：仅使用 InternVL3-8B 时，平均准确率为 **63.07**。该基线缺乏任何空间几何信息，仅依赖 2D 视觉特征进行空间推理。

2. **+VGGT 空间标记（浅层交叉注意力融合）**：引入 VGGT 空间编码器并通过浅层交叉注意力将空间标记注入视觉流，平均准确率提升至 **66.77**（+3.70）。这验证了显式几何信息对空间推理的基础价值，但相机标记在此阶段仅作为辅助嵌入，未发挥主动引导作用。

3. **+Token 权重 MLP（twMLP）**：引入查询无关的空间标记重要性权重 $W_t = \sigma(\operatorname{MLP}(f_s))$ 后，平均准确率增至 **68.60**（+1.83）。该模块通过预测每个空间标记的几何可靠性来重新缩放值向量，在绝对距离（Abs. Dist.）子任务上获得了 +1.54 的显著提升，说明对不同空间区域进行置信度加权有助于抑制不可靠的几何预测。

4. **+几何 MLP（geoMLP）**：进一步加入相机条件空间偏置 $B_g = \operatorname{MLP}([f_s, f_c])$，平均准确率达到 **69.00**（+0.40）。该模块将相机标记与空间标记拼接后生成调制偏置，使空间键值对的构建依赖于视点信息，在多数子任务上表现最优。

5. **完整 SpaceMind（含 SwiGLU 门控融合）**：加入相机条件门控 $g = \operatorname{Swish}(u) \odot v$ 对融合特征进行调制后，平均准确率达到 **69.58**（+0.58），在绝对距离、相对方向、路径规划等任务上继续提升。该结果验证了相机作为独立控制模态对最终融合质量的关键作用。

消融实验揭示了清晰的因果链：空间几何信息提供基础增益，标记置信度建模抑制噪声，相机条件偏置实现视点感知的键值调制，而相机门控则进一步精细化融合过程。每个组件均带来一致且正向的贡献。

### 跨数据集泛化能力

SpaceMind 在 VSI-Bench、SQA3D 和 SPBench 三个不同分布、不同任务类型的基准上均取得最优，证明了相机引导融合设计的跨数据集泛化能力。特别是在 SPBench 上，所有模型均未使用该基准的训练数据，SpaceMind 仍显著超越其他方法，表明其空间推理能力并非来自对特定数据分布的过拟合，而是源于对相机-场景关系的通用建模。

### 失败模式与局限性

论文未提供具体的失败案例分析或错误模式讨论。但以下潜在局限值得关注：

- **对空间编码器质量的依赖**：CGMF 模块的性能建立在 VGGT 空间编码器输出的几何标记质量之上。若空间编码器在特定场景（如低纹理区域、动态物体）下产生不可靠的几何预测，twMLP 的置信度加权机制能否完全补偿尚待验证。
- **多相机配置的扩展性**：当前设计假设每帧对应一个相机标记 $f_c \in \mathbb{R}^{N \times 1 \times d_s}$，对于多相机同时采集的场景（如自动驾驶多路摄像头），如何聚合或区分不同相机的引导信号需要进一步研究。
- **计算开销**：CGMF 引入了额外的 MLP 和交叉注意力计算，虽然论文称其为“轻量级”，但相对于浅层交叉注意力基线的具体计算增量未量化报告。

*注：以上局限性分析基于方法设计的合理推演，论文原文未提供显式的失败模式讨论，建议查阅完整论文以确认是否存在相关分析。*

### 补充图表

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/001_Figure_1.jpg]]
*Figure 1: Performance on VSI-Bench across different spatial reasoning categories. SpaceMind achieves consistently strong visuospatial intelligence compared to existing systems*

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/004_Table_1.jpg]]
*Table 1: Evaluation on VSI-Bench [68]. SpaceMind sets a new state-of-the-art, achieving the best average score and outperforming all prior models on every individual subtask, often by a large margin*

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/005_Table_2.jpg]]
*Table 2: Evaluation on SQA3D [41] test split. SpaceMind achieves the best performance across most question types and establishes a new state of the art on both EM@1 and EM@R1, despite using video-only inputs while many existing methods rely on richer modalities*

![[assets/figures/papers/paper_list_l2419_https_arxiv_org_abs_2511_23075/figures/006_Table_3.jpg]]
*Table 3: Evaluation on SPBench [34]. All models are evaluated without using SPBench training data. SpaceMind achieves the best performance on both SPBench-SI and SPBench-MV, outperforming general-purpose VLMs and prior spatial models by a clear margin*



## 定位与知识库关联

### 核心问题与现有方法的瓶颈

现有视觉语言模型（VLM）在3D空间推理任务上的根本瓶颈在于**融合机制对“视点”与“场景内容”的混淆**。无论是通用VLM（如LLaVA-NeXT-Video、InternVL3-8B）还是专门的空间推理VLM（如**Spatial-MLLM**，Wu et al., NeurIPS 2025；**VLM-3R**；**SpaceR**），其多模态融合策略均将相机（视点）特征和场景（几何/外观）特征统一处理——或通过浅层交叉注意力拼接，或通过简单的MLP投影混合。这种设计隐含地假设相机信息只是场景描述的被动元数据，而非一个具有独立调控能力的主动信号源。

其直接后果是：模型无法根据视点变化动态调整对空间信息的依赖程度。当相机位姿发生显著变化时，某些空间标记的几何预测可能变得不可靠（例如深度估计在远距离或遮挡区域失效），但现有方法缺乏机制来显式评估并抑制这些低质量空间信号。**Spatial-MLLM**虽引入了几何编码器，但其融合层并未区分相机标记与空间标记的角色差异；**VLM-3R**和**SpaceR**则完全未引入专用几何编码器，依赖训练策略隐式学习空间关系，缺乏对3D几何的显式建模。

### SpaceMind的方法定位

SpaceMind的核心贡献在于**将相机表示从被动元数据提升为独立的主动引导模态**，并围绕这一理念设计了相机引导模态融合（Camera-Guided Modality Fusion, CGMF）模块。该方法在以下三个维度上区别于既有工作：

1. **相机作为控制信号而非辅助输入**：在**Spatial-MLLM**和**VLM-3R**中，相机标记被拼接到空间/视觉标记后统一送入融合层，其作用与场景标记无本质区别。SpaceMind则通过三个机制使相机显式地引导融合过程：（a）相机条件空间偏置——将相机标记与空间标记拼接后通过MLP生成偏置项$B_g$，直接调制空间键值对（Eq. 8-10）；（b）相机条件门控——通过SwiGLU机制生成门控信号$g$，逐元素调制融合后的特征（Eq. 20-21）；（c）相机嵌入参与注意力记忆，影响跨模态注意力的计算。

2. **查询无关的空间置信度建模**：现有方法未对空间标记的可靠性进行显式估计。SpaceMind引入轻量级token权重MLP（twMLP），仅从空间分支预测每个空间标记的重要性权重$W_t = \sigma(\mathrm{MLP}(f_s))$，并通过sigmoid输出（Eq. 11）。该权重反映几何预测的置信度（例如深度、法线估计的不确定性），用于重新缩放值向量，使模型自动抑制不可靠的空间信号。这一设计与相机引导形成互补：相机条件偏置提供“视点相关性”，而$W_t$提供“几何可靠性”。

3. **与基础VLM的解耦设计**：SpaceMind冻结视觉编码器（InternViT）和空间编码器（VGGT），仅训练CGMF模块并对LLM主干应用LoRA（秩256）。这种设计保证了：（a）不破坏预训练视觉和几何知识；（b）CGMF模块可作为即插即用组件嵌入其他VLM架构；（c）训练高效，仅需RGB视频输入即可超越依赖深度或点云等额外模态的方法（如LLAVA-3D、Scene-LLM）。

### 知识库中的位置与适用边界

SpaceMind处于**3D空间推理VLM**与**多模态融合机制设计**的交叉点。其上游依赖包括：视觉编码器（InternViT，源自InternVL3系列）、空间编码器（VGGT，一种前馈几何预测网络）、以及LLM骨干（InternVL3-8B，基于Qwen2-7B）。下游可对接任何需要空间推理能力的VLM应用，如具身导航、AR/VR场景理解、3D问答等。

**适用边界**：
- **输入模态限制**：SpaceMind设计为RGB视频输入，不依赖深度、点云或相机参数等额外模态。这既是优势（降低数据获取成本），也是限制——在需要精确度量重建的场景（如工业测量）中，显式3D信息可能仍是必要的。
- **空间编码器依赖**：CGMF的有效性依赖于空间编码器（VGGT）提供的几何标记和相机标记质量。若替换为较弱的几何预测网络，相机引导融合的增益可能衰减。消融实验（Table 4）已显示，移除VGGT空间标记（回退至纯InternVL3-8B）导致VSI-Bench平均准确率从66.77降至63.07，降幅达3.7个百分点。
- **相机标记的语义粒度**：当前设计使用每帧一个相机标记$f_c \in \mathbb{R}^{N \times 1 \times d_s}$概括视点信息。对于需要帧间细粒度视点变化建模的任务（如快速旋转下的动态空间关系推理），该表示可能不足以捕捉瞬时视点差异。
- **跨域泛化**：论文在VSI-Bench、SQA3D和SPBench上验证了有效性，但这些基准主要覆盖室内场景和静态空间关系。在室外大规模场景或动态物体交互场景下的表现尚需进一步验证。

### 局限与开放问题

论文未明确列出局限性，但基于方法设计可识别以下潜在问题：

1. **相机引导融合的计算开销**：CGMF模块包含相机条件偏置MLP、token权重MLP、几何MLP和SwiGLU门控等多个子组件。虽然论文强调其“轻量级”，但未提供与浅层交叉注意力基线的参数量和推理延迟对比，实际部署效率需手动验证。

2. **空间标记的冗余处理**：空间编码器输出的寄存器标记$f_{\mathrm{register}}$被直接丢弃（Section 3.1 Eq. 2）。这些标记可能包含全局场景上下文信息，其丢弃策略是否损失有用信号未经验证。

3. **相机标记的获取方式**：VGGT从RGB图像中隐式推断相机标记，而非使用真实相机参数。这种隐式推断的准确性在极端视点（如大角度旋转、低纹理区域）下的退化程度未经过系统评估，可能成为CGMF引导信号质量的瓶颈。

4. **多帧一致性的显式建模缺失**：CGMF在每帧内独立进行相机引导融合，帧间关系仅通过LLM的自注意力隐式建模。对于需要跨帧几何一致性推理的任务（如物体追踪、3D重建），显式的时序融合机制可能带来额外增益。

5. **与更强基线的对比缺失**：论文以InternVL3-8B作为基础VLM，但未与同期更强的通用VLM（如GPT-4V、Gemini Pro Vision）在空间推理任务上进行对比。SpaceMind的增益是否在更强的基础模型上仍能保持，需要手动验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/SpaceMind_Camera_Guided_Modality_Fusion_for_Spatial_Reasoning_in_Vision_Language_Models.pdf]]

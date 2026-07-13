---
title: "Superman: Unifying Skeleton and Vision for Human Motion Perception and Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Superman_Unifying_Skeleton_and_Vision_for_Human_Motion_Perception_and_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Superman_Unifying_Skeleton_and_Vision_for_Human_Motion_Perception_and_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- Superman
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 视觉引导的运动标记器（Vision-Guided Motion Tokenizer）及其混合码本（Hybrid Codebook），每个标记是包含成对视觉原型和几何原型的双模态实体，确保量化过程同时由视频外观特征和3D骨架几何结构引导。
primary_logic: 将人体运动视为一种通用语言，通过跨模态运动词汇（视觉+骨架）和单一MLLM架构，将3D姿态估计、运动预测和运动中间帧生成等多任务重新定义为条件序列生成问题，实现感知与生成的统一。
claims:
- "Superman在Human3.6M上的3D姿态估计相比最先进的多任务感知方法HiC 有11.97%的改进。"
- Superman (with MAFT)在Human3.6M上取得了39.41（N-MPJPE）和51.61（MPJPE）的性能，优于所有传统多任务和LLM/MLLM基线。
- 统一的联合训练在姿态估计（PE）、运动预测（MP）和运动中间帧生成（MIB）三个任务上均优于独立训练的特化模型。
- 平衡的视觉-骨架融合权重（β_s=0.5, β_v=0.5）在标记器重建误差和下游PE任务上取得最佳效果。
---

# Superman: Unifying Skeleton and Vision for Human Motion Perception and Generation

> [!tip] 核心洞察
> 将人体运动视为一种通用语言，通过跨模态运动词汇（视觉+骨架）和单一MLLM架构，将3D姿态估计、运动预测和运动中间帧生成等多任务重新定义为条件序列生成问题，实现感知与生成的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | Superman：统一的骨架与视觉人体运动感知与生成 |
| 英文题名 | Superman: Unifying Skeleton and Vision for Human Motion Perception and Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Superman_Unifying_Skeleton_and_Vision_for_Human_Motion_Perception_and_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Superman |
| Dataset | Human3.6M |

> [!tip] 效果简介
> - Human3.6M 上，PE N-MPJPE (mm) 39.41 (Superman w/ MAFT) vs 44.77 (HiC) (-5.36)；PE MPJPE (mm) 51.61 (Superman w/ MAFT) vs 53.86 (HiC) (-2.25)；MP Avg MPJPE (mm) 26.13 vs 26.66 (HiC) (-0.53)。

## 概要

### 问题背景与瓶颈

人体运动分析领域长期面临严重的**碎片化**困境。一方面，以 **MotionBERT**（Zhu et al., ICCV 2023）、**Skeleton-in-Context (SiC)**（Wang et al., CVPR 2024）、**Human-in-Context (HiC)**（Liu et al., ArXiv 2025）为代表的传统多任务感知模型能够从视频理解运动，但仅输出文本或数值结果，不具备生成能力。另一方面，以 **MotionGPT**（Jiang et al., NeurIPS 2023）、**MotionGPT3**（Zhu et al., ICLR 2026）为代表的生成式 LLM 模型能够生成运动序列，却无法处理原始视觉输入。而现有的 MLLM 方法如 **PoseLLaVA**（Feng et al., AAAI 2025）、**UniPose**（Li et al., CVPR 2025）虽能结合视觉与语言，却局限于单帧静态姿态，缺乏时序运动建模能力。更深层的问题是，现有运动词汇表——如 MotionGPT 所使用的——仅由骨架数据构建，**割裂了视觉域与几何域的连接**，使得感知与生成无法在统一的表征空间内完成。

### 核心方法

Superman 的核心思想是将人体运动视为一种**通用语言**，通过构建跨模态运动词汇和单一 MLLM 架构，将 3D 姿态估计、运动预测和运动中间帧生成等多任务重新定义为**条件序列生成问题**，实现感知与生成的统一。

其关键创新在于**视觉引导的运动标记器（Vision-Guided Motion Tokenizer, VGMT）**及配套的**混合码本（Hybrid Codebook）**。与仅使用骨架特征的现有方案不同，VGMT 通过骨架编码器（Skeleton Encoder）捕捉时空运动学结构，同时利用视觉-骨架注意力模块（Visual-Skeleton Attention, VSA）从视频帧中聚合关节相关的视觉外观特征。量化过程联合最小化视觉特征与骨架特征到混合原型（成对的视觉原型和几何原型）的欧氏距离，确保每个离散标记同时携带视觉外观和 3D 几何的双模态信息。这一设计从根本上解决了视觉域与运动域割裂的问题。

在解码端，Superman 以 **Qwen2.5-VL-7B** 作为核心序列处理器，自回归地预测运动标记序列。可选的**运动感知微调模块（Motion-Aware Fine-Tuning, MAFT）**以不足 0.2% 的额外参数，通过视觉-骨架交叉注意力增强 MLLM 的视觉标记，显著提升依赖视觉输入的任务性能。

### 主要结果

Superman 在 Human3.6M 基准上取得了全面领先的性能：

- **3D 姿态估计**：Superman（含 MAFT）达到 **39.41 mm**（N-MPJPE）和 **51.61 mm**（MPJPE），相比当前最强的多任务感知方法 HiC 分别降低 5.36 mm 和 2.25 mm，相对改进达 11.97%。
- **运动预测**：平均 MPJPE 为 **26.13 mm**，优于 HiC 的 26.66 mm。
- **运动中间帧生成**：平均 MPJPE 为 **30.61 mm**，优于 HiC 的 31.13 mm。

消融实验进一步揭示了方法的关键机制：**平衡的视觉-骨架融合权重**（β_s=0.5, β_v=0.5）在标记器重建误差和下游姿态估计任务上均取得最优；**统一多任务联合训练**在姿态估计、运动预测和中间帧生成三个任务上全面优于各自独立训练的特化模型，验证了统一框架的正向迁移效应；模型容量（3B→7B）和码本规模的增长可一致降低各项误差，展现出良好的扩展性。

### 方法定位

Superman 在方法谱系中占据独特位置：它既不同于仅做感知或仅做生成的传统模型，也超越了仅处理单帧的 MLLM 方案。通过视觉引导的跨模态运动标记器和统一的条件序列生成框架，Superman 首次将视频感知、骨架建模和运动生成纳入同一 MLLM 架构，为人体运动分析提供了一个端到端、多任务统一的范式。

### 领域碎片化：感知与生成的割裂

人体运动分析是计算机视觉与图形学的核心课题，涵盖3D姿态估计、运动预测、运动中间帧生成等关键任务。然而，当前该领域存在严重的**架构碎片化**：感知模型（如**MotionBERT**，Zhu et al., ICCV 2023）擅长从视频理解运动，但仅输出文本或数值结果，不具备生成能力；生成模型（如**MotionGPT**，Jiang et al., NeurIPS 2023）能够合成逼真的运动序列，却无法处理原始视觉输入。这种“理解”与“创造”的分离，使得构建一个既能感知又能生成人体运动的统一系统成为长期未解的挑战。

### 生成式多模态大模型的局限

近年来，多模态大语言模型（MLLM）在图像理解与生成任务上取得了突破性进展。然而，当它们被应用于人体姿态领域时，几乎全部局限于**单帧静态姿态**的处理。例如，**PoseLLaVA**（Feng et al., AAAI 2025）和**UniPose**（Li et al., CVPR 2025）虽能进行姿态理解或生成，但缺乏对时序运动动态的建模能力。这些模型无法捕捉运动序列中蕴含的时空依赖关系，因而无法胜任运动预测或中间帧生成等核心时序任务。

### 运动词汇表的模态鸿沟

将运动序列转化为离散标记（token）是使LLM能够处理运动数据的关键技术路径。然而，现有运动词汇表——如**MotionGPT**和**MotionGPT3**（Zhu et al., ICLR 2026）所采用的——**仅由骨架数据构建**。这种“骨架唯一”的词汇表从根本上割裂了运动与视觉域的连接：当模型需要从视频中感知运动时，缺乏视觉引导的标记器无法有效对齐外观特征与几何结构，导致信息在量化过程中大量丢失。这一模态鸿沟成为统一感知与生成的核心瓶颈。

### Superman的动机与核心思路

针对上述问题，Superman提出了一项根本性的范式转变：**将人体运动视为一种通用语言**。其核心洞察在于，3D姿态估计、运动预测和运动中间帧生成等看似迥异的任务，本质上都可以重新定义为**条件序列生成问题**——给定视觉输入（视频）或运动历史，自回归地预测运动标记序列。

为实现这一统一，Superman设计了两个关键创新：

1. **视觉引导的运动标记器（Vision-Guided Motion Tokenizer, VGMT）**：通过构建包含成对视觉原型与几何原型的混合码本（Hybrid Codebook），确保运动量化过程同时由视频外观特征和3D骨架几何结构联合引导，弥合模态鸿沟。
2. **单一MLLM统一架构**：以Qwen2.5-VL-7B为核心解码器，整合文本、视频和3D骨架三种模态信息，将多任务统一为条件序列生成，实现感知与生成的真正融合。

这一设计使得Superman在Human3.6M基准上的3D姿态估计相比当前最先进的多任务感知方法**HiC**（Liu et al., ArXiv 2025）取得了11.97%的显著改进，同时在运动预测和中间帧生成任务上保持了领先水平，首次证明了单一模型在人体运动感知与生成全任务上达到最优性能的可行性。

## 核心方法与创新机理

Superman 的核心创新在于通过**视觉引导的运动标记器（Vision-Guided Motion Tokenizer, VGMT）** 及其**混合码本（Hybrid Codebook）**，将人体运动建模从“骨架孤岛”拉回到“视觉-骨架联合空间”，并以此为基础，用一个单一的 MLLM 架构统一了感知与生成任务。

### 创新一：从“仅骨架”到“视觉引导”的运动词汇构建

现有基于 LLM 的运动生成模型（如 **MotionGPT** (Jiang et al., NeurIPS 2023)、**MotionGPT3** (Zhu et al., ICLR 2026)）的运动标记器仅依赖骨架数据构建码本，割裂了运动与视觉域的联系。Superman 的 VGMT 通过**视觉-骨架注意力（Visual-Skeleton Attention, VSA）** 模块，从视频帧特征图中采样并聚合与关节相关的视觉外观特征，与骨架编码器捕获的几何特征进行融合。量化过程不再是对单一模态特征的最近邻搜索，而是**联合最小化视觉和骨架特征与混合原型之间的欧氏距离**：

$$k_{w} = \arg\min_{k} \left( \|\mathbf{z}_{w}^{v} - \mathbf{c}_{k}^{v}\|_{2}^{2} + \|\mathbf{z}_{w}^{s} - \mathbf{c}_{k}^{s}\|_{2}^{2} \right)$$

混合码本中的每个标记是一个包含**成对视觉原型和几何原型**的双模态实体。消融实验（Table 6）证实，平衡的视觉-骨架融合权重（$\beta_s=0.5, \beta_v=0.5$）在标记器重建误差（4.7 mm）和下游姿态估计性能上均达到最优，显著优于仅视觉或仅骨架的标记器配置。

### 创新二：从“感知与生成分离”到“单一 MLLM 统一”

传统范式将感知模型（如 **MotionBERT** (Zhu et al., ICCV 2023)、**Skeleton-in-Context** (Wang et al., CVPR 2024)、**Human-in-Context** (Liu et al., ArXiv 2025)）与生成模型（如 MotionGPT 系列）割裂开来；现有的生成式 MLLM（如 **PoseLLaVA** (Feng et al., AAAI 2025)、**UniPose** (Li et al., CVPR 2025)）也仅局限于单帧静态姿态。Superman 将所有任务——3D 姿态估计、运动预测、运动中间帧生成——重新定义为**条件序列生成问题**，由单一 MLLM（Qwen2.5-VL-7B）自回归地预测运动标记序列。统一联合训练在三个任务上均优于各自独立训练的特化模型（Table 7），证明了共享运动语言的有效性。

### 创新三：轻量运动感知微调模块（MAFT）

为增强 MLLM 对运动视频的理解，Superman 引入可选的 **Motion-Aware Fine-Tuning (MAFT)** 模块。该模块通过视觉-骨架交叉注意力，将骨骼几何信息注入 MLLM 的视觉标记：

$$\hat{\mathbf{Z}}_{\mathrm{grid}} = \mathbf{VSA}(\mathbf{Z}_{\mathrm{grid}}, \mathbf{Z}_{\mathrm{pose}})$$

MAFT 仅增加不到 0.2% 的额外参数，却带来显著的感知性能提升——在 Human3.6M 上，Superman with MAFT 的 N-MPJPE 达到 39.41 mm，相比当前最优的多任务感知方法 HiC 降低 5.36 mm（11.97% 相对改进），验证了视觉-骨架跨模态融合在感知任务中的关键作用。

Superman 将人体运动感知与生成统一为一个**条件序列生成**问题，其核心 pipeline 由两个解耦的阶段构成：首先通过视觉引导的运动标记器（Vision-Guided Motion Tokenizer, VGMT）将连续的高维运动数据压缩为离散的语义标记序列，随后由单一的多模态大语言模型（MLLM）以自回归方式预测这些运动标记，从而同时完成 3D 姿态估计、运动预测和运动中间帧生成三项任务。

### 两阶段流水线

**第一阶段：运动离散化。** VGMT 接收一个包含 $F$ 帧的骨架序列 $\mathbf{X} \in \mathbb{R}^{F \times J \times 3}$ 以及对应的视频帧，将其转换为长度为 $T$ 的整数标记序列 $\mathbf{K}_{1:T}$。该标记器的权重在训练完成后被冻结，为下游 MLLM 提供稳定的运动“词汇表”。

**第二阶段：统一序列建模。** 以冻结的 VGMT 为基础，Superman 微调一个仅解码器的 MLLM（**Qwen2.5-VL-7B**），使其学会根据不同的条件输入自回归地预测运动标记序列。具体而言：
- 对于**姿态估计**，MLLM 以视频帧的视觉特征为条件，生成完整的运动标记序列，再通过 VGMT 解码器重建 3D 姿态；
- 对于**运动预测**，MLLM 以历史运动标记为条件，生成未来的运动标记；
- 对于**运动中间帧生成**，MLLM 以首尾帧的运动标记为条件，生成中间过渡的运动标记。

### 模块关系与数据流

整个框架的模块关系与数据流如 Figure 3 所示，可概括为以下通路：

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Superman_Unifying/figures/004_Figure_3.jpg]]
*Figure 3: Network architecture and training paradigm. Superman fine-tune a single LLM to integrate information from text, video, and 3D skeleton modalities. Optionally, a Motion-Aware Fine-Tuning (MAFT) module can be integrated. With \<0.2% extra parameters, MAFT enhances motion perception by enabling cross-video-motion fusion, leading to substantial improvement on tasks with visual input, as validated by the experiment results*

1. **视觉编码通路**：输入视频帧经过视觉编码器提取网格特征 $\mathbf{Z}_{\mathrm{grid}}$，同时由固定的 2D 姿态估计器提供 2D 关节投影，用于 VGMT 中的视觉-骨架注意力（VSA）模块。
2. **运动标记化通路**：VGMT 内部的骨架编码器 $E_s$ 提取 3D 骨架的时空几何特征，VSA 模块从视觉特征图中采样并聚合关节相关的视觉特征，二者融合后经混合码本量化为离散运动标记。
3. **MLLM 推理通路**：量化后的运动标记与视觉网格特征一同送入 MLLM。可选的运动感知微调模块（MAFT）通过视觉-骨架交叉注意力将骨架几何信息注入视觉标记，生成增强的视觉标记 $\hat{\mathbf{Z}}_{\mathrm{grid}}$。MLLM 据此自回归地预测目标运动标记序列。
4. **运动解码通路**：预测的标记序列通过 VGMT 解码器恢复为 3D 骨架坐标，完成从离散标记到连续运动的映射。

### 关键设计：MAFT 模块

MAFT 作为可选插件嵌入 MLLM 的视觉处理流程中，参数量不足整体模型的 0.2%。其核心操作如公式所示：

$$\hat{\mathbf{Z}}_{\mathrm{grid}} = \mathbf{VSA}(\mathbf{Z}_{\mathrm{grid}}, \mathbf{Z}_{\mathrm{pose}})$$

其中 $\mathbf{Z}_{\mathrm{pose}}$ 为从输入骨架提取的姿态特征。该模块通过视觉-骨架注意力实现跨模态特征融合，显著提升了对视觉输入依赖较强的任务（如姿态估计）的性能，而对纯骨架驱动的任务（如运动预测）影响甚微。

Superman 的核心由两个阶段构成：**视觉引导运动标记器（Vision-Guided Motion Tokenizer, VGMT）** 将连续运动序列离散化为语义标记，**多模态大语言模型（MLLM）** 以自回归方式预测这些标记来统一执行多项运动任务。

### 视觉引导运动标记器（VGMT）

VGMT 的设计目标是构建一个跨模态的运动词汇表，使每个离散标记同时编码视觉外观和 3D 骨架几何信息。其架构由以下子模块串联而成：

1. **骨架编码器（Skeleton Encoder, $E_s$）**：接收输入姿态序列，通过时空建模捕捉运动学结构，输出骨架特征 $\mathbf{z}_w^s$。

2. **视觉-骨架注意力模块（Visual-Skeleton Attention, VSA）**：将骨架查询特征与视频帧特征图进行交叉注意力，从 2D 投影位置采样并聚合关节相关的视觉特征，增强对遮挡的鲁棒性。对于帧 $f$ 中的关节 $j$，其视觉特征输出为：
   $$
   \mathbf{v}_{j,f} = \mathrm{VSA}(\mathbf{q}_{j,f}, \mathcal{F}_{f}, \mathbf{p}_{j,f})
   $$
   其中 $\mathbf{q}_{j,f}$ 为骨架编码器产生的查询特征，$\mathcal{F}_{f}$ 为帧 $f$ 的特征图，$\mathbf{p}_{j,f}$ 为关节在该帧的 2D 投影位置。

3. **视觉编码器（Visual Encoder, $E_v$）**：进一步处理 VSA 输出的视觉特征，生成视觉特征 $\mathbf{z}_w^v$。

4. **混合码本（Hybrid Codebook）**：码本中的每个条目是一对成型的视觉原型 $\mathbf{c}_k^v$ 和几何原型 $\mathbf{c}_k^s$。对于时间窗口 $w$，量化索引通过联合最小化视觉和骨架特征与原型之间的欧氏距离确定：
   $$
   k_{w} = \arg\min_{k} \left( \|\mathbf{z}_{w}^{v} - \mathbf{c}_{k}^{v}\|_{2}^{2} + \|\mathbf{z}_{w}^{s} - \mathbf{c}_{k}^{s}\|_{2}^{2} \right)
   $$
   这一双模态约束确保量化过程同时由视频外观和 3D 骨架几何引导，而非仅依赖单一模态。

5. **解码器**：根据量化后的混合原型重建 3D 姿态序列。

VQ-VAE 的训练目标包含重建误差和双重承诺损失：
$$
\mathcal{L}_{\mathrm{VQ}} = \|\mathbf{X}_{w} - \hat{\mathbf{X}}_{w}\|_{2}^{2} + \beta_{s} \|\mathrm{sg}[\mathbf{z}_{w}^{s}] - \hat{\mathbf{c}}_{w}^{s}\|_{2}^{2} + \beta_{v} \|\mathrm{sg}[\mathbf{z}_{w}^{v}] - \hat{\mathbf{c}}_{w}^{v}\|_{2}^{2}
$$
其中 $\mathrm{sg}[\cdot]$ 表示停止梯度算子，$\beta_s$ 和 $\beta_v$ 分别控制骨架和视觉承诺损失的权重。消融实验表明，平衡的融合权重（$\beta_s=0.5, \beta_v=0.5$）在标记器重建误差和下游姿态估计任务上均取得最优效果。

### 运动感知微调模块（MAFT）

MAFT 是一个轻量级模块（额外参数 <0.2%），插入在 MLLM 的视觉编码器与语言解码器之间。其作用是通过视觉-骨架交叉注意力，将 3D 姿态特征注入到 MLLM 的网格视觉标记中，增强视频特征的运动感知能力：
$$
\hat{\mathbf{Z}}_{\mathrm{grid}} = \mathbf{VSA}(\mathbf{Z}_{\mathrm{grid}}, \mathbf{Z}_{\mathrm{pose}})
$$
其中 $\mathbf{Z}_{\mathrm{grid}}$ 为 MLLM 视觉编码器输出的网格特征，$\mathbf{Z}_{\mathrm{pose}}$ 为姿态编码器产生的 3D 骨架特征。增强后的视觉标记 $\hat{\mathbf{Z}}_{\mathrm{grid}}$ 随后送入语言解码器进行自回归生成。

### 统一任务的条件序列生成

MLLM（基于 Qwen2.5-VL-7B）将所有任务重新定义为条件序列生成问题。不同任务对应不同的条件输入：

- **姿态估计**：给定视频视觉特征，自回归生成运动标记序列：
  $$
  \mathcal{L}_{\mathrm{est}} = \sum_{t=1}^{T} \log P(k_{t} | \mathbf{K}_{<t}, \hat{\mathbf{Z}}_{\mathrm{grid}})
  $$

- **运动预测**：给定历史运动标记序列，预测未来标记：
  $$
  \mathcal{L}_{\mathrm{pred}} = \sum_{t=T'+1}^{T} \log P(k_{t} | \mathbf{K}_{<t})
  $$

- **运动中间帧生成**：给定首尾帧标记，生成中间帧的标记序列。

这种统一范式使单一模型能够同时处理感知（从视觉到骨架）和生成（从骨架到骨架）任务，并在联合训练中实现跨任务的知识共享。

## 实验与关键发现

### 主实验：Human3.6M 基准上的综合性能

Superman 在 Human3.6M 数据集上统一评估了三维姿态估计（PE）、运动预测（MP）和运动中间帧生成（MIB）三项任务，与传统的多任务模型和基于 LLM/MLLM 的方法进行了全面对比。如 Table 2 所示，配备 MAFT 模块的 Superman 在姿态估计任务上取得了 39.41 mm 的 N-MPJPE 和 51.61 mm 的 MPJPE，显著优于此前最优的传统多任务模型 **HiC**（Liu et al., ArXiv 2025）的 44.77 mm 和 53.86 mm，相对改进幅度达 11.97%。在运动预测和运动中间帧生成任务上，Superman 同样取得了最优或极具竞争力的结果：平均 MPJPE 分别为 26.13 mm 和 30.61 mm，均低于 HiC 的 26.66 mm 和 31.13 mm。

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Superman_Unifying/figures/005_Table_2.jpg]]
*Table 2: Comparison of our model with traditional multi-task models and LLM / MLLM-based models on three human motion tasks: pose estimation (PE), motion prediction (MP), and motion in-betweening (MIB) on Human3.6M [13]. All tasks are evaluated using Mean Per Joint Position Error (MPJPE) in millimeter, averaged over all test data, where lower is better. “T ” means how many frames the model inputs and outputs*

值得注意的是，Superman（不含 MAFT）在姿态估计上的 N-MPJPE 为 44.90 mm，已优于所有基于 LLM/MLLM 的基线方法，如 **MotionGPT3**（Zhu et al., ICLR 2026）和 **UniPose**（Li et al., CVPR 2025），验证了统一框架本身的强大能力。Table 3 进一步给出了各动作类别的细粒度 N-MPJPE 对比，Superman 在 SitDown（47.12 mm）、Smoke（48.97 mm）、Photo（41.31 mm）等挑战性动作上均展现出明显优势，表明视觉引导标记器对复杂姿态的感知能力更强。

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Superman_Unifying/figures/006_Table_3.jpg]]
*Table 3: Action-specific N-MPJPEs for pose estimation on Human3.6M [13]*

**Figure 5** 的定性结果直观展示了 Superman 与 HiC 在姿态估计上的差异：在存在自遮挡和深度歧义的场景中，Superman 恢复的三维姿态与真值更为吻合，尤其在四肢末端的深度估计上表现出更高的精度。

### 泛化能力：3DPW 未见数据集

为验证模型的跨域泛化能力，所有模型仅在 Human3.6M 上训练，直接在 3DPW 数据集上进行测试。如 Table 4 所示，Superman 在运动预测和运动中间帧生成两项任务上均显著优于所有基线模型，且优势幅度大于在 Human3.6M 上的表现。这一结果表明，视觉引导的混合码本所学习到的运动表示具有良好的场景迁移能力，而非过拟合于受控室内环境。**Figure 6** 的定性对比进一步证实了这一点：在 3DPW 的野外场景中，Superman 预测的未来运动序列保持了更自然的运动学结构，而基线方法 SiC（Wang et al., CVPR 2024）则出现了明显的关节漂移。

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Superman_Unifying/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative results for generalizing to motion prediction on 3DPW (unseen dataset). Our method is compared with SiC [19], the current SoTA on the task*

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Superman_Unifying/figures/008_Table_4.jpg]]
*Table 4: Comparison of results on generalization to unseen data. Motion prediction (MP) and motion in-betweening (MIB) on 3DPW [27] are reported. All models are trained on Human3.6M only, with 3DPW completely excluded from training*

### 消融实验：关键设计的因果验证

**标记器组件与融合权重的消融。** Table 6 系统性地验证了视觉引导标记器（VGMT）中各组件的贡献。当仅使用骨架特征（Skeleton-Only）或仅使用视觉特征（Vision-Only）构建码本时，标记器的重建误差分别上升至 5.8 mm 和 6.2 mm，而视觉-骨架融合（$\beta_s = 0.5, \beta_v = 0.5$）实现了最低的 4.7 mm 重建误差。这一优势直接传导至下游任务：融合设置下的姿态估计 N-MPJPE 为 44.9 mm，显著优于仅骨架（47.8 mm）和仅视觉（49.3 mm）方案。融合权重的对称设置（各 0.5）被证明是最优的，偏离该平衡点（如 $\beta_s = 0.8, \beta_v = 0.2$）会导致性能下降，说明视觉外观和骨架几何信息对运动标记的构建具有同等重要的互补作用。

**统一多任务训练 vs. 特化训练。** Table 7 的消融实验揭示了一个核心发现：统一的联合训练模型在三个任务上均优于各自独立训练的特化模型。具体而言，统一模型的 PE N-MPJPE 为 44.9 mm，优于特化 PE 模型的 46.5 mm；MP 平均 MPJPE 为 26.1 mm，优于特化 MP 模型的 27.3 mm；MIB 平均 MPJPE 为 30.6 mm，优于特化 MIB 模型的 33.1 mm。这一反直觉的结果表明，多任务联合训练不仅没有造成任务间干扰，反而通过共享运动语言知识实现了正向迁移，验证了将人体运动视为通用语言这一核心洞察的合理性。

**MAFT 模块的效率与效能。** Table 5 显示，MAFT 模块仅引入不到 0.2% 的额外参数，却带来了显著的性能增益：在姿态估计任务上，N-MPJPE 从 44.90 mm 降至 39.41 mm（降幅 12.2%）。这一轻量级设计通过视觉-骨架交叉注意力增强 MLLM 的视觉标记，以极小的计算代价实现了运动感知能力的实质性提升。

### 扩展性分析

**Figure 4** 展示了模型容量和码本规模的扩展性。将基础 MLLM 从 3B 扩展至 7B，姿态估计和运动预测的 MPJPE 均呈一致下降趋势；将码本大小从 4096×1024 扩展至 4096×2048 同样带来性能增益。这一趋势表明，Superman 框架能够有效利用更大的模型容量和更丰富的离散表示空间，具有良好的扩展潜力。

### 码本利用率与表示质量

**Figure 7** 对 VQ-VAE 码本的使用效率进行了定量分析。推理阶段最多有 65.4% 的码本编码保持活跃，表明离散潜在空间得到了有效利用，未出现严重的码本坍缩问题。同时，绝大多数编码对之间的余弦相似度接近 0，证明混合码本学习到了高度去相关的离散表示，为下游 MLLM 提供了信息丰富的运动词汇基础。

### 失败模式与局限性

尽管 Superman 在受控基准上表现优异，论文未明确讨论模型的失败案例。基于其设计特点，可推断以下潜在退化场景：（1）依赖预先计算的二维关节投影和固定的二维姿态估计器，在极端遮挡或非典型视角下，二维输入的噪声会通过 VSA 模块传播至三维估计；（2）训练数据局限于 Human3.6M 等受控室内数据集，对复杂野外场景中多人交互、动态背景等情况的泛化能力缺乏系统验证；（3）MLLM 的自回归推理范式在长序列生成时可能面临误差累积问题，但论文未对此进行分析。这些局限性需要在后续研究中通过更大规模的多样化数据和鲁棒性测试加以验证。

![[assets/figures/papers/paper_list_l25_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Superman_Unifying/figures/012_Table_6.jpg]]
*Table 6: Ablation on tokenizer components and fusion weights*

## 定位与知识库关联

### 1. 与现有工作的关系定位

Superman 的核心贡献在于弥合了当前人体运动分析领域的两大碎片化断层：**感知模型与生成模型的分离**，以及**基于骨架的运动词汇与视觉域的割裂**。为明确这一贡献，需将 Superman 置于三条主要研究脉络中进行比较。

#### 1.1 与传统多任务运动感知模型的对比

传统多任务模型致力于在统一架构下处理姿态估计、运动预测等多种运动分析任务，但其输出通常局限于数值化的骨架坐标，不具备生成能力。代表性工作包括：

- **MotionBERT** (Zhu et al., ICCV 2023)：通过双向Transformer编码器在2D/3D姿态估计、运动预测等任务上实现多任务学习，但其架构本质上是判别式的，无法生成运动序列。
- **Skeleton-in-Context (SiC)** (Wang et al., CVPR 2024)：将骨架序列建模为上下文学习问题，提升了运动预测的性能，但同样局限于骨架域内的感知任务。
- **Human-in-Context (HiC)** (Liu et al., ArXiv 2025)：作为当前最先进的多任务跨域运动建模方法，HiC 尝试融合视频和骨架信息，在 Table 2 中以 44.77 N-MPJPE 的姿态估计性能成为最强传统基线。

Superman 与上述工作的根本差异在于**架构范式**：传统模型采用分别的感知和生成模型设计，而 Superman 以单一 MLLM 统一处理所有任务，将 3D 姿态估计、运动预测和运动中间帧生成重新定义为**条件序列生成问题**。在 Human3.6M 上，Superman (w/ MAFT) 以 39.41 N-MPJPE 的姿态估计性能相比 HiC 实现了 11.97% 的改进（Table 2），同时在运动预测（26.13 vs. 26.66 Avg MPJPE）和运动中间帧生成（30.61 vs. 31.13 Avg MPJPE）任务上也全面超越。

#### 1.2 与基于 LLM/MLLM 的运动生成模型的对比

近年来，将大语言模型应用于人体运动生成成为一个新兴方向，但这些工作普遍存在两个局限：**仅依赖骨架数据构建运动词汇**，以及**局限于运动生成而无法处理原始视觉输入**。代表性工作包括：

- **MotionGPT** (Jiang et al., NeurIPS 2023)：首次将运动视为语言，通过 VQ-VAE 将骨架序列量化为离散标记，再由 LLM 进行生成，但其运动词汇仅由骨架数据构建。
- **MotionGPT3** (Zhu et al., ICLR 2026)：在 MotionGPT 基础上扩展，但同样仅使用骨架模态。
- **PoseLLaVA** (Feng et al., AAAI 2025) 和 **UniPose** (Li et al., CVPR 2025)：基于 MLLM 的姿态理解与生成模型，但均局限于**单帧静态姿态**，缺乏对时序运动的建模能力。
- **LocLLM** (Wang et al., CVPR 2024)：基于 LLM 的关键点定位模型，同样仅处理静态姿态。

Superman 的关键差异化设计在于**运动标记器模态**的根本性转变：从“仅骨架”升级为“视觉引导 + 骨架”的混合码本设计。Vision-Guided Motion Tokenizer (VGMT) 中的每个标记是包含成对视觉原型和几何原型的双模态实体，量化过程同时由视频外观特征和 3D 骨架几何结构引导（Equation 2）。这一设计使得 Superman 成为首个能够从视频输入直接生成 3D 运动序列的 MLLM 模型，在 Table 2 中相比最强 LLM/MLLM 基线实现了 10.91% 的姿态估计改进。

#### 1.3 能力边界对比

Table 1 系统对比了现有模型在感知与生成能力上的覆盖范围。传统多任务模型（MotionBERT, SiC, HiC）具备“理解”能力但无法“生成”；LLM/MLLM 模型（MotionGPT, PoseLLaVA）具备“生成”能力但无法处理原始视觉输入或仅局限于单帧。Superman 是首个同时覆盖“视频感知”、“文本理解”和“3D 运动生成”三项能力的统一框架。

### 2. 方法的适用边界与局限

尽管 Superman 在统一感知与生成方面取得了显著进展，其设计仍存在若干明确的适用边界，这些边界在论文中未作为正式局限性讨论，但从方法设计和实验设定中可以推断：

**（1）对固定 2D 姿态估计器的依赖。** Superman 的 VGMT 模块需要预先计算好的 2D 关节投影作为输入（通过 Visual-Skeleton Attention 模块中的 $\mathbf{p}_{j,f}$ 参数），且整个系统依赖于一个固定的外部 2D 姿态估计器。在极端遮挡、非典型视角或低光照条件下，2D 姿态估计器的退化将直接传播至整个 pipeline。这一依赖关系在 Figure 2 的架构中明确体现，但论文未对 2D 估计器失效场景进行消融分析。

**（2）训练数据的场景局限性。** 所有实验基于 Human3.6M 和 3DPW 两个数据集进行训练和评估。Human3.6M 是受控室内环境下的单人动作数据集，3DPW 虽然包含野外场景但仍以单人动作为主。Table 4 展示了在未见的 3DPW 上的泛化性能，Superman 在运动预测和中间帧生成上均优于所有基线，但这仍限于单人场景。**该方法对多人交互、复杂社交场景、以及大规模野外无约束视频的泛化能力尚未经验证**，这是一个需要后续工作填补的空白。

**（3）视觉-骨架融合权重的敏感性。** Table 6 的消融实验表明，平衡的融合权重（$\beta_s=0.5, \beta_v=0.5$）在标记器重建误差和下游 PE 任务上取得最佳效果。当退化为仅视觉（$\beta_s=0$）或仅骨架（$\beta_v=0$）时，性能均显著下降。这说明混合码本的有效性高度依赖于两种模态的均衡贡献，在某一模态质量严重下降的场景下（如视频模糊或骨架检测失败），方法性能可能面临非线性退化。

**（4）计算效率与实时性的权衡。** 尽管 MAFT 模块仅引入 <0.2% 的额外参数（Table 5），但核心 MLLM 基于 Qwen2.5-VL-7B，推理延迟对于实时应用（如人机交互、自动驾驶）仍是一个挑战。Figure 4 的扩展性分析显示增大模型容量（3B→7B）可一致提升性能，但这也意味着实时部署需要在精度和延迟之间做出权衡。

### 3. 开放问题与未来方向

基于 Superman 的设计选择和实验边界，以下几个开放问题值得后续研究关注：

**（1）视觉引导标记器在未配对数据上的训练策略。** 当前 VGMT 的训练依赖于配对的视频-骨架数据，这限制了可用的训练数据规模。能否利用大规模无监督或弱监督视频数据（仅包含视频而无 3D 骨架标注）来进一步提升运动词汇的泛化能力，是一个重要的开放方向。

**（2）不同视觉 backbone 对标记器表达能力的影响。** 当前 VGMT 的视觉编码器设计在论文中未详细讨论 backbone 选择的影响。不同的视觉 backbone（如 ViT、ConvNeXt、VideoMAE）可能对时空特征的提取质量产生显著差异，进而影响混合码本的表达能力和下游任务性能。这一消融在现有实验中缺失。

**（3）多人场景与交互建模的扩展。** 当前框架以单人运动序列为核心设计，码本中的每个标记对应单个时间窗口内的单人姿态。扩展到多人场景需要解决个体身份保持、交互关系建模、以及码本容量随人数增长而指数膨胀的问题。

**（4）MLLM 推理效率的优化。** 在实时应用场景中，能否通过知识蒸馏、模型量化或推测解码等技术降低 MLLM 的推理延迟，同时保持统一框架的性能优势，是推动该方法走向实际部署的关键问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Superman_Unifying_Skeleton_and_Vision_for_Human_Motion_Perception_and_Generation.pdf]]

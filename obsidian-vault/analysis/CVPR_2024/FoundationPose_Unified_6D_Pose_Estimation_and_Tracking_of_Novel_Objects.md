---
title: "FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects.pdf
aliases:
- FoundationPose
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 本文的核心调节杠杆包括：(1) 利用LLM辅助的大规模合成数据生成管线，实现多样化纹理增强与海量训练，打破数据多样性瓶颈；(2) 采用Transformer架构与对比学习范式，替代传统CNN，提升跨域泛化能力；(3) 引入基于SDF的神经隐式物体场（Neural Object Field），统一模型驱动与模型自由设置，实现高效的新视角RGBD渲染，支撑统一...
primary_logic: 通过LLM驱动的自动化纹理增强生成超大规模多样化合成数据，配合Transformer架构与分层姿态比较（Hierarchical Comparison）策略，FoundationPose 实现了对新物体的强泛化能力，无需微调即可在多个任务上全面超越专用方法；同时，基于SDF的神经物体场可在缺少CAD模型时快速重建物体并提供实时渲染，真正统一了两种工作范式。
claims:
- 在YCB-Video模型自由位姿估计任务中，FoundationPose的ADD-S AUC达到97.4，显著超过最佳基线FS6D的88.4，且无需微调。
- 在LINEMOD模型自由位姿估计任务中，FoundationPose的平均ADD-0.1d达到99.9%，远超所有现有方法。
- 在BOP多数据集模型驱动位姿估计中，FoundationPose的平均AR分数达到83.3，比最强的实例级方法SurfEmb+ICP（79.7）高出3.6个百分点。
- 在YCBInEOAT位姿追踪任务中，FoundationPose的ADD-S AUC达到96.42，比se(3)-TrackNet的84.30高出12.12个百分点。
---

# FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects

> [!tip] 核心洞察
> 通过LLM驱动的自动化纹理增强生成超大规模多样化合成数据，配合Transformer架构与分层姿态比较（Hierarchical Comparison）策略，FoundationPose 实现了对新物体的强泛化能力，无需微调即可在多个任务上全面超越专用方法；同时，基于SDF的神经物体场可在缺少CAD模型时快速重建物体并提供实时渲染，真正统一了两种工作范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | FoundationPose：统一的新物体6D位姿估计与追踪 |
| 英文题名 | FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://nvlabs.github.io/FoundationPose/) · [Code](https://github.com/) · [paper](https://arxiv.org/abs/2312.08344) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | FoundationPose |
| Dataset | YCB-Video, LINEMOD, BOP datasets (LM-O, YCB-V, T-LESS) - model-based, YCBInEOAT |

> [!tip] 效果简介
> - YCB-Video (model-free pose estimation) 上，AUC of ADD-S 97.4 vs 88.4 (FS6D) (+9.0)。
> - LINEMOD (model-free pose estimation) 上，ADD-0.1d (Avg) 99.9 vs 91.5 (FS6D + ICP) (+8.4)。
> - BOP datasets (LM-O, YCB-V, T-LESS) - model-based 上，AR score (Avg) 83.3 vs 79.7 (SurfEmb + ICP) (+3.6)。

## 概述

6D物体位姿估计与追踪是机器人操控、增强现实等应用的基础能力。现有方法高度专业化：模型驱动与模型自由、位姿估计与追踪任务各自孤立，且通常需要针对特定实例进行训练或微调，难以在新物体上实现即拍即用。同时，无纹理、严重遮挡等挑战场景下的鲁棒性不足，进一步限制了实际部署。

FoundationPose提出了一个统一的基础模型，同时支持模型驱动与模型自由两种设置，覆盖6D位姿估计与追踪四项任务。其核心洞察在于：通过大语言模型（LLM）辅助的超大规模多样化合成数据生成，配合Transformer架构与分层姿态比较策略，实现对新物体的强泛化能力，无需微调即可全面超越各任务上的专用方法。具体而言，LLM驱动的两级层次提示策略自动生成逼真纹理增强，打破了数据多样性瓶颈；基于SDF的神经隐式物体场统一了有无CAD模型时的渲染-比对流程；解耦的平移与旋转更新表示以及多头自注意力的分层姿态选择，显著提升了位姿精度与排序质量。

实验验证了FoundationPose的领先地位：在YCB-Video模型自由位姿估计中，ADD-S AUC达到97.4，比最佳基线FS6D（88.4）高出9.0个百分点（Table 1）；在LINEMOD上，平均ADD-0.1d达99.9%（Table 2）；在BOP多数据集模型驱动位姿估计中，平均AR分数83.3，超过最强实例级方法SurfEmb+ICP的79.7（Table 3）；在YCBInEOAT位姿追踪中，ADD-S AUC达96.42，比se(3)-TrackNet（84.30）高出12.12个百分点（Table 4）。在BOP未见物体定位排行榜上，FoundationPose以AR_core 0.726位列第一，超越先前最佳方法PoMZ（0.692）0.03（Figure 8）。消融实验进一步证实，LLM纹理增强、Transformer架构和分层比较策略均为关键设计（Table 6）。

FoundationPose仍存在若干局限：依赖外部2D检测器，虚警或漏检常成为位姿估计的瓶颈；在纹理缺失、严重遮挡与有限边缘线索叠加时，方向估计可能失效（Figure 11）；追踪模式下缺乏长期重初始化机制，可能产生累积漂移。未来方向包括将检测-位姿-追踪统一为端到端框架，以及拓展至非刚体或多物体交互场景。

## 背景与动机

6D物体位姿估计与追踪是机器人操作、增强现实等应用的核心感知任务。现有方法通常针对特定设置进行专项设计：**模型驱动**（model-based）方法依赖已知CAD模型进行渲染-比对，而**模型自由**（model-free）方法则从参考图像中重建或检索物体表示；位姿估计与追踪也往往由独立流水线处理。这种碎片化的研究格局导致三个关键缺口：

1. **缺乏统一的新物体泛化框架**：无论是模型驱动还是模型自由方法，多数需要针对特定物体实例进行训练或微调，难以在无先验知识的新物体上即拍即用。即便部分方法声称支持新物体，其泛化能力仍受限于训练数据的规模和多样性。

2. **数据多样性瓶颈**：现有合成数据生成依赖随机纹理混合（如FS6D从ImageNet/MS-COCO随机混合纹理），生成的训练图像缺乏真实感，限制了模型对多样化外观的适应能力。这直接制约了从合成域到真实域的迁移效果。

3. **鲁棒性不足**：在无纹理、严重遮挡等挑战性场景下，现有方法的位姿估计精度急剧下降。模型自由方法通常依赖局部特征匹配或检索，缺乏全局几何推理；模型驱动方法则受限于渲染质量与比对策略的有效性。

本文的核心动机在于构建一个**统一的基础模型**，同时支持模型驱动与模型自由两种设置下的位姿估计与追踪，且对新物体保持零微调（fine-tune-free）的强泛化能力。为实现这一目标，需要从数据、表示、推理三个层面进行系统性创新：利用大规模多样化合成数据打破数据瓶颈，采用统一的神经渲染桥接两种工作范式，并通过全局上下文感知的位姿推理提升鲁棒性。

## 核心创新

FoundationPose 的核心创新并非单一算法的改进，而是一套系统性重构新物体位姿估计与追踪范式的“杠杆组合”。其关键创新点可归纳为以下五个相互耦合的维度，直接对应方法体系中的 changed slots。

---

### 1. LLM 驱动的超大规模多样化合成数据生成管线

**改变了什么**：将纹理增强从“随机混合”升级为“LLM 引导的语义感知生成”。

现有模型自由方法（如 **FS6D**）采用从 ImageNet/MS-COCO 随机提取纹理块进行混合的策略，生成的纹理缺乏物体语义一致性，限制了训练数据的真实感与多样性。FoundationPose 提出两级层次化提示策略（two-level hierarchical prompt）：首先由 ChatGPT 自动描述物体的可能外观（材质、颜色、纹理风格），再将该描述作为文本提示输入扩散模型生成高质量、语义匹配的纹理贴图（Figure 3）。该管线可在无需人工标注的情况下，为 4 万余个 3D 资产生成多样化纹理，最终构建包含 60 万场景、120 万图像的合成训练集。

**因果机制**：更大的数据规模与语义多样性直接提升了模型对新物体的泛化能力。消融实验（Table 6）表明，去除 LLM 纹理增强后，YCB-Video 上的 ADD-S AUC 显著下降。训练数据规模实验（Figure 7）进一步验证了数据量对性能的单调正向影响。

---

### 2. 基于 SDF 的神经隐式物体场统一两种工作范式

**改变了什么**：将模型自由设置从“独立管线”统一到“渲染-比对”框架。

传统模型自由方法（如 **OnePose++**、**FS6D**）依赖 SfM 重建或检索匹配，与模型驱动方法的渲染-比对流程截然不同，难以统一。FoundationPose 引入基于 SDF 的神经物体场（Neural Object Field），由几何函数 $\Omega: \mathbf{x} \mapsto s$ 和外观函数 $\Phi: (f_{\Omega(\mathbf{x})}, \mathbf{n}, \mathbf{d}) \mapsto \mathbf{c}$ 组成。通过体渲染积分（Eq. 1）与钟形概率密度函数（Eq. 2），可在缺少 CAD 模型时仅需少量参考图像快速重建物体，并通过 Marching Cubes 提取网格实现实时 RGBD 渲染。

$$
c(\mathbf{r}) = \int_{z(\mathbf{r})-\lambda}^{z(\mathbf{r})+0.5\lambda} w(x_i) \Phi(f_{\Omega(x_i)}, \mathbf{n}(x_i), \mathbf{d}(x_i)) dt
$$

$$
w(x_i) = \frac{1}{1+e^{-\alpha \Omega(x_i)}} \cdot \frac{1}{1+e^{\alpha \Omega(x_i)}}
$$

**因果机制**：神经物体场使模型自由设置也能生成任意新视角的 RGBD 渲染，从而与模型驱动设置共享完全相同的渲染-比对-优化流程，真正实现统一框架。

---

### 3. 解耦的平移与旋转位姿更新表示

**改变了什么**：将位姿更新从“齐次 SE(3) 变换”改为“相机坐标系下解耦的平移与旋转”。

传统位姿优化网络直接预测单一的齐次变换矩阵，平移更新依赖于当前旋转估计，耦合了平移与旋转的误差传播。FoundationPose 将位姿更新分解为相机坐标系下独立的平移更新 $\Delta \mathbf{t}$ 和旋转更新 $\Delta R$：

$$
\mathbf{t}^{+} = \mathbf{t} + \Delta \mathbf{t}, \quad R^{+} = \Delta R \otimes R
$$

优化网络（CNN-Transformer 混合编码器）同时预测这两个解耦分量，训练损失为 L2 范数（Eq. 10）：

$$
\mathcal{L}_{\mathrm{refine}} = w_1 \| \Delta \mathbf{t} - \Delta \bar{\mathbf{t}} \|_2 + w_2 \| \Delta R - \Delta \bar{R} \|_2
$$

**因果机制**：解耦表示消除了平移更新对旋转估计的依赖，使两个子问题的优化更稳定。Figure 10 示意了该机制，在消融实验（Table 6）中去除解耦表示同样导致性能下降。

---

### 4. 分层姿态比较策略

**改变了什么**：将姿态评分从“独立绝对打分”升级为“利用全局上下文的层次化比较”。

传统方法对每个位姿假设独立打分，忽略了假设之间的相对关系，导致排序不稳定。FoundationPose 提出分层比较（Hierarchical Comparison）：首先在粗粒度层面比较假设间的相对优劣，再通过多头自注意力（multi-head self-attention）在所有假设间建模全局上下文，预测每个假设的得分。训练采用姿态条件的三元组损失（Eq. 11），正样本定义为与真值旋转测地距离小于阈值 $d$ 的假设（Eq. 12）：

$$
\mathcal{L}(i^{+}, i^{-}) = \max(\mathbf{S}(i^{-}) - \mathbf{S}(i^{+}) + \alpha, 0)
$$

$$
\mathbb{V}^{+} = \{ i : D(R_i, \bar{R}) < d \}
$$

**因果机制**：全局比较使评分能同时对齐形状和纹理线索，预测出更平滑准确的排序趋势（Figure 4）。消融实验（Table 6）证实该策略对最终精度至关重要。

---

### 5. 零微调的跨任务统一泛化

**改变了什么**：从“每任务专项设计+微调”到“单模型零微调覆盖四任务”。

现有方法通常针对位姿估计或追踪单独设计，且需在目标数据集上微调（如 **FS6D** 在 YCB-Video 上需按实例分组微调）。FoundationPose 以统一的渲染-比对-优化流程，配合上述创新，实现了单一模型在模型驱动/模型自由、位姿估计/追踪四个任务上的零微调部署，且全面超越各任务专用方法（Figure 1）。

**因果机制**：大规模多样化合成数据提供了强泛化基础，Transformer 架构与解耦更新增强了跨域迁移能力，神经物体场弥合了范式差异——三者共同使零微调泛化成为可能。在公平性设计上，所有对比方法使用相同 2D 检测结果，FoundationPose 在更少参考图像下仍保持优势（Figure 6），且无需任何微调。

---

### 创新之间的耦合关系

上述五个创新并非孤立叠加，而是形成相互增强的闭环：

- **LLM 数据生成** 提供规模与多样性，是泛化能力的上游保障；
- **神经物体场** 打通模型自由与模型驱动的壁垒，使统一框架成为可能；
- **解耦位姿更新** 与 **分层比较** 分别从优化和决策层面提升精度与鲁棒性；
- **零微调泛化** 是前四项创新的必然结果，也是 FoundationPose 作为“基础模型”的核心定位。

> **需注意**：部分消融实验的定量细节（Table 6 完整数值）在已有证据中未完全展开，建议读者查阅原文获取精确数据。

## 整体框架

FoundationPose 是一个统一的6D物体位姿估计与追踪基础模型，其核心设计目标是消除传统方法中“模型驱动/模型自由”与“位姿估计/位姿追踪”之间的任务隔离，实现对全新物体的零微调泛化。整体框架由四个关键模块串联构成，形成从数据生成到最终位姿输出的完整流水线（Figure 2）。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our framework. To reduce manual efforts for large scale training, we developed a novel synthetic data generation pipeline by leveraging recent emerging techniques and resources including 3D model database, large language models and diffusion models (Sec. 3.1). To bridge the gap between model-free and model-based setup, we leverage an object-centric neural field (Sec. 3.2) for novel view RGBD rendering for subsequent render-99.00 and-compare. For pose estimation, we first initialize global poses uniformly around the object, which are then refined by the refinement network (Sec. 3.3). Finally, we forward the refined poses to the pose selection module which predicts their scores. T...*

### 1. 大规模合成数据生成管线

为突破训练数据的多样性与规模瓶颈，框架首先引入了一条基于LLM辅助的自动化合成数据生成管线（Sec. 3.1）。该管线利用两级层次化提示策略：先由ChatGPT根据物体类别自动生成外观描述，再将描述作为文本提示输入扩散模型进行纹理增强，从而在超过40K个3D资产上生成高度逼真且多样化的纹理。最终构建了包含600K场景、1.2M图像的训练集，为后续网络的大规模预训练提供了数据基础。

### 2. 统一渲染-比对范式

框架通过引入**神经物体场**（Neural Object Field），统一了模型驱动与模型自由两种设置下的渲染-比对流程（Sec. 3.2）。在模型驱动设置下，直接使用CAD模型进行渲染；在模型自由设置下，则基于SDF的神经隐式表示对目标物体进行快速重建，并通过Marching Cubes提取网格实现实时RGBD渲染。这一设计使得无论是否具备CAD模型，后续的位姿估计模块均可复用相同的渲染-比对逻辑，真正弥合了两种范式的鸿沟。

### 3. 位姿假设生成与迭代优化

位姿估计的核心流程分为初始化和优化两步（Sec. 3.3）。首先，利用2D检测框内的中值深度初始化平移量，同时在物体为中心的Icosphere上均匀采样旋转视角，结合面内旋转增广生成 $N_s \times N_i$ 个全局位姿假设。随后，所有假设经过一个基于CNN-Transformer混合编码器的**位姿优化网络**进行迭代修正。该网络的关键创新在于采用解耦的位姿更新表示——平移更新 $\Delta \pmb{t}$ 和旋转更新 $\Delta R$ 均在摄像机坐标系下独立进行：

$$\pmb{t}^{+} = \pmb{t} + \Delta \pmb{t}, \quad R^{+} = \Delta R \otimes R$$

这种解耦设计消除了平移更新对当前旋转状态的依赖，使网络输入与更新量统一在同一坐标系下，显著提升了优化稳定性。

### 4. 分层姿态比较与最优选择

优化后的位姿假设进入**分层姿态选择模块**（Sec. 3.4）。该模块采用两级自注意力机制：首先对各假设进行独立的渲染-比对特征提取，然后通过多头自注意力层在所有假设之间进行全局上下文交互，最终为每个假设预测一个对齐质量分数。与传统独立打分策略相比，这种分层比较能够利用姿态假设间的全局几何与纹理一致性，更准确地识别最优姿态（Figure 4）。训练时采用基于姿态条件的对比三元组损失：

$$\mathcal{L}(i^{+}, i^{-}) = \max(\mathbf{S}(i^{-}) - \mathbf{S}(i^{+}) + \alpha, 0)$$

其中正样本集 $\mathbb{V}^{+}$ 由与真值旋转测地距离小于阈值 $d$ 的假设构成。

### 5. 追踪模式下的扩展

在位姿追踪任务中，框架以上一帧的估计位姿作为当前帧的初始假设，经过同一优化网络进行迭代更新，无需重新初始化。模型自由追踪模式下，参考图像通过贪心选择策略（Eq. 15）最大化视角覆盖，确保神经物体场能够提供高质量的渲染参考。整个追踪流程端到端运行，不依赖外部重初始化机制。

### 输入输出流总结

- **输入**：单帧RGBD图像、2D检测框（由外部检测器提供）、可选的CAD模型或参考图像集。
- **输出**：物体的6D位姿（旋转 $R$ 与平移 $\pmb{t}$），在追踪模式下输出逐帧连续位姿序列。
- **关键依赖**：外部2D检测器（如CNOS或Mask R-CNN）提供物体区域；模型自由设置需提供至少4张参考图像用于神经物体场重建。

## 核心模块与公式推导

FoundationPose 的统一框架由四个核心模块构成：**LLM辅助的大规模合成数据生成**、**神经隐式物体场**、**位姿初始化与优化网络**，以及**分层姿态比较与选择**。以下逐一阐述各模块的关键设计与数学表达。

---

### 3.1 LLM辅助的纹理增强数据生成

为突破训练数据多样性的瓶颈，本文提出两级分层提示（Two-Level Hierarchical Prompt）策略，自动化生成大规模、高真实感的纹理增强合成数据。如 Figure 2 左上角所示，第一级提示：向 ChatGPT 询问某物体的可能外观描述（如“一只陶瓷杯可能有哪些颜色和纹理？”）；第二级提示：将 ChatGPT 的回答作为文本提示输入扩散模型，生成相应的纹理图像并映射到 3D 资产表面。

相较于 FS6D 采用的从 ImageNet/MS-COCO 随机混合纹理的方式（Figure 3 上排），本方法生成的纹理更具语义合理性与视觉真实感（Figure 3 下排）。最终构建了包含 600K 场景、1.2M 图像的训练集，覆盖 40K+ 物体，为后续 Transformer 架构的强泛化能力提供了数据基础。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/003_Figure_3.jpg]]
*Figure 3: Top: Random texture blending proposed in FS6D [22]. Bottom: Our LLM-aided texture augmentation yields more realistic appearance. Leftmost is the original 3D assets. Text prompts are automatically generated by ChatGPT*

---

### 3.2 神经隐式物体场（Neural Object Field）

在模型自由设置下，缺少 CAD 模型时，本文采用基于 SDF（Signed Distance Function）的神经隐式表示，统一模型驱动与模型自由的渲染-比对流程。物体由两个函数描述（Figure 2）：

- **几何函数** $\Omega: \mathbf{x} \mapsto s$，将 3D 点 $\mathbf{x}$ 映射到带符号距离 $s$；
- **外观函数** $\Phi: (f_{\Omega(\mathbf{x})}, \mathbf{n}, \mathbf{d}) \mapsto \mathbf{c}$，以几何特征 $f_{\Omega(\mathbf{x})}$、法向 $\mathbf{n}$ 和视线方向 $\mathbf{d}$ 为输入，输出颜色 $\mathbf{c}$。

沿光线 $\mathbf{r}$ 的颜色体渲染积分限定在截断的近表面区域 $[z(\mathbf{r})-\lambda, z(\mathbf{r})+0.5\lambda]$ 内：

$$c(\mathbf{r}) = \int_{z(\mathbf{r})-\lambda}^{z(\mathbf{r})+0.5\lambda} w(\mathbf{x}_i) \, \Phi\big(f_{\Omega(\mathbf{x}_i)}, \mathbf{n}(\mathbf{x}_i), \mathbf{d}(\mathbf{x}_i)\big) \, dt \tag{1}$$

其中权重函数 $w(\mathbf{x}_i)$ 为基于 SDF 的钟形概率密度，峰值位于隐式物体表面：

$$w(\mathbf{x}_i) = \frac{1}{1+e^{-\alpha \Omega(\mathbf{x}_i)}} \cdot \frac{1}{1+e^{\alpha \Omega(\mathbf{x}_i)}} \tag{2}$$

深度渲染同理。训练收敛后，通过 Marching Cubes 提取显式网格，实现实时 RGBD 渲染，直接对接后续的渲染-比对优化流程。

---

### 3.3 位姿初始化与解耦优化网络

**初始化**：平移由检测到的 2D 边界框内中值深度对应的 3D 点确定；旋转通过在物体为中心的 Icosphere 上均匀采样 $N_s$ 个视点，并辅以 $N_i$ 个离散化的面内旋转增广，生成 $K = N_s \times N_i$ 个全局位姿假设。

**解耦位姿更新**：与传统齐次 SE(3) 变换不同，本文在摄像机坐标系下解耦平移和旋转更新（Figure 10）：

$$\mathbf{t}^{+} = \mathbf{t} + \Delta\mathbf{t}, \quad R^{+} = \Delta R \otimes R \tag{8-9}$$

该表征消除了平移更新对更新后旋转的依赖，使更新量与输入观测统一于同一坐标系，利于网络学习。

**优化网络**：采用 CNN-Transformer 混合编码器（Figure 9），以渲染-观测图像对为输入，预测解耦的平移修正 $\Delta\mathbf{t}$ 和旋转修正 $\Delta R$。训练监督为 L2 损失：

$$\mathcal{L}_{\mathrm{refine}} = w_1 \|\Delta\mathbf{t} - \Delta\bar{\mathbf{t}}\|_2 + w_2 \|\Delta R - \Delta\bar{R}\|_2 \tag{10}$$

其中 $\bar{\mathbf{t}}$、$\bar{R}$ 为真值，权重 $w_1$、$w_2$ 经验性设为 1。

---

### 3.4 分层姿态比较与选择

优化后的 $K$ 个位姿假设需进行全局最优选择。本文提出**分层比较（Hierarchical Comparison）**策略：首先通过姿态排序编码器对每个假设独立提取对齐质量特征 $\mathbf{F} \in \mathbb{R}^{512}$，随后采用多头自注意力（Multi-Head Self-Attention）在所有 $K$ 个假设间进行全局上下文交互，预测每个假设的得分 $\mathbf{S}(i)$。

训练采用姿态条件三元组损失：

$$\mathcal{L}(i^{+}, i^{-}) = \max\big(\mathbf{S}(i^{-}) - \mathbf{S}(i^{+}) + \alpha, 0\big) \tag{11}$$

正样本集定义为与真值旋转的测地距离小于阈值 $d$ 的假设：

$$\mathbb{V}^{+} = \{ i : D(R_i, \bar{R}) < d \} \tag{12}$$

负样本集为全部 $K$ 个假设 $\mathbb{V}^{-} = \{0, 1, \dots, K-1\}$。该策略使模型能利用全局姿态上下文（如形状一致性和纹理对齐趋势）进行更准确的排序（Figure 4），显著优于独立绝对打分方式。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/004_Figure_4.jpg]]
*Figure 4: Pose ranking visualization. Our proposed hierarchical comparison leverages the global context among all pose hypotheses for a better overall trend prediction that aligns both shape and texture. The true best pose is annotated with red circle*

---

### 3.5 追踪模式下的参考图像选择

在模型自由追踪中，需从历史帧中选取参考图像以维持渲染比对。本文采用贪心策略最大化视角覆盖：从候选集 $\mathbb{S}_t$ 中逐帧选取与已选集合 $\mathbb{S}_r$ 中所有帧的最小旋转测地距离最大的帧：

$$i^{*} = \underset{i \in \mathbb{S}_t, i \notin \mathbb{S}_r}{\mathrm{argmax}} \left( \underset{j \in \mathbb{S}_r}{\min} \, D(\mathbf{R}_i, \mathbf{R}_j) \right) \tag{15}$$

该策略确保参考图像集在 SO(3) 上均匀分布，提升多视角下的位姿追踪鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/016_Figure_10.jpg]]
*Figure 10: Illustration of disentangled representation for pose updates*

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/015_Figure_9.jpg]]
*Figure 9: Network architecture for image feature embedding used in pose refinement and selection networks. The ResBlock is from ResNet-34 [17]*

## 实验与分析

### 核心实验设置与公平性说明

FoundationPose 在四个任务上进行了系统性评估：模型自由位姿估计、模型驱动位姿估计、位姿追踪，以及 BOP 未见物体定位排行榜。所有对比实验均遵循严格的公平性原则：**所有方法使用相同的 2D 检测结果**（Mask R-CNN 或 CNOS）作为输入；在模型自由设置中，除 RGB-only 方法外，均提供 16 张参考图像。值得注意的是，部分基线方法（如 FS6D）在目标数据集上进行了**微调**，而 FoundationPose 始终保持**零微调**，且在更少参考图像下仍表现更优。位姿追踪实验中未采用重初始化，以评估长期跟踪鲁棒性；FoundationPose 的端到端流水线可自初始化，无需外部姿态提供。

### 模型自由位姿估计

在 YCB-Video 数据集上（Table 1），FoundationPose 取得了 **AUC of ADD-S 97.4** 的显著成绩，比最佳基线 FS6D（88.4）高出 **9.0 个百分点**。在 ADD 指标上，FoundationPose 达到 91.5，同样大幅领先所有对比方法。这一优势建立在 FS6D 已对测试集进行实例分组微调的前提下，而 FoundationPose 完全无需微调。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/005_Table_1.jpg]]
*Table 1: Model-free pose estimation results measured by AUC of ADD and ADD-S on YCB-Video dataset. “Finetuned” means the method was fine-tuned with group split of object instances on the testing dataset, as introduced by [22]*

在 LINEMOD 数据集上（Table 2），FoundationPose 的平均 **ADD-0.1d 达到 99.9%**，远超 FS6D + ICP（91.5%）达 8.4 个百分点，近乎饱和的性能表明该方法对弱纹理工业零件具有极强的泛化能力。Figure 5 的定性对比进一步显示，在严重自遮挡和缺乏纹理的胶水瓶等挑战场景中，OnePose++ 和 LatentFusion 均出现明显漂移，而 FoundationPose 成功估计了正确姿态。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/006_Table_2.jpg]]
*Table 2: Model-free pose estimation results measured by ADD-0.1d on LINEMOD dataset. Gen6D* [40] represents the variation without fine-tuning*

### 模型驱动位姿估计

在 BOP 核心数据集（LM-O、YCB-V、T-LESS）上（Table 3），FoundationPose 的平均 **AR 分数达到 83.3**，比最强的实例级方法 SurfEmb + ICP（79.7）高出 **3.6 个百分点**。这一结果表明，FoundationPose 作为通用模型，在模型驱动设置下不仅超越了所有专用方法，且无需针对特定实例进行任何微调。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/008_Table_3.jpg]]
*Table 3: Model-based pose estimation results measured by AR score on representative BOP datasets. All methods use the RGBD modality*

在 BOP 未见物体定位排行榜上（Figure 8），FoundationPose 以 **AR_core 0.726** 位列第一，超越先前最佳方法 PoMZ（0.692）**0.03**，创造了新的基准记录。这一结果直接验证了该方法对全新物体的强泛化能力。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/014_Figure_8.jpg]]
*Figure 8: Screenshot on BOP leaderboard. At the time of submission, our approach outperforms the previous best method “PoMZ” (not yet published) by a considerable margin of 0.03 on*

### 位姿追踪

在 YCBInEOAT 数据集上（Table 4），FoundationPose 的 **AUC of ADD-S 达到 96.42**，比 se(3)-TrackNet（84.30）高出 **12.12 个百分点**。在 YCB-Video 追踪任务中（Table 5），FoundationPose 在模型自由设置下同样表现优异，进一步证明了统一框架在追踪任务上的有效性。Ours† 变体使用位姿估计模块进行自初始化，展示了端到端流水线无需外部姿态提供的优势。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/009_Table_4.jpg]]
*Table 4: Pose tracking results of RGBD methods measured by AUC of ADD and ADD-S on YCBInEOAT dataset. Ours† represents our unified pipeline that uses the pose estimation module for pose initialization*

### 消融实验

Table 6 的消融实验揭示了三个关键设计的作用：

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/011_Table_6.jpg]]
*Table 6: Ablation study of critical design choices*

1. **LLM 纹理增强**：去除 LLM 辅助的纹理增强后，性能显著下降，验证了大规模多样化合成数据对泛化能力的关键贡献。
2. **Transformer 架构**：替换为传统 CNN 架构导致性能退化，表明 Transformer 的全局建模能力对跨域泛化至关重要。
3. **分层比较策略**：去除分层比较后性能明显降低，证明了利用全局姿态上下文进行打分的重要性。

Figure 6 展示了参考图像数量的影响：**即便仅使用 4 张参考图像，FoundationPose 仍优于使用 16 张参考图像的 FS6D**，进一步凸显了方法的样本效率优势。Figure 7 表明，训练数据规模的持续扩大带来稳定的性能增益，验证了大规模合成数据管线的价值。

![[assets/figures/papers/paper_list_l14_FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects_motion20v/figures/013_Figure_6.jpg]]
*Figure 6: Effects of number of reference images*

### 失败模式与局限性

Figure 11 展示了典型的失败案例：在**纹理缺失、严重遮挡、有限边缘线索**等多重挑战叠加的情况下，FoundationPose 的方向估计可能失效。这揭示了当前方法在极端条件下的根本瓶颈——当视觉线索极度匮乏时，基于渲染-比对的优化策略缺乏足够的约束信号。

此外，FoundationPose 依赖外部 2D 检测器（如 CNOS 或 Mask R-CNN），虚警或漏检常成为 6D 位姿估计的瓶颈，未能实现检测-位姿联合端到端。追踪模式下未引入长期重初始化机制，可能产生累积漂移。这些问题指向了未来将 2D 检测、6D 位姿估计与追踪统一为端到端框架的研究方向。

## 方法谱系与知识库定位

### 1. 与现有基线方法的关系

FoundationPose 的提出，本质上是对6D位姿估计与追踪领域长期存在的“任务-设定”双重割裂的一次统一性回应。在它之前，模型驱动（model-based）与模型自由（model-free）、位姿估计与位姿追踪四类任务各自发展出了高度特化的方法，彼此之间缺乏共享的框架与泛化能力。

**模型自由位姿估计基线**：该设定下的核心挑战在于，测试物体没有可用的CAD模型，仅提供少量参考图像。**FS6D**（He et al., CVPR 2022）是此设定下的代表性工作，其核心思路是“渲染-比对”：利用随机纹理增强的合成数据训练一个位姿评分网络，在测试时对参考图像进行三维重建或新视角渲染，再通过评分网络评估位姿假设的质量。FS6D的关键局限在于：（1）纹理增强策略仅为从ImageNet/MS-COCO中随机混合纹理，生成的训练数据多样性有限；（2）需要在目标测试集上进行微调才能达到最佳性能；（3）评分网络独立评估每个位姿假设，忽略了假设之间的全局上下文。**OnePose++**（He et al., CVPR 2023）则走向了另一条路径——基于RGB输入的稀疏重建与2D-3D匹配，不依赖深度传感器，但对无纹理和遮挡场景的鲁棒性显著不足。**Gen6D**（Liu et al., ECCV 2022）尝试用生成式方法处理新物体，但在不微调的情况下性能大幅下降。

FoundationPose 对上述基线的超越是系统性的：它将纹理增强策略从“随机混合”升级为“LLM辅助的两级层次化提示”（ChatGPT描述物体外观 → 扩散模型生成纹理），使合成数据的视觉真实性大幅提升；将评分策略从“独立绝对评分”升级为“分层比较”（hierarchical comparison），通过多头自注意力机制在所有位姿假设之间建立全局上下文；并且在整个过程中**不进行任何针对目标物体的微调**。在YCB-Video模型自由设定中，FoundationPose的ADD-S AUC达到97.4，比经过微调的FS6D（88.4）高出9.0个百分点（Table 1）；在LINEMOD上，ADD-0.1d平均达到99.9%，远超FS6D+ICP的91.5%（Table 2）。即便仅使用4张参考图像，FoundationPose仍优于使用16张参考图像的FS6D（Figure 6），这直接证明了其数据效率与泛化能力的优势。

**模型驱动位姿估计基线**：在提供CAD模型的设定下，BOP挑战赛提供了标准化的评测基准。**SurfEmb+ICP**（Hodaň et al., IJCV 2024）是此前最强的实例级方法，其核心是利用物体表面的神经嵌入场进行渲染-比对，并结合ICP精修，在LM-O、YCB-V、T-LESS等数据集上平均AR分数达到79.7。**MegaPose-RGBD**（Labbe et al., CoRL 2023）则采用了一种检索-比对的策略，通过在大规模合成数据上训练的Transformer进行位姿估计。FoundationPose 在同一基准上以平均AR 83.3超越了SurfEmb+ICP（+3.6），且这一优势是在**零微调**的前提下取得的（Table 3）。值得注意的是，SurfEmb等方法需要针对每个物体实例单独训练嵌入场，而FoundationPose的通用渲染-比对流程无需任何实例级训练。

**位姿追踪基线**：追踪任务要求方法在视频序列中持续估计物体位姿。**se(3)-TrackNet**（Wen et al., BMVC 2020）是实例级RGBD追踪的代表，通过SE(3)上的等变网络进行帧间位姿更新，在YCBInEOAT上ADD-S AUC为84.30。**BundleTrack**（Wen & Bekris, IROS 2021）则支持模型自由设定，通过在线关键帧图优化进行追踪，但缺乏全局重初始化能力。FoundationPose 的追踪模块直接复用其位姿估计网络进行帧间更新，在YCBInEOAT上ADD-S AUC达到96.42，比se(3)-TrackNet高出12.12个百分点（Table 4）。更重要的是，FoundationPose的端到端流水线具备自初始化能力（无需外部提供初始位姿），而多数基线方法依赖外部初始化或假设首帧位姿已知。

**BOP未见物体定位排行榜**：在更具挑战性的“未见物体”设定下（测试物体完全不出现在训练集中），FoundationPose以AR_core 0.726位列第一，超越此前最佳方法**PoMZ**（未正式发表）的0.692，差距达到0.03（Figure 8）。这一结果直接验证了其作为“基础模型”的泛化边界。

### 2. 核心调节杠杆与因果机制

FoundationPose 的性能优势可归因于四个环环相扣的因果调节杠杆，它们共同构成了从数据到架构再到推理策略的系统性改进：

**杠杆一：LLM辅助的大规模合成数据生成管线**。传统合成数据的纹理增强（如FS6D的随机混合）受限于人工设计的规则，难以覆盖真实世界中物体外观的多样性与合理性。FoundationPose 引入两级层次化提示策略——先让ChatGPT描述物体的可能外观，再将该描述作为扩散模型的文本提示生成纹理——使得纹理增强既具有语义合理性，又具备视觉多样性。这一管线在超过40K个3D资产上生成了600K个场景、1.2M张图像（Sec. 3.1, Sec. 5.2），数据规模与多样性远超此前任何工作。消融实验表明，去除LLM纹理增强后，YCB-Video上的ADD-S从97.40降至94.90（Table 6），验证了数据质量对泛化能力的因果贡献。

**杠杆二：基于SDF的神经隐式物体场**。模型自由设定的根本困难在于缺少CAD模型，无法进行传统的渲染-比对。FoundationPose 通过一个物体中心的神经隐式场（包含几何函数Ω和外观函数Φ），在仅需数十张参考图像的情况下即可快速重建物体，并通过Marching Cubes提取网格实现实时RGBD渲染（Sec. 3.2）。这一设计巧妙地将模型自由设定“转化”为模型驱动设定的子问题——无论原始设定如何，后续的位姿估计模块始终面对的是“渲染图像与观测图像的比对”。这种统一性消除了传统方法中两套独立管线的冗余与不兼容。

**杠杆三：Transformer架构与对比学习范式**。传统的位姿评分网络（如FS6D的CNN编码器）独立处理每个位姿假设，缺乏对全局假设分布的感知。FoundationPose 的位姿选择模块采用多头自注意力机制，在所有K个位姿假设之间进行分层比较（先分组比较，再跨组比较），使得评分能够利用全局上下文——例如，当多个假设都指向相似的错误方向时，网络可以通过对比识别出真正的正确位姿（Figure 4）。消融实验显示，将分层比较替换为独立评分后，ADD从91.52降至88.67（Table 6），证明了全局上下文对精确位姿选择的必要性。

**杠杆四：解耦的位姿更新表示**。传统位姿更新使用齐次SE(3)变换，平移更新依赖于旋转更新后的坐标系，导致优化耦合且不稳定。FoundationPose 将平移和旋转更新解耦，均在摄像机坐标系下独立表达：$\pmb{t}^{+} = \pmb{t} + \Delta \pmb{t}$，$R^{+} = \Delta R \otimes R$（Eq. 8-9）。这一设计消除了平移更新对方向的依赖，使网络学习更加稳定。消融实验表明，去除解耦表示后，ADD从91.52降至89.06（Table 6）。

### 3. 适用边界与失效模式

尽管FoundationPose展现了强大的泛化能力，其适用边界同样清晰可辨：

**对外部2D检测器的依赖**：FoundationPose 假设目标物体已被一个2D检测器（如Mask R-CNN或CNOS）定位，其位姿初始化直接使用检测框内的中值深度。这意味着2D检测的虚警或漏检会直接成为6D位姿估计的不可恢复错误。这一设计使得FoundationPose 并非一个真正端到端的检测-位姿联合系统，在密集遮挡或多物体交互场景中，检测器本身的局限性可能成为瓶颈。

**极端挑战条件下的方向估计失效**：论文明确展示了失败案例（Figure 11）：在纹理缺失、严重遮挡、有限边缘线索三者叠加的情况下，FoundationPose 的方向估计可能完全错误。这表明基于渲染-比对的范式在视觉线索极度匮乏时仍然脆弱——当渲染图像与观测图像之间的差异主要由噪声而非位姿误差主导时，评分网络缺乏足够的判别信号。值得注意的是，这种失效模式并非FoundationPose独有，而是整个渲染-比对范式的共性瓶颈。

**追踪模式下的累积漂移**：FoundationPose 的追踪模块采用帧间迭代更新，未引入长期重初始化机制。在长序列中，微小的帧间误差可能逐步累积，最终导致位姿漂移。论文在追踪实验中未采用重初始化（以评估长期鲁棒性），这意味着在需要长时间稳定追踪的应用场景（如机器人持续操作）中，累积漂移可能成为实际问题。

**神经隐式场的重建质量依赖**：在模型自由设定下，FoundationPose 的性能高度依赖于神经物体场的重建质量。如果参考图像视角覆盖不足或物体表面反射/透明，SDF重建可能产生几何缺陷，进而影响后续渲染-比对的质量。论文未系统评估不同参考图像质量对最终位姿精度的影响。

### 4. 开放问题与后续工作方向

FoundationPose 的提出开启了若干值得深入探索的方向：

**统一检测-位姿端到端框架**：将2D检测、6D位姿估计与追踪统一为一个端到端可训练的基础模型，消除对外部检测器的依赖。这需要处理检测与位姿的联合优化问题，以及如何在统一框架中平衡不同任务的损失函数。

**拓展至非刚体与多物体交互**：当前框架假设物体为刚体且场景中仅关注单一物体。将基础模型拓展至铰接物体、可变形物体，以及多物体交互场景（如装配、堆叠）的状态估计，是走向通用物体状态理解的关键一步。

**极端条件下的鲁棒性增强**：如何在无纹理和强遮挡条件下为渲染-比对提供更丰富的判别信号？可能的方向包括：引入触觉等多模态传感、利用时序一致性约束、或采用更强大的特征学习策略（如基于基础视觉模型的特征提取）。

**轻量化神经渲染**：当前方法通过Marching Cubes提取显式网格进行渲染，这一步骤在实时性要求高的场景中可能成为瓶颈。探索直接基于神经隐式场的轻量渲染（如高效的光线步进策略或知识蒸馏为小型渲染网络），有望进一步提升实时性。

**更广泛的物体类别覆盖**：FoundationPose 的训练数据主要来自3D模型数据库，覆盖的物体类别仍然有限。如何利用互联网规模的图像-视频数据（如通过自监督学习）进一步扩展基础模型的物体知识，使其能够处理真正“任意”的新物体，是一个开放且有价值的问题。

## 原文 PDF

![[paperPDFs/CVPR_2024/FoundationPose_Unified_6D_Pose_Estimation_and_Tracking_of_Novel_Objects.pdf]]
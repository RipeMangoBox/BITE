---
title: Exploring Spatial Intelligence from a Generative Perspective
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Exploring_Spatial_Intelligence_from_a_Generative_Perspective.pdf
project_link: null
code_link: null
aliases:
- GBGS
- ESIFGP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在精确的合成空间编辑数据（GSI-Syn）上对统一多模态模型进行微调，迫使模型学习物理上合理的 3D 空间变换，从而增强内部空间表征。
primary_logic: 生成式空间编辑训练能够内化为鲁棒的空间表征，不仅提升编辑任务的合规性，还可迁移至下游空间理解任务，建立以生成促理解的新路径。
claims:
- 在 GSI-Real 真实场景编辑上，微调 BAGEL 的平均分从 28.46 提升至 36.28，增益 7.83 分。
- 在 OmniSpatial 空间理解基准上，整体准确率从 41.55 提升至 42.07。
- 在 SAT-Real 空间推理基准上，整体准确率从 65.33 提升至 69.33。
- BAGEL + GSI-Syn 在 GSI-Syn-Room 合成基准上比原始 BAGEL 平均分提升 +22.15。
---

# Exploring Spatial Intelligence from a Generative Perspective

> [!tip] 核心洞察
> 生成式空间编辑训练能够内化为鲁棒的空间表征，不仅提升编辑任务的合规性，还可迁移至下游空间理解任务，建立以生成促理解的新路径。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从生成视角探索空间智能 |
| 英文题名 | Exploring Spatial Intelligence from a Generative Perspective |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.20570) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GSI-Bench 与基于 GSI-Syn 的生成式空间智能增强方法 |
| Dataset | GSI-Syn-Room, GSI-Real, OmniSpatial, SAT-Real |

> [!tip] 效果简介
> - GSI-Syn-Room 上，Avg BAGEL+GSI-Syn vs BAGEL (+22.15)。
> - GSI-Real 上，Average score 36.28 vs 28.46 (+7.83)。
> - OmniSpatial 上，Overall accuracy 42.07 vs 41.55 (+0.52)。

## 概述

### 问题背景与瓶颈

当前多模态模型的空间智能研究主要集中于**空间理解**（spatial understanding）维度，即评估模型能否正确回答关于物体位置、空间关系、视角变换等问题。然而，空间智能的另一关键侧面——**生成式空间智能**（Generative Spatial Intelligence, GSI）——长期被忽视。这一瓶颈表现为：模型缺乏在图像生成或编辑过程中遵循精确空间约束的能力，也难以通过生成任务内化鲁棒的空间表征，从而限制了理解与生成的耦合利用。

### 核心思路与因果机制

本文从生成视角重新审视空间智能，将其操作化为**空间约束下的图像编辑任务**：给定输入图像 $\mathcal{I}$ 和明确的空间编辑指令 $\mathcal{T}$，统一多模态模型 $f$ 需生成输出图像 $\mathcal{I}^{\prime} = f(\mathcal{I}, \mathcal{T})$，其中空间变换必须物理合理且精确可控。

核心因果机制在于：通过在**大规模合成空间编辑数据（GSI-Syn）** 上对统一多模态模型进行微调，迫使模型学习将自然语言空间指令映射为结构化的 3D 场景变换。这一过程将空间推理内化为模型的隐式表征，不仅直接提升编辑任务的空间合规性，还能**迁移至下游空间理解任务**，建立“以生成促理解”的新路径。

### 方法与基准定位

为支撑上述研究，本文构建了 **GSI-Bench**，一个包含合成与真实场景的空间智能基准，涵盖七种定量空间操作（移动、放置、旋转、容纳、视角变换、删除、缩放）。其数据生成管线利用 3D 先验与规则化操作生成、多模态大模型质量门控及人工验证，产出高质量的 $( \mathcal{I}, \mathcal{T}, \mathcal{I}^{\prime} )$ 三元组。在方法谱系中，该工作位于**空间推理基准**与**统一多模态生成模型**的交叉地带：与侧重理解的 OmniSpatial、SAT-Real 等基准互补，同时在模型层面以 **BAGEL**（Deng et al., arXiv 2025）为基线，对比 **Emu3.5**（Cui et al., arXiv 2025）、**GPT-img**（Hurst et al., arXiv 2024）等统一或商用模型。

### 主要结果

- **空间编辑能力大幅提升**：BAGEL + GSI-Syn 在合成基准 GSI-Syn-Room 上平均分提升 **+22.15**；在真实场景 GSI-Real 上平均分从 28.46 提升至 36.28（**+7.83**）。
- **空间理解迁移增益**：在 OmniSpatial 空间理解基准上整体准确率从 41.55 提升至 42.07（**+0.52**）；在 SAT-Real 空间推理基准上从 65.33 提升至 69.33（**+4.00**），尤其在目标导向理解与自我中心推理维度增益显著。
- **跨域泛化验证**：合成数据微调带来的编辑能力提升同时表现在合成域和真实域，初步证明该方法的跨域迁移潜力。

### 局限与开放问题

当前验证仅基于单一架构（BAGEL），合成环境多样性有限，真实场景操作依赖 3D 重建精度。开放问题包括：生成式训练能否在无理解标签的情况下提升更复杂的全局空间推理？模型是否真正建立了隐式 3D 世界模型，还是仅实现了表层的图像级模仿？以及该方法能否扩展到动态交互场景以连接具身智能。

## 背景与动机

### 空间智能的定义缺口：从理解到生成

空间智能（Spatial Intelligence）长期以来被多模态模型社区视为一项核心能力，但现有工作几乎完全从“理解”的角度对其进行定义与评估。典型的空间理解基准——如目标定位、空间关系判断、视角推理等——衡量的是模型对静态场景中空间结构、物体关系与相机位姿的解析能力。然而，这种单向的评估范式忽略了一个关键维度：**生成式空间智能（Generative Spatial Intelligence, GSI）**，即模型是否能够根据明确的空间指令，对视觉场景进行物理上合理的、受约束的编辑与操作。

这一缺口在方法论层面形成了一个真实瓶颈：当前多模态模型缺乏对生成式空间约束遵循与操作能力的系统性评估，导致生成过程中的空间推理无法被强化，理解与生成之间的耦合关系也难以被利用。论文的核心洞察在于，**生成式空间编辑训练能够内化为鲁棒的空间表征**——模型在学习“将物体向左移动”或“将杯子放在盘子右侧”的过程中，被迫建立对 3D 空间关系、遮挡、透视和物体恒常性的精细表征，这种表征不仅服务于编辑任务本身，还可迁移至下游的空间理解任务，从而建立一条“以生成促理解”的新路径。

### 现有基准的能力盲区

当前主流的空间推理基准存在两个结构性缺陷。其一，**任务类型单一**：绝大多数基准仅覆盖空间理解任务（如 VQA 形式的相对位置判断、多视角一致性检验），缺乏对生成式空间操作——移动、放置、旋转、容纳、视角变换、删除、缩放——的评估。其二，**场景域受限**：现有数据集要么依赖合成场景（缺乏真实世界的纹理、光照和物体多样性），要么仅提供自然图像但缺乏精确的 3D 标注，难以支撑对空间编辑结果的自动化、细粒度评估。

这些盲区导致了一个关键问题无法被回答：**现代生成式或统一多模态模型是否具备生成式空间智能？** 换言之，当模型被要求“将桌子上的红苹果移到蓝色书本旁边”时，它能否在保持场景外观一致性的前提下，准确执行这一空间操作？现有的评估体系无法给出答案。

### 统一多模态模型的潜力与未验证的假设

近年来，统一多模态模型（如 BAGEL、Emu3.5、JanusPro）将图像理解与生成整合到单一架构中，通过自注意力机制实现感知与生成模块的深度交互。这类模型为生成式空间智能提供了理想的技术载体：它们天然支持图像编辑任务，且其内部表征可能同时编码了场景的语义与空间信息。

然而，一个悬而未决的假设是：**在精确的合成空间编辑数据上进行微调，能否迫使统一模型学习物理上合理的 3D 空间变换，从而增强其内部空间表征？** 这一假设构成了论文的因果调节变量（causal knob）。如果成立，它将意味着生成式训练可以成为空间智能的强化路径，而不仅仅是评估手段。论文通过构建 GSI-Bench 基准和 GSI-Syn 合成训练数据集，对这一假设进行了系统性验证。

## 核心创新

### 生成式空间智能的范式定义

本工作的根本创新在于将空间智能从传统的“理解”范式拓展至“生成”范式。现有空间智能研究（如空间VQA、具身导航）主要衡量模型对空间关系的感知与推理能力，但忽略了模型在**生成过程中主动遵循空间约束**的能力。GSI-Bench 首次将生成式空间智能（Generative Spatial Intelligence, GSI）操作化为一个**空间约束下的图像编辑任务**：给定输入图像 $\mathcal{I}$ 和一条包含明确空间关系的文本指令 $\mathcal{T}$，模型需生成符合物理空间规律的目标图像 $\mathcal{I}^{\prime} = f(\mathcal{I}, \mathcal{T})$（Section 3.2）。这一任务定义将空间推理从被动选择转变为主动构建，迫使模型在生成过程中内化 3D 空间变换。

### 核心因果机制：以生成促理解

该工作的核心洞察在于揭示了**生成式空间编辑训练可以内化为鲁棒的空间表征，并迁移至下游空间理解任务**。这一“以生成促理解”的因果链条构成了整个方法论的基石：

- **因果干预变量**：在精确的合成空间编辑数据 GSI-Syn 上对统一多模态模型进行微调。GSI-Syn 通过物理模拟器生成精确的 $( \mathcal{I}, \mathcal{T}, \mathcal{I}^{\prime} )$ 三元组，使模型学习在 3D 几何约束下执行物理上合理的空间变换（Section 5）。
- **因果效应验证**：微调后的 BAGEL 模型不仅在编辑任务上大幅提升，还在两个独立的空间理解基准上获得增益——OmniSpatial 准确率从 41.55 提升至 42.07（Table 3），SAT-Real 准确率从 65.33 提升至 69.33（Table 4）。这表明生成式训练习得的空间表征具有跨任务迁移能力，无需额外理解标注即可强化空间推理。

### 相对基线的关键创新点（Changed Slots）

与现有统一多模态模型（如 BAGEL、Emu3.5）相比，本工作在以下两个核心维度上进行了根本性改造：

**1. 训练数据来源：从通用多模态数据到精确空间编辑数据**

基线模型依赖通用多模态预训练数据（图文对、通用编辑数据），这类数据缺乏精确的空间标注和物理约束。GSI-Syn 通过一套完整的合成数据生成管线，产出包含精确 3D 几何真值的空间编辑三元组：
- 基于 AI2-THOR 和 Mesa-Task 模拟器构建室内场景，通过 DBSCAN 聚类划分房间并进行最大分散视点采样（Section 4.1）。
- 在 3D 场景中生成关系/相机变换候选，通过几何检查验证物理可行性，再经物理模拟器执行并校验成功，失败则回滚重采样（Section 4.1）。
- 引入 MLLM 质量门控（Qwen3-VL-235B）进行后处理过滤，剔除模拟瑕疵和不合理遮挡等异常样本（Section 4.1）。

这一数据构造策略确保了每条训练样本都携带精确的空间变换真值，为模型学习物理上合理的空间操作提供了监督信号。

**2. 训练任务：从通用理解-生成混合到定量空间操作**

基线模型通常混合训练图像理解与文本生成任务，缺乏对空间关系精确遵循的专门训练。GSI-Bench 定义了七种定量空间操作类型（Table 1）：移动、放置、旋转、容纳、视角变换、删除、缩放。这些操作覆盖了关系约束（如“将杯子放在盘子左侧”）、相机变换（如“从右侧观察场景”）和物体属性修改（如“放大沙发”）等核心空间交互模式，迫使模型在生成过程中精确遵循 3D 空间约束，而非仅依赖表层的图像统计模式。

### 方法谱系与知识库定位

GSI-Bench 位于空间智能评估与生成式模型训练的交汇点，其方法谱系可沿以下维度定位：

- **空间理解基准谱系**：不同于 OmniSpatial（空间VQA）、SAT-Real（空间推理选择题）等纯理解基准，GSI-Bench 引入了生成维度的评估，要求模型在像素空间中主动构建符合空间约束的输出。
- **图像编辑基准谱系**：不同于 MagicBrush、InstructPix2Pix 等通用编辑基准，GSI-Bench 聚焦于**空间约束的精确遵循**，并通过四维评估协议（指令遵守 IC、空间准确性 SA、外观一致性 AC、编辑局部性 EL）进行细粒度度量（Section 4.3）。
- **统一多模态模型训练**：以 **BAGEL**（Deng et al., arXiv 2025）作为基础架构，该模型原生支持图像编辑并通过自注意力机制实现感知与生成模块的深度交互。GSI-Syn 微调可视为一种**空间感知的指令微调**，与通用指令微调形成互补。

### 局限与待验证边界

需要指出的是，当前创新存在以下边界条件，需在解读时审慎对待：

- **架构泛化性未验证**：微调实验仅基于 BAGEL 单一架构，GSI-Syn 训练在其他统一多模态模型（如 Emu3.5、JanusPro）上的有效性尚待验证。
- **合成到真实的域间隙**：GSI-Syn 的合成环境（AI2-THOR、Mesa-Task）在视觉多样性和物理真实度上有限，GSI-Real 上的增益（+7.83 分）虽显著但低于合成域增益（+22.15 分），表明域间隙仍是影响迁移效果的关键因素。
- **空间理解增益的幅度有限**：OmniSpatial 上仅提升 0.52 个百分点，提示生成式训练对特定空间推理子能力的迁移机制仍需深入分析。

## 整体框架

GSI-Bench 的构建围绕一个核心任务展开：**空间接地的图像编辑**（Spatially Grounded Image Editing）。给定输入图像 $\mathcal{I}$ 和一条明确的空间编辑指令 $\mathcal{T}$，统一多模态模型 $f$ 需要生成符合指令的目标图像 $\mathcal{I}^{\prime}$，即 $\mathcal{I}^{\prime} = f(\mathcal{I}, \mathcal{T})$。这一任务形式化的关键在于，每一条编辑指令背后都对应着一个潜在的 3D 场景变换，迫使模型在生成过程中隐式地推理物体的空间关系、相机视角和物理可行性。

### 场景建模与操作定义

为将模糊的语言指令转化为可验证的几何操作，GSI-Bench 将每个视觉场景建模为 3D 结构 $\mathcal{S} = \{\mathcal{O}_{i}\}_{i=1}^{N} \cup \{\mathcal{C}\}$，其中物体 $\mathcal{O}_{i} = (\mathbf{c}_{i}, \mathbf{s}_{i}, \mathbf{R}_{i})$ 由中心坐标、尺寸和旋转矩阵表示，相机 $\mathcal{C} = (\mathbf{R}_{c}, \mathbf{t}_{c}, K)$ 则由旋转、平移和内参矩阵定义。通过投影方程 $\tilde{\mathbf{p}}_{i} = \pi(K(\mathbf{R}_{c}\mathbf{p}_{i} + \mathbf{t}_{c}))$，3D 空间中的点被映射到图像平面，从而建立起像素与几何之间的桥梁。

在此表示之上，GSI-Bench 定义了七种定量空间操作（Table 1），包括移动、放置、旋转、容纳、视角变换、删除和缩放。这些操作通过关系约束（如 $\mathbf{c}_{\mathrm{cup}}' = \mathbf{c}_{\mathrm{plate}} + \Delta_{\mathrm{left}}$）将语言指令转化为具体的 3D 几何变换，确保操作具有物理可解释性。

### 基准构建双分支流水线

GSI-Bench 由两个互补的数据集构成，分别对应合成域和真实域，共享统一的场景处理、操作生成与验证框架（Figure 2）：

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/003_Figure_2.jpg]]
*Figure 2: Benchmark curation pipeline.The pipeline builds both synthetic (GSI-Syn) and real-world (GSI-Real) benchmarks through unified scene processing, action generation, and validation. For GSI-Syn, scenes are sampled from diverse viewpoints, feasible actions are generated via 3D geometric checks, and a simulator validates outcomes before filtering failures and anomalies. For GSI-Real, clear frames are selected, 3D scene structure is reconstructed, and spatial operations are generated and validated on bounding boxes. Human review then refines captions and corrects residual annotation errors, ensuring high-quality spatial-editing supervision*

**GSI-Syn（合成分支）** 基于 AI2-THOR 和 Mesa-Task 等开源模拟器构建。流水线首先通过 DBSCAN 聚类将室内平面图划分为独立房间，并在每个房间内进行最大分散视点采样，确保视点多样性且包含可操作物体。随后，系统在 3D 场景中随机选择物体并生成候选空间操作，通过几何检查验证物理可行性后在模拟器中执行。操作成功与否通过比较理想状态与实际结果判定，失败则回滚重采样。最后，经过两阶段过滤：先用实例分割掩码去除像素级变化过小的样本，再调用 Qwen3-VL-235B 作为 MLLM 质量门控，剔除模拟瑕疵、不合理遮挡等异常样本。

**GSI-Real（真实分支）** 基于 ScanNet++ 真实场景数据构建。流水线首先选取清晰帧，利用 DetAny3D 重构 3D 场景结构，并在物体边界框上生成移动、旋转、删除等候选操作。每个样本以五元组 $(\mathcal{I}, \mathcal{T}, \mathcal{S}_{\mathrm{src}}, \Phi_{3\mathrm{D}}, \mathcal{S}_{\mathrm{dst}})$ 表示，包含原始图像、指令、源场景、3D 变换和目标场景。随后，MLLM 承担三重角色：识别并丢弃物理上不可行的操作、修正标注错误、生成多样化的自然语言指令。最后通过人工审核修正残余错误，确保高质量的空间编辑监督信号。

### 多维度自动化评估协议

GSI-Bench 的评估不依赖参考编辑图像，而是从四个维度自动量化模型的空间智能表现：**指令遵守**（Instruction Compliance, IC）衡量编辑结果是否忠实执行了文本指令；**空间准确性**（Spatial Accuracy, SA）评估物体位移、旋转等几何变换的精确程度；**外观一致性**（Appearance Consistency, AC）检查非编辑区域的视觉保真度；**编辑局部性**（Edit Locality, EL）通过 $100(1 - \mathrm{LPIPS})$ 计算非目标区域的 LPIPS 分数，确保编辑仅影响指定区域而不扩散至无关部分。这一评估协议同时适用于合成和真实场景，为空间编辑能力提供了细粒度的诊断工具。

### 生成式空间智能增强方法

在基准之外，GSI-Syn 同时作为训练数据，用于验证“以生成促理解”的核心假设。方法以统一多模态模型 **BAGEL**（Deng et al., arXiv 2025）为基础，该模型原生支持图像编辑，其感知与生成模块通过自注意力机制实现深度交互。训练集从 GSI-Syn 中采样包含移动、旋转、缩放、删除、视角变换等多样化空间操作的三元组 $(\mathcal{I}, \mathcal{T}, \mathcal{I}^{\prime})$，对 BAGEL 进行微调，迫使模型学习物理上合理的 3D 空间变换，从而内化鲁棒的空间表征。

### 补充图表

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/001_Figure_1.jpg]]
*Figure 1: We introduce GSI Bench, a benchmark for grounded spatial intelligence that spans both real-world and synthetic scenes. GSI Bench evaluates a diverse set of spatial editing skills across multiple domains. By incorporating fine-grained evaluation protocols covering instruction compliance, spatial accuracy, edit locality, and appearance consistency, GSI Bench enables rigorous assessment of spatial reasoning in image-editing models. We further show that fine-tuning with GSI-Syn significantly boosts models’ spatial understanding and generalization across all subsets of the benchmark*

## 核心模块与公式推导

### 任务形式化

GSI-Bench 将生成式空间智能操作化为**空间接地的图像编辑任务**。给定输入图像 $\mathcal{I}$ 和明确的文本空间指令 $\mathcal{T}$，统一多模态模型 $f$ 需生成经过物理合理空间变换后的输出图像 $\mathcal{I}^{\prime}$：

$$\mathcal{I}^{\prime} = f(\mathcal{I}, \mathcal{T})$$

为形式化七种空间操作（移动、放置、旋转、容纳、视角变换、删除、缩放，见 Table 1），每个视觉场景被建模为其潜在 3D 结构。场景 $\mathcal{S}$ 由 $N$ 个物体和相机组成：

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/002_Table_1.jpg]]
*Table 1: Spatial operation taxonomy*

$$\mathcal{S} = \{\mathcal{O}_{i}\}_{i=1}^{N} \cup \{\mathcal{C}\}$$

其中物体 $\mathcal{O}_{i}$ 由中心 $\mathbf{c}_{i}$、尺寸 $\mathbf{s}_{i}$ 和旋转 $\mathbf{R}_{i}$ 表示：

$$\mathcal{O}_{i} = (\mathbf{c}_{i}, \mathbf{s}_{i}, \mathbf{R}_{i})$$

相机 $\mathcal{C}$ 由旋转 $\mathbf{R}_{c}$、平移 $\mathbf{t}_{c}$ 和内参 $K$ 参数化：

$$\mathcal{C} = (\mathbf{R}_{c}, \mathbf{t}_{c}, K)$$

3D 点 $\mathbf{p}_{i}$ 到图像平面的投影通过标准针孔相机模型实现：

$$\tilde{\mathbf{p}}_{i} = \pi(K(\mathbf{R}_{c}\mathbf{p}_{i} + \mathbf{t}_{c}))$$

文本空间指令通过**关系约束**映射到 3D 几何变换。例如，“将杯子放在盘子左侧”被形式化为：

$$\mathbf{c}_{\mathrm{cup}}' = \mathbf{c}_{\mathrm{plate}} + \Delta_{\mathrm{left}}$$

该约束将语言指令直接转化为物体中心的定量位移，确保编辑结果在 3D 空间中物理合理。

### 合成数据生成流水线 (GSI-Syn)

GSI-Syn 构建于开源模拟器 AI2-THOR 和 Mesa-Task 之上，通过四个关键模块生成精确的 $(I, T, I')$ 三元组：

1. **室内场景初始化与视点选取**：采用 DBSCAN 聚类对平面图进行房间划分，在每个房间内进行最大分散视点采样，确保视点覆盖丰富且包含可操作物体。

2. **空间操作候选生成与几何验证**：在 3D 场景中随机选择物体，生成关系变换（如相对位移）或相机变换，并通过 3D 几何检查验证物理可行性，排除碰撞、穿透等不合理操作。

3. **模拟执行与成功校验**：在物理模拟器中执行候选动作，比较理想状态与实际结果。操作成功则保留样本，失败则回滚并重采样。

4. **后处理过滤（MLLM 质量门控）**：首先使用实例分割掩码过滤像素级变化可忽略的样本，随后调用 Qwen3-VL-235B 作为质量门控，剔除模拟瑕疵、不合理遮挡等异常样本。

### 真实场景数据生成流水线 (GSI-Real)

GSI-Real 基于 ScanNet++ 真实扫描数据构建，每个样本表示为五元组：

$$(\mathcal{I}, \mathcal{T}, \mathcal{S}_{\mathrm{src}}, \Phi_{\mathrm{3D}}, \mathcal{S}_{\mathrm{dst}})$$

包含输入图像 $\mathcal{I}$、空间指令 $\mathcal{T}$、源场景 $\mathcal{S}_{\mathrm{src}}$、3D 变换 $\Phi_{\mathrm{3D}}$ 和目标场景 $\mathcal{S}_{\mathrm{dst}}$。流水线核心模块包括：

1. **3D 重构与操作生成**：选取清晰帧，利用 DetAny3D 重构 3D 场景结构，生成移动、旋转、删除等候选空间操作。

2. **可视化验证与 MLLM 辅助**：将原始与变换后的物体边界框投影到图像平面，MLLM 负责三方面工作：(1) 识别并丢弃物理不可行的操作；(2) 修正标注错误；(3) 生成多样化的文本指令。

### 多维度自动化评估协议

评估协议包含四个维度，无需参考真实编辑图像：

- **指令遵守 (IC)**：评估生成图像是否忠实执行了文本空间指令。
- **空间准确性 (SA)**：衡量物体空间位置、姿态变换的精确程度。
- **外观一致性 (AC)**：评估非目标区域的外观保持程度。
- **编辑局部性 (EL)**：通过非目标区域的 LPIPS 距离计算，分数为 $100(1 - \mathrm{LPIPS})$，衡量编辑是否仅影响目标区域而不扩散到无关区域。

### 微调设置

实验选择 BAGEL（Deng et al., arXiv 2025）作为基础模型，该模型原生支持图像编辑，并通过自注意力机制实现感知与生成模块的深度交互。训练集从 GSI-Syn 中构建，涵盖移动、旋转、缩放、删除、视角变换等多样化空间操作类型。

## 实验与分析

### 核心实验设置

为验证生成式空间智能训练的有效性，作者以统一多模态模型 **BAGEL**（Deng et al., arXiv 2025）作为基座模型。BAGEL 原生支持图像编辑，并通过自注意力机制实现感知与生成模块的深度交互。训练数据从 GSI-Syn 中构建，涵盖移动、放置、旋转、容纳、视角变换、删除、缩放等七种空间操作（Section 6）。对比基线包括统一模型 **Emu3.5**（Cui et al., arXiv 2025）、开源统一模型 **JanusPro**，以及闭源商用模型 **GPT-img**（Hurst et al., arXiv 2024）和 **Nano Banana**（Comanici et al., arXiv 2025）。

### GSI-Bench 主结果

表 2 报告了各模型在 GSI-Bench 三个子集上的四维评估结果（指令遵守 IC、空间准确性 SA、外观一致性 AC、编辑局部性 EL）。

在合成基准 **GSI-Syn-Room** 上，经 GSI-Syn 微调的 BAGEL+ 相比原始 BAGEL 平均分提升 **+22.15**，达到所有开源模型中的最优水平，验证了合成空间编辑训练对空间操作能力的直接强化效应（Table 2, confidence 0.98）。

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on the proposed GSI-Bench across three datasets and four spatial reasoning dimensions: Instruction Compliance (IC), Spatial Accuracy (SA), Appearance Consistency (AC), and Edit Locality (EL). Higher is better*

在真实场景基准 **GSI-Real** 上，Emu3.5 在开源模型中取得最佳平均分 43.52，而 BAGEL 原始得分为 28.46。经 GSI-Syn 微调后，BAGEL+ 提升至 **36.28**，增益 **+7.83** 分（Section 6.3, confidence 0.95）。这一跨域提升表明合成数据训练带来的空间编辑能力具有较好的现实泛化性。值得注意的是，BAGEL+ 在真实场景上的表现仍与 Emu3.5 存在差距，说明合成到真实的域间隙尚未完全弥合。

在桌面级合成基准 **GSI-Syn-Table** 上，商用模型 Nano Banana 和 GPT-img 分别取得 37.03 和 33.97 的平均分（Table 2, confidence 0.98），反映出闭源模型在精细空间编辑任务上的既有优势。

### 下游空间理解迁移

为验证“以生成促理解”的核心假设，作者在两组空间理解基准上评估了微调前后 BAGEL 的表现。

在 **OmniSpatial** 基准上，BAGEL+ 的整体准确率从 41.55 提升至 **42.07**，增益 +0.52 个百分点（Table 3, confidence 0.95）。提升主要集中在空间交互（Spatial Interaction）和视角采择（Perspective Taking）维度，说明生成式空间编辑训练对涉及物体间关系和视角推理的理解子任务具有选择性增强效应。

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/005_Table_3.jpg]]
*Table 3: Evaluation on OmniSpatial benchmark. We report accuracy (%) across four core reasoning dimensions. Fine-tuning on GSI-Syn improves spatial understanding, particularly in Spatial Interaction and Perspective Taking. Best results among opensource 7B models are bolded. †Proprietary models*

在 **SAT-Real** 基准上，BAGEL+ 的整体准确率从 65.33 提升至 **69.33**，增益 **+4.00** 个百分点（Table 4, confidence 0.95）。其中目标导向理解（goal-directed understanding）和自我中心理解（egocentric understanding）维度提升尤为显著，进一步支持了生成训练内化空间表征并迁移至理解任务的因果链条。

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/006_Table_4.jpg]]
*Table 4: Evaluation on SAT-Real benchmark [24]. Accuracy (%) across five spatial reasoning dimensions. Fine-tuning with GSI-Syn notably improves goal-directed and egocentric understanding. Best results among open-source 7B models are bolded*

### 定性分析与操作难度差异

定性结果揭示了不同空间操作类型的难度分化。大多数模型在**空间删除（SR）**操作上表现优于移动、放置或旋转等操作（Figure 3, confidence 0.9）。这一现象的可能解释是：删除操作仅需从场景中移除物体并填充背景，对模型的空间推理和几何变换能力要求较低；而移动、放置等操作要求模型同时理解源位置与目标位置的三维空间关系，并保持物体外观一致性，难度显著更高。

![[assets/figures/papers/paper_list_l2479_https_arxiv_org_abs_2604_20570/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison of spatial editing results across five instruction types. Rows 1–2 use GSI-Real samples, Rows 3–4 use GSI-Table, and the last row uses GSI-Room. Columns show the input image, outputs from Emu3.5, BAGEL, BAGEL+(fine-tuned with GSI-Syn), and the ground-truth target. BAGEL+ demonstrates stronger spatial fidelity and better preservation of unaffected content. Further examples and corresponding metrics are provided in the appendix*

图 3 的定性对比进一步显示，BAGEL+ 在空间保真度和非目标区域内容保持方面均优于原始 BAGEL 和 Emu3.5，特别是在涉及多物体空间关系约束的复杂指令上表现更为稳健。

### 局限与失败模式

尽管结果整体积极，但以下失败模式值得关注：

1. **架构依赖**：微调实验仅基于 BAGEL 单一架构，未在 Emu3.5、Show-o 等其他统一模型上验证 GSI-Syn 训练的有效性，结论的架构泛化性尚不明确。
2. **域间隙残留**：GSI-Real 上 BAGEL+ 仍显著落后于 Emu3.5，说明合成数据训练无法完全覆盖真实场景的纹理、光照和遮挡复杂性。
3. **3D 重建精度瓶颈**：GSI-Real 的构建依赖 DetAny3D 的物体位姿估计，不准确的位姿可能导致部分标注操作在物理上不可行，进而影响训练信号质量。
4. **操作覆盖面有限**：当前基准聚焦于七种预定义室内静态操作，难以评估动态交互、遮挡推理等更复杂的空间智能维度。

### 开放性讨论

实验结果引出了若干待验证的深层问题：生成式空间训练能否在无需理解标签的情况下直接提升更复杂的全局空间推理（如路径规划、多步导航）？模型在编辑过程中是否真正建立了隐式 3D 世界模型，还是仅通过图像层次模仿实现了表面上的空间合规？这些问题指向了生成式空间智能研究的下一步方向。

## 方法谱系与知识库定位

### 与基线工作的关系

GSI-Bench 所提出的生成式空间智能增强方法，建立在统一多模态模型（unified multimodal model）的图像编辑能力之上。其核心基线为 **BAGEL**（Deng et al., arXiv 2025），该模型原生支持图像编辑，并通过自注意力机制实现感知模块与生成模块之间的深层交互。本文选择 BAGEL 作为微调基座，正是利用了这一统一的感知-生成架构，使空间编辑训练能够同时影响模型的视觉理解与图像生成能力。

在空间编辑任务的横向对比中，GSI-Bench 还引入了多个具有代表性的基线模型：

- **Emu3.5**（Cui et al., arXiv 2025）：同为统一多模态模型，在 GSI-Real 真实场景编辑上取得了开源模型中最优的平均分（43.52），表明其具备较强的空间编辑基础能力。
- **GPT-img**（Hurst et al., arXiv 2024）与 **Nano Banana**（Comanici et al., arXiv 2025）：作为闭源商用生成模型，在 GSI-Syn-Table 合成基准上分别达到 33.97 和 37.03 的平均分，代表了当前商用系统的空间编辑水平。
- **JanusPro**：开源统一模型，作为补充对比基线。

从方法谱系来看，本文的工作区别于上述模型的关键在于：**不依赖更大规模的预训练或更强的架构设计，而是通过构建精确的合成空间编辑数据（GSI-Syn）进行针对性微调，迫使模型内化 3D 空间变换规律**。这一思路与传统的“理解驱动”空间智能研究形成互补——后者通常依赖空间 VQA 或关系推理等理解任务来评估和改进模型，而本文则从生成视角切入，以编辑合规性为训练信号。

### 适用边界与条件

本方法的有效性建立在以下关键条件之上：

1. **统一多模态架构依赖**：微调实验仅基于 BAGEL 单一架构完成。BAGEL 的自注意力机制使感知与生成模块深度耦合，这是空间编辑训练能够同时提升理解能力的重要结构前提。对于感知与生成模块解耦的架构，GSI-Syn 训练是否能产生同等的理解迁移效果，尚需验证。

2. **合成数据质量与多样性**：GSI-Syn 的构建依赖于 AI2-THOR 和 Mesa-Task 两个开源模拟器。这些模拟器提供了可控的室内场景与物理交互，但其环境多样性和物理真实度有限。当目标应用场景显著偏离模拟器覆盖的室内家居环境时（如室外场景、工业场景），模型的泛化能力可能受限。

3. **真实场景的 3D 重建精度**：GSI-Real 的真实场景操作生成依赖于 DetAny3D 进行 3D 场景重构。不准确的物体位姿估计可能导致部分空间操作在实际中不可行，进而影响训练数据的质量。

4. **操作类型覆盖**：基准目前聚焦于七种预定义空间操作（移动、放置、旋转、容纳、视角变换、删除、缩放），主要面向室内静态场景。对于动态交互、遮挡推理、多步序列操作等更复杂的空间智能维度，该方法尚未覆盖。

### 局限与开放问题

**已识别的局限：**

1. **架构泛化性未验证**：微调实验仅基于 BAGEL 单一架构，未在其他统一多模态模型（如 Emu3.5、Show-o）上验证 GSI-Syn 训练的有效性。BAGEL 的特定设计（如自注意力耦合）是否构成方法成功的关键因素，尚不明确。

2. **合成到真实的域间隙**：尽管实验表明 GSI-Syn 微调在 GSI-Real 上带来了 +7.83 的平均分增益，但合成场景的物理真实度有限，可能限制模型在更复杂真实场景中的表现。如何更有效地弥合这一域间隙，是方法规模化应用的关键瓶颈。

3. **场景与操作覆盖有限**：当前基准聚焦于室内静态场景与预定义操作，难以涵盖动态交互、遮挡推理、路径规划等更复杂的空间智能维度。

**开放问题：**

1. **生成能否直接提升复杂空间推理？** 实验已证明生成式空间编辑训练可迁移至空间理解任务（OmniSpatial +0.52，SAT-Real +4.00），但这种迁移能否延伸到更复杂的全局空间推理（如路径规划、多步导航），仍需探索。

2. **模型是否建立了隐式 3D 世界模型？** 在生成编辑过程中，模型究竟是通过图像层次的模式模仿实现了表面上的空间合规，还是真正内化了隐式的 3D 世界表征？这一问题关乎方法的根本有效性，需要更深入的机制分析。

3. **架构迁移的可行性**：该方法能否无缝迁移到其他统一多模态架构，并在更大规模模型上表现出一致性？这决定了 GSI-Syn 训练策略是否具有普适的工具价值。

4. **向动态场景与具身智能的扩展**：如何将生成式空间智能从静态图像编辑扩展到动态场景和交互任务，实现与具身智能的更紧密连接，是该方法走向实际应用的重要方向。

5. **合成到真实域间隙的系统性弥合**：除增强 3D 重建精度外，域随机化、真实场景增强等策略是否能进一步缩小域间隙，值得系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Exploring_Spatial_Intelligence_from_a_Generative_Perspective.pdf]]
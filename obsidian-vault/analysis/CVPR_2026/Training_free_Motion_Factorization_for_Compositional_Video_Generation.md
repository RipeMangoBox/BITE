---
title: Training-free Motion Factorization for Compositional Video Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Training_free_Motion_Factorization_for_Compositional_Video_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Training-free_Motion_Factorization_for_Compositional_Video_Generation_CVPR_2026_paper.html
project_link: null
code_link: https://github.com/ZixuanWang0525/MF-CVG
aliases:
- MFCVGMC
- TFMFCVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 将场景运动因子分解为三个基本类别（静止、刚体、非刚体），并基于结构化运动图进行规划，再通过类别特定的解耦引导分支生成各实例运动。
primary_logic: 将复杂运动分解为三个基本类别，通过结构化运动图推理消除语义歧义，并设计三类解耦引导（外观一致性、几何不变性、空间形变）实现多样且一致的运动生成，无需额外训练即可大幅提升组合式视频生成质量。
claims:
- 在 VideoCrafter-v2.0 架构上，将 Subject Consistency 从 91.00% 提升至 98.27%（对比 R&P 基线）。
- 非刚体运动引导（SDG）使 Dynamic Degree 获得 27.81% 的增益，表明解耦引导对运动多样性的关键作用。
- 逐步引入各引导分支（RCG、GIG、SDG）使所有指标持续提升，验证了每个组件的贡献。
- CVGBench-m 上 Subject Consistency (%) = 98.27
---

# Training-free Motion Factorization for Compositional Video Generation

> [!tip] 核心洞察
> 将复杂运动分解为三个基本类别，通过结构化运动图推理消除语义歧义，并设计三类解耦引导（外观一致性、几何不变性、空间形变）实现多样且一致的运动生成，无需额外训练即可大幅提升组合式视频生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需训练的运动分解用于组合式视频生成 |
| 英文题名 | Training-free Motion Factorization for Compositional Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Training-free_Motion_Factorization_for_Compositional_Video_Generation_CVPR_2026_paper.html) · [Code](https://github.com/ZixuanWang0525/MF-CVG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Motion Factorization for Compositional Video Generation (MF-CVG) |
| Dataset | CVGBench-m, CVGBench-p |

> [!tip] 效果简介
> - CVGBench-m 上，Subject Consistency (%) 98.27 vs 91.00 (+7.27)；Dynamic Degree (%) 96.00 vs 91.02 (+4.98)。
> - CVGBench-p 上，Subject Consistency (%) 98.81 vs N/A (N/A)。

## 概要

### 问题瓶颈

组合式视频生成（Compositional Video Generation, CVG）旨在根据文本描述生成包含多个实例且运动各异的视频。现有方法主要聚焦于语义绑定——即确保文本中的每个实例出现在正确的位置——却忽略了对提示中不同**运动类别**的理解。这导致一个关键瓶颈：不同实例的运动模式趋于雷同，缺乏应有的多样性。例如，提示中要求“一只猫在奔跑，一个球在滚动”，现有方法可能将两者都生成为相似的刚性平移，而非区分猫的非刚体运动与球的刚体滚动。

### 核心方法

本文提出**无需训练的运动分解框架 MF-CVG（Motion Factorization for Compositional Video Generation）**，将场景运动因子分解为三个基本类别——**静止、刚体运动、非刚体运动**——并为每个实例唯一分配一个类别。框架包含两个核心模块：

- **结构化运动推理（Structured Motion Reasoning, SMR）**：从用户提示构建运动图，以节点表示实例及其运动属性，以有向边编码实例间的交互关系；基于该图推理运动规律，为每个实例生成差异化的时空边界框布局。
- **解耦运动引导（Disentangled Motion Guidance, DMG）**：针对三类运动设计三个独立的引导分支——**参考条件引导（RCG）** 增强静止实例的跨帧外观一致性，**几何不变性引导（GIG）** 保持刚体实例的几何不变性，**空间形变引导（SDG）** 捕捉非刚体实例的复杂形变。

该方法无需额外训练，可直接作用于预训练视频扩散模型（如 VideoCrafter-v2.0 的 3D U-Net 架构和 CogVideoX-2B 的 DiT 架构）。

### 方法谱系与知识库定位

MF-CVG 属于**训练自由的组合式视频生成方法**，区别于需要微调或额外训练的 CVG 方案。与 **R&P**（区域与边界感知的文本到图像/视频生成）、**VideoTetris**（基于框引导的组合式视频生成）和 **LVD**（LLM 引导的视频扩散模型）等基线相比，MF-CVG 的关键差异在于**显式建模运动类别**并设计**类别特定的解耦引导**，而非采用统一的扩散引导策略。

### 核心结论

在 CVGBench-m 和 CVGBench-p 两个基准上的实验表明：
- 相较 R&P 基线，MF-CVG 将 Subject Consistency 从 91.00% 提升至 **98.27%**，Dynamic Degree 从 91.02% 提升至 **96.00%**。
- 消融实验证实，逐步引入 RCG、GIG、SDG 三个引导分支使所有指标持续提升，其中 SDG 单独贡献了 **27.81%** 的动态程度增益，验证了非刚体运动引导对运动多样性的关键作用。
- 更强的语言模型骨干（LLaMA-3.3-70B 对比 LLaMA-3.1-8B）能更准确地推理运动规律，进一步提升生成质量。

### 局限与开放问题

当前方法假设视点固定，未考虑相机位姿变化，限制了全局视点改变的动态场景建模。此外，当小物体的边界框过小时，运动引导不足，生成质量下降。未来的方向包括结合相机位姿实现全局视点变化，以及提升小目标运动生成的鲁棒性。

### 问题背景：组合式视频生成中的运动多样性缺失

组合式视频生成（Compositional Video Generation, CVG）旨在根据文本提示同时生成多个实例及其交互运动，是视频生成领域的前沿方向。现有CVG方法——如 **VideoTetris**、**LVD** 和 **R&P**——主要聚焦于**语义绑定**（semantic binding），即确保每个文本实体与正确的视觉实例对应，并通过边界框或区域引导实现空间布局控制。然而，这些方法普遍采用统一的扩散引导范式，**不区分不同实例的运动类别**，导致生成的实例运动模式趋于雷同。

问题的本质在于：真实场景中，不同实例的运动特性存在根本性差异——一片飘落的树叶（非刚体形变）、一辆匀速行驶的汽车（刚体平移）和一栋静止的建筑（无运动）需要截然不同的生成约束。现有方法将所有这些运动类型混为一谈，用相同的引导策略处理，自然无法产生多样化的运动表现。

### 核心瓶颈：缺乏运动类别的理解与分解

当前CVG方法的根本瓶颈在于**忽略了对提示中不同运动类别的理解**。具体表现为：

1. **运动表示模糊**：现有方法直接从用户提示中推断边界框序列，缺乏对运动规律的结构化推理。当提示描述复杂场景时（如“一只猫在追逐飘动的蝴蝶”），模型难以区分猫的刚体运动与蝴蝶的非刚体运动。

2. **引导策略单一**：无论实例是静止、平移还是形变，都采用相同的扩散引导机制。这种“一刀切”的策略使得静止实例可能出现外观漂移，刚体实例可能发生形状扭曲，而非刚体实例的复杂形变则完全无法捕捉。

3. **运动多样性受限**：由于缺乏类别特定的约束，生成结果中不同实例的运动往往趋同，无法体现真实世界中运动模式的丰富性。

### 本文动机：运动因子分解与解耦引导

针对上述瓶颈，本文提出核心洞察：**将复杂场景运动分解为三个基本类别——静止（motionlessness）、刚体运动（rigid motion）和非刚体运动（non-rigid motion）——并通过结构化推理消除语义歧义，再为每个类别设计专用的解耦引导分支**。

这一思路的合理性在于：三类运动在物理约束上存在本质差异。静止实例需要最大化跨帧外观一致性；刚体实例需要保持几何形状不变，仅允许位置变化；非刚体实例则需要建模复杂的像素级形变。通过将运动因子分解，可以为每类运动施加恰当的约束，从而在无需额外训练的前提下，大幅提升组合式视频生成的质量与多样性。

## 核心方法与创新机理

现有组合式视频生成（CVG）方法普遍关注语义绑定，却忽略了对提示中不同运动类别的理解，导致不同实例的运动模式趋于雷同——这是当前CVG系统在运动多样性上的核心瓶颈。MF-CVG 通过三个相互耦合的创新点从根本上解决了这一问题。

**1. 运动因子分解：将场景运动拆解为三个基本类别**

首次将复杂场景运动显式分解为三个基本类别：静止（motionlessness）、刚体运动（rigid motion）和非刚体运动（non-rigid motion），每个实例被唯一分配到一个运动类别。这一分解并非简单的分类标签，而是为后续的差异化运动规划与引导提供了结构化前提。与此相对，R&P、VideoTetris 等基线方法采用统一的扩散引导，不区分运动类型，本质上将所有实例的运动视为同质过程。

**2. 结构化运动推理（SMR）：从运动图到时空布局的推理链**

不直接从用户提示推断边界框序列，而是构建一个**结构化运动图**（structured motion graph）作为中间表示。图中节点代表实例及其运动属性与类别标签，有向边编码实例间的交互关系。基于该运动图，利用大语言模型（LLaMA-v3.3-70B）推理运动规律，生成各实例的时空布局：

$$\{ B_{1}, B_{2}, \dots, B_{F} \} = \mathrm{LLM}( \mathcal{R}; C )$$

对于刚体实例，边界框更新遵循物理运动学：

$$\boldsymbol{B}_{f}(\boldsymbol{v}_{n}) = \boldsymbol{B}_{f-1}(\boldsymbol{v}_{n}) + \vec{u}_{\boldsymbol{v}_{n}} + \frac{1}{2} \vec{a}_{\boldsymbol{v}_{n}}$$

这一推理链消除了直接从提示生成布局时的语义歧义，使运动规划具备因果可解释性。

**3. 解耦运动引导（DMG）：类别特定的三支引导分支**

针对三个运动类别设计了三类解耦引导，分别作用于扩散模型的去噪过程：

- **参考条件引导（RCG）**：对静止实例，强制每帧仅与选定的参考帧交互，以增强跨帧外观一致性。参考帧通过最小化特征差异选取：
  
  $$f^{*} = \arg\min_f \sum_{f'=1}^F D(\varphi(\mathbf{z}_f^t), \varphi(\mathbf{z}_{f'}^t))$$

- **几何不变性引导（GIG）**：对刚体运动实例，限制前景跨帧交互仅在形状对齐区域内，保持几何结构不变。

- **空间形变引导（SDG）**：对非刚体运动实例，通过感知形变与边界框诱导形变之差调节跨帧相关性，惩罚因子为：
  
  $$\Lambda[i,j] = \exp(-\alpha \cdot (\mathcal{D}_{\mathrm{perc}}[i,j] - \mathcal{D}_{\mathrm{box}}[i,j])) + 1$$

三类引导通过统一的形式注入扩散过程——在3D U-Net架构中作为损失梯度更新视频嵌入，在DiT架构中直接修改注意力分数：

$$\mathbf{A} = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top} (1 + \beta \odot (\mathcal{G}_{\mathrm{m}} + \mathcal{G}_{\mathrm{r}} + \mathcal{G}_{\mathrm{nr}}))}{\sqrt{d}} \right)$$

**创新点的协同效应**：三个 changed slots 形成因果链条——运动类别分解（slot 3）为运动图推理提供语义基础（slot 1），推理得到的时空布局为解耦引导提供空间约束（slot 2）。消融实验证实了这一协同关系：逐步引入RCG、GIG、SDG使所有指标持续提升，其中SDG单独贡献了27.81%的动态程度增益，而更强的LLM骨干（LLaMA-3.3-70B vs LLaMA-3.1-8B）将Subject Consistency从97.55%提升至98.40%，Dynamic Degree从75.34%提升至82.21%。

**关键优势**：整个框架无需额外训练，仅通过推理阶段的运动规划与扩散引导即可显著提升组合式视频生成质量。在VideoCrafter-v2.0架构上，Subject Consistency从91.00%跃升至98.27%（对比R&P基线），Background Consistency从90.85%提升至97.73%，充分验证了运动因子分解范式的有效性。

MF-CVG（Motion Factorization for Compositional Video Generation）采用**运动规划–运动生成**两阶段范式，将组合式视频生成中的复杂场景动态分解为三个基本运动类别（静止、刚体、非刚体），并通过解耦引导实现多样且一致的运动合成。

### 两阶段流水线

整个框架的输入为用户文本提示，输出为包含多实例差异化运动的视频。流水线由两个核心模块串联构成：

1. **结构化运动推理（Structured Motion Reasoning, SMR）**：从用户提示中构建运动图，推理各实例的运动类别与时空变化规律，生成结构化的时空布局（即每帧每个实例的边界框序列）。
2. **解耦运动引导（Disentangled Motion Guidance, DMG）**：基于 SMR 输出的时空布局，对预训练视频扩散模型的去噪过程施加类别特定的引导约束，分别控制静止实例的外观一致性、刚体实例的几何不变性，以及非刚体实例的空间形变，最终合成包含多样化运动的连贯视频。

### 输入输出流

```
用户提示 → SMR → 时空布局 {B₁, B₂, ..., B_F} → DMG → 视频帧序列
```

**SMR 阶段**：首先利用大语言模型将用户提示解析为结构化运动图 $\mathcal{R} = (\mathcal{V}, \mathcal{E})$，其中节点 $\mathcal{V}$ 表示场景中的实例（标注运动类别、外观属性等），有向边 $\mathcal{E}$ 编码实例间的交互关系。随后，LLM 基于该运动图和原始提示推理生成时空布局：

$$\{ B_{1}, B_{2}, \dots, B_{F} \} = \mathrm{LLM}( \mathcal{R}; C )$$

其中 $C$ 为用户提示，$F$ 为总帧数。对于刚体实例，其边界框序列按运动学规律更新：

$$\boldsymbol{B}_{f}(\boldsymbol{v}_{n}) = \boldsymbol{B}_{f-1}(\boldsymbol{v}_{n}) + \vec{u}_{\boldsymbol{v}_{n}} + \frac{1}{2} \vec{a}_{\boldsymbol{v}_{n}}$$

其中 $\vec{u}_{\boldsymbol{v}_{n}}$ 和 $\vec{a}_{\boldsymbol{v}_{n}}$ 分别为实例 $\boldsymbol{v}_{n}$ 的速度和加速度。

**DMG 阶段**：将 SMR 生成的时空布局注入预训练视频扩散模型的去噪过程。对于 3D U-Net 架构（如 VideoCrafter-v2.0），通过梯度更新视频嵌入：

$$\mathbf{z}_{1:F}^{t-1} = \mathbf{z}_{1:F}^{t} - \nabla \mathcal{L}$$

其中引导损失 $\mathcal{L}$ 基于注意力图 $\mathbf{A}$ 和三类运动引导掩码计算：

$$\mathcal{L} = 1 - \frac{\beta}{P} \sum ( \mathbf{A} \odot ( \mathcal{G}_{\mathrm{m}} + \mathcal{G}_{\mathrm{r}} + \mathcal{G}_{\mathrm{nr}} ) )$$

对于 DiT 架构（如 CogVideoX-2B），则直接将引导掩码注入注意力分数：

$$\mathbf{A} = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top} (1 + \beta \odot (\mathcal{G}_{\mathrm{m}} + \mathcal{G}_{\mathrm{r}} + \mathcal{G}_{\mathrm{nr}}))}{\sqrt{d}} \right)$$

### 三类运动引导分支

DMG 模块包含三个解耦的引导分支，分别对应三种运动类别：

- **参考条件引导（Reference Conditioned Guidance, RCG）**：针对静止实例，强制每帧仅与选定的参考帧交互，以保持跨帧外观一致性。参考帧通过最小化帧间特征差异选取：$f^{*} = \arg\min_f \sum_{f'=1}^F D(\varphi(\mathbf{z}_f^t), \varphi(\mathbf{z}_{f'}^t))$。

- **几何不变性引导（Geometric Invariance Guidance, GIG）**：针对刚体实例，将跨帧注意力限制在形状对齐区域内，保持几何结构不变。

- **空间形变引导（Spatial Deformation Guidance, SDG）**：针对非刚体实例，通过形变惩罚因子 $\Lambda[i,j] = \exp(-\alpha \cdot (\mathcal{D}_{\mathrm{perc}}[i,j] - \mathcal{D}_{\mathrm{box}}[i,j])) + 1$ 调节跨帧相关性，最小化感知形变与边界框诱导形变之间的差异。

### 关键设计原则

整个框架的核心设计原则是**运动类别先解耦、后组合**：SMR 模块在规划阶段为每个实例分配唯一的运动类别，消除语义歧义；DMG 模块在生成阶段针对不同类别施加差异化约束，确保各实例运动既独立又协调。该方法无需额外训练，可直接适配 3D U-Net 和 DiT 两类主流视频扩散架构。

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Training_free_Mot/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our motion factorization framework. First, for each instance belonging to a particular motion category, our framework infers its per-frame changes in shape and position from a structured motion graph (Sec. 3.2). Second, conditioned on the motion category, dedicated guidance branches synthesize per-instance motions, which are subsequently composed into a coherent scene (Sec. 3.3)*

### 3.1 整体框架：两阶段运动因子分解

MF-CVG 将组合式视频生成分解为**规划**与**生成**两个阶段。给定用户提示 $C$，框架首先通过结构化运动推理（SMR）模块生成时空布局——即每个实例在各帧的边界框序列：

$$\{ B_{1}, B_{2}, \dots, B_{F} \} = \mathrm{LLM}( \mathcal{R}; C ) \tag{1}$$

其中 $\mathcal{R}$ 为从提示构建的结构化运动图，$F$ 为总帧数。随后，解耦运动引导（DMG）模块依据每个实例的运动类别（静止、刚体、非刚体），将类别特定的引导信号注入预训练视频扩散模型的去噪过程。

对于 **3D U-Net** 架构（如 VideoCrafter-v2.0），引导通过梯度更新视频嵌入实现：

$$\mathbf{z}_{1:F}^{t-1} = \mathbf{z}_{1:F}^{t} - \nabla \mathcal{L} \tag{2}$$

其中引导损失 $\mathcal{L}$ 基于注意力图 $\mathbf{A}$ 与三类运动引导掩码的加权和计算：

$$\mathcal{L} = 1 - \frac{\beta}{P} \sum ( \mathbf{A} \odot ( \mathcal{G}_{\mathrm{m}} + \mathcal{G}_{\mathrm{r}} + \mathcal{G}_{\mathrm{nr}} ) ) \tag{3}$$

对于 **DiT** 架构（如 CogVideoX-2B），引导直接注入注意力分数：

$$\mathbf{A} = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top} (1 + \beta \odot (\mathcal{G}_{\mathrm{m}} + \mathcal{G}_{\mathrm{r}} + \mathcal{G}_{\mathrm{nr}}))}{\sqrt{d}} \right) \tag{4}$$

其中 $\mathcal{G}_{\mathrm{m}}$、$\mathcal{G}_{\mathrm{r}}$、$\mathcal{G}_{\mathrm{nr}}$ 分别为静止、刚体、非刚体运动的引导掩码，$\beta$ 为引导强度系数。

---

### 3.2 结构化运动推理（SMR）

SMR 模块的核心创新在于**以结构化运动图替代直接的提示到布局映射**，从而消除语义歧义并推理运动规律。

**运动图构建**：从用户提示中提取实例及其交互关系，构建有向图 $\mathcal{R} = (V, E)$。节点 $V$ 代表场景实例，标注运动类别（静止/刚体/非刚体）及外观属性；有向边 $E$ 编码实例间的空间关系与运动交互约束。

**时空布局生成**：对于刚体运动实例，边界框序列通过运动学更新生成：

$$\boldsymbol{B}_{f}(\boldsymbol{v}_{n}) = \boldsymbol{B}_{f-1}(\boldsymbol{v}_{n}) + \vec{u}_{\boldsymbol{v}_{n}} + \frac{1}{2} \vec{a}_{\boldsymbol{v}_{n}} \tag{5}$$

其中 $\vec{u}_{\boldsymbol{v}_{n}}$ 和 $\vec{a}_{\boldsymbol{v}_{n}}$ 分别为实例 $\boldsymbol{v}_{n}$ 的速度与加速度，由 LLM 从运动图的交互边中推理得出。更一般地，边界框更新可写为：

$$B_f(v_n) = B_{f-1}(v_n) + \Delta_f(v_n) \tag{6}$$

其中 $\Delta_f(v_n)$ 为运动图推理得到的帧间位移向量。

---

### 3.3 解耦运动引导（DMG）

DMG 模块针对三种运动类别设计了三类独立的引导分支，这是本文实现运动多样性的**因果调节旋钮**。

#### 3.3.1 参考条件引导（RCG）——静止实例

对于静止实例，核心约束是跨帧外观一致性。RCG 首先选择特征差异最小的帧作为参考帧：

$$f^{*} = \arg\min_f \sum_{f'=1}^F D(\varphi(\mathbf{z}_f^t), \varphi(\mathbf{z}_{f'}^t)) \tag{7}$$

其中 $\varphi(\cdot)$ 为特征提取器，$D(\cdot, \cdot)$ 为距离度量。随后强制所有帧仅与参考帧 $f^{*}$ 进行跨帧注意力交互，从而抑制无关运动漂移，保持静止实例的外观稳定。

#### 3.3.2 几何不变性引导（GIG）——刚体运动实例

刚体运动要求实例在平移/旋转过程中保持几何形状不变。GIG 将跨帧注意力限制在**形状对齐区域**内：对于实例 $\boldsymbol{v}_n$，其前景掩码经边界框诱导的几何变换对齐后，仅允许对齐区域内的像素进行跨帧交互。这确保了旋转和平移不会引入非预期的形变。

#### 3.3.3 空间形变引导（SDG）——非刚体运动实例

非刚体运动（如动物奔跑、衣物飘动）涉及复杂的局部形变，是现有方法的主要失败模式。SDG 的核心机制是通过**形变惩罚因子** $\Lambda[i,j]$ 调节跨帧相关性：

$$\Lambda[i,j] = \exp(-\alpha \cdot (\mathcal{D}_{\mathrm{perc}}[i,j] - \mathcal{D}_{\mathrm{box}}[i,j])) + 1 \tag{15}$$

其中 $\mathcal{D}_{\mathrm{perc}}[i,j]$ 为像素 $i$ 与 $j$ 间的感知特征距离，$\mathcal{D}_{\mathrm{box}}[i,j]$ 为边界框诱导的刚性位移距离。该因子的作用机制是：当感知形变与刚性位移一致时（$\mathcal{D}_{\mathrm{perc}} \approx \mathcal{D}_{\mathrm{box}}$），$\Lambda \approx 2$，增强跨帧交互；当感知形变显著偏离刚性位移时，$\Lambda \rightarrow 1$，退化为普通注意力。这使模型能自适应地捕捉非刚体形变。

SDG 的前景掩码通过 k-means 聚类获得，最终引导掩码为：

$$\mathcal{G}_{\mathrm{nr}} = ( \mathcal{M}(v_n) \cdot \mathcal{M}(v_n)^{\top} ) \odot \mathbf{1} \tag{16}$$

其中 $\mathcal{M}(v_n)$ 为实例 $v_n$ 的前景掩码矩阵。

---

### 3.4 模块间因果链路

三个引导分支的**递进消融实验**（Table 3）验证了其因果贡献：逐步加入 RCG、GIG、SDG 使所有评估指标持续提升。其中 SDG 单独贡献了 **+27.81%** 的动态程度增益，证明非刚体引导是解决运动多样性瓶颈的关键组件。LLaMA-3.3-70B 相比 LLaMA-3.1-8B 将动态程度从 75.34% 提升至 82.21%（Table 2），表明更强的运动图推理能力直接转化为更准确的时空布局生成。

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Training_free_Mot/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Structured Motion Reasoning (SMR) module ( Sec. 3.2). (a) Given a user prompt, we organize it into a motion graph describing instances and their interactions. (b) For each instance, conditioned on its motion category, we infer a bounding box sequence from graph-derived motion cues. All bounding box sequences are then composed into a coherent spatial-temporal layout*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Training_free_Mot/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Disentangled Motion Guidance (DMG) module ( Sec. 3.3). (a) For motionless instances, we enforce each frame interacts only with a designated anchor frame. (b) For rigidly moving instances, we restrict cross-frame interactions of a foreground within the shape aligned regions. (c) For instances undergoing non-rigid movements, we minimize pixel-wise discrepancies between perceptual deformations and box-induced deformations*

## 实验与关键发现

### 1. 实验设置

**基准与指标**：实验在自建的 **CVGBench-m** 和 **CVGBench-p** 两个组合式视频生成基准上评估。核心指标包括 **Subject Consistency**（主体一致性）、**Background Consistency**（背景一致性）和 **Dynamic Degree**（动态程度），分别衡量生成视频中实例外观的跨帧稳定性和运动的丰富程度。

**基线方法**：对比方法涵盖通用视频生成模型和组合式生成模型。通用模型包括 **VideoCrafter-v2.0**（3D U-Net 架构）和 **CogVideoX-2B**（DiT 架构）；组合式方法包括 **R&P**（Region-and-Boundary aware grounded generation，适配至视频）、**VideoTetris**（基于框引导的组合式生成）和 **LVD**（LLM-grounded video diffusion）。

**实现细节**：结构化运动推理模块（SMR）采用 **LLaMA-v3.3-70B** 作为骨干语言模型；解耦运动引导模块（DMG）分别应用于 VideoCrafter-v2.0 和 CogVideoX-2B 两种架构，验证方法的跨架构泛化性。

### 2. 主要结果

**跨架构的全面领先**：如表 1 所示，MF-CVG 在两种基础架构上均取得最优性能。以 VideoCrafter-v2.0 为基座时，在 CVGBench-m 上 Subject Consistency 达到 **98.40%**，Dynamic Degree 达到 **82.21%**；在 CVGBench-p 上 Subject Consistency 达到 **98.81%**，Dynamic Degree 达到 **78.24%**，均显著超越所有对比方法。

**相对基线的关键增益**：与 R&P 相比，MF-CVG 将 Subject Consistency 从 91.00% 提升至 **98.27%**（+7.27 个百分点），Background Consistency 从 90.85% 提升至 **97.73%**（+6.88 个百分点），Dynamic Degree 从 91.02% 提升至 **96.00%**（+4.98 个百分点）。这一结果表明，运动因子分解策略在保持外观一致性的同时，有效增强了运动多样性。

**跨架构鲁棒性**：在 CogVideoX-2B（DiT 架构）上同样取得最优成绩，证明了 DMG 模块中两种引导范式——3D U-Net 的梯度更新（Eq. 3）和 DiT 的注意力修改（Eq. 4）——均能有效工作。

### 3. 消融实验

**运动推理骨干网络的影响**：如表 2 所示，LLaMA-3.3-70B 相比 LLaMA-3.1-8B 将 Subject Consistency 从 97.55% 提升至 **98.40%**，Dynamic Degree 从 75.34% 提升至 **82.21%**。这表明更强的语言模型能更准确地从结构化运动图中推理运动规律，生成更合理的时空布局。

**解耦引导分支的贡献**：如表 3 所示，逐步引入三个引导分支使所有指标持续提升：
- 单独加入 **RCG**（参考条件引导）使 Subject Consistency 显著提高，验证了锚帧机制对静止实例外观一致性的关键作用；
- 加入 **GIG**（几何不变性引导）进一步提升了刚体运动的一致性；
- 加入 **SDG**（空间形变引导）带来 Dynamic Degree 的 **+27.81%** 最大增益，证明基于感知形变与边界框形变之差（Eq. 15）的非刚体引导对运动多样性的决定性贡献。

三个分支的协同作用最终实现了外观一致性与运动多样性之间的最优平衡。

### 4. 定性分析

**运动类别的差异化生成**：图 4 展示了在静止、刚体、非刚体三类运动场景下的生成对比。基线方法（VideoCrafter-v2.0 和 CogVideoX-2B）在不同实例间倾向于产生雷同的运动模式，而 MF-CVG 能够为每个实例生成符合其运动类别特征的独立运动——静止物体保持外观稳定，刚体保持几何形状不变地进行平移/旋转，非刚体则呈现自然的形变。

**复杂组合运动的生成**：图 5 展示了多类别运动组合的复杂行为，包括顺序运动、空间组合运动和关节运动。MF-CVG 能够将不同运动类别的实例组合成一个连贯的场景，体现了结构化运动图推理在消除语义歧义方面的优势。

### 5. 失败模式与局限性

**小目标运动引导不足**：如图 6 所示，当实例的边界框过小时，运动引导信号不足，导致小物体的生成质量下降。这是因为 DMG 模块的引导强度依赖于边界框区域内的注意力调制，过小的区域无法提供充分的约束信号。

**视点固定的假设**：当前方法假设相机视点固定，未考虑相机位姿变化。这限制了在需要全局视点变换的动态场景（如镜头平移、旋转）中的应用。如何处理相机运动与实例运动的解耦是未来的开放问题。

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Training_free_Mot/figures/004_Table_1.jpg]]
*Table 1: Performance comparison of cross-modal compositional video generation approaches on our CVGBench-m and CVGBench-p datasets. Best/2nd best scores are bolded/underlined. † indicates compositional generation models*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Training_free_Mot/figures/005_Figure.jpg]]
*Figure: Baseline: VideoCrafter-v2.0 (3D Unet architecture) Baseline: CogVideoX-2B (DiT architecture)*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Training_free_Mot/figures/008_Table_2.jpg]]
*Table 2: Ablation analysis of diverse backbones for motion reasoning. Best scores are bolded*

## 定位与知识库关联

### 1. 与组合式视频生成（CVG）基线的关系

**MF-CVG** 直接对标组合式视频生成（Compositional Video Generation, CVG）任务中的两类代表性方法：基于边界框引导的布局控制方法，以及基于大语言模型（LLM）规划的扩散生成方法。

**（1）相对于 R&P（Region & Boundary Aware Grounding）的改进。** R&P 最初为组合式文本到图像生成设计，通过区域感知的交叉注意力实现实例与文本的语义绑定。将其适配至视频生成时，R&P 对每一帧独立施加统一的区域引导，但**不区分不同实例的运动类别**——这意味着一个静止的杯子和一个滚动的球在引导机制上被等同对待。MF-CVG 的核心突破在于将运动因子显式分解为静止、刚体、非刚体三个类别，并为每个类别设计解耦的引导分支：参考条件引导（RCG）约束静止实例的跨帧外观一致性，几何不变性引导（GIG）保持刚体实例的形状不变性，空间形变引导（SDG）捕捉非刚体实例的复杂形变。这一设计使得 Subject Consistency 从 R&P 的 91.00% 提升至 98.27%（CVGBench-m），Dynamic Degree 从 91.02% 提升至 96.00%。

**（2）相对于 VideoTetris 的改进。** VideoTetris 通过框引导实现组合式视频生成，但其运动规划直接从用户提示生成边界框序列，缺乏对运动规律的显式推理。MF-CVG 引入**结构化运动图（Structured Motion Graph）** 作为中间表示：将提示解析为描述实例及其交互关系的图结构（节点标注运动类别和属性，有向边编码成对关系），再由 LLM 从图中推理运动规律生成时空布局。这一设计消除了直接从文本到布局的语义歧义，使不同实例的运动模式真正差异化。

**（3）相对于 LVD（LLM-grounded Video Diffusion）的差异。** LVD 同样利用 LLM 进行视频生成的布局规划，但其引导范式是统一的，不区分运动类别。MF-CVG 的 DMG 模块在扩散去噪过程中，对 3D U-Net 架构通过梯度更新视频嵌入（Eq. 3），对 DiT 架构通过修改注意力分数注入引导掩码（Eq. 4），实现了类别特定的解耦控制。

### 2. 技术谱系中的位置

MF-CVG 处于**训练自由（training-free）的组合式视频生成**这一技术节点。与需要额外微调或定制训练的方法不同，MF-CVG 直接作用于预训练视频扩散模型（VideoCrafter-v2.0 的 3D U-Net 架构和 CogVideoX-2B 的 DiT 架构），无需任何模型参数更新。这一特性使其具有即插即用的工程优势，但同时也受限于基座模型的能力边界。

从运动建模的角度，MF-CVG 将物理世界的运动抽象为三个基本类别，这一简化假设在大多数自然场景中成立，但在涉及相机位姿变化或运动类别边界模糊的场景中可能失效——论文明确指出现有框架假设视点固定，未考虑相机运动。

### 3. 适用边界与局限

**（1）小目标运动引导不足。** 消融实验和失败案例分析（Figure 6）表明，当实例的边界框过小时，运动引导信号不足以约束生成过程，导致小物体（尤其是静止类别）的生成质量下降。这是基于注意力引导方法的固有局限：引导掩码的粒度受限于潜在空间的空间分辨率。

**（2）固定视点假设。** 当前框架假设相机视点固定，运动仅来自场景内实例的位置和形状变化。这一假设排除了全局视点变化（如镜头平移、旋转、缩放）的场景，限制了框架在更复杂动态场景中的适用性。

**（3）运动类别互斥假设。** 每个实例被唯一分配到一个运动类别（静止、刚体、非刚体之一）。对于同时包含多种运动模式的实例（如一个既平移又形变的物体），这一互斥分类可能过于简化。

### 4. 开放问题

论文明确提出了两个开放方向：其一，**如何结合相机位姿实现全局视点变化**，以支持第一人称视角或镜头运动场景的组合式生成；其二，**如何处理小物体运动证据不足的问题**，可能需要引入多尺度引导机制或改进注意力图的分辨率。此外，从方法谱系的角度，将运动因子分解的思想从视频生成迁移至其他时序生成任务（如 4D 场景生成、世界模型）是一个自然的延伸方向，但论文未对此展开讨论。

## 原文 PDF

![[paperPDFs/CVPR_2026/Training_free_Motion_Factorization_for_Compositional_Video_Generation.pdf]]

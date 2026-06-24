---
title: "Cortical Policy: A Dual-Stream View Transformer for Robotic Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Cortical_Policy_A_Dual_Stream_View_Transformer_for_Robotic_Manipulation.pdf
openreview_forum_id: eWe8zqGvs5
aliases:
- CP
- CPDSVTRM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "用静态几何一致流和动态腕部视角流增强RVT-2机器人操作策略。"
primary_logic: "Cortical Policy先用VGGT监督静态多视角特征几何一致，再用预训练GLC从腕部视角生成动作热力图并融合动作预测。"
claims:
- "静态视图流通过SmoothAP和循环几何一致性损失对齐不同相机中同一3D位置的特征。"
- "动态视图流把腕部相机输入建模为末端执行器位置热力图，为动作推理提供自我中心线索。"
- "仅加入双流会降低性能，几何一致性损失和冻结的位置感知预训练是双流生效的关键。"
- "Cortical Policy在RLBench 18任务和COLOSSEUM鲁棒性基准上均超过RVT-2等基线。"
---

# Cortical Policy: A Dual-Stream View Transformer for Robotic Manipulation

> [!tip] 核心洞察
> Cortical Policy

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cortical Policy: A Dual-Stream View Transformer for Robotic Manipulation |
| 英文题名 | Cortical Policy: A Dual-Stream View Transformer for Robotic Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eWe8zqGvs5) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method |  |
| Dataset | |

## 概述

现有机器人操作中的视图变换器（view transformer）在多视角场景下存在明显短板：它们缺乏对**跨视角空间关系**的显式建模能力。例如，当任务要求理解两个瓶子之间的空间位置以决定放置点时，RVT-2 等先前方法因无法有效融合不同相机视角的信息而失败（Figure 1）。这一瓶颈的根源在于，传统方法将多视图特征视为孤立的信息源，缺少几何一致的3D表征与面向动作的精细定位能力。

针对上述问题，本文提出 **Cortical Policy**——一种受视觉神经科学中背侧-腹侧通路启发的**双流视图变换器**（Figure 2）。其核心设计包含两条互补处理流：

- **静态视图流（Static-View Stream）**：通过跨视图几何一致性学习来编码场景的3D空间结构，该过程由预训练的3D基础模型 **VGGT** 提供监督信号。
- **动态视图流（Dynamic-View Stream）**：从腕部相机的自我中心视角直接预测末端执行器位置，将动作推理建模为注意力图生成，其骨干来自预训练的自我中心注视估计模型 **GLC**。

在 **RLBench 18任务多任务基准**上，Cortical Policy 取得了 **81.0%** 的平均成功率，较最强基线 RVT-2（77.5%）提升 **+3.5%**，在参数量与计算量更少的情况下实现了性能超越（Table 1）。在 **COLOSSEUM** 扰动鲁棒性基准上，该方法同样以 **69.9%** 的平均成功率领先所有对比方法（Table 3）。真实世界实验进一步验证了其从仿真到现实的迁移能力（Figure 4）。

从方法谱系看，Cortical Policy 定位为 **RVT-2 架构的增强型变体**：它保留了 RVT-2 的两阶段处理、视图内自注意力和视觉-语言协同注意力机制，同时通过双流设计引入了此前视图变换器所缺失的3D几何感知与自我中心动作定位能力。这一改进使模型在不显著增加推理开销的前提下，显著提升了对空间关系敏感任务的泛化性与鲁棒性。

## 背景与动机

机器人操控任务要求智能体在三维空间中精确理解物体间的空间关系，并据此生成可执行的动作序列。近年来，基于视图变换器（View Transformer）的方法通过将多视角 RGB‑D 图像渲染为可学习的 token 序列，在语言条件操控基准上取得了显著进展。然而，现有方案存在一个共性的结构缺陷：它们将多个静态相机视图独立编码为 token，再通过自注意力机制进行融合，但**缺乏对跨视图几何关系的显式建模**。

这一缺陷在需要精细空间推理的任务中尤为突出。如 Figure 1 所示，当任务要求机器人理解两个瓶子之间的相对位置以决定放置点时，RVT‑2 等先前方法无法有效融合不同相机视图中的空间线索，导致动作预测失败。根本原因在于，静态多相机设置受限于固定的正交投影约束，难以捕捉物体在三维空间中的精确位姿关系；同时，这些方法也缺少来自机器人第一人称视角的动态、以动作为导向的视觉信号，无法形成对末端执行器位置的直接感知。

受视觉神经科学中背侧‑腹侧双通路理论的启发，本文提出 **Cortical Policy**，一种双流视图变换器架构。该架构包含两个互补的处理流：**静态视图流**（static‑view stream）负责从多视角静态图像中提取三维空间结构，通过跨视图几何一致性约束增强场景理解；**动态视图流**（dynamic‑view stream）则从腕部动态相机视角直接预测末端执行器位置，为动作推理提供以目标为导向的注意力线索。两条通路协同工作，旨在弥补现有视图变换器在空间推理和动态感知上的双重不足。

## 核心创新

Cortical Policy 的核心创新在于将机器人操作策略构建为**双流视图 Transformer**，分别模拟生物视觉皮层中“腹侧通路”（what）与“背侧通路”（where）的功能分工。这一架构在 RVT-2 基线（Goyal et al., 2024）的基础上引入了两个关键 changed slots，直接针对现有多视图 Transformer 在空间推理与动态感知上的结构性瓶颈。

**创新一：静态视图流 + 跨视图几何一致性监督**

现有视图 Transformer（如 RVT-2）将多相机视图独立编码后简单拼接，缺乏对视图间空间关系的显式建模。Cortical Policy 的静态视图流在 RVT-2 的特征提取器中嵌入跨视图几何一致性学习：利用预训练的 3D 基础模型 VGGT 提取跨视图几何一致的关键点作为监督信号，通过 SmoothAP 排序损失强制同一 3D 位置在不同视图中的特征表示对齐。进一步地，引入**循环几何一致性损失** $\mathcal{L}_{cgc}$，在闭合视图环 $v_1 \to v_2 \to \dots \to v_N \to v_1$ 上最小化排序损失，以抑制累积动作估计误差。这一设计使静态视图流能够学习到 3D 感知的语义表征，显著提升了需要空间关系理解的任务（如“将物体放在两个瓶子之间”）的成功率。

**创新二：动态视图流 + 位置感知预训练注意力**

基线方法受限于固定正交相机的严格几何约束，无法灵活跟踪末端执行器的动态变化。Cortical Policy 引入动态视图流，将手腕相机（机器人自我中心视图）作为输入，并将动作推理建模为注意力图生成问题——这一思路借鉴了自我中心注视估计模型 GLC（Lai et al., 2024）。动态视图流使用在 3,600 个位置标注视频上预训练的 GLC 作为特征提取器，生成以末端执行器位置为焦点的热力图，作为显式的动作线索。该流与静态视图流并行处理，最终通过热力图加权池化与全局特征拼接实现双流融合。消融实验表明，冻结预训练权重的方式优于端到端联合训练（+1.9%），且热力图是动态流发挥作用的关键组件——移除热力图后，双流模型性能反而不及单流变体。

**创新三：双流融合机制**

两个流并非简单堆叠，而是通过热力图引导的特征聚合实现互补：静态流提供多视角全局 3D 结构理解，动态流提供末端执行器中心的局部动作先验。全局特征向量由四个视角（三个静态正交视图 + 一个动态自我中心视图）的热力图加权特征与最大池化特征拼接而成，最终输入 RVT-2 的动作预测头。这一融合方式使得模型在 RLBench 18 任务上达到 81.0% 的平均成功率（较 RVT-2 提升 3.5%），并在 COLOSSEUM 鲁棒性基准上领先 RVT-2 达 9.4%。

总体而言，Cortical Policy 的 changed slots 集中在**特征提取阶段的几何约束注入**（静态流）与**感知模态的扩展**（动态流），而保留了 RVT-2 的两阶段处理、视图内自注意力和视觉-语言协同注意力等核心机制，属于在成熟基线框架上的定向增强。

## 整体框架

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_eWe8zqGvs5/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed cortical policy. Inspired by the dorsal-ventral pathways in visual neuroscience, this architecture implements dual processing streams: a static-view stream for 3D spatial understanding and a dynamic-view stream for end-effector position awareness*

Cortical Policy 的整体架构受视觉神经科学中背侧–腹侧通路的启发，设计为双流视图变换器（dual-stream view transformer），由**静态视图流（static-view stream）**和**动态视图流（dynamic-view stream）**并行构成，二者联合推理以生成机器人操作动作。

### 输入与双流分工

系统接收两类视觉输入：

- **静态多相机视图**：来自场景中固定安装的多个 RGB-D 相机，提供覆盖工作空间的完整三维场景信息。
- **动态腕部视图**：来自安装在机器人末端执行器上的腕部相机，随机械臂运动而变化，提供以末端执行器为中心的第一人称视角。

两条流的分工明确：静态视图流负责理解场景的三维空间结构，动态视图流负责从末端执行器视角提取面向动作的注意力线索。

### 静态视图流

静态视图流以 **RVT-2**（Goyal et al., 2024）为骨干，保留其两阶段处理、视图内自注意力以及视觉–语言协同注意力等核心机制，并在特征提取器（RVT Encoder）层面进行增强。该流的核心创新在于引入**跨视图几何一致性约束**：利用预训练的三维基础模型 **VGGT** 提取跨视图几何一致的稀疏关键点作为三维监督信号，通过 **SmoothAP 排序损失**强制不同视图中对应同一三维位置的特征在语义空间中保持相近。这一约束以**循环几何一致性损失** $\mathcal{L}_{cgc}$ 的形式组织——沿闭合的视图环 $v_1 \rightarrow v_2 \rightarrow \cdots \rightarrow v_N \rightarrow v_1$ 最小化排序损失，从而降低累积动作估计误差。静态视图流最终输出多视图特征图与动作热力图。

### 动态视图流

动态视图流将动作推理建模为注意力图生成问题，类比于以自我为中心的视频注视估计。其核心是一个**预训练的位置感知变换器**，源自以自我为中心的注视估计模型 **GLC**（Lai et al., 2024）。该变换器在由 18 个任务 × 100 条轨迹 × 2 个阶段构成的 3,600 条位置标注视频数据集上预训练，使用 KL 散度损失训练 15 个周期后冻结。动态视图流从腕部相机图像中提取自注意力特征和全局–局部相关特征，经拼接与线性投影后生成动态特征图 $\mathbf{F} \in \mathbb{R}^{B \times (P \times P) \times C}$，同时通过 $2 \times 2 \times 2$ 下采样生成显著性图（saliency map），经尺寸调整和时间维压缩后与静态视图热力图对齐。显著性图作为显式动作线索，直接指示末端执行器的目标位置区域。

### 双流融合与动作预测

两条流的输出在全局特征层面进行融合。具体而言，对于三个静态视图和一个动态视图，分别计算热力图加权和池化特征 $\phi(\mathbf{F}_i \odot \mathbf{H}_i)$ 与最大池化特征 $\psi(\mathbf{F}_i)$，将所有视图的这两类特征拼接形成全局特征向量：

$$[\phi(\mathbf{F}_1 \odot \mathbf{H}_1); \phi(\mathbf{F}_2 \odot \mathbf{H}_2); \phi(\mathbf{F}_3 \odot \mathbf{H}_3); \phi(\mathbf{F}_4 \odot \mathbf{H}_4); \psi(\mathbf{F}_1); \psi(\mathbf{F}_2); \psi(\mathbf{F}_3); \psi(\mathbf{F}_4)]$$

该全局特征随后送入 RVT-2 的动作头，预测末端执行器的平移、旋转、夹爪开合等动作分量。

### 训练目标

总损失函数由两项组成：

$$\mathcal{L} = \mathcal{L}_{action} + \lambda \mathcal{L}_{cgc}$$

其中 $\mathcal{L}_{action}$ 为各动作分量的交叉熵损失之和，$\mathcal{L}_{cgc}$ 为跨视图几何一致性损失，权衡参数 $\lambda = 1$。

### 关键设计决策

- **动态虚拟相机**突破了现有多相机视图变换器严格的平行投影约束，使模型能够从末端执行器的移动视角理解场景，增强对动态遮挡和局部空间关系的鲁棒性。
- **位置感知预训练**优于端到端联合训练：消融实验表明，冻结预训练的注视模型比端到端训练高出 1.9% 的平均成功率（Table 2，变体 E vs. C），验证了预训练位置先验对动态视图流的关键作用。
- **显著性热力图**是动态视图流不可或缺的组件：去除热力图后（Table 2，变体 D），双流模型性能甚至低于单流变体，确认了显式动作线索的核心地位。

## 核心模块与公式推导

### 双流架构总览

Cortical Policy 的核心架构由两个互补的处理流构成：**静态视角流（Static-View Stream）** 和 **动态视角流（Dynamic-View Stream）**。静态视角流从多个固定相机视图中提取 3D 空间结构信息，动态视角流则从腕部相机的自视角中直接预测末端执行器的位置热力图。两流输出在 RVT-2 的动作预测头中融合，最终产生抓取位姿和运动指令。

### 静态视角流：交叉视角几何一致性

静态视角流以 RVT-2 的 backbone 为基础（Goyal et al., 2024），保留其两阶段处理、视角内自注意力和视觉-语言协同注意力机制，同时在其特征提取器（RVT Encoder）上施加几何约束。核心思路是强制不同视角下对应同一 3D 点的特征表示保持一致，从而学习 3D 感知的语义表征。

**几何监督信号**来自预训练的 3D 基础模型 VGGT。VGGT 在多视角图像中检测几何一致的 2D 关键点——这些关键点对应场景中相同的 3D 位置，构成跨视角的对应关系。方法利用这些关键点作为监督，要求同一 3D 点在任意两个视角下的特征向量在嵌入空间中彼此接近，而与其他 3D 点的特征向量保持距离。

**交叉视角特征排序损失**采用 SmoothAP 损失函数。对于从视角 $v_p$ 到视角 $v_q$ 的查询，SmoothAP 损失定义为：

$$L^{\circ}(v_p \to v_q) = \frac{1}{|K_p|} \sum_{i=1}^{|K_p|} \frac{1 + \sum_{\mathbf{k}_j \in K(i)} \mathcal{G}(D_{ij})}{1 + \sum_{\mathbf{k}_j \in K(i)} \mathcal{G}(D_{ij}) + \sum_{\mathbf{k}_j \in \mathcal{N}(i)} \mathcal{G}(D_{ij})}$$

其中 $K_p$ 是视角 $v_p$ 中的关键点集合，$K(i)$ 是与关键点 $i$ 匹配的正样本集合（来自视角 $v_q$ 中对应同一 3D 点的关键点），$\mathcal{N}(i)$ 是负样本集合。$D_{ij}$ 表示正样本对与负样本对在特征点积相似度上的差异，$\mathcal{G}(\cdot)$ 为 sigmoid 函数，用于平滑排序度量。

**循环几何一致性损失**（Cyclic Geometric Consistency Loss）进一步约束多视角间的全局一致性。给定 $N$ 个静态视角，构建闭合循环 $v_1 \to v_2 \to \cdots \to v_N \to v_1$，最小化该循环上的累计排序损失：

$$\mathcal{L}_{cgc} = 1 - \frac{1}{N} \sum_{p=1}^{N} \mathrm{SmoothAP}(v_p \to v_{p \oplus 1})$$

其中 $p \oplus 1$ 表示循环中的下一个视角索引。该损失强制特征在完整的视角环中保持一致性，降低累积动作估计误差。

### 动态视角流：位置感知的注意力热力图

动态视角流将动作推理建模为注意力图生成问题，类比于自视角注视估计（Lai et al., 2024）。输入为腕部相机的自视角图像，输出为末端执行器目标位置的二维热力图。

特征提取器采用预训练的 **GLC（Global-Local Correlation）模型**，该模型在自建数据集上进行了位置感知预训练。预训练数据集包含 3,600 段位置标注视频（18 个任务 × 100 条轨迹 × 2 个阶段），使用 KL 散度损失训练 15 个 epoch。预训练完成后，GLC 的参数被冻结，作为动态视角流的固定特征提取器。

GLC 输出两类特征：
- **自注意力特征** $\mathbf{F}^{SA}$：捕捉全局上下文信息
- **全局-局部相关特征** $\mathbf{F}^{GLC}$：编码局部细节与全局结构的关联

两类特征沿通道维度拼接后，通过线性投影映射到 RVT-2 的 token 空间：

$$\mathbf{F} = \mathbf{LP}([\mathbf{F}^{SA}, \mathbf{F}^{GLC}]_c) \in \mathbb{R}^{B \times (P \times P) \times C}$$

其中 $B$ 为 batch size，$P \times P$ 为 patch 数量，$C$ 为通道维度。同时，GLC 生成形状为 $B \times 1 \times 2 \times 128 \times 128$ 的显著性热力图，经上采样至 $224 \times 224$ 并通过 3D 卷积压缩时间维度后，与静态视角流的热力图进行融合。

### 双流融合与全局特征

静态视角流（3 个固定视角）与动态视角流（1 个自视角）各产生特征图 $\mathbf{F}_i$ 和对应的热力图 $\mathbf{H}_i$。全局特征向量由以下两部分拼接而成：

$$[\phi(\mathbf{F}_1 \odot \mathbf{H}_1); \phi(\mathbf{F}_2 \odot \mathbf{H}_2); \phi(\mathbf{F}_3 \odot \mathbf{H}_3); \phi(\mathbf{F}_4 \odot \mathbf{H}_4); \psi(\mathbf{F}_1); \psi(\mathbf{F}_2); \psi(\mathbf{F}_3); \psi(\mathbf{F}_4)]$$

其中 $\phi(\cdot)$ 表示求和池化，$\psi(\cdot)$ 表示最大池化，$\odot$ 表示逐元素乘积。热力图加权特征提供空间注意力引导的局部信息，最大池化特征保留全局上下文。

### 总损失函数

训练总损失为动作预测损失与交叉视角几何一致性损失的加权和：

$$\mathcal{L} = \mathcal{L}_{action} + \lambda \mathcal{L}_{cgc}$$

其中 $\mathcal{L}_{action}$ 为各动作分量（抓取位姿、开合角度等）的交叉熵损失之和，$\lambda$ 为权衡系数，设置为 1。该设计使模型在优化行为克隆目标的同时，通过几何一致性约束学习更鲁棒的 3D 空间表征。

## 实验与分析

### 主结果：RLBench 多任务性能

Cortical Policy 在 RLBench 18 任务多任务设定下取得了 **81.0%** 的平均成功率，平均排名 **1.8**（Table 1），较此前最优基线 RVT-2（77.5%，排名 3.5）提升 **+3.5 个百分点**。在 18 项任务中，Cortical Policy 有 14 项进入前两名，其中 Drag Stick、Meat off Grill、Push Buttons、Put in Drawer、Sweep to Dustpan 五项任务达到 **100.0%** 成功率。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_eWe8zqGvs5/figures/004_Table_1.jpg]]
*Table 1: Comparison with SOTA methods on RLBench. The “Avg. Success” and “Avg. Rank” columns report the average success rate (%) and the average rank across 18 tasks. Best results are highlighted in bold, and the second best are underlined*

性能增益并非来自参数量的简单堆砌。容量控制实验（Table 7）显示，Cortical Policy 以 **144.7M** 参数量和 **22.37G** FLOPs 取得 81.0% 成功率，而加深的 RVT-2 变体在更大参数量下仍不及该结果，说明双流架构的设计本身是性能提升的核心驱动。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_eWe8zqGvs5/figures/016_Table_7.jpg]]
*Table 7: Capacity-controlled ablation study on RLBench*

### 消融分析：双流架构各组件贡献

Table 2 的消融实验逐层拆解了各设计组件的贡献，以单流 RVT-2 基线（Variant A，77.5%）为起点：

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_eWe8zqGvs5/figures/005_Table_2.jpg]]
*Table 2: Ablation study on dual-stream view transformer. All designs contribute to improving performance of Cortical Policy. “Arch.”, “Pre.”, “Heat.” denote model architecture, position-aware pretraining, dynamic-view heatmap, respectively. “Single” means single-stream model with only static viewpoints, “Dual” means dual-stream model integrating dynamic and static viewpoints*

| 变体 | 架构 | L_cgc | 预训练 | 热力图 | 平均成功率 |
|------|------|-------|--------|--------|------------|
| A | 单流 | ✗ | ✗ | ✗ | 77.5 |
| B | 双流 | ✗ | ✗ | ✗ | 73.3 |
| C | 双流 | ✗ | 端到端联合训练 | ✗ | 71.4 |
| D | 双流 | ✗ | 冻结预训练 | ✗ | 72.7 |
| E | 双流 | ✓ | 冻结预训练 | ✗ | 79.5 |
| F（完整） | 双流 | ✓ | 冻结预训练 | ✓ | **81.0** |

**关键因果链**：

1. **仅加双流架构反而有害**（B vs. A：73.3% vs. 77.5%）。双流架构引入动态视角后，若缺乏几何一致性约束，多视角特征无法对齐，反而破坏原有单流表征。

2. **L_cgc 是双流生效的前提**（E vs. B：+6.2 个百分点）。跨视角几何一致性损失强制静态流学习 3D 一致特征，使双流架构的增益得以释放。L_cgc 对单流同样有效（B vs. A 的 2.6% 增益来自 L_cgc 加入），但对双流的边际贡献更大。

3. **位置感知预训练优于端到端训练**（E vs. C：79.5% vs. 71.4%）。冻结预训练注视模型（GLC）比端到端联合训练高出 **1.9 个百分点**（E vs. C），且端到端训练（C）甚至低于无预训练的 B（71.4% vs. 73.3%），说明动态流特征提取器需要稳定的先验，联合训练会破坏其表征质量。

4. **热力图提供显式动作线索**（F vs. E：+1.5 个百分点）。无热力图的变体 D（72.7%）甚至低于单流基线，证实动态流中的注意力热力图是动作推理的关键显式信号，而非可有可无的辅助信息。

### 鲁棒性：THE COLOSSEUM 扰动基准

在 THE COLOSSEUM 基准上，Cortical Policy 取得 **69.9%** 平均成功率（Table 3），较 RVT-2 提升 **9.4 个百分点**，在所有 12 种扰动类型下均保持最优或次优。该基准通过改变光照、纹理、相机位姿、物体摆放等方式测试策略的泛化鲁棒性，Cortical Policy 的大幅领先表明双流架构对视觉域偏移具有更强的容忍度——静态流提供的 3D 几何先验和动态流提供的注视引导注意力共同增强了表征的不变性。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_eWe8zqGvs5/figures/006_Table_3.jpg]]
*Table 3: Results on THE COLOSSEUM. The “Avg. Success” and “Avg. Rank” columns report the average success rate (%) and the average rank across all perturbations on 4 COLOSSEUM tasks*

### 真实世界验证

真实世界实验中，Cortical Policy 在空间推理任务（如堆叠方块）上较 RVT 和 RVT-2 成功率高出 **30%**；在动态扰动场景下仍保持 **80%** 成功率（Figure 4b）。轨迹可视化（Figure 4c）显示，Cortical Policy 在“堆叠两方块且底座位移”任务中能自适应调整末端执行器路径，而基线方法的轨迹则出现明显偏移。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_eWe8zqGvs5/figures/007_Figure_4.jpg]]
*Figure 4: (a) Training time of Cortical Policy modules, with time cost of 3D supervision generation, dual streams, action head. (b) (Top) Real-world performance comparison. (Bottom) Visualization of the initial and final states for the four real-world tasks. (c) Trajectory visualization for “stack 2 blocks with base displacement” task*

### 训练效率

Figure 4a 给出了各模块的训练时间分解：双流训练总计约 3.76×10² 分钟（静态流约 1.30×10² 分钟，动态流约 2.46×10² 分钟），3D 监督信号生成额外消耗约 0.58×10² 分钟。动态流预训练阶段使用 3600 段位置标注视频（18 任务 × 100 片段 × 2 阶段），以 KL 散度损失训练 15 轮。

### 失败模式与局限

论文未系统报告失败案例分析，但从消融实验可推断关键失效条件：

- **无 L_cgc 的双流架构**（Variant B，73.3%）性能显著退化，说明当跨视角几何约束缺失时，静态流与动态流的特征无法有效融合，多视角信息反而成为噪声。
- **端到端训练动态流**（Variant C，71.4%）表现最差，表明注视模型的预训练先验对稳定动态流表征至关重要，联合优化会导致表征坍塌。
- 论文未讨论动态遮挡、极端光照、未见物体类别等条件下的失败模式，这些场景下的鲁棒性需手动验证。

### 开放问题

论文提出的两个开放方向值得关注：一是如何增强组合抽象能力以实现零样本任务泛化；二是如何将动态流从跟踪末端执行器扩展到跟踪多样化的任务相关目标。这两个问题直接关系到 Cortical Policy 从“多任务熟练”走向“新任务泛化”的可行性。

## 方法谱系与知识库定位

### 与现有工作的关系

Cortical Policy 的核心架构建立在 **RVT-2**（Goyal et al., 2024）的骨干网络之上，保留了其两阶段处理流程、视角内自注意力（intra-view self-attention）和视觉-语言协同注意力（vision-language co-attention）机制。在此基础上，Cortical Policy 对特征提取器（RVT Encoder）进行了增强，引入了双流架构和跨视角几何一致性约束，使其在 RLBench 18 任务多任务评测中取得 **81.0%** 的平均成功率，较 RVT-2 的 77.5% 提升了 **+3.5%**（Table 1）。

与现有视图变换器（view transformer）方法相比，Cortical Policy 的关键差异在于显式建模了多视角之间的关系。此前的视图变换器（如 RVT、RVT-2）将多相机输入视为独立视图，缺乏对视角间空间关系的显式推理。Cortical Policy 通过两条互补的流解决这一瓶颈：

- **静态视图流**：从三个正交静态相机视角学习 3D 感知特征，利用 3D 基础模型 **VGGT** 提供的几何一致性关键点作为监督信号，通过循环几何一致性损失 $\mathcal{L}_{cgc}$ 强制不同视角下同一 3D 位置的特征对齐。这一设计将 3D 几何先验注入到原本仅依赖 2D 图像特征的策略学习中。
- **动态视图流**：引入了一个动态的腕部相机视角（机器人自我中心视角），将动作推理建模为注意力图生成，类比于以自我为中心的人类注视估计。该流使用了一个预训练的、位置感知的 Transformer，该 Transformer 源自自我中心注视估计模型 **GLC**（Lai et al., 2024），并在 3600 个位置标注视频（18 任务 × 100 条轨迹 × 2 阶段）上进行了预训练。

与 **PerAct**（Shridhar et al., CoRL 2022）和 **VIHE**（Gu et al., 2024）等方法相比，Cortical Policy 在 RLBench 上取得了最高的平均排名（1.8），且在 18 个任务中的 14 个任务上位列前两名（Table 1）。在 COLOSSEUM 鲁棒性基准上，Cortical Policy 以 **69.9%** 的平均成功率显著超越 RVT-2（+9.4%），表明其在动态扰动和视觉变化下的泛化能力更强（Table 3）。

消融实验（Table 2）进一步揭示了各组件的贡献机制：静态视图流和动态视图流分别带来 **+2.6%** 和 **+0.9%** 的增益；循环几何一致性损失 $\mathcal{L}_{cgc}$ 在单流和双流架构上均带来一致提升（变体 B vs. A 提升 2.6%，完整模型 F vs. E 提升 1.5%）；位置感知预训练相比端到端联合训练提升了 **1.9%** 的平均成功率（变体 E vs. C）；动态视图热力图（heatmap）作为显式动作线索对动态视图流至关重要，移除热力图后变体 D 的表现甚至不及单流变体。

### 适用边界

Cortical Policy 的设计依赖于以下前提条件，这些条件界定了其适用边界：

1. **多相机设置**：静态视图流需要三个正交静态相机（顶部、前部、右侧）的 RGB 图像输入。在仅能获取单一视角或相机布局差异较大的场景中，该流的几何一致性监督可能失效。
2. **腕部相机可用性**：动态视图流依赖腕部相机的自我中心视角。若机器人平台未配备腕部相机，或腕部相机视场受限，则动态视图流的动作推理能力将受到限制。
3. **3D 基础模型依赖**：静态视图流的几何一致性关键点由 VGGT 生成。若 VGGT 对特定场景（如低纹理、透明物体、强光照变化）的 3D 重建质量下降，则 $\mathcal{L}_{cgc}$ 的监督信号质量会受到影响。
4. **任务类型**：当前验证集中在桌面级操作任务（RLBench 的 18 个任务、COLOSSEUM 的 4 个任务），涉及抓取、放置、推拉、堆叠等操作。对于需要长期规划、力控精度或动态交互的复杂任务，方法的有效性尚未验证。

### 局限与开放问题

论文中明确指出的开放问题包括：

- **组合抽象能力的泛化**：如何增强模型的组合抽象能力，以实现零样本任务泛化（zero-shot task generalization）？当前模型在多任务学习中表现优异，但未见其在新任务组合或未见任务上的泛化实验。
- **动态视图流的目标扩展**：如何将动态视图流从跟踪末端执行器扩展到跟踪多样化的目标（如被操作物体、工具、人手）？当前热力图生成仅针对末端执行器位置，限制了其在更复杂交互场景中的应用。

此外，从实验设置中可推断的潜在局限：

- **训练数据需求**：动态视图流的预训练需要 3600 条位置标注视频，这在实际部署中可能构成数据采集瓶颈。虽然预训练后冻结了注视模型参数，但预训练阶段本身的数据成本不可忽视。
- **计算开销**：Figure 4(a) 显示，双流架构的训练时间显著增加（动态视图流约 2.46×10³ 分钟，静态视图流约 1.30×10³ 分钟），相比 RVT-2 的单一动作头（约 0.74×10³ 分钟）有约 5 倍的总训练时间增长。不过，Table 7 的容量控制消融表明，Cortical Policy 在参数更少（144.7M vs. 更深基线）的情况下取得了更高成功率，说明效率与性能之间存在设计权衡空间。
- **真实世界验证规模**：真实世界实验仅涉及 4 个任务，且未报告重复次数和统计显著性。文中声称在空间推理任务上比 RVT 和 RVT-2 高出 30% 成功率、在动态扰动下达到 80% 成功率，但这些数字需在更大规模的真实世界评测中进一步验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Cortical_Policy_A_Dual_Stream_View_Transformer_for_Robotic_Manipulation.pdf]]

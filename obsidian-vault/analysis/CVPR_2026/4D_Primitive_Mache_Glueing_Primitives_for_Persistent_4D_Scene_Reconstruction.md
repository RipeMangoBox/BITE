---
title: "4D Primitive-Mache: Glueing Primitives for Persistent 4D Scene Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/4D_Primitive_Mache_Glueing_Primitives_for_Persistent_4D_Scene_Reconstruction.pdf
project_link: "https://makezur.github.io/4DPM/"
code_link: null
aliases:
- 4PM4
- 4PMGPP4SR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将场景分解为刚性运动的3D基元，并为每个基元赋予SE(3)姿态参数。这一紧凑参数化将复杂的逐帧密集映射问题简化为每个基元的单一刚体运动估计，大幅降低了动态重建的维度。
primary_logic: 通过前馈重建模型获取各时刻的3D基元，利用稠密2D对应关系跨时间优化每个基元的SE(3)姿态（即"拼合"基元），并基于对象分组实现运动分割与遮挡物体的运动外推，从而在任意观测时刻回放完整的4D场景重建。
claims:
- 将场景分解为一组刚性3D基元，通过优化管道联合推断其刚性运动
- 基于基元的运动参数化将逐像素运动场表示为稀疏的每基元SE(3)姿态，显著降低动态重建维度
- 通过运动分组技术实现对不可见物体的运动外推，赋予系统空间记忆能力
- 在物体扫描和多物体数据集上，定量和定性结果均显著优于现有方法
---

# 4D Primitive-Mache: Glueing Primitives for Persistent 4D Scene Reconstruction

> [!tip] 核心洞察
> 通过前馈重建模型获取各时刻的3D基元，利用稠密2D对应关系跨时间优化每个基元的SE(3)姿态（即"拼合"基元），并基于对象分组实现运动分割与遮挡物体的运动外推，从而在任意观测时刻回放完整的4D场景重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4D Primitive-Mache：通过基元拼合实现持久4D场景重建 |
| 英文题名 | 4D Primitive-Mache: Glueing Primitives for Persistent 4D Scene Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Mazur_4D_Primitive-Mache_Glueing_Primitives_for_Persistent_4D_Scene_Reconstruction_CVPR_2026_paper.html) · [Project](https://makezur.github.io/4DPM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 4D Primitive-Mache (4DPM) |
| Dataset | HO3D, Multi-Object |

> [!tip] 效果简介
> - HO3D (多视角手-物体交互数据集) 上，F-score (1cm阈值，动态部分) 0.7573 (平均F-score) vs 所有基线中最佳方法显著低于此值 (显著优于所有基线 (substantial margin))。
> - Multi-Object (多物体动态场景数据集) 上，Mean F-score (1cm阈值，动态部分) 0.7948 (平均F-score) vs 所有基线方法均明显低于此值 (显著优于所有基线 (significantly outperforms))。

## 概要

### 问题瓶颈

单目动态场景重建的核心瓶颈在于**缺乏持久性**：现有方法仅在观测时刻估计几何，历史观测信息随时间被丢弃。当物体移出视野或被遮挡后，其几何信息永久丢失，导致重建完整性差且精度受限。本文提出的 **4D Primitive-Mache (4DPM)** 旨在解决这一问题——在所有已观测时间戳上输出完整的4D场景重建。

### 核心思路

4DPM 将场景**分解为一组刚性运动的3D基元**，并为每个基元赋予 SE(3) 姿态参数。这一紧凑参数化将复杂的逐帧密集映射问题简化为每个基元的单一刚体运动估计，大幅降低了动态重建的维度。通过估计的稠密2D对应关系，系统跨时间联合优化所有基元的 SE(3) 姿态（即“拼合”基元），并基于对象分组实现运动分割与被遮挡物体的运动外推。

### 方法定位

4DPM 属于**前馈重建模型 + 后端正交优化**的混合范式。前端利用前馈重建模型 π³（Wang et al., ICLR 2026）获取各时刻的3D基元，并通过 SAMv2 传播掩码形成跨时间的对象级分组；后端通过 Gauss-Newton 联合优化求解所有非静态对象的基元姿态，不依赖逐像素运动场或成对帧间变换。与 **St4track**（Feng et al., CVPR 2025）和 **PO-MATO**（Zhang et al., ICCV 2025）等基于 DUSt3R 的跟踪重建方法相比，4DPM 的基元级运动参数化更为稀疏且结构化，并具备对不可见物体的运动推理能力。

### 主要结果

在 **HO3D** 多视角手-物体交互数据集上，4DPM 在动态部分的 F-score（1cm 阈值）达到 **0.7573**，显著优于所有基线方法。在 **Multi-Object** 多物体动态场景数据集上，平均 F-score 达到 **0.7948**，同样大幅领先。定性结果进一步表明，4DPM 在旋转球体、机器人夹爪等挑战性物体上能正确聚合所有历史观测，并在抽屉关闭等完全遮挡场景下展现出物体持久性重建能力。



单目动态场景重建是计算机视觉的核心挑战之一，其目标是从一段手持拍摄的RGB视频中恢复出每帧对应的完整三维几何。这一能力对增强现实、机器人操作和数字孪生等应用至关重要。近年来，前馈式场景重建模型取得了显著进展，能够从单张或少数几张图像中直接预测稠密点云。然而，将这些模型应用于动态视频时，一个根本性瓶颈浮现：**现有方法仅在观测时刻估计几何，缺乏“持久性”（object permanence）**。

所谓持久性，是指系统能够记住并利用所有历史观测信息，而非仅仅依赖当前帧的可见内容。在动态场景中，物体频繁地被遮挡或移出视野——例如抽屉关闭时内部物体完全不可见，或机器人手臂旋转时遮挡操作台上的零件。现有方法在处理这类情况时，被遮挡物体的信息会永久丢失，导致重建完整性差且精度受限。基线方法如 **π³ (last view)**（Wang et al., ICLR 2026）仅使用最新帧的点云，代表了无持久性的动态重建下限；**π³ (time-warped)** 尝试用2D对应关系进行简单的时间变换，但缺乏结构化的运动约束；**St4track**（Feng et al., CVPR 2025）和 **PO-MATO**（Zhang et al., ICCV 2025）虽然建立了帧间对应关系，但其运动表示仍以逐像素运动场或成对帧间变换为主，维度高且难以对遮挡物体进行运动推理。

上述方法的共同缺口在于：**缺乏一种紧凑且结构化的场景运动表示**，能够将跨时间的碎片化观测整合为一致的4D重建。具体而言，现有方案面临三个相互关联的挑战：（1）逐像素运动估计的高维度使得全局优化困难且易受噪声干扰；（2）历史观测信息被丢弃，无法在后续时刻复用；（3）对不可见物体的运动缺乏推理机制，无法维持场景的时空连续性。

本文的动机正是填补这一缺口。我们观察到，大多数动态场景中的物体可以近似为刚体——它们的运动可以用一个单一的SE(3)姿态变换来描述。这一洞察启发我们提出一种**基于基元的运动参数化**：将场景分解为一组刚性3D基元（primitives），每个基元仅需一个SE(3)姿态即可表示其所有可见时刻的运动，从而将复杂的逐帧密集映射问题简化为稀疏的每基元刚体运动估计。在此基础上，通过跨时间的联合优化“拼合”这些基元，并引入运动分割技术实现对不可见物体的运动外推，我们旨在构建一个真正持久的4D场景重建系统——在任意观测时刻回放完整的场景几何。



## 核心方法与创新机理

4DPM 的核心创新在于将动态场景重建从“逐帧密集映射”重新定义为“稀疏基元的跨时间拼合”，通过三个紧密耦合的机制解决了现有方法的根本瓶颈。

### 瓶颈：时间遗忘与维度爆炸

现有单目动态重建方法（如 **π³**、**St4track** (Feng et al., CVPR 2025)、**PO-MATO** (Zhang et al., ICCV 2025)）存在两个结构性缺陷：

1. **缺乏持久性**：仅在观测时刻估计几何，历史观测信息被丢弃。当物体被遮挡或移出视野时，其几何信息永久丢失，无法在后续时刻恢复。
2. **运动参数化冗余**：逐像素运动场或成对帧间变换的表示方式维度极高，缺乏结构化约束，导致优化困难且精度受限。

### 创新一：基于基元的稀疏运动参数化

4DPM 将场景分解为一组刚性运动的3D基元，每个基元仅需一个 SE(3) 姿态参数即可表示其所有可见时刻的运动。这一参数化将逐像素运动场压缩为稀疏的每基元姿态，大幅降低了动态重建的维度。

**核心机制**：给定前馈重建模型 π³ 在各时刻估计的点云，系统将每个基元视为刚体，其从时刻 $p$ 到时刻 $q$ 的变换由姿态函数 $T(S^p)$ 和 $T(S^q)$ 唯一确定：

$$T^{p \mapsto q} := [T(S^q)]^{-1} T(S^p)$$

姿态更新通过李代数参数化实现：$T \gets T \oplus \tau$，其中 $\tau \in \mathfrak{se}(3) \simeq \mathbb{R}^6$，使优化在光滑流形上进行。

### 创新二：跨时间联合拼合优化

与基线方法仅做逐对帧对齐不同，4DPM 对所有非静态对象进行全局联合优化。代价函数直接最小化属于同一对象 $\mathcal{O}$ 的相邻基元经姿态变换后的3D点距离：

$$E(\mathcal{O}) = \sum_{(i,j) \in \mathcal{T}(\mathcal{O})} \| \mathbf{w}_{ij} \cdot S_i \cdot \widehat{S}_j (T_j^{-1} T_i \mathbf{X}_i - \widehat{\mathbf{X}}_j) \|_{\rho}$$

其中 $\mathbf{w}_{ij}$ 为稠密2D对应置信度权重，$\rho$ 为 Huber 范数。全局代价为所有非静态对象代价之和：

$$E_{\mathrm{final}} = \sum_i E(\mathcal{O}_i)$$

该优化通过迭代重加权最小二乘法的 Gauss-Newton 求解：

$$\mathbf{J}^T \mathbf{W} \mathbf{J} \boldsymbol{\tau} = -\mathbf{J}^T \mathbf{W} \mathbf{r}, \quad T_i = T_i \oplus \boldsymbol{\tau}$$

这一设计使系统能够利用所有历史观测约束当前重建，实现了从“时间遗忘”到“时间聚合”的根本转变。

### 创新三：运动分割与物体持久性推理

当物体被完全遮挡后，4DPM 通过运动分割技术推断其持续运动，赋予系统“空间记忆”能力。具体机制包括：

- **空间接触**：通过定向包围盒（OBB）交集判断基元间的物理接触关系
- **速度聚类**：利用规范不变速度比较 $T'(t)^{-1} T'(t-1) = T(t)^{-1} T(t-1)$，证明不同对象的相对速度与未知的规范自由度 $F$ 无关，使跨对象速度聚类成为可能

基于此，不可见物体被链接到可见的父物体，其运动通过传递性推理得以维持。这一能力在抽屉关闭等完全遮挡场景中得到验证——即使抽屉完全闭合，系统仍能重建内部物体和抽屉本体。

### 与基线的本质差异

| 维度 | 基线方法 | 4DPM |
|------|---------|------|
| **运动参数化** | 逐像素运动场或成对帧间变换 | 每基元单一 SE(3) 姿态 |
| **时间覆盖** | 仅观测时刻 | 任意时间戳完整回放 |
| **遮挡处理** | 信息永久丢失 | 运动分割与传递性推理 |
| **优化目标** | 逐对帧对齐或全局 BA | 跨所有非静态对象联合优化 |

这些创新共同构成了从“逐帧估计”到“持久4D重建”的范式转变，使系统在 HO3D 和 Multi-Object 数据集上以显著优势超越所有基线方法。



4DPM 的输入为单目 RGB 视频（如 iPhone 拍摄的随意手持视频），目标是利用所有历史观测，在每一个被观测的时间戳上重建完整的场景几何 $$\{X^0, X^1, ..., X^n\}$$。这一目标与现有动态重建方法有本质区别——后者仅在观测时刻估计几何，缺乏跨时间的信息聚合能力，导致被遮挡或移出视野的物体信息永久丢失。

为克服这一瓶颈，4DPM 将动态场景重建分解为两个核心阶段：**前端（frontend）** 负责从各帧独立提取结构基元与跨帧对应关系；**后端（backend）** 则通过全局优化“拼合”这些基元，实现完整的 4D 重建。

### 前端：基元提取与跨帧关联

前端接收单目 RGB 视频，在选定的关键帧上依次执行三个模块：

1. **几何估计**：使用前馈重建模型 **π³**（Wang et al., ICLR 2026）在每一关键帧的观测时刻估计点云 $$X_i^i$$，将每帧场景表示为无序的 3D 基元集合。
2. **分割与对象跟踪**：对首帧进行超像素分割（SuperPrimitive 风格），并利用 **SAMv2** 将掩码传播至所有关键帧，形成跨时间的对象级分组。每个对象 $$\mathcal{O}$$ 被定义为一组跨时间关联的基元 $$\{S^{t_{\text{start}}}, ..., S^{t_{\text{end}}}\}$$，且被假设为刚体运动。
3. **稠密对应估计**：运行稠密点跟踪网络在相邻关键帧间获取像素级光流及对应的置信度权重 $$w_{ij}$$，为后端优化提供约束。

### 后端：联合姿态优化与时间重映射

后端的核心是将动态重建转化为一个稀疏的 SE(3) 姿态估计问题。每个 3D 基元 $$S_p$$ 被赋予一个时变刚体姿态 $$T(S_p) \in SE(3)$$，其更新通过李代数元素 $$\tau \in \mathfrak{se}(3) \simeq \mathbb{R}^6$$ 完成：

$$T \gets T \oplus \tau$$

优化目标为最小化属于同一对象 $$\mathcal{O}$$ 的相邻基元经姿态变换后的 3D 点距离，按对应置信度加权并使用 Huber 范数：

$$E(\mathcal{O}) = \sum_{(i,j) \in \mathcal{T}(\mathcal{O})} \| \mathbf{w}_{ij} \cdot S_i \cdot \widehat{S}_j (T_j^{-1} T_i \mathbf{X}_i - \widehat{\mathbf{X}}_j) \|_{\rho}$$

全局代价为所有非静态对象的代价之和：

$$E_{\mathrm{final}} = \sum_i E(\mathcal{O}_i)$$

该优化问题通过迭代重加权最小二乘法（Gauss-Newton）联合求解所有对象的姿态：

$$\mathbf{J}^T \mathbf{W} \mathbf{J} \boldsymbol{\tau} = -\mathbf{J}^T \mathbf{W} \mathbf{r}, \quad T_i = T_i \oplus \boldsymbol{\tau}$$

优化前，系统通过对应残差阈值自动识别并冻结静态基元，仅对动态基元进行姿态估计，动静分割作为副产品自然产生（参见 Figure 3）。

### 时间重映射与持久性推理

优化完成后，任意基元 $$S^p$$ 可被变换至任意目标时间戳 $$q$$：

$$T^{p \mapsto q} := [T(S^q)]^{-1} T(S^p)$$

这一操作将所有历史观测“拉回”至同一坐标系，实现完整的 4D 可回放重建。

对于被遮挡或移出视野的物体，系统通过**运动分割**技术维持其空间记忆：基于空间接触（OBB 交集）和速度聚类（规范不变速度比较）推断不可见物体与可见父物体的关联，从而外推其持续运动。速度比较的规范不变性由下式保证：

$$T'(t)^{-1} T'(t-1) = T(t)^{-1} T(t-1)$$

这意味着不同对象的相对速度与未知的规范自由度 $$F$$ 无关，使跨对象速度聚类成为可能。

### 关键设计决策

这一管道设计的核心洞察在于：**将场景分解为刚性运动的 3D 基元，并将逐像素运动场压缩为稀疏的每基元 SE(3) 姿态**。相比现有方法（如 **St4track**（Feng et al., CVPR 2025）的成对帧间变换或 **PO-MATO**（Zhang et al., ICCV 2025）的逐点匹配），这一参数化将动态重建的维度从逐像素运动估计大幅降低至每个基元仅需 6 个自由度，同时通过对象级分组引入了结构化的运动约束，使得联合优化在计算上可行且鲁棒。

### 补充图表

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/001_Figure_1.jpg]]
*Figure 1: Our method (4DPM) takes in casual monocular videos (captured by an iPhone) and outputs complete 3D scene reconstructions at every observed timestamp, using all scene observations. The method takes in the outputs of a feedforward reconstruction model (top row) and glues dynamic geometry observations across time (middle row). This results in a complete and accurate geometric reconstruction, which re-uses observations from all timestamps (bottom row)*



### 问题形式化与基元运动参数化

4DPM 将动态场景重建问题形式化为：给定一段单目 RGB 视频的关键帧集合，目标是重建每个观测时刻 $t$ 的完整场景几何 $\mathbf{X}^t$。核心创新在于将场景分解为一组**刚性 3D 基元**（rigid 3D primitives），每个基元 $S$ 被表示为一个带分割掩码的 3D 点云，并赋予一个随时间变化的 $\mathrm{SE}(3)$ 姿态 $T(S^p)$。这一参数化将原本需要逐像素估计的稠密运动场压缩为**每个基元仅需一个 6 自由度姿态**的稀疏表示，从根本上降低了动态重建的维度。

每个基元的姿态更新采用李代数参数化：
$$T \gets T \oplus \tau \tag{1}$$
其中 $\tau \in \mathfrak{se}(3) \simeq \mathbb{R}^6$ 为李代数元素，$\oplus$ 表示通过指数映射将李代数元素转换为 $\mathrm{SE}(3)$ 变换并与当前姿态复合。这一参数化保证了优化过程中姿态始终位于 $\mathrm{SE}(3)$ 流形上。

### 前端：几何估计、分割与稠密对应

前端模块负责为后端优化提供初始几何和跨帧对应关系，包含三个关键步骤：

1. **几何估计**：对每个关键帧运行前馈重建模型 **π³**（Wang et al., ICLR 2026），估计各观测时刻的点云 $\mathbf{X}_i^i$，作为基元的初始几何。

2. **分割与对象跟踪**：对首帧进行超像素分割，利用 **SAMv2** 将掩码传播至所有关键帧，形成跨时间的对象级分组。每个对象 $\mathcal{O}$ 被定义为一组在时间上连续的基元集合 $\mathcal{O} = \{ S^{t_{\text{start}}}, \dots, S^{t_{\text{end}}} \}$，并假设其内部所有基元作刚体运动。

3. **稠密对应估计**：运行稠密点跟踪网络获取相邻关键帧间的像素级光流及对应置信度权重 $\mathbf{w}_{ij}$，这些权重将用于后端优化中的残差加权。

### 后端：联合姿态优化

后端优化的核心目标是最小化属于同一对象的基元在 3D 空间中的对齐误差。对于单个对象 $\mathcal{O}$，稠密对齐代价函数定义为：

$$E(\mathcal{O}) = \sum_{(i,j) \in \mathcal{T}(\mathcal{O})} \| \mathbf{w}_{ij} \cdot S_i \cdot \widehat{S}_j (T_j^{-1} T_i \mathbf{X}_i - \widehat{\mathbf{X}}_j) \|_{\rho} \tag{2}$$

其中 $\mathcal{T}(\mathcal{O})$ 为对象 $\mathcal{O}$ 内具有稠密对应关系的基元对集合；$S_i$ 和 $\widehat{S}_j$ 为选择算子，分别提取基元 $i$ 和基元 $j$ 中具有对应关系的点；$T_i, T_j$ 为对应基元的 $\mathrm{SE}(3)$ 姿态；$\| \cdot \|_{\rho}$ 为 Huber 范数，用于增强对离群对应的鲁棒性。直观上，该代价函数将基元 $i$ 的点通过 $T_i$ 变换到世界坐标系，再通过 $T_j^{-1}$ 拉回到基元 $j$ 的局部坐标系，度量其与基元 $j$ 对应点 $\widehat{\mathbf{X}}_j$ 的 3D 距离，并按对应置信度 $\mathbf{w}_{ij}$ 加权。

全局联合优化代价为所有非静态对象的代价之和：
$$E_{\mathrm{final}} = \sum_i E(\mathcal{O}_i) \tag{3}$$

优化采用**迭代重加权最小二乘法**，通过 Gauss-Newton 方法求解。每次迭代中，解析计算雅可比矩阵 $\mathbf{J}$，求解正规方程：
$$\mathbf{J}^T \mathbf{W} \mathbf{J} \boldsymbol{\tau} = -\mathbf{J}^T \mathbf{W} \mathbf{r}, \quad T_i = T_i \oplus \boldsymbol{\tau} \tag{4}$$
其中 $\mathbf{W}$ 为权重矩阵（由 Huber 重加权和对应置信度共同决定），$\mathbf{r}$ 为残差向量，$\boldsymbol{\tau}$ 为所有基元姿态的增量李代数参数。解析雅可比的使用保证了优化效率。

### 动静分割

在优化前，系统通过**冻结静态基元**来降低问题维度：对每个基元计算其稠密对应残差，若残差低于阈值，则判定该基元为静态，将其姿态固定为单位变换，不参与后续优化。这一策略不仅减少了优化变量数量，还自然地产生了运动分割作为副产品（见 Figure 3）。

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/003_Figure_3.jpg]]
*Figure 3: Static vs dynamic segmentation. We visualise all estimated primitives on the left. Before motion estimation, we freeze primitives with insufficiently high correspondence residuals, assuming they are static. On the right, only dynamic primitives are shown. Our system produces motion segmentation as a byproduct*

### 时间重映射与 4D 可回放重建

优化完成后，任意基元 $S^p$（在时刻 $p$ 观测）可被变换至任意目标时刻 $q$：
$$T^{p \mapsto q} := [T(S^q)]^{-1} T(S^p) \tag{5}$$
该变换先将基元变换到其最新观测帧的坐标系（通过 $T(S^p)$），再拉回至目标时刻 $q$（通过 $[T(S^q)]^{-1}$）。通过将所有基元重映射到同一时刻，系统可在任意观测时间戳回放完整的 4D 场景重建。

### 运动分割与持久性推理

为实现对被遮挡物体的运动外推，系统基于两个准则识别潜在的父物体：

1. **空间接触**：通过基元的定向包围盒（OBB）交集判断物体间的物理接触。
2. **速度相似性**：比较不同物体的规范不变速度。关键洞察在于，尽管每个物体的绝对速度依赖于未知的规范自由度 $F$，但其相对速度与 $F$ 无关：
$$T'(t)^{-1} T'(t-1) = T(t)^{-1} T(t-1) \tag{6}$$
其中 $T'$ 和 $T$ 分别表示不同规范下的姿态。这一性质使得跨对象的速度聚类成为可能。当某物体不可见时，系统通过将其链接到仍可见的父物体，传递性地推断其持续运动（如 Figure 5 中抽屉关闭后内部物体的重建）。

### 补充图表

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/002_Figure_2.jpg]]
*Figure 2: 4D reconstruction with 4DPM. (left) Our frontend takes in a monocular RGB video and splits it into a set of 3D primitives. Each primitive is represented as a 3D point map in the world coordinate space, cut out by a segmentation mask. These primitives are matched across time (visualised with consistent colours) to form consistent entities across time, to which we refer as objects. (top right) Freeze Static Primitives Given geometric observations positioned at their respective timestamps, we “glue” primitives belonging to the same object across time according to their estimated dense 2D correspondences. (bottom right) The resulting complete reconstruction can be replayed across all observed t...*



## 实验与关键发现

### 评估设置与基准

4DPM在两个动态场景数据集上进行评估：**HO3D**（多视角手-物体交互数据集）和**Multi-Object**（多物体动态场景数据集）。评估聚焦于动态场景部分，排除辅助相机捕获但主相机从未观测到的静态区域，以确保完整性（recall）度量的有效性。长序列被分割为150帧的独立块进行测试，报告每序列的平均结果。所有方法的预测几何通过Umeyama对齐到真值坐标系，消除Sim(3)规范自由度的影响。

主要评估指标为**F-score**（1cm阈值），即精度（预测点中与真值距离<1cm的比例）与召回率（真值点中被覆盖的比例）的调和平均。对比基线包括：
- **π³ (last view)**（Wang et al., ICLR 2026）：仅使用最新帧点云，代表无持久性的动态重建下限；
- **π³ (time-warped)**（Wang et al., ICLR 2026）：使用2D对应关系进行时间变换的简单聚合方案；
- **St4track**（Feng et al., CVPR 2025）：基于DUSt3R的4D跟踪与重建方法；
- **PO-MATO**（Zhang et al., ICCV 2025）：基于DUSt3R的动态3D重建方法。

### 主实验结果

**HO3D数据集**（Table 1）：4DPM在动态物体扫描任务上以**0.7573的平均F-score**显著优于所有基线方法，提供了精度与完整性的最佳平衡。各基线的F-score均明显低于此值，验证了基于基元拼合的持久重建策略在单物体动态扫描场景中的有效性。

**Multi-Object数据集**（Table 2）：在多物体动态重建任务上，4DPM取得了**0.7948的平均F-score**，在所有序列上均显著优于基线方法。定性对比（Figure 4）进一步显示，4DPM成功处理了多物体运动场景中的挑战性物体（如旋转球体、机器人夹爪），正确聚合了所有历史观测，生成了完整且准确的物体扫描结果。相比之下，基线方法在物体被遮挡或移出视野后无法恢复其几何信息。

### 物体持久性能力

Figure 5展示了4DPM的核心能力——**物体持久性**。在抽屉关闭序列中，当抽屉完全关闭后（最右列），内部物体及抽屉本体已被完全遮挡。4DPM通过运动分割技术将抽屉本体与其前面板关联，并基于空间接触和速度聚类，将内部物体通过传递关系与可见的抽屉前面板关联，从而推断其持续运动。即使在完全不可见的情况下，系统仍能重建被遮挡物体的几何，体现了基元表示赋予的空间记忆能力。

### 消融与失败模式

本文实验部分未报告系统性的消融研究，主要对比对象为上述基线方法。从方法设计角度，以下组件的贡献可通过基线对比间接推断：
- **持久性聚合**：π³ (last view) 与4DPM的差距量化了历史观测聚合的收益；
- **基元拼合优化**：π³ (time-warped) 使用简单时间变换，其与4DPM的差距反映了联合SE(3)姿态优化的价值；
- **运动分割与外推**：St4track和PO-MATO缺乏遮挡物体的运动外推机制，在Multi-Object数据集上的差距体现了运动分割模块的作用。

**已知局限**：
- 系统假设每个基元为刚体，无法表示非刚性形变（如布料、软体物体）；
- 当前处理固定长度的视频片段（每段150帧），增量式建图能力尚未探索；
- 静态/动态分类依赖对应残差阈值，该阈值的自适应调整策略及对复杂相机运动场景的泛化性有待研究。

### 关键图表结论

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | HO3D数据集上F-score达0.7573，显著优于所有基线 |
| **Table 2** | Multi-Object数据集上F-score达0.7948，多物体场景重建能力领先 |
| **Figure 3** | 动静分割可视化：系统通过对应残差自动区分静态与动态基元 |
| **Figure 4** | 定性对比：4DPM在挑战性多物体场景中正确聚合历史观测，基线方法则出现几何缺失 |
| **Figure 5** | 物体持久性：完全遮挡后仍能重建被遮挡物体的几何，展示空间记忆能力 |

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on HO3D dataset. We report F-score (threshold at 1 cm) per sequence for all methods. Average Fscore, precision, and recall across all sequences are also reported. Our method outperforms all baselines by a substantial margin in terms of F-score for dynamic object scanning, providing the best balance between completeness and accuracy. Best is highlighted as bold, while second-best is underscored*

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on Multi-Object dataset. Input video frames are shown in purple. Below each video, we visualise all observed point-maps time-warped to the latest timestamp. Our system successfully handles multi-object motion and performs well on particularly challenging objects such as the spinning ball and robot gripper (top row). We provide a top-down view of multiple objects spinning on a rotating base (bottom row). Our method correctly aggregates all observations, resulting in complete and accurate object scans*

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation on Multi-Object dataset. We report F-score (threshold at 1 cm) per sequence for all methods. Average F-score, precision, and recall across all sequences are also reported. Our method significantly outperforms all baselines in terms of F-score multi-object dynamic reconstruction, providing the best balance between completeness and accuracy. Best is highlighted as bold, while second-best is underscored*

![[assets/figures/papers/paper_list_l2076_https_openaccess_thecvf_com_content_CVPR2026_html_Mazur_4D_Primitive_Mac/figures/007_Figure_5.jpg]]
*Figure 5: Object permanence capabilities. In (top row) we show input frames of a drawer closing sequence. The resulting reconstruction estimated with 4DPM from the top-down view in the (bottom row). When the drawer is fully closed (rightmost column), our method still reconstructs objects inside the drawer and the drawer body, despite it being completely occluded. This showcases object permanence capabilities of 4DPM. The top of the drawer is removed from reconstruction for better viewing*



## 定位与知识库关联

### 核心设计理念：从逐帧重建到持久4D表示

当前单目动态重建方法的核心瓶颈在于**缺乏跨时间的持久性**。现有方法仅在观测时刻估计几何，历史观测信息被丢弃，导致被遮挡或移出视野的物体信息永久丢失。4D Primitive-Mache（4DPM）通过一个根本性的参数化转换打破这一限制：**将场景分解为一组刚性运动的3D基元，每个基元仅需一个SE(3)姿态参数**。这一紧凑表示将复杂的逐帧密集映射问题简化为每个基元的单一刚体运动估计，大幅降低了动态重建的维度，同时使所有观测能够跨时间聚合。

### 与基线方法的关系

4DPM建立在**前馈重建模型**π³（Wang et al., ICLR 2026）的几何估计基础之上，但与其两个变体基线形成鲜明对比：
- **π³ (last view)**：仅使用最新帧点云，代表无持久性的动态重建下限；
- **π³ (time-warped)**：使用2D对应关系进行简单时间变换，代表朴素的时间聚合方案。

这两类基线均缺乏结构化的运动模型，无法推理场景中物体的长期运动。

与同样基于DUSt3R的**St4track**（Feng et al., CVPR 2025）和**PO-MATO**（Zhang et al., ICCV 2025）相比，4DPM的区分度更为显著：
- St4track和PO-MATO通过建立帧间对应关系将点云变换至不同时间帧，本质上仍是对成对帧间变换的建模，维度高且缺乏结构化约束；
- 4DPM通过**对象级别的基元分组与联合姿态优化**，将优化目标从逐对帧对齐提升为跨所有非静态对象的全局联合优化，直接最小化属于同一对象的基元3D点之间的距离，并按对应置信度加权。

### 关键方法差异

| 维度 | 基线方法 | 4DPM |
|------|---------|------|
| 运动参数化 | 逐像素运动场或成对帧间变换 | 每基元一个SE(3)姿态，稀疏且紧凑 |
| 时间覆盖 | 仅在观测时刻重建几何 | 所有观测变换至任意时间戳，完整4D可回放 |
| 被遮挡物体 | 不可见后信息永久丢失 | 通过运动分割与父物体关联，实现运动外推 |
| 优化目标 | 逐对帧点云对齐或全局BA | 跨所有非静态对象的联合优化，直接最小化基元间3D距离 |

### 适用边界与局限

4DPM的有效性建立在两个核心假设之上：
1. **刚体假设**：每个基元被建模为刚体，通过SE(3)姿态描述其运动。这一假设对刚性物体（如机械臂、抽屉、球体）效果显著，但**无法表示复杂的非刚性形变**（如布料、软体物体）。论文明确指出，扩展至非刚性形变同时保持计算效率是未来重要方向。
2. **批处理模式**：当前系统处理固定长度的视频片段（每段150帧），**尚未支持增量建图能力**——即场景表示无法在扩展序列上逐步构建和更新，这限制了其在长期持续运行场景（如机器人持久环境感知）中的应用。

### 开放问题与未来方向

1. **非刚性形变扩展**：如何在维持紧凑基元表示优势的同时，引入对非刚性形变的建模能力？可能的路径包括为基元赋予可学习的形变场，或结合物理先验约束。
2. **增量式建图**：如何使场景表示在长序列上逐步构建和更新？这需要解决基元生命周期的管理问题——包括基元的创建、合并、删除，以及姿态估计的在线更新机制。
3. **学习先验的融合**：基于基元的表示是否能与物体级别的动态预测先验结合？例如，利用学习到的物体运动模式进一步提升遮挡场景下的运动推理鲁棒性。
4. **动静分类的自适应**：当前系统的静态/动态分类依赖对应残差阈值，该阈值的自适应调整策略及对复杂相机运动场景的泛化性有待进一步研究。

### 在知识库中的定位

4DPM在动态场景重建领域占据了一个独特的位置：它**桥接了前馈几何估计与结构化运动推理**。与纯学习的前馈方法（如π³）相比，它通过优化后端引入了时间一致性；与传统的SLAM/BA方法相比，它利用前馈模型的强几何先验避免了脆弱的帧间匹配。这种“前馈+优化”的混合范式，结合基元级别的紧凑运动参数化，为持久4D重建提供了一个可扩展的框架，尤其适用于以刚体运动为主的动态场景（如机器人操作、物体扫描）。



## 原文 PDF

![[paperPDFs/CVPR_2026/4D_Primitive_Mache_Glueing_Primitives_for_Persistent_4D_Scene_Reconstruction.pdf]]

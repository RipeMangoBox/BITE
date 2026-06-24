---
title: "Dynamic-eDiTor: Training-Free Text-Driven 4D Scene Editing with Multimodal Diffusion Transformer"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dynamic_eDiTor_Training_Free_Text_Driven_4D_Scene_Editing_with_Multimodal_Diffusion_Transformer.pdf
project_link: "https://di-lee.github.io/dynamic-eDiTor/"
code_link: null
aliases:
- DE
- Dynamic-eDiTor
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在统一相机-时间网格上部署MM-DiT，通过局部时空子网格注意力（STGA）联合处理相邻视图与时间帧，并利用上下文令牌传播（CTP）在网格中全局扩散融合特征，从而在不增加训练的前提下强制执行多视角和时间一致性。
primary_logic: 将多视角视频帧组织为相机-时间网格，对每个2×2子网格应用STGA实现跨视图和时间相邻帧的联合注意力融合；随后通过CTP的令牌继承与光流引导替换，将局部融合信息传播至整个网格，最终直接优化预训练的4DGS，无需迭代式数据集更新即可实现全局一致的4D编辑。
claims:
- STGA扩展MM-DiT的双流自注意力，在局部子网格内聚合跨视角和时间相邻帧特征，形成局部一致性基础。
- CTP通过结构化的遍历路径显式传播令牌，重叠区域完全继承，非重叠区域通过光流引导替换，确保全局一致性。
- 编辑后的帧直接用于优化预训练的4DGS，避免迭代式数据集更新（IDU），从而保持整体结构稳定性。
- DyNeRF 上 CLIP_dir↑ = 0.1849
---

# Dynamic-eDiTor: Training-Free Text-Driven 4D Scene Editing with Multimodal Diffusion Transformer

> [!tip] 核心洞察
> 将多视角视频帧组织为相机-时间网格，对每个2×2子网格应用STGA实现跨视图和时间相邻帧的联合注意力融合；随后通过CTP的令牌继承与光流引导替换，将局部融合信息传播至整个网格，最终直接优化预训练的4DGS，无需迭代式数据集更新即可实现全局一致的4D编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | Dynamic-eDiTor：基于多模态扩散Transformer的训练免费文本驱动4D场景编辑 |
| 英文题名 | Dynamic-eDiTor: Training-Free Text-Driven 4D Scene Editing with Multimodal Diffusion Transformer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00677) · [Project](https://di-lee.github.io/dynamic-eDiTor/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Dynamic-eDiTor |
| Dataset | DyNeRF |

> [!tip] 效果简介
> - DyNeRF 上，CLIP_dir↑ 0.1849 vs 0.1501 (Instruct-4DGS) (+0.0348)；CLIP_sim↑ 0.6397 vs 0.6342 (Instruct-4DGS) (+0.0055)；User Overall Quality (%) 48.95 vs 27.57 (Instruct4D-to-4D) (+21.38)。

## 概述

4D场景编辑旨在对动态三维场景进行语义级操控，同时保持多视角几何一致性与时间运动连贯性。现有方法（如 **Instruct4D-to-4D**、**Instruct-4DGS**、**CTRL-D**）普遍依赖逐帧独立的2D扩散模型进行编辑，缺乏跨视角与跨时间的联合处理机制，导致运动失真、几何漂移和编辑不完整等瓶颈。

针对上述问题，本文提出 **Dynamic-eDiTor**，一种训练免费的文本驱动4D场景编辑框架。其核心思路是：将多视角视频帧组织为统一的**相机-时间网格**，并在其上部署多模态扩散Transformer（MM-DiT），通过两个关键机制实现时空一致性编辑——**时空子网格注意力（Spatio-Temporal Sub-Grid Attention, STGA）** 在局部 $2\times 2$ 子网格内联合关注相邻视图与时间帧，形成局部一致性基础；**上下文令牌传播（Context Token Propagation, CTP）** 则通过令牌继承与光流引导替换，将局部融合信息全局扩散至整个网格。编辑后的帧直接用于一次性优化预训练的4D高斯溅射（4DGS），避免了传统方法中迭代式数据集更新（Iterative Dataset Update, IDU）带来的结构不稳定性。

在DyNeRF数据集上的实验表明，Dynamic-eDiTor在编辑保真度（CLIP_dir 0.1849）和用户偏好（总体质量48.95%）上显著优于现有基线，同时保持了可竞争的重建保真度。消融研究验证了STGA与CTP在消除运动模糊和几何漂移方面的互补作用，以及将STGA限制在MM-DiT前30层的关键设计选择。

**方法谱系与知识库定位**：Dynamic-eDiTor继承了两条技术路线——基于MM-DiT的图像编辑能力（源自 **FLUX** 架构，Black Forest Labs, 2024）和4DGS的动态场景表示。与 **Instruct-4DGS** 等使用U-Net扩散模型逐帧编辑的方法不同，本方法首次在统一时空网格上利用MM-DiT的双流自注意力实现跨视角-时间联合编辑，属于训练免费4D编辑框架的新范式。

## 背景与动机

### 4D场景编辑的兴起与核心挑战

4D场景表示——即在三维空间基础上引入时间维度，对动态场景进行建模——近年来取得了显著进展。以4D高斯溅射（4D Gaussian Splatting, 4DGS）为代表的显式表示方法，能够从多视角视频中重建出高质量的可渲染动态场景。然而，如何对这些预训练的4D场景进行灵活、高质量的编辑，使其响应用户的文本指令，仍然是一个开放且极具挑战的问题。

现有4D场景编辑方法面临一个根本性的瓶颈：**它们普遍依赖基于U-Net架构的2D扩散模型对每一帧进行独立编辑，缺乏在编辑过程中同时维护多视角一致性和时间一致性的机制**。具体而言，逐帧独立的编辑策略导致三个层面的严重退化：

1. **运动失真**：相邻帧之间编辑结果的不连贯破坏了原始场景的时序动态，产生抖动和闪烁。
2. **几何漂移**：不同视角下同一区域的编辑结果不一致，导致3D几何结构在重建时发生偏移或坍塌。
3. **编辑不完整**：缺乏跨帧信息传递使得编辑效果无法在时空维度上均匀覆盖，部分区域编辑不足或过度。

### 现有方法的缺口

当前主流的文本驱动4D编辑方法——如**Instruct4D-to-4D**、**Instruct-4DGS**和**CTRL-D**——虽然在特定场景下取得了一定效果，但均受限于上述框架性缺陷。这些方法通常采用**迭代式数据集更新（Iterative Dataset Update, IDU）** 策略：先对部分帧进行2D编辑，再将其用于更新4D表示，随后重新渲染并再次编辑，如此循环。IDU不仅计算开销大，而且在迭代过程中容易累积误差，导致编辑结果偏离原始场景结构。

更深层的问题在于，这些方法所使用的2D扩散模型（以U-Net为骨干）本身缺乏对多视角和时序关系的原生建模能力。尽管可以通过注意力注入、特征对齐等后处理手段进行补救，但这些手段本质上是在一个“逐帧处理”的框架下打补丁，无法从根本上解决时空一致性问题。

### 本文动机：从2D逐帧编辑到统一时空编辑

上述分析揭示了一个关键洞察：**4D编辑的核心矛盾不在于2D编辑模型的能力不足，而在于缺乏一个将多视角视频帧作为统一时空整体进行联合处理的框架**。近年来，多模态扩散Transformer（MM-DiT）的兴起为突破这一瓶颈提供了新的可能。与U-Net不同，MM-DiT基于Transformer架构，其自注意力机制天然支持对不同来源的令牌进行灵活拼接和联合建模，这为在扩散过程中同时融合多视角和时序信息创造了架构基础。

基于这一认识，本文提出**Dynamic-eDiTor**，一个无需训练的文本驱动4D场景编辑框架。其核心动机是：**将多视角视频帧组织为统一的相机-时间网格，在MM-DiT的扩散过程中引入局部时空联合注意力与全局令牌传播机制，从而在不增加训练的前提下强制执行多视角和时间一致性**。该方法从根本上跳出了“逐帧编辑+后处理对齐”的范式，转而追求编辑过程本身即具备时空一致性，为4D场景编辑提供了一个更加简洁、鲁棒的解决方案。

## 核心创新

Dynamic-eDiTor 的核心创新在于将4D场景编辑从“逐帧独立2D扩散”范式升级为“统一时空联合编辑”范式。其关键突破可归纳为三个层面的 **changed slots**，分别对应编辑框架基础、时空一致性机制和4D表示优化策略的质变。

### 从U-Net到MM-DiT：编辑框架的范式迁移

现有4D编辑方法（如 **Instruct4D-to-4D**、**Instruct-4DGS**、**CTRL-D**）普遍依赖基于U-Net架构的2D扩散模型对多视角视频进行逐帧独立编辑。这种“单帧处理、事后缝合”的策略在本质上割裂了视角间和时间帧间的语义关联，导致运动失真、几何漂移和编辑不完整等系统性缺陷。

Dynamic-eDiTor 直接将编辑过程构建在 **多模态扩散Transformer（MM-DiT）** 之上。MM-DiT 的双流自注意力机制天然支持文本与图像特征的联合建模，为跨帧、跨视角的信息融合提供了统一的表示空间。在此基础上，论文提出将整个多视角视频组织为一个 **相机-时间网格**（Camera–Time Grid）：

$$Grid = \{ f_{v,t} \ | \ v \in [0, \ldots, V], \ t \in [0, \ldots, T] \}$$

这一网格化表示将原本离散的帧集合转化为结构化的时空张量，使得编辑过程可以在局部和全局两个粒度上同时维护多视角一致性与时间一致性。

### 从孤立编辑到联合时空一致性：STGA与CTP的协同机制

传统方法缺乏对多视角和时间维度的联合处理能力。Dynamic-eDiTor 通过两个互补的机制解决了这一问题：

**Spatio-Temporal Sub-Grid Attention (STGA)** 在局部 $2\times2$ 子网格内执行跨视角和时间相邻帧的联合注意力融合。对于每个子网格 $\mathcal{S}_{v,t} = \{ f_{v,t}, f_{v+1,t}, f_{v,t+1}, f_{v+1,t+1} \}$，STGA 将所有帧的图像特征拼接为联合键值对，并与文本流一起参与注意力计算：

$$\operatorname{STGA}(\mathcal{S}_{v,t}) = \operatorname{softmax}([Q_{\mathrm{txt}}, \operatorname{RoPE}(Q_{f_{v,t}})] \cdot [K_{\mathrm{txt}}, \operatorname{RoPE}(K_{\mathcal{S}_{v,t}})]^{\top} / \sqrt{d_k}) \cdot [V_{\mathrm{txt}}, V_{\mathcal{S}_{v,t}}]$$

这一设计使每个帧在编辑时能同时“看见”其相邻视角和相邻时刻的内容，从而在局部范围内形成一致性基础。

**Context Token Propagation (CTP)** 则将局部融合信息传播至整个网格，确保全局一致性。CTP 沿结构化的遍历路径显式传播令牌：在子网格间的重叠区域采用**全令牌继承**（Full Token Inheritance），直接复用前一子网格的融合令牌；在非重叠的时间区域则通过**光流引导令牌替换**（Flow-guided Token Replacement）进行传播：

$$\hat{\phi}_{\mathrm{r}}(S_{v,t}) = \mathrm{Warp}(\mathbf{F}_{t \rightarrow t-1}(x,y), \phi_{\mathrm{r}}(S_{v,t-1}))$$

$$\phi_{\mathrm{r}}(S_{v,t}) = \mathrm{M} \odot \hat{\phi}_{\mathrm{r}}(S_{v,t}) + (1 - \mathrm{M}) \odot \phi_{\mathrm{r}}(S_{v,t})$$

光流一致性掩码 $\mathrm{M}$ 确保仅在有效映射区域替换令牌，无效区域保留原始令牌，避免错误传播。消融实验（Table 3）证实，CTP-Full 和 CTP-Flow 缺一不可——单独移除任一部分均会导致全局时空一致性的显著下降。

### 从迭代更新到一次性直接优化：4DGS优化策略的简化

传统方法（如 Instruct-4DGS）采用 **Iterative Dataset Update (IDU)** 策略：编辑后的帧需反复注入训练流程，逐步更新4D表示。这一过程不仅计算开销大，还可能因迭代累积误差导致结构退化。

Dynamic-eDiTor 利用 STGA 和 CTP 已确保编辑帧的全局一致性，因此可以直接将全部编辑帧一次性用于优化预训练的4DGS模型：

$$\mathcal{G}_{\mathrm{edit}}' = \arg\min_{\mathcal{G}} \sum_{v,t \in V,T} \|\hat{f}_{v,t} - f_{v,t}^{\mathrm{edit}}\| + \mathcal{L}_{\mathrm{tv}}$$

这一简化消除了 IDU 的迭代开销，同时保持了整体结构的稳定性。

### 关键设计选择：STGA的层范围约束

一个值得注意的实现细节是 STGA 并非在 MM-DiT 的全部层上应用。层范围分析（Figure 3, Table 5）表明，将 STGA 限制在前约30层（0-29）能在一致性与编辑保真度之间取得最佳平衡。若在更深的层上施加 STGA，会导致纹理重复和编辑质量下降；完全不加 STGA 则无法建立跨帧一致性。这一发现揭示了 MM-DiT 不同层的功能分化：浅层负责建立跨帧语义对应，深层则更专注于单帧的细节生成。

综上，Dynamic-eDiTor 的创新本质在于**将4D编辑从“2D扩散+后处理”的松散组合转变为一个内建时空一致性的统一框架**，其 STGA-CTP 协同机制和直接4DGS优化策略共同构成了这一转变的技术支柱。

## 整体框架

Dynamic-eDiTor 提出了一种训练免费、文本驱动的 4D 场景编辑框架，其核心设计思想是将多视角视频帧组织为一个统一的**相机-时间网格**（Camera–Time Grid），并在此网格上部署基于多模态扩散 Transformer（MM-DiT）的时空一致性编辑机制，最终直接优化预训练的 4D 高斯溅射（4DGS）模型。

### Pipeline 总览

整个框架的输入为：一个预训练的 4DGS 场景表示 $\mathcal{G}$，以及一条描述编辑目标的文本指令。从 $\mathcal{G}$ 渲染得到的多视角视频帧 $\{f_{v,t}\}$ 被组织为统一的网格结构：

$$Grid = \{ f_{v,t} \ | \ v \in [0, \ldots, V], \ t \in [0, \ldots, T] \}$$

其中 $v$ 为视点索引，$t$ 为时间索引。该网格是后续所有编辑操作的基础数据结构。

编辑流程由三个核心模块串联构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/002_Figure_2.jpg]]
*Figure 2: Dynamic-eDiTor Overview. We represent the multi-view video as a unified camera–time grid. Dynamic-eDiTor combines Spatio-Temporal Sub-Grid Attention (STGA), which performs locally coherent cross-view and temporal fusion within each sub-grid, with Context Token Propagation (CTP), which globally propagates the aggregated features across the grid via Full Token Inheritance and Flow-guided Token Replacement for robust spatio-temporal consistency enforcement. Together, these modules enable seamless, globally consistent multi-view video editing without additional training, while directly optimizing the pre-trained 4DGS*

1. **Spatio-Temporal Sub-Grid Attention (STGA)**：在局部 $2\times 2$ 子网格 $\mathcal{S}_{v,t} = \{ f_{v,t}, f_{v+1,t}, f_{v,t+1}, f_{v+1,t+1} \}$ 内执行跨视角和时间的联合注意力融合，为每个帧聚合来自相邻视点和相邻时刻的特征，形成局部一致性基础。

2. **Context Token Propagation (CTP)**：通过结构化的遍历路径，将 STGA 产生的局部融合信息显式传播至整个网格。传播机制包含两个关键策略：在重叠区域执行**全令牌继承**（Full Token Inheritance），在非重叠时间区域通过**光流引导令牌替换**（Flow-guided Token Replacement）进行更新，确保全局时空一致性。

3. **直接 4DGS 优化**：编辑后的帧 $\{f_{v,t}^{\text{edit}}\}$ 被直接用于一次性优化预训练的 4DGS 模型，无需迭代式数据集更新（Iterative Dataset Update, IDU）。优化目标为：

$$\mathcal{G}_{\text{edit}}' = \arg\min_{\mathcal{G}} \sum_{v,t \in V,T} \|\hat{f}_{v,t} - f_{v,t}^{\text{edit}}\| + \mathcal{L}_{\text{tv}}$$

其中 $\hat{f}_{v,t}$ 为编辑后 4DGS 的渲染帧，$\mathcal{L}_{\text{tv}}$ 为全变分正则化损失，用于抑制噪声。

### 模块间的因果链路

STGA 与 CTP 构成**局部-全局**的递进式一致性保障体系。STGA 扩展了 MM-DiT 的双流自注意力机制，将子网格内四帧的图像特征拼接为联合键值对 $K_{\mathcal{S}_{v,t}}, V_{\mathcal{S}_{v,t}}$，与文本流特征共同参与注意力计算（Eq. 5），使每个帧能够同时关注其跨视图和时间邻居。然而，STGA 的作用范围局限于 $2\times 2$ 子网格内部，相邻子网格之间缺乏显式的信息交换。

CTP 填补了这一缺口：它沿着相机-时间网格的遍历路径，将前一子网格 STGA 输出的融合令牌传递至当前子网格。对于重叠区域（如左列两帧已在上一子网格中作为右列出现），直接继承已融合的令牌；对于非重叠的时间相邻区域，则利用光流 $\mathbf{F}_{t \rightarrow t-1}$ 将令牌从 $t-1$ 时刻变形至 $t$ 时刻（Eq. 6），并通过光流一致性掩码 $\mathrm{M}$ 进行选择性替换（Eq. 7），无效变形区域保留原始令牌。这一传播机制使得局部一致性信息能够逐步扩散至整个网格，最终实现全局一致的 4D 编辑。

### 关键设计决策

框架中有一个重要的经验性设计选择：STGA 并非在 MM-DiT 的所有 Transformer 层上执行，而是仅应用于前约 30 层（0–29 层）。如 Figure 3 和 Table 5 所示，这一层范围在一致性指标（Warping Error、MEt3R）与编辑保真度（CLIP Text-Image Directional Similarity）之间取得了最佳平衡。若将 STGA 扩展至更深层，会导致纹理重复和编辑质量下降；若完全不使用 STGA，则多视角和时间编辑出现明显不一致。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 网格构建 | 预训练 4DGS + 多视点/时间参数 | 相机-时间网格 $\{f_{v,t}\}$ |
| STGA | 网格 + 文本指令 | 局部融合的帧特征 |
| CTP | STGA 输出 + 光流 | 全局一致的编辑帧 $\{f_{v,t}^{\text{edit}}\}$ |
| 直接优化 | 编辑帧 + 预训练 4DGS | 编辑后的 4DGS 模型 $\mathcal{G}_{\text{edit}}'$ |

整个流程无需对 MM-DiT 进行微调，也无需迭代式地更新训练数据集，体现了“训练免费”的核心优势。一次完整的 4D 编辑（以 DyNeRF 的 “coffee martini” 场景为例）在单张 NVIDIA H100 GPU 上耗时约 51 分钟。

## 核心模块与公式推导

Dynamic-eDiTor 的核心由三个紧密耦合的模块构成：**相机‑时间网格构建**、**时空子网格注意力 (STGA)** 与 **上下文令牌传播 (CTP)**，以及最终的 **直接 4DGS 优化**。整个流程围绕一个统一的相机‑时间网格展开，在该网格上通过局部联合注意力与全局令牌传播强制执行多视角‑时间一致性，无需额外训练。

---

### 3.1 相机‑时间网格构建

给定预训练的 4DGS 模型，首先从所有视点 $v$ 和时间步 $t$ 渲染多视角视频帧，并将其组织为统一网格：

$$Grid = \{ f_{v,t} \ | \ v \in [0, \ldots, V], \ t \in [0, \ldots, T] \}$$

其中 $f_{v,t}$ 表示视点 $v$ 在时间 $t$ 的渲染帧。该网格为后续的局部融合与全局传播提供了结构化的时空索引基础。

---

### 3.2 时空子网格注意力 (STGA)

STGA 在 MM‑DiT 的双流自注意力机制上进行扩展，使其能够在局部子网格内联合关注相邻视点与相邻时间帧，从而建立起局部一致性基础。

**子网格定义**：对于网格中的每个位置 $(v,t)$，构造一个 $2\times2$ 的局部子网格：

$$\mathcal{S}_{v,t} = \{ f_{v,t}, f_{v+1,t}, f_{v,t+1}, f_{v+1,t+1} \}$$

该子网格包含当前帧及其跨视点邻居和跨时间邻居，共四帧。

**键值拼接**：将子网格内所有帧的图像特征令牌沿序列维度拼接为联合键值：

$$K_{\mathcal{S}_{v,t}} = [K_{f_{v,t}}, K_{f_{v+1,t}}, K_{f_{v,t+1}}, K_{f_{v+1,t+1}}], \quad V_{\mathcal{S}_{v,t}} = [V_{f_{v,t}}, V_{f_{v+1,t}}, V_{f_{v,t+1}}, V_{f_{v+1,t+1}}]$$

**注意力操作**：STGA 同时融合文本流和时空图像流，使用 RoPE 编码位置信息：

$$\operatorname{STGA}(\mathcal{S}_{v,t}) = \operatorname{softmax}\left([Q_{\mathrm{txt}}, \operatorname{RoPE}(Q_{f_{v,t}})] \cdot [K_{\mathrm{txt}}, \operatorname{RoPE}(K_{\mathcal{S}_{v,t}})]^{\top} / \sqrt{d_k}\right) \cdot [V_{\mathrm{txt}}, V_{\mathcal{S}_{v,t}}]$$

其中 $Q_{\mathrm{txt}}, K_{\mathrm{txt}}, V_{\mathrm{txt}}$ 为文本流的查询、键、值，$Q_{f_{v,t}}$ 为当前帧的图像查询。通过将子网格内四帧的键值拼接，每帧的查询可以同时关注自身、相邻视点和相邻时间步的特征，在局部范围内实现跨视图‑时间的信息融合。

**关键层范围约束**：实验分析表明（见 Figure 3 与 Table 5），将 STGA 限制在 MM‑DiT 的前约 30 层（层索引 0–29）可在一致性与编辑保真度之间取得最佳折衷。更深的层范围会导致纹理重复和编辑质量下降，而完全不施加 STGA 则产生不一致的多视角和时间编辑。

---

### 3.3 上下文令牌传播 (CTP)

STGA 仅实现局部子网格内的融合，CTP 则通过结构化的遍历路径将局部融合信息显式传播至整个网格，确保全局一致性。CTP 包含两个互补机制：

**全令牌继承**：在网格遍历过程中，当前子网格 $\mathcal{S}_{v,t}$ 与前一子网格 $\mathcal{S}_{\text{prev}}$ 的重叠区域（左侧两帧）直接继承已融合的令牌，避免重复计算并维持连续性。

**光流引导令牌替换**：对于非重叠区域（右侧两帧），利用光流将前一子网格的令牌变形至当前时间步：

$$\hat{\phi}_{\mathrm{r}}(S_{v,t}) = \mathrm{Warp}\left(\mathbf{F}_{t \rightarrow t-1}(x,y), \phi_{\mathrm{r}}(S_{v,t-1})\right)$$

其中 $\mathbf{F}_{t \rightarrow t-1}$ 为从 $t$ 到 $t-1$ 的光流场，$\phi_{\mathrm{r}}(S_{v,t-1})$ 为前一子网格右侧列的令牌。随后通过光流一致性掩码 $\mathrm{M}$ 进行选择性替换：

$$\phi_{\mathrm{r}}(S_{v,t}) = \mathrm{M} \odot \hat{\phi}_{\mathrm{r}}(S_{v,t}) + (1 - \mathrm{M}) \odot \phi_{\mathrm{r}}(S_{v,t})$$

光流有效区域的令牌由变形令牌替换，无效区域保留原始令牌，从而在传播一致性的同时避免错误传播带来的伪影。

---

### 3.4 直接 4DGS 优化

传统方法采用迭代式数据集更新 (IDU) 逐步优化 4D 表示，容易累积误差并导致结构漂移。Dynamic-eDiTor 将编辑后的所有帧直接用于一次性优化预训练的 4DGS：

$$\mathcal{G}_{\mathrm{edit}}' = \arg\min_{\mathcal{G}} \sum_{v,t \in V,T} \|\hat{f}_{v,t} - f_{v,t}^{\mathrm{edit}}\| + \mathcal{L}_{\mathrm{tv}}$$

其中 $\hat{f}_{v,t}$ 为编辑后 4DGS 的渲染帧，$f_{v,t}^{\mathrm{edit}}$ 为经 STGA 与 CTP 处理后的目标编辑帧，$\mathcal{L}_{\mathrm{tv}}$ 为全变分正则化损失。该目标函数直接在整个时空体积上优化高斯参数，无需迭代式数据集更新，从而保持整体结构稳定性。

---

### 3.5 变形高斯参数

为支持动态场景建模，4DGS 在规范高斯参数 $(x, r, s)$ 上叠加预测偏移量 $(\Delta x, \Delta r, \Delta s)$，得到变形后的动态高斯参数：

$$(x', r', s') = (x + \Delta x, r + \Delta r, s + \Delta s)$$

其中 $x$ 为位置，$r$ 为旋转，$s$ 为尺度。该变形机制使 4DGS 能够表达非刚性运动，为后续编辑提供可操作的动态表示基础。

### 补充图表

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/003_Figure_3.jpg]]
*Figure 3: Vital Layer Range Analysis. We analyze the impact of applying Spatio-Temporal Sub-Grid Attention (STGA) across different layer ranges in MM-DiT [11, 54] during the multiview video editing process. Performance is evaluated by temporal consistency (Warping Error [30]), multi-view consistency (MEt3R [2]), and editing fidelity (CLIP Text-Image Directional Similarity [42]). Applying STGA to the early ∼30 layers provides the best trade-off between consistency and editing fidelity*

## 实验与分析

### 实验设置

Dynamic-eDiTor 在 **DyNeRF** 多视图视频数据集上进行评估，涵盖多种非刚性动态场景。所有方法仅使用文本提示作为编辑输入，未使用额外视觉线索或人工标注。编辑流程在单张 **NVIDIA H100** GPU 上完成，完整 4D 场景编辑耗时约 **51 分钟**（以 “coffee martini” 场景为例）。

### 主实验结果

**Table 1** 从编辑保真度、用户偏好和重建保真度三个维度进行定量对比。在编辑保真度方面，Dynamic-eDiTor 取得了最高的 **CLIP_dir**（0.1849，较 Instruct-4DGS 提升 +0.0348）和 **CLIP_sim**（0.6397），表明编辑结果与文本提示的语义对齐度最优。用户研究中，本方法以 **48.95%** 的综合质量偏好率显著领先于 Instruct4D-to-4D（27.57%），优势达 +21.38 个百分点。

在重建保真度上，本方法在 **PSNR**（29.25）、**SSIM**（0.8064）和 **LPIPS**（0.1006）上略低于 CTRL-D（分别为 31.06、0.8498、0.0970）。这一差距反映了本方法的设计权衡：优先保证时空一致性而非逐像素精确重建，用户研究结果也印证了感知质量更优。

**Figure 4** 的定性对比进一步表明，Dynamic-eDiTor 在非刚性内容操控上更鲁棒，能够实现更完整的 4D 场景编辑，而基线方法常出现运动失真、几何漂移和编辑不完整。

### 消融实验

#### STGA 与 CTP 的贡献

**Table 2** 和 **Figure 5** 系统消融了 STGA 和 CTP 的作用。同时移除两个组件时，编辑结果出现严重伪影和几何漂移。单独添加 STGA 或 CTP 逐步改善结果，但仍残留运动模糊和几何漂移。完整方法（STGA + CTP）成功消除了上述伪影，确保了时空一致性。

**Figure 6** 从 2D 一致性角度进一步揭示：STGA 强化了语义对齐和视图一致性，保留了跨视角的细粒度细节；CTP 则增强了时间连贯性，使编辑内容在时间轴上平滑过渡。

#### CTP 内部机制消融

**Table 3** 在包含 STGA 的条件下消融 CTP 的子组件。全令牌继承（CTP-Full）和光流引导令牌替换（CTP-Flow）对增强时空一致性均至关重要：缺失任一部分都会导致全局一致性下降，尽管 CLIP 类指标可能出现微小波动，但时空连贯性的实质性退化是不可接受的。

#### 非对称子网格遍历

**Table 4** 和 **Figure 9** 消融了非对称子网格遍历（AGT）的作用。无 AGT 时，子网格间出现明显的不连续性，虽然局部一致性指标可能略优（因为各子网格独立优化），但全局多视角和时间一致性受到严重破坏。AGT 通过重叠子网格促进信息传播，是保持全局一致性的关键设计。

#### 关键层范围分析

**Figure 3** 和 **Table 5** 分析了在 MM-DiT 不同层范围内应用 STGA 的影响。将 STGA 限制在 **前 30 层（0–29）** 在一致性和编辑保真度之间取得最佳平衡。更深的层范围（如所有层）会导致纹理重复和编辑质量下降，而完全不应用 STGA 则产生不一致的多视角和时间编辑。**Figure 7** 的定性分析直观展示了这一趋势：全层应用引入跨视图和时间伪影，限制在前 30 层则有效避免了这些问题。

#### 局部与全局一致性

**Table 6** 和 **Table 7** 分别从局部和全局一致性角度量化各组件的贡献。完整方法在扭曲误差（Warping Error）和 MEt3R 指标上均达到最低，证明 STGA 和 CTP 共同作用，既保证了每个子网格内部的局部一致性，也确保了子网格间的全局一致性。

### 失败模式与局限性

1. **重建精度与一致性的权衡**：如 Table 1 所示，PSNR 和 SSIM 略低于 CTRL-D，这是优先保证时空一致性的必然代价。在需要严格逐像素重建的场景中，本方法可能不是最优选择。

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison. The evaluation spans three aspects: editing fidelity, user preference, and reconstruction fidelity. CLIP-based metrics [42] show that Dynamic-eDiTor achieves strong alignment with the editing prompts across 4D scenes, and user studies indicate a clear preference for our results over the baselines in terms of semantic alignment, perceptual realism, and coherent motion. Although reconstruction metrics (PSNR, SSIM [52], LPIPS [60]) are slightly lower, they remain competitive and do not detract from the method’s overall superiority in semantic accuracy and perceptual edit quality*

2. **编辑耗时**：完整流程约 51 分钟/场景，尚未达到实时或快速编辑需求，限制了交互式应用场景。

3. **几何编辑能力受限**：当前主要针对非刚性外观编辑和风格化任务，对于大幅几何变化的编辑（如对象形变）可能效果有限，需进一步验证。

4. **数据集泛化性**：实验主要在 DyNeRF 多视图视频数据集上进行，单目视频扩展仍处于初步阶段，在更多样化的动态场景上的泛化性有待检验。

### 补充图表

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparison. Dynamic-eDiTor enables more robust non-rigid content manipulation and achieves more complete edits of the 4D scene. The top-row displays the original rendered frames, while the following rows show the edited 4DGS renderings produced by each baseline. Our method (bottom-row) outperforms all baselines in both text alignment and overall editing fidelity, while maintaining strong temporal and spatial consistency*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Ablation Results. The model lacking both components (top-left) suffers from severe artifacts and geometric drift. Adding only STGA or only CTP progressively improves the result, but still leaves residual motion blur and geometric drift. Our full method (bottom-right) successfully ensuring the spatiotemporal consistency to produce a stable and complete edit*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/007_Table_2.jpg]]
*Table 2: Ablation Study. Each component, Spatio-Temporal Sub-Grid Attention (STGA) and Context Token Propagation (CTP), helps preserve temporal and multi-view consistency, improving the 4D reconstruction quality. Our method prioritizes a globally stable 4D structure, yielding consistent temporal and spatial behavior and thus more robust reconstruction fidelity. Although CLIP-based metrics [42] show a slight drop due to the trade-off between semantic alignment and spatio-temporal coherence, our method still produces more stable and reliable 4D edits, avoiding the geometric and temporal artifacts seen in the ablated variants*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/008_Table_3.jpg]]
*Table 3: Ablation Study: Context Token Propagation (CTP). This ablation study is conducted with STGA included to isolate the impact of CTP. Full Token Inheritance (CTP-Full) and Flow-Guided Token Replacement (CTP-Flow) play a critical role in reinforcing temporal and multi-view consistency, enabling more accurate reconstruction of the edited dynamic scene. Despite a slight trade-off in CLIP-based metrics [42], CTP substantially improves spatio-temporal coherence and overall 4D editing fidelity*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/010_Figure_6.jpg]]
*Figure 6: Ablation Study: 2D Consistency. Each component in our method strengthens temporal and multi-view consistency in 2D editing. STGA improves semantic alignment and preserves fine details across views, while CTP enhances coherence by propagating information across neighboring frames*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative Analysis of Vital Layer Range. Applying STGA to all layers introduces visual artifacts across views and time, while omitting STGA produces inconsistent multi-view and temporal edits. Restricting STGA to the vital range yields the most coherent and stable multi-view–time editing results*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/014_Table_5.jpg]]
*Table 5: Detailed vital layer range analysis for STGA. This table reports the exact numerical values corresponding to the trend shown in Figure 3 of the main paper*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/012_Table_4.jpg]]
*Table 4: Ablation Study: Asymmetric Sub-Grid Traversal (AGT). This evaluation is conducted without CTP to isolate the impact of Asymmetric Sub-Grid Traversal (AGT). The results show that sub-grids without AGT achieve slightly better local consistency metrics because all frames within each sub-grid are updated independently. However, the lack of linkage between sub-grids introduces discontinuities, weakening overall 4D reconstruction fidelity. In contrast, applying AGT improves global consistency by overlapping frames across sub-grids, even at the cost of some local editing precision, as it enables effective information propagation. This leads to more stable and reliable 4D edits, demonstrating that...*

![[assets/figures/papers/paper_list_l2471_https_arxiv_org_abs_2512_00677/figures/013_Figure_9.jpg]]
*Figure 9: Ablation Study: Asymmetric Sub-Grid Traversal (AGT). This qualitative result clearly demonstrates that AGT preserves global multi-view and temporal consistency. Without AGT, noticeable discontinuities appear between sub-grids*

## 方法谱系与知识库定位

### 与现有方法的谱系关系

Dynamic-eDiTor 处于**训练免费文本驱动4D场景编辑**这一新兴方向，其核心贡献在于首次将多模态扩散Transformer（MM-DiT）引入4D编辑管线，并通过统一的相机-时间网格上的时空一致性机制解决了此前方法的两大根本性瓶颈：多视角不一致和时间不连贯。

**与基于U-Net的2D扩散编辑方法的区别。** 现有4D编辑方法（如 **Instruct4D-to-4D**、**Instruct-4DGS**、**CTRL-D**）普遍依赖基于U-Net架构的2D扩散模型对多视角视频进行逐帧独立编辑，随后通过迭代式数据集更新（Iterative Dataset Update, IDU）将编辑结果蒸馏回4D表示。这类管线存在结构性缺陷：逐帧编辑缺乏跨视角和时间维度的联合约束，导致编辑后的帧序列出现几何漂移、运动模糊和编辑不完整等问题。Dynamic-eDiTor 的根本性改进在于用 MM-DiT 替代 U-Net 作为编辑主干，并在此基础上构建了**时空子网格注意力（STGA）**和**上下文令牌传播（CTP）**两个协同模块，在编辑过程中直接强制执行多视角和时间一致性，从而从根源上消除了逐帧独立编辑带来的不一致性。

**与迭代式数据集更新（IDU）策略的决裂。** 此前的4D编辑方法通常采用 IDU 策略，即交替进行“编辑-重建-再编辑”的循环优化过程。Dynamic-eDiTor 则完全摒弃了这一策略，转而采用**一次性直接优化**：编辑后的多视角视频帧直接用于优化预训练的4D高斯溅射（4DGS）模型，无需迭代循环。这一设计选择不仅简化了管线，更重要的是避免了IDU过程中可能引入的误差累积和结构退化，使得编辑后的4D表示能够更好地保持原始场景的全局结构稳定性。

**在扩散模型谱系中的定位。** Dynamic-eDiTor 的编辑主干建立在 **FLUX**（Black Forest Labs, 2024）等 MM-DiT 架构之上，利用了 MM-DiT 的双流自注意力机制和强大的文本-图像对齐能力。与基于 U-Net 的扩散模型相比，MM-DiT 的 Transformer 架构天然更适合处理多帧联合注意力操作，这使得 STGA 能够通过简单的键值拼接（key-value concatenation）实现局部时空融合，而无需对模型架构进行侵入式修改。该方法通过 **diffusers** 库（von Platen et al., 2022）实现，保持了与主流扩散模型生态的兼容性。

### 适用边界与能力范围

**强项场景。** Dynamic-eDiTor 在以下场景中展现出显著优势：
- **非刚性外观编辑**：如改变物体材质、颜色、纹理风格等，STGA 和 CTP 能够有效保持编辑在多视角和时间维度上的一致性。
- **风格化编辑**：将整个4D场景转换为特定艺术风格，全局一致性机制确保了风格在空间和时间上的连贯传播。
- **局部语义编辑**：如替换场景中的特定对象类别，CTP 的令牌继承机制能够在编辑区域和非编辑区域之间保持平滑过渡。

**能力边界。** 根据论文中报告的结果和局限性分析，该方法存在以下适用边界：
- **大幅几何变换受限**：当前方法主要针对外观和风格编辑，对于涉及显著几何形变（如对象大幅度扭曲、拓扑变化）的编辑任务可能力不从心。这是因为编辑过程在2D图像空间中进行，缺乏对3D几何的直接操控能力。
- **场景规模约束**：实验主要在 DyNeRF 数据集上进行，该数据集包含有限数量的多视角视频场景。在更大规模动态场景（更多视点、更长序列）上的稳定性和效率尚未得到充分验证。
- **单目视频泛化有限**：论文仅在附录中初步验证了单目视频设置的扩展，该方法对单目输入的支持仍处于早期阶段，泛化性有待进一步检验。

### 关键局限与设计权衡

**重建精度与时空一致性的权衡。** 定量实验（Table 1）揭示了一个重要的设计权衡：Dynamic-eDiTor 在 PSNR（29.25 vs. 31.06）、SSIM（0.8064 vs. 0.8498）和 LPIPS（0.1006 vs. 0.0970）等重建精度指标上略低于 **CTRL-D**。这并非方法缺陷，而是有意为之的设计选择——该方法优先保证全局时空一致性，而非逐像素的精确重建。用户研究结果（Overall Quality 偏好率 48.95% vs. 27.57% 对比 Instruct4D-to-4D）证实了这一权衡在感知质量层面的合理性：人类观察者更倾向于时空连贯的编辑结果，即使其像素级重建精度略低。

**计算效率瓶颈。** 完整的4D编辑流程耗时约51分钟/场景（在单个 NVIDIA H100 GPU 上测试“coffee martini”场景），远未达到实时或快速编辑需求。这一耗时主要源于：MM-DiT 的多帧联合推理、STGA 在多个层上的注意力计算、以及 CTP 的结构化遍历传播过程。对于需要快速迭代的交互式编辑场景，当前效率仍是一大障碍。

**层范围敏感性。** STGA 的层范围选择对编辑质量有显著影响。消融实验（Figure 3, Table 5）表明，将 STGA 限制在 MM-DiT 的前30层（0-29）能够在一致性和编辑保真度之间取得最佳平衡。若将 STGA 应用到所有层，会导致纹理重复和编辑质量下降；若完全不应用 STGA，则会产生多视角和时间不一致的编辑结果。这种对层范围的敏感性意味着该方法需要针对不同场景和编辑任务进行一定程度的超参数调优。

### 开放问题与未来方向

基于论文中明确提出的局限性以及方法设计所隐含的扩展空间，以下几个开放问题值得关注：

1. **几何编辑能力的扩展。** 当前方法在2D图像空间中进行编辑，缺乏对3D几何的直接操控。是否可以将 STGA 和 CTP 的时空一致性机制与3D感知的编辑方法（如基于神经辐射场的几何编辑）相结合，从而支持更剧烈的运动编辑和几何变换？

2. **与其它4D表示的兼容性。** Dynamic-eDiTor 目前专门针对4D高斯溅射（4DGS）设计，但其核心的时空一致性编辑机制（STGA + CTP）本质上是表示无关的。该框架是否可与其它4D表示（如 Dynamic NeRF、K-Planes 等）结合，形成更通用的4D编辑框架？这需要解决不同表示在渲染、优化和梯度回传方面的接口差异。

3. **大规模动态场景的扩展。** 在更多视点、更长序列的大规模动态场景中，相机-时间网格的规模将急剧增长，STGA 的子网格遍历和 CTP 的全局传播将面临计算效率和内存消耗的双重挑战。如何设计更高效的稀疏注意力机制或分层传播策略，以保持线性或亚线性的计算复杂度？

4. **编辑粒度与时效性的提升。** 当前方法以整个场景为单位进行编辑，缺乏对局部区域或特定时间段的精细控制。同时，51分钟的处理时间限制了交互式应用。如何在保持一致性的前提下，支持更细粒度的编辑控制（如空间掩码、时间窗口）并显著降低延迟？这可能需要在 MM-DiT 的推理效率和4DGS的优化策略上进行联合改进。

5. **评估体系的完善。** 当前评估主要依赖 CLIP-based 指标和用户研究，缺乏专门针对4D编辑一致性的自动化度量标准。论文中使用的 Warping Error 和 MEt3R 指标（Table 6）是向正确方向迈出的一步，但4D编辑领域仍然急需更全面、更细粒度的自动化评估基准，以系统性地衡量多视角一致性、时间连贯性和编辑保真度之间的复杂权衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dynamic_eDiTor_Training_Free_Text_Driven_4D_Scene_Editing_with_Multimodal_Diffusion_Transformer.pdf]]

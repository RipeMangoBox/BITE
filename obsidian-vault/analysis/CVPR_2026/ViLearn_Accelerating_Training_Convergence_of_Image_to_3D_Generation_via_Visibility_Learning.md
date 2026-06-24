---
title: "ViLearn: Accelerating Training Convergence of Image-to-3D Generation via Visibility Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ViLearn_Accelerating_Training_Convergence_of_Image_to_3D_Generation_via_Visibility_Learning.pdf
project_link: null
code_link: null
aliases:
- ViLearn
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将可见性结构和位置归纳偏置显式注入图像到3D的pipeline，通过将形状token划分为可见/不可见子集并赋予可见性感知的位置编码。
primary_logic: 通过明确告知扩散模型哪些形状token对应可见几何、哪些对应遮挡区域，能够将可见重建与不可见幻觉解耦，从而缩小假设空间并提供清晰的几何结构引导，加速收敛。
claims:
- ViLearn achieves up to 4.4× faster training convergence compared to vanilla VecSet-based training.
- ViLearn attains best final-step metrics (IS-AS 0.702, Floater 31.5) among comparable SOTA models.
- "Visibility Grouping effectively separates visible and invisible geometry: visible tokens reconstruct visible surfaces, invisible tokens capture occluded regions."
- Hi3DEval + AI-generated test set (1,100 images) 上 IS-AS (Image-Shape Alignment Score) = 0.702
---

# ViLearn: Accelerating Training Convergence of Image-to-3D Generation via Visibility Learning

> [!tip] 核心洞察
> 通过明确告知扩散模型哪些形状token对应可见几何、哪些对应遮挡区域，能够将可见重建与不可见幻觉解耦，从而缩小假设空间并提供清晰的几何结构引导，加速收敛。

| 字段 | 内容 |
|------|------|
| 中文题名 | ViLearn：通过可见性学习加速图像到三维生成训练收敛 |
| 英文题名 | ViLearn: Accelerating Training Convergence of Image-to-3D Generation via Visibility Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_ViLearn_Accelerating_Training_Convergence_of_Image-to-3D_Generation_via_Visibility_Learning_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ViLearn |
| Dataset | Hi3DEval + AI-generated test set |

> [!tip] 效果简介
> - Hi3DEval + AI-generated test set (1,100 images) 上，IS-AS (Image-Shape Alignment Score) 0.702 vs 0.656 (+0.046 (7% relative gain))；Floater (lower is better) 31.5 vs 74.8 (-43.3 (57.8% reduction))；GP 5.988 vs 5.826 (+0.162)。

## 概述

**问题瓶颈**：当前主流的VecSet-based 3D生成方法将形状token视为无序集合，不施加任何位置编码。这迫使扩散模型在一个庞大的置换不变token空间中同时学习可见对应关系与幻觉不可见几何，导致训练效率低下、收敛不稳定。

**核心洞察**：将可见性结构与位置归纳偏置显式注入图像到3D的生成pipeline，通过告知模型哪些token对应可见几何、哪些对应遮挡区域，可以将可见重建与不可见幻觉解耦，缩小假设空间并提供清晰的几何结构引导。

**方法定位**：ViLearn（Visibility Learning）在标准VecSet + MM-DiT框架内引入两个协同组件——**Visibility Grouping (VG)** 与**Visibility-Aware Positional Encoding (VAPE)**。VG在数据准备阶段利用可见表面点与形状token的交叉注意力分数，将token划分为可见子集（VST）和不可见子集（IST）；VAPE则将这一可见性信息注入MM-DiT的注意力机制，为图像token与可见形状token赋予共享的位置编码以强化跨模态交互，同时为不可见token赋予独立编码以维护其幻觉能力。

**方法谱系**：ViLearn属于VecSet-based单图到3D生成路线，其基线为vanilla VecSet训练（无可见性学习）。对比的SOTA模型包括**Hunyuan3D 2.0**（Tencent Hunyuan3D Team, 2025, 1.1B）、**TripoSG**（Li et al., 2025, 1.3B）和**Step1X-3D**（1.3B）。ViLearn通过收敛加速，仅使用32块GPU即达到最佳对齐效果，而上述SOTA模型通常在数百块GPU上训练数周。

**主要结果**：
- **收敛加速**：VA-RoPE变体在仅25K迭代步即达到vanilla基线110K步的性能，加速比最高达**4.4×**。
- **最终指标**（110K步，Hi3DEval + AI生成测试集1,100张图像）：ViLearn在全部四项指标上取得最优——IS-AS **0.702**（基线0.656）、Floater **31.5**（基线74.8，降低57.8%）、GP **5.988**、GD **2.688**，均优于同参数量级的SOTA模型。
- **消融验证**：可见性分组有效分离可见/不可见几何，且可见性感知编码（VA-RoPE/VA-LPE）显著优于vanilla RoPE，证实了显式注入可见性结构的关键作用。

## 背景与动机

### 从单图到三维生成：VecSet范式的兴起

单图到三维生成旨在从单张二维图像重建完整的三维几何形状，是计算机视觉与图形学领域的核心挑战之一。近年来，基于**VecSet（向量集合）表示**的三维生成方法取得了显著进展。这类方法首先通过一个预训练的三维VAE将三维形状压缩为一组无序的一维形状token，随后利用**多模态扩散Transformer（MM-DiT）** 以图像token为条件对形状token进行去噪生成，最终通过VecSet解码器将形状token恢复为三维网格。

MM-DiT的输入由两类token组成：来自VecSet tokenizer的形状token（表征三维几何），以及来自视觉编码器（如DINOv2）的图像token。在双流注意力块中，形状token和图像token的查询、键、值矩阵被拼接后执行双向交叉注意力：

$$
\left\{ \begin{array}{ll} Q = \mathrm{Concat}[Q_{\mathrm{shape}}, Q_{\mathrm{image}}] \\ K = \mathrm{Concat}[K_{\mathrm{shape}}, K_{\mathrm{image}}] \\ V = \mathrm{Concat}[V_{\mathrm{shape}}, V_{\mathrm{image}}] \end{array} \right.
$$

该机制使得模型能够捕捉图像条件与三维几何之间的跨模态对应关系。**Hunyuan3D 2.0**（Tencent Hunyuan3D Team, 2025）、**TripoSG**（Li et al., 2025）和**Step1X-3D**等SOTA模型均采用这一范式，参数规模达到1.1B至1.3B，并在大规模GPU集群上训练数周以取得高质量生成结果。

### 核心瓶颈：置换不变性下的可见性学习困境

尽管VecSet范式取得了可观进展，但其设计中存在一个根本性的结构缺陷：**形状token被视为无序集合，且未引入任何显式的位置编码**。这一设计选择虽然保证了token序列的置换不变性，却给扩散模型的训练带来了严峻挑战。

具体而言，单张输入图像仅能提供三维物体在特定视角下的**可见表面信息**，而模型需要同时完成两项截然不同的子任务：（1）根据图像重建可见几何；（2）基于先验知识幻觉不可见的遮挡区域。在缺乏显式可见性结构引导的情况下，扩散模型被迫在庞大的置换不变token空间中**同时学习可见对应关系和不可见几何的推断**。这种可见重建与不可见幻觉的耦合使得假设空间急剧膨胀，严重阻碍了训练效率和收敛稳定性。

### 现有方法的局限与本文动机

现有VecSet方法普遍忽略了可见性结构这一关键的几何先验。模型在训练过程中无法区分哪些形状token对应于输入图像中实际可见的表面，哪些对应于被遮挡的不可见区域。这导致两个层面的效率损失：其一，图像token与形状token之间的跨模态注意力缺乏聚焦，难以高效建立可见对应关系；其二，模型对不可见几何的推断缺乏来自可见几何的结构化约束。

**ViLearn的动机**正是针对上述瓶颈，将可见性结构和位置归纳偏置显式注入图像到三维生成的pipeline。其核心洞察在于：通过明确告知扩散模型哪些形状token对应可见几何、哪些对应遮挡区域，能够将可见重建与不可见幻觉解耦，从而缩小假设空间并提供清晰的几何结构引导，最终实现训练收敛的显著加速。

## 核心创新

### 问题根源：VecSet表示中的可见性盲区

当前主流的VecSet-based 3D生成方法（如Hunyuan3D 2.0、TripoSG、Step1X-3D）将3D形状压缩为一组无序的1D token，并在多模态扩散Transformer（MM-DiT）中与图像token进行交叉注意力交互。然而，这种设计存在一个根本性瓶颈：**形状token被建模为置换不变的集合，缺乏任何位置编码或几何结构信息**。扩散模型被迫在一个庞大的无序token空间中同时学习两个任务——从图像token推断哪些形状token对应可见表面，以及幻觉出被遮挡的不可见几何。这两个任务的耦合极大地膨胀了假设空间，导致训练收敛缓慢且不稳定。

### 核心洞察：将可见性结构显式注入扩散过程

ViLearn的核心创新在于**将可见性作为一种结构归纳偏置显式注入图像到3D的生成pipeline**。其关键思想是：通过明确告知扩散模型哪些形状token对应可见几何、哪些对应遮挡区域，将可见重建与不可见幻觉解耦，从而缩小假设空间并提供清晰的几何结构引导。这一洞察催生了两个协同组件。

### 创新组件一：可见性分组（Visibility Grouping, VG）

VG在数据准备阶段将无序的形状token集合划分为**可见形状token（VST）**和**不可见形状token（IST）**两个子集。具体而言，VG利用从3D几何表面在条件图像视角下渲染的可见点图（visible points map）作为查询，通过与预训练VecSet解码器的交叉注意力机制计算每个可见点与各形状token的注意力分数：

$$\mathbf{A} = (\mathbf{W}_q \mathbf{P}_{\mathrm{vis}}) (\mathbf{W}_k \mathbf{S})^T$$

对每个可见点，选择注意力分数最高的形状token索引：

$$a_i = \operatorname{argmax}_{j \in \{1, \dots, N\}} \mathbf{A}_{i,j}$$

所有被选中的token构成VST，其余归为IST。实验证明，**分别解码这两个子集可产生互补的几何信息**：VST重建可见表面，IST编码被遮挡区域（见Figure 2）。这种划分从根本上改变了模型需要学习的内容——不再需要从无序集合中隐式推断可见性对应关系。

### 创新组件二：可见性感知位置编码（Visibility-Aware Positional Encoding, VAPE）

VAPE将VG产生的可见性结构注入MM-DiT的注意力机制。其设计原则是：**为图像token和可见形状token分配共享的位置编码，以显式强化它们的跨模态交互；为不可见token分配独立的位置编码，使其形成独立的表征子空间**。具体实现提供了两种变体：

- **VA-RoPE**：使用两个可学习的旋转矩阵 $R_m$（可见类）和 $R_n$（不可见类）对查询和键施加旋转位置编码。图像token和VST共享 $R_m$，IST使用 $R_n$，从而强化类内交互、削弱跨类交互：

$$\begin{cases}
\hat{Q}_{\mathrm{IT}} = Q_{\mathrm{IT}} R_m, \quad \hat{K}_{\mathrm{IT}} = K_{\mathrm{IT}} R_m \\
\hat{Q}_{\mathrm{shape}} = \mathrm{Concat}[Q_{\mathrm{VST}} R_m, Q_{\mathrm{IST}} R_n] \\
\hat{K}_{\mathrm{shape}} = \mathrm{Concat}[K_{\mathrm{VST}} R_m, K_{\mathrm{IST}} R_n]
\end{cases}$$

- **VA-LPE**：使用两个可学习的加性嵌入 $e_v$（可见）和 $e_i$（不可见）直接注入可见性信息：

$$\begin{cases}
\hat{Q}_{\mathrm{IT}} = Q_{\mathrm{IT}} + e_v, \quad \hat{K}_{\mathrm{IT}} = K_{\mathrm{IT}} + e_v \\
\hat{Q}_{\mathrm{shape}} = \operatorname{Concat}[Q_{\mathrm{VST}} + e_v, Q_{\mathrm{IST}} + e_i] \\
\hat{K}_{\mathrm{shape}} = \operatorname{Concat}[K_{\mathrm{VST}} + e_v, K_{\mathrm{IST}} + e_i]
\end{cases}$$

### 创新本质：从“隐式学习可见性”到“显式注入可见性”

相较于vanilla VecSet训练（无位置编码、无可见性分组），ViLearn的根本改变在于将**可见性对应关系从模型需要隐式学习的隐藏变量转变为显式的结构先验**。这一转变通过两个changed slots实现：

| 设计维度 | Vanilla VecSet训练 | ViLearn |
|---------|-------------------|---------|
| 可见性结构 | 无；形状token为无序集合 | VG将token划分为VST和IST子集 |
| 位置编码策略 | 无（置换不变） | VAPE根据可见性状态分配差异化编码 |

消融实验验证了这一设计的有效性：**VA-RoPE仅需25K步即可达到vanilla baseline 110K步的性能，收敛加速约4.4倍**，且最终指标全面超越（IS-AS从0.656提升至0.702，Floater从74.8降至31.5，降幅57.8%）。值得注意的是，即使加入VG但使用vanilla RoPE（无可见性感知）的变体性能显著低于VA-RoPE，证实了**可见性自适应编码是不可或缺的关键设计**。

## 整体框架

ViLearn 的整体 pipeline 围绕一个核心设计展开：**将可见性结构显式注入 VecSet 图像到三维生成的扩散训练流程**。如图 4 所示，框架由四个主要阶段构成：数据准备、可见性分组（Visibility Grouping, VG）、可见性感知位置编码（Visibility-Aware Positional Encoding, VAPE）以及 MM-DiT 扩散训练。

### 数据准备阶段

训练前，系统准备三类输入 token：

- **形状 token**：由预训练的 VecSet VAE（三维 tokenizer）将三维网格压缩为一组无序的一维 token 集合 $\mathbf{S} \in \mathbb{R}^{N \times d}$。该集合本身不具备位置编码，是置换不变的。
- **图像 token**：由视觉编码器（如 DINOv2）从条件图像中提取。
- **可见表面点**：从三维几何表面以条件图像的视点渲染得到可见点图 $\mathbf{P}_{\text{vis}}$，作为后续可见性分组的查询依据。

### 可见性分组（VG）

VG 模块在数据准备阶段执行，目标是将无序的形状 token 集合划分为**可见形状 token（VST）**和**不可见形状 token（IST）**两个子集。具体流程如下：

1. 利用预训练 VecSet 解码器中的交叉注意力投影层 $\mathbf{W}_q, \mathbf{W}_k$，计算可见表面点（查询）与形状 token（键）之间的注意力分数矩阵：

   $$\mathbf{A} = (\mathbf{W}_q \mathbf{P}_{\text{vis}}) (\mathbf{W}_k \mathbf{S})^T$$

2. 对每个可见点 $i$，选取注意力分数最高的形状 token 索引：

   $$a_i = \operatorname{argmax}_{j \in \{1, \dots, N\}} \mathbf{A}_{i,j}$$

3. 被选中的 token 构成 VST 集合，其余 token 归入 IST 集合。

这种划分将可见几何与遮挡区域的 token 解耦，为后续 VAPE 提供结构基础。如图 2 所示，单独解码 VST 和 IST 可得到互补的几何信息：VST 重建可见表面，IST 编码被遮挡区域。

### 可见性感知位置编码（VAPE）

VAPE 在 MM-DiT 的注意力计算中注入可见性信息。其核心操作是将形状 token 的查询和键矩阵按可见性划分：

$$\begin{cases} Q_{\text{shape}} = \text{Concat}[Q_{\text{VST}}, Q_{\text{IST}}] \\ K_{\text{shape}} = \text{Concat}[K_{\text{VST}}, K_{\text{IST}}] \end{cases}$$

随后对划分后的查询和键施加可见性感知编码。ViLearn 提供两种设计选择（图 5）：

- **VA-RoPE**：使用两个预定义的旋转矩阵 $R_m$（可见类）和 $R_n$（不可见类）对查询和键进行旋转编码。图像 token 和 VST 共享 $R_m$，IST 使用 $R_n$，从而强化类内交互、削弱跨类交互：

  $$\begin{cases} \hat{Q}_{\text{IT}} = Q_{\text{IT}} R_m, \quad \hat{K}_{\text{IT}} = K_{\text{IT}} R_m \\ \hat{Q}_{\text{shape}} = \text{Concat}[Q_{\text{VST}} R_m, Q_{\text{IST}} R_n] \\ \hat{K}_{\text{shape}} = \text{Concat}[K_{\text{VST}} R_m, K_{\text{IST}} R_n] \end{cases}$$

- **VA-LPE**：使用两个可学习的加性嵌入 $e_v$（可见）和 $e_i$（不可见）对查询和键进行编码：

  $$\begin{cases} \hat{Q}_{\text{IT}} = Q_{\text{IT}} + e_v, \quad \hat{K}_{\text{IT}} = K_{\text{IT}} + e_v \\ \hat{Q}_{\text{shape}} = \text{Concat}[Q_{\text{VST}} + e_v, Q_{\text{IST}} + e_i] \\ \hat{K}_{\text{shape}} = \text{Concat}[K_{\text{VST}} + e_v, K_{\text{IST}} + e_i] \end{cases}$$

### MM-DiT 扩散训练

编码后的 token 进入 MM-DiT 骨干网络进行条件扩散去噪。MM-DiT 包含双流注意力块和单流注意力块，其核心缩放点积注意力为：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

在双流块中，形状 token 和图像 token 的投影被拼接以形成双向交叉注意力：

$$\begin{cases} Q = \text{Concat}[Q_{\text{shape}}, Q_{\text{image}}] \\ K = \text{Concat}[K_{\text{shape}}, K_{\text{image}}] \\ V = \text{Concat}[V_{\text{shape}}, V_{\text{image}}] \end{cases}$$

通过 VAPE 编码后的查询和键，图像 token 与 VST 共享相同的可见性编码（$R_m$ 或 $e_v$），显式强化了它们之间的跨模态交互，使模型能够高效学习可见对应关系；而 IST 使用独立的编码（$R_n$ 或 $e_i$），引导模型以不同机制处理遮挡区域的幻觉生成。

### 数据流总结

整个 pipeline 的数据流为：三维网格 → VecSet VAE → 无序形状 token → VG 划分 VST/IST → VAPE 可见性编码 → MM-DiT 条件扩散去噪 → VecSet 解码器 → 三维网格。可见性信息从数据准备阶段注入，贯穿注意力计算全过程，将原本庞大的置换不变假设空间压缩为可见/不可见双通道结构，这是 ViLearn 实现最高 4.4 倍训练加速的因果机制。

### 补充图表

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/004_Figure_4.jpg]]
*Figure 4: Overview of ViLearn. (a) We prepare shape tokens, image tokens, and visible points. (b) Visibility Grouping (VG). Using cross-attention scores between visible points and shape tokens, we partition shape tokens into visible (VST) and invisible (IST) sets. (c) Visibility-Aware Positional Encoding (VAPE). We apply VAPE to VST, IST, and image tokens (IT) during MM-DiT [10] training, enabling the model to distinguish visibility states. Two VAPE designs are explored in Fig. 5 and Sec. 4.2*

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/001_Figure.jpg]]
*Figure: (b) Our 3D LDM Training (Visibility Learning)*

## 核心模块与公式推导

### 问题背景：VecSet表示中的可见性瓶颈

现有VecSet-based 3D生成方法将形状token视为**无序集合**，且不施加任何位置编码。在MM-DiT（Multimodal Diffusion Transformer）框架下，形状token与图像token通过双流注意力块进行交叉模态交互，其核心操作为缩放点积注意力：

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

在双流块中，形状token和图像token的投影被拼接为统一的查询、键、值矩阵：

$$\left\{ \begin{array}{ll} Q = \mathrm{Concat}[Q_{\mathrm{shape}}, Q_{\mathrm{image}}] \\ K = \mathrm{Concat}[K_{\mathrm{shape}}, K_{\mathrm{image}}] \\ V = \mathrm{Concat}[V_{\mathrm{shape}}, V_{\mathrm{image}}] \end{array} \right.$$

这种置换不变的无序集合表示迫使扩散模型在庞大的token空间中**同时学习可见对应关系与幻觉不可见几何**，严重阻碍训练效率和收敛稳定性。ViLearn的核心思路是将**可见性结构和位置归纳偏置显式注入**图像到3D的pipeline，通过将形状token划分为可见/不可见子集并赋予可见性感知的位置编码，将可见重建与不可见幻觉解耦。

### 模块一：Visibility Grouping（VG）

VG的目标是在数据准备阶段将无序的形状token集合划分为**可见子集（VST）**和**不可见子集（IST）**。其关键洞察是：利用预训练VecSet解码器中的交叉注意力机制，以条件图像的视点下渲染的可见表面点作为查询，识别与之最相关的形状token。

具体流程如下：

**步骤1：获取可见表面点。** 从几何表面以扩散模型条件图像的视点渲染可见点图（visible points map），得到可见表面点集合 $\mathbf{P}_{\mathrm{vis}}$。

**步骤2：计算交叉注意力分数。** 使用预训练VecSet解码器的投影层，计算可见表面点（作为查询）与形状token（作为键）之间的交叉注意力分数：

$$\mathbf{A} = (\mathbf{W}_q \mathbf{P}_{\mathrm{vis}}) (\mathbf{W}_k \mathbf{S})^T$$

其中 $\mathbf{W}_q$、$\mathbf{W}_k$ 为预训练投影矩阵，$\mathbf{S}$ 为形状token集合。

**步骤3：逐点选择最高分token。** 对每个可见点 $i$，选择注意力分数最高的形状token索引：

$$a_i = \operatorname{argmax}_{j \in \{1, \dots, N\}} \mathbf{A}_{i,j}$$

所有被选中的形状token构成可见子集VST，其余token归入不可见子集IST。实验表明，分别解码这两个子集可产生互补的几何信息：**可见token重建可见表面，不可见token编码遮挡区域**（见图2）。

### 模块二：Visibility-Aware Positional Encoding（VAPE）

VAPE将VG产生的可见性结构注入MM-DiT的注意力机制。核心操作是**按可见性划分形状token的查询和键矩阵**：

$$\begin{cases} Q_{\mathrm{shape}} = \mathrm{Concat}[Q_{\mathrm{VST}}, Q_{\mathrm{IST}}] \\ K_{\mathrm{shape}} = \mathrm{Concat}[K_{\mathrm{VST}}, K_{\mathrm{IST}}] \end{cases}$$

随后对划分后的查询和键施加可见性感知的编码。论文探索了两种实现方案：

#### VA-RoPE（旋转位置编码变体）

VA-RoPE使用两个不同的旋转矩阵 $R_m$（可见类）和 $R_n$（不可见类）对查询和键施加旋转位置编码。图像token与可见形状token共享 $R_m$，强化其跨模态交互；不可见形状token使用独立的 $R_n$，削弱与可见类的交互：

$$\left\{ \begin{array}{c} \hat{Q}_{\mathrm{IT}} = Q_{\mathrm{IT}} R_m, \quad \hat{K}_{\mathrm{IT}} = K_{\mathrm{IT}} R_m \\ \hat{Q}_{\mathrm{shape}} = \mathrm{Concat}[Q_{\mathrm{VST}} R_m, Q_{\mathrm{IST}} R_n] \\ \hat{K}_{\mathrm{shape}} = \mathrm{Concat}[K_{\mathrm{VST}} R_m, K_{\mathrm{IST}} R_n] \end{array} \right.$$

#### VA-LPE（可学习加性位置编码变体）

VA-LPE使用两个可学习的加性嵌入 $e_v$（可见）和 $e_i$（不可见），直接加到对应token的查询和键上：

$$\left\{ \begin{array}{ll} \hat{Q}_{\mathrm{IT}} = Q_{\mathrm{IT}} + e_v, \quad \hat{K}_{\mathrm{IT}} = K_{\mathrm{IT}} + e_v \\ \hat{Q}_{\mathrm{shape}} = \operatorname{Concat}[Q_{\mathrm{VST}} + e_v, Q_{\mathrm{IST}} + e_i] \\ \hat{K}_{\mathrm{shape}} = \operatorname{Concat}[K_{\mathrm{VST}} + e_v, K_{\mathrm{IST}} + e_i] \end{array} \right.$$

### 两种VAPE变体的机制差异

VA-RoPE通过旋转矩阵改变查询-键点积的几何关系：同类token（可见-可见或不可见-不可见）的点积保持不变，而跨类token的点积被旋转角度 $m-n$ 调制，从而**显式控制类间交互强度**。VA-LPE则通过加性偏置直接偏移token表示，使模型学习可见性相关的表示偏移。消融实验表明，VA-RoPE在收敛速度和最终性能上均优于VA-LPE，且显著优于仅使用VG但无可见性感知编码的"Vanilla RoPE"变体，证实了**可见性自适应编码的必要性**。

### 补充图表

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/005_Figure_5.jpg]]
*Figure 5: Two design choices of VAPE. (a) VA-RoPE multiply two pre-defined rotary matrices, i.e*

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/002_Figure_2.jpg]]
*Figure 2: Complementary information of visible and invisible shape tokens. Full tokens are partitioned into visible and invisible subsets via frontal visible points [51] in this case. The decoded meshes and their geometric normal maps show visible tokens reconstruct visible surfaces while invisible tokens capture occluded surfaces, demonstrating complementary geometric information*

## 实验与分析

### 主实验结果

为全面评估ViLearn的生成质量与训练效率，我们在Hi3DEval基准与1,100张AI生成图像的联合测试集上，将ViLearn与vanilla VecSet训练基线及三款参数量可比的SOTA VecSet模型——**Hunyuan3D 2.0**（Tencent Hunyuan3D Team，2025，1.1B）、**TripoSG**（Li et al.，2025，1.3B）和**Step1X-3D**（1.3B）——进行对比。所有模型均训练至110K步，结果汇总于Table 1。

ViLearn在所有四项指标上均取得最优结果。具体而言，其图像-形状对齐分数（IS-AS）达到**0.702**，较vanilla基线的0.656提升7%（+0.046），表明生成形状与输入图像的条件一致性显著增强。在衡量漂浮几何伪影的Floater指标上，ViLearn录得**31.5**，相比基线的74.8大幅降低57.8%（−43.3），说明可见性学习有效抑制了不可见区域的几何幻觉。几何精度（GP）和几何完整性（GD）也分别从5.826/2.623提升至**5.988**和**2.688**，印证了整体重建质量的改善。

值得强调的是，上述SOTA模型通常在数百块GPU上训练数周，而ViLearn仅使用**32块GPU**即达到最佳对齐效果，这直接归因于可见性学习带来的训练效率跃升。

### 收敛速度分析

ViLearn的核心优势在于训练收敛的显著加速。Figure 1(c)和Figure 7展示了不同模型在各训练步数的指标曲线。以Floater和IS-AS为追踪指标，**VA-RoPE变体在仅25K步时即达到vanilla基线110K步的性能水平，收敛加速约4.4倍**。当训练至相同的110K步时，VA-RoPE在所有指标上均超越基线，证实了加速并非以牺牲最终性能为代价。

Figure 6提供了这一加速效应的视觉佐证：在25K步时，VA-RoPE生成的几何法向图已与输入图像高度吻合，而vanilla基线的输出仍存在明显的几何错位和漂浮伪影。随着训练推进至110K步，VA-RoPE的法向图质量进一步提升，与真值的IS-AS匹配度持续领先。

### 消融实验

为解耦ViLearn各组件的贡献，我们设计了系统的消融实验，所有变体使用相同的AdamW优化器（lr=0.0001）和约8天的训练时长。

**可见性感知位置编码的关键性。** Figure 7对比了四种配置的训练曲线：
- **ViLearn w/ VA-RoPE**：收敛最快，最终指标最优。
- **ViLearn w/ VA-LPE**：收敛显著优于vanilla基线，但略逊于VA-RoPE，表明可学习加性嵌入同样能有效注入可见性信息，但旋转位置编码在建模类内/跨类交互方面更具优势。
- **Ours w/ Vanilla RoPE**：该变体保留了可见性分组（VG）模块，但将VA-RoPE替换为标准RoPE，移除了可见性感知机制。其收敛速度和最终性能均明显低于VA-RoPE和VA-LPE，证实了**可见性自适应编码是不可或缺的性能驱动因素**，单纯的token分组不足以充分引导模型。
- **Vanilla VecSet baseline**：无VG、无VAPE，收敛最慢，最终指标最低。

**可见性分组的几何有效性。** Figure 2提供了VG模块的直接证据：将完整形状token集按可见性划分为可见子集（VST）和不可见子集（IST）后分别解码，可见token重建出与输入视角一致的可见表面，而不可见token则编码了遮挡区域的互补几何。这一解耦验证了VG确实将可见重建与不可见幻觉分离开来，为VAPE提供了干净的几何结构先验。

### 失败模式与局限性

尽管ViLearn取得了显著性能提升，但分析揭示了以下局限：

1. **固定划分策略的刚性。** 推理时采用前1/3为可见token、后2/3为不可见token的固定比例划分，未根据输入图像的视角、遮挡程度或物体类别进行动态调整。在极端仰角、俯角或严重遮挡场景下，该固定比例可能无法精确匹配实际的可见几何范围。

2. **对预训练解码器的依赖。** VG模块依赖预训练VecSet解码器的交叉注意力分数来建立可见点与形状token的对应关系。对于训练数据中罕见的物体类别或具有复杂拓扑的形状，解码器的注意力质量可能下降，导致可见性分组出现偏差，进而影响VAPE的输入质量。

3. **表示形式的泛化性未验证。** 当前方法仅在VecSet表示上进行了验证，其对其他3D表示（如voxel-based、triplane-based）的适用性尚未探索。

### 开放问题

基于上述分析，以下方向值得进一步探索：
- 能否设计自适应机制，根据输入图像动态确定可见token的比例和选择策略？
- 可见性分组对输入图像中的遮挡、噪声或极端光照条件的鲁棒性如何？
- VA-RoPE中旋转角度$m$、$n$的选择是否可学习化，或需要更细致的调优策略以适应不同数据分布？
- 该方法是否可扩展到text-to-3D等多模态条件生成任务？

### 补充图表

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/008_Table_1.jpg]]
*Table 1: Final-step (110K) metrics of ViLearn, the vanilla baseline, and SOTA VecSet-based models of comparable size (1.1B or 1.3B). ViLearn performs best in all metrics*

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/007_Figure_7.jpg]]
*Figure 7: Training Steps vs. metric on different ablation models*

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/006_Figure_6.jpg]]
*Figure 6: Visual comparisons for ablation models across training steps. We render the geometric normals for all the generated meshes and showcase the most matched normal compared to the estimated normal of the input image using the IS-AS metric. Our method with VA-RoPE achieves the baseline’s performance in only 25K iterations (approximately 4.4× faster), and reaches the best performance when trained for the same 110K iterations*

![[assets/figures/papers/paper_list_l2273_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_ViLearn_Accelerat/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative Comparison: Our Scaled Model vs. Scaled Baseline vs. SOTAs. For single-image-to-3D, we compare the quality of generated meshes among our scaled model (ViLearn), scaled vanilla baseline, and state-of-the-art (SOTA) open-sourced models, all with comparable model parameters: 1.1B (ours, baseline, Hunyuan3D 2.0 [50]) and 1.3B (TripoSG [23], Step1X-3D [22]), using the Image-Shape Alignment Score (range 0-1, higher is better) in Sec. 5.2. Note that while SOTA models [22, 23, 50] typically train on hundreds of GPUs for weeks, we achieve the best alignment with only 32 GPUs by accelerating convergence with visibility learning*

## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

ViLearn 针对的是 **VecSet-based 图像到3D生成** 中一个被忽视的结构性瓶颈：VecSet 表示将3D形状压缩为一组无序的1D token，且不包含显式的位置编码。在这种设定下，扩散模型被迫在一个庞大的置换不变token空间中**同时学习可见对应关系与不可见几何的幻觉**，导致假设空间巨大、训练收敛缓慢且不稳定。

ViLearn 的核心洞察在于：**通过显式告知扩散模型哪些形状token对应可见几何、哪些对应遮挡区域，可以将可见重建与不可见幻觉解耦，从而缩小假设空间并提供清晰的几何结构引导**。这一思路将3D生成中的“可见性”从隐式学习目标提升为一阶归纳偏置，直接注入到扩散Transformer的注意力机制中。

### 2. 方法谱系定位

#### 2.1 上游基础

ViLearn 建立在两个成熟的技术栈之上：

- **VecSet 表示与MM-DiT架构**：ViLearn 沿用 VecSet VAE（3D tokenizer）将3D形状压缩为无序token，并以 Multimodal Diffusion Transformer（MM-DiT）作为条件扩散去噪的主干网络。MM-DiT 的双流注意力块通过拼接形状token和图像token的投影来实现双向交叉注意力：
  
  $$Q = \mathrm{Concat}[Q_{\mathrm{shape}}, Q_{\mathrm{image}}], \quad K = \mathrm{Concat}[K_{\mathrm{shape}}, K_{\mathrm{image}}], \quad V = \mathrm{Concat}[V_{\mathrm{shape}}, V_{\mathrm{image}}]$$
  
  图像token来自视觉编码器（如DINOv2），形状token来自VecSet tokenizer。这一架构在 **Hunyuan3D 2.0**（Tencent Hunyuan3D Team, 2025）、**TripoSG**（Li et al., 2025）和 **Step1X-3D** 等SOTA模型中已被广泛采用。

- **可见点图（Visible Points Map）**：ViLearn 利用渲染的可见表面点作为查询，通过预训练VecSet解码器的交叉注意力分数来索引可见token。这一机制借鉴了3D重建中显式可见性建模的思想，但将其创造性地应用于扩散模型的训练数据准备阶段。

#### 2.2 与Baseline的关键差异

| 维度 | Vanilla VecSet Training | ViLearn |
|------|------------------------|---------|
| **Token组织** | 无序集合，无位置编码 | 按可见性划分为VST（可见）和IST（不可见）子集 |
| **位置编码** | 无（置换不变） | VA-RoPE或VA-LPE，按可见性赋予差异化编码 |
| **注意力机制** | 统一的跨模态交互 | 可见token与图像token共享编码以强化对应学习；不可见token独立编码以支持遮挡几何幻觉 |
| **训练效率** | 需110K步收敛 | 25K步即达到baseline的110K步性能（4.4×加速） |

Vanilla VecSet training 将形状token视为完全置换不变的集合，这一设计虽然在理论上保证了表示的灵活性，但迫使模型在巨大的组合空间中自行发现可见性结构。ViLearn 通过 **Visibility Grouping（VG）** 和 **Visibility-Aware Positional Encoding（VAPE）** 两个协同组件，将可见性结构作为显式归纳偏置注入训练过程。

#### 2.3 与SOTA的关系

ViLearn 的最终性能超越了同等参数规模的SOTA VecSet-based模型，包括 **Hunyuan3D 2.0**（1.1B）、**TripoSG**（1.3B）和 **Step1X-3D**（1.3B）。在 Table 1 的最终步（110K）指标中，ViLearn 在所有指标上均表现最优：

- **IS-AS（图像-形状对齐分数）**：0.702 vs. baseline 0.656（+7%相对增益）
- **Floater（浮动几何指标，越低越好）**：31.5 vs. baseline 74.8（57.8%降低）

值得注意的是，ViLearn 仅使用 **32块GPU** 即达到最佳对齐效果，而上述SOTA模型通常在数百块GPU上训练数周。这一效率优势直接源于可见性学习带来的收敛加速。

### 3. 适用边界与局限

#### 3.1 已知局限

1. **固定token划分比例**：推理时采用固定的可见/不可见划分（前1/3为可见，后2/3为不可见），这一启发式策略可能无法精确适配所有输入视角。对于极端视角或复杂遮挡场景，固定比例可能导致可见token不足或冗余。

2. **对预训练解码器的依赖**：VG 的可见性索引依赖于预训练VecSet解码器的交叉注意力质量。对于未见过的物体类别或复杂形状，解码器的注意力分布可能产生偏差，导致可见性分组不准确。这一依赖关系构成了方法的潜在脆弱点。

3. **表示形式的泛化性未验证**：目前仅在VecSet表示上验证了ViLearn的有效性。对于其他3D表示形式（如voxel-based、triplane-based或NeRF-based），可见性学习的适用性和效果尚不明确。

#### 3.2 适用场景

- **单图像到3D生成**：这是ViLearn的直接应用场景，尤其适合需要快速训练迭代和高质量几何对齐的任务。
- **资源受限的训练环境**：ViLearn 的4.4×收敛加速使其在GPU资源有限的场景下具有显著优势。
- **需要显式可见性建模的下游任务**：如3D编辑、视角补全等，可见/不可见token的分离提供了结构化的中间表示。

### 4. 开放问题

1. **自适应可见token比例**：能否设计自适应机制动态确定可见token的数量或比例，而非固定划分？例如，基于输入图像的复杂度或视角信息来调整VST/IST的划分策略，可能进一步提升鲁棒性。

2. **对遮挡和噪声的鲁棒性**：VG 对输入图像中的遮挡、噪声或极端视角的鲁棒性如何？当前方法假设渲染的可见点图是准确的，但在真实场景中，条件图像可能包含自遮挡、物体间遮挡或成像噪声。

3. **跨任务扩展**：可见性学习是否可扩展到其他3D生成任务（如text-to-3D）？在文本条件下，可见性结构需要从语义理解中推断，而非直接从条件图像渲染，这带来了新的挑战。

4. **VA-RoPE中旋转角度的优化**：VA-RoPE 使用预定义的旋转矩阵 $R_m$（可见类）和 $R_n$（不可见类），其旋转角度 $m$ 和 $n$ 的选择是否可以学习或需要更细致的调优策略？当前消融实验显示VA-RoPE优于VA-LPE，但旋转角度的敏感性分析尚未充分展开。

5. **与多视角信息的结合**：当前方法仅利用单一条件图像的可见性信息。如果能结合多视角或多光照条件下的可见性结构，可能进一步提升不可见几何的幻觉质量。

### 5. 知识库定位总结

ViLearn 在图像到3D生成领域的方法谱系中占据了一个独特的位置：它**不是提出新的骨干架构或tokenizer，而是通过注入可见性归纳偏置来改造现有的VecSet+MM-DiT训练范式**。这一思路与传统的“改进表示”或“增大模型”路径正交，属于**训练策略与结构引导**层面的创新。其4.4×的收敛加速和57.8%的Floater指标降低，以较小的工程代价（仅修改数据准备和注意力编码）换取了显著的性能提升，为后续工作在效率与质量之间寻求平衡提供了可参考的范式。

## 原文 PDF

![[paperPDFs/CVPR_2026/ViLearn_Accelerating_Training_Convergence_of_Image_to_3D_Generation_via_Visibility_Learning.pdf]]
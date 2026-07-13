---
title: "VIMCAN: Visual-Inertial 3D Human Pose Estimation with Hybrid Mamba-Cross-Attention Network"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VIMCAN_Visual_Inertial_3D_Human_Pose_Estimation_with_Hybrid_Mamba_Cross_Attention_Network.pdf
project_link: null
code_link: "https://github.com/Eddieyzp/VIMCAN"
aliases:
- VIMCAN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用线性复杂度的Mamba进行时间序列建模以提升效率，同时引入Cross-Attention进行跨模态空间依赖提取和融合，从而同时解决效率与精度问题。
primary_logic: 通过将Mamba的高效序列处理与Cross-Attention的跨模态空间推理相结合，设计出混合架构，在保持线性复杂度的同时实现高性能的视觉-惯性融合姿态估计。
claims:
- VIMCAN在长序列推理中内存使用远低于基于GCN-Transformer的融合方法，且吞吐量更高（图1）。
- 在TotalCapture数据集上，VIMCAN的MPJPE为17.2 mm（GT 2D）或31.2 mm（SimpleNet），均显著优于Wang's GCN-Transformer方法（表1, 表7）。
- 消融实验表明，Cross-Attention融合策略相比纯视觉Self-Attention基线将MPJPE降低9.7 mm，证明了跨模态空间推理的关键作用（表5）。
- TotalCapture 上 MPJPE (P1, mm) = 31.2 (VIMCAN-B with SimpleNet 2D)
---

# VIMCAN: Visual-Inertial 3D Human Pose Estimation with Hybrid Mamba-Cross-Attention Network

> [!tip] 核心洞察
> 通过将Mamba的高效序列处理与Cross-Attention的跨模态空间推理相结合，设计出混合架构，在保持线性复杂度的同时实现高性能的视觉-惯性融合姿态估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | VIMCAN: 混合Mamba-交叉注意力网络的视觉-惯性三维人体姿态估计 |
| 英文题名 | VIMCAN: Visual-Inertial 3D Human Pose Estimation with Hybrid Mamba-Cross-Attention Network |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.07552) · [Code](https://github.com/Eddieyzp/VIMCAN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VIMCAN |
| Dataset | TotalCapture |

> [!tip] 效果简介
> - TotalCapture 上，MPJPE (P1, mm) 31.2 (VIMCAN-B with SimpleNet 2D) vs 34.9 (Wang's GCN-Transformer) (-3.7)。

## 概要

视觉-惯性三维人体姿态估计旨在融合RGB图像关键点与惯性测量单元（IMU）数据，以在遮挡、快速运动等挑战场景下获得鲁棒的姿态预测。现有主流方法多基于Transformer架构，其自注意力机制在长序列建模中面临**二次计算复杂度**，导致实时推理时内存占用高、吞吐量低；而纯Mamba方法虽具备线性复杂度优势，却在多模态融合中难以充分捕捉跨模态的空间依赖关系。

针对这一效率与精度的两难困境，本文提出**VIMCAN**——一种混合Mamba-交叉注意力网络。其核心洞见在于：将Mamba的高效时序建模能力与交叉注意力（Cross-Attention）的跨模态空间推理能力解耦并协同，在保持线性复杂度的前提下实现高性能的视觉-惯性融合。具体而言，VIMCAN以视觉关键点作为Query、IMU特征作为Key/Value计算分组多头交叉注意力，使视觉分支能够主动查询惯性分支的空间信息，从而弥补纯Mamba融合在空间依赖建模上的不足。

实验结果表明，VIMCAN在TotalCapture数据集上取得了**17.2 mm**（使用真值2D关键点）和**31.2 mm**（使用SimpleNet检测器）的平均关节位置误差（MPJPE），显著优于基于GCN-Transformer的融合方法（Wang et al., 2025）的34.9 mm。在推理效率方面，VIMCAN的峰值内存占用远低于GCN-Transformer方法，且吞吐量更高，验证了混合架构在实时部署场景下的优势。消融实验进一步揭示，引入交叉注意力融合相比纯视觉自注意力基线将MPJPE降低了**9.7 mm**，确认了跨模态空间推理的关键作用。

**方法定位**：VIMCAN属于视觉-惯性融合姿态估计中的混合架构路线，在时序建模层采用状态空间模型（Mamba）替代Transformer，在多模态融合层采用交叉注意力替代简单的特征拼接或自注意力。相较于纯视觉Mamba方法（如PoseMamba，Huang et al., AAAI 2025），VIMCAN通过引入惯性模态和交叉注意力融合实现了显著的精度提升；相较于GCN-Transformer融合方法，VIMCAN在精度和效率上均取得领先。



三维人体姿态估计是计算机视觉与机器人领域的核心任务，在运动分析、人机交互、增强现实等场景中具有广泛应用。纯视觉方法虽能提供丰富的空间信息，但在遮挡、快速运动或光照变化下容易出现关节漂移甚至失效；惯性传感器（IMU）则不受视觉退化影响，能稳定捕捉肢体的旋转与加速度，却难以提供绝对位置约束。因此，**视觉-惯性融合**成为提升姿态估计鲁棒性与精度的关键路径。

然而，现有的视觉-惯性融合方法面临一个根本性瓶颈：**基于Transformer的架构在处理长序列时具有二次计算复杂度**，导致实时推理的内存占用和延迟急剧上升。以 **Wang's GCN-Transformer**（Wang et al., Robotics Comput. Integr. Manuf. 2025）为代表的融合方法，在序列长度增加时峰值内存呈超线性增长（见Figure 1），严重限制了其在资源受限设备上的部署能力。另一方面，纯Mamba方法（如 **PoseMamba**，Huang et al., AAAI 2025）虽然具备线性复杂度，但在多模态融合中捕捉跨模态空间依赖关系的能力不足——Mamba的扫描机制擅长序列建模，却缺乏对视觉与惯性特征之间显式的空间对齐与交互推理。

这一困境揭示了领域内的一个核心矛盾：**效率与精度在多模态长序列建模中难以兼得**。Transformer的Self-Attention能灵活建模全局空间依赖，但计算代价高昂；Mamba高效却缺乏跨模态空间推理的机制。本文的动机正是打破这一折衷——**能否设计一种混合架构，既保留Mamba的线性复杂度优势，又引入Cross-Attention来补偿跨模态空间推理的缺失？**

VIMCAN的核心洞察在于：将Mamba的高效时序处理与Cross-Attention的跨模态空间推理解耦并协同工作。Mamba负责各模态内部的时空特征提取，保证整体计算效率；Cross-Attention则以视觉特征为Query、惯性特征为Key/Value，显式建立跨模态的空间对应关系，弥补纯Mamba在融合阶段的语义对齐缺陷。这一混合设计使得VIMCAN在TotalCapture数据集上达到**17.2 mm MPJPE**（GT 2D输入），同时推理内存远低于GCN-Transformer基线（Figure 1），在长序列场景下吞吐量显著提升，为视觉-惯性姿态估计的实时部署提供了新的技术路线。



## 核心方法与创新机理

VIMCAN的核心创新在于**将Mamba的高效序列建模能力与交叉注意力的跨模态空间推理能力相结合**，构建了一个面向视觉-惯性三维人体姿态估计的混合架构。该设计直击现有方法的两个关键瓶颈：基于Transformer的方法在处理长序列时具有二次计算复杂度，导致实时推理困难；而纯Mamba方法虽有线性复杂度，但在多模态融合中捕捉复杂空间依赖关系的能力不足。

### 创新一：双向时空状态空间模型（BiSTSSM）替代自注意力

VIMCAN用**双向时空状态空间模型（BiSTSSM）**替换了传统Transformer中的自注意力机制（Self-Attention）或图卷积网络（GCN），这是其效率提升的核心来源。BiSTSSM基于Mamba架构，通过四向扫描（SS2D）和门控机制实现线性复杂度的时序建模，具体流程为：

$$F_{x}^{ssm} = \mathrm{LN}(\mathrm{SS2D}(\sigma(\mathrm{DWConv}(F_{x}))))$$

$$F_{y}^{ssm} = F_{x}^{ssm} \cdot \sigma(F_{z})$$

$$Y^{ssm} = \mathrm{FC}(F_{y}^{ssm}) + F$$

其中输入特征 $F$ 经全连接层投影并分割为特征部分 $F_x$ 和门控部分 $F_z$，$F_x$ 依次经过深度可分离卷积（DWConv）、SiLU激活函数、四向扫描（SS2D）和层归一化（LN），再通过门控机制与 $F_z$ 相乘，最后经全连接层投影回原维度并加残差连接。

与纯视觉自注意力基线（**PoseMamba**，Huang et al., AAAI 2025 的纯Mamba方案）相比，这一替换本身并非简单复制——VIMCAN进一步引入了**骨架感知的扫描策略**：视觉分支采用骨架拓扑引导的双向扫描，惯性分支采用四向扫描，使得状态空间模型能够感知人体关节的空间邻接关系。消融实验（Table 4）表明，骨架感知扫描在保持相近参数量的同时提升了精度。

### 创新二：分组多头交叉注意力融合策略

这是VIMCAN在**多模态融合策略**上的关键创新。传统方法通常采用特征拼接或自注意力进行视觉-惯性融合，而VIMCAN设计了**分组多头交叉注意力（Grouped Multi-Head Cross-Attention）**，将视觉特征作为Query，IMU特征作为Key和Value：

$$\mathbf{MHCA} = \mathbf{Concat}\left[\mathrm{Softmax}\left(\frac{Q_g^V {K_g^I}^\top}{\sqrt{d_k}}\right) V_g^I\right]_h, \quad Z_g = \mathbf{LN}(\mathbf{MHCA}) + Q_g^V$$

这一设计的核心洞察在于：**视觉关键点提供精确的空间位置信息，IMU提供鲁棒的绝对方向信息**，将视觉设为Query可以保留视觉的空间结构，而IMU作为Key/Value则向视觉特征注入惯性方向约束。残差连接 $+Q_g^V$ 进一步保证了视觉空间信息不被稀释。

消融实验（Table 5）提供了决定性证据：与纯视觉自注意力基线（26.9 mm）相比，集成IMU并通过Cross-Attention融合将MPJPE降至17.2 mm，**差异达9.7 mm**，证明了跨模态空间推理的关键作用。相比之下，采用Cross-Mamba（纯Mamba融合）的方案精度明显不及Cross-Attention，验证了交叉注意力在捕捉跨模态空间依赖方面优于纯序列建模。

### 创新三：骨架感知的分组扫描与融合

VIMCAN将人体关节按骨架拓扑分为 $G=5$ 组（躯干、左臂、右臂、左腿、右腿），IMU也对应划分为5组（Figure 3）。这种分组策略使得：

- **视觉分支**：骨架感知的BiSTSSM扫描能够利用关节间的物理连接关系，提升时空建模的结构一致性；
- **惯性分支**：各IMU组独立提取时空特征，保留肢体运动的局部特性；
- **融合阶段**：分组交叉注意力在组内进行视觉-惯性对齐，避免全局融合带来的信息混淆。

Table 4的消融实验验证了分组策略的有效性：适当的分组数量在精度和效率之间取得平衡。

### 方法谱系与知识库定位

VIMCAN处于**视觉-惯性融合三维人体姿态估计**这一研究脉络中，其直接对比的基线包括：

- **Wang's GCN-Transformer**（Wang et al., Robotics Comput. Integr. Manuf. 2025）：基于GCN和Transformer的混合架构，是视觉-惯性融合的代表性方法。VIMCAN在TotalCapture数据集上以31.2 mm（SimpleNet 2D）显著优于该方法的34.9 mm（Table 7），且在长序列推理中内存使用远低于GCN-Transformer（Figure 1），吞吐量更高。
- **PoseMamba**（Huang et al., AAAI 2025）：纯视觉Mamba姿态估计模型。VIMCAN通过引入IMU模态和交叉注意力融合，在精度上大幅超越纯视觉方案。

VIMCAN的贡献在于证明了**线性复杂度的状态空间模型可以替代Transformer进行多模态姿态估计的时序建模**，同时**交叉注意力是Mamba框架下实现高效跨模态融合的关键组件**。这一混合设计为实时、低功耗的视觉-惯性姿态估计系统提供了新的架构范式。

### 局限与待验证问题

当前方法的一个显著局限是**依赖严格的传感器标定**：IMU到人体骨段的旋转矩阵 $\mathbf{R}_B^I$ 需预先精确测量，限制了即插即用的部署灵活性。此外，以下问题有待进一步验证：

- 在更多样化的运动场景和复杂遮挡下，混合Mamba-Cross-Attention架构的鲁棒性如何？
- 如何开发自适应标定或在线标定技术以减少对预标定的依赖？



VIMCAN 的整体架构遵循“双流特征提取 → 分组交叉注意力融合 → 全局时空建模 → 姿态回归”的流水线，其核心设计思想是将 Mamba 的高效序列建模能力与 Cross-Attention 的跨模态空间推理能力相结合，在保持线性复杂度的同时实现高性能的视觉-惯性融合姿态估计。

### 输入表示

模型接收双模态输入：

- **视觉流**：来自单目 RGB 视频的 $J=17$ 个关键点的二维坐标，归一化至 $[-1, 1]$ 范围。
- **惯性流**：来自 $I=6$ 个 IMU 传感器的单位四元数测量值，分别佩戴于骨盆、胸骨及四肢。IMU 按人体部位划分为 $G=5$ 组（躯干、左臂、右臂、左腿、右腿），如图 3 所示。

### 双流特征提取

视觉和惯性输入分别进入独立的时空建模模块（图 2）：

- **视觉分支**：采用骨架感知的 STMamba（Skeleton-aware STMamba），利用人体骨架拓扑结构指导双向扫描路径，提取关键点的时空特征。
- **惯性分支**：采用部位感知的 STMamba（Part-aware STMamba），对各 IMU 组分别进行时空建模，捕捉不同身体部位的运动模式。

两个分支均以 BiSTSSM（Bidirectional Spatio-Temporal State Space Model）为基本构建块。BiSTSSM 模块（图 4）的内部流程为：输入特征 $F$ 经全连接层投影后切分为特征部分 $F_x$ 和门控部分 $F_z$（式 1），$F_x$ 依次经过深度卷积、SiLU 激活、SS2D 四向扫描和层归一化得到 $F_x^{ssm}$（式 2），再与经 SiLU 激活的门控信号 $F_z$ 逐元素相乘获得门控输出 $F_y^{ssm}$（式 3），最后通过残差连接和 MLP 得到模块最终输出 $Y$（式 4）：

$$F_{x}, F_{z} = \operatorname{Chunk}(\operatorname{FC}(F)) \tag{1}$$

$$F_{x}^{ssm} = \mathrm{LN}(\mathrm{SS2D}(\sigma(\mathrm{DWConv}(F_{x})))) \tag{2}$$

$$F_{y}^{ssm} = F_{x}^{ssm} \cdot \sigma(F_{z}) \tag{3}$$

$$Y^{ssm} = \mathrm{FC}(F_{y}^{ssm}) + F, \quad Y = \mathrm{MLP}(\mathrm{LN}(Y^{ssm})) + Y^{ssm} \tag{4}$$

### 分组交叉注意力融合

双流特征提取后，视觉与惯性特征进入 Cross-Attention 融合模块。该模块按人体部位分组进行多头交叉注意力计算：视觉特征作为 Query（$Q_g^V$），惯性特征作为 Key（$K_g^I$）和 Value（$V_g^I$），通过注意力机制实现跨模态信息交互（式 5）。残差连接将原始视觉 Query 加回注意力输出，以保留视觉空间信息：

$$\mathbf{MHCA} = \mathbf{Concat}\left[\mathrm{Softmax}\left(\frac{Q_g^V {K_g^I}^\top}{\sqrt{d_k}}\right) V_g^I\right]_h, \quad Z_g = \mathbf{LN}(\mathbf{MHCA}) + Q_g^V \tag{5}$$

消融实验（表 5）表明，该 Cross-Attention 融合策略相比纯视觉 Self-Attention 基线将 MPJPE 降低 9.7 mm（从 26.9 mm 降至 17.2 mm），验证了跨模态空间推理对精度提升的关键作用。

### 全局时空建模与姿态回归

分组融合后的特征 $Z_g$ 经全连接层降维后，送入堆叠的骨架感知 STMamba 模块进行全局时空建模，进一步捕捉全身关节间的长程依赖关系。最终，姿态回归头将融合特征映射为三维关节坐标。

### 训练目标

模型以端到端方式训练，总损失函数为四项损失的加权组合（式 10）：

$$\mathcal{L}_{\mathrm{Total}} = \lambda_{\mathrm{MPJPE}} \cdot \mathcal{L}_{\mathrm{MPJPE}} + \lambda_{\mathrm{N-MPJPE}} \cdot \mathcal{L}_{\mathrm{N-MPJPE}} + \lambda_{\mathrm{V}} \cdot \mathcal{L}_{\mathrm{V}} + \lambda_{\mathrm{TC}} \cdot \mathcal{L}_{\mathrm{TC}} \tag{10}$$

其中 $\mathcal{L}_{\mathrm{MPJPE}}$ 为平均关节位置误差，$\mathcal{L}_{\mathrm{N-MPJPE}}$ 为尺度归一化后的位置误差，$\mathcal{L}_{\mathrm{V}}$ 为速度一致性损失，$\mathcal{L}_{\mathrm{TC}}$ 为时序一致性损失。

### 替代融合方案：Cross-Mamba

作者还提出了 Cross-Mamba 作为替代融合模块（图 5）。与 Cross-Attention 不同，Cross-Mamba 采用 Cross-SSM 沿空间轴拼接视觉与惯性特征，并通过双向扫描（SS1D）进行融合。消融实验（表 5）中 Cross-Mamba 变体的性能可供参考，但 Cross-Attention 方案在精度上更具优势。

**架构优势总结**：VIMCAN 的混合设计使模型在保持线性计算复杂度的同时，兼具 Mamba 的长序列高效处理能力和 Cross-Attention 的跨模态空间推理能力。如图 1 所示，VIMCAN 在长序列推理时的峰值内存使用远低于基于 GCN-Transformer 的融合方法，且吞吐量更高，验证了该架构在实时推理场景下的效率优势。

### 补充图表

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/002_Figure_2.jpg]]
*Figure 2: The framework of VIMCAN*

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of skeleton topology and group components*



### 整体架构概览

VIMCAN 的完整框架如 **Figure 2** 所示，由四个核心阶段构成：视觉特征提取、惯性特征提取、跨模态融合、全局时空建模与姿态回归。模型接收 $J=17$ 个 2D 关键点坐标（视觉分支）和 $I=6$ 个 IMU 的四元数测量值（惯性分支）作为输入。IMU 按人体部位划分为 $G=5$ 组：躯干、左臂、右臂、左腿、右腿（**Figure 3**）。

### 双向时空状态空间模型（BiSTSSM）

BiSTSSM 是 VIMCAN 的基础构建块（**Figure 4**），其核心计算流程如下：

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/004_Figure_4.jpg]]
*Figure 4: The architecture of BiSTSSM module*

**特征投影与分割**：输入特征 $F$ 首先通过全连接层投影到内部 SSM 维度，然后沿通道维度分割为特征部分 $F_x$ 和门控部分 $F_z$：

$$F_x, F_z = \operatorname{Chunk}(\operatorname{FC}(F)) \tag{1}$$

**SS2D 扫描与门控**：对 $F_x$ 依次应用深度可分离卷积（DWConv）、SiLU 激活函数 $\sigma$、四向扫描（SS2D）和层归一化（LN），得到扫描输出：

$$F_x^{ssm} = \mathrm{LN}(\mathrm{SS2D}(\sigma(\mathrm{DWConv}(F_x)))) \tag{2}$$

随后通过门控机制将扫描输出与 $F_z$ 融合：

$$F_y^{ssm} = F_x^{ssm} \cdot \sigma(F_z) \tag{3}$$

**残差连接与 MLP**：门控输出经全连接层投影回原始维度后与输入 $F$ 相加，再通过 MLP 和残差连接得到最终输出：

$$Y^{ssm} = \mathrm{FC}(F_y^{ssm}) + F, \quad Y = \mathrm{MLP}(\mathrm{LN}(Y^{ssm})) + Y^{ssm} \tag{4}$$

### 骨架感知与分组扫描策略

视觉分支采用**骨架感知的双向扫描**：根据人体骨架拓扑结构（**Figure 3**），将 17 个关键点按骨骼连接关系组织成序列，沿骨架链进行双向扫描以捕捉空间依赖。惯性分支则采用**部位感知的四向扫描**：5 个 IMU 组各自独立进行四向扫描，分别建模躯干和四肢的运动模式。消融实验（**Table 4**）表明，骨架感知扫描相比无骨架先验的扫描方案能显著降低 MPJPE，同时仅引入可忽略的参数量增加。

### 跨模态融合模块

融合模块采用**分组多头交叉注意力**（Grouped Multi-Head Cross-Attention），视觉特征作为 Query，惯性特征作为 Key 和 Value。对于第 $g$ 组，计算如下：

$$\mathbf{MHCA}_g = \mathbf{Concat}\left[\mathrm{Softmax}\left(\frac{Q_g^V {K_g^I}^\top}{\sqrt{d_k}}\right) V_g^I\right]_h \tag{5}$$

$$Z_g = \mathbf{LN}(\mathbf{MHCA}_g) + Q_g^V$$

其中 $Q_g^V$ 为视觉分支的分组特征，$K_g^I$ 和 $V_g^I$ 为惯性分支的分组特征，$h$ 表示多头拼接。残差连接 $+ Q_g^V$ 保留了视觉空间结构信息。各组的融合特征 $Z_g$ 拼接后送入后续的全局骨架感知 STMamba 堆栈进行深层时空建模。

**Cross-Mamba 替代方案**：论文同时提出了 Cross-Mamba 模块（**Figure 5**）作为融合的替代方案。与 SS2D 的四向扫描不同，Cross-SSM 将视觉和惯性特征沿空间轴拼接后采用双向扫描（SS1D），以对齐两种模态的空间维度。消融实验（**Table 5**）显示 Cross-Attention 融合策略优于 Cross-Mamba，验证了跨模态空间推理在视觉-惯性融合中的关键作用。

### 损失函数

VIMCAN 采用四项损失的加权组合进行端到端训练：

$$\mathcal{L}_{\mathrm{Total}} = \lambda_{\mathrm{MPJPE}} \cdot \mathcal{L}_{\mathrm{MPJPE}} + \lambda_{\mathrm{N-MPJPE}} \cdot \mathcal{L}_{\mathrm{N-MPJPE}} + \lambda_{\mathrm{V}} \cdot \mathcal{L}_{\mathrm{V}} + \lambda_{\mathrm{TC}} \cdot \mathcal{L}_{\mathrm{TC}} \tag{10}$$

其中 $\mathcal{L}_{\mathrm{MPJPE}}$ 为平均每关节位置误差（L2 距离），$\mathcal{L}_{\mathrm{N-MPJPE}}$ 为经尺度因子 $s$ 对齐后的归一化 MPJPE 损失，$\mathcal{L}_{\mathrm{V}}$ 为速度一致性损失（相邻帧关节位移的 L2 误差），$\mathcal{L}_{\mathrm{TC}}$ 为时序一致性损失（约束预测加速度的平滑性）。

### 补充图表

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/005_Figure_5.jpg]]
*Figure 5: The architecture of Cross-Mamba module*



## 实验与关键发现

### 核心实验设置

VIMCAN 在两个主流人体姿态估计基准上进行了全面评估：**TotalCapture**（多模态室内数据集，含 RGB 视频与 6 个 IMU）和 **3DPW**（室外自然场景，使用合成 IMU 数据）。评估指标包括 **MPJPE（P1，平均每关节位置误差，mm）** 和 **P-MPJPE（P2，Procrustes 对齐后的 MPJPE）**，效率指标涵盖参数量、峰值内存（MB）和帧率（FPS）。

视觉输入为从单目 RGB 视频提取的 17 个 2D 关键点坐标（归一化至 $[-1, 1]$），分别使用 **MediaPipe**、**SimpleNet** 和 **Ground-Truth（GT）** 三种 2D 检测器。惯性输入为 6 个 IMU 的单位四元数测量值，IMU 按身体部位划分为 5 组（躯干、左臂、右臂、左腿、右腿）。训练采用加权组合损失函数 $\mathcal{L}_{\mathrm{Total}}$（Eq. 10），联合优化位置误差、尺度归一化位置误差、速度误差和时序一致性。

### 主实验结果

#### TotalCapture 性能对比（Table 1）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/006_Table_1.jpg]]
*Table 1: The performance comparison on TotalCapture dataset with different visual-inertial fusion methods. #IMUs: Number of IMUs used. 2D: Type of 2D pose detector (MP: MediaPipe, SN: SimpleNet, GT: Ground-Truth). S: Seen subject. U: Unseen subject. W: Walking. A: Acting. FS: Freestyle. P1: Average MPJPE (mm) across all test sets (lower is better). P2: Procrustes-aligned MPJPE (mm, lower is better)*

在 TotalCapture 数据集上，VIMCAN 在所有 2D 检测器配置下均显著优于现有视觉-惯性融合方法：

- **GT 2D 输入**：VIMCAN 达到 **P1 17.2 mm，P2 13.8 mm**，相比 **Wang's GCN-Transformer**（Wang et al., Robotics Comput. Integr. Manuf. 2025）的 P1 21.2 mm 降低了 4.0 mm。
- **SimpleNet 2D 输入**：VIMCAN-B 配置达到 **P1 31.2 mm，P2 23.6 mm**，相比 Wang's GCN-Transformer 的 P1 34.9 mm 降低了 3.7 mm。
- **MediaPipe 2D 输入**：VIMCAN 达到 **P1 33.2 mm，P2 25.7 mm**，同样优于对比方法。

在 Seen/Unseen 主体和 Walking/Acting/Freestyle 各子集上，VIMCAN 均保持一致的领先优势，验证了方法的跨主体和跨动作泛化能力。

#### 3DPW 性能对比（Table 2）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/007_Table_2.jpg]]
*Table 2: The performance comparison on 3DPW testing set using MediaPipe 2D pose detector*

在 3DPW 测试集上使用 MediaPipe 2D 检测器，VIMCAN 达到 **P1 45.3 mm**，优于先前方法。需注意 3DPW 使用合成 IMU 数据，可能无法完全反映真实惯性传感器的噪声特性，该结果需在此前提下解读。

### 计算效率分析（Table 7, Figure 1）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/001_Figure_1.jpg]]
*Figure 1: The comparison of peak memory usage during inference for a GCN-Transformer-based model [29] and the proposed VIMCAN. The peak memory usage at different lengths of input sequence. The x-axis denotes sequence length, and the y-axis represents peak memory usage (lower is better, in MB). The circles indicate the GCN-Transformer-based model, while the stars denote VIMCAN. The size of Symbol reflects the memory I/O throughput, illustrating computational efficiency during on-device inference*

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/013_Table_7.jpg]]
*Table 7: The comparison for computational efficiency on Total-Capture testing set. P1: Average MPJPE (mm). #Params.: Number of parameters. Peak: Peak Memory (MB). FPS: Frames Per Second*

VIMCAN 的核心优势在于**线性计算复杂度**带来的高效率。在 TotalCapture 测试集上：

- **VIMCAN-B** 参数量 7.3M，峰值内存 **423 MB**，帧率 **128 FPS**，P1 31.2 mm。
- 相比之下，**Wang's GCN-Transformer** 参数量 7.9M，峰值内存 **1,561 MB**，帧率仅 **42 FPS**，P1 34.9 mm。
- **VIMCAN-L** 参数量 11.2M，峰值内存 1,079 MB，仍远低于 GCN-Transformer。

**Figure 1** 展示了推理时峰值内存随序列长度的变化趋势：GCN-Transformer 的内存占用随序列长度急剧增长（二次复杂度），而 VIMCAN 保持近乎线性的内存增长，在长序列场景下优势尤为明显。图中以圆圈和星形分别标注两种方法，符号大小反映内存 I/O 吞吐量，VIMCAN 在设备端推理中展现出更高的计算效率。

### 消融实验

#### 变长训练策略（Table 3）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/008_Table_3.jpg]]
*Table 3: The ablation study for variable-length training strategy using the ground-truth 2D inputs on TotalCapture testing set. T: Fixed lengths. V: Variable-length. P1: Average MPJPE (mm, lower is better)*

采用变长序列训练（V）在 TotalCapture 测试集上达到 **P1 18.9 mm**，接近固定长度 81 帧的结果（17.2 mm），验证了模型对变长输入的鲁棒性。这一特性对实际部署中视频长度不固定的场景至关重要。

#### 分组与骨架感知扫描（Table 4）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/009_Table_4.jpg]]
*Table 4: The ablation study for grouping and skeleton-aware scanning on TotalCapture testing set. #G: Number of groups for body parts. Skel.: Whether to use a skeleton-aware scanning schema or not. P1: Average MPJPE. #Params.: Number of parameters. Peak: Peak Memory (MB)*

消融实验验证了分组策略和骨架感知扫描的有效性：

- 分组数 #G 从 1 增至 5，P1 逐步降低，验证了按身体部位分组的合理性。
- 骨架感知扫描（Skel.）的引入进一步降低了 P1，同时参数量和峰值内存基本不变，说明该设计以零额外成本提升了时空建模质量。

#### 融合策略对比（Table 5）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/010_Table_5.jpg]]
*Table 5: The ablation study for fusion strategies on TotalCapture test set. M: Methods. PM: PoseMamba (vision-only) [10], SA: Self-Attention (vision-only with Self-Attention module), CM: Cross-Mamba (visual-inertial Mamba-based fusion), CA: Cross-Attention (visual-inertial fusion with Cross-Attention module). P1: Average MPJPE*

这是验证 VIMCAN 核心设计的关键消融：

- **纯视觉 PoseMamba**（Huang et al., AAAI 2025）：P1 26.9 mm。
- **纯视觉 Self-Attention 基线**（SA）：P1 26.9 mm。
- **Cross-Mamba 融合**（CM，基于 Mamba 的跨模态融合变体）：P1 18.0 mm。
- **Cross-Attention 融合**（CA，VIMCAN 采用）：**P1 17.2 mm**。

相比纯视觉 Self-Attention 基线，集成 IMU 并通过 Cross-Attention 融合将 MPJPE 降低了 **9.7 mm**，证明了跨模态空间推理的关键作用。Cross-Attention 相比 Cross-Mamba 也有 0.8 mm 的提升，表明在融合阶段使用注意力机制捕捉视觉-惯性空间对应关系优于纯 Mamba 扫描。

#### 超参数敏感性（Table 6）

分组维度 $D_g$ 从 64 增大到 256，P1 从 36.7 mm 降至 31.2 mm，但参数量（3.0M → 7.3M）和计算量随之增加。作者在精度与效率之间选择了 $D_g=128$ 作为 VIMCAN-B 的平衡点。

### 失败模式与局限性

1. **传感器标定依赖**：方法要求 IMU 到人体骨段的旋转矩阵 $\mathbf{R}_B^I$ 预先精确测量（Eq. 11），限制了即插即用的部署灵活性。在标定不准确的场景下，性能可能显著下降。
2. **合成 IMU 的泛化差距**：3DPW 数据集使用合成 IMU 数据，无法完全模拟真实传感器的噪声和漂移特性，该基准上的结果需谨慎解读。
3. **极端遮挡场景**：论文未系统评估在严重遮挡（如多人交互、物体遮挡）下的鲁棒性，这是实际应用中的重要开放问题。

### 定性分析（Figure 6）

![[assets/figures/papers/paper_list_l1039_https_arxiv_org_abs_2605_07552/figures/011_Figure_6.jpg]]
*Figure 6: The qualitative analysis of VIMCAN. The green dashed lines denote the ground truth, and other colored lines represent the predictions*

Figure 6 展示了 VIMCAN 预测姿态与真值的对比，绿色虚线表示真值，其他颜色线条表示预测结果。在快速运动和自遮挡场景下，VIMCAN 的预测仍能紧密跟随真值，尤其在四肢末端关节的定位上表现出色，这得益于惯性传感器对快速运动的捕捉能力和 Cross-Attention 对空间依赖的精确建模。



## 定位与知识库关联

### 1. 方法定位与核心差异

VIMCAN 处于**视觉-惯性融合三维人体姿态估计**这一研究线，其直接对比的基线是 **Wang's GCN-Transformer**（Wang et al., Robotics Comput. Integr. Manuf. 2025），后者采用 GCN 与 Transformer 的混合架构进行多模态融合。两类方法的核心分歧在于对时序建模效率与多模态空间推理能力的权衡：

- **Wang's GCN-Transformer** 继承了 Transformer 的 Self-Attention 机制，在捕捉长程时序依赖时具有二次计算复杂度 $O(T^2)$，导致长序列推理时内存占用急剧膨胀。如 Figure 1 所示，当输入序列长度增至 243 帧时，该方法的峰值内存超过 3000 MB，而 VIMCAN 仅需约 600 MB，且内存 I/O 吞吐量更高（图中符号大小反映吞吐量）。

- **VIMCAN** 的因果旋钮在于：用时序线性复杂度的 Mamba（具体为 BiSTSSM 模块）替代 Transformer 进行高效序列建模，同时保留 Cross-Attention 进行跨模态空间依赖提取。这一“Mamba 管时间、Cross-Attention 管空间融合”的分工设计，使其在 TotalCapture 数据集上以 31.2 mm MPJPE（SimpleNet 2D 输入）显著优于 Wang's GCN-Transformer 的 34.9 mm（Table 7），同时参数量更低（7.3M vs 7.9M）。

与纯视觉 Mamba 方法 **PoseMamba**（Huang et al., AAAI 2025）相比，VIMCAN 的关键增量在于多模态融合策略。Table 5 的消融实验揭示了这一差异的因果链路：纯视觉 Self-Attention 基线（SA）的 MPJPE 为 26.9 mm；引入 IMU 并通过 Cross-Attention 融合后（CA），MPJPE 降至 17.2 mm，降幅达 9.7 mm。这表明 Cross-Attention 以视觉特征为 Query、IMU 特征为 Key/Value 的设计，有效利用了惯性传感对快速运动和遮挡的鲁棒性来校正视觉估计的歧义。

### 2. 设计空间的关键选择与消融证据

VIMCAN 的设计空间中有三个被消融实验验证的关键选择：

**（1）融合策略：Cross-Attention vs. Cross-Mamba。** 作者同时探索了纯 Mamba 风格的跨模态融合方案 Cross-Mamba（CM），其采用 Cross-SSM 沿空间轴拼接视觉与惯性特征后进行双向扫描（Figure 5）。Table 5 显示，Cross-Mamba 的 MPJPE 为 18.6 mm，虽优于纯视觉基线，但弱于 Cross-Attention 的 17.2 mm。这验证了核心洞察：Mamba 的线性扫描机制在捕捉跨模态的复杂空间依赖关系时能力不足，而 Cross-Attention 的全局感受野更适合此类细粒度空间推理。

**（2）数据扫描方式：骨架感知扫描。** VIMCAN 在视觉分支采用骨架感知的双向扫描，在惯性分支采用四向扫描。Table 4 的消融显示，移除骨架感知扫描后 MPJPE 从 17.2 mm 升至 18.2 mm，且峰值内存反而略增（从 1538 MB 升至 1556 MB），表明骨架拓扑先验不仅提升精度，还优化了扫描路径的计算效率。

**（3）分组策略。** 将 6 个 IMU 按人体部位划分为 5 组（躯干、左臂、右臂、左腿、右腿，Figure 3），使各组的时空特征提取更有针对性。Table 4 中分组数 #G 从 1（不分組）增至 5 时，MPJPE 持续下降，验证了部位感知设计的有效性。

### 3. 适用边界与局限

**适用场景：** VIMCAN 擅长处理长序列推理场景（如长时间运动捕捉），其线性复杂度在序列长度增加时优势愈发显著。变长训练策略（Table 3）使模型在变长输入下仅损失 1.7 mm MPJPE（17.2 mm → 18.9 mm），证明了对实际部署中非固定帧率输入的鲁棒性。

**关键局限：依赖严格传感器标定。** 方法要求预先精确测量 IMU 到人体骨段的旋转矩阵 $\mathbf{R}_B^I$（见 Eq. 11 的骨骼方向计算链：$\mathbf{R}_B^C = \mathbf{R}_B^I \cdot \mathbf{R}_I^S \cdot \mathbf{R}_S^G \cdot \mathbf{R}_G^C$），这限制了即插即用的部署灵活性。在 3DPW 数据集上使用合成 IMU 数据（Table 2）的实验设置也无法完全反映真实惯性传感器的噪声特性，该结果的泛化性需要手动验证。

**公平性注意：** 由于 Wang's GCN-Transformer 代码未公开，作者重新实现了该模型用于效率对比，参数规模与原始报告基本一致（7.3M vs 7.9M），但复现偏差可能影响对比的绝对精度。

### 4. 开放问题

1. **标定依赖性：** 如何开发自适应标定或在线标定技术，使 VIMCAN 类方法摆脱对预标定的依赖，实现真正的即插即用？
2. **极端场景鲁棒性：** 在更复杂的遮挡（如多人交互、手持物体遮挡 IMU 佩戴部位）和多样化运动（如极限运动、舞蹈旋转）下，混合 Mamba-Cross-Attention 架构的鲁棒性尚未被充分验证。
3. **IMU 数量与布局优化：** 当前 6 IMU 的布局是固定的，是否存在更优的传感器配置（如更少 IMU 或不同佩戴位置）能在精度与成本间取得更好平衡？这一方向尚未被系统探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/VIMCAN_Visual_Inertial_3D_Human_Pose_Estimation_with_Hybrid_Mamba_Cross_Attention_Network.pdf]]

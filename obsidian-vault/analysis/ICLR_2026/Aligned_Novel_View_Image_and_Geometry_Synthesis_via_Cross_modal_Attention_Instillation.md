---
title: Aligned Novel View Image and Geometry Synthesis via Cross-modal Attention Instillation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Aligned_Novel_View_Image_and_Geometry_Synthesis_via_Cross_modal_Attention_Instil_f3c511aaa3a8.pdf
project_link: "https://cvlab-kaist.github.io/MoAI/"
code_link: null
aliases:
- MCMAI
- ANVIGSCMAI
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 跨模态注意力注入（MoAI）将图像扩散分支的空间注意力图注入到并行的几何扩散分支中，使得几何修复受益于图像的语义感知能力，图像生成则通过几何修复的确定性结构约束获得正则化。同时，基于邻近性的网格条件化（proximity-based mesh conditioning）通过将稀疏点云转化为网格并引入深度/法线线索，滤除错误投影，增强对应条件的可靠性。
primary_logic: 图像生成与几何修复形成协同多任务学习：图像网络提供聚焦的语义注意力图，帮助几何网络捕获细粒度跨视角对应；几何网络的完成任务本身具有更强的结构确定性和稳健性，反过来为图像生成提供正则化，约束其生成过程，从而使两者天然对齐。
claims:
- 在 RealEstate10K 外推设置下，逐一添加点图条件、基于邻近性的网格条件化和跨模态注意力注入，PSNR 从 16.55 逐步提升至 17.41，验证各模块的增益。
- 在 DTU 零样本外推任务中，双视图设置下本方法 PSNR 达到 15.58，大幅优于最优基线 NoPoSplat (13.58)，证明强泛化能力。
- 跨模态注意力注入使几何去噪网络中原本发散的注意力（缺乏语义线索）变得聚焦，同时图像修复也因几何正则化而更一致，消融实验表明该设计是实现最高性能的关键。
- DTU 上 PSNR (extrapolative, 2-view) = 15.58
---

# Aligned Novel View Image and Geometry Synthesis via Cross-modal Attention Instillation

> [!tip] 核心洞察
> 图像生成与几何修复形成协同多任务学习：图像网络提供聚焦的语义注意力图，帮助几何网络捕获细粒度跨视角对应；几何网络的完成任务本身具有更强的结构确定性和稳健性，反过来为图像生成提供正则化，约束其生成过程，从而使两者天然对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于跨模态注意力注入的对齐新视角图像与几何合成 |
| 英文题名 | Aligned Novel View Image and Geometry Synthesis via Cross-modal Attention Instillation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vjvwYexMQn) · [Project](https://cvlab-kaist.github.io/MoAI/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoAI（Cross-modal Attention Instillation） |
| Dataset | DTU, RealEstate10K |

> [!tip] 效果简介
> - DTU 上，PSNR (extrapolative, 2-view) 15.58 vs 13.58 (NoPoSplat) (+2.00)。
> - RealEstate10K 上，PSNR (extrapolative, 2-view) 17.41 vs 14.36 (NoPoSplat) (+3.05)。
> - DTU (large model comparison) 上，PSNR (1-view) 15.56 vs 14.04 (ViewCrafter) (+1.52)。

## 概要

少样本新视角合成（Novel View Synthesis, NVS）在推理性场景下面临一个根本性矛盾：前馈式方法（如 **PixelSplat** (Charatan et al., 2024)、**MVSplat** (Chen et al., 2024)）依赖代价体或显式几何投影，在参考视角凸包内的插值区域表现良好，但无法合成未观测区域的内容；生成式方法（如 **LucidDreamer** (Chung et al., 2023)、**GenWarp** (Seo et al., 2024)）虽能通过变形-修复范式外推到新视角，却受限于训练域内的相机位姿分布，且缺乏显式几何对齐机制，导致生成的图像与底层三维几何失配。大模型方法（如 **ViewCrafter** (Yu et al., 2024)）虽展现出一定的外推能力，但推理时间长、几何一致性弱，难以满足实际应用需求。

本文提出 **MoAI（Cross-modal Attention Instillation）**，一种基于扩散模型的变形-修复框架，首次将图像生成与几何修复统一为协同多任务学习范式。其核心调控机制是**跨模态注意力注入**：在并行运行的图像扩散分支与几何扩散分支之间，将图像分支的空间注意力图注入几何分支，使几何修复受益于图像的语义感知能力，同时图像生成通过几何修复的确定性结构约束获得正则化。此外，**基于邻近性的网格条件化**将稀疏点云转化为网格表示，引入深度图、法线图及法线掩码作为附加条件，滤除错误投影，增强对应条件的可靠性。

在 DTU 零样本外推设置下，MoAI 在双视图条件下达到 **15.58 PSNR**，较最优基线 NoPoSplat (13.58) 提升 **+2.00 dB**；在 RealEstate10K 域内外推设置下达到 **17.41 PSNR**，较 NoPoSplat (14.36) 提升 **+3.05 dB**。消融实验证实，逐一添加点图条件、网格条件化和跨模态注意力注入，PSNR 从 16.55 逐步提升至 17.41，各模块均带来持续增益。模型对几何条件的噪声和稀疏性高度鲁棒，在 80% 点掩码或 15% 高斯噪声下仍保持稳定性能。

新视角合成（Novel View Synthesis, NVS）旨在从稀疏的参考图像中生成任意目标视角下的场景外观。近年来，前馈式方法（如 **PixelSplat** (Charatan et al., 2024)、**MVSplat** (Chen et al., 2024)）通过端到端可微渲染取得了显著进展，但其本质依赖从参考视角到目标视角的可投影区域，无法合成未观测区域（即外推场景）的内容。另一方面，基于生成式先验的变形-修复（warping-and-inpainting）方法（如 **LucidDreamer** (Chung et al., 2023)、**GenWarp** (Seo et al., 2024)）虽能对外推区域进行合理填充，却面临两个核心瓶颈：其一，生成过程仅作用于图像域，缺乏显式的几何约束，导致生成图像与场景几何失配；其二，修复过程仅依赖2D语义线索，在大幅视点变化和几何噪声下容易产生不一致的结构。

这一困境揭示了当前少样本NVS领域的一个根本矛盾：**前馈方法受限于可投影区域，无法外推；生成式方法虽能外推，却缺乏几何对齐机制，难以保证图像与几何的一致性。** 更具体地，现有变形-修复框架将几何预测与图像生成解耦为两个独立步骤——先由现成几何模型（如 **DUSt3R** (Wang et al., 2024)）预测稀疏点云并投影，再对投影结果进行图像修复。这种串行范式使得图像生成无法感知几何修复中的不确定性，而几何预测也无法受益于图像的语义理解能力，最终导致两模态之间的系统性失配。

此外，现有生成式NVS方法在输入条件上存在脆弱性：仅依赖投影点图作为对应条件，容易引入错误投影（如遮挡边界的拖影），且缺乏对几何可靠性的显式建模。大模型NVS方法（如 **LVSM** (Jin et al., 2024)、**ViewCrafter** (Yu et al., 2024)）虽凭借海量数据训练获得了强泛化能力，但其推理耗时较长，且同样未从根本上解决图像-几何对齐问题。

针对上述缺口，本文提出 **MoAI（Cross-modal Attention Instillation）**，一种基于扩散模型的联合图像-几何生成框架。核心动机在于：**让图像生成与几何修复形成协同多任务学习——图像网络提供聚焦的语义注意力图，帮助几何网络捕获细粒度跨视角对应；几何网络的完成任务本身具有更强的结构确定性，反过来为图像生成提供正则化，约束其生成过程，从而使两者天然对齐。** 同时，通过基于邻近性的网格条件化（proximity-based mesh conditioning）滤除错误投影，增强对应条件的可靠性。这一设计使得MoAI在无位姿设定下，既能实现推理性外推，又能保证生成图像与几何的严格一致。

## 核心方法与创新机理

MoAI 的核心创新在于将新视角合成（NVS）从“图像生成”或“几何预测”的单一范式，重新构建为**图像与几何的协同多任务扩散框架**，并通过**跨模态注意力注入**实现两者的内在对齐。以下从三个关键维度拆解相对现有基线的根本性改变。

### 1. 任务范式：从单模态生成到图像-几何联合扩散

现有方法在 NVS 中通常将图像生成与几何估计解耦：前馈式方法（如 **PixelSplat** (Charatan et al., 2024)、**MVSplat** (Chen et al., 2024)）直接回归图像，缺乏对未观测区域的显式几何推理；变形-修复方法（如 **LucidDreamer** (Chung et al., 2023)、**GenWarp** (Seo et al., 2024)）仅依赖 2D 修复，难以处理大幅视点变化和几何噪声。大模型方法（如 **ViewCrafter** (Yu et al., 2024)、**LVSM** (Jin et al., 2024)）虽能外推，但缺乏显式的几何对齐机制。

MoAI 的根本性改变在于：将变形-修复策略**从图像域推广到几何域**，在目标视角同时完成图像修复和几何修复。具体而言，系统从无位姿参考图像出发，利用现成的几何预测器（VGGT, Wang et al., 2024/2025）获得稀疏点云，将其投影到目标视角后，通过扩散模型对图像和几何的缺失区域进行联合修复。这一范式转换使得图像生成与几何修复天然耦合，而非事后对齐。

### 2. 核心机制：跨模态注意力注入（MoAI）

这是本方法最关键的创新点。在并行运行的图像扩散 U-Net 和几何扩散 U-Net 中，MoAI **将图像分支的空间注意力图注入到几何分支中**，替代几何网络原本独立的注意力计算。数学上，几何分支的注意力操作变为：

$$\mathrm{Attention}(Q^{I}, K^{I}, V^{P}) = \mathrm{softmax}\left({\frac{Q^{I} K^{I^{T}}}{\sqrt{d_{k}}}}\right) V^{P}$$

其中 $Q^{I}$、$K^{I}$ 来自图像分支，$V^{P}$ 来自几何分支。这一设计带来双重增益：

- **几何修复受益于图像语义**：图像网络的注意力图富含语义感知能力，能够聚焦于跨视角对应的关键区域。如 Figure 3 所示，几何网络原本的注意力呈发散分布（缺乏语义线索），注入后变得高度聚焦，帮助几何分支捕获细粒度的跨视角对应关系。
- **图像生成受几何正则化约束**：几何修复任务本身具有更强的结构确定性和稳健性，反过来为图像生成提供正则化，约束其生成过程，使图像与几何天然对齐。

消融实验（Table 3）表明，在 RealEstate10K 外推设置下，添加跨模态注意力注入使 PSNR 从 16.55（仅有点图条件）提升至 17.41（完整模型），是性能提升的最大贡献组件。

### 3. 条件表示：基于邻近性的网格条件化

传统变形-修复方法仅将投影点图作为条件信号，但稀疏点云的投影容易引入错误对应（如背景点错误投影到前景区域）。MoAI 提出**基于邻近性的网格条件化**，包含两个关键改进：

- **点云到网格的转换**：使用滚球算法（ball-pivoting algorithm, Bernardini et al., 1999）将稀疏点云转化为网格表示，从而获得连续的表面信息。
- **多线索条件与法线掩码**：在网格投影的基础上，附加深度图 $D$、法线图 $N$ 及法线掩码 $M$，构建增强的对应条件：

$$\mathbf{c^{t}} = [\mathcal{E}(X_{t}^{\mathrm{II}}), D_{t}^{\mathrm{II}}, N_{t}^{\mathrm{II}}, M_{t}], \quad \mathbf{c_{n}^{r}} = [\mathcal{E}(X_{n}), D_{n}, N_{n}, \mathbf{1}]$$

法线掩码通过排除法线方向与目标视角偏差超过 90° 的网格平面，有效滤除错误投影，增强对应条件的可靠性。消融实验（Table 3）证实，基于邻近性的网格条件化在点图条件基础上进一步带来显著增益。

### 创新总结

三个 changed slots 形成递进关系：**任务范式**从单模态转向联合扩散奠定框架基础；**跨模态注意力注入**作为核心机制实现图像与几何的内在对齐；**网格条件化**提升输入条件的可靠性，为对齐提供更稳健的几何先验。三者协同使得 MoAI 在零样本外推（DTU 双视图 PSNR 15.58 vs. NoPoSplat 13.58）和域内外推（RealEstate10K PSNR 17.41 vs. NoPoSplat 14.36）任务上均取得显著领先，同时展现出对几何噪声和稀疏性的高度鲁棒性（Table 5-6, Figure 10-11）。

MoAI 采用**变形-修复（warping-and-inpainting）**范式，将其从单图像域同时扩展到多视图图像域与几何域，构建了一个**图像与几何联合生成的扩散框架**。整体 pipeline 由三个核心阶段串联而成：现成几何预测 → 对应条件构建 → 双分支扩散修复。

### 输入输出流

**输入**为一组无位姿（unposed）的稀疏参考图像 $\{I_n \in \mathbb{R}^{H \times W \times 3}\}_{n=1}^{N}$ 以及目标相机位姿 $\pi_t$。**输出**为目标视角下的完整 RGB 图像 $\hat{I}_t$ 与对应的稠密点图 $\hat{P}_t$，二者通过跨模态注意力机制天然对齐。

### 阶段一：现成几何预测

利用现成的几何预测模型 **VGGT**（Wang et al., 2024; 2025）从每张参考图像 $I_n$ 预测其点图 $P_n$ 与相机位姿。所有参考点图被合并为统一点云 $P = \bigcup_{n=1}^{N} P_n$，再通过投影操作得到目标视角下的投影点图：

$$P_{t}^{\Pi} = \Pi(P, \pi_{t})$$

该投影点图仅包含参考视角可见区域的几何信息，目标视角下被遮挡或未观测的区域呈现为空洞，为后续几何修复提供初始条件。

### 阶段二：对应条件构建

将投影点图 $P_t^{\Pi}$ 与各参考点图 $P_n$ 分别编码为对应条件。目标条件 $\mathbf{c}^t$ 与参考条件集 $\mathbf{c}^r$ 通过傅里叶特征编码与可见性掩码组合而成：

$$\mathbf{c}^{t} = [\mathcal{E}(P_{t}^{\Pi}), M_{t}], \quad \mathbf{c}_{n}^{r} = [\mathcal{E}(P_{n}), \mathbf{1}], \quad \mathbf{c}^{r} = \{\mathbf{c}_{n}^{r}\}_{n=1}^{N}$$

掩码 $M_t$ 标记投影点图中的有效区域，$\mathbf{1}$ 表示参考点图完全可见。这一条件设计为后续扩散网络提供了显式的跨视角几何对应线索。

### 阶段三：双分支扩散修复

框架核心由两个并行的扩散 U-Net 组成（Figure 1, Figure 2）：

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_vjvwYexMQn/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our diffusion-based framework. From one or more unposed reference images, we predict a partial colored point cloud and project it to the target view. Our diffusion model then inpaints missing regions with the cross-Modal Attention Instillation (MoAI), ensuring alignment between image and geometry, resulting in a complete 3D scene*

- **图像去噪分支**：图像参考网络从参考图像提取语义特征，图像去噪 U-Net 通过**聚合空间注意力**机制（Eq 6）跨所有参考图像与目标条件进行特征聚合，生成新视角 RGB 图像。
- **几何去噪分支**：几何参考网络从参考点图提取几何特征，几何去噪 U-Net 以投影点图为条件，对目标视角下未观测区域进行几何修复，生成完整的目标点图。

两个分支的关键连接在于**跨模态注意力注入（MoAI）**：在几何去噪 U-Net 的空间注意力层中，原始几何注意力图被替换为图像分支对应层的空间注意力图。具体而言，使用图像分支的查询 $Q^I$ 与键 $K^I$，但将值替换为几何分支的值 $V^P$：

$$\mathrm{Attention}(Q^{I}, K^{I}, V^{P}) = \mathrm{softmax}\left(\frac{Q^{I} K^{I^{T}}}{\sqrt{d_{k}}}\right) V^{P}$$

这一设计使几何修复受益于图像网络的语义感知能力，而图像生成则通过几何修复的确定性结构约束获得正则化，两者形成协同多任务学习，天然保证了图像与几何的对齐。

### 基于邻近性的网格条件化

为增强对应条件的可靠性，框架引入**基于邻近性的网格条件化**（proximity-based mesh conditioning）。使用球旋转算法（ball-pivoting algorithm, Bernardini et al., 1999）将稀疏点云转化为网格表示，投影后获得网格投影点图 $X_t^{\Pi}$ 及其深度图 $D_t^{\Pi}$、法线图 $N_t^{\Pi}$。最终的条件向量扩展为：

$$\mathbf{c^{t}} = [\mathcal{E}(X_{t}^{\Pi}), D_{t}^{\Pi}, N_{t}^{\Pi}, M_{t}], \quad \mathbf{c_{n}^{r}} = [\mathcal{E}(X_{n}), D_{n}, N_{n}, \mathbf{1}]$$

同时应用法线掩码，剔除法线方向与目标视角方向偏差超过 90° 的网格面片，有效滤除错误投影，提升外推场景下的条件质量。

MoAI 框架围绕三个核心模块构建：**图像-几何双分支扩散架构**、**跨模态注意力注入（MoAI）** 和 **基于邻近性的网格条件化**。以下逐一展开其设计逻辑与关键公式。

### 1. 图像-几何双分支扩散架构

框架接收 $N$ 张无位姿参考图像 $\{ I_n \in \mathbb{R}^{H \times W \times 3} \}_{n=1}^{N}$，首先通过现成的几何预测模型 **VGGT**（Wang et al., 2024; 2025）获得每张参考图像的点图 $P_n$ 和相机位姿，形成部分彩色点云。将合并后的参考点云 $P = \bigcup_{n=1}^{N} P_n$ 投影到目标视角 $\pi_t$，得到投影点图：

$$P_{t}^{\Pi} = \Pi(P, \pi_{t})$$

**瓶颈**：投影点图 $P_t^{\Pi}$ 仅包含参考视角可见区域的几何信息，目标视角中的未观测区域（外推场景尤为严重）存在大面积空洞，需要扩散模型进行修复。

基于此，构建目标视角与参考视角的对应条件：

$$\mathbf{c}^{\mathbf{t}} = [\mathcal{E}(P_{t}^{\Pi}), M_{t}], \quad \mathbf{c}_{n}^{\mathbf{r}} = [\mathcal{E}(P_{n}), \mathbf{1}], \quad \mathbf{c}^{\mathbf{r}} = \{\mathbf{c}_{n}^{\mathbf{r}}\}_{n=1}^{N}$$

其中 $\mathcal{E}(\cdot)$ 为傅里叶特征编码，$M_t$ 为投影掩码（标记有效投影区域），参考条件 $\mathbf{c}_n^{\mathbf{r}}$ 使用全1掩码表示完全已知。图像去噪 U-Net 和几何去噪 U-Net 分别以这些条件为输入，并行执行图像生成与几何修复。

图像去噪网络中的聚合空间注意力机制将目标特征与所有参考特征联合建模：

$$\mathrm{Attention}(Q^{I}, K^{I}, V^{I}) = \mathrm{Softmax}\left(\frac{Q^{I} K^{I^{T}}}{\sqrt{d_{k}}}\right) V^{I}$$

其中 $Q^I$ 为目标视角的图像查询特征，$K^I$ 和 $V^I$ 为拼接了所有参考图像和目标图像的空间键值特征。

### 2. 跨模态注意力注入（MoAI）

**因果机制**：在独立的双分支扩散中，几何去噪网络的注意力缺乏语义线索，注意力图呈发散分布（Figure 3 证实），难以捕获细粒度跨视角对应。MoAI 将图像分支的空间注意力图直接注入几何分支，使几何修复复用图像网络的语义感知能力：

$$\mathrm{Attention}(Q^{I}, K^{I}, V^{P}) = \mathrm{softmax}\left({\frac{Q^{I} K^{I^{T}}}{\sqrt{d_{k}}}}\right) V^{P}$$

**关键设计**：公式中使用图像分支的查询 $Q^I$ 和键 $K^I$ 计算注意力权重，但值 $V^P$ 来自几何分支。这意味着注意力分布由图像的语义特征驱动（何处需要关注），而实际聚合的信息来自几何特征空间（关注什么内容）。这一设计在训练和推理阶段均执行，形成**协同多任务学习**：图像网络提供聚焦的语义注意力，几何网络受益于这种引导；反过来，几何修复的确定性结构约束又通过共享的注意力图正则化图像生成过程，使两者天然对齐。

消融实验（Table 3）表明，在 RealEstate10K 外推设置下，加入 MoAI 后 PSNR 从 17.10 提升至 17.41，是实现最高性能的关键组件。

### 3. 基于邻近性的网格条件化

**瓶颈**：直接使用投影点图 $P_t^{\Pi}$ 作为条件存在两个问题——稀疏点云在投影后可能产生错误对应（如背景点错误投影到前景区域），且缺乏显式的几何线索（深度、法线）来约束生成。

**解决方案**：首先使用滚球算法（Ball-Pivoting, Bernardini et al., 1999）将稀疏点云转化为网格表示，再投影得到网格投影点图 $X_t^{\mathrm{II}}$、深度图 $D_t^{\mathrm{II}}$ 和法线图 $N_t^{\mathrm{II}}$。通过法线掩码滤除网格面法线与目标视角方向偏差超过 90° 的错误投影。最终增强的对应条件为：

$$\mathbf{c^{t}} = [\mathcal{E}(X_{t}^{\mathrm{II}}), D_{t}^{\mathrm{II}}, N_{t}^{\mathrm{II}}, M_{t}], \quad \mathbf{c_{n}^{r}} = [\mathcal{E}(X_{n}), D_{n}, N_{n}, \mathbf{1}]$$

**因果机制**：网格表示通过邻近性隐式编码了三维结构的连续性约束，深度和法线线索为扩散模型提供了强几何先验，法线掩码则主动抑制了错误投影对生成过程的干扰。消融实验（Table 3）显示，从点图条件切换到网格条件化后，PSNR 从 16.55 提升至 17.10，验证了该模块的有效性。

## 实验与关键发现

### 核心定量结果

MoAI 在零样本外推与域内外推两个关键场景上均显著超越了现有方法，验证了跨模态注意力注入与基于邻近性网格条件化的协同效应。

在 **DTU 零样本外推** 设定（双视图）下，MoAI 的 PSNR 达到 **15.58**，较最优无位姿基线 **NoPoSplat**（Ye et al., 2024）的 13.58 提升 **+2.00 dB**（Table 1）。该设定对所有模型均为零样本，直接检验泛化能力。在单视图外推子设定中，MoAI 同样以 15.56 dB 的 PSNR 超越大模型基线 **ViewCrafter**（Yu et al., 2024）的 14.04 dB（Table 7），表明其以远小于大模型的参数量实现了更强的几何一致性生成。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_vjvwYexMQn/figures/014_Table_7.jpg]]
*Table 7: Comparison to large model baselines. We quantitatively compare our model against recent large-scale models*

在 **RealEstate10K 域内外推** 设定（双视图）下，MoAI 的 PSNR 达到 **17.41**，较 NoPoSplat 的 14.36 提升 **+3.05 dB**（Table 2）。该数据集上的大幅领先表明，即使在训练域内，前馈方法在视点大幅偏离参考视角时仍存在根本性能力瓶颈，而 MoAI 的变形-修复范式与几何正则化设计有效突破了这一限制。

### 消融实验：各模块的因果贡献

Table 3 的消融实验以 RealEstate10K 外推设置为平台，逐步添加各组件，揭示了清晰的因果链：

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_vjvwYexMQn/figures/010_Table_3.jpg]]
*Table 3: Ablation study. We demonstrate how each of our components contributes to enhanced performance in novel view synthesis*

1. **基础变形-修复**（无点图条件）：PSNR 16.55。仅依赖图像扩散修复，缺乏显式几何对应，性能最低。
2. **+ 点图条件**：PSNR 提升至 16.90。引入投影点图作为对应条件，为修复提供稀疏几何线索。
3. **+ 基于邻近性的网格条件化**：PSNR 进一步提升至 17.14。将稀疏点云转化为网格并附加深度图、法线图及法线掩码，滤除错误投影，增强条件的可靠性与密度。
4. **+ 跨模态注意力注入（MoAI）**：PSNR 达到最终的 17.41。图像分支的空间注意力图注入几何分支，使几何修复受益于语义感知能力，同时几何完成任务的确定性结构反向正则化图像生成，实现图像与几何的内在对齐。

该消融链表明：每个组件均带来 **非冗余的正向增益**，且 MoAI 注意力注入是达到最高性能的关键设计。定性消融（Figure 15）进一步显示，从朴素基线（空间不连贯）到点图条件化（深度感知改善），再到网格邻近条件化（伪影减少），最终到跨模态注意力注入（最高质量与一致性），各组件逐步解决了不同的失效模式。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_vjvwYexMQn/figures/021_Figure_15.jpg]]
*Figure 15: Ablation results. Qualitative ablation study across five Co3D scenes demonstrating progressive improvements from naive baseline (spatially incoherent), through pointmap conditioning (improved depth awareness), to mesh-based proximity conditioning (reduced artifacts), and finally cross-modal attention distillation (highest quality with superior consistency). Each component contributes essential capabilities that culminate in state-of-the-art performance with well-aligned modalities and enhanced realism*

### 几何鲁棒性分析

MoAI 对几何对应条件中的噪声和稀疏性表现出高度鲁棒性：

- **高斯噪声扰动**（Table 5）：在对应条件上施加高斯噪声后，性能仅出现轻微下降，模型仍能保持合理的生成质量。Figure 10 的可视化表明，即使预测几何存在显著噪声，MoAI 仍能输出几何一致的修复结果。
- **稀疏性鲁棒性**（Table 6, Figure 11）：当对几何对应条件施加高达 **80% 的点掩码**（即仅保留 20% 的几何点）时，模型性能保持稳定。这得益于网格条件化提供的连续表面表示以及图像注意力注入带来的语义补全能力。

此外，**相机空间点图归一化**（Figure 8, Appendix A.3）被证实是提升几何一致性的关键工程实践。消融显示，移除该归一化会导致边界模糊、几何对齐退化，表明归一化有效稳定了不同相机位姿下的几何表示尺度。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_vjvwYexMQn/figures/013_Figure_8.jpg]]
*Figure 8: Ablation on pointmap normalization. Ablation study comparing synthesis results with and without camera-space pointmap normalization. Normalization significantly improves geometric consistency, boundary sharpness, and geometric alignment with projected geometry*

### 输入视角数量分析

尽管 MoAI 仅在双视图设定下训练，其多视图聚合注意力机制使其在推理时可泛化至任意数量的参考图像。Table 4 和 Table 8（Co3D 数据集）的定量分析表明，随着参考视角数量增加，图像与几何生成性能 **持续提升**。Figure 18 的定性结果进一步显示，更多参考视角提供了更丰富的对应信息，使模型在外推区域生成更完整的几何结构和更一致的纹理。

### 大模型基线对比

Table 7 将 MoAI 与 **LVSM**（Jin et al., 2024）、**ViewCrafter**（Yu et al., 2024）等近期大模型 NVS 方法进行了定量对比。在 DTU 单视图设定下，MoAI 以 PSNR 15.56 超越 ViewCrafter 的 14.04，同时在推理时间上具有显著优势（Figure 7）。在 Navi 数据集上的定性对比（Figure 9）显示，MoAI 在保持几何一致性的同时，生成质量与大模型方法具有竞争力，验证了显式几何对齐相对于纯生成式方法的优势。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_vjvwYexMQn/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparison with large model-based NVS methods. Qualitative comparison of our method to previous approaches demonstrates our method’s superior capabilities in conducting geometrically coherent image novel view synthesis with relatively short inference time*

### 外推场景下的遮挡与光照处理

Figure 13 展示了 MoAI 在极端外推视角（目标相机与参考视角夹角超过 90 度）下的表现。模型不仅能够合理修复被遮挡区域的图像内容，还能处理光照变化和阴影效果，生成几何一致的新视角。这一能力源于几何分支为图像生成提供的确定性结构约束——即使语义信息不足，几何完成任务的稳健性仍能引导图像生成朝向物理上合理的解。

### 失败模式与局限

当前方法的一个潜在局限在于其对现成几何预测模型（如 **VGGT**）的依赖。若参考视角的几何预测质量较差（如纹理缺失区域或极端视角变化），投影点图和网格条件的可靠性将降低，可能影响外推和对齐性能。文中未对此进行专项消融，但 Table 5 和 Table 6 的鲁棒性实验间接表明，MoAI 对几何噪声和稀疏性具有相当程度的容忍度。在域外城市数据（Figure 12, MegaDepth, CityScapes）上的泛化结果进一步说明，即使几何预测模型的训练域与测试域不匹配，MoAI 仍能保持高保真度的新视角合成能力。

## 定位与知识库关联

### 1. 方法谱系：从变形-修复到跨模态对齐生成

MoAI 继承了“变形-修复”（warping-and-inpainting）范式，但对其进行了根本性的扩展和重构。传统变形-修复方法（如 **LucidDreamer**（Chung et al., 2023）、**GenWarp**（Seo et al., 2024））仅将参考图像变形到目标视角后进行2D修复，缺乏显式几何建模，难以处理大幅视点变化和几何噪声。MoAI 在两个关键维度上突破这一局限：

**（1）从图像域到几何域的范式推广。** MoAI 将变形-修复策略同时应用于图像和几何两个模态：在目标视角，不仅修复图像，还修复由现成模型（VGGT）预测的部分点云。这使方法天然具备生成对齐的 RGB-D 输出的能力，而非仅输出图像。

**（2）从单模态修复到跨模态协同。** 这是 MoAI 区别于所有现有方法的核心创新。传统方法中图像生成和几何预测是分离的，而 MoAI 通过跨模态注意力注入（Cross-Modal Attention Instillation）将二者耦合：图像扩散分支的空间注意力图被注入到并行的几何扩散分支中。其因果机制在于：
- 图像网络提供聚焦的语义注意力图，帮助几何网络捕获细粒度跨视角对应（Figure 3 显示，无注入时几何注意力发散，注入后变得聚焦）；
- 几何修复任务本身具有更强的结构确定性和稳健性，反过来为图像生成提供正则化，约束其生成过程。

这种双向协同使图像与几何天然对齐，无需后处理对齐步骤。

### 2. 与前馈式NVS方法的关系与边界

前馈式新视角合成方法（如 **PixelSplat**（Charatan et al., 2024）、**MVSplat**（Chen et al., 2024）、**NoPoSplat**（Ye et al., 2024））通过单次前向传播预测目标视角图像，速度快但存在根本性局限：它们只能合成参考视角中已观测到的内容，无法处理外推场景中未观测区域的生成。

MoAI 通过扩散模型的生成能力突破了这一边界。在 RealEstate10K 外推设置下，MoAI 的 PSNR 达到 17.41，显著优于 NoPoSplat 的 14.36（Table 2）。在 DTU 零样本外推任务中，双视图设置下 MoAI 的 PSNR 为 15.58，而 NoPoSplat 仅为 13.58（Table 1）。这些结果表明，MoAI 在推理性场景中具有前馈方法无法比拟的优势。

然而，MoAI 的扩散式生成也带来了推理速度的代价，这是当前方法的一个适用边界——在对实时性要求极高的场景中，前馈方法仍有其价值。

### 3. 与大模型NVS方法的关系

近期大模型NVS方法（如 **LVSM**（Jin et al., 2024）、**ViewCrafter**（Yu et al., 2024））通过大规模预训练获得了强大的生成先验，但通常缺乏显式几何对齐机制，且推理时间较长。MoAI 在 DTU 单视图设置下以 15.56 的 PSNR 优于 ViewCrafter 的 14.04（Table 7），同时推理时间更短（Figure 7 的定性对比也显示 MoAI 的几何一致性更优）。

MoAI 与大模型方法的关键区别在于：MoAI 通过显式的几何对应条件和跨模态注意力注入，将几何约束内嵌于生成过程中，而非依赖模型规模隐式学习几何一致性。这使得 MoAI 在相对紧凑的模型规模下即可实现强几何对齐。

### 4. 与无位姿三维重建方法的关系

MoAI 依赖现成几何预测模型（VGGT，Wang et al., 2024; 2025）提供初始点云和相机位姿，这与 **DUSt3R**（Wang et al., 2024）等无位姿重建方法形成互补。MoAI 的贡献不在于位姿估计本身，而在于：给定不完美的初始几何（可能包含噪声、稀疏和错误投影），如何生成对齐的图像和几何。

消融实验（Table 5, Table 6, Figure 10, Figure 11）表明，MoAI 对几何条件中的噪声和稀疏性高度鲁棒——在 80% 点掩码或 15% 高斯噪声下仍保持稳定性能。这意味着 MoAI 可以与不同质量的外部几何预测器配合使用，降低了对上游模块的精度要求。

### 5. 关键设计决策的消融验证

消融实验（Table 3）揭示了 MoAI 各组件的因果贡献链。在 RealEstate10K 外推设置下：
- 基础变形-修复基线：PSNR = 16.55
- 添加点图条件（pointmap conditioning）：PSNR 提升至 16.82
- 进一步添加基于邻近性的网格条件化（proximity-based mesh conditioning）：PSNR 提升至 17.12
- 最终添加跨模态注意力注入（MoAI）：PSNR 达到 17.41

基于邻近性的网格条件化（通过球旋转算法将稀疏点云转为网格，并附加深度图、法线图及法线掩码以滤除错误投影）是提升条件可靠性的关键设计。相机空间点图归一化（camera-space pointmap normalization）也被证明显著提升几何一致性和边界清晰度（Figure 8）。

### 6. 局限与开放问题

**对上游几何预测器的依赖。** MoAI 依赖现成的几何预测模型（VGGT）提供初始点云和相机位姿。若参考几何预测质量极差（例如在纹理缺失或重复纹理区域），可能影响外推和对齐性能。文中未对此进行系统讨论，但这是方法的一个固有依赖边界。

**推理效率。** 作为扩散式方法，MoAI 的推理速度慢于前馈方法，这限制了其在实时应用中的适用性。

**视角外推的极限。** 虽然 MoAI 在外推场景中表现优异，但文中未系统探索外推角度的极限——当目标视角与参考视角的差异极大（例如超过 120 度）时，生成质量如何退化仍是一个开放问题。

**域外泛化的边界。** Figure 12 展示了在城市数据（MegaDepth, CityScapes）上的泛化结果，但缺乏大规模域外定量评估。MoAI 在室内场景（RealEstate10K）训练后向室外场景迁移的性能边界尚需进一步验证。

**多模态对齐的度量。** 当前评估主要依赖图像质量指标（PSNR/SSIM/LPIPS），对几何对齐的评估仅通过可视化（Figure 14 使用 DepthAnything V3 进行对齐验证）。缺乏直接量化图像-几何对齐程度的指标，这限制了方法在精确对齐要求场景中的可信度。

## 原文 PDF

![[paperPDFs/ICLR_2026/Aligned_Novel_View_Image_and_Geometry_Synthesis_via_Cross_modal_Attention_Instil_f3c511aaa3a8.pdf]]

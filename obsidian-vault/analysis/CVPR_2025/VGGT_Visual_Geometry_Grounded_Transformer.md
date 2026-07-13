---
title: "VGGT: Visual Geometry Grounded Transformer"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/VGGT_Visual_Geometry_Grounded_Transformer.pdf
project_link: null
code_link: https://github.com/facebookresearch/vggt
aliases:
- VVGGT
- VGGT
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用大规模多任务训练，结合交替帧间与全局自注意力的Transformer架构，使模型能够从多视图图像中直接端到端地预测相机参数、深度图、点云图与点跟踪特征，无需任何后处理优化。
primary_logic: 即便Transformer缺乏显式的3D几何偏置，通过大规模多样的3D标注数据学习，配合交替注意力机制能够隐式捕捉多视图几何关系；多任务联合训练比单任务训练产生更精确的预测，且推理时将独立估计的深度与相机结合优于直接预测点云，从而实现快速、通用的3D重建。
claims:
- VGGT在前馈模式下显著超越依赖优化的方法（如DUSt3R+Global Align和MASt3R）在RealEstate10K和CO3Dv2上的相机姿态估计，同时速度极快。
- 多任务学习消融表明，同时训练相机、深度和跟踪估计显著提升点云精度。
- 交替注意力（Alternating-Attention）架构远优于仅全局自注意力和交叉注意力变体。
- VGGT的预训练特征作为CoTracker2的骨干，显著提升动态点跟踪性能。
---

# VGGT: Visual Geometry Grounded Transformer

> [!tip] 核心洞察
> 即便Transformer缺乏显式的3D几何偏置，通过大规模多样的3D标注数据学习，配合交替注意力机制能够隐式捕捉多视图几何关系；多任务联合训练比单任务训练产生更精确的预测，且推理时将独立估计的深度与相机结合优于直接预测点云，从而实现快速、通用的3D重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | VGGT：视觉几何扎根的Transformer |
| 英文题名 | VGGT: Visual Geometry Grounded Transformer |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.11651) · [Code](https://github.com/facebookresearch/vggt) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VGGT (Visual Geometry Grounded Transformer) |
| Dataset | RealEstate10K, CO3Dv2, DTU, ETH3D |

> [!tip] 效果简介
> - RealEstate10K 上，AUC@30 ↑ 85.3 vs 76.4 (+8.9)。
> - CO3Dv2 上，AUC@30 ↑ 88.2 vs 83.4 (+4.8)。
> - DTU (MVS) 上，Overall ↓ (Chamfer) 0.382 vs 1.741 (-1.359)。

## 概要

### 1. 问题背景与瓶颈

从多张二维图像恢复场景的三维几何结构——包括相机姿态、深度图和稠密点云——是计算机视觉的基础问题。现有主流方法大致分为两类：一类依赖**多阶段优化后处理**，如可微分束调整（Bundle Adjustment, BA），代表方法为**VGGSfM v2**（Wang et al., CVPR 2024）；另一类采用**前馈网络直接预测**，但通常仅支持两视图输入，需通过全局对齐等后处理融合多帧结果，代表方法为**DUSt3R**（Wang et al., CVPR 2024）和**MASt3R**（Leroy et al., arXiv 2024）。前者精度较高但推理缓慢，后者速度受限且无法一次性处理任意数量的视图并同时输出所有三维属性。核心瓶颈在于：**缺乏一种既能端到端前馈推理、又能从多视图联合预测全部三维属性的统一架构**。

### 2. 核心方法

**VGGT**（Visual Geometry Grounded Transformer）是一个大规模前馈Transformer，其核心设计理念是：**即便Transformer缺乏显式的三维几何偏置，通过大规模多样的三维标注数据学习，配合交替注意力机制，也能隐式捕捉多视图几何关系**。具体而言：

- **输入与输出**：接受一至数百张无序RGB图像，一次性端到端地预测每帧的相机参数（内外参）、深度图、点云图及三维点跟踪特征，无需任何后处理优化。
- **架构关键**：采用**交替注意力**（Alternating-Attention）机制——在24层Transformer中交替执行帧内自注意力和全局自注意力，使模型既能保持单帧内的空间连贯性，又能建立跨视图的几何对应关系。
- **多任务联合训练**：同时优化相机估计、深度估计、点云估计和点跟踪四个任务的损失函数，使各任务相互促进。

### 3. 主要结果与结论

VGGT在前馈模式下显著超越了依赖后处理的优化方法：

- **相机姿态估计**：在RealEstate10K上AUC@30达到**85.3**（对比MASt3R的76.4），在CO3Dv2上达到**88.2**（对比MASt3R的83.4），推理时间仅需**0.2秒**，而对比方法需约9秒（Table 1）。
- **多视图深度估计**：在DTU数据集上Overall Chamfer距离降至**0.382**，远优于DUSt3R的1.741（Table 2）。
- **点云估计**：在ETH3D上Overall指标为**0.677**，且从深度图与相机参数间接构建点云优于直接预测点云（Table 3）。
- **点跟踪与特征迁移**：VGGT的预训练特征作为CoTracker2的骨干网络，在TAP-Vid RGB-S上将$\delta_\text{avg}^\text{vis}$从78.9提升至**84.0**（Table 8）。

消融实验进一步证实：交替注意力架构远优于仅全局自注意力或交叉注意力变体（Table 5），且多任务联合训练比单任务训练产生更精确的点云估计（Table 6）。这些结果表明，**大规模数据驱动的前馈Transformer可以隐式学习多视图几何推理能力，在速度与精度上同时超越传统优化方法**。



从多张二维图像恢复场景的三维几何结构是计算机视觉的核心问题，其应用涵盖自动驾驶、机器人导航、增强现实与三维内容创作等领域。传统三维重建流程通常分为稀疏重建（Structure-from-Motion，SfM）与稠密重建（Multi-View Stereo，MVS）两个阶段，并高度依赖束调整（Bundle Adjustment，BA）等迭代优化后处理来消除累积误差。这类优化方法虽然精度较高，但计算开销大、推理耗时长，难以满足实时或大规模应用的需求。

近年来，前馈神经网络在三维重建领域取得了显著进展。以 **DUSt3R**（Wang et al., CVPR 2024）和 **MASt3R**（Leroy et al., arXiv 2024）为代表的方法，能够直接从图像对中预测点云图，避免了传统SfM的级联流程。然而，这些方法存在两个关键瓶颈：

1. **视图数量受限**：现有前馈方法的输入仅限于两两图像对，处理多视图场景时需要对所有图像对分别推理，再通过全局对齐（global alignment）等后处理步骤进行融合。这不仅增加了整体推理时间，还可能在融合过程中引入不一致性。
2. **输出维度单一**：这些方法仅输出点云图（或从点云图中后提取相机参数），无法在一次前馈推理中同时获得相机参数、深度图、点云图与点跟踪等多种三维属性。对于需要完整场景理解的下游任务而言，这种输出维度的局限意味着需要串联多个独立模型。

从更宏观的视角看，现有方法陷入了“前馈速度”与“优化精度”的权衡困境：纯前馈方法（如DUSt3R）速度快但精度受限，依赖优化的方法（如 **VGGSfM v2**，Wang et al., CVPR 2024）精度高但耗时长达数秒甚至数十秒。这一困境的根本原因在于，前馈模型缺乏对多视图几何关系的有效建模机制，而优化方法虽然显式地编码了几何约束，却牺牲了计算效率。

本文的核心动机在于打破上述权衡。作者观察到，即便Transformer架构本身缺乏显式的三维几何偏置，通过大规模、多样化的三维标注数据进行多任务联合训练，模型依然能够隐式地捕捉多视图之间的几何对应关系。基于这一洞察，VGGT被设计为一个通用的前馈三维感知模型，旨在以单次推理、无需任何后处理的方式，从任意数量的输入视图中同时预测相机参数、深度图、点云图与点跟踪特征，从而实现速度与精度的双重突破。



## 核心方法与创新机理

VGGT的核心创新在于将3D重建从**多阶段优化范式**彻底转向**单次前馈预测范式**，同时将输出范围从单一几何量扩展为完整的3D场景属性集。其关键创新点可归纳为以下三个维度的突破。

### 1. 从两两视图到任意多视图的联合推理

现有前馈方法如 **DUSt3R**（Wang et al., CVPR 2024）和 **MASt3R**（Leroy et al., arXiv 2024）采用共享权重的两两图像对处理策略，多视图场景需通过事后融合或全局对齐获得一致重建。VGGT将输入槽位从“图像对”改为“任意数量视图的联合序列”，通过分块化（DINO Tokenizer）和交替注意力机制，使Transformer能够一次性感知所有视图间的全局几何关系，从根本上消除了对后处理对齐的依赖。

### 2. 从单一输出到多任务联合预测

VGGT的输出范围从仅预测点云图（或从中后提取相机）扩展为**同时预测四类3D属性**：相机参数 $\mathbf{g}_i$（含四元数、平移、视场角）、深度图 $D_i$、点云图 $P_i$ 和跟踪特征 $T_i$（见公式1）。这一设计的关键洞察在于：**多任务联合训练产生比单任务训练更精确的预测**（Table 6消融实验证实，同时训练相机、深度和跟踪估计显著提升点云精度）。推理时，将独立估计的深度与相机参数结合构建点云（Depth + Cam路径），优于直接预测点云（Point路径），如ETH3D上Overall指标0.677 vs. 直接点云预测的更优表现（Table 3）。

### 3. 交替注意力机制替代显式几何偏置

VGGT的架构创新体现在**交替注意力（Alternating-Attention）** 设计上：24层Transformer交替执行帧内自注意力（每帧token独立交互，捕捉局部几何）和全局自注意力（跨帧token联合交互，捕捉多视图对应关系）。该设计**不引入任何显式3D几何偏置**（如极线约束、投影模型），而是依赖大规模3D标注数据驱动模型隐式学习多视图几何。Table 5的消融实验提供了决定性证据：交替注意力架构的Overall误差为0.709，远优于仅全局自注意力（0.827）和交叉注意力变体（1.061），证明交替模式是多视图几何推理的关键结构瓶颈。

### 创新本质的因果解读

VGGT的成功可归因于一个核心因果链条：**大规模多任务训练 × 交替注意力架构 → 隐式多视图几何捕获 → 端到端前馈3D重建**。即便Transformer缺乏显式几何偏置，通过海量多样的3D标注数据（训练需64张A100 GPU持续9天）配合交替注意力机制，模型学会在token交互中隐式编码相机位姿、深度一致性和跨视图对应关系。这一发现挑战了“3D视觉模型必须嵌入几何先验”的传统观念，为通用视觉几何模型开辟了新路径。



VGGT 的整体设计遵循一个简洁的前馈范式：输入任意数量的 RGB 图像，经过一个大型 Transformer 一次性端到端地输出每帧的相机参数、深度图、点云图和点跟踪特征，全程无需任何后处理优化。其核心映射函数为：

$$f \left( ( I _ { i } ) _ { i = 1 } ^ { N } \right) = ( \mathbf { g } _ { i } , D _ { i } , P _ { i } , T _ { i } ) _ { i = 1 } ^ { N }$$

其中 $\mathbf{g}_i = [\mathbf{q}, \mathbf{t}, f]$ 表示相机外参（四元数 $\mathbf{q}$ 和平移向量 $\mathbf{t}$）与内参（视场角 $f$），$D_i$ 为深度图，$P_i$ 为点云图，$T_i$ 为跟踪特征图。

整个 pipeline 由以下模块串联构成（参见 Figure 2）：

1. **图像分块（DINO Tokenizer）**：利用预训练的 DINOv2 将每张输入图像分块并转换为 token 序列，作为 Transformer 的初始表示。这一步为后续的跨视图信息交互提供了统一的视觉特征。

2. **相机 Token 与寄存器 Token 注入**：为每帧图像 token 序列追加可学习的相机 token $t_i^g$ 和寄存器 token $t_i^R$。相机 token 专门用于聚合该帧的相机参数信息，寄存器 token 则为全局注意力提供额外的存储空间。首帧与其他帧的相机 token 初始化方式有所区分，以建立坐标系基准。

3. **交替注意力 Transformer（24 层）**：这是 VGGT 架构的核心。模型交替执行**帧内自注意力**（每帧的 token 独立交互）与**全局自注意力**（所有帧的 token 联合交互），共 24 层，且不使用任何交叉注意力。这种设计使模型在缺乏显式 3D 几何偏置的情况下，依然能够隐式地捕捉多视图间的几何对应关系。消融实验（Table 5）证实，交替注意力架构在 ETH3D 上的 Overall 指标为 0.709，显著优于仅全局自注意力（0.827）和交叉注意力变体（1.061）。

4. **密集预测头（DPT + Conv）**：对 Transformer 输出的图像 token，采用 DPT（Dense Prediction Transformer）进行上采样，再通过 3×3 卷积层生成深度图 $D_i$、点云图 $P_i$ 和跟踪特征图 $T_i$。值得注意的是，推理时使用深度图与相机参数联合构造点云（Depth + Cam）优于直接预测点云（Point），这是实验中发现的关键设计选择（Table 3）。

5. **相机预测头**：从每帧的相机 token 直接回归相机外参和内参，输出 $\mathbf{g}_i$。

6. **跟踪模块（CoTracker2 架构）**：给定查询点，在查询帧的跟踪特征图上进行双线性采样获取查询特征，然后与所有其他帧的跟踪特征图进行相关性计算，再通过自注意力机制预测该查询点在所有图像中的对应 2D 坐标。

训练时，所有模块联合优化，总损失为多任务损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{depth}} + \mathcal{L}_{\mathrm{pmap}} + \lambda \mathcal{L}_{\mathrm{track}}$$

其中 $\lambda = 0.05$，$\mathcal{L}_{\mathrm{camera}}$ 为相机参数的 Huber 损失，$\mathcal{L}_{\mathrm{depth}}$ 为带异方差不确定度的深度损失（包含 L1 项和梯度项），$\mathcal{L}_{\mathrm{track}}$ 为所有查询点预测坐标与真实坐标的 L1 距离。

与现有方法的关键区别在于：**DUSt3R**（Wang et al., CVPR 2024）和 **MASt3R**（Leroy et al., arXiv 2024）仅支持两视图输入，需要将多视图拆分为两两图像对分别处理后，再通过全局对齐进行融合；而 VGGT 一次性接受全部视图，直接输出完整的 3D 属性，推理时间仅约 0.2 秒（10 帧），相比需要约 9 秒的基线方法快了两个数量级。

### 补充图表

![[assets/figures/papers/vggt_cvpr2025_quick/figures/001_Figure_1.jpg]]
*Figure 1: VGGT is a large feed-forward transformer with minimal 3D-inductive biases trained on a trove of 3D-annotated data. It accepts up to hundreds of images and predicts cameras, point maps, depth maps, and point tracks for all images at once in less than a second, which often outperforms optimization-based alternatives without further processing*



VGGT的核心是一个标准的大型Transformer，其关键设计在于**交替注意力（Alternating-Attention）架构**和多任务预测头。整个模型将任意数量的RGB图像映射为每帧的相机参数、深度图、点云图和跟踪特征，映射函数为：

$$f \left( ( I _ { i } ) _ { i = 1 } ^ { N } \right) = ( \mathbf { g } _ { i } , D _ { i } , P _ { i } , T _ { i } ) _ { i = 1 } ^ { N }$$

其中 $\mathbf{g}_i = [\mathbf{q}, \mathbf{t}, f]$ 表示相机姿态四元数、平移向量和视场角（Eq. (1), Sec. 3.1）。

### 交替注意力Transformer骨干

VGGT的Transformer骨干共 $L=24$ 层，**不包含任何交叉注意力层，仅使用自注意力**（Sec. 3.2）。其核心机制是交替执行两种自注意力：

- **帧内自注意力（Frame-wise Self-Attention）**：每帧的图像token $t_k^I$ 仅在各自帧内进行注意力计算，捕获单帧内部的几何线索。
- **全局自注意力（Global Self-Attention）**：所有帧的全部token $t^I$ 联合参与注意力计算，建立跨视图的对应关系。

这种交替设计使模型能够隐式地捕捉多视图几何关系，而无需显式的对极几何或三角测量偏置（Sec. 3.2, Fig. 2）。消融实验证实，交替注意力架构在ETH3D上的Overall指标为0.709，远优于仅全局自注意力（0.827）和交叉注意力变体（1.061）（Table 5）。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/002_Figure_2.jpg]]
*Figure 2: Architecture Overview. Our model first patchifies the input images into tokens by DINO, and appends camera tokens for camera prediction. It then alternates between frame-wise and global self attention layers. A camera head makes the final prediction for camera extrinsics and intrinsics, and a DPT [87] head for any dense output*

### 图像分块与Token增强

输入图像首先通过预训练的DINOv2进行分块（patchify），转换为图像token序列。在此基础上，模型为每帧添加两类可学习的辅助token（Sec. 3.3）：

- **相机Token** $t_i^g \in \mathbb{R}^{1 \times C'}$：每帧一个，用于聚合该帧的相机相关信息，最终输入相机预测头。
- **寄存器Token** $t_i^R \in \mathbb{R}^{4 \times C'}$：每帧四个，提供额外的存储空间以缓解注意力瓶颈。

### 多任务预测头

交替注意力层处理完毕后，模型通过三个并行的预测头输出所有3D属性（Sec. 3.3, Fig. 2）：

1. **相机预测头**：从相机token $t_i^g$ 直接回归相机内参和外参。
2. **密集预测头**：采用DPT（Dense Prediction Transformer）架构对图像token进行上采样，随后通过 $3\times3$ 卷积生成深度图 $D_i$、点云图 $P_i$ 和跟踪特征 $T_i$。
3. **跟踪模块**：采用CoTracker2架构，对查询点特征与所有帧的跟踪特征图进行相关运算，再通过自注意力预测查询点在所有图像中的对应2D坐标。

### 多任务训练损失

模型端到端训练，总损失为四项任务的加权和（Eq. (2), Sec. 3.4）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{depth}} + \mathcal{L}_{\mathrm{pmap}} + \lambda \mathcal{L}_{\mathrm{track}}$$

其中 $\lambda=0.05$，各项损失定义如下：

- **相机损失**：预测与真值相机参数之间的Huber损失，$\mathcal{L}_{\mathrm{camera}} = \sum_{i=1}^{N} \|\hat{\mathbf{g}}_i - \mathbf{g}_i\|_{\epsilon}$。
- **深度损失**：带异方差不确定度的深度损失，同时约束深度值和梯度，$\mathcal{L}_{\mathrm{depth}} = \sum_{i=1}^{N} \| \hat{\Sigma}_i^D \odot (\hat{D}_i - D_i) \| + \| \Sigma_i^D \odot (\nabla \hat{D}_i - \nabla D_i) \| - \alpha \log \Sigma_i^D$。
- **跟踪损失**：所有查询点在所有图像上的预测坐标与真值坐标的L1距离，$\mathcal{L}_{\mathrm{track}} = \sum_{j=1}^{M} \sum_{i=1}^{N} \| \mathbf{y}_{j,i} - \hat{\mathbf{y}}_{j,i} \|$。

多任务联合训练是VGGT性能的关键因素。消融实验表明，移除相机、深度或跟踪任一任务均导致点云估计精度下降，同时训练所有任务达到最优点云精度（Table 6）。

### 推理策略

值得注意的是，尽管理论上点云图 $P_i$ 可直接由密集预测头输出，但论文发现**将独立估计的深度图与相机参数结合来构建点云（Depth + Cam）优于直接预测点云**（Table 3）。这一策略利用了深度估计和相机估计各自的特化能力，在ETH3D上取得了更低的Overall误差（0.677 vs 直接点云头输出）。



## 实验与关键发现

### 相机姿态估计：前馈速度与优化级精度

VGGT 在 RealEstate10K 和 CO3Dv2 两个标准基准上评估多视图相机姿态估计，使用 10 帧随机采样输入。所有方法均未在 RealEstate10K 上训练，保证了泛化性对比的公平性。如 Table 1 所示，VGGT 以纯前馈模式取得 AUC@30 为 85.3 (Re10K) 和 88.2 (CO3Dv2)，显著超越需要后处理全局对齐的 **DUSt3R** (Wang et al., CVPR 2024) 和 **MASt3R** (Leroy et al., arXiv 2024)，以及可微分束调整方法 **VGGSfM v2** (Wang et al., CVPR 2024)。关键差距在于：VGGT 仅需 0.2 秒单次前馈推理，而对比方法耗时约 9 秒（含后处理），实现了近 45 倍加速同时精度领先 8.9 个百分点。在更具挑战的 IMC 数据集上，VGGT 的 AUC@10° 达 84.91，超越 CVPR 2024 IMC 挑战赛冠军 VGGSfM v2 的 76.82（Table 10），证明其在真实世界复杂光照与纹理下的鲁棒性。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/005_Table_1.jpg]]
*Table 1: Camera Pose Estimation on RealEstate10K [161] and CO3Dv2 [88] with 10 random frames. All metrics the higher the better. None of the methods were trained on the Re10K dataset. Runtime were measured using one H100 GPU. Methods marked with ‡ represent concurrent work*

![[assets/figures/papers/vggt_cvpr2025_quick/figures/016_Table_10.jpg]]
*Table 10: Camera Pose Estimation on IMC [54]. Our method achieves state-of-the-art performance on the challenging phototropism data, outperforming VGGSfMv2 [125] which ranked first on the latest CVPR’24 IMC Challenge in camera pose (rotation and translation) estimation*

### 多视图深度与点云估计：无需已知相机的端到端重建

在 DTU 多视图立体匹配基准上，VGGT 在不使用真实相机参数的方法中取得 Overall Chamfer 距离 0.382，大幅领先次优方法（1.741），且接近部分使用真实相机的方法（Table 2）。这一结果直接验证了 VGGT 联合估计相机与深度的有效性。在 ETH3D 点云估计任务中，VGGT 的“Depth + Cam”策略（从深度图与相机参数合成点云）取得 Overall 0.677，优于直接预测点云头（Ours Point）的 0.709，也优于依赖全局对齐的 DUSt3R（0.826）和 MASt3R（0.828），且推理速度远超后者（Table 3）。这表明将独立估计的深度与相机结合比直接回归点云更精确——模型隐式学习了多视图几何一致性，而非记忆点云坐标。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/008_Table_3.jpg]]
*Table 3: Point Map Estimation on ETH3D [97]. DUSt3R and MASt3R use global alignment while ours is feed-forward and, hence, much faster. The row Ours (Point) indicates the results using the point map head directly, while Ours (Depth + Cam) denotes constructing point clouds from the depth map head combined with the camera head*

![[assets/figures/papers/vggt_cvpr2025_quick/figures/007_Table_2.jpg]]
*Table 2: Dense MVS Estimation on the DTU [51] Dataset. Methods operating with known ground-truth camera are in the top part of the table, while the bottom part contains the methods that do not know the ground-truth camera*

### 双视图匹配与点跟踪：超越专用方法

尽管 VGGT 的跟踪模块未针对双视图匹配专门设计，其在 ScanNet-1500 双视图基准上取得 AUC@20 为 73.4，超越专用双视图匹配器 Roma（70.9）（Table 4）。这得益于多任务训练中跟踪特征学习到的强判别性。在动态点跟踪任务上，将 VGGT 预训练权重作为 **CoTracker2** 的骨干网络进行微调，在 TAP-Vid RGB-S 上将 δ_avg^vis 从 78.9 提升至 84.0（Table 8）。该结果揭示了 VGGT 特征的可迁移性：即便模型面向静态场景训练，其学到的几何感知表示仍能显著增强动态跟踪器的时序对应能力。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/014_Table_8.jpg]]
*Table 8: Dynamic Point Tracking Results on the TAP-Vid benchmarks. Although our model was not designed for dynamic scenes, simply fine-tuning CoTracker with our pretrained weights significantly enhances performance, demonstrating the robustness and effectiveness of our learned features*

![[assets/figures/papers/vggt_cvpr2025_quick/figures/006_Table_4.jpg]]
*Table 4: Two-View matching comparison on ScanNet-1500 [18, 92]. Although our tracking head is not specialized for the twoview setting, it outperforms the state-of-the-art two-view matching method Roma. Measured in AUC (higher is better)*

### 架构消融：交替注意力的决定性作用

Table 5 展示了 Transformer 骨干的消融结果。仅使用全局自注意力（无帧内注意力）时 Overall 升至 0.827，而使用交叉注意力变体更差至 1.061，相比之下交替注意力取得 0.709。这说明纯粹的全局自注意力无法有效捕捉帧内局部几何结构，而交叉注意力引入的归纳偏置反而破坏了多视图信息流。交替注意力通过帧内自注意力保留每帧的空间结构，再通过全局自注意力建立跨视图对应，形成了隐式的“特征匹配-几何推理”循环。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/010_Table_5.jpg]]
*Table 5: Ablation Study for Transformer Backbone on ETH3D. We compare our alternating-attention architecture against two variants: one using only global self-attention and another employing cross-attention*

### 多任务学习消融：联合训练优于单任务

Table 6 的多任务消融表明，同时训练相机、深度和跟踪三个任务时点云估计精度最高。移除任一任务均导致 ETH3D 上的 Overall 指标恶化。这验证了核心洞见：相机估计提供全局几何约束，深度估计提供局部表面信息，跟踪估计提供跨视图对应——三者形成互补监督信号，迫使 Transformer 学习更完整的场景几何表示。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/012_Table_6.jpg]]
*Table 6: Ablation Study for Multi-task Learning, which shows that simultaneous training with camera, depth and track estimation yields the highest accuracy in point map estimation on ETH3D*

### 推理效率与扩展性

Table 9 报告了不同输入帧数下的推理时间与 GPU 显存占用。在 H100 GPU 上，10 帧输入仅需 0.2 秒、约 8 GB 显存；200 帧时增至约 40 GB，达到当前硬件的实用上限。这一扩展性瓶颈源于 Transformer 全局自注意力的二次复杂度，但已覆盖大多数实际应用场景。

![[assets/figures/papers/vggt_cvpr2025_quick/figures/015_Table_9.jpg]]
*Table 9: Runtime and peak GPU memory usage across different numbers of input frames. Runtime is measured in seconds, and GPU memory usage is reported in gigabytes*

### 失败模式与局限

VGGT 主要面向静态场景设计，动态物体会破坏其相机与深度估计的一致性。训练未集成可微分束调整（因训练效率考虑），虽然后处理 BA 可进一步提升精度（如 Table 1 中 Ours + BA 的结果），但未实现端到端优化。此外，模型仅支持透视投影相机，无法处理鱼眼或全景图像；参数规模约 12 亿，训练需 64 张 A100 GPU 持续 9 天，计算成本高昂。在欠代表域或复杂场景下，泛化能力仍有待验证。

### 补充图表

![[assets/figures/papers/vggt_cvpr2025_quick/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of our predicted 3D points to DUSt3R on in-the-wild images. As shown in the top row, our method successfully predicts the geometric structure of an oil painting, while DUSt3R predicts a slightly distorted plane. In the second row, our method correctly recovers a 3D scene from two images with no overlap, while DUSt3R fails. The third row provides a challenging example with repeated textures, while our prediction is still high-quality. We do not include examples with more than 32 frames, as DUSt3R runs out of memory beyond this limit*



## 定位与知识库关联

### 与前馈多视图几何方法的关系

VGGT 可视为前馈多视图几何重建路线上的一个关键节点。其最直接的前驱是 **DUSt3R**（Wang et al., CVPR 2024）和 **MASt3R**（Leroy et al., arXiv 2024），二者首次展示了从图像对直接回归点云图的可行性，但存在两个结构性限制：① 仅支持两两视图输入，多视图场景需额外融合与全局对齐后处理；② 输出以点云图为主，相机参数需从中后提取，精度受限于该间接路径。VGGT 通过三个维度突破了这些限制：

- **输入范式**：将两两图像对扩展为任意数量视图的联合输入，通过交替注意力机制一次性处理所有帧，消除了对全局对齐或束调整（Bundle Adjustment）的依赖。
- **输出范围**：从单一的点云图扩展为同时预测相机参数、深度图、点云图和跟踪特征的四元输出，形成更完整的 3D 场景表征。
- **推理效率**：在保持前馈简洁性的前提下，将多视图推理时间压缩至 0.2 秒（RealEstate10K 上 10 帧），而 DUSt3R + Global Align 需约 9 秒（Table 1）。

在相机姿态估计这一核心任务上，VGGT 的前馈模式直接超越了需要后处理的 DUSt3R 和 MASt3R：RealEstate10K 上 AUC@30 达到 85.3（对比 MASt3R 76.4），CO3Dv2 上达到 88.2（对比 MASt3R 83.4）。值得注意的是，所有方法均未在 RealEstate10K 上训练，该对比具有跨域泛化意义。

### 与可微分束调整方法的关系

VGGT 与基于优化的方法（尤其是可微分束调整路线）形成互补而非替代关系。**VGGSfM v2**（Wang et al., CVPR 2024）代表了将 BA 嵌入学习管线的努力，在 IMC 挑战赛上曾排名第一。VGGT 的实验表明，其纯前馈预测已超越 VGGSfM v2（IMC 上 AUC@10° 84.91 vs 76.82，Table 10），且将 VGGT 的预测作为 BA 的初始解可进一步改善精度（Table 1 中 Ours + BA 行）。这说明前馈模型与优化方法存在“粗到精”的协作空间：前馈提供高质量初值，BA 进行局部精化。当前 VGGT 的训练未集成可微分 BA（因训练效率考量），如何高效地将 BA 融入前馈训练仍是一个开放问题。

### 架构设计的核心创新与消融支撑

VGGT 的架构选择并非偶然，而是经过消融验证的关键设计决策：

- **交替注意力（Alternating-Attention）**：在 ETH3D 点云估计上，交替注意力架构的 Overall 误差为 0.709，而仅全局自注意力变体为 0.827，交叉注意力变体为 1.061（Table 5）。帧内自注意力允许每帧独立建模局部几何，全局自注意力则建立跨视图对应，二者的交替执行使 Transformer 在缺乏显式 3D 偏置的情况下隐式习得多视图几何关系。
- **多任务联合训练**：消融实验表明，同时训练相机、深度和跟踪估计能显著提升点云精度（Table 6）。移除任一任务均导致性能下降，验证了多任务信号之间的相互正则化效应。
- **深度+相机组合优于直接点云预测**：在 ETH3D 上，从深度图和相机参数重建点云（Ours Depth + Cam）的 Overall 误差为 0.677，优于直接使用点云预测头（Ours Point 的 0.709，Table 3）。这表明将深度估计与相机估计解耦，再通过几何关系合成点云，比端到端直接回归点云更可靠——这一发现对前馈 3D 重建的设计空间具有指导意义。

### 适用边界与局限

VGGT 的能力边界由以下因素划定：

1. **静态场景假设**：模型主要针对刚性静态场景设计。自身的相机和深度估计可能受场景运动影响；对动态场景的泛化需要额外微调（如作为 CoTracker2 的骨干时需针对动态数据进行微调，Table 8）。
2. **相机模型限制**：仅支持透视投影相机模型（参数化为四元数、平移、视场角），未涵盖鱼眼、全景等特殊镜头类型。
3. **计算资源门槛**：模型参数约 12 亿，训练需 64 张 A100 GPU 持续 9 天；推理时受限于 GPU 显存（约 40 GB），最大可处理约 200 帧输入（Table 9）。这使得在资源受限环境下部署存在挑战。
4. **数据依赖**：依赖大规模 3D 标注数据进行训练，对欠代表域（under-represented domains）或复杂场景可能泛化不足。虽然 RealEstate10K 上的零样本结果展示了跨域能力，但极端域偏移下的行为尚未充分验证。

### 作为通用 3D 视觉骨干的潜力

VGGT 的特征展现出超越其设计任务的可迁移性。最显著的证据来自动态点跟踪：将 VGGT 的预训练权重作为 **CoTracker2** 的骨干初始化，在 TAP-Vid RGB-S 上 δ_avg^vis 从 78.9 提升至 84.0（Table 8）。这表明通过大规模 3D 多任务预训练学到的特征具有通用的场景几何理解能力，可能惠及更广泛的 3D 视觉下游任务（如 3D 物体检测、场景理解、新视图合成等）。Table 7 中新视图合成的初步结果也支持这一方向。

### 开放问题

基于上述分析，以下几个方向值得关注：

- **高效 BA 集成**：如何在不显著增加训练成本的前提下，将可微分束调整融入前馈训练管线，以同时保留前馈效率与优化精度？
- **模型轻量化**：能否通过知识蒸馏或架构压缩，将 12 亿参数模型缩减至可在消费级 GPU 上运行的规模？
- **动态场景扩展**：如何从静态场景的 3D 重建扩展到非刚性形变和通用动态场景，实现统一的时空 3D 理解？
- **非透视相机支持**：如何在不大幅改动架构的前提下，扩展对鱼眼、全景等非透视相机模型的支持？
- **弱监督与数据扩展**：能否在海量无标注互联网数据上进行弱监督或自监督训练，降低对 3D 标注的依赖？
- **下游任务迁移**：VGGT 特征作为通用 3D 骨干的潜力是否可推广到更多任务（如 3D 语义分割、物体姿态估计等）？



## 原文 PDF

![[paperPDFs/CVPR_2025/VGGT_Visual_Geometry_Grounded_Transformer.pdf]]

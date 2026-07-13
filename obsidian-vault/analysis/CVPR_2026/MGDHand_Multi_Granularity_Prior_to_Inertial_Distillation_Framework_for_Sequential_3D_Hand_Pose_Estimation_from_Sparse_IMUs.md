---
title: "MGDHand: Multi-Granularity Prior-to-Inertial Distillation Framework for Sequential 3D Hand Pose Estimation from Sparse IMUs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MGDHand_Multi_Granularity_Prior_to_Inertial_Distillation_Framework_for_Sequential_3D_Hand_Pose_Estimation_from_Sparse_IMUs.pdf
project_link: null
code_link: null
aliases:
- MGDHand
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将教师模型中的手部先验解耦为静态形状、动态姿态和时序运动三个互补粒度，并在对应语义空间中进行分层蒸馏（SSD、DPD、TMD），弥合稀疏到密集的映射差距。
primary_logic: 将教师模型的跨模态先验按形状-姿态-运动属性解耦，再通过多粒度蒸馏模块在匹配粒度上传递给学生，从而无需额外推理模态即可显著提升稀疏IMU下手部姿态估计的精度和时序稳定性。
claims:
- 在VIHand数据集上，使用7个IMU时，MGDHand的MPJPE为9.13 mm、MPVPE为10.46 mm，显著优于所有对比方法。
- 与采用粗粒度全局特征蒸馏的VIFNet-S相比，MGDHand将MPJPE降低33.3%（9.13mm vs 13.69mm），MPVPE降低36.7%（10.46mm vs 16.53mm）。
- 消融实验显示，去除动态姿态蒸馏（DPD）导致MPJPE增加35.7%、MPVPE增加32.9%，是影响最大的组件。
- 在7-IMU配置下，MGDHand较无蒸馏学生基线降低MPJPE 40.7%（15.4mm→9.13mm），降低MPVPE约39.0%（10.46mm vs 17.15mm）。
---

# MGDHand: Multi-Granularity Prior-to-Inertial Distillation Framework for Sequential 3D Hand Pose Estimation from Sparse IMUs

> [!tip] 核心洞察
> 将教师模型的跨模态先验按形状-姿态-运动属性解耦，再通过多粒度蒸馏模块在匹配粒度上传递给学生，从而无需额外推理模态即可显著提升稀疏IMU下手部姿态估计的精度和时序稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MGDHand：面向稀疏IMU的序列化3D手部姿态估计的多粒度先验-惯性蒸馏框架 |
| 英文题名 | MGDHand: Multi-Granularity Prior-to-Inertial Distillation Framework for Sequential 3D Hand Pose Estimation from Sparse IMUs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_MGDHand_Multi-Granularity_Prior-to-Inertial_Distillation_Framework_for_Sequential_3D_Hand_Pose_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MGDHand |
| Dataset | VIHand |

> [!tip] 效果简介
> - VIHand (7 IMUs) 上，MPJPE (↓) 9.13 mm vs 13.69 mm (VIFNet-S) (-4.56 mm (-33.3%))；MPVPE (↓) 10.46 mm vs 16.53 mm (VIFNet-S) (-6.07 mm (-36.7%))；MPJPE (↓) 9.13 mm vs 15.4 mm (no distill) (-6.27 mm (-40.7%))。

## 概要

从稀疏惯性测量单元（IMU）实时重建密集的3D手部姿态，是沉浸式交互与可穿戴计算的关键技术。然而，稀疏IMU仅能提供局部运动信号，与结构化的全局手部姿态之间存在显著的语义鸿沟与信息密度差异——从稀疏信号直接回归密集姿态本质上是一个高度模糊的逆问题。传统跨模态知识蒸馏方法通常将教师模型中的视觉或运动学先验以耦合的全局特征形式传递给学生，忽略了模态间细粒度的语义不匹配，导致学生模型在仅使用IMU推理时优化困难、精度受限。

针对上述瓶颈，本文提出**MGDHand**——一个多粒度先验-惯性蒸馏框架。其核心洞察是：将教师模型中的跨模态先验按**静态形状、动态姿态和时序运动**三个互补粒度进行解耦，再通过分层蒸馏将这些先验在匹配的语义空间上传递给学生模型，从而弥合稀疏到密集的映射差距。具体而言，MGDHand预训练一个MANO-IMU融合教师模型，通过形态学增强、一致性增强和惯性增强模块从统一表示中提取三类先验特征；随后，在仅使用IMU输入的学生模型上施加静态形状蒸馏（SSD）、动态姿态蒸馏（DPD）和时序运动蒸馏（TMD），使学生在不引入任何额外推理模态的前提下，吸收教师的结构化知识。

在VIHand数据集上的实验表明，MGDHand在7-IMU配置下取得了**9.13 mm MPJPE**和**10.46 mm MPVPE**，显著优于所有对比方法。相较于采用粗粒度全局特征蒸馏的**VIFNet-S**（Wang et al., ACM MM 2025），MPJPE降低**33.3%**（9.13 mm vs. 13.69 mm），MPVPE降低**36.7%**（10.46 mm vs. 16.53 mm）；相较于无蒸馏学生基线，MPJPE降低**40.7%**（9.13 mm vs. 15.4 mm）。消融实验进一步揭示，动态姿态蒸馏（DPD）是影响最大的组件——去除后MPJPE升高35.7%、MPVPE升高32.9%；静态形状蒸馏（SSD）主要影响顶点几何精度，去除后MPVPE升高20.3%；时序运动蒸馏（TMD）则提供一致但幅度较小的增益。这些结果验证了多粒度解耦蒸馏策略在稀疏IMU手部姿态估计任务中的有效性与组件协同性。

### 问题背景：稀疏IMU到密集手部姿态的映射鸿沟

3D手部姿态估计是人机交互、虚拟现实和具身智能中的基础任务。基于视觉的方案虽已取得显著进展，但其对光照、遮挡和视角变化的敏感性，以及对计算资源和隐私的较高要求，限制了在可穿戴场景下的部署。近年来，惯性测量单元（IMU）凭借其轻量、低功耗和隐私友好等特性，成为视觉方案的有力替代。然而，IMU仅能提供附着点处的局部加速度和角速度读数，从这些稀疏、局部的运动信号直接回归具有21个关节的高维手部姿态，本质上是一个高度欠定的病态映射问题。

如 Figure 1(a) 所示，稀疏IMU提供的局部运动信息与结构化全局手部姿态之间存在显著的**语义鸿沟**和**信息密度差异**——少量传感器读数需要推断出完整的手部骨架形变和表面几何，这使得直接从稀疏信号回归密集手部姿态面临严重的模糊性。

### 现有方法缺口：跨模态先验利用的粗粒度困境

为缓解上述模糊性，现有方法通常引入辅助模态（如视觉或MANO参数模型）作为训练时的监督信号或先验来源。其中，跨模态知识蒸馏（cross-modal knowledge distillation）是一种有前景的范式：在训练阶段利用多模态教师模型编码丰富的几何与运动学先验，然后将这些先验知识传递给仅依赖IMU的学生模型，从而在推理时无需额外模态即可提升估计精度。

然而，传统跨模态蒸馏方法存在一个关键局限：**教师模型中的先验知识以耦合形式传递**。例如，**VIFNet-S**（Wang et al., ACM MM 2025）采用粗粒度的全局特征蒸馏，将教师模型的多模态融合特征作为一个整体去约束学生模型。这种做法忽略了模态间的语义不匹配——MANO参数提供的静态手部形状先验、IMU信号蕴含的瞬时姿态信息、以及时序运动模式在语义属性上截然不同，将其混为一谈地蒸馏不仅会使学生模型难以聚焦于最关键的知识成分，还可能导致优化目标之间的冲突。

### 本文动机：多粒度解耦蒸馏

针对上述瓶颈，本文提出一个核心思路：**将教师模型中的跨模态先验按语义属性解耦为静态形状（static shape）、动态姿态（dynamic pose）和时序运动（temporal motion）三个互补粒度，并在各自匹配的语义空间中进行分层蒸馏**。这一策略的直觉在于：

- **静态形状先验**刻画手部固有的几何形态（如手指长度比例、手掌宽度），是相对稳定的个体属性，应在全局层面进行蒸馏；
- **动态姿态先验**反映每一帧的关节构型，是逐帧变化的，需要帧级对齐；
- **时序运动先验**编码相邻帧之间的运动连贯性，对缓解时序抖动和滞后至关重要。

通过这种“分而治之”的蒸馏策略，学生模型能够从不同维度吸收教师模型的结构化知识，弥合稀疏IMU信号到密集手部姿态之间的映射差距，同时保持推理时仅使用IMU的高效性。实验表明，该方案在7-IMU配置下较无蒸馏基线降低MPJPE **40.7%**（15.4 mm → 9.13 mm），较粗粒度全局特征蒸馏方法VIFNet-S降低MPJPE **33.3%**（13.69 mm → 9.13 mm），验证了多粒度解耦蒸馏的有效性。

## 核心方法与创新机理

MGDHand的核心创新在于**将教师模型中的跨模态手部先验解耦为静态形状、动态姿态和时序运动三个互补粒度，并在匹配语义空间中进行分层蒸馏**，从而弥合稀疏IMU信号到密集手部姿态之间的语义鸿沟。与现有方法相比，这一策略在三个关键维度上实现了根本性改变。

### 1. 教师先验利用方式：从耦合全局特征到多粒度解耦蒸馏

传统跨模态蒸馏方法（如**VIFNet-S**，Wang et al., ACM MM 2025）将教师模型中的先验知识以耦合的全局视觉特征形式传递给学生。这种方式忽略了稀疏IMU提供的局部运动信息与结构化全局手部姿态之间的模态语义不匹配，导致学生模型优化困难。

MGDHand则从根本上改变了这一范式：教师模型中的手部先验被解耦为**静态形状**（手部几何形态）、**动态姿态**（逐帧关节构型）和**时序运动**（运动速度与加速度）三个独立且互补的粒度。这三种先验通过SSD（静态形状蒸馏）、DPD（动态姿态蒸馏）和TMD（时序运动蒸馏）三个模块，在各自对应的语义空间中被分别传递给学生模型。定量结果表明，这一策略带来了显著收益：在VIHand数据集7-IMU配置下，MGDHand的MPJPE为9.13 mm，较VIFNet-S的13.69 mm降低33.3%；MPVPE为10.46 mm，较VIFNet-S的16.53 mm降低36.7%。

### 2. 特征解耦策略：从无显式解耦到增强型先验提取

基线方法通常不对特征进行显式解耦，而是将编码后的特征直接用于姿态回归。MGDHand则引入了三个专用的增强模块来实现细粒度先验提取：

- **形态学特定增强模块（MSEM）**：通过差分与交互操作增强MANO主导的形态学成分，提取静态形状先验特征 $\mathbf{Z}_{\mathcal{T}}^{\mathrm{sh}}$；
- **一致性增强模块（CEM）**：强调两种模态的共有成分，提取动态姿态先验特征 $\mathbf{Z}_{\mathcal{T}}^{\mathrm{po}}$；
- **惯性特定增强模块（ISEM）**：增强运动信息成分，提取时序运动先验特征 $\mathbf{Z}_{\mathcal{T}}^{\mathrm{tm}}$。

这三个模块均以教师模型的统一语义表示 $\mathbf{Z}$ 为引导，通过交叉注意力机制分别细化形态学分支和运动学分支特征，确保每种先验特征在语义上与其目标属性对齐。

消融实验验证了这一解耦策略的有效性：去除DPD（动态姿态蒸馏）导致MPJPE升高35.7%、MPVPE升高32.9%，是影响最大的组件；去除SSD（静态形状蒸馏）主要损害顶点几何精度，MPVPE升高20.3%；去除TMD（时序运动蒸馏）则带来较小但一致的性能下降（MPJPE升高5.7%，MPVPE升高2.7%）。这表明三种先验在重建过程中扮演着不同但互补的角色。

### 3. 学生模型训练：从纯重建损失到多粒度蒸馏联合优化

传统IMU-only学生模型仅依赖重建损失进行监督训练，缺乏对结构化手部先验的有效利用。MGDHand在重建损失基础上引入了多粒度蒸馏损失：

$$\mathcal{L}_{\mathrm{distill}} = \lambda_{\mathrm{sh}}\mathcal{L}_{ss} + \lambda_{\mathrm{po}}\mathcal{L}_{ps} + \lambda_{\mathrm{tm}}\mathcal{L}_{ts}$$

其中，$\mathcal{L}_{ss}$ 对齐全局形状特征，$\mathcal{L}_{ps}$ 逐帧对齐姿态特征，$\mathcal{L}_{ts}$ 逐帧对齐时序运动特征。这一联合优化方案使学生模型能够从形状、姿态和运动三个维度同时吸收教师先验，而无需引入任何额外的推理模态或计算开销。

整体而言，完整MGDistill方案在7-IMU配置下较无蒸馏学生基线降低MPJPE 40.7%（15.4 mm → 9.13 mm），降低MPVPE约39.0%（17.15 mm → 10.46 mm），充分证明了多粒度解耦蒸馏相较于耦合式特征蒸馏和纯重建训练的显著优势。

MGDHand 遵循 **两阶段训练范式**：先预训练一个融合 MANO 参数与 IMU 信号的多模态教师模型，再通过多粒度解耦蒸馏将教师中的先验知识迁移至仅依赖 IMU 的学生模型。推理时，学生模型仅以稀疏 IMU 序列作为输入，无需 MANO 标注或视觉模态，不引入额外计算开销。

### 教师模型：MANO-IMU 融合编码

教师模型 $\mathcal{T}$ 的核心目标是学习一个跨模态对齐的统一语义空间 $\mathbf{Z}$，使其同时编码手部的几何形态先验与运动学先验。为此，教师采用双流 DSTFormer 编码器分别处理 MANO 参数序列 $\mathbf{G}$ 和 IMU 信号序列 $\mathbf{I}$，提取形态学潜在特征 $\mathbf{F}_{\mathcal{T}}^{\mathrm{m}}$ 与运动学潜在特征 $\mathbf{F}_{\mathcal{T}}^{\mathrm{k}}$。随后，以 MANO 特征为查询对 IMU 特征执行残差交叉注意力（见 Eq. (1)），生成融合表示 $\widetilde{\mathbf{F}}_{\mathcal{T}}^{\mathrm{m}}$，并以此定义统一语义空间 $\mathbf{Z}$。

在统一表示 $\mathbf{Z}$ 的基础上，教师端通过三个增强模块将先验知识解耦为互补的三粒度表示：

- **形态学特定增强模块（MSEM）**：通过差分与哈达玛积运算增强 MANO 主导成分，提取 **静态形状先验** $\mathbf{Z}_{\mathcal{T}}^{\mathrm{sh}}$，刻画手部固有几何结构。
- **一致性增强模块（CEM）**：强调两模态共有成分，提取 **动态姿态先验** $\mathbf{Z}_{\mathcal{T}}^{\mathrm{po}}$，编码逐帧关节姿态。
- **惯性特定增强模块（ISEM）**：增强运动信息，提取 **时序运动先验** $\mathbf{Z}_{\mathcal{T}}^{\mathrm{tm}}$，建模速度与加速度等动态特性。

三个模块的输出分别送入对应的辅助回归头：形状头预测 MANO 形状参数 $\beta$，姿态头预测 MANO 姿态参数 $\theta$，时序头预测关节速度 $\mathbf{v}$ 与加速度 $\boldsymbol{\alpha}$。教师总损失 $\mathcal{L}_{\mathcal{T}}$ 由重建损失与三项辅助先验损失加权构成，确保解耦后的特征在各自语义粒度上具有判别力。

### 学生模型：IMU-only 编码与多粒度蒸馏

学生模型 $\mathcal{S}$ 仅接收 IMU 序列 $\mathbf{I}$，经投影头与 DSTFormer 编码器得到学生潜在表示 $\mathbf{F}_{\mathcal{S}}$。为使学生从教师的解耦先验中获益，学生端设置并行的解耦分支：

- **姿态分支**采用空间注意力模块 $\mathcal{A}_{\mathrm{po}}$，从 $\mathbf{F}_{\mathcal{S}}$ 中提取逐帧姿态特征 $\mathbf{Z}_{\mathcal{S}}^{\mathrm{po}}$。
- **时序分支**采用时序注意力模块 $\mathcal{A}_{\mathrm{tm}}$，提取运动特征 $\mathbf{Z}_{\mathcal{S}}^{\mathrm{tm}}$。
- **形状特征** $\mathbf{Z}_{\mathcal{S}}^{\mathrm{sh}}$ 则通过对 $\mathbf{F}_{\mathcal{S}}$ 进行全局池化获得。

### 多粒度解耦蒸馏（MGDistill）

MGDistill 方案包含三个蒸馏模块，分别对齐学生与教师在对应粒度上的归一化特征：

- **静态形状蒸馏（SSD）**：$\mathcal{L}_{ss} = \| \hat{\mathbf{Z}}_{\mathcal{S}}^{\mathrm{sh}} - \hat{\mathbf{Z}}_{\mathcal{T}}^{\mathrm{sh}} \|_2^2$，对齐全局形状特征。
- **动态姿态蒸馏（DPD）**：$\mathcal{L}_{ps} = \frac{1}{T}\sum_{t=1}^{T} \| \hat{\mathbf{Z}}_{\mathcal{S},t}^{\mathrm{po}} - \hat{\mathbf{Z}}_{\mathcal{T},t}^{\mathrm{po}} \|_2^2$，逐帧对齐姿态特征。
- **时序运动蒸馏（TMD）**：$\mathcal{L}_{ts} = \frac{1}{T}\sum_{t=1}^{T} \| \hat{\mathbf{Z}}_{\mathcal{S},t}^{\mathrm{tm}} - \hat{\mathbf{Z}}_{\mathcal{T},t}^{\mathrm{tm}} \|_2^2$，逐帧对齐运动特征。

总蒸馏损失为三者的加权组合：$\mathcal{L}_{\mathrm{distill}} = \lambda_{\mathrm{sh}}\mathcal{L}_{ss} + \lambda_{\mathrm{po}}\mathcal{L}_{ps} + \lambda_{\mathrm{tm}}\mathcal{L}_{ts}$。学生最终优化目标为重建损失与蒸馏损失之和：$\mathcal{L}_{\mathcal{S}} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{distill}}$。

### 推理流程

推理时仅需学生模型：IMU 序列经投影头与 DSTFormer 编码后，由姿态分支与形状池化分别输出 MANO 姿态参数 $\theta$ 和形状参数 $\beta$，再通过 MANO 解码器恢复 3D 手部关节与网格顶点。整个过程无需求助教师模型或任何额外模态，保持了与纯 IMU 方法相同的推理效率。

Figure 2 展示了上述框架的完整数据流：教师端双流编码→统一表示→三模块解耦→辅助头监督；学生端单流编码→并行解耦分支→三粒度蒸馏损失对齐；最终由 MANO 解码器输出密集手部姿态。

![[assets/figures/papers/paper_list_l977_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MGDHand_Multi_Gra/figures/002_Figure_2.jpg]]
*Figure 2: The overview of the multi-granularity prior-to-inertial distillation framework. A MANO-IMU fusion teacher model is pre-trained using both MANO sequences and IMU signals to learn a cross-modal aligned latent manifold that explicitly relates inertial dynamic information to the hand model MANO parameter space. An IMU-only student model is trained under multi-granularity decoupled distillation to absorb static shape priors, dynamic pose priors and temporal motion priors from the teacher, while only using IMUs at inference time*

### 3.1 多模态融合教师模型中的统一语义空间

MGDHand 的核心设计起点是预训练一个 **MANO-IMU 融合教师模型**，使其在跨模态对齐的潜在流形中显式关联惯性动态信息与手部模型 MANO 参数空间。教师模型采用双流 DSTFormer 编码器，分别从 MANO 参数序列 $G$ 和 IMU 信号序列 $I$ 中提取形态学潜在特征 $\mathbf{F}_{\mathcal{T}}^{\mathrm{m}}$ 和运动学潜在特征 $\mathbf{F}_{\mathcal{T}}^{\mathrm{k}}$。

为建立统一的跨模态语义空间，教师模型以 MANO 特征为查询，对 IMU 特征执行残差交叉注意力，生成融合表示 $\widetilde{\mathbf{F}}_{\mathcal{T}}^{\mathrm{m}}$：

$$
\widetilde{\mathbf{F}}_{\mathcal{T}}^{\mathrm{m}} = \mathbf{F}_{\mathcal{T}}^{\mathrm{m}} + \mathrm{softmax}\left(\frac{(\mathbf{F}_{\mathcal{T}}^{\mathrm{m}}W_Q^{m})(\mathbf{F}_{\mathcal{T}}^{\mathbf{k}}W_K^{k})^{\top}}{\sqrt{d_k}}\right)(\mathbf{F}_{\mathcal{T}}^{\mathbf{k}}W_V^{k})
$$

该融合表示经过多层感知机投影后，定义了统一语义空间中的潜在向量 $\mathbf{Z}$。这一设计使教师模型能够在单一表示中同时编码几何形态先验和运动学先验，为后续的多粒度解耦蒸馏奠定基础。

### 3.2 特征解耦模块：MSEM、CEM 与 ISEM

教师模型获得统一表示 $\mathbf{Z}$ 后，MGDHand 通过三个专用的增强模块将耦合的跨模态知识解耦为静态形状、动态姿态和时序运动三种互补先验。具体而言，首先以 $\mathbf{Z}$ 为查询，对形态学分支和运动学分支分别执行 $\mathbf{Z}$ 引导的交叉注意力，得到精炼特征 $\widehat{\mathbf{F}}_{\mathcal{T}}^{m}$ 和 $\widehat{\mathbf{F}}_{\mathcal{T}}^{k}$：

$$
\widehat{\mathbf{F}}_{\mathcal{T}}^{m} = \mathrm{softmax}\left(\frac{(\mathbf{Z}W_Q)(\mathbf{F}_{\mathcal{T}}^{m}W_K^m)^\top}{\sqrt{d_k}}\right)(\mathbf{F}_{\mathcal{T}}^{m}W_V^m)
$$

$$
\widehat{\mathbf{F}}_{\mathcal{T}}^{k} = \mathrm{softmax}\left(\frac{(\mathbf{Z}W_Q)(\mathbf{F}_{\mathcal{T}}^{k}W_K^k)^\top}{\sqrt{d_k}}\right)(\mathbf{F}_{\mathcal{T}}^{k}W_V^k)
$$

在此基础上，三个增强模块通过差异化和互补性操作提取不同粒度的先验特征：

- **形态学特异性增强模块（MSEM）** 提取静态形状先验 $\mathbf{Z}_{\mathcal{T}}^{\mathrm{sh}}$，通过增强 MANO 主导成分来捕捉与个体手部几何形态相关的稳定特征：

$$
\mathbf{Z}_{\mathcal{T}}^{\mathrm{sh}} = (\widehat{\mathbf{F}}_{\mathcal{T}}^{m} - \widehat{\mathbf{F}}_{\mathcal{T}}^{k}) \oplus (\widehat{\mathbf{F}}_{\mathcal{T}}^{m} \odot \widehat{\mathbf{F}}_{\mathcal{T}}^{k})
$$

- **惯性特异性增强模块（ISEM）** 提取时序运动先验 $\mathbf{Z}_{\mathcal{T}}^{\mathrm{tm}}$，通过增强 IMU 主导的运动信息来捕捉速度、加速度等动态变化：

$$
\mathbf{Z}_{\mathcal{T}}^{\mathrm{tm}} = (\widehat{\mathbf{F}}_{\mathcal{T}}^{k} - \widehat{\mathbf{F}}_{\mathcal{T}}^{m}) \oplus (\widehat{\mathbf{F}}_{\mathcal{T}}^{m} \odot \widehat{\mathbf{F}}_{\mathcal{T}}^{k})
$$

- **一致性增强模块（CEM）** 提取动态姿态先验 $\mathbf{Z}_{\mathcal{T}}^{\mathrm{po}}$，通过强调两模态的共有成分来捕捉与当前手势姿态相关的语义：

$$
\mathbf{Z}_{\mathcal{T}}^{\mathrm{po}} = (\widehat{\mathbf{F}}_{\mathcal{T}}^{m} \odot \widehat{\mathbf{F}}_{\mathcal{T}}^{k}) \oplus (\widehat{\mathbf{F}}_{\mathcal{T}}^{m} \oplus \widehat{\mathbf{F}}_{\mathcal{T}}^{k})
$$

这三种先验特征分别通过辅助回归头进行监督：形状头预测 MANO 形状参数 $\beta$，姿态头预测 MANO 姿态参数 $\theta$，时序头预测手部运动速度 $v$ 和加速度 $\alpha$（其真值标签由关节点的一阶和二阶离散差分 $\mathbf{d}_t^{\mathrm{gt}} = [\Delta \mathbf{J}_t^{\mathrm{gt}}, \Delta^2 \mathbf{J}_t^{\mathrm{gt}}]$ 提供）。这些辅助头与重建分支联合训练，使解耦特征在各自语义维度上充分专业化。

### 3.3 多粒度蒸馏损失设计

学生模型仅以 IMU 序列为输入，经投影头和 DSTFormer 编码器产生学生潜在特征 $\mathbf{F}_S$。为吸收教师的解耦先验，学生端采用并行的空间注意力模块 $A_{po}$ 和时间注意力模块 $A_{tm}$ 分别提取姿态和运动特征，并通过全局平均池化获得形状特征。多粒度蒸馏方案（MGDistill）通过三个模块在匹配粒度上对齐师生特征：

- **静态形状蒸馏（SSD）**：对齐师生归一化全局形状特征，传递与个体手部几何形态相关的稳定先验：

$$
\mathcal{L}_{ss} = \left\| \hat{\mathbf{Z}}_S^{\mathrm{sh}} - \hat{\mathbf{Z}}_T^{\mathrm{sh}} \right\|_2^2
$$

- **动态姿态蒸馏（DPD）**：逐帧对齐归一化姿态特征，传递与手势姿态相关的逐帧运动学先验：

$$
\mathcal{L}_{ps} = \frac{1}{T} \sum_{t=1}^{T} \left\| \hat{\mathbf{Z}}_{S,t}^{\mathrm{po}} - \hat{\mathbf{Z}}_{T,t}^{\mathrm{po}} \right\|_2^2
$$

- **时序运动蒸馏（TMD）**：逐帧对齐归一化时序运动特征，传递与运动连贯性相关的动态先验：

$$
\mathcal{L}_{ts} = \frac{1}{T} \sum_{t=1}^{T} \left\| \hat{\mathbf{Z}}_{S,t}^{\mathrm{tm}} - \hat{\mathbf{Z}}_{T,t}^{\mathrm{tm}} \right\|_2^2
$$

总蒸馏损失为三者的加权组合：

$$
\mathcal{L}_{\mathrm{distill}} = \lambda_{\mathrm{sh}}\mathcal{L}_{ss} + \lambda_{\mathrm{po}}\mathcal{L}_{ps} + \lambda_{\mathrm{tm}}\mathcal{L}_{ts}
$$

学生模型的最终训练目标在标准重建损失 $\mathcal{L}_{\mathrm{recon}}$ 基础上增加上述蒸馏损失：$\mathcal{L}_S = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{distill}}$。消融实验表明，DPD 是影响最大的组件——去除 DPD 导致 MPJPE 升高 35.7%、MPVPE 升高 32.9%，验证了动态姿态先验在弥合稀疏到密集映射差距中的核心作用。SSD 主要影响顶点几何精度（去除后 MPVPE 升高 20.3%），而 TMD 提供较小但一致的时序稳定性增益（MPJPE 升高 5.7%，MPVPE 升高 2.7%）。

## 实验与关键发现

### 主实验结果

#### VIHand 数据集 7-IMU 配置下的性能对比

在 VIHand 数据集上使用 7 个 IMU 传感器的标准配置下，MGDHand 框架取得了最优的 3D 手部姿态估计精度。如 Table 1 所示，MGDHand 的 MPJPE 达到 **9.13 mm**，MPVPE 达到 **10.46 mm**，在所有对比方法中均取得最低误差。与采用粗粒度全局特征蒸馏的 **VIFNet-S**（Wang et al., ACM MM 2025）相比，MGDHand 将 MPJPE 降低了 **33.3%**（9.13 mm vs. 13.69 mm），MPVPE 降低了 **36.7%**（10.46 mm vs. 16.53 mm）。与基于相邻关节注意力蒸馏的 **SCJD**（Chen et al., arXiv 2025）相比，MPJPE 和 MPVPE 分别进一步降低了 2.11 mm 和 3.04 mm。更重要的是，相较于完全不使用蒸馏的学生基线模型，MGDHand 将 MPJPE 从 15.4 mm 降至 9.13 mm，性能提升幅度高达 **40.7%**，MPVPE 亦从 17.15 mm 降至 10.46 mm（约 39.0% 的改善）。

![[assets/figures/papers/paper_list_l977_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MGDHand_Multi_Gra/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods of MPJPE (mm) and MPVPE (mm) on VIHand. #IMUs denotes the number of inertial sensors. † indicates tested with pre-trained weights*

这些结果表明，多粒度解耦蒸馏策略通过将教师模型中的静态形状、动态姿态和时序运动先验分层传递给学生，能够有效弥合稀疏 IMU 信号与密集手部姿态之间的语义鸿沟，且推理阶段不引入任何额外模态或计算开销。

#### 不同稀疏 IMU 配置下的鲁棒性

Table 2 展示了在不同 IMU 数量配置下的性能对比。随着 IMU 数量从 7 个减少到更稀疏的设置，所有方法的误差均有所上升，但 MGDHand 始终保持着对现有方法的显著优势。这一趋势验证了多粒度先验蒸馏在极端稀疏传感条件下的鲁棒性——即使在 IMU 信息极度受限时，解耦后的形状、姿态和运动先验仍能为学生模型提供有效的结构化引导。

![[assets/figures/papers/paper_list_l977_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MGDHand_Multi_Gra/figures/006_Table_2.jpg]]
*Table 2: Comparison of state-of-the-art IMU-based methods on VIHand. We report MPJPE (mm) and MPVPE (mm) under different sparse IMU configurations*

### 消融实验

为验证 MGDistill 方案中各组件的独立贡献，Table 3 报告了在 7-IMU 配置下的消融实验结果。

![[assets/figures/papers/paper_list_l977_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MGDHand_Multi_Gra/figures/005_Table_3.jpg]]
*Table 3: Ablation study of the MGDistill components on VIHand under 7 IMU configurations*

**动态姿态蒸馏（DPD）** 被证明是影响最大的组件：去除 DPD 后，MPJPE 从 9.13 mm 升至 12.39 mm（增加 **35.7%**），MPVPE 从 10.46 mm 升至 13.90 mm（增加 **32.9%**）。这表明逐帧对齐的姿态特征蒸馏是学生模型学习手部关节空间配置的核心驱动力，其缺失将导致姿态估计精度的大幅退化。

**静态形状蒸馏（SSD）** 的去除主要损害顶点级几何精度：MPVPE 升高 **20.3%**（10.46 mm → 12.58 mm），而 MPJPE 的退化相对温和。这一发现与 SSD 的设计目标一致——全局形状特征蒸馏主要约束手部网格的整体形态，对关节位置的直接影响小于对顶点分布的约束。

**时序运动蒸馏（TMD）** 的去除导致 MPJPE 升高 5.7%（9.13 mm → 9.65 mm），MPVPE 升高 2.7%（10.46 mm → 10.74 mm）。虽然提升幅度相对较小，但 TMD 的贡献在时序一致性方面具有重要价值：如 Figure 3 的定性对比所示，完整 MGDistill 方案在缓解手部变形、姿态偏差和时序滞后方面均优于去除 TMD 的变体。TMD 通过对齐逐帧运动特征，帮助学生模型更好地捕捉手部运动的动态连续性。

### 蒸馏策略对比

Table 4 进一步将 MGDistill 与多种蒸馏策略进行了对比。结果表明，无论是采用单一粒度的全局特征蒸馏，还是基于注意力迁移或关系蒸馏的方法，其性能均显著弱于本文提出的多粒度解耦蒸馏方案。这验证了核心洞察：将教师先验按形状-姿态-运动属性解耦，并在匹配的语义粒度上进行蒸馏，是弥合稀疏到密集映射差距的关键。

![[assets/figures/papers/paper_list_l977_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MGDHand_Multi_Gra/figures/007_Table_4.jpg]]
*Table 4: Comparison with different distill methods on VIHand under 7 IMU configurations*

### 定性分析

Figure 3 提供了与 SOTA 方法的定性可视化对比。在快速手势变化和复杂手指构型场景下，MGDHand 重建的手部姿态在关节位置精度、手指弯曲自然度和时序平滑性方面均优于对比方法。特别地，传统蒸馏方法（如 VIFNet-S）在手指末端关节和手腕旋转角度上容易出现偏差，而 MGDHand 通过 DPD 的逐帧姿态对齐有效缓解了这一问题。此外，TMD 的时序运动蒸馏使得重建结果在连续帧之间表现出更好的运动连贯性，减少了抖动和滞后现象。

![[assets/figures/papers/paper_list_l977_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MGDHand_Multi_Gra/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons with SOTAs. Our method mitigates hand deformation, pose deviation, and temporal lag*

### 实验设置与公平性说明

所有实验均在相同稀疏 IMU 配置下进行评估，学生模型推理时仅使用 IMU 数据，无额外模态或计算开销。教师模型仅在训练阶段使用 MANO 标注与 IMU 配对数据，推理时不需要。训练采用两阶段策略：首先使用 AdamW 优化器（初始学习率 1e-4，余弦衰减）训练 MANO-IMU 融合教师模型 80 个 epoch（batch size 32），然后固定教师权重，通过多粒度蒸馏损失联合训练学生模型。所有对比方法均在其公开的最佳配置下复现或引用原文结果，确保对比的公平性。

## 定位与知识库关联

### 1. 核心问题与基线对比

MGDHand 针对的是**稀疏IMU到手部姿态的跨模态映射**这一高度欠约束问题。其核心瓶颈在于：稀疏惯性信号仅提供局部运动信息，而密集手部姿态需要全局结构化输出，二者之间存在显著的语义鸿沟和信息密度差异。传统跨模态蒸馏方法（如 **VIFNet-S** (Wang et al., ACM MM 2025)）采用粗粒度全局特征蒸馏，将教师模型中的先验知识以耦合形式传递，忽略了模态间的语义不匹配，导致学生模型优化困难。

与现有工作的关键区别在于**先验解耦策略**：

| 对比维度 | VIFNet-S (Wang et al., ACM MM 2025) | SCJD (Chen et al., arXiv 2025) | MGDHand (本文) |
|---------|-------------------------------------|-------------------------------|----------------|
| 蒸馏粒度 | 粗粒度全局特征蒸馏 | 相邻关节注意力蒸馏 | 多粒度解耦蒸馏（形状/姿态/运动） |
| 先验利用 | 耦合视觉特征 | 关节级结构关系 | 解耦的静态形状、动态姿态、时序运动 |
| 语义对齐 | 跨模态特征空间直接对齐 | 局部关节关系对齐 | 在匹配语义粒度上分层对齐 |
| 推理模态 | IMU-only | IMU-only | IMU-only |

定量对比上，在 VIHand 数据集 7-IMU 配置下，MGDHand 的 MPJPE 为 9.13 mm，较 VIFNet-S 的 13.69 mm 降低 33.3%，较 SCJD 的 11.24 mm 降低 2.11 mm。这一差距源于 MGDHand 将教师先验按**形状-姿态-运动**属性解耦后，在对应语义空间中进行分层蒸馏，弥合了稀疏到密集的映射差距。

### 2. 方法谱系定位

MGDHand 在跨模态知识蒸馏和稀疏IMU姿态估计两条方法线上进行了关键创新：

**跨模态蒸馏线**：传统方法（如 VIFNet-S）将教师模型中的跨模态知识作为一个整体传递，学生模型需要同时学习模态转换和姿态回归。MGDHand 将这一过程拆解为三个互补子任务——静态形状蒸馏（SSD）对齐手部几何形态、动态姿态蒸馏（DPD）对齐逐帧关节配置、时序运动蒸馏（TMD）对齐运动一致性——使学生在各自语义空间内分别吸收教师先验，降低了优化难度。

**稀疏IMU姿态估计线**：现有方法多依赖单一重建损失从IMU直接回归姿态参数。MGDHand 引入的**多粒度先验-惯性蒸馏框架**（MGDistill）通过预训练 MANO-IMU 融合教师模型，将几何形态学先验、运动学先验和时序运动先验显式编码，再通过三个增强模块（MSEM、CEM、ISEM）解耦后传递给学生，实现了从“信号-姿态”直接映射到“信号-先验-姿态”结构化推理的范式转变。

### 3. 消融揭示的组件重要性

消融实验（Table 3）揭示了三个蒸馏模块的差异化贡献：

- **动态姿态蒸馏（DPD）** 是影响最大的组件：去除后 MPJPE 增加 35.7%、MPVPE 增加 32.9%。这表明逐帧姿态对齐是稀疏IMU姿态估计的核心挑战，教师模型提供的动态运动学先验对学生至关重要。
- **静态形状蒸馏（SSD）** 主要影响顶点几何精度：去除后 MPVPE 升高 20.3%，但对关节位置影响相对较小。这验证了形状先验在约束手部网格几何形态方面的专门作用。
- **时序运动蒸馏（TMD）** 贡献较小但一致：去除后 MPJPE 升高 5.7%、MPVPE 升高 2.7%。这说明时序一致性先验提供了增量但稳定的改进，有助于缓解帧间抖动。

完整 MGDistill 方案较无蒸馏学生基线降低 MPJPE 40.7%（15.4 mm → 9.13 mm），验证了多粒度解耦蒸馏策略的整体有效性。

### 4. 适用边界与局限

**适用条件**：
- 方法设计针对**稀疏IMU配置**（5-7个传感器），在传感器数量减少时仍保持性能优势（Table 2 显示在不同稀疏配置下均优于对比方法）。
- 依赖 MANO 手部模型的参数化表示，适用于有对应标注的数据集。
- 教师模型训练需要 MANO 标注与 IMU 信号的配对数据，但推理阶段仅需 IMU 输入。

**已知局限**：
- 教师模型的预训练需要完整的手部姿态标注（MANO 参数），限制了在纯IMU数据上的直接扩展。虽然文中未明确讨论，但这是跨模态蒸馏方法的固有约束。
- 多粒度蒸馏引入了三个超参数（λ_sh、λ_po、λ_tm），需要针对不同数据集和传感器配置进行调节。
- 文中未讨论极端手势（如严重遮挡、快速运动）下的性能，需要手动验证这些场景的鲁棒性。

**开放问题**：
- 教师模型解耦先验的质量如何影响学生性能？不同解耦策略（如基于物理约束的解耦）是否可进一步提升？
- 多粒度蒸馏框架是否可推广至其他跨模态姿态估计任务（如人体姿态、面部表情）？
- 在完全无标注的IMU数据上，是否可通过自监督或弱监督方式学习类似的多粒度先验表示？

## 原文 PDF

![[paperPDFs/CVPR_2026/MGDHand_Multi_Granularity_Prior_to_Inertial_Distillation_Framework_for_Sequential_3D_Hand_Pose_Estimation_from_Sparse_IMUs.pdf]]

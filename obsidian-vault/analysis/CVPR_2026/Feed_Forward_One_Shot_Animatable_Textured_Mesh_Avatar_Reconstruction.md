---
title: Feed-Forward One-Shot Animatable Textured Mesh Avatar Reconstruction
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Feed_Forward_One_Shot_Animatable_Textured_Mesh_Avatar_Reconstruction.pdf
project_link: "https://meshlam.github.io"
code_link: null
aliases:
- FFOSATMAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于GRU的迭代式解码机制配合重投影纹理引导——通过多步渐进式变形和纹理细化，利用隐藏状态保持时序一致性；同时将输入图像通过当前几何估计动态反投影到UV空间，为纹理合成提供直接的视觉监督信号，形成3D几何与2D观测之间的闭环反馈。
primary_logic: 将形状（顶点变形）和外观（UV纹理贴图）显式解耦为双分支架构，利用共享Transformer分别提取几何和纹理特征；引入迭代式GRU解码器实现从粗到细的渐进优化，每步通过拓扑校正和分部位变形约束保持网格完整性；创新性地使用重投影机制将输入图像的可见像素动态映射到UV空间，为纹理合成提供强视觉锚定，克服了单次回归的不稳定性。
claims:
- 直接回归顶点变形导致网格坍塌，GRU迭代解码有效防止该问题
- 去除纹理贴图分支导致性能崩溃（PSNR从25.23降至18.09），证明显式UV贴图表征的关键作用
- 8K顶点的网格重建质量显著优于80K高斯点的LAM方法，尤其在纹身、文字等高频细节上
- 重投影纹理引导对纹理质量至关重要，去除后导致模糊
---

# Feed-Forward One-Shot Animatable Textured Mesh Avatar Reconstruction

> [!tip] 核心洞察
> 将形状（顶点变形）和外观（UV纹理贴图）显式解耦为双分支架构，利用共享Transformer分别提取几何和纹理特征；引入迭代式GRU解码器实现从粗到细的渐进优化，每步通过拓扑校正和分部位变形约束保持网格完整性；创新性地使用重投影机制将输入图像的可见像素动态映射到UV空间，为纹理合成提供强视觉锚定，克服了单次回归的不稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MeshLAM：前馈式单图可驱动纹理网格头像重建 |
| 英文题名 | Feed-Forward One-Shot Animatable Textured Mesh Avatar Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.22865) · [Project](https://meshlam.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MeshLAM |
| Dataset | VFHQ test split |

> [!tip] 效果简介
> - VFHQ test split 上，PSNR↑ 25.233 (Ours w/ UNet) vs 22.850 (ROME w/ UNet) (+2.383)；LPIPS↓ 0.061 (Ours w/ UNet) vs 0.098 (ROME w/ UNet) (-0.037)；CSIM↑ 0.948 (Ours w/ UNet) vs 0.681 (ROME w/ UNet) (+0.267)。

## 概要

从单张图片重建可驱动的3D头像是一个具有挑战性的问题。现有前馈式方法主要面临两个根本瓶颈：**基于3D高斯的方法**（如LAM、GAGAvatar）需要大量基元（高达80K高斯点）来建模细节纹理，导致训练和推理计算开销大，且单次前向传递难以优化出高保真细节，产生模糊结果；**直接回归顶点变形偏移量**则会导致网格坍塌和拓扑破坏，尤其在长发、头饰等需要大变形的区域，因为独立预测的顶点位移缺乏结构约束，误差会传播为严重的网格畸变。

**MeshLAM** 针对上述瓶颈提出了一套系统性的解决方案。其核心洞察是将形状（顶点变形）与外观（UV纹理贴图）显式解耦为双分支架构，利用共享Transformer分别提取几何和纹理特征；引入迭代式GRU解码器实现从粗到细的渐进优化，每步通过拓扑校正和分部位变形约束保持网格完整性；创新性地使用重投影机制将输入图像的可见像素动态映射到UV空间，为纹理合成提供强视觉锚定，克服了单次回归的不稳定性。

在VFHQ测试集上，MeshLAM以仅8K顶点的网格表征取得了PSNR 25.23、LPIPS 0.061、CSIM 0.948的成绩，显著优于基于80K高斯点的LAM方法（PSNR 25.08、FID 24.27）和网格基线ROME（PSNR 22.85、LPIPS 0.098）。消融实验证实：去除纹理贴图分支导致PSNR骤降至18.09，去除GRU迭代解码使PSNR降至23.08，去除重投影引导则导致纹理模糊。方法推理速度仅需0.7秒，大幅快于LAM的1.4秒（20K高斯）至5.8秒（80K高斯），在效率与质量之间取得了优异平衡。

在方法谱系上，MeshLAM属于**前馈式单图可驱动网格头像重建**方法，与基于3D高斯的前馈方法（LAM、GAGAvatar）和传统网格回归方法（ROME）形成对比。其知识贡献在于证明了显式UV纹理贴图表征配合迭代GRU解码和重投影视觉引导，可以在低顶点数网格上实现超越高斯基元数量的重建质量，为高效高保真3D头像重建开辟了新路径。

### 问题背景：单图可驱动3D头像重建

从单张RGB图像重建可驱动的3D头像，是计算机视觉与图形学交叉领域的核心问题之一。其目标是从一张输入照片中同时恢复出完整的几何形状和外观纹理，并使其能够被任意表情参数驱动、从新视角渲染。这一能力在虚拟现实、远程呈现、数字人交互和影视制作等场景中具有广泛的应用需求。

近年来，前馈式（feed-forward）单次重建方法因其无需逐例优化的推理速度优势而受到关注。这类方法通过训练神经网络直接从输入图像映射到3D表征，在推理时仅需一次前向传递即可完成重建，避免了传统优化方法（如NeRF或3DGS的逐场景优化）所需的数分钟甚至数小时的拟合过程。

### 现有方法的两个根本瓶颈

尽管前馈式方法在效率上具有明显优势，但现有方案在重建质量和表征效率上面临两个根本性瓶颈：

**瓶颈一：3D高斯表征的细节-效率矛盾。** 基于3D高斯点云（3D Gaussian Splatting）的前馈方法（如**LAM**）需要大量基元来建模细节纹理——典型配置需约80K高斯点——导致训练和推理的计算开销显著增加。更关键的是，在单次前向传递中，网络难以同时优化如此大量基元的位置、协方差和颜色参数以恢复高保真细节，最终产生模糊的重建结果。实验证据显示，即使使用80K高斯点，LAM仍无法准确重建纹身、文字等高频纹理细节（Figure 2）。

**瓶颈二：直接回归顶点变形的网格坍塌问题。** 基于网格的方法试图直接回归顶点变形偏移量，但这种独立预测的顶点位移缺乏结构约束。在需要大变形的区域（如长发、头饰），各顶点误差独立累积并传播，导致严重的网格坍塌和拓扑破坏。消融实验证实，去除GRU迭代解码、采用直接回归时，网格会出现“severe mesh collapse and topological corruption”（Figure 4），表明单次回归策略在几何层面存在根本性的不稳定性。

### 本文动机与核心思路

针对上述瓶颈，本文提出**MeshLAM**，一种基于可驱动纹理网格的前馈式单图头像重建方法。其核心动机在于：**将形状与外观显式解耦，并通过迭代式渐进优化克服单次回归的不稳定性**。

具体而言，MeshLAM采用双分支架构，将顶点变形（几何）和UV纹理贴图（外观）分离为两个并行分支，利用共享Transformer分别提取几何和纹理特征。在此基础上，引入基于GRU的迭代式解码机制，通过多步渐进变形和纹理细化，利用隐藏状态保持时序一致性，实现从粗到细的稳定优化。同时，创新性地使用重投影机制（reprojection-based unwrapping），将输入图像的可见像素动态映射到UV空间，为纹理合成提供直接的视觉监督信号，形成3D几何与2D观测之间的闭环反馈。

这一设计使得MeshLAM仅需8K顶点即可重建出优于80K高斯点方法的纹理细节，同时将推理时间压缩至0.7秒，在质量与效率之间取得了突破性平衡。

## 核心方法与创新机理

MeshLAM 的核心创新在于通过三个相互协同的机制设计，系统性地克服了前馈式单图头像重建中的两大瓶颈——3D高斯表征的高计算开销与细节模糊，以及直接回归顶点变形导致的网格坍塌。

### 1. 显式解耦的形状-外观双分支架构

MeshLAM 将三维头像重建问题**显式解耦**为几何与外观两个独立分支：形状分支预测顶点相对于 FLAME 模板的变形偏移量，纹理分支合成高分辨率 UV 对齐纹理贴图。这一设计与现有基于 3D 高斯点云（Gaussian Splatting）的方法形成根本性差异——后者需要大量基元（如 LAM 需 80K 高斯点）来隐式建模纹理细节，而 MeshLAM 仅用 **8K 顶点**即可实现更高保真度的纹理重建，尤其在纹身、文字等高频细节上优势显著（Figure 2）。

从表征层面看，这一解耦带来了三重收益：
- **计算效率**：推理速度仅需 0.7 秒，显著快于 LAM（1.4 秒 @20K 高斯，5.8 秒 @80K 高斯）；
- **纹理质量**：UV 纹理贴图作为显式外观表征，为纹理合成提供了结构化先验，去除该分支导致 PSNR 从 25.23 崩溃至 18.09，FID 从 22.70 飙升至 74.08（Table 2）；
- **可编辑性**：显式 UV 贴图天然支持纹理编辑和跨域迁移（如文本到 3D 头像生成，Figure 3）。

### 2. 迭代式 GRU 渐进解码机制

针对单次前向回归（single-pass regression）在预测顶点变形时产生的网格坍塌和拓扑破坏问题（Figure 4），MeshLAM 引入基于 **GRU 的迭代式解码机制**。该机制通过多步渐进式变形和纹理细化，利用隐藏状态保持时序一致性，实现从粗到细的稳定优化。

核心因果链条如下：
- 直接回归独立预测每个顶点的位移，缺乏结构约束，误差在大变形区域（长发、头饰）传播为严重畸变；
- GRU 迭代解码将变形过程分解为多个连贯步骤，每步基于上一步的网格状态和当前视觉误差信号进行增量修正；
- 消融实验证实，去除 GRU 迭代解码后 PSNR 从 25.23 降至 23.08，FID 从 22.70 升至 26.40（Table 2），且出现明显的网格坍塌现象（Figure 4）；
- 两次迭代（N=2）实现最优性能平衡（Table 2）。

### 3. 重投影纹理引导机制

MeshLAM 创新性地引入**重投影反扭曲（reprojection-based unwrapping）**模块，将输入图像的可见像素通过当前几何估计动态映射到 UV 纹理空间，为纹理合成提供直接的视觉监督信号。这形成了 3D 几何与 2D 观测之间的闭环反馈：几何估计越准确，反扭曲的纹理信号越可靠；纹理信号越清晰，下一步的几何优化越精准。

与基线方法中纹理完全依赖隐式学习不同，重投影机制为纹理 GRU 解码器提供了强视觉锚定：
- 每步迭代将输入图像 $\mathcal{U}(I_{\text{input}}, \mathcal{R}(M_t^{\text{animated}}))$ 和渲染误差 $F_{d_t}$ 反扭曲到 UV 空间，与当前纹理估计拼接后送入卷积 GRU 进行渐进式细化；
- 去除该机制导致纹理合成失去直接视觉引导，产生模糊外观（Figure 5），定量指标明显退化（Table 2）。

### 4. 分部位感知变形约束与拓扑校正

为在保持网格完整性的同时允许大变形区域的灵活表达，MeshLAM 引入**分部位感知变形裁剪（part-aware deformation clipping）**和**拓扑校正（topology correction）**两个互补机制：

- **变形裁剪**：对不同语义区域设定差异化的变形范围——头发区域 $\delta_{\text{hair}}=0.08$、颈部 $\delta_{\text{neck}}=0.02$、面部 $\delta_{\text{face}}=0.003$，防止面部结构出现不合理的畸变（Figure 6）；
- **拓扑校正**：在每次变形后对网格进行长边细分、翻转面修正和无效面删除，并更新蒙皮权重，确保动画兼容性。

这两个机制共同构成了从“无约束直接回归”到“结构化渐进变形”的关键转变，使得 MeshLAM 在保持解剖学正确性的同时，能够灵活处理头发和配饰等大变形区域。

MeshLAM 提出了一种**前馈式单图可驱动纹理网格头像重建**方法，其核心设计围绕三个关键创新展开：**显式解耦的形状-外观双分支架构**、**迭代式 GRU 渐进解码机制**、以及**重投影纹理引导**。整体流程从单张输入图像出发，最终输出一个具有高保真纹理的可驱动 3D 头部网格。

### 输入输出与表征选择

方法以单张 RGB 图像作为输入，输出一个基于 **FLAME 模板网格**的可驱动 3D 头像。与当前主流的 3D 高斯点云（Gaussian Splatting）表征不同，MeshLAM 采用**显式纹理网格**作为三维表征——几何由顶点变形偏移量（per-vertex deformations）描述，外观则由 UV 空间对齐的高分辨率纹理贴图（1024×1024）承载。这一设计选择直接回应了高斯方法的核心瓶颈：为建模细节纹理需要大量基元（如 80K 高斯点），导致训练和推理计算开销大，且单次前向传递难以优化出高保真细节（参见 Figure 2 的定性对比）。

### 双分支特征提取

pipeline 的起点是共享的 **DINOv2 ViT 骨干网络**，用于从输入图像中提取多尺度图像特征 $F_I \in \mathbb{R}^{N \times C}$。随后，框架分叉为两个并行的交叉注意力分支：

- **顶点分支**：将 FLAME 模板网格的顶点作为可学习 token，通过多层交叉注意力与图像特征交互，提取几何感知的顶点特征 $F_V$：
  $$F_{V_i} = \mathcal{A}_i(F_{V_{i-1}}, F_I) \quad \text{(Eq. 1)}$$

- **纹理分支**：维护一个可学习的 UV 空间 token 网格，通过**共享**的交叉注意力层与图像特征交互，提取外观感知的纹理特征 $F_T$：
  $$F_{T_i} = \mathcal{A}_i(F_{T_{i-1}}, F_I) \quad \text{(Eq. 2)}$$

两个分支共享交叉注意力层的结构但独立处理各自的 token，实现了形状与外观的显式解耦——这是方法能够分别优化几何精度和纹理保真度的结构基础。

### 迭代式 GRU 渐进解码

区别于单次前向回归（single-pass regression）方法，MeshLAM 引入了**基于 GRU 的迭代式解码机制**，对几何和纹理进行多步渐进优化。这一设计的因果动因在于：直接回归顶点变形偏移量会导致网格坍塌和拓扑破坏，尤其在需要大变形的区域（如长发、头饰），因为独立预测的顶点位移缺乏结构约束，误差会传播为严重的网格畸变（Figure 4 提供了直接回归与 GRU 迭代解码的对比证据）。

每次迭代中，两个 GRU 解码器协同工作：

- **纹理 GRU 解码器**：融合当前纹理估计 $T_t$、反扭曲图像 $U_t$、潜在特征 $F_a$ 和预测误差 $F_{d_t}$，通过卷积 GRU 逐步细化纹理：
  $$T_{t+1} = \mathrm{GRU}_{\mathrm{tex}}(\varphi([\varphi([T_t, U_t]), F_a, F_{d_t}]), h_t^{\mathrm{tex}}) \quad \text{(Eq. 4)}$$

- **几何 GRU 解码器**：融合顶点位置编码、视觉预测误差特征 $F_{d_t2v}$ 和顶点特征 $F_V$，预测变形偏移量：
  $$\Delta V_{t+1} = \mathrm{GRU}_{\mathrm{geo}}([\psi(\vartheta(V_t), F_{d_t2v}), F_V], h_t^{\mathrm{geo}}) \quad \text{(Eq. 5)}$$

GRU 的隐藏状态 $h_t$ 在迭代间保持时序一致性，使得变形和纹理细化过程具有连贯性，从粗到细逐步收敛。实验表明，两次迭代（$N=2$）实现了最优的性能-效率平衡（Table 2 消融实验证实）。

### 重投影纹理引导

纹理分支的关键创新在于**重投影反扭曲机制**（reprojection-based unwrapping）。在每次迭代中，当前几何估计 $M_t^{\mathrm{animated}}$ 被光栅化后，输入图像 $I_{\mathrm{input}}$ 通过该几何代理**动态反投影到 UV 纹理空间**：
$$U_t = \mathcal{U}(I_{\mathrm{input}}, \mathcal{R}(M_t^{\mathrm{animated}})) \quad \text{(Eq. 3)}$$

这一机制为纹理合成提供了直接的视觉锚定信号——将 2D 观测与 3D 几何之间形成闭环反馈。去除该模块会导致纹理模糊，性能明显退化（Figure 5 和 Table 2 消融实验证实），证明了显式视觉引导对高保真纹理重建的关键作用。

### 几何约束与拓扑保持

为保持网格的解剖学正确性和拓扑完整性，几何分支在每次 GRU 迭代后施加两类约束：

- **分部位感知变形裁剪**（part-aware deformation clipping）：对头发区域允许较大的变形范围（$\delta_{\mathrm{hair}} = 0.08$），而面部区域施加严格约束（$\delta_{\mathrm{face}} = 0.003$），颈部取中间值（$\delta_{\mathrm{neck}} = 0.02$）。这一设计防止了不合理的面部结构扭曲（Figure 6 消融实验提供证据）。

- **拓扑校正**（topology correction）：对超过阈值 $\varepsilon$ 的长边进行细分、修正翻转的三角面方向、删除几何无效面，并同步更新蒙皮权重，确保网格在动画驱动下保持完整性。

### 可选神经渲染器与损失函数

最终渲染阶段，方法可选地通过一个 **StyleGAN-like UNet 神经渲染器**对光栅化结果进行增强，进一步提升渲染质量。训练采用多分量联合优化目标，核心损失包括：

- **图像重建损失**：像素级 L2 损失与感知损失的组合：
  $$\mathcal{L}_{\mathrm{img}} = \|I_{\mathrm{rendered}} - I_{\mathrm{gt}}\|_2^2 + \phi(I_{\mathrm{rendered}}, I_{\mathrm{gt}}) \quad \text{(Eq. 6)}$$

- **拉普拉斯正则化**：对网格顶点施加一阶邻域平滑约束，防止顶点散射和自交：
  $$\mathcal{L}_{\mathrm{lap}} = \sum_{v_i} \left\| v_i - \frac{1}{|\mathcal{N}(i)|} \sum_{j \in \mathcal{N}(i)} v_j \right\|^2 \quad \text{(Eq. 10)}$$

$N$ 次迭代的损失按衰减因子 $\gamma = 0.8$ 加权求和：
$$\mathcal{L}_{\mathrm{total}} = \sum_{t=1}^{N} \gamma^{N-t} \mathcal{L}_{t}$$

### 推理效率

得益于显式网格表征和高效的双分支设计，MeshLAM 从单张图像重建完整 3D 头像仅需 **0.7 秒**，显著快于基于高斯的 LAM 方法（1.4 秒 @20K 高斯点，5.8 秒 @80K 高斯点），在保持高保真纹理的同时实现了实用的推理速度。

MeshLAM 的核心架构围绕**形状-外观显式解耦**与**迭代式渐进优化**两条主线展开。整体流程为：共享 DINOv2 ViT 主干提取多尺度图像特征 $F_I \in \mathbb{R}^{N \times C}$，双分支交叉注意力分别提取顶点特征 $F_V$ 和纹理特征 $F_T$，随后进入迭代 GRU 解码循环，每一步同时更新几何变形和 UV 纹理贴图，并通过重投影机制形成 3D 几何与 2D 观测之间的闭环反馈。

### 3.1 双分支特征提取

**顶点交叉注意力（Vertex Cross-Attention）** 将 FLAME 模板顶点作为查询，与图像特征交互以获取几何先验：

$$F_{V_i} = \mathcal{A}_i(F_{V_{i-1}}, F_I) \quad \text{(Eq. 1)}$$

**纹理交叉注意力（Texture Cross-Attention）** 在可学习的 UV 空间 token 网格上执行共享注意力操作，提取外观特征：

$$F_{T_i} = \mathcal{A}_i(F_{T_{i-1}}, F_I) \quad \text{(Eq. 2)}$$

两个分支共享交叉注意力层权重 $\mathcal{A}_i$，确保几何与纹理特征在统一的图像条件下协同演化。Transformer 配置为 2 层、16 注意力头、隐藏维度 $C_t = 1024$。

### 3.2 纹理空间重投影与反扭曲

这是 MeshLAM 区别于隐式纹理合成方法的关键机制。在第 $t$ 次迭代中，将输入图像 $I_{\text{input}}$ 通过当前动画网格 $M_t^{\text{animated}}$ 光栅化后反扭曲到 UV 纹理空间：

$$U_t = \mathcal{U}(I_{\text{input}}, \mathcal{R}(M_t^{\text{animated}})) \quad \text{(Eq. 3)}$$

其中 $\mathcal{R}$ 为可微光栅化器，$\mathcal{U}$ 为 UV 反扭曲操作。该模块将输入图像的可见像素动态映射到 UV 空间，为纹理合成提供直接的视觉锚定信号，克服了单次回归中纹理模糊的问题。消融实验证实，去除该机制后纹理合成失去直接视觉引导，产生模糊外观（Figure 5）。

![[assets/figures/papers/paper_list_l1020_https_arxiv_org_abs_2604_22865/figures/009_Figure_5.jpg]]
*Figure 5: Effect of texture space reprojection. Without our reprojection mechanism (middle), texture synthesis lacks direct visual guidance, resulting in a blurry appearance, while ours enable highfidelity texture details*

### 3.3 迭代纹理 GRU 解码

纹理细化采用卷积 GRU 结构，融合四个信息源：当前纹理估计 $T_t$、反扭曲图像 $U_t$、潜在特征 $F_a$ 以及预测误差特征 $F_{d_t}$：

$$T_{t+1} = \mathrm{GRU}_{\mathrm{tex}}(\varphi([\varphi([T_t, U_t]), F_a, F_{d_t}]), h_t^{\mathrm{tex}}) \quad \text{(Eq. 4)}$$

其中 $\varphi$ 为卷积特征编码器，$h_t^{\mathrm{tex}}$ 为 GRU 隐藏状态。预测误差特征 $F_{d_t}$ 捕捉当前渲染与输入图像之间的差异，为 GRU 提供显式的修正信号：

$$F_{d_t} = \mathcal{U}(\varphi([I_{\text{input}}, I_{\text{rendered}}, I_{\text{input}} - I_{\text{rendered}}]))$$

这一残差驱动的设计使得纹理合成能够逐步修正局部误差，从粗到细地恢复高频细节。

### 3.4 迭代几何 GRU 变形

几何分支同样采用 GRU 迭代预测顶点变形偏移量 $\Delta V_{t+1}$，输入包括顶点位置编码 $\vartheta(V_t)$、视觉预测误差特征 $F_{d_t2v}$ 以及顶点特征 $F_V$：

$$\Delta V_{t+1} = \mathrm{GRU}_{\mathrm{geo}}([\psi(\vartheta(V_t), F_{d_t2v}), F_V], h_t^{\mathrm{geo}}) \quad \text{(Eq. 5)}$$

其中 $\psi$ 为融合函数，$h_t^{\mathrm{geo}}$ 为几何 GRU 隐藏状态。与直接回归顶点位移不同，GRU 的隐藏状态在迭代间保持时序一致性，使得变形过程平滑且可控。消融实验表明，去除 GRU 迭代解码直接回归会导致严重的网格坍塌和拓扑破坏（Figure 4），PSNR 从 25.23 降至 23.08，FID 从 22.70 升至 26.40（Table 2）。

### 3.5 分部位感知变形约束与拓扑校正

为防止无约束变形导致不合理的面部结构，MeshLAM 对不同语义区域施加差异化的变形裁剪范围：

- 头发区域：$\delta_{\text{hair}} = 0.08$
- 颈部区域：$\delta_{\text{neck}} = 0.02$
- 面部区域：$\delta_{\text{face}} = 0.003$

此外，每次迭代后执行**拓扑校正**操作：细分边长超过阈值 $\varepsilon$ 的三角形、翻转方向不一致的面、删除几何无效面，并更新蒙皮权重以保持动画兼容性。消融实验证实，去除分部位约束会导致不合理的面部结构（Figure 6）。

![[assets/figures/papers/paper_list_l1020_https_arxiv_org_abs_2604_22865/figures/010_Figure_6.jpg]]
*Figure 6: Effect of part-aware deformation. Without semantic constraints, deformation leads to implausible facial structures. Our part-aware approach preserves anatomical correctness while allowing flexible deformation of hair and accessories*

### 3.6 损失函数

**图像重建损失** 结合像素级 L2 损失与感知损失 $\phi$，确保纹理锐度和全局外观一致性：

$$\mathcal{L}_{\mathrm{img}} = \|I_{\mathrm{rendered}} - I_{\mathrm{gt}}\|_2^2 + \phi(I_{\mathrm{rendered}}, I_{\mathrm{gt}}) \quad \text{(Eq. 6)}$$

**掩码损失** 约束渲染轮廓与真值前景掩码一致：

$$\mathcal{L}_{\mathrm{mask}} = \|M_{\mathrm{rendered}} - M_{\mathrm{gt}}\|_2^2$$

**拉普拉斯正则化** 对网格顶点施加一阶邻域平滑约束，防止顶点散射和自交：

$$\mathcal{L}_{\mathrm{lap}} = \sum_{v_i} \left\| v_i - \frac{1}{|\mathcal{N}(i)|} \sum_{j \in \mathcal{N}(i)} v_j \right\|^2 \quad \text{(Eq. 10)}$$

**总损失** 对 $N$ 次迭代的损失按衰减因子 $\gamma$ 加权求和，赋予后期迭代更高权重：

$$\mathcal{L}_{\mathrm{total}} = \sum_{t=1}^{N} \gamma^{N-t} \mathcal{L}_{t}$$

其中 $N=2$，$\gamma=0.8$。两次 GRU 迭代在性能与效率之间取得最优平衡（Table 2）。

### 3.7 可选神经渲染器

最终渲染结果可选择通过一个 StyleGAN 风格的 UNet 神经渲染器进行增强，进一步提升照片真实感。Table 1 中 "Ours w/ UNet" 与 "Ours w/o UNet" 的对比量化了该模块的贡献。

## 实验与关键发现

### 主实验结果

我们在VFHQ测试集上对MeshLAM进行了全面的定量评估。Table 1报告了单图3D头像重建任务的核心指标。在配对图像指标上，MeshLAM配合可选的UNet神经渲染器（Ours w/ UNet）取得了PSNR 25.233、SSIM 0.879、LPIPS 0.061的成绩，相较于基于网格的基线方法**ROME**（w/ UNet）的PSNR 22.850和LPIPS 0.098，分别提升了+2.383 dB和–0.037。在身份保持指标上，MeshLAM的CSIM达到0.948，远超ROME的0.681（+0.267），表明我们的方法在保持人物身份特征方面具有显著优势。

当将MeshLAM的重建结果作为初始化，再结合**LAM**的3D高斯优化管线（LAM+Ours）时，整体性能进一步提升至PSNR 25.889、SSIM 0.893、LPIPS 0.050，全面超越LAM+FLAME基线的25.082、0.882、0.058。在分布级指标FID上，Ours w/ UNet达到22.699，优于LAM+FLAME的24.270（–1.571），说明我们的网格表征能生成更逼真、更符合真实分布的渲染结果。

Table 3的补充对比进一步验证了这一优势：MeshLAM在PSNR（25.233）和FID（22.699）上均领先于前馈式高斯方法**GAGAvatar**（25.020 / 30.137）和**Portrait4Dv2**（24.650 / 25.014），尤其在FID上优势明显，表明网格表征在生成质量上优于高斯点云方法。

### 定性分析

Figure 2展示了在挑战性纹理案例上的定性对比。MeshLAM仅使用8K顶点即可成功建模纹身、文字、发丝等高频纹理细节，而基于3D高斯的**LAM**方法即使使用80K高斯点仍无法捕捉这些精细结构，产生模糊结果。这直接验证了我们核心设计动机的有效性：显式UV纹理贴图表征相比隐式的高斯球谐系数，能更高效地编码和合成高保真外观细节。

Figure 7展示了重建的几何网格和UV纹理贴图。即使在驱动到与输入图像不同的表情时，MeshLAM仍能生成清晰、一致的展开纹理，证明了双分支解耦设计在几何和外观学习上的有效性。

### 消融实验

Table 2系统性地评估了各核心组件的贡献，揭示了以下关键发现：

**纹理贴图分支的不可替代性。** 移除纹理贴图分支（w/o Texture Map）导致性能灾难性崩溃：PSNR从25.23骤降至18.09（–7.14），FID从22.70飙升至74.08（+51.38）。这一极端退化证明显式UV纹理贴图是高质量外观重建的基石，隐式颜色回归无法弥补其缺失。

**迭代GRU解码的关键作用。** 去除GRU迭代解码（w/o GRU）使PSNR降至23.08（–2.15），FID升至26.40（+3.70）。Figure 4的定性结果揭示了退化机制：直接回归顶点变形偏移量会导致严重的网格坍塌和拓扑破坏，尤其在长发、头饰等需要大位移的区域。GRU的渐进式变形策略通过隐藏状态保持时序一致性，配合分部位变形约束，有效防止了误差累积导致的网格畸变。

**重投影纹理引导的必要性。** 移除重投影反扭曲机制（w/o Unwrapping）造成纹理质量的明显退化。Figure 5显示，缺乏重投影引导时，纹理合成失去直接的视觉锚定信号，导致模糊的外观。这一结果证实了我们的核心洞察：将输入图像的可见像素动态映射到UV空间，为纹理合成提供了强视觉监督，克服了单次回归的不稳定性。

**分部位变形约束的贡献。** 去除分部位感知变形裁剪（w/o Part-aware）导致不合理的面部结构（Figure 6）。通过为头发区域（δ=0.08）、颈部（δ=0.02）和面部（δ=0.003）设置差异化的变形范围，该方法在保持解剖学正确性的同时，允许头发和配饰区域的灵活变形。

**迭代次数的优化。** 两次GRU迭代（N=2）实现了最优性能平衡。增加迭代次数可略微提升细节，但计算开销线性增长；单次迭代则无法充分发挥渐进式优化的优势。

### 计算效率

MeshLAM在推理效率上展现出显著优势：从单张输入图像重建完整3D头像仅需0.7秒。相比之下，基于3D高斯的LAM方法在20K高斯点配置下需要1.4秒，80K高斯点配置下则需5.8秒。MeshLAM以更少的基元（8K顶点 vs 80K高斯点）实现了更优的重建质量和更快的推理速度，验证了网格表征在前馈式头像重建任务中的计算效率优势。

### 失败模式与局限性

尽管MeshLAM在VFHQ测试集上取得了优异表现，论文未提供系统性的失败案例分析。从方法设计和开放问题推断，以下场景可能存在退化风险：

1. **极端头部姿态**：当输入图像存在大幅度侧转或仰头时，重投影反扭曲模块可能因大面积自遮挡而缺乏足够的可见像素，导致纹理合成质量下降。
2. **重度遮挡**：口罩、墨镜、手部遮挡等场景会同时破坏几何和纹理分支的输入信号，当前方法对此类情况的鲁棒性未经充分验证。
3. **拓扑校正的边界情况**：在极端变形下，长边细分和翻转面修正操作可能引入不稳定的拓扑变化，其对动画兼容性的影响需要更系统的测试。

需要注意的是，上述局限性分析基于方法设计的逻辑推断，而非论文中报告的实证结果，具体退化程度需要进一步实验验证。

![[assets/figures/papers/paper_list_l1020_https_arxiv_org_abs_2604_22865/figures/011_Table_2.jpg]]
*Table 2: Quantitative ablation study of different design choices*

![[assets/figures/papers/paper_list_l1020_https_arxiv_org_abs_2604_22865/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative comparison of 3D head avatar creation and animation on challenging texture cases. Our mesh-based framework successfully models high-fidelity texture details with only 8K vertices, substantially outperforming the Gaussian-based LAM method that requires 80K Gaussian points while still failing to capture fine details*

![[assets/figures/papers/paper_list_l1020_https_arxiv_org_abs_2604_22865/figures/012_Figure_7.jpg]]
*Figure 7: Reconstructed geometry and texture map visualization. Our method produces a mesh with high-fidelity texture, even when animated to an expression different from the input image. The sharp, consistently unwrapped texture details demonstrate the effectiveness of our dual-branch design*

![[assets/figures/papers/paper_list_l1020_https_arxiv_org_abs_2604_22865/figures/005_Figure_3.jpg]]
*Figure 3: The cross-domain generalization capability of our framework enables easy adaptation to text-to-3D avatar generation and editing, by incorporating a pretrained image generation framework*

## 定位与知识库关联

### 1. 技术路线定位：从3D高斯到可驱动纹理网格

MeshLAM处于单次前馈式3D头像重建的技术演进线上，其核心贡献在于**表征范式转换**——从当前主流的3D高斯泼溅（3D Gaussian Splatting）回归到显式纹理网格表征。这一选择由两个根本瓶颈驱动：

- **高斯表征的细节-效率矛盾**：基于高斯的LAM方法需要约80K高斯点来建模纹理细节，但即使如此仍难以捕捉纹身、文字等高频纹理（Figure 2证实了这一点）。大量基元导致训练和推理计算开销大（80K高斯点推理需5.8秒），且在单次前向传递中难以优化出高保真细节，产生模糊结果。
- **网格表征的拓扑稳定性挑战**：直接回归顶点变形偏移量会导致网格坍塌和拓扑破坏，尤其在长发、头饰等需要大变形的区域。独立预测的顶点位移缺乏结构约束，误差会传播为严重的网格畸变（Figure 4提供了直观证据）。

MeshLAM的应对策略是**显式解耦形状与外观**：形状分支预测相对于FLAME模板的逐顶点变形，纹理分支合成UV对齐的高分辨率纹理贴图。这种解耦使得仅需8K顶点即可实现超越80K高斯点的纹理质量，同时将推理时间压缩至0.7秒。

### 2. 关键机制创新：迭代GRU解码与重投影闭环

MeshLAM区别于先前工作的三个核心机制：

| 机制 | 基线做法 | MeshLAM做法 | 因果作用 |
|------|----------|-------------|----------|
| 解码策略 | 单次前向回归 | 迭代式GRU渐进解码（N=2） | 通过隐藏状态保持时序一致性，从粗到细渐进优化，防止网格坍塌 |
| 纹理引导 | 隐式学习，无显式视觉监督 | 重投影反扭曲（reprojection unwrapping） | 将输入图像通过当前几何估计动态映射到UV空间，为纹理合成提供强视觉锚定 |
| 几何约束 | 无约束直接回归 | 分部位感知变形裁剪 + 拓扑校正 | 头发区域允许较大变形（δ_hair=0.08），面部区域严格约束（δ_face=0.003），保持解剖学正确性 |

**重投影机制**是MeshLAM最具特色的设计：在每次GRU迭代中，当前动画网格被光栅化后，输入图像和预测误差被反扭曲到UV纹理空间（Eq. 3: $U_t = \mathcal{U}(I_{\mathrm{input}}, \mathcal{R}(M_t^{\mathrm{animated}}))$），形成3D几何与2D观测之间的闭环反馈。消融实验证实，去除该机制会导致纹理模糊（Figure 5），PSNR显著下降。

### 3. 与现有方法的定量关系

在VFHQ测试集上的主实验结果（Table 1）揭示了方法间的性能梯度：

- **与网格基线ROME的对比**：MeshLAM在PSNR上领先2.38dB（25.23 vs 22.85），LPIPS降低38%（0.061 vs 0.098），CSIM身份保持指标提升39%（0.948 vs 0.681）。这表明双分支解耦和迭代细化显著优于单次网格回归。
- **与高斯基线LAM的对比**：即使LAM使用80K高斯点，MeshLAM仅用8K顶点仍在FID上领先1.57（22.70 vs 24.27）。当MeshLAM的纹理贴图用于增强LAM渲染（LAM+Ours配置）时，PSNR进一步提升至25.89，说明UV贴图表征本身具有独立价值。
- **与其他前馈方法的对比**（Table 3）：GAGAvatar（PSNR 25.02, FID 30.14）和Portrait4Dv2（PSNR 24.65, FID 25.01）均不及MeshLAM（PSNR 25.23, FID 22.70），尤其是在分布级指标FID上的差距更为显著，暗示MeshLAM的重建结果在整体外观分布上更接近真实图像。

### 4. 消融实验揭示的因果链路

Table 2的消融实验建立了清晰的因果链：

1. **纹理贴图分支是关键组件**：去除后PSNR从25.23崩溃至18.09，FID从22.70飙升至74.08——这是所有消融中影响最大的操作，证明显式UV贴图表征对纹理质量的决定性作用。
2. **GRU迭代解码防止网格坍塌**：去除后PSNR降至23.08，FID升至26.40。Figure 4可视化表明，直接回归导致严重的网格坍塌和拓扑破坏，而GRU渐进变形保持了网格完整性。
3. **重投影反扭曲提供视觉锚定**：去除后纹理合成缺乏直接视觉引导，导致模糊外观（Figure 5）。
4. **分部位变形约束保持解剖合理性**：去除后面部结构出现不合理变形（Figure 6）。
5. **迭代次数N=2实现最优平衡**：更多迭代未带来显著增益，表明两轮从粗到细的优化已足够收敛。

### 5. 适用边界与局限性

基于论文提供的证据和开放问题推断，MeshLAM的适用边界如下：

**已验证的能力边界**：
- 单张正面/近正面人脸图像输入，VFHQ数据集分布内的姿态和光照条件
- 支持表情驱动动画，通过FLAME模板的表情参数实现
- 可处理纹身、文字、妆容等高频纹理细节（Figure 2）
- 具备一定的跨域泛化能力，可适配文本到3D头像生成（Figure 3）

**推断的局限与未验证场景**（需人工验证）：
- **极端姿态鲁棒性**：论文未展示大幅度侧转、仰头/低头等极端姿态下的重建质量。FLAME模板的姿态空间覆盖范围可能成为瓶颈。
- **重度遮挡场景**：未评估口罩、墨镜、手部遮挡等情况下的鲁棒性。重投影机制依赖可见像素映射，遮挡区域可能产生纹理伪影。
- **真实场景泛化**：Figure 8展示了挑战性光照和遮挡的定性结果，但缺乏大规模真实场景的定量评估。
- **拓扑校正的稳定性**：在极端变形下，拓扑校正操作（长边细分、翻转面修正、无效面删除）对动画兼容性的影响未经充分测试。
- **迭代收敛的理论保证**：GRU解码的收敛性缺乏理论分析，迭代次数N=2的最优性可能依赖于训练数据分布。

### 6. 开放问题与后续方向

从方法设计和实验缺口可识别以下开放问题：

1. **表征扩展性**：UV纹理贴图分辨率（1024×1024）是否为性能瓶颈？更高分辨率能否进一步提升细节？该方法能否扩展到全身头像或包含身体的完整数字人重建？
2. **时序一致性**：当前方法逐帧独立重建，未利用视频输入的时序信息。引入时序约束可能进一步提升动画连贯性。
3. **计算效率的进一步优化**：0.7秒推理虽优于高斯方法，但相比纯单次回归方法仍有延迟。是否可以通过知识蒸馏将迭代GRU的渐进优化能力迁移到单次前向网络？
4. **与生成模型的融合**：Figure 3展示了文本到3D的初步适配，但该方向的定量评估和系统化研究尚未展开。MeshLAM的UV贴图表征天然适合作为扩散模型或GAN的生成目标。
5. **物理真实性**：当前方法未建模光照、次表面散射等物理效应，重建结果的外观一致性依赖于训练数据分布。引入物理渲染先验可能提升真实场景泛化能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Feed_Forward_One_Shot_Animatable_Textured_Mesh_Avatar_Reconstruction.pdf]]

---
title: "Neural Kernel Surface Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Neural_Kernel_Surface_Reconstruction.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/NKSR/
code_link: null
aliases:
- NKSRN
- NKSR
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入紧支撑核函数与层次化稀疏体素结构，将重建问题转化为稀疏梯度拟合（法向一致性约束），从而构建正定稀疏线性系统，可高效并行求解；同时，通过预测核特征场归纳几何先验，使模型在稀疏、噪声和分布外输入上保持高保真度。"
primary_logic: "利用层次化体素结构和紧支撑核函数，NKSR将3D表面重建形式化为在预测的核特征空间中求解稀疏线性系统，该系统融合了梯度（法向）约束与点位置约束，从而在保持泛化能力的同时，实现了可扩展的、对噪声鲁棒的重建。核函数的紧凑支撑与体素层级修剪协同作用，使求解规模与输入复杂度解耦，且无需预先计算SDF，可直接从任意稠密定向点云训练。"
claims:
- "NKSR通过紧支撑核和层次体素结构将线性系统稀疏化，可处理百万级点云"
- "梯度拟合损失使NKSR对噪声具有鲁棒性，避免了NKF在噪声下性能急剧下降"
- "消融实验证实层次结构和梯度约束对性能贡献显著"
- "NKSR在多个基准（对象、室内、室外）上达到最先进性能，且厨房水槽模型展示强泛化性"
---

# Neural Kernel Surface Reconstruction

> [!tip] 核心洞察
> 利用层次化体素结构和紧支撑核函数，NKSR将3D表面重建形式化为在预测的核特征空间中求解稀疏线性系统，该系统融合了梯度（法向）约束与点位置约束，从而在保持泛化能力的同时，实现了可扩展的、对噪声鲁棒的重建。核函数的紧凑支撑与体素层级修剪协同作用，使求解规模与输入复杂度解耦，且无需预先计算SDF，可直接从任意稠密定向点云训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 神经核表面重建 |
| 英文题名 | Neural Kernel Surface Reconstruction |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2305.19590) · [Project](https://research.nvidia.com/labs/toronto-ai/NKSR/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Kernel Surface Reconstruction (NKSR) |
| Dataset | ABC (σ=0), ABC (σ=0.05L), ShapeNet (3000 pts, σ=0.005, 含法向), CARLA (Outdoor, Novel subset) |

> [!tip] 效果简介
> - ABC (σ=0) 上，Chamfer距离 d_C ×10³ 为 3.68，对比 3.92 (NGSolver)，变化 -0.24。
> - ABC (σ=0.05L) 上，F-Score 为 73.2，对比 66.4 (NGSolver)，变化 +6.8。
> - ShapeNet (3000 pts, σ=0.005, 含法向) 上，IoU 为 94.3，对比 91.2 (NKF)，变化 +3.1。

## 概要

从定向点云重建3D表面是计算机视觉与图形学的基础问题。现有学习方法（如Neural Kernel Fields, NKF）虽具强泛化能力，但其全局核函数导致稠密线性系统，无法扩展至大规模点云（>10k点），且对输入噪声敏感——精确值插值约束缺乏对测量误差的容错。此外，这些方法需预计算占用/符号距离函数，限制了训练数据的多样性。

**Neural Kernel Surface Reconstruction (NKSR)** 针对上述瓶颈，提出三项关键改进：

1. **紧支撑核函数**：将NKF的全局核替换为在一体素邻域内衰减至零的紧支撑核，使线性系统稀疏化。
2. **梯度拟合目标**：以法向一致性约束替代精确位置值插值，增强对噪声的鲁棒性。
3. **层次化稀疏体素结构**：预测多级体素网格，实现多尺度表示与高效修剪。

三者协同作用，将3D表面重建形式化为在预测的核特征空间中求解稀疏正定线性系统，使求解规模与输入复杂度解耦，且无需预先计算SDF，可直接从任意稠密定向点云训练。

**核心结论**：NKSR在多个基准（单物体ABC/Thingi10K、ShapeNet、室内ScanNet/Matterport3D、室外CARLA）上达到最先进性能，尤其在噪声与分布外场景下优势显著。例如，在CARLA室外新场景上F-Score达96.0，较TSDF-Fusion提升15.3点；在ShapeNet上IoU达94.3，较NKF提升3.1点。消融实验证实，移除层次结构导致IoU下降1.0，移除梯度约束下降1.6，验证了设计要件的贡献。

**方法定位**：NKSR属于“学习先验 + 经典求解”的混合范式——利用神经网络预测核特征场以归纳几何先验，再通过稀疏线性求解器高效重建表面。这一设计使其兼具数据驱动的泛化能力与经典方法的可扩展性，在百万级点云（Waymo场景，1000万点，20秒）上仍可高效运行。



三维表面重建是计算机视觉与图形学中的核心问题，其目标是从离散的定向点云恢复连续、高保真的表面几何。该任务在自动驾驶、机器人导航、数字孪生和增强现实等应用中具有广泛需求。然而，现实世界的输入点云通常伴随噪声、稀疏采样和分布外场景，这对重建方法的泛化能力、可扩展性和鲁棒性提出了严峻挑战。

传统重建方法，如**SPSR**（Screened Poisson Surface Reconstruction），依赖手工设计的数学先验，在受控条件下表现良好，但对噪声敏感且缺乏数据驱动的几何先验。近年来，基于学习的方法试图从数据中归纳重建知识，但普遍面临以下瓶颈：

**瓶颈一：可扩展性不足。** 以**NKF**（Neural Kernel Fields）为代表的学习型核方法虽然展现了较强的泛化能力，但其全局核函数导致稠密线性系统，求解复杂度随点数超线性增长，无法扩展至大规模点云（>10k点）。这从根本上限制了其在真实大规模场景中的应用。

**瓶颈二：对噪声的脆弱性。** 现有学习方法多依赖精确的位置占用值或符号距离函数（SDF）作为监督信号，这种“精确值插值”约束缺乏对测量误差的容错机制。当输入点云含有噪声时，强制拟合噪声位置会导致重建质量急剧退化——NKF在噪声环境下性能的显著下降即为明证。

**瓶颈三：训练数据限制。** 主流学习方法（如ConvONet、POCO等）通常需要预计算的占用场或SDF作为训练监督，这不仅增加了数据准备的复杂度，也限制了可用的训练数据规模和多样性，削弱了模型在分布外场景下的泛化能力。

针对上述问题，**NKSR**（Neural Kernel Surface Reconstruction）提出了一个统一的解决方案。其核心动机在于：通过重新设计核函数的支撑域、拟合目标和空间表示结构，在保持学习型方法泛化优势的同时，实现可扩展、对噪声鲁棒的高保真重建。具体而言，NKSR引入紧支撑核函数与层次化稀疏体素结构，将重建问题转化为稀疏梯度拟合（法向一致性约束），从而构建正定稀疏线性系统，可高效并行求解。这一设计使求解规模与输入复杂度解耦，且无需预先计算SDF，可直接从任意稠密定向点云训练，为大规模、跨场景的通用表面重建开辟了新路径。



## 核心方法与创新机理

NKSR 相对于前身 NKF（Neural Kernel Fields）的核心创新并非简单的模块替换，而是一次系统性的重构：通过引入**紧支撑核函数**与**层次化稀疏体素结构**，将重建问题从“全局稠密插值”转化为“稀疏梯度拟合”，从而在保持强泛化能力的同时，一举突破了可扩展性、噪声鲁棒性和训练数据依赖三大瓶颈。

### 关键创新点与 Changed Slots

#### 1. 从全局核到紧支撑核：稀疏性的根本来源

NKF 使用的全局核函数导致 Gram 矩阵完全稠密，求解复杂度随点数二次增长，使其无法处理超过约 10k 点的点云。NKSR 的核心操作是将核函数调制为**紧支撑**形式：

$$
K_{\theta}^{(l)}(\mathbf{x}, \mathbf{x}') = \langle \phi_{\theta}^{(l)}(\mathbf{x}), \phi_{\theta}^{(l)}(\mathbf{x}') \rangle \cdot K_{\mathrm{b}}^{(l)}(\mathbf{x}, \mathbf{x}')
$$

其中 $K_{\mathrm{b}}^{(l)}$ 是二阶 B 样条乘积构成的 Bezier 核，在超出约 1.5 个体素宽度的邻域后严格衰减至零（见附录 A.2）。这一设计使得每个核基函数仅在其紧邻体素内非零，从而将线性系统 $( \mathbf{Q}^\top \mathbf{Q} + \mathbf{G}^\top \mathbf{G} ) \alpha = \mathbf{Q}^\top n$ 变为**稀疏正定**系统，可在 GPU 上用 Jacobi 预条件共轭梯度法高效求解（第 3.1 节）。

**因果机制**：紧支撑性并非孤立的数学技巧，而是与层次化体素结构深度协同——稀疏体素层次决定了核中心的分布密度，紧支撑核则限制了每个核的影响范围，两者共同将求解规模与输入点云规模解耦。

#### 2. 从精确值插值到梯度（法向）一致性拟合：噪声鲁棒性的来源

NKF 依赖精确的位置占用值约束，对输入点噪声高度敏感——噪声直接污染插值目标，导致隐式场在表面附近剧烈震荡。NKSR 将拟合目标从“点值逼近”切换为**梯度一致性**：

$$
\alpha^{*} = \arg \min \sum_{l,i} \|\nabla_x f_{\theta}(\mathbf{x}_i^{(l)}) - \mathbf{n}_i^{(l)}\|_2^2 + \sum_{j} |f_{\theta}(\mathbf{x}_j^{\mathrm{in}})|^2
$$

第一项强制隐式场梯度与输入法向对齐，第二项仅要求输入点处函数值为零，形成对测量误差具有容错性的最小二乘问题。由于法向是表面的一阶微分信息，对位置噪声的敏感度远低于零阶值约束。

**消融证据**：Figure 11 显示，移除梯度约束（仅用点值拟合）导致 IoU 下降 1.6，验证了梯度项对性能的实质性贡献。

#### 3. 层次化稀疏体素结构：多尺度与可扩展性的统一

NKF 使用单层点支撑的核场，缺乏空间层次，无法根据几何复杂度自适应分配表示能力。NKSR 通过稀疏卷积主干预测**多级体素网格**（L 层），每层体素携带特征和法向，核中心位于体素中点。这种层次结构带来三重增益：

- **多尺度表示**：粗层级捕捉全局拓扑，细层级恢复局部细节
- **自适应稀疏性**：仅在被占用的体素处放置核基函数，远离表面的区域不分配计算资源
- **可扩展性**：体素层次可随场景规模灵活调整，配合分块合并策略（out-of-core），可处理 Waymo 数据集中 1000 万+ 点的场景（Figure 9，20–35 秒重建）

**消融证据**：Figure 11 显示，移除层次结构（仅用最细层级）导致 IoU 下降 1.0，证实多尺度融合的必要性。

#### 4. 无需预计算 SDF：训练数据范式的突破

NKF 等先前学习方法需要预计算占用值或符号距离函数（SDF）作为监督信号，限制了训练数据的多样性和规模。NKSR 的梯度拟合损失直接以**稠密定向点云**为监督——只需从网格表面采样点和法向即可训练，无需昂贵的 SDF 预计算。这使得模型可以在 ABC、Thingi10K、ShapeNet、CARLA 等多个异构数据集上联合训练，形成“厨房水槽模型”（kitchen-sink model），展现出对分布外场景（如仅用 ShapeNet 训练后泛化到 ScanNet 室内场景，Table 4）的强泛化能力。

### 创新总结

| 维度 | NKF (Baseline) | NKSR (Proposed) | 因果机制 |
|------|----------------|-----------------|----------|
| 核支撑域 | 全局 → 稠密 Gram 矩阵 | 紧支撑 Bezier 核 → 稀疏正定系统 | 与层次体素协同，解耦求解规模与输入点数 |
| 拟合目标 | 精确位置值插值 | 梯度（法向）一致性 + 点零值约束 | 一阶微分约束对噪声具有天然鲁棒性 |
| 空间结构 | 单层点支撑 | 多级稀疏体素层次 | 多尺度表示 + 自适应计算分配 |
| 训练监督 | 需预计算占用/SDF | 直接使用稠密定向点云 | 降低数据准备成本，支持多域联合训练 |

这些创新并非独立叠加，而是围绕一个统一洞察展开：**将重建形式化为在预测的核特征空间中求解稀疏线性系统，用梯度约束取代值约束，用层次化紧支撑核取代全局核**。这一设计使 NKSR 在保持 NKF 强泛化性的同时，实现了对大规模、噪声和分布外输入的鲁棒可扩展重建。



NKSR 的整体 pipeline 遵循“编码—求解—提取”三阶段范式，将 3D 表面重建形式化为在预测的核特征空间中求解一个稀疏正定线性系统的过程。如 **Figure 3** 所示，系统接收含法向的点云作为输入，依次通过体素层次预测、核特征场构建、线性系统求解和表面提取四个核心模块，最终输出重建网格。

**输入与预处理**：方法接受一个定向点云 $\{X_{\mathrm{in}}, N_{\mathrm{in}}\}$，其中每个点包含三维坐标和对应的法向量。点云首先被体素化，并通过一个稀疏卷积主干网络（点编码器 + U-Net，详见 **Figure 12** 和 **Figure 13**）进行处理。

**体素层次预测**：主干网络输出一个多级稀疏体素层次结构（$L$ 层，典型值 $L=3$），每个体素携带两个关键信息：（1）一个 $d$ 维特征向量，用于后续构建核特征场；（2）一个预测的法向量，用于梯度拟合约束。体素的激活状态由结构预测模块决定，仅保留靠近表面的体素，形成稀疏表示（**Figure 14**）。

**核特征场构建**：对于层次中第 $l$ 层的每个体素中心 $\mathbf{x}_i^{(l)}$，通过 Bezier 插值与 MLP 将空间坐标映射到特征向量 $\phi_\theta^{(l)}(\mathbf{x})$。核函数定义为特征场内积与紧支撑 Bezier 核的乘积：

$$K_\theta^{(l)}(\mathbf{x}, \mathbf{x}') = \langle \phi_\theta^{(l)}(\mathbf{x}), \phi_\theta^{(l)}(\mathbf{x}') \rangle \cdot K_b^{(l)}(\mathbf{x}, \mathbf{x}')$$

其中 $K_b^{(l)}$ 为二阶 B 样条乘积构成的紧支撑核，在约 1.5 个体素邻域外衰减至零，保证后续线性系统的稀疏性。

**线性系统构建与求解**：隐式场 $f_\theta$ 表示为所有层次上核基函数的加权和（**Figure 4**）：

$$f_\theta(\mathbf{x}) = \sum_{i,l} \alpha_i^{(l)} K_\theta^{(l)}(\mathbf{x}, \mathbf{x}_i^{(l)})$$

系数 $\alpha$ 通过最小化梯度（法向）一致性损失与点位置零值约束来确定：

$$\alpha^* = \arg\min_\alpha \sum_{l,i} \|\nabla f_\theta(\mathbf{x}_i^{(l)}) - \mathbf{n}_i^{(l)}\|_2^2 + \sum_j |f_\theta(\mathbf{x}_j^{\mathrm{in}})|^2$$

该优化问题等价于求解稀疏正定线性系统：

$$(\mathbf{Q}^\top \mathbf{Q} + \mathbf{G}^\top \mathbf{G})\alpha = \mathbf{Q}^\top n$$

其中 $\mathbf{G}$ 为核函数值矩阵，$\mathbf{Q}$ 为核函数梯度矩阵。由于紧支撑核的局部性，该系统高度稀疏，可在 GPU 上使用 Jacobi 预条件共轭梯度法高效求解。

**掩码与表面提取**：一个额外的掩码模块 $\varphi: \mathbb{R}^3 \to \{0,1\}$ 预测空间点是否属于有效表面区域，用于修剪远离表面的虚假几何。最后，在体素角点处评估隐式场值，通过双行进立方体（Dual Marching Cubes）提取最终网格。

整个 pipeline 的关键特性在于：核函数的紧支撑性与层次体素修剪协同作用，使线性系统规模与输入复杂度解耦；梯度拟合目标替代了传统的位置精确插值，赋予方法对输入噪声的天然鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/001_Figure_1.jpg]]
*Figure 1: We present Neural Kernel Surface Reconstruction (NKSR) for recovering a 3D surface from an input point cloud. Trained directly from dense points, our method reaches state-of-the-art reconstruction quality and scalability. NKSR is also highly generalizable: All the meshes in this figure are reconstructed using a single trained model*



### 整体流水线

NKSR的推理流水线由三个核心模块串联构成（Figure 3）：**体素层次预测网络**从定向点云中预测稀疏的多级体素网格及其特征与法向；**核特征场构造**将体素中心的特征映射为紧支撑的正定核函数；**稀疏线性求解器**在核特征空间中求解一组每体素系数，最终通过双行进立方体（Dual Marching Cubes）提取零等值面。

### 体素层次预测网络

给定输入点云 $X_{\text{in}}$ 及其法向 $N_{\text{in}}$，首先通过稀疏卷积主干网络（U-Net架构，见Figure 13）预测 $L$ 层体素网格。每层 $l$ 的体素中心 $\mathbf{x}_i^{(l)}$ 携带 $d$ 维特征向量，用于后续构造核函数。网络同时预测每个体素的结构类别（Figure 14），决定该体素是否参与后续重建。此外，网络分支输出掩码模块 $\varphi: \mathbb{R}^3 \to \{0,1\}$，用于修剪远离预测表面的虚假几何区域。

### 核特征场构造

隐式场 $f_\theta$ 定义为分层核函数的加权和：

$$f_{\theta}(\mathbf{x} | X_{\text{in}}, N_{\text{in}}) = \sum_{i,l} \alpha_i^{(l)} K_{\theta}^{(l)}(\mathbf{x}, \mathbf{x}_i^{(l)} | X_{\text{in}}, N_{\text{in}}) \tag{1}$$

其中核函数 $K_{\theta}^{(l)}$ 分解为特征场内积与紧支撑Bezier核的乘积：

$$K_{\theta}^{(l)}(\mathbf{x}, \mathbf{x}') = \langle \phi_{\theta}^{(l)}(\mathbf{x}; \mathbf{X}_{\text{in}}, N_{\text{in}}), \phi_{\theta}^{(l)}(\mathbf{x}'; \mathbf{X}_{\text{in}}, N_{\text{in}}) \rangle \cdot K_{\mathrm{b}}^{(l)}(\mathbf{x}, \mathbf{x}') \tag{2}$$

**关键设计**：特征场 $\phi_{\theta}^{(l)}$ 通过Bezier插值与MLP将坐标映射到 $d$ 维特征空间，其内积 $\langle \phi_{\theta}^{(l)}(\mathbf{x}), \phi_{\theta}^{(l)}(\mathbf{x}') \rangle$ 构成正定核，捕获几何相似性。Bezier核 $K_{\mathrm{b}}^{(l)}$ 由三个二阶B样条乘积构成，在每体素的一环邻域内衰减至零（Appendix A.2），使每个核仅在一体素邻域内非零，从而保证整体线性系统稀疏。

### 系数优化与稀疏线性系统

系数 $\alpha_i^{(l)}$ 通过最小化以下损失求得：

$$\alpha^{*} = \arg \min_{\alpha_i^{(l)}} \sum_{l=1}^{L'} \sum_{i=1}^{n^{(l)}} \|\nabla_x f_{\theta}(\mathbf{x}_i^{(l)}) - \mathbf{n}_i^{(l)}\|_2^2 + \sum_{j=1}^{n_{\text{in}}} |f_{\theta}(\mathbf{x}_j^{\text{in}})|^2 \tag{3}$$

该损失包含两项：第一项强制隐式场梯度与预测法向一致（**梯度拟合**），第二项约束输入点位于零等值面附近（**点位置零值约束**）。与NKF的精确位置占用值插值不同，NKSR以法向一致性为主导，使模型对输入噪声具有显著鲁棒性。

将公式(1)代入公式(3)，得到法方程形式的线性系统：

$$(\mathbf{Q}^{\top} \mathbf{Q} + \mathbf{G}^{\top} \mathbf{G}) \alpha = \mathbf{Q}^{\top} n \tag{4}$$

其中 $\mathbf{G}$ 和 $\mathbf{Q}$ 分别为核函数值和梯度构成的Gram矩阵块：

$$\mathbf{G}_{i,j}^{(l)} = K_{\theta}(\mathbf{x}_i^{\text{in}}, \mathbf{x}_j^{(l)}), \quad \mathbf{Q}_{i,j}^{(l)} = \partial_{\mathbf{x}_i^{(l')}} K_{\theta}(\mathbf{x}_i^{(l')}, \mathbf{x}_j^{(l)}) \tag{6}$$

**系统性质**：由于紧支撑核 $K_{\mathrm{b}}^{(l)}$ 的调制，矩阵 $\mathbf{Q}^{\top} \mathbf{Q} + \mathbf{G}^{\top} \mathbf{G}$ 是稀疏的；且因源自Gram矩阵，该矩阵正定（3.1节）。系统采用Jacobi预条件共轭梯度法在GPU上高效求解，求解规模与输入复杂度解耦，可处理百万级点云。

### 训练监督

模型端到端训练，总损失包含四项（4. Experiments节）：
- **TSDF损失**：监督隐式场在稠密采样点处的截断符号距离值；
- **法向损失**：监督隐式场梯度与真实法向的一致性；
- **外部损失**：约束远离表面的空间点具有较大有符号距离值；
- **最小表面损失** $\mathcal{L}_{\text{surf}}(f) = \mathbb{E}_{\mathbf{x} \in X_{\text{dense}}} [\|f(\mathbf{x})\|_1]$：确保隐式场在真实表面附近趋近于零。

训练直接使用稠密定向点云作为监督，无需预计算占用场或SDF，从而支持更大规模、更多样化的训练数据。



## 实验与关键发现

### 核心性能验证

NKSR在多个重建基准上取得了最先进的结果，覆盖了从单一物体到室内外大场景的广泛范围。**Table 1** 展示了在ABC/Thingi10K数据集上的定量对比。在无噪声（σ=0）条件下，NKSR的Chamfer距离（$d_C \times 10^3$）为3.68，优于NGSolver的3.92；在高噪声（σ=0.05L）条件下，NKSR的F-Score达到73.2，显著超越NGSolver的66.4，体现了其梯度拟合损失对噪声的鲁棒性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/007_Table_1.jpg]]
*Table 1: ABC/Thingi10K [36, 79] comparison. d _ { C } is multiplied by 1 0 ^ { 3 } . . σ is the Gaussian noise added to the sensor depth and L is the largest box length. 10 scans are used to accumulate the point cloud unless specified*

**Table 2** 报告了ShapeNet数据集上的结果。在3000点、σ=0.005噪声且含输入法向的设置下，NKSR的IoU达到94.3，较直接前身NKF的91.2提升了3.1个百分点。值得注意的是，即使在无输入法向的变体中，NKSR依然保持了竞争力，验证了其通过核特征场归纳几何先验的能力。

在室外场景上，**Table 3** 显示NKSR在CARLA数据集的Novel子集上F-Score高达96.0，远超TSDF-Fusion的80.7，提升幅度达15.3个百分点。这不仅体现了泛化能力，也凸显了传统融合方法在稀疏、噪声室外数据上的局限性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/009_Table_3.jpg]]
*Table 3: CARLA [17] comparison. d _ { C } is the average of Acc. and Comp. (Unit is cm. The smaller the better.)*

对于室内场景，**Table 4** 表明，即使在仅用ShapeNet训练的条件下，NKSR在ScanNet上的Chamfer距离（$d_C \times 10^3$）为2.68，远优于DOGNN的4.93。这一跨域泛化能力源于核特征场学习到的通用几何先验，而非对特定数据分布的记忆。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/012_Table_4.jpg]]
*Table 4: Room-level dataset [12, 5] comparison. d _ { C } is multiplied by 1 0 ^ { 3 } Chamfer distance that reflects reconstruction accuracy (Acc.) and completeness (Comp.). We additionally report average running times for each method on the datasets. The mean/min/max number of input points in this setting are 490k/290k/820k. Compared to ours, SPSR is quite sensitive to the noise and sparsity in the input, leaving bumpy and incomplete geometries. Although POCO could reach a similar completeness value, the fitted surfaces fail to faithfully respect the input. The long running time (161x slower than ours) also prohibits POCO from practical use*

### 消融研究：层次结构与梯度约束的因果贡献

**Figure 11** 的消融实验直接验证了核心设计选择的因果效应。移除层次结构（仅使用最细层级）导致IoU下降1.0，证实了多尺度体素层次对捕捉不同粒度几何特征的关键作用。移除梯度约束（即仅用点值拟合）导致IoU下降1.6，这一更大的性能衰减揭示了法向一致性约束在构建鲁棒隐式场中的核心地位——它使系统对输入点位置噪声不敏感，避免了NKF在噪声下性能急剧下降的问题。

### 扩展能力与失败模式

NKSR展示了显著的扩展能力。**Figure 9** 显示，厨房水槽模型（多数据集联合训练）可在Waymo数据集上以核外方式处理1000万至1100万点的大规模场景，分别仅需20秒和35秒。**Figure 10** 和 **Table 5** 进一步验证了模型对不同输入密度的泛化能力，在1.5m/scan至15m/scan的稀疏度变化下保持稳定的F-Score。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/013_Figure_9.jpg]]
*Figure 9: Application to Waymo [57] dataset. We run our kitchen-sink-model in an out-of-core manner (see Appendix for implementation details) to scale to very large scenes consisting of 10M / 11M (left / right) points, taking only 20s / 35s*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/015_Table_5.jpg]]
*Table 5: Performance comparison using different input densities. Here the F-Score ↑ metric is shown*

然而，分析揭示了若干失败模式：
- **领域自适应不足**：厨房水槽模型在特定领域上的性能略低于领域专用模型，说明联合训练尚未完全消除领域偏差。
- **内存线性增长**：超大场景仍需分块合并策略，内存占用随场景规模线性增长，限制了端到端城市级重建。
- **训练数据依赖**：模型训练依赖于稠密定向点云作为监督，对于仅有稀疏点或无定向信息的数据集可能无法直接训练。
- **核函数容量限制**：当前核函数维度固定，可能未能充分利用更高阶的几何特征，这在高曲率区域可能表现为细节丢失。

### 关键图表结论

- **Figure 3** 的流水线图揭示了NKSR的核心机制：从点云到体素层次预测，再到稀疏线性系统构建与求解，最终通过双行进立方体提取表面。整个流程将重建问题转化为在预测的核特征空间中求解稀疏正定系统。
- **Figure 4** 直观展示了隐式场作为体素层次上核基函数之和的表示，每个体素中心的核基函数仅在其一环邻域内非零，这是稀疏性的根源。
- **Figure 15** 的核可视化提供了对学习到的几何先验的洞察：PCA显示特征在不同几何区域呈现结构化分布，相似度热力图表明核函数捕捉了局部几何相似性，水平集则展示了紧支撑核的局部影响范围。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/006_Figure_5.jpg]]
*Figure 5: ABC/Thingi10K [36, 79] visualization. Figure 6: ShapeNet [6] visualization. The two shapes are with $\sigma$ = 0 . 0 0 5 and $\sigma$ = 0 . 0 2 5 Gaussian noise respectively

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/016_Figure.jpg]]
*Figure: Voxel size (×0.01)*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/008_Table_2.jpg]]
*Table 2: ShapeNet [6] comparison. $\mathbf { \omega } ^ { \prime } \mathbf { N } . \mathbf { \omega }$ denotes whether normals $N _ { \mathrm { i n } }$ are used as input. $d _ { C }$ is multiplied by 1 $0 ^ { 3 }$

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/017_Figure_11.jpg]]
*Figure 11: Ablation study. IoU metric is shown. The back arrows indicate the setting we use to obtain Tab. 2*


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2305_19590/figures/024_Table_7.jpg]]
*Table 7: Dataset specifications for CARLA*



## 定位与知识库关联

### 1. 与基线方法的关系

NKSR 的直接前身是 **Neural Kernel Fields (NKF)**，后者首次将核方法引入学习的3D重建中，通过学习全局核函数对点云进行插值。NKF 的核心瓶颈在于其全局支撑域导致 Gram 矩阵完全稠密，求解复杂度随点数呈立方增长，无法处理超过 10k 点的输入；同时，NKF 依赖精确的位置占用值约束，对输入噪声极为敏感——在噪声增加时性能急剧退化（Table 1, Table 2 中 NKF 在噪声场景下的指标显著下降）。NKSR 对 NKF 进行了三个关键改造：

1. **核函数支撑域从全局改为紧支撑**：引入可分离的 Bezier 核 $K_{\mathrm{b}}^{(l)}$（见附录 A.2 的 $\psi^2(s)$ 定义，在一体素邻域外严格为零），使 Gram 矩阵稀疏化。
2. **拟合目标从精确值插值改为梯度一致**：将优化目标重构为 $\alpha^{*} = \arg\min \sum \|\nabla f - \mathbf{n}\|_2^2 + \sum |f(\mathbf{x}^{\mathrm{in}})|^2$（公式3），优先满足法向一致性而非精确位置值，从而对噪声具有天然容错。
3. **引入层次化稀疏体素结构**：替代 NKF 的单层点支撑，预测多级体素网格，使核中心分布于多尺度空间，实现从粗到细的重建。

在经典重建方法谱系中，**SPSR (Screened Poisson Surface Reconstruction)** 是最具代表性的传统基准。SPSR 通过求解全局 Poisson 方程进行重建，具有坚实的数学基础，但缺乏数据驱动的几何先验，在稀疏、噪声或分布外输入上保真度有限。NKSR 可视为将 Poisson 重建的梯度拟合思想与学习的核特征空间进行了融合——公式(3)中的法向一致性项本质上是离散的梯度拟合，而特征场 $\phi_{\theta}$ 则提供了数据驱动的核函数设计。

与其他学习方法相比：

- **POCO**（基于 Transformer 的占用场方法）和 **ConvONet**（卷积占用网络）依赖预计算的占用值/SDF 作为监督，限制了训练数据的多样性和规模。NKSR 直接从稠密定向点云训练，无需预计算 SDF。
- **NGSolver (Neural Galerkin Solver)** 使用可学习基函数，在 ABC 数据集上表现接近 NKSR（Table 1: Chamfer 距离 3.92 vs 3.68），但其方法在噪声场景下（$\sigma=0.05L$）F-Score 仅 66.4，远低于 NKSR 的 73.2，说明梯度拟合策略对噪声鲁棒性的贡献是独立的。
- **SAP (Shape as Points)** 和 **TSDF-Fusion** 分别代表基于上采样+Poisson 重建和传统融合的方法，在 CARLA 室外场景中 F-Score 分别为 92.0 和 80.7，均低于 NKSR 的 96.0（Table 3），且 TSDF-Fusion 需放宽体素尺寸至 30cm 以保证完整性。

### 2. 适用边界与局限

**适用场景**：NKSR 在以下条件下表现最佳：
- 输入为含法向的定向点云（或可通过网络预测法向的变体，见 Table 2 中"w/o N."设置）
- 点云密度从稀疏（3000点）到超大规模（千万点）均可处理
- 场景类型覆盖单一物体（ShapeNet）、室内空间（ScanNet/Matterport3D）和室外环境（CARLA/Waymo）

**已知局限**：

1. **领域自适应差距**：厨房水槽模型（多数据集联合训练）在特定领域上的性能略低于领域专用模型。如 Table 1 中，专门在 ABC 上训练的模型 Chamfer 距离为 3.68，而通用模型在特定子集上可能略有下降，说明领域自适应仍有提升空间。

2. **超大场景的内存瓶颈**：对于 Waymo 数据集中千万点级别的场景（Figure 9），仍需采用分块合并策略（out-of-core），内存占用随场景规模线性增长。Figure 16 展示了分块加权平均的拼合机制，但这一过程引入了额外的工程复杂度和潜在的拼合伪影。

3. **训练数据依赖**：模型训练依赖稠密定向点云作为监督（3.2节中的 $\mathcal{L}_{\mathrm{surf}}$ 等损失函数均需稠密真值点），对于仅有稀疏点或无定向信息的数据集可能无法直接训练。虽然推理阶段可处理稀疏输入，但训练阶段的数据要求限制了可用的训练数据范围。

4. **核函数表达力上限**：当前核函数维度固定（通过 MLP 将坐标映射到 $d$ 维特征空间），可能未能充分利用更高阶的几何特征。Figure 15 的核可视化显示核函数在局部区域内表现出一定的几何感知能力，但维度限制可能制约了对复杂几何细节的捕捉。

### 3. 开放问题

1. **深度核网络的可能性**：当前核函数 $K_{\theta}^{(l)}(\mathbf{x}, \mathbf{x}') = \langle \phi_{\theta}^{(l)}(\mathbf{x}), \phi_{\theta}^{(l)}(\mathbf{x}') \rangle \cdot K_{\mathrm{b}}^{(l)}(\mathbf{x}, \mathbf{x}')$ 采用简单的特征场内积结构。是否可通过更复杂的核模型（如深度核网络、注意力机制增强的核函数）进一步提升重建精度，同时保持线性系统的稀疏性和正定性？

2. **端到端城市级重建**：当前分块合并策略（Figure 16）虽可扩展至千万点，但内存占用仍线性增长。如何通过层次化求解、自适应体素修剪或增量式求解策略，实现更大规模（如城市级）的端到端重建，避免分块带来的拼合开销？

3. **多信号联合重建**：Figure 17 展示了将 NKSR 扩展到纹理重建的初步尝试（800次迭代优化颜色），Figure 18 展示了离群点检测能力。是否可将 NKSR 框架系统性地扩展到颜色、语义、材质等多信号的联合重建，利用核特征场的共享表示实现多任务协同？

4. **实时 SLAM 系统集成**：NKSR 的线性求解器使用 Jacobi 预条件共轭梯度法在 GPU 上求解，对于中等规模场景已具备较高效率（Waymo 千万点场景 20-35 秒）。是否可通过增量式求解（利用前一帧的解作为当前帧的初始值）和自适应体素更新策略，将 NKSR 嵌入实时 SLAM 系统，实现在线重建？

5. **无监督/自监督训练**：当前训练依赖稠密定向点云监督。是否可通过可微渲染损失或一致性约束，降低对真值点云的依赖，使模型能够从原始扫描数据或 RGB-D 序列中自监督学习？



## 原文 PDF

![[paperPDFs/CVPR_2023/Neural_Kernel_Surface_Reconstruction.pdf]]

---
title: "Anatomica: Localized Control over Geometric and Topological Properties for Anatomical Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Anatomica_Localized_Control_over_Geometric_and_Topological_Properties_for_Anatomical_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/jmclong/random-fourier-featurespytorch"
aliases:
- Anatomica
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 推理时引导与局部化控制域的结合：通过立方体控制域切片局部子结构，利用可微分几何矩和持久同调测量属性，并使用梯度引导反向扩散过程，从而在无需重新训练的情况下实现精确的局部几何与拓扑控制。
primary_logic: 将可微分的几何矩和持久同调与基于控制域的子结构解析（V-parsing / L-parsing）相结合，可以在推理时对解剖扩散模型施加精确的局部几何和拓扑约束，实现组合式、多尺度的解剖结构控制。
claims:
- Anatomica是一个推理时框架，能够生成具有局部几何-拓扑控制的多类解剖体素图。
- 通过立方体控制域提取局部子结构，并计算可微分惩罚函数来引导采样。
- 几何特征通过体素矩控制，拓扑特征通过持久同调强制实现。
- 神经场解码器允许从潜在空间直接部分解析子结构，提高效率。
---

# Anatomica: Localized Control over Geometric and Topological Properties for Anatomical Diffusion Models

> [!tip] 核心洞察
> 将可微分的几何矩和持久同调与基于控制域的子结构解析（V-parsing / L-parsing）相结合，可以在推理时对解剖扩散模型施加精确的局部几何和拓扑约束，实现组合式、多尺度的解剖结构控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | Anatomica：解剖扩散模型的几何与拓扑属性局部控制 |
| 英文题名 | Anatomica: Localized Control over Geometric and Topological Properties for Anatomical Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20587) · [Code](https://github.com/jmclong/random-fourier-featurespytorch) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | Anatomica |
| Dataset | Cardiac (TotalSegmentator) – Right Ventricle Task, Cardiac (TotalSegmentator) – Atrial Separation Task, Aortic Branch – Branch Connectivity Task |

> [!tip] 效果简介
> - Cardiac (TotalSegmentator) – Right Ventricle Task 上，Mass Fidelity (×1e5, ↓) 17.5 (Anatomica-L) vs 154.5 (Explicit Conditioning) (-137.0)；FMD (↓) 93.7 (Anatomica-L) / 84.9 (Anatomica-V) vs 164.7 (Explicit Conditioning) (-71.0 / -79.8)。
> - Cardiac (TotalSegmentator) – Atrial Separation Task 上，B0 Precision (%, ↑) 78.9 (Anatomica-L) vs 7.81 (Unconditional) (+71.09)。
> - Aortic Branch – Branch Connectivity Task 上，B0 Precision (%, ↑) 77.3 (Anatomica-L) vs 55.5 (Unconditional) (+21.8)。

## 概述

现有解剖生成模型（如显式/隐式条件扩散模型）在生成过程中面临一个核心瓶颈：难以对局部解剖结构的几何属性（大小、形状、位置）和拓扑属性（连通分量、环、空洞）施加精确、可微分的控制。传统方法依赖条件训练，将几何属性编码为标量信号或3D热图输入模型，缺乏直观的局部编辑能力，且无法在推理时灵活组合不同的几何-拓扑约束。

**Anatomica** 是一个推理时引导框架，其核心洞察在于：将可微分的几何矩（质量、质心、协方差）和持久同调（persistent homology）与基于立方体控制域的子结构解析相结合，可以在无需重新训练的情况下，对预训练的解剖扩散模型施加精确的局部几何和拓扑约束。具体而言，该方法通过立方体控制域（cuboidal control domains）定义感兴趣区域，利用 V-parsing（体素空间解析）或 L-parsing（潜在空间解析）提取局部子结构，然后计算可微分的几何与拓扑惩罚函数，并通过梯度引导反向扩散过程，实现组合式、多尺度的解剖结构控制。

在方法定位上，Anatomica 与显式条件（Explicit Conditioning）和隐式条件（Implicit Conditioning）基线形成鲜明对比：前者将控制方式从条件训练转变为推理时梯度引导，并引入了子结构解析策略（V-parsing / L-parsing），后者不具备此类局部化解析能力（见 Table 1）。该框架的核心模块包括控制域定义、子结构解析、几何测量（体素矩）、拓扑测量（持久同调）、势函数设计以及梯度引导去噪（见 Figure 2, Figure 3）。

主要实验结果表明：在心脏几何控制任务（TotalSegmentator 右心室）中，Anatomica-L 的质量保真度（Mass Fidelity）达到 17.5（×1e5），相比显式条件的 154.5 降低了 137.0；FMD 达到 93.7，优于显式条件的 164.7（见 Table 2）。在拓扑控制任务中，心房分离任务的 B0 精度从无条件基线的 7.81% 提升至 78.9%（Anatomica-L），主动脉分支连接任务的 B0 精度从 55.5% 提升至 77.3%（见 Table 3）。消融研究表明，解耦的几何引导（仅质心损失）即可达到与全损失相当的质心保真度，且不影响生成质量（Figure 8）；部分解码分辨率在 64³ 时提供了 11 倍的加速比，是保真度与速度的良好折衷（Figure 10, Table 13）。

该方法的局限性在于拓扑引导的计算开销较大（每样本约 420 秒），主要受限于持久同调缺乏公开的 GPU 实现；曲线控制域的骨架化步骤仍在 CPU 上执行；且仅在有限解剖数据集（心脏、主动脉、脊柱、冠状动脉）上验证，泛化性有待进一步检验。

## 背景与动机

### 解剖生成模型的现状与瓶颈

医学影像中解剖结构的自动生成是虚拟临床试验、数据增强和手术规划的关键技术。近年来，扩散模型在三维解剖体素图的生成上取得了显著进展，能够合成逼真的多类组织分割。然而，现有方法面临一个核心瓶颈：**难以在生成过程中对解剖结构的几何特征（大小、形状、位置）和拓扑特征（连通分量、环、空洞）施加局部化、可微分的精确控制**。

传统方法依赖条件训练（conditional training），将几何属性作为标量条件信号输入扩散模型（显式条件），或通过三维热图间接编码（隐式条件）。这些方法存在两个根本缺陷：一是控制粒度粗糙，无法针对特定解剖子结构进行局部编辑；二是缺乏直观的交互手段，用户难以在推理时动态调整生成结果。此外，拓扑特征——如血管的连通性、心腔的分隔状态——在条件训练范式中几乎无法被显式约束，导致生成样本在解剖合理性上存在严重缺陷。

### 核心动机：从全局条件到局部推理时引导

本文的核心动机是**将解剖生成的控制范式从“训练时条件注入”转变为“推理时可微分引导”**。具体而言，Anatomica 框架旨在实现以下三个目标：

1. **局部化控制**：通过立方体控制域（cuboidal control domains）精确定义感兴趣的子结构区域，支持笛卡尔、曲线、球面、柱面等多种坐标系，实现对任意解剖部位的独立编辑。
2. **几何-拓扑联合约束**：利用可微分的体素矩（voxel-wise moments）测量子结构的质量、质心和协方差矩阵，同时引入持久同调（persistent homology）来强制连通分量数（$B_0$）、环数（$B_1$）和空洞数（$B_2$）等拓扑先验。
3. **免重训练部署**：所有控制信号通过梯度反向传播注入扩散模型的去噪过程，无需修改或重新训练基础生成模型，即可在推理时实现组合式、多尺度的解剖属性控制。

### 方法定位与创新边界

与现有工作相比，Anatomica 在三个维度上实现了突破：

- **控制方式**：从条件训练（显式/隐式）转向推理时梯度引导，使控制与生成解耦。
- **子结构解析**：提出 V-parsing（体素空间解析）和 L-parsing（潜在空间解析）两种策略，前者通过布尔子集算子和体素切片提取子结构，后者直接从潜在网格切片并用神经场解码器解码，避免了完整体素重建的计算开销。
- **拓扑可控性**：首次将持久同调引入解剖扩散模型的推理时控制，通过保留/抑制损失函数最大化或最小化特定拓扑特征的持久性，实现了对连通性、环状结构和空洞的精确操纵。

这些创新使 Anatomica 成为首个能够在推理时对多类解剖体素图施加局部几何-拓扑联合控制的框架，为解剖生成模型的临床落地提供了新的技术路径。

## 核心创新

Anatomica 的核心创新在于将**推理时引导**与**局部化控制域**相结合，在无需重新训练扩散模型的前提下，实现对解剖体素图几何属性与拓扑属性的精确、局部化、可微分控制。与依赖条件训练的传统方法相比，这一范式转变带来了三个关键维度的改变。

### 从条件训练到推理时引导

现有解剖生成模型通常将几何属性（如大小、位置）作为条件信号输入扩散模型进行训练：**Explicit Conditioning** 将属性编码为标量条件，**Implicit Conditioning** 则通过 3D 热图间接编码。这两种方式均需在训练阶段固化控制能力，且缺乏对局部子结构的直观编辑手段。

Anatomica 将控制完全移至推理阶段。在每个去噪步骤中，利用解剖势函数的梯度修正无条件去噪输出，形成引导去噪：

$$D_\theta^w(\mathbf{z}_\sigma; \sigma) = D_\theta(\mathbf{z}_\sigma; \sigma) - \sigma^2 \cdot \nabla_{\mathbf{z}_\sigma} \mathcal{L}$$

这一设计使模型无需针对特定控制任务重新训练，即可在采样过程中动态施加几何与拓扑约束。

### 控制域驱动的子结构解析

Anatomica 引入**立方体控制域**来定义局部感兴趣区域，支持全局、笛卡尔、界面、曲线、球面、柱面等多种坐标系，通过仿射变换将模板点网格定位到目标区域：

$$\mathbf{X}_k = \mathbf{R}_k \,\mathrm{diag}(\mathbf{s}_k)\, \mathbf{X}_k^{\mathrm{temp}} + \mathbf{t}_k$$

在此基础上，框架提供两种子结构解析策略：
- **V-parsing**：在体素空间先通过布尔子集算子选择组织通道，再用体素切片算子提取局部子结构；
- **L-parsing**：直接从潜在空间切片并利用神经场解码器部分解码，避免完整体素重建，显著提升效率。

### 可微分几何-拓扑联合测量

Anatomica 将几何矩与持久同调统一为可微分惩罚函数，实现了对局部解剖属性的精确量化与控制：

- **几何控制**：通过 0 阶矩（质量）、1 阶矩（质心）和 2 阶矩（协方差）可微地测量子结构的大小、形状和方向，并以加权 MSE 损失驱动：

$$\mathcal{L}_k^{\mathrm{geo}} = \lambda_0 \mathcal{L}_{\mathrm{MSE}}(m_k, \bar{m}_k) + \lambda_1 \mathcal{L}_{\mathrm{MSE}}(\mathbf{p}_k, \bar{\mathbf{p}}_k) + \lambda_2 \mathcal{L}_{\mathrm{MSE}}(\Sigma_k^n, \bar{\Sigma}_k^n)$$

- **拓扑控制**：利用持久同调（Cubical Ripser）提取子结构的连通分量（$B_0$）、环（$B_1$）和空洞（$B_2$），通过最大化保留集持久性和最小化抑制集持久性来强制拓扑先验：

$$\mathcal{L}_k^{\mathrm{topo}} = - \sum_{p \in \mathcal{V}_k} |\mathbf{S}_k(r_b^p) - \mathbf{S}_k(r_d^p)|^2 + \sum_{p \in \mathcal{Z}_k} |\mathbf{S}_k(r_b^p) - \mathbf{S}_k(r_d^p)|^2$$

这种联合测量机制使 Anatomica 能够在统一的推理时框架下，同时精确控制解剖结构的几何形态与拓扑连通性，实现了现有方法无法达成的组合式、多尺度解剖控制能力。

## 整体框架

Anatomica 是一个**推理时组合式扩散引导框架**，用于生成具有局部化几何与拓扑控制的多类三维解剖体素图。其核心设计理念是：在不重新训练基础扩散模型的前提下，通过在反向采样过程中注入可微分的解剖势函数梯度，实现对生成结构的大小、形状、位置（几何属性）以及连通分量、环、空洞（拓扑属性）的精确控制。

### 框架流水线

整个框架由五个核心模块串联而成，形成一条从“控制域定义”到“梯度引导去噪”的闭环流水线：

1.  **控制域定义**：用户通过立方体控制域指定感兴趣区域。框架支持笛卡尔、曲线、球面、柱面等多种坐标系，通过仿射变换将模板点网格定位到目标解剖位置。
2.  **子结构解析**：从当前扩散状态中提取控制域内的局部子结构。框架提供两种策略——**V-parsing**（先解码为完整体素图再切片）和 **L-parsing**（直接从潜在空间切片并用神经场解码器局部解码）。
3.  **属性测量**：对提取的子结构进行可微分的几何测量（体素矩：质量、质心、协方差）和拓扑测量（持久同调，提取 Betti 特征）。
4.  **势函数构建**：将测量值与用户指定的目标属性比较，构建解剖势函数——几何势函数采用加权 MSE 损失，拓扑势函数通过最大化保留集持久性、最小化抑制集持久性来强制拓扑先验。
5.  **梯度引导去噪**：在每个采样步骤中，用势函数关于当前潜在变量的梯度修正无条件去噪输出，实现引导去噪。

### 输入输出与数据流

-   **输入**：用户定义的控制域参数（位置、尺寸、方向、组织类别）及目标属性（目标几何椭球或目标拓扑先验）。
-   **核心过程**：从随机噪声 $`\mathbf{z}_\sigma`$ 出发，沿反向扩散轨迹迭代。每步先由 U-Net 去噪器 $`D_\theta`$ 预测干净潜在 $`\hat{\mathbf{z}}_0`$，再通过子结构解析提取局部体素，计算势函数梯度 $`\nabla_{\mathbf{z}_\sigma} \mathcal{L}`$，最终修正去噪方向：
    $$D_\theta^w(\mathbf{z}_\sigma; \sigma) = D_\theta(\mathbf{z}_\sigma; \sigma) - \sigma^2 \cdot \nabla_{\mathbf{z}_\sigma} \mathcal{L}$$
-   **输出**：满足局部几何与拓扑约束的多类解剖体素图。

### 关键设计决策

框架的灵活性体现在三个方面：其一，**组合式引导**允许同时施加多个控制域的几何/拓扑约束，各势函数独立计算后梯度可累加；其二，**L-parsing 策略**利用神经场解码器的连续性，支持任意分辨率的局部解码，在保真度与计算效率之间提供可调节的权衡；其三，**控制域与测量模块解耦**，使得同一框架可适配从全局器官到局部亚结构的多种控制任务。

这种设计使得 Anatomica 区别于传统的条件训练方法——后者需要将几何属性编码为条件信号并重新训练模型，而 Anatomica 将控制逻辑完全外置于推理阶段，实现了零训练成本的局部化解剖属性编辑。

### 补充图表

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/001_Figure_1.jpg]]
*Figure 1: Anatomica is a compositional diffusion-guidance framework for generating segmentations based on anatomical features that are localized within cuboidal control domains. Left: We generate voxel maps according to localized target geometry (size, shape, and position) visualized as red ellipsoids. Right: We generate voxel maps according to target topology (components, loops, and voids)*

## 核心模块与公式推导

Anatomica 的核心由四个关键模块串联构成，形成“定义控制域 → 解析子结构 → 测量属性 → 引导采样”的闭环。

### 1. 控制域定义

控制域通过一个可学习的仿射变换，将标准化的立方体模板点网格 $\mathbf{X}_k^{\mathrm{temp}}$ 映射到体素空间中的任意感兴趣区域：

$$
\mathbf{X}_k = \mathbf{R}_k \, \mathrm{diag}(\mathbf{s}_k) \, \mathbf{X}_k^{\mathrm{temp}} + \mathbf{t}_k
$$

其中 $\mathbf{R}_k$ 为旋转矩阵，$\mathbf{s}_k$ 为各向异性缩放因子，$\mathbf{t}_k$ 为平移向量。该变换支持笛卡尔、曲线、柱面、球面等多种坐标系，使控制域能够贴合不同解剖结构的自然形态（如沿血管走向的曲线域、包裹心脏的球面域）。

### 2. 子结构解析

从生成过程中提取局部子结构是施加局部约束的前提。Anatomica 提供两种互补的解析策略：

**V-parsing（体素空间解析）** 先在完整预测体素图 $\hat{\mathbf{V}}$ 上应用布尔子集算子 $\mathcal{U}[\mathbf{u}]$ 选择目标组织通道，再通过体素切片算子 $\mathcal{T}^s[\mathbf{X}_k]$ 提取控制域内的子结构：

$$
\mathbf{S}_k = \mathcal{T}^s[\mathbf{X}_k] \circ \mathcal{U}[\mathbf{u}](\hat{\mathbf{V}})
$$

**L-parsing（潜在空间解析）** 则直接从去噪后的潜在预测 $\hat{\mathbf{z}}_0$ 出发，利用神经场解码器 $\mathcal{F}$ 和潜在切片算子 $\mathcal{T}^l$ 在局部区域解码，避免完整体素重建：

$$
\mathbf{S}_k = \mathcal{U}[\mathbf{u}] \mathcal{F}[\mathbf{X}_k] \circ \mathcal{T}^l[\mathbf{X}_k](\hat{\mathbf{z}}_0)
$$

L-parsing 是 Anatomica 高效性的关键：粗粒度 L-parsing 使用低分辨率网格进行全局快速估计，局部化 L-parsing 则仅在高分辨率下解码控制域附近区域，在保真度与速度之间取得平衡。

### 3. 可微分属性测量

**几何测量** 基于体素矩实现。对子结构 $\mathbf{S}_k$ 的每个体素赋予概率权重 $\Omega_k$，计算其质量（0 阶矩）、质心（1 阶矩）和协方差矩阵（2 阶矩）：

$$
m_k = \mathbf{1}^T \cdot \Omega_k, \quad
\mathbf{p}_k = \frac{\Omega_k^T \mathbf{r}_k}{m_k}, \quad
\Sigma_k = \frac{1}{m_k} \mathbf{r}_k^T \text{diag}(\Omega_k) \mathbf{r}_k - \mathbf{p}_k \mathbf{p}_k^T
$$

其中 $\mathbf{r}_k$ 为控制域内的坐标网格。协方差矩阵可进一步分解为大小（特征值）、形状（归一化特征值比）和方向（特征向量），实现对结构几何的精细刻画。

**拓扑测量** 使用持久同调（persistent homology）捕捉子结构的连通分量（$B_0$）、环（$B_1$）和空洞（$B_2$）。通过超水平集过滤生成持久性图，每个点 $(r_b^p, r_d^p)$ 表示一个拓扑特征出生和消亡的强度阈值。

### 4. 势函数与引导

将测量值转化为可微的势函数，用于驱动反向扩散过程。

**几何势函数** 采用加权 MSE 损失，惩罚与目标质量 $\bar{m}_k$、质心 $\bar{\mathbf{p}}_k$ 和归一化协方差 $\bar{\Sigma}_k^n$ 的偏差：

$$
\mathcal{L}_k^{\mathrm{geo}} = \lambda_0 \mathcal{L}_{\mathrm{MSE}}(m_k, \bar{m}_k) + \lambda_1 \mathcal{L}_{\mathrm{MSE}}(\mathbf{p}_k, \bar{\mathbf{p}}_k) + \lambda_2 \mathcal{L}_{\mathrm{MSE}}(\Sigma_k^n, \bar{\Sigma}_k^n)
$$

**拓扑势函数** 将持久性点划分为保留集 $\mathcal{V}_k$ 和抑制集 $\mathcal{Z}_k$，通过最大化保留集中特征的持久性、最小化抑制集中特征的持久性来强制拓扑先验：

$$
\mathcal{L}_k^{\mathrm{topo}} = - \sum_{p \in \mathcal{V}_k} |\mathbf{S}_k(r_b^p) - \mathbf{S}_k(r_d^p)|^2 + \sum_{p \in \mathcal{Z}_k} |\mathbf{S}_k(r_b^p) - \mathbf{S}_k(r_d^p)|^2
$$

**引导去噪** 在每个采样步，将无条件去噪输出 $D_\theta$ 与势函数梯度相结合：

$$
D_\theta^w(\mathbf{z}_\sigma; \sigma) = D_\theta(\mathbf{z}_\sigma; \sigma) - \sigma^2 \cdot \nabla_{\mathbf{z}_\sigma} \mathcal{L}
$$

这一修正项使采样轨迹偏离无条件分布，逐步逼近满足局部几何-拓扑约束的样本，且整个过程无需重新训练扩散模型。

### 补充图表

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/002_Figure_2.jpg]]
*Figure 2: Differentiable measurement of anatomical properties from multi-class voxel maps. A: We differentiably parse relevant substructures from anatomical voxel maps for localized measurement. B: We spatially transform cuboidal primitives (template domains) into control domains that slice into anatomical structures (V-parsing). C: The substructure is then differentiably measured in terms of geometric properties; as well as D: persistent homology-based topological properties*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/003_Figure_3.jpg]]
*Figure 3: Efficient parsing of anatomical substructures during diffusion guidance. A: During guidance, we parse relevant substructures directly from the clean latent prediction with a neural field decoder (L-parsing). B: In coarse L-parsing, we use a coarse grid to decode globally defined substructures at low spatial resolution. C: In localized L-parsing, we use a similar grid size but spatially transform the template point grid to decode localized substructures at high spatial resolution*

## 实验与分析

Anatomica 的实验设计围绕两个核心维度展开：**几何控制**与**拓扑控制**。几何控制实验评估框架对局部子结构的大小、形状和位置进行精确操控的能力；拓扑控制实验则评估对连通分量（Betti‑0）、环（Betti‑1）和空洞（Betti‑2）等拓扑先验的强制能力。实验在心脏（TotalSegmentator）、主动脉分支、脊柱和冠状动脉四个解剖数据集上进行，基线方法包括显式条件扩散模型（Explicit Conditioning）、隐式条件扩散模型（Implicit Conditioning）和无条件扩散模型（Unconditional）。

### 几何控制任务

**Table 1** 对比了不同方法的解码器类型、子结构解析策略和控制方式。Anatomica 的两个变体——Anatomica‑V（体素空间 V‑parsing + 卷积解码器）和 Anatomica‑L（潜在空间 L‑parsing + 神经场解码器）——均采用推理时梯度引导，无需针对特定几何属性重新训练扩散模型。

**Figure 4** 展示了通过改变组织通道选择、模板网格尺寸和空间变换定义的四项心脏几何控制任务。**Figure 5** 的定性结果表明，Anatomica 生成的解剖分割与目标控制域（黑色边框）和目标几何特征（红色椭球）高度吻合，样本几何以绿色椭球叠加显示。

**Table 2** 报告了定量结果。以右心室（Right Ventricle）任务为例：
- **质量保真度**：Anatomica‑L 达到 17.5（×10⁵），Anatomica‑V 达到 12.3，而显式条件基线高达 154.5，Anatomica 将质量偏差降低了约一个数量级。
- **质心保真度**：Anatomica‑L 为 48.6（×10⁴），Anatomica‑V 为 30.2，显式条件基线为 72.2。
- **协方差保真度**：Anatomica‑L 为 22.1（×10⁵），Anatomica‑V 为 21.6，显式条件基线为 27.9。
- **生成质量**：以 FMD 衡量，Anatomica‑V 取得 84.9 的最优值，Anatomica‑L 为 93.7，均显著优于显式条件基线的 164.7。1‑NNA 指标上 Anatomica‑L（0.566）和 Anatomica‑V（0.590）也优于显式条件（0.690），表明引导过程未损害样本的整体分布质量。

隐式条件基线在多数任务中表现最差，说明通过 3D 热图间接编码几何属性的方式难以实现精确的局部控制。

### 拓扑控制任务

**Figure 6** 展示了四项拓扑控制任务的定性结果，包括心房分离（Atrial Separation）、分支连通性（Branch Connectivity）、钙化计数（Calcium Count）和脊柱连续性（Spine Continuity）。Anatomica 成功生成了符合目标拓扑先验的分割，例如强制左右心房分离、确保主动脉分支的连通性等。

**Table 3** 的定量评估以 Betti 精度和 1‑NNA 为指标：
- **心房分离任务**（目标 B₀=2）：Anatomica‑L 的 B₀ 精度达 78.9%，无条件基线仅 7.81%，提升超过 71 个百分点。B₁ 和 B₂ 精度也分别达到 99.8% 和 100%。
- **分支连通性任务**（目标 B₀=1）：Anatomica‑L 的 B₀ 精度为 77.3%，无条件基线为 55.5%，提升 21.8 个百分点。
- **钙化计数任务**（目标 B₀=4）：Anatomica‑L 的 B₀ 精度为 60.9%，无条件基线仅 1.56%，提升近 60 个百分点。
- **脊柱连续性任务**：Anatomica 同样在所有 Betti 数上保持高精度。

值得注意的是，拓扑引导在显著提升拓扑保真度的同时，1‑NNA 指标与无条件基线保持可比甚至更优（如心房分离任务中 Anatomica‑L 的 1‑NNA 为 0.387，无条件基线为 0.415），表明拓扑约束的引入未导致生成样本偏离真实分布。

### 消融实验

消融实验系统性地考察了引导权重、损失解耦、部分解码策略和 softmax 温度等因素的影响。

**几何引导解耦**（**Figure 8**）：仅使用质心损失即可达到与全损失相当的质心保真度，且不对质量保真度、形状保真度或 FMD 产生显著负面影响，验证了几何矩各阶统计量之间的解耦控制能力。当所有损失项同时激活时，增加引导权重可提升几何保真度，但超过一定阈值后样本质量下降，导致保真度反而降低，揭示了引导强度与生成质量之间的倒 U 型关系。

**拓扑引导权重与 softmax 温度**（**Figure 9**）：提高 softmax 温度可在相同引导权重下提升拓扑保真度，同时增强对过高引导权重的鲁棒性，减轻过引导导致的样本质量退化。

**部分解码策略**（**Table 4** 和 **Figure 10**）：对比了粗粒度 L‑parsing、局部化 L‑parsing 和 V‑parsing 在不同解码分辨率下的表现。解码分辨率为 64 时提供了 **11 倍加速比**，是保真度与计算效率的良好折衷。过低的解码分辨率会降低拓扑保真度，但即使分辨率降至 16，Anatomica 仍能保持显著优于无条件基线的拓扑控制能力。

### 多尺度与多坐标系控制

**Figure 7** 展示了 Anatomica 在不同坐标系（笛卡尔、曲线、柱面、球面）下对解剖子结构进行多尺度几何控制的能力。通过改变控制域的仿射变换参数，框架可适应从器官级到亚结构级的多种控制粒度，无需修改底层扩散模型。

### 局限性与失败模式

尽管 Anatomica 在几何和拓扑控制任务上表现优异，但存在以下关键局限：
1. **计算开销**：拓扑引导的持久同调计算缺乏公开的 GPU 实现，单个样本在高解码分辨率下约需 420 秒（使用卷积解码器），限制了大规模应用。
2. **曲线控制域的骨架化瓶颈**：曲线坐标系的骨架化步骤仍在 CPU 上执行，成为并行化的瓶颈。
3. **速度‑精度权衡**：部分解码虽能提速，但过低的分辨率会显著降低拓扑保真度，需根据任务需求手动调整。
4. **泛化性未验证**：实验仅在心脏、主动脉、脊柱和冠状动脉等有限解剖数据集上进行，未在其他器官或病理数据上测试。

> **注意**：Figure 8、Figure 9、Figure 10 的具体数值曲线需结合原文图表进行详细解读，此处仅报告已验证的趋势性结论。

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/021_Figure_8.jpg]]
*Figure 8: Geometric guidance and disentangled guidance ablation study*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/022_Figure_9.jpg]]
*Figure 9: Topological guidance and softmax temperature ablation study*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/023_Figure_10.jpg]]
*Figure 10: Topological guidance and partial decoding resolution ablation study*

### 补充图表

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/004_Figure_4.jpg]]
*Figure 4: Geometric Control Tasks. We define a variety of relevant tasks by varying the selected tissues, template domain grid size, and control domain-specific spatial transforms*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/006_Table_1.jpg]]
*Table 1: Comparison of geometric control task approaches*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/008_Table_2.jpg]]
*Table 2: Quantitative results for geometric control tasks. We report geometric fidelity and generation quality for each taskapproach combination. Fidelity values for mass, centroid, and covariance are multiplied by 1e5, 1e4, 1e5 respectively*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation for topological control tasks. We report Betti precision for number of connected components B0, loops B1, and voids*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/010_Figure_7.jpg]]
*Figure 7: Multi-scale geometric control of various anatomical substructures over different coordinate systems. We generate anatomical segmentations based on domain size and anatomically relevant coordinate systems (Cartesian, curvilinear, cylindrical, and spherical)*

![[assets/figures/papers/paper_list_l2440_https_arxiv_org_abs_2511_20587/figures/011_Table_4.jpg]]
*Table 4: Quantitative ablation study for partial decoding strategies. We evaluate the geometric fidelity and generation quality, and sampling speed for different decoding strategies and resolutions. Speed is measured in terms of sampled label maps per second using the maximum allowable batch size on a single GPU, normalized to the slowest method. Fidelity values for mass, centroid, and covariance are multiplied by 1e5, 1e4, 1e5 respectively*

## 方法谱系与知识库定位

### 1. 问题定位：解剖生成中的局部化控制瓶颈

医学图像合成领域长期面临一个核心矛盾：扩散模型（Diffusion Models）能够生成高质量的解剖结构，但缺乏对生成过程进行**局部化（localized）**、**可微分（differentiable）**控制的机制。传统方法将控制目标编码为全局条件信号，通过条件训练（conditional training）将生成分布拉向目标属性，但这种方式存在两个根本性局限：

- **控制粒度粗放**：条件信号（如标量属性值或全局热图）无法精确指定局部子结构的几何特征（大小、形状、位置）和拓扑特征（连通分量数、环数、空洞数）。
- **缺乏编辑灵活性**：条件训练将控制逻辑固化在模型权重中，改变控制目标需要重新训练，无法实现推理时的交互式编辑。

Anatomica 的定位是**推理时引导框架（inference-time guidance framework）**，其核心创新在于将控制逻辑从训练阶段剥离，转而通过梯度引导在采样过程中施加约束。这一设计选择使其与现有方法形成了清晰的代际差异。

### 2. 与基线方法的对比

论文在几何控制任务上系统对比了三类方法，Table 1 给出了架构层面的差异概览：

| 方法 | 解码器类型 | 子结构解析策略 | 控制方式 |
|------|-----------|---------------|---------|
| Explicit Conditioning | 神经场（Neural Field） | 无 | 条件训练（标量属性） |
| Implicit Conditioning | 神经场（Neural Field） | 无 | 条件训练（3D热图） |
| Anatomica-V | 卷积（Convolutional） | V-parsing（体素空间解析） | 推理时梯度引导 |
| Anatomica-L | 神经场（Neural Field） | L-parsing（潜在空间解析） | 推理时梯度引导 |

**Explicit Conditioning** 将几何属性（如质量、质心坐标）直接编码为标量条件信号，输入扩散模型进行条件训练。该方法在概念上最直接，但控制精度严重受限于条件信号的表达能力——标量无法传递空间局部性信息，导致生成样本的几何保真度较差。在 Right Ventricle 任务上，其质量保真度（Mass Fidelity）为 154.5（×1e5），而 Anatomica-L 仅为 17.5，差距接近一个数量级（Table 2）。

**Implicit Conditioning** 通过 3D 热图（椭圆形距离图）间接编码几何属性，将热图与噪声潜在变量拼接后输入模型。热图提供了空间先验，但本质上仍是一种全局条件信号，无法对局部子结构施加精确约束。论文未单独报告其定量结果，但从定性对比可见，其控制精度介于 Explicit Conditioning 与 Anatomica 之间。

**Anatomica** 的推理时引导策略从根本上改变了控制范式：不再依赖条件训练将属性“注入”模型分布，而是在每个采样步骤中计算解剖势函数（anatomical potential functions）的梯度，通过公式 $D_\theta^w(\mathbf{z}_\sigma; \sigma) = D_\theta(\mathbf{z}_\sigma; \sigma) - \sigma^2 \cdot \nabla_{\mathbf{z}_\sigma} \mathcal{L}$ 修正无条件去噪输出。这种设计使得控制目标可以任意组合和动态调整，无需重新训练模型。

### 3. 方法谱系中的位置

从更广阔的学术谱系来看，Anatomica 处于三个研究方向的交汇点：

**扩散模型引导（Diffusion Guidance）**：Anatomica 继承了分类器引导（classifier guidance）和通用损失引导（universal guidance）的思想，但将其扩展到 3D 解剖生成领域，并引入了局部化控制域的概念。与现有工作仅关注全局属性（如图像类别、文本对齐）不同，Anatomica 的引导目标是空间局部化的几何和拓扑属性。

**可微分拓扑计算（Differentiable Topology）**：在拓扑数据分析（TDA）领域，持久同调（persistent homology）已被用于网络训练中的拓扑正则化。Anatomica 的独特贡献在于将持久同调用于**推理时控制**而非权重更新——通过将持久性点划分为保留集 $\mathcal{V}_k$ 和抑制集 $\mathcal{Z}_k$，构建拓扑势函数 $\mathcal{L}_k^{\mathrm{topo}}$，实现对连通分量（B0）、环（B1）和空洞（B2）的精确操控。这一设计避免了拓扑损失对模型训练稳定性的影响。

**神经场表示（Neural Field Representations）**：Anatomica-L 利用神经场解码器直接从潜在空间解析子结构（L-parsing），无需完整体素重建。这种设计在计算效率上具有优势：部分解码分辨率为 64 时，相比全分辨率解码可提供 11 倍的加速比（Table 13），同时保持可接受的拓扑保真度。

### 4. 适用边界与局限

尽管 Anatomica 在几何和拓扑控制任务上展现了显著优势，其适用性受以下因素制约：

**计算开销**：拓扑引导的计算成本较高，每个样本约需 420 秒（最高解码分辨率下使用卷积解码器）。这一瓶颈主要源于持久同调（Cubical Ripser）缺乏公开的 GPU 实现，曲线控制域的骨架化步骤仍在 CPU 上执行。对于需要批量生成的应用场景，这一开销可能构成实际障碍。

**速度-精度权衡**：部分解码策略虽能提速，但过低的分辨率会降低拓扑保真度。消融实验（Figure 10）表明，解码分辨率从 128 降至 32 时，拓扑精度显著下降，需要在速度与精度之间谨慎权衡。

**数据集泛化性**：论文仅在心脏（TotalSegmentator）、主动脉、脊柱和冠状动脉等有限解剖数据集上验证，未在其他器官（如肝脏、肺部、脑部）或病理数据上测试泛化性。不同解剖结构在几何复杂度和拓扑多样性上的差异可能影响方法的有效性。

**控制域定义依赖手动参数**：立方体控制域的空间变换（旋转 $\mathbf{R}_k$、缩放 $\mathbf{s}_k$、平移 $\mathbf{t}_k$）需要手动设置，尚未实现自动化。对于复杂解剖结构，找到合适的控制域参数可能需要领域专家的介入。

### 5. 开放问题

1. **范式扩展**：框架能否扩展到其他生成范式（如流匹配、一致性模型）或更高维度的控制任务？推理时引导的核心思想——利用可微分测量函数修正采样过程——在原理上具有通用性，但具体实现需要针对不同生成框架调整梯度计算方式。

2. **拓扑计算加速**：能否通过近似持久同调或可学习的拓扑模块进一步加速计算？近期在可微分拓扑领域的工作（如拓扑自编码器）可能提供更高效的替代方案，但其在 3D 体素数据上的适用性有待验证。

3. **控制域自动化**：如何自动确定控制域的空间变换参数？将控制域定义与解剖标志点检测或分割模型结合，可能实现端到端的自动化控制，减少对人工输入的依赖。

4. **下游应用验证**：在真实临床虚拟试验或合成数据增强中的下游效果如何？论文展示了生成样本的几何和拓扑保真度，但未评估这些样本在下游任务（如分割模型训练、病理检测）中的实际效用，这是从方法研究走向临床落地的关键一步。

## 原文 PDF

![[paperPDFs/CVPR_2026/Anatomica_Localized_Control_over_Geometric_and_Topological_Properties_for_Anatomical_Diffusion_Models.pdf]]
---
title: "FreeForm: Reduced-Order Deformable Simulation from Particle-Based Skinning Eigenmodes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FreeForm_Reduced_Order_Deformable_Simulation_from_Particle_Based_Skinning_Eigenmodes.pdf
project_link: null
code_link: null
aliases:
- FreeForm
tags:
- CVPR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "采用再生核粒子法（RKPM）显式离散化蒙皮权重，并通过弹性能量Hessian矩阵的广义特征分解直接获得最优蒙皮特征模态，替代神经网络优化。"
primary_logic: "利用RKPM显式参数化蒙皮权重，使得弹性能量的二次近似可以解析表示为Hessian矩阵，进而通过高效的广义特征值求解得到一组正交且表达能力强的蒙皮基，兼顾了训练速度与仿真精度。"
claims:
- "我们的方法训练速度比Simplicits快约40倍（3.19±2.48s vs 121.44±10.15s）。"
- "在标准悬臂梁测试和Thingi10K/Simready数据集上，我们的方法在所有自由度数下均一致优于Simplicits的仿真精度。"
- "基于Hessian的特征分解训练策略在精度上优于Simplicits的随机仿射损失函数（Random z loss）。"
- "RKPM基函数相比原始RBF或单位分解RBF能生成更光滑、更准确的拉普拉斯特征模态。"
---

# FreeForm: Reduced-Order Deformable Simulation from Particle-Based Skinning Eigenmodes

> [!tip] 核心洞察
> 利用RKPM显式参数化蒙皮权重，使得弹性能量的二次近似可以解析表示为Hessian矩阵，进而通过高效的广义特征值求解得到一组正交且表达能力强的蒙皮基，兼顾了训练速度与仿真精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FreeForm：基于粒子蒙皮特征模态的降阶可变形仿真 |
| 英文题名 | FreeForm: Reduced-Order Deformable Simulation from Particle-Based Skinning Eigenmodes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://research.nvidia.com/labs/sil/projects/freeform/assets/main.pdf) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | FreeForm |
| Dataset | 标准悬臂梁弯曲 (Bend, m=32), 标准悬臂梁扭转 (Twist, m=16), Thingi10K (Fix Side, Simready (Fix Side |

> [!tip] 效果简介
> - 标准悬臂梁弯曲 (Bend, m=32) 上，归一化均方误差 (MSE) 为 2.93e-06，对比 Simplicits: 1.17e-04，变化 ~40倍精度提升。
> - 标准悬臂梁扭转 (Twist, m=16) 上，归一化均方误差 (MSE) 为 3.46e-06，对比 Simplicits: 1.30e-04，变化 ~37倍精度提升。
> - Thingi10K (Fix Side, m=32) 上，归一化MSE 为 6.87e-03，对比 Simplicits: 8.97e-03，变化 误差降低34.2%。

## 概要

**核心问题与瓶颈** 现有的网格无关降阶弹性仿真方法（如 **Simplicits**）需要为每个物体单独优化一个神经网络来学习蒙皮权重，训练时间长（约 2 分钟）且模拟精度有限；传统的基于网格的降阶方法则依赖高质量四面体网格，难以直接应用于现代点云表示（如 3D 高斯泼溅）。因此，如何在保持网格无关优势的同时，快速获得高质量、表达能力强的降阶基函数，成为该方向的关键瓶颈。

**核心方法定位** 本文提出 **FreeForm**——一种基于粒子蒙皮特征模态的网格无关降阶可变形仿真方法。其核心思路是：采用**再生核粒子法（RKPM）** 显式地离散化蒙皮权重函数，进而将弹性能量的二次近似解析地表示为权值空间 Hessian 矩阵；通过对该矩阵进行广义特征分解，直接获得一组正交且表达能力强的蒙皮特征模态，从而替代 Simplicits 中耗时的神经网络随机优化过程。

**方法谱系与知识库定位** FreeForm 属于**基于线性混合蒙皮（LBS）的网格无关降阶弹性仿真**范式。与 **Simplicits**（神经场 + 随机仿射损失优化）不同，FreeForm 将基函数构造问题转化为一个确定性的广义特征值问题，在训练速度与基函数质量之间取得了突破性平衡。在仿真阶段，FreeForm 与 Simplicits 共享相同的 LBS 变形映射与隐式时间积分框架，因此可直接替代后者。此外，FreeForm 的输入表示兼容任意支持体积积分的几何表示（网格、粒子、高斯泼溅等），使其在应用范围上显著优于依赖四面体网格的传统有限元降阶方法。

**主要结果概览** 在标准悬臂梁弯曲与扭转测试中，FreeForm 的归一化均方误差（MSE）比 Simplicits 降低约 40 倍（Table 1）。在 Thingi10K 和 Simready 数据集上，FreeForm 在所有自由度数下均一致优于 Simplicits，同时训练速度提升约 40 倍（3.19 s vs 121.44 s，Table 2）。消融实验表明，基于 Hessian 的特征分解训练策略在精度上优于 Simplicits 的随机仿射损失函数（Table 3），且 RKPM 基函数相比原始 RBF 能生成更光滑、更准确的拉普拉斯特征模态（Figure 3b）。此外，FreeForm 在多层非均质材料场景中能捕捉不同刚度层间的差异化变形行为，而 Simplicits 仅产生全局刚性变形（Figure 7）。

**局限与开放问题** FreeForm 作为降阶模型，难以捕捉高频细节（如褶皱），无法处理强非线性效应（如尖锐接触与碰撞）及拓扑变化（如断裂）。基函数质量依赖于 RKPM 核半径、采样密度和粒子分布的合理选择。如何将 RKPM 特征模态推广到断裂、切割等拓扑变化场景，以及如何在降阶框架中高效处理大变形接触与碰撞，仍是值得探索的开放问题。



### 问题背景：可变形体仿真的降阶需求

在计算机图形学、机器人仿真和虚拟现实等领域，对可变形弹性体进行高效且准确的动态仿真是一个核心挑战。全自由度仿真方法——如有限元法（FEM）、物质点法（MPM）和光滑粒子流体动力学（SPH）——虽然精度高，但计算成本巨大，难以满足实时交互式应用的需求。降阶模型（Reduced-Order Model, ROM）通过在低维子空间中近似物体的变形，大幅降低了仿真自由度，成为平衡精度与效率的关键技术路线。

### 现有方法及其瓶颈

当前主流的降阶弹性仿真方法存在两类典型的技术缺口：

**网格依赖型降阶方法**：传统降阶仿真（如基于FEM的模态分析）通常依赖高质量的四面体或六面体网格来定义形变子空间。然而，现代几何表示（如3D高斯泼溅、神经辐射场、点云等）往往是无网格的。对这类表示进行网格重建不仅引入额外的前处理开销，还可能在复杂拓扑上产生低质量单元，影响仿真稳定性。

**网格无关型降阶方法**：以 **Simplicits** 为代表的基于神经场的网格无关方法，通过神经网络隐式参数化蒙皮权重（skinning weights），绕开了对显式网格的依赖。但其存在两个显著瓶颈：

1. **训练效率低**：Simplicits需要为每个物体独立优化神经网络参数，通过最小化随机仿射变换下的期望弹性能量来训练蒙皮权重。这一过程需数分钟（约121秒），难以满足快速部署的需求。
2. **仿真精度受限**：其训练目标函数为随机仿射损失（Random z loss）加正交性软约束，优化过程高度非凸，容易陷入局部最优，导致蒙皮基函数表达能力不足，仿真结果与FEM黄金标准之间存在较大误差。

### 核心动机：从神经网络优化到解析特征分解

上述瓶颈的根源在于，Simplicits将蒙皮权重的获取建模为一个**隐式的、基于随机采样的神经网络优化问题**。本文的核心动机在于提出一种全新的视角：

> 是否可以通过显式参数化蒙皮权重，将弹性能量的二次近似解析地表达为权值空间的Hessian矩阵，从而将蒙皮基的求解转化为一个**确定性的广义特征值问题**？

这一思路的关键优势在于：广义特征分解天然保证了解的正交性（无需软约束惩罚项），且可通过成熟的线性代数库高效求解，避免了随机梯度下降的收敛不确定性。同时，特征向量对应最小特征值的性质，使所得蒙皮模态恰好对应物体最易被激发的低能变形模式，理论上具有更强的物理表达能力。

### 技术突破口：再生核粒子法（RKPM）的引入

要实现上述构想，需要一种能够**显式离散化空间连续函数**的无网格方法。本文选择引入**再生核粒子法（Reproducing Kernel Particle Method, RKPM）**作为核心技术工具。RKPM通过一组粒子中心上的核函数及其修正，能够以任意精度逼近空间中的光滑函数。将RKPM应用于蒙皮权重的参数化，使得：

- 权值空间的弹性能量Hessian矩阵 $\mathbf{H}_w$ 可以解析推导（见Proposition 1），尤其对常用的Neo-Hookean材料，其元素具有简洁的核梯度内积加权积分形式：
  $$(\mathbf{H}_w)_{ij} = \int_{\Omega} (\lambda(\mathbf{X}) + 4\mu(\mathbf{X})) \nabla \phi_i(\mathbf{X})^T \nabla \phi_j(\mathbf{X}) d\mathbf{X}$$
- 蒙皮特征模态的求解转化为标准的广义特征值问题 $\mathbf{H}_w \mathbf{v} = \lambda \mathbf{M} \mathbf{v}$，可直接调用高效数值线性代数例程。

这一设计从根本上改变了蒙皮权重的获取范式：从“为每个物体训练一个神经网络”变为“为每个物体组装Hessian矩阵并求解一次特征分解”。



## 核心方法与创新机理

FreeForm 的核心创新在于**用显式粒子基函数替代神经网络来参数化蒙皮权重**，从而将原本需要随机优化的降阶基构建问题转化为一个**确定性、可解析求解的广义特征值问题**。这一范式转换直接解决了现有网格无关降阶弹性仿真方法的两大瓶颈：训练速度慢和仿真精度受限。

### 瓶颈突破：从隐式优化到显式特征分解

现有网格无关降阶方法（以 **Simplicits** 为代表）使用神经网络隐式表示蒙皮权重函数 $\mathbf{W}(\mathbf{X})$，训练时需要在随机采样的仿射变换下最小化期望弹性能量，并辅以正交性软约束项。这一策略存在三个根本性问题：

1. **优化成本高**：每次迭代需对随机采样点计算弹性能量梯度，训练一个物体通常需要数万次迭代。
2. **收敛不稳定**：随机优化对超参数敏感，正交性仅由惩罚项近似保证。
3. **表达能力受限**：神经网络的隐式表示缺乏对弹性变形物理结构的先验知识。

FreeForm 的突破在于认识到：**若蒙皮权重采用再生核粒子法（RKPM）显式离散化，则弹性能量在权值空间的二次近似可解析表达为 Hessian 矩阵 $\mathbf{H}_w$**，进而将蒙皮基的优化问题转化为：

$$\operatorname{argmin}_{\mathbf{c} \in \mathbb{R}^{K \times m}} \mathrm{tr}(\mathbf{c}^T \mathbf{H}_w \mathbf{c}), \quad \mathrm{subject\ to} \quad \mathbf{c}^T \mathcal{M} \mathbf{c} = \mathbf{I}$$

这一问题的全局最优解恰好是广义特征值问题 $\mathbf{H}_w \mathbf{v} = \lambda \mathcal{M} \mathbf{v}$ 的前 $m$ 个最小特征值对应的特征向量。由此，**训练过程退化为一次高效的矩阵特征分解**，无需任何迭代优化。

### 关键技术组件

#### 1. RKPM 显式参数化（changed slot：蒙皮权重表示方法）

传统方法使用神经网络 $\mathbf{W}_\theta(\mathbf{X})$ 隐式编码蒙皮权重，FreeForm 改用 RKPM 显式插值：

$$\mathbf{W}^j(\mathbf{X}) = \sum_{k=1}^{K} \phi_k(\mathbf{X}) \mathbf{c}_k^j$$

其中 $\phi_k(\mathbf{X})$ 是满足再生条件（可精确重构多项式）的修正径向基核函数，$\mathbf{c}_k^j$ 是节点 $k$ 上第 $j$ 个蒙皮权重的值。这一选择使得权值空间的自由度从神经网络的隐式参数转变为显式的节点值向量 $\mathbf{c}$，为后续解析推导奠定基础。

#### 2. Hessian 解析推导（changed slot：训练目标函数）

在 RKPM 框架下，Neo-Hookean 弹性能量的权值空间 Hessian 矩阵具有简洁的解析形式（Proposition 1）：

$$(\mathbf{H}_w)_{ij} = \int_{\Omega} (\lambda(\mathbf{X}) + 4\mu(\mathbf{X})) \nabla \phi_i(\mathbf{X})^T \nabla \phi_j(\mathbf{X}) d\mathbf{X}$$

对于均质材料，$\mathbf{H}_w$ 进一步退化为弱形式 Laplace 矩阵的缩放：$\mathbf{H}_w = (\lambda + 4\mu) \mathbf{L}$。这意味着**蒙皮特征模态本质上就是材料感知的拉普拉斯特征模态**，物理意义清晰且计算高效。

#### 3. 天然正交性保证（changed slot：正交性约束实现）

特征分解天然满足离散正交性 $\mathbf{c}^T \mathcal{M} \mathbf{c} = \mathbf{I}$（达到数值精度），无需像 Simplicits 那样引入软约束损失项。这不仅简化了训练流程，还保证了蒙皮基之间的独立性，避免冗余自由度浪费。

#### 4. 确定性积分采样（changed slot：积分点采样方式）

训练阶段采用预先生成的均匀网格采样点进行数值积分，替代 Simplicits 的每次迭代随机采样。消融实验（Table 3）表明，均匀网格采样的 Hessian 损失在精度上显著优于随机仿射损失（Random z），且与直接特征分解精度相当。

### 创新效果总结

上述创新带来的实际收益在实验中得到了充分验证：

| 维度 | Simplicits | FreeForm | 提升幅度 |
|------|-----------|----------|---------|
| 训练时间 | 121.44 ± 10.15 s | 3.19 ± 2.48 s | ~40× 加速 |
| 悬臂梁弯曲精度 (MSE) | 1.17e-04 | 2.93e-06 | ~40× 精度提升 |
| 悬臂梁扭转精度 (MSE) | 1.30e-04 | 3.46e-06 | ~37× 精度提升 |
| Thingi10K 精度 (MSE) | 8.97e-03 | 6.87e-03 | 误差降低 34.2% |
| 基函数拟合残差 | 较高 | 显著更低 (Table 6, 7) | 表达能力更强 |

值得强调的是，这些提升并非来自计算资源的堆砌——两种方法在相同自由度、相同积分点数量、相同物理参数下进行公平对比——而是源于**将随机优化问题重构为确定性特征分解问题**这一根本性的方法创新。



![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/001_Figure_1.jpg]]
*Figure 1: Left: we show results of our reduced-order elastic simulation applied to 3D Gaussian Splatting (3DGS) objects. Middle: our simulation can handle multiple interacting 3DGS objects. Right: we show the application of our method in simulating robot interaction*

FreeForm 的完整 pipeline 包含两个解耦的阶段：**训练阶段**（基函数构建）与**仿真阶段**（降阶时间积分），其输入输出流如图 Figure 2 所示。

### 输入与预处理

方法接受任意支持体积积分的几何表示（如四面体网格、粒子云、高斯泼溅）以及材料参数（Lamé 常数 $\lambda$, $\mu$）。首先通过最远点采样（Farthest Point Sampling）在物体内部选取 $K$ 个核中心 $\mathbf{p}_k$，并构建再生核粒子法（RKPM）基函数 $\phi_k(\mathbf{X})$。该基函数由径向基函数（RBF）与多项式再生修正项组成，满足 $\sum_{k=1}^{K} \phi_k(\mathbf{X}) \mathbf{P}(\mathbf{p}_k) = \mathbf{P}(\mathbf{X})$ 的再生条件，从而保证对多项式场的精确插值能力。

### 训练阶段：蒙皮特征模态构建

训练阶段的核心任务是将蒙皮权重函数 $\mathbf{W}^j(\mathbf{X})$ 显式参数化为 RKPM 节点值的形式：

$$\mathbf{u}(\mathbf{X}; \mathbf{c}) = \sum_{k=1}^{K} \phi_k(\mathbf{X}) \mathbf{c}_k$$

基于此离散化，论文推导了 Neo-Hookean 弹性能量在权值空间的 Hessian 矩阵 $\mathbf{H}_w$ 的简洁解析表达式（Proposition 1）。对于均质材料，$\mathbf{H}_w$ 与弱形式 Laplace 矩阵 $\mathbf{L}$ 成正比：

$$(\mathbf{H}_w)_{ij} = (\lambda + 4\mu) \mathbf{L}_{ij}$$

随后，通过求解广义特征值问题 $\mathbf{H}_w \mathbf{v} = \lambda \mathbf{M} \mathbf{v}$，取最小 $m$ 个特征值对应的特征向量作为蒙皮权重的节点值 $\mathbf{c}$。该特征分解天然满足离散正交性约束 $\mathbf{c}^T \mathcal{M} \mathbf{c} = \mathbf{I}$，无需额外的软约束损失项。

### 仿真阶段：降阶弹性时间积分

仿真阶段采用线性混合蒙皮（LBS）变形映射：

$$\mathbf{x} = \Phi(\mathbf{X}, \mathbf{z}) = \mathbf{X} + \sum_{j=1}^{m} \mathbf{W}^{j}(\mathbf{X}) \mathbf{Z}_{j} \overline{\mathbf{X}}$$

其中 $\mathbf{z} \in \mathbb{R}^{12m}$ 为 $m$ 个仿射变换的低维自由度。每个时间步通过极小化增量势进行隐式时间积分：

$$\mathbf{z}_{t+1} = \arg \min_{\mathbf{z}} \mathrm{Ir}(\mathbf{z}, \mathbf{z}_{t}) + E_{\mathrm{pot}}(\mathbf{z}) + E_{\mathrm{ext}}(\mathbf{z})$$

弹性势能 $E_{\mathrm{pot}}$ 通过 Monte Carlo 积分在预先生成的均匀网格采样点上近似计算，采用 Newton 法迭代求解。

### 模块关系总结

整个 pipeline 的关键模块串联关系为：

1. **RKPM 粒子构建**：从积分点采样核中心，生成再生核基函数 → 输出 $\phi_k(\mathbf{X})$
2. **Hessian 与质量矩阵组装**：利用材料参数和核梯度解析计算 $\mathbf{H}_w$ 和 $\mathbf{M}$ → 输出稀疏矩阵
3. **广义特征分解**：求解 $\mathbf{H}_w \mathbf{v} = \lambda \mathbf{M} \mathbf{v}$ → 输出蒙皮权重节点值 $\mathbf{c}$
4. **降阶弹性仿真**：LBS 变形映射 + 隐式时间积分 → 输出各时间步的变形状态

该设计将训练阶段从 Simplicits 的神经网络随机优化（约 121 秒）转变为确定性特征分解（约 3.2 秒），实现了约 40 倍的训练加速，同时特征分解的解析性质保证了基函数的全局最优性（在二次近似意义下）。



FreeForm 的降阶弹性仿真管线由两个阶段构成：**训练阶段**通过 RKPM 显式离散化与广义特征分解直接获得蒙皮权重，**仿真阶段**则利用这些权重进行低自由度隐式时间积分。以下分述其核心模块与关键公式。

### 3.1 变形映射与仿真框架

降阶仿真的自由度由 $m$ 个仿射变换 $\mathbf{Z}_j \in \mathbb{R}^{3 \times 4}$ 构成，结合固定的蒙皮权重函数 $\mathbf{W}^j(\mathbf{X})$，通过线性混合蒙皮（LBS）表达物体变形：

$$
\mathbf{x} = \Phi(\mathbf{X}, \mathbf{z}) = \mathbf{X} + \sum_{j=1}^{m} \mathbf{W}^{j}(\mathbf{X}) \mathbf{Z}_{j} \overline{\mathbf{X}}
\tag{Eq. (1)}
$$

其中 $\overline{\mathbf{X}} = [\mathbf{X}, 1]^T$ 为齐次坐标。仿真阶段采用标准隐式时间积分，极小化增量势：

$$
\mathbf{z}_{t+1} = \arg \min_{\mathbf{z}} \mathrm{Ir}(\mathbf{z}, \mathbf{z}_{t}) + E_{\mathrm{pot}}(\mathbf{z}) + E_{\mathrm{ext}}(\mathbf{z})
\tag{Eq. (2)}
$$

三项分别对应惯性势、弹性势能与外力势能。训练阶段的核心任务是为每个物体构造一组表达能力强且正交的蒙皮权重函数 $\mathbf{W}^j$。

### 3.2 RKPM 显式离散化

FreeForm 采用再生核粒子法（RKPM）替代神经网络来参数化蒙皮权重。对于任意向量值函数 $\mathbf{u}(\mathbf{X})$，RKPM 通过节点值 $\mathbf{c}_k$ 与再生核 $\phi_k(\mathbf{X})$ 进行插值：

$$
\mathbf{u}(\mathbf{X}; \mathbf{c}) = \sum_{k=1}^{K} \phi_k(\mathbf{X}) \mathbf{c}_k
\tag{Eq. (6)}
$$

再生核 $\phi_k(\mathbf{X})$ 在原始径向基函数 $\varphi_k(\mathbf{X})$ 上施加修正项以满足多项式再生条件：

$$
\phi_k(\mathbf{X}) = \varphi_k(\mathbf{X}) \mathbf{P}^T(\mathbf{p}_k) \mathbf{C}(\mathbf{X})
\tag{Eq. (8)}
$$

$$
\sum_{k=1}^{K} \phi_k(\mathbf{X}) \mathbf{P}(\mathbf{p}_k) = \mathbf{P}(\mathbf{X})
\tag{Eq. (7)}
$$

其中 $\mathbf{P}(\mathbf{X})$ 为最高 $D$ 阶的多项式基向量，$\mathbf{C}(\mathbf{X})$ 为修正矩阵。这一显式参数化使得弹性能量的二次近似可以解析表达，为后续特征分解奠定基础。

### 3.3 广义特征分解求蒙皮特征模态

将蒙皮权重以 RKPM 节点值 $\mathbf{c} \in \mathbb{R}^{K \times m}$ 表示后，训练目标转化为在正交约束下最小化权值空间的二次弹性势能：

$$
\operatorname{argmin}_{\mathbf{c} \in \mathbb{R}^{K \times m}} \mathrm{tr}(\mathbf{c}^T \mathbf{H}_w \mathbf{c}), \quad \mathrm{subject\ to} \quad \mathbf{c}^T \mathcal{M} \mathbf{c} = \mathbf{I}
\tag{Eq. (15)}
$$

其中 $\mathbf{H}_w$ 为权值空间 Hessian 矩阵，$\mathcal{M}$ 为质量矩阵。该问题等价于广义特征值问题：

$$
\mathbf{H}_w \mathbf{v} = \lambda \mathcal{M} \mathbf{v}
\tag{Eq. (15)}
$$

取最小 $m$ 个特征值对应的广义特征向量 $\mathbf{v}_1, \ldots, \mathbf{v}_m$ 作为 $\mathbf{c}$，即得蒙皮特征模态。此过程天然满足离散正交性 $\mathbf{c}^T \mathcal{M} \mathbf{c} = \mathbf{I}$（至数值精度），无需额外正交惩罚项。

### 3.4 Neo-Hookean 材料下 Hessian 的解析形式

**Proposition 1** 给出了 Neo-Hookean 弹性能量在 RKPM 离散化下权值空间 Hessian 的简洁解析表达式：

$$
(\mathbf{H}_w)_{ij} = \int_{\Omega} (\lambda(\mathbf{X}) + 4\mu(\mathbf{X})) \nabla \phi_i(\mathbf{X})^T \nabla \phi_j(\mathbf{X}) d\mathbf{X}
\tag{Proposition 1}
$$

其中 $\lambda, \mu$ 为 Lamé 参数，$\nabla \phi_i$ 为 RKPM 核函数的空间梯度。该 Hessian 由三个坐标分量的全 Hessian 块组合而成：$\mathbf{H}_w = \mathbf{H}_{xx} + \mathbf{H}_{yy} + \mathbf{H}_{zz}$，优先捕捉平移主导的蒙皮模态。对于均质材料（$\lambda, \mu$ 为常数），Hessian 进一步简化为弱形式 Laplace 矩阵的缩放：

$$
(\mathbf{H}_w)_{ij} = (\lambda + 4\mu) \mathbf{L}_{ij}
\tag{Eq. (17)}
$$

这意味着均质材料的蒙皮特征模态与 Laplace 特征模态共享，物理直觉清晰且计算高效。

### 3.5 仿真阶段的能量离散

仿真阶段需对全自由度弹性势能进行积分。FreeForm 采用 Monte Carlo 近似，在预先生成的积分点 $\mathbf{X}_i$ 上求和：

$$
E_{\mathrm{pot}}(\mathbf{d}) \approx \sum_i v_i \Psi(\mathbf{F}(\mathbf{X}_i, \mathbf{d}))
\tag{Eq. (22)}
$$

其中 $v_i$ 为积分点体积权重，$\Psi$ 为 Neo-Hookean 能量密度函数（Eq. 16），$\mathbf{F}$ 为变形梯度。积分点采样方式（均匀网格 vs 随机采样）对精度影响有限，消融实验（Table 4）表明 FreeForm 在两种采样策略下均一致优于 Simplicits。



## 实验与关键发现

### 核心实验设计

FreeForm的实验评估围绕三个核心维度展开：**仿真精度**（以FEM全自由度结果为黄金标准）、**训练效率**（基函数构建耗时）以及**基函数表达能力**（拟合残差）。所有对比均在相同边界条件、时间步长和物理参数下进行，积分点数量与自由度数（m）保持一致。Simplicits基线使用与原论文一致的超参数（6层MLP，宽度64，10k次迭代）。FEM参考解采用相同的Neo-Hookean本构模型和高精度网格。

### 主实验结果

#### 标准悬臂梁测试

在经典悬臂梁弯曲与扭转基准上，FreeForm在所有自由度数下均一致优于Simplicits，且精度优势随自由度增加而扩大（Table 1，Figure 4）。以m=32弯曲工况为例，FreeForm的归一化MSE为2.93e-06，Simplicits为1.17e-04，精度提升约40倍。在m=16扭转工况下，FreeForm的MSE为3.46e-06，对比Simplicits的1.30e-04，提升约37倍。Figure 4的可视化对比中，FEM参考解以半透明方式叠加显示，FreeForm的变形结果与FEM几乎完全重合，而Simplicits在相同自由度下存在明显的形状偏差。

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/004_Table_1.jpg]]
*Table 1: Quantitive evaluation on the standard beam deformation test. We report the normalized Mean Squared Error (MSE) of simulated point locations on two types of boundary conditions. The results are reported for different numbers m of affine transformations for Simplicits and our method. We also show the results of MPM and SPH for comparison*

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/005_Figure_4.jpg]]
*Figure 4: Visual comparison on standard beam test. For the case of bending cantilever beam, FEM solution is overlaid semi-transparently on top of the simulated result from all competing methods to aid visual comparison*

#### Thingi10K与Simready数据集

在更大规模的数据集测试中（Table 2，Figure 5），FreeForm在三种边界条件（Fix Side、Pull Sides、Pull Farthest）下均保持精度优势。以m=32的Fix Side工况为例，在Thingi10K上FreeForm的归一化MSE为6.87e-03，Simplicits为8.97e-03，误差降低34.2%；在Simready上FreeForm的MSE为1.01e-09，Simplicits为2.16e-09，误差降低18.9%。最大误差指标同样呈现一致的优势。

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/006_Table_2.jpg]]
*Table 2: Quantitive evaluation on the Thingi10K and Simready Datasets. We report the normalized Mean Squared Error (MSE) and maximum error across all the examples for each boundary condition. We also show the training time of our method compared to Simplicits, and the improvement of our method in percentage, for a total of m = 32 skinning functions*

**训练效率方面**，FreeForm的平均训练时间为3.19±2.48秒，而Simplicits需要121.44±10.15秒，加速约40倍。这一差异源于FreeForm将基函数构建转化为广义特征值问题，可利用高效线性代数库直接求解，避免了Simplicits所需的迭代梯度优化过程。

#### 运行时效率

在仿真阶段的单步耗时对比中（Table 5，dt=0.01s），FreeForm与Simplicits处于同一量级，均远低于全自由度FEM。降阶模型的运行时效率主要取决于自由度数m和积分点数量，FreeForm的显式基函数求值在GPU上同样高效。

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/011_Table_5.jpg]]
*Table 5: Comparison of runtime in milliseconds (ms) for a simulation step of dt = 0.01s on average. The timing results are reported for the beam-bending experiment*

### 消融实验

#### 训练策略消融（Table 3）

为验证特征分解策略的有效性，实验对比了四种训练变体：
- **Hessian-Grid**：使用Hessian近似损失进行梯度下降优化，积分点采用均匀网格采样
- **Random z-Grid**：使用Simplicits的随机仿射损失函数，均匀网格采样
- **Random z-Random**：随机仿射损失函数，随机采样积分点
- **Ours**：直接特征分解

结果表明：（1）Hessian损失在精度上显著优于随机仿射损失（Random z），验证了Hessian二次近似作为训练目标的优越性；（2）在相同Hessian损失下，梯度下降优化（Hessian-Grid）与直接特征分解（Ours）精度相当，但特征分解的训练时间远低于优化方法；（3）随机采样积分点的效果不如均匀网格采样，且随机仿射损失对采样方式更为敏感。

#### 仿真阶段采样方式消融（Table 4）

在仿真阶段，分别测试了5k均匀网格采样点与5k随机采样点两种策略。结果表明，FreeForm在两种采样方式下均优于Simplicits，且自身对采样方式的敏感度较低。这一鲁棒性得益于RKPM基函数的光滑性和空间连续性。

#### 非均质材料测试（Figure 7）

在四层软硬交替的非均质球体上，FreeForm能够捕捉不同刚度层间的差异化变形行为——硬质层保持形状而软质层发生显著压缩。相比之下，Simplicits仅产生全局刚性变形，无法表达层间刚度差异导致的局部应变集中。这一优势源于FreeForm的Hessian矩阵能够显式编码空间变化的Lamé参数（λ(X), μ(X)），而Simplicits的随机仿射损失无法有效感知材料非均质性。

### 基函数表达能力分析（Table 6, Table 7）

通过对FEM仿真结果进行最小二乘拟合，定量评估蒙皮权重的表达能力。在标准悬臂梁测试（Table 6）和数据集测试（Table 7）中，FreeForm的拟合残差均显著低于Simplicits，表明RKPM特征模态构成的变形子空间能够更准确地逼近真实弹性变形。这一优势的根源在于：RKPM的再生核条件保证了基函数对多项式场的精确再现能力（Figure 3b），而广义特征分解确保了模态间的严格正交性和能量的最优递减排序。

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/012_Table_6.jpg]]
*Table 6: Comparison of basis fitting residual for reduced order methods (Simplicits and ours) for the standard beam test*

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/013_Table_7.jpg]]
*Table 7: Basis fitting residual error on the Thingi10K and Simready Datasets. We compute the least square fitting of the FEM simulation results using the predicted skinning weights from Simplicits and our method, and report the fitting residual to quantify the capability of those skinning weights to express the full-order FEM deformation. Our results show consistent improvement over the Simplicits baseline*

### 失败模式与局限性

尽管FreeForm在精度和效率上取得了显著提升，但仍存在以下局限：

1. **高频细节捕捉不足**：降阶模型的本质决定了其变形子空间维度有限，难以捕捉褶皱等高频局部变形。
2. **强非线性效应处理困难**：尖锐接触和碰撞等强非线性场景超出了当前LBS变形映射的表达能力。
3. **拓扑变化无法模拟**：断裂、切割等拓扑变化需要动态修改基函数结构，当前框架不支持。
4. **基函数质量对参数敏感**：RKPM核半径、采样密度和粒子分布的选择直接影响基函数质量，缺乏自动化的参数选择机制。

此外，Table 7中的具体残差数值未在正文中完整给出，需补充完整数据以进行更细致的定量分析。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/008_Table_4.jpg]]
*Table 4: Ablation studies on sampling method of integration points in simulation stage. We test with 5k integration points sampled from a uniform grid or random uniform distribution*

![[assets/figures/papers/paper_list_l2_https_research_nvidia_com_labs_sil_projects_freeform_assets_main_pdf/figures/009_Table_3.jpg]]
*Table 3: Ablation results on different training strategy. We compare variants of our method trained using different loss functions and integration point sampling methods. We also highlight the efficiency of our eigenanalysis formulation over gradient-based optimization in terms of training time for m = 32*



## 定位与知识库关联

### 问题背景与现有路线

弹性体降阶仿真旨在用少量自由度近似高维变形，从而大幅加速物理模拟。现有方法大致分为两条路线：

**基于网格的降阶方法**依赖高质量四面体或六面体网格，通过模态分析（如线性模态、PCA基）构建降阶子空间。这类方法在工程中成熟，但网格生成本身是瓶颈，尤其难以处理现代图形学中常见的点云表示（如3D高斯泼溅）。

**网格无关的降阶方法**试图绕过网格约束。其中最具代表性的是 **Simplicits**，它采用神经网络隐式参数化蒙皮权重，通过最小化随机仿射变换下的期望弹性能量来训练，实现了对任意几何表示的降阶仿真。然而，Simplicits存在两个核心瓶颈：
1. **训练代价高**：需要为每个物体单独优化神经网络（6层MLP，约10k次迭代），训练时间约121秒。
2. **精度受限**：随机采样的训练策略和软正交约束导致蒙皮基的表达能力并非最优。

### FreeForm的方法定位

FreeForm在网格无关降阶仿真路线中引入**再生核粒子法（RKPM）**作为蒙皮权重的显式参数化工具，将训练问题从随机优化转化为确定性的广义特征分解。这一设计带来了三个层面的改进：

**1. 参数化方式的根本转变。** Simplicits用神经网络隐式表示蒙皮权重函数，需要随机梯度下降优化；FreeForm用RKPM显式基函数插值，将蒙皮权重表示为节点值的线性组合。这使得弹性能量的二次近似可以解析表达为权值空间Hessian矩阵 $\mathbf{H}_w$，进而通过求解 $\mathbf{H}_w \mathbf{v} = \lambda \mathbf{M} \mathbf{v}$ 直接获得最优蒙皮特征模态。

**2. 正交性的天然满足。** Simplicits需要额外的正交惩罚项 $\mathcal{L}_{\text{ortho}}$ 来近似约束 $\mathbf{c}^T \mathcal{M} \mathbf{c} = \mathbf{I}$，这是一个软约束。FreeForm的特征分解天然满足离散正交性（精确到数值精度），消除了这一近似误差来源。

**3. Neo-Hookean Hessian的解析推导。** FreeForm推导了Neo-Hookean弹性能量在RKPM离散化下权值空间Hessian的简洁解析形式（Proposition 1）：
$$(\mathbf{H}_w)_{ij} = \int_{\Omega} (\lambda(\mathbf{X}) + 4\mu(\mathbf{X})) \nabla \phi_i(\mathbf{X})^T \nabla \phi_j(\mathbf{X}) d\mathbf{X}$$
对于均质材料，这进一步退化为弱形式Laplace矩阵的常数倍：$(\mathbf{H}_w)_{ij} = (\lambda + 4\mu) \mathbf{L}_{ij}$。这一解析形式避免了Simplicits中Monte Carlo采样的随机性，也使得Hessian矩阵的组装高效且确定性。

### 与全自由度方法的边界

FreeForm作为降阶方法，其仿真精度以全自由度方法为参照。论文以**有限元法（FEM）**作为黄金标准，同时对比了**物质点法（MPM）**和**光滑粒子流体动力学（SPH）**。这些全自由度方法可以捕捉任意高频变形细节，但计算代价远高于降阶方法。FreeForm在悬臂梁弯曲测试中达到与FEM参考解 $2.93 \times 10^{-6}$ 的归一化MSE（m=32），证明了降阶近似的高保真性。

值得注意的是，论文指出MPM存在非预期的数值断裂问题（Figure 6），这进一步凸显了稳定降阶仿真的实用价值。

### 适用边界与局限

**适用场景：**
- 输入几何可以是任意允许体积积分的形式（网格、点云、3DGS等），无需高质量网格。
- 均质和非均质Neo-Hookean材料均可处理（Figure 7展示了四层刚-柔交替非均质球体的差异化变形）。
- 训练阶段约3秒即可完成，适合需要快速切换物体的应用场景。

**已知局限：**
1. **高频细节缺失**：降阶模型受限于基函数的数量（自由度数m），难以捕捉褶皱等高频几何特征。
2. **强非线性效应**：尖锐接触和碰撞等强非线性边界条件超出了当前框架的处理能力。
3. **拓扑变化**：无法模拟断裂、切割等拓扑改变场景。
4. **基函数质量依赖**：RKPM核半径、采样密度和粒子分布的选择会影响基函数的稳定性和精度。对于极度稀疏或非均匀的粒子分布，基函数质量可能退化。

### 开放问题

1. 如何在降阶框架中高效处理大变形接触和碰撞？这需要将接触力学引入RKPM基函数的构建或仿真阶段的约束处理。
2. RKPM特征模态是否能推广到断裂和切割等拓扑变化场景？这可能需要在基函数构建中引入局部自适应机制。
3. 对于极度稀疏或非均匀的粒子分布，如何保证基函数的稳定性和精度？可能需要自适应核半径选择或粒子重采样策略。
4. 当前方法仅在Neo-Hookean材料上验证了Hessian的解析形式，推广到更复杂的本构模型（如Mooney-Rivlin、Ogden等）是否仍能保持解析简洁性？

> **注意**：Table 7中的具体残差数值在提供的上下文中未完整给出，该消融实验的定量结论需手动核实原文。



## 原文 PDF

![[paperPDFs/CVPR_2026/FreeForm_Reduced_Order_Deformable_Simulation_from_Particle_Based_Skinning_Eigenmodes.pdf]]

---
title: "QuadSync: Quadrifocal Tensor Synchronization via Tucker Decomposition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/QuadSync_Quadrifocal_Tensor_Synchronization_via_Tucker_Decomposition.pdf
project_link: null
code_link: null
aliases:
- QIAJOQTEM
- QuadSync
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 构建块四焦距张量并揭示其Tucker分解形式，利用其多线性秩(4,4,4,4)的低秩约束，通过ADMM-IRLS联合优化未知尺度和相机矩阵。
primary_logic: 块四焦距张量的Tucker分解其因子矩阵即为堆叠的相机矩阵，且多线性秩固定为(4,4,4,4)，不随相机数量变化并在共线相机下保持稳定，这比块基本矩阵和块三焦距张量具有更强的代数约束，从而实现鲁棒的全局同步。
claims:
- 块四焦距张量具有Tucker分解Q^n = G_Q ×_1 C ×_2 C ×_3 C ×_4 C，其中C为堆叠相机矩阵，G_Q为常数稀疏核心张量。
- 当相机不完全共享同一中心时，mlrank(Q^n) = (4,4,4,4)；在共线相机下该秩不下降，优于基本矩阵和三焦距张量。
- 通过HOSVD可直接从任何mode- flattening中取前4个奇异向量恢复相机矩阵（至投影歧义）。
- QuadSync和Joint Opt.在ETH3D和EPFL数据集上的位置误差显著优于仅用三焦距张量的Trifocal Sync，且在共线相机场景中仍可成功恢复位姿。
---

# QuadSync: Quadrifocal Tensor Synchronization via Tucker Decomposition

> [!tip] 核心洞察
> 块四焦距张量的Tucker分解其因子矩阵即为堆叠的相机矩阵，且多线性秩固定为(4,4,4,4)，不随相机数量变化并在共线相机下保持稳定，这比块基本矩阵和块三焦距张量具有更强的代数约束，从而实现鲁棒的全局同步。

| 字段 | 内容 |
|------|------|
| 中文题名 | QuadSync：基于Tucker分解的四焦距张量同步 |
| 英文题名 | QuadSync: Quadrifocal Tensor Synchronization via Tucker Decomposition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22639) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | QuadSync (IRLS-ADMM) and Joint Optimization (QuadSync, TrifocalSync, Essential matrices) |
| Dataset | ETH3D - courtyard, EPFL - FountainP11, EPFL - CastleP19 |

> [!tip] 效果简介
> - ETH3D - courtyard 上，平均位置误差 (mean location error) 0.0477 (QuadSync), 0.0489 (Joint Opt.) vs 0.1753 (Trifocal Sync) (下降约73%)；中位位置误差 (median location error) 0.0307 (QuadSync), 0.0324 (Joint Opt.) vs 0.0947 (Trifocal Sync) (下降约68%)。
> - EPFL - FountainP11 上，平均位置误差 0.0002 (QuadSync/Joint Opt.) vs 0.0098 (Trifocal Sync) (大幅优于)。
> - EPFL - CastleP19 上，平均位置误差 0.5130 (QuadSync), 0.4921 (Joint Opt.) vs 7.6932 (Trifocal Sync) (Trifocal Sync严重失败，QuadSync大幅改善)。

## 概要

传统运动恢复结构（SfM）中的全局同步主要依赖成对基本矩阵或三焦距张量，四焦距张量所蕴含的四视图高阶约束长期未被有效利用，且缺乏针对四焦距张量集合的全局同步算法。本文提出**QuadSync**，首次将四焦距张量纳入全局同步框架，核心发现是：块四焦距张量 $\mathcal{Q}^n$ 具有Tucker分解形式 $\mathcal{Q}^n = \mathcal{G}_Q \times_1 C \times_2 C \times_3 C \times_4 C$，其因子矩阵即为堆叠的相机矩阵 $C \in \mathbb{R}^{3n \times 4}$，多线性秩固定为 $(4,4,4,4)$，不随相机数量 $n$ 变化（Theorem 3.1）。这一低秩约束比块基本矩阵的秩-6约束和三焦距块张量的多线性秩 $(6,4,4)$ 更为严格，且在共线相机退化场景下仍保持稳定——基本矩阵和三焦距张量在此条件下秩下降，而四焦距张量不受影响（Remark 1, Theorem 8.1）。

基于该代数结构，QuadSync采用双层**ADMM-IRLS**优化框架，联合恢复未知尺度张量 $\Lambda$ 和相机矩阵 $C$：外环IRLS处理鲁棒 $\ell_1$ 损失，内环ADMM通过行闭式解并行更新各模式的因子矩阵。HOSVD初始化可直接从任意mode-flattening取前4个奇异向量恢复相机矩阵至投影歧义（Corollary 3.1.1），无需外部初值。

在ETH3D和EPFL数据集上，QuadSync的位置误差显著优于仅使用三焦距张量的**Trifocal Sync**（Lerman et al., 2024）：ETH3D courtyard场景平均位置误差从0.1753降至0.0477（下降约73%），EPFL CastleP19场景从7.6932降至0.5130（Trifocal Sync严重失败而QuadSync大幅改善）。联合优化方案（同时利用四焦距、三焦距和基本矩阵）进一步提升鲁棒性。消融实验表明，分布式同步（3个簇）可将全同步运行时间从1666秒压缩至约150秒，仅牺牲少量精度；随机列采样（如30列）亦可在保持精度的同时显著加速。

该方法的主要局限在于计算复杂度为 $O(n^4)$，对四视图匹配完整性敏感，且四焦距张量的估计质量依赖预处理。尽管如此，QuadSync揭示了高阶张量约束在全局SfM中的潜力，为将四焦距信息集成到现代增量式流程（如GLOMAP）开辟了方向。



### 多视图几何中的同步问题

从多幅图像中恢复三维结构和相机位姿是计算机视觉的核心任务，其基础建立在多视图几何的张量关系之上。给定一组图像，两视图间的对应点满足基本矩阵约束 $\mathbf{x_i}^T F_{ij} \mathbf{x_j} = 0$，三视图间的对应点满足三焦距张量约束，四视图间的对应点则满足四焦距张量约束。这些多视图张量——基本矩阵、三焦距张量和四焦距张量——均可从相机矩阵直接计算得到，例如四焦距张量由下式给出：

$$( Q _ { i j k l } ) ^ { p q r s } = \operatorname* { d e t } \left[ \begin{array} { l } { P _ { i } ^ { p } } \\ { P _ { j } ^ { q } } \\ { P _ { k } ^ { r } } \\ { P _ { l } ^ { s } } \end{array} \right]$$

在运动恢复结构（Structure from Motion, SfM）中，这些多视图关系通常从特征匹配中独立估计，随后需要通过“同步”过程将其整合为一致的全局相机位姿。

### 现有方法的瓶颈

传统全局SfM同步方法主要依赖成对测量（基本矩阵）或三视角测量（三焦距张量），利用其已知的低秩结构进行约束。具体而言，块基本矩阵的秩为6，块三焦距张量的多线性秩为 $(6,4,4)$。这些方法包括**LUD**（基于低秩分解）、**NRFM**（非凸鲁棒基本矩阵同步）、**MPLS BATA**和**MPLS CS**（基于多视角线搜索的同步）等。然而，这些低阶测量在特定退化场景下存在根本性局限：当相机近似共线时，基本矩阵和三焦距张量的低秩结构会退化，导致同步失败。

四焦距张量作为四视图间的高阶几何关系，蕴含着比基本矩阵和三焦距张量更强的代数约束。然而，目前尚缺乏针对四焦距张量集合的全局同步算法——这一缺口正是本文的核心动机。高阶信息未被有效利用，意味着现有方法在面对共线相机等挑战性配置时缺乏鲁棒性。

### 本文动机与核心思路

本文旨在填补这一空白，首次提出四焦距张量的全局同步算法。核心洞察在于：将多个四焦距张量堆叠为**块四焦距张量**（block quadrifocal tensor）$\mathcal{Q}^n \in \mathbb{R}^{3n \times 3n \times 3n \times 3n}$ 后，该张量具有精确的Tucker分解形式：

$$\mathcal{Q}^n = \mathcal{G}_Q \times_1 C \times_2 C \times_3 C \times_4 C$$

其中 $C \in \mathbb{R}^{3n \times 4}$ 为堆叠的相机矩阵，$\mathcal{G}_Q \in \mathbb{R}^{4 \times 4 \times 4 \times 4}$ 为常数稀疏核心张量（元素仅取 $\{-1,0,1\}$），多线性秩固定为 $(4,4,4,4)$，不随相机数量 $n$ 变化。这一代数结构具有两个关键优势：

1. **更强的约束力**：与块基本矩阵（秩6）和块三焦距张量（多线性秩 $(6,4,4)$）相比，块四焦距张量的多线性秩 $(4,4,4,4)$ 提供了更紧的低秩约束。
2. **共线鲁棒性**：当相机不完全共享同一中心时，$\operatorname{mlrank}(\mathcal{Q}^n) = (4,4,4,4)$ 保持不变；即使在共线相机配置下该秩也不下降，这从根本上优于基本矩阵和三焦距张量在共线场景下的退化行为。

基于此，本文开发了**QuadSync**算法，通过ADMM-IRLS双层优化联合恢复未知尺度参数和相机矩阵，并进一步提出联合优化框架，同时利用四焦距张量、三焦距张量和基本矩阵的低秩约束，实现更鲁棒的全局同步。



## 核心方法与创新机理

QuadSync 的核心创新在于**首次将四焦距张量引入全局 SfM 同步框架**，并揭示了其独特的代数结构，从而实现了比传统成对/三视角方法更强的约束能力和鲁棒性。具体体现在以下三个 changed slots 上：

### 1. 同步输入：从三焦距张量到四焦距张量

传统全局 SfM 同步方法依赖成对基本矩阵（如 **LUD**、**NRFM**）或三焦距张量（如 **Trifocal Sync**, Lerman et al., 2024），其信息覆盖范围有限。QuadSync 将输入测量升级为**块四焦距张量**（block quadrifocal tensor），同时编码四个视图之间的几何关系。

这一升级的关键在于：四焦距张量蕴含了完整的二视图和三视图几何信息（Proposition 3.3），因此单个四焦距测量携带的约束远强于基本矩阵或三焦距张量。此外，QuadSync 的联合优化框架（Joint Optimization）可同时融合四焦距张量、三焦距张量和基本矩阵三类测量，形成多层级约束互补。

### 2. 低秩约束形式：Tucker 分解与多线性秩 (4,4,4,4)

这是 QuadSync 最根本的理论创新。作者发现，由 $n$ 个相机形成的块四焦距张量 $\mathcal{Q}^n \in \mathbb{R}^{3n \times 3n \times 3n \times 3n}$ 具有精确的 Tucker 分解形式：

$$\mathcal{Q}^n = \mathcal{G}_Q \times_1 C \times_2 C \times_3 C \times_4 C$$

其中 $C \in \mathbb{R}^{3n \times 4}$ 是堆叠的相机矩阵，核心张量 $\mathcal{G}_Q \in \mathbb{R}^{4 \times 4 \times 4 \times 4}$ 是一个**常数稀疏张量**，所有元素取值仅为 $\{-1, 0, 1\}$（Theorem 3.1）。这意味着块四焦距张量的多线性秩恒为 $(4, 4, 4, 4)$，**与相机数量 $n$ 无关**。

对比之下：
- 块基本矩阵的秩为 6
- 块三焦距张量的多线性秩为 $(6, 4, 4)$（Theorem 2.2）

QuadSync 的秩约束显著更低且更紧，提供了更强的代数正则化。更重要的是，**在共线相机场景下，$(4,4,4,4)$ 的秩不会退化**（Theorem 8.1, Remark 1），而基本矩阵和三焦距张量在该场景下会出现秩亏，导致同步失败。这一特性使得 QuadSync 在近共线视角下仍能成功恢复位姿（Figure 3）。

### 3. 优化方法：双层 ADMM-IRLS

针对块四焦距张量的高维特性（$\mathcal{O}(n^4)$ 存储）和未知尺度问题，QuadSync 设计了**双层优化架构**：

- **外环 IRLS**：将鲁棒 $\ell_1$ 损失转化为加权最小二乘，权重基于前次迭代残差计算：

$$w_{ijkl} = 1 / \max(\delta, \| \Lambda^{(t-1)}_{ijkl} \tilde{Q}^n_{ijkl} - [\mathcal{G}_Q; C_1, C_2, C_3, C_4]_{ijkl} \|_F )$$

- **内环 ADMM**：求解加权最小二乘问题，对四个模式的因子矩阵 $C_i$ 进行逐行闭式更新（Eq. 6），实现并行化；尺度张量 $\Lambda$ 通过闭式解更新并对称化（Eq. 7）；一致变量 $B$ 和对偶变量 $\Gamma_i$ 通过标准 ADMM 步骤更新（Eq. 8-9）。

该架构的关键优势在于：$C_i$ 的行更新可独立并行，且支持随机列采样加速（Figure 4），在牺牲极少精度的情况下大幅降低计算时间。

### 创新总结

QuadSync 的 changed slots 形成了完整的创新链条：**四焦距输入提供更丰富的高阶几何信息 → Tucker 分解揭示极低且稳定的多线性秩约束 → ADMM-IRLS 实现可扩展的鲁棒优化**。三者协同使得 QuadSync 在 ETH3D 和 EPFL 数据集上的位置误差较仅用三焦距张量的 Trifocal Sync 降低约 68-73%（Table 4-5），并在共线相机场景中展现出传统方法不具备的鲁棒恢复能力。



QuadSync 的整体流程围绕“块四焦距张量的 Tucker 分解”这一核心代数结构展开，将多视图几何中的全局同步问题转化为一个结构化的张量低秩逼近与联合优化问题。整个 pipeline 可划分为三个主要阶段：**块张量构建**、**HOSVD 初始化**、以及**双层优化求解（IRLS-ADMM）**，并可扩展为联合基本矩阵与三焦距张量的**联合优化框架**。

### 输入与块张量构建

系统的输入是一组已估计的四焦距张量 $\tilde{Q}_{ijkl}$（每个对应于四个相机 $i,j,k,l$），这些张量通过四视图特征匹配与初始位姿估计获得。由于四焦距张量只能估计到未知的非零尺度，每个 $\tilde{Q}_{ijkl}$ 与真值之间存在一个待恢复的尺度因子 $\lambda_{ijkl}$。

将所有相机（共 $n$ 个）的四焦距张量沿四个模式堆叠，形成**块四焦距张量** $\tilde{\mathcal{Q}}^n \in \mathbb{R}^{3n \times 3n \times 3n \times 3n}$。该块张量具有两个关键性质（Theorem 3.1）：
- 它存在一个 Tucker 分解 $\mathcal{Q}^n = \mathcal{G}_Q \times_1 C \times_2 C \times_3 C \times_4 C$，其中 $C \in \mathbb{R}^{3n \times 4}$ 是堆叠的相机矩阵，核心张量 $\mathcal{G}_Q \in \mathbb{R}^{4 \times 4 \times 4 \times 4}$ 是一个元素仅取自 $\{-1, 0, 1\}$ 的常数稀疏张量；
- 其多线性秩恒为 $(4,4,4,4)$，与相机数量 $n$ 无关，且在共线相机配置下该秩不会退化（Remark 1, Theorem 8.1），这赋予了 QuadSync 相比基于基本矩阵（秩 6）或三焦距张量（多线性秩 $(6,4,4)$）方法更强的代数约束力。

### HOSVD 初始化

在进入迭代优化之前，首先对块四焦距张量 $\tilde{\mathcal{Q}}^n$ 进行高阶奇异值分解（HOSVD）。根据 Corollary 3.1.1，从任意一个 mode 展开矩阵中取前 4 个左奇异向量，即可直接恢复出相机矩阵 $C$ 的初始估计（至投影歧义）。这为后续的 ADMM-IRLS 优化提供了一个高质量的起点，显著加速收敛。

### 双层优化：IRLS 外环 + ADMM 内环

QuadSync 的核心优化问题是在未知尺度 $\Lambda$ 和相机矩阵 $C$ 上联合最小化块张量的重构误差（Section 4.1）：

$$\min_{\Lambda, C} \sum_{(i,j,k,l) \in \Omega} \| \Lambda_{ijkl} \tilde{\mathcal{Q}}^n_{ijkl} - [\mathcal{G}_Q; C,C,C,C]_{ijkl} \|_F, \quad \text{s.t. } \Lambda \in S^4(\mathbb{R}^n), \|\Lambda\|_F^2=1$$

其中 $\Omega$ 为已观测的四焦距块索引集合，$\Lambda$ 被约束为四阶对称张量并做归一化以避免平凡解。

为求解该非凸、带 L1 损失的优化问题，算法采用**双层结构**（Algorithm 1）：

1. **IRLS 外环**（Section 4.1.1）：将 L1 损失转化为加权最小二乘问题。每次外迭代根据上一轮的残差计算权重 $w_{ijkl} = 1 / \max(\delta, \text{残差})$（Eq. 5），对残差大的块赋予低权重以实现鲁棒性。

2. **ADMM 内环**（Section 4.1.2）：在固定 IRLS 权重后，求解带一致约束的加权最小二乘问题。引入一致变量 $B$ 和对偶变量 $\Gamma_i$，将问题分解为四个可并行求解的子问题：
   - **更新 $C_i$**：逐行求解闭式解（Eq. 6），四个模式的因子矩阵 $C_1, C_2, C_3, C_4$ 独立更新；
   - **更新 $\Lambda$**：通过闭式解更新每个四焦距块的尺度，并进行对称化与归一化（Eq. 7）；
   - **更新 $B$ 与 $\Gamma_i$**：$B = \frac{1}{4}\sum(C_i + \Gamma_i)$，对偶上升 $\Gamma_i \leftarrow \Gamma_i + C_i - B$（Eq. 8-9）。

### 联合优化框架

在 QuadSync 的基础上，论文进一步提出了一个**联合优化框架**（Section 4.2），将四焦距张量、三焦距张量和基本矩阵的低秩约束统一到同一个目标函数中（Eq. 10）。该框架同时利用三种测量各自的代数结构——块四焦距张量的 Tucker 分解（核心张量 $\mathcal{G}_Q$，因子矩阵 $C$）、块三焦距张量的 Tucker 分解（核心张量 $\mathcal{G}_T$，因子矩阵 $\mathcal{P}$ 和 $C$）、以及块基本矩阵的矩阵分解（$\mathcal{G}_E$ 与 $\mathcal{P}$）——通过加权联合优化实现信息互补。联合优化在四焦距块完成率较低的数据集上尤为有效，因为三焦距和基本矩阵的约束可以填补四焦距测量的缺失。

### 分布式同步

为应对块四焦距张量 $O(n^4)$ 的存储与计算复杂度，论文还设计了分布式同步策略：将相机划分为多个簇，每个簇内独立运行 QuadSync，再通过簇间对齐合并为全局一致的相机位姿。该策略在牺牲少量精度的情况下可大幅降低运行时间（Table 2）。

### 输出

优化完成后，从收敛的 $C$ 中即可提取每个相机的 $3 \times 4$ 投影矩阵，进而分解为内参和外参（旋转与平移），完成全局相机位姿同步。



### 块四焦距张量的Tucker分解

QuadSync的核心代数洞察在于揭示块四焦距张量 $\mathcal{Q}^n \in \mathbb{R}^{3n \times 3n \times 3n \times 3n}$ 的Tucker分解形式。该张量由所有四元组 $(i,j,k,l)$ 的四焦距张量沿四个模式堆叠而成。Theorem 3.1给出了其精确的低秩结构：

$$\mathcal{Q}^n = \mathcal{G}_Q \times_1 C \times_2 C \times_3 C \times_4 C$$

其中 $C \in \mathbb{R}^{3n \times 4}$ 是所有 $n$ 个相机的 $3 \times 4$ 投影矩阵 $P_i$ 按行堆叠形成的矩阵，$\mathcal{G}_Q \in \mathbb{R}^{4 \times 4 \times 4 \times 4}$ 是一个**常数稀疏核心张量**，其所有元素取值于 $\{-1, 0, 1\}$。这一分解意味着块四焦距张量的多线性秩（multilinear rank）恒为 $(4, 4, 4, 4)$，与相机数量 $n$ 无关。

### 四焦距张量的代数定义

单个四焦距张量 $Q_{ijkl}$ 可直接由四个相机矩阵通过行列式构造：

$$(Q_{ijkl})^{pqrs} = \det \begin{bmatrix} P_i^p \\ P_j^q \\ P_k^r \\ P_l^s \end{bmatrix}$$

其中 $P_i^p$ 表示相机 $i$ 的投影矩阵的第 $p$ 行。这一构造方式揭示了四焦距张量与相机矩阵之间的直接代数关联，是Tucker分解中因子矩阵即为堆叠相机矩阵的根本原因。

### HOSVD初始化

基于Theorem 3.1，Corollary 3.1.1指出：通过对 $\mathcal{Q}^n$ 进行高阶奇异值分解（HOSVD），从任意一个mode的展平矩阵中取前4个左奇异向量，即可直接恢复相机矩阵 $C$（至一个 $4 \times 4$ 投影歧义）。这为QuadSync提供了无需随机初始化的解析起点。

### QuadSync主优化问题

实际估计的四焦距张量 $\tilde{Q}_{ijkl}$ 仅能恢复至一个未知非零尺度。QuadSync的核心优化目标是在未知尺度张量 $\Lambda$ 和相机矩阵 $C$ 之间进行联合估计：

$$\min_{\Lambda, C} \sum_{(i,j,k,l) \in \Omega} \| \Lambda_{ijkl} \tilde{Q}^n_{ijkl} - [\mathcal{G}_Q; C, C, C, C]_{ijkl} \|_F$$

约束条件为 $\Lambda \in S^4(\mathbb{R}^n)$（尺度张量满足四阶对称性）且 $\|\Lambda\|_F^2 = 1$（防止平凡零解）。损失函数采用 $L_1$ 范数以增强对离群值的鲁棒性。

### IRLS外环：鲁棒加权

为求解 $L_1$ 优化，QuadSync采用迭代重加权最小二乘（IRLS）策略。在第 $t$ 次迭代中，基于前一次残差计算权重：

$$w_{ijkl}^{(t)} = 1 / \max(\delta, \| \Lambda_{ijkl}^{(t-1)} \tilde{Q}^n_{ijkl} - [\mathcal{G}_Q; C_1^{(t-1)}, C_2^{(t-1)}, C_3^{(t-1)}, C_4^{(t-1)}]_{ijkl} \|_F)$$

其中 $\delta$ 为防止除零的小常数。权重将原 $L_1$ 问题转化为加权最小二乘问题，对残差大的块赋予低权重以抑制离群值。

### ADMM内环：交替求解

固定IRLS权重后，内环使用ADMM求解加权最小二乘问题。引入一致变量 $B$ 和对偶变量 $\Gamma_i$，将约束 $C_1 = C_2 = C_3 = C_4 = B$ 松弛后，交替执行以下更新：

**$C_i$ 的行闭式更新**：对每个模式 $i$ 的因子矩阵 $C_i$，其第 $j$ 行通过闭式解并行计算：

$$x_j = \left( \frac{\rho}{2} (B - \Gamma_i)_j + ((W_{(i)}^2)_j \odot_b [(\Lambda \odot_b \tilde{Q}^n)_{(i)}]_j) K^T \right) \left( \frac{\rho}{2} I_{4\times4} + K \text{diag}((W_{(i)}^2)_j) K^T \right)^{-1}$$

其中 $\rho$ 为ADMM惩罚参数，$K$ 为与核心张量 $\mathcal{G}_Q$ 相关的常数矩阵，$\odot_b$ 表示分块Hadamard积。

**$\Lambda$ 的闭式更新**：对每个四焦距块 $\Lambda_{ijkl}$，通过投影到单位Frobenius范数球上求解，并进行对称化处理以满足 $\Lambda \in S^4(\mathbb{R}^n)$。

**$B$ 与 $\Gamma_i$ 的更新**：

$$B = \frac{1}{4} \sum_{i=1}^4 (C_i + \Gamma_i), \quad \Gamma_i \leftarrow \Gamma_i + C_i - B$$

### 联合优化框架

QuadSync可进一步与三焦距张量和基本矩阵的低秩约束联合优化。联合目标函数为三部分的加权和：

$$\min_{\Lambda_E, \Lambda_T, \Lambda_Q, C} \frac{1}{n_Q} \| W_Q \odot_b (\Lambda_Q \odot_b \tilde{Q}^n - [\mathcal{G}_Q; C, C, C, C]) \|_F^2 + \frac{1}{n_T} \| W_T \odot_b (\Lambda_T \odot_b \tilde{T}^n - [\mathcal{G}_T; \mathcal{P}, C, C]) \|_F^2 + \frac{1}{n_E} \| W_E \odot_b (\Lambda_E \odot_b \tilde{\mathcal{E}}^n - [\mathcal{G}_E; \mathcal{P}, \mathcal{P}]) \|_F^2$$

其中三个项分别对应四焦距张量、三焦距张量和基本矩阵的低秩约束，$n_Q, n_T, n_E$ 为各类型观测的有效数量。该框架同时利用四种不同阶数的多视角几何约束，实现更强的全局一致性。



## 实验与关键发现

### 主实验结果

QuadSync及其联合优化变体在ETH3D和EPFL两个真实数据集上进行了评估，与**Trifocal Sync**（Lerman et al., 2024）、**LUD**、**NRFM**、**MPLS BATA**和**MPLS CS**等基线方法进行对比。所有方法使用相同的特征匹配和初始估计（通过GlueStick/GC-RANSAC等获取），四焦距张量从四视图点对应中估计。

在ETH3D courtyard数据集上，QuadSync取得了0.0477的平均位置误差，Joint Opt.为0.0489，而Trifocal Sync为0.1753，误差下降约73%（Table 4）。中位位置误差方面，QuadSync为0.0307，Joint Opt.为0.0324，Trifocal Sync为0.0947，下降约68%（Table 5）。

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/010_Table_4.jpg]]
*Table 4: Mean location error by method*

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/011_Table_5.jpg]]
*Table 5: Median location error by method*

在EPFL数据集上，差距更为显著。FountainP11场景中，QuadSync和Joint Opt.的平均位置误差仅为0.0002，而Trifocal Sync为0.0098（Table 4）。CastleP19场景中，Trifocal Sync严重失败，平均位置误差高达7.6932，而QuadSync降至0.5130，Joint Opt.降至0.4921，体现了四焦距张量在复杂场景下的鲁棒性优势。

旋转误差方面，QuadSync和Joint Opt.在多数场景下同样优于仅使用三焦距张量的方法（Table 6, Table 7）。完整的数值对比见Table 4–7。

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/012_Table_6.jpg]]
*Table 6: Mean rotation error by method*

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/013_Table_7.jpg]]
*Table 7: Median rotation error by method*

### 共线相机鲁棒性验证

传统基于基本矩阵或三焦距张量的同步方法在相机共线时面临严重的秩退化问题。QuadSync的核心理论优势在于：块四焦距张量的多线性秩固定为(4,4,4,4)，在共线相机下不下降（Theorem 8.1）。合成实验（Table 1）验证了这一性质：在10个共线相机的配置下（Figure 5展示真值位置），QuadSync成功恢复相机位姿，而基于低秩分解的基线方法出现显著退化。在ETH3D SLAM的plant scene 1近共线视图上，QuadSync同样成功恢复了相机位姿（Figure 3）。

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/006_Table_1.jpg]]
*Table 1: Results for synthetic experiments with collinear cameras*

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/003_Figure_3.jpg]]
*Figure 3: QuadSync retrieved camera poses on near-collinear views from plant scene 1 dataset from ETH3D SLAM*

### 分布式同步

为缓解计算复杂度，论文探索了分布式同步策略。将相机划分为多个簇，在每个簇内独立运行QuadSync，再通过对齐步骤合并结果。合成实验（Table 2）表明，3个簇的分布式同步在无噪声条件下将运行时间从全同步的1666秒降至150秒（对齐后），在1%噪声条件下从1944秒降至247秒，精度损失有限。CastleP30数据集上的定性结果（Figure 6）展示了手选簇的分布式同步恢复位姿与真值的对比。

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/008_Table_2.jpg]]
*Table 2: Results for synthetic distributed synchronization*

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/007_Figure_6.jpg]]
*Figure 6: Retrieved poses (colored, where each cluster has a distinct color) vs. ground truth poses (black) for CastleP30 with handpicked clusters*

### 消融实验

随机列采样更新策略在ETH3D relief数据集上进行了消融（Figure 4）。在QuadSync的ADMM内环中对C_i的更新使用随机列采样（例如30列），可实现与全列更新相近的精度，同时获得显著加速。这一策略为大规模场景提供了实用的加速手段。

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/004_Figure_4.jpg]]
*Figure 4: Randomized updates in QuadSync tested on ETH3D ‘relief’ dataset*

### 计算效率与完成率

Table 3报告了各数据集的四焦距块完成率和运行时间。四焦距张量的估计依赖于四视图匹配的完整性，部分数据集的完成率较低（如<30%），这会影响算法性能。QuadSync和Joint Opt.的计算负担随相机数量呈O(n^4)增长，运行时间显著高于仅使用三焦距张量的Trifocal Sync，这是高阶张量同步的固有代价。

### 失败模式与局限性

1. **观测稀疏性敏感**：当四焦距块完成率过低时，可用的四视图约束不足，算法精度下降。这是四焦距张量估计对稠密四视图匹配依赖的直接后果。
2. **计算复杂度瓶颈**：块四焦距张量的存储和更新复杂度为O(n^4)，在相机数量较多的场景中计算负担急剧增加，限制了方法的可扩展性。
3. **预处理误差传播**：四焦距张量的估计需要良好的特征匹配和位姿初值，实际应用中该步骤可能引入额外误差，影响后续同步质量。
4. **分布式对齐误差**：分布式同步虽然加速，但在噪声存在时对齐步骤可能导致误差累积，需要在簇划分和对齐策略上进行更精细的设计。
5. **对比公平性**：部分基线方法在特定数据集上的完成率与QuadSync不同（Table 3），这源于四视图匹配截断对不同方法输入完整性的影响差异，需在解读结果时注意。

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/009_Table_3.jpg]]
*Table 3: Completion rates and runtimes of different methods*

### 小结

实验结果表明，四焦距张量携带的高阶几何约束在全局SfM同步中具有显著优势，尤其在共线相机和复杂场景下展现出传统方法无法比拟的鲁棒性。然而，计算复杂度和对观测完整性的依赖仍是实用化的主要障碍，分布式同步和随机化更新策略提供了初步的缓解方向。

### 补充图表

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/005_Figure_5.jpg]]
*Figure 5: Ground truth location of 10 cameras*

![[assets/figures/papers/paper_list_l2136_https_arxiv_org_abs_2602_22639/figures/001_Figure_1.jpg]]
*Figure 1: Mean location error for ETH3D datasets*



## 定位与知识库关联

### 问题定位：从成对/三视角同步到四焦距高阶同步

传统全局SfM的同步（synchronization）问题主要围绕两个代数对象展开：**基本矩阵**（fundamental matrix）和**三焦距张量**（trifocal tensor）。基本矩阵同步利用秩-2约束和成对极线几何，三焦距张量同步则利用块三焦距张量的多线性秩$(6,4,4)$ Tucker分解（Lerman et al., 2024 ）。然而，这两类方法在面对**近共线相机**（near-collinear cameras）时都会遭遇代数退化——基本矩阵的秩降为1，三焦距张量的多线性秩也会下降，导致同步算法无法稳定恢复相机位姿。

QuadSync的工作填补了一个明确的空白：**四焦距张量**（quadrifocal tensor）作为四视图几何的代数编码，其高阶信息在全局同步中从未被系统利用。核心发现是：块四焦距张量$\mathcal{Q}^n$具有Tucker分解$\mathcal{Q}^n = \mathcal{G}_Q \times_1 C \times_2 C \times_3 C \times_4 C$，其中因子矩阵$C \in \mathbb{R}^{3n \times 4}$即为堆叠的相机矩阵，核心张量$\mathcal{G}_Q \in \mathbb{R}^{4 \times 4 \times 4 \times 4}$是取值为$\{-1,0,1\}$的常数稀疏张量（Theorem 3.1）。关键代数优势在于：其多线性秩固定为$(4,4,4,4)$，**不随相机数量$n$变化，且在共线相机下不退化**（Remark 1; Theorem 8.1），这比基本矩阵和三焦距张量提供了更强的约束。

### 与现有方法的代数关系

QuadSync并非孤立地使用四焦距张量，而是将其置于一个**统一的低秩同步框架**中。从代数角度看，基本矩阵、三焦距张量和四焦距张量之间存在明确的包含关系（Proposition 3.3）：块四焦距张量显式地编码了两视图和三视图几何信息。这使得作者能够提出**联合优化**（Joint Optimization）方案，将三类测量的低秩约束整合到同一目标函数中（Section 4.2, Eq. (10)）：

$$
\min_{\Lambda_E,\Lambda_T,\Lambda_Q,C} \frac{1}{n_Q} \| W_Q \odot_b (\Lambda_Q \odot_b \tilde{\mathcal{Q}}^n - [\mathcal{G}_Q; C,C,C,C] \|_F^2 + \frac{1}{n_T} \| W_T \odot_b (\Lambda_T \odot_b \tilde{\mathcal{T}}^n - [\mathcal{G}_T; \mathcal{P},C,C] ) \|_F^2 + \frac{1}{n_E} \| W_E \odot_b (\Lambda_E \odot_b \tilde{\mathcal{E}}^n - [\mathcal{G}_E; \mathcal{P},\mathcal{P}] \|_F^2
$$

这种联合框架在谱系上可以视为对**Trifocal Sync**（Lerman et al., 2024）的自然扩展——从三视图张量同步扩展到四视图，同时保留了与成对测量的兼容性。

### 优化方法的谱系定位

在优化策略上，QuadSync采用了**双层ADMM-IRLS**架构：外环IRLS将L1鲁棒损失转化为加权最小二乘，内环ADMM交替求解相机矩阵$C_i$、尺度$\Lambda$和一致变量$B$。这一设计继承了全局同步领域使用IRLS处理外点的传统（如NRFM等鲁棒基本矩阵同步方法），但将其适配到了四阶张量的Tucker分解约束下。

一个值得注意的实现细节是$C_i$的行闭式更新（Eq. (6)），它利用了块四焦距张量的mode展开结构与核心张量$\mathcal{G}_Q$的稀疏性，使得每行可独立并行求解。这与Trifocal Sync中三焦距块张量的更新逻辑同源，但因多线性秩从$(6,4,4)$降至$(4,4,4,4)$，每次迭代的计算量反而更可控。

### 适用边界与局限

**计算复杂度**是QuadSync最显著的瓶颈。块四焦距张量的存储和更新复杂度为$O(n^4)$，随着相机数量增长，计算负担急剧增加。Table 3中报告了各数据集的运行时间，例如在ETH3D的某些场景中，QuadSync的全同步耗时可达数千秒。作者提出的**分布式同步**（将相机划分为簇分别同步后对齐）和**随机列采样**（Figure 4）是缓解这一问题的实用策略，但分布式方案在噪声存在时对齐步骤可能引入误差累积。

**对观测完整性的依赖**是另一个关键限制。四焦距张量的估计需要足够的四视图匹配来形成稠密的张量块；当四焦距块完成率较低（如$<30\%$）时，算法性能会下降。Table 3中的完成率数据显示，不同数据集和场景下四焦距块的稀疏程度差异显著，这直接影响QuadSync相对于仅用三焦距或基本矩阵方法的增益幅度。

**四焦距张量估计本身的质量**也是一个前置依赖。实际流程中，四焦距张量需要通过特征匹配和位姿初值来估计（例如使用GlueStick/GC-RANSAC等前端），该步骤引入的误差会传播到同步阶段。论文中所有对比方法使用相同的输入特征匹配，但四焦距张量估计的鲁棒性并未被独立评估。

### 开放问题

1. **张量估计质量的提升**：能否绕过显式的四焦距张量估计，直接从四视图特征匹配构建更紧致的代数约束？这关系到减少对稠密四视图匹配的依赖。

2. **复杂度降阶**：块四焦距张量的$O(n^4)$复杂度限制了其在大规模场景中的应用。能否利用核心张量$\mathcal{G}_Q$的极端稀疏性（仅含$\{-1,0,1\}$且高度结构化）开发更高效的随机化或分解算法，将有效复杂度降至接近$O(n^2)$或$O(n^3)$？

3. **代数约束的完备化**：四焦距张量与三焦距张量、基本矩阵之间存在未显式利用的代数约束（如$P_i$的$2 \times 2$子式关系）。将这些约束显式加入联合优化框架，可能进一步增强一致性并减少退化情况。

4. **与现代SfM流程的集成**：QuadSync目前作为一个独立的同步模块运行。如何将其无缝集成到如GLOMAP等现代增量式或全局式SfM流程中，实现端到端的性能提升，仍需探索。特别是，四焦距张量的估计和同步能否与特征匹配、外点滤除等前端步骤形成闭环反馈？

5. **理论完备性**：Theorem 8.1证明了共线相机下多线性秩保持$(4,4,4,4)$，但该结论是否对所有退化配置（如所有相机共面、部分相机纯旋转等）成立，仍需更系统的代数分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/QuadSync_Quadrifocal_Tensor_Synchronization_via_Tucker_Decomposition.pdf]]

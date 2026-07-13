---
title: "A Resolution-Agnostic Geometric Transformer for Chromosome Modeling Using Inertial Frame"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Resolution_Agnostic_Geometric_Transformer_for_Chromosome_Modeling_Using_Inertial_Frame.pdf
project_link: null
code_link: https://github.com/yize1203/InertialGenome
aliases:
- RAGTCMUIF
- InertialGenome
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/genetics_cell_biology_health_etc
core_operator: "引入惯性框架（Inertial Frame）进行姿态规范化，并结合基于Nyström估计的几何感知位置编码（Geometry-aware Positional Encoding），使Transformer能够学习分辨率无关的鲁棒表示。"
primary_logic: "通过惯性框架将任意旋转/平移下的染色体坐标对齐到由惯性张量主轴定义的标准坐标系，消除姿态变化；再利用Nyström方法对3D坐标的径向基函数（RBF）核进行低秩近似，高效捕获长程结构依赖，从而实现跨分辨率的稳定重建。"
claims:
- "InertialGenome在单细胞Hi-C数据集（Frontal cortex和B-Lymphocyte）的四个分辨率上，dSCC和dRMSE指标均优于所有四种基线方法。"
- "跨分辨率迁移学习（320kb→160kb/80kb/40kb）中，InertialGenome相比同分辨率原始模型提升高达5%。"
- "消融实验表明，移除惯性对齐、RoPE或Nyström分支均导致性能下降，其中移除Nyström在精细分辨率（40kb）上dRMSE上升0.0114。"
- "TAD验证中，IG-3DMAX的intra/inter距离比（0.760–0.814）显著低于HiCEGNN（0.914–0.993），且Mann–Whitney U检验p值极小。"
---

# A Resolution-Agnostic Geometric Transformer for Chromosome Modeling Using Inertial Frame

> [!tip] 核心洞察
> 通过惯性框架将任意旋转/平移下的染色体坐标对齐到由惯性张量主轴定义的标准坐标系，消除姿态变化；再利用Nyström方法对3D坐标的径向基函数（RBF）核进行低秩近似，高效捕获长程结构依赖，从而实现跨分辨率的稳定重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于惯性框架的分辨率无关几何Transformer用于染色体建模 |
| 英文题名 | A Resolution-Agnostic Geometric Transformer for Chromosome Modeling Using Inertial Frame |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OwLl8Xi6JG) · [GitHub](https://github.com/yize1203/InertialGenome) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/genetics_cell_biology_health_etc |
| Method | InertialGenome |
| Dataset | Frontal cortex cell test set, B-Lymphocyte cell test set |

> [!tip] 效果简介
> - Frontal cortex cell test set 上，dSCC 为 0.9030 (IG-3DMAX, 320kb)，对比 0.8815 (3DMAX, 320kb)，变化 +0.0215。
> - Frontal cortex cell test set 上，dRMSE 为 0.1547 (IG-3DMAX, 320kb)，对比 0.1453 (3DMAX, 320kb)，变化 +0.0094 (数值略高，但dSCC显著提升)。
> - B-Lymphocyte cell test set 上，dSCC 为 0.9209 (IG-3DMAX, 1MB)，对比 0.9012 (3DMAX, 1MB)，变化 +0.0197。

## 概要

基于Hi-C接触矩阵的染色体三维重建是理解基因组空间组织与功能的核心问题。现有深度学习方法（如HiC-GNN、HiCEGNN）受限于模型表达能力不足和跨分辨率泛化能力差：HiCEGNN的SE(3)-等变约束难以处理非对称结构（如锚定环），且所有方法仅依赖接触矩阵，缺乏显式几何先验（如染色质主轴或方向性链结构），导致在精细分辨率下性能显著下降。

针对上述瓶颈，本文提出InertialGenome——一种分辨率无关的几何Transformer框架。其核心创新在于：**通过惯性框架（Inertial Frame）进行姿态规范化**，将任意旋转/平移下的染色体坐标对齐到由惯性张量主轴定义的标准坐标系，消除姿态变化；**结合基于Nyström估计的几何感知位置编码（Geometry-aware Positional Encoding）**，高效捕获长程结构依赖，使Transformer能够学习分辨率无关的鲁棒表示。此外，模型采用混合损失函数（结构保持损失+值加权MSE损失），平衡全局拓扑保持与精确距离回归。

在两个单细胞Hi-C数据集（Frontal cortex和B-Lymphocyte）的四个分辨率（320kb、160kb、80kb、40kb）上，InertialGenome（以IG-3DMAX为代表）在dSCC和dRMSE指标上均优于所有四种基线方法（3DMAX、LorDG、HiC-GNN、HiCEGNN）。例如，在Frontal cortex 320kb分辨率下，IG-3DMAX的dSCC达到0.9030，较最佳基线3DMAX（0.8815）提升+0.0215（Table 1）；在B-Lymphocyte 1MB分辨率下，dSCC达0.9209，dRMSE降至0.0822（Table 2）。跨分辨率迁移学习实验中，从320kb迁移至160kb/80kb/40kb时，InertialGenome相比同分辨率原始模型提升高达5%（Table 3）。消融实验证实，移除惯性对齐、RoPE或Nyström分支均导致性能下降，其中移除Nyström在40kb精细分辨率上dRMSE上升0.0114（Table 7）。生物学验证方面，TAD域内/域间距离比（IG-3DMAX为0.760–0.814，显著低于HiCEGNN的0.914–0.993）和FISH距离趋势均与已知生物学规律一致（Table 8, Table 9）。

方法定位上，InertialGenome通过显式姿态规范化替代SE(3)-等变网络的隐式处理，为染色体3D重建提供了一种更灵活、表达能力更强的替代方案。主要局限包括：当前仅使用Hi-C接触矩阵，未整合多模态基因组数据；惯性框架的稳定性依赖于初始坐标的谱间隙，当谱间隙很小时（如Gram嵌入），主轴对齐可能不稳定。



从Hi-C接触矩阵重建染色质三维结构是理解基因组空间组织与功能的核心问题。现有方法主要分为两类：一是基于距离几何的数值优化方法（如3DMAX、LorDG），二是近年兴起的深度学习方法（如HiC-GNN、HiCEGNN）。然而，这两类方法均面临根本性瓶颈。

数值方法（3DMAX、LorDG）依赖迭代优化过程，其表达能力受限于手工设计的能量函数，难以捕获染色质高阶结构中的复杂非线性依赖。深度学习方法虽提升了表示能力，但存在更本质的缺陷：HiC-GNN采用图卷积网络，其感受野受限于局部邻域，无法有效建模染色质长程相互作用；HiCEGNN引入SE(3)-等变约束以增强物理一致性，但这种强对称性假设反而成为障碍——染色质结构中的锚定环、拓扑关联域（TAD）边界等关键非对称特征，在等变网络中会被隐式平滑化，导致结构保真度下降。此外，所有现有方法均仅依赖Hi-C接触矩阵作为输入，缺乏显式的几何先验（如染色质主轴的取向、链的线性方向性），使得模型在跨分辨率场景下泛化能力严重不足。

本文的动机正是针对上述三个核心缺口：**表达能力受限**、**对称性假设与真实结构矛盾**、**缺乏几何先验导致跨分辨率脆弱**。作者提出InertialGenome，其核心洞察在于：通过惯性框架（Inertial Frame）对输入坐标进行姿态规范化，将任意旋转/平移下的染色质坐标对齐到由惯性张量主轴定义的标准坐标系，从而在数据预处理阶段消除姿态变化，而非依赖网络架构的等变性。这一设计解耦了物理约束与模型架构，允许使用表达能力更强的Transformer直接学习结构特征。同时，结合基于Nyström估计的几何感知位置编码，高效捕获长程结构依赖，实现分辨率无关的鲁棒表示。



## 核心方法与创新机理

InertialGenome 的核心创新在于将**姿态规范化（Pose Canonicalization）**与**几何感知位置编码**相结合，使 Transformer 能够学习分辨率无关的鲁棒染色体 3D 表示，从而突破了现有方法（如 HiC-GNN、HiCEGNN）在模型表达能力和跨分辨率泛化上的瓶颈。

**核心洞察**：现有深度学习方法（尤其是 HiCEGNN 的 SE(3)-等变网络）通过对称性约束隐式处理旋转和平移，但强等变约束难以建模非对称结构（如锚定环），且所有基线方法仅依赖 Hi-C 接触矩阵，缺乏显式几何先验（如染色质主轴或方向性链结构）。InertialGenome 通过惯性框架将任意姿态下的染色体坐标对齐到由惯性张量主轴定义的标准坐标系，从而消除姿态变化；再利用 Nyström 方法对 3D 坐标的径向基函数（RBF）核进行低秩近似，高效捕获长程结构依赖。

**三个关键变更槽（Changed Slots）**：

1. **姿态规范化方法**：从无显式规范化（或 SE(3)-等变网络的隐式处理）变为**惯性框架规范化**。具体步骤包括质心平移、归一化惯性张量计算（$\hat{\mathbf{I}} = \frac{1}{N} \sum_{i=1}^N \left( \|\mathbf{c}_i'\|^2 \mathbf{I}_3 - \mathbf{c}_i' (\mathbf{c}_i')^T \right)$）、主轴对齐（通过对 $\hat{\mathbf{I}}$ 进行特征分解 $\hat{\mathbf{I}} = L \Lambda L^T$）以及手性校正，最终得到姿态不变表示 $\mathbf{s}_i = R \mathbf{c}_i'$（Section 3.1）。该方法的稳定性由 Davis–Kahan 定理控制：主轴对齐的鲁棒性取决于输入坐标协方差矩阵的谱间隙 $\delta(\mathbf{C}^*) = \mu_1 - \mu_2$。实验表明，当谱间隙较大时（如 3DMax 嵌入 $\delta \approx 18.6$），对齐稳定；当谱间隙接近零时（如 Gram 嵌入 $\delta \approx 0.0000$），主轴方向对噪声敏感（Table 4, Figure 5）。

2. **位置编码**：从标准 Transformer 位置编码或图神经网络的边特征变为**几何感知位置编码**。该编码包含两个互补分支：（a）**3D-RoPE**：将 3D 空间编码分解为三个独立的 2D 旋转子空间（对应 (x,y)、(y,z)、(z,x) 平面），作用于查询向量；（b）**Nyström 位置编码**：通过可学习锚点对 RBF 核进行低秩近似，高效建模全局结构依赖。初始 token 表示为语义嵌入与原始空间坐标的拼接 $\mathbf{x}_i = [\mathbf{E}_{\mathrm{token}}(t_i); \mathbf{s}_i] \in \mathbb{R}^d$（Section 3.2）。

3. **损失函数**：从单一 MSE 损失变为**混合损失**：$\mathcal{L}_{\mathrm{total}} = \alpha \mathcal{L}_{\mathrm{struct}} + \beta \mathcal{L}_{\mathrm{weighted.mse}}$，其中 $\beta = 1 - \alpha$。结构保持损失 $\mathcal{L}_{\mathrm{struct}}$ 为双向 KL 散度（通过 $\lambda$ 平衡假阳性和遗漏），值加权 MSE 损失 $\mathcal{L}_{\mathrm{weighted-mse}}$ 基于真实距离值排名分配自适应权重。消融实验（Table 6）表明，$\alpha=0.1/0.5$ 时取得最佳权衡，纯结构损失（$\alpha=1.0$）在精细分辨率上 dRMSE 显著升高。

**决定性证据**：
- 在单细胞 Hi-C 数据集（Frontal cortex 和 B-Lymphocyte）的四个分辨率上，InertialGenome 的 dSCC 和 dRMSE 均优于所有四种基线方法（Table 1, Table 2）。例如，在 Frontal cortex 320kb 分辨率下，IG-3DMAX 的 dSCC 达 0.9030，较 3DMAX 提升 0.0215。
- 跨分辨率迁移学习（320kb→160kb/80kb/40kb）中，InertialGenome 相比同分辨率原始模型提升高达 5%（Table 3）。
- 消融实验（Table 7）证实，移除惯性对齐、RoPE 或 Nyström 分支均导致性能下降，其中移除 Nyström 在精细分辨率（40kb）上 dRMSE 上升 0.0114。
- TAD 验证（Table 8）中，IG-3DMAX 的 intra/inter 距离比（0.760–0.814）显著低于 HiCEGNN（0.914–0.993），且 Mann–Whitney U 检验 p 值极小，表明其重建结构更符合生物学先验。
- FISH 验证（Table 9）中，预测的 L1–L2 距离（0.8–2.3）均短于 L2–L3 距离（3.3–13.1），与 Hi-C 接触概率趋势一致。

**证据强度说明**：上述证据置信度均≥0.95，但需注意惯性框架的稳定性依赖于初始坐标的谱间隙——当谱间隙很小时（如 Gram 嵌入），主轴对齐可能不稳定，该局限性在论文中明确讨论但未完全解决。



![[assets/figures/papers/iclr26_0003_OwLl8Xi6JG_A_Resolution-Agnostic_Geometric_Transformer_for/figures/001_Figure_1.jpg]]
*Figure 1: Overview of chromosome 3D reconstruction using Hi-C technology. (A): Experimental implementation of Hi-C for obtaining contact matrix information. (B): Computational pipeline for 3D structure reconstruction via mathematical modeling or machine learning based on the Hi-C contact matrix*

InertialGenome的整体pipeline采用“数值初始化 → 姿态规范化 → 几何感知Transformer编码 → 混合损失优化”的四阶段架构，核心设计目标是在不依赖SE(3)-等变网络的前提下，通过显式几何先验实现跨分辨率的稳定重建。

**输入与初始化**：pipeline的输入为Hi-C接触矩阵，首先通过距离转换公式 $D_{ij} = IF_{ij}^{-\gamma}$（$\gamma \in [0.1, 0.2, ..., 2]$）将接触频率转换为空间距离，然后由数值方法（3DMAX或LorDG）生成初始3D坐标 $\mathbf{C}^* \in \mathbb{R}^{N \times 3}$。这一设计确保所有后续方法（包括基线）共享相同的初始结构，实现公平比较。

**模块A：惯性框架规范化**（Section 3.1, Figure 2A）——这是pipeline的关键瓶颈突破点。原始坐标 $\mathbf{C}^*$ 经过四个子步骤变换为姿态不变表示：①质心平移 $\bar{c} = \frac{1}{N} \sum_{i=1}^N \mathbf{c}_i$ 消除平移自由度；②归一化惯性张量计算 $\hat{\mathbf{I}} = \frac{1}{N} \sum_{i=1}^N \left( \|\mathbf{c}_i'\|^2 \mathbf{I}_3 - \mathbf{c}_i' (\mathbf{c}_i')^T \right)$；③特征分解 $\hat{\mathbf{I}} = L \Lambda L^T$ 获取主轴方向；④通过旋转矩阵 $R$ 将中心化坐标变换为 $\mathbf{s}_i = R \mathbf{c}_i'$，并辅以手性校正。该模块的因果机制在于：通过将任意旋转/平移下的染色体坐标对齐到由惯性张量主轴定义的标准坐标系，消除了姿态变化对后续学习的影响。其稳定性由Davis–Kahan定理控制，即特征向量扰动上界 $\sin \angle(u, \widetilde{u}) \leq \frac{\|\Delta A\|_2}{\delta}$ 取决于谱间隙 $\delta = \mu_1 - \mu_2$。实验证据显示，当初始坐标来自3DMAX时（$\delta \approx 18.6$），对齐稳定；而Gram嵌入（$\delta \approx 0$）会导致主轴方向不稳定（Table 4, Figure 5），这解释了为什么IG-Gram性能远低于IG-3DMAX（Table 5）。

**模块B：几何感知位置编码**（Section 3.2, Figure 2B）——该模块将规范化后的坐标 $\mathbf{s}_i$ 与语义嵌入拼接为初始token表示 $\mathbf{x}_i = [\mathbf{E}_{\mathrm{token}}(t_i); \mathbf{s}_i] \in \mathbb{R}^d$，然后通过两条并行路径编码空间信息：①3D旋转位置编码（3D-RoPE）将3D空间分解为三个独立的2D旋转子空间（对应(x,y)、(y,z)、(z,x)平面），对查询向量施加旋转操作；②Nyström位置编码通过可学习锚点对径向基函数（RBF）核进行低秩近似，高效捕获长程结构依赖。该模块提供了三种应用模式（Selective/Separate/Full），其中Selective模式在保持特征表达的同时降低了计算开销。

**模块C：Transformer编码器**（Figure 2C）——基于位置编码的注意力机制，学习结构特征并输出校正后的3D坐标。Transformer架构相较于基线方法（HiC-GNN的图卷积网络、HiCEGNN的SE(3)-等变图网络）提供了更强的建模能力，能够处理非对称结构（如锚定环）——这是HiCEGNN的强对称性约束所难以处理的。

**训练与优化**：pipeline采用混合损失函数 $\mathcal{L}_{\mathrm{total}} = \alpha \mathcal{L}_{\mathrm{struct}} + \beta \mathcal{L}_{\mathrm{weighted.mse}}$（$\beta = 1 - \alpha$），其中结构保持损失 $\mathcal{L}_{\mathrm{struct}}$ 通过双向KL散度（$\lambda$平衡假阳性和遗漏）保持全局拓扑，值加权MSE损失 $\mathcal{L}_{\mathrm{weighted.mse}}$ 基于真实距离值排名分配自适应权重，强调高接触概率（短距离）区域的精确重建。消融实验表明，$\alpha=0.1/0.5$时取得最佳权衡，纯结构损失（$\alpha=1.0$）在精细分辨率上dRMSE显著升高（Table 6）。

**模块间关系与数据流**：整个pipeline形成“输入→A→B→C→输出”的线性流，其中模块A的输出直接作为模块B的输入，模块B的位置编码注入模块C的注意力计算。关键设计在于：惯性框架规范化（A）作为姿态消除的前置步骤，使得后续的几何感知编码（B）和Transformer学习（C）能够在标准化的坐标系中进行，避免了模型需要隐式学习旋转不变性的负担。这与HiCEGNN的SE(3)-等变网络形成对比——后者通过架构约束处理对称性，但牺牲了处理非对称结构的能力。

**证据强度评估**：pipeline整体架构的各个模块均有明确的公式定义和消融实验支持（Table 7），但“惯性框架稳定性依赖于谱间隙”这一机制仅在附录中通过Gram vs. 3DMAX对比验证（Table 4, Figure 5），缺乏对不同谱间隙阈值下性能的系统性分析。此外，pipeline在极精细分辨率（如10kb以下）上的行为尚未验证，这是需要后续研究补充的开放问题。



InertialGenome 的核心创新在于将物理惯性框架与基于Nyström估计的几何感知Transformer相结合，替代了传统SE(3)-等变网络的隐式姿态处理。其核心模块包括：惯性框架规范化、几何感知位置编码（3D-RoPE + Nyström编码）、以及混合损失函数。

### 惯性框架规范化

该模块旨在消除染色体3D坐标的任意旋转和平移变化，将其对齐到一个由惯性张量主轴定义的姿态不变坐标系。具体流程如下：

1.  **质心平移**：计算初始3D坐标 $\mathbf{c}_i$ 的质心 $\bar{c} = \frac{1}{N} \sum_{i=1}^N \mathbf{c}_i$，得到中心化坐标 $\mathbf{c}_i' = \mathbf{c}_i - \bar{c}$。
2.  **惯性张量计算**：从中心化坐标估计归一化惯性张量 $\hat{\mathbf{I}} = \frac{1}{N} \sum_{i=1}^N \left( \|\mathbf{c}_i'\|^2 \mathbf{I}_3 - \mathbf{c}_i' (\mathbf{c}_i')^T \right)$。
3.  **主轴对齐**：对惯性张量进行特征分解 $\hat{\mathbf{I}} = L \Lambda L^T$，其中 $\Lambda$ 包含特征值，$L$ 的列定义了主轴方向。通过旋转矩阵 $R$ 将中心化坐标变换到姿态不变表示 $\mathbf{s}_i = R \mathbf{c}_i'$。
4.  **手性校正**：确保主轴坐标系满足右手定则，保证物理一致性。

**关键分析**：该模块的稳定性直接受限于初始坐标的谱间隙 $\delta(\mathbf{C}^*) = \mu_1 - \mu_2$，即样本协方差矩阵最大两个特征值之差。根据Davis–Kahan定理，扰动前后特征向量夹角的正弦值上界为 $\sin \angle(u, \widetilde{u}) \leq \frac{\|\Delta A\|_2}{\delta}$。这意味着当谱间隙很小时，主轴对齐会非常不稳定，例如在Gram嵌入中（谱间隙 δ ≈ 0），其方向对噪声极其敏感，而3DMax嵌入（谱间隙 δ ≈ 18.6）则非常稳定。这是该模块的一个关键失败模式。

### 几何感知位置编码

在姿态规范化后，模型通过两种互补的编码方式将3D空间信息注入Transformer：

1.  **3D旋转位置编码 (3D-RoPE)**：将标准RoPE扩展到3D空间，通过将3D空间分解为三个独立的2D旋转子空间（对应于xy, yz, zx平面）来实现。其核心操作是对查询向量应用旋转：
    
$$
R_{\mathbf{s}_x, \mathbf{s}_y, \mathbf{s}_z} q^{\mathrm{raw}} = \left[ \begin{array}{l} q_0^{\mathrm{raw}} \\ q_0^{\mathrm{raw}} \\ q_2^{\mathrm{raw}} \\ q_3^{\mathrm{raw}} \\ q_4^{\mathrm{raw}} \\ q_5^{\mathrm{raw}} \end{array} \right] \odot \left[ \begin{array}{l} \cos(s_x \theta_0) \\ \cos(s_x \theta_0) \\ \cos(s_y \theta_0) \\ \cos(s_y \theta_0) \\ \cos(s_z \theta_0) \\ \cos(s_z \theta_0) \end{array} \right] + \left[ \begin{array}{l} -q_1^{\mathrm{raw}} \\ q_0^{\mathrm{raw}} \\ -q_3^{\mathrm{raw}} \\ q_2^{\mathrm{raw}} \\ -q_5^{\mathrm{raw}} \\ q_4^{\mathrm{raw}} \end{array} \right] \odot \left[ \begin{array}{l} \sin(s_x \theta_0) \\ \sin(s_x \theta_0) \\ \sin(s_y \theta_0) \\ \sin(s_y \theta_0) \\ \sin(s_z \theta_0) \\ \sin(s_z \theta_0) \end{array} \right]
$$

    该编码提供了感知成对距离的能力。论文提出了三种应用模式：Selective（仅对空间维度编码）、Separate（空间与特征维度分别编码）、Full（对所有维度编码）。

2.  **Nyström位置编码**：基于径向基函数（RBF）核的低秩近似，通过一组可学习的锚点（landmarks）高效捕获全局长程结构依赖。该机制避免了直接计算所有点对间的核矩阵，显著降低了计算复杂度。

**关键分析**：消融实验（Table 7）证实，移除RoPE会一致性地降低dSCC和dRMSE，而移除Nyström分支在精细分辨率（40kb）上导致dRMSE上升0.0114，表明该编码在捕获精细结构时尤为重要。

### 混合损失函数

模型使用一个混合损失函数来平衡全局拓扑保持和精确距离回归：

$$
\mathcal{L}_{\mathrm{total}} = \alpha \mathcal{L}_{\mathrm{struct}} + \beta \mathcal{L}_{\mathrm{weighted.mse}}, \qquad \beta = 1 - \alpha
$$

1.  **结构保持损失** $\mathcal{L}_{\mathrm{struct}}$：采用双向KL散度，通过参数 $\lambda$ 平衡假阳性（false positives）和遗漏（misses）：
    
$$
\mathcal{L}_{\mathrm{struct}} = \lambda \sum_i \sum_{j\neq i} p_{j|i} \log \frac{p_{j|i}}{q_{j|i}} + (1-\lambda) \sum_i \sum_{j\neq i} q_{j|i} \log \frac{q_{j|i}}{p_{j|i}}
$$

    该损失旨在保持输入距离分布（$p$）与预测距离分布（$q$）之间的全局拓扑一致性。

2.  **值加权MSE损失** $\mathcal{L}_{\mathrm{weighted-mse}}$：基于真实距离值的排名分配自适应权重，强调短距离（高接触概率）的回归精度：
    
$$
\mathcal{L}_{\mathrm{weighted-mse}} = \sum_{v \in \mathcal{V}} w_v \cdot \frac{1}{N_v} \sum_{(i,j) \in \mathcal{T}_v} \left( y_{ij} - \hat{y}_{ij} \right)^2
$$

    其中，$\mathcal{V}$ 是按距离值划分的组，$w_v$ 是组权重。

**关键分析**：消融实验（Table 6）表明，当 $\alpha=0.1/0.5$ 时取得最佳权衡，而纯结构损失（$\alpha=1.0$）在精细分辨率上dRMSE显著升高，说明纯粹的拓扑约束不足以精确回归坐标。



## 实验与关键发现

### 主结果：InertialGenome在单细胞Hi-C重建中全面超越基线

在Frontal cortex和B-Lymphocyte两个单细胞Hi-C数据集上，InertialGenome（以IG-3DMAX为代表）在四个分辨率（320kb/160kb/80kb/40kb或1MB/500kb/250kb/125kb）的dSCC和dRMSE指标上均优于所有四种基线方法（3DMAX、LorDG、HiC-GNN、HiCEGNN）。以Frontal cortex测试集为例，IG-3DMAX在320kb分辨率下dSCC达到0.9030，较次优的3DMAX（0.8815）提升0.0215；在B-Lymphocyte测试集1MB分辨率下dSCC达到0.9209，较3DMAX（0.9012）提升0.0197（Table 1, Table 2）。值得注意的是，IG-3DMAX在精细分辨率（40kb/125kb）上的优势更为显著，说明其几何感知位置编码机制在数据稀疏时仍能有效捕获结构信息。

![[assets/figures/papers/iclr26_0003_OwLl8Xi6JG_A_Resolution-Agnostic_Geometric_Transformer_for/figures/003_Table_1.jpg]]
*Table 1: Performance comparison of six methods on 3D chromosome structure reconstruction from single-cell Hi-C data (Frontal cortex cell test set). Metrics report distance-based Spearman correlation (dSCC ↑) and root mean square error (dRMSE ↓) at four resolutions. Best results in bold*

![[assets/figures/papers/iclr26_0003_OwLl8Xi6JG_A_Resolution-Agnostic_Geometric_Transformer_for/figures/004_Table_2.jpg]]
*Table 2: Performance comparison of six methods on 3D chromosome structure reconstruction from single-cell Hi-C data (B-Lymphocyte cell test set). Metrics report distance-based Spearman correlation (dSCC ↑) and root mean square error (dRMSE ↓) at four resolutions. Best results in bold*

跨分辨率迁移学习实验（Table 3）进一步验证了模型的分辨率无关性：将320kb训练的IG-3DMAX直接迁移到160kb/80kb/40kb，性能相比同分辨率原始模型提升高达5%。而HiCEGNN的迁移结果则出现明显退化，表明强对称性约束（SE(3)-等变）限制了模型对尺度变化的适应能力。

![[assets/figures/papers/iclr26_0003_OwLl8Xi6JG_A_Resolution-Agnostic_Geometric_Transformer_for/figures/009_Table_3.jpg]]
*Table 3: Cross-resolution transfer results. Bold: improvement over same-resolution original model; underline: HICEGNN transfer improvement*

### 消融实验：三个核心组件缺一不可

Table 7的组件消融实验揭示了惯性框架、3D-RoPE和Nyström位置编码各自的贡献：
- **移除惯性对齐**：所有分辨率上dRMSE均上升，320kb从0.1547升至0.1641，说明姿态规范化是模型稳定性的基础。
- **移除RoPE**：dSCC和dRMSE均一致退化，证实旋转位置编码对空间关系建模的必要性。
- **移除Nyström分支**：在精细分辨率（40kb）上dRMSE上升0.0114，表明Nyström的低秩近似在数据稀疏时对长程依赖建模尤为关键。

损失权重消融（Table 6）显示，纯结构损失（α=1.0）在精细分辨率上dRMSE显著升高，而纯MSE损失（α=0）则丢失全局拓扑。最优权衡出现在α=0.1/0.5，此时结构正则化与坐标回归达到平衡。

### 生物验证：TAD与A/B compartment的结构一致性

TAD验证（Table 8）中，IG-3DMAX的intra/inter距离比（0.760–0.814）显著低于HiCEGNN（0.914–0.993），且Mann–Whitney U检验p值极小，表明IG-3DMAX重建的结构中同TAD内位点空间聚集更紧密，更符合生物学先验。Figure 4的可视化进一步显示，IG-3DMAX的TAD边界清晰，而HiCEGNN的域间距离与域内距离差异不明显。

A/B compartment验证（Figure 6）同样支持IG-3DMAX的优势：同compartment内距离显著小于不同compartment间距离，而HiCEGNN的分离度较弱。

FISH验证（Table 9）在GM12878细胞系的三个染色体（11、14、17）上，IG-3DMAX预测的L1–L2距离（0.8–2.3）均短于L2–L3距离（3.3–13.1），与Hi-C接触概率趋势一致，说明模型能正确恢复局部相对位置关系。

### 失败模式与局限性

1. **惯性框架的谱间隙依赖性**：Table 4显示，Gram嵌入的谱间隙δ≈0，导致主轴对齐不稳定（Figure 5中PC1角度随噪声快速增大），而3DMax嵌入的δ≈18.58则保持稳定。这说明惯性规范化对初始坐标质量敏感——当初始结构缺乏明确主方向时，对齐可能引入额外噪声。Table 5中IG-Gram的性能（dSCC 0.787–0.869）低于IG-3DMAX，印证了此限制。

![[assets/figures/papers/iclr26_0003_OwLl8Xi6JG_A_Resolution-Agnostic_Geometric_Transformer_for/figures/010_Table_4.jpg]]
*Table 4: Stability metrics for Chromosome 3 (320 kb)*

![[assets/figures/papers/iclr26_0003_OwLl8Xi6JG_A_Resolution-Agnostic_Geometric_Transformer_for/figures/012_Table_5.jpg]]
*Table 5: dSCC and dRMSE of IG-Gram on different resolutions*

2. **精细分辨率下的性能瓶颈**：尽管IG-3DMAX在40kb分辨率上仍优于基线，但dSCC（0.5890）和dRMSE（0.3256）相比粗分辨率显著下降，提示模型在数据极度稀疏时仍面临挑战。Nyström锚点数量和尺度参数的选择在高分辨率下可能成为新的瓶颈。

3. **跨分辨率迁移的局限性**：Table 3中，320kb→160kb迁移的dSCC（0.7399）低于160kb原始模型（0.8621），说明低分辨率训练会丢失高分辨率细节，迁移学习仅能部分补偿。这一差距在更精细分辨率上进一步扩大。

4. **实验泛化范围有限**：当前验证仅覆盖两个单细胞Hi-C数据集（Frontal cortex和B-Lymphocyte），且未涉及多模态数据（如ChIP-seq、RNA-seq）的整合。模型在群体Hi-C或其它物种上的表现尚待验证。



## 定位与知识库关联

### 与基线方法的关系

InertialGenome 定位于染色体3D重建方法谱系中“深度学习+显式几何先验”这一尚未被充分探索的生态位。其基线覆盖了该领域的两个主要分支：传统数值方法（3DMAX、LorDG）和深度学习方法（HiC-GNN、HiCEGNN）。

与数值方法相比，InertialGenome 的 Transformer 架构提供了更强的建模容量，能够从 Hi-C 接触矩阵中学习比简单距离几何约束更复杂的结构模式。实验证据表明，在 Frontal cortex 细胞测试集 320kb 分辨率下，IG-3DMAX 的 dSCC（0.9030）显著高于纯 3DMAX（0.8815），提升约 2.15 个百分点（Table 1）。然而，InertialGenome 的输入坐标仍依赖数值方法初始化（3DMAX 或 LorDG），因此其性能上限受限于初始结构的质量——这一依赖关系在附录 Table 4 和 Figure 5 中得到量化：当初始嵌入的谱间隙 δ 很小时（如 Gram 嵌入，δ≈0），惯性框架的主轴对齐变得不稳定，导致 IG-Gram 在精细分辨率下性能急剧下降（Table 5）。

与深度学习方法 HiC-GNN 和 HiCEGNN 相比，InertialGenome 的核心差异在于姿态处理策略。HiCEGNN 采用 SE(3)-等变图神经网络，通过架构约束隐式处理旋转/平移对称性；而 InertialGenome 通过惯性框架显式规范化姿态，再使用标准 Transformer 学习。这种“先对齐、后学习”的策略带来了两个关键优势：一是避免了等变网络对非对称结构（如锚定环）的表达限制；二是允许使用更灵活的 Transformer 架构。实验上，InertialGenome 在所有分辨率和两个数据集上均优于 HiCEGNN（Table 1, Table 2），且在 TAD 验证中，IG-3DMAX 的 intra/inter 距离比（0.760–0.814）显著低于 HiCEGNN（0.914–0.993），表明其对拓扑结构域的捕获更准确（Table 8）。

### 适用边界与条件

InertialGenome 的适用性受以下条件约束：

**输入质量依赖**：惯性框架的稳定性由初始坐标的谱间隙 δ = μ₁ - μ₂（样本协方差矩阵最大两个特征值之差）决定。Davis–Kahan 定理给出扰动界：特征向量夹角的正弦上界与谱间隙成反比。实验验证了这一理论预测：3DMax 嵌入的 δ≈18.58，其主轴在噪声下保持稳定；而 Gram 嵌入的 δ≈0，PC1 角度随噪声急剧增长（Figure 5）。因此，InertialGenome 仅在初始嵌入具有足够谱间隙时有效，对于谱间隙接近零的初始结构（如某些基于 MDS 的嵌入），惯性对齐本身可能引入额外误差。

**分辨率敏感性**：消融实验（Table 7）揭示不同组件在不同分辨率下的贡献差异。移除 Nyström 分支在精细分辨率（40kb）上导致 dRMSE 上升 0.0114，而在粗分辨率（320kb）上影响较小，说明长程依赖建模在精细尺度更为关键。相反，惯性对齐在所有分辨率上均贡献稳定提升（320kb 移除后 dRMSE 从 0.1547 升至 0.1641）。这暗示模型在极精细分辨率（如 10kb 以下）的性能可能受限于 Nyström 近似的精度和 Transformer 的计算开销。

**数据模态限制**：当前方法仅使用 Hi-C 接触矩阵作为唯一输入，未整合 ChIP-seq、RNA-seq 等多模态数据。这限制了模型在缺乏 Hi-C 数据的细胞类型或条件下的适用性，也意味着模型无法利用表观遗传标记等互补信息来约束重建。

### 局限与开放问题

**理论局限**：惯性框架本质上是将染色体视为刚体进行姿态规范化，但染色质在细胞核内是柔性聚合物，其惯性张量主轴可能随构象变化而漂移。当前方法仅对初始结构做一次对齐，未考虑对齐后结构变化对主轴的影响。这种“一次对齐”策略在多大程度上限制了模型对柔性构象的表达能力，尚需理论分析。

**实证局限**：实验仅在两个单细胞 Hi-C 数据集（Frontal cortex 和 B-Lymphocyte）上进行验证，泛化到其他细胞类型（如植物细胞、癌细胞）或物种（如小鼠、果蝇）尚未验证。跨分辨率迁移实验（Table 3）显示，IG-3DMAX 从 320kb 迁移到 160kb 时 dSCC 从 0.8621 降至 0.7399，虽优于 HiCEGNN 迁移结果，但性能损失仍显著，说明跨分辨率泛化的机制尚未完全解决。

**开放问题**：
1. **多模态集成**：如何将 ChIP-seq、RNA-seq 等数据作为额外 token 或约束融入 Transformer 框架？这需要解决异质数据对齐和特征融合问题。
2. **自适应谱间隙**：是否存在自适应调整惯性对齐策略的方法？例如，当谱间隙低于阈值时，降级为 SE(3)-等变网络或使用其他规范化策略。
3. **任务泛化性**：InertialGenome 的“姿态规范化 + 几何感知 Transformer”范式能否推广到其他生物分子结构预测任务（如蛋白质结构预测、RNA 二级结构建模）？这需要验证惯性框架在非染色体系统（如非连续、非链状结构）中的有效性。
4. **Nyström 配置优化**：Nyström 位置编码中锚点数量和 RBF 核尺度参数的选择对性能的影响尚未系统研究。是否存在与分辨率相关的自适应配置策略？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Resolution_Agnostic_Geometric_Transformer_for_Chromosome_Modeling_Using_Inertial_Frame.pdf

![[paperPDFs/ICLR_2026/A_Resolution_Agnostic_Geometric_Transformer_for_Chromosome_Modeling_Using_Inertial_Frame.pdf]]

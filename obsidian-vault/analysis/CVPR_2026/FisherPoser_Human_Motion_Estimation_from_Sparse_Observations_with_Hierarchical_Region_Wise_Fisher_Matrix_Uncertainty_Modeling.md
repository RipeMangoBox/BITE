---
title: "FisherPoser: Human Motion Estimation from Sparse Observations with Hierarchical Region-Wise Fisher-Matrix Uncertainty Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FisherPoser_Human_Motion_Estimation_from_Sparse_Observations_with_Hierarchical_Region_Wise_Fisher_Matrix_Uncertainty_Modeling.pdf
project_link: null
code_link: null
aliases:
- FisherPoser
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将姿态估计建模为SO(3)上Matrix-Fisher分布的概率推断，并通过区域特定令牌和层次化递归解码传播姿态与不确定性，从而在稀疏观测下显式量化并利用逐关节置信度。
primary_logic: 在SO(3)流形上为每个关节预测Matrix-Fisher分布，其模式给出最可能姿态，浓度参数量化旋转不确定性；结合身体分区（五区域）和运动链路递归解码，既实现校准的逐关节置信度，又保证运动学一致性，解决了稀疏观测下的一对多歧义。
claims:
- 在Protocol 1上，MPJRE从之前最好的2.28°降至2.04°（相对提升10.5%），MPJPE从31.9 mm降至29.7 mm（提升6.9%），均达到最优。
- 消融实验表明，移除区域令牌和层次递归（Ours-Fisher）导致MPJPE从29.7升至38.7；用高斯分布替代Matrix-Fisher（Ours-AR-Gaussian）导致MPJPE升至45.0且Jitter升高，证明SO(3)上矩阵-Fisher不确定性建模和区域/层次设计的必要性。
- AMASS-P1 上 MPJRE(°) = 2.04
- AMASS-P1 上 MPJPE(mm) = 29.7
---

# FisherPoser: Human Motion Estimation from Sparse Observations with Hierarchical Region-Wise Fisher-Matrix Uncertainty Modeling

> [!tip] 核心洞察
> 在SO(3)流形上为每个关节预测Matrix-Fisher分布，其模式给出最可能姿态，浓度参数量化旋转不确定性；结合身体分区（五区域）和运动链路递归解码，既实现校准的逐关节置信度，又保证运动学一致性，解决了稀疏观测下的一对多歧义。

| 字段 | 内容 |
|------|------|
| 中文题名 | FisherPoser：基于分层区域Fisher矩阵不确定性建模的稀疏观测人体运动估计 |
| 英文题名 | FisherPoser: Human Motion Estimation from Sparse Observations with Hierarchical Region-Wise Fisher-Matrix Uncertainty Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xia_FisherPoser_Human_Motion_Estimation_from_Sparse_Observations_with_Hierarchical_Region-Wise_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FisherPoser |
| Dataset | AMASS-P1, AMASS-P2 |

> [!tip] 效果简介
> - AMASS-P1 上，MPJRE(°) 2.04 vs 2.28 (HMDPoser) (-0.24 (相对提升10.5%))；MPJPE(mm) 29.7 vs 31.9 (HMDPoser) (-2.2 (相对提升6.9%))。
> - AMASS-P2 上，MPJRE(°) 3.89 vs 4.27 (HMDPoser) (-0.38 (相对提升8.9%))；Jitter 3.18 vs 4.99 (RPM-Reactive) (-1.81 (相对降低36.3%))。

## 概述

从稀疏VR设备（仅头显与双手柄共三个6-DoF追踪器）恢复全身人体运动，本质上是一个严重的一对多歧义问题：下肢关节缺乏直接观测，确定性回归极易产生脆性解，且无法提供可靠的逐关节置信度。**FisherPoser** 将姿态估计重新建模为 SO(3) 流形上的概率推断——为每个关节预测一个 **Matrix-Fisher 分布**，其模式给出最可能旋转，浓度参数量化旋转不确定性。在此基础上，方法引入**五区域身体分区**（躯干、左右臂、左右腿）构建区域令牌，并通过沿四肢运动链的**层次化递归解码**传播父关节的分布与不确定性，在保证运动学一致性的同时实现校准的逐关节置信度估计。

在 AMASS 基准的两个协议上，FisherPoser 均取得最优结果：Protocol 1 上 MPJRE 降至 2.04°（相对提升 10.5%），MPJPE 降至 29.7 mm（提升 6.9%）；Protocol 2 上 MPJRE 降至 3.89°（提升 8.9%），Jitter 降至 3.18（相对降低 36.3%）。消融实验进一步验证，移除区域令牌与层次递归设计会使 MPJPE 从 29.7 mm 升至 38.7 mm，而将 Matrix-Fisher 替换为欧氏空间高斯分布则导致 MPJPE 升至 45.0 mm 且时间平滑性严重恶化，确认了 SO(3) 流形上适当不确定性参数化与区域/层次设计的必要性。

## 背景与动机

### 稀疏VR运动估计的歧义困境

在消费级虚拟现实（VR）设备中，用户通常仅佩戴头戴显示器（HMD）和双手控制器，共提供三个6-DoF追踪信号。要从这极度稀疏的观测中恢复包含22个关节的全身运动，本质上是一个严重欠定的逆问题：同一组稀疏输入可能对应无数种合理的全身姿态——例如，HMD和手部位置固定时，下肢可以站立、下蹲、交叉或迈步。现有的确定性回归方法（如**AvatarPoser** (Jiang et al., ECCV 2022)、**AGRoL** (Du et al., CVPR 2023)、**AvatarJLM** (Zheng et al., ICCV 2023)、**SAGE** (Feng et al., CVPR 2024)、**HMDPoser** (Dai et al., CVPR 2024)、**RPM-Reactive** (Barquero et al., CVPR 2025)）直接学习从稀疏输入到单一姿态的映射，在面临这种一对多歧义时，往往产生脆性的平均化解，导致下肢姿态抖动、运动学不一致，且无法告知用户“哪些关节的估计不可靠”。

### 现有方法的三个结构性缺口

1. **确定性输出缺乏置信度**：主流方法将姿态估计视为回归问题，输出单一的关节旋转向量或矩阵。这种点估计无法表达预测的不确定性，尤其对于远离观测源的下肢关节，模型既不知道“自己不知道”，也无法将这种无知量化为可操作的置信度信号。

2. **身体整体建模忽略区域差异**：现有方法通常将身体编码为单一全局特征，平等对待所有关节。然而，在稀疏VR场景下，不同身体区域的信息丰度差异悬殊——躯干因靠近HMD和双手控制器而具有较强观测约束，而四肢末端（如脚踝）几乎完全缺乏直接观测。整体建模无法针对性地为弱观测区域分配专门的表示容量。

3. **并行预测违背运动链先验**：人体骨骼形成严格的运动学树，父关节的旋转直接决定子关节的全局位置。但现有方法大多并行预测所有关节，忽略了这一强结构先验，导致预测姿态可能出现运动学不一致，且无法利用父关节已推断的信息来约束子关节的歧义空间。

### 核心动机：概率化、区域化、层次化

FisherPoser的核心动机是系统性地填补上述三个缺口。首先，将姿态估计重新定义为**SO(3)流形上的概率推断问题**，为每个关节预测一个矩阵-Fisher（Matrix-Fisher）分布——其模态给出最可能的旋转，浓度参数量化旋转不确定性，从而在几何一致的空间中实现校准的逐关节置信度。其次，引入**身体分区表示**，将身体划分为躯干、左右臂、左右腿五个运动学区域，通过区域特定令牌驱动局部化的矩阵-Fisher回归，使模型能够为观测弱区分配差异化容量。最后，设计**沿运动链的层次化递归解码器**，从父关节向子关节顺序传播姿态分布与不确定性，将运动学先验显式注入推理过程，既提升运动一致性，又利用父关节信息约束子关节的歧义空间。

## 核心创新

FisherPoser 的核心创新在于将稀疏观测下的一对多歧义问题显式建模为 **SO(3) 流形上的概率推断**，并通过**区域感知与层次递归**的双重结构设计，实现校准的逐关节置信度估计和运动学一致的姿态预测。相较于现有确定性回归或缺乏校准的生成式方法，FisherPoser 在三个关键设计维度上做出了根本性改变。

### 1. 输出表征与不确定性建模：从确定性回归到 Matrix-Fisher 分布

现有方法（如 **AvatarPoser** (Jiang et al., ECCV 2022)、**AGRoL** (Du et al., CVPR 2023)、**HMDPoser** (Dai et al., CVPR 2024) 等）将姿态估计建模为确定性回归问题——直接输出关节的轴角或旋转矩阵，这导致在弱观测区域（如下肢）产生脆性解，且无法量化预测的可靠程度。FisherPoser 将每个关节的姿态表示为 SO(3) 上的 **Matrix-Fisher 分布**：

$$p(R_{t}^{(j)} \mid \mathcal{F}_{t}^{(j)}) = \frac{1}{c(F_{t}^{(j)})} \exp(\mathrm{tr}((F_{t}^{(j)})^{\top} R_{t}^{(j)}))$$

其中参数矩阵 $F_{t}^{(j)}$ 通过 SVD 分解 $F_{t}^{(j)} = U_{t}^{(j)} S_{t}^{(j)} V_{t}^{(j)\top}$ 可同时提取两个关键信息：**模态旋转** $\hat{R}_{t}^{(j)}$（最可能的姿态）和**浓度参数**（量化旋转不确定性）。这一设计使得模型在稀疏观测下不仅能给出最优姿态估计，还能显式告知哪些关节的预测不可靠——例如 Figure 4 显示，左膝在剧烈运动时浓度显著下降，准确反映了观测信息不足导致的置信度降低。

消融实验（Table 3）验证了这一设计的关键性：当用欧氏空间的高斯分布替代 SO(3) 上的 Matrix-Fisher 分布（Ours-AR-Gaussian）时，MPJPE 从 29.7 mm 急剧恶化至 45.0 mm，且时间平滑性指标 Jitter 从 5.33 飙升至 20.73，表明在非欧流形上使用适当的概率参数化对于姿态估计精度和时序一致性至关重要。

### 2. 身体建模粒度：从整体回归到五区域语义分区

现有方法通常将身体视为单一整体进行编码与回归，忽略了不同身体区域在稀疏观测下的信息不对称性——例如，手部控制器直接约束手臂姿态，而下肢完全缺乏直接观测。FisherPoser 将身体划分为**五个语义区域**（躯干、左臂、右臂、左腿、右腿），通过注意力池化构建区域特定令牌（Region-wise Token），驱动各区域的 Matrix-Fisher 分布回归。

这一设计的因果机制在于：区域令牌使得模型能够根据各区域的实际观测信息量自适应地调整预测策略。对于有直接观测约束的区域（如手臂），区域令牌可提取高置信度特征；对于缺乏观测的下肢，区域令牌则捕捉运动先验和躯干传导信息，并以较低的浓度参数反映其固有不确定性。

消融实验（Table 2）表明，移除区域令牌和层次递归设计（Ours-Fisher）后，MPJPE 从 29.7 mm 升至 38.7 mm，相对退化达 30.3%，证明了区域感知建模对于处理稀疏观测下信息不对称问题的必要性。

### 3. 关节点解码顺序：从并行预测到运动链递归传播

现有方法的并行预测策略忽略了人体运动链的物理依赖关系——子关节的姿态受父关节约束，这种结构先验在稀疏观测下尤为珍贵。FisherPoser 设计了**层次化递归解码器**，沿四肢运动链（肩→肘→腕，髋→膝→踝）顺序传播父关节的分布信息：子关节的特征向量显式拼接父关节的 Matrix-Fisher 参数 $F_{\mathrm{pred},t}^{(p)}$ 和浓度向量 $\mathbf{u}_{\mathrm{pred},t}^{(p)}$，并通过混合机制融合直接预测与传播结果：

$$\mathbf{f}_{t}^{(c)} = [\mathbf{z_H}_{t}; \mathbf{\mathcal{T}}_{r(c),t}; \mathrm{vec}(F_{\mathrm{pred},t}^{(p)}); \mathbf{u}_{\mathrm{pred},t}^{(p)}]$$

这一设计的深层优势在于：父关节的不确定性通过浓度参数显式传递给子关节，使得模型在父关节预测不可靠时（如髋关节缺乏观测），子关节（如膝关节）能够相应地降低置信度，而非盲目继承一个不可靠的确定性姿态。这种**不确定性沿运动链的诚实传播**是 FisherPoser 实现校准置信度的关键机制。

Table 2 的消融结果表明，区域令牌与层次递归具有互补性——两者联合移除导致性能大幅退化，验证了“区域感知提供语义先验 + 层次递归保证运动学一致性”的双重设计逻辑。

## 整体框架

FisherPoser 的整体 pipeline 将稀疏 VR 观测（三个 6‑DoF 追踪器：HMD 及左右手柄）映射为全身体姿的概率推断，核心由三个级联模块构成（Figure 2）：

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/002_Figure_2.jpg]]
*Figure 2: Overview of FisherPoser, consisting of three core components: (1) A Transformer-based auto-regressive motion encoding for global context extraction. (2) Region-wise token construction for local Matrix-Fisher estimation. (3) A recursive propagator that refines limb poses hierarchically for kinematic consistency*

1. **因果 Transformer 编码器（Autoregressive Temporal Encoder）**  
   以自回归方式融合当前帧的稀疏追踪信号与运动历史，生成全局上下文特征 $\mathbf{z}_H^t$。该模块为后续所有区域和关节点预测提供统一的时序感知表征。

2. **区域令牌构建（Region‑wise Token Construction）**  
   将身体划分为五个语义区域——躯干（torso）、左臂、右臂、左腿、右腿。利用预定义的区域语义锚点，通过交叉注意力从全局上下文中池化出区域特定令牌 $\mathcal{T}_{r,t}$。每个区域令牌驱动对应区域内所有关节的初步 Matrix‑Fisher 分布回归，实现区域粒度的条件化建模。

3. **层次化递归传播器（Hierarchical Recursive Propagator）**  
   沿四肢运动链（肩→肘→腕，髋→膝→踝）顺序传播父关节的分布信息。子关节的特征向量显式拼接父关节的 Matrix‑Fisher 参数矩阵 $F_{\mathrm{pred},t}^{(p)}$ 及其浓度向量 $\mathbf{u}_{\mathrm{pred},t}^{(p)}$，与全局上下文和区域令牌共同输入细化网络。直接预测的分布 $F_{\mathrm{dir},t}^{(c)}$ 与递归传播得到的分布 $F_{\mathrm{prop},t}^{(c)}$ 通过可学习的混合系数 $\lambda$ 融合，形成子关节的最终分布。这一设计在保持运动学一致性的同时，使不确定性沿运动链向下游关节传导。

**输入/输出流**：输入为每帧三个追踪器的 6‑DoF 位姿，输出为 22 个关节各自在 SO(3) 上的 Matrix‑Fisher 分布。分布的模态给出最可能旋转，浓度参数量化逐关节置信度——弱观测关节（如下肢远端）自动获得低浓度（高不确定性），强观测关节（如头部、手部）获得高浓度（低不确定性）。训练时通过负对数似然损失 $\mathcal{L}_{MF}$ 和测地线模态对齐损失 $\mathcal{L}_{\mathrm{mode}}$ 联合优化，推理时直接取模态旋转作为确定性姿态估计。

### 补充图表

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/001_Figure_1.jpg]]
*Figure 1: FisherPoser can estimate the full-body motion using three tracking signals (HMD and hand controllers)*

## 核心模块与公式推导

FisherPoser 的核心架构由三个级联模块构成（Figure 2），其设计逻辑是：先通过自回归时序编码器提取全局运动上下文，再按身体区域构建区域令牌以驱动局部矩阵-Fisher 分布预测，最后沿四肢运动链递归传播父关节的姿态与不确定性，实现运动学一致的逐关节概率估计。

### 3.1 姿态表征与矩阵-Fisher 分布

**姿态向量化**：对于时刻 $t$，将所有关节的相对旋转矩阵 $R_t^{(j)} \in SO(3)$ 向量化并拼接为 198 维姿态表示（22 个关节 × 9 维旋转矩阵元素）：

$$
\pmb{\theta}_{t} = \mathrm{vec}\left(\{R_{t}^{(j)}\}_{j=1}^{J}\right) \in \mathbb{R}^{9J} = \mathbb{R}^{198}
\tag{1}
$$

**矩阵-Fisher 分布**：FisherPoser 的核心创新在于将每个关节的旋转建模为 SO(3) 流形上的矩阵-Fisher 分布，而非确定性姿态。对于关节 $j$，其旋转 $R_t^{(j)}$ 的概率密度由参数矩阵 $F_t^{(j)} \in \mathbb{R}^{3\times3}$ 定义：

$$
p(R_{t}^{(j)} \mid \mathcal{F}_{t}^{(j)}) = \frac{1}{c(F_{t}^{(j)})} \exp\left(\mathrm{tr}\left((F_{t}^{(j)})^{\top} R_{t}^{(j)}\right)\right)
\tag{2}
$$

其中 $c(F)$ 为归一化常数。该分布具有两个关键性质：
- **模态旋转**：对 $F$ 进行奇异值分解 $F = U S V^{\top}$（Eq.3），则分布的模态（最可能旋转）为 $\hat{R} = U\,\mathrm{diag}(1,1,|\mathbf{UV}|)\,V^{\top}$（Eq.4）；
- **浓度参数**：奇异值 $S = \mathrm{diag}(s_1, s_2, s_3)$ 量化了旋转不确定性——奇异值越大，分布越集中，置信度越高。

### 3.2 自回归时序编码器

该模块以自回归方式融合稀疏 VR 观测（头显与双手柄的 6-DoF 追踪信号）与运动历史，生成全局上下文 $Z_H$。编码器基于 Causal Transformer 架构，确保时序因果性，为后续区域和关节级预测提供统一的时序特征基础（Section 3.2, Figure 2）。

### 3.3 区域令牌构建与局部矩阵-Fisher 回归

FisherPoser 将身体划分为五个语义区域：躯干、左臂、右臂、左腿、右腿。针对每个区域 $r$，利用语义锚点关节和交叉注意力机制从全局上下文 $Z_H$ 中池化出区域特定令牌 $\mathcal{T}_{r,t}$。这些令牌驱动对应区域内各关节的矩阵-Fisher 参数 $F_{\mathrm{dir},t}^{(j)}$ 的直接预测。

该设计的因果逻辑是：稀疏观测对不同区域的信息量差异显著（如双手柄提供丰富的上肢约束，而下肢几乎无直接观测），区域令牌使模型能够为不同区域学习差异化的先验强度和不确定性校准策略。

### 3.4 层次化递归传播器

这是 FisherPoser 实现运动学一致性的关键模块。沿四肢运动链（肩→肘→腕，髋→膝→踝）顺序处理，将父关节的分布信息显式传播给子关节。

**子关节特征构建**：对于子关节 $c$，拼接四类信息形成细化特征向量（Eq.14）：

$$
\mathbf{f}_{t}^{(c)} = \left[\mathbf{z_H}_{t}; \mathbf{\mathcal{T}}_{r(c),t}; \mathrm{vec}\left(F_{\mathrm{pred},t}^{(p)}\right); \mathbf{u}_{\mathrm{pred},t}^{(p)}\right]
$$

其中 $\mathbf{u}_{\mathrm{pred},t}^{(p)}$ 为父关节的浓度向量（由奇异值导出），$\mathrm{vec}(F_{\mathrm{pred},t}^{(p)})$ 为父关节的矩阵-Fisher 参数向量化。该特征使子关节能够“感知”父关节的当前姿态估计及其置信度。

**混合预测**：子关节的最终矩阵-Fisher 参数通过直接预测与递归传播的加权混合得到：

$$
F_{\mathrm{pred},t}^{(c)} = (1 - \lambda) F_{\mathrm{dir},t}^{(c)} + \lambda F_{\mathrm{prop},t}^{(c)}
$$

其中 $F_{\mathrm{prop},t}^{(c)}$ 由父关节分布经运动链变换传播而来，$\lambda$ 为可学习或预设的混合系数。最终通过 SVD 和浓度调整得到 $F_{\mathrm{final},t}^{(j)}$（Eq.17），用于损失计算。

### 3.5 训练目标

FisherPoser 采用多损失联合训练：

**负对数似然损失（NLL）**：基于矩阵-Fisher 分布的最大似然估计（Eq.5）：

$$
\mathcal{L}_{MF} = -\log(p(R;F)) = \log(c(F)) - \mathrm{tr}[F^{T}R]
$$

**测地线模态对齐损失**：惩罚预测模态旋转与真值之间的旋转误差（Eq.19）：

$$
\mathcal{L}_{\mathrm{mode}} = \sum_{j=1}^{22} \left\| \log\left(\hat{R}_{t}^{(j)\top} R_{\mathrm{gt},t}^{(j)}\right) \right\|_{2}^{2}
$$

此外还引入了物理相关损失项（如速度、加速度平滑约束），具体细节见补充材料。

### 补充图表

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/003_Figure_4.jpg]]
*Figure 4: Visualization on the changes in concentration of left knee; the lower the concentration, the higher uncertainty*

## 实验与分析

### 主要结果与定量对比

FisherPoser 在两个标准协议上均实现了最优性能，验证了概率不确定性建模与区域-层次解码设计的有效性。Table 1 汇总了与现有方法的全面对比。

在 **Protocol 1**（AMASS-P1）上，FisherPoser 的旋转误差 **MPJRE** 降至 **2.04°**，相比此前最优的 **HMDPoser**（Dai et al., CVPR 2024）的 2.28° 相对提升 **10.5%**；位置误差 **MPJPE** 降至 **29.7 mm**，较 HMDPoser 的 31.9 mm 提升 **6.9%**。这一结果表明，在仅有三个 6-DoF 追踪器的极端稀疏观测下，FisherPoser 的逐关节 Matrix-Fisher 分布能有效解决一对多歧义，生成更准确的姿态模式。

在 **Protocol 2**（AMASS-P2）上，FisherPoser 同样表现最优：MPJRE 为 **3.89°**（HMDPoser 为 4.27°，提升 8.9%），且时间平滑性指标 **Jitter** 降至 **3.18**，相比 **RPM-Reactive**（Barquero et al., CVPR 2025）的 4.99 相对降低 **36.3%**。Jitter 的大幅下降说明，区域令牌和层次递归传播不仅提升了空间精度，还通过沿运动链的分布传播增强了时序一致性，抑制了帧间抖动。

Figure 3 展示了三条测试序列的定性对比，FisherPoser 预测的姿态在四肢末端（尤其是下肢）与真值吻合度明显优于基线方法，直观印证了定量指标的提升。

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of motion estimation on three test sequences from AMASS-P1*

### 消融实验

为厘清各组件的贡献，论文设计了系统消融（Table 2 与 Table 3）。

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/006_Table_2.jpg]]
*Table 2: The ablation study on our method*

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/007_Table_3.jpg]]
*Table 3: The ablation study on the uncertainty estimation*

**区域令牌与层次递归的必要性**（Table 2）：移除区域令牌和层次递归传播后，模型退化为仅保留 Matrix-Fisher 输出的全局解码器（Ours-Fisher），Protocol 1 上 MPJPE 从 **29.7 mm 急剧升至 38.7 mm**。这表明，身体五区域划分和沿运动链的递归传播对于稀疏观测下的精准姿态估计是不可或缺的——全局单一表征无法有效区分不同区域的运动模式与不确定性特征。

**SO(3) 流形上 Matrix-Fisher 分布的关键作用**（Table 3）：将 Matrix-Fisher 分布替换为欧氏空间高斯分布（Ours-AR-Gaussian）后，MPJPE 从 29.7 mm 骤升至 **45.0 mm**，且 Jitter 从 5.33 恶化至 **20.73**。这一对比揭示了在 SO(3) 流形上对旋转进行适当概率参数化的根本重要性：欧氏空间高斯无法刻画旋转空间的紧致性和几何结构，导致模式估计偏差和严重的时间抖动。Figure 5 的可视化进一步显示，高斯变体的预测姿态出现明显畸变和漂移。

### 不确定性量化的有效性

Figure 4 可视化了左膝关节的浓度参数随时间的变化曲线。在运动剧烈或遮挡导致观测信息不足的时刻，浓度显著降低，对应的高不确定性区域与真实误差增大区域高度吻合。这说明 FisherPoser 的逐关节浓度参数能够提供**校准的置信度估计**，为下游应用（如运动重定向、安全决策）提供了可靠的元信息。

### 失败模式与局限性

论文指出的主要失败模式来自**自回归架构的长期漂移**：在长时间序列推理中，预测误差会沿时间轴累积，导致末端关节的姿态逐渐偏离真值。这一问题在快速连续运动中尤为明显，因为历史误差通过自回归编码器持续影响后续帧的全局上下文。此外，当下肢长期缺乏有效观测时（如静坐场景），不确定性持续高位，但模式估计本身缺乏外部锚点进行校正。

> **注意**：论文未提供针对漂移的定量分析或具体失败案例的误差曲线，上述局限性描述基于作者在论文中的声明，建议读者结合补充材料进一步验证。

### 方法对比总结

| 方法 | 核心策略 | MPJRE (°) P1 | MPJPE (mm) P1 | Jitter P2 |
|------|----------|-------------|---------------|-----------|
| AvatarPoser (Jiang et al., ECCV 2022) | 确定性回归 | — | — | — |
| AGRoL (Du et al., CVPR 2023) | 确定性回归 | — | — | — |
| AvatarJLM (Zheng et al., ICCV 2023) | 确定性回归 | — | — | — |
| SAGE (Feng et al., CVPR 2024) | 确定性回归 | — | — | — |
| HMDPoser (Dai et al., CVPR 2024) | 确定性回归 | 2.28 | 31.9 | — |
| RPM-Reactive (Barquero et al., CVPR 2025) | 生成式采样 | — | — | 4.99 |
| **FisherPoser** | **SO(3) Matrix-Fisher + 区域-层次解码** | **2.04** | **29.7** | **3.18** |

FisherPoser 在所有指标上均取得最优，且消融实验证实其三个核心设计——SO(3) 上 Matrix-Fisher 分布、五区域令牌、层次递归传播——是互补且必要的。

### 补充图表

![[assets/figures/papers/paper_list_l1047_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_FisherPoser_Human/figures/005_Figure_5.jpg]]
*Figure 5: Visualization results for ablation study*

## 方法谱系与知识库定位

### 1. 核心创新与差异化定位

FisherPoser 的核心创新在于将稀疏 VR 观测下的全身体姿估计从确定性回归范式迁移至 SO(3) 流形上的概率推断框架。与现有方法相比，FisherPoser 在三个关键维度上实现了范式级改进：

**输出表征的根本转变。** 现有主流方法——包括 **AvatarPoser** (Jiang et al., ECCV 2022)、**AGRoL** (Du et al., CVPR 2023)、**AvatarJLM** (Zheng et al., ICCV 2023)、**SAGE** (Feng et al., CVPR 2024)、**HMDPoser** (Dai et al., CVPR 2024) 和 **RPM-Reactive** (Barquero et al., CVPR 2025)——均输出确定性姿态（轴角或旋转矩阵），或采用无校准的生成式采样策略。这类确定性回归在稀疏观测下存在根本性缺陷：仅三个 6-DoF 追踪器（头显和双手控制器）提供的约束极为稀疏，导致全身体姿估计存在严重的一对多歧义，确定性模型易产生脆性解，且无法量化对弱观测关节（如下肢）的置信度。FisherPoser 将每个关节的旋转建模为 SO(3) 上的 Matrix-Fisher 分布，其参数矩阵 $F$ 的奇异值分解同时给出最可能旋转（模式）和浓度参数（不确定性量化），实现了几何一致的、可校准的逐关节置信度估计。

**身体建模粒度的层级化。** 现有方法普遍将身体视为单一整体进行编码与回归，忽略了不同身体区域在稀疏观测下的信息不对称性——躯干和手臂受追踪器直接约束，而下肢完全依赖运动先验推断。FisherPoser 引入区域特定令牌机制，将身体划分为五个语义区域（躯干、左/右臂、左/右腿），通过注意力池化提取区域特定特征，使模型能够为不同区域学习差异化的不确定性模式。

**解码顺序的运动学一致性。** 现有方法通常并行预测所有关节姿态，忽略了运动链中父子关节间的因果依赖关系。FisherPoser 设计层次化递归解码器，严格沿四肢运动链（肩→肘→腕，髋→膝→踝）顺序传播父关节的 Matrix-Fisher 分布和浓度信息到子关节，并通过混合直接预测与传播结果的方式实现运动学一致性约束。

### 2. 方法谱系中的位置

FisherPoser 处于稀疏观测人体运动估计、概率姿态建模和 SO(3) 流形学习的交叉点。

**稀疏 VR 运动估计谱系。** 从 AvatarPoser 的纯确定性回归，到 AGRoL 引入注意力机制增强上下文建模，再到 HMDPoser 的混合密度网络尝试，该领域逐步认识到不确定性建模的必要性。FisherPoser 是首个在 SO(3) 流形上为每个关节显式建模完整 Matrix-Fisher 分布的方法，将不确定性量化从辅助输出提升为核心表征。

**概率姿态建模谱系。** 此前工作多采用欧氏空间的高斯分布或混合密度网络对姿态进行概率建模，但这些方法忽略了旋转空间的非欧几何特性。FisherPoser 的消融实验（Table 3）提供了关键证据：用欧氏空间高斯分布替代 SO(3) 上的 Matrix-Fisher 分布（Ours-AR-Gaussian），MPJPE 从 29.7 mm 急剧升至 45.0 mm，且时间平滑性显著恶化（Jitter 20.73 vs 5.33），充分证明了在流形上选择适当不确定性参数化的必要性。

**区域化与层次化建模谱系。** 身体分区策略在计算机视觉中已有先例，但将其与概率分布传播和运动学递归相结合是 FisherPoser 的独特贡献。消融实验（Table 2）表明，移除区域令牌和层次递归（Ours-Fisher）导致 MPJPE 从 29.7 mm 升至 38.7 mm，验证了区域感知条件化和肢体递归机制的必要性与互补性。

### 3. 适用边界与局限

FisherPoser 的设计假设和适用边界需明确认识：

**稀疏观测假设。** 方法专为三追踪器 VR 场景设计（头显+双手控制器），其区域化策略和不确定性建模的优势在此设定下最为显著。当观测密度增加（如增加腰部或脚部追踪器）时，一对多歧义自然减弱，概率建模的相对收益可能收窄。

**自回归架构的时序脆弱性。** 论文明确指出自回归架构在长时间序列推理中可能出现漂移失败，预测误差随时间累积。这一局限在真实世界长时间会话中尤为关键，当前方法缺乏对累积误差的显式检测和校正机制。

**运动先验的依赖性。** 下肢关节完全依赖从训练数据中学习的运动先验进行推断，当遇到训练分布外的运动模式（如特殊步态、极限动作）时，Matrix-Fisher 分布的模式可能偏离真值，且浓度参数可能给出错误的高置信度——即模型可能"自信地犯错"。

### 4. 开放问题与后续方向

基于 FisherPoser 的框架特性，以下方向值得关注：

**环境锚点融合。** 如何将接触信息、地形几何等环境约束纳入 Matrix-Fisher 分布的参数化，以进一步降低下肢不确定性？当前框架仅依赖运动学先验，融合物理环境信息可从本质上缩小一对多歧义空间。

**时序鲁棒性增强。** 针对自回归漂移问题，可能的改进方向包括：引入非自回归的全局时序编码、设计漂移检测与重校准模块、或结合滤波框架（如扩展卡尔曼滤波在 SO(3) 上的变体）进行在线校正。

**人-物交互建模。** 当人体与物体接触时（如坐椅子、推桌子），接触约束可提供强先验。将交互约束编码为 Matrix-Fisher 分布的附加条件，有望同时提升姿态估计的物理合理性和不确定性校准质量。

**跨域泛化。** 当前方法在 AMASS 基准上验证，向真实 VR 设备部署时需处理传感器噪声特性差异、用户身体尺寸变化和实时性约束。FisherPoser 的概率输出天然适合与传感器融合框架结合，但实时推理效率尚需验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/FisherPoser_Human_Motion_Estimation_from_Sparse_Observations_with_Hierarchical_Region_Wise_Fisher_Matrix_Uncertainty_Modeling.pdf]]
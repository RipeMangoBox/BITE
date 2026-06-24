---
title: Dual Octree Graph Networks for Learning Adaptive Volumetric Shape Representations
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Dual_Octree_Graph_Networks_for_Learning_Adaptive_Volumetric_Shape_Representations.pdf
project_link: "https://wang-ps.github.io/dualocnn"
code_link: null
aliases:
- DOGN
- DOGNLAVSR
tags:
- SIGGRAPH_2022
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 基于对偶八叉树图的多分辨率邻域信息聚合方式 —— 将相邻不同尺度八叉树节点的特征按固定方向融合，并通过可学习的权重索引进行图卷积。
primary_logic: 利用对偶八叉树图的半正则性，将图卷积退化为索引权重的GEMM操作，既保留了多尺度特征交互的能力，又实现了高度并行化；同时配合神经MPU模块保证体积场的连续性，从而在自适应特征体积上高效学习高质量的形状表征。
claims:
- 在ShapeNet 13类形状重建测试中，本方法在所有指标（CD、NC、IoU、F-Score）上均取得最优，且显著超越DeepMLS和ConvONet。
- 在D-Faust无监督人体重建任务上，Chamfer距离为0.048，比IGR（0.499）低一个数量级，且推理速度快394倍。
- 消融实验表明，对偶八叉树图卷积（FULLGRAPH）比单尺度卷积或KNN图卷积（KPConv、EdgeConv）在精度和训练效率上均有显著提升。
- D-Faust (unsupervised surface reconstruction) 上 CD↓ = 0.048
---

# Dual Octree Graph Networks for Learning Adaptive Volumetric Shape Representations

> [!tip] 核心洞察
> 利用对偶八叉树图的半正则性，将图卷积退化为索引权重的GEMM操作，既保留了多尺度特征交互的能力，又实现了高度并行化；同时配合神经MPU模块保证体积场的连续性，从而在自适应特征体积上高效学习高质量的形状表征。

| 字段 | 内容 |
|------|------|
| 中文题名 | 对偶八叉树图网络用于学习自适应体积形状表征 |
| 英文题名 | Dual Octree Graph Networks for Learning Adaptive Volumetric Shape Representations |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://wang-ps.github.io/dualocnn) · [Project](https://wang-ps.github.io/dualocnn") |
| Topic | #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Dual Octree Graph Networks |
| Dataset | D-Faust, ShapeNet autoencoder |

> [!tip] 效果简介
> - D-Faust (unsupervised surface reconstruction) 上，CD↓ 0.048 vs 0.499 (IGR) (-0.451)；Time↓ 0.281s vs 110.8s (IGR) (394× faster)。
> - ShapeNet autoencoder 上，CD↓ 0.89 vs 1.37 (IM-Net) (-0.48)；NC↑ 0.921 vs 0.811 (IM-Net) (+0.110)；Time↓ 0.143s vs 0.841s (IM-Net) (5.9× faster)。

## 概要

现有三维体积表示方法面临一个共同瓶颈：规则网格CNN显存与算力随分辨率立方增长，稀疏体素CNN忽略空区域特征，神经隐式MLP推理缓慢且缺乏通用编码器，难以同时实现高效计算、精细几何重建和对噪声/不完整输入的鲁棒性。本文提出**对偶八叉树图网络（Dual Octree Graph Networks）**，核心思路是利用对偶八叉树图的半正则性，将多尺度邻域特征按固定方向融合，并通过可学习的权重索引将图卷积退化为高效GEMM操作，同时配合神经MPU模块保证体积场的连续性，从而在自适应特征体积上学习高质量形状表征。在ShapeNet 13类形状重建中，本方法在所有指标（Chamfer距离、法向一致性、IoU、F-Score）上均取得最优，显著超越DeepMLS和ConvONet；在D-Faust无监督人体重建任务上，Chamfer距离低至0.048，比IGR的0.499降低一个数量级，推理速度快394倍。消融实验证实，对偶八叉树图卷积相比单尺度卷积或KNN图卷积在精度与训练效率上均有显著提升。该方法将自适应八叉树特征体积与图卷积编码器-解码器相结合，为体积形状表征提供了一种高效且通用的学习框架。

## 核心方法与创新机理

### 问题背景与核心瓶颈

现有三维形状表示学习方法面临一个根本性矛盾：规则网格CNN受限于立方增长的显存与算力，稀疏体素CNN忽略空区域特征导致信息丢失，而神经隐式MLP方法虽然连续性好但推理速度极慢且缺乏通用编码器。本文识别的核心瓶颈是：**如何在自适应分辨率下实现高效的多尺度邻域特征聚合，同时保证体积场的连续性**。现有方法要么在规则网格上做单尺度卷积（如O-CNN），要么在隐式空间做全局MLP查询（如IM-Net、IGR），无法同时兼顾效率、精度和鲁棒性。

### 核心创新：对偶八叉树图卷积

本方法的核心创新在于**将对偶八叉树图的半正则性转化为计算优势**。具体而言，八叉树节点在三维空间中具有固定的六个邻域方向（上、下、左、右、前、后），即使相邻节点处于不同深度级别，其相对方向仍然离散且有限。基于这一观察，作者将图卷积中的权重函数 $W(\Delta p_{ij})$ 退化为一个可学习的权重矩阵 $W = (W_1, \dots, W_k)$，其中 $k$ 对应固定方向的数量。邻域特征聚合时，通过方向索引 $\mathcal{I}(\Delta p_{ij})$ 直接检索对应权重，避免了传统图卷积中动态计算权重的开销。

**Changed Slot 1：邻域聚合方式** —— 从单尺度3D卷积或KNN图卷积转变为多层级对偶八叉树图卷积。传统方法（如O-CNN）仅在相同深度的八叉树节点上进行卷积，丢失了跨尺度信息交互；KPConv和EdgeConv等通用图卷积需要动态计算边权重，训练效率低。本方法的关键公式为：

$$F_i = \sum_{j \in N_i} W_{\mathcal{I}(\Delta p_{ij})} \times [F_j \parallel D_j \parallel \Delta p_{ij}]$$

其中 $F_j$ 为邻域节点特征，$D_j$ 为节点深度编码，$\Delta p_{ij}$ 为相对位置差，$\parallel$ 表示特征拼接。该设计同时融合了多尺度几何信息和拓扑深度信息。

### 高效实现机制

图卷积的计算实现（Fig. 5）是该方法工程化的关键。通过 `torch.scatter` 操作，将邻域节点特征按固定方向聚合成一个形状为 $(N, C_i, 7)$ 的张量 $M$（7列分别对应中心节点及六个方向）。更新后的节点特征通过矩阵乘法 $F = M \times W$ 计算，复杂度仅为 $O(7N \times C_i \times C_o)$。由于该操作退化为高度优化的GEMM运算，训练速度比KPConv和EdgeConv快5倍以上（Table 3: 17.4h vs 89.1h/96.5h）。

![[assets/figures/papers/paper_list_l29_https_wang_ps_github_io_dualocnn/figures/006_Figure_5.jpg]]
*Figure 5: The computation of the proposed graph convolution with a 2D example. The numbers in the dual octree represent the indices of node features. The matrix ?? is constructed via torch.scatter. The first column of ?? stores the features of the centering nodes, and other columns store the features in up, down, left and right directions. In matrix ??, x represents the node in the corresponding direction is missing and zeros are filled, ?? in the first row of ?? represents the sum of features at node 1 and node 4, ?? represents the sum of features at node 5 and node 6. The updated features ?? are computed via a matrix product of ?? and a small weight matrix ??*

### 神经MPU模块：保证场连续性

**Changed Slot 2：场连续性保证** —— 从离散占用预测或全局MLP转变为基于单位分解的局部MLP混合。稀疏体素方法在每个节点独立预测离散占用值，导致表面不连续；坐标式MLP虽然连续但推理慢。本方法提出的Neural MPU模块将自适应特征体积映射为连续三维场：

$$F(x) = \frac{\sum_i c_i \cdot w_i(x) \cdot \Phi(x, F_i)}{\sum_i c_i \cdot w_i(x)}$$

其中 $\Phi(x, F_i)$ 是一个紧凑的MLP，以查询点 $x$ 和节点特征 $F_i$ 为输入预测局部场值；$c_i$ 为可学习的置信度权重；$w_i(x)$ 为线性B样条权重函数：

$$w_i(x) = B\left(\frac{|x - o_i|}{r_i}\right), \quad B(x) = \begin{cases} 1 - |x| & \text{if } |x| < 1; \\ 0 & \text{otherwise.} \end{cases}$$

该权重函数以节点中心 $o_i$ 和单元半径 $r_i$ 定义局部支撑域，保证C0连续性。多个局部预测通过加权平均融合为全局连续场，既保留了自适应分辨率的高效性，又避免了离散化伪影。

### 完整流水线与模块因果关系

**模块1：对偶八叉树图构建**（Section 3.1, Fig. 3-4）。从输入点云出发，先构建八叉树结构，再通过渐进式算法生成对偶图。对偶图的节点对应八叉树叶节点的角点，边连接空间相邻的节点。渐进构建过程从深度0开始，逐层检测无效节点（其子节点在八叉树中存在），将其替换为子节点并更新边连接。整个预处理过程仅需约2ms（Intel I7 CPU，3000点输入）。

**模块2：图CNN编码器-解码器**（Section 3.2, Fig. 6）。采用U-Net架构，输入为深度6的对偶八叉树图。编码器通过图卷积和下采样操作逐步提取多尺度特征，解码器通过上采样和跳跃连接恢复分辨率。网络同时预测两个输出：八叉树节点细分状态（用于自适应分辨率）和节点特征体积（用于场值查询）。下采样和上采样操作在相同深度的节点上进行，通过池化和插值实现。

**模块3：神经MPU**（Section 3.3）。将模块2输出的特征体积映射为连续场。查询任意三维点时，找到其所在的八叉树单元，提取对应节点特征，通过局部MLP和B样条混合得到场值。该模块使得推理时无需遍历所有节点，仅需查询包含目标点的局部区域。

**因果关系链**：模块1提供多尺度拓扑结构 → 模块2利用该结构进行图卷积特征提取，其中方向索引机制使得跨尺度消息传递高效可行 → 模块3将离散特征体积连续化，补偿八叉树离散化的精度损失。三个模块形成闭环：八叉树的自适应性降低计算量，图卷积的半正则性保证训练效率，Neural MPU保证输出质量。

### 训练与推理路径

**训练损失**包括三项。八叉树损失 $\mathcal{L}_{octree}$ 为节点细分状态的二值交叉熵。回归损失 $\mathcal{L}_{regress}$ 监督场值及其梯度：

$$\mathcal{L}_{regress} = \sum_d \frac{1}{N\rho} \sum_{x \in \mathcal{P}} \left( \lambda_v \|F(x) - G(x)\|_2^2 + \|\nabla F(x) - \nabla G(x)\|_2^2 \right)$$

梯度项的引入使得预测场在表面附近具有正确的法向信息，消融实验表明移除该项会导致CD轻微上升（0.267→0.269）。无监督训练时使用梯度损失 $\mathcal{L}_{grad}$，鼓励占用场在输入点附近为零且梯度匹配法向。

**推理路径**：输入点云 → 八叉树构建（~2ms）→ 对偶图生成 → U-Net前向传播（~280ms，V100 GPU）→ Neural MPU场值查询 → Marching Cubes提取表面。端到端推理时间约0.28s，比IGR（110.8s）快394倍。

![[assets/figures/papers/paper_list_l29_https_wang_ps_github_io_dualocnn/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our method illustrated with an 2D example. From left to right: given a point cloud as input, our method first constructs a dual octree graph and then applies a graph-CNN-based encoder-decoder network on the input graph to extract an adaptive feature volume. After that, the learned Neural MPU module maps the adaptive feature volume to a 3D volumetric field of the resulting surface*

![[assets/figures/papers/paper_list_l29_https_wang_ps_github_io_dualocnn/figures/003_Figure_3.jpg]]
*Figure 3: A 2D illustration of dual octree graph (using quadtree). (a): an octree built from the points sampled from the orange curve. (b)&(c): the dual octree graphs of the octree under different resolutions, the green lines in the figure are graph edges*

![[assets/figures/papers/paper_list_l29_https_wang_ps_github_io_dualocnn/figures/007_Figure_6.jpg]]
*Figure 6: A U-Net built on our basic graph CNN operators. This network takes a dual octree graph with depth 6 as input, and predicts the octree splitting and corresponding volumetric fields*

## 实验与关键发现

### 主结果：形状重建与表面重建

**ShapeNet 多类别重建。** 在 ShapeNet 13 类形状重建测试集上，本方法在所有评估指标上均取得最优结果（Table 1）。与当时领先的 **DeepMLS**（Liu et al., CVPR 2021）和 **ConvONet**（Peng et al., ECCV 2020）相比，Chamfer 距离（CD，乘以 100）和法向一致性（NC）均有显著提升。在 5 个未见类别上的泛化测试中，括号内指标同样保持领先，表明自适应特征体积对形状类别变化具有较好的鲁棒性。从噪声点云重建的视觉效果（Fig. 7）显示，本方法能够恢复更精细的几何细节，而 ConvONet 在场景级重建中甚至出现缺失部分物体的情况（Fig. 9）。

**D-Faust 无监督人体重建。** 在 D-Faust 数据集的无监督表面重建任务上，本方法展现出压倒性优势（Table 6）。与隐式神经表示方法 **IGR**（Gropp et al., ICML 2020）相比，Chamfer 距离从 0.499 降至 **0.048**，降低了一个数量级；同时推理时间从 110.8 秒缩短至 **0.281 秒**，加速约 **394 倍**。这一速度优势源于自适应特征体积 + 局部 MLP 的架构设计，无需像 IGR 那样对每个查询点执行深层 MLP 前向传播。视觉对比（Fig. 10）进一步佐证：IGR 无法重建手部，且在脚部产生虚假表面片，而本方法输出完整且拓扑正确。

**ShapeNet 自编码器。** 在形状自编码器任务上（Table 7），本方法以 CD = **0.89**、NC = **0.921** 显著优于 **IM-Net**（Chen and Zhang, CVPR 2019）的 CD = 1.37、NC = 0.811，推理速度快 **5.9 倍**（0.143s vs 0.841s）。视觉结果（Fig. 13）显示 IM-Net 存在伪影且细节缺失，而本方法重建质量更接近真值。

### 关键消融实验

**对偶八叉树图卷积的必要性。** Table 2 系统对比了不同邻域聚合策略：仅使用单尺度卷积的 **SINGLESCALE**（CD = 0.291, IoU = 0.889）和仅从细到粗单向边的 **FINE→COARSE**（CD = 0.276, IoU = 0.899）均不及完整的对偶八叉树图卷积 **FULLGRAPH**（CD = **0.267**, IoU = **0.904**）。这表明双向多尺度信息流——即细节点聚合粗节点上下文、粗节点聚合细节点细节——对高质量特征学习至关重要。Fig. 8 的可视化消融进一步印证：单尺度卷积重建结果存在明显噪声和不连续区域。

**图卷积实现的效率优势。** Table 3 将本方法的图卷积与通用图卷积算子 **KPConv** 和 **EdgeConv** 进行对比。在相同网络架构下替换卷积算子，本方法训练时间仅为 **17.4 小时**，而 KPConv 需 89.1 小时、EdgeConv 需 96.5 小时，加速超过 **5 倍**；同时重建精度（CD = 0.267）也优于两者。这一效率优势源于对偶八叉树图的半正则性：将邻域聚合退化为固定方向上的 `torch.scatter` 操作和 GEMM 矩阵乘法（Eq. (2)，Fig. 5），避免了通用图卷积的动态邻域搜索和逐边权重计算开销。

**Neural MPU 梯度项的作用。** 移除回归损失中的梯度项后，性能略微下降（CD 从 0.267 升至 0.269），但仍优于 DeepMLS 和 ConvONet。这表明梯度监督对连续场学习有正向贡献，但并非性能主导因素；自适应特征体积本身已编码了足够的几何信息。

### 失败模式与适用边界

**八叉树结构的被动依赖性。** 当前方法的特征体积自适应性完全取决于输入点云预建的八叉树结构，网络仅预测节点是否细分（通过 $\mathcal{L}_{octree}$），而非主动优化树结构本身。这意味着：若初始八叉树因点云稀疏或噪声而遗漏关键几何区域，网络难以在推理过程中动态增补节点。这构成了方法的上限——表示质量受限于前端八叉树构建策略。

**图下采样的深度限制。** 当前的图下采样和上采样操作每次仅在同一深度的节点上进行，而非在所有叶节点上同步执行。这限制了多尺度消息传递的效率，可能阻碍深层特征向浅层细粒度节点的有效传播。作者将此列为开放问题，暗示存在进一步提升空间。

**形状理解任务的扩展性未验证。** 本方法仅初步在 ModelNet40 分类上测试（92.4% 精度，略低于 DGCNN 和 PCT），尚未在语义分割、目标检测等三维理解任务上充分验证对偶八叉树图卷积的有效性。其固定方向权重索引的设计是否适用于需要长距离语义依赖的任务，仍需进一步探索。

**场景级重建的细节缺失。** 尽管在 D-Faust 人体重建上表现优异，但场景级重建（Fig. 9）中仍存在部分细节缺失，且未与专门针对大规模场景的方法（如基于稀疏卷积的 MinkowskiEngine 方案）进行系统对比。当前实验主要验证了中等规模形状（单物体、人体）的表示能力，向更大规模场景的扩展需要评估显存和计算效率的 scaling 行为。

### 公平性说明

所有对比方法在相同数据集划分上训练和测试，使用一致的评估指标（Chamfer 距离、法向一致性、IoU、F-Score）。时间测量均在 NVIDIA V100 GPU 上执行，且排除 Marching Cubes 后处理时间以公平对比推理效率。值得注意的边界条件：ConvONet 因使用均匀体积 CNN 在分辨率为 64 时显存溢出，而本方法因自适应八叉树稀疏性保持可管理的内存占用，这在高分辨率场景下构成实质优势。

![[assets/figures/papers/paper_list_l29_https_wang_ps_github_io_dualocnn/figures/008_Table_1.jpg]]
*Table 1: Quantitative evaluation on the ShapeNet dataset. The numbers outside and inside the parentheses are the results on the testing dataset of 13 categories from ShapeNet and on the 5 unseen categories respectively. The Chamfer distance (CD) is multiplied by a factor of 100 for better display*

![[assets/figures/papers/paper_list_l29_https_wang_ps_github_io_dualocnn/figures/009_Table_2.jpg]]
*Table 2: Ablation study on the necessity of incorporating multiscale voxels in the convolution. O-CNN and SINGLESCALE involve voxels of single scale in the convolution. FINE→COARSE adds coarse voxels for fine-scale voxels when doing convolution. FULLGRAPH operates on the full dual octree graph*

## 定位与知识库关联

本文在三维体积表示学习领域的关键贡献在于**改变了邻域聚合（neighborhood aggregation）和场连续性（field continuity）两个核心设计槽位**，构建了一种在计算效率、几何精度和鲁棒性之间取得新平衡的自适应体积表示。

### 相对于已有方法的本质差异

**槽位一：邻域聚合方式**。现有方法在此槽位上主要采取两种策略：(1) 基于规则网格或稀疏体素的单尺度3D卷积，如 **O-CNN** (Wang et al., SIGGRAPH 2017) 仅在八叉树同一深度的节点间进行卷积，忽略了跨尺度特征交互；(2) 基于KNN的通用图卷积，如 **KPConv** (Thomas et al., ICCV 2019) 和 **EdgeConv** (Wang et al., ACM Trans. Graph. 2019)，虽然支持不规则邻域，但邻域搜索和动态核计算导致训练效率低下（消融实验中KPConv训练耗时89.1小时，EdgeConv 96.5小时）。本文的**对偶八叉树图卷积**将邻域聚合限定在六个固定方向（上、下、左、右、前、后），利用八叉树节点间的相对位置差 $\Delta p_{ij}$ 作为索引直接检索可学习权重矩阵 $W_{\mathcal{I}(\Delta p_{ij})}$，将图卷积退化为高度优化的GEMM矩阵乘法操作（训练仅需17.4小时）。这一设计**既保留了多尺度特征交互能力（FULLGRAPH在CD和IoU上显著优于SINGLESCALE），又实现了5倍以上的训练加速**。

**槽位二：场连续性保证**。基于稀疏体素的方法（如 **ConvONet** (Peng et al., ECCV 2020)）在每个节点处预测离散的占据概率，缺乏节点间的连续性约束；而基于坐标的MLP方法（如 **DeepMLS** (Liu et al., CVPR 2021)、**IGR** (Gropp et al., ICML 2020)）虽能产生连续场，但推理时需要为每个查询点执行完整的前向传播，速度极慢。本文的**神经MPU模块**通过B样条权重函数 $w_i(x) = B(|x - o_i|/r_i)$ 将局部MLP预测值融合为全局连续场，既保证了C⁰连续性，又因MLP极轻量（仅数层）而保持了快速推理。在D-Faust无监督重建任务上，本方法推理速度（0.281s）比IGR（110.8s）快394倍，且Chamfer距离（0.048）远低于IGR（0.499）。

### 知识库挂载点

本工作可挂载到**自适应体积表示学习**和**图神经网络几何处理**两个知识节点：

1. **与自适应体积表示的连接**：本方法延续了从 **O-CNN** 到 **Adaptive O-CNN** (Wang et al., SIGGRAPH Asia 2019) 的自适应八叉树表示线，但将特征存储从八叉树节点转移到了对偶图节点，使得每个图节点自然地连接相邻不同尺度的八叉树单元。与 **ACORN** (Martel et al., SIGGRAPH 2021) 等动态优化八叉树结构的方法不同，本文的八叉树结构完全由输入点云预建，未在学习过程中动态调整——这是作者明确指出的局限性。

2. **与图卷积几何处理的连接**：本方法属于“利用几何先验简化图卷积”这一设计范式。与 **KPConv** 的半径邻域核函数和 **EdgeConv** 的动态KNN图不同，对偶八叉树图通过固定方向索引将图结构“半正则化”，在通用性和计算效率之间找到了一个实用折中点。这一思路可追溯到 **MeshCNN** (Hanocka et al., ACM Trans. Graph. 2019) 在网格边上定义固定卷积核的设计哲学。

### 适用边界与后续启发

**适用边界**：(1) 本方法假设输入为点云且可构建有意义的八叉树结构，对于极度稀疏或高度非均匀采样的输入，八叉树质量可能下降；(2) 特征体积的自适应性完全取决于预建八叉树，对于需要主动分配表示容量的任务（如包含高频细节的局部区域），缺乏动态调整机制；(3) 图卷积设计目前针对体积场重建和生成任务优化，扩展到语义分割等任务时仅初步验证（ModelNet40分类92.4%，略低于DGCNN和PCT）。

**后续启发**：(1) 作者提出的开放问题——在所有不同深度的叶节点上同步进行下采样和上采样——可能进一步提升多尺度消息传递效率，值得后续工作探索；(2) 将本方法的图卷积与 **ACORN** 等可学习八叉树结构优化方法结合，有望在保持效率的同时实现更优的表示紧凑性；(3) 对偶八叉树图的“半正则”图卷积设计范式可启发其他层次化几何表示（如多分辨率网格、层次化点云）上的高效图网络设计。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Dual_Octree_Graph_Networks_for_Learning_Adaptive_Volumetric_Shape_Representations.pdf]]
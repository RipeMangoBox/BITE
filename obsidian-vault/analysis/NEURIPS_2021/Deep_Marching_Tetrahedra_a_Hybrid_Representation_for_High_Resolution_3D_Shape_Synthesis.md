---
title: "Deep Marching Tetrahedra: a Hybrid Representation for High-Resolution 3D Shape Synthesis"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/Deep_Marching_Tetrahedra_a_Hybrid_Representation_for_High_Resolution_3D_Shape_Synthesis.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/DMTet/
aliases:
- DMTD
- DMTHRHR3SS
tags:
- NEURIPS_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入一种可微的行进四面体（Marching Tetrahedra）层，将可变形四面体网格上编码的隐式SDF转换为显式三角网格，从而使损失函数可以直接定义在显式曲面之上，并通过反向传播联合优化几何与拓扑。"
primary_logic: "通过可微行进四面体层连接隐式SDF和显式表面网格，构建了一个端到端的混合3D表示。该表示既能保留隐式场对任意拓扑的建模能力，又能利用显式表面损失直接监督几何细节，同时通过网格变形和选择性细分实现高效的高分辨率合成。"
claims:
- "DMTET在粗糙体素上采样器的形状合成任务中，所有指标（L2 Chamfer、Normal Consistency、LFD、Classification Score）均显著优于ConvOnet和DECOR-GAN等最强基线。"
- "用户研究显示，DMTET生成的形状在美观度（better looking）和细节质量（better details）上分别以95%和95%的优势大幅超过ConvONet。"
- "消融实验证实，体积细分（volume subdivision）和表面细分（surface subdivision）分别贡献了显著的性能提升，去除两者会导致Chamfer L1从0.77增加到0.81。"
- "Animal Shape Dataset (Coarse Voxel to High-Res Mesh) 上 L2 Chamfer Distance (↓) = 0.75"
---

# Deep Marching Tetrahedra: a Hybrid Representation for High-Resolution 3D Shape Synthesis

> [!tip] 核心洞察
> 通过可微行进四面体层连接隐式SDF和显式表面网格，构建了一个端到端的混合3D表示。该表示既能保留隐式场对任意拓扑的建模能力，又能利用显式表面损失直接监督几何细节，同时通过网格变形和选择性细分实现高效的高分辨率合成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 深度行进四面体：一种用于高分辨率3D形状合成的混合表示 |
| 英文题名 | Deep Marching Tetrahedra: a Hybrid Representation for High-Resolution 3D Shape Synthesis |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://arxiv.org/abs/2111.04276) · [Project](https://nv-tlabs.github.io/DMTet/) · [Project](https://research.nvidia.com/labs/toronto-ai/DMTet/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Deep Marching Tetrahedra (DMTET) |
| Dataset | Animal Shape Dataset (Coarse Voxel to High-Res Mesh) |

> [!tip] 效果简介
> - Animal Shape Dataset (Coarse Voxel to High-Res Mesh) 上，L2 Chamfer Distance (↓) 为 0.75，对比 0.83 (ConvOnet) / 1.32 (DECOR-Retv.)，变化 -0.08 / -0.57。
> - Animal Shape Dataset (Coarse Voxel to High-Res Mesh) 上，Normal Consistency (↑) 为 0.918，对比 0.901 (ConvOnet) / 0.876 (DECOR-Retv.)，变化 +0.017 / +0.042。
> - Animal Shape Dataset (Coarse Voxel to High-Res Mesh) 上，Light Field Distance (LFD) (↓) 为 2823，对比 3220 (ConvOnet) / 3689 (DECOR-Retv.)，变化 -397 / -866。

## 概要

**问题瓶颈**：现有基于神经隐式场（如占用场或有符号距离函数）的三维形状生成方法在训练时无法直接在显式表面上施加监督，导致重建结果丢失几何细节并产生伪影；而直接生成显式网格的方法则受限于预设拓扑，难以处理复杂变化的拓扑结构。

**核心洞见**：Deep Marching Tetrahedra (DMTET) 提出一种**混合三维表示**——在可变形四面体网格顶点上编码有符号距离函数（SDF），并通过一个**可微的行进四面体（Marching Tetrahedra）层**将其转换为显式三角网格。这一设计使损失函数可以直接定义在最终表面上，并通过反向传播联合优化几何与拓扑，同时保留了隐式场对任意拓扑的建模能力。

**方法定位**：DMTET 介于纯隐式方法（如 **ConvONet**, Peng et al., ECCV 2020）与纯显式网格变形方法（如 **Pixel2Mesh**, Wang et al., ECCV 2018）之间。它继承了 **DefTet**（Gao et al., NeurIPS 2020）的可变形四面体网格框架，但将占用场替换为顶点上的 SDF，并引入可微等值面提取和可学习的体积/表面细分机制，实现了端到端的高分辨率形状合成。

**主要结果**：
- 在粗糙体素超分辨任务（Animal Shape Dataset）上，DMTET 在所有指标（L2 Chamfer、Normal Consistency、LFD、Classification Score）上均显著优于 ConvONet 和 DECOR-GAN 等最强基线（Table 1）。
- 用户研究表明，DMTET 生成的形状在美观度和细节质量上分别以 95% 的优势大幅超过 ConvONet（Table 2）。
- 在点云重建任务（ShapeNet 风格）上，DMTET 的 Chamfer L1 达到 0.77，优于 ConvONet（0.95）、DefTet（0.97）、Mesh R-CNN（1.01）等，且推理速度约比 ConvONet 快 6.7 倍（Table 3）。
- 消融实验证实，体积细分和表面细分是精细几何重建的关键模块，去除两者会使 Chamfer L1 从 0.77 退化至 0.81（Table 3）。

### 3D 形状生成的核心瓶颈：隐式与显式表示的两难

近年来，基于神经网络的三维形状生成取得了长足进展，但其底层表示的选择始终制约着生成质量的上限。主流方法可大致分为两条技术路线，各自面临根本性困境。

**隐式表示路线**以**卷积占用网络**（ConvOnet, Peng et al., ECCV 2020）为代表，通过回归有符号距离函数（SDF）或占用场（Occupancy）来间接描述形状。这类方法天然支持任意拓扑变化，无需预设顶点连接关系。然而，其致命弱点在于训练过程中损失函数只能定义在隐式场上——网络从未直接“看见”最终提取的表面。这导致两个连锁后果：其一，缺乏对表面几何的直接监督，重建结果容易丢失精细细节并产生伪影；其二，最终表面需通过等值面提取算法（如 Marching Cubes）后处理获得，而该步骤不可微，切断了从显式表面到隐式场的梯度流动。

**显式表示路线**则直接生成三角网格或体素，表面损失可以精确计算。但这类方法要么受限于固定拓扑模板——如 **Pixel2Mesh**（Wang et al., ECCV 2018）依赖球面网格逐步变形，无法生成具有不同亏格（genus）的形状；要么陷入分辨率与计算代价的尖锐矛盾——如 **DECOR-GAN**（Chen et al., arXiv 2020）虽能生成高分辨率体素，但内存占用随分辨率立方增长，难以扩展至精细几何。

### 可微等值面提取的早期尝试与不足

为打破上述僵局，**Deep Marching Cubes**（DMC, Liao et al., CVPR 2018）率先提出可微的等值面提取方案：通过对网格单元内所有可能的 Marching Cubes 拓扑配置求期望，近似计算表面损失的反向传播。然而，这一策略存在两个根本缺陷：一是期望计算引入的近似误差随网格分辨率累积，导致梯度信号模糊；二是 Marching Cubes 本身存在拓扑歧义（ambiguous faces），在复杂几何区域易产生不连续表面。

另一条并行探索来自 **可变形四面体网格**（DefTet, Gao et al., NeurIPS 2020），它允许四面体顶点自由变形以贴合目标形状，但其核心设计是将占用值编码在四面体而非顶点上，且占用预测与顶点变形的监督相互独立。这意味着 DefTet 同样缺乏从最终表面到隐式编码的端到端梯度通路，表面细节的优化效率受限。

### DMTET 的破局思路：混合表示与端到端可微性

Deep Marching Tetrahedra（DMTET）的核心动机正是弥合上述鸿沟。其关键洞察在于：**如果能在隐式 SDF 与显式三角网格之间建立一个精确可微的桥梁，就可以同时享有隐式场的拓扑灵活性与显式表面的直接监督能力**。

具体而言，DMTET 提出三个相互咬合的设计要素：

1. **将 SDF 编码于可变形四面体网格的顶点上**，而非四面体内部。这一改动使得 SDF 的零等值面能够随顶点移动而连续演化，为拓扑变化提供机制基础。
2. **引入可微的行进四面体层**（Differentiable Marching Tetrahedra），根据顶点 SDF 符号和线性插值精确确定表面顶点位置，并将表面损失梯度无损回传至顶点 SDF 值和空间坐标。与 DMC 的期望近似不同，MT 层的梯度计算是精确的，且四面体网格天然避免了 Marching Cubes 的面歧义问题。
3. **通过网格变形与选择性细分实现高效的高分辨率合成**。网络仅对当前表面附近的四面体进行体积细分，将计算资源聚焦于几何细节丰富的区域，避免了全局高分辨率网格的算力浪费。

这一混合表示架构使得损失函数可以首次直接定义在显式曲面之上——Chamfer 距离、法向一致性、对抗损失等均作用于最终三角网格——而梯度却能穿透 MT 层，反向传播至隐式 SDF 和顶点变形参数，实现几何与拓扑的联合优化。论文的实验表明，这种端到端可微设计在粗糙体素超分辨任务上，较 ConvOnet 在 Chamfer L2 距离上提升约 9.6%（0.75 vs 0.83），推理速度更是快约 6.7 倍（129ms vs 866ms），验证了混合表示在质量与效率上的双重优势。

## 核心方法与创新机理

DMTET 的核心创新在于构建了一条从**隐式场到显式网格的端到端可微通路**，使损失函数能够直接定义在最终输出的三角网格上，从而在保留隐式表示对任意拓扑建模能力的同时，获得显式表面监督带来的几何细节保真度。这一设计通过三个紧密耦合的“changed slots”实现，从根本上区别于既有方法。

### 1. 从占用场到顶点 SDF 的底层表示转换

现有可变形四面体网格方法（如 **DefTet**，Gao et al., NeurIPS 2020）在每个四面体上编码占用值（occupancy），其监督信号与最终提取的表面之间存在语义鸿沟——占用场只指示空间是否被占据，而非表面到该点的精确距离。DMTET 将这一底层表示替换为**定义在四面体网格顶点上的有符号距离函数（SDF）**（`s(v_i)`）。这一转换并非简单的符号替换，而是改变了整个优化景观：SDF 的零等值面天然定义了表面位置，其梯度场直接编码法向信息，使得后续的可微等值面提取层能够通过线性插值精确地定位表面顶点，而非像占用场那样需要启发式阈值。

这一设计的因果机制在于：**SDF 的连续性和可微性使得网络预测的隐式场与最终表面之间建立了精确的解析对应关系**，梯度可以通过行进四面体层无近似地回传至每一个网格顶点的 SDF 值及其空间位置。

### 2. 可微行进四面体层：从隐式到显式的精确梯度桥梁

这是 DMTET 最关键的架构创新。在 DMTET 之前，将隐式场转换为显式网格的主流方案存在根本性缺陷：

- **非可微的 Marching Cubes**：作为后处理步骤，切断了训练时的梯度流，迫使方法只能在隐式空间中间接监督（如采样点上的 SDF 回归），无法直接优化表面几何。
- **可微近似方案**（如 **DMC**，Liao et al., CVPR 2018）：通过对一个网格单元内所有可能的等值面拓扑构型求期望来近似梯度，计算代价高且近似误差随网格分辨率累积。

DMTET 提出的**可微行进四面体（Marching Tetrahedra, MT）层**从根本上解决了这一问题。其可微性建立在两个数学性质之上：

1. **四面体等值面构型的确定性**：与立方体存在 256 种拓扑构型不同，四面体在考虑符号对称性后仅有 3 种独特的表面构型（Figure 3），使得等值面提取的计算路径简洁且确定。
2. **表面顶点的线性插值定位**：表面顶点位置通过边上两端点的 SDF 值线性插值获得，该操作对顶点位置和 SDF 值均为可微。

这使得**表面损失（Chamfer 距离、法向一致性）的梯度可以精确地传播至网格顶点的 SDF 值 `s(v_i)` 和空间坐标 `v_i`**，实现了对几何和拓扑的联合端到端优化。消融实验间接证实了这一设计的优势：与使用期望近似的 DMC 相比，DMTET 在相同设置下取得了显著更优的重建质量，论文明确指出这是因为“使用行进四面体层训练比计算一个网格单元内所有可能构型的期望更高效”。

### 3. 可学习的分辨率自适应机制：体积细分与表面细分

传统方法使用固定分辨率网格或需要预计算的八叉树结构，无法根据形状的局部复杂度动态分配计算资源。DMTET 引入了两级可学习细分机制：

**体积细分（Volume Subdivision）**：在每次细化迭代中，网络根据当前顶点的 SDF 符号自动识别表面四面体（即四个顶点 SDF 符号不完全相同的四面体），仅对这些表面四面体及其直接邻域进行细分——通过在每条边的中点插入新顶点，将一个四面体分裂为 8 个子四面体（Figure 2）。这一策略使得计算资源聚焦于表面区域，在保持高分辨率细节的同时控制总体计算开销。消融实验证实，移除体积细分后 Chamfer L1 从 0.77 退化到 0.79，用户研究中细节质量也出现可感知的下降。

**可学习表面细分（Learnable Surface Subdivision）**：在 MT 层提取表面网格后，DMTET 采用 Loop Subdivision 框架但将其参数（顶点位置和细分权重 `α_i`）交由 GCN 预测，而非使用固定参数。这使得细分过程能够根据局部几何特征自适应地调整，进一步消除量化误差并增强视觉质量。移除该模块导致 Chamfer L1 升至 0.78。

当同时移除网格变形能力和所有细分模块（仅在固定网格上预测 SDF）时，Chamfer L1 急剧退化至 0.91，验证了**可变形网格与自适应细分之间的协同效应是 DMTET 高效表征能力的基础**。

### 创新总结

DMTET 的三个 changed slots 形成了因果链条：顶点 SDF 表示提供了精确的隐式表面编码 → 可微 MT 层将隐式编码无损转换为显式网格并允许表面损失直接监督 → 可学习细分机制在训练过程中动态提升分辨率。这一设计使得 DMTET 在推理速度上比 ConvOnet 快约 6.7 倍（129ms vs 866ms），同时在所有几何指标上大幅领先，证明了混合表示在效率与质量之间的优越平衡。

DMTET 的整体 pipeline 遵循“隐式编码—可微等值面提取—显式表面监督”的端到端范式，其核心设计在于将可变形四面体网格上的有符号距离函数（SDF）作为中间表示，通过可微的行进四面体层桥接隐式场与显式网格，从而在保留拓扑灵活性的同时实现对表面几何的直接损失监督。

### 输入编码与初始 SDF 预测

pipeline 的输入端接受点云或粗糙体素表面采样点。对于粗糙体素输入，先在体素表面采样点以形成点云表示。随后，采用 **PVCNN**（Shi et al., NeurIPS 2019）作为编码器，从输入点云中提取三维特征体积 $F_{\text{vol}}(x)$。

在初始阶段，一个全连接网络（MLP）为可变形四面体网格的每个顶点 $v_i$ 预测其初始 SDF 值：

$$s(v_i) = \text{MLP}\big(F_{\text{vol}}(v_i, x),\; v_i\big)$$

其中 $F_{\text{vol}}(v_i, x)$ 是在顶点位置 $v_i$ 处通过三线性插值获得的体积特征。这一步骤将全局形状先验编码为定义在四面体网格顶点上的隐式场，为后续的几何细化与拓扑演化提供起点。

### 表面细化与体积细分

获得初始 SDF 后，pipeline 进入迭代的“表面细化—体积细分”循环。首先，根据顶点 SDF 符号识别表面四面体 $T_{\text{surf}}$（即四个顶点 SDF 符号不全相同的四面体），并提取表面顶点集合 $V_{\text{surf}}$。对每个表面顶点 $v_i$，将其坐标、当前 SDF 值 $s(v_i)$、体积特征 $F_{\text{vol}}(v_i, x)$ 以及上一阶段的特征 $f(v_i)$ 拼接为 GCN 输入特征：

$$f_{v_i}' = \text{concat}\big(v_i,\; s(v_i),\; F_{\text{vol}}(v_i, x),\; f(v_i)\big)$$

图卷积网络（GCN）在由表面顶点构成的图 $G$ 上运行，预测每个顶点的位置偏移量 $\Delta v_i$、SDF 残差 $\Delta s(v_i)$ 以及更新后的特征 $\overline{f(v_i)}$：

$$(\Delta v_i,\; \Delta s(v_i),\; \overline{f(v_i)})_{i=1,\ldots,N_{\text{surf}}} = \text{GCN}\big((f_{v_i}')_{i=1,\ldots,N_{\text{surf}}},\; G\big)$$

通过叠加位置偏移，网格顶点发生变形，使四面体网格自适应地贴合物体几何。随后，体积细分模块仅对表面四面体及其直接邻域进行细分——在每条边的中点插入新顶点，将每个表面四面体剖分为 8 个子四面体，从而在表面附近动态提升分辨率，同时避免全局均匀细分带来的计算与内存开销。

### 可微行进四面体层与表面提取

在任意细化阶段，均可通过可微行进四面体（Marching Tetrahedra, MT）层将隐式 SDF 转换为显式三角网格。MT 层根据四面体四个顶点的 SDF 符号确定等值面构型：由于四面体只有 3 种独特的表面构型（相比 Marching Cubes 的 15 种），拓扑歧义大幅减少。等值面顶点的位置沿符号变化的边进行线性插值，该插值过程对顶点位置和 SDF 值均可微，因此表面损失（如 Chamfer 距离、法向一致性损失）的梯度可以直接反向传播至四面体网格顶点的坐标与 SDF 值，实现端到端的联合优化。

### 可学习表面细分

从 MT 层提取的三角网格可进一步通过可学习表面细分增强视觉质量。DMTET 遵循 Loop Subdivision 的拓扑细分规则，但将固定的细分参数替换为由 GCN 预测的可学习参数：GCN 为每个顶点预测更新后的位置 $v_i'$ 以及用于控制细分曲面形状的权重 $\alpha_i$。这一设计使细分过程能够针对训练数据自适应地消除量化误差并增强细节表现力，而非依赖人工设定的固定参数。

### 判别器与损失监督

pipeline 的末端引入一个 3D 判别器，以提供对抗性监督。判别器以 **DECOR-GAN**（Chen et al., arXiv 2020）的 3D CNN 为基础，在随机选取的高曲率区域上比较真实网格与预测网格的 SDF 体积，而非直接作用于网格顶点。生成器的总损失由五项加权组成：

$$L = \lambda_{\text{cd}} L_{\text{cd}} + \lambda_{\text{normal}} L_{\text{normal}} + \lambda_{\text{G}} L_{\text{G}} + \lambda_{\text{SDF}} L_{\text{SDF}} + \lambda_{\text{def}} L_{\text{def}}$$

其中 $L_{\text{cd}}$ 和 $L_{\text{normal}}$ 分别为 L2 Chamfer 距离与法向一致性损失，直接定义在预测网格与真值网格的采样点集上；$L_{\text{G}}$ 为最小二乘 GAN（LSGAN）生成器损失；$L_{\text{SDF}}$ 约束四面体网格顶点的 SDF 值与真实符号距离一致；$L_{\text{def}}$ 对顶点变形量施加 L2 正则化。所有损失通过可微 MT 层反向传播，联合优化编码器、MLP、GCN 以及细分参数，形成一个完整的端到端训练框架。

### 数据流总结

整体数据流可概括为：**输入点云 → PVCNN 特征体积 → MLP 初始 SDF → GCN 迭代细化（含网格变形与体积细分） → 可微 MT 层提取显式网格 → 可学习表面细分 → 判别器评估与多损失反向传播**。该流程实现了从粗糙输入到高分辨率三角网格的由粗到精（coarse-to-fine）合成，且在推理时无需进行等值面查询或后处理优化，推理速度较基于隐式场的方法（如 ConvOnet）快约 6.7 倍。

### 3.1 可变形四面体网格与隐式SDF表示

DMTET将形状表示为一个定义在可变形四面体网格上的有符号距离函数（SDF）。给定四面体网格 $(V_T, T)$，其中 $V_T$ 为网格顶点集合，$T$ 为四面体集合，每个四面体 $T_k$ 由四个顶点 $\{v_{a_k}, v_{b_k}, v_{c_k}, v_{d_k}\}$ 构成。网格顶点可以自由变形，从而更高效地适配目标形状的几何结构。

每个顶点 $v_i$ 上编码一个SDF值 $s(v_i)$，四面体内部任意点的SDF值通过其四个顶点的重心插值获得。这一隐式表示使得DMTET能够处理任意拓扑的形状，同时通过顶点的可变形性将计算资源集中在表面区域。

### 3.2 体积细分与表面四面体识别

为在保持计算效率的同时提升分辨率，DMTET采用可学习的体积细分策略。首先通过检查四面体顶点SDF值的符号差异来识别表面四面体 $T_{surf}$：若一个四面体的顶点具有不同的SDF符号（即包含正负值），则该四面体与零等值面相交，被标记为表面四面体。随后，对 $T_{surf}$ 及其直接邻域四面体进行细分，通过在各边中点添加新顶点，将每个四面体分裂为8个子四面体（Figure 2）。这一过程仅聚焦于表面区域，避免了全局均匀细分带来的计算开销。

### 3.3 可微行进四面体层

可微行进四面体（Marching Tetrahedra, MT）层是DMTET连接隐式SDF与显式网格的核心模块。与Marching Cubes在立方体单元内提取等值面不同，MT在四面体单元内操作，具有更简洁的等值面构型：仅存在三种独特的表面配置（Figure 3），且符号翻转不改变表面拓扑。对于每条发生符号变化的边，表面顶点的位置通过线性插值确定：

$$p = \frac{s(v_a) v_b - s(v_b) v_a}{s(v_a) - s(v_b)}$$

其中 $v_a$ 和 $v_b$ 为边的两个端点，$s(v_a)$ 与 $s(v_b)$ 符号相反。由于插值过程完全可微，表面损失（如Chamfer距离、法向一致性损失）的梯度可以通过MT层反向传播至顶点位置和SDF值，实现端到端的联合优化。这一设计克服了传统Marching Cubes不可微的瓶颈，也避免了Deep Marching Cubes（DMC, Liao et al., CVPR 2018）中通过期望近似计算表面损失的效率问题。

### 3.4 可学习表面细分

在MT层提取显式网格后，DMTET进一步应用可学习的表面细分以消除量化误差并增强视觉质量。该方法遵循Loop Subdivision的细分方案，但将固定的细分参数替换为可学习参数。具体地，图卷积网络（GCN）为每个顶点预测更新后的位置 $v_i'$ 和Loop细分权重 $\alpha_i$，从而生成更光滑、细节更丰富的参数化曲面。

### 3.5 生成器管线公式

**初始SDF预测**：给定输入点云或粗糙体素表面采样点，PVCNN编码器提取3D特征体积 $F_{vol}(x)$。对于初始可变形四面体网格中的每个顶点 $v$，MLP预测其初始SDF值：

$$s(v) = \text{MLP}(F_{vol}(v, x), v)$$

**表面细化GCN**：在表面细化阶段，GCN的输入特征 $f_{v_i}'$ 由顶点坐标、当前SDF值、体积特征和上一阶段特征拼接而成：

$$f_{v_i}' = \text{concat}(v_i, s(v_i), F_{vol}(v_i, x), f(v_i))$$

GCN在表面顶点图 $G$ 上操作，输出每个表面顶点的位置偏移量 $\Delta v_i$、SDF残差 $\Delta s(v_i)$ 以及更新后的特征：

$$(\Delta v_i, \Delta s(v_i), \overline{f(v_i)})_{i=1,\cdots N_{surf}} = \text{GCN}((f_{v_i}')_{i=1,\cdots N_{surf}}, G)$$

这一迭代细化过程使网格顶点能够逐步变形以贴合目标表面，同时SDF残差允许拓扑的局部调整。

### 3.6 损失函数

DMTET的端到端训练损失由五个项加权组成：

$$L = \lambda_{\mathrm{cd}} L_{\mathrm{cd}} + \lambda_{\mathrm{normal}} L_{\mathrm{normal}} + \lambda_{\mathrm{G}} L_{\mathrm{G}} + \lambda_{\mathrm{SDF}} L_{\mathrm{SDF}} + \lambda_{\mathrm{def}} L_{\mathrm{def}}$$

**表面对齐损失**：在预测网格 $M_{pred}$ 和真实网格 $M_{gt}$ 上分别采样点集 $P_{pred}$ 和 $P_{gt}$，计算L2 Chamfer距离和法向一致性损失：

$$L_{\mathrm{cd}} = \sum_{p \in P_{pred}} \min_{q \in P_{gt}} ||p - q||_2 + \sum_{q \in P_{gt}} \min_{p \in P_{pred}} ||q - p||_2$$

$$L_{\mathrm{normal}} = \sum_{p \in P_{pred}} (1 - |\vec{\mathbf{n}}_p \cdot \vec{\mathbf{n}}_{\hat{q}}|)$$

其中 $\vec{\mathbf{n}}_p$ 为预测点 $p$ 的法向量，$\vec{\mathbf{n}}_{\hat{q}}$ 为 $p$ 在真实网格上最近点 $\hat{q}$ 的法向量。

**对抗损失**：采用最小二乘GAN（LSGAN）形式，判别器 $D$ 在随机选取的高曲率区域上评估SDF体积：

$$L_{\mathrm{D}} = \frac{1}{2} [(D(M_{gt}) - 1)^2 + D(M_{pred})^2]$$

$$L_{\mathrm{G}} = \frac{1}{2} [(D(M_{pred}) - 1)^2]$$

**正则化损失**：SDF正则化约束四面体网格顶点的SDF值与真实形状的符号距离一致，防止表面断裂：

$$L_{\mathrm{SDF}} = \sum_{v_i \in V_T} |s(v_i) - \text{SDF}(v_i, M_{gt})|^2$$

变形正则化对顶点偏移量施加L2惩罚，防止训练过程中产生异常变形：

$$L_{\mathrm{def}} = \sum_{v_i \in V_T} ||\Delta v_i||_2$$

## 实验与关键发现

### 核心定量结果：粗糙体素超分辨率

DMTET 在动物形状数据集（Animal Shape Dataset）的粗糙体素到高分辨率网格合成任务上，在所有指标上均显著超越最强基线。Table 1 给出了系统对比：

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2111_04276/figures/007_Table_1.jpg]]
*Table 1: Super Resolution of Animal Shapes: DMTET significantly outperforms all baselines in all metrics*

- **L2 Chamfer Distance (↓)**：DMTET 达到 0.75，相比 ConvOnet（Peng et al., ECCV 2020）的 0.83 降低 0.08，相比 DECOR-Retv.（Chen et al., arXiv 2020）的 1.32 降低 0.57。
- **Normal Consistency (↑)**：DMTET 达到 0.918，高于 ConvOnet 的 0.901 和 DECOR-Retv. 的 0.876。
- **Light Field Distance (LFD) (↓)**：DMTET 为 2823，ConvOnet 为 3220，DECOR-Retv. 为 3689，降幅分别达 397 和 866。
- **Classification Score (Cls) (↓)**：DMTET 为 0.54，优于 ConvOnet 的 0.63 和 DECOR-Retv. 的 0.66。

这些指标覆盖了表面距离、法向一致性、感知相似度和分类器可区分性，一致表明 DMTET 生成的形状在几何精度和视觉真实性上均具有显著优势。DMTET 的性能增益根源于其混合表示：可变形四面体网格上的隐式 SDF 保留了任意拓扑建模能力，而可微行进四面体层使损失函数能直接作用于显式表面，避免了隐式方法中因缺乏表面级监督而导致的细节丢失与伪影。

### 用户研究：感知质量验证

Table 2 报告了用户研究结果。在与 ConvOnet 的成对比较中，DMTET 生成的形状在 **美观度（better looking）** 上以 95% 的优势胜出，在 **细节质量（better details）** 上同样以 95% 的优势胜出。这一结果与定量指标相互印证，说明 DMTET 的优势不仅体现在数值指标上，也直接转化为人类可感知的视觉质量提升。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2111_04276/figures/008_Table_2.jpg]]
*Table 2: User Study on 3D Shape Synthesis from Coarse voxels. In each cell, we report percentages of shapes for which the users agree are better looking (left) or have better details (right)*

### 点云重建对比与推理效率

在 ShapeNet 风格的点云重建任务中（Table 3），DMTET 同样展现出全面的领先优势：

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2111_04276/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative results on 3D Reconstruction from Point Clouds: Our model reconstructs shapes with more geometric details compared to baselines. Table 3: Quantitative Results on Point Cloud Reconstruction (Chamfer L1). Note that all the networks in the baselines are not designed for this task, and thus we use the same encoder and their decoder for a fair comparison. We also ablate ourselves by operating on fixed grid (DMTET wo (Def, Vol., Surf.)), removing volume subdivision (DMTET wo Vol.), or surface subdivision (DMTET wo Surf.), or the both (DMTET wo (Vol., Surf.))*

- **Chamfer L1 (×10³) (↓)**：DMTET 为 0.77，ConvOnet 为 0.95，DefTet（Gao et al., NeurIPS 2020）为 0.97，Mesh R-CNN（Gkioxari et al., ICCV 2019）为 1.01，Pixel2Mesh（Wang et al., ECCV 2018）为 1.35，DMC（Liao et al., CVPR 2018）为 1.45，3D-R2N2（Choy et al., ECCV 2016）为 1.61。DMTET 相对于最强隐式基线 ConvOnet 降低 0.18，相对于可微等值面基线 DMC 降低 0.68。
- **推理时间**：DMTET 仅需 129 ms，而 ConvOnet 需要 866 ms，速度提升约 6.7 倍。这得益于 DMTET 通过体积细分将计算资源聚焦于表面区域，避免了全局密集采样的开销。

公平性说明：所有基线均使用相同的 PVCNN 编码器，仅替换各自的解码器，并在相同设置下重新训练，排除了编码器差异对结果的干扰。

### 消融实验：各模块贡献

Table 3 的消融实验系统解耦了 DMTET 各组件的贡献（以 Chamfer L1 为指标）：

| 配置 | Chamfer L1 (×10³) ↓ |
|------|---------------------|
| DMTET（完整） | 0.77 |
| DMTET 去除体积细分（wo Vol.） | 0.79 |
| DMTET 去除表面细分（wo Surf.） | 0.78 |
| DMTET 去除体积细分和表面细分（wo Vol., Surf.） | 0.81 |
| DMTET 去除变形、体积细分和表面细分（wo Def., Vol., Surf.） | 0.91 |

**关键发现**：
1. **体积细分与表面细分的协同作用**：单独去除体积细分或表面细分分别导致指标退化为 0.79 和 0.78，同时去除两者则进一步退化为 0.81。用户研究也佐证了这一点——DMTET 完整版本在细节质量上以 78%/61% 的优势胜出去除体积细分的变体。这表明体积细分通过增加表面区域的分辨率来捕获更精细的几何结构，而可学习表面细分则进一步消除量化误差、增强视觉平滑度。
2. **可变形网格的核心地位**：去除网格变形和所有细分模块后（仅在固定网格上预测 SDF），Chamfer L1 急剧上升至 0.91。这验证了可变形网格是高效表征的关键——它使网格顶点能主动适配物体几何，在有限计算预算下实现更高的有效分辨率。
3. **与 DMC 的对比**：DMC 使用 Marching Cubes 的可微近似（基于期望计算表面损失），其 Chamfer L1 为 1.45，远高于 DMTET 的 0.77。DMTET 的优势在于行进四面体层的精确可微性——它直接在确定的等值面构型上计算梯度，而非像 DMC 那样对网格单元内所有可能构型取期望，从而实现了更高效、更准确的训练信号传播。

### 与 Oracle 的对比分析

Figure 8 和 Figure 9 对比了 DMTET 与 Marching Cubes (MC) 和 Marching Tetrahedra (MT) 的 Oracle 性能。Oracle 实验指在已知真实 SDF 的情况下，直接用 MC 或 MT 提取等值面，以此衡量等值面提取算法本身的信息损失上限。结果表明：即使在 Oracle 设置下，MT 也优于 MC；而经过训练的 DMTET 能够逼近甚至在某些细节结构上超越 Oracle MT 的表现，说明网络学习到的 SDF 和网格变形有效补偿了离散采样带来的信息损失。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2111_04276/figures/011_Figure_8.jpg]]
*Figure 8: Comparing our DMTET with oracle performance of MC and MT*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2111_04276/figures/012_Figure_9.jpg]]
*Figure 9: We compare trained DMTET to oracle performance of MT and MC. Number in bracket indicates number of SDF points queried*

### 失败模式与局限性

尽管 DMTET 在多个任务上表现优异，论文也指出了若干局限：

1. **全局形状一致性的判别困难**：当前判别器在随机选取的高曲率局部区域上评估 SDF 体积，可能难以捕捉全局形状的结构一致性。这可能导致生成形状在局部细节逼真的同时，整体比例或拓扑出现不协调。论文建议未来探索更有效的全局判别器。
2. **数据域泛化未验证**：所有实验均基于动物形状数据集，其在更多样化、更复杂的真实世界物体（如机械零件、建筑结构）上的泛化能力尚未得到验证。
3. **高分辨率实时交互的瓶颈**：尽管推理速度大幅领先隐式方法（129 ms vs 866 ms），但在需要实时交互的应用场景中，四面体网格的管理开销仍可能构成瓶颈，尤其是在多次迭代细化的高分辨率设置下。

### 开放问题

1. 可微行进四面体层在训练中实现拓扑变化的确切机制——其梯度流动与 Marching Cubes 方案的理论差异——尚需严格的形式化分析。
2. 该混合表示能否扩展到大规模场景（如室内场景、城市场景）或需要处理开放表面的任务（如单视图重建），仍有待探索。
3. 对于极细薄结构（如飞机机翼、灯杆），当前表面细分策略的保真度是否可通过更高效的自适应四面体剖分进一步提升？
4. 基于局部 SDF 体积的对抗损失是否能被更有效的全局纹理或结构判别器所取代，以进一步提升生成质量？

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2111_04276/figures/003_Figure_3.jpg]]
*Figure 3: Three unique surface configurations in MT. Vertex color indicates the sign of signed distance value. Notice that flipping the signs of all vertices will result in the same surface configuration. Position of the vertex is linearly interpolated along the edges with sign change*

## 定位与知识库关联

### 1. 方法演进脉络

DMTET 的核心贡献在于通过**可微行进四面体层**将隐式场与显式网格连接为端到端可训练的混合表示。这一设计并非凭空产生，而是沿着两条此前相互隔离的技术路线交汇而成：隐式神经表示与可微等值面提取。

**隐式神经表示的前置工作。** 以占用场（Occupancy Networks, Mescheder et al., CVPR 2019）和符号距离函数（DeepSDF, Park et al., CVPR 2019）为代表的隐式方法能够建模任意拓扑，但其训练时无法直接在表面上定义损失，导致重建细节模糊。**ConvOnet**（Peng et al., ECCV 2020）通过卷积编码器增强隐式场的局部特征表达能力，但仍受限于间接监督的瓶颈。**DefTet**（Gao et al., NeurIPS 2020）首次将可变形四面体网格与占用场结合，使网格顶点可以主动适配几何，但占用场定义在四面体上、SDF 定义在顶点上的差异使其无法直接利用等值面提取来获得显式网格进行端到端监督。

**可微等值面提取的探索。** **DMC**（Liao et al., CVPR 2018）率先提出可微 Marching Cubes，通过对网格单元内所有可能拓扑构型求期望来近似梯度，但该近似方案计算效率低且梯度不精确。DMTET 将 Marching Cubes 替换为 Marching Tetrahedra，利用四面体网格仅存在三种独特表面构型（Figure 3）的特性，使等值面提取**精确可微**且计算更高效——这是 DMTET 相较于 DMC 取得显著更优重建质量的根本原因。

**显式网格变形方法。** **Pixel2Mesh**（Wang et al., ECCV 2018）和 **Mesh R-CNN**（Gkioxari et al., ICCV 2019）分别代表固定拓扑变形和拓扑可变的两类网格方法。前者从初始椭球变形，无法处理拓扑变化；后者分阶段预测占用和顶点位置，缺乏隐式-显式联合优化。DMTET 通过可变形四面体网格上的 SDF 隐式定义表面，既保留了拓扑自由度，又通过 MT 层实现了显式表面的直接监督。

**体素与生成对抗方法。** **3D-R2N2**（Choy et al., ECCV 2016）是早期体素重建代表，受限于低分辨率。**DECOR-GAN**（Chen et al., arXiv 2020）使用 3D 补丁判别器在体素空间进行对抗训练以提升高分辨率合成质量。DMTET 继承了 DECOR-GAN 的 3D CNN 判别器设计，但将其应用于从预测网格计算得到的 SDF 体积上，并在高曲率区域进行局部对抗训练。

### 2. 关键设计选择与对比

| 设计维度 | 基线方案 | DMTET 方案 | 因果效应 |
|----------|----------|------------|----------|
| 隐式场类型 | 占用场（DefTet, ConvOnet） | 定义在四面体网格顶点上的 SDF | 顶点 SDF 可通过线性插值直接确定等值面位置，为可微 MT 层提供精确梯度路径 |
| 等值面提取 | 非可微 MC 或期望近似（DMC） | 精确可微 Marching Tetrahedra | 三种构型使梯度计算封闭且高效，避免 DMC 的期望近似误差 |
| 分辨率自适应 | 固定网格或预计算八叉树 | 可学习体积细分：仅对表面四面体及其邻域细分 | 计算资源聚焦于表面区域，实现高分辨率而不过度增加开销 |
| 表面后处理 | 无或固定参数细分 | 可学习 Loop Subdivision | 进一步消除量化伪影，增强视觉平滑度 |
| 监督方式 | 间接监督（隐式方法）或分阶段监督（Mesh R-CNN） | 端到端直接表面损失 + 对抗损失 + SDF 正则化 | 表面损失直接优化几何精度，对抗损失提升局部真实性，SDF 正则化防止断裂 |

### 3. 适用边界与局限

**已验证的适用场景：**
- 粗糙体素到高分辨率网格的超分辨率合成（Animal Shape Dataset）
- 点云到网格的三维重建（ShapeNet 风格数据）
- 推理速度显著优于隐式方法（约 6.7× 快于 ConvOnet，Table 3）

**已知局限：**
1. **判别器范围受限。** 当前 3D 判别器仅在局部高曲率区域评估 SDF 体积，可能难以捕捉全局形状一致性和长距离结构依赖。论文明确指出需要探索更有效的全局判别器。
2. **数据集泛化性未验证。** 所有实验基于动物形状数据集，其在更多样化、更复杂的真实世界物体（如机械零件、建筑结构）上的表现尚未评估。
3. **高分辨率实时应用受限。** 尽管推理速度大幅领先纯隐式方法，四面体网格管理（变形、细分、MT 提取）仍存在计算开销，可能制约实时交互场景。
4. **极细薄结构保真度。** 当前细分策略对极细薄结构（如飞机机翼、灯杆）的保真度可能不足，需要更高效的表面细分或自适应剖分方法。

### 4. 开放问题与后续方向

1. **可微 MT 层的拓扑变化机制。** 训练过程中，顶点 SDF 符号翻转如何精确驱动拓扑变化，其梯度流动与 DMC 方案的理论差异尚未被严格分析。理解这一机制有助于设计更稳定的训练策略。

2. **混合表示的场景级扩展。** 当前 DMTET 处理的是单个物体，能否将可变形四面体网格与可微 MT 层扩展到大规模场景（室内场景、城市场景）或需要处理开放表面的任务（如单视图重建），是一个开放挑战。

3. **全局判别器设计。** 现有基于局部 SDF 体积的对抗损失难以保证全局形状合理性。是否存在更有效的全局纹理判别器或结构判别器来引导生成，值得进一步研究。

4. **与新兴表示的融合。** 3D Gaussian Splatting 等新兴显式表示在渲染质量上表现出色，DMTET 的混合表示思想能否与之结合，在保持高分辨率几何的同时获得更优的渲染效果，是潜在的研究方向。

5. **训练稳定性与损失平衡。** 总损失包含五个加权项（Chamfer、法向一致性、GAN、SDF 正则化、变形正则化），各系数对训练稳定性和最终质量的影响机制尚需系统消融研究。

## 原文 PDF

![[paperPDFs/NEURIPS_2021/Deep_Marching_Tetrahedra_a_Hybrid_Representation_for_High_Resolution_3D_Shape_Synthesis.pdf]]

---
title: "MeshFlow: Efficient Artistic Mesh Generation via MeshVAE and Flow-based Diffusion Transformer"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MeshFlow_Efficient_Artistic_Mesh_Generation_via_MeshVAE_and_Flow_based_Diffusion_Transformer.pdf
project_link: null
code_link: null
aliases:
- MeshFlow
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 提出MeshVAE将网格顶点、法线和拓扑连接压缩为紧凑的连续潜空间，避免任何离散化和量化，再结合整流流扩散变换器（Rectified Flow DiT）实现所有顶点和边的并行生成，从根本上消除自回归的序列依赖。
primary_logic: 为每个顶点学习连续边嵌入，通过嵌入向量距离与阈值的比较隐式定义边的存在，将离散拓扑转换为可微的连续表示；利用预测的顶点法线自动确定面片朝向，无需显式编码半边结构即可恢复有向三角网格；采用TokenMerge/TokenSplit策略进行高效下采样与上采样，以极少潜码（n_v/4）实现高质量重建。
claims:
- MeshVAE将网格压缩至n_v/4个潜向量仍能高精度重建，压缩比达0.014（比朴素令牌化少72倍，比最紧凑的令牌化少16倍）
- 利用连续边嵌入和对比学习表示离散拓扑，避免了量化离散化
- 生成速度比最快的自回归方法快18倍
- 在Toys4K数据集上达到最低的Chamfer Distance和Hausdorff Distance，推理时间仅约1.2秒
---

# MeshFlow: Efficient Artistic Mesh Generation via MeshVAE and Flow-based Diffusion Transformer

> [!tip] 核心洞察
> 为每个顶点学习连续边嵌入，通过嵌入向量距离与阈值的比较隐式定义边的存在，将离散拓扑转换为可微的连续表示；利用预测的顶点法线自动确定面片朝向，无需显式编码半边结构即可恢复有向三角网格；采用TokenMerge/TokenSplit策略进行高效下采样与上采样，以极少潜码（n_v/4）实现高质量重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | MeshFlow：基于MeshVAE和整流流扩散变换器的高效艺术网格生成 |
| 英文题名 | MeshFlow: Efficient Artistic Mesh Generation via MeshVAE and Flow-based Diffusion Transformer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_MeshFlow_Efficient_Artistic_Mesh_Generation_via_MeshVAE_and_Flow-based_Diffusion_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MeshFlow |
| Dataset | Toys4K 点云条件网格生成 |

> [!tip] 效果简介
> - 网格压缩重建 (Table 1) 上，CD (×100) ↓ 1.29 vs 1.63 (TreeMeshGPT) (-0.34 (优于TreeMeshGPT))；压缩比 ↓ 0.014 vs 0.22 (TreeMeshGPT) (15.7× 更小)。
> - Toys4K 点云条件网格生成 (Table 2) 上，CD (×100) ↓ 2.45 vs 未提供具体基线值 (所有方法中最低)；HD (×100) ↓ 6.40 vs 未提供具体基线值 (所有方法中最低)。
> - 推理速度 (Toys4K) 上，加速比 1× (MeshFlow) vs 1× (最快自回归方法) (18× 更快)。

## 概要

3D网格是影视、游戏与工业设计中的核心资产，但高质量艺术网格的自动生成仍面临根本性效率瓶颈。现有自回归网格生成方法（如**MeshGPT** (Siddiqui et al., arXiv 2023)、**MeshXL** (Chen et al., arXiv 2024)、**EdgeRunner** (Tang et al., arXiv 2024)）存在三重结构性缺陷：**推理计算复杂度与网格面数呈二次方关系**，难以生成大规模精细网格；**顶点坐标被离散化为仅128级**，引入量化误差导致顶点坍塌和面片重叠；**序列生成可能提前终止**，产生不完整几何体。

**MeshFlow**（CVPR 2026）提出了一种根本性的范式转换：将网格生成从自回归离散序列预测转变为连续潜空间的并行生成。其核心由两大组件构成：

- **MeshVAE**：一种新型网格自编码器，将顶点位置、法线和拓扑连接统一压缩为紧凑的连续潜空间表示。关键创新在于为每个顶点学习**连续边嵌入**，通过嵌入向量距离与阈值的比较隐式定义边的存在（$A_{ij} = \mathbb{I}[d(\mathbf{h}_i, \mathbf{h}_j) \leq \tau]$），将离散拓扑转换为可微的连续表示，彻底消除了量化误差。配合TokenMerge/TokenSplit下采样策略，仅需 $n_v/4$ 个潜向量（压缩比0.014）即可实现高精度重建——比朴素令牌化少72倍，比最紧凑的令牌化少16倍。

- **整流流扩散变换器**：在MeshVAE的连续潜空间上，以点云编码和顶点数量为条件，通过Rectified Flow并行生成所有顶点和边的潜码，从根本上消除了自回归的序列依赖。

在Toys4K数据集上的实验表明，MeshFlow在Chamfer Distance和Hausdorff Distance两项指标上均达到最优，同时**推理速度比最快的自回归方法快18倍**（约1.2秒/物体），且推理时间仅随网格大小线性增长。定性结果进一步显示，自回归方法常因提前终止产生不完整几何，而MeshFlow能高效生成几何完整的高质量网格。



### 3D网格生成的核心挑战

3D网格是计算机图形学与视觉计算中的基本形状表示，广泛应用于游戏、影视、工业设计和具身智能等领域。生成高质量、拓扑合理的三角网格面临双重挑战：既要精确建模顶点在连续空间中的几何位置，又要正确恢复离散的边与面连接关系。这一离散-连续混合特性使网格生成天然比图像或点云生成更为困难。

### 自回归范式的三大瓶颈

近年来，以PolyGen（Nash et al., ICML 2020）、MeshGPT（Siddiqui et al., arXiv 2023）、MeshXL（Chen et al., arXiv 2024）为代表的自回归（Autoregressive, AR）方法主导了网格生成的研究。这些方法将网格序列化为令牌流，逐令牌预测顶点坐标和面索引。然而，该范式存在三个根本性瓶颈：

**瓶颈一：推理计算复杂度与网格规模呈二次方关系。** 自回归生成中，每个新令牌的预测需要关注所有已生成令牌，导致推理时间随面数呈二次方增长。对于包含数千个面的中等规模网格，单物体推理时间常超过20秒，严重制约了实际应用。

**瓶颈二：顶点坐标离散化引入量化误差。** 为适配离散令牌预测框架，现有方法将顶点坐标量化为有限级别（通常仅128级）。如图2所示，低量化分辨率导致顶点位置偏差，进而引发顶点坍塌和面片重叠等严重几何缺陷。这种离散化本质上将连续几何问题退化为了分类问题，牺牲了网格的精细几何保真度。

**瓶颈三：序列生成可能提前终止。** 自回归模型依赖隐式学习序列终止条件，实践中常出现生成提前停止（early stopping）现象，产生缺失大量面片的不完整几何（如图7定性对比所示）。这一问题在分布外形状上尤为突出，因为模型难以准确判断序列长度。

### 现有非自回归尝试的局限

针对上述瓶颈，已有工作开始探索非自回归生成路径。MeshCraft（He et al., arXiv 2025）采用图卷积自编码器加扩散变换器的方案，但图卷积对拓扑结构的建模能力有限。SpaceMesh（Shen et al., SIGGRAPH Asia 2024）使用连续半边表示，但表示效率较低。PDT（Wang et al., ACM SIGGRAPH 2025）仅生成顶点位置，面片拓扑需额外后处理。这些方法或保留了部分离散化操作，或在拓扑质量上仍有明显不足，未能同时解决速度、精度和拓扑完整性的三重挑战。

### 本文动机与核心思路

本文的核心洞察是：**离散拓扑与连续几何的分离建模是上述瓶颈的根源。** 自回归方法被迫将连续顶点坐标离散化以适配序列预测，而面片索引的逐令牌生成又引入了序列依赖。我们提出MeshFlow，通过两个关键技术突破从根本上重塑网格生成流程：

1. **连续统一的网格表示**：设计MeshVAE，为每个顶点学习连续边嵌入，通过嵌入向量距离与阈值的比较隐式定义边的存在（$A_{ij} = \mathbb{I}[d(\mathbf{h}_i, \mathbf{h}_j) \leq \tau]$），将离散拓扑转换为可微的连续表示。顶点坐标保持连续值，完全避免量化操作。同时利用预测的顶点法线自动确定面片朝向，无需显式编码半边结构即可恢复有向三角网格。

2. **并行潜空间生成**：采用整流流扩散变换器（Rectified Flow DiT）在MeshVAE的紧凑连续潜空间中并行生成所有顶点和边的潜码，从根本上消除自回归的序列依赖。推理时间仅随网格大小线性增长，而非二次方增长。

这一设计使MeshFlow在生成速度上比最快的自回归方法快18倍，同时以仅$n_v/4$个潜向量（压缩比0.014，比最紧凑的令牌化方案少16倍）实现高精度重建，在Toys4K数据集上取得了最低的Chamfer Distance和Hausdorff Distance。



## 核心方法与创新机理

MeshFlow 的核心创新在于**从根本上重构了网格的表示、压缩与生成范式**，以连续潜空间中的并行生成替代了现有自回归方法的离散序列建模。这一转变通过三个紧密耦合的技术支柱实现，分别对应网格表示、压缩编码和生成策略三个维度的 changed slots。

### 从离散令牌到连续边嵌入的拓扑表示

现有自回归网格生成方法（如 **PolyGen** (Nash et al., ICML 2020)、**MeshGPT** (Siddiqui et al., arXiv 2023)、**MeshXL** (Chen et al., arXiv 2024) 等）普遍采用基于面索引的离散令牌化——每个三角面至少需要9个令牌来编码三个顶点索引，且顶点坐标被量化为有限的离散级别（通常仅128级）。这种离散化带来两个根本性缺陷：其一，量化误差导致顶点位置偏移，引发顶点坍塌和面片重叠（Figure 2 右侧直观展示了低量化分辨率下的几何退化）；其二，面片令牌数量与网格复杂度呈线性关系，使得序列长度随面数增长，加剧自回归的推理负担。

MeshFlow 提出了一种**连续边嵌入机制**来隐式定义拓扑连接。具体而言，为每个顶点 $i$ 学习一个边嵌入向量 $\boldsymbol{h}_i$，两个顶点之间存在边的条件由嵌入距离与阈值 $\tau$ 的比较决定：

$$\mathcal{A}_{ij} = \mathbb{I}[d(\boldsymbol{h}_i, \boldsymbol{h}_j) \leq \tau]$$

这一设计的核心洞察在于：**将离散的拓扑关系转化为可微的连续表示**，使得边的存在性可以通过嵌入空间的几何关系自然涌现，无需显式编码半边结构或面片索引。训练时采用对比学习策略——正样本对（存在边的顶点）的嵌入被拉近至距离小于 $\tau$，负样本对（不存在边的顶点）的嵌入被推远至距离大于 $\tau$，对应的正负对比损失分别为：

$$\mathcal{L}_{\mathrm{pos}} = -\frac{1}{|E|}\sum_{(i,j)\in E}\log\left(\sigma(d(\hat{\mathbf{e}}_i, \hat{\mathbf{e}}_j) - \tau)\right)$$

$$\mathcal{L}_{\mathrm{neg}} = -\frac{1}{|\neg E|}\sum_{(i,j)\notin E}\log\left(\sigma(\tau - d(\hat{\mathbf{e}}_i, \hat{\mathbf{e}}_j))\right)$$

在网格恢复阶段，从边嵌入判定有效边集后，通过寻找共享三个不同顶点的边三元组即可恢复三角面：

$$F = \{\{f_1, f_2, f_3\} : \{f_1, f_2\}, \{f_2, f_3\}, \{f_3, f_1\} \in E\}$$

同时，预测的顶点法线自动确定面片朝向，避免了显式半边结构的需求。这一连续表示从根本上消除了顶点坐标的量化误差，使得网格生成可以在完全连续的几何空间中运作。

### 极致压缩的 MeshVAE：TokenMerge/TokenSplit 与 n_v/4 潜空间

网格压缩的核心挑战在于如何在保留拓扑和几何精度的前提下，将变长、离散的网格数据映射到紧凑的固定维度潜空间。MeshVAE 的设计围绕三个关键决策展开：

**输入特征构造**：编码器以每个顶点的位置 $\boldsymbol{v}_i$、法线 $\boldsymbol{n}_i$ 及其邻居顶点集合 $\mathcal{N}_i$ 作为输入，通过 Fourier 位置编码将几何信息嵌入高维空间：

$$\boldsymbol{x}_i = \mathrm{Concat}(\mathrm{PE}(\boldsymbol{v}_i), \mathrm{PE}(\boldsymbol{n}_i), \mathrm{Concat}_{j\in\mathcal{N}_i}(\boldsymbol{v}_j))$$

这一设计使得每个顶点的输入特征同时编码了自身的几何属性（位置、朝向）和局部拓扑上下文（邻居顶点坐标），为后续的压缩提供了丰富的信息基础。

**TokenMerge 下采样策略**：与常见的 Q-former 交叉注意力压缩或最远点采样（FPS）不同，MeshVAE 采用了一种类似像素洗牌（pixel-shuffle）的 TokenMerge 操作进行下采样。消融实验（Table 3）表明，TokenMerge 在重建质量上显著优于 Q-former 和 FPS，F1 分数达到 99.78。其优势在于：TokenMerge 通过空间局部性保持了几何信息的连续性，避免了 Q-former 的全局压缩导致的信息弥散，也避免了 FPS 的随机采样带来的信息丢失。

**极致压缩比**：MeshVAE 仅需 $n_v/4$ 个潜向量即可实现高精度重建，压缩比达到 0.014。这意味着相比朴素令牌化（每面9个令牌，约 $9n_f \approx 18n_v$ 个令牌），MeshVAE 的令牌数量减少了 **72倍**；相比最紧凑的现有令牌化方案（如 TreeMeshGPT 的 0.22 压缩比），仍减少了 **16倍**。在定量对比中（Table 1），MeshVAE 取得 Chamfer Distance 1.29（×100），优于 TreeMeshGPT 的 1.63，同时压缩比仅为后者的 1/15.7。

解码器通过对称的 TokenSplit 上采样操作，从潜码逐步恢复顶点位置、法线、边嵌入和有效顶点掩码，实现从紧凑潜空间到完整网格的忠实重建（Figure 6 展示了 MeshVAE 对拓扑和几何细节的保留能力）。

### 整流流扩散变换器：并行生成与线性时间推理

传统自回归方法的核心瓶颈在于**序列依赖**——每个令牌的生成依赖于前序令牌，导致推理时间与序列长度呈二次方关系，且可能因提前终止而产生不完整几何。MeshFlow 采用**整流流扩散变换器（Rectified Flow DiT）** 实现所有顶点和边的并行生成，从根本上打破这一瓶颈。

**生成范式转变**：以预训练点云编码器提取的特征令牌和顶点数量为条件，整流流模型在 MeshVAE 的连续潜空间中学习从噪声到目标潜码的向量场。训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t,\mathbf{x}_0,\epsilon} \Vert \pmb{v}_{\theta}(\pmb{x}, t) - (\epsilon - \pmb{x}_0) \Vert_2^2$$

该损失训练向量场网络 $\pmb{v}_{\theta}$ 逼近从噪声 $\epsilon$ 到真实潜码 $\mathbf{x}_0$ 的变换方向。推理时，通过常微分方程（ODE）求解器沿学习到的向量场积分，从随机噪声并行生成全部潜码，再经 MeshVAE 解码器恢复完整网格。

**推理效率的质变**：由于所有顶点和边同时生成，推理时间仅随网格大小**线性增长**，而非自回归方法的二次方增长。在 Toys4K 数据集上，MeshFlow 的推理时间约 1.2 秒，比最快的自回归方法快 **18倍**。更为关键的是，论文特别指出了推理时间计算的公平性问题：自回归方法通常按批次平均报告推理时间，但处理单个对象实际需要报告值的约 6 倍时间（因批次填充和并行化开销被均摊），而 MeshFlow 的推理时间保持恒定，不受批次大小影响。这一特性使得 MeshFlow 在实际部署中具有显著的响应时间优势。

**质量与速度的兼得**：在 Toys4K 点云条件网格生成任务中（Table 2），MeshFlow 取得了最低的 Chamfer Distance（2.45，×100）和 Hausdorff Distance（6.40，×100），同时保持最快的推理速度。定性对比（Figure 7）显示，自回归方法常因提前终止而产生不完整几何，而 MeshFlow 的并行生成机制天然避免了这一问题，能够稳定输出完整、高质量的三角网格。



MeshFlow 的整体管线由三个核心模块串联构成：**MeshVAE 编码器**将离散网格压缩为紧凑的连续潜表示，**整流流扩散变换器**（Rectified Flow DiT）在该潜空间中并行生成全部潜码，**MeshVAE 解码器**与后处理步骤从生成的潜码中恢复完整的三角网格。图 Figure 3 展示了这一端到端流程：输入网格经 MeshVAE 编码为潜向量 $z$，生成器以点云特征和顶点数量为条件采样潜码 $\hat{z}$，最终解码还原为网格。

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our method. We first propose MeshVAE, which compresses vertices, vertex normals, and discrete adjacency relationships of a mesh into a continuous latent space. This is supervised by the ground-truth vertices and vertex normals, coupled with a contrastive learning approach applied to vertex adjacency. We then employ latent Rectified Flow based on the proposed representation, and finally pass the result through the Mesh Decoder to obtain a mesh*

### 输入表示

MeshFlow 将网格形式化为每个顶点的三元组 $(\boldsymbol{v}_i, \boldsymbol{n}_i, \boldsymbol{h}_i)$，分别表示顶点的三维坐标、顶点法线以及**连续边嵌入**（edge embedding）。这种表示的核心创新在于：不再显式存储面索引，而是通过边嵌入向量之间的距离与阈值 $\tau$ 的比较来隐式定义边的存在：

$$\mathcal{A}_{ij} = \mathbb{I}\left[d(\boldsymbol{h}_i, \boldsymbol{h}_j) \leq \tau\right]$$

若顶点 $i$ 和 $j$ 的边嵌入距离小于阈值 $\tau$，则判定二者之间存在一条边。这一设计将离散的拓扑连接转化为可微的连续表示，彻底规避了自回归方法中顶点坐标离散化（通常仅 128 级）带来的量化误差和面片坍塌问题。

### MeshVAE：压缩与重建

**编码器** $\mathcal{E}$ 接收顶点坐标 $\boldsymbol{v}$、法线 $\boldsymbol{n}$ 以及从邻接矩阵提取的邻居顶点信息。每个顶点的输入特征由三部分拼接而成：

$$\boldsymbol{x}_i = \mathrm{Concat}\left(\mathrm{PE}(\boldsymbol{v}_i), \mathrm{PE}(\boldsymbol{n}_i), \mathrm{Concat}_{j \in \mathcal{N}_i}(\boldsymbol{v}_j)\right)$$

其中 $\mathrm{PE}(\cdot)$ 为 Fourier 位置编码。编码器随后通过 **TokenMerge** 策略对顶点特征进行下采样——将相邻顶点的特征合并为更少的潜令牌，再经过交叉注意力（以合并后的令牌为 query，原始特征为 key/value）和多层自注意力，最终输出紧凑的潜码 $z$。解码器则通过对称的 **TokenSplit** 上采样、自注意力和交叉注意力，从潜码中重建顶点坐标、法线、边嵌入以及有效顶点掩码。

这一压缩方案极为高效：仅需保留 $n_v/4$ 个潜向量即可实现高精度重建，压缩比低至 0.014，比朴素令牌化方案少 72 倍，比最紧凑的令牌化方案少 16 倍。

### 整流流扩散变换器：并行生成

生成阶段采用 **Rectified Flow** 框架训练一个 DiT（Diffusion Transformer），以预训练点云编码器提取的特征令牌和顶点数量为条件，直接在 MeshVAE 的连续潜空间中并行生成所有潜码。训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \left\Vert \boldsymbol{v}_{\theta}(\boldsymbol{x}, t) - (\epsilon - \boldsymbol{x}_0) \right\Vert_2^2$$

该损失训练向量场网络 $\boldsymbol{v}_\theta$ 逼近从噪声 $\epsilon$ 到真实数据 $\boldsymbol{x}_0$ 的变换方向。由于所有潜码同时生成，推理时间仅随网格大小**线性增长**，彻底消除了自回归方法的序列依赖和二次方计算复杂度。在 Toys4K 数据集上，MeshFlow 的推理时间仅约 1.2 秒，比最快的自回归方法快 18 倍。

### 网格恢复与后处理

解码器输出的连续表示需要通过确定性的恢复流程转化为三角网格。首先根据边嵌入距离阈值提取有效边集 $E$，然后查找共享三个不同顶点的边三元组以形成三角面：

$$F = \left\{ \{f_1, f_2, f_3\} : \{f_1, f_2\}, \{f_2, f_3\}, \{f_3, f_1\} \in E \right\}$$

由于生成结果可能残留少量边界孔洞，MeshFlow 实现了一个启发式后处理步骤：检测仅属于一个三角面的边界边，将其组织为 $k$-gon 环，并对 $k < 5$ 的环进行三角化修补。



MeshFlow 的生成管线由两大核心模块构成：MeshVAE 将离散网格压缩为紧凑的连续潜表示，整流流扩散变换器在该潜空间中进行高效并行生成。以下逐一剖析各模块的设计动机、关键公式与变量含义。

### 3.1 连续网格表示与拓扑可微化

传统自回归方法将网格离散化为面索引序列，每个面至少需要 9 个令牌，且顶点坐标被量化至 128 级，引入不可忽略的量化误差。MeshFlow 的根本创新在于将网格重新表示为一组连续向量，彻底消除离散化。

一个网格被表示为三元组 $\mathcal{M} = (\mathbf{v}, \mathbf{n}, \mathbf{h})$，其中 $\mathbf{v}_i \in \mathbb{R}^3$ 为顶点位置，$\mathbf{n}_i \in \mathbb{R}^3$ 为顶点法线，$\mathbf{h}_i \in \mathbb{R}^d$ 为每个顶点的边嵌入向量。边嵌入是 MeshFlow 的核心机制——它通过连续距离隐式编码离散拓扑：

$$\mathcal{A}_{ij} = \mathbb{I}\left[d(\mathbf{h}_i, \mathbf{h}_j) \leq \tau\right]$$

其中 $d(\cdot, \cdot)$ 为距离函数，$\tau$ 为可学习阈值。若顶点 $i$ 和 $j$ 的边嵌入距离小于 $\tau$，则判定二者之间存在边。这一设计将离散的邻接关系转化为可微的连续函数，使得整个表示可以被梯度下降端到端优化。

从边恢复三角面的过程同样简洁：遍历所有边三元组，若三条边恰好共享三个不同顶点并形成闭环，则该三元组构成一个三角面：

$$F = \left\{ \{f_1, f_2, f_3\} : \{f_1, f_2\}, \{f_2, f_3\}, \{f_3, f_1\} \in E \right\}$$

这里 $E$ 为从边嵌入恢复的有效边集合。面片朝向由预测的顶点法线自动确定，无需显式编码半边结构。

### 3.2 MeshVAE 编码器-解码器架构

MeshVAE 的目标是将上述连续表示压缩为极低维度的潜码 $\mathbf{z}$，并从中高精度重建完整网格。其架构设计围绕两个关键操作：**TokenMerge**（下采样）与**TokenSplit**（上采样），如 Figure 4 所示。

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/005_Figure_4.jpg]]
*Figure 4: Detailed structure of our MeshVAE. We found that using a simple TokenMerge and TokenSplit strategies for downsampling and upsampling enables more effective preservation of the original information, thereby achieving better reconstruction performance*

**编码器** $\mathbf{z} = \mathcal{E}(\mathbf{v}, \mathbf{n}, \mathcal{A})$ 的输入为每个顶点的特征向量，由三部分拼接而成：

$$\mathbf{x}_i = \mathrm{Concat}\left(\mathrm{PE}(\mathbf{v}_i), \mathrm{PE}(\mathbf{n}_i), \mathrm{Concat}_{j \in \mathcal{N}_i}(\mathbf{v}_j)\right)$$

其中 $\mathrm{PE}(\cdot)$ 为 Fourier 位置编码，$\mathcal{N}_i$ 为顶点 $i$ 的邻居顶点集合（由邻接矩阵 $\mathcal{A}$ 提取）。该特征向量同时编码了顶点几何、法线方向及其局部拓扑上下文。

TokenMerge 操作将 $n_v$ 个输入令牌压缩至 $n_v/4$ 个，随后通过 MLP 生成交叉注意力的查询向量。潜码 $\mathbf{z}$ 由压缩令牌与原始特征令牌进行交叉注意力后，再经 $L_e$ 层自注意力得到：

$$\mathbf{z} = \mathrm{SA}^{(L_e)}\left(\mathrm{CA}(\mathbf{z}_{\mathrm{merged}}, \mathbf{X})\right)$$

**解码器** 通过 TokenSplit 操作将潜码上采样回原始顶点数，经自注意力和交叉注意力逐层恢复顶点坐标 $\hat{\mathbf{v}}$、法线 $\hat{\mathbf{n}}$、边嵌入 $\hat{\mathbf{h}}$ 以及有效顶点掩码。

**训练损失** 由五项加权组成：

$$\mathcal{L}_{\mathrm{rec}} = \mathcal{L}_{\mathrm{mask}} + \mathcal{L}_{\mathbf{v}} + \mathcal{L}_{\mathbf{n}} + \mathcal{L}_{\mathrm{adj}} + \lambda_{kl}\mathcal{L}_{kl}$$

其中 $\mathcal{L}_{\mathrm{mask}}$ 为顶点有效性二值交叉熵，$\mathcal{L}_{\mathbf{v}}$ 和 $\mathcal{L}_{\mathbf{n}}$ 分别为顶点坐标和法线的 MSE 损失，$\mathcal{L}_{kl}$ 为潜空间 KL 正则项。核心的 $\mathcal{L}_{\mathrm{adj}}$ 采用对比学习范式，由正边损失和负边损失构成：

$$\mathcal{L}_{\mathrm{pos}} = -\frac{1}{|E|} \sum_{(i,j) \in E} \log\left(\sigma(d(\hat{\mathbf{e}}_i, \hat{\mathbf{e}}_j) - \tau)\right)$$

$$\mathcal{L}_{\mathrm{neg}} = -\frac{1}{|\neg E|} \sum_{(i,j) \notin E} \log\left(\sigma(\tau - d(\hat{\mathbf{e}}_i, \hat{\mathbf{e}}_j))\right)$$

正边损失鼓励真实存在边的顶点嵌入距离小于阈值 $\tau$，负边损失则推动不存在边的顶点嵌入距离大于 $\tau$。这种对比机制使得边嵌入空间自然形成拓扑感知的几何结构。

### 3.3 网格恢复与后处理

从 MeshVAE 解码器输出 $(\hat{\mathbf{v}}, \hat{\mathbf{n}}, \hat{\mathbf{h}})$ 恢复三角网格分为两步：

1. **边恢复**：根据 $\mathcal{A}_{ij} = \mathbb{I}[d(\hat{\mathbf{h}}_i, \hat{\mathbf{h}}_j) \leq \tau]$ 获取有效边集合 $E$。
2. **面恢复**：遍历所有共享三个不同顶点的边三元组，若构成闭环则形成三角面。

由于潜空间压缩可能引入少量边界缺陷，MeshFlow 采用启发式后处理：检测仅属于一个三角面的边界边，将其组织为 $k$-gon 环，对 $k < 5$ 的环进行三角化修补。这一步骤是当前方法的已知局限之一，理想情况下应通过改进训练目标消除对后处理的依赖。

### 3.4 整流流扩散变换器生成

在获得紧凑潜表示后，MeshFlow 采用整流流（Rectified Flow）在潜空间中进行生成。整流流学习一个从噪声分布到数据分布的直线传输路径，其训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \left\| \mathbf{v}_{\theta}(\mathbf{x}, t) - (\epsilon - \mathbf{x}_0) \right\|_2^2$$

其中 $\mathbf{x}_0$ 为真实潜码，$\epsilon \sim \mathcal{N}(0, I)$ 为噪声，$t \in [0, 1]$ 为时间步，$\mathbf{x} = t\epsilon + (1-t)\mathbf{x}_0$ 为插值点。向量场网络 $\mathbf{v}_{\theta}$ 学习预测从噪声指向数据的直线方向 $(\epsilon - \mathbf{x}_0)$。

生成器采用 Diffusion Transformer（DiT）架构，以预训练点云编码器提取的特征令牌和顶点数量为条件。推理时从纯噪声出发，沿学习到的向量场进行 ODE 积分，并行生成全部潜码，再经 MeshVAE 解码器恢复为完整网格。与自回归方法的序列依赖不同，该过程的推理时间仅随网格大小**线性增长**，从根本上突破了二次复杂度瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/003_Figure_2.jpg]]
*Figure 2: Data Statistics Visualization. (Left) Distribution of vertices and faces, showing that the face count is roughly double the vertex count. (Right) Impact of reduced quantization resolution, illustrating that lower resolution leads to increased geometric errors and face collapse*



## 实验与关键发现

### 4.1 网格压缩重建评估

为验证 MeshVAE 的表示能力，我们首先在网格压缩重建任务上进行评估。Table 1 给出了与现有网格编码器的定量对比。MeshVAE 取得了 **CD 1.29**（×100）的最优重建精度，优于 TreeMeshGPT 的 1.63。更重要的是，MeshVAE 的压缩比仅为 **0.014**，比朴素令牌化（每个面 9 个令牌）少 72 倍，比最紧凑的令牌化方法少 16 倍——仅需 $n_v/4$ 个潜向量即可高精度重建完整网格。

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of MeshVAE. The Chamfer Distances (CD) are scaled by a factor of 100. Although some methods share the same 128-level quantization, failures on specific meshes can still shift the average score*

这一优势源于两个关键设计：(1) 连续潜空间消除了顶点坐标的 128 级离散化，避免了量化误差导致的顶点坍塌和面片重叠（Figure 2 右图可视化了低量化分辨率带来的几何退化）；(2) 边嵌入的对比学习将离散拓扑转换为可微的连续表示，使得解码器能从极少量潜码中忠实地恢复拓扑结构。Figure 5 的定性对比显示，基于自回归的方法因网格量化而丢失精细几何细节，而 MeshVAE 在连续空间中工作，能够忠实保留输入网格的细节特征。Figure 6 进一步验证了 MeshVAE 对拓扑信息的忠实保留。

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparisons with other mesh encoders. AR-based methods necessitate mesh quantization. Our MeshVAE works in continuous space, enabling the faithful preservation of the fine details in the input mesh*

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/008_Figure_6.jpg]]
*Figure 6: Reconstruction results of our MeshVAE. Our MeshVAE faithfully retains the topological information of the input geometry within the continuous latent space. Please refer to the supplementary for more results*

### 4.2 点云条件网格生成

在 Toys4K 数据集上的点云条件网格生成任务中，MeshFlow 取得了所有方法中最低的 Chamfer Distance（**CD 2.45**，×100）和 Hausdorff Distance（**HD 6.40**，×100），如 Table 2 所示。Figure 7 的定性对比揭示了自回归方法的两大失效模式：推理时间显著更长，且频繁出现提前终止（early stopping），导致生成不完整的几何。相比之下，MeshFlow 的扩散变换器并行生成所有顶点和边，推理时间恒定且仅随网格大小线性增长，生成速度比最快的自回归方法快 **18 倍**，单物体推理仅约 **1.2 秒**。

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/011_Table_2.jpg]]
*Table 2: Quantitative comparison of shape-conditioned mesh generation on the Toys4K dataset. The CD and HD are scaled by a factor of 100. To ensure consistency, we adopted the “Inf. Time” calculation used by FastMesh, which reports the average inference time of a batch of multiple objects. Notably, processing a single object with AR-based methods often requires 6→ the reported time, whereas our method maintains a constant runtime*

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparisons with baseline methods for mesh generation conditioned on a point cloud. The AR-based methods require significantly longer inference and frequently encounter early stopping, which often results in incomplete geometry. In contrast, our diffusion-based method generates high-quality meshes efficiently*

需要指出的是，Table 2 中的推理时间采用了与 FastMesh 一致的批处理平均计算方式。然而，自回归方法处理单个物体实际需要报告时间的 6 倍，而 MeshFlow 保持恒定运行时间——这意味着实际部署场景下 MeshFlow 的速度优势更为显著。

### 4.3 消融实验

Table 3 给出了 MeshVAE 不同设计选择的消融结果。在令牌下采样策略上，**TokenMerge** 取得了最优的重建质量（F1 分数 **99.78**），显著优于 Q-former 和 FPS（最远点采样）。TokenMerge 类似于像素洗牌（pixel-shuffle）操作，通过 MLP 生成交叉注意力的初始查询，能够更有效地保留原始信息，从而在下采样和上采样过程中保持几何和拓扑的完整性。

![[assets/figures/papers/paper_list_l2261_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MeshFlow_Efficient/figures/010_Table_3.jpg]]
*Table 3: Ablation studies of different MeshVAE settings. All values are scaled by a factor of 100*

### 4.4 失败模式与局限性

尽管 MeshFlow 在定量指标和推理速度上均取得了领先，其生成结果仍存在以下局限：

- **边界孔洞**：生成的网格可能包含少量小孔洞或边界缺陷。当前方法依赖启发式后处理——检测仅属于一个三角面的边界边，形成 k 边形环，并对 $k < 5$ 的环进行三角化修复。这一后处理步骤并非端到端可学习，在复杂边界情况下可能失效。
- **评价指标盲区**：当前使用的 Chamfer Distance 和 Hausdorff Distance 主要衡量几何误差，缺乏对网格拓扑质量（如翻转法线、非流形边、孔洞数量）的自动度量，可能导致指标与视觉质量之间的不一致。
- **纹理缺失**：方法目前仅专注于几何生成，未包含纹理或 UV 映射生成，无法直接输出带纹理的完整资产。



## 定位与知识库关联

### 自回归网格生成的演进与瓶颈

MeshFlow 所回应的核心问题是自回归（Autoregressive, AR）网格生成范式的系统性局限。自 **PolyGen**（Nash et al., ICML 2020）开创性地将网格生成建模为序列预测任务以来，该范式经历了快速迭代：**MeshGPT**（Siddiqui et al., arXiv 2023）采用仅解码器架构生成三角网格，**MeshXL**（Chen et al., arXiv 2024）将其扩展为基础模型规模，**MeshAnything**（Chen et al., arXiv 2024）引入点云条件控制，**EdgeRunner**（Tang et al., arXiv 2024）结合自回归自编码器与潜扩散，**FastMesh**（Kim et al., arXiv 2025）通过确定性面片重建加速推理，**TreeMeshGPT**（Lionar et al., arXiv 2025）探索树形生成结构，**MeshSilksong**（Song et al., arXiv 2025）引入分层令牌化，**Meshtron**（Hao et al., arXiv 2024）则采用层次化Hourglass Transformer。

然而，这些方法共享三个根本瓶颈：

1. **二次方推理复杂度**：自回归逐令牌预测使推理时间随网格面数二次增长，单物体生成常超过20秒。
2. **量化误差累积**：顶点坐标被离散化为有限级别（通常仅128级），引入的量化误差导致顶点坍塌和面片重叠——Figure 2 的右图直观展示了降低量化分辨率如何加剧几何误差与面片坍塌。
3. **序列提前终止**：自回归解码可能在生成完整几何前停止，产生不完整的残缺网格。

### 非自回归路线的并行探索

与 MeshFlow 同期，非自回归网格生成方向也出现了若干探索。**MeshCraft**（He et al., arXiv 2025）采用图卷积自编码器配合扩散变换器进行非自回归生成，但其表示仍依赖离散化。**SpaceMesh**（Shen et al., SIGGRAPH Asia 2024）引入连续半边表示，**PDT**（Wang et al., ACM SIGGRAPH 2025）则通过点分布变换扩散模型生成顶点。这些工作表明领域正在从序列预测向并行生成迁移，但尚未同时解决拓扑连续性、顶点精度和压缩效率的三重挑战。

### MeshFlow 的知识库定位

MeshFlow 在以下维度上建立了独特的知识贡献：

**表示层面**：首次将网格的顶点位置、法线和拓扑连接统一压缩为完全连续的潜空间。边嵌入通过对比学习获得，邻接关系由嵌入距离与阈值比较隐式判定（$\mathcal{A}_{ij} = \mathbb{I}[d(\boldsymbol{h}_i, \boldsymbol{h}_j) \leq \tau]$），彻底消除了离散令牌化和量化操作。这一设计与现有所有基于面索引编码的方法形成根本差异——朴素令牌化每个面需至少9个令牌，最紧凑的方案也需约2.7 $n_f$ 个令牌，而 MeshVAE 仅需 $n_v/4$ 个潜向量（约 $n_f/8$），压缩比达0.014，比最紧凑的自回归令牌化少16倍。

**生成范式层面**：采用整流流扩散变换器（Rectified Flow DiT）实现所有顶点和边的并行生成，推理时间仅随网格大小线性增长。在 Toys4K 数据集上，生成速度比最快的自回归方法快18倍，单物体推理约1.2秒。这一速度优势源于对自回归序列依赖的根本性消除，而非对解码步骤的工程优化。

**拓扑恢复机制**：利用预测的顶点法线自动确定面片朝向，通过边嵌入恢复有效边后，查找三边共享三顶点的闭环形成三角面（$F = \{ \{f_1, f_2, f_3\} : \{f_1, f_2\}, \{f_2, f_3\}, \{f_3, f_1\} \in E \}$），无需显式编码半边结构即可重建有向三角网格。

### 适用边界与局限

MeshFlow 的适用边界受以下因素约束：

1. **几何专注**：当前框架仅生成几何网格，不包含纹理坐标（UV）或材质属性，无法直接输出带纹理的完整资产。这与 MeshGPT 系列部分支持纹理的路线形成互补而非替代关系。

2. **后处理依赖**：生成的网格可能包含少量小孔洞或边界缺陷，当前依赖启发式后处理（边界边检测、k-gon环形成、k<5时的三角化）进行修复。这表明边嵌入的对比学习目标尚不能完全保证拓扑封闭性。

3. **拓扑类型限制**：方法设计围绕三角网格展开，对四边形面或混合拓扑的支持尚未验证。在艺术建模领域，四边形网格常用于细分曲面工作流，这一限制可能影响其在特定管线中的直接适用性。

4. **评价体系缺口**：当前使用的 Chamfer Distance 和 Hausdorff Distance 主要衡量几何误差，缺乏对网格拓扑质量（翻转法线、非流形边、孔洞）的自动度量。这一缺口使生成质量的全面评估依赖于人工检查。

### 开放问题

1. **拓扑完备性**：如何通过改进训练目标或解码器设计，减少甚至消除生成结果中的孔洞，使网格恢复不再依赖启发式后处理？可能的路径包括在边嵌入对比损失中引入全局拓扑约束，或在解码器中加入显式的流形性正则项。

2. **表示可扩展性**：能否将连续边嵌入框架扩展至四边形面或混合拓扑网格？这需要重新设计面片恢复算法，可能涉及对边环检测逻辑的泛化。

3. **纹理协同生成**：如何在当前框架中集成UV映射生成，实现几何与纹理的协同生成？这需要将UV坐标纳入潜空间表示，并处理UV图集切割与几何拓扑的一致性约束。

4. **拓扑质量度量**：如何设计能够自动评估网格拓扑质量的度量指标？理想的指标应能检测翻转法线、孔洞边界、非流形边和自交面，为生成模型的训练和评估提供更全面的反馈信号。



## 原文 PDF

![[paperPDFs/CVPR_2026/MeshFlow_Efficient_Artistic_Mesh_Generation_via_MeshVAE_and_Flow_based_Diffusion_Transformer.pdf]]

---
title: "HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HiFi_BRep_High_Fidelity_Latent_Representation_for_Robust_B_Rep_Generation.pdf
project_link: null
code_link: "https://github.com/1nnoh/HiFi-BRep"
aliases:
- HB
- HiFi-BRep
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过拓扑感知编码器消除填充噪声并限制跨流交互于拓扑邻接对，以及单阶段解码器嵌入可微的流形约束（每条边恰好关联两个面），这两项设计协同作用，直指脆性根源。
primary_logic: 使用可学习查询替代填充来从变长序列中提取固定长度的潜在码，并以显式边-面邻接矩阵作为硬注意力掩码，防止无关面-边对的特征污染；同时将‘每条边恰有两个关联面’的流形约束转化为行级双峰分类目标，使其成为可端到端优化的学习目标，从而在训练中直接促进拓扑有效性。
claims:
- 拓扑感知编码器通过可学习查询消除填充噪声，并通过拓扑掩码限制注意力范围，从而学习到高保真潜在表示。
- 单阶段解码器将几何与拓扑并行预测，并采用行级双峰目标强制每条边关联两个面，避免了级联错误和后处理 mismatch。
- 在 DeepCAD 和 ABC 数据集上，HiFi-BRep 的生成有效性（Validity）显著超越此前最佳方法，并且可编译性与有效性差距大幅缩小。
- DeepCAD 上 Validity (%) = 72.20
---

# HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation

> [!tip] 核心洞察
> 使用可学习查询替代填充来从变长序列中提取固定长度的潜在码，并以显式边-面邻接矩阵作为硬注意力掩码，防止无关面-边对的特征污染；同时将‘每条边恰有两个关联面’的流形约束转化为行级双峰分类目标，使其成为可端到端优化的学习目标，从而在训练中直接促进拓扑有效性。

| 字段 | 内容 |
|------|------|
| 中文题名 | HiFi-BRep：用于鲁棒 B-Rep 生成的高保真潜在表示 |
| 英文题名 | HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hou_HiFi-BRep_High-Fidelity_Latent_Representation_for_Robust_B-Rep_Generation_CVPR_2026_paper.html) · [Code](https://github.com/1nnoh/HiFi-BRep) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/generative_models_diffusion/diffusion_image_video |
| Method | HiFi-BRep |
| Dataset | DeepCAD, ABC |

> [!tip] 效果简介
> - DeepCAD 上，Validity (%) 72.20 vs 43.20 (DTGBrepGen) (+29.0)；Compilability→Validity gap (%) 18.18 (90.38→72.20) vs 49.28 (92.48→43.20 for DTGBrepGen) (−31.10)；Inference time (s/shape) 3.83 vs 8.09 (BRepGen) (−52.7% (2.1× faster))。
> - ABC 上，Validity (%) 32.66 vs 24.88 (DTGBrepGen) (+7.78)。

## 概要

**HiFi-BRep** 针对现有 B-Rep 生成方法中两大根本性脆性提出统一解决方案：**表示脆性**——因序列填充引入噪声、无约束跨流注意力导致面/边特征污染；**生成脆性**——级联式生成引起误差累积，训练后非可微的合法性修复造成训练-推理不匹配。这两类脆性使得同时保证几何保真度与拓扑有效性极为困难。

HiFi-BRep 的核心设计通过两个因果调节变量直指脆性根源：

1. **拓扑感知双流编码器**：用可学习查询替代填充，从变长序列中提取无噪声的固定长度潜在码；同时将显式边-面邻接矩阵作为硬注意力掩码（Topo-Mask），严格限制跨流交互仅发生在拓扑相邻对之间，杜绝无关特征污染。
2. **单阶段合法性约束解码器**：摒弃级联范式，并行联合预测几何与拓扑；将“每条边恰好关联两个面”的流形约束转化为可微的行级双峰分类目标，使拓扑有效性在训练中直接得到优化，而非延迟到后处理阶段。

在 **DeepCAD** 和 **ABC** 数据集上的无条件生成实验中，HiFi-BRep 的生成有效性（Validity）分别达到 **72.20%** 和 **32.66%**，较此前最优方法 DTGBrepGen 分别提升 **+29.0** 和 **+7.78** 个百分点。更关键的是，可编译性与有效性之间的差距大幅缩小——在 DeepCAD 上从 49.28 降至 **18.18**，表明模型生成的形状即便可编译，也远更可能真正满足流形约束。推理速度方面，HiFi-BRep 以 **3.83 s/shape** 的耗时比 BRepGen 快约 2.1 倍。

消融实验进一步验证了各组件的因果贡献：移除单阶段设计导致重建有效性从 95.2% 骤降至 69.3%；将行级双峰目标替换为独立 BCE 损失会破坏边-面邻接约束；去除 Topo-Mask 则因引入无关交互而损害重建质量。

HiFi-BRep 的方法定位可概括为：在 B-Rep 生成领域，首次将**拓扑感知的表示学习**与**可微流形约束**统一在端到端框架中，为鲁棒且高保真的 CAD 模型生成提供了新的基准。

### 边界表示（B-Rep）的生成需求与核心挑战

边界表示（Boundary Representation, B-Rep）是计算机辅助设计（CAD）领域的主流几何建模范式，通过显式存储拓扑实体（面、边、顶点）及其连接关系来精确描述三维形状。B-Rep 的生成能力对于自动化设计探索、仿真驱动优化和逆向工程等下游任务具有关键价值。然而，B-Rep 的生成远比其他三维表示（如网格、点云）更具挑战性，原因在于其必须同时满足两个强约束：**几何保真度**（曲面的精确数学描述）和**拓扑有效性**（满足流形条件，如每条边恰好关联两个面）。这两个目标的耦合使得生成任务成为一个高度结构化的离散-连续联合优化问题。

### 现有方法的双重脆性

近年来，基于深度学习的 B-Rep 生成方法取得了一定进展，包括 **DeepCAD** (Wu et al., ICCV 2021)、**BRepGen** (Xu et al., TOG 2024)、**DTGBrepGen** (Li et al., CVPR 2025)、**BrepDiff** (Lee et al., SIGGRAPH 2025) 和 **HoLa** (Liu et al., TOG 2025) 等代表性工作。然而，这些方法普遍面临两类根本性的脆性问题，严重制约了生成质量的上限。

**表示脆性（Representation Fragility）** 源于两个设计缺陷。其一，现有方法通常使用填充（padding）将变长的面/边序列补齐至固定长度以适配 Transformer 架构，但填充 token 在注意力计算中引入噪声，污染了潜在表示。其二，跨流注意力（cross-stream attention）不加约束地允许所有面-边对交互，忽略了 B-Rep 的拓扑局部性——实际上，一个面仅与其边界上的边存在有意义的几何-拓扑耦合。这种无差别的全局交互导致无关特征相互污染，削弱了潜在编码的判别力。

**生成脆性（Generation Fragility）** 同样来自两个关键瓶颈。其一，主流方法采用级联（cascaded）生成范式——例如先解码几何再预测拓扑，或分层次逐步生成——这种顺序依赖导致前序模块的误差向后累积，使得拓扑预测在已受损的几何基础上进行，严重损害最终有效性。其二，流形合法性（manifold validity）通常被推迟到训练后的非可微后处理阶段进行修复，而非作为训练目标的一部分。这种训练-推理的不匹配（mismatch）意味着模型在训练时从未被显式引导去生成合法拓扑，导致推理输出大量无效结构，需依赖不可靠的后处理修补。

这两类脆性的叠加效应在现有方法的实验结果中体现得尤为明显：即便部分方法在可编译性（compilability）上达到较高水平，其实际有效性（validity）却大幅滑坡，两者之间存在巨大鸿沟——例如 DTGBrepGen 在 DeepCAD 数据集上的可编译性为 92.48%，但有效性仅 43.20%，差距高达 49.28 个百分点。这表明现有方法能够生成语法正确的结构，却无法保证拓扑的流形合法性。

### 本文动机与核心思路

针对上述瓶颈，HiFi-BRep 的核心动机是：**通过重新设计编码器和解码器，从根本上消除表示脆性和生成脆性的成因，而非依赖后处理来弥补缺陷**。具体而言，本文提出两个协同设计：

- **拓扑感知编码器**：使用可学习查询（learnable queries）替代填充来聚合变长序列，消除填充噪声；同时将显式的边-面邻接矩阵转化为硬注意力掩码（Topo-Mask），严格限制跨流交互仅发生在拓扑相邻的面对之间，防止特征污染。
- **单阶段合法性约束解码器**：摒弃级联范式，在单一阶段内并行预测几何参数与拓扑邻接关系，实现双向联合优化；并将“每条边恰有两个关联面”的流形约束嵌入为可微的行级双峰分类目标，使其成为训练过程中直接优化的学习目标，从而在源头促进拓扑有效性。

这一设计理念的预期效果是：潜在表示更干净、更具判别力，解码过程更稳定、更自洽，最终显著缩小可编译性与有效性之间的差距，同时提升生成效率。

## 核心方法与创新机理

HiFi-BRep 的核心创新在于系统性地解决了现有 B-Rep 生成方法中“表示脆性”与“生成脆性”两大瓶颈，通过四项关键设计（changed slots）协同作用，首次实现了高保真潜在表示下的鲁棒生成。

### 1. 从填充到可学习查询：消除表示噪声

现有方法（如 **DeepCAD** (Wu et al., ICCV 2021)、**BRepGen** (Xu et al., TOG 2024)）通常使用填充（padding）将变长的面/边序列补齐至固定长度，以适配 Transformer 架构。然而，填充 token 在注意力计算中会引入无意义的噪声，污染特征表示。

HiFi-BRep 的编码器摒弃了填充方案，转而引入一组**可学习查询（learnable queries）**，通过交叉注意力机制从变长序列中聚合信息，直接输出干净的固定长度潜在码。这一设计从根源上消除了填充噪声，使得潜在空间能够更忠实地编码 B-Rep 的几何与拓扑结构。

### 2. 拓扑掩码：约束跨流交互，防止特征污染

B-Rep 的面流（face stream）和边流（edge stream）之间存在天然的稀疏关联——每条边仅与恰好两个面相邻。然而，现有方法的跨流注意力通常不加约束，允许所有面-边对自由交互，导致无关特征相互污染。

HiFi-BRep 利用显式的边-面邻接矩阵 $\mathbf{A}$ 构建**拓扑掩码（Topo-Mask）**，将其作为硬注意力掩码嵌入跨流注意力计算：

$$\mathrm{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V};\mathbf{S}) = \mathrm{softmax}\Big(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d}} + \mathbf{S}\Big)\mathbf{V},\quad \mathbf{S}[u,i] = \begin{cases}0, & \mathbf{A}[u,i]=1,\\-\infty, & \mathrm{otherwise}.\end{cases}$$

该掩码严格限制注意力仅在拓扑相邻的边-面对之间进行，将跨流交互的复杂度从 $O(F_{\max}E_{\max}D)$ 降至 $O(\|\mathbf{A}\|_0 D)$，同时确保了特征聚合的拓扑一致性。

### 3. 单阶段并行解码：消除级联误差累积

此前方法普遍采用级联生成范式——先解码几何，再基于几何预测拓扑（如 **DTGBrepGen** (Li et al., CVPR 2025)），或分层逐步生成。这种多阶段流程导致前序误差向后序累积，严重损害最终输出的有效性。

HiFi-BRep 采用**单阶段并行解码器**，从潜在码中联合预测面/边数量、几何参数（Bézier 控制点、包围盒、顶点）以及边-面邻接矩阵。几何与拓扑的预测在同一解码过程中双向交互优化，从根本上切断了级联误差的传播路径。消融实验证实：若将单阶段设计替换为级联方案（先解码几何再单独预测拓扑），重建有效性从 **95.2% 骤降至 69.3%**，邻接准确率从 97.5% 降至 73.2%。

### 4. 可微流形约束：将合法性内化为学习目标

传统方法依赖训练后的非可微后处理（如基于内核的合法性修复）来修正拓扑错误，这导致训练与推理之间存在严重 mismatch——模型在训练时从未学习如何生成合法拓扑。

HiFi-BRep 将核心流形约束——“每条边恰好关联两个面”——转化为**行级双峰分类目标（row-wise two-peak objective）**。具体而言，对邻接矩阵的每一行（对应一条边）施加 softmax 后，监督其输出两个概率峰，分别指向该边关联的两个面。这一可微损失直接嵌入 VAE 训练总目标：

$$\mathcal{L} = \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{len}}[\mathrm{CE}(\hat{n}_f,n_f) + \mathrm{CE}(\hat{n}_e,n_e)] + \lambda_{\mathrm{geom}}\mathcal{L}_{\mathrm{geom}} + \lambda_{\mathrm{adj}}\mathcal{L}_{\mathrm{row-wise}}(S)$$

消融实验表明，将行级双峰目标替换为独立的 BCE 损失后，边-面邻接准确率显著下降，进一步验证了该约束作为学习目标的必要性。

### 协同效应：从脆性到鲁棒性

上述四项设计并非孤立改进，而是形成了闭环协同：**可学习查询**与**拓扑掩码**共同构建了高保真的潜在表示，为解码器提供了干净的输入；**单阶段解码**与**可微流形约束**则确保从该表示中可以端到端地生成几何精确且拓扑有效的 B-Rep。这一协同最终体现在生成结果上——在 DeepCAD 数据集上，HiFi-BRep 的 Validity 达到 **72.20%**，较此前最佳方法 DTGBrepGen 的 43.20% 提升 **+29.0 个百分点**；Compilability–Validity 差距从 49.28 大幅缩小至 18.18，表明模型生成的形状更接近可直接编译的工业标准。

HiFi-BRep 采用两阶段流水线：先训练一个变分自编码器（VAE）将 B-Rep 压缩到高保真潜在空间，再在该潜在空间中训练一个去噪扩散概率模型（DDPM）实现无条件或条件生成。VAE 由**拓扑感知双流编码器**和**单阶段合法性约束解码器**组成，二者通过固定长度的潜在码连接，形成端到端可训练的压缩-重建通路。

**输入表示**：每个 B-Rep 被分解为面（face）和边（edge）两类基元。面特征由包围盒嵌入与 Bézier 控制网格嵌入求和得到；边特征由包围盒嵌入、控制点嵌入和显式端点嵌入求和得到。全局拓扑结构通过边-面邻接矩阵显式编码，矩阵元素指示每条边与哪些面相邻。

**编码器**接收变长的人脸和边序列，通过双流 Transformer 进行特征提取。每个 BiModalBlock 首先在面和边流内分别执行自注意力，随后在跨流交互中引入 **Topo-Mask**——基于边-面邻接矩阵的硬注意力掩码，仅允许拓扑相邻的边-面对参与交叉注意力，杜绝无关基元间的特征污染。经过若干层双流编码后，使用一组**可学习查询**（learnable queries）对变长序列进行池化，输出固定长度的潜在码，从而消除传统填充方案引入的噪声。

**解码器**从潜在码出发，采用“先计数量、再解内容”的策略：首先预测面和边的数量，据此构建硬填充掩码以处理变长歧义；随后通过若干 **DecBiBlock** 以拓扑感知方式联合解码几何与拓扑信息。几何头回归 Bézier 曲面/曲线的控制点、包围盒和顶点坐标；拓扑求解头通过行级 softmax 预测边-面邻接矩阵，并受**行级双峰目标**监督，强制每条边恰好关联两个面——将核心流形约束嵌入为可微学习目标，避免训练后非可微后处理带来的训练-推理不匹配。

**扩散模型**在训练好的 VAE 潜在空间中学习去噪扩散概率模型，支持无条件生成以及类别标签、点云、图像等多模态条件生成。

![[assets/figures/papers/paper_list_l885_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_HiFi_BRep_High_Fid/figures/003_Figure_3.jpg]]
*Figure 3: Overview of HiFi-BRep. (a) Face and edge tokens undergo per-stream self-attention and cross-stream attention masked by edgeface incidence (Topo-Mask), then learnable queries pool them into a fixed-length latent. (b) The decoder first predicts face and edge counts to build hard padding masks, then updates learnable face and edge queries. Stacked DecBiBlocks then decode topology-aware geometry sequences. Geometry heads regress primitive parameters, while a topology solver head predicts adjacency with row-wise softmax and two-peak targets*

### 3.1 输入表示：几何-拓扑解耦的特征构建

HiFi-BRep 将 B-Rep 分解为面（face）和边（edge）两类基本元素，并为每类元素构建统一的几何-拓扑特征（Figure 2）。面的特征由包围盒嵌入与 Bézier 控制网格嵌入求和得到；边的特征由包围盒嵌入、控制点嵌入和显式端点嵌入求和得到。全局结构连接关系通过显式的边-面邻接矩阵 $\mathbf{A}$ 编码，其中 $\mathbf{A}[u,i]=1$ 表示边 $u$ 与面 $i$ 拓扑相邻。

![[assets/figures/papers/paper_list_l885_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_HiFi_BRep_High_Fid/figures/002_Figure_2.jpg]]
*Figure 2: Input B-Rep formulation. We construct unified primitive features by decomposing the shape into geometric and topological components. Specifically, we derive the face feature by summing the embeddings of the bounding box*

### 3.2 拓扑感知双流编码器

编码器采用双流 Transformer 架构（Figure 3a），分别处理面序列和边序列。核心创新在于两点：

**（1）Topo-Mask 跨流注意力。** 面流和边流各自进行流内自注意力后，通过双向跨流注意力交换信息。为防止无关面-边对的特征污染，跨流注意力被显式边-面邻接矩阵 $\mathbf{A}$ 硬约束：

$$
\mathrm{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V};\mathbf{S}) = \mathrm{softmax}\Big(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d}} + \mathbf{S}\Big)\mathbf{V},\quad \mathbf{S}[u,i] = \begin{cases}0, & \mathbf{A}[u,i]=1,\\-\infty, & \mathrm{otherwise}.\end{cases}
$$

其中 $\mathbf{S}$ 为基于邻接矩阵的硬注意力掩码——仅当边 $u$ 与面 $i$ 拓扑相邻时允许交互，否则注意力权重被置零。这一设计将跨流交互严格限制在有物理意义的邻接对上，从根源上消除了无关特征污染。

**（2）可学习查询池化。** 传统方法使用填充（padding）将变长序列补齐至固定长度，引入噪声。HiFi-BRep 采用一组可学习查询（learnable queries）通过交叉注意力从面/边序列中聚合信息，输出固定长度的干净潜在序列，完全消除了填充噪声。

### 3.3 单阶段合法性约束解码器

解码器（Figure 3b）摒弃了级联生成范式，采用单阶段并行解码，联合预测几何参数与拓扑关系。

**数量预测优先。** 解码开始时，首先通过计数预测器输出面数 $\hat{n}_f$ 和边数 $\hat{n}_e$，以此构建硬掩码，解决变长序列歧义。

**拓扑感知解码块（DecBiBlocks）。** 可学习的面查询和边查询经过堆叠的 DecBiBlocks 进行拓扑感知解码，其内部同样使用 Topo-Mask 约束跨流交互。

**几何头。** 并行回归 Bézier 曲面/曲线的控制点、包围盒和顶点坐标。

**拓扑求解头。** 预测边-面邻接矩阵 $\mathbf{S}$，对每一行（每条边）施加行级 softmax，并以双峰目标分布监督——强制每条边恰好关联两个面，将流形约束嵌入为可微学习目标。

### 3.4 训练目标

VAE 的总损失由四项组成：

$$
\mathcal{L} = \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{len}}[\mathrm{CE}(\hat{n}_f,n_f) + \mathrm{CE}(\hat{n}_e,n_e)] + \lambda_{\mathrm{geom}}\mathcal{L}_{\mathrm{geom}} + \lambda_{\mathrm{adj}}\mathcal{L}_{\mathrm{row-wise}}(S)
$$

其中 $\mathcal{L}_{\mathrm{KL}}$ 为潜在空间 KL 散度；第二项为面/边数量的交叉熵损失；$\mathcal{L}_{\mathrm{geom}}$ 为掩码几何重建损失：

$$
\mathcal{L}_{\mathrm{geom}} = \mathrm{MSE}(\widehat{F}_z, F_z) + \mathrm{MSE}(\widehat{E}_z, E_z) + \mathrm{MSE}(\widehat{F}_p, F_p) + \mathrm{MSE}(\widehat{E}_p, E_p) + \mathrm{MSE}(\widehat{\mathcal{V}}, \mathcal{V})
$$

分别监督面/边 Bézier 控制点、包围盒及顶点的重建精度（仅对有效元素计算 MSE）；$\mathcal{L}_{\mathrm{row-wise}}(S)$ 为行级双峰邻接损失，强制边-面邻接矩阵每行恰有两个激活值。

### 3.5 潜在扩散模型

在 VAE 训练收敛后，于其潜在空间中训练去噪扩散概率模型（DDPM），支持无条件生成及类别标签、点云、图像等条件生成。

### 3.6 复杂度分析

编码器中，面流自注意力复杂度为 $\mathcal{O}(F_{\max}^2 D)$，边流自注意力为 $\mathcal{O}(E_{\max}^2 D)$。Topo-Mask 跨流注意力仅计算邻接对，复杂度为 $\mathcal{O}(\|\mathbf{A}\|_0 D)$，其中 $\|\mathbf{A}\|_0$ 为邻接矩阵非零元数量。在流形 B-Rep 中每条边恰关联两个面，故 $\|\mathbf{A}\|_0 = 2E$，跨流注意力实际为线性复杂度，显著低于全对全注意力的 $\mathcal{O}(F_{\max}E_{\max}D)$。

## 实验与关键发现

HiFi-BRep 在无条件生成任务上进行了系统评估，涵盖 DeepCAD 和 ABC 两个标准数据集，与 **DeepCAD** (Wu et al., ICCV 2021)、**BRepGen** (Xu et al., TOG 2024)、**DTGBrepGen** (Li et al., CVPR 2025)、**BrepDiff** (Lee et al., SIGGRAPH 2025) 和 **HoLa** (Liu et al., TOG 2025) 等代表性基线进行全面对比。评估指标包括有效性（Validity）、可编译性（Compilability）、倒角距离（MMD-CD）和 Jensen-Shannon 散度（JSD）。

### 无条件生成主结果

Table 1 汇总了 DeepCAD 和 ABC 两个数据集上的无条件生成性能。HiFi-BRep 在核心指标上取得显著突破：

![[assets/figures/papers/paper_list_l885_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_HiFi_BRep_High_Fid/figures/004_Table_1.jpg]]
*Table 1: Unconditional generation on DeepCAD and ABC. Best is bold, second-best is underlined. MMD-CD and JSD are ×100 (DeepCAD convention)*

- **有效性大幅领先**：在 DeepCAD 上，HiFi-BRep 达到 72.20% 的有效性，较此前最佳方法 DTGBrepGen 的 43.20% 提升 29.0 个百分点；在 ABC 上，有效性为 32.66%，较 DTGBrepGen 的 24.88% 提升 7.78 个百分点。ABC 数据集因包含更复杂的拓扑结构，整体有效性低于 DeepCAD，但 HiFi-BRep 的相对优势依然显著。

- **可编译性-有效性差距大幅缩小**：此前方法普遍存在“可编译但无效”的问题——模型生成的 B-Rep 可通过内核编译，但因拓扑不合法而被剔除。在 DeepCAD 上，DTGBrepGen 的可编译性为 92.48%，但有效性仅 43.20%，差距高达 49.28 个百分点。HiFi-BRep 将这一差距压缩至 18.18 个百分点（90.38% → 72.20%），表明其端到端嵌入的流形约束有效弥合了训练-推理不匹配。

- **几何质量保持竞争力**：HiFi-BRep 在 DeepCAD 上取得最低的 MMD-CD（1.05），在 ABC 上几何指标与最优方法可比。这表明有效性提升并非以牺牲几何保真度为代价。

### 消融实验

Table 2 通过 DeepCAD 重建任务系统验证各设计组件的贡献。完整模型达到面数准确率 100.0%、边数准确率 99.5%、邻接准确率 97.5%、重建有效性 95.2%。

![[assets/figures/papers/paper_list_l885_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_HiFi_BRep_High_Fid/figures/008_Table_2.jpg]]
*Table 2: Ablations on DeepCAD reconstruction. Metrics: Face Acc = face-count accuracy; Edge Acc = edge-count accuracy; Adj Acc = edge–face incidence matrix accuracy*

**单阶段解码是关键**：将单阶段联合解码替换为级联方案（先解码几何，再单独预测拓扑）导致重建有效性从 95.2% 骤降至 69.3%，邻接准确率从 97.5% 降至 73.2%。这一 25.9 个百分点的降幅揭示了级联生成中误差累积的严重性——几何解码的微小偏差会传播至拓扑预测阶段，造成不可恢复的邻接错误。

**行级双峰目标不可替代**：将行级双峰分类目标替换为独立 BCE 损失后，每行的边-面邻接预测失去竞争约束，破坏了“每条边必须恰好关联两个面”的流形条件，邻接准确率随之下降。这验证了将流形约束转化为可微学习目标的必要性。

**Topo-Mask 防止特征污染**：移除编码器中的拓扑掩码后，无关面-边对之间的跨流交互引入噪声，导致重建质量下降。这证实了限制注意力范围于拓扑邻接对是学习高保真潜在表示的关键。

**规范顺序稳定训练**：添加面/边序列的规范排序可减少排列方差，提升训练稳定性和模型鲁棒性。

### 推理效率

Table 3 的推理耗时对比显示，HiFi-BRep 在 DeepCAD 上平均每形状推理时间仅 3.83 秒，较 BRepGen 的 8.09 秒加速约 2.1 倍（−52.7%）。这得益于单阶段并行解码设计消除了级联方法的串行等待开销，同时 Topo-Mask 将跨流注意力复杂度从 $O((F_{\text{max}}+E_{\text{max}})^2 D)$ 降至 $O(\|\mathbf{A}\|_0 D)$。

![[assets/figures/papers/paper_list_l885_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_HiFi_BRep_High_Fid/figures/009_Table_3.jpg]]
*Table 3: Runtime comparison (seconds per shape) on the Deep-CAD dataset. Results are averaged over 1000 runs*

### 失败模式分析

尽管整体有效性显著提升，HiFi-BRep 仍存在三类典型失败模式（Figure 6）：

1. **裁剪不一致/缺失面片**：面数预测正确，但解码的环未能形成有效裁剪区域，内核在合并阶段丢弃该面。这源于当前框架缺少可微的裁剪可行性约束。

2. **结点不一致/非流形边**：合并后的 T 型结点或重复线段破坏了流形邻接关系。行级双峰目标虽强制每条边关联两个面，但无法保证结点级别的几何一致性。

3. **退化几何/薄片**：控制点病态导致近零面积或自交面片。这表明几何回归头在极端参数配置下仍不够鲁棒。

这些失败模式指向一个共同瓶颈：当前方法缺少可微的可行性投影机制，无法在解码过程中主动修正裁剪不一致和结点错误。此外，解码器使用固定容量预算（最大面/边数），对高面数长尾形状的适应性有限——Figure 5 显示，当面数超过常见范围时，重建有效性从 >90% 降至约 61.5%。

![[assets/figures/papers/paper_list_l885_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_HiFi_BRep_High_Fid/figures/006_Figure_5.jpg]]
*Figure 5: Reconstruction validity by face count on DeepCAD. Validity remains stable across common counts and ≥ 61.5% in high–face-count bins, evidencing robust generalization from the encoder*

### 关键图表

- **Table 1**：无条件生成定量对比，展示有效性、可编译性及几何质量的全维度评估。
- **Table 2**：消融实验结果，量化单阶段设计、行级双峰目标、Topo-Mask 和规范排序的贡献。
- **Table 3**：推理耗时对比，验证单阶段设计的效率优势。
- **Figure 5**：按面数分桶的重建有效性，揭示模型在长尾拓扑上的泛化边界。
- **Figure 6**：典型失败案例，为后续改进提供明确方向。

## 定位与知识库关联

### 1. 问题域与基线谱系

HiFi-BRep 定位于**边界表示（B-Rep）的生成建模**，即从潜在空间中采样并生成由参数化曲面/曲线与显式拓扑邻接关系构成的 CAD 实体模型。该领域近年来涌现出多条技术路线，HiFi-BRep 所对比的核心基线构成了一条清晰的方法谱系：

- **DeepCAD** (Wu et al., ICCV 2021)：早期基于 Transformer 的 B-Rep 生成方法，采用级联生成流程，先解码几何参数再预测拓扑关系，其生成有效性受限于误差累积与训练-推理不匹配。
- **BRepGen** (Xu et al., TOG 2024)：引入扩散模型进行 B-Rep 生成，但仍沿用多阶段级联范式，且使用填充（padding）处理变长序列，引入噪声。
- **DTGBrepGen** (Li et al., CVPR 2025)：通过层次化生成与拓扑约束增强有效性，在 HiFi-BRep 出现前保持 DeepCAD 数据集上的最高 Validity（43.20%）。
- **BrepDiff** (Lee et al., SIGGRAPH 2025) 与 **HoLa** (Liu et al., TOG 2025)：分别从扩散建模与层次化潜在表示角度推进生成质量，但均未从根本上解决表示脆性与生成脆性的耦合问题。

HiFi-BRep 的突破在于**同时直指两大脆性根源**：在编码侧通过可学习查询消除填充噪声、通过拓扑掩码限制跨流交互范围；在解码侧以单阶段并行预测替代级联流程，并将流形约束嵌入可微学习目标。这种“编码高保真 + 解码合法性内生”的设计使其在 DeepCAD 上的生成有效性达到 72.20%，较此前最佳方法 DTGBrepGen 提升 29 个百分点；在 ABC 数据集上达到 32.66%，提升 7.78 个百分点（Table 1）。

### 2. 核心设计决策的因果机制

HiFi-BRep 的方法贡献可归纳为四个关键设计槽位，每个槽位的变更都直指现有方法的脆性根源：

| 设计槽位 | 基线做法 | HiFi-BRep 做法 | 解决的问题 |
|:---|:---|:---|:---|
| 序列聚合方式 | 填充补齐至固定长度 | 可学习查询聚合变长序列 | 消除填充噪声，生成干净的固定长度潜在码 |
| 跨流注意力范围 | 无约束的面-边全交互 | Topo-Mask 限制于邻接对 | 防止无关面-边对的特征污染 |
| 生成流程 | 多阶段级联（先几何后拓扑） | 单阶段并行解码，联合预测 | 消除级联误差累积，实现几何-拓扑双向优化 |
| 流形合法性处理 | 训练后非可微后处理修复 | 行级双峰分类目标嵌入训练 | 消除训练-推理不匹配，直接促进拓扑有效性 |

**因果链条**：编码器的可学习查询（图 3a）从变长面/边序列中提取固定长度潜在码，避免了填充 token 对注意力计算的干扰；同时，基于显式边-面邻接矩阵的 Topo-Mask 将跨流注意力严格限制在 $A[u,i]=1$ 的位置（$S[u,i]=0$），其余位置置为 $-\infty$，从而从机制上杜绝无关交互。解码器首先预测面/边数量以解决变长歧义，随后通过 DecBiBlocks 并行更新面/边查询，几何头回归 Bézier 控制点与顶点，拓扑头以行级 softmax 预测边-面邻接矩阵，并通过双峰目标强制每条边恰好关联两个面。这种端到端的合法性约束是 HiFi-BRep 将 Compilability–Validity 差距从 49.28 个百分点压缩至 18.18 个百分点的关键（Table 1）。

### 3. 适用边界

HiFi-BRep 的设计存在明确的适用范围：

- **仅适用于封闭流形实体**：当前框架假设每条边恰好关联两个面，无法直接处理开放边界模型（如曲面片、壳体）或装配体（多体组合）。
- **固定容量预算**：解码器使用预设的最大面数 $F_{\text{max}}$ 和边数 $E_{\text{max}}$，对于面数极多的长尾形状缺乏灵活性。实验表明，在面数超过 50 的高面数区间，重建有效性从常见区间的 >90% 降至约 61.5%（Figure 5）。
- **Bézier 参数化假设**：几何表示依赖 Bézier 曲面/曲线的控制点、包围盒与顶点坐标，无法直接适配其他曲面类型（如 NURBS、细分曲面）。

### 4. 局限与失败模式

尽管 HiFi-BRep 大幅提升了生成有效性，论文明确列出了三类典型失败模式（Figure 6）：

1. **裁剪不一致 / 缺失面片**：面数量预测正确，但解码的环（loop）无法形成有效的裁剪区域，导致几何内核丢弃该面。
2. **结点不一致 / 非流形边**：T 型结点或合并后的重复线段破坏了流形邻接关系，产生非流形边。
3. **退化几何 / 薄片面**：控制点病态导致近零面积或自交面片，无法通过合法性检查。

这些失败模式揭示了一个深层局限：**当前框架缺少可微的可行性投影机制**来在解码过程中直接修正裁剪不一致和结点错误。行级双峰目标仅约束了边-面邻接数量的合法性，但无法保证邻接关系的几何一致性（如环的闭合性、裁剪区域的有效性）。

### 5. 开放问题

基于上述局限，论文与 verified analysis 共同指向以下开放问题：

- **扩展到开放边界与装配体**：如何重新设计流形约束，使其支持边界边（仅关联一个面）和多体拓扑，是通向通用 CAD 生成的关键。
- **动态容量解码器**：能否使用变长查询（而非固定数量）来适应长尾拓扑分布，避免固定容量预算对复杂形状的限制？
- **可微可行性投影**：能否将裁剪一致性、结点合法性等几何约束转化为可微损失或投影层，在解码过程中直接抑制错误，进一步缩小 Compilability–Validity 差距？
- **长尾拓扑泛化**：如何提升高面数区间的生成质量，使有效性在复杂形状上也能维持 >90% 的水平？

### 6. 知识库定位

HiFi-BRep 在 B-Rep 生成领域的知识贡献可定位为**从“表示-生成耦合脆性”到“高保真潜在空间 + 内生合法性”的范式转换**。其核心洞察——用可学习查询替代填充、用拓扑掩码限制注意力、用行级双峰目标替代后处理修复——不仅适用于 B-Rep 生成，也对其他结构化几何表示（如网格、点云序列）的编码器-解码器设计具有启发意义。该方法已在 DeepCAD 和 ABC 两个标准基准上验证，代码开源（https://github.com/1nnoh/HiFi-BRep），为后续研究提供了可复现的基线。

## 原文 PDF

![[paperPDFs/CVPR_2026/HiFi_BRep_High_Fidelity_Latent_Representation_for_Robust_B_Rep_Generation.pdf]]

---
title: "CoRoGS: Contextual Gaussian Splatting for Robust Large-Deviation View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CoRoGS_Contextual_Gaussian_Splatting_for_Robust_Large_Deviation_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- CCAGS
- CoRoGS
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入上下文推理机制，通过图神经网络在高斯间进行消息传递，建模依赖关系，并利用渐进式图扩张增强场景覆盖。
primary_logic: 将高斯表示从独立基元转化为上下文感知的图结构，利用Delaunay三角剖分构建高斯图，并通过几何与语义双分支的消息传递和跨模态融合实现一致性高斯更新，辅以语义引导的上下文平滑损失和自适应图扩张，从而在大视角偏差下保持全局结构连贯和高保真渲染。
claims:
- CoRoGS adopts a contextual formulation that explicitly models inter-Gaussian dependencies.
- This representation is implemented by constructing a 3D Gaussian graph, which propagates relational geometry and semantics via message passing, resulting in context-aware Gaussian...
- We incorporate a progressive graph expansion strategy that adaptively grows and prunes Gaussians.
- We present Context-Aware Gaussian Splatting, which instantiates this formulation via graph-based contextual reasoning, achieving superior rendering quality and robust generalizati...
---

# CoRoGS: Contextual Gaussian Splatting for Robust Large-Deviation View Synthesis

> [!tip] 核心洞察
> 将高斯表示从独立基元转化为上下文感知的图结构，利用Delaunay三角剖分构建高斯图，并通过几何与语义双分支的消息传递和跨模态融合实现一致性高斯更新，辅以语义引导的上下文平滑损失和自适应图扩张，从而在大视角偏差下保持全局结构连贯和高保真渲染。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoRoGS：面向鲁棒大偏差视图合成的上下文感知高斯泼溅 |
| 英文题名 | CoRoGS: Contextual Gaussian Splatting for Robust Large-Deviation View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_CoRoGS_Contextual_Gaussian_Splatting_for_Robust_Large-Deviation_View_Synthesis_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | CoRoGS (Context-Aware Gaussian Splatting) |
| Dataset | KITTI, KITTI & Waymo |

> [!tip] 效果简介
> - KITTI (0.5m lateral right-shift, supervised) 上，PSNR↑ 24.96；SSIM↑ 0.849；LPIPS↓ 0.180。

## 概要

### 研究问题与瓶颈

大偏差新视图合成（Large-Deviation Novel View Synthesis, LD-NVS）要求模型在训练视角覆盖范围之外生成高质量渲染结果，这对自动驾驶等应用中的稀疏采样场景至关重要。以 **3DGS**（Kerbl et al., ACM TOG 2023）为代表的显式辐射场方法虽在常规视图合成中表现优异，但其根本瓶颈在于：**将高斯核视为相互独立的基元，缺乏对高斯间空间与语义依赖关系的显式建模**。当测试视角大幅偏离训练轨迹时，独立优化得到的高斯属性无法保持全局结构一致性，导致几何错位、外观退化和语义混乱。

### 核心方法定位

**CoRoGS（Context-Aware Gaussian Splatting）** 针对上述瓶颈提出了一种**上下文感知的高斯表示范式**，将高斯从独立基元转化为图结构中的关联节点。其核心洞察在于：通过显式建模高斯间的依赖关系，使每个高斯的属性更新不仅依赖自身梯度信号，更融合来自邻域的几何与语义上下文信息。方法层面，CoRoGS 在以下方面与现有工作形成根本差异：

| 维度 | 现有3DGS方法 | CoRoGS |
|------|-------------|--------|
| 高斯表示范式 | 独立基元，无显式依赖建模 | 上下文感知的高斯图，建模高斯间空间与语义依赖 |
| 拓扑构建 | 基于SfM点云随机初始化或简单邻近 | 基于MVS点云的Delaunay三角剖分构建高斯图 |
| 属性优化 | 逐高斯独立梯度下降 | 图神经网络消息传递，融合几何与语义上下文 |
| 场景覆盖 | 固定初始高斯集合 | 渐进式图扩张，填补空洞并修剪冗余 |
| 平滑正则化 | 仅深度/法线损失，忽略语义边界 | 语义加权的上下文平滑损失，保护物体边界 |

在方法谱系中，CoRoGS 处于**3DGS与图神经网络**的交叉点。相较于同样关注几何一致性的 **GaussianPro**（Cheng et al., ICML 2024）和 **DC-Gaussian**（Wang et al., NeurIPS 2024），CoRoGS 的独特贡献在于将高斯优化形式化为图上的上下文推理问题，而非仅添加辅助正则项；相较于引入语义信息的 **SAGS**（Ververas et al., ECCV 2024），CoRoGS 通过跨模态融合机制实现了几何与语义的深度耦合，而非简单的多通道拼接。

### 主要结果

在 KITTI 数据集 0.5m 横向偏移的监督设置下，CoRoGS 达到 **PSNR 24.96 dB / SSIM 0.849 / LPIPS 0.180**。在更具挑战性的非监督大偏差场景（KITTI & Waymo，包括 5m 横向、2m 纵向和 5m 对角线偏移）中，CoRoGS 的 FID 指标相较最强基线 **DC-Gaussian** 平均降低 **21%–33%**。消融实验证实，几何更新模块、语义更新模块、跨模态融合、图扩张和上下文平滑损失各自对最终性能均有显著贡献，其中移除几何更新模块导致 PSNR 下降 1.71 dB，移除图扩张导致 PSNR 下降 0.93 dB。定性可视化（图 1、图 3、图 4）进一步表明，CoRoGS 在大偏差视角下能保持更完整的几何结构和更清晰的语义边界，渲染法线图的质量也显著优于基线方法。

### 局限与开放问题

当前方法仍存在两个主要局限：**对动态对象的处理能力有限**，难以建模包含运动物体的场景；**在大角度旋转场景下几何一致性可能下降**，表明旋转感知的结构约束尚未充分融入。相应的开放问题包括：如何将上下文推理范式扩展到动态高斯场、如何融入旋转感知的结构先验，以及如何优化大规模城市场景中的图构建计算开销。

### 大偏差视图合成：从独立基元到上下文感知表示

新视角合成（Novel View Synthesis, NVS）是三维视觉的核心任务之一，其目标是从一组稀疏的输入视图重建出任意新视角下的场景外观。近年来，**3D Gaussian Splatting (3DGS)**（Kerbl et al., ACM TOG 2023）以其显式点基元表示和高效可微光栅化管线，在渲染速度与质量之间取得了突破性平衡，迅速成为该领域的主导范式。然而，现有3DGS方法存在一个根本性的结构缺陷：**将每个高斯核视为独立的几何基元，缺乏对高斯间空间与语义依赖关系的显式建模**。

这一缺陷在常规视角合成任务中尚可容忍，因为此时训练视图与测试视图之间的视点偏移较小，独立高斯通过梯度下降优化即可获得合理的局部外观。但当面临**大偏差视图合成（Large-Deviation Novel View Synthesis, LD-NVS）**——即测试视角与训练视角之间存在显著的空间偏移时，问题便会急剧恶化。具体表现为两个层面：

1. **几何不一致性**：缺乏邻域约束的独立高斯在未见视角下容易产生位置漂移和形状畸变，导致重建的几何结构出现断裂、空洞或重叠。例如，远处建筑物的墙面可能因高斯间缺乏共面约束而呈现波浪状扭曲。

2. **外观退化**：语义上属于同一物体（如车辆、路面）的高斯之间没有信息共享机制，当视角偏差增大时，各高斯独立推断的颜色和不透明度难以保持全局一致性，产生纹理撕裂和模糊伪影。

### 现有改进路线的局限

针对上述问题，学界已提出多种改进方案，但均未从根本上解决“独立基元”这一范式瓶颈：

- **几何正则化方法**（如 **GaussianPro**, Cheng et al., ICML 2024；**SAGS**, Ververas et al., ECCV 2024）通过引入深度或法线损失来约束高斯的位置和朝向，但这些约束施加于单个高斯层面，无法建模高斯之间的结构依赖关系。

- **语义引导方法**（如 **DC-Gaussian**, Wang et al., NeurIPS 2024）利用语义信息辅助高斯优化，但语义特征仅用于监督信号，并未参与高斯间的信息交互。

- **场景特定方案**（如 **StreetSurf**, Guo et al., arXiv 2023；**GSDF**, Yu et al., NeurIPS 2024；**VEGS**, Hwang et al., ECCV 2024）针对城市场景设计了专门的表示和先验，但缺乏通用的上下文推理机制，泛化能力受限。

- **最新探索**（如 **DeSiRe-GS**, Peng et al., CVPR 2025）开始关注高斯的空间关系，但仍停留在局部启发式层面，未形成系统化的上下文建模框架。

综合来看，**现有方法的共同瓶颈在于：将3DGS表示局限于一组相互独立的高斯基元**，而真实三维场景中的几何结构（如平面、边缘）和语义区域（如道路、建筑）本质上是由高斯间的依赖关系所定义的。当视角发生大偏差时，这种依赖关系对于维持全局结构连贯和外观一致性至关重要。

### 核心动机与研究思路

本文的核心动机在于：**将3DGS从“独立基元集合”重新定义为“上下文感知的图结构表示”**。这一范式转换的关键洞察是：

> 每个高斯不仅由其自身属性（位置、协方差、颜色）所定义，更应通过其空间邻域和语义上下文来理解——正如场景中的一个点，其意义取决于它所在的平面、所属的物体以及它与周围结构的关系。

基于此，CoRoGS提出了一种**上下文感知高斯泼溅（Context-Aware Gaussian Splatting）**框架，其技术路线包含三个核心创新：

1. **图结构化表示**：通过Delaunay三角剖分将高斯点云组织为图结构，显式编码高斯间的空间邻近关系，使每个高斯能够感知其邻域上下文。

2. **双分支消息传递**：设计几何更新分支和语义更新分支，在图神经网络中分别传播几何一致性信息（法线、距离）和语义亲和性信息，再通过跨模态融合机制生成上下文感知的高斯特征。

3. **自适应图扩张**：引入渐进式图扩张策略，在渲染梯度驱动下动态地向未覆盖区域添加高斯节点，同时修剪冗余节点，确保场景拓扑的完备性。

通过这一上下文推理机制，CoRoGS使得每个高斯在大偏差视角下仍能保持与邻域的结构一致性，从而从根本上缓解几何不一致和外观退化问题。

## 核心方法与创新机理

CoRoGS 的核心创新在于将 3D 高斯泼溅（3DGS）从“独立基元”范式转向“上下文感知的图表示”范式，通过显式建模高斯间的空间与语义依赖关系，从根本上解决了大视角偏差下几何不一致与外观退化这一瓶颈。

### 范式跃迁：从独立基元到上下文感知图表示

传统 3DGS 方法（如 **3DGS** (Kerbl et al., ACM TOG 2023) 及其后续变体）将每个高斯视为独立的可微基元，其属性仅通过光度损失驱动的梯度下降独立优化。这种独立性假设导致高斯间缺乏协调机制，在大视角偏差下容易出现结构撕裂、语义混淆和伪影。CoRoGS 引入了一个统一的上下文推理公式：

$$\hat{\phi}_i = \Phi(\phi_i, \mathcal{C}_i), \qquad \mathcal{C}_i = \Psi(\{\phi_j \mid j \in \mathcal{N}(i)\})$$

每个高斯 $\hat{\phi}_i$ 的更新不再仅依赖自身属性 $\phi_i$，而是融合了从其邻域 $\mathcal{N}(i)$ 聚合的上下文信息 $\mathcal{C}_i$。这一范式转变是整个方法体系的基石，后续所有模块均围绕如何构建图拓扑、如何实现 $\Psi$ 和 $\Phi$ 函数展开。

### 关键创新点拆解

以下五个 changed slots 构成了 CoRoGS 相对于 baseline 方法的核心差异：

**1. 高斯拓扑构建：从随机初始化到 Delaunay 三角剖分**

基线方法通常基于 SfM 点云随机初始化高斯位置，或仅依赖简单的空间邻近关系。CoRoGS 转而利用 MVS 重建点云进行 Delaunay 三角剖分构建高斯图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$，将高斯作为节点，剖分边作为空间连接。这一拓扑选择具有明确的几何意义：Delaunay 剖分天然避免狭长三角形，保证连接的局部性与均匀性，为后续消息传递提供高质量的结构骨架。

**2. 高斯属性优化：从独立梯度下降到图神经网络消息传递**

这是方法体系中最关键的改变。CoRoGS 用高斯图神经网络（Gaussian GNN）替代了传统的逐高斯梯度下降优化，具体包含三个子模块：
- **属性嵌入**：通过傅里叶位置编码和 MLP 将节点/边属性映射到高维空间，其中边属性显式编码法线余弦相似度和欧氏距离 $\mathbf{e}_{ij}^g = [\cos(\mathbf{n}_i, \mathbf{n}_j), \lVert \mathbf{p}_i - \mathbf{p}_j \rVert_2]$。
- **几何与语义双分支更新**：分别沿几何边和语义边进行消息传递，通过注意力机制聚合邻域信息到节点，确保几何结构约束和语义一致性被分别捕获。
- **跨模态融合**：通过跨模态注意力实现几何与语义特征的相互引导，再以自适应门控系数 $\eta_i = \sigma(\mathbf{W}_\eta [\tilde{\mathbf{f}}_i^g \lVert \tilde{\mathbf{f}}_i^s])$ 融合为统一表示。

消融实验表明，移除几何更新模块导致 PSNR 从 24.96 降至 23.25，移除语义更新模块降至 23.69，移除跨模态融合（退化为简单拼接）则降至 23.93，三者均造成显著的视觉伪影。

**3. 场景覆盖策略：从固定集合到渐进式图扩张**

基线方法在整个优化过程中保持初始高斯集合不变，难以填补未被充分覆盖的场景区域。CoRoGS 引入渐进式图扩张策略，基于梯度驱动检测未覆盖区域，自适应添加新高斯节点，同时修剪冗余节点。这一拓扑约束下的动态增长机制有效缓解了因初始拓扑不完整导致的渲染空洞。消融显示移除图扩张使 PSNR 下降 0.93 dB。

**4. 平滑正则化：从无视语义边界到上下文平滑损失**

现有方法常用深度/法线平滑损失，但对所有区域施加均匀约束，导致物体边界处的几何细节被模糊。CoRoGS 提出上下文平滑损失 $\mathcal{L}_{\mathrm{context}}$，在渲染法线图上以语义相似性作为权重对邻域像素施加平滑约束：

$$\mathcal{L}_{\mathrm{context}} = \sum_{h,w} w_{(h,w),(h+1,w)} \|\mathcal{N}_{h+1,w} - \mathcal{N}_{h,w}\|_1 + w_{(h,w),(h,w+1)} \|\mathcal{N}_{h,w+1} - \mathcal{N}_{h,w}\|_1$$

语义权重使得平滑在物体内部被强制，而在语义边界处被抑制，从而保护了边缘结构。消融证实该损失对渲染质量有显著贡献。

**5. 语义属性注入：从纯几何到几何-语义联合编码**

CoRoGS 通过 PointNet++ 编码器从位置和法线提取语义属性 $\mathbf{z}_i = f_{\boldsymbol\Theta}(\mathbf{p}_i, \mathbf{n}_i)$，使每个高斯节点同时携带几何与语义信息。这一设计使得后续的消息传递能够感知语义边界，避免跨类别高斯的不当融合，是实现语义一致性渲染的前提。

### 创新总结

CoRoGS 的创新并非孤立的模块堆叠，而是围绕“上下文感知高斯图”这一核心洞察的系统性重构：用图拓扑替代独立基元，用消息传递替代独立优化，用语义引导的平滑和扩张替代无差别的正则化与覆盖策略。这五个 changed slots 相互协同，共同实现了在大视角偏差下全局结构连贯、语义一致的高保真渲染。

CoRoGS 的整体 pipeline 围绕“上下文感知的高斯泼溅”这一核心范式展开，将传统 3DGS 中相互独立的高斯基元转化为一个显式建模空间与语义依赖关系的**3D 高斯图结构**，并通过图神经网络的消息传递机制实现一致性高斯更新。整个框架由五个关键模块串联构成，形成从场景初始化到最终渲染的闭环。

**输入**为多视图图像及对应的相机位姿，首先通过 MVS（多视角立体）重建获得稀疏点云，作为高斯的初始位置和法线估计。随后进入核心流水线：

1. **3D Gaussian Graph Construction（3D 高斯图构建）**：基于 MVS 点云执行 Delaunay 三角剖分，以剖分顶点作为高斯节点、边作为空间连接关系，构建初始高斯图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$。每个节点 $v_i$ 携带位置 $\mathbf{p}_i$、法线 $\mathbf{n}_i$ 和通过 PointNet++ 编码器 $f_{\boldsymbol\Theta}$ 提取的语义属性 $\mathbf{z}_i$；每条边 $\mathbf{e}_{ij}^g$ 编码法线余弦相似度和欧氏距离。这一拓扑构建使高斯之间建立了显式的几何邻接关系，为后续上下文推理提供结构基础。

2. **Gaussian Graph Neural Network（高斯图神经网络）**：该模块实现上下文感知的高斯更新函数 $\Phi$，由三个子模块串联组成：
   - **Attributes Embedding（属性嵌入）**：通过傅里叶位置编码和 MLP 将节点几何/语义属性映射到高维嵌入空间，得到几何嵌入 $\mathbf{g}_i^v$ 和语义嵌入 $\mathbf{s}_i^v$。
   - **Geometric and Semantic Update（几何与语义更新）**：在几何和语义两个独立分支中，先通过 MLP 更新边特征，再利用注意力机制将边特征聚合到节点，生成节点级几何特征 $\mathbf{f}_i^g$ 和语义特征 $\mathbf{f}_i^s$。
   - **Cross-Modal Fusion（跨模态融合）**：通过跨模态注意力实现几何与语义特征的相互引导，再经由可学习的门控系数 $\eta_i$ 自适应融合，生成统一的节点表示 $\mathbf{z}_i^o$。

3. **Context-Aware Gaussian Decoder（上下文感知高斯解码器）**：将融合后的节点特征与视角方向共同输入解码器，预测每个高斯的尺度、旋转、不透明度和颜色参数。此时的高斯参数已包含邻域上下文信息，而非独立优化。

4. **损失函数与渲染**：总损失联合了光度损失 $\mathcal{L}_1$、结构损失 $\mathcal{L}_{\mathrm{D\text{-}SSIM}}$、法线损失 $\mathcal{L}_{\mathrm{normal}}$、语义损失 $\mathcal{L}_{\mathrm{semantic}}$ 以及核心的**上下文平滑损失** $\mathcal{L}_{\mathrm{context}}$。$\mathcal{L}_{\mathrm{context}}$ 在渲染法线图上施加语义加权的邻域平滑约束——利用语义相似性作为权重 $w_{ij}$，在均质区域强制局部几何一致性，同时在语义边界处允许不连续，从而保护物体边缘。

5. **Graph Expansion（图扩张）**：采用梯度驱动和拓扑约束的渐进式策略，在渲染梯度大的未覆盖区域动态添加新高斯节点，同时修剪冗余节点。这一机制使高斯图能够自适应填补场景空洞，保持几何连贯和语义连续。

**输出**为经过上下文推理优化的高斯场，可直接通过可微光栅化渲染任意新视角的图像、法线图和语义图。整体框架的闭环设计使得从图构建、消息传递、参数解码到损失监督和拓扑扩张形成了端到端的优化循环，如图 2 所示。

![[assets/figures/papers/paper_list_l2248_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_CoRoGS_Contextual_G/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our CoRoGS. (a) 3D Gaussian Graph Construction module builds a graph representation of Gaussians in Sec. 3.3. (b) Gaussian Graph Neural Network in Sec. 3.4 refines each Gaussian through three submodules: 1) attributes embedding, 2) geometric and semantic update, 3) cross-modal fusion. (c) Context-aware Gaussian decoder in Sec. 3.5. (d) Contextual smoothness loss in Sec. 3.6. (e) Graph Expansion module in Sec. 3.7 iteratively refines the graph by adding nodes in uncovered regions while pruning redundant ones to alleviate artifacts caused by incomplete topology*

CoRoGS 的核心在于将高斯表示从独立基元转化为上下文感知的图结构，并通过图神经网络实现高斯间的消息传递与协同更新。本节聚焦于支撑这一范式的关键模块与核心公式。

### 上下文高斯更新范式

传统3DGS将每个高斯视为独立优化的基元，忽略了高斯之间在空间和语义上的依赖关系。CoRoGS引入上下文推理机制，将每个高斯的更新定义为其自身属性与邻域上下文信息的函数：

$$\hat{\phi}_i = \Phi(\phi_i, \mathcal{C}_i), \qquad \mathcal{C}_i = \Psi(\{\phi_j \mid j \in \mathcal{N}(i)\})$$

其中 $\phi_i$ 表示高斯 $i$ 的原始属性（位置、法线、语义特征等），$\mathcal{C}_i$ 为从邻域 $\mathcal{N}(i)$ 聚合的上下文信息，$\Phi$ 为上下文感知的更新函数，$\hat{\phi}_i$ 为更新后的高斯属性。这一范式将独立优化转化为图结构上的协同推理，为后续模块提供了统一的数学框架。

### 3D高斯图构建

为实例化上述范式，CoRoGS首先从MVS（多视图立体）重建的点云出发，利用Delaunay三角剖分构建3D高斯图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$。每个节点 $v_i \in \mathcal{V}$ 携带三类属性：位置 $\mathbf{p}_i$、法线 $\mathbf{n}_i$ 和语义特征 $\mathbf{z}_i$，其中语义特征通过预训练的PointNet++编码器从几何输入中提取：

$$\mathbf{z}_i = f_{\boldsymbol{\Theta}}(\mathbf{p}_i, \mathbf{n}_i), \qquad v_i = \{\mathbf{p}_i, \mathbf{n}_i, \mathbf{z}_i\}$$

边属性则编码相邻高斯之间的几何关系，定义为法线余弦相似度与欧氏距离的拼接：

$$\mathbf{e}_{ij}^g = [\cos(\mathbf{n}_i, \mathbf{n}_j), \ \lVert \mathbf{p}_i - \mathbf{p}_j \rVert_2] \in \mathbb{R}^2$$

Delaunay三角剖分的选择具有明确的几何动机：相较于简单的K近邻连接，它能够生成无冗余、覆盖均匀的图拓扑，且天然保持局部流形结构，为后续消息传递提供高质量的邻域定义。

### 属性嵌入

在消息传递之前，节点和边的属性需映射到高维嵌入空间。节点属性嵌入分为几何与语义两个分支，通过傅里叶位置编码和MLP实现：

$$\mathbf{g}_i^v = \mathcal{M}_v^g([\psi(\mathbf{p}_i), \psi(\mathbf{n}_i)]), \quad \mathbf{s}_i^v = \mathcal{M}_v^s(\mathbf{z}_i)$$

其中 $\psi(\cdot)$ 为傅里叶位置编码，$\mathcal{M}_v^g$ 和 $\mathcal{M}_v^s$ 分别为几何和语义嵌入MLP。边属性同样经过MLP映射：$\mathbf{g}_{ij}^e = \mathcal{M}_e^g(\mathbf{e}_{ij}^g)$，$\mathbf{s}_{ij}^e = \mathcal{M}_e^s(\mathbf{e}_{ij}^g)$。双分支设计允许几何和语义信息在后续更新中保持独立的表示空间，仅在融合阶段进行交互。

### 几何与语义更新

消息传递的核心是边特征更新与节点特征聚合。边特征首先通过MLP和残差连接进行更新（以几何分支为例：$\tilde{\mathbf{g}}_{ij}^e = \mathcal{U}_e^g([\mathbf{g}_i^v, \mathbf{g}_j^v, \mathbf{g}_{ij}^e])$），随后通过注意力机制聚合到节点：

$$\mathbf{f}_i^g = \sum_{j \in \mathcal{N}(i)} \mathrm{Attn}(\tilde{\mathbf{g}}_{ij}^e, \mathbf{g}_i^v)$$

$$\mathbf{f}_i^s = \sum_{j \in \mathcal{N}(i)} \mathrm{Attn}(\tilde{\mathbf{s}}_{ij}^e, \mathbf{s}_i^v)$$

注意力机制以节点当前嵌入为查询，更新后的边特征为键值，使节点能够自适应地关注不同邻居的贡献。几何与语义分支独立执行上述过程，分别捕获空间结构依赖和语义关联。

### 跨模态融合

几何与语义特征携带互补信息，简单拼接无法充分利用二者的交互。CoRoGS采用跨模态注意力机制实现双向特征精炼：

$$\tilde{\mathbf{f}}_i^g = \sum_{k=1}^N \alpha_{ik}^{g \to s} \mathbf{q}_k^s, \quad \tilde{\mathbf{f}}_i^s = \sum_{k=1}^N \alpha_{ik}^{s \to g} \mathbf{q}_k^g$$

其中 $\alpha_{ik}^{g \to s}$ 表示几何特征对语义特征的注意力权重（反之亦然），$\mathbf{q}_k^g$、$\mathbf{q}_k^s$ 为线性投影后的查询向量。精炼后的特征通过自适应门控进行融合：

$$\mathbf{z}_i^o = \eta_i \tilde{\mathbf{f}}_i^g + (1 - \eta_i) \tilde{\mathbf{f}}_i^s, \quad \eta_i = \sigma(\mathbf{W}_\eta [\tilde{\mathbf{f}}_i^g \lVert \tilde{\mathbf{f}}_i^s])$$

门控系数 $\eta_i$ 由几何和语义特征的拼接经线性投影和sigmoid激活得到，使模型能够根据每个高斯所处的局部上下文动态调整几何与语义信息的融合比例。

### 上下文平滑损失

为强制局部几何一致性并保护语义边界，CoRoGS在渲染法线图上施加语义加权的上下文平滑损失。该损失惩罚相邻像素间法线的不连续性，但以语义相似性为权重，避免在物体边界处过度平滑：

$$\mathcal{L}_{\mathrm{context}} = \sum_{h=1}^{H-1}\sum_{w=1}^{W-1} \left[ w_{(h,w),(h+1,w)} \|\mathcal{N}_{h+1,w} - \mathcal{N}_{h,w}\|_1 + w_{(h,w),(h,w+1)} \|\mathcal{N}_{h,w+1} - \mathcal{N}_{h,w}\|_1 \right]$$

其中 $\mathcal{N}$ 为渲染法线图，$w_{ij}$ 为基于渲染语义图计算的像素间相似性权重。总训练损失联合了光度损失、结构相似性损失、法线损失、语义损失和上下文平滑损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_1 + \lambda_D \mathcal{L}_{\mathrm{D-SSIM}} + \lambda_N \mathcal{L}_{\mathrm{normal}} + \lambda_S \mathcal{L}_{\mathrm{semantic}} + \lambda_C \mathcal{L}_{\mathrm{context}}$$

### 渐进式图扩张

初始高斯图受限于MVS点云的覆盖范围，可能遗漏场景中的细节区域。CoRoGS引入梯度驱动、拓扑约束的渐进式图扩张策略：在训练过程中，根据渲染梯度识别覆盖不足的区域，在高梯度位置添加新高斯节点，并通过Delaunay边连接融入现有图结构；同时修剪对渲染贡献可忽略的冗余高斯。这一策略使高斯图能够自适应地填补结构空洞，在保持几何连贯性和语义连续性的同时提升场景覆盖。

![[assets/figures/papers/paper_list_l2248_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_CoRoGS_Contextual_G/figures/010_Figure_6.jpg]]
*Figure 6: Visualization of initial and optimized Gaussian graph*

## 实验与关键发现

### 主实验结果

CoRoGS 在两种实验设置下均展现出显著优势：监督小偏差设置和非监督大偏差设置。在 KITTI 数据集上采用 0.5m 横向右移相机的监督小偏差配置下，CoRoGS 在所有评估指标上均取得最优性能，PSNR 达到 24.96，SSIM 达到 0.849，LPIPS 降至 0.180，CD 指标为 1.32（Table 1）。CD 指标的领先表明 CoRoGS 不仅渲染质量优越，其底层几何重建也更为精确。

在更具挑战性的非监督大偏差设置下（Table 2），实验覆盖 KITTI 和 Waymo Open 两个数据集，评估 Left-5m、Up-2m 和 Diagonal-5m 三种大偏差轨迹。以 DC-Gaussian（Wang et al., NeurIPS 2024）为强基线，CoRoGS 在 FID 指标上分别实现 32.72%、28.38% 和 21.04% 的相对改善。这表明上下文感知的高斯表示能够有效缓解大视角偏差下的几何不一致和外观退化问题，而独立高斯基元方法在此类场景中难以维持全局结构连贯性。

![[assets/figures/papers/paper_list_l2248_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_CoRoGS_Contextual_G/figures/006_Table_2.jpg]]
*Table 2: Quantitative results under unsupervised large-deviation settings, averaged across the KITTI and Waymo Open datasets*

定性结果（Figure 3, Figure 4）进一步印证了定量结论。在 KITTI 和 Waymo 数据集的大偏差视图下，CoRoGS 渲染的法线图更加平滑且保持清晰的物体边界，而基线方法则出现明显的几何断裂和语义混淆。放大区域显示，CoRoGS 的高斯分布更加结构化，能够更好地覆盖场景几何。

![[assets/figures/papers/paper_list_l2248_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_CoRoGS_Contextual_G/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of rendered images and normals on the Waymo Open dataset under typical large-deviation views. Our method achieves higher visual quality than baseline approaches, consistent with the quantitative results in Tab. 2*

![[assets/figures/papers/paper_list_l2248_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_CoRoGS_Contextual_G/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons on the KITTI dataset under differnt view deviations. Left part setting corresponds to Tab. 1, while the right corresponds to Tab. 2. Zoomed-in image patches and the associated normals demonstrate the superior rendering quality of our method compared to competing baselines*

### 消融研究

为验证各模块的贡献，论文在 KITTI 数据集上进行了系统的消融实验（Table 3, Figure 5）。完整模型在 PSNR/SSIM/LPIPS/FID 上达到 24.96/0.8492/0.1805/68.25，移除任一核心模块均导致性能显著下降：

![[assets/figures/papers/paper_list_l2248_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_CoRoGS_Contextual_G/figures/008_Table_3.jpg]]
*Table 3: Ablation studies on the KITTI [5] dataset*

- **几何更新模块**：移除后 PSNR 降至 23.25（下降 1.71 dB），渲染结果出现明显的几何伪影。该模块通过边到节点的注意力聚合机制传播空间结构信息，是维持大偏差下几何一致性的关键。
- **语义更新模块**：移除后 PSNR 降至 23.69，不同语义区域出现错误融合。语义分支的消息传递使得高斯能够感知物体边界，避免跨语义区域的属性污染。
- **跨模态融合**：将自适应门控融合替换为简单拼接后，PSNR 下降 1.03 dB 至 23.93。这表明几何与语义特征的协同推理对上下文感知的高斯更新至关重要，简单拼接无法有效建模模态间的互补关系。
- **图扩张模块**：移除后 PSNR 下降 0.93 dB，所有指标一致退化。渐进式图扩张策略通过梯度驱动和拓扑约束在未覆盖区域增加高斯并修剪冗余，是填补场景空洞、缓解不完整拓扑伪影的必要机制。
- **上下文平滑损失**：移除该损失后渲染质量明显下降。该损失通过在渲染法线图上施加语义加权的邻域平滑，在强制局部几何一致性的同时保护物体边界，是提升法线图质量和最终渲染保真度的重要因素。

### 失败模式与局限性

尽管 CoRoGS 在大偏差视图合成上取得了显著进展，论文明确指出以下局限性：

1. **动态对象处理能力有限**：当前方法假设场景为静态，难以建模运动物体。在包含动态对象的场景中，上下文推理可能因运动不一致而产生伪影。
2. **大角度旋转下的几何退化**：在大角度旋转场景下，几何一致性仍可能下降。这暗示当前的图结构约束和消息传递机制对旋转变化的感知能力不足，需要进一步融入旋转感知的结构约束。
3. **大规模场景的计算开销**：Delaunay 三角剖分和图神经网络的消息传递在超大规模城市场景中可能成为计算瓶颈，图构建和推理的效率优化是实用化部署的关键问题。

### 关键图表结论

- **Table 1**：在监督小偏差设置下，CoRoGS 在 PSNR/SSIM/LPIPS/CD 四项指标上全面领先，验证了上下文感知高斯表示在标准场景下的有效性。
- **Table 2**：在非监督大偏差设置下，CoRoGS 相对 DC-Gaussian 的 FID 改善幅度随偏差增大而增加（Left-5m: -32.72%，Diagonal-5m: -21.04%），说明上下文建模对大偏差场景的鲁棒性增益尤为突出。
- **Table 3 & Figure 5**：几何更新模块和跨模态融合对性能贡献最大，移除后 PSNR 分别下降 1.71 dB 和 1.03 dB；图扩张和上下文平滑损失则对场景覆盖和边界保持至关重要。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

大偏差视图合成（Large-Deviation Novel View Synthesis, LD-NVS）的核心挑战在于：当测试视角与训练视角之间存在显著空间偏移时，3D场景表示需要具备全局几何一致性和语义连续性。现有基于3D Gaussian Splatting的方法——包括原始**3DGS**（Kerbl et al., ACM TOG 2023）及其后续改进——普遍将高斯球视为**独立基元**，每个高斯的属性（位置、协方差、颜色、不透明度）通过独立的梯度下降进行优化，缺乏对高斯间空间与语义依赖关系的显式建模。这种“孤立假设”在大视角偏差下会导致两类系统性问题：

1. **几何不一致**：独立优化的高斯在偏离训练视角时无法协同保持全局几何结构，表现为渲染法线断裂、深度不连续和表面空洞。
2. **外观退化**：语义边界处的颜色和纹理出现模糊、混叠或错误融合，因为缺乏跨高斯的语义一致性约束。

现有改进方法尝试从不同角度缓解这一问题，但均未从根本上改变高斯的独立基元范式：

- **GaussianPro**（Cheng et al., ICML 2024）引入几何先验引导高斯生长，但先验本身是全局静态的，无法适应局部上下文变化。
- **SAGS**（Ververas et al., ECCV 2024）和**DC-Gaussian**（Wang et al., NeurIPS 2024）通过深度/法线正则化增强几何约束，但正则化项作用于单个高斯层面，缺乏对邻域关系的结构化建模。
- **StreetSurf**（Guo et al., arXiv 2023）和**GSDF**（Yu et al., NeurIPS 2024）分别利用表面表示和符号距离函数，但在大偏差下仍受限于隐式表示的泛化边界。
- **DeSiRe-GS**（Peng et al., CVPR 2025）和**VEGS**（Hwang et al., ECCV 2024）探索了视图自适应策略，但未建立高斯间的显式依赖图。

CoRoGS的核心洞察在于：**将高斯表示从独立基元转化为上下文感知的图结构**，通过显式建模高斯间的几何与语义依赖关系，使每个高斯的更新不仅依赖于自身观测，还融合其邻域的上下文信息。

### 2. 方法谱系中的位置

从方法学角度看，CoRoGS处于三个研究方向的交叉点：

**（1）3D Gaussian Splatting的演化谱系**

CoRoGS直接继承3DGS的可微渲染框架，但在表示层面进行了范式转换。传统3DGS及其变体可视为“独立基元优化”范式的不同实例，而CoRoGS开创了“上下文感知基元优化”的新范式。这一转变的关键技术载体是**3D高斯图**——通过Delaunay三角剖分从MVS点云构建图拓扑，将无结构的高斯集合转化为具有显式空间连接关系的图结构。

**（2）图神经网络在3D视觉中的应用**

CoRoGS将图神经网络（GNN）引入高斯属性优化，这与点云处理中的GNN方法（如PointNet++的层级特征学习）形成呼应，但有本质区别：传统点云GNN处理的是静态点特征，而CoRoGS的GNN需要在可微渲染的梯度反馈下动态更新高斯属性。具体而言，CoRoGS的GNN包含三个关键创新：

- **双分支消息传递**：分别沿几何边（编码法线相似度和欧氏距离）和语义边进行消息传递，避免单一模态的信息瓶颈。
- **跨模态融合**：通过门控注意力机制自适应融合几何与语义特征，使模型能够根据不同区域的特点动态调整两种信息的权重。
- **视角条件解码**：融合后的节点特征与视角方向一起解码为高斯参数，使上下文感知能力与视角适应性相结合。

**（3）场景覆盖与自适应拓扑**

CoRoGS的渐进式图扩张策略与NeRF中的自适应采样和3DGS中的克隆/分裂操作有相似动机，但实现机制不同：图扩张基于梯度驱动的节点添加和拓扑约束的冗余修剪，确保新增高斯不仅填补几何空洞，还保持与现有图结构的语义连续性。这使得CoRoGS在非监督大偏差设置下（左移5m、上移2m、对角移5m）相比**DC-Gaussian**在FID指标上分别改善32.72%、28.38%和21.04%。

### 3. 适用边界与局限

尽管CoRoGS在LD-NVS任务上展现出显著优势，其适用边界和局限值得关注：

**（1）动态场景的建模能力有限**

当前方法假设场景是静态的，高斯图结构在训练过程中虽然可以扩张和修剪，但无法处理动态对象的运动。对于包含移动车辆、行人等动态元素的城市场景，CoRoGS可能将运动物体误认为几何不一致，导致图结构错误调整。将上下文推理扩展到动态高斯场是未来的重要方向。

**（2）大角度旋转下的几何一致性退化**

实验主要验证了平移偏差下的鲁棒性（横向、纵向、对角偏移），但在大角度旋转场景下，Delaunay三角剖分构建的初始图拓扑可能无法正确反映旋转后的空间邻近关系，导致消息传递路径失效。融入旋转感知的结构约束（如基于相机位姿的图重连机制）是提升大旋转鲁棒性的可能路径。

**（3）计算开销与可扩展性**

图神经网络的引入增加了训练和推理的计算开销，尤其是在大规模城市场景（如Waymo Open Dataset的完整序列）中，高斯节点数可达数十万量级，图构建和消息传递的复杂度随节点数超线性增长。如何在保持上下文推理能力的同时降低图计算开销，是实际部署中需要解决的问题。

### 4. 开放问题与后续方向

基于CoRoGS的方法框架和当前局限，以下开放问题值得关注：

1. **动态高斯场中的上下文推理**：如何将图结构的消息传递机制与时序信息结合，使高斯图能够同时建模空间依赖和时间演化？可能的路径包括引入时空图神经网络或与4D Gaussian Splatting框架融合。

2. **旋转鲁棒的图构建策略**：能否设计一种基于相机位姿自适应的图拓扑更新机制，使高斯图在视角旋转后自动重连以保持正确的空间邻近关系？这可能需要将旋转信息显式编码到边属性中。

3. **大规模场景的高效图计算**：能否通过层次化图结构（如粗粒度场景图与细粒度局部图的嵌套）或稀疏注意力机制降低消息传递的计算复杂度？这关系到方法在自动驾驶等实际应用中的可行性。

4. **跨场景的上下文先验迁移**：CoRoGS的语义属性编码器（PointNet++）在特定数据集上训练，能否通过预训练或元学习使上下文推理能力在不同场景间迁移，减少对新场景的适配成本？

## 原文 PDF

![[paperPDFs/CVPR_2026/CoRoGS_Contextual_Gaussian_Splatting_for_Robust_Large_Deviation_View_Synthesis.pdf]]

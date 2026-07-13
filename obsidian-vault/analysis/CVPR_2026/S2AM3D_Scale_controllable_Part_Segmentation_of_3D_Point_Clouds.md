---
title: "S$^2$AM3D: Scale-controllable Part Segmentation of 3D Point Clouds"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/S_2_AM3D_Scale_controllable_Part_Segmentation_of_3D_Point_Clouds.pdf
project_link: "https://sumuru789.github.io/S2AM3D-website/"
code_link: null
aliases:
- S2ASCPS3PC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过3D对比监督增强点特征全局一致性，并利用连续尺度信号引导解码器实现粒度可控的部件分割。
primary_logic: 融合2D视觉基础先验与3D对比学习，在保持多视角一致性的同时，结合尺度感知机制，实现了从精细到粗糙的连续可控3D零件分割。
claims:
- 在PartObjaverse-Tiny和PartNet-E上，S2AM3D在交互式分割和全分割任务中均达到了最优性能，且仅需更少的训练数据即可达到与大规模训练模型相当的性能。
- 消融研究显示，移除3D对比监督导致mIoU大幅下降（PartObjaverse-Tiny上从61.19降至53.94），证明了3D几何一致性对全局特征的关键作用。
- 引入尺度提示（+scale）在交互式分割上带来14.72%和14.99%的性能提升，验证了连续尺度调制对分割粒度的有效控制。
- PartObjaverse-Tiny 上 IoU (interactive) = 46.47 / 61.19 (+scale)
---

# S$^2$AM3D: Scale-controllable Part Segmentation of 3D Point Clouds

> [!tip] 核心洞察
> 融合2D视觉基础先验与3D对比学习，在保持多视角一致性的同时，结合尺度感知机制，实现了从精细到粗糙的连续可控3D零件分割。

| 字段 | 内容 |
|------|------|
| 中文题名 | S²AM3D：尺度可控的三维点云部件分割 |
| 英文题名 | S$^2$AM3D: Scale-controllable Part Segmentation of 3D Point Clouds |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Su_S2AM3D_Scale-controllable_Part_Segmentation_of_3D_Point_Clouds_CVPR_2026_paper.html) · [Project](https://sumuru789.github.io/S2AM3D-website/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | S2AM3D |
| Dataset | PartObjaverse-Tiny, PartNet-E |

> [!tip] 效果简介
> - PartObjaverse-Tiny 上，IoU (interactive) 46.47 / 61.19 (+scale) vs 优于所有比较方法（具体值见表1） (+14.72 (scale gain))；mIoU (full segmentation) 63.29 vs 优于PartField、SAMPart3D等方法 (N/A)。
> - PartNet-E 上，IoU (interactive) 62.52 / 77.51 (+scale) vs 优于所有比较方法 (+14.99)；mIoU (full segmentation) 77.98 vs 优于PartField、SAMPart3D等方法 (N/A)。

## 概要

三维点云的部件分割是细粒度三维理解的核心任务，但现有方法面临两个关键瓶颈：（1）基于2D视觉基础模型（如SAM）的蒸馏方法因遮挡、细薄结构及复杂拓扑导致多视角分割结果不一致；（2）大规模高质量3D部件标注数据稀缺，限制了模型的泛化能力。S²AM3D通过**融合2D视觉先验与3D对比学习**解决一致性问题，并引入**连续尺度信号**实现从精细到粗糙的可控部件分割，仅需更少的训练数据即可达到与大规模训练模型相当的性能。

在PartObjaverse-Tiny和PartNet-E两个基准上，S²AM3D在交互式分割和全分割任务中均达到最优。具体而言，引入尺度提示（+scale）后，交互式分割IoU在PartObjaverse-Tiny上从46.47提升至61.19（+14.72），在PartNet-E上从62.52提升至77.51（+14.99）；全分割mIoU分别为63.29和77.98，显著优于PartField、SAMPart3D等同类方法。消融研究证实，移除3D对比监督导致mIoU大幅下降（PartObjaverse-Tiny上从61.19降至53.94），验证了3D几何一致性对全局特征的关键作用。

三维点云部件分割旨在将点云分解为具有独立语义或几何意义的组成部分，是三维视觉理解中的基础任务，广泛支撑机器人操作、三维建模与编辑、增强现实等下游应用。近年来，随着视觉基础模型（如SAM）的兴起，基于二维先验的三维分割方法取得了显著进展：这类方法通过多视角渲染将三维形状投影到二维平面，利用预训练的二维分割模型提取部件级信息，再将其反投影至三维空间。然而，这一范式存在一个根本性瓶颈：**二维分割先验因遮挡、细薄结构及复杂拓扑会导致多视角分割结果不一致**——同一三维部件在不同视角下可能被分割为不同片段，或与相邻部件发生混淆，最终导致三维空间的部件边界模糊、拓扑不完整。

现有方法在面对上述问题时采取了不同的应对策略。**PartSLIP**（Liu et al., CVPR 2023）及其增强版**PartSLIP++**（Zhou et al., arXiv 2023）通过多视角特征聚合提升二维特征的稳定性，但仍缺乏对三维几何一致性的显式建模。**SAMPart3D**（Yang et al., arXiv 2024）直接利用SAM进行部件分割，并依赖后处理聚类来控制分割粒度，但聚类策略无法灵活适配不同粒度的语义需求。**PartField**（Liu et al., arXiv 2025）作为最新的代表性工作，同样基于二维分割先验，通过后处理聚类确定粒度，在复杂场景下仍面临多视角不一致的挑战。另一方面，原生三维分割方法如**P3-SAM**（Ma et al., arXiv 2025）和**Point-SAM**（Zhou et al., arXiv 2024）虽然直接在三维空间操作，但受限于大规模高质量三维部件标注数据的稀缺，其泛化能力受到严重制约。

上述分析揭示出当前三维部件分割领域的两个核心缺口：其一，**缺乏将二维语义先验与三维几何一致性有效融合的机制**，导致多视角分割结果难以在三维空间形成全局一致的部件表达；其二，**缺乏显式且连续的粒度控制手段**，现有方法要么产生固定粒度的分割结果，要么依赖离散的后处理聚类，无法支持从精细零件到粗糙部件的平滑过渡。这两个缺口的共同根源在于：二维先验提供了丰富的语义信息但缺乏三维几何约束，而三维监督能提供几何一致性但高质量标注数据极为稀缺。

针对上述问题，本文提出**S²AM3D**（Scale-controllable Part Segmentation of 3D Point Clouds），旨在通过融合二维视觉基础先验与三维对比学习，在保持多视角一致性的同时，结合尺度感知机制，实现从精细到粗糙的连续可控三维零件分割。

## 核心方法与创新机理

S²AM3D 的核心创新在于通过两个关键机制解决了现有 2D 先验驱动 3D 部件分割方法的根本瓶颈——多视角分割不一致与粒度不可控。

### 瓶颈诊断

现有方法（如 **PartField** (Liu et al., arXiv 2025)、**SAMPart3D** (Yang et al., arXiv 2024)）将 2D 视觉基础模型的多视角分割结果蒸馏到 3D 表示中，但面临两个致命缺陷：

1. **多视角不一致**：遮挡、细薄结构及复杂拓扑导致不同视角的 2D 分割结果相互矛盾，直接蒸馏会产生混乱的 3D 特征。
2. **粒度不可控**：分割粒度依赖后处理聚类或隐式确定，无法根据需求灵活调整从精细零件到粗糙部件的输出。

### 关键创新点

针对上述瓶颈，S²AM3D 引入两个 changed slots：

| 创新维度 | Baseline 做法 | S²AM3D 做法 |
|---------|-------------|-----------|
| **编码器监督** | 仅多视角 2D 蒸馏，无 3D 约束 | 在 2D 蒸馏基础上增加**实例内 3D 对比监督**，增强全局点特征一致性 |
| **粒度控制** | 后处理聚类或缺乏显式控制 | 引入**显式连续尺度信号** $s \in [0,1]$，经可学习正弦嵌入与 FiLM 进行跨层调制 |

### 创新一：点一致性部件编码器

编码器通过 Tri-plane 投影将多视角 2D 特征聚合为逐点特征：

$$\mathbf{F} = \Big[ \mathbf{T}_{xy}(x_n, y_n) + \mathbf{T}_{yz}(y_n, z_n) + \mathbf{T}_{zx}(z_n, x_n) \Big]_{n=1}^{N}$$

在此基础上，引入**实例内对比损失**，对同一 3D 实例内属于同一部件的点对施加吸引力、不同部件的点对施加排斥力：

$$\mathcal{L}_{\mathrm{contr}} = \frac{1}{|\hat{P}|} \sum_{i \in \hat{P}} -\log \frac{\sum_{j \in \hat{P}(i)} e^{s_{ij}}}{\sum_{j \in \hat{P} \setminus \{i\}} e^{s_{ij}}}$$

这一 3D 原生监督信号迫使编码器学习几何一致的全局特征，从根本上缓解了多视角蒸馏的不一致问题。消融实验（Table 3）证实：移除 3D 监督后，PartObjaverse-Tiny 上 mIoU 从 61.19 骤降至 53.94，PartNet-E 上从 77.51 降至 64.11，降幅分别达 7.25 和 13.40 个百分点。

### 创新二：尺度感知提示解码器

解码器包含两个子模块：

- **Scale Modulator**：将连续尺度 $s \in [0,1]$ 通过可学习正弦嵌入映射为高维向量，再经线性层生成通道级 FiLM 参数 $[\gamma, \beta]$，对编码器特征进行仿射调制：

$$[\gamma, \beta] = \mathrm{Linear}\big(\mathrm{LN}(\mathbf{e}(s))\big), \quad \mathrm{FiLM}(\mathbf{X}; s) = \mathbf{X} \odot (1 + \alpha\gamma) + \alpha\beta$$

- **双向交叉注意力**：替代传统的单向注意力，使点提示查询与全局特征相互增强：

$$\mathbf{q}^{(\ell+1)} = \mathbf{q}^{(\ell)} + \mathrm{CAttn}(\mathbf{q}^{(\ell)}; \mathbf{Y}^{(\ell)}), \quad \mathbf{Y}^{(\ell+1)} = \mathrm{FFN}(\mathbf{Y}^{(\ell)} + \mathrm{CAttn}(\mathbf{Y}^{(\ell)}; \mathbf{q}^{(\ell+1)}))$$

引入尺度提示（+scale）在交互式分割上带来 **14.72%**（PartObjaverse-Tiny）和 **14.99%**（PartNet-E）的性能提升（Table 1），验证了连续尺度调制对分割粒度的有效控制。

### 创新三：解耦训练策略

区别于端到端联合训练，S²AM3D 采用**解耦训练**：先稳定编码器表示（2D 蒸馏 + 3D 对比学习），再冻结编码器训练尺度感知解码器。这一策略避免了 2D 与 3D 监督信号在联合优化中的冲突，确保编码器先学到一致的点特征，解码器再在此基础上学习粒度调制。

S²AM3D 提出了一种**尺度可控、点提示驱动的三维点云部件分割框架**，其核心设计目标是在融合2D视觉基础先验的同时，解决多视角不一致与粒度不可控两大瓶颈。如图2所示，整体pipeline由四个关键模块串联构成：**Point-Consistent Part Encoder**、**Scale Modulator**、**Bi-directional Cross-Attention Decoder** 和 **Segmentation Head**，并采用解耦训练策略分别优化编码器与解码器。

**输入**：原始点云 $P \in \mathbb{R}^{N \times 3}$ 及交互提示 $(p, s)$，其中 $p$ 为查询点索引，$s \in [0,1]$ 为连续尺度信号。

**Point-Consistent Part Encoder** 首先通过Tri-plane投影将点云映射到三个正交特征平面，聚合多视角2D特征得到逐点特征 $\mathbf{F} \in \mathbb{R}^{N \times D}$（Eq. 1）。在此基础上，编码器同时接受**多视角2D蒸馏**与**实例内3D对比监督**（Eq. 2），拉近同部件点特征、推远异部件点特征，从而增强全局几何一致性——这是解决遮挡和细薄结构导致的多视角分割不一致的核心机制（Sec. 3.2）。

**Scale Modulator** 将连续尺度 $s$ 通过可学习正弦嵌入映射为高维向量 $\mathbf{e}(s)$（Eq. 3），再经线性层生成通道级仿射参数 $[\gamma, \beta]$，以FiLM方式对编码器各层特征进行调制（Eq. 4），使特征表示携带尺度信息。

**Bi-directional Cross-Attention Decoder** 接收尺度调制后的全局特征与查询点特征，通过 $L_d$ 层双向交叉注意力（Eq. 7）实现查询点与全局上下文的联合精炼：先以查询点特征为Query交叉关注全局特征，再反向以更新后的全局特征关注查询点，最后经FFN更新。

**Segmentation Head** 以轻量MLP + Sigmoid输出逐点部件掩码概率 $\hat{\mathbf{m}} \in [0,1]^N$（Eq. 8）。

**训练策略**：采用解耦训练（Sec. 3.4）——先以PartField预训练参数初始化编码器，结合对比损失在3D部件标注上精调至收敛后冻结；再单独训练尺度感知解码器，使用动态加权BCE与Dice组合损失（Eq. 9-10）处理正负样本极不平衡问题。这种解耦设计避免了编码器与解码器联合训练时的梯度冲突，确保编码器特征的稳定性。

**输出**：给定任意点提示 $p$ 和尺度 $s$，模型实时输出该尺度下对应部件的分割掩码，支持从精细零件到粗糙部件的连续粒度调控。

![[assets/figures/papers/paper_list_l2092_https_openaccess_thecvf_com_content_CVPR2026_html_Su_S2AM3D_Scale_contro/figures/001_Figure_1.jpg]]
*Figure 1: Paradigm comparison (left): Native 3D methods present limited generalization, and 2D-based methods fail in complex cases like occlusions. Our hybrid solution solves these issues. Performance Comparison (right): Our method reaches large-scale training performance with much less data and significantly outperforms previous methods at similar data scales*

S²AM3D 的整体架构由四个核心模块构成：**Point-Consistent Part Encoder**、**Scale Modulator**、**Bi-directional Cross-Attention Decoder** 和 **Segmentation Head**。以下逐一阐述其设计逻辑与关键公式。

---

### 3.1 Point-Consistent Part Encoder

编码器的核心目标是提取**全局一致**的逐点特征，解决纯2D蒸馏在多视角间的不一致性问题。其设计包含两个关键步骤：

**Tri-plane 投影与特征聚合。** 给定输入点云 $P \in \mathbb{R}^{N \times 3}$，首先将每个点正交投影到三个坐标平面 $xy$、$yz$、$zx$ 上，从对应的 Tri-plane 特征图 $\mathbf{T}_{xy}, \mathbf{T}_{yz}, \mathbf{T}_{zx}$ 中采样并求和，得到逐点特征：

$$\mathbf{F} = \Big[ \mathbf{T}_{xy}(x_n, y_n) + \mathbf{T}_{yz}(y_n, z_n) + \mathbf{T}_{zx}(z_n, x_n) \Big]_{n=1}^{N} \tag{1}$$

其中 $\mathbf{F} \in \mathbb{R}^{N \times D}$ 为聚合后的逐点特征，$D$ 为特征维度。Tri-plane 特征图本身由 2D 视觉基础模型（如 DINOv2）的多视角渲染结果蒸馏而来，继承了丰富的 2D 语义先验。

**实例内 3D 对比监督。** 仅靠 2D 蒸馏无法保证同一零件在不同视角下的特征一致性。为此，编码器额外引入**实例内对比损失**，在 3D 标注的监督下拉近同一零件的点特征、推远不同零件的点特征：

$$\mathcal{L}_{\mathrm{contr}} = \frac{1}{|\hat{P}|} \sum_{i \in \hat{P}} -\log \frac{\sum_{j \in \hat{P}(i)} e^{s_{ij}}}{\sum_{j \in \hat{P} \setminus \{i\}} e^{s_{ij}}} \tag{2}$$

其中 $\hat{P}$ 为采样点集，$\hat{P}(i)$ 表示与点 $i$ 属于同一零件的正样本点集。相似度 $s_{ij}$ 基于 $\ell_2$ 归一化后的特征向量计算余弦相似度，并除以温度系数 $\tau = 0.07$ 进行缩放。这一对比机制直接作用于 3D 几何空间，是编码器获得**点级全局一致性**的因果关键——消融实验中移除该监督后，PartObjaverse-Tiny 上 mIoU 从 61.19 骤降至 53.94（Table 3），验证了其决定性作用。

---

### 3.2 Scale Modulator

为实现**连续可控**的粒度分割，S²AM3D 引入显式的尺度信号 $s \in [0,1]$，其中 $s \to 0$ 对应细粒度（如螺丝、按钮），$s \to 1$ 对应粗粒度（如整个座椅）。该信号通过两个步骤嵌入网络：

**可学习正弦嵌入。** 将连续标量 $s$ 映射为高维嵌入向量：

$$\mathbf{e}(s) = \left[ \sin(\omega_k s + \phi_k), \cos(\omega_k s + \phi_k) \right]_{k=1}^{M} \tag{3}$$

其中 $\omega_k$ 和 $\phi_k$ 为可学习参数，$M$ 为嵌入维度。与固定频率的标准正弦位置编码不同，可学习参数使嵌入能自适应地捕捉尺度空间的结构。

**FiLM 通道调制。** 嵌入向量经 LayerNorm 和线性层后，分解为缩放参数 $\gamma$ 和偏移参数 $\beta$，对编码器特征进行通道级仿射变换：

$$[\gamma, \beta] = \mathrm{Linear}\big(\mathrm{LN}(\mathbf{e}(s))\big), \quad \mathrm{FiLM}(\mathbf{X}; s) = \mathbf{X} \odot (1 + \alpha \gamma) + \alpha \beta \tag{4}$$

其中 $\alpha$ 为门控系数，控制尺度调制的强度。FiLM 层共堆叠 $L_m = 2$ 层，逐层调节特征表示，使网络在不同尺度下激活不同的特征通道子集。消融实验表明，带尺度嵌入训练的模型即使在测试时不提供尺度条件（No scale 组），其性能仍优于完全无尺度嵌入的模型（Table 3），证明尺度嵌入增强了特征解码的鲁棒性。

---

### 3.3 Bi-directional Cross-Attention Decoder

解码器接收尺度调制后的全局特征 $\tilde{\mathbf{F}}$ 和点提示 $p$（即用户点击的目标点索引），通过**双向交叉注意力**实现提示与全局上下文的交互精炼。

记点提示对应的初始查询向量为 $\mathbf{q}^{(0)} = \tilde{\mathbf{F}}_p$，全局特征为 $\mathbf{Y}^{(0)} = \tilde{\mathbf{F}}$。每层解码器执行两步交叉注意力：

$$\begin{aligned}
\mathrm{CAttn}(\boldsymbol{A}; \boldsymbol{B}) &= \mathrm{MHA}(\boldsymbol{Q}=\boldsymbol{A}, \boldsymbol{K}=\boldsymbol{B}, \boldsymbol{V}=\boldsymbol{B}), \\
\mathbf{q}^{(\ell+1)} &= \mathbf{q}^{(\ell)} + \mathrm{CAttn}(\mathbf{q}^{(\ell)}; \mathbf{Y}^{(\ell)}), \\
\mathbf{Y}^{(\ell+1)} &= \mathrm{FFN}(\mathbf{Y}^{(\ell)} + \mathrm{CAttn}(\mathbf{Y}^{(\ell)}; \mathbf{q}^{(\ell+1)})).
\end{aligned} \tag{7}$$

其中 $\mathrm{MHA}$ 为多头注意力，$\mathrm{FFN}$ 为前馈网络。第一步将查询向量作为 Query，全局特征作为 Key/Value，使提示聚焦于相关区域；第二步反过来将全局特征作为 Query，更新后的查询向量作为 Key/Value，将提示信息广播回全局特征。这种**双向设计**相较于单向交叉注意力能更充分地融合局部提示与全局上下文。解码器共堆叠 $L_d = 4$ 层，在效率与性能间取得平衡。

---

### 3.4 Segmentation Head 与损失函数

解码器输出的交互增强特征 $\mathbf{H} = \mathbf{Y}^{(L_d)}$ 经轻量级 MLP 和 Sigmoid 输出逐点掩码概率：

$$\mathbf{o} = \mathrm{MLP}(\mathbf{H}), \qquad \hat{\mathbf{m}} = \sigma(\mathbf{o}) \in [0,1]^N \tag{8}$$

训练采用**混合分割损失**，结合动态加权 BCE 与 Dice 损失以应对正负样本严重不平衡问题：

$$\mathcal{L}_{\mathrm{seg}} = \lambda_{\mathrm{bce}} \mathrm{BCE}_{\mathrm{dyn}}(\hat{\mathbf{m}}, \mathbf{m}) + \lambda_{\mathrm{dice}} \Big(1 - \frac{2\hat{\mathbf{m}}^{\top}\mathbf{m}}{\|\hat{\mathbf{m}}\|_1 + \|\mathbf{m}\|_1}\Big) \tag{9}$$

其中 $\lambda_{\mathrm{bce}} = 0.7$，$\lambda_{\mathrm{dice}} = 0.3$。动态 BCE 根据当前样本中正样本比率 $\pi$ 自适应调整正样本权重 $\beta$：

$$\beta = \frac{1 - \pi}{\pi + \varepsilon}, \quad \pi = \frac{1}{N}\sum_{j=1}^{N} m_j \tag{10}$$

$$\mathrm{BCE}_{\mathrm{dyn}} = -\frac{1}{N}\Big(\beta \sum_{j \in J_{+}} \log \hat{m}_j + \sum_{j \in J_{-}} \log(1 - \hat{m}_j)\Big)$$

当正样本极少（$\pi \to 0$）时，$\beta$ 自动增大，防止模型退化为全负预测。Dice 损失则直接优化预测掩码与真值掩码的重叠度，对边界质量有额外约束。

---

### 3.5 解耦训练策略

S²AM3D 采用**解耦训练**方案：首先使用 PartField 预训练参数初始化编码器，在 3D 对比监督下精调至收敛后冻结；随后仅训练解码器部分。这一策略避免了联合训练中编码器特征尚未稳定时解码器梯度对其的干扰，确保尺度调制和双向注意力在高质量特征基础上发挥作用。

## 实验与关键发现

### 核心定量结果

S²AM3D在交互式分割与全分割两个任务上均取得最优性能，且仅需远少于大规模训练方法的数据量即可达到相当甚至更优的水平。

**交互式分割。** 在PartObjaverse-Tiny和PartNet-E两个基准上，S²AM3D的IoU分别达到46.47%和62.52%。引入尺度提示（+scale）后，性能大幅跃升至61.19%和77.51%，相对提升分别为+14.72和+14.99个百分点（Table 1）。这一结果验证了连续尺度信号对分割粒度的有效调控能力：模型可以根据同一提示点，按需输出从精细零件到粗糙部件的不同粒度掩码。

**全分割。** 在PartObjaverse-Tiny上，S²AM3D取得63.29% mIoU；在PartNet-E上取得77.98% mIoU，均显著优于PartField、SAMPart3D等基于2D先验的方法（Table 2）。值得注意的是，S²AM3D仅使用远少于P3-SAM的训练数据，即达到了与之可比的全分割性能（Figure 1右），证明2D-3D混合训练策略有效缓解了3D标注数据稀缺的瓶颈。

### 消融实验与因果验证

消融实验系统拆解了各设计选择的贡献，结果汇总于Table 3。

**3D对比监督的关键作用。** 移除编码器中的3D对比监督（w/o 3D supervision）导致性能急剧下降：PartObjaverse-Tiny上mIoU从61.19%降至53.94%，PartNet-E上从77.51%降至64.11%。Figure 6的可视化进一步揭示，无3D监督时点特征在部件边界处出现明显混淆，分割结果边界模糊、拓扑不完整；而完整模型的特征在同类部件内部高度一致，边界清晰。这确证了实例内对比损失对于消除多视角2D特征不一致性、建立全局几何一致表征的决定性作用。

**训练数据的质量贡献。** 将本文构建的大规模高质量数据集替换为PartNet进行训练（w/o our data），两个基准上的mIoU分别下降至57.86%和71.67%。这表明自动标注管道产出的数据在覆盖多样性和标注精度上均优于现有公开数据集，是模型性能的重要支撑。

**尺度嵌入的结构性收益。** 即使测试时不提供尺度条件（No scale组），带尺度嵌入训练的模型（Full）仍优于无尺度嵌入的模型（w/o scale embedding），说明尺度嵌入在训练过程中增强了特征解码的鲁棒性，使模型学到了更具判别力的表征，而非仅在推理时利用尺度信号。

**解码器深度配置。** 尺度调制层数L_m=2、双向交叉注意力层数L_d=4在效率和性能间取得良好平衡（Sec. 5.1），更深的解码器未带来显著增益。

### 定性分析与可控性验证

Figure 4展示了交互式分割的定性比较：S²AM3D对点提示的响应更精准，生成的掩码边界干净、拓扑完整，而对比方法在细薄结构或遮挡区域常出现断裂或溢出。Figure 5的全分割定性结果表明，S²AM3D在复杂拓扑和多部件场景下仍能保持一致的部件划分。

Figure 7直观验证了连续尺度可控性：对同一提示点，当尺度s从0连续增大至1时，分割结果从精细零件平滑过渡到粗糙部件组，而未使用尺度条件的对照则无法实现这种粒度调控。这证明尺度调制器（Scale Modulator）通过FiLM机制成功将连续标量信号转化为有意义的层级语义控制。

### 局限性与失效模式

尽管S²AM3D在定量和定性上均表现优异，仍存在以下已知局限：

1. **提示模态单一。** 当前框架仅支持点提示与尺度信号，缺乏对文本描述等更丰富模态的支持，限制了语义驱动的自然交互方式。论文在开放问题中也明确指出了这一方向。
2. **数据依赖与标注噪声。** 数据采集管道依赖自动标注流程，虽经过质量过滤与连通性细化，仍可能存在标注噪声和类别长尾分布问题，在极端稀有部件上的分割质量需进一步验证。
3. **极端几何的鲁棒性。** 对于极度细长或严重遮挡的零件，2D先验本身可能失效，3D对比监督的补偿能力存在上限，此类场景下的分割一致性有待更系统的评估。

> **注意：** 以上局限性的量化边界（如遮挡程度与性能退化的具体关系）在现有材料中未提供详细实验数据，建议读者在复现或应用时针对具体场景进行补充验证。

![[assets/figures/papers/paper_list_l2092_https_openaccess_thecvf_com_content_CVPR2026_html_Su_S2AM3D_Scale_contro/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison of full segmentation*

![[assets/figures/papers/paper_list_l2092_https_openaccess_thecvf_com_content_CVPR2026_html_Su_S2AM3D_Scale_contro/figures/009_Table_3.jpg]]
*Table 3: Ablation studies (mIoU, %). Groups indicate whether scale information is provided at test time: +scale means a scale condition is given, while No scale means it is not*

![[assets/figures/papers/paper_list_l2092_https_openaccess_thecvf_com_content_CVPR2026_html_Su_S2AM3D_Scale_contro/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of continuous scale controllability. With the same prompt point, as the scale s increases from 0 to 1, the segmentation transitions smoothly from fine to coarse; a (No scale) counterpart is also provided for reference*

![[assets/figures/papers/paper_list_l2092_https_openaccess_thecvf_com_content_CVPR2026_html_Su_S2AM3D_Scale_contro/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of full segmentation (PartObjaverse-Tiny [35]). For ease of comparison with our point cloud method, mesh-level outputs are presented as point clouds by uniformly sampling the segmented meshes*

![[assets/figures/papers/paper_list_l2092_https_openaccess_thecvf_com_content_CVPR2026_html_Su_S2AM3D_Scale_contro/figures/003_Figure_3.jpg]]
*Figure 3: Dataset overview: covering diverse categories and providing high-quality part-level annotations; the histogram shows the longtailed distribution of part counts*

## 定位与知识库关联

### 1. 从2D先验到3D一致性的技术演进

S²AM3D 的核心定位是**融合2D视觉基础先验与3D几何约束的混合范式**，其技术谱系可沿两条主线追溯：

**2D先验驱动的3D分割线**：早期工作 **PartSLIP**（Liu et al., CVPR 2023）利用多视角2D特征提升低资源场景下的3D部件分割，其增强版 **PartSLIP++**（Zhou et al., arXiv 2023）进一步引入多视角实例分割与最大似然估计。**Segment3D**（Huang et al., ECCV 2024）探索了无手工标签的细粒度类别不可知分割。然而，这些方法的核心瓶颈在于：2D分割先验因遮挡、细薄结构及复杂拓扑会导致多视角分割结果不一致。**PartField**（Liu et al., arXiv 2025）和 **SAMPart3D**（Yang et al., arXiv 2024）虽利用SAM进行部件分割，但依赖后处理聚类控制粒度，缺乏显式的粒度调制机制。

**原生3D分割线**：**P3-SAM**（Ma et al., arXiv 2025）和 **Point-SAM**（Zhou et al., arXiv 2024）等原生3D方法直接处理点云，但泛化能力受限，且需要大规模高质量3D部件标注数据——这正是当前领域的稀缺资源。**Find3D**（Ma et al., ICCV 2025）在查找任意3D部件方面做出了探索，但同样面临数据饥渴问题。

S²AM3D 的突破在于**以3D对比监督增强点特征全局一致性**，同时**以连续尺度信号引导解码器实现粒度可控的部件分割**，在两条技术路线之间找到了关键平衡点。

### 2. 关键设计差异与因果机制

与最相近的基线方法相比，S²AM3D 在四个关键维度上做出了实质性改变：

| 设计维度 | 基线方法 | S²AM3D 改进 | 因果作用 |
|---------|---------|------------|---------|
| 编码器监督 | 仅多视角2D蒸馏（如PartField） | 增加实例内3D对比监督 | 消除跨视角不一致，增强全局点特征一致性 |
| 粒度控制 | 后处理聚类或无显式控制 | 连续尺度信号 $s \in [0,1]$ 经可学习正弦嵌入与FiLM跨层调制 | 实现从精细到粗糙的连续可控分割 |
| 解码器注意力 | 单向交叉注意力 | 双向交叉注意力 | 联合精炼局部提示与全局特征信息 |
| 训练策略 | 端到端联合训练 | 解耦训练：先稳定编码器表征，再训练解码器 | 避免编码器-解码器联合优化中的表征漂移 |

其中，**3D对比监督**是最具决定性的因果旋钮——消融实验显示，移除该监督后，PartObjaverse-Tiny上mIoU从61.19骤降至53.94，PartNet-E上从77.51降至64.11（Table 3），充分证明了3D几何约束对全局特征一致性的关键作用。**尺度提示**则贡献了交互式分割上14.72%（PartObjaverse-Tiny）和14.99%（PartNet-E）的性能提升（Table 1），验证了连续尺度调制对分割粒度的有效控制。

### 3. 适用边界与局限

尽管S²AM3D在多个基准上达到了最优性能，其适用边界仍需明确：

**提示模态受限**：当前框架主要依赖点提示和尺度信号进行交互，缺乏对文本描述等更丰富提示模态的支持。这意味着用户无法通过自然语言（如“椅子的扶手”）直接指定分割目标，限制了更直观的语义交互场景。

**数据依赖与标注质量**：尽管本文构建了大规模数据集（Figure 3），但数据采集管道依赖自动标注流程，仍可能存在标注噪声和类别不均衡问题。消融实验中，使用PartNet替代本文数据集训练导致性能下降（Table 3, w/o our data），说明高质量标注数据的规模对模型性能有显著影响。

**极端几何的鲁棒性**：模型在极度细长或遮挡严重的零件上可能仍存在不一致性，这一局限在Figure 4的定性比较中有所暗示，但缺乏系统的鲁棒性验证实验。

### 4. 开放问题与未来方向

**多模态提示集成**：如何将文本描述等多模态提示集成到框架中，实现更自然的语义驱动部件分割，是当前最直接的扩展方向。这需要解决文本-3D特征对齐和跨模态注意力机制设计等问题。

**开放类别泛化**：在开放类别场景下，模型如何泛化到未见过的零件类别？当前的对比学习框架依赖实例内标注，难以直接迁移到零样本场景。引入大规模视觉-语言模型的知识蒸馏可能是潜在路径。

**层次式语义分割**：能否将尺度可控性从单一粒度拓展到层次式语义分割，支持多级粒度同时输出？例如，同时输出“椅子→靠背→靠背横杆”的层次化分割结果，这需要设计树形结构的尺度编码机制。

**与基础模型的深度融合**：当前方法以PartField预训练参数初始化编码器，未来可探索与更强大的3D基础模型（如Uni3D、Point-BERT等）的深度融合，进一步提升特征表征能力和泛化性能。

## 原文 PDF

![[paperPDFs/CVPR_2026/S_2_AM3D_Scale_controllable_Part_Segmentation_of_3D_Point_Clouds.pdf]]

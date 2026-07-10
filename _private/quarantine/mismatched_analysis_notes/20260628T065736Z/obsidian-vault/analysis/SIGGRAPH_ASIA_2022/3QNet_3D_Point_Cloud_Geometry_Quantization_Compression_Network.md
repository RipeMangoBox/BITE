---
title: "3QNet: 3D Point Cloud Geometry Quantization Compression Network"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/3QNet_3D_Point_Cloud_Geometry_Quantization_Compression_Network.pdf
project_link: null
code_link: "https://github.com/"
aliases:
- IIARM
- 33PCGQCN
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将离散表示学习从三维体积网格迁移到一维隐向量：先将编码后的体素特征投影到三个轴对齐正交平面，再用耦合网络将三平面特征融合为紧凑的隐向量，并在该隐向量上进行向量量化。
primary_logic: 通过在隐向量上执行离散表示学习，并借助耦合网络消除各元素在三维空间中的明确位置映射，既能将复杂度从 O(r³) 降至 O(r²) 且控制序列长度，又能获得更易处理的自回归顺序，使标准 Transformer 可以高效地学习形状先验，同时自然地支持无条件与多种条件生成任务。
claims:
- ImAM 在无条件生成任务上全面超越现有方法，在 ECD、1-NNA、MMD 与 CovT 等指标上取得最优
- 消融研究证实“隐向量 (Vector)”离散表示在生成质量上显著优于“三平面 (Tri-Plane)”表示，且重建精度接近“网格 (Grid)”表示但内存开销大幅降低
- 耦合网络有效消除了展平顺序带来的不稳定性：Vector 表示在不同顺序下的标准差远低于 Tri-Plane 表示
- 在类别引导、部分点云补全、图像引导和文本引导四种条件生成任务上，ImAM 均以显著优势超越对应基线
---

# 3QNet: 3D Point Cloud Geometry Quantization Compression Network

> [!tip] 核心洞察
> 通过在隐向量上执行离散表示学习，并借助耦合网络消除各元素在三维空间中的明确位置映射，既能将复杂度从 O(r³) 降至 O(r²) 且控制序列长度，又能获得更易处理的自回归顺序，使标准 Transformer 可以高效地学习形状先验，同时自然地支持无条件与多种条件生成任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于改进自回归模型的多功能三维形状生成 |
| 英文题名 | 3QNet: 3D Point Cloud Geometry Quantization Compression Network |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://tyshiwo.github.io/) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ImAM (Improved Auto-regressive Model) |
| Dataset | ShapeNet |

> [!tip] 效果简介
> - ShapeNet (13 categories, class-guide generation) 上，COV ↑ 79.67 vs GBIF 73.00 (+6.67)。
> - ShapeNet (image-guide generation) 上，FPD ↓ 1.680 vs CLIP-Forge 8.094 (-6.414)。
> - ShapeNet (unconditional generation, Plane category) 上，ECD ↓ 236 vs Tri-Plane 743 (-507)。

## 概要

现有基于自回归（AR）的三维形状生成方法通常将形状表示为三维体积网格上的离散码，面临两大瓶颈：**立方级离散码导致 Transformer 计算复杂度急剧上升**，难以收敛；**网格空间的展平顺序具有高度模糊性**，简单的逐行展平会破坏邻域耦合关系，导致生成质量不佳甚至模式坍塌。

本文提出 **ImAM（Improved Auto-regressive Model）**，核心思路是将离散表示学习从三维体积网格迁移到一维隐向量。具体而言，先将编码后的体素特征投影到三个轴对齐正交平面，再通过耦合网络将三平面特征融合为紧凑的隐向量，并在该隐向量上执行向量量化。这一设计将复杂度从 $O(r^3)$ 降至 $O(r^2)$，同时耦合网络消除了各元素在三维空间中的显式位置映射，使自回归序列获得更易处理的顺序，让标准 Transformer 可以高效地学习形状先验。

在 ShapeNet 数据集上，ImAM 在无条件生成任务上全面超越现有方法（ECD、1-NNA、MMD 等指标均最优）；在类别引导、部分点云补全、图像引导和文本引导四种条件生成任务上，均以显著优势超越对应基线。消融实验证实，隐向量离散表示在生成质量上显著优于三平面表示，且内存开销远低于网格表示；耦合网络有效消除了展平顺序带来的不稳定性。

## 核心方法与创新机理

### 问题瓶颈：体积网格自回归的两重困境

现有基于体积网格（volumetric grids）的自回归三维生成方法面临两个根本性瓶颈。第一，**立方级离散码导致的复杂度爆炸**：将三维形状编码为分辨率为 $r$ 的体积网格后，离散码的数量为 $O(r^3)$，Transformer 的自注意力计算复杂度随序列长度呈平方增长，使得模型难以收敛。第二，**网格展平顺序的高度模糊性**：将三维网格按固定空间顺序（如 x-y-z 轴方向逐行展开）展平为一维序列时，相邻元素在原始三维空间中的邻域耦合关系被破坏——不同的展平顺序会导致截然不同的序列结构，而模型对顺序极其敏感，直接导致生成质量不佳甚至模式坍塌。

### 核心洞察：从三维网格到一维隐向量的离散表示迁移

ImAM 的核心创新在于**将离散表示学习从三维体积网格迁移到一维隐向量空间**，通过一个精心设计的“三平面投影 + 耦合网络”模块链，在保留三维几何信息的前提下消除显式空间位置映射。这一迁移同时解决了上述两个瓶颈：

- **复杂度降维**：离散码数量从 $O(r^3)$ 降至 $O(r^2)$（三平面特征经耦合网络压缩后的隐向量长度），Transformer 的序列长度和计算复杂度得到根本性控制。
- **顺序模糊性消除**：耦合网络将三平面特征融合为无明确空间位置映射的隐向量，使得自回归序列成为“易处理顺序”（tractable order），不同展平顺序对生成结果的影响大幅降低。

### 框架总览：两阶段训练范式

ImAM 采用标准的两阶段自回归生成框架（Figure 2），但通过上述离散表示空间的创新实现了质的提升：

![[assets/figures/papers/paper_list_l13_https_tyshiwo_github_io/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our ImAM. Given an arbitrary 3D shape, we first project encoded volumetric grids into the three axis-aligned planes, and then use a coupling network to further project them into a latent vector. Vector quantization is thus performed on it for discrete representation. Taking advantages of such a compact representation with tractable orders, vanilla transformers are adopted to auto-repressively learn shape distributions. Furthermore, we can freely switch from unconditional generation to conditional generation by concatenating various conditions, such as point clouds, categories and images*

- **第一阶段（离散表示学习）**：训练一个自动编码器，将三维形状编码为离散码序列，并通过解码器重建原始形状。关键是离散化操作在隐向量而非体积网格上执行。
- **第二阶段（先验学习）**：固定编码器和解码器，使用标准 Transformer（decoder-only）自回归地学习离散码序列的联合分布。条件生成通过将条件特征拼接到序列开头实现。

### 第一阶段：改进的离散表示学习

第一阶段由五个串行模块组成，模块间的因果关系构成了 ImAM 的核心技术链。

**模块 1：点特征编码器（PointNet + Voxelization）**

输入为三维形状的点云采样，首先通过 PointNet 提取逐点特征，随后通过体素化（voxelization）将点特征聚合为分辨率为 $r \times r \times r$ 的体积网格特征 $f^{v} \in \mathbb{R}^{r \times r \times r \times d}$。这一模块将无序点云转化为结构化的网格表示，为后续的三平面投影提供基础。

**模块 2：三平面投影（Tri-Planar Projection）**

将体积网格特征分别沿三个轴对齐正交平面（xy、yz、xz）进行投影，通过池化操作将三维特征压缩为三个二维特征图 $f^{xy}, f^{yz}, f^{xz} \in \mathbb{R}^{r \times r \times d}$。这一步的关键作用是将 $O(r^3)$ 的三维表示降维为三个 $O(r^2)$ 的二维表示，同时保留不同视角下的几何信息。

**模块 3：耦合网络（Coupling Network）——核心创新模块**

耦合网络是 ImAM 消除顺序模糊性的关键设计。其操作分为两步：

1. **拼接**：将三个平面特征以任意顺序拼接，形成组合特征 $[f^{xy}; f^{yz}; f^{xz}]$。
2. **卷积融合与展平**：通过一个卷积网络 $\mathcal{G}$（由若干卷积层组成，详见 Table 9）对拼接特征进行融合学习，随后按行优先顺序展平为一维隐向量：

$$f = \tau(\mathcal{G}([f^{xy}; f^{yz}; f^{xz}]; \theta)) \in \mathbb{R}^{m \times d}$$

其中 $\tau$ 为展平操作，$m$ 为隐向量的元素数量，$d$ 为特征维度。耦合网络的卷积层通过可学习的感受野，将三平面特征中的空间邻域信息重新整合为无明确位置映射的隐向量元素，从而使得后续的自回归序列不再受限于固定的空间展平顺序。

**模块 4：向量量化（Vector Quantization）**

在隐向量 $f$ 上执行向量量化，而非在体积网格上。对于隐向量中的每个特征 $f_{(h,l,w)}^{v}$（此处沿用体积网格的索引习惯，实际为隐向量元素），将其替换为可学习码本 $\mathbf{q}$ 中距离最近的码本项：

$$\mathbf{z}^{v} = \mathcal{Q}(f^{v}) := \arg\min_{\mathbf{e}_i \in \mathbf{q}} || f_{(h,l,w)}^{v} - \mathbf{e}_i ||$$

量化后的离散码序列 $\mathbf{z}$ 即为形状的紧凑离散表示。码本大小和隐向量长度 $m$ 共同决定了表示的压缩率。

**模块 5：解码器（Decoder + Implicit Function）**

解码过程是编码的逆操作：从量化码本索引恢复隐向量特征，通过耦合网络的逆变换重建三平面特征，随后对任意查询点的三维坐标，通过在三平面上进行双线性插值获取特征，再经由一个轻量级隐式函数（MLP）预测该点的占位值（occupancy）。

**训练目标**

第一阶段的训练损失由两部分组成：

- **占位损失**（Occupancy Loss）：预测占位值 $y_o$ 与真值 $\tilde{y}_o$ 之间的二元交叉熵：

$$\mathcal{L}_{occ} = -(\tilde{y}_o \cdot \log(y_o) + (1 - \tilde{y}_o) \cdot \log(1 - y_o))$$

- **码本损失**（Codebook Loss）：拉近量化前后特征的距离，$\mathrm{sg}[\cdot]$ 表示停止梯度操作，$\beta=0.4$：

$$\mathcal{L}_{code} = \beta || \mathrm{sg}[f] - \mathbf{q}_{(\mathbf{z})} ||_2^2 + || f - \mathrm{sg}[\mathbf{q}_{(\mathbf{z})}] ||_2^2$$

第一项促使码本项向编码器特征靠近，第二项促使编码器特征向码本项靠近，共同保证量化过程的稳定性。

### 第二阶段：标准 Transformer 学习形状先验

第二阶段使用标准的 decoder-only Transformer 自回归地学习离散码序列的联合分布。对于无条件生成，Transformer 逐步预测序列中的每个离散码：

$$p(\mathbf{z}) = \prod_{i=1}^{m} p(\mathbf{z}_i \mid \mathbf{z}_{<i})$$

对于条件生成（如类别引导、部分点云补全、图像引导、文本引导），ImAM 采用统一的“前缀拼接”策略，将条件特征 $\mathbf{c}$ 置于序列开头：

$$p(\mathbf{z}) = \prod_{i=1}^{m} p(\mathbf{z}_i \mid \mathbf{c}, \mathbf{z}_{<i})$$

这一设计的优雅之处在于：**无需修改 Transformer 的结构或训练目标**，即可自由切换无条件生成与多种条件生成任务。条件特征 $\mathbf{c}$ 根据不同任务从对应的编码器（如类别嵌入、点云编码器、CLIP 图像编码器、CLIP/BERT 文本编码器）提取，并在训练时随机丢弃以支持无条件和条件生成的联合训练。

### 推理路径

推理时，Transformer 从起始标记开始，自回归地逐元素预测离散码序列，每次预测基于已生成的前缀序列（以及可选的条件特征）。完整的离散码序列随后通过第一阶段的解码器恢复为三维形状的隐式场表示，再通过 Marching Cubes 等算法提取显式网格。由于自回归的序列生成特性，推理需要 $m$ 次前向操作，这是自回归模型的固有开销。

### Changed Slots 总结

相对于以 AutoSDF、ShapeFormer 为代表的体积网格自回归方法，ImAM 改变了两个关键设计槽位：

| 设计槽位 | 基线方案 | ImAM 方案 | 因果作用 |
|---------|---------|----------|---------|
| 离散表示空间 | 三维体积网格 | 一维隐向量（经三平面投影与耦合网络获得） | 将复杂度从 $O(r^3)$ 降至 $O(r^2)$，控制序列长度 |
| 自回归顺序 | 固定空间展平顺序（如 x-y-z 逐行展开） | 耦合网络消除显式位置映射，获得易处理顺序 | 消除顺序模糊性，提升生成稳定性与质量 |

这两个 changed slots 之间存在因果依赖：**只有将离散表示从体积网格迁移到隐向量，耦合网络才能发挥作用；而耦合网络的存在，又使得隐向量表示在消除顺序模糊性方面显著优于直接在三平面上执行量化（即 Tri-Plane 表示）**。消融实验（Table 7）证实了这一因果链：Vector 表示在无条件生成质量上显著优于 Tri-Plane 表示，且耦合网络使不同展平顺序下的标准差远低于未耦合的 Tri-Plane 方案（Table 8 / Figure 10）。

![[assets/figures/papers/paper_list_l13_https_tyshiwo_github_io/figures/016_Figure_9.jpg]]
*Figure 9: Illustration of auto-regressive generation for triplanar representation. Here, we show three different flattening orders as examples*

## 实验与关键发现

ImAM 在无条件生成、类别引导生成、部分点云补全、图像引导生成和文本引导生成五类任务上均进行了系统验证。所有基线方法均在相同的训练/测试数据划分上重新训练或评估，使用统一的评估协议（COV、MMD、ECD、1-NNA 等），并引入带 LFD 阈值过滤的 CovT 指标以排除离群样本造成的虚假覆盖。

### 无条件生成

Table 1 报告了在 ShapeNet 五个代表性类别（Plane、Car、Chair、Rifle、Table）上的无条件生成结果。ImAM 在 ECD 和 1-NNA 两个核心指标上全面取得最优：ECD 平均值为 110（Plane 1236、Car 4842、Chair 1265、Rifle 4365、Table 4531），1-NNA 同样领先所有竞争对手。在 MMD 指标上，ImAM 以平均值 2608 显著优于所有基线（Plane 3124、Car 1213、Chair 2703、Rifle 3628、Table 2374），CovT 指标同样展现出明显优势。定性结果（Figure 3）进一步支持了定量结论，生成形状在不同类别间表现出高度的多样性和保真度。

![[assets/figures/papers/paper_list_l13_https_tyshiwo_github_io/figures/003_Table_1.jpg]]
*Table 1: Results of unconditional generation. Models are trained for each category. The best and second results are highlighted in bold and underlined*

![[assets/figures/papers/paper_list_l13_https_tyshiwo_github_io/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative results of unconditional generation*

### 条件生成

**类别引导生成**（Table 10）：在 ShapeNet 全 13 类别上训练，ImAM 的 COV 达到 79.67，相比 GBIF 的 73.00 提升 +6.67，较 AutoSDF 的 57.18 提升 +22.49，在所有指标上均以显著优势超越竞争对手。

**多模态部分点云补全**（Table 3）：在随机视角缺失场景下，ImAM 的 MMD（×10³）平均值为 0.869，远低于 cGAN 的 1.691、PVD 的 2.189 和 ShapeFormer 的 1.074。在固定上半部分缺失的设置下（Table 4），ImAM 同样保持最优。

**图像引导生成**（Table 5/Table 11）：ImAM 的 FPD 为 1.680，相比 CLIP-Forge 的 8.094 降低 6.414，降幅达 79.2%，在 COV 和 MMD 上也全面领先。

**文本引导生成**（Table 6）：ImAM 同样展现出强大的文本条件响应能力，定量指标优于 ITG 等基线方法。

### 关键消融实验

**离散表示空间的选择**（Table 7）：在 Plane 类别上对比了三种离散表示方案——网格（Grid）、三平面（Tri-Plane）和隐向量（Vector）。Vector 表示在无条件生成质量上显著优于 Tri-Plane：分辨率 32 时 Vector 的 ECD 为 236，Tri-Plane 为 743，差距达 507。Grid 表示虽在重建 IoU 上略高，但内存开销极大，在高分辨率下甚至无法运行（Figure 12）。Vector 表示在生成质量与计算效率之间取得了最佳平衡。

**耦合网络对展平顺序稳定性的影响**（Table 8 / Figure 10）：消融实验对比了有无耦合网络时不同展平顺序对生成结果的影响。在 Tri-Plane 表示下，不同展平顺序导致的性能标准差较大，表明网格空间的固定展平顺序具有高度模糊性；而 Vector 表示借助耦合网络消除了显式的位置映射关系，不同顺序下的标准差远低于 Tri-Plane，验证了耦合网络有效消解了展平顺序的不稳定性。

**条件嵌入策略**（Table 12）：使用序列级嵌入（如 CLIP 序列或 BERT 嵌入）作为文本条件，可进一步提升 ImAM 的文本引导生成性能，表明更丰富的条件表达有助于自回归模型学习条件分布。

### 局限性与适用边界

自回归模型的固有局限在 ImAM 中仍然存在：推理需要多次前向操作，生成单个样本耗时较长；存在错误累积风险，当输入条件包含噪声时可能生成不正确甚至坍塌的形状。目前模型仅在 ShapeNet 等标准数据集上验证，对极端复杂场景或开放域文本/图像条件的鲁棒性尚未充分评估，需要进一步验证。

![[assets/figures/papers/paper_list_l13_https_tyshiwo_github_io/figures/011_Table_5.jpg]]
*Table 5: Quantitative results of image-guide generation*

![[assets/figures/papers/paper_list_l13_https_tyshiwo_github_io/figures/008_Table_3.jpg]]
*Table 3: Results of multi-modal partial point completion. The missing parts vary according to random viewpoints*

## 定位与知识库关联

ImAM 的核心贡献在于对自回归 3D 形状生成框架中**离散表示空间**这一关键 slot 的重构。已有基于体积网格的自回归方法（如 AutoSDF 、ShapeFormer ）直接在三维体素网格上执行向量量化，导致码本序列长度随分辨率立方增长，且空间展平顺序的任意性严重破坏局部邻域耦合。ImAM 将该 slot 从“三维体积网格”替换为“一维隐向量”，通过三平面投影与耦合网络消除显式空间位置映射，使序列长度从 $O(r^3)$ 降至 $O(r^2)$，同时获得对自回归模型更友好的可处理顺序。这一改变的本质是将离散表示学习从“结构化空间量化”迁移到“解耦的隐空间量化”，属于**生成式 3D 自回归模型的表示层创新**。

**知识库挂载点**：
1. **离散表示学习 (VQ-VAE 家族)**：ImAM 继承了 VQ-VAE 的两阶段训练范式（编码-量化-解码 + 自回归先验学习），但将量化操作从 2D 图像特征图或 3D 体素网格迁移到一维隐向量。该设计可挂载到“向量量化表示学习”知识节点，关键差异在于量化前的**维度压缩策略**（三平面投影 + 耦合网络），这为后续研究提供了“通过几何投影降低自回归序列复杂度”的通用思路。
2. **三平面表示 (Tri-Plane)**：三平面表示本身已在 NeRF 加速等领域得到验证，ImAM 将其引入离散自回归框架作为中间表示，并通过耦合网络将其融合为紧凑向量。这建立了“三平面编码”与“自回归生成”之间的桥接点，后续工作可探索其他多平面投影方式或更高效的融合策略。
3. **自回归 3D 生成**：ImAM 证明了标准 Transformer（decoder-only）在恰当设计的离散表示上即可取得 SOTA，无需针对 3D 设计特殊的位置编码或序列表征。该结论可挂载到“自回归序列建模”节点，表明表示空间的设计比模型架构的定制化更为关键。

**相对已有方法的本质差异**：
- 相比 **AutoSDF**（Mittal et al., CVPR 2022）和 **ShapeFormer**（Yan et al., ECCV 2022）等基于网格量化的自回归方法，ImAM 将量化位置从“空间网格”移至“隐向量”，从根本上规避了展平顺序模糊性问题。消融实验（Table 8 / Figure 10）证实，耦合后的 Vector 表示在不同展平顺序下的标准差远低于 Tri-Plane 表示，这是网格方法无法实现的稳定性。
- 相比 **IM-GAN** 和 **GBIF** 等隐式生成对抗方法，ImAM 采用自回归似然建模，天然支持显式密度估计与条件拼接，在无条件生成（Table 1）和类别引导生成（Table 10，COV 79.67 vs GBIF 73.00）上均实现显著超越。
- 相比 **CLIP-Forge**（Sanghi et al., CVPR 2022）等基于 CLIP 嵌入的生成方法，ImAM 在图像引导任务上通过将 CLIP 特征直接拼接到序列开头实现条件注入，FPD 从 8.094 降至 1.680（Table 11），表明自回归框架对多模态条件的兼容性优于归一化流或扩散先验。

**适用边界**：
1. **数据分布**：ImAM 目前仅在 ShapeNet 的 13 个类别上验证，对开放域复杂形状或跨类别泛化的能力尚未评估。三平面投影假设形状可被三个正交平面充分表征，对于极度细长或拓扑复杂的形状可能存在信息瓶颈。
2. **推理效率**：自回归生成需要逐 token 解码（序列长度 $m$ 次前向），相比单次前向的 GAN 或扩散模型，推理延迟较高。这是自回归范式的固有局限，而非 ImAM 特有问题。
3. **条件鲁棒性**：当输入条件包含强噪声时（如稀疏部分点云或低质量渲染图），自回归的错误累积可能导致生成崩溃。论文未对此进行系统的鲁棒性测试。

**后续启发**：
- **表示空间设计优先于模型架构**：ImAM 的成功表明，为自回归模型设计紧凑且顺序无关的离散表示，比设计复杂的 3D-aware Transformer 更为有效。后续研究可探索其他维度压缩策略（如球面投影、图编码）或非欧几里得量化空间。
- **耦合网络作为顺序稳定器**：耦合网络通过卷积融合三平面特征并展平为向量，实质上是将“空间顺序选择”委托给可学习的卷积核。该设计可推广到其他需要处理多维数据展平问题的自回归任务（如视频生成、多视图生成）。
- **统一条件生成框架**：ImAM 通过简单拼接实现类别、点云、图像、文本四种条件的统一注入，无需针对每种条件设计独立的编码器或交叉注意力模块。这种“前置条件 token”的范式为构建通用 3D 生成基础模型提供了简洁的接口设计参考。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/3QNet_3D_Point_Cloud_Geometry_Quantization_Compression_Network.pdf]]
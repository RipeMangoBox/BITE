---
title: "From Rays to Projections: Better Inputs for Feed-Forward View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/From_Rays_to_Projections_Better_Inputs_for_Feed_Forward_View_Synthesis.pdf
project_link: "https://wuzirui.github.io/pvsm-web"
code_link: null
aliases:
- PPVSM
- FRPBIFFVS
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 使用确定性栅格化引擎生成的“目标视角投影点云图像”替代原始Plücker射线参数作为模型输入，将相机几何处理完全代理给非学习的投影算子。
primary_logic: 将新视角合成从脆弱的几何回归问题重构成一个稳定的图像到图像转换任务：投影算子天然提供了坐标系统不变的商空间表示，使网络无需浪费容量学习全局变换不变性。
claims:
- 随机SE(3)变换下，Plücker射线条件模型输出严重退化，而投影条件保持鲁棒（Figure 3）。
- 在世界尺度变换测试中，投影条件模型PSNR为25.43 dB，而LVSM仅14.56 dB，差距超过10 dB，印证射线条件对尺度变化的极度脆弱（Table 1）。
- 投影算子q将配置空间映射到商空间，消除对全局坐标系的选择依赖，从数学上保证了不变性（Section 4.1）。
- RealEstate10K (Total) 上 PSNR = 25.64 (12 layers)
---

# From Rays to Projections: Better Inputs for Feed-Forward View Synthesis

> [!tip] 核心洞察
> 将新视角合成从脆弱的几何回归问题重构成一个稳定的图像到图像转换任务：投影算子天然提供了坐标系统不变的商空间表示，使网络无需浪费容量学习全局变换不变性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从光线到投影：前馈视图合成的更好输入条件 |
| 英文题名 | From Rays to Projections: Better Inputs for Feed-Forward View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.05116) · [Project](https://wuzirui.github.io/pvsm-web) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | PVSM (Projective View Synthesis Model) |
| Dataset | RealEstate10K, Consistency Benchmark, RealEstate10K Small Overlap |

> [!tip] 效果简介
> - RealEstate10K (Total) 上，PSNR 25.64 (12 layers) vs LVSM 24.60 (12 layers) (+1.04)；PSNR 26.90 (24 layers) vs LVSM 25.74 (24 layers) (+1.16)。
> - Consistency Benchmark (World Scale) 上，PSNR (M) 25.43 vs LVSM 14.56 (+10.87)。
> - Consistency Benchmark (Anisotropic Pixel) 上，SSIM 0.763 vs LVSM 0.725 (+0.038)。

## 概要

前馈式新视角合成（feed-forward novel view synthesis）旨在从少量标定上下文图像直接预测目标视角的RGB图像，避免逐场景优化。然而，现有方法普遍将相机参数编码为**Plücker射线坐标**作为条件输入，这一设计对全局坐标系统高度敏感——即使微小的SE(3)变换也会在6D射线空间中产生大幅度、非均匀的扰动，导致模型泛化能力差、几何一致性脆弱。

本文提出**PVSM（Projective View Synthesis Model）**，核心思想是将新视角合成从脆弱的几何回归问题**重构为稳定的图像到图像转换任务**。具体而言，PVSM使用确定性栅格化引擎生成“目标视角投影点云图像”替代原始Plücker射线参数：先从上下文视图提取深度图并反投影为统一3D点云，再从目标相机视角栅格化。该投影算子天然提供坐标系统不变的商空间表示，使网络无需浪费容量学习全局变换不变性。

**核心结论**：
- 在一致性基准测试中，投影条件模型在世界尺度变换下达到25.43 dB PSNR，而基于射线的LVSM仅14.56 dB，差距超过10 dB，印证射线条件对几何变换的极度脆弱。
- 在RealEstate10K数据集上，PVSM以12层ViT达到25.64 PSNR，较LVSM提升1.04 dB；24层模型达到26.90 PSNR，提升1.16 dB。
- 引入MAE自监督预训练和DINOv3特征先验进一步增强了场景补全能力和结构一致性。

**方法定位**：PVSM属于前馈式视图合成方法，与基于3D高斯泼溅的PixelSplat、MVSplat、NoPoSplat、AnySplat等并行工作互补，也与基于射线的LVSM（Jin et al., ICLR 2025）、RayZer（Jiang et al., arXiv 2025）形成直接对比。其关键创新在于将相机几何处理完全代理给非学习的投影算子，从而在根本上解决了射线条件对全局坐标系敏感的核心瓶颈。

### 前馈视图合成中的条件输入问题

新视角合成（Novel View Synthesis, NVS）旨在从一组稀疏的上下文图像中生成任意目标视角的逼真图像。近年来，前馈式大视角合成模型（Large View Synthesis Models, LVSMs）因其无需逐场景优化的高效推理能力而受到广泛关注。这类模型的核心范式是：将上下文图像与目标视角的相机参数编码为条件信号，输入神经网络直接预测目标视图。

然而，现有方法在**条件输入的设计**上存在根本性缺陷。主流方案采用**Plücker射线坐标**作为相机姿态的条件表示——对每个目标像素构造一条从相机光心出发、穿过像素平面的射线，并用6维Plücker坐标 $(\mathbf{m}, \mathbf{d})$ 编码其空间位置与方向。这种表示虽然在数学上完备，却引入了一个关键瓶颈：

> **Plücker射线条件对全局坐标系统的选择高度敏感。** 即使对场景施加一个微小的刚体变换（SE(3)），射线坐标也会在6D空间中产生大幅度、非均匀的扰动，导致模型泛化能力差和几何一致性脆弱。

具体而言，给定一个全局SE(3)变换 $g = (R, \mathbf{t})$，其在Plücker坐标上的作用为：

$$(\mathbf{m}', \mathbf{d}') = \rho(g)(\mathbf{m}, \mathbf{d}) = (R\mathbf{m} + [\mathbf{t}]_\times R\mathbf{d}, R\mathbf{d})$$

这一变换揭示了两层问题：**方向分量** $\mathbf{d}$ 仅随旋转 $R$ 变化，而**矩分量** $\mathbf{m}$ 同时受旋转和平移的耦合影响，且平移项 $[\mathbf{t}]_\times R\mathbf{d}$ 在空间上非均匀分布。这意味着，网络必须隐式地学习对这种全局变换的不变性——这是一项浪费容量且难以泛化的任务。

### 现有方法的缺口

以 **LVSM**（Jin et al., ICLR 2025）为代表的射线条件模型在标准基准上取得了可观性能，但其脆弱性在分布外（OOD）场景下暴露无遗。当测试时对全局坐标系统施加随机SE(3)变换时，射线条件模型的输出严重退化，产生不可用的渲染结果（Figure 3）。更定量地看，在世界尺度变换测试中，LVSM的PSNR骤降至14.56 dB，而本文提出的投影条件方法可达25.43 dB——差距超过10 dB（Table 1）。这印证了射线条件对尺度变化的极度脆弱。

此外，**RayZer**（Jiang et al., arXiv 2025）等方法将视角索引硬编码到位置嵌入中，进一步加剧了模型对特定相机配置的过拟合，难以泛化到任意视角排列。**PixelSplat**、**MVSplat**、**NoPoSplat** 等基于前馈3D高斯泼溅的方法虽然显式建模了几何结构，但其条件输入本质上仍依赖相机参数与坐标系统的对齐，同样面临泛化瓶颈。

### 本文动机与核心洞察

上述分析指向一个根本性的重思考：**能否将新视角合成从脆弱的几何回归问题，重构为一个稳定的图像到图像转换任务？**

本文的核心洞察在于：**投影算子天然提供了坐标系统不变的商空间表示。** 当我们将上下文像素反投影为统一3D点云，再从目标相机视角栅格化时，这一组合操作 $q$ 的输出仅依赖于相机与几何之间的**相对排列**，而与全局坐标系统的选择无关。数学上，同时变换相机矩阵 $\mathbf{P}$ 和三维点 $\mathbf{X}$ 不改变投影关系：

$$\mathbf{P}' \mathbf{X}' \sim (\mathbf{P} T^{-1}) (T \mathbf{X}) = \mathbf{P} \mathbf{X}$$

因此，$q(\mathbf{X})$ 提供了配置空间 $X/\text{SE}(3)$ 的不变表示，使网络无需浪费容量学习全局变换不变性。

基于这一洞察，本文提出**投影条件（Projective Conditioning）**：使用确定性栅格化引擎生成的“目标视角投影点云图像”替代原始Plücker射线参数作为模型输入，将相机几何处理完全代理给非学习的投影算子。这一设计将视图合成问题转化为一个条件图像生成任务，天然具备对全局坐标变换的鲁棒性。

## 核心方法与创新机理

PVSM的核心创新在于将前馈视图合成从**脆弱的几何回归问题重构为稳定的图像到图像转换任务**。这一重构通过三个关键设计实现，每个设计都对应一个传统Plücker射线条件范式的根本缺陷。

### 瓶颈洞察：Plücker射线的坐标敏感性

现有前馈视图合成方法（如**LVSM**，Jin et al., ICLR 2025）使用6D Plücker射线参数 $(\mathbf{m}, \mathbf{d})$ 作为目标视角的条件输入。然而，这种表示对全局坐标系统的选择高度敏感。如Section 3.2所揭示，当场景和相机同时经历一个SE(3)变换 $g = (R, \mathbf{t})$ 时，Plücker坐标的变换规律为：

$$(\mathbf{m}', \mathbf{d}') = \rho(g)(\mathbf{m}, \mathbf{d}) = (R\mathbf{m} + [\mathbf{t}]_\times R\mathbf{d}, R\mathbf{d})$$

这一变换在射线空间中产生**非均匀、空间变化的扰动**——不同像素位置的射线参数变化幅度截然不同。网络被迫消耗大量容量去隐式学习这种全局变换不变性，而非专注于场景几何与外观的建模。这直接导致了两个后果：泛化能力差（对未见过相机位姿的合成质量下降）和几何一致性脆弱（对世界尺度、像素各向异性、FOV变化和旋转等变换极度敏感）。

### 核心创新一：投影条件替代射线条件

PVSM用**投影点云图像** $\mathcal{T}^{ct}$ 完全替代Plücker射线图作为目标视角的条件输入（changed slot: target view conditioning input）。其生成过程如下：

$$\mathcal{T}^{ct} = \mathtt{Rast}(\{\mathtt{UnProj}(\mathcal{D}_i^c, \mathcal{T}_i^c, \mathcal{C}_i^c)\}, \mathcal{C}^t)$$

具体而言：首先使用现成感知模型（如MapAnything）从上下文视图提取深度图 $\mathcal{D}_i^c$；然后将上下文像素反投影为统一3D点云；最后从目标相机视角 $\mathcal{C}^t$ 栅格化该点云，生成一幅携带几何线索的2D投影图像。

这一设计的关键在于**将相机几何处理完全代理给确定性的非学习投影算子**。如Section 4.1的数学分析所示，投影算子 $q$ 将配置空间 $\mathcal{X}$ 映射到商空间 $\mathcal{X}/\mathrm{SE}(3)$：

$$\mathbf{P}' \mathbf{X}' \sim (\mathbf{P} T^{-1}) (T \mathbf{X}) = \mathbf{P} \mathbf{X}$$

该等式证明：同时变换相机和三维点不改变投影关系，因此 $q(\mathcal{X})$ 提供了与全局坐标系统无关的不变表示。网络只需学习映射 $h: \operatorname{Im}(q) \to \mathcal{T}^t$，整体函数 $f = h \circ q$ 从设计上保证了坐标无关性。

**决定性证据**：Figure 3展示了随机全局SE(3)变换下，Plücker射线条件模型输出严重退化，而投影条件保持鲁棒。Table 1的定量结果更为惊人——在世界尺度变换测试中，PVSM的PSNR达到25.43 dB，而LVSM仅14.56 dB，差距超过10 dB，直接印证了射线条件对尺度变化的极度脆弱。

### 核心创新二：MAE自监督预训练

PVSM引入了一个**掩码自编码器预训练阶段**（changed slot: pretraining），充分利用投影条件的2D特性。与基线方法从零开始在标定数据上训练不同，PVSM首先在**无标定图像数据**上进行自监督预训练：输入上下文视图和随机掩码的目标视图，训练模型重构完整目标视图。这一阶段学习跨视图的场景补全先验，降低了对昂贵3D标注的依赖。

预训练的有效性在Table 4中得到验证：在DL3DV上预训练并在RealEstate10K上微调50K步，可获得最佳PSNR（27.43/25.60/23.64 on Large/Medium/Small splits）。Table 6的消融进一步表明，预训练、DINO特征先验和投影条件三者结合达到最佳总体结果（25.64 PSNR, 0.832 SSIM）。

### 核心创新三：RoPE位置编码

为处理投影点云图像中因遮挡产生的空洞区域，PVSM对所有token应用**旋转位置嵌入**（RoPE，changed slot: positional encoding）。这一设计的必要性在Table 7的消融中得到强有力的证明：移除RoPE导致PSNR从30.03骤降至21.18，且模型在空洞区域完全崩溃，输出完全相同的图像块。RoPE确保每个token获得唯一的位置信息，使网络能够区分有效投影区域和待补全的空洞区域。

### 辅助改进

除上述三个核心changed slot外，PVSM还引入了**DINOv3特征先验**（changed slot: context features），将预训练视觉模型的语义特征与RGB图像块拼接作为上下文token，经验性地增强了结构一致性。

PVSM的整体流水线围绕一个核心设计原则展开：**将新视角合成从脆弱的几何回归问题重构为稳定的图像到图像转换任务**。为此，方法将相机几何处理完全代理给一个非学习的确定性投影算子，网络本身仅需学习2D图像域内的映射。

### 两阶段训练范式

方法采用"预训练—微调"的两阶段训练策略，如Figure 2所示：

1. **MAE自监督预训练阶段**：模型以一组上下文视图和一个随机掩码的目标视图为条件，学习重建完整的目标视图。该阶段使用无标定图像数据，利用投影条件的2D特性学习场景补全先验，从而减少对昂贵3D标注的依赖。

2. **投影条件微调阶段**：模型以上下文视图和从目标相机视角栅格化生成的投影点云图像为条件，直接预测目标视图的RGB输出。投影点云图像由深度提取与反投影—栅格化模块生成，提供与全局坐标系统无关的稳定2D输入。

### 核心模块与数据流

整个流水线由以下模块串联构成：

**深度提取** → **反投影与栅格化** → **ViT主干网络** → **RGB解码**

- **深度提取**：使用现成感知模型（如MapAnything）从每个上下文视图提取深度图，为后续几何变换提供必要的场景几何信息。
- **反投影与栅格化**：将上下文像素反投影为统一3D点云，再从目标相机视角栅格化，生成投影点云图像 $\mathcal{T}^{c t}$。这一过程由确定性算子 $\mathtt{Rast}(\{\mathtt{UnProj}(\mathcal{D}_i^c, \mathcal{T}_i^c, \mathcal{C}_i^c)\}, \mathcal{C}^t)$ 完成，将相机几何处理完全代理给非学习的投影算子。
- **ViT主干网络**：采用解码器形式的Vision Transformer，处理拼接后的三类标记——上下文RGB图像块、投影点云图像块以及DINOv3特征标记。所有标记应用RoPE位置编码以保证空间唯一性。
- **RGB解码**：线性层加sigmoid激活，将目标视图对应的输出标记解码回RGB图像块。

### 输入输出规范

- **输入**：$N^c$ 个上下文视图 $\{\mathcal{T}_i^c\}$ 及其深度图 $\{\mathcal{D}_i^c\}$、上下文相机参数 $\{\mathcal{C}_i^c\}$、目标相机参数 $\mathcal{C}^t$。
- **中间表示**：投影点云图像 $\mathcal{T}^{c t}$，作为目标视图的几何先验条件。
- **输出**：目标视图的RGB图像 $\hat{\mathcal{Z}}^t$。

### 训练目标

训练损失结合MSE和感知损失：

$$\mathcal{L} = \mathsf{MSE}(\mathbb{Z}^t, \hat{\mathcal{Z}}^t) + \lambda \cdot \mathsf{Perceptual}(\mathbb{Z}^t, \hat{\mathcal{Z}}^t)$$

其中 $\mathbb{Z}^t$ 为真实目标图像，$\lambda$ 为平衡超参数。

![[assets/figures/papers/paper_list_l2494_https_arxiv_org_abs_2601_05116/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our proposed two-stage training pipeline. 1. Pretraining: This stage is self-supervised with the model conditioned on a set of context views and a randomly masked version of the target view itself (Masked Image). Its objective is to reconstruct the complete, original Ground Truth (GT) Target View. 2. Fine-Tuning: The context views are first unprojected into a unified 3D point cloud with extracted depth from perception models [14], which is then rasterized from the perspective of the target camera’s frustum to create a point cloud projection image that provides geometric cues. The model is then fine-tuned to generate the final target image*

### 问题形式化：SE(3) 不变性的缺失

前馈视图合成模型的核心任务可表述为：给定 $N^c$ 个上下文视图 $\{(\mathcal{T}_i^c, \mathcal{C}_i^c)\}_{i=1}^{N^c}$ 和目标相机参数 $\mathcal{C}^t$，预测目标视图图像 $\mathcal{T}^t$。一个理想的视图合成模型 $\mathcal{M}$ 应满足 SE(3) 不变性——当对整个场景和所有相机施加同一个全局刚体变换 $g \in \text{SE}(3)$ 时，渲染结果应保持不变：

$$\mathcal{M}(\{(\mathcal{T}_i^c, g \cdot \mathcal{C}_i^c)\}_{i=1}^{N^c}, g \cdot \mathcal{C}^t) = \mathcal{M}(\{(\mathcal{T}_i^c, \mathcal{C}_i^c)\}_{i=1}^{N^c}, \mathcal{C}^t)$$

现有方法使用 Plücker 射线坐标 $\mathbf{L} = (\mathbf{m}, \mathbf{d})$ 作为相机条件输入，其中 $\mathbf{m} = \mathbf{o} \times \mathbf{d}$ 为矩向量，$\mathbf{o}$ 为射线原点，$\mathbf{d}$ 为归一化方向。然而，在全局 SE(3) 变换 $g = (R, \mathbf{t})$ 下，Plücker 坐标的作用规律为：

$$(\mathbf{m}', \mathbf{d}') = \rho(g)(\mathbf{m}, \mathbf{d}) = (R\mathbf{m} + [\mathbf{t}]_\times R\mathbf{d}, R\mathbf{d})$$

该变换对每个像素的射线产生**非均匀、空间变化的扰动**——靠近相机中心与边缘区域的射线参数变化幅度截然不同。这使得网络必须隐式学习全局坐标变换的不变性，导致容量浪费和泛化脆弱性（Figure 3 展示了随机 SE(3) 扰动下 Plücker 条件模型的严重退化）。

### 核心模块一：投影条件算子

PVSM 的核心创新在于用**投影点云图像** $\mathcal{T}^{ct}$ 替代 Plücker 射线图作为目标视图条件输入。该算子由两个子步骤级联构成：

**深度提取与反投影**：首先利用现成感知模型（如 MapAnything）从每个上下文视图提取深度图 $\mathcal{D}_i^c$，然后将上下文像素反投影为统一世界坐标系下的 3D 点云：

$$\text{UnProj}(\mathcal{D}_i^c, \mathcal{T}_i^c, \mathcal{C}_i^c)$$

**目标视角栅格化**：将所有上下文视图反投影得到的点云合并，从目标相机 $\mathcal{C}^t$ 的视角进行确定性栅格化渲染，生成一张 2D 投影点云图像：

$$\mathcal{T}^{ct} = \mathtt{Rast}(\{\mathtt{UnProj}(\mathcal{D}_i^c, \mathcal{T}_i^c, \mathcal{C}_i^c)\}, \mathcal{C}^t)$$

该投影点云图像编码了从目标视角可见的场景几何与纹理信息。其关键性质在于：投影算子 $q$ 将原始配置空间映射到**商空间** $\mathcal{X}/\text{SE}(3)$，输出仅依赖于相机与几何之间的**相对排列**，而与全局坐标系的选取无关。数学上，同时变换相机矩阵和三维点不改变投影关系：

$$\mathbf{P}' \mathbf{X}' \sim (\mathbf{P} T^{-1}) (T \mathbf{X}) = \mathbf{P} \mathbf{X}$$

因此网络学习的是一个从商空间到目标图像的映射 $h: \text{Im}(q) \to \mathcal{T}^t$，整体函数 $f = h \circ q$ 从设计上保证了规范不变性（gauge-free conditioning）。

### 核心模块二：标记化与 Transformer 主干

投影点云图像 $\mathcal{T}^{ct}$ 与上下文 RGB 图像 $\mathcal{T}_i^c$ 均被切分为不重叠的 $p \times p$ 图像块，经线性嵌入转化为标记序列：

$$\mathbf{x}_{ij}^{\mathrm{c}} = \mathrm{Linear}_{\mathrm{c}}(\mathcal{T}_{ij}^c), \quad \mathbf{x}_{j}^{\mathrm{t}} = \mathrm{Linear}_{\mathrm{p}}(\mathcal{T}_{j}^{ct})$$

此外，模型还拼接了来自预训练 DINOv3 模型的上下文视图特征 $\mathbf{f}^{\text{dino}}$，以增强结构一致性。所有标记拼接后送入**仅解码器的 ViT 主干网络**进行处理。为解决投影点云图像中空洞区域（无投影点覆盖的像素）可能导致的标记混淆，所有标记均施加**旋转位置嵌入（RoPE）**，确保每个标记获得唯一的位置信息。消融实验表明，移除 RoPE 会导致 PSNR 从 30.03 骤降至 21.18，且模型在空洞区域坍缩为预测完全相同的图像块（Table 7, Figure 8）。

### 核心模块三：两阶段训练策略

**第一阶段——MAE 预训练**：利用投影条件的 2D 特性，在**无标定数据**上进行掩码自编码预训练。将目标视图随机掩码后作为输入，以上下文视图为条件，训练模型重构完整目标视图。该阶段学习跨视图的场景补全先验，降低对昂贵 3D 标注的依赖。

**第二阶段——投影条件微调**：在标定数据上，将掩码目标视图替换为投影点云图像 $\mathcal{T}^{ct}$，微调模型从投影条件直接预测目标视图。训练损失结合 MSE 和感知损失：

$$\mathcal{L} = \mathsf{MSE}(\mathbb{Z}^t, \hat{\mathcal{Z}}^t) + \lambda \cdot \mathsf{Perceptual}(\mathbb{Z}^t, \hat{\mathcal{Z}}^t)$$

其中 $\mathbb{Z}^t$ 为真实目标图像，$\hat{\mathcal{Z}}^t$ 为预测图像，$\lambda$ 为平衡超参数。最终，最后一层 Transformer 输出中对应目标视图的标记经线性层和 sigmoid 激活解码为 RGB 图像块。

### 方法局限性

投影条件算子的精度高度依赖外部深度估计模型的质量；当前流水线仅适用于静态场景，对动态物体会产生鬼影或模糊伪影；模型的插值能力仍局限于训练数据分布，对未观测区域的填空缺乏生成多样性。

## 实验与关键发现

### 一致性基准：几何鲁棒性的压力测试

为系统评估不同条件输入对相机变换的鲁棒性，作者构建了一致性基准（Consistency Benchmark），对同一场景施加四种相机变换：各向异性像素缩放（Anisotropic Pixel）、世界尺度缩放（World Scale）、视场角变化（FOV）和绕光轴旋转（Roll）。基线方法**LVSM**（Jin et al., ICLR 2025）在Plücker射线条件下对全局坐标变换极度敏感——在世界尺度测试中PSNR仅14.56 dB，而PVSM达到25.43 dB，差距超过10 dB（Table 1）。在绕光轴旋转测试中，PVSM的SSIM为0.629，LVSM仅0.489，进一步印证射线条件对非均匀扰动的脆弱性。定性结果（Figure 4）显示，LVSM在变换后产生严重的几何错位和模糊，而PVSM保持了稳定的场景结构。

![[assets/figures/papers/paper_list_l2494_https_arxiv_org_abs_2601_05116/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on our proposed Consistency Benchmark. We evaluate model robustness against four types of camera transformations. Our method produces more consistency results with the projective conditioning compared to ray-based [10, 12] view synthesis models and 3D Gaussian baselines [11, 18]. *We use the 24 view checkpoint from RayZer [10], see Sec. 5.1 for details. “+ aug.” denotes models fine-tuned with additional camera augmentations for 500 extra steps*

![[assets/figures/papers/paper_list_l2494_https_arxiv_org_abs_2601_05116/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Results on our Consistency Benchmark. Our method produces more geometrically consistent results. LVSM struggles to maintain geometric consistency, while RayZer and AnySplat fail to retrieve accurate camera parameters*

| 变换类型 | 指标 | LVSM | PVSM (Ours) | 提升 |
|---------|------|------|-------------|------|
| World Scale | PSNR (M) | 14.56 | 25.43 | +10.87 |
| Anisotropic Pixel | SSIM | 0.725 | 0.763 | +0.038 |
| FOV | SSIM | 0.840 | 0.877 | +0.037 |
| Roll | SSIM | 0.489 | 0.629 | +0.140 |

### RealEstate10K标准基准

在RealEstate10K数据集上，PVSM在12层和24层配置下均超越LVSM基线。12层配置下PVSM达到25.64 PSNR（LVSM为24.60），24层配置下达到26.90 PSNR（LVSM为25.74），提升分别为+1.04和+1.16 dB（Table 2）。在小重叠（Small Overlap）场景下，PVSM的优势更为显著：已见场景（Seen）PSNR达24.30（LVSM 22.14），未见场景（Unseen）达21.29（LVSM 19.39），分别提升+2.16和+1.90 dB（Table 3）。这表明投影条件在输入视图与目标视图差异较大时，其几何先验能更有效地引导模型完成跨视图推理。

![[assets/figures/papers/paper_list_l2494_https_arxiv_org_abs_2601_05116/figures/007_Table_2.jpg]]
*Table 2: Quantitative evaluation results on the RealEstate10K [50] dataset. We follow the benchmark splits from NoPoSplat [39]. *We use the 24 view checkpoint from RayZer [10], see Sec. 5.1 for details*

### 消融实验：核心组件的贡献

**投影条件的独立增益**：在LVSM架构上仅增加投影映射（projection），PSNR即从基线约24.60提升至25.20（Table 6），证明投影条件本身是性能提升的核心驱动力，而非架构或训练技巧的附带效应。

**预训练策略**：在DL3DV大规模数据集上预训练并在RealEstate10K上微调50K步，可获得最佳PSNR（27.43/25.60/23.64，对应NoPoSplat的大/中/小重叠基准）（Table 4）。预训练赋予模型跨视图补全的先验知识，显著降低了对目标域标注数据的依赖。

**DINOv3特征先验**：引入DINOv3特征后，PSNR从24.60提升至25.20，SSIM从0.812提升至0.822（Table 6）。DINO特征提供了语义层面的结构一致性约束，有助于模型在遮挡和纹理稀疏区域保持合理的几何推断。

**RoPE位置编码的关键作用**：移除RoPE位置编码后，模型性能从30.03 PSNR骤降至21.18（Table 7），且出现严重退化——模型在空洞区域输出完全相同的图像块（Figure 8）。这是因为投影点云图像中存在大量无投影覆盖的空白区域，RoPE为每个token提供了唯一的位置信息，使模型能够区分有效区域与空白区域，避免注意力机制在空白区域塌缩为常数输出。

### 失败模式与局限性

定性比较（Figure 6）揭示了PVSM的两类典型失败模式：

![[assets/figures/papers/paper_list_l2494_https_arxiv_org_abs_2601_05116/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparisons on the RealEstate10K [50] dataset. Our model consistently generates more plausible and geometrically consistent results. We highlight two common failure modes where Orange boxes indicate rendering artifacts like blurriness and ghosting, while blue boxes suggest geometric errors where models fail to preserve scene structure or render from the correct viewpoint*

- **动态物体伪影**：对于包含移动物体的场景，模型会产生模糊或鬼影，因为投影条件假设场景是静态的，动态物体的深度信息在上下文视图间不一致，导致反投影和栅格化产生错误的几何对应。
- **未观测区域的填空局限**：当目标视角包含上下文视图完全未覆盖的区域时，模型只能生成训练数据中的平均模式，输出缺乏细节和真实感。这是前馈式方法的固有限制——模型学习的是场景补全的先验分布，而非真正的生成能力。

此外，PVSM依赖外部深度估计模型（如MapAnything）提供的几何信息，深度估计的误差会通过反投影-栅格化流水线传播，影响最终渲染质量。在深度估计失败的区域（如透明表面、镜面反射），投影点云图像会出现空洞或错位，模型需依赖上下文图像特征进行补偿，但在极端情况下仍会产生明显伪影。

![[assets/figures/papers/paper_list_l2494_https_arxiv_org_abs_2601_05116/figures/013_Table_7.jpg]]
*Table 7: Ablation studies on the use of RoPE [27]*

## 定位与知识库关联

### 前馈视图合成的方法谱系

本文提出的**PVSM**（Projective View Synthesis Model）处于前馈视图合成（feed-forward view synthesis）这一活跃研究脉络中。该脉络的核心目标是从稀疏的上下文视图直接预测新视角图像，避免逐场景优化，代表性工作可分为两大技术路线：

**基于3D显式重建的路线**以**PixelSplat**、**MVSplat**、**NoPoSplat**等为代表，它们通过前馈网络预测3D Gaussian Splatting原语，再通过可微分栅格化渲染目标视角。这类方法显式构建中间3D表示，对相机标定精度和跨视图几何一致性有较高要求。**AnySplat**（Jiang et al., arXiv 2505.23716, 2025）进一步拓展至无约束视角输入，**Hunyuan-WorldMirror**（Liu et al., arXiv 2510.10726, 2025）则引入任意先验提示进行3D世界重建。

**基于图像到图像转换的路线**以**LVSM**（Jin et al., ICLR 2025）为代表，将视图合成建模为从上下文图像到目标图像的像素级预测任务，使用Plücker射线作为相机姿态的条件输入。**RayZer**（Jiang et al., arXiv 2505.00702, 2025）在此基础上引入自监督训练策略，进一步扩展了模型规模。

PVSM在谱系上的定位是：延续LVSM的图像到图像转换范式，但从根本上替换了条件输入机制——用投影点云图像替代Plücker射线。这一替换并非简单的工程改进，而是对“相机几何如何注入网络”这一核心设计选择的重新审视。

### 核心创新与基线方法的关键差异

PVSM与基线方法的核心差异体现在条件输入的设计哲学上：

| 设计维度 | LVSM / RayZer | PVSM |
|---------|--------------|------|
| 条件输入 | Plücker射线图（6D） | 投影点云图像（3D→2D投影） |
| 几何处理 | 网络需隐式学习相机几何 | 投影算子显式处理几何 |
| 坐标系统依赖性 | 依赖全局坐标系选择 | 商空间表示，天然SE(3)不变 |
| 预训练策略 | 无/有限 | MAE自监督预训练（利用投影条件的2D特性） |
| 语义先验 | 仅RGB | RGB + DINOv3特征 |

**Plücker射线的脆弱性根源**：给定全局SE(3)变换 $g=(R,\mathbf{t})$，Plücker坐标的变换为

$$(\mathbf{m}', \mathbf{d}') = \rho(g)(\mathbf{m}, \mathbf{d}) = (R\mathbf{m} + [\mathbf{t}]_\times R\mathbf{d}, R\mathbf{d})$$

其中 $\mathbf{m}$ 为矩向量，$\mathbf{d}$ 为方向向量。该变换在6D空间中产生非均匀、空间变化的扰动——平移分量 $\mathbf{t}$ 通过叉积项 $[\mathbf{t}]_\times R\mathbf{d}$ 耦合进矩向量，使得即使微小的全局刚体变换也会导致各像素的射线参数发生不同幅度的变化。网络必须从数据中隐式学习这种复杂的变换不变性，这本质上是一个脆弱的几何回归问题。

**投影条件的商空间不变性**：PVSM通过投影算子 $q$ 将配置空间映射到商空间 $\mathcal{X}/\text{SE}(3)$。核心数学保证在于：

$$\mathbf{P}' \mathbf{X}' \sim (\mathbf{P} T^{-1}) (T \mathbf{X}) = \mathbf{P} \mathbf{X}$$

即同时变换相机投影矩阵 $\mathbf{P}$ 和三维点 $\mathbf{X}$ 不改变投影关系。因此，投影算子 $q(\mathcal{X})$ 的输出仅依赖于相机与几何之间的相对排列，与全局坐标系的选择无关。网络学习映射 $h: \text{Im}(q) \to \mathcal{T}^t$，整体函数 $f = h \circ q$ 在结构上保证了规范不变性（gauge-free conditioning）。

这一设计将新视角合成从脆弱的几何回归问题重构为稳定的图像到图像转换任务——投影算子承担了所有几何推理，网络仅需处理2D图像域的补全和细化。

### 适用边界与局限性

**静态场景假设**：PVSM的核心流水线——深度提取、反投影、栅格化——天然假设场景是静态的。对于包含动态物体的场景，反投影的点云会在运动区域产生几何不一致，导致投影点云图像中出现撕裂或鬼影，最终渲染结果也会继承这些伪影。论文明确指出这是方法的固有限制。

**插值能力的本质约束**：尽管MAE预训练使模型学习了场景补全先验，但其本质仍是对训练数据平均模式的回归。对于大面积未观测区域（如严重遮挡或大基线视角变化），模型倾向于生成模糊的平均纹理，而非多样化的真实内容。这是前馈确定性模型的结构性限制，与生成式方法（如扩散模型）形成对比。

**深度估计依赖**：投影条件图像的质量直接取决于深度图的精度。PVSM使用现成感知模型（如MapAnything）提取深度，其误差会通过反投影-栅格化管道传播。在深度估计失败的区域（如无纹理表面、细薄结构、反射表面），投影点云图像会出现空洞或错位，模型需要额外的容量来补偿这些缺陷。

**训练数据分布依赖**：RealEstate10K数据集以室内外房地产场景为主，相机运动模式相对规整（多为平滑平移）。模型在此分布上学到的先验可能难以泛化到任意相机轨迹或截然不同的场景类型（如航拍、显微成像）。

### 开放问题

**与生成模型的融合**：投影条件提供了几何稳定的输入表示，但其确定性输出在未观测区域缺乏多样性。一个自然的研究方向是将投影条件作为扩散模型或自回归模型的条件信号，在保持几何一致性的同时产生多样化且符合场景上下文的补全内容。这需要解决如何在生成过程中保持跨视图一致性的挑战。

**动态场景的拓展**：处理动态场景需要超越静态反投影的几何建模。可能的路径包括：(1) 引入运动估计模块，对动态区域单独处理；(2) 使用时变投影条件表示；(3) 将动态物体视为独立图层进行合成。这要求训练数据包含动态场景标注，且微调策略需要平衡静态先验与动态适应。

**无标定场景的泛化**：当前方法依赖精确的相机内外参和深度图。向无标定图像或大规模非结构化视频数据拓展，需要联合优化或学习相机姿态估计、深度估计与视图合成，构成更具通用性的端到端系统。投影条件框架的模块化设计为此提供了潜在的接口——深度提取和相机估计模块可被替换为可学习组件。

**规模化与数据效率**：MAE预训练已展示了利用无标定数据学习场景先验的潜力，但预训练数据规模、领域多样性与下游性能的缩放关系尚未充分探索。此外，如何在不牺牲几何一致性的前提下减少对精确深度标注的依赖，仍是一个开放问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/From_Rays_to_Projections_Better_Inputs_for_Feed_Forward_View_Synthesis.pdf]]

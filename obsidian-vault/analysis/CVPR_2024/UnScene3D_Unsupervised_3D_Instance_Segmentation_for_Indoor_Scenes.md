---
title: "UnScene3D: Unsupervised 3D Instance Segmentation for Indoor Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/UnScene3D_Unsupervised_3D_Instance_Segmentation_for_Indoor_Scenes.pdf
aliases:
- UnScene3D
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在几何基元上进行多模态自监督特征融合与归一化割生成稀疏伪掩码，并通过自训练迭代扩展和细化实例分割。"
primary_logic: "利用几何过分割基元作为粗化表示，一方面降低计算复杂度并正则化特征噪声，另一方面在统一图上融合互补的2D颜色和3D几何自监督特征，通过归一化割提取稀疏但可靠的伪掩码，再通过自训练逐步发现缺失实例，实现无监督的密集实例分割。"
claims:
- "在ScanNet上，UnScene3D的AP达到15.9，相比传统聚类方法（如Felzenswalb AP 5.0）提升超过3倍（300%）。"
- "融合2D颜色和3D几何特征生成的伪掩码显著优于单一模态，最终自训练后AP达到15.9（3D-only: 13.3, 2D-only: 15.7）。"
- "自训练从初始伪掩码不断改进性能，约4轮后饱和（AP: 初始5.9 → 第1轮10.4 → 第4轮15.9）。"
- "使用DropLoss应对伪掩码的噪声和缺失标注，最终AP达到15.9，优于基线损失（AP 14.2）和投影损失（AP 7.2）。"
---

# UnScene3D: Unsupervised 3D Instance Segmentation for Indoor Scenes

> [!tip] 核心洞察
> 利用几何过分割基元作为粗化表示，一方面降低计算复杂度并正则化特征噪声，另一方面在统一图上融合互补的2D颜色和3D几何自监督特征，通过归一化割提取稀疏但可靠的伪掩码，再通过自训练逐步发现缺失实例，实现无监督的密集实例分割。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | UnScene3D：面向室内场景的无监督三维实例分割 |
| 英文题名 | UnScene3D: Unsupervised 3D Instance Segmentation for Indoor Scenes |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2303.14541); [Project](https://rozdavid.github.io/unscene3d) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UnScene3D |
| Dataset | ScanNet, S3DIS Area 5, ScanNet (self-training progression) |

> [!tip] 效果简介
> - ScanNet 上，AP@25 / AP@50 / AP 为 58.5 / 32.2 / 15.9，对比 38.9 / 12.7 / 5.0 (Felzenswalb)，变化 +19.6 / +19.5 / +10.9。
> - S3DIS Area 5 上，AP@25 / AP@50 / AP 为 52.6 / 40.3 / 21.4，对比 27.9 / 11.2 / 5.0 (HDBSCAN)，变化 +24.7 / +29.1 / +16.4。
> - ScanNet (self-training progression) 上，AP (from initial pseudo masks to final) 为 15.9 (after 4 iterations)，对比 5.9 (initial pseudo masks)，变化 +10.0。

## 概述

### 问题瓶颈

无监督3D实例分割旨在不依赖任何人工标注的情况下，从三维场景中分离出语义上有意义的独立物体。现有方法在杂乱室内场景中面临严重性能退化：传统聚类方法（如 **Felzenswalb**、**HDBSCAN**）仅依赖几何或颜色信号进行启发式分割，缺乏对物体级语义的推理能力；基于图割的细化方法（如 **Nunes et al.**）虽然引入了优化框架，但仍受限于单一模态特征的表达能力；而将二维无监督方法（如 **CutLER**）投影到三维的策略则难以保持三维空间中的实例一致性。核心瓶颈在于：**现有方法无法充分利用多模态自监督特征进行对象级推理，且缺乏有效的自训练机制以从噪声数据中逐步学习**。

### 核心方法定位

**UnScene3D** 提出了一套完整的无监督3D实例分割框架，其核心思想可以概括为“粗化表示—多模态融合—稀疏伪掩码—自训练扩展”的闭环流程：

1. **几何基元粗化**：在网格场景上使用 Felzenswalb 算法进行几何过分割，将数万顶点聚合为数百个基元，降低计算复杂度并正则化特征噪声。
2. **多模态特征融合**：在基元上聚合自监督的2D颜色特征（DINO）和3D几何特征（CSC），通过加权平均构建统一的相似度图。
3. **掩蔽归一化割生成伪掩码**：迭代应用归一化割（Normalized Cut）从融合特征中提取稀疏但可靠的伪掩码，作为自训练的初始监督信号。
4. **自训练扩展**：使用3D Transformer骨架配合 DropLoss 进行多轮自训练，从初始稀疏伪掩码逐步发现遗漏实例，最终输出密集、完整的实例分割。

该方法的关键创新在于**在几何基元层次上进行多模态自监督特征融合与归一化割**，既避免了直接对原始点云操作的计算开销，又通过互补模态增强了伪掩码的可靠性；而**DropLoss 自训练机制**则有效应对了伪掩码的噪声和缺失标注问题，使模型能够从稀疏监督中学习到完整的实例分割能力。

### 主要结果

在 ScanNet 数据集上，UnScene3D 的类无关实例分割 AP 达到 **15.9**，相比传统聚类方法 Felzenswalb（AP 5.0）提升超过 **3倍（300%）**。消融实验表明，融合2D和3D特征生成的伪掩码（最终 AP 15.9）显著优于单一模态（3D-only: 13.3，2D-only: 15.7）；自训练从初始伪掩码 AP 5.9 逐步提升至 15.9，约4轮后趋于饱和；DropLoss 策略（AP 15.9）优于标准损失（AP 14.2）和投影损失（AP 7.2）。在 S3DIS Area 5 上，UnScene3D 同样展现出显著的跨数据集泛化能力（AP 21.4 vs HDBSCAN 5.0）。

## 背景与动机

三维场景理解是计算机视觉与机器人领域的核心问题，其中**三维实例分割**——将场景分解为独立的、语义一致的对象区域——是实现精细场景交互的关键前提。然而，现有高性能的三维实例分割方法几乎完全依赖大规模人工标注数据进行全监督训练。三维数据的标注成本极高：标注者需要在密集的三维点云或网格上逐点勾勒对象边界，这比二维图像标注耗时数个数量级。

这一困境催生了**无监督三维实例分割**的研究方向：在不使用任何人工标注的条件下，从原始三维数据中直接发现并分割出语义上有意义的对象实例。然而，当前的无监督方法普遍面临性能瓶颈。在杂乱、遮挡严重的室内场景中，传统聚类方法（如基于密度的**HDBSCAN**、基于图的**Felzenswalb**过分割）以及基于图割的细化方法（如**Nunes et al.**）往往产生大量碎片化或错误合并的分割结果。在ScanNet基准上，这些方法的平均精度（AP）仅约5.0，远未达到实用水平。

造成这一瓶颈的深层原因有三个方面：

1. **模态利用不足**：现有方法大多仅依赖三维几何信息（如法向量、空间坐标）进行聚类，未能有效利用RGB图像中丰富的颜色和纹理信号。二维自监督模型（如DINO）已展现出强大的对象级语义感知能力，但这些信号尚未被系统地融入三维无监督分割流程。

2. **缺乏对象级推理机制**：直接对密集的三维点或体素进行聚类，容易受到局部几何噪声的干扰，难以形成全局一致的对象边界。现有方法缺少一种既能降低计算复杂度、又能正则化特征噪声的中间表示，以支持可靠的对象级图分割。

3. **无有效的自训练范式**：在无监督设定下，初始伪标签不可避免地包含噪声和遗漏。现有方法缺乏一种能从稀疏、不完美的伪掩码出发，通过迭代自训练逐步发现缺失实例并细化边界的机制。如何设计损失函数以应对伪标签中的假阴性（遗漏实例），是一个尚未被充分探索的关键问题。

此外，二维无监督实例分割方法（如**CutLER**）虽可通过深度投影扩展到三维，但投影过程引入的几何误差和跨视图不一致性严重限制了其三维分割质量。三维自监督预训练方法（如**CSC**）能学习有判别力的点级特征，但如何将这些特征转化为对象级的实例分割，仍缺乏有效的下游机制。

上述缺口共同指向了一个核心需求：**在几何粗化表示上融合多模态自监督特征，生成稀疏但可靠的伪掩码，并通过鲁棒的自训练机制迭代扩展为密集的实例分割结果**。这正是UnScene3D所瞄准的问题空间。

## 核心创新

UnScene3D针对无监督3D实例分割在杂乱室内场景中性能低下的瓶颈，提出了一套从伪掩码生成到自训练细化的完整方案。其核心创新并非单一技术的堆砌，而是围绕**几何基元上的多模态归一化割**与**噪声鲁棒的自训练循环**这两个因果调节变量展开，形成了从稀疏可靠掩码到密集完整分割的递进式推理路径。

### 1. 几何基元上的多模态归一化割伪掩码生成

传统无监督方法（如HDBSCAN、Felzenswalb）直接对点云或网格顶点进行聚类或图割，易受局部几何噪声干扰，且无法有效利用自监督深度特征的语义信息。UnScene3D的关键设计在于引入**几何过分割基元（geometric primitives）**作为场景的粗化表示——通过Felzenswalb算法将网格顶点按法向量和颜色相似性聚类为过分割块，将图节点数从百万级顶点降至数百个基元。这一操作同时实现了三个目的：降低归一化割的计算复杂度、正则化逐点特征噪声、提供具有物理边界的操作单元。

在此基元图上，UnScene3D融合了互补的**2D颜色自监督特征（DINO）**与**3D几何自监督特征（CSC）**，通过独立计算相似度矩阵后加权平均的方式构建多模态亲和图。随后，采用迭代的**掩蔽归一化割（Masked NCut）**提取伪掩码：每轮求解广义特征值问题$(D-W)v = \lambda D v$得到第二小特征向量，通过阈值$\tau_{cut}$二值化相似度矩阵后分割出当前最显著的对象区域，并将其从图中移除后继续下一轮提取。该策略产生的初始伪掩码$M^0$虽然稀疏（ScanNet上AP仅5.9），但精度远高于直接聚类方法，为后续自训练提供了高质量的起点。

消融实验（Table 3）证实了这一设计的有效性：仅使用3D特征生成的伪掩码经一轮自训练后AP为13.3，仅使用2D特征为15.7，而融合双模态后达到15.9。Table 12进一步表明，归一化割生成的伪掩码质量显著优于FreeMask等替代方案。

### 2. 噪声鲁棒的自训练循环与DropLoss

伪掩码的稀疏性和不可避免的噪声标注构成了自训练的天然障碍。UnScene3D采用3D Transformer骨架进行多轮自训练，其核心创新体现在两个层面：

**掩码增扩策略（Mask Addition）**：Table 8的消融表明，直接使用上轮预测作为监督或使用Felzenswalb掩码均会导致性能退化。最优策略是保持初始伪掩码固定，每轮动态添加高置信度的新预测结果，在保持标签清洁度的同时逐步扩展覆盖范围。

**DropLoss损失函数**：面对伪掩码中大量未标注区域（缺失实例），标准交叉熵与Dice损失会将未匹配区域视为负样本，抑制模型发现新实例。UnScene3D采用DropLoss，仅对与上一轮伪标注重叠超过阈值$\tau_{drop}$的预测区域计算损失，未匹配区域不参与梯度回传。Table 6显示，DropLoss在4轮自训练后达到AP 15.9，显著优于标准损失（AP 14.2）和投影损失（AP 7.2），证明其有效释放了模型发现遗漏实例的能力。

自训练的迭代效果在Table 4中得到量化：初始伪掩码AP为5.9，第1轮自训练后跃升至10.4，第4轮达到15.9后趋于饱和。Figure 6的可视化进一步印证了自训练在实例数量和掩码质量上的持续改进。

### 3. 与基线方法的系统差异

UnScene3D相对于现有基线的方法槽位变更可归纳为：

| 方法槽位 | 基线方法 | UnScene3D设计 | 因果作用 |
|---------|---------|--------------|---------|
| 场景表示 | 直接对点/体素操作 | 几何基元图粗化 | 降低计算复杂度，正则化噪声 |
| 特征模态 | 仅3D几何特征 | 2D颜色+3D几何自监督特征融合 | 互补信号提升对象区分度 |
| 伪掩码生成 | 直接聚类或图割 | 几何基元上的迭代掩蔽归一化割 | 提取稀疏但高精度的初始掩码 |
| 自训练损失 | 标准交叉熵+Dice | DropLoss（忽略未匹配区域） | 防止噪声负样本抑制新实例发现 |

这些变更共同构成了UnScene3D的核心技术路径：以几何基元为粗化载体，以多模态归一化割为伪掩码生成引擎，以DropLoss驱动的自训练为密集化手段，最终在ScanNet上实现AP 15.9（相比Felzenswalb的AP 5.0提升超过3倍），在S3DIS Area 5上达到AP 21.4（相比HDBSCAN的AP 5.0提升超过4倍）。

## 整体框架

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/009_Figure_7.jpg]]
*Figure 7: As UnScene3D does not require any human annotation, so we can also train and test our method on the ARKitScenes [2] dataset. We leverages 3D features followed by a series of selftraining iterations for cleaner, more accurate instance segmentation. Qualitative results shows consistently better results than our baselines*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/001_Figure_1.jpg]]
*Figure 1: We propose UnScene3D, a fully-unsupervised 3D instance segmentation method, effectively separating semantic instances without requiring any manual annotations. We utilize geometric primitives to ensure crisp masks, and due to our self-training loop, we can also obtain a dense set of predictions, even in cluttered indoor scenarios*

UnScene3D 的整体 pipeline 由两个级联阶段构成：**伪掩码生成（Pseudo Mask Generation）**与**自训练（Self-Training）**，如 Figure 2 所示。其核心设计思想是：在几何基元（geometric primitives）上融合多模态自监督特征，通过归一化割（Normalized Cut）提取稀疏但可靠的伪掩码，再利用自训练迭代扩展和细化，最终输出密集的实例分割结果。

### 输入与场景表示

方法以室内场景的 RGB‑D 重建网格作为输入，将场景建模为图 $G = (V, E)$，其中 $V$ 为网格顶点，$E$ 为三角形面的边。这一网格图表示是整个 pipeline 的基础数据结构。

### 阶段一：伪掩码生成

伪掩码生成的目标是从无标注数据中自动提取一组初始实例候选。该阶段由三个关键模块串联而成：

1. **几何基元提取**：使用 Felzenswalb 算法将网格顶点按其法线和颜色相似性进行过分割，得到一组几何基元 $\{S_N\} = \{C_1, \dots, C_N\}$。这一粗化步骤一方面降低了后续图割的计算复杂度，另一方面通过局部几何一致性正则化特征噪声，为生成“锐利”的实例边界奠定基础。

2. **多模态特征聚合**：在几何基元上分别聚合二维自监督特征 $\mathcal{F}_{2D}$（如 DINO）和三维自监督特征 $\mathcal{F}_{3D}$（如 CSC），得到维度为 $\mathbb{R}^{N \times D_{2D/3D}}$ 的特征矩阵。二维颜色特征仅用于此阶段的伪掩码生成，自训练和测试阶段仅使用三维几何特征。

3. **掩蔽归一化割（Masked NCut）**：在聚合特征上构建多模态相似度矩阵（由 2D 和 3D 相似度矩阵加权平均得到），并迭代应用归一化割。具体流程如 Algorithm 1 所示：首先通过阈值 $\tau_{cut}$ 将相似度矩阵二值化以形成连通图，然后求解广义特征值问题 $(D - W)v = \lambda D v$ 得到第二小特征向量进行图分割；每次分割后过滤掉分离的碎片，仅保留包含特征向量绝对值最大项的连通分量作为伪掩码 $m_j$。迭代终止于达到最大实例数 $N_m$ 或场景中无剩余片段，最终得到初始伪掩码集 $M^0 = \{m_i\}_{i=1}^{N_m}$。

该阶段输出的伪掩码具有**稀疏但相对干净**的特点——这一“质量优先”的策略是后续自训练能够有效展开的关键。

### 阶段二：自训练

自训练阶段以初始伪掩码集 $M^0$ 作为监督信号，训练一个基于 3D Transformer 的实例分割模型，并通过多轮迭代逐步扩展和细化实例掩码。

- **训练策略**：每轮自训练使用上一轮的模型预测更新伪标注。消融实验（Table 8）表明，最优策略是**保持初始掩码固定**，并动态添加高置信度的新预测（Mask Addition），而非直接使用上一轮的全部预测或 Felzenswalb 掩码。
- **损失函数**：采用 DropLoss 应对伪掩码的噪声和缺失标注——仅对与上一轮标注的重叠度超过阈值 $\tau_{drop}$ 的预测区域计算交叉熵和 Dice 损失的加权组合，未匹配区域的损失被直接丢弃。这一设计使模型能够发现初始伪掩码遗漏的实例区域。
- **收敛特性**：自训练约 4 轮后性能趋于饱和（AP 从初始伪掩码的 5.9 提升至 15.9，Table 4）。

### 输出

自训练完成后，模型输出最终的实例分割预测 $M'$，在保持边界锐利的同时，实现了从稀疏候选到密集覆盖的跨越。

### 关键设计选择与因果链路

| 设计选择 | 因果作用 | 证据锚点 |
|---------|---------|---------|
| 几何基元粗化 | 降低计算复杂度，正则化特征噪声，保证边界锐利 | Section 3.1.3, Table 9 |
| 多模态特征融合 | 2D 颜色与 3D 几何信号互补，伪掩码质量显著优于单一模态 | Table 3 |
| 掩蔽 NCut 生成稀疏伪掩码 | 提供“干净但稀疏”的初始监督，避免噪声放大 | Algorithm 1, Table 12 |
| DropLoss + 固定初始掩码 | 允许模型发现遗漏实例，同时防止噪声强化 | Table 6, Table 8 |

整个 pipeline 的因果逻辑可概括为：**粗化 → 融合 → 稀疏提取 → 迭代扩展**，每一步都针对无监督 3D 实例分割中“特征噪声大、标注缺失”的核心瓶颈进行了定向设计。

## 核心模块与公式推导

UnScene3D 的核心管线由三个紧密耦合的模块构成：**几何基元提取与特征聚合**、**掩蔽归一化割伪掩码生成**、以及**基于 DropLoss 的自训练**。以下逐一展开其关键机制与数学形式。

### 场景图粗化：几何基元提取与特征聚合

为降低在高分辨率三维数据上直接操作的复杂度并正则化特征噪声，UnScene3D 首先将场景网格过分割为几何基元。给定输入网格图 $G = ( V , E )$（$V$ 为顶点集，$E$ 为三角形面边），采用 **Felzenswalb** 算法（基于图的高效图像分割方法）将具有相似法向量与颜色的邻接顶点聚类，得到基元集合 $\{S_N\} = \{C_1, \dots, C_N\}$（Section 3.1.3）。这一粗化步骤将后续计算从百万级顶点压缩至数百个基元节点，构成图上的超节点表示。

在此基础上，分别提取两类自监督特征并聚合到基元上（Section 3.1.1, 3.1.4）：
- **2D 颜色特征** $\mathcal{F}_{2D} \in \mathbb{R}^{N \times D_{2D}}$：来自 DINO 自监督模型在 RGB 图像上的逐像素特征，通过相机位姿投影至网格顶点，再在基元内平均池化；
- **3D 几何特征** $\mathcal{F}_{3D} \in \mathbb{R}^{N \times D_{3D}}$：来自 **CSC**（自监督 3D 预训练方法）在网格顶点上的特征，同样经基元聚合。

### 伪掩码生成：掩蔽归一化割

伪掩码生成的核心是在基元图上执行**迭代掩蔽归一化割**，以从多模态特征中提取稀疏但可靠的对象级区域。其数学基础是归一化割的特征值分解（Section 3.1.2）：

$$(D - W) v = \lambda D v$$

其中 $W$ 为邻接矩阵，$D$ 为度矩阵，$D(i,i) = \sum_j W(i,j)$。第二小特征向量 $v$ 指示最优二分割。

**多模态相似度融合**：对 2D 和 3D 特征分别计算相似度矩阵 $A_{2D}$ 和 $A_{3D}$，取加权平均得到最终相似度矩阵，再通过阈值 $\tau_{cut}$ 二值化以形成连通图（Algorithm 1）：

$$\mathcal{W}_{i,k} = \begin{cases} 1 & \text{if } \mathcal{W}_{i,k} \ge \tau_{cut} \\ \epsilon & \text{if } \mathcal{W}_{i,k} < \tau_{cut} \end{cases}$$

**迭代掩蔽过程**：每次归一化割后，提取第二小特征向量 $v_j$ 生成二值掩码 $m_j$。若 $m_j$ 包含多个物理分离的连通分量，仅保留包含特征向量中绝对值最大元素的分量 $\tilde{m}_j$，其余区域放回场景进行下一轮分割。如此迭代直至达到预设掩码数上限或无可分割区域，得到初始伪掩码集 $M^{0} = \{ m_i \}_{i=1}^{N_m}$（Section 3.1）。

### 自训练：DropLoss 与掩码增广

初始伪掩码 $M^0$ 虽稀疏，但为 3D Transformer 骨架提供了监督信号。自训练的关键在于**损失函数设计**与**伪掩码增广策略**。

**DropLoss 机制**（Section 7.2）：标准交叉熵与 Dice 损失的加权组合用于伪掩码的双边匹配，但伪掩码存在噪声与缺失标注。DropLoss 通过计算当前预测与上一轮伪标注的重叠度，仅保留重叠超过阈值 $\tau_{drop}$ 的预测区域参与反向传播，从而避免对未匹配区域的错误惩罚，使模型能够自主发现被遗漏的实例区域。消融实验证实，DropLoss 最终 AP 达到 15.9，显著优于标准损失（AP 14.2）和投影损失（AP 7.2）（Table 6）。

**掩码增广策略**（Table 8）：自训练中保持初始伪掩码 $M^0$ 固定不变，每轮迭代从模型预测中采样高置信度新掩码动态加入监督集，而非直接用上轮预测替换。这种策略在保持初始掩码相对清洁的同时，逐步扩展掩码覆盖密度，是最终性能饱和于第 4 轮（AP 从初始 5.9 提升至 15.9）的关键机制（Table 4, Figure 6）。

## 实验与分析

### 主结果：ScanNet 与 S3DIS 上的性能突破

UnScene3D 在标准室内数据集上实现了无监督三维实例分割的大幅性能跃升。在 ScanNet 验证集上，该方法取得了 **AP@25 58.5 / AP@50 32.2 / AP 15.9** 的成绩，相比传统聚类基线 Felzenswalb（AP 5.0）提升超过 **3 倍**（Table 1）。这一差距的核心来源并非单一模块，而是伪掩码生成与自训练两个阶段的协同：初始伪掩码本身已优于直接聚类方法，而自训练进一步将稀疏、粗糙的提案细化为密集、完整的实例分割。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/003_Table_1.jpg]]
*Table 1: Unsupervised class-agnostic 3D instance segmentation on ScanNet [10]. Our approach improves significantly over baselines (3x improvement in AP) due to our pseudo mask generation and self-training strategy*

在 S3DIS Area 5 上，UnScene3D 仅使用在 ScanNet 上预训练的 3D 特征，取得了 **AP@25 52.6 / AP@50 40.3 / AP 21.4**，显著超越先前无监督方法（Table 2）。这表明该方法具备跨数据集的泛化能力，无需针对新场景重新设计伪掩码生成策略。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/005_Table_2.jpg]]
*Table 2: Evaluation on S3DIS dataset (Area 5). UnScene3D is able to adapt to other datasets as well and shows a significant improvement over previous SOTA methods*

### 伪掩码生成：多模态融合的因果作用

伪掩码的质量直接决定了自训练的起点。Table 3 的消融揭示了模态选择的关键因果链路：

- **仅用 3D 几何特征**生成伪掩码，经过 4 轮自训练后 AP 为 13.3；
- **仅用 2D 颜色特征**（DINO 自监督特征投影到 3D），最终 AP 为 15.7；
- **融合两种模态**，最终 AP 达到 **15.9**。

值得注意的是，颜色特征**仅在初始伪掩码生成阶段使用**，自训练和测试阶段仅依赖 3D 特征。这意味着多模态融合的收益主要作用于伪掩码的初始质量——更准确的伪掩码为自训练提供了更可靠的监督信号，而非在推理时引入额外信息。Table 12 进一步证实，基于归一化割（NCut）的伪掩码生成在两种模态下均优于 FreeMask 的 3D 适应版本。

### 自训练的动态演化与饱和点

自训练是性能提升的另一个核心引擎。Table 4 追踪了从初始伪掩码到多轮迭代的性能轨迹：

- **初始伪掩码**（未经自训练）：AP 仅 5.9；
- **第 1 轮自训练**：AP 跃升至 10.4；
- **第 4 轮自训练**：AP 达到 15.9 并趋于饱和。

Figure 6 从可视化角度印证了这一趋势：随着自训练迭代，预测实例的数量逐步增加，掩码质量持续改善。饱和现象说明模型在现有伪掩码框架下已充分挖掘信息，进一步改进需要突破初始伪掩码的覆盖限制。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/010_Figure_6.jpg]]
*Figure 6: UnScene3D employs self-training to refine the initial sparse set of proposals. We can see consistent improvement over both the number of predicted instances and the quality of the instance masks. Here we show results using the pseudo annotations obtained from both modalities. Table 4. Multiple iterations of self-training significantly improve performance, saturating around 4 iterations*

### DropLoss：处理噪声监督的关键设计

自训练的核心挑战在于伪掩码存在噪声和遗漏标注。Table 6 对比了三种损失策略：

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/016_Table_6.jpg]]
*Table 6: A 3D projection loss struggles with under-determined associations, while DropLoss helps UnScene3D to discover parts of the scene that were missed by the source supervision. We report all metrics after a single iteration and the AP scores after 4 iterations of self-training. Table 7. Our pseudo mask generation quality, as measured by AP metrics, maintains robustness to a large range of τ thresholds that extract saliency. Note that this measures the quality of only the pseudo masks; our full approach with self-training produces significantly improved results. In this table we show results and parameters used by our method in bold and report pseudo mask performance generated from both modaliti...*

- **标准交叉熵 + Dice 损失**：AP 14.2；
- **投影损失（3D Projection Loss）**：AP 仅 7.2，因为未匹配区域的关联不确定；
- **DropLoss**：AP **15.9**，通过忽略与上轮标注重叠低于阈值 $\tau_{drop}$ 的预测区域，使模型能够发现伪掩码遗漏的实例区域。

这一结果揭示了无监督自训练中的一个关键原则：**选择性忽略不确定性区域比强制匹配所有预测更有效**。DropLoss 的机制本质上是让模型在“已知可靠”的区域学习，同时为“未知”区域保留探索空间。

### 伪掩码增强策略：固定初始掩码 + 动态添加

Table 8 检验了自训练中伪掩码的更新策略。直接使用上一轮预测作为下一轮监督会导致噪声累积；而**保持初始伪掩码固定，每轮动态添加高置信度新预测**（Mask Addition）在清洁度与覆盖率之间取得了最佳平衡。这一策略避免了初始稀疏但相对可靠的掩码被后续噪声预测污染。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/015_Table_8.jpg]]
*Table 8: Instead of using masks from previous iteration directly it is the best to keep the initial masks fixed, and iteratively sample plausible predictions to enrich the pseudo dataset during selftraining. This method strikes a balance between relatively clean, but sparse labels and increasing number of confident samples. Finally, even though Felzenswalb oversegmentation yields to higher precision, then our initial mask prediction algorithm, it also includes more background into the training, and this way plateauing at a lower self-training performance*

### 鲁棒性分析

UnScene3D 对关键超参数表现出良好的鲁棒性：

- **$\tau_{cut}$ 阈值**（Table 7）：在 0.4–0.8 范围内伪掩码质量保持稳定，最佳值为 0.65；
- **几何过分割参数**（Table 9）：方法对分割块大小和相似度度量具有较强鲁棒性，仅在分割块被约束过大时性能有所下降。此外，物理上分离的前景块独立处理对性能有益。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/018_Table_9.jpg]]
*Table 9: We denote the parameters used by our method in bold. We show that our method is robust to a wide range of numbers regarding segments sizes and different similarity metrics, and only degrades somewhat in performance when segments are constrained to be too large. We also show that the separation of physically distant foreground patches is important and it is beneficial to use the activation of the eigenvector for the best results. Finally, we show that denser initial mask predictions lead to quantitatively better initial pseudo annotations, and even better self-training performance after a single iteration, but underperforming in their final scores. This behaviour can be explained by the larg...*

### 失败模式与局限性

尽管整体性能显著领先，UnScene3D 存在以下已知失败模式：

1. **极小物体遗漏**：几何过分割可能导致非常小的物体（如笔、手机）在伪掩码生成阶段被忽略，因为基元粒度不足以捕获这些物体；
2. **网格表示依赖**：当前方法依赖网格图进行图粗化，限制了向原始点云或体素表示的扩展；
3. **固定初始掩码的噪声强化风险**：自训练过程中初始伪掩码集保持不变，可能强化某些噪声预测，尤其在初始掩码存在系统性偏差时。

### 预训练潜力

Table 5 和 Figure 4 展示了 UnScene3D 自训练产生的 3D 特征可作为强大的预训练策略。在有限标注数据场景下，UnScene3D 预训练显著优于自监督预训练方法 CSC，表明无监督实例分割任务本身能够学习到可迁移的 3D 表征。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/013_Table_5.jpg]]
*Table 5: Unsupervised class-agnostic pretraining with our method can also act as a powerful pretraining strategy, advancing over state of the art. We report pretraining with CSC [19] and UnScene3D, and evaluate the downstream weakly-supervised instance segmentation performance on ScanNet with percentage of limited annoated scenes used denoted in the top row. As we found that CSC degraded performance when using a transformer-based backbone, we also report the performance of training from scratch and CSC on their originally proposed backbone of a sparse UNet with bottom-up voting*

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/019_Table_10.jpg]]
*Table 10: 2D evaluation on ScanNet images. Table 11. UnScene3D achieves significantly better performance on ScanNet than SAM3D through our strong multi-modal reasoning*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2303_14541/figures/014_Table.jpg]]

## 方法谱系与知识库定位

### 核心设计理念与知识贡献

UnScene3D 的核心设计理念在于将**几何先验**与**多模态自监督特征**在统一的图表示上进行融合，以解决无监督三维实例分割中“从噪声数据中学习对象级推理”这一瓶颈。该方法并非简单地将二维无监督技术迁移到三维，而是通过三个关键机制构建了独特的知识贡献：

1. **几何基元粗化**：利用 Felzenswalb 过分割算法将网格顶点聚类为几何基元，将场景表示从百万级顶点压缩至千级基元。这一粗化不仅降低了归一化割的计算复杂度，更重要的是通过强制实例边界与基元边界对齐，有效正则化了自监督特征的噪声，避免了直接对点云操作时的碎片化分割。

2. **多模态归一化割伪掩码生成**：在几何基元图上，独立计算二维颜色特征（DINO）和三维几何特征（CSC）的相似度矩阵，通过加权平均融合后迭代应用归一化割，生成稀疏但高精度的初始伪掩码。消融实验（Table 3）证实，融合双模态的最终 AP 达到 15.9，优于仅使用三维特征（AP 13.3）或仅使用二维特征（AP 15.7），验证了颜色与几何信号的互补性。

3. **DropLoss 驱动的自训练**：针对伪掩码的噪声和缺失标注问题，采用 DropLoss 机制——仅保留与上一轮伪标注重叠超过阈值 $\tau_{drop}$ 的预测区域进行反向传播，允许模型在未匹配区域自由探索新实例。Table 6 显示，DropLoss（AP 15.9）显著优于标准交叉熵与 Dice 损失（AP 14.2）和投影损失（AP 7.2），证明其有效平衡了伪标注利用与新实例发现。

### 与现有工作的关系定位

**相对于传统聚类方法的突破**：传统方法如 **HDBSCAN**（基于密度聚类）和 **Felzenswalb**（基于图的过分割）直接对几何特征进行聚类，在杂乱室内场景中性能极差（ScanNet 上 Felzenswalb AP 仅 5.0）。UnScene3D 通过引入自监督深度特征和自训练机制，将 AP 提升至 15.9（超过 3 倍），证明了深度特征在对象级推理中的关键作用。

**相对于图割方法的改进**：**Nunes et al.** 采用图割和聚类细化进行无监督三维分割，但未利用多模态自监督特征。UnScene3D 在归一化割框架中融合了二维和三维自监督特征，并通过几何基元粗化提升了效率和鲁棒性，在 S3DIS Area 5 上 AP 达到 21.4，显著超越先前方法。

**相对于二维无监督方法的投影策略**：**CutLER** 作为二维无监督实例分割方法，通过投影到三维并聚合预测进行三维分割。然而，投影过程中的遮挡和深度不连续性导致实例边界模糊。UnScene3D 直接在三维网格上操作，利用几何基元保证边界清晰，定性结果（Figure 3）显示其掩码质量显著优于投影方法。

**相对于自监督预训练方法**：**CSC** 作为三维自监督预训练方法，提供了强大的几何特征。UnScene3D 将其作为特征提取器，但进一步通过自训练生成的伪标注进行微调，在数据高效预训练场景下（Table 5）显著超越单独使用 CSC 的性能，证明自训练过程本身能够产生更强的下游任务特征。

**相对于 SAM3D**：Table 11 显示 UnScene3D 在 ScanNet 上显著优于 SAM3D，这得益于其多模态推理能力——SAM3D 主要依赖二维基础模型的提示，而 UnScene3D 在三维几何基元上融合了互补的二维和三维信号。

### 适用边界与限制条件

**表示依赖性**：UnScene3D 的核心操作（几何基元提取、图粗化、归一化割）均建立在网格表示 $G = (V, E)$ 之上。对于原始点云或体素表示，需要额外的网格重建步骤，这可能引入几何误差并限制方法在 LiDAR 扫描等非网格数据上的直接应用。Table 9 显示方法对过分割参数（段大小、相似度度量）具有较强鲁棒性，但性能在段过大时有所下降，表明基元粒度需要与目标实例尺度匹配。

**小物体遗漏风险**：几何过分割倾向于将具有相似法线和颜色的顶点聚类，可能导致非常小的物体（如笔、手机）被合并到相邻的大型基元中，在伪掩码生成阶段即被遗漏。自训练机制虽然能够发现部分缺失实例，但无法恢复在初始阶段完全丢失的极小物体。

**伪掩码噪声强化**：自训练过程中保持初始伪掩码固定（Table 8 中的 Mask Addition 策略），虽然通过动态添加高置信度预测扩展了伪标注集，但固定的初始掩码可能包含噪声，在迭代中被模型学习并强化。Table 4 显示性能在第 4 轮后饱和（AP 15.9），暗示自训练的上限受限于初始伪掩码的质量。

**模态可用性约束**：二维颜色特征（DINO）仅在初始伪掩码生成阶段使用，自训练和测试阶段仅依赖三维几何特征。这意味着在颜色信息缺失或光照条件极差的场景中，初始伪掩码质量可能下降，进而影响最终性能。Table 3 中仅使用三维特征的最终 AP 为 13.3，显著低于双模态的 15.9，验证了颜色信号的重要性。

### 开放问题与未来方向

1. **跨表示泛化**：如何将基于网格的图粗化步骤扩展到原始点云或体素表示？可能的方案包括基于超点（superpoint）的图构建或可学习的粗化策略，但需要验证这些替代表示能否保持几何基元带来的边界正则化效果。

2. **小物体发现机制**：如何在伪掩码生成中显式建模多尺度信息，防止极小物体被遗漏？可能的改进包括多尺度几何基元提取或引入二维基础模型（如 SAM）的弱监督提示，但需要处理二维到三维投影的不确定性。

3. **动态伪掩码更新**：自训练过程中如何动态更新初始伪掩码以避免噪声强化？可能的方案包括基于预测置信度的掩码替换策略或在线伪标注清洗机制，但需要在伪标注纯度和完整性之间取得平衡。

4. **弱监督模型集成**：如何集成 SAM 等弱监督二维模型以增强多模态推理？Table 11 已初步比较了 SAM3D，但更深入的融合策略（如将 SAM 的掩码提议作为归一化割的初始分割）可能进一步提升性能。

5. **语义信息利用**：当前方法仅进行类无关实例分割，未利用语义信息。如何在无监督框架下同时实现实例和语义分割，或利用自监督特征中的语义线索进行实例分组，是值得探索的方向。

6. **计算效率优化**：归一化割的特征值分解在大规模场景中计算开销较大。如何通过近似算法或层次化图分割提升效率，使方法适用于更大规模的三维场景？

### 证据强度评估

- **高置信度结论**（confidence ≥ 0.95）：多模态融合优于单一模态（Table 3）、自训练显著提升性能并在 4 轮后饱和（Table 4）、DropLoss 优于标准损失（Table 6）、几何基元粗化对参数鲁棒（Table 9）、Mask Addition 策略优于直接使用上轮预测（Table 8）。这些结论由充分的消融实验支持。

- **中等置信度结论**（confidence 0.9）：伪掩码生成对 $\tau_{cut}$ 阈值鲁棒（Table 7）、在 ARKitScenes 上的泛化能力（Figure 7）。这些结论有实验支持但分析深度有限。

- **需手动验证的推断**：小物体遗漏的具体量化影响、自训练噪声强化的程度、跨数据集泛化的上限。这些方面在论文中未充分展开，需要进一步实验验证。

## 原文 PDF

![[paperPDFs/CVPR_2024/UnScene3D_Unsupervised_3D_Instance_Segmentation_for_Indoor_Scenes.pdf]]

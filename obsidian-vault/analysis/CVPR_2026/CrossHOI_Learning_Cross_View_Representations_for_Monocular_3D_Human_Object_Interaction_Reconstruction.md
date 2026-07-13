---
title: "CrossHOI: Learning Cross-View Representations for Monocular 3D Human-Object Interaction Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CrossHOI_Learning_Cross_View_Representations_for_Monocular_3D_Human_Object_Interaction_Reconstruction.pdf
project_link: null
code_link: "https://github.com/peigeng99/CrossHOI.git"
aliases:
- CrossHOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 从单张图像生成另一个新视角的图像特征，为单目重建补充空间几何信息；在初始重建、接触估计和网格优化全阶段引入跨视角融合机制，利用双视角互补特征增强对遮挡区域的感知与推理。
primary_logic: 利用预训练的跨视角生成器从单视角输入推断出另一视角的特征表示，通过空间跨视角融合增强初始重建，再借助双向跨视角Transformer融合多视角顶点特征，使模型能够在严重遮挡下更准确地预测接触区域并生成几何一致、物理合理的交互重建。
claims:
- 在BEHAVE和InterCap数据集上，CrossHOI在重建精度和接触预测方面全面超越现有SOTA方法（如CONTHO、HOI-TG），尤其在严重遮挡场景下提升显著。
- 消融实验证明，引入跨视角特征在初始重建和接触估计两个阶段均能带来增益，且双向交叉注意力融合策略在所有融合方式中表现最优，尤其对接触相关指标的提升幅度更大。
- BEHAVE 上 CD_human ↓ , CD_object ↓ , Contactp ↑ , Contactr ↑ = 4.27 / 7.68 / 0.687 / 0.576
- InterCap 上 CD_human ↓ , CD_object ↓ , Contactp ↑ , Contactr ↑ = 5.17 / 8.38 / 0.724 / 0.491
---

# CrossHOI: Learning Cross-View Representations for Monocular 3D Human-Object Interaction Reconstruction

> [!tip] 核心洞察
> 利用预训练的跨视角生成器从单视角输入推断出另一视角的特征表示，通过空间跨视角融合增强初始重建，再借助双向跨视角Transformer融合多视角顶点特征，使模型能够在严重遮挡下更准确地预测接触区域并生成几何一致、物理合理的交互重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | CrossHOI：学习跨视角表征的单目三维人-物交互重建 |
| 英文题名 | CrossHOI: Learning Cross-View Representations for Monocular 3D Human-Object Interaction Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Geng_CrossHOI_Learning_Cross-View_Representations_for_Monocular_3D_Human-Object_Interaction_Reconstruction_CVPR_2026_paper.html) · [Code](https://github.com/peigeng99/CrossHOI.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | CrossHOI |
| Dataset | BEHAVE, InterCap |

> [!tip] 效果简介
> - BEHAVE 上，CD_human ↓ , CD_object ↓ , Contactp ↑ , Contactr ↑ 4.27 / 7.68 / 0.687 / 0.576 (超越所有先前SOTA方法)。
> - InterCap 上，CD_human ↓ , CD_object ↓ , Contactp ↑ , Contactr ↑ 5.17 / 8.38 / 0.724 / 0.491 (超越所有先前SOTA方法)。

## 概要

单目三维人-物交互（HOI）重建的核心瓶颈在于**人与物的相互遮挡**：被遮挡区域的几何信息完全缺失，导致重建完整性不足，尤其是接触区域的估计极不准确。现有方法仅依赖单视角图像特征，缺乏对不可见空间关系的推理能力。

**CrossHOI** 的核心思路是**从单张图像生成另一个新视角的图像特征**，为单目重建补充空间几何先验，并在初始重建、接触估计和网格优化全阶段引入跨视角融合机制。具体而言，该方法利用预训练的跨视角生成器从原始视角推断出互补视角的特征表示，通过空间交叉注意力进行自适应融合以增强初始重建，再借助双向跨视角 Transformer 融合双视角的顶点特征，使模型能够在严重遮挡下更准确地预测接触区域并生成几何一致、物理合理的交互重建。

在 **BEHAVE** 和 **InterCap** 两个公开数据集上，CrossHOI 在重建精度（Chamfer 距离）和接触预测（精度与召回率）方面全面超越现有 SOTA 方法（如 **CONTHO**、**HOI-TG**），尤其在严重遮挡场景下提升显著。消融实验进一步验证了跨视角特征在初始重建和接触估计两个阶段均能带来增益，且双向交叉注意力融合策略在所有融合方式中表现最优。

### 单目三维人-物交互重建的核心瓶颈

单目三维人-物交互（Human-Object Interaction, HOI）重建的目标是从单张RGB图像中同时恢复出人体和物体的三维网格，并准确估计两者之间的接触关系。这一任务在增强现实、机器人操作理解和行为分析等领域具有广泛应用前景。然而，其核心挑战在于**人与物之间的相互遮挡**：当人手持或倚靠物体时，接触区域往往被遮挡，导致单视角图像中不可见区域的几何信息严重缺失。这使得重建的完整性和接触估计的准确性都面临根本性困难。

现有方法——如基于预定义物理约束的**PHOSA**（Zhang et al., ECCV 2020）、使用隐式表面表示的**CHORE**（Xie et al., ECCV 2022）、基于接触引导细化的**CONTHO**（Nam et al., CVPR 2024）以及引入图感知Transformer的**HOI-TG**（Wang et al., CVPR 2025）——均仅依赖单视角图像特征进行重建。在严重遮挡场景下，这些方法无法有效推理被遮挡的接触点和空间关系，导致接触区域估计失败和网格穿透等几何不一致问题。

### 跨视角信息的关键作用

本文的核心洞察在于：**从单目图像中生成另一个视角的特征表示，可以为遮挡区域提供互补的空间几何信息**。这一思想源自一个直观观察——当人从一个视角观察交互场景时，被遮挡的接触区域在另一个视角下往往是可见的。因此，若能通过生成式建模从单视角输入推断出另一视角的图像特征，并在重建的全流程中加以利用，就有可能在无需额外输入的前提下，显著增强模型对遮挡区域的感知与推理能力。

具体而言，本文提出**CrossHOI**框架，通过三个层面的跨视角融合来系统性地解决上述瓶颈：

1. **特征生成层面**：设计一个预训练的跨视角生成器，从单张图像推断出另一视角的图像特征，在特征层面补充空间几何先验。
2. **初始重建层面**：通过空间跨视角特征融合模块，自适应地聚合原始视角与生成视角的互补线索，增强初始人体网格与物体位姿的估计质量。
3. **接触估计与细化层面**：引入双向跨视角Transformer，在顶点级别融合双视角特征，使模型能够在严重遮挡下更准确地预测接触区域，并生成几何一致、物理合理的最终重建。

这一跨视角表征学习范式，为单目HOI重建中“从不可见到可见”的推理提供了新的技术路径。

## 核心方法与创新机理

CrossHOI 的核心创新在于**从单张图像显式生成另一视角的特征表示，并将跨视角互补信息系统性地注入到三维人-物交互重建的全流程中**。与现有方法仅依赖单视角特征进行重建不同，CrossHOI 通过“生成—融合—细化”三阶段机制，使模型能够在严重遮挡下感知被遮挡的接触区域和空间几何关系。

### 创新一：跨视角生成器——从单目输入推断新视角特征

**Changed Slot：初始重建的图像特征来源**

- **Baseline 做法**：现有方法（如 **CONTHO** (Nam et al., CVPR 2024)、**HOI-TG** (Wang et al., CVPR 2025)）仅从当前单视角图像的 CNN 特征出发进行重建，无法获取被遮挡区域的几何信息。
- **CrossHOI 做法**：设计一个预训练的**跨视角生成器（Cross-view Generator）**，以当前视角的图像特征为输入，通过交叉注意力机制生成另一视角的图像特征。生成器将相机内参嵌入作为位置偏置，使特征具备几何感知能力：

$$E_{K_A} = \mathbf{MLP}( \mathbf{Flatten}(K_A) )$$

$$\tilde{F}_A = F_A^t + E_{K_A}$$

$$F_B' = \mathrm{CrossAttn}(\tilde{F}_A, T_{KV})$$

其中 $T_{KV}$ 为可学习的键/值令牌，用于将源视角特征映射为目标视角特征。训练时通过结合 MSE 和余弦相似度的映射损失 $\mathcal{L}_{\mathrm{map}}$ 约束生成特征与真实目标视角特征的对齐。

**因果机制**：生成器从多视角数据中学习到视角变换的先验知识，在推理时无需额外输入即可为单目重建补充空间几何信息。实验表明，生成的跨视角特征与真实目标视角特征的平均余弦相似度达到 **0.784**，类别间 MMD 值低于 **0.05**，验证了生成特征的有效性和分布一致性。

### 创新二：全阶段跨视角融合——从图像级到顶点级的双视角互补

**Changed Slot：接触估计中的顶点特征表示**

- **Baseline 做法**：现有方法仅从当前视角的图像平面采样单组顶点特征用于接触预测。
- **CrossHOI 做法**：在初始重建、接触估计和网格细化三个阶段均引入跨视角融合机制：

1. **图像级融合（初始重建阶段）**：通过**空间跨视角特征融合模块**，以原始视角特征为查询、生成视角特征为键/值，利用空间交叉注意力自适应聚合互补信息：

$$F_{AB} = \mathrm{Softmax}\left(\frac{Q_A K_B^{\top}}{\sqrt{d}}\right) V_B + F_A$$

残差连接保留了原始表征，同时选择性注入了新视角的几何线索。

2. **顶点级融合（接触估计阶段）**：将初始网格的顶点分别投影到两个视角的特征图上，采样得到两组与视角相关的顶点特征，再通过**双向跨视角 Transformer** 进行融合：

$$\hat{F}_{vA} = \mathrm{Softmax}\left(\frac{Q_{vA} K_{vB}^{\top}}{\sqrt{d_v}}\right) V_{vB} + F_{vA}$$

$$\hat{F}_{vB} = \mathrm{Softmax}\left(\frac{Q_{vB} K_{vA}^{\top}}{\sqrt{d_v}}\right) V_{vA} + F_{vB}$$

双向交叉注意力使每个视角的顶点特征都能从另一视角获取互补信息，从而更准确地预测人-物接触概率。

3. **接触引导的细化阶段**：利用预测的接触图加权选择接触相关顶点特征，再次通过双向交叉注意力融合后回归每个顶点的偏移量，得到最终的人体和物体网格。

**因果机制**：单视角下被遮挡的接触点在另一视角中可能可见，跨视角顶点特征融合使模型能够“看到”原本不可见的区域，从而提升接触估计的精度和召回率。

### 消融验证的关键结论

- **双向融合优于单向**：双向顶点特征融合 (A↔B) 在重建和接触估计上均优于单向融合（A→B 或 B→A）以及无融合，验证了双向互补信息的必要性。
- **交叉注意力融合最优**：在初始重建阶段，基于交叉注意力的图像特征融合方式优于直接相加、拼接+MLP 和加权求和，尤其对接触相关指标的提升幅度更大。
- **全阶段注入收益最大**：在初始重建和接触估计两个阶段同时引入跨视角特征对整体性能提升最大；单独在其中任一阶段加入也能带来收益。
- **遮挡场景增益显著**：在严重遮挡的 500 张样本上，CrossHOI 相较 CONTHO 基线在接触估计精度和召回率上分别提升 **5.6pp** 和 **6.1pp**，重建误差也显著降低。

CrossHOI的整体流程围绕一个核心思想展开：**从单张RGB图像中生成另一个视角的图像特征，并在重建的多个阶段引入跨视角融合，以弥补单目输入中被遮挡区域的几何信息缺失**。如图2所示，整个框架由一条从图像到网格的级联通路构成，包含预训练的跨视角生成器、初始重建模块、顶点特征采样与融合模块，以及接触引导的跨视角细化模块。

**输入与特征提取。** 给定单张图像 $I_A$ 及其相机内参 $K_A$，首先使用CNN骨干网络提取原始视角的图像特征 $F_A$。同时，相机内参通过一个小型MLP映射为与特征等维度的嵌入向量 $E_{K_A}$，作为位置偏置加到展平后的特征token上，形成几何感知的查询特征 $\tilde{F}_A$。这一设计使后续的跨视角映射能够显式地利用相机几何信息，而非仅依赖外观特征。

**跨视角生成器（预训练）。** $\tilde{F}_A$ 被送入一个轻量级的跨视角生成器——该生成器由一组可学习的键/值令牌 $T_{KV}$ 和交叉注意力层构成，将源视角特征映射为目标视角特征 $F_B'$。生成器在BEHAVE和InterCap等多视角数据集上离线预训练，训练目标同时约束MSE损失和余弦相似度损失，使 $F_B'$ 在数值和方向上均与真实目标视角特征 $F_B$ 对齐。推理时，生成器仅需单张图像输入即可产生互补视角的特征，无需额外的视角标注或图像。

**空间跨视角特征融合与初始重建。** 获得双视角特征 $F_A$ 与 $F_B'$ 后，框架通过空间交叉注意力对二者进行自适应融合：以 $F_A$ 为查询、$F_B'$ 为键/值，计算注意力权重后选择性地注入互补信息，并通过残差连接保留原始表征，得到融合特征 $F_{AB}$。该融合特征随后输入初始重建模块，同时回归人体参数（SMPL+H模型）和物体的6DoF位姿，构建初始的3D人体网格 $M_{init}^h$ 与物体网格 $M_{init}^o$。

**顶点特征采样与双向跨视角融合。** 初始网格的顶点被分别投影到 $F_A$ 和 $F_B'$ 的特征图上，通过网格采样收集各视角的顶点视觉特征，并与顶点坐标拼接，形成两组视角相关的顶点表示 $F_{vA}$ 和 $F_{vB}$。随后，一个双向跨视角Transformer对两组顶点特征执行交叉注意力：$F_{vA}$ 以 $F_{vB}$ 为上下文增强自身，反之亦然。这种双向融合策略使得每个视角的顶点都能从另一视角获取被遮挡区域的互补信息，从而更准确地预测人-物接触概率图。

**接触引导的跨视角细化。** 预测的接触图被用于加权选择接触相关的顶点特征，这些特征再次通过双向交叉注意力进行融合。融合后的表示经MLP回归出人体和物体的逐顶点偏移量 $\Delta M^h$、$\Delta M^o$，最终通过 $M_{final}^h = M_{init}^h + \Delta M^h$ 和 $M_{final}^o = M_{init}^o + \Delta M^o$ 得到细化后的网格。整个框架以初始重建损失、接触估计损失和细化损失之和作为总训练目标，实现多阶段联合优化。

**关键设计选择。** 跨视角特征在初始重建和接触估计两个阶段均被引入，消融实验表明这种全阶段融合策略带来的增益最大。在顶点融合层面，双向交叉注意力（A↔B）在所有融合方向中表现最优，尤其在接触相关指标上提升显著，验证了双视角互补信息对于遮挡场景下接触推理的关键作用。

![[assets/figures/papers/paper_list_l1012_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_CrossHOI_Learning/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of the proposed CrossHOI. Image features*

CrossHOI 围绕“从单视角推断互补视角特征”这一核心思想，构建了三个紧密协作的关键模块：**跨视角生成器**、**空间跨视角特征融合**以及**双向跨视角 Transformer**。以下逐一解析其设计逻辑与核心公式。

### 跨视角生成器（Cross-view Generator）

该模块的目标是：给定视角 A 的图像特征 $F_A$ 及其相机内参 $K_A$，生成视角 B 的图像特征 $F_B'$，从而为单目重建补充被遮挡区域的几何先验。其设计包含两个关键步骤。

**几何感知特征嵌入。** 为使生成器感知视角变换的几何约束，首先将相机内参矩阵 $K_A$ 展平后通过 MLP 映射为与图像特征同维度的嵌入向量：

$$E_{K_A} = \mathbf{MLP}(\mathbf{Flatten}(K_A)) \tag{1}$$

该嵌入作为位置偏置加到展平后的图像特征每个 token 上，得到几何感知的查询特征：

$$\tilde{F}_A = F_A^t + E_{K_A} \tag{2}$$

**跨视角特征映射。** 以几何感知特征 $\tilde{F}_A$ 作为查询，通过交叉注意力与一组可学习的键/值令牌 $T_{KV}$ 交互，生成目标视角特征：

$$F_B' = \mathrm{CrossAttn}(\tilde{F}_A, T_{KV}) \tag{3}$$

其中 $T_{KV}$ 在训练时从目标视角 $I_B$ 及其相机参数初始化，使生成器学会视角间的特征对应关系。训练损失从数值和方向两个层面约束生成特征与真实目标特征 $F_B$ 的对齐：

$$\mathcal{L}_{\mathrm{map}} = \lambda_1 \|F_B' - F_B\|_2^2 + \lambda_2(1 - \cos(F_B', F_B)) \tag{4}$$

该生成器离线预训练，推理时无需额外输入，仅从单张图像即可推断出新视角特征。

### 空间跨视角特征融合（Spatial Cross-view Feature Fusion）

获得双视角特征 $F_A$ 和 $F_B'$ 后，初始重建阶段需要自适应地聚合互补信息。CrossHOI 采用空间交叉注意力实现融合，以视角 A 的特征为查询、视角 B 的特征为键/值，选择性注入互补线索，并通过残差连接保留原始表征：

$$F_{AB} = \mathrm{Softmax}\left(\frac{Q_A K_B^{\top}}{\sqrt{d}}\right) V_B + F_A \tag{5}$$

消融实验（Table 3）表明，该交叉注意力融合方式在接触相关指标上的提升幅度明显大于直接相加、拼接+MLP 和加权求和等替代方案，验证了自适应选择性聚合对遮挡区域感知的重要性。

### 双向跨视角 Transformer（Bidirectional Cross-view Transformer）

初始重建完成后，需要从双视角特征中提取顶点级信息以进行接触估计和网格细化。首先将初始人体与物体网格的顶点分别投影到两个视角的特征图上，通过网格采样获得两组视角相关的顶点特征 $F_{vA}$ 和 $F_{vB}$，并与顶点坐标拼接。

随后，双向跨视角 Transformer 以交叉注意力实现双视角顶点特征的相互增强。视角 A 从视角 B 获取上下文：

$$\hat{F}_{vA} = \mathrm{Softmax}\left(\frac{Q_{vA} K_{vB}^{\top}}{\sqrt{d_v}}\right) V_{vB} + F_{vA} \tag{6}$$

对称地，视角 B 从视角 A 获取上下文：

$$\hat{F}_{vB} = \mathrm{Softmax}\left(\frac{Q_{vB} K_{vA}^{\top}}{\sqrt{d_v}}\right) V_{vA} + F_{vB} \tag{7}$$

融合后的特征用于预测人-物接触概率图。在细化阶段，利用预测的接触图加权选择接触相关顶点特征，再次通过双向交叉注意力融合后，回归每个顶点的偏移量，以残差形式修正初始网格：

$$M_{\mathrm{final}}^h = M_{\mathrm{init}}^h + \Delta M^h \tag{8}$$

$$M_{\mathrm{final}}^o = M_{\mathrm{init}}^o + \Delta M^o \tag{9}$$

消融实验（Table 2）证实，双向融合（A↔B）在重建精度和接触估计上均优于单向融合（A→B 或 B→A）以及无融合方案，说明双视角信息的对称互补对遮挡场景下的接触推理至关重要。

### 多阶段联合优化

整个框架的端到端训练目标为三个阶段的损失之和：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{init}} + \mathcal{L}_{\mathrm{est}} + \mathcal{L}_{\mathrm{ref}} \tag{10}$$

其中 $\mathcal{L}_{\mathrm{init}}$ 监督初始人体参数与物体位姿，$\mathcal{L}_{\mathrm{est}}$ 监督接触概率图，$\mathcal{L}_{\mathrm{ref}}$ 监督顶点偏移。跨视角生成器在此阶段冻结，仅作为特征提取器参与前向传播。

## 实验与关键发现

### 整体性能对比

CrossHOI在BEHAVE和InterCap两个主流多视角HOI数据集上与一系列代表性方法进行了全面对比，评估指标涵盖重建精度（CD_human和CD_object，越低越好）与接触估计质量（Contact_p精度和Contact_r召回率，越高越好）。对比基线包括基于物理约束的早期方法**PHOSA**（Zhang et al., ECCV 2020）、隐式表面联合重建方法**CHORE**（Xie et al., ECCV 2022）、基于接触细化Transformer的**CONTHO**（Nam et al., CVPR 2024），以及引入图感知Transformer的端到端框架**HOI-TG**（Wang et al., CVPR 2025）。

如Table 1所示，CrossHOI在两个数据集上全面超越所有先前方法。在BEHAVE数据集上，CrossHOI的人体重建Chamfer距离降至4.27，物体重建Chamfer距离降至7.68，接触精度和召回率分别达到0.687和0.576；在InterCap数据集上，四项指标分别为5.17、8.38、0.724和0.491。值得注意的是，CrossHOI在接触相关指标上的提升幅度尤为显著，验证了跨视角融合机制对遮挡区域接触推理的有效性。

### 消融实验

#### 顶点特征融合策略

双向跨视角Transformer的融合方向对性能有显著影响。Table 2对比了无融合、单向融合（A→B或B→A）和双向融合（A↔B）四种策略。结果表明，双向融合在所有指标上均取得最优结果：相比无融合基线，接触精度和召回率分别获得大幅提升，同时重建误差也有明显下降。单向融合虽然也能带来增益，但效果明显弱于双向方案，这验证了双视角互补信息在顶点级特征交互中的必要性。Figure 6的定性对比进一步显示，单向融合在遮挡严重区域仍会出现接触预测失败（红色圆圈标注），而双向融合能够更完整地恢复接触关系。

#### 图像特征融合方式

在初始重建阶段，跨视角图像特征的融合方式对性能有重要影响。Table 3对比了直接相加、拼接+MLP、加权求和和交叉注意力四种融合策略。基于交叉注意力的空间融合在所有指标上均取得最优结果，且接触相关指标（Contact_p和Contact_r）的提升幅度明显大于整体重建指标（CD_human和CD_object）。这一差异表明，交叉注意力机制能够自适应地选择性地注入互补视角的几何信息，对接触区域的感知尤为关键，而简单的线性融合方式难以有效利用跨视角特征中的空间对应关系。

#### 跨视角特征在各阶段的贡献

Table 4的消融实验系统分析了跨视角特征在初始重建阶段和接触估计/细化阶段分别引入时的效果。以CONTHO作为基线，仅在其中任一阶段加入跨视角特征均能带来性能提升，但同时在两个阶段引入跨视角特征时整体性能达到最优。这一结果揭示了跨视角几何先验在全流程中的累积增益效应：初始重建阶段的跨视角融合为后续提供了更准确的网格初始化，而顶点融合阶段的跨视角特征则直接增强了对遮挡接触区域的推理能力。

#### 严重遮挡场景分析

为验证方法在核心瓶颈场景下的有效性，实验从BEHAVE数据集中筛选了500张严重遮挡样本进行专项评估（Table 5）。以CONTHO为基线，CrossHOI在接触估计精度和召回率上分别提升5.6个百分点和6.1个百分点，重建误差也显著降低。这一结果直接验证了论文的核心动机——跨视角特征能够有效补充被遮挡区域的缺失几何信息，使模型在极富挑战性的遮挡条件下仍能准确推断接触关系。

### 跨视角生成器质量验证

预训练跨视角生成器的输出质量是后续所有融合阶段的基础。Figure 4展示了生成特征与真实目标视角特征之间的余弦相似度分布，平均相似度达到0.784，表明生成器能够有效学习视角间的特征映射。Figure 5进一步从分布层面分析了生成特征与真实特征的一致性，各类别物体的MMD（Maximum Mean Discrepancy）值均低于0.05，说明生成特征在分布层面与真实跨视角特征高度一致，为下游任务提供了可靠的几何先验。

### 定性对比

Figure 7展示了CrossHOI与HOI-TG和CONTHO在BEHAVE和InterCap数据集上的定性对比。在存在严重人与物相互遮挡的场景中，HOI-TG和CONTHO往往在接触区域出现明显的预测失败（红色圆圈标注），表现为人体穿透物体或接触点偏移。CrossHOI借助双视角互补特征，能够更准确地恢复接触几何，生成物理上更合理的交互姿态。这一定性结果与定量指标相互印证，进一步支持了跨视角融合机制在遮挡推理中的核心作用。

### 失败模式与局限性

尽管CrossHOI在两个基准数据集上取得了全面领先，论文仍指出了若干局限。首先，跨视角生成器的训练依赖多视角数据集（如BEHAVE、InterCap），在缺少多视角标注的场景下泛化能力有限。其次，物体重建仍然基于预定义的离散物体模板，无法处理未知类别或非刚性物体。此外，方法目前仅在室内固定物体的交互场景下验证，在开放世界、动态物体和复杂背景下的表现尚未评估。最后，虽然生成器本身是轻量的，但整体框架相比单视角方法增加了额外的特征生成与融合模块，实时性未作详细讨论，这在实际部署中可能需要进一步优化。

![[assets/figures/papers/paper_list_l1012_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_CrossHOI_Learning/figures/004_Table_1.jpg]]
*Table 1: Comparison of reconstruction quality*

![[assets/figures/papers/paper_list_l1012_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_CrossHOI_Learning/figures/008_Table_2.jpg]]
*Table 2: Comparison of different vertex feature fusion strategies on the BEHAVE dataset*

![[assets/figures/papers/paper_list_l1012_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_CrossHOI_Learning/figures/010_Table_3.jpg]]
*Table 3: Comparison of different image feature fusion methods on the BEHAVE dataset*

![[assets/figures/papers/paper_list_l1012_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_CrossHOI_Learning/figures/009_Table_4.jpg]]
*Table 4: Impact of cross-view features at each stage. Baseline refers to CONTHO [28]. ∗ indicates our reimplementation*

![[assets/figures/papers/paper_list_l1012_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_CrossHOI_Learning/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative comparison of human-object contact estimation with HOI-TG and CONTHO on the BEHAVE dataset (left) and InterCap dataset (right). Red circles indicate regions of contact prediction failure*

## 定位与知识库关联

### 1. 方法沿革与关系定位

CrossHOI 处于单目三维人-物交互（HOI）重建这一研究脉络中，其核心推进在于将“跨视角几何推理”引入原本仅依赖单视角特征的重建流程。为理解这一贡献的坐标，有必要梳理其与前序工作的关系。

**早期物理约束范式。** 以 **PHOSA**（Zhang et al., ECCV 2020）为代表的方法，通过在优化过程中施加预定义的物理约束（如穿透惩罚、接触力等）来获得几何上更合理的人-物交互。这类方法不显式学习接触模式，而是依赖手工设计的先验，因此在复杂遮挡和多样化交互下的泛化能力受限。

**隐式表示与端到端重建。** **CHORE**（Xie et al., ECCV 2022）采用隐式表面表示同时重建人与物体，摆脱了对显式模板的部分依赖。然而，该方法仍从单视角图像特征出发，未显式建模被遮挡区域的几何补全问题，导致在严重遮挡场景下重建完整性不足。

**接触感知的Transformer细化。** **CONTHO**（Nam et al., CVPR 2024）引入了基于接触的细化Transformer，将接触估计与网格优化耦合，显著提升了接触区域的重建精度。**HOI-TG**（Wang et al., CVPR 2025）进一步引入图感知Transformer来增强接触建模，是端到端HOI重建的强基线。但二者均仅从当前视角的图像特征中采样顶点特征，当接触区域因遮挡而不可见时，缺乏来自其他视角的互补信息来推理被遮挡的接触点。

**CrossHOI的方法学突破**在于将上述“单视角特征→单组顶点特征”的范式，改造为“单视角输入→双视角特征生成→双向顶点融合”的跨视角框架。其关键推进点有二：
1. **跨视角生成器**：从单张图像推断另一视角的图像特征，在特征层面为单目重建补充空间几何信息，而不依赖额外的推理输入。
2. **全阶段跨视角融合**：在初始重建、接触估计和网格细化三个阶段均引入双视角特征的融合机制，使模型能在严重遮挡下更准确地感知接触区域并生成几何一致的重建。

从方法论谱系看，CrossHOI 可视为在 CONTHO 和 HOI-TG 的接触感知重建框架之上，引入了跨视角特征生成与双向融合这一新的维度。其并非替代接触建模本身，而是为接触建模提供了更丰富、更完整的顶点特征表示。

### 2. 适用边界与能力约束

CrossHOI 的适用性受以下边界条件约束，这些约束源于其方法设计中的结构性假设：

**多视角训练数据依赖。** 跨视角生成器的训练需要成对的多视角图像特征作为监督（通过 MSE 与余弦相似度损失对齐生成特征与真实目标视角特征）。当前训练依赖 BEHAVE 和 InterCap 这类多视角数据集。在缺乏多视角标注的场景下，生成器的训练无法进行，方法的泛化能力受限。这是该方法最核心的部署约束。

**固定物体模板假设。** 物体重建仍基于预定义的离散物体模板（如椅子、桌子等固定类别），通过回归 6DoF 位姿来放置模板网格。这意味着 CrossHOI 无法重建未知类别或非刚性物体。对于开放世界中的任意物体交互，该方法需要额外的物体类别识别与模板匹配模块。

**室内静态场景验证。** 当前实验验证集中于室内固定物体的交互场景（BEHAVE 中的椅子、桌子等；InterCap 中的类似设置）。在动态物体、复杂背景或室外场景下的表现尚未评估。

**相机内参依赖。** 几何感知特征 $ \tilde{F}_A = F_A^t + E_{K_A} $ 的构建依赖相机内参矩阵 $ K_A $ 作为位置偏置。在缺乏相机内参的普通单目图像上，该机制的有效性如何维持是一个待验证的问题。

**实时性未讨论。** 虽然跨视角生成器被描述为“轻量”，但整体框架相比单视角方法增加了特征生成、空间融合和双向Transformer等模块。论文未提供推理延迟的定量分析，实时应用场景下的可行性需要进一步评估。

### 3. 局限性与已知失效模式

**跨视角生成器的分布外泛化。** 生成器在训练视角分布内表现良好（平均余弦相似度 0.784，类别间 MMD < 0.05），但在极端视角差异（如 360° 旋转）下的生成质量可能显著下降。论文未测试生成器在训练集视角范围之外的泛化能力。

**接触估计的边界模糊性。** 尽管 CrossHOI 在接触精度和召回率上全面超越 SOTA，但 Contact_r 在 InterCap 上仅为 0.491，意味着仍有超过一半的真实接触顶点未被正确预测。在严重遮挡的 500 样本子集上，虽然相对基线提升显著（+5.6pp Contact_p，+6.1pp Contact_r），但绝对数值仍表明接触估计是开放挑战。

**物体重建精度相对滞后。** 在 BEHAVE 上 CD_object（7.68）明显高于 CD_human（4.27），在 InterCap 上同样如此（8.38 vs 5.17）。这反映物体重建精度仍是瓶颈，可能与物体模板的刚性假设以及物体纹理/几何特征的稀疏性有关。

**双向融合并非无成本。** 消融实验（Tab. 2）显示，单向融合（A→B 或 B→A）在部分指标上已接近双向融合的效果，表明在某些场景下双向融合带来的额外计算可能边际收益有限。

### 4. 开放问题与后续方向

**无相机内参场景的适配。** 当输入为普通单目图像（无标定信息）时，几何感知特征 $ E_{K_A} $ 的构建机制失效。一个自然的问题是：能否通过自监督学习从图像中隐式推断相机参数，或设计不依赖显式内参的几何编码方案？

**跨视角生成的少样本/自监督学习。** 当前生成器需要成对的多视角特征进行监督训练。能否从更少的视角对，甚至通过自监督方式（如基于3D一致性的循环一致性约束）学到有效的视角变换？这将显著降低数据采集成本。

**超越模板的物体重建。** 将跨视角融合策略与基于隐式场或高斯泼溅的物体重建方法结合，有望突破固定模板的限制，实现对未知类别物体的3D交互重建。

**时序扩展。** 当前方法处理单帧图像。在视频序列中，时序信息可以提供额外的跨视角线索（如物体旋转带来的自遮挡解除），将跨视角生成与时序融合结合是一个有前景的方向。

**极端视角差异下的鲁棒性。** 系统评估跨视角融合策略在 360° 旋转、大基线视角差异下的稳定性，并设计针对性的鲁棒训练策略，是推动该方法走向实际部署的关键步骤。

## 原文 PDF

![[paperPDFs/CVPR_2026/CrossHOI_Learning_Cross_View_Representations_for_Monocular_3D_Human_Object_Interaction_Reconstruction.pdf]]

---
title: Deep Deformable 3D Caricatures With Learned Shape Control
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Deep_Deformable_3D_Caricatures_With_Learned_Shape_Control.pdf
project_link: "https://ycjungsubhuman.github.io/DeepDeformable3DCaricatures"
code_link: "https://github.com/ycjungSubhuman/DeepDeformable3DCaricatures"
aliases:
- DD3CMSMH
- DD3CLSC
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将3D形状建模为固定模板上的连续位移函数，并使用超网络（hypernetwork）根据潜在码生成SIREN MLP的权重，从而在保留模板细节的同时捕捉复杂的形状变化。
primary_logic: 通过学习一个由超网络参数化的连续模板变形函数，可以在紧凑的潜在空间中有效表达3D漫画的高度夸张和多样性，并为编辑任务提供便利的控制。
claims:
- SIREN MLP hypernetwork模型在测试集上的重建误差为0.017，而顶点位置数组MLP为0.031，且收敛更快（Fig.5）。
- SDF-based方法（DeepSDF，DIF-Net）重建的整体形状合理但丢失了眼睛和嘴部等关键细节（Fig.6）。
- Ablation研究表明，超网络架构相比潜在码拼接能提供更低的训练误差和更快的收敛（Fig.7）。
- 3DCaricShop test set (registered meshes) 上 mean l2 reconstruction error (per-vertex) = 0.017
---

# Deep Deformable 3D Caricatures With Learned Shape Control

> [!tip] 核心洞察
> 通过学习一个由超网络参数化的连续模板变形函数，可以在紧凑的潜在空间中有效表达3D漫画的高度夸张和多样性，并为编辑任务提供便利的控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于学习形状控制的深度可变形3D漫画 |
| 英文题名 | Deep Deformable 3D Caricatures With Learned Shape Control |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://ycjungsubhuman.github.io/DeepDeformable3DCaricatures/) · [Project](https://ycjungsubhuman.github.io/DeepDeformable3DCaricatures) · [Code](https://github.com/ycjungSubhuman/DeepDeformable3DCaricatures) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Deep Deformable 3D Caricature Model (SIREN MLP Hypernetwork) |
| Dataset | 3DCaricShop test set |

> [!tip] 效果简介
> - 3DCaricShop test set (registered meshes) 上，mean l2 reconstruction error (per-vertex) 0.017 vs 0.031 (Vertex position array MLP) (-0.014)。

## 概要

3D漫画形状具有高度夸张和多样性，但数据稀疏（约1400个注册网格），传统线性模型（如3DMM）难以同时保留细节并适应大变形，而隐式SDF方法会丢失眼睛、嘴部等关键特征。本文提出一种基于学习的深度可变形3D漫画模型，核心思路是将3D形状建模为固定模板表面上的连续位移函数：用一个超网络（hypernetwork）根据128维潜在码生成SIREN MLP的全部权重与偏置，再由该SIREN MLP将模板上的3D点映射为位移向量。这一“超网络+SIREN”的自动解码器架构在紧凑的潜在空间中有效捕捉了漫画的夸张形变，同时保留了模板细节。在3DCaricShop测试集上，该方法的重建误差为0.017，显著优于顶点位置数组MLP（0.031）和DeepSDF、DIF-Net等SDF基线。此外，该模型支持语义编辑和点控编辑等应用，为3D漫画的生成与编辑提供了数据驱动的形变空间。

## 核心方法与创新机理

### 问题瓶颈与设计动机

3D漫画建模面临一个核心矛盾：漫画形状具有高度多样性和夸张变形（如超大鼻子、极度拉伸的下巴），但可用的3D漫画数据却极为稀疏（约1400个注册网格）。传统的线性模型（如3DMM）受限于低维线性空间，无法表达漫画中强烈的非线性变形；而隐式SDF方法（如DeepSDF、DIF-Net）虽然能重建整体形状，却丢失了眼睛、嘴部等关键细节。另一方面，直接输出顶点位置数组的MLP在稀疏数据下收敛缓慢且泛化能力差——测试集重建误差高达0.031。

本文的核心洞察是：**将3D漫画建模为固定模板表面上的连续位移函数，并通过超网络（hypernetwork）根据潜在码生成该函数的网络权重**，从而在保留模板细节的同时，用紧凑的潜在空间捕捉复杂的形状变化。

### 形状表示：连续位移函数

方法的关键创新在于改变了3D形状的表示方式（changed slot 1）。传统方法将形状表示为顶点位置数组或隐式SDF场，而本文提出在**固定模板网格**上学习一个连续位移函数。给定模板表面上的一个3D点 $\hat{p}$，SIREN MLP $S$ 输出一个3D位移向量，最终的变形模型定义为：

$$D(\hat{p}, z) = S(\hat{p}, H(z)) + \hat{p}$$

其中 $H$ 是超网络，$z \in \mathbb{R}^{128}$ 是潜在码。这个公式的含义是：对模板上的每个点，先通过SIREN MLP计算位移，再将位移加回原点得到变形后的位置。该表示具有三个关键优势：

1. **细节保留**：模板网格本身携带了眼睛、嘴部等精细几何结构，位移函数只需学习变形量，而非从头生成几何。
2. **连续性**：SIREN MLP（使用周期性激活函数）建模的是连续函数，因此即使在模板的大三角形内部也能产生平滑形状（图8验证了这一点）。
3. **分辨率无关**：推理时可在模板表面任意采样，生成不同分辨率的网格（从约1.1万顶点到约74万顶点均可）。

### 网络架构：超网络条件化

第二个关键设计是网络的条件化机制（changed slot 2）。传统自动解码器将潜在码拼接到MLP的输入或中间特征层，但本文观察到这种方式收敛极慢。替代方案是使用**超网络架构**：超网络 $H$ 接收潜在码 $z$，输出SIREN MLP $S$ 的所有权重和偏置。

超网络由多个ReLU MLP分支组成，每个分支负责生成SIREN MLP中一个层的参数。SIREN MLP本身采用5层结构，每层使用正弦激活函数 $\sin(\omega_0 \cdot x)$，这使得网络能够表达高频细节。超网络与SIREN MLP联合训练，形成自动解码器框架。

这种设计的因果机制在于：**超网络将潜在码直接映射到整个位移函数的参数空间，而非仅在局部点条件化网络**。这等价于学习一个从潜在空间到函数空间的映射，使得每个潜在码对应一个完整的、全局一致的位移场。实验证明（图7），相比潜在码拼接，超网络提供了更快的收敛速度和更低的训练误差。

### 训练流程

训练采用自动解码器范式，交替优化网络参数和每个训练样本的潜在码。损失函数为：

$$L(p, \hat{p}, z_k) = \frac{\lambda_{mse}}{N} \sum_i^N ||p_i - S(\hat{p}_i, H(z_k)) - \hat{p}_i||_2^2 + \frac{\lambda_{reg}}{M} ||z_k||_2^2$$

其中第一项是MSE重建损失：对于训练样本的每个表面点 $p_i$，计算其在模板上的对应点 $\hat{p}_i$ 经变形模型后的位置与真实位置的距离。第二项是潜在码的L2正则化，防止过拟合。$\lambda_{mse}$ 和 $\lambda_{reg}$ 是平衡两个损失的超参数。

训练点采样采用**混合策略**：除了模板顶点外，还在表面均匀采样额外点。这一设计的动机是模板网格中存在较大三角形，仅用顶点采样会导致这些区域欠约束。消融实验证实，混合采样将测试集重建误差从0.0188降至0.0171。

### 推理与应用路径

训练完成后，模型支持多种推理路径：

1. **随机生成**：从标准正态分布采样潜在码 $z$，通过变形模型生成3D漫画。
2. **从2D关键点重建**：给定2D漫画的关键点位置，通过交替优化姿态参数（旋转 $R$、平移 $t$、投影 $\Pi$）和潜在码 $z$，最小化投影误差：
   $$L_{rec}(b, \hat{p}, z) = \frac{1}{B} \sum_i^B ||\Pi R D(\hat{p}_{l(i)}, z) + t - b_i||_2^2 + \frac{\lambda_{reg}}{M} ||z||_2^2$$
3. **语义编辑**：在潜在空间中学习语义方向（如“微笑”、“大鼻子”），沿该方向移动潜在码实现可控编辑。
4. **点控编辑**：用户拖拽模型上的控制点，通过优化潜在码满足位置约束，同时用L1正则项保持编辑后形状与原始形状接近：
   $$L_{edit}(\delta, \hat{p}, z) = \frac{\lambda_{con}}{H} \sum_i^H ||p_{h(i)} + \delta_i - D(\hat{p}_{h(i)}, z)||_2^2 + \frac{\lambda_{pre}}{M} ||z_0 - z||_1$$

### 模块间因果关系总结

整个框架的模块顺序和因果链为：**模板网格**提供几何先验和细节锚点 → **混合点采样**确保训练信号的充分覆盖 → **超网络**将潜在码映射为SIREN MLP的完整参数 → **SIREN MLP**建模连续位移场 → **变形模型**组合模板和位移得到最终形状。这一链条的核心在于超网络将“形状变化”编码为“函数参数变化”，使得紧凑的128维潜在空间能够表达高度非线性的漫画变形，同时保持模板的细节结构。

![[assets/figures/papers/paper_list_l17_https_ycjungsubhuman_github_io_DeepDeformable3DCaricatures/figures/005_Figure_3.jpg]]
*Figure 3: Overall framework for our deep deformable 3D caricature model*

![[assets/figures/papers/paper_list_l17_https_ycjungsubhuman_github_io_DeepDeformable3DCaricatures/figures/009_Figure_7.jpg]]
*Figure 7: Ablation study on the network architecture. We inspect error on the training set (left) and test set (right) of each model at different epochs. Star (★) indicates early stopping at epoch 1500 determined by checking the validation error*

## 实验与关键发现

### 主结果：连续形变表示 vs. 顶点数组表示

论文的核心实验是对比所提出的**SIREN MLP超网络**与基于**顶点位置数组MLP**的基线在3D漫画重建任务上的表现。两者使用相同的训练/测试分割、优化器和批量大小，早停法基于验证误差确定。在3DCaricShop测试集上，顶点位置数组MLP的平均逐顶点L2重建误差为**0.031**，而所提方法达到**0.017**，误差降低约45%（见Figure 5）。这一差距的因果机制在于：顶点数组MLP直接输出高维坐标向量，需要从零学习所有顶点位置，收敛慢且泛化差；而所提方法将形状建模为固定模板上的连续位移函数，网络只需学习相对模板的偏移量，先验地保留了模板的拓扑结构和细节（如眼睛、嘴部轮廓），从而在稀疏数据（约1400个注册网格）下实现更快收敛和更好泛化。

Figure 5同时展示了两种方法的训练/测试误差收敛曲线：所提方法在训练早期即快速下降，而顶点数组MLP的误差曲线下降缓慢且最终收敛到较高水平。这验证了"连续位移函数+超网络"这一表示选择是性能提升的核心因果旋钮。

### 与隐式SDF方法的定性对比

论文进一步将所提方法与基于符号距离函数（SDF）的自动解码器方法——**DeepSDF**（Park et al., CVPR 2019）和**DIF-Net**（Deng et al., CVPR 2021）——进行了定性比较（Figure 6）。结果显示，DeepSDF和DIF-Net能够重建出整体形状的大致轮廓，但**丢失了关键细节**，尤其是眼睛的形状和嘴部周围的表情特征。这一失败模式的根源在于：SDF表示对全局形状建模有效，但在3D漫画这种高度夸张、细节丰富的场景下，隐式表面难以精确捕捉模板表面上的局部几何变化。相比之下，所提方法使用固定模板网格并显式建模表面位移，天然保留了模板中的细节结构，因此在视觉质量上明显优于SDF基线。

![[assets/figures/papers/paper_list_l17_https_ycjungsubhuman_github_io_DeepDeformable3DCaricatures/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparison to SDF-based auto-decoder methods. We show reconstructions of 3D shapes in the training set. While DeepSDF and DIF-Net reconstruct overall shapes reasonably, the reconstructions miss important details such as the shape of eyes or the expression around the mouth*

**需要注意的是**：论文未报告与SDF方法的定量误差对比，仅提供了定性视觉结果。这一比较的公平性也需审慎看待——SDF方法并非为带模板的形变建模设计，直接对比可能低估了SDF在无模板场景下的优势。

### 关键消融实验

论文通过Figure 7的消融研究系统性地拆解了各设计选择的贡献，所有变体使用相同的训练协议并在epoch 1500处以验证误差早停（图中以★标记）：

**1. 位移表示 vs. 绝对位置表示**

将顶点位移数组MLP与顶点位置数组MLP对比，前者在训练集和测试集上均获得更低的误差。这表明将输出空间从"绝对坐标"改为"相对模板的位移"本身就是一个有效的归纳偏置——网络无需重新学习模板的基准形状，只需建模变形量。

**2. 超网络 vs. 潜在码拼接**

将SIREN MLP超网络与SIREN MLP with conditioning（将潜在码拼接到输入和中间特征）对比，超网络变体在训练误差上显著更低且**收敛速度大幅加快**。潜在码拼接方法需要更长时间才能收敛到相近水平。这一结果说明：超网络通过直接生成MLP的权重和偏置，为每个潜在码实例化了专门的形变函数，相比简单的特征拼接提供了更强的条件生成能力。这是论文方法的核心架构创新。

**3. 混合点采样策略**

论文在Sec. 3.3中报告了采样策略的消融：仅使用模板顶点采样时测试集重建误差为**0.0188**，而采用混合采样（顶点 + 表面均匀采样）后降至**0.0171**。这一改进的因果逻辑是：模板网格中存在较大三角形面片，仅采样顶点会忽略面片内部的形变信息；增加表面均匀采样点能更好地约束这些区域的位移函数学习，从而提升整体精度。

### 应用验证：从2D关键点重建与编辑

论文通过两个应用场景间接验证了模型的实用性：

**2D关键点重建**（Figure 9）：从2D漫画的稀疏关键点出发，通过交替优化姿态参数和潜在码，能够重建出合理的3D漫画形状。该方法在StyleCariGAN生成的2D漫画上展示了可行的重建结果，但论文未报告定量的关键点重投影误差或与基线方法的对比，因此该应用的精度水平需要进一步验证。

**语义编辑与点控编辑**（Figure 10, 11）：利用InterFaceGAN技术在潜在空间中识别语义方向（如"微笑"、"大额头"、"大鼻子"），可实现连续程度的语义编辑。点控编辑则通过优化潜在码满足用户指定的控制点约束，同时以L1正则项保持编辑后形状与原形状接近。这些编辑结果在视觉上合理，但论文明确指出**编辑操作缺乏对身份保留的显式保证**——过度编辑可能导致身份特征丢失。

### 失败模式与适用边界

论文坦诚地列出了方法的局限性，这些构成了重要的适用边界：

1. **细节质量与自相交**：生成的3D漫画细节仍有提升空间，且形变过程中可能产生网格自相交。论文将此列为未来工作方向，说明该方法在极端夸张变形下的几何合理性尚未得到保证。

2. **身份保留缺失**：编辑操作（无论是语义编辑还是点控编辑）没有显式的身份保持约束，编辑后的形状可能偏离原始身份特征。

3. **数据规模限制**：训练数据仅包含约1400个注册网格（来自3DCaricShop），限制了可学习形变空间的丰富度。在数据覆盖不足的漫画风格或极端夸张程度上，模型可能无法生成合理结果。

4. **模板依赖**：方法强依赖于一个预定义的固定模板网格（来自FaceWarehouse的均值脸），该模板具有张嘴结构。对于与模板拓扑差异过大的漫画风格，形变模型可能难以适应。

### 推理效率

论文在Sec. 5.5中报告了推理时间：生成一个包含11,551个顶点的3D形状耗时约**17 ms**；即使将采样密度提升至739,183个顶点，也仅需**987 ms**。这表明SIREN MLP的前向推理效率较高，支持交互式应用场景。但需注意，这些时间仅测量了网络前向传播，不包括后续的网格提取或后处理步骤。

![[assets/figures/papers/paper_list_l17_https_ycjungsubhuman_github_io_DeepDeformable3DCaricatures/figures/007_Figure_5.jpg]]
*Figure 5: Comparison to using vertex position array. Using our proposed representation and network architecture, the model provides faster convergence and better generalization. The reported error is the mean*

![[assets/figures/papers/paper_list_l17_https_ycjungsubhuman_github_io_DeepDeformable3DCaricatures/figures/012_Figure_9.jpg]]
*Figure 9: 3D caricature reconstruction from 2D caricature landmarks. Using manually marked sparse landmarks on the input, we optimize the latent code for our model to fit the landmark constraints. The inputs are 2D caricatures generated by StyleCariGAN [Jang et al. 2021]*

![[assets/figures/papers/paper_list_l17_https_ycjungsubhuman_github_io_DeepDeformable3DCaricatures/figures/013_Figure_10.jpg]]
*Figure 10: Semantic editing using InterFaceGAN technique. (a) Editing on the label Smile. (b) Large forehead. (c) Big nose. (+) denotes adding the editing vector that corresponds to the direction of the label on each row. (−) denotes subtracting the vector*

## 定位与知识库关联

本文的核心贡献在于改变了3D漫画建模中两个关键设计槽位：**形状表示形式**和**网络条件化机制**，从而在稀疏且高度多样化的漫画数据上实现了比已有方法更优的重建精度与编辑灵活性。

### 1. 改变的槽位一：从离散顶点/SDF到连续模板位移函数

传统3D形状生成通常采用两种表示：直接输出顶点位置数组，或将形状隐式编码为符号距离函数（SDF）。前者将形状视为固定拓扑下顶点坐标的集合，后者则学习一个从空间坐标到有符号距离的连续函数。

**相对于顶点数组方法**：直接预测顶点位置（Vertex position array MLP）在漫画数据上收敛缓慢且泛化误差大——本文实验表明其测试集重建误差为0.031，而本文方法仅0.017（Fig.5）。根本原因在于，顶点数组表示没有利用模板的先验结构，网络必须同时学习“合理的人脸拓扑”和“漫画夸张变形”，导致优化困难。本文改用**固定模板上的连续位移函数**，将问题分解为“模板提供基础结构”+“网络只学变形量”，大幅降低了学习难度。消融实验证实，即使仅将顶点数组改为顶点位移数组（Vertex displacement array MLP），训练和测试误差均已显著下降（Fig.7）。

**相对于SDF方法**：DeepSDF（Park et al., CVPR 2019）和DIF-Net（Deng et al., CVPR 2021）等隐式方法虽然能重建整体形状，但在漫画数据上丢失了眼睛形状、嘴部表情等关键细节（Fig.6）。这是因为SDF表示将形状建模为等值面，对表面细节的敏感度天然低于直接在表面上定义的位移函数。此外，SDF方法需要后处理步骤（如Marching Cubes）提取网格，而本文的位移表示可直接在模板顶点上采样，生成即用的拓扑一致网格，这对后续编辑应用至关重要。

**知识库挂载点**：本槽位的改变将本文挂载到“模板引导的连续形变建模”这一技术脉络中。该脉络可追溯至3D Morphable Model（3DMM）的线性形变空间，但本文用SIREN MLP替代了线性基，实现了非线性、高表现力的形变。同时，本文借鉴了DIF-Net中Deform-Net的架构思路（将形状分解为模板+变形），但将训练目标从SDF重建改为模板表面位移回归，这一改动是方法成功的关键。

### 2. 改变的槽位二：从潜在码拼接到超网络权重生成

在自动解码器框架中，如何将潜在码注入网络以控制形状变化是另一个关键设计。常见做法是将潜在码拼接到网络输入或中间层特征（conditioning by concatenation），这也是DeepSDF等方法的默认选择。

本文改用**超网络（hypernetwork）**：一个独立的ReLU MLP根据潜在码直接生成SIREN MLP的全部权重和偏置。消融实验（Fig.7）清晰展示了这一改变的因果效应：SIREN MLP hypernetwork的训练误差显著低于SIREN MLP with conditioning，且收敛速度快得多。论文明确指出“conditioning via latent code concatenation took much longer time to converge”（Sec. 3.2）。

这一现象的机理解释在于：拼接式条件化要求网络自身学习如何将潜在码信息与空间坐标信息融合，这是一个复杂的非线性映射；而超网络将“形状变化”的生成与“位移函数”的执行解耦，前者由超网络完成，后者由SIREN MLP执行，每个网络各司其职，优化更为高效。

**知识库挂载点**：超网络用于形状生成并非本文首创——DIF-Net已使用超网络为SDF的Deform-Net生成权重。但本文将其迁移到“模板表面位移”这一新的表示空间，并验证了其在漫画这一极端变形场景下的有效性。这说明超网络+连续位移的组合具有跨领域的泛化潜力，可视为一个可复用的技术模式。

### 3. 适用边界与局限性

本文方法在以下条件下表现良好，但也存在明确的边界：

- **数据依赖**：模型使用约1400个注册网格训练，漫画的多样性受限于数据集的覆盖范围。对于超出训练分布的极端变形，模型可能产生不自然的结果。
- **细节与自相交**：论文明确指出生成细节仍有提升空间，且可能产生网格自相交，这两个问题被列为未来工作。
- **编辑的身份保持**：语义编辑和点控编辑缺乏对身份特征的显式保证，过度编辑可能导致原始人物特征丢失。
- **拓扑固定**：模型假设所有形状与模板共享相同拓扑，无法处理拓扑变化（如张嘴程度极大时口腔内部的拓扑改变）。

### 4. 后续研究启发

本文为知识库贡献了以下可迁移的技术洞察：

1. **“模板+连续位移+超网络”的组合**可推广至其他需要在大变形下保持细节的3D建模任务（如人体姿态变形、动物形状生成），只需替换模板网格即可。
2. **混合点采样策略**（顶点+表面均匀采样，将测试误差从0.0188降至0.0171）是一个低成本但有效的训练技巧，适用于任何基于表面采样的形变模型。
3. 本文展示的**2D关键点到3D漫画重建**（Fig.9）和**潜在空间语义编辑**（Fig.10）为2D漫画生成模型（如StyleCariGAN）与3D建模之间建立了桥梁，后续工作可探索端到端的2D-to-3D漫画生成流水线。
4. 防止自相交和提升细节质量（论文的开放问题）可能引入几何正则化项（如法向一致性损失、ARAP能量）或对抗训练，这些方向值得探索。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Deep_Deformable_3D_Caricatures_With_Learned_Shape_Control.pdf]]
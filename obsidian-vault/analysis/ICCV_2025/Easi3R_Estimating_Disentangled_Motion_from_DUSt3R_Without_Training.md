---
title: "Easi3R: Estimating Disentangled Motion from DUSt3R Without Training"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Easi3R_Estimating_Disentangled_Motion_from_DUSt3R_Without_Training.pdf
project_link: https://easi3r.github.io/
code_link: null
aliases:
- Easi3R
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "DUSt3R的交叉注意力层隐含编码了丰富的相机和物体运动信息。通过解耦注意力图，可以在推理时直接实现动态分割和鲁棒的4D重建，无需任何训练。"
primary_logic: "预训练静态3D模型DUSt3R的注意力层已捕获场景动态，通过简单的聚合与分解策略即可提取动态对象分割并指导第二次推理中的注意力重新加权，从而将静态模型无缝适配到动态场景。"
claims:
- "DUSt3R的注意力层隐含编码了相机和物体运动的丰富信息。"
- "解耦注意力图实现了准确的动态区域分割、相机位姿估计和4D稠密点云重建。"
- "动态分割可从预训练的DUSt3R注意力层中提取，无需光流或分割训练。"
- "DAVIS-16 上 JM↑ (w/o SAM2) = 57.7 (Easi3R_monst3r)"
---

# Easi3R: Estimating Disentangled Motion from DUSt3R Without Training

> [!tip] 核心洞察
> 预训练静态3D模型DUSt3R的注意力层已捕获场景动态，通过简单的聚合与分解策略即可提取动态对象分割并指导第二次推理中的注意力重新加权，从而将静态模型无缝适配到动态场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Easi3R：无需训练从DUSt3R估计解耦运动 |
| 英文题名 | Easi3R: Estimating Disentangled Motion from DUSt3R Without Training |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2503.24391) · [Project](https://easi3r.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Easi3R |
| Dataset | DAVIS-16, DyCheck |

> [!tip] 效果简介
> - DAVIS-16 上，JM↑ (w/o SAM2) 为 57.7 (Easi3R_monst3r)，对比 42.1 (DUSt3R)，变化 +15.6。
> - DyCheck 上，ATE↓ 为 0.021 (Easi3R_dust3r w/flow)，对比 0.029 (DUSt3R w/flow)，变化 -0.008。
> - DyCheck 上，RTE↓ 为 0.014 (Easi3R_dust3r w/flow)，对比 0.021 (DUSt3R w/flow)，变化 -0.007。

## 概要

### 问题与瓶颈

从单目视频中恢复4D动态场景（即随时间变化的3D几何与运动）是计算机视觉的核心挑战。现有方法通常依赖大规模动态4D数据集进行预训练或微调，然而**训练高度泛化的4D模型所需的动态4D数据集规模和多样性有限**，成为主要瓶颈。以DUSt3R为代表的静态3D重建模型在静态场景中表现优异，但直接应用于包含动态物体的视频时，重建质量会因动态物体造成的对齐退化而显著下降（Figure 2）。

### 核心发现

Easi3R的关键洞察在于：**预训练静态3D模型DUSt3R的注意力层已隐含编码了丰富的相机和物体运动信息**。DUSt3R解码器中的交叉注意力图在视图间传递信息时，会自然形成对动态区域、静态区域、遮挡边界等的差异化响应模式（Figure 4）。通过精心设计的注意力图聚合与分解策略，可以在不引入任何额外训练的情况下，从这些预训练的注意力层中提取动态物体分割，并利用该分割指导第二次推理中的注意力重新加权，从而将静态模型无缝适配到动态场景。

### 方法定位

Easi3R是一种**训练无关、即插即用的推理时适配方法**。与需要在大规模动态数据集上微调的MonST3R、DAS3R、CUT3R等方法不同，Easi3R直接作用于预训练的DUSt3R或其变体（如MonST3R）之上，无需光流估计或显式分割头训练。其核心流程为：首次前向推理时聚合交叉注意力图并解耦出动态分割掩码，随后在第二次推理中对动态区域的交叉注意力进行重新加权，抑制动态物体对相机位姿估计和静态场景重建的干扰。

### 主要结果

在动态物体分割、相机位姿估计和4D点云重建三个任务上，Easi3R均展现出超越需要训练的方法的性能：

- **动态分割**：在DAVIS-16数据集上，Easi3R_monst3r的JM指标达到57.7（不含SAM2后处理），较DUSt3R基线（42.1）提升15.6个百分点（Table 1）。
- **相机位姿**：在DyCheck数据集上，Easi3R_dust3r（w/flow）的ATE从基线的0.029降至0.021，RTE从0.021降至0.014（Table 2）。
- **点云重建**：在DyCheck上，Easi3R_dust3r的Accuracy Mean从0.772降至0.703（越低越好），提升显著（Table 7消融）。

值得注意的是，Easi3R在静态场景（如ScanNet）上也带来友好提升，表明其注意力重新加权机制不会过度分割静态场景，而是倾向于重新加权低置信度区域，从而改善位姿估计（Figure 10, Table 9）。

### 局限与开放问题

Easi3R的改进主要集中在动态区域处理和全局对齐，**无法纠正静态部分的深度预测误差**，因此每视角深度精度仍存在差距。此外，重建结果在动态物体边界附近仍可能出现浮动体（floaters）伪影（Figure 9）。未来工作方向包括：纠正静态部分的逐视角深度预测以弥补深度精度差距，以及进一步减少边界附近的浮动体伪影。



### 动态4D重建的核心瓶颈

从单目视频中恢复时空一致的4D表示是计算机视觉的核心挑战之一。近年来，以DUSt3R为代表的静态3D重建方法取得了显著进展，能够从稀疏图像对中直接预测稠密点图。然而，当这些方法被直接应用于包含动态物体的视频时，重建质量会急剧下降——动态物体占据显著画面比例时，跨帧对齐会出现严重退化（Figure 2）。

这一困境的根源在于**训练高度泛化的4D模型所需的动态4D数据集规模和多样性有限**。现有方法尝试通过在大规模动态数据集上进行微调来弥补这一缺口，例如MonST3R在DUSt3R基础上针对动态场景进行微调，DAS3R进一步添加显式分割头，CUT3R则在静态与动态数据混合集上训练前馈重建变体。但这些方案始终受制于数据覆盖范围的限制，泛化能力难以突破训练数据的边界。

### 现有方法的缺口

当前动态4D重建方法存在两个关键的结构性缺陷：

1. **对显式运动信号的依赖**：主流方法通常依赖光流估计或预先训练的显式分割头来识别动态区域。这不仅引入了额外的计算开销和误差累积，还使系统对光流质量高度敏感。
2. **训练与数据的耦合**：微调范式将模型性能与训练数据的规模和质量深度绑定，在面对训练分布之外的场景时泛化能力不足。

### 本文动机：从注意力中挖掘运动信息

Easi3R的核心动机源自一个关键发现：**预训练静态3D模型DUSt3R的交叉注意力层已经隐含编码了丰富的相机和物体运动信息**。这一发现意味着，动态场景理解的关键线索并非必须通过额外训练来注入，而是可以从已有模型中直接提取。

基于此，Easi3R提出了一条与现有范式截然相反的路径：**无需任何训练，仅通过推理阶段的注意力解耦与重新加权，将静态DUSt3R无缝适配到动态场景**。具体而言，通过聚合解码器中的交叉注意力图，可以提取出具有明确语义的动态注意力模式；利用这些模式进行动态区域分割，并在第二次推理中重新加权注意力分布以隔离动态物体的干扰，从而实现鲁棒的4D重建与相机运动恢复。

这一训练无关的即插即用策略绕过了动态4D数据瓶颈，同时避免了对光流或分割标注的依赖，为静态模型向动态场景的泛化提供了新的思路。



## 核心方法与创新机理

Easi3R的核心创新在于**无需任何训练**，仅通过解耦预训练静态模型DUSt3R内部的交叉注意力图，即可将静态3D重建模型适配到动态4D场景。这一范式转变源自一个关键发现：**DUSt3R的交叉注意力层已隐含编码了丰富的相机与物体运动信息**，只需在推理时采用简单的聚合与分解策略即可提取这些信息。

具体而言，Easi3R相对于现有基线实现了以下三个**changed slots**：

### 1. 动态分割：从注意力图分解替代光流与分割头

现有方法（如MonST3R、DAS3R）依赖光流估计或显式训练的分割头来识别动态区域，这需要额外的网络模块或微调。Easi3R提出了一种全新的无训练、无光流的分割策略：通过对DUSt3R解码器中的交叉注意力图进行时间维度的均值与方差聚合，生成四个语义注意力图——$\mathbf{A}_\mu^{b=\mathrm{src}}$、$\mathbf{A}_\sigma^{b=\mathrm{src}}$、$\mathbf{A}_\mu^{a=\mathrm{ref}}$、$\mathbf{A}_\sigma^{a=\mathrm{ref}}$，然后通过元素级乘积组合为每帧的动态注意力图：

$$\mathbf{A}^{a=\mathrm{dyn}} = (1 - \mathbf{A}_\mu^{a=\mathrm{src}}) \cdot \mathbf{A}_\sigma^{a=\mathrm{src}} \cdot \mathbf{A}_\mu^{a=\mathrm{ref}} \cdot (1 - \mathbf{A}_\sigma^{a=\mathrm{ref}})$$

其中，$(1 - \mathbf{A}_\mu^{a=\mathrm{src}})$ 捕获源视图中对参考视图贡献较低的区域（即动态物体所在位置），$\mathbf{A}_\sigma^{a=\mathrm{src}}$ 反映时序上的注意力波动（动态物体引起的匹配不确定性），而参考视图的逆均值项 $(1 - \mathbf{A}_\sigma^{a=\mathrm{ref}})$ 则用于抑制纹理缺失区域和相机运动造成的干扰。实验表明，这一纯注意力驱动的分割策略在DAVIS-16数据集上使DUSt3R的分割JM指标从42.1提升至57.7（+15.6），且四个聚合注意力图缺一不可（Table 6）。

### 2. 推理流程：第二次推理中的注意力重新加权

传统DUSt3R及其变体仅执行单次前向推理，动态物体直接参与交叉注意力计算，导致点图预测和对齐退化。Easi3R引入**第二次推理**机制：利用第一次推理提取的动态分割掩码，在第二次推理时对交叉注意力层进行重新加权——将动态区域对应的注意力值直接置零：

$$\mathrm{softmax}(\tilde{\mathbf{A}}_l^{ab}) = \begin{cases} 0 & \mathrm{if~} \mathbf{M}^{ab} \\ \mathrm{softmax}(\mathbf{A}_l^{ab}) & \mathrm{otherwise} \end{cases}$$

这一操作使解码器在第二次推理中“忽略”动态物体，仅基于静态区域进行匹配，从而显著提升相机位姿估计和静态场景重建的鲁棒性。消融实验（Table 7）证实，仅对参考视图解码器分支重新加权优于同时重新加权两个分支，且该方法在静态场景（如ScanNet）中同样带来友好提升，不会导致过度分割。

### 3. 全局对齐优化：分割感知的光流重投影一致性损失

原始DUSt3R的全局对齐仅使用点图间的L1损失，未显式建模动态场景中的运动一致性。Easi3R在全局对齐优化目标中增加了**分割感知的光流重投影一致性损失**：

$$\mathcal{L}_{\mathrm{flow}} = \sum_{t \in T} \sum_{i \in \varepsilon^{t}} (1 - \mathbf{M}^{a}) \cdot \| \hat{\mathcal{F}}_{i}^{a \to b} - \mathcal{F}_{i}^{a \to b} \|_1 + (1 - \mathbf{M}^{b}) \cdot \| \hat{\mathcal{F}}_{i}^{b \to a} - \mathcal{F}_{i}^{b \to a} \|_1$$

该损失仅在静态区域（由掩码 $\mathbf{M}$ 标记）上约束投影点流与光流的一致性，确保动态物体不干扰全局对齐。在DyCheck数据集上，加入光流约束后，Easi3R_dust3r的ATE从0.029降至0.021，RTE从0.021降至0.014（Table 2），消融实验（Table 7）进一步验证了该模块对4D重建质量的持续提升作用。

### 创新本质

这三个changed slots共同构成了一条**因果链条**：注意力图分解（Slot 1）提供动态分割，分割掩码驱动注意力重新加权（Slot 2）以改善成对重建，分割感知的全局对齐（Slot 3）则确保多帧一致性。整个流程无需任何训练数据、微调或额外网络模块，仅通过推理时的注意力操控就实现了从静态3D到动态4D的无缝适配——这正是Easi3R与所有现有方法（MonST3R、DAS3R、CUT3R等）的根本区别。



Easi3R 提出了一种无需训练的即插即用式4D重建框架，其核心思想是：**预训练静态3D模型DUSt3R的交叉注意力层已经隐含编码了丰富的相机与物体运动信息**，通过对这些注意力图进行解耦与聚合，可以在推理阶段直接实现动态分割与鲁棒的4D重建，无需任何微调或额外数据训练。

### 输入与输出

框架的输入为一段随意拍摄的视频序列 $\{ I^{t} \in \mathbb{R}^{W \times H \times 3} \}_{t=1}^{T}$，共 $T$ 帧，目标输出包括：
- 每帧的**动态物体分割掩码**；
- 全局一致的**相机位姿估计**；
- 解耦的**静态场景点云**与**动态物体4D点云**。

### 整体流程

Easi3R 的推理流程分为三个关键阶段，如 Figure 3 所示：

**第一阶段：DUSt3R 成对推理与注意力提取。** 采用滑动时间窗口策略，以当前帧 $t$ 为中心构建对称窗口（窗口大小 $n$，如 $n=3$），对窗口内的所有图像对进行 DUSt3R 网络推理。DUSt3R 由权重共享的 ViT 编码器和两个解码器组成（参考视图解码器和源视图解码器），解码器通过自注意力和交叉注意力在视图间交换信息。在此过程中，Easi3R 从解码器的所有层中提取交叉注意力图，并沿层维度和空间维度进行平均，得到每对图像的空间注意力图 $\mathbf{A}^{b=\mathrm{src}}$，表示源视图 $b$ 对参考视图的整体贡献。

**第二阶段：时序注意力聚合与动态分割。** 将所有成对的空间注意力图沿时间维度进行聚合，计算每个视图作为源视图和参考视图时的均值注意力图（$\mathbf{A}_{\mu}$）与标准差注意力图（$\mathbf{A}_{\sigma}$），共产生四个语义图（Figure 4）。通过分析这些注意力图的组合特性——源视图的逆平均注意力 $(1 - \mathbf{A}_{\mu}^{a=\mathrm{src}})$ 捕获外观变化区域，源视图的标准差注意力 $\mathbf{A}_{\sigma}^{a=\mathrm{src}}$ 捕获时序不一致区域，参考视图的平均注意力 $\mathbf{A}_{\mu}^{a=\mathrm{ref}}$ 和逆标准差注意力 $(1 - \mathbf{A}_{\sigma}^{a=\mathrm{ref}})$ 用于抑制纹理缺失区域和相机运动——Easi3R 通过元素级乘积计算每帧的动态注意力图：

$$\mathbf{A}^{a=\mathrm{dyn}} = (1 - \mathbf{A}_{\mu}^{a=\mathrm{src}}) \cdot \mathbf{A}_{\sigma}^{a=\mathrm{src}} \cdot \mathbf{A}_{\mu}^{a=\mathrm{ref}} \cdot (1 - \mathbf{A}_{\sigma}^{a=\mathrm{ref}})$$

对该图施加阈值 $\alpha$ 即可得到每帧的动态物体分割掩码 $\mathbf{M}^{t}$。此外，跨帧特征聚类被用于增强分割的时间一致性（Figure 8）。

**第三阶段：注意力重新加权与第二次推理。** 利用第一阶段获得的动态分割掩码，Easi3R 执行第二次 DUSt3R 前向推理，但在交叉注意力层中对动态区域进行重新加权——将动态区域对应的注意力值置零：

$$\mathrm{softmax}(\tilde{\mathbf{A}}_{l}^{ab}) = \begin{cases} 0 & \mathrm{if~} \mathbf{M}^{ab} \\ \mathrm{softmax}(\mathbf{A}_{l}^{ab}) & \mathrm{otherwise} \end{cases}$$

这种机制使网络在重建时“忽略”动态物体，从而获得更准确的静态场景点图和相机位姿。最后，在全局对齐阶段，Easi3R 引入分割感知的光流重投影一致性损失 $\mathcal{L}_{\mathrm{flow}}$，在静态区域上约束投影点流与光流估计一致，进一步提升全局对齐质量。

### 关键设计选择

1. **无训练特性**：整个流程仅使用预训练的 DUSt3R 或 MonST3R 权重，不涉及任何微调或额外优化。
2. **注意力解耦而非显式头**：与 DAS3R 等方法需训练分割头不同，Easi3R 直接从注意力图中提取动态信息，避免了动态数据集的依赖。
3. **双阶段推理**：第一次推理用于提取注意力图和分割掩码，第二次推理利用掩码进行注意力重新加权，实现运动解耦。
4. **光流约束为可选模块**：光流损失仅用于全局对齐优化，可在无光流条件下运行，确保与不使用光流的基线公平比较。



Easi3R 的核心设计围绕一个发现展开：DUSt3R 解码器中的交叉注意力层已隐含编码了丰富的相机与物体运动信息。通过解耦这些注意力图，可以在推理时直接实现动态分割与鲁棒的 4D 重建，无需任何训练。整个流程包含四个关键模块。

### 3.1 成对点图预测与全局对齐

给定视频序列 $\{ I ^ { t } \in \mathbb { R } ^ { W \times H \times 3 } \} _ { t = 1 } ^ { T }$，Easi3R 采用滑动时间窗口处理，对以帧 $t$ 为中心的对称窗口内所有图像对进行推理。DUSt3R 接受两幅图像 $I^a, I^b$，输出参考视图坐标空间内的两个点图：

$$X^{aa}, X^{ba} = \mathrm{DUSt3R}(I^a, I^b)$$

其中 $X^{aa}$ 为参考视图 $I^a$ 的自身点图，$X^{ba}$ 为源视图 $I^b$ 在参考视图坐标空间中的点图。

为获得全局一致的重建，Easi3R 通过优化每个图像对的相似变换将成对点图对齐到全局坐标系：

$$\mathcal{X}^* = \arg\min_{\mathcal{X},\mathbf{P},\mathbf{s}} \sum_{t \in T} \sum_{i \in \varepsilon^t} \| \mathcal{X}^a - \mathbf{s}_i^t \mathbf{P}_i^t X^{aa} \|_1 + \| \mathcal{X}^b - \mathbf{s}_i^t \mathbf{P}_i^t X^{ba} \|_1$$

其中 $\mathbf{P}_i^t$ 和 $\mathbf{s}_i^t$ 分别为第 $i$ 个图像对的旋转矩阵和尺度因子，$\mathcal{X}$ 为全局对齐后的点图。

### 3.2 交叉注意力图聚合

DUSt3R 包含两个分支：上分支处理参考图像 $I^a$，下分支处理源图像 $I^b$。两幅图像首先经过权重共享的 ViT 编码器提取特征标记，随后由两个解码器通过自注意力和交叉注意力在视图内和视图间交换信息。解码器第 $l$ 层的交叉注意力图定义为：

$$\mathbf{A}_l^{ab} = \mathbf{Q}_l^a \mathbf{K}_l^{b^T} / \sqrt{c}, \quad \mathbf{A}_l^{ba} = \mathbf{Q}_l^b \mathbf{K}_l^{aT} / \sqrt{c}$$

其中 $\mathbf{Q}_l^a, \mathbf{K}_l^b$ 分别为查询和键矩阵，$c$ 为通道维度。

**空间聚合**：跨所有解码器层和空间位置平均，得到视图 $b$ 作为源视图时对参考视图的整体贡献：

$$\mathbf{A}^{b=\mathrm{src}} = \sum_l \sum_x \mathbf{A}_l^{ab}(x,y,z) / (L \times h \times w)$$

**时间聚合**：沿时间维度对注意力图计算均值和方差，以捕捉时序动态：

$$\mathbf{A}_\mu^{b=\mathrm{src}} = \mathbf{Mean}(\mathbf{A}_i^{b=\mathrm{src}}), \quad \mathbf{A}_\sigma^{b=\mathrm{src}} = \mathbf{Std}(\mathbf{A}_i^{b=\mathrm{src}})$$

最终产生四个语义图：$\mathbf{A}_\mu^{b=\mathrm{src}}$（源视图平均注意力）、$\mathbf{A}_\sigma^{b=\mathrm{src}}$（源视图注意力方差）、$\mathbf{A}_\mu^{a=\mathrm{ref}}$（参考视图平均注意力）、$\mathbf{A}_\sigma^{a=\mathrm{ref}}$（参考视图注意力方差）。这些图分别捕获纹理对应、遮挡边界、静态区域和动态变化等不同模式（参见图 4 的可视化）。

### 3.3 动态物体分割

动态物体的注意力特征表现为：作为源视图时注意力均值低（因为动态区域难以建立稳定对应）且方差高（对应关系随时间剧烈变化）；作为参考视图时注意力均值高（静态背景持续关注动态物体）且方差低。基于此，每帧动态注意力图由四个语义图的元素级乘积得到：

$$\mathbf{A}^{a=\mathrm{dyn}} = (1 - \mathbf{A}_\mu^{a=\mathrm{src}}) \cdot \mathbf{A}_\sigma^{a=\mathrm{src}} \cdot \mathbf{A}_\mu^{a=\mathrm{ref}} \cdot (1 - \mathbf{A}_\sigma^{a=\mathrm{ref}})$$

其中 $(1 - \mathbf{A}_\mu^{a=\mathrm{src}})$ 突出对应关系弱的区域，$\mathbf{A}_\sigma^{a=\mathrm{src}}$ 捕获时间上不稳定的对应，$\mathbf{A}_\mu^{a=\mathrm{ref}}$ 标识被持续关注的区域，$(1 - \mathbf{A}_\sigma^{a=\mathrm{ref}})$ 抑制相机运动引起的全局变化。通过阈值化即可获得每帧动态分割掩码 $\mathbf{M}^t = [\mathbf{A}^{t=\mathrm{dyn}}] > \alpha$。

### 3.4 注意力重新加权与分割感知全局对齐

获得动态掩码后，Easi3R 进行第二次推理，在交叉注意力层中对动态区域进行重新加权：

$$\mathrm{softmax}(\tilde{\mathbf{A}}_l^{ab}) = \begin{cases} 0 & \mathrm{if~} \mathbf{M}^{ab} \\ \mathrm{softmax}(\mathbf{A}_l^{ab}) & \mathrm{otherwise} \end{cases}$$

这等效于在交叉注意力中屏蔽动态区域的对应关系，迫使网络仅依赖静态背景进行匹配，从而消除动态物体对相机位姿估计和点云重建的干扰。

为进一步提升全局对齐质量，Easi3R 引入分割感知的光流重投影一致性损失：

$$\mathcal{L}_{\mathrm{flow}} = \sum_{t \in T} \sum_{i \in \varepsilon^{t}} (1 - \mathbf{M}^{a}) \cdot \| \hat{\mathcal{F}}_{i}^{a \to b} - \mathcal{F}_{i}^{a \to b} \|_1 + (1 - \mathbf{M}^{b}) \cdot \| \hat{\mathcal{F}}_{i}^{b \to a} - \mathcal{F}_{i}^{b \to a} \|_1$$

其中 $\hat{\mathcal{F}}$ 为从点图投影得到的光流，$\mathcal{F}$ 为真实光流。该损失仅在静态区域 $(1 - \mathbf{M})$ 上约束投影点流与光流一致，确保动态物体不影响全局对齐优化。注意光流约束为可选模块，以保证与不使用光流的基线公平比较。



## 实验与关键发现

### 核心实验设计

Easi3R 在三个任务上验证其有效性：动态物体分割、相机位姿估计和 4D 稠密点云重建。评估采用滑动时间窗口逐对推理，无需任何微调或额外数据优化。主要基线包括 **DUSt3R**、**MonST3R**（基于 DUSt3R 微调的动态 4D 重建方法）、**DAS3R**（在 MonST3R 上添加分割头）和 **CUT3R**（在静动态数据集上微调的 DUSt3R 变体）。光流约束作为可选模块，以确保与不使用光流的基线公平比较。

### 动态物体分割

在 DAVIS-16 数据集上，Easi3R 展现出显著的动态分割能力。以 MonST3R 为骨干时，Easi3R_monst3r 在无 SAM2 后处理的 JM 指标上达到 **57.7**，相比原始 DUSt3R 的 42.1 提升 **+15.6**（Table 1）。这一提升归因于注意力图解耦策略——通过组合逆平均注意力和标准差注意力（公式 9），直接从预训练模型的交叉注意力层提取动态区域，无需光流估计或显式分割头训练。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/006_Table_1.jpg]]
*Table 1: Dynamic Object Segmentation on the DAVIS dataset. The best and second best results are bold and underlined, respectively. Easi3R dust3r/monst3r denotes the Easi3R experiment with the backbones of MonST3R/DUSt3R*

定性结果（Figure 5）显示，Easi3R 的分割掩码在物体边界完整性和时序一致性上均优于基线。消融实验（Table 6）进一步揭示因果机制：四个时序聚合的交叉注意力图（源视图均值/方差、参考视图均值/方差）均对分割有贡献，禁用任一个都会导致性能下降；特征聚类通过增强时序一致性显著提升分割质量。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/014_Table_6.jpg]]
*Table 6: Ablation of Dynamic Object Segmentation on DAVIS*

### 相机位姿估计

在 DyCheck、ADT 和 TUM-dynamics 三个动态基准上，Easi3R 展示了鲁棒的相机运动恢复能力。以 DUSt3R 为骨干并启用光流约束时，Easi3R_dust3r 在 DyCheck 上取得 **ATE 0.021**（原始 DUSt3R 为 0.029，降低 0.008）、**RTE 0.014**（原始 0.021，降低 0.007）的领先结果（Table 2）。这一改进的核心机制是注意力重新加权——第二次推理时在交叉注意力层将动态区域对应的注意力置零（公式 10），使模型聚焦于静态场景结构进行位姿优化。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/008_Table_2.jpg]]
*Table 2: Benefits of Easi3R on Camera Pose Estimation on the DyCheck, ADT and TUM-dynamics datasets. The best and second best results are bold and underlined, respectively. Easi3R dust3r/monst3r denotes the Easi3R experiment with the backbones of MonST3R/DUSt3R*

Table 3 的全面比较表明，Easi3R 在多数设置下优于所有经过动态数据集训练的 DUSt3R 变体。Figure 7 的轨迹可视化直观展示了 Easi3R 估计的相机轨迹（橙色）相比原始骨干（蓝色）更接近真值（灰色），偏差明显减小。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/010_Table_3.jpg]]
*Table 3: Quantitative Comparisons of Camera Pose Estimation on the DyCheck, ADT and TUM-dynamics datasets. The best and second best results are bold and underlined, respectively*

值得注意的是，在静态场景（如 ScanNet）中，Easi3R 同样带来友好提升（Table 9）。Figure 10 揭示了原因：Easi3R 倾向于对静态场景中的低置信度区域进行重新加权，这实际上起到了不确定性感知的注意力校准作用，而非过度分割。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/019_Table_9.jpg]]
*Table 9: Camera Pose Evaluation. We use the evaluation results from CUT3R for baselines*

### 点云重建

在 DyCheck 数据集上，Easi3R 的点云重建精度和完整性均得到改善。以 DUSt3R 为骨干时，Easi3R_dust3r 的 Accuracy Mean 从 0.772（仅参考视图，无掩码）降至 **0.703**（Ref w/ Mask），降低了 0.069（Table 7 消融）。Table 4 和 Table 5 的完整比较表明，Easi3R 在 Accuracy、Completeness 和 Distance 三项指标上优于多数基线。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/007_Table_4.jpg]]
*Table 4: Benefits of Easi3R on Point Cloud Reconstruction on the DyCheck dataset. The best and second best results are bold and underlined, respectively. Easi3R $\mathrm { d u s t }$ 3 $\mathrm { r } / \mathrm { m o n s t }$ 3 $\mathrm { r }$ denotes the Easi3R experiment with the backbones of MonST3R/DUSt3R

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/009_Table_5.jpg]]
*Table 5: Quantitative Comparisons of Point Cloud Reconstruction on the DyCheck dataset. The best and second best results are bold and underlined, respectively*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/015_Table_7.jpg]]
*Table 7: Ablation Study of Camera Pose Estimation and Point Cloud Reconstruction on the DyCheck dataset*

Figure 6 的定性比较展示了跨帧全局对齐的静态场景与动态点云分离效果。Easi3R 实现了静态场景的时序一致性重建，同时保持了动态物体的独立点云表示。这一能力源于注意力引导分割与分割感知全局对齐的协同——后者在静态区域上施加光流重投影一致性约束（公式 11），确保投影点流与光流估计一致。

### 消融分析的关键发现

消融实验（Table 6、Table 7）揭示了几个重要的因果机制：

1. **四个注意力图的贡献**：源视图均值/方差和参考视图均值/方差四个注意力图均不可或缺，禁用任一个都导致分割性能下降，验证了动态信息分布在多个注意力模式中。

2. **重新加权的分支选择**：仅对参考视图解码器进行注意力重新加权优于同时重新加权两个分支（Table 7），表明动态物体的干扰主要通过参考视图的交叉注意力传播。

3. **分割感知全局对齐**：在光流监督下，分割感知的全局对齐持续提升 4D 重建质量（Table 7），证明将分割信息融入优化目标的有效性。

4. **特征聚类的作用**：跨帧特征聚类通过增强时序一致性，显著提高分割性能（Table 6 w/o Clustering vs Full），这是方法实现时序稳定分割的关键设计。

### 失败模式与局限性

尽管 Easi3R 在多个任务上取得显著提升，但仍存在明确的失败模式：

- **深度精度瓶颈**：当骨干网络（DUSt3R/MonST3R）预测的深度不准确时，Easi3R 仍会失败。方法主要改进动态区域处理和全局对齐，未纠正静态部分的深度误差，因此每视角深度精度仍存在明显差距（Table 8 视频深度评估）。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/018_Table_8.jpg]]
*Table 8: Video Depth Evaluation. We use the evaluation results from CUT3R for baselines*

- **边界浮动体伪影**：重建结果在动态物体边界附近仍可能出现浮动体（Figure 9）。虽然 Easi3R 改善了相机位姿和点云对齐（Figure 9 上行），但物体边界处的深度不连续性仍导致漂浮点云碎片。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/016_Figure_9.jpg]]
*Figure 9: Limitation. We visualize static reconstructions from two different viewpoints in the top and bottom rows. Easi3R improves camera pose estimation and point cloud reconstruction (top row), enhancing alignment in structures like swing supports through attention re-weighting and segmentation-aware global alignment. However, from another viewpoint (bottom row), Easi3R still produces floaters near object boundaries*

- **静态场景中的“动态”掩码**：Easi3R 在静态场景中也会生成掩码（Figure 10），这实际上是低置信度区域的重新加权，虽然对位姿估计有益，但在语义上并非真正的动态分割。

这些局限性指向两个开放问题：如何纠正静态部分的每视角深度预测以弥补深度精度差距，以及如何进一步减少动态物体边界附近的浮动体伪影。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/020_Table_10.jpg]]
*Table 10: Comparisons of Dynamic Object Segmentation on DAVIS with 2D dynamic segmentation methods*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2503_24391/figures/021_Table_11.jpg]]
*Table 11: More ablations on segmentation quality using DAVIS. * denotes the value used in the submission*



## 定位与知识库关联

### 1. 与基线方法的关系

Easi3R 的核心贡献在于提出了一种**训练无关（training-free）**的推理时适配策略，其方法定位与以下四类基线工作形成明确对比：

- **DUSt3R**：作为静态3D重建的预训练骨干网络，DUSt3R 在动态场景中会因物体运动导致对齐退化（见 Figure 2）。Easi3R 直接复用其预训练权重，通过注意力图解耦实现动态适配，无需任何微调。

- **MonST3R**：在 DUSt3R 基础上针对动态场景进行微调。Easi3R 与 MonST3R 的关系是**即插即用的增强层**——Easi3R 可同时作用于 DUSt3R 和 MonST3R 两种骨干，在两者上均带来一致的性能提升。实验表明，MonST3R 倾向于产生欠分割的动态掩码（见 Figure 12），而 Easi3R 的注意力引导分解能有效缓解这一问题。

- **DAS3R**：在 MonST3R 上额外添加显式分割头，需要针对分割任务进行专门训练。Easi3R 的核心差异在于**完全消除了对分割头训练和光流估计的依赖**，直接从预训练模型的交叉注意力层中提取动态分割信息。

- **CUT3R**：在静态和动态数据集上联合微调的 DUSt3R 变体，支持前馈重建。Easi3R 的独特优势在于**无需访问任何动态4D训练数据**，仅通过推理时的注意力重加权即可达到甚至超越这些需要大规模动态数据集训练的方法。

### 2. 方法适用边界

Easi3R 的适用性受以下条件约束：

1. **骨干网络依赖性**：方法要求底层模型采用 DUSt3R 式的双分支解码器架构，且交叉注意力层可被访问和修改。对于其他架构的3D重建模型，注意力解耦策略需要重新设计。

2. **深度预测质量瓶颈**：Easi3R 主要改进动态区域的掩码和全局对齐，但**不纠正静态部分的每视角深度预测误差**。当骨干网络（DUSt3R/MonST3R）本身预测的深度不准时，Easi3R 仍会失败——这是一个上游模型能力决定的硬性边界。

3. **动态物体边界伪影**：尽管注意力重加权有效隔离了动态区域的影响，重建结果在物体边界附近仍可能出现浮动体（floaters）伪影（见 Figure 9），这是当前方法的已知局限。

4. **静态场景的友好性**：值得注意的是，Easi3R 在静态场景中并不会产生过度分割——它倾向于对低置信度区域进行重加权，反而带来了位姿估计的友好提升（见 Figure 10 和 Table 9 中 ScanNet 的结果）。

### 3. 方法谱系中的独特定位

从方法谱系角度看，Easi3R 占据了一个此前未被探索的位置：**利用预训练静态模型的内部表示（注意力图）直接进行动态场景推理，而不引入任何训练信号**。这与以下技术路线形成对照：

| 维度 | 传统路线 | Easi3R 路线 |
|------|---------|------------|
| 动态分割 | 光流估计 / 显式分割头训练 | 注意力图分解（无训练、无光流） |
| 4D 重建 | 在动态数据集上微调 | 推理时注意力重加权 |
| 全局对齐 | 仅 L1 点图对齐 | 增加分割感知的光流重投影一致性损失 |
| 数据需求 | 大规模动态4D数据集 | 零额外训练数据 |

### 4. 局限性与开放问题

**已识别的局限性**：

1. **深度精度差距**：Easi3R 改善了对齐和动态处理，但每视角深度精度仍与需要微调的方法存在明显差距。这是因为方法未触及静态区域的深度预测机制。

2. **边界浮动体**：动态物体边界附近的浮动体伪影（Figure 9）源于注意力掩码的二值化处理，边界区域的过渡不够平滑。

3. **极端动态场景**：当动态物体占据画面绝大部分且纹理稀疏时，注意力图的信噪比下降，分割质量可能退化。

**开放问题**：

1. **如何纠正静态部分的每视角深度预测？** 这是弥补与微调方法之间深度精度差距的关键。可能的路径包括在第二次推理中同时调整解码器的自注意力机制，或引入轻量级的测试时优化。

2. **如何进一步减少动态物体边界的浮动体伪影？** 当前二值掩码策略可被替换为软注意力重加权（连续值掩码），但需要研究如何从注意力图中可靠地估计边界过渡区域的权重。

3. **注意力解耦策略能否泛化到其他视觉 backbone？** 当前设计紧密耦合于 DUSt3R 的双分支交叉注意力架构。探索该策略在更通用的 ViT 或多模态模型中的适用性是一个有价值的方向。



## 原文 PDF

![[paperPDFs/ICCV_2025/Easi3R_Estimating_Disentangled_Motion_from_DUSt3R_Without_Training.pdf]]

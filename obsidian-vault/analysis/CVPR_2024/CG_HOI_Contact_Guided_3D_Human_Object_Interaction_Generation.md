---
title: "CG-HOI: Contact-Guided 3D Human-Object Interaction Generation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation.pdf
aliases:
- CH
- CG-HOI
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式建模人体表面与物体几何之间的接触距离，并将其作为联合扩散过程中的桥接模态，通过交叉注意力实现人体、物体、接触之间的信息交换，并利用接触预测对物体运动假设进行加权聚合以及推理阶段的接触引导优化。
primary_logic: 接触信息是连接人体与物体运动的关键纽带：物体运动主要由与其密切接触的身体部位驱动，因此联合建模人体、物体和接触三者，并通过接触距离对多部位物体运动假设进行加权，同时利用接触预测在推理时提供梯度引导，能大幅度提升交互生成的物理合理性和语义相关性。
claims:
- 联合生成人体、物体和接触的扩散过程通过交叉注意力有效学习了模态间的相互依赖关系。
- 基于接触距离的物体运动加权方案使得与物体密切接触的身体部位对物体运动有更强的影响，从而生成更合理的物体轨迹。
- 推理阶段的接触引导通过惩罚接触距离的偏离，进一步修正了生成序列中的物理不一致（如物体漂浮）。
- 消融实验表明，移除交叉注意力或接触预测会显著降低生成质量（FID大幅上升），而完整的接触建模带来最佳性能。
---

# CG-HOI: Contact-Guided 3D Human-Object Interaction Generation

> [!tip] 核心洞察
> 接触信息是连接人体与物体运动的关键纽带：物体运动主要由与其密切接触的身体部位驱动，因此联合建模人体、物体和接触三者，并通过接触距离对多部位物体运动假设进行加权，同时利用接触预测在推理时提供梯度引导，能大幅度提升交互生成的物理合理性和语义相关性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CG-HOI：接触引导的三维人-物交互生成 |
| 英文题名 | CG-HOI: Contact-Guided 3D Human-Object Interaction Generation |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CG-HOI |
| Dataset | BEHAVE, CHAIRS |

> [!tip] 效果简介
> - BEHAVE 上，FID (Text-Cond. HOI) 6.31 vs 8.70 (InterDiff) / 9.21 (MDM) (-2.39 / -2.90)；R-Prec. top-3 (Text-Cond. HOI) 0.62 vs 0.53 (InterDiff) / 0.49 (MDM) (+0.09 / +0.13)。
> - CHAIRS 上，FID (Text-Cond. HOI) 6.45 vs 7.53 (InterDiff) / 9.23 (MDM) (-1.08 / -2.78)；R-Prec. top-3 (Text-Cond. HOI) 0.74 vs 0.69 (InterDiff) / 0.53 (MDM) (+0.05 / +0.21)。

## 概述

### 问题与瓶颈

生成逼真且物理合理的三维人-物交互（HOI）序列是具身智能与计算机视觉的核心挑战。现有方法通常孤立地建模人体运动，或假设物体处于静态场景中，忽视了人体与物体运动之间深层的物理依赖关系。这种割裂的建模方式导致生成的交互序列频繁出现物体悬浮、穿透等伪影，且缺乏语义一致性——例如，当文本描述为“搬运椅子”时，生成的椅子轨迹却与手部运动毫无关联。其根本瓶颈在于：**缺乏一个有效的桥接模态来显式捕捉人体表面与物体几何之间的动态接触关系**，从而无法将物体运动与驱动它的身体部位紧密耦合。

### 核心思路

**CG-HOI** 提出以**接触（Contact）**作为连接人体与物体运动的关键纽带，通过联合扩散过程同时生成人体运动、物体运动及人体表面的接触距离，并设计三项核心机制实现模态间的深度耦合：

1. **人体-物体-接触交叉注意力**：在扩散U-Net的每个残差块后插入跨模态交叉注意力模块，使人体、物体、接触三种表征能够相互查询与更新，从而在去噪过程中持续交换信息，学习三者间的相互依赖关系。

2. **基于接触距离的物体运动加权**：为人体表面均匀分布的128个标记点分别预测物体变换假设，并按预测接触距离的倒数进行加权聚合——与物体接触越紧密的身体部位，对物体运动的贡献越大。这一设计使得物体轨迹自然地跟随驱动它的身体部位（如手部搬运椅子时，椅子运动主要由手部决定）。

3. **推理阶段的接触引导优化**：在扩散采样过程中，利用预测接触距离与当前生成序列重算接触距离之间的L2损失梯度，修正每一步的均值估计，强制生成序列在物理接触层面保持一致性，有效抑制物体漂浮等伪影。

### 方法定位

CG-HOI属于**条件运动扩散模型**，其方法谱系可定位于以下坐标：

- **上游范式**：以**MDM**（Tevet et al., ICLR 2023）为代表的人体运动扩散生成框架，以及**InterDiff**（Xu et al., ICCV 2023）为代表的物理信息人-物交互扩散模型。CG-HOI继承了扩散模型在运动生成中的高保真度优势，但通过引入接触模态突破了前两者在物理耦合建模上的局限。

- **关键创新点**：（1）首次在扩散过程中**联合建模人体、物体、接触三模态**，而非仅生成人体运动或将物体作为附属输出；（2）提出**接触引导的物体运动加权方案**，使物体运动与身体接触部位自然关联；（3）在推理阶段引入**接触一致性梯度引导**，提供额外的物理约束。

- **技术基础**：扩散骨干采用U-Net架构，文本条件通过预训练CLIP-ViT-B/32编码，物体几何条件通过PointNet编码，接触距离定义为人体表面标记点到物体几何最近点的距离。

### 主要结果

在**BEHAVE**和**CHAIRS**两个公开数据集上，CG-HOI在文本条件HOI生成任务中显著优于现有方法：

| 数据集 | 指标 | CG-HOI | InterDiff | MDM | 提升幅度 |
|--------|------|--------|-----------|-----|----------|
| BEHAVE | FID ↓ | **6.31** | 8.70 | 9.21 | -27.5% / -31.5% |
| BEHAVE | R-Prec. top-3 ↑ | **0.62** | 0.53 | 0.49 | +17.0% / +26.5% |
| CHAIRS | FID ↓ | **6.45** | 7.53 | 9.23 | -14.3% / -30.1% |
| CHAIRS | R-Prec. top-3 ↑ | **0.74** | 0.69 | 0.53 | +7.2% / +39.6% |

消融实验（Table 2）进一步验证了各组件的关键贡献：移除交叉注意力导致FID从6.31升至10.44，完全移除接触预测使FID升至9.64，移除接触加权方案升至8.54，移除推理引导升至7.22。用户感知研究（Figure 5）也表明参与者显著偏好CG-HOI的生成真实感和文本一致性。此外，CG-HOI展现出良好的灵活性：无需重新训练即可在给定物体轨迹条件下生成对应人体运动，并可直接应用于静态3D场景扫描中的物体交互生成。

## 背景与动机

### 问题背景：三维人-物交互生成的核心挑战

生成逼真的三维人-物交互（Human-Object Interaction, HOI）序列是计算机视觉与图形学中的关键问题，其应用涵盖虚拟现实、机器人学习和动画制作等领域。给定一段文本描述（如“一个人拿起椅子并行走”）和目标物体的几何形状，系统需要同时生成人体运动序列和物体运动轨迹，且两者必须在物理上一致、语义上相关。

该任务的核心难点在于人体运动与物体运动之间存在**强相互依赖**：物体的运动轨迹主要由与之密切接触的身体部位驱动——例如，搬运椅子时椅子的位姿由双手的运动决定，坐在椅子上移动时则由下半身的运动主导（Figure 3）。孤立地生成人体或物体运动，必然导致两者之间缺乏协调，产生物理不合理的结果。

### 现有方法的缺口

当前主流的HOI生成方法存在两个关键局限：

1. **忽视人-物运动的物理耦合**：以**MDM**（Tevet et al., ICLR 2023）为代表的扩散模型仅专注于人体运动生成，虽可通过扩展token和几何条件支持物体运动输出，但其本质上仍将人体与物体视为独立流，缺乏对两者物理依赖关系的显式建模。

2. **依赖静态场景假设**：以**InterDiff**（Xu et al., ICCV 2023）为代表的方法基于观察序列预测交互延续，在动态场景下表现良好，但其核心设计并未显式建模人体表面与物体几何之间的接触关系，导致生成的序列常出现**物体悬浮**或**穿透**等伪影。

上述方法的共同缺陷在于：**缺少一个连接人体运动与物体运动的桥接模态**。接触信息——即人体表面与物体几何之间的距离——天然地编码了人-物交互的物理约束：接触距离的分布直接反映了哪些身体部位正在驱动物体运动，以及物体相对于人体的空间关系。然而，现有工作并未将接触作为显式的生成目标或条件信号。

### 本文动机与核心思路

CG-HOI的提出正是为了填补这一缺口。其核心动机是：**将接触作为人体与物体之间的桥接信息，通过联合建模三者来提升HOI生成的物理合理性与语义一致性**。

具体而言，CG-HOI将人体运动、物体运动和接触距离三者置于统一的去噪扩散过程中联合生成，并通过交叉注意力机制实现模态间的信息交换。在此基础上，模型根据预测的接触距离对多个身体部位的物体运动假设进行加权聚合，使紧密接触的部位主导物体轨迹；在推理阶段，进一步利用接触预测结果计算梯度，引导扩散采样过程朝向物理一致的解空间修正。

这一设计使得CG-HOI能够从根本上缓解物体悬浮和穿透等问题，同时无需重新训练即可适配物体轨迹条件生成和静态场景扫描等下游应用。

## 核心创新

CG-HOI的核心创新在于首次将**接触（Contact）**显式建模为人-物交互生成中的桥接模态，并围绕接触设计了一套完整的联合生成、运动加权与推理优化机制，从而系统性地解决了现有方法中人体与物体运动相互孤立、生成结果物理不合理（如物体悬浮、穿透）的根本瓶颈。

### 创新点一：人体-物体-接触联合扩散与跨模态交叉注意力

现有方法（如MDM、InterDiff）仅独立生成人体运动，或将物体运动作为简单附加输出，缺乏对二者物理依赖关系的显式建模。CG-HOI将**人体运动、物体运动和接触距离**三者统一纳入一个扩散过程，并在U-Net的每个残差块后引入**人体-物体-接触交叉注意力模块**。该模块以人体特征为查询（Query），以物体与接触特征的拼接为键和值（Key/Value），通过缩放点积注意力实现三模态间的信息交换：

$$h_i = \mathrm{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V, \quad Q=H,\ K=V=O \odot C$$

这使得人体运动生成能感知物体几何与当前接触状态，物体运动生成也能反向受人体姿态约束，从而学习到真实的交互依赖关系。消融实验表明，移除交叉注意力后BEHAVE数据集上的FID从6.31急剧升至10.44，R-Precision从0.62降至0.35（Table 2），验证了跨模态信息交换对生成质量的决定性作用。

### 创新点二：基于接触距离的物体运动加权聚合

传统方法直接预测单个物体变换序列，忽视了“物体运动主要由与之密切接触的身体部位驱动”这一物理事实。CG-HOI提出**接触加权方案**：在人体表面均匀采样M=128个标记点，为每个点独立预测一个物体位姿假设$o_i^j$，然后按预测接触距离的倒数进行加权聚合：

$$o_i = \frac{1}{\sum_j \max(|c_i|) - |c_i^j|} \sum_{j=0}^{M-1} (\max(|c_i|) - |c_i^j|) o_i^j$$

这一设计使得与物体紧密接触的身体部位（如搬椅子时的手部）对物体轨迹有更强的主导影响，而远离物体的部位权重自然降低，从而生成更符合物理直觉的物体运动。消融实验证实，移除该加权方案后FID升至8.54（Table 2），且可视化结果中出现明显的物体漂浮伪影（Figure 6）。

### 创新点三：推理阶段的接触引导优化

推理时，CG-HOI在标准扩散采样基础上引入**接触引导**（Contact-Based Diffusion Guidance）。每一步利用预测的接触距离$\bar{c}_t$与从生成的人体-物体几何重算的接触距离$c_t$之间的L2损失，计算梯度并修正扩散均值估计：

$$\hat{\mu}_t = \mu_t + s \Sigma_t \nabla_{x_t} \mathcal{G}(x_t), \quad \mathcal{G}(z_t) = \|c_t - \bar{c}_t\|_2^2, \ s=100.0$$

这一机制在推理阶段额外施加了物理一致性约束，惩罚生成序列中接触距离偏离预测值的程度，从而有效减少物体穿透和悬浮等伪影。消融实验表明，移除接触引导后FID从6.31升至7.22（Table 2），证明推理时的接触优化对提升物理合理性具有独立贡献。

### 创新点四：无需重新训练的物体轨迹条件生成

CG-HOI在推理时可通过简单的**替换注入**策略，将给定的物体运动序列直接注入扩散过程，无需任何重新训练即可生成与之匹配的人体运动。这一能力源于联合扩散框架内在的模态间依赖——交叉注意力已学会从物体运动推断人体响应，使得模型天然支持物体轨迹条件生成（Figure 7），并可应用于静态3D场景扫描中的交互生成（Figure 8）。

## 整体框架

CG-HOI 的整体流程围绕一个核心设计展开：**将接触显式建模为连接人体运动与物体运动的桥接模态**，并在统一的扩散框架中对三者进行联合生成。图 Figure 2 给出了方法的两阶段总览——训练阶段通过跨模态交叉注意力学习人-物-接触的相互依赖，推理阶段则在接触引导下采样以增强物理合理性。

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. Given a text description and object geometry, CG-HOI produces a human-object interaction (HOI) sequence, modeling both human and object motion. To produce realistic HOIs, we additionally model contact to bridge the interdependent motions. Our method jointly generates all three during training (left), using a U-Net-based diffusion with cross-attention across human, object, and contact. During inference (right), we drive synthesis under guidance of estimated contact to sample more physically plausible interactions*

**输入与条件编码。** 系统接收两类条件信号：一段描述交互动作的简短文本 $T$，以及目标物体的静态几何 $G$。文本由预训练的 CLIP-ViT-B/32 编码器 $E_T$ 提取语义特征；物体几何则以世界坐标系下均匀采样的点云形式输入，经在部件分割任务上预训练的 PointNet 编码器 $E_G$ 处理，得到几何条件。这两类条件贯穿整个扩散过程。

**联合扩散生成。** 方法的核心是一个以 U-Net 为骨干的扩散模型，它同时预测人体运动序列 $H$、物体运动序列 $O$ 以及人体表面的接触距离 $C$（定义为 $M=128$ 个均匀分布标记点与物体几何最近点之间的距离）。U-Net 中为人体、物体、接触分别设有独立的残差块，并在每个残差块后插入**人体-物体-接触交叉注意力模块**——这是信息交换的关键枢纽。具体而言，以人体特征为查询 $Q=H$，物体与接触特征的拼接为键和值 $K=V=O \odot C$，通过缩放点积注意力更新人体潜在特征：

$$ h_i = \mathrm{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V $$

物体和接触模态也以类似方式关注其他两种模态，从而在扩散去噪的每一步实现三者的协同演化。训练损失函数对人体参数和物体位姿使用 $L_1$ 损失，对接触距离使用 $L_2$ 损失，权重分别为 $1.0, 0.9, 0.9$。

**接触驱动的物体运动聚合。** 物体运动并非直接生成单一变换序列，而是为 $M$ 个身体接触点分别预测物体位姿假设 $o_i^j$，再按预测接触距离的倒数进行加权聚合（接触越紧密，权重越大）：

$$ o_i = \frac{1}{\sum_j \max(|c_i|) - |c_i^j|} \sum_{j=0}^{M-1} (\max(|c_i|) - |c_i^j|) o_i^j $$

这一方案将物体轨迹的主导权赋予与之密切接触的身体部位（如手部携物时由手部运动决定物体轨迹），从而提升物体运动的合理性。

**推理阶段的接触引导。** 在推理采样时，方法引入基于接触距离的扩散引导：每步计算预测接触与从生成序列重算接触之间的 $L_2$ 损失，以其梯度修正均值估计，强制生成序列满足接触一致性。修正公式为 $\hat{\mu}_t = \mu_t + s \Sigma_t \nabla_{x_t} \mathcal{G}(x_t)$，引导尺度 $s=100.0$。同时采用分类器无关引导（scale=2.5）以平衡多样性与保真度。

**无需重训练的灵活应用。** 该框架支持在推理时注入给定的物体轨迹 $O'$，通过替换式方法将外部物体运动嵌入扩散采样过程，从而生成与之匹配的人体运动，无需重新训练。这一能力可进一步拓展至从静态 3D 场景扫描中分割物体并生成相应的人-物交互序列（Figure 8）。

## 核心模块与公式推导

### 4.1 概率去噪扩散框架

CG-HOI 将人体运动 $H$、物体运动 $O$ 和接触 $C$ 的联合生成建模为一个条件去噪扩散概率过程。给定文本描述 $T$ 和物体几何 $G$，模型学习逆转一个逐步加噪的马尔可夫过程。

**前向扩散过程**：从干净数据 $\mathbf{z}_0 = [H, O, C]$ 开始，逐步添加高斯噪声：

$$q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\sqrt{\beta_t} \mathbf{z}_{t-1} + (1 - \beta_t) \mathbf{I})$$

其中 $\beta_t$ 为第 $t$ 步的噪声方差。利用累积乘积 $\alpha_t = \prod_{s=1}^t (1-\beta_s)$，可直接从 $\mathbf{z}_0$ 采样任意时间步的噪声版本：

$$\mathbf{z}_t = \sqrt{\alpha_t} \mathbf{z}_0 + \sqrt{1 - \alpha_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

**反向去噪过程**：模型学习预测噪声 $\epsilon_\theta(\mathbf{z}_t, t, T, G)$，通过最小化预测噪声与真实噪声之间的差异来训练。去噪网络采用 U-Net 骨干架构，为人体、物体、接触分别设置独立的残差块。

### 4.2 人体-物体-接触交叉注意力

为促进三种模态间的信息交换，在每个残差块后插入自定义的交叉注意力模块。以更新人体特征为例，采用缩放点积注意力（Scaled Dot-Product Attention）：

$$h_i = \mathrm{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V$$

其中查询 $Q$ 来自人体潜在特征 $H$，键 $K$ 和值 $V$ 来自物体特征 $O$ 与接触特征 $C$ 的拼接 $O \odot C$，$d$ 为特征维度。物体和接触特征的更新方式类似，均以自身为查询、其余两种模态的拼接为键值对，形成双向信息流。

该设计使每种模态在去噪过程中能够持续关注其他两种模态的状态，从而学习人体运动、物体运动与接触距离之间的相互依赖关系。

### 4.3 基于接触的物体运动加权

物体轨迹主要由与之密切接触的身体部位驱动（如手部携带物体时主导物体运动）。CG-HOI 在人体表面预定义 $M=128$ 个均匀分布的运动标记点，为每个标记点 $j$ 预测独立的物体变换假设 $o_i^j$，然后按预测接触距离的倒数进行加权聚合：

$$o_i = \frac{1}{\sum_j \max(|c_i|) - |c_i^j|} \sum_{j=0}^{M-1} (\max(|c_i|) - |c_i^j|) o_i^j$$

其中 $c_i^j$ 为第 $j$ 个标记点的预测接触距离（人体表面到物体几何最近点的距离）。接触距离越小，该部位对物体运动的贡献权重越大，确保物体运动紧密跟随与物体接触的身体部位。

### 4.4 训练损失函数

联合训练的总损失由三部分组成：

$$\mathbf{L} = \lambda_h \| h_i - \hat{h}_i \|_1 + \lambda_o \| o_i - \hat{o}_i \|_1 + \lambda_c \| c_i - \hat{c}_i \|_2$$

人体运动参数和物体位姿采用 L1 损失（权重 $\lambda_h=1.0, \lambda_o=0.9$），接触距离采用 L2 损失（权重 $\lambda_c=0.9$），以平衡不同模态的数值尺度。

### 5.1 基于接触的扩散引导

推理阶段引入接触引导以进一步修正物理不一致。给定预测的接触距离 $\bar{c}_t$ 和从当前生成序列重新计算的接触距离 $c_t$，定义引导函数：

$$\mathcal{G}(\mathbf{z}_t) = \| c_t - \bar{c}_t \|_2^2$$

利用该函数的梯度修正每一步的均值估计：

$$\hat{\mu}_t = \mu_t + s \sum_t \nabla_{\mathbf{x}_t} \mathcal{G}(\mathbf{x}_t)$$

其中 $s=100.0$ 为引导尺度。该机制惩罚生成的接触距离偏离预测值，有效减少物体悬浮、穿透等伪影。

### 补充图表

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/003_Figure_3.jpg]]
*Figure 3: An object’s trajectory is largely defined by the motion of the region of the body in close contact with the object, e.g. the hand(s) when carrying an object (left, middle) or the lower body when moving with an object while sitting (right). This informs our contact-based approach to generating object motion*

## 实验与分析

### 主实验结果

CG-HOI在BEHAVE和CHAIRS两个公开数据集上进行了系统评估，并与两个代表性基线方法进行了对比：**MDM**（Tevet et al., ICLR 2023）和**InterDiff**（Xu et al., ICCV 2023）。实验覆盖三种设置：仅文本条件的人体运动生成（Text-Cond. Human Only）、基于观察序列的人-物交互延续预测（Motion-Cond. HOI），以及文本条件的人-物交互生成（Text-Cond. HOI）。评估指标包括FID、R-Precision top-3、Diversity和MultiModality，同时辅以用户感知研究。

在核心的文本条件HOI生成任务上，CG-HOI在两个数据集上均取得最优性能。在BEHAVE数据集上，FID降至6.31，相比InterDiff的8.70降低了2.39，相比MDM的9.21降低了2.90；R-Precision top-3达到0.62，分别超出InterDiff和MDM 0.09和0.13。在CHAIRS数据集上，FID为6.45，优于InterDiff的7.53和MDM的9.23；R-Precision top-3为0.74，比InterDiff高0.05，比MDM高0.21。这些结果表明，CG-HOI生成的交互序列在分布匹配度和文本语义一致性上均显著优于现有方法。

在仅评估人体运动质量（Human Only）和运动条件HOI预测两种设置下，CG-HOI同样保持领先，体现了联合建模人体、物体和接触三者的综合优势。定性比较（Figure 4）进一步显示，CG-HOI生成的交互序列明显减少了穿透和物体悬浮等物理伪影，接触区域的贴合度更高。用户感知研究（Figure 5）证实，参与者在整体真实感和文本一致性上显著偏好CG-HOI的生成结果。

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison to state-of-the-art methods MDM [73] and InterDiff [88]. Our approach generates high-quality HOIs by jointly modeling contact (closer contact in red), reducing penetration and floating artifacts (black highlight boxes)*

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/006_Figure_5.jpg]]
*Figure 5: Perceptual User Study. Participants significantly favor our method over baselines, for overall realism and text coherence*

### 消融实验

为量化各设计组件的贡献，论文进行了系统的消融实验（Table 2），以BEHAVE数据集上的文本条件HOI生成为基准。

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/007_Table_2.jpg]]
*Table 2: Ablation on our design choices. Joint contact prediction with cross-attention encourages the generation of more natural HOIs, and our weighting scheme and inference-time contact guidance together enable the best generation performance*

**移除交叉注意力（No cross-attention）**导致FID从6.31急剧上升至10.44，R-Precision从0.62降至0.35，性能退化最为严重。这验证了人体-物体-接触交叉注意力模块对学习模态间相互依赖关系的核心作用——仅靠独立处理各模态无法捕捉交互的动态耦合。

**完全移除接触预测（No contact prediction）**使FID升至9.64，表明接触信息作为连接人体与物体运动的桥接模态不可或缺。缺少接触预测时，模型失去了推断物体应如何响应人体运动的关键线索。

**移除接触加权方案（No contact weighting）**导致FID上升至8.54。该消融将物体运动生成从多部位加权聚合改为直接预测单一变换，证实了基于接触距离的加权机制能有效使物体运动紧密跟随与之密切接触的身体部位，从而提升物体轨迹的合理性。

**移除推理时的接触引导（No contact guidance）**使FID升高到7.22，证明推理阶段的接触一致性约束提供了额外的物理合理性修正，能进一步抑制物体漂浮等伪影。

**使用离线独立训练的接触预测模型（Separate contact pred.）**替换联合训练方案，FID为8.01，远不及联合训练的6.31。这凸显了在扩散过程中联合学习人体、物体和接触三者的协同优势——独立预测无法充分捕捉模态间的动态交互。

消融实验的可视化（Figure 6）直观展示了各组件缺失时的典型失败模式：缺少接触加权或引导时，生成序列出现明显的物体漂浮现象，物体与人体之间的空间关系失去物理合理性。

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of ablations of our method design: Generation, weighting, and inference-time guidance work together to enable realistic interactions in our method, resolving artifacts such as object floating*

### 失败模式与局限性分析

尽管CG-HOI在整体性能上表现优异，论文明确指出以下局限性：

1. **单物体交互限制**：当前方法仅支持人与单个物体的交互，难以处理涉及多个物体协同的长时动作序列（如烹饪流程中依次操作多个厨具），限制了其在复杂场景下的应用范围。
2. **数据依赖性**：模型训练依赖高质量的三维人-物交互动捕数据（如BEHAVE和CHAIRS），此类数据采集成本高且物体类别多样性有限，可能阻碍模型向更广泛的物体类别和交互类型泛化。
3. **细粒度控制不足**：文本描述仅提供高层动作语义，无法精确控制交互的细腻细节（如手部的具体抓取方式），生成结果的细粒度可控性有待提升。
4. **物理约束的边界**：虽然接触建模增强了物理合理性，但并未显式引入动力学或接触力约束，某些生成的交互仍可能存在轻微的物理偏差。接触度量目前仅基于距离，尚未扩展到穿透深度、相对速度等更丰富的几何特征。

### 重要图表结论

- **Table 1**：CG-HOI在BEHAVE和CHAIRS两个数据集的所有评估设置下均优于MDM和InterDiff，验证了联合建模人体、物体和接触的有效性。
- **Table 2**：消融实验量化证实，交叉注意力、接触预测、接触加权和推理引导四个组件对性能均有显著贡献，其中交叉注意力的移除导致最大性能退化。
- **Figure 4**：定性对比显示CG-HOI生成的交互序列具有更紧密的接触贴合度和更少的穿透/悬浮伪影。
- **Figure 5**：用户研究结果从感知层面验证了CG-HOI在真实感和文本一致性上的优势。
- **Figure 6**：消融可视化直观揭示了缺少接触加权或引导时物体漂浮等典型失败模式。

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art approaches MDM [73] and InterDiff [88]. Human Only results are evaluated only on the human pose sequence, and motion-cond. denotes predictions additionally conditioned on past observations of both human and object behavior. For metrics with →, results closer to the real distribution are better. Our approach outperforms these baselines in all three settings, indicating a strong learned correlation between human and object motion*

### 补充图表

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/010_Figure_7.jpg]]
*Figure 7: Given an object trajectory at inference time, our method can generate corresponding human motion without re-training*

![[assets/figures/papers/paper_list_l1710_CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation/figures/009_Figure_8.jpg]]
*Figure 8: Application to static 3D scene scans. Our method can generate HOIs from segmented objects in such environments*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

CG-HOI 处于三维人-物交互（HOI）生成这一新兴方向，其核心贡献在于首次将**接触（contact）**显式建模为连接人体运动与物体运动的桥接模态，并在联合扩散框架中进行生成。与现有工作的关系可从以下两条脉络理解。

**相对于人体运动生成方法的扩展。** 以 **MDM**（Tevet et al., ICLR 2023）为代表的扩散模型在纯人体运动生成上取得了显著进展，但其设计并未考虑物体运动，无法处理交互场景。CG-HOI 在 MDM 的扩散框架基础上，将生成空间从单一人体表征扩展为**人体-物体-接触**三元联合表征，并通过交叉注意力实现跨模态信息交换。这一扩展并非简单的维度增加——消融实验表明，仅扩展 token 而不引入接触建模（即 MDM 的 HOI 适配版）在 BEHAVE 数据集上的 FID 高达 9.21，而 CG-HOI 降至 6.31，说明**接触作为中间模态是学习人-物相互依赖关系的关键**。

**相对于物理信息 HOI 预测方法的改进。** **InterDiff**（Xu et al., ICCV 2023）首次将扩散模型应用于 HOI 生成，通过观察序列预测未来交互，并引入了初步的物理约束。CG-HOI 在此基础上做出了三个重要改进：
1. **接触预测替代隐式物理约束**：InterDiff 通过物理损失间接约束交互合理性；CG-HOI 则直接预测人体表面与物体几何之间的接触距离（128 个均匀标记点的最近点距离），将物理合理性转化为可学习、可引导的显式信号。
2. **多部位物体运动假设与接触加权聚合**：InterDiff 直接生成单个物体变换序列；CG-HOI 为人体表面多个接触点分别预测物体变换假设，并按预测接触距离的倒数加权求和（$o_i = \frac{1}{\sum_j \max(|c_i|) - |c_i^j|} \sum_{j=0}^{M-1} (\max(|c_i|) - |c_i^j|) o_i^j$），使物体运动紧密跟随与之密切接触的身体部位（如手部搬运物体时主导物体轨迹，见图 3）。
3. **推理阶段接触引导**：InterDiff 在推理时无显式物理约束；CG-HOI 引入基于接触距离的扩散引导（$\hat{\mu}_t = \mu_t + s \sum_t \nabla_{x_t} \mathcal{G}(x_t)$，引导尺度 $s=100.0$），通过惩罚预测接触与重算接触之间的 L2 偏差，在采样过程中主动修正物理不一致。

**方法定位总结**：CG-HOI 不是对现有 HOI 生成方法的简单改进，而是**重新定义了问题的建模方式**——将接触从隐式约束提升为一等公民的生成模态。这一设计选择使得模型能够显式学习“哪个身体部位在驱动物体运动”这一因果机制，从而在 BEHAVE 和 CHAIRS 两个数据集上均显著优于 MDM 和 InterDiff（FID 分别降低 2.39–2.90 和 1.08–2.78，R-Precision top-3 分别提升 0.09–0.13 和 0.05–0.21，见表 1）。

### 2. 适用边界

CG-HOI 的核心假设与适用边界如下：

**输入条件要求**：
- **文本描述**：需提供高层动作语义（如“a person sits on a chair”），由 CLIP-ViT-B/32 编码器提取特征。文本仅提供动作类别层面的引导，无法精确控制交互的细粒度细节（如手的抓取方式、接触力的大小）。
- **物体几何**：需提供静态物体的三维几何（世界坐标系下均匀采样的点云），由预训练 PointNet 编码。模型假设物体为刚体，不处理可变形物体（如衣物、绳索）。

**交互类型限制**：
- **单物体交互**：当前方法仅支持人与单个物体的交互。对于涉及多个物体协同的长时动作序列（如烹饪流程中依次操作多个厨具），需要将框架扩展为多物体联合生成，这在当前架构下尚未实现。
- **单人交互**：不涉及多人协作场景（如两人抬桌子）。

**数据依赖性**：
- 模型训练依赖高质量的三维人-物交互动捕数据（BEHAVE、CHAIRS），此类数据采集成本高、物体类别有限（以椅子和桌子为主）。向更广泛物体类别和交互类型的泛化能力受限于训练数据的多样性。
- 在 CHAIRS 数据集上按物体类别划分训练/测试集（80/10/10）的实验表明，模型对训练中未见过的物体实例具有一定泛化能力，但未见物体类别（如从椅子泛化到箱子）的性能仍需验证。

**物理合理性的边界**：
- 接触建模增强了物理合理性，但并未显式引入动力学约束（如接触力、摩擦力）或穿透深度惩罚。消融实验可视化（图 6）显示，移除接触引导后物体漂浮伪影增加，但完整模型仍可能在极端姿态下产生轻微穿透。
- 接触引导的尺度参数 $s=100.0$ 是在当前数据集上调优的经验值，在不同场景下可能需要调整。

### 3. 局限与开放问题

**当前局限**：
1. **单物体、单人限制**：无法处理多物体协同或多人交互的复杂日常行为，限制了在真实场景（如厨房操作、协作搬运）中的应用。
2. **数据饥渴**：依赖昂贵的三维动捕数据，物体类别和交互类型的多样性有限，阻碍向开放世界物体和动作的泛化。
3. **细粒度控制不足**：文本条件仅提供高层语义，无法精确控制抓取方式、接触部位、力的大小等细腻交互细节。手部姿态参数（如 MANO）尚未纳入生成框架。
4. **接触度量的简化**：当前接触仅定义为最近点距离（标量），未区分接触类型（如推、拉、握）或接触方向，信息维度有限。
5. **刚体假设**：物体被假设为刚体，不适用于可变形物体的交互（如折叠衣物、捏橡皮泥）。

**开放问题**：
1. **多物体、多人扩展**：如何将接触引导的联合扩散框架扩展到多物体、多人交互场景？可能的路径包括：引入物体间/人与人之间的接触图、使用层次化生成策略（先规划高层交互图，再生成具体运动）、或采用自回归方式逐步生成多物体序列。
2. **数据效率提升**：能否通过弱监督或利用大规模二维动作数据（如视频）来减少对昂贵三维动捕数据的依赖？可能的路径包括：从视频中提取二维接触线索作为弱监督信号、使用预训练的视频-运动模型进行跨模态蒸馏、或利用物理模拟器生成合成训练数据。
3. **更丰富的接触语义**：如何将接触度量从距离扩展到更丰富的几何和物理特征？可能的扩展包括：接触法向方向、相对速度、穿透深度、接触力估计等。这些特征可以增强接触引导的物理正确性，并为精细控制提供接口。
4. **手部姿态与抓取合成**：如何将手部姿态参数（如 MANO 模型）纳入联合生成框架，实现从“身体-物体接触”到“手-物体抓取”的细粒度生成？这需要解决手部姿态的高维性和抓取多样性的问题。
5. **与物理模拟器的闭环结合**：当前接触引导是一种软约束，无法保证严格的物理正确性。未来可探索将扩散模型的生成结果作为物理模拟器的初始化，通过少量模拟步数进行物理修正，或使用可微分物理模拟器提供更强的梯度信号。
6. **交互意图理解与可控生成**：如何从文本中提取更精细的交互意图（如“轻轻拿起” vs “用力推”），并将其映射为接触力、速度等可控参数？这需要构建文本到物理参数的映射模型，或在扩散条件中引入更结构化的交互描述。

**注**：以上开放问题中，关于多物体扩展和手部姿态合成的部分在论文中未提供直接证据，属于基于方法逻辑的合理推演，需后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2024/CG_HOI_Contact_Guided_3D_Human_Object_Interaction_Generation.pdf]]
---
title: HOIDiffusion Generating Realistic 3D Hand Object Interaction Data
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data.pdf
aliases:
- HGR3HOID
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过法线图、手-物分割图以及手部2D骨架投影作为结构条件，实现几何与外观的解耦控制。
primary_logic: 将预训练扩散模型的丰富视觉先验与3D几何条件（法线、分割、骨架）相结合，并引入背景正则化防止风格过拟合，从而在保留文本编辑能力的同时生成逼真且可控的手-物体交互数据。
claims:
- HOIDiffusion在FID上显著低于所有基线，表明生成图像具有更高保真度
- HOIDiffusion在手-物体接触召回率(Contact Recall)和关键点准确率(PCK)上均优于基线，证明几何一致性更好
- 完整结构控制（法线+分割+骨架）实现最低FID
- 背景正则化模块有效缓解微调时的风格漂移，提升文本-图像对齐(CLIPScore)
---

# HOIDiffusion Generating Realistic 3D Hand Object Interaction Data

> [!tip] 核心洞察
> 将预训练扩散模型的丰富视觉先验与3D几何条件（法线、分割、骨架）相结合，并引入背景正则化防止风格过拟合，从而在保留文本编辑能力的同时生成逼真且可控的手-物体交互数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOIDiffusion：生成逼真的3D手—物体交互数据 |
| 英文题名 | HOIDiffusion Generating Realistic 3D Hand Object Interaction Data |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://mq-zhang1.github.io/HOIDiffusion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HOIDiffusion |
| Dataset | DexYCB, Hand Contact Recall, PCK, NOCS 物体6D姿态估计 |

> [!tip] 效果简介
> - DexYCB (生成图像质量评估) 上，FID ↓ 55.22 vs ControlNet 87.99 (LDM 63.71) (-32.77 vs ControlNet)。
> - DexYCB (手-物体交互生成) 上，sFID ↓ 91.28 vs DreamBooth 92.82 (-1.54)。
> - DexYCB (生成多样性) 上，IS ↑ 7.73 vs DreamBooth 7.99 (-0.26)。

## 概述

**核心问题**：现有文本到图像扩散模型（如Stable Diffusion）在生成手—物体交互场景时存在严重缺陷——手指数量错误、抓取姿态不自然、物体与手部空间关系混乱。根本原因在于，纯文本条件无法为扩散模型提供精确的3D几何约束，导致生成结果在物理和几何上不可靠。

**方法定位**：HOIDiffusion提出一种两阶段可控生成框架，将预训练扩散模型的丰富视觉先验与显式3D几何条件解耦结合。第一阶段基于物体模型生成手部抓取轨迹，提取法线图、手—物分割图和手部2D骨架投影作为结构条件；第二阶段通过注入三个条件编码器微调Stable Diffusion，并引入背景缓冲正则化防止微调导致的风格过拟合与文本编辑能力退化。

**核心发现**：几何与外观的解耦控制是生成逼真手—物交互数据的关键。完整的三重结构条件（法线+分割+骨架）缺一不可，任一缺失均导致生成质量显著下降（Table 4）。背景正则化模块对保持文本编辑灵活性至关重要——无正则化时CLIPScore从0.79骤降至0.66（Table 5）。

**主要结果**：
- **图像质量**：HOIDiffusion在DexYCB上取得FID 55.22，显著优于ControlNet（87.99）和微调LDM（63.71），降幅达32.77（Table 1）。
- **几何一致性**：手—物体接触召回率均值达95.49%，手部关键点准确率（PCK）为0.85，均优于所有基线方法（Table 2）。
- **下游任务验证**：将生成数据用于NOCS物体6D姿态估计训练，在DualPoseNet上IoU@25达90.9，5°2cm达29.2，较原始方法均有提升（Table 3），证明合成数据具备实际应用价值。
- **零样本视频生成**：利用跨帧交叉注意力机制，框架可扩展至抓取轨迹的视频生成，初步缓解帧间闪烁问题（Figure 6）。

**方法谱系与知识库定位**：HOIDiffusion建立在Stable Diffusion（Rombach et al., CVPR 2022）的预训练权重之上，与DreamBooth（Ruiz et al., CVPR 2023）和ControlNet（Zhang et al., ICCV 2023）同属可控文本到图像生成范式，但区别于二者的是：DreamBooth面向个性化主体保留，ControlNet提供通用多条件控制，而HOIDiffusion专攻手—物体交互这一细粒度物理场景，通过3D几何条件注入实现结构精确可控的交互数据合成。

**局限与开放问题**：训练数据仅使用DexYCB，物体类别有限，极端未见物体形状下的几何一致性未经充分验证。当前框架依赖精确的3D条件输入，若法线或分割存在噪声，生成质量可能下降。如何扩展至双手交互、全身人体—物体交互，以及结合更强视频扩散模型生成长序列，是值得探索的方向。生成数据在真实机器人操作任务中的有效性仍需实验验证。

## 背景与动机

### 问题背景

生成逼真的手—物体交互（Hand-Object Interaction, HOI）图像是计算机视觉与图形学中的关键挑战，其应用涵盖机器人抓取学习、增强现实、人机交互等领域。然而，现有文本到图像生成模型在这一任务上存在根本性缺陷：它们无法生成物理和几何上合理的手—物体交互图像，常见问题包括手指数量错误、抓取姿态不自然，且缺乏对3D几何结构的精确控制。这一问题源于纯2D扩散模型仅从文本和图像分布中学习，缺少对三维空间关系的显式建模能力。

### 现有方法缺口

当前主流的可控图像生成方法在HOI场景下均存在明显不足：

- **Stable Diffusion / LDM**（Rombach et al., CVPR 2022）：直接微调后仍无法保证手部与物体的正确接触几何，生成的手部姿态常出现解剖学错误。
- **ControlNet**（Zhang et al., ICCV 2023）：虽支持多条件控制，但其条件信号（如边缘图、深度图）缺乏对手—物体接触边界的精细刻画，导致抓取姿态不自然。
- **DreamBooth**（Ruiz et al., CVPR 2023）：侧重于个性化主体生成，对物理交互结构的保持能力有限。

这些方法的共同瓶颈在于：**条件信号与3D几何结构之间存在语义鸿沟**。它们无法将手部关节姿态、物体表面法向、接触区域分割等信息有效地注入生成过程，导致生成的图像在几何一致性和物理合理性上不可靠。

### 本文动机

针对上述缺口，本文提出核心洞察：**将预训练扩散模型的丰富视觉先验与3D几何条件（法线图、手—物分割图、手部骨架投影）相结合，并引入背景正则化防止风格过拟合，从而在保留文本编辑能力的同时生成逼真且可控的手—物体交互数据。**

具体而言，HOIDiffusion通过以下机制突破现有瓶颈：
1. **几何与外观解耦控制**：以法线图、分割图和骨架投影作为结构条件，使模型学习形状先验，同时通过文本控制外观风格，实现“固定几何、改变风格”或“固定风格、改变几何”的灵活生成。
2. **背景正则化**：利用合成背景图像构建缓冲器，通过联合损失防止微调时风格漂移，保持预训练模型的文本编辑能力。

这一设计使得HOIDiffusion能够生成高保真度、几何准确的HOI图像，并可直接用于下游任务（如物体6D姿态估计）的性能提升。

## 核心创新

HOIDiffusion 的核心创新在于**将3D几何结构控制与预训练扩散模型的视觉先验深度融合**，解决了文本到图像扩散模型在手-物体交互（HOI）场景下的两大瓶颈：（1）物理几何不合理（手指数量错误、抓取姿态不自然）；（2）几何与外观耦合导致无法独立控制。以下从三个关键维度剖析其相对于基线的创新点。

### 1. 结构条件输入：从纯文本到多模态几何控制

**基线方案**（LDM、DreamBooth、ControlNet）仅依赖文本提示或通用边缘图作为条件，缺乏对手-物体交互场景中精细3D几何结构的显式建模。HOIDiffusion 引入了三类互补的结构条件（Section 3.3，Figure 3）：

| 条件类型 | 作用机制 | 解决的核心问题 |
|---------|---------|--------------|
| **法线图** | 编码物体表面几何和光照信息，引导模型感知三维形状 | 物体形状失真、纹理与几何不匹配 |
| **手-物分割图** | 提供手部与物体的清晰边界，强制模型区分交互区域 | 手物边界模糊、穿透伪影 |
| **手部2D骨架投影** | 精确刻画手部关节的空间位置和姿态 | 手指数量错误、抓取姿态不自然 |

这三类条件通过独立的编码器注入 Stable Diffusion 的 U-Net（Adapter 方式），实现了几何与外观的**解耦控制**——用户可固定结构条件而改变文本描述来控制风格，或固定文本而替换结构条件来改变交互姿态（Figure 1）。消融实验（Table 4）证实：移除任一条件模块均导致 FID 显著上升（完整模型 FID 77.64），证明三者缺一不可。

### 2. 外观正则化：防止微调中的风格过拟合

**关键洞察**：直接在 DexYCB 等小规模 HOI 数据集上微调 Stable Diffusion 会导致模型遗忘预训练阶段的多样化视觉先验，出现“风格坍缩”——生成图像趋于训练集的实验室背景风格，丧失文本编辑能力。

HOIDiffusion 提出了**背景缓冲正则化**策略（Section 3.3，Equation 3）：利用预训练模型合成多样化背景图像构建缓冲器，在微调时联合优化 HOI 图像和背景图像的噪声预测损失：

$$\mathcal{L} = E_{x_0, x_r, \epsilon, \epsilon_r} [||\epsilon - f_{\theta}(\sqrt{\overline{\alpha_t}} x_0 + \sqrt{1-\overline{\alpha_t}} \epsilon, t)||^2 + w_r ||\epsilon_r - f_{\theta}(\sqrt{\overline{\alpha_t}} x_r + \sqrt{1-\overline{\alpha_t}} \epsilon_r, t)||^2]$$

其中 $x_r$ 为背景缓冲图像，$w_r=1$ 平衡两项损失。该正则化强制模型在保留 HOI 结构控制能力的同时，维持对多样化背景的生成能力。

**决定性证据**（Table 5）：引入正则化后 CLIPScore 从 0.66 提升至 0.79，定性结果（Figure 7）显示模型可在不同背景提示下生成多样化图像，而无正则化时则趋于训练集风格。

### 3. 两阶段管线：几何先验与外观生成的因果衔接

HOIDiffusion 采用**两阶段框架**（Figure 2），将几何生成与外观合成解耦：

- **第一阶段**（抓取轨迹生成）：基于物体模型，利用预训练的 GrabNet 生成手部抓取姿势，并通过球面线性插值得到完整轨迹，输出法线图、分割图和骨架投影作为第二阶段的结构条件。
- **第二阶段**（条件扩散图像合成）：以第一阶段输出的几何条件和 LLaVA 生成的详细文本描述为条件，通过微调的 Stable Diffusion 生成逼真图像。

这一设计的关键因果机制在于：**3D几何条件作为“结构骨架”约束图像生成，而文本条件则填充外观细节**。与 ControlNet 等通用条件框架相比，HOIDiffusion 的条件设计专门针对 HOI 场景的物理约束进行了定制，从而在接触召回率（Mean Contact Recall 95.49%）和关键点准确率（PCK 0.85）上显著超越基线（Table 2）。

### 创新点总结

| 创新维度 | 基线方案 | HOIDiffusion 方案 | 证据强度 |
|---------|---------|------------------|---------|
| 条件控制 | 纯文本/通用边缘图 | 法线+分割+骨架三通道几何条件 | Table 4 消融验证 |
| 训练策略 | 标准微调 | 背景缓冲正则化+分类器自由引导 | Table 5 CLIPScore 提升 |
| 数据生成 | 无结构先验 | GrabNet 抓取轨迹生成→条件扩散合成 | Table 2 接触召回率优势 |
| 几何-外观解耦 | 耦合 | 结构条件与文本条件独立控制 | Figure 1 定性展示 |

**局限性提示**：该方法依赖精确的3D几何条件输入，若提供的法线、分割或骨架有噪声，生成质量可能下降；训练数据仅使用 DexYCB，物体类别有限，极端未见物体形状下的几何一致性未经充分验证。

## 整体框架

HOIDiffusion 采用**两阶段流水线**，核心思路是“先构造3D几何条件，再以几何条件驱动图像生成”，从而实现几何结构与外观纹理的解耦控制。

### 阶段一：手部抓取轨迹生成

第一阶段的目标是为后续的图像合成提供精确的3D几何控制信号。给定一个物体的3D模型，框架首先利用预训练的 **GrabNet**（Taheri et al.）生成手部对该物体的抓取终止姿态。GrabNet 以物体的 BPS（Body Part Segmentation）编码为条件，通过变分自编码器输出手部的3D网格姿态。随后，在起始姿态（手远离物体）与终止抓取姿态之间使用**球面线性插值**生成完整的手部接近与抓取轨迹。该轨迹为每一帧提供了手部与物体的精确3D位姿，从而可以渲染出三类几何条件图：**法线图**、**手-物体分割图**以及**手部2D骨架投影**。

### 阶段二：条件扩散图像合成

第二阶段以第一阶段输出的几何条件图和文本描述为双重条件，通过微调的 Stable Diffusion 模型生成逼真的手-物体交互图像。具体而言，三个条件编码器分别处理法线图、分割图和骨架投影，将提取的条件特征通过 **Adapter** 方式注入到 U-Net 的编码器层中。这种设计使得模型在保留预训练扩散模型丰富视觉先验的同时，获得了对3D几何结构的精确控制能力。

### 外观正则化模块

直接在 DexYCB 等实验室环境数据集上微调会导致模型过拟合到训练集的背景风格，丧失文本编辑的灵活性。为此，HOIDiffusion 引入了**背景缓冲正则化**策略：利用预训练 Stable Diffusion 合成大量多样化背景图像，构建背景缓冲器。训练时，模型在真实 HOI 图像和背景缓冲图像上联合优化去噪损失：

$$
\mathcal{L} = E_{x_0, x_r, \epsilon, \epsilon_r} \left[ \|\epsilon - f_\theta(\sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, t)\|^2 + w_r \|\epsilon_r - f_\theta(\sqrt{\bar{\alpha}_t} x_r + \sqrt{1-\bar{\alpha}_t} \epsilon_r, t)\|^2 \right]
$$

其中 $x_0$ 为真实 HOI 图像，$x_r$ 为背景缓冲图像，$w_r=1$。该正则化项强制模型在背景区域保持预训练模型的先验分布，从而有效缓解微调带来的风格漂移。

### 输入输出流

整个框架的输入为：① 物体3D模型（mesh）；② 描述场景、物体外观和背景的文本提示。输出为：与3D几何条件严格对齐、且外观可由文本灵活控制的高保真手-物体交互图像。通过固定几何条件而改变文本输入，可以控制背景和物体外观风格；通过固定文本而改变几何条件，可以控制手部姿态和物体形状——这正是 Figure 1 所展示的几何与外观解耦生成能力。

### 补充图表

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline. We propose a two-stage pipeline to synthesize hand-object-interaction data. During the first stage, we utilize a pretrained GrabNet to output 3D hand poses given by a single object model. Then in the second stage, we use those 3D hand poses along with segmentation maps, normal maps and skeletons to conditionally generate high-quality HOI data*

## 核心模块与公式推导

HOIDiffusion 的核心架构建立在预训练 Stable Diffusion 之上，通过注入三个并行的条件编码器实现几何与外观的解耦控制，并引入背景缓冲正则化以保持文本编辑能力。

### 扩散模型基础

模型沿用标准去噪扩散概率模型（DDPM）框架。给定带噪图像 $x_t$ 和时间步 $t$，U-Net 模型 $f_\theta$ 预测当前步的噪声分量：

$$\hat{\epsilon_t} = f_{\theta}(x_t, t)$$

基于预测噪声，通过反向扩散过程估计上一时间步的图像：

$$x_{t-1} = \frac{1}{\sqrt{\alpha_t}} (x_t - \frac{1-\alpha_t}{\sqrt{1-\overline{\alpha}_t}} \hat{\epsilon_t}) + \sigma_t z$$

其中 $\alpha_t$ 和 $\overline{\alpha}_t$ 为噪声调度参数，$\sigma_t$ 为反向过程的标准差，$z \sim \mathcal{N}(0, I)$ 为随机噪声。该公式构成了所有条件生成的基础推理步骤（Equation 1, 2）。

### 三路条件编码器注入

HOIDiffusion 的核心创新在于将三类几何结构条件通过 Adapter 方式注入 Stable Diffusion 的 U-Net 编码器（Figure 3）。三个条件编码器分别处理：

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/003_Figure_3.jpg]]
*Figure 3: Model Figure. We inject three conditional encoders into the stable diffusion model. We utilize both the HOI datasets and high-quality background images to train HOIDiffusion. The background images are synthesized using the scenery prompts. The texts sent to the model are output by LLaVA for detailed description*

1. **法线图（Normal Map）**：从 3D 手-物体模型中渲染的表面法线，引导模型感知表面纹理与光照关系。
2. **手-物体分割图（Hand-Object Segmentation）**：提供手部与物体的清晰边界，帮助模型区分交互区域。
3. **手部 2D 骨架投影（Skeleton Projection）**：将 3D 手部关键点投影到图像平面，精确定义手部关节姿态。

三个条件编码器的输出特征在 U-Net 编码器的各层以加权求和方式注入，权重记为 $(h, n, s)$，分别对应手部投影、法线图和分割图（Table 7）。这种多条件并行注入的设计使得模型能够同时约束手部姿态、物体形状和接触边界，实现几何结构的精确控制。

### 外观正则化联合损失

直接微调 Stable Diffusion 会导致模型过拟合训练集的背景风格，丧失文本编辑能力。HOIDiffusion 引入背景缓冲正则化（Background Buffer Regularization）来解决这一问题。具体而言，利用预训练模型基于风景提示词合成一批高质量背景图像 $x_r$，与真实 HOI 图像 $x_0$ 混合训练，联合损失函数为：

$$\mathcal{L} = E_{x_0, x_r, \epsilon, \epsilon_r} [||\epsilon - f_{\theta}(\sqrt{\overline{\alpha_t}} x_0 + \sqrt{1-\overline{\alpha_t}} \epsilon, t)||^2 + w_r ||\epsilon_r - f_{\theta}(\sqrt{\overline{\alpha_t}} x_r + \sqrt{1-\overline{\alpha_t}} \epsilon_r, t)||^2]$$

其中 $\epsilon$ 和 $\epsilon_r$ 分别为真实 HOI 图像和背景缓冲图像对应的采样噪声，$w_r = 1$ 为背景正则化项的权重（Equation 3）。该损失函数在保持模型对 HOI 场景拟合能力的同时，强制模型保留对多样化背景的生成能力，从而缓解微调带来的风格漂移。

### 两阶段管线模块

整个方法由两个核心模块串联构成（Figure 2）：

**第一阶段：手部抓取轨迹生成。** 给定物体 3D 模型，利用预训练的 GrabNet（基于 BPS 编码的 VAE 模型）生成手部抓取终止姿态，再通过球面线性插值（Slerp）生成从初始位置到抓取位置的完整轨迹。该阶段输出每帧的 3D 手部姿态和物体位姿，为第二阶段提供几何条件（分割图、法线图、骨架投影）的渲染依据。

**第二阶段：条件扩散图像合成。** 以上述几何条件与 LLaVA 生成的详细文本描述共同作为输入，通过三路条件编码器注入微调的 Stable Diffusion，生成逼真的手-物体交互图像。训练时结合背景缓冲正则化，推理时支持分类器自由引导（Classifier-Free Guidance）以增强条件遵循度。

## 实验与分析

### 主实验结果

#### 生成图像质量与文本对齐

HOIDiffusion 在 DexYCB 数据集上对所有基线方法展现出显著的图像质量优势。如 Table 1 所示，HOIDiffusion 取得了最低的 FID（55.22），相比微调后的 **LDM**（Rombach et al., CVPR 2022）的 63.71 降低了 8.49，相比 **ControlNet**（Zhang et al., ICCV 2023）的 87.99 更是大幅降低了 32.77。这表明引入 3D 几何条件（法线图、分割图、骨架投影）后，生成图像与真实 HOI 图像分布的距离显著缩小，保真度更高。

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with previous baseline methods. All models are trained on the DexYCB. We use FID to directly measure the synthesis quality of generated hand-object interaction images. sFID is a recently proposed metric to evaluate image quality using higher-level spatial features. IS is measured for diversity and CLIPScore is to evaluate generated images alignment with provided prompts*

在空间感知质量指标 sFID 上，HOIDiffusion 达到 91.28，略优于 **DreamBooth**（Ruiz et al., CVPR 2023）的 92.82（降低 1.54），说明高层空间特征层面的生成质量同样领先。在多样性指标 IS 上，HOIDiffusion 为 7.73，略低于 DreamBooth 的 7.99（差距 0.26），但考虑到 FID 的大幅优势，这一微小差距是可控的——模型在保真度与多样性之间取得了更优的权衡。

文本-图像对齐方面，HOIDiffusion 的 CLIPScore 为 0.78，与 ControlNet 的 0.77 基本持平。这表明引入强几何条件并未牺牲文本控制能力，模型仍能根据文本描述生成相应外观。

#### 手部交互几何准确性

从手部视角评估，HOIDiffusion 在接触质量和关键点精度上均显著优于基线。如 Table 2 所示，Mean Contact Recall 达到 95.49%，表明生成图像中的手部末端姿态与物体保持了高度紧密的接触关系。在 PCK（关键点正确率）上，HOIDiffusion 取得了 0.85 的最高分，说明生成的手部姿态在 2D 投影上与真实几何条件高度一致。

这些结果验证了核心设计思路的有效性：通过注入法线图、手-物分割图和手部骨架投影三种结构条件，模型能够学习到精确的几何先验，从而生成物理上合理的手-物体交互姿态。相比之下，纯文本条件的方法（如 LDM、DreamBooth）缺乏对 3D 几何的显式控制，容易出现手指数量错误或抓取姿态不自然的问题。

#### 下游任务验证

为验证生成数据的实用价值，论文将 HOIDiffusion 生成的图像用于训练 NOCS 物体 6D 姿态估计模型。如 Table 3 所示，以 DualPoseNet 为基准，使用 HOIDiffusion 生成的训练数据后，IoU@25 从原始水平提升至 90.9，5°2cm 指标提升至 29.2，在所有指标上均有改善。这证明生成的 HOI 图像不仅视觉质量高，而且包含足够的几何信息来增强下游感知任务。

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation on NOCS. We use SPD and DualPoseNet and change the synthesized images in the dataset with our generated images for training. Our performance improve on all metrics with DualPoseNet and all cm metrics with SPD which demonstrates the good quality of our images and can be utilized for downstream tasks*

### 消融实验

#### 结构控制组件的必要性

Table 4 的消融实验系统验证了三种几何条件的各自贡献。完整模型（法线 + 分割 + 骨架）在 1000 张图像的 FID 评估中取得 77.64 的最优结果。逐一移除任一条件模块均导致 FID 显著上升，证明三者在几何控制上互补且缺一不可：

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/010_Table_4.jpg]]
*Table 4: Ablation study on structural control. FID evaluation on 1,000 images of different types of missing modules to demonstrate the necessity of all physical conditions. Our method outperforms all others*

- **法线图**引导模型感知表面纹理与光照方向，提供精细的 3D 形状线索；
- **手-物分割图**提供清晰的前景边界，帮助模型区分手、物体和背景区域；
- **手部骨架投影**精确描绘手部关节姿态，约束手指位置和抓取构型。

缺失任一组件的模型在生成时会出现几何结构漂移，例如手指穿透物体或抓取姿态失真，这直接体现为 FID 的恶化。

#### 外观正则化的关键作用

外观正则化模块（背景缓冲器）对保持文本编辑能力至关重要。Table 5 显示，无正则化时 CLIPScore 从 0.79 降至 0.66，降幅达 16.5%。其因果机制在于：DexYCB 训练集背景单一（多为实验室环境），直接微调会导致模型过拟合到训练集风格，丧失对多样化背景文本的响应能力。

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/012_Table_5.jpg]]
*Table 5: CLIPScore evaluation. Consistency is evaluated between provided prompts and generated images for different backgrounds and instances*

背景缓冲器的设计通过以下方式解耦风格与几何：
1. 利用预训练模型合成多样化背景图像（如风景、室内场景）；
2. 在训练时联合优化真实 HOI 图像的噪声预测损失和背景图像的噪声预测损失（见 Equation 3，权重 $w_r=1$）；
3. 结合分类器自由引导（classifier-free guidance），使模型在推理时能根据文本提示灵活切换背景风格。

Figure 7 的定性结果进一步佐证：有正则化时，相同几何条件下输入不同背景文本（如“在沙滩上”、“在厨房里”）可生成风格迥异的图像；无正则化时，所有输出趋于训练集的实验室风格，文本编辑能力几乎丧失。

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/011_Figure_7.jpg]]
*Figure 7: Ablation study on appearance regularization. Different backgrounds are used as prompts with the same geometry conditions to compare the text editing flexibility brought by the regularization module*

### 定性分析

Figure 4 展示了 HOIDiffusion 的几何-外观解耦能力：固定背景文本描述，变化物理条件（物体形状、姿态、手部骨架），模型能生成对应几何结构一致但外观保持的多样化图像。Figure 8 和 Figure 9 分别验证了对象外观控制（不同风格文本改变物体纹理）和背景控制（从日常风景到虚拟场景）的灵活性。

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on different structures. Generated images with the same background description but different physical conditions (object shape, poses, and hand skeletons). With plain prompts, HOIDiffusion could generate more realistic images similar to the style in training datasets*

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/013_Figure_8.jpg]]
*Figure 8: Generated images using different style texts to control object appearance*

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/016_Figure_9.jpg]]
*Figure 9: Generated images with more text prompts ranging from daily landscape to virtual scene*

### 失败模式与局限性

尽管整体性能优异，HOIDiffusion 仍存在以下已知局限：

1. **物体类别泛化有限**：训练仅使用 DexYCB，物体类别有限。对于极端未见物体形状，几何一致性未经充分验证，可能需要域适应策略。
2. **视频生成缺乏定量评估**：Figure 6 展示了零样本抓取轨迹视频生成，通过跨帧交叉注意力缓解闪烁，但仅提供定性展示，缺少闪烁程度等定量指标，且视频长度受限于插值轨迹。
3. **手部外观多样性受限**：手部形状风格受限于训练数据（LAION 和 DexYCB），可能无法灵活生成特定肤色或手型，公平性影响未讨论。
4. **对输入条件质量敏感**：方法依赖精确的 3D 几何条件输入（法线、分割、骨架）。若这些条件存在噪声或估计误差，生成质量可能下降，但论文未对此进行鲁棒性分析。

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/008_Figure_6.jpg]]
*Figure 6: Zero-shot video generation of hand grasping trajectory. Images along the same line represent the sequential motion of reaching an object. By leveraging temporal-level cross-attention, the frame flickering problem is mitigated*

### 补充图表

![[assets/figures/papers/paper_list_l1716_HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data/figures/001_Figure_1.jpg]]
*Figure 1: (i) Left: Hand-object synthesis with Stable Diffusion model; (ii) Right: HOIDiffusion generates high-quality hand-object interaction images conditioned on physical structures and detailed text description. The model disentangles the geometry from appearance, exhibiting high generation diversity. Each row: We can fix the structure and control the style based on text inputs; Each column: We can fix the style and control the structure based on 3D structural inputs*

## 方法谱系与知识库定位

### 1. 方法溯源与基线关系

HOIDiffusion 位于“文本到图像扩散模型 + 3D结构条件控制”的交叉点，其核心思想是将预训练扩散模型的丰富视觉先验与显式3D几何条件相结合，以解决现有方法在手-物体交互（HOI）场景中的几何失真和物理不合理性。

**与上游基础模型的关系**：HOIDiffusion 直接建立在 **Stable Diffusion**（Rombach et al., CVPR 2022）的潜在扩散框架之上。标准Stable Diffusion仅以文本提示为条件，在HOI场景中频繁出现手指数量错误、抓取姿态不自然等问题（见Figure 1左侧）。HOIDiffusion通过注入三个额外的条件编码器（法线图、手-物分割图、手部2D骨架投影），将3D几何结构引入生成过程，实现了几何与外观的解耦控制。

**与可控生成基线的关系**：
- **ControlNet**（Zhang et al., ICCV 2023）是通用多条件可控生成的代表，但在HOI场景下表现不佳：Table 1显示ControlNet在DexYCB上的FID高达87.99，远高于HOIDiffusion的55.22。这说明通用的边缘/深度条件不足以约束手-物体之间精细的接触关系。
- **DreamBooth**（Ruiz et al., CVPR 2023）是个性化文本到图像生成的典型方法，但其生成的多样性（IS 7.99）与HOIDiffusion（IS 7.73）相当，而图像质量（FID）和几何一致性（Contact Recall）均显著落后，表明单纯的个性化微调无法解决HOI场景的结构控制问题。

**与HOI特定方法的关系**：
- **Affordance Diffusion**（Ye et al., CVPR 2023）是HOI生成领域的相关工作，在Table 2的接触召回率比较中被引用。HOIDiffusion在Mean Contact Recall上达到95.49%，优于Affordance Diffusion，证明显式的3D几何条件（分割、法线、骨架）比隐式的可供性条件对接触建模更有效。
- **GrabNet**（Taheri et al., ECCV 2020）作为第一阶段的抓取姿势生成器，是HOIDiffusion的几何条件来源。HOIDiffusion将GrabNet的输出（3D手部姿态）转化为2D投影条件，实现了从3D抓取到2D逼真图像的“渲染式”生成。

**核心改进槽位总结**：
| 槽位 | 基线做法 | HOIDiffusion做法 |
|------|----------|------------------|
| 结构条件输入 | 无或单一条件（如Canny边缘） | 法线图 + 手-物分割图 + 手部2D骨架投影的三条件组合 |
| 训练正则化 | 无 | 背景缓冲正则化 + 分类器自由引导，防止风格过拟合 |
| 模型架构 | 标准Stable Diffusion UNet | 注入三个Adapter式条件编码器，条件嵌入加至UNet编码器 |

### 2. 适用边界与局限性

**已知适用场景**：
- 以DexYCB数据集为代表的桌面级单手-刚性物体交互，物体类别包括 mug, can, bottle, bowl 等日常物品。
- 输入需要精确的3D物体模型（mesh），以生成对应的抓取姿势和几何条件。
- 生成质量依赖于条件输入的精度：若提供的法线图、分割图或骨架投影存在噪声，生成质量可能下降（论文未对此进行定量消融，需手动验证）。

**已知局限**：
1. **物体类别泛化有限**：训练仅使用DexYCB数据集，物体类别受限。针对极端未见物体形状的几何一致性未经充分验证。
2. **手部外观多样性受限**：手部形状风格受限于训练数据（LAION预训练权重 + DexYCB微调），可能无法灵活生成特定肤色或手型属性。论文未讨论公平性影响。
3. **视频生成缺乏定量评估**：Figure 6展示了零样本视频生成能力，通过跨帧交叉注意力缓解闪烁，但仅提供定性展示，缺乏闪烁程度等定量指标，且视频长度受限于插值轨迹。
4. **背景偏见与缓解**：DexYCB背景单一（多为实验室环境），论文通过合成多样化背景（scenery prompts）和LLaVA生成的详细描述来缓解，但背景正则化模块本身引入了额外的合成数据依赖。

### 3. 开放问题与未来方向

1. **交互复杂度扩展**：当前框架仅处理单手-单物体交互。如何扩展至双手协同操作或多物体交互场景（如一只手握杯、另一只手倒水）是一个自然但非平凡的扩展方向。
2. **真实机器人验证**：生成的数据在真实机器人抓取或移动操作任务中的有效性尚未验证。Table 3仅在NOCS 6D姿态估计这一下游任务上验证了数据增强效果，与物理抓取执行之间存在差距。
3. **全身交互扩展**：是否可将该框架推广至全身人体-物体交互（如整个人体去抓持大物体），需要解决全身骨架、自遮挡和更大运动范围带来的几何建模挑战。
4. **更长时序生成**：在保持可控性的前提下，能否利用更强的视频扩散模型（如SVD, VideoCrafter等）生成更长的交互序列，而不仅仅是插值轨迹的零样本扩展？
5. **域适应与泛化**：针对极端未见物体形状，是否需要额外的泛化训练策略（如域适应、少样本微调），使几何条件编码器能处理训练分布外的物体几何？

### 4. 知识库定位

HOIDiffusion 在3D视觉与生成模型的交叉领域占据以下定位：

- **上游依赖**：Stable Diffusion（潜在扩散模型）、GrabNet（3D手部抓取生成）、LLaVA（详细文本描述生成）
- **同级方法**：ControlNet（通用可控生成）、DreamBooth（个性化生成）、Affordance Diffusion（HOI生成）
- **下游应用**：NOCS物体6D姿态估计（已验证）、潜在应用包括机器人抓取数据增强、AR/VR交互内容生成、HOI理解模型的训练数据合成
- **技术贡献**：首次证明“法线图+分割图+骨架投影”的三条件组合可以在保留预训练扩散模型文本编辑能力的同时，实现对HOI场景的精确几何控制，并通过背景正则化解决了微调中的风格漂移问题。

## 原文 PDF

![[paperPDFs/CVPR_2024/HOIDiffusion_Generating_Realistic_3D_Hand_Object_Interaction_Data.pdf]]
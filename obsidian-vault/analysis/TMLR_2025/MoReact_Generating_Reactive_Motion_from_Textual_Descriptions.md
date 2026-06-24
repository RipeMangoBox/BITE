---
title: MoReact Generating Reactive Motion from Textual Descriptions
type: paper
paper_level: A
venue: TMLR
year: 2025
pdf_ref: paperPDFs/TMLR_2025/MoReact_Generating_Reactive_Motion_from_Textual_Descriptions.pdf
aliases:
- MGRMFTD
tags:
- TMLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 两阶段顺序扩散生成（先全局轨迹再局部运动）与基于加权交互图的交互损失函数。
primary_logic: 全局轨迹是局部运动与交互真实性的基础，应首先生成；通过在扩散去噪过程中融入高质量轨迹并强调关键关节对的相对运动，可显著提升反应的物理合理性与文本对齐质量。
claims:
- 在反应运动中加入噪声时，对全局轨迹的噪声比对局部运动的噪声对交互真实性的损害更大。
- 全局轨迹的下降暗示反应者应当跌倒而非站立，说明全局轨迹对局部动作语义具有决定性作用。
- 在两阶段框架中，运动学损失、交互损失与阈值策略均对提升生成质量（FID）至关重要。
- 轨迹扩散模型预测噪声（而非直接预测干净数据）获得更好的生成效果。
---

# MoReact Generating Reactive Motion from Textual Descriptions

> [!tip] 核心洞察
> 全局轨迹是局部运动与交互真实性的基础，应首先生成；通过在扩散去噪过程中融入高质量轨迹并强调关键关节对的相对运动，可显著提升反应的物理合理性与文本对齐质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoReact：基于文本描述的反应式运动生成 |
| 英文题名 | MoReact Generating Reactive Motion from Textual Descriptions |
| 会议/期刊 | TMLR 2025 |
| Links | [Project](https://xiyan-xu.github.io/MoReactWebPage/) · [Code](https://github.com/tr3e/InterGen) · [paper](https://openreview.net/forum?id=4zuT73heqm) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoReact |
| Dataset | InterHuman, CHI3D |

> [!tip] 效果简介
> - InterHuman 上，FID ↓ 2.412 ±0.050 vs InterGen 7.207 ±0.114 (-4.795)；Diversity → 7.775 ±0.046 (最接近 Real 7.799) vs InterGen 7.692 ±0.038 (+0.083)。
> - CHI3D 上，Accuracy ↑ 0.687 ±0.014 vs InterGen 0.531 ±0.017 (+0.156)；FID ↓ 10.801 ±0.313 vs MDM 13.850 ±0.375 (-3.049)。

## 概述

文本驱动的反应式运动生成（text-driven reaction generation）旨在根据演员的动作与自然语言描述，合成另一交互者（反应者）的合理全身运动。现有方法面临的核心瓶颈在于**无法有效解耦全局轨迹与局部运动**，且对文本语义信息的利用不充分，导致生成结果中出现交互错位、语义不一致等问题（Figure 1）。

MoReact 的核心洞察是：**全局轨迹是局部运动与交互真实性的物理基础，应首先生成**。实验表明，在反应运动中加入相同尺度的噪声时，对全局轨迹的噪声比对局部运动的噪声对交互真实性的损害更大（Figure 1(b), Figure C.1）；全局轨迹的下降直接暗示反应者应当跌倒而非站立，说明全局轨迹对局部动作语义具有决定性作用（Figure 1(c)）。

基于此，MoReact 提出了一种**两阶段顺序扩散生成框架**：首先利用轨迹扩散模型（Trajectory Diffusion Module）根据演员运动与文本生成反应者的全局轨迹，再通过全身运动扩散模型（Full-Body Motion Diffusion Module）在轨迹引导下合成局部运动，并通过修复机制（Inpainting）将轨迹持续融入去噪过程。同时，引入**基于距离加权的交互图损失函数**，动态突出近距离关节对的相对运动建模，显著提升了近距离交互（如握手）的物理合理性。

在 InterHuman 和 CHI3D 两个基准数据集上，MoReact 在 FID、R-precision 和 Diversity 等关键指标上均显著优于 **InterGen**（Liang et al., 2024）与 **MDM**（Tevet et al., 2023）等基线方法。消融实验进一步证实，运动学损失、交互损失、阈值策略以及两阶段框架本身对生成质量的提升均至关重要（Table 2）。

## 背景与动机

### 问题背景

生成逼真的人体反应运动是计算机视觉与图形学中的核心挑战，其应用涵盖虚拟现实、人机交互、机器人学习与动画制作等领域。给定一个演员（actor）的运动序列和一段文本描述，系统需要合成一个反应者（reactor）的运动，使其在语义上与文本一致，在物理上与演员的交互真实可信。这一任务的关键难点在于：反应运动需要同时满足**全局轨迹的合理性**（反应者相对于演员的空间位置与移动路径）与**局部运动的精细度**（肢体动作、关节姿态），并且二者必须与文本语义高度对齐。

### 现有方法的缺口

当前主流的文本驱动运动生成方法主要分为两类：**单人运动生成**与**双人交互生成**。前者如 **MDM**（Tevet et al., 2023）专注于根据文本合成单人的全身运动，但缺乏对交互上下文的显式建模；将其直接适配为反应生成基线时，通常只能通过简单拼接演员与反应者的运动特征来实现，无法保证交互的真实性。后者如 **InterGen**（Liang et al., 2024）虽然能够生成双人交互运动，但其设计目标并非专门针对反应生成，且往往在单阶段框架中同时处理全局与局部运动，未对二者进行解耦。

这些方法暴露出两个结构性缺口：

1. **全局轨迹与局部运动的耦合不足**：现有方法未显式区分反应者的全局轨迹（如根节点的位移与朝向）与局部运动（如肢体摆动、关节旋转）。这导致生成结果中交互错位频繁出现——例如反应者与演员的相对位置不合理，或文本描述的“握手”动作因根节点位置偏差而无法正确接触。
2. **文本语义利用不充分**：在反应生成中，文本不仅描述反应者自身的动作，还隐式定义了其与演员的交互模式。现有方法未能有效利用文本信息来约束交互的物理合理性，导致语义不一致（如文本描述“躲闪”但生成的反应者仍停留在原地）。

### 本文动机

MoReact 的动机源于一个关键观察：**全局轨迹对反应运动的交互真实性与语义合理性具有决定性作用**。如 **Figure 1(b)** 所示，当在反应运动中注入相同尺度的噪声时，对全局轨迹添加噪声对交互真实性的损害远大于对局部运动添加噪声。进一步地，**Figure 1(c)** 表明，全局轨迹的下降趋势暗示反应者应当跌倒，而非站立或行走——这说明全局轨迹直接约束了局部动作的语义空间。

基于上述观察，MoReact 提出将反应生成**解耦为两阶段顺序生成**：首先生成反应者的全局轨迹，再基于该轨迹合成全身局部运动。这一设计从根本上改变了生成管线：全局轨迹不再是局部运动的附属产物，而是作为局部运动的**先验基础**被优先确定。同时，MoReact 引入**加权交互图损失**，在扩散去噪过程中动态突出近距离关节对的相对运动，从而强化文本描述中关键交互（如握手、击掌）的物理一致性。

## 核心创新

MoReact 的核心创新在于将反应运动生成解耦为**全局轨迹→局部运动**的两阶段顺序扩散框架，并辅以**加权交互图损失**与**修复式轨迹融入机制**，从而系统性地解决了现有方法中交互错位与语义不一致的瓶颈。

### 1. 两阶段顺序生成管线

现有方法（如 **MDM**（Tevet et al., 2023）、**InterGen**（Liang et al., 2024））采用单阶段生成，未显式区分全局轨迹与局部运动，导致两者在扩散过程中相互干扰。MoReact 的关键洞察在于：**全局轨迹是局部运动语义与交互真实性的先决条件**。

**动机证据**（Figure 1(b), Figure C.1）：对反应运动分别注入相同尺度的局部运动噪声与全局轨迹噪声，后者对交互真实性的损害显著更大——FID 随轨迹噪声扩散步数急剧上升，而局部噪声的影响则平缓得多。Figure 1(c) 进一步表明，全局轨迹的下降直接暗示反应者应当“跌倒”而非“站立”，验证了轨迹对局部动作语义的决定性作用。

基于此，MoReact 将生成管线重构为两个顺序阶段（Figure 2）：
- **第一阶段（轨迹扩散模型）**：基于演员全身运动与文本描述，生成反应者的全局轨迹 $\mathbf{g}$（4 维：根节点位置与朝向）。
- **第二阶段（全身运动扩散模型）**：基于演员运动、文本描述以及第一阶段生成的轨迹，合成反应者的完整全身运动。

消融实验（Table 2, Figure E.1）证实，两阶段框架在所有指标上显著优于单阶段变体，验证了顺序解耦策略的有效性。

### 2. 加权交互图损失

现有交互损失（如 InterGen、ReMoS 的设计）通常对所有关节对施加均匀权重，或仅考虑对应关节，忽略了交互中**空间距离对关节重要性的动态调制**——近距离关节对（如握手时的手部）对交互真实性的贡献远大于远距离关节对。

MoReact 提出基于距离加权的交互图损失（Eq. 5–6）：
$$L_{\mathrm{I}}^p = \frac{1}{|S|} \sum_{(i,j,k)\in S} W_p[i,j,k] \, \| \tilde{M}_p[i,j,k] - M_p[i,j,k] \|_2^2$$

其中权重 $W_p$ 随演员与反应者对应关节的距离增大而衰减，仅对真值中距离小于阈值 $c$ 的关节对计算损失。这一设计使模型在扩散去噪过程中**自适应地聚焦于关键接触区域**，同时避免远距离关节对的噪声信号干扰训练。

对比实验（Table E.2）表明，该加权损失在 R-precision、FID 和 MM Dist 上均一致优于 InterGen 和 ReMoS 的交互损失设计。

### 3. 修复式轨迹融入机制

为保证第二阶段生成的全身运动严格遵循第一阶段指定的全局轨迹，MoReact 在推理阶段的扩散去噪过程中引入修复机制（Eq. 8）：
$$\hat{\mathbf{x}}_0 = (1 - M) \odot \tilde{\mathbf{x}}_0 + M \odot \mathbf{g}$$

在每一步去噪中，模型先估计干净运动 $\tilde{\mathbf{x}}_0$，再通过二值掩码 $M$ 将预生成的全局轨迹 $\mathbf{g}$ 强制替换到对应维度。这一设计使全局轨迹作为**硬约束持续引导生成**，而非仅在输入阶段简单拼接。

### 4. 损失门控策略

MoReact 还引入时间步阈值 $\bar{t}$ 对运动学损失 $L_{\mathrm{K}}$ 和交互损失 $L_{\mathrm{I}}$ 进行门控（Eq. 7）：
$$L_{\mathrm{full}} = \lambda_{\mathrm{R}} L_{\mathrm{R}} + I(t \leq \bar{t}) (\lambda_{\mathrm{I}} L_{\mathrm{I}} + \lambda_{\mathrm{K}} L_{\mathrm{K}})$$

仅当扩散时间步 $t \leq \bar{t}$（即去噪后期、运动结构已初步形成）时才激活这两项损失。消融实验（Table 2）证实，该阈值策略对降低 FID 有显著贡献，避免了早期去噪阶段因噪声过大而引入误导性运动学或交互梯度。

### 关键创新总结

| 创新维度 | Baseline 做法 | MoReact 做法 | 证据锚点 |
|---------|-------------|------------|---------|
| 生成管线 | 单阶段同时生成全局与局部运动 | 两阶段顺序生成：先轨迹后全身 | Table 2, Figure E.1 |
| 交互损失 | 均匀权重或仅对应关节 | 基于距离加权的交互图损失 | Eq. 5–6, Table E.2 |
| 轨迹融入 | 未使用或仅输入拼接 | 推理阶段逐步修复式融合 | Eq. 8, Sec. 3.4 |
| 损失调度 | 全程激活所有损失 | 时间步阈值门控 $L_{\mathrm{K}}$ 与 $L_{\mathrm{I}}$ | Eq. 7, Table 2 |

这些创新共同构成了 MoReact 的技术骨架：**两阶段解耦**确立生成顺序的因果正确性，**加权交互损失**精细建模接触区域的相对运动，**修复机制**保证轨迹一致性，**损失门控**优化训练信号质量。三者协同作用，使 MoReact 在 InterHuman 和 CHI3D 数据集上均取得最优的 FID（2.412 与 10.801）与 Accuracy（0.687），同时生成多样性最接近真实分布（Table 1）。

## 整体框架

MoReact 将文本驱动的反应运动生成解耦为**两阶段顺序扩散管线**，其核心设计动机源于一个关键观察：对反应者全局轨迹施加噪声，比在局部运动上施加同等强度噪声对交互真实性的破坏更严重（Figure 1(b)），且全局轨迹的下降直接暗示反应者应当跌倒而非站立（Figure 1(c)）。据此，MoReact 确立了“先全局轨迹、后局部运动”的生成策略。

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/004_Figure_1.jpg]]
*Figure 1: (a) Our model, MoReact, learns to generate lifelike reactions, represented by the blue mesh, based on the textual description and the actor’s motion, represented by the red mesh. (b) As an important motivating analysis for developing our approach, we introduce noise of the same scale to local motion, full-body motion, and global trajectory, respectively. The results indicate that the precision of the global trajectory has a greater impact on the perceptual realism of the reaction. (c) We demonstrate global trajectory’s significant influence on the motion’s semantic information in certain scenarios, such as fall actions*

### 两阶段生成管线

整体框架由两个串联的扩散模块组成（Figure 2）：

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/005_Figure_2.jpg]]
*Figure 2: Overview of MoReact. (a) Our approach to text-driven reaction generation employs a two-stage framework. First, we employ a trajectory diffusion model to generate the global trajectory of the reactor, based on the actor’s full-body motion and the text description. Subsequently, we apply a full-body motion diffusion model to generate the reactor’s full-body motion, based on the actor’s full-body motion, the text description, as well as the synthesized reactor’s trajectory. (b) Our full-body motion diffusion model is built upon a transformer-based architecture, where the ‘TE’ in the figure denotes a Transformer Encoder. The trajectory diffusion model mirrors this architecture but omits the cro...*

1. **轨迹扩散模块（Trajectory Diffusion Module）**  
   输入：演员的全身运动序列 $\mathbf{y}$ 与文本描述 $\mathbf{w}$。  
   输出：反应者在每一帧的全局轨迹 $\mathbf{g} = [\mathbf{g}^1, \dots, \mathbf{g}^T]$，其中每帧轨迹 $\mathbf{g}^i \in \mathbb{R}^4$ 包含根节点位移与绕垂直轴的旋转。  
   该模块仅建模反应者的空间位移路径，不涉及肢体姿态。

2. **全身运动扩散模块（Full-Body Motion Diffusion Module）**  
   输入：演员运动 $\mathbf{y}$、文本 $\mathbf{w}$，以及第一阶段生成的全局轨迹 $\mathbf{g}$。  
   输出：反应者的完整运动序列 $\mathbf{x} = [\mathbf{x}^1, \dots, \mathbf{x}^T]$，每帧姿态 $\mathbf{x}^i \in \mathbb{R}^{263}$ 由全局轨迹 $\mathbf{g}^i$ 和局部姿态 $\mathbf{l}^i \in \mathbb{R}^{259}$ 拼接而成。  
   该模块基于 Transformer 架构，通过自注意力、交叉注意力与前馈网络将运动特征与文本、演员运动、反应者轨迹三类条件信号融合（Figure 2(b)）。

### 推理阶段的修复机制

为保证最终生成的全身运动严格遵循第一阶段产出的全局轨迹，MoReact 在推理时引入**修复机制（Inpainting Mechanism）**：在扩散去噪的每一步，模型先估计当前时间步对应的干净运动 $\tilde{\mathbf{x}}_0$，再通过二值掩码 $M$ 将预先生成的全局轨迹 $\mathbf{g}$ 逐帧注入：

$$\hat{\mathbf{x}}_0 = (1 - M) \odot \tilde{\mathbf{x}}_0 + M \odot \mathbf{g}$$

其中掩码 $M$ 在轨迹对应维度上置 1，其余局部姿态维度置 0。这一操作确保去噪过程中全局轨迹始终被锁定，仅对局部运动进行自由生成，从而在保持轨迹可控性的同时释放局部运动的多样性。

### 输入输出流总结

- **输入**：演员全身运动序列 + 文本描述（反应动作的语义标签）。  
- **阶段一输出**：反应者全局轨迹（根位移 + 旋转）。  
- **阶段二输入**：演员运动 + 文本 + 阶段一轨迹。  
- **最终输出**：反应者全身运动序列，其中全局轨迹被显式约束，局部运动由扩散模型合成。

## 核心模块与公式推导

### 问题定义与运动表示

给定演员的运动序列 $\mathbf{y}$ 与文本描述 $\mathbf{w}$，目标是生成反应者的运动序列 $\mathbf{x} = [\mathbf{x}^1, \mathbf{x}^2, \dots, \mathbf{x}^T]$，其中 $T$ 为帧数。每一帧的姿态 $\mathbf{x}^i$ 被解耦为两个部分：

$$\mathbf{x}^i = (\mathbf{g}^i, \mathbf{l}^i)$$

其中 $\mathbf{g}^i \in \mathbb{R}^4$ 表示全局轨迹（含根节点位置与朝向），$\mathbf{l}^i \in \mathbb{R}^{259}$ 表示局部姿态。这一解耦是 MoReact 两阶段生成管线的形式化基础（Sec. 3.1, Task Definition）。

### 轨迹扩散模块（Trajectory Diffusion Module）

第一阶段的目标是从演员运动 $\mathbf{y}$ 和文本 $\mathbf{w}$ 中生成反应者的全局轨迹 $\mathbf{g}$。该模块采用扩散模型架构，其训练损失为标准的重建损失——预测噪声 $\tilde{\epsilon}$ 与真实噪声 $\epsilon$ 之间的 $\ell_2$ 距离：

$$L_{\mathrm{traj}} = \| \epsilon - \tilde{\epsilon} \|_2^2$$

消融实验表明，预测噪声（而非直接预测干净数据 $\mathbf{x}_0$）在 R-precision、FID 和 Multi-Modality Distance 上均取得更优性能（Table E.1, confidence 0.98），验证了该损失设计的有效性。

### 全身运动扩散模块（Full-Body Motion Diffusion Module）

第二阶段在给定演员运动 $\mathbf{y}$、文本 $\mathbf{w}$ 以及第一阶段生成的轨迹 $\mathbf{g}$ 的条件下，合成反应者的全身运动。该模块基于 Transformer 架构，通过自注意力、交叉注意力和前馈网络实现多模态特征的融合（Figure 2(b)）。交叉注意力层将运动特征与来自文本、演员运动和反应者轨迹的特征进行整合（Sec. 3.2）。

训练该模块的损失函数由三项加权构成：

$$L_{\mathrm{full}} = \lambda_{\mathrm{R}} L_{\mathrm{R}} + I(t \leq \bar{t}) (\lambda_{\mathrm{I}} L_{\mathrm{I}} + \lambda_{\mathrm{K}} L_{\mathrm{K}})$$

其中：
- $L_{\mathrm{R}}$ 为重建损失，与轨迹模块类似，预测噪声与真实噪声的 $\ell_2$ 距离。
- $L_{\mathrm{K}}$ 为运动学损失（Kinematic Loss）。
- $L_{\mathrm{I}}$ 为交互损失（Interaction Loss）。
- $I(t \leq \bar{t})$ 为指示函数，仅在扩散时间步 $t$ 不超过阈值 $\bar{t}$ 时激活运动学损失和交互损失。

阈值策略的设计动机在于：扩散过程的早期阶段（高噪声水平）全局结构尚未形成，此时施加精细的运动学与交互约束不仅无效，还可能干扰生成方向。消融实验证实，该阈值策略对降低 FID 有显著贡献（Table 2, confidence 0.95）。

### 运动学损失（Kinematic Loss）

运动学损失由四个子项加权求和构成，用于约束生成运动的物理合理性：

$$\mathcal{L}_{\mathrm{K}} = \lambda_{\mathrm{foot}} L_{\mathrm{K}}^{\mathrm{foot}} + \lambda_{\mathrm{vel}} L_{\mathrm{K}}^{\mathrm{vel}} + \lambda_{\mathrm{rot}} L_{\mathrm{K}}^{\mathrm{rot}} + \lambda_{\mathrm{traj}} L_{\mathrm{K}}^{\mathrm{traj}}$$

四个子项分别惩罚：
- **足部滑动**（$L_{\mathrm{K}}^{\mathrm{foot}}$）：约束足部接触地面时的位移。
- **关节速度异常**（$L_{\mathrm{K}}^{\mathrm{vel}}$）：抑制不合理的关节速度突变。
- **全局旋转偏差**（$L_{\mathrm{K}}^{\mathrm{rot}}$）：约束根节点的旋转。
- **全局位置偏差**（$L_{\mathrm{K}}^{\mathrm{traj}}$）：约束根节点的位置。

### 交互损失（Interaction Loss）

交互损失是 MoReact 的核心创新之一，旨在提升近距离交互（如握手、拥抱）的真实性。其关键洞察是：并非所有关节对在交互中同等重要——距离越近的关节对，其相对运动的准确性对交互真实性的影响越大。

位置交互损失的形式为：

$$L_{\mathrm{I}}^p = \frac{1}{|S|} \sum_{(i,j,k)\in S} W_p[i,j,k] \| \tilde{M}_p[i,j,k] - M_p[i,j,k] \|_2^2$$

其中：
- $M_p$ 和 $\tilde{M}_p$ 分别为真值与生成结果的交互图（interaction map），编码了反应者与演员对应关节之间的相对位置关系。
- $S$ 为有效关节对的集合，仅包含真值中距离小于阈值 $c$ 的关节对——这意味着损失仅关注那些在实际交互中确实接近的关节对，避免远距离关节对的噪声干扰。
- $W_p[i,j,k]$ 为基于距离的权重，距离越近的关节对权重越大，从而动态突出关键接触区域。

速度交互损失 $L_{\mathrm{I}}^v$ 采用类似形式，约束关节间相对速度的一致性。完整的交互损失为两者之和：$L_{\mathrm{I}} = L_{\mathrm{I}}^p + L_{\mathrm{I}}^v$。

消融实验显示，该加权交互损失在 R-precision、FID 和 MM Dist 上均优于 InterGen（Liang et al., 2024）和 ReMoS（Ghosh et al., 2024）的交互损失设计（Table E.2, confidence 0.98），验证了距离加权与有效关节对筛选策略的有效性。

### 修复机制（Inpainting Mechanism）

推理阶段，全身运动扩散模型需要在去噪过程中持续融入第一阶段生成的全局轨迹 $\mathbf{g}$，以确保最终生成的全身运动与指定轨迹一致。修复机制通过掩码融合实现：

$$\hat{\mathbf{x}}_0 = (1 - M) \odot \tilde{\mathbf{x}}_0 + M \odot \mathbf{g}$$

其中：
- $\tilde{\mathbf{x}}_0$ 为扩散模型在当前时间步估计的干净运动。
- $\mathbf{g}$ 为第一阶段生成的全局轨迹。
- $M$ 为二值掩码，在轨迹对应的维度上取值为 1，其余维度为 0。
- $\odot$ 表示逐元素乘法。

该操作在扩散去噪的每一步执行，将已知的轨迹信息“注入”到估计的干净运动中，使生成过程始终受到轨迹的引导（Sec. 3.4, Eq. 8）。这一机制是两阶段框架能够解耦全局与局部运动生成的关键技术环节。

## 实验与分析

### 核心瓶颈与动机验证

MoReact 的设计根植于一个关键观察：在反应运动生成中，**全局轨迹的准确性对交互真实性的影响远大于局部运动**。作者通过向真实反应运动的不同成分注入等量噪声进行验证（Figure 1(b), Figure C.1）：当噪声被添加到全局轨迹时，交互质量（以 FID 衡量）急剧恶化；而向局部运动添加相同量级的噪声，交互质量下降幅度明显更小。这一现象表明，现有方法未能有效解耦全局轨迹与局部运动，导致生成结果中出现交互错位和语义不一致。

进一步地，Figure 1(c) 展示了全局轨迹对局部动作语义的决定性作用：当反应者的全局轨迹呈下降趋势时，合理的局部动作应当是“跌倒”，而非“站立”或“行走”。这一发现确立了 MoReact **先全局轨迹、后局部运动**的两阶段顺序生成策略的因果逻辑。

### 主实验结果

MoReact 在 InterHuman 和 CHI3D 两个数据集上与多个基线方法进行了全面对比（Table 1）。主要结果如下：

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/006_Table_1.jpg]]
*Table 1: Quantitative Comparison on InterHuman and CHI3D. ± represents the 95% confidence interval, and → indicates that values that closer to the Real are better. * indicates the model is evaluated without motion infilling mechanism*

**InterHuman 数据集上**：
- **FID ↓**：MoReact 达到 **2.412 ± 0.050**，相比 InterGen（Liang et al., 2024）的 7.207 ± 0.114 降低 4.795，相比 MDM（Tevet et al., 2023）的 4.899 ± 0.137 降低 2.487。
- **Diversity →**：MoReact 的多样性指标为 7.775 ± 0.046，在所有方法中最接近真实数据的 7.799。
- **R-Precision ↑** 和 **MM Dist ↓** 指标上同样取得最优或接近最优结果。

**CHI3D 数据集上**：
- **FID ↓**：MoReact 达到 **10.801 ± 0.313**，显著优于 MDM 的 13.850 ± 0.375 和 MDM-GRU 的 15.556 ± 0.445。
- **Accuracy ↑**：MoReact 达到 **0.687 ± 0.014**，相比 InterGen 的 0.531 ± 0.017 提升 0.156。

需要说明的是，InterGen 公开检查点在训练时使用了测试集数据，为保证公平对比，作者从零重新训练了 InterGen。所有模型在同一硬件环境中训练，并使用相同的评估指标和 95% 置信区间。

### 定性对比

Figure 3 展示了 MoReact 与 MDM、InterGen 的定性对比。MoReact 在多个挑战性场景下表现出一致的优势：
- **(a)(b) 身体穿透**：MDM 和 InterGen 生成的反应者身体与演员身体发生明显穿透，MoReact 则有效避免了这一问题。
- **(c) 文本-运动语义不匹配**：当文本描述要求特定反应动作时，基线方法生成的动作与文本语义不一致，MoReact 则准确对齐。
- **(d) 交互错位**：在需要精确空间对齐的交互（如握手）中，基线方法出现位置偏差，MoReact 生成的交互位置准确。

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative comparison. We show that MoReact consistently generates more realistic reactions than MDM InterGen, avoiding issues such as body penetration (a)(b), text-motion mismatch (c), and interaction misalignment (d)*

### 消融实验

**Table 2 的消融研究**系统验证了各组件对生成质量的贡献（均在 InterHuman 数据集上以 FID 为主要指标）：

1. **运动学损失 L_K 的有效性**：移除 L_K 后 FID 从 2.412 升至 3.021（+0.609），验证了足部滑动约束、关节速度约束和全局旋转/位置约束对运动物理合理性的贡献。

2. **交互损失 L_I 的有效性**：移除 L_I 后 FID 升至 2.856（+0.444），证明加权交互图损失对近距离交互真实性的关键作用。

3. **阈值策略的有效性**：取消阈值策略（始终应用 L_K 和 L_I）导致 FID 升至 2.731（+0.319），说明在去噪早期阶段避免施加运动学和交互约束有利于生成多样性，仅在后期精细去噪时引入这些约束更为合理。

4. **两阶段框架 vs. 单阶段框架**：将 MoReact 改为单阶段同时生成全局轨迹和局部运动，FID 从 2.412 升至 3.198（+0.786），在所有指标上均显著劣于两阶段框架（Figure E.1 提供了更详细的可视化对比）。这一结果直接验证了“先全局后局部”的顺序生成策略的有效性。

**Table E.1 的轨迹预测目标消融**：轨迹扩散模型预测噪声 $\epsilon$（而非直接预测干净数据 $\mathbf{x}_0$）在 R-Precision、FID 和 Multi-Modality Distance 上均取得更优结果，验证了扩散模型中预测噪声的标准做法的合理性。

**Table E.2 的交互损失设计对比**：MoReact 提出的**加权交互损失**在 R-Precision、FID 和 MM Dist 上均优于 InterGen（Liang et al., 2024）和 ReMoS（Ghosh et al., 2024）的交互损失设计。其核心机制在于：
- 通过距离加权动态突出近距离关节对（距离越近权重越大）
- 仅对真值中距离小于阈值 $c$ 的关节对计算损失
- 有效弱化远距离关节对的噪声干扰

### 控制能力验证

Figure 4 展示了 MoReact 对反应者全局轨迹的控制能力。通过修改输入轨迹或文本描述，模型能够生成符合指定空间位置和语义要求的反应运动，验证了修复机制（Inpainting）在推理阶段将全局轨迹有效融入全身运动生成的能力。

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative evaluation of the control capacity*

### 失败模式与局限性

尽管 MoReact 在定量和定性评估中表现优异，仍存在以下局限：

1. **多人群体的扩展性不足**：当前框架仅考虑对单个演员运动的反应生成，尚未推广至多人群体复杂交互场景。

2. **固定序列长度的限制**：模型依赖于固定长度的动作序列，尚未验证在任意时长文本驱动反应生成中的表现。

3. **极端接触下的穿透问题**：尽管交互损失改善了近距离接触的真实性，但在极端接触或复杂物理约束（如碰撞、挤压）下仍可能出现穿透现象，说明纯数据驱动损失无法完全替代物理仿真约束。

4. **应用伦理考量**：军事训练等潜在应用可能带来负面社会影响，文中已关注但未提出具体缓解措施。

### 关键图表结论汇总

- **Figure 1**：全局轨迹噪声对交互真实性的损害远大于局部运动噪声；全局轨迹下降暗示反应者应跌倒，证明轨迹对语义的决定性作用。
- **Figure 2**：MoReact 的两阶段架构由轨迹扩散模块和全身运动扩散模块组成，后者基于 Transformer 架构并通过修复机制融入轨迹。
- **Table 1**：MoReact 在 InterHuman 和 CHI3D 上均取得最优 FID，在 CHI3D 上取得最优 Accuracy。
- **Table 2**：L_K、L_I、阈值策略和两阶段框架均对 FID 有显著贡献，移除任一组件均导致性能下降。
- **Figure 3**：MoReact 在避免身体穿透、文本-运动语义匹配和交互空间对齐方面均优于 MDM 和 InterGen。

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/007_Table_2.jpg]]
*Table 2: Ablation Studies on InterHuman dataset. The results demonstrate the effectiveness of kinematic loss*

### 补充图表

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/010_Figure.jpg]]
*Figure: FID Over Time Steps Figure C.1: Change of FID for different noising modes and diffusion steps. Adding noise to the global trajectory has a more detrimental effect on the realism of interactions compared with adding noise to the local motion*

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/011_Figure.jpg]]
*Figure: MoReact MoReact (1-Stage) MoReact (1-Stage) Figure E.1: Ablation study on the design choice within MoReact*

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/012_Table.jpg]]
*Table: E.1: Ablation studies on predicted term of trajectory diffusion model. The trajectory model that predicts ϵ achieves better performance in R-precision, FID and Multi-Modality Distance*

![[assets/figures/papers/paper_list_l1929_MoReact_Generating_Reactive_Motion_from_Textual_Descriptions/figures/013_Table.jpg]]
*Table: E.2: Quantitative comparison of different interaction loss designs. Our weighted interaction loss consistently outperforms InterGen (Liang et al., 2024) and ReMoS (Ghosh et al., 2024) losses on R-precision, FID, and MM Dist, demonstrating its superior effectiveness in generating realistic reactions*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

MoReact 处于**文本驱动的人体运动生成**与**双人交互运动建模**的交叉地带。其核心思路——将反应生成解耦为全局轨迹与局部运动两个阶段——并非凭空产生，而是对现有方法瓶颈的直接回应。

#### 1.1 对单人运动生成方法的继承与突破

**MDM**（Tevet et al., 2023）作为基于扩散的单人运动生成方法，为 MoReact 提供了扩散生成的基本范式。但 MDM 原生设计仅处理单人运动，在适配为反应生成基线时，需将演员与反应者的动作/反应特征进行拼接。这一朴素拼接策略暴露了关键缺陷：**全局轨迹与局部运动被混为一谈**，导致生成的交互中出现身体穿透、文本-运动语义错位等问题（见 Figure 3）。

MoReact 的突破在于显式建模了反应运动的内在层级结构：**全局轨迹决定了交互的空间可行性与高层语义，局部运动则填充细节**。这一洞察通过 Figure 1(b) 的噪声注入实验得到验证——对全局轨迹施加与局部运动相同尺度的噪声，对交互真实性的损害显著更大。Figure 1(c) 进一步表明，全局轨迹的下降暗示反应者应当跌倒而非站立，说明全局轨迹对局部动作语义具有决定性约束。

#### 1.2 对双人交互生成方法的改进

**InterGen**（Liang et al., 2024）是双人交互生成的代表性工作。MoReact 在以下关键维度上对其进行了改进：

| 改进维度 | InterGen 策略 | MoReact 策略 | 证据 |
|---------|-------------|------------|------|
| **生成管线** | 单阶段同时生成全局与局部运动 | 两阶段顺序生成：先轨迹扩散，再全身运动扩散 | Table 2, Figure E.1 |
| **交互损失** | 均匀权重、仅考虑对应关节的简单损失 | 基于距离加权的交互图损失，动态突出近距离关节对 | Eq. 5-6, Table E.2 |
| **轨迹融入机制** | 推理阶段引入修复（inpainting） | 在扩散每一步将预生成的全局轨迹通过掩码与估计的干净运动融合 | Eq. 8, Sec. 3.4 |

值得强调的是，MoReact 的加权交互损失设计在 R-precision、FID 和 MM Dist 上均优于 InterGen 和 ReMoS（Ghosh et al., 2024）的交互损失方案（Table E.2），证明**动态距离加权**对建模近距离交互（如握手）的关节级相对运动至关重要。

#### 1.3 在知识库中的定位

MoReact 的方法贡献可归纳为三个“调控旋钮”（causal knobs），每个旋钮对应一个明确的设计选择：

1. **两阶段顺序扩散生成**：先全局轨迹后局部运动。这一选择基于一个可验证的因果假设——全局轨迹是局部运动与交互真实性的基础，应首先生成。消融实验（Table 2, Figure E.1）表明，两阶段框架在所有指标上显著优于单阶段框架。

2. **加权交互图损失**：通过距离门控机制，仅计算真值中距离小于阈值 $c$ 的关节对差异，并以距离倒数作为权重。这迫使模型在去噪早期（$t \leq \bar{t}$）集中优化近距离接触的关节相对运动，而非均匀对待所有关节对。

3. **推理阶段的修复融合**：$\hat{\mathbf{x}}_0 = (1 - M) \odot \tilde{\mathbf{x}}_0 + M \odot \mathbf{g}$。这一机制确保最终生成的全身运动严格遵循第一阶段生成的全局轨迹，而非仅将其作为输入条件。

### 2. 适用边界与局限

尽管 MoReact 在 InterHuman 和 CHI3D 两个基准上取得了显著提升（FID 分别降至 2.412 和 10.801，Table 1），其适用边界与局限同样清晰：

**适用边界**：
- **输入条件**：需要完整的文本描述 + 单个演员的全身运动序列。文本描述需包含动作语义信息，尚未验证在稀疏或模糊描述下的表现。
- **输出范围**：针对单个反应者的全身运动生成，不涉及多人群体交互。
- **序列长度**：固定长度的动作序列，未验证可变时长生成。
- **运动表示**：基于 HumanML3D 改编的 263 维姿态表示（全局轨迹 4 维 + 局部姿态 259 维），依赖该表示体系的完备性。

**已知局限**：
1. **多人扩展未验证**：MoReact 目前仅考虑针对单个演员运动的反应生成，尚未推广至多人群体的复杂交互场景。
2. **物理穿透残留**：尽管交互损失改善了近距离接触的真实性，极端接触或复杂物理约束（如碰撞）仍可能出现穿透现象。交互损失尚未与物理约束（如接触力）结合。
3. **实时性未验证**：两阶段扩散生成的计算开销使其难以直接适配 VR/AR 等实时交互应用。
4. **文本细粒度不足**：文本驱动的反应生成尚未捕捉细粒度的意图和情感信息。
5. **社会影响**：军事训练等潜在应用可能带来负面社会影响，文中已关注但未提出具体缓解措施。

### 3. 开放问题

基于上述局限，MoReact 框架引出以下值得进一步探索的方向：

1. **多参与者扩展**：如何将两阶段反应生成框架推广到基于文本和多个参与者运动的场景？这需要解决多轨迹协调与交互图的多方扩展问题。

2. **物理约束融合**：交互损失能否进一步与物理约束（如接触力、动量守恒）结合以消除穿透？这可能需要引入可微物理模拟器作为额外的监督信号。

3. **实时交互适配**：能否通过蒸馏、一致性模型或缩减扩散步数将 MoReact 框架适配到实时交互应用（如 VR/AR）？

4. **细粒度语义建模**：文本驱动的反应生成如何更好地捕捉意图（如“友好地” vs “敌意地”）和情感（如“恐惧地后退” vs “愤怒地反击”）？

5. **稀疏文本条件**：在更稀疏的文本描述（如仅给出“做出反应”而非完整动作描述）条件下，模型是否仍能生成合理反应？这涉及反应生成的内在不确定性与多模态建模能力。

6. **轨迹扩散模型的预测目标选择**：Table E.1 表明预测噪声（$\epsilon$）优于直接预测干净数据（$x_0$），这一现象是否在更广泛的运动生成任务中普遍成立？其理论根源值得深挖。

## 原文 PDF

![[paperPDFs/TMLR_2025/MoReact_Generating_Reactive_Motion_from_Textual_Descriptions.pdf]]
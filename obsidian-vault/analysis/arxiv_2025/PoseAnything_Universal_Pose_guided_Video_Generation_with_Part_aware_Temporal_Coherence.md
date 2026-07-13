---
title: "PoseAnything: Universal Pose-guided Video Generation with Part-aware Temporal Coherence"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/PoseAnything_Universal_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.pdf
project_link: https://ryan-w2024.github.io/project/PoseAnything/
code_link: null
aliases:
- PoseAnything
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入 Part-aware Temporal Coherence Module (PTCM) 实现部件级交叉注意力；利用 Decoupled CFG 将主体姿态注入正锚点、相机运动注入负锚点，解耦两种运动。
primary_logic: 通过部件分割、注意力权重匹配和部件级交叉注意力，将整体外观一致性分解为细粒度的部件级控制；借助 CFG 的正/负锚点首次实现主体与相机运动的独立注入，消除相互干扰。
claims:
- PoseAnything is the first universal pose-guided video generation framework capable of handling both human and nonhuman characters, supporting arbitrary skeletal inputs.
- Part-aware Temporal Coherence Module divides the subject into parts, matches them across frames via attention weights, and applies part-aware cross-attention to achieve fine-grain...
- Subject and Camera Motion Decoupled CFG independently controls camera movement by injecting subject pose into the positive anchor and camera motion into the negative anchor of CFG.
- PoseAnything outperforms all state-of-the-art methods on TikTok (human) and XPose (non-human) benchmarks across all metrics, establishing new state of the art.
---

# PoseAnything: Universal Pose-guided Video Generation with Part-aware Temporal Coherence

> [!tip] 核心洞察
> 通过部件分割、注意力权重匹配和部件级交叉注意力，将整体外观一致性分解为细粒度的部件级控制；借助 CFG 的正/负锚点首次实现主体与相机运动的独立注入，消除相互干扰。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseAnything：通用姿态引导视频生成与部件感知时序一致性 |
| 英文题名 | PoseAnything: Universal Pose-guided Video Generation with Part-aware Temporal Coherence |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.13465) · [Project](https://ryan-w2024.github.io/project/PoseAnything/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PoseAnything |
| Dataset | TikTok, XPose-benchmark |

> [!tip] 效果简介
> - TikTok (Human) 上，PSNR 31.50 vs 30.78 (Animate-X) (+0.72)；SSIM 0.836 vs 0.811 (Unianimate) (+0.025)；LPIPS 0.224 vs 0.231 (Unianimate) (-0.007)。
> - XPose-benchmark (Non-human) 上，PSNR 30.29 vs 30.15 (ATI) (+0.14)；SSIM 0.7114 vs 0.6929 (Tora) (+0.0185)；LPIPS 0.3241 vs 0.3530 (Tora) (-0.0289)。

## 概要

现有姿态引导视频生成方法长期受限于两大瓶颈：其一，仅支持人体骨骼结构，无法泛化至任意非人体主体（如动物、机械体等）；其二，缺乏对主体外观一致性的细粒度控制，且不能独立操控相机运动，导致主体动作与背景运动相互耦合、生成质量受限。

针对上述问题，本文提出 **PoseAnything**——首个通用姿态引导视频生成框架，能够同时处理人体与非人体角色，支持任意骨骼输入。其核心调控机制包含两个关键创新：

- **部件感知时序一致性模块（Part-aware Temporal Coherence Module, PTCM）**：将主体按骨骼段分割为多个部件，利用跨帧注意力权重建立部件对应关系，并通过部件级交叉注意力实现细粒度的外观一致性控制，将整体一致性分解为可独立优化的部件级约束。
- **主体与相机运动解耦 CFG（Subject and Camera Motion Decoupled CFG）**：首次借助分类器自由引导（CFG）的正/负锚点机制，将主体姿态条件注入正锚点、相机运动条件注入负锚点，实现两种运动的独立注入与解耦控制，消除相互干扰。

在实验验证层面，PoseAnything 在人体基准 TikTok 和非人体基准 XPose 上均以全面优势超越现有最优方法：TikTok 上 PSNR 达 31.50（较 Animate‑X 提升 +0.72），FVD 降至 133.95；XPose 上 PSNR 达 30.29，FVD 降至 99.97。消融实验进一步证实，通道维拼接的姿态注入策略相比 MLP 融合使 FVD 降低 52.8%，PTCM 在所有指标上显著优于全局交叉注意力基线。值得注意的是，模型在仅注入 10% 姿态帧的稀疏条件下仍能保持竞争性能（PSNR 30.21），展现出强时序插值能力。

PoseAnything 的方法定位处于图像到视频扩散模型与结构化运动引导的交汇点，以 Wan2.2‑TI2V‑5B 为骨干，通过部件感知时序建模与解耦运动注入，首次将通用姿态引导视频生成推向实用化。

### 问题背景

姿态引导视频生成旨在根据给定的姿态序列驱动主体运动，生成与之相符的视频内容。该技术在虚拟主播、游戏角色动画、电影特效等领域具有广泛应用。现有方法已在人体姿态引导的视频生成上取得显著进展，代表性工作包括 **Disco**、**MagicAnimate**、**AnimateAnyone**、**Champ**、**Unianimate** 以及 **Animate-X** 等。这些方法通常以人体骨骼关键点作为条件信号，驱动参考图像中的人物执行目标动作。

### 现有方法的结构性缺口

尽管人体姿态引导已相对成熟，现有方法仍存在三个根本性局限：

**第一，主体泛化能力缺失。** 现有方法仅支持人体骨骼结构（如 17 关键点的 COCO 格式），无法泛化至任意非人体主体——例如动物、机械臂、卡通角色等具有不同骨架拓扑的对象。对于非人体主体，现有方案主要依赖拖拽式运动控制（如 **ATI**、**Tora**、**SG-I2V**），但这类方法缺乏对骨架级运动语义的精确建模。在真实应用中，大量主体并非人体，这一缺口严重限制了姿态引导视频生成的适用范围。

**第二，外观一致性控制粒度粗糙。** 现有方法在维持主体外观一致性时通常采用全局交叉注意力或 ControlNet 机制，将主体作为一个整体进行帧间约束。这种全局策略难以捕捉主体的细粒度结构——例如，当人体手臂和腿部以不同速度运动时，全局约束可能导致肢体模糊、纹理漂移或部件错位。

**第三，主体运动与相机运动相互耦合。** 现有方法要么完全不具备相机运动控制能力，要么将主体运动与相机运动信号混合注入，导致两类运动无法独立操控。当用户希望主体执行特定动作的同时镜头进行推拉或平移时，耦合注入会引发运动信号冲突，使生成结果中主体的姿态跟随与相机运动相互干扰。

### 本文动机

针对上述三个结构性缺口，本文提出 **PoseAnything**——首个通用姿态引导视频生成框架。其核心动机在于：

1. **实现任意骨架拓扑的通用姿态引导**：通过构建覆盖多类别非人体主体的 XPose 数据集，并设计通道维条件注入策略，使单一模型能够处理人体与非人体主体的任意骨架输入。
2. **引入部件级时序一致性控制**：设计 Part-aware Temporal Coherence Module (PTCM)，将主体分解为独立部件，利用注意力权重建立跨帧部件对应关系，并通过部件级交叉注意力实现细粒度的外观一致性约束。
3. **解耦主体与相机运动**：提出 Subject and Camera Motion Decoupled CFG，首次在姿态引导视频生成中实现相机运动的独立控制——将主体姿态注入 CFG 的正锚点、相机运动注入负锚点，消除两类运动信号的相互干扰。

## 核心方法与创新机理

PoseAnything 的核心创新可归结为三个互为支撑的机制，分别解决了通用姿态注入、部件级时序一致性和运动解耦控制三个瓶颈。

### 1. 通用姿态注入：通道维拼接融合

现有姿态引导视频生成方法（如 **Disco**、**MagicAnimate**、**AnimateAnyone**、**Champ** 等）仅支持人体骨骼，其姿态注入策略通常采用 MLP 融合或宽度维拼接。PoseAnything 将这一策略替换为**通道维拼接**（Channel-wise Concatenation）：将参考图像隐变量 $Z_0$ 与姿态隐变量 $Z_p$ 沿通道维拼接，再通过卷积进行融合，作为 DiTBlock 的输入：

$$Z_{agr} = [Z_0, Z_p] \in F \times H \times W \times 2C, \quad Z = Conv(Z_{agr})$$

这一设计使得模型能够接受任意骨架结构（人体或非人体）作为条件输入，从注入层面突破了“仅人体”的限制。消融实验（Table 4）表明，通道维拼接在 TikTok 数据集上取得 PSNR 31.50、SSIM 0.8362、FVD 133.95，相比 MLP 融合策略的 FVD 降低了 52.8%，验证了该注入策略在保持生成质量上的显著优势。

### 2. 部件感知时序一致性模块（PTCM）

现有方法的时序一致性控制通常依赖全局交叉注意力或 ControlNet 结构，缺乏对主体外观的细粒度控制。PoseAnything 提出的 **Part-aware Temporal Coherence Module (PTCM)** 将整体外观一致性分解为部件级控制，包含三个步骤：

- **部件分割与掩码生成**：将骨架按段 $s_{ij}$ 划分，通过膨胀操作得到部件像素掩码 $m_{ij} = Dilate(s_{ij}, \alpha)$。
- **注意力权重匹配**：利用跨帧注意力权重，将第一帧的部件与后续帧的对应部件进行匹配：

$$s_{ij'} \sim s_{0j} \iff j' = \underset{t}{\operatorname{argmax}} \ attn\_weight[m_{0j}][m_{it}]$$

- **部件感知交叉注意力**：对匹配的部件对，以第一帧部件作为 Key/Value、当前帧部件作为 Query 执行交叉注意力：

$$x' = x + Cross\text{-}Attn(Q_j, K_j, V_j), \quad Q_j = m_{ij} X W_q, \quad K_j = m_{0j} X_0 W_k, \quad V_j = m_{0j} X_0 W_v$$

消融实验（Table 3）显示，PTCM 在 XPose 基准上相比纯拼接基线（Concat）将 PSNR 从 29.85 提升至 30.29，SSIM 从 0.6964 提升至 0.7114，FVD 从 102.30 降至 99.97，且相比全局交叉注意力变体（EC）在各项指标上均有增益，证明部件级控制是提升时序一致性的关键。

### 3. 主体与相机运动解耦 CFG

现有方法要么不支持相机运动控制，要么将主体运动与相机运动耦合注入，导致两类运动相互干扰。PoseAnything 首次提出 **Subject and Camera Motion Decoupled CFG**，利用分类器自由引导（CFG）的正/负锚点实现两类运动的独立注入：

$$\tilde{\epsilon} = \hat{\epsilon}_\theta(\emptyset_s, z_c) + s \cdot (\hat{\epsilon}_\theta(z_s, \emptyset_c) - \hat{\epsilon}_\theta(\emptyset_s, z_c))$$

其中，主体姿态条件 $z_s$ 注入 CFG 正锚点，相机运动条件 $z_c$ 注入负锚点。这一机制使得模型在遵循姿态引导的同时，能够独立执行相机运动（如推拉、平移），且二者互不干扰。

**证据强度评估**：上述三项创新的消融实验均在受控条件下完成（相同训练配置、batch size、学习率和 GPU 数量），置信度较高。但需注意，PTCM 的部件匹配依赖注意力权重，在骨架极端复杂或初始步数不足时可能出现匹配错误，该失败模式尚未被量化分析；Decoupled CFG 的相机运动类型覆盖面和自动化程度也未详细讨论，需要进一步验证。

PoseAnything 以一张参考图像 $I_r$ 和一段任意主体的骨架序列 $P$ 为输入，生成符合指定运动轨迹的视频片段（Figure 4）。整体 pipeline 基于预训练的图像到视频扩散模型 **Wan2.2-TI2V-5B** 构建，围绕三个核心设计展开：**通道维条件注入**、**部件感知时序一致性模块（PTCM）** 和 **主体与相机运动解耦 CFG**。

### 输入编码与条件注入

参考图像 $I_r$ 经 VAE 编码得到初始隐变量 $Z_0 \in \mathbb{R}^{F \times H \times W \times C}$，骨架序列 $P$ 经姿态编码器提取为姿态隐变量 $Z_p$，二者沿通道维拼接后通过卷积进行融合：

$$Z_{agr} = [Z_0, Z_p] \in \mathbb{R}^{F \times H \times W \times 2C}, \quad Z = \text{Conv}(Z_{agr})$$

融合后的隐变量 $Z$ 作为 DiTBlock 的输入。消融实验（Table 4）表明，通道维拼接策略在 PSNR（31.50）、SSIM（0.8362）和 FVD（133.95）上均优于宽度拼接和 MLP 融合方案，其中 FVD 相比 MLP 融合降低了 52.8%。

### 部件感知时序一致性模块（PTCM）

PTCM 是 PoseAnything 实现细粒度外观一致性控制的核心模块，置于 DiTBlock 的最终交叉注意力层之后，包含三个阶段：

1. **部件分割与掩码生成**：将骨架分解为独立段 $s_{ij}$，对每段进行膨胀得到部件像素掩码 $m_{ij} = \text{Dilate}(s_{ij}, \alpha)$。
2. **跨帧部件匹配**：利用注意力权重建立帧间部件对应关系，将第一帧部件 $s_{0j}$ 与后续帧部件 $s_{ij'}$ 进行匹配：
   $$s_{ij'} \sim s_{0j} \iff j' = \underset{t}{\operatorname{argmax}}\ \text{attn\_weight}[m_{0j}][m_{it}]$$
3. **部件感知交叉注意力**：对匹配的部件对，以第一帧部件作为 Key/Value、当前帧部件作为 Query 执行交叉注意力：
   $$x' = x + \text{Cross-Attn}(Q_j, K_j, V_j), \quad Q_j = m_{ij} X W_q, \quad K_j = m_{0j} X_0 W_k, \quad V_j = m_{0j} X_0 W_v$$

PTCM 将整体外观一致性分解为部件级控制，消融实验（Table 3）显示其相较纯拼接基线（Concat）在 PSNR 上提升 +0.44（30.29 vs. 29.85），且优于全局交叉注意力变体（EC）。

### 主体与相机运动解耦 CFG

PoseAnything 首次在姿态引导视频生成中实现相机运动的独立控制。通过解耦分类器自由引导（CFG），将主体运动条件（姿态序列）注入正锚点，将相机运动条件注入负锚点：

$$\tilde{\epsilon} = \hat{\epsilon}_\theta(\emptyset_s, z_c) + s \cdot (\hat{\epsilon}_\theta(z_s, \emptyset_c) - \hat{\epsilon}_\theta(\emptyset_s, z_c))$$

其中 $\emptyset_s$ 表示空主体条件，$\emptyset_c$ 表示空相机条件。该设计使主体运动与相机运动在去噪过程中互不干扰，最终引导光流被分解为主体运动分量和反向的背景（相机）运动分量：$\mathbf{F}_t = s_s V_s - s_c V_{bg}$。

### 整体数据流

完整的生成流程为：参考图像与骨架序列分别编码后经通道拼接注入 DiTBlock → PTCM 在部件级别精炼跨帧一致性 → 解耦 CFG 在推理阶段独立调节主体与相机运动强度 → 解码器输出最终视频帧。该框架同时支持人体与非人体主体，是首个通用姿态引导视频生成模型（Figure 1）。

PoseAnything 以预训练 **Wan2.2-TI2V-5B** 作为图像到视频扩散主干，在其 DiT Block 中嵌入三个关键模块：通道维条件注入、部件感知时序一致性模块（PTCM）、以及基于 CFG 的主体与相机运动解耦控制。以下逐一展开核心公式与机理。

### 4.1 通道维条件注入

给定参考图像隐变量 $Z_0 \in \mathbb{R}^{F \times H \times W \times C}$ 和姿态序列隐变量 $Z_p$，PoseAnything 采用通道维拼接（Concat by Channel）进行融合：

$$Z_{agr} = [Z_0, Z_p] \in \mathbb{R}^{F \times H \times W \times 2C}, \quad Z = \text{Conv}(Z_{agr}) \in \mathbb{R}^{f \times h \times w \times c}$$

其中 $[\,\cdot\,,\,\cdot\,]$ 表示沿通道轴拼接，$\text{Conv}$ 为将拼接特征投影至 DiT 输入维度的卷积层。消融实验（Table 4）表明，该策略在 TikTok 上取得 PSNR 31.50、SSIM 0.8362、FVD 133.95，相比 MLP 融合方案 FVD 下降 52.8%，验证了通道维注入在保留空间-时序结构上的显著优势。

### 4.2 部件感知时序一致性模块（PTCM）

PTCM 将整体外观一致性分解为细粒度的部件级控制，包含三个子步骤：

**步骤一：部件掩码生成。** 将姿态骨架按语义段 $s_{ij}$ 分割，对每个段进行膨胀得到像素级部件掩码：

$$m_{ij} = \text{Dilate}(s_{ij}, \alpha)$$

其中 $\alpha$ 为膨胀系数，$m_{ij}$ 表示第 $i$ 帧第 $j$ 个部件的二值掩码。

**步骤二：跨帧部件匹配。** 利用 DiT Block 中的注意力权重建立帧间部件对应关系，将第一帧部件 $s_{0j}$ 与后续帧部件 $s_{ij'}$ 匹配：

$$s_{ij'} \sim s_{0j} \iff j' = \underset{t}{\operatorname{argmax}}\ \text{attn\_weight}[m_{0j}][m_{it}]$$

该匹配机制无需额外标注，完全依赖模型内部注意力模式自动建立对应（注意力权重可视化见 Figure 9）。

**步骤三：部件感知交叉注意力。** 对匹配的部件对执行局部交叉注意力，以第一帧部件作为 Key/Value，当前帧部件作为 Query：

$$x' = x + \text{Cross-Attn}(Q_j, K_j, V_j)$$

$$Q_j = m_{ij} X W_q,\quad K_j = m_{0j} X_0 W_k,\quad V_j = m_{0j} X_0 W_v$$

其中 $X$ 和 $X_0$ 分别为当前帧和第一帧的 DiT 中间特征，$W_q, W_k, W_v$ 为投影矩阵。该模块插入 DiT Block 最后一层交叉注意力之后（Figure 4）。消融实验（Table 3）表明，PTCM 在 XPose 上将 PSNR 从纯拼接基线的 29.85 提升至 30.29，SSIM 从 0.6964 提升至 0.7114，验证了部件级控制对非人体主体外观一致性的关键作用。

![[assets/figures/papers/PoseAnything_Universal_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coh_78f56b8ab3f0/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our PoseAnything. Given a reference image Ir and a pose sequence P , we first encode P into pose latent Z _ { p } , and then concatenate it with the latent Z _ { 0 } of I _ { r } along the channel dimension. Additionally, we propose Part-aware Temporal Coherence Module for fine-grained appearance consistency control: 1) We segment the pose into separate segments s _ { i j } and dilate each segment to obtain the subject part masks m _ { i j } ; 2 ) We then use attention patterns to match the same parts across different frames; 3) For each pair \< m _ { 0 j } , m _ { i j } > , we introduce a part-aware cross-attention module in the DiTBlock to compute cross-attention between matche...*

### 4.3 主体与相机运动解耦 CFG

传统 CFG 无法独立操控相机运动。PoseAnything 首次将主体姿态注入正锚点、相机运动注入负锚点，实现两种运动的解耦：

$$\tilde{\epsilon} = \hat{\epsilon}_\theta(\emptyset_s, z_c) + s \cdot \big(\hat{\epsilon}_\theta(z_s, \emptyset_c) - \hat{\epsilon}_\theta(\emptyset_s, z_c)\big)$$

其中：
- $z_s$：包含主体姿态条件（正锚点）；
- $z_c$：包含相机运动条件（负锚点）；
- $\emptyset_s, \emptyset_c$：分别表示置空主体或相机条件；
- $s$：CFG 尺度。

该公式的直觉是：正锚点 $\hat{\epsilon}_\theta(z_s, \emptyset_c)$ 编码“主体运动 + 无相机运动”的噪声估计，负锚点 $\hat{\epsilon}_\theta(\emptyset_s, z_c)$ 编码“无主体运动 + 相机运动”的噪声估计，二者之差提取出纯净的主体运动信号，叠加到相机运动基线上，实现互不干扰的独立控制（Figure 5）。

### 4.4 引导光流分解（附录补充）

在光流引导的实现层面，最终引导光流被分解为主体运动分量与反向的背景（相机）运动分量：

$$\mathbf{F}_t = s_s V_s - s_c V_{bg}$$

其中 $V_s$ 为主体光流，$V_{bg}$ 为背景光流，$s_s, s_c$ 分别为对应的控制强度。该分解使得相机运动控制可独立调节而不影响主体动作的保真度（Figure 8 展示了典型相机控制案例）。

---

**模块间因果链路总结：** 通道维注入提供高效的条件融合基础 → PTCM 在 DiT 特征空间内以部件为单位精炼帧间一致性 → 解耦 CFG 在噪声预测层面将主体与相机运动分离，三者协同实现通用姿态引导视频生成中外观保真度与运动可控性的统一。

## 实验与关键发现

### 主实验结果

PoseAnything 在人体与非人体两类场景中均取得了全面最优的定量结果，验证了其作为首个通用姿态引导视频生成框架的有效性。

**人体姿态引导（TikTok 基准）**。如 Table 1 所示，PoseAnything 在所有四项指标上均超越现有方法。PSNR 达到 31.50，较此前最优的 **Animate-X**（30.78）提升 +0.72 dB；SSIM 为 0.836，超过 **Unianimate**（0.811）0.025；LPIPS 降至 0.224，比 Unianimate（0.231）降低 0.007；FVD 为 133.95，较 Animate-X（139.01）下降 5.06。值得注意的是，PoseAnything 仅在 TikTok 训练集上训练 1500 次迭代即取得上述结果，而多数基线方法使用了更大规模的训练数据，这从侧面反映了通道拼接注入策略与部件感知时序一致性模块的样本效率优势。

**非人体姿态引导（XPose 基准）**。Table 2 的定量对比覆盖了基于拖拽的方法（**ATI**、**Tora**、**SG-I2V**）等非人体基线。PoseAnything 在 PSNR（30.29 vs. ATI 30.15）、SSIM（0.7114 vs. Tora 0.6929）、LPIPS（0.3241 vs. Tora 0.3530）和 FVD（99.97 vs. ATI 101.44）四项指标上均取得最优。XPose 的 51 个测试视频在训练阶段被完全排除，保证了评估的公平性。Figure 7 的定性对比进一步显示，基线方法在非人体主体上常出现肢体错位、外观漂移或背景失真，而 PoseAnything 能够保持部件级的外观一致性和准确的姿态跟随。

### 消融实验

消融实验围绕三个关键设计展开：部件感知时序一致性模块（PTCM）、条件注入策略和稀疏姿态条件注入。

**PTCM 的贡献**。Table 3 对比了三种变体：(1) 仅使用通道拼接的基线（Concat）；(2) 在拼接基础上加入全局交叉注意力的增强一致性模块（EC）；(3) 完整的 PTCM。结果显示，PTCM 在全部四项指标上均优于前两者：PSNR 30.29 vs. 29.85（Concat）和 30.27（EC），SSIM 0.7114 vs. 0.6964/0.7107，LPIPS 0.3241 vs. 0.3304/0.3243，FVD 99.97 vs. 102.30/101.50。全局交叉注意力（EC）虽能带来一定增益，但 PTCM 通过将整体外观一致性分解为部件级控制，实现了更精细的时序一致性，这一定性优势在 Figure 4 的注意力权重可视化（Figure 9）中也得到了印证——匹配的部件对在注意力图上呈现清晰的对齐模式。

**条件注入策略**。Table 4 比较了三种注入方式：MLP 融合（Concat by MLP）、宽度拼接（Concat by Width）和通道拼接（Concat by Channel）。通道拼接在所有指标上均显著领先：PSNR 31.50，SSIM 0.8362，FVD 133.95。与 MLP 融合相比，FVD 降低了 52.8%，表明通道维度的信息保留对视频生成质量至关重要。Figure 10 和 Figure 11 分别展示了三种策略的结构差异与定性生成效果，MLP 融合在复杂姿态下容易出现主体模糊和细节丢失。

**稀疏姿态注入**。Table 5 检验了 PTCM 在仅注入部分帧姿态条件下的时序插值能力。当仅注入 10% 帧的姿态时，PSNR 为 30.21，SSIM 0.733，LPIPS 0.317，FVD 97.02，与全量注入相比性能下降极小；即使仅注入 2.5% 帧，PSNR 仍保持 29.82，SSIM 0.6757。这表明 PTCM 的部件匹配机制具备强大的时序外推能力，能够在稀疏条件下维持部件级一致性。Figure 12 的定性对比显示，稀疏注入下的生成结果在主体外观保持和运动平滑性方面与全量注入几乎无异。

**CFG 尺度的影响**。Table 6 揭示了 CFG 尺度与注入密度之间的交互效应。在密集注入条件下，当 CFG 尺度从 1.2 增至 5.0 时，PSNR 从 30.61 降至 29.92，表明过强的引导会损害生成质量；而在稀疏注入条件下，模型对高 CFG 尺度的容忍度更高。Figure 13 的定性对比显示，高 CFG 尺度在密集注入时会导致过饱和和伪影，而在稀疏注入时则能有效增强姿态跟随性而不引入明显失真。

### 相机运动解耦控制

Figure 8 展示了 Subject and Camera Motion Decoupled CFG 的实际效果。通过将主体姿态注入 CFG 正锚点、相机运动注入负锚点，模型能够同时响应两个独立的运动信号：主体按照姿态序列执行动作，而相机平滑地执行推拉、平移等运动。该机制首次在姿态引导视频生成中实现了主体与相机运动的独立控制，消除了传统方法中两者相互干扰的问题。

### 失败模式与局限性

尽管 PoseAnything 在定量和定性评估中表现优异，仍存在若干值得关注的局限：

1. **极端骨架变形的鲁棒性**：PTCM 的部件匹配依赖跨帧注意力权重，当骨架段数极多或变形剧烈时，注意力匹配可能出现错误，导致部件错位。该问题在 XPose 的高难度子集（Figure 16）中有所显现，但缺乏系统的量化分析。

2. **相机运动覆盖范围**：Decoupled CFG 通过注入相机运动的相反信号实现控制，但当前仅验证了有限的相机运动类型（推拉、平移），更复杂的相机路径（如弧线运动、变焦）的自动化程度和生成质量尚未充分讨论。

3. **多主体与遮挡场景**：当前框架仅考虑单主体场景，PTCM 的部件分割和匹配机制尚未扩展到多主体交互或主体间遮挡的情形。

4. **CFG 尺度自适应**：CFG 尺度对注入密度敏感，但当前缺乏自动化的尺度选择策略，需要针对不同场景进行手动调参。

以上局限为后续研究提供了明确方向：部件匹配机制的鲁棒性增强、相机运动控制的路径规划自动化、以及向多主体场景的扩展。

![[assets/figures/papers/PoseAnything_Universal_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coh_78f56b8ab3f0/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparisons with the state-of-the-arts on TikTok dataset (Human)*

![[assets/figures/papers/PoseAnything_Universal_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coh_78f56b8ab3f0/figures/010_Table_3.jpg]]
*Table 3: Quantitative results of ablation study. ing to the pose guidance, while the camera simultaneously executes the specified movement smoothly and coherently. The ability to maintain high fidelity for both the subject’s action and the global camera motion provides strong empirical evidence that our method effectively disentangles the two control signals, achieving the precise and independent manipulation it was designed for*

![[assets/figures/papers/PoseAnything_Universal_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coh_78f56b8ab3f0/figures/011_Table_2.jpg]]
*Table 2: Quantitative comparison between the state-of-the-arts and Ours on XPose-benchmark (Non-human)*

![[assets/figures/papers/PoseAnything_Universal_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coh_78f56b8ab3f0/figures/015_Table_4.jpg]]
*Table 4: Quantitative Comparison of Injection Strategies*

![[assets/figures/papers/PoseAnything_Universal_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coh_78f56b8ab3f0/figures/016_Table_5.jpg]]
*Table 5: Quantitative Result of Sparse Pose Condition Injectionattn_weights挑选层数/timesteps数, attn_weights可视化*

## 定位与知识库关联

### 1. 技术路径与基线关系

PoseAnything 处于**姿态引导视频生成**这一技术路线上，但其核心贡献在于将该范式的适用边界从人体姿态拓展至任意骨架结构，并首次实现了主体运动与相机运动的解耦控制。

在人体姿态引导子领域，PoseAnything 与以下方法构成直接对比关系：

- **Disco**、**MagicAnimate**、**MagicPose**、**AnimateAnyone**、**Champ**、**Unianimate**、**Animate-X**：这些方法均面向人体姿态引导的视频生成，其共同瓶颈在于仅支持预定义的人体骨骼拓扑（通常为 COCO 17 关键点或 SMPL 骨架），无法泛化至非人体主体。PoseAnything 在 TikTok 数据集上以 PSNR 31.50、SSIM 0.836、FVD 133.95 全面超越上述方法（Table 1），其中相较最强的 Animate-X（PSNR 30.78）提升 +0.72 dB，相较 Unianimate（SSIM 0.811）提升 +0.025。

在非人体/通用运动迁移子领域，PoseAnything 与以下基于拖拽或光流的方法形成对比：

- **ATI**、**Tora**、**SG-I2V**：这些方法通过拖拽点或轨迹实现运动控制，可处理非人体主体，但缺乏对骨架结构的显式建模，导致运动精度和外观一致性不足。PoseAnything 在 XPose-benchmark 上以 PSNR 30.29、SSIM 0.7114、FVD 99.97 超越上述方法（Table 2），其中相较 ATI（PSNR 30.15）提升 +0.14 dB，相较 Tora（SSIM 0.6929）提升 +0.0185。

**因果机制差异**：现有方法在条件注入策略上普遍采用 MLP 融合或宽度拼接（Concat by Width），PoseAnything 的消融实验（Table 4）表明，通道拼接（Concat by Channel）策略使 FVD 相较 MLP 融合降低 52.8%，这构成了其性能优势的重要工程基础。在时序一致性控制上，现有方法依赖全局交叉注意力或 ControlNet，而 PoseAnything 的 PTCM 模块将整体外观一致性分解为部件级控制，消融实验（Table 3）显示 PTCM 相较纯拼接基线在 PSNR 上提升 0.44 dB（29.85 → 30.29），相较全局交叉注意力变体（EC）在 FVD 上降低 1.53（101.50 → 99.97）。

### 2. 适用边界

PoseAnything 的适用边界由其三个核心模块的能力范围共同决定：

**（1）骨架通用性边界**：该方法支持任意骨架拓扑的输入，理论上可处理从简单刚性物体到高度铰接的非人体角色。但论文未量化极端骨架变形（如超过 50 个骨架段的复杂铰接结构）下的性能退化程度，也未讨论骨架段数量与生成质量之间的标度律。XPose 数据集的统计分布（Figure 3）显示骨架段数主要集中在 5-20 段区间，超出此范围的泛化能力缺乏实验支撑。

**（2）部件感知时序一致性边界**：PTCM 依赖跨帧注意力权重进行部件匹配（Eq. 8），其匹配精度在以下场景可能退化：① 初始去噪步数不足时注意力图尚未收敛；② 骨架段高度重叠或自遮挡导致部件掩码边界模糊；③ 运动幅度过大导致跨帧部件对应关系断裂。论文通过注意力权重可视化（Figure 9）定性展示了匹配效果，但未给出匹配失败率的量化统计。

**（3）运动解耦控制边界**：Decoupled CFG 将主体姿态注入正锚点、相机运动注入负锚点（Eq. 10），实现了两类运动的独立控制。但该方法要求显式指定相机运动信号，自动化程度有限。论文仅展示了平移和缩放两类相机运动（Figure 8），更复杂的相机路径（如旋转、倾斜、推拉组合）的覆盖面和连续控制精度未经系统评估。

**（4）数据依赖边界**：PoseAnything 基于 Wan2.2-TI2V-5B 预训练模型，其生成质量依赖于底层扩散先验的覆盖范围。对于 Wan2.2 训练分布中罕见的主体类别或运动模式，即使骨架条件正确，生成结果仍可能出现纹理失真或运动不自然。

### 3. 局限与开放问题

**已识别的局限性**：

1. **部件匹配的脆弱性**：PTCM 的部件匹配机制依赖于注意力权重的准确性，在初始步数不足或骨架极端复杂时可能产生错误匹配，导致部件错位或外观混叠。该问题未被量化分析，仅通过定性可视化间接展示。

2. **相机控制的有限覆盖**：Decoupled CFG 需要反向注入相机运动的相反信号，相机运动类型的覆盖面有限。论文未讨论旋转、倾斜等复杂相机运动的控制效果，也未提供相机运动连续性的定量评估指标。

3. **单主体假设**：当前框架仅考虑单主体场景，未涉及多主体交互或主体间遮挡的处理机制。

**开放问题**：

1. **CFG 尺度的自适应调节**：消融实验（Table 6）表明，密集姿态注入下 CFG 尺度从 1.2 增至 5.0 时 PSNR 从 30.61 降至 29.92，而稀疏注入下退化幅度较小。如何根据姿态密度自动选择最优 CFG 尺度仍是一个开放问题。

2. **极端分布外泛化**：对于高度铰接的非人体角色或极端骨架变形，PoseAnything 的泛化能力未经量化评估。XPose 数据集的难度分层（Figure 14-16）提供了测试基础，但论文未报告各难度子集上的性能差异。

3. **多主体扩展**：PTCM 的部件分割和匹配机制在理论上可扩展至多主体场景，但如何处理主体间遮挡、如何区分不同主体的部件对应关系，仍需进一步研究。

4. **相机路径规划自动化**：当前 Decoupled CFG 需要人工指定相机运动信号，如何实现端到端的相机路径规划（如根据场景内容自动生成合理的相机运动）是提升实用性的关键方向。

5. **稀疏注入的理论解释**：稀疏姿态注入实验（Table 5）表明，仅注入 10% 帧的姿态条件即可维持 PSNR 30.21 的生成质量，甚至在 2.5% 注入率下仍保持竞争力。这种强时序插值能力的理论机制（是预训练模型的先验知识还是 PTCM 的部件匹配在起作用）尚未被深入分析。

## 原文 PDF

![[paperPDFs/arxiv_2025/PoseAnything_Universal_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.pdf]]

---
title: "KinemaDiff: Towards Diffusion for Coherent and Physically Plausible Human Motion Prediction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/KinemaDiff_Towards_Diffusion_for_Coherent_and_Physically_Plausible_Human_Motion_Prediction.pdf
project_link: null
code_link: null
openreview_forum_id: uxTQeKAUh5
aliases:
- KinemaDiff
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "每个关节的噪声注入幅度（联合自适应噪声）以及每步去噪过程中骨骼长度的一致性约束（结构对齐正则化）。"
primary_logic: "通过在扩散过程中直接嵌入依据关节动力学特性学习的异质噪声，并利用历史运动的骨骼结构逐步骤约束生成结果，可以同时提升运动多样性和物理合理性，从而实现更逼真的人体运动生成。"
claims:
- "联合自适应噪声和结构对齐正则化共同降低了预测误差并提高了物理真实性。"
- "逐步施加骨骼长度约束优于仅在最终步施加约束，骨骼拉伸显著减少。"
- "学习的关节噪声幅度与运动学自由度一致，动态关节（如腕、脚）获得更大噪声，反常识的噪声分配严重损害性能。"
- "在 Human3.6M 和 AMASS 上，本方法在准确度和真实性指标上均达到最优，FID 相对此前最佳模型 CoMusion 提升约 19%。"
---

# KinemaDiff: Towards Diffusion for Coherent and Physically Plausible Human Motion Prediction

> [!tip] 核心洞察
> 通过在扩散过程中直接嵌入依据关节动力学特性学习的异质噪声，并利用历史运动的骨骼结构逐步骤约束生成结果，可以同时提升运动多样性和物理合理性，从而实现更逼真的人体运动生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | KinemaDiff：面向连贯且物理合理的人体运动预测的扩散方法 |
| 英文题名 | KinemaDiff: Towards Diffusion for Coherent and Physically Plausible Human Motion Prediction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=uxTQeKAUh5) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | KinemaDiff |
| Dataset | Human3.6M, AMASS |

> [!tip] 效果简介
> - Human3.6M 上，ADE (平均位移误差) 为 0.331，对比 0.350 (CoMusion)，变化 -0.019。
> - Human3.6M 上，FDE (最终位移误差) 为 0.449，对比 0.494 (CoMusion)，变化 -0.045。
> - Human3.6M 上，FID (Fréchet Inception Distance) 为 0.083，对比 0.102 (CoMusion)，变化 −19% (相对改善)。

## 概要

人体运动预测的核心挑战在于生成既多样又符合人体解剖学约束的合理运动序列。现有的扩散式方法普遍采用均匀高斯噪声注入所有关节，忽视了不同关节在运动学自由度上的本质差异；同时，这些方法缺乏对骨骼结构的显式建模，导致生成的运动常出现肢体拉伸、骨骼变形等物理不合理现象。

针对上述瓶颈，本文提出 **KinemaDiff**，一个将人体骨骼结构与关节特异性运动动力学直接嵌入扩散过程的框架。其核心调控机制包含两个关键模块：

- **联合自适应噪声生成器**：依据关节索引与历史运动轨迹，为每个关节学习实例化的异质噪声方差 $\Sigma = \mathrm{diag}(s_1^2, \dots, s_J^2)$，使高动态关节（如腕部、脚部）获得更大的噪声扰动，从而增强运动多样性。
- **结构对齐正则化器**：在每一步去噪过程中，强制预测的骨骼长度与历史观测的平均骨骼长度保持一致，直接在扩散轨迹上施加解剖学一致性约束，而非事后校正。

通过直接预测干净运动 $\hat{y}_0$（而非噪声 $\epsilon$），KinemaDiff 得以在全去噪过程中持续施加结构先验。在 Human3.6M 和 AMASS 两个基准上的实验表明，该方法在准确度（ADE、FDE）与运动真实性（FID）上均达到最优水平，其中 FID 相较此前最佳扩散模型 **CoMusion**（Sun & Chowdhary, ECCV 2024）实现了约 19% 的相对提升（0.102 → 0.083）。消融实验进一步验证了联合自适应噪声与逐步骨骼约束各自的关键贡献：移除结构对齐正则化使 FID 从 0.088 急剧恶化至 0.177；而仅在后几步施加骨骼约束则导致肢体拉伸从 2.4 升至 3.7。

需要指出的是，该方法在追求高物理真实度时，生成多样性（APD）略低于不强调物理约束的模型（如 **MotionDiff**, Wei et al., AAAI 2023），这属于真实度与多样性之间的可控权衡。此外，当前验证仅限于受控室内场景（Human3.6M）与多数据集汇集场景（AMASS），在遮挡、多人交互等复杂条件下的泛化能力尚待检验。



人体运动预测是计算机视觉与具身智能中的核心任务，其目标是根据观测到的历史姿态序列，生成未来一段时间的合理运动轨迹。该任务在自动驾驶、人机交互、运动分析和虚拟角色动画等领域具有广泛的应用前景。然而，人体运动的高维性、时空耦合性以及物理约束的隐式性，使得生成既准确又物理合理的长期运动序列成为一个极具挑战性的问题。

近年来，扩散模型在图像和视频生成领域取得了显著成功，其通过逐步去噪生成高质量样本的能力也被引入到人体运动预测中。以 **MotionDiff**（Wei et al., AAAI 2023）为代表的早期工作建立了二阶段扩散运动预测框架，**HumanMAC**（Chen et al., ICCV 2023）则通过掩码补全简化了训练流程。在此基础上，**CoMusion**（Sun & Chowdhary, ECCV 2024）在 DCT 空间使用图卷积网络捕获时空依赖，取得了当时最优的生成质量。**BeLFusion**（Barquero et al., ICCV 2023）则探索了基于 VAE 潜在空间的扩散方法，并将物理一致性检验作为后处理步骤。

尽管这些方法在运动多样性上取得了进展，但它们共享一个关键瓶颈：**现有扩散式运动预测方法使用均匀的高斯噪声对所有关节进行同等强度的扰动，忽视了不同关节在运动学上的天然异质性**。例如，腕关节和踝关节在人体运动中具有远高于脊柱关节的自由度和活动范围，但标准扩散过程却对它们施加相同的噪声尺度。这种“一刀切”的噪声策略导致生成的运动序列中，高动态关节的多样性不足，而低动态关节又被过度扰动，最终产生不自然的运动模式。

更严重的是，**现有方法缺乏对骨骼结构的显式约束**。人体骨骼是一组通过关节连接的刚体链，相邻关节之间的距离（骨骼长度）在运动过程中应保持恒定。然而，现有扩散模型仅在数据分布层面隐式地学习这种解剖学约束，无法保证生成结果的骨骼一致性。这直接导致了生成运动中常见的骨骼变形、肢体拉伸等物理不合理现象。虽然 **SkeletonDiffusion**（Curreli et al., CVPR 2025）尝试引入基于静态骨架树的各向异性噪声，但其噪声特性是固定的，无法根据具体运动实例进行自适应调整。

上述两个缺陷——均匀噪声与缺失结构约束——并非孤立存在，而是相互耦合的：均匀噪声破坏了运动学上合理的关节协同模式，而缺乏结构约束则使得去噪过程无法纠正由此产生的骨骼变形，两者共同导致生成运动的物理可信度下降。

针对这些问题，本文提出 **KinemaDiff**，一个从扩散过程内部重塑人体运动生成的新框架。其核心动机在于：**将人体骨骼结构和关节特异性运动动力学直接嵌入扩散过程**，而非将其视为后处理或外部约束。具体而言，KinemaDiff 通过两个关键模块实现这一目标：（1）**联合自适应噪声生成器**，根据关节索引和历史运动轨迹学习每个关节的实例化噪声方差，使噪声注入与关节的运动学自由度相匹配；（2）**结构对齐正则化器**，在每一步去噪过程中强制预测的骨骼长度与历史观测的平均骨骼长度保持一致，从源头上消除骨骼变形。通过这种“噪声异质化 + 结构逐步骤约束”的双重机制，KinemaDiff 旨在同时提升运动多样性和物理合理性，实现更逼真的人体运动生成。



## 核心方法与创新机理

KinemaDiff 的核心创新并非引入全新的生成范式，而是对扩散式人体运动预测框架中的两个关键“控制旋钮”进行了根本性重塑：**噪声注入方式**与**结构约束机制**。这两个改进直接针对现有方法的两大瓶颈——忽视关节运动学异质性的均匀噪声假设，以及缺乏显式骨骼约束导致的物理不合理变形。

### 从均匀噪声到联合自适应噪声

现有扩散式运动预测方法（如 **CoMusion** (Sun & Chowdhary, ECCV 2024)、**MotionDiff** (Wei et al., AAAI 2023)）普遍采用标准 DDPM 的前向过程，对所有关节点施加相同强度的高斯噪声：

$$q ( y _ { t } \mid y _ { t - 1 } ) = \mathcal { N } \big ( y _ { t } ; \sqrt { \alpha _ { t } } y _ { t - 1 } , ( 1 - \alpha _ { t } ) \mathbf { I } \big )$$

这一假设忽略了人体运动学的基本事实：不同关节的自由度和运动范围存在本质差异。例如，腕关节的活动范围远大于肘关节，而均匀噪声无法捕捉这种异质性，导致生成的运动缺乏关节级别的自然差异。

KinemaDiff 将上述过程替换为**联合自适应扩散**：

$$q ( y _ { t } \mid y _ { t - 1 } ) = \mathcal { N } \big ( y _ { t } ; \alpha _ { t } y _ { t - 1 } , ( 1 - \alpha _ { t } ) \Sigma \big ), \quad \Sigma = \mathrm { d i a g } ( s _ { 1 } ^ { 2 } , \dots , s _ { J } ^ { 2 } )$$

其中每个关节的噪声缩放因子 $s_j$ 由一个可学习的函数动态生成：

$$s _ { j } = f _ { \theta } ( j , \mathbf { x } _ { j } ^ { ( 1 : H ) } )$$

这一设计的因果机制在于：噪声强度同时取决于**关节身份**（$j$，编码了该关节固有的运动学属性）和**该关节的历史运动轨迹**（$\mathbf{x}_j^{(1:H)}$，提供实例化的运动模式信息）。这意味着对于同一关节，不同样本（如“走路”与“跳舞”）也会获得不同的噪声强度，实现样本级别的自适应。

消融实验（Table 8）验证了这一机制的因果链条：仅保留静态关节噪声（No Temporal）时，性能已优于完全均匀噪声；引入时序运动信息后，性能进一步提升。一个反向验证更为有力——当故意将学习的噪声分配反转（Reverse-scale，即给静态关节分配大噪声、动态关节分配小噪声）时，ADE 退化至 0.349、FID 恶化至 0.115（Table 11），证明噪声分配与关节运动学自由度的一致性并非巧合，而是性能的关键驱动因素。

### 从隐式学习到逐步结构对齐

现有方法对骨骼结构的处理存在两种局限：一是依赖模型隐式学习关节间的空间关系（如 **CoMusion** 的 GCN），缺乏显式约束；二是仅在生成完成后进行后处理校正（如 **BeLFusion** (Barquero et al., ICCV 2023)），无法在生成过程中阻止骨骼变形的累积。

KinemaDiff 的**结构对齐正则化器**（Structure-Aligned Regularizer）改变了这一范式：在**每一步去噪过程中**，强制预测的骨骼长度与历史观测的平均骨骼长度保持一致。具体而言，损失函数同时约束预测骨架和经验重建骨架：

$$\mathcal { L } _ { \mathrm { a l i g n } } = \frac { 1 } { | \mathcal { E } | } \sum _ { ( i , j ) \in \mathcal { E } } | \bar { b } _ { \mathrm { o b s } } ^ { ( i , j ) } - \bar { b } _ { \mathrm { p r e d } } ^ { ( i , j ) } | _ { 2 } + \frac { 1 } { | \mathcal { E } | } \sum _ { ( i , j ) \in \mathcal { E } } | \bar { b } _ { \mathrm { o b s } } ^ { ( i , j ) } - \bar { b } _ { \mathrm { r e f } } ^ { ( i , j ) } | _ { 2 }$$

这一设计之所以可行，得益于 KinemaDiff 采用了**直接预测干净运动**（direct $y_0$ prediction）的策略，而非标准 DDPM 的噪声预测。这使得模型在每一步都能获得显式的姿态估计，从而施加结构先验。

逐步约束的因果效应在 Table 14 中得到清晰验证：在所有去噪步上施加骨骼长度约束时，骨骼拉伸值（Stretch）仅为 2.4；若仅在最后 20% 或 30% 的步数施加约束，拉伸值分别升至 3.7 和 3.4，且 ADE/FDE/FID 均变差。这表明早期去噪阶段的骨骼约束对于防止变形累积至关重要。

### 两个创新点的协同效应

消融实验（Table 3）揭示了两个模块的协同关系：仅使用联合自适应噪声（Encoder+J-Noise）时，FID 为 0.088；加入结构对齐正则化后，FID 进一步降至 0.083。反过来，若移除结构对齐而仅保留自适应噪声，FID 急剧恶化至 0.177。这表明自适应噪声主要贡献于运动多样性和关节级建模精度，而结构对齐正则化是物理真实性的核心保障——两者并非独立改进，而是在“多样性-真实性”轴上形成互补。



![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/003_Figure_3.jpg]]
*Figure 3: The overview of our proposed Kinemadiff. (a): Our Joint-adaptive noise generator. We learn joint-adaptive noise from the historical human joints and add it to the future human motions. (b): Initial motion reconstruction. The future human motion with injected noise is processed through a self-attention mechanism, which generates an initial prediction in the absence of external conditioning. (c): Structure-Aligned Regularizer. The initial prediction is concatenated with the motion observations and then processed in the frequency domain through a frequency-aware GCN, and subsequently transformed back to the temporal domain for structural alignment*

KinemaDiff 的整体 pipeline 围绕一个核心洞察构建：**在扩散过程中直接嵌入关节异质噪声与骨骼结构约束，可以同时提升运动多样性与物理合理性**。框架由三个协同模块串联而成，形成“噪声注入—初始重建—结构对齐”的闭环。

### 输入输出流

给定一段历史观测运动序列 $x$（$H$ 帧），目标是对未来 $T$ 帧的人体姿态 $y$ 进行预测。整个去噪过程的起点是随机采样的高斯噪声，终点是干净的运动预测 $\hat{y}_0$。与标准 DDPM 预测噪声 $\epsilon$ 不同，KinemaDiff 采用 **直接预测干净运动**（direct $y_0$ prediction）的策略，使得在去噪的每一步都能施加骨骼结构先验。

### 三大模块的协同机制

1. **联合自适应噪声生成器（Joint-Adaptive Noise Generator）**
   该模块位于 pipeline 最前端，负责为每个关节生成实例化的异质噪声。它依据关节索引 $j$ 和历史运动轨迹 $\mathbf{x}_j^{(1:H)}$，学习逐关节的噪声缩放因子 $s_j = f_\theta(j, \mathbf{x}_j^{(1:H)})$，构造对角协方差矩阵 $\Sigma = \mathrm{diag}(s_1^2, \dots, s_J^2)$。这一设计使得动态关节（如腕、踝）获得更大的噪声扰动幅度，而稳定关节（如髋、肩）则保持较小的噪声，从而在扩散起点就注入了符合运动学特性的多样性。

2. **初始编码器（Initial Encoder）**
   由两层 Transformer 堆叠而成（特征维度 512），接收注入自适应噪声后的未来帧，输出初始运动重建。该模块提供无外部条件的基线预测，为后续的结构对齐提供待优化的初始解。

3. **结构对齐正则化器（Structure-Aligned Regularizer）**
   这是 pipeline 的核心约束模块，在**每一步去噪过程中**强制预测的骨骼长度与历史观测的平均骨骼长度一致。具体而言，它通过频率特异性 GCN 建模完整运动序列，分别计算预测骨架和经验重建骨架的平均骨骼长度，并与历史骨骼长度施加 L2 对齐损失 $\mathcal{L}_{\mathrm{align}}$。该损失与重建损失 $\mathcal{L}_{\mathrm{rec}}$ 加权组合，形成总训练目标：

   $$\mathcal{L}_{\mathrm{total}} = \alpha \cdot \mathcal{L}_{\mathrm{rec}} + \beta \cdot \mathcal{L}_{\mathrm{align}}$$

### 推理流程

推理时采用 10 步 DDPM 采样。每一步的去噪过程为：从当前含噪运动 $y_t$ 出发，经初始编码器得到 $\hat{y}_0$，再经结构对齐正则化器施加骨骼长度约束，最后通过逆向扩散步更新得到 $y_{t-1}$。两个核心模块——联合自适应噪声生成器和结构对齐正则化器——均内嵌于扩散步内，而非作为后处理步骤。

消融实验（Table 3）验证了这一协同设计的必要性：去除结构对齐正则化器后，FID 从 0.083 急剧升至 0.177，ADE/FDE 也明显恶化；去除联合自适应噪声则导致多样性下降和预测精度损失。全模型在 Human3.6M 上取得了 ADE 0.331、FDE 0.449、FID 0.083 的最优结果。



### 扩散过程基础

KinemaDiff 建立在条件扩散模型的框架之上。给定历史观测运动 $x \in \mathbb{R}^{H \times J \times 3}$（$H$ 帧、$J$ 个关节），目标是生成未来运动序列 $y \in \mathbb{R}^{T \times J \times 3}$。标准的前向扩散过程逐步向干净运动 $y_0$ 添加高斯噪声：

$$q(y_t \mid y_{t-1}) = \mathcal{N}\big(y_t; \sqrt{\alpha_t} y_{t-1}, (1 - \alpha_t) \mathbf{I}\big) \tag{1}$$

其中 $\alpha_t$ 为噪声调度参数。逆向去噪过程以历史运动 $x$ 为条件，逐步从纯噪声恢复出干净运动：

$$p_{\theta}(y_{t-1} \mid y_t, x) = \mathcal{N}\big(y_{t-1}; \mu_{\theta}(y_t, x, t), \sigma_{\theta}^2(y_t, x, t) \mathbf{I}\big) \tag{2}$$

与大多数预测噪声 $\epsilon$ 的扩散模型不同，KinemaDiff 采用**直接预测干净运动 $\hat{y}_0$** 的策略。这一设计的核心动机在于：只有在每一步去噪过程中都能获得显式的姿态预测，才能在扩散全过程中持续施加骨骼结构先验约束。

---

### 联合自适应噪声生成器

现有扩散方法对所有关节施加均匀的高斯噪声，忽视了人体运动学中不同关节的自由度差异——例如腕关节的运动范围远大于肩关节。KinemaDiff 提出**联合自适应噪声生成器**，为每个关节学习实例化的噪声方差。

前向扩散过程被重新定义为带有异质协方差矩阵的形式：

$$q(y_t \mid y_{t-1}) = \mathcal{N}\big(y_t; \alpha_t y_{t-1}, (1 - \alpha_t) \Sigma\big), \quad \Sigma = \mathrm{diag}(s_1^2, \dots, s_J^2) \tag{3}$$

其中 $s_j$ 是关节 $j$ 的噪声缩放因子，由一个小型神经网络从关节索引和历史运动轨迹中学习得到：

$$s_j = f_{\theta}(j, \mathbf{x}_j^{(1:H)}) \tag{4}$$

这里 $\mathbf{x}_j^{(1:H)}$ 表示关节 $j$ 在历史 $H$ 帧中的完整轨迹。该设计的因果机制在于：**$s_j$ 同时编码了关节身份（静态运动学特性）和运动历史（动态行为模式）**，使得噪声强度能够自适应地匹配每个关节的实际运动自由度。实验证据表明，学习的噪声幅度与运动学自由度高度一致——动态关节（如腕、脚）获得更大的噪声注入，而若将噪声分配反转（Reverse-scale），ADE 将退化至 0.349、FID 升至 0.115（Table 11），验证了自适应噪声分配的因果有效性。

---

### 结构对齐正则化器

仅靠自适应噪声不足以防止生成运动中的骨骼变形和肢体拉伸。KinemaDiff 进一步提出**结构对齐正则化器**，在每一步去噪过程中显式约束预测的骨骼长度与历史观测保持一致。

该模块的核心思想基于一个关键观察：在扩散过程的任意时刻 $t$，含噪运动 $y_t$ 可分解为干净信号与零均值噪声的叠加：

$$y_t = \sqrt{\bar{\alpha}_t} y_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon \tag{5}$$

通过对批次内多个样本取平均，零均值噪声项趋于抵消，从而获得干净运动的近似估计：

$$\bar{y}_t = \frac{1}{B} \sum_{b=1}^{B} y_t^{(b)} \approx \sqrt{\bar{\alpha}_t} y_0 \tag{6}$$

利用这一近似，正则化器在频域通过频率特异性 GCN 建模完整运动序列的骨骼结构，并施加骨骼长度对齐损失：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{|\mathcal{E}|} \sum_{(i,j) \in \mathcal{E}} \big| \bar{b}_{\mathrm{obs}}^{(i,j)} - \bar{b}_{\mathrm{pred}}^{(i,j)} \big|_2 + \frac{1}{|\mathcal{E}|} \sum_{(i,j) \in \mathcal{E}} \big| \bar{b}_{\mathrm{obs}}^{(i,j)} - \bar{b}_{\mathrm{ref}}^{(i,j)} \big|_2 \tag{7}$$

其中 $\mathcal{E}$ 为骨架边集，$\bar{b}_{\mathrm{obs}}^{(i,j)}$ 为历史观测中关节对 $(i,j)$ 的平均骨骼长度，$\bar{b}_{\mathrm{pred}}^{(i,j)}$ 为直接预测 $\hat{y}_0$ 的骨骼长度，$\bar{b}_{\mathrm{ref}}^{(i,j)}$ 为通过批次平均近似恢复的骨骼长度。该损失同时约束两条路径，确保骨骼结构的双重一致性。

---

### 总训练目标

最终训练目标为加权联合损失：

$$\mathcal{L}_{\mathrm{total}} = \alpha \cdot \mathcal{L}_{\mathrm{rec}} + \beta \cdot \mathcal{L}_{\mathrm{align}} \tag{8}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为预测运动与真实运动之间的重建损失。消融实验（Table 3）验证了两个模块的独立贡献：移除结构对齐正则化器使 FID 从 0.083 飙升至 0.177，而移除联合自适应噪声生成器则导致 ADE 和 FDE 显著恶化，证实了两者在提升准确度和物理真实性方面的互补作用。



## 实验与关键发现

### 主要结果

#### Human3.6M 基准测试

KinemaDiff 在 Human3.6M 数据集上与 GAN 类、VAE 类及扩散类共 13 种方法进行了全面对比。如表 1 所示，该方法在准确度与真实度指标上均达到最优：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on Human3.6M. The best results are highlighted in bold. The symbol ‘–’ indicates not reported in the baseline work. For all metrics except for APD, lower is better*

- **ADE (平均位移误差)**：0.331，较此前最佳的 **CoMusion**（Sun & Chowdhary, ECCV 2024）的 0.350 降低了 5.4%。
- **FDE (最终位移误差)**：0.449，较 CoMusion 的 0.494 降低了 9.1%。
- **FID (Fréchet Inception Distance)**：0.083，较 CoMusion 的 0.102 实现了约 19% 的相对改善，表明生成运动的分布与真实运动分布高度一致。

在多样性与多模态指标上，KinemaDiff 的 APD 为 6.912，低于部分不强调物理约束的方法（如 **MotionDiff** 的 15.353），但作者指出这是高真实度与高多样性之间的可控取舍——所有生成样本均保持在解剖可行域内，避免了其他方法中常见的骨骼变形问题。

#### AMASS 跨数据集泛化

在更具挑战性的跨数据集场景下（Human3.6M 训练，AMASS 测试），KinemaDiff 同样展现出优异的泛化能力。如表 2 所示，该方法在 6 项指标中的 4 项取得最优：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/005_Table_2.jpg]]
*Table 2: Quantitative results for AMASS dataset. The best results are highlighted in bold. As AMASS does not contain class labels, the FID metric is not used for evaluation*

- **ADE**：0.478（CoMusion 为 0.494）
- **FDE**：0.540（CoMusion 为 0.547）
- **MMADE**：0.456
- **MMFDE**：0.457

这一泛化性能归因于结构对齐正则化器学习的是骨骼长度等内在且不变的解剖属性，而非与特定场景绑定的运动模式。

---

### 消融实验

#### 核心模块消融

表 3 系统评估了三个核心组件的贡献：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/006_Table_3.jpg]]
*Table 3: Ablation of the main components in our method on Human3.6M. Table 4: Experiment results on Human3.6M with different Scheduler*

| 配置 | APD ↑ | ADE ↓ | FDE ↓ | FID ↓ |
|------|-------|-------|-------|-------|
| 仅 Encoder | 1.186 | 0.378 | 0.518 | 0.177 |
| Encoder + J-Noise | 6.912 | 0.331 | 0.449 | 0.088 |
| Encoder + J-Noise + Align (完整模型) | 6.912 | 0.331 | 0.449 | **0.083** |

关键发现：
1. **初始编码器**的作用是大幅压缩多样性（APD 从无编码器时的 16.537 降至 1.186），将生成约束在合理运动空间内。
2. **联合自适应噪声**在此基础上恢复了多样性（APD 回升至 6.912），同时显著提升准确度（ADE 降至 0.331）。
3. **结构对齐正则化**的加入并未改变 ADE/FDE，但将 FID 从 0.088 进一步降至 0.083，表明骨骼约束主要提升运动的真实感而非逐帧精度。移除该模块会导致 FID 急剧恶化至 0.177。

#### 噪声调度器选择

表 4 对比了三种噪声调度策略。**方差调度器**（Variance Scheduler）在准确度与真实度之间取得最佳平衡（ADE 0.331, FID 0.083），优于标准余弦调度和均方根调度。余弦调度虽获得最高多样性（APD 7.213），但 FID 退化为 0.102。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/007_Table_4.jpg]]
*Table 4: 2023), we use the Cumulative Motion Distribution (CMD) area for global plausibility to evaluate how realistically the model’s generated diversity reflects that of the ground truth*

#### 联合自适应噪声的深入分析

表 8 的消融揭示了自适应噪声的两个关键维度：
- **无关节噪声**（均匀噪声）：性能显著下降，验证了关节异质噪声的必要性。
- **仅静态关节噪声**（无时序信息）：优于完全均匀噪声，但仍弱于完整模型，表明自适应噪声需同时依赖关节身份和运动历史。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/022_Table_8.jpg]]
*Table 8: Detailed ablation of the Joint-Adaptive Noise Generator. The full model achieves the best accuracy and realism while maintaining competitive diversity*

表 10 展示了学习到的各关节噪声尺度：腕部、脚部等动态关节获得更大的噪声幅度，与运动学自由度高度一致。表 11 进一步验证了这一分配的必要性——若反转噪声分配（动态关节小噪声、静态关节大噪声），ADE 退化至 0.349、FID 恶化至 0.115，证实了该机制并非简单的噪声幅度调节，而是对关节运动特性的精准建模。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/024_Table_10.jpg]]
*Table 10: The Learned Noise Scale per Joint in different noise settings on Human3.6M*

#### 结构约束的施加时机

表 14 对比了在不同去噪阶段施加骨骼长度约束的效果：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/030_Table_14.jpg]]
*Table 14: Comparison with Late-Stage Constraints*

| 约束时机 | Stretch ↓ | ADE ↓ | FDE ↓ | FID ↓ |
|----------|-----------|-------|-------|-------|
| 仅最终步 | — | — | — | — |
| 后 20% 步 (t<0.2) | 3.7 | 0.335 | 0.453 | 0.092 |
| 后 30% 步 (t<0.3) | 3.4 | 0.334 | 0.452 | 0.089 |
| **所有步** | **2.4** | **0.331** | **0.449** | **0.083** |

在所有去噪步上施加约束使骨骼拉伸值降至 2.4，显著优于仅在后期施加约束的方案（3.7/3.4）。这表明早期去噪阶段的骨骼约束对防止误差累积至关重要。

#### 物理真实性指标

表 5 的物理真实性对比显示：
- KinemaDiff 的**肢体拉伸**（Limb Stretch）为 2.42，远低于 **SkeletonDiffusion**（Curreli et al., CVPR 2025）的 3.90。
- 额外引入**帧间骨骼长度抖动损失**（Jitter Loss）可将肢体抖动从 0.45 降至 0.28，且不损害主要指标。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/012_Table_5.jpg]]
*Table 5: Comparison of physical realism metrics on Human3.6M*

---

### 定性分析

图 9 展示了不同去噪步的输出演变过程。即使在早期去噪阶段（第 1-3 步），模型已能生成大致合理的姿态；随着去噪推进至第 10 步，预测结果逐步收敛至与真值高度一致的运动序列。这一渐进改善的特性验证了结构对齐正则化在每一步中持续约束骨骼长度的有效性。

---

### 局限性与注意事项

1. **多样性-真实度权衡**：KinemaDiff 的 APD（6.912）低于不强调物理约束的方法（如 MotionDiff 的 15.353）。作者认为这是可接受的取舍，因为高多样性方法常伴随大量物理不合理样本。
2. **验证场景有限**：当前仅在 Human3.6M（室内受控环境）和 AMASS（多数据集汇集）上验证，尚未在极端遮挡或多人交互等复杂场景中评估。
3. **扩散步数敏感**：图 4 的消融显示模型在 10 步时达到最佳性能，步数过少或过多均会导致指标下降，表明该配置需针对具体场景调优。

### 补充图表

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/013_Table_6.jpg]]
*Table 6: Effect of different loss functions in Structure-Aligned Regularizer*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/021_Table_7.jpg]]
*Table 7: Evaluation metrics used for motion prediction*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_uxTQeKAUh5/figures/023_Table_9.jpg]]
*Table 9: Comparison with Standard Bone-Length Constraints*



## 定位与知识库关联

### 1. 在扩散式人体运动预测谱系中的位置

人体运动预测的生成范式经历了从 GAN、VAE 到扩散模型的演进。KinemaDiff 处于扩散式方法的第三波——**在扩散过程内部嵌入运动学先验**，而非将其作为后处理或外部约束。

**第一波：标准扩散框架的直接迁移。** **MotionDiff**（Wei et al., AAAI 2023）建立了二阶段扩散运动预测的经典范式，但使用均匀高斯噪声且未显式建模骨骼结构。**HumanMAC**（Chen et al., ICCV 2023）通过掩码补全简化训练流程，同样缺乏结构约束。这些方法的共同瓶颈在于：扩散过程对 22–25 个关节施加完全相同的噪声扰动，忽视了腕关节与髋关节在运动学自由度上的本质差异。

**第二波：物理一致性作为后处理。** **BeLFusion**（Barquero et al., ICCV 2023）在 VAE 潜在空间中进行扩散，通过行为编码器提升语义控制，但其物理一致性检验发生在生成完成后，无法阻止去噪过程中骨骼变形的累积。这种“先生成、后校正”的策略意味着中间步骤的解剖学误差会传播到最终输出。

**第三波：扩散过程内部的结构嵌入。** **CoMusion**（Sun & Chowdhary, ECCV 2024）在 DCT 空间使用 GCN 捕获时空依赖，是 KinemaDiff 的直接基线，但未改进扩散过程本身的噪声特性。**SkeletonDiffusion**（Curreli et al., CVPR 2025）首次引入基于静态骨架树的各向异性噪声，然而其噪声特性是固定的，不随具体运动样本或关节历史轨迹自适应调整。

KinemaDiff 的关键跃迁在于同时解决两个因果旋钮——**噪声注入的异质性**与**结构约束的时序一致性**。联合自适应噪声生成器使每个关节的噪声方差成为其索引和历史轨迹的函数 $s_j = f_\theta(j, \mathbf{x}_j^{(1:H)})$，而结构对齐正则化器在每一步去噪中强制预测骨骼长度与历史观测的平均骨骼长度一致。这两个模块的协同作用构成了该方法在谱系中的独特位置：**扩散过程本身被重塑为运动学感知的生成管道**。

### 2. 适用边界与限制条件

**骨骼拓扑的固定性。** 结构对齐正则化器依赖于预定义的骨骼边集 $\mathcal{E}$ 和历史观测的平均骨骼长度 $\bar{b}_{\mathrm{obs}}^{(i,j)}$。这意味着该方法假设：
- 骨骼拓扑在训练和推理阶段保持不变；
- 目标人物的骨骼比例与训练数据统计一致。

在跨骨骼拓扑场景（如不同角色、带道具交互）中，该约束需要重新设计。论文明确将“扩展到可变骨骼拓扑”列为开放问题。

**多样性-真实性的权衡。** 消融实验（Table 3）揭示了一个结构性取舍：仅保留初始编码器（无关节噪声、无结构对齐）时，APD 高达 14.176，但 ADE/FDE/FID 均显著恶化；加入全部模块后，APD 降至 6.912，但所有准确性指标达到最优。与不考虑物理约束的方法（如 MotionDiff 的 APD 15.353）相比，KinemaDiff 的生成多样性有所降低。作者将此定性为“可控的取舍”——所有生成样本保持在解剖可行域内，真实度远高于基线（§A.10）。这一特性使得该方法更适用于对物理合理性要求严格的场景（如运动预测、生物力学分析），而在需要极端多样性的创意生成任务中可能受限。

**数据分布依赖。** 验证仅在 Human3.6M（室内受控环境、7 名受试者、15 种动作类别）和 AMASS（多数据集汇集）上进行。尚未在极端遮挡、多人交互、或野外场景中评估。结构对齐正则化器依赖历史观测来估计骨骼长度，当观测帧数不足或存在严重遮挡时，估计的可靠性会下降。

**扩散步数的敏感性。** 消融实验（Fig. 4）表明，模型在 10 步扩散时达到最优性能，步数过少或过多均导致指标下降。这意味着实际部署时需要针对具体场景调整扩散步数，而非简单地增加步数就能提升质量。

### 3. 局限与开放问题

**已确认的局限：**

1. **多样性上限受物理约束限制。** APD 6.912 低于部分不考虑物理约束的方法，这是高真实度与高多样性之间的内在权衡，而非工程缺陷。

2. **跨数据集泛化的未验证维度。** 尽管在 AMASS 上展示了跨数据集能力，但 AMASS 本身是多数据集的汇集，仍以受控动捕数据为主。在 in-the-wild 视频估计的 3D 姿态序列上的表现未知。

3. **计算开销的结构性约束。** 结构对齐正则化器需要在每个去噪步计算频率特异性 GCN 和骨骼长度对齐损失，这增加了推理成本。论文未报告与标准扩散模型的推理时间对比。

**开放问题：**

1. **可变骨骼拓扑的扩展。** 论文明确提出的第一个开放问题：结构对齐的思想能否泛化到不同角色或带道具的交互场景？这需要将固定的骨骼边集 $\mathcal{E}$ 替换为可学习的或条件化的图结构。

2. **多样性-物理一致性的帕累托前沿。** 如何在保持解剖约束的前提下，扩大生成样本的覆盖范围以包含更长尾的运动模式？可能的路径包括：在结构对齐损失中引入自适应权重、使用层次化噪声调度、或在潜在空间中施加物理约束而非直接在关节空间操作。

3. **多模态条件与物理约束的融合。** 当前方法仅以历史运动为条件。当引入文本、音频等额外模态时，结构对齐正则化器如何与跨模态信号协同工作，是一个未探索的方向。

4. **物理合理性指标的标准化。** 论文使用了骨骼拉伸（Limb Stretch）和骨骼抖动（Limb Jitter）作为物理合理性指标，但这些指标尚未成为社区标准。建立统一的物理合理性评估体系，对于推动该方向的发展具有方法论意义。



## 原文 PDF

![[paperPDFs/ICLR_2026/KinemaDiff_Towards_Diffusion_for_Coherent_and_Physically_Plausible_Human_Motion_Prediction.pdf]]

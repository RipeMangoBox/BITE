---
title: "Zero-shot Human Pose Estimation using Diffusion-based Inverse solvers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Zero_shot_Human_Pose_Estimation_using_Diffusion_based_Inverse_solvers.pdf
project_link: null
code_link: null
openreview_forum_id: Bs4FbnrE82
aliases:
- ZSHPEUDBIS
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "将姿态估计转化为逆问题，通过贝叶斯规则将条件得分分解为尺度无关的旋转先验和尺度相关的位置似然。仅用旋转训练扩散模型作为先验，推理时利用位置测量计算似然梯度进行引导，无需针对新用户微调即可适应不同体形。"
primary_logic: "利用位置测量作为伪逆引导而非直接条件输入，使得扩散模型的先验知识与特定用户的尺度信息解耦，从而实现零样本泛化。"
claims:
- "InPose在身体形状缩放（0.6-1.4倍）时，MPJPE（按缩放归一化）和MPJRE几乎保持恒定，而基线方法误差显著增大。"
- "InPose对位置测量噪声具有鲁棒性：增加高斯噪声时MPJPE几乎不变，而基线方法S有（如BoDiffusion）明显退化。"
- "在上半身骨骼长度非均匀缩放（如手臂×1.4、躯干×0.7）时，InPose的MPJPE和UPE低于所有基线方法。"
- "定理1证明：在良好训练的分数模型下，通过非线性映射D(·)后的旋转矩阵分布可近似为高斯分布，从而使得基于ΠGDM的似然引导可行。"
---

# Zero-shot Human Pose Estimation using Diffusion-based Inverse solvers

> [!tip] 核心洞察
> 利用位置测量作为伪逆引导而非直接条件输入，使得扩散模型的先验知识与特定用户的尺度信息解耦，从而实现零样本泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于扩散逆求解器的零样本人体姿态估计 |
| 英文题名 | Zero-shot Human Pose Estimation using Diffusion-based Inverse solvers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Bs4FbnrE82) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | InPose |
| Dataset | AMASS (Protocol 1, Upper body ×0.7), Arms ×1.4), default shape) |

> [!tip] 效果简介
> - AMASS (Protocol 1, Upper body ×0.7) 上，MPJPE (cm) 为 6.67，对比 7.44 (BoDiffusion(Global))，变化 -0.77。
> - AMASS (Protocol 1, Arms ×1.4) 上，MPJPE (cm) 为 8.25，对比 9.51 (BoDiffusion(Global))，变化 -1.26。
> - AMASS (Protocol 1, default shape) 上，MPJPE under increasing location noise 为 几乎不变（~7.6 → ~7.8），对比 BoDiffusion(Global) 从 ~6.0 显著上升，变化 N/A。

## 概要

### 问题瓶颈

基于可穿戴传感器的人体姿态估计面临一个关键瓶颈：**体形泛化**。现有条件扩散模型（如BoDiffusion）同时依赖惯性测量单元（IMU）提供的关节旋转和位置信息进行姿态预测。由于位置测量与用户体形（骨骼长度）强耦合，模型在训练数据中习得的体形分布限制了其泛化能力——当遇到训练集中未见过的体形时，性能会大幅下降。这一“尺度依赖”问题使得传统方法要么需要覆盖多体形的联合训练数据，要么需要针对新用户进行微调，难以实现真正的零样本部署。

### 核心思路

InPose将姿态估计重新构建为一个**逆问题**，核心洞察在于将姿态分解为尺度无关的旋转先验与尺度相关的位置似然，并通过贝叶斯规则实现两者的解耦：

- **训练阶段**：扩散模型仅以旋转测量 $r_m$ 作为条件输入，学习与体形无关的姿态先验 $p(r_M | r_m)$。
- **推理阶段**：利用位置测量 $l_m$ 计算似然梯度 $\nabla_{r_M^t} \log p_t(l_m | r_M^t)$，作为“伪逆引导”信号修正去噪过程，而体形参数仅出现在似然计算中，无需参与扩散模型的训练。

这一设计的因果杠杆在于：**将位置测量从条件输入降级为引导信号**，使得扩散先验与用户体形彻底解耦。新用户只需提供其骨骼长度参数，即可在不进行任何微调的情况下完成姿态估计。

### 方法定位

InPose属于**基于扩散模型的逆求解器**，在方法谱系中处于条件扩散模型与物理引导的交叉点。与BoDiffusion（Castillo et al., 2023）等使用分类器自由引导（CFG）直接条件化的方法不同，InPose仅将CFG用于旋转先验，而将位置信息通过ΠGDM（Pseudoinverse-Guided Diffusion Models）框架引入。该方法继承了扩散模型的多模态表达能力，同时通过逆问题公式获得了对体形变化的零样本鲁棒性。

### 主要结果

在AMASS数据集上的实验验证了InPose的零样本泛化能力：

- **体形缩放鲁棒性**：当身体形状在0.6–1.4倍范围内均匀缩放时，InPose的归一化位置误差（MPJPE/Scale）和旋转误差（MPJRE）几乎保持恒定，而基线方法（AvatarJLM、BoDiffusion）的误差随缩放程度显著增大（Fig. 3a, b）。
- **非均匀缩放优势**：在上半身骨骼长度非均匀缩放场景（如手臂×1.4、躯干×0.7）下，InPose的上体位置误差UPE达到2.42 cm，优于所有基线方法（Table 1, Protocol 1）。
- **测量噪声鲁棒性**：当位置测量叠加高斯噪声时，InPose的MPJPE几乎不变（~7.6 → ~7.8 cm），而BoDiffusion(Global)的误差从~6.0 cm显著上升（Fig. 3c）。
- **默认体形下的权衡**：在默认体形下，InPose的位置误差略高于BoDiffusion(Global)（7.64 cm vs. 5.97 cm），其优势主要体现在体形变化场景——这是方法设计取舍的直接体现。

### 局限与开放问题

InPose假设用户的骨骼长度参数预先已知，对骨长估计误差较为敏感——当骨长噪声超过1 cm时性能即出现明显退化（Fig. 8）。此外，下体运动估计完全依赖先验推断，在缺少头部平移信息时可能发生灾难性失败（Fig. 12）。未来方向包括：将根平移直接纳入逆引导框架、设计无需显式骨长校准的自动推理机制，以及提升下体运动估计的精度。



人体姿态估计是计算机视觉与可穿戴计算领域的核心问题，其目标是从稀疏传感器测量中恢复完整的三维人体骨架运动。近年来，基于扩散模型的条件生成方法在该任务上取得了显著进展，其中**BoDiffusion**（Castillo et al., 2023）等代表性工作利用分类器自由引导（CFG），同时以关节旋转和位置测量作为条件输入，直接预测全身姿态。

然而，现有条件扩散模型面临一个关键瓶颈：**位置测量与用户体形之间存在不可解耦的耦合关系**。具体而言，关节位置不仅取决于姿态本身，还受用户骨骼长度（即体形参数）的显著影响。当训练数据中体形分布有限时，模型学习到的从位置到姿态的映射将过度依赖训练集中的体形特征，导致在未见过的体形上性能大幅退化。如图1所示，InPose的输入包括三个端点的旋转与位置测量，而输出为完整的全身姿态序列——这一问题的核心挑战在于，如何在体形变化时依然保持估计的准确性与鲁棒性。

本文将姿态估计重新形式化为一个**逆问题**：利用贝叶斯规则将条件得分分解为尺度无关的旋转先验与尺度相关的位置似然。其核心洞察在于：**扩散模型仅需从旋转测量中学习姿态先验，而位置测量则作为伪逆引导信号，在推理阶段通过似然梯度修正去噪过程**。这种解耦设计使得先验知识与用户特定的尺度信息分离，从而无需针对新用户微调即可实现零样本泛化。



## 核心方法与创新机理

InPose 的核心创新在于将**条件扩散模型**的输入解耦为尺度无关的旋转先验与尺度相关的位置似然，从而在不针对新用户体形进行任何微调的前提下实现零样本泛化。

### 瓶颈分析：条件耦合导致的泛化失效

现有基于条件扩散的姿态估计方法（如 **BoDiffusion** (Castillo et al., 2023)）采用分类器自由引导（CFG），同时将旋转测量 $r_m$ 和位置测量 $l_m$ 作为条件输入。这一设计的根本缺陷在于：位置测量受用户体形（骨长 $b_{j,p_j}$）的直接影响，因此训练数据中的体形分布会内嵌到模型的条件依赖中。当测试用户的体形偏离训练分布时——例如手臂长度缩放至 1.4 倍或躯干缩放至 0.7 倍——模型的姿态预测精度会大幅退化（见 Fig. 3a,b）。换言之，**位置-旋转耦合条件**构成了制约泛化能力的关键瓶颈。

### 因果调节：逆问题公式与贝叶斯分解

InPose 通过将姿态估计重新表述为**逆问题**来切断上述耦合。其核心逻辑基于贝叶斯规则对条件得分进行分解：

$$
\nabla_{r_M^t} \log p_t(r_M^t \mid r_m, l_m) = \underbrace{\nabla_{r_M^t} \log p_t(r_M^t \mid r_m)}_{\text{尺度无关的旋转先验}} + \underbrace{\nabla_{r_M^t} \log p_t(l_m \mid r_M^t)}_{\text{尺度相关的位置似然}}
$$

这一分解将条件得分拆分为两个独立可操作的部分：
- **旋转先验项**仅依赖旋转测量 $r_m$，与用户体形完全无关，可通过 CFG 扩散模型在标准数据集上预训练获得。
- **位置似然项**利用已知的用户骨长参数，通过前向运动学（Eq. 1）将去噪后的旋转估计 $\hat{r}_M^t$ 映射为预测关节位置，并与实际位置测量 $l_m$ 比较以计算引导梯度。

### Changed Slots：从联合条件到伪逆引导

与基线方法相比，InPose 在两个关键设计槽位上做出了根本性改变：

| 设计槽位 | 基线方法（BoDiffusion） | InPose |
|---------|----------------------|--------|
| **CFG 条件输入** | 同时接受 $r_m$ 和 $l_m$ 作为条件，模型直接学习从测量到姿态的映射 | 仅接受 $r_m$ 作为条件，学习尺度无关的姿态先验 |
| **位置测量使用方式** | 作为条件信号嵌入扩散过程 | 作为**伪逆引导**信号，在推理时通过 $\Pi$GDM 似然梯度 $g$ 修正去噪方向 |

这一改变的实质是：位置测量从"条件输入"降级为"引导信号"。CFG 分数模型 $\epsilon_\theta(r_M^t, t, r_m)$ 仅基于旋转测量提供姿态先验估计 $\hat{r}_M^t$（通过 Tweedie 公式，Eq. 4），而位置似然梯度 $g$（Eq. 9）则在每个去噪步骤中作为修正项加入后验更新：

$$
r_M \leftarrow \sqrt{\bar{\alpha}_s} \hat{r}_M^t + c_1 \epsilon + c_2 \epsilon_t + \sqrt{\bar{\alpha}_t} g
$$

这种设计的核心优势在于：扩散先验与特定用户的体形参数完全解耦，推理时仅需将用户的骨长信息注入似然计算即可适应任意体形，无需重新训练或微调。

### 理论支撑：定理 1 的高斯近似

似然引导的可行性依赖于 **定理 1**（置信度 0.95）：在良好训练的分数模型下，通过非线性映射 $\mathcal{D}(\cdot)$ 后的旋转矩阵分布可近似为高斯分布 $\mathcal{N}(\mathcal{D}(\hat{r}_M^t), w_t^2 \Sigma_{\hat{r}_M^t})$。这使得 $\Pi$GDM 框架下的似然梯度计算具有闭式解（Eq. 9），为位置测量的伪逆引导提供了严格的理论基础。

### 零样本泛化的机制本质

InPose 的零样本能力并非来自更大规模的体形数据训练，而是源于**公式层面的结构解耦**：将体形参数 $b_{j,p_j}$ 从先验学习中移除，仅在推理阶段作为已知量参与似然计算。这一设计使得模型在体形均匀缩放（0.6-1.4 倍）和非均匀缩放（如手臂 ×1.4、躯干 ×0.7）下均能保持稳定的 MPJPE 和 MPJRE（Fig. 3a,b, Table 1），而基线方法在偏离默认体形时误差显著增大。



![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Bs4FbnrE82/figures/002_Figure_2.jpg]]
*Figure 2: InPose pipeline: 3-point sensor rotation + location measurements are inputs. Rotations are fed to the CFG score model, which outputs a conditional prior; location measurements estimate the likelihood, which is used to steer diffusion*

InPose将人体姿态估计重新形式化为一个逆问题，其核心思想是将姿态分解为尺度无关的旋转先验与尺度相关的位置似然，并通过扩散模型实现两者的解耦融合。整体流程如Figure 2所示，包含三个关键阶段：**条件先验估计**、**似然梯度计算**和**后验更新**。

**输入与输出**：系统接收来自三点传感器的旋转测量 $r_m$ 和位置测量 $l_m$ 作为输入，输出全局关节旋转序列 $r_M$，进而通过前向运动学恢复完整的人体姿态。

**Pipeline模块关系**：

1. **CFG分数模型 $\epsilon_\theta$**：作为尺度无关的姿态先验，该模型仅在旋转测量 $r_m$ 的条件下进行训练。在推理时，它接收当前噪声样本 $r_M^t$、时间步 $t$ 和测量旋转 $r_m$，输出条件分数估计。这是InPose与现有方法的核心差异——**BoDiffusion**（Castillo et al., 2023）同时使用位置和旋转作为CFG条件，而InPose仅使用旋转，将位置测量从条件输入转化为伪逆引导信号。

2. **Tweedie去噪估计**：利用CFG分数模型的输出，通过Tweedie公式计算当前时间步的条件去噪旋转估计 $\hat{r}_M^t$：
   $$\hat{r}_M^t = \frac{r_M^t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(r_M^t, t, r_m)}{\sqrt{\bar{\alpha}_t}}$$
   该估计作为后续似然计算的桥梁，将扩散过程中的噪声样本映射回干净的旋转空间。

3. **似然分数计算**：基于位置测量 $l_m$ 和去噪估计 $\hat{r}_M^t$，通过$\Pi$GDM框架计算似然梯度 $g$。该模块利用前向运动学算子 $\mathcal{D}(\cdot)$ 将旋转映射为关节位置，并计算位置残差与雅可比矩阵，最终得到似然梯度：
   $$g = \left((l_m - \mathcal{A} \cdot \mathcal{D}(\hat{r}_M^t))^\top (w_t^2 \mathcal{A} \Sigma_{\hat{r}_M^t} \mathcal{A}^\top + \sigma_l^2 \mathrm{I})^{-1} \mathcal{A} \frac{\partial \mathcal{D}(\hat{r}_M^t)}{\partial r_M^t}\right)^\top$$
   定理1为这一计算提供了理论支撑：在良好训练的分数模型下，$\mathcal{D}(r_M^0)$ 关于 $r_M^t$ 的条件分布可近似为高斯分布，使得基于$\Pi$GDM的似然引导可行。

4. **后验更新（修改的DDIM步骤）**：将条件先验估计 $\hat{r}_M^t$、随机噪声和似然梯度 $g$ 组合，通过修改的DDIM步骤生成下一时间步的样本：
   $$r_M \leftarrow \sqrt{\bar{\alpha}_s} \hat{r}_M^t + c_1 \epsilon + c_2 \epsilon_t + \sqrt{\bar{\alpha}_t} g$$
   这一更新机制使得扩散过程同时受到尺度无关的运动先验和特定用户的尺度信息的约束。

**数据流总结**：旋转测量驱动CFG先验，提供尺度无关的姿态约束；位置测量通过似然梯度注入尺度相关的修正信号；两者在后验更新中融合，逐步从噪声中恢复与用户体形相适应的姿态序列。这种解耦设计使得InPose无需针对新用户微调即可适应不同体形，实现零样本泛化。



### 问题形式化

InPose将姿态估计建模为逆问题：给定来自三点传感器的旋转测量 $r_m$ 和位置测量 $l_m$，目标是从后验分布 $p(r_M \mid \{l_m, r_m\})$ 中采样全局关节旋转序列 $r_M$。通过贝叶斯规则，条件得分函数被分解为两项：

$$\nabla_{r_M^t} \log p_t(r_M^t \mid r_m) + \nabla_{r_M^t} \log p_t(l_m \mid r_M^t)$$

第一项是**尺度无关的旋转先验**，仅以旋转测量 $r_m$ 为条件；第二项是**尺度相关的位置似然**，利用位置测量 $l_m$ 计算引导梯度。这一分解是InPose实现零样本泛化的核心——扩散先验与用户体形解耦，位置测量仅作为推理时的伪逆引导信号。

### 关键模块

**CFG分数模型 $\epsilon_\theta$**：基于分类器自由引导（Classifier-Free Guidance）的条件扩散模型，仅接受旋转测量 $r_m$ 作为条件输入，学习尺度无关的姿态先验。该模型在AMASS数据集上训练，以噪声旋转序列 $r_M^t$、时间步 $t$ 和测量旋转 $r_m$ 为输入，输出噪声估计。

**Tweedie去噪估计**：利用当前噪声样本和CFG分数模型的输出，计算去噪后的旋转估计：

$$\hat{r}_M^t = \frac{r_M^t - \sqrt{1 - \bar{\alpha}_t} \, \epsilon_\theta(r_M^t, t, r_m)}{\sqrt{\bar{\alpha}_t}}$$

其中 $\bar{\alpha}_t$ 是扩散过程的累积噪声调度参数。该估计作为似然计算的中间变量。

**似然梯度计算**：基于 $\Pi$GDM框架，位置似然的梯度通过测量残差和雅可比矩阵计算。核心假设来自**定理1**：在良好训练的分数模型下，经非线性映射 $\mathcal{D}(\cdot)$ 后的旋转矩阵分布可近似为高斯分布：

$$p_t(\mathcal{D}(r_M^0) \mid r_M^t) \approx \mathcal{N}(\mathcal{D}(\hat{r}_M^t), w_t^2 \Sigma_{\hat{r}_M^t})$$

基于此，似然梯度 $g$ 的闭合形式为：

$$g = \left((l_m - \mathcal{A} \cdot \mathcal{D}(\hat{r}_M^t))^\top (w_t^2 \mathcal{A} \Sigma_{\hat{r}_M^t} \mathcal{A}^\top + \sigma_l^2 \mathrm{I})^{-1} \mathcal{A} \frac{\partial \mathcal{D}(\hat{r}_M^t)}{\partial r_M^t}\right)^\top$$

其中 $\mathcal{A}$ 是位置测量的线性选择矩阵，$\mathcal{D}(\cdot)$ 是通过前向运动学将旋转映射到关节位置的函数，$\Sigma_{\hat{r}_M^t}$ 是去噪估计的协方差，$\sigma_l^2$ 是位置测量噪声方差。该梯度作为修正信号，将扩散过程引导至与位置测量一致的方向。

**后验更新（修改的DDIM）**：将先验估计、随机噪声和似然梯度组合，逐步更新姿态样本：

$$r_M \leftarrow \sqrt{\bar{\alpha}_s} \, \hat{r}_M^t + c_1 \epsilon + c_2 \epsilon_t + \sqrt{\bar{\alpha}_t} \, g$$

其中 $\epsilon$ 和 $\epsilon_t$ 是随机噪声项，$c_1$、$c_2$ 为DDIM调度系数。完整的推理流程见Algorithm 1。

### 平移处理

为处理根关节平移 $l_1(i) \neq 0$ 的情况，InPose利用三点位置测量之间的差值来消除根平移的影响。前向运动学链可表达为：

$$l_j(i) = \sum_{k=3}^j (l_{p_k}(i) + R_{p_k}(i) \cdot b_{k,p_k}) + R_1(i) \cdot b_{2,1} + l_1(i)$$

通过取位置测量间的差分，根平移项 $l_1(i)$ 被抵消，使得线性逆引导公式在动态平移场景下仍可应用。

### 表示选择

消融实验（Figure 5）验证了6D旋转表示相对于原始 $3\times3$ 旋转矩阵的优势：6D表示能显著降低输出姿态的抖动（Jitter）。6D表示通过提取旋转矩阵的前两列构建：

$$r_j(i) = [R_j^{(1,1)}(i) \; R_j^{(2,1)}(i) \; R_j^{(3,1)}(i) \; R_j^{(1,2)}(i) \; R_j^{(2,2)}(i) \; R_j^{(3,2)}(i)]^\top$$

这一表示更适合神经网络训练，且通过Gram-Schmidt正交化可恢复完整的旋转矩阵。



## 实验与关键发现

### 核心实验设置

所有实验在AMASS数据集上完成，遵循与基线方法相同的训练/测试协议。测试集采用Transitions和HumanEVA子集，训练集使用CMU、BMLrub、HDM05按90/10划分。评估指标包括平均关节位置误差（MPJPE，cm）、平均关节旋转误差（MPJRE，度）、上半身位置误差（UPE，cm）和下半身位置误差（LPE，cm）。基线方法包括传统神经网络方法**AvatarJLM**（Zheng et al., 2023）以及两种基于分类器自由引导（CFG）的扩散模型变体：**BoDiffusion(Local)**（Castillo et al., 2023）输出局部关节角度，**BoDiffusion(Global)**输出全局关节角度，二者均同时使用位置和旋转测量作为CFG条件输入。

实验设计围绕零样本泛化的核心瓶颈展开：现有条件扩散模型同时依赖位置和旋转测量，而位置测量受用户体形影响，训练数据中的体形分布限制了模型在未见体形上的泛化能力。为验证InPose通过逆问题公式化将体形参数作为已知量用于似然计算、使扩散先验与体形解耦的有效性，实验涵盖均匀缩放、非均匀缩放（如手臂、躯干独立缩放）等多种体形变化场景。

### 零样本泛化：体形缩放鲁棒性

图3(a,b)展示了InPose与基线方法在身体形状均匀缩放（0.6-1.4倍）下的性能对比。InPose的MPJPE（按缩放归一化）和MPJRE几乎保持恒定，而基线方法（BoDiffusion(Local)、BoDiffusion(Global)、AvatarJLM）在偏离默认体形（缩放因子1.0）时误差显著增大，呈现典型的V形曲线。这一结果表明，InPose成功解耦了尺度无关的姿态先验与尺度相关的位置信息，验证了核心因果机制的有效性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Bs4FbnrE82/figures/005_Figure_3.jpg]]
*Figure 3: (a) Position error vs. body shape scaling. (b) Rotation error vs. body scale. (c) Position error vs. location noise. All these tests were performed using Protocol 1*

在上半身骨骼长度非均匀缩放的极端场景下（Table 1, Protocol 2），InPose展现出系统性优势。当手臂缩放至1.4倍、躯干缩放至0.7倍时，InPose的MPJPE为8.25 cm，优于BoDiffusion(Global)的9.51 cm（Δ=-1.26 cm）；当上半身整体缩放至0.7倍时，InPose的MPJPE为6.67 cm，优于BoDiffusion(Global)的7.44 cm（Δ=-0.77 cm）。在旋转误差MPJRE和上半身位置误差UPE上，InPose同样全面领先。值得注意的是，在默认体形下，InPose的位置误差略高于BoDiffusion(Global)（约7.64 cm vs ~6.0 cm），其优势主要体现在体形变化场景——这正是该方法设计的核心目标。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Bs4FbnrE82/figures/007_Table_1.jpg]]
*Table 1: Algorithm comparison for varying upper body shape. The metrics used are Mean Joint Position Error(MPJPE) in cm, Mean Joint Rotation Error(MPJRE) in degrees, Upper Joint Position Error(UPE) in cm, and Lower Joint Position Error(LPE) in cm. The lower body shape was kept the same, while the upper body bone lengths were scaled. (a) Results with Upper body shape variation (Protocol 1) (↓ is better)*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Bs4FbnrE82/figures/009_Table_2.jpg]]
*Table 2: Algorithm comparison for varying upper body shape using Protocol 1. InPose (head) augments InPose by using the head translation input for CFG. The Shape variation in this table is less extreme than in Table 1*

图4的定性对比进一步揭示了BoDiffusion在非默认体形下的典型失败模式：由于位置条件与训练数据中的体形分布不匹配，BoDiffusion的下体预测出现明显偏差，而InPose利用尺度无关的旋转先验保持了合理的姿态估计。

### 测量噪声鲁棒性

InPose对位置测量噪声展现出显著鲁棒性（图3c）。当向位置测量添加递增的高斯噪声时，InPose的MPJPE几乎保持不变（从约7.6 cm微增至约7.8 cm），而BoDiffusion(Global)的误差从约6.0 cm显著上升。这一差异源于两种方法对位置信息的使用方式：BoDiffusion将位置直接作为条件输入，噪声直接污染了条件信号；InPose将位置用于ΠGDM似然梯度计算，通过协方差加权机制（Eq. 9中的$(w_t^2 \mathcal{A} \Sigma_{\hat{r}_M^t} \mathcal{A}^\top + \sigma_l^2 \mathrm{I})^{-1}$项）自然抑制了噪声的影响。

在旋转测量噪声方面（图9），InPose同样保持最低且最稳定的旋转误差（约6.3-7.1°），优于BoDiffusion(Local)和BoDiffusion(Global)，表明旋转先验在输入扰动下具有良好的稳定性。

### 消融实验

**位置引导的必要性**（Table 4）：当完全移除位置引导、仅使用旋转先验时，InPose的MPJPE从7.64 cm急剧恶化至15.98 cm，验证了位置似然梯度在修正姿态估计中的关键作用。这一结果也说明，纯CFG模型（BoDiffusion(Global)去除位置条件）与InPose的核心区别不在于网络架构，而在于位置信息的使用方式——作为伪逆引导而非直接条件输入。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Bs4FbnrE82/figures/019_Table_4.jpg]]
*Table 4: Comparison between InPose, BoDiffusion(Global) and BoDiffusion(Global) with no l _ { m } as input for CFG using Protocol 1*

**6D旋转表示**（图5）：采用6D旋转表示相比原始3×3旋转矩阵能显著降低输出姿态的抖动（Jitter指标），为扩散模型在旋转空间中的训练提供了更稳定的参数化方案。

**头部平移增强**（Table 2）：将头部平移作为CFG额外输入（InPose (head)）能够在所有评估指标上进一步提升性能。在较温和的体形变化场景（Protocol 1）下，InPose (head)几乎在所有指标上超越所有基线方法。这一增强有效缓解了InPose在缺少根平移信息时对下体运动推断的不足。

**局部vs全局逆引导**（Table 5）：基于局部关节角度的逆引导（Local(Gradient Descent)）在下体误差LPE上表现更优，但上体误差UPE和角度误差MPJRE更高。InPose在全局角度空间中进行逆引导，实现了上下体误差的更好平衡。

**协方差简化**：设置ΠGDM中的协方差矩阵为单位阵即可获得合理性能，大幅降低计算开销，在实际部署中具有重要的工程意义。

### 失败模式与局限性

**下体运动估计不足**：InPose的下体运动估计精度有限，尤其在缺少直接位置引导时完全依赖旋转先验。图12展示了灾难性失败案例：当用户极度接近地面时，若未提供头部平移信息，InPose无法推断下体运动。InPose (head)通过将头部平移纳入CFG条件可部分缓解此问题，但根本原因在于根平移未直接纳入逆引导框架。

**骨长估计敏感性**：方法假设用户的骨长参数预先已知且准确。图8显示，InPose对骨长估计误差较为敏感：当关节长度噪声标准差超过1 cm时，MPJPE和MPJRE均呈线性增长趋势（噪声10 cm时MPJPE约15.5 cm，MPJRE约9°）。这一敏感性源于位置似然计算（Eq. 9）中测量矩阵$\mathcal{A}$对骨长参数的依赖，骨长偏差直接导致位置残差$l_m - \mathcal{A} \cdot \mathcal{D}(\hat{r}_M^t)$的系统性偏移。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_Bs4FbnrE82/figures/016_Figure_8.jpg]]
*Figure 8: Performance with joint length error. The left axis is the MPJPE, and the right axis is the MPJRE*

**默认体形性能略低**：在默认体形下，InPose的位置误差略高于专门的CFG基线（如BoDiffusion），这是将位置从条件输入转为引导信号的固有代价——引导信号的修正能力弱于直接条件。

**理论假设限制**：定理1的高斯近似依赖根关节静止的简化假设，动态平移场景下的建模精度有待改进。

### 计算效率

Table 6显示，InPose的处理速度约为229样本/秒，介于BoDiffusion（约392样本/秒）和AvatarJLM（约102样本/秒）之间。ΠGDM逆引导引入的额外计算开销主要来自似然梯度计算中的雅可比矩阵$\frac{\partial \mathcal{D}(\hat{r}_M^t)}{\partial r_M^t}$和矩阵求逆操作，但在协方差简化为单位阵的配置下，这一开销可控制在可接受范围内。



## 定位与知识库关联

InPose 的核心贡献在于将人体姿态估计重新构造为一个逆问题，通过贝叶斯分解将尺度无关的旋转先验与尺度相关的位置似然解耦。这一设计使其在方法谱系中占据了一个独特位置：它既不同于传统的神经网络回归方法，也区别于直接将位置测量作为扩散模型条件的现有方案。

### 与基线方法的关系

**AvatarJLM** (Zheng et al., 2023) 代表了传统的神经网络姿态估计范式，未使用扩散模型。这类方法通常依赖训练数据中的体形分布，在未见过的体形上泛化能力受限。InPose 通过引入扩散先验和逆引导机制，从根本上改变了这一范式——先验知识与特定用户的体形参数在推理时动态结合，而非在训练时固化。

**BoDiffusion(Local)** (Castillo et al., 2023) 和 **BoDiffusion(Global)** 是 InPose 最直接的对比基线。两者均采用分类器自由引导（CFG）的扩散模型，但同时将旋转测量 $r_m$ 和位置测量 $l_m$ 作为条件输入。这种设计导致模型的条件分布 $p(r_M | r_m, l_m)$ 隐含地编码了训练数据中的体形分布，因为位置测量 $l_m$ 本身受用户体形影响——同一姿态在不同体形下会产生不同的关节位置。当测试用户的体形偏离训练分布时，模型的条件预测会产生系统性偏差。这正是 Fig. 3(a,b) 和 Table 1 中 BoDiffusion 在体形缩放时误差显著增大的根本原因。

InPose 的关键改动在于：CFG 模型仅接受旋转测量 $r_m$ 作为条件，学习尺度无关的先验 $\nabla_{r_M^t} \log p_t(r_M^t | r_m)$；位置测量 $l_m$ 则被重新定位为伪逆引导信号，通过 $\Pi$GDM 似然梯度 $\nabla_{r_M^t} \log p_t(l_m | r_M^t)$ 在推理时引导去噪过程。这一改动使得扩散先验与用户体形彻底解耦，从而实现了零样本泛化。

### 适用边界与局限

InPose 的逆引导框架依赖于几个关键假设，这些假设定义了其适用边界：

**骨长参数的依赖性**是首要局限。似然计算需要已知用户的骨长向量 $b_{j,p_j}$（即身体形状参数），因为前向运动学将旋转映射到关节位置时依赖这些参数。Fig. 8 的敏感性分析显示，骨长估计误差超过 1 cm 即导致 MPJPE 和 MPJRE 显著上升。这意味着在实际部署中，InPose 需要配合准确的骨长校准流程，或依赖外部体形估计模块。这一依赖性在方法设计中被明确承认，但论文未提供自动骨长推理的机制。

**下体运动估计的精度瓶颈**源于信息不对称。在标准的 3 点传感器配置下，位置测量仅来自上半身（头部和双手），下体关节完全依赖旋转先验推断。Table 1 中 InPose 的 LPE（下肢位置误差）在部分体形变化下高于 BoDiffusion(Global)，反映了这一结构性限制。更严重的是，当用户接近地面时（如俯身动作），缺少根平移信息会导致灾难性失败（Fig. 12）。InPose (head) 变体通过将头部平移作为 CFG 额外输入部分缓解了这一问题（Table 2），但并未从根本上解决下体运动建模的不足。

**根关节静止假设**是理论推导中的简化。似然梯度的线性化推导（Theorem 1）假设根关节平移为零或通过差分测量消除，但动态场景中的根平移建模仍有待改进。这一假设限制了方法在包含大幅位移的运动序列上的适用性。

**默认体形下的性能权衡**值得注意。在默认体形（scale=1.0）下，InPose 的 MPJPE 略高于 BoDiffusion(Global)（Table 1 中约 7.64 cm vs. 约 6.0 cm），这表明逆引导框架在训练分布内付出了轻微的精度代价，以换取分布外的泛化能力。这一权衡是方法设计的固有特性：位置测量作为引导信号而非直接条件，使得先验在最终估计中扮演更重要角色，在分布内可能不如直接条件建模精确。

### 开放问题

1. **根平移的统一建模**：当前框架通过差分测量消除根平移，但将根平移直接纳入逆引导的似然计算（而非仅作为 CFG 条件）可能从根本上提升下体运动估计。这需要扩展 Theorem 1 的高斯近似以处理非零均值的平移分量。

2. **无校准骨长推理**：能否将骨长参数 $b_{j,p_j}$ 也作为隐变量纳入扩散采样过程，实现姿态与体形的联合推断？这将消除对外部校准的依赖，显著增强实用性。

3. **下体先验的增强**：当前下体运动完全依赖从上半身旋转中学到的条件先验。引入物理约束（如足部接触一致性）或额外的运动学先验可能缩小 LPE 差距。

4. **计算效率优化**：$\Pi$GDM 似然梯度涉及雅可比矩阵 $\partial \mathcal{D}(\hat{r}_M^t)/\partial r_M^t$ 的计算和协方差矩阵求逆。附录 B 指出将协方差设为单位阵即可获得合理性能，但大批量或在线场景下的进一步加速仍需探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/Zero_shot_Human_Pose_Estimation_using_Diffusion_based_Inverse_solvers.pdf]]

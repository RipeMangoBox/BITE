---
title: "DCM: Dual-Expert Consistency Model for Efficient and High-Quality Video Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/DCM_Dual-Expert_Consistency_Model_for_Efficient_and_High-Quality_Video_Generation.pdf
project_link: null
code_link: "https://github.com/Vchitect/DCM"
aliases:
- DECMD
- DCM
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 将 ODE 轨迹划分为语义合成与细节精修两个阶段，分别训练语义专家（SemE）与细节专家（DetE）去噪器，并通过参数高效手段（冻结语义专家、添加时间步依赖嵌入层与 LoRA）实现解耦，避免优化干扰。
primary_logic: 通过可视化训练动态，发现不同噪声水平对应的学习目标存在根本冲突，因此采用双专家架构分离语义与细节学习，辅以时间一致性损失和 GAN/特征匹配损失进行针对性优化。
claims:
- 图 2(b) 显示蒸馏过程中高、低噪声下损失和梯度范数的显著差异，证实冲突学习的存在。
- 图 3 证明语义专家与细节专家的组合（SemE+DetE）优于单一一致性模型（VCM），验证解耦有效性。
- 表 1 显示 DCM 在 4 步采样下 VBench 总分 83.83，与原始 50 步 HunyuanVideo 相当，且显著优于 LCM (80.33) 和 PCM (80.83)。
- 用户偏好研究（表 2）表明评分者对 DCM 的偏好远高于 LCM 和 PCM（一致超过 72%）。
---

# DCM: Dual-Expert Consistency Model for Efficient and High-Quality Video Generation

> [!tip] 核心洞察
> 通过可视化训练动态，发现不同噪声水平对应的学习目标存在根本冲突，因此采用双专家架构分离语义与细节学习，辅以时间一致性损失和 GAN/特征匹配损失进行针对性优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | DCM：双专家一致性模型用于高效高质量视频生成 |
| 英文题名 | DCM: Dual-Expert Consistency Model for Efficient and High-Quality Video Generation |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2506.03123) · [Code](https://github.com/Vchitect/DCM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Dual-Expert Consistency Model (DCM) |
| Dataset | HunyuanVideo, CogVideoX |

> [!tip] 效果简介
> - HunyuanVideo (VBench) 上，Total Score 83.83 (DCM 4-step) vs 80.33 (LCM 4-step) (+3.50)；Total Score 83.83 (DCM 4-step) vs 80.83 (PCM 4-step) (+3.00)。
> - HunyuanVideo (Latency) 上，Latency (sec.) 121.52 (DCM 4-step) vs 120.68 (LCM 4-step) (+0.84)。
> - CogVideoX (User Study) 上，Rater Preference (DCM vs LCM) 75.33% vs 24.67% (+50.66%)。

## 概述

**问题瓶颈**：在一致性蒸馏过程中，高噪声与低噪声样本之间的损失贡献与梯度范数存在显著差异，导致单一学生模型在同时学习语义布局/运动与细节细化时产生优化冲突，难以收敛到最优解，造成视频时序不一致与细节质量下降。

**核心思路**：将 ODE 轨迹划分为语义合成与细节精修两个阶段，分别训练语义专家（SemE）与细节专家（DetE）去噪器，并通过参数高效手段（冻结语义专家、添加时间步依赖嵌入层与 LoRA）实现解耦，避免优化干扰。

**方法定位**：DCM 属于基于一致性蒸馏的少步视频生成方法，在 LCM、PCM 等一致性模型基础上引入双专家架构与针对性损失设计，以极小的参数增量（仅 DetE 新增的嵌入层与 LoRA）换取显著的质量提升。

**主要结果**：
- 在 HunyuanVideo 的 VBench 基准上，DCM 以 4 步采样取得总分 83.83，与原始 50 步教师模型相当，显著优于 LCM（80.33）和 PCM（80.83）。
- 用户偏好研究中，评分者对 DCM 的偏好一致超过 72%，远高于 LCM 和 PCM。
- 推理延迟与 LCM、PCM 几乎相同（均在 121 秒左右，双 A100 GPU），未引入额外推理开销。

## 背景与动机

### 视频扩散模型的加速困境

扩散模型已成为文本到视频生成的主流范式，其核心在于通过一个常微分方程（ODE）轨迹逐步从纯噪声中恢复出高保真视频。前向过程将干净数据 $\pmb{x}_0$ 逐步加噪至 $\pmb{x}_t$：

$$q(\pmb{x}_t | \pmb{x}_0) = \mathcal{N}(\pmb{x}_t; \sqrt{\alpha_t} \pmb{x}_0, \sqrt{1 - \alpha_t} \pmb{I})$$

去噪网络 $\epsilon_\theta$ 通过预测添加的噪声进行训练：

$$\mathcal{L}_{DM} = \mathbb{E}_{\pmb{x}, \epsilon \sim \mathcal{N}(0,1), t} \left[ || \epsilon - \epsilon_{\theta}(\pmb{x}_t, t) ||_2^2 \right]$$

然而，高质量视频生成通常需要 50 步甚至更多的采样步数，导致推理延迟极高。例如，**HunyuanVideo**（50 步）在双 A100 GPU 上生成 129 帧 1280×720 视频需要数千秒级别的延迟。一致性模型（Consistency Model）通过将整个 ODE 轨迹直接映射到终点，理论上可将采样步数压缩至 4 步甚至更少，为加速推理提供了可能。

### 一致性蒸馏中的冲突学习瓶颈

直接将一致性蒸馏应用于视频扩散模型时，存在一个被忽视的根本性瓶颈。**图 2(b)** 揭示了训练过程中的关键现象：在高噪声水平（采样早期）与低噪声水平（采样后期）下，学生模型的损失值和梯度范数存在显著差异。这意味着单一学生模型被要求同时完成两个性质截然不同的学习任务：

- **高噪声阶段**：需要从几乎完全被噪声淹没的潜变量中重建视频的全局语义布局、物体形状和运动轨迹。
- **低噪声阶段**：需要在语义结构基本确定后，精修纹理细节、边缘锐度和局部真实感。

这两个目标的优化方向存在冲突，单一模型难以同时收敛到最优解。**图 2(a)** 进一步可视化了这一现象：采样早期输出变化剧烈且迅速（语义成形阶段），而采样后期变化趋于平缓（细节精修阶段）。这种冲突直接导致蒸馏后的模型在视频时序一致性和细节质量上出现退化。

### 现有加速方法的不足

现有的一致性蒸馏变体未能有效解决上述冲突：

- **LCM**（Latent Consistency Model）在整个 ODE 轨迹上训练单一学生模型，直接遭受优化冲突，导致 VBench 总分仅为 80.33（4 步），显著低于教师模型。
- **PCM**（Phased Consistency Model）虽然引入了分阶段训练，但各阶段仍独立使用完整模型，未实现语义与细节的架构解耦，VBench 总分仅提升至 80.83。

这些方法在低步数采样下，往往出现运动不连贯、细节模糊或伪影等问题。**图 1**（左）的视觉对比直观展示了这一差距：LCM 和 PCM 生成的视频在细节保真度和运动自然度上明显劣于原始 50 步 HunyuanVideo。

### 本文动机

基于上述观察，本文的核心动机是：**通过架构解耦来消除一致性蒸馏中的优化冲突**。具体而言，将 ODE 轨迹分割为语义合成与细节精修两个阶段，分别训练专门的去噪专家，使每个专家只需专注于单一类型的学习目标。同时，通过参数高效的设计（冻结共享基座、仅添加轻量适配层）来控制额外开销，并辅以针对性损失函数（时间一致性损失、GAN 损失）分别增强两个专家的输出质量。

## 核心创新

DCM 的核心创新在于对一致性蒸馏过程中**优化冲突**的识别与解耦。作者通过可视化训练动态（图 2(b)）发现，高噪声与低噪声样本对应的损失贡献与梯度范数存在显著差异——这导致单一学生模型（VCM）在同时学习语义布局/运动和细节细化时陷入优化冲突，难以收敛到最优解，最终损害视频的时序一致性与细节质量。

基于这一瓶颈，DCM 引入了四个关键改动槽位：

1. **双专家架构（SemE + DetE）**  
   将 ODE 轨迹沿时间步维度分割为高噪声子轨迹（$i=\kappa..N$）与低噪声子轨迹（$j=0..\kappa$），分别由**语义专家 SemE** 和**细节专家 DetE** 负责学习。SemE 在高噪声阶段学习语义布局与运动，DetE 在低噪声阶段专攻细节精修，从根本上避免了单一模型面临的冲突学习问题。图 3 的消融实验直接验证了 SemE+DetE 组合优于 VCM，证明解耦的有效性。

2. **参数高效的专家实现**  
   DetE 并非独立训练的全量模型，而是以冻结的 SemE 为基座，仅添加**时间步依赖嵌入层**与 **LoRA** 适配器进行微调。图 5 的权重差异分析显示，两个专家的权重分布高度接近，表明参数高效方案在几乎不增加参数量和内存开销的前提下实现了功能解耦。消融实验（Table 3）进一步证实，参数高效蒸馏（PE）大幅降低资源需求，同时几乎不影响视觉质量。

3. **针对性的损失函数设计**  
   - 语义专家在一致性损失 $L_{CD}$ 基础上额外引入**时间一致性损失 $L_{TC}$**，通过约束相邻帧间运动关系来增强时序连贯性。  
   - 细节专家则在 $L_{CD}$ 基础上叠加 **GAN 损失**与**特征匹配损失 $L_{FM}$**，利用对抗训练提升细节真实感与训练稳定性。  
   消融实验分别验证了 TC 损失对运动自然度的改善，以及 GAN/特征匹配损失对细节质量的提升。

4. **轨迹分割点 $\kappa$ 的选取**  
   分割边界 $\kappa=37$ 并非随意设定，而是基于相邻时间步 L1 距离分析选定的最优分割点（图 10），确保语义与细节阶段在噪声水平上具有清晰的界限。

这些改动协同作用，使 DCM 在仅 4 步采样下即达到 VBench 总分 83.83，与原始 50 步 HunyuanVideo 相当，且显著优于 LCM（80.33）和 PCM（80.83），同时推理延迟几乎不变（Table 1）。用户偏好研究（Table 2）中评分者对 DCM 的偏好率一致超过 72%，进一步佐证了创新设计的实际收益。

## 整体框架

DCM 的整体训练流程分为两个解耦的阶段：语义学习阶段与细节学习阶段，分别对应 ODE 轨迹上高噪声与低噪声的两个子区间。其核心思想源于对一致性蒸馏训练动态的诊断——图 2(b) 显示，高噪声样本与低噪声样本在损失值和梯度范数上存在显著差异，表明单一学生模型（VCM）在同时学习语义布局/运动与细节细化时面临优化冲突，这是导致收敛困难与生成质量下降的根本瓶颈。

### 阶段一：语义专家训练

在第一阶段，DCM 训练语义专家去噪器 $F_{\mathrm{SemE}}$。该专家仅在高噪声子轨迹 $\{\mathbf{x}_{t_i}\}_{i=\kappa}^{N}$ 上学习，其中 $\kappa=37$ 为通过相邻时间步 L1 距离选定的最优分割边界（见 Section 4.3, Figure 10）。语义专家的学习目标由两部分组成：

- **一致性蒸馏损失** $\mathcal{L}_{\mathrm{CD}}$：使 $F_{\mathrm{SemE}}$ 能够将子轨迹上的任意点直接映射到分割边界 $t_\kappa$ 处的状态，即 $\Phi(\mathbf{x}_{t_m}, F_{\mathrm{SemE}}(\mathbf{x}_{t_m}, t_m, c), t_\kappa)$。
- **时间一致性损失** $\mathcal{L}_{\mathrm{TC}}$：通过约束相邻帧之间位移量的一致性，增强语义专家对运动模式的建模能力。

这一阶段的训练使语义专家专注于捕获视频的全局语义布局和运动结构，而不受低噪声阶段细节优化的干扰。

### 阶段二：细节专家训练

在第二阶段，DCM 以冻结的语义专家权重作为初始化，构建细节专家去噪器 $F_{\mathrm{DetE}}$。为实现参数高效适配，细节专家仅在共享基座上添加两组可训练组件：

- **时间步依赖嵌入层** $\Psi$：为低噪声子轨迹提供专门的时序条件信号。
- **LoRA 适配器** $\Lambda^\dagger$：以低秩分解的形式注入注意力块，参数量远小于完整独立专家。

细节专家在低噪声子轨迹 $\{\mathbf{x}_{t_j}\}_{j=0}^{\kappa}$ 上进行训练，仅更新 $\Psi$ 和 $\Lambda^\dagger$，而基座权重保持冻结。其学习目标包括：

- **一致性蒸馏损失** $\mathcal{L}_{\mathrm{CD}}$：将低噪声子轨迹上的点直接映射到干净数据 $t_0$。
- **GAN 损失与特征匹配损失** $\mathcal{L}_{\mathrm{FM}}$：引入判别器对去噪结果进行对抗训练，以增强细节真实感并稳定训练过程。

### 推理流程

推理时，DCM 将两个专家串联使用：首先由语义专家 $F_{\mathrm{SemE}}$ 从纯噪声 $t_N$ 采样至分割点 $t_\kappa$，完成语义布局与运动的构建；随后由细节专家 $F_{\mathrm{DetE}}$ 从 $t_\kappa$ 继续采样至 $t_0$，完成细粒度细节的精修。整个流程仅需 4 步采样，即可达到与原始 50 步教师模型 HunyuanVideo 相当的视觉质量（VBench 总分 83.83，见表 1）。

### 关键设计决策

| 设计要素 | 基线做法 (VCM) | DCM 做法 | 依据 |
|---------|---------------|---------|------|
| 专家架构 | 单一学生模型 | SemE + DetE 双专家 | Figure 3 证明解耦有效性 |
| 参数效率 | 两个完整独立专家 | 共享基座 + 时间步嵌入 + LoRA | Table 3 显示几乎不影响质量 |
| 语义专家损失 | 仅 $\mathcal{L}_{\mathrm{CD}}$ | $\mathcal{L}_{\mathrm{CD}} + \mathcal{L}_{\mathrm{TC}}$ | Table 3 验证时间一致性增益 |
| 细节专家损失 | 仅 $\mathcal{L}_{\mathrm{CD}}$ | $\mathcal{L}_{\mathrm{CD}}$ + GAN + $\mathcal{L}_{\mathrm{FM}}$ | Table 3 验证细节真实感提升 |
| 轨迹分割 | 全轨迹训练 | $\kappa=37$ 分割高/低噪声区间 | Figure 10 展示 $\kappa$ 敏感性 |

整体框架通过解耦优化避免了高噪声与低噪声样本之间的梯度冲突，同时以参数高效的方式控制额外开销，使得 DCM 在 4 步推理下即可实现与教师模型相当的质量，且每步推理延迟与 LCM、PCM 几乎相同（表 1）。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/004_Figure_4.jpg]]
*Figure 4: The training process of DCM consists of two stages. In the semantic learning stage, we train SemE on high-noise samples with consistency loss and temporal coherence loss as the learning objectives. In the detail learning stage, we initialize DetE with the weights of SemE and introduce a set of time-dependent layers and LoRA. DetE is then trained on low-noise samples, where only the newly added layers and LoRA are updated. The learning objectives in this stage include consistency loss, GAN loss, and Feature Matching loss*

## 核心模块与公式推导

### 问题背景：一致性蒸馏中的优化冲突

DCM 的核心动机源于对一致性蒸馏训练动态的观察。在标准的扩散模型中，前向过程逐步向干净数据 $\pmb{x}_0$ 添加噪声，得到 $\pmb{x}_t$：

$$q(\pmb{x}_t | \pmb{x}_0) = \mathcal{N}(\pmb{x}_t; \sqrt{\alpha_t} \pmb{x}_0, \sqrt{1 - \alpha_t} \pmb{I})$$

教师模型 $\epsilon_\theta$ 通过预测噪声来学习反向过程：

$$\mathcal{L}_{DM} = \mathbb{E}_{\pmb{x}, \epsilon \sim \mathcal{N}(0,1), t} \left[ || \epsilon - \epsilon_{\theta}(\pmb{x}_t, t) ||_2^2 \right]$$

一致性蒸馏（Consistency Distillation）的目标是训练学生模型 $F_S$，使其能将 ODE 轨迹上的任意点直接映射到轨迹终点。其核心损失函数为：

$$\mathcal{L}_{CD} = \mathbb{E}_{\mathbf{x}, t_n} || \Phi(\mathbf{x}_{t_n}, F_S(\mathbf{x}_{t_n}, t_n, c), t_{end}) - \Phi(\hat{\mathbf{x}}_{t_{n-1}}, F_S^-(\hat{\mathbf{x}}_{t_{n-1}}, t_{n-1}, c), t_{end}) ||_2^2$$

其中教师模型计算 ODE 轨迹上的下一个点：

$$\hat{\pmb{x}}_{t_{n-1}} = \Phi(\pmb{x}_{t_n}, F_T(\pmb{x}_{t_n}, t_n, c), t_{n-1})$$

然而，DCM 通过可视化训练动态（Figure 2）发现了关键瓶颈：**高噪声样本与低噪声样本之间的损失贡献和梯度范数存在显著差异**。在采样早期（高噪声阶段），生成结果变化剧烈，模型需要学习语义布局和运动；在采样后期（低噪声阶段），变化趋于平缓，模型主要进行细节精修。单一学生模型同时处理这两类任务时产生优化冲突，导致收敛困难、时序不一致和细节质量下降。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the video synthesis process and the trend of loss variation. (a) In the early stages of sampling, the results change significantly and rapidly, whereas in the later stages, the changes become gradual and smooth. (b) During distillation, the loss and gradient norm of the student model exhibit significant differences between samples with high and low noise levels*

### 核心模块一：双专家架构与轨迹分割

DCM 将 ODE 轨迹在时间步 $\kappa$ 处分割为两个子轨迹：
- **高噪声子轨迹** $\{t_i\}_{i=\kappa}^N$：对应语义合成阶段
- **低噪声子轨迹** $\{t_j\}_{j=0}^\kappa$：对应细节精修阶段

基于此分割，DCM 分别训练两个专家去噪器：

**语义专家（SemE）** 在高噪声子轨迹上训练，学习语义布局和运动。其损失函数为：

$$\mathcal{L}_{SemE} = \mathbb{E}_{\mathbf{x}, t_m \in [t_\kappa, t_N]} || \Phi(\mathbf{x}_{t_m}, F_{SemE}(\mathbf{x}_{t_m}, t_m, c), t_\kappa) - \Phi(\hat{\mathbf{x}}_{t_{m-1}}, F_{SemE}^-(\hat{\mathbf{x}}_{t_{m-1}}, t_{m-1}, c), t_\kappa) ||_2^2$$

注意 SemE 的目标终点是 $t_\kappa$ 而非 $t_0$，即它只需将高噪声样本映射到语义-细节的分界点。

**细节专家（DetE）** 在低噪声子轨迹上训练，负责细粒度细节生成。其损失函数为：

$$\mathcal{L}_{DetE} = \mathbb{E}_{\mathbf{x}, t_n \in [t_0, t_{\kappa}]} || \Phi(\mathbf{x}_{t_n}, F_{DetE}(\mathbf{x}_{t_n}, t_n, c), t_0) - \Phi(\hat{\mathbf{x}}_{t_{n-1}}, F_{DetE}^-(\hat{\mathbf{x}}_{t_{n-1}}, t_{n-1}, c), t_0) ||_2^2$$

DetE 的目标终点是 $t_0$（干净数据），完成最终的细节生成。

推理时，SemE 和 DetE 组合使用：SemE 负责从纯噪声到 $t_\kappa$ 的去噪，DetE 负责从 $t_\kappa$ 到 $t_0$ 的精修。Figure 3 的消融实验证明，SemE+DetE 组合优于单一一致性模型（VCM），验证了优化解耦的有效性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of the visual quality of denoiser variants trained at different noise level samples. By optimizing two expert denoisers to decouple the distillation process into semantic learning and detail learning, and combining them during inference, we achieve the best quantitative and qualitative visual results*

### 核心模块二：参数高效的双专家实现

为避免双专家架构导致参数量翻倍，DCM 采用参数高效策略：
- **共享基座**：SemE 训练完成后冻结，作为 DetE 的初始化
- **DetE 增量参数**：仅添加时间步依赖嵌入层 $\Psi$ 和注意力块的 LoRA 适配器 $\Lambda^\dagger$
- 训练 DetE 时，仅更新 $\Psi$ 和 $\Lambda^\dagger$，冻结其余参数

Figure 5 通过归一化 L1 距离量化了两个专家之间的权重差异，证明了参数高效设计的合理性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/005_Figure_5.jpg]]
*Figure 5: Weight difference distribution between expert denoisers. We employ the normalized L1 distance to quantify the difference between the weights*

### 核心模块三：专家特定的辅助损失

针对两个专家的不同任务特性，DCM 引入了差异化的辅助损失。

**语义专家的时间一致性损失（Temporal Coherence Loss）**：为增强 SemE 生成视频的时序一致性，引入相邻帧约束：

$$\mathcal{L}_{TC} = ||(\pmb{x}_{l:L}^{t_\kappa} - \pmb{x}_{0:L-l}^{t_\kappa}) - (\hat{\pmb{x}}_{l:L}^{t_\kappa} - \hat{\pmb{x}}_{0:L-l}^{t_\kappa})||_2^2$$

该损失强制学生模型在 $t_\kappa$ 处生成的结果与教师模型具有相同的帧间运动模式，从而提升运动自然度。

**细节专家的 GAN 与特征匹配损失**：DetE 在低噪声阶段需要生成逼真的纹理细节，仅靠一致性损失难以保证感知质量。DCM 引入对抗训练：

特征匹配损失用于稳定 GAN 训练：

$$\mathcal{L}_{FM} = \mathbb{E}_{\mathbf{x}, t_n} \left| \left| \Omega(\mathbf{x}_{fake}) - \Omega(\mathbf{x}_{real}) \right| \right|_2^2$$

生成器损失结合对抗损失与特征匹配损失：

$$\mathcal{L}_G = \mathbb{E}_{\mathbf{x}, t_n} [1 - f_D(\Omega(\mathbf{x}_{fake}))] + \mathcal{L}_{FM}$$

判别器损失：

$$\mathcal{L}_D = \mathbb{E}_{\mathbf{x}, t_n} [f_D(\Omega(\mathbf{x}_{fake}))] + \mathbb{E}_{\mathbf{x}, t_n} [1 - f_D(\Omega(\mathbf{x}_{real}))]$$

其中 $\Omega$ 为判别器的中间特征提取器，$f_D$ 为判别器函数。GAN 和特征匹配损失仅作用于 DetE 的训练阶段。

### 关键超参数：分割点 $\kappa$

$\kappa$ 的选择直接影响两个专家的任务划分。DCM 基于相邻时间步之间的 L1 距离来确定最优分割点，默认 $\kappa=37$。Figure 10 展示了不同 $\kappa$ 取值对性能的影响，验证了该选择的合理性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/010_Figure_10.jpg]]
*Figure 10: Impact of different κ*

## 实验与分析

### 核心瓶颈验证：高噪声与低噪声样本的优化冲突

DCM 的设计动机源于对一致性蒸馏训练动态的细致诊断。图 2(b) 可视化了蒸馏过程中学生模型在不同噪声水平样本上的损失与梯度范数变化趋势。结果显示，高噪声样本（对应语义合成阶段）与低噪声样本（对应细节精修阶段）之间存在显著的损失贡献与梯度范数差异。这种差异表明，单一学生模型（VCM）在同时学习语义布局/运动与细节细化时面临根本性的优化冲突——两类目标对模型参数提出了不一致的更新方向，导致收敛困难，最终表现为视频时序不一致与细节质量下降。这一发现构成了 DCM 双专家架构解耦策略的经验基础。

### 主要结果：效率与质量权衡的突破

**VBench 基准评测。** 表 1 汇总了 DCM 与各基线方法在 HunyuanVideo 和 CogVideoX 上的综合表现。在 HunyuanVideo 上，DCM 仅需 4 步采样即达到 VBench 总分 83.83，与原始 50 步教师模型（83.47）相当，且显著优于 LCM（4 步，80.33）和 PCM（4 步，80.83），提升幅度分别达 +3.50 和 +3.00 分。在 CogVideoX 上，DCM 同样以 4 步采样取得 81.00 分，超过 LCM（79.70）和 PCM（80.17）。值得注意的是，DCM 的单步推理延迟与 LCM、PCM 几乎一致（HunyuanVideo 上约 121.5 秒，双 A100 GPU），表明双专家架构并未引入额外的推理开销。

**用户偏好研究。** 表 2 的双盲用户研究进一步验证了 DCM 的感知质量优势。在 HunyuanVideo 上，评分者对 DCM 的偏好率高达 77.33%，远超 PCM 的 22.67%；在 CogVideoX 上，DCM 相对 LCM 的偏好率为 75.33%。这些结果一致表明，DCM 生成的视频在视觉质量和时序自然度上获得了显著的人类偏好优势。

### 消融实验：各组件的独立贡献

表 3 系统拆解了 DCM 各设计组件的贡献。

**解耦优化（OD）。** 将单一 VCM 替换为语义专家（SemE）与细节专家（DetE）的组合，VBench 总分从 80.33 提升至 82.5 以上。图 3(b)(c) 的视觉对比进一步证实，SemE 和 DetE 分别在语义布局/运动和细节精修方面超越了 VCM，验证了将 ODE 轨迹分割为高噪声子轨迹（i=κ..N）和低噪声子轨迹（j=0..κ）进行分阶段训练的有效性。

**参数高效蒸馏（PE）。** 相比训练两个完整独立专家（参数量翻倍），DCM 采用共享基座、仅对 DetE 添加时间步依赖嵌入层和 LoRA 的策略，大幅降低了参数和内存需求，同时几乎不影响视觉质量。图 5 的权重差异分布分析表明，SemE 与 DetE 的权重差异主要集中在新增的轻量模块上，印证了参数高效设计的合理性。

**时间一致性损失（TC）。** 为 SemE 引入时间一致性损失后，VBench 质量分数和运动自然度均获改善。图 8 的视觉对比显示，TC 损失有助于抑制帧间抖动，提升运动连贯性。

**GAN 与特征匹配损失（GF）。** 为 DetE 添加 GAN 损失和特征匹配损失后，细节真实感显著增强。图 9 的对比表明，GF 损失有效提升了纹理清晰度和局部结构的逼真度。

**轨迹分割边界 κ。** 图 10 展示了不同 κ 值对性能的影响。实验基于相邻时间步 L1 距离选定 κ=37 为最佳分割点，该设置在语义合成与细节精修之间取得了最优平衡。

### 局限性与失败模式

尽管 DCM 在 4 步采样下取得了优异表现，但当采样步数进一步减少至 2 步时，合成质量出现显著下降，无法产生令人满意的结果。这表明当前的双专家蒸馏范式在极低步数场景下仍面临挑战。此外，现有实验主要在 HunyuanVideo 和 CogVideoX 两个教师模型上进行验证，其在更广泛的视频扩散模型上的泛化能力尚待确认。GAN 训练的不稳定性在更长视频或更复杂场景下是否会影响整体性能，也需进一步评估。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/006_Table_1.jpg]]
*Table 1: Comparison of efficiency and visual quality of different methods. The latency of HunyuanVideo was measured on two A100 GPUs, and that of CogVideoX on a single A100 GPU*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/009_Table_2.jpg]]
*Table 2: User preference study. The numbers represent the percentage of raters who favor the videos synthesized by our method*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/008_Table_3.jpg]]
*Table 3: Impact of different components of our method*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of visual results between our DCM (4 steps), the original HunyuanVideo, and other competing methods (left). Comparison of latency and VBench score across different methods (right). Latency is measured on two A100 GPUs under the video synthesis configuration of 129 frames at 1280 × 720 resolution*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/007_Figure_6.jpg]]
*Figure 6: Visual quality comparison of different methods. Differences are highlighted in boxes*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/011_Figure_7.jpg]]
*Figure 7: Impact of optimization decoupling and parameterefficient distillation*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2506_03123/figures/012_Figure_8.jpg]]
*Figure 8: Impact of temporal coherence loss*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

DCM 的出发点源于对一致性蒸馏（Consistency Distillation）训练动态的细致观察。论文通过可视化实验（Figure 2）揭示了关键瓶颈：在将教师扩散模型的 ODE 轨迹蒸馏至学生一致性模型的过程中，高噪声阶段（对应语义布局与运动合成）与低噪声阶段（对应细节精修）的损失贡献与梯度范数存在显著差异。这种差异导致单一学生模型在同时学习两类目标时产生优化冲突——模型难以在“快速确定全局结构”与“精细刻画局部细节”之间取得平衡，最终表现为视频的时序不一致与细节退化。

这一发现将问题从“如何设计更快的采样器”重新定义为“如何解耦冲突的学习目标”，为双专家架构提供了直接的经验依据。

### 与一致性蒸馏谱系的关系

DCM 建立在一致性模型（Consistency Models）及其蒸馏变体的技术谱系之上，但通过任务分解与专家化策略形成了清晰的分叉：

- **LCM（Latent Consistency Model）** 是该谱系的基础工作，通过在完整 ODE 轨迹上施加一致性损失 $L_{CD}$，训练单一学生模型直接从任意噪声水平映射至轨迹终点。DCM 的消融基线 VCM（Vanilla Consistency Model）即对应这一范式。实验表明，VCM 在 VBench 上仅获 80.33 分（4 步），显著低于 DCM 的 83.83 分（Table 1），验证了单一模型在视频生成场景下的优化冲突问题。

- **PCM（Phased Consistency Model）** 将蒸馏过程按时间步分阶段进行，但仍使用单一模型在不同阶段之间切换。DCM 与此的关键分歧在于：PCM 是“时序上的分阶段训练”，而 DCM 是“架构上的专家解耦”——语义专家 SemE 与细节专家 DetE 是两个具有不同参数和损失函数的去噪器，在推理时协同工作。实验数据（Table 1）显示 PCM 的 VBench 分数为 80.83，落后 DCM 约 3 分，且用户偏好研究中 DCM 以 77.33% 的显著优势胜出（Table 2），表明架构层面的解耦比单纯的训练策略分解更有效。

### 参数高效策略的定位

双专家架构的一个直接代价是参数量翻倍。DCM 通过参数高效蒸馏（Parameter-Efficient Distillation）规避了这一问题：语义专家 SemE 首先在高噪声子轨迹上完整训练，随后被冻结作为细节专家 DetE 的初始化基座；DetE 仅新增时间步依赖嵌入层 $\Psi$ 和注意力块的 LoRA 适配器 $\Lambda^\dagger$，在低噪声子轨迹上仅优化这些新增参数（Figure 4, Section 3.3）。

这一设计与当前大模型参数高效微调（PEFT）的主流实践一致，但其贡献在于将 PEFT 从“下游任务适配”重新定位为“学习目标解耦的使能器”——LoRA 的低秩约束恰好构成对语义知识的隐式正则化，防止细节学习干扰已习得的全局结构。Figure 5 的权重差异分析（归一化 L1 距离）量化了两个专家之间的参数分化程度，为解耦的有效性提供了结构层面的证据。

### 损失函数设计的针对性

DCM 对两个专家施加了差异化的辅助损失，进一步强化了任务分离：

- **语义专家 SemE** 额外引入时间一致性损失 $L_{TC}$，通过约束相邻帧在边界时间步 $t_\kappa$ 处的预测一致性，显式增强运动平滑性。这一定位弥补了标准一致性损失对时序关系的弱监督。

- **细节专家 DetE** 额外引入 GAN 损失与特征匹配损失 $L_{FM}$，利用判别器对低噪声阶段的生成结果进行真实感监督。特征匹配损失通过判别器中间层特征的 L2 对齐稳定训练，缓解了 GAN 在低噪声区域的模式坍塌风险。

消融实验（Table 3）表明，移除时间一致性损失会降低运动自然度指标，而移除 GAN/特征匹配损失则导致细节真实感下降，验证了两种辅助损失与其对应专家角色的匹配性。

### 轨迹分割的边界选择

ODE 轨迹的分割点 $\kappa$（默认值 37）是双专家架构的关键超参数。论文通过分析相邻时间步之间教师模型预测的 L1 距离来确定这一边界（Section 4.3, Figure 10）：在高噪声区域，相邻步的预测变化剧烈（对应语义快速形成）；在低噪声区域，变化趋于平缓（对应细节渐进精修）。$\kappa$ 被选为这一过渡区域的拐点，使得 SemE 聚焦于“变化大、结构性强”的阶段，DetE 聚焦于“变化小、细节密集”的阶段。Figure 10 的敏感性分析显示，偏离最优 $\kappa$ 会导致语义质量或细节质量的单方面下降，验证了分割点的合理性。

### 适用边界与局限

DCM 的有效性已在 HunyuanVideo 和 CogVideoX 两个教师模型上得到验证，但其适用边界需要审慎界定：

1. **采样步数下限**：论文明确指出，当采样步数降至 4 步以下（如 2 步）时，合成质量显著退化。这表明双专家架构并未根本解决极低步数下的信息压缩极限问题，4 步仍是当前方法的能力下界。

2. **教师模型依赖性**：DCM 的性能上限受限于教师模型的质量。目前仅在 HunyuanVideo 和 CogVideoX 上验证，尚未在更多样化的视频扩散模型（如基于 3D VAE 或时空分离架构的模型）上测试，其跨架构泛化性需要进一步验证。

3. **GAN 训练的稳定性风险**：细节专家的 GAN 损失在低噪声阶段引入对抗训练，虽然在当前实验设置（29 帧、720×480 分辨率）下表现稳定，但在更长视频或更复杂场景下，GAN 的不稳定性可能成为潜在瓶颈。

### 开放问题

1. **单步/两步生成的可行性**：如何进一步压缩采样步数至 1–2 步同时保持高质量，是当前一致性蒸馏范式的共性难题。可能的路径包括改进轨迹分割策略、引入更激进的蒸馏目标，或探索与 rectified flow 等替代框架的融合。

2. **跨架构泛化**：参数高效的双专家蒸馏范式能否直接迁移至基于不同骨干（如 DiT、U-ViT）或不同 VAE 压缩率的视频扩散模型，尚待实证检验。

3. **时间一致性损失的优化空间**：当前 $L_{TC}$ 仅使用固定帧间隔 $l$，其设计空间（如多尺度帧间隔、可学习的时序对齐策略）仍有探索潜力。

4. **GAN 训练的规模化稳定性**：随着视频长度和分辨率的增加，细节专家的 GAN 训练是否需要引入额外的稳定化技术（如自适应判别器增强、梯度惩罚），是一个待验证的工程问题。

## 原文 PDF

![[paperPDFs/ICCV_2025/DCM_Dual-Expert_Consistency_Model_for_Efficient_and_High-Quality_Video_Generation.pdf]]
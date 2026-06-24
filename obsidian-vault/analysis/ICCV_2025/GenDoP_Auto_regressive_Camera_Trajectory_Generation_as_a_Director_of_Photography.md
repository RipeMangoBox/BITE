---
title: "GenDoP: Auto-regressive Camera Trajectory Generation as a Director of Photography"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.pdf
aliases:
  - GenDoP
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建了首个面向自由移动艺术相机轨迹的大规模多模态数据集 DataDoP（包含 29K 镜头、轨迹、深度图和详细字幕），并设计了一种将相机参数离散化为 token 的自回归 Transformer 模型 GenDoP，利用序列建模和多模态条件（文本 + RGBD）实现可控、稳定的轨迹生成。
primary_logic: 将相机轨迹生成形式化为离散 token 序列的逐步预测任务，通过自回归模型结合初始帧的几何与外观信息，有效捕捉相机运动的时序依赖性和场景交互，生成稳定且具有导演意图的自由移动轨迹。
claims:
  - 在 Motion 字幕条件下，GenDoP 的 CLaTr-CLIP 得分（36.179）显著高于在 DataDoP 上重新训练的 Director3D（31.689），F1-Score 达 0.400，CLaTr-FID 低至 22.714（Director3D 为 31.979）。
  - 在 Directorial 字幕条件下，GenDoP 同样以 CLaTr-CLIP 32.408 领先 Director3D 的 23.505，F1-Score 0.399 对比 0.361，且用户研究在 Alignment、Quality、Complexity 维度均获最高评分。
  - 消融实验证实典型归一化显著提升性能：有归一化时 CLaTr-CLIP 为 36.179、CLaTr-FID 22.714，移除归一化则分别降至 14.917 和 68.590。
  - 可训练编码器（文本、视觉）相比冻结编码器在所有指标上均带来增益，表明跨模态对齐对轨迹生成至关重要。
---

# GenDoP: Auto-regressive Camera Trajectory Generation as a Director of Photography

> [!tip] 核心洞察
> 将相机轨迹生成形式化为离散 token 序列的逐步预测任务，通过自回归模型结合初始帧的几何与外观信息，有效捕捉相机运动的时序依赖性和场景交互，生成稳定且具有导演意图的自由移动轨迹。

| 字段      | 内容                                                                                                             |
| ------- | -------------------------------------------------------------------------------------------------------------- |
| 中文题名    | GenDoP：作为摄影指导的自回归相机轨迹生成                                                                                        |
| 英文题名    | GenDoP: Auto-regressive Camera Trajectory Generation as a Director of Photography                              |
| 会议/期刊   | ICCV 2025                                                                                                      |
| Links   | [paper](https://arxiv.org/abs/2504.07083) · [Project](https://kszpxxzmc.github.io/GenDoP/)                     |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | GenDoP                                                                                                         |
| Dataset | Motion Caption, Directorial Caption, User Study                                                                |

> [!tip] 效果简介
> - Motion Caption (DataDoP test set) 上，CLaTr-CLIP Score 36.179 vs 31.689 (Director3D trained on DataDoP) (+4.490)；F1-Score (Motion Tag Accuracy) 0.400 vs 0.391 (Director3D trained on DataDoP) (+0.009)；CLaTr-FID 22.714 vs 31.979 (Director3D trained on DataDoP) (-9.265)。
> - Directorial Caption (DataDoP test set) 上，CLaTr-CLIP Score 32.408 vs 23.505 (Director3D trained on DataDoP) (+8.903)。
> - User Study (Motion & Directorial) 上，Average User Rating - Alignment 4.693 (Motion) / 4.617 (Directorial) vs 最高基线 3.753 (Motion) / 3.808 (Directorial) (significant improvement)。

## 概述

现有相机轨迹生成方法面临一个核心瓶颈：训练数据多来自跟踪主导或物体/场景中心的镜头，缺乏体现导演意图的自由移动轨迹和对应的详细文本描述；同时，基于扩散模型的生成范式容易产生抖动和不稳定的轨迹，且与文本指令的对齐能力有限。

针对这一问题，本文提出 **GenDoP**——一种将相机轨迹生成形式化为离散 token 序列逐步预测的自回归 Transformer 模型。其核心洞察在于：通过将相机参数离散化为 token，并利用自回归序列建模捕捉相机运动的时序依赖性和场景交互，能够生成稳定且高度可控的自由移动轨迹。方法的关键创新包含两个层面：(1) 构建了首个面向自由移动艺术相机轨迹的大规模多模态数据集 **DataDoP**（29K 镜头，含轨迹、深度图和详细字幕）；(2) 设计了多模态条件（文本 + 可选 RGBD 图像）驱动的自回归解码框架，结合典型归一化策略，显著提升了轨迹的稳定性和文本对齐度。

在方法谱系上，GenDoP 将生成范式从扩散模型（如 **Director3D** (Li et al., NeurIPS 2024)、**CCD** (Jiang et al., Comput. Graph. Forum 2024)、**E.T.** (Courant et al., ECCV 2024)）转向自回归 Transformer，将条件输入从纯文本或角色轨迹扩展为文本与初始帧几何/外观信息的融合，并依托 DataDoP 的大规模自由移动轨迹数据，突破了现有方法在运动复杂度和指令跟随方面的局限。

实验结果验证了上述设计的有效性：在 Motion 字幕条件下，GenDoP 的 CLaTr-CLIP 得分达到 36.179，显著优于在 DataDoP 上重新训练的 Director3D（31.689），CLaTr-FID 低至 22.714（对比 31.979）；在 Directorial 字幕条件下，CLaTr-CLIP 以 32.408 领先 Director3D 的 23.505。用户研究进一步表明，GenDoP 在轨迹对齐度、质量和复杂度维度均获得最高评分。消融实验证实，典型归一化和可训练编码器是性能的关键支撑——移除归一化导致 CLaTr-CLIP 骤降约 21 分、CLaTr-FID 飙升约 46 分。

## 背景与动机

### 问题背景：从文本到视频生成中的相机控制困境

文本到视频（T2V）和图像到视频（I2V）生成近年来取得了显著进展，但一个核心瓶颈始终存在：**如何生成具有专业摄影指导意图的相机运动轨迹**。在电影和视频创作中，相机运动（推拉、摇移、跟拍、环绕等）不仅是技术操作，更是叙事语言——它决定了观众的视觉焦点、空间感知和情感节奏。然而，现有的相机轨迹生成方法在应对这一需求时，暴露出三个结构性缺陷。

### 现有方法的三个缺口

**第一，数据集存在系统性偏差。** 现有方法所依赖的数据集——例如 CCD（Jiang et al., Comput. Graph. Forum 2024）和 E.T.（Courant et al., ECCV 2024）使用的人像跟踪数据，以及 Director3D（Li et al., NeurIPS 2024）使用的物体/场景中心多视角数据——几乎全部聚焦于**跟踪主导或物体中心**的运动模式。这些数据集中，相机要么跟随特定人物移动，要么围绕固定物体旋转，缺少电影中常见的**自由移动艺术轨迹**（如穿越场景、动态变焦、复合运动）。更关键的是，这些数据集缺乏描述**导演意图**的详细字幕，使得模型无法学习“为何这样移动相机”的语义层面。

**第二，生成范式存在稳定性缺陷。** 当前主流方法普遍采用扩散模型（CCD、E.T.）或 DiT（Director3D）来生成连续相机参数。扩散模型虽然在图像生成中表现出色，但在轨迹生成中容易产生**抖动和不稳定**——相机位姿在相邻帧之间出现高频噪声，导致生成的视频观感不专业。这是因为扩散模型一次生成完整轨迹，缺乏对相机运动**时序依赖性**的显式建模：第 *t* 帧的位姿应该由前序位姿和场景约束共同决定，而非独立采样。

**第三，文本对齐能力有限。** 即使提供了文本描述，现有方法生成的轨迹与指令之间的语义对齐度仍然不足。Director3D 仅接受文本条件，无法利用首帧的几何与外观信息进行场景感知的运动规划；而 CCD 和 E.T. 虽然引入了角色轨迹，但并未建立文本-场景-运动三者之间的有效跨模态对齐机制。

### 本文动机：从数据集到生成范式的双重重构

针对上述缺口，GenDoP 提出了一个**数据集-模型协同设计**的解决方案。其核心动机包含两个层面：

1. **构建首个面向自由移动艺术相机轨迹的大规模多模态数据集 DataDoP**。该数据集包含 29K 个镜头、12M 帧、113 小时视频，平均镜头时长 14.4 秒，覆盖 27 种平移运动和 7 种旋转运动的组合。每个镜头配备两类字幕：**运动字幕**（Motion Caption）描述相机运动本身，**导演字幕**（Directorial Caption）描述相机运动与场景的交互及导演意图。这一设计填补了“自由移动轨迹 + 导演意图描述”的数据空白。

2. **设计自回归 Transformer 模型 GenDoP**，将相机轨迹生成形式化为**离散 token 序列的逐步预测任务**。通过将相机参数离散化为 token，并利用自回归解码器结合文本、RGB 和深度图等多模态条件，GenDoP 有效捕捉了相机运动的时序依赖性和场景交互，从根本上缓解了扩散模型的抖动问题，同时显著提升了文本对齐精度。

这一双重重构使得 GenDoP 在可控性、稳定性和运动复杂度三个维度上均超越了现有方法，为相机控制视频生成铺平了道路。

## 核心创新

GenDoP 的核心创新在于将相机轨迹生成从传统的扩散范式转向**自回归序列建模**，并通过**数据集-表示-架构**三个层面的协同重构解决了现有方法的根本瓶颈。

### 1. 范式转换：从扩散生成到自回归序列建模

现有方法普遍采用扩散模型范式：**CCD**（Jiang et al., Comput. Graph. Forum 2024）和 **E.T.**（Courant et al., ECCV 2024）依赖扩散过程生成轨迹，**Director3D**（Li et al., NeurIPS 2024）则使用 DiT 架构。这些方法面临两个结构性缺陷：一是生成轨迹易出现抖动和不稳定，二是文本对齐能力有限。

GenDoP 将相机轨迹生成**形式化为离散 token 序列的逐步预测任务**（Sec. 4.1, Figure 3）。具体而言，相机位姿序列 $\mathcal{C} = \{ \mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_{N-1} \}$ 中的每个位姿 $\mathbf{x}_i = [ \mathbf{R}_i | \mathbf{t}_i | \mathbf{K}_i ]$ 被离散化为整型 token，由基于 OPT Transformer 的自回归解码器按时间顺序逐 token 预测。这一设计使模型能够**显式捕捉相机运动的时序依赖性和场景交互**，从根本上抑制了扩散模型中常见的轨迹抖动问题。

### 2. 条件输入扩展：从单一文本到多模态融合

基线方法的条件输入存在显著局限：Director3D 仅依赖文本条件，CCD 和 E.T. 虽引入角色轨迹，但缺乏对场景几何与外观的感知能力。

GenDoP 构建了**多模态条件融合机制**（Sec. 4.3）：
- **文本编码器**基于 Stable Diffusion 2.1 预训练文本编码器 + MLP，提取细粒度语义特征 $\mathbf{Z}_T$；
- **RGB 编码器**基于 CLIP Vision Model + MLP，从首帧 RGB 图像提取视觉外观特征 $\mathbf{Z}_I$；
- **深度编码器**同样基于 CLIP Vision Model + MLP，从首帧深度图提取几何结构特征 $\mathbf{Z}_D$。

三者拼接为统一潜在表示 $\mathbf{Z} = [ \mathbf{Z}_T ; \mathbf{Z}_I ; \mathbf{Z}_D ] \in \mathbb{R}^{M \times L}$，作为自回归解码器的条件输入。消融实验证实，**可训练编码器相比冻结编码器在所有指标上均带来显著增益**（Table 4），表明跨模态对齐对轨迹生成至关重要。

### 3. 轨迹表示革新：典型归一化与离散化

基线方法使用原始连续坐标或未归一化表示，导致模型难以学习稳定的运动模式。GenDoP 引入**典型归一化**（Canonical Normalization）策略（Sec. 4.2）：

- **旋转归一化**：$\mathbf{R}_i^{\mathrm{norm}} = \mathbf{R}_0^{\top}\mathbf{R}_i$，将第 $i$ 帧旋转相对首帧变换；
- **平移归一化**：$\hat{\mathbf{t}}_i = \mathbf{R}_0^{\top}(\mathbf{t}_i - \mathbf{t}_0)$，$\mathbf{t}_i^{\mathrm{norm}} = \hat{\mathbf{t}}_i / (s + \epsilon)$，平移量经相对化后缩放到单位最大范数。

归一化后的连续参数被压缩至 $[0,1]$ 区间，再通过可学习码本 $\mathcal{V} \in \mathbb{R}^{(B+4) \times L}$ 离散化为 token。**消融实验表明这是性能的关键因素**（Table 4）：移除归一化后，CLaTr-CLIP 从 36.179 骤降至 14.917（下降约 21 分），CLaTr-FID 从 22.714 飙升至 68.590（上升约 46 分）。超参数消融进一步确定最优离散 bin 数 $B=256$（Table S1）。

### 4. 数据集支撑：DataDoP 填补自由移动轨迹空白

上述方法创新的有效性建立在**DataDoP 数据集**之上（Table 1）。现有数据集局限于跟踪主导或物体/场景中心的轨迹，缺少体现导演意图的自由移动轨迹和详细字幕。DataDoP 包含 29K 镜头、12M 帧、113 小时数据，平均镜头时长 14.4 秒，提供两种互补字幕：
- **Motion Caption**：描述相机运动本身；
- **Directorial Caption**：描述相机运动与场景的交互及导演意图。

用户研究验证了数据集的高质量（Table 2）：Video-Traj 对齐准确率 0.863，Traj-Motion 准确率 0.913，Traj-Directorial 准确率 0.858，质量评分 0.945，Fleiss' Kappa > 0.4。

### 5. 创新的综合效果

四个 changed slots 的协同作用使 GenDoP 在多项指标上显著超越基线（Table 3）：
- Motion 字幕条件下，CLaTr-CLIP 达 36.179（Director3D 为 31.689），CLaTr-FID 低至 22.714（Director3D 为 31.979）；
- Directorial 字幕条件下，CLaTr-CLIP 领先 Director3D 近 9 分（32.408 vs 23.505）；
- 用户研究中，Alignment 评分达 4.693/4.617（Motion/Directorial），远超最高基线 3.753/3.808。

值得注意的是，大模型虽获得最低 CLaTr-FID（20.474），但文本对齐指标（CLaTr-CLIP 33.843）低于 base 模型，揭示了**轨迹质量与文本对齐之间的权衡**（Table S1），为后续研究指明了优化方向。

## 整体框架

GenDoP 的整体框架围绕“将相机轨迹生成形式化为离散 token 序列的自回归预测”这一核心洞察构建。其 pipeline 由数据预处理端的**典型归一化与轨迹标记化**、多模态条件端的**文本/视觉/深度编码器**、以及生成端的**自回归解码器**三大模块串联而成，形成从多模态输入到完整相机轨迹的端到端映射。

### 输入输出流

系统接受两类输入组合：**仅文本条件**（运动字幕或导演字幕）或**文本 + 首帧 RGBD 条件**。文本条件 $T$ 描述期望的相机运动（如“镜头缓慢推进的同时向左平移”）或包含场景交互与导演意图的复合描述；可选的 RGBD 输入由首帧 RGB 图像 $I_0$ 及其对应深度图 $D_0$ 组成，为轨迹生成提供初始帧的几何与外观约束。输出为一条包含 $N$ 帧的相机轨迹 $\mathcal{C} = \{ \mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_{N-1} \}$，其中每帧位姿 $\mathbf{x}_i = [\mathbf{R}_i | \mathbf{t}_i | \mathbf{K}_i]$ 包含旋转矩阵、平移向量和内参矩阵（Figure 3 顶部）。

### 模块关系与数据流

**1. 典型归一化与轨迹标记器 (Trajectory Tokenizer)**  
在训练阶段，原始相机轨迹首先经过典型归一化（Canonical Normalization）：将首帧设为世界参考系（$\mathbf{R}_0^{\mathrm{norm}} = \mathbf{I}$，$\mathbf{t}_0^{\mathrm{norm}} = \mathbf{0}$），后续帧的旋转和平移均相对首帧进行变换：
$$\mathbf{R}_i^{\mathrm{norm}} = \mathbf{R}_0^{\top}\mathbf{R}_i, \quad \hat{\mathbf{t}}_i = \mathbf{R}_0^{\top}(\mathbf{t}_i - \mathbf{t}_0)$$
平移量进一步缩放到单位最大范数 $\mathbf{t}_i^{\mathrm{norm}} = \hat{\mathbf{t}}_i / (s + \epsilon)$。归一化后的连续参数被压缩至 $[0,1]$ 区间，再通过可学习的码本 $\mathcal{V}$ 离散化为整型 token 序列 $\{y_0, y_1, \ldots, y_{N-1}\}$。这一步骤是 GenDoP 稳定性的关键——消融实验（Table 4）表明，移除典型归一化会导致文本对齐指标 CLaTr-CLIP 从 36.179 骤降至 14.917，轨迹质量指标 CLaTr-FID 从 22.714 恶化至 68.590。

**2. 多模态条件编码器**  
三个并行的编码器负责将异构输入映射到统一的潜在空间：
- **文本编码器**：基于 Stable Diffusion 2.1 预训练文本编码器 + MLP，从字幕 $T$ 中提取语义特征，生成潜在代码 $\mathbf{Z}_T$。
- **RGB 编码器**：基于 CLIP Vision Model 预训练编码器 + MLP，从首帧 RGB 图像 $I_0$ 中提取视觉外观特征 $\mathbf{Z}_I$。
- **深度编码器**：同样基于 CLIP Vision Model + MLP，从首帧深度图 $D_0$ 中提取几何结构特征 $\mathbf{Z}_D$。

三种潜在代码沿特征维度拼接为最终条件向量：
$$\mathbf{Z} = [\mathbf{Z}_T; \mathbf{Z}_I; \mathbf{Z}_D] \in \mathbb{R}^{M \times L}, \quad M = M_T + M_I + M_D$$
消融实验（Table 4）证实，可训练编码器相比冻结编码器在所有指标上均带来显著增益，说明跨模态对齐对轨迹生成至关重要。当仅使用文本条件时，RGB 和深度编码器分支被省略，$\mathbf{Z}$ 仅由 $\mathbf{Z}_T$ 构成。

**3. 自回归解码器**  
解码器基于 OPT Transformer 架构，以自回归方式逐步生成轨迹。在第 $P$ 步，解码器接收条件向量 $\mathbf{Z}$ 与已生成的历史 token $\{y_0, \ldots, y_{P-1}\}$，经嵌入和位置编码后形成输入：
$$\mathbf{X}_P = \mathrm{PosEmbed}([\mathbf{Z}; \mathcal{V}[y_{0:P-1}]])$$
解码器输出下一个 token 的概率分布，通过交叉熵损失与 L2 正则项联合优化：
$$L = \mathrm{CrossEntropy}(S[1:], \hat{S}[:,-1]) + \lambda \|\mathbf{Z}\|_2^2$$
其中 $S$ 为真实 token 序列，$\hat{S}$ 为预测 logits。推理时，模型从起始 token 开始逐帧生成，直至产生完整的 $N$ 帧轨迹，再经逆归一化恢复为世界坐标系下的相机位姿。

### 设计逻辑

将相机轨迹生成转化为离散 token 的自回归预测，使得模型能够天然捕捉相机运动的**时序依赖性**——每一帧的位姿预测都显式地以历史轨迹为条件，从而抑制扩散模型中常见的抖动和不稳定问题。同时，多模态条件（文本 + RGBD）的引入使模型在遵循语言指令的同时，能够感知初始帧的**几何与外观约束**，生成与场景内容相协调的自由移动轨迹。超参数消融（Table S1）进一步确定了最优配置：离散 bin 数 256、轨迹长度 30、模型规模 base（L=1024, 12 layers），在此设置下模型在文本对齐与轨迹质量之间取得最佳平衡。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/001_Figure_1.jpg]]
*Figure 1: Overview. Top: DataDoP data construction. Given RGB video frames, we extract RGBD images and camera poses, then tag the pose sequence with different motion categories (in different colors). With LLM, we generate two types of captions from motion tags and RGBD inputs: Motion Caption describes the camera movements, while Directorial Caption describes the camera movements along with their interaction with the scene and directorial intent. Bottom: Our GenDoP method supports multi-modal inputs for trajectory creation. The generated camera sequence can be easily applied to various video generation tasks, including text-to-video (T2V) [13] and image-to-video (I2V) generation [15]. GenDoP paves the...*

## 核心模块与公式推导

GenDoP 将相机轨迹生成形式化为一个自回归的序列预测任务，其核心架构由轨迹标记器、多模态编码器和自回归解码器三个关键模块构成。

### 相机轨迹标记器

相机轨迹被定义为一组连续的位姿序列：

$$
\mathcal{C} = \{ \mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_{N-1} \}
$$

其中每个位姿 $\mathbf{x}_i$ 包含旋转矩阵 $\mathbf{R}_i$、平移向量 $\mathbf{t}_i$ 和内参矩阵 $\mathbf{K}_i$：

$$
\mathbf{x}_i = [ \mathbf{R}_i \mid \mathbf{t}_i \mid \mathbf{K}_i ]
$$

**典型归一化**是轨迹标记器的关键操作，其核心机制是将所有位姿相对于首帧进行变换，从而消除绝对世界坐标系的歧义性，使模型专注于相对运动模式。具体而言：

- **旋转归一化**：将第 $i$ 帧的旋转矩阵左乘首帧旋转的逆，使其表达为首帧坐标系下的相对旋转：
  $$
  \mathbf{R}_i^{\mathrm{norm}} = \mathbf{R}_0^{\top}\mathbf{R}_i
  $$
- **平移归一化**：首先计算相对于首帧的平移差，再通过首帧旋转对齐坐标系，最后除以最大范数进行尺度归一化：
  $$
  \hat{\mathbf{t}}_i = \mathbf{R}_0^{\top}(\mathbf{t}_i - \mathbf{t}_0), \quad \mathbf{t}_i^{\mathrm{norm}} = \frac{\hat{\mathbf{t}}_i}{s + \epsilon}
  $$
  其中 $s$ 为所有平移向量的最大范数，$\epsilon$ 为防止除零的小常数。

归一化后的连续参数被压缩至 $[0,1]$ 区间，再离散化为整型 token 序列，作为自回归解码器的预测目标。消融实验证实，移除典型归一化会导致 CLaTr-CLIP 从 36.179 骤降至 14.917，CLaTr-FID 从 22.714 飙升至 68.590，表明该模块是性能的决定性因素。

### 多模态编码器

模型支持三类条件输入的编码，分别通过独立的预训练编码器与可训练的 MLP 投影层实现：

- **文本编码器**：基于 Stable Diffusion 2.1 的预训练文本编码器提取语义特征，经 MLP 生成潜在代码 $\mathbf{Z}_T$。
- **RGB 编码器**：基于 CLIP Vision Model 从首帧 RGB 图像提取外观特征，经 MLP 生成潜在代码 $\mathbf{Z}_I$。
- **深度编码器**：同样基于 CLIP Vision Model 从首帧深度图提取几何特征，经 MLP 生成潜在代码 $\mathbf{Z}_D$。

三类潜在代码通过拼接形成统一的条件表示，作为解码器的前缀嵌入：

$$
\mathbf{Z} = [ \mathbf{Z}_T ; \mathbf{Z}_I ; \mathbf{Z}_D ] \in \mathbb{R}^{M \times L}, \quad M = M_T + M_I + M_D
$$

消融研究表明，可训练编码器相比冻结编码器在所有指标上均带来显著增益，说明跨模态对齐对轨迹生成至关重要。

### 自回归解码器

解码器基于 OPT Transformer 架构，将轨迹生成转化为逐步的 next-token 预测问题。在预测第 $P$ 个 token 时，解码器的输入嵌入由条件向量和历史 token 的嵌入拼接后加入位置编码构成：

$$
\mathbf{X}_P = \mathrm{PosEmbed}\big( [ \mathbf{Z} ; \mathcal{V}[\mathbf{y}_{0:P-1}] ] \big) \in \mathbb{R}^{(M+P) \times L}
$$

其中 $\mathcal{V}$ 为可学习的离散化码本，$\mathbf{y}_{0:P-1}$ 为已生成的前 $P$ 个轨迹 token。解码器基于 $\mathbf{X}_P$ 预测下一个 token 的概率分布，通过交叉熵损失与潜在代码的 L2 正则项联合优化：

$$
\mathcal{L} = \mathrm{CrossEntropy}(S[1:], \hat{S}[:,-1]) + \lambda \|\mathbf{Z}\|_2^2
$$

该自回归范式使模型能够显式捕捉相机运动的时序依赖性——每个新位姿的预测都受到历史相机状态和输入条件的共同约束，从而生成稳定且符合指令的轨迹。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/005_Figure_3.jpg]]
*Figure 3: Our Auto-regressive Generation Model. Our model supports multi-modal inputs and generates trajectories based on these inputs. By treating the task as an auto-regressive next-token prediction problem, the model sequentially generates trajectories, with each new pose prediction influenced by previous camera states and input conditions*

## 实验与分析

### 核心瓶颈与因果机制

现有相机轨迹生成方法面临三个关键瓶颈：第一，训练数据集（如 **CCD**（Jiang et al., Comput. Graph. Forum 2024）和 **E.T.**（Courant et al., ECCV 2024）所用的人像跟踪数据，以及 **Director3D**（Li et al., NeurIPS 2024）所用的物体/场景中心数据）缺乏自由移动的艺术化相机轨迹和体现导演意图的详细字幕；第二，基于扩散模型的生成范式（CCD、E.T. 使用扩散模型，Director3D 使用 DiT）容易产生轨迹抖动和不稳定；第三，文本与轨迹的对齐能力有限，难以捕捉复杂的导演指令。

GenDoP 通过两个因果性设计解决上述问题：**数据层面**，构建了 DataDoP——首个面向自由移动艺术相机轨迹的大规模多模态数据集（29K 镜头、12M 帧、113 小时），每条轨迹配有运动字幕（Motion Caption）和导演字幕（Directorial Caption），并提供首帧 RGBD 图像；**模型层面**，将相机轨迹生成形式化为离散 token 序列的自回归预测任务，利用 Transformer 解码器逐步生成相机位姿，通过序列建模捕捉相机运动的时序依赖性和场景交互，实现稳定且指令对齐的轨迹生成。

### 主要实验结果

#### 文本条件生成（Motion Caption 与 Directorial Caption）

在 DataDoP 测试集上，GenDoP 在所有指标上均显著超越基线方法。为公平对比，Director3D 在 DataDoP 上重新训练，消除了数据集差异的影响。

**Motion Caption 条件**下（Table 3），GenDoP 的文本-轨迹对齐指标 CLaTr-CLIP 达到 **36.179**，较 Director3D（31.689）提升 **+4.490**；轨迹质量指标 CLaTr-FID 低至 **22.714**，远优于 Director3D 的 31.979（降低 **-9.265**）；运动标签准确率 F1-Score 为 **0.400**，略高于 Director3D 的 0.391。定性结果（Figure 4）显示，GenDoP 生成的轨迹稳定且紧密跟随指令，而其他方法存在明显抖动或指令失配。

**Directorial Caption 条件**下，GenDoP 的优势更为突出：CLaTr-CLIP 达到 **32.408**，较 Director3D（23.505）提升 **+8.903**；F1-Score 为 **0.399** vs 0.361。这表明 GenDoP 能更好地理解包含场景交互和导演意图的复杂描述。

#### 用户研究

用户研究从 Alignment（对齐度）、Quality（轨迹质量）、Complexity（复杂度）三个维度评估。GenDoP 在 Motion 条件下获得 **4.693** 的 Alignment 评分，在 Directorial 条件下获得 **4.617**，均显著高于最佳基线（Motion: 3.753, Directorial: 3.808）。Fleiss' Kappa 系数超过 0.4，验证了评分一致性。

#### RGBD 与文本条件生成

引入首帧 RGBD 图像后，GenDoP 在相同文本条件下能生成更贴合场景几何约束的轨迹（Figure 5）。虽然纯文本模型已能生成指令合规的轨迹，但 RGBD 条件模型展现出更强的场景适应能力，能利用深度和外观信息调整运动路径。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative Results of RGBD & Text-conditioned Generation. This figure compares the impact of incorporating RGBD input on trajectory generation under identical text conditions. While both models generate command-compliant trajectories, the RGBD & Text-conditioned model demonstrates superior scene adaptation by utilizing RGBD data to integrate geometric and contextual constraints*

### 消融实验

#### 典型归一化的关键作用

典型归一化（Canonical Normalization）是 GenDoP 性能的核心支撑。消融实验（Table 4）表明，移除归一化导致性能急剧恶化：CLaTr-CLIP 从 **36.179** 骤降至 **14.917**（下降约 21 分），CLaTr-FID 从 22.714 飙升至 **68.590**（上升约 46 分）。这证实了将相机位姿相对化到首帧坐标系对于自回归建模至关重要——归一化消除了绝对坐标的歧义性，使模型能专注于运动模式的建模。

#### 编码器可训练性的影响

可训练编码器（文本编码器、视觉编码器均参与训练）相比冻结编码器在所有指标上均带来显著增益（Table 4）。这表明跨模态对齐（文本-轨迹、视觉-轨迹）需要端到端的联合优化，冻结预训练特征无法充分捕捉轨迹生成所需的细粒度语义和几何对应关系。

#### 超参数消融

超参数消融（Table S1）确定了最优配置：离散 bin 数 **B=256**、轨迹长度 **N=30**、模型规模 **base**（L=1024, 12 layers）。增大模型规模至 large 虽能进一步降低 CLaTr-FID 至 **20.474**（轨迹质量提升），但 CLaTr-CLIP 降至 **33.843**（文本对齐下降），揭示了轨迹质量与文本对齐之间存在权衡——更大模型可能过拟合轨迹分布而牺牲条件跟随能力。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/015_Table.jpg]]
*Table: S1. Ablation Study on Hyperparameters. We conduct ablation experiments on several hyperparameters, including the number of discrete bins, trajectory length, and model size. These parameters correspond to the discrete bin size B, the trajectory length N , and the model size (as detailed in Sec. 5.1). The results show that the optimal performance is achieved when the number of discrete bins is set to 256, the trajectory length to 30, and the model size to base*

### 失败模式与局限性

1. **几何估计依赖**：轨迹提取依赖 MonST3R 的动态场景几何估计，在高度动态或低纹理场景中可能引入噪声，影响训练数据质量。
2. **字幕偏差**：DataDoP 字幕由 GPT-4o 生成，尽管经过人工验证，仍可能存在语言描述偏差或与真实导演意图不完全一致。
3. **固定长度限制**：当前模型针对 N=60 的轨迹长度设计，对超长或极短镜头的灵活性有限。
4. **泛化能力未知**：模型仅在 DataDoP 上训练，对数据集之外的电影风格或镜头类型的泛化能力尚未验证。
5. **量化精度损失**：相机参数离散化虽便于自回归建模，但可能带来量化精度损失，影响细微运动（如微距推拉）的重现精度。

### 图表结论摘要

- **Table 1**：DataDoP 是首个专注于自由移动艺术轨迹的大规模数据集，填补了现有数据集在轨迹多样性和字幕丰富度上的空白。
- **Figure 2**：DataDoP 包含 27 种平移运动和 7 种旋转运动的组合分布，同一字幕对应多样化的轨迹实现，体现了数据集的高多样性。
- **Table 3**：GenDoP 在 Motion 和 Directorial 字幕条件下全面超越所有基线，CLaTr-CLIP 最高提升 +8.903，用户研究 Alignment 评分最高达 4.693。
- **Table 4**：典型归一化是性能的最关键因素，移除后 CLaTr-CLIP 下降约 21 分；可训练编码器相比冻结编码器在所有指标上均有显著增益。
- **Table S1**：最优超参数为 B=256、N=30、base 规模；大模型在轨迹质量与文本对齐间存在权衡。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/006_Table_3.jpg]]
*Table 3: Quantitative Results. We present the quantitative results of our GenDoP across two text-conditional generation tasks and an RGBD & Text-conditioned task, comparing it with human-tracking methods CCD [22] and E.T. [8], as well as the object/scenecentric method Director3D [26]. Our model consistently outperforms all baselines across all metrics and caption subsets, confirming the effectiveness of both our dataset and auto-regressive framework, positioning GenDoP as a state-of-the-art trajectory generation model*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/002_Table_1.jpg]]
*Table 1: DataDoP Dataset. We compare the DataDoP dataset to other datasets containing camera trajectories. DataDoP is a large dataset focusing on artistic, free-moving trajectories, each accompanied by high-quality caption annotations. The provided captions detail the camera movements, their interactions with scene content, and the underlying directorial intent. To capture more intricate camera movements, each video clip spans 10-20 seconds, averaging 14.4 seconds*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/004_Figure_2.jpg]]
*Figure 2: Dataset Statistics. (a) The figure illustrates the composition and distribution of 27 translation motions (left) and 7 rotation motions (right), emphasizing the complexity and diversity of trajectories in our DataDoP dataset. (b) Based on the same caption, our dataset includes diverse trajectories that still conform to the given caption. As shown in the figure, the trajectories exhibit variations in terms of length, direction, and speed, effectively showcasing the diversity within our dataset*

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative Results of Text-conditioned Trajectory Generation. We offer a comparative analysis of text-conditioned trajectory generation in the figure. Our model’s trajectories (color-coded to highlight text alignment) remain stable and closely follow the instructions, while other models exhibit significant jitter or fail to match the instructions well*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/003_Figure.jpg]]
*Figure: (a) Distribution of Translation and Rotation Motion Tags. (b) Diverse Trajectories*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/013_Figure.jpg]]
*Figure: R3. Tag Distribution. The distribution of Translation and Rotation combinations is shown in the figure. Different tag modes are represented by shades of yellow, ranging from deep to light: Static, Translation only, Rotation only, and both Translation and Rotation*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/014_Figure.jpg]]
*Figure: R4. Caption Generation. We structure the motion tags by incorporating context, instructions, constraints, and examples, and then leverage GPT-4o to generate Motion captions that describe the camera motion alone. Next, we extract 16 evenly spaced frames from the shots to create a 4 × 4 grid, prompting GPT-4o to consider both the previous caption and the image sequence. This enables GPT-4o to generate Directorial captions that describe the camera movement, the interaction between the camera and scene, and the directorial intent*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_07083/figures/008_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 与现有工作的关系

#### 1.1 相对于扩散式轨迹生成方法的定位

GenDoP 的核心贡献在于将相机轨迹生成从扩散范式迁移到自回归序列建模范式，这一转变解决了现有扩散方法的两大瓶颈：轨迹抖动与文本对齐有限。

- **相对于 Director3D**（Li et al., NeurIPS 2024）：Director3D 采用 DiT 架构，以文本为条件在连续空间中生成物体/场景中心的相机轨迹，但其训练数据局限于多视图数据集，缺少自由移动的镜头和体现导演意图的字幕。GenDoP 在生成范式上以自回归 Transformer 取代扩散模型，在数据层面引入 DataDoP（29K 自由移动轨迹 + 运动和导演字幕），在表示层面引入典型归一化与离散 token 化。在公平对比条件下（Director3D 在 DataDoP 上重新训练），GenDoP 在 Motion 字幕条件下的 CLaTr-CLIP 得分（36.179 vs 31.689）和 CLaTr-FID（22.714 vs 31.979）均显著领先（Table 3），验证了自回归范式在稳定性和文本对齐上的优势。

- **相对于 CCD**（Jiang et al., Comput. Graph. Forum 2024）和 **E.T.**（Courant et al., ECCV 2024）：这两类方法聚焦于人像跟踪轨迹生成，依赖角色轨迹作为条件输入，其扩散模型在自由移动场景下泛化能力有限。GenDoP 以文本（运动/导演字幕）和可选的 RGBD 首帧作为条件，不依赖角色轨迹，在用户研究的 Alignment 维度上以 4.693（Motion）和 4.617（Directorial）显著超越最高基线（3.753 / 3.808）（Table 3），表明自回归模型在自由移动轨迹的指令遵循和运动稳定性上具有本质优势。

**因果机制**：扩散模型在连续空间中一步去噪生成完整轨迹，难以捕捉相机运动的时序依赖性和帧间平滑约束，易产生高频抖动；自回归模型将轨迹生成形式化为逐 token 预测，历史位姿通过注意力机制显式约束当前预测，天然具备时序平滑性。

#### 1.2 在自回归生成谱系中的位置

GenDoP 将自回归建模从语言、图像、音频领域拓展到相机轨迹这一结构化连续序列，其关键创新在于：

- **离散化策略**：将连续相机参数（旋转、平移、内参）经典型归一化后压缩至 [0,1] 并离散化为 256 个 bin 的整型 token（Table S1 消融确认该 bin 数最优），使 Transformer 可以直接以分类方式预测下一 token。
- **多模态条件融合**：通过可训练的文本编码器（基于 Stable Diffusion 2.1）和视觉编码器（基于 CLIP Vision Model）分别提取语义、外观和几何特征，拼接为潜在代码 $\mathbf{Z} = [\mathbf{Z}_T; \mathbf{Z}_I; \mathbf{Z}_D]$（Eq. 1），作为自回归解码器的前缀条件。消融实验证实可训练编码器相比冻结编码器在所有指标上带来显著增益（Table 4），表明跨模态对齐对轨迹生成至关重要。

#### 1.3 与相机控制视频生成的关系

GenDoP 定位于“摄影指导”（Director of Photography）角色，为下游视频生成模型提供可控的相机轨迹。论文明确指出 GenDoP 生成的轨迹可应用于 text-to-video 和 image-to-video 生成任务（Figure 1），但当前工作尚未与特定视频生成方法（如 CameraCtrl）进行端到端集成，这构成了一个开放问题。

### 2. 适用边界

#### 2.1 适用场景

- **文本到轨迹生成**：在 Motion Caption 和 Directorial Caption 两种字幕类型下均表现优异，尤其适合需要体现导演意图的自由移动镜头设计。
- **RGBD + 文本到轨迹生成**：当提供首帧 RGBD 图像时，模型能利用几何和外观信息生成与场景结构适配的轨迹（Figure 5 定性结果证实）。
- **轨迹长度**：当前最优设置针对固定长度 N=30 的轨迹（Table S1），适用于中等时长的镜头（DataDoP 平均镜头时长 14.4 秒）。

#### 2.2 适用边界

- **数据集依赖**：模型仅在 DataDoP 数据集上训练，该数据集来源于电影片段，其轨迹风格和镜头类型具有特定的艺术特征。对数据集之外的电影风格或镜头类型的泛化能力尚未验证。
- **轨迹长度灵活性**：当前模型针对固定长度轨迹设计，处理超长或极短镜头时可能需要架构调整。
- **离散化精度**：相机参数离散化为 256 个 bin 虽便于自回归建模，但可能带来量化精度损失，影响细微运动的精确重现。

### 3. 局限与开放问题

#### 3.1 已知局限

1. **轨迹提取噪声**：轨迹提取依赖 MonST3R 的几何估计质量，在高度动态或低纹理场景中可能引入噪声，进而影响训练数据的精度。
2. **字幕偏差**：数据集字幕由 GPT-4o 生成，尽管经过人工验证（Table 2 用户研究显示高质量评分），仍可能存在语言描述偏差或与真实导演意图不完全一致的情况。
3. **文本对齐与轨迹质量的权衡**：超参数消融显示，大模型（large）虽获得最低的 CLaTr-FID（20.474），但 CLaTr-CLIP（33.843）低于 base 模型（36.179）（Table S1），表明模型规模增大可能以牺牲文本对齐为代价换取轨迹平滑性。

#### 3.2 开放问题

1. **显式几何信息的融合**：当前仅使用首帧深度图作为几何条件，如何利用 4D 点云或场景重建等更丰富的显式几何信息进一步增强轨迹生成的空间感知能力，是值得探索的方向。
2. **端到端创作流水线**：如何将 GenDoP 与已有的相机控制视频生成方法统一，实现从文本描述到最终视频的端到端创作流水线，是推动该技术实际应用的关键步骤。
3. **自回归与扩散的混合范式**：是否可能将自回归生成与扩散模型结合，以同时获得自回归的稳定性和扩散的多样性，是一个有潜力的研究方向。
4. **长序列全局连贯性**：如何针对极长序列和复杂多变的导演需求，维持轨迹的全局语义连贯性，需要进一步研究序列建模的架构改进。

## 原文 PDF

![[paperPDFs/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.pdf]]

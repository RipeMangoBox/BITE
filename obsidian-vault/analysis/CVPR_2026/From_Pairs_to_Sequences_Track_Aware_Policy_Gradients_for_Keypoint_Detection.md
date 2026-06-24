---
title: "From Pairs to Sequences: Track-Aware Policy Gradients for Keypoint Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/From_Pairs_to_Sequences_Track_Aware_Policy_Gradients_for_Keypoint_Detection.pdf
project_link: null
code_link: "https://github.com/xiaomi-research/traqpoint"
aliases:
- FPSTAPGKD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将关键点检测重新定义为序列决策问题，利用强化学习直接在图像序列上最大化由 Rank Reward（局部显著性一致性）和 Distinctiveness Reward（全局独特性）合成的轨迹感知奖励，迫使策略网络学会选择在结构显著区域且跨帧高度一致的关键点。
primary_logic: 通过解耦描述符训练与策略学习，使用冻结的描述符提供稳定奖励信号，将优化目标从单对图像的可匹配性转变为整条轨迹的跟踪质量，从而训练出更适用于 3D 视觉 pipeline 的关键点。
claims:
- 序列化 RL 训练相对于成对训练将 MegaDepth AUC@5 提升 2.5，并将平均关键点跟踪长度（AKTL）提升 2.3。
- Rank Reward 和 Distinctiveness Reward 各自对匹配精度和跟踪稳定性有显著贡献（去除后 AUC 降至 52.6 与 54.6，AKTL 降至 4.0 与 5.9）。
- TraqPoint 在 MegaDepth 和 ScanNet 的 AUC@5 上以大幅优势超过最强成对训练方法 RDD。
- MegaDepth-1500 上 AUC@5° = 55.8
---

# From Pairs to Sequences: Track-Aware Policy Gradients for Keypoint Detection

> [!tip] 核心洞察
> 通过解耦描述符训练与策略学习，使用冻结的描述符提供稳定奖励信号，将优化目标从单对图像的可匹配性转变为整条轨迹的跟踪质量，从而训练出更适用于 3D 视觉 pipeline 的关键点。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从图像对到序列：面向关键点检测的轨迹感知策略梯度 |
| 英文题名 | From Pairs to Sequences: Track-Aware Policy Gradients for Keypoint Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20630) · [Code](https://github.com/xiaomi-research/traqpoint) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TraqPoint |
| Dataset | MegaDepth-1500, ScanNet |

> [!tip] 效果简介
> - MegaDepth-1500 上，AUC@5° 55.8 vs 51.9 (RDD) (+3.9)。
> - ScanNet 上，AUC@5° 16.6 vs 13.7 (RDD) (+2.9)。

## 概述

### 问题瓶颈：从“瞬时匹配”到“长期跟踪”的鸿沟

现有关键点检测方法——无论是基于学习的 **SuperPoint**（DeTone et al., CVPR 2018 Workshops）、**DISK**（Tyszkiewicz et al., NeurIPS 2020）、**RIPE**（Kunzel et al., ICCV 2025），还是近期最强的 **RDD**（Chen et al., CVPR 2025）——均在成对图像上训练，优化目标局限于单对图像间的“瞬时匹配性”（pairwise matchability）。然而，在 SLAM、SfM、视觉里程计等实际序列应用中，关键点需要在跨越视角、光照和场景变化的**长序列**中保持稳定可跟踪。这一“长期可跟踪性”（long-term trackability）的缺失，是制约下游三维视觉 pipeline 性能的瓶颈。

### 核心思路：将关键点检测建模为序列决策问题

TraqPoint 将关键点检测重新定义为**序列决策问题**，提出端到端的强化学习框架，直接在图像序列上优化关键点的“轨迹质量”（Track-quality）。其核心洞察是：通过**解耦描述符训练与策略学习**（“先描述，后检测”），利用冻结的描述符分支提供稳定的奖励信号，将优化目标从单对图像的可匹配性转变为整条轨迹的跟踪质量。

### 方法定位：TraqPoint 的三重变革

1. **训练范式变革**：从成对匹配优化转向**序列级轨迹感知 RL 优化**，策略网络在序列中学习选择跨帧高度一致的关键点。
2. **奖励机制变革**：设计复合轨迹奖励——**Rank Reward** 激励关键点在局部邻域内保持高显著性排序一致性，**Distinctiveness Reward** 激励关键点具备全局独特性，二者共同引导策略网络选择结构显著且可重复检测的位置。
3. **架构与训练解耦**：沿用 RDD 的双分支结构，但将特征提取器升级为 **DINOv3-ConvNeXt**；关键点分支作为轻量策略网络（基于 ALIKED 的 4 层卷积设计），描述符分支预训练后冻结，确保奖励信号的稳定性。

### 主要结果：匹配精度与跟踪稳定性的双重突破

在 MegaDepth 相对位姿估计基准上，TraqPoint 以 **AUC@5° = 55.8** 显著超越最强成对训练方法 RDD 的 51.9（+3.9）；在 ScanNet 上同样以 16.6 对 13.7 取得领先（+2.9）。更重要的是，序列化 RL 训练将平均关键点跟踪长度（AKTL）提升 2.3，且消融实验证实 Rank Reward 与 Distinctiveness Reward 各自对匹配精度和跟踪稳定性有不可替代的贡献——去除任一奖励均导致 AUC 和 AKTL 大幅下降。在视觉定位（Aachen Day-Night）、视觉里程计（KITTI）和三维重建（ETH）等序列任务上，TraqPoint 同样展现出全面的性能优势。

## 背景与动机

### 关键点检测：从图像对到序列的范式鸿沟

关键点检测是三维视觉任务（SLAM、SfM、视觉定位）的基础环节，其核心目标是从图像中提取可稳定匹配的稀疏特征点。长期以来，无论是基于手工描述符的方法（如 SIFT）还是基于深度学习的方法（如 **SuperPoint**，DeTone et al., CVPR 2018 Workshops；**ALIKED**，Zhao et al., IEEE TIM 2023），其训练范式都建立在**成对图像匹配**之上：模型学习在两幅图像之间寻找外观相似、几何一致的对应点。

这种“成对训练”范式的优化目标本质上是**瞬时匹配性**（pairwise matchability）——即关键点在两张图像之间能否被正确匹配。然而，在 SLAM 或 SfM 等实际应用中，关键点需要在**跨越数十甚至数百帧的长序列**中持续被跟踪，经历显著的视角变化、光照变化和遮挡。成对训练无法直接优化这种**长期可跟踪性**（long-term trackability），导致关键点在序列中频繁丢失或漂移，最终损害下游任务的精度与鲁棒性。

### 现有方法的瓶颈：奖励信号与优化目标的错位

少数工作尝试将强化学习引入关键点检测，例如 **DISK**（Tyszkiewicz et al., NeurIPS 2020）和 **RIPE**（Kunzel et al., ICCV 2025），但它们仍局限于成对训练框架：DISK 以成对内点率作为奖励，RIPE 以极线约束下的内点率作为奖励。这些奖励信号本质上衡量的仍然是两帧之间的匹配质量，并未触及“关键点能否在整条轨迹上稳定存活”这一核心问题。

更深层的问题在于**描述符训练与关键点检测的耦合**。传统方法通常将描述符和关键点检测器端到端联合训练，但描述符的学习目标（跨帧匹配）与关键点的选择目标（长期跟踪）并不完全一致。这种耦合导致奖励信号不稳定，难以引导策略网络学习到真正有利于序列跟踪的关键点分布。

### TraqPoint 的动机：将跟踪质量作为一阶优化目标

本文的核心动机是弥合上述范式鸿沟。我们提出一个根本性的视角转换：**将关键点检测重新定义为序列决策问题**，并引入强化学习框架直接在图像序列上优化关键点的“轨迹质量”（Track-quality）。这一框架的关键创新在于：

1. **解耦描述符与策略学习**：冻结预训练的描述符分支，为策略网络提供稳定、一致的奖励信号，避免联合训练中的目标冲突。
2. **设计轨迹感知的复合奖励**：奖励函数由两部分构成——**Rank Reward**（局部显著性一致性）激励策略选择在局部邻域内跨帧保持高显著性的点；**Distinctiveness Reward**（全局独特性）激励选择具有全局区分度的点，避免重复或模糊区域。
3. **序列级优化目标**：策略网络不再最大化单对图像的匹配得分，而是最大化整条轨迹上关键点的累积跟踪奖励，从而直接优化长期可跟踪性。

通过这一范式转换，TraqPoint 能够生成在结构显著区域且跨帧高度一致的关键点，从根本上提升下游序列任务（位姿估计、视觉里程计、三维重建）的性能。

## 核心创新

TraqPoint 的核心创新在于**将关键点检测从“成对匹配性优化”重新定义为“序列级可跟踪性优化”**，并通过强化学习框架实现这一范式转变。以下从四个关键维度展开分析。

### 1. 训练范式：从成对匹配到序列决策

现有关键点检测方法（包括基于强化学习的 DISK 和 RIPE）均在成对图像上训练，优化目标本质上是“瞬时匹配性”——即两帧之间特征点的可匹配程度。这一范式存在根本性瓶颈：**成对可匹配性无法保证关键点在长序列中跨越视角、光照和场景变化时的长期可跟踪性**，导致在 SLAM、SfM 等序列应用中性能退化。

TraqPoint 将关键点检测重新定义为序列决策问题：给定一个图像序列，策略网络需要在参考帧上选择一组关键点，使得这些关键点在整个序列中能够被稳定跟踪。这一范式转变使得优化目标从“两帧之间的匹配质量”提升为“整条轨迹的跟踪质量”，直接对齐下游序列应用的真实需求。消融实验表明，仅将训练从成对切换为序列化 RL，即可在 MegaDepth 上将 AUC@5 提升 2.5，并将平均关键点跟踪长度提升 2.3（Table 5），验证了范式转变的独立贡献。

### 2. 奖励机制：从匹配内点率到轨迹感知复合奖励

成对 RL 方法（如 DISK）通常使用匹配内点数量作为奖励信号，其局限性在于：内点率高仅反映两帧间的几何一致性，无法区分关键点是否位于结构显著区域，也无法保证跨帧的重复检测性。

TraqPoint 设计了由两个互补信号合成的**轨迹感知复合奖励**：

- **Rank Reward（排名奖励）**：利用冻结的描述符分支，计算关键点在目标帧 saliency map 中的排序百分位。若该关键点在其局部邻域内保持高显著性（超过阈值 $\tau_{\mathrm{rank}}$），则获得正奖励。该机制激励策略网络选择在结构显著区域且跨帧高度一致的关键点，增强可重复检测性。

- **Distinctiveness Reward（独特性奖励）**：基于描述符的最近邻距离比测试。若关键点描述符与其最近邻的距离比低于阈值 $\tau_{\mathrm{dist}}$，说明该点具有全局独特性，易于跨帧匹配。该机制抑制选择纹理模糊或重复模式区域的关键点。

两种奖励的互补性在消融实验中得到了明确验证：去除 Rank Reward 后 AUC 降至 52.6、AKTL 降至 4.0；去除 Distinctiveness Reward 后 AUC 降至 54.6、AKTL 降至 5.9（Table 5）。Rank Reward 对跟踪稳定性的贡献更为显著，而 Distinctiveness Reward 对匹配精度的提升更为关键。

### 3. 训练耦合：描述符与策略网络的解耦

传统关键点检测方法通常将描述符与检测器联合训练或端到端优化。TraqPoint 采用**“先描述后检测”的范式**：描述符分支在 MegaDepth 上使用 Focal Loss 预训练后完全冻结，仅策略网络（关键点分支）通过 RL 进行训练。

这一设计的关键优势在于：冻结的描述符提供**稳定且无偏的奖励信号**，避免了联合训练中描述符与检测器相互适应导致的奖励漂移问题。描述符的预训练目标（匹配性）与 RL 奖励（可跟踪性）形成互补——描述符负责提供可靠的视觉相似度度量，策略网络负责在此基础上选择最优关键点集合。

### 4. 架构与采样策略的协同改进

在架构层面，TraqPoint 继承了 RDD 的双分支结构，但将特征提取器从 ResNet-50 替换为 **DINOv3-ConvNeXt**，利用更强的预训练视觉表征提升底层特征质量。关键点分支保持 ALIKED 的轻量级 4 层卷积设计，其最后的 1×1 卷积层作为策略头输出关键点概率分布。

在采样策略上，TraqPoint 提出了**混合采样机制**：结合全局 Top-K 采样（利用当前策略选择高置信度关键点）和网格采样（保证空间覆盖多样性），在利用与探索之间取得平衡。这一设计对于 RL 训练的稳定性至关重要——纯 Top-K 采样容易导致策略过早收敛到局部最优，而网格采样确保了对图像所有区域的充分探索。

## 整体框架

TraqPoint 将关键点检测重新定义为**序列决策问题**，其核心 pipeline 遵循“先描述、后检测”（describe‑then‑detect）的范式，由两条解耦的分支构成：

1. **描述符分支（Descriptor Branch）**：预训练并冻结的特征提取网络，为下游奖励计算提供稳定、一致的描述符信号。该分支采用 DINOv3‑ConvNeXt 作为骨干，通过 Focal Loss 在正对应关系上完成预训练后，参数在整个策略学习阶段保持冻结。
2. **策略网络（Keypoint Branch / Policy Network）**：继承自 ALIKED 的轻量级 4 层卷积设计，其最后一层 1×1 卷积作为策略头（policy head），输出全图逐像素的关键点概率分布 $P_\theta$，并据此进行关键点采样。

### 序列感知的策略学习流程

整体训练流程（图 3）围绕“轨迹感知奖励最大化”展开，输入为一段图像序列，输出为在参考帧上采样得到的关键点集合及其对应的策略梯度更新。具体步骤为：

1. **参考帧选取与混合采样**：从输入序列中选定一帧作为参考帧，在其上执行**混合采样（Hybrid Sampling）**——结合全局 Top‑K 采样与网格采样，在保证高响应区域利用的同时维持空间覆盖的探索性，生成候选关键点集 $\mathcal{A}$。
2. **几何映射与可见性统计**：利用已知的深度与相机位姿，将参考帧上的每个候选关键点映射到序列中其他帧，统计各关键点在整条序列中的可见帧集合 $\mathcal{V}_i$。
3. **逐帧奖励计算**：对每个可见帧 $t \in \mathcal{V}_i$，分别计算两项互补奖励：
   - **排名奖励（Rank Reward）** $R_{\mathrm{rank},i}^{t}$：衡量关键点在目标帧局部显著性排序中的跨视图一致性，鼓励策略选择在结构显著区域可重复检测的点。
   - **独特性奖励（Distinctiveness Reward）** $R_{\mathrm{dist},i}^{t}$：基于描述符最近邻距离比，惩罚与周围区域过于相似的点，增强全局独特性。
4. **轨迹奖励聚合**：将逐帧奖励在可见帧上取平均，得到该关键点的最终轨迹奖励 $R_i = \frac{1}{|\mathcal{V}_i|} \sum_{t\in\mathcal{V}_i} R_i^t$。
5. **策略优化**：以轨迹奖励为权重，通过策略梯度损失、空间熵正则化项和预热损失构成的复合损失函数 $\mathcal{L}(\theta)$ 更新策略网络参数。

### 输入输出与模块关系

- **输入**：一段固定长度（最优为 5 帧）的图像序列，以及对应的深度图和相机位姿（仅训练阶段需要，用于几何映射）。
- **输出**：策略网络在参考帧上生成的关键点概率分布，经采样后得到最终的关键点位置集合。
- **模块解耦关系**：描述符分支与策略网络完全解耦——前者提供冻结的奖励信号，后者仅依据该信号通过强化学习优化关键点的长期可跟踪性。这种设计避免了端到端联合训练中描述符与检测器相互干扰的问题，使优化目标从“单对图像的可匹配性”转变为“整条轨迹的跟踪质量”。

> **需要手动核实的细节**：论文未明确说明推理阶段是否仍需描述符分支参与（例如是否在推理时也需计算描述符用于匹配），以及混合采样中全局采样与网格采样的具体比例分配。

### 补充图表

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/002_Figure_2.jpg]]
*Figure 2: Following the architectural design of RDD [5], we adopt an identical network structure. Specifically, we replace the feature extractor employed in RDD [5] with DINOv3-ConvNeXt [45]. The keypoint branch serves as the policy network (πθ)*

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our proposed Sequence-Aware Keypoint Policy Learning framework: First, we select a reference frame from the input image sequence and perform hybrid keypoint sampling on it. Next, we leverage geometric mapping to locate the corresponding positions of the reference frame’s keypoints in other frames of the sequence. We then count the number of these keypoints visible across the entire sequence. After that, we compute per-frame rewards for each sampled point and aggregate these into a final track reward. Finally, we update the policy network’s gradients*

## 核心模块与公式推导

### 3.1 描述符分支预训练

TraqPoint 采用“先描述再检测”（describe-then-detect）的训练范式。描述符分支首先在 MegaDepth 数据集上进行预训练，随后参数被冻结，为后续的策略学习提供稳定的奖励信号。

描述符分支的预训练使用 Focal Loss，仅对真实匹配对 $\mathcal{M}_{gt}$ 中的正对应关系进行优化：

$$
\mathcal{L}_{desc} = -\frac{1}{|\mathcal{M}_{gt}|} \sum_{i\in\mathcal{M}_{gt}} \alpha (1-\mathbf{P}_{ii})^\gamma \log(\mathbf{P}_{ii})
$$

其中 $\mathbf{P}_{ii}$ 表示匹配对 $i$ 的预测匹配概率，$\alpha$ 和 $\gamma$ 为 Focal Loss 的标准超参数。该损失函数使描述符网络学会为真实匹配点生成高度一致的描述向量，为后续轨迹奖励计算奠定基础。

### 3.2 策略网络结构

策略网络（关键点分支）沿用 **ALIKED**（Zhao et al., IEEE TIM 2023）的轻量级 4 层卷积设计，其最后一层 $1\times1$ 卷积层作为策略头（policy head），输出关键点的概率分布 $P_\theta$。特征提取器则替换为 **DINOv3-ConvNeXt**，以提供更强的视觉表征能力。

### 3.3 混合采样策略

为平衡强化学习中的利用（exploitation）与探索（exploration），TraqPoint 提出混合采样策略：

- **全局 Top-K 采样**：从策略头输出的概率图中选取得分最高的 $N_g$ 个关键点，保证高质量点的利用。
- **网格采样**：将图像划分为均匀网格，每格选取得分最高的点，共采样 $N_{grid}$ 个点，确保空间覆盖的探索性。

最终采样集合包含 $N = N_g + N_{grid}$ 个关键点，送入后续的轨迹奖励计算流程。

### 3.4 轨迹感知奖励函数

轨迹感知奖励是 TraqPoint 的核心创新，由两个互补信号组成：**排名奖励（Rank Reward）** 和 **独特性奖励（Distinctiveness Reward）**。

#### 3.4.1 排名奖励

排名奖励衡量关键点在跨视图中的局部显著性一致性。给定参考帧中采样点 $\mathbf{x}_i$，通过几何映射找到其在目标帧 $t$ 中的对应位置，计算该位置在目标帧显著性图（由冻结的描述符分支生成）中的排名百分位 $\mathrm{rank.prop}$：

$$
R_{\mathrm{rank},i}^{t} = \max\left(0, \frac{\mathrm{rank.prop} - \tau_{\mathrm{rank}}}{1.0 - \tau_{\mathrm{rank}}}\right)
$$

其中 $\tau_{\mathrm{rank}}$ 为排名阈值。该奖励鼓励策略选择在序列各帧中均保持高局部显著性的点，增强关键点的可重复性。

#### 3.4.2 独特性奖励

独特性奖励通过描述符的最近邻距离比（nearest neighbor ratio）衡量关键点的全局独特性：

$$
R_{\mathrm{dist},i}^{t} = \max\left(0, \frac{\tau_{\mathrm{dist}} - \mathrm{ratio}}{\tau_{\mathrm{dist}}}\right)
$$

其中 $\mathrm{ratio}$ 为目标帧中最近邻与次近邻描述符距离之比，$\tau_{\mathrm{dist}}$ 为独特性阈值。该奖励抑制选择纹理模糊、易混淆的区域，提升关键点的判别力。

#### 3.4.3 轨迹奖励聚合

对于每个采样关键点 $i$，其逐帧奖励在可见帧集合 $\mathcal{V}_i$ 上取平均，得到该点的最终轨迹奖励：

$$
R_i = \frac{1}{|\mathcal{V}_i|} \sum_{t\in\mathcal{V}_i} R_i^t
$$

整个采样动作集 $\mathcal{A}$ 的总奖励 $\mathcal{R}(\mathcal{A})$ 为所有关键点轨迹奖励的均值。

### 3.5 策略优化目标

策略网络 $\pi_\theta$ 的优化目标为最大化期望奖励：

$$
\mathcal{J}(\theta) = \mathbb{E}_{\mathcal{A}\sim P_{\theta}} [\mathcal{R}(\mathcal{A})]
$$

对应的复合损失函数为：

$$
\mathcal{L}(\theta) = -\mathcal{R}(\mathcal{A}) \cdot \left(\frac{1}{N} \sum_{i=1}^{N} \log P_{\theta}(\mathbf{x}_i)\right) - \lambda \mathcal{H}(P_{\theta}) + \alpha_t \mathcal{L}_w
$$

其中：
- 第一项为策略梯度损失，以轨迹奖励 $\mathcal{R}(\mathcal{A})$ 加权对数概率，引导策略向高奖励方向更新。
- 第二项 $\mathcal{H}(P_{\theta})$ 为空间熵正则化项，防止策略过早收敛到局部最优，$\lambda$ 为权重系数。
- 第三项 $\mathcal{L}_w$ 为预热损失（warm-up loss），在训练初期使用成对匹配信号辅助策略收敛，$\alpha_t$ 随训练步数衰减。

## 实验与分析

### 相对位姿估计

TraqPoint 在 MegaDepth-1500 和 ScanNet 两个标准相对位姿估计基准上均以显著优势超越所有对比方法，包括最强成对训练基线 **RDD**（Chen et al., CVPR 2025）。在 MegaDepth 上，TraqPoint 的 AUC@5° 达到 55.8，比 RDD 的 51.9 高出 3.9 个点；在 ScanNet 上，TraqPoint 的 AUC@5° 为 16.6，比 RDD 的 13.7 高出 2.9 个点（Table 1）。这一提升覆盖了不同匹配器（MNN 与 LG）和不同关键点数量设置，表明轨迹感知策略梯度训练出的关键点在跨视角匹配中具有更强的鲁棒性。值得注意的是，TraqPoint 在 MegaDepth 上相对于 **SuperPoint + LG**（DeTone et al., CVPR 2018 Workshops）的 AUC@5° 提升高达 5.9 个点（49.9 → 55.8），进一步验证了序列化 RL 训练范式的有效性。

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/006_Table_1.jpg]]
*Table 1: Comparison on the MegaDepth [23] and ScanNet [8]. Top 4,096 features are used for all sparse matching methods. Best in bold, second best underlined*

### 视觉定位

在 Aachen Day-Night 视觉定位基准上，TraqPoint 在所有日间设置和两个夜间设置中均取得最优召回率（Table 2）。日间场景下，在 0.25m/2° 的最严格阈值下召回率达到 87.9%，比第二名的 85.4% 高出 2.5 个百分点；夜间场景下同样保持领先（85.7% vs. 83.3%）。这表明轨迹感知训练不仅提升了关键点的匹配精度，还增强了其在剧烈光照变化下的长期可跟踪性，直接转化为定位 pipeline 中的召回率增益。

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/005_Table_2.jpg]]
*Table 2: Visual Localization on Aachen day-night [41]. Best in bold, second best underlined*

### 视觉里程计

在 KITTI 序列 01-03 的视觉里程计测试中，TraqPoint 在所有指标上均取得最优（Table 3）。以序列 01 为例，TraqPoint 的平均轨迹误差（ATE）为 29.9m，最大轨迹误差（MTE）为 51.4m，均显著低于 RDD（ATE 36.2m，MTE 59.1m）和其他基线。更重要的是，TraqPoint 的平均关键点跟踪长度（AKTL）达到 7.3，比 RDD 的 5.0 提高了 46%，直观体现了“轨迹感知”训练对关键点跨帧持续性的直接改善。序列 02 和 03 上同样呈现一致趋势，AKTL 分别从 RDD 的 2.6/6.4 提升至 3.8/8.7。

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/008_Table_3.jpg]]
*Table 3: Visual Odometry test results on sequence (01-03) of KITTI [14]. ATE: Average Trajectory Error; MTE: Maximum Trajectory Error; AKTL: Average Keypoint Tracking Length*

### 3D 重建

在 ETH 基准的 3D 重建评估中，TraqPoint 在所有指标上均优于对比方法（Table 4）。其重建出的点云在完整性和精度之间取得了更好的平衡，定性结果（Figure 4）显示 TraqPoint 的关键点更集中于结构显著区域（如建筑边缘、窗户角点），且跨视角一致性更高——成功生成地标的点（蓝色）更多，失败点（红色）更少。这直接源于 Rank Reward 对局部显著性一致性的激励和 Distinctiveness Reward 对全局独特性的筛选，使得关键点在多视角几何验证中更易通过极线约束。

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/007_Table_4.jpg]]
*Table 4: Results on ETH benchmark [44] for 3D reconstruction. Best in bold, second best underlined*

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results on the MegaDepth dataset [23] and the ETH benchmark [44]. For feature matching, keypoints are plotted in orange. Green lines indicate correct matches, while red lines denote incorrect ones. For multi-view reconstruction, keypoints that successfully generate point cloud landmarks are marked in blue; failed ones are marked in red. Our TraqPoint produces keypoints with better structural saliency and high cross-view consistency, which effectively improves feature matching and reconstruction tasks*

### 消融实验

Table 5 的消融实验系统拆解了 TraqPoint 各设计组件的贡献，以 MegaDepth AUC@5° 衡量匹配能力，以 KITTI 序列 01-03 的平均 AKTL 衡量跟踪稳定性。

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/010_Table_5.jpg]]
*Table 5: Ablation study. We report matching capability (AUC@5° on MegaDepth [23]) and tracking stability (average value of AKTL on KITTI [14] sequence 01-03)*

**序列化训练范式的核心作用。** 将成对训练（pairwise）替换为序列化 RL 训练（sequentialization），AUC@5° 从 53.3 提升至 55.8（+2.5），AKTL 从 4.6 提升至 6.9（+2.3）。这直接证实了本文的核心主张：成对优化“瞬时匹配性”无法保证“长期可跟踪性”，而序列感知策略梯度通过直接在轨迹上最大化跟踪质量，使关键点学会选择跨帧高度一致的位置。

**Rank Reward 与 Distinctiveness Reward 的互补性。** 去除 Rank Reward 后，AUC@5° 骤降至 52.6（-3.2），AKTL 降至 4.0（-2.9），说明局部显著性一致性对匹配精度和跟踪稳定性的贡献均极为关键——没有该奖励，策略网络倾向于选择在参考帧显著但在目标帧不显著的点，导致跨帧可重复性大幅下降。去除 Distinctiveness Reward 后，AUC@5° 降至 54.6（-1.2），AKTL 降至 5.9（-1.0），证明全局独特性奖励通过抑制重复纹理区域的歧义匹配，对跟踪稳定性有独立且不可替代的增强作用。两个奖励同时去除（仅保留内点率奖励）时性能最差，验证了二者互补设计的必要性。

**骨干网络的影响。** 将 DINOv3-ConvNeXt 替换为 ResNet-50 后，AUC@5° 降至 52.9（-2.9），AKTL 降至 5.6（-1.3），表明更强的视觉表征能力为奖励计算提供了更准确的 saliency 和描述符信号，间接提升了策略学习的上限。但即使使用 ResNet-50，序列化 RL 训练仍优于成对训练，说明范式改进与骨干升级各自独立贡献。

**超参数敏感性。** Figure 5 展示了训练序列长度和采样关键点数量的消融曲线。最优配置为序列长度 5、采样点数 256。序列过短（如 3）时轨迹信息不足，过长（如 7）时跨帧几何映射误差累积导致奖励信号噪声增大；采样点数过少限制探索，过多则稀释高奖励点的梯度贡献。

### 定性分析

Figure 1 和 Figure 4 从多视角重建和特征匹配两个维度提供了直观对比。在重建场景中，TraqPoint 的关键点密集分布于建筑立面、窗框等结构显著区域，且跨视角一致性好，大部分点成功生成地标（蓝色）；RDD 的关键点则更分散，包含大量在纹理重复或弱纹理区域失败的点（红色）。在匹配场景中，TraqPoint 的正确匹配线（绿色）更密集且分布更均匀，错误匹配线（红色）更少。这些定性结果与定量指标高度一致，共同说明轨迹感知策略梯度使关键点学会了“在哪里检测才能被稳定跟踪”这一 3D 视觉 pipeline 的核心需求。

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/001_Figure_1.jpg]]
*Figure 1: Multi-view reconstruction: Our TraqPoint vs. RDD [5]. Keypoints that successfully generate landmarks are marked in blue. Failed keypoints are marked in red. Our TraqPoint generates more keypoints in structurally significant areas with higher cross-view consistency, yielding more landmarks*

### 补充图表

![[assets/figures/papers/paper_list_l2081_https_arxiv_org_abs_2602_20630/figures/009_Figure_5.jpg]]
*Figure 5: Ablation study on sequence length and the number of sampled keypoints*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

**TraqPoint** 的核心贡献在于将关键点检测从“成对图像匹配”范式迁移至“序列轨迹优化”范式。这一转变使其在方法谱系中处于独特位置：它既继承了基于强化学习的关键点检测思路，又从根本上改变了优化目标与训练信号。

#### 1.1 与成对训练方法的对比

传统关键点检测方法（无论监督还是自监督）均在成对图像上优化“瞬时匹配性”，典型代表包括：

- **SuperPoint**（DeTone et al., CVPR 2018 Workshops）：通过自监督方式在合成数据上训练关键点检测与描述，开创了自监督关键点检测的先河，但其优化目标仅限于单对图像的可匹配性。
- **ALIKED**（Zhao et al., IEEE TIM 2023）：轻量级关键点检测与描述网络，作为 TraqPoint 关键点分支的原型架构，但其训练范式仍为成对匹配。
- **RDD**（Chen et al., CVPR 2025）：当前最强的成对训练基线，与 TraqPoint 共享相同的网络结构设计，但采用监督训练方式优化成对匹配精度。TraqPoint 在 MegaDepth 上将 AUC@5 从 RDD 的 51.9 提升至 55.8（+3.9），在 ScanNet 上从 13.7 提升至 16.6（+2.9）——这些增益直接来源于训练范式的转变，而非网络架构的改进。

TraqPoint 与 RDD 的对比尤为关键：二者架构相同，唯一差异在于训练方式（序列 RL vs. 成对监督），因此性能提升可干净地归因于“序列化”训练范式。消融实验进一步证实：将成对训练替换为序列 RL 训练后，MegaDepth AUC@5 提升 2.5，平均关键点跟踪长度（AKTL）提升 2.3（Table 5）。

#### 1.2 与基于强化学习的关键点检测方法对比

在强化学习路线上，TraqPoint 的直接前驱包括：

- **DISK**（Tyszkiewicz et al., NeurIPS 2020）：首次将 RL 引入关键点检测，使用“器内点数”（inlier count）作为奖励信号。但其奖励定义在成对匹配上，无法捕捉跨多帧的跟踪稳定性。
- **RIPE**（Kunzel et al., ICCV 2025）：无监督 RL 关键点检测器，使用极线约束下的内点率作为奖励。同样局限于成对几何约束，未涉及序列级优化。

TraqPoint 与上述方法的本质区别在于 **奖励函数的设计维度**：
- DISK/RIPE 的奖励信号来自“两帧之间的匹配质量”；
- TraqPoint 的奖励信号来自“多帧轨迹上的可跟踪性”，由 Rank Reward（局部显著性跨视图一致性）和 Distinctiveness Reward（全局独特性）复合而成。

这一差异使得 TraqPoint 能够显式优化关键点的长期跟踪稳定性，而非仅追求单对匹配精度。消融实验表明，Rank Reward 和 Distinctiveness Reward 各自对匹配精度和跟踪稳定性有显著贡献：去除 Rank Reward 后 AUC 降至 52.6、AKTL 降至 4.0；去除 Distinctiveness Reward 后 AUC 降至 54.6、AKTL 降至 5.9（Table 5）。

#### 1.3 “描述-后检测”范式定位

TraqPoint 采用“describe-then-detect”训练范式：先预训练描述符分支并冻结参数，再在此冻结描述符提供的稳定奖励信号下训练策略网络（关键点分支）。这与端到端联合训练的描述-检测方法形成对比：
- **联合训练方法**（如 SuperPoint、RDD）同时优化描述符与关键点检测器，描述符质量与关键点选择相互耦合；
- **TraqPoint** 的解耦设计使得奖励信号不受描述符训练波动的影响，策略网络可以专注于“在已有描述空间中选择最可跟踪的点”。

这一设计选择的技术合理性在于：描述符的“描述能力”和关键点的“可跟踪性”是两个可分离的目标，冻结描述符后，RL 策略只需学习“选择”而非同时学习“描述”。

### 2. 适用边界

**适用场景**：
- 需要跨多帧跟踪关键点的序列化 3D 视觉任务，如 SLAM、SfM、视觉里程计、多视图重建；
- 对关键点长期稳定性和结构显著性要求较高的应用；
- 训练时可获取图像序列及相机位姿/深度真值（用于几何映射计算对应位置）。

**不适用或未验证的场景**：
- 仅需成对匹配的独立图像检索或单对拼接任务——此时序列级优化的收益可能有限，且引入的序列训练开销未必划算；
- 无法获取序列数据或几何真值的场景——当前 TraqPoint 依赖已知相机位姿和深度图来计算关键点在其他帧中的对应位置，这限制了其在无真值数据上的直接应用；
- 实时性要求极高的嵌入式场景——尽管关键点分支采用轻量级设计（4层卷积），但 DINOv3-ConvNeXt 特征提取器计算量较大，论文未提供推理延迟数据。

### 3. 局限与开放问题

**已确认的局限**：
- 论文未明确列出方法局限（limitations 字段为空），但可从方法设计中推断：TraqPoint 的训练依赖序列几何真值（深度+位姿），这限制了其在无真值数据上的扩展性。

**开放问题**（来自论文分析）：

1. **自监督序列奖励构建**：能否在无需深度与相机位姿真值的场景下，通过自监督信号（如多视图光度一致性）构建序列奖励？这将显著扩展 TraqPoint 范式的适用范围。

2. **范式拓展至密集任务**：Track-Aware Policy Gradient 范式能否拓展至密集匹配或光流估计任务？这些任务同样面临长序列一致性问题，但动作空间从离散关键点选择变为连续/密集预测，需要重新设计策略参数化与奖励函数。

3. **特征提取器依赖**：TraqPoint 的性能增益部分来自 DINOv3-ConvNeXt 替换 ResNet-50（Table 5 消融显示骨干网络替换贡献了 AUC 从 52.5 到 53.3 的提升），但论文未完全解耦“序列 RL 训练”与“更强骨干网络”各自的贡献比例。这一交互效应值得进一步量化分析。

4. **序列长度与计算开销的权衡**：消融实验表明最优训练序列长度为 5（Figure 5），但更长序列是否能在更大时间跨度上进一步提升跟踪稳定性，同时引入多少计算开销，尚未探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/From_Pairs_to_Sequences_Track_Aware_Policy_Gradients_for_Keypoint_Detection.pdf]]
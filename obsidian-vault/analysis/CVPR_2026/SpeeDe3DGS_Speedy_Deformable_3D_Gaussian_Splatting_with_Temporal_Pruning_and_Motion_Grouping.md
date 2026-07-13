---
title: "SpeeDe3DGS: Speedy Deformable 3D Gaussian Splatting with Temporal Pruning and Motion Grouping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpeeDe3DGS_Speedy_Deformable_3D_Gaussian_Splatting_with_Temporal_Pruning_and_Motion_Grouping.pdf
project_link: "https://speede3dgs.github.io"
code_link: null
aliases:
- SpeeDe3DGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 减少需要形变推理的高斯原语数量（通过剪枝移除冗余原语）和降低每个原语的推理成本（通过分组共享SE(3)形变）。
primary_logic: 通过对高斯原语的时序敏感性进行聚合分析，可以在保持视觉质量的前提下移除大量低贡献原语；将神经形变场蒸馏为分组的SE(3)刚性变换，能在几乎不损失精度的情况下大幅降低形变推理的成本。
claims:
- 在NeRF-DS数据集上，集成TSP、TSS和GroupFlow的完整SpeeDe3DGS实现10.68×渲染加速（505.60 FPS），而PSNR仅下降0.14 dB（23.66 vs 23.80）。
- 在MonoDyGauBench的50个动态场景上，DeformableGS+GroupFlow实现13.71×渲染加速和2.53×训练加速。
- TSP+TSS在NeRF-DS bell场景中将高斯数量减少11×，同时SSIM高于未剪枝的DeformableGS基线（0.8838 vs 0.8781）。
- 单独使用TSP在HyperNeRF上实现9.37×渲染加速，GroupFlow单独实现15.66×加速，两者结合达到29.21×加速。
---

# SpeeDe3DGS: Speedy Deformable 3D Gaussian Splatting with Temporal Pruning and Motion Grouping

> [!tip] 核心洞察
> 通过对高斯原语的时序敏感性进行聚合分析，可以在保持视觉质量的前提下移除大量低贡献原语；将神经形变场蒸馏为分组的SE(3)刚性变换，能在几乎不损失精度的情况下大幅降低形变推理的成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpeeDe3DGS：基于时间修剪与运动分组的快速可变形3D高斯泼溅 |
| 英文题名 | SpeeDe3DGS: Speedy Deformable 3D Gaussian Splatting with Temporal Pruning and Motion Grouping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.07917) · [Project](https://speede3dgs.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SpeeDe3DGS |
| Dataset | NeRF-DS, MonoDyGauBench, HyperNeRF |

> [!tip] 效果简介
> - NeRF-DS 上，FPS (RTX 3090) 505.60 (10.68×) vs 54.37 (DeformableGS) (+451.23 (9.29× 绝对提升))；高斯数量 11.10K (减少 11.91×) vs 132.22K (DeformableGS) (-121.12K)；训练时间 (s) 625.48 (加速 2.44×) vs 1523.83 (DeformableGS) (-898.35)。
> - MonoDyGauBench (50 scenes) 上，FPS (RTX 3090) 276.91 (13.71×) vs 20.20 (DeformableGS) (13.71×)。
> - HyperNeRF (8 scenes) 上，FPS (RTX 3090) 260.05 (23.84×) vs 10.91 (DeformableGS) (23.84×)。

## 概要

动态3D高斯泼溅（3DGS）方法通过对每一帧、每一个高斯原语执行神经网络形变推理来建模场景运动，导致渲染计算开销极大。以**DeformableGS**为代表的基线方法虽然重建质量优异，但渲染速度远低于实时交互需求，这构成了本文的核心瓶颈。

SpeeDe3DGS针对上述瓶颈提出了两个因果性调控手段：**减少需要形变推理的高斯原语数量**与**降低每个原语的形变推理成本**。其核心洞察在于：通过对高斯原语的时序敏感性进行聚合分析，可以在保持视觉质量的前提下移除大量低贡献原语；同时，将逐高斯的神经形变场蒸馏为分组的SE(3)刚性变换，能在几乎不损失精度的情况下大幅降低形变推理开销。

基于此，方法体系由三个模块构成——**时序敏感性剪枝（TSP）** 计算时序敏感度分数并定期剪除低分高斯，**时序敏感性采样（TSS）** 在敏感度估计时对时间戳注入线性退火的高斯噪声以抑制浮空伪影，以及**GroupFlow运动分组**通过轨迹相似度聚类将高斯分配到共享SE(3)变换的运动组中。三者协同实现了原语数量与单原语推理成本的双重压缩。

在NeRF-DS真实世界动态数据集上，完整SpeeDe3DGS实现**10.68×渲染加速**（505.60 FPS），PSNR仅下降0.14 dB（23.66 vs 23.80），高斯数量减少11.91×，训练时间加速2.44×。在涵盖50个动态场景的MonoDyGauBench基准上，DeformableGS+GroupFlow实现13.71×渲染加速和2.53×训练加速。单独使用TSP在HyperNeRF上实现9.37×渲染加速，GroupFlow单独实现15.66×加速，两者结合达到29.21×加速。值得注意的是，TSP+TSS在NeRF-DS bell场景中将高斯数量减少11×的同时，SSIM反而高于未剪枝的DeformableGS基线（0.8838 vs 0.8781），验证了时序敏感性剪枝不仅压缩模型，还能通过移除时间不稳定的高斯来提升渲染质量。

方法定位上，SpeeDe3DGS属于动态3DGS加速方向，以DeformableGS（基于MLP的神经形变场）为主要基线直接扩展，同时与4DGS（基于HexPlane网格的神经形变）和RTGS（隐式4D高斯表示）形成对比。其贡献在于首次将梯度敏感度剪枝从静态场景泛化到时序动态场景，并提出了神经形变到分组刚性变换的蒸馏范式，在实时渲染速度与重建质量之间取得了显著的帕累托改进。

**局限性**方面，该方法继承了动态3DGS基线对高度非刚性运动场景的建模挑战；GroupFlow通过共享刚性变换建模非刚性运动，在极度变形区域可能不够灵活；训练与评测在不同GPU上进行，存在硬件差异导致的对比公平性风险（论文已明确标注测量GPU）。



### 动态3DGS的效率瓶颈

3D高斯泼溅（3DGS）在静态场景的新视角合成中实现了实时渲染，但将其扩展到动态场景时，现有方法面临严重的效率问题。以**DeformableGS**为代表的神经形变方法，对每一帧、每一个高斯原语都需要执行MLP形变推理，导致计算开销极大，渲染速度远低于实时要求。这种逐原语、逐帧的密集推理构成了动态3DGS的核心效率瓶颈。

具体而言，DeformableGS在NeRF-DS数据集上的渲染速度仅为54.37 FPS（RTX 3090），在HyperNeRF上更是低至10.91 FPS，且模型存储量高达132.22K个高斯原语。这种低效源于两个相互耦合的因素：一是原语数量庞大且缺乏针对性筛选，大量对动态场景贡献微弱的高斯仍参与形变计算；二是形变表示本身计算密集——每个高斯独立通过MLP预测位移和旋转，无法利用场景中广泛存在的运动相似性。

### 现有方法的缺口

当前动态3DGS的加速尝试存在明显不足。基于HexPlane网格的**4DGS**虽然结构规整，但渲染速度仍远未达到实时交互需求。**RTGS**等隐式4D表示方法追求极致速度，却以牺牲视觉质量为代价。更为关键的是，现有方法缺乏对“哪些高斯真正需要形变”这一问题的系统回答——所有原语被无差别地送入形变网络，忽视了动态场景中大量高斯在时间维度上几乎静止或贡献极低的事实。

另一方面，场景中相邻区域的高斯往往共享相似的运动模式（如刚体部件的整体位移），但逐高斯的独立形变表示完全无法利用这种结构先验，造成了冗余计算。将运动表示从“逐原语”提升到“分组共享”的粒度，是突破效率瓶颈的自然思路，但如何在不牺牲精度的前提下实现这一蒸馏，此前未有有效方案。

### 本文动机与核心思路

SpeeDe3DGS的动机直接针对上述两个缺口：**减少需要形变推理的高斯数量**，以及**降低每个原语的形变推理成本**。

第一条路径通过**时间敏感性剪枝（Temporal Sensitivity Pruning, TSP）**实现。核心洞察在于：高斯原语对动态重建的贡献可以通过其在时间维度上的聚合梯度来量化——如果某个高斯在所有训练时间戳上的投影梯度都很小，说明它对场景运动的刻画几乎无影响，可以被安全移除。这一思想将静态场景的梯度敏感性分析推广到时域，同时引入**时间敏感性采样（Temporal Sensitivity Sampling, TSS）**对时间戳注入扰动，以探查邻近运动状态，暴露时间不稳定的浮空伪影。

第二条路径通过**GroupFlow**实现：将MLP形变场蒸馏为分组的SE(3)刚性变换。方法首先基于轨迹相似度将高斯聚类到若干运动组，然后利用Umeyama对齐为每组估计从规范帧到各时间戳的刚性变换。形变推理从“逐高斯MLP前传”简化为“逐组SE(3)作用”，在几乎不损失精度的情况下大幅降低计算量。

两条路径协同作用：剪枝移除了冗余原语，为GroupFlow提供了更紧凑、运动更一致的高斯集合；GroupFlow的共享刚性变换进一步压缩了形变表示。在HyperNeRF上，单独TSP+TSS实现9.37×渲染加速，单独GroupFlow实现15.66×加速，两者结合达到29.21×加速（Table 9），验证了“剪枝+分组”这一组合策略的有效性。



## 核心方法与创新机理

SpeeDe3DGS 围绕“减少形变推理开销”这一核心瓶颈，在 **DeformableGS** 基线上引入了两条正交且可叠加的创新路径：**原语级剪枝**与**运动表示蒸馏**。二者分别从“推理哪些高斯”和“如何推理其运动”两个维度切入，共同实现了数量级的渲染加速。

### 1. 时序敏感度驱动的原语剪枝（TSP + TSS）

DeformableGS 对每一帧的所有高斯原语执行逐高斯的 MLP 形变推理，计算成本与高斯数量呈线性关系。SpeeDe3DGS 的核心洞察在于：**动态场景中存在大量运动冗余或时间不稳定的高斯原语，可在几乎不影响视觉质量的前提下被移除**。

**时序敏感度剪枝（TSP）** 将基于梯度的敏感度分析从静态 3DGS 推广到动态域。其关键机制是计算 L2 重建损失对每个高斯投影贡献的二阶敏感度，并在所有训练视图和时间步上聚合：

$$\tilde{U}_{\mathcal{G}_i} \approx \nabla_{g_i}^2 L_2 \approx \sum_{\phi, t \in \mathcal{P}_{gt}} \left( \nabla_{g_i} I_{\mathcal{G}_t}(\phi) \right)^2$$

当训练收敛、残差项可忽略时，剪枝分数简化为图像空间梯度的平方和，直接反映高斯在**时空上的累计贡献**。分数低的高斯意味着其存在与否对重建结果影响甚微，可被安全剪除。

**时序敏感度采样（TSS）** 是 TSP 的关键增强。标准 TSP 仅在训练时间戳上评估敏感度，无法探查高斯在邻近运动状态下的稳定性。TSS 在形变函数的时间戳输入上注入线性退火的高斯噪声：

$$\mathcal{X}(i) = \mathcal{N}(0, 1) \cdot \beta \cdot \Delta t \cdot (1 - i / \tau)$$

这一扰动迫使模型在邻近运动状态下评估敏感度，有效暴露那些仅在特定时间戳“侥幸”高响应、但在时间邻域内不稳定的“浮空”高斯。消融实验表明，TSP+TSS 在 NeRF-DS 的 bell 场景中将高斯数量减少 **11×**，同时 SSIM **高于**未剪枝的 DeformableGS 基线（0.8838 vs 0.8781），并显著抑制了时间闪烁和浮空伪影（Figure 3）。

**与静态剪枝的本质区别**：传统基于不透明度或尺度的剪枝无法感知时间维度的冗余——一个在多数帧“隐身”但在关键帧“闪现”的高斯可能被误删。TSP 的时序聚合机制天然规避了这一问题，TSS 则进一步强化了对时间不稳定原语的识别能力。

### 2. 从逐高斯 MLP 到分组 SE(3) 的运动蒸馏（GroupFlow）

DeformableGS 使用 MLP 为每个高斯独立预测形变，这是渲染速度的主要瓶颈。GroupFlow 的核心思想是：**场景中空间邻近的高斯往往共享相似的运动轨迹，可以用分组共享的 SE(3) 刚性变换替代逐高斯的神经网络推理**。

GroupFlow 分两步实现这一蒸馏：

**运动分组**：首先通过最远点采样选取 $J$ 个控制点，然后基于轨迹相似度将每个高斯分配到运动最相似的控制点组。相似度度量同时考虑了时间残差的标准差和均值：

$$S_{i,j} = \lambda_r \mathrm{std}_t(\| \mu_i^t - h_j^t \|) + (1 - \lambda_r) \mathrm{mean}_t(\| \mu_i^t - h_j^t \|)$$

**SE(3) 运动估计**：对每个组，利用 Umeyama 对齐在采样的均值上估计从规范帧到时间 $t$ 的刚性变换 $[R_j^t | T_j^t]$。变形后的均值和旋转分别由组的刚性变换直接计算：

$$\mu_i^t = R_j^t (\mu_i^0 - h_j^0) + h_j^0 + T_j^t$$

$$r_i^t = \mathrm{quat}\big(R_j^t \mathrm{mat}(r_i^0)\big)$$

这一设计将形变推理的计算复杂度从 $\mathcal{O}(N \cdot C_{\text{MLP}})$ 降至 $\mathcal{O}(J \cdot C_{\text{SE(3)}})$，其中 $J \ll N$（默认 $J=2048$）。在 HyperNeRF 上，单独使用 GroupFlow 即实现 **15.66×** 渲染加速；与 TSP+TSS 结合后达到 **29.21×**，而 PSNR 仅从 24.63 降至 24.40（Table 9）。

### 3. 两条路径的协同效应

TSP+TSS 和 GroupFlow 解决的是**不同维度**的效率瓶颈：前者减少需要推理的原语数量，后者降低每个原语的推理成本。二者叠加产生乘法效应——在 NeRF-DS 上，完整 SpeeDe3DGS（TSP+TSS+GF）实现 **10.68×** 渲染加速（505.60 FPS vs 54.37 FPS），高斯数量减少 **11.91×**，训练时间缩短 **2.44×**，而 PSNR 仅下降 0.14 dB（Table 1）。在 MonoDyGauBench 的 50 个动态场景上，DeformableGS + GroupFlow 实现 **13.71×** 渲染加速和 **2.53×** 训练加速（Table 2）。

**关键设计选择**：剪枝采用“软剪枝 60% + 硬剪枝 30%”的两阶段策略（Figure 5），在稠密化阶段软剪枝保留模型探索能力，稠密化后硬剪枝最大化推理效率。GroupFlow 的 $J=2048$ 在视觉质量与模型紧凑性之间取得最佳平衡（Table 10）。

### 4. 局限性

GroupFlow 通过共享刚性变换建模非刚性运动，在极度变形区域可能不够灵活。增加 $J$ 可缓解此问题，但固定分组数存在建模能力上限。此外，方法继承了动态 3DGS 基线对高度非刚性运动和噪声相机位姿的敏感性。



SpeeDe3DGS 是一个面向动态3D高斯泼溅（3D Gaussian Splatting, 3DGS）的加速框架，其核心目标是解决现有可变形3DGS方法（如 **DeformableGS**）中逐高斯、逐帧的神经网络形变推理带来的巨大计算开销。该框架通过两条正交的加速路径——**原语精简**与**运动表示简化**——在保持视觉质量的前提下实现数量级的渲染与训练加速。

### 核心洞察

动态3DGS场景中存在大量对最终渲染贡献极低的冗余高斯原语，这些原语在时间维度上持续消耗形变推理和光栅化资源。同时，神经形变场（通常为MLP）为每个高斯独立预测位移和旋转的方式存在严重的计算冗余：场景中许多高斯原语的运动模式高度相似，可以被共享的刚性变换近似。SpeeDe3DGS 正是围绕这两个瓶颈展开设计：通过时序敏感度分析识别并剪除低贡献高斯，再通过运动分组将逐高斯的神经形变蒸馏为分组的 SE(3) 刚性变换。

### 方法概览

SpeeDe3DGS 由三个核心模块构成，按训练流程顺序集成于 DeformableGS 基线之上：

1. **Temporal Sensitivity Pruning (TSP)**：在训练过程中定期计算每个高斯的时序敏感度分数，并剪除分数最低的高斯原语。敏感度分数基于 L2 重建损失对高斯投影贡献的二阶敏感度，聚合所有训练视图和时间步，反映高斯在时空上的累计重要性。当训练收敛、残差项可忽略时，该分数简化为图像空间梯度的平方和：
   $$\tilde { U } _ { \mathcal { G } _ { i } } \approx \nabla _ { g _ { i } } ^ { 2 } L _ { 2 } \approx \sum _ { \phi , t \in \mathcal { P } _ { g t } } \left( \nabla _ { g _ { i } } I _ { \mathcal { G } _ { t } } ( \phi ) \right) ^ { 2 }$$

2. **Temporal Sensitivity Sampling (TSS)**：在敏感度估计阶段，对形变函数的时间戳输入注入线性退火的高斯噪声，以探查高斯在邻近运动状态下的稳定性：
   $$\begin{array} { c } { { ( \mu + \Delta \mu , r + \Delta r , s + \Delta s ) = \mathcal { D } ( \mu , r , s , t + \mathcal { X } ( i ) ) , } } \\ { { \mathcal { X } ( i ) = \mathcal { N } ( 0 , 1 ) \cdot \beta \cdot \Delta t \cdot ( 1 - i / \tau ) } } \end{array}$$
   这一扰动机制能有效暴露时间不稳定的高斯（如浮空伪影的源头），使剪枝过程不仅考虑静态重要性，还兼顾时序一致性。消融实验表明，TSP+TSS 在 NeRF-DS bell 场景上将高斯数量减少 11× 的同时，SSIM 反而高于未剪枝的 DeformableGS 基线（0.8838 vs 0.8781），并显著抑制了时间闪烁和浮空伪影。

3. **GroupFlow**：在剪枝完成后，GroupFlow 将神经形变场蒸馏为分组的 SE(3) 刚性变换。具体流程为：(a) 通过最远点采样选取 J 个控制点；(b) 基于轨迹相似度将每个高斯分配到运动模式最接近的控制点所在组；(c) 利用 Umeyama 对齐估计每组从规范帧到各时间步的刚性变换 $[R_j^t | T_j^t]$：
   $$\underset { R _ { j } ^ { t } , T _ { j } ^ { t } } { \arg \operatorname* { m i n } } \sum _ { \mu _ { i } \in \mathcal { M } _ { s a m p } ^ { j } } \Vert \mu _ { i } ^ { t } - ( R _ { j } ^ { t } ( \mu _ { i } ^ { 0 } - h _ { j } ^ { 0 } ) + h _ { j } ^ { 0 } + T _ { j } ^ { t } ) \Vert ^ { 2 }$$
   变形后的均值和旋转则通过组变换直接计算：
   $$\mu _ { i } ^ { t } = R _ { j } ^ { t } ( \mu _ { i } ^ { 0 } - h _ { j } ^ { 0 } ) + h _ { j } ^ { 0 } + T _ { j } ^ { t }, \quad \boldsymbol { r } _ { i } ^ { t } = \operatorname { q u a t } \big ( \boldsymbol { R } _ { j } ^ { t } \operatorname { m a t } ( \boldsymbol { r } _ { i } ^ { 0 } ) \big )$$
   这一设计将形变推理的计算量从 $O(N \cdot C_{\text{MLP}})$ 降至 $O(J \cdot C_{\text{SE(3)}})$，其中 $N$ 为高斯数量（通常数万至数十万），$J$ 为分组数（默认 2048）。

### 训练流程

SpeeDe3DGS 的训练分为两个阶段：

- **稠密化阶段**：采用软剪枝（soft pruning），即在稠密化过程中逐步移除低敏感度高斯，同时允许新高斯通过克隆和分裂继续生长。软剪枝比例为 60%。
- **后稠密化阶段**：稠密化结束后执行硬剪枝（hard pruning），一次性移除 30% 的低分高斯，固定模型容量。随后初始化 GroupFlow 控制点与分组，进行端到端优化。

在 NeRF-DS 数据集上，完整 SpeeDe3DGS（TSP+TSS+GroupFlow）将高斯数量从 132.22K 压缩至 11.10K（减少 11.91×），渲染速度从 54.37 FPS 提升至 505.60 FPS（10.68× 加速），训练时间从 1523.83 s 缩短至 625.48 s（2.44× 加速），而 PSNR 仅下降 0.14 dB（23.66 vs 23.80）。

### 模块间关系

三个模块在加速机制上相互正交且可叠加：TSP/TSS 通过减少高斯数量降低形变和光栅化的计算量；GroupFlow 通过共享刚性变换降低每个剩余高斯的形变推理成本。消融实验证实了两条路径的独立性——在 HyperNeRF 上，单独 TSP 实现 9.37× 渲染加速，单独 GroupFlow 实现 15.66× 加速，两者结合达到 29.21× 加速。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/001_Figure_1.jpg]]
*Figure 1: Our SpeeDe3DGS framework achieves 9.88× faster rendering, 11.37× fewer Gaussians, and 2.87× shorter training on the HyperNeRF [37] chicken scene while preserving the image quality of DeformableGS [53] through Temporal Sensitivity Pruning (TSP) and Sampling (TSS). Applying our GroupFlow method on top of pruning accelerates rendering and training by 33.13× and 4.24×, respectively*



SpeeDe3DGS 围绕两个因果旋钮展开：**减少需要形变推理的高斯原语数量**（通过时序敏感性剪枝）和**降低每个原语的形变推理成本**（通过分组共享 SE(3) 刚性变换）。以下按模块展开其核心机制与关键公式。

### 3D 高斯原语与动态形变基线

动态 3DGS 将场景表示为 $N$ 个 3D 高斯原语的集合：

$$\mathcal { G } = \{ \mathcal { G } _ { i } = \{ \mu _ { i } , s _ { i } , r _ { i } , h _ { i } , \sigma _ { i } \} \} _ { i = 1 } ^ { N }$$

其中 $\mu_i$ 为均值（位置），$s_i$ 为尺度，$r_i$ 为旋转四元数，$h_i$ 为球谐颜色系数，$\sigma_i$ 为不透明度。在 DeformableGS 等基线中，每个高斯在时间 $t$ 的位置和旋转由一个逐高斯的 MLP 形变场 $\mathcal{D}$ 预测：$(\mu_i^t, r_i^t, s_i^t) = \mathcal{D}(\mu_i, r_i, s_i, t)$。这一逐原语推理是计算瓶颈的核心来源。

### 模块一：时序敏感性剪枝（TSP）

**核心思想**：通过聚合高斯原语在全部训练时间步上的图像空间梯度，量化其对重建损失的时序贡献，周期性移除低分原语。

**关键公式——二阶敏感度**：对于 L2 重建损失，高斯 $\mathcal{G}_i$ 在其投影像素集 $\mathcal{P}_{g_t}$ 上的二阶敏感度为：

$$\nabla _ { g _ { i } } ^ { 2 } L _ { 2 } = \sum _ { \phi , t \in \mathcal { P } _ { g _ { t } } } \left( \left( \nabla _ { g _ { i } } I _ { \mathcal { G } _ { t } } ( \phi ) \right) ^ { 2 } + \left( I _ { \mathcal { G } _ { t } } ( \phi ) - I _ { g t } \right) \nabla _ { g _ { i } } ^ { 2 } I _ { \mathcal { G } _ { t } } ( \phi ) \right)$$

该式包含两项：图像空间梯度的平方（一阶项）和残差加权的二阶项。当训练收敛、残差项 $(I_{\mathcal{G}_t}(\phi) - I_{gt})$ 趋近于零时，剪枝分数简化为：

$$\tilde { U } _ { \mathcal { G } _ { i } } \approx \nabla _ { g _ { i } } ^ { 2 } L _ { 2 } \approx \sum _ { \phi , t \in \mathcal { P } _ { g t } } \left( \nabla _ { g _ { i } } I _ { \mathcal { G } _ { t } } ( \phi ) \right) ^ { 2 }$$

**变量含义**：$g_i$ 为高斯 $i$ 在像素 $\phi$ 处的 2D 投影值；$I_{\mathcal{G}_t}(\phi)$ 为时间 $t$ 的渲染像素值；$I_{gt}$ 为真值像素。该分数本质上量化了高斯在时空上的累计视觉贡献——分数越低，移除该高斯对重建质量的影响越小。

### 模块二：时序敏感性采样（TSS）

**核心思想**：在估计剪枝分数时，对形变函数的时间戳注入线性退火的高斯噪声，迫使模型探查邻近运动状态下的敏感度，从而暴露时间不稳定的高斯（如浮空伪影源）。

**关键公式——时间扰动**：

$$\begin{array} { c } { { ( \mu + \Delta \mu , r + \Delta r , s + \Delta s ) = \mathcal { D } ( \mu , r , s , t + \mathcal { X } ( i ) ) , } } \\ { { \mathcal { X } ( i ) = \mathcal { N } ( 0 , 1 ) \cdot \beta \cdot \Delta t \cdot ( 1 - i / \tau ) } } \end{array}$$

**变量含义**：$\mathcal{X}(i)$ 为第 $i$ 次迭代的扰动幅值；$\beta$ 为初始扰动幅度（默认 0.1）；$\Delta t$ 为相邻训练帧的时间间隔；$\tau$ 为退火周期（默认 20,000 次迭代），扰动随训练进行线性衰减至零。消融实验表明 TSS 对 $\beta$ 和 $\tau$ 不敏感，在所有配置下均优于无 TSS 的 TSP（Table 11）。

**因果机制**：静态剪枝（如基于不透明度的标准剪枝）无法区分“始终可见但贡献低”的高斯与“仅在少数帧贡献高”的高斯。TSP 通过时序聚合解决前者，TSS 通过扰动探查解决后者——在 bell 场景中，TSP+TSS 将高斯数量减少 11×，同时 SSIM 高于未剪枝基线（0.8838 vs 0.8781），并有效抑制了时间闪烁和浮空伪影（Figure 3）。

### 模块三：GroupFlow——运动分组与 SE(3) 蒸馏

GroupFlow 将逐高斯的 MLP 形变蒸馏为分组共享的 SE(3) 刚性变换，从两个维度降低推理成本：形变推理次数从 $N$（高斯数）降至 $J$（组数）；每次推理从 MLP 前向传播变为矩阵乘法。

#### 3.1 运动轨迹表示与聚类

每个高斯 $\mathcal{G}_i$ 的运动轨迹定义为其在所有 $F$ 个时间帧上的均值和旋转序列：

$$\mathcal { M } = \{ \mathcal { M } _ { i } \} _ { i = 1 } ^ { N } , \quad \mathcal { M } _ { i } = \{ \mu _ { i } ^ { t } , r _ { i } ^ { t } \} _ { t = 0 } ^ { F - 1 }$$

通过最远点采样（FPS）选取 $J$ 个控制点 $\{h_j\}_{j=1}^J$，然后基于轨迹相似度将每个高斯分配到最相似的控制点组。相似度分数结合了时间残差的标准差与均值：

$$S _ { i , j } = \lambda _ { r } \mathrm { s t d } _ { t } ( \| \mu _ { i } ^ { t } - h _ { j } ^ { t } \| ) + ( 1 - \lambda _ { r } ) \mathrm { m e a n } _ { t } ( \| \mu _ { i } ^ { t } - h _ { j } ^ { t } \| )$$

其中 $\lambda_r$ 为平衡系数。该设计确保同一组内的高斯具有高度一致的运动模式。

#### 3.2 SE(3) 刚性变换估计与预测

对每个组 $j$ 和时间 $t$，利用 Umeyama 对齐在采样的组内均值上估计从规范帧（$t=0$）到当前帧的刚性变换 $[R_j^t | T_j^t]$：

$$\underset { R _ { j } ^ { t } , T _ { j } ^ { t } } { \arg \operatorname* { m i n } } \sum _ { \mu _ { i } \in \mathcal { M } _ { s a m p } ^ { j } } \Vert \mu _ { i } ^ { t } - ( R _ { j } ^ { t } ( \mu _ { i } ^ { 0 } - h _ { j } ^ { 0 } ) + h _ { j } ^ { 0 } + T _ { j } ^ { t } ) \Vert ^ { 2 }$$

**变量含义**：$h_j^0$ 为控制点 $j$ 在规范帧的位置；变换以控制点为枢轴，先减去 $h_j^0$ 进行旋转，再加回平移。估计完成后，组内任意高斯的形变通过共享变换直接计算：

均值预测：
$$\mu _ { i } ^ { t } = R _ { j } ^ { t } ( \mu _ { i } ^ { 0 } - h _ { j } ^ { 0 } ) + h _ { j } ^ { 0 } + T _ { j } ^ { t }$$

旋转预测：
$$\boldsymbol { r } _ { i } ^ { t } = \operatorname { q u a t } \big ( \boldsymbol { R } _ { j } ^ { t } \operatorname { m a t } ( \boldsymbol { r } _ { i } ^ { 0 } ) \big )$$

其中 $\operatorname{mat}(\cdot)$ 将四元数转为旋转矩阵，$\operatorname{quat}(\cdot)$ 将旋转矩阵转回四元数。尺度 $s_i$ 在 GroupFlow 中保持不变，因为 SE(3) 变换不包含缩放分量。

**瓶颈与权衡**：分组数 $J$ 是核心超参数。$J=2048$ 在视觉质量（PSNR/SSIM）与模型紧凑性之间达到最佳平衡（Table 10）；$J$ 过小丢失运动细节，$J$ 过大则参数量增加而收益递减。对于极度非刚性形变场景，共享刚性变换的建模能力存在理论上限，这是 GroupFlow 的主要局限性。

### 训练流程集成

SpeeDe3DGS 的训练分两阶段进行（Section 4.3）：**稠密化阶段**应用软剪枝（默认移除 60% 高斯），在保持模型探索能力的同时逐步压缩容量；**稠密化后**执行硬剪枝（默认再移除 30%），进一步精简模型；随后初始化 GroupFlow 控制点与分组，端到端优化 SE(3) 变换参数。软剪枝 60% + 硬剪枝 30% 在渲染速度与 PSNR 之间取得最佳权衡（Figure 5 热力图）。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our GroupFlow method. Given a dynamic Gaussian Splatting model G, we identify a subset of Gaussians as control points and assign each Gaussian to the control point*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of our pruning methods on the real-world NeRF-DS [52] bell scene. Our proposed Temporal Sensitivity Pruning (TSP) and Temporal Sensitivity Sampling (TSS) methods achieve higher SSIM than the baseline DeformableGS [53] model while using 11× fewer Gaussians. The left regions of the renderings appear visually identical, while the right regions show that combining TSP with TSS significantly reduces temporal flicker and floating artifacts compared to both standard pruning and the unpruned baseline*



## 实验与关键发现

### 核心性能：NeRF-DS 上的组件消融

Table 1 在真实世界 NeRF-DS 数据集上对 SpeeDe3DGS 的三个核心组件进行了逐层消融，揭示了各组件对速度-质量权衡的独立与协同贡献。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/005_Table_1.jpg]]
*Table 1: Results on the seven scenes in the real-world NeRF-DS dataset [52] with our SpeeDe3DGS framework. TSP, TSS, and GF denote Temporal Sensitivity Pruning, Sampling, and GroupFlow, respectively. Size measures the combined deformation network and point cloud storage. Each experiment is run three times and averaged to reduce training variance. The best and second-best results are highlighted. FPS and Train Time are measured on RTX 3090 and RTX A5000 GPUs, respectively. Appendix A.6 reports per-scene results*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/009_Table_5.jpg]]
*Table 5: Results for the seven scenes in the real-world NeRF-DS dataset [52] with MonoDyGauBench [25]. Results with our SpeeDe3DGS framework are reported in Table 1*

**Temporal Sensitivity Pruning (TSP) 的独立效果。** 仅启用 TSP 时，高斯原语数量从 132.22K 锐减至 10.90K（12.13× 压缩），渲染 FPS 从 54.37 跃升至 346.96（6.38× 加速），训练时间从 1523.83s 缩短至 844.55s（1.80× 加速）。值得注意的是，PSNR 仅下降 0.32 dB（23.80 → 23.48），SSIM 几乎持平（0.8789 → 0.8773）。这表明时序敏感度分数能有效识别并移除对重建贡献微弱的高斯原语，而不会显著损害视觉质量。

**Temporal Sensitivity Sampling (TSS) 的增益。** 在 TSP 基础上叠加 TSS 后，PSNR 回升至 23.53 dB，SSIM 提升至 0.8802——甚至略高于未剪枝的 DeformableGS 基线（SSIM 0.8789）。这一反直觉的提升验证了 TSS 的核心机制：通过对形变函数的时间戳注入线性退火高斯噪声，模型被迫在邻近运动状态下评估原语的敏感度，从而暴露并移除了那些仅在特定时间戳上活跃、但在时序上不稳定的“浮空”原语。Figure 3 在 NeRF-DS bell 场景上直观展示了这一效果：TSP+TSS 以 11× 更少的高斯数量获得了比未剪枝基线更高的 SSIM（0.8838 vs 0.8781），且右侧渲染区域的时间闪烁和浮空伪影显著减少。

**GroupFlow 的叠加效应。** 在 TSP+TSS 剪枝基础上引入 GroupFlow，渲染 FPS 进一步飙升至 505.60（10.68× 加速），训练时间缩短至 625.48s（2.44× 加速）。PSNR 为 23.66 dB，与未剪枝 DeformableGS 基线的 23.80 dB 仅差 0.14 dB，而 SSIM 以 0.8807 保持领先。这证明将逐高斯 MLP 形变蒸馏为分组共享的 SE(3) 刚性变换，在几乎不损失精度的前提下大幅降低了形变推理的计算瓶颈。模型总大小从 26.47 MB 压缩至 8.12 MB（3.26× 压缩），这得益于剪枝减少了高斯数量，以及 GroupFlow 用紧凑的刚性变换参数替代了 MLP 权重。

### 跨数据集泛化验证

**MonoDyGauBench 大规模基准。** Table 2 在覆盖 5 个数据集、50 个动态场景的 MonoDyGauBench 上验证了方法的泛化性。将 SpeeDe3DGS 应用于 DeformableGS 基线时，完整方法（TSP+TSS+GF）实现了 13.71× 渲染加速（20.20 → 276.91 FPS）和 2.53× 训练加速。值得注意的是，剪枝后的 DeformableGS（TSP+TSS）在 PSNR 上仅下降 0.01 dB（28.37 vs 28.38），而 GroupFlow 叠加后 PSNR 为 28.20 dB，下降幅度仍然可控。当 SpeeDe3DGS 应用于 4DGS 基线时，完整方法实现了 3.63× 渲染加速和 1.99× 训练加速，证明该方法对不同的神经形变后端具有通用性。

**HyperNeRF 与 D-NeRF 数据集。** 在 HyperNeRF 的 8 个场景上（Table 9），GroupFlow 单独实现了 23.84× 渲染加速（10.91 → 260.05 FPS），而 TSP 单独实现 9.37× 加速，两者结合达到 29.21× 加速。在合成 D-NeRF 数据集上（Table 8），完整 SpeeDe3DGS 实现 11.42× 渲染加速（43.36 → 495.27 FPS），PSNR 下降仅 0.30 dB（38.94 → 38.64）。这些结果表明，该方法在真实世界和合成场景、不同运动复杂度下均表现出稳健的加速能力。

### 关键超参数消融

**GroupFlow 分组数量 J。** Table 10 在 NeRF-DS 和 D-NeRF 上对分组数 J 进行了消融。当 J=2048 时，PSNR 和 SSIM 达到或接近最优，同时模型大小保持紧凑。J 过小（如 512）时，每组覆盖的运动区域过大，共享刚性变换无法精细建模局部非刚性运动，导致 PSNR 下降；J 过大（如 4096）时，参数量增加但视觉质量收益递减。因此 J=2048 被选为默认配置，在视觉保真度与模型紧凑性之间取得最佳平衡。

**TSS 扰动参数。** Table 11 表明 TSS 对超参数不敏感：在扰动幅度 β∈{0.05, 0.1, 0.2} 和退火周期 τ∈{10000, 20000, 30000} 的所有配置下，TSP+TSS 的 PSNR 和 SSIM 均优于无 TSS 的 TSP。默认配置 β=0.1、τ=20000 在 NeRF-DS 上表现良好。

**软硬剪枝比例。** Figure 5 的热力图展示了软剪枝（稠密化阶段）和硬剪枝（稠密化后）比例的联合消融。红色标记点（60% 软剪枝 + 30% 硬剪枝）在渲染 FPS 与 PSNR 之间取得最佳权衡，被选为默认参数。过高的硬剪枝比例（如 >50%）会导致 PSNR 急剧下降，表明稠密化后过度移除高斯会损害模型的表达能力。

### 失败模式与局限性

尽管 SpeeDe3DGS 在多数场景下表现出色，但仍存在若干已知局限：

1. **高度非刚性运动场景。** GroupFlow 通过共享 SE(3) 刚性变换来建模运动，在极度变形的区域（如大幅度的流体、布料褶皱）可能不够灵活。增加分组数 J 可以部分缓解，但固定 J=2048 时存在建模能力上限。
2. **相机位姿噪声。** 当相机位姿估计不准确或场景运动不稳定时，基线方法（DeformableGS）本身存在重建质量问题，SpeeDe3DGS 继承并可能放大这些误差。
3. **极端剪枝比例。** 当剪枝比例超过 90% 时，当前敏感度指标可能无法精确区分关键原语与冗余原语，导致视觉质量显著下降。如何设计更智能的剪枝策略或引入原语重新增补机制仍是开放问题。
4. **硬件差异导致的对比偏差。** 论文中 FPS 统一在 RTX 3090 上测量，但训练时间分别在 RTX A5000（NeRF-DS、D-NeRF）和 RTX A6000（HyperNeRF）上测量。尽管已明确标注，跨方法的训练时间对比仍需注意这一硬件差异。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/006_Table_2.jpg]]
*Table 2: Results on Monocular Dynamic Gaussian Splatting Benchmark (MonoDyGauBench) [25]. Quantitative results averaged across five datasets and 50 scenes for all methods in Section 3.2. We cumulatively apply our SpeeDe3DGS methods to the DeformableGS [53] and 4DGS [49] baselines, keeping the original neural variants with low FPS for reference, but excluding them from comparisons to focus on real-time methods. Pruning is performed using TSP and TSS. Each experiment is repeated three times and averaged. The best and second-best results are highlighted; improvements over corresponding baselines are bolded. FPS and baseline Train Time are measured on an RTX 3090 GPU, while our Train Time* is measured o...*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/013_Table_9.jpg]]
*Table 9: Results on the eight real-world scenes from the HyperNeRF dataset [37] in the DeformableGS [53] paper with our SpeeDe3DGS framework. TSP, TSS, and GF denote Temporal Sensitivity Pruning, Sampling, and GroupFlow, respectively. Size measures the combined deformation network and point cloud storage. Each experiment is run three times and averaged to reduce training variance. The best and second-best results are highlighted. FPS and Train Time are measured on RTX 3090 and RTX A6000 GPUs, respectively. Per-scene results are reported in Appendix A.6. Results with MonoDyGauBench [25] are reported in Table 4*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/016_Figure_5.jpg]]
*Figure 5: Ablation on pruning percentages with our SpeeDe3DGS framework. We sweep soft (densification-stage) and hard (postdensification) pruning ratios in 5% increments for the NeRF-DS [52] and D-NeRF [39] datasets using the DeformableGS [53] codebase. Each configuration is run three times without TSS or GroupFlow, and results are averaged across all runs. (0%, 0%) corresponds to the unpruned baseline, while the first row and column show pruning in isolation. The red dot marks our selected (60%, 30%) soft–hard ratio. FPS and Train Time improvements are measured on an RTX A5000 GPU*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/014_Table_10.jpg]]
*Table 10: Ablation on group count J on the NeRF-DS [52] and D-NeRF [39] datasets with our SpeeDe3DGS framework. J= indicates that GroupFlow is not used. Each experiment is repeated three times and averaged to reduce training variance. The best and second best results are highlighted. FPS and Train Time are measured on RTX 3090 and RTX A5000 GPUs, respectively*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/015_Table_11.jpg]]
*Table 11: Ablation on perturbation magnitude β and annealing period τ on the NeRF-DS [52] dataset with our SpeeDe3DGS framework. β=− and τ =− indicate that TSS is not used. Each experiment is repeated three times and averaged to reduce training variance*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/012_Table_8.jpg]]
*Table 8: Results on the eight scenes in the synthetic D-NeRF dataset [39] with our SpeeDe3DGS framework. TSP, TSS, and GF denote Temporal Sensitivity Pruning, Sampling, and GroupFlow, respectively. Size measures the combined deformation network and point cloud storage. Each experiment is run three times and averaged to reduce training variance. The best and second-best results are highlighted. FPS and Train Time are measured on RTX 3090 and RTX A5000 GPUs, respectively. Per-scene results are provided in Appendix A.6. Results with MonoDyGauBench [25] are reported in Table 3*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_07917/figures/008_Table_4.jpg]]
*Table 4: Results for the 17 scenes in the real-world HyperNeRF dataset [37] with MonoDyGauBench [25]. Results with our SpeeDe3DGS framework are reported in Table 9*



## 定位与知识库关联

### 1. 与基线方法的关系

SpeeDe3DGS 并非从零构建一个全新的动态场景表示框架，而是在现有动态 3DGS 基线之上，通过**原语剪枝**和**运动表示蒸馏**两条正交路径进行加速。其核心基线为 **DeformableGS**，该方法使用逐高斯的 MLP 形变场将规范帧高斯映射到各时间步，是动态 3DGS 领域最具代表性的神经形变范式。SpeeDe3DGS 的三个组件——TSP、TSS、GroupFlow——均以 DeformableGS 为基础进行扩展，且可独立或组合应用。

**与 DeformableGS 的关系**：DeformableGS 承担了“神经形变教师”角色。在训练阶段，SpeeDe3DGS 首先依赖 DeformableGS 的 MLP 形变场来学习场景运动并计算时序敏感度分数；在剪枝完成后，GroupFlow 将 MLP 所学到的运动知识蒸馏为分组的 SE(3) 刚性变换，从而在推理阶段完全替代逐高斯 MLP 推理。这种“先学习后蒸馏”的策略使得 SpeeDe3DGS 既保留了神经形变场的建模能力，又规避了其高昂的推理成本。

**与 4DGS 的关系**：**4DGS** 采用 HexPlane 网格表示时空形变，是另一种主流的神经形变基线。SpeeDe3DGS 在 MonoDyGauBench 上将 TSP/TSS/GroupFlow 同样应用于 4DGS 基线，验证了剪枝和分组策略对非 MLP 形变表示的通用性（Table 2）。这表明 SpeeDe3DGS 的加速思想不依赖于特定的形变场实现，而是针对“逐原语推理”这一动态 3DGS 的共性瓶颈。

**与 RTGS 的关系**：**RTGS** 采用隐式 4D 高斯表示，不依赖显式神经形变场，是动态渲染速度的参考上限。SpeeDe3DGS 在速度上接近甚至超过 RTGS，同时在视觉质量上显著优于后者，证明了“剪枝+分组蒸馏”路径在速度-质量权衡上的优越性。

### 2. 方法谱系中的定位

从技术路线看，SpeeDe3DGS 处于两条研究脉络的交汇点：

**脉络一：3DGS 原语剪枝**。静态 3DGS 中已有基于梯度、不透明度或尺度的剪枝工作，但直接将静态剪枝策略迁移到动态场景会忽略时间维度的冗余——一个高斯可能在某些帧重要、在其他帧冗余。SpeeDe3DGS 的 TSP 将剪枝分数从空间域推广到时空域，通过聚合所有时间步的图像空间梯度来量化高斯的“时序贡献”，这在动态 3DGS 剪枝中属于开创性工作。TSS 进一步引入时间扰动机制，通过探查邻近运动状态来暴露时间不稳定的浮空高斯，这是对传统剪枝策略的重要补充。

**脉络二：运动表示简化**。DeformableGS 和 4DGS 等方法的逐原语形变推理是速度瓶颈的根源。GroupFlow 的核心思想是将高维的逐高斯运动轨迹压缩为低维的分组刚性变换——通过最远点采样选取控制点、基于轨迹相似度聚类、利用 Umeyama 对齐估计每组 SE(3)。这一策略本质上是用空间局部性换取计算效率：它假设空间邻近的高斯具有相似的刚性运动，从而将形变推理的计算复杂度从 $O(N)$ 降至 $O(J)$（$J \ll N$）。与直接学习低维运动基的方法不同，GroupFlow 的蒸馏策略确保了分组变换忠实于已学到的神经运动场，避免了从零训练分组表示可能带来的收敛困难。

### 3. 适用边界

**剪枝的有效边界**：TSP 和 TSS 的核心假设是场景中存在大量对重建贡献微小的高斯原语。在 NeRF-DS 数据集上，DeformableGS 的高斯数量可被削减约 12× 而几乎不损失视觉质量，说明基线方法确实存在严重的原语冗余。然而，在场景本身已经高度紧凑（如简单刚体运动）或高斯分布极为稀疏的情况下，剪枝的收益会递减。软剪枝 60% + 硬剪枝 30% 的默认配置（Figure 5）是在 NeRF-DS 和 D-NeRF 上经验调优的结果，极端场景可能需要调整。

**GroupFlow 的建模能力边界**：GroupFlow 用共享 SE(3) 刚性变换近似局部区域的非刚性运动，其建模精度受分组数 $J$ 控制。消融实验（Table 10）表明 $J=2048$ 在视觉质量与模型紧凑性之间达到最佳平衡，但固定 $J$ 意味着 GroupFlow 对极度变形或复杂非刚性运动（如流体、布料褶皱）的建模能力存在上限。增加 $J$ 可缓解此问题，但会稀释分组共享带来的加速收益。

**对基线质量的依赖**：SpeeDe3DGS 继承了动态 3DGS 基线的固有局限。当相机位姿有噪声或场景运动不稳定时，基线本身的重建质量会下降，TSP 的敏感度估计和 GroupFlow 的运动蒸馏也会受到影响。此外，在高度可变形和非刚性运动场景中，基线方法本身仍具挑战性，SpeeDe3DGS 的加速策略无法弥补基线建模能力的不足。

### 4. 局限与开放问题

**已明确的局限**：
- **非刚性运动建模上限**：GroupFlow 通过共享刚性变换近似局部运动，在极度变形区域可能不够灵活。尽管增加分组数 $J$ 可缓解，但固定分组策略缺乏对运动复杂度的自适应能力。
- **硬件差异带来的对比公平性风险**：论文中 FPS 统一在 RTX 3090 上测量，但训练时间分别在 RTX A5000 和 RTX A6000 上测量，跨方法训练时间对比需注意这一差异。部分基线（如 DeformableGS 在 HyperNeRF 上）显存占用超过 24 GB，剪枝使得在 24 GB 显存的 GPU 上训练成为可能，这一硬件适应性提升值得关注。
- **剪枝比例的泛化性**：软剪枝 60% + 硬剪枝 30% 的默认配置在 NeRF-DS 和 D-NeRF 上有效，但在其他数据集或场景类型上可能需要重新调优。

**开放问题**：
- **自适应分组**：能否根据运动复杂度动态调整分组数 $J$，或在粗糙分组基础上对高变形区域进行局部精细化？这将使 GroupFlow 在保持加速优势的同时提升对复杂非刚性运动的建模能力。
- **极端剪枝下的质量保持**：在剪枝比例超过 90% 的极端情况下，如何设计更智能的敏感度指标（如融合不透明度、尺度、视点依赖可见性）或引入重新增补高斯的机制，以同时维持渲染速度和视觉质量？
- **GroupFlow 的泛化增强**：能否通过融合更多运动基（如混合形变场）或引入 2D 光流先验来增强 GroupFlow 对高度变形场景的泛化能力？这涉及到将数据驱动的运动先验注入分组过程。
- **时序敏感度度量的扩展**：当前的 TSP 分数基于 L2 损失的二阶敏感度近似，是否可与其他重要性度量（如对感知损失的贡献、对时序一致性的影响）结合，以进一步提升剪枝的针对性和鲁棒性？



## 原文 PDF

![[paperPDFs/CVPR_2026/SpeeDe3DGS_Speedy_Deformable_3D_Gaussian_Splatting_with_Temporal_Pruning_and_Motion_Grouping.pdf]]

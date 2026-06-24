---
title: "Gaussian See, Gaussian Do: 3D Semantic Motion Transfer"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Gaussian_See_Gaussian_Do_3D_Semantic_Motion_Transfer.pdf
aliases:
- GSGD
- GSGD3SMT
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入基于锚点的视角感知运动嵌入机制（通过slerp插值实现跨视角信息共享），并结合ARAP旋转约束与LPIPS感知损失构建鲁棒的4D重建流程。"
primary_logic: "不同视角的运动嵌入共享底层三维运动信息，锚点插值机制可在保持视角一致性的同时加速收敛；使用LPIPS感知损失替代像素级损失并施加显式的旋转刚性约束，能有效抑制监督视频中的噪声和视点不一致伪影，实现高质量动态重建。"
claims:
- "在 Mini-Mixamo 和 Cross-Category 基准上，本方法在 Motion Fidelity 和 CLIP 分数上显著优于 SC4D 和 DreamGaussians4D，Motion Fidelity 分别达到 0.74/0.66 vs 0.65/0.61 和 0.56/0.54。"
- "人类评估中，本方法在外观质量上获得 4.66/5 评分，是唯一能够保持目标身份的方法，运动质量与 SC4D 相当。"
- "锚点插值机制实现了优于简单插值和全局嵌入的新视角运动合成，MSE 低至 0.0028。"
- "ARAP Rotation 和 LPIPS 损失显著改善重建结构完整性和 CLIP 分数（Naive:0.9423 → +ARAP:0.9608 → +LPIPS:0.9636），尽管 Motion Fidelity 变化不大。"
---

# Gaussian See, Gaussian Do: 3D Semantic Motion Transfer

> [!tip] 核心洞察
> 不同视角的运动嵌入共享底层三维运动信息，锚点插值机制可在保持视角一致性的同时加速收敛；使用LPIPS感知损失替代像素级损失并施加显式的旋转刚性约束，能有效抑制监督视频中的噪声和视点不一致伪影，实现高质量动态重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Gaussian See, Gaussian Do：三维语义运动迁移 |
| 英文题名 | Gaussian See, Gaussian Do: 3D Semantic Motion Transfer |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2511.14848); [Project](https://gsgd-motiontransfer.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Gaussian See, Gaussian Do |
| Dataset | Mini-Mixamo, Cross-Category, Novel-view Motion Synthesis |

> [!tip] 效果简介
> - Mini-Mixamo 上，Motion Fidelity↑ 为 0.74，对比 SC4D:0.65, DG4D:0.61，变化 +0.09 vs SC4D, +0.13 vs DG4D。
> - Cross-Category 上，Motion Fidelity↑ 为 0.66，对比 SC4D:0.56, DG4D:0.54，变化 +0.10 vs SC4D, +0.12 vs DG4D。
> - Mini-Mixamo 上，CLIP Score↑ 为 0.963，对比 SC4D:0.905, DG4D:0.945，变化 +0.058 vs SC4D, +0.018 vs DG4D。

## 概述

**Gaussian See, Gaussian Do** 提出了一种语义驱动的三维运动迁移框架，旨在将多视角源视频中的运动模式“迁移”到任意静态 3D 高斯泼溅（3DGS）目标资产上，使其产生语义匹配的动态效果（Fig. 1）。该工作的核心挑战在于：现有方法缺乏对无骨架三维物体进行跨类别、语义有意义的运动迁移能力，且依赖视频扩散模型生成的监督视频存在噪声和视点不一致，严重影响 4D 重建质量。

针对上述瓶颈，方法引入两个关键机制。其一为**基于锚点的视角感知运动嵌入**：通过在多视角间共享锚点嵌入并以球面线性插值（slerp）获取任意视角的运动编码，实现跨视角信息共享与加速收敛。其二为**鲁棒的 4D 重建流程**：采用 LPIPS 感知损失替代像素级 MSE 损失，并施加显式的 ARAP Rotation 旋转刚性约束，有效抑制监督视频中的噪声与伪影。

在 Mini-Mixamo 和 Cross-Category 两个基准上，本方法在 Motion Fidelity 指标上分别达到 0.74 和 0.66，显著优于改编后的基线方法 SC4D（0.65/0.56）和 DreamGaussians4D（0.61/0.54）；CLIP 分数同样取得领先（0.963 vs 0.905/0.945）。人类评估中，本方法是唯一能保持目标身份的方法，外观质量评分达 4.66/5。消融实验证实，锚点插值机制在新视角运动合成上的 MSE 低至 0.0028，而 ARAP Rotation 与 LPIPS 损失的组合将 CLIP 分数从 0.9423 提升至 0.9636。方法同时存在局限性：对高关节活动（如踢腿、跳跃）效果不佳，受限于底层视频扩散模型的反演能力，且运动保真度指标 MF3D 对结构失真不敏感，可能高估部分重建质量。

## 背景与动机

### 问题背景：三维语义运动迁移

将一段视频中观察到的运动模式迁移到另一个静态三维物体上，使其“活起来”，是计算机视觉与图形学中长期存在的挑战。与传统的骨骼驱动动画不同，**语义运动迁移**不依赖显式的骨架或关键点标注，而是要求模型理解运动的高级语义（如“翅膀拍打”“前腿抬起”），并将其适配到形态迥异的目标物体上。这一能力对影视制作、游戏开发、增强现实等场景具有重要价值，但现有方法在此任务上存在明显瓶颈。

### 现有方法缺口

当前的三维运动迁移方法主要沿两条路径展开，但均无法满足语义运动迁移的需求：

- **基于骨骼重定向的方法**：要求源和目标均具备可用的骨架结构，无法处理无骨架的通用三维资产（如卡通大象、车辆等）。
- **基于视频扩散模型的生成方法**：虽然可以利用预训练的视频扩散模型从单目视频中提取运动信息，但**生成的监督视频普遍存在噪声和视点不一致问题**。具体而言，视频扩散模型在不同视角下生成的视频帧可能出现外观漂移、几何伪影，甚至运动方向矛盾——例如，同一人物在0°视角向左移动，在180°视角却同样向左移动（见 Fig. 16）。这些伪影直接导致后续4D重建质量下降。

### 核心瓶颈

综合来看，该领域的**核心瓶颈**在于：

> **缺乏对任意无骨架三维物体进行语义有意义的跨类别运动迁移的能力；现有视频扩散模型生成的监督视频存在噪声和视点不一致，导致4D重建质量下降。**

这一瓶颈可分解为两个子问题：
1. **运动嵌入的视角一致性问题**：如何从多视角源视频中提取一个统一的、视角感知的运动表示，使得在不同视角下生成的视频保持运动语义一致？
2. **鲁棒的4D重建问题**：如何在监督视频本身存在噪声和伪影的情况下，仍然重建出结构完整、外观保真、运动平滑的动态三维场景？

### 本文动机

针对上述瓶颈，本文提出 **Gaussian See, Gaussian Do** 方法，核心动机是通过两个关键设计来突破限制：

- **基于锚点的视角感知运动嵌入机制**：通过球面线性插值（slerp）在锚点嵌入之间共享跨视角信息，既保证不同视角的运动语义一致，又加速优化收敛。
- **鲁棒的4D重建流程**：引入ARAP旋转约束（显式约束局部区域的旋转刚性）和LPIPS感知损失（替代像素级MSE损失），有效抑制监督视频中的噪声和视点不一致伪影，实现高质量动态重建。

通过这两个设计，方法能够在无需骨架标注的条件下，将源视频中的运动语义迁移到形态各异的静态三维高斯泼溅（3DGS）资产上，实现跨类别语义运动迁移。

## 核心创新

Gaussian See, Gaussian Do 的核心创新在于构建了一套从多视角视频中提取语义运动并鲁棒迁移至任意无骨架三维物体的完整管线，其关键突破体现在三个紧密耦合的“变更槽”上。

### 基于锚点的视角感知运动嵌入

传统方法对每个源视角独立优化运动嵌入，导致跨视角信息割裂、收敛缓慢且无法泛化至新视角。本工作引入**基于锚点的球面线性插值（slerp）运动嵌入机制**：在源视角范围内均匀分布固定数量 $K$ 个锚点嵌入 $\{\mathbf{m}_k^*\}$，对于任意目标视角 $\phi$，通过其最近两个锚点的 slerp 插值获得运动嵌入：

$$\mathbf{m}_{\phi} = \mathrm{slerp}\left(\mathbf{m}_{i}, \mathbf{m}_{j}, \frac{\phi - \phi_{i}}{\phi_{j} - \phi_{i}}\right)$$

训练时，每次采样一个源视角视频，使用插值后的运动编码进行去噪分数匹配优化，联合更新所有锚点嵌入：

$$\{\mathbf{m}_k^*\}_{1}^{K} = \underset{\{\mathbf{m}_k\}}{\mathrm{argmin}} \; \mathbb{E}\left[\lambda_{\sigma} \| D_{\theta}(\widetilde{\mathcal{V}_S}[i]; \sigma, \mathbf{m}_{\phi}) - \mathcal{V}_S[i] \|_{2}^{2}\right]$$

这一设计的核心洞察在于：不同视角的运动嵌入共享底层三维运动信息，锚点插值机制强制跨视角信息共享，在保持视角一致性的同时显著加速收敛。定量证据表明，锚点插值在新视角运动合成上 MSE 低至 $0.0028 \pm 0.0016$，远优于简单插值（$0.0926$）和全局嵌入（$0.0038$）（Table 2）。消融实验进一步揭示，锚点数 $K=5$ 在收敛速度与重建质量之间取得最佳平衡；单全局嵌入收敛最慢且最终性能最差（Fig. 8）。

### LPIPS 感知损失替代像素级损失

监督视频由冻结的视频扩散模型生成，不可避免地包含噪声和视点不一致伪影。传统像素级 MSE 损失对逐像素差异过于敏感，会将生成视频中的高频噪声直接传播至重建结果。本工作将重建损失替换为 **LPIPS 感知损失**（Zhang et al., 2018），该损失在深层特征空间度量差异，对像素级噪声具有天然鲁棒性。消融实验显示，在基础重建上引入 LPIPS 损失后，CLIP 分数从 $0.9423$ 提升至 $0.9608$（Table 3），且人类偏好评估中外观真实感获得显著提升（Fig. 5 right）。

### ARAP Rotation 显式旋转约束

标准 ARAP（As-Rigid-As-Possible）损失仅约束控制点之间的相对位置变化，对局部旋转缺乏显式约束，导致变形过程中出现结构扭曲和纹理撕裂。本工作引入 **ARAP Rotation 机制**，显式计算并约束每个控制点邻域的最优旋转矩阵：

$$\hat{R}_{k}^{t} = \underset{R}{\mathrm{argmin}} \sum_{i \in \mathcal{N}_{k}} w_{ik} \| (p_{i}^{t} - p_{k}^{t}) - R(p_{i} - p_{k}) \|^{2}$$

$$\mathcal{L}_{ARAP} = \sum_{t \in 1..F} \sum_{i \in \mathcal{N}_{k}} w_{ik} \| (p_{i}^{t} - p_{k}^{t}) - \hat{R}_{k}^{t}(p_{i} - p_{k}) \|^{2}$$

该约束强制局部区域在变形时保持尽可能刚性的变换，有效抑制了生成视频中的视点不一致伪影。消融实验证实，ARAP Rotation 显著改善重建结构完整性（Fig. 7），与 LPIPS 损失联合使用后 CLIP 分数进一步提升至 $0.9636$（Table 3）。

### 创新协同效应

上述三个变更槽并非孤立改进，而是形成协同增强的闭环：锚点插值机制提供视角一致的初始运动嵌入，LPIPS 感知损失容忍生成视频的局部噪声，ARAP Rotation 从几何层面约束变形刚性。三者共同构成“鲁棒 4D 重建管线”的核心，使得本方法在 Mini-Mixamo 和 Cross-Category 基准上的 Motion Fidelity 分别达到 $0.74$ 和 $0.66$，显著优于 SC4D（$0.65/0.56$）和 DreamGaussians4D（$0.61/0.54$）（Table 1）。人类评估中，本方法是唯一能够保持目标身份的方法，外观质量评分达 $4.66/5$（Fig. 5 left）。

## 整体框架

**Gaussian See, Gaussian Do** 提出了一种将源物体的三维运动语义迁移到目标静态 3DGS 资产的两阶段流水线，其核心设计目标是解决现有方法在跨类别、无骨架条件下的运动迁移中存在的视点不一致与监督噪声问题。

### 流水线总览

整个框架由三个紧密耦合的模块构成（Fig. 2）：

1. **结构化多视角运动反演 (Structured Multiview Motion Inversion)**：从源物体的多视角视频中提取结构化的运动嵌入。该模块引入基于锚点的球面线性插值（slerp）机制，将一组固定数量 $K$ 的锚点运动嵌入均匀分布在源视角范围内，通过协同优化使不同视角共享底层三维运动信息，从而在加速收敛的同时保证跨视角一致性。
2. **视角感知语义运动迁移 (View-aware Semantic Motion Transfer)**：利用冻结的视频扩散模型，以渲染的目标物体首帧图像和插值得到的运动嵌入为条件，生成各视角的监督视频序列。这些视频为目标物体的动态重建提供了逐视角的二维运动监督信号。
3. **4D 重建固化 (4D Consolidation)**：通过控制点和变形场网络将目标 3DGS 与监督视频对齐，并施加 ARAP Rotation 旋转约束与 LPIPS 感知损失，将噪声监督转化为高质量、时序稳定的动态三维重建。

### 输入输出流

- **输入**：源物体的多视角视频 $\mathcal{V}_S$ 与目标静态 3DGS 资产。
- **中间产物**：锚点运动嵌入 $\{\mathbf{m}_k^*\}_{k=1}^K$ 与逐视角监督视频。
- **输出**：具有源运动语义的动态目标 3DGS 场景。

### 关键设计决策

流水线中的两个关键设计决策直接回应了核心瓶颈：

- **锚点插值机制**：替代逐视角独立优化嵌入的方式，通过 $\mathbf{m}_\phi = \mathrm{slerp}(\mathbf{m}_i, \mathbf{m}_j, \frac{\phi - \phi_i}{\phi_j - \phi_i})$ 实现运动嵌入的连续视角插值，解决了单全局嵌入收敛慢、泛化差的问题（Table 2：新视角 MSE 低至 0.0028）。
- **ARAP Rotation + LPIPS 损失**：在 4D 固化阶段，标准 ARAP 损失仅约束位置偏移，无法限制旋转自由度，导致结构伪影；显式施加旋转刚性约束（ARAP Rotation）并替换像素级 MSE 为 LPIPS 感知损失，显著提升重建结构完整性与 CLIP 分数（Table 3：从 0.9423 提升至 0.9636）。

### 与基线方法的本质差异

相较于改编的 **SC4D**（依赖文本描述，易引入外观不一致）和 **DreamGaussians4D**（使用 SDS 损失，易导致高斯坍缩和模糊），本方法的流水线在以下三处进行了根本性改造：

| 改造槽位 | 基线做法 | 本方法做法 |
|---------|---------|-----------|
| 运动嵌入策略 | 逐视角独立优化 | 锚点 slerp 插值协同优化 |
| 重建损失函数 | 像素级 MSE | LPIPS 感知损失 |
| 旋转正则化 | 标准 ARAP（仅约束位置） | ARAP Rotation 显式约束旋转 |

这些改造使得本方法成为唯一能在保持目标身份的同时实现高质量运动迁移的框架（人类评估外观质量 4.66/5，Fig. 5）。

### 补充图表

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2511_14848/figures/001_Figure_1.jpg]]
*Figure 1: Semantic 3D Motion Transfer in Action. Our method extracts motion embeddings from a multiview video and applies them to a static 3D Gaussian Splatting (3DGS) asset, bringing it to life with motion that matches the semantics of the source. Left: A bird’s wing flapping motion is transferred to an elephant cartoon’s ears. Right: A horse’s rearing motion animates a vehicle lifting its front wheels. We encourage watching the supplementary video for a clearer depiction of motion, which is best appreciated in dynamic form*

## 核心模块与公式推导

### 3.1 结构化多视角运动反演（Structured Multiview Motion Inversion）

本模块的目标是从源多视角视频中提取可泛化的运动表征。直接为每个视角独立优化运动嵌入存在两个瓶颈：一是无法泛化到未见视角，二是优化效率低下。为此，方法引入**基于锚点的视角感知运动嵌入机制**。

具体而言，在源视角范围内均匀分布 $K$ 个锚点嵌入 $\{\mathbf{m}_k\}_{k=1}^K$。当需要某个特定方位角 $\phi$ 的运动嵌入时，通过球面线性插值（slerp）从两个最近锚点合成：

$$
\mathbf{m}_{\phi} = \mathrm{slerp}\left(\mathbf{m}_i, \mathbf{m}_j, \frac{\phi - \phi_i}{\phi_j - \phi_i}\right)
$$

其中 $\mathbf{m}_i$、$\mathbf{m}_j$ 为距离 $\phi$ 最近的两个锚点嵌入，$\phi_i$、$\phi_j$ 为对应的方位角。这一插值机制使得不同视角的运动嵌入共享底层三维运动信息，是实现跨视角一致性的关键因果调节变量。

锚点嵌入通过联合优化去噪分数匹配损失获得。训练循环中，每次随机采样一个源视角视频 $\mathcal{V}_S[i]$（方位角 $\phi$），利用插值得到的 $\mathbf{m}_{\phi}$ 作为条件，最小化以下目标：

$$
\{\mathbf{m}_k^{*}\}_{1}^{K} = \underset{\{\mathbf{m}_k\}}{\mathrm{argmin}}\ \mathbb{E}\left[\lambda_{\sigma} \| D_{\theta}(\widetilde{\mathcal{V}}_S[i]; \sigma, \mathbf{m}_{\phi}) - \mathcal{V}_S[i] \|_2^2\right]
$$

其中 $D_{\theta}$ 为冻结的视频扩散模型去噪器，$\widetilde{\mathcal{V}}_S[i]$ 为加噪后的视频，$\sigma$ 为噪声水平，$\lambda_{\sigma}$ 为噪声相关的权重系数。

**对比基准**：若采用逐视角独立优化（即 Eq. 4 的朴素方案），每个视角需单独优化一个嵌入，不仅计算开销大，且嵌入之间无信息共享，导致新视角运动合成完全失败（Table 2 中 MSE 高达 0.0926）。若采用单一全局嵌入，则无法编码视角依赖的运动差异——例如方位角 $0^\circ$ 和 $180^\circ$ 下二维运动方向完全相反，单一嵌入会过拟合到某一视角的运动模式（Fig. 16），新视角 LPIPS 达 0.0709。

**锚点数量的权衡**：消融实验表明（Fig. 8），锚点数 $K=5$ 在收敛速度与重建质量之间取得最佳平衡。锚点过少（如 $K=1$，即全局嵌入）收敛最慢且最终性能最差；锚点过多则因优化变量增加而降低收敛速度。

### 3.2 视角感知语义运动迁移（View-aware Semantic Motion Transfer）

获得运动嵌入后，本模块负责生成用于驱动目标物体的监督视频。对目标物体的每个渲染视角，利用对应的插值运动嵌入 $\mathbf{m}_{\phi}$ 和渲染的首帧图像作为条件，通过视频扩散模型生成该视角下的运动视频序列。这些生成视频随后作为 4D 重建阶段的监督信号。

需要指出的是，此阶段生成的监督视频存在固有噪声和视点不一致伪影（Fig. 10–12），这构成了后续 4D 重建模块必须解决的核心瓶颈。

### 3.3 四维重建（4D Consolidation）

本模块将噪声监督视频转化为目标 3DGS 物体的高质量动态重建，其核心因果调节变量包括两个关键设计：**ARAP Rotation 约束**和 **LPIPS 感知损失**。

#### 3.3.1 控制点驱动的变形框架

在目标 3DGS 物体表面采样一组控制点，通过变形场网络 $\Psi$ 预测每一帧下控制点的位移，进而驱动整个高斯场的变形。控制点的原始位置记为 $\mathbf{p}_i$，第 $t$ 帧的变形位置记为 $\mathbf{p}_i^t$。

#### 3.3.2 ARAP Rotation 机制

标准 ARAP 损失仅约束相邻控制点的相对位置保持刚性，但未显式约束旋转，导致变形过程中出现结构扭曲。本方法引入显式旋转约束。首先估计每个控制点邻域的最优旋转矩阵：

$$
\hat{R}_k^t = \underset{R}{\mathrm{argmin}} \sum_{i \in \mathcal{N}_k} w_{ik} \| (\mathbf{p}_i^t - \mathbf{p}_k^t) - R(\mathbf{p}_i - \mathbf{p}_k) \|^2
$$

其中 $\mathcal{N}_k$ 为控制点 $k$ 的邻域集合，$w_{ik}$ 为权重。随后将估计的旋转纳入 ARAP 损失：

$$
\mathcal{L}_{ARAP} = \sum_{t \in 1..F} \sum_{i \in \mathcal{N}_k} w_{ik} \| (\mathbf{p}_i^t - \mathbf{p}_k^t) - \hat{R}_k^t (\mathbf{p}_i - \mathbf{p}_k) \|^2
$$

该损失强制局部区域在变形时保持尽可能刚性的变换，有效抑制非物理的结构扭曲。

#### 3.3.3 LPIPS 感知损失

监督视频中的噪声和视点不一致使得像素级 MSE 损失难以有效优化——逐像素对齐会过拟合到噪声模式，导致重建质量下降。方法将像素级损失替换为 LPIPS 感知损失，在特征空间而非像素空间计算差异，对局部纹理偏移和光照变化具有更强的鲁棒性。

**消融证据**（Table 3, Fig. 7）：朴素重建（仅使用像素损失和标准 ARAP）的 CLIP 分数为 0.9423，加入 ARAP Rotation 后提升至 0.9608，进一步加入 LPIPS 后达到 0.9636。定性结果显示，ARAP Rotation 消除了结构伪影，LPIPS 则显著改善了纹理细节保真度。人类偏好研究（Fig. 5 右）同样证实两者对感知质量的实质性提升。

#### 3.3.4 课程学习策略

对于运动幅度较大的场景，方法采用课程学习策略：先在较少帧上优化，逐步增加帧数。消融实验（Fig. 9）表明，无课程学习时模型难以泛化，产生断裂的运动过渡；课程学习则能引导模型学习平滑、自然的运动轨迹。

**关于 SDS 损失的说明**：实验尝试了 SDS 损失及其变体，但发现 SDS 会导致高斯坍缩和模糊（Fig. 15），原因在于 SVD 的单步去噪预测本身模糊。虽然 SDS 变体与 ARAP+LPIPS 结合后有所改进，但显著增加了优化时间，故最终未采用。

### 3.4 公式汇总

| 公式 | 含义 | 所属模块 |
|------|------|----------|
| $\mathbf{m}_{\phi} = \mathrm{slerp}(\mathbf{m}_i, \mathbf{m}_j, \frac{\phi - \phi_i}{\phi_j - \phi_i})$ | 锚点球面线性插值，合成任意视角的运动嵌入 | 结构化多视角运动反演 |
| $\{\mathbf{m}_k^{*}\} = \underset{\{\mathbf{m}_k\}}{\mathrm{argmin}}\ \mathbb{E}[\lambda_{\sigma} \| D_{\theta}(\widetilde{\mathcal{V}}_S[i]; \sigma, \mathbf{m}_{\phi}) - \mathcal{V}_S[i] \|_2^2]$ | 联合优化所有锚点嵌入的去噪分数匹配目标 | 结构化多视角运动反演 |
| $\hat{R}_k^t = \underset{R}{\mathrm{argmin}} \sum_{i \in \mathcal{N}_k} w_{ik} \| (\mathbf{p}_i^t - \mathbf{p}_k^t) - R(\mathbf{p}_i - \mathbf{p}_k) \|^2$ | 估计控制点邻域的最优刚性旋转矩阵 | 4D 重建（ARAP Rotation） |
| $\mathcal{L}_{ARAP} = \sum_{t} \sum_{i \in \mathcal{N}_k} w_{ik} \| (\mathbf{p}_i^t - \mathbf{p}_k^t) - \hat{R}_k^t (\mathbf{p}_i - \mathbf{p}_k) \|^2$ | 尽可能刚性损失，约束局部变形保持旋转一致性 | 4D 重建（ARAP Rotation） |
| $C = \sum_i c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$ | 三维高斯泼溅的透明度混合，计算最终像素颜色 | 基础渲染（3DGS 标准公式） |

## 实验与分析

### 主要结果对比

本文在 **Mini-Mixamo** 和 **Cross-Category** 两个基准上对方法进行了定量评估，对比的基线方法包括 **SC4D**（从文本描述驱动的 2D-to-4D 生成方法改编）和 **DreamGaussians4D (DG4D)**（从图像到 4D 的生成方法改编，使用目标的原始 3DGS 作为输入）。需要注意的是，这两个基线并非原生设计用于多视角视频的运动迁移任务，SC4D 依赖文本描述可能引入外观不一致，因此对比结果需在此前提下理解。

**Table 1** 展示了主要定量结果，本方法在运动保真度和语义一致性上均显著优于两个基线：

| 基准 | 指标 | Ours | SC4D | DG4D | 提升幅度 |
|------|------|------|------|------|----------|
| Mini-Mixamo | Motion Fidelity↑ | **0.74** | 0.65 | 0.61 | +0.09 / +0.13 |
| Cross-Category | Motion Fidelity↑ | **0.66** | 0.56 | 0.54 | +0.10 / +0.12 |
| Mini-Mixamo | CLIP Score↑ | **0.963** | 0.905 | 0.945 | +0.058 / +0.018 |
| Mini-Mixamo | CLIP-I↑ | **0.950** | 0.888 | 0.931 | +0.062 / +0.019 |
| Cross-Category | CLIP-I↑ | **0.948** | 0.872 | 0.908 | +0.076 / +0.040 |

在交叉类别迁移场景下，本方法的 Motion Fidelity 达到 0.66，比 SC4D 高 0.10，比 DG4D 高 0.12，表明锚点插值机制能够有效捕获跨视角共享的三维运动信息，即使源和目标在几何结构上差异显著。

**定性对比**（Fig. 3）进一步揭示：SC4D 因依赖文本描述驱动生成，难以保持目标物体的外观身份；DG4D 虽然直接操作目标 3DGS，但在运动迁移的准确性上明显不足。相比之下，本方法是唯一能够在保持目标身份的同时实现高质量运动迁移的方案。

**人类评估**（Fig. 5 左）印证了这一结论：本方法在外观质量上获得 4.66/5 的平均主观评分，显著领先；运动质量评分与 SC4D 相当，但结合外观保持能力，整体表现最优。

### 新视角运动合成

**Table 2** 报告了新视角运动合成的定量结果，评估指标为仅计算在训练中未见视角上的 MSE 和 LPIPS：

| 方法 | MSE↓ | LPIPS↓ |
|------|------|--------|
| 逐视角独立优化嵌入（Eq.4） | 0.0926 | 0.3874 |
| 单全局嵌入 | 0.0038 | 0.0709 |
| **锚点插值（Ours）** | **0.0028 ± 0.0016** | **0.0403 ± 0.0170** |

逐视角独立优化嵌入完全无法泛化到新视角，MSE 高达 0.0926，LPIPS 达 0.3874。单全局嵌入虽然有所改善，但收敛速度最慢且最终性能仍逊于锚点机制。本方法的锚点插值机制通过 slerp 在相邻锚点间共享运动信息，实现了最低的 MSE（0.0028）和 LPIPS（0.0403），验证了“不同视角的运动嵌入共享底层三维运动信息”这一核心洞察。

**定性结果**（Fig. 6, Fig. 14）显示，简单插值和全局嵌入在新视角下产生明显的运动失真和外观伪影，而锚点机制成功恢复了与源运动一致的动态表现，即使应用于不同的目标物体。

### 消融实验

**Table 3** 和 **Fig. 7** 系统消融了 4D 重建流程中的关键设计选择：

| 配置 | CLIP Score↑ | Motion Fidelity↑ | 备注 |
|------|-------------|------------------|------|
| Naive（像素级 MSE + 标准 ARAP） | 0.9423 | — | 几何和纹理伪影严重 |
| + ARAP Rotation | 0.9608 | — | 结构完整性显著改善 |
| + ARAP Rotation + LPIPS | **0.9636** | 变化不大 | 纹理细节和感知质量最佳 |

**因果机制分析**：
1. **ARAP Rotation 的作用**：标准 ARAP 损失仅约束控制点的相对位置，未显式约束局部旋转，导致变形过程中出现非刚性扭曲。引入 ARAP Rotation 机制后，通过显式计算并施加局部最优旋转约束（Eq. 8），使变形保持局部刚性，CLIP 分数从 0.9423 提升至 0.9608。
2. **LPIPS 感知损失的作用**：监督视频由视频扩散模型生成，存在噪声和视点不一致伪影。像素级 MSE 损失强制逐像素对齐，会将噪声传播到重建结果。LPIPS 在感知特征空间计算损失，对高频噪声和轻微视点偏移具有鲁棒性，进一步将 CLIP 分数提升至 0.9636。

值得注意的是，Motion Fidelity 指标在消融中变化不大，这暴露了 MF3D 指标的局限性——该指标对轨迹对齐敏感，但无法反映结构完整性和纹理细节的改善。人类偏好研究（Fig. 5 右）则明确显示，LPIPS 和 ARAP Rotation 均显著提升了感知质量。

**锚点数量 K 的敏感性**（Fig. 8, Section 6.5）：锚点数量过少会导致运动信息共享不足，优化收敛缓慢且最终质量差；锚点数量过多则增加计算开销。实验表明 K=5 在收敛速度与重建质量之间取得最佳平衡。单全局嵌入（K=1）收敛最慢且最终性能最差，进一步验证了多锚点协作的必要性。

**课程学习的作用**（Fig. 9, Appendix B.2）：在运动幅度较大的场景中，直接进行全帧 4D 重建会导致高斯控制点出现阶梯式运动过渡。课程学习策略通过逐步增加时间帧数，使模型先学习粗略运动模式再细化，是实现平滑运动过渡的关键。

**SDS 损失的失败分析**（Fig. 15, Appendix E.2）：实验尝试在 4D 重建阶段引入 SDS 损失或其变体（Iterative Dataset Update），但发现 SDS 损失导致高斯坍缩和模糊伪影。根本原因在于底层视频扩散模型（SVD）的单步去噪预测本身模糊，无法提供有效的梯度信号。尽管 SDS 变体与 ARAP+LPIPS 结合后有改进，但显著增加了优化时间，因此最终方案未采用。

### 失败模式分析

本方法存在以下已知失败模式：

1. **高关节活动场景**（Fig. 12, Fig. 13）：对于踢腿、跳跃等高关节复杂度的运动，逐视角运动反演容易失败。具体表现为：生成的监督视频出现严重视点不一致和伪影（Fig. 12），这些噪声通过 4D 重建管道传播，导致最终动态场景出现可见伪影（Fig. 13）。根本瓶颈在于底层视频扩散模型对复杂运动的 2D 反演能力不足。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2511_14848/figures/016_Figure_13.jpg]]
*Figure 13: Final result example - Failure case. Final result rendered at a 45° angle, showing the kicking motion on the woman figure. The video supervisions leading to this failure are shown in Fig. 12*

2. **2D 反演上限约束**：方法整体受限于预训练视频扩散模型的运动反演能力。当 2D 反演本身失败时，后续的锚点插值和 4D 重建均无法恢复正确的运动信息。

3. **指标局限性**：MF3D 指标对轨迹对齐敏感，但无法反映结构完整性和纹理细节。消融实验中观测到：某些配置下 MF3D 变化不大，但视觉质量差异显著，可能导致对重建质量的高估。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | 本方法在 Motion Fidelity 和 CLIP 分数上全面超越 SC4D 和 DG4D |
| Fig. 3 | 本方法是唯一保持目标身份的方法，基线存在外观漂移或运动不准确 |
| Fig. 5 左 | 外观质量评分 4.66/5，运动质量与 SC4D 相当 |
| Table 2 | 锚点插值在新视角运动合成上 MSE 低至 0.0028，远超简单插值和全局嵌入 |
| Fig. 6 | 锚点机制成功泛化到未见视角，其他方法产生运动失真 |
| Table 3 | ARAP Rotation + LPIPS 将 CLIP 分数从 0.9423 提升至 0.9636 |
| Fig. 7 | ARAP Rotation 修复结构伪影，LPIPS 保留纹理细节 |
| Fig. 8 | K=5 锚点在收敛速度与质量间最优，单全局嵌入最差 |
| Fig. 9 | 课程学习对平滑运动过渡至关重要，否则出现阶梯式运动 |
| Fig. 12/13 | 高关节活动下监督视频严重伪影，导致最终结果失败 |
| Fig. 15 | SDS 损失导致高斯坍缩，不适合本任务的 4D 重建 |

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2511_14848/figures/003_Table_1.jpg]]
*Table 1: Quantitative Comparison with Baselines. Our method achieves significantly higher Motion Fidelity, CLIP-I, and CLIP similarity scores across both benchmarks compared to the baselines. We encourage the reader to refer to Figure 3 for a visual illustration of these improvements*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2511_14848/figures/006_Table_2.jpg]]
*Table 2: Quantitative results for Novel-view Motion Synthesis using MSE and LPIPS. Metrics are computed only on viewing angles unseen during training*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2511_14848/figures/018_Table_3.jpg]]
*Table 3: Ablation study results*

### 补充图表

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2511_14848/figures/009_Figure.jpg]]

## 方法谱系与知识库定位

### 核心问题与解决思路

**Gaussian See, Gaussian Do** 瞄准一个此前未被充分解决的核心瓶颈：**对任意无骨架三维物体进行语义有意义的跨类别运动迁移**。现有方法要么依赖骨架绑定（需人工标注且仅适用于同类别物体），要么通过文本/图像条件生成运动（难以精确控制运动语义），要么直接使用视频扩散模型生成监督信号（面临噪声和视点不一致问题）。本方法的因果调控旋钮在于三点协同创新：**(1) 基于锚点的视角感知运动嵌入机制**（通过 slerp 插值实现跨视角信息共享和加速收敛）、**(2) ARAP Rotation 旋转约束**（显式约束局部旋转的刚性）、**(3) LPIPS 感知损失**（替代像素级 MSE 损失以抑制监督视频中的噪声和视点不一致伪影）。

### 与基线方法的差异定位

**SC4D**（adapted 2D-to-4D generation baseline）和 **DreamGaussians4D (DG4D)**（adapted image-to-4D model with SDS loss）是本方法的主要对比基线。需注意，这两个基线并非原生设计用于多视角视频运动迁移：SC4D 通过目标物体的文本描述条件进行生成，可能引入外观不一致；DG4D 使用 SDS 损失和目标的原始 3DGS 进行图像到 4D 的生成。本方法在以下关键维度上做出了差异化设计：

| 设计维度 | SC4D / DG4D（基线） | Gaussian See, Gaussian Do（本方法） |
|---------|-------------------|----------------------------------|
| **运动嵌入策略** | 逐视角独立优化嵌入 | 基于锚点的球面线性插值（slerp）嵌入，跨视角共享底层三维运动信息 |
| **重建损失函数** | 像素级 MSE 损失 | LPIPS 感知损失，在感知空间而非像素空间进行监督 |
| **旋转正则化** | 标准 ARAP 损失（仅约束位置） | ARAP Rotation 机制，显式约束局部旋转的刚性 |
| **身份保持** | 外观可能漂移（SC4D 依赖文本描述） | 唯一能保持目标身份的方法（人类评估外观质量 4.66/5） |

这些差异直接转化为量化优势：在 Mini-Mixamo 基准上，Motion Fidelity 达到 **0.74**（vs SC4D 0.65, DG4D 0.61），CLIP Score 达到 **0.963**（vs SC4D 0.905, DG4D 0.945）；在 Cross-Category 基准上，Motion Fidelity 达到 **0.66**（vs SC4D 0.56, DG4D 0.54）。

### 关键技术谱系

本方法处于 **视频扩散模型运动理解** 与 **动态三维高斯泼溅重建** 的交叉地带：

- **运动提取侧**：继承视频扩散模型（Stable Video Diffusion）的条件反演范式，通过去噪分数匹配损失从源视频中提取运动嵌入。创新点在于引入锚点插值机制，将逐视角独立优化转化为协作优化，使运动嵌入具备视角泛化能力。

- **三维表示侧**：基于 3D Gaussian Splatting (3DGS) 的动态场景表示，通过控制点驱动变形场网络实现运动迁移。这与 SC4D 的 4D 表示和 DG4D 的 SDS 优化形成对比——后者在实验中导致高斯坍缩和模糊（见 Fig. 15），而本方法的 ARAP Rotation + LPIPS 组合有效避免了这一问题。

- **正则化设计**：ARAP Rotation 机制从经典几何处理中的 As-Rigid-As-Possible 变形演化而来，但将其扩展到显式约束旋转矩阵，解决了标准 ARAP 仅约束位置导致的旋转自由度不受控问题。LPIPS 感知损失的引入借鉴了图像生成领域的感知质量评估思想，将其应用于动态重建中的噪声抑制。

### 适用边界与局限

1. **高关节活动场景失效**：对踢腿、跳跃等大幅度关节运动效果不佳。根本原因在于逐视角运动反演在这些场景下容易失败，导致监督视频产生严重伪影并传播至最终重建结果（见 Fig. 12-13 的失败案例）。

2. **受限于底层视频扩散模型的反演能力**：当 2D 反演本身失败时，方法无法恢复。这是一个上游依赖瓶颈，而非本方法特有缺陷。

3. **新视角运动合成功能尚未完全集成**：虽然锚点机制在独立的新视角运动合成实验中表现优异（MSE 低至 0.0028，LPIPS 0.0403），但该能力尚未完全融入运动迁移管线以进一步提升整体性能。

4. **指标局限性**：所使用的 MF3D 指标对轨迹对齐敏感，但对结构完整性和纹理细节不敏感。消融实验中观测到高分但重建质量差的情况，提示该指标可能高估部分重建质量。

5. **计算开销**：条件反演和 4D 重建的优化过程存在一定计算开销。锚点机制虽有所加速（K=5 在收敛速度与质量间取得最佳平衡），但仍需分钟量级的时间。

### 开放问题

- **如何改进高关节复杂性运动的逐视角运动反演**，以减少监督伪影？这是当前失效模式的核心瓶颈。
- **能否开发更具综合性且对结构失真敏感的 3D 语义运动评估指标**，弥补 MF3D 的盲区？
- **可否将锚点嵌入的新视角合成能力完全融入运动迁移管道**，实现更强的泛化和更少的人工指定视角？
- **如何进一步减少条件反演和锚点优化的运行时间**，使其更适用于实时或交互式应用？
- **能否通过引入时间一致性正则化或改进生成模型来提升监督视频的质量和视点一致性**，从上游解决噪声传播问题？

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Gaussian_See_Gaussian_Do_3D_Semantic_Motion_Transfer.pdf]]

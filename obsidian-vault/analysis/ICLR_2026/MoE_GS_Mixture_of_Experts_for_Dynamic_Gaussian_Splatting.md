---
title: "MoE-GS: Mixture of Experts for Dynamic Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MoE_GS_Mixture_of_Experts_for_Dynamic_Gaussian_Splatting_610a761de4a8.pdf
project_link: "https://cvsp-lab.github.io/MoE-GS"
code_link: null
aliases:
- MGMEDGS
- MoE-GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入专家混合（MoE）架构，自适应地选择和融合多个具有互补变形先验的专家模型，使得每个局部时空区域都能被最适合的变形策略处理，从而整体提升动态重建质量。
primary_logic: 在2D图像空间进行专家输出混合，同时利用可微分的体素感知权重投射将3D几何信息注入路由过程，既保证了训练稳定性，又能保持细节保真度。同时，通过知识蒸馏将MoE模型的性能迁移到单一专家，实现轻量化部署，弥合了质量与效率之间的差距。
claims:
- MoE-GS在N3V和Technicolor数据集上的平均PSNR均超过所有单专家基线及NeRF类方法
- Volume-aware Pixel Router在定量和定性上均显著优于纯像素路由和纯体素路由
- 在多次重复训练中，MoE-GS始终稳定优于任何单一专家模型
- 蒸馏后的单一专家模型性能大幅超越原基线，逼近MoE-GS，验证了知识蒸馏的有效性
---

# MoE-GS: Mixture of Experts for Dynamic Gaussian Splatting

> [!tip] 核心洞察
> 在2D图像空间进行专家输出混合，同时利用可微分的体素感知权重投射将3D几何信息注入路由过程，既保证了训练稳定性，又能保持细节保真度。同时，通过知识蒸馏将MoE模型的性能迁移到单一专家，实现轻量化部署，弥合了质量与效率之间的差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoE-GS：用于动态高斯泼溅的专家混合 |
| 英文题名 | MoE-GS: Mixture of Experts for Dynamic Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=WrEQFwWCdT) · [Project](https://cvsp-lab.github.io/MoE-GS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoE-GS (Mixture of Experts for Dynamic Gaussian Splatting) |
| Dataset | N3V, Technicolor |

> [!tip] 效果简介
> - N3V (Neural 3D Video) 上，Average PSNR (dB) ↑ 33.27 (MoE-GS N=4) vs 32.33 (E-D3DGS, 最佳单一专家) (+0.94)。
> - Technicolor 上，Average PSNR (dB) ↑ 34.55 (MoE-GS N=3) vs 33.69 (STG, 最佳单一专家) (+0.86)。
> - N3V (效率) 上，PSNR / FPS / Memory 32.80 / 83 / 351.2 MB (55% pruning, N=2) vs 31.92 / 88.5 / 609.5 MB (STG) (PSNR +0.88, FPS 接近, 内存更小)。

## 概要

动态场景重建的核心挑战在于**场景级、空间级和时间级的不一致性**：没有任何单一变形先验能够在所有区域和所有时间步上同时达到最优重建质量。现有动态高斯泼溅方法（如 **4DGaussians** (Wu et al., 2024)、**E-D3DGS** (Bae et al., 2024)、**STG** (Li et al., 2024)、**Ex4DGS** (Lee et al., 2024)）各自擅长处理特定类型的运动模式（静止、快速、平滑、不规则等），但在跨场景、跨区域和跨时间的泛化上均表现出明显的性能波动（Figure 1）。这一瓶颈的本质在于：**单一模型无法普适地处理现实场景中多样化的动态行为**。

针对上述问题，本文提出 **MoE-GS（Mixture of Experts for Dynamic Gaussian Splatting）**，将专家混合（MoE）架构引入动态高斯泼溅。其核心思路是：集成多个具有互补变形先验的专家模型，通过一个可学习的 **Volume-aware Pixel Router** 自适应地为每个局部时空区域选择和融合最合适的专家输出。该路由器在 2D 图像空间进行混合，同时通过可微分的体素感知权重投射将 3D 几何信息注入路由过程，兼顾训练稳定性与细节保真度。此外，MoE-GS 引入**知识蒸馏**策略，将多专家模型的性能迁移至单一专家，弥合质量与效率之间的差距。

**核心结论**：
- 在 **N3V** 和 **Technicolor** 两个数据集上，MoE-GS 的平均 PSNR 分别达到 **33.27 dB** 和 **34.55 dB**，一致超越所有单专家基线及 NeRF 类方法（Table 1, Table 2）。
- Volume-aware Pixel Router 在定量和定性上均显著优于纯像素路由和纯体素路由（Table 4, Figure 5）。
- 多次重复训练中，MoE-GS 始终稳定优于任何单一专家模型，排除了方差优势（Table 12）。
- 蒸馏后的单一专家模型性能大幅超越原基线并逼近 MoE-GS，验证了知识蒸馏的有效性（Table 7, Table 11）。

**方法定位**：MoE-GS 属于动态高斯泼溅方法的框架级改进，通过可学习的专家选择与融合机制，在不改变各专家内部结构的前提下，系统性地提升了动态场景的重建质量与鲁棒性。其知识蒸馏管线进一步为高质量动态重建的轻量化部署提供了可行路径。



**动态场景重建的核心瓶颈：单一变形先验的普适性困境**

动态高斯泼溅（Dynamic Gaussian Splatting）已成为新视角合成的前沿范式，其核心思路是为静态高斯表征引入时变变形场，从而在紧凑的显式几何基元上刻画场景运动。然而，现有方法在变形建模策略上存在根本性的分歧——不同方法采用截然不同的变形先验，包括基于每高斯嵌入的形变（如 **E-D3DGS**，Bae et al., 2024）、基于多项式轨迹的运动建模（如 **STG**，Li et al., 2024）、基于时空插值的变形（如 **Ex4DGS**，Lee et al., 2024），以及基于HexPlane编码的变形场（如 **4DGaussians**，Wu et al., 2024）。

**问题本质在于：没有一种单一的变形先验能够在所有场景、所有空间区域和所有时间步上同时达到最优。** 这一结论得到了系统性的实证支撑（Figure 1）：

- **场景级不一致性**：同一方法在不同场景上的性能排名剧烈波动，没有任何方法能够一致地占据主导地位。
- **空间级不一致性**：在单帧图像内部，不同空间区域对不同变形模型表现出显著偏好——例如，静态背景区域可能更受益于保守的插值策略，而快速运动的前景区域则需要更灵活的多项式轨迹建模。
- **时间级不一致性**：在同一场景的不同时间步上，最优方法的选择会随运动模式的切换而动态变化，表明单一模型的时序泛化能力存在系统性盲区。

这种多维度不一致性的根源在于真实动态场景的运动复杂性：场景中同时存在静止区域、平滑运动、快速位移和不规则形变等多种模式，每种模式对应着不同的建模难度和最优先验。单一模型被迫在所有区域和时间步上使用相同的变形策略，必然在部分局部区域产生次优重建。

**现有方法缺口**：尽管已有工作尝试通过改进单一变形场的表达能力来缓解上述问题，但这一思路存在理论上限——当变形先验的结构性假设与局部运动模式失配时，仅靠增大模型容量无法从根本上弥补建模偏差。另一方面，直接训练多个独立模型并在后处理阶段进行硬性选择或简单融合，则面临训练成本线性增长、融合策略缺乏可微优化、以及模型间缺乏协同等实际障碍。

**本文动机**：MoE-GS 的核心洞察是将“选择最优变形策略”这一决策本身建模为一个可学习的问题。通过引入专家混合（Mixture of Experts, MoE）架构，框架能够为每个局部时空区域自适应地选择和融合最合适的变形专家，从而突破单一先验的普适性瓶颈。这一思路将动态场景重建从“寻找一个万能模型”重新定义为“学习如何动态组合多个专用模型”，为弥合不同变形先验之间的性能差距提供了统一的解决方案。



## 核心方法与创新机理

MoE-GS 的核心创新在于将专家混合（Mixture of Experts, MoE）范式引入动态高斯泼溅（Dynamic Gaussian Splatting），通过架构层面三个相互协同的 **changed slots**，系统性解决了现有方法中单一变形先验无法普适处理复杂动态场景的根本瓶颈。

### 1. 模型架构：从单一先验到自适应专家融合

现有动态高斯方法（如 **STG** (Li et al., 2024)、**Ex4DGS** (Lee et al., 2024)、**E-D3DGS** (Bae et al., 2024)、**4DGaussians** (Wu et al., 2024)）各自依赖单一的变形先验（多项式轨迹、插值、每高斯嵌入或 HexPlane 嵌入），在场景级、空间级和时间级均存在不一致性——没有任何单一方法能在所有区域和时间步上同时达到最佳重建质量（Figure 1）。

MoE-GS 将上述方法集成为异构专家池，并引入 **Volume-aware Pixel Router** 实现自适应融合。该路由器通过为每个高斯分配可学习的权重向量 $\pmb{w}_i^{per} = [w_i, w_i^{dir}, (t \cdot w_i^{time})]^T$，编码视角和时间依赖信息，经可微分光栅化投射到像素空间后，由轻量 MLP 残差修正得到路由逻辑值 $R'(u)$，最终通过 Softmax 生成像素级专家融合权重 $G'_k(u)$（Eq. 2, 6-8）。这一设计将 3D 几何信息注入路由过程，既保证了训练稳定性，又能保持细节保真度。

消融实验证实，Volume-aware Pixel Router 在定量指标和定性细节保持上均显著优于纯 Pixel Router（忽略体积特征）和纯 Volume Router（难以优化），验证了 2D 混合与 3D 感知相结合的设计优势（Table 4, Figure 5）。

### 2. 渲染效率：单通道多专家渲染与门控感知剪枝

多专家模型面临计算开销随专家数量线性增长的挑战。MoE-GS 提出两项效率优化：

- **Single-Pass Multi-Expert Rendering**：通过为每个高斯分配 one-hot 专家身份标识 $(e_j)_k$，在一次光栅化中同时生成所有专家的着色图 $C_k(u)$（Eq. 9），消除了各专家独立执行投影与光栅化的冗余计算。
- **Gate-Aware Gaussian Pruning**：累积门控权重对每高斯参数的梯度作为重要性度量 $\mathcal{E}_i$（Eq. 10），剪除低贡献高斯。这一策略直接利用路由器已学习的时空注意力信号，无需额外的重要性评估网络。

消融实验表明，同时启用两项优化可大幅提升 FPS 并降低内存占用，而 PSNR 损失极小（Table 5）。在 N=2 专家配置下，经 55% 剪枝的 MoE-GS 以接近单专家的推理速度（83 FPS）和更小的内存（351.2 MB），实现了超越最佳单专家基线（STG, 31.92 dB）的 PSNR（32.80 dB）（Table 3）。

### 3. 部署模式：知识蒸馏弥合质量-效率差距

完整 MoE-GS 的推理开销仍高于单专家模型。MoE-GS 提出知识蒸馏策略，利用 MoE 渲染图像作为伪监督，结合路由器权重引导，重新训练各专家模型。蒸馏损失函数（Eq. 11）同时约束专家输出逼近真值（在路由器关注区域）和 MoE 输出（在路由器忽略区域），使单专家模型能继承 MoE 的融合知识。

蒸馏后的单专家模型性能大幅超越原基线，逼近完整 MoE-GS（Table 7, Table 11），验证了该策略的有效性。这一设计使得在实际部署中可以用单一模型的成本获得接近多专家融合的质量，弥合了质量与效率之间的关键差距。

### 创新点之间的因果关联

上述三个 changed slots 形成递进闭环：**自适应架构**提供质量上限，**效率优化**降低多专家推理成本，**知识蒸馏**将 MoE 能力迁移至轻量部署模型。三者共同支撑了 MoE-GS 在 N3V 和 Technicolor 数据集上一致超越所有单专家基线和 NeRF 类方法的实验结果（Table 1, Table 2）。



MoE-GS 的整体框架遵循“先多样化、后自适应融合”的两阶段设计，将多个异构的动态高斯泼溅专家集成到一个统一的 Mixture of Experts 架构中。如 Figure 2 所示，整个 pipeline 由两个核心阶段构成：

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the MoE-GS framework. In Stage 1 (Expert Training), each expert is independently trained to reconstruct the dynamic scene by optimizing its own Gaussian representation, ensuring diverse modeling capabilities. In Stage 2 (Router Training), with all expert parameters fixed, the Volume-aware Pixel Router learns to dynamically blend expert-rendered images by computing spatially and temporally adaptive gating weights. The Candidate Experts (right) illustrate diverse Gaussian-based reconstruction methods integrated into our framework, including HexPlane Embedding-based, Per-Gaussian embedding-based, Interpolation-based, and Polynomial-based approaches, each suited for capturing differ...*

**第一阶段：独立专家训练（Expert Training）**  
各候选专家在完全相同的训练数据和超参数设置下独立优化自身的高斯表征与变形参数。这些专家覆盖了当前动态高斯泼溅的主流变形先验，包括基于 HexPlane 嵌入的方法、逐高斯嵌入的方法、基于插值的方法以及基于多项式轨迹的方法。独立训练确保了每个专家具备差异化的场景建模能力，从而为后续的专家混合提供互补的重建特性。

**第二阶段：路由器训练（Router Training）**  
在所有专家参数冻结的前提下，引入 Volume-aware Pixel Router 学习空间-时间自适应的像素级融合权重。该路由器的核心机制是将高斯层级的可学习权重通过可微分权重投射（differentiable weight splatting）投影到 2D 像素空间，再经轻量 MLP 残差修正得到最终的路由逻辑值。这一设计同时利用了 3D 体素几何信息和 2D 像素着色信息，解决了纯像素路由忽略几何结构、纯体素路由难以优化的问题。

**推理与效率优化**  
在推理阶段，MoE-GS 采用单通道多专家渲染（Single-Pass Multi-Expert Rendering）：所有专家的高斯被合并，通过 one-hot 身份标识在一次光栅化中同时生成各专家的着色图，消除了重复投影与可见性计算。此外，门控感知高斯剪枝（Gate-Aware Gaussian Pruning）累积门控权重对每高斯参数的梯度作为重要性度量，剪除低贡献高斯，进一步压缩模型体积。

**知识蒸馏部署**  
为弥合多专家推理的计算开销与单专家部署的效率需求之间的差距，MoE-GS 引入知识蒸馏策略。利用 MoE 渲染图像作为伪监督信号，结合路由器权重引导的蒸馏损失，重新训练各单一专家模型，使其逼近 MoE 的渲染品质。这一策略使得蒸馏后的单专家模型在显著降低计算成本的同时，性能大幅超越原始基线。

框架的输入为多视角动态视频帧及其对应的相机参数与时间戳，输出为任意新视角、新时刻的渲染图像。整个流程中，第一阶段产出多样化的专家表征，第二阶段产出自适应融合权重，最终通过加权混合得到渲染结果。



### 3.1 标准 MoE 形式化

MoE-GS 将动态场景重建建模为一个专家混合问题。给定输入 $x$（在本文中为时空坐标），标准 MoE 的输出为各专家输出的加权和：

$$\mathbf{MoE}(x) = \sum_{k=1}^{N} G_k(x) \cdot E_k(x) \tag{1}$$

其中 $E_k(x)$ 为第 $k$ 个专家的输出，门控权重 $G_k(x)$ 通过 softmax 归一化得到：

$$G_k(x) = \mathrm{Softmax}(R_k(x)) \tag{2}$$

$R_k(x)$ 为路由器输出的原始逻辑值。这一形式化直接迁移到动态高斯泼溅中：每个专家 $E_k$ 是一个完整的动态高斯重建模型，输出其对该时空点的颜色预测，路由器则负责在像素级别自适应地融合这些预测。

### 3.2 Volume-aware Pixel Router

路由器的核心挑战在于如何将 3D 几何信息注入像素级融合决策。论文设计了三种路由器架构（Figure 3），并最终采用 **Volume-aware Pixel Router** 作为最优方案。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of Router Architectures. The Pixel Router (top-left) assigns weights purely at the pixel level, ignoring volumetric features. The Volume Router (bottom-left) uses Gaussian-level weights but is difficult to optimize. Our Volume-aware Pixel Router (right) combines Gaussian-level weights with rasterization-based splatting*

**每高斯可学习权重。** 每个高斯携带一组可学习权重，编码视角和时间依赖：

$$\pmb{w}_i^{per} = [w_i, w_i^{dir}, (t \cdot w_i^{time})]^T \tag{6}$$

其中 $w_i$ 为基础权重，$w_i^{dir}$ 编码视角方向依赖，$w_i^{time}$ 与时间戳 $t$ 相乘编码时间依赖。这些权重随高斯优化，构成体素级路由信息。

**可微分权重投射。** 将高斯级权重通过可微分光栅化投射到 2D 像素空间，得到像素级路由特征：

$$R'(u) = w_{2D}(u) + \Phi(w_{2D}^{dir}(u), w_{2D}^{time}(u), r(u)) \tag{7}$$

其中 $w_{2D}(u)$、$w_{2D}^{dir}(u)$、$w_{2D}^{time}(u)$ 分别为光栅化后的 2D 权重图，$r(u)$ 为像素 $u$ 的光线方向，$\Phi$ 为一个轻量 MLP，对投射后的权重进行残差修正，输出最终的路由逻辑值。这一设计的关键在于：3D 几何信息通过权重投射自然注入 2D 路由，而 MLP 仅做轻量残差修正，避免了纯体素路由的优化困难，也克服了纯像素路由忽略几何结构的缺陷。

**最终混合。** 将路由逻辑值通过 softmax 归一化，对各专家渲染图进行像素级加权融合：

$$I_{MoE}(u) = \sum_{k=1}^{N} G'_k(u) I_{E_k}(u) \tag{8}$$

其中 $G'_k(u) = \mathrm{Softmax}(R'_k(u))$，$I_{E_k}(u)$ 为第 $k$ 个专家在像素 $u$ 处的渲染颜色。整个路由器的训练发生在第二阶段，此时所有专家参数冻结，仅优化高斯权重和轻量 MLP，保证了训练的稳定性和效率。

### 3.3 单通道多专家渲染与门控感知剪枝

**单通道多专家渲染。** 在推理时，若每个专家独立执行投影和光栅化，计算开销将随专家数量线性增长。MoE-GS 通过为每个高斯分配 one-hot 专家身份标识 $(e_j)_k$，将所有专家的高斯合并后在一次光栅化中同时生成各专家的着色图：

$$C_k(u) = \sum_{j=1}^{M} T_j(u) \alpha_j(u) c_j \cdot (e_j)_k \tag{9}$$

其中 $M$ 为合并后的高斯总数，$T_j(u)$ 为透射率，$\alpha_j(u)$ 为不透明度，$c_j$ 为颜色，$(e_j)_k$ 为第 $j$ 个高斯对第 $k$ 个专家的 one-hot 指示。这一设计共享了投影和可见性计算，大幅减少冗余。

**门控感知高斯剪枝。** 为进一步降低内存和计算开销，利用门控权重对每高斯参数的梯度累积作为重要性度量：

$$\mathcal{E}_i = \frac{1}{|\mathcal{D}|} \sum_{v \in \mathcal{D}} \Bigl\| \frac{\partial G'_k(v)}{\partial \pmb{w}_i^{per}(v)} \Bigr\| \tag{10}$$

其中 $\mathcal{D}$ 为训练视角集合，$\frac{\partial G'_k(v)}{\partial \pmb{w}_i^{per}(v)}$ 为门控权重对每高斯可学习权重的梯度。重要性 $\mathcal{E}_i$ 低的低贡献高斯被剪除。实验表明（Table 5），55% 剪枝率下 PSNR 损失极小，FPS 接近单专家水平，内存显著降低。

### 3.4 知识蒸馏

MoE-GS 的多专家推理开销虽经优化，仍高于单专家。为此引入知识蒸馏策略，将 MoE 的性能迁移到单一专家。蒸馏损失结合真值和 MoE 渲染的伪标签，并由路由权重引导关注区域：

$$\mathcal{L}_k^{KD} = \lambda \cdot \mathcal{L}(G'_k \cdot I_{E_k}, G'_k \cdot I_{GT}) + (1-\lambda) \cdot \mathcal{L}((1-G'_k) \cdot I_{E_k}, (1-G'_k) \cdot I_{MoE}) \tag{11}$$

其中 $G'_k$ 为路由器分配给第 $k$ 个专家的权重，$I_{GT}$ 为真值图像，$I_{MoE}$ 为完整 MoE-GS 的渲染图像。第一项在高权重区域约束专家输出逼近真值，第二项在低权重区域约束其逼近 MoE 输出，使得蒸馏后的单专家模型在自身擅长的区域保持精度，在非擅长区域学习 MoE 的融合结果。实验验证了该蒸馏策略能一致提升单专家的 PSNR、SSIM 和 LPIPS（Table 7, Table 11），蒸馏后性能大幅超越原基线并逼近 MoE-GS。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/001_Figure_1.jpg]]
*Figure 1: Limitations of existing dynamic Gaussian splatting methods. (a) Scene-level: No single method consistently dominates across scenes. (b) Spatial-level: Different spatial regions favor different deformation models. (c) Temporal-level: The best-performing method changes over time within the same scene. We also visualize representative motion trajectories of four experts—4DGaussians (Green), STG (Purple), E-D3DGS (Pink), and Ex4DGS (black)—to illustrate their distinct motion behaviors. Additional video results are provided on the project page*



## 实验与关键发现

### 主实验结果

MoE-GS 在两个主流动态场景重建基准上均取得了最优的平均重建质量。在 N3V 数据集上，N=4 专家配置的 MoE-GS 达到 **33.27 dB** 的平均 PSNR，相比最佳单一专家基线 E-D3DGS（32.33 dB）提升 **+0.94 dB**（Table 1）。在 Technicolor 数据集上，N=3 专家配置以 **34.55 dB** 的平均 PSNR 超越最佳单一专家 STG（33.69 dB）**+0.86 dB**（Table 2）。值得注意的是，MoE-GS 的领先优势具有跨场景一致性——在 Table 1 和 Table 2 的逐场景细分中，MoE-GS 在绝大多数场景上均取得最优或次优指标，验证了混合专家策略对场景级不一致性问题的有效缓解。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/004_Table_1.jpg]]
*Table 1: Performance comparison on the N3V dataset (Li et al., 2022). †: Models were trained on a dataset split into 150 frames. We highlight best and second-best values for each metric*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/005_Table_2.jpg]]
*Table 2: Comparison results on the Technicolor dataset (Sabater et al., 2017)*

效率评估（Table 3）显示，N=2 专家变体（Ex4DGS + STG）在 55% 剪枝率下达到 **32.80 dB PSNR / 83 FPS / 351.2 MB**，相比 STG 的 31.92 dB / 88.5 FPS / 609.5 MB，PSNR 提升 +0.88 dB 的同时内存占用降低约 42%，FPS 仅轻微下降。这表明单通道多专家渲染与门控感知剪枝的组合能够在质量与效率之间取得实用平衡。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/007_Table_3.jpg]]
*Table 3: Efficiency evaluation with N=2 Expert Variants on N3V (Li et al., 2022)*

定性结果（Figure 4）进一步揭示了 MoE-GS 的融合机制：路由权重图显示，不同空间区域自适应地激活不同专家——例如静态背景区域倾向于激活 Ex4DGS，而快速运动区域则更多依赖 STG 或 E-D3DGS——最终混合结果在细节保真度上一致优于任一单独专家。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/006_Figure_4.jpg]]
*Figure 4: N3V Qualitative Results Comparison of our MoE-GS with other dynamic Gaussian splatting methods on Neural 3D Video dataset (Li et al., 2022). black background highlight the method that produces the most visually accurate result among the baselines for each region*

### 路由器架构消融

Table 4 和 Figure 5 系统比较了三种路由器变体：
- **Pixel Router**：直接在 2D 像素空间预测权重，忽略 3D 几何信息，导致细节模糊和结构不一致。
- **Volume Router**：在高斯层级进行权重分配，虽保留几何信息但优化困难，训练不稳定。
- **Volume-aware Pixel Router**（本文方案）：通过可微分权重投射将高斯层级的体素感知权重 splat 到像素空间，兼具几何感知能力和优化稳定性。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/008_Table_4.jpg]]
*Table 4: Performance Comparison of Different MoE Router Variants*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparison of MoE Router variants. Each router applies a different routing strategy, resulting in varied structural consistency and detail across the outputs*

定量结果表明，Volume-aware Pixel Router 在 PSNR 上显著优于两种基线变体，定性对比（Figure 5）显示其能更好地保持边缘锐度和纹理细节。该消融直接验证了核心设计主张：**将 3D 几何信息注入路由过程是保证融合质量的关键**。

### 效率优化消融

Table 5 对单通道渲染（Single-Pass Rendering）和门控感知剪枝（Gate-Aware Pruning）进行了独立与组合消融。仅使用单通道渲染可大幅提升 FPS，仅使用剪枝可显著降低内存，两者组合在 PSNR 损失极小（< 0.1 dB）的前提下实现了 FPS 和内存的双重优化。这证明两项效率优化具有良好的正交性和叠加效果。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/009_Table_5.jpg]]
*Table 5: Ablation of Efficiency Optimizations*

### 训练预算与蒸馏

Table 6 展示了专家训练预算对 MoE-GS 性能的影响。即使每个专家仅使用 **20% 的训练迭代预算**，MoE-GS（N=3）仍能超越完全训练的单专家基线。这一发现具有重要实践意义：MoE-GS 不仅提升性能上限，还能在有限训练资源下提供更强的重建能力。

知识蒸馏实验（Table 7）表明，使用 MoE-GS 渲染图像作为伪标签对单专家进行蒸馏训练，可一致提升其 PSNR、SSIM 和 LPIPS。进一步引入路由权重引导（routing-weighted distillation）后，蒸馏模型性能更逼近完整 MoE-GS。Table 13 的补充消融确认了路由加权的额外增益。这意味着蒸馏后的单专家模型可在保持接近 MoE 质量的同时，消除多专家推理开销，弥合了质量与效率之间的差距。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/012_Table_7.jpg]]
*Table 7: Ablation Studies on MoE-GS Distillation Methods on Technicolor dataset*

### 训练稳定性

Table 12 报告了多次重复训练（不同随机种子）下的性能波动。虽然单一专家模型在不同运行间存在一定方差，但 **MoE-GS 在所有运行中始终稳定优于任何单一专家变体**，排除了"MoE 仅靠方差降低取得优势"的替代解释。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_WrEQFwWCdT/figures/023_Table_12.jpg]]
*Table 12: Stability across repeated trainings. Variability exists across runs, but MoE-GS consistently outperforms all single-expert variants*

### 局限性与失效模式

尽管 MoE-GS 在整体指标上表现优异，分析中仍识别出以下局限：

1. **多专家推理开销**：当专家数量 N 较大时，即使经过单通道渲染和剪枝优化，FPS 下降和内存增加仍然不可忽略。Table 3 中 N=2 配置已接近实用，但 N=4 配置的实时性需进一步验证。
2. **蒸馏性能差距**：蒸馏后的单专家模型虽大幅超越原基线，但仍略低于完整 MoE-GS（Table 7），表明 MoE 的部分增益来自推理时的动态融合，无法完全通过蒸馏迁移。
3. **专家集固定性**：当前实验使用固定的四类变形先验（HexPlane 嵌入、逐高斯嵌入、插值、多项式轨迹），对于包含未知运动模式的场景可能无法覆盖最优变形策略。
4. **数据集规模**：实验主要在中等规模的多视角数据集（N3V、Technicolor）上进行，对大规模、长序列或单目视频的泛化性需要额外验证。

### 开放问题

基于上述分析，以下方向值得后续探索：
- 将专家池扩展至 NeRF 类方法或其他显式表征，以覆盖更丰富的变形先验。
- 在极端动态或稀疏视图条件下验证路由器和蒸馏策略的鲁棒性。
- 探索路由器的在线学习或终身学习机制，避免额外的独立训练阶段。
- 将 MoE-GS 的几何一致性提升与下游任务（如动态场景理解、目标跟踪）结合。
- 通过硬件加速或模型量化进一步降低多专家推理开销，推动实时应用落地。



## 定位与知识库关联

### 1. 问题定位：动态高斯泼溅中的单一先验瓶颈

动态场景重建的核心挑战在于运动模式的异质性——同一场景中往往同时存在静止背景、平滑刚体运动、快速非刚体形变以及不规则瞬态变化。现有动态高斯泼溅方法各自内嵌了不同的变形先验，例如：

- **4DGaussians** (Wu et al., 2024) 采用 HexPlane 嵌入的时空变形场；
- **E-D3DGS** (Bae et al., 2024) 使用逐高斯嵌入的变形网络；
- **STG** (Li et al., 2024) 将轨迹建模为多项式函数；
- **Ex4DGS** (Lee et al., 2024) 依赖时间插值策略。

这些方法在特定运动模式下表现优异，但**没有任何单一变形先验能够在所有空间区域和时间步上同时达到最佳重建质量**。如 Figure 1 所示，这种不一致性体现在三个层面：(a) 场景级——同一方法在不同场景上的性能排名剧烈波动；(b) 空间级——同一帧内不同区域偏好不同的变形模型；(c) 时间级——同一场景中，最优方法随时间步推移而切换。这一发现构成了 MoE-GS 的核心动机：**动态场景重建本质上是一个需要多策略协作的问题，而非单一模型能够胜任的任务**。

### 2. 方法谱系：从单一专家到专家混合

MoE-GS 在动态高斯泼溅领域首次系统性地引入了**专家混合（Mixture of Experts）**范式。其方法定位可沿以下维度展开：

**相对于单专家动态高斯方法。** MoE-GS 并不提出新的变形先验，而是将现有方法作为可插拔的候选专家纳入统一框架。这种设计使得 MoE-GS 天然具备向后兼容性——任何未来的动态高斯方法都可以作为新专家加入，无需修改框架本身。实验表明，即使每个专家仅使用 20% 的训练预算，MoE-GS 仍能超越完全训练的单专家基线（Table 6），说明专家间的互补性收益远超个体训练充分性的损失。

**相对于 NeRF 类动态方法。** 与 **HyperReel** (Attal et al., 2023)、**K-Planes** (Fridovich-Keil et al., 2023)、**MixVoxels-L** (Wang et al., 2023) 等基于隐式表征的方法相比，MoE-GS 继承了 3D Gaussian Splatting 的显式光栅化优势，在渲染速度上具有数量级领先，同时在 N3V 和 Technicolor 数据集上取得了更高的 PSNR（Tables 1-2）。

**相对于其他动态高斯基线。** **3DGStream** (Sun et al., 2024)、**DASS** (Liu et al., 2024)、**SaRO-GS** (Yan et al., 2024)、**SwinGS** (Liu & Banerjee, 2024) 等方法同样聚焦于动态高斯重建，但均采用单一模型架构。MoE-GS 的差异化在于将“模型选择”本身作为一个可学习的过程——通过 Volume-aware Pixel Router 实现空间-时间自适应的专家融合，而非依赖人工预设的启发式规则。

### 3. 关键技术贡献的知识定位

MoE-GS 的三项核心设计分别填补了现有工作的不同空白：

**Volume-aware Pixel Router（路由器设计）。** 传统 MoE 路由通常在高维特征空间进行（如 LLM 中的 token-level routing），而动态场景渲染需要处理 3D 几何与 2D 投影之间的对应关系。MoE-GS 的路由器通过可微分的体素感知权重投射（differentiable weight splatting），将高斯级的 3D 权重映射到像素空间，再经轻量 MLP 残差修正得到最终门控权重。这一设计在定量（Table 4）和定性（Figure 5）上均显著优于纯像素路由（忽略几何一致性）和纯体素路由（优化困难）。

**单通道多专家渲染（效率优化）。** 朴素的多专家渲染需要为每个专家独立执行投影和光栅化，导致计算开销随专家数量线性增长。MoE-GS 通过为每个高斯分配 one-hot 专家身份标识，在一次光栅化中同时生成所有专家的着色图（Eq. 9），消除了冗余的投影和可见性计算。配合门控感知高斯剪枝（Gate-Aware Gaussian Pruning），可在 PSNR 损失极小的情况下大幅提升 FPS 并降低内存占用（Table 5）。

**知识蒸馏部署策略。** 完整 MoE-GS 在推理时仍需维护多个专家模型，限制了实时应用。MoE-GS 提出利用 MoE 渲染图像和路由权重作为蒸馏目标，将多专家知识迁移至单一专家模型。蒸馏后的单专家性能大幅超越原基线，逼近 MoE-GS 品质（Table 7, Table 11），弥合了质量与效率之间的差距。这一策略与 Hinton et al. (2015) 的经典知识蒸馏框架一脉相承，但创新性地引入了路由权重引导的注意力机制（Eq. 11），使蒸馏过程聚焦于各专家负责的时空区域。

### 4. 适用边界与局限

尽管 MoE-GS 在多个基准上取得了最优结果，其适用边界和局限需要明确认识：

**推理效率的固有权衡。** 多专家推理时 FPS 下降和内存增加是 MoE 架构的固有代价。虽然单通道渲染和剪枝策略有效缓解了这一问题（N=2 时 FPS 接近单专家，内存甚至更小，Table 3），但在专家数量较多时开销仍然显著。知识蒸馏提供了一条部署路径，但蒸馏后的单专家性能仍略低于完整 MoE-GS，且需要额外的训练阶段。

**专家集的封闭性。** 当前实验固定使用四类变形先验（HexPlane 嵌入、逐高斯嵌入、多项式轨迹、时间插值）。对于包含未知运动模式的场景（如流体模拟、布料动力学），现有专家集可能无法提供足够的覆盖度。框架本身支持专家扩展，但如何自动发现或生成新专家类型仍是一个开放问题。

**数据规模与场景多样性。** 当前验证主要在中等规模的多视角数据集（N3V、Technicolor）上进行。对于大规模场景、长序列视频或单目输入条件下的鲁棒性，论文未提供系统验证，需要进一步实验确认。

**训练稳定性与随机种子敏感性。** 重复训练实验（Table 12）表明 MoE-GS 始终稳定优于任何单一专家，但多次运行间仍存在一定方差。路由器的优化依赖于第一阶段专家训练的质量，专家训练的不稳定性可能传导至路由阶段。

### 5. 开放问题与未来方向

基于上述分析，MoE-GS 开启的研究方向包括：

1. **专家类型的扩展与自动化。** 能否将基于 NeRF 的专家或其他显式表征（如网格、点云）纳入同一 MoE 框架？如何自动学习或搜索最优专家组合，而非依赖人工预设？

2. **极端条件下的鲁棒性。** 在稀疏视图、剧烈光照变化或严重遮挡条件下，路由器和蒸馏策略是否依然有效？路由器能否利用多视图几何一致性（如深度约束）来提升路由质量？

3. **在线与终身学习。** 当前路由器需要两阶段离线训练。能否设计在线路由机制，使 MoE-GS 在推理过程中持续适应场景变化，而无需重新训练？

4. **下游任务集成。** MoE-GS 生成的路由权重本身编码了丰富的时空运动信息。这些权重能否作为动态场景理解的中间表征，服务于目标跟踪、动作识别或场景编辑等下游任务？

5. **硬件加速与量化。** 在实时应用（如 VR/AR）中，可否通过 GPU 定制化算子、混合精度量化或专家剪枝进一步降低多专家推理的延迟和功耗？



## 原文 PDF

![[paperPDFs/ICLR_2026/MoE_GS_Mixture_of_Experts_for_Dynamic_Gaussian_Splatting_610a761de4a8.pdf]]

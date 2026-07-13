---
title: "GIFSplat: Generative Prior-Guided Iterative Feed-Forward 3D Gaussian Splatting from Sparse Views"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GIFSplat_Generative_Prior_Guided_Iterative_Feed_Forward_3D_Gaussian_Splatting_from_Sparse_Views.pdf
project_link: null
code_link: null
aliases:
- GI
- GIFSplat
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用迭代前馈残差更新机制：基于当前高斯状态与差异线索（观察证据与生成先验线索）预测残差，实现无需测试时梯度回传的场景自适应细化，并可通过步数灵活控制质量与效率平衡。
primary_logic: 将三维高斯泼溅视为可迭代更新的表达，利用权重共享的细化模块，将渲染差异与扩散模型增强的生成先验转化为高斯级线索，在纯前馈下近似最小化观察误差，参数与步数无关。
claims:
- 移除迭代细化模块导致PSNR从26.559降至24.781，为消融中最显著的下降。
- 添加生成先验模块在所有指标上均有提升（PSNR从26.291升到26.559，LPIPS从0.145降至0.138）。
- 在多个数据集（DL3DV, RealEstate10K, DTU）和不同视图重叠度下，均超越最新前馈方法，PSNR最高提升+2.1 dB。
- RealEstate10K (2-view, average over Small/Medium/Large overlap) 上 PSNR / SSIM / LPIPS = 26.559 / 0.867 / 0.138
---

# GIFSplat: Generative Prior-Guided Iterative Feed-Forward 3D Gaussian Splatting from Sparse Views

> [!tip] 核心洞察
> 将三维高斯泼溅视为可迭代更新的表达，利用权重共享的细化模块，将渲染差异与扩散模型增强的生成先验转化为高斯级线索，在纯前馈下近似最小化观察误差，参数与步数无关。

| 字段 | 内容 |
|------|------|
| 中文题名 | GIFSplat：基于生成先验引导的迭代前馈式3D高斯泼溅（面向稀疏视图） |
| 英文题名 | GIFSplat: Generative Prior-Guided Iterative Feed-Forward 3D Gaussian Splatting from Sparse Views |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22571) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GIFSplat / IFSplat |
| Dataset | RealEstate10K, DL3DV, DTU |

> [!tip] 效果简介
> - RealEstate10K (2-view, average over Small/Medium/Large overlap) 上，PSNR / SSIM / LPIPS 26.559 / 0.867 / 0.138 vs best feed-forward baselines (outperforms all, up to +2.1 dB PSNR)。
> - DL3DV (8 input views) 上，PSNR / SSIM / LPIPS 24.91 / 0.824 / 0.164 vs existing feed-forward approaches (highest among feed-forward methods (pose-required or pose-free))。
> - DTU (cross-dataset, model trained on RealEstate10K) 上，PSNR / SSIM / LPIPS 20.214 / 0.716 / 0.251 vs existing feed-forward approaches (superior out-of-distribution performance)。

## 概要

### 问题与瓶颈

从稀疏、未标定的多视图图像中重建高质量三维场景，现有前馈方法普遍采用一次性预测范式。这类方法推理效率高，但受模型容量限制，缺乏针对单个场景的逐实例细化能力，导致在视图重叠度低或约束不足的区域出现模糊、纹理粘连等伪影。另一方面，基于测试时梯度优化的方法虽然能通过数千次更新提升质量，但在稀疏视图下优化信号不足，且推理成本极高。**核心瓶颈在于：如何在保持纯前馈效率的前提下，实现对三维表达的迭代式场景自适应细化，并有效注入生成先验以补偿缺失的观测信息。**

### 核心方法

GIFSplat提出了一种**生成先验引导的迭代前馈三维高斯泼溅框架**，其核心思路是将三维高斯泼溅视为可迭代更新的表达，通过一个权重共享的迭代高斯头，在纯前馈模式下进行多步残差更新。具体而言：

- **迭代前馈残差更新**：在每一细化步，基于当前高斯状态与差异线索（渲染图像与输入图像的特征差异），预测高斯参数的残差修正量，并直接叠加到当前状态上，全程无需测试时梯度回传。
- **生成先验融合**：引入一个冻结的扩散增强器（DIFIX）对中间渲染视图进行增强，将增强后的图像与原始渲染在特征空间的残差汇聚为高斯级先验线索，与观察线索共同指导残差预测，从而在纹理细节和几何边界上实现显著提升。
- **灵活的质量-效率平衡**：通过控制迭代步数T，可在不改变模型参数的前提下，灵活权衡重建质量与推理延迟。

### 主要结果

在RealEstate10K、DL3DV和DTU三个数据集上，GIFSplat在所有视图重叠度设置下均超越了现有的前馈三维重建方法（包括需要相机位姿和无需位姿的方法），PSNR最高提升**+2.1 dB**。消融实验表明，迭代细化模块是最关键的组件，移除后PSNR从26.559降至24.781；生成先验模块在所有指标上均有额外增益（PSNR从26.291升至26.559，LPIPS从0.145降至0.138）。推理时间随迭代步数近似线性增长，在T=3时实现质量-延迟的最优平衡。

### 稀疏视图三维重建的范式困境

从少量二维图像重建完整的三维场景是计算机视觉的核心挑战。当前主流方案可归为两类范式，但各自存在根本性瓶颈。

**梯度优化范式**（如3D Gaussian Splatting原版）通过数千次测试时梯度回传迭代优化场景表达，在密集视图场景下能取得高质量重建。然而，当输入视图稀疏时，优化信号极度匮乏，模型极易陷入局部最优，产生模糊几何与纹理失真。更关键的是，其高昂的测试时计算成本（通常需要数分钟至数十分钟）使其难以部署于实时或交互式应用。

**一次性前馈范式**（如**pixelSplat**（Charatan et al., CVPR 2024）、**MVSplat**（Chen et al., ECCV 2024）、**AnySplat**（Jiang et al., arXiv 2025）等）通过端到端网络直接从输入视图预测三维高斯表达，推理效率极高（秒级甚至亚秒级）。然而，这类方法采用“一次成形”的预测策略，受限于模型容量和前馈网络固有的局部感受野，缺乏针对具体场景的逐实例细化能力。其输出往往残留明显的模糊、边缘锯齿和纹理粘连（texture sticking）等伪影，在视图重叠度低的困难区域表现尤甚。

### 生成先验的利用困境

近年来，扩散模型在图像生成领域展现出强大的先验建模能力，为三维重建提供了丰富的语义与纹理线索。然而，现有方法在注入生成先验时面临两难：

- **测试时优化注入**：在推理阶段对扩散模型进行梯度回传或迭代采样，虽能提升细节恢复，但严重牺牲了前馈方法的效率优势。
- **训练时蒸馏注入**：仅在训练阶段利用扩散模型作为监督信号，测试时不引入任何生成先验，导致对未观测区域的细节恢复能力有限。

如何在保持纯前馈推理效率的前提下，有效利用冻结的扩散模型为每个场景提供生成先验引导，是一个尚未被充分解决的问题。

### 本文动机与核心思路

针对上述困境，本文提出**GIFSplat**（Generative Prior-Guided Iterative Feed-Forward 3D Gaussian Splatting），核心动机在于回答一个关键问题：**能否设计一种既保持前馈效率、又具备逐场景自适应细化能力的重建范式，并在此过程中无缝融合生成先验？**

GIFSplat的应对策略可概括为三个层次：

1. **范式突破**：将三维高斯泼溅视为可迭代更新的表达，引入权重共享的迭代前馈残差更新机制。在每一步中，基于当前高斯状态与差异线索（观察证据与生成先验线索）预测残差，实现无需测试时梯度回传的场景自适应细化（见Figure 1与Figure 2）。

2. **先验融合**：利用冻结的扩散增强器（DIFIX）处理渲染图像，提取特征空间残差作为生成先验线索，并将其与观察线索共同馈入细化模块，实现生成先验的测试时注入而不引入梯度计算（见Figure 4）。

3. **效率-质量可控**：通过调整迭代步数$T$灵活控制质量与延迟的平衡——实验表明约3步后性能趋于饱和，推理时间随$T$近似线性增长（见Figure 7），实际部署中可采用$T=3$实现最优折衷。

这一设计使得GIFSplat在多个数据集（DL3DV、RealEstate10K、DTU）和不同视图重叠度下均超越了现有前馈方法，PSNR最高提升+2.1 dB，同时保持了亚秒级推理速度。

## 核心方法与创新机理

GIFSplat 针对现有前馈三维重建方法的两大瓶颈——**一次性预测范式缺乏逐场景细化能力**，以及**难以在保持前馈效率的前提下有效注入生成先验**——提出了三项紧密耦合的关键创新，构成一个完整的迭代前馈重建框架。

### 创新一：迭代前馈残差更新范式

现有前馈方法（如 **pixelSplat** (Charatan et al., CVPR 2024)、**MVSplat** (Chen et al., ECCV 2024)、**AnySplat** (Jiang et al., arXiv 2025)）均采用一次性预测范式，直接从前馈网络输出完整的3D高斯场，受模型容量限制，无法针对特定场景进行自适应细化。GIFSplat 将3D高斯泼溅重新定义为**可迭代更新的表达**，引入权重共享的迭代高斯头 $U_\theta$，在纯前馈模式下执行多步残差更新：

$$\Delta\mathcal{G}^{(t+1)} \gets U_\theta([\mathcal{G}^{(t)} \parallel \{\mathbf{o}_i\}^{(t)}])$$

$$\mathcal{G}^{(t+1)} \gets \mathcal{G}^{(t)} + \Delta\mathcal{G}^{(t)}$$

这一设计的核心优势在于：**参数与步数无关**（权重共享），**无需测试时梯度回传**，在保持前馈效率的同时实现了场景自适应细化。消融实验提供了决定性证据：移除迭代细化模块后，PSNR 从 26.559 骤降至 24.781（Table 4），这是所有消融中幅度最大的性能下降，确证了迭代细化是最关键的创新组件。

### 创新二：冻结扩散模型驱动的生成先验融合

现有方法要么完全未利用生成先验，要么需要测试时梯度优化（如基于 SDS 的方法），难以兼顾效率与质量。GIFSplat 提出了一种**保守而高效的生成先验注入机制**：采用完全冻结的扩散增强器（DIFIX），对新视图渲染进行增强，然后将增强图像与原始渲染在特征空间的残差，通过软分配权重池化为高斯级先验线索：

$$\mathbf{p}_i^{(t)} = \frac{\sum_{m \in \mathcal{S}^{(t)}} \sum_u w_i(u) P_m^{(t)}(u)}{\sum_{m \in \mathcal{S}^{(t)}} \sum_u w_i(u) + \varepsilon}$$

最终，先验线索与观察线索并接，共同驱动残差预测：

$$\Delta\mathcal{G}_i^{(t)} = U_\theta([g_i^{(t)} \parallel \{\mathbf{o}_i\}^{(t)} \parallel \{\mathbf{p}_i\}^{(t)}])$$

消融实验表明，添加生成先验模块在所有指标上均有提升（PSNR 从 26.291 升至 26.559，LPIPS 从 0.145 降至 0.138，Table 4），尤其在纹理清晰度和高频细节恢复上效果显著（Figure 4）。值得注意的是，扩散增强器在推理时完全冻结且无梯度回传，这保证了推理效率，但也构成了细节恢复上限的约束。

### 创新三：点基高斯与窗口注意力邻域建模

区别于前馈方法中常用的像素对齐高斯表达，GIFSplat 采用**点基高斯**（point-based Gaussians），并通过**窗口注意力**（window attention）显式建模3D局部邻域关系。消融实验显示，移除窗口注意力后 PSNR 从 26.559 降至 25.327（Table 4），验证了点基高斯加窗口注意力设计的有效性。这一设计使得高斯场在迭代细化过程中能够更好地传播局部几何和外观信息，为残差预测提供更丰富的上下文。

### 创新间的协同关系

三项创新并非孤立存在，而是形成了**因果闭环**：点基高斯与窗口注意力为迭代细化提供了高质量的初始表达和邻域上下文；迭代前馈残差更新机制为生成先验的注入提供了多步递进的载体——每一步的渲染结果都可被扩散增强器提炼为新的先验线索，反馈至下一步更新；而冻结扩散模型的设计则确保了整个迭代循环保持纯前馈效率。这一协同设计使得 GIFSplat 在多个数据集（DL3DV、RealEstate10K、DTU）和不同视图重叠度下均超越最新前馈方法，PSNR 最高提升 +2.1 dB（Table 1, Table 2, Table 3）。

GIFSplat 提出一种**迭代前馈式三维高斯泼溅框架**，其核心设计围绕一个因果闭环展开：现有前馈方法采用一次性预测范式，受模型容量限制而缺乏逐场景细化能力，同时难以在保持前馈效率的前提下有效注入生成先验。GIFSplat 的解决方案是将三维高斯泼溅视为可迭代更新的表达，通过权重共享的细化模块，将渲染差异与扩散模型增强的生成先验转化为高斯级线索，在纯前馈下近似最小化观察误差，且参数规模与迭代步数解耦。

### 三组件流水线

框架由三个模块串联构成（Figure 2），形成“初始化—迭代细化—先验融合”的完整链路：

![[assets/figures/papers/paper_list_l2511_https_arxiv_org_abs_2602_22571/figures/002_Figure_2.jpg]]
*Figure 2: Overview of GIFSplat. Our framework consists of a Gaussian initializer, an iterative Gaussian head, and a generative prior fusion module. The initializer takes sparse input views and predicts camera parameters and initial*

1. **高斯初始化器（Gaussian Initializer, $F_\phi$）**  
   以稀疏未标定视图作为输入，直接预测相机参数和初始三维高斯泼溅 $\mathcal{G}^{(0)}$。该模块基于 **AnySplat**（Jiang et al., arXiv 2025）构建，但移除了原方法中的体素化微调模块，以适应后续迭代细化的需求。

2. **迭代高斯头（Iterative Gaussian Head, $U_\theta$）**  
   对初始高斯进行 $T$ 步前向残差更新，每步接收当前高斯状态 $\mathcal{G}^{(t)}$、观察线索 $\{o_i\}^{(t)}$ 和生成先验线索 $\{p_i\}^{(t)}$，预测残差 $\Delta\mathcal{G}^{(t)}$ 并直接叠加到当前参数上：
   $$\mathcal{G}^{(t+1)} \leftarrow \mathcal{G}^{(t)} + \Delta\mathcal{G}^{(t)}$$
   整个过程无需测试时梯度回传，通过权重共享的 Transformer 实现参数与步数无关。

3. **生成先验融合模块（Generative Prior Fusion Module）**  
   利用冻结的扩散增强器（DIFIX）对中间渲染视图进行增强，提取增强前后在特征空间的残差，并将其汇聚为高斯级先验线索 $\{p_i\}^{(t)}$，注入迭代头的下一次更新中。

### 数据流与关键机制

每步迭代的数据流如下：

- **渲染与差异提取**：将当前高斯 $\mathcal{G}^{(t)}$ 通过可微光栅化器 $\mathcal{R}$ 渲染到参考视点和新视点，计算渲染图像与输入图像在特征空间中的逐像素差异 $O_m^{(t)}$。
- **观察线索汇聚**：通过软分配权重 $w_i(u)$ 将像素级差异池化到每个高斯上，形成观察线索 $\mathbf{o}_i^{(t)}$（Eq. 1）。
- **先验线索汇聚**（可选）：将扩散增强图像与原始渲染的特征差异以相同方式池化，形成先验线索 $\mathbf{p}_i^{(t)}$（Eq. 4）。
- **残差预测与状态更新**：将当前高斯参数 $g_i^{(t)}$ 与线索拼接后送入 $U_\theta$，预测残差并更新（Eq. 5–6）。

该设计的关键优势在于：**迭代细化模块与生成先验模块可独立启用或关闭**。当仅使用观察线索时，框架退化为 IFSplat 模式（Eq. 2）；同时启用先验线索时即为完整的 GIFSplat 模式（Eq. 5）。这种模块化设计使得质量与效率的平衡可通过迭代步数 $T$ 灵活控制——实验表明性能在约 3 步后趋于饱和，推理时间随 $T$ 近似线性增长（Figure 7）。

### 两阶段训练策略

为稳定训练这一多步迭代系统，GIFSplat 采用两阶段训练：

- **第一阶段**：仅训练高斯初始化器 $F_\phi$，使用逐像素 L2 重建损失与几何蒸馏损失的组合（Eq. 7–8），目标是提供可靠的初始高斯状态。
- **第二阶段**：冻结 $F_\phi$，训练迭代高斯头 $U_\theta$，对每一步的渲染结果施加加权 L2 损失（Eq. 9），使模型学会利用观察线索和先验线索逐步修正初始预测。

这一框架的边界条件在于：当前设计仅针对静态场景，未处理动态内容；扩散增强器在推理时完全冻结且无梯度回传，虽保证了效率，但可能限制了细节恢复的上限。

![[assets/figures/papers/paper_list_l2511_https_arxiv_org_abs_2602_22571/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual comparison of reconstruction paradigms. Gradient optimization performs thousands updates, incurring heavy test-time cost, often achieving high quality in dense-view scenarios but struggling in sparse-view scenarios; One-shot feedforward [7] is efficient but leaves noticeable artifacts; Our iterative residual feed-forward scheme keeps feed-forward efficiency and achieves higher reconstruction quality without test-time gradient backpropagation*

### 3.1 框架总览

GIFSplat 由三个核心组件构成（Figure 2）：**高斯初始化器** $F_\phi$、**迭代高斯头** $U_\theta$ 以及**生成先验融合模块**。

**高斯初始化器**基于 AnySplat（Jiang et al., arXiv 2025）移除体素化微调模块，从稀疏未标定视图直接预测相机参数和初始 3D 高斯 $\mathcal{G}^{(0)} = \{g_i^{(0)}\}$。每个高斯参数包含位置、尺度、旋转、颜色和透明度：

$$g_i = (\mathbf{x}_i, \mathbf{s}_i, \mathbf{r}_i, \mathbf{c}_i, \alpha_i)$$

给定相机参数 $\Pi_m$，通过可微光栅化器 $\mathcal{R}$ 渲染视图：

$$R_m = \mathcal{R}(\mathcal{G}; \Pi_m)$$

**迭代高斯头**在初始化后施加 $T$ 步纯前馈残差更新，无需测试时梯度回传。每步基于当前高斯状态与差异线索预测残差 $\Delta\mathcal{G}^{(t)}$，通过加法更新：

$$\mathcal{G}^{(t+1)} \gets \mathcal{G}^{(t)} + \Delta\mathcal{G}^{(t)}$$

### 3.2 观察线索与残差预测

在每步 $t$，将渲染图像与输入图像送入共享特征编码器，计算像素级特征差异 $O_m^{(t)}(u)$。通过光栅化时产生的软分配权重 $w_i(u)$，将这些差异池化到每个高斯上，形成**观察线索** $\mathbf{o}_i^{(t)}$：

$$\mathbf{o}_i^{(t)} = \frac{\sum_{m \in S^{(t)}} \sum_u w_i(u) O_m^{(t)}(u)}{\sum_{m \in S^{(t)}} \sum_u w_i(u) + \varepsilon} \quad \text{(Eq. 1)}$$

其中 $S^{(t)}$ 为当前步选定的源视图集合，$\varepsilon$ 防止除零。该池化操作将渲染与真实观测的差异转化为高斯级别的反馈信号。

在不使用生成先验的 IFSplat 模式下，迭代头 $U_\theta$ 仅拼接当前高斯状态与观察线索来预测残差：

$$\Delta\mathcal{G}^{(t+1)} \gets U_\theta([\mathcal{G}^{(t)} \parallel \{o_i\}^{(t)}]) \quad \text{(Eq. 2)}$$

为建模 3D 局部关系，迭代头采用**点基高斯 + 窗口注意力**机制，在高斯点云上施加空间局部注意力，替代传统前馈方法中像素对齐的高斯表达。

### 3.3 生成先验融合

生成先验融合模块（Figure 4）引入冻结的扩散增强器 **DIFIX**，在无梯度回传的前提下为细化过程注入高频纹理先验。具体流程：

1. 对当前步渲染视图 $R_m^{(t)}$ 施加 DIFIX 增强，得到增强图像 $\tilde{R}_m^{(t)}$；
2. 将增强图像与原始渲染图像送入特征编码器，计算特征空间残差 $P_m^{(t)}(u)$；
3. 通过相同的软分配权重池化，形成**先验线索** $\mathbf{p}_i^{(t)}$：

$$\mathbf{p}_i^{(t)} = \frac{\sum_{m \in \mathcal{S}^{(t)}} \sum_u w_i(u) P_m^{(t)}(u)}{\sum_{m \in \mathcal{S}^{(t)}} \sum_u w_i(u) + \varepsilon} \quad \text{(Eq. 4)}$$

最终，将当前高斯参数、观察线索和先验线索拼接，共同预测残差：

$$\Delta\mathcal{G}_i^{(t)} = U_\theta([g_i^{(t)} \parallel \{o_i\}^{(t)} \parallel \{p_i\}^{(t)}]) \quad \text{(Eq. 5)}$$

这一设计的关键在于：扩散增强器完全冻结且无梯度，仅提供特征空间残差作为线索；迭代头通过端到端训练学会如何利用这些先验信号来修正欠约束区域的几何与纹理。

### 3.4 损失函数

训练分两阶段进行。**第一阶段**训练高斯初始化器，损失包含重建损失与几何蒸馏损失：

$$\mathcal{L}_{\mathrm{rec}} = \lambda_{\mathrm{rgb}} \| I_m - R_m \|_2 \quad \text{(Eq. 7)}$$

$$\mathcal{L}_{\mathrm{stage1}} = \sum_{m \in \mathcal{M}} (\mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{dist}}) \quad \text{(Eq. 8)}$$

**第二阶段**训练迭代高斯头，对每个细化步骤的渲染结果施加加权 L2 损失：

$$\mathcal{L}_{\mathrm{stage2}} = \sum_{t=1}^{T} \omega_t \sum_{m \in \mathcal{M}} \| I_m - R_m^{(t)} \|_2 \quad \text{(Eq. 9)}$$

其中 $\omega_t$ 为步骤权重。该多步监督信号驱动迭代头逐步减小渲染误差，实现无梯度场景自适应细化。

## 实验与关键发现

### 主实验结果

GIFSplat在多个数据集和输入配置下均取得一致的性能优势，验证了迭代前馈细化范式的有效性。

**RealEstate10K 2-view新视角合成。** 在2视图输入、涵盖小/中/大三种重叠度的设定下，GIFSplat在所有指标上均超越现有前馈方法（Table 1）。全模型达到PSNR 26.559 / SSIM 0.867 / LPIPS 0.138，相比最强基线最高提升+2.1 dB PSNR。特别在小重叠度场景中，优势更为显著——这类场景对一次性预测方法构成严峻挑战，而迭代细化机制通过多步残差更新逐步恢复被遮挡或欠约束区域的几何与纹理。定性对比（Figure 5）进一步表明，GIFSplat能恢复更清晰的边界（如门框、墙角）和更忠实的纹理，有效抑制纹理粘连伪影。

**DL3DV 8-view设定。** 在8视图输入下，GIFSplat达到PSNR 24.91 / SSIM 0.824 / LPIPS 0.164（Table 2），在所有前馈方法中排名第一。值得注意的是，GIFSplat无需相机内参或外参，而部分对比方法依赖已知位姿。这一结果证明迭代细化与生成先验的融合不仅补偿了位姿未知带来的不确定性，还在多视图条件下进一步提升了重建精度。定性结果（Figure 6）显示GIFSplat在保持锐利边缘和纹理细节的同时，有效抑制模糊和纹理粘连。

**跨数据集零样本泛化（DTU）。** 所有模型均使用RealEstate10K上训练的权重，直接在DTU数据集上评估（Table 3）。GIFSplat取得PSNR 20.214 / SSIM 0.716 / LPIPS 0.251，显著优于其他前馈方法。这表明迭代残差更新机制具有内在的泛化能力——细化模块学习的是“如何根据差异线索修正高斯状态”这一通用能力，而非记忆特定数据分布，因此在分布外场景下仍能有效运作。

### 消融实验

Table 4系统剥离了三个核心组件，揭示了各模块的贡献层级。

**迭代细化模块（最关键组件）。** 移除迭代细化（w/o Refinement）后，性能从全模型PSNR 26.559骤降至24.781，SSIM从0.867降至0.826，LPIPS从0.138升至0.169。这一降幅在所有消融中最为显著，证实了多步前馈残差更新是方法的核心驱动力。其因果机制在于：一次性预测受限于模型容量，无法对每个场景进行针对性调整；而迭代头通过权重共享的残差预测，在无梯度回传的前提下逐步逼近更优解。

**生成先验模块。** 移除生成先验（w/o Gen. Prior）后，PSNR从26.559降至26.291，LPIPS从0.138升至0.145。虽然降幅小于迭代模块，但LPIPS的提升表明扩散增强器主要贡献于纹理清晰度和感知质量。该模块将冻结扩散模型的特征空间残差蒸馏为高斯级先验线索，在不引入测试时优化的前提下注入高频外观信息。

**窗口注意力。** 移除窗口注意力（w/o window att.）后，PSNR降至25.327，SSIM降至0.837。这验证了点基高斯配合窗口注意力建模局部3D关系的有效性——相比像素对齐的高斯表达，该设计能更好地捕获空间邻域信息，提升几何一致性。

### 迭代步数分析

Table 5和Figure 7分析了细化步数T对性能与效率的影响。从初始预测（T=0）开始，随T增加（0→4），PSNR单调提升，约在3步后趋于饱和。实际采用T=3实现质量-延迟最优平衡。推理时间随T近似线性增长（Figure 7），验证了纯前馈设计避免了迭代优化中的计算爆炸问题。

### 失败模式与局限性

尽管整体性能优异，GIFSplat存在以下局限：

1. **静态场景限制。** 当前细化模块仅针对静态场景设计，无法处理动态内容。对于包含运动物体的场景，迭代残差更新缺乏时序建模能力，可能导致运动区域模糊或伪影。

2. **几何先验缺失。** 方法仅利用RGB输入，未融合深度图、法线图等显式几何先验。在极稀疏视图（如2-view小重叠）下，纯RGB线索可能不足以约束几何，导致部分区域的深度歧义。

3. **扩散先验的上限。** 扩散增强器在推理时完全冻结且无梯度回传，虽保证了效率，但限制了细节恢复的潜力——增强器自身的生成能力上限决定了先验线索的质量，且无法根据场景反馈自适应调整。

4. **跨域泛化的边界。** 尽管DTU零样本结果优于基线，但绝对PSNR（20.214）仍显著低于域内结果，表明迭代细化机制虽具泛化性，但在领域差异极大时仍存在性能衰减。

![[assets/figures/papers/paper_list_l2511_https_arxiv_org_abs_2602_22571/figures/005_Table_1.jpg]]
*Table 1: Novel view synthesis performance comparison on the RealEstate10K with 2 views as input. Our method largely outperforms pose-free and pose-required methods across all overlap settings, especially for small overlap setting. The best and second-best results are highlighted*

![[assets/figures/papers/paper_list_l2511_https_arxiv_org_abs_2602_22571/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on DL3DV with 8 input views. The pose-needed column indicates whether a method requires camera parameters. Metrics are PSNR↑, SSIM↑, and LPIPS↓. Among feed-forward approaches, Ours requires neither intrinsics nor extrinsics and achieves the highest PSNR/SSIM and the lowest LPIPS. The best and second-best results are highlighted*

![[assets/figures/papers/paper_list_l2511_https_arxiv_org_abs_2602_22571/figures/009_Table_3.jpg]]
*Table 3: Out-of-distribution performance comparison. Our method shows superior performance when cross-dataset evaluation on DTU using the model solely trained on RealEstate10K. The best and second-best results are highlighted*

![[assets/figures/papers/paper_list_l2511_https_arxiv_org_abs_2602_22571/figures/012_Table_4.jpg]]
*Table 4: Ablation study. We ablate the iterative refinement module (w/o Refinement), the window attention (w/o window att.), and the generative prior (w/o Gen. prior) from our full model, respectively. The full configuration achieves the best performance across all metrics. The best and second-best results are highlighted*

## 定位与知识库关联

### 前馈三维重建的范式演进

GIFSplat 的核心贡献在于将前馈三维高斯泼溅（3DGS）从“一次性预测”范式推进为“迭代前馈残差更新”范式。现有前馈方法，如 **pixelSplat**（Charatan et al., CVPR 2024）、**MVSplat**（Chen et al., ECCV 2024）以及无位姿方法 **AnySplat**（Jiang et al., arXiv 2025）和 **NoPoSplat**（Ye et al., arXiv 2024），均采用单步前馈预测，直接从未标定或已标定的稀疏视图回归三维高斯参数。这类范式受模型容量限制，缺乏逐场景的自适应细化能力，在遮挡严重或重叠度低的区域易产生模糊和伪影。

GIFSplat 引入的迭代残差头 $U_\theta$ 改变了这一范式：它不依赖测试时梯度回传，而是通过权重共享的前馈更新模块，在多个细化步骤中基于当前高斯状态与差异线索预测残差 $\Delta\mathcal{G}^{(t)}$，并通过 $\mathcal{G}^{(t+1)} \gets \mathcal{G}^{(t)} + \Delta\mathcal{G}^{(t)}$ 实现纯前馈的场景自适应细化。这与 **DUSt3R**（Wang et al., CVPR 2024）和 **FLARE**（Zhang et al., CVPR 2025）等基于点图回归的无位姿方法形成互补——后者提供可靠的初始几何估计，而 GIFSplat 在此基础上通过迭代机制持续改进外观与几何质量。

### 生成先验的注入方式对比

在生成先验利用方面，GIFSplat 的设计与现有基于优化的方法形成鲜明对比。传统方法（如基于 SDS 损失的 3D 生成管线）需要在测试时通过扩散模型进行梯度回传优化，计算开销巨大。GIFSplat 采用“冻结扩散增强器 + 特征空间残差蒸馏”的保守设计：使用冻结的 DIFIX 扩散增强器对新视图渲染进行增强，提取增强图像与原始渲染在特征空间的残差 $P_m^{(t)}$，并通过与观察线索相同的软分配池化机制汇聚为高斯级先验线索 $\mathbf{p}_i^{(t)}$。这一设计使得生成先验的注入完全融入前馈推理流程，无需任何测试时优化步骤。

值得注意的是，在移除生成先验模块的消融实验中（Table 4, w/o Gen. Prior），PSNR 从 26.559 降至 26.291，LPIPS 从 0.138 升至 0.145，表明生成先验在提升纹理清晰度和细节保真度方面具有独立贡献，但并非性能提升的唯一来源——迭代细化本身（w/o Refinement 导致 PSNR 降至 24.781）才是最关键组件。

### 适用边界与局限

**输入模态与场景类型**：当前框架仅针对静态场景设计，输入模态固定为稀疏 RGB 视图。方法未融合深度图、法线图等几何先验，在纹理稀疏或重复纹理区域的几何重建可能受限。在 DTU 跨数据集零样本评估中（Table 3），PSNR 为 20.214，虽优于现有前馈方法，但绝对值仍偏低，表明在分布外场景下的泛化能力存在提升空间。

**扩散增强器的上限约束**：生成先验模块中的扩散增强器在推理时完全冻结且无梯度回传，虽然保证了前馈效率，但也意味着增强效果受限于预训练扩散模型的能力边界。在极稀疏视图（如单视图）场景下，仅靠扩散先验可能不足以弥补严重的观察信息缺失。

**计算效率与质量的权衡**：迭代步数 $T$ 的增加带来性能单调提升，但约在 3 步后趋于饱和（Table 5, Figure 7）。推理时间随 $T$ 近似线性增长，实际采用 $T=3$ 实现质量-延迟最优平衡。对于实时性要求极高的应用场景，仍需在步数与质量间做出权衡。

### 开放问题

1. **动态场景扩展**：如何将迭代前馈细化框架扩展到 4D 高斯表达，处理动态内容（如人体运动、流体），同时保持亚秒级推理速度？这需要重新设计时间维度的线索池化与残差预测机制。

2. **多模态先验融合**：能否在不显著增加计算成本的前提下，注入更丰富的几何先验（深度图、法线图）或更强的生成先验（如视频扩散模型）？这涉及线索池化模块的扩展以及多模态特征的对齐问题。

3. **稀疏度-先验平衡的量化**：在极稀疏视图（如单视图）下，观察信息极度匮乏，生成先验的作用会更加关键。如何量化观察信息与先验信息的相对贡献，并据此动态调整融合权重，是一个值得探索的方向。

4. **表达方式的泛化性**：参数共享的迭代细化模块是否可能泛化到完全不同的三维表达方式，如 NeRF 或三平面？这需要验证残差预测机制对不同参数空间的适应性。

5. **训练效率优化**：当前两阶段训练策略（先训练初始器，再训练迭代头）虽保证了稳定性，但增加了训练复杂度。端到端联合训练是否可行，且能否进一步提升性能，尚待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/GIFSplat_Generative_Prior_Guided_Iterative_Feed_Forward_3D_Gaussian_Splatting_from_Sparse_Views.pdf]]

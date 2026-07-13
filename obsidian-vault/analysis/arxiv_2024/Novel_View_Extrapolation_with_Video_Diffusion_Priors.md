---
title: Novel View Extrapolation with Video Diffusion Priors
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Novel_View_Extrapolation_with_Video_Diffusion_Priors.pdf
project_link: https://kunhaoliu.github.io/ViewExtrapolator/
code_link: null
aliases:
- NVEVDP
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用Stable Video Diffusion (SVD)的大规模预训练生成先验，通过修改ODE导数方向将伪影视频融合进去噪过程，并设计引导退火与重采样退火策略来精细调控注入的引导强度，从而在保留场景结构的同时消除伪影。
primary_logic: 预训练视频扩散模型内化了自然视频的分布，能够为外推帧生成逼真细节。通过在扩散过程早期施加有伪影视频的引导，再逐步退火至无引导的自然视频生成，既保持了粗糙几何与内容，又利用模型的先验修补不可见区域并消除伪影，无需任何微调。
claims:
- ViewExtrapolator (3DGS) 在 LLFF-Extra 上取得最优 SSIM (0.460)、PSNR (15.46)、LPIPS (0.378)，大幅优于基线 3DGS (0.416, 14.46, 0.429) 和 DRGS (0.406, 14.68, 0.457)。
- 消融实验显示，移除引导退火使 LPIPS 从 0.378 急升至 0.448，移除重采样退火使 LPIPS 升至 0.382，且视觉上伪影明显残留；两者协同对于高保真外推不可或缺。
- ViewExtrapolator 是一种推理阶段方法，无需微调 SVD，可直接应用于不同 3D 渲染（辐射场、点云），体现了通用性与数据/计算高效性。
- LLFF-Extra 上 SSIM ↑ = 0.460
---

# Novel View Extrapolation with Video Diffusion Priors

> [!tip] 核心洞察
> 预训练视频扩散模型内化了自然视频的分布，能够为外推帧生成逼真细节。通过在扩散过程早期施加有伪影视频的引导，再逐步退火至无引导的自然视频生成，既保持了粗糙几何与内容，又利用模型的先验修补不可见区域并消除伪影，无需任何微调。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于视频扩散先验的新视角外推方法 |
| 英文题名 | Novel View Extrapolation with Video Diffusion Priors |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2411.14208) · [Project](https://kunhaoliu.github.io/ViewExtrapolator/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ViewExtrapolator |
| Dataset | LLFF-Extra |

> [!tip] 效果简介
> - LLFF-Extra 上，SSIM ↑ 0.460 vs 0.416 (+0.044)；PSNR ↑ 15.46 vs 14.46 (+1.00)；LPIPS ↓ 0.378 vs 0.429 (-0.051)。

## 概要

**问题瓶颈**：现有辐射场方法（如 **3DGS**，Kerbl et al., SIGGRAPH 2023）在新视角外推时，由于新视角远超出训练视图覆盖范围，渲染结果充斥着大量伪影与失真，严重制约了自由视角探索的沉浸感。这一瓶颈的根源在于辐射场对未观测区域的几何与外观缺乏有效约束。

**核心洞察**：预训练视频扩散模型（**Stable Video Diffusion**, SVD）内化了自然视频的分布先验，能够为外推帧生成逼真细节。ViewExtrapolator 正是利用这一能力，通过修改 ODE 导数方向，将带伪影的视频融入去噪过程，在保留场景粗糙结构的同时，借助模型先验修补不可见区域并消除伪影——整个过程无需任何微调。

**方法定位**：ViewExtrapolator 是一种**训练无关的推理阶段精炼范式**，作用于辐射场或点云渲染的伪影视频之上。其核心机制包括两项协同的退火策略——**引导退火**在去噪早期施加伪影视频的引导以保持内容，随后逐步退火至无引导生成以释放 SVD 的自然先验；**重采样退火**在每个引导步内多次迭代去噪-扩散循环并逐步关闭引导，从而精细抑制累积伪影。

**主要结果**：在 LLFF-Extra 基准上，ViewExtrapolator (3DGS) 取得最优 **SSIM 0.460**、**PSNR 15.46**、**LPIPS 0.378**，大幅优于基线 3DGS（0.416, 14.46, 0.429）和 DRGS（0.406, 14.68, 0.457）。消融实验表明，移除引导退火使 LPIPS 急升至 0.448，移除重采样退火使 LPIPS 升至 0.382，验证了两者对高保真外推的不可或缺性。该方法可直接应用于不同的 3D 渲染方式（3DGS、Instant-NGP、点云），体现了较强的通用性。

### 新视角外推：辐射场的阿喀琉斯之踵

以 **3D Gaussian Splatting**（3DGS, Kerbl et al., SIGGRAPH 2023）为代表的辐射场方法，在训练视角覆盖范围内的新视角插值（novel view interpolation）上取得了令人瞩目的渲染质量。然而，当用户试图将相机移动到训练视角范围之外——即进行新视角外推（novel view extrapolation）时，这些方法会暴露出根本性的缺陷：渲染结果中充斥着大量漂浮物、几何坍塌和纹理模糊等伪影，严重破坏了自由视角探索的沉浸感。

这一瓶颈的根源在于辐射场表征的本质局限。辐射场的优化完全依赖于训练视角提供的多视图光度一致性约束，对于训练视角未曾覆盖的区域，模型缺乏任何几何或外观先验来推断合理的场景内容。当外推距离增大时，渲染质量会急剧恶化，使得现有的辐射场方法无法支撑真正自由的视点漫游体验。

### 现有方法的缺口：插值基准与外推需求的错位

值得注意的是，现有的新视角合成基准——如 LLFF、NeRF Synthetic 和 DTU 等——其测试视角的外推度（extrapolation degree）普遍较小，本质上仍主要评估的是插值能力。这意味着，社区长期以来缺乏一个专门针对外推场景的严格评测基准，导致方法在“伪插值”设定下的良好表现掩盖了其在真实外推场景中的脆弱性。

### 核心动机：视频扩散先验的机遇

与此同时，以 **Stable Video Diffusion**（SVD）为代表的大规模视频生成模型，在海量自然视频上学习了丰富的动态场景先验。这些先验内化了自然视频的时空一致性分布，具备为缺失区域生成逼真细节的能力。一个自然的思路是：能否利用这种预训练的视频生成先验，来“修复”辐射场在外推视角下产生的伪影渲染？

然而，直接将辐射场的伪影视频输入扩散模型进行去噪，会面临一个根本性的张力：扩散模型倾向于生成与自然视频分布一致的干净内容，但这可能偏离原始场景的结构和外观；而完全保留伪影视频的内容，又无法消除伪影。如何在“保留场景内容”与“消除伪影、生成合理细节”之间取得精细平衡，是这一思路面临的核心挑战。

### 本文的切入：无需微调的推理阶段精炼范式

本文提出 **ViewExtrapolator**——一种完全训练无关（training-free）的推理阶段精炼管线。它通过重新设计 SVD 的去噪过程，将伪影视频的引导信号巧妙地融入扩散去噪的 ODE 导数方向，并设计了**引导退火**与**重采样退火**两种机制来精细调控引导强度：在去噪早期施加较强引导以保留粗糙的场景几何与内容，随后逐步退火至无引导的自然视频生成，让 SVD 的先验接管不可见区域的细节生成。这一设计使得 ViewExtrapolator 无需任何微调即可直接应用于不同的 3D 渲染管线（辐射场、点云等），兼具通用性与数据/计算高效性。

## 核心方法与创新机理

ViewExtrapolator 的核心创新在于**将预训练视频扩散模型的生成先验转化为新视角外推的精炼器**，并通过两个协同的退火策略精细调控引导强度，从而在无需任何微调的条件下消除辐射场渲染的严重伪影。其关键创新点体现在以下四个“changed slots”上：

### 1. 从标准去噪到伪影引导的去噪方向修正

标准扩散去噪过程仅从噪声中逐步恢复视频，而 ViewExtrapolator 重新设计了去噪方向。给定从辐射场渲染的伪影视频 $\tilde{\mathbf{x}}$ 和 SVD 预测的干净视频 $\hat{\mathbf{x}}_0$，方法通过不透明度掩码 $\mathbf{m}$ 将二者混合，构造引导方向：

$$
\hat{\mathbf{x}}_0^{\mathrm{dir}} = \tilde{\mathbf{x}} \odot \mathbf{m} + \hat{\mathbf{x}}_0 \odot (1 - \mathbf{m})
$$

该混合方向随后替代标准 ODE 导数方向，驱动去噪步 $\mathbf{x}_{t-1} = \mathrm{Denoise}(\mathbf{x}_t, \hat{\mathbf{x}}_0^{\mathrm{dir}})$。其核心机理在于：掩码 $\mathbf{m}$ 标记了渲染中的不可见区域，在这些区域中 SVD 的预测被优先采纳以修补缺失内容；而在可见区域，伪影视频的结构信息得以保留，从而在消除伪影的同时维持场景的粗糙几何与内容一致性。

### 2. 引导退火：限制引导步数以释放生成先验

若在整个去噪过程中持续施加伪影视频的引导，SVD 的生成先验将被过度约束，导致伪影无法被充分消除。ViewExtrapolator 提出**引导退火**策略：仅在去噪的前 $T^{\mathrm{guide}}$ 步使用伪影引导方向，后续步骤切换为无引导的标准去噪。这一设计的直觉在于：早期去噪步决定了视频的全局结构与布局，此时需要伪影视频提供粗糙的场景锚定；而在后期去噪步，SVD 的先验应主导细节生成，以自然视频的分布填补不可见区域并消除残留伪影。消融实验证实，移除引导退火后 LPIPS 从 0.378 急升至 0.448，视觉上大部分伪影未得到纠正，表明该机制对于在去噪后期摆脱伪影干扰至关重要。

### 3. 重采样退火：逐步精炼潜变量以抑制累积伪影

单一去噪步难以完全消除复杂伪影。ViewExtrapolator 进一步引入**重采样退火**：在每个引导去噪步内执行 $R$ 次“去噪-扩散”循环，且仅在前 $R^{\mathrm{guide}}$ 次重采样中使用引导方向，后续重采样切换为无引导模式。组合退火方向的形式化定义为：

$$
\hat{\mathbf{x}}_0^{\mathrm{dir}} = \begin{cases} \hat{\mathbf{x}}_0, & \text{if } t \leq T - T^{\mathrm{guide}} \text{ and } r > R^{\mathrm{guide}} \\ \tilde{\mathbf{x}} \odot \mathbf{m} + \hat{\mathbf{x}}_0 \odot (1 - \mathbf{m}), & \text{else} \end{cases}
$$

该机制通过反复注入噪声并重新去噪，逐步精炼潜变量，有效抑制伪影在去噪轨迹上的累积。消融实验显示，移除重采样退火后 LPIPS 升至 0.382，仅部分伪影被消除，验证了逐步重采样对细化潜变量的必要性。两种退火策略的协同作用是实现高保真外推的不可或缺因素。

### 4. 完全训练无关的 SVD 使用范式

与通常需要针对特定场景微调或训练相机条件模型的做法不同，ViewExtrapolator **直接使用冻结的预训练 SVD 模型**，无需任何额外训练数据或参数更新。这一训练无关的设计使其成为一种通用的推理阶段精炼范式，可灵活应用于不同的 3D 渲染方式（辐射场、点云等），体现了数据与计算的高效性。

ViewExtrapolator 构建了一条**训练无关**的精炼管线，其核心思想是将辐射场在新视角下渲染的伪影视频“融合”进冻结的 Stable Video Diffusion (SVD) 去噪过程，利用 SVD 内化的自然视频先验消除伪影并修补不可见区域，最终输出高保真的外推视图。整个框架由五个关键模块串联而成，形成“渲染—条件注入—引导去噪—退火调控—可选精炼”的闭环。

### 管线总览

如图 3 所示，管线从一段**带有伪影的视频**出发：给定一个外推新视角，系统首先从最近的训练视图出发，逐步向该新视角渲染一帧帧图像，构成一条视频序列。由于辐射场（如 3DGS）在训练视图覆盖范围之外缺乏足够的几何与外观约束，该视频的后期帧通常布满漂浮物、孔洞和模糊等严重伪影。

随后，这段伪影视频被送入 SVD 的去噪循环。SVD 接收两个输入：其一是作为**图像条件**的第一帧（该帧通常无伪影，提供场景的基础内容锚点）；其二是整段视频的噪声潜变量。在去噪的每一步，SVD 会预测一个“干净视频” $\hat{\mathbf{x}}_0$，并据此计算 ODE 导数以推进去噪。

ViewExtrapolator 的核心改造发生在去噪方向上：它不再直接使用 SVD 预测的 $\hat{\mathbf{x}}_0$，而是将原始伪影视频 $\tilde{\mathbf{x}}$ 与 $\hat{\mathbf{x}}_0$ 按**不透明度掩码** $\mathbf{m}$ 进行混合，构造出一个“引导方向” $\hat{\mathbf{x}}_0^{\mathrm{dir}} = \tilde{\mathbf{x}} \odot \mathbf{m} + \hat{\mathbf{x}}_0 \odot (1 - \mathbf{m})$。这一混合操作在不可见区域（掩码为 1）保留伪影视频的粗糙结构，在可见区域（掩码为 0）则完全交由 SVD 的先验生成自然细节，从而在去噪过程中同时实现“结构保持”与“伪影消除”。

### 退火机制的双重调控

单纯的引导去噪存在一个关键矛盾：如果整个去噪过程始终施加伪影视频的引导，SVD 的先验将无法充分施展，导致伪影残留；反之，若过早放弃引导，则场景的粗糙几何和内容可能被 SVD 的自由生成所覆盖，产生语义漂移。为此，ViewExtrapolator 设计了两层退火机制，精细调控引导强度在去噪过程中的衰减：

- **引导退火**：仅在去噪的前 $T^{\mathrm{guide}}$ 步施加混合引导方向，后续步切换为无引导的标准去噪。这使得早期步利用伪影视频锚定场景结构，后期步则完全依赖 SVD 的生成先验来精炼细节、消除残余伪影。

- **重采样退火**：在每个引导去噪步内，执行 $R$ 次“去噪—扩散”重采样循环。仅在前 $R^{\mathrm{guide}}$ 次重采样中使用引导方向，后续重采样无引导。这一机制通过反复精炼潜变量，逐步抑制因引导引入的累积伪影，使潜变量在 SVD 的流形上收敛到更自然的区域。

两层退火的协同作用由组合退火方向公式统一表达：

$$
\hat{\mathbf{x}}_0^{\mathrm{dir}} = 
\begin{cases} 
\hat{\mathbf{x}}_0, & \text{if } t \leq T - T^{\mathrm{guide}} \text{ and } r > R^{\mathrm{guide}} \\ 
\tilde{\mathbf{x}} \odot \mathbf{m} + \hat{\mathbf{x}}_0 \odot (1 - \mathbf{m}), & \text{else} 
\end{cases}
$$

### 输出与可选精炼

去噪完成后，SVD 解码器将最终潜变量解码为精炼后的视频帧。这些帧即为 ViewExtrapolator 的直接输出，可直接作为新视角外推结果使用。此外，论文还在附录中展示了**可选的 3DGS 精炼步骤**：利用精炼后的视频帧对预训练的 3DGS 模型进行微调，进一步提升几何一致性和多视角外观一致性。这一步骤并非必需，但可进一步压缩伪影、锐化细节。

### 通用性

值得注意的是，上述管线对前端渲染方式不敏感。论文验证了该方法可无缝应用于 3D Gaussian Splatting、Instant-NGP 辐射场，以及单视图或单目视频重建的点云渲染，体现了其作为通用后处理精炼器的潜力。整个流程无需对 SVD 进行任何微调，仅依赖其冻结的预训练权重，在数据与计算效率上具有显著优势。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed ViewExtrapolator. We render an artifact-prone video from the closest training view to an extrapolative novel view, and then refine it by guiding SVD to preserve the original scene content and eliminate the artifacts with guidance annealing and resampling annealing*

ViewExtrapolator 的核心创新在于将**冻结的 Stable Video Diffusion (SVD) 预训练模型**作为一个“视频先验修复器”，通过对去噪过程的精细调控，将辐射场渲染的伪影视频精炼为逼真外推视图。整个精炼管线围绕三个关键模块展开：**去噪方向重定向**、**引导退火**和**重采样退火**。

### 3.1 扩散去噪的 EDM 预条件框架

ViewExtrapolator 基于 EDM 预条件框架对 SVD 的去噪过程进行抽象。在扩散时间步 $t$，给定噪声潜变量 $\mathbf{x}_t$，模型 $F_{\pmb{\theta}}$ 预测干净视频 $\hat{\mathbf{x}}_0$：

$$
\hat{\mathbf{x}}_0 = c_{\mathrm{skip}}(\sigma_t) \mathbf{x}_t + c_{\mathrm{out}}(\sigma_t) F_{\pmb{\theta}}(c_{\mathrm{in}}(\sigma_t) \mathbf{x}_t; c_{\mathrm{noise}}(\sigma_t)) \tag{1}
$$

其中 $\sigma_t$ 为当前噪声水平，$c_{\mathrm{skip}}$、$c_{\mathrm{out}}$、$c_{\mathrm{in}}$、$c_{\mathrm{noise}}$ 为 EDM 预条件系数。基于此预测，ODE 导数定义为当前噪声潜变量与预测干净视频之间的残差：

$$
\mathrm{d}\mathbf{x} = (\mathbf{x}_t - \hat{\mathbf{x}}_0) / \sigma_t \tag{2}
$$

该导数指示了从当前噪声状态向干净视频演化的方向。利用欧拉步更新到前一扩散步 $\sigma_{t-1}$ 的潜变量：

$$
\mathbf{x}_{t-1} = \mathbf{x}_t + \mathrm{d}\mathbf{x} (\sigma_{t-1} - \sigma_t) \tag{3}
$$

整个去噪过程被抽象为两个原子操作：`Predict`（公式 (1)）和 `Denoise`（公式 (2)–(3)）。

### 3.2 伪影视频渲染与条件注入

给定预训练的辐射场（如 3DGS）和一组训练视图，ViewExtrapolator 首先从**最近训练视图**到**目标外推新视图**之间渲染一段平滑相机轨迹的视频。由于外推视角远离训练覆盖范围，视频的后期帧包含大量浮空高斯、几何崩塌等伪影（见 Figure 3）。

该伪影视频 $\tilde{\mathbf{x}}$ 作为引导信号，而视频的**第一帧**（无伪影）被注入 SVD 作为图像条件，为去噪过程提供场景的基础内容和结构锚点。

### 3.3 去噪方向重定向：引导去噪

标准扩散去噪完全依赖模型预测 $\hat{\mathbf{x}}_0$ 来驱动潜变量更新。ViewExtrapolator 的核心操作是**修改去噪方向**，将伪影视频 $\tilde{\mathbf{x}}$ 的结构信息融合进更新过程。

具体而言，利用渲染时生成的不透明度掩码 $\mathbf{m}$（标记可见区域与不可见区域），定义引导方向 $\hat{\mathbf{x}}_0^{\mathrm{dir}}$ 为伪影视频与预测干净视频的**逐元素插值**：

$$
\hat{\mathbf{x}}_0^{\mathrm{dir}} = \tilde{\mathbf{x}} \odot \mathbf{m} + \hat{\mathbf{x}}_0 \odot (1 - \mathbf{m}) \tag{4}
$$

其中 $\odot$ 表示逐元素乘法。在掩码 $\mathbf{m}$ 标记的可见区域，引导方向保留伪影视频的原始像素；在不可见区域，则采用 SVD 预测的生成内容。随后，用该引导方向替代标准预测方向执行去噪：

$$
\mathbf{x}_{t-1} = \mathrm{Denoise}(\mathbf{x}_t, \hat{\mathbf{x}}_0^{\mathrm{dir}}) \tag{5}
$$

这一设计使去噪过程在**保留可见区域内容**的同时，利用 SVD 的生成先验**修补不可见区域并消除伪影**。

### 3.4 双重退火策略：引导退火与重采样退火

直接在整个去噪过程中持续施加引导（公式 (5)）会导致两个问题：(1) 去噪后期模型应自由生成自然细节，伪影视频的持续引导会干扰这一过程；(2) 单步去噪无法充分精炼潜变量，伪影可能累积。为此，ViewExtrapolator 设计了**引导退火**和**重采样退火**两个互补机制。

**引导退火**限制引导去噪仅在最初的 $T^{\mathrm{guide}}$ 步执行，后续步骤切换为无引导的标准去噪，让 SVD 在先验分布下自由生成无伪影的自然细节。

**重采样退火**在每个引导去噪步内执行 $R$ 次“去噪-扩散”循环，且仅在前 $R^{\mathrm{guide}}$ 次重采样中使用引导方向，后续重采样无引导。这相当于在潜变量空间中逐步精炼，反复利用 SVD 先验修复残留伪影。

两种退火策略通过以下统一条件实现：

$$
\hat{\mathbf{x}}_0^{\mathrm{dir}} = \begin{cases} \hat{\mathbf{x}}_0, & \text{if } t \leq T - T^{\mathrm{guide}} \text{ and } r > R^{\mathrm{guide}} \\ \tilde{\mathbf{x}} \odot \mathbf{m} + \hat{\mathbf{x}}_0 \odot (1 - \mathbf{m}), & \text{else} \end{cases} \tag{6}
$$

其中 $t$ 为去噪步索引，$r$ 为重采样步索引。当去噪步已超出引导窗口（$t \leq T - T^{\mathrm{guide}}$）且重采样步已超出引导重采样窗口（$r > R^{\mathrm{guide}}$）时，使用纯 SVD 预测方向；否则使用混合引导方向。

消融实验（Table 1, Figure 8）为双重退火的必要性提供了强证据：移除引导退火（w/o GA）使 LPIPS 从 0.378 急升至 0.448，视觉上大部分伪影未得到纠正；移除重采样退火（w/o RA）使 LPIPS 升至 0.382，仅部分伪影被消除。两者协同作用是实现高保真外推精炼的关键。

### 3.5 外推度量化

为系统衡量外推难度，论文定义了外推度 $e$。设训练视图沿方向 $\mathbf{d}$ 的最大跨度为 $r$，新视图到训练视图中心的距离为 $\|\mathbf{d}\|$，则：

$$
r = \max_i(\mathbf{p}_i \cdot \frac{\mathbf{d}}{\|\mathbf{d}\|}) - \min_i(\mathbf{p}_i \cdot \frac{\mathbf{d}}{\|\mathbf{d}\|}) \tag{7}
$$

$$
e = \frac{\|\mathbf{d}\|}{r} \tag{8}
$$

$e$ 越大，表示新视图离训练视图覆盖范围越远，外推难度越高。LLFF-Extra 基准的平均 $e$ 达到 5.4，而现有基准的 $e$ 普遍较小（Figure 6），验证了该基准对外推评估的针对性。

### 补充图表

## 实验与关键发现

### 基准构建：LLFF-Extra

现有新视角合成基准（如 LLFF、NeRF-LLFF）中的测试视图通常紧邻训练视图分布，其外推度 $e$ 普遍较小，本质上仍属于插值范畴（Figure 6）。为系统性评估真实外推能力，作者在 LLFF 数据集基础上构建了 **LLFF-Extra** 基准：将训练视图限制在场景前方的一个狭窄扇区内，测试视图则大幅偏离至训练视图范围之外，使得平均外推度 $e$ 达到 5.4，远超现有基准。外推度 $e$ 的定义为：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/007_Figure_6.jpg]]
*Figure 6: Distributions of extrapolation degree e across existing benchmarks and our proposed LLFF-Extra. Unlike LLFF-Extra, all existing benchmarks exhibit a small e, indicating that they predominantly focus on the evaluation of novel view interpolation instead of extrapolation*

$$r = \max_i(\mathbf{p}_i \cdot \frac{\mathbf{d}}{\|\mathbf{d}\|}) - \min_i(\mathbf{p}_i \cdot \frac{\mathbf{d}}{\|\mathbf{d}\|})$$

$$e = \frac{\|\mathbf{d}\|}{r}$$

其中 $\mathbf{d}$ 为新视图到训练视图中心的距离向量，$r$ 为训练视图沿 $\mathbf{d}$ 方向的最大跨度（Figure 5）。这一设计确保评估的是模型对不可见区域的真实外推能力，而非对训练分布的插值记忆。

### 主实验结果

在 LLFF-Extra 基准上，ViewExtrapolator 以 **3DGS**（Kerbl et al., SIGGRAPH 2023）为渲染后端，在所有指标上均显著超越基线方法（Table 1）：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons and ablation studies. The first four rows present the comparison results, while the last two rows show the ablation studies. ViewExtrapolator w/o GA denotes results without guidance annealing, and ViewExtrapolator w/o RA denotes results without resampling annealing*

| 方法 | SSIM ↑ | PSNR ↑ | LPIPS ↓ |
|------|--------|--------|---------|
| 3DGS | 0.416 | 14.46 | 0.429 |
| DRGS | 0.406 | 14.68 | 0.457 |
| **ViewExtrapolator (3DGS)** | **0.460** | **15.46** | **0.378** |

ViewExtrapolator 相对 3DGS 基线在 SSIM 上提升 0.044，PSNR 提升 1.00 dB，LPIPS 降低 0.051。这一增益源于 SVD 生成先验对伪影区域的“想象性修补”——基线方法因训练视图未覆盖外推区域，渲染出大量空洞、模糊和几何崩塌伪影，而 ViewExtrapolator 通过引导去噪机制在保留可见内容的同时，利用视频扩散模型的自然视频分布先验填充了不可见区域的逼真细节（Figure 4、Figure 9）。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparisons. We compare ViewExtrapolator with 3DGS and DRGS on novel view extrapolation. ViewExtrapolator demonstrates superior generation quality with much fewer artifacts. The last column shows the distribution of training and test views as well as the corresponding extrapolation degree e. Zoom in for details*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/010_Figure_9.jpg]]
*Figure 9: Additional comparisons. We compare ViewExtrapolator with 3DGS and DRGS on novel view extrapolation. ViewExtrapolator demonstrates superior generation quality with much fewer artifacts. The last column shows the distribution of training and test views as well as the corresponding extrapolation degree e. Zoom in for details*

定性对比显示，3DGS 和 DRGS 在外推视图中产生明显的漂浮高斯碎片和纹理撕裂，而 ViewExtrapolator 精炼后的视图在结构完整性和视觉真实感上均有质的提升。

### 消融实验：退火策略的必要性

为验证两个核心设计——**引导退火**（Guidance Annealing, GA）和**重采样退火**（Resampling Annealing, RA）——的独立贡献，作者进行了严格的消融实验（Table 1 后两行；Figure 8）：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/009_Figure_8.jpg]]
*Figure 8: Ablation studies. We show the ablation results for 3DGS and point cloud renderings. As point clouds are used for single-image novel view extrapolation without ground truth, we show the input image for reference instead. As highlighted in the red circles, both guidance annealing and resampling annealing are essential for artifact refinement. Please zoom in for details*

| 消融变体 | SSIM ↑ | PSNR ↑ | LPIPS ↓ |
|----------|--------|--------|---------|
| ViewExtrapolator (完整) | 0.460 | 15.46 | 0.378 |
| w/o GA（移除引导退火） | 0.442 | 15.14 | 0.448 |
| w/o RA（移除重采样退火） | 0.456 | 15.33 | 0.382 |

**移除引导退火**导致 LPIPS 从 0.378 急剧恶化至 0.448，SSIM 下降 0.018。视觉上，大部分伪影未被纠正（Figure 8 红圈标注区域），说明若整个去噪过程持续施加伪影视频的引导，SVD 的先验无法在后期有效“覆盖”这些伪影——模型被锁定在输入伪影的分布附近，丧失了生成自然细节的能力。引导退火的本质是在去噪前期利用伪影视频提供粗糙的几何和内容约束，后期则完全释放 SVD 的生成能力，使其在先验分布下自由修补。

**移除重采样退火**使 LPIPS 升至 0.382，虽劣化幅度小于移除 GA，但视觉上仍有部分伪影残留。重采样退火在每个引导步内执行多次“去噪-扩散”循环，并逐步关闭引导，反复精炼潜变量。缺少这一机制时，单次引导去噪无法充分消除累积的伪影信号，导致最终输出中仍有可察觉的失真。

两个退火机制呈现**协同效应**：引导退火负责宏观的“何时停止引导”，重采样退火负责微观的“如何在引导步内精细调控”。两者缺一不可，共同构成了 ViewExtrapolator 高保真外推的基础。

### 跨渲染后端的通用性

ViewExtrapolator 作为一种训练无关的推理阶段精炼范式，可无缝适配不同的 3D 渲染后端。除 3DGS 外，作者验证了其在 **Instant-NGP**（NeRF 变体）和**点云**渲染上的有效性（Figure 7）。对于点云渲染，即使输入仅为单张图像或单目视频，ViewExtrapolator 仍能精炼出视觉合理的外推视图。这种通用性源于方法的核心设计——仅依赖渲染视频的帧序列和预训练 SVD 的先验，而不对渲染管线的内部表示做任何假设。

### 失败模式与局限性

尽管 ViewExtrapolator 在标准外推场景下表现出色，其能力边界受限于以下因素（Figure 10）：

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/011_Figure_10.jpg]]
*Figure 10: Limitations and failure cases. The generation quality would degrade when handling (a) novel views at extreme angles or (b) dynamic videos with rapid motion. (The top row in each section is the rendered artifact-prone video and the bottom row is the refined video.)*

1. **极端视角退化**：当新视角与训练视图几乎无重叠（极端角度旋转），SVD 先验缺乏足够的场景内容锚点，生成结果出现结构崩塌和严重的语义不一致。
2. **动态场景快速运动**：对于包含快速相机运动或物体运动的动态视频，时序一致性难以维持，精炼后的视频可能出现抖动或内容跳变。
3. **SVD 固有缺陷继承**：作为完全冻结的预训练模型，SVD 的低分辨率输出、颜色偏移等固有问题会直接传递到最终结果中。
4. **推理效率**：单段视频（25 帧）的精炼耗时约 3 分 20 秒（A5000 GPU），尚无法满足实时应用需求。

这些失败模式揭示了当前方法的根本瓶颈：**生成先验的质量上限决定了外推质量的上限**。在域差距过大或运动模式超出 SVD 训练分布的场景中，先验本身不再可靠，引导机制难以弥补这一缺口。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2411_14208/figures/008_Figure.jpg]]
*Figure: (a) 3D Gaussian Splatting (b) Instant NGP (c) Point cloud from single view*

## 定位与知识库关联

### 1. 与基线方法的关系

ViewExtrapolator 定位为一种**推理阶段的新视角外推精炼器**，其核心贡献在于将预训练视频扩散模型的生成先验引入辐射场渲染的后处理流程，而非重新设计三维重建方法。因此，它与两类基线形成互补或替代关系。

**相对于辐射场渲染基线（3DGS、DRGS）**
- **3D Gaussian Splatting (3DGS)**（Kerbl et al., SIGGRAPH 2023）和 **DRGS** 是 ViewExtrapolator 的直接渲染上游。这两类方法在训练视图范围内的插值表现优异，但在外推视角下因缺乏训练覆盖而产生大量伪影和结构崩塌——这正是 ViewExtrapolator 所瞄准的瓶颈。
- ViewExtrapolator 不修改 3DGS 或 DRGS 的重建过程，而是将其渲染的伪影视频作为输入，通过 SVD 引导去噪进行精炼。定量结果表明，ViewExtrapolator（以 3DGS 为渲染后端）在 LLFF-Extra 上将 SSIM 从 0.416 提升至 0.460，PSNR 从 14.46 提升至 15.46，LPIPS 从 0.429 降至 0.378（Table 1），验证了该后处理策略的有效性。

**相对于视频扩散模型的直接应用**
- 标准的 Stable Video Diffusion（SVD）具备图像条件视频生成能力，但如果直接用于外推帧生成，缺乏对场景已有几何结构的保持机制，容易产生内容漂移。
- ViewExtrapolator 通过**修改 ODE 导数方向**（Eq. (4)–(5)）将伪影视频与 SVD 预测的干净视频按不透明度掩码混合，使得去噪过程既保留了可见区域的场景内容，又利用 SVD 先验修补不可见区域。这一“引导去噪”范式区别于传统的分类器引导或无分类器引导，是一种面向结构保持的引导策略。

### 2. 方法谱系中的定位

ViewExtrapolator 处于以下几条研究线的交汇点：

**新视角合成 → 外推扩展**
现有新视角合成方法（NeRF 系列、3DGS 系列）主要面向插值场景。ViewExtrapolator 通过定义外推度 $e = \frac{\|\mathbf{d}\|}{r}$（Eq. (7)–(8)）明确量化了外推程度，并构建了平均 $e=5.4$ 的 LLFF-Extra 基准（Figure 6），将评估焦点从插值转向外推。这为后续研究提供了问题定义和评估框架。

**扩散先验用于三维场景**
近年来，利用预训练扩散模型为三维重建提供先验的工作逐渐增多。ViewExtrapolator 的独特之处在于：**完全训练无关**（training-free），直接使用冻结的 SVD（xt-1-1 版本），无需针对特定场景微调或训练相机条件模型。这使得方法具有即插即用的通用性——论文展示了其对 3DGS、Instant-NGP 和点云渲染的精炼能力（Figure 7）。

**退火策略在生成控制中的应用**
引导退火和重采样退火是 ViewExtrapolator 的关键设计。消融实验表明，移除引导退火使 LPIPS 从 0.378 急升至 0.448，移除重采样退火使 LPIPS 升至 0.382（Table 1），且视觉上伪影明显残留（Figure 8）。这一发现揭示了一个深层原理：在扩散早期施加结构引导、后期释放生成自由度，是平衡内容保持与伪影消除的有效范式，可推广至其他需要“先约束后生成”的场景。

### 3. 适用边界

**有效场景**
- 静态场景的适度外推（外推度 $e$ 在训练视图范围的数倍以内）。
- 多视角训练数据可用的场景（用于构建辐射场或点云）。
- 渲染伪影以结构失真和模糊为主，而非完全缺失内容的场景。

**失效场景**
- **极端视角外推**：当新视角与训练视图几乎无重叠时，生成质量明显下降，易出现结构崩塌（Figure 10a）。
- **快速运动动态视频**：SVD 对快速运动场景的建模能力有限，导致外推帧出现大量伪影（Figure 10b）。
- **域差距大的场景**：方法依赖 SVD 在自然视频上的预训练先验，在水下、医疗影像等域差距较大的场景中的有效性尚未验证。

### 4. 局限性与开放问题

**已知局限**
1. **分辨率与质量上限**：受限于 SVD 模型，继承其低分辨率和颜色偏移等问题。
2. **推理效率**：每段视频约需 3 分 20 秒（A5000 GPU），难以满足实时应用需求。
3. **场景类型受限**：仅验证了静态场景和简单动态场景，未覆盖复杂多物体交互或长序列外推。

**开放问题**
1. **高分辨率扩展**：能否将退火策略迁移到更高分辨率的视频扩散模型，突破当前分辨率瓶颈？
2. **自适应退火参数**：当前 $T^{\text{guide}}$ 和 $R^{\text{guide}}$ 为固定超参数，能否根据外推度 $e$ 动态调节引导强度？
3. **几何约束融合**：如何将 ViewExtrapolator 与三维重建的几何约束（如多视图一致性）结合，在更多不可见区域中保持准确的几何结构？
4. **跨域泛化**：在域差距较大的场景中，是否需要轻量适配策略（如少量域内数据的提示微调）来激活 SVD 先验？
5. **范式推广**：该推理阶段精炼范式是否可推广至其他生成式扩散模型（文本到视频、可控视频生成），以实现更多类型的外推或修复任务？

*注：DRGS 在论文中未给出全称和引用，可能为密集高斯变体，其与 3DGS 的具体差异需查阅原文或联系作者确认。*

## 原文 PDF

![[paperPDFs/arxiv_2024/Novel_View_Extrapolation_with_Video_Diffusion_Priors.pdf]]

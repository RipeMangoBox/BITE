---
title: "Proxy-GS: Unified Occlusion Priors for Training and Inference in Structured 3D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Proxy_GS_Unified_Occlusion_Priors_for_Training_and_Inference_in_Structured_3D_Gaussian_Splatting.pdf
project_link: null
code_link: "https://github.com/graphdeco-inria/fast-gaussian-rasterization"
aliases:
- PG
- Proxy-GS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 轻量级代理网格（proxy mesh）与硬件光栅化结合，以极低延迟（<1 ms）提供精确的遮挡深度图，成为统一训练和推理阶段遮挡剔除与锚点致密化的关键先验。
primary_logic: 通过在训练和推理阶段使用相同的代理网格深度先验，一致地执行遮挡剔除和表面引导的锚点致密化，既消除了被遮挡区域的计算浪费，又促进了锚点沿真实几何结构生长，从而在显著提升渲染速度的同时改善或保持了渲染质量。
claims:
- 在遮挡严重的MatrixCity Streets数据集上，Proxy-GS相比Octree-GS实现超过2.5倍加速，同时渲染质量（PSNR、SSIM）均有提升。
- 消融实验表明，仅推理时使用代理遮挡剔除会导致渲染质量大幅下降（PSNR从21.41降至19.06），而训练和推理均使用代理先验并加入代理引导致密化（ID 4）获得最佳质量与速度权衡。
- 轻量级代理深度渲染仅需约1 ms，且降低代理网格分辨率对PSNR影响极小，验证了方法对代理精度的鲁棒性。
- MatrixCity Block 5 上 PSNR↑ = 21.68
---

# Proxy-GS: Unified Occlusion Priors for Training and Inference in Structured 3D Gaussian Splatting

> [!tip] 核心洞察
> 通过在训练和推理阶段使用相同的代理网格深度先验，一致地执行遮挡剔除和表面引导的锚点致密化，既消除了被遮挡区域的计算浪费，又促进了锚点沿真实几何结构生长，从而在显著提升渲染速度的同时改善或保持了渲染质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Proxy-GS：统一遮挡先验的结构化3D高斯泼溅训练与推理框架 |
| 英文题名 | Proxy-GS: Unified Occlusion Priors for Training and Inference in Structured 3D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.24421) · [Code](https://github.com/graphdeco-inria/fast-gaussian-rasterization) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Proxy-GS |
| Dataset | MatrixCity Block 5, Small City, Berlin |

> [!tip] 效果简介
> - MatrixCity Block 5 上，PSNR↑ 21.68 vs 21.41 (Octree-GS) (+0.27)；FPS↑ 151 vs 48 (Octree-GS) (+103 (约3.1×))。
> - Small City (real-world, heavy occlusion) 上，PSNR↑ 23.09 vs 23.03 (Octree-GS) (+0.06)。
> - Small City 上，FPS↑ 139 vs 51 (Octree-GS) (+88 (约2.73×))。

## 概要

现有基于MLP的3D高斯泼溅（3DGS）方法缺乏有效的遮挡感知能力。在训练和推理过程中，大量锚点（anchor）和高斯原语（Gaussian）被放置于被遮挡区域，这些不可见元素仍需经过MLP解码和光栅化管线，造成显著的计算冗余。这一问题在遮挡严重的大规模城市街道场景和多房间室内场景中尤为突出，成为制约渲染速度的主要瓶颈。

针对上述问题，本文提出**Proxy-GS**——一个基于统一遮挡先验的结构化3DGS训练与推理框架。其核心洞察在于：通过引入轻量级代理网格（proxy mesh）并利用硬件光栅化实时生成精确的遮挡深度图，可以在训练和推理阶段一致地执行遮挡剔除与表面引导的锚点致密化。这一设计同时达成两个目标：（1）消除被遮挡区域的计算浪费，大幅提升推理速度；（2）引导锚点沿真实几何表面生长，改善或保持渲染质量。

在方法定位上，Proxy-GS以**Octree-GS**为基线框架，继承其MLP解码器与八叉树LOD结构，但将改进聚焦于遮挡感知机制：将基于代理深度的逐像素遮挡剔除与视锥剔除融合为单个CUDA内核，并引入代理引导的表面致密化策略，使锚点生长与场景几何保持一致。与**Scaffold-GS**、**Hierarchical-GS**等依赖梯度信号或LOD合并的方法相比，Proxy-GS的遮挡先验在训练与推理间保持统一，避免了锚点分布与几何结构脱节的问题。

实验结果表明，在遮挡严重的MatrixCity Streets数据集上，Proxy-GS相比Octree-GS实现了超过**2.5倍**的渲染加速（FPS从48提升至151），同时PSNR和SSIM均有提升。在真实城市场景Small City上，FPS从51提升至139（约2.73倍），PSNR从23.03提升至23.09。消融实验进一步验证了训练与推理统一使用代理先验的必要性：仅在推理时使用遮挡剔除会导致PSNR大幅下降（从21.41降至19.06），而训练和推理均启用代理引导致密化可获得最佳的质量-速度权衡。轻量级代理深度渲染仅需约**1 ms**，且对代理网格分辨率不敏感，表明该方法对代理精度具有良好的鲁棒性。

### 3D高斯泼溅及其结构化演进

基于3D高斯泼溅（3DGS）的显式辐射场表达已成为新视角合成的主流范式。其核心思想是将场景表达为一组可微的三维高斯原语，通过基于瓦片的快速光栅化实现实时渲染。然而，原始3DGS为每个高斯独立优化全部属性（位置、协方差、颜色、不透明度），导致在大规模场景中高斯数量急剧膨胀，存储与渲染开销随之失控。

为缓解这一问题，基于MLP的结构化3DGS方法被提出。这类方法引入稀疏锚点（anchor）作为场景的紧凑表达，每个锚点携带一个可学习的特征向量 $f_i$，通过共享的MLP解码器根据观测方向 $v_i$ 动态生成其邻域内的高斯属性：

$$\{ \mu_j, \Sigma_j, c_j, \alpha_j \}_{j\in\mathcal{M}} = \mathrm{MLP}_\theta (f_i, v_i)_{i\in\mathcal{N}}$$

其中 **Scaffold-GS** 使用体素锚点，**Octree-GS** 进一步引入八叉树LOD策略，在保持渲染质量的同时有效压缩了模型规模。Proxy-GS正是以Octree-GS为基础框架构建的。

### 被忽视的遮挡计算浪费

尽管结构化方法有效压缩了场景表达，但它们普遍缺乏**遮挡感知能力**。在训练和推理过程中，锚点和由其解码生成的高斯大量分布在被遮挡区域——例如建筑物背面、室内隔墙后方、或街道视角下被前景完全遮蔽的远处结构。这些不可见的锚点仍需经过MLP解码和光栅化管线处理，产生大量无效计算。

这一问题在**遮挡严重的大规模场景**中尤为突出。以MatrixCity城市街道数据集和Small City真实场景为例，建筑物密集排列、视角受限，被遮挡区域占比极高。现有方法对此缺乏显式建模：训练时的锚点致密化仅依赖梯度信号，可能在遮挡区域产生冗余锚点；推理时的LOD选择仅基于距离，无法区分可见与遮挡。其结果是，大量GPU时间消耗在对最终渲染毫无贡献的解码与光栅化操作上。

### 现有遮挡处理方案的局限

针对3DGS的遮挡剔除已有初步探索，但存在明显不足：

- **训练与推理不一致**：部分方法仅在推理阶段引入遮挡剔除，而训练过程未考虑遮挡先验。这导致训练时锚点与高斯的分布未针对可见性优化，推理时强行剔除会破坏训练阶段建立的锚点-高斯一致性，造成渲染质量显著下降。
- **深度获取代价过高**：若使用nvdiffrast等软件光栅化或从预训练3DGS模型中提取深度图，耗时远超实时渲染的容忍范围（如nvdiffrast仅深度渲染即需数十毫秒），抵消了遮挡剔除带来的加速收益。

### 核心动机：统一遮挡先验

本文的核心动机在于：**能否以极低的计算代价，在训练和推理阶段一致地引入遮挡先验，从而同时实现加速渲染和质量保持？**

关键洞察是：轻量级的代理网格（proxy mesh）可通过硬件光栅化在1毫秒内生成精确的遮挡深度图，这一深度先验既可指导推理时的锚点剔除，又可引导训练时的锚点致密化沿真实几何表面生长。训练与推理使用相同的遮挡先验，保证了锚点分布与可见性结构的一致性，从而在显著减少解码和渲染计算量的同时，维持甚至提升渲染质量。

## 核心方法与创新机理

Proxy-GS 的核心创新在于将**轻量级代理网格（proxy mesh）**作为统一的遮挡先验，同时作用于训练与推理两个阶段，系统性地解决了现有 MLP-based 3D 高斯泼溅方法中因缺乏遮挡感知而导致的计算冗余与几何生长盲目性问题。该方法通过四个关键 changed slots 实现突破：

### 1. 统一遮挡剔除机制：从“无显式遮挡建模”到“代理深度驱动的逐像素剔除”

**Baseline 状态**：Octree-GS 等结构化 3DGS 方法仅依赖训练时的自然淘汰或简单的 LOD 距离选择，未显式建模遮挡关系，导致大量锚点和高斯分布位于被遮挡区域，造成无效解码与渲染计算。

**Proxy-GS 方案**：引入基于代理网格深度图的逐像素遮挡剔除，与视锥剔除融合在单个 CUDA 内核中执行（Section 4.2）。具体而言，对于每个锚点，将其投影到图像平面后，与代理深度图进行深度测试：若锚点的相机空间深度 $z_{\mathrm{h}}$ 大于调整后的代理深度 $\hat{d}(x_{\mathrm{pix}}, y_{\mathrm{pix}}) + \gamma$，则剔除该锚点（其中 $\gamma$ 为安全裕度）。这一机制使推理时的平均解码锚点数量大幅减少，在 MatrixCity Block 5 上从 Octree-GS 的基线水平降至约 1/3，直接贡献了超过 3× 的 FPS 提升（Table 3）。

### 2. 代理引导的表面致密化：从“梯度驱动盲目生长”到“几何结构感知的锚点生长”

**Baseline 状态**：基于梯度的致密化策略可能在遮挡区域或空旷空间中产生冗余锚点，锚点生长缺乏对场景真实几何结构的感知。

**Proxy-GS 方案**：提出代理引导的表面致密化（Proxy-Guided Densification，Section 4.3），利用代理深度和补丁渲染误差选择表面位置生成新锚点。具体流程为：将图像划分为补丁 $\mathcal{P}$，计算每个补丁的平均损失 $\ell_{\mathcal{P}}$，选择损失大于全局平均 3 倍的补丁（$\ell_{\mathcal{P}} > 3\bar{\ell}$）；随后利用相机内外参和代理深度 $d_{\mathrm{mesh}}$ 将选中像素反向投影到 3D 空间作为新锚点位置 $\hat{\mathbf{p}}_{\mathcal{P}}$。同时，通过代理网格密度控制（将空间划分为网格，每个单元最多容纳 $K$ 个锚点）防止冗余生长。这一策略使锚点沿真实几何结构生长，而非在遮挡区域浪费容量。

### 3. 极低延迟的深度获取：从“无深度或慢速深度”到“硬件光栅化亚毫秒级深度图”

**Baseline 状态**：不使用深度图，或使用 nvdiffrast 等非实时方法获取深度，无法满足实时渲染需求。

**Proxy-GS 方案**：使用轻量级代理网格进行硬件光栅化，结合集群剔除（cluster culling）、Hi-Z 和 Early-Z 等现代 GPU 特性，在约 1 ms 内生成 1000×1000 深度图，并通过 Vulkan-CUDA 互操作实现 GPU 零拷贝数据传输（Section 4.2 及 Appendix 7.6）。对比实验表明，该方案相比 nvdiffrast 等替代方案在 FPS 上具有压倒性优势（Table 6）。

### 4. 训练与推理一致性：从“阶段间机制不一致”到“统一的遮挡先验驱动”

**Baseline 状态**：训练和推理的锚点选择机制可能不一致（如推理时使用 LOD 而训练时未使用），导致训练-推理分布偏移。

**Proxy-GS 方案**：训练和推理均采用相同的代理引导遮挡剔除和致密化策略，保持锚点与场景几何的一致性。消融实验（Table 3）揭示了这一一致性的关键作用：仅推理时使用代理遮挡剔除（ID 2）虽带来超过 3× 的 FPS 提升，但 PSNR 从 21.41 骤降至 19.06，因为训练时未考虑遮挡导致锚点-高斯一致性被破坏；而在训练和推理中均启用代理遮挡剔除（ID 3）即可超过基线渲染质量（PSNR 21.50），再加入代理引导致密化（ID 4）进一步将 PSNR 提升至 21.68，同时保持高 FPS（143）。

**创新本质总结**：Proxy-GS 并非提出全新的表示或渲染范式，而是通过引入一个极低成本的几何代理，将“遮挡感知”系统性地注入到结构化 3DGS 的训练与推理全流程中。这一设计使得计算资源从被遮挡的无效区域重新分配到可见的几何表面，在显著加速渲染的同时改善或保持了渲染质量——这一“加速且提质”的特性在遮挡严重的场景中尤为突出（MatrixCity Streets 上超过 2.5× 加速且 PSNR 提升 0.27 dB）。

Proxy-GS 的整体框架围绕一个核心设计原则展开：**在训练与推理阶段统一使用轻量级代理网格提供的遮挡深度先验**，实现对结构化 3D 高斯泼溅（3DGS）中锚点与高斯的遮挡感知管理。如 Figure 2 所示，框架由四个关键模块串联构成，形成从几何先验构建到最终渲染的完整流水线。

![[assets/figures/papers/paper_list_l2038_https_arxiv_org_abs_2509_24421/figures/002_Figure_2.jpg]]
*Figure 2: Proxy-GS Framework. We first construct a lightweight proxy mesh. During rendering, hardware rasterization produces a depth map in under 1 ms, which is then used to efficiently cull anchors that are occluded. During training, in addition to the same rendering pipeline, we further introduce structure-aware anchor densification, encouraging anchors to grow adaptively along the proxy mesh geometry*

**代理网格构建。** 框架首先根据场景类型（室外街道、室内多房间、密集或稀疏点云）采用不同策略生成简化的代理网格（proxy mesh）。该网格作为场景几何的轻量级近似，为后续的深度获取和锚点致密化提供统一的几何先验（详见 Section 4.2 及 Appendix 7.5）。

**快速深度获取。** 在每次渲染时，利用硬件光栅化（hardware rasterization）对代理网格进行极低延迟的深度渲染。通过结合集群剔除（cluster culling）、Hi-Z 和 Early-Z 等 GPU 硬件特性，该模块可在约 1 ms 内生成 1000×1000 分辨率的线性相机空间深度图。深度数据通过 Vulkan-CUDA 互操作实现 GPU 端零拷贝传输，避免了 CPU-GPU 数据搬运的开销（详见 Section 4.2 及 Appendix 7.6）。

**锚点遮挡剔除。** 获得代理深度图后，框架在单个 CUDA 内核中融合视锥剔除（frustum culling）与基于深度的遮挡剔除。对于每个锚点，将其投影到图像平面，查询对应像素的代理深度，若锚点的相机空间深度大于调整后的代理深度（加安全裕度 $\gamma$），则判定该锚点被遮挡并予以剔除。这一操作从源头过滤了大量位于遮挡区域、本不会对最终渲染产生贡献的锚点，从而显著减少后续 MLP 解码和光栅化的计算量。

**代理引导训练致密化。** 在训练阶段，框架在相同的遮挡剔除流水线之上引入结构感知的锚点致密化策略。具体而言，将图像划分为补丁（patch），计算每个补丁的平均渲染损失 $\ell_{\mathcal{P}}$，选择损失大于全局平均 3 倍的补丁作为致密化候选区域。对于选中的像素，利用相机内外参和代理深度将其反向投影到 3D 空间，得到位于代理网格表面附近的新锚点位置。同时，通过密度网格（每个网格单元最多容纳 $K$ 个锚点）控制锚点增长，防止在已充分表达的区域产生冗余。

**神经高斯解码与渲染。** 经过遮挡剔除后保留的锚点，其特征 $f_i$ 与观测方向 $v_i$ 被送入 MLP 解码器，生成对应高斯的均值、协方差、颜色和透明度等属性，随后执行标准的 3DGS 光栅化渲染。

框架的关键创新在于**训练与推理的一致性**：推理时的遮挡剔除与训练时的致密化均依赖同一代理网格深度先验。这种一致性确保了训练过程中锚点的生长与推理时的可见性判断相匹配——锚点被引导沿真实几何表面生长，而非在遮挡区域无效增殖，从而在消除计算浪费的同时促进锚点布局的结构合理性。消融实验（Table 3）充分验证了这一设计：仅在推理时使用代理遮挡剔除会导致 PSNR 从 21.41 大幅下降至 19.06，而训练与推理均启用代理先验并加入代理引导致密化可获得最佳的渲染质量与速度权衡（PSNR 21.68，FPS 143）。

![[assets/figures/papers/paper_list_l2038_https_arxiv_org_abs_2509_24421/figures/001_Figure_1.jpg]]
*Figure 1: We propose Proxy-GS, an occlusion-aware training and inference framework built upon lightweight proxies. By introducing proxy-guided densification, our method effectively guides anchors to grow in more geometrically meaningful regions. As a result, Proxy-GS not only achieves higher rendering quality but also delivers significantly faster rendering compared to state-of-the-art MLP-based 3DGS approaches*

### 整体框架

Proxy-GS 的核心设计是在现有 MLP-based 3DGS 框架（以 Octree-GS 为基础）上引入统一的遮挡先验。如 Figure 2 所示，框架包含两大关键模块：**代理引导的遮挡剔除**（推理阶段）和**代理引导的表面致密化**（训练阶段）。两者共享同一个轻量级代理网格，通过硬件光栅化实时生成深度图，确保训练与推理的几何一致性。

### 神经高斯解码（基础模块）

Proxy-GS 继承了结构化 3DGS 的 MLP 解码范式。给定锚点特征 $f_i$ 和观测方向 $v_i$，MLP 解码出每个锚点对应的多个高斯属性：

$$\{ \mu_j, \Sigma_j, c_j, \alpha_j \}_{j\in\mathcal{M}} = \mathrm{MLP}_\theta (f_i, v_i)_{i\in\mathcal{N}}$$

其中 $\mu_j$ 为高斯均值（位置），$\Sigma_j$ 为协方差矩阵，$c_j$ 为颜色，$\alpha_j$ 为透明度。$\mathcal{N}$ 为锚点集合，$\mathcal{M}$ 为解码出的高斯集合。该模块本身并非 Proxy-GS 的创新，但其计算开销与锚点数量成正比——这正是遮挡剔除的核心优化目标。

### 快速深度获取模块

Proxy-GS 利用硬件光栅化管线，在极低延迟下生成代理网格的深度图。具体流程为：

1. **代理网格构建**：根据场景类型（室外/室内、密集/稀疏点云）采用不同策略生成简化网格（详见附录 7.5）。
2. **硬件光栅化**：利用集群剔除（Cluster Culling）、层次化深度剔除（Hi-Z）和 Early-Z 等 GPU 硬件特性，在约 1 ms 内渲染 1000×1000 分辨率的深度图。
3. **Vulkan-CUDA 互操作**：通过 GPU 零拷贝机制，将深度图直接传递到 CUDA 端，避免 CPU-GPU 数据传输瓶颈。

硬件深度值 $z_{hw}$ 需转换为线性相机空间深度，以支持后续的遮挡测试：

$$d_{\mathrm{mesh}}(x_{\mathrm{pix}}, y_{\mathrm{pix}}) = \frac{n f}{f - z_{hw}(x_{\mathrm{pix}}, y_{\mathrm{pix}})(f - n)}$$

其中 $n$ 和 $f$ 分别为近平面和远平面距离。

### 锚点遮挡剔除模块

遮挡剔除与视锥剔除融合在单个 CUDA 内核中执行，流程如下：

**步骤 1：锚点投影**。将每个锚点的 3D 位置 $\mathbf{p}$ 投影到图像平面，计算其像素坐标：

$$x_{\mathrm{pix}} = \left\lfloor \frac{(x_{\mathrm{ndc}}+1)}{2}\cdot W \right\rfloor, \quad y_{\mathrm{pix}} = \left\lfloor \frac{(y_{\mathrm{ndc}}+1)}{2}\cdot H \right\rfloor$$

其中 $(x_{\mathrm{ndc}}, y_{\mathrm{ndc}})$ 为归一化设备坐标，$W$ 和 $H$ 为图像宽高。

**步骤 2：深度测试**。将锚点的相机空间深度 $z_{\mathrm{h}}$ 与对应像素的代理深度 $\hat{d}$ 进行比较：

$$\mathbf{Cull}(\mathbf{p}) = \left\{ \mathrm{true}, \; z_{\mathrm{h}} > \hat{d}(x_{\mathrm{pix}}, y_{\mathrm{pix}}) + \gamma \right.$$

若锚点深度大于代理深度（加安全裕度 $\gamma$），则判定为被遮挡，予以剔除。安全裕度 $\gamma$ 用于补偿代理网格与真实几何之间的偏差，消融实验表明 $\gamma=0.3$ 在渲染质量与 FPS 之间取得最佳折衷（Table 10）。

**步骤 3：过滤执行**。被剔除的锚点不会进入后续的 MLP 解码和高斯光栅化阶段，从而直接减少计算量。

### 代理引导的表面致密化模块

训练阶段的致密化策略是 Proxy-GS 的另一核心创新，确保锚点沿真实几何结构生长：

**步骤 1：补丁误差计算**。将渲染图像划分为补丁 $\mathcal{P}$，计算每个补丁的平均损失：

$$\ell_{\mathcal{P}} = \frac{1}{|\Omega_{\mathcal{P}}|} \sum_{(u,v)\in\Omega_{\mathcal{P}}} \ell(u,v)$$

其中 $\Omega_{\mathcal{P}}$ 为补丁像素集合，$\ell(u,v)$ 为逐像素损失（L1 与 SSIM 的组合）。

**步骤 2：高误差补丁选择**。计算全局平均损失 $\bar{\ell}$，选择损失超过阈值（$3\bar{\ell}$）的补丁作为致密化候选区域：

$$\bar{\ell} = \frac{1}{|S|} \sum_{\mathcal{P}\in S} \ell_{\mathcal{P}}, \quad \text{选择 } \ell_{\mathcal{P}} > 3\bar{\ell}$$

**步骤 3：代理引导反向投影**。利用相机内外参和代理深度，将选中补丁的中心像素 $(u_{\mathcal{P}}, v_{\mathcal{P}})$ 反向投影到 3D 空间，作为新锚点位置：

$$\hat{\mathbf{p}}_{\mathcal{P}} = \mathbf{o} + \mathbf{R}^\top \left( d_{\mathrm{mesh}}(u_{\mathcal{P}}, v_{\mathcal{P}}) \mathbf{K}^{-1} [u_{\mathcal{P}}, v_{\mathcal{P}}, 1]^\top \right)$$

其中 $\mathbf{o}$ 为相机光心，$\mathbf{R}$ 为旋转矩阵，$\mathbf{K}$ 为内参矩阵。该操作确保新锚点位于代理网格表面，而非悬浮于空间中。

**步骤 4：密度网格控制**。为防止锚点过度密集，将空间划分为网格单元，每个单元最多容纳 $K$ 个锚点：

$$\mathbf{c}(\mathbf{a}) = \left\lfloor \frac{\mathbf{a} - \mathbf{b}_{\min}}{h} \right\rfloor \in \mathbb{Z}^3, \quad \text{若 } \kappa[\mathbf{c}(\mathbf{a})] < K \text{ 则插入 } \mathbf{a}$$

其中 $\mathbf{b}_{\min}$ 为网格原点，$h$ 为单元尺寸，$\kappa[\cdot]$ 为当前单元锚点计数。

### 关键设计决策的因果链路

消融实验（Table 3）揭示了各模块之间的因果依赖关系：

- **仅推理时使用遮挡剔除（ID 2）**：FPS 提升超过 3×（从 48 到 151），但 PSNR 从 21.41 骤降至 19.06。原因在于训练时未考虑遮挡，锚点与高斯的一致性被破坏。
- **训练与推理均启用遮挡剔除（ID 3）**：PSNR 恢复至 21.50，超过基线，验证了训练-推理一致性的必要性。
- **加入代理引导致密化（ID 4）**：PSNR 进一步提升至 21.68，同时保持高 FPS（143），证明表面引导的锚点生长对质量有独立贡献。

这一因果链路表明：**遮挡剔除负责加速，训练-推理一致性保证质量不退化，表面致密化提供额外质量增益**。三者缺一不可。

## 实验与关键发现

### 核心瓶颈与因果机制

现有基于MLP的3D高斯泼溅方法（如Octree-GS、Scaffold-GS）在训练和推理过程中缺乏有效的遮挡感知，导致大量锚点和高斯原语位于被遮挡区域，产生无效的解码与渲染计算。这一冗余在遮挡严重的大规模城市街道（如MatrixCity Streets）和室内多房间场景中尤为突出，成为限制渲染速度的关键瓶颈。

Proxy-GS的核心因果杠杆在于：引入轻量级代理网格（proxy mesh）并利用硬件光栅化以极低延迟（<1 ms）生成精确的遮挡深度图，将其作为统一训练和推理阶段的遮挡剔除与锚点致密化的先验。通过保持训练与推理的遮挡先验一致性，该方法既消除了被遮挡区域的计算浪费，又促进了锚点沿真实几何结构生长，从而在显著提升渲染速度的同时改善或保持了渲染质量。

### 主实验结果

#### MatrixCity合成数据集

Table 1展示了Proxy-GS与基线方法在MatrixCity各区块上的定量对比。在遮挡最为严重的Block 5上，Proxy-GS取得了**PSNR 21.68**，相比基础框架Octree-GS（21.41）提升0.27 dB，同时FPS从48飙升至**151**，实现约**3.1×加速**。在Block 1&2和Block 3&4上，Proxy-GS同样在保持或提升渲染质量的前提下，将FPS从约50提升至126-131。值得注意的是，显式高斯方法3DGS虽在部分场景取得最高PSNR，但其FPS仅为30-31，远低于Proxy-GS。

#### 真实场景数据集

Table 2展示了在真实室外与室内数据集上的结果。在遮挡严重的**Small City**数据集上，Proxy-GS以**PSNR 23.09**（Octree-GS为23.03）和**FPS 139**（Octree-GS为51）实现了**约2.73×加速**。在遮挡相对较弱的Berlin数据集上，FPS从263提升至275，增幅有限（+12），这验证了该方法在遮挡丰富场景中的增益更为显著。在室内多房间数据集CUHK-LOWER上，Proxy-GS同样保持了竞争力的渲染质量与速度。

#### 推理时间占用分析

Figure 3对比了Proxy-GS与Octree-GS各推理组件的时间占比。Proxy-GS的深度渲染仅占极低比例（约1 ms），而锚点过滤模块由于融合了视锥剔除与遮挡剔除，其开销远低于Octree-GS的LOD选择策略。整体上，Proxy-GS将更多GPU时间集中于实际的高斯光栅化渲染，而非无效锚点的解码与处理。

### 消融实验

#### 训练与推理策略消融

Table 3在Block 5上系统消融了不同训练与推理策略的效果：

- **ID 1（Octree-GS基线）**：PSNR 21.41，FPS 48，平均解码锚点数最高。
- **ID 2（仅推理时使用代理遮挡剔除）**：FPS大幅提升至超过3×，但PSNR骤降至**19.06**。原因在于训练过程中未考虑遮挡先验，锚点与高斯的分布与推理时的可见性要求不一致，导致大量有效锚点被误剔除。
- **ID 3（训练与推理均启用代理遮挡剔除）**：PSNR恢复至**21.50**，已超越基线，FPS保持高水平。这验证了训练-推理一致性对渲染质量的关键作用。
- **ID 4（完整Proxy-GS，加入代理引导致密化）**：PSNR进一步提升至**21.68**，FPS为143，平均解码锚点数进一步降低。代理引导致密化使新锚点沿代理网格表面生成，有效增强了场景几何的表达能力。

这一消融清晰地揭示了核心洞察：**仅推理时使用遮挡剔除会破坏锚点分布一致性，必须在训练阶段同步引入代理先验，并结合表面引导的致密化，才能实现质量与速度的最优权衡。**

#### 代理保真度鲁棒性

Figure 7展示了代理网格分辨率与顶点噪声对PSNR的影响：
- 降低代理网格分辨率对渲染质量影响极小，因为城市场景以近平面结构为主，粗糙代理仍能保持可见性结构。
- 引入顶点噪声会破坏遮挡边界，导致PSNR明显下降，表明精确的遮挡边缘比几何细节更为关键。

#### 安全裕度γ消融

Table 10在Small City数据集上分析了安全裕度γ的影响。γ=0.3取得最佳渲染质量与FPS的折衷。γ过小（如0.1）会产生近处穿透伪影，γ过大（如0.5）则引入过多冗余锚点，降低剔除效率。

#### 与不同3DGS渲染器结合

Table 4展示了Proxy-GS与不同3DGS渲染加速方案的兼容性。与硬件3DGS渲染器结合后，FPS可从126进一步提升至**167**（+41），但PSNR轻微下降约0.06 dB，体现了速度与精度的经典权衡。

### 失败模式与局限性

1. **低遮挡场景增益有限**：在Berlin等遮挡较弱的场景中，FPS提升仅约4.6%，代理深度渲染的额外开销几乎抵消了剔除收益。
2. **代理网格构建依赖**：代理网格的构建依赖于密集点云或预训练模型（如MapAnything、CityGS-X），在极度稀疏或无纹理场景中可能引入几何误差，需要手动验证。
3. **安全裕度需人工调整**：γ是场景相关的超参数，缺乏完全自适应的机制。
4. **透明与薄结构挑战**：当前的代理引导致密化基于补丁误差和代理深度，可能无法有效处理完全透明的表面或极薄的几何结构。

### 公平性说明

所有对比方法均训练40,000次迭代。为公平对比，3DGS和Hierarchical-GS的致密化阈值统一降至$10^{-4}$以提升其渲染质量至接近Octree-GS的水平；Scaffold-GS使用更小的体素尺寸（$10^{-4}$）和更低的致密化阈值（$10^{-4}$）以增强表达力。Octree-GS的默认LOD策略和初始化在Proxy-GS中保持不变。

![[assets/figures/papers/paper_list_l2038_https_arxiv_org_abs_2509_24421/figures/007_Table_3.jpg]]
*Table 3: Ablations of different training and inference strategies on Block 5. Average anchor denotes the average number of decoded anchors in the scene*

![[assets/figures/papers/paper_list_l2038_https_arxiv_org_abs_2509_24421/figures/020_Table_10.jpg]]
*Table 10: Ablations of different safety margin of depth culling γ trained on Small City [16]*

![[assets/figures/papers/paper_list_l2038_https_arxiv_org_abs_2509_24421/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on MatrixCity [21]. We report average results over Block 1&2, Block 3&4, and Block 5. (Block 1&2 and 3&4 represent the average evaluation metrics of their respective two blocks.) The best and second-best are highlighted*

![[assets/figures/papers/paper_list_l2038_https_arxiv_org_abs_2509_24421/figures/009_Figure_5.jpg]]
*Figure 5: Quantitative mesh visualization on different Resolutions and Vertex noise on Block 5*

## 定位与知识库关联

### 所属技术脉络

Proxy-GS 属于 **MLP-based 结构化 3D 高斯泼溅 (3DGS)** 这一细分方向。该方向的核心思路是使用稀疏锚点（anchor）配合 MLP 解码器来生成高斯原语，从而在保持显式渲染管线优势的同时，引入隐式表示的表达力和压缩能力。Proxy-GS 直接建立在 **Octree-GS** 的基础框架之上，沿用了其默认的 LOD 策略和初始化方式，但在遮挡感知这一关键维度上进行了系统性增强。

与显式 3DGS 基线（**3DGS**）和基于 LOD 的显式高斯合并方法（**Hierarchical-GS**）不同，Proxy-GS 保留了 MLP 解码器的结构化优势。与另一 MLP-based 方法 **Scaffold-GS**（使用体素锚点）相比，Proxy-GS 继承了 Octree-GS 的八叉树层级结构，并在其上叠加了统一的遮挡先验。

### 与基线方法的关键差异

| 维度 | 3DGS / Hierarchical-GS | Scaffold-GS | Octree-GS | **Proxy-GS** |
|------|----------------------|-------------|-----------|-------------|
| 锚点结构 | 无锚点（直接优化高斯） | 体素锚点 | 八叉树 LOD 锚点 | 八叉树 LOD 锚点 |
| 遮挡建模 | 无显式遮挡机制 | 无显式遮挡机制 | 无显式遮挡机制 | 代理网格深度图 + 逐像素遮挡剔除 |
| 致密化策略 | 基于梯度的致密化 | 基于梯度的致密化 | 基于梯度的致密化 | 代理引导的表面致密化 + 密度网格控制 |
| 训练-推理一致性 | 一致 | 一致 | 可能不一致（推理时使用 LOD） | 训练和推理使用相同的遮挡剔除和致密化策略 |
| 深度图获取 | 不使用 | 不使用 | 不使用 | 硬件光栅化代理网格（<1 ms） |

核心差异可归纳为两个“统一”：（1）将遮挡剔除从无到有地引入，并与视锥剔除融合在单个 CUDA 内核中执行；（2）将训练和推理阶段的遮挡处理统一起来，消除了传统方法中训练时无遮挡感知、推理时突然引入剔除所导致的锚点-高斯不一致问题。

### 适用边界

**强适用场景：**
- 遮挡严重的大规模城市场景（如 MatrixCity Streets、Small City），此时 Proxy-GS 的加速效果最为显著，可达 2.5–3 倍 FPS 提升。
- 室内多房间场景，遮挡边界清晰，代理网格易于构建。
- 对渲染速度有严格要求的实时应用，代理深度渲染仅需约 1 ms 的额外开销。

**弱适用场景：**
- 几乎无遮挡的开阔场景（如 Berlin 数据集），FPS 提升有限（仅从 263 到 275），代理剔除的边际收益较小。
- 极度稀疏或无纹理场景，代理网格的构建依赖密集点云或预训练模型（如 MapAnything、CityGS-X），可能引入额外预处理复杂度和几何误差。

### 局限性与开放问题

**已知局限：**

1. **代理网格构建依赖外部输入**：代理网格的生成需要密集点云或预训练模型，在稀疏点云场景中可能引入几何误差。论文中代理网格的构建方法因场景类型而异（室外/室内，密集/稀疏点云），缺乏统一的自动化方案。

2. **安全裕度 γ 需人工设定**：遮挡剔除的深度测试中，安全裕度 γ 的最佳取值（论文中为 0.3）需要根据场景遮挡程度和代理精度手动调整——γ 过小会产生近处穿透伪影，γ 过大则引入过多冗余锚点。目前缺乏完全自适应的机制。

3. **对透明/极薄结构不敏感**：当前的代理引导致密化基于补丁误差和代理深度，可能无法处理完全透明的表面或极薄的几何结构（如玻璃幕墙、栅栏），这些区域的代理深度可能不准确。

4. **无遮挡场景加速有限**：深度获取和遮挡剔除虽然极快，但在几乎无遮挡的简单场景下，FPS 提升有限，额外的 GPU 工作成为纯开销。

**开放问题：**

- **动态场景推广**：代理先验能否推广到动态场景或可变形物体（如包含运动的街道或人物）？这需要代理网格的实时更新或变形能力。
- **端到端优化**：能否将代理网格的构建和更新整合到在线训练循环中，实现代理几何与高斯表示的联合优化？
- **移动端部署**：在移动设备或算力更弱的消费级 GPU 上，代理渲染和 Hi-Z 剔除的额外开销是否仍可忽略？当前验证仅在桌面级 GPU 上进行。
- **与高效解码器结合**：该方法是否可以与更高效的 MLP 解码器（如量化或剪枝）结合，进一步降低推理成本？表 4 显示 Proxy-GS 与硬件 3DGS 渲染器结合可进一步提升 FPS，暗示了与其他加速技术的兼容性。

### 知识库定位

在 3D 高斯泼溅的知识体系中，Proxy-GS 填补了“遮挡感知的结构化 3DGS”这一空白。其核心贡献不在于提出新的表示形式或解码器架构，而在于引入了一个**轻量级、统一的几何先验注入机制**——代理网格深度图——使得遮挡剔除和表面引导致密化可以在训练和推理中一致地执行。这一思路与神经渲染中“显式几何引导隐式表示”的趋势一致，但通过硬件光栅化实现了极低延迟的深度获取，使其在实时应用中具有实际可行性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Proxy_GS_Unified_Occlusion_Priors_for_Training_and_Inference_in_Structured_3D_Gaussian_Splatting.pdf]]

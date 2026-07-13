---
title: "DiffPBR: Point-Based Rendering via Spatial-Aware Residual Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DiffPBR_Point_Based_Rendering_via_Spatial_Aware_Residual_Diffusion_9d4873f74381.pdf
project_link: null
code_link: null
aliases:
- DiffPBR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 视角投影的结构化噪声图（CoNo-Splatting）作为扩散模型的几何一致性引导，同时残差学习使模型仅预测渲染残差，从而将点云几何先验注入生成过程。
primary_logic: 将点云渲染为携带3D几何线索的彩色图像和噪声图，利用残差扩散模型只修复缺失细节，并用同一3D点云保证多视图噪声的一致性，从而实现高效、可泛化且视图一致的照片级渲染。
claims:
- 用 CoNo-Splatting 替代 i.i.d. 高斯噪声，将几何与遮挡信息嵌入扩散过程。
- 残差扩散只预测渲染图像与真值的残差，显著减少扩散步数和训练时间。
- 自适应点云栅格化全局调节点尺度，平衡保真度与空洞填补，提升后续扩散的有效性。
- ScanNet 上 PSNR / SSIM / LPIPS = 23.28 / 0.827 / 0.399 (DiffPBR-Q)
---

# DiffPBR: Point-Based Rendering via Spatial-Aware Residual Diffusion

> [!tip] 核心洞察
> 将点云渲染为携带3D几何线索的彩色图像和噪声图，利用残差扩散模型只修复缺失细节，并用同一3D点云保证多视图噪声的一致性，从而实现高效、可泛化且视图一致的照片级渲染。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffPBR: 基于空间感知残差扩散的点云渲染 |
| 英文题名 | DiffPBR: Point-Based Rendering via Spatial-Aware Residual Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tqOBZbW6j8) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DiffPBR |
| Dataset | ScanNet, DTU, THuman2.0 |

> [!tip] 效果简介
> - ScanNet 上，PSNR / SSIM / LPIPS 23.28 / 0.827 / 0.399 (DiffPBR-Q) vs 19.86 / 0.758 / 0.452 (PFGS) (+3.42 / +0.069 / -0.053)。
> - DTU 上，PSNR / SSIM / LPIPS 28.45 / 0.935 / 0.124 (DiffPBR-Q) vs 25.44 / 0.901 / 0.164 (PFGS) (+3.01 / +0.034 / -0.040)。
> - THuman2.0 上，PSNR / SSIM / LPIPS 41.27 / 0.989 / 0.003 (DiffPBR-Q) vs 35.88 / 0.985 / 0.006 (PFGS†) (+5.39 / +0.004 / -0.003)。

## 概要

点云是三维视觉中最基础的表示形式，但将离散点云渲染为照片级真实感图像仍面临根本性瓶颈：栅格化过程不可避免地产生空洞、锯齿和视图间不一致，而直接使用标准扩散模型从纯噪声恢复完整图像不仅效率低下，还会引入多视图不一致。DiffPBR 针对这一瓶颈提出了两个关键机制。

**核心思路**：将点云几何先验注入扩散生成过程。具体而言，DiffPBR 通过自适应 CoNo-Splatting 将点云渲染为携带三维几何线索的彩色图像和结构化噪声图，然后利用残差扩散模型仅预测渲染结果与真实图像之间的残差，而非重建完整图像。这一设计使得模型在保持多视图一致性的同时，大幅降低了扩散模型的训练和推理成本。

**方法定位**：DiffPBR 属于可泛化的神经点云渲染方法，无需逐场景优化。其核心贡献在于用视角一致的、几何感知的噪声图替代传统扩散模型中的独立同分布高斯噪声，并将学习目标从完整图像重建转变为残差预测，从而将点云几何先验与扩散模型的生成能力深度融合。

**主要结果**：在 ScanNet、DTU 和 THuman2.0 三个基准数据集上，DiffPBR 相比现有方法在 PSNR 指标上提升 3∼5 dB，同时将训练时间从 41 GPU 小时缩减至约 8 GPU 小时，推理速度提升约 2.8 倍。

### 点云渲染的核心瓶颈

点云作为一种轻量、灵活的3D表示，在计算机视觉与图形学中被广泛用于场景重建与视图合成。然而，将离散点云转换为照片级真实感图像面临一个根本性矛盾：**稀疏采样点无法提供连续表面的完备覆盖**。当点云通过栅格化投影到像面时，点与点之间的间隙会产生空洞，而离散采样带来的混叠效应则表现为锯齿状伪影。更棘手的是，这些空洞和伪影会随视角变化而漂移，导致**多视图渲染结果不一致**——同一3D区域在不同视角下呈现不同的纹理细节，破坏了视觉连贯性。

现有方法对这一瓶颈的处理可分为两条路线。传统图形学栅格化方法（如 **Pytorch3D**，Ravi et al., 2020）依赖固定点尺度或启发式空洞填充，难以在保真度与覆盖率之间取得平衡：点尺度过小则空洞密集，过大则模糊细节。神经点渲染方法（如 **NPBG**，Aliev et al., 2020；**NPBG++**，Rakhimov et al., 2022）通过可学习的神经描述符增强点特征，但仍受限于栅格化的离散本质，高频纹理恢复能力有限。**PFGS**（Wang et al., 2024a）引入3D高斯泼溅改善了渲染质量，但其逐场景优化范式导致训练耗时（约41 GPU小时）且泛化能力受限。

### 扩散模型的机遇与挑战

扩散模型在图像生成领域展现了强大的高频细节合成能力，自然成为提升点云渲染质量的候选方案。然而，直接将标准扩散模型应用于点云渲染面临两个关键障碍：

1. **几何先验缺失**：标准扩散过程从独立同分布（i.i.d.）高斯噪声出发重建完整图像，完全忽略了点云携带的3D几何与遮挡信息。模型需要同时推断场景结构和纹理细节，导致训练低效且难以保证多视图一致性。
2. **全图重建冗余**：点云栅格化图像已经提供了低频几何和颜色信息，要求扩散模型从纯噪声重建整张图像是对已知信息的浪费，增加了不必要的训练负担和推理步数。

### 本文动机

针对上述瓶颈，DiffPBR 提出了一条紧凑的解决路径：**将点云几何先验注入扩散过程，使模型专注于修复渲染残差而非重建整幅图像**。核心洞察在于——点云栅格化产生的空洞和锯齿并非随机噪声，而是携带3D结构线索的**结构化缺失**。如果能将这种结构化信息编码为扩散模型的引导信号，同时让模型只预测栅格化图像与真实照片之间的残差，就能在保持多视图几何一致性的前提下，高效合成照片级细节。

这一动机直接催生了 DiffPBR 的两个关键设计：用视角一致的几何噪声图替换 i.i.d. 高斯噪声的 **CoNo-Splatting**，以及使模型仅学习渲染残差的**残差扩散范式**。两者协同，将点云从“待修复的残缺表示”转变为“扩散过程的几何锚点”，实现了训练效率（约8 GPU小时）与渲染质量（PSNR提升3∼5 dB）的双重突破。

## 核心方法与创新机理

DiffPBR 的核心创新围绕一个根本矛盾展开：**离散点云在栅格化过程中不可避免地产生空洞、锯齿和视图间不一致，而直接使用标准扩散模型恢复完整图像不仅效率低下，还会引入多视图不一致**。针对这一瓶颈，DiffPBR 通过三个相互耦合的 changed slots 将点云几何先验系统性地注入扩散生成过程，实现了高效、可泛化且视图一致的照片级渲染。

### 从 i.i.d. 噪声到 3D 一致的几何噪声先验

标准扩散模型以 i.i.d. 高斯噪声作为起点，完全忽略了场景的 3D 结构。DiffPBR 的关键突破在于将这一无结构噪声替换为**经由 CoNo-Splatting 渲染的 3D 一致噪声图 $I_\epsilon$**（Figure 1）。具体而言，CoNo-Splatting 将每个点云的 6 通道特征（3 通道颜色 + 3 通道噪声）通过可微泼溅投影到像面：

$$F(p) = \frac{ \sum_{i=1}^n \kappa\Big( (p - \pi(\mathbf{K}^v, \mathbf{M}^v, \mathbf{x}_i)) / s_i \Big) v(z_i) \mathbf{f}_i }{ \sum_{j=1}^n \kappa\Big( (p - \pi(\mathbf{K}^v, \mathbf{M}^v, \mathbf{x}_j)) / s_j \Big) v(z_j) + \delta }$$

这一公式的核心机制在于：像素接收到的噪声贡献强度与对应 3D 点到相机的距离和遮挡关系直接相关——距离相机更近的点贡献更强，被遮挡或远处的点贡献更弱。因此，同一 3D 点云在不同视角下渲染出的噪声图天然保持了几何一致性，从根本上解决了多视图不一致的问题。消融实验（Table 7）证实，移除这一 3D 一致噪声将导致 PSNR 显著下降和收敛步数增加。

### 从完整图像重建到残差扩散

传统扩散模型需要从纯噪声逐步重建完整图像，这既低效又容易在点云已提供大量低频结构信息的情况下产生冗余计算。DiffPBR 将学习目标从“重建完整图像”转变为**预测渲染残差与噪声的加权组合**（残差扩散）：

$$\mathcal{L}_{\mathrm{rdm}} = \mathbb{E}_{I_0, I_\epsilon, t} \left[ \| res\epsilon - \mathcal{F}_\theta(\hat{I}_t, I_c, I_m, t) \|_2 \right]$$

这里的因果机制是：CoNo-Splatting 已经输出了携带完整几何和低频颜色信息的彩色图像 $I_c$，扩散模型只需专注于恢复 $I_c$ 与真值 $I_0$ 之间的高频细节差异（即残差）。这一设计将扩散模型的负担从“生成一切”缩减为“精炼细节”，直接带来了约 5 倍的训练时间缩减（从 41 GPU 小时降至约 8 GPU 小时，Table 2）和约 2.8 倍的推理速度提升（从 3.6 FPS 提升至 10 FPS，Table 2）。消融实验（Table 7）进一步表明，残差扩散范式在收敛步数和最终 PSNR 上均优于纯 DDPM 变体。

### 自适应点栅格化：平衡保真度与空洞填补

上述两个 changed slots 的有效性高度依赖 CoNo-Splatting 输出的彩色图像质量——如果栅格化图像空洞过多或过度模糊，扩散模型将难以有效精炼。DiffPBR 通过**基于 KNN 距离的自适应点尺度策略**解决这一问题：

$$s_i = \mathrm{clamp\_max}\big( \bar{s}_i, \beta \cdot \mathrm{median}\big( \{\bar{s}_j\}_{j=1}^N \big) \big)$$

其中 $\bar{s}_i$ 是点 $i$ 到其 $k$ 个最近邻的平均距离，$\beta$ 是可学习的全局截断因子。这一设计的精巧之处在于：局部尺度 $\bar{s}_i$ 保证了点云密集区域的保真度（小尺度避免模糊），而全局中位数截断则强制稀疏区域的点尺度扩大以填补空洞。覆盖损失 $\mathcal{L}_{\mathrm{cov}}$ 和紧凑性损失 $\mathcal{L}_{\mathrm{cmp}}$ 的对抗作用（Figure 2）进一步驱动 $\beta$ 在训练中自适应调整（Figure 3），在覆盖率和锐度之间找到最优平衡。消融实验（Table 5）证实，这一自适应策略在扩散精炼后获得的 PSNR 显著优于固定尺度或 CNN 预测尺度的方案。值得注意的是，该自适应泼溅模块具有即插即用特性——将其直接应用于 PFGS 即可显著提升渲染质量（Table 13, Figure 11）。

### 创新耦合的内在逻辑

三个 changed slots 并非孤立改进，而是形成了因果闭环：自适应栅格化为扩散模型提供高质量的初始彩色图像和掩膜；3D 一致噪声图将几何先验嵌入扩散过程，保证多视图一致性；残差学习范式则利用这一强先验大幅降低扩散模型的训练和推理成本。这种“几何引导生成、生成补偿几何”的设计范式，是 DiffPBR 在三个基准数据集上均以 3～5 dB PSNR 优势超越现有方法（Table 1）的根本原因。

DiffPBR 提出了一种**两阶段、端到端可微**的点云渲染管线，将自适应栅格化与残差扩散模型有机结合。其核心设计思路是：不直接从离散点云重建完整图像，而是先生成一个携带 3D 几何线索的“粗糙”渲染，再通过扩散模型仅修复缺失的细节，从而在效率、质量和多视图一致性之间取得平衡。

### 输入输出流

管线的输入为：

- **带颜色的点云** $\mathcal{P}_{in} = \{(\mathbf{x}_i, \mathbf{c}_i)\}_{i=1}^N$，其中 $\mathbf{x}_i \in \mathbb{R}^3$ 为空间坐标，$\mathbf{c}_i \in \mathbb{R}^3$ 为 RGB 颜色；
- **已标定的相机参数**，包括内参矩阵 $\mathbf{K}^v$ 和外参矩阵 $\mathbf{M}^v$，用于指定目标视角。

管线的最终输出为与该视角对应的**照片级真实感渲染图像**。

### 两阶段模块关系

如 Figure 1 所示，DiffPBR 由两个串行且联合训练的模块组成：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tqOBZbW6j8/figures/001_Figure_1.jpg]]
*Figure 1: Framework Overview. Given a colored point cloud and calibrated cameras, DiffPBR synthesizes photo-realistic renderings via Adaptive CoNo-Splatting (Sec. 3.1) for view-consistent initialization, and a Spatial-aware Residual Diffusion stage (Sec. 3.2) for refinement*

#### 第一阶段：自适应 CoNo-Splatting（Adaptive CoNo-Splatting）

该模块负责将点云投影到像面，生成三个关键中间产物：

1. **彩色渲染图** $I_c^v$：通过可微泼溅（differentiable splatting）将点云颜色投影到图像平面，形成携带场景几何结构的粗糙渲染；
2. **3D 一致噪声图** $I_\epsilon^v$：每个点额外携带一个 3 通道可学习噪声属性，同样通过泼溅投影，生成与视角对齐的几何感知噪声图——这是替代传统扩散模型中 i.i.d. 高斯噪声的关键设计；
3. **软掩膜** $I_m^v$：指示像素是否被有效泼溅覆盖，用于后续扩散模型区分“空洞”与“有效区域”。

这一阶段的**核心创新**在于**自适应点尺度机制**：每个点的泼溅半径 $s_i$ 由其 $k$-近邻平均距离初始化，再通过可学习的全局参数 $\beta$ 按中位数截断：

$$s_i = \mathrm{clamp\_max}\big( \bar{s}_i, \beta \cdot \mathrm{median}\big( \{\bar{s}_j\}_{j=1}^N \big) \big)$$

这一设计平衡了“保真度”（小尺度保持细节）与“空洞填补”（大尺度减少间隙），为后续扩散精炼提供高质量的初始化。

#### 第二阶段：空间感知残差扩散（Spatial-aware Residual Diffusion）

该模块以第一阶段的输出为条件，对粗糙渲染进行精炼。其核心设计包含两个关键决策：

- **残差学习范式**：模型不预测完整图像，而是预测渲染图 $I_c^v$ 与真实图像 $I_0$ 之间的**残差**与噪声的加权组合。这使模型只需关注缺失的高频细节，显著降低学习难度，减少扩散步数和训练时间。
- **3D 一致噪声注入**：用第一阶段生成的 $I_\epsilon^v$ 替代传统 i.i.d. 高斯噪声。由于同一 3D 点云在不同视角下泼溅出的噪声图天然保持几何一致性，扩散模型在去噪过程中隐式地受到 3D 结构约束，从而保证多视图渲染的一致性。

扩散模型以彩色渲染图 $I_c^v$ 和软掩膜 $I_m^v$ 为条件输入，通过预测残差噪声 $res\epsilon$ 来驱动去噪过程，损失函数为：

$$\mathcal{L}_{\mathrm{rdm}} = \mathbb{E}_{I_0, I_\epsilon, t} \left[ \| res\epsilon - \mathcal{F}_\theta(\hat{I}_t, I_c, I_m, t) \|_2 \right]$$

### 端到端训练

两个阶段并非分步预训练，而是**端到端联合优化**。第一阶段通过覆盖损失 $\mathcal{L}_{\mathrm{cov}}$ 和紧凑性损失 $\mathcal{L}_{\mathrm{cmp}}$ 的对抗平衡来学习自适应点尺度；第二阶段的反传梯度同时流向扩散模型和泼溅模块，使点云的颜色与噪声属性能够针对最终渲染质量进行优化。消融实验（Table 6, Table 7）证实，这种联合训练策略对收敛稳定性和最终 PSNR 至关重要。

DiffPBR 由两个紧密耦合的核心模块构成：**自适应 CoNo-Splatting**（Adaptive CoNo-Splatting）和**空间感知残差扩散模块**（Spatial-aware Residual Diffusion）。前者负责将离散点云转化为携带几何一致性线索的彩色图像、噪声图和软掩膜；后者以这些中间表示为条件，通过残差扩散范式仅预测渲染残差，从而高效恢复高频细节并保持多视图一致。

### 自适应 CoNo-Splatting

该模块的核心挑战在于：点云投影到像面后会产生空洞和锯齿，而点尺度过大则导致模糊。DiffPBR 采用基于 K-近邻的自适应尺度策略与覆盖-紧凑对抗损失来平衡保真度与空洞填补。

**自适应点尺度。** 每个点的初始尺度 $\bar{s}_i$ 由其到 $k$ 个最近邻点的平均距离确定，随后通过全局可学习参数 $\beta$ 与所有点尺度的中位数进行截断：

$$s_i = \mathrm{clamp\_max}\big( \bar{s}_i, \beta \cdot \mathrm{median}\big( \{\bar{s}_j\}_{j=1}^N \big) \big)$$

其中 $\bar{s}_i = \frac{1}{k}\sum_{j \in \mathcal{N}_k(i)} \|\mathbf{x}_i - \mathbf{x}_j\|_2$，$\mathrm{clamp\_max}$ 将尺度上界限制在 $\beta \cdot \mathrm{median}(\{\bar{s}_j\})$。这一设计的因果机制在于：局部 KNN 距离反映点云密度变化，而全局中位数截断防止稀疏区域尺度爆炸，$\beta$ 作为可学习参数在训练中自适应调节截断强度。

**CoNo-Splatting 特征渲染。** 给定相机内参 $\mathbf{K}^v$ 和外参 $\mathbf{M}^v$，每个点 $\mathbf{x}_i$ 携带 6 通道特征 $\mathbf{f}_i = [\mathbf{c}_i; \mathbf{n}_i]$（前 3 通道为颜色，后 3 通道为可学习噪声属性），通过可微泼溅渲染为特征图：

$$F(p) = \frac{ \sum_{i=1}^n \kappa\Big( (p - \pi(\mathbf{K}^v, \mathbf{M}^v, \mathbf{x}_i)) / s_i \Big) v(z_i) \mathbf{f}_i }{ \sum_{j=1}^n \kappa\Big( (p - \pi(\mathbf{K}^v, \mathbf{M}^v, \mathbf{x}_j)) / s_j \Big) v(z_j) + \delta }$$

其中 $\pi(\cdot)$ 为透视投影函数，$\kappa(\cdot)$ 为径向基核函数，$v(z_i)$ 为基于深度的可见性权重（距离相机越近权重越大），$\delta$ 为防止除零的小常数。随后从特征图中分离出彩色图像和噪声图：

$$I_{c}^{v}(p) = [F(p)]_{1:3}, \quad I_{\epsilon}^{v}(p) = [F(p)]_{4:6}$$

噪声图 $I_\epsilon$ 的关键作用在于**替代传统扩散模型中的 i.i.d. 高斯噪声**：由于噪声属性 $\mathbf{n}_i$ 绑定在 3D 点上，不同视角渲染出的噪声图天然具有几何一致性——像素从距离相机更近的点接收更强的噪声贡献，而远距离或被遮挡的点贡献较弱。这隐式地将遮挡关系和深度信息嵌入扩散过程。

**覆盖损失与紧凑损失。** 为引导自适应尺度学习，引入一对对抗性损失。覆盖损失 $\mathcal{L}_{\mathrm{cov}}$ 促使点尺度扩大以增加有效像素覆盖：

$$\mathcal{L}_{\mathrm{cov}} = \mathbb{E}_{(i,j)\sim p}\left[\left|\left| I_c(i,j) - I_0(i,j) \right|\right|_{1}\right]$$

紧凑性损失 $\mathcal{L}_{\mathrm{cmp}}$ 抑制掩膜过度扩散以避免模糊：

$$\mathcal{L}_{\mathrm{cmp}} = \mathbb{E}_{(i,j)\sim p}\big[-\log\left(p(i,j) + \delta\right)\big]$$

其中 $p(i,j)$ 为泼溅产生的软掩膜 $I_m$ 在像素 $(i,j)$ 处的值。两者的对抗平衡是实现稳定收敛和高质量渲染的关键（消融实验 Table 6 证实）。

### 空间感知残差扩散模块

传统扩散模型从纯噪声重建完整图像，效率低且易引入多视图不一致。DiffPBR 采用**残差扩散范式**：模型仅需预测渲染图像 $I_c$ 与真值 $I_0$ 之间的残差，而非完整图像。

**前向过程。** 定义残差 $res = I_0 - I_c$，在时间步 $t$ 构造带噪残差：

$$\hat{I}_t = I_c + \sqrt{\bar{\alpha}_t} \cdot res + \sqrt{1 - \bar{\alpha}_t} \cdot I_\epsilon$$

其中 $I_\epsilon$ 为 CoNo-Splatting 渲染的 3D 一致噪声图，$\bar{\alpha}_t$ 为噪声调度参数。与标准 DDPM 的关键区别在于：噪声项 $I_\epsilon$ 替代了 i.i.d. 高斯噪声，且信号项以 $I_c$ 为基座而非从零开始。

**训练目标。** 模型 $\mathcal{F}_\theta$ 以带噪残差 $\hat{I}_t$、彩色图像 $I_c$、软掩膜 $I_m$ 和时间步 $t$ 为条件，预测残差噪声 $res\epsilon$：

$$\mathcal{L}_{\mathrm{rdm}} = \mathbb{E}_{I_0, I_\epsilon, t} \left[ \| res\epsilon - \mathcal{F}_\theta(\hat{I}_t, I_c, I_m, t) \|_2 \right]$$

其中 $res\epsilon = \sqrt{\bar{\alpha}_t} \cdot res + \sqrt{1 - \bar{\alpha}_t} \cdot I_\epsilon$ 为真值残差噪声。该设计的因果机制在于：$I_c$ 已提供低频结构和几何布局，模型只需聚焦高频细节恢复；$I_m$ 指示有效像素区域，使模型避免在空洞区域产生伪影；$I_\epsilon$ 的 3D 一致性确保多视图精炼结果相互协调。

**推理过程。** 从 $\hat{I}_T = I_c + I_\epsilon$ 开始，通过多步去噪逐步恢复 $I_0$。消融实验（Table 7）表明，残差扩散 + 3D 一致噪声在收敛步数和 PSNR 上均优于纯 DDPM 或去除 3D 噪声的变体；$\epsilon$-预测的 multi-step 采样在所有训练规模下取得最高 PSNR（Table 9）。

## 实验与关键发现

### 主要定量结果

DiffPBR 在三个覆盖室内场景、物体和人体重建的基准数据集上系统性地超越了所有对比方法。Table 1 汇总了核心指标：在最具挑战性的 **ScanNet** 数据集上，DiffPBR-Q 以 23.28 PSNR / 0.827 SSIM / 0.399 LPIPS 领先最强基线 PFGS（19.86 / 0.758 / 0.452），PSNR 提升达 **+3.42 dB**；在 **DTU** 上取得 28.45 PSNR（+3.01 dB vs. PFGS）；在 **THuman2.0** 上达到 41.27 PSNR（+5.39 dB vs. PFGS†），LPIPS 降至 0.003，几乎与真值不可区分。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tqOBZbW6j8/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation of state-of-the-art point-based rendering methods on three benchmark datasets. † indicates our reproduction results of the method*

这一性能优势的因果链条清晰：自适应 CoNo-Splatting 生成的彩色图像 $I_c$ 保留了完整的几何结构，而 3D 一致的噪声图 $I_\epsilon$ 将遮挡关系和深度信息隐式编码进扩散过程——远处或被遮挡的点贡献更弱的噪声信号。残差扩散模型仅需预测渲染残差与噪声的加权组合，而非从纯噪声重建整张图像，这使扩散步数大幅减少，同时视图一致性由共享的点云几何天然保证。

### 模型效率对比

Table 2 在 THuman2.0 上量化了效率优势。DiffPBR 端到端训练仅需约 **8 GPU 小时**，而 PFGS 需 41 GPU 小时，训练成本降低约 **5 倍**。推理端，DiffPBR-E 达到 10 FPS，较 PFGS 的 3.6 FPS 提升约 **2.8 倍**。效率增益源于两个设计选择：（1）残差扩散范式使模型可在更少去噪步数内收敛；（2）自适应泼溅本身是轻量级的可微栅格化操作，不依赖昂贵的逐场景优化。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tqOBZbW6j8/figures/006_Table_2.jpg]]
*Table 2: Evaluation of Model Efficiency on Thuman2.0*

### 点云密度鲁棒性

Table 3 展示了 DiffPBR 在不同点云密度下的鲁棒性。随着点数从高密度逐步下采样，DiffPBR 的性能衰减显著慢于 PFGS 等基线。这一特性归因于自适应点尺度机制：当点云稀疏时，$\beta \cdot \text{median}(\{\bar{s}_j\})$ 的全局截断允许点尺度适度扩大以填补空洞；当点云稠密时，紧凑损失 $L_{cmp}$ 抑制掩膜过度扩散，避免模糊。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tqOBZbW6j8/figures/008_Table_3.jpg]]
*Table 3: Robustness with respect to point density on Thuman2.0*

### 消融实验

**自适应泼溅策略。** Table 5 比较了三种点尺度方案在扩散精炼前后的 PSNR。仅用 KNN 初始化（无 $\beta$ 截断）在泼溅阶段 PSNR 较高，但精炼后增益有限；固定尺度方案空洞严重，精炼也无法弥补；CNN 预测尺度引入了额外参数但未见明显优势。KNN + 可学习 $\beta$ 的方案在精炼后取得最高 PSNR，验证了全局截断在保真度与空洞填补之间取得最优平衡。

**覆盖损失与紧凑损失的对抗平衡。** Table 6 揭示了 $L_{cov}$ 与 $L_{cmp}$ 的协同机制。单独使用 $L_{cov}$ 导致掩膜过度膨胀、精炼后 PSNR 下降；单独使用 $L_{cmp}$ 使点尺度收缩、空洞增多；两者联合使用时，可学习参数 $\beta$ 在训练中自适应调整（见 Figure 3），最终取得最优质量。这一对抗设计是稳定收敛的关键。

**残差扩散模块有效性。** Table 7 逐模块拆解了残差扩散的贡献。将标准 DDPM 替换为残差扩散（RDDM）可提升收敛速度和最终 PSNR；进一步用 CoNo-Splatting 的 3D 一致噪声替代 i.i.d. 高斯噪声，带来额外增益。去除 3D 噪声或退化回纯 DDPM 均导致性能明显下降，证实了两个设计缺一不可。

**扩散配置消融。** Table 9 系统比较了不同扩散参数组合在 THuman2.0 和 ScanNet 上、不同训练规模下的表现。$\epsilon$-预测的 multi-step 采样在所有设置下均取得最高 PSNR，验证了残差噪声预测范式的优势。Table 10 进一步表明，颜色与噪声联合泼溅（同一泼溅核）优于位置分离泼溅策略，因为联合泼溅确保了颜色和噪声在空间上的严格对齐。

**自适应泼溅的即插即用性。** Table 13 和 Figure 11 展示了一项关键发现：将自适应 CoNo-Splatting 模块直接插入 PFGS 管线，可显著提升其渲染质量，表明该模块具有独立于扩散后端的通用价值。

### 跨数据集泛化

使用仅在 DTU 上训练的模型直接测试 THuman2.0（无微调），DiffPBR 仍能生成合理的渲染结果（Figure 5），且质量明显优于 PFGS 等基线。这种泛化能力源于方法的核心设计——点云几何先验通过 CoNo-Splatting 注入扩散过程，而非依赖场景特定的外观特征学习。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tqOBZbW6j8/figures/007_Figure_5.jpg]]
*Figure 5: Cross-dataset generalization. Evaluation results labeled “DTU (X)” indicate that method X is trained on DTU without fine-tuning on Thuman2.0, whereas “Thuman2.0 (X)” refers to the in-domain setting*

### 失败模式与局限

当点云出现大面积缺失（如扫描盲区）时，DiffPBR 难以推测未见区域的内容。这是因为模型从头训练，缺乏大规模预训练图像先验，残差扩散仅能修复已有几何结构上的细节，无法凭空补全缺失的几何。此外，当前实现受输出分辨率限制，渲染速度在 1.9～10 FPS 之间，尚未达到实时交互需求（30+ FPS）。

### 公平性说明

所有对比实验在相同基准数据集上评测，PFGS 带 † 标记的结果为作者复现结果。效率对比统一使用 NVIDIA RTX 3090 GPU 环境。跨数据集泛化实验未进行任何微调，确保了比较的公平性。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_tqOBZbW6j8/figures/017_Table_9.jpg]]
*Table 9: Ablation studies on different combinations of diffusion configurations. Each configuration is evaluated under different training set sizes on both THuman2.0 and ScanNet datasets*

## 定位与知识库关联

### 1. 方法谱系：从传统栅格化到残差扩散增强

DiffPBR 处于**神经点云渲染**与**扩散生成模型**的交叉地带。其技术谱系可从两个维度追溯：

**点云渲染的演进。** 传统图形学中，**Pytorch3D** (Ravi et al., 2020) 等可微栅格化器将点投影到像面后直接着色，但离散点云在投影后必然产生空洞与锯齿，导致渲染质量严重受限。神经点渲染方法试图通过学习逐点特征来弥补这一缺陷：**NPBG** (Aliev et al., 2020) 使用神经描述符增强点云外观，**NPBG++** (Rakhimov et al., 2022) 进一步引入在线描述符聚合以提升视图一致性。然而，这些方法本质上仍是对栅格化结果的局部修补，缺乏对全局场景结构的理解。

近年来，两条路线试图突破这一瓶颈：一是引入体素或隐式表示作为几何载体，如 **TriVol** (Hu et al., 2023) 将体素与 NeRF 结合；二是采用更丰富的基元，如 **3DGS** (Kerbl et al., 2023) 使用各向异性 3D 高斯进行逐场景优化，**PFGS** (Wang et al., 2024a) 和 **RPBG** (Zhu et al., 2024) 则将高斯泼溅与神经点渲染融合。DiffPBR 继承了点云作为唯一基元的简洁性，但通过**自适应点尺度策略**和**扩散后处理**，在保持跨场景泛化能力的同时，弥补了纯栅格化的结构性缺陷。

**扩散模型的角色转变。** 标准扩散模型（DDPM）从纯噪声中逐步重建图像，这一过程计算量大且缺乏几何约束。DiffPBR 的核心创新在于将扩散模型从“图像生成器”重新定位为“残差精炼器”：模型仅需预测渲染图像与真实图像的差异，而非从零重建。这一“残差扩散”范式（RDDM）大幅降低了学习难度，使训练时间从 PFGS 的 41 GPU 小时缩减至约 8 GPU 小时，同时将单步推理速度从 3.6 FPS 提升至 10 FPS（DiffPBR-E 变体）。

### 2. 因果机制：三个关键设计瓶颈

DiffPBR 的性能优势源于对三个因果瓶颈的系统性解决：

| 瓶颈 | 传统方案 | DiffPBR 方案 | 因果机制 |
|------|----------|-------------|----------|
| **离散点云的空洞与锯齿** | 固定尺度或网络预测尺度 | 基于 KNN 距离的自适应尺度 + 可学习全局 β 截断 | $s_i = \mathrm{clamp\_max}(\bar{s}_i, \beta \cdot \mathrm{median}(\{\bar{s}_j\}))$ 在保真度与覆盖度之间取得平衡 |
| **扩散过程的几何无知** | i.i.d. 高斯噪声 | CoNo-Splatting 渲染的 3D 一致噪声图 $I_\epsilon$ | 噪声图携带深度与遮挡信息，使扩散过程隐式感知 3D 结构 |
| **全图重建的高计算成本** | 从纯噪声重建完整图像 | 残差扩散：预测 $res\epsilon$（渲染残差与噪声的加权组合） | 模型仅学习“缺失的细节”，收敛步数和训练时间大幅减少 |

其中，**覆盖损失 $\mathcal{L}_{cov}$ 与紧凑损失 $\mathcal{L}_{cmp}$ 的对抗平衡**是实现稳定训练的关键机制。$\mathcal{L}_{cov}$ 推动点尺度扩大以填补空洞，$\mathcal{L}_{cmp}$ 则抑制掩膜过度扩散导致模糊。消融实验（Table 6）表明，二者联合使用时自适应 β 值可收敛至合理区间，单独使用任一项均会导致渲染质量显著下降。

### 3. 适用边界与局限

**已验证的适用场景：**
- 多视图一致的静态场景渲染（ScanNet 室内、DTU 物体、THuman2.0 人体）
- 跨数据集泛化：在 DTU 上训练的模型直接测试 THuman2.0，PSNR 仍显著优于 PFGS 等基线（Figure 5）
- 点云密度鲁棒性：在 THuman2.0 上对点云进行下采样后，DiffPBR 的性能衰减明显小于对比方法（Table 3）

**已确认的局限：**
1. **大面积缺失区域的推理能力不足。** 当点云中存在大片未观测区域时，模型缺乏从头训练带来的强图像先验，难以推测未见内容。这是残差扩散范式的固有限制——模型被训练为“修复已知几何的细节”，而非“幻想未知几何”。
2. **渲染速度尚未达到实时。** DiffPBR-E 的 10 FPS 虽比 PFGS 提升约 2.8 倍，但距离 30+ FPS 的实时交互要求仍有差距，主要受输出分辨率和扩散采样步数限制。

### 4. 知识库定位与开放问题

**在现有知识体系中的位置：** DiffPBR 提供了一种**将几何先验注入扩散过程的通用范式**。其 CoNo-Splatting 模块作为即插即用组件，可直接提升 PFGS 等现有方法的渲染质量（Table 13, Figure 11），表明该方法论具有跨架构的可迁移性。

**待验证的开放问题：**
- **强先验融合：** 如何在保持视图一致性的前提下，引入大规模预训练图像扩散模型（如 Stable Diffusion）的先验，以处理严重缺失区域？直接引入可能导致多视图不一致。
- **实时化路径：** 是否可通过多阶段蒸馏（将多步扩散采样蒸馏为单步预测）或高效采样器（如 DPM-Solver）将渲染速度提升至 30+ FPS？
- **显式表面结合：** 自适应泼溅策略能否与显式表面重建（如泊松重建）结合，在空洞区域生成合理的代理几何，从而减少扩散模型的修复负担？

**证据强度说明：** 上述局限与开放问题均来自论文自身的讨论部分，其中大面积缺失的推理能力不足有明确的定性证据支持，但缺乏系统的定量消融实验；实时化路径的可行性尚未在论文中验证，需后续工作确认。

## 原文 PDF

![[paperPDFs/ICLR_2026/DiffPBR_Point_Based_Rendering_via_Spatial_Aware_Residual_Diffusion_9d4873f74381.pdf]]

---
title: "NimbusGS: Unified 3D Scene Reconstruction under Hybrid Weather"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NimbusGS_Unified_3D_Scene_Reconstruction_under_Hybrid_Weather.pdf
project_link: null
code_link: "https://github.com/lyy-ovo/NimbusGS"
aliases:
- NimbusGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于物理的天气效应分解（连续散射场与颗粒残余层）和几何引导的梯度缩放机制，有效分离场景结构与天气干扰，并缓解因能见度不均导致的远距离梯度不平衡。
primary_logic: 将天气退化解耦为视点一致的连续传输场和视点相关的颗粒残余，在三维高斯泼溅框架中统一建模，使得场景几何与天气效应可分离优化；并通过几何引导的梯度缩放提升远距离区域的几何重建完整性。
claims:
- 在雾天场景中，NimbusGS在所有指标上领先第二名基线，PSNR平均高出4.64 dB，SSIM高出0.067。
- 在混合天气条件下，NimbusGS取得最佳总体性能。
- CSM（高斯驱动的消光场）在雾天场景中优于均匀消光基线。
- Hazy Scenes (Mip-NeRF360/Deblur-NeRF) 上 PSNR↑/SSIM↑/LPIPS↓ = 20.79/0.776/0.190
---

# NimbusGS: Unified 3D Scene Reconstruction under Hybrid Weather

> [!tip] 核心洞察
> 将天气退化解耦为视点一致的连续传输场和视点相关的颗粒残余，在三维高斯泼溅框架中统一建模，使得场景几何与天气效应可分离优化；并通过几何引导的梯度缩放提升远距离区域的几何重建完整性。

| 字段 | 内容 |
|------|------|
| 中文题名 | NimbusGS：混合天气条件下的统一三维场景重建 |
| 英文题名 | NimbusGS: Unified 3D Scene Reconstruction under Hybrid Weather |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27228) · [Code](https://github.com/lyy-ovo/NimbusGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NimbusGS |
| Dataset | Hazy Scenes, Rainy Scenes, Snowy Scenes, Hybrid Weather Scenes |

> [!tip] 效果简介
> - Hazy Scenes (Mip-NeRF360/Deblur-NeRF) 上，PSNR↑/SSIM↑/LPIPS↓ 20.79/0.776/0.190 vs WaterSplatting: 16.15/0.695/0.251 (+4.64 dB PSNR, +0.067 SSIM)。
> - Rainy Scenes (RainyScape) 上，PSNR↑/SSIM↑/LPIPS↓ 32.41/0.904/0.139 vs RainyScape: 29.87/0.851/0.154 (+2.54 dB PSNR, +0.053 SSIM)。
> - Snowy Scenes 上，PSNR↑/SSIM↑/LPIPS↓ 23.27/0.779/0.162 vs RainyScape: 22.34/0.742/0.193。

## 概要

三维场景重建方法在晴朗条件下已取得显著进展，但在雨、雪、雾及混合天气下仍面临根本性瓶颈：现有方案通常针对单一退化类型设计，缺乏对连续介质衰减（如雾）与视点依赖离散粒子（如雨滴、雪花）的联合物理建模，导致几何学习不稳定，产生漂浮伪影和结构失真。

NimbusGS 针对这一瓶颈，提出在三维高斯泼溅框架内对天气效应进行物理驱动的解耦——将退化分解为视点一致的连续传输场（连续散射建模，CSM）和视点相关的颗粒残余层（颗粒层建模，PLM），使场景几何与天气干扰可分离优化。同时引入几何引导的梯度缩放机制（GGS），依据深度、投影半径和重建误差自适应调整高斯梯度，缓解因能见度不均导致的远距离梯度不平衡。

在方法谱系上，NimbusGS 区别于两类现有路线：一类是天气特定的重建方法，如 **SeaSplat**（Yang et al., ICRA 2025）和 **WaterSplatting**（Li et al., 3DV 2025）仅针对水下/雾天场景，**DerainNeRF**（Li et al., ICRA 2024）和 **RainyScape**（Lyu et al., ACM MM 2024）仅处理雨痕去除；另一类是通用瞬态效应去除方法，如 **RobustSplat**（Fu et al., ICCV 2025）和 **WeatherGS**（Qian et al., ICRA 2025），它们缺乏对连续介质散射的显式物理建模。NimbusGS 通过统一的退化渲染方程 $I_{\mathrm{deg}} = \hat{I} \cdot T + P + R$ 将两类退化纳入同一框架，实现了跨天气类型的泛化重建。

实验表明，NimbusGS 在单一和混合天气条件下均取得领先性能：在雾天场景上，PSNR 平均高出第二名基线 4.64 dB，SSIM 高出 0.067（Table 1）；在雨天场景上，PSNR 领先 2.54 dB（Table 2）；在雾+雨+雪混合场景上，PSNR 达到 22.25 dB，显著超越复原+重建管线 OR+3DGS 的 20.09 dB（Table 4）。消融实验进一步验证了 CSM 对连续介质建模的关键作用、PLM 对颗粒效应分离的必要性，以及 GGS 对远距离几何重建的实质性提升。



三维场景重建是计算机视觉与图形学中的基础任务，其目标是从多视角图像中恢复场景的几何结构与外观信息。近年来，以**3D Gaussian Splatting (3DGS)**（Kerbl et al., ACM TOG 2023）为代表的显式辐射场方法，凭借其高效的渲染速度和高质量的几何重建能力，已成为该领域的主流范式。然而，现有方法通常假设输入图像是在晴朗、均匀光照条件下采集的，当面对雾、雨、雪等恶劣天气条件时，其重建性能会急剧退化。

恶劣天气对三维重建的挑战源于两类本质上不同的物理退化机制。第一类是**连续介质衰减**，如雾霾引起的散射与吸收，它沿视线方向累积性地降低对比度并引入视点一致的空气光效应。第二类是**离散颗粒扰动**，如雨滴和雪花，它们在图像平面上形成视点依赖的瞬态遮挡和反射。现有工作大多针对单一退化类型设计专用解决方案——例如**SeaSplat**（Yang et al., ICRA 2025）和**WaterSplatting**（Li et al., 3DV 2025）聚焦水下/雾天场景，**DerainNeRF**（Li et al., ICRA 2024）和**RainyScape**（Lyu et al., ACM MM 2024）专门处理雨痕去除——缺乏对连续介质衰减与视点依赖离散粒子的**联合物理建模**。

这一方法缺口在**混合天气条件**下尤为突出。真实世界中，雾、雨、雪往往同时或交替出现，形成复杂的复合退化。当单一退化模型被强行应用于混合场景时，场景几何与天气效应之间缺乏可分离的物理约束，导致优化过程中几何学习不稳定，产生漂浮伪影和结构失真。此外，恶劣天气下能见度不均还会引发**远距离梯度不平衡**问题：近处区域因信号较强而获得充足的梯度更新，而远处区域因衰减严重而几乎无法驱动高斯点的稠密化，进一步加剧了几何重建的不完整性。

针对上述瓶颈，NimbusGS提出了一种统一的物理驱动框架，核心思路是将天气退化解耦为**视点一致的连续传输场**和**视点相关的颗粒残余**，在三维高斯泼溅框架中实现场景几何与天气效应的可分离优化。同时，引入**几何引导的梯度缩放机制**，依据深度、投影半径和重建误差自适应调整梯度，显著改善远距离区域的几何重建完整性。这一设计使得NimbusGS能够在雾、雨、雪及任意混合组合下，以单一模型实现鲁棒的三维重建。



## 核心方法与创新机理

NimbusGS 的核心创新在于将混合天气条件下的三维重建问题重新表述为**物理驱动的退化分解与几何自适应优化**。与现有方法针对单一退化类型（雾、雨或雪）设计专用模块不同，NimbusGS 通过三个关键机制（changed slots）实现了对连续介质衰减和离散颗粒效应的统一建模，并在优化过程中解决了因天气导致的梯度不平衡问题。

### 1. 退化渲染模型：从标准α混合到物理分解

标准三维高斯泼溅（**3DGS**, Kerbl et al., ACM TOG 2023）的渲染模型为简单的α混合：

$$C = \sum_i c_i \alpha_i \prod_{j=1}^{i-1} (1-\alpha_j)$$

NimbusGS 将其替换为基于物理的退化渲染模型：

$$I_{\mathrm{deg}} = {\hat{I}} \cdot T + P + R$$

其中 ${\hat{I}}$ 为清晰的场景渲染，$T$ 为透射率（transmission），$P$ 为空气光散射项（airlight），$R$ 为颗粒残余层（particulate residual）。这一分解的**因果逻辑**在于：连续介质（雾、霾）造成的衰减是视点一致的，可以通过全局传输场建模；而雨滴、雪花等离散颗粒是视点相关的瞬态扰动，需要逐视图的残余层来捕捉。通过将退化过程显式参数化，模型能够将场景几何与天气效应**解耦优化**，避免几何学习被天气干扰污染。

### 2. 连续散射建模（CSM）：高斯驱动的消光场

现有方法缺乏对连续介质的显式建模，NimbusGS 引入了**连续散射建模（Continuous Scattering Modeling, CSM）**。其核心是一个体素化的消光场 $\beta(\mathbf{x})$，沿视线积分得到透射率：

$$T = \exp\Big( -\sum_{j=1}^{K} \beta\big( \mathbf{r}(s_j) \big) \Delta s_j \Big)$$

空气光项则由各采样点的散射贡献累积：

$$P = \sum_{i=1}^{K} T_i \left( 1 - \exp\big( -\beta(\mathbf{r}(s_i)) \Delta s_i \big) \right) A$$

消光场由三维高斯驱动估计，这使得连续介质衰减的建模与场景几何表示**共享同一表示空间**。消融实验（Table 5）证实，CSM 在雾天场景上取得 20.79 PSNR，优于均匀消光基线（20.55 PSNR），验证了空间变化消光场对非均匀雾的建模优势。

### 3. 颗粒层建模（PLM）：逐视图瞬态残余

对于雨、雪等离散颗粒，NimbusGS 设计了**颗粒层建模（Particulate Layer Modeling, PLM）**。其关键设计在于：训练初期通过**几何初始化阶段**（前 4k 迭代）稳定场景几何，将瞬态颗粒效应隔离为逐视图的残余层 $R$，防止颗粒被错误吸收进高斯表示中。后续联合优化阶段每 100 次迭代刷新残余层，以适应动态颗粒的变化。消融实验（Table 5）表明，移除 PLM 后雨天场景 PSNR 从 32.41 骤降至 29.65，定性结果（Figure 7）进一步显示颗粒残余层有效去除了雨痕和雪花伪影。

### 4. 几何引导梯度缩放（GGS）：解决远距离梯度不平衡

恶劣天气下能见度不均导致远距离区域梯度信号微弱，标准 3DGS 的稠密化策略难以在远距离生成足够的高斯。NimbusGS 提出**几何引导梯度缩放（Geometry-Guided Gradient Scaling, GGS）**，自适应调整每个高斯的梯度：

$$w_i = d_{\mathrm{norm}}^{i} \cdot \left(\frac{r_i}{r_0}\right) \cdot \sigma(e_{\mathrm{norm}}^{i})$$

三个因子分别对应：深度归一化 $d_{\mathrm{norm}}^{i}$（远距离高斯获得更大梯度）、投影半径比 $r_i/r_0$（补偿透视投影造成的梯度衰减）、重建误差 $\sigma(e_{\mathrm{norm}}^{i})$（高误差区域获得更多优化关注）。消融实验（Table 6）表明，移除深度因子导致重建质量下降最大，验证了远距离梯度补偿是 GGS 的核心贡献。在混合天气场景中，GGS 将 PSNR 从 21.80 提升至 22.25（Table 5）。

### 5. 两阶段训练策略

上述组件通过**两阶段训练策略**协同工作：第一阶段（几何初始化）仅优化清晰场景渲染与颗粒残余层，将颗粒效应从几何中分离；第二阶段联合优化高斯表示、消光场和空气光 MLP，损失函数为：

$$\mathcal{L} = (1 - \lambda_{\mathrm{r}}) \|I_{\mathrm{in}} - I_{\mathrm{deg}}\|_1 + \lambda_{\mathrm{r}} (1 - \mathrm{SSIM}(I_{\mathrm{in}}, I_{\mathrm{deg}})) + \mathcal{L}_{\mathrm{TV}}$$

这一策略的**瓶颈突破**在于：通过先分离后联合的课程式学习，避免了天气效应与场景几何在优化初期的相互干扰，使得 CSM 和 PLM 能够各司其职。

---

**创新总结**：NimbusGS 的方法创新并非简单的模块堆砌，而是通过**物理驱动的退化分解**（CSM + PLM）将天气效应从场景表示中解耦，再通过**几何自适应的优化策略**（GGS + 两阶段训练）解决恶劣天气特有的优化困难。这一设计使得单一框架在雾、雨、雪及混合天气条件下均显著超越专用基线方法。



NimbusGS 提出了一种统一的退化渲染模型，将混合天气条件下的三维场景重建问题形式化为对清晰场景渲染、连续介质衰减和视点依赖颗粒效应的联合估计。其核心思想在于：输入退化图像 $I_{\mathrm{deg}}$ 可分解为三个物理可解释分量的叠加——

$$I_{\mathrm{deg}} = {\hat{I}} \cdot T + P + R$$

其中 ${\hat{I}}$ 为清晰场景的渲染结果，$T$ 为沿视线的透射率，$P$ 为空气光散射累积项，$R$ 为颗粒残余层。这一分解将天气退化解耦为**视点一致的连续传输场**（$T$ 与 $P$）和**视点相关的瞬态颗粒效应**（$R$），使得场景几何与天气干扰可分离优化。

围绕上述退化模型，NimbusGS 构建了四个核心模块，形成完整的自监督优化管线（Figure 2）：

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/002_Figure_2.jpg]]
*Figure 2: Overview of NimbusGS. Starting from a geometry initialization, transient particle effects are separated as per-view residuals. CSM estimates an extinction field from which transmission and airlight are derived, blended with the scene rendering and residuals to reproduce the degradations. This self-supervised process guides the Gaussian representation toward a clean and consistent reconstruction*

1. **几何初始化（Geometry Initialization）**：在训练初期稳定场景几何结构，防止颗粒效应被吸收进三维高斯表示中，为后续的颗粒层分离提供可靠的几何基底。

2. **连续散射建模（Continuous Scattering Modeling, CSM）**：通过体素化的消光场 $\beta(\mathbf{x})$ 和空气光 MLP 估计全局连续介质衰减，沿视线积分得到透射率 $T$ 和空气光项 $P$，建模雾、霾等视点一致的散射效应。

3. **颗粒层建模（Particulate Layer Modeling, PLM）**：提取逐视图的颗粒残余 $R$，捕捉雨痕、雪花等动态瞬态扰动。该层在几何初始化阶段被隔离提取，避免其干扰高斯表示的几何学习。

4. **几何引导梯度缩放（Geometry-Guided Gradient Scaling, GGS）**：根据每个高斯的深度 $d_i$、投影半径 $r_i$ 和重建误差 $e_i$ 自适应调整梯度缩放权重——

$$w_i = d_{\mathrm{norm}}^{i} \cdot \left(\frac{r_i}{r_0}\right) \cdot \sigma(e_{\mathrm{norm}}^{i})$$

该机制有效缓解了因能见度不均导致的远距离区域梯度不平衡问题，改善了远端几何的稠密化质量。

**训练策略**采用两阶段方案：第一阶段（前 4k 次迭代）仅优化高斯表示以初始化几何，同时分离颗粒残余层；第二阶段（后续 26k 次迭代）联合优化高斯表示与所有退化组件，颗粒层每 100 次迭代刷新一次。最终损失函数结合 L1 损失、SSIM 损失和全变分正则项：

$$\mathcal{L} = (1 - \lambda_{\mathrm{r}}) \|I_{\mathrm{in}} - I_{\mathrm{deg}}\|_1 + \lambda_{\mathrm{r}} (1 - \mathrm{SSIM}(I_{\mathrm{in}}, I_{\mathrm{deg}})) + \mathcal{L}_{\mathrm{TV}}$$

整体而言，NimbusGS 的管线设计实现了从“输入退化图像 → 几何初始化 → 颗粒效应分离 → 连续散射估计 → 联合退化渲染 → 自监督优化”的闭环，在无需成对清晰数据的情况下，统一处理雾、雨、雪及其混合组合的天气退化。

### 补充图表

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/001_Figure_1.jpg]]
*Figure 1: We propose NimbusGS, a unified framework for 3D reconstruction under diverse and hybrid weather conditions. It jointly addresses continuous medium effects (haze, H), particulate degradations (snow, S; rain, R), and their mixed combinations. Panel (a) presents visual comparisons across weather types, while panel (b) summarizes metric profiles over seven single and hybrid settings*



NimbusGS 的核心设计思路是将混合天气退化分解为两类物理上可区分的效应：视点一致的连续介质衰减和视点依赖的离散颗粒扰动。基于这一分解，方法在三维高斯泼溅框架中引入三个关键模块——连续散射建模（CSM）、颗粒层建模（PLM）和几何引导梯度缩放（GGS），并通过两阶段训练策略实现稳定优化。

### 退化渲染模型

标准三维高斯泼溅的像素颜色由 alpha 混合得到：

$$C = \sum_{i} c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$

其中 $c_i$ 为高斯颜色，$\alpha_i$ 为经不透明度与二维协方差调制的有效 alpha 值。NimbusGS 将这一清晰渲染结果记为 $\hat{I}$，并在此基础上叠加天气退化效应，形成最终的退化渲染方程：

$$I_{\mathrm{deg}} = {\hat{I}} \cdot T + P + R$$

式中各项含义如下：
- **$T$（透射率）**：描述连续介质（雾、霾）对场景辐射的指数衰减，取值范围 $[0,1]$，由消光场沿视线积分得到。
- **$P$（空气光项）**：描述环境光经介质散射后进入相机的累积贡献，是雾天图像“泛白”现象的物理来源。
- **$R$（颗粒残余层）**：逐视图的残差图像，用于捕捉雨滴、雪花等瞬态离散颗粒的局部遮挡和散射效应。

### 连续散射建模（CSM）

CSM 的目标是从输入视图中估计一个全局共享的消光场 $\beta(\mathbf{x})$，进而计算每条视线的透射率和空气光项。对于沿视线 $\mathbf{r}(s) = \mathbf{o} + s\mathbf{d}$ 采样的 $K$ 个点，透射率定义为：

$$T = \exp\Big(-\sum_{j=1}^{K} \beta\big(\mathbf{r}(s_j)\big) \Delta s_j\Big)$$

空气光项则由各采样点散射贡献的累积给出：

$$P = \sum_{i=1}^{K} T_i \Big(1 - \exp\big(-\beta(\mathbf{r}(s_i)) \Delta s_i\big)\Big) A$$

其中 $T_i$ 为从相机到采样点 $s_i$ 的累积透射率，$A$ 为空气光颜色，由一个轻量 MLP 预测。消光场 $\beta(\mathbf{x})$ 通过体素网格参数化，由三维高斯的位置驱动优化，使得场景几何与介质衰减可在统一框架中联合学习。这种“高斯驱动”的消光场设计是 CSM 区别于均匀消光假设的关键——消融实验（Table 5）表明，CSM 在雾天场景上取得 20.79 PSNR，优于均匀消光基线的 20.55 PSNR。

### 颗粒层建模（PLM）

PLM 负责处理雨、雪等视点依赖的离散颗粒效应。核心观察是：颗粒在连续帧间快速运动，而场景几何保持静态。因此，PLM 为每个训练视图维护一个可学习的残余图像 $R$，直接建模退化渲染方程中的颗粒项。训练第一阶段（几何初始化阶段）仅优化高斯表示和 $R$，不引入 CSM 组件，迫使颗粒效应被分离到残差层而非被吸收进高斯几何中。第二阶段联合优化时，$R$ 每 100 次迭代刷新一次，以适应颗粒分布的动态变化。

消融实验（Table 5）验证了 PLM 的有效性：在雨天场景上，完整方法取得 32.41 PSNR，移除 PLM 后降至 29.65 PSNR，降幅达 2.76 dB。

### 几何引导梯度缩放（GGS）

恶劣天气下远距离区域能见度低、梯度信号弱，标准三维高斯泼溅的累积梯度阈值稠密化策略会导致远距离几何欠重建。GGS 通过三个互补因子自适应缩放每个高斯的梯度：

$$w_i = d_{\mathrm{norm}}^{i} \cdot \left(\frac{r_i}{r_0}\right) \cdot \sigma(e_{\mathrm{norm}}^{i})$$

- **深度因子 $d_{\mathrm{norm}}^{i}$**：将高斯深度归一化至 $[0,1]$，远距离高斯获得更大权重，补偿其天然较小的投影梯度。
- **半径因子 $r_i / r_0$**：$r_i$ 为高斯的二维投影半径，$r_0$ 为参考半径。大半径高斯对应远距离或欠采样区域，增大其梯度以促进稠密化。
- **误差因子 $\sigma(e_{\mathrm{norm}}^{i})$**：$e_i$ 为退化渲染与输入图像在投影位置 $(u_i, v_i)$ 处的 L1 误差，经归一化和 sigmoid 激活后，高重建误差区域获得额外梯度放大。

因子消融实验（Table 6）表明，移除深度因子导致重建质量下降最大，证实了远距离梯度补偿是 GGS 的核心作用机制。完整 GGS 将混合天气场景的 PSNR 从 21.80 提升至 22.25。

### 两阶段训练策略

训练分为两个阶段：
1. **几何初始化阶段**（前 4k 迭代）：仅优化高斯表示和颗粒残差层 $R$，不使用 CSM 组件。此阶段的目标是在颗粒效应被分离的前提下建立稳定的场景几何先验，防止后续联合优化中颗粒被错误吸收进高斯结构。
2. **联合优化阶段**（后续 26k 迭代）：同时优化高斯表示、消光场 $\beta$、空气光 MLP 和颗粒残差层 $R$，损失函数为：

$$\mathcal{L} = (1 - \lambda_{\mathrm{r}}) \|I_{\mathrm{in}} - I_{\mathrm{deg}}\|_1 + \lambda_{\mathrm{r}} (1 - \mathrm{SSIM}(I_{\mathrm{in}}, I_{\mathrm{deg}})) + \mathcal{L}_{\mathrm{TV}}$$

其中 $\lambda_{\mathrm{r}}$ 平衡 L1 和 SSIM 损失，$\mathcal{L}_{\mathrm{TV}}$ 为全变分正则项，约束消光场的空间平滑性。损失项消融（Table 7）显示，移除暗通道先验损失 $\mathcal{L}_{\mathrm{DCP}}$ 后 PSNR 从 22.25 骤降至 17.32，说明物理先验正则对收敛至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/013_Figure_7.jpg]]
*Figure 7: Qualitative ablation of Particulate Layer Modeling. Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/015_Figure_9.jpg]]
*Figure 9: Qualitative ablation of Geometry-Guided Gradient Scaling. Best viewed zoomed in*



## 实验与关键发现

### 主实验结果

NimbusGS 在单一退化与混合天气条件下均展现出统一的场景重建能力，其核心优势源于物理驱动的天气效应分解——连续散射场（CSM）与颗粒残余层（PLM）的协同建模，以及几何引导的梯度缩放机制（GGS）对远距离梯度不平衡的缓解。

**雾天场景（Hazy Scenes）**：在 Mip-NeRF360 与 Deblur-NeRF 数据集上，NimbusGS 以平均 **20.79 dB PSNR / 0.776 SSIM / 0.190 LPIPS** 取得所有指标最优（Table 1）。相较于次优基线 WaterSplatting（Li et al., 3DV 2025），PSNR 领先 **4.64 dB**，SSIM 高出 **0.067**。定性对比（Figure 3）显示，3DGS（Kerbl et al., ACM TOG 2023）在雾天场景中产生大量漂浮伪影与结构失真，而 NimbusGS 有效恢复了清晰几何与纹理细节。这一性能差距的根本原因在于：3DGS 缺乏对连续介质衰减的建模，将消光效应错误地解释为几何结构；NimbusGS 通过 CSM 的高斯驱动消光场显式分离了传输衰减，使几何优化免受雾天干扰。

**雨天场景（Rainy Scenes）**：在 RainyScape 数据集上，NimbusGS 以 **32.41 dB PSNR / 0.904 SSIM** 超越所有雨天专用基线（Table 2），较 RainyScape（Lyu et al., ACM MM 2024）提升 **2.54 dB PSNR** 与 **0.053 SSIM**。Figure 4 的定性结果表明，DerainNeRF（Li et al., ICRA 2024）和 WeatherGS（Qian et al., ICRA 2025）在去除雨痕时容易引入过度平滑或残留伪影，而 NimbusGS 的 PLM 通过逐视图颗粒残余层有效捕捉了雨滴的视点依赖特性，同时保护了底层几何完整性。

**雪天场景（Snowy Scenes）**：NimbusGS 取得 **23.27 dB PSNR / 0.779 SSIM**（Table 3），在 PSNR 与 SSIM 上均优于所有对比方法。Figure 5 的定性对比显示，RobustSplat（Fu et al., ICCV 2025）在雪花密集区域仍残留明显颗粒伪影，而 NimbusGS 的 PLM 成功将雪花建模为瞬态残余，避免其污染高斯几何表示。

**混合天气场景（Hybrid Weather Scenes）**：这是最能体现 NimbusGS 统一建模优势的测试设置。在同时包含雾、雨、雪的 H+R+S 条件下，NimbusGS 取得 **22.25 dB PSNR / 0.742 SSIM / 0.202 LPIPS**（Table 4），显著优于 OneRestore+3DGS 复原-重建管线（Guo et al., ECCV 2024; Kerbl et al., ACM TOG 2023）的 20.09 dB PSNR / 0.661 SSIM。Figure 6 的定性结果进一步表明，WeatherGS 在混合天气下出现明显的结构崩溃与颜色偏移，而 NimbusGS 能够同时处理连续介质衰减与离散颗粒效应，保持几何一致性与纹理保真度。该结果验证了核心洞察：将天气退化解耦为视点一致的传输场与视点相关的颗粒残余，使得场景几何与天气效应可分离优化，是混合天气重建成功的关键。

### 消融实验

消融实验系统验证了 NimbusGS 各组件的独立贡献与因果机制。

**连续散射建模（CSM）**：Table 5 显示，在雾天场景上，CSM（高斯驱动消光场）取得 20.79 dB PSNR，优于均匀消光基线的 20.55 dB PSNR。Figure 8 的定性消融表明，移除 CSM 后，模型无法正确建模雾天的视点一致衰减，导致远景区域出现明显的能见度估计错误与几何坍塌。这验证了 CSM 中体素化消光场 $\beta(\mathbf{x})$ 与空气光 MLP 对连续介质衰减的物理建模必要性。

**颗粒层建模（PLM）**：在雨天场景上，完整 PLM 取得 32.41 dB PSNR，移除后骤降至 29.65 dB PSNR（Table 5）。Figure 7 的定性消融进一步揭示，无 PLM 时雨痕被错误地吸收进高斯几何表示，产生不可逆的几何污染与伪影。PLM 的有效性建立在其两阶段训练策略之上：几何初始化阶段（前 4k 迭代）先将颗粒效应从静态几何中分离，再在联合优化阶段（后 26k 迭代）协同精炼高斯与退化组件。

**几何引导梯度缩放（GGS）**：在混合天气 H+R+S 设置下，GGS 将 PSNR 从 21.80 dB 提升至 22.25 dB（Table 5 底部）。因子级消融（Table 6）表明，移除深度因子 $d_{\mathrm{norm}}^{i}$ 导致性能下降最大，验证了远距离高斯因能见度降低而梯度不足是核心瓶颈，深度感知的梯度重缩放是 GGS 最关键的因果旋钮。Figure 9 的定性消融显示，无 GGS 时远景区域几何重建不完整，出现空洞与模糊。

**损失函数消融**：Table 7 揭示，移除暗通道先验损失 $\mathcal{L}_{\mathrm{DCP}}$ 导致性能从 22.25 dB 骤降至 17.32 dB PSNR，是所有消融项中影响最大的。这表明 $\mathcal{L}_{\mathrm{DCP}}$ 在自监督框架中起到了关键的几何正则化作用，但其在后期优化中可能导致偏向欠曝光解的风险已在论文中被识别并处理。

**几何初始化迭代次数**：Table 8 的消融表明，4k 次几何初始化迭代在 PSNR 与 SSIM 上均取得最优，过少（2k）导致颗粒分离不充分，过多（8k）则过度约束几何灵活性。

### 复杂度与效率分析

Table 9 报告了 H+R+S 设置下的模型复杂度与运行时间对比。NimbusGS 在参数量、训练显存、训练时间与渲染帧率（FPS）方面的开销需查阅原文 Table 9 获取精确数值。总体而言，NimbusGS 以可接受的计算代价换取了跨天气类型的统一建模能力与显著的性能提升。

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/018_Table_9.jpg]]
*Table 9: Model complexity and runtime comparison under the H+R+S setting. Params., Memory, Training, and FPS denote parameter count, training memory usage, training time, and rendering speed, respectively*

### 失败模式与局限性

论文明确指出，NimbusGS 在**稀疏视图设置**下存在性能下降。当输入视图稀疏时，去除颗粒残余会暴露缺乏外观线索的遮挡区域，模型缺少足够先验来恢复这些区域的几何与纹理，导致重建不完整。这一局限性指向一个开放挑战：稀疏视图下的几何补全问题仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on hazy scenes. The best and second-best scores are color-encoded for clarity*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results on hazy scenes. Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons on rainy scenes. The best and second-best scores are color-encoded for clarity*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results on rainy scenes. Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results on snowy scenes. Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative results on hybrid-weather scenes (haze, rain, and snow). Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2553_https_arxiv_org_abs_2603_27228/figures/017_Table_7.jpg]]
*Table 7: Ablation of loss terms. Best results are marked in bold*



## 定位与知识库关联

### 与现有方法的关系

NimbusGS 的提出根植于一个明确的瓶颈：现有三维重建方法在恶劣天气下通常针对单一退化类型设计，缺乏对连续介质衰减和视点依赖离散粒子的联合物理建模，导致在混合天气条件下几何学习不稳定，产生漂浮伪影和结构失真。为应对这一瓶颈，NimbusGS 在三维高斯泼溅框架中引入了一套物理驱动的天气效应分解与几何引导优化机制，其方法谱系可从以下几个维度定位。

**与标准三维高斯泼溅（3DGS）的关系。** 3DGS（Kerbl et al., ACM TOG 2023）提供了基础的高效可微渲染管线，但其标准 α 混合模型（$C = \sum_i c_i \alpha_i \prod_{j=1}^{i-1}(1-\alpha_j)$）假定场景辐射在透明介质中自由传播，无法处理散射衰减和瞬态遮挡。NimbusGS 将这一标准渲染模型替换为退化渲染模型 $I_{\mathrm{deg}} = \hat{I} \cdot T + P + R$，在 3DGS 的显式几何表示之上叠加了透射率场 $T$、空气光散射项 $P$ 和颗粒残余层 $R$，使高斯表示能够在保持显式几何优势的同时，与天气退化过程进行物理一致的交互。这一改造的核心在于将 3DGS 从“清晰场景重建”扩展为“退化感知的场景重建”，而非简单地在前端或后端串联一个去退化模块。

**与天气专用重建方法的关系。** 在雾天场景中，**SeaSplat**（Yang et al., ICRA 2025）和 **WaterSplatting**（Li et al., 3DV 2025）分别针对水下介质衰减设计，但均依赖均匀介质假设，无法适应实际雾天中消光系数的空间变化。NimbusGS 的连续散射建模（CSM）通过体素化消光场 $\beta(\mathbf{x})$ 和空气光 MLP 实现了空间变化的散射参数化，在雾天基准上以 20.79 dB PSNR 显著超越 WaterSplatting 的 16.15 dB（Table 1），验证了非均匀消光建模的必要性。在雨天场景中，**DerainNeRF**（Li et al., ICRA 2024）和 **RainyScape**（Lyu et al., ACM MM 2024）专注于雨痕去除，但缺乏对场景几何的显式建模；**RobustSplat**（Fu et al., ICCV 2025）通过瞬态效应掩膜处理遮挡，但未区分连续散射与离散颗粒的物理成因。NimbusGS 的颗粒层建模（PLM）将雨、雪等动态扰动建模为逐视图的残余层，通过两阶段训练中的几何初始化阶段将其与静态场景几何分离，在雨天场景上取得 32.41 dB PSNR，较 RainyScape 的 29.87 dB 提升 2.54 dB（Table 2）。

**与天气感知高斯泼溅方法的关系。** **WeatherGS**（Qian et al., ICRA 2025）是直接可比的天气感知三维高斯泼溅方法，同样尝试在 3DGS 框架内处理多种天气退化。然而，WeatherGS 未区分连续介质衰减与颗粒效应的物理差异，其退化建模缺乏对透射率场和空气光项的显式物理参数化。NimbusGS 通过 CSM 与 PLM 的分解式设计，将视点一致的连续散射与视点相关的颗粒残余解耦，使得场景几何与天气效应可分离优化。在混合天气场景（H+R+S）中，NimbusGS 取得 22.25 dB PSNR，优于 WeatherGS 及其他基线（Table 4），证明了解耦物理建模在复杂退化组合下的泛化优势。

**与“复原+重建”管线的关系。** **OneRestore+3DGS**（Guo et al., ECCV 2024; Kerbl et al., ACM TOG 2023）代表了另一种技术路线：先对退化图像进行复原，再在复原图像上运行标准 3DGS。这种串联管线存在两个根本性问题：一是复原步骤的信息损失不可逆，二是复原模型通常针对单一天气训练，在混合天气下泛化能力有限。NimbusGS 通过将退化建模嵌入渲染管线内部，避免了前置复原带来的信息瓶颈。在混合天气基准上，NimbusGS 的 SSIM 为 0.742，而 OR+3DGS 仅为 0.661（Table 4），这一差距反映了端到端物理建模相对于串联管线的结构性优势。

### 适用边界与局限

NimbusGS 的设计假设场景退化可由连续散射场与颗粒残余层的叠加来近似，这意味着其适用边界受限于该物理模型的表达能力。当退化机制超出该范畴——例如强湍流导致的光线弯曲、冰雹等大尺寸遮挡物造成的完全遮挡——模型的分解能力将下降。此外，NimbusGS 依赖多视图观测来分离静态场景与动态颗粒效应，在**稀疏视图设置下**，去除颗粒残余会暴露缺乏外观线索的区域，模型缺少先验来恢复这些区域，导致性能下降。这一局限在论文中被明确指认为当前方法的不足，稀疏视图下的几何补全问题仍是一个开放挑战。

从计算开销角度，NimbusGS 在 3DGS 基础上增加了消光场体素查询、空气光 MLP 推理和颗粒层刷新操作。根据 Table 9，在 H+R+S 设置下，NimbusGS 的参数量、训练显存占用和训练时间均高于标准 3DGS，但渲染速度仍保持在实时水平。这一开销换取的是混合天气条件下的大幅质量提升，在应用场景允许离线训练的前提下是可接受的。

### 开放问题

论文揭示或未解决的开放问题包括：

1. **稀疏视图下的几何补全。** 当输入视图数量减少时，颗粒层去除暴露的遮挡区域缺乏多视图一致性约束，当前框架缺少有效的先验来填充这些区域。引入生成式先验或深度基础模型可能是潜在的解决方向，但论文未对此展开探索。

2. **退化类型的可扩展性。** NimbusGS 当前覆盖雾、雨、雪及其组合，但未验证其对其他大气效应（如烟、尘、热浪）的泛化能力。这些退化类型可能涉及不同的散射相位函数或非刚性运动，需要进一步扩展物理模型。

3. **暗通道先验的取舍。** 消融实验（Table 7）显示，移除暗通道先验损失 $L_{\mathrm{DCP}}$ 导致 PSNR 从 22.25 dB 骤降至 17.32 dB，表明该先验在训练早期对几何初始化至关重要。然而，论文同时指出暗通道先验基于自然图像统计假设，可能在后期优化中偏向欠曝光解。如何在训练过程中动态调整该先验的权重，或寻找更鲁棒的替代先验，是一个值得深入的方向。

4. **实时应用场景的优化。** 尽管渲染速度保持实时，但训练阶段的额外开销限制了 NimbusGS 在需要快速部署的场景（如自动驾驶在线建图）中的适用性。如何通过模型蒸馏或轻量化消光场表示来降低训练成本，是走向实际部署的关键问题。



## 原文 PDF

![[paperPDFs/CVPR_2026/NimbusGS_Unified_3D_Scene_Reconstruction_under_Hybrid_Weather.pdf]]

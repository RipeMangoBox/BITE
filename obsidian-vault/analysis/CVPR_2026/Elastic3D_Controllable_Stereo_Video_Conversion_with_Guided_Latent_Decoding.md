---
title: "Elastic3D: Controllable Stereo Video Conversion with Guided Latent Decoding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Elastic3D_Controllable_Stereo_Video_Conversion_with_Guided_Latent_Decoding.pdf
project_link: null
code_link: null
aliases:
- Elastic3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 标量视差因子δ（中值视差）作为3D强度的直观控制旋钮；左视图引导的VAE解码器通过极线注意机制从输入视图注入高频细节，绕过潜在空间瓶颈。
primary_logic: 在潜在扩散框架中完全绕过深度估计和扭曲步骤，直接生成右视图；利用视差条件实现对立体效果的无级控制，并通过左视图引导的VAE解码器恢复纹理细节，从而获得无伪影、高保真且可控的立体视频。
claims:
- 视差条件在iPhone数据集上带来+3.8 dB PSNR提升，证明了跨基线泛化和3D强度控制的必要性。
- 引导解码器将GT右视图重构的PSNR从30.2提升至34.3 dB，LPIPS相对改善35%，表明其有效绕过了标准VAE的信息瓶颈。
- 在端到端立体转换任务上，引导解码器使LPIPS降低16%，Matchability误差（双眼竞争代理指标）下降44%，且能即插即用地提升M2SVid等基线。
- 在AVP数据集上，Elastic3D以25.9 PSNR / 0.196 LPIPS全面优于所有基线，定性结果也显示其生成更清晰的纹理和更准确的几何。
---

# Elastic3D: Controllable Stereo Video Conversion with Guided Latent Decoding

> [!tip] 核心洞察
> 在潜在扩散框架中完全绕过深度估计和扭曲步骤，直接生成右视图；利用视差条件实现对立体效果的无级控制，并通过左视图引导的VAE解码器恢复纹理细节，从而获得无伪影、高保真且可控的立体视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | Elastic3D：基于引导潜在解码的可控立体视频转换 |
| 英文题名 | Elastic3D: Controllable Stereo Video Conversion with Guided Latent Decoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.14236) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Elastic3D |
| Dataset | AVP Spatial Video, Stereo4D, iPhone Spatial Video |

> [!tip] 效果简介
> - AVP Spatial Video (Vision Pro) 上，PSNR / SSIM / LPIPS / εMatch / P-PSNR / Disp.err / Temp.err 25.9 / 0.894 / 0.196 / 30.9 / 28.4 / 1.74 / 1.31 vs M2SVid: 24.4 / 0.821 / 0.221 / 41.5 / 27.3 / 2.30 / 1.35 (+1.5 dB PSNR, -25% LPIPS, -25% Matchability)。
> - Stereo4D (test set) 上，PSNR / SSIM / LPIPS / εMatch / P-PSNR / Disp.err / Temp.err 26.1 / 0.913 / 0.176 / 27.8 / 27.4 / 1.24 / 1.30 vs M2SVid: 24.6 / 0.819 / 0.206 / 39.6 / 26.3 / 1.56 / 1.35 (+1.5 dB PSNR, -15% LPIPS, -30% Matchability)。
> - iPhone Spatial Video 上，PSNR / SSIM / LPIPS / εMatch / P-PSNR / Disp.err / Temp.err 22.5 / 0.890 / 0.193 / 26.5 / 26.2 / 0.77 / 3.10 vs M2SVid: 22.9 / 0.865 / 0.205 / 38.4 / 25.1 / 0.60 / 3.06 (PSNR -0.4, SSIM +0.025, LPIPS -0.012, Matchability -31%)。

## 概述

### 问题背景

单目转立体视频转换是实现空间视频（Spatial Video）内容创作的关键技术，广泛应用于Apple Vision Pro、Meta Quest等XR设备。传统方法依赖显式深度估计与基于扭曲（warping）的重投影管线：先从输入左视图估计深度图，再将像素扭曲到右眼视角，最后通过修补（inpainting）或扩散模型精修填补空洞与遮挡区域。代表性工作如**SVG**（Yu et al., 2024）、**StereoCrafter**（2024）和**M2SVid**（Ye et al., 2024）均遵循此范式。

然而，这一管线存在两个根本性瓶颈：
1. **扭曲伪影**：深度估计误差和遮挡区域导致空洞、撕裂和几何失真，后续精修步骤难以完全修复；
2. **潜在空间信息瓶颈**：基于潜在扩散模型（LDM）的视频生成方法（如Stable Video Diffusion）依赖VAE将视频压缩至低维潜在空间（压缩比约1:48），这一高度有损压缩会丢失高频纹理细节，导致双眼竞争（binocular rivalry）——左右视图纹理不一致引发的视觉不适。

此外，现有方法缺乏对立体效果强度的直观控制：扭曲方法需间接缩放深度图，而免扭曲方法如**Eye2Eye**（2024）则完全无法调节3D强度，限制了实际部署的灵活性。

### 核心方法

**Elastic3D**提出了一种直接、免扭曲的前馈立体视频生成框架，完全绕过深度估计和扭曲步骤，在潜在扩散模型的潜在空间中直接合成右视图视频。其核心设计包含三个关键创新：

- **免扭曲直接生成**：以Stable Video Diffusion为基础，将输入左视图编码为潜在表示$z_L$后，前馈生成网络$f_\theta$从零噪声$\mathbf{0}$出发，直接预测右视图潜在表示$\hat{z}_R$，无需任何显式几何推理。

- **标量视差条件控制**：引入标量中值视差$\delta = \mathrm{P}_{50}(D_{LR}^0)$作为条件信号，通过可学习的视差令牌$\tau(\delta)$注入生成网络。用户仅需调节一个连续标量即可直观控制立体效果的强弱，实现了从平面到强3D效果的无级调节。

- **左视图引导的VAE解码器**：针对标准VAE解码器的高频信息丢失问题，设计了一种包含极线交叉注意力（Epipolar Cross-Attention）的引导解码器$\mathcal{D}'$。该解码器在逐层上采样过程中，通过沿核线方向的一维交叉注意力从原始左视图$V_L$的多尺度特征中提取高频细节，并将其注入右视图解码过程，从而绕过潜在空间的信息瓶颈，恢复纹理保真度。

整体推理流程为：
$$\hat{V}_R = \mathcal{D}'(f_\theta(\mathbf{0}, z_L, \tau(\delta)), V_L), \quad z_L = \mathcal{E}(V_L)$$

### 主要结果

在三个域外（in-the-wild）数据集上的全面评估表明，Elastic3D在重建质量、立体保真度和跨基线泛化能力上均显著优于现有方法：

- **AVP Spatial Video数据集**：PSNR达25.9 dB，LPIPS为0.196，Matchability误差（双眼竞争代理指标）仅30.9%，较最优基线**M2SVid**分别提升+1.5 dB、-25% LPIPS和-25% Matchability误差（Table 5）。

- **Stereo4D测试集**：PSNR 26.1 dB，LPIPS 0.176，Matchability误差27.8%，较M2SVid提升+1.5 dB PSNR、-15% LPIPS和-30% Matchability误差（Table 6）。

- **iPhone Spatial Video数据集**（分布外）：SSIM达0.890，LPIPS为0.193，Matchability误差仅26.5%，较M2SVid的38.4%降低31%，证明了对不同相机基线的强泛化能力（Table 7）。

消融实验揭示了各组件的决定性贡献：
- **视差条件**在iPhone数据集上带来+3.8 dB PSNR的提升（18.7→22.5），且不损害几何精度，验证了其跨基线泛化的必要性（Table 1）。
- **引导解码器**在GT潜码重构任务中将PSNR从30.2提升至34.3 dB（+4.1 dB），LPIPS相对改善35%，证明其有效绕过了标准VAE的信息瓶颈（Table 3）；在完整立体转换任务中使LPIPS降低16%，Matchability误差下降44%，且可作为即插即用组件提升M2SVid等基线方法（Table 4）。

### 方法定位

Elastic3D在立体视频生成方法谱系中占据独特位置：

| 维度 | 扭曲方法（SVG/StereoCrafter/M2SVid） | 免扭曲方法（Eye2Eye） | **Elastic3D** |
|------|--------------------------------------|----------------------|---------------|
| 生成范式 | 深度估计→扭曲→精修 | 两阶段像素空间扩散 | 单步前馈潜在空间生成 |
| 3D强度控制 | 间接（缩放深度图） | 无控制 | 标量视差条件$\delta$，无级连续可调 |
| 细节保真度 | 受限于修补能力 | 受限于像素空间扩散 | 极线注意力引导解码，直接从输入注入细节 |
| 几何来源 | 显式深度估计 | 隐式学习 | 隐式学习（偶有轻微几何幻觉） |

从知识库定位看，Elastic3D融合了视频潜在扩散模型（Video LDM）的高效生成先验与几何感知的特征注入机制，在免扭曲框架中首次实现了可控的立体视频生成。其引导解码器设计独立于生成网络，可作为通用模块即插即用地增强其他基于LDM的立体生成管线。

**局限性与待验证点**：模型对极端视差（基线>63mm）的泛化较弱；单一标量视差条件在动态场景（如变焦镜头）中可能产生歧义；隐式几何学习偶尔导致平坦表面的轻微“波浪”深度幻觉。这些需要在实际部署中结合场景特点进行验证。

## 背景与动机

立体视频（Spatial Video）正随着Apple Vision Pro、Meta Quest等设备的普及而成为沉浸式内容消费的核心媒介。然而，立体内容的创作仍然高度依赖专业双摄设备，导致高质量3D视频供给严重不足。单目转立体（mono-to-stereo）视频转换——从普通单视点视频生成对应的右眼视图——因此成为极具实用价值的研究方向。

### 现有方法的瓶颈

当前单目转立体方法的主流范式是**基于扭曲（warping-based）的管线**：先通过单目深度估计器从输入左视图提取深度图，再根据目标基线进行像素重投影生成右视图，最后用修复（inpainting）或扩散模型填补空洞和遮挡区域。代表性工作包括**SVG**（Yu et al., 2024）、**StereoCrafter**（2024）、**M2SVid**（Ye et al., 2024）以及**ReStereo**等。这一范式存在两个根本性缺陷：

1. **扭曲伪影不可避免**：重投影步骤对深度估计误差高度敏感，尤其在遮挡边界和细薄结构处，容易产生空洞、撕裂和几何失真。后续修复步骤虽然能部分掩盖这些伪影，但无法从根本上恢复被遮挡区域的真实纹理。

2. **VAE信息瓶颈导致细节丢失**：近年兴起的潜在扩散模型（LDM）方法将生成过程迁移到压缩潜在空间以提高效率，但标准视频扩散模型的自编码器（VAE）压缩比高达1:48，在编码-解码过程中会不可逆地丢失高频纹理细节。这一瓶颈在立体场景中尤为致命——左右眼视图间的纹理不一致会直接引发**双眼竞争（binocular rivalry）**，严重破坏观看舒适度。

此外，**Eye2Eye**（2024）虽然提出了一种免扭曲的两阶段像素空间扩散方法，避免了深度估计的依赖，但该方法完全缺失对3D强度的控制能力，用户无法调节立体效果的强弱，限制了实际部署的灵活性。

### 本文动机与核心思路

针对上述问题，Elastic3D提出了一种**直接、免扭曲、前馈的潜在空间立体视频生成框架**，其核心设计围绕三个关键洞察展开：

- **绕过深度估计与扭曲**：在潜在扩散框架中完全摒弃显式深度估计和像素重投影步骤，直接从输入左视图的潜在表示生成右视图潜在表示，从根源上消除扭曲伪影。

- **标量视差条件实现无级3D控制**：引入中值视差因子 $\delta$ 作为3D强度的直观控制旋钮——用户仅需设定一个标量即可连续调节立体效果的强弱，无需操作深度图或复杂参数。

- **左视图引导的VAE解码器恢复高频细节**：设计一个包含极线交叉注意力机制的引导解码器 $\mathcal{D}'$，在解码阶段直接从输入左视图 $V_L$ 的多尺度特征中提取高频信息并注入右视图重建过程，有效绕过标准VAE的压缩瓶颈，显著缓解双眼竞争。

通过这三项设计的协同，Elastic3D在多个在野数据集上实现了对传统扭曲方法和免扭曲基线的全面超越，同时保持了直观的用户控制能力。

## 核心创新

传统单目转立体视频方法的核心瓶颈在于对显式深度估计和像素扭曲（warping）的依赖，这一范式在遮挡区域和纹理稀疏处不可避免地产生空洞与伪影；同时，主流潜在扩散模型（LDM）中标准VAE的高压缩率（1:48）导致高频纹理信息在编解码过程中大量丢失，引发双眼竞争。Elastic3D 通过三个关键“changed slots”系统性地绕开了上述瓶颈，构成了其核心创新。

### 1. 免扭曲的直接潜在空间生成

Elastic3D 完全摒弃了传统的“深度估计→重投影→修复”管线，转而采用一种**直接、免扭曲的前馈生成范式**。其合成网络 $f_\theta$ 以零噪声 $\mathbf{0}$、输入左视图的潜在表示 $z_L$ 和视差条件令牌 $\tau(\delta)$ 为输入，在单次前向传播中直接预测右视图的潜在表示：
$$\hat{z}_R = f_\theta(\mathbf{0}, z_L, \tau(\delta))$$

这一设计使得模型无需显式建模深度或执行逐像素扭曲操作，从而从根源上消除了遮挡空洞和几何错位等扭曲伪影。消融实验证实了该范式的优势：在 AVP 数据集上，免扭曲方案相比基于扭曲的基线获得了 **+1.4 dB PSNR** 的提升，同时视差误差从 2.33 降至 **1.74**（Tab. 2）。与 **SVG**（Yu et al., 2024）、**StereoCrafter**（2024）、**M2SVid**（Ye et al., 2024）等扭曲-修复两阶段方法相比，Elastic3D 的端到端前馈生成在结构简洁性和几何一致性上具有本质优势。

### 2. 标量视差条件：直观的3D强度控制旋钮

现有方法对立体效果强度的控制存在明显缺陷：扭曲方法需通过缩放深度图间接调节，操作不直观且可能引入几何畸变；而免扭曲方法 **Eye2Eye**（2024）则完全丧失了控制能力，限制了实用性。Elastic3D 引入了一个**标量中值视差条件 $\delta$**，定义为左视图到右视图第一帧视差图的中值：
$$\delta = \mathrm{P}_{50}(D_{LR}^0)$$

该标量被编码为条件令牌 $\tau(\delta)$ 注入合成网络，为用户提供了一个连续、直观的“3D强度旋钮”。训练时通过对真实视差图进行随机缩放增强，使模型学会响应不同的视差水平。这一设计的决定性证据来自跨基线泛化实验：在分布外的 iPhone Spatial Video 数据集上，移除视差条件导致 PSNR 从 22.5 dB 骤降至 **18.7 dB**（−3.8 dB），而视差误差几乎不变（Tab. 1），表明条件机制在不损害几何精度的情况下提供了必要的3D强度控制，是模型跨设备泛化的关键使能器。

### 3. 极线注意力引导的VAE解码器

标准 Stable Video Diffusion 的 VAE 解码器将潜在表示上采样 48 倍以恢复像素级视频，这一过程构成了严重的信息瓶颈——即使输入 GT 右视图的潜在码，重构 PSNR 也仅为 30.2 dB，高频纹理大量丢失（Tab. 3, Fig. 4）。Elastic3D 提出的**引导解码器 $\mathcal{D}'$** 通过极线交叉注意力机制，直接从输入左视图 $V_L$ 的多尺度特征中提取高频细节，注入右视图的解码过程：
$$h_i'(p) = h_i(p) + \mathcal{A}_{\mathrm{epipolar}}(h_i(p), g_i)$$

其中 $h_i(p)$ 为解码器第 $i$ 层在位置 $p$ 的特征，$g_i$ 为对应层的左视图引导特征，$\mathcal{A}_{\mathrm{epipolar}}$ 沿核极线执行一维交叉注意力。这一设计将注意力矩阵的内存需求从标准二维注意力的 128 GB 降至 **256 MB**，使得高分辨率引导在计算上可行。

引导解码器的有效性在多个层面得到验证：
- **重构任务**：单独解码 GT 潜码时，PSNR 从 30.2 dB 提升至 **34.3 dB**（+4.1 dB），LPIPS 相对改善 **35%**（Tab. 3）。
- **端到端立体转换**：LPIPS 降低 **16%**，Matchability 误差（双眼竞争代理指标）下降 **44%**（Tab. 4）。
- **即插即用泛化**：将引导解码器 $\mathcal{D}'$ 接入 **M2SVid** 基线，同样带来一致的性能增益（Tab. 4），证明其模块化设计可独立于合成网络发挥作用。

### 创新总结

Elastic3D 的三个 changed slots 形成了协同增效的创新闭环：免扭曲生成消除了几何伪影的源头，视差条件赋予了跨场景的可控泛化能力，引导解码器则弥补了潜在扩散模型固有的细节损失。这一组合使得模型在 AVP 数据集上以 **25.9 PSNR / 0.196 LPIPS** 全面超越所有基线（Tab. 5），同时保持了从零噪声单步前馈的推理效率。

## 整体框架

Elastic3D 是一个直接、免扭曲（warping-free）的前馈立体视频转换框架。给定一段左眼视频 $V_L \in \mathbb{R}^{N \times H \times W \times 3}$，系统通过三个级联模块一次性生成对应的右眼视频 $\hat{V}_R$，全程无需显式深度估计或像素重投影。

**Pipeline 总览**

整个推理流程可概括为以下公式：

$$
\hat{V}_R = \mathcal{D}'(f_\theta(\mathbf{0}, z_L, \tau(\delta)), V_L), \quad z_L = \mathcal{E}(V_L)
$$

三个核心模块依次为：

1. **VAE 编码器 $\mathcal{E}$**  
   冻结的 Stable Video Diffusion 编码器将输入左视图 $V_L$ 压缩到潜在空间，得到 $z_L$。该压缩过程存在约 1:48 的空间降采样，是后续高频细节丢失的根本瓶颈。

2. **合成网络 $f_\theta$**  
   基于 Stable Video Diffusion 架构的前馈生成器，以零噪声 $\mathbf{0}$、左视图潜在 $z_L$ 和视差令牌 $\tau(\delta)$ 为条件，直接预测右视图潜在表示 $\hat{z}_R = f_\theta(\mathbf{0}, z_L, \tau(\delta))$。该模块完全在潜在空间中操作，绕过了传统方法中“深度估计→扭曲→修补”的级联误差。

3. **引导解码器 $\mathcal{D}'$**  
   修改版 VAE 解码器，同时接收生成的右视图潜在 $\hat{z}_R$ 和原始左视图 $V_L$ 作为输入。通过极线交叉注意力机制，解码器从 $V_L$ 的多尺度特征中提取高频纹理信息，注入到右视图的重建过程中，从而绕过标准 VAE 的信息瓶颈。

**输入输出流**

- **输入**：单目左眼视频 $V_L$，以及一个标量中值视差 $\delta$（作为 3D 强度的控制旋钮）。
- **输出**：高保真右眼视频 $\hat{V}_R$，其立体强度由 $\delta$ 连续调节。
- **数据流**：$V_L \xrightarrow{\mathcal{E}} z_L \xrightarrow{f_\theta(\cdot, z_L, \tau(\delta))} \hat{z}_R \xrightarrow{\mathcal{D}'(\cdot, V_L)} \hat{V}_R$。

**关键设计决策**

- **免扭曲范式**：$f_\theta$ 不依赖任何深度估计或像素扭曲操作，从根本上消除了遮挡区域的空洞和撕裂伪影。这一选择在 AVP 数据集上带来了 +1.4 dB PSNR 的提升，并将视差误差从 2.33 降至 1.74（Tab. 2）。
- **视差条件注入**：标量 $\delta = \mathrm{P}_{50}(D_{LR}^0)$（首帧左右视差图的中值）通过可学习的令牌 $\tau(\delta)$ 注入合成网络，使用户能以直观、连续的方式控制立体效果强度。消融实验表明，该条件在分布外数据集（iPhone Spatial Video）上贡献了 +3.8 dB PSNR 的跨基线泛化增益（Tab. 1）。
- **引导解码的模块化设计**：$\mathcal{D}'$ 与 $f_\theta$ 分开训练，可即插即用地提升其他方法（如 M2SVid）的性能——替换其标准解码器后，LPIPS 降低 16%，Matchability 误差下降 44%（Tab. 4）。当前受限于 GPU 内存，联合训练尚不实用，但模块化设计为未来的端到端优化保留了空间。

### 补充图表

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/002_Figure_2.jpg]]
*Figure 2: Inference Pipeline.A frozen VAE Encoderε computes the latent code*

## 核心模块与公式推导

### 整体推理管线

Elastic3D 的推理流程由三个核心模块串联构成，整体公式为：

$$\hat{V}_R = \mathcal{D}'(f_\theta(\mathbf{0}, z_L, \tau(\delta)), V_L), \quad z_L = \mathcal{E}(V_L)$$

其中 $V_L \in \mathbb{R}^{N \times H \times W \times 3}$ 为输入左眼视频（$N$ 帧，分辨率 $H \times W$），$\hat{V}_R$ 为生成的右眼视频。三个模块依次为：

1. **VAE 编码器 $\mathcal{E}$**：将左视图视频压缩至潜在空间，得到 $z_L$。
2. **合成网络 $f_\theta$**：以前馈方式从零噪声、$z_L$ 和视差令牌 $\tau(\delta)$ 直接生成右视图潜在表示 $\hat{z}_R$。
3. **引导解码器 $\mathcal{D}'$**：融合 $\hat{z}_R$ 与原始左视图 $V_L$ 的高频细节，输出最终右视图视频。

该管线完全绕过深度估计与扭曲步骤，在潜在扩散框架内实现端到端的前馈立体生成。

### 模块一：VAE 编码器

采用冻结的 Stable Video Diffusion 标准 VAE 编码器，将输入左视图视频 $V_L$ 压缩为潜在表示 $z_L$。该编码器的高压缩比（约 1:48）虽利于扩散模型训练，但会丢失高频纹理细节——这一瓶颈正是后续引导解码器所要解决的核心问题。

### 模块二：合成网络 $f_\theta$ 与视差条件

合成网络基于 Stable Video Diffusion 架构，以单步前馈方式生成右视图潜在表示：

$$\hat{z}_R = f_\theta(\mathbf{0}, z_L, \tau(\delta))$$

其中 $\mathbf{0}$ 表示零噪声初始化（推理时无需扩散去噪），$\tau(\delta)$ 为视差条件令牌。视差因子 $\delta$ 定义为左视图到右视图第一帧视差图的中值：

$$\delta = \mathrm{P}_{50}(D_{LR}^0)$$

该标量通过傅里叶特征编码后注入合成网络，作为控制立体强度的直观旋钮（Figure 3）。训练时，通过对真实视差图 $D_{LR}^0$ 随机缩放因子 $s$ 并前向扭曲生成新的右视图真值，使模型学习视差条件的连续响应。

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/003_Figure_3.jpg]]
*Figure 3: The strength of the stereo effect can be controlled by varying the parameter δ that acts as a conditioning for the median disparity of the generated video (see Sec. 4.2)*

### 模块三：引导解码器 $\mathcal{D}'$ 与极线注意力

标准 VAE 解码器仅从潜在表示 $\hat{z}_R$ 重建图像，受限于压缩瓶颈，高频细节严重丢失（Figure 4）。引导解码器 $\mathcal{D}'$ 通过极线交叉注意力机制，直接从输入左视图 $V_L$ 提取多尺度特征并注入解码过程。

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/004_Figure_4.jpg]]
*Figure 4: Decoding the ground truth latent. The compression with the standard VAE of an LDMis unsuitable for discriminative tasks*

设 $h_i(p)$ 为解码器第 $i$ 层在像素位置 $p$ 的特征，$g_i$ 为对应尺度的左视图特征，极线注意力的残差更新为：

$$h_i'(p) = h_i(p) + \mathcal{A}_{\mathrm{epipolar}}(h_i(p), g_i)$$

$\mathcal{A}_{\mathrm{epipolar}}$ 沿核极线执行一维交叉注意力：以 $h_i(p)$ 为查询，仅在 $p$ 对应的极线上与 $g_i$ 的特征进行注意力计算。这一设计将 16 位注意力矩阵的显存需求从 128 GB 降至 256 MB，使高分辨率特征融合成为可能。引导解码器独立于合成网络训练，可即插即用地提升其他基线方法（如 M2SVid）的细节恢复能力。

## 实验与分析

### 评估协议与基准

实验在统一的“黑盒”协议下进行：所有方法在推理时仅以单目左视图作为输入，不依赖任何额外的深度或位姿信息。对于基于扭曲（warping）的基线方法，使用 **DepthCrafter** 提取相对深度并进行尺度对齐；对于 Elastic3D，使用真实中值视差 $\delta$ 作为条件信号。

评估覆盖三个数据集：
- **Stereo4D**（测试集）：训练分布内数据，用于验证核心能力。
- **Apple Vision Pro Spatial Video (AVP)**：基线分布与训练集相似，但视频内容为分布外。
- **iPhone Spatial Video**：相机标定与视频内容均为分布外，用于检验跨基线泛化能力。

评估指标包括像素级质量（PSNR、SSIM、LPIPS）、立体感知保真度（Matchability Error $\mathcal{E}_{\mathrm{Match}}$、P-PSNR）和几何精度（视差误差 Disp.err、时序一致性 Temp.err）。其中 Matchability Error 定义为基于一致性匹配点的 Jaccard 距离，直接量化双眼竞争程度：

$$\mathcal{E}_{\mathrm{Match}} = 1 - \frac{|M_{gt} \cap M_{pred}|}{|M_{gt} \cup M_{pred}|}$$

### 主要结果：与 SOTA 的全面对比

**AVP 数据集**（Table 5）上，Elastic3D 以 **25.9 PSNR / 0.894 SSIM / 0.196 LPIPS** 全面优于所有基线。相比最强基线 **M2SVid**（Ye et al., 2024），PSNR 提升 1.5 dB，LPIPS 降低 11%，Matchability 误差从 41.5 降至 30.9（**降低 25%**），视差误差从 2.30 降至 1.74。扭曲基线 **StereoCrafter**（2024）和 **SVG**（Yu et al., 2024）的 LPIPS 分别为 0.223 和 0.221，Matchability 误差高达 42.0 和 41.0，表明扭曲伪影导致的双眼竞争问题严重。免扭曲的 **Eye2Eye**（2024）因缺乏 3D 强度控制，Matchability 误差为 36.4，PSNR 仅 24.6。

**Stereo4D 测试集**（Table 6）上，Elastic3D 达到 **26.1 PSNR / 0.913 SSIM / 0.176 LPIPS**，Matchability 误差 27.8，相比 M2SVid（39.6）**降低 30%**，证明在分布内数据上同样具有显著优势。

**iPhone 数据集**（Table 7）上，Elastic3D 的 PSNR 为 22.5，略低于 M2SVid（22.9），但 SSIM 高出 0.025，LPIPS 降低 0.012，Matchability 误差从 38.4 降至 26.5（**降低 31%**）。PSNR 的轻微劣势主要源于 iPhone 的宽基线（>63mm）超出了训练分布，但感知质量和立体一致性指标仍显著领先。

### 消融实验：因果机制的逐层验证

#### 视差条件：跨基线泛化的关键旋钮

Table 1 展示了视差条件 $\delta$ 的消融效果。在分布内 Stereo4D 上，去除条件使 PSNR 从 26.1 降至 25.1（-1.0 dB），Matchability 从 27.8 升至 29.8。在分布外 iPhone 数据上，差距急剧扩大：PSNR 从 22.5 暴跌至 18.7（**-3.8 dB**），Matchability 从 26.5 升至 30.5。这证明标量视差条件不仅是 3D 强度的控制接口，更是模型跨基线泛化的必要条件——没有该条件，模型在未见过的相机基线上完全失效。值得注意的是，去除条件并未损害几何精度（Disp.err 保持 0.77），说明条件机制主要影响生成质量而非隐式几何学习。

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/005_Table_1.jpg]]
*Table 1: ． Impact of our conditioning approach (Sec.4.2） on Stereo4D [23] (top) and iPhone Spatial Video [22] (bottom)*

#### 免扭曲范式：从根源消除伪影

Table 2 将 Elastic3D 的免扭曲生成与基于扭曲的变体进行对比（AVP 数据集）。扭曲基线使用 DepthCrafter 估计深度后重投影，PSNR 为 24.5，视差误差 2.33。Elastic3D 的直接生成将 PSNR 提升至 25.9（**+1.4 dB**），视差误差降至 1.74。扭曲方法在遮挡边界和深度不连续区域产生空洞和拉伸伪影，而免扭曲方法通过隐式学习场景几何避免了这些问题。

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/006_Table_2.jpg]]
*Table 2: Impact of warping free paradigm (Sec.4.1) on the Apple Vision Pro Spatial Video dataset [22]*

#### 引导解码器：突破 VAE 信息瓶颈

引导解码器 $\mathcal{D}'$ 的消融分两步验证。

**重构实验**（Table 3）：将 GT 右视图通过标准 Stable Video Diffusion VAE 编码-解码，PSNR 仅 30.2 dB，LPIPS 高达 0.195，说明 1:48 的高压缩比导致严重细节丢失。引入引导解码器后，PSNR 跃升至 34.3 dB（**+4.1 dB**），LPIPS 降至 0.127（**相对改善 35%**），SSIM 从 0.923 提升至 0.961。这证明极线注意力机制能有效从左视图注入高频纹理，绕过潜在空间的信息瓶颈。

**端到端立体转换**（Table 4）：在完整任务中，引导解码器使 LPIPS 从 0.193 降至 0.162（**降低 16%**），Matchability 误差从 49.8 降至 27.8（**降低 44%**）。更重要的是，将引导解码器即插即用地接入 **M2SVid** 后，其 LPIPS 从 0.206 降至 0.191，Matchability 从 39.6 降至 35.4，验证了该模块的通用性和独立价值。

### 失败模式与局限性

1. **极端视差泛化不足**：iPhone 数据集（基线 >63mm）上 PSNR 略低于 M2SVid，说明训练数据（Stereo4D 基线约 63mm）的视差分布限制了模型对宽基线场景的适应能力。扭曲方法在此类场景仍保有优势。
2. **几何幻觉**：模型隐式学习几何，偶尔在平坦表面（如墙壁、桌面）产生轻微的“波浪”深度，几何刚性弱于显式深度估计方法。这源于免扭曲框架缺乏显式的平面一致性约束。
3. **全局条件的歧义性**：单一标量 $\delta$ 在场景几何动态变化时（如变焦镜头、大景深变化）无法反映局部深度差异，可能产生全局一致的视差但局部不准确的立体效果。
4. **长视频与高分辨率限制**：当前实现受 GPU 内存约束（单 H100 约 45 帧 @512×512），需依赖时间自回归和空间平铺策略，推理效率有待优化。

### 人类感知研究

Table 9 的配对人类感知研究中，参与者在 Elastic3D 与 M2SVid 的比较中 **63.6% 偏好 Elastic3D**，仅 18.2% 偏好 M2SVid；在与 Eye2Eye 的比较中 **54.5% 偏好 Elastic3D**，31.8% 认为两者持平。这验证了自动指标（特别是 Matchability 和 LPIPS 的显著改善）与人类对立体舒适度和纹理保真度的主观感知高度一致。

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/019_Table_9.jpg]]
*Table 9: ResultsofPairwiseHumanPerceptionStudy.PrtcipantscomparedElastic3Dagainsttwoothermethods: M2SVidandEye2Eye. The table shows the number oftimes (%of total for each row)each method was preferred,orifthey were rated as equal*

### 补充图表

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/007_Table_5.jpg]]
*Table 5: State-of-the-art comparison on the Apple Vision Pro Spatial Video dataset [22]. The baseline of the dataset is similar to during training while the content is out-of-distribution*

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/008_Table_3.jpg]]
*Table 3: Reconstruction results on Stereo4D[23],where the VAE is applied on the ground truth right views*

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/009_Table_4.jpg]]
*Table 4: ．Impact of our guided-VAE decoder*

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/011_Table_6.jpg]]
*Table 6: State-of-the-art comparison on the Stereo4D [23] test set*

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/012_Table_7.jpg]]
*Table 7: State-of-the-art comparison on the iPhone portion of Spatial Video dataset [22].Both calibration and video content are out-of-distribution*

![[assets/figures/papers/paper_list_l2473_https_arxiv_org_abs_2512_14236/figures/023_Table_12.jpg]]
*Table 12: Model Latency Comparison.Runtimes are measured for generating a video of 16 frames with a resolution of 512 × 512. All evaluations were performed on an NVIDIA H10o GPU.“Monodepth”and“Warp”denote the time taken for depth estimation and geometric warping,respectively*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

Elastic3D 的提出建立在立体视频转换领域两条技术路线的基础之上：**基于扭曲（warping-based）的显式深度估计与重投影方法**，以及**免扭曲（warping-free）的端到端生成方法**。

**基于扭曲的方法**构成了当前的主流范式。这类方法首先从单目左视图估计深度图，然后通过前向或后向重投影生成右视图，最后对遮挡区域和空洞进行修补（inpainting）或扩散精炼。代表性工作包括：
- **SVG**（Yu et al., 2024）：采用扭曲加修补的精炼策略。
- **StereoCrafter**（2024）与 **M2SVid**（Ye et al., 2024）：在扭曲基础上引入潜在扩散模型进行精炼，提升纹理质量和时序一致性。
- **ReStereo**：结合重建与修补的扭曲方法。

这些方法的**根本瓶颈**在于对显式深度估计的依赖：深度估计误差会直接传播到重投影步骤，产生遮挡区域的空洞和几何伪影，且扭曲操作本身在纹理薄弱或深度不连续区域易引入拉伸和撕裂。

**免扭曲的方法**试图绕过深度估计，直接从输入视图生成目标视图。**Eye2Eye**（2024）是这一方向的代表，采用两阶段像素空间扩散模型，完全免除了扭曲步骤。然而，Eye2Eye 缺乏对立体效果强度的控制能力——用户无法调节生成内容的3D深度感，这严重限制了其实用性。

Elastic3D 在免扭曲范式的基础上做出了**三个关键改进**，形成了与两类基线工作的本质区别：

| 维度 | 扭曲方法（SVG/StereoCrafter/M2SVid） | Eye2Eye | **Elastic3D** |
|------|--------------------------------------|---------|---------------|
| 生成范式 | 扭曲+精炼（依赖深度估计） | 免扭曲像素空间扩散 | **免扭曲潜在空间前馈生成** |
| 3D强度控制 | 间接（缩放深度图） | 无控制 | **标量中值视差条件 δ** |
| 细节恢复 | 依赖扭曲精度 | 依赖扩散生成 | **左视图引导VAE解码器** |

**证据支撑**：消融实验（Tab. 2）表明，免扭曲的直接生成范式在AVP数据集上相比扭曲基线带来 +1.4 dB PSNR 提升，视差误差从 2.33 降至 1.74，证实了绕过深度估计的优越性。在完整系统对比中（Tab. 5），Elastic3D 以 25.9 PSNR / 0.196 LPIPS 全面优于 M2SVid（24.4 / 0.221）和 Eye2Eye 等所有基线。

### 2. 适用边界

Elastic3D 的核心设计假设决定了其适用范围和局限性：

**适用场景**：
- 与训练数据基线分布相近的立体视频转换（Stereo4D、AVP Spatial Video 等数据集）。
- 用户需要灵活调节立体效果强度的应用场景（如内容创作、后期制作），通过标量 δ 实现从平面到夸张深度的连续控制。
- 对纹理细节和双眼舒适度要求较高的场景，引导解码器能有效抑制双眼竞争。

**不适用或性能退化的边界**：
1. **极端视差场景**（基线 > 63mm）：模型在超出训练分布的宽基线条件下泛化能力较弱，此时基于扭曲的方法可能因显式几何建模而更具优势。这一限制源于训练数据中视差分布的覆盖范围。
2. **动态变焦或景深剧烈变化的镜头**：单一标量中值视差条件 δ 是全局量，无法反映场景内空间变化的深度结构。在变焦镜头或前景/背景深度差异极大的场景中，全局条件可能产生歧义。
3. **长视频与高分辨率推理**：受 GPU 内存限制（单 H100 约支持 45 帧 @ 512×512），当前实现需要时间自回归和空间平铺等工程策略，尚未实现原生的任意长度/分辨率支持。
4. **对几何精度要求极高的应用**：模型隐式学习几何关系，偶尔在平坦表面产生“波浪”深度幻觉，几何刚性弱于基于显式深度估计的扭曲方法。

### 3. 局限与开放问题

**已知局限**（论文明确讨论或实验揭示）：

1. **GPU内存瓶颈**：UNet 和引导解码器目前分开训练，联合训练因内存过高而不实用。推理时，长视频需时间自回归，高分辨率需空间平铺，限制了端到端的效率。当前模块化设计允许解码器即插即用，但未能实现联合优化。
2. **极线注意力实现效率**：引导解码器中的极线交叉注意力以 Python 行循环实现，存在解释器开销，未能完全发挥 GPU 吞吐量。论文指出需要定制 CUDA 内核来加速。
3. **全局条件的歧义性**：标量 δ 作为全局条件，无法表达空间变化的视差分布，在复杂场景中可能产生几何歧义。
4. **几何幻觉**：模型在平坦表面偶尔产生轻微深度波动，缺乏显式几何约束。

**开放问题**（从局限中自然引申，供后续工作参考）：

1. **高效推理架构**：如何设计高效的时间自回归和空间平铺策略，使模型原生支持任意长度和高分辨率的立体视频生成？定制 CUDA 核实现并行极线注意力后，推理延迟能降低多少？能否满足实时系统部署需求？
2. **宽基线泛化**：能否通过增加宽基线训练数据或引入条件生成策略（如基线距离条件），提高对极端视差的泛化能力？
3. **条件表示改进**：如何改进视差条件表示——例如空间变化的条件图、动态序列条件、或从输入视频中预测的视差先验——以消除全局标量在复杂场景中的歧义？
4. **弱几何先验融合**：是否可以在免扭曲框架中引入弱几何先验（如平面一致性约束、极线几何正则化），以减少几何幻觉，同时保持免扭曲的灵活性？
5. **端到端联合训练**：在更好的硬件条件下，联合训练 UNet 和引导解码器能否实现端到端优化的质量收益？当前模块化设计的性能上限在哪里？
6. **与其他基线的即插即用集成**：Tab. 4 已证明引导解码器对 M2SVid 有即插即用增益（LPIPS 降低，Matchability 误差下降 44%）。这一模块能否泛化到更广泛的立体生成框架中，成为通用组件？

## 原文 PDF

![[paperPDFs/CVPR_2026/Elastic3D_Controllable_Stereo_Video_Conversion_with_Guided_Latent_Decoding.pdf]]
---
title: "Robust3DGSW: Toward Robust Watermarking for Quantization-Aware 3D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Robust3DGSW_Toward_Robust_Watermarking_for_Quantization_Aware_3D_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- Robust3DGSW
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 中频带水印嵌入与多尺度对抗扰动配合的渐进量化感知双解码训练。
primary_logic: 在中频带（既非视觉重要又非量化敏感的频带）嵌入水印，并通过渐进式从高到低比特的量化感知训练，使双解码器能够从量化噪声中准确恢复水印信号，从而同时保障水印鲁棒性和渲染质量。
claims:
- 从32位到4位量化，3D-GSW的准确率从98%骤降至61%，而Robust3DGSW仅从99.78%降至87.51%，展示了对量化的鲁棒性。
- 4位量化下，3D-GSW的PSNR仅10dB，Robust3DGSW达到20.46dB，证明量化感知设计对渲染质量的保护。
- 消融研究证实，移除中频嵌入或渐进训练后，4位量化下水印准确率大幅下降，说明各组件对鲁棒性的关键作用。
- Blender, LLFF, MipNeRF360 (平均) 上 Bit Accuracy (无量化) = 99.78%
---

# Robust3DGSW: Toward Robust Watermarking for Quantization-Aware 3D Gaussian Splatting

> [!tip] 核心洞察
> 在中频带（既非视觉重要又非量化敏感的频带）嵌入水印，并通过渐进式从高到低比特的量化感知训练，使双解码器能够从量化噪声中准确恢复水印信号，从而同时保障水印鲁棒性和渲染质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Robust3DGSW：面向量化感知的3D高斯泼溅鲁棒水印 |
| 英文题名 | Robust3DGSW: Toward Robust Watermarking for Quantization-Aware 3D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Robust3DGSW_Toward_Robust_Watermarking_for_Quantization-Aware_3D_Gaussian_Splatting_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Robust3DGSW |
| Dataset | Blender, LLFF, MipNeRF360 |

> [!tip] 效果简介
> - Blender, LLFF, MipNeRF360 (平均) 上，Bit Accuracy (无量化) 99.78% vs 98% (3D-GSW) (+1.78%)；Bit Accuracy (4-bit 量化) 87.51% vs 61% (3D-GSW) (+26.51%)；PSNR (4-bit 量化) 20.46 dB vs 10 dB (3D-GSW) (+10.46 dB)。

## 概要

3D高斯泼溅（3D Gaussian Splatting, 3DGS）已成为高质量新视角合成的主流方案，但其模型文件体积庞大，量化压缩成为实际部署的必然选择。然而，现有的3DGS水印方法（如 **3D-GSW**（Jang et al., CVPR 2025）、**GaussianMarker**（Huang et al., NeurIPS 2024））在设计时均未考虑量化带来的信号损失，导致在低比特量化场景下出现两个严重问题：水印提取精度急剧下降，以及渲染图像质量大幅受损。如 Figure 1 所示，3D-GSW在32位精度下水印准确率达98%，但降至4位量化时骤降至61%；同时，其渲染PSNR从约35 dB暴跌至仅10 dB，几乎丧失实用性。

针对这一瓶颈，本文提出 **Robust3DGSW**——一种面向量化感知的两阶段3DGS水印框架。其核心思路是：**在中频带（既非视觉敏感又非量化敏感的频率区间）嵌入水印，并通过渐进式量化感知的双解码器训练，使水印信号能够在极端量化噪声下被稳定恢复。** 具体而言，第一阶段在3D高斯位置的DCT系数和渲染图像的FFT系数中频带上注入水印噪声，以平衡不可感知性与量化鲁棒性；第二阶段采用2D HiDDeN与3D PointNet双解码器架构，配合多尺度对抗扰动和从高比特到低比特的渐进式量化训练，使解码器学会从量化误差中准确提取水印。

实验结果表明，Robust3DGSW在三个标准基准（Blender、LLFF、MipNeRF360）上实现了显著突破：无量化条件下位准确率达99.78%，超越基线3D-GSW的98%；在4位极端量化下，位准确率仍保持87.51%（提升26.51个百分点），渲染PSNR达20.46 dB（提升10.46 dB），证明了量化感知设计对水印鲁棒性和渲染质量的双重保护。消融研究进一步验证了中频嵌入、渐进训练和多尺度对抗扰动等各组件的关键作用。



3D高斯泼溅（3D Gaussian Splatting, 3DGS）作为一种显式神经渲染技术，凭借其高质量实时渲染能力，正在成为3D内容创作与分发的主流表示形式。随着3DGS资产在数字市场中快速流通，版权保护问题日益突出——创作者需要一种可靠的水印机制来声明所有权并追踪未经授权的分发。为此，研究者们提出了多种面向3DGS的水印方法，如**3D-GSW**（Jang et al., CVPR 2025）和**GaussianMarker**（Huang et al., NeurIPS 2024），它们能够在3D高斯场景中嵌入水印并在渲染图像中提取水印信息。

然而，现有水印方法在设计时普遍忽略了一个关键的实际约束：**模型量化**。为了在边缘设备上高效部署和传输，3DGS模型通常需要从32位浮点精度压缩至8位甚至4位整数精度。量化操作会对3D高斯参数（包括水印嵌入载体）引入不可逆的信息损失，这对水印的鲁棒性构成了严峻挑战。

**量化对水印的破坏性影响**在现有方法中表现得尤为突出。以3D-GSW为例，当量化位宽从32位降至4位时，其水印提取准确率从98%骤降至61%，渲染图像的PSNR也从35 dB暴跌至10 dB（见Figure 1）。这一现象揭示了现有方法的根本缺陷：它们将水印信息嵌入在量化敏感的参数空间或频带中，导致低比特量化时水印信号被量化噪声淹没，同时渲染质量也遭受严重破坏。

问题的核心在于**水印嵌入位置与量化误差分布之间的失配**。量化操作本质上是一种高频截断过程——低比特量化会优先丢弃参数中的高频细节分量，而传统水印方法恰恰倾向于在高频带或全空间域中嵌入水印，使得水印信息在量化后大量丢失。与此同时，水印嵌入对高斯参数的扰动也会在量化过程中被放大，进一步恶化渲染质量。

Robust3DGSW正是针对这一瓶颈而提出。其核心洞察是：**在中频带嵌入水印**——这一频带既非视觉感知最敏感的低频区域，也非量化最先丢弃的高频区域——能够使水印信号在量化过程中得以保留，同时最小化对渲染质量的负面影响。配合**渐进式量化感知训练**和**双解码器架构**，Robust3DGSW能够从量化噪声中稳定恢复水印信息，在4位极端量化下仍保持87.51%的提取准确率和20.46 dB的渲染PSNR，相比3D-GSW分别提升了26.51个百分点和10.46 dB。



## 核心方法与创新机理

Robust3DGSW 的核心创新在于构建了一套**量化感知的中频带水印嵌入与渐进式双解码器训练框架**，从根本上解决了现有3DGS水印方法在模型量化场景下的双重困境——水印提取精度崩溃与渲染质量急剧退化。

### 创新一：中频带双域水印嵌入

现有3DGS水印方法（如 **3D-GSW**，Jang et al., CVPR 2025）通常在全空间域或高频带嵌入水印，未考虑量化对信号分布的差异化影响。Robust3DGSW 的关键洞察在于：**低频带承载视觉核心信息，高频带在量化中首先被丢弃，而中频带恰好处于“视觉容忍”与“量化幸存”的交叠区间**。

基于此，方法在两个模态上同步实施中频带嵌入：

- **3D域**：对3D高斯位置矩阵施加1D离散余弦变换（DCT），在中频系数区间 $[k_{\mathrm{low}}, k_{\mathrm{high}}]$ 上添加高斯噪声以嵌入水印，再通过逆DCT恢复带水印的空间坐标：
  $$\tilde{F}_{k,d}^{3D} = F_{k,d}^{3D} + \alpha_{3D} \cdot \mathcal{N}(0, \sigma_{3D}^2), \quad k \in [k_{\mathrm{low}}, k_{\mathrm{high}}]$$

- **2D域**：对渲染图像的每个颜色通道施加2D快速傅里叶变换（FFT），在中频环形区域 $[r_{\mathrm{low}}^2, r_{\mathrm{high}}^2]$ 内添加噪声，形成冗余嵌入：
  $$\tilde{F}_c^{2D}[u,v] = F_c^{2D}[u,v] + \alpha_{2D} \cdot \mathcal{N}(0, \sigma_{2D}^2)$$

这一双域中频策略的因果机制在于：3D域嵌入从源头保护水印信号免受高斯参数量化的直接侵蚀，2D域嵌入则在渲染管线的末端提供额外冗余，两者协同确保水印信号在量化压缩后仍可恢复。

### 创新二：多尺度对抗扰动机制

传统方法在解码器训练时仅使用干净或轻度失真的输入，导致解码器对量化噪声缺乏适应性。Robust3DGSW 在解码器训练阶段引入了**三类对抗性扰动**：

1. **频率域扰动**：对3D高斯特征施加DCT域噪声 $\epsilon_{\mathrm{DCT}}$，对渲染图像施加FFT域噪声 $\epsilon_{\mathrm{FFT}}$；
2. **量化噪声**：模拟目标位宽 $b(p)$ 下的量化操作 $\mathcal{Q}(\cdot, b(p))$ 及量化误差 $\mathcal{N}(0, \sigma_q(b))$；
3. **渲染级失真**：通过渲染扰动算子 $\mathcal{A}_{\mathrm{render}}$ 引入图像域退化。

扰动后的3D特征和渲染图像可统一表示为：
$$\tilde{\mathbf{f}}_{3D} = \mathcal{Q}(\mathbf{f}_{3D} + \epsilon_{\mathrm{DCT}}, b(p)) + \mathcal{N}(0, \sigma_q(b)), \quad \hat{\mathbf{I}} = \mathcal{A}_{\mathrm{render}}\big(\mathcal{Q}(\tilde{I}_{\mathrm{wm}} + \epsilon_{\mathrm{FFT}}, b(p))\big)$$

消融实验（Table 1）证实，移除多尺度对抗扰动后，裁剪失真下的水印准确率从82.79%骤降至65.78%，表明该机制是解码器获得失真鲁棒性的关键驱动力。

### 创新三：渐进式量化感知训练

直接在高位宽上训练的解码器在面对极端低位宽（如4-bit）时会出现严重的分布偏移。Robust3DGSW 采用**渐进式位宽调度**，按 $b(p)$ 从8-bit逐步降至4-bit，使解码器参数 $\theta_{\mathrm{dec}}$ 在训练过程中逐步适应逐渐增强的量化噪声：

$$\theta_{\mathrm{dec}}^* = \arg\min_{\theta} \mathbb{E}_{p \sim \mathcal{U}(0,1)} \left[ \mathcal{L}(\theta; b(p)) \right]$$

这一策略的因果效果极为显著：消融实验显示，移除渐进训练后，4-bit量化下的水印准确率从87.51%暴跌至67.42%，证明渐进式课程学习是应对极端量化不可或缺的手段。

### 创新四：双解码器架构与跨域一致性

Robust3DGSW 部署了**异构双解码器**——2D HiDDeN解码器处理渲染图像，3D PointNet解码器处理高斯特征——并通过跨域一致性损失对齐两者的输出：

$$\mathcal{L}_{\mathrm{cons}} = \| \sigma(\mathbf{w}_{2D}) - \sigma(\mathbf{w}_{3D}) \|^2$$

这一设计使得水印可以从两个互补的模态中独立提取，当某一域因量化或失真而退化时，另一域仍能提供可靠的水印信号，从而大幅提升整体鲁棒性。

### 创新总结

上述四个创新点构成了一个紧密耦合的系统：**中频带嵌入**确保水印信号位于量化幸存区间，**多尺度对抗扰动**赋予解码器对量化噪声和失真的预适应能力，**渐进式训练**通过课程学习平滑分布偏移，**双解码器一致性**提供跨模态冗余保障。这一组合使得Robust3DGSW在4-bit极端量化下仍能维持87.51%的水印准确率和20.46 dB的PSNR，而基线方法3D-GSW在同等条件下仅分别达到61%和10 dB。



Robust3DGSW 采用**两阶段**设计，将水印嵌入与量化感知解码器训练解耦，形成“嵌入—渲染—解码”的闭环流水线。整体结构如图2所示。

### 第一阶段：量化感知水印嵌入

该阶段在3D高斯场景重建的基础上，向**两个模态**的中频频带注入水印信号，以在渲染质量与量化鲁棒性之间取得平衡。

1. **3D高斯场景重建**：从多视角图像与对应相机位姿出发，使用原始3DGS方法重建场景的3D高斯表示。每个高斯原语由中心位置、协方差矩阵、颜色和不透明度等属性参数化，其数学形式为：
   $$
   \mathcal { G } _ { i } ( { \mathbf x } ) = e ^ { - \frac { 1 } { 2 } ( { \mathbf x } - { \pmb \mu } _ { i } ) ^ { \top } { \pmb \Sigma } _ { i } ^ { - 1 } ( { \mathbf x } - { \pmb \mu } _ { i } ) }
   $$
   渲染时通过α混合沿深度排序的高斯原语计算像素颜色：
   $$
   I [ x , y ] = \mathcal { R } ( \mathcal { G } , C _ { j } ) = \sum _ { i = 1 } ^ { N } \mathbf { c } _ { i } \alpha _ { i } \prod _ { k = 1 } ^ { i - 1 } ( 1 - \alpha _ { k } )
   $$

2. **3D频域水印嵌入**：对3D高斯的位置矩阵施加1D离散余弦变换（DCT），得到频域系数。在**中频带**（即视觉非重要且量化非敏感的区间）上添加高斯噪声以嵌入水印：
   $$
   \tilde { F } _ { k , d } ^ { 3 D } = F _ { k , d } ^ { 3 D } + \alpha _ { 3 D } \cdot \mathcal { N } ( 0 , \sigma _ { 3 D } ^ { 2 } ) , \quad k \in [ k _ { \mathrm { l o w } } , k _ { \mathrm { h i g h } } ]
   $$
   随后通过逆DCT将带水印的频域系数映射回空间坐标，得到带水印的3D高斯。

3. **2D频域水印嵌入**：利用带水印的3D高斯进行可微渲染，生成带水印的2D图像。对渲染图像的每个颜色通道施加2D快速傅里叶变换（FFT），在中频环形区域添加噪声，进一步提升水印冗余：
   $$
   \tilde { F } _ { c } ^ { 2 D } [ u , v ] = F _ { c } ^ { 2 D } [ u , v ] + \alpha _ { 2 D } \cdot \mathcal { N } ( 0 , \sigma _ { 2 D } ^ { 2 } ) , \quad ( u - u _ { c } ) ^ { 2 } + ( v - v _ { c } ) ^ { 2 } \in [ r _ { \mathrm { l o w } } ^ { 2 } , r _ { \mathrm { h i g h } } ^ { 2 } ]
   $$
   经逆FFT和ifftshift操作后得到最终的水印渲染图像。

**核心设计动机**：中频频带处于“感知容忍区”——低频承载视觉内容、高频易被量化截断，中频则能在嵌入水印时不显著损害渲染质量，同时保留对量化噪声的抵抗能力。这一双模态中频嵌入策略构成了Robust3DGSW应对量化的第一道防线。

### 第二阶段：渐进量化感知双解码器训练

该阶段训练两个并行的解码器（2D HiDDeN + 3D PointNet），使其能从量化噪声中准确恢复水印信号。

1. **多尺度对抗扰动**：在解码器训练过程中，对3D高斯特征和2D渲染图像同时注入三类扰动——频率域扰动（DCT/FFT噪声）、量化噪声和渲染级失真（如裁剪、模糊等），模拟极端量化下的信号退化：
   $$
   \tilde { \mathbf { f } } _ { 3 D } = \mathcal { Q } ( \mathbf { f } _ { 3 D } + \epsilon _ { \mathrm { D C T } } , b ( p ) ) + \mathcal { N } ( 0 , \sigma _ { q } ( b ) ) , \quad \hat { \mathbf { I } } = \mathcal { A } _ { \mathrm { r e n d e r } } \big ( \mathcal { Q } ( \tilde { I } _ { \mathrm { w m } } + \epsilon _ { \mathrm { F F T } } , b ( p ) ) \big )
   $$

2. **渐进式量化调度**：按照从高到低的位宽调度（8-bit → 4-bit）逐步降低量化比特，优化双解码器参数，使其渐进适应量化误差：
   $$
   \theta _ { \mathrm { d e c } } ^ { * } = \arg \underset { \theta } { \mathrm { m i n } } \mathbb { E } _ { p \sim \mathcal { U } ( 0 , 1 ) } \left[ \mathcal { L } ( \theta ; b ( p ) ) \right]
   $$

3. **双解码器架构**：
   - **2D解码器**：基于HiDDeN编码器加线性适配层，从归一化渲染图像中提取M位水印：$\mathbf { w } _ { 2 D } = \mathbf { A } _ { \mathrm { a d a p t } } \mathbf { H } _ { \mathrm { H i D D e N } } ( \mathbf { I } _ { \mathrm { n o r m } } )$
   - **3D解码器**：基于预训练PointNet处理14维高斯属性向量，经最大池化和MLP输出水印：$\mathbf { w } _ { 3 D } = \mathbf { M L P } ( \mathbf { M a x P o o l } ( \operatorname { P o i n t N e t } ( \mathbf { f } _ { 3 D } ) ) )$

4. **损失函数驱动优化**：整体训练目标由二元交叉熵损失（2D/3D解码器）、跨解码器一致性损失、位平衡损失和批一致性损失加权组合：
   $$
   \mathcal{L}_{\mathrm{total}} = \lambda_{2D} \mathcal{L}_{2D} + \lambda_{3D} \mathcal{L}_{3D} + \lambda_{\mathrm{cons}} \mathcal{L}_{\mathrm{cons}} + \mathcal{L}_{\mathrm{rec}}
   $$
   其中一致性损失 $\mathcal{L}_{\mathrm{cons}} = \| \sigma(\mathbf{w}_{2D}) - \sigma(\mathbf{w}_{3D}) \|^2$ 约束两个解码器输出对齐，保证跨域水印提取的稳定性。

### 数据流与模块关系

整体数据流可概括为：**多视角图像 → 3D高斯重建 → 3D DCT中频嵌入 → 带水印高斯渲染 → 2D FFT中频嵌入 → 水印图像 → 多尺度扰动注入 → 渐进量化解码器训练 → 双解码器水印提取**。两个阶段并非完全串行——第一阶段产生带水印的3D高斯和渲染图像，第二阶段在此基础上进行解码器训练，扰动和量化噪声仅在训练阶段施加，推理时解码器可直接从量化后的高斯和渲染图像中提取水印。

> **注意**：上述流水线描述基于论文Section 3.1–3.4及Figure 2的方法论陈述。由于论文元数据中venue/year字段为空，部分实现细节（如中频带具体范围、扰动强度超参数）需查阅原文确认。

### 补充图表

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/002_Figure_2.jpg]]
*Figure 2: Workflow of Robust3DGSW. Initially, we reconstruct 3D Gaussian representations from multiple image views and their corresponding camera poses using the 3DGS method. Next, to ensure watermark embedding is compatible with quantization, we introduce frequency-domain bands in two modalities. This process involves applying a 3D Discrete Cosine Transform (DCT) to the Gaussian positions to embed watermarks in the mid-frequency range, and applying a 2D Fast Fourier Transform (FFT) to the rendered images to embed watermarks in the mid-frequency spectrum. Lastly, during quantization-aware decoder training, we implement multi-scale adversarial perturbations to both the 3D Gaussians and the images befo...*



Robust3DGSW 的核心技术路线可分解为三个递进模块：**量化感知的中频带水印嵌入**、**多尺度对抗扰动生成**，以及**渐进式双解码器训练**。以下逐一展开其公式机理与变量含义。

### 3D 高斯场景重建与渲染基础

方法建立在原始 3DGS 的表示之上。场景由 $N$ 个 3D 高斯原语构成，第 $i$ 个高斯原语定义为：

$$
\mathcal { G } _ { i } ( { \mathbf x } ) = e ^ { - \frac { 1 } { 2 } ( { \mathbf x } - { \pmb \mu } _ { i } ) ^ { \top } { \pmb \Sigma } _ { i } ^ { - 1 } ( { \mathbf x } - { \pmb \mu } _ { i } ) }
$$

其中 $\pmb \mu_i$ 为高斯中心位置，$\pmb \Sigma_i$ 为协方差矩阵。给定相机位姿，像素 $(x,y)$ 的颜色通过按深度排序的 $\alpha$ 混合渲染得到：

$$
I [ x , y ] = \mathcal { R } ( \mathcal { G } , C _ { j } ) = \sum _ { i = 1 } ^ { N } \mathbf { c } _ { i } \alpha _ { i } \prod _ { k = 1 } ^ { i - 1 } ( 1 - \alpha _ { k } )
$$

其中 $\mathbf{c}_i$ 为颜色，$\alpha_i$ 为透明度。此渲染过程可微，是后续水印嵌入与解码器训练的基础。

### 模块一：量化感知的中频带水印嵌入

核心洞察在于：**高频带**承载视觉细节，量化极易将其抹除，导致水印丢失；**低频带**承载场景结构，扰动会严重损害渲染质量。因此，Robust3DGSW 选择在 **3D 高斯位置的中频 DCT 系数**和 **2D 渲染图像的中频 FFT 环形区域**同时嵌入水印，以兼顾鲁棒性与视觉保真度。

**3D 域嵌入**。对 3D 高斯位置矩阵施加 1D 离散余弦变换（DCT），获得频域系数 $F_{k,d}^{3D}$，随后在中频区间 $[k_{\mathrm{low}}, k_{\mathrm{high}}]$ 添加高斯噪声：

$$
\tilde { F } _ { k , d } ^ { 3 D } = F _ { k , d } ^ { 3 D } + \alpha _ { 3 D } \cdot \mathcal { N } ( 0 , \sigma _ { 3 D } ^ { 2 } ) , \quad k \in [ k _ { \mathrm { l o w } } , k _ { \mathrm { h i g h } } ]
$$

其中 $\alpha_{3D}$ 为嵌入强度，$\sigma_{3D}^2$ 控制噪声方差。嵌入后通过逆 DCT 得到带水印的空间坐标。

**2D 域嵌入**。对渲染图像的每个颜色通道施加 2D 快速傅里叶变换（FFT），在频域中频环形区域 $[r_{\mathrm{low}}, r_{\mathrm{high}}]$ 内添加噪声：

$$
\tilde { F } _ { c } ^ { 2 D } [ u , v ] = F _ { c } ^ { 2 D } [ u , v ] + \alpha _ { 2 D } \cdot \mathcal { N } ( 0 , \sigma _ { 2 D } ^ { 2 } ) , \quad ( u - u _ { c } ) ^ { 2 } + ( v - v _ { c } ) ^ { 2 } \in [ r _ { \mathrm { l o w } } ^ { 2 } , r _ { \mathrm { h i g h } } ^ { 2 } ]
$$

其中 $(u_c, v_c)$ 为频域中心。嵌入后经逆 FFT 和 `ifftshift` 操作恢复空间域图像。双域中频嵌入形成冗余，使水印信号在量化压缩下不易被完全破坏。

### 模块二：多尺度对抗扰动

为使解码器在极端量化下仍能恢复水印，训练阶段对 3D 高斯特征和 2D 渲染图像同时注入三类扰动：频率域扰动、量化噪声和渲染级失真。扰动后的 3D 特征 $\tilde{\mathbf{f}}_{3D}$ 和渲染图像 $\hat{\mathbf{I}}$ 定义为：

$$
\tilde { \mathbf { f } } _ { 3 D } = \mathcal { Q } ( \mathbf { f } _ { 3 D } + \epsilon _ { \mathrm { D C T } } , b ( p ) ) + \mathcal { N } ( 0 , \sigma _ { q } ( b ) ) , \quad \hat { \mathbf { I } } = \mathcal { A } _ { \mathrm { r e n d e r } } \big ( \mathcal { Q } ( \tilde { I } _ { \mathrm { w m } } + \epsilon _ { \mathrm { F F T } } , b ( p ) ) \big )
$$

其中 $\mathcal{Q}(\cdot, b(p))$ 表示位宽为 $b(p)$ 的量化操作，$p$ 为渐进训练调度参数；$\epsilon_{\mathrm{DCT}}$ 和 $\epsilon_{\mathrm{FFT}}$ 分别为 3D 和 2D 频域扰动；$\sigma_q(b)$ 为量化噪声标准差；$\mathcal{A}_{\mathrm{render}}$ 模拟渲染级失真（如 JPEG 压缩、模糊等）。这种多尺度对抗扰动迫使解码器学会从严重退化信号中提取水印。

### 模块三：渐进式双解码器训练

**双解码器架构**。2D 解码器基于 HiDDeN 编码器加线性适配层，从归一化渲染图像 $I_{\mathrm{norm}}$ 中提取 $M$ 位水印：

$$
\mathbf { w } _ { 2 D } = \mathbf { A } _ { \mathrm { a d a p t } } \mathbf { H } _ { \mathrm { H i D D e N } } ( \mathbf { I } _ { \mathrm { n o r m } } )
$$

3D 解码器基于预训练 PointNet 处理 $N \times 14$ 维高斯属性向量，经最大池化和 MLP 输出水印：

$$
\mathbf { w } _ { 3 D } = \mathbf { M L P } ( \mathbf { M a x P o o l } ( \operatorname { P o i n t N e t } ( \mathbf { f } _ { 3 D } ) ) )
$$

**渐进式量化训练**。解码器参数 $\theta_{\mathrm{dec}}$ 的优化目标为在均匀采样的位宽分布下的期望损失最小化：

$$
\theta _ { \mathrm { d e c } } ^ { * } = \arg \underset { \theta } { \mathrm { m i n } } \mathbb { E } _ { p \sim \mathcal { U } ( 0 , 1 ) } \left[ \mathcal { L } ( \theta ; b ( p ) ) \right] , \quad \mathcal { L } ( \theta ; b ( p ) ) = \mathcal { L } _ { 2 D } ( \hat { \mathbf { I } } ) + \mathcal { L } _ { 3 D } ( \tilde { \mathbf { f } } _ { 3 D } ) + \mathcal { L } _ { \mathrm { r e g } }
$$

训练采用从 8-bit 到 4-bit 的渐进式位宽调度，使解码器逐步适应量化误差。2D 和 3D 解码器各自的二元交叉熵损失为：

$$
\mathcal{L}_{2D} = \mathrm{BCE}( D_{2D}(\bar{\mathbf{I}}), \mathbf{m} ), \quad \mathcal{L}_{3D} = \mathrm{BCE}( D_{3D}(\tilde{\mathbf{f}}_{3D}), \mathbf{m} )
$$

**跨域一致性损失**。为保证 2D 与 3D 解码器输出一致，引入 L2 一致性约束：

$$
\mathcal{L}_{\mathrm{cons}} = \| \sigma(\mathbf{w}_{2D}) - \sigma(\mathbf{w}_{3D}) \|^2
$$

其中 $\sigma$ 为 sigmoid 函数。**批一致性损失**则通过微小噪声惩罚解码器的不稳定性：

$$
\mathcal{L}_{\mathrm{batch}} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0, 10^{-6})} \left[ \| \mathbf{D}(\mathbf{x}) - \mathbf{D}(\mathbf{x} + \epsilon) \|^2 \right]
$$

**整体训练目标**。加权组合上述损失与重建正则化项：

$$
\mathcal{L}_{\mathrm{total}} = \lambda_{2D} \mathcal{L}_{2D} + \lambda_{3D} \mathcal{L}_{3D} + \lambda_{\mathrm{cons}} \mathcal{L}_{\mathrm{cons}} + \mathcal{L}_{\mathrm{rec}}
$$

其中重建正则化 $\mathcal{L}_{\mathrm{rec}} = \lambda_{\mathrm{bal}} \mathcal{L}_{\mathrm{balance}} + \lambda_{\mathrm{batch}} \mathcal{L}_{\mathrm{batch}}$，$\mathcal{L}_{\mathrm{balance}}$ 为位平衡损失，促进解码器输出各比特位均衡。

### 关键设计总结

三个模块形成因果闭环：中频带嵌入从源头规避量化对水印信号的毁灭性压缩；多尺度对抗扰动在训练中模拟量化与渲染退化，强制解码器习得鲁棒特征；渐进式双解码器训练通过从高到低的位宽调度和跨域一致性约束，使水印在 2D 渲染域和 3D 高斯域之间形成冗余互证。消融实验（Table 1）证实，移除任一组件均导致 4-bit 量化下准确率大幅下降——尤其移除渐进量化训练后准确率从 87.51% 骤降至 67.42%，验证了该模块在极端量化场景下的不可替代性。

### 补充图表

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/001_Figure_1.jpg]]
*Figure 1: Trends in watermark robustness and rendered image quality of 3D-GSW as quantization levels decrease*

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/004_Figure_6.jpg]]
*Figure 6: Trends in watermarking robustness and rendered image quality of Robust3DGSW as quantization levels decrease*



## 实验与关键发现

### 量化退化：3DGS水印的脆弱性

量化对现有3DGS水印方法构成致命威胁。图1揭示了**3D-GSW** (Jang et al., CVPR 2025) 在量化位宽降低时的性能崩溃：水印提取准确率从32位的98%骤降至4位的61%，而渲染质量PSNR从35 dB暴跌至10 dB。这一退化现象的根本原因在于，现有方法将水印信号嵌入全空间域或高频带，这些频带在低比特量化时首当其冲地被截断——高频系数因幅值小而直接被量化为零，导致水印信号完全淹没在量化噪声中。Robust3DGSW的设计正是针对这一瓶颈，通过中频带嵌入和量化感知训练双管齐下地解决该问题。

### 无量化条件下的性能对比

在无量化条件下，Robust3DGSW在所有评估指标上均优于基线方法。如图3所示，在Blender、LLFF和MipNeRF360三个数据集的平均结果上，Robust3DGSW的位准确率达到99.78%，比**3D-GSW**的98%高出约1.78个百分点。在渲染质量方面，Robust3DGSW同样在PSNR、SSIM和LPIPS上保持领先或持平水平。这一优势源于中频带嵌入策略——中频带既避开了低频区域（修改低频会严重损害视觉质量），又避开了高频区域（高频对渲染质量影响小但对量化极度敏感），从而在无量化场景下也实现了更优的水印-质量平衡。

### 4位量化下的性能对比

量化场景才是Robust3DGSW与基线方法拉开差距的主战场。图4展示了4位量化下的性能对比，Robust3DGSW的位准确率保持在87.51%，而**3D-GSW**仅为61%，提升幅度高达26.51个百分点。在渲染质量上，Robust3DGSW的PSNR达到20.46 dB，是**3D-GSW**（10 dB）的两倍以上。这一显著优势来自三个协同机制：(1) 中频带嵌入使水印信号天然避开量化截断区域；(2) 渐进式量化训练（从8位逐步降至4位）使双解码器逐步适应量化噪声的统计特性；(3) 多尺度对抗扰动在训练中模拟了量化带来的复合失真，迫使解码器学习从噪声中恢复水印的鲁棒映射。

### 失真鲁棒性分析

图5展示了4位量化下各方法面对噪声、模糊、旋转和裁剪四种常见失真的鲁棒性。Robust3DGSW在所有失真类型下均显著优于基线。以裁剪失真为例，Robust3DGSW的位准确率为82.79%，而3D-GSW的对应值大幅落后。这一鲁棒性得益于多尺度对抗扰动机制——在解码器训练阶段，系统同时对3D高斯特征施加频率域扰动和量化噪声，对2D渲染图像施加渲染级失真，使解码器在训练中暴露于多种失真组合，从而习得对未见失真的泛化能力。值得注意的是，模糊失真下Robust3DGSW的准确率（82.52%）相对其他失真类型有所下降，这暗示中频带嵌入对低频模糊的敏感性可能是一个潜在的脆弱点。

### 消融研究：各组件的因果贡献

表1的消融研究系统性地揭示了五个关键组件的因果贡献。以下按组件重要性递减顺序分析：

**解码器训练是基础前提。** 移除解码器训练后，无量化条件下的位准确率仅为63.44%，模糊失真下更是低至46.59%，在所有配置中均为最低。这表明，即使水印已嵌入3D高斯和渲染图像，若缺乏专门的解码器训练，从高斯表示中恢复水印信号几乎是不可行的。

**渐进式量化训练是应对极端量化的核心。** 移除渐进训练后，4位量化准确率从87.51%暴跌至67.42%，降幅达20个百分点。这一结果证实，简单地在固定位宽下训练解码器无法应对量化位宽的大幅变化——解码器需要在不同量化级别下逐步适应，才能建立起对量化误差的鲁棒表征。

**水印鲁棒性增强（中频嵌入）对量化鲁棒性不可或缺。** 移除该组件（即改用高频嵌入）后，4位量化准确率降至72.57%，模糊失真下更是降至65.76%。这验证了中频带选择的因果作用：高频嵌入在量化时被严重破坏，而中频带处于量化保留区，是水印信号存活的必要条件。

**多尺度对抗扰动对失真鲁棒性至关重要。** 移除该扰动后，裁剪失真下的准确率从82.79%骤降至65.78%，降幅超过17个百分点。这表明，仅在干净数据上训练的解码器对失真极为脆弱，而对抗扰动通过数据增广的方式迫使解码器学习失真不变的水印特征。

**图像质量增强（2D中频嵌入）对渲染质量和水印提取均有贡献。** 移除后4位量化准确率降至78.56%，PSNR降至18.68 dB。这证明在渲染图像的2D频域中额外嵌入水印，不仅为水印提取提供了冗余信号通路，也有助于约束渲染质量。

### 量化鲁棒性趋势

图6展示了Robust3DGSW在不同量化级别下的性能变化趋势。与图1中3D-GSW的断崖式下降不同，Robust3DGSW的位准确率和PSNR随量化位宽降低呈现平缓下降——从32位到4位，准确率仅从99.78%降至87.51%，PSNR从约35 dB降至20.46 dB。这一平滑退化曲线表明，渐进式量化训练成功地将量化误差的影响分散到整个训练过程中，避免了在某个位宽阈值处的性能突变。

### 失败模式与局限

尽管Robust3DGSW在量化鲁棒性上取得了显著提升，但仍存在两个明确的局限。**第一，训练效率**：双解码器训练阶段相比基线方法需要约40%的额外训练时间，这源于多尺度对抗扰动的计算开销和渐进式训练的迭代需求。**第二，对抗性失真**：当前版本仅评估了噪声、模糊、旋转、裁剪四种常见失真，未针对精心设计的对抗性失真（如针对特定频带的定向攻击）进行鲁棒性测试。在对抗性场景下，攻击者可能利用中频带嵌入的已知频带范围设计精准的破坏策略，这是需要进一步研究的开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/003_Figure_3.jpg]]
*Figure 3: Performance comparison (without quantization)*

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/005_Figure_4.jpg]]
*Figure 4: Performance comparison (with 4-bit quantization)*

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/006_Figure_5.jpg]]
*Figure 5: Robustness against distortions under 4-bit quantization*

![[assets/figures/papers/paper_list_l2733_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Robust3DGSW_Towar/figures/007_Table_1.jpg]]
*Table 1: Ablation study on key parts of Robust3DGSW, with results denoting the average score on Blender, LLFF, and MipNeRF360*



## 定位与知识库关联

### 与基线方法的关系

Robust3DGSW 是针对 3D 高斯泼溅（3DGS）版权保护场景提出的量化感知水印框架，其技术定位可从以下四个维度与现有基线进行对比。

**3DGS 原生水印方法。** 最直接的对比对象是 **3D-GSW**（Jang et al., CVPR 2025）和 **GaussianMarker**（Huang et al., NeurIPS 2024）。这两类方法均在 3D 高斯参数空间或渲染管线中嵌入水印，但均未考虑模型量化带来的信号衰减问题。实验证据表明，当量化位宽从 32 位降至 4 位时，3D-GSW 的水印提取准确率从 98% 骤降至 61%，PSNR 从 35 dB 跌至 10 dB（Figure 1）。Robust3DGSW 的核心改进在于引入了中频带嵌入策略和渐进式量化感知训练，使 4 位量化下的准确率保持在 87.51%、PSNR 达到 20.46 dB（Table 1），从根本上解决了量化鲁棒性缺失的瓶颈。

**NeRF 水印方法的 3DGS 适配。** **StegaNeRF + 3DGS**（Li et al., ICCV 2023; Kerbl et al., ACM Trans. Graph. 2023）将隐式 NeRF 的水印方案迁移至 3DGS 渲染管线，但 NeRF 的连续隐式表示与 3DGS 的显式高斯原语在参数结构和量化敏感度上存在本质差异，导致迁移后的水印在量化场景下鲁棒性不足。Robust3DGSW 通过针对 3D 高斯位置矩阵的 1D DCT 中频嵌入和针对渲染图像的 2D FFT 中频嵌入，实现了对 3DGS 参数特性的适配。

**2D 水印解码器的 3DGS 结合。** **HiDDeN + 3DGS**（Zhu et al., ECCV 2018; Kerbl et al., ACM Trans. Graph. 2023）将传统 2D 图像水印解码器 HiDDeN 与 3DGS 渲染结合，但仅依赖单一 2D 解码器，缺乏对 3D 高斯特征空间的直接监督。Robust3DGSW 提出双解码器架构——2D HiDDeN 解码器（含线性适配层）与 3D PointNet 解码器并行工作，并通过一致性损失 $\mathcal{L}_{\mathrm{cons}} = \| \sigma(\mathbf{w}_{2D}) - \sigma(\mathbf{w}_{3D}) \|^2$ 对齐跨域输出，显著增强了水印提取的冗余性和稳定性。

**关键设计差异总结。** 三个核心“变化槽”构成了 Robust3DGSW 与基线的方法学边界：（1）水印嵌入频带从全空间域/高频带迁移至中频带，在视觉重要性与量化敏感性之间取得平衡（Section 3.2）；（2）解码器训练策略从固定精度或无量化训练升级为渐进式量化感知训练（8-bit → 4-bit），配合多尺度对抗扰动（频率域扰动、量化噪声、渲染级失真），使解码器学会从量化误差中恢复水印信号（Section 3.3）；（3）解码器架构从单一解码器扩展为双解码器，并引入一致性损失和批一致性损失 $\mathcal{L}_{\mathrm{batch}}$ 以稳定训练（Section 3.4）。

### 适用边界与局限

**适用场景。** Robust3DGSW 主要面向需要对 3DGS 模型进行版权保护且模型可能经历量化压缩的部署场景，如移动端/边缘端的 3D 场景渲染应用。方法在 Blender、LLFF 和 MipNeRF360 三个基准数据集上进行了验证，涵盖无量化、4 位量化以及噪声、模糊、旋转、裁剪等常见失真条件（Figure 3–5）。

**训练开销。** 论文明确指出，双解码器训练阶段相比基线方法需要大约 40% 的额外训练时间。这一开销主要来源于多尺度对抗扰动的在线生成和双解码器的联合优化。对于资源受限的训练环境，该开销可能构成实用瓶颈。

**失真覆盖范围。** 当前版本的 Robust3DGSW 仅评估了常见失真类型（噪声、模糊、旋转、裁剪），未涉及复杂的对抗性失真攻击。在恶意攻击者精心构造对抗性扰动以破坏水印的场景下，方法的鲁棒性尚未得到验证，这是一个明确的适用边界。

**量化位宽下限。** 消融研究（Table 1）显示，虽然渐进式量化训练使 4 位量化下的准确率达到 87.51%，但移除该组件后准确率骤降至 67.42%。这表明方法对极端低位宽（如 2 位或 1 位）量化的适应性仍存在不确定性，论文未报告 4 位以下的实验结果。

### 开放问题

基于论文明确的局限性和方法设计中的潜在扩展空间，以下开放问题值得关注：

1. **训练效率优化。** 如何降低双解码器训练阶段约 40% 的额外时间开销？可能的路径包括：扰动生成的离线预计算、解码器的知识蒸馏压缩、或渐进训练调度的自适应加速策略。

2. **对抗鲁棒性增强。** 如何使 Robust3DGSW 能够抵御精密的对抗性失真攻击？这需要在多尺度对抗扰动机制的基础上，引入对抗训练范式或认证鲁棒性约束，使解码器对最坏情况扰动具有可证明的下界保障。

3. **极端量化边界探索。** 在 2 位甚至 1 位量化的极端条件下，中频带嵌入策略是否仍然有效？可能需要重新审视频带划分策略，或引入纠错编码机制以补偿极端量化造成的信息损失。

4. **跨模型泛化性。** 当前方法在 3DGS 框架内验证，其对其他显式场景表示（如 3D Gaussian 变体、点云渲染）的泛化能力尚未探讨，这决定了方法在更广泛 3D 资产保护场景中的适用性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Robust3DGSW_Toward_Robust_Watermarking_for_Quantization_Aware_3D_Gaussian_Splatting.pdf]]

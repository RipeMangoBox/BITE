---
title: "CADC: Content Adaptive Diffusion-Based Generative Image Compression"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CADC_Content_Adaptive_Diffusion_Based_Generative_Image_Compression.pdf
project_link: null
code_link: null
aliases:
- CCADBIC
- CADC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入不确定性引导的自适应量化（UGAQ）对齐噪声分布与内容、辅助解码器引导的信息集中（ADGIC）强制关键信息流向主通道、以及无码率自适应文本条件化（BFATC）从辅助重建图像提取内容感知文本，实现压缩过程与图像内容的自适应匹配，从而释放扩散模型的生成潜力。
primary_logic: 核心洞察在于：压缩过程的每一环节（量化、潜表示、条件化）必须动态适应图像内容，而非采用全局固定策略；通过空间变化的不确定性地图调制噪声、损失驱动的信息集中以及代理重建生成的语义条件，可以在不增加码率的前提下极大地提升极低码率图像压缩的感知质量。
claims:
- UGAQ通过从主潜变量与上采样超先验潜变量的残差中学习空间不确定性图，从而调制量化噪声并实现内容感知噪声整形。
- ADGIC引入轻量级辅助解码器，仅操作噪声潜变量的前4个通道，通过辅助重建损失强制信息集中，解决了信息集中瓶颈。
- BFATC使用预训练BLIP模型从辅助重建图像生成内容自适应字幕，无需任何额外文本码率，提供了语义引导。
- Kodak 上 LPIPS BD-rate = M3 (full CADC) BD-rate -6.8%
---

# CADC: Content Adaptive Diffusion-Based Generative Image Compression

> [!tip] 核心洞察
> 核心洞察在于：压缩过程的每一环节（量化、潜表示、条件化）必须动态适应图像内容，而非采用全局固定策略；通过空间变化的不确定性地图调制噪声、损失驱动的信息集中以及代理重建生成的语义条件，可以在不增加码率的前提下极大地提升极低码率图像压缩的感知质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | CADC：内容自适应扩散生成图像压缩 |
| 英文题名 | CADC: Content Adaptive Diffusion-Based Generative Image Compression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21591) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CADC (Content-Adaptive Diffusion-Based Image Compression) |
| Dataset | Kodak, Kodak, DIV2K Val, CLIC 2020 Test |

> [!tip] 效果简介
> - Kodak 上，LPIPS BD-rate M3 (full CADC) BD-rate -6.8% vs M0 (baseline) (-6.8%)；DISTS BD-rate M3 BD-rate -5.5% vs M0 (-5.5%)；Top-1 user preference 58.5% vs StableCodec 29.0%, DLF 12.5% (+29.5% over StableCodec)。
> - Kodak, DIV2K Val, CLIC 2020 Test 上，LPIPS, DISTS, FID, KID superior perceptual quality vs all compared generative codecs (state-of-the-art)。

## 概要

**CADC** (Content-Adaptive Diffusion-Based Image Compression) 是一种面向极低码率图像压缩的内容自适应扩散生成编解码框架。其核心动机在于解决现有扩散图像压缩方法中三个关键瓶颈：**各向同性量化**导致量化噪声与扩散模型的噪声先验错配、**信息集中瓶颈**源于高维噪声潜变量与预训练扩散解码器固定4通道输入之间的维度失配、以及**文本条件化策略**要么消耗额外码率传输文本，要么使用与内容无关的通用提示而无法提供有效语义指导。

针对上述问题，CADC提出了三个协同设计的方法模块：

- **不确定性引导的自适应量化 (UGAQ)**：从主潜变量与上采样超先验潜变量的残差中学习空间变化的不确定性图，据此调制量化噪声，实现内容感知的噪声整形，使压缩失真与扩散模型的噪声相关生成先验对齐。
- **辅助解码器引导的信息集中 (ADGIC)**：引入轻量级辅助解码器，仅操作噪声潜变量的前4个通道，通过辅助重建损失强制关键语义信息向主通道集中，解决信息集中瓶颈。
- **无码率自适应文本条件化 (BFATC)**：利用预训练BLIP模型从辅助重建图像中生成内容自适应字幕，并以零额外码率作为扩散去噪的语义条件，提供内容感知的生成引导。

**核心洞察**在于：压缩过程的每一环节——量化、潜表示、条件化——必须动态适应图像内容，而非采用全局固定策略。通过空间变化的不确定性地图调制噪声、损失驱动的信息集中以及代理重建生成的语义条件，CADC在不增加码率的前提下显著提升了极低码率图像压缩的感知质量。

**主要结果**：在Kodak数据集上，完整CADC（M3）相较基线M0在LPIPS和DISTS指标上分别取得−6.8%和−5.5%的BD-rate增益。用户研究中，CADC以58.5%的Top-1偏好率显著优于StableCodec（29.0%）和DLF（12.5%）。在Kodak、DIV2K验证集和CLIC 2020 Professional测试集上，CADC在LPIPS、DISTS、FID、KID等感知质量指标上均达到最优水平，尤其在极低码率条件下展现出明显优势。

**方法定位**：CADC属于扩散生成压缩方法谱系，与StableCodec（Zhang et al., ICCV 2025）、HiFiC、DiffEIC等生成编解码器形成对比。其独特贡献在于将内容自适应机制系统性地引入量化、信息分配和条件化三个环节，而非依赖更大的模型或更复杂的扩散采样策略。



### 生成式图像压缩的范式演进

图像压缩长期遵循“编码器-量化-熵编码-解码器”的变换编码范式。近年来，深度生成模型——特别是扩散模型——的引入，使压缩目标从像素保真度转向感知质量，催生了**生成式图像压缩**这一新范式。其核心思想是：在解码端利用扩散模型的强大先验，从极度压缩的潜表示中重建出纹理丰富、语义合理的图像，从而在极低码率（通常 < 0.01 bpp）下突破传统编解码器的质量上限。

然而，现有扩散压缩方法在将扩散模型“嫁接”到压缩管线时，普遍忽视了压缩过程与图像内容之间的**自适应匹配**，导致三个相互关联的结构性瓶颈。

### 瓶颈一：各向同性量化与内容异质性的错配

传统压缩方法采用**各向同性量化**——对所有空间位置施加统一的量化步长 $\Delta$，这意味着整幅图像共享相同的信噪比（SNR）。这一设计假设图像内容的“重要性”在空间上是均匀分布的，但现实图像恰恰相反：平坦区域对量化噪声极为敏感，而纹理丰富区域则可容忍更强的噪声。在扩散压缩的语境下，这一问题被进一步放大：扩散模型的去噪过程依赖于噪声潜变量 $l_T$ 的统计特性与预训练噪声先验的对齐。当量化噪声在空间上均匀注入时，高信息密度区域（如边缘、人脸）的信噪比不足，而低信息密度区域（如天空、墙面）的信噪比过剩，形成**噪声-内容错配**，直接限制了扩散模型的生成重建潜力。

### 瓶颈二：信息集中瓶颈与维度不匹配

扩散压缩的另一个关键瓶颈源于潜表示的维度冲突。预训练的稳定扩散（Stable Diffusion）VAE 解码器 $\mathcal{D}_{SD}$ 被硬编码为仅接受 4 通道输入，而压缩管线中的合成变换 $g_s$ 通常输出高维噪声潜变量 $l_T$（例如 320 通道）以保留足够的上下文信息。现有方法（如 **StableCodec**，Zhang et al., ICCV 2025）将完整的 $l_T$ 馈入扩散 UNet 以估计 4 通道噪声，但这一策略本质上是一个**信息集中瓶颈**：模型缺乏显式约束来确保关键的语义和结构信息被集中到前 4 个通道中——而这些通道才是最终被去噪并解码为重建图像的唯一信息载体。这导致主通道可能仅承载了部分信息，而大量有用信号残留在辅助通道中，在去噪过程中被浪费。

### 瓶颈三：文本条件化的码率与语义困境

扩散模型的重建质量高度依赖于文本条件化。现有方案面临两难：要么传输文本描述（消耗额外码率，在极低码率场景下不可接受），要么使用与内容无关的固定通用提示（如“a high quality image”），无法提供语义引导。这一困境的根本原因在于，解码端在重建完成前缺乏对图像内容的语义认知，因此无法在不增加码率的前提下生成内容感知的条件信号。

### 本文动机与核心洞察

上述三个瓶颈指向一个共同的根源：**压缩过程的每一环节（量化、潜表示、条件化）均采用全局固定策略，而非动态适应图像内容**。CADC 的核心洞察在于：通过引入内容自适应的量化噪声整形、损失驱动的信息集中机制、以及基于代理重建的无码率语义条件化，可以在不增加码率的前提下，使扩散压缩管线与图像内容的局部特性实现精细对齐，从而充分释放扩散模型的生成潜力。



## 核心方法与创新机理

CADC 针对现有扩散图像压缩方法在极低码率下的三个结构瓶颈，提出了三项内容自适应机制，构成从量化、潜表示到条件化的全链路创新。

### 瓶颈一：各向同性量化与扩散先验错配

现有方法采用全局统一的量化步长，忽略了图像内容的空间异质性。在极低码率下，量化噪声的统计特性与预训练扩散模型的噪声相关先验之间存在严重错配：平坦区域和纹理区域承受相同的量化损伤，导致扩散解码器无法有效利用其生成能力进行差异化修复。

**创新：不确定性引导的自适应量化（UGAQ）**

UGAQ 的核心思想是让量化噪声的分布与图像内容的空间结构对齐。具体而言，系统从主潜变量 $\mathbf{y}$ 与上采样超先验潜变量 $\bar{\mathbf{z}} = \mathrm{UP}(\hat{\mathbf{z}})$ 之间的残差 $\mathbf{r} = \mathbf{y} - \overline{\mathbf{z}}$ 中，学习一个空间变化的不确定性图 $\mathbf{m} = f_u(\mathbf{r})$（$m_{i,j} \geq 1$）。量化前，主潜变量被逐元素调制为 $\bar{\mathbf{y}} = \mathbf{y} / \mathbf{m}$，再执行均匀量化 $\hat{\mathbf{y}} = Q(\bar{\mathbf{y}})$。

这一设计的因果机制在于：高不确定性区域（如复杂纹理）对应的 $m_{i,j}$ 较大，调制后的 $\bar{y}_{i,j}$ 被压缩，量化后等效信噪比降低，扩散模型在解码端被“告知”该区域需要更强的生成式修复；低不确定性区域（如平坦区域）则保留较高信噪比，维持结构保真度。有效局部信噪比 $\mathrm{SNR}_{i,j} \propto \mathbb{E}[y_{i,j}^2] / (m_{i,j}^2 \cdot \sigma_{\epsilon}^2)$ 实现了内容感知的噪声整形，无需传输额外的空间重要性图。

### 瓶颈二：高维噪声潜变量与固定解码器接口的信息集中瓶颈

预训练的 Stable Diffusion VAE 解码器 $\mathcal{D}_{SD}$ 仅接受 4 通道输入，而合成变换 $g_s$ 输出的噪声潜变量 $\boldsymbol{l}_T$ 具有高通道数（如 320）。现有方法将全部通道送入扩散 UNet 以利用上下文信息，但缺乏显式机制确保关键语义信息集中到前 4 个主通道中，导致信息分散在辅助通道中而无法被解码器直接利用。

**创新：辅助解码器引导的信息集中（ADGIC）**

ADGIC 引入一个轻量级辅助解码器 $g_{aux}$，仅操作噪声潜变量的前 4 个通道 $\boldsymbol{l}_T^{(1:4)}$，生成辅助重建图像 $\hat{\mathbf{x}}_{aux} = g_{aux}(\boldsymbol{l}_T^{(1:4)})$，并以原始图像为监督目标计算辅助重建损失 $\mathcal{L}_{aux} = \|\mathbf{x} - \hat{\mathbf{x}}_{aux}\|_2^2$。

该设计的因果逻辑是：辅助解码器只有 4 通道输入，为最小化 $\mathcal{L}_{aux}$，网络被迫将重建所需的核心语义信息（结构、纹理、语义）集中到前 4 个通道中。消融实验证实，加入 ADGIC 后，前 4 通道的能量占比显著提升（Figure 6），验证了信息集中的有效性。这一机制以极小的计算开销解决了高维潜空间与固定解码器接口之间的维度错配。

### 瓶颈三：文本条件化的码率开销与语义空洞

扩散模型的条件化文本对生成质量至关重要，但现有策略陷入两难：传输文本描述消耗额外码率，使用固定通用提示则无法提供内容相关的语义引导。

**创新：无码率自适应文本条件化（BFATC）**

BFATC 利用 ADGIC 的辅助重建图像作为代理，通过冻结的预训练 BLIP 模型提取内容自适应字幕 $c_{aux} = f_c(\hat{\mathbf{x}}_{aux})$，并将其与固定通用描述拼接 $c = c_{aux} + c_{fix}$ 作为扩散去噪的条件。

该设计的精妙之处在于：辅助重建图像本身由前 4 通道生成，不消耗额外码率；BLIP 模型在编码器和解码器端均可独立运行，无需传输文本。Figure 7 展示，即使在极低码率下，从辅助重建图像中提取的字幕仍能准确捕捉场景语义（如“a group of people standing on a beach”），为扩散解码器提供有效的语义锚点。

### 三项创新的协同效应

消融实验（Table 1）揭示了各项创新的累积贡献：以无任何自适应机制的基线 M0 为参照，UGAQ 单独带来 LPIPS BD-rate 降低 3.7%、DISTS BD-rate 降低 2.7%；叠加 ADGIC 后，LPIPS 进一步降低 1.6%（累计 −5.3%），DISTS 降低 0.8%（累计 −3.5%）；加入 BFATC 后，LPIPS 再降低 1.5%（累计 −6.8%），DISTS 再降低 2.0%（累计 −5.5%）。三项创新从量化噪声整形、信息流控制和语义条件化三个维度形成互补，共同释放了扩散模型的生成潜力。



CADC (Content-Adaptive Diffusion-Based Image Compression) 构建了一个端到端的、内容自适应的扩散生成图像压缩框架，其核心设计理念是使压缩过程的每一环节——量化、潜表示、条件化——均动态匹配图像内容的空间异质性。整体系统架构如 Figure 2 所示，编码端与解码端通过三个关键创新模块实现内容感知：不确定性引导的自适应量化 (UGAQ)、辅助解码器引导的信息集中 (ADGIC) 和零码率自适应文本条件化 (BFATC)。

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/002_Figure_2.jpg]]
*Figure 2: On the encoder side, an analysis transform*

### 编码端 (Encoder Side)

编码端负责将输入图像 $\mathbf{x}$ 压缩为紧凑的比特流。其数据流如下：

1. **主分析变换** $g_a$ 将输入图像 $\mathbf{x}$ 编码为紧凑的潜表示 $\mathbf{y}$。
2. **超先验编码**：超分析变换 $h_a$ 从 $\mathbf{y}$ 生成超先验潜变量 $\mathbf{z}$，经量化后由超合成变换 $h_s$ 生成边信息 $\mathbf{c}_h$，用于后续熵模型的均值/方差预测。
3. **不确定性引导的自适应量化 (UGAQ)**：
   - 将量化的超先验潜变量 $\hat{\mathbf{z}}$ 双线性上采样至与 $\mathbf{y}$ 相同分辨率：$\bar{\mathbf{z}} = \mathrm{UP}(\hat{\mathbf{z}})$。
   - 计算残差以捕获内容不确定性：$\mathbf{r} = \mathbf{y} - \bar{\mathbf{z}}$。
   - 轻量级不确定性估计网络 $f_u$ 从 $\mathbf{r}$ 预测空间变化的不确定性图 $\mathbf{m} = f_u(\mathbf{r})$（元素 $\geq 1$）。
   - 内容自适应缩放：$\bar{\mathbf{y}} = \mathbf{y} / \mathbf{m}$。
   - 均匀量化：$\hat{\mathbf{y}} = Q(\bar{\mathbf{y}}) = \lfloor \bar{\mathbf{y}} / \Delta \rfloor \cdot \Delta$，其中 $\Delta$ 为全局量化步长。
4. **算术编码** (AE) 对 $\hat{\mathbf{y}}$ 和 $\hat{\mathbf{z}}$ 进行无损熵编码，生成传输比特流。

UGAQ 的核心机理在于：通过逐元素除法调制，解码端的有效局部信噪比变为 $\mathrm{SNR}_{i,j} \propto \mathbb{E}[y_{i,j}^2] / (m_{i,j}^2 \cdot \sigma_{\epsilon}^2)$。高不确定性区域（$m_{i,j}$ 大）获得更低 SNR，允许扩散模型进行更强的生成式重建；低不确定性区域（$m_{i,j}$ 小）保持更高 SNR，保留结构保真度。这实现了量化噪声与扩散模型噪声相关先验的内容感知对齐。

### 解码端 (Decoder Side)

解码端从比特流重建图像，其数据流与关键模块关系如下：

1. **算术解码** 恢复 $\hat{\mathbf{y}}$ 和 $\hat{\mathbf{z}}$。
2. **主合成变换** $g_s$ 将 $\hat{\mathbf{y}}$ 上采样为高维噪声潜变量 $\mathbf{l}_T$（例如 320 通道），其空间分辨率匹配预训练的 Stable Diffusion VAE 解码器 $\mathcal{D}_{SD}$ 的要求。
3. **信息集中瓶颈处理**：$\mathcal{D}_{SD}$ 仅接受固定的 4 通道输入，而 $\mathbf{l}_T$ 具有高通道数。CADC 将全部 $\mathbf{l}_T$ 输入扩散去噪 UNet $\epsilon_{SD}$（通过修改 UNet 第一卷积层的输入通道数），利用全部上下文信息估计更准确的 4 通道噪声；UNet 的输出通道数仍为 4，去噪过程仅作用于前 4 个通道 $\mathbf{l}_T^{(1:4)}$。
4. **辅助解码器引导的信息集中 (ADGIC)**：
   - 轻量级辅助解码器 $g_{aux}$ 仅从 $\mathbf{l}_T^{(1:4)}$ 重建辅助图像：$\hat{\mathbf{x}}_{aux} = g_{aux}(\mathbf{l}_T^{(1:4)})$。
   - 计算辅助重建损失：$\mathcal{L}_{aux} = \|\mathbf{x} - \hat{\mathbf{x}}_{aux}\|_2^2$。
   - 该损失强制关键语义信息集中到前 4 个通道，解决信息集中瓶颈。
5. **零码率自适应文本条件化 (BFATC)**：
   - 使用冻结的预训练 BLIP 模型 $f_c$ 从辅助重建图像 $\hat{\mathbf{x}}_{aux}$ 生成内容自适应文本描述：$c_{aux} = f_c(\hat{\mathbf{x}}_{aux})$。
   - 将 $c_{aux}$ 与固定通用描述 $c_{fix}$ 拼接：$c = c_{aux} + c_{fix}$，作为扩散去噪的条件。
6. **扩散去噪**：UNet $\epsilon_{SD}$ 在文本条件 $c$ 和完整 $\mathbf{l}_T$ 的引导下，对 $\mathbf{l}_T^{(1:4)}$ 执行一步或多步去噪，得到标准 4 通道清洁潜变量 $\mathbf{l}_0$。
7. **VAE 解码**：预训练的 Stable Diffusion VAE 解码器 $\mathcal{D}_{SD}$ 将 $\mathbf{l}_0$ 解码为最终重建图像 $\hat{\mathbf{x}}$。

### 模块协同与训练策略

三个创新模块形成级联协同：UGAQ 在量化阶段实现内容感知噪声整形，ADGIC 在潜表示阶段确保关键信息流向主通道，BFATC 在条件化阶段提供零码率语义引导。辅助重建图像 $\hat{\mathbf{x}}_{aux}$ 作为关键中间表示，同时服务于 ADGIC 的监督信号和 BFATC 的文本生成源，实现了信息集中与语义条件的耦合。

训练采用两阶段策略以适应极低码率场景：
- **第一阶段**：使用较小的 $\lambda_{\text{base}}$ 训练基础模型，优化目标 $\mathcal{L}_1 = \lambda_{\text{base}} \mathcal{R} + \mathcal{D}_1$。
- **第二阶段**：使用目标大 $\lambda_{\text{target}}$ 微调至极低码率，优化目标 $\mathcal{L}_2 = \lambda_{\text{target}} \mathcal{R} + \mathcal{D}_2$。

整体率失真损失为 $\mathcal{L} = \lambda \mathcal{R} + \mathcal{D}$，其中 $\mathcal{R}$ 为码率项，$\mathcal{D}$ 为失真项。各网络模块的详细结构见 Figure 8，熵建模流程见 Figure 9。

### 与基线方法的本质差异

相较于现有扩散图像压缩方法（如 **StableCodec** (Zhang et al., ICCV 2025)、**DLF**、**HiFiC** 等），CADC 在三个关键维度上实现了根本性改进：(1) 从各向同性量化转向空间自适应量化；(2) 从无引导的潜表示转向损失驱动的信息集中；(3) 从消耗码率的文本传输或通用固定提示转向零码率内容感知文本条件化。这些改进使 CADC 在极低码率下显著提升了感知质量，尤其在复杂纹理区域表现突出（见 Figure 1 定性对比）。



CADC 的编码器首先通过主分析变换 $g_a$ 将输入图像 $\mathbf{x}$ 压缩为紧凑的潜表示 $\mathbf{y}$。超先验分析变换 $h_a$ 进一步将 $\mathbf{y}$ 编码为超先验潜变量 $\mathbf{z}$，经量化后由超先验合成变换 $h_s$ 生成边信息 $\mathbf{c}_h$ 用于熵建模。量化后的主潜变量 $\hat{\mathbf{y}}$ 经算术编码形成码流传输。

解码端，主合成变换 $g_s$ 将 $\hat{\mathbf{y}}$ 上采样至预训练稳定扩散 VAE 解码器 $\mathcal{D}_{SD}$ 所需的空间分辨率，产生高维噪声潜变量 $\boldsymbol{l}_T$（典型通道数为 320）。然而 $\mathcal{D}_{SD}$ 仅接受 4 通道输入，因此整个 $\boldsymbol{l}_T$ 被送入 Unet $\epsilon_{SD}$ 以利用全部上下文估计更准确的 4 通道噪声，去噪过程仅作用于前 4 个噪声通道 $l_T^{(1:4)}$，得到标准 4 通道干净潜变量 $\iota_0$ 后由 $\mathcal{D}_{SD}$ 解码为重建图像 $\hat{\mathbf{x}}$。

### 不确定性引导的自适应量化（UGAQ）

UGAQ 的核心在于通过空间变化的不确定性图调制量化噪声，实现内容感知的噪声整形。首先将超先验潜变量 $\hat{\mathbf{z}}$ 双线性上采样至与主潜变量相同的分辨率：

$$\bar{\mathbf{z}} = \mathrm{UP}(\hat{\mathbf{z}})$$

计算主潜变量与上采样超先验潜变量之间的残差，该残差反映了内容的不确定性：

$$\mathbf{r} = \mathbf{y} - \overline{\mathbf{z}}$$

轻量级不确定性估计网络 $f_u$ 从残差中预测空间变化的不确定性图 $\mathbf{m}$（元素 $\geq 1$）：

$$\mathbf{m} = f_u(\mathbf{r})$$

使用不确定性图对潜变量进行逐元素除法，实现自适应缩放：

$$\bar{\mathbf{y}} = \mathbf{y} / \mathbf{m}$$

对调制后的潜变量执行均匀量化，量化步长为 $\Delta$：

$$\hat{\mathbf{y}} = Q(\bar{\mathbf{y}}) = \left\lfloor \frac{\bar{\mathbf{y}}}{\Delta} \right\rceil \cdot \Delta$$

由于量化前的不确定性调制，解码器输入端形成空间变化的有效局部信噪比，高不确定性区域获得更强的生成干预，低不确定性区域则保留结构保真度：

$$\mathrm{SNR}_{i,j} \propto \frac{\mathbb{E}[\bar{y}_{i,j}^2]}{\sigma_{\epsilon}^2} = \frac{\mathbb{E}[y_{i,j}^2]}{m_{i,j}^2 \cdot \sigma_{\epsilon}^2}$$

### 辅助解码器引导的信息集中（ADGIC）

ADGIC 引入轻量级辅助解码器 $g_{aux}$，仅操作噪声潜变量的前 4 个通道，生成辅助重建图像：

$$\hat{\mathbf{x}}_{aux} = g_{aux}(l_T^{(1:4)})$$

通过原始图像与辅助重建之间的均方误差损失，强制语义信息集中到前 4 个通道：

$$\mathcal{L}_{aux} = \|\mathbf{x} - \hat{\mathbf{x}}_{aux}\|_2^2$$

### 无码率自适应文本条件化（BFATC）

BFATC 使用冻结的预训练 BLIP 模型 $f_c$ 从辅助重建图像中提取内容自适应文本描述，无需额外文本码率：

$$c_{aux} = f_c(\hat{\mathbf{x}}_{aux})$$

将内容自适应文本与固定通用描述 $c_{fix}$ 拼接，作为扩散去噪的条件：

$$c = c_{aux} + c_{fix}$$

### 训练目标

整体训练采用标准率失真损失，$\lambda$ 权衡码率与失真：

$$\mathcal{L} = \lambda \mathcal{R} + \mathcal{D}$$

超先验熵模型的编码过程为：

$$\mathbf{z} = h_a(\mathbf{y}), \quad \hat{\mathbf{z}} = \lfloor \mathbf{z} \rfloor, \quad \mathbf{c}_h = h_s(\hat{\mathbf{z}})$$

为稳定极低码率训练，采用两阶段策略：第一阶段用小 $\lambda_{\text{base}}$ 训练基础模型，第二阶段用大 $\lambda_{\text{target}}$ 微调到目标极低码率：

$$\begin{array}{rl}\text{Stage I}: & \arg\min_\theta \mathcal{L}_1 = \lambda_{\text{base}} \mathcal{R} + \mathcal{D}_1 \\ \text{Stage II}: & \arg\min_\theta \mathcal{L}_2 = \lambda_{\text{target}} \mathcal{R} + \mathcal{D}_2 \end{array}$$

### 补充图表

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/008_Figure_7.jpg]]
*Figure 7: Illustration of the textual descriptions extracted from auxiliary reconstructed images under different bitrate conditions*

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/009_Figure_8.jpg]]
*Figure 8: Network structures of the main modules, including the main analysis transform*

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/010_Figure_9.jpg]]
*Figure 9: Illustration of our entropy modeling process*



## 实验与关键发现

### 核心定量结果

CADC在Kodak、DIV2K验证集和CLIC 2020 Professional测试集上，与多个生成式图像压缩方法进行了全面对比。在极低码率条件下，完整CADC模型（M3）在Kodak数据集上实现了LPIPS BD-rate −6.8%和DISTS BD-rate −5.5%的增益（Table 1）。对比的基线方法包括**StableCodec**（Zhang et al., ICCV 2025）、HiFiC、DiffEIC、GLC、DLF、ResULIC、MKIC和OSCAR。在感知质量指标LPIPS、DISTS、FID和KID上，CADC在所有评估数据集上均取得最优结果（Figure 3, Figure 10）。

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/005_Table_1.jpg]]
*Table 1: Ablation studies of our proposed methods on Kodak. Negative BD-rate (%) values indicate better compression performance. The distortion is measured by LPIPS and DISTS*

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/003_Figure_3.jpg]]
*Figure 3: Quantitative comparisons of different generative image codecs on Kodak, DIV2K Val, and CLIC 2020 Test*

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/012_Figure_10.jpg]]
*Figure 10: All rate-distortion curves of different generative image codecs on Kodak, the validation set of DIV2K, and the test set of CLIC 2020 Professional in terms of LPIPS, DISTS, FID, KID, MS-SSIM, and PSNR metrics*

值得注意的是，CADC在编码效率上并未牺牲速度：编码时间仅为0.034秒，与StableCodec的0.030秒基本持平（Table 2）。解码延迟为0.355秒，虽高于DLF等非扩散模型，但在通信上行受限的场景下仍可接受。

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/011_Table_2.jpg]]
*Table 2: Runtime comparison of in seconds averaged on the Kodak dataset*

### 用户偏好研究

在Kodak数据集上的主观用户研究中，CADC获得了58.5%的Top-1偏好率，大幅领先StableCodec（29.0%）和DLF（12.5%）（Table 3）。这一优势在包含复杂纹理的区域尤为明显，DLF和StableCodec在这些区域常出现模糊和色偏等显著伪影（Figure 1, Figure 4）。

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/013_Table_3.jpg]]
*Table 3: Top-1 user preference on the Kodak dataset*

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/001_Figure_1.jpg]]
*Figure 1: A qualitative comparison between our codec, StableCodec [66], and DLF [59] when compressing a 2K-resolution image of the test set of CLIC 2020 Professional [57] under ultra-low bitrate conditions. Our codec produces images with high visual quality, especially in regions with complex texture. In contrast, DLF and StableCodec exhibit noticeable artifacts, such as blurring and color shifting*

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of different generative image codecs on the Kodak dataset under ultra-low bitrate conditions*

### 消融实验：三大组件的贡献

Table 1的消融实验以M0（无任何提出的组件）为基线，逐步叠加UGAQ、ADGIC和BFATC，揭示了各组件的独立贡献：

- **UGAQ（M1 vs M0）**：单独引入不确定性引导的自适应量化，LPIPS BD-rate降低3.7%，DISTS BD-rate降低2.7%。这验证了内容感知噪声整形对扩散先验匹配的关键作用。
- **ADGIC（M2 vs M1）**：在UGAQ基础上加入辅助解码器引导的信息集中，LPIPS BD-rate进一步降低1.6%（累计−5.3%），DISTS BD-rate降低0.8%（累计−3.5%）。Figure 6的能量分析证实，ADGIC显著增强了前4个噪声潜变量通道的信息承载能力。
- **BFATC（M3 vs M2）**：最后引入无码率自适应文本条件化，带来额外的1.5% LPIPS BD-rate增益（累计−6.8%）和2.0% DISTS BD-rate增益（累计−5.5%）。Figure 7展示的文本描述示例表明，即使在极低码率下，辅助重建图像仍能生成语义相关的字幕，为扩散去噪提供有效指导。

### 关键机制分析

**UGAQ与各向同性量化的对比**（Figure 5）：UGAQ通过空间变化的不确定性图调制量化过程，在高不确定性区域施加更强的生成干预，在低不确定性区域保留结构保真度。这形成了内容自适应的有效局部信噪比：

$$\mathrm{SNR}_{i,j} \propto \frac{\mathbb{E}[y_{i,j}^2]}{m_{i,j}^2 \cdot \sigma_{\epsilon}^2}$$

其中不确定性图$m_{i,j} \geq 1$由轻量级网络$f_u$从残差$\mathbf{r} = \mathbf{y} - \overline{\mathbf{z}}$中学习。

**ADGIC的信息集中效应**（Figure 6）：辅助解码器$g_{aux}$仅操作噪声潜变量的前4个通道，通过重建损失$\mathcal{L}_{aux} = \|\mathbf{x} - \hat{\mathbf{x}}_{aux}\|_2^2$强制关键语义信息向主通道集中。能量对比实验直接验证了这一机制的有效性。

**BFATC的语义引导**（Figure 7）：使用冻结的预训练BLIP模型从辅助重建图像生成内容自适应字幕$c_{aux} = f_c(\hat{\mathbf{x}}_{aux})$，与固定通用描述拼接后作为扩散去噪的条件，实现了零额外码率的语义增强。

### 失败模式与局限

尽管CADC在极低码率下表现出色，但存在以下局限：

1. **解码延迟**：0.355秒的解码时间限制了实时交互应用，根源在于扩散去噪的迭代采样过程。
2. **高码率适应性**：模型针对<0.01 bpp的极低码率优化，两阶段训练策略（先小λ基础训练，后大λ微调）在高码率下的表现未经深入验证。
3. **域迁移依赖**：强依赖预训练的Stable Diffusion VAE和BLIP模型，域迁移时可能需要重新适配。
4. **全局量化步长**：UGAQ通过调制间接实现自适应，但量化步长Δ仍为全局值，可能未达到最优化。

### 公平性保障

实验设计采取了多项公平性措施：基线M0（StableCodec变体）移除了原有VAE编码器和辅助编码器，替换为与CADC相同的主分析/合成变换、超先验变换和上下文模型，确保网络架构差异不干扰方法贡献评估。消融研究固定随机种子和训练方案，每种配置运行多次以减少波动。用户研究采用随机化显示顺序和独立参与者的标准Top-1偏好协议。

### 补充图表

![[assets/figures/papers/paper_list_l844_https_arxiv_org_abs_2602_21591/figures/014_Figure_11.jpg]]
*Figure 11: Visual examples and comparisons on 2K-resolution images from the test set of CLIC 2020 Professional*



## 定位与知识库关联

### 与现有生成式图像压缩方法的关系

CADC 处于扩散生成压缩（diffusion-based generative compression）这一新兴脉络中，其直接对话对象是近期将预训练扩散模型引入图像压缩的一系列工作。与 CADC 最相关的基线包括 **StableCodec**（Zhang et al., ICCV 2025）、**DLF**、**HiFiC**、**DiffEIC**、**GLC**、**ResULIC**、**MKIC** 和 **OSCAR** 等。这些方法共享一个基本范式：利用学习型编解码器将图像压缩为紧凑潜表示，再借助扩散模型的生成能力在解码端恢复视觉细节。然而，CADC 与它们的关键分水岭在于对“压缩过程各环节必须动态适应图像内容”这一原则的系统性贯彻。

具体而言，现有扩散压缩方法普遍面临三个结构性瓶颈，CADC 针对每个瓶颈提出了对应的内容自适应机制：

1. **量化策略**：基线方法（包括 StableCodec 等）采用各向同性量化（isotropic quantization），即对所有空间位置应用统一的量化步长和信噪比。这种全局固定策略忽略了图像内容的空间异质性——纹理丰富区域与平坦区域对量化噪声的容忍度截然不同。CADC 的不确定性引导自适应量化（UGAQ）通过学习空间变化的不确定性图 $\mathbf{m} = f_u(\mathbf{r})$ 来调制量化噪声，其中残差 $\mathbf{r} = \mathbf{y} - \overline{\mathbf{z}}$ 捕获了主潜变量与超先验潜变量之间的局部差异。这一设计使解码器输入端形成空间变化的有效信噪比 $\mathrm{SNR}_{i,j} \propto \mathbb{E}[y_{i,j}^2] / (m_{i,j}^2 \cdot \sigma_{\epsilon}^2)$，将扩散模型的噪声相关生成先验与内容特性对齐。

2. **信息集中**：扩散解码器（Stable Diffusion VAE 解码器 $\mathcal{D}_{SD}$）固定接受 4 通道输入，而合成变换 $g_s$ 输出的噪声潜变量 $\boldsymbol{l}_T$ 通常具有高维通道数（如 320）。现有方法将完整的 $\boldsymbol{l}_T$ 输入 UNet $\epsilon_{SD}$ 以利用全部上下文估计噪声，但缺乏显式机制确保关键语义信息集中到前 4 个通道。这构成了信息集中瓶颈。CADC 的辅助解码器引导信息集中（ADGIC）引入轻量级辅助解码器 $g_{aux}$，仅操作 $\boldsymbol{l}_T^{(1:4)}$，通过辅助重建损失 $\mathcal{L}_{aux} = \|\mathbf{x} - \hat{\mathbf{x}}_{aux}\|_2^2$ 强制关键信息汇聚到主通道。

3. **文本条件化**：部分方法传输文本描述以提供语义引导，但消耗额外码率；另一些方法使用固定通用提示，无法提供内容感知的指导。CADC 的无码率自适应文本条件化（BFATC）从辅助重建图像 $\hat{\mathbf{x}}_{aux}$ 出发，利用冻结的 BLIP 模型 $f_c$ 生成内容自适应字幕 $c_{aux}$，再与固定描述 $c_{fix}$ 拼接作为扩散条件 $c = c_{aux} + c_{fix}$。这一设计在不增加文本码率的前提下实现了语义引导。

从方法演进角度看，CADC 可视为对 StableCodec 的架构性改进：消融实验中的基线模型 M₀ 即为移除了原有 VAE 编码器和辅助编码器、替换为与 CADC 相同基础变换模块的 StableCodec 变体。这确保了性能增益可归因于三个内容自适应模块本身，而非底层网络架构差异。

### 适用边界

CADC 的设计和评估高度聚焦于**极低码率场景**（ultra-low bitrate，通常 < 0.01 bpp）。两阶段训练策略——第一阶段用小 $\lambda$ 训练基础模型，第二阶段用大 $\lambda$ 微调到目标极低码率——明确反映了这一优化目标。在此码率区间，传统编解码器的重建质量严重退化，扩散模型的生成能力得以最大化发挥。

该方法对**高分辨率图像**（如 2K 分辨率的 CLIC 2020 Professional 测试集和 DIV2K 验证集）表现出良好的扩展性，这得益于其基于潜空间的扩散解码流程。定性比较（Figure 1、Figure 4、Figure 11-14）显示 CADC 在复杂纹理区域（如织物、毛发、文字）的视觉质量显著优于 DLF 和 StableCodec，后者出现明显模糊和色彩偏移。

然而，CADC 的适用性存在以下边界约束：

- **码率范围**：针对极低码率优化的训练策略和网络配置可能无法直接迁移到中高码率场景。在高码率下，ADGIC 和 BFATC 的相对贡献是否依然显著，以及网络结构是否需要相应调整，目前缺乏深入探讨。
- **域迁移**：方法强依赖于预训练的 Stable Diffusion VAE 解码器和 BLIP 模型。当输入图像域与这些预训练模型的训练分布存在显著偏移时（如医学影像、遥感图像、非自然图像），生成质量和文本条件化的准确性可能下降，需要重新适配。
- **实时性要求**：解码延迟（0.355s，Table 2）高于 DLF 等非扩散方法，尽管编码时间（0.034s）与 StableCodec（0.030s）相当。在需要即时解码反馈的交互式应用中，这一延迟可能构成瓶颈；但在通信上行受限、解码端算力充裕的场景（如卫星图像下传、移动设备云端备份）中是可接受的。

### 局限与开放问题

**已知局限**：

1. **解码延迟**：尽管采用了一步扩散去噪策略，解码过程仍需 0.355 秒（Table 2），主要瓶颈在于 UNet 去噪和 VAE 解码。这限制了在实时交互场景中的部署。
2. **量化步长的全局性**：UGAQ 通过不确定性图 $\mathbf{m}$ 的逐元素调制间接实现了空间自适应量化，但底层量化步长 $\Delta$ 仍为全局值。这种“调制而非直接优化步长”的策略可能未达到最优的信噪比分配。
3. **码率范围单一**：训练和评估集中在极低码率，高码率下的行为未经系统研究。
4. **外部模型依赖**：对 Stable Diffusion VAE 和 BLIP 的依赖引入了额外的模型权重和潜在许可约束，也增加了域迁移时的适配成本。

**开放问题**：

1. **更高效的扩散采样**：能否设计针对压缩场景特化的扩散采样策略（如蒸馏、一致性模型、更激进的步数缩减），将解码延迟进一步降低到接近非扩散生成压缩方法的水平？
2. **噪声调度的理论联系**：UGAQ 的空间变化信噪比调制与扩散模型的理论噪声调度之间是否可以建立更紧密的联系？若能基于扩散过程的噪声水平推导最优的空间 SNR 分配，可能获得更优的率失真性能。
3. **跨模态与跨任务推广**：内容自适应量化的核心思想——从潜表示残差中学习空间不确定性并调制压缩噪声——是否可以推广到视频压缩（时域不确定性）、三维表示压缩，或其他生成模型（如基于流的模型、自回归模型）？
4. **高码率下的贡献分配**：在更高码率下，生成能力的重要性相对下降，而保真度要求上升。ADGIC 的信息集中机制和 BFATC 的语义引导在高码率下的相对贡献是否依然显著？是否需要对网络容量和损失权重进行结构性调整？
5. **不确定性估计的替代路径**：当前不确定性图 $\mathbf{m}$ 来源于主潜变量与超先验潜变量的残差 $\mathbf{r}$。是否存在更直接的不确定性估计方式（如基于熵模型的概率分布、基于梯度的显著性）能进一步提升自适应量化的效果？



## 原文 PDF

![[paperPDFs/CVPR_2026/CADC_Content_Adaptive_Diffusion_Based_Generative_Image_Compression.pdf]]

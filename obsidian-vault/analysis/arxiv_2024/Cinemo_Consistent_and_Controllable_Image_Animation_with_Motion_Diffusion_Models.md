---
title: "Cinemo: Consistent and Controllable Image Animation with Motion Diffusion Models"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Cinemo_Consistent_and_Controllable_Image_Animation_with_Motion_Diffusion_Models.pdf
aliases:
- Cinemo
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过运动残差学习（建模相邻帧的差异而非直接预测画面）以及基于离散余弦变换的推理噪声初始化（DCTInit），模型在训练和推理阶段分别有效缓解了细节丢失和运动突变的因果因素。
primary_logic: 将图像动画问题分解为运动残差学习、运动强度控制与运动突变缓解三个子问题，并分别设计针对性的训练目标（残差预测+SSIM强度编码）和推理策略（DCT低频引导），能够同步提升时间一致性和用户可控的运动生成质量。
claims:
- 在UCF-101和MSR-VTT基准上，Cinemo在FVD、IS、FID、CLIPSIM等指标上全面超越现有方法
- DCTInit消融实验表明，去除DCTInit后生成视频出现显著运动突变和颜色不一致（Fig. 5）
- 通过调节SSIM运动强度桶，用户可以精细控制生成视频的运动幅度（Fig. 6）
- UCF-101 上 FVD = 168.16
---

# Cinemo: Consistent and Controllable Image Animation with Motion Diffusion Models

> [!tip] 核心洞察
> 将图像动画问题分解为运动残差学习、运动强度控制与运动突变缓解三个子问题，并分别设计针对性的训练目标（残差预测+SSIM强度编码）和推理策略（DCT低频引导），能够同步提升时间一致性和用户可控的运动生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Cinemo：一致且可控的图像动画与运动扩散模型 |
| 英文题名 | Cinemo: Consistent and Controllable Image Animation with Motion Diffusion Models |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2407.15642) · [Project](https://maxin-cn.github.io/cinemo\_project) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Cinemo |
| Dataset | UCF-101, MSR-VTT |

> [!tip] 效果简介
> - UCF-101 上，FVD 168.16；IS 58.71；FID 13.17。
> - MSR-VTT 上，FVD 93.51；CLIPSIM 0.2858。

## 概述

**核心问题**：图像动画（image animation）任务要求从单张静态图像和文本提示生成连贯的动态视频。现有方法面临两个相互耦合的瓶颈——**细粒度视觉一致性**难以保持（物体形状、纹理、背景在帧间出现失真），以及**运动可控性**不足（生成的运动模式与文本提示脱节或出现不期望的全局移动）。

**核心洞见**：Cinemo 将图像动画问题分解为三个可独立优化的子问题——运动残差学习、运动强度控制与运动突变缓解——并分别设计针对性的因果干预机制，从而同步提升时间一致性与用户可控的运动生成质量。

**方法定位**：Cinemo 以 LaVie 文本到视频扩散模型为骨干，提出三项关键改进：
1. **预测目标重构**：不直接预测后续帧的潜变量，而是学习运动残差（后续帧减去第一帧）的分布，从根本上缓解内容失真。
2. **运动强度可控嵌入**：基于帧间平均 SSIM 计算运动强度，并将其量化为桶嵌入注入时间步条件，提供从静态到快速运动的细粒度控制。
3. **推理噪声初始化（DCTInit）**：利用离散余弦变换提取输入图像的低频分量，与随机噪声的高频分量组合作为初始推理噪声，有效抑制运动突变和颜色不一致。

**主要结果**：在 UCF-101 和 MSR-VTT 基准上，Cinemo 在 FVD、IS、FID、CLIPSIM 等指标上全面超越 PIA、DynamiCrafter、ConsistI2V 等现有图像动画方法（Tab. 1）。消融实验证实 DCTInit 对减少运动突变和保持色彩一致性有决定性作用（Fig. 5），而 SSIM 运动强度桶使用户可精细调节生成视频的运动幅度（Fig. 6）。

**局限与开放问题**：当前模型受限于 LaVie 架构的能力边界，仅支持 16 帧、320×512 分辨率的视频生成；向 Transformer 架构（如 Latte）迁移、扩展到更长视频和更高分辨率，以及验证 DCTInit 和运动强度控制策略在其他视频扩散模型上的泛化性，是值得探索的方向。

## 背景与动机

图像动画任务旨在将一幅静态图像与一段文本提示相结合，生成一段时间连贯且语义匹配的动态视频。该任务在影视特效、虚拟数字人、交互式内容创作等领域具有广泛的应用前景。然而，现有方法在同时满足**视觉一致性**（保持输入图像的形状、纹理、背景等细粒度信息）和**运动可控性**（精确响应文本提示所描述的运动模式）方面仍面临显著挑战。

当前的主流基线方法（如 **PIA**、**SEINE**、**DynamiCrafter** 等）在图像动画生成中暴露出两类典型失效模式。如 Figure 1 所示，当给定“风车转动”的文本提示时，PIA 生成的视频帧之间出现明显的颜色和纹理差异，破坏了视觉一致性；SEINE 则将整个房屋连同风车一起移动，未能精确响应文本提示中仅“风车”应转动的语义约束，导致运动偏差。这些案例揭示了现有方法的共同瓶颈：**难以在保持输入图像细粒度视觉特征的同时，生成与文本提示精确对齐的运动模式**。

从因果机制分析，上述瓶颈的根源在于两个层面：

1. **训练目标的偏差**：传统方法通常直接预测后续帧的完整图像潜变量。这种“全局重建”范式使得模型倾向于学习平均化的静态外观，导致生成视频出现内容失真或静态化倾向，无法有效保留输入图像的细节纹理和背景结构。
2. **推理阶段的运动突变**：标准扩散模型在推理时采用纯随机噪声初始化，缺乏对输入图像空间布局的先验约束。这使得生成过程在初始阶段缺乏低频结构引导，容易产生运动突变、颜色偏移等时间不一致性问题。

针对上述问题，**Cinemo** 提出了三个核心设计思路：通过**运动残差学习**替代直接帧预测，将模型的学习目标从“重建画面”转变为“建模变化”，从而在因果层面缓解细节丢失问题；引入基于**结构相似度（SSIM）的运动强度控制**机制，使用户能够精细调节生成视频的运动幅度；设计**DCTInit 推理噪声初始化策略**，利用离散余弦变换的低频系数为推理过程提供输入图像的结构先验，有效抑制运动突变。这三个设计分别对应训练目标、可控性接口和推理策略三个关键环节，共同构成了一个面向一致且可控图像动画的系统性解决方案。

## 核心创新

Cinemo 的核心创新在于将图像动画问题分解为三个因果性子问题，并分别设计针对性的机制加以解决，从而在保持输入静态图像细粒度视觉一致性的同时，实现对运动模式的精确响应。

### 1. 预测目标重构：从直接帧预测到运动残差学习

现有方法（如 PIA、SEINE、DynamiCrafter 等）通常直接预测后续帧的图像潜变量，这导致模型倾向于生成静态画面或出现纹理、颜色失真（见 **Figure 1** 中的失败案例）。Cinemo 改变了这一预测目标：**模型学习的是运动残差的分布，而非直接预测后续帧**。

具体而言，给定 VAE 编码后的视频帧潜变量序列 $\mathbf{Z} = \{z_1, z_2, ..., z_N\}$，运动残差定义为后续帧与第一帧的差值：

$$\mathbf{M} = \{z_2 - z_1, z_3 - z_1, ..., z_N - z_1\}$$

扩散模型在训练时对 $\mathbf{M}$ 加噪并学习去噪，而非对原始帧潜变量操作（**Algorithm 1**）。这一设计使模型专注于学习帧间的“变化量”，从而天然保持第一帧的视觉内容不变，有效缓解了内容失真和静态预测倾向。消融实验的定性结果（**Figure 4**）表明，与直接预测相比，运动残差学习策略避免了静态预测和内容失真的问题。

### 2. 运动强度控制：基于 SSIM 的细粒度调节机制

现有方法缺乏对运动幅度的显式控制手段，或仅能通过 FPS/光流进行粗粒度调节。Cinemo 提出了一种**基于结构相似度（SSIM）的运动强度编码与注入策略**。

对于视频 $\mathbf{V}$，其运动强度定义为连续帧之间的平均 SSIM：

$$s(\mathbf{V}) = \frac{1}{N-1} \sum_{i=2}^{N} SSIM(x_i, x_{i-1})$$

该值被离散化映射到预定义的“运动强度桶”（motion intensity bucket）$b$ 中，并以嵌入形式注入扩散模型的时间步条件。最终训练目标整合了运动残差学习和运动强度控制：

$$\mathcal{L}_{final} = \mathbb{E}_{\mathbf{z} \sim p(z), \epsilon \sim \mathcal{N}(0,1), t} \left[ \left\| \epsilon - \epsilon_{\theta}(\mathbf{X}_t, p, b, t) \right\|_2^2 \right]$$

其中 $p$ 为文本提示，$b$ 为运动强度桶嵌入。在推理阶段，用户可通过设置不同的 $b$ 值实现从静态到快速运动的精细控制（**Figure 6**），这是现有基线方法所不具备的能力。

### 3. 推理阶段噪声初始化：DCTInit 缓解运动突变

标准扩散模型在推理时使用纯随机噪声初始化，这容易导致生成视频出现运动突变和颜色不一致。Cinemo 提出 **DCTInit** 策略，利用离散余弦变换（DCT）对初始推理噪声进行细化。

具体做法是：将输入静态图像的加噪版本 $z_1^\tau$ 与随机噪声 $\epsilon$ 分别进行 DCT 分解，提取前者低频系数 $D_{z_1^\tau}^L$（保留图像布局信息）和后者高频系数 $D_\epsilon^H$（保留细节多样性），通过逆 DCT 组合得到细化噪声 $\epsilon' = IDCT(D_{z_1^\tau}^L + D_\epsilon^H)$。与 FFT 分解相比，DCT 能更好地保持生成视频的颜色一致性（**Figure 3**）。消融实验（**Figure 5**）表明，去除 DCTInit 后生成视频出现显著运动突变和颜色不一致，验证了该策略对时间一致性的关键作用。

### 创新维度总结

| 创新维度 | 基线做法 | Cinemo 方案 | 因果机制 |
|---------|---------|------------|---------|
| 预测目标 | 直接预测帧潜变量 | 预测运动残差 $\mathbf{M}$ | 解耦静态内容与动态变化，保持第一帧一致性 |
| 运动控制 | 无显式控制或全局粗调 | SSIM 运动强度桶嵌入 | 帧间结构相似度编码为可调节的条件信号 |
| 噪声初始化 | 纯随机噪声 | DCTInit 低频/高频分解重组 | 低频提供布局先验，高频保留生成多样性 |

这三个创新点形成了协同效应：运动残差学习保证了内容一致性，SSIM 强度控制提供了用户可控的运动幅度，DCTInit 则在推理阶段进一步稳定了时间连续性。三者共同构成了 Cinemo 相对于现有图像动画方法的根本性改进。

## 整体框架

Cinemo 的整体流程遵循“训练阶段学习运动残差分布 + 推理阶段精细化噪声初始化”的双阶段设计，其核心架构如图 2 所示。模型接收一张静态 RGB 图像与一段文本提示作为输入，输出一段与图像内容一致且与文本语义对齐的动画视频。

**潜空间编码与运动残差计算。** 给定输入视频帧序列 $\mathbf{V} = \{x_1, x_2, \dots, x_N\}$，首先通过预训练的 VAE Encoder 将所有帧压缩至潜空间，得到潜变量序列 $\mathbf{Z} = \{z_1, z_2, \dots, z_N\}$。与传统方法直接预测后续帧不同，Cinemo 计算运动残差 $\mathbf{M} = \{z_2 - z_1, z_3 - z_1, \dots, z_N - z_1\}$，即每一帧潜变量与第一帧潜变量的差值。这一设计的因果逻辑在于：模型只需学习帧间的变化量，而非重建完整的帧内容，从而将第一帧的细粒度视觉信息（纹理、形状、背景）天然保留在最终输出中，缓解内容失真问题。

**运动强度可控的条件去噪。** 运动残差 $\mathbf{M}$ 被送入以 LaVie 为骨干的运动扩散模型进行去噪训练。模型的条件信号包含两部分：文本提示 $p$ 和运动强度桶嵌入 $b$。运动强度由连续帧之间的平均结构相似度（SSIM）量化：

$$s(\mathbf{V}) = \frac{1}{N-1} \sum_{i=2}^{N} SSIM(x_i, x_{i-1})$$

该值被离散化映射到预定义的桶中，作为时间步嵌入的一部分注入去噪网络。最终训练目标为：

$$\mathcal{L}_{final} = \mathbb{E}_{\mathbf{z} \sim p(z), \epsilon \sim \mathcal{N}(0,1), t} \left[ \left\| \epsilon - \epsilon_{\theta}(\mathbf{X}_t, p, b, t) \right\|_2^2 \right]$$

其中 $\mathbf{X}_t$ 为加噪后的运动残差，$\epsilon_{\theta}$ 为去噪网络。训练数据采用 WebVid-10M 和 Vimeo25M，每段视频采样 16 帧、分辨率为 320×512、帧间隔为 3–10。

**推理阶段的 DCTInit 噪声初始化。** 标准扩散模型在推理时从纯随机噪声开始去噪，容易导致生成视频出现运动突变和颜色不一致。Cinemo 提出 DCTInit 策略：对输入静态图像的加噪版本 $z_1^{\tau}$ 进行离散余弦变换（DCT），提取其低频系数 $D_{z_1^{\tau}}^L$；同时从随机噪声 $\epsilon$ 的 DCT 分解中提取高频系数 $D_{\epsilon}^H$。将两者组合后经逆 DCT 得到精细化噪声 $\epsilon' = IDCT(D_{z_1^{\tau}}^L + D_{\epsilon}^H)$，作为推理的初始噪声。低频分量提供了图像的全局布局和颜色信息，高频分量保留了生成多样运动所需的随机性，从而在保持视觉一致性的同时允许合理的运动变化。消融实验（Fig. 5）证实，去除 DCTInit 后生成视频出现显著运动突变和色彩不一致。

**输入输出流总结。** 推理时，用户提供一张静态图像和文本提示，并可选择指定运动强度桶来控制运动幅度。图像经 VAE Encoder 编码后参与 DCTInit 噪声初始化，随后运动扩散模型在文本和运动强度条件的引导下进行 DDIM 去噪（50 步，classifier-free guidance scale 7.5），生成运动残差潜变量。最终将运动残差与第一帧潜变量相加，经 VAE Decoder 解码得到动画视频帧序列。

**模块关系与职责分工。** 五个核心模块形成清晰的分工：VAE Encoder/Decoder 负责潜空间压缩与重建；Motion Residual Computation 将帧预测问题转化为残差学习问题；SSIM-based Motion Intensity Embedding 提供用户可控的运动幅度调节；Motion Diffusion Model（LaVie 骨干）执行条件去噪生成；DCTInit Noise Refinement 在推理端稳定生成过程。三个关键设计——运动残差学习、SSIM 强度控制、DCTInit——分别针对内容一致性、运动可控性和时间稳定性三个瓶颈问题，形成互补的因果干预体系。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/002_Figure_2.jpg]]
*Figure 2: Model pipeline overview. During training, instead of predicting the subsequent frames directly, our model learns the distribution of motion residuals, while providing effective motion intensity control. The details of the training procedure can be seen in Algorithm. 1. During inference, we use Discrete Cosine Transformation to extract low-frequency components to refine the inference noise, which can stabilize the generation process of image animation*

## 核心模块与公式推导

### 3.1 运动残差学习（Motion Residual Learning）

传统图像动画方法直接预测后续帧的潜变量，容易导致内容失真和静态预测问题。Cinemo 的核心改变在于将预测目标从“绝对帧”转换为“运动残差”：给定输入视频的潜变量序列 $\mathbf{Z} = \{z_1, z_2, ..., z_N\}$，运动残差定义为

$$\mathbf{M} = \{z_2 - z_1, z_3 - z_1, ..., z_N - z_1\}$$

模型学习的是运动残差 $\mathbf{M}$ 的分布，而非直接预测 $z_2, ..., z_N$。在推理阶段，通过将预测的残差加回第一帧 $z_1$ 来重建完整视频。这一策略的因果逻辑在于：残差信号天然剥离了静态背景和物体外观信息，使扩散模型专注于运动模式建模，从而缓解了直接预测带来的细节丢失和内容漂移。

### 3.2 基于 SSIM 的运动强度控制

为实现细粒度的运动幅度可控性，Cinemo 引入基于结构相似度（SSIM）的运动强度编码机制。首先计算连续帧之间的平均 SSIM 作为运动强度度量：

$$s(\mathbf{V}) = \frac{1}{N-1} \sum_{i=2}^{N} SSIM(x_i, x_{i-1})$$

其中 $x_i$ 为第 $i$ 帧的像素空间图像。该值越低表示帧间差异越大、运动越剧烈。随后将 $s(\mathbf{V})$ 映射到离散的运动强度桶 $b$，并通过嵌入层注入扩散模型的时间步条件中，使得模型在训练阶段学会根据不同的运动强度桶生成相应幅度的运动。

### 3.3 最终训练目标

结合运动残差学习和运动强度控制，Cinemo 的最终训练损失函数为：

$$\mathcal{L}_{final} = \mathbb{E}_{\mathbf{z} \sim p(z), \epsilon \sim \mathcal{N}(0,1), t} \left[ \left\| \epsilon - \epsilon_{\theta}(\mathbf{X}_t, p, b, t) \right\|_2^2 \right]$$

其中 $\mathbf{X}_t$ 为加噪后的运动残差潜变量，$p$ 为文本提示条件，$b$ 为运动强度桶嵌入，$\epsilon_{\theta}$ 为基于 LaVie 骨干的去噪网络。该目标在标准潜扩散简单损失（Eq. 1）的基础上增加了运动强度条件维度，使模型同时具备文本响应能力和运动幅度可控性。

### 3.4 DCTInit：推理阶段噪声初始化

标准扩散模型推理从纯随机噪声 $\epsilon \sim \mathcal{N}(0,1)$ 开始，容易导致生成视频出现运动突变和颜色不一致。DCTInit 的核心思想是利用离散余弦变换（DCT）将输入静态图像的结构信息注入初始噪声：提取输入图像加噪版本的 DCT 低频系数 $D_{z_1^{\tau}}^L$，与随机噪声的 DCT 高频系数 $D_{\epsilon}^H$ 组合，再通过逆 DCT 得到精炼后的初始噪声：

$$\epsilon' = IDCT(D_{z_1^{\tau}}^L + D_{\epsilon}^H)$$

低频分量保留了图像的全局布局和颜色分布，高频分量提供生成多样性。相比于 FFT 分解，DCT 在保持色彩一致性方面表现更优（见 Fig. 3）。该模块仅在推理阶段使用，无需额外训练。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/003_Figure_3.jpg]]
*Figure 3: Influence of the FFT and DCT decomposition. The prompt is*

## 实验与分析

### 主实验结果

Cinemo在UCF‑101和MSR‑VTT两个标准基准上进行了系统评估，与**PIA**、**SEINE**、**DynamiCrafter**、**ConsistI2V**、**I2V-Adapter**等图像动画基线以及**VideoCrafter1**等文本到视频基线进行了全面对比。所有方法均在相同的测试子集上评估，采用统一的DDIM 50步推理和classifier-free guidance scale 7.5。

**Table 1** 展示了定量对比的核心结果。在UCF‑101基准上，Cinemo取得了FVD 168.16、IS 58.71、FID 13.17，在所有指标上均显著优于对比方法。在MSR‑VTT基准上，Cinemo的FVD降至93.51，CLIPSIM达到0.2858，进一步验证了其在视频质量（FVD衡量时间一致性）和语义对齐（CLIPSIM衡量文本-视频匹配度）两个维度上的综合优势。

这些定量优势的因果根源在于三个相互协同的设计选择：运动残差学习避免了直接预测完整帧带来的内容失真，SSIM运动强度编码使模型在训练期间就学会了区分不同运动幅度下的残差分布，而DCTInit则在推理阶段稳定了生成过程，减少了突变伪影对FVD等时序指标的影响。

### 消融实验

**运动残差学习的定性验证（Figure 4）**：与直接预测后续帧的策略相比，运动残差学习有效避免了静态预测和内容失真问题。Figure 4展示了Cinemo与多个基线（包括商业闭源工具）的定性对比结果，Cinemo生成的动画在保持输入图像纹理、形状和背景细节的同时，准确响应了文本提示的运动模式。

**DCTInit消融（Figure 5）**：去除DCTInit后，生成的视频出现显著的运动突变和颜色不一致。Figure 5以“woman smiling”为提示，对比了启用和未启用DCTInit的生成结果：中间未启用DCTInit的视频在帧间出现明显的色彩漂移和运动不连贯，而启用DCTInit后视频保持了稳定的色彩一致性和平滑的运动过渡。这验证了DCT低频系数引导初始推理噪声的策略对缓解运动突变的关键作用。

**运动强度可控性验证（Figure 6）**：通过调节SSIM运动强度桶嵌入，用户可以从静态到快速运动进行精细调整。Figure 6以“shark swimming”为提示，展示了不同运动强度桶设置下的生成效果，证实了基于平均SSIM的运动强度编码提供了细粒度、可解释的运动控制能力。

### 失败模式与局限性

尽管Cinemo在定量和定性评估中表现优异，其性能仍受限于以下因素：

1. **基础模型能力瓶颈**：Cinemo基于LaVie T2V架构构建，其生成质量和语义对齐的上限受LaVie能力和训练数据分布（WebVid-10M、Vimeo25M）的制约。当输入图像或文本提示超出训练分布时，生成质量可能下降。

2. **视频长度与分辨率限制**：当前模型仅支持16帧、320×512分辨率的视频生成。扩展到更长视频或更高分辨率需要额外的架构设计，例如引入时序注意力机制或级联生成策略。

3. **架构探索不充分**：未探索基于Transformer架构的视频扩散模型（如Latte）的适用性。当基础模型从U-Net切换到Transformer时，运动残差学习、SSIM强度控制和DCTInit三大策略是否依然有效且能进一步提升性能，仍是一个开放问题。

### 重要图表结论

- **Figure 4**：定性对比表明，Cinemo在保持细粒度视觉一致性（物体形状、纹理、背景）和响应文本提示的运动模式方面，均优于现有图像动画基线。
- **Figure 5**：DCTInit是缓解运动突变和色彩不一致的关键推理策略，去除后视频质量显著退化。
- **Figure 6**：SSIM运动强度桶嵌入实现了用户可控的运动幅度调节，验证了运动强度控制设计的有效性。
- **Table 1**：Cinemo在UCF‑101和MSR‑VTT的FVD、IS、FID、CLIPSIM指标上全面超越现有方法，定量证明了运动残差学习、强度控制与DCTInit三者协同设计的优越性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons between the baselines and our model. ↓ means the lower the better. ↑ means the higher the better*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/006_Figure_5.jpg]]
*Figure 5: Effectiveness of DCTInit. The middle video is generated by our model without enabling DCTInit. The prompt is “woman smiling”. Best viewed with Acrobat Reader. Please click the image to view the animated videos*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/008_Figure_6.jpg]]
*Figure 6: Motion intensity controllability. The prompt is “shark swimming”. Our model allows users to control the motion intensity by setting the input-associated information to different values. Best viewed with Acrobat Reader. Please click the image to view the animated videos*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative visual comparisons between the baselines and our model. We compare our approach with both closed-source commercial tools and research works. “Girl smiling” means the used prompt when the method accepts it. Best viewed with Acrobat Reader. Please click the image to view the animated videos*

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/001_Figure_1.jpg]]
*Figure 1: Explanations of image consistency and motion controllability. Frames in (b) and (c) are image animation results obtained from PIA [21] and SEINE [31], respectively. We use “windmill turning” as the text descriptions. (b) The frames show clear differences in color and texture. In (c), the entire house is moving, which does not match the information provided in the textual prompt*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2407_15642/figures/009_Figure_8.jpg]]
*Figure 8: Motion transfer/Video editing results. Our model can easily extend to other applications. Best viewed with Acrobat Reader. Please click the image to view the animated videos*

## 方法谱系与知识库定位

### 1. 在图像动画与视频扩散模型谱系中的位置

图像动画任务近年来经历了从基于GAN的方法向扩散模型的迁移。Cinemo 处于**视频扩散模型驱动的图像动画**这一新兴分支，其直接竞争对手包括：

- **PIA**：基于图像提示适配器的动画方法，但存在严重的纹理和颜色不一致问题（Fig. 1）。
- **SEINE**：视频预测/图像动画方法，但运动模式难以精确匹配文本提示，常出现整体场景平移而非局部运动（Fig. 1）。
- **DynamiCrafter**、**ConsistI2V**、**I2V-Adapter**：同期图像动画基线，在 Tab. 1 的定量对比中全面落后于 Cinemo。
- **VideoCrafter1**：文本到视频基线，缺乏对输入静态图像的细粒度一致性约束。

Cinemo 的核心技术基座是 **LaVie** 文本到视频扩散模型，因此其生成质量和语义对齐能力天然受限于 LaVie 的架构上限和训练数据分布。这构成了其方法谱系中的**基础能力边界**。

### 2. 方法差异化的三个关键维度

Cinemo 相对于上述基线的本质差异体现在三个因果性设计选择上：

| 设计维度 | 基线做法 | Cinemo 做法 | 因果机制 |
|---------|---------|------------|---------|
| **预测目标** | 直接预测后续帧的潜变量 | 预测运动残差（后续帧减去第一帧） | 将模型容量集中于学习时序变化而非静态内容，缓解内容失真 |
| **运动强度控制** | 无显式控制或基于FPS的全局调节 | 基于平均SSIM的运动强度桶嵌入 | 提供细粒度的用户可控性，使运动幅度可精确调节（Fig. 6） |
| **推理噪声初始化** | 标准随机高斯噪声 | DCTInit：DCT低频系数与随机噪声高频结合 | 为生成过程提供输入图像的结构先验，缓解运动突变和颜色漂移（Fig. 5） |

这三个设计并非孤立改进，而是分别对应**视觉一致性保持**、**运动幅度可控**、**时序稳定性**三个子问题，形成互补的解决方案。

### 3. 适用边界与已知局限

**适用场景**：
- 单张静态图像到短视频（16帧）的动画生成
- 支持文本提示驱动的运动控制（Fig. 7）
- 可扩展至运动迁移和视频编辑任务（Fig. 8）

**明确局限**（来自论文自身分析）：
1. **架构依赖瓶颈**：模型基于 LaVie 的 U-Net 骨干，未探索 Transformer 架构（如 Latte）的适用性，可能限制性能上限。
2. **时空分辨率限制**：当前仅支持 16 帧、320×512 分辨率的视频生成，扩展到更长视频或更高分辨率需要额外设计。
3. **数据分布约束**：训练数据为 WebVid-10M 和 Vimeo25M，生成内容的语义多样性和质量受限于这两个数据集的分布。

### 4. 开放问题与可能的后续方向

基于论文的讨论和方法边界，以下问题值得关注：

1. **架构迁移的泛化性**：当将 Cinemo 的三大策略（运动残差学习、SSIM强度控制、DCTInit）移植到 Transformer 架构的视频扩散模型（如 Latte）时，是否依然有效？这涉及 U-Net 和 Transformer 在时序建模上的本质差异。

2. **长视频与高分辨率扩展**：如何将模型扩展到 16 帧以上和 512p 以上分辨率，同时保持视觉一致性和运动可控性？这可能需要层次化生成策略或时序注意力机制的重新设计。

3. **策略的跨任务泛化**：DCTInit 和运动强度控制策略是否可泛化至其他视频扩散任务（如通用文本到视频生成、视频编辑、视频预测）？这涉及这些策略是否利用了图像动画任务特有的结构先验。

4. **运动强度控制的客观评价**：当前 SSIM 运动强度桶的控制效果主要通过定性展示（Fig. 6），缺乏客观的量化指标来衡量控制精度和线性度，这限制了该模块的系统性优化。

**注意**：上述开放问题第1、3点来自论文自身的讨论，第2、4点需要进一步实验验证。

## 原文 PDF

![[paperPDFs/arxiv_2024/Cinemo_Consistent_and_Controllable_Image_Animation_with_Motion_Diffusion_Models.pdf]]
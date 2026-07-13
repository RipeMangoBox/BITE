---
title: "EMR-Diff: Edge-aware Multimodal Residual Diffusion Model for Hyperspectral Image Super-resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EMR_Diff_Edge_aware_Multimodal_Residual_Diffusion_Model_for_Hyperspectral_Image_Super_resolution.pdf
project_link: null
code_link: "https://github.com/luocz55/EMR-Diff"
aliases:
- EMR-Diff
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在扩散过程中引入多模态残差传递和边缘感知噪声调制
primary_logic: 将多模态残差嵌入马尔可夫链可以显著减少扩散步数，同时利用HR-MSI边缘信息引导噪声使模型专注于高频细节重建
claims:
- 在ICVL、Harvard、Chikusei三个数据集上，EMR-Diff在PSNR/SSIM/SAM/ERGAS四项指标上均取得最优
- 多模态残差机制相比于无残差方案PSNR提升1.35 dB，相比于单模态残差提升0.82 dB
- 边缘感知噪声相比于纯高斯噪声PSNR提升0.92 dB
- BAF-UNet中的MSGAB模块相比普通残差块PSNR提升1.06 dB
---

# EMR-Diff: Edge-aware Multimodal Residual Diffusion Model for Hyperspectral Image Super-resolution

> [!tip] 核心洞察
> 将多模态残差嵌入马尔可夫链可以显著减少扩散步数，同时利用HR-MSI边缘信息引导噪声使模型专注于高频细节重建

| 字段 | 内容 |
|------|------|
| 中文题名 | EMR-Diff: 边缘感知多模态残差扩散模型用于高光谱图像超分辨率 |
| 英文题名 | EMR-Diff: Edge-aware Multimodal Residual Diffusion Model for Hyperspectral Image Super-resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_EMR-Diff_Edge-aware_Multimodal_Residual_Diffusion_Model_for_Hyperspectral_Image_Super-resolution_CVPR_2026_paper.html) · [Code](https://github.com/luocz55/EMR-Diff) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | EMR-Diff |
| Dataset | ICVL, Harvard, Chikusei |

> [!tip] 效果简介
> - ICVL 上，PSNR/SSIM/SAM/ERGAS 55.40/0.9997/0.0040/0.1588。
> - Harvard 上，PSNR/SSIM/SAM/ERGAS 49.28/0.9990/0.0233/0.7800。
> - Chikusei 上，PSNR/SSIM/SAM/ERGAS 47.55/0.9980/0.0950/1.4943。

## 概要

高光谱图像（HSI）超分辨率的任务是从低分辨率高光谱图像（LR-HSI）和高分辨率多光谱图像（HR-MSI）的融合中恢复高分辨率高光谱图像（HR-HSI）。扩散模型在该任务中面临三个核心瓶颈：采样效率低（通常需要数百至上千步）、细节生成受限、以及去噪过程对高频信息关注不足。

EMR-Diff 通过两项关键机制突破这些瓶颈。**多模态残差传递**将 HR-HSI 与（上采样 LR-HSI + HR-MSI）之间的联合差异 $\mathcal{E}_0$ 注入扩散马尔可夫链，使信息在模态间高效流动，仅需 **5 步**即可完成扩散过程。**边缘感知噪声调制**利用 HR-MSI 的 Sobel 梯度强度对高斯噪声进行加权，在边缘区域施加更强的噪声扰动，引导去噪网络优先重建高频细节。

在去噪网络层面，BAF-UNet 采用双路径设计（噪声输入路径 + 多模态引导路径），结合多尺度分组注意力模块（MSGAB）和多尺度监督损失，进一步提升了重建精度。

在 ICVL、Harvard、Chikusei 三个标准数据集上，EMR-Diff 在 PSNR、SSIM、SAM、ERGAS 四项指标上均取得最优结果（Table 1）。消融实验证实：多模态残差相比无残差方案 PSNR 提升 1.35 dB（Table 2），边缘感知噪声相比纯高斯噪声提升 0.92 dB（Table 3），MSGAB 模块相比普通残差块提升 1.06 dB（Table 4）。



高光谱图像（HSI）超分辨率旨在从低分辨率高光谱图像（LR-HSI）与高分辨率多光谱图像（HR-MSI）中重建高分辨率高光谱图像（HR-HSI），其观测模型可形式化为：

$$\mathcal{V} = \mathcal{D}(B(\mathcal{X})), \quad \mathcal{Z} = \mathbf{R}\mathcal{X}$$

其中 $\mathcal{X}$ 为待重建的 HR-HSI，$\mathcal{V}$ 为经模糊 $B$ 和下采样 $\mathcal{D}$ 后的 LR-HSI，$\mathcal{Z}$ 为经光谱响应矩阵 $\mathbf{R}$ 退化得到的 HR-MSI。该任务的核心挑战在于：从严重欠定的多模态观测中恢复高频空间细节与高保真光谱信息。

近年来，扩散模型在图像生成与恢复任务中展现出强大的分布拟合能力，但其在 HSI 超分辨率中的应用面临三个关键瓶颈：**采样效率低**——标准 DDPM 需数百步迭代推理，计算成本高昂；**细节生成受限**——纯高斯噪声缺乏对图像结构的先验引导，模型难以聚焦于高频边缘区域的恢复；**去噪不充分**——现有 UNet 架构未能有效融合多模态互补信息，导致光谱保真度与空间细节难以兼顾。

针对上述缺口，EMR-Diff 提出了三个核心设计动机：第一，将多模态残差嵌入马尔可夫链以加速信息传递，使扩散过程在极少数步内完成；第二，利用 HR-MSI 的边缘信息调制噪声分布，引导模型优先关注高频细节区域；第三，构建双路径去噪网络 BAF-UNet，通过模态特定分支与多尺度监督实现精细的多模态融合。这些设计共同指向一个目标：在保持扩散模型生成质量优势的同时，大幅提升推理效率与细节重建精度。



## 核心方法与创新机理

EMR-Diff 的核心创新在于将多模态残差传递与边缘感知噪声调制引入扩散模型的马尔可夫链，从而在仅需 5 个扩散步骤的条件下实现高光谱图像超分辨率重建。该方法在三个关键维度上对标准扩散范式进行了改造：

### 扩散过程设计：从纯噪声退化到多模态残差传递

标准 DDPM 通过逐步添加纯高斯噪声来破坏数据，通常需要数百甚至上千个步骤才能完成正向扩散与反向去噪。EMR-Diff 的出发点在于：HSI 超分辨率任务天然拥有两种互补的退化观测——低分辨率高光谱图像（LR-HSI）与高分辨率多光谱图像（HR-MSI）。与其让模型从纯噪声中重建，不如将这两种模态与目标 HR-HSI 之间的**联合差异**（即多模态残差 $\mathcal{E}_0$）作为扩散过程中传递的信息载体。

具体而言，正向扩散的起点 $\mathcal{X}_0'$ 被设为 HR-HSI，而 $\mathcal{A}_0$ 是上采样后的 LR-HSI 与 HR-MSI 在通道维度的拼接。多模态残差定义为：
$$\mathcal{E}_0 = \mathcal{A}_0 - \mathcal{X}_0'$$
这一残差编码了“两种退化观测联合起来与真实高分辨率目标之间的差距”。正向扩散过程不再单纯添加高斯噪声，而是按照单调递增序列 $\eta_t$ 逐步将 $\mathcal{E}_0$ 注入 $\mathcal{X}_t'$：
$$\mathcal{X}_t' = \mathcal{X}_0' + \eta_t \mathcal{E}_0 + \kappa \sqrt{\eta_t} N_*$$
反向过程则对称地回传残差：
$$\mathcal{X}_{t-1}' = \frac{\eta_{t-1}}{\eta_t} \mathcal{X}_t' + \frac{\alpha_t}{\eta_t} f_\theta(\mathcal{X}_t', \mathcal{A}_0, t) + \kappa \sqrt{\frac{\eta_{t-1}}{\eta_t} \alpha_t} N_*$$
这一设计使得扩散链的信息传递效率大幅提升——消融实验表明，多模态残差机制相比无残差方案 PSNR 提升 1.35 dB，相比仅使用单一模态残差提升 0.82 dB（Table 2）。扩散步数也因此可以压缩至 5 步即可达到最佳性能（Table 5）。

### 噪声类型：从各向同性高斯噪声到边缘感知噪声

标准扩散模型使用各向同性的纯高斯噪声 $N \sim \mathcal{N}(0, I)$，对所有空间位置施加同等强度的扰动。EMR-Diff 观察到 HR-HSI 与 HR-MSI 在边缘结构上具有高度相似性（Figure 3），因此提出利用 HR-MSI 的边缘信息来调制噪声分布。

具体做法是：对 HR-MSI 的每个波段应用 Sobel 算子提取水平梯度 $G_x$ 和垂直梯度 $G_y$，计算梯度幅值 $M = \sqrt{G_x^2 + G_y^2 + \varepsilon}$，然后对所有波段的梯度幅值取均值并做归一化得到权重图 $W = \mathrm{norm}(M)$。边缘感知噪声定义为：
$$N_* = N \cdot W$$
其效果是：在边缘等高频区域施加更强的噪声扰动，迫使去噪网络将注意力集中于这些细节重建困难的位置；在平坦区域则保持较低的噪声强度。消融实验显示，边缘感知噪声相比纯高斯噪声在所有指标上均有提升，PSNR 提升 0.92 dB（Table 3）。

### 去噪网络架构：从单路径 UNet 到 BAF-UNet

为适配上述扩散机制，EMR-Diff 设计了 BAF-UNet（Bilateral Attention Fusion UNet）作为去噪网络 $f_\theta$，包含三个互补的子创新：

1. **模态特定的双路径设计**：第一路径处理含噪输入 $\mathcal{X}_t'$ 并嵌入时间步信息，第二路径处理拼接后的 LR-HSI 与 HR-MSI（即 $\mathcal{A}_0$），两路径在多个尺度上通过特征融合进行交互。
2. **MSGAB 模块**（Multi-scale Group Attention Block）：替代标准残差块，通过分组注意力机制实现多尺度特征聚合。消融实验表明，MSGAB 相比普通残差块 PSNR 提升 1.06 dB（Table 4）。
3. **多尺度监督**：在 BAF-UNet 的四个上采样阶段分别计算输出与下采样真值之间的 L1 损失，相比单尺度监督 PSNR 提升 0.4 dB（Table 4）。

### 创新总结

三项 changed slots 之间存在因果耦合关系：多模态残差机制降低了扩散链对大量步骤的依赖，使 5 步扩散成为可能；边缘感知噪声将去噪网络的优化目标聚焦于高频细节区域；BAF-UNet 的双路径设计与 MSGAB 模块则为残差回传和边缘重建提供了足够强的网络容量。三者协同使得 EMR-Diff 在 ICVL、Harvard、Chikusei 三个数据集上均取得最优的 PSNR/SSIM/SAM/ERGAS 指标（Table 1）。



EMR-Diff 的整体 pipeline 围绕一个核心洞察展开：**将多模态残差嵌入马尔可夫链可以显著压缩扩散步数，同时利用 HR-MSI 的边缘信息引导噪声，使模型专注于高频细节重建**。如图 2 所示，系统由三个紧密耦合的模块构成：

1. **多模态残差注入 (Multimodal Residual Injection)**：将上采样后的 LR-HSI 与 HR-MSI 沿通道拼接得到 $\mathcal{A}_0$，计算其与目标 HR-HSI 之间的联合差异 $\mathcal{E}_0 = \mathcal{A}_0 - \mathcal{X}_0'$，并将该残差逐步注入前向扩散链。
2. **边缘感知噪声生成 (Edge-aware Noise Generation)**：从 HR-MSI 中提取 Sobel 梯度强度 $M$，经归一化后调制纯高斯噪声 $N$，得到边缘感知噪声 $N_* = N \cdot \mathrm{norm}(M)$，使噪声在边缘区域具有更强的扰动幅度。
3. **BAF-UNet 去噪网络 (BAF-UNet Denoising Network)**：接收带噪输入 $\mathcal{X}_t'$ 与多模态引导 $\mathcal{A}_0$，通过双路径设计与 MSGAB 模块逐步重建 HR-HSI，并在多个尺度上进行监督。

**输入输出流**：系统以 LR-HSI ($\mathcal{V}$) 和 HR-MSI ($\mathcal{Z}$) 为输入，经过前向扩散（逐步注入多模态残差与边缘感知噪声）后，由 BAF-UNet 执行反向去噪，最终输出超分辨率 HR-HSI。整个过程仅需 **5 个扩散步骤**即可收敛至最优性能（Table 5），相比标准 DDPM 大幅提升了采样效率。

**模块间的因果链路**：多模态残差 $\mathcal{E}_0$ 为扩散链提供了从低分辨率到高分辨率的显式信息桥接，使反向过程不再依赖纯噪声空间的盲目探索；边缘感知噪声 $N_*$ 则在边缘区域施加更强的扰动，迫使 BAF-UNet 在去噪时优先恢复高频结构；BAF-UNet 的双路径设计分别处理时序噪声信息和多模态引导信息，通过 MSGAB 中的自适应融合机制实现两者的高效交互。消融实验证实，多模态残差相比无残差方案 PSNR 提升 **1.35 dB**，边缘感知噪声相比纯高斯噪声提升 **0.92 dB**，MSGAB 相比普通残差块提升 **1.06 dB**（Table 2–4），三者协同构成了 EMR-Diff 的性能瓶颈突破路径。

### 补充图表

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of the proposed EMR-Diff for HSI super-resolution. The multimodal residual E0 is obtained by subtracting A0 from X ′0, and edge-aware noise N ∗ is generated by modulating Gaussian noise with the edge information of HR-MSI. During the forward diffusion process, the starting point X ′0 is gradually injected with E0 and N ∗, both controlled by a monotonically increasing sequence ηt*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of different diffusion models. With edgeaware noise and multimodal residual, EMR-Diff significantly improves the performance and efficiency*



### 观测模型

HSI超分辨率的退化过程可形式化为：

$$\mathcal{V} = \mathcal{D}(B(\mathcal{X})), \quad \mathcal{Z} = \mathbf{R}\mathcal{X}$$

其中 $\mathcal{X}$ 为HR-HSI，$\mathcal{V}$ 为LR-HSI，$\mathcal{Z}$ 为HR-MSI。$B$ 为模糊核，$\mathcal{D}$ 为空间下采样，$\mathbf{R}$ 为光谱响应矩阵。该模型建立了三种模态间的物理约束关系。

### 多模态残差注入机制

EMR-Diff的核心创新在于将多模态残差显式嵌入扩散马尔可夫链。定义扩散起点为LR-HSI上采样与HR-MSI的通道拼接：

$$\mathcal{A}_0 = \mathcal{V}_{\uparrow} \oplus \mathcal{Z}$$

多模态残差 $\mathcal{E}_0$ 刻画了HR-HSI与两种低质模态联合表示之间的差异：

$$\mathcal{E}_0 = \mathcal{A}_0 - \mathcal{X}_0'$$

其中 $\mathcal{X}_0'$ 为HR-HSI的初始估计。与标准DDPM仅注入纯高斯噪声不同，EMR-Diff的前向过程同时注入残差与噪声：

$$\mathcal{X}_t' = \mathcal{X}_0' + \eta_t \mathcal{E}_0 + \kappa \sqrt{\eta_t} N_*$$

$\eta_t$ 为单调递增序列，控制残差与噪声的注入比例；$\kappa$ 为噪声强度系数。反向过程则逐步回传残差并去噪：

$$\mathcal{X}_{t-1}' = \frac{\eta_{t-1}}{\eta_t} \mathcal{X}_t' + \frac{\alpha_t}{\eta_t} f_\theta(\mathcal{X}_t', \mathcal{A}_0, t) + \kappa \sqrt{\frac{\eta_{t-1}}{\eta_t} \alpha_t} N_*$$

$f_\theta$ 为去噪网络，$\alpha_t = \eta_t - \eta_{t-1}$。该设计将多模态信息传递嵌入扩散链，使模型仅需5个扩散步骤即可达到最佳性能。

### 边缘感知噪声调制

利用HR-MSI与HR-HSI在边缘结构上的高度相似性，EMR-Diff从HR-MSI提取边缘信息调制噪声分布。首先对HR-MSI各波段求和后使用Sobel算子提取梯度：

$$C_x = \begin{bmatrix} -1 & 0 & +1 \\ -2 & 0 & +2 \\ -1 & 0 & +1 \end{bmatrix}, \quad C_y = \begin{bmatrix} +1 & +2 & +1 \\ 0 & 0 & 0 \\ -1 & -2 & -1 \end{bmatrix}$$

梯度幅值 $M = \sqrt{G_x^2 + G_y^2 + \varepsilon}$（$\varepsilon = 10^{-8}$），经归一化后得到边缘权重 $W = \text{norm}(M)$。边缘感知噪声通过权重调制纯高斯噪声生成：

$$N_* = N \cdot W = N \cdot \text{norm}(M)$$

该机制对边缘区域施加更强的噪声扰动，迫使去噪网络优先关注高频细节重建。消融实验表明，边缘感知噪声相比纯高斯噪声PSNR提升0.92 dB。

### BAF-UNet去噪网络

BAF-UNet采用双路径设计：第一条路径处理含噪输入 $\mathcal{X}_t'$ 并融入时间步嵌入（正弦-余弦位置编码），第二条路径接收LR-HSI与HR-MSI的拼接输入。核心模块MSGAB通过多尺度分组注意力实现跨模态特征自适应融合。训练采用多尺度监督策略，在四个上采样阶段计算L1损失：

$$L_{\text{multi}} = \sum_{k=0}^{3} \| O_k + \mathcal{V}_{\uparrow n} \oplus \mathcal{Z}_{\downarrow n'} - \mathcal{X}_{\downarrow n'}' \|_1$$

其中 $O_k$ 为第 $k$ 阶段输出，$\mathcal{X}_{\downarrow n'}'$ 为对应分辨率的下采样真值。MSGAB相比普通残差块PSNR提升1.06 dB，多尺度监督相比单尺度监督提升0.4 dB。

### 补充图表

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of the proposed BAF-UNet. Multi-scale supervision calculates the L1 loss between the result of fusing*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/003_Figure_3.jpg]]
*Figure 3: Edge similarity of HR-HSI and MR-HSI*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/011_Figure_7.jpg]]
*Figure 7: Visualization of pure noise and edge-aware noise*



## 实验与关键发现

### 主要定量结果

EMR-Diff在三个公开高光谱基准数据集上进行了系统评估：ICVL、Harvard和Chikusei。评估指标覆盖空间重建质量（PSNR、SSIM）和光谱保真度（SAM、ERGAS），其中↑表示越高越好，↓表示越低越好。Table 1汇总了所有对比方法的定量结果。

在ICVL数据集上，EMR-Diff取得PSNR 55.40 dB、SSIM 0.9997、SAM 0.0040、ERGAS 0.1588，四项指标均为最优。Harvard数据集上达到PSNR 49.28 dB、SSIM 0.9990、SAM 0.0233、ERGAS 0.7800，同样全面领先。Chikusei数据集上获得PSNR 47.55 dB、SSIM 0.9980、SAM 0.0950、ERGAS 1.4943，在所有对比方法中表现最佳。三个数据集的难度梯度（ICVL > Harvard > Chikusei）与各方法的性能衰减趋势一致，EMR-Diff在最具挑战性的Chikusei场景下仍保持明显优势。

### 定性可视化分析

Figure 5展示了各方法在三个数据集上的伪彩色重建结果及误差图。在ICVL和Harvard数据集上，选取第10、20、30波段合成伪彩色图像，以第30波段作为误差图；Chikusei数据集则选取第10、60、80波段合成伪彩色图像，以第60波段作为误差图。EMR-Diff生成的伪彩色图像在空间细节和色彩还原上最接近Ground Truth，其误差图明显更蓝（表示误差更小），尤其在边缘和纹理区域优势突出。

Figure 6进一步给出了光谱误差曲线，对比像素位置为Figure 5中黄色星标处。EMR-Diff在所有波段上的光谱误差均低于其他方法，表明边缘感知噪声和多模态残差机制有效兼顾了空间细节重建与光谱信息保真。

### 消融实验

#### 多模态残差机制

Table 2比较了三种残差策略：无残差（纯扩散）、单模态残差（仅使用LR-HSI或HR-MSI的残差）和多模态残差（同时利用LR-HSI和HR-MSI）。多模态残差相比无残差方案PSNR提升1.35 dB，相比单模态残差提升0.82 dB。这一结果表明，LR-HSI与HR-MSI的联合差异信息是扩散过程中高效传递融合知识的关键瓶颈——单一模态的残差无法充分表达HR-HSI与观测数据之间的复杂映射关系。

#### 边缘感知噪声

Table 3验证了边缘感知噪声策略的有效性。将纯高斯噪声替换为边缘调制噪声后，PSNR提升0.92 dB，SSIM、SAM和ERGAS也均有改善。Figure 7可视化了纯噪声与边缘感知噪声的差异：边缘感知噪声在HR-MSI的边缘区域施加更强的扰动，迫使去噪网络优先关注高频细节重建。这一设计的因果逻辑在于：扩散模型的标准高斯噪声对图像各区域的扰动强度均匀，而HSI超分辨率任务中边缘区域的信息损失更为严重，需要差异化的噪声引导。

#### BAF-UNet架构

Table 4对去噪网络BAF-UNet进行了组件级消融。MSGAB模块（Multi-scale Group Attention Block）相比普通残差块PSNR提升1.06 dB，验证了多尺度分组注意力对跨模态特征融合的增益。多尺度监督（MSS）相比单尺度监督（BAF-UNet(S)）PSNR提升0.4 dB，说明在多个分辨率层级施加重建约束有助于稳定扩散反向过程的梯度传播。

#### 扩散步数

Table 5探究了扩散步数对性能的影响。步数从3增加到5时，图像质量持续提升；步数设为5时达到最佳PSNR；继续增加步数并未带来进一步增益。这表明多模态残差机制将有效信息传递压缩到了极少的扩散步骤中，仅需5步即可收敛，相比标准DDPM通常所需的数百至上千步大幅提升了推理效率。

#### 伪多光谱合成策略

Table 6分析了不同伪MSI合成方式的影响。实验对比了三种策略：使用HR-HSI全部波段、前三个波段、以及不使用伪MSI。提取HR-HSI前三个波段合成Pseudo-MSI取得最佳性能，说明在训练阶段引入与HR-MSI光谱维度一致的辅助信息有助于模型学习跨模态映射，但过多的波段反而引入冗余。

### 失败模式与局限性

尽管EMR-Diff在三个基准数据集上表现优异，仍存在以下局限：首先，所有实验均在受控数据集上进行，模型跨传感器和场景的泛化能力尚待验证——不同传感器的光谱响应函数和空间退化模型差异可能导致性能下降。其次，扩散采样步数虽已压缩至5步，但对于实时或近实时应用场景，推理时间仍有进一步优化的空间。这些方向留待后续工作探索。

### 补充图表

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/005_Table_1.jpg]]
*Table 1: All methods are compared quantitatively on the ICVL, Harvard, and Chikusei datasets. ↑ and ↓ indicate that higher or lower values correspond to better results. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparison results for all methods across the ICVL, Harvard, and Chikusei datasets. Under the ICVL and Harvard datasets, the 10th, 20th, and 30th bands are selected to fuse into pseudo-color images, and the 30th band is used as the error map. In the Chikusei dataset, the 10th, 60th, and 80th bands are selected to fuse into pseudo-color images, and the 60th band is used as the error map*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/008_Table_2.jpg]]
*Table 2: Ablation study of multimodal residual*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/009_Table_3.jpg]]
*Table 3: Ablation study of edge-aware noise*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/010_Table_4.jpg]]
*Table 4: Ablation study on BAF-UNet. MSS denotes multi-scale supervision. BAF-UNet(S) is with single supervision*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/012_Table_5.jpg]]
*Table 5: Ablation study of diffusion steps*

![[assets/figures/papers/paper_list_l867_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_EMR_Diff_Edge_aw/figures/013_Table_6.jpg]]
*Table 6: Ablation study of pseudo-MSI synthesis*



## 定位与知识库关联

### 扩散模型在图像复原中的演进定位

EMR-Diff 位于扩散概率模型（DDPM）应用于图像复原的演进线上。标准 DDPM 通过马尔可夫链逐步加噪与去噪来学习数据分布，在图像生成领域取得了显著成功。当该方法被迁移至图像超分辨率等复原任务时，面临三个核心瓶颈：**采样效率低**（通常需要数百至上千步）、**细节生成受限**（纯高斯噪声缺乏对高频结构的引导）、以及**多模态融合不充分**（标准扩散过程未显式建模多源图像间的残差关系）。

EMR-Diff 针对上述瓶颈提出了三个相互耦合的改进槽位，形成了一条从“通用扩散”到“任务感知扩散”的方法演化路径：

| 设计槽位 | 基线方案（标准DDPM） | EMR-Diff方案 | 因果作用 |
|---------|-------------------|-------------|---------|
| 扩散过程 | 纯高斯噪声，大量步骤 | 多模态残差传递，5步即可 | 将融合残差嵌入马尔可夫链，大幅压缩步数 |
| 噪声类型 | 纯高斯噪声 $\mathcal{N}$ | 边缘感知噪声 $\mathcal{N}_* = \mathcal{N} \cdot \mathrm{norm}(M)$ | 引导去噪网络聚焦高频边缘区域 |
| 去噪网络 | 标准UNet或单路径UNet | BAF-UNet：双路径+MSGAB+多尺度监督 | 多模态特征自适应融合，多粒度重建监督 |

这三个槽位的改进并非独立叠加，而是形成了因果闭环：多模态残差传递使扩散过程在极低步数下仍能保持信息流动；边缘感知噪声则将去噪网络的注意力精确导向残差传递中最难恢复的高频区域；BAF-UNet 的双路径设计和多尺度监督则为这种“残差+边缘”的扩散范式提供了匹配的去噪能力。

### 与现有HSI超分辨率方法的边界

HSI超分辨率的主流范式可大致分为三类：基于优化的方法、基于CNN/GAN的深度学习方法、以及新兴的扩散模型方法。EMR-Diff 与这些范式的边界清晰：

**与传统优化的关系**：传统方法通常依赖手工设计的先验（如光谱稀疏性、空间平滑性），在观测模型 $\mathcal{V} = \mathcal{D}(B(\mathcal{X})), \mathcal{Z} = \mathbf{R}\mathcal{X}$ 下求解反问题。EMR-Diff 保留了这一观测模型的物理约束——多模态残差 $\mathcal{E}_0 = \mathcal{A}_0 - \mathcal{X}_0'$ 本质上是对 $\mathcal{V}$ 和 $\mathcal{Z}$ 联合信息与真实 $\mathcal{X}$ 之间差异的显式建模，但将求解过程从优化迭代转变为扩散去噪，从而避免了手工先验的局限性。

**与CNN/GAN方法的区别**：CNN/GAN方法通常直接学习从 $\mathcal{V}, \mathcal{Z}$ 到 $\mathcal{X}$ 的端到端映射。EMR-Diff 的差异在于：(1) 不直接预测 $\mathcal{X}$，而是通过逐步去噪重建残差；(2) 边缘感知噪声机制利用了HR-MSI与HR-HSI在边缘结构上的高度相似性（Figure 3），这一先验在端到端方法中通常未被显式利用。

**与其他扩散方法的差异**：部分工作将标准DDPM直接应用于HSI超分辨率，但未针对多模态融合特性进行适配。EMR-Diff 的关键区分点在于多模态残差的引入——它将扩散过程从“从纯噪声中生成图像”转变为“从多模态残差中恢复细节”，这一范式转换是扩散步数从数百步降至5步的根本原因（Table 5）。

### 适用边界与局限

根据论文提供的证据，EMR-Diff 的适用边界和局限可归纳如下：

**已验证的适用条件**：
- 输入模态为 LR-HSI 与 HR-MSI 的融合超分辨率场景
- 三个基准数据集（ICVL、Harvard、Chikusei）上均取得最优，覆盖了室内、室外和航空遥感场景
- 扩散步数设为5时达到最佳性能，表明该方法在极低步数下有效

**已知局限**（论文明确提及）：
1. **跨传感器泛化未验证**：模型在特定数据集上训练，对未见过的传感器光谱响应函数和空间退化模型的泛化能力尚待检验。
2. **跨场景泛化未验证**：三个数据集虽有一定多样性，但真实世界中更复杂的混合场景（如云覆盖、阴影、大气扰动）下的表现未知。
3. **采样效率仍有提升空间**：虽然5步已远少于标准DDPM的数百步，但相比单步前馈方法仍有推理延迟差距。论文指出探索更高效的扩散采样器是开放方向。

**证据强度说明**：
- 消融实验覆盖了所有三个核心组件（Table 2-4），且每个组件的增益均有独立验证，证据链条完整。
- 多模态残差 vs 无残差（+1.35 dB PSNR）和边缘感知噪声 vs 纯高斯噪声（+0.92 dB PSNR）的增益幅度较大，表明改进具有实质性。
- 但消融仅在单个数据集（Harvard）上进行，跨数据集的消融一致性需要手动验证。

### 开放问题与后续方向

基于论文的分析和局限声明，可识别的开放问题包括：

1. **泛化能力增强**：如何设计传感器无关的特征表示或域适应机制，使模型能泛化到训练时未见过的传感器配置？这可能需要引入光谱响应函数的显式编码或元学习策略。

2. **更高效的采样**：5步扩散虽已高效，但能否进一步降至1-2步？这涉及对多模态残差传递机制的更精细建模，或引入一致性模型等新的扩散范式。

3. **边缘感知噪声的泛化形式**：当前边缘感知噪声依赖HR-MSI的Sobel梯度，但在HR-MSI边缘质量较差（如压缩伪影、噪声）时，该机制的鲁棒性如何？是否需要引入边缘质量评估或自适应调制？

4. **多模态残差的物理可解释性**：$\mathcal{E}_0$ 的数学定义清晰，但其在不同扩散步中传递的信息成分（光谱残差 vs 空间残差）如何解耦？这关系到模型在极端退化条件下的行为预测。

5. **与其他融合范式的结合**：EMR-Diff 的残差传递机制是否可推广至其他多模态融合任务（如多曝光融合、多焦距融合）？这需要验证多模态残差的定义在不同任务中的适应性。



## 原文 PDF

![[paperPDFs/CVPR_2026/EMR_Diff_Edge_aware_Multimodal_Residual_Diffusion_Model_for_Hyperspectral_Image_Super_resolution.pdf]]

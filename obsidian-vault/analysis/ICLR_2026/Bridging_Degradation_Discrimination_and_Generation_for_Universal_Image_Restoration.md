---
title: "Bridging Degradation Discrimination and Generation for Universal Image Restoration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bridging_Degradation_Discrimination_and_Generation_for_Universal_Image_Restoration.pdf
project_link: null
code_link: null
aliases:
- BBDDG
- BDDGUIR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "BDG aligns MAS-GLCM degradation descriptors with diffusion intermediate features in a three-stage restoration training pipeline."
primary_logic: "It pretrains generation, bridges degradation features to diffusion features with bidirectional alignment, then fine-tunes restoration with low-quality image injection."
claims:
- "MAS-GLCM provides fine-grained degradation type and level discrimination."
- "The bridge stage injects degradation awareness while retaining the diffusion model generation prior."
- "The note reports PSNR gains over DiffUIR on all-in-one restoration tasks."
---

# Bridging Degradation Discrimination and Generation for Universal Image Restoration

> [!tip] 核心洞察
> 通过多角度多尺度灰度共生矩阵（MAS-GLCM）实现细粒度退化判别，并将其特征与扩散模型的中间特征进行双向对齐，从而在单一模型中同时保留生成先验和退化判别能力，实现保真度与感知质量的平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 桥接退化判别与生成：面向通用图像复原 |
| 英文题名 | Bridging Degradation Discrimination and Generation for Universal Image Restoration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hVFoiCDiMB) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BDG (Bridging Degradation discrimination and Generation) |
| Dataset | 5D All-in-One (Deraining), 5D All-in-One (Low-light Enhancement), 5D All-in-One (Desnowing), 5D All-in-One (Dehazing) |

> [!tip] 效果简介
> - 5D All-in-One (Deraining) 上，PSNR 为 34.75，对比 31.03 (DiffUIR)，变化 +3.72。
> - 5D All-in-One (Low-light Enhancement) 上，PSNR 为 27.42，对比 25.12 (DiffUIR)，变化 +2.30。
> - 5D All-in-One (Desnowing) 上，PSNR 为 32.86，对比 32.86 (DiffUIR)，变化 0.00。

## 概要

本文提出BDG（Bridging Degradation discrimination and Generation）框架，旨在解决通用图像复原中退化判别能力与生成先验难以兼得的根本矛盾。核心创新包括：（1）提出多角度多尺度灰度共生矩阵（MAS-GLCM）实现细粒度退化判别；（2）设计三阶段扩散训练范式（生成预训练→桥接阶段→复原微调），通过双向特征对齐将退化判别信息注入扩散模型。实验表明，BDG在5D全合一复原任务中全面超越DiffUIR，在去雨任务上PSNR提升3.72 dB；在真实世界超分辨率任务中，在DIV2K-Val上PSNR达到24.1977，比第二好的扩散方法高出2.45 dB。



现有通用图像复原方法可分为两类：

- **基于判别的方法**（如AirNet、PromptIR、DCPT）：在保真度指标上表现良好，但输出过于平滑，缺乏真实纹理。
- **基于生成先验的方法**（如StableSR、DiffBIR、DiffUIR）：能生成丰富细节，但在多任务场景下容易产生与输入不一致的伪影，保真度不足。

核心瓶颈在于：退化判别与生成先验在单一模型中难以兼顾。基于判别的方法依赖显式退化表征（梯度、频率、可学习参数、文本指令），但这些表征的细粒度判别能力有限；基于生成先验的方法虽能利用扩散模型的强大生成能力，但缺乏对退化类型和级别的精确感知。



## 核心方法与创新机理

1. **MAS-GLCM退化表征**：提出多角度多尺度灰度共生矩阵（Multi-Angle and multi-Scale Gray Level Co-occurrence Matrix），通过计算多个角度和尺度下GLCM的平均值，实现对退化类型和级别的细粒度判别。在退化类型分类上达到97.13%准确率，在退化级别分类上达到74.17%准确率，远超梯度、频率等传统表征方法（Table 1）。

2. **三阶段扩散训练范式**：将扩散模型训练分为生成预训练、桥接阶段和复原微调三个阶段，通过系数调度（Eq.4中的α_t、β_t、δ_t）控制模型行为模式，在单一模型中同时保留生成先验和退化判别能力。

3. **双向特征对齐**：在桥接阶段通过双向交叉熵损失（Eq.6）将MAS-GLCM特征与扩散模型中间特征对齐，使模型获得退化感知能力。




![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_hVFoiCDiMB_Bridging_Degr/figures/001_Figure_1.jpg]]

BDG的整体框架如Figure 2所示，包含三个训练阶段：

- **生成预训练阶段**：设置α_t≡0且δ_t≡0，模型仅学习高质量图像分布，获得生成先验。
- **桥接阶段**：设置δ_t≡0，通过MAS-GLCM特征与扩散模型中间特征的双向对齐，使模型获得退化判别能力。
- **复原微调阶段**：所有系数正常调度，模型直接注入低质量图像以增强保真度。

在全合一和混合退化任务中，使用36M参数的UNet（预训练于ImageNet）；在真实世界超分辨率任务中，使用Stable Diffusion 2作为基础模型，不引入交叉注意力或ControlNet等额外架构。



### 5.1 MAS-GLCM退化表征

GLCM定义（Eq.1）：
$$M_{\Delta x, \Delta y}(i,j) = \sum_{x=1}^{W} \sum_{y=1}^{H} \left\{ 1, \quad \mathrm{if} I(x,y)=i \atop \mathrm{and} I(x+\Delta x, y+\Delta y)=j \right.$$

MAS-GLCM公式（Eq.2）：
$$M_{mas} = \frac{1}{n \times m} \sum_{i=1,j=1}^{L,\Theta} M_{L_i \cdot \sin(\Theta_j), L_i \cdot \cos(\Theta_j)}$$

对多个尺度L和角度Θ下的GLCM取平均，得到多角度多尺度的退化表征。

### 5.2 扩散模型采样公式

前向过程（Eq.3）：
$$x_t = x_{t-1} + \alpha_t x_{res} + \beta_t \epsilon_{t-1} - \delta_t x_{lq}$$

其中x_res = x_lq - x_hq为残差，α_t、β_t、δ_t分别为残差、噪声和低质量图像的系数。

采样公式（Eq.4，隐式概率模型）：
$$x_{t-1} = x_t - \alpha_t x_{res}^\theta - \frac{\beta_t^2}{\overline{\beta}_t} \epsilon^\theta + \delta_t x_{lq}$$

三个系数共同控制模型行为模式：
- 当α_t≡0且δ_t≡0时，模型仅具备生成能力（退化为VE SDE去噪公式）
- 当仅δ_t≡0时，模型进入桥接阶段，可同时保留生成先验并感知退化
- 当所有系数正常调度时，模型进入复原阶段，直接注入低质量图像以增强保真度

### 5.3 损失函数

生成损失（Eq.5）：
$$\mathcal{L}_{gen} = \mathbb{E}_{t,\epsilon,x_{res}} [||\alpha_t (x_{res}^\theta - x_{res}) + \frac{\beta_t^2}{\overline{\beta}_t} (\epsilon^\theta - \epsilon)||^2]$$

桥接损失（Eq.6，双向交叉熵）：
$$\mathcal{L}_{bridge} = \frac{1}{2} \mathbb{E}[H(y^{m2d}(F_{mas}), p^{m2d}(F_{mas})) + H(y^{d2m}(F_{diff}), p^{d2m}(F_{diff}))]$$

退化分类损失（Eq.7）：
$$\mathcal{L}_{deg-cls} = H(MLP(F_{mas}), C)$$

桥接阶段总损失（Eq.8）：
$$\mathcal{L}_{bdg} = L_{gen} + \lambda (\mathcal{L}_{bridge} + \mathcal{L}_{deg-cls})$$

复原微调损失（Eq.9）：
$$\mathcal{L}_{rft} = ||x_{gt}^\theta - x_{gt}||_1 + \lambda \mathcal{L}_{bridge}$$

全负对比损失（Eq.10，仅在RFT阶段使用）：
$$\mathcal{L}_{fcnl} = \sum_{i \in \mathcal{B}_1} \sum_{j \in \mathcal{B}_2} (1 - \cos(F_{mas}^i, F_{mas}^j))$$



## 实验与关键发现


### 6.1 全合一图像复原

在5D全合一复原任务中，BDG全面超越DiffUIR（Table 2）：


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_hVFoiCDiMB_Bridging_Degr/figures/008_Table_2.jpg]]
*Table 2: We train a 5D all-in-one image restoration model with simulated dataset following DiffUIR (Zheng et al., 2024). This model is validated on simulated and real-world scenarios. Table 2: All-in-one Image Restoration results. † means the methods are retrained within datasets we used for fair comparison. The best and second results are shown in red and blue respectively.*

| 任务 | BDG (PSNR) | DiffUIR (PSNR) | 提升 |
|------|------------|----------------|------|
| 去雨 | 34.75 | 31.03 | +3.72 |
| 低光增强 | 27.42 | 25.12 | +2.30 |
| 去雪 | 32.86 | 32.86 | 0.00 |
| 去雾 | 34.33 | 32.94 | +1.39 |
| 去模糊 | 31.11 | 29.17 | +1.94 |

### 6.2 混合退化复原

在CDD数据集上，BDG在雾+雨场景中PSNR达到34.21，比之前最优方法（Zamfir et al., 2025）提升4.28 dB（Table 4）。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_hVFoiCDiMB_Bridging_Degr/figures/017_Table_4.jpg]]
*Table 4: Table 4: Comparison to state-of-the-art on composited degradations. The best and second results are shown in red and blue respectively.*

### 6.3 真实世界超分辨率

在DIV2K-Val上，BDG的PSNR达到24.1977，比第二好的扩散方法ResShift（21.75）高出2.45 dB；在DrealSR上PSNR达到28.7961，与StableSR持平（Table 5）。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_hVFoiCDiMB_Bridging_Degr/figures/018_Table_5.jpg]]
*Table 5: Table 5: Real-world super resolution results on synthetic and real-world benchmarks. The best and second best results of each metric in diffusion-based methods are highlighted in red and blue, respectively.*

### 6.4 消融实验

- **训练阶段消融**（Table 6）：同时使用桥接阶段和RFT阶段时性能最优（PSNR 32.09 / SSIM 0.950），缺少任一阶段都会导致性能下降。
- **损失函数消融**（Table 7）：在桥接阶段，同时使用L_gen、L_bridge和L_deg-cls三种损失时性能最优；缺少L_deg-cls会导致MAS-GLCM编码器崩溃。
- **MAS-GLCM配置消融**（Table 8）：完整角度（9个）和尺度（6个）配置达到最佳性能（PSNR 32.09 / SSIM 0.950），减少角度或尺度会导致性能下降。

### 6.5 公平性说明

- 所有全合一复原实验均使用与DiffUIR相同的模拟数据集和训练协议。
- 真实世界超分辨率实验遵循StableSR和SeeSR的训练协议。
- 消融实验中，桥接阶段和RFT阶段各训练150k迭代，总迭代数300k，与基线方法保持一致。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_hVFoiCDiMB_Bridging_Degr/figures/006_Table_1.jpg]]
*Table 1: Table 1: MAS-GLCM has substantial capability in the classification of both types and levels of degradation.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_hVFoiCDiMB_Bridging_Degr/figures/015_Table_3.jpg]]
*Table 3: Table 3: Real-world restoration results in four real-world degradation types under the zero-shot setting. The best and second results are shown in red and blue respectively.*




## 定位与知识库关联

BDG属于**通用图像复原**领域，具体位于**基于扩散模型的通用复原方法**子方向。与现有方法的关系如下：

- **与判别式方法（AirNet、PromptIR、DCPT）的关系**：BDG通过MAS-GLCM实现了更细粒度的退化判别，并通过桥接阶段将判别信息注入扩散模型，而非仅用于条件控制。
- **与生成式方法（StableSR、DiffBIR、DiffUIR）的关系**：BDG在扩散采样中同时预测残差和噪声（Eq.4），而DiffUIR仅预测残差，因此BDG能保留生成先验。
- **与ResShift的关系**：BDG的扩散前向过程（Eq.3）与ResShift类似，但通过三阶段训练和MAS-GLCM特征对齐实现了更优的退化感知。

**局限性**：
- MAS-GLCM当前无法检测颜色偏差或全局几何变换，且可能对图像分辨率敏感。
- BDG依赖于相对复杂的三阶段训练范式。
- 在混合退化场景中，MAS-GLCM对相似复合退化（如low+haze+rain与low+haze）的区分能力有限。
- 在RealSR数据集上，BDG的PSNR略低于StableSR（25.5105 vs 25.52）。
- 在处理复杂噪声和文本细节时仍存在一定的过平滑问题（Figure 9）。

**开放问题**：
- 如何将MAS-GLCM的泛化能力扩展到更广泛的低级视觉任务？
- 能否进一步简化BDG的三阶段训练策略？
- MAS-GLCM能否与更强大的基础模型（如更大的扩散模型或视觉语言模型）结合？
- 如何解决MAS-GLCM对颜色偏差和全局几何变换不敏感的问题？
- 能否将BDG的桥接思想应用于其他条件生成任务？



## 原文 PDF

![[paperPDFs/ICLR_2026/Bridging_Degradation_Discrimination_and_Generation_for_Universal_Image_Restoration.pdf]]

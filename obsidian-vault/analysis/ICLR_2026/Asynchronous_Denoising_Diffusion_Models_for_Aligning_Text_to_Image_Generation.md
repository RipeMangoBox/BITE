---
title: "Asynchronous Denoising Diffusion Models for Aligning Text-to-Image Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Asynchronous_Denoising_Diffusion_Models_for_Aligning_Text_to_Image_Generation.pdf
project_link: null
code_link: https://github.com/hu-zijing/AsynDM
aliases:
- ADMA
- ADDMATIG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "AsynDM为不同像素分配异步去噪时间步，并用交叉注意力掩码调度提示相关区域。"
primary_logic: "模型从注意力图识别提示相关像素，让这些区域慢速去噪并从更清晰背景中获取上下文。"
claims:
- "同步去噪把所有像素置于同一噪声水平，限制文本相关区域利用清晰上下文。"
- "像素级时间步张量和凹函数调度在不微调模型的情况下改善图文对齐。"
- "AsynDM在Animal Activity、Drawbench、GenEval和MSCOCO提示集上提升多项对齐指标。"
---

# Asynchronous Denoising Diffusion Models for Aligning Text-to-Image Generation

> [!tip] 核心洞察
> 在扩散模型的去噪过程中，不同区域（提示相关 vs. 无关）对上下文清晰度的需求不同。通过异步去噪，让提示相关区域更慢地降噪，使其能够从已经更清晰的无关区域获取更好的上下文参考，从而提升对齐效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 异步去噪扩散模型用于文本到图像生成的对齐 |
| 英文题名 | Asynchronous Denoising Diffusion Models for Aligning Text-to-Image Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZHb4bduWkM) · [GitHub](https://github.com/hu-zijing/AsynDM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Asynchronous Diffusion Models (AsynDM) |
| Dataset | Animal Activity |

> [!tip] 效果简介
> - Animal Activity 上，BERTScore 为 0.6414，对比 0.6353 (DM)，变化 +0.0061。
> - Animal Activity 上，CLIPScore 为 0.3750，对比 0.3685 (DM)，变化 +0.0065。
> - Animal Activity 上，ImageReward 为 0.9219，对比 0.7543 (DM)，变化 +0.1676。

## 概要

本文提出**异步扩散模型（Asynchronous Diffusion Models, AsynDM）**，一种无需微调、即插即用的方法，用于提升文本到图像生成中的文本-图像对齐效果。核心思想是：在扩散模型的去噪过程中，为不同像素分配不同的时间步（pixel-level timesteps），使提示相关区域去噪更慢、无关区域去噪更快，从而让提示相关区域能够从已经更清晰的无关区域获取更好的上下文参考。在Animal Activity、Drawbench、GenEval和MSCOCO四个提示集上，AsynDM在BERTScore、CLIPScore、ImageReward和QwenScore四个指标上均一致优于所有基线方法。

### 2.1 同步去噪的根本瓶颈

现有扩散模型（如Stable Diffusion）采用**同步去噪（synchronous denoising）**机制：所有像素同时从噪声逐步演变为清晰图像。论文指出，这种机制是导致文本-图像不对齐的根本原因——"synchronous denoising treats all pixels equally, overlooking the heterogeneous nature of different regions"。在同步去噪中，与提示相关的区域只能参考处于相同噪声水平的无关区域，无法获得清晰的上下文信息，从而损害了对齐效果。

### 2.2 现有方法的局限性

现有提升文本-图像对齐的方法主要分为两类：
- **微调方法**：需要额外训练，计算成本高。
- **无微调方法**：如Z-Sampling（锯齿形扩散步骤）、SEG（自注意力能量视角）、S-CFG和CFG++（改进无分类器引导）。这些方法虽然无需训练，但未从根本上解决同步去噪导致的上下文不清晰问题。

## 核心方法与创新机理

### 3.1 核心洞察

论文的核心洞察是：在扩散模型的去噪过程中，不同区域（提示相关 vs. 无关）对上下文清晰度的需求不同。通过异步去噪，让提示相关区域更慢地降噪，使其能够从已经更清晰的无关区域获取更好的上下文参考，从而提升对齐效果。

### 3.2 因果旋钮

**像素级时间步（pixel-level timesteps）的分配与调度**。通过为不同像素分配不同的时间步，并利用从交叉注意力图提取的掩码动态调节时间步调度，使提示相关区域去噪更慢、无关区域去噪更快，从而提供更清晰的像素间上下文。

### 3.3 关键变更

| 变更模块 | 基线值 | 提出值 |
|---------|--------|--------|
| 时间步调度 | 所有像素使用相同的线性调度器，从T到0同步降噪 | 提示相关区域使用凹函数调度器（如二次函数），无关区域使用线性调度器，实现异步降噪 |
| 时间步表示 | 标量时间步t，所有像素共享 | 像素级时间步张量t_i ∈ R^{h×w}，每个像素独立编码时间步 |
| 去噪过程索引 | 从T到0的逆序索引 | 从0到T的正序索引i，因为不同像素有不同的时间步t |
| 掩码生成 | 无掩码 | 从交叉注意力图动态提取二进制掩码M，标识提示相关区域 |

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_ZHb4bduWkM_Asynchronous_/figures/001_Figure_1.jpg]]
*Figure 1: Existing diffusion models generate images through synchronous denoising, where all pixels are simultaneously denoised step-by-step from noises to images, hindering text-to-image alignment. Asynchronous diffusion models denoise the prompt-related regions more gradually than other regions, thereby receiving clearer inter-pixel context and ultimately achieving improved alignment.*

AsynDM的整体框架如Figure 2所示，包含四个核心模块：

1. **像素级时间步编码器**：将像素级时间步张量t_i独立编码并逐像素注入去噪模型。
2. **交叉注意力掩码提取器**：从交叉注意力图提取提示相关区域的二进制掩码M。
3. **异步调度器**：根据掩码M为不同区域分配不同的时间步调度（凹函数 vs 线性）。
4. **异步DDPM/DDIM采样器**：执行像素级时间步的去噪步骤，保持马尔可夫性质。

### 5.1 像素级时间步分配

标准DDPM的同步去噪步骤为：

$$p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c}) = \mathcal{N}(\mathbf{x}_{t-1} \mid \mu_\theta(\mathbf{x}_t, t, \mathbf{c}), \sigma_t^2 \mathbf{I})$$

其中均值函数为：

$$\mu_\theta(\mathbf{x}_t, t, \mathbf{c}) = \frac{1}{\sqrt{\alpha_t}} (\mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}}) \epsilon_\theta(\mathbf{x}_t, t, \mathbf{c})$$

在异步扩散模型中，时间步t被替换为像素级时间步张量t_i ∈ R^{h×w}。去噪步骤变为：

$$p_\theta(\mathbf{x}_{i+1} \mid \mathbf{x}_i, \mathbf{c}) = \mathcal{N}(\mathbf{x}_{i+1} \mid \mu_\theta(\mathbf{x}_i, \mathbf{t}_i, \mathbf{c}), \sigma_i^2 \mathbf{I})$$

均值函数变为：

$$\mu_\theta(\mathbf{x}_i, \mathbf{t}_i, \mathbf{c}) = \frac{1}{\sqrt{\alpha_{\mathbf{t}_i}}} (\mathbf{x}_i - \frac{\beta_{\mathbf{t}_i}}{\sqrt{1 - \bar{\alpha}_{\mathbf{t}_i}}}) \epsilon_\theta(\mathbf{x}_i, \mathbf{t}_i, \mathbf{c})$$

其中对α、β、ᾱ进行逐元素索引。论文证明，异步扩散模型仍然保持马尔可夫性质，t_i作为马尔可夫链中的状态而非逆时间索引。

### 5.2 凹函数调度器

论文提出使用凹函数f(i)作为调度函数，满足f(0)=T, f(T)=0。对于阴影区域内的任意点，都可以沿平移后的凹函数到达t=0（Figure 3）。平移条件为：

$$f(i_0 - a) + b = t_0, \quad f(T - a) + b = 0$$

实验中使用的二次调度函数为：

$$\bar{f}(i) = T - \frac{1}{T} i^2$$

消融实验中还使用了分段线性调度器和指数调度器：

$$f(i) = \min(T - \frac{1}{2} i, \frac{3}{2}T - \frac{3}{2} i)$$

$$f(i) = \frac{T}{e-1} \cdot (e - e^{\frac{1}{T} i})$$

### 5.3 交叉注意力掩码提取

从交叉注意力图提取二进制掩码M，标识提示相关区域：

$$M = \bigvee_{o \in \mathcal{O}_\mathbf{c}} \{ \mathbf{1}[A^o > A_\mathrm{mean}^o] \}$$

其中A^o是第o个提示词对应的交叉注意力图，A_mean^o是其均值，通过阈值化并逐元素OR得到最终掩码。对于DiT-based模型（如SD3.5），交叉注意力图从联合注意力矩阵中提取子矩阵A = A_joint[:(h×w), (h×w):]。

### 5.4 掩码引导的异步去噪

在每个去噪步骤i，根据掩码M_i为不同区域分配不同的调度：提示相关区域（M_i=1）使用凹函数调度器，无关区域（M_i=0）使用线性调度器。通过调度器重加权控制最大时间步差异：

$$f' = \omega \cdot f + (1 - \omega) \cdot g$$

其中ω控制凹函数f与线性函数g的加权比例。

### 5.5 异步DDIM采样器

像素级时间步的DDIM更新方程为：

$$\mathbf{x}_{i+1} = \sqrt{\alpha_{\mathbf{t}_{i+1}}} \cdot \hat{\mathbf{x}}_0 + \sqrt{1 - \alpha_{\mathbf{t}_{i+1}} - \sigma_i^2} \cdot \epsilon_\theta(\mathbf{x}_i, \mathbf{t}_i, \mathbf{c}) + \sigma_i \epsilon_i$$

其中x̂_0预测为：

$$\hat{\mathbf{x}}_0 = \frac{1}{\sqrt{\alpha_{\mathbf{t}_i}}}(\mathbf{x}_i - \sqrt{1 - \alpha_{\mathbf{t}_i}} \cdot \epsilon_\theta(\mathbf{x}_i, \mathbf{t}_i, \mathbf{c}))$$

## 实验与关键发现

### 6.1 主要定量结果

Table 1展示了AsynDM在四个提示集上的主要定量结果。以Animal Activity提示集为例：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_ZHb4bduWkM_Asynchronous_/figures/005_Table_1.jpg]]
*Table 1: Text-to-image alignment performance of AsynDM compared with baseline methods across diverse prompts.*

| 指标 | DM (基线) | AsynDM (提出) | 提升 |
|------|-----------|---------------|------|
| BERTScore | 0.6353 | 0.6414 | +0.0061 |
| CLIPScore | 0.3685 | 0.3750 | +0.0065 |
| ImageReward | 0.7543 | 0.9219 | +0.1676 |
| QwenScore | 4.9445 | 5.5218 | +0.5773 |

在Drawbench、GenEval和MSCOCO上，AsynDM同样在所有指标上优于所有基线方法（包括DM、DM_concave、Z-Sampling、SEG、S-CFG、CFG++）。

### 6.2 消融实验

**掩码消融**（Table 2）：使用固定掩码时，AsynDM仍能提升对齐效果（如BERTScore 0.6405），但动态掩码的提升更大（0.6414），表明动态更新掩码的有效性。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_ZHb4bduWkM_Asynchronous_/figures/007_Table_2.jpg]]
*Table 2: Text-to-image alignment performance of AsynDM when employing different concave schedulers and using fixed masks, across prompts from animal activity set.*

**调度器消融**（Table 2）：二次、分段线性、指数三种凹调度器均能提升对齐效果，表明方法对调度器形式具有鲁棒性。

**最大时间步差异消融**（Figure 8）：通过ω控制最大时间步差异，存在最优值。ω过小提升不足，ω过大（0.8, 0.9）导致快速降噪区域保留噪声，产生模糊和噪声背景。

**去噪步数消融**（Table 6）：AsynDM在不同总去噪步数T（5, 10, 20, 30, 40, 50, 60）下均能一致提升对齐效果。

**模型无关性验证**（Table 4和Table 5）：AsynDM在SDXL-base-1.0和SD3.5-medium上也能一致提升对齐效果，表明方法具有模型无关性。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_ZHb4bduWkM_Asynchronous_/figures/034_Table_4.jpg]]
*Table 4: Text-to-image alignment performance of AsynDM compared with baseline methods on animal activity prompt set. The base model is SDXL-base-1.0 (Podell et al., 2023).*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_ZHb4bduWkM_Asynchronous_/figures/035_Table_5.jpg]]
*Table 5: Text-to-image alignment performance of AsynDM compared with baseline methods on animal activity prompt set. The base model is SD3.5-medium (Esser et al., 2024).*

### 6.3 人类评估

Figure 5展示了人类评估结果：52名来自八所大学的参与者评估了DM、DM_concave和AsynDM生成的图像，AsynDM在文本-图像对齐上获得更高的偏好率。

### 6.4 应用展示

Figure 6展示了AsynDM的两个应用：
- **(a) 减少图像失真**：通过掩码覆盖失真区域并使用相同种子，AsynDM能生成改进的图像。
- **(b) 增强编辑性能**：通过手动标注待编辑区域并应用凹调度器，使编辑结果更符合用户期望。

### 6.5 公平性说明

- AsynDM是一种即插即用、无需微调的方法，不改变预训练模型的参数，因此不会引入额外的训练偏见。
- 方法依赖于交叉注意力图来识别提示相关区域，对于包含多个对象的复杂提示，掩码提取可能不完整，导致某些对象被忽略。
- 人类评估涉及52名来自八所大学的参与者，样本量有限，可能无法完全代表一般用户偏好。
- 实验主要在英文提示上进行，对非英文提示的对齐效果尚未验证。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_ZHb4bduWkM_Asynchronous_/figures/033_Table_3.jpg]]
*Table 3: Hyperparameters of our experiments.*

## 定位与知识库关联

### 7.1 方法谱系

AsynDM属于**无微调的文本-图像对齐增强方法**，与以下方法形成对比：

- **基于微调的方法**：需要额外训练，计算成本高。
- **基于引导的方法**（S-CFG, CFG++）：通过改进无分类器引导来提升对齐，但未解决同步去噪的上下文问题。
- **基于注意力控制的方法**（Z-Sampling, SEG）：通过修改注意力图或采样轨迹来增强对齐，但同样受限于同步去噪框架。

AsynDM的核心创新在于从**时间步调度**的角度切入，通过像素级异步去噪从根本上解决上下文不清晰的问题。

### 7.2 知识库定位

AsynDM建立在以下基础工作上：
- **DDPM** (Ho et al., 2020)：扩散模型的基础框架。
- **Latent Diffusion Models** (Rombach et al., 2022)：Stable Diffusion的基础架构。
- **DDIM** (Song et al., 2022)：高效采样方法。
- **Cross-Attention** (Vaswani et al., 2017)：用于文本条件注入的注意力机制。
- **Attend-and-Excite** (Chefer et al., 2023)：基于注意力引导的对齐方法。

### 7.3 局限性与开放问题

**局限性**：
- 最大时间步差异需要谨慎调节：ω过小提升不足，ω过大导致模糊和噪声背景。
- 方法依赖于交叉注意力图识别提示相关区域，对于复杂提示的掩码提取可能不完整。
- 采样时间（86分钟）略高于标准DM（78分钟），主要开销来自像素级时间步的额外编码。
- 非英文提示上的对齐效果尚未验证。
- 对于DiT-based模型，交叉注意力图需要从联合注意力矩阵中提取子矩阵，实现稍复杂。

**开放问题**：
- 如何自动学习最优的凹调度函数，而不是手动选择形式？
- 能否将像素级时间步调度与强化学习或可微分优化结合，实现端到端的调度学习？
- 对于包含多个对象且对象间存在复杂关系的提示，如何更精确地提取掩码？
- 异步去噪的思想是否可以推广到视频生成、3D生成等其他生成任务？
- 在极少数去噪步数（如T=5）下，如何进一步优化对齐效果？

## 原文 PDF

![[paperPDFs/ICLR_2026/Asynchronous_Denoising_Diffusion_Models_for_Aligning_Text_to_Image_Generation.pdf]]

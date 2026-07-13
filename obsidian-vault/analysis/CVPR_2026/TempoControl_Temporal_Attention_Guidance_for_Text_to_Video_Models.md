---
title: "TempoControl: Temporal Attention Guidance for Text-to-Video Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TempoControl_Temporal_Attention_Guidance_for_Text_to_Video_Models.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Schiber_TempoControl_Temporal_Attention_Guidance_for_Text-to-Video_Models_CVPR_2026_paper.html
project_link: https://shiraschiber.github.io/TempoControl/
code_link: null
aliases:
- TempoControl
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion/diffusion_image_video
- topic/generative_models_diffusion
core_operator: 交叉注意力图中的时间注意力信号 a_i^t —— 它编码了每个词在各帧的语义影响强度，通过控制该信号的形状与强度即可直接操控概念的时序出现。
primary_logic: 在不微调模型的前提下，通过在去噪过程中对潜变量施加梯度优化，利用 Pearson 相关对齐时序、幅度损失调控强弱、熵正则保持空间一致性，即可实现精确的时序控制，同时维持视频质量与多样性。
claims:
- Wan 2.1 即使收到明确的时间提示，也无法生成符合时间约束的视频，而 TEMPOCONTROL 可以纠正这一行为。
- TEMPOCONTROL 在三个时序控制基准（单对象、双对象、动作）上均大幅提升 Temporal Accuracy，且保持成像质量。
- 消融实验证明 Pearson 相关项是时序对齐的主要驱动力，熵正则项对保持语义保真度至关重要。
- 在 VBench 多对象基准上，TEMPOCONTROL 在保持语义的同时提升了 Multiple Object 指标。
---

# TempoControl: Temporal Attention Guidance for Text-to-Video Models

> [!tip] 核心洞察
> 在不微调模型的前提下，通过在去噪过程中对潜变量施加梯度优化，利用 Pearson 相关对齐时序、幅度损失调控强弱、熵正则保持空间一致性，即可实现精确的时序控制，同时维持视频质量与多样性。

| 字段      | 内容                                                                                                                                                                                                                                                                             |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 中文题名    | TempoControl：面向文本生成视频的时间注意力引导                                                                                                                                                                                                                                                  |
| 英文题名    | TempoControl: Temporal Attention Guidance for Text-to-Video Models                                                                                                                                                                                                             |
| 会议/期刊   | CVPR 2026                                                                                                                                                                                                                                                                      |
| Links   | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Schiber_TempoControl_Temporal_Attention_Guidance_for_Text-to-Video_Models_CVPR_2026_paper.html) · [Project](https://shira-schiber.github.io/TempoControl/) · [Code](https://github.com/Shira-Schiber/TempoControl) |
| Topic   | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion/diffusion_image_video #topic/generative_models_diffusion                                                                             |
| Method  | TEMPOCONTROL                                                                                                                                                                                                                                                                   |
| Dataset | One Object Temporal Control, Two Objects Temporal Control, Movement Temporal Control, VBench Multiple Object                                                                                                                                                                   |

> [!tip] 效果简介
> - One Object Temporal Control 上，Temporal Accuracy (%) 83.56 (Wan2.1-S) vs 63.94 (Wan2.1-S text-only) (+19.62)。
> - Two Objects Temporal Control 上，Temporal Accuracy (%) 53.17 (Wan2.1-S) vs 37.50 (Wan2.1-S text-only) (+15.67)。
> - Movement Temporal Control 上，Temporal Accuracy (%) 54.00 (Wan2.1-S) vs 19.00 (Wan2.1-S text-only) (+35.00)。

## 概要

**核心问题**：现有文本到视频扩散模型（如 Wan2.1、CogVideoX-5B）缺乏细粒度的时间控制能力——即便在提示词中明确描述视觉元素出现的时间节点，模型也无法可靠地将概念约束在指定的时序窗口内。例如，提示词要求“狗在后半段出现”，生成视频中狗却往往过早登场（Figure 2）。

**核心洞察**：交叉注意力图中的时间注意力信号 $a_i^t$ 编码了每个词在各帧的语义影响强度。通过控制该信号的形状与强度，可以直接操控概念的时序出现，而无需微调模型。

**方法定位**：TEMPOCONTROL 是首个面向文本到视频扩散模型的推理时（inference-time）时序控制方法。它在去噪过程中对潜变量施加梯度优化，利用三个互补的损失项引导交叉注意力图的时间模式：
- **Pearson 相关损失**（$\mathcal{L}_{\mathrm{corr}}$）：将时间注意力信号与目标掩码进行时序对齐；
- **幅度损失**（$\mathcal{L}_{\mathrm{mag}}$）：在目标帧增强注意力、在非目标帧抑制注意力；
- **熵正则**（$\mathcal{L}_{\mathrm{entropy}}$）：维持空间注意力的一致性，防止语义扭曲。

**主要结果**：在三个时序控制基准上，TEMPOCONTROL 均大幅超越纯文本时序提示基线：单对象时序准确率从 63.94% 提升至 83.56%（+19.62%），双对象从 37.50% 提升至 53.17%（+15.67%），动作控制从 19% 提升至 54%（+35%），同时保持成像质量不退化（Table 1）。该方法还可零样本拓展至音频-视频对齐任务。

### 文本到视频生成中的时间控制缺口

文本到视频扩散模型近年来取得了显著进展，代表性工作包括 **Wan2.1**（Wan et al., arXiv 2025）和 **CogVideoX-5B**（Yang et al., arXiv 2024）。这些模型能够根据自然语言描述生成连贯的视频序列，但在**细粒度时间控制**方面存在根本性缺陷：它们无法可靠地指定视觉元素在生成序列中出现的**具体时间点**。

具体而言，即使提示中明确包含时间描述——例如“视频前半段只有猫，狗在后半段才出现”——模型也往往无法遵循这一约束。**Figure 2** 清晰地展示了这一现象：在没有 TEMPOCONTROL 优化时，尽管提示明确要求狗在“后半段”出现，Wan2.1 生成的视频中狗却过早地进入了画面。这揭示了当前文本到视频模型的一个核心瓶颈：**文本中的时间描述不足以作为可靠的控制信号**。

### 瓶颈的根源：交叉注意力中的时间信号

扩散模型通过交叉注意力机制将文本语义注入视觉生成过程。对于视频生成，每个词 $i$ 在每一帧 $j$ 上都有一个空间注意力图 $\bar{A}_{j,i}^t$。将其在空间维度上聚合，可以得到一个**时间注意力向量**：

$$a_{i}^{t} = [\hat{A}_{1,i}^{t}, \hat{A}_{2,i}^{t}, ..., \hat{A}_{T',i}^{t}] \in \mathbb{R}^{T'}$$

该向量编码了词 $i$ 在视频各帧中的语义影响强度。**Figure 2** 底部对比了优化前后的时间注意力曲线与目标掩码：在无优化条件下，注意力信号与目标时间模式几乎不相关（Pearson 相关系数极低）；而通过引导注意力信号去匹配目标掩码，可以显著提升时间对齐程度。

这一观察揭示了一个关键的**因果旋钮**：交叉注意力图中的时间注意力信号 $a_i^t$ 直接决定了概念的时序出现模式。控制该信号的形状与强度，即可在不修改模型参数的前提下实现精确的时序控制。

### 现有方法的局限与本文动机

现有解决时间控制问题的思路大致分为两类：

1. **基于文本提示的方法**：在提示中加入时间副词或时间描述（如“first”、“then”、“in the second half”），但如 **Figure 2** 所示，模型对这些语言线索的遵循度很低。定量评估也证实了这一点：在单对象时间控制基准上，Wan2.1-S 仅依靠文本时间提示时，时间准确率仅为 63.94%（**Table 1**）。

2. **基于微调的方法**：通过对模型进行额外训练来增强时间控制能力，但这需要大量标注数据、计算资源，且会改变基础模型的生成分布，牺牲了通用性和灵活性。

本文的核心动机在于提出一种**推理时优化方法**——TEMPOCONTROL，它无需微调、无需额外监督信号，仅通过在去噪过程中对潜变量施加梯度优化，利用三个互补的损失项（Pearson 相关对齐时序、幅度损失调控强弱、熵正则保持空间一致性）来引导交叉注意力图的时间模式，从而实现精确的时序控制，同时维持视频质量与多样性。**Figure 1** 展示了该方法在单对象、多对象、动作控制和音频对齐等多种场景下的应用能力。

## 核心方法与创新机理

### 问题瓶颈：文本提示中时序约束的不可靠性

现有文本到视频扩散模型（如 **Wan2.1-S/L**（Wan et al., arXiv 2025）、**CogVideoX-5B**（Yang et al., arXiv 2024））缺乏细粒度的时间控制能力。即便在提示中明确加入时间描述（如“视频前半段只有猫，后半段狗才出现”），模型仍无法可靠地将视觉元素映射到指定的时间点。Figure 2 展示了典型失败案例：提示要求狗在后半段出现，但基线模型生成的视频中狗过早出现，表明模型对文本时序线索的响应几乎失效。

这一瓶颈的根源在于：标准文本到视频扩散模型仅通过交叉注意力机制将文本语义注入视频 token，但该机制并未对概念出现的**具体时间点**施加任何显式约束。模型学到的是“狗与猫共同出现”的统计关联，而非“狗在何时出现”的时序规约。

### 核心洞察：交叉注意力图作为时序控制旋钮

TEMPOCONTROL 的核心发现是：**交叉注意力图中的时间注意力信号 $a_i^t$ 编码了每个词在各帧的语义影响强度，通过控制该信号的形状与强度，即可直接操控概念的时序出现**。

具体而言，在去噪步 $t$，对于目标词 $i$，从各交叉注意力层和头聚合得到空间注意力图 $\bar{A}_{j,i}^t$，再沿空间维度求和得到标量注意力值 $\hat{A}_{j,i}^t$，最终构成时间注意力向量：

$$a_i^t = [\hat{A}_{1,i}^t, \hat{A}_{2,i}^t, \ldots, \hat{A}_{T',i}^t] \in \mathbb{R}^{T'}$$

该向量的每个元素表示词 $i$ 在对应帧 $j$ 的语义激活强度。Figure 3 展示了这一提取与聚合流程。关键洞察在于：**$a_i^t$ 的形状直接反映了概念出现的时间模式**，因此通过优化潜变量 $z_t$ 来重塑 $a_i^t$，即可在不微调模型的前提下实现精确的时序控制。

### Changed Slot 1：从无显式时序控制到推理时潜变量优化

**Baseline 值**：标准文本到视频扩散模型仅依赖文本中的时间描述，无任何显式时序控制机制，导致时序约束不可靠。

**Proposed 值**：TEMPOCONTROL 在推理过程中对潜变量 $z_t$ 施加梯度优化，通过最小化精心设计的时空损失函数来引导交叉注意力图的时间模式：

$$z_t' = z_t - \alpha \nabla_{z_t} \mathcal{L}^t$$

其中 $\alpha$ 为学习率，$\mathcal{L}^t$ 为组合损失。这一设计的关键优势在于：**无需额外训练数据、无需模型微调、无需辅助网络**，仅利用预训练模型内部已有的交叉注意力信号即可实现控制。

### Changed Slot 2：从标准扩散去噪损失到三项协同损失函数

**Baseline 值**：标准扩散模型仅使用去噪损失（如噪声预测的 MSE），对注意力分布无任何直接约束。

**Proposed 值**：引入三项互补的损失函数，分别从时序对齐、注意力强度和空间一致性三个维度引导生成过程：

1. **Pearson 相关损失 $\mathcal{L}_{\mathrm{corr}}^t$**：衡量标准化后的时间注意力向量 $\tilde{a}_i^t$ 与目标掩码 $m_i$ 的线性匹配程度，是时序对齐的**主要驱动力**。消融实验（Table 3）表明，单独使用该项即可带来显著的时序准确率提升。

2. **幅度损失 $\mathcal{L}_{\mathrm{mag}}^t$**：由正幅度项 $\mathcal{L}_{\oplus}^t$（鼓励活跃帧注意力增强）和负幅度项 $\mathcal{L}_{\ominus}^t$（惩罚非活跃帧注意力）组合而成：
   $$\mathcal{L}_{\mathrm{mag}}^t = \mathcal{L}_{\ominus}^t - \mathcal{L}_{\oplus}^t$$
   该项调控注意力在目标帧与非目标帧之间的强度对比。

3. **空间熵正则 $\mathcal{L}_{\mathrm{entropy}}^t$**：对活跃帧的空间注意力分布施加熵最小化，防止注意力过度扩散导致语义扭曲。Table 3 和 Figure 4 证实，单独使用熵正则项可获得最高的成像质量（59.52%），表明其对维持空间一致性和语义保真度至关重要。

最终组合损失为：
$$\mathcal{L}^t = \mathcal{L}_{\mathrm{corr}}^t + \lambda_1 \mathcal{L}_{\mathrm{magnitude}}^t + \lambda_2 \mathcal{L}_{\mathrm{entropy}}^t$$
其中 $\lambda_1 = 0.3$，$\lambda_2 = 10$。完整方法（C+E）在 Table 3 中达到最佳时序准确率，同时成像质量接近最高水平。

### 方法定位：推理时控制的新范式

TEMPOCONTROL 在方法谱系中占据独特位置：它不同于需要微调或额外训练数据的可控生成方法，也不同于仅修改文本提示的软约束方法。其本质是**利用预训练模型内部表征（交叉注意力）作为可微分控制接口，通过测试时优化实现零样本时序控制**。这一范式与图像生成中的推理时注意力引导方法（如 Prompt-to-Prompt 等）共享精神内核，但 TEMPOCONTROL 首次将其系统性地扩展到视频生成的**时间维度**，并提出了三项协同损失以同时解决时序对齐、强度调控和语义保真度三个子问题。

TEMPOCONTROL 是一种推理时优化方法，其核心思想是利用文本到视频扩散模型中已有的交叉注意力图作为控制手柄，在不微调模型的前提下实现对视觉概念时序出现的精确操控。整体流程围绕“提取注意力信号→计算时空损失→梯度更新潜变量”这一闭环展开，如图 3 所示。

### 输入与输出

方法的输入端包含三个要素：

- **预训练文本到视频扩散模型**（如 **Wan2.1**，Wan et al., arXiv 2025；**CogVideoX-5B**，Yang et al., arXiv 2024），在去噪过程中提供交叉注意力图；
- **文本提示**，其中包含需要时序控制的词元（token）；
- **目标时序掩码** $m_i \in \mathbb{R}^{T'}$，指定每个受控词 $i$ 在视频各帧中应出现（$m_{i,j} > \tau$）或不应出现（$m_{i,j} \leq \tau$）的时间区间。掩码可以来自人工标注、规则定义，或从音频包络等外部信号中提取。

输出为经过潜变量优化的视频序列，其中受控概念的时序出现模式与目标掩码对齐。

### 三大模块与数据流

方法在每个去噪步 $t$ 中依次执行三个模块，形成统一的优化回路：

1.  **交叉注意力聚合（Cross-Attention Aggregation）**
    从扩散模型的所有交叉注意力层和多头中提取空间注意力图，按层和头求平均得到聚合注意力矩阵 $\bar{A}^t \in \mathbb{R}^{n_v \times n_p}$。对于每个受控词 $i$，在空间维度 $(x, y)$ 上求和得到标量注意力值 $\hat{A}_{j,i}^t$，并按帧拼接为时间注意力向量：
    $$a_i^t = [\hat{A}_{1,i}^t, \hat{A}_{2,i}^t, \dots, \hat{A}_{T',i}^t] \in \mathbb{R}^{T'}$$
    该向量编码了词 $i$ 在每一帧的语义影响强度，是后续优化的直接对象。

2.  **时序损失计算（Temporal Loss Computation）**
    将时间注意力向量 $a_i^t$ 与目标掩码 $m_i$ 对齐，通过三个互补的损失项驱动优化：
    - **Pearson 相关损失** $\mathcal{L}_{\mathrm{corr}}^t$：衡量标准化后的注意力与掩码的线性匹配程度，是时序对齐的主要驱动力；
    - **幅度损失** $\mathcal{L}_{\mathrm{mag}}^t$：由正幅度项 $\mathcal{L}_{\oplus}^t$（增强活跃帧注意力）和负幅度项 $\mathcal{L}_{\ominus}^t$（抑制非活跃帧注意力）组合而成，调控注意力的绝对强度；
    - **空间熵正则** $\mathcal{L}_{\mathrm{entropy}}^t$：对活跃帧的空间注意力分布施加熵最小化，防止注意力过度扩散导致语义扭曲。
    
    总损失为三者的加权和：
    $$\mathcal{L}^t = \mathcal{L}_{\mathrm{corr}}^t + \lambda_1 \mathcal{L}_{\mathrm{mag}}^t + \lambda_2 \mathcal{L}_{\mathrm{entropy}}^t$$
    其中 $\lambda_1=0.3$，$\lambda_2=10$。

3.  **潜变量梯度更新（Latent Gradient Update）**
    计算总损失 $\mathcal{L}^t$ 对当前潜变量 $z_t$ 的梯度，使用 AdamW 优化器进行更新：
    $$z_t' = z_t - \alpha \nabla_{z_t} \mathcal{L}^t$$
    其中 $\alpha$ 为学习率。更新后的潜变量 $z_t'$ 继续参与后续去噪步。为控制推理开销，优化仅在前 5 个去噪步中执行，每步最多进行 10 次梯度更新，并引入基于 Pearson 相关的早停机制——当相关度超过阈值 $\tau_{\mathrm{corr}}$ 时提前终止当前步的优化。

### 关键设计原则

框架的有效性建立在三个互补原则之上：

- **相关（Correlation）**：对齐时序模式，确保概念在正确的帧出现或消失；
- **幅度（Magnitude）**：调控注意力强度，使概念在需要可见时获得足够的语义响应；
- **熵（Entropy）**：保持空间一致性，防止注意力在活跃帧中过度扩散而导致语义失真（如图 4 所示，消融实验证实熵正则对维持语义保真度至关重要）。

这种模块化设计使得 TEMPOCONTROL 可以即插即用地应用于不同的扩散模型骨干网络，无需任何微调或额外监督信号。

TEMPOCONTROL 的核心工作流程由三个模块串联而成：交叉注意力聚合、时序损失计算、以及潜变量梯度更新。整个流程在每个去噪步 $t$ 中执行，通过迭代优化潜变量来引导生成视频的时序行为，如图 Figure 3 所示。

### 交叉注意力聚合模块

该模块负责从扩散模型的交叉注意力层中提取并聚合词级别的时序信号。具体而言，对于每个去噪步 $t$，首先将所有注意力头与所有交叉注意力层的注意力图取平均，得到聚合注意力矩阵：

$$\bar{A}^t \in \mathbb{R}^{n_v \times n_p}$$

其中 $n_v$ 为视频 token 数量，$n_p$ 为文本 token 数量。随后，对每个词 $i$ 在每帧 $j$ 的空间注意力求和，得到标量注意力值：

$$\hat{A}_{j,i}^t = \langle \bar{A}_{j,i}^t \rangle_{x,y}$$

将所有帧的标量值拼接，构成该词的时间注意力向量：

$$a_i^t = [\hat{A}_{1,i}^t, \hat{A}_{2,i}^t, ..., \hat{A}_{T',i}^t] \in \mathbb{R}^{T'}$$

其中 $T'$ 为潜变量中的时间维度。这个向量 $a_i^t$ 编码了词 $i$ 在各帧的语义影响强度，是后续时序控制的核心操纵对象。

### 时序损失计算模块

该模块通过三个互补的损失项来塑造时间注意力信号的形状与强度，使其与用户指定的目标掩码 $m_i$ 对齐。

**Pearson 相关损失** 是时序对齐的主要驱动力。它衡量标准化后的注意力向量 $\tilde{a}_i^t$ 与目标掩码 $m_i$ 之间的线性匹配程度：

$$\mathcal{L}_{\mathrm{corr}}^{t} = -\frac{\mathrm{Cov}(m_i, \tilde{a}_i^t)}{\sigma_{m_i} \sigma_{\tilde{a}_i^t}}$$

该损失鼓励注意力信号的时间波形与目标掩码的形状一致，而不强制绝对幅值匹配，从而保留模型原有的注意力动态范围。

**幅度损失** 在相关损失的基础上进一步调控注意力的强弱。它由正、负两个子项组成。正向幅度损失鼓励在掩码活跃的帧（$m_{i,j} > \tau$）增加注意力强度：

$$\mathcal{L}_{\oplus}^{t} = \frac{1}{T'} \sum_{j=1}^{T'} \mathbb{1}_{\{m_{i,j} > \tau\}} \cdot a_{i,j}^t$$

负向幅度损失则惩罚在掩码非活跃帧的注意力强度：

$$\mathcal{L}_{\ominus}^{t} = \frac{1}{T'} \sum_{j=1}^{T'} \mathbb{1}_{\{m_{i,j} \leq \tau\}} \cdot a_{i,j}^t$$

将两者组合为净幅度损失：

$$\mathcal{L}_{\mathrm{mag}}^{t} = \mathcal{L}_{\ominus}^{t} - \mathcal{L}_{\oplus}^{t}$$

**空间熵正则损失** 用于防止注意力在空间维度上过度扩散，从而维持语义保真度。它对掩码活跃帧的空间注意力分布施加熵最小化：

$$\mathcal{L}_{\mathrm{entropy}}^{t} = \frac{1}{T'} \sum_{j=1}^{T'} \mathbb{1}_{\{m_{i,j} > \tau\}} \cdot \mathcal{H}(\bar{A}_{j,i}^t)$$

其中 $\mathcal{H}(\cdot)$ 为 Shannon 熵。消融实验（Table 3, Figure 4）表明，该正则项对保持成像质量和防止语义扭曲至关重要。

![[assets/figures/papers/paper_list_l30_https_openaccess_thecvf_com_content_CVPR2026_html_Schiber_TempoControl_T/figures/004_Figure_4.jpg]]
*Figure 4: Entropy regularization helps preserve semantic fidelity*

最终的总损失为三项的加权和：

$$\mathcal{L}^t = \mathcal{L}_{\mathrm{corr}}^{t} + \lambda_1 \mathcal{L}_{\mathrm{magnitude}}^{t} + \lambda_2 \mathcal{L}_{\mathrm{entropy}}^{t}$$

其中 $\lambda_1 = 0.3$，$\lambda_2 = 10$。

### 潜变量梯度更新模块

在计算得到总损失 $\mathcal{L}^t$ 后，对当前去噪步的潜变量 $z_t$ 施加梯度优化：

$$z_t' = z_t - \alpha \nabla_{z_t} \mathcal{L}^t$$

其中 $\alpha$ 为学习率。优化在前 5 个去噪步中执行，每步最多进行 10 次梯度更新。为减少计算开销，方法引入了基于相关性的早停机制：若当前步的 Pearson 相关系数超过阈值 $\tau_{\mathrm{corr}}$，则提前终止该步的优化。

### 音频对齐扩展

对于音频驱动的时序控制，TEMPOCONTROL 将音频起始强度包络 $\hat{s}_t$ 处理为控制信号。经过阈值保留与高斯平滑后得到 $\tilde{s}_t$，用作时间掩码 $m_i$ 的替代目标，使生成的视频内容与音频节奏对齐。该扩展在简单音频峰值场景下已验证有效，复杂音频的泛化性仍有待进一步验证。

## 实验与关键发现

### 时序控制基准评估

TEMPOCONTROL 在三个自建的时序控制基准上进行了系统评估：单对象（One Object）、双对象（Two Objects）和动作（Movement）控制。评估采用四个指标：Temporal Accuracy（时序准确率）、Absence（缺失帧准确率）、Presence（存在帧准确率）和 Imaging Quality（成像质量，通过 CLIP-I 衡量）。目标检测由 YOLOv10 完成，动作检测依赖光流，两者作为代理指标提供量化参考。

**Table 1** 展示了在 Wan2.1-S、Wan2.1-L 和 CogVideoX-5B 三个主干模型上的对比结果。核心发现如下：

- **单对象控制**：Wan2.1-S 的 Temporal Accuracy 从 63.94% 提升至 **83.56%**（+19.62%），Wan2.1-L 从 69.50% 提升至 **85.06%**（+15.56%），CogVideoX-5B 从 49.75% 提升至 **66.88%**（+17.13%）。提升主要来自 Presence 指标的显著改善（Wan2.1-S 从 56.94% 升至 79.75%），表明模型在指定时间窗口内成功生成了目标对象。
- **双对象控制**：Wan2.1-S 的 Temporal Accuracy 从 37.50% 提升至 **53.17%**（+15.67%）。该任务难度显著高于单对象，基线模型的准确率普遍偏低，TEMPOCONTROL 在此场景下仍带来一致增益。
- **动作控制**：Wan2.1-S 的 Temporal Accuracy 从 19.00% 提升至 **54.00%**（+35.00%），提升幅度最大，说明文本提示中的动作时序描述对基线模型几乎无效，而 TEMPOCONTROL 能够有效纠正这一行为。

### VBench 多对象基准

为验证方法对通用视频生成质量的影响，在 VBench 多对象基准上进行了测试（**Table 2**）。TEMPOCONTROL 在 Wan2.1-S 上将 Multiple Object (GRiT) 指标从 74.13% 提升至 **76.37%**（+2.24%），同时其他 VBench 指标保持稳定或略有提升。这表明时间注意力引导不仅没有损害空间语义，反而通过熵正则化帮助维持了多对象场景下的语义一致性。

![[assets/figures/papers/paper_list_l30_https_openaccess_thecvf_com_content_CVPR2026_html_Schiber_TempoControl_T/figures/006_Table_2.jpg]]
*Table 2: Comparison on the multiple-object benchmark. Baselines rely on text-only temporal cues, while Ours applies TEMPOCON-TROL. Bold denotes the best result in each column*

### 消融实验

**Table 3** 在单对象基准上对损失项进行了消融分析，揭示了各组件的功能分工：

- **仅 Pearson 相关项（C）**：带来显著的时序准确率提升，但成像质量下降，表明单纯的时序对齐会牺牲空间语义保真度。
- **仅熵正则项（E）**：获得最高的成像质量（59.52%），但时序准确率提升有限，说明熵正则主要作用于维持空间一致性。
- **完整方法（C+E）**：达到最佳的时序准确率，且成像质量接近仅使用熵正则的水平，验证了两个组件的互补性。

**Figure 4** 的定性结果进一步证实：不使用熵正则时，注意力过度聚焦会导致对象形态扭曲；加入熵正则后，模型在满足时序约束的同时保持了合理的空间分布。

### 用户调研

**Table 4** 展示了用户调研结果。参与者在时序准确性和视觉质量两个维度上对 TEMPOCONTROL 与 Wan2.1 基线进行盲评。TEMPOCONTROL 在时序准确性上获得显著偏好，视觉质量与基线持平或略优，与定量指标趋势一致。

### 失败模式与局限性

尽管 TEMPOCONTROL 在多数场景下有效，仍存在以下局限：

1. **推理开销增加**：方法在前 5 个去噪步中每步最多执行 10 次梯度更新，相比标准采样增加了计算时间。虽然无需重新训练，但在实时应用场景中仍需优化。
2. **属性偏移风险**：当前损失函数未显式约束完整的语义一致性，在某些情况下可能引入轻微的颜色或纹理变化。
3. **评估指标噪声**：时序缺失（Absence）指标依赖 YOLOv10 检测，在图像质量下降或遮挡场景下可能产生假阴性，需结合定性分析综合判断。
4. **多概念协调不足**：双对象场景下的约束设计仍较初步，未对多概念间的交互关系进行显式建模。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| Table 1 | 三个基准上 Temporal Accuracy 均大幅提升，动作控制增益最大（+35%） |
| Table 2 | VBench 多对象指标提升 2.24%，其他指标未退化 |
| Table 3 | Pearson 相关驱动时序对齐，熵正则维护语义保真度，二者互补 |
| Figure 4 | 熵正则防止注意力过度聚焦导致的对象形态扭曲 |
| Table 4 | 用户偏好 TEMPOCONTROL 的时序准确性，视觉质量与基线持平 |

![[assets/figures/papers/paper_list_l30_https_openaccess_thecvf_com_content_CVPR2026_html_Schiber_TempoControl_T/figures/005_Table_1.jpg]]
*Table 1: Comparison on one-object, two-object, and movement temporal-control benchmarks. Baselines rely on text-only temporal cues, while Ours applies TEMPOCONTROL on the corresponding backbone. Bold denotes the best result in each block*

![[assets/figures/papers/paper_list_l30_https_openaccess_thecvf_com_content_CVPR2026_html_Schiber_TempoControl_T/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the one-object benchmark. C denotes Pearson correlation and E denotes entropy. Bold denotes the best result in each column*

![[assets/figures/papers/paper_list_l30_https_openaccess_thecvf_com_content_CVPR2026_html_Schiber_TempoControl_T/figures/008_Table_4.jpg]]
*Table 4: User study comparing our method with Wan2.1 in terms of temporal accuracy and visual quality*

![[assets/figures/papers/paper_list_l30_https_openaccess_thecvf_com_content_CVPR2026_html_Schiber_TempoControl_T/figures/010_Figure_6.jpg]]
*Figure 6: Examples of video alignment to an audio signal. 5.2. Qualitative Results*

## 定位与知识库关联

### 任务定位与基线关系

TEMPOCONTROL 解决的是文本到视频生成中的一个新问题：**细粒度时序控制**——即在推理时指定某个视觉概念在视频序列中出现的具体时间窗口，而不修改模型参数。这一问题不同于传统的文本到视频生成（仅依赖提示文本中的时间副词，如“first”、“then”），也不同于已有的空间可控生成或运动可控生成。

在现有 T2V 模型中，**Wan2.1-S** 和 **Wan2.1-L**（Wan et al., arXiv 2025）以及 **CogVideoX-5B**（Yang et al., arXiv 2024）仅依赖文本中的时间描述来间接控制时序，但实验表明这种控制极不可靠——即便提示明确指定“狗在后半段出现”，模型仍可能在早期帧就生成该对象（Figure 2）。TEMPOCONTROL 在**不微调**这些基座模型的前提下，通过推理时潜变量优化，将时序准确率大幅提升（例如 Wan2.1-S 单对象场景从 63.94% 提升至 83.56%，+19.62%）。

从方法谱系来看，TEMPOCONTROL 属于**推理时注意力引导**（inference-time attention guidance）范式。该范式在图像生成领域已有广泛探索（通过操控交叉注意力图实现布局控制、属性绑定等），但在视频生成中首次被用于**时间维度**的细粒度控制。其核心创新在于将空间交叉注意力聚合为时间注意力信号 $a_i^t$，并通过 Pearson 相关、幅度损失和空间熵正则三组损失函数对该信号进行形状与强度调控。

### 核心机制与设计选择

TEMPOCONTROL 的因果操控旋钮是**交叉注意力图的时间注意力信号** $a_i^t$，它编码了每个文本词在各帧的语义影响强度。方法在去噪的前 $K$ 步（默认 $K=5$）对潜变量 $z_t$ 施加梯度优化：

$$z_{t}^{\prime} = z_{t} - \alpha \nabla_{z_{t}} \mathcal{L}^{t}$$

其中总损失由三项加权组成：

$$\mathcal{L}^{t} = \mathcal{L}_{\mathrm{corr}}^{t} + \lambda_{1} \mathcal{L}_{\mathrm{mag}}^{t} + \lambda_{2} \mathcal{L}_{\mathrm{entropy}}^{t}$$

- **$\mathcal{L}_{\mathrm{corr}}$**（Pearson 相关损失）：衡量标准化后的注意力信号与目标时间掩码 $m_i$ 的线性匹配程度，是时序对齐的**主要驱动力**。
- **$\mathcal{L}_{\mathrm{mag}}$**（幅度损失）：通过正项 $\mathcal{L}_{\oplus}$ 增强活跃帧的注意力强度，通过负项 $\mathcal{L}_{\ominus}$ 抑制非活跃帧的注意力，确保概念在指定时间窗口“充分可见”。
- **$\mathcal{L}_{\mathrm{entropy}}$**（空间熵正则）：对活跃帧的空间注意力分布施加熵最小化，防止注意力过度扩散导致语义扭曲。消融实验（Table 3）表明，仅使用相关项（C）虽能提升时序准确率，但会牺牲成像质量；单独使用熵正则（E）获得最高成像质量（59.52%）；完整方法（C+E）达到最佳时序准确率且成像质量接近最优。

### 适用边界与局限

1. **推理开销**：方法在前 5 个去噪步中每步最多 10 次梯度更新，虽然无需重新训练，但仍比标准采样慢。对于实时应用场景，这一开销需要权衡。
2. **语义保真度**：当前损失函数未显式约束完整的语义一致性，可能引入轻微的属性偏移（如颜色变化）。熵正则缓解了这一问题，但并非完全消除。
3. **评估噪声**：时序缺失（Absence）指标依赖 YOLOv10 物体检测，可能因检测失败或图像质量下降产生噪声；时序存在（Presence）指标更可靠，主要提升来自 Presence。
4. **多对象协调**：当前方法对多对象场景的约束设计仍较初步，未显式协调多个概念之间的交互关系（如遮挡、共现）。
5. **音频对齐泛化**：音频-视频对齐仅在简单场景（清晰音频峰值）上验证，复杂音频（如混合音源）的泛化性有待检验。

### 开放问题

- 如何将该方法扩展到更复杂的多模态控制（例如同时控制多个对象的出现时间及交互关系）？
- 能否通过自适应调整优化步数和学习率来进一步降低推理计算开销？
- 熵正则项在更广泛的视频生成任务中是否具有普遍的正则化作用？
- 如何结合少量标注数据对控制信号进行微调，以进一步提升在困难场景下的时序精度？
- 该方法能否与其他推理时控制技术（如运动控制、相机控制）结合，实现统一的视频编辑框架？

## 原文 PDF

![[paperPDFs/CVPR_2026/TempoControl_Temporal_Attention_Guidance_for_Text_to_Video_Models.pdf]]

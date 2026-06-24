---
title: "Score Distillation Sampling for Audio: Source Separation, Synthesis, and Beyond"
type: paper
paper_level: A
venue: ICML
year: 2025
pdf_ref: paperPDFs/ICML_2025/Score_Distillation_Sampling_for_Audio_Source_Separation_Synthesis_and_Beyond.pdf
aliases:
- AS
- SDSASSSB
tags:
- ICML_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "解码器端分数蒸馏采样（Decoder-SDS）通过避免编码器微分，显著稳定了音频领域的SDS优化过程，是提升生成质量和语义对齐的关键设计选择。"
primary_logic: "通过将预训练文本到音频扩散模型的评分函数作为蒸馏信号，可引导任意可微分参数化音频表示（如FM合成、物理冲击模拟、源分离潜在变量）对齐文本描述，从而用单一冻结模型统一多种音频任务，无需任务特定数据集。"
claims:
- "Decoder-SDS 避免了编码器的微分不稳定性，显著提升了音频生成的稳定性和质量。"
- "多尺度频谱加权比时间域L2损失更好地保留了瞬态和高频细节，提升了感知质量。"
- "多步去噪提供了更稳定的引导信号，相比单步去噪在CLAP分数上提升0.14。"
- "Audio-SDS 在提示驱动源分离中将平均SDR从-2.5 dB提升至2.2 dB（+4.7），表明SDS更新有效正则化了欠定分离。"
---

# Score Distillation Sampling for Audio: Source Separation, Synthesis, and Beyond

> [!tip] 核心洞察
> 通过将预训练文本到音频扩散模型的评分函数作为蒸馏信号，可引导任意可微分参数化音频表示（如FM合成、物理冲击模拟、源分离潜在变量）对齐文本描述，从而用单一冻结模型统一多种音频任务，无需任务特定数据集。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 音频分数蒸馏采样：源分离、合成及其他 |
| 英文题名 | Score Distillation Sampling for Audio: Source Separation, Synthesis, and Beyond |
| 会议/期刊 | ICML 2025 |
| Links | [paper](https://arxiv.org/abs/2505.04621); [Project](https://research.nvidia.com/labs/toronto-ai/Audio-SDS/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Audio-SDS |
| Dataset | Prompt-driven Source Separation (10s clips), Prompt-driven Source Separation (first half), Prompt-driven Source Separation, Impact Synthesis (e.g., kick drum, hitting pot) |

> [!tip] 效果简介
> - Prompt-driven Source Separation (10s clips) 上，SDR (dB) 为 2.2 (mean)，对比 -2.5 (mean)，变化 +4.7。
> - Prompt-driven Source Separation (first half) 上，SDR (dB) 为 9.4 (mean)，对比 -2.3 (mean)，变化 +11.7。
> - Prompt-driven Source Separation 上，Mean CLAP score 为 0.2，对比 0.18，变化 +0.02。

## 概述

**问题瓶颈**：现有文本到音频扩散模型主要关注从噪声中生成采样，缺乏对可解释结构化参数（如合成器旋钮、物理模拟系数）的直接优化能力，难以在结构化约束下生成语义一致且可控的音频。

**核心洞察**：将预训练文本到音频扩散模型的评分函数作为蒸馏信号，可引导任意可微分参数化音频表示（FM合成、物理冲击模拟、源分离潜在变量）对齐文本描述，从而用单一冻结模型统一多种音频任务，无需任务特定数据集。

**方法定位**：Audio-SDS 将原本用于文本到3D生成的分数蒸馏采样（Score Distillation Sampling, SDS）迁移至音频领域，并提出三项关键改进以稳定优化过程：
- **Decoder-SDS**：在解码后的音频域计算更新，避免通过VAE编码器微分带来的不稳定性（Fig. 10, +0.15 CLAP vs. Encoder-SDS）。
- **多尺度频谱加权**：使用多个窗口大小的STFT幅度残差替代时域L2损失，更好地保留瞬态和高频细节（Fig. 11）。
- **多步去噪**：采用DDIM多步部分去噪提供更稳定的引导信号，相比单步去噪在CLAP分数上提升0.14（Fig. 12）。

**主要结果**：
- **提示驱动源分离**：将平均SDR从-2.5 dB提升至2.2 dB（+4.7 dB），前半段音频更达9.4 dB（+11.7 dB）（Table 1），在保持低重建损失的同时提升了语义对齐（Table 2, CLAP +0.02）。
- **FM合成与冲击合成**：CLAP分数随优化持续上升（Fig. 7），冲击合成跨提示提升0.10–0.18，FM合成提升0.13（Fig. 6），验证了语义对齐的逐步增强。

**局限性**：方法对分布外提示效果差，长音频（>10–15秒）可能出现过渡生硬或静音；简单参数模型（如FM合成器）难以表达超出其能力的声源；训练对超参数敏感，需针对不同提示仔细调节。

## 背景与动机

### 文本到音频生成与结构化约束的鸿沟

近年来，文本到音频扩散模型在生成采样质量上取得了显著进展，能够根据自然语言描述生成逼真的音频片段。然而，这些模型的核心能力被锁定在“从噪声生成波形”这一范式内——它们擅长无条件或有条件的随机采样，却缺乏对**可解释参数**的直接优化能力。当任务需要生成符合结构化约束的音频时（例如，调整FM合成器的调制矩阵以匹配“深沉的回响底鼓”，或从混合录音中分离出“萨克斯风”与“交通噪声”），现有扩散模型无法直接操作这些参数化表示，导致语义一致的音频生成成为一个开放挑战。

这一瓶颈的根源在于：扩散模型的评分函数（score function）虽然提供了数据分布密度的梯度方向，但传统上仅用于采样过程本身，而非作为通用优化信号来引导可微分参数化模型。**核心洞察**在于，若能将冻结的预训练文本到音频扩散模型视为一个“语义评分黑箱”，其预测噪声与真实噪声的残差便可蒸馏为参数更新方向，从而将扩散模型的能力从生成采样拓展到参数优化——这正是Score Distillation Sampling（SDS）的核心思想。然而，SDS最初在文本到3D合成领域提出，将其迁移到音频领域面临三个关键障碍：

1. **编码器微分的不稳定性**：音频扩散模型通常依赖VAE将波形压缩到潜空间。标准SDS需要在潜空间计算梯度，这要求微分通过VAE编码器，而编码器的非线性压缩过程引入了梯度噪声和训练不稳定。
2. **时域损失对感知质量的忽视**：标准SDS在时间域计算L2残差，但人类听觉对瞬态和高频细节的感知高度依赖频谱特征，时域损失难以保留这些关键信息。
3. **单步去噪的引导质量不足**：原始SDS仅使用单步去噪预测，其评分信号在优化初期可能过于粗糙，导致收敛缓慢或陷入局部最小值。

### 从3D到音频：SDS的跨模态迁移挑战

SDS在文本到3D合成中的成功依赖于图像扩散模型对渲染图像的评分能力。将其迁移到音频领域时，上述三个障碍的严重程度被放大：音频的时频特性使得潜空间压缩更容易丢失精细瞬态信息；音频合成任务（如FM合成、物理冲击模拟）的参数空间通常比3D渲染更小但更刚性，对梯度质量要求更高；且音频领域缺乏像3D那样成熟的参数化先验模型。

本文的**动机**正是填补这一空白：通过系统性地改造SDS的更新域、损失空间和去噪策略，使其适配音频扩散模型的特性，从而用**单一冻结模型**统一解决FM合成参数调优、物理冲击合成、提示驱动源分离等多种音频任务——所有这些任务共享同一扩散先验，无需任何任务特定数据集或微调。

## 核心创新

Audio-SDS 的核心创新并非提出新的扩散模型架构，而是**将冻结的预训练文本到音频扩散模型重新定位为可微分评分函数**，通过分数蒸馏采样（SDS）将文本语义直接注入可解释的参数化音频表示中。这一范式转换的关键在于三个相互关联的设计选择（changed slots），它们共同解决了将 SDS 从图像/三维领域迁移至音频领域时面临的根本性不稳定问题。

### 瓶颈与因果机制

现有文本到音频扩散模型的主要瓶颈在于：它们擅长无条件或有条件生成采样，但缺乏对**结构化参数**（如合成器旋钮、物理模拟系数、分离源潜在变量）的直接优化能力。这导致难以在保持语义一致性的同时满足显式约束（如源分离中的重建保真度）。

Audio-SDS 的因果机制可概括为：**解码器端评分蒸馏（Decoder-SDS）作为稳定化核心，多尺度频谱加权作为感知保真度增强，多步部分去噪作为收敛稳定性保障**。这三者构成一条因果链——Decoder-SDS 避免了编码器梯度带来的优化崩溃，频谱加权确保更新方向与人类听觉感知对齐，多步去噪则提供了更可靠的评分信号，使整个优化过程能够稳定收敛。

### Changed Slot 1：从潜在空间到解码音频域的 SDS 更新

标准 SDS 在潜在扩散模型的潜在空间中计算更新，这要求对编码器 $\operatorname{enc}_\phi$ 进行微分（见 Eq. (4)）。在音频领域，这一设计暴露出严重的数值不稳定问题：VAE 编码器的梯度在高频分量上存在剧烈的局部振荡，导致优化过程频繁发散或陷入病理局部最小值。

Audio-SDS 提出的 **Decoder-SDS**（Eq. (5)）将更新域从潜在空间转移至解码后的音频波形空间：

$$\mathbf{u}_{\mathrm{SDS}}^{\mathrm{dec}}(\theta; p) = \Big( \underset{t', \epsilon}{\mathbb{E}} [ \hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p) ] - \mathbf{x}(\theta) \Big) \nabla_{\theta} \mathbf{x}(\theta)$$

其中 $\hat{\mathbf{x}}_{\phi}$ 是经过“编码→加噪→去噪→解码”完整管线后的重建音频。该设计的核心洞察在于：**编码器仅作为前向计算的一部分参与噪声预测，但其雅可比被完全避免**，梯度仅通过可微渲染器 $\mathbf{x}(\theta)$ 回传。消融实验（Fig. 10）证实，Decoder-SDS 在冲击合成任务上相较 Encoder-SDS 提升 **+0.15 CLAP**，且定性结果显示出更稳定的收敛行为。

### Changed Slot 2：从时域 L2 残差到多尺度频谱加权

标准 SDS 在原始信号空间（对图像为像素空间，对音频为波形采样点）计算 L2 残差。然而，音频感知质量高度依赖于频谱能量分布，时域 L2 损失对相位差异过度敏感，而对瞬态和高频细节的保留能力不足。

Audio-SDS 引入**多尺度频谱加权**（Eq. (7)），在多个 STFT 窗口大小 $\{S_m\}_{m=1}^M$ 上计算幅度谱残差：

$$\mathbf{u}_{\mathrm{SDS}}^{S,\mathrm{dec}}(\theta; p) = \sum_{m} \Bigl( \mathbb{E}\bigl[ S_{m}(\hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p)) \bigr] - S_{m}(\mathbf{x}(\theta)) \Bigr) \nabla_{\theta} S_{m}(\mathbf{x}(\theta))$$

该设计借鉴了多尺度频谱损失在音频重建中的成功经验，通过平均不同时间-频率分辨率的窗口来避免单一窗口的时频权衡困境。消融实验（Fig. 11）表明，频谱加权相比时域 L2 损失在源分离重建中定性保留了更清晰的瞬态结构，听觉质量显著更优。

### Changed Slot 3：从单步去噪到多步部分去噪

标准 SDS 在每个优化步中仅执行单次加噪-去噪操作，这导致评分信号方差较大，尤其在优化初期参数远离分布时。Audio-SDS 采用 **DDIM 多步部分去噪**（Sec. 3.1.3），在 2-10 步内逐步精炼噪声潜在表示，从而获得更稳定的评分估计。

这一改进的直觉在于：单步去噪对噪声采样的随机性高度敏感，而多步去噪通过部分逆扩散过程平滑了评分信号，减少了梯度方差。消融实验（Fig. 12）显示，10 步去噪相比单步去噪在冲击合成中提升 **+0.14 CLAP**，且定性谱图展现出更清晰的谐波结构。

### 创新协同效应

三个 changed slots 之间存在协同放大效应。Decoder-SDS 提供了稳定的梯度传播基础，使得频谱加权和多步去噪的改进能够有效累积；频谱加权确保感知相关的频率成分获得更大的更新幅度；多步去噪则降低了评分信号噪声，使频谱加权的精细调整不被随机扰动淹没。这一协同作用在源分离任务中尤为突出：联合更新（Eq. (13)）将平均 SDR 从 -2.5 dB 提升至 2.2 dB（**+4.7 dB**），同时 CLAP 语义对齐分数从 0.18 提升至 0.20。

### 方法局限性

尽管上述创新显著提升了音频 SDS 的可行性与质量，但方法仍存在若干根本性限制：对分布外提示（out-of-distribution prompts）效果急剧退化，输出可能退化为重复噪声；较长音频（超过 10-15 秒）的优化容易出现过渡生硬或末端静音伪影；简单参数模型（如 FM 合成器）的表达能力上限限制了复杂声景的生成质量（例如，FM 合成无法生成“木勺敲锅”的金属质感，见 Fig. 6）。此外，高分类器自由引导（CFG）尺度可能导致优化陷入病理局部最小值，训练过程对超参数选择敏感。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our Audio-SDS method, marrying the Score Distillation Sampling (SDS) [66] with an audio diffusion model in a robust framework for various audio tasks. SDS (see Sec. 2.2) – originally developed for text-to-3D generation – computes an update for rendered data x in the diffusion models modality (e.g., image or audio), then propagates that update through a differentiable simulation g to update parameters θ. Intuitively, this nudges the render parameters to make it “more likely” under our conditioning, here the text prompt p. Adapting SDS to audio, we propose three modifications shown in red: (a) Decoder-SDS to circumvent differentiating through the encoder (Sec. 3.1.1), (b) a spectr...*

Audio-SDS 的核心思想是将预训练文本到音频扩散模型的评分函数作为蒸馏信号，引导任意可微分参数化音频表示对齐文本描述，从而用一个冻结的扩散模型统一多种音频任务。其整体 pipeline 由三个关键阶段构成：**可微音频渲染**、**扩散模型评分**、**参数更新**。

### 模块关系与数据流

整个框架的模块关系与输入输出流如下：

1. **可微音频渲染器 `g_audio`**：接收可优化参数 `θ`，生成立体声波形 `x = g_audio(θ)`。这是整个 pipeline 的起点，也是唯一需要梯度的生成模块。根据任务不同，`g_audio` 可以是 FM 合成器、物理冲击模拟器或源分离的潜在变量表示（Sec. 3.2）。

2. **VAE 编码器 `enc`**：将渲染的音频波形 `x` 压缩到潜在空间 `h = enc(x)`，为后续扩散过程提供紧凑表示。该模块来自预训练音频扩散模型的冻结组件（Sec. 2.3）。

3. **扩散去噪器（冻结）**：对加噪后的潜在表示 `z` 预测噪声 `ε̂_φ(z, t', p)`，提供文本条件 `p` 下的评分信号。该模块完全冻结，不参与梯度计算——这是 SDS 方法的核心设计选择（Sec. 2.2）。

4. **VAE 解码器 `dec`**：将去噪后的潜在表示解码回音频波形 `x̂ = dec(ẑ)`。在 **Decoder-SDS** 设计中，评分信号的差异在解码后的音频域计算，从而避免了通过编码器 `enc` 反向传播梯度（Sec. 3.1.1）。

5. **多尺度 STFT 模块**：计算多个窗口大小的频谱幅度 `S_m(·)`，用于频谱加权损失。该模块强调瞬态和高频细节，相比时间域 L2 损失更好地保留了感知质量（Sec. 3.1.2）。

6. **DDIM 采样器（多步去噪）**：执行多个部分去噪步骤（通常 2-10 步），逐步精炼加噪潜在表示，提供更稳定的引导信号。相比单步去噪，多步去噪在 CLAP 分数上提升 0.14（Fig. 12；Sec. 3.1.3）。

### 关键设计选择：Decoder-SDS

标准 SDS 在潜在空间计算更新，需要对编码器求导：

$$
\mathbf{u}_{\mathrm{SDS}}(\pmb{\theta}; p) = \underset{t', \epsilon, c}{\mathbb{E}} [ \omega(t') ( \hat{\epsilon}_{\phi}(\mathbf{z}(\pmb{\theta}, c), t', p) - \epsilon ) \nabla_{\pmb{\theta}} \mathbf{z}(\pmb{\theta}, c) ]
$$

然而，音频 VAE 编码器的微分不稳定，导致优化过程震荡。Decoder-SDS 将评分差异的计算转移到解码后的音频域，更新公式变为：

$$
\mathbf{u}_{\mathrm{SDS}}^{\mathrm{dec}}(\theta; p) = \Big( \underset{t', \epsilon}{\mathbb{E}} [ \hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p) ] - \mathbf{x}(\theta) \Big) \nabla_{\theta} \mathbf{x}(\theta)
$$

其中 `x̂_φ` 是经过“编码→加噪→去噪→解码”完整流程后的重建音频。这一设计是提升音频生成稳定性和质量的关键因果旋钮——消融实验表明，Decoder-SDS 在冲击合成中相比 Encoder-SDS 在 CLAP 上提升 0.15（Fig. 10）。

### 频谱加权与多步去噪

Decoder-SDS 进一步结合多尺度频谱加权，得到最终更新形式：

$$
\mathbf{u}_{\mathrm{SDS}}^{S,\mathrm{dec}}(\theta; p) = \sum_{m} \Bigl( \mathbb{E}\bigl[ S_{m}(\hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p)) \bigr] - S_{m}(\mathbf{x}(\theta)) \Bigr) \nabla_{\theta} S_{m}(\mathbf{x}(\theta))
$$

该更新通过多个 STFT 窗口大小 `m` 的频谱幅度残差加权，强调瞬态和高频细节，避免单一窗口大小带来的时间-频率权衡（Sec. 3.1.2）。

### 任务适配

上述通用 pipeline 通过切换 `g_audio` 的具体实现适配三种任务（Fig. 2）：

- **FM 合成**：`θ` 为 FM 矩阵 `A` 和各振荡器的频率比 `ω_v`、起音 `α_v`、衰减 `δ_v`，`g_audio` 输出调制后的合成音频。
- **物理冲击合成**：`θ` 控制物体脉冲响应 `I_obj^θ`（阻尼正弦和）和混响脉冲响应 `I_reverb^θ`，渲染音频为两者的卷积。
- **提示驱动源分离**：`θ = {θ_k}` 对应 `K` 个源的参数，联合更新结合了重建损失梯度 `∇_θ L_rec(θ)` 和各源 SDS 更新的加权和（γ 控制权衡）。

### 证据强度

Decoder-SDS 和频谱加权的有效性均有强消融证据支持（confidence ≥ 0.95）。多步去噪的定量提升（+0.14 CLAP）来自受控对比实验。整体框架在源分离任务中将平均 SDR 从 -2.5 dB 提升至 2.2 dB（+4.7 dB，Table 1），在冲击合成中 CLAP 分数随优化持续上升（Fig. 7），表明语义对齐逐步增强。

## 核心模块与公式推导

### 3.1 可微音频渲染器 g_audio

Audio-SDS 的核心抽象是将任意音频生成过程封装为一个可微渲染函数：

$$ \mathbf{x} = g_{\text{audio}}(\pmb{\theta}) \in \mathbb{R}^{2 \times T} $$

其中 $\pmb{\theta}$ 为可优化参数，$\mathbf{x}$ 为立体声音频波形。该抽象将三类任务统一为同一优化框架：FM 合成中 $\pmb{\theta}$ 为合成器参数，物理冲击合成中 $\pmb{\theta}$ 为脉冲响应参数，源分离中 $\pmb{\theta}$ 为各源波形的直接表示（Sec. 3.2）。渲染器 $g_{\text{audio}}$ 必须可微，以便将扩散模型的评分信号通过链式法则反向传播至参数空间。

### 3.2 标准 SDS 损失与更新

给定文本提示 $\pmb{p}$，标准 SDS 在扩散模型的潜在空间定义损失：

$$ \mathcal{L}_{\mathrm{SDS}}(\pmb{\theta}; \pmb{p}) = \underset{t', \epsilon, c}{\mathbb{E}} \left[ \omega(t') \| \hat{\epsilon}_{\phi}(\mathbf{z}(\pmb{\theta}, c), t', \pmb{p}) - \epsilon \|^2 \right] \tag{Eq. 2} $$

其中 $\mathbf{z}(\pmb{\theta}, c) = \alpha_{t'} \mathbf{g}(\pmb{\theta}, c) + \sigma_{t'} \epsilon$ 为加噪后的渲染结果，$\hat{\epsilon}_{\phi}$ 为冻结扩散模型的噪声预测，$\epsilon \sim \mathcal{N}(0, I)$ 为实际添加的噪声，$t'$ 为采样时间步，$c$ 为条件变量（如 CFG 的引导尺度），$\omega(t')$ 为时间步权重。

SDS 的核心近似在于省略扩散模型雅可比 $\mathbf{J}_{\hat{\epsilon}_{\phi}}(\mathbf{z})$，将其视为单位矩阵，从而得到简洁的参数更新：

$$ \mathbf{u}_{\mathrm{SDS}}(\pmb{\theta}; p) = \underset{t', \epsilon, c}{\mathbb{E}} \left[ \omega(t') \left( \hat{\epsilon}_{\phi}(\mathbf{z}(\pmb{\theta}, c), t', p) - \epsilon \right) \nabla_{\pmb{\theta}} \mathbf{z}(\pmb{\theta}, c) \right] \tag{Eq. 4} $$

该更新直观上将渲染结果“推向”扩散模型认为更符合文本提示的方向。

### 3.3 Decoder-SDS：规避编码器微分

标准 SDS 在潜在空间计算更新，需通过 VAE 编码器 $\mathrm{enc}_{\phi}$ 反向传播梯度。作者发现，音频 VAE 编码器的微分不稳定，导致优化过程发散。Decoder-SDS 将更新计算移至解码后的音频域，完全规避编码器梯度：

$$ \mathbf{u}_{\mathrm{SDS}}^{\mathrm{dec}}(\theta; p) = \left( \underset{t', \epsilon}{\mathbb{E}} \left[ \hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p) \right] - \mathbf{x}(\theta) \right) \nabla_{\theta} \mathbf{x}(\theta) \tag{Eq. 5} $$

其中 $\hat{\mathbf{x}}_{\phi}$ 为“编码→加噪→去噪→解码”后的重建音频：

$$ \hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p) = \operatorname{dec}_{\phi}\left( \operatorname{denoise}_{\phi}\left( \mathrm{noise}(\mathrm{enc}_{\phi}(\mathbf{x}(\theta)), t', \epsilon), p \right) \right) $$

关键设计选择：梯度仅通过 $\mathbf{x}(\theta)$ 端（即解码器输出与渲染音频的差异端）流动，$\hat{\mathbf{x}}_{\phi}$ 端被 detach，不参与梯度计算。消融实验证实，Decoder-SDS 在冲击合成中相比 Encoder-SDS 的 CLAP 提升 **+0.15**（Fig. 10），是提升生成稳定性和质量的核心决策。

### 3.4 多尺度频谱加权

时域 L2 残差对瞬态和高频细节不敏感。Audio-SDS 引入多尺度 STFT 幅度残差，在 $M$ 个不同窗口大小上计算频谱差异：

$$ \mathbf{u}_{\mathrm{SDS}}^{S,\mathrm{dec}}(\theta; p) = \sum_{m=1}^{M} \left( \mathbb{E}_{t', \epsilon}\left[ S_m(\hat{\mathbf{x}}_{\phi}(\theta, t', \epsilon, p)) \right] - S_m(\mathbf{x}(\theta)) \right) \nabla_{\theta} S_m(\mathbf{x}(\theta)) \tag{Eq. 7} $$

其中 $S_m(\cdot)$ 为第 $m$ 个窗口大小的 STFT 幅度谱。多窗口设计避免了单一窗口的时间-频率分辨率权衡：大窗口提供更好的频率分辨率，小窗口捕获瞬态细节。实验定性显示，频谱加权比 L2 强调更好地保留了瞬态和听觉质量（Fig. 11）。

### 3.5 多步部分去噪

标准 SDS 使用单步去噪，噪声预测方差大。Audio-SDS 采用 DDIM 采样器执行 $2\sim10$ 步部分去噪，每步从当前噪声水平向干净信号方向推进：

$$ \hat{\mathbf{z}} = \operatorname{DDIM}_{\phi}(\mathbf{z}(\theta, c), t', p, \text{steps}=K) $$

多步去噪提供了更稳定的引导信号。消融实验显示，10 步去噪相比单步去噪在冲击合成中 CLAP 提升 **+0.14**（Fig. 12），在所有任务上一致改善了收敛稳定性。

### 3.6 源分离的联合更新

对于提示驱动源分离，混合信号 $\mathbf{m}$ 被建模为 $K$ 个源波形的和：

$$ \mathbf{m} \approx \sum_{k=1}^{K} \mathbf{g}_k(\pmb{\theta}_k) = \mathbf{g}(\pmb{\theta}) $$

欠定分解通过两项联合正则化：多尺度 STFT 重建损失要求分离源之和等于混合信号，SDS 更新要求每个分离源对齐其文本提示。重建损失定义为：

$$ \mathcal{L}_{\mathrm{rec}}(\pmb{\theta}) = \sum_{m=1}^{M} \left\| S_m(\mathbf{m}) - S_m\left( \sum_{k=1}^{K} \mathbf{g}_k(\pmb{\theta}_k) \right) \right\|_2^2 \tag{Eq. 12} $$

最终联合更新为两项的加权和：

$$ \mathbf{u}_{\mathrm{Sep}}(\pmb{\theta}; \{p_k\}_{k=1}^{K}) = \nabla_{\pmb{\theta}} \mathcal{L}_{\mathrm{rec}}(\pmb{\theta}) + \gamma \sum_{k=1}^{K} \mathbf{u}_{\mathrm{SDS}}^{S,\mathrm{dec}}(\pmb{\theta}_k; \pmb{p}_k) \tag{Eq. 13} $$

其中 $\gamma$ 控制语义对齐与重建保真度之间的权衡。该更新将平均 SDR 从 **-2.5 dB 提升至 2.2 dB**（+4.7 dB），表明 SDS 更新有效正则化了欠定分离问题（Table 1）。

## 实验与分析

### 核心任务结果

**提示驱动源分离**是Audio-SDS最具挑战性的验证场景。给定一段10秒混合音频，方法需在无监督条件下将混合信号分解为多个与文本提示语义一致的声源，同时满足重建约束——即分离源之和必须等于原始混合信号。Table 1报告了信号失真比（SDR）的定量结果。


![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/010_Table_1.jpg]]
*Table 1: Source Separation Distance to Ground-truth. We show Signal-to-Distortion Ratio (SDR) in dB (higher is better) for each separated source of the full 10s clips. Our method improves significantly over the baseline, boosting mean SDR to the source prompts from - 2 . 5 $\to$ 2 . 2 ( + 4 . 7 ) Most recovery artifacts are at the audio’s end, which we hypothesize is due to the diffusion model preferring audio with silence at the end. Comparing recovery for only the first half, we see the mean SDR goes from −2.3 → 9.4(+11.7)*

在完整10秒片段上，Audio-SDS将平均SDR从基线-2.5 dB提升至2.2 dB（**+4.7 dB**），表明SDS更新有效正则化了欠定分离问题。当仅评估前半段时，平均SDR从-2.3 dB跃升至9.4 dB（**+11.7 dB**），暗示大部分恢复伪影集中在音频末端。作者推测这源于扩散模型对末尾静音的偏好——预训练模型倾向于生成以静音结尾的音频，导致分离源在尾部区域出现失真。

Table 2从语义对齐角度补充了评估。Audio-SDS在保持低重建损失的同时，将平均CLAP分数从0.18提升至0.20（+0.02），最大CLAP从0.27提升至0.34（+0.10）。这组数据揭示了方法的核心能力：在严格重建约束下，SDS更新仍能为每个分离源注入与提示一致的语义特征。


![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/009_Table_2.jpg]]
*Table 2: Source Separation Prompt Alignment. We show CLAP scores (higher is better) for each source and reconstruction loss (lower is better) to the mixture m. We achieve better CLAP scores, maintaining low reconstruction loss, indicating better source separation than baselines, boosting mean/min/- max CLAP to the prompts from (0.18, 0.02, 0.27) → ( 0 . 2 ( + 0 . 0 2 ) , 0 . 0 5 ( + 0 . 0 3 ) , 0 . 3 4 ( + 0 . 1 0 ) )*

**物理冲击合成**展现了方法对结构化参数空间的优化能力。Figure 7追踪了不同提示下CLAP分数随优化步数的变化曲线。对于“kick drum, bass, reverb”提示，CLAP从随机初始化持续上升约+0.10；对于“hitting pot with wooden spoon”提示，提升幅度达+0.18。曲线呈单调上升趋势，未出现明显的过拟合或退化迹象，验证了SDS更新在物理参数空间中的稳定收敛性。

**FM合成**的结果则揭示了参数表达能力的瓶颈。对于域内提示“kick drum, bass, reverb”，FM合成器优化后CLAP提升+0.13；但对于更具挑战性的“hitting pot with wooden spoon”，CLAP仅提升+0.01（Figure 6）。这一对比表明，当目标声音超出FM合成器的表达能力时（如需要表现金属质感的木质锅敲击声），参数优化无法弥补模型容量的根本限制。


![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/007_Figure_6.jpg]]
*Figure 6: FM and Impact Synthesis: Qualitative Results. Spectrograms of the initialization and final result after optimization for two prompts. Takeaway: Outputs separate into distinct results according to prompts, reflecting quantitative results (Fig. 7, end of caption). FM Synthesis fits the “kick drum. . . ”, but fails for more challenging “hitting $\mathrm { p o t . . . } ^ { \mathsf { 7 } }$ . However, the more complex impact synthesis fits both. Audio links: init. FM, init. impact, final FM “kick drum, bass, reverb” (+0.13 CLAP vs. init.), final FM “hitting pot with wooden spoon” (+0.01 CLAP vs. init.) final impact “kick drum,. . . ” (+0.10 CLAP vs. init., −0.01 CLAP vs. FM), final impact “hittin...

### 消融实验

**Decoder-SDS vs. Encoder-SDS**（Figure 10）：在冲击合成任务中，Decoder-SDS相比直接通过编码器微分的Encoder-SDS在CLAP上取得**+0.15**的显著优势。这一结果直接验证了核心设计选择——避免编码器微分能够消除潜空间映射引入的数值不稳定性，是音频SDS稳定优化的关键。

**多步去噪 vs. 单步去噪**（Figure 12）：使用10步DDIM部分去噪相比标准单步去噪在冲击合成中CLAP提升**+0.14**。多步去噪提供了更平滑的引导信号，减少了单步去噪中噪声预测误差对参数更新的扰动。


![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/015_Figure_12.jpg]]
*Figure 12: Single-Step vs. Multi-Step Denoising We visualize spectrograms in dB of the audio initialization and the final result after optimization for our proposed multi-step denoising and the standard single-step denoising for impact synthesis with the prompt “hitting pot with wooden spoon”. Takeaway: The Decoder-SDS performs qualitatively and quantitatively better than the Encoder-SDS here. Audio links: single-step, 10-step (+0.14 CLAP vs. single-step)*

**频谱加权 vs. 时域L2损失**（Figure 11）：在源分离重建中，多尺度STFT幅度残差相比时域L2损失定性地保留了更多瞬态和高频细节。频谱加权通过在不同窗口大小上平均频率差异，避免了单一窗口带来的时间-频率分辨率权衡，对冲击类声音的瞬态保留尤为关键。


![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/014_Figure_11.jpg]]
*Figure 11: Spectrogram vs. $\ell _ { 2 }$ me Time (s) Emphasis: We visualize spectrograms (in dB) and waveforms of a target audio, and our reconstruction result using a spectrogram and $\ell _ { 2 }$ emphasis. Takeaway: The spectrogram emphasis is qualitatively better than the $\ell _ { 2 }$ emphasis. Audio links: target, $\ell _ { 2 }$ emphasis, spectrogram emphasis

### 失败模式与局限性

1. **分布外提示退化**：对于扩散模型训练分布之外的提示，优化输出可能退化为重复噪声或微弱伪影。这一问题在FM合成中尤为突出——当提示描述的声音超出合成器表达能力时，优化无法收敛到有意义的解。

2. **长音频尾部伪影**：源分离实验中，恢复伪影主要集中在音频末端。作者假设这与扩散模型偏好末尾静音有关，但缺乏直接的因果验证。这一现象在超过10-15秒的片段上更为明显。

3. **参数表达能力瓶颈**：FM合成器仅含4个振荡器，无法生成需要复杂谐波结构的声音（如金属撞击声）。物理冲击模型虽更灵活，但其阻尼正弦和参数化仍受限于特定声学假设。

4. **超参数敏感性**：训练过程对分类器自由引导（CFG）尺度、学习率和SDS更新权重γ敏感，需要针对不同提示进行调节。高CFG尺度可能导致不稳定和病理局部最小值。

5. **编码器压缩损失**：潜在编码器/解码器的压缩可能丢失精细瞬态信息，频谱加权虽部分缓解了这一问题，但无法完全恢复被编码器丢弃的高频细节。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/001_Figure.jpg]]
*Figure: (b) Audio-SDS Update (c) Audio-SDS Tasks*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2505_04621/figures/002_Table.jpg]]

## 方法谱系与知识库定位

### 1. 方法继承与谱系定位

Audio-SDS 的核心思想直接继承自 **Score Distillation Sampling (SDS)**（Poole et al., 2022），该方法最初为文本到3D生成而提出，通过将预训练扩散模型的评分函数作为蒸馏信号，引导可微分渲染器的参数优化，从而避免直接对扩散模型求导。Audio-SDS 将这一范式从图像/3D域迁移至音频域，但迁移过程并非简单复用——音频信号的时序特性、瞬态结构以及潜在编码器的不稳定性迫使方法做出三项关键改造。

在音频生成谱系中，Audio-SDS 的定位不同于主流的文本到音频扩散模型（如 AudioLDM、Stable Audio 等），后者聚焦于从噪声直接采样生成音频，而 Audio-SDS 关注的是**参数化音频表示的优化**：给定一个冻结的预训练扩散模型作为“语义评分器”，通过梯度下降调整可微渲染器参数，使生成的音频对齐文本描述。这一范式使得单一冻结模型能够统一处理多种音频任务，而无需任务特定的训练数据集。

### 2. 与基线方法的差异分析

论文通过消融实验系统对比了三类基线变体，揭示了 Audio-SDS 设计选择的关键性：

**Decoder-SDS vs. Encoder-SDS（朴素潜在SDS）**：标准SDS在潜在扩散模型中需要微分编码器 $\operatorname{enc}_\phi$ 以计算参数梯度。然而，实验表明，编码器的梯度路径在音频域引入显著不稳定性，导致优化发散或生成质量下降。Decoder-SDS 的核心创新在于将SDS更新从潜在空间移至解码后的音频域：先对渲染音频进行编码-加噪-去噪-解码，得到 $\hat{\mathbf{x}}_\phi$，再在音频波形空间计算残差 $\mathbb{E}[\hat{\mathbf{x}}_\phi] - \mathbf{x}(\theta)$，从而完全规避编码器微分。消融实验（Fig. 10）显示，在冲击合成任务中，Decoder-SDS 相比 Encoder-SDS 在 CLAP 分数上提升 **+0.15**，证实了编码器不稳定性是音频SDS的主要瓶颈。

**多尺度频谱加权 vs. 时间域L2损失**：标准SDS在像素/波形空间使用L2残差，但音频感知质量对瞬态和高频细节高度敏感。Audio-SDS 引入多尺度STFT幅度残差（Eq. 7），在多个窗口大小下计算频谱差异，从而避免时频分辨率权衡。消融实验（Fig. 11）定性地表明，频谱加权在瞬态保留和听觉质量上优于L2强调，尤其在源分离重建中表现更佳。

**多步去噪 vs. 单步去噪**：标准SDS仅使用单步去噪预测噪声，但音频波形对部分去噪的中间步骤更敏感。Audio-SDS 采用DDIM采样器执行2-10步部分去噪，提供更稳定的引导信号。消融实验（Fig. 12）显示，10步去噪相比单步在冲击合成中 CLAP 提升 **+0.14**，验证了多步去噪对收敛稳定性的贡献。

### 3. 适用边界与约束条件

Audio-SDS 的适用性受以下边界约束：

- **参数化表示的表达能力**：方法要求渲染函数 $g_\text{audio}(\theta)$ 可微分，且其表达能力决定了生成音频的上限。简单参数模型（如FM合成器）难以生成超出其设计空间的复杂声音——例如，FM合成器无法表现“木勺敲击金属锅”所需的金属质感（Fig. 6 中该提示仅获得 +0.01 CLAP），而更复杂的物理冲击模型（阻尼正弦和）则可获得 +0.18 CLAP。

- **提示分布内/外**：方法对分布外提示效果差，输出可能退化为重复噪声或微弱伪影。这一限制源于冻结扩散模型的评分信号仅在训练分布内可靠。

- **音频时长与复杂度**：较长音频（超过10-15秒）或复杂声景可能导致过渡生硬或部分静音。源分离实验中，多数恢复伪影出现在音频末端（Table 1），论文假设这是扩散模型偏好末尾静音所致。

- **超参数敏感性**：训练过程对超参数敏感，包括分类器自由引导（CFG）尺度、SDS更新权重 $\gamma$ 以及去噪步数，需要针对不同提示仔细调节。高CFG尺度可能导致不稳定和病理局部最小值。

### 4. 局限性与失效模式

除适用边界外，Audio-SDS 存在以下内在局限：

- **潜在编解码器的信息损失**：VAE编码器-解码器的压缩过程可能丢失精细瞬态信息，这构成了Decoder-SDS虽避免编码器梯度但无法完全恢复瞬态的根本限制。

- **欠定源分离的正则化依赖**：提示驱动源分离本质上是一个欠定问题（Eq. 11），分离质量高度依赖文本提示的语义区分度。当源成分语义重叠时，SDS正则化可能无法有效解耦。

- **负提示的缺失**：当前框架未探索负提示机制，无法显式排除特定背景成分，这限制了在复杂混合场景中的分离精度。

### 5. 开放问题与后续方向

论文提出以下待解决问题，构成潜在的后续研究方向：

- **自动提示生成**：在没有地面真值标签的情况下，如何自动为混合音频选择源分离提示？论文初步探索了音频描述模型+LLM的流水线（Fig. 9），但其鲁棒性和泛化性仍需验证。

- **参数化与潜在表示的融合**：如何将物理/FM合成参数化与潜在表示结合，以处理不同真实程度的声源？这涉及可解释性与表达能力的权衡。

- **动态音频场景扩展**：当前SDS处理静态音频片段，如何扩展到动态场景，建模移动声源和视角依赖的提示，是一个开放挑战。

- **层次化与调度策略**：如何提升罕见或极长音频片段上的保真度，可能需要层次化方法或更先进的噪声调度策略。

- **跨模态扩展**：能否将SDS与联合音视频扩散模型结合，实现视听共优化，是富有前景的方向。

**注意**：以上基线方法（Encoder-SDS、Single-step denoising、Time-domain L2 loss）均为论文内部消融变体，未提供外部引用元数据。如需补充与外部工作的详细对比，建议手动验证相关文献。

## 原文 PDF

![[paperPDFs/ICML_2025/Score_Distillation_Sampling_for_Audio_Source_Separation_Synthesis_and_Beyond.pdf]]

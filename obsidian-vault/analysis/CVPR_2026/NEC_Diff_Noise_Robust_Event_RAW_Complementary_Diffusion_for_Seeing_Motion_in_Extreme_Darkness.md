---
title: "NEC-Diff: Noise-Robust Event-RAW Complementary Diffusion for Seeing Motion in Extreme Darkness"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NEC_Diff_Noise_Robust_Event_RAW_Complementary_Diffusion_for_Seeing_Motion_in_Extreme_Darkness.pdf
project_link: null
code_link: "https://github.com/jinghan-xu/NEC-Diff"
aliases:
- ND
- NEC-Diff
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: RAW图像与事件之间的物理一致性关系（对数亮度变化约束）使得双模态相互指导去噪成为可能；基于去噪结果动态估计双模态SNR并据此自适应选择高可靠性特征，决定了融合信息的可信度。
primary_logic: 利用RAW图像的线性光响应特性与事件相机的亮度变化本质建立物理驱动的双模态协同去噪约束（强度一致性损失），同时基于去噪结果动态估计两模态的SNR来引导自适应特征融合，将高可靠性信息注入扩散模型实现高保真重建。
claims:
- 移除ECNS模块导致PSNR下降3.45 dB，验证了协同去噪的核心作用
- 双SNR引导融合相比直接融合提升0.76 dB PSNR，相比仅图像SNR引导融合提升0.43 dB
- NEC-Diff在LLRVD-simu上达到27.74 PSNR，在REAL上达到24.51 PSNR，显著超越所有对比方法
- 强度一致性损失有效约束去噪过程，保证双模态输出满足物理对数关系
---

# NEC-Diff: Noise-Robust Event-RAW Complementary Diffusion for Seeing Motion in Extreme Darkness

> [!tip] 核心洞察
> 利用RAW图像的线性光响应特性与事件相机的亮度变化本质建立物理驱动的双模态协同去噪约束（强度一致性损失），同时基于去噪结果动态估计两模态的SNR来引导自适应特征融合，将高可靠性信息注入扩散模型实现高保真重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | NEC-Diff：面向极端暗光运动成像的噪声鲁棒事件-RAW互补扩散模型 |
| 英文题名 | NEC-Diff: Noise-Robust Event-RAW Complementary Diffusion for Seeing Motion in Extreme Darkness |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20005) · [Code](https://github.com/jinghan-xu/NEC-Diff) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NEC-Diff |
| Dataset | LLRVD-simu, REAL |

> [!tip] 效果简介
> - LLRVD-simu 上，PSNR 27.74 vs SOTA（详见表1） (显著超越所有对比方法)；SSIM 0.828 vs SOTA（详见表1） (显著超越所有对比方法)；LPIPS 0.125 vs SOTA（详见表1） (显著低于所有对比方法)。
> - REAL 上，PSNR 24.51 vs SOTA（详见表1） (显著超越所有对比方法)；SSIM 0.742 vs SOTA（详见表1） (显著超越所有对比方法)。

## 概述

极端暗光条件下的运动成像面临一个根本性瓶颈：光子匮乏导致传统相机与事件相机同时遭受严重的传感器噪声，纹理保留与噪声抑制之间存在难以调和的权衡。现有低光增强方法要么过度平滑导致纹理丢失，要么残存噪声破坏结构；而事件相机虽然在暗光区域能提供高动态纹理信息，但其自身在低光照下也会产生密集的散粒噪声——密度可比其他噪声高出50倍以上。现有的事件-图像融合方法未能对两种模态同时进行精准去噪，往往顾此失彼。

NEC-Diff 针对这一瓶颈提出了三个层面的创新。首先，利用 RAW 图像的线性光响应特性与事件相机的亮度变化本质，建立了**物理驱动的双模态协同去噪约束**：RAW 图像提供照明先验指导事件去噪，去噪后的事件高动态边缘信息再辅助图像去噪，并通过强度一致性损失确保两者满足对数亮度变化关系。其次，基于去噪结果动态估计图像与事件双模态的信噪比（SNR），通过 **SNR 引导的自适应特征选择**，将高可靠性信息注入后续重建过程，有效抑制噪声主导区域。最后，以双模态融合特征为条件的**扩散模型**通过 DDIM 确定性采样完成高保真重建，在极端暗光下展现出更强的鲁棒性和细节保真度。

在定量评估中，NEC-Diff 在 LLRVD-simu 数据集上达到 27.74 dB PSNR，在 REAL 真实暗光数据集上达到 24.51 dB PSNR，显著超越所有对比方法。消融实验进一步验证了各模块的关键作用：移除事件-RAW 协同去噪模块（ECNS）导致 PSNR 下降 3.45 dB；双 SNR 引导融合相比直接融合提升 0.76 dB PSNR，相比仅图像 SNR 引导融合提升 0.43 dB。

**方法定位**：NEC-Diff 属于事件-RAW 互补融合的暗光增强方法，以物理一致性约束驱动双模态协同去噪，以 SNR 自适应机制引导可靠信息提取，以扩散模型实现高质量重建。其核心区别于现有工作之处在于：（1）采用 RAW 而非 sRGB 作为图像输入，保留了线性光响应和更易建模的噪声分布；（2）同时建模图像与事件双模态 SNR，而非仅依赖图像 SNR 进行融合；（3）引入基于物理对数关系的强度一致性损失，约束去噪过程。

**局限性**：扩散模型的迭代采样增加了推理计算开销，可能限制实时应用；方法依赖像素对齐的 RAW-事件配对数据，此类同轴多传感器采集系统搭建门槛较高；事件对比度阈值在不同场景下的变化如何自适应处理，尚待进一步研究。

## 背景与动机

### 极端暗光成像的根本困境

在光照低于0.1 lux的极端暗光条件下，传统CMOS相机面临光子匮乏的物理极限：传感器捕获的光电子数急剧减少，光子散粒噪声、读出噪声和量化噪声在信号中的占比急剧攀升。这一困境的数学本质可由RAW图像噪声模型刻画：

$$R = K I + K N_p + N_{\mathrm{read}} + N_d$$

其中像素值$R$等于增益$K$乘以光电子数$I$，叠加光子散粒噪声$N_p$、读出噪声$N_{\mathrm{read}}$和量化噪声$N_d$。当光电子数$I$极小时，噪声项主导了像素值，导致图像信噪比崩塌。

现有的低光图像增强（LLIE）方法在此条件下陷入一个根本性权衡：**纹理保留与噪声抑制无法兼得**。如图1(a)所示，传统增强方法要么过度平滑导致纹理细节丢失，要么残留密集噪声破坏结构完整性。这一瓶颈的根源在于，单帧RAW图像在极端暗光下携带的场景信息已严重退化，仅凭图像模态自身难以区分信号与噪声。

### 事件相机的潜力与挑战

事件相机以异步方式感知亮度变化的对数差异，其理想观测模型为：

$$E(t) = \frac{1}{C} \log \frac{I(t) + b_{pr}}{I(t - \Delta t) + b_{pr}}$$

其中$C$为对比度阈值，$b_{pr}$为感光器偏置项。事件相机具备微秒级时间分辨率和高动态范围，理论上能在暗光中捕获运动纹理的边缘信息，弥补传统相机的纹理丢失问题。

然而，在极端暗光条件下，事件相机同样遭受严重的噪声污染。图3揭示了一个关键现象：**事件噪声密度与光照强度呈正相关**——在较亮区域，事件噪声密度显著增加。定量分析表明，低光照下事件数据中的散粒噪声密度比其他噪声类型高出50倍以上。这意味着，直接将噪声事件引入增强流程不仅无法补充纹理，反而会引入额外的噪声干扰。

### 现有方法的缺口

现有事件-图像融合方法存在三个系统性缺陷：

1. **噪声处理策略单一**：大多数方法采用低通滤波或独立事件去噪网络（如**ELEDNet**（Kim et al., ECCV 2024）中的事件滤波），但这类策略在抑制噪声的同时不可避免地抹除弱信号，难以在光子匮乏条件下保留有价值的结构信息。

2. **输入数据类型的局限**：主流方法（如**LightenDiffusion**（Jiang et al., ECCV 2024）、**EvLowLight**（Liang et al., ICCV 2023））以经ISP非线性处理后的sRGB图像为输入，丢失了RAW域的线性光响应特性和可建模的噪声分布，增加了去噪难度。

3. **融合机制缺乏可靠性感知**：现有融合策略（如**EvLight**（Liang et al., CVPR 2024）的SNR引导增强）仅考虑图像模态的信噪比，忽略了事件模态在不同空间区域的SNR差异。图4的分析表明，在暗光纹理丰富区域，事件SNR高于图像SNR；而在平滑区域，事件SNR趋近于零。忽略这一互补特性会导致信息提取的次优。

### 本文的核心动机

上述分析揭示了两个关键洞察：

- **物理一致性关系**：RAW图像与事件之间存在固有的对数亮度变化约束——理想事件流可用无噪声RAW信号表示为$\tilde{E}(t) = \frac{1}{C} \log \frac{\tilde{R}(t)}{\tilde{R}(t - \Delta t)}$。这一物理关系使得双模态相互指导去噪成为可能。

- **SNR互补性**：图像和事件在暗光场景的不同区域呈现互补的SNR分布，为自适应选择高可靠性特征提供了依据。

基于此，本文提出**NEC-Diff**框架，核心动机是：利用RAW图像的线性光响应特性与事件相机的亮度变化本质，建立物理驱动的双模态协同去噪约束；同时基于去噪结果动态估计两模态的SNR，引导自适应特征融合，将高可靠性信息注入扩散模型实现高保真重建。这一设计旨在从根本上突破暗光成像中纹理保留与噪声抑制的权衡瓶颈。

## 核心创新

NEC-Diff 的核心创新围绕一个根本性瓶颈展开：在光子匮乏的极端暗光条件下，RAW 图像与事件相机同时遭受严重的传感器噪声，而现有方法无法对两种模态进行有效的协同去噪与可信融合。基于此，NEC-Diff 在输入选择、噪声处理策略、融合机制、重建骨干和物理约束五个关键维度上做出了系统性改进。

### 1. 从 sRGB 到 RAW 的输入空间转换

传统低光增强方法（如 **LightenDiffusion**，Jiang et al., ECCV 2024）以经 ISP 非线性处理后的 sRGB 图像为输入，噪声分布复杂且难以精确建模。NEC-Diff 直接采用 **RAW 图像**作为输入，保留传感器的线性光响应特性，使噪声分布（光子散粒噪声、读出噪声、量化噪声）更易建模，同时保留更丰富的场景信息。这一输入空间的转换是后续物理约束能够建立的前提。

### 2. 从独立滤波到跨模态协同去噪

事件相机在低光照下的噪声问题远比图像模态严重：事件噪声密度与光照强度呈正相关，在极暗区域噪声密度可达信号事件的 50 倍以上。现有方法（如 **ELEDNet**，Kim et al., ECCV 2024）通常采用低通滤波或独立事件去噪网络，难以在抑制噪声的同时保留微弱的纹理信号。

NEC-Diff 的 **事件-RAW 协同噪声抑制（ECNS）** 模块提出了一种**双向互指导**的去噪策略：
- **RAW 指导事件去噪**：利用 RAW 图像提供的照明先验，识别事件流中的低光照区域，指导事件去噪网络精准区分噪声事件与信号事件；
- **事件辅助图像去噪**：利用去噪后事件保留的高动态边缘信息，辅助 RAW 图像在纹理区域的去噪，缓解传统方法中纹理丢失与噪声抑制之间的根本性权衡。

这一协同机制由**强度一致性损失**（Intensity Consistency Loss）进行物理约束，确保去噪后的 RAW 帧与事件流之间满足对数亮度变化关系：
$$\mathcal{L}_{\mathrm{cons}} = \left\| \hat{E}(t) \cdot C - \log \frac{\hat{R}(t) + \epsilon}{\hat{R}(t - \Delta t) + \epsilon} \right\|_1$$

消融实验验证了该模块的核心作用：**移除 ECNS 模块导致 PSNR 下降 3.45 dB**（Table 2），强度一致性损失使训练中重建损失更低、生成纹理更精细（Figure 7b）。

### 3. 从单模态 SNR 到双模态 SNR 引导融合

现有事件-图像融合方法（如 **EvLight**，Liang et al., CVPR 2024）通常仅基于图像 SNR 进行加权，忽略了事件模态自身的信噪比变化。NEC-Diff 通过分析发现，两模态的 SNR 在空间上呈现互补分布：在暗纹理区域，事件 SNR 高于图像 SNR；在平滑区域，事件 SNR 趋近于零（Figure 4）。

基于这一洞察，NEC-Diff 的 **SNR 引导可靠信息提取（SRIE）** 模块同时建模图像与事件的双模态 SNR：
$$M_{\mathrm{SNR}} = 10 \cdot \log \frac{M_{\mathrm{in}}^2}{(M_{\mathrm{in}} - M_{\mathrm{den}})^2 + \epsilon}$$

利用去噪输出动态估计每个空间位置的信噪比，通过轻量网络生成空间权重图，自适应增强高 SNR 区域特征、抑制噪声主导区域。消融实验表明，**双 SNR 引导融合相比直接融合提升 0.76 dB PSNR，相比仅图像 SNR 引导融合提升 0.43 dB PSNR**（Figure 8）。

### 4. 从 CNN 直接映射到扩散模型条件生成

传统方法多采用 CNN/UNet 直接映射进行重建，在极端暗光下容易产生过度平滑或伪影。NEC-Diff 的 **跨模态注意力扩散（CAD）** 模块通过双向交叉注意力融合加权后的图像和事件特征，并将其作为条件注入扩散模型，通过 DDIM 确定性采样完成高质量重建。扩散模型的生成能力为极端条件下的细节保真度提供了更强的鲁棒性。

### 5. 从纯重建损失到物理约束多目标优化

NEC-Diff 将优化目标从单一的 L1/L2 重建损失扩展为多目标联合优化：
$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{grad}} \mathcal{L}_{\mathrm{grad}} + \lambda_{\mathrm{cons}} \mathcal{L}_{\mathrm{cons}}$$

其中梯度保持损失 $\mathcal{L}_{\mathrm{grad}}$ 保留纹理结构，强度一致性损失 $\mathcal{L}_{\mathrm{cons}}$ 约束双模态输出的物理一致性（$\lambda_{\mathrm{grad}}=10$，$\lambda_{\mathrm{cons}}=0.5$）。这一物理驱动的约束体系是 NEC-Diff 在极端暗光下实现高保真重建的关键保证。

## 整体框架

NEC-Diff 的整体 pipeline 围绕一个核心洞察展开：在极端暗光条件下，RAW 图像与事件流在噪声分布和信号可靠性上具有天然的互补性——RAW 图像在亮区 SNR 高但暗区纹理丢失严重，事件流在暗纹理区域 SNR 高但在平滑区域噪声密度急剧上升（可达其他区域的 50 倍以上）。基于此，NEC-Diff 构建了三个紧密协作的模块，形成“协同去噪 → 可靠性感知特征提取 → 条件扩散重建”的信息流。

**输入输出流**：系统接收一对时空对齐的噪声 RAW 图像和对应的事件流，输出高保真、纹理清晰的增强图像。RAW 图像保留了线性光响应特性（未经过 ISP 非线性处理），使噪声分布更易建模；事件流以稀疏异步形式记录了场景的亮度变化信息。两者首先进入 **Event-RAW Collaborative Noise Suppression (ECNS)** 模块进行跨模态协同去噪，随后由 **SNR-Guided Reliable Information Extraction (SRIE)** 模块基于去噪结果动态估计双模态 SNR 并自适应提取高可靠性特征，最终通过 **Cross-Modal Attentive Diffusion (CAD)** 模块以双向交叉注意力融合加权特征，注入扩散模型通过 DDIM 确定性采样完成重建（Figure 2）。

**模块间的因果依赖关系**：ECNS 是 pipeline 的根基——消融实验表明，移除该模块直接导致 PSNR 下降 3.45 dB（Table 2），验证了协同去噪在整个框架中的决定性作用。ECNS 的去噪质量直接影响 SRIE 中 SNR 估计的准确性：SNR 图由原始输入与去噪输出之差计算得到（见公式 $M_{\mathrm{SNR}} = 10 \cdot \log \frac{M_{\mathrm{in}}^2}{(M_{\mathrm{in}} - M_{\mathrm{den}})^2 + \epsilon}$），若去噪不充分，SNR 估计将失准，导致后续特征加权错误地增强噪声区域或抑制有效信号。SRIE 输出的加权特征则作为 CAD 中扩散模型的条件输入——特征质量直接决定重建的上限。这种流水线式的因果链使得任一模块的失效都会级联放大最终误差，但也正是这种紧密耦合设计使得三个模块能形成正向协同：ECNS 提供干净的双模态信号 → SRIE 精准识别高 SNR 区域 → CAD 在可靠条件的引导下生成高保真结果。

**物理约束的贯穿性作用**：强度一致性损失 $\mathcal{L}_{\mathrm{cons}}$ 并非仅作用于 ECNS 模块内部，而是对整个 pipeline 施加全局物理约束。该损失基于 RAW 与事件之间的对数亮度变化关系（$\mathcal{L}_{\mathrm{cons}} = \left\| \hat{E}(t) \cdot C - \log \frac{\hat{R}(t) + \epsilon}{\hat{R}(t - \Delta t) + \epsilon} \right\|_1$），要求去噪后的事件流 $\hat{E}(t)$ 与去噪后的 RAW 帧 $\hat{R}(t)$ 之间满足物理一致性。这一约束在训练中同时反传梯度至 ECNS 和后续的特征提取网络，确保整个 pipeline 的输出不仅视觉质量高，而且在物理上是自洽的——这从根本上区别于仅依赖像素级重建损失的现有方法。实验证据表明，该损失使训练中重建损失更低，生成纹理更精细（Figure 7b）。

**与现有方法在 pipeline 层面的本质差异**：现有事件-图像融合方法（如 **EvLight**（Liang et al., CVPR 2024）、**ELEDNet**（Kim et al., ECCV 2024））通常采用“各自独立去噪 → 直接特征拼接”的串行策略，忽略了两种模态在去噪过程中的相互指导潜力，且融合时仅依赖图像单模态 SNR 或简单拼接，未对事件模态的信号可靠性进行动态建模。NEC-Diff 的关键突破在于将“协同去噪”和“双模态 SNR 引导融合”系统性地嵌入同一框架：ECNS 实现了去噪阶段的跨模态信息交互（RAW 照明先验指导事件去噪，事件高动态边缘辅助图像去噪），SRIE 则在特征提取阶段同时建模两模态 SNR 并动态选择高置信度信息。这种“去噪即融合、融合即选择”的设计，使得 pipeline 能在极端暗光（<0.3 lux，占 REAL 数据集约 70% 场景）下同时实现噪声抑制和纹理保持，避免了现有方法的纹理-噪声权衡困境。

### 补充图表

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of NEC-diff includes an Event-RAW Collaborative Noise Suppression (ECNS), a SNR-Guided Reliable Information Extraction (SRIE), and a Cross-Modal Attentive Diffusion (CAD). The ECNS jointly exploits illumination priors from RAW images and texture cues from events for cross-modal denoising. The SRIE adaptively selects high-SNR features from both modalities. The CAD integrates reliable features via cross-modal attention into a diffusion model for high-quality reconstruction*

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of problem and main idea. (a) LLIE methods suffer from a trade-off between texture preservation and noise suppression. (b) Events effectively complement textures but introduce additional noise. NEC-Diff exploits the characteristics of both events and RAW images to achieve robust denoising while preserving textures, fusing features guided by SNR and injecting them into the diffusion model to achieve high-fidelity results*

## 核心模块与公式推导

### 3.1 噪声建模与物理一致性约束

在极端暗光条件下，RAW图像与事件相机分别遵循不同的噪声生成机制，理解二者的物理关系是协同去噪的基础。

**RAW图像噪声模型**：RAW像素值 $R$ 由增益 $K$、光电子数 $I$ 及多源噪声叠加构成：

$$R = K I + K N_p + N_{\mathrm{read}} + N_d$$

其中 $N_p$ 为光子散粒噪声，$N_{\mathrm{read}}$ 为读出噪声，$N_d$ 为量化噪声。RAW图像保留线性光响应，其噪声分布比经ISP非线性处理后的sRGB图像更易建模，这是本文采用RAW而非sRGB作为输入的关键原因。

**事件流观测模型**：事件相机在像素亮度变化超过对比度阈值 $C$ 时触发事件，其理想观测模型为：

$$E(t) = \frac{1}{C} \log \frac{I(t) + b_{pr}}{I(t - \Delta t) + b_{pr}}$$

其中 $b_{pr}$ 为感光器偏置项。理想事件生成条件为：

$$\log I(x, y, t) - \log I(x, y, t - \Delta t) = p C$$

即对数光强变化等于极性 $p$ 乘以阈值 $C$。

**RAW-事件物理对应关系**：将理想事件流用无噪声RAW信号 $\tilde{R}$ 表示，可建立双模态的物理桥梁：

$$\tilde{E}(t) = \frac{1}{C} \log \frac{K I(t)}{K I(t - \Delta t)} = \frac{1}{C} \log \frac{\tilde{R}(t)}{\tilde{R}(t - \Delta t)}$$

该关系揭示了一个核心洞察：**干净RAW帧与对应事件流之间存在由对数亮度变化约束的确定性物理关系**，这为双模态相互指导去噪提供了理论依据。

### 3.2 事件噪声密度与光照的相关性

实验观测揭示了低光照下事件噪声的关键特性（Figure 3）：**事件噪声密度与光照强度呈正相关**——在较亮区域，背景活动噪声密集；在极暗区域，噪声反而稀疏。这一反直觉现象的成因在于事件相机依赖光电流触发，光子匮乏时基底噪声不足以频繁跨越阈值。统计表明，在低光照条件下，事件噪声密度可比其他噪声源高50倍以上。

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/003_Figure_3.jpg]]
*Figure 3: Correlation between event noise density and illumination under low-light conditions. (a) Denoised RAW image indicating illumination intensity across different regions. (b) Event noise density under varying illumination levels. (c) Statistical analysis of event noise density across regions of the gray card*

基于此，ECNS模块采用**光照引导的事件去噪**策略：利用RAW图像提供的照明先验指导事件去噪过程——在亮度较高区域施加更强的事件噪声抑制，在暗区则保留弱信号。随后，**事件辅助的图像去噪**利用去噪后事件的高动态边缘信息指导图像纹理恢复，形成双向互补的去噪循环。

### 3.3 强度一致性损失

为确保双模态去噪输出满足物理对数关系，引入强度一致性损失：

$$\mathcal{L}_{\mathrm{cons}} = \left\| \hat{E}(t) \cdot C - \log \frac{\hat{R}(t) + \epsilon}{\hat{R}(t - \Delta t) + \epsilon} \right\|_1$$

其中 $\hat{E}(t)$ 和 $\hat{R}(t)$ 分别为去噪后的事件流和RAW帧，$C$ 为可学习的缩放因子，$\epsilon$ 为防止除零的小常数。该损失以L1范数约束去噪结果满足对数亮度变化关系，使双模态输出在物理层面保持一致，有效避免去噪过程中的伪影引入（Figure 7b验证了该损失使训练中重建损失更低、生成纹理更精细）。

### 3.4 SNR引导的可靠信息提取

在去噪完成后，如何从双模态中筛选高质量信息进行融合是关键问题。Figure 4揭示了双模态SNR的互补特性：**在暗区纹理丰富区域，事件SNR高于图像SNR；在平滑区域，事件SNR趋近于零**。这启发SRIE模块同时建模两模态的信号可靠性。

**SNR图计算**：利用原始输入 $M_{\mathrm{in}}$ 与去噪结果 $M_{\mathrm{den}}$ 逐像素计算信噪比：

$$M_{\mathrm{SNR}} = 10 \cdot \log \frac{M_{\mathrm{in}}^2}{(M_{\mathrm{in}} - M_{\mathrm{den}})^2 + \epsilon}$$

该公式以dB为单位量化每个空间位置的信号可信度：去噪前后差异大的区域（噪声主导）获得低SNR，差异小的区域（信号主导）获得高SNR。

**SNR引导的特征加权**：通过轻量网络从SNR图生成空间权重图 $\mathcal{W}$，逐元素调制对应模态特征：

$$\mathcal{F}_{\mathrm{img-w}} = \mathcal{F}_{\mathrm{img}} \odot \mathcal{W}_{\mathrm{img}}, \quad \mathcal{F}_{\mathrm{evt-w}} = \mathcal{F}_{\mathrm{evt}} \odot \mathcal{W}_{\mathrm{evt}}$$

该机制实现了**动态模态选择**：在图像SNR高的区域增强图像特征权重，在事件SNR高的区域增强事件特征权重，噪声主导区域则被抑制。消融实验表明（Figure 8），双SNR引导融合相比直接融合提升0.76 dB PSNR，相比仅图像SNR引导融合提升0.43 dB PSNR，验证了双模态SNR联合建模的必要性。

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/011_Figure_8.jpg]]
*Figure 8: Effectiveness of SNR-guided fusion. Compared with (a) direct fusion and (b) image SNR-guided fusion, (c) dual SNRguided fusion achieves the best performance*

### 3.5 交叉模态注意力扩散重建

加权后的双模态特征通过**双向交叉注意力**实现深度融合。以图像特征为Query、事件特征为Key/Value计算事件注意力，反之亦然：

$$A_E = \mathrm{Softmax}\left(\frac{Q_I K_E^\top}{\sqrt{d}}\right) V_E, \quad A_I = \mathrm{Softmax}\left(\frac{Q_E K_I^\top}{\sqrt{d}}\right) V_I$$

其中 $d$ 为特征维度。该设计使图像特征能够查询事件中的运动纹理信息，事件特征能够查询图像中的光照结构信息，实现双向信息互补。

融合特征 $F_{\mathrm{fused}}$ 作为条件注入扩散模型，在时间步 $t$ 预测噪声：

$$\hat{\epsilon}_\theta = \epsilon_\theta(x_t, F_{\mathrm{fused}}, t)$$

最终通过DDIM确定性采样从纯噪声逐步重建清晰图像：

$$\boldsymbol{x}_{t-1} = \mathrm{DDIM}(\boldsymbol{x}_t, \hat{\boldsymbol{\epsilon}}_{\boldsymbol{\theta}}, \alpha_t)$$

扩散模型的迭代生成能力为极端暗光条件下的高保真重建提供了强鲁棒性，有效避免了直接映射方法常见的过平滑或噪声残留问题。

### 3.6 总体优化目标

完整训练目标由三项损失加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{grad}} \mathcal{L}_{\mathrm{grad}} + \lambda_{\mathrm{cons}} \mathcal{L}_{\mathrm{cons}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为重建损失，$\mathcal{L}_{\mathrm{grad}}$ 为梯度保持损失（保护边缘结构），$\mathcal{L}_{\mathrm{cons}}$ 为前述强度一致性损失。超参数设定为 $\lambda_{\mathrm{grad}}=10$，$\lambda_{\mathrm{cons}}=0.5$，平衡各损失项的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/004_Figure_4.jpg]]
*Figure 4: SNR Comparison between RAW and Event Modalities. (a) and (c) show the visualizations of the RAW image and events, while (b) and (d) present their SNR maps. (e) compares the SNR of the image and events across different regions. It can be observed that in dark regions with rich textures, the event SNR is higher, whereas in smooth areas, the event SNR approaches zero*

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/010_Figure_7.jpg]]
*Figure 7: Effectiveness of ECNS. (a) ECNS effectively enhances the quality of reconstructed details. (b) Effects of cooperative denoising and consistency loss*

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/008_Figure.jpg]]
*Figure: (a) Direct fusion (b) Image SNR-guided Fusion (c) Dual SNR-guided Fusion*

## 实验与分析

### 主实验结果

NEC-Diff在两个数据集上对全部指标均取得最优，且优势幅度显著。在LLRVD-simu数据集上，NEC-Diff达到**27.74 dB PSNR**、**0.828 SSIM**和**0.125 LPIPS**；在REAL数据集上，NEC-Diff达到**24.51 dB PSNR**和**0.742 SSIM**，在三个指标上均全面超越所有对比方法（Table 1）。REAL数据集的参考图像平均比RAW输入亮300×至500×，且约70%的场景照度低于0.3 lux，验证了方法在真实极端暗光条件下的有效性。

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison on LLRVD and REAL datasets*

从对比方法的覆盖范围来看，NEC-Diff同时超越了以下代表性工作的性能上限：
- 基于扩散模型的低光增强方法 **LightenDiffusion**（Jiang et al., ECCV 2024）
- 事件相机夜间图像重建方法 **NER-Net**（Liu et al., CVPR 2024）
- 事件引导低光增强方法 **EvLowLight**（Liang et al., ICCV 2023）、**EvLight**（Liang et al., CVPR 2024）、**ELEDNet**（Kim et al., ECCV 2024）
- 事件-RAW混合重建方法 **EvRAW**（Zheng et al., ACM Multimedia 2025）
- 基于事件照明估计的方法 **RETINEV**（Sun et al., arXiv 2025）

可视化对比（Figure 6）进一步表明，NEC-Diff在亮度均衡性和边缘锐度方面均展现出明显的多维视觉质量优势，有效解决了现有方法中纹理保留与噪声抑制之间的根本性权衡。

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/006_Figure_6.jpg]]
*Figure 6: Visual comparison between other SOTA methods and the proposed NEC-diff across different datasets*

### 消融实验

Table 2报告了REAL数据集上各模块的消融结果，揭示了以下关键因果链：

**ECNS模块的核心作用。** 移除Event-RAW Collaborative Noise Suppression模块导致PSNR下降**3.45 dB**，这是所有消融项中降幅最大的，直接验证了双模态协同去噪在整个框架中的决定性地位。ECNS通过RAW照明先验指导事件去噪、去噪后事件的高动态边缘辅助图像去噪的双向机制，实现了单一模态去噪无法达到的效果。

**双SNR引导融合的增益。** Figure 8定量比较了三种融合策略：(a) 直接融合、(b) 仅图像SNR引导融合、(c) 双SNR引导融合。双SNR引导融合相比直接融合提升**0.76 dB PSNR**，相比仅图像SNR引导融合提升**0.43 dB PSNR**。这一结果表明，事件模态SNR的建模并非冗余——在暗纹理区域事件SNR更高，而在平滑区域事件SNR趋近于零（Figure 4），仅依赖图像SNR会丢失事件模态提供的关键纹理信息。

**强度一致性损失的约束效果。** Figure 7(b)展示了协同去噪与一致性损失的效果：引入强度一致性损失后，训练过程中的重建损失更低，生成纹理更精细。该损失直接约束去噪后事件Ê(t)与去噪后RAW帧R̂(t)之间满足对数亮度变化关系，从物理层面保证了双模态输出的互洽性。

**扩散模型骨干的贡献。** 将扩散模型替换为CNN/UNet直接映射会导致性能下降，扩散模型的迭代去噪过程为极端暗光下的高保真重建提供了更强的鲁棒性和细节保真度。

### 泛化性验证

在未见夜间动态场景中，NEC-Diff在不同光照水平下的NIQE分数一致优于所有竞争者（Figure 9(b)），表明方法具有良好的跨场景泛化能力。REAL数据集覆盖0.01–0.8 lux照度范围，但极端条件（<0.001 lux）下的性能边界尚未充分验证，这是当前方法的一个已知局限。

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/012_Figure_9.jpg]]
*Figure 9: (a) Visual comparisons and (b) quantitative results in dynamic scenes under extremely low-light nighttime conditions*

### 失败模式与局限性

1. **事件对比度阈值敏感性。** 事件对比度阈值C在不同实际应用场景中可能变化，当前方法未自适应处理变化的阈值，这可能影响噪声抑制精度和跨相机泛化能力。
2. **推理效率。** 扩散模型的迭代DDIM采样过程增加了推理计算开销，可能限制实时应用场景的部署。
3. **数据依赖。** 方法依赖像素对齐的RAW-事件配对数据，此类同轴多传感器采集系统的搭建门槛较高，限制了方法的可复现性和数据扩展性。

### 补充图表

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/009_Table_2.jpg]]
*Table 2: Ablation study of each module on the REAL dataset*

![[assets/figures/papers/paper_list_l904_https_arxiv_org_abs_2603_20005/figures/005_Figure_5.jpg]]
*Figure 5: Details of the REAL dataset. (a) Hardware setup of the coaxial imaging system. (b) Distributions of image-pair brightness and platform motion speed. (c) Visualization of representative data pairs*

## 方法谱系与知识库定位

### 与基线方法的关系

NEC-Diff 处于**极端暗光运动成像**这一交叉问题空间，其设计同时回应了低光图像增强（LLIE）、事件相机重建和事件-图像融合三条技术路线的既有瓶颈。

**与低光增强方法的对比。** 传统LLIE方法（如基于Retinex分解或端到端CNN的方案）以sRGB图像为输入，但ISP非线性处理会扭曲噪声分布，使去噪与纹理保留之间陷入根本性权衡。**LightenDiffusion**（Jiang et al., ECCV 2024）虽引入扩散模型提升细节生成能力，但仍工作于sRGB域，无法规避ISP带来的信息损失。NEC-Diff的关键分歧点在于**直接以RAW图像为输入**——RAW保留线性光响应，噪声分布更易建模，同时为后续事件-图像物理一致性约束提供了数学基础。

**与事件相机重建方法的对比。** 事件相机在暗光下同样遭受严重传感器噪声：**Figure 3** 的统计分析表明，事件噪声密度与光照强度呈正相关，且噪声事件密度可比有效信号事件密度高50倍以上。**NER-Net**（Liu et al., CVPR 2024）等夜间事件重建方法通常依赖低通滤波或独立事件去噪网络，难以在抑制密集散粒噪声的同时保留弱信号边缘。NEC-Diff的差异在于**利用RAW图像提供的照明先验指导事件去噪**——RAW帧的亮度分布指示了场景中哪些区域的事件更可能是噪声主导，从而使事件去噪过程具备场景自适应性。

**与事件-图像融合方法的对比。** 现有融合方法在信息提取策略上存在明显局限：**EvLowLight**（Liang et al., ICCV 2023）依赖运动一致性进行事件引导增强，**EvLight**（Liang et al., CVPR 2024）仅基于图像SNR进行加权，**ELEDNet**（Kim et al., ECCV 2024）虽引入事件滤波但融合机制仍为直接拼接。这些方法共同忽略了**事件模态自身的SNR变化**——**Figure 4** 的实证分析揭示，在暗光纹理丰富区域事件SNR高于图像SNR，而在平滑区域事件SNR趋近于零。NEC-Diff的SRIE模块通过同时对图像和事件建模SNR图，动态选择高置信度模态的特征进行加权融合，相比仅图像SNR引导融合提升0.43 dB PSNR（**Figure 8**）。

**与事件-RAW混合方法的对比。** **EvRAW**（Zheng et al., ACM Multimedia 2025）同样采用事件-RAW混合输入，但其关注点在于细节与颜色恢复，缺乏物理驱动的协同去噪机制。NEC-Diff的核心区分在于**强度一致性损失**——该损失直接约束去噪后事件流与去噪后RAW帧之间满足对数亮度变化关系（Equation 5），使双模态去噪过程在物理层面相互制约，而非独立处理后再融合。

### 适用边界

NEC-Diff的有效性建立在以下几个前提之上，这些前提同时划定了其适用边界：

1. **像素对齐的RAW-事件配对数据可用。** 方法依赖同轴多传感器成像系统（如**Figure 5(a)** 所示的光学衰减同轴采集平台）获取严格对齐的训练数据。这类系统的搭建门槛较高，限制了方法在缺乏专用硬件场景下的直接迁移。

2. **光照条件处于可探测阈值之上。** REAL数据集覆盖0.01–0.8 lux范围（约70%场景低于0.3 lux），参考图像比RAW输入亮300×至500×。在低于0.001 lux的极端条件下，光子匮乏可能导致RAW和事件双模态同时丧失有效信号，协同去噪的物理约束可能退化为噪声-噪声匹配，性能边界尚未充分验证。

3. **运动速度在事件相机响应带宽内。** 事件相机产生事件的速率受限于对比度阈值C和光强变化速率。在高速旋转或剧烈振动场景下，事件与RAW帧的时间对齐误差可能增大，进而影响强度一致性损失的约束精度。

4. **事件对比度阈值C保持稳定。** 强度一致性损失依赖于C值将事件流与对数亮度变化关联。不同事件相机型号或同一相机在不同偏置设置下C值可能变化，方法当前未包含对C的自适应估计机制。

### 局限与开放问题

**已识别的局限。** 消融实验（**Table 2**）表明ECNS模块移除后PSNR下降3.45 dB，验证了协同去噪的核心作用，但扩散模型的迭代DDIM采样过程增加了推理计算开销，可能限制实时应用场景（如自动驾驶中的低延迟视频处理）。此外，强度一致性损失中C被设为可学习参数（Equation 5），但其在不同场景下的泛化行为未做系统消融。

**开放问题。** 以下方向值得后续工作关注：

- **无配对数据训练。** 在没有像素对齐的RAW-事件配对数据的情况下，能否通过物理仿真或自监督方式（如利用理想事件生成条件Equation 4构造伪标签）训练类似的协同去噪框架？
- **阈值无关的物理约束。** 事件对比度阈值C在不同相机型号和设置下的变化规律如何？能否设计对C不敏感的强度一致性约束（如基于相对排序而非精确对数比值）？
- **轻量化生成骨干。** 扩散模型能否替换为一致性模型或蒸馏扩散模型，在保持高保真重建的同时满足实时视频处理需求？
- **极端运动下的鲁棒性。** 在高速运动场景中，事件与RAW的时间对齐误差如何定量影响去噪和融合质量？能否通过引入事件时间戳引导的可变形对齐来缓解？
- **物理约束的跨模态推广。** ECNS的协同去噪范式——利用一种模态的物理先验指导另一种模态去噪——能否推广到其他多模态成像场景（如红外-可见光融合去噪、深度-彩色联合去噪）？

*注：部分开放问题（如低于0.001 lux的性能边界、C值的跨相机变化规律）未在原论文中提供实验证据，需要后续研究手动验证。*

## 原文 PDF

![[paperPDFs/CVPR_2026/NEC_Diff_Noise_Robust_Event_RAW_Complementary_Diffusion_for_Seeing_Motion_in_Extreme_Darkness.pdf]]

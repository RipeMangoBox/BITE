---
title: Accelerating Autoregressive Video Diffusion via History-Guided Cache and Residual Correction
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Accelerating_Autoregressive_Video_Diffusion_via_History_Guided_Cache_and_Residual_Correction.pdf
project_link: null
code_link: null
aliases:
- AAVDHGCRC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: ① 历史令牌（history tokens）的变化与模型输出的变化之间存在强相关性，可用于可靠地决定缓存刷新时机；② 未加速的首段残差轨迹在不同段落间高度一致且稳定，可作为清洁参考来矫正加速导致的残差漂移。
primary_logic: 通过监控历史令牌而非全局输入来调度缓存（HGC），更准确地抑制段内近似误差；利用首段的清洁残差轨迹参数替换后续段落的轨迹参数进行残差校正（ERC），以几乎可忽略的计算开销阻断误差跨段传播，实现高质量的自回归视频加速生成。
claims:
- 历史输入与模型输出之间的 Spearman 相关系数显著高于其他输入组件，证明历史令牌是预测输出变化的更可靠依据。
- PCA 投影显示 ARDM 中残差特征在不同段落间形成高度相似且稳定的轨迹，首段轨迹未受误差污染，可作为后续校正的理想参考。
- ARCache 在 FramePack-F1、SkyReels-V2 和 Matrix-Game 上分别实现 2.88×、1.87× 和 3.13× 加速，同时保持高视觉保真度，验证了其广泛的适用性。
- FramePack-F1 上 Speedup = 2.88×
---

# Accelerating Autoregressive Video Diffusion via History-Guided Cache and Residual Correction

> [!tip] 核心洞察
> 通过监控历史令牌而非全局输入来调度缓存（HGC），更准确地抑制段内近似误差；利用首段的清洁残差轨迹参数替换后续段落的轨迹参数进行残差校正（ERC），以几乎可忽略的计算开销阻断误差跨段传播，实现高质量的自回归视频加速生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于历史引导缓存与残差校正的自回归视频扩散加速方法 |
| 英文题名 | Accelerating Autoregressive Video Diffusion via History-Guided Cache and Residual Correction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Nan_Accelerating_Autoregressive_Video_Diffusion_via_History-Guided_Cache_and_Residual_Correction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ARCache |
| Dataset | FramePack-F1, SkyReels-V2, Matrix-Game |

> [!tip] 效果简介
> - FramePack-F1 上，Speedup 2.88× vs 1.0× (unaccelerated) (+1.88×)。
> - SkyReels-V2 上，Speedup 1.87× vs 1.0× (unaccelerated) (+0.87×)。
> - Matrix-Game 上，Speedup 3.13× vs 1.0× (unaccelerated) (+2.13×)。

## 概要

自回归视频扩散模型（ARDM）通过逐段生成的方式有效缓解了长视频合成中的时序一致性问题，但其高昂的计算开销严重制约了实际部署。现有的免训练缓存加速方法主要面向标准扩散模型（SDM）设计，直接迁移至 ARDM 时会因自回归架构的顺序依赖性而引发严重的误差累积——每段内的近似误差会沿时间顺序传播至后续帧，导致画面逐渐失真。本文提出 **ARCache**，首个专为自回归视频扩散模型设计的免训练缓存加速框架，其核心在于两个关键洞察：① 历史令牌（history tokens）的变化与模型输出变化之间存在强相关性，可作为缓存刷新的可靠决策依据；② 未加速的首段残差轨迹在不同段落间高度一致且稳定，可作为清洁参考来矫正加速导致的残差漂移。基于此，ARCache 通过**历史引导缓存（HGC）** 监控历史令牌的累积偏差以自适应调度缓存刷新，抑制段内近似误差；通过**增强残差校正（ERC）** 将首段的清洁残差轨迹参数迁移至后续段落，以几乎可忽略的计算开销阻断误差跨段传播。实验表明，ARCache 在 FramePack-F1、SkyReels-V2 及自回归世界模型 Matrix-Game 上分别实现 **2.88×**、**1.87×** 和 **3.13×** 的加速，同时保持高视觉保真度，验证了其广泛的适用性。



自回归视频扩散模型（Auto-Regressive Diffusion Models, ARDMs）已成为高质量视频生成的主流范式之一，其核心思想是将视频逐段（segment）生成，每一段的去噪过程依赖于前一段产生的历史上下文。然而，这种逐段自回归生成方式带来了极高的推理成本——每一段内部仍需执行完整的迭代去噪过程，导致端到端生成耗时过长，严重制约了实际部署。

### 标准缓存加速在 ARDM 中的失效

针对标准扩散模型（Standard Diffusion Models, SDMs），研究者提出了多种免训练的特征缓存加速方法，如 **TeaCache**（Liu et al., CVPR 2025）、**FORA**（Selvaraju et al., arXiv 2024）、**DeepCache**（Ma et al., CVPR 2024）等。这些方法的核心思路是：在相邻去噪步之间复用模型中间层的特征，避免重复计算。其基础公式为：

$$\mathcal{F}(\mathbf{x}_{t-k}) := \mathcal{F}(\mathbf{x}_t), \quad k \in \{1, \ldots, N\}$$

其中 $\mathcal{F}(\mathbf{x}_t)$ 表示第 $t$ 步计算得到的特征，在后续 $N$ 步中直接复用。

若将这一策略直接迁移到 ARDM，则需在每段内部对历史令牌与噪声令牌的拼接特征进行缓存：

$$\mathcal{F}([\mathbf{h}_{t-k}^s, \mathbf{x}_{t-k}^s]) := \mathcal{F}([\mathbf{h}_t^s, \mathbf{x}_t^s]), \quad k \in \{1, \ldots, N\}$$

然而，ARDM 与 SDM 存在本质差异（图 1）：SDM 中所有帧联合生成，缓存引入的近似误差被限制在单次生成内部；而在 ARDM 中，视频是逐段生成的，前一段的缓存近似误差会作为历史上下文传递至后续段落，沿时间顺序逐段**传播并累积**，导致后续帧出现严重失真。传统缓存方法（如 TeaCache 基于全局输入变化决定缓存刷新）未能感知这种顺序依赖性误差扩散机制，因此在 ARDM 场景下直接失效。

### 核心瓶颈与本文动机

上述问题的**真实瓶颈**在于：缓存加速引入的段内近似误差并非独立存在，而是沿 ARDM 的自回归时间轴顺序传播并逐段放大，形成“误差漂移”（error drift）。这一瓶颈可分解为两个层面：

1. **段内层面**：缓存刷新调度缺乏对 ARDM 特性的适配。传统方法（如 TeaCache）监控全部模型输入的变化来决定刷新时机，但在 ARDM 中，并非所有输入组件对输出变化的预测能力等同。
2. **跨段层面**：缺乏有效的误差阻断机制。即使段内缓存调度得当，残余的近似误差仍会传递至下一段，若无校正手段，误差将随段落数增加而持续累积。

针对以上缺口，本文提出 **ARCache**——首个专为自回归视频扩散模型设计的免训练缓存加速框架。ARCache 包含两个协同模块：**历史引导缓存（History-Guided Cache, HGC）** 通过监控历史令牌的累积偏差自适应调度缓存刷新，抑制段内近似误差；**增强残差校正（Enhanced Residual Correction, ERC）** 利用首段的清洁残差轨迹参数对后续段落进行跨段校正，以几乎可忽略的计算开销阻断误差传播。



## 核心方法与创新机理

ARCache 的核心创新在于针对自回归视频扩散模型（ARDM）特有的“顺序依赖性误差传播”问题，提出了两个紧密协作的 changed slots：**缓存调度决策依据** 与 **残差校正策略**。与面向标准扩散模型（SDM）的缓存方法不同，ARCache 并不将“全部模型输入的变化”作为缓存刷新信号，而是通过监控**历史令牌（history tokens）的累积偏差**来调度缓存（HGC），更精准地抑制段内近似误差；同时，它摒弃了基于当前段落轨迹的预测校正，转而利用**首段的清洁残差轨迹参数**进行跨段残差校正（ERC），以几乎可忽略的计算开销阻断误差跨段传播。

### 从“全局输入监控”到“历史令牌监控”：HGC 的调度逻辑

现有缓存加速方法（如 **TeaCache** (Liu et al., CVPR 2025)）通常依赖全局模型输入的变化来决定是否刷新缓存。这一策略在 SDM 中有效，因为所有帧联合生成，近似误差在空间上被稀释。然而，在 ARDM 中，视频被逐段生成，每一段的输出会作为下一段的**历史输入**。直接沿用全局监控策略会导致缓存刷新时机失准：全局输入的微小变化可能掩盖历史令牌的显著漂移，而历史令牌的漂移恰恰是导致后续段落严重失真的根本原因。

ARCache 通过定量分析揭示了关键因果机制：**历史输入与模型输出之间的 Spearman 相关系数显著高于其他输入组件**（Figure 3）。这一发现表明，历史令牌的变化是预测输出变化、从而决定缓存是否可安全复用的更可靠依据。基于此，HGC 将调度决策依据从“全局输入变化”切换为“历史令牌的归一化 L1 偏差累积”：

$$\Delta ( \mathbf { h } _ { t } ^ { s } ) = \frac { \left\| \mathbf { h } _ { t } ^ { s } - \mathbf { h } _ { t + 1 } ^ { s } \right\| _ { 1 } } { \left\| \mathbf { h } _ { t + 1 } ^ { s } \right\| _ { 1 } }$$

当相邻去噪步之间的累积偏差超过预设阈值 $\delta$ 时，HGC 触发缓存刷新：

$$\sum _ { i = t + 1 } ^ { t _ { \mathrm { r e f } } } \Delta ( \mathbf { h } _ { i } ^ { s } ) \leq \delta < \sum _ { i = t } ^ { t _ { \mathrm { r e f } } } \Delta ( \mathbf { h } _ { i } ^ { s } )$$

这一 changed slot 的本质在于：它不再被动地响应所有输入的变化，而是主动锁定误差传播的**因果源头**——历史令牌。消融实验证实，在相同加速比（2.88×）下，HGC 的 PSNR、SSIM 和 LPIPS 均优于基于全局输入调度（IGC）或常量缓存调度（CGC）的策略（Table 2），验证了“历史令牌监控”这一调度依据的优越性。

### 从“段内预测校正”到“跨段清洁参考校正”：ERC 的误差阻断机制

缓存加速不可避免地引入残差特征的近似误差。现有方法如 **TaylorSeer** (Liu et al., arXiv 2025) 试图通过当前段落的残差轨迹进行一阶预测校正，但这一策略在 ARDM 中面临根本性困境：**后续段落的残差轨迹本身已被前序段落的累积误差污染**，基于受污染轨迹的校正无法有效阻断误差漂移。

ARCache 的 PCA 分析揭示了一个关键现象：ARDM 中残差特征不仅在不同时间步上形成稳定轨迹，而且**不同段落之间的残差轨迹高度相似**（Figure 4）。更重要的是，首段作为生成过程的起点，其残差轨迹未受任何前序段落误差的影响，是天然的“清洁参考”。ERC 正是利用这一跨段相似性，将残差校正策略从“基于当前段落的受污染轨迹预测”切换为“基于首段清洁轨迹参数的跨段校正”：

$$\mathbf { r } _ { t } ^ { s } = \mathbf { r } _ { t _ { b } } ^ { s } + { \frac { \operatorname { L 1 } _ { \mathrm { r e l } } \left( \mathbf { r } _ { t } ^ { 1 } , \mathbf { r } _ { t _ { b } } ^ { 1 } \right) } { \operatorname { L 1 } _ { \mathrm { r e l } } \left( \mathbf { r } _ { t _ { a } } ^ { 1 } , \mathbf { r } _ { t _ { b } } ^ { 1 } \right) } } \left( \mathbf { r } _ { t _ { a } } ^ { s } - \mathbf { r } _ { t _ { b } } ^ { s } \right)$$

其中轨迹参数 $\lambda_t^s$ 直接复用首段的 L1 相对距离比，而非从当前段落重新计算。这一 changed slot 的核心价值在于：它用**零额外计算成本**（仅依赖残差计算，避免了 TaylorSeer 的逐层校正开销）实现了误差传播的有效阻断。消融实验显示，在 HGC 基础上引入 ERC 后，PSNR 从 24.13 提升至 24.79，SSIM 从 0.8169 提升至 0.8266，LPIPS 从 0.1159 降至 0.1117，而推理速度几乎不受影响（Table 2）。

### 双槽协同：从段内抑制到跨段阻断的完整防御

HGC 与 ERC 并非两个孤立的技术点，而是针对 ARDM 误差传播链的**分段防御体系**：HGC 在段内层面，通过监控历史令牌的累积偏差，在误差尚未扩散时精准触发缓存刷新，抑制段内近似误差的产生；ERC 在跨段层面，利用首段清洁轨迹参数校正后续段落的残差，阻断已产生的误差向更远段落传播。两者协同，构成了从“误差源头控制”到“误差传播阻断”的完整防御链，使得 ARCache 在 FramePack-F1（2.88×）、SkyReels-V2（1.87×）和 Matrix-Game（3.13×）上均实现了领先的加速比与视觉保真度。



ARCache 是首个专为自回归视频扩散模型（ARDM）设计的免训练缓存加速框架。其核心 pipeline 由两个协同模块构成：**历史引导缓存（History-Guided Cache, HGC）** 与 **增强残差校正（Enhanced Residual Correction, ERC）**，二者分别针对自回归生成中两类根本性误差——段内近似误差与段间误差传播——进行联合抑制。

### 问题定位

标准扩散模型（SDM）一次生成全部帧，缓存引入的近似误差在空间上分散，影响有限。ARDM 则逐段生成视频：每段内部执行多步去噪，当前段的输出历史令牌会作为下一段的条件输入。直接将传统缓存策略（如 TeaCache, Liu et al., CVPR 2025）应用于 ARDM 时，段内缓存近似误差会沿时间顺序逐段累积，导致后续帧出现严重失真（图 1）。因此，ARDM 的加速面临两个独特挑战：

1. **段内缓存调度失准**：传统方法基于全局输入变化决定缓存刷新，忽略了历史令牌在自回归结构中的主导作用。
2. **段间误差传播**：缓存造成的残差漂移在段落间传递，缺乏有效的跨段校正机制。

### Pipeline 设计

ARCache 的整体流程如图 2 所示，包含以下关键环节：

**输入与段生成循环**：对于每个视频段落 $s$，模型接收历史令牌 $\mathbf{h}^s$ 与当前段噪声令牌 $\mathbf{x}^s$ 的拼接作为输入，经 DiT 骨干网络处理后输出残差特征。HGC 与 ERC 分别作用于特征计算与残差校正两个阶段。

**HGC 模块**：位于 DiT 内部的特征缓存调度层。该模块监控相邻去噪步之间历史令牌的归一化 L1 偏差：

$$\Delta ( \mathbf { h } _ { t } ^ { s } ) = \frac { \left\| \mathbf { h } _ { t } ^ { s } - \mathbf { h } _ { t + 1 } ^ { s } \right\| _ { 1 } } { \left\| \mathbf { h } _ { t + 1 } ^ { s } \right\| _ { 1 } }$$

并以累积偏差是否超过阈值 $\delta$ 作为缓存刷新条件：

$$\sum _ { i = t + 1 } ^ { t _ { \mathrm { r e f } } } \Delta ( \mathbf { h } _ { i } ^ { s } ) \leq \delta < \sum _ { i = t } ^ { t _ { \mathrm { r e f } } } \Delta ( \mathbf { h } _ { i } ^ { s } )$$

当累积偏差未超阈值时，复用上一步缓存的特征；否则触发完整前向计算并更新缓存。这一设计的核心依据是：历史令牌变化与模型输出变化之间的 Spearman 相关系数显著高于其他输入组件（图 3），使其成为预测输出变化、决定缓存复用安全性的更可靠信号。

**ERC 模块**：位于每段去噪完成后的残差校正阶段。其运作依赖于一个关键观察：ARDM 中残差特征在不同段落间形成高度相似且稳定的轨迹（图 4，PCA 投影）。首段（$s=1$）因未受缓存误差污染，其残差轨迹可作为清洁参考。ERC 提取首段的轨迹参数 $\lambda_t^1$，直接替换后续段落的轨迹参数进行校正：

$$\mathbf { r } _ { t } ^ { s } = \mathbf { r } _ { t _ { b } } ^ { s } + \lambda _ { t } ^ { 1 } \left( \mathbf { r } _ { t _ { a } } ^ { s } - \mathbf { r } _ { t _ { b } } ^ { s } \right)$$

其中 $\lambda_t^1$ 由首段最近两次重计算步的残差 L1 相对距离比定义。该校正仅依赖残差层面的轻量运算，避免了 TaylorSeer（Liu et al., arXiv 2025）式的逐层校正开销，几乎不增加推理时间。

**输出流**：校正后的残差经标准去噪流程更新当前段噪声令牌，最终解码为视频帧序列。下一段的历史令牌由当前段输出构建，进入新一轮循环。

### 模块关系

HGC 与 ERC 形成“抑制-阻断”的双重防护：HGC 在段内通过历史令牌引导的自适应调度，从源头减少近似误差的产生；ERC 则在段间利用首段清洁轨迹进行残差校正，阻断已产生误差的跨段传播。消融实验表明，仅使用 HGC（$\delta=0.30$）即可在 FramePack-F1 上实现 2.88× 加速，且 PSNR、SSIM、LPIPS 均优于基于全局输入（IGC）或常量缓存（CGC）的调度策略；在 HGC 基础上引入 ERC，PSNR 从 24.13 进一步提升至 24.79，SSIM 从 0.8169 升至 0.8266，LPIPS 从 0.1159 降至 0.1117，而推理速度几乎不受影响。

### 补充图表

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ARCache. The proposed ARCache integrates a History-Guided Cache (HGC) and an Enhanced Residual Correction (ERC) module to efficiently reuse features while mitigating error accumulation in ARDMs. The left panel illustrates the adaptive cache scheduling mechanism, which leverages correlations between historical inputs and model outputs to optimize cache usage. The right panel depicts the process of residual feature correction along the generation trajectory, effectively suppressing error accumulation*



### 问题形式化：自回归扩散模型中的缓存误差传播

标准扩散模型（SDM）一次性生成全部帧，缓存近似误差仅影响单个去噪轨迹，破坏范围有限。自回归视频扩散模型（ARDM）将视频分段生成，每段内部进行多步去噪，并将已生成段作为“历史令牌”（history tokens）输入后续段。当直接沿用传统特征缓存策略时，段内近似误差会嵌入历史令牌，沿时间顺序传播并逐段累积，导致后续帧严重失真（见 Figure 1）。

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of the proposed ARCache and conventional caching strategies for video generation across different diffusion models. (a) In SDMs, all frames are generated jointly, resulting in limited errors. (b) In ARDMs, videos are generated segment by segment. Directly applying conventional caching strategies leads to the accumulation of historical errors across segments, resulting in severe artifacts in later frames. (c) Our ARCache suppresses approximation errors within individual segments and mitigates error propagation across subsequent frames, effectively preventing error drift and preserving high-quality, temporally consistent video synthesis*

ARDM 中段 $s$ 在去噪步 $t$ 的基线缓存公式为：

$$\mathcal{F}\left(\left[\mathbf{h}_{t-k}^{s}, \mathbf{x}_{t-k}^{s}\right]\right):=\mathcal{F}\left(\left[\mathbf{h}_{t}^{s}, \mathbf{x}_{t}^{s}\right]\right),\quad k\in\{1,\dots,N\}$$

其中 $\mathcal{F}$ 为模型某层的特征计算函数，$\mathbf{h}_t^s$ 为历史令牌，$\mathbf{x}_t^s$ 为当前段噪声令牌。该公式将第 $t$ 步的特征复用于后续 $N$ 步，但未考虑历史令牌变化对输出的影响，是误差传播的根本原因。

### HGC：历史引导的缓存调度

**核心洞察**：历史令牌的变化与模型输出变化之间存在显著更高的相关性。在 FramePack-F1 上的定量分析表明，历史令牌–输出对的 Spearman 相关系数远高于其他输入组件（如当前段令牌）与输出的相关系数，且 P 值更低（见 Figure 3）。这意味着**监控历史令牌的波动可以更可靠地预测输出何时发生实质性变化，从而决定缓存复用是否安全**。

基于此，HGC 定义相邻去噪步历史令牌的归一化 L1 偏差：

$$\Delta(\mathbf{h}_t^s)=\frac{\|\mathbf{h}_t^s-\mathbf{h}_{t+1}^s\|_1}{\|\mathbf{h}_{t+1}^s\|_1}$$

设 $t_{\mathrm{ref}}$ 为最近一次缓存刷新步，HGC 累积从 $t_{\mathrm{ref}}$ 到当前步的历史偏差，当累积量超过阈值 $\delta$ 时触发刷新：

$$\sum_{i=t+1}^{t_{\mathrm{ref}}}\Delta(\mathbf{h}_i^s)\leq\delta<\sum_{i=t}^{t_{\mathrm{ref}}}\Delta(\mathbf{h}_i^s)$$

该策略仅监控历史令牌子集，而非全局输入，计算开销极低。与基于全局输入的调度（IGC）和固定间隔调度（CGC）相比，HGC 在相同加速比下取得更高的 PSNR 和 SSIM、更低的 LPIPS（见 Table 2 消融实验），验证了历史令牌作为缓存决策信号的优越性。

### ERC：增强残差校正

**核心洞察**：ARDM 中残差特征在不同段间形成高度相似且稳定的轨迹。PCA 投影显示，首段残差沿去噪步的演化轨迹与后续段轨迹模式高度一致（见 Figure 4），且首段未经缓存加速污染，可作为“清洁参考”来校正后续段因缓存引入的残差漂移。

设 $\mathbf{r}_t^s$ 为段 $s$ 在步 $t$ 的残差特征，$t_a$、$t_b$ 为最近两次重新计算步（$t_b<t<t_a$）。残差轨迹的一阶近似为：

$$\mathbf{r}_t^s=\mathbf{r}_{t_b}^s+\lambda_t^s\left(\mathbf{r}_{t_a}^s-\mathbf{r}_{t_b}^s\right)$$

其中 $\lambda_t^s$ 为轨迹参数，控制插值位置。传统方法（如 TaylorSeer）从当前段自身估计 $\lambda_t^s$，但缓存误差已污染当前段残差，导致估计偏差沿段传播。

ERC 的关键创新在于**跨段参数替换**：直接使用首段清洁轨迹参数 $\lambda_t^1$ 替换所有后续段的参数：

$$\lambda_t^s=\lambda_t^1=\frac{\operatorname{L1}_{\mathrm{rel}}\left(\mathbf{r}_t^1,\mathbf{r}_{t_b}^1\right)}{\operatorname{L1}_{\mathrm{rel}}\left(\mathbf{r}_{t_a}^1,\mathbf{r}_{t_b}^1\right)}$$

其中 $\operatorname{L1}_{\mathrm{rel}}$ 为 L1 相对距离。代入得跨段校正公式：

$$\mathbf{r}_t^s=\mathbf{r}_{t_b}^s+\frac{\operatorname{L1}_{\mathrm{rel}}\left(\mathbf{r}_t^1,\mathbf{r}_{t_b}^1\right)}{\operatorname{L1}_{\mathrm{rel}}\left(\mathbf{r}_{t_a}^1,\mathbf{r}_{t_b}^1\right)}\left(\mathbf{r}_{t_a}^s-\mathbf{r}_{t_b}^s\right)$$

该公式用首段的“方向”引导后续段的“步长”，以几乎可忽略的计算开销阻断误差跨段传播。消融实验表明，在 HGC 基础上引入 ERC 后，PSNR 从 24.13 提升至 24.79，SSIM 从 0.8169 提升至 0.8266，LPIPS 从 0.1159 降至 0.1117，且推理速度几乎无影响（见 Table 2）。这得益于 ERC 仅依赖残差计算，避免了 TaylorSeer 的逐层校正开销。

### 模块协作与局限

HGC 与 ERC 协同工作：HGC 在每段内部通过历史令牌监控抑制近似误差产生，ERC 利用首段清洁轨迹校正跨段残差漂移。两者共同实现了对 ARDM 缓存误差“段内抑制 + 段间阻断”的双重控制。

当前方法存在两个主要局限：① HGC 的阈值 $\delta$ 需手动设定（实验中固定为 0.30 以获得 2.88× 加速），尚未实现完全自适应的阈值机制；② ERC 假设首段残差轨迹对所有后续段具有代表性，当视频内容发生剧烈变化或首段自身加速质量不佳时，校正准确性可能下降。

### 补充图表

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of Spearman Correlation and P-Value across various input–output pairs on FramePack-F1. In ARDMs, historical context serves as a more reliable basis for caching decisions relative to the full model input, which is the standard practice in previous caching-based acceleration methods*

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/004_Figure_4.jpg]]
*Figure 4: PCA projections of residual features across timesteps in ARDMs*



## 实验与关键发现

### 核心加速效果

ARCache 在三种架构差异显著的自回归视频扩散模型上均实现了大幅推理加速，同时将视觉质量损失控制在极低水平。在 FramePack‑F1 上，ARCache‑fast 以 2.88× 加速取得 PSNR 28.13、SSIM 0.8454、LPIPS 0.1037，PSNR 仅比未加速基线低 0.65 dB；ARCache‑slow 则达到 PSNR 28.13，逼近未加速基线的 28.78 dB。在 SkyReels‑V2 上，ARCache 实现 1.87× 加速，PSNR 28.79、SSIM 0.8460、LPIPS 0.0851；在自回归世界模型 Matrix‑Game 上，加速比高达 3.13×，PSNR 26.88、SSIM 0.7880、LPIPS 0.0858。上述结果均显著优于 TeaCache、FORA、DeepCache、PAB 及 TaylorSeer 等先前缓存加速方法，验证了 ARCache 作为首个面向自回归视频扩散模型的免训练缓存框架的广泛适用性。

### 与先前缓存方法的对比

在 Table 1 的系统对比中，ARCache 在所有三个基准上均取得最佳或次佳的 PSNR、SSIM 和 LPIPS，同时保持领先的加速比。以 FramePack‑F1 为例，TeaCache 在相近加速比下 PSNR 仅 26.03，LPIPS 高达 0.1334；TaylorSeer 的 PSNR 为 27.49，仍低于 ARCache‑fast 的 28.13。值得注意的是，PAB 在 SkyReels‑V2 上出现 OOM，而 ARCache 因仅依赖残差层面的轻量校正，在所有模型上均未遇到显存瓶颈。定性结果（Figure 5）进一步显示，先前方法在长序列生成中后期帧出现明显模糊、色彩偏移和结构失真，而 ARCache 保持了与未加速基线高度一致的时序连贯性和视觉保真度。

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on different auto-regressive diffusion models with baselines. The best result is highlighted in bold, while the second-best result is underlined. “OOM” indicates CUDA out of memory on the H100 80GB GPU*

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison with previous competing methods. Please zoom in for more details*

### 逐帧质量稳定性

Figure 6 的逐帧评估曲线揭示了不同方法在长序列生成中的质量衰减模式。未加速基线的 PSNR 和 SSIM 随帧序号仅轻微下降，LPIPS 缓慢上升，呈现理想的稳定趋势。直接应用 TeaCache 或 FORA 等传统缓存策略时，PSNR 从约第 20 帧起急剧下降，LPIPS 同步攀升，表明近似误差沿自回归链迅速累积。相比之下，ARCache 的逐帧曲线紧贴未加速基线，PSNR 均值仅略低，LPIPS 均值仅略高，且在整个序列长度内未出现发散性退化。这直接印证了 HGC 对段内近似误差的抑制和 ERC 对跨段误差传播的阻断作用。

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/007_Figure_6.jpg]]
*Figure 6: Frame-wise evaluation across different ARDMs. Dashed lines denote mean values. Please zoom in for more details*

### 消融实验：缓存调度策略

Table 2 的消融实验首先对比了三种缓存调度策略：基于常量间隔的 CGC、基于全局输入变化的 IGC，以及本文提出的基于历史令牌变化的 HGC。在相同加速比 2.88×（δ=0.30）下，HGC 取得 PSNR 24.13、SSIM 0.8169、LPIPS 0.1159，三项指标均优于 IGC 和 CGC。该结果与 Figure 3 的 Spearman 相关性分析一致——历史令牌与模型输出之间的相关性显著高于其他输入组件，因此监控历史令牌的累积偏差能更准确地判断何时需要刷新缓存，从而在相同计算预算下保留更多关键特征信息。

![[assets/figures/papers/paper_list_l831_https_openaccess_thecvf_com_content_CVPR2026_html_Nan_Accelerating_Autor/figures/008_Table_2.jpg]]
*Table 2: Ablation studies of different components and hyperparameters using FramePack-F1*

### 消融实验：残差校正模块

在 HGC 基础上引入 ERC 后，PSNR 从 24.13 进一步提升至 24.79（+0.66 dB），SSIM 从 0.8169 升至 0.8266，LPIPS 从 0.1159 降至 0.1117，而推理速度几乎无变化。这一几乎零开销的质量增益源于 ERC 的设计：它仅利用首段残差轨迹参数进行跨段校正，避免了 TaylorSeer 那种逐层特征预测与校正的繁重计算。Figure 4 的 PCA 投影为 ERC 提供了机理层面的支撑——不同段落的残差特征在时间步上形成高度相似且稳定的轨迹，首段轨迹因未受缓存近似误差污染，可作为清洁参考来校正后续段落的残差漂移。

### 超参数敏感性

δ 控制 HGC 的累积偏差阈值，直接决定缓存刷新频率与加速比。Table 2 显示，当 δ 从 0.20 增大到 0.40 时，加速比从 2.42× 升至 3.26×，但 PSNR 从 24.79 降至 23.87，LPIPS 从 0.1117 升至 0.1265，呈现典型的速度‑质量折衷。实验中固定 δ=0.30 作为默认配置，在实际部署中可根据场景需求灵活调节。

### 失败模式与局限性

尽管 ARCache 在三个基准上表现出色，其设计仍存在以下边界条件。第一，HGC 依赖手动设定的阈值 δ，尚未实现完全自适应的缓存调度，在视频内容统计特性剧烈变化时可能需要重新调参。第二，ERC 假设首段残差轨迹对所有后续段落具有代表性；当首段本身因加速导致质量显著下降，或视频内容发生场景切换等剧烈变化时，校正的准确性可能降低。第三，当前实验覆盖的模型架构有限，在更大规模世界模型或不同噪声调度下的泛化性仍需进一步验证。上述局限性在论文中已明确讨论，建议在实际应用中针对具体模型和场景进行适配性测试。



## 定位与知识库关联

### 与标准扩散模型缓存方法的差异

ARCache 的核心定位是**首个专为自回归视频扩散模型（ARDM）设计的免训练缓存加速框架**。它与面向标准扩散模型（SDM）的缓存方法存在根本性差异，这种差异源于两类模型生成范式的不同。

在 SDM 中，所有帧联合生成，缓存引入的近似误差被限制在单次生成过程内，影响范围有限。然而在 ARDM 中，视频被逐段生成，每一段的输出作为下一段的“历史”输入。当直接应用传统缓存策略时，段内近似误差会通过历史令牌（history tokens）传递到后续段落，形成**顺序依赖性的错误传播与累积**，导致后期帧出现严重失真（Figure 1）。

现有面向 SDM 的缓存方法——如 **TeaCache**（Liu et al., CVPR 2025）基于时间步嵌入调度缓存、**FORA**（Selvaraju et al., arXiv 2024）面向 DiT 架构进行特征缓存、**DeepCache**（Ma et al., CVPR 2024）在 UNet 中进行层次化特征复用——均未考虑 ARDM 中跨段误差传播这一独特挑战。ARCache 通过两个协同模块直接应对这一瓶颈：**HGC** 抑制段内近似误差，**ERC** 阻断跨段误差传播。

### 方法谱系中的位置

ARCache 处于“免训练缓存加速”与“自回归视频扩散模型”两个研究方向的交汇点。在缓存加速谱系中，它继承了对模型特征进行时间步间复用的基本思想，但其调度依据和校正策略均针对 ARDM 的序列生成特性进行了重新设计。

**缓存调度决策依据的演进**：传统方法（如 TeaCache）基于全部模型输入的变化来决定缓存刷新时机。ARCache 通过定量分析发现，在 ARDM 中，历史令牌的变化与模型输出变化之间的 **Spearman 相关系数显著高于其他输入组件**（Figure 3），因此将监控对象从全局输入收缩到历史令牌子空间。这一发现构成了 HGC 的理论基础——通过追踪历史令牌的归一化 L1 累积偏差来触发缓存刷新，比基于全局输入的调度策略（IGC）或常量缓存策略（CGC）更准确地捕捉输出变化的时机。

**残差校正策略的演进**：**TaylorSeer**（Liu et al., arXiv 2025）提出了基于特征预测与校正的缓存加速方法，但其校正依赖当前段落的轨迹参数，且需要逐层计算，开销较大。ARCache 的 ERC 模块观察到 ARDM 中残差特征在不同段落间形成高度相似且稳定的轨迹（Figure 4），且首段轨迹未受缓存误差污染，因此**直接复用首段的清洁残差轨迹参数** $\lambda_t^1$ 来校正所有后续段落。这一策略避免了 TaylorSeer 的逐层校正开销，计算负担几乎可忽略。

### 适用边界与局限

ARCache 的有效性建立在两个核心假设之上，这些假设同时划定了方法的适用边界：

1. **历史令牌与输出变化的高相关性假设**：HGC 依赖历史令牌的波动来预测输出变化。当视频内容发生剧烈突变（如场景切换）时，历史令牌的稳定性可能不足以准确反映输出变化，此时缓存刷新时机的判断精度可能下降。实验仅在 FramePack-F1、SkyReels-V2 和 Matrix-Game 三种特定的 ARDM 架构上验证，泛化到其他架构（如更大规模世界模型或不同噪声调度策略）的有效性仍需进一步验证。

2. **首段残差轨迹的代表性假设**：ERC 假设首段的残差轨迹对所有后续段落均具有代表性。当首段本身的生成质量因缓存加速而受损，或视频内容在不同段落间差异极大时，这一假设可能不成立，校正准确性将下降。此外，HGC 依赖超参数 $\delta$ 手动控制缓存刷新频率（实验中固定为 0.30 以获得 2.88× 加速），实际部署时仍需人工调节以平衡速度与质量，尚未实现完全自适应的阈值机制。

### 开放问题

基于上述局限，一个自然的开放问题是：能否设计完全自适应的、无预定义阈值的缓存刷新策略，使 ARCache 在无需人工调参的情况下自动适应不同模型和生成任务的速度‑质量平衡需求？这需要更深入地理解历史令牌动态与输出质量之间的函数关系，或引入轻量级的在线质量估计模块。



## 原文 PDF

![[paperPDFs/CVPR_2026/Accelerating_Autoregressive_Video_Diffusion_via_History_Guided_Cache_and_Residual_Correction.pdf]]

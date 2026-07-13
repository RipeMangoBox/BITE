---
title: "Reward Forcing: Efficient Streaming Video Generation with Rewarded Distribution Matching Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Reward_Forcing_Efficient_Streaming_Video_Generation_with_Rewarded_Distribution_Matching_Distillation.pdf
project_link: "https://reward-forcing.github.io/"
code_link: null
aliases:
- RF
- RFESVGRDMD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过指数移动平均动态更新沉没令牌，打破对首帧的过度依赖，同时利用视觉语言模型作为奖励函数，为高动态样本赋予更高的蒸馏权重，引导生成分布向高奖励区域偏移。
primary_logic: 将滑动窗口中被丢弃的中间帧信息通过EMA持续压缩进固定大小的沉没令牌中，既保留了全局上下文又引入了近期动态；并在蒸馏过程中引入奖励加权，将强化学习的偏好优化与分布匹配结合，在不牺牲保真度的前提下有效提升视频动态性。
claims:
- EMA-Sink通过指数移动平均将逐出窗口的令牌持续融合进压缩状态，避免信息瓶颈。
- Re-DMD使用视觉语言模型作为奖励函数，对高动态样本加权分布匹配梯度，使生成分布偏向高奖励区域。
- Reward Forcing在VBench短视频评测中取得总分84.13，推理速度达23.1 FPS，超越所有基线。
- 在长视频生成中，动态得分大幅提升至66.95（较LongLive提升88%），同时质量漂移最小。
---

# Reward Forcing: Efficient Streaming Video Generation with Rewarded Distribution Matching Distillation

> [!tip] 核心洞察
> 将滑动窗口中被丢弃的中间帧信息通过EMA持续压缩进固定大小的沉没令牌中，既保留了全局上下文又引入了近期动态；并在蒸馏过程中引入奖励加权，将强化学习的偏好优化与分布匹配结合，在不牺牲保真度的前提下有效提升视频动态性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Reward Forcing：基于奖励分布匹配蒸馏的高效流式视频生成 |
| 英文题名 | Reward Forcing: Efficient Streaming Video Generation with Rewarded Distribution Matching Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04678) · [Project](https://reward-forcing.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Reward Forcing |
| Dataset | VBench, VBench Long |

> [!tip] 效果简介
> - VBench (5s short clips) 上，Total Score ↑ 84.13 vs 83.80 (Self Forcing) (+0.33)；sFPS ↑ 23.1 vs 17.0 (Self Forcing) (+6.1 (1.36×))。
> - VBench Long (60s) 上，Total Score ↑ 81.41 vs 79.53 (LongLive) (+1.88)；Dynamic Degree ↑ 66.95 vs 35.54 (LongLive) (+31.41)；Drift ↓ 2.505 vs 2.531 (LongLive) (-0.026)。

## 概要

**问题瓶颈**：现有自回归视频生成方法普遍采用滑动窗口注意力与静态初始帧沉没令牌（Sink Token），导致模型过度依赖首帧信息，运动动态性严重退化；同时，标准分布匹配蒸馏（DMD）对所有样本一视同仁，无法优先优化高动态样本，限制了生成视频的动态表现力。

**核心思路**：本文提出 **Reward Forcing**，从两个维度突破上述瓶颈。其一，设计 **EMA-Sink** 机制——通过指数移动平均（EMA）持续将被逐出滑动窗口的中间帧键值对融合进固定大小的沉没令牌中，使压缩状态既保留全局上下文又引入近期动态信息，打破对首帧的过度依赖。其二，提出 **奖励加权分布匹配蒸馏（Re-DMD）**——利用视觉语言模型作为奖励函数评定样本的运动质量，对高动态样本赋予更高的蒸馏权重，从而引导生成分布向高奖励区域偏移，在不牺牲保真度的前提下有效提升视频动态性。

**方法定位**：Reward Forcing 将强化学习的偏好优化思想与分布匹配蒸馏相结合，在继承 Self Forcing 自回滚训练-推理对齐机制的基础上，引入 EMA-Sink 的状态打包策略和 Re-DMD 的奖励驱动优化，构建了一个支持流式推理的高效自回归视频生成框架。

**主要结果**：
- **短视频生成**：在 VBench 5秒短视频评测中，Reward Forcing 取得总分 **84.13**，超越所有可比基线；推理速度达 **23.1 FPS**（单张 H100 GPU），较 Self Forcing 的 17.0 FPS 提升 1.36 倍。
- **长视频生成**：在 60 秒长视频评测中，动态得分大幅提升至 **66.95**，较 LongLive 的 35.54 提升 88.38%，同时质量漂移最小（2.505 vs. 2.531），在显著增强运动幅度的同时保持了时序一致性。
- **消融验证**：移除 Re-DMD 训练后动态得分从 64.06 骤降至 43.75；进一步移除 EMA-Sink 模块后动态得分继续降至 35.15，运动平滑度同步下降，证实了两个核心组件的关键作用。



### 视频生成范式的演进

近年来，视频生成领域经历了从单向扩散模型到自回归流式生成的重要范式转变。单向视频扩散模型通过逐帧去噪实现高质量视频合成，但其双向注意力机制要求模型在推理时一次性处理完整序列，导致内存开销随视频长度线性增长，难以支持长时域生成与实时交互。相比之下，自回归学生模型将视频生成重新定义为逐帧预测任务，结合滑动窗口注意力与KV缓存机制，能够以恒定的内存和计算开销实现流式推理，为实时视频生成铺平了道路。

### 现有自回归方法的核心瓶颈

尽管自回归蒸馏方法在推理效率上取得了显著突破，当前主流方案仍面临两个紧密耦合的瓶颈，严重制约了生成视频的运动动态性与长程质量。

**瓶颈一：静态沉没令牌导致运动退化。** 为在滑动窗口注意力中维持全局上下文，现有方法通常将首帧作为固定的“沉没令牌”永久保留在KV缓存中。然而，这种静态策略使模型过度依赖初始帧的信息，随着窗口滑动，被逐出的中间帧所携带的运动线索完全丢失，导致生成视频的物体运动幅度逐渐衰减，甚至退化为近乎静态的“帧复制”现象。**LongLive**等使用静态Sink Token的基线方法在长视频生成中动态得分仅为35.54，充分暴露了这一缺陷。

**瓶颈二：标准分布匹配蒸馏对所有样本一视同仁。** 当前主流的分布匹配蒸馏损失对所有生成样本赋予均等的优化权重。这意味着模型在蒸馏过程中不会区分高动态样本与低动态样本，无法针对性地提升运动质量。在教师模型本身对高动态场景生成能力有限的情况下，均匀加权策略进一步加剧了学生模型在运动动态性上的退化。

### Reward Forcing的动机与核心思路

针对上述瓶颈，本文提出**Reward Forcing**框架，通过两个关键创新实现高效流式视频生成与运动动态性的协同提升：

1. **EMA-Sink机制**：以指数移动平均的方式，将被逐出滑动窗口的中间帧令牌持续融合进固定大小的压缩状态中。这一设计打破了静态沉没令牌对首帧的过度依赖，使模型在保留全局上下文的同时捕获近期动态信息，从根本上缓解运动退化问题。

2. **Re-DMD训练策略**：引入视觉语言模型作为奖励函数，对生成样本的运动质量进行评分，并将该评分作为权重融入分布匹配蒸馏梯度。通过优先优化高动态样本，Re-DMD引导生成分布向高奖励区域偏移，在不牺牲保真度的前提下有效提升视频动态性。

这两种机制的协同作用使得Reward Forcing能够在单张H100 GPU上实现23.1 FPS的实时流式视频生成，同时在长视频场景下将动态得分提升至66.95（较LongLive提升88%），且质量漂移保持在最低水平。



## 核心方法与创新机理

Reward Forcing 针对现有流式视频生成的两大瓶颈——**滑动窗口注意力对首帧的过度依赖导致运动动态退化**，以及**标准分布匹配蒸馏对所有样本一视同仁无法优先优化高动态样本**——提出了两个紧密协作的核心创新：EMA-Sink 状态打包机制与 Re-DMD 奖励加权蒸馏目标。

### 创新一：EMA-Sink——动态全局状态压缩

在自回归长视频生成中，滑动窗口注意力为控制计算与内存成本必须逐出旧令牌，但直接丢弃中间帧信息会导致模型过度依赖窗口内保留的首帧（sink token），引发“帧复制”现象，运动幅度严重衰减。EMA-Sink 的核心思想是：**将被逐出窗口的中间帧信息通过指数移动平均持续压缩进固定大小的沉没令牌中**，使模型在保持恒定内存的同时持续获取全局上下文与近期动态。

具体而言，当第 $i-w$ 帧被逐出滑动窗口时，其键值对 $(\mathbf{K}^{i-w}, \mathbf{V}^{i-w})$ 并不被直接丢弃，而是按如下方式融入压缩的沉没状态：

$${\pmb S}_{\mathbf{K}}^{i} = \alpha \cdot {\pmb S}_{\mathbf{K}}^{i-1} + (1 - \alpha) \cdot {\pmb K}^{i-w}$$

$${\cal S}_{V}^{i} = \alpha \cdot {\cal S}_{V}^{i-1} + (1 - \alpha) \cdot {\cal V}^{i-w}$$

其中 $\alpha$ 为动量衰减系数（实验选定 $\alpha = 0.99$）。更新后的沉没状态与当前窗口内的令牌拼接，构成全局注意力上下文：

$$K_{\mathrm{global}}^{i} = [S_{K}^{i}; K^{i-w+1:i}], \quad V_{\mathrm{global}}^{i} = [S_{V}^{i}; V^{i-w+1:i}]$$

这一设计带来三重优势：**(1)** 打破了对首帧的过度依赖——EMA 融合使沉没令牌不再仅是静态初始帧的副本，而是携带了历史动态信息；**(2)** 令牌逐出复杂度为 $O(1)$，内存占用与序列长度解耦，保障了实时推理效率；**(3)** 与 **LongLive** 等使用静态 Sink Token 的基线相比，EMA-Sink 在长视频生成中动态得分大幅提升（消融实验显示移除 EMA-Sink 后动态得分从 64.06 骤降至 35.15，运动平滑度从 98.91 降至 98.64）。

### 创新二：Re-DMD——奖励驱动的分布匹配蒸馏

标准分布匹配蒸馏（DMD）通过最小化学生生成分布与教师真实分布之间的 KL 散度来训练生成器，其梯度形式为：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} \approx -\mathbb{E}_t \Big(\int (s_{\mathrm{real}} - s_{\mathrm{fake}}) \frac{\mathrm{d} G_{\theta}(\epsilon)}{\mathrm{d}\theta} \mathrm{d}\epsilon \Big)$$

该目标对所有样本赋予相同权重，无法区分高动态与低动态样本。Reward Forcing 提出 **Re-DMD**，将强化学习的偏好优化思想融入分布匹配：**利用视觉语言模型（VLM）作为奖励函数评估每个样本的运动质量，将奖励分数作为权重乘到分布匹配梯度上**，引导生成分布向高奖励（高动态）区域偏移。

Re-DMD 的目标函数为：

$$\mathcal{T}_{\mathrm{Re-DMD}} = \mathbb{E}_{p(c)p_{\mathrm{fake}}^{\prime}(\pmb{x}_{0}|c)} \left[ \frac{\exp(r(\pmb{x}_{0},\pmb{c})/\beta)}{Z(\pmb{c})} \log \frac{p_{\mathrm{fake}}(\pmb{x}_{0}|\pmb{c})}{p_{\mathrm{real}}(\pmb{x}_{0}|\pmb{c})} \right]$$

对应的梯度近似为：

$$\nabla_{\theta} \mathcal{J}_{\mathrm{Re-DMD}} \approx -\mathbb{E}_t \Big(\int \exp(r^{c}(\pmb{x}_{t})/\beta) \cdot (s_{\mathrm{real}} - s_{\mathrm{fake}}) \frac{\mathrm{d} G_{\theta}(\epsilon)}{\mathrm{d}\theta} \mathrm{d}\epsilon \Big)$$

关键设计在于：**奖励函数仅作为静态权重作用于梯度，无需计算奖励模型自身的梯度**。这带来了两个重要特性：**(1)** 训练稳定——避免了强化学习中常见的策略梯度高方差问题；**(2)** 收敛加速——奖励信号直接引导优化方向，训练过程中动态得分稳步上升（见 Figure 6 训练曲线）。温度参数 $\beta$ 控制奖励权重的集中程度，实验选定 $\beta = 1/2$ 在动态得分与一致性指标间取得最优平衡。

### 创新协同：训练-推理一致性的完整闭环

Reward Forcing 继承并扩展了 **Self Forcing** 的自回滚训练机制，使训练与推理的序列生成方式保持一致。在此框架下，EMA-Sink 与 Re-DMD 形成协同效应：

- **EMA-Sink** 在推理时保障长视频生成的运动动态性与时序连贯性，使模型有能力产生高动态样本；
- **Re-DMD** 在训练时引导模型优先学习这些高动态样本的分布特征，形成“能力-偏好”的正向循环。

消融实验证实了这一协同关系：单独移除 Re-DMD 导致动态得分从 64.06 降至 43.75；在此基础上进一步移除 EMA-Sink，动态得分再降至 35.15，运动平滑度同步下降。完全去除 Sink Token 则导致生成质量显著退化。这些结果表明，两个创新组件分别从推理架构与训练目标两个维度解决了运动动态性不足的瓶颈，且缺一不可。

### 与基线方法的差异总结

| 方法 | Sink Token 更新策略 | 蒸馏目标 | 训练-推理对齐 |
|------|---------------------|----------|---------------|
| **LongLive** | 静态首帧，全程不变 | 标准 DMD | 无自回滚 |
| **Self Forcing** | 静态首帧 | 标准 DMD | 自回滚机制 |
| **Reward Forcing (Ours)** | **EMA 动态融合逐出令牌** | **Re-DMD 奖励加权** | 自回滚机制 |

Reward Forcing 是首个将动态状态压缩与奖励驱动分布匹配结合用于流式视频生成的工作，在不牺牲保真度的前提下，有效突破了现有方法在长视频运动动态性上的瓶颈。



Reward Forcing 的核心目标是将一个双向视频扩散模型蒸馏为支持实时流式生成的自回归学生模型。整个框架由三条设计主线交织而成：**流式推理管道**负责维持恒定内存的自回归生成，**EMA-Sink 模块**在滑动窗口注意力中动态压缩全局状态，**Re-DMD 训练模块**则通过奖励加权将生成分布推向高动态区域。

### 流式推理管道：KV 缓存与滑动窗口注意力

管道以文本提示为条件，逐块生成视频帧。具体而言，当前流中的噪声令牌首先被投影为新的键-值对（图3绿色块），追加至 KV 缓存以参与注意力计算。当 KV 缓存达到预设的注意力窗口上限时，最早进入窗口的令牌将被逐出，同时通过 EMA-Sink 机制将逐出令牌的信息融合进压缩的沉没状态中（图3黄色块）。这一设计使注意力计算与序列长度解耦，实现 O(1) 的令牌逐出开销和恒定内存占用，从而支撑 23.1 FPS 的实时推理。

### EMA-Sink：动态全局状态压缩

EMA-Sink 是打破模型对首帧过度依赖的关键。在滑动窗口注意力中，传统方法仅保留初始帧作为固定的沉没令牌（Sink Token），中间帧被直接丢弃，导致模型严重偏向首帧、运动动态性退化。EMA-Sink 将沉没令牌初始化为起始帧，并在每帧被逐出窗口时，通过指数移动平均将其键-值对持续融合进压缩状态：

$${\pmb S}_{\bf K}^{i} = \alpha \cdot {\pmb S}_{\bf K}^{i-1} + (1 - \alpha) \cdot {\pmb K}^{i-w}$$

$${\cal S}_{V}^{i} = \alpha \cdot {\cal S}_{V}^{i-1} + (1 - \alpha) \cdot {\cal V}^{i-w}$$

其中 $\alpha$ 为动量衰减系数（实现中取 $\alpha = 9e^{-3}$），$w$ 为窗口大小。融合后的全局状态 $S_{K}^{i}$、$S_{V}^{i}$ 与窗口内近期令牌 $K^{i-w+1:i}$、$V^{i-w+1:i}$ 拼接，构成完整的全局键-值状态参与注意力计算。这一机制既保留了全局上下文，又引入了近期动态信息，在长视频生成中显著提升了运动动态性和时序一致性。

### Re-DMD：奖励加权的分布匹配蒸馏

在训练侧，Reward Forcing 继承 Self Forcing 的自回滚机制以保证训练-推理一致性，并将标准分布匹配蒸馏（DMD）扩展为奖励加权的 Re-DMD。核心思想是：利用强大的视觉语言模型作为奖励函数，对生成样本的运动质量进行评分，然后用该评分对分布匹配梯度进行加权：

$$\nabla_{\theta} \mathcal{J}_{\mathrm{Re-DMD}} \approx -\mathbb{E}_t \Big(\int \exp(r^{c}({\pmb x}_{t})/\beta) \cdot (s_{\mathrm{real}} - s_{\mathrm{fake}}) \frac{\mathrm{d} G_{\theta}(\epsilon)}{\mathrm{d}\theta} \mathrm{d}\epsilon \Big)$$

其中 $r^{c}({\pmb x}_{t})$ 为奖励分数，$\beta$ 为温度系数（最终选取 $\beta = 1/2$）。奖励函数作为静态权重，无需计算其梯度，从而稳定训练并加速收敛。这一设计将强化学习的偏好优化与分布匹配相结合，在不牺牲保真度的前提下，引导生成器优先优化高动态样本，使生成分布向高奖励区域偏移。

### 模块协作流程

三个模块在训练与推理中紧密协作：
1. **训练阶段**：学生模型以自回滚方式生成视频片段，幻觉令牌被解码为视频后送入奖励模型评分，评分结果用于加权 Re-DMD 梯度，由教师模型提供分布匹配信号。
2. **推理阶段**：学生模型在 KV 缓存与滑动窗口注意力下自回归生成，EMA-Sink 持续更新沉没状态以维持全局上下文，实现恒定内存的流式视频生成。

消融实验证实了这一协作的必要性：移除 Re-DMD 训练后，长视频动态得分从 64.06 骤降至 43.75；进一步移除 EMA-Sink 模块，动态得分继续降至 35.15，运动平滑度也从 98.91 下降至 98.64。完全去除沉没令牌则导致生成质量显著退化。这些结果表明，EMA-Sink 与 Re-DMD 在打破首帧依赖与提升运动动态性方面形成了互补增强效应。

### 补充图表

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/001_Figure_1.jpg]]
*Figure 1: We propose Reward Forcing to distill a bidirectional video diffusion model into a few-step autoregressive student model that enables real-time (23.1 FPS) streaming video generation. Instead of using vanilla distribution matching distillation (DMD), Reward Forcing adopts a novel rewarded distribution matching distillation (Re-DMD) that prioritizes matching towards high-reward regions, leading to enhanced object motion dynamics and immersive scene navigation dynamics in generated videos*

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of Reward Forcing. In a streaming text-to-video generation, noisy tokens in the current stream are first projected to produce new key-value pairs (green blocks), which are appended to the KV cache for attention computation. When the current KV cache reaches its maximum attention window size, sink tokens initialized from start frames (yellow blocks) are updated via exponential moving average using evicted tokens (pink blocks). During training, hallucinated tokens are decoded into videos to compute a reward score via a reward function. This score is then used to weight the distribution matching gradient from the teacher model*



Reward Forcing 的核心架构由两个关键模块构成：**EMA-Sink** 负责在流式生成中动态维护全局压缩状态，打破传统滑动窗口自回归对首帧的过度依赖；**Re-DMD** 则在分布匹配蒸馏过程中引入视觉语言模型奖励加权，将生成分布导向高动态区域。两者协同工作于继承了 Self Forcing 自回滚机制的流式推理管道之上。

### EMA-Sink：指数移动平均沉没令牌

传统滑动窗口注意力机制（如 LongLive）将初始帧作为静态 Sink Token 固定于 KV 缓存中，全程不变。这导致被逐出窗口的中间帧信息永久丢失，模型过度依赖首帧，运动动态性严重退化。EMA-Sink 的核心思想是：**将逐出窗口的令牌通过指数移动平均持续融合进固定大小的压缩状态中**，使 Sink Token 既保留全局上下文，又捕获近期动态。

具体地，设滑动窗口大小为 $w$，当第 $i$ 帧进入窗口时，第 $i-w$ 帧被逐出。其键-值对 $(\pmb{K}^{i-w}, \pmb{V}^{i-w})$ 并非直接丢弃，而是按 EMA 方式融入压缩的沉没状态 $\pmb{S}_{\bf K}^{i}$ 和 $\pmb{S}_{V}^{i}$：

$${\pmb S}_{\bf K}^{i} = \alpha \cdot {\pmb S}_{\bf K}^{i-1} + (1 - \alpha) \cdot {\pmb K}^{i-w}$$

$${\cal S}_{V}^{i} = \alpha \cdot {\cal S}_{V}^{i-1} + (1 - \alpha) \cdot {\cal V}^{i-w}$$

其中 $\alpha$ 为动量衰减系数，控制历史信息保留程度。当前全局键-值状态由压缩沉没状态与窗口内活跃令牌拼接而成：

$$K_{\mathrm{global}}^{i} = \left[ S_{K}^{i} ; K^{i-w+1:i} \right], \quad V_{\mathrm{global}}^{i} = \left[ S_{V}^{i} ; V^{i-w+1:i} \right]$$

这一设计的因果机制在于：**EMA 的递归更新使 Sink Token 成为所有被逐出帧的加权聚合**，权重随时间指数衰减，天然赋予近期帧更高影响权重。同时，注意力计算仅依赖固定大小的全局状态，实现了 O(1) 令牌逐出与恒定内存占用，保障了实时推理效率。消融实验表明，完全去除 Sink Token 会导致生成质量显著退化；移除 EMA-Sink 后动态得分从 43.75 进一步降至 35.15，运动平滑度从 98.91 降至 98.64，验证了该模块对动态性与时序一致性的关键作用。

### Re-DMD：奖励加权的分布匹配蒸馏

标准分布匹配蒸馏（DMD）对所有生成样本施加均等权重，其梯度形式为：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} \approx -\mathbb{E}_t \Big(\int (s_{\mathrm{real}}(\Psi(G_{\theta}(\epsilon),t),t) - s_{\mathrm{fake}}(\Psi(G_{\theta}(\epsilon),t),t)) \frac{\mathrm{d} G_{\theta}(\epsilon)}{\mathrm{d}\theta} \mathrm{d}\epsilon \Big)$$

其中 $s_{\mathrm{real}}$ 与 $s_{\mathrm{fake}}$ 分别为真实分布与生成分布的得分函数，梯度通过两者之差驱动生成器 $G_{\theta}$ 更新。然而，这种均等加权策略无法优先优化高动态样本，导致模型在运动质量上的提升有限。

Re-DMD 的突破在于：**将强化学习的奖励最大化目标与分布匹配蒸馏统一**。其目标函数为：

$$\mathcal{T}_{\mathrm{Re-DMD}} = \mathbb{E}_{p(c)p_{\mathrm{fake}}^{\prime}(\pmb{x}_{0}|c)} \left[ \frac{\exp(r(\pmb{x}_{0},\pmb{c})/\beta)}{Z(\pmb{c})} \log \frac{p_{\mathrm{fake}}(\pmb{x}_{0}|\pmb{c})}{p_{\mathrm{real}}(\pmb{x}_{0}|\pmb{c})} \right]$$

其中 $r(\pmb{x}_{0}, \pmb{c})$ 为视觉语言模型评定的运动质量奖励，$\beta$ 为温度系数控制奖励权重强度，$Z(\pmb{c})$ 为归一化因子。该目标本质上是**以奖励指数加权后的 KL 散度**，使生成分布向高奖励区域偏移，同时保持与真实分布的保真度约束。

在实际训练中，Re-DMD 的梯度近似为将奖励作为静态权重直接乘到 DMD 梯度上：

$$\nabla_{\theta} \mathcal{J}_{\mathrm{Re-DMD}} \approx -\mathbb{E}_t \Big(\int \exp(r^{c}(\pmb{x}_{t})/\beta) \cdot (s_{\mathrm{real}}(\Psi(G_{\theta}(\epsilon),t),t) - s_{\mathrm{fake}}(\Psi(G_{\theta}(\epsilon),t),t)) \frac{\mathrm{d} G_{\theta}(\epsilon)}{\mathrm{d}\theta} \mathrm{d}\epsilon \Big)$$

这一近似的关键优势在于：**无需计算奖励模型的梯度**，避免了强化学习中常见的策略梯度高方差问题，训练稳定且收敛更快。消融实验证实，移除 Re-DMD 训练后动态得分从 64.06 大幅降至 43.75；奖励权重 $\beta = 1/2$ 在动态得分、运动平滑度与质量漂移之间取得了最优折中。

### 训练-推理一致性

Reward Forcing 继承了 **Self Forcing** 的自回滚机制，在训练时即采用与推理一致的自回归生成范式，消除了训练-推理分布偏移。在此基础上，EMA-Sink 和 Re-DMD 分别针对状态打包策略与蒸馏目标函数进行改进，形成了完整的流式视频生成方案。训练采用分块去噪策略，每块 3 个潜在帧，基础模型为 **Wan2.1-T2V-1.3B**。

### 补充图表

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of EMA Sink with Existing Methods. Long video generation models typically extrapolate beyond their training sequence length during inference. (a) Window Attention caches only recent tokens for efficient inference but suffers performance degradation. (b) Sliding Window with attention sinks retains initial tokens for stable attention computation and recent tokens for extrapolation. However, discarding intermediate frames causes over-reliance on the first frame, leading to “frame copy*



## 实验与关键发现

### 短视频生成性能

Reward Forcing 在标准 VBench 5 秒短视频评测上取得 **总分 84.13**，略高于强基线 Self Forcing 的 83.80（Table 1）。更关键的提升在于推理效率：Reward Forcing 达到 **23.1 FPS**，相比 Self Forcing 的 17.0 FPS 提升约 1.36 倍，首次在单张 H100 GPU 上实现实时流式视频生成。该结果验证了 EMA-Sink 与 Re-DMD 蒸馏框架在保持生成质量的同时，显著降低了推理延迟。

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/006_Table_1.jpg]]
*Table 1: Short video performance comparison with baselines. The comparison includes representative open-source models of comparable scale. Best results in bold, second-best underlined*

### 长视频生成性能

在 60 秒长视频评测（VBench Long）上，Reward Forcing 取得 **总分 81.41**，超越 LongLive 的 79.53（Table 2）。其中动态维度提升最为显著：**动态得分从 35.54 跃升至 66.95，提升幅度达 88.38%**，同时质量漂移指标（Drift）从 2.531 微降至 2.505，表明动态性的大幅增强并未以牺牲时序稳定性为代价。定性对比（Figure 4、Figure 5）进一步显示，Reward Forcing 在长程文本对齐、运动动态和时序一致性上均优于基线方法，后者则出现明显的动态退化与一致性衰减。

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/007_Table_2.jpg]]
*Table 2: Long video performance comparison with key baselines. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison on dynamic complexity of long video generation. Reward Forcing excels in both text alignment and motion dynamics while baselines exhibit diminished dynamics and weaker alignment*

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison on long-range temporal consistency. Reward Forcing maintains superior coherence over long-horizon, while baselines suffer from noticeable quality degradation and inconsistency over time*

### 消融实验

Table 3 系统拆解了各模块的贡献。以完整 Reward Forcing 为基准（动态得分 64.06，运动平滑度 98.82，漂移 1.77）：

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/008_Table_3.jpg]]
*Table 3: Ablation studies on key components. The best results for the “Improvement” module are indicated in bold*

- **移除 Re-DMD 训练**：动态得分骤降至 43.75，证明奖励加权分布匹配是驱动高动态生成的核心机制。
- **进一步移除 EMA-Sink**：动态得分继续下滑至 35.15，运动平滑度从 98.91 降至 98.64，说明 EMA-Sink 对维持运动流畅性不可或缺。
- **完全去除 Sink Token**：生成质量出现显著退化，验证了压缩全局状态对长视频一致性的基础作用。

超参数分析表明，EMA 系数 $\alpha = 0.99$ 时取得运动平滑度 98.96 与漂移 2.52 的最优平衡；奖励权重 $\beta = 1/2$ 在动态得分、一致性与美学质量之间达到最佳折中。训练动态曲线（Figure 6 右）显示，Re-DMD 训练过程中动态得分持续上升，验证了奖励信号对生成分布的有效引导。

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/009_Figure_6.jpg]]
*Figure 6: (Left) Ablation study on our proposed module, showing qualitative improvement. (Right) Top: Reward Forcing training leads to a steady rise in the dynamic score. Bottom: The plot of attention size versus FPS underscores the source of our inference efficiency*

### 失败模式与局限性

尽管 Reward Forcing 在动态性上取得显著提升，仍存在若干值得关注的失败模式：

1. **奖励模型与评测标准的对齐偏差**：当前视频奖励模型可能过度强调某一维度（如时序一致性），而相对忽视美学质量等其他维度，导致奖励提升未能等比例转化为 VBench 综合得分的增长。这反映出单一奖励函数在多目标视频质量评估中的局限性。

2. **长程伪影捕捉不足**：现有视觉语言模型奖励函数仍难以完美检测微小时序伪影（如帧间抖动）和复杂语义属性，限制了奖励导向优化的上限。

3. **对奖励模型质量的强依赖**：若奖励模型本身存在偏差，Re-DMD 的加权机制可能放大不公平或欠代表性问题。该发现提示未来工作需探索多目标奖励建模与人类反馈集成。

### 补充图表

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/010_Figure_7.jpg]]
*Figure 7: Interactive video generation. Reward Forcing supports real-time prompt interaction with seamless transitions*

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/013_Table_4.jpg]]
*Table 4: Average User Rating*

![[assets/figures/papers/paper_list_l2291_https_arxiv_org_abs_2512_04678/figures/015_Table_6.jpg]]
*Table 6: Quality evaluation on extended VBench*



## 定位与知识库关联

### 1. 与基线方法的关系

Reward Forcing 的核心贡献建立在两条技术路线的交叉点上：**自回归流式视频生成** 与 **分布匹配蒸馏（DMD）**。其直接基线可沿以下维度定位。

**相对于自回归生成基线。** 流式视频生成的主流范式是滑动窗口注意力配合静态 Sink Token，典型代表为 **LongLive**。该方案将初始帧固定为注意力沉没令牌，全程不变，导致模型过度依赖首帧、运动动态性严重退化。Reward Forcing 提出的 **EMA-Sink** 模块从根本上改变了这一机制：通过指数移动平均将逐出窗口的 KV 对持续融合进固定大小的压缩状态中（公式见 Eq. 4–5），既保留了全局上下文，又引入了近期动态信息，打破了首帧依赖瓶颈。消融实验（Table 3）证实，移除 EMA-Sink 后动态得分从 64.06 骤降至 35.15，运动平滑度从 98.91 降至 98.64，验证了该模块对运动质量的关键作用。

**相对于蒸馏训练基线。** 在训练范式上，Reward Forcing 继承 **Self Forcing** 的自回滚机制（训练与推理对齐），但对其蒸馏目标函数进行了根本性改造。标准 DMD 对所有样本均等加权，无法区分高动态与低动态样本。Reward Forcing 引入 **Re-DMD**，利用视觉语言模型作为奖励函数评定样本的运动质量，对高动态样本赋予更高的分布匹配梯度权重（Eq. 10–11），使生成分布向高奖励区域偏移。这一设计将强化学习的偏好优化思想与分布匹配蒸馏相结合，在不牺牲保真度的前提下有效提升视频动态性。消融实验表明，移除 Re-DMD 训练后动态得分从 64.06 降至 43.75（Table 3），验证了奖励加权的核心贡献。

**相对于早期蒸馏方法。** 与 **CausVid** 等早期因果蒸馏方法相比，Reward Forcing 在训练-推理对齐（Self Forcing 机制）、状态压缩（EMA-Sink）和优化目标（Re-DMD）三个维度上均有实质性改进，形成了完整的流式生成方案。

**相对于联合去噪基线。** **Rolling Forcing** 采用联合去噪多帧生成，而 Reward Forcing 的自回归逐帧生成在推理效率上具有天然优势，配合 KV Cache 与滑动窗口注意力实现了 O(1) 令牌逐出和恒定内存占用，达到 23.1 FPS 的实时推理速度。

### 2. 适用边界

**场景适用性。** Reward Forcing 主要面向流式文本到视频生成场景，支持短视频（5 秒）和长视频（60 秒以上）生成，并支持实时提示词交互（Figure 7）。其流式架构天然适合需要低延迟、持续输出的应用，如交互式内容创作、实时视频流生成等。

**模型规模约束。** 当前实现基于 **Wan2.1-T2V-1.3B**（开源基础模型），蒸馏为学生模型后达到 23.1 FPS（单张 H100 GPU）。方法的核心机制（EMA-Sink、Re-DMD）在原理上可推广至更大规模的视频扩散模型，但奖励模型的质量和推理开销可能成为扩展瓶颈。

**动态性提升的边界。** 在 VBench Long 评测中，Reward Forcing 将动态得分从 LongLive 的 35.54 大幅提升至 66.95（+88.38%），同时质量漂移最小（2.505 vs. 2.531）。这表明方法在保持时序一致性的前提下有效增强了运动幅度，但动态得分的绝对水平仍受限于基础模型的生成能力和奖励模型的判别精度。

### 3. 局限与开放问题

**局限。** 论文明确指出的局限包括：（1）当前视频奖励模型的优化方向可能与 VBench 综合评价标准不完全对齐，可能过度强调某一维度（如时序一致性）而相对忽视其他维度（如美学质量），导致奖励提升未能等比例转化为 VBench 得分；（2）视频奖励模型仍难以完美捕捉长程时序依赖、微小时序伪影（如帧抖动）以及复杂语义属性，限制了奖励导向优化的上限；（3）本方法对奖励模型的质量有较强依赖，若奖励模型存在偏差，可能放大不公平或欠代表性问题。

**开放问题。** 从方法设计和实验结果中可提炼出以下开放方向：（1）如何设计能够更好捕捉长程时间依赖和细微抖动等伪影的奖励模型？（2）如何通过多目标奖励建模平衡视频质量的各个维度？（3）如何集成人类反馈环节，使奖励模型更贴近人的感知判断？（4）EMA-Sink 中的动量衰减系数 $\alpha$ 如何在不同场景下自适应调整以兼顾平滑性与动态性？（当前 $\alpha = 0.99$ 在运动平滑度 98.96 与漂移 2.52 间取得最优平衡，但该参数对不同运动幅度场景的敏感性尚需进一步研究。）

### 4. 知识库定位

Reward Forcing 在视频生成知识库中的定位可概括为：**将强化学习中的奖励引导思想引入分布匹配蒸馏，同时通过状态压缩机制解决自回归长视频生成中的信息瓶颈**。其方法论贡献位于以下交叉领域：

- **视频扩散模型蒸馏**：继承 DMD 框架，创新性地引入奖励加权（Re-DMD），将偏好优化与分布匹配统一。
- **自回归长视频生成**：提出 EMA-Sink 作为滑动窗口注意力的状态打包方案，解决了静态 Sink Token 导致的运动退化问题。
- **流式推理系统**：通过 KV Cache + 滑动窗口 + O(1) 令牌逐出实现恒定内存与实时推理，为流式视频生成提供了高效推理范式。

该方法为后续工作提供了两个可独立复用的模块（EMA-Sink 与 Re-DMD），并开辟了“奖励驱动的分布匹配蒸馏”这一研究方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Reward_Forcing_Efficient_Streaming_Video_Generation_with_Rewarded_Distribution_Matching_Distillation.pdf]]

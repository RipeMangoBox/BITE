---
title: "VideoJAM: Joint Appearance-Motion Representations for Enhanced Motion Generation in Video Models"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Generation_in_Video_Models.pdf
project_link: https://hila-chefer.github.io/videojam-paper.github.io/
code_link: https://github.com/genmoai/
aliases:
- VideoJAM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在训练阶段显式引入光流运动表示作为额外预测目标，并在推理阶段使用模型自身生成的运动预测进行内部引导（Inner-Guidance），为生成模型注入运动先验。
primary_logic: 仅添加两个线性层即可将标准视频生成器改造为双输入双输出架构，学习单一的联合外观-运动潜在表示，从而在不增加数据与模型规模的条件下大幅提升运动连贯性。
claims:
- 原始 DiT 模型对帧顺序扰动几乎不敏感，直到去噪步骤 60 损失变化极小，表明像素目标无法捕获时序信息。
- VideoJAM 模型对时间扰动高度敏感，损失差异显著，证明运动目标显式参与训练。
- 在 VideoJAM-bench 上，VideoJAM-30B 在运动评分上分别以 68.5% 和 63.8% 的人类投票率显著优于 Sora 和 Kling 1.5。
- 移除运动引导或推理时光流输入导致运动连贯性大幅下降，验证运动表示和 Inner-Guidance 的关键作用。
---

# VideoJAM: Joint Appearance-Motion Representations for Enhanced Motion Generation in Video Models

> [!tip] 核心洞察
> 仅添加两个线性层即可将标准视频生成器改造为双输入双输出架构，学习单一的联合外观-运动潜在表示，从而在不增加数据与模型规模的条件下大幅提升运动连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoJAM：联合外观-运动表示增强视频运动生成 |
| 英文题名 | VideoJAM: Joint Appearance-Motion Representations for Enhanced Motion Generation in Video Models |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://hila-chefer.github.io/videojam-paper.github.io/) · [Code](https://github.com/genmoai/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoJAM |
| Dataset | VideoJAM-bench, Movie Gen benchmark |

> [!tip] 效果简介
> - VideoJAM-bench 上，Human Eval Motion (视频对比中 VideoJAM 获胜百分比) 96.1% vs CogVideo2B；Human Eval Motion 82.0% vs DiT-4B；Auto. Metric Motion (VBench) 93.7 vs DiT-4B (78.3) (+15.4)。
> - Movie Gen benchmark 上，Human Eval Motion 100% vs DiT-30B (0%)。

## 概要

**核心问题**：当前主流视频生成模型（扩散模型或自回归模型）的训练目标几乎完全围绕像素级重建损失设计。这导致模型过度优化外观质量，却缺乏对时序动态和物理运动规律的显式建模能力。其直接后果是生成的视频频繁出现运动不连贯、违背基本物理定律（如人物穿透物体、重复同一动作帧）等系统性失败（Figure 2）。

**核心发现与动机**：通过对基础 DiT 模型进行帧顺序随机置换实验，作者发现：原始模型在去噪步骤 60 之前对时序扰动几乎完全不敏感——置换帧前后的损失值差异极小。这表明标准像素重建目标无法有效捕获视频中的时序运动信息（Figure 3）。这一发现直接揭示了现有视频生成范式的根本瓶颈。

**解决方案**：VideoJAM 提出了一种极简而高效的框架，核心理念是**为视频生成模型注入显式的运动先验**。具体而言，该方法仅需在标准视频扩散模型（DiT）上添加两个线性投影层，将其改造为双输入双输出架构：训练时同时接收视频和光流运动表示作为输入，并同时预测外观和运动两个目标，从而学习单一的联合外观-运动潜在表示。推理时，引入 **Inner-Guidance** 机制，利用模型自身在每个去噪步骤中产生的运动预测作为动态引导信号，调整采样分布以增强运动连贯性。

**关键结果**：
- 在 VideoJAM-bench 上，VideoJAM-30B 在人类评估的运动偏好投票中分别以 **68.5%** 和 **63.8%** 的显著优势击败商业模型 Sora 和 Kling 1.5（Table 2）。
- 在 Movie Gen benchmark 上，VideoJAM-30B 的运动人类偏好达到 **100%**，而基线 DiT-30B 为 0%（Table 7）。
- 消融实验证实，移除 Inner-Guidance 导致运动偏好从 96.1% 骤降至 66.2%；推理时丢弃光流输入则降至 80.2%，验证了运动表示与引导机制的关键作用（Table 3）。

**方法定位**：VideoJAM 属于训练阶段注入运动先验、推理阶段自引导增强的方法。其显著优势在于**不需要额外数据、不增加模型规模**，仅通过修改输入输出投影层和损失函数即可将运动连贯性大幅提升至超越商业闭源模型的水平。

### 视频生成中的运动连贯性困境

文本到视频生成模型近年来取得了显著进展，以 **Sora**（Brooks et al., 2024）、**Kling 1.5**（KlingAI, 2024）、**RunWay Gen3**（RunwayML, 2024）为代表的商业模型，以及 **CogVideo**（Hong et al., 2022）、**Mochi**（Genmo, 2024）、**PyramidFlow**（Jin et al., 2024a）等开源模型，在视觉质量上不断刷新记录。然而，一个核心瓶颈始终未被有效突破：**运动连贯性不足**。

现有模型虽然在单帧外观上表现出色，但在时序维度上频繁出现违背物理规律的生成结果。如 Figure 2 所示，基于 **DiT**（Peebles & Xie, 2023）的 30B 参数模型在基础运动上也会反复出错——跑步时重复迈出同一条腿；在复杂运动中，体操动作出现不自然的形变；在物理交互场景中，呼啦圈直接穿过人体；在旋转运动中，无法复现简单的周期性模式。这些失败并非个例，而是系统性缺陷的体现。

### 根本原因：像素重建目标对时序信息的忽视

这一困境的根源在于当前视频生成模型的训练范式。主流方法采用扩散模型或流匹配（Flow Matching）框架，其训练目标是最小化预测噪声与真实噪声之间的像素级重建误差。这种目标函数天然倾向于优化外观质量——颜色、纹理、边缘的精确还原——却无法显式捕捉帧与帧之间的运动时序关系。

论文通过一个关键动机实验（Figure 3）直观地揭示了这一问题：对标准 DiT 模型，将视频帧随机打乱顺序后重新计算损失，在去噪步数 $t \leq 60$ 的范围内，损失值几乎不变。这意味着**模型对帧的时序排列完全不敏感**——无论视频是正向播放还是随机乱序，模型都给出相似的预测。直到去噪后期（$t > 60$），当时序结构已基本确定时，损失才出现微小差异。这一发现直接证明：像素重建目标无法在生成过程中注入运动先验，模型实际上是在“盲生成”时序内容。

### 现有方法的缺口

针对运动连贯性问题，已有工作主要沿两条路径探索：

**1. 扩大数据与模型规模**：通过增加训练数据量和模型参数量来隐式学习运动模式。然而，Figure 2 中的 DiT-30B 和 Figure 6 中 Sora、Kling 1.5 的失败案例表明，单纯扩展规模无法根治问题——即使是顶级商业模型，在基础运动（如走路、跑步）上仍会出现“倒退行走”或“不自然运动”等低级错误。

**2. 推理时引导（Inference-time Guidance）**：在生成过程中引入额外的运动信号或约束。这类方法的问题在于，基础模型本身缺乏运动感知能力，外部引导信号与模型内部表示之间存在语义鸿沟，引导效果有限且不稳定。

### 本文动机：为生成模型注入显式运动先验

VideoJAM 的核心动机源于一个关键洞察：**运动连贯性不应是模型规模扩大后的“涌现”产物，而应是训练目标中显式编码的结构性先验**。

具体而言，论文提出两个基本假设：
1. 如果在训练阶段让模型同时学习预测外观和运动，模型将被迫学习一个包含时序信息的联合表示，从而从根本上解决对帧顺序不敏感的问题。
2. 如果在推理阶段利用模型自身生成的运动预测来动态引导采样过程，可以在不引入外部模型的前提下，将运动先验有效传递到最终生成结果中。

基于这两个假设，VideoJAM 设计了一个轻量级框架——仅需添加两个线性投影层，即可将任意视频扩散模型改造为双输入双输出架构，在几乎不增加计算开销的条件下，大幅提升运动连贯性。后续章节将详细阐述其技术实现与实验验证。

## 核心方法与创新机理

VideoJAM 的核心创新在于**将运动先验显式注入视频扩散模型的训练与推理过程**，仅需极小的架构改动即可大幅提升生成视频的运动连贯性。其本质是通过三个**changed slots**（输入投影层、输出投影层、训练损失函数）将标准视频生成器改造为**双输入双输出架构**，并引入**Inner-Guidance**推理机制，在不增加数据与模型规模的条件下解决了传统像素重建目标对时序信息不敏感的瓶颈。

### 1. 瓶颈洞察：像素目标无法捕获时序信息

传统视频扩散模型（如 **DiT**，Peebles & Xie, 2023）仅以像素重建作为训练目标，模型过度关注单帧外观质量，对帧间时序关系几乎无感知。VideoJAM 通过动机实验（Figure 3）揭示了这一根本缺陷：对原始 DiT 模型随机打乱视频帧顺序后，在去噪步骤 $t \leq 60$ 的范围内损失值几乎不变，表明模型对时间扰动近乎不敏感。这一发现构成了 VideoJAM 设计的因果起点——**必须引入显式的运动信号作为训练目标**，才能迫使模型学习时序依赖。

### 2. 架构改造：双输入双输出的最小化改动

VideoJAM 对基础 DiT 架构的改动极为克制，仅涉及两个线性投影层的扩展：

- **输入投影层 $\mathbf{W}_{\text{in}}^+$**：原始 DiT 仅投影视频 patch。VideoJAM 在 $\mathbf{W}_{\text{in}}$ 基础上增加 $C_{\text{TAE}} \cdot p^2$ 行零向量，使其能够同时接收视频潜在表示 $\mathbf{x}_t$ 和光流潜在表示 $\mathbf{d}_t$ 的拼接，将两者映射到统一的联合潜在空间（Section 4.2, Figure 4(a)）。

- **输出投影层 $\mathbf{W}_{\text{out}}^+$**：原始 DiT 仅输出视频预测。VideoJAM 将输出头扩展为双重输出 $\mathbf{u}^+ = [\mathbf{u}^x, \mathbf{u}^d]$，前部通道预测外观（视频），后部通道预测运动（光流），从同一联合表示中同时恢复两个模态（Section 4.2, Figure 4(a)）。

- **训练损失函数**：从标准 Flow Matching 损失 $\mathcal{L} = \mathbb{E} \left[ || \mathbf{u}(\mathbf{x}_t, y, t; \theta) - \mathbf{v}_t ||_2^2 \right]$（Eq. 3）扩展为联合外观-运动损失 $\mathcal{L} = \mathbb{E} \left[ || \mathbf{u}^+([\mathbf{x}_t, \mathbf{d}_t], y, t; \theta') - \mathbf{v}_t^+ ||_2^2 \right]$（Eq. 6），显式要求模型同时预测视频和光流的速度目标。

这种设计的核心洞察在于：**通过共享同一个联合潜在表示，模型被迫学习外观与运动的耦合关系**，而非将两者视为独立任务。

### 3. 推理创新：Inner-Guidance 动态引导

标准无分类器引导（CFG）仅利用文本条件调整采样分布，无法针对运动连贯性进行定向优化。VideoJAM 提出 **Inner-Guidance**（Section 4.3, Figure 4(b)），利用模型自身在每一步生成的运动预测作为动态引导信号，修改采样分布为：

$$\tilde{p}_{\theta'}([\mathbf{x}_t, \mathbf{d}_t]|y) \propto p_{\theta'}([\mathbf{x}_t, \mathbf{d}_t]|y) \, p_{\theta'}(y|[\mathbf{x}_t, \mathbf{d}_t])^{w_1} \, p_{\theta'}(\mathbf{d}_t|\mathbf{x}_t, y)^{w_2}$$

对应的推理时预测公式为：

$$\tilde{\mathbf{u}}^{+}([\mathbf{x}_t, \mathbf{d}_t], y, t; \theta') = (1 + w_1 + w_2) \cdot \mathbf{u}^{+}([\mathbf{x}_t, \mathbf{d}_t], y, t; \theta') - w_1 \cdot \mathbf{u}^{+}([\mathbf{x}_t, \mathbf{d}_t], \varnothing, t; \theta') - w_2 \cdot \mathbf{u}^{+}([\mathbf{x}_t, \varnothing], y, t; \theta')$$

其中 $w_1=5$ 控制文本引导强度，$w_2=3$ 控制运动引导强度（默认设置）。Inner-Guidance 的关键特性在于：**运动引导信号来自模型自身的实时预测，无需外部模型或额外训练**，实现了“自举式”的运动质量提升。

### 4. 创新有效性验证

消融实验（Table 3）系统验证了各 changed slots 的独立贡献：

- **完全移除 Inner-Guidance（$w_2=0$）**：人类运动偏好从完整模型的基准降至 66.2%，证明运动引导对生成质量的巨大影响。
- **推理时丢弃光流输入（$\mathbf{d}=0$）**：运动性能降至最低（人类偏好 80.2%），验证了运动表示在推理过程中的关键作用。
- **替换为 IP2P 引导**：自动运动评分从 93.7 降至 90.4，说明 Inner-Guidance 的独特有效性并非任意引导机制可替代。

在 VideoJAM-bench 上，VideoJAM-30B 在运动评分上分别以 68.5% 和 63.8% 的人类投票率显著优于商业模型 Sora 和 Kling 1.5（Table 2），以仅增加两个线性层的代价实现了对大规模商业模型的超越，充分证明了“显式运动先验注入”这一创新路径的有效性。

VideoJAM 的整体设计遵循一个核心原则：**将运动信息显式地注入视频扩散模型的训练与推理全过程**。该框架由两个协同单元构成——训练阶段的联合外观-运动学习与推理阶段的内部运动引导（Inner-Guidance），其整体架构如图 Figure 4 所示。

![[assets/figures/papers/paper_list_l1838_VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Gen/figures/004_Figure_4.jpg]]
*Figure 4: VideoJAM Framework. VideoJAM is constructed of two units; (a) Training. Given an input video*

### 训练管线

训练管线的输入为一对数据：原始视频 $x_1$ 及其对应的运动表示 $d_1$。运动表示通过离线光流提取器 **RAFT** 从训练视频中预先计算，并转换为 RGB 格式以便与视频共享同一编码器。两路信号分别经过相同的加噪过程（Flow Matching 框架下的线性插值，$x_t = t x_1 + (1-t) x_0$，$d_t = t d_1 + (1-t) d_0$），随后进入**时空自编码器（Temporal Auto-Encoder, TAE）** 压缩到潜在空间。

关键改造在于 DiT 骨干网络的输入输出层：
- **双输入线性层 $W_{in}^+$**：将视频潜在表示与光流潜在表示拼接后投影到 DiT 的隐藏维度。实现方式是在原始 $W_{in}$ 矩阵上添加 $C_{TAE} \cdot p^2$ 行零行，使其能够接收双倍通道的输入（Section 4.2, Figure 4(a)）。
- **DiT 骨干网络**：基于 Transformer 的视频扩散主干，处理联合潜在表示，学习外观与运动的统一表征。
- **双输出线性层 $W_{out}^+$**：从 DiT 输出中并行预测两个分量——视频预测 $\mathbf{u}^x$ 和光流预测 $\mathbf{u}^d$，构成联合输出 $\mathbf{u}^+ = [\mathbf{u}^x, \mathbf{u}^d]$。

训练损失从标准 Flow Matching 损失（Eq. 3）扩展为**联合外观-运动损失**（Eq. 6）：
$$\mathcal{L} = \mathbb{E}_{[x_1,d_1],[x_0,d_0],y,t} \left[ || \mathbf{u}^+([x_t,d_t],y,t;\theta') - \mathbf{v_t^+} ||_2^2 \right]$$
其中 $\mathbf{v_t^+} = [x_1 - x_0, d_1 - d_0]$ 为联合速度目标。该损失迫使模型同时学习像素重建和运动预测，从而在单一联合潜在表示中编码外观与运动信息。

### 推理管线

推理阶段的核心创新是 **Inner-Guidance** 机制（Figure 4(b)）。与传统无分类器引导（CFG）仅利用文本条件不同，Inner-Guidance 利用模型自身每一步预测的运动信息来动态调整采样分布：
$$\tilde{p}_{\theta'}([x_t,d_t]|y) \propto p_{\theta'}([x_t,d_t]|y) \, p_{\theta'}(y|[x_t,d_t])^{w_1} \, p_{\theta'}(d_t|x_t,y)^{w_2}$$

实际推理时，模型预测由三项加权组合而成（Section 4.3, Eq. after Eq. 8）：
$$\tilde{\mathbf{u}}^{+}([x_t, d_t], y, t; \theta') = (1 + w_1 + w_2) \cdot \mathbf{u}^{+}([x_t, d_t], y, t; \theta') - w_1 \cdot \mathbf{u}^{+}([x_t, d_t], \varnothing, t; \theta') - w_2 \cdot \mathbf{u}^{+}([x_t, \varnothing], y, t; \theta')$$

其中 $w_1=5$ 控制文本引导强度，$w_2=3$ 控制运动引导强度。第三项 $\mathbf{u}^{+}([x_t, \varnothing], y, t; \theta')$ 表示丢弃光流输入时模型仅基于视频和文本的预测，将其从条件预测中减去，等效于增强运动条件 $d_t$ 对生成结果的约束力。

### 输入输出流总结

| 阶段 | 输入 | 处理模块 | 输出 |
|------|------|----------|------|
| 训练 | 视频 $x_1$ + 光流 $d_1$ + 文本 $y$ | TAE → $W_{in}^+$ → DiT → $W_{out}^+$ | 视频预测 $\mathbf{u}^x$ + 光流预测 $\mathbf{u}^d$ |
| 推理 | 噪声 + 文本 $y$ | TAE → $W_{in}^+$ → DiT → $W_{out}^+$ → Inner-Guidance | 去噪视频 |

值得注意的是，整个框架仅需**添加两个线性层**（$W_{in}^+$ 和 $W_{out}^+$）即可将标准视频生成器改造为双输入双输出架构，无需修改 DiT 骨干网络本身，也无需增加数据规模或模型参数量。这种轻量级设计使得 VideoJAM 可以即插即用地应用于各类基于 DiT 的视频生成模型。

### 4.1 时空压缩与 Flow Matching 基础

VideoJAM 构建在基于 Transformer 的扩散主干网络 **DiT**（Peebles & Xie, 2023）之上，使用 **Temporal Auto-Encoder (TAE)** 对视频进行时空压缩编码，将视频和光流映射到统一的潜在空间（Section 4.1）。

训练采用 **Flow Matching** 框架。给定干净视频潜在表示 $x_1$ 和噪声 $x_0 \sim \mathcal{N}(0,1)$，通过时间 $t$ 线性插值得到噪声化潜在表示：

$$x_t = t x_1 + (1 - t) x_0$$

模型需要预测从噪声到干净视频的速度（velocity），即两者的差值：

$$v_t = \frac{d x_t}{d t} = x_1 - x_0$$

标准 Flow Matching 的训练损失为：

$$\mathcal{L} = \mathbb{E}_{x_1, x_0 \sim \mathcal{N}(0,1), y, t} \left[ || u(x_t, y, t; \theta) - v_t ||_2^2 \right]$$

其中 $u(\cdot; \theta)$ 为模型预测的速度场，$y$ 为文本条件。该损失仅约束像素空间的外观重建，缺乏对运动时序信息的显式监督。

### 4.2 联合外观-运动训练：双输入双输出架构

VideoJAM 的核心改造是将标准 DiT 扩展为**双输入双输出**架构，仅需修改两个线性投影层（Figure 4a）：

**运动表示。** 使用离线 **RAFT** 模型从训练视频中提取光流作为运动标签 $d_1$。光流通过归一化转换为 RGB 图像格式以适配 TAE 编码器：

$$m = \min\left\{1, \frac{\sqrt{u^2+v^2}}{\sigma \sqrt{H^2+W^2}}\right\}, \quad \alpha = \arctan2(v,u)$$

其中 $m$ 为归一化幅度，$\alpha$ 为运动方向，$\sigma$ 为缩放因子。

**输入投影层 $W_{in}^+$。** 将原始输入投影矩阵 $W_{in}$ 扩展为 $W_{in}^+$：在原有视频潜在投影的基础上添加 $C_{TAE} \cdot p^2$ 行零行，使模型能够同时接收噪声视频 $x_t$ 和噪声光流 $d_t$ 的拼接输入，将其嵌入到单一的联合潜在表示中。

**输出投影层 $W_{out}^+$。** 将原始输出投影矩阵 $W_{out}$ 扩展为 $W_{out}^+$：增加输出通道以同时预测外观（视频）和运动（光流）。双输出记为 $\mathbf{u}^+ = [u^x, u^d]$，前部通道为视频预测，后部通道为光流预测。

**联合训练损失。** 扩展后的损失函数同时约束外观和运动预测：

$$\mathcal{L} = \mathbb{E}_{[x_1,d_1],[x_0,d_0],y,t} \left[ || \mathbf{u}^+([x_t,d_t],y,t;\theta') - \mathbf{v_t^+} ||_2^2 \right]$$

其中 $\mathbf{v_t^+} = [x_1 - x_0, d_1 - d_0]$ 为扩展的速度目标。该损失使模型从单一的联合潜在表示中同时学习外观和运动信息，无需增加数据规模或模型容量。

### 4.3 Inner-Guidance：推理时的运动引导机制

推理阶段，VideoJAM 提出 **Inner-Guidance** 机制，利用模型自身生成的运动预测动态调整采样分布，无需额外训练或外部模型（Figure 4b）。

**核心思想。** 修改采样分布以提高文本条件似然和运动条件似然：

$$\tilde{p}_{\theta'}([x_t,d_t]|y) \propto p_{\theta'}([x_t,d_t]|y) \; p_{\theta'}(y|[x_t,d_t])^{w_1} \; p_{\theta'}(d_t|x_t,y)^{w_2}$$

其中 $w_1$ 为文本引导尺度，$w_2$ 为运动引导尺度。对应的条件分数函数为：

$$(1+w_1+w_2) \nabla_{\theta'} \log p_{\theta'}([x_t,d_t]|y) - w_1 \nabla_{\theta'} \log p_{\theta'}([x_t,d_t]) - w_2 \nabla_{\theta'} \log p_{\theta'}(x_t|y)$$

**推理实现。** 实际推理时，模型预测由三项组合而成：

$$\tilde{\mathbf{u}}^{+}([x_t, d_t], y, t; \theta') = (1 + w_1 + w_2) \cdot \mathbf{u}^{+}([x_t, d_t], y, t; \theta') - w_1 \cdot \mathbf{u}^{+}([x_t, d_t], \varnothing, t; \theta') - w_2 \cdot \mathbf{u}^{+}([x_t, \varnothing], y, t; \theta')$$

- 第一项：同时条件于文本 $y$ 和光流 $d_t$ 的预测。
- 第二项：无条件预测（文本置空 $\varnothing$），实现标准无分类器引导。
- 第三项：仅条件于文本、光流置空的预测，通过减去该分量增强运动一致性。

默认引导尺度为 $w_1 = 5, w_2 = 3$，其中 $w_1 = 5$ 为基础模型的文本引导尺度。Inner-Guidance 的关键创新在于：每一步推理中，模型使用自身当前预测的噪声光流 $d_t$ 作为运动条件，形成自循环的动态引导，无需外部运动提取器。

### 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|---------|------|
| $x_t = t x_1 + (1-t)x_0$ | $x_1$：干净视频，$x_0$：噪声，$t$：时间步 | 前向加噪 |
| $v_t = x_1 - x_0$ | 速度目标 | 训练预测目标 |
| $m = \min\{1, \frac{\sqrt{u^2+v^2}}{\sigma\sqrt{H^2+W^2}}\}$ | $u,v$：光流分量，$H,W$：帧尺寸 | 光流归一化幅度 |
| $\mathbf{u}^+ = [u^x, u^d]$ | $u^x$：外观预测，$u^d$：运动预测 | 双输出结构 |
| $\tilde{\mathbf{u}}^{+} = (1+w_1+w_2)\mathbf{u}^{+}_{y,d_t} - w_1\mathbf{u}^{+}_{\varnothing,d_t} - w_2\mathbf{u}^{+}_{y,\varnothing}$ | $w_1$：文本引导尺度，$w_2$：运动引导尺度 | Inner-Guidance 推理 |

## 实验与关键发现

### 核心发现：运动连贯性的量化飞跃

VideoJAM 的核心实验结论是：在完全不增加模型参数规模与训练数据的条件下，仅通过引入联合外观-运动训练目标和 Inner-Guidance 推理机制，即可在运动连贯性上实现跨量级的提升，甚至显著超越参数量更大的商业级模型。

**瓶颈验证实验（Figure 3）** 为整个方法提供了坚实的动机锚点。实验对标准 DiT 模型和 VideoJAM 微调模型分别进行帧顺序随机置换，并观察损失变化。结果显示，原始 DiT 模型在去噪步数 $t \leq 60$ 之前，对时序扰动几乎完全不变（损失差异极小），这直接证明了像素重建目标无法有效捕获时序信息，模型在生成早期对运动结构几乎没有约束。相比之下，VideoJAM 模型对帧置换表现出极高的损失敏感性，差异显著，证实运动目标已显式参与训练并形成了强时序先验。

### 主实验结果

**4B 规模模型（Table 1）**：在 VideoJAM-bench 上，VideoJAM-4B 在人类评估的运动偏好中，以 96.1% 的投票率碾压 CogVideo2B，以 82.0% 的投票率显著优于其基础模型 DiT-4B。自动指标方面，VBench 运动评分从 DiT-4B 的 78.3 跃升至 93.7（+15.4），提升幅度巨大。值得注意的是，VideoJAM-4B 甚至超越了参数量为其 1.25 倍的 CogVideo5B。

**30B 规模模型（Table 2）**：VideoJAM-30B 在与顶级商业模型的直接对比中展现出惊人的竞争力。在 VideoJAM-bench 人类运动偏好评估中，VideoJAM-30B 分别以 68.5% 和 63.8% 的投票率显著优于 Sora 和 Kling 1.5，以 77.3% 优于 RunWay Gen3，以 74.2% 优于 Mochi。自动指标上，VBench 运动评分从 DiT-30B 的 88.1 提升至 92.4（+4.3）。在 Movie Gen benchmark（Table 7）上，VideoJAM-30B 在人类运动偏好评估中取得 100% 的压倒性优势（DiT-30B 为 0%），进一步验证了方法的跨基准泛化能力。

**外观-运动平衡（Table 4-6, 8）**：VBench 的细粒度分解揭示了 VideoJAM 的关键优势——在动态程度（Dynamic Degree）和运动平滑度（Motion Smoothness）之间取得了最优平衡。Table 6 进一步显示，VideoJAM-30B 相比 DiT-30B 在 VBench 的几乎所有自动指标上均有提升，证明运动增强并未以牺牲外观质量为代价。

### 消融实验：因果链的严格验证

Table 3 的消融实验系统拆解了 VideoJAM 各组件的贡献：

![[assets/figures/papers/paper_list_l1838_VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Gen/figures/010_Table_3.jpg]]
*Table 3: Ablation study. Ablations of the primary components of our framework on VideoJAM-4B using VideoJAM-bench. Human evaluation shows percentage of votes favoring VideoJAM*

1. **移除文本引导（$w_1=0$）**：自动运动评分从 93.7 小幅降至 93.3，但人类运动偏好从 96.1% 骤降至 63.3%。这表明文本引导对运动质量有重要辅助作用，但仅靠文本条件远不足以保证运动连贯性。
2. **完全移除 Inner-Guidance（$w_2=0$）**：人类运动偏好降至 66.2%，证明运动引导信号是推理阶段运动质量的核心驱动力。
3. **推理时丢弃光流输入（$d=0$）**：这是性能下降最剧烈的消融设置，人类偏好降至 80.2%，验证了运动表示在推理过程中的关键作用——即使模型在训练时学习了运动预测能力，推理时若切断该信号通路，运动质量仍会大幅退化。
4. **替换为 IP2P 引导**：自动运动评分从 93.7 降至 90.4，说明 Inner-Guidance 利用模型自身运动预测进行动态引导的机制，优于外部预训练运动模型提供的引导信号。

### 失败模式与局限性

Figure 7 和论文讨论明确指出了 VideoJAM 的适用边界：

![[assets/figures/papers/paper_list_l1838_VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Gen/figures/009_Figure_7.jpg]]
*Figure 7: Limitations. Our method is less effective for: (a) motion observed in “zoom-out” (the moving object covers a small part of the frame). (b) Complex physics of object interactions*

- **放大场景（zoom-out）失效**：当运动物体占画面比例极小时，光流表示的相对运动幅度微弱，模型难以捕获有效运动信号。
- **复杂物体交互的物理违背**：如球未触脚而轨迹改变等场景，暴露了运动表示缺乏显式物理定律编码的根本局限——光流可以描述运动，但无法保证运动符合真实世界的碰撞、重力等约束。
- **分辨率与表示瓶颈**：受限于训练分辨率和 RGB 运动表示，远距离微小运动的连贯性难以保证。

这些失败模式指向了明确的研究缺口：如何在高分辨率下改善小物体运动捕获，以及如何将物理先验融入运动表示。

![[assets/figures/papers/paper_list_l1838_VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Gen/figures/007_Table_1.jpg]]
*Table 1: Comparison of VideoJAM-4B with prior work on VideoJAM-bench. Human evaluation shows percentage of votes favoring VideoJAM; automatic metrics use VBench*

![[assets/figures/papers/paper_list_l1838_VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Gen/figures/008_Table_2.jpg]]
*Table 2: Comparison of VideoJAM-30B with prior work on VideoJAM-bench. Human evaluation shows percentage of votes favoring VideoJAM; automatic metrics use VBench*

![[assets/figures/papers/paper_list_l1838_VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Gen/figures/016_Table_7.jpg]]
*Table 7: Comparison of VideoJAM-30B with prior work on the Movie Gen benchmark. Human evaluation shows percentage of votes favoring VideoJAM; automatic metrics use VBench*

## 定位与知识库关联

### 1. 核心瓶颈：像素重建目标的运动盲区

现有视频生成模型（如 **DiT** (Peebles & Xie, 2023)、**CogVideo** (Hong et al., 2022)、**Sora** (Brooks et al., 2024)）的训练目标几乎完全围绕像素级重建损失设计。这一设计导致了根本性的运动盲区：模型在去噪过程中过度关注单帧外观质量，而将时序动态视为次要的、隐式的建模副产品。

VideoJAM 通过一个简洁的动机实验（Figure 3）量化了这一缺陷：对原始 DiT 模型，随机打乱视频帧顺序后，在去噪步骤 $t \leq 60$ 的范围内，损失函数几乎不发生变化。这意味着模型在生成过程的绝大部分阶段对时序信息完全不敏感——它“看到”的只是一堆无序的图像集合，而非一个连贯的运动序列。相比之下，经过 VideoJAM 微调的模型对帧置换表现出极高的损失敏感性，证明运动信息已被显式编码到模型的联合表示中。

这一发现揭示了问题的本质：**不是模型容量不足，而是训练信号本身缺乏对运动的约束**。

### 2. 方法定位：联合外观-运动表示的轻量改造范式

VideoJAM 的核心设计哲学是“最小侵入性改造”——它不重新设计扩散主干网络，不增加额外数据，不扩大模型规模，而是通过两个关键改动将运动先验注入现有视频生成器：

| 改动维度 | 基线做法 | VideoJAM 做法 |
|---------|---------|--------------|
| 输入投影层 $\mathbf{W}_{in}$ | 仅投影视频 patch | 扩展为双输入矩阵 $\mathbf{W}_{in}^+$，同时接受视频与光流 latent 的拼接 (Figure 4a) |
| 输出投影层 $\mathbf{W}_{out}$ | 仅输出视频预测 | 扩展为双输出矩阵 $\mathbf{W}_{out}^+$，同时预测外观和运动 (Figure 4a) |
| 训练损失 | 仅像素损失 $\mathcal{L} = \mathbb{E}[||\mathbf{u}(x_t, y, t) - v_t||_2^2]$ | 联合外观-运动损失 $\mathcal{L} = \mathbb{E}[||\mathbf{u}^+([x_t, d_t], y, t) - \mathbf{v}_t^+||_2^2]$ (Eq. 6) |
| 推理引导 | 标准无分类器引导 (CFG) | Inner-Guidance：利用模型自身运动预测动态调整采样分布 (Eq. 7-8) |

**改动量极小**：仅需在 DiT 的输入和输出端各添加一个线性层（零行扩展），其余 Transformer 主干完全复用。这种设计使得 VideoJAM 可以无缝适配任何基于 DiT 架构的视频生成模型。

**运动表示的选择**：VideoJAM 采用 RAFT 离线计算的光流作为运动标签，并将其通过归一化映射为 RGB 图像（Eq. 5），从而可直接复用现有的时空自编码器 (TAE)，无需训练专用的运动编码器。

### 3. 与相关工作的关系

#### 3.1 与基于像素损失的基线模型

VideoJAM 直接对比的基线包括：
- **DiT-4B / DiT-30B** (Peebles & Xie, 2023)：纯像素训练目标，运动连贯性差（Figure 2 展示了跑步同腿重复、体操变形、物体穿透人体等典型失败）。
- **CogVideo2B / CogVideo5B** (Hong et al., 2022)：开源文本-视频模型，同样缺乏显式运动建模。
- **Sora** (Brooks et al., 2024)、**Kling 1.5** (KlingAI, 2024)、**RunWay Gen3** (RunwayML, 2024)：商业级模型，在 VideoJAM-bench 上的人类运动偏好投票中均显著低于 VideoJAM-30B（分别为 68.5%、63.8%、77.3% 的投票率偏向 VideoJAM，Table 2）。

关键结论：**即使是最强的商业模型，在运动连贯性上仍存在系统性缺陷**（如 Sora 出现“倒退行走”，Kling 出现“不自然运动”，Figure 6），而 VideoJAM 通过显式运动目标在 30B 参数规模下超越了它们。

#### 3.2 与运动注入方法

VideoJAM 的 Inner-Guidance 机制与传统的无分类器引导 (CFG) 和 Compositional Guidance 有本质区别：
- **标准 CFG**：通过提高文本条件似然 $p(y|x)$ 来增强文本-视频对齐，但无法直接约束运动。
- **Compositional Guidance**：假设条件独立 $p(x|c_1,...,c_n) \propto p(x)\prod_i p(c_i|x)$，但该假设在运动与外观高度耦合的场景下不成立。
- **Inner-Guidance**：直接利用模型自身对运动的预测 $p(d_t|x_t, y)$ 作为动态引导信号，修改采样分布为 $\tilde{p}_{\theta'}([x_t,d_t]|y) \propto p_{\theta'}([x_t,d_t]|y) p_{\theta'}(y|[x_t,d_t])^{w_1} p_{\theta'}(d_t|x_t,y)^{w_2}$ (Eq. 7)，在每一步去噪中同时考虑文本条件（$w_1$）和运动一致性（$w_2$）。

消融实验（Table 3）表明：将 Inner-Guidance 替换为 IP2P 引导会导致自动运动评分从 93.7 降至 90.4，验证了 Inner-Guidance 的独特有效性。

#### 3.3 与物理仿真方法的差异

VideoJAM 的运动表示（光流）是数据驱动的，**不包含显式的物理定律编码**（如碰撞检测、重力约束、动量守恒）。这使其区别于基于物理仿真器的方法。优点是通用性强，可处理任意运动类型；缺点是对于复杂物理交互（如球未触脚而轨迹改变）和远距离微小运动（“放大”场景）的处理能力有限（Figure 7）。

### 4. 适用边界与局限性

根据论文自身披露和实验证据，VideoJAM 的适用边界如下：

| 场景 | 表现 | 原因分析 |
|------|------|---------|
| 主体占画面比例较大的常规运动 | 显著优于基线（人类投票率 63.8%-96.1%） | 光流信号强度足够，运动目标有效 |
| “放大”拍摄场景（运动物体占画面比例小） | 性能下降 (Figure 7a) | 光流幅度归一化后信号微弱，难以提供有效运动约束 |
| 复杂物体间物理交互 | 处理能力有限 (Figure 7b) | 光流仅描述像素位移，不编码作用力、碰撞等物理语义 |
| 高分辨率远距离运动 | 受限于训练分辨率和 RGB 运动表示 | 光流在低分辨率 latent 空间中丢失细节 |

### 5. 开放问题

1. **高分辨率运动建模**：如何改善远距离小物体的运动连贯性？可能需要层次化运动表示或自适应分辨率的光流计算。

2. **物理定律的显式编码**：能否将碰撞、重力、刚体约束等物理先验融入运动表示中，而非纯数据驱动的光流？这可能是解决 Figure 7b 类失败的关键。

3. **长时序扩展**：VideoJAM 框架能否线性扩展到更长的视频序列（如分钟级）？光流计算和 Inner-Guidance 的计算开销是否会成为瓶颈？

4. **跨任务泛化**：联合外观-运动训练范式能否迁移到其他生成任务？例如图像编辑中的运动一致性保持、3D 生成中的时序连贯性等。

5. **多物体遮挡交互**：在严重遮挡场景下，光流信号本身存在歧义，如何保证运动一致性？可能需要引入物体级别的运动表示或自监督的遮挡推理。

## 原文 PDF

![[paperPDFs/arxiv_2025/VideoJAM_Joint_Appearance_Motion_Representations_for_Enhanced_Motion_Generation_in_Video_Models.pdf]]

---
title: WorldPlay Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/WorldPlay_Towards_Long_Term_Geometric_Consistency_for_Real_Time_Interactive_World_Modeling.pdf
project_link: null
code_link: https://github.com/Tencent-Hunyuan/HY-WorldPlay
aliases:
- WorldPlay
- HY-World-1.5
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过重构上下文记忆（Reconstituted Context Memory）动态构建时空记忆并采用时序重帧（Temporal Reframing）克服长程衰减，配合上下文强制（Context Forcing）在蒸馏过程中对齐教师和学生的记忆上下文，使得学生模型在少量去噪步骤下仍能保持长期几何一致性。
primary_logic: 在记忆感知的扩散模型中，通过重建记忆上下文并利用时序重帧将重要的远距离记忆“拉近”，再通过蒸馏时对齐记忆分布，可以有效保留长期空间信息，从而实现实时、长期一致的视频生成。
claims:
- WorldPlay 全模型在长期几何一致性测试（≥250 帧）上显著超越所有基线，PSNR 达 18.94，比最佳有记忆基线 Gen3C 高出 3.57 dB。
- 重构上下文记忆和时序重帧有效提升了长期一致性，移除上下文强制会使长期 PSNR 降低至 16.27。
- 上下文强制蒸馏使模型在仅 4 个去噪步骤（NFE=4）下即可达到接近 100 步教师模型的生成质量，并实现实时交互。
- Our long-term test set (≥250 frames), custom cycle trajectories 上 PSNR↑ = 18.94
---

# WorldPlay Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling

> [!tip] 核心洞察
> 在记忆感知的扩散模型中，通过重建记忆上下文并利用时序重帧将重要的远距离记忆“拉近”，再通过蒸馏时对齐记忆分布，可以有效保留长期空间信息，从而实现实时、长期一致的视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | WorldPlay：面向实时交互世界建模的长期几何一致性 |
| 英文题名 | WorldPlay Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.14614) · [Code](https://github.com/Tencent-Hunyuan/HY-WorldPlay) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | WorldPlay |
| Dataset | Our long-term test set (≥250 frames), custom cycle trajectories, Our short-term test set, Our long-term test set |

> [!tip] 效果简介
> - Our long-term test set (≥250 frames), custom cycle trajectories 上，PSNR↑ 18.94 vs 15.37 (Gen3C) (+3.57)。
> - Our short-term test set (61 frames) 上，PSNR↑ 21.92 vs 21.68 (Gen3C) (+0.24)。
> - Our long-term test set (≥250 frames) 上，SSIM↑ 0.585 vs 0.431 (Gen3C) (+0.154)。

## 概要

### 问题与瓶颈

交互式世界模型（interactive world model）需要在用户实时操控下持续生成视觉一致的视频流，但当前方法面临**实时生成速度**与**长期几何一致性**之间的根本性矛盾。蒸馏式方法虽然推理速度快，却缺乏长期记忆机制，导致场景在用户重返时发生不可逆的几何漂移；而基于显式三维记忆或隐式记忆的方法能保持一致性，却因计算开销过高而难以实现实时交互，且蒸馏困难。这一瓶颈使得低延迟与高一致性长期被视为互斥目标。

### 核心方法

WorldPlay 通过三个相互协同的机制打破上述僵局：

- **重构上下文记忆（Reconstituted Context Memory）**：动态地从历史帧中同时检索时序邻近和空间邻近的记忆块，构建一个紧凑的时空上下文集合，而非依赖固定窗口或纯视锥检索。
- **时序重帧（Temporal Reframing）**：丢弃绝对时序索引，为所有上下文帧重新分配相对位置编码，将远距离的关键空间记忆“拉近”到当前帧附近，从而抑制 Transformer 中的长程衰减和误差累积。
- **上下文强制蒸馏（Context Forcing）**：在教师（双向扩散模型）与学生（自回归模型）之间对齐记忆上下文分布，使学生在仅 4 个去噪步骤下即可逼近教师 100 步的生成质量，实现实时交互。

### 主要结果

在作者构建的长期几何一致性测试集（≥250 帧）上，WorldPlay 全模型取得 **PSNR 18.94 dB**，比最强有记忆基线 Gen3C 高出 **3.57 dB**（15.37 dB），SSIM 从 0.431 提升至 0.585。消融实验表明，移除上下文强制会使长期 PSNR 降至 16.27 dB；将时序重帧替换为标准 RoPE 则进一步降至 14.03 dB，验证了各模块的关键作用。蒸馏后的学生模型以 NFE=4 达到 PSNR 18.94 dB，在保持长期一致性的同时支持 720p 分辨率下 24 FPS 的流式交互。定性对比显示，WorldPlay 在真实场景、风格化场景及第三人称智能体控制等多种域上均展现出显著的泛化能力和重访一致性。

### 方法定位

WorldPlay 属于**记忆感知的自回归视频扩散模型**，其方法谱系可定位于：

- **无记忆的动作控制扩散模型**：如 CameraCtrl、SEVA、ViewCrafter、Matrix-Game-2.0、GameCraft 等，仅依赖当前动作和近期帧，缺乏长期记忆。
- **基于显式 3D 记忆的动作控制扩散模型**：如 Gen3C、VMem，通过维护三维表征保持一致性，但计算成本高，实时性受限。

WorldPlay 通过重构式记忆与上下文强制蒸馏，首次在通用域上同时实现长时域生成、灵活动作控制、实时交互与长期几何一致性（见 Table 1 的特性对比）。其核心改动槽位包括：双重动作表示（离散键 + 连续相机姿态）、重构上下文记忆构建、时序重帧位置编码、以及上下文强制蒸馏方法。



### 问题背景：交互式世界模型的实时性与一致性困境

世界模型旨在从高维感官输入中学习环境的内部表征，从而预测未来状态并支持交互式决策。在视觉领域，生成式世界模型已展现出从单张图像或文本提示出发、根据用户动作生成未来视频帧的能力。然而，一个根本性的瓶颈始终存在：**实时交互性与长期几何一致性难以兼得**。

所谓长期几何一致性，是指当用户在虚拟世界中导航并重返先前访问过的位置时，场景的几何结构、纹理细节和空间关系应保持连贯不变。这一需求对沉浸式交互体验至关重要，但现有方法在满足该需求时均存在显著折衷：

- **基于蒸馏的实时方法**：通过将计算密集的教师模型蒸馏为轻量级自回归学生模型，可以实现低延迟的流式生成。然而，这些方法缺乏有效的长期记忆机制，导致模型在生成新帧时逐渐遗忘早期场景信息，重返时出现几何漂移和纹理不一致。
- **基于显式或隐式记忆的方法**：通过维护 3D 点云、特征缓存或检索增强的记忆库来保留历史信息，能够在一定程度上缓解遗忘问题。但其高昂的计算和存储成本使得实时交互（如 24 FPS 下的 720p 流式生成）变得极为困难，且这类记忆感知模型通常难以通过标准蒸馏方法压缩为高效的学生模型。

这一困境的核心在于：**记忆的保留与计算的效率之间存在结构性冲突**。标准自回归 Transformer 中的绝对位置编码会随着序列增长而衰减远距离帧的影响力，即便将历史帧显式地纳入上下文，模型也难以有效利用这些“遥远”的记忆。同时，在蒸馏过程中，教师模型和学生模型所见的记忆上下文分布不一致，进一步加剧了蒸馏后的性能退化。

### 现有方法缺口

当前交互式世界模型可大致分为两类，但均未能同时解决实时性和长期一致性问题：

1. **无记忆的动作控制扩散模型**（如 CameraCtrl、SEVA、ViewCrafter、Matrix-Game-2.0、GameCraft）：这些方法专注于根据相机姿态或离散按键生成未来帧，但缺乏对历史场景的结构化记忆。在短期生成中表现尚可，但在长期轨迹（如 ≥250 帧的循环导航）中，重返场景的几何一致性急剧下降。

2. **基于显式 3D 记忆的方法**（如 Gen3C、VMem）：通过维护显式 3D 表征或特征缓存来保留空间信息，在长期一致性上优于无记忆方法。但其计算开销大，难以实现实时交互，且其记忆机制与高效蒸馏之间存在不兼容性。

如表 1 所总结，现有方法在“低延迟”与“高一致性”之间形成了明显的取舍关系，同时实现两者仍是一个开放问题。

### 本文动机

本文提出 **WorldPlay**，旨在打破上述困境，实现**实时交互**与**长期几何一致性**的统一。核心动机源于以下洞察：

- **记忆的构建方式比记忆的存在本身更为关键**。与其简单地缓存历史帧，不如动态重构一个包含时序和空间双重维度的上下文记忆集合，使模型始终能访问对当前生成最具信息量的历史信息。
- **位置编码的设计决定了记忆的可利用性**。标准绝对位置编码使远距离记忆在注意力机制中天然衰减，通过“时序重帧”将重要的远距离记忆在位置编码空间中“拉近”，可以克服这一长程衰减。
- **蒸馏过程中的记忆对齐是保持一致性的关键**。传统分布匹配蒸馏忽略了教师和学生模型所见记忆上下文的差异，通过在蒸馏时强制对齐两者的记忆分布（上下文强制），可以使轻量学生模型在极少去噪步骤下仍保留长期几何一致性。

基于以上动机，WorldPlay 构建了一个记忆感知的自回归扩散 Transformer，能够在 720p 分辨率下以 24 FPS 进行流式交互，同时在长达 250 帧以上的循环导航中保持场景的几何连贯性，显著超越所有现有基线方法。



## 核心方法与创新机理

WorldPlay 的核心创新在于通过一套系统性的“记忆感知生成与蒸馏”机制，首次在单一框架内同时解决了实时交互世界建模中长期存在的速度与几何一致性矛盾。其关键突破可归结为四个相互协同的技术槽位变更。

### 1. 双重动作表示：从单一按键到姿态-键位协同

现有动作控制扩散模型（如 **CameraCtrl**、**SEVA**、**ViewCrafter**、**Matrix-Game-2.0**、**GameCraft**）普遍仅使用离散按键输入，缺乏对连续相机运动的精确描述能力，导致控制精度受限且难以缓存精确位置信息。WorldPlay 提出了**双重动作表示**，将离散按键与连续相机姿态统一编码为控制信号。离散键用于鲁棒的动作类型识别与位置缓存，连续相机姿态则通过 PRoPE 注入因果自注意力，提供精确的空间运动信息。消融实验（Table 3）证实，双重表示在控制精度上显著优于纯离散或纯连续方案，全量指标达到 PSNR 22.09、旋转距离 0.028、平移距离 0.113，为后续记忆机制提供了可靠的空间锚点。

### 2. 重构上下文记忆：从局部检索到时空联合记忆

基于显式 3D 记忆的方法（如 **Gen3C**、**VMem**）虽能保持一定几何一致性，但依赖高计算成本的点云或特征体，难以实现实时交互。无记忆方法则完全丧失长期一致性。WorldPlay 的**重构上下文记忆**动态构建两类记忆：**时序记忆**保留最近 L 个 chunk，维持时序连续性；**空间记忆**从非相邻历史帧中采样，保持空间覆盖。这一设计使模型在仅需少量去噪步骤的轻量架构下，仍能访问关键历史信息。Table 2 显示，引入该记忆后长期 PSNR 从无记忆基线的不足 15 提升至 16.27（w/o Context Forcing），验证了记忆本身的有效性。

### 3. 时序重帧：从绝对位置到相对距离的编码重写

标准 RoPE 使用绝对时序索引，导致远距离记忆帧的位置编码超出有效范围，引发长程衰减和误差累积。WorldPlay 的**时序重帧**丢弃绝对索引，动态为所有上下文帧重新分配位置编码，使远距离空间记忆帧与当前帧之间保持固定的小相对距离。Table 4 显示，仅将标准 RoPE 替换为时序重帧 RoPE，长期 PSNR 即从 14.03 跃升至 16.27。Figure 7 进一步揭示了其作用机制：重帧 RoPE 避免了超出位置范围，并通过维持小相对距离缓解了误差累积，使远距离几何信息得以有效保留。

### 4. 上下文强制蒸馏：从分布匹配到记忆上下文对齐

标准分布匹配蒸馏（如 DMD）在教师和学生模型之间仅对齐输出分布，忽略了记忆上下文的差异——教师使用双向注意力访问完整上下文，学生则依赖自回归生成的、可能包含伪影的历史帧。这种上下文错位导致蒸馏失败，输出崩溃。WorldPlay 的**上下文强制**通过两个关键设计解决此问题：其一，为教师模型增广记忆，使其条件分布与学生保持一致；其二，在教师条件中屏蔽学生的自回归块，强制教师仅基于记忆上下文进行预测。Table 6 表明，上下文强制使学生模型在仅 4 个去噪步骤（NFE=4）下达到 PSNR 18.94，接近教师模型 100 步的 19.31，且显著优于未蒸馏的自回归模型。移除上下文强制则使长期 PSNR 降至 16.27，证实了记忆对齐对蒸馏成功的关键作用。

上述四个槽位变更形成了一条清晰的因果链：双重动作表示提供精确的空间锚定 → 重构上下文记忆动态维护时空信息 → 时序重帧克服长程衰减使远距离记忆可用 → 上下文强制蒸馏将记忆能力高效压缩至实时学生模型。这一链式创新使 WorldPlay 在长期几何一致性测试（≥250 帧）上以 PSNR 18.94 显著超越最佳有记忆基线 Gen3C（15.37），同时实现 24 FPS 的实时流式生成。



WorldPlay 是一个面向实时交互式世界建模的自回归视频生成框架，其核心目标是在用户流式操控下，以低延迟生成长期几何一致的视频序列。如图 Figure 2 所示，系统接收单张图像或文本提示作为世界描述，随后以“块”（chunk）为单位执行下一段预测任务——每个块包含 16 帧视频，生成过程受用户动作信号的条件控制。

框架的顶层工作流可概括为三个关键阶段：

1. **动作编码与条件注入**：用户输入被转换为双重动作表示（离散按键 + 连续相机姿态），经专用编码器处理后注入扩散 Transformer 的骨干网络，为生成提供精确的控制信号。
2. **记忆感知的自回归生成**：对于每个新块的生成，系统从历史块中动态重构上下文记忆（Reconstituted Context Memory），并通过时序重帧（Temporal Reframing）重新分配位置编码，将远距离但几何上重要的记忆帧“拉近”至当前帧，以克服 Transformer 中的长程衰减。
3. **蒸馏与实时推理**：通过上下文强制（Context Forcing）蒸馏方法，将记忆感知的双向教师模型的知识迁移到自回归学生模型中，使学生仅需 4 个去噪步骤（NFE=4）即可保持长期一致性，配合流式 VAE 解码器、KV-cache 和混合并行优化，最终实现 720p 分辨率下 24 FPS 的实时交互生成。

各模块间的数据流关系如下：历史观测 $O_{t-1}$ 与动作序列 $A_{t-1}$ 首先进入重构上下文记忆构建器，输出记忆上下文 $C_t$；$C_t$ 与当前动作 $a_t$、条件 $c$ 一同馈入自回归扩散 Transformer，经流匹配（Flow Matching）去噪生成当前块 $x_t$ 的潜变量，最后由流式 VAE 解码器输出视频帧。蒸馏阶段，教师模型（双向扩散）与学生模型（自回归）共享记忆上下文结构，上下文强制通过屏蔽学生的自回归块来对齐两者的记忆分布，从而在极少去噪步骤下保留长期几何一致性。

### 补充图表

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/004_Figure_3.jpg]]
*Figure 3: Detailed architecture of our autoregressive diffusion transformer. The discrete key is incorporated with time embedding, while the continuous camera pose is injected into causal selfattention through PRoPE [33]*



### 3.1 视频扩散模型基础

WorldPlay 的视频生成骨干是一个基于流匹配（Flow Matching）的自回归视频扩散 Transformer。给定当前世界状态，模型以“下一块”（next chunk，16 帧视频）预测的方式生成未来视频。其训练损失为流匹配损失：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{k, z_0, z_1} \| N_\theta(z_k, k) - v_k \|^2$$

其中 $z_0$ 和 $z_1$ 分别表示干净视频潜变量和噪声潜变量，$z_k$ 为中间插值状态，$v_k = z_0 - z_1$ 为速度场目标。模型 $N_\theta$ 在每个去噪步骤 $k$ 上预测该速度场。这一公式是整个扩散训练的基础，后续所有模块均在此框架上构建。

### 3.2 双重动作表示编码器（Dual Action Representation Encoder）

**设计动因**：交互式世界模型需要将用户输入转化为可控的生成信号。纯离散按键输入（如 WASD）语义明确但缺乏精确的空间定位；纯连续相机姿态虽定位准确但难以从噪声中学习。WorldPlay 提出双重动作表示，将二者结合。

**实现机制**（Figure 3）：
- **离散键（Discrete Key）**：将按键输入编码为离散 token，通过时间嵌入（time embedding）注入 Transformer 的 AdaLN 层。
- **连续相机姿态（Continuous Camera Pose）**：通过 PRoPE（Perspective Rotary Position Encoding）注入因果自注意力计算。具体地，标准三维 RoPE 自注意力为：

$$Attn_1 = Attn(R^{\top} \odot Q, R^{-1} \odot K, V)$$

其中 $R$ 为三维旋转位置编码矩阵。在此基础上，引入相机视锥自注意力：

$$Attn_2 = D^{proj} \odot Attn((D^{proj})^{\top} \odot Q, (D^{proj})^{-1} \odot K, (D^{proj})^{-1} \odot V)$$

其中 $D^{proj}$ 为基于相机投影矩阵构建的变换，将相机视锥关系编码到注意力计算中，使模型感知空间透视关系。

**消融验证**（Table 3）：全量双重动作表示在控制精度上显著优于纯离散或纯连续方案，PSNR 达 22.09，旋转距离 $R_{dist}$ 为 0.028，平移距离 $T_{dist}$ 为 0.113。

### 3.3 重构上下文记忆与时序重帧（Reconstituted Context Memory & Temporal Reframing）

**核心瓶颈**：标准自回归生成仅依赖近期帧，导致重返场景时几何不一致。显式 3D 记忆方法计算成本高，难以实时交互。

**重构上下文记忆**（Figure 2, Figure 4）：为每个新块 $x_t$ 动态构建记忆上下文 $C_t$，包含两部分：
- **时序记忆 $C_t^T$**：选取最近 $L$ 个已生成块，保持时序连续性。
- **空间记忆 $C_t^S$**：基于当前相机位置，从非相邻历史帧中检索空间邻近的帧，保持空间几何一致性。

**时序重帧（Temporal Reframing）**：标准 RoPE 使用绝对时序索引，远距离记忆帧的位置编码与当前帧差异过大，导致 Transformer 的注意力衰减严重。时序重帧丢弃绝对索引，为所有上下文帧重新分配相对位置编码，将远距离记忆“拉近”至当前帧附近（Figure 4c, Figure 7）。消融实验（Table 4）显示，时序重帧 RoPE 相较于标准 RoPE 在长期 PSNR 上从 14.03 提升至 16.27，并有效缓解了误差累积。

### 3.4 上下文强制蒸馏（Context Forcing Distillation）

**设计动因**：教师模型（双向视频扩散，100 步去噪）生成质量高但无法实时交互；学生模型（自回归扩散，4 步去噪）速度快但缺乏长期一致性。标准分布匹配蒸馏（Distribution Matching Distillation）直接匹配师生输出分布，其梯度为：

$$\nabla_{\theta} \mathcal{L}_{DMD} = \mathbb{E}_{k} \big( \nabla_{\theta} \mathrm{KL} \big( p_{\theta}(x_{0:t}) \big| \big| p_{data}(x_{0:t}) \big) \big)$$

**上下文强制**（Figure 5, Algorithm 1）：上述标准蒸馏忽略了师生模型在记忆上下文上的差异——教师可访问完整双向上下文，而学生仅能访问自回归因果上下文。上下文强制通过以下两步对齐记忆分布：

1. **记忆增强自回滚（Memory-Augmented Self-Rollout）**：学生模型自回归生成伪块，作为教师模型的输入上下文。
2. **记忆增强双向视频扩散**：教师模型以学生生成的历史块为记忆上下文，但将待预测的学生自回滚块从教师输入中屏蔽，使教师条件分布变为：

$$p_{data}(x_{j:j+3} | x_{0:j-1}) = p_{\beta}(x_{j:j+3} | C_{j:j+3} - x_{j:j+3})$$

其中 $C_{j:j+3}$ 为包含学生自回滚块的完整上下文，$-x_{j:j+3}$ 表示屏蔽这些块。这迫使教师模型在仅依赖学生可用的记忆上下文的条件下进行预测，从而消除师生间的上下文分布不匹配。

**关键结果**（Table 6）：上下文强制蒸馏后，学生模型在仅 4 步去噪（NFE=4）下 PSNR 达 18.94，接近教师模型 100 步的 19.31；移除上下文强制后，蒸馏失败，输出崩塌（Figure 8a）。

### 3.5 流式 VAE 解码与推理加速

为实现实时交互（24 FPS, 720p），WorldPlay 采用流式 VAE 解码器渐进式多步解码，降低单帧延迟。推理加速方面，通过混合并行（序列并行 + 注意力并行）将每块 token 分布到多设备，结合 KV-cache 和量化技术加速自回归生成（Algorithm 2）。

### 补充图表

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/001_Figure_1.jpg]]
*Figure 1: WorldPlay is a real-time, interactive world model that achieves long-term geometric consistency. It responds to user navigation commands in a streaming fashion, while maintaining scenes remain coherent when revisiting (shown in red boxes). Our model shows remarkable generalization across diverse scenes, including (a) real world, (b) stylized world, and (c) third-person agent control. Furthermore, it supports (d) 3D scene generation via reconstruction and (e) dynamic world events triggered by text-based manipulation*

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/003_Figure_2.jpg]]
*Figure 2: Method overview. Given a single image or text prompt to describe a world, WorldPlay performs a next chunk (16 video frames) prediction task to generate future videos conditioned on action from users. For the generation of each chunk, we dynamically reconstitute context memory from past chunks to enforce long-term temporal and geometric consistency*

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/006_Figure_5.jpg]]
*Figure 5: Context forcing is a novel distillation method that employs memory-augmented self-rollout and memory-augmented bidirectional video diffusion to preserve long-term consistency, enable real-time interaction, and mitigate error accumulation*



## 实验与关键发现

### 核心实验设置与评估协议

WorldPlay 在一个大规模、精心策划的数据集上训练，该数据集包含 32 万段真实与合成视频。评估分为短期（61 帧）和长期（≥250 帧）两种设定，重点考察视频生成质量（PSNR、SSIM、LPIPS）与动作控制精度（旋转误差 R_dist、平移误差 T_dist）。长期测试集专门设计了循环轨迹，以检验模型在重返场景时的几何一致性。所有基线模型均使用官方发布版本或论文描述的最佳设置进行测试，确保公平性。

### 主要量化结果：长期一致性的显著突破

Table 2 展示了 WorldPlay 与现有方法的全面比较。在长期几何一致性测试上，WorldPlay 全模型取得了 **18.94 PSNR** 和 **0.585 SSIM**，显著超越所有基线。相比最佳有记忆基线 **Gen3C**（15.37 PSNR / 0.431 SSIM），PSNR 提升了 **3.57 dB**，SSIM 提升了 **0.154**。这一差距在长期设定下尤为突出，因为无记忆方法（如 CameraCtrl、SEVA、ViewCrafter、Matrix-Game-2.0、GameCraft）在重返场景时会产生严重的几何不一致，而有记忆方法（如 Gen3C、VMem）虽然具备一定记忆能力，但无法在实时约束下维持如此高的一致性。

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparisons. We compare against both methods without memory, i.e., CameraCtrl [16], SEVA [80], ViewCrafter [77], Matrix-Game-2.0 [17], and GameCraft [31], and methods with memory, i.e., Gen3C [52], VMem [32]. Our method achieves superior results, particularly in long-term settings, which more clearly demonstrate the long-term consistency*

在短期设定下，WorldPlay 同样表现出色（21.92 PSNR / 0.702 SSIM），略优于 Gen3C（21.68 PSNR），表明模型在保持长期一致性的同时并未牺牲短期生成质量。

### 消融实验：各组件的因果贡献

#### 动作表示设计

Table 3 验证了双重动作表示的有效性。纯离散按键方案控制精度不足，纯连续相机姿态方案鲁棒性较差，而将两者结合的全量方案在所有指标上均达到最优：PSNR 22.09、R_dist 0.028、T_dist 0.113。这一设计使模型既能通过离散键实现稳健的位置缓存，又能通过连续姿态实现精确的相机控制。

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/010_Table_3.jpg]]
*Table 3: Ablation for action representation. We conduct validation using the bidirectional model*

#### 位置编码与时序重帧

Table 4 对比了标准 RoPE 与时序重帧 RoPE 的效果。在长期测试中，标准 RoPE 仅获得 14.03 PSNR，而时序重帧将其提升至 **16.27 PSNR**，提升超过 2 dB。Figure 7 揭示了其机制：标准 RoPE 中远距离记忆帧的绝对位置索引超出有效范围，导致注意力衰减和误差累积；时序重帧通过动态重新分配相对位置编码，将重要的远距离空间记忆“拉近”至当前帧，维持了有效的注意力连接。

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/011_Figure_7.jpg]]
*Figure 7: RoPE design comparisons. Upper: Our reframed RoPE avoids exceeding the the positional range in standard RoPE, alleviating error accumulation. Bottom: By maintaining a small relative distance to long-range spatial memory, it achieves better long-term consistency*

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/009_Table_4.jpg]]
*Table 4: Ablation for positional encoding design in memory. The results are evaluated on the long-term test data*

#### 上下文强制蒸馏

Table 6 展示了上下文强制的核心作用。蒸馏前的自回归学生模型（Student AR, NFE=4）仅取得 13.66 PSNR，几乎无法维持长期一致性。使用标准分布匹配蒸馏但移除上下文强制时（w/o Context Forcing），PSNR 降至 16.27。而上下文强制使蒸馏后的模型（Final distilled, NFE=4）达到 **18.94 PSNR**，接近教师模型（Teacher bidirectional, NFE=100）的 19.31 PSNR。这意味着模型仅需 4 个去噪步骤即可实现接近 100 步教师模型的生成质量，从而满足实时交互需求。Figure 8 进一步表明，当教师与学生的记忆上下文不对齐时，蒸馏会失败并导致输出崩溃。

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/012_Figure_8.jpg]]
*Figure 8: Ablation for context forcing. a) When the teacher and student have misaligned context, it leads to distillation failure, resulting in collapsed outputs. b) Self-rollout historical context can introduce artifacts. Zoom in for details. Figure 9. Promptable event. Our method supports text-based manipulation during streaming*

#### 记忆规模与类型

Table 7 分析了记忆规模的影响。较大的时序记忆（更多近期块）对维持时序连续性更为关键，而空间记忆过大反而会增加教师模型的训练和蒸馏难度。这一发现指导了记忆配置的实用选择。

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/018_Table_7.jpg]]
*Table 7: Ablation for memory size. Spa. and Tem. denote the number of chunks in spatial memory and temporal memory, respectively*

### 失败模式与局限性

尽管 WorldPlay 在长期一致性上取得了显著进展，但仍存在以下局限：
- 将框架扩展到更长时长（远超 250 帧）、多智能体交互和更复杂物理动态的视频生成仍需进一步研究。
- 当前动作空间有限，扩展到更广泛的动作类型（如更复杂的物体操作）是另一个有前景的方向。
- 上下文强制蒸馏依赖于记忆感知的教师模型，当教师与学生记忆分布差异过大时，蒸馏效果可能退化。

### 关键图表结论总结

- **Table 2**：WorldPlay 在长期一致性上碾压所有基线，PSNR 领先最佳有记忆方法 3.57 dB。
- **Table 3**：双重动作表示在全量指标上均优于纯离散或纯连续方案。
- **Table 4 + Figure 7**：时序重帧通过缓解长程衰减，将长期 PSNR 从 14.03 提升至 16.27。
- **Table 6 + Figure 8**：上下文强制是蒸馏成功的关键，使 4 步学生模型达到接近 100 步教师的质量。
- **Table 7**：时序记忆比空间记忆对一致性更重要，但空间记忆过大会增加训练难度。

### 补充图表

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/005_Figure_4.jpg]]
*Figure 4: Memory mechanism comparisons. The red and blue blocks represent the memory and current chunk, respectively. The number in each block represents the temporal index in RoPE. For simplicity of illustration, each chunk only contains one frame*

![[assets/figures/papers/WorldPlay_Towards_Long-Term_Geometric_Consistency_for_Real-Time_Interactive_Worl_47494ea383d3/figures/002_Table_1.jpg]]
*Table 1: Comparison with recent interactive world models. WorldPlay distinguishes itself as a general-domain model that simultaneously achieves long-horizon video generation, flexible action control, real-time interactivity, and long-term geometric consistency*



## 定位与知识库关联

### 1. 与现有工作的关系

WorldPlay 处于交互式世界建模（interactive world modeling）这一快速发展的领域，其核心贡献在于首次同时实现了实时交互生成与长期几何一致性。我们将现有工作按记忆机制和实时性两个维度进行定位。

**无记忆的动作控制扩散模型**构成了该领域的早期基线。这类方法将用户动作作为条件注入预训练的视频扩散模型，通过自回归方式生成连续帧序列。代表性工作包括 **CameraCtrl**、**SEVA**、**ViewCrafter**、**Matrix-Game-2.0** 和 **GameCraft**。它们的共同瓶颈在于缺乏对历史帧的显式记忆：每一轮生成仅依赖最近的若干帧，当用户重返先前访问过的场景时，模型无法保证几何结构的一致性，导致场景“漂移”或“遗忘”。这些方法在短期视觉质量上表现尚可，但在长期一致性测试中迅速退化（Table 2 中无记忆方法长期 PSNR 普遍低于 15 dB）。

**基于显式 3D 记忆的方法**试图通过维护显式的三维表示来克服遗忘问题。**Gen3C** 和 **VMem** 是这一路线的代表：它们在生成过程中构建并更新显式的 3D 场景表示（如点云或神经辐射场），并在每一帧生成时从该表示中检索相关信息。这一策略在理论上能够保证几何一致性，但代价是高昂的计算开销：3D 表示的构建、更新和查询使得每帧生成时间远超实时要求，且难以通过蒸馏压缩为轻量级模型。Table 2 的数据证实了这一点：Gen3C 在长期测试中取得 15.37 PSNR，显著优于无记忆方法，但仍远低于 WorldPlay 的 18.94，且其推理速度无法支持实时交互。

**WorldPlay 的方法论定位**是在上述两条路线之间开辟了第三条路径：通过**重构上下文记忆（Reconstituted Context Memory）** 动态构建时空记忆，既避免了显式 3D 表示的计算瓶颈，又克服了无记忆方法的长期遗忘问题。其核心创新在于将记忆机制内嵌于扩散 Transformer 的自注意力计算中，而非依赖外部 3D 数据结构。这使得记忆的构建和查询与生成过程深度融合，为后续的蒸馏压缩奠定了基础。

### 2. 关键设计选择的谱系分析

WorldPlay 的四个核心模块各自对应着领域内的特定瓶颈，其设计选择可以从方法谱系的角度加以理解。

**双重动作表示**解决了交互控制中离散按键与连续相机姿态的长期张力。纯离散表示（如按键映射）虽然鲁棒但控制精度有限；纯连续表示（如相机姿态向量）精度高但对噪声敏感。WorldPlay 将离散键作为时间嵌入注入，将连续姿态通过 PRoPE 注入因果自注意力（Eq. 2-3），实现了两者的互补。Table 3 的消融实验表明，全量双重表示在 PSNR（22.09）、旋转误差（R_dist 0.028）和平移误差（T_dist 0.113）上均优于单一方案。

**重构上下文记忆**是 WorldPlay 区别于所有现有工作的核心机制。传统方法要么仅使用最近的若干帧（如无记忆方法的滑动窗口），要么基于当前视锥（FOV）进行空间检索（如 Gen3C 的 3D 点查询）。WorldPlay 同时维护**时序记忆**（最近的 L 个 chunk）和**空间记忆**（从非相邻历史帧中基于空间邻近性采样），并在每个生成步骤动态重构上下文集合。Table 7 的消融揭示了时序记忆与空间记忆的非对称重要性：较大的时序记忆对保持时序连续性更为关键，而过大的空间记忆反而增加教师模型的训练和蒸馏难度。

**时序重帧（Temporal Reframing）** 针对的是 Transformer 架构中位置编码的长程衰减问题。标准 RoPE 为每帧分配绝对时序索引，当记忆帧与当前帧的时间距离过大时，注意力权重会因位置编码的衰减而失效。WorldPlay 丢弃绝对索引，动态为所有上下文帧重新分配相对位置编码，将远距离记忆“拉近”至当前帧（Figure 7 展示了这一机制如何缓解误差累积）。Table 4 的对比验证了这一设计的有效性：重帧 RoPE 将长期 PSNR 从标准 RoPE 的 14.03 提升至 16.27。

**上下文强制（Context Forcing）** 是蒸馏方法谱系中的新成员。标准分布匹配蒸馏（如 DMD）仅对齐教师和学生的输出分布，忽略了自回归生成中记忆上下文的差异：教师模型（双向扩散）可以访问完整的上下文，而学生模型（自回归）只能看到已生成的历史帧。这种上下文不对齐会导致蒸馏失败，表现为生成质量坍塌（Figure 8a）。上下文强制通过屏蔽学生自回归块并让教师基于相同的记忆上下文进行条件生成（Eq. 5），强制对齐两者的记忆分布。Table 6 的结果表明，经过上下文强制蒸馏的学生模型在仅 4 个去噪步骤（NFE=4）下即可达到 PSNR 18.94，接近教师模型 100 步的 19.31，同时实现了实时交互。

### 3. 适用边界与局限

WorldPlay 的当前能力边界可从以下几个维度界定：

**场景域泛化**：模型在 320K 真实与合成视频上训练，展现出对真实世界、风格化世界和第三人称智能体控制的泛化能力（Figure 1）。但该泛化仍限于训练数据覆盖的场景类型，对于极端偏离训练分布的视觉域（如抽象艺术风格或非欧几何空间），一致性保证可能减弱。

**时间尺度**：当前模型在 ≥250 帧的长期测试中表现优异，但将框架扩展到更长时间尺度（如数千帧的持续探索）仍需验证。时序重帧机制虽然缓解了长程衰减，但其有效性依赖于相对索引的分配策略，在极长时间跨度下可能需要更复杂的记忆管理策略。

**动作空间**：当前双重动作表示覆盖了离散导航键和连续相机姿态，但尚未扩展到更丰富的动作类型（如物体抓取、工具使用、物理交互）。论文明确指出将动作类型扩展到更广泛的集合是未来的研究方向。

**多智能体与复杂物理**：WorldPlay 目前聚焦于单用户导航场景。扩展到多智能体交互和更复杂的物理动态（如流体、形变体）需要重新设计记忆机制和动作表示，这是论文列出的开放问题之一。

**推理效率的边界**：虽然通过 KV-cache、混合并行和量化实现了 24 FPS 的 720p 流式生成，但这一性能是在特定硬件配置下测得的。在资源受限的边缘设备上部署时，可能需要额外的模型压缩或架构简化。

### 4. 开放问题

从方法谱系的角度，WorldPlay 提出了若干值得进一步探索的开放问题：

1. **时序重帧的长程衰减定量分析**：时序重帧在多大程度上定量缓解了 Transformer 中的长程衰减？是否存在一个临界时间跨度，超过该跨度后即使重帧也无法有效恢复注意力？对这一问题的回答将指导记忆窗口大小的选择策略。

2. **记忆感知蒸馏的分布不匹配性质**：当从记忆感知的自回归学生蒸馏到无记忆的双向教师时（或反之），具体的分布不匹配性质是什么？上下文强制提供了一种工程解决方案，但对不匹配的理论刻画仍然缺失。

3. **记忆机制的动态自适应**：当前重构上下文记忆的时序窗口大小 L 和空间采样策略是固定的。能否设计自适应的记忆管理策略，根据场景复杂度和探索历史动态调整记忆的组成和大小？

4. **多智能体与物理交互的扩展**：将 WorldPlay 扩展到多智能体交互和复杂物理模拟环境，需要重新思考记忆的归属（哪个智能体的记忆？）和物理状态的一致性约束。这是从“世界观察者”到“世界参与者”的关键一步。

5. **与显式 3D 表示的融合**：WorldPlay 的隐式记忆机制在效率上优于显式 3D 表示，但在几何精度上可能不及后者。是否存在一种混合方案，在保持实时性的前提下，利用稀疏的显式 3D 锚点来进一步增强长期几何一致性？



## 原文 PDF

![[paperPDFs/arxiv_2025/WorldPlay_Towards_Long_Term_Geometric_Consistency_for_Real_Time_Interactive_World_Modeling.pdf]]

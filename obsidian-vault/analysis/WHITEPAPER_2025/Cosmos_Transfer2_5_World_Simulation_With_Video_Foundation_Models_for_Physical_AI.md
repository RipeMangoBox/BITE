---
title: "Cosmos-Transfer2.5: World Simulation With Video Foundation Models for Physical AI"
type: paper
paper_level: A
venue: Whitepaper
year: 2025
pdf_ref: paperPDFs/WHITEPAPER_2025/Cosmos_Transfer2_5_World_Simulation_With_Video_Foundation_Models_for_Physical_AI.pdf
code_link: https://github.com/nvidia-cosmos/cosmos-transfer2.5
project_link: https://www.nvidia.com/en-us/ai/cosmos/
aliases:
- CP5CT5
- CT5WSVFMPA
tags:
- WHITEPAPER_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "通过极严格的数据过滤（仅保留4%高质量视频）、采用解码器型VLM (Cosmos-Reason1) 替代T5文本编码器、流匹配训练中的高噪声偏向、多域有监督微调合并以及GRPO强化学习后训练，共同大幅提升了视频质量和物理对齐。"
primary_logic: "更干净的数据、更强的文本表征、流匹配速度预测、模型合并策略和RL微调形成系统化改进，使得较小的模型（2B）在长视频、控制对齐和下游物理AI任务中均超越上一代7B模型。"
claims:
- "Cosmos-Transfer2.5-2B (质量分9.31) 超越 Cosmos-Transfer1-7B (9.24)，尽管参数减少3.5倍。"
- "Cosmos-Transfer2.5-2B增强的机器人策略成功率显著提升 (24/30 vs. baseline 5/30, base 1/30)。"
- "长视频生成中，Cosmos-Transfer2.5-2B的RNDS指标下降远小于Transfer1-7B，表明错误积累显著减少。"
- "RL后训练将Cosmos-Predict2.5-2B的Text2World reward从1.23提升至1.74，Image2World从0.24提升至0.45。"
---

# Cosmos-Transfer2.5: World Simulation With Video Foundation Models for Physical AI

> [!tip] 核心洞察
> 更干净的数据、更强的文本表征、流匹配速度预测、模型合并策略和RL微调形成系统化改进，使得较小的模型（2B）在长视频、控制对齐和下游物理AI任务中均超越上一代7B模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cosmos-Transfer2.5: 基于视频基础模型的物理AI世界仿真 |
| 英文题名 | Cosmos-Transfer2.5: World Simulation With Video Foundation Models for Physical AI |
| 会议/期刊 | Whitepaper 2025 |
| Links | [paper](https://d1qx31qr3h6wln.cloudfront.net/publications/World_Simulation_with_Video_Foundation_Models_for_Physical_AI.pdf) · [GitHub](https://github.com/nvidia-cosmos/cosmos-transfer2.5) · [Project](https://www.nvidia.com/en-us/ai/cosmos/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Cosmos-Predict2.5 / Cosmos-Transfer2.5 |
| Dataset | PAI-Bench-Transfer (Universal Weights), Real-Robot Manipulation (10 scenarios), Bridge Dataset (Action-Conditioned Prediction), Multi-view Driving Generation (RDS-HQ-HL) |

> [!tip] 效果简介
> - PAI-Bench-Transfer (Universal Weights) 上，Quality Score↑ 为 Cosmos-Transfer2.5-2B: 9.31，对比 Cosmos-Transfer1-7B: 9.24，变化 +0.07。
> - Real-Robot Manipulation (10 scenarios) 上，Success rate (out of 30) 为 Cosmos-Transfer2.5-2B augmented: 24/30，对比 Standard augmentation: 5/30; Base policy: 1/30，变化 +19 (vs. baseline), +23 (vs. base)。
> - Bridge Dataset (Action-Conditioned Prediction) 上，PSNR↑ 为 Cosmos-Predict2.5-2B: 24.95，对比 Cosmos-Predict1-7B-Sample-ActionCond: 21.14，变化 +3.81。

## 概要

### 问题瓶颈

物理AI世界仿真需要视频生成模型具备长程一致性、精确的控制跟随能力和高度的物理真实性。然而，现有视频生成模型在生成长视频时普遍存在**幻觉和错误积累**问题，生成质量随时间推移显著退化。同时，模型对控制输入（如边缘、深度、分割图）的跟随性不足，导致生成的世界状态偏离真实物理。更深层的原因在于：训练数据质量参差不齐、文本编码器（如T5）的语义理解深度有限，以及训练策略未能充分优化指令对齐，共同限制了模型的物理真实性和长程一致性。

### 核心方法

Cosmos-Transfer2.5 通过系统化的改进链解决上述瓶颈：

1. **极严格的数据过滤**：从超过2亿原始视频中仅保留约4%的高质量片段（约2亿个可训练片段），通过多级过滤（美学评分、运动检测、OCR过滤、感知质量、语义伪影、VLM过滤）和语义去重，构建高纯净度训练集。
2. **解码器型VLM替代T5**：采用 Cosmos-Reason1（物理AI视觉语言模型）作为文本编码器，通过多块拼接投影提供更丰富的语义基座，增强文本与视觉的对齐。
3. **流匹配训练与高噪声偏向**：从扩散模型转向流匹配的速度预测目标，并通过时间步偏移将训练分布偏向高噪声区域，提升生成质量。
4. **多域SFT与模型合并**：在多个物理AI领域分别进行有监督微调，再通过模型合并策略综合各域能力，不损害通用域性能。
5. **GRPO强化学习后训练**：基于 VideoAlign 奖励模型进行RL微调，进一步优化生成视频的视觉质量和指令对齐。

在控制网（ControlNet）结构上，Cosmos-Transfer2.5 将控制块从连续插入主分支首部改为**均匀插入主分支**（每7个块插入一个），显著改善了控制跟随性和长视频错误积累。

### 核心结论

尽管 Cosmos-Transfer2.5-2B 的参数量仅为上一代 Cosmos-Transfer1-7B 的约1/3.5，其在多个基准上实现了全面超越：

- **视频质量**：在 PAI-Bench-Transfer 上，Cosmos-Transfer2.5-2B 的质量分达到 9.31，超越 Transfer1-7B 的 9.24（Table 10）。
- **长视频错误积累**：RNDS 指标的下降幅度远小于 Transfer1-7B，表明错误积累显著减少（Figure 9）。
- **机器人操作**：在真实机器人10个测试场景中，Cosmos-Transfer2.5-2B 增强的策略成功率达到 24/30，远超基线增强的 5/30 和基础策略的 1/30（Table 11）。
- **RL后训练收益**：RL后训练将 Text2World reward 从 1.23 提升至 1.74，Image2World reward 从 0.24 提升至 0.45（Table 6）。

更干净的数据、更强的文本表征、流匹配速度预测、模型合并策略和RL微调形成系统化改进，使得较小模型在长视频生成、控制对齐和下游物理AI任务中均取得显著突破。

### 方法谱系与知识库定位

Cosmos-Transfer2.5 属于**视频世界模型**和**可控视频生成**的交叉领域。其方法谱系可定位于：

- **基础架构**：基于流匹配的 DiT（Diffusion Transformer）架构，采用 WAN2.1 VAE 进行 4×8×8 压缩，使用 3D RoPE 相对位置编码。
- **文本编码**：以解码器型VLM（Cosmos-Reason1）替代传统T5编码器，属于“VLM-as-Encoder”的技术路线。
- **控制机制**：基于 ControlNet 的多模态控制（边缘、模糊、深度、分割），控制块均匀插入策略区别于传统连续插入方式。
- **后训练范式**：SFT + RL（GRPO）的两阶段后训练，与当前LLM/VLM的主流对齐范式一致。

与同期工作的对比：**Wan2.1-14B**（Wan et al., arXiv 2025）和 **Wan2.2-5B** 作为竞争视频生成模型，Cosmos-Predict2.5-2B 在人类评估中与二者相当（Figure 6），但参数量显著更小，且额外具备物理AI下游任务（机器人、自动驾驶）的专门优化。前代 **Cosmos-Predict1**（NVIDIA, arXiv 2025）基于EDM扩散和T5编码器，Cosmos-Transfer2.5 在架构、数据和训练策略上均实现了代际升级。

### 局限与开放问题

1. **大模型后训练未完成**：Cosmos-Predict2.5-14B 的后训练结果尚未报告，更大规模模型的性能上限未知。
2. **长视频错误积累**：虽大幅改善，但长视频生成中仍存在一定的错误积累，未完全消除。
3. **多视图遮挡处理**：世界场景地图在多视图驾驶仿真中如何处理遮挡和动态物体交互未详细阐明。
4. **时间步偏移扩展性**：渐进式时间步偏移参数 β 在高于720p分辨率时的扩展行为尚不明确。
5. **领域自适应需求**：在智能空间、人体动力学等其他物理AI领域的领域自适应是否仍需进一步微调，有待验证。

物理AI的核心愿景是构建能够模拟真实世界动态的生成式世界模型，从而为机器人、自动驾驶等具身智能系统提供可扩展的训练与评估环境。视频生成模型因其对视觉世界的强大建模能力，被视为实现这一目标的关键技术路径。然而，当前视频世界模型在服务于物理AI下游任务时，仍面临三个根本性瓶颈。

**长视频生成中的幻觉与错误积累。** 物理仿真要求模型能够生成长时序、物理一致的视频序列。但现有模型在生成长视频时，画面质量随帧数增加而显著退化，表现为物体形变、纹理漂移和物理规则违背等幻觉现象。这种错误积累的根源在于模型缺乏对长程时序依赖的有效建模，以及训练数据中长视频样本的稀缺。

**控制跟随性不足导致世界失真。** 物理AI应用通常需要精确的条件控制——例如基于边缘图、深度图、分割掩码或动作指令来驱动视频生成。然而，上一代模型（如**Cosmos-Transfer1**，NVIDIA, arXiv 2025）对控制信号的跟随能力有限，生成的视频往往与控制输入产生偏差，导致仿真世界与预期物理状态不一致。这种偏差在需要精确几何和运动约束的机器人操作场景中尤为致命。

**数据质量与语义理解的系统性缺陷。** 大规模视频预训练数据的质量参差不齐，原始网络视频中包含大量低质量、重复和语义噪声内容。同时，传统文本编码器（如T5）对物理世界的语义理解深度不足，难以将复杂的物理指令精确映射到视觉生成空间。此外，训练策略未能充分优化指令对齐，使得模型在开放域文本条件下的生成结果缺乏物理真实感。

针对上述问题，**Cosmos-Transfer2.5** 提出了一套系统化改进方案：通过极严格的数据过滤管线（仅保留约4%的高质量视频）、采用解码器型视觉语言模型 **Cosmos-Reason1** 替代T5文本编码器、引入流匹配训练目标与高噪声偏向的时间步调度、多域有监督微调合并策略以及基于GRPO的强化学习后训练，在参数规模缩小3.5倍的情况下，实现了长视频质量、控制对齐和下游物理AI任务性能的全面超越。

## 核心方法与创新机理

Cosmos-Predict2.5 / Transfer2.5 的核心创新并非单一技术突破，而是围绕“数据质量-语义理解-训练策略”三条主线对前代模型（**Cosmos-Predict1** / **Cosmos-Transfer1**，NVIDIA, arXiv 2025）的系统性重构。其关键改进可归纳为以下六个 **changed slots**：

### 1. 文本编码器：从 T5 到 Cosmos-Reason1 的语义跃迁
前代模型使用通用文本编码器 T5，对物理世界语义的捕捉深度有限。Cosmos-Predict2.5 替换为 **Cosmos-Reason1**——一个专为物理 AI 设计的解码器型视觉语言模型（VLM），并通过多块拼接投影将文本特征注入 DiT 去噪网络（Section 3.2）。这一替换使模型获得了更丰富的文本锚定能力，为物理真实性和指令跟随性提供了更强的语义基础。

### 2. 训练目标：从扩散模型到流匹配速度预测
前代 Cosmos-Predict1 基于 EDM 扩散框架。Cosmos-Predict2.5 全面转向**流匹配**范式，直接预测速度场 $\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$，并采用高噪声偏向的偏移对数正态分布 $t_s = \frac{\beta t}{1 + (\beta - 1) t}$ 将训练重心引向高噪声区域（Section 3.1, Equation 4）。这一设计显著提升了模型在低信噪比条件下的生成质量，是长视频错误积累减少的关键机制之一。

### 3. 视觉分词器与位置编码的架构精简
Cosmos-Predict2.5 采用 **WAN2.1 VAE** 作为视觉分词器，以 $4 \times 8 \times 8$ 的压缩率处理视频序列（Section 3.2）。与此同时，模型移除了绝对位置编码，仅保留基于 **3D RoPE** 的相对位置编码。这一精简不仅降低了参数量，还增强了模型对可变长度视频的泛化能力。

### 4. 多域 SFT 合并与 GRPO 强化学习后训练
Cosmos-Predict2.5 在后训练阶段采用**多域有监督微调合并**策略：先在驾驶、机器人等多个物理 AI 领域分别进行 SFT，再将领域模型合并，使综合模型在各域均达到最佳胜率而不损害通用域性能（Figure 3, Figure 4）。在此基础上，模型进一步经过基于 VideoAlign 的 **GRPO 强化学习**后训练，将 Text2World reward 从 1.23 提升至 1.74，Image2World reward 从 0.24 提升至 0.45（Table 6），在人类投票中也获得显著偏好（Figure 5）。

### 5. 控制网结构：从连续插入到均匀分布
Cosmos-Transfer2.5 对控制网分支的插入策略进行了关键调整：前代 Transfer1 将控制块连续插入主分支首部，而 Transfer2.5 改为**每 7 个主分支块插入一个控制块**的均匀分布策略（Section 6.1）。这一改变带来了更好的控制跟随性和更低的错误积累，是 Transfer2.5-2B 在长视频生成中 RNDS 指标显著优于 Transfer1-7B 的重要结构因素（Figure 9）。

### 6. 数据管线：4% 生存率的极严格过滤
上述方法创新的有效性建立在极高质量的训练数据之上。Cosmos-Predict2.5 的数据管线从 2 亿原始视频中仅保留约 4% 的高质量片段（约 2 亿个可训练片段），经过镜头分割、GPU 加速转码、多级过滤（美学评分、运动、OCR、感知质量、语义伪影、VLM 过滤）、语义去重和结构化分片等七阶段处理（Section 2.1, Figure 1）。这种“数据优先”的策略是较小模型（2B）超越上一代 7B 模型的根本性保障。

**系统性创新的效果**：上述改进形成了协同增益——更干净的数据、更强的文本表征、流匹配速度预测、模型合并策略和 RL 微调共同作用，使得 Cosmos-Transfer2.5-2B 在参数减少 3.5 倍的情况下，质量评分（9.31）超越 Cosmos-Transfer1-7B（9.24）（Table 10），并在真实机器人操作策略中实现 24/30 的成功率，远超 baseline 的 5/30 和 base policy 的 1/30（Table 11）。

Cosmos-Transfer2.5 的整体框架围绕“预测—后训练—翻译”三阶段构建，核心目标是生成物理真实、控制对齐的长视频，并直接服务于物理 AI 下游任务。其基础是世界预测模型 **Cosmos-Predict2.5**，该模型统一了 Text2World、Image2World 和 Video2World 三种生成模式，随后通过后训练与模型合并策略注入领域知识，最后经由世界翻译模型 **Cosmos-Transfer2.5** 实现多模态控制下的结构化世界仿真。

### 视频数据管线

整个系统的数据基础是一条极严格的视频策展管线（Figure 1），包含七个阶段：镜头感知的视频切分、GPU 加速转码与裁剪、多级过滤、视频标注、语义去重、以及结构化分片。其中多级过滤是数据质量的瓶颈控制点——依次通过美学评分、运动、OCR、感知质量、语义伪影和 VLM 过滤，最终仅约 **4%** 的视频片段通过全部关卡，从超过 2 亿原始视频中产出约 2 亿可训练片段。这种极低留存率直接构成了“更干净的数据”这一核心因果旋钮。

### 世界预测模型架构

Cosmos-Predict2.5 的架构（Figure 2）以**流匹配**（flow matching）替代了前代 Cosmos-Predict1 的 EDM 扩散范式。具体而言，模型在 WAN2.1 VAE 的潜在空间中工作——该 VAE 以 $4 \times 8 \times 8$ 的压缩率将视频编码为潜在表示，再经 $1 \times 2 \times 2$ 的补丁化处理。去噪网络是一个 DiT 结构，由自注意力、交叉注意力、前馈 MLP 与自适应层归一化模块重复堆叠而成。

![[assets/figures/papers/paper_list_l39_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/005_Figure_2.jpg]]
*Figure 2: Overall architecture of [Cosmos-Predict2.5]. As shown on the right, in the latent space, the model applies repeated blocks of self-attention, cross-attention, and feed-forward MLP layers, modulated by adaptive layer normalization (scale, shift, gate) for a given time step ??. We leverage [Cosmos-Reason1] as the text encoder (shown on the left). [Cosmos-Reason1] can also accommodate visual inputs (image and video) beyond text, which we leave for future work*

关键的架构变更包括：

- **文本编码器替换**：用解码器型 VLM **Cosmos-Reason1** 替代 T5，通过多块拼接投影提供更丰富的物理语义表征。这是解决“文本编码器语义理解深度有限”的核心手段。
- **位置编码简化**：移除绝对位置嵌入，仅保留 3D RoPE 相对位置编码。
- **训练目标切换**：从扩散模型的噪声预测转为流匹配的速度预测，损失函数为：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{x}, \boldsymbol{\epsilon}, \mathbf{c}, t} \left\| \mathbf{u}(\mathbf{x}_t, t, \mathbf{c}; \boldsymbol{\theta}) - \mathbf{v}_t \right\|^2$$

其中 $\mathbf{x}_t = (1 - t) \mathbf{x} + t \boldsymbol{\epsilon}$ 是数据与噪声的线性插值，$\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$ 是真实速度。训练中通过偏移逻辑正态分布 $t_s = \frac{\beta t}{1 + (\beta - 1) t}$ 将时间步分布偏向高噪声区域，使模型在去噪早期获得更多训练信号。

对于 Image2World 和 Video2World 任务，模型采用**条件帧替换策略**——将初始帧替换为给定的条件帧，从而在统一的流匹配框架内实现多任务训练。

### 后训练与模型合并

预训练完成后，Cosmos-Predict2.5 经历两个后训练阶段：

1. **多域有监督微调（SFT）**：在不同领域（机器人、驾驶等）分别进行 SFT，各自显著提升域内胜率（Figure 3）。
2. **模型合并**：将多个域 SFT 模型的权重合并，使单一模型在保持通用域性能的同时获得各域最佳能力（Figure 4）。这是“模型合并策略”作为因果旋钮的直接体现。
3. **GRPO 强化学习后训练**：基于 VideoAlign 奖励模型进行 RL 微调，将 Text2World reward 从 1.23 提升至 1.74，Image2World 从 0.24 提升至 0.45（Table 6），有效改善视频质量与指令对齐。

### 世界翻译模型

Cosmos-Transfer2.5 在 Cosmos-Predict2.5 的基础上附加控制网分支，支持边缘、模糊、深度、分割等多模态控制信号。相比前代 Transfer1 将控制块连续插入主分支首部的做法，Transfer2.5 采用**均匀插入策略**（每 7 个主分支块插入一个控制块），这一设计直接带来了更好的控制跟随和更低的错误积累（Figure 9, Table 10）。

### 输入输出流总览

系统接受文本描述、初始图像/视频帧、以及可选的多模态控制信号作为输入。在预测模式下，输出为符合物理规律的世界状态推演视频；在翻译模式下，输出为受控制信号引导的结构化世界仿真。所有生成结果均可直接用于物理 AI 下游任务，如机器人策略训练的数据增强（Table 11）和多视图驾驶仿真（Table 12）。

### 流匹配生成框架

Cosmos-Predict2.5 的核心生成范式从扩散模型转向**流匹配**（Flow Matching），训练目标为速度预测。给定数据样本 $\mathbf{x}$ 和高斯噪声 $\boldsymbol{\epsilon}$，构造插值潜在变量：

$$\mathbf{x}_t = (1 - t) \mathbf{x} + t \boldsymbol{\epsilon}$$

其中 $t \in [0, 1]$ 为时间步。对应的真实速度定义为：

$$\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$$

模型 $\mathbf{u}(\mathbf{x}_t, t, \mathbf{c}; \boldsymbol{\theta})$ 以条件 $\mathbf{c}$ 为输入，通过均方误差学习预测该速度：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{x}, \boldsymbol{\epsilon}, \mathbf{c}, t} \left\| \mathbf{u}(\mathbf{x}_t, t, \mathbf{c}; \boldsymbol{\theta}) - \mathbf{v}_t \right\|^2$$

为增强对高噪声区域的建模能力，训练时对时间步施加偏移，使其服从偏移对数正态分布。具体变换为：

$$t_s = \frac{\beta t}{1 + (\beta - 1) t}$$

其中 $\beta$ 为偏移参数。该单调变换将采样密度向 $t=1$（纯噪声）方向倾斜，迫使模型在更具挑战性的高噪声区间投入更多优化资源。

### 视觉分词器与补丁化

模型采用 **WAN2.1 VAE** 作为视觉分词器，在时间、高度、宽度维度上实现 $4 \times 8 \times 8$ 的压缩率。压缩后的潜在表示进一步经过 $1 \times 2 \times 2$ 的补丁化处理，形成输入 DiT 骨干网络的 token 序列。

### 文本编码器替换

Cosmos-Predict2.5 将前代使用的 T5 文本编码器替换为 **Cosmos-Reason1**——一个面向物理 AI 的解码器型视觉语言模型。该编码器通过多块拼接投影，将文本特征注入 DiT 的交叉注意力层，提供更丰富的语义接地和更精细的世界仿真控制。

### DiT 骨干网络

去噪网络采用标准 DiT 架构，由自注意力、交叉注意力、前馈 MLP 层堆叠而成，各层通过自适应层归一化（scale、shift、gate）进行调制。关键架构变更为**移除绝对位置编码**，仅保留 3D RoPE 相对位置编码，以增强对可变分辨率与帧数的泛化能力。

### 条件帧替换策略

在 Image2World 和 Video2World 任务中，模型采用条件帧替换机制：将生成序列的初始帧直接替换为给定的条件帧，使模型仅需预测后续帧，从而降低任务难度并提升时序一致性。

### 控制网分支结构

Cosmos-Transfer2.5 在 Predict2.5 基础上引入控制网分支，支持边缘、模糊、深度、分割等多模态控制信号。相比 Transfer1 将控制块连续插入主分支首部的设计，Transfer2.5 改为**每 7 个主分支块插入一个控制块**的均匀分布策略，显著提升了控制跟随性和长视频生成中的错误积累抑制能力（见 Figure 9 的 RNDS 退化曲线）。

### 长视频质量退化度量

为量化长视频生成中的错误积累，提出**归一化相对 Dover 分数**（Normalized Relative Dover Score, RNDS）：

$$\mathsf{RNDS}[i] = \left( \frac{\mathrm{DOVER}[i]}{\mathrm{DOVER}_{\mathrm{GT}}[i]} \right) / \left( \frac{\mathrm{DOVER}[1]}{\mathrm{DOVER}_{\mathrm{GT}}[1]} \right)$$

其中 $\mathrm{DOVER}[i]$ 为生成视频第 $i$ 块的感知质量分数，$\mathrm{DOVER}_{\mathrm{GT}}[i]$ 为对应真实视频块的质量分数。RNDS 以首块为基准归一化，其随块索引的下降速率直接反映错误积累程度。

## 实验与关键发现

### 核心性能突破

Cosmos-Transfer2.5-2B 在参数规模仅为前代 Cosmos-Transfer1-7B 的 28.6% 的条件下，实现了全面的性能超越。在 PAI-Bench-Transfer 通用权重质量评估中，Transfer2.5-2B 的质量分达到 9.31，超越 Transfer1-7B 的 9.24（Table 10）。这一提升的因果链路可追溯至三个关键改进：**极严格的数据过滤**（仅保留约 4% 高质量视频片段，从 2 亿原始视频中筛选出约 2 亿可训练片段）、**更强的文本表征**（以解码器型 VLM Cosmos-Reason1 替代 T5 编码器）以及**均匀控制块插入策略**（每 7 个主分支块插入一个控制块，替代 Transfer1 的连续首部插入）。

在长视频生成这一核心瓶颈上，Cosmos-Transfer2.5-2B 展现出显著降低的错误积累。Figure 9 的归一化相对 Dover 分数（RNDS）曲线表明，随着视频块索引增加，Transfer2.5-2B 的质量退化远小于 Transfer1-7B。RNDS 定义为：

![[assets/figures/papers/paper_list_l39_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/020_Figure_9.jpg]]
*Figure 9: Error accumulation for long video generations. These plots show the Normalized Relative Dover Score vs Chunk Index for auto-regressive multi-trunk long video generation where each trunk is 93 frames. As shown, for all four control modalities (edge/blur/depth/seg), compared to [Cosmos-Transfer1-7B] (blue curves), [Cosmos-Transfer2.5-2B] (green curves) has much less reduction in RNDS along the chunk index dimension, which shows less hallucination and error accumulation for long videos*

![[assets/figures/papers/paper_list_l39_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/033_Figure.jpg]]

$$\mathsf{RNDS}[i] = \left( \frac{\mathrm{DOVER}[i]}{\mathrm{DOVER}_{\mathrm{GT}}[i]} \right) / \left( \frac{\mathrm{DOVER}[1]}{\mathrm{DOVER}_{\mathrm{GT}}[1]} \right)$$

该指标衡量生成视频各块相对于真实视频的质量衰减比例，Transfer2.5 的曲线更平缓，直接验证了均匀控制块插入对抑制长程错误传播的有效性。

### 下游物理 AI 任务验证

在真实机器人操作任务中，Cosmos-Transfer2.5-2B 增强的策略成功率达到 **24/30**，远超标准数据增强的 5/30 和基础策略的 1/30（Table 11）。这一 23 个成功案例的绝对提升，源于 Transfer2.5 生成的世界状态在物理真实性和控制跟随性上的双重改进——Figure 11 的数据增强画廊显示，Transfer2.5 生成的增强样本在光照、纹理和遮挡处理上均优于基线。

在 Bridge 数据集的机器人动作条件视频预测中，Cosmos-Predict2.5-2B 的 PSNR 达到 **24.95**，相比 Cosmos-Predict1-7B-Sample-ActionCond 的 21.14 提升了 +3.81（Table 17）。动作向量为 7 维笛卡尔空间参数：

$$(\Delta x, \Delta y, \Delta z, \Delta \theta_r, \Delta \theta_p, \Delta \theta_y, \mathrm{GripperWidth})$$

消融实验（Table 18）进一步揭示，**时间嵌入**是注入动作条件的最优方式，其性能优于交叉注意力和通道拼接方案。

在多视图驾驶仿真中，Cosmos-Transfer2.5-2B/auto/multiview 在 RDS-HQ-HL 数据集上的 FVD StyleGAN 达到 24.22，相比 Transfer1-7B-Sample-AV 实现了最高 **2.3 倍**的提升（Table 12）。Table 13 的车道和边界框检测评估进一步验证了生成视图在下游感知任务中的实用性。

### 训练策略消融

**领域 SFT 与模型合并**：Figure 3 显示，针对特定领域（如机器人、驾驶）的有监督微调显著提升了各域内的胜率。Figure 4 表明，合并后的模型在保持通用域性能的同时，综合性能最优——这验证了多域 SFT 合并策略的有效性，避免了灾难性遗忘。

**RL 后训练**：基于 VideoAlign 的 GRPO 强化学习将 Cosmos-Predict2.5-2B 的 Text2World reward 从 1.23 提升至 **1.74**，Image2World reward 从 0.24 提升至 **0.45**（Table 6）。Figure 5 的人类投票结果进一步确认 RL 后训练显著改善了生成视频的视觉质量和指令对齐度。

**流匹配与高噪声偏向**：训练采用速度预测目标，损失函数为：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{x}, \boldsymbol{\epsilon}, \mathbf{c}, t} \left\| \mathbf{u}(\mathbf{x}_t, t, \mathbf{c}; \boldsymbol{\theta}) - \mathbf{v}_t \right\|^2$$

其中潜在变量插值 $\mathbf{x}_t = (1 - t) \mathbf{x} + t \boldsymbol{\epsilon}$，真实速度 $\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$。通过偏移 logit-normal 分布的时间步变换 $t_s = \frac{\beta t}{1 + (\beta - 1) t}$ 将训练偏向高噪声区域，这一设计直接贡献于长视频生成中错误积累的减少。

### 与外部模型的对比

Figure 6 的人类评估显示，尽管参数规模更小，Cosmos-Predict2.5-2B 后训练模型在多样化提示词上与 **Wan2.2-5B** 和 **Wan2.1-14B**（Wan et al., arXiv 2025）性能相当。这一结果表明，数据质量、文本编码器和训练策略的系统化改进能够以更小的模型规模实现竞争力性能。

### 已知局限

尽管长视频生成质量大幅改善，Figure 9 的 RNDS 曲线仍呈现下降趋势，表明错误积累尚未完全消除。Cosmos-Predict2.5-14B 的后训练结果尚未完成，其性能上限仍有待验证。此外，多视图驾驶仿真中世界场景地图对遮挡和动态物体交互的处理机制未详细阐明，该点需人工核实。

![[assets/figures/papers/paper_list_l39_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/001_Table_1.jpg]]
*Table 1: List of released models with their corresponding capabilities and inputs*

![[assets/figures/papers/paper_list_l39_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/003_Table_2.jpg]]
*Table 2: Overview of high-quality robotics datasets with video counts by camera perspective*

![[assets/figures/papers/paper_list_l39_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/004_Table_3.jpg]]
*Table 3: Configuration details of [Cosmos-Predict2.5] models*

## 定位与知识库关联

### 1. 与前代工作的关系

**Cosmos-Predict2.5 / Cosmos-Transfer2.5** 是 NVIDIA Cosmos 系列视频世界模型的第二代，直接继任自 **Cosmos-Predict1** 与 **Cosmos-Transfer1**（NVIDIA, arXiv 2025）。两代之间的关键架构变更可从以下维度理解：

| 维度 | Cosmos-Predict1 / Transfer1 | Cosmos-Predict2.5 / Transfer2.5 | 变更动机 |
|------|---------------------------|-------------------------------|---------|
| **文本编码器** | T5 | Cosmos-Reason1（解码器型VLM，多块拼接投影） | 提升语义理解深度，增强物理场景的文本对齐能力 |
| **训练目标** | EDM扩散 | 流匹配（velocity prediction） | 更稳定的训练动力学，更高效的采样路径 |
| **视觉分词器** | 未明确VAE | WAN2.1 VAE（4×8×8压缩） | 更强的视频压缩与重建质量 |
| **位置编码** | 绝对+相对位置编码 | 仅3D RoPE相对位置编码 | 提升长视频生成的长度外推能力 |
| **控制网结构** | 控制块连续插入主分支首部 | 控制块均匀插入主分支（每7块插1个） | 改善控制跟随性，降低长视频错误积累 |
| **后训练RL** | 无 | GRPO强化学习（基于VideoAlign） | 进一步提升视频质量与指令对齐 |

这些变更形成系统化改进链条：更干净的数据（仅4%通过率）→ 更强的文本表征（Cosmos-Reason1）→ 流匹配速度预测 → 多域SFT合并 → RL微调。最终结果是，**2B参数模型在长视频质量、控制对齐和下游物理AI任务中全面超越上一代7B模型**（Table 10: 质量分9.31 vs. 9.24）。

### 2. 与同期竞争工作的关系

在人类偏好评估中，Cosmos-Predict2.5-2B与同期视频生成模型进行了直接比较（Figure 6）：
- **Wan2.1-14B**（Wan et al., arXiv 2025）：14B参数，Cosmos-Predict2.5-2B在多样化提示集上与其持平。
- **Wan2.2-5B**：5B参数，Cosmos-Predict2.5-2B同样达到可比的胜率。

这表明Cosmos-Predict2.5在参数量显著更少（2B vs. 14B）的情况下，仍具备竞争力。然而，Cosmos-Predict2.5-14B的后训练尚未完成，其最终性能边界仍待验证。

### 3. 方法适用边界

**适用场景：**
- 物理AI世界仿真：包括机器人操作、自动驾驶多视图生成、动作条件视频预测等任务。
- 多模态控制生成：支持边缘、模糊、深度、分割、相机轨迹等多种控制信号。
- 数据增强：在真实机器人策略训练中，Cosmos-Transfer2.5-2B增强的策略成功率从基准的5/30提升至24/30（Table 11）。

**边界与局限：**
- **长视频错误积累**：尽管RNDS指标显示Cosmos-Transfer2.5-2B的错误积累远小于Transfer1-7B（Figure 9），但长视频生成中仍存在一定程度的退化。
- **14B模型未完成**：Cosmos-Predict2.5-14B的后训练结果缺失，大模型性能上限未知。
- **世界场景地图细节缺失**：多视图驾驶仿真中，世界场景地图如何处理遮挡和动态物体交互未详细阐明。
- **领域自适应需求**：在不同物理AI领域（如智能空间、人体动力学）的迁移是否仍需进一步微调，目前未给出明确答案。

### 4. 开放问题

1. **渐进式时间步偏移参数** $t_s = \frac{\beta t}{1 + (\beta - 1) t}$ 中的 $\beta$ 在高于720p分辨率时如何进一步扩展？（Section 3.1, Equation 4）
2. **模型合并的超参数搜索**：多域SFT模型的合并权重搜索范围和选择标准是什么？（Figure 3-4）
3. **世界场景地图的遮挡处理**：多视图驾驶仿真中，场景地图如何处理动态物体交互和遮挡？（Section 6.5）
4. **14B模型性能上限**：Cosmos-Predict2.5-14B后训练完成后，性能提升幅度会有多大？
5. **跨领域泛化**：在智能空间、人体动力学等非机器人/驾驶领域的物理AI任务中，是否需要额外的领域自适应微调？

### 5. 知识库定位

Cosmos-Transfer2.5在视频世界模型知识库中的定位可概括为：

- **数据质量驱动范式**：通过极严格过滤（4%生存率）和语义去重，证明了数据质量对视频世界模型的根本性影响，与当前“数据为中心”的AI趋势一致。
- **小模型高效路线**：2B模型超越上一代7B模型，展示了架构优化（流匹配+RoPE+控制块均匀插入）和训练策略（RL后训练+模型合并）的组合效率，为资源受限的物理AI部署提供了可行路径。
- **物理AI垂直整合**：将视频生成与下游机器人策略训练、自动驾驶感知评估紧密结合，形成了从生成到应用的闭环验证体系，区别于纯视频生成模型的通用定位。

## 原文 PDF

![[paperPDFs/WHITEPAPER_2025/Cosmos_Transfer2_5_World_Simulation_With_Video_Foundation_Models_for_Physical_AI.pdf]]

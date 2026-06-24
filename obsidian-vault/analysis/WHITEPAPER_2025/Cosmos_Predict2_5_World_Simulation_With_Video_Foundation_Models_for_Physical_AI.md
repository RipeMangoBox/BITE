---
title: "Cosmos-Predict2.5: World Simulation With Video Foundation Models for Physical AI"
type: paper
paper_level: A
venue: Whitepaper
year: 2025
pdf_ref: paperPDFs/WHITEPAPER_2025/Cosmos_Transfer2_5_World_Simulation_With_Video_Foundation_Models_for_Physical_AI.pdf
project_link: https://www.nvidia.com/en-us/ai/cosmos/
aliases:
- CP5
- CP5WSVFMPA
tags:
- WHITEPAPER_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用流匹配（flow matching）架构替代扩散模型；用Cosmos-Reason1解码器式视觉语言模型替换T5文本编码器；引入领域特定的监督微调和基于强化学习的后训练；升级大规模视频数据筛选管道以提高数据质量和多样性。"
primary_logic: "通过从扩散范式转向流匹配训练、集成专门用于物理AI的视觉语言模型作为文本编码器、并施加面向物理场景的SFT与RL后训练，可以系统性提升世界模型在多个物理AI领域的视频真实感、一致性和指令遵循能力。"
claims:
- "Cosmos-Predict2.5-2B在PAI-Bench Text2World和Image2World基准上分别达到0.768和0.810的Overall Score，超越前代模型及部分外部模型。"
- "Cosmos-Transfer2.5-2B以3.5倍更小的体积，在多种控制条件下取得了比Cosmos-Transfer1-7B更高的质量分数和控制一致性。"
- "使用Cosmos-Transfer2.5-2B生成数据增强后，机器人策略在10个测试场景中成功率达24/30，远超基础策略（1/30）和常规增强策略（5/30）。"
- "强化学习后训练显著提升了生成视频的人类偏好度，在Text2World和Image2World两种模式下VideoAlign奖励分数均大幅提高。"
---

# Cosmos-Predict2.5: World Simulation With Video Foundation Models for Physical AI

> [!tip] 核心洞察
> 通过从扩散范式转向流匹配训练、集成专门用于物理AI的视觉语言模型作为文本编码器、并施加面向物理场景的SFT与RL后训练，可以系统性提升世界模型在多个物理AI领域的视频真实感、一致性和指令遵循能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cosmos-Predict2.5：面向物理AI的基于视频基础模型的世界模拟 |
| 英文题名 | Cosmos-Predict2.5: World Simulation With Video Foundation Models for Physical AI |
| 会议/期刊 | Whitepaper 2025 |
| Links | [paper](https://d1qx31qr3h6wln.cloudfront.net/publications/World_Simulation_with_Video_Foundation_Models_for_Physical_AI.pdf); [GitHub](https://github.com/nvidia-cosmos/cosmos-transfer2.5); [Project](https://www.nvidia.com/en-us/ai/cosmos/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Cosmos-Predict2.5 |
| Dataset | PAI-Bench-Predict-Text2World, PAI-Bench-Predict-Image2World, Transfer Model Quality, Real-Robot Policy Testing (10 scenarios) |

> [!tip] 效果简介
> - PAI-Bench-Predict-Text2World 上，Overall Score 为 0.768 (Cosmos-Predict2.5-2B post-trained)，对比 N/A (best in benchmark)，变化 N/A。
> - PAI-Bench-Predict-Image2World 上，Overall Score 为 0.810 (Cosmos-Predict2.5-2B post-trained)，对比 N/A (best in benchmark)，变化 N/A。
> - Transfer Model Quality 上，Quality Score 为 9.31 (Cosmos-Transfer2.5-2B Uniform Weights)，对比 9.24 (Cosmos-Transfer1-7B Uniform Weights)，变化 +0.07。

## 概述

**问题背景**：构建能够真实模拟物理世界动态的视频世界模型，是通向具身智能与物理AI的关键路径。然而，现有方法普遍面临视频生成质量不足、对复杂指令的语义跟随能力弱、长时序生成一致性差，以及缺乏面向物理AI场景的统一训练框架等瓶颈。前代模型**Cosmos-Predict1**采用扩散模型训练范式与T5文本编码器，其生成真实感和语义对齐能力受限，且缺少针对机器人、自动驾驶等物理领域的专用后训练策略。

**核心思路**：**Cosmos-Predict2.5**通过三个系统性升级来解决上述问题：（1）将训练范式从扩散模型切换为**流匹配（Flow Matching）**，使去噪网络直接预测速度场，并引入偏移对数正态分布以强化高噪声区域的学习；（2）用面向物理AI的解码器式视觉语言模型**Cosmos-Reason1**替代T5文本编码器，拼接多块激活并投影到1024维空间，以提供更丰富的文本语义与视觉条件扩展能力；（3）引入面向五个物理AI领域（机器人、自动驾驶、智能空间、人体动态、物理）的监督微调（SFT）、模型合并（Model Soup）以及基于VideoAlign奖励模型和GRPO算法的强化学习后训练，系统性提升指令遵循与视频质量。

**方法定位**：Cosmos-Predict2.5是一个基于DiT架构的流匹配潜在视频生成模型，统一支持Text2World、Image2World和Video2World三种世界模拟模式。它使用WAN2.1 VAE进行视频压缩（压缩率4×8×8），并采用1×2×2分块策略生成93帧（约5.8秒）16fps视频。模型发布2B和14B两个规模，其中2B版本已完成完整的预训练与后训练流程，并配套发布了**Cosmos-Transfer2.5**控制网络，用于多模态条件下的世界翻译与长视频自回归生成。

**主要结果**：在PAI-Bench基准上，后训练后的Cosmos-Predict2.5-2B在Text2World和Image2World模式下分别取得0.768和0.810的Overall Score，超越前代及外部模型。Cosmos-Transfer2.5-2B以仅约1/3.5的参数量，在多种控制条件下获得9.31的质量分数，优于7B的前代模型（9.24）。在真实机器人策略评估中，使用Cosmos-Transfer2.5生成数据增强后，策略在10个测试场景中成功率达24/30，远超基础策略（1/30）和常规增强策略（5/30）。强化学习后训练使VideoAlign奖励分数在Text2World下从1.08提升至1.69，在Image2World下从0.23提升至0.42，人类投票也一致确认质量改善。在自动驾驶多视图生成和动作条件视频预测等下游任务上，模型同样展现出显著的性能优势。

## 背景与动机

**物理AI的核心挑战：世界仿真器的缺位**

物理AI（Physical AI）系统——涵盖自动驾驶、机器人操作、智能空间等——需要在真实物理世界中感知、推理与行动。训练这些系统依赖海量、多样且带标注的交互数据，但物理世界数据的采集成本极高、覆盖场景有限且存在安全风险。因此，构建能够生成高保真、物理一致、指令可控的视频世界模型（World Simulator），以替代或增强真实数据采集，成为推动物理AI发展的关键技术路径。

**现有世界模型的关键瓶颈**

尽管视频生成领域近年来取得显著进展，但现有模型在物理AI场景下仍存在系统性不足：

1. **视频质量与物理一致性不足**：前代模型（如Cosmos-Predict1）采用扩散模型（Elucidated Diffusion Model, EDM）训练范式，生成视频在时序连贯性和视觉真实感上存在明显局限，尤其在长序列生成中容易出现突然过渡伪影（transition artifacts）。
2. **文本语义对齐弱**：Cosmos-Predict1使用通用T5文本编码器，缺乏对物理场景（如机器人动作、驾驶语义、空间关系）的深层理解，导致生成的视频与复杂指令之间的语义对齐度不足。
3. **缺乏面向物理AI的专门后训练**：现有模型通常仅进行通用预训练，未针对机器人、自动驾驶等特定领域进行监督微调（SFT）或偏好对齐（RLHF/RL），难以满足各物理AI子领域对视频生成的差异化需求。
4. **训练框架与数据管道的局限性**：数据筛选管道不够严格（前代管道保留率约30%），训练数据中低质量、冗余片段占比较高；同时缺少统一的逐步预训练策略来系统提升模型的分辨率和任务多样性。

**本文动机：系统性升级世界仿真器**

为突破上述瓶颈，Cosmos-Predict2.5提出了一套覆盖数据、架构、训练范式和后训练策略的系统性改进方案：

- **数据层**：升级为七阶段视频筛选管道，将片段保留率从约30%压缩至约4%，从3500万小时原始视频中精选出2亿高质量片段，并针对五个物理AI领域（机器人、自动驾驶、智能空间、人体动态、物理）构建领域专用标注数据。
- **架构层**：从扩散模型转向**流匹配（Flow Matching）**训练范式，以预测速度场替代噪声预测；将文本编码器从T5替换为专门面向物理AI的解码器式视觉语言模型**Cosmos-Reason1**；移除绝对位置嵌入，仅保留3D RoPE相对位置嵌入以支持任意分辨率和长度的推理。
- **训练策略层**：采用从低分辨率Text2Image到高分辨率Video2World的逐步预训练，并引入偏移对数正态分布采样以偏置高噪声区域，有效抑制过渡伪影。
- **后训练层**：首次为世界模型引入领域特定SFT、模型合并（Model Soup）以及基于VideoAlign奖励模型和GRPO算法的强化学习后训练，系统提升模型在各物理AI领域的指令遵循能力和视频质量。

通过上述多维度的协同改进，Cosmos-Predict2.5旨在构建一个更统一、更可控、更高质量的视频世界仿真器，为物理AI的下游应用（如机器人策略学习、自动驾驶仿真）提供更可靠的生成式数据支撑。

## 核心创新

Cosmos-Predict2.5 的核心创新在于对前代 Cosmos-Predict1 世界模型进行了系统性的范式重构，通过四个关键槽位的变更，从根本上解决了视频质量不足、指令跟随弱和生成不一致等瓶颈。

### 从扩散模型到流匹配的训练范式迁移

Cosmos-Predict1 采用 Elucidated Diffusion Model (EDM) 作为生成范式，而 Cosmos-Predict2.5 全面转向**流匹配**。模型不再预测去噪方向，而是预测扩散轨迹的速度场 $\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$，并通过最小化均方误差损失进行训练：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{x}, \boldsymbol{\epsilon}, \mathbf{c}, t} \left\| \mathbf{u}(\mathbf{x}_t, t, \mathbf{c}; \boldsymbol{\theta}) - \mathbf{v}_t \right\|^2$$

其中 $\mathbf{x}_t = (1 - t) \mathbf{x} + t \boldsymbol{\epsilon}$ 为数据与噪声的线性插值。为增强对高噪声区域的建模能力，训练时采用了**偏移对数正态分布**对时间步 $t$ 进行采样，并通过单调递增变换 $t_s = \frac{\beta t}{1 + (\beta - 1) t}$ 将采样分布偏向高噪声区间。这一设计配合将 5% 的训练样本显式从最高 2% 噪声区间采样的策略，显著减少了生成视频中的突然过渡伪影（Section 4.1）。

### Cosmos-Reason1 视觉语言模型替代 T5 文本编码器

文本编码器从通用的 T5 编码器升级为**Cosmos-Reason1**，这是一个面向物理 AI 的解码器式视觉语言模型。具体实现中，模型拼接 Cosmos-Reason1 多个 Transformer 块的激活值，并投影到 1024 维空间，为去噪网络提供更丰富的语义条件。这一设计不仅增强了文本与生成视频之间的语义对齐，还为未来激活 Cosmos-Reason1 的视觉编码分支、实现图像/视频级别的细粒度风格控制预留了架构空间（Section 3.2, Figure 2）。

### 位置编码的精简与泛化能力提升

Cosmos-Predict2.5 移除了前代 DiT 架构中的**绝对位置嵌入**，仅保留**3D 旋转位置嵌入**。这一架构变更使模型摆脱了对固定分辨率和序列长度的依赖，支持任意分辨率和帧数的推理，为后续的长视频生成和跨分辨率泛化奠定了基础（Section 3.2）。

### 面向物理 AI 的领域后训练体系

Cosmos-Predict2.5 构建了完整的后训练流水线，这是前代模型所不具备的：

1. **领域特定监督微调**：针对机器人、自动驾驶、智能空间、人类动态和物理五个物理 AI 领域分别进行 SFT。消融实验表明，领域 SFT 在每个目标域上均显著提升了预训练基线的 win rate（Figure 3）。

2. **模型合并**：通过 Model Soup 方法将各领域 SFT 模型合并为统一模型，在保留通用域性能的同时集成各领域优势，性能优于任何单一领域模型（Figure 4）。

3. **强化学习后训练**：采用 VideoAlign 作为奖励模型，结合 GRPO 算法进行视频质量对齐。在 Text2World 模式下，VideoAlign 奖励分数从 1.08 提升至 1.69；在 Image2World 模式下，从 0.23 提升至 0.42（Table 6）。人类投票也一致证实 RL 后训练有效提升了生成视频的质量（Figure 5）。

### 视频分词器的升级

Cosmos-Predict2.5 采用 **WAN2.1 VAE** 作为视频分词器，压缩率为 $4 \times 8 \times 8$，随后进行 $1 \times 2 \times 2$ 的分块处理，生成 93 帧（约 5.8 秒）、16fps 的视频。这一分词器选择与流匹配架构协同，为高质量视频生成提供了更紧凑的潜在表示（Section 3.2）。

### 创新总结

上述创新构成了一个相互增强的系统：流匹配提供了更稳定的训练动力学和更快的推理收敛；Cosmos-Reason1 编码器强化了物理场景的语义理解；精简的位置编码释放了泛化潜力；而领域后训练体系则使通用世界模型能够精准适配物理 AI 的多样化需求。这一组合最终使 2B 参数的 Cosmos-Predict2.5 在 PAI-Bench Text2World 和 Image2World 基准上分别达到 0.768 和 0.810 的 Overall Score，超越了前代模型及部分外部模型（Table 8, Table 9）。

## 整体框架

Cosmos-Predict2.5是一个面向物理AI的统一世界模拟框架，其核心设计目标是通过架构、数据和训练策略的系统性改进，解决前代模型在视频质量、指令跟随和生成一致性上的瓶颈。该框架以**流匹配（Flow Matching）**为训练范式，以**Cosmos-Reason1视觉语言模型**为语义编码器，在单一模型中统一了Text2World、Image2World和Video2World三种生成模式。

### 数据与预处理管道

模型能力的根基在于一个七阶段视频筛选管道（Figure 1），该管道将超过3500万小时的原始视频转化为约2亿个高质量训练片段：

1. **镜头感知的视频分割**：将原始视频按镜头边界切分为独立片段。
2. **GPU加速转码**：统一编码格式与帧率。
3. **视频裁剪**：去除边缘冗余区域。
4. **多级过滤**：依次应用美学评分、运动强度、OCR、感知质量、语义伪影和VLM过滤器，最终仅约4%的片段通过全部筛选。
5. **自动标注**：为每个片段生成描述性文本。
6. **语义去重**：采用在线去重策略，将新片段与已保留片段比较，优先保留时间更早且分辨率更高的版本。
7. **分片**：使用26类内容分类器为片段分配语义标签，并按内容类型、分辨率、宽高比和时长进行多维分片。

在通用数据之上，框架还针对五个物理AI目标领域——机器人、自动驾驶、智能空间、人类动态和物理——设计了领域专用数据管道，收集并标注高质量视觉数据（Table 2, Table 5）。

### 模型架构核心

Cosmos-Predict2.5的生成主干基于潜在空间中的DiT（Diffusion Transformer）架构（Figure 2），但相较前代Cosmos-Predict1做出了三个关键改变：

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/005_Figure_2.jpg]]
*Figure 2: Overall architecture of [Cosmos-Predict2.5]. As shown on the right, in the latent space, the model applies repeated blocks of self-attention, cross-attention, and feed-forward MLP layers, modulated by adaptive layer normalization (scale, shift, gate) for a given time step ??. We leverage [Cosmos-Reason1] as the text encoder (shown on the left). [Cosmos-Reason1] can also accommodate visual inputs (image and video) beyond text, which we leave for future work*

- **训练范式切换**：从扩散模型（EDM）转向流匹配。模型预测速度场 $\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$，并采用偏移对数正态分布偏置高噪声区域的训练采样，以抑制生成视频中的突然过渡伪影。
- **文本编码器升级**：用Cosmos-Reason1解码器式VLM替换T5编码器。该编码器拼接多块激活并投影到1024维空间，提供更丰富的语义条件，并预留了未来视觉条件输入的扩展能力。
- **位置编码简化**：移除绝对位置嵌入，仅保留3D RoPE相对位置嵌入，使模型能泛化到任意分辨率和序列长度。

视频分词器采用WAN2.1 VAE，压缩率为4×8×8，随后进行1×2×2分块，生成93帧（约5.8秒）16fps的视频。在Image2World和Video2World模式下，框架采用帧替换策略——用条件帧替换生成序列的前几帧，以增强时序一致性。

### 训练与后训练流程

训练遵循渐进式策略，分为预训练和后训练两个阶段：

**预训练阶段**沿两条轴逐步增加难度：像素分辨率（从256p升至720p）和任务多样性（从Text2Image扩展到Video2World/Text2World），共分多个阶段（Table 4）。条件帧通过掩码方案标识——每个输入token由原始token与二进制掩码token拼接而成。

**后训练阶段**包含三个关键步骤：
1. **领域监督微调**：在五个物理AI领域上分别进行SFT，每个领域模型在目标域上均显著优于预训练基线（Figure 3）。
2. **模型合并**：通过Model Soup将各领域SFT模型合并为统一模型，在保留通用域性能的同时集成各领域优势（Figure 4）。
3. **强化学习对齐**：以VideoAlign作为奖励模型，采用GRPO算法对生成视频的质量进行优化，在Text2World和Image2World两种模式下均大幅提升奖励分数（Table 6），人类投票也一致确认质量改善（Figure 5）。

### 输入输出流

框架支持三种生成模式，输入输出关系如下：
- **Text2World**：文本描述 → 视频序列
- **Image2World**：文本描述 + 条件图像 → 视频序列（条件图像作为首帧或前几帧）
- **Video2World**：文本描述 + 条件视频片段 → 完整视频序列

所有模式均通过统一的流匹配去噪网络处理，条件信息（文本嵌入、条件帧）在潜在空间中通过交叉注意力和帧替换机制注入。

## 核心模块与公式推导

### 流匹配训练范式

Cosmos-Predict2.5 的核心训练范式从扩散模型转向**流匹配（Flow Matching）**。其基本思路是在数据 $\mathbf{x}$ 与噪声 $\boldsymbol{\epsilon}$ 之间建立线性插值路径：

$$\mathbf{x}_t = (1 - t) \mathbf{x} + t \boldsymbol{\epsilon}$$

其中时间步 $t$ 从对数正态分布采样。流匹配的目标是让模型预测该路径上的**真实速度场**：

$$\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$$

去噪网络 $\mathbf{u}(\cdot;\boldsymbol{\theta})$ 通过最小化预测速度与真实速度之间的均方误差来训练：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\mathbf{x}, \boldsymbol{\epsilon}, \mathbf{c}, t} \left\| \mathbf{u}(\mathbf{x}_t, t, \mathbf{c}; \boldsymbol{\theta}) - \mathbf{v}_t \right\|^2$$

其中 $\mathbf{c}$ 为条件信息（文本、图像等）。与 Cosmos-Predict1 使用的 Elucidated Diffusion Model (EDM) 相比，流匹配直接预测扩散轨迹的速度而非噪声，简化了训练目标的推导。

为增强高噪声区域的训练密度，模型引入**偏移对数正态分布**来偏置时间步采样。具体地，对原始时间步 $t$ 施加单调递增变换：

$$t_s = \frac{\beta t}{1 + (\beta - 1) t}$$

其中 $\beta$ 为偏移超参数。该变换将更多训练样本推向高噪声区间，有效抑制了生成视频中的突然过渡伪影——实验表明，仅将 5% 的训练样本从最高 2% 噪声区间显式采样，即可显著减少此类伪影。

### 去噪网络架构

去噪网络沿用 Cosmos-Predict1 的 **DiT（Diffusion Transformer）** 结构，在潜在空间中运行。其核心由重复的**自注意力、交叉注意力和前馈 MLP 层**组成，每层均由**自适应层归一化（AdaLN）** 调制，接受时间步和条件信息的控制。

与上一代的关键架构差异在于位置编码：Cosmos-Predict2.5 **移除了绝对位置嵌入，仅保留 3D RoPE 相对位置嵌入**。这一改动使模型能够泛化到任意分辨率和序列长度，为后续的长视频自回归生成和跨分辨率推理提供了架构基础。

### 文本编码器升级

文本条件编码从 **T5 编码器**替换为 **Cosmos-Reason1**——一个面向物理 AI 的解码器式视觉语言模型。具体做法是：拼接 Cosmos-Reason1 多层激活输出，对每个 token 投影到 1024 维空间，作为交叉注意力的文本条件。该编码器不仅提供更丰富的语义对齐，还预留了视觉编码分支，支持未来通过图像/视频条件实现风格控制等细粒度调控。

### 视频分词与分块策略

视频在进入潜在空间前，由 **WAN2.1 VAE** 进行压缩，压缩率为 $4 \times 8 \times 8$（时间×高度×宽度）。随后对潜在表征施加 $1 \times 2 \times 2$ 的分块策略，将时空维度进一步 token 化。标准生成配置为 93 帧、16 fps，对应约 5.8 秒的视频片段。

### 条件帧注入机制

在 Image2World 和 Video2World 模式下，模型采用**帧替换策略**：将生成序列的前几帧直接替换为条件帧，以强制时序一致性。为区分条件帧与待生成帧，每个输入 token 由原始 token 与一个二值掩码 token 拼接而成，掩码标记该位置是否为条件输入。

## 实验与分析

### 核心性能：PAI-Bench 基准

Cosmos-Predict2.5-2B 在物理 AI 专用的 PAI-Bench 基准上取得了领先的总体得分。在后训练（post-training）之后，模型在 Text2World 模式下的 Overall Score 达到 0.768，在 Image2World 模式下达到 0.810（Table 8、Table 9），超越了前代 Cosmos-Predict1 及部分外部模型。这表明从扩散范式转向流匹配、并引入领域特定后训练，系统性地提升了视频真实感和指令遵循能力。

### 世界翻译模型：更小但更强

Cosmos-Transfer2.5-2B 在多模态控制条件下以 **3.5 倍更小的体积**取得了比 Cosmos-Transfer1-7B 更高的质量分数（Uniform Weights Quality Score: 9.31 vs. 9.24，Table 10）。这意味着架构改进（流匹配、Cosmos-Reason1 文本编码器）在压缩模型规模的同时，仍然增强了控制一致性与生成保真度。

### 真实机器人策略验证

在 10 个真实机器人测试场景中，使用 Cosmos-Transfer2.5-2B 生成数据进行增强后训练的策略，成功次数达到 **24/30**，远超基础策略的 1/30 和常规增强策略的 5/30（Table 11）。这一结果直接证明了世界模型生成的合成数据对下游物理 AI 任务具有显著的策略迁移价值。

### 后训练策略的消融分析

后训练三阶段——领域监督微调（SFT）、模型合并（Model Soup）和强化学习（RL）——均对模型性能产生了可量化的增益：

- **领域 SFT**：在机器人、自动驾驶、智能空间、人类动态和物理五个目标域上，领域专用 SFT 模型相对于预训练基线的 win rate 均显著提升（Figure 3），验证了针对性数据与微调策略的必要性。
- **模型合并**：通过 Model Soup 合并各领域 SFT 模型，可以在保留通用域性能的同时集成各域优势，性能优于任何单一领域模型（Figure 4）。
- **强化学习后训练**：使用 VideoAlign 作为奖励模型、GRPO 算法进行 RL 后训练后，Text2World 模式下的 VideoAlign 奖励分数从 1.08 提升至 1.69，Image2World 模式下从 0.23 提升至 0.42（Table 6）；人类投票也一致确认 RL 提升了生成视频的质量（Figure 5）。

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/033_Figure.jpg]]

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/011_Table_6.jpg]]
*Table 6: Rewards of [Cosmos-Predict2.5-2B], before and after reinforcement learning on VideoAlign, for Text2World and Image2World settings*

### 动作条件视频预测与注入方式消融

在 Bridge 数据集上的动作条件视频预测任务中，Cosmos-Predict2.5-2B/robot/action-cond 取得了 PSNR 24.95、SSIM 0.85、Latent L2 0.28、FVD 146 的结果（Table 17），显著优于基线。消融实验进一步表明，通过时间嵌入（time embedding）注入动作条件优于交叉注意力或通道拼接方式，获得了最佳的 PSNR/SSIM/FVD（Table 18）。

### 训练稳定性与噪声调度

预训练阶段的一个关键发现是：将 5% 的训练样本从最高 2% 的噪声区间显式采样，可以显著减少生成视频中的突然过渡伪影（Section 4.1）。这一针对流匹配噪声调度的微调，有效提升了时序一致性，是高噪声区域偏置策略（shifted logit-normal distribution）在实践中的重要补充。

### 评估局限性与待验证方向

当前评估存在以下局限，需要人工核验或进一步实验确认：

- 人类评估仅在小样本上进行，自动化指标（FVD、FID）与人类感知的一致性有限。
- 多数实验基于 NVIDIA 自有数据集和基准，不同机构复现时可能因数据分布差异导致结果波动。
- Cosmos-Predict2.5-14B 的完整后训练尚未完成，大模型潜力的评估尚不全面。
- 世界仿真器在远离训练分布的开放场景中仍可能出现幻觉或违反物理规律的行为，这一点缺乏系统性量化分析。
- 强化学习奖励模型 VideoAlign 在更多样化的物理 AI 场景中的可靠性尚未验证，是否需要多目标奖励仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/019_Figure.jpg]]
*Figure: Edge Control Depth Control*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/020_Figure_9.jpg]]
*Figure 9: Error accumulation for long video generations. These plots show the Normalized Relative Dover Score vs Chunk Index for auto-regressive multi-trunk long video generation where each trunk is 93 frames. As shown, for all four control modalities (edge/blur/depth/seg), compared to [Cosmos-Transfer1-7B] (blue curves), [Cosmos-Transfer2.5-2B] (green curves) has much less reduction in RNDS along the chunk index dimension, which shows less hallucination and error accumulation for long videos*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/027_Figure_13.jpg]]
*Figure 13: Generated multi-view frames from [Cosmos-Transfer2.5-2B/auto/multiview]. The multi-view 720p control videos for driving simulation consist of HD map elements like lanes, road markings, poles, traffic signals, traffic lights (with state), all of which can represent complex road topologies (including overpasses) as well as actors represented as cuboids. Each cuboid is color-coded based on a coarse class ontology (e.g., truck, vehicle, pedestrian), and is also shaded to differentiate between the front and back*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/001_Table_1.jpg]]
*Table 1: List of released models with their corresponding capabilities and inputs*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/003_Table_2.jpg]]
*Table 2: Overview of high-quality robotics datasets with video counts by camera perspective*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/004_Table_3.jpg]]
*Table 3: Configuration details of [Cosmos-Predict2.5] models*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/006_Table_4.jpg]]
*Table 4: Stages of progressive pretraining and their specifications*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/007_Table_5.jpg]]
*Table 5: Video statistics across different post-train domains*

![[assets/figures/papers/paper_list_l38_https_d1qx31qr3h6wln_cloudfront_net_publications_World_Simulation_with_V/figures/012_Table_7.jpg]]
*Table 7: Training efficiency with 4096 NVIDIA H100 GPUs where the video resolution is 720p and number of frames is 93*

## 方法谱系与知识库定位

### 与前代模型的关系

Cosmos-Predict2.5 是 NVIDIA Cosmos 世界模型系列的直接演进，其前代模型 **Cosmos-Predict1** 和 **Cosmos-Transfer1** 构成了本文的基线。从方法谱系看，该系列遵循“视频基础模型 + 下游世界翻译”两阶段范式，但 Cosmos-Predict2.5 在三个核心维度上进行了系统性重构：

1. **训练范式切换**：Cosmos-Predict1 采用 Elucidated Diffusion Model（EDM）扩散框架，而 Cosmos-Predict2.5 转向**流匹配（Flow Matching）**，将去噪网络的目标从预测噪声改为预测扩散轨迹的速度场 $\mathbf{v}_t = \boldsymbol{\epsilon} - \mathbf{x}$。这一转变配合偏移对数正态分布（shifted logit-normal distribution）对高噪声区域的偏置采样，显著减少了生成视频中的突然过渡伪影。

2. **文本编码器升级**：Cosmos-Predict1 使用 T5 编码器进行文本条件注入，Cosmos-Predict2.5 替换为 **Cosmos-Reason1**——一个面向物理 AI 的解码器式视觉语言模型。该编码器通过拼接多块激活并投影到 1024 维空间，提供更丰富的语义基础，且架构上预留了未来视觉条件控制的扩展空间。

3. **后训练体系建立**：Cosmos-Predict1 仅停留在预训练阶段，而 Cosmos-Predict2.5 引入了完整的后训练管线：领域特定监督微调（SFT）→ 模型合并（Model Soup）→ 基于 VideoAlign 奖励模型和 GRPO 算法的强化学习（RL）。这一体系将通用世界模型适配到机器人、自动驾驶、智能空间、人类动态和物理五个物理 AI 领域。

在模型规模上，Cosmos-Predict2.5 提供 2B 和 14B 两个版本（Table 3），而 Cosmos-Transfer2.5-2B 以 **3.5 倍更小的体积**（相比 Transfer1-7B）在多种控制条件下取得了更高的质量分数（Table 10：Uniform Weights Quality Score 9.31 vs 9.24），体现了架构效率的显著提升。

### 与外部工作的关系

论文在人类评估中将 Cosmos-Predict2.5 与外部视频生成模型 **Wan2.2-5B** 和 **Wan2.1-14B** 进行了对比，但未提供详细的定量对比数据。在 PAI-Bench 基准上，Cosmos-Predict2.5-2B 的后训练版本在 Text2World 和 Image2World 上分别达到 0.768 和 0.810 的 Overall Score（Table 8, Table 9），被报告为该基准上的最佳结果，但需注意该基准可能缺乏广泛的外部模型参与，其相对排名需要更多独立验证。

在自动驾驶多视图生成任务上，Cosmos-Predict2.5-2B/auto/mv 在 RDS-HQ-HL 数据集上取得了 FVD StyleGAN 23.060、FVD I3D 25.308、FID 12.095 的成绩（Table 12），并与前代 Cosmos-Transfer1-7B-Sample-AV 形成对比。在动作条件视频预测任务上（Bridge 数据集），Cosmos-Predict2.5-2B/robot/action-cond 的 PSNR/SSIM/Latent L2/FVD 分别为 24.95/0.85/0.28/146（Table 17），相比基线有“substantial improvement”，但基线具体数值未在可验证材料中给出，需查阅原文确认。

### 适用边界与能力定位

Cosmos-Predict2.5 的能力边界可从以下维度界定：

- **输入模态**：当前仅支持文本和图像/视频作为条件输入，未融合音频、力反馈等其他物理感知模态。Cosmos-Reason1 的视觉编码分支虽在架构上预留但尚未激活，限制了细粒度视觉条件控制。
- **生成时长**：模型生成 93 帧（约 5.8 秒，16fps）视频。Transfer2.5 通过自回归多段生成长视频时，归一化相对 Dover 分数（RNDS）显示误差累积显著低于 Transfer1（Figure 9），但在极长序列（数十段）下仍会出现质量退化。
- **物理真实性**：世界仿真器在远离训练分布的开放场景中可能出现幻觉或违反物理规律的行为，训练目标中尚未显式引入物理定律约束。
- **领域覆盖**：后训练覆盖五个物理 AI 领域，但评估主要依赖自动化指标和有限的人类偏好研究，尚未在更广泛的真实物理 AI 下游任务（如全栈机器人部署）中验证。

### 局限与开放问题

**已确认的局限**：

1. Cosmos-Predict2.5-14B 的完整后训练尚未完成，大模型潜力的评估不全面。
2. 强化学习奖励模型 VideoAlign 在多样化物理 AI 场景中的可靠性未经验证，当前仅使用单一奖励目标。
3. 数据筛选管道中的 VLM 过滤器虽然提高了精度，但可能引入 VLM 自身的偏见，且计算成本较高。
4. 评估主要依赖自动化指标（FVD、FID 等），这些指标与人类感知的一致性存在已知偏差。

**开放问题**：

1. 如何激活 Cosmos-Reason1 的视觉编码分支，实现更细粒度的图像/视频条件控制？
2. 能否通过更好的位置编码扩展（当前仅保留 3D RoPE 相对位置嵌入）和推理策略，将一致性维持在数十秒乃至分钟级的长视频上？
3. 如何构建涵盖复杂多智能体交互、长期推理的综合物理 AI 世界模型基准？
4. 小型模型（2B）的优势能否通过蒸馏等方式迁移到更大模型，或反之？
5. 通过生成数据增强训练的策略（Table 11 中 24/30 的成功率）在更多机器人任务和真实世界部署中的泛化能力如何？

## 原文 PDF

![[paperPDFs/WHITEPAPER_2025/Cosmos_Transfer2_5_World_Simulation_With_Video_Foundation_Models_for_Physical_AI.pdf]]

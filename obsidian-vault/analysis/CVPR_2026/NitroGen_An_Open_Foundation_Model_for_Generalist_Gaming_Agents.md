---
title: "NitroGen: An Open Foundation Model for Generalist Gaming Agents"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NitroGen_An_Open_Foundation_Model_for_Generalist_Gaming_Agents.pdf
aliases:
- NitroGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 利用玩家直播中的输入覆盖层（input overlay）自动提取动作标签，将互联网上的游戏视频转变为大规模行为克隆训练数据。
primary_logic: 通过在40,000小时的公开游戏视频上自动解析游戏手柄动作，训练统一的视觉-动作基础模型，使代理无需人工演示即可学会跨游戏、跨类型的通用游戏技能。
claims:
- 从超过1,000款游戏中收集了40,000小时的带动作标签的视频，成为当前最大的游戏视频动作数据集。
- 无需针对特定游戏微调，预训练模型即可在多种游戏上实现非平凡的成功率。
- 在未见的游戏上微调，最高可获得52%的相对任务成功率提升。
- 游戏手柄动作提取平均摇杆R²=0.84，按钮帧准确率=0.96。
---

# NitroGen: An Open Foundation Model for Generalist Gaming Agents

> [!tip] 核心洞察
> 通过在40,000小时的公开游戏视频上自动解析游戏手柄动作，训练统一的视觉-动作基础模型，使代理无需人工演示即可学会跨游戏、跨类型的通用游戏技能。

| 字段 | 内容 |
|------|------|
| 中文题名 | NitroGen：面向通用游戏代理的开放基础模型 |
| 英文题名 | NitroGen: An Open Foundation Model for Generalist Gaming Agents |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.02427) · [arXiv](https://arxiv.org/abs/2410.24164) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | NitroGen |
| Dataset | Multi-game benchmark, Isometric roguelike, 3D action-RPG, Gamepad action extraction benchmark |

> [!tip] 效果简介
> - Multi-game benchmark (10 games, 30 tasks) 上，任务完成率 (零样本) 在多种游戏和任务上实现非平凡成功率 vs 无基线（纯预训练评估） (N/A)。
> - Isometric roguelike (held-out game, varying data quantity) 上，任务完成率相对提升 10% vs from scratch training (+10%)。
> - 3D action-RPG (held-out game, low-data regime 30h) 上，任务完成率相对提升 up to 52% vs from scratch training (+52%)。

## 概述

通用游戏代理面临一个核心瓶颈：缺乏大规模、多样化的带动作标签的视频数据集，以及统一的跨游戏评估基准，导致现有方法难以从视觉输入学习可泛化的游戏策略。NitroGen 通过一个关键的因果杠杆解决了这一问题——利用玩家直播中常见的输入覆盖层（input overlay）自动提取动作标签，将互联网上公开的游戏视频转变为大规模行为克隆训练数据。

核心洞察在于：通过在 40,000 小时、覆盖超过 1,000 款游戏的公开视频上自动解析游戏手柄动作，训练统一的视觉-动作基础模型，使代理无需人工演示即可学会跨游戏、跨类型的通用游戏技能。这一思路将数据获取成本从“人工录制演示”降为“互联网视频自动标注”，从根本上改变了通用游戏代理的规模化路径。

主要结果验证了这一范式的有效性：
- 预训练模型在多种未见游戏上实现了非平凡（non-trivial）的零样本任务成功率（Figure 6）。
- 在下游未见游戏上微调后，相对从头训练的模型，任务成功率最高可提升 52%（Figure 7b）。
- 动作提取流水线自身也具备高可靠性：摇杆位置的平均 R² 达到 0.84，按钮帧准确率达到 0.96（Figure 5）。

NitroGen 的方法定位介于“单游戏专用策略”与“依赖语言模型的复合系统”之间，构建了首个面向通用游戏的视觉-动作基础模型。其训练范式采用视觉-动作 Transformer（SigLIP 2 ViT + DiT）结合流匹配目标，在互联网规模数据上端到端训练，无需针对特定游戏微调即可展现跨游戏能力。同时，配套构建的通用模拟器通过拦截系统时钟实现帧级同步控制，为任意商业游戏提供统一的 Gymnasium API，填补了跨游戏评估基准的空白。

需要指出的是，当前模型仅基于纯视觉-动作映射，不支持自然语言指令，且数据集偏向动作 RPG 和平台跳跃等游戏类型，对策略、模拟等依赖复杂规划或键盘操作的游戏泛化能力尚待验证。这些限制指明了后续扩展的方向。

## 背景与动机

### 通用游戏代理的核心瓶颈

构建能在各种电子游戏中自主操作的通用代理，是人工智能领域长期以来的挑战。与棋盘游戏或受控模拟环境不同，商业电子游戏具有视觉丰富、动态变化、目标多样且缺乏统一程序化接口的特点。当前方法面临两大结构性瓶颈：

**数据稀缺**：训练具备泛化能力的游戏代理需要大规模、多样化的带动作标签的视觉数据。然而，现有数据集的构建严重依赖人工演示收集或特定模拟器 API 的交互数据，每个游戏通常只能获得数十到数百小时的标注数据。这种方式不仅成本高昂，且难以覆盖游戏类型的多样性，从根本上限制了代理的泛化边界。

**评估碎片化**：不同游戏拥有各自独立的操作接口、观测空间和任务定义，缺乏统一的跨游戏评估基准。研究者通常针对单一游戏设计专用环境和策略网络，导致方法之间难以进行公平比较，也无法衡量代理在未见过游戏上的迁移能力。

这两大瓶颈相互强化：数据获取的困难使得模型倾向于在单一游戏上过拟合，而评估标准的缺失又削弱了研究者构建通用系统的动力。因此，该领域亟需一种能够以低成本获取大规模跨游戏训练数据，并在统一接口下进行系统评估的新范式。

### 现有方法的局限

当前游戏代理的研究大致可分为三类，但每一类都难以同时满足通用性、可扩展性和实用性的要求：

1. **单游戏专用系统**：针对特定游戏设计的小型策略网络或基于规则的代理，在各自领域内可能表现优异，但完全不具备跨游戏迁移能力。这类方法需要为每个新游戏重新设计状态表示和动作空间，工程成本与游戏数量线性增长。

2. **基于语言模型的复合系统**：利用视觉-语言模型（VLM）理解游戏画面并生成高层计划，再通过底层控制器执行。虽然具备一定的零样本泛化潜力，但依赖语言作为中介引入了推理延迟和语义歧义，且无法直接学习精细的实时操控技能。更重要的是，这类方法通常需要游戏特定的文本描述或 API 支持，难以在纯视觉条件下端到端运行。

3. **行为克隆方法**：从人类演示数据中学习视觉到动作的直接映射。这是最接近人类学习方式的技术路线，但传统行为克隆受限于数据规模——每个游戏的演示数据通常只有几十小时，无法支撑跨游戏泛化所需的视觉多样性和策略多样性。

### 解锁互联网规模的游戏数据

NitroGen 的核心洞察在于识别了一种被忽视的大规模数据来源：**游戏直播和录播视频中的输入覆盖层（input overlay）**。许多内容创作者在分享游戏视频时，会实时显示自己的手柄输入状态——包括摇杆位置和按钮按压情况。这些覆盖层以视觉形式直接嵌入视频画面中，本质上构成了帧级别的动作标签。

这一发现意味着，互联网上已有的海量游戏视频可以被转化为行为克隆的训练数据。关键挑战在于如何从视频中自动、准确地提取这些动作信息。NitroGen 提出了一套完整的自动化流水线来解决这一问题：

- **模板匹配定位**：利用 SIFT 和 XFeat 特征匹配，在约 300 种常见手柄模板中定位覆盖层区域
- **语义分割解析**：通过微调的 SegFormer 模型解析摇杆位置和按钮状态
- **质量过滤**：仅保留动作密度≥50% 的视频片段，防止模型坍缩至空动作

通过这套流水线，NitroGen 从超过 1,000 款游戏中收集了 40,000 小时的带动作标签视频，成为当前最大的游戏视频动作数据集。这一规模是传统人工收集数据的数百倍，且覆盖了动作 RPG（34.9%）、平台跳跃（18.4%）、动作冒险（9.2%）等多种游戏类型。

### 统一评估与端到端训练

在数据规模突破的基础上，NitroGen 进一步构建了两个关键基础设施：

**通用游戏模拟器**：通过拦截系统时钟实现帧级同步控制，为任意商业游戏提供统一的 Gymnasium API。这使得模型可以在完全相同的接口下与不同游戏交互，支持 10 款商业游戏上的 30 个标准化任务评估。

**视觉-动作基础模型**：采用 SigLIP 2 视觉编码器与扩散 Transformer（DiT）相结合的架构，通过条件流匹配（conditional flow matching）目标在 40,000 小时数据上进行端到端训练。模型仅需单帧 256×256 RGB 图像作为输入，即可生成 16 步未来动作序列，无需任何语言指令或游戏特定信息。

这种设计哲学——纯粹从视觉到动作的映射、大规模跨游戏数据、统一的评估接口——使得 NitroGen 成为一个真正意义上的游戏基础模型：预训练后无需微调即可在多种游戏上展现非平凡的操作能力，而经过少量微调后，在未见过的游戏上可获得最高 52% 的相对任务成功率提升。

## 核心创新

NitroGen 的核心创新在于**将通用游戏代理的训练从“人工演示驱动”转变为“互联网数据驱动”**，通过三个关键环节的系统性重构，突破了此前通用游戏代理面临的数据规模瓶颈。

### 数据来源的范式转换：从人工采集到互联网挖掘

传统游戏代理的训练数据高度依赖人工收集的演示数据，或通过特定模拟器 API 获取的交互轨迹，每条数据都需要高昂的采集成本。NitroGen 首次提出利用公开互联网视频中**游戏手柄覆盖层（input overlay）**作为动作标签的来源——内容创作者在直播或录制时叠加在画面上的实时按键与摇杆显示（Figure 2）。这一思路将数据获取成本降至近乎为零，使训练数据规模从传统方法的“每游戏数十至数百小时”跃升至 **40,000 小时视频，覆盖超过 1,000 款游戏**（Figure 3），成为当前最大的游戏视频动作数据集。

### 动作提取的自动化：从人工标注到解析流水线

从覆盖层中提取动作并非简单任务——视频压缩、控制器样式差异、透明度变化等因素使得直接识别极具挑战。NitroGen 构建了一套三阶段自动化解析流水线：
1. **模板匹配定位**：使用 SIFT 和 XFeat 特征对约 300 种常见手柄模板进行匹配，定位并裁剪覆盖层区域；
2. **语义分割解析**：基于 SegFormer 微调的语义分割模型，精确解析摇杆位置和按钮状态；
3. **质量过滤**：仅保留动作密度 ≥50% 的片段（丢弃约 45% 数据），防止模型坍缩至空动作。

该流水线在测试中达到**摇杆 R² = 0.84、按钮帧准确率 = 0.96** 的提取精度（Figure 5），为大规模行为克隆提供了可靠的动作标签。

### 模型架构与训练范式的统一：从单游戏策略到视觉-动作基础模型

NitroGen 将模型设计为统一的**视觉-动作 Transformer**：以 SigLIP 2 编码单帧 256×256 RGB 图像，通过 DiT 结合流匹配目标生成 16 步未来动作序列。与依赖语言模型或多模块复合的传统方案不同，NitroGen 完全摒弃语言条件，专注于可扩展的视觉-动作映射。这一设计使其成为一个可跨游戏迁移的**基础模型**——预训练后无需微调即可在多种游戏上实现非平凡的任务成功率（Figure 6），在未见游戏上微调后最高可获得 **52% 的相对任务成功率提升**（Figure 7(b)）。

### 评估环境的标准化：从单一模拟器到通用 Gymnasium 封装

为支撑跨游戏评估，NitroGen 开发了**通用游戏模拟器**：通过拦截系统时钟实现帧级同步控制，为任意商业游戏提供统一的 Gymnasium API。这一封装支持 10 款商业游戏的 30 个任务，为通用游戏代理提供了此前缺失的标准化评估基准。

综上，NitroGen 的创新本质在于**将数据、模型、评估三个维度同时从“游戏特定”推向“跨游戏通用”**，其因果杠杆是覆盖层动作提取技术——正是这一技术使得互联网海量游戏视频能够转化为可用的训练信号，从而支撑起通用视觉-动作基础模型的训练。

## 整体框架

NitroGen 的整体框架由三个核心组件构成，它们协同工作，形成一个从互联网视频数据到通用游戏代理的端到端流水线（Figure 1）。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/001_Figure_1.jpg]]
*Figure 1: NitroGen overview. NitroGen consists of three main components: (1) Multi-game foundation agent (center) - a generalist vision-action model that takes in game observations and generates gamepad actions, enabling zero-shot gameplay across multiple titles and serving as a foundation for fine-tuning on new games; (2) Universal simulator (left) - an environment wrapper that allows any commercial game to be controlled through a Gymnasium API; and (3) Internet-scale dataset (right) - the largest and most diverse open-source gaming dataset curated from 40,000 hours of publicly available gaming videos, spanning more than 1,000 games with extracted action labels*

**流水线总览**：系统首先从公开视频中自动提取游戏手柄动作，构建大规模视觉-动作数据集；然后在该数据集上预训练一个统一的视觉-动作基础模型；最后通过一个通用模拟器接口，使该模型能够在任意商业游戏中执行任务。

**三大组件及其关系**：

1. **互联网规模视频-动作数据集（Internet-scale Video-Action Dataset）**：这是整个系统的数据基础。流水线从包含“输入覆盖层”（input overlay）的公开游戏视频中收集了71,000小时原始视频，经过质量过滤后保留40,000小时，覆盖超过1,000款游戏（Figure 3）。动作提取通过三阶段流水线完成：模板匹配定位覆盖层区域、SegFormer语义分割解析摇杆位置与按钮状态、时序后处理确保动作标签质量。该组件输出帧级对齐的（观测图像，游戏手柄动作）对，作为下游模型训练的唯一监督信号。

2. **通用游戏模拟器（Universal Game Simulator）**：该组件通过拦截游戏引擎的系统时钟，为任意商业游戏提供标准的 Gymnasium API 接口。它将游戏的原始画面帧作为观测输出，同时接收模型生成的动作指令并注入游戏。这一设计使得 NitroGen 能够在10款商业游戏、30个任务上进行统一的评估和微调，无需依赖特定游戏的模拟器或 API。

3. **多游戏基础代理（Multi-game Foundation Agent）**：这是系统的核心决策模块。模型以单帧 256×256 RGB 游戏画面作为输入，通过 SigLIP 2 视觉编码器提取特征，再由基于 DiT（Diffusion Transformer）的动作解码器结合流匹配（flow matching）目标，从高斯噪声中逐步去噪，生成未来16步的游戏手柄动作序列。该模型完全基于视觉-动作映射，不依赖语言指令或游戏内部状态。

**输入输出流**：在推理时，通用模拟器将当前游戏画面帧送入视觉编码器，编码后的特征与噪声动作拼接后进入 DiT 解码器，经16步欧拉积分去噪后输出连续动作序列。模拟器按帧率逐步执行这些动作，并将新的观测帧反馈给模型，形成闭环控制。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/002_Figure.jpg]]
*Figure: (a) Examples of gamepad overlay videos. Gamepad cropping Action extraction*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/003_Figure.jpg]]

## 核心模块与公式推导

### 互联网规模视频-动作数据集构建

NitroGen 的核心创新在于绕过人工演示收集，直接从互联网公开视频中自动提取游戏手柄动作标签。该流水线分为三个阶段：

**阶段一：游戏手柄覆盖层定位。** 系统维护约 300 种常见手柄模板库，对每个视频采样 25 帧，使用 SIFT 和 XFeat 特征进行模板匹配，定位并裁剪出覆盖层区域。

**阶段二：游戏手柄动作解析。** 在裁剪出的覆盖层区域上，使用微调后的 SegFormer 语义分割模型同时解析摇杆位置的回归值和按钮状态的多标签分类。模型在合成数据集上训练，通过域随机化（随机背景、手柄样式、覆盖层透明度）增强泛化能力。

**阶段三：质量过滤与时序后处理。** 仅保留动作密度 ≥ 50% 的片段（即至少一半时间步存在非零按钮或摇杆动作），丢弃约 45% 的无效数据，防止模型坍缩至空动作输出。最终数据集包含 40,000 小时视频，覆盖超过 1,000 款游戏，其中 846 款游戏超过 1 小时数据，91 款超过 100 小时，15 款超过 1,000 小时。

### 通用游戏仿真器

为统一评估接口，NitroGen 开发了一个通用仿真器，通过拦截游戏引擎的系统时钟实现帧级同步控制，将任意商业游戏包装为 Gymnasium API。该仿真器提供标准化的观测-动作空间，支持暂停、步进和重置操作，使模型能在完全相同的接口下评估多款游戏。

### 视觉-动作模型架构

NitroGen 采用视觉-动作 Transformer 架构，由两个核心组件构成：

- **视觉编码器**：使用 SigLIP 2 ViT 将单帧 256×256 RGB 图像编码为视觉特征。实验发现使用多帧历史并未带来额外收益，因此仅使用当前帧作为观测输入。
- **动作解码器**：基于 Diffusion Transformer（DiT）架构，以流匹配目标生成 16 步未来动作序列。相比单步生成，动作块生成显著改善了时间一致性。

### 流匹配公式推导

NitroGen 将动作生成建模为条件流匹配问题。给定观测 $o$ 和真实动作序列 $a$，训练目标是从高斯噪声逐步恢复动作。

**含噪动作构造：**
$$a_{t} = (1 - t) \cdot \epsilon + t \cdot a$$
其中 $t \in [0, 1]$ 为流匹配时间步，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。当 $t=0$ 时 $a_t = \epsilon$（纯噪声），$t=1$ 时 $a_t = a$（真实动作）。

**条件速度场：**
$$\mathbf{u}^{\mathrm{cond}}(\mathbf{x}, t, \mathbf{a}, \epsilon, \mathbf{o}) = \mathbf{a} - \epsilon$$
速度场定义为真实动作与噪声的差，表示从噪声指向真实动作的恒定方向向量。

**条件流匹配损失：**
$$\mathcal{L}^{\mathrm{CFM}}(\theta, \phi) = \mathbb{E}_{t, a, \epsilon}\left[ \| \pi_{\theta}(a_{t}, \psi_{\phi}(o), t) - (a - \epsilon) \|^{2} \right]$$
其中 $\psi_{\phi}$ 为视觉编码器（参数 $\phi$），$\pi_{\theta}$ 为 DiT 策略网络（参数 $\theta$）。损失函数最小化模型预测的速度与目标速度之间的均方误差，联合训练视觉编码器和扩散 Transformer。

### 推理过程

推理时从纯高斯噪声 $a_0 \sim \mathcal{N}(0, I)$ 出发，使用欧拉积分进行 $k=16$ 步去噪：

$$a_{t + 1/k} = a_{t} + \frac{1}{k} \pi_{\theta}(a_{t}, \psi_{\phi}(o), t)$$

每一步沿模型预测的速度方向推进 $1/k$ 步长，从 $t=0$ 逐步积分至 $t=1$，最终输出 16 步动作序列。模型使用指数移动平均（EMA）权重（衰减率 0.9999），实验表明 EMA 权重始终优于非 EMA 权重。

### 训练配置

模型使用 AdamW 优化器（权重衰减 0.001），采用预热-稳定-衰减学习率调度，稳定阶段学习率为常数 0.0001。数据增强包括随机亮度、对比度、饱和度、色调扰动，以及 ±5° 随机旋转和随机裁剪。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/004_Figure.jpg]]
*Figure: Input video frame Gamepad localization with template matching*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/005_Figure.jpg]]

## 实验与分析

### 动作解析流水线精度验证

NitroGen 的训练数据质量直接取决于从视频覆盖层提取游戏手柄动作的精度。作者构建了一个包含多种手柄家族（Xbox、PlayStation、Nintendo Switch Pro 等）的标注基准，以地面真值动作日志为参考，量化评估解析流水线的性能。**图5** 展示了核心结果：

- **摇杆位置回归**：平均 R² 分数达到 **0.84**，表明解析模型能够高度准确地恢复玩家施加的摇杆方向与幅度。不同手柄家族之间存在细微差异，但整体一致性良好。
- **按钮状态分类**：帧级按钮准确率达到 **0.96**，说明“按下/释放”的二值判断几乎与人工标注一致。

这一精度水平为后续的行为克隆训练提供了可靠的动作监督信号。需要注意的是，该评估假设覆盖层在视频中清晰可见；在实际互联网视频中，压缩伪影、透明度变化或非标准皮肤可能导致局部精度下降，但整体流水线的鲁棒性已通过大规模数据筛选得到验证。

### 零样本预训练性能

NitroGen 的核心主张是：仅通过互联网视频的行为克隆预训练，模型即可在未见过（或仅通过视频“见过”）的商业游戏中展现非平凡的游戏能力。**图6** 报告了 NitroGen 500M 参数模型在 10 款游戏、30 个任务上的零样本任务完成率（每任务 5 次 rollout 取平均）。

主要发现包括：

- **跨游戏泛化成立**：模型在多种 2D 和 3D 游戏中均能完成部分任务，包括需要记忆固定路线和需要在程序生成世界中自适应探索的任务。
- **非平凡成功率**：虽然绝对成功率因游戏和任务难度而异，但模型远非随机策略——它学会了移动、跳跃、攻击等基础操作，并在部分任务中展现出连贯的行为序列。
- **单帧上下文足够**：消融实验表明，使用多于 1 帧的历史观测并未带来性能增益。模型仅依赖当前帧即可生成合理的动作序列，这简化了架构设计并降低了推理延迟。

需要指出，零样本评估依赖人工评判任务完成与否，且仅覆盖 30 个特定任务，因此对模型综合能力的估计可能存在偏差。此外，成功率在游戏间差异显著，反映出预训练数据分布不均的影响。

### 迁移学习与微调增益

为量化预训练权重的迁移价值，作者在两个未见过的游戏上对比了 **从 NitroGen 权重微调** 与 **从头训练（随机初始化）** 的效果。**图7** 展示了关键结果：

- **等距视角 Roguelike 游戏（可变数据量）**：在不同微调数据规模下，预训练模型始终优于从头训练，平均相对任务完成率提升 **10%**。这表明预训练学到的视觉-动作先验即使在数据相对充足时仍有正向迁移。
- **3D 动作 RPG 游戏（低数据场景，30 小时）**：这是最具说服力的证据——预训练模型微调后，相对任务成功率提升最高可达 **52%**。在数据稀缺的条件下，NitroGen 的通用游戏知识显著加速了下游任务的学习，验证了其作为基础模型的核心价值。

### 关键消融与设计选择

除了上述核心结果，论文还通过消融实验验证了若干关键设计决策：

| 消融项 | 结论 | 证据强度 |
|--------|------|----------|
| 动作块长度 | 生成 16 步动作块优于单步生成，改善了时间一致性 | 中等（定性描述） |
| 数据过滤阈值 | 仅保留动作密度 ≥ 50% 的片段（丢弃约 45% 数据），防止模型坍缩至“空动作” | 强（训练稳定性关键） |
| EMA 权重 | 衰减系数 0.9999 的指数移动平均权重始终优于非 EMA 权重 | 强（所有结果均使用 EMA） |
| 多帧历史 | 使用多于 1 帧历史无额外收益 | 中等（经验观察） |

其中，**动作密度过滤** 是最关键的工程决策。互联网视频中存在大量过场动画、菜单浏览等无操作片段，若不加过滤直接训练，模型会倾向于输出“什么都不做”的坍缩策略。保留至少 50% 时间步包含非零动作的片段，有效缓解了这一问题。

### 失败模式与局限性

尽管 NitroGen 展现了令人鼓舞的泛化能力，其失败模式揭示了当前方法的边界：

1. **长时程任务退化**：模型缺乏显式记忆与规划机制，在需要数分钟以上持续上下文的任务中（如迷宫探索、多阶段解谜），行为逐渐偏离目标。
2. **游戏类型偏差**：预训练数据以动作 RPG（34.9%）和平台跳跃（18.4%）为主，导致模型在策略游戏、模拟经营等依赖复杂决策的类型上表现未知。
3. **输入模态限制**：模型仅处理游戏手柄信号，无法应对键盘+鼠标输入的游戏（如 FPS、RTS），也缺乏对自然语言指令的响应能力。
4. **同步仿真假设**：推理时通过暂停系统时钟实现帧级同步，虽然在测试中未破坏游戏物理，但在实时或异步部署环境下的鲁棒性未经检验。
5. **覆盖层依赖脆弱性**：动作解析完全依赖视频中的手柄覆盖层，一旦覆盖层缺失、被遮挡或风格异常，数据质量急剧下降。

这些失败模式指向了未来的改进方向：引入世界模型进行前向预测、结合语言指令实现任务条件化、扩展输入模态支持键盘鼠标，以及探索离线强化学习对预训练策略的进一步精炼。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/008_Figure_5.jpg]]
*Figure 5: Gamepad parsing performance for different controller families. We verify the correctness of our action extraction pipeline by comparing performance across different controller families against ground-truth data. (a) shows joystick R2 correlation scores (averaged for both left and right joysticks) with an overall average of 0.84. (b) shows button frame accuracy with an overall average of 0.96*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/009_Figure_6.jpg]]
*Figure 6: NitroGen 500M pre-training results across different games. We evaluate NitroGen after behavior-cloning pre-training. The model is not fine-tuned for specific games. For each game, we measure the average task completion rate on 3 tasks with 5 rollouts per task. Despite being trained on a very noisy internet dataset, NitroGen is able to perform non-trivial tasks over games with different visual styles (3D, 2D top-down, 2D side-scrolling) and genres (platformer, action-RPG, roguelike, etc.)*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/010_Figure_7.jpg]]
*Figure 7: Post-training experiments: NitroGen pre-training improves downstream agents in unseen environments. We pre-train NitroGen on the dataset described in Section 2.1, holding out one game. We then fine-tune the pre-trained checkpoint on the held-out game and compare the results with a model trained from scratch using the same architecture, data and compute budget. (a) When varying data quantity, task-completion rate scales with dataset size, and fine-tuning achieves on average a 10% relative improvement in task-completion rate. (b) When varying task type in the low-data regime (30h), fine-tuning achieves up to 52% relative improvement in task-completion rate*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2601_02427/figures/006_Figure_3.jpg]]
*Figure 3: Distribution of the NitroGen dataset across games and genres. After filtering, the NitroGen dataset contains 40,000 hours of gameplay videos spanning more than 1,000 games. (a) Hours per game shows broad coverage, with 846 games having over one hour of data, 91 games with over 100 hours, and 15 games exceeding 1,000 hours each. (b) Genre distribution reveals Action-RPG games are most common (34.9% of total hours), followed by Platformer (18.4%) and Action-Adventure (9.2%) games, with the remainder distributed across seven genres*

## 方法谱系与知识库定位

### 核心突破：从人工演示到互联网规模的行为克隆

NitroGen 的核心贡献在于将通用游戏代理的训练范式从“依赖人工收集的演示数据”推进到“利用互联网公开视频自动构建大规模行为克隆数据集”。这一转变的关键在于 **输入覆盖层（input overlay）** 的利用——许多游戏直播和视频创作者会实时显示自己的手柄操作，NitroGen 通过自动化流水线从中提取帧级动作标签，从而将原本需要昂贵人工标注的数据获取过程转化为可扩展的自动化流程。

在方法谱系中，NitroGen 属于**视觉-动作基础模型**这一新兴方向，但与现有工作存在显著差异：

- **相比于依赖模拟器 API 的方法**（如通过程序化接口获取底层游戏状态）：NitroGen 完全从像素级视觉输入学习，不依赖任何游戏内部状态访问，使其能够泛化到任意商业游戏。
- **相比于语言模型驱动的复合系统**（如利用 VLM 进行推理和规划的代理）：NitroGen 放弃了语言条件化，专注于纯视觉-动作映射的规模化训练，强调从多样化的游戏数据中学习可迁移的感知-运动技能。
- **相比于单游戏专用策略网络**：NitroGen 在超过 1,000 款游戏、40,000 小时的视频数据上进行预训练，构建了一个统一的跨游戏基础模型，而非为每个游戏单独设计策略。

### 方法适用边界

NitroGen 的能力边界由以下几个关键设计选择所定义：

1. **输入模态限制**：模型仅接受手柄动作作为输出，不支持键盘与鼠标操作。这使其天然适用于主机游戏和动作类游戏，但对第一人称射击（FPS）、即时战略（RTS）等依赖键鼠的游戏类型缺乏直接适用性。

2. **游戏类型偏向**：数据集以动作 RPG（34.9%）、平台跳跃（18.4%）和动作冒险（9.2%）为主，这些类型的游戏通常具有密集的动作序列。对于策略游戏、模拟经营等依赖长期规划和低频操作的游戏类型，模型的泛化能力未经验证。

3. **纯视觉-动作映射**：NitroGen 不支持自然语言指令或视觉提示，无法根据文本描述执行特定任务。这限制了其在需要灵活任务指定的场景中的应用。

4. **同步推理假设**：模型通过拦截系统时钟实现帧级同步控制，虽然在测试中未破坏游戏物理，但在实时或异步部署环境下的行为尚不明确。

5. **缺乏长期规划**：模型仅基于单帧历史生成 16 步动作块，不具备显式的长期记忆或规划能力，难以胜任需要数十分钟以上上下文的复杂任务。

### 局限与开放问题

**已知局限**：

- **数据质量依赖覆盖层可视性**：动作提取流水线依赖游戏手柄覆盖层的清晰可见，视频压缩、控制器透明度差异或风格变化可能导致提取错误。虽然整体摇杆 R² 达到 0.84、按钮准确率达到 0.96，但在特定控制器类型上性能可能下降。
- **评估覆盖有限**：成功率评估依赖人工评判，且仅覆盖 10 款游戏中的 30 个特定任务，可能不足以全面反映代理的综合能力。
- **动作密度过滤的副作用**：为防模型坍缩至空动作，仅保留动作密度 ≥ 50% 的片段（丢弃约 45% 数据），这可能系统性地排除了需要静止等待或观察的游戏场景。

**开放问题**：

1. **语言与多模态扩展**：如何向 NitroGen 注入语言指令或视觉提示，以实现更灵活的零样本任务描述？能否利用游戏音频、文本聊天、UI 提示等多模态数据补充视觉信号？

2. **强化学习后训练**：能否通过离线或在线强化学习对预训练策略进行微调，以解锁需要深度探索和长期回报的任务？

3. **输入设备扩展**：如何将框架扩展到使用键盘与鼠标的游戏类型，覆盖更广泛的游戏生态？

4. **世界模型引入**：引入世界模型对未来观察进行预测，是否能提升策略的规划能力和对动态环境的适应性？

5. **实时部署鲁棒性**：在异步或实时推理环境下，当前基于时钟暂停的仿真方式是否仍然稳定？是否需要新的同步机制？

### 知识库定位

NitroGen 在通用游戏代理领域占据了一个独特的位置：它是**首个从互联网规模视频数据中学习、无需人工演示即可在多种商业游戏中实现非平凡零样本性能的开放基础模型**。其核心知识贡献包括：

- **数据飞轮机制**：证明了输入覆盖层是一种可扩展的动作监督信号来源，为视觉-动作基础模型的大规模训练提供了数据基础。
- **统一仿真接口**：通过系统时钟拦截实现的通用 Gymnasium 包装器，为任意商业游戏的标准化评估提供了基础设施。
- **预训练-微调范式**：验证了在大规模多样化游戏数据上的行为克隆预训练能够为未见游戏提供有效的策略初始化，在低数据场景下可获得高达 52% 的相对任务成功率提升。

该方法为后续研究提供了可复用的数据流水线、模型架构和评估基准，同时也揭示了纯视觉-动作映射在复杂任务规划和语言理解方面的根本性局限，为未来的多模态游戏代理研究指明了方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/NitroGen_An_Open_Foundation_Model_for_Generalist_Gaming_Agents.pdf]]
---
title: "Less is More: Data-Efficient Adaptation for Controllable Text-to-Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Less_is_More_Data_Efficient_Adaptation_for_Controllable_Text_to_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- LIM
- LIMDEACTVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过仅用低保真度、稀疏的合成数据，并采用联合训练策略（主干 LoRA 吸收域偏移，解耦交叉注意力适配器学习物理效果），在推理时选择性丢弃浅层 LoRA 权重以恢复原始主干先验，从而在不损害生成质量的前提下实现精准、连续的物理控制。
primary_logic: 微调数据集的有效性不取决于其真实感，而取决于其解耦程度。简单、可控的合成数据能避免语义纠缠和灾难性遗忘，比真实风格数据更高效地诱导出预训练模型已有的视觉先验。
claims:
- 合成数据训练的模型在 FEP 监控中漂移速度远低于真实数据，SVP 验证的语义分数与基线持平，而真实数据导致分数崩溃。
- 联合训练的适配器产生有效秩为1的低维条件信号，而仅使用适配器训练会产生高秩内容记忆信号（推土机效应），验证了解耦设计的必要性。
- 解耦推断在所有物理控制下维持了与原始主干几乎一致的视频质量指标（主体一致性、背景一致性、运动平滑度等），且语义保真度变化小于2%。
- VBench SVP (96-prompt high-motion suite) 上 X-CLIP Score = 25.587 (Decoupled, Shutter)
---

# Less is More: Data-Efficient Adaptation for Controllable Text-to-Video Generation

> [!tip] 核心洞察
> 微调数据集的有效性不取决于其真实感，而取决于其解耦程度。简单、可控的合成数据能避免语义纠缠和灾难性遗忘，比真实风格数据更高效地诱导出预训练模型已有的视觉先验。

| 字段 | 内容 |
|------|------|
| 中文题名 | 少即是多：面向可控文本到视频生成的数据高效适应 |
| 英文题名 | Less is More: Data-Efficient Adaptation for Controllable Text-to-Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17844) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Less is More（数据高效联合训练与解耦推断） |
| Dataset | VBench SVP, Monotonicity Analysis |

> [!tip] 效果简介
> - VBench SVP (96-prompt high-motion suite) 上，X-CLIP Score 25.587 (Decoupled, Shutter) vs 25.390 (WAN 2.1 backbone) (+0.197)。
> - VBench SVP 上，VQA Score 0.521 (Decoupled, Shutter) vs 0.522 (WAN 2.1 backbone) (-0.001)；Subject Consistency 0.946 (Decoupled, Shutter) vs 0.951 (WAN 2.1 backbone) (-0.005)；Motion Smoothness 0.987 (Decoupled, Shutter) vs 0.988 (WAN 2.1 backbone) (-0.001)。
> - Monotonicity Analysis (80-prompt subset, 5-frame outputs) 上，Median Spearman |ρ| 1.000 (all controls) vs N/A (Perfect monotonic response)。

## 概要

### 问题与瓶颈

文本到视频（T2V）扩散模型在生成质量上取得了显著进展，但为其赋予**连续的物理控制能力**（如快门速度、光圈、色温）仍面临根本性瓶颈：现有方案依赖大规模、高保真的真实数据，而这类数据不仅获取成本极高，更关键的是其高复杂度会导致**语义漂移**和**灾难性遗忘**——微调后的模型在获得控制能力的同时，会严重破坏预训练主干网络的生成先验。

### 核心发现：“少即是多”

本文提出了一个反直觉的核心洞察：**微调数据集的有效性并不取决于其真实感，而取决于其解耦程度**。简单、可控的低保真合成数据能够避免语义纠缠，比真实风格数据更高效地诱导出预训练模型已有的视觉先验。基于这一洞察，该方法仅使用**稀疏的低保真合成数据**（几何图元场景，仅 150 个训练样本），即可在 14B 参数的 WAN 2.1 主干上实现精准、连续的物理控制。

### 方法定位

该方法提出了一种**数据高效的联合训练与解耦推断**范式，其关键设计在于：

- **联合训练**：主干 LoRA（注入所有 DiT 块）吸收合成数据的域偏移，而解耦交叉注意力适配器（仅作用于最深 1/3 的 Transformer 块）学习物理效果的条件信号。
- **解耦推断**：推理时丢弃浅层 2/3 块的主干 LoRA 权重，恢复原始主干先验，仅保留深层适配器实现精准控制。

这一“分离关注点”的设计确保了控制能力与生成质量互不损害。

### 主要结果

实验表明，该方法在快门速度、光圈和色温三个连续物理控制任务上均实现了**完美的单调响应**（Spearman |ρ| = 1.000），且解耦推断下的视频质量指标（主体一致性 0.946、运动平滑度 0.987、X-CLIP 25.587）与原始 WAN 2.1 主干几乎一致，语义保真度变化小于 2%。消融实验进一步验证：合成数据训练的主干漂移速率远低于真实数据，且联合训练是避免适配器“推土机效应”（高秩内容记忆）的必要条件。



### 问题背景

文本到视频（T2V）生成模型近年来取得了显著进展，能够根据自然语言描述合成高保真、时序连贯的视频内容。然而，当前的生成范式主要局限于**语义层面的控制**——用户通过修改文本提示来间接影响生成结果，缺乏对**连续物理参数**（如快门速度、光圈大小、色温）的精确操控能力。在真实摄影和电影制作中，这些参数是塑造视觉风格、运动模糊、景深效果和色彩氛围的核心手段。将此类连续物理控制引入大规模 T2V 模型，有望弥合生成模型与专业视觉创作工具之间的鸿沟。

### 现有方法缺口

为 T2V 模型扩展物理控制面临一个根本性困境：**数据需求与数据可得性之间的尖锐矛盾**。现有两种主流路径均存在明显局限：

1. **文本提示工程**：依赖自然语言描述（如“长曝光摄影”、“浅景深”）来近似物理效果。然而，自然语言本质上是离散、模糊且高度语义纠缠的——同一段文字同时影响构图、光照、物体运动等多个维度，无法实现连续、解耦的标量控制。例如，仅凭文本难以精确指定“光圈 f/2.8 到 f/16 之间的平滑过渡”。

2. **专用数据密集型方法**：针对特定物理效果（如散景、相机感知合成）训练专用模型，如 **Generative Photography**（Yuan et al., CVPR 2025）和 **Bokeh Diffusion**（Fortes et al., SIGGRAPH Asia 2025）。这类方法需要大量高保真真实数据，而获取覆盖完整物理参数空间的高质量视频数据成本极高，甚至在某些控制维度上几乎不可行。

更关键的是，直接使用高复杂度真实数据进行微调会引发两个严重问题：
- **语义漂移**：真实数据的丰富视觉细节与预训练分布存在偏差，导致模型逐步遗忘主干网络原有的语义理解能力；
- **灾难性遗忘**：微调过程破坏预训练模型在多样化场景上的生成先验，使模型退化为只能复现训练分布的“记忆机器”。

### 核心动机

本文的核心假设是：**微调数据集的有效性不取决于其真实感，而取决于其解耦程度**。预训练 T2V 模型已经内化了丰富的视觉世界先验——它“知道”运动模糊是什么样、散景如何随深度变化、不同色温下场景的色调如何偏移。问题不在于“教会”模型这些效果，而在于**以最小干扰的方式唤醒这些先验，并将其与连续控制信号建立映射**。

基于这一洞察，本文提出 **“Less is More”** 框架：仅使用**低保真度、稀疏的合成数据**（简单几何图元与程序化物理变化），通过**联合训练与解耦推断**策略，在不损害主干生成质量的前提下，实现精准、连续的物理控制。这一设计的核心逻辑是：简单、可控的合成数据避免了语义纠缠，使模型能够以“最少的数据”学到“最纯的控制”。



## 核心方法与创新机理

本文的核心创新在于提出了一套**数据高效联合训练与解耦推断**范式，使得大规模文生视频（T2V）扩散模型仅需极少量低保真合成数据，即可获得精准、连续的物理相机控制能力。其关键洞察是：**微调数据集的有效性不取决于其真实感，而取决于其解耦程度**——简单、可控的合成数据能避免语义纠缠和灾难性遗忘，比真实风格数据更高效地诱导出预训练模型已有的视觉先验。

### 条件注入机制的创新：解耦交叉注意力适配器

相较于纯文本提示的 T2V 基线（如 **WAN 2.1**，Wan et al., arXiv:2503.20314, 2025），本方法在条件信号注入方式上做出了根本性改变。基线模型仅依赖自然语言提示，无法实现精确的标量物理参数控制；而本方法引入了一个**解耦条件模块**，将连续标量条件 $c \in [-1, 1]$ 通过一个小型 MLP 投影为高维嵌入向量：

$$e_{\mathrm{cond}} = \mathrm{MLP}_{\mathrm{cond}}(c)$$

该嵌入通过一个**并行交叉注意力层**注入到 DiT 骨干网络的最深 1/3 Transformer 块中，并与文本条件信号通过可学习门控 $g$ 进行线性组合：

$$y_{\mathrm{combined}} = y_{\mathrm{text}} + g \cdot y_{\mathrm{cond}}$$

这种设计使得物理控制信号与文本语义信号在注意力空间中保持解耦，避免了条件信号对内容生成路径的污染。与之形成对比的是，专门的数据密集型图像基线方法（如 **Bokeh Diffusion**，Fortes et al., SIGGRAPH Asia 2025；**Generative Photography**，Yuan et al., CVPR 2025）需要大量真实感数据来学习物理效果，而本方法仅用稀疏合成数据即可达到可比甚至更优的控制精度。

### 训练策略的创新：骨干 LoRA 与适配器的联合优化

本方法在微调策略上的核心创新是**联合训练骨干 LoRA 与条件适配器**，而非传统的孤立微调。具体而言：

- **骨干 LoRA** 被注入到所有 DiT 块中，其作用是吸收合成数据带来的域偏移（domain shift），充当“缓冲层”；
- **条件适配器** 仅安装在最深 1/3 块中，专注于学习物理效果的条件映射。

这种“关注点分离”的设计通过奇异值谱分析得到了有力验证（Figure 6）：联合训练模型的适配器输出 $y_{\mathrm{cond}}$ 呈现尖锐的谱衰减，有效秩仅为 1，表明其学习到了物理效果的低维本质表征；而仅使用适配器训练（无骨干 LoRA）的模型，其条件信号呈现高秩且缓慢衰减的谱特征，与内容信号 $y_{\mathrm{text}}$ 高度相似，说明适配器“记忆”了训练数据的内容而非分离出物理控制效应——作者将这一现象称为**推土机效应（Bulldozer Effect）**。

### 推断策略的创新：选择性丢弃浅层 LoRA 权重

本方法在推断阶段引入了**解耦推断**策略：在推理时，**丢弃浅层 2/3 Transformer 块中的骨干 LoRA 权重**，仅保留深层 1/3 块中的骨干 LoRA 和条件适配器。这一设计的动机在于：骨干 LoRA 在训练期间吸收了合成数据的域偏移，若全量保留，会在推理时引入轻微的合成偏置；而选择性丢弃浅层 LoRA 权重能够恢复预训练骨干的原始先验，同时深层保留的 LoRA 与适配器协同工作，维持物理控制能力。

实验表明（Table 1），解耦推断在所有物理控制下维持了与原始 WAN 2.1 骨干几乎一致的视频质量指标——主体一致性（0.946 vs. 0.951）、背景一致性、运动平滑度（0.987 vs. 0.988）等指标的偏差均在 0.5% 以内，语义保真度（X-CLIP 分数）变化小于 2%。相比之下，全量 LoRA 推断虽然生成质量仍然可接受，但会引入可测量的合成偏置。

### 数据范式的创新：低保真合成数据优于真实数据

本方法颠覆了“数据越真实越好”的直觉。消融实验（Figure 4, Top Row）显示：

- 使用**真实感数据**微调的模型在 FEP（快速评估协议）监控中漂移速度极快，分布漂移率 $\nu_{\mathrm{drift}}$ 显著高于合成数据模型，SVP（慢速验证协议）中语义分数（X-CLIP、VQA）出现崩溃；
- 使用**低保真合成数据**（仅 150 个样本，30 帧/视频）训练的模型，FEP 指标保持稳定，SVP 语义分数与基线持平。

其因果机制在于：真实数据的高复杂度导致物理效果与场景内容高度纠缠，微调时模型难以解耦二者，从而引发灾难性遗忘；而合成数据（金字塔采样的几何图元场景）的极低复杂度使得物理变化成为数据中唯一显著的变化因子，模型能够干净地分离出控制信号。这一发现构成了本文“少即是多”哲学的经验基础。

### 评估协议的创新：FEP 与 SVP 双层验证

为系统量化微调对骨干模型的冲击，本方法设计了**双层评估协议**：

- **FEP（快速评估协议）**：基于单步去噪指标（SSF、SS-FD）进行轻量级监控，通过分布漂移率 $\nu_{\mathrm{drift}} = \delta(\mathrm{SS-FD}) / \delta(\mathrm{steps})$ 量化数据集复杂度及其对骨干的冲击程度；
- **SVP（慢速验证协议）**：采用完整多步去噪流程，使用 X-CLIP、VQA 和 VBench 等成熟指标评估最终生成质量和时序一致性。

这一双层设计使得研究者能够在训练过程中高效监控模型健康度，避免在已发生灾难性遗忘后才发现问题。

### 控制精度的创新：完美单调响应

本方法在控制精度上实现了**完美的单调响应**。在 80 个提示词子集上的单调性分析（Table 2）显示，所有物理控制参数（快门速度、光圈、色温）的 Spearman 秩相关系数中位数 $|\rho| = 1.000$，意味着生成结果与控制标量之间存在完全单调的映射关系。这一特性使得用户可以通过连续调节标量值获得可预期的、平滑的物理效果变化，而基于文本提示的基线方法无法实现这种精确的连续控制。



本文提出一种面向可控文本到视频生成的数据高效适应框架，核心思想是“少即是多”：仅使用稀疏、低保真度的合成数据，通过联合训练与解耦推断策略，即可在大型预训练文生视频（T2V）扩散模型上实现精准的连续物理控制。该方法以 **WAN 2.1**（Wan et al., arXiv:2503.20314, 2025）作为骨干网络，在不损害其原有生成先验的前提下，赋予模型对快门速度、光圈、色温三个标量参数的连续操控能力。

### 控制信号注入架构

框架在骨干 DiT（Diffusion Transformer）之上引入两类轻量级适配模块，构成解耦的条件注入通路：

- **解耦条件适配器（Disentangled Conditioning Module）**：标量控制值 $c \in [-1, 1]$ 首先通过一个小型多层感知机投影为高维嵌入向量 $e_{\mathrm{cond}} = \mathrm{MLP}_{\mathrm{cond}}(c)$。该嵌入随后注入到骨干网络最深层的 1/3 Transformer 块中，以并行交叉注意力（parallel cross-attention）的形式与文本条件信号融合：$y_{\mathrm{combined}} = y_{\mathrm{text}} + g \cdot y_{\mathrm{cond}}$，其中 $g$ 为可学习门控参数。这一设计将物理属性的控制信号与文本语义信号在注意力空间中显式解耦，避免语义纠缠。

- **骨干 LoRA（Backbone LoRA）**：在所有 DiT 块中注入标准低秩适配器 $W_{\mathrm{lora}} = W_{\mathrm{pre}} + \Delta W_{\mathrm{lora}}$，其作用是吸收合成训练数据与预训练分布之间的域偏移，保护条件适配器免受分布差异的干扰。

### 联合训练策略

训练阶段，骨干 LoRA 与解耦条件适配器同步优化。这种联合训练强制执行一种“关注分离”机制：骨干 LoRA 承担合成域偏移的吸收任务，使条件适配器能够专注于学习纯粹的物理效应表示，而非记忆训练数据的内容。训练数据来自一个金字塔采样数据引擎，该引擎通过分层抖动采样在极少的场景（仅 150 个样本）中生成覆盖完整控制范围的连续标量序列，场景本身仅包含随机几何图元，具有极低的视觉复杂度。

### 解耦推断策略

推断阶段的关键操作是选择性丢弃浅层 LoRA 权重：对于未配备条件适配器的浅层 2/3 Transformer 块，移除其骨干 LoRA 更新，仅保留预训练权重；深层 1/3 块则同时保留骨干 LoRA 与条件适配器。这一策略在推理时有效恢复骨干网络的原始生成先验，使得模型既能响应连续物理控制信号，又几乎不损失视频生成质量。

### 评估协议

为系统衡量适应过程对骨干模型的冲击，框架配套设计了两阶段评估协议：

- **快速评估协议（Fast Evaluation Protocol, FEP）**：通过单步去噪指标（语义相似度分数 SSF 及其分布差异 SS-FD）实时监控训练过程中的语义漂移，并定义分布漂移速率 $\nu_{\mathrm{drift}} = \delta(\mathrm{SS-FD}) / \delta(\mathrm{steps})$ 来量化数据集复杂度对模型的冲击程度。
- **慢速验证协议（Slow Validation Protocol, SVP）**：采用完整多步去噪流程，使用 X-CLIP、VQA 及 VBench 等成熟指标评估最终生成视频的语义保真度、主体一致性、背景一致性、运动平滑度等质量维度。

整个框架的输入为文本提示与标量物理控制参数，输出为连续可控的高保真视频，其训练与推断流程的整体架构如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our controllable generation pipeline. To achieve decoupled control, we encode the scalar condition separately from the text guidance via a parallel cross-attention module. During training (top), we optimize the conditional adapter while actively updating the backbone by injecting LoRA layers into all DiT blocks. During inference (bottom), we discard the LoRA weights from the shallow two-thirds of the transformer blocks, retaining only the conditional adapter and backbone LoRA in the deepest third of the blocks. This selective retention enables high-fidelity physical control while minimizing semantic corruption of the backbone*



### 整体架构概览

本方法在预训练的文生视频（T2V）扩散主干上引入两个关键架构修改，形成数据高效的可控生成管线（Figure 2）。核心设计遵循“关注点分离”原则：**Backbone LoRA** 负责吸收合成数据的域偏移，而**解耦条件适配器（Disentangled Conditioning Module）** 专注于学习物理控制效果本身，二者通过联合训练协同工作，在推理时通过选择性丢弃浅层 LoRA 权重恢复主干先验。

### 解耦条件适配器

条件适配器将标量物理控制参数 $c$（归一化至 $[-1, 1]$）编码为高维嵌入，并通过并行交叉注意力机制独立注入到扩散Transformer（DiT）块中，与文本条件信号解耦。

**条件嵌入投影**：标量条件 $c$ 首先通过一个小型多层感知机（MLP）投影到高维嵌入向量：

$$e_{\mathrm{cond}} = \mathrm{MLP}_{\mathrm{cond}}(c)$$

该嵌入随后被送入并行交叉注意力模块，生成条件信号 $y_{\mathrm{cond}}$。条件适配器仅被注入到 DiT 主干最深的 1/3 层（即 Block 27–40，共40层），以确保物理控制作用于高层语义表征而非底层纹理细节。

**信号融合机制**：在每个注入层，条件信号 $y_{\mathrm{cond}}$ 与文本交叉注意力输出 $y_{\mathrm{text}}$ 通过可学习门控标量 $g$ 进行线性组合：

$$y_{\mathrm{combined}} = y_{\mathrm{text}} + g \cdot y_{\mathrm{cond}}$$

门控 $g$ 初始化为零，确保训练初期模型行为与原始主干一致，随后逐步学习条件信号的贡献权重。这种设计避免了条件信号在训练初期干扰预训练的文本-视觉对齐。

### Backbone LoRA 与训练-推理解耦

**训练阶段**：在所有 DiT 块中注入低秩适配器（LoRA），与条件适配器联合优化。LoRA 将预训练权重 $W_{\mathrm{pre}}$ 更新为：

$$W_{\mathrm{lora}} = W_{\mathrm{pre}} + \Delta W_{\mathrm{lora}}$$

其中 $\Delta W_{\mathrm{lora}}$ 为低秩分解矩阵的乘积。联合训练迫使 Backbone LoRA 承担合成数据的域偏移吸收，而条件适配器仅需学习物理效果的纯净表征。

**推理阶段（解耦推断）**：丢弃浅层 2/3 DiT 块（Block 1–26）中的 Backbone LoRA 权重，仅保留最深层 1/3 块（Block 27–40）中的 LoRA 更新和条件适配器。这一选择性保留策略的关键在于：浅层块主要处理底层视觉特征，其 LoRA 更新携带合成数据的风格偏置；深层块处理语义级表征，其 LoRA 更新与物理控制信号协同作用。丢弃浅层 LoRA 等价于将浅层权重恢复为 $W_{\mathrm{pre}}$，从而在保留物理控制能力的同时，最大程度恢复预训练主干的生成先验。

### 分布漂移率

为量化不同训练数据对主干模型的冲击程度，引入**分布漂移率（Distributional Drift Rate）** 指标：

$$\nu_{\mathrm{drift}} = \frac{\delta(\mathrm{SS\text{-}FD})}{\delta(\mathrm{steps})}$$

其中 $\mathrm{SS\text{-}FD}$（Single-Step Fréchet Distance）是快速评估协议（FEP）中的核心指标，测量单步去噪输出与基线模型输出之间的分布距离。$\nu_{\mathrm{drift}}$ 捕捉该距离随训练步数的变化速率，数值越高表示数据对主干的语义分布冲击越大。该指标在消融实验中用于定量对比合成数据与真实数据对主干造成的漂移程度（Figure 4, Top Row）。

### 有效秩分析

为验证解耦设计的必要性，对条件信号 $y_{\mathrm{cond}}$ 进行奇异值分解（SVD）分析。将强条件（$c=1$）下的条件信号矩阵化后计算奇异值谱，评估其有效秩。联合训练模型的 $y_{\mathrm{cond}}$ 呈现尖锐的谱衰减，有效秩为 1，表明适配器学到了物理效果的低维紧凑表征（Figure 6a）；而仅训练适配器（无 Backbone LoRA）的模型中，$y_{\mathrm{cond}}$ 呈现高秩、缓慢衰减的谱特性，与内容信号 $y_{\mathrm{text}}$ 的谱结构相似，表明适配器记忆了训练数据内容而非分离出控制效果——这一现象被称为“推土机效应”（Bulldozer Effect，Figure 6b）。该分析从表征几何角度证明了 Backbone LoRA 联合训练对于解耦的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/007_Figure_6.jpg]]
*Figure 6: Singular value spectrum of the conditional signal ycond in Block 27. (a) In our jointly trained model, the conditional signal exhibits a sharp spectral decay with an effective rank of 1, confirming that the adapter learned an efficient, low-dimensional representation of the physical effect. (b) In the adapter-only model, the signal is high-rank, with a slow spectral decay that mirrors the content signal*

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/015_Figure_12.jpg]]
*Figure 12: Backbone content drift across depth for the shutter speed condition. Analysis performed on the value projection*



## 实验与关键发现

### 核心实验设计逻辑

论文的实验设计围绕一个中心命题展开：**微调数据集的有效性不取决于其真实感，而取决于其解耦程度**。为验证这一命题，作者构建了一套双层评估体系——**快速评估协议（FEP）** 和**慢速验证协议（SVP）**——分别用于轻量级监测训练过程中的主干语义漂移和最终生成质量的全面评估。

FEP 阶段采用单步去噪指标（SSF、SS-FD），并引入**分布漂移速率** $\nu_{\mathrm{drift}} = \delta(\mathrm{SS-FD}) / \delta(\mathrm{steps})$ 来量化不同数据集对预训练主干的冲击程度。SVP 阶段则使用全步去噪，结合 X-CLIP、VQA 及 VBench 等成熟指标评估语义保真度、视频质量和时序一致性。

所有消融实验均在严格控制变量的条件下进行：每个控制参数仅使用单一场景，数据规模极小（150 个训练样本，每视频 30 帧），排除了数据规模或多样性的混淆因素。

---

### 主结果：解耦推断维持了原始主干的生成质量

Table 1 展示了全 LoRA 推断（Full）与解耦推断（Dec.）在 VBench SVP 基准（96 条高运动提示词）上的定量对比。核心发现是：**解耦推断在所有物理控制下维持了与原始 WAN 2.1 主干几乎一致的视频质量指标，语义保真度变化小于 2%。**

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/004_Table_1.jpg]]
*Table 1: Quantitative SVP Results. Comparison of Full-LoRA (Full) and Decoupled (Dec.) inference against the original backbone baseline across three controls. Within each control pair, highlighted values are closer to the baseline*

以快门控制为例，解耦推断的 X-CLIP 得分为 25.587，与基线 25.390 的差异仅为 +0.197；VQA 得分 0.521 与基线 0.522 几乎无差异。在主体一致性（0.946 vs. 0.951）、运动平滑度（0.987 vs. 0.988）等 VBench 子指标上，解耦推断与基线的差距均在 0.005 以内。相比之下，全 LoRA 推断虽然也能生成高质量视频，但在部分指标上引入了轻微合成数据偏置。

**控制单调性分析**（Table 2）进一步验证了物理控制的精准性：在 80 条提示词子集上，所有控制参数的斯皮尔曼秩相关系数中位数 |ρ| 达到 1.000，表明模型对连续标量输入实现了完美的单调响应。

定性对比（Figure 5）显示，该方法在快门速度（运动模糊）、光圈（散景）和色温三个物理参数上均实现了连续、高保真的控制，显著优于纯文本提示的 WAN 2.1 基线，并与数据密集型图像方法 **Generative Photography**（Yuan et al., CVPR 2025）和 **Bokeh Diffusion**（Fortes et al., SIGGRAPH Asia 2025）的效果相当。

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of physical controls. We compare our method against text-based prompting in a T2V backbone (WAN 2.1) and specialized, data-intensive image baselines Generative Photography [53] and Bokeh Diffusion [7]*

---

### 消融实验一：合成数据 vs. 真实数据——灾难性遗忘的根源

Figure 4（顶行）揭示了数据复杂度对主干语义漂移的决定性影响。在 FEP 监控中，使用真实风格数据微调的模型（虚线）在 SSF 和 SS-FD 指标上呈现出远快于合成数据模型（实线）的漂移速率。SVP 验证进一步量化了这一差异：真实数据模型的 X-CLIP 和 VQA 语义得分出现了**灾难性崩溃**，而合成数据模型的得分与基线持平。

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/005_Figure_4.jpg]]
*Figure 4: Ablation studies on data complexity and inference strategy. Top Row: Synthetic vs. Real Data. A one-shot comparison of fine-tuning on our low-fidelity synthetic*

这一现象的本质原因在于：真实数据的高复杂度导致语义纠缠——物理控制信号与场景内容信息在特征空间中难以分离，迫使主干在适应物理效果的同时“记忆”了训练数据的内容分布，从而破坏了预训练的生成先验。低复杂度合成数据则天然避免了这一问题。

---

### 消融实验二：解耦推断 vs. 全 LoRA 推断——选择性丢弃的必要性

Figure 4（底行）对比了两种推断策略。全 LoRA 推断保留所有 DiT 块的骨干 LoRA 权重，解码推断则丢弃浅层 2/3 块的 LoRA 权重。SVP 结果表明，解耦推断在所有语义和视频质量指标上均更接近原始基线，验证了**选择性丢弃浅层 LoRA 权重能够有效恢复主干先验**的设计合理性。

进一步的分析表明，浅层 DiT 块主要负责内容生成和语义理解，而深层块更多参与物理效果的渲染。因此，仅保留深层块的 LoRA 更新既能传递物理控制信号，又能避免合成数据的偏置污染浅层的内容先验。

---

### 消融实验三：联合训练 vs. 仅适配器训练——“推土机效应”的发现

Figure 6 通过条件信号 $y_{\mathrm{cond}}$ 的奇异值谱分析揭示了训练策略的关键差异。在联合训练模型中（Figure 6a），$y_{\mathrm{cond}}$ 呈现尖锐的谱衰减，有效秩为 1，证实适配器学到了物理效果的低维表征。而在仅适配器训练模型中（Figure 6b），$y_{\mathrm{cond}}$ 呈现高秩、缓慢衰减的谱结构，与内容信号 $y_{\mathrm{text}}$ 的谱特征高度相似。

这一现象被称为**“推土机效应”（Bulldozer Effect）**：当骨干 LoRA 不存在时，条件适配器被迫同时承担域偏移吸收和物理效果学习的双重任务，最终导致高秩的内容记忆而非低维的条件编码。联合训练通过“关注点分离”机制——骨干 LoRA 吸收合成域偏移，条件适配器专注物理效果——从根本上避免了这一问题。

---

### 失败模式与局限性

尽管方法在三个标量相机参数上表现出色，但仍存在以下已知局限：

1. **超出训练范围的控制值**：当条件标量 $c \in [-1.5, 1.5]$ 超出训练范围时，模型虽能产生平滑过渡，但极端值可能导致饱和度增加或语义退化，缺乏系统性量化。

2. **极度简单的训练场景**：训练数据仅使用几何图元，在需要高度语义对齐或文本引导的复杂构成时，控制精度可能受限。

3. **参数独立性假设**：当前仅针对三个标量参数独立训练，未探索多通道联合控制，无法处理光圈与色温等参数的复合交互效应。

4. **单骨干验证**：所有实验仅在 **WAN 2.1**（DiT-based 14B）上完成，对其他 T2V 骨干（如 HunyuanVideo、闭源 Sora）的泛化性有待验证。

5. **数据规模效应未探索**：仅使用 150 个样本的金字塔采样策略，数据缩放对控制鲁棒性的影响缺乏系统研究。

---

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| **Figure 4（顶行）** | 合成数据训练的模型在 FEP 监控中漂移速度远低于真实数据；SVP 验证的语义分数与基线持平，而真实数据导致分数崩溃 |
| **Figure 4（底行）** | 解耦推断在所有指标上均优于全 LoRA 推断，验证了选择性丢弃浅层 LoRA 的有效性 |
| **Figure 6** | 联合训练的条件信号有效秩为 1（低维物理效果编码），仅适配器训练的条件信号呈高秩（内容记忆），验证了解耦设计的必要性 |
| **Table 1** | 解耦推断在主体一致性、背景一致性、运动平滑度等指标上与原始主干差异小于 0.005，语义保真度变化小于 2% |
| **Table 2** | 所有控制参数实现完美单调响应（Spearman \|ρ\| = 1.000） |

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/012_Table_2.jpg]]
*Table 2: Quantitative Monotonicity Analysis. Spearman rank correlation*

### 补充图表

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/014_Figure_11.jpg]]
*Figure 11: Out-of-range inference. Qualitative sweep over*

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/017_Figure_14.jpg]]
*Figure 14: Qualitative results of our controllable generation. Our model demonstrates precise and continuous control over shutter speed (Rows 1–2, motion blur), aperture (Rows 3–4, bokeh), and color temperature (Rows 5–6) by varying the conditional input c from -1.0 to 1.0 across diverse, high-fidelity video prompts*

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/022_Figure_15.jpg]]
*Figure 15: Generalization of shutter control to scenes with complex motion. The model responds reliably to the shutter scalar in settings involving moving cameras (e.g., camera-follow and first-person views) and scenes with multiple independently moving objects*

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/028_Figure_17.jpg]]
*Figure 17: Despite being trained only on images, the model renders smooth bokeh variation as depth changes, enabled by the backbone’s strong prior*

![[assets/figures/papers/paper_list_l2221_https_arxiv_org_abs_2511_17844/figures/003_Figure.jpg]]
*Figure: Ared sports car speeding down a coastal highway with waves crashing on the side. wider Aperture narrower A cat siting by a window watching the rain*



## 定位与知识库关联

### 1. 与基线工作的关系

本工作以 **WAN 2.1**（Wan et al., arXiv:2503.20314, 2025）作为文生视频（T2V）主干基线。WAN 2.1 仅支持纯文本提示，不具备显式的连续标量控制能力。本文的核心贡献并非提出新的生成主干，而是在冻结或部分适应预训练主干的约束下，注入连续物理控制信号。

与数据密集型的专用图像基线相比：
- **Bokeh Diffusion**（Fortes et al., SIGGRAPH Asia 2025）和 **Generative Photography**（Yuan et al., CVPR 2025）均依赖大规模高质量真实数据来学习散景/光圈或相机感知合成。这些方法在各自领域内实现了精细控制，但数据采集成本高昂，且难以直接迁移到视频域。
- 本文的“Less is More”范式则反其道而行之：仅用极少量低保真度合成数据（150 个样本），通过解耦训练策略达到可比甚至更优的控制效果，同时保持视频主干原有的生成质量。

**关键区别**：已有方法将控制能力的来源归因于数据的真实感与规模，而本文证明控制能力的来源在于数据的**解耦程度**——简单、可控的合成数据能避免语义纠缠和灾难性遗忘，更高效地诱导出预训练模型已有的视觉先验。

### 2. 方法适用边界

**已验证的适用范围**：
- 主干架构：DiT-based 14B 参数模型（WAN 2.1），使用 3D VAE 潜空间扩散框架。
- 控制维度：三个独立的一维连续物理参数——快门速度（运动模糊）、光圈（散景/景深）、色温。
- 控制范围：标量条件 $c \in [-1, 1]$，训练时采用金字塔采样策略覆盖连续区间。
- 推理策略：解耦推断（丢弃浅层 2/3 块的 Backbone LoRA）在保持视频质量方面显著优于全 LoRA 推断。

**已知局限与未验证边界**（需手动核实具体论文声明）：
- **多通道联合控制**：当前每个物理参数独立训练独立模型，未探索光圈与色温等参数的联合解耦控制。
- **超出训练范围的外推**：$c \in [-1.5, 1.5]$ 虽可产生平滑过渡，但极端值可能导致饱和度增加或语义退化，缺乏系统性量化。
- **其他 T2V 主干的泛化性**：仅在 WAN 2.1 上验证，对 HunyuanVideo、闭源 Sora 类模型是否成立尚不可知。
- **复杂语义场景的控制精度**：训练数据场景极其简单（几何图元），在需要高度语义对齐或文本引导的复杂构成时，控制精度可能受限。
- **数据缩放行为**：仅使用 150 个样本的金字塔采样策略，数据量对控制鲁棒性的影响未系统研究。

### 3. 核心因果机制定位

本文的方法论贡献可归纳为三个因果层级：

**第一层：数据选择的反直觉发现**
微调数据集的有效性不取决于其真实感，而取决于其解耦程度。FEP 监控（Figure 4, Top Row）提供了决定性证据：真实数据训练的模型在分布漂移速率（$\nu_{\mathrm{drift}}$）上远高于合成数据，SVP 验证的语义分数（X-CLIP, VQA）与基线持平，而真实数据导致分数崩溃。

**第二层：联合训练的必要性**
仅用适配器训练会产生“推土机效应”（Bulldozer Effect）：条件信号的有效秩为高秩，与内容信号 $y_{\mathrm{text}}$ 的谱衰减模式相似，表明适配器记忆了训练数据内容而非隔离物理效应（Figure 6b）。联合训练强制 Backbone LoRA 吸收合成域偏移，使适配器学习到有效秩为 1 的低维条件表示（Figure 6a），实现真正的解耦。

**第三层：解耦推断的保真机制**
推理时丢弃浅层 2/3 块的 Backbone LoRA 权重，本质上是选择性恢复预训练先验。Table 1 表明，解耦推断在所有物理控制下维持了与原始主干几乎一致的视频质量指标（主体一致性、背景一致性、运动平滑度等），且语义保真度变化小于 2%。

### 4. 开放问题与未来方向

基于本文的分析和局限，以下问题有待探索：

1. **多参数联合解耦**：如何将多个物理参数（如光圈与色温）解耦到单一联合控制向量中，实现更连贯的复合控制？当前独立训练的架构无法处理参数间的交互效应。

2. **跨模态控制迁移**：该数据高效范式能否直接迁移到其他空间控制任务（如深度、姿态、轨迹），仅用简单几何数据即可实现准确控制？这需要验证解耦机制在不同控制语义下的普适性。

3. **数据复杂度的相变边界**：低复杂度合成数据的最优“简单度”如何量化？是否存在一个关于数据集复杂度和控制学习效率的相变边界？$\nu_{\mathrm{drift}}$ 指标为此提供了可能的量化工具，但需要更系统的实验验证。

4. **无丢弃的保先验方案**：若不丢弃任何 LoRA 权重，能否通过更精细的正则化或知识蒸馏直接保留主干先验，同时避免合成数据的偏置污染？这关系到方法在更广泛部署场景中的简洁性。

5. **跨主干泛化性**：在不同视频生成骨干上（如 HunyuanVideo、Sora 类模型），是否仍能观察到相同的“少即是多”效应？这决定了该范式的生态影响力边界。



## 原文 PDF

![[paperPDFs/CVPR_2026/Less_is_More_Data_Efficient_Adaptation_for_Controllable_Text_to_Video_Generation.pdf]]

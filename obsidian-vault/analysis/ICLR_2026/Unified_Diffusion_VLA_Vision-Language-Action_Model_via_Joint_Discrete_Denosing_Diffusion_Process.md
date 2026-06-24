---
title: "Unified Diffusion VLA: Vision-Language-Action Model via Joint Discrete Denosing Diffusion Process"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unified_Diffusion_VLA_Vision-Language-Action_Model_via_Joint_Discrete_Denosing_Diffusion_Process.pdf
aliases:
- UVUDV
- UDVVLAMJDDDP
acceptance: accepted
tags:
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: 联合离散去噪扩散过程（JD3P）：将未来图像和动作 tokens 在同一个离散扩散轨迹中同步去噪，每一步动作 tokens 因果地关注图像 tokens，通过迭代精炼实现从视觉观察到动作的渐进式映射。
primary_logic: 同步联合去噪使得动作预测在持续、充分的未来视觉引导下由粗到精地演化，将抽象的动作推理转化为以视觉预测为条件的逆运动学问题，从而在统一的扩散轨迹中实现理解、生成和执行的深度协同。
claims:
- JD3P 联合解码相比自回归解码在 CALVIN 上平均长度提升 0.46（4.64 vs. 4.18），推理速度提升 4.3 倍（219.3 vs. 50.2 tokens/s）。
- 联合预测未来图像（而非无视觉生成或仅重建当前图像）使 CALVIN 平均长度从 4.21/4.39 显著提升至 4.64。
- UD-VLA 在 CALVIN (Avg. Len. 4.64)、LIBERO (Avg. 96.1%) 和 SimplerEnv (Overall 76.0%) 上均取得 SOTA，超越所有先前统一 VLA。
- Hybrid attention（块内双向、块间因果）比纯因果或纯双向注意力平均长度提升 0.32–0.60。
paradigm: 同步联合去噪使得动作预测在持续、充分的未来视觉引导下由粗到精地演化，将抽象的动作推理转化为以视觉预测为条件的逆运动学问题，从而在统一的扩散轨迹中实现理解、生成和执行的深度协同。
---

# Unified Diffusion VLA: Vision-Language-Action Model via Joint Discrete Denosing Diffusion Process

> [!tip] 核心洞察
> 同步联合去噪使得动作预测在持续、充分的未来视觉引导下由粗到精地演化，将抽象的动作推理转化为以视觉预测为条件的逆运动学问题，从而在统一的扩散轨迹中实现理解、生成和执行的深度协同。

| 字段 | 内容 |
|------|------|
| 中文题名 | 统一扩散VLA：基于联合离散去噪扩散过程的视觉-语言-动作模型 |
| 英文题名 | Unified Diffusion VLA: Vision-Language-Action Model via Joint Discrete Denosing Diffusion Process |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=UvQOcw2oCD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | UD-VLA (Unified Diffusion VLA) |
| Dataset | CALVIN ABCD→D, LIBERO, SimplerEnv-WidowX, JD3P Decoding Efficiency (CALVIN) |

> [!tip] 效果简介
> - CALVIN ABCD→D 上，Average Length (Avg. Len.) 为 4.64，对比 MDT 4.52，变化 +0.12。
> - LIBERO 上，Average Success Rate (%) 为 96.1，对比 F1 (best prior, exact avg. not reported but lower)，变化 outperforms all baselines (SOTA)。
> - SimplerEnv-WidowX 上，Overall Success Rate (%) 为 76.0，对比 SpatialVLA/F1 (next best, exact overall not reported but lower)，变化 outperforms all baselines。

## 概述

现有统一视觉-语言-动作（VLA）模型普遍将视觉生成与动作预测视为分离的模块或解码过程，限制了未来视觉信息对动作推理的直接引导，导致视觉与动作之间缺乏内禀的协同。针对这一瓶颈，本文提出统一扩散 VLA（Unified Diffusion VLA, UD-VLA），以联合离散去噪扩散过程（Joint Discrete Denoising Diffusion Process, JD3P）为核心，将未来图像和动作 tokens 置于同一个离散扩散轨迹中同步去噪，使动作预测能够在持续的未来视觉引导下由粗到精地演化，从而实现理解、生成和执行的深度耦合并存。

UD-VLA 通过三项关键设计构筑统一的生成—行动回路：1）采用 VQ 视觉分词器与 FAST 动作分词器将多模态输入/输出统一为离散 token 序列，无需外部专家；2）提出混合注意力机制，在生成块（未来图像）和动作块内部使用双向注意力以充分利用模态内上下文，块间使用因果注意力（视觉→动作），杜绝动作向视觉的信息泄漏；3）基于 JD3P 进行联合解码，在每一去噪步中图像 tokens 被优先更新，随后动作 tokens 因果性地关注当前图像 tokens，通过迭代精炼实现从视觉观察到动作的渐进式映射。训练采用两阶段策略：先在视频数据上以后训练方式预测未来图像以激活世界模型能力，再在机器人数据上联合训练图像生成与动作预测。

实验结果表明，UD-VLA 在多个长序列机器人操作基准上取得最优性能：在 CALVIN ABCD→D 条件下平均任务长度达到 4.64，超越先前最佳方法 MDT（4.52）以及所有统一 VLA 基线；在 LIBERO 基准上平均成功率 96.1%，其中物体和长序列子任务分别达到 98.8% 和 95.2%；在 SimplerEnv‑WidowX 基准上整体成功率 76.0%，堆叠任务显著领先。相较于自回归解码，JD3P 带来 4.3 倍的推理速度提升（219.3 tokens/s vs. 50.2 tokens/s），同时动作质量更高（平均长度 +0.46）。消融研究进一步确认，混合注意力、预测未来图像（而非不生成图像或重建当前帧）以及联合扩散解码是性能增益的关键来源。在真实世界实验中，UD-VLA 在堆碗、摆块、翻塔等任务上成功率超过 80%，并对未见物体和场景展现出强泛化能力。

## 背景与动机

近年来，视觉‑语言‑动作模型（VLA）逐渐成为具身智能的核心范式，旨在统一多模态理解与物理执行。为突破早期流水线式设计的局限，一系列统一 VLA（如 GR‑1、SEER、UP‑VA、F1 等）试图在单一框架内同时处理视觉生成与动作预测，期望通过共享的表征和联合训练实现理解、生成与执行的协同。然而，这些工作大多将视觉生成和动作预测视为分离的模块或解码过程（Table 1）：部分方法依赖外部专家（例如独立 ViT 编码器、扩散解码器）进行视觉处理；另一部分虽统一了输入输出空间，却采用分离的视觉解码与动作解码，或在训练时建模视觉但推理时仅解码动作（如 WorldVLA、UniVLA），或将视觉生成与动作预测分配给不同的生成范式（如 CoT‑VLA 用自回归解码图像、扩散解码动作）。这种**分离式的设计**直接切断了未来视觉信息对动作推理的持续引导，导致视觉与动作之间缺乏内禀的协同——动作预测既不能从逐步生成的未来图像中获益，也无法利用视觉预测的迭代精炼来修正自身的决策。

后续消融实验清楚地揭示了这一缺口的代价：显式预测未来图像作为生成目标，相比完全不生成视觉或仅重建当前帧，可将 CALVIN 平均任务长度从 4.21/4.39 显著提升至 4.64（Table 6），证明未来视觉知识对动作质量的因果性支撑；而分离式范式恰恰抹去了这一关键信息通道。注意力机制的设计同样暴露出协同不足的缺陷——许多方法采用纯因果注意力或简单的块间因果/块内双向，要么压制了模态内部的必要交互，要么造成动作到视觉的信息泄露，直接损害长周期任务表现（纯因果与纯双向的平均长度仅为 4.04 和 4.32，远低于精心设计的混合注意力下的 4.64，Table 5）。此外，解码效率与动作质量的权衡也是一大痛点：自回归解码速度慢（约 50 tokens/s），独立扩散或并行解码（如 Jacobi）又往往以质量退让为代价，而分离式设计难以让视觉与动作在去噪过程中相互校准，从而错失了同时提升质量与速度的机会（Table 7）。

上述瓶颈指向一个核心动机：**需要一种能将未来视觉生成与动作预测内在耦合的机制**，使动作推理能够在持续、充分的未来视觉引导下由粗到精地演化，将抽象的动作规划转化为以视觉预测为条件的逆向运动学问题。受离散扩散模型在生成任务上的成功启发，本文提出**联合离散去噪扩散过程（JD3P）**：将未来图像 tokens 与动作 tokens 置于同一条离散扩散轨迹中，通过逐时间步的同步去噪实现联合生成；每一步动作 tokens 因果地关注图像 tokens（当前观测与逐步恢复的未来视觉），从而在统一的扩散轨迹中实现理解、生成和执行的深度协同。配合精心设计的统一离散分词、块内双向‑块间因果的混合注意力，以及先视频后机器人的两阶段训练，本文的 UD‑VLA 首次在统一 VLA 中填补了视觉‑动作内在协同的空白，并在 CALVIN、LIBERO、SimplerEnv 等多个权威基准上取得了全面的 SOTA 性能与显著的推理效率提升。

## 核心创新

现有统一VLA（如WorldVLA、UniVLA、CoT-VLA）普遍将视觉生成与动作预测置于分离的解码模块中，视觉未来信息无法直接影响动作推理过程，导致视觉-动作之间缺乏内在的协同关系。UD-VLA 通过 **联合离散去噪扩散过程（JD3P）** 打破这一瓶颈：将未来图像和动作令牌统一在同一离散扩散轨迹中同步去噪，并且在每一步去噪中动作令牌因果地关注图像令牌，使动作预测随视觉信号的逐步恢复而由粗到精地演化。这一设计将抽象的动作规划转化为以未来视觉预测为条件的“逆运动学”问题，使得理解、生成与执行在统一的扩散轨迹中深度耦合，形成内禀的协同效应。

### 关键机制：JD3P 与三处核心改动

相较于基线方法，UD-VLA 在以下四个 **changed slots** 上实现了系统性创新，共同支撑 JD3P 的联合解码能力。

- **解码方式：从独立解码到联合扩散。**  
  先前工作使用自回归（AR）、独立扩散（ID）或混合方案分别处理视觉与动作模态，视觉输出对动作预测的辅助仅在解码终端生效，无法在中间过程中提供引导。JD3P 则将固定长度的图像 token 和可变长的动作 token 拼接成一个联合序列，在每一步去噪时按照因子化概率  
  $$p_{\boldsymbol{\theta}}(\mathbf{v}_{t-1},\mathbf{a}_{t-1}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c}) = p_{\theta}(\mathbf{v}_{t-1}\mid\mathbf{v}_t,\mathbf{c})\, p_{\theta}(\mathbf{a}_{t-1}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c})$$  
  同时恢复图像与动作，且动作模型显性地以当前视觉 token $\mathbf{v}_t$ 为条件。这使得动作预测能够持续获得逐步精炼的未来视觉信息，从而在迭代射影中实现从视觉观察到动作的渐进式映射。**Table 7** 显示，JD3P 相较于 AR 解码在 CALVIN 上平均长度提升 0.46（4.64 vs. 4.18），同时推理速度提升 4.3 倍（219.3 vs. 50.2 tokens/s），验证了联合扩散在质量与效率上的双重优势。

- **模态统一方式：移除外部专家，统一离散 token 空间。**  
  基线方法多依赖外部编码器/解码器（如 ViT、扩散解码器）或分离的 token 空间，增加了系统复杂度并可能阻碍端到端的耦合学习。UD-VLA 采用 VQ 视觉分词器 (Zheng et al., 2022) 和 FAST 动作分词器 (Pertsch et al., 2025) 将图像与动作统一离散化，形成单一的多模态 token 序列：  
  $$[ \text{text tokens} ; \text{current image tokens} ; \text{future image tokens} ; \text{action tokens} ].$$  
  序列以文本和当前图像为条件，未来图像与动作作为联合生成目标，无需任何外部专家组件，从而在统一的词汇表和 Transformer 主干下实现全模态的紧耦合学习（Section 3.1, Figure 1）。

- **注意力机制：混合注意力防止信息泄露并强化模态内交互。**  
  纯因果注意力限制了图像生成所需的全局上下文，纯双向注意力则可能造成动作 token 向视觉 token 的信息泄漏。UD-VLA 提出 **Hybrid Attention**（Figure 2）：在生成块（未来图像）和动作块内部使用双向注意力以充分利用模态内依赖，而块间采用严格因果注意力（视觉→动作，无反向），阻断动作向视觉的信息回流。**Table 5** 的消融实验表明，这种混合注意力在 CALVIN 上的平均长度达到 4.64，比纯因果（4.04）和纯双向（4.32）分别高出 0.60 和 0.32，验证了该设计在防止信息泄漏与增强模态内协同方面的关键作用。

- **训练策略：两阶段激活视觉生成能力。**  
  不同于在机器人数据上单阶段微调，UD-VLA 采用两阶段训练：（i）首先在视频数据上以世界模型方式后训练，仅预测未来图像，使模型获取生成可靠视觉预测的能力；（ii）再在机器人数据上联合训练图像生成与动作预测，同时使用 $\omega$ 降权重视觉损失以平衡类别不平衡（Section 3.2, Figure 1）。这种渐进式策略确保了第二阶段能够有效耦合视觉-动作联合任务，而不会因图像生成难度过大而损伤动作学习。**Table 6** 的消融实验进一步证实，以未来图像为生成目标相较于无视觉生成（Avg. Len. 4.21）或仅重建当前图像（4.39）能显著提升动作质量（4.64），说明未来视觉信息的显式建模是动作推理增益的核心来源。

### 从核心创新到 SOTA 表现

上述四个改动的协同效果直接体现在多个机器人操作基准上：UD-VLA 在 CALVIN 长序列操纵（Table 2, Avg. Len. 4.64）、LIBERO（Table 3, Avg. 96.1%）、SimplerEnv-WidowX（Table 4, Overall 76.0%）均取得 SOTA 成绩，超越所有先前统一 VLA（包括 MDT、F1、SpatialVLA 等）。特别是在 CALVIN 上，JD3P 带来的性能增益（+0.12 相对于前最强方法 MDT 的 4.52）和速度提升（4.3×）共同证明了联合扩散与混合注意力等创新在长序列任务中的累积效应。真实世界实验（Figure 3, Section 4.4）展示了 UD-VLA 在堆碗、摆块、翻塔等任务上超过 80% 的成功率，优于 GR00T N1 和 UniVLA，进一步验证了其泛化能力。

> 注：生成图像的保真度受限于离散 token 的压缩程度和未使用大规模生成预训练，详见 Limitations。

## 整体框架

![[obsidian-vault/assets/figures/papers/iclr26_0013_UvQOcw2oCD_Unified_Diffusion_VLA_Vision-Language-Action_Mod/figures/002_Figure_1.jpg]]
*Figure 1: Overview of our Unified Diffusion VLA. 1. We construct our UD-VLA and formalize a Joint Discrete Denoising Diffusion Process (JD3P) to allow visual generation and action prediction to be intrinsically synergistic. 2. We design a two-stage training, including a post-training stage in a world-model manner to predict future images and a fine-tuning stage to generate both future images and actions. 3. During inference, the noising fixed-length image tokens and varied-length action tokens are denoised into clean tokens after T steps in JD3P*

![[obsidian-vault/assets/figures/papers/iclr26_0013_UvQOcw2oCD_Unified_Diffusion_VLA_Vision-Language-Action_Mod/figures/003_Figure_2.jpg]]
*Figure 2: Hybrid attention mechanism in UD-VLA*

UD-VLA 的整体设计围绕一个核心瓶颈展开：现有统一 VLA 将视觉生成与动作预测视为分离模块，未来视觉信息无法直接、持续地引导动作推理，导致视觉–动作之间缺乏内禀协同。为解决这一问题，UD-VLA 将视觉生成和动作预测统一进同一个离散扩散过程，使动作在每一步都能以当前去噪得到的未来视觉为条件，从而实现同步、由粗到精的跨模态联合解码。

图 1 概括了整个框架，主要包括三条设计轴线：
1. **统一离散化与序列化**：通过 VQ 视觉分词器（Zheng et al., 2022）和 FAST 动作分词器（Pertsch et al., 2025）将图像、动作与语言多模态统一为离散 token，并与 [text tokens ; current image tokens ; future image tokens ; action tokens] 格式组织成单一多模态序列。
2. **联合离散去噪扩散过程（JD3P）**：将固定的图像 token 序列和变长的动作 token 序列拼接为联合扩散目标，通过 mask-and-replace 的方式同步去噪。每一步去噪时，动作头以当前视觉 token 为条件进行预测，图像和动作之间形成因果式的迭代精炼，使抽象的动作推理转化为以未来视觉为引导的逆运动学问题。
3. **两阶段训练与高效推理**：第一阶段在大型视频数据上进行后训练，使模型具备预测未来图像的世界模型能力；第二阶段在机器人数据上联合微调视觉生成与动作预测。推理侧则通过置信度引导解码、Top-K 更新以及固定令牌的 KV Cache 预填充，大幅提升解码效率（较自回归解码提速 4.3 倍）而不损失动作质量。

下面按模块详述流程。

### 多模态统一分词与序列构建

三种模态被分别映射到离散空间：
- **语言**：由预训练 VLM 自带的 tokenizer 处理。
- **当前观测图像**：使用 VQ 视觉分词器编码为一组离散 token，并置于序列的前部作为条件。
- **未来图像与动作**：均为生成目标。未来图像采用同一 VQ 分词器编码，动作采用 FAST 分词器编码（动作块大小固定或变长）。

最终序列格式化为：
$$
[ \text{text tokens} ; \text{current image tokens} ; \text{future image tokens} ; \text{action tokens} ]
$$
其中，文本和当前图像仅作为条件输入，模型只对 future image tokens 和 action tokens 进行去噪生成。特殊标记（如 `<BOI>`、`<EOI>`、`<BOA>` 等）用于分隔不同块，以便后续注意力控制。

### 多模态 Transformer 骨干与混合注意力

骨干网络沿用预训练 VLM 的多模态 Transformer 结构，负责在统一序列上执行条件生成。为避免传统全因果注意力中动作信息向视觉部分的泄漏（从而削弱未来视觉对动作的引导），UD-VLA 设计了混合注意力机制（图 2）：
- **块内双向注意力**：在生成块（未来图像）和动作块内部分别采用双向注意力，充分建模模态内在依赖，可视为利用视觉上下文或动作序列内部的互信息。
- **块间严格因果**：生成块注意输入（文本 + 当前图像），动作块在每一层同时注意输入和生成块；但任何反向信息流（动作→生成、动作→输入）均被切断。这保证了动作总是能以当前已去噪的未来视觉为条件，而不会提前污染视觉预测。

消融实验表明，这种混合机制在 CALVIN 上将平均任务长度从纯因果的 4.04 和纯双向的 4.32 提升至 4.64（表 5），验证了防止信息泄漏并充分利用模态内双向交互的重要性。

### 联合离散去噪扩散过程（JD3P）

JD3P 是整个流程的生成核心。令完整的联合目标序列为：
$$
\mathbf{v}_0,\mathbf{a}_0 = (v_{0,1},\dots,v_{0,L_v},a_{0,1},\dots,a_{0,L_a})
$$
其中 $\mathbf{v}_0$ 为未来图像的离散 token 序列，$\mathbf{a}_0$ 为动作 token 序列，长度 $L_v$ 固定，$L_a$ 随任务变化。

**加噪过程**（训练时）采用离散扩散中的独立 mask 替换操作：对每个 token 以概率 $\beta_t$ 替换为 `<MASK>` 令牌，其一步转移定义为
$$
\mathbf{Q}_t \mathbf{e}_{t,r} = (1-\beta_t)\mathbf{e}_{t,r} + \beta_t \mathbf{e}_{\mathrm{M}}
$$
经过 $T$ 步后，序列趋于全 mask 状态。

**去噪过程**（训练与推理时）则基于因子化条件概率：
$$
p_{\boldsymbol{\theta}}(\mathbf{v}_{t-1},\mathbf{a}_{t-1}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c}) = p_{\theta}(\mathbf{v}_{t-1}\mid\mathbf{v}_t,\mathbf{c}) \, p_{\theta}(\mathbf{a}_{t-1}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c})
$$
即视觉去噪仅依赖上下文 $\mathbf{c}$（文本 + 当前图像）和当前视觉状态 $\mathbf{v}_t$，动作去噪还额外以 $\mathbf{v}_t$ 为条件。这种设计使得在每个去噪步，动作都能利用同一步下已精细化的视觉信息，实现真正的视觉导向式动作规划。

训练损失仅计算被 mask 位置的交叉熵：
$$
\mathcal{L}_{\mathrm{CE}}(\theta) = -\omega \sum_{j}^{L_v} \log p_{\theta}^{(v)}(v_{0,j}\mid\mathbf{v}_t,\mathbf{c}) \cdot \mathbb{1}\{v_{t,j}=\mathrm{M}\}
- \sum_{i}^{L_a} \log p_{\theta}^{(a)}(a_{0,i}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c}) \cdot \mathbb{1}\{a_{t,i}=\mathrm{M}\}
$$
视觉部分通过权重 $\omega$ 平衡类别不均衡（视觉 token 数量远多于动作 token），避免视觉损失主导训练。

### 推理时解码

推理从纯 mask 的视觉与动作序列开始，在 $T$ 步迭代中去噪。每步采用置信度引导的 Top-K 选择：
1. 对每个被 mask 的位置 $r$ 计算置信度 $q_{t-1,r} = \max_\ell p_{\theta}(\ell \mid \mathbf{v}_t, \mathbf{u})$。
2. 选择 top $(1-\rho_t)|M_t|$ 个高置信度 mask 位置构成更新集合 $\Omega_t$。
3. 对 $\Omega_t$ 中的视觉和动作 token，通过 Gumbel-max 采样得到更新后 token：
   $$
   v_{t-1,j}, a_{t-1,i} = \mathop{\mathrm{GumbelMax}}_{y} p_{\theta}(y\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{u}),\quad (j,i)\in\Omega_t
   $$
余弦形式的 mask 调度 $\rho_t$ 控制更新速率，早期大步更新粗粒度结构，后期精细修正细节。

为了进一步加速，UD-VLA 预填充输入和分隔 token 的 KV Cache，避免每步重复计算固定部分；同时解码空间映射确保预测的离散 token 始终位于对应模态的有效码本内。

### 两阶段训练策略

1. **后训练阶段（世界模型训练）**：在大量视频数据上，只训练模型预测未来图像。此阶段冻结语言部分，仅更新视觉生成相关参数，使模型先具备强健的未来帧预测能力。
2. **联合微调阶段**：在机器人数据上同时优化未来图像生成和动作预测。两条损失共同作用，使模型在联合去噪时能从世界模型中受益，进而提升动作质量。

实验表明，预测未来图像作为生成目标（Avg. Len. 4.64）显著优于不生成图像（4.21）或仅重建当前图像（4.39），证实了未来视觉信息对动作推理的显式引导机制（表 6）。此外，与独立扩散和自回归解码相比，JD3P 联合去噪在同等推理预算下取得更高动作质量，且实现了 4.3 倍解码加速（表 7）。

综上，UD-VLA 整体框架以统一离散化为基础，通过混合注意力和 JD3P 构建了一个内禀协同的生成式 VLA。其输入为语言指令和当前观测，输出为未来图像的 token 序列与对应动作 token 序列，二者在一系列同步去噪步中逐步浮现，最终由解码器还原为图像和连续动作指令，驱动机器人交互。

## 核心模块与公式推导

### 1. 统一多模态分词与序列构建
UD‑VLA 使用 VQ 视觉分词器（Zheng et al., 2022）和 FAST 动作分词器（Pertsch et al., 2025）将图像与动作离散化，并与语言 token 一起拼接为统一的条件生成序列：
```
[text tokens; current image tokens; future image tokens; action tokens]
```
文本和当前图像 tokens 作为条件上下文，未来图像和动作 tokens 构成联合生成目标。该序列格式将未来预测与动作推理纳入同一框架，是后续联合扩散的基础。

### 2. 混合注意力机制（Hybrid Attention）
序列被划分为生成块（未来图像 tokens）与动作块。Transformer 采用混合注意力遮罩：
- **块内双向注意力**：充分捕捉模态内部依赖；
- **块间因果注意力**：生成块关注输入块，动作块关注输入块和生成块，禁止动作→视觉的信息回流。
该设计防止信息泄漏的同时保留了必要的跨模态交互，消融实验表明其优于纯因果或纯双向注意力（Table 5）。

### 3. 联合离散去噪扩散过程（JD3P）
JD3P 将未来图像生成与动作预测统一在一条离散扩散轨迹中同步去噪，是 UD‑VLA 的核心机制。

设联合离散序列为
$$
\mathbf{v}_0,\mathbf{a}_0 = (v_{0,1},\dots,v_{0,L_v},a_{0,1},\dots,a_{0,L_a})
$$
其中 $v_{0,j}$、$a_{0,i}$ 分别为干净的未来图像 token 和动作 token，$L_v$ 和 $L_a$ 为序列长度。前向扩散以概率 $\beta_t$ 将 token 替换为 `<MASK>`：
$$
\mathbf{Q}_t \mathbf{e}_{t,r} = (1-\beta_t)\mathbf{e}_{t,r} + \beta_t \mathbf{e}_{\mathrm{M}}
$$
$\mathbf{e}_{t,r}$ 是时间步 $t$ 第 $r$ 个 token 的独热编码，$\mathbf{e}_{\mathrm{M}}$ 对应 `<MASK>`。

去噪过程对联合分布进行因子分解，令动作额外以当前视觉 tokens 为条件：
$$
p_{\boldsymbol{\theta}}(\mathbf{v}_{t-1},\mathbf{a}_{t-1}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c}) = p_{\theta}(\mathbf{v}_{t-1}\mid\mathbf{v}_t,\mathbf{c}) \, p_{\theta}(\mathbf{a}_{t-1}\mid\mathbf{v}_t,\mathbf{a}_t,\mathbf{c})
$$
$\mathbf{c}$ 为条件上下文（语言指令与当前图像）。该分解与混合注意力的因果结构严格对齐。

训练时采用单步 mask‑predict 交叉熵损失，仅对被 mask 的位置计算，并对视觉部分配以权重 $\omega$ 以缓解类别不平衡：
$$
\mathcal{L}_{\mathrm{CE}}(\theta) = -\omega \sum_{j}^{L_v} \log p_{\theta}^{(v)}(v_{0,j}\mid \mathbf{v}_t,\mathbf{c}) \cdot \mathbb{1}\{v_{t,j}=\mathrm{M}\} - \sum_{i}^{L_a} \log p_{\theta}^{(a)}(a_{0,i}\mid \mathbf{v}_t,\mathbf{a}_t,\mathbf{c}) \cdot \mathbb{1}\{a_{t,i}=\mathrm{M}\}
$$
其中 $\mathbb{1}\{\cdot\}$ 为示性函数，$p_{\theta}^{(v)}$ 和 $p_{\theta}^{(a)}$ 分别为模型对视觉 token 和动作 token 的预测概率。通过该损失，视觉生成与动作预测在统一框架下被同步优化。

### 4. 推理机制：置信度引导解码
推理时从全 `<MASK>` 的序列开始，经 $T$ 次迭代去噪。每一步维护当前被 mask 的位置集合 $M_t$，并计算每个位置 $r$ 的置信度得分 $q_{t-1,r}$（模型预测概率的最大值）。依据预设的 mask 保留比例 $\rho_t$，选出置信度最高的 $(1-\rho_t)|M_t|$ 个位置进行更新：
$$
\Omega_t = \operatorname{TopK}_{(1-\rho_t)|M_t|} \{ q_{t-1,r} : r \in M_t \}
$$
选中位置 $\Omega_t$ 通过 Gumbel‑Max 采样确定新 token，其余保持 `<MASK>`。该策略使高置信度 token 优先解码，在保证动作质量的同时获得 4.3 倍于自回归的推理速度 (Table 7)。推理中同时配合 Prefix KV Cache 与特殊分隔 token 的预填充以进一步降低延迟。

## 实验与分析

![[obsidian-vault/assets/figures/papers/iclr26_0013_UvQOcw2oCD_Unified_Diffusion_VLA_Vision-Language-Action_Mod/figures/004_Table_2.jpg]]
*Table 2: Comprehensive Evaluation of Long-Horizon Robotic Manipulation on the CALVIN Benchmark. UniVLA∗ denotes the variant without historical frames for fair comparison. Table 3: Evaluation and comparison on the LIBERO benchmark*

![[obsidian-vault/assets/figures/papers/iclr26_0013_UvQOcw2oCD_Unified_Diffusion_VLA_Vision-Language-Action_Mod/figures/005_Table_3.jpg]]

![[obsidian-vault/assets/figures/papers/iclr26_0013_UvQOcw2oCD_Unified_Diffusion_VLA_Vision-Language-Action_Mod/figures/009_Table_7.jpg]]

![[obsidian-vault/assets/figures/papers/iclr26_0013_UvQOcw2oCD_Unified_Diffusion_VLA_Vision-Language-Action_Mod/figures/006_Table_5.jpg]]
*Table 5: Effectiveness of different attention schemes. Bidirectional applies bidirectional attention over the visual generation and the action block. Causal uses a strict lowertriangular mask, and Hybrid follows Figure 2*

### 主要结果

UD‑VLA 在三个广泛使用的机器人操作基准上均取得领先结果，验证了联合离散去噪扩散过程（JD3P）的有效性。

在长序列操纵基准 CALVIN (ABCD→D) 上，UD‑VLA 实现了 **4.64** 的平均成功序列长度，超越先前最优方法 MDT 的 4.52（Table 2）。更细粒度的 1–5 任务完成率分别为 0.992 / 0.968 / 0.936 / 0.904 / 0.840，在所有难度级别上保持优势，表明模型不仅擅长短期技能，也能可靠地组合成长时序行为。

在 LIBERO 基准的四个子任务（Spatial、Object、Goal、Long）上，UD‑VLA 整体平均成功率 **96.1%**（Table 3）。尤其在物体操控（Object，98.8%）和长序列（Long，95.2%）两类最需要时序理解和物体泛化的场景中大幅超过所有先前统一 VLA，显示出联合视觉预测对动作规划的直接助益。

在 SimplerEnv‑WidowX 的全任务评估中，UD‑VLA 取得 **76.0%** 的总体成功率，并在堆叠方块（Stack Block）等对空间精度要求极高的任务上显著领先基线方法（Table 4），证明模型在仿真‑真实差距下的泛化能力。

解码效率方面，JD3P 展现出显著的优势：与自回归解码（AR）相比，JD3P 在 CALVIN 上的平均长度从 4.18 提升至 4.64（+0.46），同时推理速度达到 **219.3 tokens/s**，是 AR（50.2 tokens/s）的 **4.3 倍**（Table 7）。这一结果源于联合扩散过程允许图像与动作 token 在同一去噪轨迹中并行生成，并通过迭代精炼渐进提升动作决策的质量。

### 消融实验

为剖析各设计选择的贡献，我们在 CALVIN 上进行了系统的消融分析。

**注意力机制。** 如表 5 所示，纯因果注意力（causal）仅取得 4.04 的平均长度，纯双向注意力（bidirectional）因存在动作向视觉的反向信息泄露而止于 4.32。本文采用的混合注意力（hybrid，块内双向、块间严格因果，且视觉→动作方向不可逆）达到 **4.64**，相比纯因果和纯双向分别提升 0.60 和 0.32，证实了既防止信息泄漏又保留模态内充分交互的必要性。

**视觉生成目标。** 从生成目标的角度（Table 6），完全不生成视觉（Null）时平均长度仅为 4.21，仅重建当前观测图像（Current Image）可提升至 4.39，而显式预测未来图像（Future Image）进一步推高至 **4.64**。这一递进趋势（+0.18 和 +0.25）强有力地证明：未来视觉帧以结构化 token 序列形式提供的时序前瞻信息，对动作的正向引导作用远大于仅从当前观测隐式提取上下文。

**解码方式。** 我们将 JD3P 与自回归（AR）、Jacobi 并行解码以及独立扩散（ID，图像与动作分别扩散）进行对比（Table 7）。JD3P 在同等推理预算下不仅取得了最高的平均长度（4.64），还实现了 219.3 tokens/s 的解码速度，远超 AR（50.2）和 ID（145.8），同时 Jacobi 解码虽然速度提升（约 2×）但成功率明显下降。这表明只有将图像与动作置于同一联合去噪轨迹，才能让动作在每个扩散步充分利用不断锐化的视觉线索，从而在速度与质量间取得最佳平衡。

### 失败模式与局限性

尽管 UD‑VLA 在多任务基准上表现优异，分析中仍暴露出几个关键瓶颈，反映出当前设计的短板：

1. **视觉生成的保真度不足。** 生成的未来图像虽能保留任务级别的物体位姿与末端执行器走向，但频繁丢失纹理和背景细节（见论文 Appendix B 的生成结果）。这主要归因于未引入大规模生成预训练，以及 VQ 视觉分词器将像素压缩到低分辨率离散 token 空间时损失了高频视觉信息。
2. **像素级精确生成的困难。** 对于精细操作（例如堆叠小方块或对齐微小物体），所生成图像的物体位置与真实轨迹存在偏差，这表明当前 token 压缩率下的视觉歧义会妨碍动作规划的部分可靠性，需要更细粒度的视觉表征加以缓解。
3. **真实世界验证的场景规模有限。** 真实机器人实验仅涵盖堆碗、摆块、翻塔三个任务（Figure 3、Figure 4），且物体与背景的泛化测试虽已考虑未见类别，但任务多样性和环境复杂度仍远低于开放真实世界需求，尚未在移动操作、多室场景等设定下进行充分验证。
4. **推理超参数缺乏自适应机制。** JD3P 的去噪步数 T 和余弦 mask schedule 的速率对不同任务难度较为敏感，当前依赖固定设置，缺乏根据任务复杂度或不确定性动态调节步数的机制；在复杂环境中手动调参会降低自动化部署效率。
5. **视觉生成对长期时序规划的辅助上限未探明。** 当前未来帧预测为单步固定窗口，尚未探索在更长时序上迭代生成视觉计划（如“视觉 lookahead”），其对极长序列任务的可能收益仍有待研究。

### 重要图表结论

- **Table 1（范式对比）：** 通过与其他统一 VLA 的组件级对比，明确 UD‑VLA 是唯一既不依赖外部视觉专家、又能以联合扩散解码统一处理图像与动作的框架，奠定了后续实验观测的架构基础。
- **Table 2 与 Table 3（CALVIN 和 LIBERO 主结果）：** 展示了 UD‑VLA 在各难度级别上的全面领先，构成方法有效性的核心定量证据。
- **Table 5 与 Table 6（消融）：** 直接揭示了混合注意力和未来图像预测两个关键设计的作用强度，为“防止信息泄漏 + 显式视觉前瞻”这一因果路径提供了清晰的数值支撑。
- **Table 7（解码效率）：** 用质量‑速度联合指标证明 JD3P 的联合扩散不仅收敛更快，而且推理更高效，是实际部署中的重要优势。
- **Figure 2（混合注意力模式）：** 以直观方式呈现了块间因果与块内双向的约束关系，帮助理解信息流设计如何影响训练动力学和最终性能。
- **Figure 3 及 Appendix Figure 5–7（真实世界实验）：** 表明 UD‑VLA 在真实机械臂上能够跨见到未见物体和背景泛化，且生成了可靠的任务级未来视觉计划，成功引导动作超越其他基线（如 GR00T N1 和 UniVLA），展示了 JD3P 从仿真到现实的迁移潜力。

## 方法谱系与知识库定位

统一 VLA（Vision-Language-Action）范式的演进可划分为三个代际，其分水岭在于“视觉—动作”耦合的深度与解码过程的统一程度。UD-VLA 所在的第三范式通过**联合离散扩散过程（JD3P）**将未来图像生成与动作预测编织为同一条去噪轨迹，从而把前序方法中的模块化耦合推向内禀协同。

**第一代：外部专家与分离解码**。GR-1、SEER、DreamVLA、F1、UP-VLA 等方法虽引入视觉生成，但视觉编码器/解码器（如外部 ViT、扩散解码器）作为独立模块存在；动作预测与视觉生成共享条件上下文，却在解码阶段完全分离。此类设计使未来视觉信息无法直接、持续地引导动作推理，成为性能提升的结构性瓶颈。

**第二代：统一输入输出空间但解码分离**。WorldVLA、UniVLA、CoT-VLA 将视觉和动作统一为离散 token 序列并一同建模，但在推理时仍将视觉生成视为辅助任务或采取“视觉 AR + 动作扩散”的混合解码。其典型局限是：训练时建模视觉信息，推理时却丢弃或仅部分利用，视觉—动作间的信息流单向且带宽受限。

**第三代：联合扩散解码**。UD-VLA 直接以未来图像 tokens 作为动作推理的因果条件（而非副产品），通过 JD3P 机制在每一个去噪步中让动作 tokens **因果地关注当前图像 tokens**，并在整个轨迹中逐步精炼。这一设计将抽象的规划问题转化为以视觉预测为条件的逆运动学求解（Table 1，Section 3.2）。证据链表明：相较于独立扩散（ID）和自回归（AR）解码，JD3P 在 CALVIN 上实现平均长度 +0.46（4.64 vs. 4.18）且推理速度提升 4.3×（219.3 vs. 50.2 tokens/s）（Table 7），证明联合去噪在质量与效率两端均带来质的增益。

从因果操纵的视角，UD-VLA 的三个核心设计槽位——**统一离散分词**、**混合注意力**、**JD3P 解码**——构成一条因果链：统一分词消除模态间隙；混合注意力通过“块内双向、块间因果”的掩码（Figure 2）防止动作到视觉的信息泄漏，使视觉对动作的引导纯净单向（消融显示 Hybrid vs. Causal/Bidirectional 分别提升 0.60/0.32，Table 5）；JD3P 则在此注意力约束下实现动作以中间视觉 tokens 为条件的迭代精炼（Table 6 证实预测“未来图像”而非“当前图像”或“无图像”带来 +0.43/ +0.25 的显著增益）。该因果链在所有基准（CALVIN Avg. Len. 4.64，LIBERO Avg. 96.1%，SimplerEnv Overall 76.0%）上均收束为 SOTA 结果，且真实世界实验中堆碗、摆块、翻塔等任务成功率超 80%（Figure 3），初步验证了泛化性。

**适用边界与局限**。UD-VLA 的增益高度依赖未来图像所包含的时序先验，因此其优势主要体现在**需要长序列推理与视觉前瞻的任务**（如 CALVIN 长序列、LIBERO 长任务）。对于短时、纯反应式操作，额外视觉生成的计算开销可能贡献有限。当前方法的真实世界验证仅覆盖三任务、有限物体和桌面场景，开放环境、移动操作或具身导航等更广泛场景尚未测试。

局限层面，最突出的瓶颈是**生成未来图像的视觉保真度不足**（如纹理、背景细节丢失），根源在于未使用大规模生成预训练（仅依赖视频后训练阶段）以及压缩 token 空间的信息瓶颈。由此导致像素级精确生成困难，限制了需要精细视觉对齐的灵巧操作。此外，JD3P 的迭代步数 $T$ 和 mask schedule 目前需针对场景静态设定，缺乏自适应步数选择机制，使得在复杂变动环境中难以动态平衡速度与质量（Section 4.3）。

**开放问题**。①能否通过更大规模的视频扩散预训练或更强的视觉 tokenizer（如更高分辨率的 VQ-VAE）提升未来图像保真度，同时保持推理效率不衰退？②JD3P 的离散扩散框架能否自然拓展到**连续动作空间**或高频遥操作数据流，而无需重训动作分词器？③联合扩散轨迹是否可与测试时计算扩展（如树搜索、推理时进化）结合，以求解更长期、组合式的任务规划？④发展**自适应去噪调度**（根据任务难度或置信度动态调整去噪步数）或学习一种“早停”机制，是进一步压缩推理成本、扩展至实时应用的关键路径。

## 原文 PDF

![[obsidian-vault/paperPDFs/ICLR_2026/Unified_Diffusion_VLA_Vision-Language-Action_Model_via_Joint_Discrete_Denosing_Diffusion_Process.pdf]]
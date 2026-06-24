---
title: "OmniGen2: Towards Instruction-Aligned Multimodal Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OmniGen2_Towards_Instruction_Aligned_Multimodal_Generation.pdf
code_link: "https://github.com/VectorSpaceLab/OmniGen2"
aliases:
- OmniGen2
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 构建解耦的文本/图像生成架构、Omni-RoPE位置编码以及精心调度的多任务强化学习对齐课程，是实现全面指令跟随的关键手段。
primary_logic: 通过解耦生成路径和显式实例空间分离，基础模型保留了可塑性；在此基础上，渐进式多任务RL利用任务间的知识迁移，显著提升指令跟随的一致性和鲁棒性。
claims:
- Omni-RoPE在toy重建任务中收敛速度远快于先前方案（~800步 vs ~2500步），最终损失更低（0.003 vs 0.017），证明了其空间一致性和实例区分能力。
- 消融实验表明，仅OCR训练导致GEdit整体分数从6.28降至6.13，而Edit & GenEval联合训练产生正向协同（GenEval 0.95 vs 0.94），证明任务选择和调度至关重要。
- 编辑优先的RL课程（Edit→GenEval→IC）在所有OOD基准上表现优于T2I优先顺序（OneIG Align 0.8289 vs 0.8242），确认了课程顺序的重要性。
- 全RL课程在Emu-Edit、GEdit、OmniContext等基准上一致大幅超越基础模型，且不对单任务造成负面影响，体现通用对齐效果。
---

# OmniGen2: Towards Instruction-Aligned Multimodal Generation

> [!tip] 核心洞察
> 通过解耦生成路径和显式实例空间分离，基础模型保留了可塑性；在此基础上，渐进式多任务RL利用任务间的知识迁移，显著提升指令跟随的一致性和鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniGen2：面向指令对齐的多模态生成 |
| 英文题名 | OmniGen2: Towards Instruction-Aligned Multimodal Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.18871) · [Code](https://github.com/VectorSpaceLab/OmniGen2) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | OmniGen2 |
| Dataset | GenEval, OneIG-Bench, Emu-Edit, GEdit-Bench-EN |

> [!tip] 效果简介
> - GenEval 上，Overall Score 0.95 vs 0.88 (BAGEL) (+0.07)。
> - OneIG-Bench 上，Overall Score 0.47 vs 0.36 (BAGEL) (+0.11)。
> - Emu-Edit 上，CLIP-Out 0.311 vs 0.307 (BAGEL) (+0.004)。

## 概述

### 问题与动机

多模态生成模型在统一框架下处理文本到图像生成、图像编辑和上下文生成等任务时，面临一个核心瓶颈：**在复杂真实场景中缺乏系统性的指令对齐**，导致模型难以兼顾多任务性能，泛化能力受限。现有方案或采用单一Transformer同时处理文本与图像生成，或依赖固定长度的query token压缩指令，这些设计在跨图像空间一致性和实例区分上存在天然局限。

### 核心方法与贡献

OmniGen2 提出了一个面向指令对齐的多模态生成框架，其核心设计包含三个关键创新：

1. **解耦生成架构**：采用独立的文本自回归Transformer和扩散图像Transformer，通过视觉语言模型（VLM）的隐藏状态进行桥接，使文本和图像生成路径各司其职，保留基础模型的可塑性。

2. **Omni-RoPE位置编码**：引入三维位置标识符 $(\Delta_I^{(k)}, h, w)$，将实例身份与局部空间坐标显式分离。这一设计使模型能够区分不同图像的同时保持空间一致性，在toy重建任务中收敛速度（约800步）远超先前方案（1200~2500步），最终损失也更低（0.003 vs 0.017）。

3. **渐进式多任务RL对齐课程**：基于Flow-GRPO的三阶段课程（Edit → GenEval → IC），通过精心调度的任务顺序实现正向知识迁移。消融实验表明，编辑优先的课程在所有分布外（OOD）基准上均优于T2I优先顺序。

### 方法谱系与知识库定位

OmniGen2 在统一多模态生成领域定位为**指令对齐型解耦架构**。与 **BAGEL**、**UniWorld-V1** 等统一多模态生成模型相比，其解耦设计避免了单一Transformer在多任务间的表示冲突。与 **FLUX.1-dev** 等专精文本到图像生成的扩散模型相比，OmniGen2 通过VLM桥接实现了对多模态指令的深层理解。在位置编码层面，Omni-RoPE 改进了 **Lumina-Image-2.0** 和 **Qwen2-VL** 的累积坐标偏移方案，将实例区分能力显式编码到位置标识中。在训练策略上，其渐进式多任务RL课程是对单任务RL微调的显著扩展，为多模态生成的对齐训练提供了新的范式。

### 主要结果概览

在多个基准上的综合评估验证了OmniGen2的通用对齐效果：

- **GenEval** 整体得分 **0.95**，超越 BAGEL（0.88）达 +0.07。
- **OneIG-Bench** 整体得分 **0.47**，较 BAGEL（0.36）提升 +0.11。
- **GEdit-Bench-EN** 整体得分 **7.21**，超越闭源模型 Gemini-2.5-Flash-Image（7.10）。
- **OmniContext** 上下文生成基准整体平均分 **7.95**，优于 Qwen-Image-Edit-2509（7.84）。

全RL课程在Emu-Edit、GEdit、OmniContext等基准上一致大幅超越基础模型，且未对单任务性能造成负面影响，体现了指令对齐的鲁棒性和泛化能力。

## 背景与动机

多模态生成模型在近年取得了显著进展，从早期的文本到图像（T2I）生成逐步扩展到图像编辑、上下文生成等更复杂的任务。然而，现有模型在实际部署中暴露出一个核心瓶颈：**在复杂真实场景（如上下文生成、精细编辑）中缺乏系统性的指令对齐，导致泛化能力不足，无法兼顾多任务性能**。具体表现为，模型往往能完成单一任务的生成，但面对组合指令、多图像上下文或需要精确空间控制的编辑任务时，指令跟随的准确性和一致性显著下降。

当前的多模态生成方法存在两个主要缺口。第一，架构层面，主流方案（如 UniWorld-V1、BAGEL）通常采用单一 Transformer 同时处理文本和图像生成，这种紧耦合设计限制了模型在不同模态生成路径上的灵活性和可塑性。第二，对齐策略层面，多数模型缺乏系统性的强化学习对齐，或仅进行单任务 RL 微调，未能充分利用多任务之间的知识迁移来提升指令跟随的鲁棒性。

OmniGen2 正是针对上述缺口提出的解决方案。其核心洞察在于：**通过解耦生成路径和显式实例空间分离，基础模型能够保留更强的可塑性；在此基础上，渐进式多任务 RL 利用任务间的知识迁移，可以显著提升指令跟随的一致性和鲁棒性**。具体而言，OmniGen2 从两个方向切入：（1）构建一个架构简洁、灵活且鲁棒的基础模型，支持多样化的多模态生成任务；（2）设计一套多任务 RL 对齐方案，通过精心调度的课程学习实现全面的指令对齐。这一“基础模型 + 渐进式指令对齐”的两阶段设计，构成了 OmniGen2 的方法论核心。

## 核心创新

OmniGen2 的核心创新在于通过一套**解耦的生成架构**与**渐进式多任务强化学习对齐课程**，系统性地解决了多模态生成模型在复杂真实场景下指令对齐不足的瓶颈。其关键创新点可归纳为以下四个“changed slots”：

### 1. 解耦的自回归/扩散生成架构

与 UniWorld-V1、BAGEL 等采用单一 Transformer 同时处理文本与图像生成的方案不同，OmniGen2 将文本生成与图像生成立意解耦为两个独立的 Transformer 模块（Figure 2）。自回归文本 Transformer 由 Qwen2.5-VL-3B 初始化，负责理解多模态指令并输出高层语义表征；扩散图像 Transformer 则专门执行高保真图像合成。这一解耦设计保留了基础模型的可塑性，使各模块能够在其专长领域内最大化性能，同时通过 VLM 的隐藏状态实现语义桥接。

### 2. 可变长度隐藏状态条件注入

传统方案（如 MetaQuery）通常将多模态指令压缩为固定长度的 query tokens 再注入扩散模型，这不可避免地造成信息瓶颈。OmniGen2 直接使用 VLM 最终层的**可变长度隐藏状态**作为扩散解码器的条件信号，并通过一个轻量级的两层 Transformer refiner 将 VLM 隐藏状态、VAE 特征与噪声潜变量对齐到统一空间。这种设计保留了指令中的细粒度语义信息，为后续的高保真生成与精确编辑提供了更丰富的条件指导。

### 3. Omni-RoPE：三维解耦位置编码

多模态序列中同时存在多个图像时，位置编码必须同时满足**跨图像区分**与**单图像内空间一致性**两个需求。现有方案（如 Lumina-Image-2.0 的累积坐标偏移、Qwen2-VL 的 RoPE 变体）往往将实例身份与空间坐标耦合，导致学习效率低下。

Omni-RoPE 将每个 token 的位置显式分解为三维标识符：
$$\mathrm{PosID}_{k}(h, w) = (\Delta_{I}^{(k)}, h, w)$$
其中 $\Delta_{I}^{(k)}$ 是第 $k$ 张图像的实例身份（该图像内所有 token 共享），$(h, w)$ 是以 $(0,0)$ 为原点的局部二维空间坐标。这种分解使模型能够清晰区分不同图像实例，同时保持单图内的空间一致性。

**决定性证据**：在 toy 重建任务中（Table 1），Omni-RoPE 仅需约 800 步即收敛至目标损失（<0.014），而先前方案需 1200~2500 步；最终损失也显著更低（0.003 vs. 0.017）。这直接证明了其空间一致性和实例区分能力的优越性。

### 4. 渐进式多任务强化学习对齐课程

OmniGen2 的对齐策略突破了单任务 RL 微调的局限，提出**三阶段渐进式多任务 RL 课程**，采用 Flow-GRPO 算法。课程设计遵循 $S = \langle \mathcal{T}_1, \dots, \mathcal{T}_N \rangle$，每个任务 $\mathcal{T} = (\tau, \delta, \mathcal{R})$ 包含任务类型 $\tau$、数据实例 $\delta$ 和奖励函数 $\mathcal{R}$。

课程的核心调度逻辑是**编辑优先**（Edit → T2I → IC），其背后的因果机制在于：

- **任务间技能迁移**：编辑任务训练出的指令跟随能力可正向迁移至文本到图像生成（T2I），而 T2I 任务学到的组合生成能力又为上下文生成（IC）提供基础。消融实验（Table 5）证实，Edit & GenEval 联合训练产生正向协同——GenEval 从单独 Edit 训练的 0.94 提升至 0.95，GEdit Overall 从 7.01 提升至 7.19。
- **负迁移风险控制**：有限技能重叠的任务（如纯 OCR 训练）会导致 GEdit Overall 从 6.28 降至 6.13，因此课程必须谨慎选择任务组合与顺序。改变课程顺序（Edit & IC & GenEval）会直接导致 GEdit Overall 从 7.21 降至 7.06（Table 5）。
- **奖励信号鲁棒性**：引入美学奖励 HPSv3 会导致 SC 与 IC 分数崩溃（奖励黑客现象），证实奖励函数设计必须与目标任务紧密对齐。

在 OOD 基准上（Table 10），编辑优先课程在所有指标上均优于 T2I 优先顺序（如 OneIG Align 0.8289 vs. 0.8242），进一步验证了课程顺序对泛化能力的关键影响。

### 创新总结

上述四个 changed slots 构成了一个完整的创新闭环：**解耦架构**提供可塑性基础，**可变长度条件注入**保留语义保真度，**Omni-RoPE** 解决多实例空间建模难题，**渐进式 RL 课程**实现系统性的指令对齐。这套组合使 OmniGen2 在 GenEval（0.95）、OneIG-Bench（0.47）、GEdit-Bench-EN（7.21）等基准上一致超越 BAGEL、Gemini-2.5-Flash-Image 等强基线，且不对任何单任务造成性能退化。

## 整体框架

OmniGen2 遵循“基础模型预训练 + 渐进式指令对齐”的两阶段设计范式。其核心架构采用**解耦的文本与图像生成路径**，由两个独立的 Transformer 模块分别承担自回归文本生成和扩散图像生成，二者通过视觉语言模型（VLM）的隐藏状态进行桥接。

### 模块组成与数据流

整个 pipeline 由以下关键模块构成，其架构关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of OmniGen2. OmniGen2 employs separate transformers for autoregressive and diffusion. Two distinct image encoders are utilized: ViT encodes images for input into the text transformer, while VAE encodes images for the diffusion transformer*

1. **视觉语言模型（VLM）**：作为系统的语义核心，VLM 负责处理多模态输入指令（文本与图像）。输入图像经 ViT 编码后送入文本 Transformer，VLM 最终层输出的可变长度隐藏状态作为高层语义指导，传递给下游扩散解码器。该 VLM 由 Qwen2.5-VL-3B 初始化。

2. **扩散 Transformer 解码器**：接收三类条件信号——VLM 隐藏状态、VAE 编码的图像特征以及噪声潜变量。这些异构信号通过一个轻量级的双层 Transformer 精炼器（refiner）进行对齐，随后由统一的 Transformer 骨干网络执行高保真图像合成。该骨干网络沿用了 Lumina-Image 2.0 的跨模态参数共享架构。

3. **Omni-RoPE 位置编码**：为多模态序列中的所有 token 提供统一的三维位置标识符 $\mathrm{PosID}_k(h, w) = (\Delta_I^{(k)}, h, w)$，其中 $\Delta_I^{(k)}$ 是第 $k$ 张图像的实例身份标识，$(h, w)$ 是局部二维空间坐标。这一设计使模型既能区分不同图像实例，又能保持单张图像内部的空间一致性。

### 训练管线

训练分为两个宏观阶段：

- **预训练与有监督微调（SFT）**：首先在多分辨率下进行通用预训练，随后在 $1024^2$ 分辨率下执行 SFT，以获取通用视觉-语义表征和初始指令跟随能力。训练课程从通用预训练逐步过渡到通用指令对齐，任务复杂度和分辨率逐步提升（详见 Table 6）。

- **强化学习对齐（Flow-GRPO）**：在 SFT 基础上，采用在线强化学习进行多任务对齐。通过渐进式课程设计，将训练任务组织为三阶段序列 $\langle \mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3 \rangle$，每个任务 $\mathcal{T} = (\tau, \delta, \mathcal{R})$ 包含任务类型 $\tau$、具体实例 $\delta$ 和奖励函数 $\mathcal{R}$。该阶段使用 Flow-GRPO 算法，按“编辑→文本到图像生成→上下文生成”的顺序逐步注入对齐信号，利用任务间的知识迁移提升指令跟随的一致性和鲁棒性。

### 输入输出规范

- **输入**：任意交错的文本和图像序列，支持多图像上下文。
- **输出**：文本响应（由自回归 Transformer 生成）或高保真图像（由扩散 Transformer 解码器合成），具体取决于用户指令。

### 补充图表

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/001_Figure_1.jpg]]
*Figure 1: Overview of versatile abilities of OmniGen2*

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/005_Figure_4.jpg]]
*Figure 4: Overview of OmniContext benchmark. Left: Image genres included in OmniContext. Right: Example images for each genre in OmniContext*

## 核心模块与公式推导

### 3.1 解耦式多模态生成架构

OmniGen2 的核心架构创新在于将文本生成与图像生成解耦为两条独立的Transformer通路，而非采用单一Transformer同时处理两种模态。模型由两个核心模块构成：

- **视觉语言模型 (VLM)**：作为自回归文本Transformer，负责处理多模态指令（文本和图像），输出语义隐藏状态，为后续图像生成提供高层语义指导。该模块从 **Qwen2.5-VL-3B** 初始化而来。
- **扩散Transformer解码器**：接收VLM最终层的可变长度隐藏状态、VAE特征和噪声潜变量，执行高保真图像合成。该模块采用统一Transformer骨干，参数跨模态共享，遵循 **Lumina-Image 2.0** 的架构设计。

两条通路之间通过VLM隐藏状态进行桥接：VLM输出的隐藏状态直接作为扩散解码器的条件信号，替代了传统方案中固定长度的query tokens压缩方式。输入条件信号（VLM隐藏状态、VAE特征、噪声潜变量）由一个轻量级的两层Transformer refiner进行对齐。此外，模型使用两种不同的图像编码器：ViT编码图像供文本Transformer输入，VAE编码图像供扩散Transformer使用。

### 3.2 Omni-RoPE 位置编码

Omni-RoPE 是本文提出的多模态位置编码方案，旨在解决多图像场景中的实例区分和空间一致性问题。其核心公式为：

$$\mathrm{PosID}_k(h, w) = (\Delta_I^{(k)}, h, w)$$

**变量含义**：
- $k$：图像实例索引，标识当前token所属的图像
- $\Delta_I^{(k)}$：第$k$张图像的实例身份标识，该图像内所有token共享此值，用于区分不同图像
- $(h, w)$：局部二维空间坐标，从$(0, 0)$开始计算，保持单张图像内的空间一致性

这一三维位置标识符将实例身份与局部空间坐标显式分离，使模型能够在区分不同图像的同时，为图像编辑等任务保持局部空间一致性。Toy重建实验验证了该设计的有效性：Omni-RoPE在约800步即收敛至目标损失（<0.014），而先前方案需要1200~2500步；最终损失也显著更低（0.003 vs. 0.017），证明了其空间一致性和实例区分能力。

### 3.3 渐进式多任务强化学习对齐

OmniGen2 的对齐训练采用三阶段渐进式多任务RL课程，使用Flow-GRPO算法。课程序列定义为 $S = \langle \mathcal{T}_1, \dots, \mathcal{T}_N \rangle$，其中每个任务 $\mathcal{T} = (\tau, \delta, \mathcal{R})$ 包含任务类型 $\tau$、任务实例 $\delta$ 和奖励函数 $\mathcal{R}$。

三阶段课程顺序为：**编辑 (Edit) → 文本到图像 (T2I) → 上下文生成 (IC)**。这一顺序的选择基于任务间的技能迁移规律：编辑任务优先训练可建立精细的指令跟随基础，随后T2I训练拓展生成多样性，最后IC训练整合上下文理解能力。消融实验证实，编辑优先的课程顺序在所有OOD基准上均优于T2I优先顺序（OneIG Align 0.8289 vs. 0.8242），确认了课程调度对最终性能的关键作用。

训练流程整体采用两阶段设计：首先通过多分辨率、混合任务的课程学习进行预训练，获取通用视觉-语义表征；随后在1024²分辨率下进行SFT，精炼高层推理和组合技能；最后通过在线RL进行多任务对齐。

### 补充图表

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of Omni-RoPE. Each token in the k-th image is assigned a three-dimensional positional identifier*

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/004_Table_1.jpg]]
*Table 1: Comparison of RoPE designs in the toy reconstruction task. Models are trained to reproduce the k-th image among randomly sampled inputs. We report the number of steps required to reach the target (loss \< 0.014). Omni-RoPE achieves both faster convergence and lower final loss. Note*

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/013_Figure_9.jpg]]
*Figure 9: Full loss curves for the Omni-RoPE toy reconstruction experiment. Omni-RoPE converges substantially faster than prior positional encoding schemes. The inset shows late-stage optimization, where adding image index embeddings yields the lowest and most stable final loss*

## 实验与分析

### 核心性能：多任务统一评测

OmniGen2 在文本到图像生成、图像编辑和上下文生成三大类任务上均展现出领先水平，验证了其统一架构与多任务对齐策略的有效性。Table 2 汇总了各模型在理解、生成、编辑和上下文生成四个维度的综合对比。在文本到图像生成基准 **GenEval** 上，OmniGen2 取得 0.95 的整体分数，显著超越统一模型 BAGEL（0.88）和专精生成模型 Qwen-Image（0.91）。在更具挑战性的组合式提示基准 **OneIG-Bench** 上，OmniGen2 达到 0.47，较 BAGEL（0.36）提升 0.11，表明其在复杂指令跟随方面具有明显优势。

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/006_Table_2.jpg]]
*Table 2: Comparison of different models across Understanding, Generation, Editing, and In-context Generation tasks. *: The first term represents the number of parameters for text generation, while the second term corresponds to the number of parameters allocated for image generation. † refers to the methods using LLM rewriter*

在图像编辑任务上，Table 3 展示了 Emu-Edit 和 GEdit-Bench-EN 的定量结果。OmniGen2 在 Emu-Edit 的 CLIP-Out 指标上达到 0.311，略优于 BAGEL（0.307），同时保持了具有竞争力的图像一致性（CLIP-I 0.830）。在 GEdit-Bench-EN 上，OmniGen2 取得 7.21 的整体分数，超越闭源模型 Gemini-2.5-Flash-Image（7.10），并在语义一致性（SC 7.58）和感知质量（PQ 7.94）两个子维度上均表现优异。

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison on Emu-Edit [81] and GEdit-Bench-EN [54]. For Emu-Edit, CLIP-I/DINO measure consistency with the source image, while CLIP-Out measures alignment with the caption of target image, CLIP-B/32 [71] and DINO-S/16 [6] are leveraged for feature calculation. For GEdit-Bench, SC (Semantic Consistency) evaluates instruction following, and PQ (Perceptual Quality) assesses image naturalness and artifacts. Higher scores are better for all metrics*

针对上下文生成这一新兴能力维度，作者构建了 **OmniContext** 基准（Figure 4），涵盖 SINGLE、MULTIPLE 和 SCENE 三种任务类型。Table 4 的整体对比显示，OmniGen2 以 7.95 的平均分超越 Qwen-Image-Edit-2509（7.84），在需要多图像理解和一致性保持的场景中展现了更强的泛化能力。

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/008_Table_4.jpg]]
*Table 4: Overall comparison of existing models on our proposed OmniContext benchmark. ”Char. + Obj.” indicates Character + Object*

### 消融实验：多任务RL策略的关键发现

多任务强化学习对齐是 OmniGen2 性能提升的核心驱动力，但其效果高度依赖于任务选择、调度顺序和奖励设计。Table 5 的系统消融揭示了以下关键规律：

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/009_Table_5.jpg]]
*Table 5: Ablation study of multi-task reinforcement learning strategies. T2I, Edit, and IC tasks are trained for 1500, 700, and 200 steps, respectively*

**任务间的协同与干扰。** 仅使用 OCR 数据进行 RL 训练导致 GEdit 整体分数从 6.28 降至 6.13，这表明技能重叠有限的任务会带来负迁移。与之形成鲜明对比的是，Edit 与 GenEval 联合训练产生了正向协同效应：GenEval 分数从单独 Edit 训练的 0.94 提升至 0.95，GEdit Overall 从 7.01 跃升至 7.19。这一结果证实，指令跟随能力作为编辑和生成的共享技能，能够在多任务训练中实现有效的知识迁移。

**课程顺序的决定性影响。** 将课程顺序从 Edit → GenEval → IC 改为 Edit → IC → GenEval 后，GEdit Overall 从 7.21 骤降至 7.06。这验证了论文的核心主张：编辑优先的渐进式课程能够为后续任务建立更稳固的指令对齐基础，而打乱顺序会破坏任务间的正向迁移路径。Table 10 进一步在 OOD 基准上验证了这一点——编辑优先课程在 OneIG Align 上取得 0.8289，优于 T2I 优先顺序的 0.8242。

**奖励信号的脆弱性。** 引入美学奖励 HPSv3 后，SC（语义一致性）和 IC（上下文生成）分数出现崩溃，呈现出典型的“奖励黑客”现象——模型学会了生成美学上讨喜但与指令不符的图像。这警示了在 RL 对齐中谨慎选取奖励函数的重要性。

### Omni-RoPE 位置编码的验证

Omni-RoPE 的设计通过一个玩具级重建任务得到了直接验证（Table 1，Figure 9）。在该任务中，模型需要从随机采样的多张图像中重建指定的第 k 张图像，这要求位置编码同时具备实例区分和空间一致性能力。Omni-RoPE 仅需约 800 步即达到目标损失（<0.014），远快于 Lumina-Image-2.0 方案的约 1200 步和 Qwen2-VL 方案的约 2500 步。最终损失方面，Omni-RoPE 达到 0.003，而对比方案最低为 0.017。Figure 9 的完整损失曲线显示，Omni-RoPE 在早期阶段即展现出更快的下降速度，且后期优化中通过加入图像索引嵌入获得了最低且最稳定的最终损失。这一结果直接支撑了三维位置标识符 $(\Delta_I^{(k)}, h, w)$ 设计的有效性——实例 ID 与局部空间坐标的解耦是实现高效多图像建模的关键。

### 失败模式与局限性

尽管整体性能优异，OmniGen2 仍存在若干系统性局限（Figure 8）：

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/012_Figure_8.jpg]]
*Figure 8: Visualization of OmniGen2’s Limitations. Line 1: The model performs poorly when processing Chinese prompts and lowquality images. Line 2: The model often struggles to modify human body shapes accurately. Line 3: The model is sensitive to ambiguous instructions involving multiple image sources*

- **中文提示退化**：模型在处理中文提示时生成质量显著低于英文，这与其 VLM 基座（Qwen2.5-VL-3B）的预训练数据分布有关，需要手动验证是否可通过多语言 SFT 数据增强改善。
- **低质量输入敏感**：当输入图像存在噪声或分辨率过低时，模型的指令跟随能力急剧下降，表明 VLM 编码器对图像质量具有较高的依赖性。
- **人体形状编辑失真**：在修改人体体型、姿态等任务中，模型常产生不自然的扭曲或比例失调，这反映了扩散解码器在细粒度几何变换上的能力边界。
- **歧义指令脆弱性**：当指令涉及多个图像源且存在歧义时，模型容易混淆来源或产生错误的绑定关系。
- **过度反思**：在带反思的生成流程中（Figure 14），模型偶尔会将正确结果误判为不符合要求，导致不必要的迭代修正。

这些失败模式指向了当前模型规模（VLM 3B + 扩散解码器 4B）可能带来的能力上限，以及数据多样性和奖励设计方面的改进空间。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 2 | OmniGen2 在 GenEval（0.95）和 OneIG-Bench（0.47）上全面领先对比模型 |
| Table 3 | 编辑任务上超越 Gemini-2.5-Flash-Image（GEdit 7.21 vs 7.10） |
| Table 4 | OmniContext 整体平均分 7.95，验证上下文生成泛化能力 |
| Table 5 | Edit & GenEval 联合训练产生正向协同；HPSv3 奖励导致分数崩溃 |
| Table 1 + Figure 9 | Omni-RoPE 收敛速度约 3 倍于先前方案，最终损失低一个数量级 |
| Figure 8 | 中文提示、低质量输入、人体编辑和歧义指令构成主要失败模式 |

### 补充图表

![[assets/figures/papers/paper_list_l2331_https_arxiv_org_abs_2506_18871/figures/023_Table_10.jpg]]
*Table 10: RL curriculum ablation on out-of-distribution (OOD) benchmarks. Base denotes the model without RL*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

OmniGen2 的提出根植于统一多模态生成模型从“专精”走向“通用”的演进脉络，其设计选择与一系列近期工作构成明确的对比和继承关系。

**与统一多模态生成模型的对比。** 在 OmniGen2 之前，**BAGEL** 和 **UniWorld-V1** 等模型已尝试用单一 Transformer 同时处理文本和图像生成任务。这类统一架构虽然简洁，但文本和图像生成对序列建模的需求本质不同：文本生成依赖因果注意力，图像生成则需双向上下文。OmniGen2 直接回应了这一瓶颈——它采用解耦的自回归文本 Transformer 和扩散图像 Transformer，仅通过 VLM 的隐藏状态进行桥接。这一设计的因果逻辑在于：解耦路径允许各自模块保留最优的建模归纳偏置，同时避免模态间的干扰。实验证据间接支持了这一判断：在 GenEval 上，OmniGen2 的总体得分（0.95）显著优于 BAGEL（0.88），在 OneIG-Bench 上差距更大（0.47 vs. 0.36），表明解耦架构在复杂多任务场景下的泛化优势。

**与专精模型的对比。** 在文本到图像生成领域，**FLUX.1-dev** 和 **Qwen-Image** 代表了专精模型的性能上限。OmniGen2 在 GenEval 上以 0.95 的总分超越了这些专精模型，说明统一架构未必以牺牲单任务性能为代价。在编辑任务上，OmniGen2 在 GEdit-Bench-EN 上取得 7.21 的总体分，略优于闭源模型 **Gemini-2.5-Flash-Image**（7.10），在 Emu-Edit 的 CLIP-Out 指标上也以 0.311 超过 BAGEL（0.307）。这些结果表明，经过精心设计的指令对齐，统一模型可以在保持编辑精度的同时兼具更强的文本跟随能力。

**位置编码方案的谱系定位。** Omni-RoPE 的提出直接针对现有多模态位置编码的不足。标准 RoPE 无法区分来自不同图像的 token，而 **Lumina-Image-2.0** 和 **Qwen2-VL** 采用的累积坐标偏移方案虽能区分实例，却破坏了空间一致性。Omni-RoPE 将位置标识符分解为三维元组 $(\Delta_I^{(k)}, h, w)$——实例身份和局部空间坐标显式分离。这一设计的有效性在 toy 重建任务中得到了定量验证：Omni-RoPE 仅需约 800 步即收敛至损失低于 0.014，而先前方案需要 1200 至 2500 步；最终损失也显著更低（0.003 vs. 0.017）。

**对齐训练策略的方法论贡献。** OmniGen2 的三阶段渐进式多任务 RL 课程（Edit → T2I → IC）是该方法最关键的因果杠杆之一。与单任务 RL 微调或无 RL 对齐的基线不同，这一课程设计基于一个核心洞察：任务间的技能重叠决定迁移的方向和强度。消融实验（Table 5）揭示了这一机制的具体表现——仅进行 OCR 训练导致 GEdit 整体分从 6.28 降至 6.13（负迁移），而 Edit & GenEval 联合训练产生了正向协同（GenEval 0.95 vs. 0.94 仅编辑，GEdit 7.19 vs. 7.01 仅编辑）。课程顺序同样至关重要：将课程改为 Edit & IC & GenEval 导致 GEdit 整体分从 7.21 降至 7.06。

### 2. 适用边界与局限

OmniGen2 的能力边界在论文中得到了较为诚实的呈现，以下局限均来自原文明确指出的失败模式：

**语言与输入质量敏感。** 模型处理中文提示时性能显著下降，生成质量逊于英文提示。对低质量输入图像（噪声或低分辨率）同样敏感，会导致指令跟随能力大幅降低。这一局限的根源可能在于训练数据的语言分布和图像质量分布偏差，但论文未提供消融证据来定量分离这两个因素。

**人体形状编辑的准确性不足。** 在修改人体形状（如体型、姿态）时，模型常出现失真，难以精确遵循指令。这暗示当前架构在细粒度空间推理上仍存在短板，可能与扩散解码器的分辨率上限或 VLM 隐藏状态中空间信息的压缩损失有关，但论文未对此进行深入诊断。

**多图像歧义指令的脆弱性。** 当指令涉及多个图像源且存在歧义时，模型可能产生错误的生成结果。这是上下文生成任务固有的挑战，Omni-RoPE 虽能区分实例身份，但在语义层面解析“哪个对象来自哪张图”的推理链路仍可能断裂。

**反思机制的过度校正。** 模型在反思过程中偶有“过度反思”现象，错误地将正确结果判定为不符合要求。这表明当前的反思触发机制缺乏可靠的置信度校准。

**模型规模的限制。** 当前 OmniGen2 的规模（VLM 3B + 扩散解码器 4B）相对较小，论文明确指出这可能限制了上下文生成任务中的一致性和保真度。这是否构成根本性瓶颈，抑或可以通过缩放定律缓解，仍是一个开放问题。

### 3. 开放问题

从 OmniGen2 的方法设计和局限性出发，以下问题值得后续工作关注：

**缩放效应的系统研究。** 扩展 VLM 和扩散解码器的参数量能否线性提升上下文生成和编辑的保真度？特别是，更大规模的 VLM 是否能提供更丰富的隐藏状态表示，从而缓解人体形状编辑等细粒度空间推理任务的失真问题？

**多语言指令对齐的泛化路径。** 中文等多语言提示下的性能下降是数据问题还是架构问题？若通过多语言数据增强即可解决，则成本可控；若涉及 VLM 基础能力的语言偏差，则可能需要从预训练阶段介入。

**反思与强化学习的深度融合。** 当前的反思机制是外挂式的，能否将其内化为 RL 对齐框架的一部分？例如，将反思信号设计为额外的奖励项，或训练模型学习“何时该反思”的元认知能力，从而避免过度反思。

**多任务课程设计的泛化性。** Edit → T2I → IC 的课程顺序在图像生成领域被证明有效，但其背后的“从局部编辑到全局生成再到上下文推理”的递进逻辑能否泛化到视频生成、3D 生成等其他多模态任务？这需要跨领域的实验验证。

**奖励黑客的系统性防御。** 消融实验中，加入美学奖励 HPSv3 导致 SC 与 IC 分数崩溃，这是一个典型的奖励黑客案例。如何设计更鲁棒的多目标对齐框架，在多个奖励信号之间建立安全的平衡机制，而非简单地加权求和，是多任务 RL 对齐的核心挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/OmniGen2_Towards_Instruction_Aligned_Multimodal_Generation.pdf]]

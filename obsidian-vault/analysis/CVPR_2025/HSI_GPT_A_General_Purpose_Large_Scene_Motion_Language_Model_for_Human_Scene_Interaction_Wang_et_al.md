---
title: "HSI-GPT: A General-Purpose Large Scene-Motion-Language Model for Human Scene Interaction"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Scene_Interaction_Wang_et_al.pdf
project_link: null
code_link: null
aliases:
- HG
- HSI-GPT
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入 LLM 的 ‘next-token prediction’ 范式，通过多模态 tokenization、扩展运动词汇表以及多模态交互聚合器 MIA，将场景、运动、语言统一到 LLM 特征空间，并利用指令微调实现多任务 HSI 处理。
primary_logic: 将人类运动视为‘身体语言’并与自然语言统一为多模态词汇表，利用 MIA 提取交互感知的场景 token，从而使 LLM 能够同时理解场景上下文、文本指令并生成符合物理约束的交互运动，成为首个通用 HSI 模型。
claims:
- HSI-GPT 在 HumanML3D 上取得最低的 MultiModal Dist (3.058)，优于 T2M-GPT (3.118) 等专用模型
- 在 Novel Evaluation Set 上，HSI-GPT 的 FID (6.452) 显著低于 Afford-Motion (7.887)，表明生成质量更高
- HSI-GPT 在 HSI captioning 任务上取得最佳 R-Precision Top1 (0.551)，验证了文本-运动理解能力
- HumanML3D (test set) 上 MultiModal Distance (MM Dist) = 3.058
---

# HSI-GPT: A General-Purpose Large Scene-Motion-Language Model for Human Scene Interaction

> [!tip] 核心洞察
> 将人类运动视为‘身体语言’并与自然语言统一为多模态词汇表，利用 MIA 提取交互感知的场景 token，从而使 LLM 能够同时理解场景上下文、文本指令并生成符合物理约束的交互运动，成为首个通用 HSI 模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | HSI-GPT：面向人-场景交互的通用大型场景-运动-语言模型 |
| 英文题名 | HSI-GPT: A General-Purpose Large Scene-Motion-Language Model for Human Scene Interaction |
| 会议/期刊 | CVPR 2025 |
| Links |  [paper](https://doi.org/10.1145/3721238.3730611)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | HSI-GPT |
| Dataset | HumanML3D, Novel Evaluation Set, HumanML3D augmented |

> [!tip] 效果简介
> - HumanML3D (test set) 上，MultiModal Distance (MM Dist) 3.058 vs 3.118 (T2M-GPT) (-0.060)。
> - Novel Evaluation Set (HumanML3D augmented) 上，FID 6.452 vs 7.887 (Afford-Motion @Enc with affordance) (-1.435)。
> - HumanML3D augmented (HSI Captioning) 上，R-Precision Top1 0.551 vs 0.506 (MotionGPT*) (+0.045)。

## 概要

**问题瓶颈**：现有的人-场景交互（HSI）方法普遍受限于单一或有限的控制模态（如纯文本或文本加姿态），且采用任务特定的框架设计，缺乏跨任务泛化能力。更重要的是，这些方法未能有效对齐场景、运动、语言三模态，导致生成的运动在物理上不可信且与文本描述脱节。

**核心洞察**：HSI-GPT 将人类运动视为一种“身体语言”，与自然语言统一为多模态词汇表，并引入 LLM 的 “next-token prediction” 范式。通过多模态交互聚合器（MIA）提取交互感知的场景 token，使 LLM 能够同时理解场景上下文、文本指令并生成符合物理约束的交互运动，成为首个通用 HSI 模型。

**方法定位**：HSI-GPT 采用三阶段训练管线——多模态 Tokenization、多模态预训练对齐、指令微调——将场景、运动和语言统一到 LLM 特征空间。其关键设计包括：基于 VQ-VAE 的运动离散 tokenization、扩展的 LLM 运动词汇表、以及 MIA 模块对场景与 affordance 的融合。模型仅微调约 1% 的 LLM 参数（通过 LoRA），即可实现多任务 HSI 处理。

**主要结果**：
- 在 HumanML3D 文本驱动运动生成上，HSI-GPT 取得最低 MultiModal Distance（3.058），优于专用模型 **T2M-GPT**（Zhang et al., CVPR 2023）的 3.118（Table 1）。
- 在 Novel Evaluation Set 上，FID 达到 6.452，显著低于 **Afford-Motion**（Wang et al., CVPR 2024）的 7.887（Table 3）。
- 在 HSI captioning 任务上，R-Precision Top1 达到 0.551，验证了其文本-运动理解能力（Table 6）。
- 在 HSI completion 任务上，FID 为 0.572，优于 MDM 的 0.787（Table 7）。

**公平性说明**：HSI-GPT 作为通用多任务模型，与各任务专用专家模型（如 cVAE、Afford-Motion）对比时，其优势在于跨任务泛化而非单一任务的极致性能。部分 LLM-based 基线（如 MotionGPT）为复现结果，可能存在实现差异。



### 问题背景：人-场景交互的生成与理解

人类在三维场景中的运动生成与理解是计算机视觉和具身智能的核心问题之一。人-场景交互（Human-Scene Interaction, HSI）要求模型不仅理解文本指令的语义，还需感知三维环境的几何与可供性约束，生成物理可信且语义一致的人体运动序列。这一任务横跨场景理解、运动生成和语言理解三个模态，天然具有高维度和强耦合特性。

### 现有方法的瓶颈

当前 HSI 研究存在三个结构性缺口，制约了模型的实际应用能力：

**第一，控制模态单一，任务框架碎片化。** 现有方法大多为特定任务定制架构：例如 **cVAE**（Wang et al., NeurIPS 2022）针对文本条件下的 HSI 生成，**Afford-Motion**（Wang et al., CVPR 2024）面向场景可供性引导的运动生成，而 **T2M-GPT**（Zhang et al., CVPR 2023）和 **MotionGPT**（Jiang et al., NeurIPS 2023）则聚焦于纯文本到运动的生成。这些模型各自处理一种或有限的控制信号（纯文本、文本+姿态），缺乏统一的框架来同时接纳场景、文本、关键姿态等多种控制模态，更无法在多个 HSI 相关任务间实现知识迁移。

**第二，场景-运动-语言三模态对齐不充分。** 现有方法通常将场景特征单独编码后直接拼接到运动生成器中，缺乏对场景与运动之间交互关系的显式建模。这导致生成的运动在物理接触（contact）和碰撞避免（non-collision）方面表现不佳，且与文本描述的语义关联度低——模型难以理解“坐在沙发上”和“走向桌子”这类空间指代性指令背后的场景可供性逻辑。

**第三，缺乏通用 HSI 基础模型。** 与自然语言处理和视觉领域已出现通用大模型不同，HSI 领域尚无一个能够同时处理运动生成、运动描述（captioning）、运动补全（completion）等多任务的统一模型。这限制了 HSI 技术从实验室走向真实场景应用的泛化能力。

### 核心动机：将 LLM 的“下一 token 预测”范式引入 HSI

大语言模型（LLM）通过将多样化任务统一为“下一 token 预测”范式，展现了强大的跨任务泛化能力。本文的核心动机在于：**能否将这一范式迁移到 HSI 领域，构建一个通用的人-场景交互模型？**

实现这一目标需要解决两个关键技术挑战：

1. **多模态 tokenization**：将连续的人体运动序列和三维场景信息转化为 LLM 可处理的离散 token，同时保持语义丰富性和物理约束。
2. **场景-语言交互建模**：设计一种机制，使 LLM 能够感知三维场景中的交互可供性——即场景中哪些区域可以与人体产生有意义的接触——而非仅仅将场景作为背景条件。

HSI-GPT 正是围绕这两个挑战展开：通过将人类运动视为一种“身体语言”（body language），与自然语言统一为多模态词汇表，并引入多模态交互聚合器（MIA）提取交互感知的场景 token，使 LLM 首次能够同时理解场景上下文、文本指令，并生成符合物理约束的交互运动。这一设计使 HSI-GPT 成为首个面向 HSI 的通用型大模型，为后续研究提供了统一的基线框架。



## 核心方法与创新机理

HSI-GPT 的核心创新在于将大语言模型的“next-token prediction”范式系统性地迁移到人-场景交互（HSI）领域，通过三个关键层面的设计突破，实现了从任务特定框架向通用多任务模型的跨越。

### 1. 运动-语言统一词汇表：将运动视为“身体语言”

现有方法通常将人体运动建模为连续隐变量（如 VAE 或扩散模型的隐空间），与自然语言处于完全不同的表征空间，导致跨模态对齐困难。HSI-GPT 的关键洞察在于**将人体运动视为一种“身体语言”**，并通过 VQ-VAE 将其离散化为语义丰富的 token 序列，直接纳入 LLM 的词汇表（Sec. 3.1, Eq. 1）：

$$ \mathbf{z}_m = \arg \min_{b_k \in \mathcal{B}} \| \mathcal{E}_m(\mathbf{m}) - b_k \|_2 $$

具体而言，运动 VQ-VAE 包含编码器 $\mathcal{E}_m$、解码器 $\mathcal{D}_m$ 和码本 $\mathcal{B}_m = \{b_1, b_2, ..., b_N\}$，将连续 SMPL-X 运动序列压缩为离散 token 索引。训练采用标准 VQ-VAE 损失（Eq. 2），包含重建损失、嵌入损失和承诺损失。随后，LLM 的文本嵌入层被扩展以容纳运动词汇，新增参数随机初始化，并通过特殊 token `<motion>` 和 `</motion>` 标记运动序列边界（Sec. 3.2）。

这一设计使得 LLM 能够以统一的 token 序列形式同时处理文本指令和运动数据，为后续的多模态理解和生成奠定基础。

### 2. 多模态交互聚合器（MIA）：场景感知的 token 压缩

传统方法通常将场景特征单独编码后直接拼接或作为条件注入生成器，缺乏对“交互”本身的显式建模。HSI-GPT 提出了**多模态交互聚合器（MIA）**，采用类似 Q-Former 的架构，通过一组可学习的 query token $Q \in \mathbb{R}^{N_q \times d_q}$ 从场景和 affordance 特征中提取交互感知的固定长度视觉 token（Sec. 3.2）。

具体流程为：预训练的场景编码器从 RGB 点云中提取场景特征 $F_s$，预训练的 affordance 编码器计算每帧骨架关节点到场景点的 $l_2$ 距离场 $d \in \mathbb{R}^{N_s \times J_m}$ 并编码为 $F_a$；MIA 以 $Q$ 为 query，$F_s$ 和 $F_a$ 为 key/value，通过交叉注意力聚合出紧凑的交互感知 token，再经线性投影映射到 LLM 的嵌入空间。

这一设计的因果作用在于：将高维、变长的场景信息压缩为固定长度的语义 token，使 LLM 能够高效地联合建模场景上下文与文本指令，而非将场景视为孤立的外部条件。

### 3. 统一指令模板与多任务微调：从专用到通用的范式转变

现有 HSI 方法（如 cVAE（Wang et al., NeurIPS 2022）、Afford-Motion（Wang et al., CVPR 2024））均为任务特定架构，分别针对文本条件生成、场景 affordance 引导生成等单一任务设计。HSI-GPT 通过**统一指令模板**将多种控制模态（3D 场景、文本指令、关键帧姿态、affordance 图）和多种任务（生成、描述、补全）整合为同一格式的 prompt（Sec. 3.3），并在多任务混合数据上进行指令微调。

训练采用 LoRA 高效微调，仅更新约 1% 的 LLM 参数，目标为最大化运动 token 在所有模态条件下的对数似然（Eq. 3）：

$$ \mathcal{L}_{\mathrm{LoRA}} = - \sum \log p_{\theta} \left( x_t \mid x_{<t}, \mathcal{T}, \mathcal{S}, \mathcal{P}, \mathcal{A} \right) $$

在推理时，同一个模型无需额外任务特定微调即可处理文本到运动生成、HSI 描述（captioning）、运动补全（completion）等多种任务，实现了从“一个任务一个模型”到“一个模型多个任务”的范式转变。这一设计的关键突破在于：多任务联合训练促进了跨任务知识迁移，使模型在单一任务上的表现不逊于专用模型，同时获得了专用模型不具备的零样本泛化能力。



HSI-GPT 提出了一种将人-场景交互（HSI）统一到大型语言模型（LLM）“next-token prediction”范式下的通用框架。其核心设计理念是将人类运动视为一种“身体语言”，与自然语言统一为多模态词汇表，从而使 LLM 能够同时理解场景上下文、文本指令，并生成符合物理约束的交互运动。

### 总体架构

如图 2 所示，HSI-GPT 的整体框架由两大核心组件构成：**多模态分词器（Multi-modal Tokenizer）** 和 **大型场景-运动-语言模型（Large Scene-Motion-Language Model）**。

**多模态分词器**负责将三种异构模态——3D 场景、人类运动和自然语言——分别编码为统一的 token 表示：
- **运动分词**：通过 VQ-VAE 将连续的 SMPL-X 运动序列量化为离散 token 索引，并扩展 LLM 的文本嵌入层以容纳运动词汇表。
- **场景编码**：利用预训练的 3D 场景编码器提取 RGB 点云的视觉特征 $\mathbf{F}_s$，同时通过预训练的 affordance 编码器计算每帧距离场 $\mathbf{d} \in \mathbb{R}^{N_s \times J_m}$ 并编码为 affordance 特征 $\mathbf{F}_a$。
- **多模态交互聚合器（MIA）**：作为连接场景与语言模态的关键桥梁，MIA 使用一组固定长度的可学习查询 token $\mathbf{Q} \in \mathbb{R}^{N_q \times d_q}$，以类似 Q-Former 的方式从 $\mathbf{F}_s$ 和 $\mathbf{F}_a$ 中提取交互感知的 3D 场景特征，并将其映射到 LLM 的特征空间。

**大型场景-运动-语言模型**以预训练 LLM（如 LLaMA 3-8B）为骨干，接收统一指令模板中组织好的多模态 token 序列。指令模板灵活支持多种控制信号组合：3D 场景、文本命令、关键帧姿态和 affordance 地图。模型以自回归方式逐 token 预测，生成运动 token 序列或文本回答。特殊 token `<motion>` 和 `</motion>` 用于标记运动序列的起止边界。

### 训练流程

HSI-GPT 采用三阶段训练策略：

1. **多模态分词**：独立训练运动 VQ-VAE，通过组合重建损失 $\mathcal{L}_{\mathrm{re}}$、嵌入损失 $\mathcal{L}_{\mathrm{emb}}$ 和承诺损失 $\mathcal{L}_{\mathrm{com}}$ 学习语义丰富的离散运动表示：
   $$\mathcal{L}_{\mathrm{VQVAE}} = \| \mathcal{D}(\mathcal{E}(\mathbf{m})) - \mathbf{m} \|^2 + \| \operatorname{sg}[\mathcal{E}(\mathbf{m})] - \mathbf{e} \|_2^2 + \beta \| \mathcal{E}(\mathbf{m}) - \operatorname{sg}[\mathbf{e}] \|_2^2$$

2. **多模态预训练对齐**：在冻结场景和 affordance 编码器权重的前提下，训练 MIA 模块以对齐场景特征与 LLM 的语义空间。

3. **指令微调**：使用 LoRA 高效微调 LLM（仅更新约 1% 的参数），同时更新 MIA 权重。训练目标为最大化运动 token 在所有模态条件下的对数似然：
   $$\mathcal{L}_{\mathrm{LoRA}} = - \sum \log p_{\theta} \left( x_t \mid x_{<t}, \mathcal{T}, \mathcal{S}, \mathcal{P}, \mathcal{A} \right)$$
   其中 $\mathcal{T}$ 为文本指令，$\mathcal{S}$ 为 3D 场景，$\mathcal{P}$ 为姿态条件，$\mathcal{A}$ 为 affordance 信息。

该统一框架使 HSI-GPT 成为首个能够处理多种 HSI 相关任务（文本/场景驱动运动生成、HSI captioning、运动补全等）的通用模型，无需针对特定任务设计独立架构。

### 补充图表

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/003_Figure_2.jpg]]
*Figure 2: TheoveralframeworkofourgenealitHS-GPinHSI-relatedtasks.Itisompoedofmulti-modaltokenizer(Sec.3.anda LargeScene-Motion-Language Model(Sec.3.2).Withanerichedmotion-languagevocabuaryandaMulti-odalInteractionAgregator (MIA) module,HSI-GPT seamlessly aligns scene,motion,and language modalities utilizing fine-tuned LLMs*

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/002_Figure_1.jpg]]
*Figure 1: IlustratioofrH-T'ssupportedtass.Giverentistructioprompts,theproposedH-Ttolycodates multiplecontrolconditiosbthandlesvarousHS-elatedtassasellasotio-centricunderstandingandgeneratiotassuforly*



### 运动离散化：VQ-VAE 运动分词器

HSI-GPT 将连续的人体运动序列转化为离散 token，使其能够被 LLM 直接处理。具体而言，给定一个 SMPL-X 运动序列 $\mathbf{m}$，运动编码器 $\mathcal{E}_m$ 将其映射为连续隐变量，随后通过向量量化在码本 $\mathcal{B}_m = \{b_1, b_2, \dots, b_N\}$ 中查找最近邻离散向量：

$$
\mathbf{z}_m = \arg \min_{b_k \in \mathcal{B}} \| \mathcal{E}_m(\mathbf{m}) - b_k \|_2
$$

其中 $\mathbf{z}_m$ 即为运动 token 的索引序列，$N$ 为码本大小。解码器 $\mathcal{D}_m$ 则负责从离散 token 重建原始运动。

训练该 VQ-VAE 的总损失由三项构成：

$$
\mathcal{L}_{\mathrm{VQVAE}} = \mathcal{L}_{\mathrm{re}} + \mathcal{L}_{\mathrm{emb}} + \mathcal{L}_{\mathrm{com}} = \| \mathcal{D}(\mathcal{E}(\mathbf{m})) - \mathbf{m} \|^2 + \| \operatorname{sg}[\mathcal{E}(\mathbf{m})] - \mathbf{e} \|_2^2 + \beta \| \mathcal{E}(\mathbf{m}) - \operatorname{sg}[\mathbf{e}] \|_2^2
$$

- **$\mathcal{L}_{\mathrm{re}}$**：重建损失，确保解码运动与原始运动一致。
- **$\mathcal{L}_{\mathrm{emb}}$**：嵌入损失，约束码本向量 $\mathbf{e}$ 向编码器输出靠拢（$\operatorname{sg}$ 为 stop-gradient 操作）。
- **$\mathcal{L}_{\mathrm{com}}$**：承诺损失，约束编码器输出向码本向量靠拢，$\beta$ 为权重系数。

通过这一量化过程，连续运动被压缩为语义丰富的离散 token，与自然语言 token 处于同一表征空间，为后续 LLM 统一处理奠定基础。

### 场景表征：Affordance 编码与 MIA 聚合器

场景信息通过两条路径注入模型。首先，预训练的场景编码器从 RGB 点云中提取视觉特征 $\mathbf{F}_s$。其次，通过计算 3D 场景点与人体骨骼关节之间的 $l_2$ 距离，得到逐帧的 affordance 距离场：

$$
d \in \mathbb{R}^{N_s \times J_m}
$$

其中 $N_s$ 为场景点数，$J_m = d_m / 3$ 为骨骼关节数（$d_m$ 为运动维度）。该距离场随后由预训练的 affordance 编码器转化为特征 $\mathbf{F}_a$，显式编码了场景中哪些区域可供人体交互。

为将稠密的场景特征压缩为 LLM 可处理的固定长度 token，HSI-GPT 引入了**多模态交互聚合器（Multi-modal Interaction Aggregator, MIA）**。MIA 采用类似 Q-Former 的架构，使用一组可学习的查询 token $\mathbf{Q} \in \mathbb{R}^{N_q \times d_q}$ 与场景特征 $\mathbf{F}_s$ 和 affordance 特征 $\mathbf{F}_a$ 进行交叉注意力交互，最终输出固定长度的交互感知视觉 token。这些 token 通过线性投影映射到 LLM 的嵌入空间，与文本 token 和运动 token 拼接后送入 LLM 主干。

### 统一序列建模与 LoRA 训练目标

HSI-GPT 将 LLM 的文本嵌入层扩展，新增运动词汇表的嵌入参数（随机初始化），并插入特殊 token `<motion>` 和 `</motion>` 标记运动序列的起止边界。在指令微调阶段，3D 场景编码器和 affordance 编码器的权重被冻结，仅更新 MIA 参数并利用 LoRA 高效微调 LLM 参数（仅约 1% 的参数被更新）。训练目标为最大化运动 token 在给定多模态条件下的对数似然：

$$
\mathcal{L}_{\mathrm{LoRA}} = - \sum \log p_{\theta} \left( x_t \mid x_{<t}, \mathcal{T}, \mathcal{S}, \mathcal{P}, \mathcal{A} \right)
$$

- **$x_t$**：第 $t$ 个运动 token。
- **$x_{<t}$**：前序 token 序列。
- **$\mathcal{T}$**：文本指令。
- **$\mathcal{S}$**：3D 场景信息。
- **$\mathcal{P}$**：关键姿态（可选控制信号）。
- **$\mathcal{A}$**：affordance 信息。

该目标驱动 LLM 以自回归方式预测下一个运动 token，实现了场景、运动、语言三模态在统一序列空间中的联合建模。



## 实验与关键发现

### 核心实验设计

HSI-GPT 的实验设计围绕一个核心目标展开：验证一个**统一的多任务框架**能否在多个 HSI 相关任务上达到甚至超越**专门设计的专家模型**的性能。为此，论文在三个维度上构建了评估体系：

1. **任务覆盖度**：涵盖文本驱动运动生成、文本条件 HSI 生成、HSI 描述生成（captioning）、HSI 运动补全（completion）四类任务。
2. **控制模态多样性**：从纯文本到文本+场景、文本+affordance、文本+关键姿态等多模态组合。
3. **基准对比公平性**：明确标注了复现结果（† 标记）、95% 置信区间，并区分了 LLM-based 方法和传统方法。

训练策略上，HSI-GPT 采用三阶段流水线：多模态 tokenization → 多模态预训练对齐 → 统一指令微调。在指令微调阶段，冻结 3D 场景编码器和 affordance 编码器的权重，仅更新 MIA 模块参数和 LLM 的 LoRA 适配器（约 1% 参数），训练目标为最大化运动 token 在所有模态条件下的对数似然：

$$ \mathcal{L}_{\mathrm{LoRA}} = - \sum \log p_{\theta} \left( x_{t} \mid x_{<t}, \mathcal{T}, \mathcal{S}, \mathcal{P}, \mathcal{A} \right) $$

### 主实验结果

#### 文本驱动运动生成（HumanML3D）

Table 1 展示了在 HumanML3D 测试集上的定量对比。HSI-GPT 在多项指标上达到最优或接近最优：

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/004_Table_1.jpg]]
*Table 1: QuanitativeresultsontheHumanMLDtestetdenotethext-based motiongenerationmethodbasedonLLM.represents 95%confidenceintervalfollowing[9].→indicates thatmetricsimproveas teygetcloserto“RealBoldfaceindicatesthebestresult*

| 指标 | HSI-GPT | T2M-GPT | MotionGPT | Real |
|------|---------|---------|-----------|------|
| R-Precision Top1 ↑ | **0.495** | 0.491 | 0.487 | 0.511 |
| FID ↓ | 0.187 | **0.116** | 0.232 | 0.002 |
| MultiModal Dist ↓ | **3.058** | 3.118 | 3.214 | 2.974 |
| Diversity → | 9.845 | 9.761 | 9.559 | 9.503 |

**关键发现**：HSI-GPT 在 MultiModal Dist（3.058）上超越了专用模型 **T2M-GPT**（Zhang et al., CVPR 2023）的 3.118，表明其生成的 motion-text 对齐度更高。但在 FID 上（0.187）不如 T2M-GPT（0.116），论文将此归因于通用模型与专用模型之间的固有 trade-off。值得注意的是，HSI-GPT 仅微调了约 1% 的 LLM 参数即达到此性能。

#### 文本条件 HSI 生成（HUMANISE）

Table 2 报告了在 HUMANISE 数据集上的 HSI 生成结果。该任务要求模型根据文本描述在 3D 场景中生成物理合理的人体运动。

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/007_Table_2.jpg]]
*Table 2: Quantitative performance of text-conditioned HSI generation.† marks our reproduced results on HUMANISE[52] dataset*

**物理合理性指标**：
- HSI-GPT（w/ affordance）在 Contact 指标上达到 85.47，显著优于 cVAE（4.094），表明生成的 motion 与场景的物理接触更真实。
- Non-Collision 达到 93.98，意味着穿模率大幅降低。

**运动质量指标**：
- HSI-GPT 的 Goal Dist（0.181）远低于 **cVAE**（Wang et al., NeurIPS 2022）的 0.422，说明生成的运动终点更准确。
- APD（Average Pairwise Distance）为 3.442，低于 cVAE 的 10.326，表明运动多样性更接近真实分布。

**Affordance 的因果作用**：当移除 affordance 条件时，HSI-GPT 的 Contact 从 85.47 骤降至 48.18，Non-Collision 从 93.98 降至 88.38。这直接验证了 affordance 编码是物理合理性的关键因果旋钮。

#### 泛化评估（Novel Evaluation Set）

Table 3 在包含未见场景的 Novel Evaluation Set 上对比了 HSI-GPT 与 **Afford-Motion**（Wang et al., CVPR 2024）：

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/008_Table_3.jpg]]
*Table 3: QualitativeResultsonNovelEvaluationSet[53].“Realdenotes themetricscomputedwithin thetestsetofHumanMDdataset*

| 指标 | HSI-GPT | Afford-Motion | Real |
|------|---------|---------------|------|
| FID ↓ | **6.452** | 7.887 | 0.002 |
| MultiModal Dist ↓ | **4.108** | 4.138 | 2.974 |
| Contact ↑ | **0.036** | 0.034 | - |

HSI-GPT 在 FID（6.452 vs 7.887）和 Contact 上均优于专门设计的 Afford-Motion，且这一优势在未见场景中得以保持（Figure 5 定性结果佐证）。这证明了 MIA 模块提取的交互感知场景特征具有良好的泛化能力。

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative results on generalization evaluation set [53]. HSI-GPT can generate high-fidelity motions in unseen 3D scenes*

#### HSI Captioning 与 Completion

**Captioning 任务**（Table 6）：HSI-GPT 在 R-Precision Top1 上达到 0.551，优于 MotionGPT 的 0.506，验证了其文本-运动双向理解能力。

**Completion 任务**（Table 7）：给定部分运动序列和场景，HSI-GPT 在预测 FID 上达到 0.572，显著优于 MDM 的 0.787（降低 27.3%），展示了强时序推理能力。

### 消融研究

#### 控制模态组合的影响（Table 4）

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/009_Table_4.jpg]]
*Table 4: Investigation of HSI generation task on the HumanML3D and HUMANISE datasets with various control signal modalities*

Table 4 系统研究了不同控制信号组合对 HSI 生成质量的影响：

- **纯文本**：FID 较高，物理接触最弱。
- **文本 + 初始姿态**：FID 显著降低，Contact 提升。
- **文本 + 初始姿态 + 关键姿态**：在 HumanML3D 上取得最佳 FID，物理合理性进一步提升。
- **文本 + affordance**：Contact 和 Non-Collision 大幅改善，验证了 affordance 对物理约束的直接贡献。

**核心洞察**：多模态控制信号的叠加产生了协同效应——文本提供语义指导，姿态提供时序锚点，affordance 提供物理约束，三者互补而非冗余。

#### LLM Backbone 的影响（Table 5）

对比 LLaMA 3-8B 与 Qwen2-1.5B 作为 backbone：
- LLaMA 3-8B 在 Goal Dist 和 Contact 上均优于 Qwen2-1.5B。
- 更大的 LLM 带来了更强的场景理解和运动规划能力，但代价是计算开销增加。

### 公平性讨论与失败模式

**公平性说明**（论文明确标注）：
1. HSI-GPT 是预训练的多任务通用模型，而 cVAE、Afford-Motion 等基线是针对特定任务训练的专家模型，直接对比存在范畴差异。
2. 在 HumanML3D 的 FID 比较中，HSI-GPT 并非最优，论文强调其通用性价值而非在每个子任务上追求 SOTA。
3. HSI-GPT 仅微调约 1% 的 LLM 参数，基线模型可能训练了全部参数。
4. MotionGPT 等 LLM-based 基线的复现可能存在实现差异（论文用 † 标记）。

**已知局限**：
- 模型未在真实机器人或具身智能体上验证，所有评估限于现有数据集（HUMANISE、HumanML3D）。
- 场景和 affordance 编码器使用固定预训练权重，未端到端联合优化，可能限制对新场景类型的适应能力。
- 仅支持单人交互，未扩展到多人协作或动态物体交互场景。
- 评估指标侧重运动质量和物理合理性，缺乏对交互语义一致性（如是否准确执行了指令中的具体动作）的细粒度评估。

### 图表核心结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 1 | HSI-GPT 在 MultiModal Dist 上超越专用模型 T2M-GPT，验证了 LLM 范式在 motion-text 对齐上的优势 |
| Table 2 | Affordance 条件是物理合理性的关键：移除后 Contact 下降 43.7% |
| Table 3 | 在未见场景中，HSI-GPT 的 FID（6.452）优于专用模型 Afford-Motion（7.887） |
| Table 4 | 多模态控制信号存在协同效应，文本+姿态+affordance 组合最优 |
| Table 6 | HSI-GPT 在 captioning 任务上 R-Precision Top1 达到 0.551，验证双向理解能力 |
| Table 7 | 在 completion 任务上 FID 较 MDM 降低 27.3%，展示强时序推理能力 |

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/010_Table_6.jpg]]
*Table 6: Experiments of HSIcaptioning task ontheaugmented HumanML3D[9]. Results marked with * are from MotionGPT[18]*

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/013_Table_7.jpg]]
*Table 7: Evaluation of generalized HSI completion using our HSI-GPT(LLaMA 3-8B)on the HumanML3D augmented with floors. The underlined results indicate the second-best performance*

### 补充图表

![[assets/figures/papers/paper_list_l1738_HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Sc/figures/006_Figure_4.jpg]]
*Figure 4: GallrtingtultsofetoiodHeatiodrrosotrloiioelyxt+lto Token,Text+LastMotionTken,adTextRandomMotionTokens (yelloposes)ontheHUMANSE[9]benchmark.Bestviewedincolor*



## 定位与知识库关联

### 范式转移：从任务专用架构到通用 LLM 驱动的 HSI

HSI-GPT 的核心贡献在于将人-场景交互（Human Scene Interaction, HSI）从“多任务多模型”的范式推向“单模型多任务”的通用范式。传统 HSI 方法通常为每个子任务设计独立的架构：例如 **cVAE (HUMANISE)**（Wang et al., NeurIPS 2022）专注于文本条件下的 HSI 生成，**Afford-Motion**（Wang et al., CVPR 2024）侧重于场景可供性引导的运动生成，而 **T2M-GPT**（Zhang et al., CVPR 2023）和 **MotionGPT**（Jiang et al., NeurIPS 2023）则仅处理文本到运动的生成，缺乏对 3D 场景上下文的整合。这些方法共享一个根本性局限：控制模态单一、任务特定设计，无法实现跨任务的知识迁移。

HSI-GPT 通过引入 LLM 的“next-token prediction”范式打破了这一瓶颈。其关键洞察在于将人类运动视为“身体语言”，通过 VQ-VAE 将连续运动序列量化为离散 token，并与自然语言词汇表统一，使 LLM 能够同时理解场景上下文、文本指令并生成符合物理约束的交互运动。这一范式转移使得单一模型能够处理文本驱动生成、场景条件生成、运动描述生成（captioning）、运动补全（completion）等多种 HSI 任务。

### 技术谱系中的关键差异点

**运动表征层面**：传统方法（如 cVAE、MDM）使用连续潜变量或扩散模型处理运动，而 HSI-GPT 采用 VQ-VAE 离散 tokenization（Eq. 1-2），将运动映射到可学习的码本中。这一设计使得运动 token 可以直接嵌入 LLM 的词汇表，与文本 token 共享统一的特征空间，是实现多模态统一的基础。

**场景整合层面**：Afford-Motion 等方法将场景特征编码后直接拼接或条件化注入生成器，缺乏对交互语义的显式建模。HSI-GPT 提出的多模态交互聚合器（Multi-modal Interaction Aggregator, MIA）使用可学习的查询 token，以 Q-Former 方式从场景特征和可供性特征中提取固定长度的交互感知 token。这一设计将场景信息压缩为 LLM 可消费的“视觉 token”，而非简单的特征向量拼接。

**控制灵活性**：基线方法通常仅支持单一控制信号（如纯文本或文本+姿态），HSI-GPT 通过统一指令模板支持多种控制模态的组合：3D 场景、文本指令、关键帧姿态、可供性地图。Table 4 的消融实验表明，结合文本和初始/关键姿态的控制方式比纯文本产生更低的 FID 和更好的物理接触，验证了多模态控制的有效性。

**参数效率**：HSI-GPT 仅微调约 1% 的 LLM 参数（通过 LoRA），而多数基线模型需要训练全部参数。这一设计在保持 LLM 预训练知识的同时实现了高效的多模态对齐。

### 适用边界与能力局限

**数据依赖性**：当前模型主要基于 HUMANISE 和 HumanML3D 数据集训练和评估，这些数据集中的场景和交互类型有限。模型在真实具身智能体或机器人场景中的表现尚未验证，泛化到全新场景类型（如户外环境、动态场景）的能力存疑。

**场景编码器的固定性**：场景和可供性编码器使用预训练权重且在指令微调阶段被冻结，这意味着模型对场景的理解受限于编码器的预训练分布。若遇到与训练数据分布差异较大的场景，MIA 提取的交互感知 token 可能无法准确反映交互可能性。

**单人交互限制**：当前模型仅支持单个人与静态场景的交互，未扩展到多人协作或与动态物体的交互。这限制了其在复杂社会交互场景（如两人协作搬运物体）中的应用。

**评估粒度不足**：现有评估指标主要关注运动质量（FID）和物理合理性（接触率、碰撞率），缺乏对交互语义一致性的细粒度评估。例如，模型可能生成物理上合理但未正确执行指令中具体动作的运动。

**部署挑战**：尽管使用了 LoRA 进行参数高效微调，HSI-GPT 仍以 LLaMA 3-8B 为骨干，在资源受限的边缘设备上实时运行面临显著挑战。

### 开放问题与未来方向

1. **动态场景与移动物体交互**：如何将 HSI-GPT 推广到包含动态物体和移动障碍物的场景？这需要模型具备时序场景理解和运动预测能力。

2. **闭环控制与实时反馈**：当前模型以开环方式生成完整运动序列，缺乏根据场景反馈动态调整的能力。引入闭环控制机制，使 Agent 能够根据执行过程中的场景变化实时调整运动，是走向实际部署的关键一步。

3. **常识知识的深度利用**：LLM 蕴含丰富的常识知识（如“坐在椅子上”意味着面向椅背还是椅面），如何更有效地利用这些知识来理解和规划复杂的长期人-场景交互，而非仅依赖训练数据中的统计模式？

4. **模型压缩与边缘部署**：探索知识蒸馏、量化等技术，将 HSI-GPT 压缩至可在边缘设备上实时运行的规模，同时保持多任务泛化能力。

5. **多人协作与社交交互**：扩展模型以支持多人场景，需要处理人物间的空间关系、时序协调和社交规范，这涉及更复杂的交互建模。

6. **细粒度语义评估**：开发能够评估生成运动与指令语义一致性的新指标，例如动作类型准确率、物体交互正确率等，以弥补现有评估体系的不足。



## 原文 PDF

![[paperPDFs/CVPR_2025/HSI_GPT_A_General_Purpose_Large_Scene_Motion_Language_Model_for_Human_Scene_Interaction_Wang_et_al.pdf]]

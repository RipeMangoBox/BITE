---
title: "HMVLM: Human Motion-Vision-Lanuage Model via MoE LoRA"
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA.pdf
project_link: null
code_link: null
aliases:
- HHMVLM
- HMVLM
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 门控网络动态路由的LoRA专家混合（MoE LoRA），其中可训练的非零专家适配特定任务，不可训练的零专家保留基础模型的预训练参数。
primary_logic: 通过门控网络为运动相关任务分配专门的LoRA专家，同时用零专家退回到原始参数路径，可以在多任务适应中大幅降低遗忘；配合基于身体部位的空间标记器，提升单帧姿态与运动序列的表征精度。
claims:
- 在相同基础模型Gemma-2‑2B‑it上，HMVLM仅造成3.34%的MT-Bench平均分下降（7.79→7.53），而MotionAgent下降87.16%（7.79→1.00），证明MoE LoRA有效缓解遗忘。
- 去除L_gat后，Vicuna‑7B‑v1.5的MT-Bench平均分从5.90崩塌至1.00，表明零专家和门控损失是知识保留的关键。
- 身体部位标记器在HumanML3D上将R-precision Top-3从0.741提升至0.785，重建MSE从1.377降至0.966，验证了空间分解的有效性。
- MT-Bench 上 Average score (1-10) after T2M fine-tuning = 7.53 (HMVLM with Gemma‑2‑2b‑it)
---

# HMVLM: Human Motion-Vision-Lanuage Model via MoE LoRA

> [!tip] 核心洞察
> 通过门控网络为运动相关任务分配专门的LoRA专家，同时用零专家退回到原始参数路径，可以在多任务适应中大幅降低遗忘；配合基于身体部位的空间标记器，提升单帧姿态与运动序列的表征精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于MoE LoRA的人体运动-视觉-语言模型 |
| 英文题名 | HMVLM: Human Motion-Vision-Lanuage Model via MoE LoRA |
| 会议/期刊 | NEURIPS 2025 |
| Links |  [paper](https://arxiv.org/abs/2511.01463)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HMVLM (Human Motion-Vision-Language Model) |
| Dataset | MT-Bench, HumanML3D, Human3.6M + 3DPW |

> [!tip] 效果简介
> - MT-Bench 上，Average score (1-10) after T2M fine-tuning 7.53 (HMVLM with Gemma‑2‑2b‑it) vs 7.79 (Gemma‑2‑2b‑it before tuning) (-0.26 (3.34% relative drop))。
> - HumanML3D (text-to-motion) 上，R-precision Top-1 ↑ 0.502 ±.003 (HMVLM single-task) vs 0.496 ±.002 (MotionGPT-2 ) (+0.006)；FID ↓ 0.123 ±.004 (HMVLM single-task) vs 0.191 ±.004 (MotionGPT-2 ) (-0.068)。
> - Human3.6M + 3DPW (human pose estimation) 上，MPJPE ↓ / PA-MPJPE ↓ (average over datasets) outperforms ChatPose (single task) vs ChatPose (qualitative and quantitative improvement)。

## 概要

**问题与瓶颈**：将3D人体运动模态集成到基础语言模型时，模态差距导致灾难性遗忘——模型在获得运动理解能力的同时，原有的对话和知识能力急剧退化。现有的离散化运动表征（如基于全身时序1D卷积的VQ-VAE）缺乏空间粒度，难以同时兼顾自回归生成架构与姿态估计等静态任务的需求。

**核心方法**：HMVLM提出一种基于门控网络动态路由的**LoRA专家混合（MoE LoRA）**策略。其关键设计在于引入一个**不可训练的零专家**，当门控网络为运动无关任务分配高权重给该专家时，模型退回到原始预训练参数路径，从而保留基础模型的语言能力；同时，多个可训练的LoRA专家分别适配不同的下游任务。配合基于身体部位（躯干+四肢，共5个部位）的空间标记器，将单帧姿态按部位独立编码并量化，再沿时间轴压缩，显著提升了运动序列的表征精度。

**主要结果**：
- **知识保留**：在Gemma-2-2B-it上，HMVLM经文本到运动微调后MT-Bench平均分仅下降3.34%（7.79→7.53），而MotionAgent下降87.16%（7.79→1.00），证明MoE LoRA有效缓解遗忘。
- **运动生成**：在HumanML3D上，单任务HMVLM的FID降至0.123，优于MotionGPT-2的0.191；R-precision Top-1达到0.502。
- **姿态估计**：在H3.6M和3DPW上定量和定性均超越专用模型ChatPose。
- **消融验证**：去除门控损失L_gat后，Vicuna-7B-v1.5的MT-Bench平均分从5.90崩塌至1.00，证实零专家和门控损失是知识保留的关键；身体部位标记器将HumanML3D的R-precision Top-3从0.741提升至0.785，重建MSE从1.377降至0.966。

**方法定位**：HMVLM属于**多模态指令微调框架**，在基础语言模型（Vicuna-7B-v1.5 / Gemma-2-2B-it）之上，通过MoE LoRA实现运动、视觉、语言三模态的统一。与MotionGPT、MotionAgent等运动-语言模型相比，其核心差异在于以极低的遗忘代价同时支持文本到运动生成、人体姿态估计和视频理解三类任务，且在多任务联合微调下仍保持竞争力。

将人体运动理解与生成能力融入基础语言模型，是构建通用人本智能体的关键一步。然而，现有方法面临两个相互纠缠的核心瓶颈。

**模态鸿沟与灾难性遗忘。** 3D人体运动作为一种高维时序模态，其统计特性与离散文本存在本质差异。当直接在预训练语言模型上进行运动相关任务的指令微调时，模型往往以牺牲原有语言能力为代价来适应新模态。实验表明，基于GPT‑4协调的**MotionAgent**框架在文本到运动（T2M）微调后，其基础模型Gemma‑2‑2B‑it的MT‑Bench平均分从7.79崩塌至1.00，降幅高达87.16%（Table 1）。这揭示了现有方案的根本缺陷：缺乏一种机制来隔离运动适配与语言知识保留之间的参数冲突。

**运动表征的粒度不足。** 主流方法（如**T2M‑GPT**、**MoMask**）普遍采用基于全身1D时序卷积的VQ‑VAE将运动序列离散化为统一标记。这种“整体式”标记化忽略了人体的自然空间结构——躯干、四肢等不同部位的运动模式在动态范围与语义关联上差异显著。由此产生的离散码本难以同时捕捉局部姿态精度与全局运动语义，制约了自回归生成与单帧姿态估计等静态任务的统一建模。

**本文动机。** 针对上述缺口，HMVLM提出两个相互配合的设计：在参数层面，通过门控网络动态路由的LoRA专家混合（MoE LoRA）实现任务感知的参数调制，其中引入不可训练的“零专家”作为预训练权重的安全回退路径；在表征层面，构建基于身体部位的空间标记器，将人体划分为多个部位并独立量化编码，在保留空间结构的同时提升重建精度。这一双轨设计的目标是：在支持文本到运动生成、人体姿态估计、视频理解等多种人本任务的同时，将基础模型的语言能力损失控制在可忽略的水平。

## 核心方法与创新机理

HMVLM 围绕“将3D人体运动模态集成到基础语言模型时，模态差距导致灾难性遗忘且现有离散化运动表征缺乏空间粒度”这一瓶颈，提出了两个关键创新点：**MoE LoRA 多任务适应架构**与**基于身体部位的空间标记器**。以下从相对于 baseline 的 changed slots 角度展开分析。

### 1. 从标准 LoRA 到 MoE LoRA：动态路由的专家混合

标准 LoRA 微调（如 MotionGPT 采用的方案）对基础模型的所有线性层施加统一的低秩适配器，在多模态指令微调中缺乏对任务差异性的显式建模，导致预训练知识被严重覆盖。HMVLM 将这一 slot 替换为 **MoE LoRA**，其核心变化体现在三个层面：

**（1）专家集合设计。** HMVLM 部署 5 个 LoRA 专家（4 个可训练 + 1 个不可训练的零专家），其中零专家的参数始终为零初始化且不参与梯度更新。调制后的权重矩阵为：

$$W' = W + \sum_{i=0}^{n} \alpha_i A_i B_i$$

当门控网络将零专家的权重 $\alpha_0$ 推向 1 时，上式退化为 $W' = W$，即模型完整保留预训练参数。这一设计使得零专家成为“参数保护区”，而可训练专家 $A_i B_i$（$i=1,\dots,4$）则专注于运动相关任务的适配。

**（2）门控网络与任务感知路由。** 门控网络 $\omega$ 是一个两层 MLP（隐层维度 512），以 CLIP 文本编码器输出的 512 维指令特征为输入，输出混合权重 $\alpha = [\alpha_0, \alpha_1, \dots, \alpha_4]$。门控网络通过学习指令中的任务语义，为文本到运动（T2M）、人体姿态估计（HPE）、人体视频理解（HVU）等任务分配不同的专家组合，而通用对话（GD）任务则被路由至零专家。

**（3）门控损失 $\mathcal{L}_{gat}$ 作为遗忘抑制的因果旋钮。** 仅靠门控网络的自主学习不足以确保零专家在运动无关任务中被激活。HMVLM 引入显式的门控损失：

$$\mathcal{L}_{gat} = -\mathbb{E}[\eta * \log p_w(\alpha_0 | \mathbb{Z}, \mathcal{P})]$$

其中 $\eta$ 为运动无关指示函数（当任务为通用对话时 $\eta=1$，否则 $\eta=0$）。该损失直接鼓励门控网络在通用对话任务上最大化零专家的选择概率。总损失 $\mathcal{L}_{total} = \mathcal{L}_{fm} + \mathcal{L}_{gat}$ 联合优化任务性能与知识保留。

**决定性证据：** Table 1 显示，在相同基础模型 Gemma-2-2B-it 上，HMVLM 微调后 MT-Bench 平均分仅下降 3.34%（7.79→7.53），而 MotionAgent 下降 87.16%（7.79→1.00）。去除 $\mathcal{L}_{gat}$ 后，Vicuna-7B-v1.5 的 MT-Bench 平均分从 5.90 崩塌至 1.00，证实零专家和门控损失是知识保留的因果关键。Table 3 进一步显示，零专家在通用对话任务上的平均权重为 0.999，验证了其作为“参数保护区”的实际行为。

### 2. 从全身时序 VQ-VAE 到身体部位空间标记器

现有方法（如 T2M-GPT、MoMask）采用全身时序 1D 卷积 VQ-VAE 将运动序列压缩为离散 token，其局限在于：① 忽略了人体各部位的运动独立性，导致细粒度空间信息丢失；② 无法兼容姿态估计等单帧静态任务。

HMVLM 将此 slot 替换为**基于身体部位的空间标记器**，由空间编码器 $\mathcal{E}_s$ 和时间压缩器 $\mathcal{E}_t$ 两级组成：

**空间编码阶段：** 将人体划分为 $N$ 个部位（躯干 + 四肢，$N=5$），对单帧姿态 $m^f$ 分别编码：

$$[\hat{z}_{B1}^f, \hat{z}_{B2}^f, \dots, \hat{z}_{BN}^f] = \mathcal{E}_s(m^f)$$

每个部位使用独立的可学习查询参数进行特征池化，并拥有独立的 codebook 进行向量量化（VQ），从而保留部位级别的空间结构。

**时间压缩阶段：** 在获得各部位的空间 token 后，沿时间轴进行压缩：

$$(\hat{z}_{Bn}^{'1}, \hat{z}_{Bn}^{'2}, \dots, \hat{z}_{Bn}^{'F/l}) = \mathcal{E}_t(\hat{z}_{Bn}^1, \dots, \hat{z}_{Bn}^F)$$

其中 $l$ 为时间压缩比。这种“先空间后时间”的设计使得标记器既能输出单帧姿态的离散编码（用于 HPE），也能输出压缩后的运动序列 token（用于 T2M）。

**决定性证据：** Table 5 显示，在 codebook 大小 $K=512$ 的设置下，身体部位标记器将 HumanML3D 上的 R-precision Top-3 从 0.741 提升至 0.785，重建 MSE 从 1.377 降至 0.966，验证了空间分解对表征精度的实质性提升。

### 创新点之间的关系

两个创新点并非孤立：MoE LoRA 解决了“如何在不遗忘的前提下学习多任务”，身体部位标记器解决了“用什么表征来桥接运动与语言”。前者通过门控网络将不同任务的梯度更新隔离到不同的专家子空间，后者为自回归语言模型提供了兼具空间粒度和时间压缩能力的离散 token。二者协同使得 HMVLM 能够在一个统一的框架内同时支持文本到运动生成、人体姿态估计和视频理解，且保持基础模型的对话能力。

**需注意的局限：** 当前框架仅实现运动与文本/视频的独立跨模态配对，尚未探索图像到文本或视频到运动的直接生成。多任务联合微调时，受固定参数预算限制，单任务性能相比单独微调有轻微下降（Table 2 中 multi-task 的 FID 从 0.123 升至 0.156）。此外，扩展到新的运动相关任务需要重新训练门控网络并添加专家，框架的任务可扩展性仍有待验证。

HMVLM 的整体设计围绕一个核心矛盾展开：如何将 3D 人体运动模态注入预训练语言模型，同时不破坏后者已有的语言理解与对话能力。框架采用**指令驱动的多模态统一架构**，其信息流可概括为三个关键阶段。

### 1. 指令感知的门控路由

系统入口接收两类输入：任务指令与文本提示。二者经 CLIP 文本编码器提取语义特征后，送入一个**两层 MLP 门控网络**（隐藏维度 512），该网络输出一组混合权重 $\alpha = [\alpha_0, \alpha_1, \dots, \alpha_n]$，用于动态组合多个 LoRA 专家。门控网络的设计使得模型能够根据输入语义自适应地激活不同的参数子空间——运动相关任务触发可训练的领域专家，而通用对话则导向零专家。

### 2. 模态对齐与嵌入投影

多模态输入（图像、视频帧、运动序列）通过各自的**模态投影层**映射到语言模型的嵌入空间，与文本 token 嵌入在序列维度上拼接。这一设计避免了为每种模态单独改造模型架构，仅需轻量的线性投影即可实现跨模态对齐。投影后的多模态嵌入与指令嵌入共同构成自回归生成的上下文前缀。

### 3. 混合专家调制与自回归生成

基础语言模型（Vicuna-7B-v1.5 或 Gemma-2-2B-it）的所有线性层均被注入 LoRA 适配器（秩为 8）。前向传播时，每个线性层的权重矩阵按以下方式调制：

$$W' = W + \sum_{i=0}^{n} \alpha_i A_i B_i$$

其中 $W$ 为预训练权重，$A_i B_i$ 为第 $i$ 个专家的低秩增量，$\alpha_i$ 为门控权重。**零专家**（$i=0$）的参数被初始化为零且不参与训练，当 $\alpha_0 \to 1$ 时，$W' \approx W$，模型退化为原始基础模型，从而在机制层面保留预训练知识。

### 4. 运动模态的专用标记化

对于人体姿态和运动序列，HMVLM 采用独立的**身体部位标记器**进行离散化。该标记器先将单帧姿态按身体部位（躯干与四肢等 5 个部位）分区，通过空间 Transformer 编码器提取各部位潜在特征并独立量化，再沿时间轴压缩。量化后的离散 token 被扩充到基础模型的词表中，使语言模型能以自回归方式生成运动 token 序列。这一空间分解策略使得同一框架既能处理单帧姿态估计任务，也能处理时序运动生成任务。

### 5. 训练目标

整体训练损失由两部分组成：

$$\mathcal{L}_{total} = \mathcal{L}_{fm} + \mathcal{L}_{gat}$$

- $\mathcal{L}_{fm}$ 为标准的下一 token 预测损失，驱动模型生成正确的响应序列。
- $\mathcal{L}_{gat}$ 为门控损失，鼓励模型在处理运动无关任务时选择零专家：

$$\mathcal{L}_{gat} = -\mathbb{E}[\eta \cdot \log p_w(\alpha_0 | \mathbb{Z}, \mathcal{P})]$$

其中 $\eta$ 为指示函数，当任务为通用对话时取 1，否则为 0。该损失是防止灾难性遗忘的关键机制——消融实验表明，去除 $\mathcal{L}_{gat}$ 后 Vicuna-7B-v1.5 的 MT-Bench 平均分从 5.90 崩塌至 1.00。

### 模块依赖关系

上述模块形成一条清晰的数据流：**CLIP 编码器 → 门控网络 → 专家权重分配** 与 **模态投影 → 嵌入拼接** 两条支路在基础语言模型的每层线性变换处汇合，经混合专家调制后完成自回归解码。身体部位标记器则作为独立的运动模态前端，将连续运动数据转化为离散 token 后接入同一生成管道。

![[assets/figures/papers/paper_list_l1917_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA/figures/002_Figure_2.jpg]]
*Figure 2: Method overview: task instructions and input prompt are processed by a gating network to produce a mixture weights. Modality-specific inputs are aligned with word embedding via projection layers, and the final outputs are generated through the pre-trained model and the weighted combination of LoRA experts*

### 3.1 MoE LoRA 动态路由机制

HMVLM 的核心创新在于将**混合专家（Mixture of Experts）**范式引入低秩适配（LoRA）框架，通过门控网络实现任务感知的参数调制。与标准 LoRA 对所有输入使用固定适配器不同，MoE LoRA 维护 $n+1$ 个专家（包括一个特殊的零专家），并根据输入语义动态混合它们的贡献。

**门控网络** $\omega$ 是一个两层 MLP（隐藏维度 512），接收 CLIP 文本编码器输出的 512 维特征向量，预测专家混合权重 $\alpha = [\alpha_0, \alpha_1, \dots, \alpha_n]$。这些权重通过 softmax 归一化，决定每个 LoRA 专家对基础模型权重的调制程度。

**调制权重更新公式**为：

$$W' = W + \sum_{i=0}^{n} \alpha_i A_i B_i$$

其中：
- $W \in \mathbb{R}^{d \times k}$：预训练基础模型的原始权重矩阵
- $A_i \in \mathbb{R}^{d \times r}$，$B_i \in \mathbb{R}^{r \times k}$：第 $i$ 个 LoRA 专家的低秩分解矩阵，秩 $r=8$
- $\alpha_i$：门控网络为第 $i$ 个专家分配的混合权重，满足 $\sum_{i=0}^{n} \alpha_i = 1$
- $W'$：调制后的权重矩阵，用于实际前向计算

所有线性模块均应用 LoRA 适配器，实现参数高效微调。

### 3.2 零专家与灾难性遗忘缓解

**零专家**（$i=0$）是 MoE LoRA 框架中防止灾难性遗忘的关键设计。其参数 $A_0, B_0$ 被初始化为零矩阵，使得 $\alpha_0 A_0 B_0 = 0$，此时 $W' = W$，模型退化为原始预训练状态。

零专家具有双重功能：
1. **知识保留**：当门控网络为通用语言任务分配高 $\alpha_0$ 权重时，模型近似使用原始预训练参数，避免运动相关微调对语言能力的侵蚀。
2. **跨任务共享专家**：作为所有任务共享的通用专家，零专家为模型提供了稳定的参数锚点，使其他可训练专家可以专注于特定任务的适配。

实验证据表明，在通用对话（GD）任务中，零专家的平均门控权重达到 0.999（Table 3），验证了其在运动无关任务中的主导地位。

### 3.3 指令微调与损失函数

HMVLM 采用统一的指令微调范式。给定任务指令 $\mathcal{I}$、文本提示 $\mathcal{P}$ 和可选的模态输入 $\mathcal{X}$（图像、视频或运动序列），模型生成响应 $\mathcal{R}$：

$$\mathcal{R} = f_{\psi}(\mathcal{I}, \mathcal{P}, \mathcal{X})$$

其中 $f_{\psi}$ 表示参数为 $\psi$ 的完整 HMVLM 模型。模态特定输入通过投影层对齐到基础模型的词嵌入空间。

**基础模型损失** $\mathcal{L}_{fm}$ 为标准的下一个 token 预测损失：

$$\mathcal{L}_{fm} = -\mathbb{E}_{R_{gt}^t \in V} [\log p(R_{gt}^t | \mathcal{I}, \mathcal{P}, \boldsymbol{\chi}, R_{gt}^{<t})]$$

其中 $R_{gt}^t$ 为第 $t$ 个真实响应 token，$V$ 为扩展后的词表（包含运动离散 token），$R_{gt}^{<t}$ 表示前 $t-1$ 个真实 token。

**门控损失** $\mathcal{L}_{gat}$ 显式鼓励门控网络为运动无关任务选择零专家：

$$\mathcal{L}_{gat} = -\mathbb{E}[\eta * \log p_w(\alpha_0 | \mathbb{Z}, \mathcal{P})]$$

其中：
- $\eta \in \{0, 1\}$：指示函数，当任务为运动无关的通用语言任务时 $\eta=1$，否则 $\eta=0$
- $p_w(\alpha_0 | \mathbb{Z}, \mathcal{P})$：给定 CLIP 特征 $\mathbb{Z}$ 和提示 $\mathcal{P}$，门控网络预测的 $\alpha_0$ 权重
- $\mathcal{L}_{gat}$ 仅在 $\eta=1$ 时激活，推动 $\alpha_0 \to 1$

**总损失**为两者的和：

$$\mathcal{L}_{total} = \mathcal{L}_{fm} + \mathcal{L}_{gat}$$

消融实验（Table 1，w/o $\mathcal{L}_{gat}$ 行）证实，移除 $\mathcal{L}_{gat}$ 后 Vicuna-7B-v1.5 的 MT-Bench 平均分从 5.90 崩塌至 1.00，证明门控损失是知识保留的必要条件。

### 3.4 身体部位运动标记器

HMVLM 提出了一种基于身体部位的空间-时间标记器，替代传统的全身 1D 卷积 VQ-VAE，以提升运动表征的空间粒度。

**向量量化基础**：给定编码器输出 $\hat{z}_i$，通过可学习码本 $Z$ 进行离散化：

$$z_i = \mathcal{Q}(\hat{z}_i) := \underset{z_k \in Z}{\arg\min} \|\hat{z}_i - z_k\|^2$$

**空间编码**：将人体划分为 $N$ 个部位（如躯干、四肢），对单帧姿态 $m^f$ 进行逐部位编码：

$$[\hat{z}_{B1}^f, \hat{z}_{B2}^f, \dots, \hat{z}_{BN}^f] = \mathcal{E}_s(m^f)$$

其中 $\mathcal{E}_s$ 为引入可学习部位参数的 Transformer 空间编码器，每个部位独立生成潜在特征。

**时间压缩**：对每个部位的 $F$ 帧空间特征序列应用时间编码器 $\mathcal{E}_t$，以压缩比 $l$ 降低时间维度：

$$(\hat{z}_{Bn}^{'1}, \hat{z}_{Bn}^{'2}, \dots, \hat{z}_{Bn}^{'F/l}) = \mathcal{E}_t(\hat{z}_{Bn}^1, \dots, \hat{z}_{Bn}^F)$$

每个部位使用独立的码本进行量化，最终将离散 token 添加到基础模型的词表中。

消融实验（Table 5）表明，在码本大小 $K=512$ 时，身体部位标记器将 HumanML3D 上的 R-precision Top-3 从 0.741 提升至 0.785，重建 MSE 从 1.377 降至 0.966，验证了空间分解对运动表征精度的显著增益。该设计同时支持单帧姿态估计（无需时间压缩）和运动序列生成（需时间压缩），实现了自回归架构与静态任务的兼容。

## 实验与关键发现

### 主要实验结果

#### 知识保留：MoE LoRA 有效缓解灾难性遗忘

将人体运动模态集成到基础语言模型的核心瓶颈在于模态差距导致的灾难性遗忘。Table 1 给出了文本到运动（T2M）任务微调前后基础模型对话能力的量化对比。在相同基础模型 Gemma‑2‑2B‑it 上，HMVLM 的 MT-Bench 平均分仅从 7.79 降至 7.53（相对下降 3.34%），而 **MotionAgent** 在同一模型上从 7.79 崩塌至 1.00（下降 87.16%）。**MotionGPT** 在 Llama‑2‑7B 上也出现了 22.71% 的显著下降（2.73 → 2.11）。这表明 MoE LoRA 框架中的零专家机制和门控损失是知识保留的关键——去除门控损失 L_gat 后，Vicuna‑7B‑v1.5 的 MT-Bench 平均分从 5.90 直接崩塌至 1.00（Table 1 w/o L_gat 行）。

Table 3 进一步揭示了门控网络的动态路由行为：在通用对话（GD）任务中，零专家（expert 0）的平均门控权重高达 0.999，而其他可训练专家权重接近零；在 T2M、人体姿态估计（HPE）和人体视频理解（HVU）任务中，门控网络则分别激活不同的专家组合。这一结果验证了零专家作为“参数保护伞”的设计意图——当输入与运动无关时，模型几乎完全退回到预训练权重路径。

#### 文本到运动生成：单任务与多任务性能

Table 2 报告了 HumanML3D 数据集上的文本到运动生成结果。HMVLM 在单任务设置下取得了 R-precision Top‑1 0.502 ± .003、FID 0.123 ± .004、MM-Dist 3.039 ± .008 的成绩，在 FID 指标上显著优于 **MotionGPT‑2**（FID 0.191 ± .004）和 **MoMask**（FID 0.106 ± .004，但 R-precision Top‑1 仅为 0.433 ± .008）。HMVLM 在 R-precision Top‑1 上达到最优，表明其生成的运动序列与文本语义的匹配度更高。

![[assets/figures/papers/paper_list_l1917_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA/figures/005_Table_2.jpg]]
*Table 2: Quantitative results of text-to-motion on the HumanML3D dataset*

在多任务联合微调设置下，HMVLM 同时学习 T2M、HPE 和 HVU 三项任务，T2M 性能出现轻微下降（R-precision Top‑1 0.463、FID 0.156），但仍保持有竞争力的水平。KIT-ML 数据集上的结果（Table 6）呈现一致趋势，验证了框架的跨数据集泛化能力。Figure 7 的定性对比显示，HMVLM 生成的姿态序列在语义一致性上优于对比方法，红色框标注的语义错误明显更少。

![[assets/figures/papers/paper_list_l1917_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative comparison on text-to-motion task. The provided state-of-the-art methods are under the same training and inference setting on HumanML3D [21]. The red box highlights the poses that do not match the prompt semantics*

![[assets/figures/papers/paper_list_l1917_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA/figures/017_Table_6.jpg]]
*Table 6: Quantitative results of text-to-motion on the KIT-ML dataset*

#### 人体姿态估计

Table 4 报告了 Human3.6M 和 3DPW 数据集上的姿态估计结果。HMVLM 在单任务设置下优于专门的基础模型姿态估计方法 **ChatPose**（该点需核实具体数值，分析数据中仅提供定性描述）。Figure 4 和 Figure 8 的定性可视化显示，HMVLM 在遮挡和复杂姿态场景下的估计结果更接近真实值。这一性能提升归因于身体部位标记器提供的空间粒度——每帧姿态被分解为 5 个部位（躯干 + 四肢）独立编码，使得模型能够更精确地捕捉局部关节位置。

![[assets/figures/papers/paper_list_l1917_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results for human pose estimation and human video understanding*

#### 人体视频理解

Figure 4 和 Figure 9 展示了人体运动视频理解的定性结果。模型能够根据视频帧序列生成关于动作类型、运动状态的文本描述。然而，视频理解基于均匀采样若干帧输入模型，若关键动作帧未被采样到，可能导致语义错误或幻觉（见局限性分析）。

### 消融实验

#### 身体部位标记器的空间分解效果

Table 5 对比了不同标记器设计在 HumanML3D 上的重建质量和下游 T2M 性能。在相同码本大小 K=512 下，身体部位标记器（Body-part）相比全身 1D 卷积标记器（Whole-body）将 R-precision Top‑3 从 0.741 提升至 0.785，重建 MSE 从 1.377 降至 0.966。当码本增大到 K=1024 时，重建 MSE 进一步降至 0.854，但 T2M 性能（FID 0.146）相比 K=512（FID 0.123）反而下降，表明过大的码本可能引入冗余离散化噪声。这一结果验证了空间分解策略的有效性——将人体按部位独立量化为运动表征提供了更精细的空间粒度，同时避免了单一码本对全局姿态的粗粒度压缩。

![[assets/figures/papers/paper_list_l1917_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA/figures/010_Table_5.jpg]]
*Table 5: Abalation study on different tokenizers. K represent the codebook size*

#### 门控损失 L_gat 的关键作用

Table 1 中 w/o L_gat 行的结果是最具决定性的消融证据：去除门控损失后，Vicuna‑7B‑v1.5 的 MT-Bench 平均分从 5.90 崩塌至 1.00，表明模型完全丧失了通用对话能力。L_gat 通过鼓励门控网络在运动无关任务上选择零专家，迫使可训练专家专注于运动相关知识的建模，从而在参数空间实现任务隔离。没有这一约束，LoRA 专家会污染预训练权重，导致不可逆的遗忘。

#### 专家数量与效率权衡

Figure 5 分析了不同专家数量下 MoE LoRA 的训练时间、参数量、推理延迟和 T2M 性能。随着专家数量增加，训练时间和参数量近似线性增长，但推理延迟在超过 5 个专家后增速加快。T2M 性能在 5 个专家时趋于饱和，继续增加专家带来的边际收益递减。这一分析为实际部署中的专家数量选择提供了效率参考。

### 失败模式与局限性

1. **多任务性能折损**：在多任务联合微调中，由于参数预算固定，单任务性能相比单独微调有轻微下降（Table 2 中 Multi-task 行 vs Single-task 行）。这是共享专家容量下的固有权衡。

2. **视频采样的关键帧遗漏**：视频理解模块基于均匀采样策略，若关键动作帧未被采样到，模型可能产生语义错误或幻觉。Figure 9 中可能存在的错误描述需人工核实。

3. **任务扩展的重新训练成本**：当前框架主要支持三种预定义的下游任务（T2M、HPE、HVU）。扩展到新的运动相关任务需要重新训练门控网络并添加新的 LoRA 专家，无法实现零样本任务迁移。

4. **跨模态生成缺失**：框架仅实现人体运动与文本或视频的独立配对，尚未探索图像到文本或视频到运动的直接跨模态生成。

5. **身体部位分割的粒度限制**：当前采用固定的 5 部位分割（躯干 + 四肢），对于手指动作、面部表情等更细粒度的运动表征可能不足。Table 5 中 K=1024 时 T2M 性能下降也暗示了当前空间分解策略在高维码本下的优化困难。

## 定位与知识库关联

### 1. 与现有基线方法的关系

HMVLM 试图在一条统一的技术路径上同时解决两个长期困扰多模态基础模型的问题：**灾难性遗忘**与**人体运动表征的粒度不足**。为理解其定位，需将其置于以下几条方法线的交汇处。

**运动-语言模型线**。以 **MotionGPT** 和 **MotionAgent** 为代表的工作率先探索了将运动模态注入语言模型的可行性。MotionGPT 采用 VQ-VAE 对运动序列进行离散化，随后在 Llama 等基础模型上进行自回归微调，但其在微调后对话能力出现严重退化（Table 1 中 Llama2 Tuned 的 MT-Bench 平均分从 2.73 降至 2.11，降幅 22.71%）。MotionAgent 则采用 GPT-4 协调的多智能体框架，虽避免了直接微调基础模型，却引入了高昂的推理成本和系统复杂性。HMVLM 在目标设定上与这两者一致——使语言模型理解并生成运动——但在实现路径上做出了关键分叉：它拒绝将运动适配视为一个“全模型微调”或“外部编排”问题，转而将其建模为一个**动态参数路由问题**。

**LoRA 高效微调线**。标准 LoRA 通过在冻结的预训练权重旁插入低秩矩阵对来实现任务适配，但它缺乏对多任务间参数冲突的显式管理机制。HMVLM 将 LoRA 扩展为专家混合形式，其关键创新不在于“使用多个 LoRA”，而在于引入了一个**不可训练的零专家**（zero expert）。该专家的 LoRA 矩阵 $A_0, B_0$ 被初始化为零，使得当门控权重 $\alpha_0 \to 1$ 时，调制后的权重 $W' = W + \alpha_0 A_0 B_0$ 退化为原始预训练权重 $W$。这一设计将“遗忘”问题从损失函数层面的正则化（如权重衰减）提升到了架构层面：基础模型的原始知识被固化为一个始终可访问的专家路径。

**运动标记化线**。此前的运动离散化方法——包括 **T2M-GPT** 和 **MoMask** 所使用的 1D 卷积 VQ-VAE——将整个身体骨架视为一个扁平向量进行时序编码。这种“整体式”标记化忽略了人体的空间结构先验，导致单帧姿态的重建精度受限。HMVLM 提出的身体部位标记器（Figure 3a）将人体划分为躯干与四肢等 $N$ 个部位，对每一帧的姿态 $m^f$ 先进行空间编码得到部位特征 $[\hat{z}_{B1}^f, \dots, \hat{z}_{BN}^f]$，再沿时间轴压缩。这一设计使得标记器在服务于自回归生成任务的同时，也能为姿态估计这类静态任务提供更精确的 token 表示。消融实验（Table 5）证实了这一改进的因果效应：在相同码本大小 $K=512$ 下，引入身体部位分解将 HumanML3D 上的 R-precision Top-3 从 0.741 提升至 0.785，重建 MSE 从 1.377 降至 0.966。

**姿态估计基础模型线**。**ChatPose** 代表了将基础模型用于人体姿态估计的早期尝试。HMVLM 在 Human3.6M 和 3DPW 上的姿态估计结果（Table 4, Figure 4, Figure 8）表明其单任务性能可超越 ChatPose，但需要指出的是，原文未提供具体的 MPJPE 数值对比，仅给出了定性描述和可视化结果，该结论的精确置信度需手动验证。

### 2. 适用边界

HMVLM 的适用边界由其三个核心设计决策共同界定。

**任务边界**。当前框架明确支持三类下游任务：文本到运动生成（T2M）、人体姿态估计（HPE）和人体视频理解（HVU）。这些任务共享一个关键特征——它们都以人体运动为核心模态，且输入输出均可被格式化为指令-响应对（Table 7 提供了各任务的指令模板）。对于超出此范围的任务（如直接的图像到文本描述、视频到运动生成），作者明确指出尚未探索。这意味着 HMVLM 目前是一个**以运动为中心的垂类多模态模型**，而非通用的全模态基础模型。

**遗忘缓解的边界**。MoE LoRA 在 Gemma-2-2b-it 上将 MT-Bench 下降控制在 3.34%（7.79 → 7.53），远优于 MotionAgent 的 87.16%（7.79 → 1.00）。但这一效果高度依赖于门控损失 $\mathcal{L}_{gat}$ 的存在：去除该损失后，Vicuna-7B-v1.5 的 MT-Bench 平均分从 5.90 崩塌至 1.00（Table 1, w/o L_gat 行）。这意味着当任务分布与训练分布存在显著偏移时，若门控网络无法正确识别“运动无关”的上下文，遗忘仍可能发生。此外，零专家在通用对话中的平均门控权重达到 0.999（Table 3），表明当前的门控行为是高度极化的——这对于已知任务类型有效，但在面对开放域的自由形式输入时，门控的鲁棒性尚未得到验证。

**视频理解的边界**。视频理解模块采用均匀采样若干帧输入模型。作者明确指出，若关键动作帧未被采样到，可能导致语义错误或幻觉。这是一个结构性的脆弱点：均匀采样策略缺乏对运动显著性的感知能力，在快速动作或细微信号场景下容易失效。

**多任务联合的边界**。当同时微调多个任务时，单任务性能相比单独微调出现轻微下降（Table 2 中 multi-task 的 FID 从 0.123 升至 0.156，R-precision Top-1 从 0.502 降至 0.463）。这是因为 MoE LoRA 的参数预算固定（5 个专家，其中 1 个为零专家），多任务共享有限的专家容量必然导致表示冲突。Figure 5 进一步揭示了专家数量与效率的权衡：增加专家数量可提升性能，但训练时间和推理延迟也随之线性增长。

### 3. 局限与开放问题

**架构层面的深层机制未明**。零专家在形式上等价于“不做任何低秩调制”，但 Table 3 显示其在不同任务上并非总是权重最高——它在通用对话中占主导（0.999），而在 T2M 和 HPE 任务中权重较低。这引出一个开放问题：零专家是否仅仅是一个“静态权重恢复器”，还是实际上参与学习了某种跨任务的通用表示？目前的分析仅停留在门控权重的统计层面，缺乏对零专家路径内部表征的深入探查。

**身体部位分割的粒度上限**。当前的身体部位标记器将人体划分为 5 个部位（躯干 + 四肢），这一粒度对于全身性的大幅度运动足够，但对于需要精细控制的场景——如面部表情、手指姿态、脚踝旋转——可能不足。一个更深层的问题是：固定的解剖学分割是否是最优的？是否存在一种可学习的“功能部位分割”，使得标记器能根据运动类型自动调整部位边界？

**视频关键帧采样的鲁棒性**。均匀采样的脆弱性已被作者识别为已知局限。可能的改进方向包括基于运动显著性的自适应采样、可学习的帧选择器，或利用光流信息引导帧选择。但这些方案均会引入额外的计算开销，与框架的端到端简洁性形成张力。

**任务扩展的可迁移性**。当前框架的任务集是封闭的——门控网络和专家数量在训练前就已固定。若要添加新的运动相关任务（如运动修复、运动风格迁移），需要重新训练门控网络并可能增加专家。这限制了 HMVLM 作为一个“运动基础模型”的即插即用能力。一个开放问题是：能否设计一种增量式的专家添加机制，使得新任务的适配不会干扰已有的专家路由？

**跨模态生成的缺失**。HMVLM 目前仅实现了文本到运动、图像/视频到姿态估计等单向映射，尚未探索直接的模态间生成（如图像到运动、视频到文本描述）。这一局限部分源于训练数据的配对约束，部分源于架构设计中各模态投影层之间缺乏显式的跨模态对齐损失。

## 原文 PDF

![[paperPDFs/NEURIPS_2025/HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA.pdf]]

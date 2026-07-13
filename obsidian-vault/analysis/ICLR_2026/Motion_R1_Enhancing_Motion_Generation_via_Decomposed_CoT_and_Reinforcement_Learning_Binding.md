---
title: "Motion-R1: Enhancing Motion Generation via Decomposed CoT and Reinforcement Learning Binding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforcement_Learning_Binding.pdf
project_link: https://motion-r1.github.io/
code_link: null
aliases:
- MR
- Motion-R1
tags:
- ICLR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入分解式 CoT 数据引擎自动生成结构化推理路径，并设计 RL Binding 策略将多模态对齐嵌入奖励函数，从而指导模型生成语义准确、动作真实的运动。"
primary_logic: "通过自动化的 CoT 推理将高层指令分解为子动作，结合简化的 GRPO 多模态奖励（格式、运动相似度、语义相似度），无需人工标注即可实现高质量且可解释的动作生成。"
claims:
- "在 HumanML3D 上 MM-Dist 指标提升 3.5%，达到最佳 2.854，超过此前最佳 MoMask 的 2.958。"
- "在 KIT-ML 上 R-Precision Top-1/2/3 和 FID 均达最佳，其中 R-Precision@1 为 0.431，FID 为 0.287。"
- "在 BABEL 多标签数据集上全部四项指标均达 SOTA，FID 仅为 0.53，远低于之前的最佳 1.14。"
- "消融实验表明，同时使用 Decomposed CoT 和 RL Binding 奖励机制时，FID 和 R-Precision 达到最佳，单独使用 CoT 或单一奖励效果较差。"
---

# Motion-R1: Enhancing Motion Generation via Decomposed CoT and Reinforcement Learning Binding

> [!tip] 核心洞察
> 通过自动化的 CoT 推理将高层指令分解为子动作，结合简化的 GRPO 多模态奖励（格式、运动相似度、语义相似度），无需人工标注即可实现高质量且可解释的动作生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion-R1：通过分解式思维链与强化学习绑定增强动作生成 |
| 英文题名 | Motion-R1: Enhancing Motion Generation via Decomposed CoT and Reinforcement Learning Binding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.10353) · [Project](https://motion-r1.github.io/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | Motion-R1 |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，MM-Dist 为 2.854，对比 2.958 (MoMask)，变化 -0.104。
> - HumanML3D 上，R-Precision Top-3 为 0.818，对比 0.807 (MoMask)，变化 +0.011。
> - KIT-ML 上，FID 为 0.287，对比 0.497 (MDM)，变化 -0.210。

## 概要

**核心问题**：现有文本-动作生成方法面临双重瓶颈。一方面，端到端模型难以捕捉复杂自然语言中的时序与因果关系，导致动作不连贯或过度简化，在分布外指令上泛化能力尤其薄弱；另一方面，基于强化学习（RL）的方法设计复杂，依赖昂贵的人工标注来训练偏好模型（如 MotionCritic），难以规模化应用。

**核心洞察**：Motion-R1 提出“分解式思维链（Decomposed CoT）+ 强化学习绑定（RL Binding）”双轮驱动方案。通过自动化 CoT 数据引擎将高层指令拆解为子动作推理路径，并借助简化的 GRPO 多模态奖励（格式、运动相似度、语义相似度）将对齐信号嵌入 RL 优化过程，在无需人工标注的前提下实现语义准确、动作真实且可解释的运动生成。

**方法定位**：Motion-R1 属于“LLM 驱动的运动生成”路线，与 **MotionGPT**（Jiang et al., 2023）的 GPT+VQ-VAE 范式、**MotionLLM**（Wu et al., 2024）的语义规划思路一脉相承，但首次将 CoT 推理与 GRPO 强化学习绑定引入该领域。其流水线由 VQ-VAE 动作分词器、基于 Qwen-2.5-3B-Instruct 的 LLM 骨干、分解式 CoT 数据引擎和 GRPO RL Binding 四模块构成，形成“冷启动监督微调→RL 对齐优化”的两阶段训练范式。

**主要结果**：在 HumanML3D 上，MM-Dist 指标提升 3.5%（从 MoMask 的 2.958 降至 2.854），R-Precision Top-3 达 0.818；在 KIT-ML 上，FID 降至 0.287，R-Precision@1 达 0.431，均刷新记录；在 BABEL 多标签数据集上，四项指标全面 SOTA，FID 仅 0.53（此前最佳为 1.14）。消融实验证实，CoT 推理与多模态奖励缺一不可——单独使用 CoT 数据引擎时 R-Precision Top-1 仅 0.340、FID 高达 0.530，而完整的 CoT + 语义奖励 + 运动奖励组合使 FID 降至 0.201、R-Precision Top-1 升至 0.515。



文本驱动的三维人体动作生成旨在根据自然语言描述合成逼真、语义一致的人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。然而，现有方法面临两个核心瓶颈。

**端到端模型的泛化困境。** 以 **MDM**（Tevet et al., 2023）、**MoMask**（Guo et al., 2024）和 **MotionGPT**（Jiang et al., 2023）为代表的传统方法，将文本到动作的映射建模为直接的端到端生成过程。这些模型在分布内（in-distribution）指令上表现尚可，但面对需要多步时序推理或包含复杂因果关系的分布外（out-of-distribution）指令时，往往产生不连贯或过度简化的动作序列。其根本原因在于，高层指令中隐含的子动作分解、时序依赖和空间约束无法被单一前向映射有效捕捉——模型缺乏将复杂语义拆解为可执行子步骤的结构化推理能力（Figure 1a）。

**基于强化学习方法的标注依赖。** 为提升语义对齐质量，近期工作尝试引入强化学习（RL）来优化动作生成。然而，现有 RL 方案通常依赖昂贵的人工标注来训练偏好模型（如 MotionCritic），以此构建奖励信号。这种设计不仅增加了数据获取成本，还限制了方法向大规模实际应用的扩展（Figure 1c）。同时，复杂的多阶段 RL 训练流程进一步提高了工程实现的门槛。

针对上述缺口，本文提出 **Motion-R1**，其核心动机在于：**通过自动化的分解式思维链（Decomposed Chain-of-Thought, CoT）推理，将高层指令转化为结构化的子动作规划，并结合简化的 RL 绑定（RL Binding）策略，在无需人工标注的条件下实现语义准确、动作真实且可解释的运动生成**（Figure 1b, 1d）。具体而言，Motion-R1 引入两大创新：一是 Decomposed CoT Data Engine，利用大语言模型自动合成逐步推理数据，使模型显式学习“思考如何运动”的中间推理过程；二是 RL Binding 机制，将多模态对齐嵌入 GRPO 优化的奖励函数中，通过格式奖励、运动相似度奖励和语义相似度奖励三项自动化信号，直接指导模型在推理与生成两个层面同时对齐文本语义与运动真实性。



## 核心方法与创新机理

Motion-R1 的核心创新围绕两个相互协同的机制展开：**分解式思维链（Decomposed CoT）数据引擎**和**基于强化学习的绑定策略（RL Binding）**。二者共同解决了现有文本-动作生成中的关键瓶颈——传统端到端模型无法有效捕捉复杂自然语言中的时序与因果关系，而现有 RL 方法则依赖昂贵的人工标注。

### 创新一：Decomposed CoT 数据引擎

传统方法（如 **MDM** Tevet et al., 2023；**MoMask** Guo et al., 2024）采用端到端映射，直接将文本映射为动作序列，缺乏中间推理步骤。当面对分布外（OOD）指令或包含多步时序逻辑的复杂描述时，这类方法往往生成不连贯或过度简化的动作（见 Figure 1a）。

Motion-R1 引入的 Decomposed CoT 数据引擎改变了这一范式。该引擎利用大语言模型（LLM）自动将高层指令分解为结构化的逐步推理规划，生成包含 `<think>`、`<output>` 和 `<Motion>` token 的推理轨迹（见 Figure 2）。其关键改变在于：

- **推理步骤**：从“无”（端到端映射）变为“有”（Decomposed CoT 推理生成子动作序列），使模型能够显式地对复杂指令进行时序和因果分解。
- **数据获取**：通过自动化 CoT 标注管线，无需人工介入即可合成高质量的推理数据，大幅降低了数据获取成本。

这一设计使模型在分布外指令上展现出更强的泛化能力（Figure 1b），能够理解如“沿无限符号形状的路径缓慢行走”这类需要多步推理的抽象指令（Figure 4）。

### 创新二：RL Binding 策略

现有基于 RL 的动作生成方法（如 MotionCritic）需要训练偏好模型，依赖昂贵的人类标注来提供奖励信号（Figure 1c）。Motion-R1 提出的 RL Binding 策略则通过**将多模态对齐嵌入奖励函数**，实现了无需人工标注的高效优化。

具体而言，RL Binding 采用 GRPO（Group Relative Policy Optimization）优化框架，并设计了三种自动化奖励函数：

- **格式奖励**：约束输出格式的规范性。
- **运动相似度奖励**（$r_{\text{motion}}$）：衡量生成动作与真实动作特征间的余弦相似度，保证动作真实性。
- **语义相似度奖励**（$r_{\text{semantic}}$）：衡量生成动作与输入文本特征间的余弦相似度，保证语义对齐。

与基线方法相比，RL 奖励函数的设计从“复杂 RL 需要人工标注的偏好模型”转变为“三种自动化奖励的组合”，实现了高效的多模态对齐（Figure 1d）。

### 协同效应

消融实验（Table 2）揭示了两个创新的协同关系：单独使用 Decomposed CoT 数据引擎时效果最差（HumanML3D 上 R-Precision Top-1 仅 0.340，FID 为 0.530），而同时使用 CoT 与完整的 $R_{\text{sem}} + R_{\text{motion}}$ 奖励组合时达到最优（FID 0.201，R-Precision Top-1 0.515）。这表明**推理分解与奖励对齐缺一不可**——CoT 提供了结构化的语义理解基础，RL Binding 则通过多模态奖励将其与真实动作分布对齐，二者共同驱动了性能的显著提升。



Motion-R1 的整体 pipeline 由两大核心组件构成：一个预训练的**动作分词器（Motion Tokenizer）**和一个具备动作导向推理能力的**大语言模型（LLM）**。训练过程分为两个阶段：首先通过监督微调进行冷启动，然后引入基于 GRPO 的强化学习绑定（RL Binding）策略进行优化。

### 动作分词器：连续动作到离散 Token 的桥梁

动作分词器采用 VQ-VAE 架构，负责将连续的 3D 人体运动序列压缩为离散的码本索引序列。其工作流程如下：编码器将原始运动帧映射为潜在向量 $\mathbf{z}_i$，随后通过最近邻查找将其量化为码本 $\mathbf{C}$ 中的离散向量：

$$\hat{\mathbf{z}}_i = \arg\min_{\mathbf{c}_n \in \mathbf{C}} \| \mathbf{z}_i - \mathbf{c}_n \|_2$$

该分词器的训练目标为三项损失的组合：

$$L_{\mathrm{vq}} = L_{\mathrm{reconstruct}} + L_{\mathrm{commit}} + L_{\mathrm{embed}}$$

分别对应运动重建质量、编码器输出向码本向量靠拢的承诺损失，以及码本向量的嵌入更新。量化后的码本索引序列即为 LLM 可直接处理的“动作语言”。

### 推理骨干：LLM 驱动的动作生成

Motion-R1 采用 **Qwen-2.5-3B-Instruct** 作为 LLM 骨干。在推理时，模型接收文本指令，通过分解式思维链（Decomposed CoT）生成包含 `<think>`（推理过程）、`<output>`（动作描述）和 `<Motion>`（动作 token）的结构化输出，最终由动作分词器的解码器将 `<Motion>` token 序列重建为连续运动序列。

### 两阶段训练流程

**第一阶段：冷启动监督微调（Cold-Start SFT）**。利用 Decomposed CoT Data Engine 自动构建的“文本描述—CoT 推理轨迹—动作 token 序列”三元组，对 LLM 进行监督微调，使其初步具备生成结构化推理路径和对应动作 token 的能力。

**第二阶段：RL Binding 强化学习优化**。将文本到动作的生成形式化为强化学习问题，采用 GRPO 算法进行策略优化，目标函数为：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{c} \left[ \frac{1}{G} \sum_{i=1}^{G} \min \left( \frac{\pi_{\theta}(o_i | q)}{\pi_{\mathrm{old}}(o_i | q)} \hat{A}_i, \mathrm{clip} \left( \frac{\pi_{\theta}(o_i | q)}{\pi_{\mathrm{old}}(o_i | q)}, 1 - \varepsilon, 1 + \varepsilon \right) \hat{A}_i \right) - \beta \cdot D_{\mathrm{KL}}(\pi_{\theta} \parallel \pi_{\mathrm{ref}}) \right]$$

其中包含重要性采样的裁剪机制和 KL 散度惩罚项，确保策略更新稳定。

RL Binding 的核心创新在于**将多模态对齐直接嵌入奖励函数**，设计了三种无需人工标注的自动化奖励：

- **格式奖励**：约束输出严格遵循 `<think>/<output>/<Motion>` 的结构模板。
- **运动相似度奖励**：衡量生成动作与真实动作特征间的余弦相似度：
  $$r_{\mathrm{motion}} = \frac{f_{\mathrm{motion}}(\hat{\mathbf{m}}) \cdot f_{\mathrm{motion}}(\mathbf{m})}{\| f_{\mathrm{motion}}(\hat{\mathbf{m}}) \|_2 \cdot \| f_{\mathrm{motion}}(\mathbf{m}) \|_2}$$
- **语义相似度奖励**：衡量生成动作与输入文本在共享潜在空间中的对齐程度：
  $$r_{\mathrm{semantic}} = \frac{f_{\mathrm{motion}}(\hat{\mathbf{m}}) \cdot f_{\mathrm{text}}(T)}{\| f_{\mathrm{motion}}(\hat{\mathbf{m}}) \|_2 \cdot \| f_{\mathrm{text}}(T) \|_2}$$

### 数据流与模块关系

整体数据流可概括为：**文本指令 → Decomposed CoT Data Engine（自动生成推理轨迹）→ LLM 推理生成动作 token → 动作分词器解码 → 连续运动序列**。在 RL 阶段，生成的序列经由三种奖励函数评估后，通过 GRPO 反馈更新 LLM 策略参数，形成闭环优化。Figure 2 完整展示了这一两阶段框架，突出 Decomposed CoT Data Engine 的结构化推理生成和 RL Binding 的多模态对齐机制。

### 关键设计决策

与现有基于 LLM 的动作生成方法（如 **MotionLLM**（Wu et al., 2024））相比，Motion-R1 的关键差异在于：前者仅进行端到端映射，而 Motion-R1 通过 Decomposed CoT 将高层指令显式分解为子动作序列，使模型具备可解释的逐步推理能力。与依赖昂贵人工标注偏好模型的 RL 方法（如 MotionCritic）相比，RL Binding 通过三种自动化奖励函数实现了同等的语义对齐和运动真实性约束，大幅降低了实际部署成本。

### 补充图表

![[assets/figures/papers/paper_list_l15_Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforceme/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of traditional approaches and our Motion-R1 framework. (a) Traditional end-to-end models exhibit poor generalization on out-of-distribution motions. (b) Our Decomposed CoT Data Engine enables strong generalization by structuring high-level instructions into intermediate reasoning steps. (c) Existing RL-based methods rely on expensive human annotations to train preference models for reward signals. (d) Our RL Binding mechanism achieves efficient multimodal alignment without additional annotation cost*



Motion-R1 框架的核心由两大模块构成：**Decomposed CoT Data Engine**（分解式思维链数据引擎）与 **RL Binding**（强化学习绑定机制）。前者负责将高层自然语言指令自动拆解为结构化的逐步推理路径，后者则通过多模态对齐奖励函数引导模型生成语义准确、动作真实的运动序列。以下逐一展开关键模块及其公式。

---

### 3.1 Motion Tokenizer（动作分词器）

动作分词器是整个框架的感知基础，负责将连续的人体运动序列离散化为有限的 token 序列，使 LLM 能够以语言建模的方式处理动作生成任务。该模块采用 **VQ-VAE** 架构，包含编码器、量化器和解码器三个子组件。

给定输入运动序列 $\mathbf{m}$，编码器将其映射为潜在嵌入 $\mathbf{z}_i$，随后通过向量量化将每个嵌入映射到码本 $\mathbf{C}$ 中最接近的向量：

$$\hat{\mathbf{z}}_i = \arg\min_{\mathbf{c}_n \in \mathbf{C}} \|\mathbf{z}_i - \mathbf{c}_n\|_2 \tag{1}$$

其中 $\mathbf{C} = \{\mathbf{c}_1, \mathbf{c}_2, \dots, \mathbf{c}_N\}$ 为可学习的码本，$N$ 为码本大小。量化后的嵌入 $\hat{\mathbf{z}}_i$ 经解码器重建为运动序列 $\hat{\mathbf{m}}$。

VQ-VAE 的训练目标由三项损失复合而成：

$$L_{\mathrm{vq}} = L_{\mathrm{reconstruct}} + L_{\mathrm{commit}} + L_{\mathrm{embed}} \tag{2}$$

- **$L_{\mathrm{reconstruct}}$**：重建损失，约束解码器输出与原始运动的保真度。
- **$L_{\mathrm{commit}}$**：承诺损失，强制编码器输出靠近选定的码本向量，防止码本空间漂移。
- **$L_{\mathrm{embed}}$**：嵌入损失，直接优化码本向量本身。

训练完成后，任意运动序列均可表示为一串离散的 token 索引，为后续 LLM 的条件生成提供统一的符号接口。

---

### 3.2 Decomposed CoT Data Engine（分解式思维链数据引擎）

传统文本-动作生成方法直接从自然语言指令端到端映射到运动序列，缺乏对复杂时序和因果关系的显式建模能力。Decomposed CoT Data Engine 的核心创新在于：利用通用 LLM 的推理能力，将高层指令自动分解为结构化的逐步推理路径，形成 `<think>` → `<output>` → `<Motion>` 的三段式规划轨迹。

具体而言，数据引擎接收原始文本描述 $T$，通过精心设计的提示模板驱动 LLM 生成以下结构化输出：

1. **`<think>` 段**：包含对动作的时序分解和因果推理，例如“先迈左脚，随后身体重心前移，同时双臂自然摆动”。
2. **`<output>` 段**：将推理结果凝练为简洁的动作描述，作为连接推理与生成的桥梁。
3. **`<Motion>` 段**：对应的离散动作 token 序列，由预训练的 Motion Tokenizer 编码得到。

这一自动化的 CoT 标注管线无需任何人工标注，即可为每条运动数据生成高质量的推理路径。在训练阶段，LLM Backbone（基于 **Qwen-2.5-3B-Instruct**）以文本 $T$ 为输入，自回归地预测完整的 `<think>` → `<output>` → `<Motion>` 序列，从而内化分解式推理能力。

---

### 3.3 RL Binding（强化学习绑定机制）

仅靠监督微调（SFT）难以保证生成动作的语义准确性和运动真实性。RL Binding 将文本-动作生成形式化为强化学习问题，采用 **GRPO**（Group Relative Policy Optimization）作为优化策略，并通过三种自动化奖励函数实现多模态对齐，完全消除了对昂贵人工标注的依赖。

#### 3.3.1 GRPO 优化目标

GRPO 的核心思想是对同一输入采样一组候选输出，以组内相对优势估计替代传统的价值函数，从而降低训练方差。其优化目标为：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{c} \left[ \frac{1}{G} \sum_{i=1}^{G} \min \left( \frac{\pi_{\theta}(o_i | q)}{\pi_{\mathrm{old}}(o_i | q)} \hat{A}_i, \mathrm{clip} \left( \frac{\pi_{\theta}(o_i | q)}{\pi_{\mathrm{old}}(o_i | q)}, 1 - \varepsilon, 1 + \varepsilon \right) \hat{A}_i \right) - \beta \cdot D_{\mathrm{KL}}(\pi_{\theta} \parallel \pi_{\mathrm{ref}}) \right] \tag{3}$$

- **$\pi_{\theta}$**：当前策略（待优化的 LLM）。
- **$\pi_{\mathrm{old}}$**：旧策略（用于重要性采样）。
- **$\pi_{\mathrm{ref}}$**：参考策略（通常为 SFT 后的模型）。
- **$G$**：每组采样的候选输出数量。
- **$\hat{A}_i$**：组内标准化后的优势估计，由奖励值归一化得到。
- **$\varepsilon$**：裁剪阈值，约束策略更新幅度。
- **$\beta \cdot D_{\mathrm{KL}}$**：KL 散度惩罚项，防止策略偏离参考模型过远。

#### 3.3.2 三类奖励函数

RL Binding 的核心在于三类自动化奖励函数的设计，分别从格式合规性、运动真实性和语义对齐三个维度提供反馈信号：

**（1）格式奖励（Format Reward）**
约束生成输出的结构完整性，要求输出必须严格遵循 `<think>` → `<output>` → `<Motion>` 的三段式格式，且 `<Motion>` 段中的 token 必须全部属于合法的码本索引范围。格式正确的输出获得正奖励，否则获得零奖励。

**（2）运动相似度奖励（Motion Similarity Reward）**
衡量生成动作与真实动作在特征空间中的一致性。给定生成动作 $\hat{\mathbf{m}}$ 和真实动作 $\mathbf{m}$，通过预训练的运动编码器 $f_{\mathrm{motion}}$ 提取嵌入后计算余弦相似度：

$$r_{\mathrm{motion}} = \frac{f_{\mathrm{motion}}(\hat{\mathbf{m}}) \cdot f_{\mathrm{motion}}(\mathbf{m})}{\| f_{\mathrm{motion}}(\hat{\mathbf{m}}) \|_2 \cdot \| f_{\mathrm{motion}}(\mathbf{m}) \|_2} \tag{4}$$

该奖励直接鼓励模型生成与真实人体运动分布一致的动作，抑制不自然的关节运动或时序异常。

**（3）语义相似度奖励（Semantic Similarity Reward）**
衡量生成动作与输入文本描述之间的语义对齐程度。利用同一运动编码器 $f_{\mathrm{motion}}$ 和文本编码器 $f_{\mathrm{text}}$（来自预训练的多模态对齐模型），将生成动作 $\hat{\mathbf{m}}$ 和输入文本 $T$ 映射到共享潜在空间后计算余弦相似度：

$$r_{\mathrm{semantic}} = \frac{f_{\mathrm{motion}}(\hat{\mathbf{m}}) \cdot f_{\mathrm{text}}(T)}{\| f_{\mathrm{motion}}(\hat{\mathbf{m}}) \|_2 \cdot \| f_{\mathrm{text}}(T) \|_2} \tag{5}$$

该奖励确保生成的动作在语义层面忠实于用户指令，避免出现“动作正确但含义错误”的偏差。

最终，总奖励为三类奖励的加权组合，权重通过实验调优确定。消融实验（Table 2）证实，同时使用 CoT 推理与 $r_{\mathrm{semantic}} + r_{\mathrm{motion}}$ 的组合时，模型在 HumanML3D 上取得最优的 FID（0.201）和 R-Precision Top-1（0.515），而单独使用 CoT 或单一奖励均导致性能显著下降，表明推理结构与多模态对齐奖励之间存在强协同效应。

---

### 3.4 训练流程总结

Motion-R1 的训练分为两个阶段：

1. **冷启动监督微调（Cold-Start SFT）**：利用 Decomposed CoT Data Engine 生成的（文本，CoT 推理，动作 token）三元组对 LLM Backbone 进行监督微调，使模型初步掌握分解式推理和动作 token 生成能力。
2. **RL Binding 强化学习微调**：在 SFT 模型基础上，采用 GRPO 策略和上述三类奖励函数进行强化学习优化，进一步提升生成动作的语义准确性和运动真实性。

这一两阶段设计充分利用了 CoT 数据的结构化先验和 RL 的探索能力，在无需人工标注的条件下实现了高质量的动作生成。



## 实验与关键发现

### 主实验：跨基准定量对比

Motion-R1 在三个主流文本-动作生成基准上进行了系统评估。所有实验均在 8 块 NVIDIA H20 GPU 上完成，每项指标重复 20 次并报告 95% 置信区间，对比基线均采用官方开源实现或原文最佳配置。

**HumanML3D 数据集**（Table 1）。Motion-R1 在多项核心指标上达到最优或次优。R-Precision Top-1/2/3 分别达到 **0.515 / 0.719 / 0.818**，其中 Top-2 和 Top-3 均为表中最佳，表明生成动作与文本描述的语义匹配精度显著领先。FID 降至 **0.201**，为表中第二优，仅略高于 MoMask（0.194），但显著优于 MDM（0.544）等扩散基线。MM-Dist 达到 **2.854**，较此前最佳 MoMask 的 2.958 提升 **3.5%**，反映出生成动作与真实动作在特征空间中的分布距离进一步缩小。

**KIT-ML 数据集**（Table 1）。Motion-R1 在 KIT-ML 上同样展现出强竞争力。R-Precision Top-1 达到 **0.431**，超过此前最佳 MotionDiffuse 的 0.417；FID 降至 **0.287**，大幅优于 MDM 的 0.497。MM-Dist 为 2.789，仅次于 MoMask 的 2.779，差距极小。

**BABEL 多标签数据集**（Table 3）。在更具挑战性的多标签场景下，Motion-R1 在全部四项指标上均达到 SOTA。FID 仅 **0.53**，远低于此前最佳 InfiniDreamer/DoubleTake 的 1.14，降幅超过 53%。这一结果验证了 Decomposed CoT 在复杂多语义条件下的分解能力——BABEL 的每条动作序列通常对应多个文本标签，要求模型同时理解多个动作语义并协调生成。

### 消融实验：组件贡献分析

Table 2 在 HumanML3D 上系统拆解了 Decomposed CoT Data Engine 与 RL Binding 奖励机制的各自贡献。

![[assets/figures/papers/paper_list_l15_Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforceme/figures/005_Table_2.jpg]]
*Table 2: Ablation study on HumanML3D Guo et al. (2022a). CoT, $R _ { \mathrm { s e m } }$ . and $R _ { \mathrm { m o t i o n } }$ denote Decomposed CoT Data Engine, the semantic similarity reward, and the motion similarity reward, respectively. Best results are highlighted in bold and the second best in underline

| 配置 | FID ↓ | R-Precision Top-1 ↑ |
|------|-------|---------------------|
| 仅 CoT（无 RL） | 0.530 | 0.340 |
| CoT + R_semantic | 0.252 | 0.489 |
| CoT + R_motion | 0.281 | 0.475 |
| **CoT + R_semantic + R_motion** | **0.201** | **0.515** |

**关键发现**：
- **单独使用 Decomposed CoT 效果最差**（FID 0.530，R-Precision Top-1 仅 0.340），甚至低于多数端到端基线。这说明仅靠推理规划而不施加显式的多模态对齐约束，模型无法将子动作规划有效映射为真实的运动序列。
- **语义相似度奖励（R_semantic）的增益大于运动相似度奖励（R_motion）**：CoT + R_semantic 的 R-Precision Top-1 为 0.489，高于 CoT + R_motion 的 0.475。这表明在文本-动作对齐任务中，跨模态语义对齐比动作自身的分布保真度更为关键。
- **三种组件联合使用时达到全局最优**：FID 0.201，R-Precision Top-1 0.515，验证了“推理分解 + 语义对齐 + 运动真实感”三者缺一不可的协同机制。

### 定性分析与分布外泛化

Figure 3 展示了 Motion-R1 与 MotionLLM（Wu et al., 2024）在分布内和分布外指令上的可视化对比。对于常规指令，两者均能生成合理动作；但对于分布外指令（如“沿无穷符号形状的路径缓慢行走”），MotionLLM 倾向于生成简化的直线或圆形轨迹，而 Motion-R1 能够捕捉“∞”形路径的结构特征。Figure 4 进一步展示了两个典型分布外案例：左侧为需要多步推理的复杂描述，右侧为需要语义理解的抽象描述，Motion-R1 在两种情况下均能生成结构合理、意图匹配的动作序列。

![[assets/figures/papers/paper_list_l15_Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforceme/figures/006_Figure_4.jpg]]
*Figure 4: Motion-R1 results on Out-of-Distribution prompts. Left: Complex caption with multistep reasoning. Right: Abstract caption requiring semantic understanding. Motion-R1 captures structure and intent in both cases*

### 失败模式与局限性

尽管 Motion-R1 在定量指标上表现突出，仍存在以下已知局限：

1. **CoT 分解质量依赖上游 LLM**：当输入指令模糊或高度抽象时，Decomposed CoT Data Engine 可能生成噪声或次优的子动作规划，进而影响最终动作质量。当前框架缺乏对 CoT 分解质量的自动评估与过滤机制。
2. **奖励函数设计的敏感性**：虽然 RL Binding 简化了优化流程，但 R_semantic 和 R_motion 的精心设计仍是性能的关键保障。消融实验中单独使用任一奖励均导致明显性能下降，说明奖励函数的组合方式对最终效果有显著影响。
3. **长序列生成的未验证性**：现有实验主要针对中等长度的动作序列，在更长或连续多任务生成场景下的效果尚待探索。

### 补充图表

![[assets/figures/papers/paper_list_l15_Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforceme/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of Motion-R1 on HumanML3D Guo et al. (2022a) and KIT-ML Plappert et al. (2016). The evaluations are conducted 20 times to obtain a 95% confidence interval. Best results are highlighted in bold and the second best in underline*

![[assets/figures/papers/paper_list_l15_Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforceme/figures/007_Table_3.jpg]]
*Table 3: Quantitative results of Motion-R1 on BABEL Punnakkal et al. (2021). The evaluations are conducted 20 times to obtain a 95% confidence interval. Best results are highlighted in bold and the second best in underline*



## 定位与知识库关联

### 1. 与基线方法的谱系关系

Motion-R1 处于文本驱动动作生成从**端到端映射**向**结构化推理**演进的交叉点。其设计直接回应了以下几条技术路线的瓶颈：

- **扩散模型路线**：以 **MDM** (Tevet et al., 2023) 为代表，将动作生成建模为条件扩散过程。该类方法在分布内数据上表现稳健，但缺乏对复杂时序因果关系的显式建模能力，面对分布外指令时泛化性不足。Motion-R1 通过引入分解式 CoT 推理，将高层指令展开为子动作序列，弥补了这一缺陷。

- **掩码建模路线**：以 **MoMask** (Guo et al., 2024) 为代表，采用掩码预测范式进行动作生成，在 HumanML3D 上曾保持 MM-Dist 最优（2.958）。Motion-R1 在此基础上通过 RL Binding 的多模态对齐奖励，将 MM-Dist 进一步降至 2.854，实现了 3.5% 的相对提升。

- **LLM 语义规划路线**：以 **MotionLLM** (Wu et al., 2024) 为代表，利用大语言模型进行高层语义规划再生成动作。Motion-R1 与此路线最接近，但关键区别在于：MotionLLM 仍依赖端到端的文本-动作映射，而 Motion-R1 的 Decomposed CoT Data Engine 自动生成结构化的 `<think>` → `<output>` → `<Motion>` 推理轨迹，使模型具备显式的逐步推理能力。Figure 3 的可视化对比表明，Motion-R1 在分布外指令上的生成质量显著优于 MotionLLM。

- **GPT 结合 VQ-VAE 路线**：以 **MotionGPT** (Jiang et al., 2023) 为代表，将动作 token 化后交由语言模型生成。Motion-R1 沿用了 VQ-VAE 动作分词器（Section 3.2），但在 LLM Backbone 之上叠加了 CoT 推理与 GRPO 强化学习优化，实现了从“生成动作 token”到“推理后生成动作 token”的范式升级。

- **RL-based 方法**：现有基于强化学习的动作生成方法（如 MotionCritic 等）通常需要训练偏好模型并依赖昂贵的人工标注。Motion-R1 的 RL Binding 机制通过格式奖励、运动相似度奖励、语义相似度奖励三种自动化信号，在无需人工标注的条件下实现了高效的多模态对齐。

### 2. 适用边界与局限

尽管 Motion-R1 在多个基准上取得了显著提升，其适用边界和潜在局限值得关注：

- **CoT 分解质量的依赖**：Decomposed CoT Data Engine 依赖通用 LLM 自动生成推理规划。当输入指令模糊或高度抽象时，LLM 可能生成噪声或次优的分解计划，进而影响下游动作质量。论文明确指出这一局限，并建议未来探索自适应过滤机制。

- **奖励函数设计的敏感性**：消融实验（Table 2）表明，单独使用 CoT 数据引擎时效果最差（R-Precision Top-1 仅 0.340，FID 为 0.530），而完整的 CoT + R_sem + R_motion 组合才能达到最优。这说明运动相似度奖励和语义相似度奖励的精心设计对最终性能至关重要，奖励权重或形式的调整可能导致性能波动。

- **动作序列长度的限制**：当前方法主要针对较短的动作序列进行验证（HumanML3D、KIT-ML、BABEL 均为短时动作数据集）。在更长时域或连续多任务生成场景下的效果尚未得到验证，这是一个有待探索的开放问题。

- **与人类主观偏好的对齐差距**：虽然语义相似度奖励通过共享嵌入空间实现了自动化对齐，但其与人类主观质量评价之间仍可能存在差距。论文将“探索交互式反馈机制以更紧密地结合人类偏好”列为未来工作方向。

### 3. 开放问题与未来方向

基于论文的分析与局限，以下开放问题值得后续研究关注：

1. **自适应 CoT 质量评估**：如何针对模糊或复杂指令自动评估 CoT 分解的质量，并自适应地过滤或修正低质量推理路径？

2. **奖励函数的人类偏好对齐**：能否将 RL 奖励函数与人类偏好更紧密地结合，例如通过轻量级的交互式反馈或偏好学习，实现更自然的主观质量对齐？

3. **长时域与多任务扩展**：本文方法在更长或连续多任务生成中的效果有待验证。如何将分解式 CoT 推理扩展到长时域动作规划，是一个具有实际价值的挑战。

4. **推理效率优化**：引入 CoT 推理和 GRPO 优化增加了计算开销。如何在保持推理质量的前提下降低推理成本，是实际部署中需要考虑的问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/Motion_R1_Enhancing_Motion_Generation_via_Decomposed_CoT_and_Reinforcement_Learning_Binding.pdf]]

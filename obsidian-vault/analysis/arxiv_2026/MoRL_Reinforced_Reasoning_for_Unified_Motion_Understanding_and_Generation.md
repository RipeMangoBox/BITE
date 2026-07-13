---
title: "MoRL: Reinforced Reasoning for Unified Motion Understanding and Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation.pdf
project_link: null
code_link: https://github
aliases:
- MCM
- MoRL
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 任务特定的可验证奖励设计（运动理解的语义对齐与推理连贯性、运动生成的物理合理性与文本-运动一致性）以及测试时的逐步推理与反思策略 Chain-of-Motion（CoM）。
primary_logic: 通过冷启动监督微调稳定输出格式，再利用基于组的强化学习（GRPO）优化多维度任务奖励，并在推理时引入规划、采样与迭代反思，可以显著提升统一运动模型的语义保真度、逻辑一致性和感知真实感。
claims:
- MoRL 在 HumanML3D 和 KIT-ML 的运动理解与生成指标上均显著超越现有统一模型及多数独立模型。
- 任务特定奖励的组合对性能至关重要，去除任一奖励均导致生成或理解指标退化。
- Chain-of-Motion 测试时推理策略显著提升了运动的物理性质和语义对齐。
- GRPO 优化器在稳定性与最终性能上优于 PPO 和 DPO。
---

# MoRL: Reinforced Reasoning for Unified Motion Understanding and Generation

> [!tip] 核心洞察
> 通过冷启动监督微调稳定输出格式，再利用基于组的强化学习（GRPO）优化多维度任务奖励，并在推理时引入规划、采样与迭代反思，可以显著提升统一运动模型的语义保真度、逻辑一致性和感知真实感。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoRL：面向统一运动理解与生成的增强推理 |
| 英文题名 | MoRL: Reinforced Reasoning for Unified Motion Understanding and Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [Code](https://github) · [paper](https://arxiv.org/abs/2602.14534) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoRL (with Chain-of-Motion) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D (motion understanding) 上，CIDEr 35.80 vs 33.74 (Motion Agent) (+2.06)；BLEU@1 56.99 vs 54.53 (Motion Agent) (+2.46)；ROUGE-L 51.83 vs 48.70 (Motion Agent) (+3.13)。
> - HumanML3D (motion generation) 上，R@1 (Top-1 retrieval precision) 0.527 vs 0.515 (Motion Agent) (+0.012)；MM Dist (multimodal distance) 2.790 vs 2.967 (Motion Agent) (-0.177)。
> - KIT-ML (motion generation) 上，R@1 0.779 vs ~0.7x (typical unified models) (competitive)。

## 概要

### 问题与瓶颈

现有统一运动模型（如 **MotionGPT** (Jiang et al., 2023)、**Motion Agent** (Wu et al., 2024)、**LaMP** (Li et al., 2025b)）虽然在运动理解与生成的联合建模上取得了进展，但普遍缺乏**逐步推理与测试时规划能力**。当面对复杂、多阶段或包含精细语义约束的运动任务时，这些模型容易产生语义不一致或物理不真实的输出——例如后空翻中失去连贯的起跳-旋转-落地轨迹，或风格化舞蹈中出现片段化姿态与方向错乱（Figure 1）。

核心瓶颈在于：现有方法将运动生成视为单次解码过程，未显式建模“感知-推理-执行”的认知链条，也缺乏针对任务特性的可验证反馈来驱动输出优化。

### 核心方法

**MoRL (Motion Reinforcement Learning)** 提出了一套统一的增强推理框架，从三个层面解决上述问题：

1. **任务特定的可验证奖励设计**：为运动理解设计语义对齐奖励与推理连贯性奖励，为运动生成设计物理合理性奖励与文本-运动一致性奖励，形成双头奖励体系。
2. **冷启动监督微调 + GRPO 强化学习**：先在大规模合成思维链数据集（MoUnd-CoT-140K / MoGen-CoT-140K）上进行监督微调以稳定输出格式，再采用基于组的策略优化（GRPO）进行多奖励联合优化。
3. **Chain-of-Motion (CoM) 测试时推理**：在推理阶段引入逐步规划、多候选采样与迭代反思策略，使模型能够在解码过程中自我修正。

### 方法谱系与知识库定位

MoRL 定位于**统一运动理解与生成**的交叉地带，其方法谱系可沿以下维度定位：

- **运动-语言模型**：继承自 MotionGPT 的离散运动令牌与语言模型融合范式，但在此基础上引入了完整的强化学习后训练管线。
- **强化学习与推理**：借鉴大语言模型领域的 RLVR（Reinforcement Learning with Verifiable Rewards）思想，将 GRPO 优化器与 Chain-of-Thought 推理策略迁移至运动模态。
- **统一模型对比**：相较于 Motion Agent 的纯监督范式，MoRL 新增了 RL 优化与测试时推理；相较于 **AvatarGPT** (Zhou et al., 2024) 的“全能”框架，MoRL 更聚焦于推理驱动的质量提升而非功能广度。

### 主要结果

在 HumanML3D 和 KIT-ML 两个标准基准上，MoRL 在运动理解与生成指标上均显著超越现有统一模型及多数独立模型（Table 1）：

- **运动理解**：CIDEr 达到 35.80（对比 Motion Agent 的 33.74），BLEU@1 达到 56.99，ROUGE-L 达到 51.83。
- **运动生成**：多模态距离（MM Dist）降至 2.790，为所有方法中最低；Top-1 检索精度（R@1）达到 0.527。
- **消融实验**（Table 2）证实：移除任一奖励组件均导致对应指标显著退化，移除 CoM 推理策略同样使全部指标下降，验证了各模块的必要性。
- **优化器对比**（Table 6）：GRPO 在最终性能与训练稳定性上均优于 PPO 和 DPO。

定性对比（Figure 1, Table 7-8）进一步显示，MoRL 在组合动作、长时序轨迹跟随和空间约束等复杂场景下，生成的运动序列在语义保真度与物理连贯性上均优于基线方法。用户研究（Figure 4）也表明 MoRL 获得了高度集中的高评分分布。



人体运动理解与生成是构建具身智能体与数字人的核心技术，涵盖运动描述、运动检索、文本驱动运动合成等双向任务。近年来，统一运动-语言模型试图在单一框架内同时处理理解与生成，代表性工作包括 **MotionGPT**（Jiang et al., 2023）、**Motion Agent**（Wu et al., 2024）以及 **LaMP**（Li et al., 2025b）。这些模型通过将连续运动序列离散化为运动令牌，与文本令牌一起送入预训练大语言模型进行自回归建模，在标准基准上取得了可观进展。

然而，现有统一模型存在一个关键瓶颈：**缺乏逐步推理与测试时规划能力**。当面对复杂、多阶段或精细语义的运动任务时——例如“先向前走三步，然后做一个后空翻，最后挥右手”——模型往往直接输出运动令牌或描述文本，中间没有显式的推理过程。这导致两个深层问题：

1. **语义不一致**：运动理解任务中，模型可能遗漏细粒度动作细节，或产生与输入运动序列不匹配的描述。
2. **物理不真实**：运动生成任务中，模型输出的运动序列可能出现关节角度违规、速度突变、轨迹断裂等问题，缺乏物理合理性。

以 Figure 1 中的后空翻生成为例，基线模型 **MotionLLM** 无法维持连贯的起跳-旋转-落地轨迹，导致身体朝向不稳定；而本文方法 MoRL 能够完成物理上合理的完整空翻。在 Wack 风格舞蹈生成中，MotionLLM 表现出不一致的旋转方向和碎片化的姿态，MoRL 则保持了连续的左右旋转和风格一致性。这些定性对比直观地揭示了缺乏推理能力对运动生成质量的影响。

从方法论角度看，现有统一运动模型的训练范式主要依赖监督微调，优化目标为通用的语言建模损失或简单的相似度分数。这种范式无法显式地鼓励模型关注物理约束和语义保真度，也难以在测试时对生成结果进行验证与修正。因此，本文的核心动机是：**将强化学习中的可验证奖励与测试时推理引入统一运动模型，通过任务特定的奖励设计和逐步规划策略，系统性地提升运动理解与生成的语义保真度、逻辑一致性和感知真实感。**



## 核心方法与创新机理

MoRL 的核心创新在于将**强化推理**引入统一运动理解与生成框架，通过三个相互协同的 changed slots 系统性地解决了现有统一运动模型在复杂语义任务中缺乏逐步推理与测试时规划能力的瓶颈。

### 1. 训练流程：从纯监督微调到冷启动 SFT + GRPO 强化学习

传统统一运动模型（如 **Motion Agent** (Wu et al., 2024)、**MotionGPT** (Jiang et al., 2023)）仅依赖监督微调（SFT），模型在训练时仅拟合静态的输入-输出映射，缺乏对输出质量的显式优化信号。MoRL 将训练流程重构为两阶段后训练范式：

- **冷启动 SFT**：首先在合成的大规模思维链数据集 MoUnd-CoT-140K 和 MoGen-CoT-140K 上进行监督微调，强制模型遵循包含推理轨迹的结构化输出格式，稳定输出分布，防止后续强化学习阶段的模式坍塌（Section 4.3）。
- **基于 GRPO 的强化学习**：在 SFT 基础上引入 Group Relative Policy Optimization（GRPO），通过组内奖励归一化与 KL 正则化优化模型策略。消融实验（Table 6）表明，GRPO 在 BERTScore（46.80）、CIDEr（35.80）、R@1（0.527）和 FID（0.203）四项核心指标上均优于 PPO 和 DPO，且训练方差最低，验证了其作为 RL 优化器在统一运动任务上的稳定性优势。

这一训练流程的关键因果机制在于：SFT 提供格式约束与语义先验，GRPO 则通过可验证奖励信号驱动模型在推理连贯性、语义对齐、物理合理性和文本-运动一致性四个维度上持续改进。

### 2. 奖励设计：从通用相似度到任务特定双头可验证奖励

现有方法通常使用单一的通用相似度分数（如文本-运动检索分数）作为训练信号，无法区分运动理解与生成任务的不同质量需求。MoRL 设计了**任务特定的双头奖励体系**（Section 4.4）：

**运动理解任务**的奖励组合：
- **语义对齐奖励** $R_{\mathrm{sem}} = \cos(E_{\mathrm{text}}(\hat{a}), E_{\mathrm{text}}(a))$：约束生成描述与参考描述在文本编码器下的余弦相似度。
- **推理连贯性奖励** $R_{\mathrm{coh}} = f_{\mathrm{NLI}}(\hat{r}, \hat{a})$：使用 NLI 模型（DeBERTa-v3-large）评估推理轨迹与最终答案之间的蕴含概率，确保推理逻辑自洽。

**运动生成任务**的奖励组合：
- **物理合理性奖励** $R_{\mathrm{phys}} = -\lambda_{1} \cdot L_{\mathrm{joint}}(\hat{m}) - \lambda_{2} \cdot L_{\mathrm{vel}}(\hat{m})$：加权惩罚关节角度违规（$\lambda_1=0.8$）和速度突变（$\lambda_2=0.2$），约束运动在物理上的可行性。
- **文本-运动一致性奖励** $R_{\mathrm{align}} = \cos(E_{\mathrm{text}}(t), E_{\mathrm{motion}}(\hat{m}))$：确保生成运动与输入文本在跨模态空间中的语义对齐。

消融实验（Table 2）揭示了各奖励组件的因果贡献：移除语义对齐奖励（w/o $R_{\mathrm{sem}}$）使 BERTScore 从 46.80 骤降至 44.10；移除物理合理性奖励（w/o $R_{\mathrm{phys}}$）使 FID 从 0.203 显著恶化至 0.285；移除任意单一奖励均导致对应维度的性能退化，验证了多维度奖励组合的必要性。

### 3. 测试时策略：从单次解码到 Chain-of-Motion 逐步推理与反思

基线统一模型在测试时仅执行单次自回归解码，面对复杂、多阶段运动任务时缺乏规划与纠错能力。MoRL 提出 **Chain-of-Motion（CoM）** 测试时推理策略（Section 4.5），引入三个关键机制：

- **逐步推理**：模型在生成最终输出前显式输出推理轨迹，将复杂任务分解为可验证的子步骤。
- **多候选采样**：并行采样多个候选推理-运动对，利用任务特定奖励函数进行质量评估。
- **迭代反思**：淘汰低质量候选，对高质量候选进行迭代修正，减少语义漂移和物理不合理运动。

消融实验（Table 2）显示，移除 CoM（w/o CoM）导致 FID 从 0.203 升至 0.220，BERTScore 同步下降。定性对比（Figure 1）进一步印证：在后空翻示例中，基线模型 MotionLLM 无法维持连贯的起跳-旋转-落地轨迹，身体朝向不稳定，而 MoRL 通过 CoM 完成了物理上合理的翻转；在 Wack 风格舞蹈中，MoRL 保持了连续的左右旋转和风格一致性，基线则出现旋转方向不一致和姿态碎片化的问题。

值得注意的是，CoM 的推理增益以约 2.1 倍的计算开销为代价（Table 5），这构成了该方法在实时场景中的主要工程限制。



MoRL 的整体框架围绕一个核心洞察展开：**通过冷启动监督微调稳定输出格式，再利用基于组的强化学习（GRPO）优化多维度任务奖励，并在推理时引入规划、采样与迭代反思，可以显著提升统一运动模型的语义保真度、逻辑一致性和感知真实感**。该框架将运动理解与运动生成统一在一个多模态大语言模型（MLLM）之内，以 Qwen3-4B-Instruct 为骨干初始化，并通过分层后训练管线实现从格式对齐到质量优化的渐进式提升。

### 管线概览

框架由五个核心模块串联构成，形成“离散化表示 → 格式冷启动 → 奖励驱动优化 → 测试时推理”的完整闭环：

1. **运动分词器（VQ-VAE）**：将连续的三维人体运动序列离散化为紧凑的码本令牌，使运动模态与文本模态在统一的离散令牌空间中自然对齐，同时大幅压缩序列长度以适应大语言模型的自回归生成范式。其量化过程为 $\hat{z}_i = \arg \min_{c_n \in \mathcal{C}} \| z_i - c_n \|_2^2$，训练损失为 $\mathcal{L}_{vq} = \mathcal{L}_{reconstruct} + \mathcal{L}_{commit} + \mathcal{L}_{embed}$（Section 4.2）。

2. **文本分词器（原生 LLM）**：直接继承自基座 LLM 的子词分词器，将自然语言描述映射为文本令牌，与运动令牌共享统一的表示空间。

3. **冷启动监督微调（Cold-Start SFT）**：在合成的大规模思维链数据集 MoUnd-CoT-140K 和 MoGen-CoT-140K 上进行监督微调，强制模型遵循“推理轨迹 + 简洁答案”的输出格式。这一步并非追求极致性能，而是为后续强化学习阶段提供稳定的输出结构基础，防止 RL 训练中的格式坍塌（Section 4.3）。

4. **强化学习阶段（GRPO + 任务特定奖励）**：这是框架的性能核心。采用基于组的策略优化（GRPO），在每组候选输出内进行奖励归一化 $\tilde{r}_i = \frac{r_i - \mu_r}{\sigma_r + \epsilon}$，并施加 KL 正则化以防止策略偏离过远。奖励设计采用**任务特定的双头结构**：
   - **运动理解**：语义对齐奖励 $R_{\mathrm{sem}} = \cos(E_{\mathrm{text}}(\hat{a}), E_{\mathrm{text}}(a))$ 确保生成描述与参考描述一致；推理连贯性奖励 $R_{\mathrm{coh}} = f_{\mathrm{NLI}}(\hat{r}, \hat{a})$ 使用 DeBERTa-v3-large 计算推理轨迹与答案之间的蕴含概率。
   - **运动生成**：物理合理性奖励 $R_{\mathrm{phys}} = -\lambda_{1} \cdot L_{\mathrm{joint}}(\hat{m}) - \lambda_{2} \cdot L_{\mathrm{vel}}(\hat{m})$ 惩罚关节角度违规和速度突变（$\lambda_1=0.8$，$\lambda_2=0.2$）；文本-运动一致性奖励 $R_{\mathrm{align}} = \cos(E_{\mathrm{text}}(t), E_{\mathrm{motion}}(\hat{m}))$ 确保生成运动与输入文本的跨模态对齐。

5. **Chain-of-Motion（CoM）解码**：在测试时引入显式的逐步推理与迭代反思策略。模型首先生成推理轨迹，随后采样多个候选的推理-运动对，利用任务特定奖励对其进行评估，丢弃低质量候选，对高质量候选进行迭代修正，最终输出语义连贯、物理合理的运动序列或描述。这一策略是 MoRL 在推理阶段区别于基线“单次解码”的关键差异点。

### 输入输出流

- **运动理解路径**：输入运动序列 → 运动分词器 → 运动令牌 → LLM 生成推理轨迹 → CoM 评估与反思 → 输出文本描述。
- **运动生成路径**：输入文本描述 → 文本分词器 → 文本令牌 → LLM 生成推理轨迹与运动令牌 → CoM 评估与反思 → 运动解码器 → 输出运动序列。

### 关键设计决策的因果逻辑

框架设计的每一处关键决策都指向真实瓶颈——**现有统一运动模型缺乏逐步推理和测试时规划能力，在面对复杂、多阶段或精细语义的运动任务时容易产生语义不一致或物理不真实的输出**。冷启动 SFT 解决输出格式的稳定性问题，为 RL 提供可优化的结构基础；GRPO 与任务特定奖励直接针对语义保真度和物理合理性进行梯度信号设计；CoM 则在测试时弥补了单次解码的规划缺陷，通过采样-评估-反思的闭环机制显著降低了语义漂移和物理不可信运动的发生概率。消融实验（Table 2）证实，移除任一奖励组件或 CoM 策略均会导致对应指标的显著退化，验证了这一设计逻辑的因果有效性。

### 补充图表

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/003_Figure_3.jpg]]
*Figure 3: Overview of MoRL. Our framework unifies motion understanding and generation under a reinforcement learning paradigm. Motion and text inputs are tokenized into a shared representation space. A hierarchical posttraining pipeline first applies SFT on large-scale synthetic CoT datasets to align motion sequences with reasoning traces and concise descriptions, then employs reinforcement learning with verifiable rewards (RLVR) to refine outputs, enhancing semantic alignment, reasoning coherence, physical plausibility, and text–motion consistency. At inference, the Chain-of-Motion (CoM) decoding strategy enables step-by-step reasoning and reflection, improving both motion understanding and perceptu...*



### 运动分词器（VQ-VAE）

MoRL 将连续的三维人体运动序列映射为离散的码本令牌，以适配大语言模型的自回归生成范式。该运动分词器基于 VQ-VAE 架构，包含编码器、码本和解码器三个部分。编码器将运动序列 $m$ 映射为连续潜变量序列 $\{z_i\}$，随后每个潜变量被量化为码本 $\mathcal{C} = \{c_1, c_2, \dots, c_N\}$ 中欧氏距离最近的离散码：

$$
\hat{z}_i = \arg \min_{c_n \in \mathcal{C}} \| z_i - c_n \|_2^2
$$

解码器则从量化后的表示 $\{\hat{z}_i\}$ 重建原始运动序列。整个 VQ-VAE 的训练目标由三项损失复合而成：

$$
\mathcal{L}_{vq} = \mathcal{L}_{reconstruct} + \mathcal{L}_{commit} + \mathcal{L}_{embed}
$$

其中 $\mathcal{L}_{reconstruct}$ 为重建损失，约束解码输出与原始运动一致；$\mathcal{L}_{commit}$ 为码本提交损失，鼓励编码器输出接近所选码本向量；$\mathcal{L}_{embed}$ 为嵌入损失，直接优化码本向量本身。这一离散化不仅压缩了运动序列长度，还使运动令牌与文本令牌在统一的离散空间中自然对齐。

### 文本分词器

文本分词器直接继承自基座大语言模型 Qwen3-4B-Instruct，将自然语言描述映射为子词令牌序列。运动令牌与文本令牌在嵌入层后被拼接送入统一的 Transformer 骨干网络进行联合建模。

### 冷启动监督微调（Cold-Start SFT）

在强化学习阶段之前，模型首先在合成的思维链数据集上进行监督微调。该阶段使用 MoUnd-CoT-140K（运动理解）和 MoGen-CoT-140K（运动生成）两个大规模数据集，强制模型遵循特定的推理格式：先输出逐步推理轨迹，再给出最终答案或运动序列。冷启动 SFT 的核心作用是稳定输出格式，防止后续强化学习阶段出现模式崩溃。

### 任务特定奖励函数

强化学习阶段的核心在于四类可验证奖励的设计，分别针对运动理解与运动生成的不同质量维度。

**语义对齐奖励**（运动理解）衡量生成描述 $\hat{a}$ 与参考描述 $a$ 在文本编码器 $E_{\text{text}}$ 下的语义相似度：

$$
R_{\mathrm{sem}} = \cos(E_{\text{text}}(\hat{a}), E_{\text{text}}(a))
$$

**推理连贯性奖励**（运动理解）评估推理轨迹 $\hat{r}$ 与最终答案 $\hat{a}$ 之间的逻辑蕴含关系，使用 NLI 模型 $f_{\mathrm{NLI}}$（默认 DeBERTa-v3-large）计算蕴含概率：

$$
R_{\mathrm{coh}} = f_{\mathrm{NLI}}(\hat{r}, \hat{a})
$$

**物理合理性奖励**（运动生成）通过惩罚关节角度违规和速度突变来约束生成运动的物理真实性：

$$
R_{\mathrm{phys}} = -\lambda_{1} \cdot L_{\mathrm{joint}}(\hat{m}) - \lambda_{2} \cdot L_{\mathrm{vel}}(\hat{m})
$$

其中 $L_{\mathrm{joint}}$ 检测生成运动 $\hat{m}$ 中超出人体生理极限的关节角度，$L_{\mathrm{vel}}$ 惩罚相邻帧之间的速度跳变。权重设置为 $\lambda_{1}=0.8$，$\lambda_{2}=0.2$。

**文本-运动一致性奖励**（运动生成）衡量输入文本 $t$ 与生成运动 $\hat{m}$ 在跨模态编码器下的对齐程度：

$$
R_{\mathrm{align}} = \cos(E_{\text{text}}(t), E_{\mathrm{motion}}(\hat{m}))
$$

### GRPO 优化与奖励归一化

MoRL 采用基于组的强化学习（GRPO）进行策略优化。在每组内，从当前策略采样多个候选输出，计算各自的奖励后，对组内奖励进行标准化以稳定训练：

$$
\tilde{r}_i = \frac{r_i - \mu_r}{\sigma_r + \epsilon}
$$

其中 $\mu_r$ 和 $\sigma_r$ 分别为组内奖励的均值和标准差，$\epsilon$ 为防止除零的小常数。标准化后的奖励结合 KL 散度正则项构成最终优化目标，约束策略更新幅度。

### Chain-of-Motion（CoM）测试时推理

在推理阶段，CoM 策略引入显式的逐步推理与迭代反思机制。模型首先生成推理轨迹，然后基于该轨迹采样多个候选输出（理解任务为描述文本，生成任务为运动序列）。每个候选输出通过任务特定奖励进行评估：理解任务使用推理-答案连贯性，生成任务使用语义对齐与物理合理性。低质量候选被直接丢弃，高质量候选则进入迭代反思环节，通过多轮修正减少语义漂移和物理不合理运动。



## 实验与关键发现

### 主实验结果

MoRL 在 HumanML3D 和 KIT-ML 两个标准基准上，对运动理解与运动生成任务进行了统一评估。Table 1 汇总了与现有统一模型及独立模型的主要对比结果。

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/004_Table_1.jpg]]
*Table 1: Comparison of motion generation and motion understanding on HumanML3D and KIT-ML. Highlights indicate the unified model, bold represent the best results within the unified model. Results marked with ∗ are reproduced by MotionGPT (Jiang et al., 2023) and Lyu et al. (Lyu et al., 2025), and are computed with unprocessed ground truth texts for linguistic metrics*

在 **HumanML3D 运动理解**任务上，MoRL 在所有语言指标上均显著超越统一基线模型 **Motion Agent**（Wu et al., 2024）：CIDEr 达到 35.80（+2.06），BLEU@1 达到 56.99（+2.46），ROUGE-L 达到 51.83（+3.13）。这一提升表明，任务特定的语义对齐奖励与推理连贯性奖励的组合，有效增强了模型对运动语义的细粒度捕捉与描述能力。

在 **HumanML3D 运动生成**任务上，MoRL 取得了所有方法中最低的 MM Dist（2.790），相比 Motion Agent 的 2.967 降低了 0.177，同时 R@1 提升至 0.527（+0.012）。MM Dist 的显著降低说明生成的运动与对应文本在跨模态空间中的对齐程度更高，而 R@1 的提升则反映了检索精度的增强。在多样性指标（Div）上，MoRL 达到 9.701，保持了有竞争力的生成多样性。

在 **KIT-ML** 数据集上，MoRL 同样展现出竞争力：运动生成的 R@1 达到 0.779，在统一模型中表现突出。值得注意的是，部分基线结果（标记 ∗ 的行）由第三方在未处理原文本的条件下重现，确保了语言指标的可比性。

### 消融实验分析

Table 2 的消融实验系统验证了各奖励组件与 Chain-of-Motion（CoM）推理策略的独立贡献。

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/006_Table_2.jpg]]
*Table 2: Ablation study of MoRL on HumanML3D*

**奖励组件的必要性**：
- 移除语义对齐奖励（w/o $R_{\text{sem}}$）导致 BERTScore 从 46.80 骤降至 44.10，CIDEr 从 35.80 降至 34.05，证实语义奖励对理解质量的核心作用。
- 移除推理连贯性奖励（w/o $R_{\text{coh}}$）使 ROUGE-L 降至 49.10，说明推理轨迹与最终答案之间的逻辑一致性是高质量理解的关键。
- 移除物理合理性奖励（w/o $R_{\text{phys}}$）使 FID 从 0.203 显著恶化至 0.285，这是所有消融中 FID 退化最严重的一项，表明物理约束对生成真实感运动的决定性影响。
- 移除文本-运动一致性奖励（w/o $R_{\text{align}}$）使 R@1 降至 0.492，MM Dist 变差，验证了跨模态对齐奖励对生成语义准确运动的必要性。

**Chain-of-Motion 的贡献**：
移除 CoM（w/o CoM）导致所有指标全面退化：FID 升至 0.220，BERTScore 下降。这证实测试时的逐步推理、多候选采样与迭代反思策略，对提升运动的物理性质与语义对齐具有不可替代的作用。

### 奖励设计与优化策略对比

**奖励设计对比**（Table 3）：在 HumanML3D CMS 子集上，不同奖励组合的对比显示，同时使用物理合理性奖励与文本-运动一致性奖励的组合取得了最佳生成效果，验证了多维度奖励协同设计的有效性。

**NLI 模型选择**（Table 4）：对比不同 NLI 模型作为 $f_{\text{NLI}}$ 的效果，DeBERTa-v3-large 提供了最低的奖励方差，意味着更稳定的 RL 更新过程，同时在下游 BLEU 和 FID 指标上带来了最大增益。

**优化策略对比**（Table 6）：在相同设置下，GRPO 在所有指标上均优于 PPO 和 DPO——BERTScore 46.80、CIDEr 35.80、R@1 0.527、FID 0.203，且训练方差最低。这表明 GRPO 的组内归一化机制在运动领域的 RL 训练中提供了更优的稳定性与收敛效果。

### 推理效率

Table 5 报告了单次解码与 CoM 的端到端推理效率。CoM 由于需要采样多个候选并进行迭代反思，引入了约 2.1 倍的额外延迟，吞吐量相应下降。这是测试时推理策略固有的计算代价，对实时应用场景构成限制。

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/008_Table_5.jpg]]
*Table 5: End-to-end inference efficiency of single-pass decoding vs. CoM. Latency (Lat.) is measured per sample. Throughput (Thru.) is computed at batch size 32*

### 定性分析与失败模式

**Figure 1** 的定性对比直观展示了 MoRL 相对于 MotionLLM 的优势：在后空翻示例中，MotionLLM 无法维持连贯的起跳-旋转-落地轨迹，导致身体朝向不稳定，而 MoRL 完成了物理上合理的翻转；在 Wack 风格舞蹈中，MotionLLM 表现出不一致的旋转方向和碎片化姿态，MoRL 则保持了从左到右的连续旋转与风格一致性。

**Table 7 和 Table 8** 进一步展示了序列化动作、轨迹跟随、长序列组合动作及空间约束等复杂提示下的生成对比，MoRL 在这些场景中均表现出更强的语义忠实度和运动连贯性。

**用户研究**（Figure 4）的评分分布显示，MoRL 在整体质量、语义对齐和物理真实感三个维度上均获得最高评分，与定量指标的趋势一致。

### 已知局限

尽管 MoRL 在标准基准上表现优异，仍存在以下局限：
1. **推理开销**：CoM 的测试时推理引入约 2.1 倍延迟，对实时应用需进一步优化。
2. **物理奖励的覆盖范围**：当前物理合理性奖励（关节角度违规惩罚与速度突变惩罚）相对简单，难以涵盖所有运动风格及细微的接触、交互动力学。
3. **泛化性未验证**：实验仅在 HumanML3D 和 KIT-ML 上进行，模型在更复杂场景（如人-物交互、群体运动）下的表现尚不明确，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/001_Figure_1.jpg]]
*Figure 1: Visualization comparisons with MotionLLM. In the backflip example, MotionLLM fails to maintain a coherent takeoff-rotation-landing trajectory, resulting in unstable body orientation, while MoRL completes a physically plausible flip. In the Wack-style dance, MotionLLM shows inconsistent rotation direction and fragmented poses, whereas MoRL preserves continuous left-to-right rotation and stylistic coherence*

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/010_Table_6.jpg]]
*Table 6: Comparison of different optimization strategies under identical settings. GRPO provides the best overall performance and training stability*

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/005_Table_3.jpg]]
*Table 3: Comparison of different reward designs on the CMS of HumanML3D. All methods share the same backbone and training setup, differing only in the reward used during motion generation*

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/007_Table_4.jpg]]
*Table 4: Comparison of NLI models used as*

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/009_Figure_4.jpg]]
*Figure 4: Results of user study*

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/012_Table_7.jpg]]
*Table 7: Qualitative comparison (Part I)*

![[assets/figures/papers/paper_list_l1840_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generatio/figures/013_Table_8.jpg]]
*Table 8: Qualitative comparison (Part II)*



## 定位与知识库关联

### 1. 统一运动模型的演进脉络

MoRL 的工作建立在统一运动理解与生成这一新兴范式之上。该范式的核心思想是将文本和运动序列映射到共享的离散令牌空间，利用单一的大语言模型骨干同时处理两类任务。早期代表性工作 **MotionGPT**（Jiang et al., 2023）率先将运动语言模型引入该方向，证明了共享令牌空间下统一建模的可行性。在此基础上，**Motion Agent**（Wu et al., 2024）进一步整合了运动理解与生成能力，成为 MoRL 在定量对比中的主要统一模型基线。更近期的 **LaMP**（Li et al., 2025b）代表了该方向的最新进展，而 **AvatarGPT**（Zhou et al., 2024）则尝试构建覆盖更广的全身运动框架。

然而，上述统一模型普遍缺乏显式的逐步推理机制。它们的输出通常由单次自回归解码产生，在面对需要多阶段规划或精细语义对齐的任务时，容易产生语义漂移或物理不合理的运动。MoRL 的独特贡献在于将强化学习中的可验证奖励（RLVR）与测试时推理策略引入统一运动模型，填补了这一空白。

### 2. 与独立运动生成模型的对比

除统一模型外，MoRL 还与一系列独立运动生成模型进行了比较，包括基于扩散的 **ReMoGPT**（Yu et al., 2025）、基于 GPT 的 **T2M-GPT**（Zhang and Zhang, 2023）以及基于掩码建模的 **MoMask**（Guo et al., 2024）。在 HumanML3D 基准上，MoRL 取得了 2.790 的最低多模态距离（MM Dist），显著优于上述独立模型，表明其在文本-运动语义对齐方面具有竞争力。但需注意，独立生成模型通常在生成多样性（Div）和 FID 等指标上有专门优化，MoRL 作为统一模型，其核心优势在于跨任务的语义一致性，而非在每个单项指标上追求极致。

### 3. 技术增量与关键设计选择

MoRL 的技术增量可分解为三个相互耦合的组件，每个组件在消融实验中均被证明不可或缺：

- **冷启动监督微调（Cold-Start SFT）**：在引入 RL 之前，使用合成数据集 MoUnd-CoT-140K 和 MoGen-CoT-140K 强制模型遵循推理格式。这一阶段的作用是稳定输出分布，防止后续 RL 训练中的模式崩溃。若跳过此阶段直接进行 RL，模型可能产生格式混乱的输出，奖励信号将失去引导意义。

- **任务特定的可验证奖励设计**：这是 MoRL 的核心因果调节旋钮。理解任务使用语义对齐奖励 $R_{\mathrm{sem}}$ 和推理连贯性奖励 $R_{\mathrm{coh}}$，生成任务使用物理合理性奖励 $R_{\mathrm{phys}}$ 和文本-运动一致性奖励 $R_{\mathrm{align}}$。消融实验（Table 2）提供了清晰的因果证据：移除 $R_{\mathrm{sem}}$ 使 BERTScore 从 46.80 降至 44.10；移除 $R_{\mathrm{phys}}$ 使 FID 从 0.203 飙升至 0.285。这表明每个奖励组件都控制着特定维度的输出质量，且组件间不存在冗余。

- **Chain-of-Motion（CoM）测试时推理**：CoM 在推理阶段引入多候选采样与迭代反思机制。低质量候选被丢弃，高质量候选通过奖励评估进行精炼。消融实验显示，移除 CoM 导致 FID 升至 0.220，BERTScore 下降，证实了测试时规划对物理合理性和语义保真度的独立贡献。代价是约 2.1 倍的推理延迟（Table 5），这构成了实时应用的瓶颈。

在优化器选择上，GRPO 相比 PPO 和 DPO 表现出更低的训练方差和更优的最终性能（Table 6），这与其组内奖励归一化策略 $ \tilde{r}_i = \frac{r_i - \mu_r}{\sigma_r + \epsilon} $ 密切相关——该设计消除了不同提示难度带来的奖励尺度差异，稳定了策略梯度更新。

### 4. 适用边界与局限性

MoRL 的有效性边界受以下因素制约：

1. **数据分布约束**：实验仅在 HumanML3D 和 KIT-ML 两个标准数据集上验证，这些数据集以单人、无交互的日常动作为主。模型在复杂场景（如人-物交互、群体运动、接触密集型动作）下的泛化性尚不明确。物理合理性奖励 $R_{\mathrm{phys}}$ 仅惩罚关节角度违规和速度突变，难以捕捉细微的接触动力学或风格化运动约束。

2. **推理效率与实时性**：CoM 的 2.1 倍延迟增量使其难以直接部署于实时应用。Table 5 显示吞吐量在 batch size 32 时显著下降，这限制了高并发场景的适用性。

3. **奖励函数的可迁移性**：当前的规则化奖励依赖人工设计的阈值（如关节角度范围、速度变化容限）。将这些奖励推广到新的运动领域或风格时，需要重新校准参数，缺乏自适应机制。

4. **离散表示的物理粒度**：VQ-VAE 运动分词器将连续运动压缩为离散码，虽然降低了序列长度，但可能丢失细粒度的接触信号和连续物理约束。这在高精度物理仿真场景中可能成为瓶颈。

### 5. 开放问题

从 MoRL 的设计和局限出发，以下问题值得后续工作关注：

- **自适应奖励泛化**：能否通过元学习或奖励建模，使物理合理性奖励自动适应新的运动风格和领域，减少人工阈值调参？
- **推理效率优化**：能否通过模型压缩、推测解码或早期淘汰策略，将 CoM 的延迟降至接近单次解码的水平？
- **细粒度物理建模**：如何在离散运动令牌中显式编码接触力、关节扭矩等物理信号，以更好地建模人-环境交互？
- **多模态评估体系**：当前评估依赖文本相似度指标和运动统计量，缺乏对推理过程本身质量的直接度量。如何设计面向推理链的评估基准，是统一运动模型走向更复杂语义理解的关键。



## 原文 PDF

![[paperPDFs/arxiv_2026/MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation.pdf]]

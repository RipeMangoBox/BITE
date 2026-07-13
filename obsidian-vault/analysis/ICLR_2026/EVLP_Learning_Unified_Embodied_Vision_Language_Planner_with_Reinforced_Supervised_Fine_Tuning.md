---
title: "EVLP: Learning Unified Embodied Vision-Language Planner with Reinforced Supervised Fine-Tuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EVLP_Learning_Unified_Embodied_Vision_Language_Planner_with_Reinforced_Supervised_Fine_Tuning.pdf
project_link: null
code_link: null
openreview_forum_id: eJcCW9oNfH
aliases:
- EEVLP
- EVLP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "EVLP通过单步直接建模图像条件分布、双向动态感知预训练以及强化监督微调中的动态对齐奖励，统一了语言逻辑推理与视觉空间生成，显著提升了多模态规划的动态一致性与任务成功率。"
primary_logic: "将视觉生成建模为直接的条件分布（而非逐步生成），并采用强化学习策略梯度显式奖励动态一致性，同时通过最大似然约束保持分布稳定性，使得模型能够在统一的 Transformer 架构中高效地产生空间对齐的多模态计划。"
claims:
- "EVLP 在 LoHoRavens 的 6 项任务中均取得最高成功率，显著超越所有基线（包括最强多模态规划方法 PERIA）。"
- "消融实验表明，去除 Forward Dynamic 预训练（w/o FDM）或仅使用强化学习（RL-only）会导致任务成功率骤降或完全失败，证明动态建模与 RSFT 框架的必要性。"
- "RSFT 在提升动态一致性的同时保持了图像生成质量，而仅用 RL 会导致策略崩溃，验证了联合优化的有效性。"
- "LoHoRavens Stacking 上 Success Rate (%) = 79.4±7.9"
---

# EVLP: Learning Unified Embodied Vision-Language Planner with Reinforced Supervised Fine-Tuning

> [!tip] 核心洞察
> 将视觉生成建模为直接的条件分布（而非逐步生成），并采用强化学习策略梯度显式奖励动态一致性，同时通过最大似然约束保持分布稳定性，使得模型能够在统一的 Transformer 架构中高效地产生空间对齐的多模态计划。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EVLP：基于强化监督微调的统一具身视觉语言规划器 |
| 英文题名 | EVLP: Learning Unified Embodied Vision-Language Planner with Reinforced Supervised Fine-Tuning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eJcCW9oNfH) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | EVLP (Embodied Vision-Language Planner) |
| Dataset | LoHoRavens Stacking, LoHoRavens Sort, LoHoRavens Matching, LoHoRavens Letters Shape |

> [!tip] 效果简介
> - LoHoRavens Stacking 上，Success Rate (%) 为 79.4±7.9，对比 63.9±5.8 (PERIA)，变化 +15.5。
> - LoHoRavens Sort 上，Success Rate (%) 为 77.3±4.3，对比 65.0±6.4 (PERIA)，变化 +12.3。
> - LoHoRavens Matching 上，Success Rate (%) 为 82.5±6.1，对比 72.3±7.1 (PERIA)，变化 +10.2。

## 概要

具身智能体在复杂长时序操作任务中，需要同时进行语言推理与视觉空间想象。现有方法通常将文本规划与视觉生成分离处理，导致多模态计划不一致，且缺乏对动态状态转移的显式建模，难以保证长周期任务的成功率。

EVLP（Embodied Vision-Language Planner）针对上述瓶颈，提出了一种统一的具身视觉语言规划器。其核心洞察在于：将视觉生成建模为直接的条件分布 $x_{0:N} \sim p(\cdot|c)$，通过单步前向传播即可获得完整图像，避免了扩散模型的多步去噪或自回归模型的逐步预测；同时引入强化监督微调（RSFT），利用策略梯度显式奖励动态一致性，并以最大似然约束保持分布稳定性，从而在统一的 Transformer 架构中高效产生空间对齐的多模态计划。

在 LoHoRavens 基准的 6 项任务上，EVLP 均取得最高成功率，显著超越最强多模态基线 PERIA（平均提升约 12.8 个百分点）。消融实验进一步证实，前向动态预训练（FDM）和 RSFT 联合优化是方法有效性的关键支撑。



### 问题背景

具身智能体在开放世界中执行长时序操作任务时，需要同时具备语言推理与视觉想象能力——即理解高层指令的语义内涵，并在脑海中推演操作序列可能引发的视觉状态变化。这一能力对于机器人完成复杂多步任务至关重要：智能体不仅要规划“做什么”，还要预判“做完之后场景会变成什么样”，从而确保每一步操作的可行性与连贯性。

### 现有方法缺口

当前主流的具身规划方法可大致归为三类，但均存在结构性缺陷：

**语言规划范式**（如 **PAR**, Zhang et al., 2023；**EmbodiedGPT**, Mu et al., 2023b）依赖大语言模型或多模态大模型生成文本动作序列，但完全缺失视觉想象能力，无法验证动作序列在空间层面的合理性。

**视觉规划范式**（如 **SuSIE**, Black et al., 2023b；**CoTDiffusion**, Ni et al., 2024a）利用扩散模型生成视觉子目标图像，但缺乏显式的语言推理能力，难以处理需要语义理解的复杂指令。

**多模态规划范式**（如 **PERIA**, Ni et al., 2024b）尝试将语言规划与扩散模型生成相结合，但存在两个根本性瓶颈：

1. **多模态计划不一致**：文本推理与视觉生成在分离的模块中进行，缺乏统一的动态建模，导致语言动作与视觉子目标之间缺乏空间对齐，生成的图像可能与文本指令产生语义偏差。
2. **缺乏对动态状态转移的显式建模**：现有方法未将“动作—状态变化”这一因果链条作为核心学习目标，难以有效处理需要精确空间推理的长时序操作任务。

### 核心瓶颈与解决思路

**真实瓶颈**：现有的具身多模态规划方法未能统一文本推理与视觉想象，导致多模态计划不一致，且缺乏对动态状态转移的显式建模，难以有效处理长时序操作任务。

**核心洞察**：将视觉生成建模为直接的条件分布（而非逐步生成），并采用强化学习策略梯度显式奖励动态一致性，同时通过最大似然约束保持分布稳定性，使得模型能够在统一的 Transformer 架构中高效地产生空间对齐的多模态计划。

**因果调节变量**：EVLP 通过以下三个关键设计实现突破——单步直接建模图像条件分布、双向动态感知预训练、以及强化监督微调中的动态对齐奖励——统一了语言逻辑推理与视觉空间生成，显著提升了多模态规划的动态一致性与任务成功率。



## 核心方法与创新机理

EVLP 的核心创新在于通过三个关键设计，将具身规划中的语言推理与视觉想象统一到一个 Transformer 架构中，并显式建模动态状态转移，从而解决多模态计划不一致的根本瓶颈。

### 1. 单步直接视觉生成范式

传统视觉规划方法依赖扩散模型的多步去噪（如 **SuSIE**）或自回归模型的逐步 token 预测，每次采样需要 $T$ 次或 $N$ 次前向传播（Figure 2）。EVLP 将视觉生成重新定义为直接建模图像 token 的完整条件分布 $x_{0:N} \sim p(\cdot|c)$，使 LLM 在单次前向传播中即可生成完整图像。这一设计不仅将采样效率提升数个数量级（Table 6），更重要的是消除了自回归生成中因逐步预测引入的因果偏置和累积误差——消融实验中，将 EVLP 替换为自回归生成方式（EVLP-AR）导致 LPIPS 从 0.046 恶化至 0.197，且产生更多幻觉（Table 3 Exp. D）。

### 2. 双塔视觉编码架构

现有方法通常采用单一语义编码器（如 SigLIP）提取视觉特征，但这类高层语义表示会丢失操作任务所需的空间细节。EVLP 提出双塔视觉模块（Figure 1）：**SigLIP 语义编码器**负责提取高层语义信息，同时引入**可训练的低层空间编码器**补充细节特征。消融实验验证了这一设计的必要性：移除空间编码器（w/o En）使 LPIPS 从 0.046 升至 0.087，任务成功率从 67.6 降至 56.5（Table 2 Exp. B, Table 3 Exp. B）；而仅使用空间编码器、缺少语义编码器（w/o Se）则导致语言准确率从 87.0 骤降至 73.9（Table 2 Exp. C），证明两类信息对统一规划缺一不可。

### 3. 强化监督微调（RSFT）框架

传统监督微调（SFT）仅最小化分布 KL 散度，无法显式优化生成图像的动态一致性；纯强化学习（RL）虽能通过奖励函数对齐偏好，但缺乏分布约束会导致灾难性策略崩溃。EVLP 提出 RSFT 框架（Figure 3），将 SFT 的最大似然损失与 RL 的优势加权策略梯度损失联合优化：

$$\mathcal{L} = -\mathbb{E}_{(g, x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \mathcal{L}_{\mathrm{SFT}} + \lambda \cdot \mathcal{L}_{\mathrm{RL}} \right]$$

其中 $\mathcal{L}_{\mathrm{SFT}}$ 约束整体 token 分布（Equation 3），$\mathcal{L}_{\mathrm{RL}}$ 通过动态对齐奖励函数显式增强生成图像与语言动作之间的空间一致性（Equation 4）。这一联合设计的关键在于：SFT 提供分布稳定性，防止 RL 优化过程中策略偏离过远；RL 则通过采样多候选并加权优势的方式，在分布约束下实现偏好对齐。消融实验直接验证了该框架的必要性——仅使用 RL 而不加 SFT 正则化会导致完全失败（SR 0.0, LA 14.0），而 RSFT 在提升动态一致性的同时保持了图像生成质量（Table 2 Exp. G, Figure 4, Figure 6）。

### 4. 双向动态感知预训练

在进入 RSFT 微调之前，EVLP 通过两个互补的预训练任务建立对状态转移的基本认知：**逆动态任务（IDM）** 给定两帧观测图像预测中间语言动作，增强感知与动作推理能力；**前向动态任务（FDM）** 给定当前观测与语言动作预测下一帧图像，学习状态转移规律。消融实验表明，FDM 是多模态规划的核心使能因素——移除 FDM 导致成功率从 67.6 骤降至 26.8（Table 2 Exp. E），而移除 IDM 主要影响语言规划能力（Table 2 Exp. D）。这揭示了一个因果机制：视觉想象能力（由 FDM 赋予）是统一多模态规划的基础，缺少该能力时模型无法产生与语言计划空间对齐的视觉子目标。

**证据强度说明**：上述所有 changed slots 均有 Table 2/3 的系统消融实验支撑，置信度 ≥ 0.95。RSFT 与纯 RL 的对比（Exp. G）以及 FDM 移除实验（Exp. E）提供了最直接的因果证据，效应量极大（成功率变化超过 40 个百分点），排除了混淆因素。



![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_eJcCW9oNfH/figures/001_Figure_1.jpg]]
*Figure 1: Our overall framework diagram. In terms of the model architecture, we adopt a vision tower design that integrates understanding and generation. For image understanding, we combine SigLIP with a learnable spatial encoder, while for image generation, we introduce image tokens to achieve one-step generation. Regarding the training pipeline, we design a two-stage framework: dynamic perception pretraining (illustrated above) and reinforced supervised fine-tuning (illustrated below). The black arrows represent the forward process, while the red arrows indicate the backward process*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_eJcCW9oNfH/figures/002_Figure_2.jpg]]
*Figure 2: (1) Diffusion-based Model formulates image generation as $x _ { 0 : N } ^ { t - 1 } \sim$ p ( $\cdot$ | c , $x _ { 0 : N } ^ { t }$ ) . When sampling n samples from distribution p ( $\cdot$ | c ) , the model requires n $\times$ T forward passes, where T denotes the diffusion denoising steps. (2) Autoregressive-based Model formulates image generation as $x _ { 0 : N } ^ { t - 1 } \sim$ p ( $\cdot$ | c , $x _ { 0 : N } ^ { t }$ ) . When sampling n samples from distribution p ( $\cdot$ | c ) , the model requires n $\times$ N forward passes, where N represents the token count. (3) Our Model directly models p ( $\cdot$ | c ) , enabling the sampling of n samples with only one forward pass

EVLP 提出了一套统一的具身视觉语言规划框架，其核心设计动机源于一个关键瓶颈：现有方法未能有效统一文本推理与视觉想象，导致多模态计划不一致，且缺乏对动态状态转移的显式建模。为解决这一问题，EVLP 将视觉生成建模为直接的条件分布 $x_{0:N} \sim p(\cdot|c)$，并采用强化学习策略梯度显式奖励动态一致性，同时通过最大似然约束保持分布稳定性，从而在统一 Transformer 架构中高效产生空间对齐的多模态计划。

### 模型架构总览

EVLP 的整体架构围绕一个统一的 LLM Backbone 构建，该 Backbone 同时处理文本 token 与视觉 token，其核心由三个关键模块构成：

**双塔视觉编码器（Vision Tower）** 将图像理解与图像生成解耦。在理解侧，采用 SigLIP 提取高层语义特征，同时引入一个可训练的低层空间编码器（基于图像重建损失预训练）补充细节信息，以缓解纯语义编码器在操作任务中的系统性视觉盲区。在生成侧，基于 Open-MAGVIT2 的无查找量化器将 $256\times 256$ 的输入图像编码为 $16\times 16$ 的离散 token 序列，供 LLM 直接预测。

**统一 LLM Backbone** 通过可学习的图像 token 直接建模完整图像 token 序列的条件分布，实现单步生成——即一次前向传播即可获得完整图像，无需扩散模型的多步去噪或自回归模型的逐步 token 预测（Figure 2）。

### 两阶段训练流程

EVLP 的训练分为两个阶段（Figure 1），分别对应动态感知能力的建立与多模态规划的对齐优化：

**第一阶段：双向动态感知预训练。** 模型同时学习两个互补任务：逆动态任务（IDM）给定两帧观测图像 $x_t, x_{t+1}$，预测中间的语言动作 $a_t$，强化感知与动作推理的耦合；前向动态任务（FDM）给定当前观测 $x_t$ 与语言动作 $a_t$，生成下一帧图像 $x_{t+1}$，学习状态转移的视觉规律。两个任务的损失函数分别为：

$$\mathcal{L}_{\mathrm{Inverse~Dynamic}} = - \mathbb{E}_{(x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \frac{1}{L} \sum_{i=1}^{L} \log P(a_t^{(i)} \mid a_t^{(<i)}, x_t, x_{t+1}; \theta) \right]$$

$$\mathcal{L}_{\mathrm{Forward~Dynamic}} = - \mathbb{E}_{(x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \log P(x_{t+1}^{(0:N)} \mid x_t, a_t; \theta) \right]$$

消融实验表明，FDM 的移除会导致多模态规划几乎完全失效（成功率从 67.6 骤降至 26.8），凸显了该模块对动态建模的核心作用（Table 2, Exps. D, E）。

**第二阶段：强化监督微调（RSFT）。** 在 SFT 初始化后，RSFT 联合最大似然损失与优势加权的策略梯度损失进行优化。SFT 损失联合估计动作序列与下一帧图像 token 的条件对数似然：

$$\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(g, x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \frac{1}{L} \sum_{i=1}^{L} \log P(a_t^{(i)} \mid a_t^{(<i)}, g, x_t; \theta) + \log P(x_{t+1}^{(0:N)} \mid g, x_t, a_t^{0:L}; \theta) \right]$$

RL 损失利用单步生成可独立采样多个样本的特性，通过动态对齐奖励计算优势 $A_k$，对高奖励样本进行加权：

$$\mathcal{L}_{\mathrm{RL}} = -\mathbb{E}_{(g, x_t, a_t) \sim \mathcal{D}, x_{t+1}^k \sim P(\cdot | g, x_t, a_t; \theta)} \left[ \frac{1}{K} \sum_{k=1}^{K} A_k \cdot \log P(x_{t+1}^k \mid g, x_t, a_t^{0:L}; \theta) \right]$$

最终 RSFT 总损失为两者的加权组合：

$$\mathcal{L} = -\mathbb{E}_{(g, x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \mathcal{L}_{\mathrm{SFT}} + \lambda \cdot \mathcal{L}_{\mathrm{RL}} \right]$$

这一设计的关键在于：SFT 项约束整体分布不偏离专家数据，RL 项通过动态对齐奖励显式优化空间一致性。若仅使用 RL 而不加 SFT 正则化，模型会发生灾难性策略崩溃（成功率 0.0，语言准确率 14.0），验证了联合优化的必要性（Table 2, Exp. G）。RSFT 在提升动态一致性的同时保持了图像生成质量（Figure 4, Table 2, Figure 6）。

### 输入输出流与模块关系

在推理阶段，给定高层目标指令 $g$ 与当前观测图像 $x_t$，双塔视觉编码器提取多尺度视觉特征，LLM Backbone 同时输出语言动作序列 $a_t^{0:L}$ 与下一帧子目标图像 token $x_{t+1}^{(0:N)}$。生成的子目标图像随后传递给基于 CLIPort 的低层策略，该策略根据当前观测、指令嵌入和子目标图像预测底层动作：

$$\mathcal{L}_{\mathrm{action}} = \sum_{t=1}^{T} \| \widehat{\boldsymbol{a}}_{t} - p_{\psi}(\boldsymbol{a}_{t} | \boldsymbol{o}_{t}, \boldsymbol{e}_{t}, \boldsymbol{x}_{t}) \|_{2}$$

整个 pipeline 形成了“高层多模态规划 → 低层动作执行”的层级结构，语言推理与视觉生成在统一的 Transformer 中完成，避免了模态间不一致的问题。

### 与其他 RL 方法的差异

Table 7 对比了 RSFT 与 GPG、GRPO-onpolicy 等 RL 方法的差异。GPG 无分布约束，GRPO-onpolicy 通过 KL 散度惩罚约束与参考策略的偏离，而 RSFT 通过最大似然项在特定数据集上约束分布，同时利用策略梯度优化动态对齐。这种设计使 RSFT 在保持训练稳定性的同时，有效提升了生成图像的动态一致性。



### 2.1 统一多模态生成架构

EVLP 基于统一的 Transformer 架构，将语言指令与视觉子目标图像纳入同一序列进行联合建模。其核心创新在于**采样高效的生成器**：模型直接建模图像 token 的完整条件分布 $x_{0:N} \sim p(\cdot | c)$，仅需一次前向传播即可获得完整图像，从根本上区别于扩散模型的多步去噪（需 $n \times T$ 次前向传播）和自回归模型的逐步 token 预测（需 $n \times N$ 次前向传播）（Figure 2）。

视觉模块采用**双塔设计**解耦理解与生成：

- **理解塔**：SigLIP 语义编码器提取高层语义信息，同时引入可训练的低层空间编码器（通过图像重建损失预训练）补充细节信息，弥补 SigLIP 的系统性视觉盲区。
- **生成塔**：基于 Open-MAGVIT2 的无查找量化器，将 $256 \times 256$ 图像编码为 $16 \times 16$ 的离散 token 序列，由统一 LLM 骨干通过可学习的图像 token 直接预测完整序列。

### 2.2 双向动态感知预训练

预训练阶段通过两个互补的动态预测任务，赋予模型连贯的推理与想象能力。

**逆动态任务（Inverse Dynamic Modeling, IDM）**：给定两帧观测图像 $x_t$ 和 $x_{t+1}$，模型预测中间的语言动作序列 $a_t$。该任务训练模型的感知与动作推理能力。

$$\mathcal{L}_{\text{Inverse Dynamic}} = - \mathbb{E}_{(x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \frac{1}{L} \sum_{i=1}^{L} \log P(a_t^{(i)} \mid a_t^{(<i)}, x_t, x_{t+1}; \theta) \right]$$

其中 $L$ 为动作序列的 token 长度，$a_t^{(i)}$ 为第 $i$ 个动作 token。

**前向动态任务（Forward Dynamic Modeling, FDM）**：给定当前观测 $x_t$ 与语言动作 $a_t$，模型直接生成下一帧图像 $x_{t+1}$。该任务学习状态转移规律，是后续多模态规划能力的核心基础。

$$\mathcal{L}_{\text{Forward Dynamic}} = - \mathbb{E}_{(x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \log P(x_{t+1}^{(0:N)} \mid x_t, a_t; \theta) \right]$$

其中 $x_{t+1}^{(0:N)}$ 表示下一帧图像的 $N$ 个离散 token。

### 2.3 强化监督微调（RSFT）

微调阶段的核心瓶颈在于：标准监督微调（SFT）仅最小化分布间的 KL 散度，无法显式优化生成图像与语言动作间的**动态一致性**；而纯强化学习（RL）虽能通过奖励函数对齐偏好，却缺乏分布约束，极易导致策略崩溃。RSFT 通过联合优化解决这一矛盾。

**SFT 损失**：联合估计动作序列和下一帧图像的条件对数似然，为规划能力提供初始化。

$$\mathcal{L}_{\text{SFT}} = -\mathbb{E}_{(g, x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \frac{1}{L} \sum_{i=1}^{L} \log P(a_t^{(i)} \mid a_t^{(<i)}, g, x_t; \theta) + \log P(x_{t+1}^{(0:N)} \mid g, x_t, a_t^{0:L}; \theta) \right]$$

其中 $g$ 为任务目标指令。

**RL 损失**：利用单步生成可独立采样多个样本的特性，通过优势加权的策略梯度优化动态对齐。奖励函数衡量生成图像与真实下一帧的动态一致性。

$$\mathcal{L}_{\text{RL}} = -\mathbb{E}_{(g, x_t, a_t) \sim \mathcal{D}, x_{t+1}^k \sim P(\cdot | g, x_t, a_t; \theta)} \left[ \frac{1}{K} \sum_{k=1}^{K} A_k \cdot \log P(x_{t+1}^k \mid g, x_t, a_t^{0:L}; \theta) \right]$$

其中 $K$ 为单次前向传播的采样数量，$A_k$ 为第 $k$ 个样本的优势函数值。

**RSFT 总损失**：通过加权系数 $\lambda$ 组合 SFT 与 RL 损失，实现分布约束下的偏好对齐（Figure 3）。

$$\mathcal{L} = -\mathbb{E}_{(g, x_t, a_t, x_{t+1}) \sim \mathcal{D}} \left[ \mathcal{L}_{\text{SFT}} + \lambda \cdot \mathcal{L}_{\text{RL}} \right]$$

**因果机制**：SFT 项通过最大似然约束模型整体分布，防止 RL 优化导致的分布偏移；RL 项通过动态对齐奖励显式强化生成图像与动作序列的空间一致性。消融实验证实，去除 SFT 正则化（RL-only）会导致灾难性策略崩溃（任务成功率降至 0.0，语言准确率降至 14.0），验证了联合优化的必要性（Table 2, Exp. G）。



## 实验与关键发现

### 主实验：LoHoRavens 基准任务成功率

EVLP 在 LoHoRavens 基准的全部 6 项任务上均取得最高成功率，显著超越所有基线方法（Table 1）。具体而言，在 Blocks 类任务中，EVLP 在 Stacking 上达到 79.4%±7.9，在 Sort 上达到 77.3%±4.3，在 Matching 上达到 82.5%±6.1；在 Letters 类任务中，Shape 为 75.3%±4.4，Orders 为 78.2%±7.3，Spell 为 81.8%±6.5。相较于次优的多模态规划方法 **PERIA**（Ni et al., 2024b），EVLP 在各任务上的绝对提升幅度达 +10.2% 至 +15.5%，且方差更小，表明其规划稳定性更强。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_eJcCW9oNfH/figures/006_Table_1.jpg]]
*Table 1: The evaluation of success rate between baselines and we report the mean and variance across 5 seeds*

从方法谱系来看，端到端模仿学习方法 **CLIPort**（Shridhar et al., 2022）因缺乏中间规划引导，在所有任务上表现最差（如 Stacking 仅 18.4%±3.2）。纯语言规划方法 **PAR**（Zhang et al., 2023）和 **EmbodiedGPT**（Mu et al., 2023b）虽能生成合理的语言指令，但缺少视觉子目标的空间约束，限制了低层策略的执行精度。纯视觉规划方法 **SuSIE**（Black et al., 2023b）和 **CoTDiffusion**（Ni et al., 2024a）则因缺乏语言推理能力，在需要语义理解的 Letters 任务上表现不佳。PERIA 作为多模态规划方法，联合了语言规划与扩散模型视觉生成，但受限于扩散模型的多步采样效率和模态间交互不足，未能充分对齐语言动作与视觉子目标。

### 消融实验：动态预训练与 RSFT 的核心作用

在 Meeting Preparation 任务上的消融实验（Table 2）揭示了各组件对规划性能的因果贡献：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_eJcCW9oNfH/figures/008_Table_2.jpg]]
*Table 2: Comparative analysis of task planning performance across different variants*

- **前向动态预训练（FDM）的移除**（Exp. E）导致成功率从 67.6% 骤降至 26.8%，语言准确率（LA）从 87.0% 降至 47.0%，证明 FDM 是模型学习状态转移规律、实现多模态一致规划的核心驱动力。FDM 通过预测下一帧图像 token 的条件分布，使 LLM 内化了物理世界的动态先验，这是后续 RSFT 阶段进行动态对齐优化的基础。
- **逆动态预训练（IDM）的移除**（Exp. D）主要削弱了语言规划能力（LA 从 87.0% 降至 79.4%），但对成功率的影响相对温和（SR 降至 56.0%）。IDM 通过从两帧观测反推中间动作，增强了模型的感知与动作推理能力，但其贡献可部分被 SFT 阶段的监督信号弥补。
- **仅使用强化学习而不用 SFT 正则化**（Exp. G，RL-only）导致灾难性策略崩溃：成功率为 0.0%，语言准确率降至 14.0%。这表明虽然 RL 损失通过动态对齐奖励可引导模型生成空间一致的图像，但缺少最大似然约束会导致模型分布严重偏离原始数据分布，产生无意义的输出。RSFT 通过联合优化 SFT 损失与优势加权 RL 损失，在分布约束下实现了有效的偏好对齐。
- **空间编码器的移除**（Exp. B，w/o En）使成功率降至 56.5%，图像生成质量显著恶化（LPIPS 从 0.051 升至 0.087，Table 3 Exp. B），说明低层空间细节对操作任务中的精确物体定位和状态识别至关重要。
- **语义编码器的移除**（Exp. C，w/o Se）则严重损害语言理解能力（LA 从 87.0% 降至 73.9%），验证了 SigLIP 提取的高层语义信息对 LLM 语言推理的不可替代性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_eJcCW9oNfH/figures/009_Table_3.jpg]]
*Table 3: Comparative analysis of image generation performance across different variants*

### 图像生成质量消融

Table 3 聚焦于图像生成维度的消融分析。完整 EVLP 在 Meeting Preparation 上取得 LPIPS 0.046 和 SSIM 0.95 的最佳生成质量。关键发现包括：

- **自回归生成方式**（Exp. D，EVLP-AR）导致生成质量大幅下降（LPIPS 0.197 vs 0.046），且产生更多视觉幻觉。自回归模型逐 token 预测的因果偏置使其难以捕捉图像的全局结构，且累积误差随序列长度增加而放大。EVLP 的单步直接生成通过一次前向传播建模完整图像 token 的条件分布，避免了上述问题。
- **空间编码器**对生成质量的贡献（LPIPS 从 0.046 升至 0.087）大于语义编码器（LPIPS 升至 0.060），表明低层视觉细节对图像保真度的影响更为直接。

### 采样效率优势

EVLP 的单步生成范式在推理速度上具有数量级优势（Table 6）。在 1.5B 参数规模下，生成 1 张图像仅需 0.05 秒，而扩散模型（SuSIE）需 4.41 秒，自回归模型需 5.31 秒；生成 8 张图像时，EVLP 仅需 0.13 秒，扩散模型需 35.36 秒。当模型规模扩展到 7B 时，自回归模型的推理时间急剧增长至 21.37 秒（1 张）和 172.96 秒（8 张），而 EVLP 仅需 0.15 秒和 0.40 秒。这一效率优势源于 EVLP 直接建模条件分布 $x_{0:N} \sim p(\cdot|c)$，无需扩散模型的迭代去噪或自回归模型的逐 token 串行预测。

### 真实世界数据集验证

在基于 BridgeData v2 的真实世界机器人数据集上（Table 4），EVLP 在语言准确率（LA 0.78）和视觉一致性（LPIPS 0.11）两个维度上均超越 PERIA（LA 0.75, LPIPS 0.17）、SuSIE 和 EmbodiedGPT。值得注意的是，SuSIE 无法评估语言准确率（纯视觉规划），而 EmbodiedGPT 无法评估视觉生成质量（纯语言规划），凸显了统一多模态规划的必要性。Figure 5 的可视化结果进一步展示了 EVLP 在复杂真实场景下的规划质量。

### RSFT 的动态对齐效果

Figure 4 的定性对比显示，RSFT 生成的视觉子目标比传统 SFT 具有更精细的细节和更好的动态一致性。Figure 6 的训练过程奖励曲线表明，RSFT 在测试集上的累积奖励持续优于 SFT，验证了动态对齐奖励函数的有效性。此外，附录 Figure 7 展示了 RSFT 在不可压缩性和可压缩性两种奖励函数下均具有良好的收敛性，Figure 8 验证了 RSFT 对多样化奖励函数的适应性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_eJcCW9oNfH/figures/007_Figure_4.jpg]]
*Figure 4: Comparison of generation effects between RSFT and SFT shows that RSFT generates more finely detailed results with better dynamic consistency*

### 失败模式与局限

尽管 EVLP 在 LoHoRavens 上表现优异，其规划能力仍依赖于预先收集的专家演示数据，在分布外场景下的泛化能力尚未验证。此外，EVLP 依赖基于 CLIPort 的低层策略执行具体动作，该策略的性能瓶颈可能成为整体系统的上限。在真实机器人平台上的部署验证也有待开展，实际应用中的传感器噪声和物理交互约束可能引入额外挑战。



## 定位与知识库关联

### 1. 具身规划方法的演进脉络

具身多模态规划领域呈现出从端到端模仿学习向分层规划架构演进，再向统一多模态生成范式发展的清晰路径。

**端到端模仿学习**代表了早期范式，以 **CLIPort**（Shridhar et al., 2022）为典型代表。该方法直接将高层语言指令映射为低层操作动作，跳过了中间推理步骤。然而，这种端到端映射缺乏可解释的中间表示，在处理长时序、多步骤的复杂操作任务时性能显著下降——在 LoHoRavens Stacking 任务上仅取得 18.4% 的成功率（Table 1），验证了纯端到端方法在需要结构化推理的场景中的根本性局限。

**语言规划范式**通过引入大语言模型的推理能力来弥合高层指令与低层执行之间的鸿沟。**PAR**（Zhang et al., 2023）采用 VLM 报告器与 LLM 规划器的组合架构，将视觉感知与语言推理分离处理。**EmbodiedGPT**（Mu et al., 2023b）则进一步用更强的多模态大语言模型替代分立的 LLM+VLM 组合，实现了更紧密的模态交互。然而，这些方法仅输出文本形式的动作序列，缺乏对操作结果的视觉想象，导致规划过程与真实环境状态脱节。

**视觉规划范式**试图弥补上述缺陷，通过生成视觉子目标来引导操作执行。**SuSIE**（Black et al., 2023b）利用图像编辑扩散模型生成子目标图像，首次将视觉想象引入规划流程。**CoTDiffusion**（Ni et al., 2024a）在此基础上引入语义对齐模块，通过链式思维机制提升子目标生成的连贯性。但这些方法仅关注视觉生成，缺少显式的语言推理能力，难以处理需要语义理解的复杂指令。

**多模态规划范式**代表了当前的最前沿，试图同时输出语言动作和视觉子目标。**PERIA**（Ni et al., 2024b）联合语言规划与扩散模型生成视觉子目标，在 LoHoRavens 基准上取得了当时的最优结果（Stacking 63.9%）。然而，PERIA 仍然面临两个核心瓶颈：其一，扩散模型的多步去噪过程导致视觉生成效率低下；其二，语言与视觉两个模态之间缺乏显式的动态一致性约束，使得生成的文本动作与视觉子目标可能相互矛盾。

### 2. EVLP 的方法定位与核心差异

EVLP 在以下四个关键维度上对现有多模态规划方法进行了系统性改进：

**视觉生成范式的根本转变。** 现有方法普遍采用扩散模型（多步去噪）或自回归模型（逐步 token 预测）进行图像生成，每次采样需要 T 步或 N 步前向传播。EVLP 首次提出单步直接生成范式：LLM 直接建模图像 token 的完整条件分布 $x_{0:N} \sim p(\cdot | c)$，仅需一次前向传播即可获得完整图像（Section 2.1, Figure 2）。这一设计不仅将采样效率提升了数个数量级（Table 6），更避免了自回归方法中因逐步预测引入的因果偏置和累积误差——消融实验显示，采用自回归生成方式的 EVLP-AR 变体在图像保真度上显著下降（LPIPS 从 0.046 升至 0.197），且产生更多幻觉（Table 3）。

**视觉编码的双塔解耦设计。** 现有方法通常使用单一语义编码器（如 SigLIP）提取视觉特征，这导致低层空间细节信息的系统性丢失。EVLP 创新性地采用双塔结构：SigLIP 提取高层语义信息，同时引入可训练的低层空间编码器补充细节信息（Section 2.1）。消融实验证实了这一设计的必要性：去除空间编码器显著损害图像生成质量（LPIPS 从 0.046 升至 0.087）和任务规划成功率（从 67.6 降至 56.5），而去除语义编码器则导致语言规划能力大幅下降（LA 从 87.0 降至 73.9）（Table 2, Table 3）。

**双向动态感知预训练。** 现有方法的预训练任务通常局限于图像-文本描述或问答，缺乏对操作动态过程的显式建模。EVLP 设计了双向动态感知预训练范式：逆动态任务（给定两帧图像预测中间动作）增强感知与动作推理能力，前向动态任务（给定当前观测与动作生成下一帧图像）学习状态转移规律（Section 2.2, Equations 1-2）。消融实验揭示了这两个任务的差异化作用：移除逆动态预训练削弱了语言规划能力，而移除前向动态预训练则导致多模态规划几乎完全失效（SR 从 67.6 骤降至 26.8），凸显了前向动态建模在统一推理与想象中的核心地位（Table 2）。

**强化监督微调框架。** 现有方法仅依赖监督微调（SFT）进行训练，无法显式优化多模态规划中的动态一致性。EVLP 提出的 RSFT 框架联合最大似然损失（SFT）与策略梯度强化学习损失（RL），通过动态对齐奖励函数显式奖励生成图像与语言动作之间的空间一致性（Section 2.3, Equations 3-5）。关键的是，RSFT 并非简单地将 SFT 与 RL 叠加：仅使用 RL 而不用 SFT 正则化会导致灾难性策略崩溃（SR 降至 0.0，LA 降至 14.0），验证了最大似然约束在维持分布稳定性中的不可替代作用（Table 2）。RSFT 在提升动态一致性的同时保持了图像生成质量，而纯 RL 则导致策略崩溃（Figure 4, Figure 6）。

### 3. 适用边界与局限性

尽管 EVLP 在多个基准上取得了显著提升，其方法设计仍存在以下适用边界：

**数据依赖性。** EVLP 的训练和规划能力高度依赖于预先收集的专家演示数据集。双向动态预训练和 RSFT 均需要成对的（观测，动作，下一观测）三元组数据。当面临与训练分布显著不同的新环境或任务时，模型的泛化能力可能受限。这一局限在真实世界部署场景中尤为突出，因为真实环境的视觉多样性、物体属性和物理交互模式可能远超仿真数据的覆盖范围。

**仿真到真实的迁移鸿沟。** 当前 EVLP 的主要实验验证集中在仿真环境（LoHoRavens）和离线真实数据集（BridgeData v2）上，尚未在真实机器人平台上进行在线部署验证。真实应用中存在传感器噪声、动态环境变化、物理交互约束等挑战，这些因素可能影响视觉生成的质量和动态预测的准确性。

**低层策略耦合瓶颈。** EVLP 的高层规划输出（语言动作序列和视觉子目标）最终依赖于一个基于 CLIPort 的低层策略来执行具体操作动作。该低层策略的性能上限可能成为整体系统的瓶颈——即使高层规划完全正确，低层执行的失败也会导致任务失败。当前框架未对低层策略的鲁棒性进行显式建模或优化。

**奖励函数设计的敏感性。** 动态对齐奖励函数的定义对 RSFT 的性能有显著影响。当前设计（如不可压缩性奖励）可能需要针对不同任务特性进行人工调整，这限制了方法在多样化任务上的即插即用能力。尽管附录实验（Figure 7, Figure 8）展示了 RSFT 对多种奖励函数的适应性，但奖励函数的选择仍然是一个需要领域知识的工程决策。

### 4. 开放问题与未来方向

基于 EVLP 的方法设计和当前局限，以下开放问题值得进一步探索：

**在线适应与持续学习。** 如何减少 EVLP 对固定数据集的依赖，使其能够在新环境中通过少量交互实现在线适应？将 RSFT 框架扩展为在线强化学习范式，允许模型在真实操作过程中持续优化动态预测能力，是一个有前景的方向。

**真实机器人部署与系统评估。** 将 EVLP 部署到真实机器人平台上，并系统评估其在物理世界中的鲁棒性、操作效率和安全性，是验证方法实用价值的关键步骤。这需要解决视觉生成的实时性要求、低层策略的物理约束整合以及异常情况的检测与恢复等问题。

**奖励函数的自动化设计。** 是否可以将 EVLP 的单步生成能力与逆强化学习或偏好学习相结合，从专家演示中自动推断动态对齐奖励函数，从而减少人工奖励设计的需求？这将显著提升方法在新任务上的迁移效率。

**跨任务泛化能力。** EVLP 的统一多模态生成范式是否能在更广泛的具身任务（如视觉导航、人机交互、移动操作）中带来类似增益？探索该方法在超出桌面操作场景的多样化任务上的适用性，将有助于理解统一生成范式的泛化边界。

**多模态规划的理论理解。** 当前对为什么单步生成优于逐步生成、为什么前向动态预训练对多模态规划至关重要等问题的理解仍主要停留在经验层面。建立更深入的理论框架，分析多模态生成中的误差传播机制和动态一致性的数学性质，将有助于指导未来方法的设计。



## 原文 PDF

![[paperPDFs/ICLR_2026/EVLP_Learning_Unified_Embodied_Vision_Language_Planner_with_Reinforced_Supervised_Fine_Tuning.pdf]]

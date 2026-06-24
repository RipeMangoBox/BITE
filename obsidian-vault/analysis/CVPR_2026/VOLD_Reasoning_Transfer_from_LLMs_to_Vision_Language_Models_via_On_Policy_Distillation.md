---
title: "VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VOLD_Reasoning_Transfer_from_LLMs_to_Vision_Language_Models_via_On_Policy_Distillation.pdf
code_link: null
aliases:
- VOLD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过两阶段框架（SFT冷启动策略对齐 + 统一GRPO与在线策略蒸馏），利用纯文本教师模型在纯文本数据上指导VLM学生，将文本推理能力迁移至视觉任务，无需任何视觉推理数据。
primary_logic: 1）在线策略蒸馏在VLM学生自身生成的轨迹上运用文本教师的反向KL损失，与GRPO的稀疏奖励协同，大幅提升样本效率；2）冷启动SFT阶段对建立教师-学生的分布桥梁至关重要，若未对齐，在线蒸馏无法提供有效梯度信号，几乎无增益。
claims:
- VOLD在纯文本训练下，在MathVision上达到28.0%，显著超越使用图像训练的VLAA-Thinker (24.4%)和文本训练基线X-Reasoner (24.4%)。
- 当SFT数据与教师模型分布不一致时（使用原始MoT而非教师生成数据），在线策略蒸馏完全失效，性能与无蒸馏RL持平。而使用教师生成SFT数据后在线蒸馏带来显著提升。
- SFT步数不足（<3000步）时，学生模型无法从在线蒸馏中获益；随着SFT步数增加，蒸馏收益逐渐增大并趋于饱和。
- 奖励引导的KL掩码进一步提升了训练回报，最终奖励达0.58，高于无掩码的0.56和纯GRPO的0.51。
---

# VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation

> [!tip] 核心洞察
> 1）在线策略蒸馏在VLM学生自身生成的轨迹上运用文本教师的反向KL损失，与GRPO的稀疏奖励协同，大幅提升样本效率；2）冷启动SFT阶段对建立教师-学生的分布桥梁至关重要，若未对齐，在线蒸馏无法提供有效梯度信号，几乎无增益。

| 字段 | 内容 |
|------|------|
| 中文题名 | VOLD：通过在线策略蒸馏将大语言模型推理迁移至视觉语言模型 |
| 英文题名 | VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.23497) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VOLD |
| Dataset | MMMU-Pro, MathVision, MathVista, LogicVista |

> [!tip] 效果简介
> - MMMU-Pro (Vision) 上，Accuracy 32.0 vs 31.0 (XReasoner-3B) (+1.0)。
> - MathVision 上，Accuracy 28.0 vs 24.4 (XReasoner-3B) (+3.6)。
> - MathVista 上，Accuracy 61.9 vs 61.1 (XReasoner-3B) (+0.8)。

## 概述

视觉-语言模型（VLM）在复杂推理任务上的表现长期受限，其核心瓶颈并非模型架构本身，而在于**缺乏大规模、高质量的图像-文本推理训练数据**。文本推理数据资源丰富且可扩展，但模态差异使其难以直接用于VLM的推理训练。VOLD正是针对这一瓶颈提出的一类**跨模态推理迁移框架**：它利用纯文本大语言模型（LLM）作为教师，通过两阶段后训练流程，将文本推理能力迁移至VLM学生模型，全程无需任何视觉推理数据。

VOLD的核心设计围绕一个关键因果机制展开——**在线策略蒸馏与强化学习的协同**。具体而言，VOLD在第一阶段通过监督微调（SFT）将学生模型的输出分布与教师对齐，建立跨模态的“策略桥梁”；第二阶段则在学生自身生成的推理轨迹上，同时施加GRPO稀疏奖励和教师模型的反向KL蒸馏损失，形成统一的优化目标。这种设计使得蒸馏信号与RL探索方向一致，大幅提升了样本效率。消融实验揭示了一个决定性发现：**若SFT阶段未使用教师生成数据进行充分对齐，在线蒸馏几乎完全失效**——这验证了“先对齐、后蒸馏”的因果逻辑。

在纯文本训练条件下，VOLD在MathVision上达到28.0%，显著超越使用图像训练的VLAA-Thinker（24.4%）和文本训练基线XReasoner-3B（24.4%）；在LogicVista上以45.0%领先XReasoner-3B达3.9个百分点。训练动态曲线进一步显示，VOLD在视觉验证准确率和文本训练奖励上均持续高于纯GRPO，且差距随训练逐步扩大。此外，奖励引导的KL掩码策略仅对失败轨迹施加蒸馏损失，将最终训练奖励从纯GRPO的0.51提升至0.58。

VOLD的方法定位介于**推理蒸馏**与**在线策略优化**两条技术路线的交叉点。与仅使用静态SFT轨迹的方法（如XReasoner）不同，VOLD在RL阶段持续从教师获取在线梯度信号；与依赖图像-文本数据的RL方法（如VLM-R1、VLAA-Thinker）不同，VOLD完全在文本数据上完成推理能力的注入，并可进一步作为图像RL的优质初始检查点。

## 背景与动机

### 视觉-语言模型的推理瓶颈

视觉-语言模型（VLM）在复杂多模态推理任务上仍显著落后于纯文本大语言模型（LLM）。基础模型**Qwen2.5-VL-3B**在未经任何推理后训练时，于MathVision基准上仅取得21.9%的准确率，暴露了VLM在几何、数学和逻辑推理方面的根本性弱点。这一差距的核心瓶颈在于**大规模、高质量的图像-文本推理训练数据极度稀缺**——构建此类数据需要人工标注或复杂的合成流程，成本高昂且难以规模化。

相比之下，纯文本推理数据（如数学问题链、逻辑推理轨迹）资源丰富且可扩展。然而，由于模态差异，这些文本推理资源无法直接用于VLM的推理训练：文本教师模型生成的推理轨迹缺乏视觉锚定，学生VLM需要将抽象的文本推理模式映射到视觉输入上，这一跨模态迁移构成了技术挑战。

### 现有方法的局限

当前提升VLM推理能力的方法主要分为两条路径：

**图像-文本联合训练**：**VLM-R1**（Shen et al., 2025）和**VLAA-Thinker**等方法在图像-文本数据上进行强化学习（RL）训练。这类方法虽然直接，但受限于视觉推理数据的稀缺性。更关键的是，VLAA-Thinker的训练集与评估集存在约40%的重叠，其24.4%的MathVision准确率可能存在虚高。

**纯文本训练**：**XReasoner-3B**（Liu et al., 2025）探索了仅使用文本数据进行SFT+GRPO训练，在MathVision上达到24.4%。然而，该方法仅使用教师模型生成静态SFT轨迹，在RL阶段完全放弃了教师信号的引导，未能充分利用文本教师蕴含的推理知识。其与VLM-R1-Math的性能对比也因后者在MathVista上训练而缺乏公平性。

### VOLD的核心动机

本文的核心洞察是：**文本教师的推理能力可以通过在线策略蒸馏有效迁移至VLM，关键在于建立教师-学生之间的分布桥梁，并在学生自身探索轨迹上持续提供密集的梯度引导**。

VOLD框架基于以下三个动机设计：

1. **冷启动对齐的必要性**：SFT阶段使用教师模型生成的推理轨迹对VLM进行微调，使学生的输出分布与教师对齐。若跳过此阶段或使用分布不一致的数据（如原始MoT数据集），在线蒸馏将无法提供有效梯度信号，几乎无增益。

2. **在线策略蒸馏的样本效率**：在RL阶段，对VLM自身生成的轨迹施加教师模型的反向KL损失，将稀疏的二进制奖励与密集的token级引导相结合。这种设计使VLM在训练全过程中，视觉验证准确率和训练奖励均持续高于纯GRPO，且差距逐渐扩大。

3. **选择性模仿的掩码机制**：通过奖励引导的KL掩码，仅对失败轨迹（奖励=0）施加蒸馏损失，成功轨迹则跳过。这一机制保留了正确的推理策略，同时让教师仅在学生犯错时介入，最终训练奖励达0.58，高于无掩码的0.56和纯GRPO的0.51。

VOLD的最终目标是**在完全不使用任何视觉推理数据的前提下，使VLM的推理性能超越使用图像训练的方法**，从而验证文本到视觉的推理迁移范式的有效性。

## 核心创新

VOLD的核心创新在于**首次将在线策略蒸馏（On-Policy Distillation）引入视觉-语言模型的推理训练**，通过一个两阶段框架，使纯文本大语言模型（LLM）的推理能力能够有效迁移至VLM，全程无需任何视觉推理数据。相较于现有方法，VOLD在三个关键维度上实现了突破性改进：

### 1. 训练流程：从单阶段到两阶段冷启动对齐

现有VLM推理后训练方法通常采用单阶段流程——要么仅做SFT，要么直接在图像-文本数据上进行RL训练（如**VLM-R1**，Shen et al., 2025；**VLAA-Thinker**）。纯文本训练基线**X-Reasoner**（Liu et al., 2025）虽然也使用文本数据，但仅将SFT与GRPO简单组合，未引入蒸馏机制。

VOLD引入**两阶段后训练流水线**（Figure 2）：
- **阶段一（SFT冷启动）**：使用教师LLM生成的推理轨迹对VLM学生进行监督微调，使学生的输出分布与教师对齐。此阶段仅更新语言模型部分，视觉编码器保持冻结。
- **阶段二（统一RL与在线蒸馏）**：在纯文本数学问题上，同时施加GRPO的稀疏奖励信号和教师模型的反向KL蒸馏损失，形成密集的token级引导。

这一设计的关键洞察在于：**冷启动对齐是后续在线蒸馏生效的必要条件**。消融实验（Table 2）表明，当SFT数据与教师分布不一致时（如使用原始MoT数据集而非教师生成数据），在线策略蒸馏完全失效，性能与无蒸馏RL持平；而使用教师生成SFT数据后，在线蒸馏带来显著提升。

### 2. 优化目标：GRPO + 在线反向KL蒸馏 + 奖励掩码

标准GRPO的优化目标包含与旧策略的KL散度正则化项，用于约束策略更新幅度。VOLD对此进行了根本性改造：

- **将KL项替换为与教师策略的反向KL散度**：$$\mathcal{L}_{\mathrm{VOLD}}(\theta) = \mathcal{L}_{\mathrm{GRPO}}(\theta) + \beta \cdot \mathbb{E}_{q,\tau\sim\pi_\theta}\left[\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$ 其中$\pi_\phi$为教师策略，$\pi_\theta$为学生策略。该损失在学生自身生成的轨迹上计算，使教师能够在学生实际探索的路径上提供密集引导，而非仅在静态SFT数据上示范。

- **奖励引导的KL掩码**：进一步引入选择性模仿机制，仅对失败轨迹（奖励$r(\tau)=0$）施加蒸馏损失：$$\mathcal{L}_{\mathrm{VOLD-masked}}(\theta) = \mathcal{L}_{\mathrm{GRPO}}(\theta) + \beta \cdot \mathbb{E}_{q,\tau\sim\pi_\theta}\left[(1 - r(\tau))\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$ 成功轨迹跳过蒸馏，保留其正确推理策略，避免教师信号干扰已习得的能力。实验显示，掩码版本最终训练奖励达0.58，高于无掩码的0.56和纯GRPO的0.51（Figure 5）。

### 3. 训练数据模态：纯文本实现跨模态推理迁移

与**VLM-R1**和**VLAA-Thinker**依赖图像-文本配对数据进行RL训练不同，VOLD**完全在纯文本数据上训练**——仅使用数学问题文本和教师模型生成的推理轨迹。这一设计直接回应了核心瓶颈：视觉推理标注数据稀缺且昂贵，而文本推理资源丰富且可扩展。VOLD通过在线策略蒸馏机制，使文本教师能够在VLM学生处理文本数学问题时提供实时引导，而习得的推理能力可泛化至视觉推理任务。

实验结果表明，这一跨模态迁移策略极为有效：VOLD在MathVision上达到28.0%，不仅大幅超越纯文本训练基线X-Reasoner（24.4%），甚至优于使用图像训练的VLAA-Thinker（24.4%）；在LogicVista上达到45.0%，同样显著领先（Table 1）。这证明**蒸馏信号本身可以跨越模态边界**，文本教师的推理知识通过在线策略蒸馏被有效编码进VLM的语言模块，进而在视觉推理时被激活利用。

## 整体框架

VOLD 是一个两阶段后训练框架，旨在将纯文本大语言模型（LLM）中的推理能力迁移至视觉-语言模型（VLM），全程无需任何图像-文本推理训练数据。其核心设计理念是：通过**冷启动策略对齐**与**在线策略蒸馏**的协同，使文本教师模型能够在学生 VLM 自身生成的轨迹上提供密集的 token 级引导信号，从而将文本模态的推理能力有效迁移至多模态推理任务。

### 两阶段训练流程

VOLD 的完整训练流程如 Figure 2 所示，包含两个有序且相互依赖的阶段：

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/002_Figure_2.jpg]]
*Figure 2: VOLD training pipeline: VOLD is a two-stage process to instill reasoning capabilities into a student VLM using a text-only teacher. (Stage 1), the student’s policy is aligned with the teacher’s via SFT on a corpus of teacher-generated reasoning traces. (Stage 2), the student is trained with a unified on-policy objective that leverages the same rollouts to compute both a sparse reward for RL(GRPO) and a dense distillation loss against the teacher. This combined signal enhances reasoning without requiring any vision-based reasoning data. At Inference, the resulting student model can effectively reason over novel image-text prompts*

**阶段一：SFT 冷启动策略对齐**

在正式强化学习训练之前，VOLD 首先使用教师 LLM 在纯文本数学问题上生成的推理轨迹对 VLM 学生进行监督微调。该阶段的核心目标是使学生的输出分布与教师对齐，为后续在线蒸馏建立分布桥梁。SFT 损失函数为教师轨迹上的负对数似然：

$$\mathcal{L}_{\mathrm{SFT}}(\theta) = -\mathbb{E}_{(q,\tau^*)\sim\mathcal{D}_{\mathrm{teacher}}}\left[\sum_{t=1}^{|\tau^*|}\log\pi_\theta(y_t^*|q,y_{<t}^*)\right]$$

其中 $q$ 为纯文本问题，$\tau^*$ 为教师生成的完整推理轨迹（含最终答案），$\pi_\theta$ 为学生策略。值得注意的是，视觉编码器在整个训练过程中保持冻结，仅更新语言模型部分，这使得文本推理能力的迁移成为可能——视觉编码器仅在推理阶段提供图像特征，训练阶段完全依赖文本数据。

**阶段二：统一 RL 与在线策略蒸馏**

在策略对齐的基础上，VOLD 采用一个统一目标同时进行强化学习和在线知识蒸馏。该阶段的核心创新在于：**GRPO 的稀疏奖励与教师模型的反向 KL 蒸馏共享同一批学生生成的轨迹**，形成互补的优化信号。

GRPO 部分使用组相对策略优化，其损失函数为：

$$\mathcal{L}_{\mathrm{GRPO}}(\theta) = -\mathbb{E}_{q,\{\tau_i\}\sim\pi_{\theta_{\mathrm{old}}}}\left[\frac{1}{K}\sum_{i=1}^{K}\min\left(\rho_i(\theta)A_i,\mathrm{clip}(\rho_i(\theta),1-\epsilon,1+\epsilon)A_i\right)\right] + \beta\mathbb{D}_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}})$$

其中奖励为二值稀疏信号（$r(\tau) \in \{0, 1\}$），仅以最终答案的正确性作为评判标准。

在线策略蒸馏部分对学生的**自身生成轨迹**施加教师模型的反向 KL 散度：

$$\mathcal{L}_{\mathrm{RKL}}(\theta) = \mathbb{E}_{q,\tau\sim\pi_\theta}\left[\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$

其中 $\pi_\phi$ 为教师策略。与传统的离线蒸馏（使用教师预生成的静态轨迹）不同，在线策略蒸馏在学生的当前策略分布上进行，能够提供更精准的 token 级引导。

### 统一目标与奖励掩码

VOLD 的完整统一目标将上述两部分结合：

$$\mathcal{L}_{\mathrm{VOLD}}(\theta) = \mathcal{L}_{\mathrm{GRPO}}(\theta) + \beta\cdot\mathbb{E}_{q,\tau\sim\pi_\theta}\left[\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$

为进一步提升训练效率，VOLD 引入了**奖励引导的 KL 掩码**机制。其核心直觉是：对于已经成功的轨迹（$r(\tau)=1$），蒸馏信号可能干扰学生已形成的正确推理策略；而对于失败轨迹（$r(\tau)=0$），教师的密集引导则能有效纠正错误。掩码后的目标为：

$$\mathcal{L}_{\mathrm{VOLD-masked}}(\theta) = \mathcal{L}_{\mathrm{GRPO}}(\theta) + \beta\cdot\mathbb{E}_{q,\tau\sim\pi_\theta}\left[(1 - r(\tau))\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$

其中 $(1 - r(\tau))$ 项天然构成了一个掩码：仅在奖励为 0 时激活蒸馏损失。

### 模块关系与数据流

VOLD 的模块间关系可概括为以下数据流：

1. **输入**：纯文本数学问题 $q$（来自 orz-57k 等文本推理数据集）。
2. **教师模型**：在阶段一生成推理轨迹 $\tau^*$ 用于 SFT；在阶段二对学生的在线轨迹提供 token 级概率分布 $\pi_\phi(\cdot|h_t)$。
3. **学生模型**：在阶段一学习模仿教师轨迹；在阶段二从自身策略 $\pi_\theta$ 采样轨迹 $\tau$，同时接收 GRPO 的稀疏奖励和教师的密集蒸馏信号。
4. **输出**：训练后的 VLM 能够在未见过的图像-文本推理任务（如 MathVision、LogicVista）上进行有效推理，无需在训练期间接触任何视觉数据。

### 关键设计决策

- **冷启动的必要性**：消融实验（Table 2）表明，若 SFT 阶段使用的数据与教师分布不一致（如使用原始 MoT 数据而非教师生成数据），在线蒸馏完全失效。这一发现揭示了策略对齐是后续蒸馏生效的前提条件。
- **冻结视觉编码器**：训练全程冻结视觉编码器，使得文本推理能力的迁移不依赖于视觉特征的对齐，降低了训练复杂度并保持了视觉感知能力的相对稳定。
- **与 RL 算法的正交性**：VOLD 的在线蒸馏模块与具体的 RL 算法解耦，实验验证其同样适用于 GSPO（Figure 6），表明该框架具有良好的泛化性。

## 核心模块与公式推导

VOLD 是一个两阶段后训练框架，旨在将纯文本教师 LLM 的推理能力迁移至视觉-语言学生模型，全程无需任何视觉推理数据。其核心由以下模块构成：

### 阶段一：SFT 冷启动策略对齐

在进入强化学习之前，学生模型首先在教师生成的推理轨迹上进行监督微调。该阶段的目标是使学生的输出分布与教师对齐，为后续在线蒸馏建立“分布桥梁”——若跳过此步，学生与教师策略差异过大，反向 KL 梯度将无法提供有效信号。

SFT 损失函数为教师轨迹上的负对数似然：

$$\mathcal{L}_{\mathrm{SFT}}(\theta) = -\mathbb{E}_{(q,\tau^*)\sim\mathcal{D}_{\mathrm{teacher}}}\left[\sum_{t=1}^{|\tau^*|}\log\pi_\theta(y_t^*|q,y_{<t}^*)\right]$$

其中 $q$ 为纯文本数学问题，$\tau^*$ 为教师模型生成的完整推理轨迹（含思考过程与最终答案），$\pi_\theta$ 为学生策略。该阶段使用教师生成数据而非原始 MoT（Math of Thoughts）数据集，这一点至关重要——消融实验表明，使用原始 MoT 数据将导致策略失配，使后续在线蒸馏完全失效。

### 阶段二：统一 RL 与在线策略蒸馏

第二阶段将 GRPO 强化学习与在线策略蒸馏统一为单一优化目标。学生模型在纯文本数学问题上采样多条轨迹，同一条轨迹同时用于计算两个信号：

**GRPO 损失**（稀疏奖励）：采用组内相对优势估计，含重要性采样截断与 KL 正则化：

$$\mathcal{L}_{\mathrm{GRPO}}(\theta) = -\mathbb{E}_{q,\{\tau_i\}\sim\pi_{\theta_{\mathrm{old}}}}\left[\frac{1}{K}\sum_{i=1}^{K}\min\left(\rho_i(\theta)A_i,\mathrm{clip}(\rho_i(\theta),1-\epsilon,1+\epsilon)A_i\right)\right] + \beta\mathbb{D}_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}})$$

其中 $K$ 为每组采样轨迹数，$\rho_i(\theta)$ 为重要性比率，$A_i$ 为组内相对优势。奖励为二元值 $r(\tau) \in \{0, 1\}$——仅当模型生成的最终答案与标准答案完全匹配时给予正向奖励。

**在线策略蒸馏损失**（密集 token 级引导）：在学生自身生成的轨迹上计算教师策略与学生策略之间的反向 KL 散度：

$$\mathcal{L}_{\mathrm{RKL}}(\theta) = \mathbb{E}_{q,\tau\sim\pi_\theta}\left[\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$

其中 $\pi_\phi$ 为冻结的教师策略，$h_t$ 为到第 $t$ 步的历史上下文，$T$ 为轨迹长度。与标准 KL 散度不同，反向 KL 鼓励学生覆盖教师的高概率区域，更适合知识蒸馏场景。该损失的关键特性是**在线性**：它始终在学生当前策略采样的轨迹上计算，而非离线静态数据集，从而提供与当前探索状态适配的密集梯度信号。

**VOLD 统一目标**将两者结合：

$$\mathcal{L}_{\mathrm{VOLD}}(\theta) = \mathcal{L}_{\mathrm{GRPO}}(\theta) + \beta\cdot\mathbb{E}_{q,\tau\sim\pi_\theta}\left[\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$

其中 $\beta$ 控制蒸馏强度。GRPO 提供稀疏的“对/错”信号引导整体方向，在线蒸馏则提供 token 级的密集引导，加速策略收敛。

### 奖励引导的 KL 掩码

直接对所有轨迹施加蒸馏损失可能干扰已成功轨迹的推理策略。VOLD 引入奖励引导的掩码机制，仅对失败轨迹（$r(\tau)=0$）激活蒸馏损失：

$$\mathcal{L}_{\mathrm{VOLD-masked}}(\theta) = \mathcal{L}_{\mathrm{GRPO}}(\theta) + \beta\cdot\mathbb{E}_{q,\tau\sim\pi_\theta}\left[(1 - r(\tau))\sum_{t=1}^{T} D_{\mathrm{KL}}\left(\pi_\phi(\cdot|h_t)\|\pi_\theta(\cdot|h_t)\right)\right]$$

因子 $(1 - r(\tau))$ 构成天然掩码：成功轨迹跳过蒸馏，保留其正确的推理策略；失败轨迹则被教师密集引导。实验表明，该掩码使训练奖励从无掩码的 0.56 提升至 0.58，纯 GRPO 仅为 0.51。

### 辅助模块

**冻结视觉编码器**：整个训练过程中视觉编码器参数保持不变，仅更新语言模型部分。这确保了视觉特征提取能力不被破坏，同时将计算资源集中于推理能力的迁移。训练全程使用纯文本数据，视觉编码器仅在推理时参与多模态输入处理。

**序列级熵监控**（非优化目标）：训练过程中监控学生策略生成轨迹的平均每 token 熵，用于评估策略的探索程度：

$$H(\pi_\theta) = \mathbb{E}_{q,\tau\sim\pi_\theta}\left[\frac{1}{T}\sum_{t=1}^{T} H(\pi_\theta(\cdot|h_t))\right]$$

该指标不参与梯度更新，仅作为训练动态的辅助观测。

## 实验与分析

### 核心瓶颈与实验动机

VOLD的实验设计围绕一个明确瓶颈展开：视觉-语言模型（VLM）在复杂推理任务上表现不佳，根源在于缺乏大规模、高质量的图像-文本推理训练数据。文本推理资源丰富且可扩展，但因模态差异难以直接用于VLM的推理训练。实验的核心验证目标是：**能否通过纯文本教师模型和纯文本数据，将推理能力有效迁移至视觉任务**，以及这一迁移过程中的关键条件是什么。

### 主要结果：纯文本训练超越图像训练基线

表1汇总了VOLD与各基线方法在多个多模态推理基准上的性能对比。VOLD以**Qwen2.5-VL-3B**为基础模型，全程仅使用纯文本数学问题进行训练，却在多个视觉推理基准上取得领先：

- **MathVision**：VOLD达到28.0%，显著超越同样使用文本训练的**X-Reasoner-3B**（24.4%）和使用图像训练的**VLAA-Thinker 3B**（24.4%）。这是VOLD最核心的实证优势——在最具挑战性的视觉数学推理基准上，纯文本蒸馏训练超越了图像训练方法。
- **LogicVista**：VOLD达到45.0%，较X-Reasoner（41.1%）提升3.9个百分点，较使用图像训练的**VLM-R1 3B-Math**（40.5%）提升4.5个百分点。
- **DynaMath**（平均）：VOLD达到50.7%，较X-Reasoner（47.2%）提升3.5个百分点。
- **MMMU-Pro (Vision)**：VOLD达到32.0%，较X-Reasoner（31.0%）提升1.0个百分点，与使用图像训练的VLAA-Thinker（32.2%）基本持平。
- **MathVista**：VOLD达到61.9%，较X-Reasoner（61.1%）小幅提升0.8个百分点。
- **MathVerse**：VOLD达到37.9%，较X-Reasoner（35.7%）提升2.2个百分点。

**关键对比**：X-Reasoner与VOLD使用相同的文本训练数据和基础模型，区别仅在于X-Reasoner仅使用GRPO而无在线蒸馏。VOLD在所有六个基准上全面超越X-Reasoner，直接证明了**在线策略蒸馏是性能增益的核心来源**。

**公平性说明**：VLAA-Thinker的训练集与评估集约有40%重叠，可能导致其部分基准性能虚高；VLM-R1-Math在MathVista上进行过训练，在该基准上的直接比较不公平。X-Reasoner-3B未提供官方检查点，VOLD作者自行复现，比较结果可能存在复现偏差。

### 消融实验：冷启动对齐的决定性作用

表2的策略对齐消融实验揭示了VOLD框架中最关键的因果条件：**SFT冷启动阶段必须使用教师模型自身生成的推理轨迹**，否则在线蒸馏完全失效。

具体而言，当SFT阶段使用原始MoT数据集（与教师模型分布不一致）而非教师生成数据时，后续在线蒸馏几乎不带来任何增益，性能与无蒸馏的RL训练持平。而使用教师生成SFT数据后，在线蒸馏在所有基准上均带来显著提升。这一发现确立了VOLD的核心洞察：**教师-学生的分布对齐是在线蒸馏提供有效梯度信号的必要前提**——若学生策略与教师策略差异过大，反向KL散度无法提供有意义的token级引导。

SFT步数的消融（图4）进一步量化了这一条件：SFT步数不足（<3000步）时，学生模型无法从在线蒸馏中获益；随着SFT步数从500增至4000，蒸馏增益逐步提高，约3000步后趋于饱和。这表明充分的策略对齐是解锁在线蒸馏收益的“开关”。

### 组件分析：两阶段缺一不可

表3的组件分析将VOLD拆解为SFT、GRPO、在线蒸馏三个模块，逐一评估贡献：

- **仅SFT**：性能相比基础模型轻微下降。原因是教师生成的SFT数据包含不正确的推理轨迹，未经过滤的监督训练会暂时损害模型性能。
- **SFT + GRPO**：性能大幅提升，GRPO的稀疏奖励机制有效恢复了SFT阶段的性能退化，并进一步推动模型探索正确的推理路径。
- **SFT + GRPO + 在线蒸馏**（完整VOLD）：性能达到最优，在线蒸馏在GRPO基础上提供了额外的密集token级引导，两者协同产生了超越各自独立贡献的增益。

这一分析表明，VOLD的两阶段设计不可简化：SFT建立分布桥梁，GRPO提供探索驱动，在线蒸馏注入教师知识，三者形成完整的推理迁移链条。

### 学习动态：持续优于纯GRPO

图3展示了VOLD与纯GRPO在训练过程中的动态对比。在视觉验证集Geo3K的准确率和文本训练奖励两个指标上，VOLD从训练初期即持续高于纯GRPO，且差距随训练推进逐渐扩大。这表明在线蒸馏不仅提高了最终性能，还加速了学习过程——教师模型的反向KL损失为学生提供了更密集、更稳定的梯度信号，弥补了GRPO稀疏奖励在探索效率上的不足。

### 奖励引导KL掩码的有效性

图5展示了奖励引导KL掩码的效果。掩码版本（仅对失败轨迹施加蒸馏损失）最终训练奖励达0.58，高于无掩码版本（0.56）和纯GRPO（0.51）。这一设计的直觉是：成功轨迹已包含正确的推理策略，不应被教师模型的蒸馏信号干扰；仅对失败轨迹施加蒸馏损失，可以在纠正错误的同时保留已学会的正确行为。

### 教师模型规模的影响

表5探索了教师模型大小（4B、8B、14B）对VOLD性能的影响。从4B到8B，性能在多数基准上有所提升；但从8B到14B，未见一致性的进一步增益。这表明在3B学生模型的容量限制下，8B教师已能提供足够的推理知识，更大教师模型的边际收益递减。

### 通用多模态能力：推理-感知权衡

表6评估了VOLD训练对通用多模态能力的影响。结果显示，纯文本推理训练导致视觉感知能力轻微下降，但推理能力大幅增强，整体MME得分提高。重要的是，这一权衡并非VOLD独有——使用图像训练的VLAA-Thinker也呈现相同的感知下降-推理提升模式。这表明推理-感知权衡是推理聚焦训练的内在属性，而非纯文本训练的副作用。

### VOLD作为图像RL基础模型

表7进一步验证了VOLD的实用价值：在VOLD检查点的基础上继续使用图像-文本数据进行RL训练，性能优于纯文本VOLD和从头训练的VLAA-Thinker。这表明VOLD的纯文本推理迁移可以作为图像RL的有效初始化，为后续多模态训练提供更强的推理先验。

### 方法泛化性

图6验证了在线策略蒸馏与RL算法的正交性——在线蒸馏同样适用于GSPO，在Geo3K验证准确率上均带来提升。这确认了VOLD的蒸馏框架不依赖于特定的RL算法选择。

### 失败模式与局限

1. **SFT阶段的性能退化**：由于未过滤教师错误答案，冷启动SFT后模型性能暂时下降，需依赖后续RL恢复。这是VOLD流程中的已知弱点。
2. **学生容量瓶颈**：3B学生模型对14B教师模型的蒸馏收益饱和，暗示小模型的知识吸收能力存在上限。
3. **推理-感知权衡**：纯文本训练导致视觉感知能力轻微下降，在需要精细视觉理解的任务上可能存在劣势。
4. **任务领域限制**：实验仅在数学推理数据集上进行，在科学推理、编程等其他领域的迁移效果未知。
5. **架构通用性未验证**：所有实验基于Qwen2.5-VL-3B，尚未在LLaVA、InternVL等其他VLM架构上验证。

### 补充图表

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/003_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art approaches on multimodal reasoning benchmarks: VOLD achieves a competitive performance while training exclusively on text data, outperforming baselines that use images during fine-tuning. This can be seen as a indicator that distillation based on text-only teachers can also improve systems beyond text, such as multimodal reasoning models. Baselines marked with ‡ were trained on portions of the evaluation set*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/004_Table_2.jpg]]
*Table 2: Policy Alignment Ablation: demonstrates the critical role of aligning the student with the teacher’s output distribution. We compare our full method, which uses teacher-generated SFT data for alignment, against variants trained on the original MoT dataset, creating a policy mismatch. The results show that without proper alignment, on-policy distillation provides no additional benefit*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/005_Table_3.jpg]]
*Table 3: Component Analysis of VOLD : This table isolates the contribution of each component in our two-stage framework. We show performance after SFT-only, after adding RL (GRPO), and with our full unified objective. While Stage 1 SFT aligns the policy, it temporarily degrades performance due to unfiltered teacher traces. Stage 2, which combines RL with on-policy distillation, provides the largest performance gains, demonstrating that both components are essential for optimal reasoning*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/006_Figure_3.jpg]]
*Figure 3: Learning dynamics: We visualize the validation accuracy as well as text-only training reward during training, comparing the proposed VOLD setup with the regular GRPO training. The results in both cases show a significant gain by the proposed method. (left): Accuracy on the visual Geo3K dataset. (right): Reward on the text-only orz-57k training data*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/007_Figure_4.jpg]]
*Figure 4: Sufficient Policy Alignment is Crucial for On-Policy Distillation. This figure illustrates that the benefit of our unified objective depends on the quality of the initial alignment from Stage 1. Models with short SFT phases (light blue) are poorly aligned with the teacher and fail to benefit from its guidance. As the alignment improves with more SFT steps (darker blue), the student can better leverage the on-policy distillation signal, unlocking significant performance gains over the GRPO-only baseline (red)*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/009_Figure_5.jpg]]
*Figure 5: Training reward comparison: VOLD with KL masking (blue), without masking (purple), and vanilla GRPO (red). KL masking provides consistent performance gains throughout training*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/010_Table_5.jpg]]
*Table 5: Impact of Teacher Model Size. We evaluate the final performance of VOLD when using teacher models of varying scales (4B, 8B, and 14B parameters). While increasing teacher size from 4B to 8B yields performance gains across most benchmarks, we observe diminishing returns with the 14B teacher, which provides no consistent improvement over the 8B model*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/011_Table_6.jpg]]
*Table 6: General Multimodal Capability Evaluation. Perception slightly decreases while reasoning improves. This trade-off is shared by image-trained methods (VLAA-Th.), confirming it is inherent to reasoning-focused training, not text-only training*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/012_Table_7.jpg]]
*Table 7: VOLD as Foundation for Image-Based RL. Starting from the VOLD checkpoint and applying RL on image-text data yields the best results, outperforming both text-only VOLD and image-only training from scratch*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/013_Figure_6.jpg]]
*Figure 6: Generalization to Other RL Algorithms. Validation accuracy on Geo3K. On-policy distillation (OPD) improves both GRPO and GSPO, confirming VOLD is orthogonal to the choice of RL method*

![[assets/figures/papers/paper_list_l2245_https_arxiv_org_abs_2510_23497/figures/001_Figure_1.jpg]]
*Figure 1: Visual Reasoning Examples. (left) The base model fails the task due to a flawed geometric assumption. (center) The base model trained with SFT+RL only-on text outlines a valid plan but uses an incorrect formula, leading to a wrong answer. (right) The model trained with SFT+RL and guided by on-policy distillation from a teacher LLM successfully navigates the problem. It demonstrates flexible reasoning by considering and then discarding a difficult approach in favor of a more direct and correct one*

## 方法谱系与知识库定位

### 1. 方法谱系：从纯文本RL到跨模态推理蒸馏

VOLD处于视觉-语言模型（VLM）推理后训练与知识蒸馏的交叉地带。其核心贡献在于将**纯文本大语言模型（LLM）的推理能力迁移至VLM**，而无需任何视觉推理训练数据。这一思路与现有工作形成清晰对比：

- **纯文本RL基线**：**X-Reasoner-3B**（Liu et al., 2025）同样采用纯文本数据进行SFT+GRPO训练，但未引入在线策略蒸馏。VOLD与X-Reasoner使用相同的训练数据集和基础模型，唯一的差异在于蒸馏模块的加入——这一控制变量设计使得VOLD相对于X-Reasoner的性能提升（如MathVision上+3.6%）可直接归因于在线策略蒸馏的有效性。

- **图像-文本RL基线**：**VLM-R1 3B-Math**（Shen et al., 2025）和**VLAA-Thinker 3B**均使用视觉推理数据进行强化学习训练。VOLD在纯文本训练条件下仍能超越这些方法（如MathVision上28.0% vs. VLAA-Thinker的24.4%），表明高质量的文本推理迁移可以弥补甚至超越直接使用视觉推理数据的训练效果。需注意，VLAA-Thinker的训练集与评估集约40%重叠，其性能可能虚高；VLM-R1-Math在MathVista上进行过训练，在该基准上的直接比较不公平。

- **蒸馏方法定位**：VOLD的在线策略蒸馏与传统的离线蒸馏（仅在静态数据集上对齐输出分布）有本质区别。传统方法中教师仅生成SFT轨迹供学生模仿（如X-Reasoner的做法），而VOLD在RL阶段持续利用教师模型对学生**自身生成的轨迹**提供密集的token级梯度引导，使蒸馏信号与RL探索过程动态耦合。

### 2. 关键技术改进

VOLD对标准GRPO框架的核心改动体现在三个层面：

| 改动维度 | 基线方法 | VOLD方案 | 证据强度 |
|---------|---------|---------|---------|
| 训练流程 | 单阶段（直接RL或仅SFT） | 两阶段：SFT冷启动对齐 + 统一RL与在线蒸馏 | 强（Table 3消融验证两阶段缺一不可） |
| KL正则化 | 与旧策略的KL散度（防止策略突变） | 与教师策略的反向KL散度（引导向教师分布） | 强（Equation 5统一目标） |
| 蒸馏范围 | 无或全轨迹 | 奖励引导掩码：仅对失败轨迹施加蒸馏损失 | 强（Figure 5显示掩码提升训练奖励） |

**奖励引导KL掩码**的设计动机值得关注：对成功轨迹（奖励=1）跳过蒸馏损失，避免教师信号干扰学生已学会的正确推理策略；对失败轨迹（奖励=0）施加反向KL损失，利用教师分布提供逃离低奖励区域的梯度方向。这一机制本质上是**选择性模仿**——让学生在学习教师推理模式的同时保留成功探索的成果。

### 3. 适用边界与约束条件

VOLD的有效性依赖于若干前提条件，这些条件定义了其适用边界：

**（1）冷启动对齐是必要条件。** Table 2的消融实验揭示了关键发现：当SFT阶段使用原始MoT数据集（与教师模型分布不一致）而非教师生成的推理轨迹时，在线策略蒸馏完全失效，性能与无蒸馏的RL持平。Figure 4进一步量化了这一依赖关系——SFT步数不足（<3000步）时，学生模型无法从在线蒸馏中获益；随着SFT步数增加，蒸馏收益逐渐增大并在约3000步后趋于饱和。这一现象表明，教师-学生分布对齐是反向KL损失提供有效梯度信号的前提。

**（2）学生模型容量限制蒸馏收益。** Table 5显示，教师模型从4B增至8B带来明显性能提升，但14B教师相比8B无显著增益。这表明3B学生模型的容量已接近饱和，无法充分吸收更大教师的知识。该发现暗示VOLD的扩展性受限于学生模型规模，需在更大VLM上验证。

**（3）推理-感知权衡。** Table 6表明，纯文本训练后模型的视觉感知能力轻微下降，但推理能力大幅增强。这一权衡并非VOLD特有——使用图像训练的VLAA-Thinker同样存在类似现象，说明这是推理聚焦训练的固有特性，而非纯文本训练的缺陷。

**（4）领域与架构限制。** 当前验证仅限于数学推理任务和Qwen2.5-VL-3B模型。VOLD在其他推理领域（科学、编程）和其他VLM架构（LLaVA、InternVL）上的迁移效果尚未验证。

### 4. 局限与开放问题

**已确认的局限：**

- SFT阶段未过滤教师错误答案，导致冷启动后模型性能暂时下降（Table 3中SFT-only性能低于基础模型），需后续RL阶段恢复。这增加了训练成本并引入了不必要的性能波动。
- 仅在3B参数规模验证，尚未在更大VLM上测试扩展性。
- 训练数据仅覆盖数学推理，跨领域迁移能力未知。
- 纯文本训练导致视觉感知能力轻微下降。

**开放问题：**

1. **SFT数据质量优化**：如何有效过滤教师生成的不正确推理轨迹，减少冷启动阶段的性能退化？可能的方案包括基于奖励模型的轨迹筛选或置信度加权SFT。

2. **跨架构泛化**：VOLD的在线蒸馏机制是否适用于其他VLM架构（如LLaVA、InternVL）？不同视觉编码器与语言模型的耦合方式可能影响蒸馏信号的传递效率。

3. **领域扩展**：如何将迁移范围从数学推理扩展到科学图表理解、多模态代码生成等更广泛的推理任务？这可能需要构建对应领域的文本推理数据集和教师模型。

4. **教师依赖的消减**：能否通过自蒸馏（学生模型自身的强轨迹作为蒸馏目标）或跨模态token对齐进一步减少对外部文本教师的依赖？

5. **KL估计器的改进**：当前使用的k2估计器是否存在更优变体以提升计算效率或梯度稳定性？这直接影响在线蒸馏在大规模训练中的实际可行性。

6. **VOLD作为基础模型的潜力**：Table 7显示在VOLD检查点上继续图像RL可取得最佳性能，表明VOLD可作为图像RL的优质初始化。这一方向值得进一步探索——纯文本推理预训练是否能系统性地降低下游视觉RL的样本复杂度？

## 原文 PDF

![[paperPDFs/CVPR_2026/VOLD_Reasoning_Transfer_from_LLMs_to_Vision_Language_Models_via_On_Policy_Distillation.pdf]]

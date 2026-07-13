---
title: "RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with_Humanoid_Control.pdf
project_link: https://beingbeyond.github.io/RLPF/
code_link: null
aliases:
- RLFPFR
- RFPFALMMHC
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过强化学习微调运动生成器时，引入来自预训练运动跟踪策略的物理可行性奖励（motion tracking reward）和对比学习的语义对齐验证模块，使生成器同时优化物理可行性和语义一致性。
primary_logic: 利用预训练的通用运动跟踪策略作为物理可行性评估器，结合对比预训练编码器保持文本-运动语义对齐，以强化学习框架（GRPO）优化生成模型，从而弥合运动生成和机器人控制之间的模拟到现实差距。
claims:
- RLPF采用运动跟踪策略在物理仿真器中评估可行性，并生成奖励用于微调运动生成器。
- RLPF引入对齐验证模块以保持对文本指令的语义保真度。
- RLPF在所有评估指标上持续优于所有基线方法。
- 对齐验证对于维持运动生成精度至关重要。
---

# RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control

> [!tip] 核心洞察
> 利用预训练的通用运动跟踪策略作为物理可行性评估器，结合对比预训练编码器保持文本-运动语义对齐，以强化学习框架（GRPO）优化生成模型，从而弥合运动生成和机器人控制之间的模拟到现实差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于物理反馈的强化学习：对齐大型运动模型与仿人机器人控制 |
| 英文题名 | RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.12769v1) · [Project](https://beingbeyond.github.io/RLPF/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Reinforcement Learning from Physical Feedback (RLPF) |
| Dataset | CMU, AMASS |

> [!tip] 效果简介
> - CMU 上，Success Rate (Succ) - IsaacGym 0.95 (RLPF-MA) vs 0.48 (Base Model) (+0.47)。
> - AMASS 上，Success Rate (Succ) - IsaacGym 0.92 (RLPF-MA) vs 0.48 (Base Model) (+0.44)。

## 概要

**核心问题**：现有文本到运动（Text-to-Motion, T2M）生成模型产生的动作序列在运动学或物理上不可行——脚滑、地面穿透、动态不稳定等问题普遍存在——导致生成的运动无法直接部署到仿人机器人上。根本瓶颈在于缺少物理可行性评估机制和语义对齐验证，使生成器与机器人控制之间存在显著的模拟到现实差距。

**核心思路**：该工作提出**基于物理反馈的强化学习（Reinforcement Learning from Physical Feedback, RLPF）**，利用预训练的通用运动跟踪策略作为物理可行性评估器，结合对比预训练编码器保持文本-运动语义对齐，以 Group Relative Policy Optimization (GRPO) 框架对大型运动生成模型进行微调，使生成器同时优化物理可行性和语义一致性。

**方法定位**：RLPF 位于文本到运动生成与仿人机器人控制的交叉地带。它不同于传统的监督微调（SFT）——后者仅优化负对数似然损失——也不同于基于物理启发式奖励（如 PHC-based reward, Luo et al., 2023）的方法，而是引入了**学习到的运动跟踪策略**作为奖励信号源，并辅以**对比学习对齐验证模块**来防止 RL 微调过程中的语义退化。该方法在不需要真实机器人数据的情况下，通过仿真器中的物理反馈弥合生成与控制之间的差距。

**主要结果**：
- 在 CMU 数据集上，RLPF-MA 的 IsaacGym 成功率从 Base Model 的 0.48 提升至 **0.95**（+0.47）；在 AMASS 数据集上从 0.48 提升至 **0.92**（+0.44）。
- 消融实验表明，移除对齐验证模块会导致 FID 从 3.61 急剧恶化至 32.53（CMU），模型几乎丧失语义对应性；移除运动跟踪奖励则使成功率骤降至 0.32，证实物理反馈对可行性的关键作用。
- RLPF 在所有评估指标（包括高水平生成指标 FID、R@k、MMDist 和低水平跟踪指标 Succ、MPJPE、MPKPE）上持续优于所有基线方法。

**方法谱系与知识库定位**：RLPF 在技术路径上承接了大型运动生成模型（基于 MotionX 数据集预训练的 LLM 风格生成器）和通用运动跟踪策略（受 Exbody2 启发，通过两阶段教师-学生训练在 AMASS 上学习）两条线。其 RL 微调范式与基于人类反馈的强化学习（RLHF）同构，但将反馈源从人类偏好替换为物理仿真器中的跟踪成功信号。运动重定向采用基于 SMPL 的分层优化方法（遵循 H2O），将形状适配与姿态传递解耦。该方法在 Unitree G1 平台上验证了真实世界可部署性，为文本到运动生成与机器人控制的端到端对齐提供了新范式。

### 问题背景：从文本到运动的“最后一公里”

文本驱动的人体运动生成（Text-to-Motion, T2M）近年来取得了显著进展，大规模运动模型能够根据自然语言描述合成多样化且语义相关的运动序列。然而，当这些生成的运动需要部署到仿人机器人上时，一个根本性的瓶颈浮现出来：**现有模型产生的运动序列在运动学或物理上往往不可行**——表现为脚部滑动、地面穿透、关节超限、动态不稳定等问题。这意味着，即使生成的运动在视觉上看起来合理，也无法直接转换为机器人的控制指令，形成了运动生成与机器人执行之间的“模拟到现实”鸿沟。

### 现有方法的缺口

当前文本到运动生成模型的设计目标主要集中在运动学层面的生成质量，其评估指标（如FID、R-Precision、MMDist）衡量的是生成运动与真实运动分布在特征空间中的距离，而非物理可行性与可部署性。具体而言，现有方法存在以下结构性缺口：

1. **缺乏物理可行性评估机制**：预训练的T2M生成器在训练过程中从未接触物理仿真器的反馈，无法感知生成的运动是否满足动力学约束（如接触力、质心动量、关节力矩限制等）。即使采用监督微调（Supervised Fine-Tuning, SFT）来适配特定数据分布，模型仍然缺乏对物理可行性的显式建模。

2. **语义对齐与物理可行性的冲突**：在追求物理可行性的过程中，生成的运动可能偏离原始文本描述。例如，模型可能退化为生成“站立不动”的序列，因为这是物理上最安全、最易执行的动作，但完全丧失了语义对应性。现有方法缺乏在物理约束下保持语义保真度的机制。

3. **运动重定向的形态差异**：从人体运动数据到机器人关节空间的映射（运动重定向）是一个非平凡问题。简单的关节对应或直接映射无法处理人体与机器人之间的形态差异（如连杆长度、质量分布、自由度配置），导致重定向后的运动在机器人上执行时出现偏差。

### 本文动机

针对上述缺口，本文提出**基于物理反馈的强化学习**（Reinforcement Learning from Physical Feedback, RLPF）框架，核心动机是：**利用物理仿真器中的可执行性信号作为反馈，引导大规模运动生成模型同时优化物理可行性和语义一致性**。

RLPF的设计基于以下关键洞察：

- **预训练的通用运动跟踪策略可以作为物理可行性评估器**：通过在大量运动数据上训练一个能够跟踪任意参考运动的控制策略，该策略在仿真器中执行运动时的成功/失败信号天然地反映了运动的物理可行性。将这一信号作为奖励反馈给生成器，可以使生成器学会产生“可被执行”的运动。

- **对比预训练的编码器可以保持语义对齐**：通过对比学习训练文本编码器和运动编码器，使它们在共享嵌入空间中对齐，可以在RL微调过程中提供语义对齐奖励，防止生成器为追求物理可行性而牺牲语义对应性。

- **强化学习框架（GRPO）适合联合优化多重目标**：Group Relative Policy Optimization（GRPO）允许在组内相对比较的基础上优化策略，避免了传统RL中对绝对奖励尺度的依赖，适合将物理可行性奖励和语义对齐奖励联合优化。

通过这一框架，RLPF旨在弥合运动生成和机器人控制之间的差距，使生成的运动同时具备三个关键属性：**语义对齐性**（与文本描述一致）、**物理可行性**（在仿真器中可执行）和**实际可部署性**（可在真实机器人上运行）。

## 核心方法与创新机理

RLPF 的核心创新在于引入**物理可行性反馈**与**语义对齐验证**双信号，将大规模文本到运动（T2M）生成模型的微调从传统的监督学习范式转变为强化学习范式，从而弥合生成运动的“运动学可行性”与“机器人可部署性”之间的鸿沟。其关键变化槽位（changed slots）可归纳为以下四个维度。

### 1. 微调算法：从监督微调到 GRPO 强化学习

传统 T2M 模型通常采用负对数似然（NLL）损失进行监督微调（SFT），其优化目标仅关注生成运动与参考运动在 token 空间的分布一致性，无法直接感知物理可行性。RLPF 将运动生成器形式化为一个演员策略（actor policy），并采用 **Group Relative Policy Optimization（GRPO）** 进行 RL 微调（Section 3.2）。GRPO 目标函数为：

$$\mathcal{I}_{GRPO}(\theta) = \mathbb{E}[l \sim P(L), \{\bar{z}^i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(Z|l)] \frac{1}{G} \sum_{i=1}^{G} \left(\min\left(\frac{\pi_{\theta}(\bar{z}^i|l)}{\pi_{\theta_{old}}(\bar{z}^i|l)} A_i, \operatorname{clip}\left(\frac{\pi_{\theta}(\bar{z}^i|l)}{\pi_{\theta_{old}}(\bar{z}^i|l)}, 1-\epsilon, 1+\epsilon\right) A_i\right) - \beta \mathbb{D}_{KL}(\pi_{\theta}||\pi_{ref})\right)$$

其中优势函数 $A_i$ 基于组内奖励标准化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \cdots, r_G\})}{\operatorname{std}(\{r_1, r_2, \cdots, r_G\})}$$

这一范式转变使得生成器能够直接优化来自物理仿真器的反馈信号，而非仅仅模仿数据分布。

### 2. 物理可行性反馈：从几何约束到运动跟踪策略奖励

先前方法（如 MDM）最多引入几何层面的足部接触损失，无法保证生成运动在动力学上的可执行性。RLPF 的关键创新在于使用**预训练的通用运动跟踪策略**作为物理可行性评估器（Section 3.3）。该策略通过两阶段教师-学生框架在 AMASS 数据集上训练，能够控制仿人机器人在物理仿真器中跟踪给定的运动序列。其输出的运动跟踪奖励为二值成功标志：

$$R_{tracking}^{m_i} = \mathbb{I}(Succ(\pi, m_i))$$

当且仅当策略 $\pi$ 能够以低于预设阈值 $\epsilon$ 的位置偏差完成运动 $m_i$ 的跟踪时，该奖励为 1。这一设计将物理可行性评估从人工设计的启发式规则提升为基于学习的、泛化能力更强的评估机制。消融实验（Table 4）证实，移除该奖励导致成功率从 0.95 骤降至 0.32（CMU, IsaacGym），验证了物理反馈对可行性的决定性作用。

### 3. 语义对齐保持：从无约束生成到对比学习对齐验证

SFT 和纯粹的 RL 微调均缺乏显式的语义对齐保障机制。RLPF 引入**对齐验证模块**（Section 3.4），使用对比预训练的文本编码器 $\mathbf{E_t}$ 和运动编码器 $\mathbf{E_m}$ 在共享嵌入空间中评估文本-运动一致性。其预训练对比损失为：

$$\mathcal{L}_{CL} = (1-y)(\|\mathbf{f_t} - \mathbf{f_m}\|)^2 + y(max(0, m - \|\mathbf{f_t} - \mathbf{f_m}\|))^2$$

在此基础上，RLPF 提供两种对齐奖励变体：**文本对齐奖励** $R_{TA}^{m_i} = \|\mathbf{E_t}(t) - \mathbf{E_m}(m_{pred})\|^2$ 和**运动对齐奖励** $R_{MA}^{m_i} = \|\mathbf{E_m}(m) - \mathbf{E_m}(m_{pred})\|^2$。消融实验（Table 6）表明，移除对齐验证模块后，模型在 CMU 上的 FID 从 3.61 恶化至 32.53，R@1 降至 0.09，几乎完全丧失语义对应性，仅生成站立序列（Figure 3）。

### 4. 运动重定向：从直接映射到解耦优化

为将人体运动适配到机器人形态，RLPF 采用基于 SMPL 的两步优化方法（Section 3.3.1），将形状适配与姿态迁移解耦处理。这一层次化优化策略相比简单的关节对应映射，能够生成物理上更合理的重定向运动，为后续的跟踪策略训练和奖励计算提供了更可靠的输入。

**创新本质总结**：RLPF 的核心洞察在于利用预训练的通用运动跟踪策略作为“物理可行性 oracle”，结合对比预训练编码器作为“语义对齐 oracle”，以 GRPO 框架联合优化生成模型，从而在不牺牲语义保真度的前提下，显著提升生成运动的物理可部署性。

RLPF 的整体流程围绕一个核心矛盾展开：**文本到运动（T2M）生成模型输出的运动序列在运动学上看似合理，但在物理仿真和真实机器人上往往不可行**（脚滑、穿透、动态失稳）。RLPF 的解决思路是将物理可行性评估器（预训练的运动跟踪策略）和语义对齐验证器（对比预训练编码器）同时纳入强化学习微调框架，使生成器在优化过程中被迫兼顾“能跑”和“跑得对”。

### Pipeline 总览

整个系统由五个串行且相互依赖的模块构成，数据流从文本输入到可部署运动输出：

1. **Text-to-Motion Generator Pre-training**  
   在文本-运动对上用负对数似然预训练一个基于 LLM 的运动生成器，将运动建模为离散 token 序列。该模块输出初始的运动 token，是后续 RL 微调的起点。

2. **Motion Retargeting Module**  
   将生成的人体运动通过 SMPL 优化适配到目标仿人机器人的形态。采用两步分层优化策略，先解耦体型适配，再进行姿态迁移，保证重定向后的运动在机器人运动学范围内物理合理。

3. **Motion Tracking Policy Training**  
   通过两阶段教师-学生训练框架，在 AMASS 数据集上学习一个通用运动跟踪策略。该策略在物理仿真器中执行给定的运动序列，输出成功/失败标志，作为物理可行性奖励的信号源。

4. **Alignment Verification Module**  
   使用对比学习预训练的文本编码器和运动编码器，在共享嵌入空间中评估生成运动与输入文本（或真实运动）的语义一致性，生成对齐奖励。

5. **RL Fine-tuning with GRPO**  
   将运动生成器视为 actor 策略，用 Group Relative Policy Optimization（GRPO）进行微调。每次迭代中，生成器从同一文本提示采样一组运动，分别计算跟踪奖励和对齐奖励，经组内标准化后得到优势函数，驱动策略更新。

### 模块间的输入输出关系

```
文本输入 → [T2M Generator] → 运动 token
    → 解码为运动序列 m_pred
    → 分两路：
       ① [Motion Retargeting] → 机器人运动 → [Motion Tracking Policy] → 物理可行性奖励 R_tracking
       ② [Alignment Verification Module] → 语义对齐奖励 R_TA 或 R_MA
    → 总奖励 r_i = R_tracking + R_alignment
    → [GRPO] 更新生成器参数
```

关键设计在于：**跟踪奖励和对齐奖励同时作用于同一生成器，但来源独立**。跟踪策略是预训练且冻结的，仅作为环境反馈；对齐模块也是预训练冻结的，仅作为语义监督。这种解耦使得生成器在 RL 微调中不会“欺骗”任意一方——它必须同时满足物理仿真器的动力学约束和对比编码器的语义约束。

### 奖励信号的构建逻辑

RLPF 的奖励函数由两个正交分量组成：

- **运动跟踪奖励**  
  $$R_{tracking}^{m_i} = \mathbb{I}(Succ(\pi, m_i))$$
  这是一个二值信号：若预训练跟踪策略 $\pi$ 能在仿真器中成功完成运动 $m_i$ 的跟踪任务，则奖励为 1，否则为 0。该信号直接反映运动的物理可行性，是弥合“生成-部署”差距的关键反馈通道。

- **对齐奖励**  
  提供两种变体：
  - **文本对齐奖励（TA）**：$R_{TA}^{m_i} = \|\mathbf{E_t}(t) - \mathbf{E_m}(m_{pred})\|^2$，衡量生成运动与输入文本的语义一致性。
  - **运动对齐奖励（MA）**：$R_{MA}^{m_i} = \|\mathbf{E_m}(m) - \mathbf{E_m}(m_{pred})\|^2$，衡量生成运动与真实运动（GT）的偏差。

  实验表明，运动对齐奖励（MA）优于文本对齐奖励（TA），因为与 GT 运动对齐能更直接地保留生成质量。

### GRPO 优化机制

GRPO 的核心优势在于**组内相对比较**：对同一文本 $l$ 采样 $G$ 个运动候选，计算每个候选的奖励 $r_i$，然后通过标准化得到优势函数：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \cdots, r_G\})}{\operatorname{std}(\{r_1, r_2, \cdots, r_G\})}$$

这种设计避免了绝对奖励尺度不稳定带来的训练困难，同时天然鼓励生成器在同一语义下探索物理上更可行的运动变体。GRPO 目标函数中额外加入了 KL 惩罚项，防止生成器偏离预训练分布过远，保持基础生成能力。

### 与传统方法的根本差异

传统方法（如 MDM 等）要么完全忽略物理可行性，要么仅使用几何脚接触损失等启发式约束。RLPF 的突破在于：**用数据驱动的跟踪策略替代手工设计的物理规则**，使可行性评估更接近真实动力学；同时用对比编码器保持语义对齐，避免 RL 微调中常见的“奖励黑客”导致语义退化。这一设计使得 RLPF 在 CMU 测试集上成功率从基线的 0.48 提升至 0.95，同时维持了与预训练模型相当的生成质量（FID 3.61 vs 基线的相似水平）。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_12769v1/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RLPF, which consists of three key components: i) Motion Tracking Policy which is pretrained to establish a motion tracking reward to evaluate generated motions; ii) Alignment Verification Module which enhances text-motion semantic consistency while preserving physical plausibility; iii) RL Optimization Framework that jointly optimizes the physical feasibility and semantic alignment of motions generated by the large motion model*

RLPF 的核心架构由三个功能模块和一个 RL 优化框架构成，各模块协同工作以弥合文本到运动生成与仿人机器人部署之间的物理可行性鸿沟。

### 文本到运动生成器预训练

RLPF 首先在一个大型语言模型（LLM）架构上预训练文本到运动（T2M）生成器。该生成器采用 VQ-VAE 风格的**运动分词器**（Motion Tokenizer），包含三个组件：编码器 $E$ 将运动序列映射为隐编码，解码器 $D$ 从 token 重建运动，以及码本 $C$ 用于量化表示。预训练目标为标准的负对数似然损失：

$$\mathcal{L}(\Theta) = -\sum_{j=1}^{T} \log P_{\Theta}(z_j \mid l, \vec{z}_{1:j-1})$$

其中 $l$ 为文本条件，$z_j$ 为第 $j$ 个预测的运动 token，$\Theta$ 为生成器参数。该阶段为后续 RL 微调提供了具备基础文本-运动映射能力的初始策略 $\pi_{\theta_{old}}$。

### 运动重定向模块

由于生成的人体运动与目标机器人形态存在差异，RLPF 采用基于 SMPL 模型的**分层优化**方法进行运动重定向。该过程解耦为两个阶段：首先进行**形状适配**（shape adaptation），将人体 SMPL 模型匹配至机器人身体比例；随后进行**姿态迁移**（pose transfer），在保持物理合理性的前提下将运动轨迹映射至机器人关节空间。这种解耦策略确保了重定向后的运动在运动学上与机器人本体兼容，为后续的跟踪评估提供有效输入。

### 运动跟踪策略与物理可行性奖励

这是 RLPF 实现物理可行性反馈的关键创新。系统预训练一个**通用运动跟踪策略** $\pi$，用于在物理仿真器中评估生成运动的可执行性。训练采用两阶段教师-学生框架：首先在 AMASS 数据集上训练特定运动专家策略，随后通过知识蒸馏学习一个通用策略，使其能够跟踪多样化的运动序列。

在 RL 微调阶段，该跟踪策略充当物理可行性评估器，为每条生成的运动 $m_i$ 提供二值奖励信号：

$$R_{tracking}^{m_i} = \mathbb{I}(Succ(\pi, m_i))$$

其中 $Succ(\pi, m_i)$ 为成功标志，指示跟踪策略 $\pi$ 是否能在仿真器中完成运动 $m_i$ 的跟踪任务。这一简洁的二值奖励机制直接反映了运动在物理环境中的可执行性，构成了 RL 优化中物理可行性的核心反馈源。

### 对齐验证模块

为防止 RL 微调过程中生成器为追求物理可行性而丧失语义保真度，RLPF 引入**对齐验证模块**。该模块基于对比学习预训练的文本编码器 $\mathbf{E_t}$ 和运动编码器 $\mathbf{E_m}$，将文本和运动映射至共享嵌入空间。编码器通过对比损失训练：

$$\mathcal{L}_{CL} = (1-y)(\|\mathbf{f_t} - \mathbf{f_m}\|)^2 + y(\max(0, m - \|\mathbf{f_t} - \mathbf{f_m}\|))^2$$

其中 $y$ 为匹配标签，$m$ 为间隔超参数，$\mathbf{f_t}$ 和 $\mathbf{f_m}$ 分别为文本和运动的嵌入特征。

基于此，模块提供两种对齐奖励变体：

- **文本对齐奖励**（Text Alignment, TA）：测量生成运动与输入文本的语义一致性
  $$R_{TA}^{m_i} = (\|\mathbf{E_t}(t) - \mathbf{E_m}(m_{pred})\|)^2$$

- **运动对齐奖励**（Motion Alignment, MA）：测量生成运动与真实运动（GT）的偏差
  $$R_{MA}^{m_i} = (\|\mathbf{E_m}(m) - \mathbf{E_m}(m_{pred})\|)^2$$

实验表明，运动对齐奖励（RLPF-MA）在保持生成质量方面优于纯文本对齐（RLPF-TA），说明与 GT 运动对齐对于维持语义保真度更为有效。

### GRPO 优化框架

RLPF 将运动生成器形式化为一个 actor 策略 $\pi_{\theta}$，采用**Group Relative Policy Optimization**（GRPO）算法进行微调。GRPO 的目标函数为：

$$\mathcal{I}_{GRPO}(\theta) = \mathbb{E}\left[l \sim P(L), \{\bar{z}^i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(Z|l)\right] \frac{1}{G} \sum_{i=1}^{G} \left(\min\left(\frac{\pi_{\theta}(\bar{z}^i|l)}{\pi_{\theta_{old}}(\bar{z}^i|l)} A_i, \operatorname{clip}\left(\frac{\pi_{\theta}(\bar{z}^i|l)}{\pi_{\theta_{old}}(\bar{z}^i|l)}, 1-\epsilon, 1+\epsilon\right) A_i\right) - \beta \mathbb{D}_{KL}(\pi_{\theta}||\pi_{ref})\right)$$

其中优势函数 $A_i$ 通过组内奖励标准化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \cdots, r_G\})}{\operatorname{std}(\{r_1, r_2, \cdots, r_G\})}$$

KL 散度惩罚项采用无偏估计器：

$$\mathbb{D}_{KL}(\pi_{\theta}||\pi_{ref}) = \frac{\pi_{ref}(\vec{m}^i|l)}{\pi_{\theta}(\vec{m}^i|l)} - \log\frac{\pi_{ref}(\vec{m}^i|l)}{\pi_{\theta}(\vec{m}^i|l)} - 1$$

总奖励 $r_i$ 由物理可行性奖励和对齐奖励加权组合而成，使生成器在 GRPO 框架下联合优化运动的物理可执行性和语义一致性。

## 实验与关键发现

### 核心问题与评估框架

实验围绕三个递进的研究问题展开：(Q1) RL 微调是否比监督微调（SFT）能产生更物理可行的运动？(Q2) 运动跟踪奖励对可执行性有多关键？(Q3) 对齐验证模块如何影响语义保真度？评估采用双层次指标——低水平跟踪指标（Success Rate Succ↑、MPJPE↓、MPKPE↓）测量物理可行性，高水平生成指标（FID↓、R@k↑、MMDist↓）测量语义对齐与分布匹配，在两个物理仿真器（IsaacGym、MuJoCo）和两个数据集（CMU、AMASS）上进行。

### 主实验结果

**RLPF 在所有指标上持续优于所有基线方法**。在 CMU 数据集上，RLPF-MA（运动对齐验证变体）在 IsaacGym 中的成功率从 Base Model 的 0.48 提升至 0.95（+0.47），在 MuJoCo 中从 0.32 提升至 0.75（+0.43）（Table 2）。在 AMASS 数据集上，RLPF-MA 在 IsaacGym 中达到 0.92 的成功率，同样远超 Base Model 的 0.48（Table 3）。这一结果表明 RL 微调能够从根本上改善生成运动的物理可行性，而 SFT 即使使用精心筛选的跟踪优化数据也无法达到同等水平。

在高水平生成质量上（Table 1），RLPF-MA 在 CMU 上取得 FID 3.61、R@1 0.88，在 AMASS 上取得 FID 1.84、R@1 0.93，均优于 RLPF-TA（文本对齐验证变体）和 Base Model。**仅使用文本对齐验证（RLPF-TA）比运动对齐验证（RLPF-MA）性能差**，说明与真实运动（GT）对齐比仅与文本对齐更能维持生成质量。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_12769v1/figures/003_Table_1.jpg]]
*Table 1: Comparisons of High-level generation evaluation on the CMU and AMASS test sets. RLPF-MA and RLPF-TA denote the motion alignment verification and text alignment verification, respectively, as described in Section 3.4*

### 消融实验

消融实验揭示了两个核心组件的因果作用：

**运动跟踪奖励对物理可行性至关重要**。移除运动跟踪奖励（RLPF-w/o track）后，CMU 数据集上 IsaacGym 成功率骤降至 0.32，MuJoCo 成功率降至 0.21（Table 4），表明物理反馈信号是生成可行运动的必要条件。使用传统物理启发式奖励（RLPF-PHC）虽能保持一定可行性（如 AMASS IsaacGym Succ 0.88），但成功率仍低于 RLPF-MA 的 0.92（Table 5），验证了学习到的跟踪策略作为奖励源优于手工设计的物理约束。

**对齐验证模块对语义保真度不可或缺**。移除对齐验证（RLPF-w/o align）导致高水平生成指标严重退化：CMU 上 FID 从 3.61 飙升至 32.53，R@1 从 0.88 暴跌至 0.09（Table 6）。可视化结果（Figure 3）进一步证实，缺乏对齐验证时模型几乎只生成站立序列，完全丧失与输入文本指令的语义对应性。这一失败模式揭示：**仅靠物理可行性奖励会导致模式坍塌**，对齐验证是维持生成多样性和语义准确性的关键约束。

### 关键图表结论

- **Table 1**：RLPF-MA 在 FID、R@k、MMDist 上全面优于 RLPF-TA 和 Base Model，运动对齐验证优于文本对齐验证。
- **Table 2 & 3**：RLPF 在 CMU 和 AMASS 上的低水平跟踪指标均显著领先，物理可行性提升具有跨数据集一致性。
- **Table 4 & 5**：消融证实运动跟踪奖励是成功率的核心驱动力，移除后性能崩溃。
- **Table 6**：消融证实对齐验证是语义保真度的核心保障，移除后 FID 恶化近 10 倍。
- **Figure 3**：RLPF-w/o align 的生成结果退化为单一站立姿态，直观展示了语义对齐模块的必要性。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_12769v1/figures/004_Table_2.jpg]]
*Table 2: Comparisons of low-level tracking evaluation on the CMU test set*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_12769v1/figures/006_Table_4.jpg]]
*Table 4: Ablation results of low-level tracking on IsaacGym and MuJoCo simulators (CMU Dataset)*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_12769v1/figures/008_Table_6.jpg]]
*Table 6: Ablation results of high-level generation on the CMU and AMASS test sets*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2506_12769v1/figures/009_Figure_3.jpg]]
*Figure 3: Visualizations of RLPF-w/o align. Since training relies solely on the motion tracking reward, the model predominantly generates standing motion sequences, losing semantic alignment with the input textual instructions*

### 局限性与失败模式

尽管 RLPF 表现优异，仍存在以下局限：物理可行性奖励为二值成功信号（$R_{tracking}^{m_i} = \mathbb{I}(Succ(\pi, m_i))$），可能将部分可行的运动错误标记为失败，更细粒度的连续奖励或许能进一步提升性能。运动重定向依赖 SMPL 优化，对与人体形态差异巨大的机器人可能需要重新适配。当前方法依赖固定的预训练跟踪策略，可能难以处理域外或极端运动——联合训练生成器与跟踪策略以扩展泛化性仍待探索。此外，实验仅在 Unitree G1 平台上验证，泛化至其他仿人机器人形态的证据尚不充分，需要手动验证。

## 定位与知识库关联

### 1. 方法沿革与基线对比

RLPF 处于**文本到运动生成**与**仿人机器人全身控制**的交叉点，其核心贡献在于首次将强化学习引入运动生成器的微调，以弥合生成动作的物理不可行性与机器人可部署性之间的鸿沟。传统文本到运动生成模型（如 MDM 等扩散或自回归方法）仅优化运动学层面的似然或分布匹配，缺乏对物理可行性（如脚部滑动、地面穿透、动态稳定性）的显式建模。RLPF 的基线与变体构成了一个清晰的方法谱系：

- **Base Model（预训练 T2M 生成器）**：采用基于 VQ-VAE 的运动分词器与自回归 Transformer，在文本-运动对上通过负对数似然进行预训练。该基线代表了纯运动学生成范式，其生成的动作在 CMU 数据集上的物理仿真成功率仅 0.48（IsaacGym），在 AMASS 上同为 0.48，表明预训练本身几乎不提供物理可行性保障。

- **Supervised Fine-Tuning (SFT)**：在预训练基础上使用监督微调，损失函数仍为 NLL。论文将其作为对比 RL 微调效果的基线，但未报告 SFT 的完整数值结果。从 Section 4 的研究问题 Q1 可知，SFT 即使使用经跟踪优化的策展数据，其生成的物理可行性仍不及 RL 微调，说明仅靠监督信号无法有效注入物理约束。

- **PHC-based reward（Luo et al., 2023）**：采用基于物理启发式约束（Physical Heuristic Constraints）的奖励函数，如脚部接触、关节限位等手工设计的物理规则，而非学习到的跟踪策略。消融实验中 RLPF-PHC 变体即使用此类奖励。该方法可保持一定的物理可行性，但对齐指标下降：在 AMASS 上 FID 为 1.84，R@1 略低于 RLPF-MA，表明手工物理奖励缺乏对运动整体质量的细粒度评估能力。

- **RLPF（本文提出）**：在 GRPO 强化学习框架下，联合优化两项奖励——来自预训练通用运动跟踪策略的二值成功信号 $R_{tracking}^{m_i} = \mathbb{I}(Succ(\pi, m_i))$，以及来自对比预训练编码器的语义对齐奖励（运动对齐 $R_{MA}$ 或文本对齐 $R_{TA}$）。该方法将物理可行性评估从手工规则升级为数据驱动的跟踪策略，同时通过对比学习保持文本-运动语义一致性，形成“生成-跟踪验证-对齐保持”的闭环。

### 2. 核心组件与知识来源

RLPF 的架构由五个关键模块构成，每个模块均建立在明确的先前工作之上：

| 模块 | 角色 | 知识来源/基础工作 |
|------|------|-------------------|
| 文本到运动生成器预训练 | 使用 VQ-VAE 分词器与自回归 LLM 生成运动 token | T2M-GPT 等运动分词与生成范式 |
| 运动重定向 | 通过 SMPL 模型的两步优化将人体运动适配到机器人形态 | H2O（优化解耦形状适应与姿态迁移） |
| 运动跟踪策略训练 | 两阶段教师-学生训练学习通用跟踪策略 | Exbody2（Ji et al., 2024）的教师-学生框架，基于 AMASS 数据集 |
| 对齐验证模块 | 对比预训练编码器评估文本-运动语义对齐 | 对比学习在跨模态嵌入中的应用（CLIP 范式） |
| RL 微调（GRPO） | 联合优化物理可行性与语义对齐 | GRPO（Group Relative Policy Optimization）算法 |

### 3. 适用边界与局限

基于论文报告的实验设置与消融分析，RLPF 的适用边界可归纳如下：

1. **跟踪策略的泛化瓶颈**：当前方法依赖固定的预训练通用跟踪策略作为奖励信号源。该策略在 AMASS 数据集上训练，对域外运动（如极端姿态、高动态特技动作）的跟踪能力未经验证。Section 5 明确指出“联合训练生成器与跟踪策略以扩展泛化性仍待探索”。

2. **二值奖励的粒度限制**：物理可行性奖励 $R_{tracking}$ 为二值成功标志，无法区分“完全成功”与“部分可行”的运动。消融实验中 RLPF-w/o align 在仅依赖跟踪奖励时，模型退化为主要生成站立序列（Figure 3），说明二值信号在缺乏语义约束时会导致模式坍缩。

3. **运动重定向的形态依赖**：重定向基于 SMPL 人体模型优化，对与人体形态差异显著的机器人（如四足、轮式仿人）需重新设计适配流程。Table 8 给出了人形机器人与人体的链接对应关系，但该映射的通用性有待验证。

4. **平台泛化未充分验证**：实验仅在 Unitree G1 平台上进行真机验证，其他仿人机器人形态（如 Tesla Optimus、Figure 01）的迁移效果未报告。

5. **仿真到现实的差距**：尽管 MuJoCo 与 IsaacGym 双仿真器评估提供了一定的鲁棒性证据，但 Section 5 仍将“进一步缩小仿真与真实世界的动力学差距”列为开放问题，并提及可参考 ASAP 等对齐方法。

### 4. 开放问题与未来方向

论文明确提出的开放问题及本文分析补充的方向包括：

- **联合训练生成器与可适应跟踪策略**：当前跟踪策略是固定预训练的，无法随生成器微调而进化。如何实现两者的协同优化，以泛化到域外运动，是提升系统鲁棒性的关键。

- **连续物理可行性奖励设计**：将二值成功信号替换为更细粒度的连续奖励（如跟踪误差的平滑函数、接触力合理性等），可能缓解模式坍缩并提升运动多样性。

- **跨形态泛化**：运动重定向的 SMPL 优化框架对非人形机器人的适用性有限，需探索更通用的形态适配方法。

- **仿真-现实差距缩小**：可结合域随机化、系统辨识或真实数据微调（如 ASAP 方法）进一步对齐仿真与真实动力学。

- **多模态扩展**：当前仅考虑文本输入，未来可扩展至语音、视频等指令模态，进一步拓宽人机交互边界。

## 原文 PDF

![[paperPDFs/arxiv_2025/RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with_Humanoid_Control.pdf]]

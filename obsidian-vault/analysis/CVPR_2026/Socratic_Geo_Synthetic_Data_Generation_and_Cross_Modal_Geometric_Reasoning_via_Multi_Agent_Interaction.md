---
title: "Socratic-Geo: Synthetic Data Generation and Cross-Modal Geometric Reasoning via Multi-Agent Interaction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Socratic_Geo_Synthetic_Data_Generation_and_Cross_Modal_Geometric_Reasoning_via_Multi_Agent_Interaction.pdf
project_link: null
code_link: null
aliases:
- SG
- Socratic-Geo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 目标驱动的程序化合成：通过诊断求解器（Solver）的弱点，利用Teacher的程序化Python脚本修改几何结构（RePI），并进行自验证（Reflect），从而动态生成针对性的高质量训练样本，直接提升数据质量和模型推理能力。
primary_logic: 受苏格拉底方法启发，构建一个多智能体闭环交互框架，将数据合成与模型学习动态耦合。Teacher根据Solver的失败信号，发明新的、有针对性的几何问题，并通过程序化验证确保图文严格对齐。这一持续性课程随模型能力演化，实现了用极少种子数据驱动显著性能提升的高效合成范式。
claims:
- Socratic-Solver在6个几何基准上平均准确率达49.11%，仅使用基线1/4的训练样本，超过最强基线2.43个百分点（相比零样本基线提升+4.13点）。
- Socratic-Generator在GenExam-Math上取得42.4%的Relaxed分数，创开源模型新SOTA，超越商业模型Seedream-4.0 (39.8%)，接近Gemini-2.5-Flash-Image (43.1%)。
- 去除Qualify（Reflect验证）模块后，尽管训练数据量从0.4k增至1.3k，MathVerse准确率反而降至37.09%，低于零样本基线39.59%，证明自验证对保证数据质量至关重要。
- 去除Instruction Rewriting（IR）后，GenExam-Math严格分数降为0.0%，松弛分数仅20.1%；保留IR则分别达到6.0%和42.4%，表明将自然语言问题转换为结构化绘图指令是生成精确几何图的关键。
---

# Socratic-Geo: Synthetic Data Generation and Cross-Modal Geometric Reasoning via Multi-Agent Interaction

> [!tip] 核心洞察
> 受苏格拉底方法启发，构建一个多智能体闭环交互框架，将数据合成与模型学习动态耦合。Teacher根据Solver的失败信号，发明新的、有针对性的几何问题，并通过程序化验证确保图文严格对齐。这一持续性课程随模型能力演化，实现了用极少种子数据驱动显著性能提升的高效合成范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | Socratic-Geo：通过多智能体交互实现合成数据生成与跨模态几何推理 |
| 英文题名 | Socratic-Geo: Synthetic Data Generation and Cross-Modal Geometric Reasoning via Multi-Agent Interaction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jiao_Socratic-Geo_Synthetic_Data_Generation_and_Cross-Modal_Geometric_Reasoning_via_Multi-Agent_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Socratic-Geo |
| Dataset | 六个几何推理基准（MathVerse, GeomVerse, GeoQA, MathVision, MathVista, WeMath）平均, GenExam-Math, Chart Reasoning & Multimodal Coding |

> [!tip] 效果简介
> - 六个几何推理基准（MathVerse, GeomVerse, GeoQA, MathVision, MathVista, WeMath）平均 上，Mean@1 (%) 49.11 vs Zero-shot (Qwen2.5-VL-7B-Instruct) (+4.13)。
> - GenExam-Math (图像生成数学赛道) 上，Relaxed Score (%) 42.4 vs Seedream-4.0 (39.8%) (+2.6)。
> - Chart Reasoning & Multimodal Coding 上，Mean@1 (%) gain over zero-shot 一致提升+3.9至+7.6 vs Zero-shot (Qwen2.5-VL-7B-Instruct) (+3.9 ~ +7.6)。

## 概要

**核心问题**：高质量几何训练数据的极度稀缺构成了多模态大模型在视觉几何推理领域进展缓慢的根本瓶颈。现有的自动化数据合成方法——无论是基于LLM的反向思维链生成（如**R-CoT**, Deng et al., arXiv 2024）、大规模几何数据增强（如**G-LlaVA**, Gao et al., arXiv 2025），还是基于强化学习的图像描述合成（如**GeoReasoning-10K**, Xin et al., 2025）——均采用静态、一次性生成范式，数据合成与模型学习相互脱节，无法同时保证正确性、多样性和训练有效性。

**核心方法**：本文提出**Socratic-Geo**（CVPR 2026），一个受苏格拉底方法启发的多智能体闭环交互框架。该框架将数据合成与模型学习动态耦合：Teacher智能体根据Solver的失败信号，通过程序化Python脚本（RePI机制）有针对性地发明新的几何问题，并借助自验证（Reflect）确保图文严格对齐，形成随模型能力演化的持续性课程学习闭环。

**关键结论**：
- **推理能力**：Socratic-Solver在6个几何推理基准上平均准确率达49.11%，仅使用基线1/4的训练样本，超越最强基线2.43个百分点，相比零样本基线（Qwen2.5-VL-7B-Instruct, Bai et al., arXiv 2025）提升4.13个百分点。
- **生成能力**：Socratic-Generator在GenExam-Math上取得42.4%的Relaxed分数，创开源模型新SOTA，超越商业模型Seedream-4.0（39.8%），逼近Gemini-2.5-Flash-Image（43.1%）。
- **消融验证**：去除Qualify自验证模块后，尽管训练数据量从0.4k增至1.3k，MathVerse准确率反而降至37.09%，低于零样本基线39.59%，证实自验证对数据质量的决定性作用；去除Instruction Rewriting后，GenExam-Math严格分数降为0.0%，松弛分数仅20.1%，表明结构化绘图指令是生成精确几何图的必要条件。

**方法定位**：Socratic-Geo在方法谱系中属于**目标驱动的程序化合成**范式，其核心变革在于将数据合成从静态生成转变为与模型学习深度耦合的动态闭环。相较于现有方法的被动改写或随机探索后过滤，Socratic-Geo通过诊断Solver弱点、程序化修改几何结构并进行自验证，实现了数据质量与模型能力的协同进化。



### 几何推理中的数据瓶颈

多模态大模型在自然场景理解上取得了长足进步，但在**视觉几何推理**领域进展缓慢。其核心瓶颈并非模型架构的局限，而是**高质量几何训练数据的极度稀缺**。几何问题要求模型同时具备精确的视觉感知、严格的逻辑推理和符号计算能力，这使得人工标注成本高昂，而自动化数据合成又面临三大挑战：

1. **正确性**：合成的几何问题必须逻辑自洽，图文严格对齐，任何视觉歧义或逻辑漏洞都会误导模型学习。
2. **多样性**：几何推理涉及点、线、角、圆等元素的复杂组合，单一模板生成的数据难以覆盖真实问题的分布。
3. **训练有效性**：数据合成与模型学习通常是分离的——先静态生成数据集，再用于训练。这种脱节意味着合成数据无法针对模型的具体弱点进行优化，大量样本可能是模型已经掌握的“冗余题”，而真正的薄弱环节却得不到针对性强化。

### 现有方法的局限

当前几何数据合成方法可归为两类，均存在根本性缺陷：

- **LLM驱动的被动生成**：如 **R-CoT**（Deng et al., arXiv 2024）基于反向思维链生成几何问题，**G-LlaVA**（Gao et al., arXiv 2025）进行大规模几何数据增强。这些方法依赖LLM的文本生成能力，但缺乏对几何结构的精确控制——LLM无法直接绘制图形，生成的图文对容易出现“图不对题”的对齐错误。更关键的是，它们是一次性、静态的生成过程，无法根据模型的实际表现动态调整数据分布。

- **随机探索后过滤**：如 **GeoReasoning-10K**（Xin et al., 2025）通过强化学习合成几何图像描述。这类方法虽引入了探索机制，但本质上仍是“先生成再筛选”的离线范式。大量计算资源消耗在无效样本的生成与过滤上，数据利用率低，且无法形成持续优化的闭环。

上述方法的共同症结在于：**数据合成与模型学习相互脱节**。合成器不知道模型的弱点在哪里，模型也无法向合成器反馈最需要什么样的训练样本。

### 核心动机：苏格拉底式的闭环合成

本文的动机源自一个朴素的观察：优秀的教师不会盲目地给学生布置海量习题，而是通过诊断学生的错误，**针对性地设计能暴露其思维盲区的诊断性问题**。这正是苏格拉底教学法的精髓——通过追问与反诘，引导学习者发现自身的推理缺陷。

受此启发，Socratic-Geo提出了一种**目标驱动的程序化合成范式**：构建一个多智能体闭环交互框架，让“教师”（Teacher）持续诊断“学生”（Solver）的推理失败，并利用Python代码**程序化地发明**新的、有针对性的几何问题。这种动态耦合机制使得数据合成随模型能力同步演化，实现了用极少种子数据（仅108个种子问题）驱动显著性能提升的高效合成范式。

### 技术路径的独特性

与现有方法相比，Socratic-Geo在三个维度上实现了根本性突破：

1. **动态闭环 vs. 静态生成**：Teacher根据Solver的失败信号实时触发新一轮数据合成，形成“诊断→发明→验证→训练→再诊断”的持续优化回路。
2. **程序化控制 vs. 文本驱动**：通过RePI（Representation-guided Programmatic Invention）机制，Teacher以Python脚本精确构造和修改几何结构，确保图形的数学严格性，而非依赖模糊的自然语言描述。
3. **自验证过滤 vs. 后验筛选**：Qualify（Reflect）模块使Teacher在生成新问题后**自行求解验证**，只有通过验证的样本才进入训练课程。这一机制从根本上保证了数据质量，而非在生成后被动过滤噪声。

这一范式的核心洞察在于：**将数据合成从模型训练的“前置工序”升级为“并行引擎”**，使两者在持续交互中相互促进，最终实现推理能力与生成能力的双重提升。



## 核心方法与创新机理

Socratic-Geo 的核心创新在于将几何数据合成从“静态生成、事后过滤”范式转变为**目标驱动的动态闭环合成范式**，并通过多智能体交互将数据合成与模型学习深度耦合。

### 范式转变：从静态生成到动态闭环

现有几何数据合成方法（如 **R-CoT**（Deng et al., arXiv 2024）、**G-LlaVA**（Gao et al., arXiv 2025））普遍采用一次性生成策略：LLM 被动改写或随机探索后过滤出有效样本，数据合成与模型训练相互分离。这种范式面临一个根本性瓶颈：生成器无法预知模型的具体弱点，导致大量合成样本对模型提升无效，而真正需要的针对性训练数据却无法被系统性地产生。

Socratic-Geo 的核心洞察受苏格拉底方法启发：**通过持续追问（诊断）和引导（发明），让模型在失败中学习**。具体而言，框架构建了一个 Solver-Teacher 闭环：

1. **失败触发**：Solver 在课程 $C_t$ 上尝试求解几何问题，当 $k$ 次尝试全部失败时，触发 Teacher 介入。
2. **诊断分析**：Teacher 通过 Verify 模块比照参考解定位错误，再通过 Analyze 模块进行双模态（文本推理链 + 几何图像）错误诊断，识别 Solver 的具体推理盲区。
3. **目标发明**：Teacher 基于诊断结果，通过 **RePI**（程序化几何发明）机制修改底层 Python 几何代码，针对性地构造新问题——新问题被设计为恰好暴露 Solver 的薄弱环节。
4. **自验证过滤**：Teacher 通过 **Qualify (Reflect)** 模块自行求解新发明的问题，仅当解答正确且图像视觉有效时，才将新样本纳入课程 $C_{t+1}$。

这一闭环的数学表达为课程演化规则：

$$\mathcal{C}_{t+1} = \mathcal{C}_t \cup \{ (I_{\mathrm{new}}, q_{\mathrm{new}}, a_{\mathrm{new}}) \mid \exists (I,q,a^*) \in \mathcal{C}_t, \{a_S^{(i)}\}_{i=1}^k \sim \pi_S^{(t)}(I,q), \sum_{i=1}^k \mathcal{V}(q, a_S^{(i)}, a^*) = 0 \}$$

该规则确保了**课程随模型能力动态演化**：随着 Solver 不断进步，触发 Teacher 介入的失败样本难度逐渐提升，Teacher 发明的针对性问题也随之升级，形成持续性的课程学习。

### 关键技术突破：程序化几何构造与自验证

Socratic-Geo 在三个关键 slot 上实现了对基线方法的根本性改造：

| 维度 | 基线方法 | Socratic-Geo |
|------|---------|-------------|
| **数据合成范式** | 静态、一次性生成，与训练分离 | 动态闭环：失败驱动→诊断→目标发明→自验证→课程注入 |
| **几何图像控制** | 使用现有图像或盲目符号生成，无法精细修改结构 | RePI 机制：Python 代码程序化构造/修改几何图形，确保精确图文对齐 |
| **生成器训练信号** | 无独立生成器或模糊文本提示生成像素 | 蒸馏 Teacher 的程序化绘图智能：从精确的“绘制指令-图像”对训练扩散模型 |

**RePI（程序化几何发明）** 是 Teacher 的核心能力。与依赖 LLM 直接生成像素或描述性文本不同，RePI 要求 Teacher 输出可执行的 Python 几何代码。这一设计带来了三重优势：
- **精确性**：几何关系通过代码逻辑严格定义，避免了自然语言描述的歧义。
- **可验证性**：代码执行结果可被自动检查，确保生成的图像与问题描述完全一致。
- **可干预性**：Teacher 可以针对性地修改代码中的特定几何约束（如改变角度、添加辅助线、调整点位置），实现对几何结构的精细操控。

**Qualify (Reflect) 自验证** 则是保证数据质量的关键防线。消融实验（Table 4）提供了决定性证据：移除 Qualify 模块后，尽管训练数据量从 0.4k 增至 1.3k，MathVerse 准确率反而降至 37.09%，**低于零样本基线 39.59%**。这表明未经验证的合成数据引入了严重的几何不一致和逻辑错误，反而毒化了模型训练。Qualify 模块通过 Teacher 自行求解并验证，确保每个进入课程的样本都是“可解且正确”的，实现了以更少但更高质量的数据驱动更强性能。

### 生成能力的协同提升

Socratic-Geo 的另一项创新在于将推理闭环的“副产品”——Teacher 在发明过程中产生的精确绘制指令——转化为生成器的训练信号。Teacher 在构造几何问题时，同时输出结构化的绘图指令 $p_{\mathrm{diagram}}$，这些指令与生成的图像 $I_{\mathrm{new}}$ 形成严格对齐的配对数据。生成器（扩散模型）通过监督微调损失：

$$\mathcal{L}_{\mathrm{SFT}}(\theta_{\mathcal{G}}) = \mathbb{E}_{ \substack{ z_0 = \mathcal{E}(I_{\mathrm{new}}), \\ \epsilon \sim \mathcal{N}(0,I), t } } \left[ \left\| \epsilon - \epsilon_{\theta_{\mathcal{G}}}(z_t, t, p_{\mathrm{diagram}}) \right\| ^2 \right]$$

从这些配对中蒸馏 Teacher 的程序化绘图智能。**Instruction Rewriting (IR)** 模块在此过程中扮演关键角色：将自然语言几何问题翻译为结构化绘图指令。消融实验（Table 5）表明，移除 IR 后 GenExam-Math 严格分数直接降为 0.0%，松弛分数仅 20.1%；保留 IR 则分别达到 6.0% 和 42.4%。这证明结构化绘图指令是满足复杂数学约束、生成精确几何图的根本保障——没有它，扩散模型无法将自然语言中的几何关系准确映射为像素空间中的图形结构。

### 与现有方法的本质差异

Socratic-Geo 与 **GeoReasoning-10K**（Xin et al., 2025）等基于强化学习的方法在哲学上截然不同：后者通过奖励信号在固定数据上优化模型策略，而 Socratic-Geo 通过**改变数据本身**来引导模型进化。这种“授人以渔”的范式使得仅用 108 个种子问题启动的闭环，最终在六个几何基准上达到 49.11% 的平均准确率，仅使用基线 1/4 的训练样本即超越最强基线 2.43 个百分点。



Socratic-Geo 是一个完全自主的多智能体闭环框架，将几何数据合成与模型学习动态耦合。其核心设计受苏格拉底教学法启发：Teacher（强 LLM）扮演“导师”角色，根据 Solver（推理模型）暴露的弱点，目标驱动地发明针对性训练样本，并通过程序化验证保证图文严格对齐。

### 闭环架构与模块关系

框架包含三个核心智能体，形成两条相互协同但逻辑独立的回路：

**核心推理回路（Solver-Teacher 闭环）** 是系统的主干。Solver 对课程中的几何问题进行多模态推理；当其在 $k$ 次尝试中全部失败时，触发 Teacher 的诊断-发明-验证流水线。Teacher 分析 Solver 的错误推理路径，通过 **RePI（程序化发明）** 修改底层 Python 几何代码，生成新的问题三元组 $(I_{\text{new}}, q_{\text{new}}, a_{\text{new}})$，再经 **Qualify（Reflect 自验证）** 确保问题可解且视觉有效后，注入课程 $\mathcal{C}_{t+1}$。这一课程演化规则为：

$$
\mathcal{C}_{t+1} = \mathcal{C}_t \cup \{ (I_{\mathrm{new}}, q_{\mathrm{new}}, a_{\mathrm{new}}) \mid \exists (I,q,a^*) \in \mathcal{C}_t,\ \{a_S^{(i)}\}_{i=1}^k \sim \pi_S^{(t)}(I,q),\ \sum_{i=1}^k \mathcal{V}(q, a_S^{(i)}, a^*) = 0 \}
$$

Solver 随后基于更新后的课程，通过 GRPO 强化学习优化策略。当所有尝试均失败时，Teacher 的参考解作为唯一正样本注入 GRPO 的正负样本集：

$$
( \mathcal{Z}^+, \mathcal{Z}^- ) = \begin{cases} \{a_S^{(i)} \mid R_i = 1\}, \{a_S^{(i)} \mid R_i = 0\} & \text{if } \sum_{i=1}^k R_i > 0 \\ \{a_{\mathrm{ref}}\}, \{a_S^{(1)}, \dots, a_S^{(k)}\} & \text{if } \sum_{i=1}^k R_i = 0 \end{cases}
$$

**协同生成副产品（Generator 训练回路）** 与核心推理回路独立运行。Teacher 在发明新问题时，将同一套符号化几何代码转化为结构化的**绘制指令（drawing instruction）**，与生成的几何图像构成 $(p_{\text{diagram}}, I_{\text{new}})$ 对。Generator（扩散模型）在这些对上进行监督微调，损失函数为标准的扩散去噪损失：

$$
\mathcal{L}_{\mathrm{SFT}}(\theta_{\mathcal{G}}) = \mathbb{E}_{ \substack{ z_0 = \mathcal{E}(I_{\mathrm{new}}), \\ \epsilon \sim \mathcal{N}(0,I), t } } \left[ \left\| \epsilon - \epsilon_{\theta_{\mathcal{G}}}(z_t, t, p_{\mathrm{diagram}}) \right\| ^2 \right]
$$

其中前向扩散噪声调度为 $z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$。

### Teacher 引擎的内部模块

Teacher 是框架的认知核心，包含四个功能模块：

1. **Verify（验证）**：形式化比对待 Solver 的响应与参考解，判定正确性。
2. **Analyze（诊断）**：执行双模态错误诊断，定位 Solver 的推理缺陷。
3. **Invent / RePI（发明）**：程序化修改 Python 几何代码，构造针对性的新几何问题与图像，确保图文对齐。
4. **Qualify / Reflect（资格验证）**：Teacher 自行求解已发明问题，仅当正确且视觉有效时才纳入课程，过滤噪声数据。

### 输入输出流

- **输入**：极少量种子几何问题（文中仅用 108 个）作为初始课程 $\mathcal{C}_0$，无需外部数据。
- **Solver 输出**：对几何问题的多模态推理链与答案；其失败路径触发新一轮数据合成。
- **Teacher 输出**：经过验证的新问题三元组（图像、问题文本、参考解），以及用于 Generator 训练的绘制指令。
- **Generator 输出**：基于绘制指令生成的精确几何图，蒸馏了 Teacher 的程序化绘图智能。

整个系统以几何数据为中心形成闭环：Solver 的弱点驱动 Teacher 发明，Teacher 的产出同时优化 Solver 的推理能力和 Generator 的生成能力，实现数据合成与模型学习的持续协同进化。

### 补充图表

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Socratic-Geo interaction framework. The system operates as a closed loop centered on geometric data. (a) The Core Reasoning Loop: The Solver attempts to solve geometry problems. Its failures trigger the Teacher, which analyzes the reasoning gaps and programmatically invents a new, targeted problem. The new validated problem triplet is added back to the curriculum, enabling continuous self-improvement for the Solver. (b) The Synergistic Generation Byproduct: Independently, the Generator learns from highquality data produced during the Teacher’s invention process. For each new problem, the Teacher performs to create a descriptive drawing instruction. The Generator is trained o...*



### 3.1 GRPO基础：序列级优势与策略优化

Socratic-Geo的Solver优化建立在**GRPO**（Group Relative Policy Optimization，组相对策略优化）之上。其核心思想是通过组内奖励归一化计算序列级优势，避免传统PPO对独立价值网络的依赖。

**优势函数**定义如下：

$$A^{(i)} = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)}$$

其中 $G$ 为组大小，$R_i$ 为第 $i$ 个采样序列的奖励值。该公式将绝对奖励转化为组内相对优势，使优化信号对奖励尺度不敏感。

**GRPO目标函数**采用PPO风格的裁剪替代损失，并引入KL正则化项约束策略更新幅度：

$$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \min(r_t(\boldsymbol{\theta}) A^{(i)}, \mathrm{clip}(r_t(\boldsymbol{\theta}), 1-\epsilon, 1+\epsilon) A^{(i)}) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

其中 $r_t(\boldsymbol{\theta})$ 为token级概率比，$\epsilon$ 为裁剪阈值，$\beta$ 控制KL惩罚强度，$\pi_{\mathrm{ref}}$ 为参考策略。

### 3.2 课程演化：失败驱动的闭环数据合成

Socratic-Geo的核心创新在于将数据合成与模型学习动态耦合。**课程演化方程**定义了闭环迭代规则：

$$\mathcal{C}_{t+1} = \mathcal{C}_t \cup \{ (I_{\mathrm{new}}, q_{\mathrm{new}}, a_{\mathrm{new}}) \mid \exists (I,q,a^*) \in \mathcal{C}_t, \{a_S^{(i)}\}_{i=1}^k \sim \pi_S^{(t)}(I,q), \sum_{i=1}^k \mathcal{V}(q, a_S^{(i)}, a^*) = 0 \}$$

该公式的含义是：当Solver在当前课程 $\mathcal{C}_t$ 的某个问题上进行 $k$ 次采样尝试，且全部失败（验证函数 $\mathcal{V}$ 返回0）时，触发Teacher发明新问题 $(I_{\mathrm{new}}, q_{\mathrm{new}}, a_{\mathrm{new}})$ 并追加到下一轮课程 $\mathcal{C}_{t+1}$ 中。

这一机制确保了合成数据**目标驱动**——Teacher仅针对Solver的薄弱环节生成新样本，而非盲目扩充数据量。

### 3.3 Teacher引擎：四模块诊断与发明流水线

Teacher是框架的**认知核心**，由四个功能模块构成（Section 4.2）：

| 模块 | 功能 | 关键机制 |
|------|------|----------|
| **Verify** | 形式化比较Solver输出与参考答案 | 判断求解正确性，触发后续诊断 |
| **Analyze** | 双模态错误诊断 | 同时分析视觉理解和逻辑推理层面的缺陷 |
| **Invent (RePI)** | 程序化修改Python几何代码 | 通过RePI机制精确构造新几何结构，确保图文严格对齐 |
| **Qualify (Reflect)** | Teacher自求解验证 | 仅当新问题可解且视觉有效时才纳入课程，过滤噪声数据 |

**RePI**（Invent模块的核心机制）是区别于现有方法的关键：Teacher不直接生成像素或自然语言描述，而是编写和修改**参数化Python脚本**来构造几何图形。这一程序化路径从根本上保证了生成图像的几何精确性。

**Qualify**模块的消融实验（Table 4）提供了决定性证据：移除该模块后，尽管训练数据量从0.4k增至1.3k，MathVerse准确率反而降至37.09%，低于零样本基线39.59%。这证明未经验证的数据引入的几何不一致和逻辑错误会严重损害推理性能，自验证是保证数据质量的必要环节。

### 3.4 Solver优化：正负样本集构造与GRPO损失

Solver的GRPO训练中，**正负样本集**的定义根据采样结果自适应调整：

$$( \mathcal{Z}^+, \mathcal{Z}^- ) = \begin{cases} \{a_S^{(i)} \mid R_i = 1\}, \{a_S^{(i)} \mid R_i = 0\} & \text{if } \sum_{i=1}^k R_i > 0 \\ \{a_{\mathrm{ref}}\}, \{a_S^{(1)}, \dots, a_S^{(k)}\} & \text{if } \sum_{i=1}^k R_i = 0 \end{cases}$$

当Solver在 $k$ 次尝试中至少成功一次时，成功的响应构成正样本集，失败的构成负样本集。**当所有尝试均失败时，以Teacher参考解 $a_{\mathrm{ref}}$ 作为唯一的正样本注入**——这是闭环学习的关键设计，确保Solver始终能从正确解中获得正向梯度信号。

基于上述正负样本集，**Solver的GRPO损失函数**为：

$$\mathcal{L}_{\mathrm{GRPO}}(\theta_S) = -\mathbb{E}_{(I,q)\sim \mathcal{C}_t} \left[ \frac{1}{|\mathcal{Z}^+ \cup \mathcal{Z}^-|} \sum_{a\in \mathcal{Z}^+\cup\mathcal{Z}^-} \frac{1}{|a|} \sum_{t=1}^{|a|} (\hat{A}_t(a) + \beta(r_t - 1)) \log \pi_{\theta_S}(a_t | I, q, a_{<t}) \right]$$

该损失对正负样本集中的所有序列进行token级优化，$\hat{A}_t(a)$ 为序列级优势，$r_t$ 为token级概率比，$\beta$ 为KL正则化系数。

### 3.5 Generator训练：程序化智能蒸馏

Generator与核心推理回路**独立但协同**。其训练数据来自Teacher发明过程中产生的**绘制指令-图像对** $(p_{\mathrm{diagram}}, I_{\mathrm{new}})$。

**Generator的监督微调损失**基于扩散模型的去噪目标：

$$\mathcal{L}_{\mathrm{SFT}}(\theta_{\mathcal{G}}) = \mathbb{E}_{ \substack{ z_0 = \mathcal{E}(I_{\mathrm{new}}), \\ \epsilon \sim \mathcal{N}(0,I), t } } \left[ \left\| \epsilon - \epsilon_{\theta_{\mathcal{G}}}(z_t, t, p_{\mathrm{diagram}}) \right\| ^2 \right]$$

其中 $\mathcal{E}$ 为VAE编码器，$z_0$ 为潜在表示，$\epsilon$ 为标准高斯噪声，$p_{\mathrm{diagram}}$ 为结构化绘图指令作为条件输入。前向扩散过程遵循标准噪声调度：

$$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$$

**Instruction Rewriting (IR)** 是将自然语言问题转化为 $p_{\mathrm{diagram}}$ 的关键步骤。消融实验（Table 5）表明，移除IR后GenExam-Math严格分数降为0.0%，松弛分数仅20.1%；保留IR则分别达到6.0%和42.4%。这说明结构化绘图指令是满足复杂数学约束、生成精确几何图的根本保障——扩散模型无法直接从自然语言中推断出精确的几何构造逻辑。

### 补充图表

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/004_Figure_4.jpg]]
*Figure 4: A concrete instantiation of the Socratic-Geo interaction pipeline, where the Teacher transforms flawed reasoning into diagnostic problems. Red highlighted regions mark critical intervention points including error diagnosis and geometric augmentation. Left: The Solver incorrectly assumes a right triangle structure, overlooking the given constraint*



## 实验与关键发现

### 核心实验结果

**几何推理能力：以1/4训练样本量超越最强基线**

Socratic-Solver在六个几何推理基准（MathVerse、GeomVerse、GeoQA、MathVision、MathVista、WeMath）上的平均准确率达**49.11%**，较零样本基线（Qwen2.5-VL-7B-Instruct）提升**+4.13个百分点**，超越最强竞争方法**2.43个百分点**（Figure 2b）。值得注意的是，这一成绩仅使用了基线方法约1/4的训练样本量（Table 1），验证了目标驱动合成范式在数据效率上的根本性优势。

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/005_Table_1.jpg]]
*Table 1: Evaluation of geometric data synthesis methods on six multimodal reasoning benchmarks: MathVerse, GeomVerse, GeoQA, MathVision, MathVista, and WeMath. Performance is reported in Mean@1 (%). Data Scale” denotes the size of synthetic training data in thousands (k), progressively growing across three curriculum stages. All results use LLM-as-judge (3-vote) evaluation. Arrow values represent absolute point changes relative to Zero-shot baseline, where green arrows indicate performance improvements and red arrows indicate performance declines. The Overall” column represents the average performance across five benchmarks (excluding GeomVerse). Best results per category are highlighted in bold. De...*

三阶段课程学习的递进效果在Table 1中清晰可见：Stage 1仅使用0.4k合成样本即达到40.70%的整体均值，超越**R-CoT**（Deng et al., arXiv 2024）的39.80%和**G-LlaVA**（Gao et al., arXiv 2025）的39.78%；Stage 3将数据量扩展至1.3k后，最终模型（49.11%）较**GeoReasoning-10K**（Xin et al., 2025）的46.68%拉开2.43个百分点的差距。这一结果的核心驱动力在于闭环课程机制：Teacher仅在Solver反复失败时才发明新问题（Equation 3），确保每一份新增数据都精准针对当前模型的推理盲区。

**几何图生成能力：开源模型新SOTA**

Socratic-Generator在GenExam-Math基准上取得**42.4%的Relaxed分数**，超越商业模型Seedream-4.0（39.8%），接近Gemini-2.5-Flash-Image（43.1%），创下开源模型在该基准上的新纪录（Figure 2a）。Strict分数为6.0%，表明模型在严格几何约束下的精确生成仍具挑战，但Relaxed分数的大幅领先证明了结构化绘图指令（Instruction Rewriting）的有效性。

**跨域泛化：任务无关的推理增益**

Table 2展示了Socratic-Geo在图表推理（Chart Reasoning）和多模态编码（Multimodal Coding）任务上的一致提升，增益范围为**+3.9至+7.6个百分点**。这一结果表明，尽管框架的核心设计围绕几何推理展开，但其目标驱动的闭环合成机制具有任务无关性，可迁移至其他需要结构化视觉理解的多模态推理场景。

### 消融实验：关键模块的必要性

**Qualify（Reflect验证）模块：质量胜于数量**

Table 4的消融结果揭示了Socratic-Geo框架中最具决定性的设计选择。移除Qualify模块后，尽管训练数据量从0.4k增至1.3k（数据量膨胀3.25倍），MathVerse准确率反而降至**37.09%**，低于零样本基线39.59%。这一负增益现象的直接原因是：未经Reflect验证的合成样本包含几何不一致（如辅助线与给定约束矛盾）和逻辑错误（如问题条件不充分导致无解），这些噪声数据在GRPO训练中污染了策略梯度信号，使模型习得错误的推理捷径。Qualify模块通过Teacher自求解验证，将课程净化率控制在极高水平，以0.4k高质量样本驱动了超越1.3k噪声样本的性能，证明了**数据质量对推理能力提升的决定性作用远大于数据规模**。

**Instruction Rewriting（IR）模块：结构化指令是精确生成的根基**

Table 5的消融实验对比了有无IR模块对生成质量的影响。移除IR后，GenExam-Math的Strict分数直接降至**0.0%**，Relaxed分数仅**20.1%**；保留IR则分别达到6.0%和42.4%。这一悬殊差距揭示了自然语言问题与几何绘图之间的语义鸿沟：自然语言描述（如“画一个三角形ABC，角A为60度”）缺乏对点坐标、线段比例、角度标注位置等精确约束的显式编码，扩散模型难以从模糊文本中推断出符合数学约束的几何结构。IR模块将自然语言翻译为结构化绘图指令（如明确指定顶点坐标和辅助线构造逻辑），使生成条件从模糊语义转化为可执行规范，是实现高保真几何图生成的根本保障。

### 失败模式分析

综合Table 4和Table 5的消融结果，可归纳出两类关键失败模式：

1. **数据质量驱动的推理退化**：当合成数据缺乏自验证时，几何不一致的图文对会引导Solver学习错误的视觉-逻辑映射。例如，若Teacher生成的图中辅助线位置与问题文本描述的约束不符，Solver可能将视觉错觉内化为推理规则，导致在干净测试集上的系统性能下降。
2. **指令模糊导致的生成失控**：在无IR的情况下，扩散模型仅依赖自然语言问题作为条件，无法准确还原角度、比例、平行关系等精确几何约束。Strict分数为0.0%表明，模型生成的几何图在严格数学意义上几乎全部不满足题目要求，仅能在视觉近似层面获得部分Relaxed分数。

### 重要图表结论

- **Figure 2**：双维度性能总览，Socratic-Geo在推理（+4.13点）和生成（42.4% Relaxed）上均实现显著突破，验证了闭环框架的双重有效性。
- **Table 1**：六基准主结果表，三阶段课程递进效果清晰，最终模型以1.3k数据超越使用更大数据量的GeoReasoning-10K，证明目标驱动合成的数据效率优势。
- **Table 4**：Qualify消融是全文最具因果说服力的实验——数据量增加但性能反降，直接证实自验证是闭环合成引擎不可移除的核心组件。
- **Table 5**：IR消融揭示了自然语言与精确几何生成之间的根本张力，Strict分数从0.0%到6.0%的跃迁说明结构化指令是解决这一张力的必要条件。

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/002_Figure_2.jpg]]
*Figure 2: Overall performance comparison demonstrating the dual effectiveness of the Socratic-Geo framework in both reasoning and generation. (a) Our Socratic-Generator-Image achieves an impressive 42.4 Relaxed score on the GenExam-Math benchmark, establishing a new state-of-the-art for open-source models and matches strong closed-source systems like Gemini-2.5-Flash-Image. (b) Our Socratic-Solver achieves an impressive 49.11% average accuracy across the reasoning benchmarks, marking a substantial +4.13 point improvement over the zero-shot baseline and consistently outperforming all other fine-tuning methods*

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/006_Table_4.jpg]]
*Table 4: Ablation study on the Qualify Module. The Qualify Module improves data efficiency, enabling better performance with fewer but higher-quality training samples*

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/008_Table_5.jpg]]
*Table 5: Ablation study on Instruction Rewriting (IR) for geometric diagram generation on GenExam-Math. IR converts natural language questions into structured drawing commands*

### 补充图表

![[assets/figures/papers/paper_list_l2188_https_openaccess_thecvf_com_content_CVPR2026_html_Jiao_Socratic_Geo_Synt/figures/007_Table_2.jpg]]
*Table 2: Generalizability to other multimodal reasoning domains. Socratic-Geo demonstrates consistent improvements across Chart Reasoning and Multimodal Coding tasks, confirming the framework is task-agnostic*



## 定位与知识库关联

### 几何推理数据合成的范式演进

当前多模态大模型在视觉几何推理领域的进展，本质上受限于高质量训练数据的稀缺性。**Socratic-Geo** 的提出，标志着该领域从“静态数据生成”向“目标驱动的动态合成”的范式跃迁。理解这一跃迁，需要将其置于现有方法谱系中审视。

**LLM驱动的被动生成范式**构成了早期基线。**R-CoT**（Deng et al., arXiv 2024）采用反向思维链策略，从答案反推问题结构，但其生成过程与模型训练完全分离，无法感知Solver的实际弱点。**G-LlaVA**（Gao et al., arXiv 2025）则通过大规模几何数据增强来扩充训练集，本质上是一种“量驱动”的粗放式策略。这类方法的共同瓶颈在于：数据合成是一次性的、静态的，无法根据模型学习状态进行动态调整。

**强化学习驱动的筛选范式**试图通过质量过滤来提升数据效用。**GeoReasoning-10K**（Xin et al., 2025）利用RL对几何图像描述进行合成，但其核心逻辑仍是“生成后过滤”——先随机探索解空间，再通过奖励信号筛选有效样本。这种范式未能解决一个根本矛盾：生成器不知道Solver的薄弱环节，因此大量合成样本可能落在模型已掌握的区域，造成计算浪费。

**Socratic-Geo的闭环范式**则从根本上重构了这一关系。其核心差异体现在三个维度：

1. **合成与学习的动态耦合**：Teacher根据Solver的失败信号（而非随机采样）来驱动数据生成。当Solver在k次尝试中全部失败时，Teacher才介入发明新问题——这种“按需生成”机制确保了每一条合成数据都针对模型当前的推理盲区。

2. **程序化验证替代启发式过滤**：通过RePI机制以Python代码程序化构造几何图形，并通过Reflect自验证确保图文严格对齐。这与GeoReasoning-10K等方法的RL筛选形成本质区别：前者在生成阶段即保证正确性，后者依赖事后过滤。

3. **课程学习的自然涌现**：闭环交互天然形成了从简单到复杂的课程结构。随着Solver能力提升，能够触发Teacher介入的问题难度也相应提高，形成持续性的能力爬坡。

### 适用边界与局限

尽管Socratic-Geo在几何推理和生成任务上均取得了显著突破，其适用边界仍需审慎界定。

**对Teacher能力的强依赖**构成了首要约束。当前框架中，Teacher的程序化几何构造能力依赖于底层LLM的编码水平。当几何问题涉及极端复杂的辅助线构造或需要非平凡的空间变换时，Teacher可能无法生成精确的Python代码来表达几何关系。这一局限直接传导至Generator训练：若Teacher无法用代码精确表达几何约束，则生成的“绘制指令-图像”对将引入系统性偏差，损害生成器的保真度。

**种子问题的多样性瓶颈**是另一个潜在风险。Socratic-Geo仅使用108个种子问题启动闭环，这意味着课程探索的广度受限于初始种子的覆盖范围。若种子集中缺乏某些几何推理类型（如立体几何、解析几何与综合几何的交叉问题），闭环课程可能无法自主探索到这些区域。

**跨模态对齐的隐式假设**值得关注。框架假设Teacher能够通过代码精确控制几何图的视觉呈现，但实际渲染过程中，Python绘图库的视觉表达可能与人类绘制的几何图存在风格差异。这种差异是否会影响Solver在真实考试场景中的泛化能力，尚缺乏系统验证。

### 开放问题与未来方向

Socratic-Geo的闭环合成范式打开了若干值得深入探索的方向。

**跨学科泛化的可能性**是最直接的延伸问题。物理、化学等STEM学科同样依赖结构化图形（如电路图、分子结构、力学示意图），这些领域的图形生成同样面临“图文精确对齐”的挑战。Socratic-Geo的程序化合成逻辑在理论上可迁移，但关键在于：这些学科是否具备类似几何学的形式化描述语言？若缺乏可执行的图形描述规范，Teacher的RePI机制将失去根基。

**Teacher能力天花板的影响**需要系统研究。文中使用Qwen2.5-VL-7B-Instruct作为基础模型，若替换为更强大的Teacher（如Gemini-2.5-Pro），闭环引擎的性能上限可能显著提升。但这也引发一个深层问题：Teacher自身的推理偏差是否会通过闭环课程被系统性放大？当Teacher对某类问题存在系统性误判时，其发明的“验证通过”的样本可能持续强化Solver的错误认知。如何形式化地确保长期课程的正确性，目前仍是开放挑战。

**数据效率的极限**同样值得追问。Socratic-Geo仅用基线1/4的训练样本即实现超越，但这是否意味着更少的数据（如仅50个种子问题）仍能维持性能？闭环课程的质量与数量之间存在何种权衡关系？消融实验已证明Reflect验证对数据质量的决定性作用，但“最小有效种子集”的边界尚未探明。



## 原文 PDF

![[paperPDFs/CVPR_2026/Socratic_Geo_Synthetic_Data_Generation_and_Cross_Modal_Geometric_Reasoning_via_Multi_Agent_Interaction.pdf]]

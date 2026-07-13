---
title: "IRG-MotionLLM: Interleaving Motion Generation, Assessment and Refinement for Text-to-Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation.pdf
project_link: null
code_link: https://github.com/HumanMLLM/IRG-MotionLLM
aliases:
- IM
- IRG-MotionLLM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在生成流程中嵌入文本-运动对齐评估和运动细化任务，并通过交错推理环（IRMoGen）实现多轮自评估与改进，从而连接理解与生成。
primary_logic: 运动评估与细化是连接理解与生成的关键任务；将它们与生成过程交错执行，并配合多阶段训练（初始化、CoT学习、强化学习），能持续提升生成动作与目标文本的对齐程度。
claims:
- 引入评估与细化任务显著提升文本-运动对齐（Stage‑1训练后，生成指标全面提升）
- 交错生成、评估和细化步骤在所有训练阶段均能持续提升生成性能
- Stage‑1模型即使未显式训练IRMoGen，通过手动组合任务即可使Top‑1从0.504升至0.522
- RL训练后模型产生更长的推理链，更多轮细化进一步改善对齐指标
---

# IRG-MotionLLM: Interleaving Motion Generation, Assessment and Refinement for Text-to-Motion Generation

> [!tip] 核心洞察
> 运动评估与细化是连接理解与生成的关键任务；将它们与生成过程交错执行，并配合多阶段训练（初始化、CoT学习、强化学习），能持续提升生成动作与目标文本的对齐程度。

| 字段 | 内容 |
|------|------|
| 中文题名 | IRG-MotionLLM：交错运动生成、评估与细化用于文本到运动生成 |
| 英文题名 | IRG-MotionLLM: Interleaving Motion Generation, Assessment and Refinement for Text-to-Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/HumanMLLM/IRG-MotionLLM) · [paper](https://arxiv.org/abs/2512.10730) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | IRG-MotionLLM |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 0.535 (Ours S3) vs 0.496 (MotionLLM) (+0.039)；FID 0.111 (Ours S2) vs 0.198 (MotionLLM) (-0.087)；MM-Dist 2.885 (Ours S2) vs 3.029 (MotionLLM) (-0.144)。
> - KIT-ML 上，R-Precision Top-1 0.445 (Ours S3) vs 0.391 (MotionLLM §) (+0.054)。

## 概要

### 问题瓶颈

现有统一运动感知大语言模型（UniMoLM，如 **MotionLLM** (Wang et al., ICLR 2025)、**MotionGPT**）将运动理解与运动生成视为两个孤立任务执行，流程中缺少对生成质量的中间评估与迭代细化环节。这种“一次生成即输出”的范式割裂了理解与生成之间的互补关系，使得模型无法利用文本-运动对齐的反馈信号持续改进生成质量，限制了文本到运动生成的上限。

### 核心思路

IRG-MotionLLM 的核心洞察是：**运动评估与细化是连接理解与生成的关键桥梁任务**。论文提出 **交错推理运动生成（IRMoGen）** 范式——将运动生成、文本-运动对齐评估、运动细化三个步骤编织为多轮推理循环。模型在生成初步运动后，自行评估其与目标文本的对齐程度，发现问题并生成细化指令，进而产生更贴合文本的运动，直至输出满意结果。

为赋予模型上述能力，IRG-MotionLLM 采用三阶段训练方案：**(1) IRMoGen 初始化**——在8个子任务（含基础理解/生成任务及评估/细化任务）上微调，建立元能力；**(2) IRMoGen思维链学习**——使用 IRMoGen-CoT 模板和“忽略错误”策略训练原生交错推理；**(3) GRPO 强化学习**——通过格式奖励、文本-运动对齐奖励和运动-运动对齐奖励释放多轮推理潜力。配套的自动数据引擎负责为目标文本生成分析标注、构造不同对齐水平的负样本对及评估/细化指令。

### 方法定位

IRG-MotionLLM 属于 **VQ-VAE + 运动感知大语言模型** 的技术路线：Motion VQVAE 将运动离散化为运动标记，扩展 LLM 词表后实现文本与运动的统一序列生成。在该路线中，本方法首次将交错式自评估与自细化机制引入生成流程，区别于 **MotionLLM** 的单步生成和 **MotionR1** 等近期推理基线，其独特之处在于**多轮、原生的文本-运动交错推理能力**。

### 主要结果

在 HumanML3D 和 KIT-ML 两个标准基准上，IRG-MotionLLM 显著超越基础模型 MotionLLM 并达到先进水平：

- **HumanML3D**：R-Precision Top-1 从 0.496 提升至 **0.535**（Stage-3），FID 从 0.198 降至 **0.111**（Stage-2），MM-Dist 从 3.029 降至 **2.885**（Stage-2）。
- **KIT-ML**：R-Precision Top-1 从 0.391 提升至 **0.445**（Stage-3）。

消融实验证实：引入评估与细化任务后，所有生成指标一致提升；交错推理在多训练阶段均持续带来增益，且 RL 训练后模型产生更长的推理链和更多轮细化，进一步改善文本-运动对齐。值得注意的是，即便 Stage-1 模型未显式训练 IRMoGen，仅通过手动组合相关任务即可使 Top-1 从 0.504 升至 0.522，验证了交错推理范式的内在有效性。

### 局限与展望

当前方法存在若干局限：VQVAE 离散化可能丢失细粒度运动细节；运动评估仅关注文本-运动对齐，未涵盖物理真实性；模型在高度复杂的多动作序列上可能遗漏个别子动作。未来工作可探索将物理真实性评估内化为 UniMoLM 的原生能力、在更大规模基础 LLM 和更丰富数据集上扩展 IRMoGen，以及引入额外保真度奖励缓解 RL 训练导致的 FID 恶化。



文本到运动生成（Text-to-Motion Generation）的目标是根据自然语言描述合成逼真的三维人体运动序列。该任务在电影制作、游戏开发、虚拟现实和机器人仿真等领域具有广泛的应用前景。近年来，基于向量量化（VQ）的运动感知大语言模型（Motion-aware LLMs，亦称 UniMoLM）逐渐成为该领域的主流范式——它们将连续运动序列离散化为运动标记（motion tokens），并扩展预训练大语言模型的词汇表，从而在统一的文本-运动空间中进行理解和生成。

然而，现有 UniMoLM 方法存在一个根本性的瓶颈：**运动理解与运动生成被当作两个孤立的任务处理**。以 **MotionLLM**（Wang et al., ICLR 2025）为代表的基线模型，虽然能够分别完成运动理解和文本到运动生成，但二者之间缺乏有效的交互反馈机制。具体而言，这些模型在生成运动后无法对生成结果进行自我评估，也无法基于评估结果对运动进行迭代改进。这种“一次性生成”的范式忽略了理解与生成之间的互补性——理解能力可以帮助识别生成运动与文本之间的错位，而细化能力则可以将这种识别转化为生成质量的提升。缺少评估与细化这两个中间任务，使得模型难以通过自我反馈持续提升文本-运动对齐程度。

本文的核心洞察在于：**运动评估与细化是连接理解与生成的关键桥梁**。将评估和细化任务嵌入生成流程，并使其与生成过程交错执行，可以形成一个自评估与自我改进的闭环，从而持续提升生成动作与目标文本的对齐程度。基于这一洞察，本文提出了 **交错推理运动生成范式**（Interleaved Reasoning for Motion Generation, IRMoGen），并构建了首个支持原生交错推理的运动感知大语言模型 **IRG-MotionLLM**。该模型能够在统一的推理过程中交替执行运动生成、文本-运动对齐评估和运动细化，直到生成满意的运动序列为止（Figure 1）。

为实现这一目标，本文面临两个关键挑战：其一，如何为现有文本-运动数据集自动构造包含评估与细化标注的训练数据；其二，如何设计有效的训练策略，使模型逐步获得并强化交错推理能力。针对第一个挑战，本文设计了自动数据引擎，通过生成目标分析、构造不同对齐水平的负样本对以及评估/细化指令来获得 IRMoGen 标注。针对第二个挑战，本文提出了三阶段训练方案：IRMoGen 初始化（Stage‑1）、IRMoGen‑CoT 学习（Stage‑2）和基于 GRPO 的强化学习（Stage‑3），逐步赋予并增强模型的原生交错推理能力。



## 核心方法与创新机理

### 瓶颈与因果机制

现有统一运动感知大语言模型（UniMoLM）将运动理解与生成作为孤立任务处理，缺少中间任务（如评估与细化）来建立文本与运动之间的交互反馈，限制了互补学习带来的性能提升。IRG-MotionLLM 的核心洞察在于：运动评估与细化是连接理解与生成的关键任务；将它们与生成过程交错执行，并配合多阶段训练，能持续提升生成动作与目标文本的对齐程度。

由此引入 **IRMoGen**（Interleaved Reasoning for Motion Generation）范式——通过迭代的文本-运动对话，将运动生成、评估与细化耦合在一起。IRG-MotionLLM 是首个原生支持 IRMoGen 的模型，其关键因果旋钮是在生成流程中嵌入文本-运动对齐评估和运动细化任务，并通过交错推理环实现多轮自评估与改进。

### 相对基线的关键创新（Changed Slots）

**1. 运动生成流程中的交互性**

- **基线（MotionLLM 等）**：理解与生成独立执行，无中间评估与细化步骤。
- **IRG-MotionLLM**：在生成过程中嵌入评估与细化步骤，形成“生成→评估→细化→再生成”的交错推理循环。证据表明，即使在 Stage-1 模型上手动组合相关任务，也能使 R-Precision Top-1 从 0.504 提升至 0.522（Table 3），验证了交互性本身的价值。

**2. 训练阶段与策略**

- **基线**：仅预训练或单阶段微调。
- **IRG-MotionLLM**：三阶段训练方案——
  - **Stage-1（IRMoGen 初始化）**：在 8 个子任务上微调，包括基础文本-运动理解/生成任务以及评估和细化任务，赋予模型元 IRMoGen 能力。
  - **Stage-2（IRMoGen‑CoT 学习）**：使用 IRMoGen‑CoT 模板和忽略错误（Ignore Incorrect）策略训练模型进行原生交错推理。消融实验表明，移除该策略会严重破坏已学习的文本-运动对齐（Table 1 Row 6 vs Row 7）。
  - **Stage-3（GRPO 强化）**：基于 GRPO 的强化学习释放多轮推理潜力，优化文本-运动对齐奖励。RL 训练后模型产生更长的推理链，更多轮细化进一步改善对齐指标（Figure 5）。

**3. 数据构造**

- **基线**：直接使用文本-运动对进行训练。
- **IRG-MotionLLM**：设计自动化数据引擎，通过排序采样生成目标分析、不同对齐水平的负样本对及评估/细化指令（Figure 4），为 IRMoGen 提供结构化训练数据。

### 创新有效性证据

- 引入评估与细化任务后，Stage-1 训练在所有文本-运动生成指标上实现稳定提升（Table 1 Row 4 vs Row 1），置信度 0.95。
- 交错生成、评估和细化步骤在所有训练阶段均能持续提升生成性能，该发现具有跨阶段一致性，置信度 0.95。
- IRG-MotionLLM 在 HumanML3D 和 KIT-ML 数据集上均显著超越 MotionLLM 基线，达到先进性能（Table 4），置信度 0.95。

### 方法局限与开放问题

**已知局限**：
- VQVAE 的离散化可能丢失细粒度运动细节。
- 运动评估仅关注文本-运动对齐，未涵盖物理真实性和平滑性。
- 模型在高度复杂的动作序列上可能遗忘个别子动作。
- 训练数据规模有限，2B 参数量可能限制泛化能力。

**开放问题**：
- 如何将物理真实性评估内化为 UniMoLM 的原生能力，并融入 IRMoGen 优化？
- 在更大规模基础 LLM 和更丰富的文本-运动数据集上扩展 IRMoGen 会带来怎样的表现？
- RL 训练造成的 FID 恶化是否可以通过引入额外的保真度奖励来缓解？



### 核心设计动机

现有统一运动感知大语言模型（UniMoLM，如 **MotionLLM** (Wang et al., ICLR 2025)）将运动理解与生成视为两个孤立任务执行，缺少中间环节来建立文本与运动之间的交互反馈。这种“任务孤岛”限制了理解能力对生成质量的互补提升。IRG-MotionLLM 的核心洞察在于：**运动评估与细化是连接理解与生成的关键任务**。通过将评估与细化嵌入生成流程，并构建交错推理循环（Interleaved Reasoning for Motion Generation, IRMoGen），模型能够在多轮自评估与改进中持续提升生成动作与目标文本的对齐程度。

### 整体架构与数据流

IRG-MotionLLM 的整体 pipeline 由三个核心模块串联构成，形成“离散化—推理—重建”的完整闭环：

1. **Motion VQVAE（运动离散化与重建）**  
   将连续运动序列离散化为 $K$ 个运动标记（motion tokens），同时具备从标记重建连续运动的能力。该模块为后续 LLM 处理运动数据提供离散化接口。

2. **Motion-aware LLM（扩展词汇的统一生成模型）**  
   在预训练基础 LLM 上扩展词汇表，加入运动标记及边界标记 `<Motion>` 和 `</Motion>`，使模型能够以统一的自回归方式处理文本与运动序列。该模块是整个系统的生成引擎。

3. **IRMoGen 推理循环（交错生成、评估与细化）**  
   给定目标文本与推理指令，模型首先进行目标分析（Goal Analysis），随后进入多轮迭代：每轮依次执行**运动生成 → 文本-运动对齐评估 → 细化指令生成 → 运动细化**。模型可自适应规划下一步动作（next move），直至生成满意结果。

### 三阶段训练方案

为赋予并增强 IRMoGen 所需能力，IRG-MotionLLM 采用三阶段训练策略（见 Figure 2）：

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/002_Figure_2.jpg]]
*Figure 2: A three-stage training scheme is proposed to build our IRG-MotionLLM. In the first stage (Upper), we endow the model with meta IRMoGen abilities via eight related tasks. In the second stage (Lower-Left), we define an IRMoGen-CoT template and train a model to explicitly couple motion understanding and generation knowledge and perform native interleaved reasoning. In the third stage (Lower-Right), we employ GRPO-based reinforcement learning to unleash the multi-round reasoning potential of the model*

- **Stage-1：IRMoGen 初始化（IRMoGen Initialization）**  
  在 8 个相关子任务上对模型进行监督微调，分为两类：
  - *基础任务（Basic Tasks）*：文本到运动生成（T2M）、运动到文本描述（M2T）、运动生成与描述联合任务等。
  - *改进任务（Improving Tasks）*：文本-运动对齐评估（Assessment）、运动细化（Refinement）等。  
  此阶段赋予模型元能力，使各子任务的知识能够互补。

- **Stage-2：IRMoGen-CoT 学习（IRMoGen-CoT Learning）**  
  定义 IRMoGen-CoT 模板（见 Figure 3），将目标分析、中间运动、评估结果和预设计划串联为思维链轨迹。采用**忽略错误策略（Ignore Incorrect）**：对不正确中间运动标记的损失和梯度进行掩码，防止错误中间结果破坏已学习的文本-运动对齐。

- **Stage-3：IRMoGen 强化（IRMoGen Reinforcing）**  
  基于 GRPO（Group Relative Policy Optimization）进行强化学习微调，释放模型的多轮推理潜力。奖励函数由三部分组成：
  - **格式奖励** $r_{\mathrm{form}}(o)$：若输出遵循 IRMoGen-CoT 模板则为 1，否则为 0。
  - **文本-运动对齐奖励** $r_{tm}(t, \mathbf{m_{final,i}}) = -\| E_t(t) - E_m(\mathbf{m_{final,i}}) \|^2$：负平方 L2 距离，衡量最终生成运动与目标文本的特征对齐程度。
  - **运动-运动对齐奖励** $r_{mm}(\mathbf{m_{gt}}, \mathbf{m_{final,i}}) = -\lVert E_m(\mathbf{m_{gt}}) - E_m(\mathbf{m_{final,i}}) \rVert^2$：负平方 L2 距离，衡量最终生成运动与真值运动之间的对齐程度。

### 自动数据引擎

为获得 IRMoGen 训练所需的多轮推理标注，论文设计了自动数据引擎（见 Figure 4），包含以下关键步骤：

1. **目标分析生成**：利用 LLM 对目标文本进行动作语义分析，生成结构化的目标分析标注。
2. **负样本对构造**：通过排序采样策略，从现有文本-运动数据集中选择不同程度对齐偏差的负样本对（negative text-motion pairs）。
3. **评估与细化指令生成**：为每个负样本对自动生成对齐评估结果和相应的细化指令，形成完整的 IRMoGen 训练数据。

### 输入输出规范

- **输入**：目标文本描述 + 推理指令（遵循 IRMoGen-CoT 模板格式）。
- **输出**：包含目标分析、多轮生成-评估-细化的完整推理轨迹，以及最终生成的满意运动序列。模型输出中的运动部分以 `<Motion>` 和 `</Motion>` 边界标记包裹，便于解析与重建。

### 关键证据支撑

- 消融实验（Table 1）证实：仅使用 T2M 任务微调会导致除 FID 外指标恶化；加入基础理解任务仅带来微弱改善；而**同时包含评估与细化任务使所有指标一致提升**，验证了评估与细化是连接理解与生成的关键桥梁。
- Stage-1 模型即使未显式训练 IRMoGen，通过手动组合任务即可使 R-Precision Top-1 从 0.504 升至 0.522（Table 3），表明交错推理的收益具有任务组合层面的基础。
- Stage-2 中移除评估与细化（w/o Asse.+Ref.）导致性能下降，且忽略错误策略对保护已学习对齐至关重要（Table 1 Row 5-7）。
- RL 训练后模型产生更长的推理链（Figure 5），更多轮细化进一步改善对齐指标（Table 3, Stage-3 final）。

### 待验证与局限

- VQVAE 离散化可能丢失细粒度运动细节，影响重建精度。
- 运动评估仅关注文本-运动对齐，未涵盖物理真实性与运动平滑性。
- 模型在高度复杂动作序列上可能遗忘个别子动作（如“抓头”）。
- RL 训练可能导致 FID 恶化，需额外保真度奖励进行缓解，该方向尚未验证。

### 补充图表

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our proposed IRG-MotionLLM.Given a goal text and reasoning instruction as input, our IRG-MotionLLM is able to perform Text-Motion Interleaved Reasoning until a satisfactory motion is generated. The reasoning process includes multiple moves, i.e., an initial analysis on the goal, followed by multiple rounds of motion Generation, Assessment, and Refinement. The model can also adaptively make plans for the next move*



### 3.1 运动标记化与统一词汇表

IRG‑MotionLLM 以预训练大语言模型（LLM）为核心，通过 **Motion VQVAE** 将连续运动序列离散化为有限数量的运动标记（motion tokens）。具体而言，给定一段运动序列，VQVAE 的编码器将其压缩为潜在表示，再经向量量化映射到码本中的离散索引，解码器则负责从这些离散标记重建连续运动。这一过程将运动数据转化为 LLM 可处理的离散符号序列。

为支持文本与运动的统一建模，模型在基座 LLM 的词汇表中扩展了运动专用码本标记，并引入边界标记 `<Motion>` 和 `</Motion>` 以界定运动片段。这种设计使得 LLM 能够以自回归方式在同一个序列中交替生成文本推理与运动标记，为后续的交错推理奠定基础。

### 3.2 三阶段训练方案

IRG‑MotionLLM 的核心能力——交错推理生成（IRMoGen）——通过三阶段训练逐步构建：

**Stage‑1：IRMoGen 初始化。** 该阶段在 8 个相关子任务上对模型进行监督微调，任务分为两类：基础文本‑运动任务（文本到运动生成、运动到文本描述等）和改进任务（文本‑运动对齐评估、运动细化等）。评估与细化任务的引入是连接运动理解与运动生成的关键——消融实验表明，仅使用基础任务只能带来微弱改善，而加入评估与细化后所有生成指标一致提升（Table 1, Row 4 vs Row 1）。

**Stage‑2：IRMoGen‑CoT 学习。** 在 Stage‑1 赋予模型元能力后，Stage‑2 通过构造的 IRMoGen‑CoT 模板训练模型进行原生交错推理。模板结构如 Figure 3 所示，包含目标分析、运动生成、对齐评估和细化指令的顺序组织。训练数据由自动数据引擎生成，将不同对齐水平的负样本文本‑运动对按对齐改善程度排序后插入 CoT 轨迹。关键技巧是 **忽略错误策略（Ignore Incorrect）**：训练时对不正确中间运动标记的损失和梯度进行掩码，防止模型因生成错误中间结果而破坏已学到的文本‑运动对齐（Table 1, Row 6 vs Row 7 证实该策略至关重要）。

**Stage‑3：IRMoGen 强化。** 在 Stage‑2 模型 $\\mathcal{F}_{s2}$ 基础上，采用基于 GRPO 的强化学习释放多轮推理潜力。奖励函数由三部分组成：

**格式奖励：**
$$r_{\\mathrm{form}}(o) = \\begin{cases} 1, & \\mathrm{if~} o \\mathrm{~follows~the~required~format}, \\\\ 0, & \\mathrm{otherwise}. \\end{cases}$$
鼓励输出遵循 IRMoGen‑CoT 模板结构，便于答案提取。

**文本‑运动对齐奖励：**
$$r_{tm}(t, \\mathbf{m_{final,i}}) = -\\| E_t(t) - E_m(\\mathbf{m_{final,i}}) \\|^2$$
其中 $E_t$ 和 $E_m$ 分别为文本编码器和运动编码器，$\mathbf{m_{final,i}}$ 为第 $i$ 条轨迹的最终生成运动。该奖励为负平方 L2 距离，衡量最终运动与目标文本在特征空间的对齐程度。

**运动‑运动对齐奖励：**
$$r_{mm}(\\mathbf{m_{gt}}, \\mathbf{m_{final,i}}) = -\\lVert E_m(\\mathbf{m_{gt}}) - E_m(\\mathbf{m_{final,i}}) \\rVert^2$$
衡量最终生成运动与真值运动之间的特征距离。

GRPO 在每组 $G$ 条采样轨迹内进行标准化优势估计，梯度更新采用如下形式的加权奖励：
$$R ( o ) = \\sum _ { i = 1 } ^ { G } \\frac { \\pi _ { \\theta } ( o _ { i } | q ) } { \\pi _ { b _ { \\mathrm { o l d } } } ( o _ { i } | q ) } \\cdot \\frac { r ( o _ { i } ) - \\mathrm { m e a n } \\left( \\{ r ( o _ { i } ) \\} _ { i = 1 } ^ { G } \\right) } { \\mathrm { s t d } \\left( \\{ r ( o _ { i } ) \\} _ { i = 1 } ^ { G } \\right) }$$
其中 $\\pi_{\\theta}$ 和 $\\pi_{b_{\\mathrm{old}}}$ 分别为当前策略和旧策略，$r(o_i)$ 为上述三项奖励的加权和。RL 训练后模型产生更长的推理链和更多轮细化，进一步改善对齐指标（Figure 5, Table 3）。

### 3.3 自动数据引擎

为支撑评估与细化任务的训练，论文设计了自动数据引擎（Figure 4）。该引擎利用预训练的文本‑运动对比模型，对数据集中每个目标文本检索一组候选运动，按对齐分数排序后选取排名靠后的 $p$ 比例样本作为负例，并自动生成对齐评估标注和细化指令。这使得现有文本‑运动数据集无需人工标注即可扩展出 IRMoGen 所需的训练信号。

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/004_Figure_4.jpg]]
*Figure 4: Negative text-motion pairs selection and annotation pipeline*

### 关键公式汇总

| 公式 | 含义 | 所在章节 |
|------|------|----------|
| $r_{\\mathrm{form}}(o)$ | 格式奖励，确保输出遵循 IRMoGen‑CoT 模板 | Sec 3.3, Eq. (1) |
| $r_{tm}(t, \\mathbf{m_{final,i}})$ | 文本‑运动对齐奖励，负 L2 距离 | Sec 3.3, Eq. (2) |
| $r_{mm}(\\mathbf{m_{gt}}, \\mathbf{m_{final,i}})$ | 运动‑真值对齐奖励，负 L2 距离 | Sec 3.3, Eq. (3) |
| $R(o)$ | GRPO 组内标准化优势加权奖励 | Appendix 8.4 |

### 补充图表

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/003_Figure_3.jpg]]
*Figure 3: The IRMoGen-CoT Template*




## 实验与关键发现

### 核心实验设置

IRG-MotionLLM 在 **HumanML3D** 和 **KIT-ML** 两个标准文本到运动生成基准上进行评估。所有实验均使用官方评估器（HumanML3D 评估器和 MARDM 评估器），各实验重复 20 次取平均值，并报告 95% 置信区间。基础模型为 **MotionLLM**（Wang et al., ICLR 2025），使用其官方权重初始化。对于使用大规模闭源数据集训练的方法，其结果在汇总表格中被灰出，以保证公平比较。

### 主结果：文本到运动生成

Table 4 报告了与现有 VQ-based 运动感知大语言模型在文本到运动生成任务上的对比。IRG-MotionLLM 在所有关键指标上均显著超越基线模型：

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/009_Table_4.jpg]]
*Table 4: Compared with existing VQ-based Motion-aware LLMs on Text-to-Motion task. *: We use the official weights of Motion-LLM [73] as our base model on the HumanML3D dataset. §: We train the base model following the official implementation of MotionLLM [73] on the KIT-ML dataset. Models with ♣ support both text and motion outputs. We also report 95% confidence intervals*

- **HumanML3D 数据集**：
  - R-Precision Top-1：Stage-3 模型达到 **0.535**，相较 MotionLLM 的 0.496 提升 **+0.039**。
  - FID：Stage-2 模型达到 **0.111**，相较 MotionLLM 的 0.198 降低 **0.087**，表示生成质量显著提高。
  - MM-Dist：Stage-2 模型达到 **2.885**，相较 MotionLLM 的 3.029 降低 **0.144**，文本-运动语义对齐更紧密。

- **KIT-ML 数据集**：
  - R-Precision Top-1：Stage-3 模型达到 **0.445**，相较 MotionLLM（按官方实现训练的基线）的 0.391 提升 **+0.054**。

这些结果表明，IRG-MotionLLM 不仅在 HumanML3D 上取得先进性能，在规模更小的 KIT-ML 数据集上同样展现出稳定的泛化能力。

### 消融实验：训练阶段与任务设计

#### 训练阶段的贡献（Table 1）

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/005_Table_1.jpg]]
*Table 1: Ablation studies of training stages on HumanML3D text-to-motion generation task. *: We use the official weights of MotionLLM [73] as our base model*

Table 1 在 HumanML3D 文本到运动生成任务上系统消融了各训练阶段的效果：

1. **仅使用 T2M 任务微调**（Row 2 vs Row 1）：除 FID 外所有指标恶化，表明单一生成任务导致过拟合。
2. **仅添加基础理解任务**（Row 3 vs Row 1）：Top-1 和 Top-2 仅有微弱改善，揭示任务孤岛限制了互补效应。
3. **包含评估与细化的全部任务（Stage-1）**（Row 4 vs Row 1）：所有指标一致提升，Top-1 从 0.496 升至 **0.504**，证实评估与细化是连接理解与生成的关键任务。
4. **Stage-2 CoT 学习**（Row 7 vs Row 4）：Top-1 进一步提升至 **0.526**，验证了交错推理链学习的增益。
5. **移除评估与细化（w/o Asse.+Ref.）**（Row 5 vs Row 7）：性能下降，显示 CoT 学习的收益确实来自多轮评估与改进。
6. **忽略错误策略（Ignore Incorrect）的关键性**（Row 6 vs Row 7）：若不使用该策略，模型在生成错误中间运动时会严重破坏已学习的文本-运动对齐，导致性能显著恶化。

#### 运动描述任务的互补验证（Table 2）

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/008_Table_2.jpg]]
*Table 2: Ablation studies of training tasks on the HumanML3D motion caption task. Combining both the basic and improving tasks brings stable improvement in text-motion alignment*

Table 2 在 HumanML3D 运动描述任务上的消融显示，同时组合基础任务和改进任务（评估与细化）在两个方向上均带来稳定的文本-运动对齐提升，进一步验证了任务间互补效应的双向性。

### 交错推理的增益分析（Table 3）

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/007_Table_3.jpg]]
*Table 3: Ablation Studies on IRMoGen on HumanML3D dataset. We observe clear improvement after adopting Interleaved Reasoning with multi-round motion assessment and refinement*

Table 3 对比了各阶段模型的初始生成与最终生成（经 IRMoGen 多轮评估与细化后）的指标：

- **Stage-1 模型**：即使未显式训练 IRMoGen，仅通过手动组合相关任务（按 Figure 7 的推理管线），Top-1 即可从 0.504 升至 **0.522**，证明交错推理范式本身即有效。
- **Stage-2 模型**：初始生成 Top-1 为 0.526，最终生成提升至 **0.534**。
- **Stage-3 模型（RL 强化后）**：最终生成达到最佳 Top-1 **0.535** 和 MM-Dist **2.785**。

值得注意的是，Stage-3 模型在 FID 上出现恶化（从 0.111 升至 0.226），这是缺乏密集监督的典型现象，在 UniMoLM 中常见。但其对齐指标（R-Precision、MM-Dist）仍具竞争力，且模型生成了更长的推理链（Figure 5），包含更多中间生成运动，表明 RL 成功释放了多轮推理潜力。

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/006_Figure_5.jpg]]
*Figure 5: Distributions of the number of generated motions in IRMoGen process. IRG-MotionLLM responses with longer reasoning with more intermediate generated motions after RL-tuning*

### 强化学习后的推理行为变化（Figure 5）

Figure 5 展示了 IRMoGen 过程中生成运动数量的分布。RL 调优后，IRG-MotionLLM 的响应包含更长的推理过程和更多的中间生成运动，这与 Stage-2 时超过 70% 的推理仅包含 1 轮生成形成鲜明对比。该趋势表明 GRPO 强化学习有效激励了模型进行更深入的多轮自评估与改进。

### 失败模式与局限性

1. **VQVAE 的离散化损失**：运动 VQVAE 的离散化过程可能丢失细粒度运动细节，这是 VQ-based 方法的固有限制。
2. **评估维度单一**：运动评估仅关注文本-运动对齐，未涵盖物理真实性和运动平滑性，可能导致生成的动作在视觉上不够自然。
3. **复杂动作序列的遗忘**：在高度复杂的动作序列上，模型可能遗忘个别子动作（如“抓头”），Figure 16 展示了此类失败案例。
4. **RL 训练的 FID 恶化**：GRPO 强化学习在改善对齐的同时导致 FID 恶化，该问题可能通过引入额外的保真度奖励来缓解。
5. **数据与模型规模限制**：训练所用数据集规模有限，模型参数量（2B LLM）可能限制进一步泛化。

### 鲁棒性评估

Figure 12 展示了鲁棒性评估的推理管线：在原生推理轨迹中将第一个生成运动替换为随机运动，观察模型是否能通过后续评估与细化恢复生成质量。定性结果（Figure 15）表明，IRG-MotionLLM 能够识别扰动带来的不对齐并进行有效修正，展现出对推理链噪声的鲁棒性。

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/020_Figure_12.jpg]]
*Figure 12: Inference pipeline for robustness evaluation. Given the reasoning instruction and a goal text, we first obtain the native reasoning trajectory of our IRG-MotionLLM. After that, we replace the first generated motion in the native reasoning trajectory to a random sampled perturbation motion, then feed the perturbed initial trajectory (containing only the goal analysis and perturbation motion) together with the instruction and goal back to the model for further reasoning*

### 作为奖励模型的应用（Table 10）

Table 10 在 AToM-general 基准上评估了 IRG-MotionLLM 作为文本-运动对齐奖励模型的潜力。以 MotionGPT 为基础模型，将 AToM 框架中的奖励模型替换为 IRG-MotionLLM 后，生成性能获得提升，表明 IRG-MotionLLM 学习到的对齐评估能力可迁移至其他运动生成器的优化中。

### 补充图表

![[assets/figures/papers/paper_list_l1834_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_f/figures/011_Figure_6.jpg]]
*Figure 6: Visualization results.Native interleaved reasoning enables IRG-MotionLLM to: (1) recognize the misalignment between previously generated motion and the goal text and provide proper refinement instructions; (2) refine the motion based on previous reasoning. Such characteristics help our method more accurately follow the details of the goal text than existing methods. The human figures are colored from light to dark to indicate the progression of time. Zoom in for the best view*



## 定位与知识库关联

### 1. 方法归类与谱系定位

IRG-MotionLLM 属于**统一运动感知大语言模型（Unified Motion-aware LLM, UniMoLM）** 这一新兴范式。该类方法的核心思路是将连续人体运动通过 VQ-VAE 离散化为运动标记，并扩展预训练 LLM 的词汇表，使模型能够以统一的自回归方式同时理解和生成文本与运动。在此谱系中，代表性工作包括：

- **MotionGPT**：较早探索文本-运动统一建模的 UniMoLM 基线。
- **MotionLLM**（Wang et al., ICLR 2025）：作为 IRG-MotionLLM 的直接基础模型与对比基线，提供了 Motion VQ-VAE 和扩展词汇表的基础架构。
- **MG-MotionLLM**：另一 UniMoLM 变体，在 Table 4 中作为对比方法出现。
- **MotionR1**：近期引入推理能力的基线方法。

IRG-MotionLLM 在该谱系中的**核心推进**在于：首次将运动生成、评估与细化三个子任务**交错嵌入同一推理流程**，形成名为 IRMoGen（Interleaved Reasoning for Motion Generation）的文本-运动交错推理范式。相较于此前 UniMoLM 将理解与生成作为孤立任务对待的做法，IRG-MotionLLM 通过建立文本-运动对齐评估和运动细化这两个“桥梁任务”，实现了理解与生成之间的互补学习。

### 2. 与基线方法的关键差异

#### 2.1 任务架构差异

| 维度 | 现有 UniMoLM（如 MotionLLM） | IRG-MotionLLM |
|------|---------------------------|---------------|
| 任务关系 | 理解与生成独立执行 | 生成-评估-细化交错循环 |
| 中间反馈 | 无 | 文本-运动对齐评估提供显式反馈 |
| 推理能力 | 单轮生成 | 多轮自评估与改进（IRMoGen） |
| 训练策略 | 预训练 + 单阶段微调 | 三阶段训练：初始化 → CoT 学习 → GRPO 强化 |

#### 2.2 训练策略差异

IRG-MotionLLM 的三阶段训练方案是其区别于基线的方法论核心：

- **Stage-1（IRMoGen 初始化）**：在 8 个子任务上微调，分为基础文本-运动任务（理解与生成）和改进任务（评估与细化），赋予模型元 IRMoGen 能力。
- **Stage-2（IRMoGen-CoT 学习）**：定义 IRMoGen-CoT 模板，采用“忽略错误策略”（Ignore Incorrect）屏蔽不正确中间运动标记的损失和梯度，训练模型进行原生交错推理。
- **Stage-3（IRMoGen 强化）**：基于 GRPO 的强化微调，使用格式奖励、文本-运动对齐奖励和运动-运动对齐奖励释放多轮推理潜力。

消融实验（Table 1）证实：仅使用 T2M 任务微调会导致除 FID 外指标恶化（过拟合）；添加基础理解任务仅微弱改善；唯有包含评估与细化的全部任务才能使所有指标一致提升。

### 3. 适用边界

#### 3.1 适用场景
- **文本到运动生成**：在 HumanML3D 和 KIT-ML 标准基准上显著超越基线，R-Precision Top-1 分别达到 0.535 和 0.445。
- **运动到文本字幕**：评估与细化任务的引入同样带来稳定的文本-运动对齐改善（Table 2）。
- **多轮交互式运动细化**：支持原生交错推理，能够识别生成运动与目标文本之间的不对齐并提供细化指令（Figure 6）。

#### 3.2 边界条件
- **VQ-VAE 离散化瓶颈**：运动 VQ-VAE 的离散化过程可能丢失细粒度运动细节，这是整个 UniMoLM 谱系的共有局限。
- **评估维度单一**：运动评估仅关注文本-运动对齐，未涵盖物理真实性（physical plausibility）和平滑性等维度。
- **复杂动作序列**：在高度复杂的动作描述上可能遗忘个别子动作（如“抓头”），如 Figure 16 的失败案例所示。
- **数据与模型规模**：训练所用数据集规模有限，基础 LLM 参数量约 2B，可能限制泛化能力。

### 4. 局限性与失效模式

1. **FID 与对齐指标的张力**：Stage-3 GRPO 强化后，FID 出现恶化趋势。原因是 RL 训练缺乏密集监督，模型倾向于生成更长的推理链和更多中间运动（Figure 5），但中间运动的质量缺乏显式约束。这一现象在 UniMoLM 中较为常见，但表明当前奖励设计未能同时保真运动质量。

2. **“忽略错误策略”的依赖性**：Table 1 的 Row 6 vs Row 7 显示，若在 Stage-2 中不使用 Ignore Incorrect 策略，训练模型生成不正确的中间运动会严重破坏已学习的文本-运动对齐。这意味着该方法对训练策略的精确实施有较高要求。

3. **评估器依赖性**：文本-运动对齐奖励依赖于预训练的特征提取器 $E_t$ 和 $E_m$，这些评估器本身的偏差和局限会传导至 RL 优化目标。

4. **推理效率**：多轮交错推理虽然提升了生成质量，但增加了推理步骤和计算开销。Stage-2 后超过 70% 的推理过程仅包含 1 轮生成（无细化），表明模型在无 RL 激励时倾向于“捷径”行为。

### 5. 开放问题

1. **物理真实性评估的内化**：如何将物理真实性评估（如关节角度合理性、足部滑动检测）内化为 UniMoLM 的原生能力，并融入 IRMoGen 的优化目标？当前仅依赖文本-运动对齐奖励可能不足以约束运动质量。

2. **规模扩展效应**：在更大规模的基础 LLM（如 7B+）和更丰富的文本-运动数据集（如 MotionMillion）上扩展 IRMoGen 会带来怎样的表现？数据引擎的自动化标注能力是否能够线性扩展？

3. **架构泛化性**：能否在更先进的 UniMoLM 架构（如 Mix-of-Transformers）上实现 IRMoGen 范式？交错推理模板是否需要对不同架构进行适配？

4. **FID 恶化的缓解**：RL 训练造成的 FID 恶化是否可以通过引入额外的运动保真度奖励（如基于物理模拟器的奖励）来缓解？或者通过约束最大细化轮数来平衡质量与效率？

5. **作为奖励模型的泛化应用**：IRG-MotionLLM 作为文本-运动对齐奖励模型的能力能否推广到其他运动生成器（如扩散模型）的 RLAIF 训练中？Table 10 的初步探索表明这一方向具有潜力，但需要更系统的验证。

6. **推理鲁棒性**：在输入文本存在扰动或模糊表述时，IRMoGen 的交错推理链是否仍能保持稳定？Figure 12 和 Figure 15 的初步评估提示了该问题，但缺乏定量分析。



## 原文 PDF

![[paperPDFs/arxiv_2025/IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation.pdf]]

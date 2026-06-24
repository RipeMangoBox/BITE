---
title: Improving Vision-language Models with Perception-centric Process Reward Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Improving_Vision_language_Models_with_Perception_centric_Process_Reward_Models.pdf
project_link: null
code_link: "https://github.com/RUCAIBox/Perceval"
aliases:
- PPCPREM
- IVLMPCPRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入感知为中心的PRM（PERCEVAL），在训练时对幻觉标记施加token级惩罚，在推理时截断错误并重生成，直接干预感知错误。
primary_logic: 视觉推理中的中间步骤多为可在图像中直接验证的感知声明，通过自动检测图像-文本不对齐，可实现细粒度的过程监督。
claims:
- 我们方法在3B和7B两个模型规模上均一致且显著超越GRPO基线。
- 最大增益来自V*pos（位置感知）任务，3B模型从86.95提升至90.43。
- 尽管PRM训练主要集中于视觉搜索，模型在数学和图表推理等领域也表现出强泛化能力。
- 截断-思考-重生成（Truncate-Thinking）在V*和BLINK上一致优于多数投票策略。
---

# Improving Vision-language Models with Perception-centric Process Reward Models

> [!tip] 核心洞察
> 视觉推理中的中间步骤多为可在图像中直接验证的感知声明，通过自动检测图像-文本不对齐，可实现细粒度的过程监督。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于感知中心过程奖励模型的视觉语言模型改进 |
| 英文题名 | Improving Vision-language Models with Perception-centric Process Reward Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.24583) · [Code](https://github.com/RUCAIBox/Perceval) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PERCEVAL (Perception-centric process reward evaluation model) |
| Dataset | V*pos, V*, Math and Chart tasks, BLINK |

> [!tip] 效果简介
> - V*pos (V-Star, 位置感知) 上，准确率 90.43 (Ours 3B) vs 86.95 (GRPO 3B) (+3.48)。
> - V* (总体) 上，平均提升 ~4% (相对提升) vs GRPO baseline (+4%)。
> - Math and Chart tasks (平均) 上，平均提升 ~3% (相对提升) vs GRPO baseline (+3%)。

## 概述

当前视觉语言模型（VLM）在复杂视觉推理任务中面临一个关键瓶颈：基于结果反馈的强化学习（RLVR）仅提供稀疏的序列级奖励，无法诊断推理链中间步骤的感知错误。当模型在思考过程中产生幻觉——例如错误描述物体位置、颜色或属性——这些错误会污染后续推理，而结局级监督对此无能为力。

本文提出 **PERCEVAL**（Perception-centric process reward evaluation model），一个以感知为中心的过程奖励模型，核心洞察在于：视觉推理中的中间步骤多为可在图像中直接验证的感知声明，通过自动检测图像-文本不对齐，可实现细粒度的过程监督。PERCEVAL 能够从模型响应中提取与图像相关的声明，逐条与视觉证据比对，生成 token 级的幻觉掩码。

方法层面的关键创新是将该掩码注入 GRPO 训练框架，将传统的序列级优势转化为 token 级惩罚：

$$\hat{A}_{i,t}^{\prime} := \hat{A}_{i} - \alpha \cdot m_{i,t} \cdot |\hat{A}_{i}|$$

其中 $m_{i,t}$ 为 PERCEVAL 输出的幻觉掩码，$\alpha$ 控制惩罚强度。这一调制机制使模型在训练时直接对感知错误 token 施加负向信号，从根源上抑制幻觉生成。在推理阶段，进一步提出截断-重生成策略：利用 PERCEVAL 定位首个错误 token，截断此前缀后重新生成，或附加反思提示引导模型自我纠正。

实验证据表明，该方法在 3B 和 7B 两个模型规模上均一致且显著超越 GRPO 基线。最大增益来自 V*pos（位置感知）任务，3B 模型从 86.95 提升至 90.43；尽管 PRM 训练主要集中于视觉搜索数据，模型在数学推理和图表推理等领域也展现出约 3% 的泛化提升。测试时缩放方面，截断-思考-重生成策略在 V* 和 BLINK 上一致优于多数投票，验证了过程级监督在推理时干预的有效性。

**方法定位**：PERCEVAL 属于过程监督 RLVR 路线，区别于 R1-VL 的步级别奖励、DeepEyes 的端到端视觉搜索 RL、以及 VL-Rethinker 的选择性样本重放等同期工作。其独特之处在于将感知核查从生成模型中解耦为独立的 PRM，通过 token 级优势重分配实现轻量但精准的干预，而非直接提供标量奖励。

## 背景与动机

视觉语言模型（VLMs）在复杂视觉推理任务中面临一个关键瓶颈：**稀疏奖励与粗糙的结局级监督无法诊断推理链中的感知错误**。当前主流的强化学习训练范式——如基于GRPO的RLVR——仅在生成完整响应后提供一个标量奖励信号，这使得模型难以定位推理过程中具体哪一步发生了感知幻觉。当模型在视觉搜索任务中错误地描述物体颜色、位置或属性时，这种粗粒度的反馈机制无法提供有效的纠正信号，导致模型反复产生相似的感知错误。

这一问题的根源在于视觉推理的中间步骤多为可在图像中直接验证的感知声明。例如，在回答“图中红色汽车旁边的交通标志是什么颜色？”时，模型需要先定位红色汽车，再识别其旁边的标志并判断颜色——每一步都对应着图像中可验证的具体事实。然而，现有的GRPO框架将整个响应的优势信号均匀分配给所有token，无法对产生幻觉的token施加针对性惩罚。

针对上述问题，本文提出了**PERCEVAL**（Perception-centric process reward evaluation model），一个以感知为中心的过程奖励模型。其核心洞察是：通过自动检测图像-文本不对齐，可实现细粒度的过程监督。PERCEVAL能够从模型生成的响应中提取图像相关的声明，逐一与图像中的视觉证据进行比对，从而定位幻觉发生的具体token跨度。在此基础上，本文引入了**token级优势重分配框架**，将PERCEVAL生成的错误掩码与GRPO的目标函数相结合，对幻觉token施加惩罚，同时保持对正确推理步骤的正向激励。这一设计直接干预了感知错误的因果链，将原本稀疏的结局级奖励转化为密集的过程级监督信号。

## 核心创新

本工作的核心创新在于提出了一种**感知中心的过程监督范式**，将传统GRPO中粗粒度的序列级优势替换为细粒度的token级优势，从而直接干预视觉推理链中的感知错误。这一范式包含三个紧密耦合的“changed slots”，共同构成了对基线GRPO的系统性改进。

### 从序列级优势到token级优势：惩罚调制的因果机制

标准GRPO为每个完整响应计算一个标量优势 $\hat{A}_i$，该优势对所有生成token施加相同的优化信号：

$$\hat{A}_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)}$$

这种序列级监督无法区分推理链中哪些token导致了最终错误，特别是当错误源于早期的感知幻觉时，模型无法获得针对性的纠正信号。本文的核心干预是将该优势替换为token级优势 $\hat{A}_{i,t}^{\prime}$：

$$\hat{A}_{i,t}^{\prime} := \hat{A}_{i} - \alpha \cdot m_{i,t} \cdot |\hat{A}_{i}|$$

其中 $m_{i,t}$ 是由PERCEVAL生成的幻觉掩码（$m_{i,t}=1$ 表示第 $t$ 个token被检测为幻觉），$\alpha$ 控制惩罚强度。这一设计的因果逻辑是：**仅对已被验证为幻觉的token施加梯度惩罚，而非对整个响应进行无差别压制**。这等价于在策略梯度中引入了一个token级的负反馈通道，使模型学会在生成过程中主动抑制与视觉证据不一致的声明。

### 监督信号的来源转变：PERCEVAL作为感知核查器

上述token级惩罚的有效性依赖于幻觉掩码 $m_{i,t}$ 的准确性。本文通过构建PERCEVAL（Perception-centric process reward evaluation model）实现了这一监督信号的自动化生成。PERCEVAL的核心能力是：从模型响应中提取图像相关的声明，逐条与图像中的视觉证据进行比对，并以结构化输出形式标注错误token的精确跨度。

与依赖人工标注或昂贵LLM评判的过程奖励模型不同，PERCEVAL通过SFT在聚合的幻觉检测数据上训练，其监督信号源于**可自动验证的图像-文本不对齐检测**。这种设计使得过程监督的规模化成为可能——无需为每个新任务重新标注过程标签。

### 推理时干预：从多数投票到截断-重生成

传统GRPO在推理时通常依赖多数投票（majority voting）来提升可靠性，但多数投票无法修正单个响应内部的系统性感知错误。本文提出的**截断-重生成（Truncate–then–Regenerate）**策略利用PERCEVAL在推理时定位错误token，截断错误前缀后让模型从干净上下文继续生成。**截断-思考-重生成（Truncate–Thinking–then–Regenerate）**进一步在截断点注入反思提示（如“Wait, I need to reconsider...”），引导模型进行自我纠正。

实验表明，这两种策略在V*和BLINK基准上一致优于多数投票：在k=16的设置下，Truncate-Thinking在V* Attr上达到94.78，而多数投票仅为92.17（+2.61）；在BLINK上达到78.95，同样超越多数投票。这一结果验证了**定位并阻断错误传播比单纯采样多数意见更有效**的核心假设。

### 创新的系统性耦合

上述三个changed slots并非孤立改进，而是形成了一个闭环：
1. **PERCEVAL** 提供token级错误掩码（监督信号源）；
2. **token级优势调制** 将该掩码转化为训练时的梯度惩罚（训练干预）；
3. **截断-重生成** 将该掩码转化为推理时的生成干预（推理干预）。

这种“检测-训练-推理”三位一体的设计使得感知错误的诊断和修复贯穿模型生命周期的关键阶段，而非仅在训练或推理单点进行优化。

## 整体框架

本文提出的 PERCEVAL 框架围绕一个核心洞察展开：视觉推理中的中间步骤多为可在图像中直接验证的感知声明，通过自动检测图像-文本不对齐，可实现细粒度的过程监督。基于此，框架将传统的**结果级稀疏奖励**升级为**token级感知错误惩罚**，形成“检测—惩罚—重生成”的闭环。

### 框架总览

整个 pipeline 由四个关键模块串联而成，如 Figure 1 所示：

![[assets/figures/papers/paper_list_l2658_https_arxiv_org_abs_2604_24583/figures/001_Figure_1.jpg]]
*Figure 1: An overview of our Process-Supervised GRPO framework. For each generated response, we use the Perceval to create a tokenlevel penalty mask. This mask is used to calculate a fine-grained token-level advantage, which is then incorporated into the GRPO objective to penalize hallucinatory tokens and improve the model’s perceptual grounding*

1. **PERCEVAL（感知中心过程奖励模型）**：接收策略模型生成的完整响应，逐 token 检测其中与图像证据不一致的幻觉片段，输出 token 级错误掩码 $m_{i,t}$。
2. **Token 级优势重分配**：将 GRPO 原本的序列级优势 $\hat{A}_i$ 按幻觉掩码调制为 token 级优势 $\hat{A}_{i,t}^{\prime}$，对有幻觉嫌疑的 token 施加惩罚。
3. **过程监督 GRPO 训练**：将调制后的 token 级优势代入 GRPO 裁剪替代目标，驱动策略模型在强化学习过程中主动规避感知错误。
4. **测试时截断-重生成**：推理阶段利用 PERCEVAL 定位错误 token 的起始位置，截断错误前缀后重新生成，或附加反思提示引导模型自我纠正。

### 模块间的数据流与因果链路

框架的因果链路可概括为：**检测 → 惩罚 → 优化 → 纠错**。

- **检测阶段**：策略模型针对输入图像和问题生成响应 $o_i$。PERCEVAL 以该响应和原始图像为输入，通过 SFT 训练获得的感知核查能力，输出一个二值掩码序列 $m_{i,t} \in \{0, 1\}$，标记每个 token 是否属于幻觉片段。这一步骤将原本不可见的中间推理错误显式化为可操作的 token 级信号。
- **惩罚阶段**：在 GRPO 的优势计算中，原本的序列级优势 $\hat{A}_i$ 仅反映整条响应的最终奖励。本文通过公式 $\hat{A}_{i,t}^{\prime} := \hat{A}_{i} - \alpha \cdot m_{i,t} \cdot |\hat{A}_{i}|$ 将其转化为 token 级优势，其中 $\alpha$ 为惩罚强度超参数。被标记的 token 的优势值被削减，从而在策略梯度中受到抑制。
- **优化阶段**：调制后的 $\hat{A}_{i,t}^{\prime}$ 直接替换 GRPO 目标中的 $\hat{A}_i$，使策略模型在最大化期望奖励的同时，被迫降低幻觉 token 的生成概率。重要的是，PERCEVAL 仅在优势计算阶段进行惩罚调制，而非直接提供标量奖励——这一设计有效避免了奖励黑客风险，训练过程中被标记为幻觉的响应比例保持稳定。
- **纠错阶段**：推理时，PERCEVAL 检测到错误 token 后，框架提供两种策略：（1）**截断-重生成**，在错误起始位置截断并继续生成；（2）**截断-思考-重生成**，截断后附加反思提示（如“等等，我需要重新更仔细地审视这个推理……”），引导模型基于正确感知重新推理。后者在 V* 和 BLINK 基准上一致优于多数投票策略。

### 关键设计决策

- **感知中心的数据构造**：PERCEVAL 主要在视觉搜索数据上通过 SFT 训练，使其专注于检测“可在图像中直接验证”的感知声明，而非泛化的逻辑错误。这一聚焦使得 token 级惩罚具有高精确度，但也限制了其对更广泛推理错误的覆盖能力。
- **选择性干预**：token 级优势调制仅在感知密集型训练数据上应用，其他数据仍使用标准 GRPO，避免对非感知任务引入强制干预，保证了方法的通用性。
- **测试时缩放**：截断-重生成策略允许模型基于自身已生成的上下文重新推理，比多数投票更贴近模型的原始分布，因而输出更稳定可靠。实验表明，当采样数 $k=16$ 时，截断-思考策略在 V* Attr 子任务上达到 94.78，显著优于多数投票的 92.17。

## 核心模块与公式推导

### 1. 问题瓶颈：稀疏奖励与感知错误

在视觉语言模型（VLM）的强化学习推理（RLVR）训练中，传统方法（如GRPO）采用**结局级稀疏奖励**：仅根据最终答案的正误给出一个标量奖励 $R_i$，然后在整个响应序列上广播相同的优势信号。这一机制存在根本性缺陷——它无法诊断推理链中发生的**感知错误**（如错误描述物体颜色、位置或属性），导致模型在复杂视觉推理任务上难以获得有效的细粒度反馈。

本文的核心洞察是：视觉推理中的中间步骤多为**可在图像中直接验证的感知声明**，通过自动检测图像-文本不对齐，可以实现细粒度的过程监督。

### 2. 核心模块：PERCEVAL 感知过程奖励模型

**PERCEVAL**（Perception-centric process reward evaluation model）是整个框架的感知核查引擎。它是一个通过监督微调（SFT）训练的过程奖励模型（PRM），核心功能是：

- **输入**：原始图像与模型生成的完整响应文本。
- **输出**：一个token级的幻觉掩码 $m_{i,t} \in \{0, 1\}$，标记响应中哪些token属于感知错误（幻觉）。
- **工作机制**：从响应中提取与图像相关的声明，逐一与图像中的视觉证据进行比对，定位不对齐的文本跨度。

PERCEVAL 主要在视觉搜索类数据上训练，其结构化输出能够精确标注错误token的起止位置，为后续的token级优势调制提供信号源。

### 3. 关键公式：从序列级优势到Token级优势

#### 3.1 标准GRPO的序列级优势

在传统GRPO中，第 $i$ 个响应的序列级优势通过组内归一化计算：

$$\hat{A}_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)}$$

其中 $G$ 为每组采样响应数，$R_i$ 为第 $i$ 个响应的结局奖励。该优势值在整个响应序列的所有token上保持不变。

#### 3.2 GRPO的裁剪替代目标

标准GRPO的优化目标为：

$$J(\theta) = \mathbb{E}_{(q,\{o_i\})\sim\pi_\theta} \Bigg[ \frac{1}{G} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \min \Big( r_{i,t}(\theta) \hat{A}_i, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{i,t}' \Big) - \beta D_{KL}(\pi_\theta || \pi_{ref}) \Bigg]$$

其中：
- $r_{i,t}(\theta) = \frac{\pi_\theta(o_{i,t}|q, o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t}|q, o_{i,<t})}$ 为重要性采样比率；
- $\epsilon$ 为裁剪阈值；
- $\beta D_{KL}$ 为与参考策略的KL散度惩罚项。

#### 3.3 Token级优势调制（核心创新）

本文的核心公式修改是将序列级优势 $\hat{A}_i$ 替换为**token级优势** $\hat{A}_{i,t}^{\prime}$：

$$\hat{A}_{i,t}^{\prime} := \hat{A}_{i} - \alpha \cdot m_{i,t} \cdot |\hat{A}_{i}|$$

变量含义：
- $\hat{A}_{i,t}^{\prime}$：第 $i$ 个响应中第 $t$ 个token的调制后优势值；
- $\hat{A}_{i}$：原始序列级优势（式1）；
- $m_{i,t} \in \{0, 1\}$：PERCEVAL 输出的幻觉掩码，$m_{i,t}=1$ 表示该token被判定为感知错误；
- $\alpha$：惩罚强度超参数，控制对幻觉token的惩罚力度；
- $|\hat{A}_{i}|$：取绝对值的序列优势，确保惩罚方向与原始优势符号无关。

**工作机制**：当 $m_{i,t}=1$ 时，该token的优势被减去 $\alpha \cdot |\hat{A}_{i}|$，从而降低其在策略更新中的正向贡献（或增大负向惩罚）。当 $m_{i,t}=0$ 时，优势保持不变。PERCEVAL **仅在优势计算阶段进行惩罚调制，而非直接提供替代奖励**，这种设计避免了引入额外的奖励模型偏差。

### 4. 推理时模块：截断与重生成

训练完成后，PERCEVAL 在推理时继续发挥作用，支撑两种测试时缩放策略：

- **Truncate–then–Regenerate**：检测到首个感知错误token后，截断其前缀，从截断点重新生成后续内容。
- **Truncate–Thinking–then–Regenerate**：截断后附加反思提示（如“Wait, I need to reconsider this reasoning more carefully...”），引导模型进行自我纠正后再生成。

## 实验与分析

### 主实验结果

我们在多模态基准上对 PERCEVAL 增强的 GRPO 训练框架进行了系统评估，涵盖视觉搜索、感知密集型推理以及数学与图表推理三大领域。Table 1 汇总了 3B 和 7B 两个模型规模下的主要结果。

![[assets/figures/papers/paper_list_l2658_https_arxiv_org_abs_2604_24583/figures/002_Table_1.jpg]]
*Table 1: Main results on multimodal benchmarks regarding visual search, perception-intensive reasoning and math&chart tasks. MRW and RWQA denote MME-RealWorld and RealWorldQA, respectively. Best and second best results in each group are highlighted in bold and underlined, respectively. ∗ indicates models capable of calling tools*

**总体趋势**：在 3B 和 7B 两个模型规模上，我们的方法一致且显著地超越了直接应用 GRPO 的基线模型。3B 模型的相对提升幅度更为突出：视觉搜索类别平均提升约 4%，数学与图表推理提升约 3%，感知密集型推理提升约 1%。7B 模型同样在所有类别上观察到正向增益，表明该方法具有良好的规模可扩展性。

**视觉搜索子任务深度分析**：最大增益来源于 V*pos（位置感知）子任务。在 3B 规模上，V*pos 准确率从 GRPO 基线的 86.95 提升至 90.43，绝对提升达 3.48 个百分点。这一结果直接验证了核心假设：PERCEVAL 对感知错误的 token 级惩罚能够有效改善模型的空间定位能力。V*attr（属性感知）子任务同样获得稳定提升，但幅度略小于位置感知任务，这可能与属性判断涉及更复杂的语义对齐有关。

**跨域泛化能力**：一个关键发现是模型的强泛化能力。尽管 PERCEVAL 的训练和 RL 干预主要集中在视觉搜索任务上，模型在数学推理（MathVision）和图表推理（ChartQA）等非直接训练领域仍表现出稳定的性能增益。这表明通过感知核查建立的过程监督机制具有跨任务迁移的价值——即使是非感知密集型任务，其推理链中也可能包含可被图像验证的中间声明。

**与其他方法的对比**：Table 1 同时列出了多个近期工作的结果，包括 VLM-R1、LMM-R1、R1-VL (StepGRPO)、Perception-R1、DeepEyes、PixelReasoner、VL-Rethinker、OpenVLThinker 和 MM-Eureka 等。在可比设置下，我们的方法在视觉搜索和感知密集型推理基准上取得了具有竞争力的结果。需要指出的是，部分方法使用了工具调用（标注 ∗），而我们的方法完全依赖模型自身能力，未引入外部工具。

**测试时缩放策略**：Table 2 比较了不同的测试时缩放策略。我们提出的 Truncate-Thinking（截断-思考-重生成）策略在 V* 和 BLINK 基准上一致优于传统的多数投票策略。在 k=16 的设置下，Truncate-Thinking 在 V* Attr 上达到 94.78，而多数投票仅为 92.17；在 BLINK 上达到 78.95，同样显著领先。Truncate（截断-重生成）策略在多数情况下也优于多数投票，但略逊于 Truncate-Thinking，说明在截断后附加反思提示能进一步引导模型进行有效的自我纠正。

### 消融实验

**惩罚强度 α 的敏感性分析**：Table 3 展示了关键超参数 α 的消融结果。α 控制对幻觉 token 施加的惩罚强度。实验表明 α = 0.1 在各项基准上取得了最佳平衡：V* 83.25、RealWorldQA 64.92、MathVision 26.32、ChartQA 85.04。当 α 增大至 0.3 时，模型性能出现下降，文本分析表明过强的惩罚导致了附带惩罚（collateral penalty）——语法连接词或必要上下文中被误标记的 token 受到了不应有的压制，反而损害了生成质量。α = 0.05 时惩罚力度不足，性能提升有限。

**奖励黑客风险监控**：Figure 2 展示了训练过程中被 PERCEVAL 标记为包含幻觉的响应比例。该比例在训练过程中趋于稳定，未出现持续下降至零的趋势，表明模型没有学会绕过 PERCEVAL 的检测（即未发生奖励黑客现象）。这一稳定性是过程监督方法可靠性的重要证据。

**优势调制方式的验证**：PERCEVAL 并非直接提供标量奖励，而是在优势计算阶段进行干预——仅降低被识别为幻觉贡献者的 token 的优势值。消融分析确认，这种间接调制方式比直接奖励替代更有效，因为它保留了 GRPO 原有的奖励信号结构，仅在必要时施加定向惩罚。

### 失败模式与局限性

尽管整体效果显著，我们在分析中识别出以下失败模式：

1. **子串匹配的附带惩罚**：PERCEVAL 的错误定位依赖精确的字符串匹配。当幻觉跨度与语法必要 token 重叠时（如连接词 "and" 或 "the" 被包含在错误跨度中），惩罚会波及这些中性 token，可能导致生成流畅度下降。这是当前 token 级掩码粒度的固有限制。

2. **非视觉任务的感知核查局限**：PERCEVAL 主要基于视觉搜索数据训练，其对数学推理中涉及图像的部分（如几何图形）有一定核查能力，但对纯符号推理链中的逻辑错误缺乏检测能力。这解释了为何数学推理的提升幅度（~3%）小于视觉搜索（~4%）。

3. **截断策略的计算开销**：测试时截断-重生成需要多次调用模型，在 k=16 的设置下计算成本显著增加。虽然性能持续提升，但在资源受限场景中需要权衡。

4. **更大规模模型的泛化性未知**：当前实验仅在 3B 和 7B 模型上进行，该方法在更大规模基础模型（如 13B、34B 或更大）上的扩展性尚未验证。更强的基础模型可能具有更好的内在感知能力，PERCEVAL 的边际收益可能递减，也可能因为更强的推理链而获得更大增益——这需要实验确认。

### 定性案例分析

Figure 3 展示了 GRPO 基线模型与我们方法在相同视觉推理问题上的推理过程对比。GRPO 基线模型在推理链中出现了明显的感知错误（如错误描述物体位置），且该错误在后续推理中被传播和放大。相比之下，经过 PERCEVAL 过程监督训练的模型在推理链中表现出更强的感知锚定——其生成的中间声明更频繁地引用图像中的具体视觉证据，且在出现不确定时表现出更谨慎的推理行为。这从定性角度印证了 token 级惩罚机制对感知基础的强化作用。

### 补充图表

![[assets/figures/papers/paper_list_l2658_https_arxiv_org_abs_2604_24583/figures/003_Table_2.jpg]]
*Table 2: Comparison of different test-time scaling strategies, where Truncate and Truncate-Thinking denote our proposed Truncate–then–Regenerate and Truncate–Thinking–then–Regenerate methods, respectively*

![[assets/figures/papers/paper_list_l2658_https_arxiv_org_abs_2604_24583/figures/004_Figure_2.jpg]]
*Figure 2: The proportion of responses identified by PERCEVAL as containing hallucinations during training*

![[assets/figures/papers/paper_list_l2658_https_arxiv_org_abs_2604_24583/figures/005_Table_3.jpg]]
*Table 3: Ablation study on the penalty strength hyperparameter α*

## 方法谱系与知识库定位

### 问题脉络：从稀疏奖励到感知过程监督

视觉语言模型（VLM）在复杂视觉推理任务中面临的核心瓶颈是**感知错误**——模型在推理链中生成与图像事实不符的声明（幻觉），而传统的强化学习验证器（RLVR）仅提供结果级的稀疏奖励，无法诊断这些中间步骤的感知失败。这一瓶颈在视觉搜索、位置感知等需要精确视觉定位的任务中尤为突出。

现有方法沿两条路径试图解决该问题。第一条路径是**改进RLVR本身**：**VLM-R1**将R1风格的RLVR扩展到VLM领域，**LMM-R1**探索基于文本规则的RL与多模态泛化，**R1-VL (StepGRPO)**用步级别奖励替代序列级奖励，**Perception-R1**针对感知密集型任务优化GRPO，**DeepEyes**、**PixelReasoner**、**VL-Rethinker**、**OpenVLThinker**和**MM-Eureka**等则从端到端RL、像素空间推理、选择性样本重放、迭代SFT-RL等不同角度进行改进。然而，这些方法本质上仍依赖结果级或粗粒度的监督信号，无法精确定位推理链中的感知错误。

第二条路径是**引入过程奖励模型（PRM）**，但传统PRM通常针对数学或代码推理设计，缺乏对视觉感知声明的细粒度核查能力。PERCEVAL正是在这一交叉点上提出了关键突破：构建一个**感知中心的过程奖励模型**，自动从响应中提取图像相关的声明，并逐一与图像中的视觉证据进行比对，从而实现对感知错误的token级定位。

### 核心机制差异：token级优势重分配

PERCEVAL与GRPO基线及其他RLVR方法的核心差异体现在四个关键维度：

| 维度 | GRPO基线 | PERCEVAL方法 |
|------|----------|-------------|
| **优势粒度** | 序列级优势 $\hat{A}_i$ | token级优势 $\hat{A}_{i,t}^{\prime}$，通过幻觉掩码调制 |
| **监督信号源** | 结果级稀疏奖励 | PERCEVAL提供的token级错误掩码 $m_{i,t}$ |
| **推理时优化** | 无或多数投票 | 截断-重生成 / 截断-思考-重生成 |
| **PRM模型** | 无 | PERCEVAL（SFT训练的感知PRM） |

具体而言，标准GRPO的优势函数为：
$$\hat{A}_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)}$$

该优势在组内归一化后对所有token均匀分配，无法区分感知正确与错误的token。PERCEVAL通过引入token级优势调制：
$$\hat{A}_{i,t}^{\prime} := \hat{A}_{i} - \alpha \cdot m_{i,t} \cdot |\hat{A}_{i}|$$

将序列优势转化为token级惩罚：当PERCEVAL检测到某token属于幻觉跨度时（$m_{i,t}=1$），其优势值被削减 $\alpha \cdot |\hat{A}_i|$。这一机制的关键在于**仅在优势计算阶段进行惩罚调制，而非直接提供标量奖励**，从而避免引入额外的奖励信号干扰原始优化目标。消融实验证实，惩罚系数 $\alpha = 0.1$ 在各项基准上取得最佳平衡，而 $\alpha = 0.3$ 则导致附带惩罚、效果下降。

### 适用边界与局限

**适用边界**：PERCEVAL的设计核心是检测可被图像直接验证的感知声明，因此其优势在**视觉搜索、位置感知、属性识别**等感知密集型任务上最为显著。实验显示，最大增益来自V\*pos（位置感知）任务，3B模型从86.95提升至90.43。尽管PRM训练主要集中于视觉搜索数据，模型在数学和图表推理等领域也表现出约3%的泛化提升，表明感知核查能力对多模态推理链具有正向溢出效应。

**已知局限**：

1. **训练数据覆盖范围**：PERCEVAL主要基于视觉搜索数据训练，对更广泛视觉推理任务（如复杂场景理解、抽象视觉关系判断）的误差检测能力可能受限。论文未提供PRM在非感知任务上的检测精度评估。

2. **计算成本**：测试时截断-重生成策略需要多次调用模型，每次截断后需重新生成，计算成本随迭代上限 $k$ 线性增长。虽然截断-思考-重生成在 $k=16$ 时达到BLINK 78.95、V\* Attr 94.78，但实际部署中 $k$ 的选择需要在性能增益与推理延迟之间权衡。

3. **字符串匹配的粗糙性**：PERCEVAL的错误定位依赖精确的字符串匹配来生成幻觉跨度掩码，可能在语法连接词或不连续跨度时产生附带惩罚。论文未深入分析子串级别标记对语法必要token的影响。

4. **模型规模验证不足**：实验仅在3B和7B两个模型规模上进行，未在更大规模基础模型上验证方法的可扩展性。泛化至更强基础模型时的效果和计算开销变化未知。

### 开放问题

1. **反思提示的数据构建**：截断-思考-重生成策略依赖PERCEVAL输出中的反思提示（如“Wait, I need to reconsider...”），但论文未详述这些反思数据的构建方式。如何系统性地改进反思提示数据，以提升模型的指令跟随质量和自我纠正能力，是一个关键工程问题。

2. **感知核查与逻辑推理的融合**：当前PERCEVAL仅核查图像-文本对齐，无法验证纯逻辑推理链的正确性。能否将感知核查能力与逻辑推理链验证相结合，实现更全面的过程监督？这需要PRM同时具备视觉定位和推理步骤评估的双重能力。

3. **跨模态迁移性**：该方法在非视觉推理任务（如纯文本数学）中的适用性如何？虽然实验显示数学推理有约3%的泛化提升，但这是否源于视觉搜索训练中的共性推理能力迁移，还是仅因模型整体质量的提升，尚需进一步消融分析。

4. **更智能的跨度切割**：如何通过更智能的跨度切割减少对语法必要token的误伤？例如，基于句法分析或语义完整性的跨度调整可能比纯字符串匹配更精准。

## 原文 PDF

![[paperPDFs/CVPR_2026/Improving_Vision_language_Models_with_Perception_centric_Process_Reward_Models.pdf]]

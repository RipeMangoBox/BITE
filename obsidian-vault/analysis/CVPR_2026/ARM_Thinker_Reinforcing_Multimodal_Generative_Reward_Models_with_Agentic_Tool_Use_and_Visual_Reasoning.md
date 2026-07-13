---
title: "ARM-Thinker: Reinforcing Multimodal Generative Reward Models with Agentic Tool Use and Visual Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ARM_Thinker_Reinforcing_Multimodal_Generative_Reward_Models_with_Agentic_Tool_Use_and_Visual_Reasoning.pdf
project_link: null
code_link: "https://github.com/InternLM/ARM-Thinker"
aliases:
- ARM-Thinker
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 模型是否具备在推理过程中自主调用多模态工具（图像裁剪、文档检索、指令检查）并基于返回的观察进行迭代验证的能力。
primary_logic: 将奖励模型从被动评分转变为主动代理，通过思考-行动-观察循环调用工具获取可验证的证据，并利用多阶段强化学习（GRPO）对工具调用决策和判断准确性进行联合优化，使奖励信号真正建立在可验证的事实之上。
claims:
- ARM-Thinker在奖励模型基准VL-RewardBench上相对基座模型Qwen2.5-VL-7B提升17.7%
- 在需要工具调用的ARMBench-VL上相对基座提升18.5%，并且在工具使用基准（V*, HRBench）上平均提升9.6%
- 消融实验证实，工具调用能力的引入是性能提升的关键——ARM-Thinker启用工具后获得稳定增益，而基座模型在启用工具时性能反降
- 自适应奖励设计在GRPO训练中达成最高准确率，同时避免工具使用不足或过度调用的问题
---

# ARM-Thinker: Reinforcing Multimodal Generative Reward Models with Agentic Tool Use and Visual Reasoning

> [!tip] 核心洞察
> 将奖励模型从被动评分转变为主动代理，通过思考-行动-观察循环调用工具获取可验证的证据，并利用多阶段强化学习（GRPO）对工具调用决策和判断准确性进行联合优化，使奖励信号真正建立在可验证的事实之上。

| 字段 | 内容 |
|------|------|
| 中文题名 | ARM-Thinker：通过代理工具使用与视觉推理增强多模态生成式奖励模型 |
| 英文题名 | ARM-Thinker: Reinforcing Multimodal Generative Reward Models with Agentic Tool Use and Visual Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.05111) · [Code](https://github.com/InternLM/ARM-Thinker) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ARM-Thinker |
| Dataset | VL-RewardBench, ARMBench-VL, RewardBench-2, V* Bench |

> [!tip] 效果简介
> - VL-RewardBench 上，Overall Accuracy 67.8 vs 50.1 (Qwen2.5-VL-7B) (+17.7)。
> - ARMBench-VL 上，Avg. Accuracy 64.6 vs 46.1 (Qwen2.5-VL-7B) (+18.5)。
> - RewardBench-2 上，Accuracy 59.6 vs 47.1 (Qwen2.5-VL-7B) (+12.5)。

## 概要

### 问题背景

多模态大模型在视觉问答、文档理解和指令遵循等任务上取得了显著进展，但作为其对齐核心的奖励模型（Reward Model）仍普遍停留在**被动评分**范式：给定一个查询和候选回答，模型执行单次前向推理即输出偏好判断。这一范式在复杂多模态场景中暴露出根本性瓶颈——模型缺乏**主动检索、定位和验证多模态证据**的能力，导致幻觉、弱视觉基础（weak visual grounding）以及对不可靠输出的误判。

### 核心方法

ARM-Thinker 将奖励模型从被动的评分器重构为**主动的代理推理系统**。其核心机制是一个显式的**思考—行动—观察循环**（think-act-observe loop）：模型在推理过程中自主决定何时调用何种多模态工具（图像裁剪与缩放、文档页面检索、文本指令检查），基于工具返回的观察结果迭代更新理解，最终生成可验证的判断。训练管道采用**冷启动监督微调 + 两阶段 GRPO 强化学习**：阶段一通过奖励塑造鼓励模型探索工具调用行为，阶段二将奖励重心转移到答案的事实正确性和工具调用的实际贡献上，实现工具使用与判断准确性的联合优化。

### 关键结论

在奖励模型基准 VL-RewardBench 上，ARM-Thinker-7B 以 **67.8%** 的准确率相较基座模型 Qwen2.5-VL-7B 提升 **+17.7%**；在需要工具调用的 ARMBench-VL 上提升 **+18.5%**；在工具使用基准（V*、HRBench 等）上平均提升 **+9.6%**。消融实验揭示了两个决定性发现：（1）基座模型在启用工具时性能反而下降，而 ARM-Thinker 获得稳定增益，表明**仅接入工具不足以提升性能，必须通过代理训练习得工具调用能力**；（2）自适应奖励设计在 GRPO 训练中同时实现最高准确率和稳定的工具调用频率，避免了仅准确率奖励导致的工具使用不足和固定工具奖励导致的过度调用。



### 多模态奖励模型的根本瓶颈

在大规模多模态模型的RLHF（基于人类反馈的强化学习）流水线中，奖励模型承担着评判生成质量、检测幻觉、评估指令遵循度的关键角色。然而，现有奖励模型的运作范式存在一个根本性瓶颈：**它们依赖单次前向评分，缺乏主动检索、定位和验证多模态证据的能力**。具体而言，当面对需要细粒度视觉感知（如识别图像局部细节）、长文档跨页检索（如从数十页PDF中定位事实依据）或多模态指令精确校验（如判断生成图像是否严格遵循排版约束）等复杂任务时，传统奖励模型仅凭一次端到端推理即输出评分，无法回溯性地检验其判断的事实基础。这一缺陷直接导致三类典型失效模式：

- **幻觉误判**：模型无法通过检索原始文档或放大图像局部来核实候选回答中的事实性陈述，从而对幻觉内容给出错误的高分。
- **弱视觉基础**：缺乏对图像局部区域的定向分析能力，使得细粒度视觉评判沦为“猜测”，而非基于可验证证据的推理。
- **不可靠输出的误判**：在指令遵循等需要精确比对的任务中，模型无法调用结构化检查工具，导致对格式错误、约束违反等问题的漏判。

### 从被动评分到主动代理的范式缺口

近年来，多模态大模型在工具使用（tool use）和代理推理（agentic reasoning）方面取得了显著进展。以**DeepEyes+**（Zheng et al., 2025）为代表的工作展示了模型通过调用图像缩放工具来增强视觉感知的潜力；通用多模态模型如**InternVL3-8B**（Zhu et al., 2025）和**GPT-4o**（Hurst et al., 2024）也在多项基准上展现了强大的综合能力。然而，这些能力并未被系统性地引入奖励模型的设计中。现有专门的多模态奖励模型如**UnifiedReward-7B**（Wang et al., 2025c）仍然遵循“输入-评分”的单步范式，其训练目标聚焦于偏好排序的准确性，而非证据收集与验证的完整性。

这一缺口的核心在于**因果调节变量**的缺失：模型是否具备在推理过程中自主调用多模态工具（如图像裁剪、文档检索、指令检查）并基于返回的观察进行迭代验证的能力。仅有工具接口的接入并不足以解决问题——如后续消融实验所揭示的，基座模型在启用工具时性能反而下降，说明**工具调用能力需要与专门的代理训练深度耦合**，才能使模型学会在恰当的时机选择恰当的工具，并将工具返回的证据有效融入最终的判断决策。

### 本文的核心洞察与动机

ARM-Thinker的核心洞察在于：**将奖励模型从被动评分转变为主动代理，通过“思考-行动-观察”循环调用工具获取可验证的证据，并利用多阶段强化学习对工具调用决策和判断准确性进行联合优化，使奖励信号真正建立在可验证的事实之上**。

为实现这一目标，ARM-Thinker在三个维度上进行了根本性的范式变革：

1. **推理范式**：从单次前向评分转向显式的思考-行动-观察循环，模型在推理过程中自主规划、调用多模态工具、整合观察结果，形成可追溯的证据链。
2. **训练策略**：从标准监督微调（SFT）升级为冷启动SFT + 两阶段GRPO强化学习——第一阶段鼓励工具调用探索，第二阶段侧重于准确率和可验证的工具效用，通过层次化奖励设计平衡工具使用的充分性与必要性。
3. **工具集成**：构建统一的多模态工具包，涵盖图像裁剪/缩放、文档页面检索、文本指令检查三类工具，基于OpenAI风格的函数调用接口实现无缝集成。

这一范式转变的动机直接源于对奖励模型可靠性需求的深刻理解：在RLHF流程中，奖励模型的系统性偏差会通过策略优化被放大，最终损害对齐效果。唯有让奖励模型具备主动验证的能力，才能从根本上提升其评判的可信度，为下游的模型对齐提供更坚实的信号基础。



## 核心方法与创新机理

ARM-Thinker的核心创新在于将奖励模型从**被动评分器**重构为**主动代理**，使其能够在推理过程中自主调用多模态工具获取可验证证据，并通过多阶段强化学习对工具调用决策与判断准确性进行联合优化。这一转变体现在三个关键维度的设计变更上。

### 推理范式：从单次前向评分到思考-行动-观察循环

传统多模态奖励模型（如Qwen2.5-VL-7B、UnifiedReward-7B）采用单次前向评分范式——接收问题、图像和候选回答后直接输出偏好判断，缺乏对多模态证据的主动检索与验证能力。ARM-Thinker将推理过程重构为显式的**思考-行动-观察循环**（think-act-observe loop）：

- **思考（Think）**：模型分析当前上下文，规划下一步推理或工具调用策略
- **行动（Act）**：根据思考结果，通过统一接口调用多模态工具（图像裁剪、文档检索、指令检查）
- **观察（Observe）**：接收工具返回的结果，更新索引化的文本和图像上下文

这一范式使奖励判断建立在可验证的事实基础之上。形式上，每条推理轨迹 $\tau$ 由多轮思考-工具调用-观察元组组成：

$$\tau = \{ ( \theta_{0}, t_{0}, o_{0} ), ( \theta_{1}, t_{1}, o_{1} ), \dots, ( \theta_{L}, t_{L}, o_{L} ) \}$$

其中 $\theta$ 为思考步骤，$t$ 为工具调用，$o$ 为观察结果，$L$ 为轨迹长度。模型在迭代循环中持续收集证据，直至生成最终答案。

### 训练策略：从标准SFT到两阶段GRPO强化学习

传统奖励模型的训练通常停留在监督微调（SFT）阶段，无法系统性地优化工具调用的决策质量。ARM-Thinker引入了**冷启动SFT + 两阶段GRPO**的训练策略：

**冷启动阶段**：利用LLaVA-Critic及工具特定数据集构建偏好对 $\mathcal{D}_{\mathrm{pair}} = \{ ( q, I, r^{+}, r^{-} ) \}$，其中负面样本 $r^{-}$ 由GPT-4o-mini生成，经格式、准确性和行为三维度过滤后，形成高质量的有工具交互轨迹数据，用于对Qwen2.5-VL-7B进行初始微调。

**GRPO阶段一（工具调用鼓励）**：通过奖励塑造鼓励模型主动尝试调用工具，奖励函数设计为：

$$\mathcal{R}_{\mathrm{tool}} = \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{\mathrm{try}} \cdot \mathbb{I}_{tool\_calls > 0}$$

其中 $\mathcal{R}_{\mathrm{f}}$ 为格式奖励，$\mathcal{R}_{\mathrm{try}}$ 为工具尝试奖励，仅在轨迹含有工具调用时给予正向激励。

**GRPO阶段二（准确性优化）**：在模型形成稳定工具使用模式后，将奖励重心转移到答案的事实正确性和工具调用的实际贡献上，采用层次化奖励函数：

$$\mathcal{R}_{\mathrm{acc}} = \begin{cases} \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{\mathrm{try}}, & \text{if } \mathcal{R}_{a}=0 \text{ and } tool\_calls>0 \\ \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{a}, & \text{if } \mathcal{R}_{a}>0 \text{ and } succ\_tool\_calls=0 \\ \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{a} + \mathcal{R}_{\mathrm{succ}}, & \text{if } \mathcal{R}_{a}>0 \text{ and } succ\_tool\_calls>0 \end{cases}$$

该设计根据答案正确性（$\mathcal{R}_{a}$）和成功工具调用（$\mathcal{R}_{\mathrm{succ}}$）的组合分情况给予差异化奖励，既避免工具使用不足，也抑制过度调用。

### 工具集成：从无工具能力到统一多模态工具接口

ARM-Thinker集成了三类多模态工具，统一基于OpenAI风格的函数调用接口：

- **图像操作工具**：支持图像裁剪和缩放，用于细粒度视觉细节的定位与验证
- **文档检索工具**：支持多页文档的页面检索与导航，用于长文档QA中的证据定位
- **指令检查工具**：支持文本指令的逐项验证，用于多模态指令遵循任务

所有工具继承自统一的 `baseTool` 接口，模型通过标准化的函数调用模式参数化工具请求并整合返回结果。这一设计使工具调用成为推理轨迹的自然组成部分，而非外部后处理步骤。

### 创新点的因果验证

消融实验为上述创新提供了因果证据（Table 5）：当基座模型Qwen2.5-VL-7B启用工具调用时，性能反而下降，表明**仅有工具接入不足以提升判断质量**；而ARM-Thinker在关闭工具时仍保持与基座相当的性能，启用工具后则获得稳定增益。这证实了代理训练（两阶段GRPO）是使工具调用产生正向收益的关键机制。

奖励函数消融（Figure 4）进一步表明，ARM-Thinker的自适应奖励设计在GRPO训练中实现了最高准确率（约80%）和稳定的工具调用频率（约1.12次/样本），优于仅准确率奖励（工具使用不足）和固定工具奖励（工具使用过度）的设计，验证了层次化奖励在平衡探索与效率方面的有效性。



ARM-Thinker 的核心创新在于将奖励模型从“被动评分器”转变为“主动代理”，其整体框架围绕一个显式的 **思考-行动-观察循环** 展开。模型不再依赖单次前向传播给出评分，而是在推理过程中自主决定何时调用何种多模态工具，基于工具返回的观察结果迭代验证，最终产出有据可依的判断。

### 推理范式：思考-行动-观察代理循环

ARM-Thinker 的推理过程被建模为一条由多个元组构成的结构化轨迹：

$$\tau = \{ ( \theta_{0}, t_{0}, o_{0} ), ( \theta_{1}, t_{1}, o_{1} ), \dots, ( \theta_{L}, t_{L}, o_{L} ) \}$$

其中每个元组包含三个要素：**思考**（θ，模型的内部推理规划）、**工具调用**（t，向外部工具发起的函数调用请求）和**观察**（o，工具返回的图像或文本证据）。模型在循环中维护一个索引化的上下文内存，同时存储文本和图像信息，直到产生最终答案。

这一范式使奖励模型的行为发生了质变：它不再凭空猜测答案的优劣，而是通过工具主动检索、定位和验证多模态证据。例如，在长文档 QA 任务中，模型可以调用文档页面检索工具定位关键段落；在细粒度图像感知任务中，可以调用图像裁剪/缩放工具放大局部区域进行精确比对。

### 工具集成：统一接口下的三类多模态工具

ARM-Thinker 集成了三类多模态工具，所有工具继承自统一的 `baseTool` 接口，并暴露 OpenAI 风格的函数调用 schema，使模型能够以标准化的方式参数化调用并整合返回结果：

- **图像操作工具**：支持图像裁剪和缩放，用于细粒度视觉细节的放大和定位。
- **文档检索工具**：支持对长 PDF 等文档进行页面级检索和导航。
- **指令检查工具**：用于验证文本指令的遵循情况，如格式要求、内容约束等。

这种统一的工具接口设计使得模型无需针对不同工具学习不同的调用协议，降低了工具使用的学习成本，也为未来扩展更多工具类型提供了可插拔的架构基础。

### 训练管道：冷启动 + 两阶段强化学习

ARM-Thinker 的训练管道分为三个递进阶段，如 Figure 2(b) 所示：

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ARM-Thinker’s architecture and training pipeline. (a) Agent Loop: ARM-Thinker follows a think-act-observe paradigm, maintaining indexed context for texts and images while iteratively invoking tools from the toolkit (image zoom-in, document retrieval, instruction validators) until producing the final answer. (b) Pipeline: our pipeline starting with (1) SFT & Cold Start using difficulty-filtered data, followed by (2) two-stage Group Relative Policy Optimization Shao et al. (2024)(GRPO) that first encourages correct tool calls (Stage 1) and then refines for accuracy with verifiable rewards that balance correctness and tool efficiency (Stage 2)*

1. **冷启动数据生成与监督微调**：首先基于 LLaVA-Critic 及工具特定数据集构建偏好对，由 GPT-4o-mini 生成负面样本，经格式、准确性和工具调用行为三维过滤后形成高质量的多模态轨迹数据。随后使用这些数据对基座模型 Qwen2.5-VL-7B 进行监督微调，初始化基本的奖励判断能力和工具使用行为。

2. **GRPO 阶段一：工具调用鼓励**：在群组相对策略优化框架下，通过奖励塑造鼓励模型主动尝试调用工具。阶段一奖励函数为：

   $$\mathcal{R}_{\mathrm{tool}} = \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{\mathrm{try}} \mathbb{I}_{tool\_calls > 0}$$

   其中 $\mathcal{R}_{\mathrm{f}}$ 为格式奖励，$\mathcal{R}_{\mathrm{try}}$ 为工具尝试奖励——只要轨迹中含有工具调用即给予正向激励，帮助模型形成稳定的工具使用模式。

3. **GRPO 阶段二：准确性优化**：在模型学会正确调用工具后，奖励重心转移到答案的事实正确性和工具调用的实际贡献上，采用层次化的准确性奖励：

   $$\mathcal{R}_{\mathrm{acc}} = \begin{cases} \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{\mathrm{try}}, & \text{if } \mathcal{R}_{a}=0 \text{ and } tool\_calls>0 \\ \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{a}, & \text{if } \mathcal{R}_{a}>0 \text{ and } succ\_tool\_calls=0 \\ \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{a} + \mathcal{R}_{\mathrm{succ}}, & \text{if } \mathcal{R}_{a}>0 \text{ and } succ\_tool\_calls>0 \end{cases}$$

   该设计根据答案是否正确（$\mathcal{R}_{a}$）以及是否有成功的工具调用（$\mathcal{R}_{\mathrm{succ}}$）分情况给予不同奖励分量，在鼓励工具使用的同时避免过度调用。

### 输入输出流

框架的输入为多模态上下文（问题 + 图像/文档）和候选回答，输出为经过工具验证后的判断结果。整个流程中，模型在每轮循环中自主决定：是否需要调用工具、调用哪个工具、如何解读工具返回的观察，最终基于累积的证据链给出评分或偏好判断。这种设计使得奖励信号真正建立在可验证的事实之上，而非模型的内部猜测。

### 补充图表

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/001_Figure_1.jpg]]
*Figure 1: Overview of ARM-Thinker. (a) Case Comparison: Given a complex document QA task, ARM-Thinker correctly identifies the answer by autonomously invoking the retrieval tool, while the baseline model provides an incorrect response. (b) ARMBench-VL: It evaluates reward models across three task types, each requiring specialized tool use (image manipulation, document retrieval, instruction verification). (c) Performance of ARM-Thinker: The agentic capability enables substantial gains across multiple benchmarks*



ARM-Thinker 的核心设计围绕**代理式推理循环**与**两阶段强化学习训练管道**展开，将传统被动评分的奖励模型转变为主动调用多模态工具进行证据收集与验证的代理系统。

### 代理推理循环

ARM-Thinker 的推理过程遵循**思考-行动-观察**（think-act-observe）范式。给定多模态输入后，模型在每轮迭代中自主决定是否需要调用工具、调用哪个工具，并将工具返回的观察结果整合进推理上下文，直至生成最终判断。整个过程形式化为一条推理轨迹：

$$
\tau = \{ ( \theta_{0}, t_{0}, o_{0} ), ( \theta_{1}, t_{1}, o_{1} ), \dots, ( \theta_{L}, t_{L}, o_{L} ) \}
$$

其中 $\theta_i$ 为第 $i$ 步的思考（reasoning thought），$t_i$ 为工具调用（tool invocation），$o_i$ 为工具返回的观察（observation），$L$ 为轨迹总步数。模型维护一个索引化的上下文记忆，同时存储文本和图像信息，确保多轮工具调用间的信息连贯性。

### 工具集成架构

ARM-Thinker 集成了三类多模态工具，统一基于 OpenAI 风格的函数调用接口（`baseTool`）：

- **图像裁剪/缩放工具**：支持对图像局部区域进行高分辨率放大，用于细粒度视觉感知任务；
- **文档页面检索工具**：支持在长文档（如 PDF）中按页码或内容检索，用于多模态长文档 QA；
- **文本指令检查工具**：验证模型输出是否满足指定的指令约束，用于多模态指令遵循任务。

所有工具遵循统一的调用模式：模型输出结构化的函数调用参数，系统执行后返回文本或图像观察，模型据此更新推理状态。

### 冷启动数据生成与过滤

训练数据以偏好对形式构建：

$$
\mathcal{D}_{\mathrm{pair}} = \{ ( q, I, r^{+}, r^{-} ) \}
$$

其中 $q$ 为问题，$I$ 为输入图像，$r^{+}$ 为正确答案，$r^{-}$ 为由 GPT-4o-mini 生成的错误答案。正负样本对经过三维度过滤——**格式正确性**、**答案准确性**、**工具调用行为成功性**——仅保留高质量的有工具交互轨迹数据，用于后续监督微调（SFT）冷启动。

### 两阶段 GRPO 强化学习

冷启动 SFT 后，ARM-Thinker 采用两阶段 GRPO（Group Relative Policy Optimization）进行强化学习优化。对于一组 $n$ 条轨迹：

$$
\mathcal{G} = \{ ( \tau_{i}, a_{i} ) \}_{i=1}^{n}
$$

其中 $\tau_i$ 为完整推理轨迹，$a_i$ 为最终答案。

**阶段一：工具调用鼓励。** 奖励函数设计为：

$$
\mathcal{R}_{\mathrm{tool}} = \mathcal{R}_{\mathrm{f}} + \mathcal{R}_{\mathrm{try}} \cdot \mathbb{I}_{tool\_calls > 0}
$$

其中 $\mathcal{R}_{\mathrm{f}}$ 为格式奖励（确保输出结构正确），$\mathcal{R}_{\mathrm{try}}$ 为工具尝试奖励，当轨迹中包含任意工具调用（$tool\_calls > 0$）时给予正向激励。此阶段目标是让模型建立稳定的工具使用行为模式。

**阶段二：准确性优化。** 在模型学会正确调用工具后，奖励重心转移到答案的事实正确性和工具调用的实际贡献上，采用层次化奖励函数：

$$
\mathcal{R}_{\mathrm{acc}} = \begin{cases}
\mathcal{R}_{\mathrm{f}} + \mathcal{R}_{\mathrm{try}}, & \text{if } \mathcal{R}_{a}=0 \text{ and } tool\_calls>0 \\[4pt]
\mathcal{R}_{\mathrm{f}} + \mathcal{R}_{a}, & \text{if } \mathcal{R}_{a}>0 \text{ and } succ\_tool\_calls=0 \\[4pt]
\mathcal{R}_{\mathrm{f}} + \mathcal{R}_{a} + \mathcal{R}_{\mathrm{succ}}, & \text{if } \mathcal{R}_{a}>0 \text{ and } succ\_tool\_calls>0
\end{cases}
$$

其中 $\mathcal{R}_{a}$ 为答案正确性奖励（答案错误时为 0），$succ\_tool\_calls$ 表示是否有成功的工具调用。该设计分三种情况给予差异化奖励：(1) 答案错误但尝试了工具调用——仅给予格式和尝试奖励；(2) 答案正确但无成功工具调用——给予格式和答案奖励；(3) 答案正确且有成功工具调用——额外给予工具成功奖励 $\mathcal{R}_{\mathrm{succ}}$。这种层次化设计既避免了对工具调用的盲目鼓励，又确保工具使用真正服务于判断准确性。

### 关键设计决策

消融实验（Figure 4）证实，该自适应奖励函数在 GRPO 训练中实现了**最高准确率**（约 80%）和**稳定的工具调用频率**（约 1.12 次/样本），优于仅准确率奖励（工具使用不足）和固定工具奖励（工具使用过度）的设计。此外，多模态指令遵循任务相关的工具使用数据未在 GRPO 阶段显式加入，但模型经训练后能够自然泛化，证明了框架的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/004_Figure_3.jpg]]
*Figure 3: Representative examples from ARMBench-VL. Each block shows the multimodal context, candidate responses, and available tools for one of the three tracks in ARMBench-VL: Fine-grained Perception (image crop/zoom tools for local visual details), Multimodal Long Document QA (page-retrieval tools), and Multimodal Instruction Following (instruction-checking tools)*



## 实验与关键发现

### 核心实验设置

ARM-Thinker以**Qwen2.5-VL-7B**（Bai et al., 2025）作为基座模型，经冷启动SFT后通过两阶段GRPO进行强化学习训练。评估覆盖三大类基准：（1）多模态奖励模型基准（VL-RewardBench、RewardBench-2、ARMBench-VL）；（2）视觉工具使用基准（V* Bench、HRBench系列）；（3）多模态数学与逻辑推理基准（WeMath等）。对比基线包括专门多模态奖励模型**UnifiedReward-7B**（Wang et al., 2025c）、通用多模态模型**InternVL3-8B**（Zhu et al., 2025）、商业模型**GPT-4o**（Hurst et al., 2024）以及支持图像缩放工具的**DeepEyes+**（Zheng et al., 2025）。

### 奖励模型基准主结果

Table 2展示了ARM-Thinker在三个奖励模型基准上的表现。在VL-RewardBench上，ARM-Thinker-7B达到**67.8%**的整体准确率，较基座模型Qwen2.5-VL-7B的50.1%提升**+17.7个百分点**，并全面超越UnifiedReward-7B（54.5%）和GPT-4o（57.1%）。在幻觉检测子任务上，ARM-Thinker达到80.5%，较基座提升+22.9个百分点，显示出工具调用对验证事实准确性的关键作用。

在ARMBench-VL上，ARM-Thinker平均准确率达**64.6%**，较基座（46.1%）提升**+18.5个百分点**。三个子任务——细粒度感知（FG）、指令遵循（IF）和文档理解（Doc）——分别提升至69.4%、65.4%和58.9%，表明代理式推理在所有任务类型上均带来一致增益。在纯文本奖励基准RewardBench-2上，ARM-Thinker同样取得59.6%（+12.5%），证明工具调用训练并未损害文本评估能力，反而通过强化推理链产生了正向迁移。

### 视觉工具使用基准结果

Table 3报告了在需要迭代工具调用的视觉分析基准上的表现。ARM-Thinker在四个基准上的平均准确率达**76.5%**，较基座（66.9%）提升**+9.6个百分点**。其中V* Bench达到86.4%（+11.0%），HRBench-4K达到80.1%（+11.0%）。值得注意的是，ARM-Thinker-7B在多个基准上超越了参数量更大的模型（如DeepEyes+），表明代理式工具调用策略比单纯增大模型规模更有效。

### 推理基准泛化能力

Table 4展示了向数学与逻辑推理任务的泛化结果。ARM-Thinker在WeMath上达到**46.1%**（+10.9%），在MathVerse上达到35.8%（+9.2%），在LogicVista上达到44.1%（+7.6%）。这些基准并非专门为工具调用设计，但ARM-Thinker仍展现出稳定的提升，说明代理式推理训练赋予了模型更审慎的思考习惯和更强的验证能力，这些能力可泛化至未见任务类型。

### 消融实验：工具调用的因果作用

Table 5的消融实验是验证工具调用因果作用的关键证据。实验对比了基座模型Qwen2.5-VL-7B和ARM-Thinker在**启用/禁用工具调用**两种条件下的性能。结果显示：
- **基座模型启用工具时性能反而下降**：在VL-RewardBench上从50.1%降至46.8%，在ARMBench-VL上从46.1%降至43.2%。这表明单纯接入工具接口不足以提升性能，模型需要专门的代理训练才能有效利用工具。
- **ARM-Thinker禁用工具时仍保持竞争力**：在VL-RewardBench上达到62.3%，已显著高于基座模型，说明GRPO训练本身提升了模型的推理和判断能力。
- **ARM-Thinker启用工具后获得稳定增益**：在VL-RewardBench上进一步提升至67.8%（+5.5%），在ARMBench-VL上提升至64.6%（+4.6%）。这证明工具调用能力是性能提升的独立贡献因子，且与推理能力产生正向协同。

### 奖励函数设计消融

Figure 4对比了三种GRPO奖励函数设计的训练动态：
- **仅准确率奖励（橙色）**：工具使用频率持续下降，最终趋近于零，模型退化为不使用工具的纯推理模式，准确率受限。
- **固定工具奖励（绿色）**：工具调用频率过高（约1.8次/样本），模型出现过度调用问题，准确率反而受损。
- **ARM-Thinker自适应奖励（蓝色）**：工具调用频率稳定在约**1.12次/样本**，同时达到最高准确率（约80%），在工具使用效率与判断准确性之间取得最优平衡。

该消融验证了层次化奖励设计（阶段一鼓励工具尝试，阶段二根据工具实际贡献给予差异化奖励）对塑造稳定且高效的工具使用模式至关重要。

### 失败模式与局限性

尽管ARM-Thinker取得了显著提升，论文揭示了若干值得关注的局限：
1. **分布外工具选择错误**：当前工具集覆盖图像裁剪、文档检索和文本指令检查三类，在遇到需要其他类型工具（如视频帧分析、代码执行）的任务时，模型可能错误地选择不适用工具或放弃调用，导致判断失误。
2. **工具调用失败缺乏鲁棒恢复**：论文未探讨当工具返回空结果或错误观察时，模型是否具备重试或切换策略的能力。在ARMBench-VL的文档理解任务中，检索工具可能返回不相关页面，此时模型的应对行为尚未系统评估。
3. **规模扩展性未验证**：实验仅在7B参数规模上进行，更大模型（如72B）上的代理训练收益和工具调用行为变化仍是开放问题。
4. **主观性评估任务空白**：当前实验聚焦于事实正确性和指令遵循等可验证任务，对于美学质量、创造性等主观维度，如何设计合适的工具和奖励信号尚未涉及。

### 补充图表

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/005_Table_2.jpg]]
*Table 2: Results on Reward Model benchmarks. We report the performance on three benchmarks (M=multimodal, T=text-only): VL-RewardBench tests hallucination detection (Hallu.), reasoning evaluation (Reason.), and general judgment (General). RewardBench-2 evaluates text-only pair-wise reward accuracy. ARMBench-VL assesses fine-grained perception (FG), instruction following (IF), and document understanding (Doc). ARM-Thinker achieves substantial improvements over baselines across all benchmarks*

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/008_Table_5.jpg]]
*Table 5: Ablation: Tool Use vs. No Tool Use. We evaluate both Qwen2.5-VL-7B (baseline) and ARM-Thinker with tool calling disabled (default) or enabled (w/ tool) across three benchmarks. The baseline model fails to benefit from tools, showing performance degradation when tools are enabled. ARM-Thinker maintains strong performance without tools (comparable to baseline) but achieves consistent gains when tools are enabled*

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/009_Figure_4.jpg]]
*Figure 4: Ablation study comparing three reward function designs during GRPO training. Left: Evaluation accuracy over training steps. Right: Average tool-call frequency over training steps. Our ARM-Thinker reward (blue) achieves the highest accuracy while maintaining stable tool usage, avoiding both the under-use pitfall of accuracy-only rewards (orange) and the over-use pitfall of fixed tool rewards (green)*

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/006_Table_3.jpg]]
*Table 3: Results on visual tool-use (Think-with-Images) benchmarks. We evaluate ARM-Thinker-7B against baselines on four benchmarks requiring iterative tool use for finegrained visual analysis. The symbol † indicates that results are copied from Lai et al. (2025)*

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/007_Table_4.jpg]]
*Table 4: Generalization to multimodal math and logical reasoning benchmarks. We evaluate ARM-Thinker against baseline models on six reasoning benchmarks covering general knowledge, math and logical reasoning*

![[assets/figures/papers/paper_list_l2150_https_arxiv_org_abs_2512_05111/figures/003_Table_1.jpg]]
*Table 1: Comparison of ARMBench-VL with other reward benchmarks (M=multimodal, T=text-only)*



## 定位与知识库关联

### 1. 问题定位：从被动评分到主动代理验证

现有奖励模型（Reward Model, RM）的核心瓶颈在于**单次前向评分范式**——模型接收多模态输入后直接输出偏好判断，缺乏主动检索、定位和验证证据的能力。这一缺陷在需要细粒度视觉感知、长文档检索或多模态指令遵循的场景中尤为突出：模型可能因忽略局部视觉细节而产生幻觉，或因无法检索文档中的关键页面而给出不可靠的判断。ARM-Thinker 将这一瓶颈作为切入点，将奖励模型从**被动评分器**重构为**主动代理**，通过显式的“思考-行动-观察”循环（think-act-observe loop）调用多模态工具，使奖励信号建立在可验证的事实之上。

### 2. 与基线工作的关系

#### 2.1 基座模型对比

ARM-Thinker 以 **Qwen2.5-VL-7B**（Bai et al., 2025）为基座模型进行对比。该基座模型代表当前主流的多模态大模型能力水平，但本身不具备工具调用能力，在需要主动检索证据的任务中表现受限。ARM-Thinker 在相同基座上通过冷启动 SFT 与两阶段 GRPO 训练，在不改变模型架构的前提下赋予其代理推理能力，实现了从“被动判断”到“主动验证”的范式跃迁。

#### 2.2 专用多模态奖励模型

**UnifiedReward-7B**（Wang et al., 2025c）是现有的专门多模态奖励模型，但其设计与传统 RM 一致，依赖单次前向评分。ARM-Thinker 与之的核心区别在于引入工具调用循环，使模型能够在推理过程中动态收集证据。实验表明，ARM-Thinker-7B 在 VL-RewardBench 上达到 67.8%，较基座模型提升 17.7%（Table 2），在需要工具调用的 ARMBench-VL 上平均准确率达 64.6%，提升 18.5%。

#### 2.3 通用多模态模型与商业模型

与 **InternVL3-8B**（Zhu et al., 2025）和 **GPT-4o**（Hurst et al., 2024）等通用多模态模型相比，ARM-Thinker 并非追求通用能力，而是专注于**奖励判断的可靠性**。其代理设计使得模型在判断前能主动检索证据，而非仅依赖内部知识或单次视觉编码。在视觉工具使用基准（V* Bench、HRBench-4K 等）上，ARM-Thinker-7B 平均准确率达 76.5%，较基座模型提升 9.6%（Table 3）。

#### 2.4 支持工具调用的模型

**DeepEyes+**（Zheng et al., 2025）支持图像缩放工具，但其工具使用能力是通过特定任务训练获得的，缺乏统一的代理推理框架。ARM-Thinker 的关键区别在于：通过统一的 OpenAI 风格函数调用接口集成三类多模态工具（图像裁剪/缩放、文档页面检索、文本指令检查），并利用强化学习对工具调用决策和判断准确性进行联合优化，而非仅在特定任务上硬编码工具使用模式。

### 3. 方法谱系中的位置

ARM-Thinker 处于以下三条研究线的交汇点：

| 研究线 | 代表工作 | ARM-Thinker 的继承与突破 |
|--------|---------|------------------------|
| **多模态奖励模型** | UnifiedReward, LLaVA-Critic | 继承偏好判断的基本框架，突破单次前向评分的局限，引入代理循环 |
| **工具增强推理** | DeepEyes+, V* | 继承工具调用的思想，但将工具集成从特定任务推广到统一的代理框架，并通过 GRPO 优化工具使用策略 |
| **强化学习对齐** | GRPO (Shao et al., 2024), RLHF | 继承 GRPO 的组相对策略优化方法，但针对代理奖励模型设计了层次化奖励函数，平衡工具调用探索与判断准确性 |

### 4. 适用边界与局限

1. **工具集的覆盖范围有限**：当前工具集主要覆盖图像裁剪、文档检索和文本指令检查三类操作。对时空推理、视频理解等更复杂模态的支持尚未验证，模型在这些场景下的代理能力仍是开放问题。

2. **工具调用的可靠性依赖奖励设计**：消融实验（Figure 4）表明，仅使用准确率奖励会导致工具使用不足，固定工具奖励则导致过度调用。ARM-Thinker 的自适应奖励在训练过程中达到了最优平衡，但在分布外场景中仍可能出现工具选择错误或过度调用。论文未探讨工具调用失败时的鲁棒恢复机制。

3. **规模扩展性未验证**：当前实验主要在 7B 参数规模上进行（Qwen2.5-VL-7B 基座），更大规模模型上的扩展性和收益尚未评估。代理推理引入的额外计算开销与模型规模的交互关系是未知的。

4. **主观评估任务的适用性**：在更具主观性的评估任务（如美学判断、创造性评价）中，当前工具集难以提供可验证的证据，如何设计合适的工具和奖励信号仍是开放问题。

### 5. 开放问题与后续工作方向

1. **多模态扩展**：代理奖励模型是否能够无缝扩展到视频和时空推理领域，以处理动态多模态数据的验证？这需要设计新的工具类型（如视频帧检索、时间定位）和相应的训练策略。

2. **可解释性增强**：工具调用的决策过程是否可以进一步结构化，以提供可解释的因果链，而不仅仅是最终得分？当前的思考-行动-观察循环已经提供了比传统 RM 更透明的推理轨迹，但将其转化为可审计的因果链仍需进一步研究。

3. **实时性权衡**：如何平衡工具调用的计算开销与奖励模型的实时性要求，使其适用于在线 RLHF 流程？代理循环的迭代性质天然增加了推理延迟，这在需要高吞吐量的在线训练场景中可能成为瓶颈。

4. **工具调用的鲁棒性**：在工具调用失败或返回噪声观察时，模型应具备怎样的恢复策略？当前框架缺乏显式的错误处理机制，这在实际部署中可能影响可靠性。

5. **跨任务泛化的理论理解**：论文观察到模型在未显式加入指令遵循任务相关工具使用数据的情况下，工具使用能力能够自然泛化（Section A.2）。这一泛化现象的机理尚待深入分析，可能为理解代理能力的涌现提供线索。



## 原文 PDF

![[paperPDFs/CVPR_2026/ARM_Thinker_Reinforcing_Multimodal_Generative_Reward_Models_with_Agentic_Tool_Use_and_Visual_Reasoning.pdf]]

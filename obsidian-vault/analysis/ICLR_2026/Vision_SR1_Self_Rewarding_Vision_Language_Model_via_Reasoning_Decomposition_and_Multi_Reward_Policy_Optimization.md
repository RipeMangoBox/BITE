---
title: "Vision-SR1: Self-Rewarding Vision-Language Model via Reasoning Decomposition and Multi-Reward Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Vision_SR1_Self_Rewarding_Vision_Language_Model_via_Reasoning_Decomposition_and_Multi_Reward_Policy_Optimization.pdf
project_link: null
code_link: https://github.com/zli12321/Vision-SR1
openreview_forum_id: C1M4ETatgM
aliases:
- VS
- Vision-SR1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将VLM的推理过程分解为可视描述与语言推理两个阶段，并通过模型自我评估其生成的视觉描述是否完备且足以支撑正确答案，从而实现自奖励（self-reward）；同时采用解耦的多奖励策略优化，分别为视觉奖励和语言推理奖励计算独立的优势函数、对数概率和KL散度，避免信号纠缠。"
primary_logic: "通过将视觉感知与语言推理解耦，并利用模型自身作为评判者来验证视觉描述的完备性，可以在不依赖外部监督的情况下强化视觉基础、减少语言捷径，从而有效缓解幻觉并提升多模态推理能力。"
claims:
- "Vision-SR1 将推理分解为自包含的视觉感知和语言推理，并通过自我奖励验证视觉完备性。"
- "多奖励策略优化通过独立的优势计算和分离的损失项，为视觉和答案信号提供精确的梯度路径。"
- "Vision-SR1 在多个基准测试中一致优于仅使用答案奖励的Vision-R1，并在消融实验中证明自奖励带来的性能提升。"
- "自奖励显著降低了语言捷径率（LSR），表明模型更少依赖语言先验。"
---

# Vision-SR1: Self-Rewarding Vision-Language Model via Reasoning Decomposition and Multi-Reward Policy Optimization

> [!tip] 核心洞察
> 通过将视觉感知与语言推理解耦，并利用模型自身作为评判者来验证视觉描述的完备性，可以在不依赖外部监督的情况下强化视觉基础、减少语言捷径，从而有效缓解幻觉并提升多模态推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Vision-SR1: 基于推理分解与多奖励策略优化的自奖励视觉语言模型 |
| 英文题名 | Vision-SR1: Self-Rewarding Vision-Language Model via Reasoning Decomposition and Multi-Reward Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=C1M4ETatgM) · [GitHub](https://github.com/zli12321/Vision-SR1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Vision-SR1 |
| Dataset | MMMU-Pro, MMMU, RealWorld QA, HallusionBench |

> [!tip] 效果简介
> - MMMU-Pro 上，准确率 为 40.7，对比 39.8 (Vision-R1 47K)，变化 +0.9。
> - MMMU 上，准确率 为 52.2，对比 51.8 (Vision-R1 47K)，变化 +0.4。
> - RealWorld QA 上，准确率 为 69.2，对比 66.6 (Vision-R1 47K)，变化 +2.6。

## 概要

当前视觉语言模型（VLM）的后训练方法普遍仅依赖最终答案的正确性作为监督信号，导致中间视觉推理缺乏明确指导，模型倾向于依赖语言先验而非视觉感知，从而引发视觉幻觉与语言捷径问题。针对这一瓶颈，**Vision-SR1** 提出了一种自奖励（self-rewarding）框架，核心思路是将VLM的推理过程解耦为**可视描述**与**语言推理**两个阶段，并利用模型自身作为评判者来验证视觉描述的完备性——若仅凭生成的视觉描述即可推出正确答案，则赋予视觉奖励。配合解耦的多奖励策略优化（分别计算视觉与答案奖励的优势函数、对数概率和KL散度），该方法在不引入外部监督模型的前提下，强化了视觉基础、抑制了语言捷径。

在方法谱系上，Vision-SR1 建立在以 **GRPO**（Shao et al., 2024）为代表的组相对策略梯度框架之上，与仅使用答案奖励的 **Vision-R1**（Huang et al., 2025b）、依赖外部专有MLLM提供视觉监督的 **Perception-R1**（Xiao et al., 2025）以及通过外部纯文本LLM生成结构化输出的 **Visionary-R1**（Xia et al., 2025）形成对比。Vision-SR1 的关键改进在于：将奖励信号从单一的答案正确性扩展为答案奖励与视觉自奖励的组合，同时将输出强制结构化为 `⟨visual.reasoning⟩`、`⟨think⟩`、`⟨answer⟩` 三段，并在优化时将视觉与答案rollout的优势计算和KL惩罚彻底解耦，避免了信号纠缠。

实验表明，Vision-SR1 在7项基准上的平均准确率较Vision-R1（同等47K数据集复现）提升了1.5个百分点（Qwen2.5-VL-7B: 52.2 vs. 50.7），在空间推理基准OmniSpatial上提升尤为显著（+13.1）。消融实验证实，移除视觉自奖励会导致平均性能下降（7B: 52.2 → 50.3），而语言捷径率（LSR）的降低进一步验证了自奖励对抑制语言先验依赖的有效性。此外，自奖励机制还一定程度上缓解了多模态RL训练带来的纯文本数学推理退化。



视觉语言模型（VLM）在复杂多模态推理任务中取得了显著进展，但其后训练范式长期存在一个核心瓶颈：监督信号仅来自最终答案的正确性，中间视觉推理过程缺乏显式指导。这一设计缺陷导致模型在训练中倾向于依赖语言先验而非真实的视觉感知，从而产生视觉幻觉和语言捷径——模型可能给出正确答案，但其视觉推理却是错误的。

当前基于强化学习的VLM后训练方法，如**Vision-R1**（Huang et al., 2025b），采用GRPO（Group Relative Policy Optimization）框架，仅以答案匹配的二元奖励作为优化目标。尽管这类方法在数学推理等任务上表现突出，但答案奖励无法区分“真正看懂图像”与“靠语言线索猜对”这两种行为，使得模型在视觉理解基准上的提升受限。为弥补这一缺陷，**Perception-R1**（Xiao et al., 2025）和**Visionary-R1**（Xia et al., 2025）等方法尝试引入外部监督——前者调用专有MLLM提取视觉标注作为额外奖励，后者借助纯文本LLM生成caption-reason-answer格式的监督信号。然而，这些方案依赖于外部模型的计算开销和标注质量，无法实现端到端的自监督优化。

本文的动机源于一个关键洞察：如果模型的视觉描述足够完备，能够在不依赖原始图像的情况下支撑正确答案的推理，那么该描述本身就是高质量的视觉感知证据。基于此，Vision-SR1提出将VLM的推理过程显式分解为**视觉感知**与**语言推理**两个阶段，并利用模型自身作为评判者来验证视觉描述的完备性——这一**自奖励**机制无需任何外部模型或人工标注，即可为视觉感知提供精准的梯度信号。同时，针对简单奖励求和可能引发的奖励黑客问题，Vision-SR1设计了**多奖励策略优化**，为视觉奖励和答案奖励分别计算独立的优势函数、对数概率和KL散度，从根本上避免信号纠缠。



## 核心方法与创新机理

### 1. 推理分解与自奖励机制

Vision-SR1 的核心创新在于将 VLM 的推理过程显式分解为两个自包含的阶段，并利用模型自身作为评判者来验证视觉感知的完备性，从而在不引入外部监督的前提下实现自奖励（self-reward）。

**输出结构强制分解。** 与仅生成推理链和答案的 Vision-R1 不同，Vision-SR1 要求模型输出严格遵循三段式结构：`⟨visual.reasoning⟩...⟨/visual.reasoning⟩`、`⟨think⟩...⟨/think⟩`、`⟨answer⟩...⟨/answer⟩`。其中视觉推理部分被要求具备**自包含性**——即仅凭该描述就足以回答问题，无需回看原始图像。这一设计强制模型将视觉感知与语言推理在表征层面分离，为后续的独立评估与优化提供基础。

**双轮次自奖励验证。** 训练过程中模型经历两次前向推理（Figure 1）：

- **第一轮次（答案rollout）：** 模型接收图像与问题，生成完整的结构化输出，依据最终答案的正确性获得答案奖励 $r_{ans}$。
- **第二轮次（视觉rollout）：** 仅使用第一轮生成的视觉描述 $c$ 与问题 $q$ 重新推理，产生答案 $\hat{a}$。若 $\hat{a}$ 与正确答案 $a^*$ 一致，则赋予视觉奖励 $r_{visual} = \mathbb{I}[\hat{a} = a^*]$（Equation 3）。

这一机制的核心洞见在于：**如果仅凭视觉描述就能推导出正确答案，则说明该描述是完备且准确的**。反之，若视觉描述存在幻觉或信息缺失，第二轮推理将无法得出正确答案，视觉奖励为零。由此，模型通过自我评判获得了针对中间视觉感知的细粒度反馈信号，无需依赖外部标注或专有模型。

### 2. 多奖励策略优化

Vision-SR1 在策略优化层面进行了关键改造，将视觉奖励与答案奖励的解耦从信号层面贯彻到梯度层面。

**独立优势计算。** 与标准 GRPO 对整条响应计算单一组相对优势不同，Vision-SR1 分别为答案奖励和视觉奖励计算组内 z-score 标准化优势（Equation 6）：

$$A_{ans}^{(i)} = \frac{r_{ans}^{(i)} - \mu_{ans}}{\sigma_{ans} + \varepsilon}, \quad A_{visual}^{(i)} = \frac{r_{visual}^{(i)} - \mu_{visual}}{\sigma_{visual} + \varepsilon}$$

这一设计消除了两类奖励之间的尺度耦合，使优势信号分别反映模型在答案准确性和视觉完备性两个维度上的相对表现。

**分离的损失项与 KL 惩罚。** Actor 损失对答案 token 和视觉 token 分别使用各自的优势进行加权（Equation 7），KL 散度正则化同样对两类序列独立施加惩罚（Equation 8）。这种**解耦的多奖励优化**确保了：
- 视觉奖励的提升不会因答案奖励的优势波动而被稀释或放大；
- 策略更新时，视觉感知和语言推理各自获得精确的梯度路径，避免了信号纠缠导致的 reward hacking。

### 3. 外部资源需求的根本性改变

| 维度 | Vision-R1 / GRPO | Perception-R1 | Vision-SR1 |
|------|------------------|---------------|------------|
| 中间视觉监督 | 无 | 外部专有 MLLM 提取标注 | 模型自我评估 |
| 额外 GPU / API 调用 | 无 | 需要部署外部模型 | 无（仅增加一次前向推理） |
| 训练时间开销 | 基准（~10.5h / 20 steps, 7B） | 显著增加 | +20%（~13h / 20 steps, 7B） |

Vision-SR1 通过自奖励机制完全消除了对外部视觉监督模型（如 Perception-R1 依赖的专有 MLLM）的需求，同时双轮次训练仅比标准 GRPO 增加约 10-15% 的时间开销（Section 2.4.1），远优于部署额外奖励模型的方案。

### 4. 关键消融验证

Table 6 的消融实验直接验证了上述创新的有效性：移除视觉感知自奖励后（即仅保留答案奖励和结构化输出格式），Qwen2.5-VL-7B 在 7 项基准上的平均准确率从 52.2 降至 50.3，降幅达 1.9 个百分点。这一对比排除了输出格式变化带来的混淆效应，证明**自奖励信号本身是性能提升的核心驱动力**。

此外，Table 4 显示自奖励使 7B 模型的平均语言捷径率（LSR）从 10.1 降至 9.8，表明模型更少依赖语言先验猜测答案，而是更多地基于视觉感知进行推理——这正是推理分解与自奖励机制设计的直接目标。



![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_C1M4ETatgM/figures/001_Figure_1.jpg]]
*Figure 1: Overall framework of Vision-SR1. During RL training the VLM has two rollouts. In the first pass, the model takes an image–query pair and generates a structured output (visual perception, CoT reasoning, and answer), with answer reward computed against the ground truth. In the second pass, the model is re-prompted to answer using only query and its generated visual perception. If the correct answer is derived, a self-visual reward is assigned. We compute the advantages and log probabilities for each rollout for Multi-Reward Policy Optimization*

Vision-SR1 的整体框架围绕一个核心洞察展开：**将视觉感知与语言推理解耦，并利用模型自身作为评判者来验证视觉描述的完备性**，从而在不依赖外部监督的情况下强化视觉基础、减少语言捷径。框架由三个紧密衔接的模块构成，形成“生成—验证—优化”的闭环。

### 第一轮次：标准答案 Rollout

模型接收图像 $I$ 和问题 $Q$，按照强制结构化格式生成输出：

```
⟨visual.reasoning⟩ c ⟨/visual.reasoning⟩
⟨think⟩ t ⟨/think⟩
⟨answer⟩ a ⟨/answer⟩
```

其中 $c$ 是**自包含的视觉描述**——要求该描述在脱离原图的情况下，仍能支撑后续推理得出正确答案。$t$ 为思维链推理，$a$ 为最终答案。此轮依据 $a$ 与标准答案 $a^*$ 的匹配程度计算答案奖励：

$$r_{ans}(Q, a) = r_{acc}(Q, a) + \alpha \, r_{fmt}(s) \quad \text{(式 4)}$$

其中 $r_{acc}$ 为答案正确性二元奖励，$r_{fmt}$ 为格式合规奖励。

### 第二轮次：自奖励视觉 Rollout

这是框架的**核心创新**——视觉自我奖励机制。模型仅接收问题 $Q$ 和第一轮生成的视觉描述 $c$（**不提供原图**），重新推理产生答案 $\hat{a}$：

$$\hat{a} = f_{\theta}(c, q), \quad r_{visual}(Q, c) = \mathbb{I}[\hat{a} = a^*] \quad \text{(式 3)}$$

若基于视觉描述 $c$ 能独立得出正确答案，则视觉奖励为 1，否则为 0。这一机制的本质是**让模型自我验证其视觉感知是否完备且足以支撑正确推理**，从而为视觉基础提供明确的梯度信号。视觉奖励同样叠加格式奖励：

$$r_{visual}(Q, a) = r_{vis.acc}(Q, a) + \alpha \, r_{fmt}(s) \quad \text{(式 5)}$$

该自奖励过程**无需外部奖励模型或额外 GPU 部署**，完全依赖模型自身完成评估。

### 多奖励策略优化

标准 GRPO 对整条响应使用单一组优势进行更新，这会导致视觉信号与答案信号相互纠缠。Vision-SR1 的**多奖励策略优化**将两轮 rollout 的解耦贯穿于整个更新过程：

1. **独立优势计算**：对答案奖励和视觉奖励分别在组内计算 z-score 标准化优势，消除问题级别偏差：

   $$A_{ans}^{(i)} = \frac{r_{ans}^{(i)} - \mu_{ans}}{\sigma_{ans} + \varepsilon}, \quad A_{visual}^{(i)} = \frac{r_{visual}^{(i)} - \mu_{visual}}{\sigma_{visual} + \varepsilon} \quad \text{(式 6)}$$

2. **分离的策略梯度**：Actor 损失对视觉和答案 token 分别使用各自的优势加权，提供精确的梯度路径：

   $$\mathcal{L}_{actor} = -\frac{1}{2B} \sum_{i,t} \left( A_{ans,t}^{(i)} \log \pi_{\theta}(a_{ans,t}^{(i)}) + A_{visual,t}^{(i)} \log \pi_{\theta}(a_{visual,t}^{(i)}) \right) \quad \text{(式 7)}$$

3. **解耦的 KL 正则化**：对答案序列和视觉序列分别施加 KL 惩罚，防止策略偏离参考模型：

   $$\mathcal{L}_{KL} = \frac{\beta_{ans}}{B} \sum_{i,t} \left[ \log \pi_{ref}(a_{ans,t}^{(i)}) - \log \pi_{\theta}(a_{ans,t}^{(i)}) \right] + \frac{\beta_{visual}}{B} \sum_{i,t} \left[ \log \pi_{ref}(a_{visual,t}^{(i)}) - \log \pi_{\theta}(a_{visual,t}^{(i)}) \right] \quad \text{(式 8)}$$

4. **总损失**：$$\mathcal{L}_{total} = \mathcal{L}_{actor} + \mathcal{L}_{KL} \quad \text{(式 9)}$$

### 效率分析

两轮 rollout 相比标准 GRPO 增加了约 10–15% 的训练开销：7B 模型在 8 GPU 上训练 20 步，标准 GRPO 约需 10.5 小时，Vision-SR1 约需 13 小时。这一开销远低于部署外部奖励模型（如 Perception-R1 需额外 GPU 或 API 调用），且完全在可接受范围内。

### 与基线方法的关键差异

| 维度 | Vision-R1 | Perception-R1 | Vision-SR1 |
|------|-----------|---------------|------------|
| 奖励信号 | 仅最终答案正确性 | 答案奖励 + 外部 MLLM 提取的视觉标注奖励 | 答案奖励 + 模型自我验证的视觉奖励 |
| 输出结构 | 无中间视觉描述要求 | 依赖外部模型提供标注 | 强制自包含视觉描述 |
| 优势计算 | 单一组优势 | 未明确解耦 | 视觉与答案独立优势 |
| 外部资源 | 无 | 需外部专有 MLLM | 完全自包含 |

这一框架通过推理分解与多奖励解耦优化，实现了**在不引入外部监督的前提下，为视觉感知提供明确的强化信号**，从而有效缓解视觉幻觉和语言捷径问题。



### 3.1 两阶段自奖励推理框架

Vision-SR1 的核心创新在于将 VLM 的推理过程解耦为**视觉感知**与**语言推理**两个独立阶段，并通过模型自身的自奖励机制验证视觉描述的完备性。具体流程如 Figure 1 所示，包含两个顺序的 rollout：

**第一轮次（标准 rollout）**：模型接收图像-问题对，生成结构化的三段式输出：
```
⟨visual.reasoning⟩ c ⟨/visual.reasoning⟩
⟨think⟩ t ⟨/think⟩
⟨answer⟩ a ⟨/answer⟩
```
其中 $c$ 为自包含的视觉描述，$t$ 为思维链推理，$a$ 为最终答案。该轮次依据答案正确性与格式规范计算答案奖励。

**第二轮次（自奖励 rollout）**：仅使用问题 $q$ 与第一轮生成的视觉描述 $c$ 重新推理，产生答案 $\hat{a}$。若 $\hat{a}$ 与真实答案 $a^*$ 一致，则赋予视觉奖励 1，否则为 0：

$$ \hat{a} = f_{\theta}\left( c, q \right), \quad r_{\mathrm{visual}}(Q, c) = \mathbb{I} \left[ \hat{a} = a^{*} \right] \tag{3} $$

**关键设计意图**：第二轮次中模型无法访问原始图像，仅依赖视觉描述 $c$ 作答。若此时仍能得出正确答案，则说明 $c$ 包含了足够完备的视觉信息。这一机制直接惩罚了依赖语言先验的"捷径"行为——当 $c$ 不完备时，模型无法通过语言线索弥补视觉缺失，从而迫使模型在第一轮中生成更精确的视觉描述。

### 3.2 奖励信号设计

Vision-SR1 使用两组独立的奖励信号，分别对应两个 rollout：

**答案奖励**（第一轮次）由答案准确性与格式奖励加权组成：

$$ r_{ans}(Q, a) = r_{\mathrm{acc}}(Q, a) + \alpha \, r_{\mathrm{fmt}}(s) \tag{4} $$

**视觉奖励**（第二轮次）由视觉推理准确性与格式奖励加权组成：

$$ r_{visual}(Q, a) = r_{\mathrm{vis.acc}}(Q, a) + \alpha \, r_{\mathrm{fmt}}(s) \tag{5} $$

其中 $r_{\mathrm{acc}}$ 为答案匹配的二元奖励，$r_{\mathrm{fmt}}$ 为对结构化输出格式（⟨visual.reasoning⟩、⟨think⟩、⟨answer⟩ 标签完整性）的格式奖励，$\alpha$ 为格式奖励权重。

### 3.3 多奖励策略优化

与标准 GRPO 对整条响应使用单一优势信号不同，Vision-SR1 的**多奖励策略优化**为视觉和答案信号分别计算独立的优势函数、对数概率和 KL 散度，避免信号纠缠。

**组内 z-score 标准化**：对于每个问题 $Q$ 的 $K$ 个采样响应，分别计算答案奖励和视觉奖励的组内 z-score 优势：

$$ A_{\mathrm{ans}}^{(i)} = \frac{r_{\mathrm{ans}}^{(i)} - \mu_{\mathrm{ans}}}{\sigma_{\mathrm{ans}} + \varepsilon}, \quad A_{\mathrm{visual}}^{(i)} = \frac{r_{\mathrm{visual}}^{(i)} - \mu_{\mathrm{visual}}}{\sigma_{\mathrm{visual}} + \varepsilon} \tag{6} $$

其中 $\mu$ 和 $\sigma$ 为组内均值和标准差，$\varepsilon$ 为防止除零的小常数。z-score 标准化消除了问题难度带来的奖励尺度差异，使视觉和答案信号在统一的量级上进行比较。

**解耦的 Actor 损失**：策略梯度损失对视觉和答案 token 分别使用各自的优势进行加权：

$$ \mathcal{L}_{\mathrm{actor}} = -\frac{1}{2B} \sum_{i,t} \left( A_{\mathrm{ans},t}^{(i)} \log \pi_{\theta}(a_{\mathrm{ans},t}^{(i)}) + A_{\mathrm{visual},t}^{(i)} \log \pi_{\theta}(a_{\mathrm{visual},t}^{(i)}) \right) \tag{7} $$

其中 $B$ 为批次大小，$a_{\mathrm{ans},t}^{(i)}$ 和 $a_{\mathrm{visual},t}^{(i)}$ 分别表示答案 rollout 和视觉 rollout 中第 $t$ 个 token。

**解耦的 KL 正则化**：对答案和视觉序列分别施加 KL 惩罚，防止策略偏离参考模型 $\pi_{\mathrm{old}}$：

$$ \mathcal{L}_{\mathrm{KL}} = \frac{\beta_{\mathrm{ans}}}{B} \sum_{i=1}^{B} \sum_{t} \left[ \log \pi_{\mathrm{old}}(a_{\mathrm{ans},t}^{(i)}) - \log \pi_{\theta}(a_{\mathrm{ans},t}^{(i)}) \right] + \frac{\beta_{\mathrm{visual}}}{B} \sum_{i=1}^{B} \sum_{t} \left[ \log \pi_{\mathrm{old}}(a_{\mathrm{visual},t}^{(i)}) - \log \pi_{\theta}(a_{\mathrm{visual},t}^{(i)}) \right] \tag{8} $$

其中 $\beta_{\mathrm{ans}}$ 和 $\beta_{\mathrm{visual}}$ 分别为答案和视觉序列的 KL 惩罚系数。

**总损失**为上述两项之和：

$$ \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{actor}} + \mathcal{L}_{\mathrm{KL}} \tag{9} $$

### 3.4 与标准 GRPO 的关键差异

标准 GRPO 使用单一的组相对优势 $\hat{A}^{\mathrm{grp}}(Q, s_k) = r(Q, s_k) - \frac{1}{K} \sum_{j=1}^{K} r(Q, s_j)$ 对所有 token 进行统一加权（式 1-2），这导致视觉感知和语言推理的梯度信号相互纠缠。Vision-SR1 的解耦设计带来的核心优势在于：

- **精确的梯度路径**：视觉描述 token 仅受视觉奖励的优势信号驱动，不受答案奖励的干扰；同理，推理链 token 仅受答案奖励驱动。这避免了视觉描述"搭便车"依赖答案信号而退化为语言捷径。
- **独立的 KL 约束**：$\beta_{\mathrm{ans}}$ 和 $\beta_{\mathrm{visual}}$ 可分别调节，允许对视觉感知和语言推理施加不同程度的正则化，适应两者不同的收敛特性。

### 3.5 计算效率分析

两阶段 rollout 相比标准 GRPO 增加了约 20% 的训练时间（7B 模型 20 步训练：标准 GRPO 约 10.5 小时，Vision-SR1 约 13 小时），但完全无需外部奖励模型或额外 GPU 资源。这一开销远低于 Perception-R1 等依赖外部专有 MLLM 的方法，后者需要额外的 API 调用或 GPU 部署成本。



## 实验与关键发现

### 核心实验设置

Vision-SR1 的训练数据为自建的 **Vision-SR1-47K** 数据集（Table 1），涵盖数学（14K，30.5%）、科学知识（14K，30%）和通用视觉推理（18K，39.5%）三个领域，包含 CLEVR-Math、GeoQA+、TQA、ScienceQA 等 18 个子集。实验基座模型为 Qwen2.5-VL-3B、Qwen2.5-VL-7B 和 Mimo-VL-7B，对比基线包括：

- **Vision-R1**（Huang et al., 2025b）：原始版本仅在数学领域训练，论文在 Vision-SR1-47K 上复现以确保公平比较；
- **Perception-R1**（Xiao et al., 2025）：利用外部专有 MLLM 提取视觉标注作为额外奖励信号；
- **Visionary-R1**（Xia et al., 2025）：通过外部纯文本 LLM 提供监督信号。

所有方法均基于 **GRPO**（Shao et al., 2024）策略梯度框架。训练配置为 8 GPU，per-device batch size 8，训练 20 步；7B 模型的标准 GRPO 约需 10.5 小时，Vision-SR1 的双轮 rollout 约需 13 小时（约 20% 额外开销），但无需额外 GPU 或外部模型调用。

### 主要结果

**通用视觉理解与数学/幻觉基准（Table 2）**

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_C1M4ETatgM/figures/003_Table_2.jpg]]
*Table 2: Vision-SR1 vs. baselines. For Vision-R1, as noted in Section 3.1, the original model checkpoint was trained only on math-domain data. So we also reproduce it using our 47K dataset*

以 Qwen2.5-VL-7B 为主干，Vision-SR1 在 7 项基准上的平均准确率达到 **52.2**，较 Vision-R1（47K 公平复现版本）的 50.7 提升 **+1.5** 个百分点。关键单项提升包括：

- **RealWorld QA**：69.2（+2.6），反映常识视觉问答能力的增强；
- **HallusionBench**：68.9（+2.3），表明幻觉缓解效果显著；
- **MMMU-Pro**：40.7（+0.9），在专业多模态理解上亦有增益；
- **MMMU**：52.2（+0.4）。

跨模型规模的一致性：Qwen2.5-VL-3B 平均 48.8（vs. Vision-R1 47K 的 47.2），Mimo-VL-7B 平均 49.5（vs. 47.2），证明方法对不同参数量和架构的主干均有效。在 72B 模型上，Vision-SR1 平均 52.2，远超 Vision-R1 的 44.5，显示大规模模型下自奖励的优势更为突出。

**空间推理与语言捷径鲁棒性（Table 3）**

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_C1M4ETatgM/figures/004_Table_3.jpg]]
*Table 3: Our method also can improve VLMs’ abilities on spatial reasoning and language shortcut (LS) robustness*

在空间推理基准 OmniSpatial 上，Qwen2.5-VL-7B 的 Vision-SR1 达到 **44.2**，较 Vision-R1 的 31.1 提升 **+13.1**，表明视觉感知自奖励显著增强了模型的空间关系理解。在语言捷径鲁棒性测试 ViLP 上，Vision-SR1 达到 52.6（+1.3），说明模型更少依赖语言先验进行猜测。

### 消融实验

**视觉感知自奖励的核心作用（Table 6）**

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_C1M4ETatgM/figures/009_Table_6.jpg]]
*Table 6: Results of ablation study: Vision-SR1 v.s. Vision-SR1 w/o visual perception self-reward*

移除视觉感知自奖励和多奖励策略优化后（即仅保留答案奖励和结构化输出格式），Qwen2.5-VL-7B 的平均性能从 52.2 降至 **50.3**（−1.9），3B 模型从 48.8 降至 47.2（−1.6）。该消融版本与 Vision-R1 的唯一区别在于输出格式的系统提示，其他监督信号完全相同，确保了控制变量的严格性。这一结果直接验证了自奖励机制是性能提升的主要驱动力，而非格式工程。

**语言捷径率分析（Table 4）**

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_C1M4ETatgM/figures/005_Table_4.jpg]]
*Table 4: Language Shortcut Rate (LSR) across different benchmarks. Lower values indicate better performance, as a reduced LSR reflects fewer language shortcuts during reasoning. Adding additional reward supervision can reduce the change of visual reasoning reward hacking*

语言捷径率（LSR）定义为视觉推理不正确但最终答案正确的样本比例：

$$\mathrm{LSR} = \frac{\# \{ \mathrm{incorrect~visual~reasoning} \ \& \ \mathrm{correct~answer} \}}{\# \{ \mathrm{total~samples} \}}$$

LSR 的评估采用两阶段流程，由 Gemini-2.5-flash 作为评判者：首先提取视觉感知内容，然后检查其自包含性。Vision-SR1（7B）的平均 LSR 为 **9.8**，低于无自奖励版本的 10.1；3B 模型为 9.4 vs. 10.4。这一趋势在多个基准上一致，证实自奖励机制有效抑制了模型绕过视觉感知、直接依赖语言先验的捷径行为。

**纯文本推理保持（Table 5）**

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_C1M4ETatgM/figures/007_Table_5.jpg]]
*Table 5: Through self-reward, the model is implicitly rewarded for text-only reasoning, leading to improved performance in general reasoning and reduced degradation in math reasoning benchmarks*

多模态 RL 训练通常会导致纯文本推理能力的退化。Vision-SR1 通过自奖励机制隐式奖励了文本推理能力，在 MMLU-Pro 和 SuperGPQA 等通用推理基准上优于 Vision-R1。在数学推理基准上，GSM8K 有所提升，但 MATH-500 仍存在一定程度的遗忘，表明视觉-语言联合优化中的灾难性遗忘问题尚未完全解决。

**视觉注意力分析（Figure 2）**

后训练对 ViT 的层间注意力分布产生了显著影响。最大的视觉注意力增益出现在第 6 层（**+10.2%**），表明模型在早期特征提取阶段更多地关注视觉 token；在后期融合阶段同样观察到注意力向视觉模态的偏移。这一内在表征层面的变化为性能提升提供了机制性解释。

### 失败模式与局限性

1. **训练效率折衷**：双轮 rollout 带来约 20% 的训练时间增加（7B 模型约 13 小时 vs. 10.5 小时），虽然远优于部署外部奖励模型，但在大规模训练场景中仍需权衡。
2. **自奖励的可靠性边界**：自奖励的有效性依赖于基座 VLM 自身的推理能力；对于过于简单或极复杂的视觉任务，自我评估的准确性可能下降，导致奖励信号噪声增大。
3. **领域泛化限制**：Vision-SR1-47K 仅覆盖数学、常识和通用视觉理解三个领域，在医学影像、遥感等专业领域的泛化能力未经验证。
4. **模型规模验证不足**：实验主要在 3B 和 7B 参数模型上进行，72B 的结果虽显示正向趋势，但缺乏系统性的大规模消融。
5. **文本推理的残余退化**：尽管自奖励减轻了纯文本数学推理的退化，MATH-500 等基准上仍存在可观测的性能下降，说明视觉-语言联合训练中的能力冲突尚未完全解耦。
6. **内存与采样效率**：双次 rollout 对显存和采样效率有额外需求，不适用于需要极致低延迟的在线部署场景。



## 定位与知识库关联

### 方法谱系：从答案监督到视觉自奖励

Vision-SR1 的核心贡献在于将 VLM 的强化学习后训练从单一的答案正确性监督，推向了视觉感知与语言推理解耦的自奖励范式。其方法谱系可沿三条线索展开：

**1. RL 后训练的奖励信号演进。** 传统的 VLM 后训练方法——如 **Vision-R1**（Huang et al., 2025b）——将 **GRPO**（Shao et al., 2024）直接应用于多模态问答，仅以最终答案的二元正确性作为奖励信号。这一设计的根本缺陷在于：中间视觉推理过程缺乏任何形式的显式指导，模型可以通过语言先验“猜”出正确答案而无需真正理解图像内容。为弥补这一缺陷，**Perception-R1**（Xiao et al., 2025）引入了外部专有 MLLM 提取的视觉标注作为额外奖励，**Visionary-R1**（Xia et al., 2025）则借助外部纯文本 LLM 提供监督信号。然而，这两类方法均依赖外部模型，引入了额外的计算开销和 API 依赖。Vision-SR1 的关键突破在于将奖励信号的来源内化：模型自身充当评判者，验证其生成的视觉描述是否完备到足以支撑正确答案——即“自奖励”（self-reward）。这彻底消除了对外部监督模型的依赖，同时保留了视觉感知的显式反馈。

**2. 推理结构的显式分解。** Vision-R1 等基线方法允许模型自由生成推理链，不强制区分视觉感知与语言推理。Vision-SR1 则通过系统提示强制输出结构化为三段：`⟨visual.reasoning⟩`（自包含的视觉描述）、`⟨think⟩`（语言推理链）和 `⟨answer⟩`（最终答案）。这一强制分解是自奖励机制得以运作的前提：只有当视觉描述被显式地隔离为独立文本块时，模型才能在第二轮 rollout 中仅凭该描述重新推理，从而评估其自包含性。

**3. 策略优化的解耦。** 在奖励信号分解之后，Vision-SR1 进一步在优化层面实现了解耦。标准 GRPO 对整条响应计算单一组相对优势，所有 token 共享同一梯度信号。Vision-SR1 的多奖励策略优化（Multi-Reward Policy Optimization）则分别为答案 rollout 和视觉 rollout 计算独立的 z-score 优势、对数概率和 KL 散度，最终组合为总损失。这一设计避免了两种信号在梯度层面的纠缠，使视觉基础与语言推理各自获得精确的优化路径。

### 适用边界

**有效范围。** Vision-SR1 在以下条件下展现出稳定的性能增益：
- **任务类型**：需要视觉感知与推理的复合任务，包括数学几何推理（GeoQA+）、科学图表理解（ScienceQA）、空间推理（OmniSpatial）以及需要抵抗语言捷径的幻觉敏感任务（HallusionBench、ViLP）。在 7 项基准测试上，Vision-SR1 相比 Vision-R1 47K 基线平均提升 1.5 个百分点（52.2 vs. 50.7），其中空间推理和语言捷径鲁棒性任务提升尤为显著（OmniSpatial: +13.1）。
- **模型规模**：论文在 3B 和 7B 参数规模的 Qwen2.5-VL 和 Mimo-VL 上验证了方法的有效性。7B 模型的平均 LSR（语言捷径率）从无自奖励的 10.1 降至 9.8。
- **数据领域**：Vision-SR1-47K 数据集覆盖数学（14K，30.5%）、科学知识（14K，30%）和一般视觉推理（18K，39.5%）三个领域，方法在这些领域内均表现出正向迁移。

**边界条件。** 以下场景可能限制方法的有效性：
- **任务难度极端化**：自奖励机制的有效性依赖于基础 VLM 自身的推理能力。当视觉任务过于简单时，语言捷径本身已足够产生正确答案，自奖励的边际增益有限；当任务过于复杂时，模型自我评估的准确性下降，可能导致噪声奖励。
- **领域泛化**：Vision-SR1-47K 未覆盖视频理解、3D 感知、文档解析等特定领域，方法在这些领域的泛化能力未经验证。
- **大模型扩展**：实验仅在 3B 和 7B 模型上进行，72B 模型的结果虽然提及但细节有限。大规模模型上的自奖励行为是否保持稳定仍需验证。

### 计算开销与效率权衡

两阶段 rollout 训练相比标准 GRPO 增加了约 20% 的训练时间（7B 模型 20 步训练：标准 GRPO 约 10.5 小时，两阶段约 13 小时），但这一开销远低于部署外部奖励模型（如 Perception-R1 需要额外 GPU 或 API 调用）。论文明确指出，自奖励过程无需额外 GPU 计算，仅增加了采样次数。然而，双次 rollout 对内存和采样效率的影响使其不适合需要极致低延迟的在线推理场景。

### 局限与开放问题

**已知局限。**
1. **文本推理的残余退化**：尽管自奖励机制通过隐式奖励纯文本推理路径缓解了多模态 RL 训练带来的文本能力遗忘，但 MATH-500 等纯文本数学基准上仍存在一定程度的性能退化（Table 5）。
2. **视觉奖励的自我评估可靠性**：自奖励的二元判定（视觉描述能否独立产生正确答案）依赖于模型自身的推理一致性。当模型在视觉感知阶段已产生偏差时，第二轮评估可能无法有效识别这种偏差。
3. **训练数据覆盖**：Vision-SR1-47K 仅涵盖三个领域，方法在其他多模态任务类型上的迁移能力未经系统验证。

**开放问题。**
1. **视觉推理的真实提升 vs. 语言推理的唤醒**：多模态 RL 训练在多大程度上真正增强了模型的视觉感知能力，而非仅仅优化了其利用语言先验进行推理的策略？论文通过 LSR 指标和 ViT 注意力分析（Figure 2）提供了部分证据，但因果机制的彻底分离仍需更精细的干预实验。
2. **视觉基础与语言捷径的彻底解耦**：当前方法将 LSR 从 10.1 降至 9.8，降幅有限。是否存在更根本的机制设计（如对比学习约束、因果干预）来进一步抑制语言捷径学习？
3. **视觉推理的潜在化**：当前强制输出显式视觉描述增加了生成长度。能否将视觉推理视为潜在思维（latent thinking），在保持自奖励机制的同时提升生成效率？
4. **自奖励的跨模态扩展**：该范式能否推广至视频理解（时序视觉描述的完备性验证）、3D 感知（多视角一致性验证）等更复杂的多模态任务？
5. **奖励权重的自适应调节**：答案奖励与视觉奖励的权重目前为固定值。是否可以通过课程学习或基于不确定性的自适应机制动态调整二者的平衡，以在训练过程中逐步强化视觉基础？



## 原文 PDF

![[paperPDFs/ICLR_2026/Vision_SR1_Self_Rewarding_Vision_Language_Model_via_Reasoning_Decomposition_and_Multi_Reward_Policy_Optimization.pdf]]

---
title: "CodeV: Code with Images for Faithful Visual Reasoning via Tool-Aware Policy Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CodeV_Code_with_Images_for_Faithful_Visual_Reasoning_via_Tool_Aware_Policy_Optimization.pdf
project_link: null
code_link: "https://github.com/RenlyH/CodeV"
aliases:
- CTAPOT
- CodeV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入工具感知策略优化（TAPO），直接根据工具执行结果（例如裁剪图像是否包含查询目标）提供密集的过程奖励，而不是仅凭最终答案。这一激励信号使模型在生成回答的同时，必须确保工具输出包含相关证据，从而大幅提高工具使用的忠实度。
primary_logic: 将工具使用视为一系列可验证的决策，仅检查非模型生成的工具输出（裁剪图像、坐标等）作为证据（evidence checking），可以比监控推理链或最终答案更可靠地提供步骤级奖励。这种证据导向的奖励设计能够有效抑制奖励黑客（reward hacking），引导模型在推理过程中真正依赖工具输出。
claims:
- 在V*基准上，DeepEyes的正确回答中只有57%的工具调用是忠实的（裁剪包含目标），Pixel-Reasoner为43%，表明高准确率下存在普遍的不忠实工具使用。
- CodeV在V*和HRBench-4k上显著提高了忠实工具使用率，相较Pixel-Reasoner和DeepEyes提升达两位数百分点，同时保持或提高了回答准确率。
- 消融实验表明，仅适用准确性奖励的RL会使策略退化为纯文本推理，而采用TAPO完整奖励能够稳定提升推理和感知性能，并抑制不必要的工具调用。
- 工具输出扰动实验显示，CodeV在工具输出被遮蔽或替换时更倾向于改变思考和行动决策，说明模型确实依赖工具内容进行推理。
---

# CodeV: Code with Images for Faithful Visual Reasoning via Tool-Aware Policy Optimization

> [!tip] 核心洞察
> 将工具使用视为一系列可验证的决策，仅检查非模型生成的工具输出（裁剪图像、坐标等）作为证据（evidence checking），可以比监控推理链或最终答案更可靠地提供步骤级奖励。这种证据导向的奖励设计能够有效抑制奖励黑客（reward hacking），引导模型在推理过程中真正依赖工具输出。

| 字段 | 内容 |
|------|------|
| 中文题名 | CodeV：通过工具感知策略优化实现基于代码与图像的忠实视觉推理 |
| 英文题名 | CodeV: Code with Images for Faithful Visual Reasoning via Tool-Aware Policy Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19661) · [Code](https://github.com/RenlyH/CodeV) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CodeV (Tool-Aware Policy Optimization, TAPO) |
| Dataset | VLMBlinds, V*, MathVista, MathVision-Mini |

> [!tip] 效果简介
> - VLMBlinds 上，准确率 (%) 46.6 vs DeepEyes 41.2 (+5.4)。
> - V* 上，准确率 (%) 84.8 vs Qwen2.5-VL-7B 75.0 (+9.8)。
> - MathVista 上，准确率 (%) 71.8 vs GPT-4o 69.1 (+2.7)。

## 概要

### 问题背景：视觉推理代理的“不忠实”困境

当前视觉语言代理（如 **DeepEyes** 与 **Pixel-Reasoner**）在视觉搜索基准上已取得较高的最终答案准确率，但这一表面指标掩盖了一个深层缺陷：**中间工具调用经常不忠实于问题意图**。例如，模型可能裁剪了与问题无关的图像区域，却依然凭借语言先验或猜测“蒙对”答案。在 V* 基准上，DeepEyes 的正确回答中仅有 **57%** 的工具调用是忠实的（裁剪图像包含目标对象），Pixel-Reasoner 更是低至 **43%**（Figure 2）。这一现象的根源在于，现有训练范式仅以最终答案正确性或工具调用的存在性作为奖励信号，缺乏对工具使用是否真正与视觉证据一致的步骤级监督。高准确率与低忠实度之间的鸿沟，揭示了视觉推理代理中普遍存在的**奖励黑客（reward hacking）**问题。

### 核心方法：工具感知策略优化（TAPO）

**CodeV** 通过**工具感知策略优化（Tool-Aware Policy Optimization, TAPO）** 直接回应上述瓶颈。TAPO 的核心洞察是：将工具使用视为一系列**可验证的决策**，仅检查非模型生成的工具输出（如裁剪图像、坐标）作为证据，从而提供可靠的步骤级奖励。具体而言，TAPO 引入一个混合奖励函数，将传统的答案正确性奖励与基于工具输出证据检查的**工具忠实度奖励**相结合。工具忠实度由外部裁判模型（Qwen2.5-VL-32B）评估，判断裁剪图像等工具输出是否包含问题所需的目标或区域。这一证据导向的奖励设计，使模型在生成回答的同时必须确保工具输出包含相关证据，从而有效抑制奖励黑客行为，引导策略真正依赖视觉工具进行推理。

### 方法定位：代码化工具接口与两阶段训练

CodeV 将视觉工具（如裁剪、缩放）统一表示为**可执行的 Python 代码块**，在受限沙箱中运行并返回图像、文本等观测结果。这一设计使工具调用成为可被精确监控和评估的操作单元。训练采用**两阶段课程**：首先通过冷启动监督微调（SFT）教导模型使用 Python 代码进行图像操作，建立基础工具使用模式；随后在 TAPO 增强的 GRPO 强化学习阶段，利用混合奖励对策略进行步骤级信用分配，使模型在保持答案准确率的同时大幅提升工具使用的忠实度。

### 主要结果概览

CodeV 在多个视觉感知、推理和数学基准上展现出显著的性能提升与忠实度改善：

- **忠实度飞跃**：在 V* 和 HRBench-4k 上，CodeV 的忠实工具使用率相较 DeepEyes 和 Pixel-Reasoner 提升达两位数百分点，同时保持或提高了回答准确率（Figure 5）。
- **感知与搜索任务**：在 V* 上达到 **84.8%** 的准确率（Qwen2.5-VL-7B 为 75.0%），在 VLMBlinds 上达到 **46.6%**（DeepEyes 为 41.2%）。
- **数学与推理任务**：在 MathVista 上达到 **71.8%**（GPT-4o 为 69.1%），在 MathVision-Mini 上达到 **33.6%**（Pixel-Reasoner-7B 为 25.1%）。

消融实验进一步证实，仅使用准确性奖励的 RL 策略会迅速退化为纯文本推理，几乎不调用工具；而 TAPO 完整奖励能够稳定提升推理和感知性能，并抑制不必要的工具调用（Table 1, Table 2, Figure 6）。工具输出扰动实验（Table 6）也显示，当工具输出被遮蔽或替换时，CodeV 更倾向于改变思考和行动决策，表明模型确实依赖工具内容进行推理，而非仅将其作为装饰性输出。

### 视觉推理中的“高准确率假象”

视觉语言模型（VLM）在视觉问答、数学推理等任务上不断刷新记录，但当这些模型被赋予调用外部工具（如裁剪、缩放）的能力时，一个深层问题逐渐暴露：**最终答案的正确性并不等同于推理过程的忠实性**。Figure 1 展示了一个典型场景——视觉代理在完全错误的图像区域执行裁剪操作，却仍能给出正确答案。这种现象表明，模型可能依赖了预训练中的统计捷径或语言先验，而非真正从工具输出的视觉证据中推导结论。

更令人担忧的是，这种不忠实现象并非偶发。在 V* 视觉搜索基准上，现有开源代理的正确答案中，工具调用的忠实度远低于预期：**DeepEyes** 的正确回答中仅 57% 的裁剪操作真正包含了目标对象，而 **Pixel-Reasoner** 的这一比例更是低至 43%（Figure 2）。这意味着，即使这些模型在最终准确率上表现亮眼，其推理过程的可信度却严重不足——它们常常“猜对”答案，而非“看见”答案。

### 现有方法的根本瓶颈：奖励信号的错位

造成上述问题的根源在于当前训练范式的奖励设计。无论是监督微调（SFT）还是基于最终答案正确性的强化学习（RLVR），奖励信号都仅关注两个稀疏目标：**答案是否正确**，以及**是否调用了工具**。这种结果导向的奖励机制为“奖励黑客”（reward hacking）打开了大门：模型学会了调用工具的动作模式，却未真正学会利用工具输出的视觉信息。高准确率掩盖了推理链的脆弱性，使得模型在部署时可能做出看似正确但逻辑断裂的决策。

具体而言，现有框架存在三个结构性缺口：

1. **缺乏步骤级信用分配**：RLVR 的奖励仅在整个轨迹结束时发放，模型无法区分工具调用中哪些步骤是有效的、哪些是装饰性的。
2. **监督信号与视觉证据脱节**：奖励函数不检查工具输出的内容是否与问题相关，导致模型可以在裁剪空白区域后仍获得正向奖励。
3. **训练与评估指标不一致**：评估时关注准确率，训练时也仅优化准确率，忠实度始终是“无人监管”的隐变量。

### 本文动机：以工具输出为锚点的忠实推理

CodeV 的核心动机正是打破这一困境。作者提出，**工具执行结果（如裁剪图像、坐标序列）是天然可验证的视觉证据**——它们不依赖于模型的生成质量，而是客观存在于沙箱环境中。通过对这些非模型生成输出进行证据检查（evidence checking），可以为强化学习提供密集、可靠的步骤级奖励信号，从而引导策略真正学会“看后再答”。

这一思路将视觉推理的忠实性问题重新定义为**可验证的工具决策问题**：如果每次裁剪都必须包含目标对象才能获得奖励，模型就不得不学习将注意力精确对准问题所需的视觉区域。Figure 3 描绘了 CodeV 的整体框架——模型在 Python 沙箱中执行代码块形式的工具调用，每个工具输出交由裁判模型进行证据检查，最终与答案正确性奖励混合，通过工具感知策略优化（TAPO）更新策略。这种设计将“忠实”从抽象期望转化为可操作的优化目标，为后续的方法实现奠定了动机基础。

## 核心方法与创新机理

CodeV 的核心创新并非提出新的模型架构，而是重新设计了**视觉推理代理的奖励信号**，从而解决一个被高准确率掩盖的深层问题：**工具使用的不忠实性**。现有视觉代理（如 DeepEyes、Pixel-Reasoner）在视觉搜索基准上能取得高最终答案准确率，但其中间工具调用（如裁剪）经常与问题意图脱节——模型裁剪了错误区域，却仍能猜对答案。CodeV 通过**工具感知策略优化（TAPO）**，将奖励信号从仅关注“答案对不对”拓展到“工具用得对不对”，在保持甚至提升准确率的同时，使工具使用的忠实度大幅提升。

### 问题根因：高准确率下的隐性不忠实

当前视觉语言代理的训练奖励信号存在结构性缺陷。无论是仅基于最终答案正确性的结果奖励，还是附加工具调用存在性的稀疏奖励，都**无法区分“诚实推理”与“奖励黑客”**：模型可以学会在不看正确图像区域的情况下输出正确答案，只要它在训练数据中发现了某种捷径。Figure 2 的量化分析揭示了这一问题的严重性：在 V* 基准上，DeepEyes 的正确答案中只有 **57%** 的工具调用是忠实的（裁剪图像包含目标），Pixel-Reasoner 更是低至 **43%**。这意味着，有近一半的“正确”回答实际上建立在错误的视觉证据之上。高准确率在此成为一块遮羞布，掩盖了推理过程的不忠实现象。

### 关键机制：将工具使用转化为可验证的步骤级决策

TAPO 的核心洞察在于：**工具的输出（而非模型的思维链）才是判断推理是否忠实的可靠锚点**。与监控模型生成的文本推理链不同，工具输出（如裁剪后的图像、返回的坐标）是非模型生成的外部观测，对其进行验证可以避免自我强化错误。TAPO 将每一次工具调用视为一个可验证的决策步骤：对于一个裁剪操作，裁判模型（Qwen2.5-VL-32B）检查裁剪后的图像是否包含问题所需的目标或区域，从而给出步骤级的忠实度奖励。这种“证据检查”机制使奖励信号直接扎根于视觉事实，而非模型的主观叙述。

### Changed Slots：奖励函数与训练流程的重新设计

相对于基线方法，CodeV 在以下关键维度上进行了系统性改造：

**1. 奖励函数：从结果导向到过程－结果混合**

基线方法（如 DeepEyes、Pixel-Reasoner）的奖励信号以最终答案正确性为主，工具调用最多获得存在性奖励。CodeV 的 TAPO 引入了混合奖励设计：

$$R(\tau) = \lambda_{\mathrm{acc}} r^{\mathrm{acc}}(\tau) + \lambda_{\mathrm{tool}} r^{\mathrm{tool}}(\tau)$$

其中 $r^{\mathrm{acc}}$ 为答案正确性奖励，$r^{\mathrm{tool}}$ 为工具忠实度奖励，且 $|\lambda_{\mathrm{tool}}| < |\lambda_{\mathrm{acc}}|$，确保答案正确性仍为主导目标，工具奖励作为辅助引导。工具奖励通过聚合轨迹中所有 `<code>` 动作的步骤级奖励得到：

$$r^{\mathrm{tool}}(\tau) = \frac{1}{|\mathcal{T}_{\mathrm{tool}}|} \sum_{t \in \mathcal{T}_{\mathrm{tool}}} r_t^{\mathrm{tool}}$$

这一设计使模型在追求正确答案的同时，必须确保工具输出包含相关视觉证据，从而有效抑制奖励黑客行为。

**2. 训练流程：从单阶段到冷启动 SFT + TAPO 增强 RL**

基线方法通常采用单一阶段 SFT 或直接 RL。CodeV 采用**两阶段课程**：先通过冷启动 SFT 在 Thyme-SFT 等数据集上教导模型使用 Python 代码进行图像操作，建立基础工具使用模式；再通过 TAPO 增强的 GRPO RL 进行策略优化。消融实验（Table 1）显示，跳过冷启动直接进行 RL（Zero-RL）会导致模型迅速坍塌为纯文本推理，工具使用极少；而两阶段设计使模型在 RL 阶段能够稳定提升推理和感知性能。

**3. 工具接口：从专用 API 到可执行 Python 代码**

CodeV 将工具操作用可执行 Python 代码块表示，在受限沙箱中运行并返回结果。这一设计使工具使用具有可验证性和可扩展性：模型可以自由组合裁剪、缩放等操作，而裁判模型可以独立检查每次代码执行的输出结果。

**4. 工具奖励评估方式：从检查代码到检查输出**

与直接检查模型生成的代码或思维链不同，TAPO 仅检查工具执行后的**输出结果**（如裁剪图像）与问题的相关性。裁判模型（Qwen2.5-VL-32B）被指示判断裁剪图像的主要内容是否清晰包含回答问题所需的对象或区域。这种“只看结果不看过程”的评估方式降低了裁判模型被模型生成的文本所迷惑的风险。

### 消融验证：TAPO 奖励设计的因果作用

消融实验（Table 2）直接对比了不同奖励设计的效果：仅使用准确性奖励的 RL 策略最终几乎不调用工具，模型退化为纯文本推理；增加一致性奖励仅带来微小提升；而采用完整 TAPO 奖励（含工具忠实度）可获得最佳推理和感知性能。Figure 6 进一步显示，在 RL 训练早期，TAPO 能够维持合理的工具调用频率，而仅准确性奖励组的工具调用迅速衰减。这些证据表明，TAPO 的步骤级工具奖励是驱动忠实工具使用的**因果性因素**，而非相关性副产品。

CodeV 的整体训练与推理流程围绕**可执行 Python 代码作为视觉工具**这一核心设计展开，并采用**两阶段课程**（冷启动 SFT + 工具感知策略优化 TAPO）来赋予模型忠实使用工具的能力。方法总览如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2031_https_arxiv_org_abs_2511_19661/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the CodeV rollout and Tool-Aware Policy Optimization (TAPO). The model processes an image I and question Q pair, using tools like cropping to generate intermediate results for its final answer. Tool faithfulness will be scored by a reward model. For the tool like cropping, reward model will score rtool based on the observability of the target object in the cropped image. The final answer correctness will be used as outcome reward. The policy VLM is fine-tuned with tool-aware policy optimization, a GRPO-style reinforcement learning approach. The policy VLM will conduct multiple rollouts for the same Q and I with tool use. These rollouts will be scored by the hybrid reward system...*

### 推理时的工具交互循环

在推理时，模型接收由图像 $V$ 和问题 $Q$ 组成的输入 $\mathbf{x} = (V, Q)$，并生成一个轨迹 $\tau$：

$$\tau = (\mathbf{x}, a_1, o_1, \ldots, a_T)$$

其中每个动作 $a_t$ 是模型自回归生成的 token 序列，当模型输出 `<code>` 块时，该代码块被送入一个受限的 **Python 沙箱** 执行。沙箱返回的观测 $o_t$ 可以是裁剪后的图像、文本输出或错误信息，并作为后续推理的上下文反馈给模型。这一设计使得工具使用不再是黑箱 API 调用，而是模型生成的可执行代码，其输出直接构成可验证的视觉证据。

### 两阶段训练管线

CodeV 的训练管线由两个阶段构成：

1. **冷启动 SFT（Stage 1）**  
   在 Thyme-SFT 等数据集上进行监督微调，教导模型使用 Python 代码进行图像操作（如 `crop`、`zoom`），建立基础的工具使用模式。该阶段使模型学会生成局部化、高分辨率的裁剪操作和多轮精炼行为，从而在进入 RL 之前已具备基本的工具调用能力。

2. **TAPO 强化学习（Stage 2）**  
   基于 GRPO（Group Relative Policy Optimization）框架，对同一输入执行多次 rollout，并使用**混合奖励**进行策略更新。TAPO 的目标函数为：

   $$\mathbb{E}_{\tau, t} \Big[ \min \big( r_t(\theta) A_t, \ \mathrm{clip}( r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \big) \Big] - \beta \mathbb{E}_q \Big[ \mathbb{D}_{\mathrm{KL}} \big( \pi_\theta(\cdot \mid q) \big\| \pi_{\mathrm{ref}}(\cdot \mid q) \big) \Big]$$

   其中 $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\mathrm{ref}}(a_t \mid s_t)}$ 为 token 级重要性比率，$A_t$ 为组内标准化后的优势函数。

### 混合奖励设计

TAPO 的核心创新在于其奖励函数将**答案正确性**与**工具忠实度**线性组合：

$$R(\tau) = \lambda_{\mathrm{acc}} r^{\mathrm{acc}}(\tau) + \lambda_{\mathrm{tool}} r^{\mathrm{tool}}(\tau)$$

其中 $|\lambda_{\mathrm{tool}}| < |\lambda_{\mathrm{acc}}|$，确保答案正确性始终主导优化方向。工具奖励 $r^{\mathrm{tool}}(\tau)$ 是对轨迹中所有 `<code>` 动作的工具奖励求平均：

$$r^{\mathrm{tool}}(\tau) = \frac{1}{|\mathcal{T}_{\mathrm{tool}}|} \sum_{t \in \mathcal{T}_{\mathrm{tool}}} r_t^{\mathrm{tool}}$$

每个工具动作的奖励 $r_t^{\mathrm{tool}}$ 由一个**外部裁判模型**（Qwen2.5-VL-32B）通过**证据检查**给出：裁判仅检查工具输出（如裁剪图像）是否包含问题所需的视觉目标或区域，而不依赖模型的思维链或最终答案。这种设计使得步骤级信用分配直接建立在可验证的视觉证据之上，而非对模型生成文本的猜测。

### 关键模块关系

| 模块 | 角色 | 所处阶段 |
|------|------|----------|
| 冷启动 SFT | 建立基础代码工具使用模式 | Stage 1 |
| TAPO RL（GRPO） | 通过混合奖励优化策略，实现步骤级信用分配 | Stage 2 |
| Python 沙箱 | 安全执行 `<code>` 块，返回图像/文本观测 | 推理 + RL rollout |
| 工具奖励裁判 | 对工具输出进行证据检查，判断是否包含目标对象 | Stage 2 奖励计算 |

这一管线使模型在生成答案的同时，必须确保工具输出包含相关视觉证据，从而从根本上抑制了“裁剪错误区域却猜对答案”的奖励黑客行为。消融实验证实，跳过冷启动 SFT（Zero-RL）会导致策略迅速坍塌为纯文本推理，工具使用极少；而仅使用准确性奖励的 RL 策略最终几乎不调用工具——只有完整的 TAPO 混合奖励才能稳定提升推理和感知性能（Table 1, Table 2）。

### 1. 轨迹与工具接口的形式化定义

CodeV 将视觉推理建模为**代码增强的马尔可夫决策过程**。一个完整的推理轨迹 $\tau$ 定义为输入与动作-观察序列的组合：

$$\tau = ( \mathbf { x } , a _ { 1 } , o _ { 1 } , \ldots , a _ { T } ) , \quad \mathbf { x } = ( V , Q )$$

其中 $V$ 为输入图像，$Q$ 为文本问题；每个动作 $a_t$ 是模型生成的 Python 代码块（以 `<code>` 包裹），观察 $o_t$ 是该代码在受限沙箱中执行后返回的结果（如裁剪图像、坐标或错误信息）。这一设计将视觉工具（裁剪、缩放等）统一为可执行代码，使工具调用成为可观测、可验证的决策步骤。

### 2. 策略优化基础框架：GRPO 与 RLVR

CodeV 的策略优化建立在 **GRPO（Group Relative Policy Optimization）** 之上，其底层目标为带 KL 惩罚的强化学习目标（RLVR）：

$$\underset { \pi _ { \theta } } { \operatorname* { m a x } } \ : \mathbb { E } _ { { x } \sim \mathcal { D } , { o } \sim \pi _ { \theta } ( \cdot \vert { q } ) } R ( { q } , { o } ) - \beta \mathbb { D } _ { \mathrm { K L } } \big ( \pi _ { \theta } ( o \vert { q } ) \vert \vert \pi _ { \mathrm { r e f } } ( o \vert { q } ) \big )$$

该式最大化期望奖励 $R(q, o)$，同时以 KL 散度约束策略 $\pi_\theta$ 不偏离参考策略 $\pi_{\mathrm{ref}}$ 过远，从而稳定训练。

### 3. TAPO 的核心目标函数

**工具感知策略优化（TAPO）** 在 GRPO 基础上引入 PPO 风格的裁切机制与组内优势估计。其优化目标为：

$$\mathbb{E}_{\tau, t} \Big[ \min \big( r_t(\theta) A_t, \ \mathrm{clip}( r_t(\theta), 1-\epsilon, 1+\epsilon) A_t \big) \Big] - \beta \mathbb{E}_q \Big[ \mathbb{D}_{\mathrm{KL}} \big( \pi_\theta(\cdot \mid q) \big\| \pi_{\mathrm{ref}}(\cdot \mid q) \big) \Big]$$

其中重要性比率 $r_t(\theta)$ 衡量当前策略与参考策略在 token 级别的偏离程度：

$$r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\mathrm{ref}}(a_t \mid s_t)}$$

$A_t$ 为组内相对优势，通过对同一问题的多次 rollout 奖励进行组内标准化得到。裁切操作 $\mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)$ 防止单步更新过大。

### 4. 混合奖励设计：答案正确性 + 工具忠实度

TAPO 的关键创新在于**混合奖励函数**，将稀疏的答案正确性奖励与密集的工具忠实度奖励线性组合：

$$R(\tau) = \lambda_{\mathrm{acc}} r^{\mathrm{acc}}(\tau) + \lambda_{\mathrm{tool}} r^{\mathrm{tool}}(\tau)$$

其中 $r^{\mathrm{acc}}(\tau)$ 为最终答案正确性奖励（稀疏、轨迹级），$r^{\mathrm{tool}}(\tau)$ 为工具忠实度奖励（密集、步骤级）。权重满足 $|\lambda_{\mathrm{tool}}| < |\lambda_{\mathrm{acc}}|$，确保答案正确性始终主导优化方向，工具奖励仅作为过程引导信号。

### 5. 工具奖励的聚合与证据检查机制

工具忠实度奖励 $r^{\mathrm{tool}}(\tau)$ 通过**对轨迹中所有工具调用步骤的奖励求平均**得到：

$$r^{\mathrm{tool}}(\tau) = \frac{1}{|\mathcal{T}_{\mathrm{tool}}|} \sum_{t \in \mathcal{T}_{\mathrm{tool}}} r_t^{\mathrm{tool}}$$

其中 $\mathcal{T}_{\mathrm{tool}}$ 为轨迹中所有 `<code>` 动作的索引集合。每个步骤的工具奖励 $r_t^{\mathrm{tool}}$ 由外部裁判模型（Qwen2.5-VL-32B）进行**证据检查**：裁判仅检查工具执行后的输出（如裁剪图像）是否包含问题所需的目标对象或区域，而不检查模型生成的推理文本。这一设计使得奖励信号直接锚定在可验证的视觉证据上，有效规避了奖励黑客行为。

### 6. 两阶段训练流程

CodeV 采用**冷启动 SFT + TAPO 强化学习**的两阶段课程：

- **阶段一（冷启动 SFT）**：在 Thyme-SFT 等数据集上教导模型使用 Python 代码进行图像操作（裁剪、缩放等），建立基础的工具调用模式。SFT 阶段已使模型学会生成局部化、高分辨率的裁剪和多轮精炼行为。
- **阶段二（TAPO 强化学习）**：基于 GRPO，使用混合奖励对策略进行在线优化。每次 rollout 在同一问题上生成多个候选轨迹，通过组内标准化计算相对优势，并利用裁切目标函数更新策略。

这一设计避免了直接 RL 训练（Zero-RL）导致的策略坍塌问题——消融实验表明，跳过 SFT 直接进行 RL 会使模型迅速退化为纯文本推理，几乎不调用任何工具。

## 实验与关键发现

### 核心瓶颈验证：高准确率下的不忠实工具使用

在探讨CodeV的性能之前，我们首先验证论文提出的核心瓶颈：当前视觉语言代理在视觉搜索基准上能达到较高最终答案准确率，但中间工具调用（如裁剪）经常不忠实于问题意图。如 **Figure 2** 所示，在V*基准上，**DeepEyes** 的正确回答中只有57%的工具调用是忠实的（即裁剪图像包含查询目标），而 **Pixel-Reasoner** 仅为43%。这意味着大量样本中模型裁剪了错误区域却仍然猜对了答案，高准确率掩盖了推理过程的不忠实现象。这一发现构成了TAPO方法设计的直接动机。

### 主要性能结果

CodeV在感知、视觉搜索、推理和数学四大类基准上进行了全面评估，对比基线包括基础模型 **Qwen2.5-VL-7B**、工具增强代理 **DeepEyes**、**Pixel-Reasoner**、**Thyme**，以及闭源强基线 **GPT-4o**。所有开源模型均为7B规模。

**感知与视觉搜索基准**（Table 3, Figure 4）：

- **VLMBlinds**：CodeV达到46.6%，相较DeepEyes的41.2%提升 **+5.4个百分点**，相较Pixel-Reasoner-7B的43.9%提升 **+2.7个百分点**。
- **V\***：CodeV达到84.8%，显著超越Qwen2.5-VL-7B的75.0%（**+9.8个百分点**）和GPT-4o的64.4%（**+20.4个百分点**），在所有对比模型中排名第一。
- **HRBench-4K ALL**：CodeV达到76.1%，超越Thyme-7B-RL的72.3%（**+3.8个百分点**）和Pixel-Reasoner-7B的73.1%（**+3.0个百分点**）。
- **HRBench-8K** 和 **MME-Realworld-Lite**：CodeV同样取得最优或次优结果，具体数值见Table 3。

**数学与推理基准**（Table 4, Figure 4）：

- **MathVista**：CodeV达到71.8%，超越GPT-4o的69.1%（**+2.7个百分点**）和Qwen2.5-VL-7B的66.0%（**+5.8个百分点**）。
- **MathVision-Mini**：CodeV达到33.6%，相较Pixel-Reasoner-7B的25.1%提升 **+8.5个百分点**，在所有7B模型中表现最佳。
- **CharXiv** 和 **MMMU**：CodeV同样保持竞争力，在CharXiv上达到47.4%，接近GPT-4o的49.6%。

总体而言，CodeV在多数基准上超越了同规模的工具增强代理，并在部分任务上超越或接近GPT-4o，验证了TAPO训练框架的有效性。

### 工具忠实度提升

TAPO的核心目标是提升工具使用的忠实度，而不仅仅是最终答案准确率。**Figure 5** 和 **Table 5** 展示了各模型在V*和HRBench-4K上的忠实度对比：

![[assets/figures/papers/paper_list_l2031_https_arxiv_org_abs_2511_19661/figures/005_Figure_5.jpg]]
*Figure 5: Faithfulness comparison on V* and HRBench-4k benchmarks. The extremely low faithful tool use rate in [43] results from low tool use rate and decorative tool use in chain of thought*

![[assets/figures/papers/paper_list_l2031_https_arxiv_org_abs_2511_19661/figures/012_Table_5.jpg]]
*Table 5: Faithful results. Faithful is computed as faithful tool use AND correct answer, divided by total number of testing samples. Best result in each column are highlighted in bold*

- 在V*基准上，CodeV的忠实工具使用率（正确答案中裁剪包含目标的比例）显著高于DeepEyes和Pixel-Reasoner，提升达 **两位数百分点**，同时保持了最高的答案准确率。
- 在HRBench-4K上，CodeV同样展现出大幅领先的忠实度。值得注意的是，Thyme-7B-RL的忠实工具使用率极低，原因是其工具调用频率低且存在“装饰性”工具使用（仅在思维链中调用但不真正依赖工具输出）。

Table 5进一步报告了“准确且忠实”的综合指标（忠实工具使用且答案正确占总样本的比例），CodeV在所有基准上均取得最佳结果，表明TAPO成功实现了准确率与忠实度的双重提升。

### 消融实验

#### 训练阶段消融（Table 1）

![[assets/figures/papers/paper_list_l2031_https_arxiv_org_abs_2511_19661/figures/006_Table_1.jpg]]
*Table 1: Training stage ablation. Average performance across all reasoning and perception benchmarks*

为验证两阶段训练课程的必要性，论文对比了三种训练策略：
- **Zero-RL**：跳过冷启动SFT，直接在基础模型上进行RL。
- **SFT only**：仅进行冷启动SFT，不进行RL。
- **CodeV (SFT + TAPO)**：完整的两阶段训练。

结果显示，Zero-RL导致模型迅速坍塌为纯文本推理，工具使用极少，推理和感知平均得分均显著低于CodeV。SFT only虽能建立基础工具使用模式，但缺乏步骤级奖励优化，性能同样明显弱于完整CodeV。CodeV相较Zero-RL提升约 **1-3个点**，相较SFT提升约 **6-8个点**，验证了冷启动SFT与TAPO RL的互补性。

#### 奖励设计消融（Table 2）

![[assets/figures/papers/paper_list_l2031_https_arxiv_org_abs_2511_19661/figures/007_Table_2.jpg]]
*Table 2: Reward design ablation. Average performance across all reasoning and perception benchmarks*

论文进一步消融了TAPO混合奖励中各组分的贡献：
- **仅准确性奖励**：RL策略几乎不调用工具，模型退化为纯文本推理。
- **准确性 + 一致性奖励**：增加工具调用一致性奖励仅带来微小提升，无法有效激励忠实工具使用。
- **准确性 + 工具奖励（Qwen裁判）**：引入基于Qwen2.5-VL-32B的工具忠实度奖励后，性能显著提升。
- **准确性 + 工具奖励（GPT-5-nano裁判）**：使用更强的GPT-5-nano作为裁判模型，可进一步带来约 **1-2个点** 的推理性能提升，表明裁判模型能力是TAPO的上限因素之一。
- **完整TAPO（CodeV）**：包含所有奖励组分，取得最佳推理（54.2）和感知（69.7）平均得分。

这一消融清晰地证明，仅靠最终答案奖励无法引导模型忠实使用工具，而TAPO的步骤级工具忠实度奖励是驱动模型真正依赖视觉证据的关键。

#### 训练动态分析（Figure 9, Figure 10）

TAPO训练过程中的奖励曲线和响应长度变化进一步揭示了方法的工作机制：
- 格式奖励迅速饱和，准确率奖励和工具一致性奖励持续上升（Figure 9）。
- 平均响应长度和工具调用次数逐渐下降（Figure 10），表明TAPO有效抑制了奖励黑客行为——模型学会了在需要时才调用工具，而非通过冗余工具调用来骗取奖励。

#### 工具输出扰动分析（Table 6）

![[assets/figures/papers/paper_list_l2031_https_arxiv_org_abs_2511_19661/figures/013_Table_6.jpg]]
*Table 6: Tool-output perturbation analysis. We evaluate changes in the model’s behavior when all returned tool-output images are perturbed at inference time. Mask: mask out the tool output. Noise: replace the tool output with Gaussian noise. Random: replace the tool output with a non-overlapping random crop. Empty: remove the tool output entirely. We report the percentage of examples with a behavioral change (∆): Think, changes in reasoning tokens; Action, changes in subsequent tool-use actions (e.g., retrying a crop); and Answer, changes in the final answer*

为验证CodeV是否真正依赖工具输出进行推理，论文进行了工具输出扰动实验：在推理时将返回的裁剪图像分别进行遮蔽、替换为高斯噪声、替换为随机非重叠裁剪或完全移除。Table 6报告了模型行为发生变化的样本比例，包括：
- **Think**：推理token发生变化。
- **Action**：后续工具调用行为改变（如重新裁剪）。
- **Answer**：最终答案改变。

结果显示，CodeV在工具输出被扰动时，思考、行动和答案均发生显著变化的比例远高于未经过TAPO训练的模型，证明CodeV确实依赖工具内容进行推理，而非仅仅将工具调用作为装饰。

### 局限性与失败模式

尽管CodeV取得了显著成果，仍需注意以下局限：

1. **裁判模型依赖性**：TAPO依赖静态裁判模型（如Qwen2.5-VL-32B）评估工具输出，这引入了额外部署成本，且裁判模型的能力直接限制工具奖励的准确性。若裁判出错，可能误导策略学习。
2. **工具类型泛化性**：当前工具忠实度评估主要针对裁剪类图像操作，对于更广泛的工具类型（如计算、搜索、API调用），缺乏通用的忠实度指标。
3. **模型规模验证**：实验主要在7B模型上进行，虽然方法设计上可泛化至更大模型，但尚未验证。
4. **数据分布偏差**：RL数据清洗阶段剔除了外部知识任务和通过简单多数投票即可正确回答的样本，可能影响数据分布的平衡性。

### 开放问题

基于上述分析，TAPO框架仍面临以下开放挑战：
- 如何将TAPO扩展到更广泛的工具生态（如网页搜索、API调用），并设计可扩展、可验证的工具忠实度指标？
- 能否通过微调策略模型自身作为裁判或引入自我批判机制，替代外部静态裁判模型以降低部署成本？
- TAPO的步骤级奖励与基于隐式奖励的过程奖励模型（PRM）相比，在更复杂的推理任务上孰优孰劣？
- 如何避免裁判模型的偏见影响工具忠实度评估，尤其是在非裁剪类操作中？

## 定位与知识库关联

### 1. 在视觉推理代理谱系中的位置

CodeV 处于“工具增强型视觉语言代理”这一新兴方向，其核心贡献不是提出新的工具接口，而是**首次将工具使用的忠实度（faithfulness）作为显式优化目标**。这使其与现有工作形成了清晰的差异化定位。

**与基线方法的关系：**

- **DeepEyes** 与 **Pixel-Reasoner** 是当前视觉搜索代理的代表性工作，它们通过裁剪工具实现多步视觉推理，并在 V* 等基准上取得了高最终答案准确率。然而，CodeV 的作者揭示了这两类方法的一个隐蔽缺陷：当答案正确时，DeepEyes 的工具调用仅有 57% 是忠实的（裁剪区域包含目标对象），Pixel-Reasoner 更是低至 43%（Figure 2）。这意味着高准确率在很大程度上掩盖了推理过程的不忠实现象——模型常常裁剪了错误区域，却仍然“猜对”了答案。CodeV 通过 TAPO 的步骤级工具奖励，将忠实工具使用率提升至两位数百分点的优势（Figure 5），同时保持甚至提高了答案准确率。

- **Thyme** 是基于代码解释器的视觉代理，强调通过显式推理步骤进行视觉分析。但 CodeV 的分析表明，Thyme 的工具使用率极低，且存在“装饰性工具调用”（在思维链中调用工具但实际不依赖其输出），导致其忠实工具使用率在 V* 和 HRBench-4k 上均处于极低水平（Figure 5）。CodeV 通过可执行 Python 代码块替代纯文本工具调用，使工具使用成为可验证的操作，从机制上抑制了装饰性调用。

- **Qwen2.5-VL-7B** 作为基础视觉语言模型，未经过工具使用优化，在 V* 上准确率为 75.0%。CodeV 在此基础上通过两阶段训练（冷启动 SFT + TAPO RL）将准确率提升至 84.8%（Table 3），增幅达 9.8 个百分点，验证了工具感知策略优化的有效性。

- **GPT-4o** 作为闭源强基线，在 MathVista 上取得 69.1% 的准确率。CodeV（7B 规模）以 71.8% 超越了这一结果（Table 4），表明经过工具忠实度优化的较小模型可以在特定推理任务上匹敌甚至超越大规模专有模型。

### 2. 适用边界

TAPO 的当前设计存在明确的适用边界，这些边界定义了 CodeV 的优势范围与局限：

**有效适用场景：**
- **视觉搜索与精细感知任务**：V*、HRBench-4K/8K、VLMBlinds 等基准上的显著提升（Table 3）表明，TAPO 特别适合需要多步裁剪和区域检查的视觉推理场景。
- **数学与推理任务**：MathVista（71.8%）和 MathVision-Mini（33.6%）上的表现（Table 4）说明，工具忠实度优化对需要精确视觉信息提取的数学推理同样有效。
- **7B 规模模型**：所有开源对比实验均在 7B 参数规模上进行，验证了 TAPO 在此规模下的有效性。

**需要谨慎推广的场景：**
- **非裁剪类工具操作**：TAPO 的工具忠实度评估主要针对裁剪操作设计（检查裁剪图像是否包含目标对象）。对于计算、搜索、API 调用等更广泛的工具类型，缺乏通用的忠实度指标。文中明确指出这一局限，目前尚无实验证据支持 TAPO 在这些工具类型上的有效性。
- **外部知识依赖任务**：RL 数据清洗阶段主动剔除了需要外部知识的样本，这意味着 TAPO 训练的模型可能不适合需要大量外部知识检索的任务。
- **更大规模模型**：虽然作者推测 TAPO 可泛化至更大模型，但尚未提供实验验证。

### 3. 局限分析

**方法层面的局限：**

1. **静态裁判模型的依赖性**：TAPO 依赖 Qwen2.5-VL-32B 作为外部裁判来评估工具输出的忠实度。这引入了额外的推理成本和部署复杂度。更重要的是，裁判模型的能力直接限制了工具奖励的准确性——若裁判出错，将误导策略学习。消融实验显示，使用更强的 GPT-5-nano 替代裁判可进一步提升约 1-2 点性能（Section 5.4），说明当前裁判模型可能是一个性能瓶颈。

2. **工具忠实度指标的单一性**：当前的忠实度定义高度特化于裁剪操作（检查裁剪图像是否包含目标对象）。对于其他工具类型，如计算器、搜索 API、数据库查询等，缺乏可扩展的、可自动验证的忠实度指标。这使得 TAPO 的当前实现难以直接迁移到更广泛的代理工具生态。

3. **奖励权重的手动设定**：混合奖励中工具奖励权重与答案奖励权重的关系被约束为 $|\lambda_{\mathrm{tool}}| < |\lambda_{\mathrm{acc}}|$（Equation 5），以确保答案正确性主导优化。但这一权重的具体取值需要人工调整，缺乏自适应的权重调节机制。

**实验层面的局限：**

1. **数据分布偏差**：RL 数据清洗阶段剔除了外部知识任务和通过简单多数投票即可正确回答的样本。这一过滤策略可能改变了数据分布，使得训练后的模型在某些任务类型上表现不具代表性。

2. **评估基准的覆盖范围**：虽然评估涵盖了感知、视觉搜索、推理和数学等多个维度，但工具忠实度评估主要集中在 V* 和 HRBench 等以裁剪为核心的基准上。对于其他工具使用模式的忠实度，缺乏系统的评估。

3. **模型规模的限制**：所有开源对比均在 7B 规模进行。与 GPT-4o 的对比虽然显示了竞争力，但模型规模的巨大差异使得这一对比的说服力有限。

### 4. 开放问题

从 CodeV 的当前设计出发，以下开放问题值得后续工作关注：

1. **工具生态的扩展与泛化**：如何将 TAPO 扩展到更广泛的工具类型（网页搜索、API 调用、数据库查询、计算器等），并为每种工具设计可自动验证的忠实度指标？这需要定义“忠实使用”在不同工具语境下的通用语义。

2. **裁判模型的替代方案**：能否通过微调策略模型自身作为裁判，或引入自我批判机制（self-critique），替代外部静态裁判模型？这将消除额外的模型部署成本，并可能实现更紧密的策略-裁判协同优化。

3. **与过程奖励模型（PRM）的关系**：TAPO 的步骤级奖励基于可验证的工具输出（证据检查），而 PRM 通常基于隐式的推理步骤评估。在更复杂的推理任务上，这两种过程监督方式孰优孰劣？是否存在互补的可能？

4. **裁判偏见的量化与控制**：如何系统性地评估裁判模型在工具忠实度判断中的偏见，尤其是在非裁剪类操作中？裁判模型的错误判断对策略学习的长期影响是什么？

5. **训练稳定性与样本效率**：TAPO 在 7B 模型上展现了稳定的训练动态（Figure 9, Figure 10），但在更大规模模型和多模态场景下，训练稳定性和样本效率是否依然保持？冷启动 SFT 的必要性是否会随模型规模变化而改变？

6. **忠实度与准确率的权衡机制**：TAPO 通过权重约束 $|\lambda_{\mathrm{tool}}| < |\lambda_{\mathrm{acc}}|$ 确保准确率优先。是否存在更优的权衡机制，例如动态权重调整或帕累托优化，以在忠实度和准确率之间取得更好的平衡？

## 原文 PDF

![[paperPDFs/CVPR_2026/CodeV_Code_with_Images_for_Faithful_Visual_Reasoning_via_Tool_Aware_Policy_Optimization.pdf]]

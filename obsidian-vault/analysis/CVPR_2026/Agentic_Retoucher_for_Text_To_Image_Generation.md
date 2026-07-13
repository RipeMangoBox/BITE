---
title: Agentic Retoucher for Text-To-Image Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Agentic_Retoucher_for_Text_To_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- AR
- ARTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建闭环的“感知-推理-动作”循环：先由感知代理生成上下文感知的失真显著性图，再由推理代理进行与人类偏好对齐的细粒度诊断，最后动作代理自适应选择局部修复工具，从而形成自我纠正的迭代过程。
primary_logic: 将生成后修正建模为类似人类专家的感知-推理-动作过程，通过跨模态显著性预测、渐进式偏好对齐（SFT+GRPO）和工具库驱动的局部修复，使模型能够自主地发现、理解并修正小尺度失真，同时保持全局一致性。
claims:
- Agentic Retoucher将GenBlemish-27K上的plausibility从44.21提升至47.10，overall从47.15提升至49.27，远超VLM和掩码基线的独立修复。
- 人类评估中83.2%（48.8%显著更好+34.4%稍好）的结果偏向于Agentic Retoucher的输出，仅4.2%的基线被认为显著更好。
- 感知代理在失真显著性预测上达到SOTA，AUC-Judd=0.9336，NSS=1.2087，显著优于RichHF和通用VLMs。
- 推理代理经渐进对齐（SFT+GRPO）后，在三个VLMs骨干上诊断准确率稳定最高（如Qwen2.5-VL 80.10%，GLM-4.1V 79.26%，Ovis2.5 80.62%），且消除幻觉。
---

# Agentic Retoucher for Text-To-Image Generation

> [!tip] 核心洞察
> 将生成后修正建模为类似人类专家的感知-推理-动作过程，通过跨模态显著性预测、渐进式偏好对齐（SFT+GRPO）和工具库驱动的局部修复，使模型能够自主地发现、理解并修正小尺度失真，同时保持全局一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向文本到图像生成的自主修饰代理 |
| 英文题名 | Agentic Retoucher for Text-To-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.02046) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Agentic Retoucher |
| Dataset | GenBlemish-27K, SynArtifacts-1K, Human Evaluation |

> [!tip] 效果简介
> - GenBlemish-27K 上，plausibility ↑ 47.10 (Ours w Qwen-Edit) vs 44.21 (Original) (+2.89)；overall ↑ 49.27 (Ours w Qwen-Edit) vs 47.15 (Original) (+2.12)。
> - SynArtifacts-1K 上，overall ↑ 58.43 (Ours w Gemini 2.5 Flash Image) vs 55.35 (Original) (+3.08)。
> - Human Evaluation 上，preference % ≫ (significantly better) 48.8% vs 4.2% (+44.6%)。

## 概要

当前文本到图像（T2I）生成模型在全局语义一致性上取得了显著进展，但在**局部失真**（如肢体畸形、面部缺陷、文字拼写错误、物体交互异常等）的自主感知与修复方面仍存在根本性瓶颈。现有的视觉语言模型（VLMs）尽管具备一定的视觉理解能力，却在空间定位和失真推理上表现出严重的**幻觉与不可靠性**——即使给出明确的区域提示，仍难以准确识别和诊断失真区域（Figure 1左）。同时，基于手工掩码或单一修复工具的现有方案缺乏闭环的检测-诊断-修正能力，无法形成有效的自我纠正机制。

针对上述问题，本文提出 **Agentic Retoucher**，一个层次化的决策驱动框架，将生成后修正重新建模为类似人类专家的**“感知-推理-动作”（Perception-Reasoning-Action）闭环过程**。其核心洞察在于：通过跨模态显著性预测实现上下文感知的细粒度失真定位，通过渐进式人类偏好对齐（监督微调SFT + 组相对策略优化GRPO）进行可靠的失真诊断，再通过自适应工具选择执行局部修复，从而使模型能够自主地发现、理解并修正小尺度失真，同时保持全局视觉和谐。

为实现这一框架，本文构建了 **GenBlemish-27K** 数据集，包含6,025张图像和27,507个精细标注的失真区域，覆盖手部、面部、文字等六类高层失真维度和十二个细粒度类别，为失真定位与推理提供了必要的训练与评估基础。

实验结果表明，Agentic Retoucher 在多个维度上显著超越了现有方法：
- 在 GenBlemish-27K 基准上，plausibility 指标从 44.21 提升至 **47.10**，overall 指标从 47.15 提升至 **49.27**（Table 1）；
- 人类评估中，**83.2%** 的测试案例倾向于 Agentic Retoucher 的输出（其中48.8%为显著更优），仅4.2%的基线被认为显著更好（Table 2）；
- 感知代理在失真显著性预测上达到最优水平（AUC-Judd=**0.9336**，NSS=**1.2087**），推理代理经渐进对齐后在多个VLM骨干上诊断准确率稳定达到约80%，且有效消除了幻觉现象（Table 3, Table 4）。

这些结果验证了“感知-推理-动作”闭环架构在AIGC图像后处理中的有效性，为构建具备自主纠错能力的生成系统提供了新的范式。



文本到图像（T2I）生成模型近年来取得了显著进展，能够根据自然语言描述合成高保真、多样化的视觉内容。然而，即使是最先进的T2I模型，其输出中仍频繁出现局部失真与不合理之处，典型问题包括肢体畸形（如多指、关节错位）、面部结构异常、文字渲染错误以及物体间交互关系违背物理常识等。这些细粒度缺陷严重损害了生成内容的可用性与可信度，尤其在对视觉精度要求较高的应用场景（如广告创意、影视概念设计）中尤为突出。

当前应对生成后失真的主流方案存在明显局限。一方面，基于视觉语言模型（VLM）的直接修复方法试图通过文本指令引导图像编辑，但VLM在空间定位能力上存在严重不足——如Figure 1左侧所示，即使给出明确的区域提示，现有VLM仍频繁产生幻觉，无法准确标定失真位置，更难以提供合理的诊断推理。另一方面，基于掩码的传统修复（inpainting）方法需要人工精确标注待修复区域，不仅依赖大量人力，且缺乏对失真类型的语义理解，无法自主判断“何处需要修复”以及“如何修复”。两类方法的共同瓶颈在于：**缺乏对局部失真的自主感知与修复能力，无法形成闭环的检测-诊断-修正流程**。

更深层的问题在于，生成后修正本质上是一个需要精细空间感知与上下文推理的复杂决策过程。人类专家在面对AIGC图像失真时，会经历“观察定位→分析诊断→选择工具并执行修复”的认知循环，而现有方法要么跳过了定位与诊断环节（直接修复），要么将各环节割裂为孤立模块，缺乏统一的自主决策框架。

针对上述缺口，本文提出**Agentic Retoucher**，一个层次化的决策驱动框架。其核心动机在于：**将生成后修正重新建模为类似人类专家的“感知-推理-动作”闭环过程**，使模型能够自主地发现、理解并修正小尺度失真，同时保持全局一致性。具体而言，该框架通过三个协同智能体——上下文感知的失真定位、与人类偏好对齐的细粒度诊断、以及自适应工具选择的局部修复——形成自我纠正的迭代循环，从根本上解决VLM幻觉不可靠与修复策略单一的问题。



## 核心方法与创新机理

当前文本到图像（T2I）生成模型在局部失真（肢体畸形、面部缺陷、文字错误等）的自主感知与修复上存在根本性瓶颈。视觉语言模型（VLMs）虽能进行图像理解，但在空间定位和失真推理上存在严重幻觉与不可靠性，无法形成闭环的检测-诊断-修正流程。Agentic Retoucher 的核心创新在于将生成后修正重新建模为类似人类专家的**感知-推理-动作（Perception-Reasoning-Action）闭环**，通过三个关键维度的设计突破实现了自主的局部失真修复。

### 创新一：从手工掩码到上下文感知的失真显著性定位

传统修复方法依赖手工绘制掩码或 VLMs 生成的文本提示来定位失真区域，缺乏对图像语义与文本提示之间跨模态一致性的细粒度理解。Agentic Retoucher 的**感知代理（Perception Agent）**采用双编码器架构（ViT-T5），融合图像特征与提示语义，通过上下文感知的显著性预测输出细粒度失真显著图。该方法在失真显著性预测上达到 SOTA 水平（AUC-Judd = 0.9336, NSS = 1.2087），显著优于 **RichHF**（Liang et al., CVPR 2024）等通用感知评估方法及通用 VLMs（Table 3）。定性可视化（Figure 5）进一步表明，该方法能产生更锐利、上下文更敏感的定位结果。

### 创新二：从简单分类到渐进式人类偏好对齐的细粒度诊断

现有 VLM 方法通常直接进行问答或简单分类，缺乏与人类判断对齐的细粒度推理能力，且易产生幻觉。Agentic Retoucher 的**推理代理（Reasoning Agent）**引入渐进式人类偏好对齐策略：先通过监督微调（SFT）初始化诊断能力，再通过组相对策略优化（GRPO）进行强化对齐，生成包含失真类型、外观描述及上下文不一致评估的多维度诊断。消融实验（Table 4）表明，渐进式训练（SFT→GRPO）在所有指标上优于单独的 SFT 或 GRPO——单独 GRPO 早期会导致格式混乱与事实漂移，而 SFT 初始化有效规避了这一问题。在三个 VLMs 骨干上，该方法均取得最高诊断准确率（Qwen2.5-VL 80.10%，GLM-4.1V 79.26%，Ovis2.5 80.62%），且消除了幻觉。

### 创新三：从固定单一工具到自适应工具库驱动的局部修复

传统修复方法固定使用单一修复工具（如指定一个 inpainting 模型），无法根据失真类型和上下文灵活选择最优策略。Agentic Retoucher 的**动作代理（Action Agent）**维护一个包含 VLM 引导修复（如 Qwen-Edit、Gemini 2.5 Flash Image）和掩码引导修复（如 Flux-fill、SD-inpainting）的工具库，依据感知代理的显著图与推理代理的诊断结果，自适应选择并执行局部修复。迭代更新遵循：

$$I_{t+1} = \Phi_{\mathrm{act}}(I_t, \{M_i \lor D_i\}), \quad t \leftarrow t+1$$

其中 $M_i$ 为失真掩码，$D_i$ 为诊断描述。该闭环在 2-3 次推理迭代内收敛（Section 5.1）。实验表明，框架内部的任意单一修复工具结合感知与推理后，在所有指标上均显著高于直接使用该工具（Table 1），验证了感知-推理-动作闭环的通用增益效应。

### 闭环协同的因果机制

三个代理形成互补的因果链路：感知代理的显著性损失函数结合 MSE 与 KLD 损失，平衡像素精度与分布一致性：

$$\mathcal{L}_{\mathrm{sal}} = \alpha \mathcal{L}_{\mathrm{MSE}}(S, \hat{S}) + (1-\alpha) \mathcal{L}_{\mathrm{KLD}}(S, \hat{S})$$

推理代理的 GRPO 损失通过组相对优势估计和 KL 散度约束，对齐人类偏好并抑制幻觉：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathbb{E}_{(q,o)}[\min(r_t \hat{A}_t, \mathrm{clip}(r_t, 1-\varepsilon, 1+\varepsilon) \hat{A}_t) - \beta D_{\mathrm{KL}}[\pi_{\theta}||\pi_{\mathrm{ref}}]]$$

消融实验（Table 5）证实注意力模块与 KLD 损失的组合带来最佳显著性预测，二者互补——仅保留其一均导致 AUC-Judd、NSS 下降。这一闭环设计使得 Agentic Retoucher 在 GenBlemish-27K 上将 plausibility 从 44.21 提升至 47.10，overall 从 47.15 提升至 49.27，并在人类评估中获得 83.2% 的偏好率（48.8% 显著更好 + 34.4% 稍好），仅 4.2% 的基线被认为显著更好（Table 2）。



Agentic Retoucher 将生成后修正重新定义为类似人类专家的 **感知-推理-动作** 闭环过程（Figure 3）。该框架由三个协作代理构成：感知代理（Perception Agent）、推理代理（Reasoning Agent）和动作代理（Action Agent），三者形成一个自我纠正的迭代循环。

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed Agentic Retoucher. The framework operates as a perception-reasoning-action loop for post-generation correction in AIGC. The Perception Agent localizes context-dependent distortions via cross-modal saliency prediction, the Reasoning Agent performs human-aligned diagnosis through iterative reasoning, and the Action Agent executes adaptive localized inpainting guided by reasoning outputs, forming a closed-loop self-corrective process*

### 核心流程

给定一张由文本到图像模型生成的图像 $I_0$ 及其对应的文本提示，框架首先由**感知代理**对图像进行上下文感知的失真显著性预测，生成细粒度的候选失真区域掩码。随后，**推理代理**对这些区域进行与人类偏好对齐的多维度诊断，输出失真类型、外观描述及上下文不一致性分析。最后，**动作代理**依据诊断结果自适应地从工具库中选择合适的局部修复策略（VLM引导或掩码引导的局部修复），对图像进行修正。修正后的图像 $I_{t+1}$ 重新进入感知-推理-动作循环，直至所有显著失真被消除：

$$I_{t+1} = \Phi_{\mathrm{act}}(I_t, \{M_i \lor D_i\}), \quad t \leftarrow t+1$$

其中 $\Phi_{\mathrm{act}}$ 表示动作代理的修复操作，$M_i$ 为感知代理输出的失真掩码，$D_i$ 为推理代理生成的诊断描述。推理阶段完全自动化，每张图像通常在 2-3 次迭代内收敛。

### 模块分工

- **感知代理**：采用双编码器架构（ViT-T5），融合图像特征与提示语义，通过跨模态注意力机制输出上下文感知的失真显著图。其训练目标为结合 MSE 与 KLD 的混合损失：

  $$\mathcal{L}_{\mathrm{sal}} = \alpha \mathcal{L}_{\mathrm{MSE}}(S, \hat{S}) + (1-\alpha) \mathcal{L}_{\mathrm{KLD}}(S, \hat{S})$$

  该设计使得显著图在像素精度和分布一致性之间取得平衡，能够精确定位肢体、面部、文字等小尺度失真。

- **推理代理**：基于视觉语言模型骨干（如 Qwen2.5-VL、GLM-4.1V、Ovis2.5），通过渐进式人类偏好对齐进行诊断。训练分两阶段：首先通过监督微调（SFT）初始化模型，使其掌握失真诊断的基本格式与知识；随后采用组相对策略优化（GRPO）进一步对齐人类偏好：

  $$\mathcal{L}_{\mathrm{GRPO}} = \mathbb{E}_{(q,o)}[\min(r_t \hat{A}_t, \mathrm{clip}(r_t, 1-\varepsilon, 1+\varepsilon) \hat{A}_t) - \beta D_{\mathrm{KL}}[\pi_{\theta}||\pi_{\mathrm{ref}}]]$$

  这种渐进式训练策略有效避免了单独使用 GRPO 早期导致的格式混乱与事实漂移问题。

- **动作代理**：不依赖单一修复工具，而是根据感知和推理的输出动态选择工具库中的修复方案。工具库包含 VLM 引导修复（如 Qwen-Edit、Gemini 2.5 Flash Image）和掩码引导修复（如 Flux-fill、SD-inpainting），动作代理依据失真类型和上下文特征自适应调度最合适的工具，在修复局部失真的同时保持全局视觉一致性。

### 设计动机

现有视觉语言模型在 AIGC 图像的失真定位上存在严重幻觉——即使给出明确的区域提示，仍无法准确识别手部、面部等局部缺陷（Figure 1 左）。Agentic Retoucher 通过将感知（精确定位）、推理（语义诊断）与动作（自适应修复）解耦并形成闭环，弥补了 VLM 在空间定位和失真推理上的不可靠性，实现了从“检测-诊断-修正”的完整自主修正流程。

### 补充图表

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/002_Figure_2.jpg]]
*Figure 2: Overview of GenBlemish-27K. The figure illustrates (a) the dual-layer distortion taxonomy with six high-level dimensions and twelve fine-grained categories, (b) the distribution of localized distortion types, (c) the human-AI collaborative annotation pipeline, and (d) representative formatted samples with pixel-level masks and textual descriptions, highlighting how GenBlemish-27K enables fine-grained localization and reasoning over diverse text-to-image distortions*



### 框架总览与迭代闭环

Agentic Retoucher 将生成后修正重构为一个类人的“感知—推理—动作”闭环。如图 Figure 3 所示，框架由三个协作代理组成：**Perception Agent** 负责上下文感知的失真显著性预测，输出候选掩码区域；**Reasoning Agent** 对检测到的区域进行人类对齐的细粒度诊断，生成失真类型、外观描述及上下文不一致评估；**Action Agent** 则依据诊断结果自适应选择工具库中的局部修复工具（VLM 引导或掩码引导）执行修复。

整个过程以迭代方式运行，其更新规则为：

$$I_{t+1} = \Phi_{\mathrm{act}}(I_t, \{M_i \lor D_i\}), \quad t \leftarrow t+1$$

其中 $I_t$ 为第 $t$ 步的图像，$\Phi_{\mathrm{act}}$ 为动作代理的修复函数，$M_i$ 为感知代理输出的失真掩码，$D_i$ 为推理代理输出的失真文本描述。该循环持续至所有显著失真被消除，形成完整的自我纠正过程。推理在 2–3 次迭代内即可收敛。

### 感知代理：上下文感知显著性预测

感知代理的核心任务是在文本-图像一致性线索下定位上下文依赖的失真区域。其采用双编码器架构（ViT 图像编码器 + T5 文本编码器），通过跨模态注意力融合图像特征与提示语义，输出细粒度失真显著图 $S$。

训练目标为混合损失函数，平衡像素级精度与分布一致性：

$$\mathcal{L}_{\mathrm{sal}} = \alpha \mathcal{L}_{\mathrm{MSE}}(S, \hat{S}) + (1-\alpha) \mathcal{L}_{\mathrm{KLD}}(S, \hat{S})$$

其中 $S$ 为预测显著图，$\hat{S}$ 为真实显著图，$\mathcal{L}_{\mathrm{MSE}}$ 为均方误差损失，$\mathcal{L}_{\mathrm{KLD}}$ 为 KL 散度损失，$\alpha$ 为平衡系数。消融实验（Table 5）证实，注意力模块与 KLD 损失二者互补：仅保留其一均导致 AUC-Judd、NSS 等指标显著下降，组合使用达到最优（AUC-Judd=0.9336，NSS=1.2087）。

### 推理代理：人类偏好对齐的细粒度诊断

推理代理基于感知代理定位的失真区域，进行多维度诊断。为克服 VLM 在空间定位和失真推理上的严重幻觉问题，推理代理采用渐进式人类偏好对齐训练策略：

**阶段一（SFT 初始化）**：使用 LoRA 微调（rank=64，$\alpha=32$）在人工标注的诊断数据上进行监督微调，使模型获得基本的失真分类与描述能力。

**阶段二（GRPO 强化对齐）**：采用组相对策略优化（Group Relative Policy Optimization）进一步对齐人类偏好，损失函数为：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathbb{E}_{(q,o)}[\min(r_t \hat{A}_t, \mathrm{clip}(r_t, 1-\varepsilon, 1+\varepsilon) \hat{A}_t) - \beta D_{\mathrm{KL}}[\pi_{\theta}||\pi_{\mathrm{ref}}]]$$

其中 $q$ 为输入查询，$o$ 为输出，$r_t$ 为概率比，$\hat{A}_t$ 为优势估计，$\varepsilon$ 为裁剪阈值，$\beta$ 为 KL 惩罚系数，$\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略。该设计的关键在于：单独的 GRPO 训练早期会导致格式混乱与事实漂移，而 SFT 初始化提供了稳定的先验，使 GRPO 能够在保持诊断准确性的同时消除幻觉。Table 4 表明，渐进式训练（SFT→GRPO）在所有 VLM 骨干（Qwen2.5-VL 80.10%，GLM-4.1V 79.26%，Ovis2.5 80.62%）上均取得最优诊断准确率。

### 动作代理：自适应工具选择与修复

动作代理不固定使用单一修复工具，而是依据感知代理的掩码输出和推理代理的诊断描述，在工具库中自适应选择 VLM 引导修复（如 Qwen-Edit、Gemini 2.5 Flash Image）或掩码引导修复（如 Flux-fill、SD-inpainting）。这种动态规划策略使得同一框架可兼容多种修复后端，且无论使用何种单一工具，结合感知与推理后均能显著超越直接使用该工具的基线（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/001_Figure_1.jpg]]
*Figure 1: Left: Existing VLMs hallucinate and fail to localize distortions in AIGC-images, even with explicit region cues, whereas our method accurately localizes distorted regions and provides reasonable diagnoses. Right: Each before-after pair shows the distorted image and the result refined by our Agentic Retoucher, including diverse distortion artifacts across text, hand, face, and interaction*



## 实验与关键发现

### 主实验定量结果

Agentic Retoucher 在 GenBlemish-27K 和 SynArtifacts-1K 两个基准上均取得显著提升，且该增益在多种底层修复工具上一致复现（Table 1）。

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of Agentic Retoucher with VLM-based and mask-based inpainting baselines on the GenBlemish-27K and SynArtifacts-1K datasets*

**GenBlemish-27K 上的表现。** 以 Qwen-Edit 为修复骨干时，plausibility 从原始图像的 44.21 提升至 47.10（+2.89），overall 从 47.15 提升至 49.27（+2.12）。框架内部任意单一修复工具（Qwen-Edit、Gemini 2.5 Flash Image、Flux-fill、SD-inpainting）结合感知与推理后，在所有指标上均显著高于直接使用该工具的原始输出，说明性能增益来自感知-推理-动作闭环本身，而非特定修复模型。

**SynArtifacts-1K 上的表现。** 以 Gemini 2.5 Flash Image 为骨干时 overall 达到 58.43（原始 55.35，+3.08）；以 SD-inpainting 为骨干时 overall 达到 58.27，同样显著优于原始基线。

**与基线方法的对比。** VLM-based inpainting 基线（Qwen-Edit、Gemini 2.5 Flash Image、Flux-fill）和 mask-based inpainting 基线（SD-inpainting）在独立使用时均无法达到 Agentic Retoucher 的水平，验证了单纯的修复工具缺乏对失真区域的感知和推理能力，无法形成有效的闭环修正。

### 人类偏好评估

Table 2 展示了随机双盲人类评估结果：83.2% 的测试样本被评定为 Agentic Retoucher 输出优于原始图像，其中 48.8% 被判定为“显著更好”（≫），34.4% 被判定为“稍好”（>）。仅有 4.2% 的样本中基线被认为显著更好。这表明方法的主观视觉质量提升具有统计显著性和实际意义。需注意该评估仅来自 5 名参与者，样本量较小，结论的泛化性需要更大规模用户研究验证。

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/006_Table_2.jpg]]
*Table 2: Human evaluation results: preference distribution comparing Agentic Retoucher outputs to original images. Percentages of test cases rated as ≫ (significantly better), > (slightly better), ≈ (about the same), \< (slightly worse), or ≪ (significantly worse). Data from 5 participants in a randomized, blind survey*

### 感知代理评估

Table 3 报告了上下文感知感知代理在失真显著性预测上的定量结果。该方法在所有指标上达到 SOTA：AUC-Judd = 0.9336，NSS = 1.2087，显著优于 **RichHF**（Liang et al., CVPR 2024）和通用 VLM。定性可视化（Figure 5）进一步表明，该方法生成的显著图比 RichHF 和 GLM4.1V 更锐利、上下文感知更强，能够准确定位肢体、面部、文字等小尺度失真区域。

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/005_Table_3.jpg]]
*Table 3: Quantitative evaluation of the Context-Aware Perception Agent on distortion-aware saliency prediction. Higher AUC-Judd, NSS, CC, SIM and lower KLD indicate better context perception*

### 推理代理评估与消融

Table 4 展示了人类对齐推理代理在三个 VLM 骨干上的诊断准确率及训练策略消融。经渐进式对齐（SFT→GRPO）后，三个骨干均达到最高准确率：Qwen2.5-VL 80.10%，GLM-4.1V 79.26%，Ovis2.5 80.62%。

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/010_Table_4.jpg]]
*Table 4: Quantitative evaluation and ablation of the Human-Alignment Reasoning Agent*

**渐进式训练的关键作用。** 单独的 SFT 或单独的 GRPO 在所有指标上均低于 SFT+GRPO 组合。单独 GRPO 在早期训练阶段易导致格式混乱与事实漂移，而 SFT 初始化提供了稳定的先验，GRPO 在此基础上进一步对齐人类偏好并消除幻觉。

### 感知代理消融

Table 5 的消融研究表明，注意力模块与 KLD 损失的组合带来最佳显著性预测性能，二者互补：仅保留注意力模块或仅保留 KLD 损失均导致 AUC-Judd、NSS 下降，验证了混合损失函数 $\mathcal{L}_{\mathrm{sal}} = \alpha \mathcal{L}_{\mathrm{MSE}}(S, \hat{S}) + (1-\alpha) \mathcal{L}_{\mathrm{KLD}}(S, \hat{S})$ 中像素精度与分布一致性之间的平衡是必要的。

![[assets/figures/papers/paper_list_l2161_https_arxiv_org_abs_2601_02046/figures/009_Table_5.jpg]]
*Table 5: Ablation study of the Context-Aware Perception Agent on attention and KLD loss components*

### 定性分析

Figure 4 展示了跨多样化提示的修复定性比较。白色边界框标注的放大区域显示，Agentic Retoucher 能够修复细粒度几何细节（如面部、手指、脚部），保持连贯的阴影和自然边界，同时维持全局视觉和谐。相比之下，VLM-based 和 mask-based 基线在局部失真修复上常出现不自然的纹理或边界不一致。

### 失败模式与局限

当前分析中未提供系统性的失败模式记录。从方法设计推断，潜在局限包括：感知代理对未见失真类型的泛化能力尚待验证；迭代修正过程收敛于 2-3 轮，但极端失真可能需要更多轮次或超出工具库能力；GRPO 对齐依赖人类偏好数据质量，偏好标注偏差可能影响诊断准确性。以上推断需对照论文原文手动确认。



## 定位与知识库关联

### 1. 与基线工作的关系

Agentic Retoucher 并非孤立地提出一种新的修复模型，而是在现有修复工具之上构建了一个自主的“感知-推理-动作”决策闭环。其核心创新在于**将修复能力从“执行层”解耦到“决策层”**，使得任何底层修复工具（VLM引导或掩码引导）均可被纳入框架中统一调度。这一设计使其与现有基线形成明确的功能层次关系：

- **相对于VLM引导修复基线（Qwen-Edit、Gemini 2.5 Flash Image、Flux-fill）**：这些方法直接依赖VLMs的文本描述来指导修复，但VLMs本身在AIGC图像的失真定位上存在严重幻觉——如 Figure 1 左侧所示，即使给出显式区域提示，现有VLMs仍无法准确定位失真。Agentic Retoucher 通过感知代理提供的上下文感知显著性图，为这些VLM工具补充了精确的空间定位信息，从而将修复从“盲引导”转变为“视觉锚定引导”。

- **相对于掩码引导修复基线（SD-inpainting）**：传统掩码修复需要手工绘制掩码，无法自主发现失真。Agentic Retoucher 的感知代理自动生成失真显著图作为掩码候选，使掩码修复工具获得了自主感知能力。

- **相对于感知评估基线（RichHF, Liang et al., CVPR 2024）**：RichHF 可生成失真热力图，但仅停留在评估层面，缺乏后续的诊断与修复链路。Agentic Retoucher 将显著性预测作为闭环的第一步，后续接续推理与动作代理，形成完整的修复流水线。在显著性预测精度上，感知代理达到 AUC-Judd=0.9336、NSS=1.2087，显著优于 RichHF 和通用VLMs（Table 3），验证了上下文感知设计的有效性。

### 2. 方法适用边界

Agentic Retoucher 的设计隐含以下适用前提与边界：

- **失真类型边界**：框架针对的是**局部小尺度失真**（肢体异常、面部缺陷、文字错误、物体交互不合理等），这些失真在 GenBlemish-27K 数据集中占据主导（手部失真占46.8%，面部缺陷占15.7%）。对于全局性风格偏差、整体构图失衡或语义层面的高阶不一致，框架的局部修复范式可能不适用——其感知代理输出的是像素级显著性图，天然偏向局部异常检测。

- **工具依赖性**：动作代理的自适应选择依赖于工具库中已有修复工具的能力上限。若底层修复工具（如SD-inpainting）本身对某类失真修复能力有限，Agentic Retoucher 的决策层无法超越该工具的性能天花板。Table 1 中不同工具组合的性能差异（如 SD-inpainting 在 SynArtifacts-1K 上整体分最高，而 Qwen-Edit 在 GenBlemish-27K 上 plausibility 最高）印证了这一点。

- **迭代收敛假设**：框架设计为迭代闭环，推理在2-3轮内收敛。对于需要大幅度结构调整或多轮细修的复杂失真，有限的迭代次数可能不足以完全修正。论文未提供迭代次数与修复质量之间的消融分析，这一点需要手动验证。

### 3. 局限与开放问题

基于已验证的分析，当前工作存在以下显式或隐式局限：

- **推理代理的跨模型泛化验证不足**：虽然 Table 4 展示了在 Qwen2.5-VL、GLM-4.1V、Ovis2.5 三个VLM骨干上的推理准确率（80.10%、79.26%、80.62%），但这些均属于相近量级的开源VLM。对于更大规模或架构迥异的VLM（如 Gemini 系列的原生多模态推理能力），渐进对齐策略是否仍然有效，论文未提供证据。

- **感知与推理的误差传播**：框架的流水线设计意味着感知代理的错误定位会直接导致推理代理在错误区域上进行诊断，进而使动作代理修复错误的区域。论文未分析感知代理的假阳性/假阴性对最终修复质量的影响，也未讨论流水线中误差传播的鲁棒性机制。

- **人类评估的样本与偏差**：Table 2 的人类评估仅涉及5名参与者，样本量较小，且未说明评估者的背景（是否具备AIGC图像质量评估经验）。偏好分布的统计显著性未报告置信区间或检验方法，结论的泛化性需要谨慎对待。

- **计算开销与实时性**：框架包含三个代理的串行推理及多轮迭代，推理成本显著高于单次修复基线。论文未报告每张图像的平均推理时间或计算资源消耗，这对于实际部署是关键的缺失信息。

### 4. 知识库定位

Agentic Retoucher 在文本到图像生成的后处理研究谱系中，占据**“自主感知-诊断-修复”闭环范式**的位置。与现有工作的关系可归纳如下：

- **区别于纯评估方法**（如 RichHF, Liang et al., CVPR 2024）：从“检测失真”推进到“理解并修复失真”。

- **区别于端到端修复模型**（如 SD-inpainting、Flux-fill）：不重新训练修复模型，而是在现有工具之上构建决策智能层，实现工具解耦与即插即用。

- **区别于直接使用VLM进行修复的范式**（如 Qwen-Edit、Gemini 2.5 Flash Image）：通过引入感知代理弥补VLM的空间定位缺陷，通过GRPO对齐缓解VLM的幻觉问题，将VLM的角色从“直接执行者”转变为“被引导的诊断者”。

- **训练范式定位**：感知代理采用监督学习（MSE+KLD混合损失），推理代理采用“SFT初始化 + GRPO强化”的渐进式人类偏好对齐，动作代理采用工具库调度的规则/学习混合策略。这种分阶段、分代理的训练策略在AIGC后处理领域属于较新的尝试，其“SFT→GRPO”的渐进路径（Table 4 消融显示单独SFT或GRPO均不如组合）为后续工作提供了可参考的训练范式。



## 原文 PDF

![[paperPDFs/CVPR_2026/Agentic_Retoucher_for_Text_To_Image_Generation.pdf]]

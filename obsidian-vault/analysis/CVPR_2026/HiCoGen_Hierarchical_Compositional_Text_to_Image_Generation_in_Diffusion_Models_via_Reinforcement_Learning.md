---
title: "HiCoGen: Hierarchical Compositional Text-to-Image Generation in Diffusion Models via Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HiCoGen_Hierarchical_Compositional_Text_to_Image_Generation_in_Diffusion_Models_via_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- HiCoGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过将整体生成任务转化为逐步的“合成链”（Chain of Synthesis），将复杂提示分解为多个可控制的子任务，并利用分层奖励（全局、对象、关系）和基于早期去噪阶段注入随机性的衰减随机性调度进行强化学习优化，从根本上提升多层组合生成的准确性和一致性。
primary_logic: 关键思想在于：1）利用大语言模型逐步解析和改写复杂提示，并将前一步生成的图像作为下一步的视觉上下文，从而以渐进方式构建复杂场景，避免概念混淆；2）理论证明将随机性集中在扩散去噪的早期阶段可最大化样本多样性，从而为强化学习提供有效的探索空间，并通过余弦衰减的调度器实现。
claims:
- 在HiCoPrompt基准上，HiCoGen在所有评估指标上均远超现有文本到图像模型，其中主体存在准确率(Acc_exist)相较于Qwen-Image提升约9个百分点。
- 消融实验表明，移除对象奖励导致属性准确率下降约14%，移除关系奖励导致关系准确率下降约4%，验证了分层奖励机制对提升组合生成质量的关键作用。
- 理论证明（Theorem 1）最优样本多样性要求将随机性预算集中分配在生成早期，据此设计的单调递减（余弦衰减）随机性调度大幅提高了扩散强化学习的样本多样性。
- 在处理3个及以上主体的极端复杂场景时，HiCoGen依然优于其他模型，有效缓解了概念缺失问题，证明合成链策略能够应对高难度组合生成。
---

# HiCoGen: Hierarchical Compositional Text-to-Image Generation in Diffusion Models via Reinforcement Learning

> [!tip] 核心洞察
> 关键思想在于：1）利用大语言模型逐步解析和改写复杂提示，并将前一步生成的图像作为下一步的视觉上下文，从而以渐进方式构建复杂场景，避免概念混淆；2）理论证明将随机性集中在扩散去噪的早期阶段可最大化样本多样性，从而为强化学习提供有效的探索空间，并通过余弦衰减的调度器实现。

| 字段 | 内容 |
|------|------|
| 中文题名 | HiCoGen：基于强化学习的扩散模型分层组合文本到图像生成 |
| 英文题名 | HiCoGen: Hierarchical Compositional Text-to-Image Generation in Diffusion Models via Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19965) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | HiCoGen |
| Dataset | HiCoPrompt |

> [!tip] 效果简介
> - HiCoPrompt 上，Acc_exist (主体存在准确率) 0.7127 vs 0.6292 (Qwen-Image) (+0.0835)；Acc_attribute (属性准确率) 0.7673 vs 0.6907 (Qwen-Image) (+0.0766)；Acc_relationship (关系准确率) 0.8203 vs 0.7442 (Qwen-Image) (+0.0761)。

## 概要

**问题瓶颈**：标准文本到图像（T2I）扩散模型在处理包含多个对象与层级关系的复杂提示时，面临文本域与图像域之间日益扩大的语义鸿沟。单一生成过程难以完整覆盖所有概念，导致**概念遗漏**、**概念混淆**以及图像质量下降等突出问题（Figure 1）。

**核心方法**：HiCoGen 提出了一种基于强化学习的分层组合生成框架，其核心思路是将整体生成任务转化为**合成链（Chain of Synthesis）**：首先利用大语言模型（LLM）将复杂提示逐步解析为有序的语义单元，然后迭代生成中间图像作为视觉上下文，最终组装所有概念。在此基础上，HiCoGen 设计了**分层奖励机制**（全局对齐奖励、对象保真度奖励、关系合理性奖励），并理论证明了将随机性集中于扩散去噪早期阶段可最大化样本多样性，据此实现了**衰减随机性调度器**，为强化学习提供有效探索空间。

**方法定位**：HiCoGen 不同于传统一次性整体生成的范式（如 **FLUX.1-dev**、**SDXL**），也区别于仅依赖全局图像-文本对齐奖励的优化策略。其合成链策略与 **Less-to-More**（Wu et al., arXiv 2025）的渐进生成思路存在关联，但 HiCoGen 通过分层奖励和衰减随机性调度，在多对象层级组合生成上实现了更精细的控制。

**主要结果**：在 HiCoPrompt 基准（3,000 个英文测试提示）上，HiCoGen 在所有评估指标上均显著超越现有模型。其中，主体存在准确率（Acc_exist）相较于 **Qwen-Image**（Wu et al., 2025）提升约 9 个百分点（0.7127 vs. 0.6292），属性准确率提升约 7.7 个百分点，关系准确率提升约 7.6 个百分点（Table 2）。消融实验进一步验证了分层奖励各组件的关键作用：移除对象奖励导致属性准确率下降约 14%，移除关系奖励导致关系准确率下降约 4%（Table 3）。在处理 3 个及以上主体的极端复杂场景时，HiCoGen 依然保持优势，有效缓解了概念缺失问题（Table 4）。

文本到图像（T2I）生成模型近年来取得了显著进展，**FLUX.1-dev**（Black Forest Labs, 2024）、**SDXL**（Lacey et al., arXiv 2023）等主流模型已能根据简单文本描述生成高质量的图像。然而，当面对包含多个对象、复杂属性和明确层级关系的复杂提示时，这些模型的生成质量急剧下降。核心瓶颈在于：文本与图像域之间存在巨大的语义鸿沟，随着提示复杂度的增加，单一的一次性生成过程难以准确覆盖所有概念，导致**概念遗漏**、**概念混淆**和**图像质量退化**三大突出问题。

具体而言，现有方法存在以下结构性缺口：

1. **一次性生成的局限性**：标准扩散模型将完整提示直接输入模型进行端到端生成，缺乏对复杂语义的逐步解构能力。当提示包含多个主体及其交互关系时，模型往往只能捕获部分概念而丢失其余内容。

2. **组合性监督的缺失**：现有训练范式主要依赖全局的文本-图像对齐信号（如CLIP score），缺乏对对象级别的保真度、属性准确性和关系合理性的细粒度监督，导致生成结果在细节层面容易出现偏差。

3. **探索与优化困境**：将强化学习应用于扩散模型时，标准确定性采样或均匀随机性策略导致生成样本多样性不足，限制了RL优化的探索空间，难以有效提升组合生成能力。

针对上述挑战，HiCoGen提出了一个全新的视角：将复杂文本到图像的生成任务转化为**逐步的“合成链”（Chain of Synthesis）**过程。其核心动机在于——正如人类画家在创作复杂场景时会先勾勒主体再逐步添加细节一样，生成模型也应当通过分解-合成的方式，将复杂提示拆解为多个可控制的子任务，以前一步生成的图像作为下一步的视觉上下文，从而以渐进方式构建完整场景，从根本上避免概念混淆和遗漏。

这一动机直接催生了HiCoGen的三个关键设计：利用大语言模型（LLM）进行提示解析与改写、设计分层奖励机制提供多维度监督信号、以及通过衰减随机性调度为强化学习提供充分的探索多样性。三者协同作用，使得模型能够在保持全局语义一致性的同时，精确控制每个对象的属性和对象间的交互关系。

## 核心方法与创新机理

HiCoGen 的核心创新在于将扩散模型的文本到图像生成从“一次性整体生成”重构为“逐步合成链”，并通过强化学习与分层奖励机制对合成过程进行精细优化。其相对于主流基线（如 FLUX.1-dev、Qwen-Image、SDXL）的关键突破可归纳为四个层面的 **changed slots**。

### 1. 生成范式：从单次整体生成到 Chain of Synthesis

标准扩散模型（如 FLUX.1-dev、Qwen-Image）将完整的复杂提示一次性输入模型，试图在单次去噪过程中覆盖所有概念。当提示包含多个主体及其层级关系时，文本-图像域之间的语义鸿沟急剧扩大，导致**概念遗漏**（部分主体未生成）和**概念混淆**（主体属性或关系错乱）——这正是 Figure 1 所揭示的核心瓶颈。

HiCoGen 以 **Chain of Synthesis (CoS)** 替代这一范式：首先由 LLM 将复杂提示解析为有序的主体中心化子提示序列 $\mathcal{O} = \{ P^{(1)}, P^{(2)}, \cdots, P^{(n)} \}$，然后逐步生成每个语义单元，每一步将已生成的图像作为下一步的视觉上下文输入。这种“分步构建-上下文组装”的策略将难以处理的整体任务转化为一系列可控的单主体生成与上下文组合子任务，从根本上缩小了每一步的语义鸿沟（Section 3.2, Figure 2）。

### 2. 奖励函数：从单一全局对齐到分层多维监督

基线方法（如使用 CLIP score 进行微调的工作）仅依赖全局层面的文本-图像对齐信号 $R_{\text{global}} = w_{\text{clip}} \cdot S_{\text{clip}} + w_{\text{hps}} \cdot S_{\text{hps}}$。这种粗粒度奖励无法区分“主体是否存在”“属性是否正确”“关系是否合理”等细粒度组合维度。

HiCoGen 设计了**分层奖励机制**（Section 3.3）：

$$R_{\text{total}} = R_{\text{global}} + R_{\text{subject}} + R_{\text{relationship}}$$

其中：
- **对象奖励** $R_{\text{subject}} = \frac{1}{N} \sum_{i=1}^{N} \big( w_{\text{dino}} \cdot S_{\text{DINOv2}}^{(i)} + w_{\text{vlm}} \cdot S_{\text{vlm}}^{(i)} \big)$：通过 DINOv2 特征余弦相似度衡量生成对象与参考图像的保真度，并用 VLM 评估属性准确性；
- **关系奖励** $R_{\text{relationship}} = \frac{1}{N} \sum_{i=1}^{N} S_{\text{vlm}}^{(i)}$：由 VLM 评估主体间交互的合理性与比例关系。

消融实验（Table 3）证实了这一设计的因果效应：移除对象奖励导致属性准确率下降约 14%，移除关系奖励导致关系准确率下降约 4%，仅保留全局奖励时所有指标均显著低于完整分层奖励。这表明对象级和关系级监督是提升组合生成质量的关键因果旋钮。

### 3. 噪声调度：从确定性采样到衰减随机性调度

标准扩散强化学习（如扩散 GRPO）在去噪过程中通常采用确定性采样或均匀随机性，导致生成样本多样性不足——消融实验（Figure 5）显示，未采用衰减随机性时，训练过程中样本间相似度极高（SSIM 接近 1），强化学习的探索空间被严重压缩。

HiCoGen 从理论上证明了**最优样本多样性要求将随机性预算集中分配在生成早期**（Theorem 1, Section 3.4）：在反向扩散 SDE

$$\mathrm{d}\mathbf{z}_t = \left[ \mathbf{f}(\mathbf{z}_t, t) - g(t)^2 \nabla_{\mathbf{z}_t} \log p_t(\mathbf{z}_t) \right] \mathrm{d}t + g(t) \eta(t) \mathrm{d}\mathbf{w}_t$$

中，可控随机性项 $\eta(t)$ 对最终协方差 $\mathbf{\Sigma}_0$ 的贡献通过状态转移矩阵 $\mathbf{\Phi}(0, s)$ 加权，而早期步骤的 $\mathbf{\Phi}(0, s)$ 范数更大，因此早期注入随机性对样本多样性的边际贡献更高。基于此，HiCoGen 设计了**余弦衰减随机性调度器**：

$$\eta(t) = \eta_{\min} + \frac{1}{2} \big( \eta_{\max} - \eta_{\min} \big) \left( 1 + \cos \left( \frac{\pi (T_{\max} - t)}{T_{\max}} \right) \right)$$

将随机性从 $\eta_{\max}$ 递减至 $\eta_{\min}$，在保持生成质量的同时最大化强化学习的探索效率。

### 4. 提示处理：从直接输入到 LLM 解析与改写

基线方法将原始复杂提示直接输入模型，未对提示中的层级结构和属性细节进行显式建模。HiCoGen 引入 **Parse&Rewrite LLM** 模块（Section 3.2），将提示分解为有序子提示序列并对属性进行细化改写，为后续合成链提供结构化的语义输入。这一设计使模型能够显式地处理“谁对谁做了什么”“各主体具有哪些具体属性”等层级关系，而非依赖模型隐式地从扁平文本中推断。

### 创新协同效应

上述四个 changed slots 并非孤立改进，而是形成协同增强的因果链条：LLM 解析将复杂提示分解为可控子任务，Chain of Synthesis 逐步构建图像以缩小每一步的语义鸿沟，衰减随机性调度为强化学习提供充分的探索空间，分层奖励则从全局、对象、关系三个维度提供精细的优化信号。在 HiCoPrompt 基准上，这一协同设计使 HiCoGen 的主体存在准确率达到 0.7127，相较于 Qwen-Image（0.6292）提升约 9 个百分点，属性准确率和关系准确率也分别提升约 7.7 和 7.6 个百分点（Table 2），验证了各创新组件联合作用的显著效果。

HiCoGen 的核心设计思路是将传统扩散模型“一次性生成复杂场景”的单体式任务，转化为一条可控的**合成链（Chain of Synthesis）**。该框架由五个关键模块串联而成，形成“解析—逐步合成—多层级评估—随机探索—策略优化”的闭环。

### 流水线总览

整个流水线如图 Figure 2 所示，其输入为一个包含多主体、多属性及层级关系的复杂文本提示，输出为一张忠实覆盖所有语义概念的图像。处理流程如下：

![[assets/figures/papers/paper_list_l2191_https_arxiv_org_abs_2511_19965/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of our proposed HiCoGen framework. When facing a complex hierarchical compositional prompt, HiCoGen applies the Chain of Synthesis to progressively construct the image part-by-part and employs in-context generative models to assemble the different components into the final image. This ensures all the concepts in the text domain are present in the image domain*

1. **提示解析与改写（Parse&Rewrite LLM）**  
   首先，一个大语言模型（LLM）将复杂提示分解为一组有序的、以主体为中心的子提示。每个子提示进一步被细化为具体的属性描述，最终形成结构化的语义单元序列，为后续逐步合成提供精确的文本指导。

2. **合成链逐步生成（Chain of Synthesis）**  
   生成过程不再是一次性完成，而是按子提示顺序逐步推进：每一步生成一个语义单元的高保真实例，并将已生成的图像作为**视觉上下文**注入到下一步生成中。通过这种“上下文组装”的方式，模型能够逐步将不同组件融合到同一场景中，从根本上缓解概念遗漏与混淆问题。

3. **分层奖励评估（Hierarchical Reward）**  
   每张生成的图像会接受三个层级的奖励信号评估：
   - **全局奖励**：由 CLIP 分数与人类偏好分数加权构成，衡量整体文本-图像对齐与审美质量。
   - **对象奖励**：利用 DINOv2 特征相似度与 VLM 评估，逐一检查每个主体的保真度与属性准确性。
   - **关系奖励**：通过 VLM 评估主体间的交互合理性与空间关系。
   三层奖励的加权和构成总奖励 $R_{\mathrm{total}}$，为强化学习提供细粒度的监督信号。

4. **衰减随机性调度（Decaying Stochasticity Scheduler）**  
   为保障强化学习的探索效率，框架在扩散去噪过程中引入了可控随机性项 $\eta(t)$。理论分析（Theorem 1）证明，将随机性预算集中在去噪早期阶段可最大化样本多样性。据此，实际采用余弦衰减调度器，使 $\eta(t)$ 从 $\eta_{\max}$ 平滑递减至 $\eta_{\min}$，在训练初期提供充足的探索空间，后期则保证生成质量。

5. **GRPO 策略优化（GRPO-based RL Training）**  
   整个合成链与扩散模型通过 GRPO 算法进行端到端的强化学习微调。模型在分层奖励的驱动下，逐步学会在合成链的每一步做出最优的去噪决策，从而提升最终图像在主体存在、属性准确和关系合理性等多个维度的综合表现。

### 模块间的数据流与依赖关系

上述模块的协作关系可概括为：**LLM 解析器**为**合成链**提供结构化的子任务序列；**合成链**生成的中间及最终图像进入**分层奖励模块**进行评估；**衰减随机性调度器**作用于扩散采样过程，为策略探索提供多样性保障；**GRPO 优化器**则利用分层奖励信号，反向更新合成链与扩散模型的参数。这一闭环设计使得 HiCoGen 能够在复杂组合生成任务上，系统性地提升多概念覆盖的完整性与一致性。

![[assets/figures/papers/paper_list_l2191_https_arxiv_org_abs_2511_19965/figures/001_Figure_1.jpg]]
*Figure 1: The motivation of HiCoGen. The semantic gap between text and images widens as the complexity of the text increases, particularly involving the prompts with a hierarchical relationship. While a single T2I model performs well in generating individual objects, it suffers from concept missing and confusion when processing complex prompts. HiCoGen employs a Chain of Synthesis for complex text to preserve the semantic content*

### 3.1 扩散强化学习基础

HiCoGen 将扩散模型的迭代去噪过程建模为强化学习的策略优化问题。给定文本条件 $\mathbf{c}$，扩散模型 $\pi_\theta$ 通过 $T$ 步去噪生成图像 $\mathbf{y}$。前向扩散过程采用流匹配公式，将真实数据 $\mathbf{z}_0$ 线性加噪至纯噪声：

$$\mathbf{z}_t = (1 - t) \mathbf{z}_0 + t \epsilon$$

其中 $\epsilon \sim \mathcal{N}(0, \mathbf{I})$。在去噪阶段，模型预测速度场 $\hat{\mathbf{u}} = v_\theta(\mathbf{z}_t, t, \mathbf{c})$，单步去噪更新为：

$$\mathbf{z}_s = \mathbf{z}_t + \hat{\mathbf{u}} \cdot (s - t)$$

HiCoGen 采用 **GRPO（Group Relative Policy Optimization）** 算法进行策略优化。对于每组 $n$ 个采样轨迹，每个样本 $i$ 获得奖励 $r_i$，其优势函数通过组内归一化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \ldots, r_n\})}{\operatorname{std}(\{r_1, r_2, \ldots, r_n\})}$$

基于 PPO 裁剪机制的 GRPO 优化目标为：

$$\mathcal{I}(\theta) = \mathbb{E}_{\{y_i\}_{i=1}^n \sim \pi_{\theta_{old}}(\cdot|\mathbf{c}), \mathbf{a}_{t,i} \sim \pi_{\theta_{old}}(\cdot|\mathbf{s}_{t,i})} \left[ \frac{1}{n} \sum_{i=1}^n \frac{1}{T} \sum_{t=1}^T \operatorname{min} \left( \rho_{t,i} A_i, \operatorname{clip}(\rho_{t,i}, 1-\epsilon, 1+\epsilon) A_i \right) \right]$$

其中 $\rho_{t,i}$ 为新旧策略在时间步 $t$ 的动作概率比，$\epsilon$ 为裁剪阈值。

### 3.2 合成链（Chain of Synthesis）

合成链是 HiCoGen 应对复杂组合生成的核心机制。给定复杂提示 $\mathcal{O}$，首先由 LLM 语义解析器将其分解为有序的主体中心化子提示集合：

$$\mathcal{O} = \{ P^{(1)}, P^{(2)}, \cdots, P^{(n)} \}, \quad P^{(i)} = \{ c^{(1)}, c^{(2)}, \cdots, c^{(m)} \}$$

其中每个 $P^{(i)}$ 描述一个语义单元，$c^{(j)}$ 为该单元内的细粒度属性描述。合成过程按序执行：第 $i$ 步将前 $i-1$ 步生成的图像作为视觉上下文，注入当前子提示 $P^{(i)}$ 进行生成，逐步构建包含所有概念的完整图像。这一策略将不可解的整体生成任务转化为一系列可控的单主体生成与上下文组合子任务。

### 3.3 分层奖励机制

HiCoGen 设计了三个层次的奖励信号，为强化学习提供细粒度监督。总奖励为三者之和：

$$R_{\mathrm{total}} = R_{\mathrm{global}} + R_{\mathrm{subject}} + R_{\mathrm{relationship}}$$

**全局奖励** 衡量整体文本-图像对齐与审美质量：

$$R_{\mathrm{global}} = w_{\mathrm{clip}} \cdot S_{\mathrm{clip}} + w_{\mathrm{hps}} \cdot S_{\mathrm{hps}}$$

其中 $S_{\mathrm{clip}}$ 为 CLIP 相似度分数，$S_{\mathrm{hps}}$ 为人类偏好分数（HPSv2）。

**对象奖励** 评估每个主体的保真度与属性准确性。对于第 $i$ 个主体，使用 GroundingDINO 检测并裁剪目标区域，计算其与参考图像的 DINOv2 余弦相似度：

$$S_{\mathrm{DINOv2}} = \cos \left( \mathrm{DINOv2}(I_{\mathrm{cropped}}), \mathrm{DINOv2}(I_{\mathrm{ref}}) \right)$$

同时由 VLM 对属性匹配程度进行评分 $S_{\mathrm{vlm}}^{(i)}$。$N$ 个主体的对象奖励为：

$$R_{\mathrm{subject}} = \frac{1}{N} \sum_{i=1}^{N} \Big( w_{\mathrm{dino}} \cdot S_{\mathrm{DINOv2}}^{(i)} + w_{\mathrm{vlm}} \cdot S_{\mathrm{vlm}}^{(i)} \Big)$$

**关系奖励** 关注主体间交互的合理性，由 VLM 对空间关系、比例协调性等方面进行综合评分：

$$R_{\mathrm{relationship}} = \frac{1}{N} \sum_{i=1}^{N} \left( S_{\mathrm{vlm}}^{(i)} \right)$$

### 3.4 衰减随机性调度

为增强强化学习的探索能力，HiCoGen 在标准反向扩散过程中引入可控随机性项 $\eta(t) \geq 0$，得到增广反向 SDE：

$$\mathrm{d}\mathbf{z}_t = \left[ \mathbf{f}(\mathbf{z}_t, t) - g(t)^2 \nabla_{\mathbf{z}_t} \log p_t(\mathbf{z}_t) \right] \mathrm{d}t + g(t) \eta(t) \mathrm{d}\mathbf{w}_t$$

理论分析（Theorem 1）表明，最终生成样本的协方差由早期扰动的加权积分决定：

$$\pmb{\Sigma}_0 = \int_0^T \pmb{\Phi}(0, s) \left( g(s)^2 \eta(s)^2 \mathbf{I} \right) \pmb{\Phi}(0, s)^\top ds$$

其中 $\pmb{\Phi}$ 为状态转移矩阵，权重函数 $W(s)$ 在早期阶段数值更大。因此，在总随机性预算固定的约束下，最大化样本多样性等价于求解变分问题：

$$\operatorname*{max}_{\eta(t)^2 \geq 0} \int_0^T \eta(s)^2 W(s) ds, \quad \mathrm{s.t.} \int_0^T \eta(s)^2 ds = C$$

最优解要求将随机性集中于生成早期。HiCoGen 据此设计了余弦衰减调度器，使 $\eta(t)$ 从 $\eta_{\max}$ 单调递减至 $\eta_{\min}$：

$$\eta(t) = \eta_{\operatorname*{min}} + \frac{1}{2} \big( \eta_{\operatorname*{max}} - \eta_{\operatorname*{min}} \big) \left( 1 + \cos \left( \frac{\pi (T_{\operatorname*{max}} - t)}{T_{\operatorname*{max}}} \right) \right)$$

该调度确保了训练初期的高探索多样性，同时随着去噪推进逐步收敛至确定性生成。

## 实验与关键发现

### 实验设置

HiCoGen 的实验基于自建的 **HiCoPrompt** 基准数据集。该数据集专门针对层级组合生成设计，包含 3,000 个英文测试提示和 12,000 个用于强化学习训练的提示。与现有 T2I 基准相比，HiCoPrompt 的核心挑战在于：为每个主体提供详尽且具体的属性描述，确保即使同类别的主体也具备鲜明特征，同时明确定义了主体之间的层级关系（Table 1）。

![[assets/figures/papers/paper_list_l2191_https_arxiv_org_abs_2511_19965/figures/004_Table_1.jpg]]
*Table 1: Comparison of other T2I benchmarks. The primary challenge of HiCoPrompt compared to other datasets lies in its detailed and specific descriptions for each subject, ensuring that even subjects within the same category exhibit distinct characteristics. At the same time, there exists a clear hierarchical relationship between subjects*

评估体系覆盖多个维度：
- **主体存在准确率 (Acc_exist)**：衡量生成图像中所有指定主体是否出现。
- **属性准确率 (Acc_attribute)**：衡量主体属性（颜色、纹理等）是否正确呈现。
- **关系准确率 (Acc_relationship)**：衡量主体间的空间、交互关系是否合理。
- **CLIP Score**：文本-图像整体对齐度。
- **HPSv2**：人类偏好评分。

以上指标均依赖 VLM、CLIP、DINOv2 等自动评判模型。需要指出的是，该评估体系尚未经过大规模人工评估，主观审美与真实人类偏好之间可能存在偏差。

### 主实验结果

在 HiCoPrompt 基准上，HiCoGen 在所有评估指标上均显著超越现有文本到图像模型和主体驱动生成模型（Table 2）。

![[assets/figures/papers/paper_list_l2191_https_arxiv_org_abs_2511_19965/figures/005_Table_2.jpg]]
*Table 2: Comparison of the proposed HiCoGen and other text-to-image models. HiCoGen outperforms other text-to-image models or subject-driven generative models in all metrics*

**与大型通用模型的对比**：相较于 **Qwen-Image** (Wu et al., 2025)，HiCoGen 在主体存在准确率上提升约 8.4 个百分点（0.7127 vs. 0.6292），属性准确率提升约 7.7 个百分点（0.7673 vs. 0.6907），关系准确率提升约 7.6 个百分点（0.8203 vs. 0.7442）。在 CLIP Score 和 HPSv2 上，HiCoGen 同样取得领先，其中 HPSv2 相较于 **FLUX.1-dev** (Black Forest Labs, 2024) 提升约 0.038（0.3357 vs. 0.2974）。

**与主体驱动模型的对比**：相较于 **DreamBooth** (Ruiz et al., CVPR 2023) 和 **MS-Diffusion** (Wang et al., arXiv 2024) 等专门针对主体保真度优化的模型，HiCoGen 在关系准确率和全局对齐上展现出明显优势。这验证了 Chain of Synthesis 策略在逐步构建复杂场景时，能够有效避免概念遗漏和概念混淆。

**定性结果**（Figure 4）直观展示了 HiCoGen 在处理包含明确层级关系和多个复杂主体的提示时，显著缓解了概念缺失或混淆问题。当提示涉及多个具有不同属性的主体时，基线模型往往遗漏部分主体或混淆其属性，而 HiCoGen 能够准确呈现所有概念。

### 消融实验

为验证分层奖励机制各组件的作用，论文进行了系统的消融实验（Table 3）。

![[assets/figures/papers/paper_list_l2191_https_arxiv_org_abs_2511_19965/figures/007_Table_3.jpg]]
*Table 3: The ablation studies of using different rewards in HiCoGen*

- **移除对象奖励**：属性准确率下降约 14%，表明对象级别的奖励对保证属性细节（如颜色、纹理）至关重要。仅依赖全局奖励无法有效约束单个主体的细粒度特征。
- **移除关系奖励**：关系准确率降低约 4%，验证了关系奖励在确保主体间交互合理性（如空间位置、相对大小）方面的作用。
- **仅使用全局奖励**：所有指标均低于完整分层奖励配置，进一步证明多维度监督的必要性。全局奖励（CLIP + HPSv2）能够提供整体对齐信号，但缺乏对局部组合细节的约束能力。

**衰减随机性调度的消融**：在训练过程中，当未采用衰减随机性调度时，扩散 GRPO 生成的多个样本之间相似度极高（SSIM 接近 1），样本多样性严重不足（Figure 5）。采用余弦衰减随机性调度后，样本多样性显著提升，为强化学习提供了有效的探索空间。这一结果与 Theorem 1 的理论分析一致：将随机性预算集中分配在生成早期可最大化最终样本的多样性。

### 不同主体数量的鲁棒性分析

为评估 HiCoGen 在不同复杂度场景下的鲁棒性，实验分别统计了 1 个、2 个和 3 个及以上主体时的准确率（Table 4）。结果显示，在处理 3 个及以上主体的极端复杂场景时，HiCoGen 依然优于其他模型，有效缓解了概念缺失问题。这证明 Chain of Synthesis 策略能够应对高难度组合生成，其优势随着场景复杂度的增加而更加突出。

![[assets/figures/papers/paper_list_l2191_https_arxiv_org_abs_2511_19965/figures/009_Table_4.jpg]]
*Table 4: Different number of subjects in generated images*

### 失败模式与局限性

尽管 HiCoGen 在组合生成上取得了显著提升，但仍存在以下局限：

1. **LLM 解析依赖性**：框架性能高度依赖于 LLM 对复杂提示的解析和改写质量。错误的分解可能导致后续生成偏差，尤其在面对极长或极专业术语的提示时，解析的准确性和鲁棒性尚需进一步验证。

2. **参考图像质量敏感**：对象保真度依赖于参考图像的质量和选择。若参考图像本身不准确或与提示描述存在偏差，可能导致生成对象的外观与预期不符。

3. **外部模型可靠性**：分层奖励机制依赖 VLM、DINOv2、GroundingDino 等外部模型的准确性。这些模型在特定领域（如罕见物体、专业场景）可能不可靠，且增加了计算开销。

4. **计算资源消耗**：强化学习训练过程需要多次扩散采样，计算资源消耗较大，可能限制了在资源受限环境下的应用。

5. **泛化性待验证**：实验仅在自建的 HiCoPrompt 基准（3,000 个英文测试提示）上进行，泛化到其他语言或更广泛真实场景的能力尚需进一步验证。

## 定位与知识库关联

### 与现有工作的关系

HiCoGen 处于**组合式文本到图像生成**与**扩散模型强化学习微调**两条研究线的交汇点，其核心贡献在于将二者通过“合成链”与“分层奖励”机制有机融合。

**相对于一次性生成范式**：主流 T2I 模型如 **FLUX.1-dev**（Black Forest Labs, 2024）、**SDXL**（Lacey et al., arXiv 2023）和 **Qwen-Image**（Wu et al., 2025）均采用端到端的一次性整体生成策略。当面对包含多主体、多属性及层级关系的复杂提示时，这些模型普遍遭遇概念遗漏与概念混淆问题——这是 HiCoGen 试图解决的核心瓶颈。HiCoGen 通过 Chain of Synthesis 将单一生成任务转化为逐步构建的序列，从根本上改变了问题结构。

**相对于主体驱动生成方法**：**DreamBooth**（Ruiz et al., CVPR 2023）和 **MS-Diffusion**（Wang et al., arXiv 2024）等主体驱动方法可生成特定主体的高保真图像，但通常需要多张参考图像进行微调，且难以处理多主体间的复杂交互关系。HiCoGen 借鉴了主体驱动生成中“将主体注入场景”的思想，但通过 LLM 解析与合成链策略，实现了无需额外微调的多主体场景组装。

**相对于上下文生成方法**：**Less-to-More**（Wu et al., arXiv 2025）利用上下文生成模型逐步构建场景，与 HiCoGen 的合成链思想有相似之处。HiCoGen 的差异化在于：(1) 引入了分层奖励机制对每一步合成进行精细监督；(2) 通过衰减随机性调度为强化学习提供有效的探索空间，从而在组合准确性上取得显著提升。

**相对于扩散强化学习**：现有扩散 RL 方法（如基于 GRPO 的微调）通常仅使用全局图像-文本对齐奖励（如 CLIP score），缺乏对组合细节的细粒度反馈。HiCoGen 的分层奖励机制——全局奖励（CLIP + HPSv2）、对象奖励（DINOv2 相似度 + VLM 评估）、关系奖励（VLM 交互评估）——为扩散 RL 提供了多维度监督信号，消融实验（Table 3）证实移除对象奖励导致属性准确率下降约 14%，移除关系奖励导致关系准确率下降约 4%。

### 适用边界

HiCoGen 的有效性建立在以下前提之上：

1. **LLM 解析质量依赖**：合成链的构建高度依赖于 LLM 对复杂提示的语义解析与改写质量。错误的分解或属性遗漏会直接传播到后续生成步骤，导致最终图像与原始意图偏离。在面对极长提示或包含高度专业术语的文本时，LLM 解析的鲁棒性尚需验证。

2. **参考图像保真度要求**：对象级别的奖励计算依赖 DINOv2 特征与参考图像的余弦相似度。若参考图像选择不当或质量不佳，对象保真度评估将失准，进而影响 RL 优化方向。

3. **外部模型可靠性边界**：分层奖励机制依赖 VLM、DINOv2、GroundingDino 等外部模型，这些模型在特定领域（如医学影像、罕见物体类别）的准确性可能不足，且增加了推理时的计算开销。

4. **语言与场景泛化**：实验仅在自建的 HiCoPrompt 基准（3,000 个英文测试提示）上进行，该基准虽覆盖多主体层级关系，但泛化到其他语言或更广泛真实场景的能力尚需进一步验证。

### 局限与开放问题

**当前局限**：

- 强化学习训练需要多次扩散采样，计算资源消耗较大，限制了在资源受限环境下的应用。
- 框架性能高度依赖 LLM 解析的准确性，缺乏对解析错误的自动纠正机制。
- 对象保真度与参考图像质量强耦合，实际部署中参考图像的选择策略尚未标准化。

**开放问题**：

1. **跨模态推广**：Chain of Synthesis 的逐步构建思想是否可推广到视频生成、3D 场景合成等其他模态？
2. **自适应调度**：能否根据推理时的提示复杂度自适应调整衰减随机性调度参数，以平衡生成质量与多样性？
3. **端到端简化**：能否通过端到端训练减少对外部 LLM 和 VLM 的依赖，将解析与评估能力内化到生成模型中？
4. **LLM 解析鲁棒性**：如何定量衡量并提升 LLM 解析的准确性和鲁棒性，尤其是在面对极长或极专业术语的提示时？
5. **奖励维度扩展**：除了全局、对象和关系奖励，是否还需要引入结构一致性、光照协调等其他维度的奖励，以进一步提升生成质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/HiCoGen_Hierarchical_Compositional_Text_to_Image_Generation_in_Diffusion_Models_via_Reinforcement_Learning.pdf]]

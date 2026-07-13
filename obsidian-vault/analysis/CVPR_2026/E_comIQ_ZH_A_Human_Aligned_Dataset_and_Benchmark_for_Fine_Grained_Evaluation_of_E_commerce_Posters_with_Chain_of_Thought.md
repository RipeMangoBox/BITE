---
title: "E-comIQ-ZH: A Human-Aligned Dataset and Benchmark for Fine-Grained Evaluation of E-commerce Posters with Chain-of-Thought"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/E_comIQ_ZH_A_Human_Aligned_Dataset_and_Benchmark_for_Fine_Grained_Evaluation_of_E_commerce_Posters_with_Chain_of_Thought.pdf
project_link: null
code_link: "https://github.com/4mm7/EcomIQ-ZH"
aliases:
- ECM
- E-comIQ-ZH
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建了首个面向电商海报的多维度数据集E-comIQ-18k，提供专家校准的思维链（CoT）理由，并据此训练专用评估模型E-comIQ-M。
primary_logic: 将电商海报质量解耦为对象、背景、文本、布局四个维度，并利用人类专家编辑的思维链理由指导多模态语言模型进行两阶段训练（SFT+GRPO），从而让评估模型学会对齐专家判断的细粒度评分标准。
claims:
- 文本维度是电商海报质量的主要瓶颈：在存在任何维度低于3.0的图像中，文本维度占比44.8%，并且文本与总体质量的Pearson相关最高（ρ=0.67）。
- 两阶段训练（SFT+GRPO）使E-comIQ-M在测试集上总体SRCC从基础模型Qwen2.5-VL-7B的0.119提升至0.433，显著超越通用MLLM和专业评估器。
- 在E-comIQ-Bench上，当前最强生成模型SeeDream的总体人类评分3.65略高于原始商家海报3.78（原文为3.65 vs 3.78），但文本和对象质量仍为生成式海报的主要短板。
- E-comIQ-18k test set 上 Overall PLCC = 0.425 (E-comIQ-M)
---

# E-comIQ-ZH: A Human-Aligned Dataset and Benchmark for Fine-Grained Evaluation of E-commerce Posters with Chain-of-Thought

> [!tip] 核心洞察
> 将电商海报质量解耦为对象、背景、文本、布局四个维度，并利用人类专家编辑的思维链理由指导多模态语言模型进行两阶段训练（SFT+GRPO），从而让评估模型学会对齐专家判断的细粒度评分标准。

| 字段 | 内容 |
|------|------|
| 中文题名 | E-comIQ-ZH: 基于思维链的电商海报细粒度评估数据集与基准 |
| 英文题名 | E-comIQ-ZH: A Human-Aligned Dataset and Benchmark for Fine-Grained Evaluation of E-commerce Posters with Chain-of-Thought |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21698) · [Code](https://github.com/4mm7/EcomIQ-ZH) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | E-comIQ-M |
| Dataset | E-comIQ-18k test set, E-comIQ-Bench |

> [!tip] 效果简介
> - E-comIQ-18k test set 上，Overall PLCC 0.425 (E-comIQ-M) vs 0.035 (Qwen2.5-VL-7B) (+0.390)；Overall SRCC 0.433 (E-comIQ-M) vs 0.119 (Qwen2.5-VL-7B) (+0.314)；Overall Acc@0.5 55.6% (E-comIQ-M) vs 29.3% (Qwen2.5-VL-7B) (+26.3%)。
> - E-comIQ-Bench (human scores) 上，Overall human score 3.65 (SeeDream, best generative model) vs 3.78 (Original merchant poster) (-0.13)。

## 概要

电商海报是商品推广的核心视觉载体，其质量直接影响用户的购买决策。然而，现有自动化评估工具主要面向通用美学或失真度量，缺乏对电商海报功能性、多维度质量标准的理解——尤其是中文文字的正确性与可读性。数据分析表明，文本维度在44.8%的弱项案例中成为瓶颈，且与总体质量的相关性最高（Pearson ρ=0.67），这使得低效的人工审查至今难以替代。

针对上述瓶颈，本文构建了**E-comIQ-18k**——首个面向中文电商海报的大规模多维度评估数据集，包含18,000张海报及专家校准的思维链（CoT）理由。在此基础上，提出专用评估模型**E-comIQ-M**，将海报质量解耦为对象、背景、文本、布局四个功能维度，并通过两阶段训练（监督微调SFT + 生成式重排序策略优化GRPO）对齐专家判断的细粒度评分标准。

核心实验结果如下：
- 在E-comIQ-18k测试集上，E-comIQ-M的总体SRCC从基础模型Qwen2.5-VL-7B的0.119提升至0.433，PLCC从0.035提升至0.425，显著超越GPT-4o、Gemini 2.5 Pro等通用MLLM及Q-Insight、VQ-R1等专业评估器。
- 在生成模型基准E-comIQ-Bench上，当前最强生成模型SeeDream的总体人类评分（3.65）仍略低于原始商家海报（3.78），文本和对象质量是生成式海报的主要短板。

在方法谱系上，E-comIQ-M属于**多模态大模型微调 + 强化学习奖励对齐**路线，区别于传统无参考图像质量评估方法（如MUSIQ、SPAQ）和通用MLLM的零样本评分。其关键创新在于：将领域知识注入训练数据与奖励函数设计，使模型学会输出四维功能评分及结构化诊断理由，而非单一美学分数。

本工作为电商海报的自动化细粒度评估提供了首个基准数据集和专用模型，但模型的无参考设计使其无法直接量化主体身份保真度，且在分布外生成数据上的泛化能力仍有待提升。

电商海报是连接商品与消费者的核心视觉媒介，其质量直接影响用户的点击意愿与购买决策。随着AIGC技术的爆发，商家和平台开始大规模采用生成式模型批量制作海报，这使得自动化质量评估成为刚需——人工审查不仅成本高昂，且难以在实时上架流程中规模化部署。然而，现有的自动化评估工具在这一场景中暴露出系统性缺陷。

**现有评估范式的错配。** 主流图像质量评估（IQA）方法长期围绕自然图像的失真保真度或通用美学评分展开，代表性工作如 **MUSIQ**、**SPAQ** 等传统无参考评估器，以及近年涌现的专业评估模型如 **Q-Align**、**Q-Insight**、**VQ-R1** 和 **C2Score**。这些模型的核心设计目标是判断图像是否“看起来好”，而非判断图像是否“能卖货”。电商海报的功能性——产品主体是否完整无变形、促销文字是否清晰可读且无错别字、背景是否与商品调性匹配、版式是否引导视觉动线——完全超出了现有评估框架的覆盖范围。即便是能力最强的通用多模态大模型（如 **GPT-4o**、**Gemini 2.5 Pro**、**Qwen2.5-VL-72B** 等），在面对包含中文笔画级缺陷的海报时，也常常给出虚高的评分，完全遗漏关键的质量故障（见 Figure 1 的定性对比）。

**文本维度的隐性瓶颈。** 电商海报与通用图像的一个本质区别在于文字信息的功能性负载。数据分析揭示了一个被长期忽视的事实：在存在任何维度得分低于3.0（5分制）的“弱项”海报中，文本维度占比高达44.8%，且文本得分与总体质量评分的Pearson相关系数达到ρ=0.67，是所有四个子维度中最高的（见 Figure 5d）。这意味着中文文字的正确性与可读性——包括错别字、笔画缺失、字体渲染模糊等问题——是当前电商海报质量的最大瓶颈，而现有评估器几乎完全不具备对这类缺陷的诊断能力。

**评估粒度的缺失。** 现有方法输出的通常是单一的整体评分，无法定位问题来源。对于需要迭代优化海报的设计师或需要批量筛选的运营人员而言，一个笼统的“3.2分”毫无指导价值。他们需要知道的是：扣分是因为产品边缘有伪影（对象维度），还是因为促销文案字号过小难以辨认（文本维度），抑或是背景色与主图冲突（背景维度）。这种多维度的细粒度诊断能力，是连接自动化评估与实际生产决策的关键缺口。

**领域数据的真空。** 上述问题的根源在于训练数据的缺失。此前不存在一个面向中文电商海报的、包含多维度功能评分与诊断理由的大规模数据集。唯一的电商功能评估数据集 AIGuard 仅覆盖有限维度且缺乏思维链解释。通用IQA数据集（如AVA、KonIQ-10k）的标注标准与电商场景完全脱节。

基于以上分析，本文的核心动机明确：**构建首个面向电商海报的多维度评估数据集E-comIQ-18k，并提供专家校准的思维链（CoT）理由，以此训练一个能够对齐人类专家细粒度判断的专用评估模型E-comIQ-M。** 该模型将电商海报质量解耦为对象、背景、文本、布局四个功能维度，并通过两阶段训练（监督微调SFT + 生成式重排序策略优化GRPO）学会在输出评分的同时给出可解释的诊断推理，从而填补自动化评估与人工审查之间的鸿沟。

## 核心方法与创新机理

### 问题瓶颈与动机

电商海报的自动化质量评估长期受困于两个核心挑战。其一，现有评估模型缺乏对中文电商海报功能性、多维度质量标准的理解——尤其是中文文字的正确性与可读性：在数据集中存在任一维度得分低于3.0的海报中，文本维度占比高达44.8%，且文本得分与总体质量的Pearson相关系数最高（ρ=0.67）[Figure 5d]。其二，通用多模态大模型（MLLM）和专业图像质量评估器均无法有效捕捉笔画级文字缺陷等电商场景特有的细粒度问题，导致自动化工具无法替代低效的人工审查[Figure 1]。

### 数据构建创新：维度解耦与思维链标注

本文的核心主张是将电商海报质量显式解耦为**对象（Object）、背景（Background）、文本（Text）、布局（Layout）**四个功能维度，并据此构建首个面向电商海报的多维度数据集**E-comIQ-18k**（18,000张海报）。与传统图像质量数据集仅提供单一美学评分不同，E-comIQ-18k为每张海报提供：

- **五维专家评分**：四个子维度得分加总体得分，评分范围为1–5分；
- **专家校准的思维链（CoT）理由**：通过人机协同管线生成——先由Qwen-2.5-VL-Max根据专家评分和问题标签生成初版诊断性理由，再经人类专家逐条审核修正[Figure 3]。

四个维度之间的平均Pearson相关系数仅为ρ≈0.24，呈半正交结构[Figure 5c]，表明它们捕捉了互补的质量信号。标注一致性方面，总体评分的Krippendorff’s Alpha达到0.858，宽松准确度（容差0.5）为96.4%[Table 1]，验证了专家标注的可靠性。

### 训练策略创新：SFT+GRPO两阶段对齐

**E-comIQ-M**以Qwen-2.5-VL-7B-Instruct为多模态主干，通过两阶段训练将通用MLLM转化为电商海报专用评估器：

| 训练阶段 | 数据规模 | 核心目标 |
|---------|---------|---------|
| **监督微调（SFT）** | 完整15k训练集 | 学习领域概念、评分格式与CoT理由生成 |
| **生成式重排序策略优化（GRPO）** | 精选3k困难子集 | 利用组合奖励函数进一步校准评分精度 |

GRPO阶段的设计是本方法的关键创新。与简单使用交叉熵损失的SFT不同，GRPO引入了一个精心设计的**组合奖励函数**：

$$R_{\mathrm{score}}(x, y) = \lambda_{\mathrm{score}} R_{\mathrm{acc}}(x, y) + (1 - \lambda_{\mathrm{score}}) R_{\mathrm{dist}}(x, y)$$

其中 $\lambda_{\mathrm{score}}=0.65$ 平衡两项子奖励：

- **精度奖励 $R_{\mathrm{acc}}$**：对五个评分维度的预测误差是否在容差 $\tau=0.2$ 内进行指示平均，并引入层级跨越惩罚 $p_i$——当预测得分与真实得分跨越质量层级（如从“良好”误判为“较差”）时，该项权重降至0.7：

$$R_{\mathrm{acc}}(x, y) = \frac{1}{5} \sum_{i=1}^{5} p_i \cdot \mathbb{1}\big(|S_{\mathrm{pred}}^i(y) - S_{\mathrm{gt}}^i| \leq \tau\big)$$

- **分布奖励 $R_{\mathrm{dist}}$**：以指数形式惩罚预测的四维子得分向量与真实向量的欧氏距离，$\alpha=0.5$，迫使模型保持子评分之间的几何结构一致性：

$$R_{\mathrm{dist}}(x, y) = \exp\left(-\alpha \cdot \|\vec{v}_{\mathrm{pred}}(y) - \vec{v}_{\mathrm{gt}}\|_2\right)$$

最终奖励 $R(x, y) = R_{\mathrm{score}}(x, y) + \lambda_{\mathrm{fmt}} R_{\mathrm{fmt}}(y)$ 还包含格式奖励 $R_{\mathrm{fmt}}$，确保输出符合结构化JSON格式。

消融实验[Table 5]系统验证了该训练策略的有效性：（1）**仅GRPO训练**的效果显著差于SFT only，表明纯强化学习不足以处理该多维连续评分任务；（2）在SFT基础上增加**简单精度奖励**（SFT+GRPO Simple）即可提升性能，尤其在文本维度；（3）完整的**SFT+GRPO Complex**（结合精度与分布奖励）进一步提升了所有维度的相关性与准确度，验证了分布项对子评分几何结构对齐的贡献。

### 输出形式创新：思维链诊断+结构化评分

E-comIQ-M的输出形式也区别于传统评估器。模型在 `<think>` 块中生成中文自然语言诊断，解释各维度的评分依据；在 `<answer>` 块中输出包含五维评分（Object, Background, Text, Layout, Overall）的JSON对象[Appendix B.1, Figure 13]。这种设计使评估结果兼具**可解释性**和**可编程性**，便于下游自动化流程集成。

### 创新总结

E-comIQ-M相对于现有baseline的核心创新可归纳为四个“changed slots”：

1. **训练数据**：从通用预训练数据升级为E-comIQ-18k多维度专家评分与校准CoT理由；
2. **训练策略**：从单阶段SFT升级为SFT+GRPO两阶段训练，利用困难子集上的组合奖励进行评分校准；
3. **奖励函数**：从简单交叉熵损失升级为精度项+分布项的组合奖励，显式建模层级跨越惩罚与子评分向量几何约束；
4. **输出粒度**：从单一美学评分升级为四维功能评分+总体评分，嵌入思维链自然语言解释。

E-comIQ-ZH 的整体框架由三个紧密协同的模块构成：**数据集构建**、**评估模型训练**与**生成模型基准测试**。框架的核心设计逻辑是：先通过专家标注将电商海报质量解耦为四个功能维度，再借助思维链理由将专家判断显式化，最后用两阶段训练让多模态语言模型学会对齐这些细粒度标准。

### 数据集构建：从专家评分到思维链

数据集构建是整个框架的基石。研究者将电商海报的视觉质量分解为**对象**（产品主体的视觉完整性）、**背景**（场景的兼容性与视觉吸引力）、**文本**（文字的可读性与正确性）、**布局**（整体构图与信息组织）四个维度，每个维度由人类专家给出 1–5 分的连续评分。这一分解并非随意为之——统计分析表明，四个维度之间仅存在弱相关性（平均维度间 Pearson 相关系数约为 0.24），说明它们确实捕获了海报质量的不同侧面。

为了将专家的隐式判断转化为可训练的监督信号，框架引入了人机协同的思维链生成流程（见 Figure 3）：给定专家评分、缺陷标签和海报图像，先用 **Qwen-2.5-VL-Max** 生成初步的诊断性理由，再由人类专家逐条校验和修正。这一流程在保证理由质量的同时大幅降低了纯人工编辑的成本。最终构建的 **E-comIQ-18k** 数据集包含 18,000 张海报，每张均配有四维评分、总体评分以及经过专家校准的中文思维链理由。标注一致性由 Krippendorff's Alpha 验证，总体维度达到 0.858，宽松准确度（0.5 分容差内）为 96.4%，表明专家标注具有高度可靠性。

### 评估模型训练：从监督微调到强化对齐

在数据集之上，框架训练专用的评估模型 **E-comIQ-M**。其主干网络为 **Qwen-2.5-VL-7B-Instruct**，视觉编码器负责处理输入海报图像，多模态语言模型主干融合视觉特征后生成结构化的评估输出。输出格式包含两个关键块：`<think>` 块中生成中文自然语言诊断，解释评分依据；`<answer>` 块中输出包含五个维度（Object、Background、Text、Layout、Overall）评分的 JSON 对象。

训练采用两阶段策略，对应框架图中的 (d)–(e) 部分：

1. **监督微调（SFT）**：在完整的 15k 训练集上进行，让模型初步学习领域概念、评分格式和思维链生成模式。此阶段建立了模型对电商海报质量的基本理解。
2. **生成式重排序策略优化（GRPO）**：在精心筛选的 3k 困难子集上进一步校准评分。GRPO 的关键在于其组合奖励函数，由精度项 $R_{\mathrm{acc}}$ 和分布项 $R_{\mathrm{dist}}$ 加权构成：

$$R_{\mathrm{score}}(x, y) = \lambda_{\mathrm{score}} R_{\mathrm{acc}}(x, y) + (1 - \lambda_{\mathrm{score}}) R_{\mathrm{dist}}(x, y)$$

其中精度奖励 $R_{\mathrm{acc}}$ 对五个维度的预测误差是否在容差 $\tau = 0.2$ 内进行指示平均，并引入层级跨越惩罚（跨层级时权重降至 0.7）；分布奖励 $R_{\mathrm{dist}}$ 以指数形式惩罚预测的四维子得分向量与真实向量的欧氏距离（$\alpha = 0.5$）。平衡系数 $\lambda_{\mathrm{score}}$ 经参数敏感度实验验证设为 0.65。最终奖励还包含一个格式项 $R_{\mathrm{fmt}}$，确保输出结构符合预期。

这一两阶段设计的因果逻辑是：SFT 提供领域知识和基本格式约束，GRPO 则通过奖励信号精细调整评分校准，使模型在困难样本上的判断更接近专家分布。消融实验证实了该设计的必要性——仅 GRPO 训练的效果显著差于仅 SFT，而完整的 SFT+GRPO 在所有维度上均优于仅 SFT 的变体。

### 生成模型基准测试：从评估到诊断

框架的第三个模块 E-comIQ-Bench 将训练好的评估模型应用于诊断生成式模型的海报生成能力。在这一环节，E-comIQ-M 作为自动评估器，对多个主流生成模型输出的海报进行四维评分，并与人类专家评分进行对照。这一设计实现了从“能否评估”到“能否诊断”的闭环：评估模型不仅给出分数，还通过思维链指出具体缺陷，为生成模型的迭代提供可操作的反馈。

### 输入输出流总览

整个框架的信息流可概括为：**输入海报图像** → 视觉编码器提取特征 → 多模态语言模型生成 `<think>` 诊断文本与 `<answer>` JSON 评分 → **输出五维评分与自然语言解释**。训练阶段，这一流程受专家标注的评分和思维链理由监督；推理阶段，模型独立完成从像素到结构化评估的端到端映射。

![[assets/figures/papers/paper_list_l2738_https_arxiv_org_abs_2602_21698/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the E-comIQ-ZH framework. (a–c) E-comIQ-Dataset: multi-dimensional expert annotations with Chain-of-Thought rationales. (d–e) E-comIQ-M: two-stage training via Supervised Fine-Tuning (SFT) and Generative Reranking Policy Optimization (GRPO). (f) E-comIQ-Bench: evaluation of generative models on e-commerce image generation capabilities*

E-comIQ-M 的评估流程由三个核心模块构成：**视觉编码与多模态融合**、**思维链诊断生成**，以及**结构化评分输出**。模型以 Qwen-2.5-VL-7B-Instruct 为骨干，接收电商海报图像后，首先由视觉编码器提取特征并与语言模型进行多模态融合（Section 4.1, Appendix B.1）。随后，模型在 `<think>` 块中生成中文自然语言诊断，逐维度解释评分依据；最终在 `<answer>` 块中输出包含五个维度（Object, Background, Text, Layout, Overall）的 JSON 结构化评分（Appendix B.1, Fig. 13）。

训练策略采用两阶段范式（Section 4.1, Fig. 2）：第一阶段在完整 15k 训练集上进行**监督微调（SFT）**，使模型学习领域概念、评分格式和专家校准的思维链理由；第二阶段在精心筛选的 3k 困难子集上执行**生成式重排序策略优化（GRPO）**，利用精心设计的组合奖励函数进一步校准评分精度与维度间的一致性。

GRPO 阶段的核心在于奖励函数的设计，其总奖励由评分奖励与格式奖励加权构成：

$$R(x, y) = R_{\mathrm{score}}(x, y) + \lambda_{\mathrm{fmt}} R_{\mathrm{fmt}}(y) \tag{1}$$

其中 $R_{\mathrm{fmt}}(y)$ 为格式奖励，$\lambda_{\mathrm{fmt}}$ 为平衡系数。评分奖励 $R_{\mathrm{score}}$ 进一步分解为精度项 $R_{\mathrm{acc}}$ 与分布项 $R_{\mathrm{dist}}$ 的凸组合：

$$R_{\mathrm{score}}(x, y) = \lambda_{\mathrm{score}} R_{\mathrm{acc}}(x, y) + (1 - \lambda_{\mathrm{score}}) R_{\mathrm{dist}}(x, y) \tag{2}$$

其中 $\lambda_{\mathrm{score}}$ 经验性地设为 0.65（Appendix C.1, Fig. 15）。

**精度奖励** $R_{\mathrm{acc}}$ 对五个评分维度（四个子维度加总体评分）的预测误差进行容差判定，并引入层级跨越惩罚以抑制跨质量层级的严重误判：

$$R_{\mathrm{acc}}(x, y) = \frac{1}{5} \sum_{i=1}^{5} p_i \cdot \mathcal{k}\big(|S_{\mathrm{pred}}^i(y) - S_{\mathrm{gt}}^i| \leq \tau\big) \tag{3}$$

其中 $\tau = 0.2$ 为精度容差，指示函数 $\mathcal{k}(\cdot)$ 在预测值与真实值之差不超过 $\tau$ 时返回 1；$p_i$ 为层级惩罚因子——当预测评分与真实评分跨越不同质量层级时 $p_i = 0.7$，否则为 1.0。该设计的直觉在于：跨层级的评分错误（如将“优秀”误判为“较差”）比层内的小幅偏差更具危害性。

**分布奖励** $R_{\mathrm{dist}}$ 从几何结构角度约束四个子维度评分向量的整体一致性，以指数形式惩罚预测向量 $\vec{v}_{\mathrm{pred}}(y)$ 与真实向量 $\vec{v}_{\mathrm{gt}}$ 之间的欧氏距离：

$$R_{\mathrm{dist}}(x, y) = \exp\left(-\alpha \cdot \|\vec{v}_{\mathrm{pred}}(y) - \vec{v}_{\mathrm{gt}}\|_2\right) \tag{4}$$

其中 $\alpha = 0.5$ 控制惩罚强度。消融实验证实，在精度奖励基础上引入分布项可进一步提升所有维度的相关性与准确度（Table 5），表明分布奖励有助于对齐子评分的几何结构，防止预测向量在四维空间中发生系统性偏移。参数敏感度分析进一步验证 $\tau = 0.2$ 和 $\lambda_{\mathrm{score}} = 0.65$ 为当前设定下的最优选择（Appendix C.1, Fig. 14, Fig. 15）。

## 实验与关键发现

### 1. 数据集构建与统计特征

E-comIQ-18k 包含 18,000 张电商海报，每张图像配有专家在四个功能维度（Object、Background、Text、Layout）上的 1–5 分评分及一个 Overall 综合评分。标注一致性经 Krippendorff’s α 检验，Overall 维度 α 达到 0.858，宽松准确率（误差≤0.5）为 96.4%（Table 1），表明专家标注具有高度可靠性。

数据集统计（Figure 5）揭示了几个关键特征：
- **得分分布**：Overall 得分呈多峰分布（Figure 5a），覆盖从低质到高质的全谱段，保证了样本多样性。
- **维度正交性**：四个子维度之间的平均 Pearson 相关系数仅为 ρ ≈ 0.24（Figure 5c），呈半正交结构，说明各维度捕捉了海报质量的不同侧面，单独使用 Overall 评分会丢失大量信息。
- **瓶颈维度**：在至少有一个维度得分低于 3.0 的样本中，Text 维度占比高达 44.8%（Figure 5d），且 Text 与 Overall 的 Pearson 相关性最高（ρ = 0.67），表明中文文字的正确性与可读性是电商海报质量的主要瓶颈。这一发现为后续评估模型的设计提供了直接依据。

与现有数据集的对比（Table 2）显示，E-comIQ-18k 是首个同时具备多维度功能评分、专家校准的思维链（CoT）理由、且专门面向中文电商海报的大规模评估数据集。此前的数据集或聚焦于通用美学/失真度（如 AVA、SPAQ），或仅提供整体偏好标注（如 ImageReward），唯一面向电商功能的 AIGuard 数据集也缺乏 CoT 和多维细粒度评分。

![[assets/figures/papers/paper_list_l2738_https_arxiv_org_abs_2602_21698/figures/006_Table_2.jpg]]
*Table 2: Comparison of E-comIQ-18k with representative image quality, preference, and e-commerce evaluation datasets. Most existing datasets target general aesthetics, distortion fidelity, or holistic AIGC preference, while AIGuard is the only e-commerce functional dataset but relies on binary labels without multidimensional scoring or CoT explanations. E-comIQ-18k uniquely provides e-commerce focused functional multidimensional scores together with expert verified CoT rationales*

### 2. 主实验结果

#### 2.1 与基线的相关性对比（Table 3）

![[assets/figures/papers/paper_list_l2738_https_arxiv_org_abs_2602_21698/figures/008_Table_3.jpg]]
*Table 3: Correlation performance against state-of-the-art models on the E-comIQ-18k test set. Each cell reports PLCC / SRCC. The best result is in bold, and the second-best is underlined*

Table 3 报告了 E-comIQ-M 与三类基线在 E-comIQ-18k 测试集上的 PLCC/SRCC 对比：

**传统无参考图像质量评估器**（MUSIQ、SPAQ 等）在所有维度上表现极弱，Overall SRCC 接近于零，说明基于自然图像失真度训练的模型完全无法理解电商海报的功能性质量标准。

**通用多模态大模型**中，GPT-4o 和 Gemini 2.5 Pro 表现出一定的零样本评估能力（Overall SRCC 分别为 0.245 和 0.346），但远不及经过领域微调的专用模型。值得关注的是，Qwen2.5-VL-7B（E-comIQ-M 的主干模型）在零样本条件下 Overall SRCC 仅为 0.119，而经过两阶段训练后提升至 0.433，增幅达 +0.314。

**专业图像质量评估器**（Q-Insight、VQ-R1、Q-Align 等）整体优于通用模型，其中 Q-Insight 取得 Overall SRCC 0.303 的最佳基线成绩。但 E-comIQ-M 以 Overall PLCC 0.425、SRCC 0.433 显著超越所有基线，在 Background（0.496/0.520）和 Layout（0.483/0.506）维度上的优势尤为突出。

#### 2.2 准确度指标（Table 4）

![[assets/figures/papers/paper_list_l2738_https_arxiv_org_abs_2602_21698/figures/009_Table_4.jpg]]
*Table 4: Accuracy performance against state-of-the-art models on the E-comIQ-18k test set. Each cell reports Acc@0.5 / Acc@1.0 (in %). The best result is in bold, and the second-best is underlined*

Table 4 以 Acc@0.5 和 Acc@1.0 补充了相关性指标。E-comIQ-M 在 Overall 维度上 Acc@0.5 达 55.6%、Acc@1.0 达 81.8%，分别比最强基线 Q-Insight 提升 4.6 和 1.7 个百分点。在 Text 维度上，Acc@0.5 为 49.6%，相比零样本 Qwen2.5-VL-7B 的 22.4% 提升超过一倍，验证了 CoT 理由和两阶段训练对文字质量诊断的有效性。

#### 2.3 生成模型评估基准（Table 6、Table 7）

![[assets/figures/papers/paper_list_l2738_https_arxiv_org_abs_2602_21698/figures/012_Table_6.jpg]]
*Table 6: Benchmark results for leading generative E-comIQ-Ms on E-comIQ-Bench*

在 E-comIQ-Bench 上，人类专家对原始商家海报的 Overall 评分为 3.78，而当前最强的生成模型 SeeDream 得分为 3.65，仅略低于原始海报。各生成模型在 Background 和 Layout 维度上普遍优于或接近原始海报，但在 Text 和 Object 维度上仍为明显短板——这与数据集瓶颈分析的结论一致。Table 7 的客观指标进一步证实：生成模型在主体身份保真度（DINO 相似度）和中文文字准确率（OCR 匹配度）上均与原始海报存在显著差距，其中文字准确率最低的模型不足 40%。

### 3. 消融实验（Table 5）

![[assets/figures/papers/paper_list_l2738_https_arxiv_org_abs_2602_21698/figures/010_Table_5.jpg]]
*Table 5: Ablation studies on the E-comIQ-18k test set. We analyze the impact of different training stages and reward function designs. Each cell reports PLCC / SRCC*

Table 5 系统分析了训练阶段和奖励函数设计的影响：

- **GRPO only vs SFT only**：仅使用 GRPO 训练（无 SFT）在所有维度上显著弱于 SFT only，Overall SRCC 仅为 0.088 vs 0.317。这表明纯强化学习无法有效处理该任务中连续多维评分的学习难度，监督微调阶段对于建立领域概念和评分格式的初始对齐是必需的。

- **SFT + GRPO (Simple)**：在 SFT 基础上增加仅含精度奖励的 GRPO，Overall SRCC 从 0.317 提升至 0.360，Text 维度 SRCC 从 0.287 提升至 0.357，说明强化学习的探索机制有助于在困难样本上进一步校准评分。

- **SFT + GRPO (Complex)**：引入完整的组合奖励（精度项 + 分布项，λ_score=0.65），Overall SRCC 进一步提升至 0.410，所有维度的 PLCC/SRCC 均达到最优。分布奖励 R_dist 通过惩罚子得分向量的欧氏距离，强制模型输出的四维评分保持与真实标注一致的几何结构，这对 Background 和 Layout 维度的提升尤为明显。

奖励函数超参数敏感度实验（Figure 14、Figure 15，附录 C.1）验证了精度容差 τ=0.2 和精度权重 λ_score=0.65 为最优设定。

### 4. 失败模式与局限性

尽管 E-comIQ-M 在测试集上表现优异，但在以下场景中存在明显局限：

1. **分布外泛化不足**：在 E-comIQ-Bench（由生成模型产生的未见海报）上，E-comIQ-M 与人类评分的 Overall PLCC/SRCC 仅约 0.34，远低于测试集上的 0.425/0.433。这表明模型对生成式海报中特有的伪影（如不自然的光影融合、语义不一致的文字渲染）缺乏足够的诊断能力。

2. **主体身份保真度盲区**：E-comIQ-M 作为无参考模型，无法检测生成海报中产品主体的形变、替换或细节丢失。例如，当生成模型将产品颜色或纹理改变但保持视觉美观时，E-comIQ-M 可能给出高分，而人类专家会因身份不一致而扣分。这一缺陷在 Table 7 的客观指标中得到了侧面印证。

3. **数据覆盖偏差**：训练数据主要来源于单一电商平台，品类分布和视觉风格可能存在偏向性，限制了模型在更广泛电商场景（如跨境商品、非标准版式）中的适用性。

4. **文本维度的持续挑战**：尽管 Text 维度的 Acc@0.5 从 22.4% 提升至 49.6%，但仍有超过一半的样本在 0.5 容差内无法命中，说明笔画级错误、字体风格不当等细粒度文字缺陷的识别仍是开放难题。

## 定位与知识库关联

### 核心思想与差异化定位

E-comIQ-ZH 的核心贡献在于将电商海报质量评估从通用美学或失真度量，解耦为**对象、背景、文本、布局**四个功能维度的细粒度诊断任务。这一设计直接回应了现有评估体系的两大盲区：其一，中文文字的正确性与可读性在电商场景中构成主要质量瓶颈（文本维度在 44.8% 的弱项案例中成为短板，且与总体质量的 Pearson 相关最高 ρ=0.67，见 Figure 5d）；其二，通用多模态大模型（如 GPT-4o、Gemini 2.5 Pro）和传统无参考质量评估器（如 MUSIQ、SPAQ）对笔画级中文缺陷几乎无感知能力（Figure 1 定性对比可证）。

与已有的图像质量评估（IQA）和 AIGC 偏好数据集（见表 2 全景对比）相比，E-comIQ-18k 是首个明确针对中文电商海报功能质量的大规模数据集，且提供了**专家校准的思维链（CoT）理由**，使评估过程可解释。这一设计区别于仅提供单一整体分数的 AVA、SPAQ 等数据集，也不同于侧重失真保真度的 KonIQ-10k 或侧重通用偏好的 ImageReward。

### 与基线方法的关系

**传统无参考 IQA 模型**（MUSIQ、SPAQ）在 E-comIQ-18k 测试集上的总体 PLCC/SRCC 仅约 0.05–0.11（Table 3），表明基于自然场景失真统计的特征无法迁移至电商海报的功能语义评估。这一结果并不意外：MUSIQ 等模型的设计目标是感知质量而非功能正确性，对文字错误、布局失衡等高层语义缺陷缺乏建模能力。

**通用多模态大模型**（GPT-4o、Gemini 2.5 Pro、Claude-Sonnet-4.5、Grok-4、Qwen2.5-VL-72B 等）在零样本设置下表现参差。尽管部分模型在背景和布局维度上具有一定判别力（如 Gemini 2.5 Pro 在背景维度的 PLCC 达 0.342），但总体 SRCC 最高仅约 0.119（Qwen2.5-VL-7B），远低于 E-comIQ-M 的 0.433。关键差距集中在**文本维度**：通用 MLLM 对中文字符的笔画级错误（如缺笔、错字、字体渲染异常）几乎完全失明，而 E-comIQ-M 通过领域 SFT 和 GRPO 校准显著弥补了这一短板（文本维度 SRCC 从 0.119 提升至 0.392）。

**专业评估器**（Q-Insight、VQ-R1、Q-Align、DeQA、C2Score）虽在通用 IQA 任务上表现优异，但在电商海报场景中同样受限。Q-Insight 的总体 PLCC 为 0.275，SRCC 为 0.346，已属该类最优，但仍显著低于 E-comIQ-M。值得注意的是，对 Q-Insight 施加同样的两阶段训练（SFT+GRPO）后，其性能可提升至接近 E-comIQ-M 的水平（Table 5 中 Q-Insight+SFT+GRPO 的总体 SRCC 约 0.39–0.41），说明**领域数据和 CoT 监督**是性能提升的主要驱动力，而非主干架构的差异。

### 训练策略的因果机制

E-comIQ-M 的两阶段训练（SFT → GRPO）构成了方法的核心因果链路，消融实验（Table 5）揭示了各阶段的独立贡献：

- **仅 GRPO 训练**（无 SFT 初始化）效果最差（总体 SRCC 约 0.08–0.12），表明纯强化学习在缺乏领域先验时无法有效探索多维连续评分空间。这一发现与 RLHF 在复杂结构化输出任务中的已知局限一致。
- **仅 SFT 训练**即可将总体 SRCC 从基干的 0.119 提升至约 0.35–0.37，证明了 CoT 监督信号在注入领域知识和评分格式方面的关键作用。
- **SFT + GRPO（简单精度奖励）**在 SFT 基础上进一步提升，尤其在文本维度（SRCC 从约 0.35 增至约 0.38），说明 GRPO 的探索机制有助于校准 SFT 阶段的系统性偏差。
- **SFT + GRPO（完整奖励，含分布项 R_dist）**在所有维度上达到最优（总体 SRCC 0.410–0.433），验证了分布奖励对对齐子评分几何结构的必要性。R_dist 通过指数惩罚预测子得分向量与真实向量的欧氏距离（α=0.5），迫使模型不仅关注逐维精度，还维护维度间的相对关系。

奖励函数中的关键超参数经敏感度分析验证：精度容差 τ=0.2 和精度权重 λ_score=0.65 在 E-comIQ-18k 上为最优设定（Figure 14、Figure 15），但需注意这些参数可能依赖于数据集的评分分布特性。

### 适用边界与泛化局限

E-comIQ-M 的适用边界受以下因素约束：

1. **领域依赖性**：训练数据主要来自单一电商平台，类别分布和视觉风格可能存在偏差。在未见过的平台、品类或非电商广告场景中，评分校准可能退化。论文未提供跨平台泛化实验，此处需手动验证。

2. **分布外泛化**：在 E-comIQ-Bench（生成模型产出的海报集合）上，E-comIQ-M 与人类评分的总体 PLCC/SRCC 仅约 0.34（见 Section 5.2），远低于在 E-comIQ-18k 测试集上的 0.425/0.433。这一显著下降表明模型对生成式伪影（如产品变形、文字幻觉）的评估能力有限，且训练集中生成样本的覆盖不足。

3. **无参考设定的固有限制**：E-comIQ-M 无法直接量化主体身份保真度（如生成海报中的产品是否与原图一致）。在 E-comIQ-Bench 上，最强生成模型 SeeDream 的总体人类评分（3.65）已接近原始商家海报（3.78），但客观指标（Table 7）显示其主体相似度（DINO 特征距离）和文字准确率仍显著落后。E-comIQ-M 的评分无法反映这一保真度差距，需依赖额外的参考度量作为补充。

4. **静态图像限定**：当前框架仅适用于单张静态海报，无法直接迁移至视频海报、动态 Banner 或交互式落地页等多模态电商素材。

### 开放问题与未来方向

基于上述局限，以下问题值得进一步探索：

- **主体保真度的隐式注入**：能否在不引入参考图像的条件下，通过对比学习或语义一致性约束，使评估模型隐式感知产品身份是否发生形变或替换？这可能需要构建包含“产品图–生成海报”配对数据的训练集。
- **分布外鲁棒性增强**：针对 E-comIQ-Bench 上的低一致性（ρ≈0.34），是否需要引入生成式对抗样本、领域自适应训练或测试时校准策略？GRPO 的困难子集筛选策略（当前基于评分方差）是否可扩展为基于生成模型特性的主动采样？
- **跨领域迁移**：当前四维评分框架（对象、背景、文本、布局）的维度定义在多大程度上可泛化至服装展示、房产渲染、食品摄影等垂直 AIGC 场景？各领域可能需要定制化的维度定义和相应的知识注入策略。
- **动态内容扩展**：若将评估对象从单张图像扩展至视频或交互式内容，评分维度需如何重构？例如，视频海报可能需引入“时序一致性”和“动效质量”维度，标注协议和 CoT 生成流程也需相应调整。

## 原文 PDF

![[paperPDFs/CVPR_2026/E_comIQ_ZH_A_Human_Aligned_Dataset_and_Benchmark_for_Fine_Grained_Evaluation_of_E_commerce_Posters_with_Chain_of_Thought.pdf]]

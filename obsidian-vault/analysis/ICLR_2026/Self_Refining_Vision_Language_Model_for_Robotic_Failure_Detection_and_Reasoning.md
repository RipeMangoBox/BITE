---
title: "Self-Refining Vision Language Model for Robotic Failure Detection and Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Self_Refining_Vision_Language_Model_for_Robotic_Failure_Detection_and_Reasoning.pdf
openreview_forum_id: jr9hGWQioP
aliases:
- AARBMTMRFDR
- SRVLMRFDR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将故障检测和推理建模为多轮序列精炼过程，配合多任务预测头（分类头专用于检测、语言解码器专用于推理）以及基于熵的自置信度轨迹选择。"
primary_logic: "通过多任务预测头将检测与推理解耦，同时利用离线模仿与在线精炼，在大规模稀疏标签和小规模稠密标签上迭代改进预测，使得视觉语言模型能够在多轮中减少不一致性、提升推理质量，从而兼顾检测精度与开放式、人类可读的推理。"
claims:
- "ARMOR在所有评估数据集上均达到最高的故障检测准确率和推理质量（LLM Fuzzy和ROUGE-L），显著超越现有监督微调基线和闭源VLM。"
- "消融实验表明，多任务预测头、离线模仿、在线模仿和推理精炼的组合是实现最佳性能的关键，缺少精炼会令检测准确率从0.917降至0.803。"
- "在跨域迁移设置中，ARMOR仅依靠目标域的少量稠密标签并结合源域稀疏标签，即能大幅提升检测与推理性能（R→M检测提升至0.990，S→A推理提升+14.6%）。"
- "自我精炼持续降低检测与推理熵，同时提升推理LLM Fuzzy分数，第一轮精炼即带来40%以上的相对提升。"
---

# Self-Refining Vision Language Model for Robotic Failure Detection and Reasoning

> [!tip] 核心洞察
> 通过多任务预测头将检测与推理解耦，同时利用离线模仿与在线精炼，在大规模稀疏标签和小规模稠密标签上迭代改进预测，使得视觉语言模型能够在多轮中减少不一致性、提升推理质量，从而兼顾检测精度与开放式、人类可读的推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自我精炼的视觉语言模型用于机器人故障检测与推理 |
| 英文题名 | Self-Refining Vision Language Model for Robotic Failure Detection and Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jr9hGWQioP); [Project](https://sites.google.com/utexas.edu/armor) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | ARMOR (Adaptive Round-based Multi-task mOdel for Robotic failure detection and reasoning) |
| Dataset | RLBench, Sparrow, Maniskill (R→M) |

> [!tip] 效果简介
> - RLBench 上，Detect Acc. 为 0.917，对比 0.640 (SFT-S+D) / 0.561 (Claude-3.7)，变化 +0.277 / +0.356。
> - RLBench 上，LLM Fuzzy 为 0.718，对比 0.550 (SFT-S+D) / 0.473 (Claude-3.7)，变化 +0.168 / +0.245。
> - Sparrow 上，Detect Acc. 为 0.733，对比 0.620 (SFT-S+D) / 0.517 (Claude-3.7)，变化 +0.113 / +0.216。

## 概述

机器人系统在开放环境中执行操作任务时，不可避免地会遭遇各种故障。及时检测故障并给出可理解的推理，对于提升机器人自主性和人机协作效率至关重要。然而，训练高质量的故障推理模型面临一个核心瓶颈：**数据异质性**。大规模的二值故障标签（成功/失败）可从系统日志中自动获取，但细粒度的自然语言推理标注极其昂贵且稀缺。现有方法要么将推理简化为预定义故障模式的封闭集分类，丧失对未见故障的描述能力；要么要求全套稠密标注进行标准监督微调，无法在异构监督下联合实现精确检测与开放集推理。

针对这一挑战，本文提出 **ARMOR**（**A**daptive **R**ound-based **M**ulti-task m**O**del for **R**obotic failure detection and reasoning），一种自我精炼的视觉语言模型。其核心思想是：**将故障检测与推理建模为多轮序列精炼过程**，通过多任务预测头将检测（分类）与推理（语言生成）解耦，同时利用离线模仿与在线精炼，在大规模稀疏标签和小规模稠密标签上迭代改进预测，使得视觉语言模型能够在多轮中减少不一致性、提升推理质量。

ARMOR 的方法定位与主要贡献如下：

- **方法谱系**：ARMOR 属于视觉语言模型（VLM）驱动的机器人故障分析框架。与将推理简化为封闭集分类的先前工作不同，ARMOR 执行开放式的迭代精炼。其基线包括开源 VLM（**Qwen2.5-VL**（Bai et al., 2025）、**Cosmos-Reasoning**（Azzolini et al., 2025）、**LLaVA-NeXT**（Zhang et al., 2024a））、商用闭源 VLM（**Claude-3.7**，采用少样本提示）以及仅使用稠密标签的标准监督微调基线（**SFT-D**、**SFT-S+D**）。

- **关键技术特征**：ARMOR 采用独立的分类头（用于故障检测）和语言解码头（用于推理生成），无需事后正则匹配即可直接输出结果。训练分为离线模仿（利用专家标签温启动并学习跨任务一致性）和在线精炼（利用策略自身生成轨迹进行多轮展开优化）两个阶段。推理时，模型生成多条精炼轨迹，以检测熵与推理熵的加权和作为置信度指标选择最优轨迹，并在熵不再下降时终止。

- **主要结果**：在 RLBench、Sparrow、Maniskill 和 ARMBench 四个数据集上，ARMOR 在所有评估设置下均达到最高的故障检测准确率和推理质量。相比最强监督微调基线 SFT-S+D，ARMOR 在 RLBench 上的检测准确率从 0.640 提升至 **0.917**（+27.7%），LLM Fuzzy 推理分数从 0.550 提升至 **0.718**（+16.8%）；相比闭源 Claude-3.7，检测提升达 +35.6%。在跨域迁移设置中，仅依靠目标域少量稠密标签并结合源域稀疏标签，ARMOR 即可实现大幅性能提升（Maniskill R→M 检测达 0.990，ARMBench S→A 推理提升 +52.1%）。

- **消融发现**：多任务预测头、离线专家条件化、在线模仿和推理精炼的组合是实现最佳性能的关键。若仅保留精炼而移除离线专家条件化和在线模仿，检测准确率急剧下降至 0.803，表明多组件协同不可或缺。

- **局限与展望**：推理偶尔漂移到语义相关但错误的原因（如将物品损坏误判为碰撞）；极端稀疏数据比例（30:1）下推理质量显著下降；精炼轮次增多带来额外计算开销。未来方向包括引入结构化故障属性作为中间监督、融合多模态传感信号、以及探索可学习的停止策略以优化效率与精度的权衡。

## 背景与动机

机器人系统的自主故障检测与推理是实现可靠自动化操作的关键能力。在实际部署中，机器人不仅需要判断任务是否失败（检测），更需要以自然语言解释失败的原因（推理），从而为后续的恢复策略或人工干预提供可操作的语义信息。然而，训练同时具备精确检测与细粒度推理能力的模型面临一个核心瓶颈：**数据异质性**。

具体而言，大规模的二值故障标签（成功/失败）可以从系统日志或自动评估脚本中低成本获取，构成丰富的**稀疏监督**；但高质量的、自由形式的自然语言推理标注则需要人类专家对每个故障场景进行细致描述，成本高昂且难以规模化，形成稀缺的**稠密监督**。现有方法在处理这一异质数据格局时存在明显缺口：

- **封闭集分类方法**将故障推理简化为对预定义故障模式（如“抓取不稳定”“物体滑落”）的分类，虽然可以利用稀疏标签进行训练，但无法捕捉真实世界中超出固定类别的多样化故障表现，丧失了推理的开放性和表达力。
- **端到端视觉语言模型（VLM）方法**虽然具备开放集推理的潜力，但通常依赖单一的语言建模头同时输出检测和推理结果，需要通过正则表达式等后处理手段从自由文本中提取二值决策。这种方式不仅对输出格式高度敏感，容易因格式偏差导致检测失败，更关键的是要求全套稠密标注进行监督微调，无法有效利用大规模稀疏标签。

因此，核心挑战在于：**如何在异构监督（大规模稀疏标签 + 小规模稠密标签）下，联合实现精确的二值故障检测与开放式的、人类可读的故障推理？**

ARMOR（Adaptive Round-based Multi-task mOdel for Robotic failure detection and reasoning）正是针对上述缺口提出的解决方案。其核心洞察是：将故障检测和推理建模为一个**多轮序列精炼过程**，通过多任务预测头将检测与推理解耦，同时利用离线模仿与在线精炼在异构数据上迭代改进预测。这一设计使得模型能够在多轮交互中逐步减少检测与推理之间的不一致性，提升推理质量，从而兼顾检测精度与开放式推理的表达力。

## 核心创新

ARMOR的核心创新在于将机器人故障检测与推理重新建模为一个**多轮、多任务的序列精炼问题**，并通过三个相互协同的机制设计，解决了异构监督下联合精确检测与开放集推理的瓶颈。

### 1. 多任务预测头解耦检测与推理

传统方法依赖单一语言建模头，以自由文本形式同时输出检测结果和推理内容，随后通过正则表达式事后抽取二值标签。这种设计将检测和推理耦合在同一个生成过程中，不仅引入了解析脆弱性，还限制了模型在两类任务上的专业化能力。

ARMOR引入了**独立的分类头**和**原始语言解码头**（Figure 4）。分类头从LM解码器中间层的前四层进行平均池化，通过可学习的[CLS] token进行交叉注意力后经MLP输出二值故障检测logits；语言解码头则根据任务特定提示直接生成推理文本。这一架构变更使得检测任务可以充分利用分类损失的判别性，推理任务则保留开放集语言生成的灵活性，两者各自由专用提示驱动，无需任何后处理或正则匹配（Section 4.1, Appendix B.4）。

### 2. 离线模仿与在线精炼的两阶段训练

标准监督微调将所有数据统一作为下一token预测任务，无法有效利用大规模稀疏标签（仅有二值成功/失败标注）与小规模稠密标签（含细粒度推理文本）之间的异构性。

ARMOR的训练算法（Algorithm 1）包含两个阶段：

- **离线模仿阶段**：首先在稀疏和稠密数据上温启动模型，使其学会基础检测和推理；随后利用稠密数据提供专家条件化过渡——将真实标签作为上一轮预测注入当前轮次提示，训练模型在给定正确先验的条件下保持跨轮次一致性（Section 4.2）。
- **在线精炼阶段**：针对离线模仿中专家演示与模型自身行为之间的分布不匹配，利用策略自身进行多轮展开，以二元交叉熵（检测）和下一token预测（推理）分别优化。稀疏数据仅监督检测，稠密数据同时监督两者，从而在异构标签下最大化信息利用（Section 4.2, Equation 1）。

消融实验（Table 2）严格验证了这一设计：在多任务预测基础上逐步叠加离线专家条件化、在线模仿和推理精炼，检测/推理从0.897/0.460提升至0.917/0.718。仅保留推理精炼而移除离线专家条件化和在线模仿时，检测急剧下降至0.803，推理仅略微提升至0.488，表明多组件协同是关键。

### 3. 基于熵的自置信度多轮精炼推理

现有方法采用单次前向推理直接产生最终输出，无法利用模型自身的不确定性信号来迭代改进预测。

ARMOR在推理时生成多条精炼轨迹，每轮基于前一轮的检测和推理输出构建条件化提示，计算检测熵与推理熵的加权组合熵分数 $\mathcal{C}^{(m)} = \mathcal{H}_{\mathrm{det}}^{(m)} + \lambda \mathcal{H}_{\mathrm{reason}}^{(m)}$，以最低熵选择最自信的轨迹，并在熵不再下降时终止（Algorithm 2, Section 4.3）。这一机制使得模型能够在多轮中持续降低不确定性：第一轮精炼即带来40%以上的推理相对提升（Table 3），熵值随轮次稳步下降（Figure 3a），且方差逐渐减小，表明预测趋于稳定一致。

### 4. 创新点的协同效应

上述三个创新点并非孤立生效，而是形成了完整的闭环：多任务头提供了检测与推理的解耦基础，离线-在线训练赋予了模型在异构标签下自我纠错的能力，熵驱动精炼则在推理时将这种能力转化为可观测的性能增益。三者缺一不可，共同构成了ARMOR相较于现有监督微调基线和闭源VLM的核心优势。

## 整体框架

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_jr9hGWQioP/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ARMOR. (a) Our failure data consist of heterogeneous supervision, with large-scale binary detection labels and scarce free-form reasoning labels. (b) A vision-language model (VLM) with multitask heads jointly predicts detection l via a classification head and reasoning e via a language decoder, trained with binary cross-entropy (BCE) and next-token prediction (NTP) losses. (c) We fine-tune the VLM with both offline imitation and online refinement: the model conditions on dataset labels ( l , e ) or its prior predictions (ˆl, eˆ) as well as auxiliary prompts p to generate a new round of outputs. In online refinement, this process is repeated T times. The model’s predictions (deno...*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_jr9hGWQioP/figures/012_Figure_4.jpg]]
*Figure 4: ARMOR model architecture. We select the intermediate layer representation from the LM decoder of Qwen2.5-VL (Bai et al., 2025) and attach a classification head for detection, while using the original LM decoder for reasoning. Conditioning prompts describe the previous outputs for each task, enabling iterative multi-task refinement*

ARMOR将机器人故障检测与推理建模为一个**多轮多任务自精炼过程**，其核心设计围绕三个关键问题展开：如何在异构监督信号下同时完成精确的二值检测与开放集推理，如何让模型在迭代中持续修正自身预测，以及如何在推理时以自置信度引导轨迹选择。

### 数据流与异构监督

系统的输入为一段机器人操作视频 $x$。训练数据由两类异构标注组成（Figure 2a）：
- **稀疏数据集** $D_{\mathrm{sparse}} = \{(x_i, l_i)\}$：仅包含二值成功/失败标签 $l_i$，可从系统日志自动获取，规模大但信息密度低。
- **稠密数据集** $D_{\mathrm{dense}} = \{(x_i, l_i, e_i)\}$：额外包含细粒度的自然语言故障推理 $e_i$，标注成本高，数量稀缺。

这种异构性构成了方法设计的根本约束：检测任务可受益于大规模稀疏数据，而推理任务必须从小规模稠密数据中学习泛化能力。

### 模型架构：多任务预测头解耦

ARMOR以Qwen2.5-VL（Bai et al., 2025）为骨干，在其视觉编码器与语言模型解码器之上引入**任务专用预测头**，将检测与推理在输出层解耦（Figure 2b, Figure 4）：

- **检测分类头**：从LM解码器的中间层（前四层）提取隐表示，经平均池化后通过可学习的[CLS] token进行交叉注意力，再由MLP输出二值故障检测logits。该设计避免了传统方法中依赖正则表达式从自由文本中抽取二值标签的脆弱性。
- **推理生成头**：复用原始LM解码器，根据任务特定提示直接生成故障推理文本，无需任何后处理或格式匹配。

两个预测头共享底层视觉编码器和LM解码器的主干网络，但在任务层面独立优化。每轮迭代中，模型接收上一轮的检测结果 $l^{t-1}$ 和推理文本 $e^{t-1}$，以条件提示的形式注入当前轮次的输入，形成跨轮次的信息依赖。

### 训练流程：离线模仿与在线精炼

训练分为两个阶段（Algorithm 1）：

**阶段一：离线模仿**。首先进行温启动（warm-start），模型在不依赖任何先验轮次输出的条件下，直接从视频预测检测和推理。随后利用稠密数据提供专家条件转移：给定真实的上一轮标签，训练模型学习在已知正确先验时如何生成一致的下一轮预测。稀疏数据仅监督检测头（二元交叉熵损失），稠密数据同时监督检测头和推理头（下一token预测损失）。

**阶段二：在线精炼**。为解决专家演示与模型自身行为分布之间的不匹配，ARMOR进一步使用策略自身的多轮展开进行在线微调。模型在当前策略下生成多条精炼轨迹，以BCE和NTP损失分别优化检测和推理输出。这一阶段使模型能够适应自身的误差模式，学习从自身错误中恢复。

### 推理流程：基于熵的自置信度精炼

推理时，ARMOR执行多轮自精炼循环（Algorithm 2）。每轮生成 $M$ 条随机轨迹，每条轨迹包含检测logits和推理文本。对于每条轨迹 $m$，计算组合熵分数：

$$\mathcal{C}^{(m)} = \mathcal{H}_{\mathrm{det}}^{(m)} + \lambda \mathcal{H}_{\mathrm{reason}}^{(m)}$$

其中 $\mathcal{H}_{\mathrm{det}}$ 为检测logits的熵，$\mathcal{H}_{\mathrm{reason}}$ 为推理文本的序列级熵，$\lambda$ 为加权系数。每轮选择组合熵最低的轨迹作为该轮输出，并以其检测和推理结果条件化下一轮的提示。精炼在最佳轨迹的熵分数不再下降（低于容忍度 $\epsilon$）时终止，最终输出取自熵最低的轨迹。

这一设计使模型能够在多轮中逐步降低不确定性：检测头提供相对可靠的分类信号，推理头据此修正语义细节；同时，推理文本中的上下文信息也可反向辅助检测决策的校准。实验表明，第一轮精炼即可带来40%以上的推理质量相对提升，且熵值随轮次持续下降，验证了自置信度引导的有效性。

## 核心模块与公式推导

ARMOR 将故障检测与推理建模为一个多轮多任务精炼过程，其核心架构由三个紧密耦合的模块组成：多任务预测头、两阶段训练算法，以及基于熵的自置信度推理精炼。

### 多任务预测头

传统视觉语言模型（VLM）采用单一语言建模头，同时输出检测结果和推理文本，需要依赖正则表达式事后解析，容易因格式不匹配而失败。ARMOR 将检测与推理解耦为两个独立的预测头（Figure 4, Section 4.1）：

- **检测分类头**：从 Qwen2.5-VL 的 LM 解码器中间层（前四层）提取隐空间表示，经平均池化后，通过可学习的 `[CLS]` token 进行交叉注意力，再经 MLP 输出二值故障检测 logits。该头直接产生分类结果，无需任何后处理或正则匹配。
- **推理生成头**：复用原始 LM 解码头，根据任务特定提示直接生成自然语言故障推理文本。

每轮精炼时，上一轮的检测结果（成功/失败）和推理文本以文本形式注入当前轮次的 Conditioning Prompts 中，形成跨轮次依赖，使模型能够基于先前预测进行迭代修正。

### 两阶段训练算法

ARMOR 的训练目标是在异构监督下最大化期望奖励（Section 4.2, Equation 1）：

$$\max_{\theta} \mathbb{E}_{(x,l)\sim D_{\mathrm{sparse}}} \mathbb{E}_{(l^t,e^t)\sim \pi_{\theta}(\cdot \vert [x,l^{t-1},e^{t-1},p^t])} [\mathbb{1}(l^t=l)] + \mathbb{E}_{(x,l,e)\sim D_{\mathrm{dense}}} \mathbb{E}_{(l^t,e^t)\sim \pi_{\theta}(\cdot \vert [x,l^{t-1},e^{t-1},p^t])} [\mathbb{1}(l^t=l) + \mathbb{1}(e^t=e)]$$

其中 $x$ 为输入视频，$l$ 为二值检测标签，$e$ 为推理文本标签，$p^t$ 为第 $t$ 轮的提示。稀疏数据仅监督检测正确性，稠密数据同时监督检测与推理正确性。训练分为两个阶段（Algorithm 1）：

1. **离线模仿**：先在不依赖先前轮次的条件下温启动模型，使检测头和推理头学习基础预测能力；随后利用稠密数据集提供条件化专家转移，让模型学习在给定先前专家标签的条件下生成下一轮预测，建立跨轮次一致性。
2. **在线精炼**：为解决专家演示与模型自身行为之间的分布不匹配，利用策略自身进行多轮展开，用二元交叉熵（检测）和下一 token 预测（推理）分别优化，使模型适应自身的误差模式。

### 基于熵的自置信度推理精炼

推理时，ARMOR 生成多条精炼轨迹，每轮计算组合熵分数以选择最自信的轨迹（Section 4.3）：

$$\mathcal{C}^{(m)} = \mathcal{H}_{\mathrm{det}}^{(m)} + \lambda \mathcal{H}_{\mathrm{reason}}^{(m)}$$

其中 $\mathcal{H}_{\mathrm{det}}^{(m)}$ 为第 $m$ 条轨迹的检测熵，$\mathcal{H}_{\mathrm{reason}}^{(m)}$ 为推理熵，$\lambda$ 为加权系数。每轮选择 $\mathcal{C}^{(m)}$ 最低的轨迹作为当前最优，并在熵不再下降时终止精炼。该机制使得模型在多轮中持续降低不确定性，同时提升检测与推理的一致性。

## 实验与分析

### 核心瓶颈与实验动机

机器人故障检测与推理面临一个根本性数据异质性问题：大规模的二值故障标签（成功/失败）可从系统日志自动获取，但细粒度的自然语言推理标注极其昂贵且稀缺。现有方法要么将推理简化为封闭集分类，丧失对真实世界复杂故障的开放描述能力；要么要求全套稠密标注，无法在异构监督下联合精确检测与开放式推理。ARMOR的实验设计正是围绕这一瓶颈展开——验证多任务预测头、离线-在线混合训练以及多轮自精炼能否在稀疏标签（仅监督检测）和少量稠密标签（同时监督检测与推理）的混合数据上，同时提升检测精度与推理质量。

### 主实验结果

**Table 1** 给出了ARMOR与六类基线在四个数据集上的全面对比。基线包括三个开源视觉语言模型（**Qwen2.5-VL**、**Cosmos-Reasoning**、**LLaVA-NeXT**）、商用闭源模型 **Claude-3.7**（少样本提示），以及两种监督微调变体 **SFT-D**（仅用稠密标签）和 **SFT-S+D**（稀疏+稠密标签联合微调）。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_jr9hGWQioP/figures/003_Table_1.jpg]]
*Table 1: Quantitative Results on Failure Detection and Reasoning. Metrics include detection accuracy and reasoning quality (LLM Fuzzy and $\mathsf { R O U G E } _ { L }$ ) . Our method achieves higher performance across different domains, accurately detecting failures and producing high quality reasoning*

在 **RLBench** 上，ARMOR达到 **0.917** 的检测准确率和 **0.718** 的LLM Fuzzy推理分数，分别超出最强基线SFT-S+D **+0.277** 和 **+0.168**，较Claude-3.7的检测优势更是高达 **+0.356**。在 **Sparrow** 数据集上，检测准确率从SFT-S+D的0.620提升至 **0.733**（+0.113），推理LLM Fuzzy从0.381提升至 **0.503**（+0.122）。

跨域迁移场景尤为突出：在 **Maniskill (R→M)** 设置中，ARMOR仅依靠目标域少量稠密标签并结合源域稀疏标签，检测准确率达到 **0.990**，较SFT-D的0.625提升 **+0.365**；在 **ARMBench (S→A)** 设置中，推理LLM Fuzzy从SFT-S+D的0.177跃升至 **0.698**（+0.521），相对提升超过290%。这一结果直接验证了ARMOR在异构监督下跨域泛化的核心能力。

值得注意的是，部分基线（SFT-D、SFT-S+D等）的评估依赖从模型输出的`<answer>`标签中通过正则表达式解析二值决策，解析失败即视为错误。此协议对格式敏感的基线可能造成一定低估，尽管所有测试集已按成功与失败样本等量平衡以缓解该问题。

### 消融实验

**Table 2** 系统解构了ARMOR各组件的贡献。基础配置仅包含多任务预测头（分类头+语言解码头），在RLBench上检测/推理分数分别为0.897/0.460。依次叠加各组件：

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_jr9hGWQioP/figures/004_Table_2.jpg]]
*Table 2: Ablation of ARMOR’s components. Each row shows the impact of different stages on detection accuracy and reasoning quality. ARMOR combines all components to achieve the best overall performance*

- **+Offline Warm-up**：检测提升至0.913，推理提升至0.527
- **+Offline Expert Condition**：检测微降至0.910，推理大幅提升至0.646
- **+Online Imitation**：检测回升至0.913，推理提升至0.693
- **+Refinement（完整ARMOR）**：检测达0.917，推理达0.718

关键消融发现：**仅保留推理精炼而无离线专家条件化和在线模仿**（Refinement Only行），检测急剧下降至 **0.803**，推理仅0.488。这表明多轮精炼本身不足以弥补训练阶段缺失的跨任务一致性学习——离线专家条件化教会模型在给定正确先验时保持预测稳定，在线模仿则让模型适应自身误差模式，二者与精炼形成协同效应。

### 精炼轮次分析

**Table 3** 展示了推理性能随精炼轮次的稳步提升（4个随机种子均值与标准差）：Round 0的LLM Fuzzy为0.475，Round 1跃升至 **0.676**（+42.4%相对提升），Round 2达0.703（+4.0%），Round 3达 **0.717**（+2.0%）。标准差从0.016持续收窄至0.002，表明精炼不仅提升质量，还显著增强了预测一致性。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_jr9hGWQioP/figures/008_Table_3.jpg]]
*Table 3: ARMOR’s reasoning performance across refinement rounds. Mean and std are reported across 4 seeds. Each round shows improvements with decreasing variance, demonstrating consistent gains*

**Figure 3a** 从熵的角度揭示了精炼机制：检测熵和推理熵在Round 0→1急剧下降，随后趋于平稳，与性能提升趋势高度吻合。这验证了基于组合熵分数 $\mathcal{C}^{(m)} = \mathcal{H}_{\mathrm{det}}^{(m)} + \lambda \mathcal{H}_{\mathrm{reason}}^{(m)}$ 的轨迹选择策略能有效识别并保留置信度更高的预测。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_jr9hGWQioP/figures/007_Figure_3.jpg]]
*Figure 3: Prompt: In the video, the robot is attempting to transport an object from one bin to another. Did the robot successfully transport the object? (b) Example of ARMOR’s multi-round refinement process. Figure 3: Refinement analysis in ARMOR. (a) Effect of refinement rounds on entropy and performance: detection and reasoning entropy decrease steadily across rounds, while combined plots show that refinement improves both detection accuracy and reasoning quality (values computed over 300 test datapoints). (b) Example of ARMOR’s multi-round refinement process, where predictions are iteratively updated to improve the quality and consistency between detection and reasoning outputs*

**Figure 3b** 的定性案例展示了精炼的实际效果：初始轮次中检测与推理可能不一致（如检测为失败但推理描述模糊），经过多轮迭代后，检测结果趋于稳定，推理文本逐步修正为与视觉证据一致且语义精确的描述。论文观察到推理结果倾向于根据检测结果进行修正，因为检测拥有更充足的训练数据，通常更为可靠。

### 推理成本

**Table 4** 记录了精炼的计算开销。以Round 0为基准（7.95秒，3.48 GB/GPU），每增加一轮约增加1秒推理时延和少量显存增长（Round 3为10.95秒，6.31 GB/GPU）。这一开销增幅在多数离线或准实时故障分析场景中是可接受的，但对于毫秒级实时控制回路可能构成约束。

### 数据不平衡鲁棒性与模型扩展性

**Table 7** 分析了稀疏/稠密数据比例对性能的影响。在主论文采用的5:1比例下，检测/推理为0.725/0.698；当比例升至10:1时，检测降至0.640，推理降至0.609，仍保持合理水平；但升至30:1时推理骤降至0.427，表明方法对极端稀疏标注仍存在一定依赖。**Table 8** 展示了ARMOR从7B扩展至32B参数后在Sparrow上的表现：检测从0.733提升至 **0.765**，推理从0.503提升至 **0.562**，表现出良好的模型规模扩展性。

### 失败模式

**Figure 6** 展示了一个典型失败案例：在ARMBench运输任务中，真值失败原因是物品损坏（书皮脱落），但模型推理漂移为碰撞或放置错误。这类语义相关但因果错误的推理漂移，暴露了当前方法缺乏结构化故障属性约束的局限——模型虽能识别异常发生，但在归因时可能混淆视觉上相似但因果不同的故障模式。

### 实验结论

ARMOR在异构监督下实现了检测精度与开放式推理质量的联合最优，多任务预测头解耦、离线-在线混合训练和基于熵的自精炼三者缺一不可。第一轮精炼即可带来超过40%的推理相对提升，且计算开销可控。跨域迁移实验证明了该方法在实际部署中利用少量目标域标注快速适应的潜力。主要局限在于极端稀疏标注下的推理退化，以及缺乏结构化故障属性引导时可能发生的语义漂移。

## 方法谱系与知识库定位

### 1. 与先前工作的关系

ARMOR 在机器人故障检测与推理的交叉点上，与三类工作形成对比或继承关系。

**vs. 封闭集故障分类方法。** 早期工作将故障推理简化为对预定义故障模式（如“溢出”“不稳定抓取”）的分类，本质上是一个闭集判别问题。这类方法依赖人工枚举故障类型，无法覆盖开放世界中未见的故障模式，且不提供自然语言解释。ARMOR 将检测建模为二值分类、推理建模为开放集语言生成，通过多轮精炼在保持检测精度的同时输出细粒度、人类可读的推理文本，突破了封闭集假设。

**vs. 视觉语言模型（VLM）基线。** 论文对比了三种开源 VLM——**Qwen2.5-VL**（Bai et al., 2025）、**Cosmos-Reasoning**（Azzolini et al., 2025）和**LLaVA-NeXT**（Zhang et al., 2024a）——以及商用闭源模型**Claude-3.7**（少样本提示）。这些基线均采用单一语言建模头输出自由形式文本，依赖正则表达式从 `<answer>` 标签中事后抽取二值检测结果。ARMOR 与之的核心差异在于：（1）引入独立的分类头直接输出检测 logits，消除了解析失败导致的系统性误差；（2）通过多轮自精炼迭代修正不一致预测，而基线仅执行单次前向推理。实验表明，ARMOR 在 RLBench 上的检测准确率（0.917）显著高于 SFT-S+D（0.640）和 Claude-3.7（0.561），推理 LLM Fuzzy 分数（0.718）亦大幅领先（Table 1）。

**vs. 标准监督微调（SFT）。** SFT-D（仅稠密标签微调）和 SFT-S+D（稀疏+稠密标签联合微调）代表了将异构数据统一为下一 token 预测任务的朴素方案。ARMOR 在此基础上引入了三个关键改进：多任务预测头解耦检测与推理的优化目标；离线专家条件化阶段让模型学习在给定正确先验下生成一致的多轮预测；在线精炼阶段利用策略自身展开，使模型适应自身的误差分布。消融实验证实，缺少精炼模块会使检测准确率从 0.917 骤降至 0.803（Table 2），验证了多组件协同的必要性。

**vs. 在线模仿学习（DAgger 范式）。** ARMOR 的在线精炼阶段借鉴了 DAgger（Ross et al., 2011b）的思想——用策略自身的 rollout 替代专家演示来缓解分布偏移。但 ARMOR 将其拓展到多任务、多轮场景：每轮同时监督检测（BCE 损失）和推理（下一 token 预测损失），并在推理时通过组合熵分数选择最自信的轨迹，而非简单的多数投票或单轨迹输出。

### 2. 适用边界与局限

**数据异质性的依赖边界。** ARMOR 的核心假设是存在大规模稀疏二值标签（可从系统日志自动获取）和少量稠密推理标注。当稀疏/稠密数据比例在 10 倍以内时，方法保持合理的检测（0.640）和推理（0.609）性能；但当比例升至 30 倍时，推理质量显著下降至 0.427（Table 7），表明方法对有限的稠密标注仍有一定依赖。在完全没有稠密标注的纯稀疏域，ARMOR 无法赋予模型开放集推理能力，这是一个明确的适用边界。

**推理漂移与语义混淆。** 定性分析揭示，ARMOR 的推理偶尔会漂移到语义相关但错误的原因。例如在 ARMBench 运输任务中，真值故障为物品损坏（书皮脱落），但模型推理为碰撞或放置错误（Figure 6）。这种漂移可能源于模型在开放集生成中缺乏结构化故障属性（如碰撞、损坏、抓取失败）的显式约束，推理过程过度依赖视觉表象而未能追溯到根本原因。

**计算开销与实时性。** 多轮精炼带来额外的计算成本：每增加一轮精炼，推理时延约增加 1 秒，GPU 内存从 3.48 GB 增长至 6.31 GB（Table 4）。虽然增幅有限，但对于需要毫秒级响应的实时控制回路或资源极度受限的边缘部署场景，可能构成挑战。当前基于熵阈值的停止策略（熵不再下降即终止）是启发式的，尚未针对效率-精度帕累托最优进行显式优化。

**评估协议的公平性边界。** 基线方法依赖正则表达式从 `<answer>` 标签解析二值检测结果，若模型未遵循输出格式则判定为错误。尽管测试集按成功/失败样本等量平衡以缓解此问题，但格式敏感性仍可能轻微低估部分基线的真实检测能力。这一评估偏差主要影响与 SFT 基线的比较结论，对 ARMOR 的优势幅度需保持审慎解读。

### 3. 开放问题

1. **结构化故障属性的引入。** 当前推理是完全开放集的语言生成，缺乏对故障类型（如碰撞、放置错误、损坏）的中间约束。能否引入结构化故障属性作为辅助监督信号或中间奖励，在精炼过程中引导推理向更可靠的方向收敛？

2. **多模态信号的融合。** ARMOR 仅利用视觉输入（视频帧）。实际机器人系统通常还配备力传感器、本体制感、触觉等多模态信号。如何将这些异构信号整合进同一多轮精炼框架，以提升故障检测的鲁棒性和推理的物理一致性？

3. **超越人工标注的推理能力。** 当前在线模仿仍以人工稠密标注为监督上限。能否将在线精炼与偏好学习或直接奖励优化（如 RLHF）结合，使模型在自我博弈中产生超越人工标注水平的推理策略？

4. **可学习的停止策略。** 当前推理终止依赖启发式的熵阈值（组合熵分数不再下降）。这一策略能否被可学习的停止模块替代，以在准确性与推理成本之间获得更优的权衡？例如，训练一个轻量级价值网络预测继续精炼的边际收益。

5. **纯稀疏域的开放集推理。** 在完全没有稠密标注的领域，ARMOR 当前无法赋予模型推理能力。能否通过无监督或自监督手段（如利用 VLM 的预训练知识进行零样本推理，再通过检测一致性进行筛选）在纯稀疏域中引导出初步的开放集推理，并随着稠密数据的逐步积累持续改进？

6. **跨任务泛化。** ARMOR 当前聚焦于故障检测与推理。其多轮精炼框架是否可拓展到其他协同任务，如安全违规预测、恢复策略生成，甚至更广泛的多模态推理链场景？这需要验证方法在任务类型和输出空间发生显著变化时的结构可迁移性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Self_Refining_Vision_Language_Model_for_Robotic_Failure_Detection_and_Reasoning.pdf]]

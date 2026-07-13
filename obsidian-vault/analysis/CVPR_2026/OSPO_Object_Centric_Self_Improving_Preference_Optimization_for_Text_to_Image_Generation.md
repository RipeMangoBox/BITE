---
title: "OSPO: Object-Centric Self-Improving Preference Optimization for Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OSPO_Object_Centric_Self_Improving_Preference_Optimization_for_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- OOCSIPO
- OSPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 对象中心的自改进偏好优化框架（OSPO），通过自我生成对象中心偏好数据、利用内部注意力权重构建对象掩码，并应用对象加权损失，引导模型聚焦于对象相关视觉标记。
primary_logic: 现有自改进方法依赖全局语义或Best-of-N采样，缺乏精确的对象级差异信号。OSPO显式构造对象中心偏好对，通过提示扰动与密化确保全局语义一致但对象细节不同，结合分解VQA过滤和对象加权损失，直接强化细粒度对齐。
claims:
- "在T2I-CompBench++上，OSPO在1B和7B尺度上均优于所有自改进基线，并在Complex等类别取得最高分（例如7B: 0.4147）。"
- "在DPGBench上，OSPO在统一MLLMs中取得最佳全局得分（7B: 85.61），并在GenEval上总体得分最高（7B: 0.83）。"
- 消融实验证实对象加权SimPO损失和SFT损失的组合是关键，移除加权或SFT均导致性能下降。
- 过滤和选择策略结合密化显著提升性能，在T2I-Compbench++ attribute上达到0.756，GenEval overall达到0.831。
---

# OSPO: Object-Centric Self-Improving Preference Optimization for Text-to-Image Generation

> [!tip] 核心洞察
> 现有自改进方法依赖全局语义或Best-of-N采样，缺乏精确的对象级差异信号。OSPO显式构造对象中心偏好对，通过提示扰动与密化确保全局语义一致但对象细节不同，结合分解VQA过滤和对象加权损失，直接强化细粒度对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | OSPO: 面向对象中心的自改进偏好优化用于文本到图像生成 |
| 英文题名 | OSPO: Object-Centric Self-Improving Preference Optimization for Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.02015) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OSPO (Object-centric Self-improving Preference Optimization) |
| Dataset | T2I-CompBench++, DPGBench, GenEval |

> [!tip] 效果简介
> - T2I-CompBench++ 上，Complex 1B: 0.3935 / 7B: 0.4147。
> - DPGBench 上，Global 1B: 84.46 / 7B: 85.61。
> - GenEval 上，Overall 1B: 0.76 / 7B: 0.83。

## 概要

### 问题瓶颈

统一多模态大语言模型在文本到图像生成中面临一个关键瓶颈：**难以实现细粒度的对象级对齐**。模型生成的图像经常出现对象幻觉，表现为对象遗漏、扭曲或属性错误。现有自改进方法普遍依赖全局语义信号或Best-of-N采样，忽略对象级语义差异，导致对齐精度不足。

### 核心方法定位

**OSPO**（Object-centric Self-improving Preference Optimization）是一个面向对象中心的自改进偏好优化框架。其核心洞察在于：通过显式构造对象中心偏好对，结合提示扰动与密化确保全局语义一致但对象细节不同，再利用分解VQA过滤和对象加权损失，直接强化细粒度对齐。该方法无需外部分割模型或人工标注，完全依赖模型自身的注意力权重和自评估能力。

在方法谱系中，OSPO区别于以下基线：

- **SILMM**：基于标准SimPO/DPO的自改进偏好优化，缺乏对象级差异信号。
- **SuDer**与**UniRL**：自改进基线，依赖全局语义或Best-of-N采样。
- **T2I-R1**：基于GRPO的强化学习方法，未显式建模对象区域。
- **FocusDiff**：结合SFT和GRPO的精细对齐方法，但未利用内部注意力权重构造对象掩码。

OSPO的关键改动槽位包括：偏好数据构建策略从Best-of-N采样改为提示扰动+密化+分解VQA过滤；偏好优化损失从标准SimPO改为对象加权SimPO损失+SFT损失；对象区域定位从无显式信息改为基于注意力权重的OTSU二值化掩码。

### 主要结果

在T2I-CompBench++上，OSPO在1B和7B尺度上均优于所有自改进基线，并在Complex类别取得最高分（7B: 0.4147）。在DPGBench上，OSPO在统一MLLMs中取得最佳全局得分（7B: 85.61），并在GenEval上总体得分最高（7B: 0.83）。消融实验证实，对象加权SimPO损失和SFT损失的组合是关键，移除任一组件均导致性能下降。过滤和选择策略结合密化显著提升性能，在T2I-Compbench++ attribute上达到0.756，GenEval overall达到0.831。此外，OSPO在达到更高基准性能的同时，比SILMM更省时，展现出优秀的性能-效率权衡。

文本到图像（T2I）生成领域近年来取得了显著进展，但**对象幻觉**（object hallucination）——即生成图像中对象遗漏、扭曲或属性错误——仍是制约其可靠性的核心瓶颈。这一问题在统一多模态大语言模型（MLLM）中尤为突出：尽管统一架构实现了文本与视觉模态的深度融合，其自回归解码机制却难以维持跨模态的细粒度对象级对齐。

现有自改进（self-improving）方法试图通过偏好优化提升生成质量，但其偏好数据构建策略存在根本性局限。主流方法如 **SILMM** 和 **SuDer** 依赖 Best-of-N 采样：随机生成多个候选图像，仅凭全局评分选择最优/最劣样本构成偏好对。这种策略忽略了对象级别的语义差异，导致偏好信号粗糙、噪声高，难以针对具体对象的属性、位置或关系进行精确纠偏。基于强化学习的方法如 **T2I-R1**（GRPO）和 **FocusDiff**（SFT+GRPO）虽引入更精细的优化目标，但同样缺乏显式的对象区域定位机制。

上述缺口指向一个关键瓶颈：**缺乏精确的对象级差异信号**。自改进框架若不能显式构造“全局语义一致但对象细节不同”的偏好对，便无法将优化压力聚焦于真正导致幻觉的视觉标记。OSPO 的动机正是填补这一空白——通过对象中心的自改进偏好优化，将模型注意力引导至对象相关区域，直接强化细粒度对齐，从而系统性地抑制对象幻觉。

## 核心方法与创新机理

OSPO 的核心创新在于**将对象中心的细粒度信号系统性地注入自改进偏好优化的全流程**，从而解决统一多模态大语言模型（MLLM）在文本到图像生成中普遍存在的对象幻觉问题。与现有自改进方法相比，OSPO 在三个关键维度上实现了根本性改变。

### 从 Best-of-N 采样到对象中心偏好数据构造

现有自改进方法（如 **SILMM**、**SuDer**、**UniRL**）普遍依赖 Best-of-N 采样策略：随机生成多个候选图像，然后选取全局评分最高和最低的样本构成偏好对。这种策略存在一个结构性缺陷——**偏好信号来源于全局语义差异，而非对象级的细粒度差异**，导致模型无法精确感知“哪个对象出了错”。

OSPO 用一套完整的**提示扰动-密化-分解VQA过滤**管道替代了 Best-of-N 采样。具体而言：
- **提示扰动**：对每个基础提示施加 Replace、Swap、Drop 三种扰动，生成多个变体；
- **密化**：对原始-扰动提示对进行联合密化，在保持全局语义一致的前提下，放大对象细节的差异；
- **分解VQA过滤与选择**：自生成原子化的视觉问答问题，计算逐对象对齐分数，滤除偏好-空（preference-null）和偏好-错误（preference-false）噪声对，最终选出高质量的训练对。

这一改变从根本上保证了偏好数据的**差异信号集中在对象级别**，而非被全局语义淹没。

### 从无对象感知到注意力驱动的对象掩码

现有基线方法在偏好优化过程中**不利用任何显式的对象区域信息**，损失函数对所有视觉标记一视同仁。OSPO 则从 MLLM 中间层的注意力权重中提取对象掩码——通过 OTSU 二值化直接获得对象区域，无需额外的分割模型。这一设计使得后续的偏好优化能够**精确聚焦于与对象相关的视觉标记**，从而将优化信号从“整张图好不好”收敛到“每个对象对不对”。

### 从标准偏好损失到对象加权SimPO + SFT联合损失

基于上述对象掩码，OSPO 对标准 SimPO 损失进行了关键改造：在标记级奖励上施加空间权重，形成**对象加权 SimPO 损失**：

$$
\mathcal{L}_{\mathrm{Obj-SimPO}} = -\mathbb{E}_{(x,y_w,y_\ell)\sim\mathcal{D}}\Bigg[\log\sigma\Bigg(\frac{w(y_w)}{|y_w|}\log\pi_\theta(y_w\mid x) - \frac{w(y_\ell)}{|y_\ell|}\log\pi_\theta(y_\ell\mid x) - \gamma\Bigg)\Bigg]
$$

同时，OSPO 引入 SFT 损失在偏好图像上强制全局一致性：

$$
\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(x,y_w)\sim\mathcal{D}}\left[\frac{1}{|y_w|}\sum_{t=1}^{|y_w|}\log\pi_\theta\big((y_w)_t\mid x,(y_w)_{<t}\big)\right]
$$

最终训练损失为二者的加权组合（λ=2）：

$$
\mathcal{L}_{\mathrm{OSPO}} = \mathcal{L}_{\mathrm{Obj-SimPO}} + \lambda\mathcal{L}_{\mathrm{SFT}}
$$

消融实验（Table 4）直接验证了这一设计的因果效力：移除对象加权或 SFT 损失均导致性能显著下降，证实**对象加权与全局约束的协同是 OSPO 有效性的关键瓶颈**。

### 创新总结

| 变更维度 | 基线方法 | OSPO |
|---------|---------|------|
| 偏好数据构造 | Best-of-N 采样（全局评分） | 提示扰动 + 密化 + 分解VQA过滤 |
| 对象区域定位 | 无 | 注意力权重提取对象掩码（OTSU） |
| 偏好优化损失 | 标准 SimPO / DPO | 对象加权 SimPO + SFT 联合损失 |

这三项改变的因果链路是：**精确的对象中心偏好数据 → 注意力驱动的对象掩码 → 对象加权的优化信号**。任何一环的缺失都会导致性能退化，消融实验（Table 3, Table 4）为这一因果链提供了高置信度的证据支持。

OSPO 是一个面向统一多模态大语言模型（MLLM）的对象中心自改进偏好优化框架，旨在缓解文本到图像生成中的对象幻觉问题。其核心设计理念是：**通过自生成的对象中心偏好数据，显式构造全局语义一致但对象细节不同的偏好对，并利用对象加权损失引导模型聚焦于对象相关视觉标记**。整个框架分为五个阶段，形成闭环的自改进流程（图2）。

### Pipeline 总览

**阶段一：提示生成（Prompt Generation）**。MLLM 首先生成一组基础文本提示，覆盖四类语义类型：属性（Attribute）、布局（Layout）、非空间关系（Non-spatial Relation）和复杂组合（Complex），以确保训练数据在对象级语义上的多样性。

**阶段二：提示扰动与密化（Prompt Perturbation and Densification）**。对每个基础提示，通过三种策略生成扰动变体——替换（Replace）、交换（Swap）和丢弃（Drop）——从而构造出语义相近但对象细节不同的提示对。随后，原始提示与扰动提示被联合密化（densified），即由 MLLM 为两者添加相同的上下文细节。密化的作用在于增强全局语义一致性，同时保留对象级的细粒度差异，为后续生成具有可比性的图像对奠定基础。

**阶段三：图像与对象掩码生成（Image and Object Mask Generation）**。从密化后的提示对出发，MLLM 生成候选的偏好图像（preferred）和非偏好图像（non-preferred）。同时，利用模型中间层的注意力权重，通过 OTSU 二值化提取对象空间掩码，无需额外引入分割模型，保持了计算效率。

**阶段四：基于 VQA 的偏好对构建（VQA-based Preference Pair Construction）**。MLLM 自生成分解式的原子 VQA 问题，对每张候选图像计算对齐分数 $S(y) = \frac{1}{K} \sum_{k=1}^{K} s_k(y)$，其中 $s_k(y) = p(\text{yes} \mid y, q_k) - p(\text{no} \mid y, q_k)$。基于每问题分数和聚合分数，过滤掉偏好-空（preference-null）和偏好-错误（preference-false）的噪声对，最终选择最优的训练图像对。

**阶段五：偏好优化（Preference Optimization）**。使用对象加权 SimPO 损失与 SFT 损失联合微调 MLLM。最终损失为 $\mathcal{L}_{\mathrm{OSPO}} = \mathcal{L}_{\mathrm{Obj-SimPO}} + \lambda \mathcal{L}_{\mathrm{SFT}}$（$\lambda=2$），其中对象加权 SimPO 损失通过空间权重 $w(y)$ 放大对象相关视觉标记的梯度信号，SFT 损失则在偏好图像上强化全局一致性。

### 关键设计决策与模块关系

整个 pipeline 的核心因果机制在于**偏好数据的质量决定了自改进的上限**。阶段二的扰动与密化保证了偏好对之间的全局语义可控，避免了 Best-of-N 采样中常见的随机性噪声；阶段四的分解 VQA 过滤则进一步剔除不可靠的监督信号。这两者共同为阶段五的对象加权损失提供了高质量的对象级差异信号。消融实验证实，密化与过滤/选择策略的组合在 T2I-CompBench++ attribute 上达到 0.756，在 GenEval overall 上达到 0.831，显著优于单独使用任一组件的配置（Table 3）。同时，完整 OSPO 损失（标准 SimPO + 对象加权 SimPO + SFT）在 GenEval position 上取得 0.828 的最优成绩，移除对象加权或 SFT 均导致性能下降（Table 4）。

OSPO 框架围绕“对象中心的自改进偏好优化”这一核心思想，构建了五个协同工作的关键模块。以下逐一解析各模块的设计动机、操作机制及其对应的核心公式。

### 提示生成与扰动密化

**动机**：现有自改进方法依赖 Best-of-N 采样，缺乏精确的对象级差异信号。OSPO 通过显式构造语义一致但对象细节不同的提示对，为后续偏好学习提供高质量监督。

**机制**：首先生成覆盖属性、布局、非空间关系、复杂组合四类语义的基础文本提示。随后对每个基础提示施加三种扰动策略——**Replace**（替换对象名词）、**Swap**（交换对象位置）、**Drop**（删除对象名词）——生成多个扰动变体。为强化全局语义一致性而保留细粒度差异，每个原始-扰动提示对经由 MLLM 进行**联合密化**（joint densification），添加上下文细节。

### 图像与对象掩码生成

**动机**：偏好优化需要定位图像中对象相关的视觉标记，但引入外部分割模型会带来额外计算开销。OSPO 利用模型自身的内部表示实现高效的对象区域定位。

**机制**：从密化提示对生成候选图像对后，提取模型中间层的注意力权重。对注意力图应用 OTSU 二值化，直接获得对象空间掩码，无需额外的分割模型。该掩码后续用于对视觉标记施加空间权重。

### 基于 VQA 的偏好对构造

**动机**：直接使用生成图像对进行偏好优化会引入噪声监督——偏好-空（preference-null）和偏好-错误（preference-false）图像对会误导训练。需要一种自评估机制来过滤噪声并选择最优训练对。

**机制**：MLLM 为每个图像自生成 K 个原子分解 VQA 问题 $\{q_k\}_{k=1}^K$，每个问题针对提示中的特定对象或属性。对于图像 $y$ 和问题 $q_k$，计算单问题对齐分数：

$$s_k(y) = p(\text{yes} \mid y, q_k) - p(\text{no} \mid y, q_k)$$

即模型对“是”与“否”回答的概率差值。汇总 K 个问题的分数得到整体对齐分数：

$$S(y) = \frac{1}{K} \sum_{k=1}^{K} s_k(y)$$

利用 $s_k$ 和 $S$ 过滤掉偏好-空对（两幅图像得分均低）和偏好-错误对（非偏好图像得分高于偏好图像），最终从候选池中选择得分差距最大的图像对作为训练样本。

### 对象加权偏好优化

**动机**：标准 SimPO 或 DPO 损失对所有视觉标记一视同仁，而对象相关的细粒度对齐信号被背景标记稀释。需要通过空间加权将优化焦点集中于对象区域。

**机制**：在标准 SimPO 损失中引入对象掩码导出的空间权重 $w(y)$，得到**对象加权 SimPO 损失**：

$$\mathcal{L}_{\mathrm{Obj-SimPO}} = -\mathbb{E}_{(x,y_w,y_\ell)\sim\mathcal{D}}\left[\log\sigma\left(\frac{w(y_w)}{|y_w|}\log\pi_\theta(y_w\mid x) - \frac{w(y_\ell)}{|y_\ell|}\log\pi_\theta(y_\ell\mid x) - \gamma\right)\right]$$

其中 $w(y)$ 为对象掩码在视觉标记上的空间权重，$|y|$ 为序列长度，$\gamma$ 为 margin 超参数。该损失使模型在偏好图像的对象区域获得更高奖励，在非偏好图像的对象区域获得更低奖励。

同时引入 **SFT 损失**在偏好图像上强制全局一致性：

$$\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(x,y_w)\sim\mathcal{D}}\left[\frac{1}{|y_w|}\sum_{t=1}^{|y_w|}\log\pi_\theta\big((y_w)_t\mid x,(y_w)_{<t}\big)\right]$$

最终 **OSPO 损失**为二者的加权组合（$\lambda=2$）：

$$\mathcal{L}_{\mathrm{OSPO}} = \mathcal{L}_{\mathrm{Obj-SimPO}} + \lambda\mathcal{L}_{\mathrm{SFT}}$$

消融实验证实，对象加权 SimPO 与 SFT 损失的组合是关键——移除任一项均导致 T2I-CompBench++ 和 GenEval 上的性能下降（Table 4）。

## 实验与关键发现

OSPO 在三个具有代表性的文本到图像（T2I）生成基准上接受了系统评估：T2I-CompBench++（细粒度组合对齐）、DPGBench（密集提示图对齐）和 GenEval（对象生成与属性绑定）。实验以 Janus-Pro-1B 和 Janus-Pro-7B 作为统一多模态大语言模型（MLLM）骨干，训练数据集由 20,000 条涵盖属性、布局、非空间关系和复杂组合四类语义的文本提示构成。

### 主要定量结果

在 T2I-CompBench++ 上，OSPO 在 1B 和 7B 两个尺度下均显著超越所有自改进基线方法。尤其在最具挑战性的 Complex 子类别上，OSPO 取得了最高分：1B 达到 0.3935，7B 达到 0.4147（Table 1）。这一结果直接验证了对象中心偏好数据对复杂场景下细粒度对齐的有效性。

![[assets/figures/papers/paper_list_l2193_https_arxiv_org_abs_2506_02015/figures/003_Table_1.jpg]]
*Table 1: Comparison on T2I-CompBench++ [15]. ↑ indicates higher is better, with bold highlighting the best score and underline indicating the second best among the unified MLLMs*

在 DPGBench 上，OSPO 在统一 MLLM 中取得最佳全局得分：1B 为 84.46，7B 为 85.61（Table 2）。与此同时，在 GenEval 上，OSPO 的总体得分同样位居榜首：1B 达到 0.76，7B 达到 0.83（Table 2）。跨基准的一致性优势表明，OSPO 并非对特定评测指标过拟合，而是从机制层面缓解了对象幻觉问题。

![[assets/figures/papers/paper_list_l2193_https_arxiv_org_abs_2506_02015/figures/004_Table_2.jpg]]
*Table 2: Comparison on DPGBench [13] and GenEval [9]. ↑ indicates higher is better, with bold indicating the best score and underline indicating the second best among the unified MLLMs*

### 消融实验

#### 过滤与选择策略及提示密化

Table 3 展示了过滤与选择策略以及提示密化的消融结果。在 T2I-CompBench++ 的 attribute 子类上，将密化与过滤/选择策略结合使用取得了 0.756 的最高分；在 GenEval 的 overall 指标上，同样组合取得了 0.831 的最高分。单独移除任一组件均导致性能明显下降，证实了两者之间存在协同效应：密化增强了全局语义一致性，而分解 VQA 过滤与选择则精准剔除了噪声偏好对，使训练信号聚焦于对象级差异。

![[assets/figures/papers/paper_list_l2193_https_arxiv_org_abs_2506_02015/figures/010_Table_3.jpg]]
*Table 3: Effect of filtering and selection strategy in two different settings (with and without densification) construction stage on T2I-Compbench++ (attribute) and GenEval (overall) scores. Higher is better for all benchmarks*

#### 损失函数组件

Table 4 对损失函数各组件进行了消融。完整 OSPO 损失（标准 SimPO + 对象加权 SimPO + SFT，λ=2）在 GenEval 的 position 子类上取得了 0.828 的最优成绩。移除对象加权 SimPO 或 SFT 损失均导致性能下降，证实了对象加权 SimPO 损失与 SFT 损失的组合是关键设计——前者通过空间注意力权重将优化重心导向对象相关视觉标记，后者则强制偏好图像上的全局一致性。

![[assets/figures/papers/paper_list_l2193_https_arxiv_org_abs_2506_02015/figures/009_Table_4.jpg]]
*Table 4: Ablation study on loss components with T2I-Compbench++ (attribute, layout) and GenEval (overall, position) scores. Higher is better for all benchmarks*

### 性能-效率权衡

Figure 6 对比了不同偏好优化框架的性能-效率权衡。OSPO 在 T2I-CompBench++ 的 attribute 得分和 GenEval 的 overall 得分上均优于 SILMM 等基线，同时执行成本更低。这一优势源于 OSPO 利用内部注意力权重提取对象掩码，无需额外分割模型，且自生成偏好数据的过程天然支持计算可扩展性——数据量可随可用算力线性增长。

![[assets/figures/papers/paper_list_l2193_https_arxiv_org_abs_2506_02015/figures/011_Figure_6.jpg]]
*Figure 6: Performance–Efficiency trade-off across preference optimization frameworks for T2I generation. (Left) Comparison of T2I-CompBench++ (attribute) scores against execution cost. (Right) Comparison of GenEval (overall) scores against execution cost. Higher is better for all benchmarks*

![[assets/figures/papers/paper_list_l2193_https_arxiv_org_abs_2506_02015/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative examples from Janus-Pro-7B + OSPO on T2I-CompBench++, GenEval, and DPGBench prompts*

## 定位与知识库关联

### 1. 与现有自改进方法的对比

OSPO 的核心定位是**面向对象中心的细粒度自改进偏好优化**，与传统自改进方法存在三个关键差异。

**偏好数据构建策略的范式转换。** 现有自改进基线普遍采用 Best-of-N 采样策略（如 **SILMM** 、**SuDer** 、**UniRL** ），即从同一提示随机生成多个候选图像，选择评分最高和最低的作为偏好对。这种策略的瓶颈在于：全局语义差异与对象级细节差异高度耦合，模型无法精确感知哪些视觉标记需要强化。OSPO 则通过**提示扰动（Replace/Swap/Drop）+ 密化**主动构造偏好对：扰动操作确保全局语义大致一致但对象细节不同，密化进一步压缩全局语义差异，使偏好信号集中于对象级对齐。Figure 4 的类别对比证实，OSPO 生成的偏好-空图像对在各类别下均显著优于 Best-of-N 基线。

**对象级信号的显式注入。** 现有方法（包括 **T2I-R1** 的 GRPO 强化学习和 **FocusDiff** 的 SFT+GRPO 组合）均未利用对象区域的空间信息。OSPO 从中间层注意力权重提取对象掩码（OTSU 二值化），无需额外分割模型，并将掩码作为空间权重注入 SimPO 损失，使梯度集中流向对象相关视觉标记。这是方法谱系中首次将**自监督对象定位**与**偏好优化**耦合的尝试。

**损失函数的多目标设计。** 标准 SimPO 或 DPO 损失仅优化偏好排序，缺乏对全局一致性的显式约束。OSPO 引入 $ \mathcal{L}_{\text{OSPO}} = \mathcal{L}_{\text{Obj-SimPO}} + \lambda \mathcal{L}_{\text{SFT}} $ 的联合损失，其中 SFT 损失在偏好图像上强制全局一致性（$ \lambda=2 $），对象加权 SimPO 损失负责细粒度对齐。Table 4 的消融证实，移除对象加权或 SFT 损失均导致显著性能下降，验证了双目标设计的必要性。

### 2. 方法适用边界

**模型架构依赖。** OSPO 的注意力掩码提取依赖统一多模态大语言模型（MLLM）的中间层注意力权重，当前实验仅在 Janus-Pro-1B 和 Janus-Pro-7B 上验证。对于基于扩散模型的 T2I 生成器（如 Stable Diffusion 系列），需重新设计对象区域定位机制，直接迁移存在适配成本。

**提示扰动策略的语义覆盖局限。** OSPO 的提示扰动限定于 Replace、Swap、Drop 三种操作，主要覆盖属性绑定、空间关系和非空间关系三类语义。对于更复杂的组合推理（如“在红色桌子上的蓝色杯子旁边的绿色椅子”），扰动策略的覆盖度可能不足，需人工验证。

**数据规模与计算成本权衡。** OSPO 从零生成训练数据，数据量可随计算资源扩展（Figure 5 左图显示 20k 样本后性能趋于饱和）。但 Figure 6 的性能-效率权衡分析表明，OSPO 虽比 SILMM 更省时，其五阶段流水线的总计算开销仍高于简单的 Best-of-N 采样方法，在资源受限场景下需权衡收益。

### 3. 局限与开放问题

**对象掩码质量的鲁棒性。** 注意力权重提取的对象掩码依赖 OTSU 二值化阈值，对于小对象、遮挡对象或多对象密集场景，掩码精度可能下降，进而影响对象加权损失的有效性。论文未提供掩码质量与最终性能的敏感性分析，该点需人工验证。

**分解 VQA 的覆盖完备性。** Self-VQA 的原子问题由 MLLM 自生成，问题质量直接影响偏好对过滤效果。论文未讨论 VQA 问题生成失败或覆盖不全的场景，该环节的鲁棒性存在开放问题。

**跨模型泛化能力。** 当前实验仅在同一架构的不同规模（1B/7B）上验证，OSPO 生成的偏好数据是否可迁移至其他 MLLM 架构（如 LLaVA 系列）训练，尚缺乏实验证据。

**对象幻觉的量化归因。** 虽然 OSPO 在多个基准上取得了最优或次优成绩（Table 1、Table 2），但论文未将性能提升分解为“对象遗漏减少”、“属性错误减少”、“空间关系改善”等细粒度归因，难以判断 OSPO 对不同类型幻觉的缓解程度是否均衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/OSPO_Object_Centric_Self_Improving_Preference_Optimization_for_Text_to_Image_Generation.pdf]]

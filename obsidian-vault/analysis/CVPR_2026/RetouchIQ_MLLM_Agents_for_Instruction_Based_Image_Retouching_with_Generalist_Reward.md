---
title: "RetouchIQ: MLLM Agents for Instruction-Based Image Retouching with Generalist Reward"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RetouchIQ_MLLM_Agents_for_Instruction_Based_Image_Retouching_with_Generalist_Reward.pdf
code_link: null
aliases:
- RetouchIQ
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通用奖励模型 (Generalist Reward Model) 与策略引导的奖励训练 (PGRT)，通过动态生成评估指标并消除训练分布偏移，提供更精准的上下文反馈。
primary_logic: 利用RL微调的MLLM作为通用奖励模型，根据具体指令和图像内容动态生成评估指标并输出标量反馈；结合PGRT对齐奖励模型与策略模型的数据分布，有效消除了训练偏差，从而显著提升指令一致性和美学质量。
claims:
- PGRT将奖励模型的分布转向真实策略生成数据，达到最高准确率，并使策略模型在RetouchEval上获得最佳性能。
- RETOUCHIQ在RetouchEval和MIT-Adobe5K基准上显著优于扩散模型和MLLM代理基线，包括通用MLLM、专业代理以及扩散方法。
- RetouchEval (Quality Improving category) 上 Overall = 7.51 (RetouchIQ-GRM)
- MIT-Adobe5K 上 PSNR = 23.14 (RetouchIQ-GRM)
---

# RetouchIQ: MLLM Agents for Instruction-Based Image Retouching with Generalist Reward

> [!tip] 核心洞察
> 利用RL微调的MLLM作为通用奖励模型，根据具体指令和图像内容动态生成评估指标并输出标量反馈；结合PGRT对齐奖励模型与策略模型的数据分布，有效消除了训练偏差，从而显著提升指令一致性和美学质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | RetouchIQ：使用通用奖励的MLLM代理进行基于指令的图像修饰 |
| 英文题名 | RetouchIQ: MLLM Agents for Instruction-Based Image Retouching with Generalist Reward |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.17558) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RetouchIQ |
| Dataset | RetouchEval, MIT-Adobe5K |

> [!tip] 效果简介
> - RetouchEval (Quality Improving category) 上，Overall 7.51 (RetouchIQ-GRM) vs second-best (unspecified value) (outperforms all baselines)。
> - MIT-Adobe5K 上，PSNR 23.14 (RetouchIQ-GRM) vs second-best (unspecified value) (improvement over baselines)。

## 概述

图像修饰任务的核心瓶颈在于其固有的主观性：同一用户指令可以对应多种合理的编辑结果，因此传统的基于像素相似度或参考图像对齐的规则化奖励信号并不可靠。同时，训练奖励模型时常用的合成扰动数据（如逆编辑扰动）与策略模型实际生成的编辑结果之间存在显著的分布偏移，进一步削弱了奖励反馈的精度。RetouchIQ 针对这两个问题提出了一套系统性的解决方案。

其核心思路是将一个经过强化学习微调的多模态大语言模型作为**通用奖励模型（Generalist Reward Model, GRM）**，使其能够根据具体的用户指令和图像内容，动态生成评估指标并输出标量奖励，从而替代僵化的规则化奖励。在此基础上，**策略引导的奖励训练（Policy-Guided Reward Training, PGRT）**将奖励模型的数据分布从合成扰动数据转向真实的策略生成数据，消除了训练分布偏移，使奖励模型能够更准确地评判策略模型的实际输出。

实验证据表明，PGRT 使奖励模型在策略生成数据上达到了最高的准确率，并由此驱动策略模型在 RetouchEval 基准上取得了最佳整体性能。在 RetouchEval 和 MIT-Adobe5K 两个基准上，RetouchIQ 均显著优于扩散模型基线（如 Flux-Pro）、通用多模态大语言模型（如 GPT-5、Gemini-2.5）以及专业的 MLLM 代理（如 MonetGPT、JarvisArt），在指令一致性和美学质量上均表现出大幅提升。

从方法谱系来看，RetouchIQ 属于基于 MLLM 代理的图像编辑方法，但其关键创新在于将奖励建模从规则空间迁移到语义空间，并通过 PGRT 实现了奖励模型与策略模型的数据分布对齐，为指令驱动的图像修饰任务提供了一个更精准、更通用的反馈机制。

## 背景与动机

图像修饰（image retouching）旨在根据用户意图对照片的曝光、色彩、对比度等属性进行精细化调整，以提升视觉质量或实现风格转换。与传统图像增强任务不同，修饰任务的核心挑战在于其**高度主观性**：同一张输入图像可能对应多种同样合理的编辑结果，用户对“好”的修饰的评判标准随指令和场景动态变化。这一特性使得依赖像素级相似度（如与参考图像的 PSNR、SSIM、LPIPS）的传统可验证奖励（verifiable reward）信号变得不可靠——当多个有效编辑都能满足用户意图时，基于固定参考的度量无法准确区分编辑质量的优劣（Figure 3 左侧）。

现有方法在应对这一挑战时存在两个关键缺口。首先，**通用 MLLM**（如 GPT-5、Gemini-2.5）虽然具备广泛的视觉理解能力，但缺乏针对图像编辑参数空间的精确控制机制，难以将抽象的美学目标转化为可执行的操作参数。其次，**专业 MLLM 代理**（如 MonetGPT、JarvisArt）和**扩散模型方法**（如 Flux-Pro）虽然能生成编辑结果，但其训练和评估通常依赖合成扰动数据——通过对原始图像施加逆编辑扰动（inverse-edit perturbations）生成“劣化”样本。这种数据构造方式引入了严重的**训练分布偏移**：合成扰动数据往往只涉及曝光、色温等单一调整，而策略模型实际生成的编辑结果通常包含复合、复杂的参数组合（Figure 3 右侧）。当奖励模型在合成数据上训练后，面对策略模型产出的真实分布时，其评估精度会显著下降，进而限制策略模型的优化效果。

针对上述问题，RetouchIQ 提出两个核心改进方向。其一，引入**通用奖励模型（Generalist Reward Model, GRM）**，利用 RL 微调后的 MLLM 根据具体指令和图像内容动态生成评估指标并输出标量反馈，替代僵化的基于规则的奖励信号。其二，设计**策略引导的奖励训练（Policy-Guided Reward Training, PGRT）**，通过将奖励模型的训练数据分布从合成扰动转向策略模型实际生成的样本，消除训练偏差，使奖励模型能够为策略模型提供更精准的上下文反馈。这一思路的根本洞察在于：奖励模型的精度瓶颈并非模型容量不足，而是其训练分布与策略模型产出分布之间的错配；通过主动对齐这两个分布，可以显著提升指令一致性和最终修饰质量。

## 核心创新

RetouchIQ 的核心创新在于用**通用奖励模型 (Generalist Reward Model, GRM)** 替代传统的基于规则的奖励信号，并引入**策略引导的奖励训练 (Policy-Guided Reward Training, PGRT)** 来消除训练分布偏移，从而在主观性极强的图像修饰任务中实现更精准的反馈对齐。

### 创新一：通用奖励模型 (GRM) — 从固定规则到动态生成

传统图像修饰任务的奖励信号通常依赖**基于像素相似度的可验证奖励**（如与 ground-truth 的 L1/L2 差异），但这类规则化奖励存在根本性缺陷：同一用户指令可以对应多种合理编辑结果，像素级相似度无法准确反映指令一致性（见 Figure 3）。RetouchIQ 提出的 GRM 是一个经过 RL 微调的 MLLM，它根据具体指令和图像内容**逐例动态生成评估指标**，并输出标量奖励值：

> “we propose a generalist reward model—an RL fine-tuned MLLM that evaluates edited results through a set of generated metrics on a case-by-case basis.”

这一设计使奖励信号能够灵活适应不同编辑意图，而非机械地套用固定指标。GRM 的输入包括编辑前后图像和用户指令，输出分为两步：先生成一组针对当前编辑的评估指标，再给出标量奖励。这种“指标生成 + 评分”的链式推理机制，使奖励模型具备了跨场景的通用评估能力。

### 创新二：策略引导的奖励训练 (PGRT) — 消除训练分布偏移

奖励模型的精度高度依赖其训练数据分布。传统方法通过**逆编辑扰动**（如随机调整曝光、色温）生成“次优”样本用于训练奖励模型，但这些合成扰动与策略模型实际生成的编辑结果存在显著分布差异——策略模型往往产生组合性的复杂编辑，而非单一参数扰动（见 Figure 3 右侧）。这种**训练分布偏移**导致奖励模型在评估真实策略输出时精度下降。

PGRT 的核心思想是将奖励模型的训练分布**从合成扰动数据转向真实策略生成数据**：

> “PGRT shifts the reward model’s distribution toward actual policy-generated data, achieving the highest accuracy on that set.”

具体而言，在 RL 阶段，PGRT 用策略模型自身生成的编辑结果替换原本的扰动样本，使奖励模型直接学习评估策略模型实际产出的质量排序。消融实验证实，PGRT 使奖励模型在策略生成数据上的准确率达到最高，并带来策略模型在 RetouchEval 基准上的最佳整体性能。

### 与 Baseline 的关键差异

| 设计维度 | Baseline（基于规则的奖励） | RetouchIQ（GRM + PGRT） |
|---------|--------------------------|------------------------|
| 奖励机制 | 固定像素相似度指标（L1/L2/PSNR） | MLLM 动态生成评估指标 + 标量反馈 |
| 训练数据分布 | 合成逆编辑扰动（单一参数调整） | 策略模型自身生成数据（组合复杂编辑） |
| 奖励精度 | 对多解编辑不精确 | 上下文感知的精准排序 |
| 策略优化效果 | 受限于不精确奖励 | 显著提升指令一致性与美学质量 |

消融实验进一步验证：用 GRM 替换基于规则的奖励后，所有指标均持续提升；而 PGRT 相比仅使用扰动数据训练的奖励模型，在策略模型最终性能上带来额外增益。这表明 GRM 解决了“奖励信号不可靠”的瓶颈，PGRT 则解决了“奖励模型训练偏差”的瓶颈，两者协同构成了 RetouchIQ 的核心技术壁垒。

## 整体框架

RetouchIQ 采用**两阶段训练策略**构建一个 MLLM 代理系统：第一阶段为监督微调（SFT），第二阶段为强化学习（RL）。系统的核心由两个模块构成——**策略模型（Policy Model）** 和**通用奖励模型（Generalist Reward Model, GRM）**，二者在 RL 阶段形成“执行-评估”闭环。

### 策略模型：从指令到可执行编辑

策略模型是一个 MLLM 代理，负责将用户的自然语言指令转化为两个输出：
- **推理轨迹（reasoning trace）**：解释如何理解用户意图并选择编辑参数；
- **参数化编辑操作序列**：一组可执行的工具调用，直接作用于输入图像。

如图 Figure 2 所示，给定输入图像 $I_0$ 和用户指令 $g$（如 “pop more”），策略模型 $\pi_{\theta}$ 首先推理出需要调整的参数（如曝光度），然后生成对应的编辑参数 $e$，最终通过 `Execute` 函数得到编辑后的图像。

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RETOUCHIQ. Left: We annotate the user instruction and reasoning for training data. Generated data are filtered to ensure quality. Middle: The supervised fine-tuning stage. Based on the user instruction (e.g., pop more), the policy model needs to reason the correct parameters (e.g., exposure) and change them accordingly. Right: The reinforcement learning stage. We leverage a generalist reward model to propose metrics and provide scalar reward guidance for policy model. Details of the reward model is introduced in Sec 4*

### 通用奖励模型：动态生成评估指标

传统图像修饰任务中，基于像素相似度的可验证奖励（verifiable reward）存在根本性缺陷：多个不同的编辑结果都可能满足用户意图，但像素级指标只认可与 ground-truth 最接近的那一个。此外，奖励模型的训练数据分布与策略模型的实际生成数据之间存在偏移，进一步降低了反馈的可靠性。

RetouchIQ 的通用奖励模型 $r_{\phi}$ 解决了这一问题。给定指令 $g$、原始图像 $I_0$ 和编辑后图像，奖励模型**按顺序生成两个输出**：
1. **一组自生成的评估指标**：根据具体指令和图像内容动态生成，而非使用固定的像素级指标；
2. **一个标量奖励值**：综合评估编辑结果与指令的一致性及美学质量。

### 训练流程

**SFT 阶段**：策略模型通过自回归损失进行监督微调，目标是最小化目标 token 序列的负对数似然：

$$\mathcal{L}_{\mathrm{SFT}} = -\sum_{t} \log p_{\theta}(y_{t} \mid y_{<t}, I_{0}, g) \tag{1}$$

其中 $y_t$ 为推理轨迹和编辑参数的目标序列。训练数据包含 190K 图像-指令对，经过质量过滤以确保数据可靠性。

**RL 阶段**：策略模型在通用奖励模型的指导下进行强化学习，最大化期望奖励：

$$\mathcal{I}(\theta) = \mathbb{E}_{q,s \sim \pi_{\theta}} \left[ r_{\phi}(g, I_{0}, \mathrm{Execute}(I_{0}, e)) + r_{\mathrm{format}}(q, s) \right] \tag{2}$$

其中 $r_{\phi}$ 为通用奖励模型的标量反馈，$r_{\mathrm{format}}$ 为格式奖励，确保输出结构符合预期。

奖励模型自身也经历 SFT 和 RL 两阶段训练。在 RL 阶段，引入了**策略引导奖励训练（Policy-Guided Reward Training, PGRT）**，将奖励模型的训练数据从合成扰动图像替换为策略模型的实际生成结果，从而消除训练分布偏移。这一设计是 RetouchIQ 实现指令一致性和美学质量显著提升的关键机制。

## 核心模块与公式推导

RetouchIQ 的核心架构由两个关键模块构成：**策略模型 (Policy Model)** 与**通用奖励模型 (Generalist Reward Model, GRM)**，二者通过两阶段训练（监督微调 SFT + 强化学习 RL）协同工作。

### 策略模型：从指令到可执行编辑

策略模型是一个 MLLM 代理，负责将用户的自然语言指令转化为两类输出：
- **推理轨迹 (reasoning trace)**：解释编辑决策的逻辑链条；
- **参数化编辑操作序列**：可被底层图像处理工具直接执行的曝光、色温等参数调整。

策略模型的监督微调采用自回归损失，最小化目标 token 序列的负对数似然：

$$
\mathcal{L}_{\mathrm{SFT}} = -\sum_{t} \log p_{\theta}(y_{t} \mid y_{<t}, I_{0}, g) \tag{1}
$$

其中 $I_{0}$ 为输入图像，$g$ 为用户指令，$y_{t}$ 为目标输出序列的第 $t$ 个 token。

在强化学习阶段，策略模型以最大化期望奖励为目标：

$$
\mathcal{I}(\theta) = \mathbb{E}_{q,s \sim \pi_{\theta}} \left[ r_{\phi}(g, I_{0}, \mathrm{Execute}(I_{0}, e)) + r_{\mathrm{format}}(q, s) \right] \tag{2}
$$

其中 $r_{\phi}$ 为通用奖励模型给出的标量奖励，$\mathrm{Execute}(I_{0}, e)$ 表示对输入图像执行编辑操作 $e$ 后得到的输出图像，$r_{\mathrm{format}}$ 为格式奖励项。

### 通用奖励模型：动态指标生成与标量反馈

通用奖励模型是 RetouchIQ 的核心创新。传统图像修饰任务中，基于像素相似度的可验证奖励（verifiable reward）因修饰结果的主观性与多解性而不可靠——同一指令可对应多种合理编辑，与单一 ground truth 的像素差异无法准确反映指令一致性（见 Figure 3 左中部分）。

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/003_Figure_3.jpg]]
*Figure 3: Problematic rewards in image retouching tasks. Given a before–after image pair (left), ❶ verifiable rewards (middle) rely on metrics between the edited image and ground truth, such as pixel differences. However, since multiple valid edits can satisfy user intent, these rewards become imprecise. ❷ The reward model’s precision strongly depends on its training data distribution (right). When trained to distinguish good user edits from randomly perturbed images, it may later struggle to assess results from the policy model that produces combined, complex edits*

GRM 通过 RL 微调的 MLLM 实现，其输出分为两步：
1. 根据具体指令与图像内容，**动态生成一组评估指标**；
2. 基于这些指标输出一个**标量奖励值**。

这种“按需生成指标”的机制使奖励信号能灵活适配不同修饰场景，而非依赖固定的像素级度量。

奖励模型的监督微调损失为：

$$
\mathcal{L}_{\mathrm{SFT}}^{\mathrm{reward}} = -\sum_{t} \log p_{\phi}(y_{t} \mid y_{<t}, I_{0}, I, I_{w}, g) \tag{3}
$$

其中 $I$ 为优质编辑结果，$I_{w}$ 为次优编辑结果（通过扰动生成），模型需学习正确区分二者。

### 策略引导奖励训练 (PGRT)：消除分布偏移

奖励模型的训练数据若仅由合成扰动样本构成，会与策略模型实际生成的编辑数据产生分布偏移——扰动样本多为单一参数调整，而策略模型生成的是组合式复杂编辑（见 Figure 3 右侧）。PGRT 通过将 RL 阶段的次优样本 $I_{w}$ 从扰动分布替换为策略模型自身生成的结果，使奖励模型与策略模型的数据分布对齐。

PGRT 的优化目标惩罚不正确的分数排序：

$$
\mathcal{I}(\phi) = \mathbb{E}_{m, r, r_{w} \sim \pi\phi} \left[ \mathbb{I}[r > r_{w}] + r_{\mathrm{format}}(m, r, r_{w}) \right] \tag{4}
$$

其中 $\mathbb{I}[r > r_{w}]$ 为指示函数，当优质结果的奖励 $r$ 大于次优结果的奖励 $r_{w}$ 时给予正向激励。实验表明，PGRT 使奖励模型在策略生成数据上的准确率达到最高，并带来策略模型在 RetouchEval 上的最佳整体性能。

### 补充图表

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/004_Figure_4.jpg]]
*Figure 4: Overview of generalist reward model. Left: Given a before-edited image and a user-edited after image*

## 实验与分析

### 核心瓶颈与评估逻辑

图像修饰任务的评估面临双重困境。一方面，基于像素相似度的可验证奖励（verifiable reward）假设存在唯一的地面真值，但同一用户意图往往允许多种有效编辑，导致奖励信号不精确（Figure 3 左/中）。另一方面，奖励模型的训练数据通常通过逆编辑扰动合成，与策略模型实际生成的复合编辑存在分布偏移，进一步削弱了奖励的可靠性（Figure 3 右）。RETOUCHIQ 通过通用奖励模型（GRM）和策略引导奖励训练（PGRT）系统性地解决这两个问题。

### 主实验结果

**RetouchEval 基准。** Table 1 报告了 RetouchEval 上三类场景（画质提升、风格变换、局部修饰）的定量对比。RETOUCHIQ 在 SFT 阶段（RetouchIQ-SFT）已超越通用 MLLM（GPT-5、Gemini-2.5）、MLLM 代理（MonetGPT、JarvisArt）和扩散方法（Flux-Pro），而引入 GRM 强化学习后（RetouchIQ-GRM）在所有指标上取得最优。在画质提升类别中，RetouchIQ-GRM 的 Overall 得分达到 7.51，显著优于基于规则奖励的变体（RetouchIQ-Rule），验证了通用奖励对指令一致性和感知质量的双重增益。

**MIT-Adobe5K 基准。** Table 2 显示 RetouchIQ-GRM 在 SSIM、LPIPS 和 PSNR 上均取得最佳结果，其中 PSNR 达到 23.14。值得注意的是，该基准的参考图像为单一专家修饰结果，而 RETOUCHIQ 仍能超越基线，表明其编辑质量不仅满足主观偏好，也与专业标准高度吻合。

### 消融分析：奖励机制与训练策略

Figure 5 系统对比了不同奖励模型配置下的奖励准确率与策略模型性能。核心发现如下：

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of reward model and policy model performance under different reward model configurations. The lines show the accuracies of the reward model, while the bars indicate the scores of the corresponding policy model*

1. **通用奖励 vs. 规则奖励。** 用 GRM 替换基于规则的奖励后，策略模型在 RetouchEval 所有指标上持续提升，证明动态生成的上下文相关指标比固定像素相似度更有效地捕捉指令一致性。

2. **PGRT 的分布对齐效应。** 在仅使用合成扰动数据训练奖励模型时，其对策略生成数据的准确率显著下降（红蓝线分离）。PGRT 将奖励模型的分布转向实际策略生成数据，使该准确率达到最高，并带来策略模型的最佳 RetouchEval 性能——奖励准确率与策略性能呈正相关，验证了分布对齐的关键性。

3. **训练阶段拆解。** SFT 阶段赋予策略模型基本的指令遵循和参数预测能力；RL 阶段通过 GRM 的标量反馈进一步优化推理轨迹和编辑参数，两者叠加产生累积增益。

### 关键图表结论

- **Table 1**：RetouchIQ-GRM 在 RetouchEval 三类场景中全面超越通用 MLLM、专用代理和扩散方法，且 GRM 强化学习相较 SFT 和规则奖励变体均有显著提升。
- **Table 2**：在 MIT-Adobe5K 上，RetouchIQ-GRM 的 PSNR（23.14）和感知指标均优于基线，证明其编辑质量与专家修饰高度一致。
- **Figure 5**：PGRT 通过消除训练分布偏移，使奖励模型在策略生成数据上达到最高准确率，并直接转化为策略模型的最优性能——奖励越精准，策略越强。

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on the RETOUCHEVAL benchmark. We consider three categories of baselines: general-purpose MLLMs (GPT-5, Gemini-2.5); MLLM agents (MonetGPT, JarvisArt); and diffusion-based methods (Flux-Pro). Meanwhile, we report the performance of RETOUCHIQ under both the SFT (RetouchIQ-SFT) and RL (RetouchIQ-RL) stages. We also include results from a variant trained with rule-based reward (RetouchIQ-Rule). The best results are shown in bold, and the second-best results are underlined*

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on the MIT-Adobe5K benchmark*

### 补充图表

![[assets/figures/papers/paper_list_l2664_https_arxiv_org_abs_2602_17558/figures/001_Figure_1.jpg]]
*Figure 1: We present RETOUCHIQ, an MLLM agent that performs customized image retouching. Given an user instruction and an image input, RETOUCHIQ produces high-quality results across various quality enhancement and style transformation scenarios*

## 方法谱系与知识库定位

### 任务定位：指令驱动的图像修饰

RetouchIQ 解决的是**基于自然语言指令的图像修饰**（instruction-based image retouching）任务。与传统的图像增强（如自动曝光校正、超分辨率）或文本驱动的图像生成/编辑（如 Stable Diffusion + ControlNet）不同，该任务要求模型同时理解用户的高层美学意图（“让画面更温暖”、“增加对比度使主体突出”）并将其映射为精确的、可执行的参数化编辑操作。这一任务的核心瓶颈在于：图像修饰具有高度主观性，同一指令可能对应多种合理编辑结果，因此传统基于像素相似度（PSNR、SSIM）或参考图像对齐的规则化奖励信号并不可靠。

### 方法谱系中的位置

RetouchIQ 处于 **MLLM Agent** 与 **RLHF（Reinforcement Learning from Human Feedback）** 两个研究脉络的交汇点。

**相对于通用 MLLM 与扩散模型基线**：论文将 RetouchIQ 与三类方法进行了对比（Table 1、Table 2）：

- **通用 MLLM**：GPT-5、Gemini-2.5 等模型具备跨模态理解能力，但缺乏对图像编辑工具链的结构化调用能力，其输出往往是像素空间的端到端生成，难以精确控制编辑参数。
- **MLLM Agent**：MonetGPT、JarvisArt 等方法引入了工具调用机制，将指令解析为编辑操作序列。RetouchIQ 在此基础上进一步引入了**推理轨迹（reasoning trace）**作为中间表示，使模型在输出编辑参数前先进行显式的语义分析，从而提升指令对齐的精度。
- **扩散模型方法**：Flux-Pro 等基于扩散的方法在图像生成质量上表现优异，但在指令一致性和可控性方面存在固有局限——扩散模型难以实现精确的参数化调整（如曝光+0.5EV、色温-200K），且编辑过程缺乏可解释的推理链。

**相对于规则化奖励方法**：传统 RLHF 在图像编辑中通常依赖可验证奖励（verifiable reward），例如计算编辑结果与 ground-truth 之间的像素差或感知相似度。RetouchIQ 指出了这一范式的根本缺陷（Figure 3）：由于同一指令允许多种有效编辑，规则化奖励无法准确区分“不同但都合理”的结果，导致奖励信号噪声大、优化目标模糊。RetouchIQ 的**通用奖励模型（Generalist Reward Model, GRM）**替代了这一机制——它本身是一个经 RL 微调的 MLLM，能够根据具体指令和图像内容动态生成评估指标，并输出标量反馈。

### 核心创新与因果机制

RetouchIQ 的方法论贡献可分解为两个相互耦合的因果旋钮：

**1. 通用奖励模型（GRM）——动态指标生成替代静态规则**

GRM 的核心创新在于将奖励评估从“固定指标计算”转变为“上下文相关的动态评估”。给定输入图像 $I_0$、编辑结果 $I$ 和用户指令 $g$，GRM 首先生成一组针对该具体案例的评估指标（如“肤色自然度”、“阴影细节保留度”），然后基于这些指标输出标量奖励值 $r_\phi(g, I_0, I)$。这一设计使得奖励信号能够捕捉主观美学维度，而非仅依赖像素级保真度。

奖励模型的监督微调采用自回归损失：
$$\mathcal{L}_{\mathrm{SFT}}^{\mathrm{reward}} = -\sum_{t} \log p_{\phi}(y_{t} \vert y_{<t}, I_{0}, I, I_{w}, g)$$
其中 $I_w$ 为通过扰动生成的次优编辑结果，模型需学会区分优劣编辑对。

**2. 策略引导奖励训练（PGRT）——消除训练分布偏移**

这是 RetouchIQ 最关键的因果机制。论文明确指出（Figure 3 右侧、Section 4.3）：传统奖励模型的训练数据通过“逆编辑扰动”（inverse-edit perturbation）生成——对原始编辑进行单维度随机扰动（如仅调整曝光或色温），得到次优样本。然而，策略模型实际生成的编辑往往是**多维度组合的复杂编辑**，导致训练分布与推理分布之间存在显著偏移。奖励模型在扰动数据上表现良好，却在策略生成数据上精度下降，形成“奖励破解”（reward hacking）风险。

PGRT 的解决方案是：在 RL 阶段，将奖励模型训练数据中的次优样本 $I_w$ 从“扰动合成数据”替换为“策略模型实际生成的结果”，使奖励模型的数据分布与策略模型的输出分布对齐。PGRT 的目标函数惩罚不正确的排序：
$$\mathcal{I}(\phi) = \mathbb{E}_{m, r, r_{w} \sim \pi\phi} \left[ \mathbb{I}[r > r_{w}] + r_{\mathrm{format}}(m, r, r_{w}) \right]$$

实验证据（Figure 5）强有力地支持了这一机制的有效性：PGRT 训练的奖励模型在策略生成数据上的准确率达到最高（红色折线），且使用该奖励模型训练的策略模型在 RetouchEval 基准上获得最佳整体性能（柱状图）。这表明 PGRT 通过消除分布偏移，使奖励模型能够为策略模型提供更精准的反馈信号。

### 适用边界与局限

**适用场景**：RetouchIQ 适用于需要精确参数控制和指令对齐的图像修饰任务，包括质量增强（曝光、对比度、色彩平衡）、风格转换（电影感、复古风）和局部修饰（面部提亮、背景虚化）。其 MLLM Agent 架构天然支持工具链扩展，理论上可接入更多图像处理算子。

**已知局限**（需人工验证，论文未明确列出）：
- **工具链依赖**：RetouchIQ 的编辑能力受限于其调用的参数化工具集。对于超出工具表达能力的高级编辑需求（如语义级物体替换、复杂场景合成），方法可能不适用。
- **奖励模型泛化性**：GRM 在训练时使用了特定的扰动策略和偏好数据分布，其在全新编辑风格或极端指令下的评估准确性有待验证。
- **计算开销**：两阶段训练（SFT + RL）以及 RL 阶段中 GRM 的在线评估均引入额外计算成本，论文未报告训练效率数据。
- **多指令冲突**：当用户指令包含相互矛盾的要求时（如“更亮但保持暗调氛围”），模型的推理轨迹是否能正确消解冲突，论文未提供相关分析。

### 开放问题

1. GRM 生成的动态评估指标是否具有跨任务的迁移能力？能否直接应用于视频修饰、3D 渲染等其他视觉编辑任务？
2. PGRT 在更复杂的多轮交互编辑场景中是否仍然有效？当策略模型持续进化时，奖励模型是否需要持续同步更新？
3. 论文未讨论 GRM 本身的偏好对齐问题——GRM 的评估标准来源于训练数据中的偏好标注，这些标注可能存在文化偏见或美学偏好偏差，如何检测和缓解这种偏差？
4. RetouchIQ 的推理轨迹是否可被用户干预或修正？人机协同编辑的交互范式值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/RetouchIQ_MLLM_Agents_for_Instruction_Based_Image_Retouching_with_Generalist_Reward.pdf]]

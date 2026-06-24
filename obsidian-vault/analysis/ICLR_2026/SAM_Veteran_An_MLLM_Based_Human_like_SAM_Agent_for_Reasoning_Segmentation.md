---
title: "SAM-Veteran: An MLLM-Based Human-like SAM Agent for Reasoning Segmentation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SAM_Veteran_An_MLLM_Based_Human_like_SAM_Agent_for_Reasoning_Segmentation.pdf
openreview_forum_id: oN55r8iJJW
aliases:
- SV
- SAM-Veteran
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入多任务强化学习框架（文本定位、掩码理解和辅助掩码理解任务）与动态采样策略，将MLLM与SAM的交互建模为MDP，并设计包含SAM奖励、决策奖励和IoU改进奖励的复合奖励函数。"
primary_logic: "通过多任务RL训练，MLLM能够像经验丰富的SAM用户一样执行完整的推理分割工作流程：先生成边界框获取初始掩码，再基于掩码质量生成精炼点，并自适应地决定何时终止，从而在域内和域外数据集上均取得最优性能。"
claims:
- "SAM-Veteran在ReasonSeg val上达到68.2 gIoU和67.3 cIoU，显著超越所有基线。"
- "结合文本定位、掩码理解和辅助任务的全模型实现了最佳性能与自适应终止。"
- "迭代掩码精炼带来持续的IoU提升，尤其在域外数据上效果显著。"
- "去除任何奖励分量均导致性能一致下降，验证了复合奖励设计的必要性。"
---

# SAM-Veteran: An MLLM-Based Human-like SAM Agent for Reasoning Segmentation

> [!tip] 核心洞察
> 通过多任务RL训练，MLLM能够像经验丰富的SAM用户一样执行完整的推理分割工作流程：先生成边界框获取初始掩码，再基于掩码质量生成精炼点，并自适应地决定何时终止，从而在域内和域外数据集上均取得最优性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SAM-Veteran：基于多模态大语言模型的人类化SAM推理分割智能体 |
| 英文题名 | SAM-Veteran: An MLLM-Based Human-like SAM Agent for Reasoning Segmentation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oN55r8iJJW) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SAM-Veteran |
| Dataset | ReasonSeg val, ReasonSeg test, RefCOCO testA |

> [!tip] 效果简介
> - ReasonSeg val 上，gIoU 为 68.2，对比 62.6 (Seg-Zero)，变化 +5.6。
> - ReasonSeg val 上，cIoU 为 67.3，对比 62.0 (Seg-Zero)，变化 +5.3。
> - ReasonSeg test 上，gIoU 为 62.6，对比 57.5 (Seg-Zero)，变化 +5.1。

## 概述

**核心问题**：现有的基于多模态大语言模型（MLLM）的推理分割方法存在两个根本瓶颈。其一，它们未能充分利用SAM的交互式迭代精炼能力，仅以单步生成框或点的方式与SAM交互，无法模拟人类用户使用SAM时的自然工作流程——先生成边界框获取初始掩码，再基于掩码质量进行点精炼，并自适应地决定何时终止。其二，主流的监督微调（SFT）方法在赋予模型新能力的同时，会导致灾难性遗忘，损害模型的通用推理能力。

**核心方法**：SAM-Veteran将MLLM与SAM的交互建模为马尔可夫决策过程（MDP），并引入多任务强化学习框架——基于Group Relative Policy Optimization（GRPO）同时训练文本定位、掩码理解和辅助掩码理解三项任务。其关键在于设计了一个复合奖励函数，融合了SAM奖励、决策奖励和IoU改进奖励，引导MLLM像经验丰富的SAM用户一样执行完整的推理分割工作流程：生成边界框 → 基于掩码质量生成精炼点 → 自适应终止。此外，动态采样策略确保了GRPO训练的稳定性。

**核心结论**：SAM-Veteran在域内和域外数据集上均取得最优性能。在ReasonSeg val上达到68.2 gIoU和67.3 cIoU，显著超越最强基线Seg-Zero（+5.6/+5.3）；在ReasonSeg test上同样领先（+5.1 gIoU）。在RefCOCO、RefCOCO+、RefCOCOg等域内数据集以及MMR、MUSE等域外数据集上均保持优势。消融实验证实，三项训练任务、复合奖励的每个分量、动态采样和思维链（CoT）均对最终性能有不可或缺的贡献。更重要的是，RL训练保留了模型的通用推理能力，而SFT方法在此方面出现明显退化。

**方法谱系与知识库定位**：SAM-Veteran属于基于强化学习的推理分割方法，与Seg-Zero（Liu et al., 2025a）、SegAgent（Zhu et al., 2025b）、SAM-R1（Huang et al., 2025）和POPEN（Zhu et al., 2025a）处于同一技术路线，但区别于LISA（Lai et al., 2024）、VISA（Yan et al., 2024）、PixelLM（Ren et al., 2024b）等基于SFT的方法。相较同类RL方法，SAM-Veteran的独特贡献在于：将交互建模为多步迭代过程（框→点→自适应终止）而非单步，设计多任务RL框架与复合奖励函数，并通过动态采样稳定训练。

## 背景与动机

推理分割（Reasoning Segmentation）要求模型根据复杂的自然语言查询，在图像中定位并分割出目标区域。这一任务的核心挑战在于，模型需要同时具备视觉-语言推理能力和精确的像素级掩码生成能力。

**现有范式的瓶颈。** 当前主流的推理分割方法普遍采用“MLLM预测几何提示 + SAM生成掩码”的两阶段范式。然而，这些方法存在一个关键的认知缺口：它们将MLLM与SAM的交互限定为单步操作——MLLM一次性输出边界框或稀疏点，然后交由SAM生成最终掩码。这种设计忽略了人类用户使用SAM的自然工作流程。有经验的用户在使用SAM时，通常会先给出一个粗略的边界框获取初始掩码，然后根据掩码质量不断添加正/负点进行迭代精炼，直到对结果满意为止。现有方法未能模拟这一完整的交互式精炼过程，导致分割精度受限，尤其在域外数据上表现不佳。

**训练范式的局限。** 在训练层面，现有方法主要依赖监督微调（SFT）或单一任务的强化学习（RL）。SFT方法（如**LISA** (Lai et al., 2024)、**VISA** (Yan et al., 2024)、**PixelLM** (Ren et al., 2024b)）虽然能在域内数据上取得不错的效果，但存在灾难性遗忘问题，会严重损害MLLM的通用推理能力。而现有的RL方法（如**POPEN** (Zhu et al., 2025a)、**SegAgent** (Zhu et al., 2025b)、**Seg-Zero** (Liu et al., 2025a)）虽然在一定程度上缓解了遗忘问题，但它们的动作空间和奖励设计仍然过于简单，无法引导模型学会完整的“框生成→点精炼→自适应终止”工作流程。

**本文动机。** 针对上述不足，本文提出SAM-Veteran，旨在让MLLM像经验丰富的SAM用户一样执行完整的推理分割工作流程。核心思想是：将MLLM与SAM的多步交互建模为马尔可夫决策过程（MDP），通过多任务强化学习框架训练MLLM同时掌握文本定位、掩码理解和自适应终止三种能力，并设计复合奖励函数引导模型在每一步做出最优决策。这一设计使得模型不仅能在域内数据上取得最优性能，还能在域外数据上展现出更强的泛化能力，同时保留MLLM的通用推理能力。

## 核心创新

SAM-Veteran的核心创新在于将MLLM与SAM的交互从单步传递提升为**人类化的迭代推理分割工作流**，并通过**多任务强化学习框架**驱动这一过程。与现有方法相比，其关键突破体现在以下五个维度。

### 1. 交互范式：从单步前馈到迭代精炼

现有基于MLLM的推理分割方法（如LISA、VISA、PixelLM、Seg-Zero等）通常采用单步交互：MLLM生成边界框或点坐标后一次性传递给SAM，无法利用SAM的交互式精炼能力。SAM-Veteran将整个过程建模为**马尔可夫决策过程（MDP）** $ (S, \mathcal{A}, T, R) $，其中状态 $ s = (M, I, Q) $ 由当前掩码 $ M $、图像 $ I $ 和问题 $ Q $ 组成，动作空间包含正点 $ p^+ $、负点 $ p^- $ 和空操作 $ \mathrm{null} $。模型执行完整的三阶段工作流（Figure 1）：

1. **文本定位**：根据图像-问题对生成目标边界框，输入SAM获取初始掩码；
2. **迭代点精炼**：基于当前掩码质量生成精炼点，反馈给SAM更新掩码；
3. **自适应终止**：当掩码质量满意时输出 $ (\mathrm{null}, \mathrm{null}) $ 停止迭代，而非依赖固定步数。

这一设计使MLLM能够像经验丰富的SAM用户一样，根据掩码质量动态调整精炼策略。

### 2. 训练框架：从SFT或单一RL到多任务GRPO

现有方法主要依赖监督微调（SFT）或单一RL任务。SFT方法面临**灾难性遗忘**问题——分割训练会损害MLLM的通用推理能力（Table 8）。单一RL任务则无法覆盖完整工作流所需的多维度能力。

SAM-Veteran提出基于**Group Relative Policy Optimization（GRPO）**的多任务RL框架（Figure 2），包含三个互补任务：

- **文本定位任务（Textual Grounding）**：训练MLLM生成高质量边界框，使SAM输出的初始掩码最大化IoU；
- **掩码理解任务（Mask Comprehension）**：训练MLLM根据当前掩码质量判断是否需要精炼，并生成有效的精炼点；
- **辅助掩码理解任务（Auxiliary Mask Comprehension）**：通过人工腐蚀的GT掩码（随机添加假阳性/假阴性区域）训练模型识别和定位虚假区域，增强对掩码缺陷的感知能力。

消融实验（Table 4）表明：仅用文本定位任务时模型无法自适应终止；去除掩码理解任务导致性能下降且无法终止；去除辅助任务使模型陷入无限精炼。三者协同才能实现最优性能（Avg IoU 72.2）和正确的终止行为。

### 3. 奖励函数：从简单IoU到复合多信号奖励

现有RL方法通常仅使用框IoU或掩码IoU作为单一奖励信号。SAM-Veteran设计了**复合奖励函数**，针对不同任务阶段提供多维度反馈：

- **文本定位阶段**：$ R^{\mathrm{SAM}} = \mathrm{IoU}(M, M^{\mathrm{GT}}) $ 直接将SAM输出掩码的质量作为奖励，配合硬阈值框IoU奖励 $ R_{\mathrm{IoU}}^{\mathrm{B}} $ 和L1距离奖励 $ R_{L_1}^{\mathrm{B}} $；
- **掩码精炼阶段**（Table 2）：组合三种奖励——**决策奖励** $ R^{\mathrm{DCS}} $ 鼓励模型在掩码不满意时输出精炼点、满意时输出空；**IoU改进奖励** $ R^{\Delta} $ 根据精炼前后IoU增量分档激励（增量越大奖励越高，Table 1）；**鼓励奖励** $ R^{\mathrm{ENC}} $ 在掩码已满意时对输出空的正确决策给予正向反馈。

消融实验（Table 5）验证了每个奖励分量的必要性：去除SAM奖励、决策奖励或IoU改进奖励均导致性能一致下降。将软阶梯IoU改进奖励替换为硬版本 $ R_h^{\Delta} = 3 \mathbb{1}_{\Delta > 0} $ 也会略微降低性能，说明分档设计更有效。

### 4. 采样策略：从随机采样到动态采样

标准GRPO训练中随机采样可能导致动作分布不均匀，影响优化稳定性。SAM-Veteran引入**动态采样策略**：对精炼点按 $ (\mathrm{null}, \mathrm{null}) $、$ (p^+, \mathrm{null}) $、$ (\mathrm{null}, p^-) $、$ (p^+, p^-) $ 四类情况分别以 $ (1, 2, 2, 1) $ 的比例过采样；对边界框应用NMS（IoU阈值0.8）去重。该策略在训练初期启用，300次迭代后关闭以加速训练。消融实验（Table 6）显示去除动态采样使平均IoU从72.2降至70.8。

### 5. 灾难性遗忘缓解：RL优于SFT

Table 8的系统性对比表明，基于SFT的方法（如SegAgent）在通用MLLM基准上出现显著性能退化，而SAM-Veteran的RL训练框架有效保留了基础模型的通用推理能力。这一特性源于GRPO优化过程中策略更新受KL散度约束，避免了SFT中参数的大幅偏移。

## 整体框架

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_oN55r8iJJW/figures/002_Figure_2.jpg]]
*Figure 2: Multi-task RL framework comprising Textual Grounding, Mask Comprehension, and Auxiliary Mask Comprehension. Two rollouts (with their rewards) are shown in different colors (blue and yellow). In the final reward, different bar textures represent different reward functions*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_oN55r8iJJW/figures/001_Figure_1.jpg]]
*Figure 1: Inference workflow of SAM-Veteran. Given an image-question pair, SAM-Veteran first predicts a bounding box for the target, which SAM converts into an initial mask. SAM-Veteran iteratively refines this mask by generating refinement points for SAM, until either both points are null (indicating a satisfactory segmentation) or the maximum refinement step is reached*

### 问题形式化：推理分割的马尔可夫决策过程

SAM-Veteran将推理分割建模为马尔可夫决策过程（MDP）$(S, \mathcal{A}, T, R)$，其中MLLM扮演一个经验丰富的SAM用户角色，执行完整的推理驱动分割工作流：文本定位 → 迭代精炼 → 自适应终止。

**状态空间** $s = (M, I, Q)$ 由当前分割掩码 $M$、输入图像 $I$ 和查询问题 $Q$ 组成的三元组定义。初始状态下 $M$ 为空，模型首先需要根据 $I$ 和 $Q$ 定位目标区域。

**动作空间** 在精炼阶段定义为：
$$a \in \{ (p^{+}, p^{-}), (p^{+}, \mathrm{null}), (\mathrm{null}, p^{-}), (\mathrm{null}, \mathrm{null}) \}$$
其中 $p^{+}$ 为正点（指示前景区域），$p^{-}$ 为负点（指示背景区域），$\mathrm{null}$ 表示该位置不输出点。当模型输出 $(\mathrm{null}, \mathrm{null})$ 时，表示当前掩码已满意，工作流自适应终止。

**转移函数** $T$ 由SAM承担：接收MLLM输出的边界框或精炼点，生成或更新分割掩码，并将新掩码以绿色透明覆盖图的形式叠加到原图上，作为下一状态输入MLLM。

### 多任务强化学习框架

SAM-Veteran的训练基于Group Relative Policy Optimization（GRPO），包含三个互补的RL任务，如Figure 2所示：

| 模块 | 角色 | 核心机制 |
|------|------|----------|
| **文本定位**（Task 1） | 根据图像-问题对生成目标边界框 | 复合奖励：框IoU硬阈值奖励 + 框L1距离奖励 + SAM掩码IoU奖励 |
| **掩码理解**（Task 2） | 根据当前掩码质量生成精炼点或决定终止 | 复合奖励：决策奖励 + IoU改进奖励（软阶梯函数） |
| **辅助掩码理解**（Task 3） | 识别并定位人工腐蚀掩码中的虚假区域 | 在GT掩码上注入随机多边形假阳性/假阴性区域，训练模型输出正确的点类型 |

三个任务共享同一MLLM骨干，通过不同提示模板（Figure 5）区分任务类型，在GRPO框架下联合优化。

### 复合奖励设计

奖励函数是驱动MLLM学会“人类化SAM交互”的关键因果旋钮。

**文本定位阶段**的奖励包含三个分量：
- **框IoU奖励** $R_{\mathrm{IoU}}^{\mathrm{B}}$：当预测框与GT框的IoU > 0.5时奖励为1，否则为0（硬阈值）。
- **框L1奖励** $R_{L_1}^{\mathrm{B}}$：当预测框坐标的平均L1距离 < 10像素时奖励为1。
- **SAM奖励** $R^{\mathrm{SAM}} = \mathrm{IoU}(M, M^{\mathrm{GT}})$：以SAM根据预测框生成的掩码与GT掩码的IoU作为直接奖励，将SAM的反馈信号纳入RL优化。

**掩码精炼阶段**的奖励由Table 1和Table 2定义：
- **决策奖励** $R^{\mathrm{DCS}}$：鼓励模型在掩码不满意时输出精炼点，在掩码满意时输出 $(\mathrm{null}, \mathrm{null})$，否则为0。
- **IoU改进奖励** $R^{\Delta}$：根据精炼前后IoU的增量 $\Delta$ 分档奖励——$\Delta \leq 0$ 得0分，$(0, 0.1]$ 得1分，$(0.1, 0.5]$ 得2分，$(0.5, 1]$ 得3分。这种软阶梯设计（而非硬阈值）在消融实验中被证明更有效（Table 5）。
- 总奖励 $R = R^{\mathrm{DCS}} + R^{\Delta}$，最大值为4。

### 动态采样策略

GRPO训练需要从策略中采样多个rollout来估计优势函数。为稳定训练并保证动作多样性，SAM-Veteran引入动态采样策略：
- 对边界框采样应用NMS（IoU阈值0.8）消除重复。
- 对精炼点按 $(1, 2, 2, 1)$ 的计数比例过采样四种动作类型，防止模型过早收敛到单一行为。
- 训练300次迭代后关闭动态采样以加速收敛。

消融实验（Table 6）表明，去除动态采样导致平均IoU从72.2降至70.8；去除思维链（CoT）降至70.6；两者结合使用时互补增益显著。

### 推理工作流

推理时，SAM-Veteran执行端到端工作流（Figure 1）：
1. **文本定位**：输入图像和查询问题，MLLM输出目标边界框。
2. **初始掩码生成**：SAM根据边界框生成初始分割掩码。
3. **迭代精炼**：将掩码叠加到原图，MLLM评估掩码质量并输出精炼点；SAM根据精炼点更新掩码。
4. **自适应终止**：当MLLM输出 $(\mathrm{null}, \mathrm{null})$ 或达到最大精炼步数时停止，返回最终掩码。

该工作流的关键瓶颈突破在于：MLLM不仅学会了“何时精炼”，更学会了“如何精炼”——在掩码不满意时生成有意义的正/负点，在掩码满意时主动终止，而非固定步数的盲目迭代。Figure 3的趋势曲线验证了迭代精炼带来的持续IoU提升，尤其在域外数据上效果显著。

## 核心模块与公式推导

### 3.1 推理分割的MDP建模

SAM-Veteran将完整的推理分割工作流程建模为马尔可夫决策过程（MDP），使MLLM能够像经验丰富的SAM用户一样执行多步交互式分割。MDP的形式化定义为：

$$(S, \mathcal{A}, T, R)$$

**状态空间** $S$：状态定义为当前掩码、图像和问题三元组：

$$s = (M, I, Q)$$

其中 $M$ 为SAM当前输出的分割掩码，$I$ 为输入图像，$Q$ 为推理问题。初始状态中 $M$ 为空，模型首先生成边界框，SAM据此产生初始掩码后进入迭代精炼阶段。

**动作空间** $\mathcal{A}$：精炼动作由正点（指示前景）和负点（指示背景）的组合构成：

$$a \in \{ (p^{+}, p^{-}), (p^{+}, \mathrm{null}), (\mathrm{null}, p^{-}), (\mathrm{null}, \mathrm{null}) \}$$

其中 $(p^{+}, p^{-})$ 表示同时提供正点和负点，$(p^{+}, \mathrm{null})$ 仅提供正点，$(\mathrm{null}, p^{-})$ 仅提供负点，$(\mathrm{null}, \mathrm{null})$ 表示模型判定当前掩码已满意，触发自适应终止。

**转移函数** $T$：由SAM的交互机制隐式定义——MLLM输出的点坐标传递给SAM，SAM据此更新掩码，产生新状态。

**奖励函数** $R$：由多任务RL框架中的复合奖励设计定义（详见3.2节）。

### 3.2 多任务强化学习框架

SAM-Veteran的训练基于Group Relative Policy Optimization（GRPO），包含三个互补的训练任务。

#### 3.2.1 文本定位任务（Task 1）

该任务训练MLLM根据图像和问题生成目标边界框 $b$。奖励由三个分量组成：

**Box IoU奖励**：采用硬阈值形式，当预测框与真值框的IoU超过0.5时给予正向激励：

$$R_{\mathrm{IoU}}^{\mathrm{B}} = \left\{ \begin{array}{ll} 1, & \mathrm{IoU}(b, b^{\mathrm{GT}}) > 0.5 \\ 0, & \mathrm{otherwise} \end{array} \right.$$

**Box L1奖励**：当预测框坐标的平均L1距离小于10像素时给予奖励：

$$R_{L_1}^{\mathrm{B}} = \left\{ \begin{array}{ll} 1, & \sum_i |b_i - b_i^{\mathrm{GT}}| / 4 < 10 \\ 0, & \mathrm{otherwise} \end{array} \right.$$

**SAM奖励**：直接以SAM根据预测框生成的掩码与真值掩码的IoU作为奖励，将SAM的反馈信号纳入RL优化：

$$R^{\mathrm{SAM}} = \mathrm{IoU}(M, M^{\mathrm{GT}})$$

消融实验（Table 10）表明，Box IoU奖励采用硬阈值0.5优于软IoU奖励，验证了这一设计的合理性。

#### 3.2.2 掩码理解任务（Task 2）

该任务训练MLLM根据当前掩码质量生成精炼点或决定终止。掩码根据IoU分为两类：IoU $=1$ 的掩码被标记为“Good Enough”（满意），IoU $<0.9$ 的掩码被标记为“Need Refinement”（需要精炼）。

**决策奖励** $R^{\mathrm{DCS}}$：鼓励模型在掩码需要精炼时输出有效精炼点，在掩码满意时输出 $(\mathrm{null}, \mathrm{null})$ 以终止；若行为与掩码状态不匹配则奖励为0。

**IoU改进奖励** $R^{\Delta}$：根据精炼前后IoU的增量分档奖励（Table 1）：

| IoU增量 $\Delta$ | 奖励 $R^{\Delta}$ |
|---|---|
| $\Delta \leq 0$ | 0 |
| $0 < \Delta \leq 0.1$ | 1 |
| $0.1 < \Delta \leq 0.5$ | 2 |
| $0.5 < \Delta \leq 1$ | 3 |

当掩码需要精炼时，总奖励为决策奖励与IoU改进奖励之和：

$$R = R^{\mathrm{DCS}} + R^{\Delta}$$

最大可达4分。Table 2汇总了所有情况下的奖励组合。

#### 3.2.3 辅助掩码理解任务（Task 3）

该任务通过人工腐蚀的真值掩码训练模型识别和定位虚假区域。具体地，对真值掩码随机添加多边形包含区（作为假阳性区域）和排除区（作为假阴性区域），要求MLLM对这些区域输出相应的正点或负点。

**决策奖励** $R_{A}^{\mathrm{DCS}}$：鼓励模型对假阳性区域输出负点，对假阴性区域输出正点，对无缺陷区域输出空。

**点位置评估**：使用距离阈值 $\tau_d = 50$ 像素——若输出点与缺陷区域中心的距离小于50像素，则认为位置准确。

### 3.3 动态采样策略

为稳定GRPO训练中的动作多样性，SAM-Veteran采用动态采样策略。在文本定位任务中，对MLLM生成的多个候选框应用NMS（IoU阈值0.8）去重后采样。在掩码理解任务中，按 $(1, 2, 2, 1)$ 的比例分别采样 $(\mathrm{null}, \mathrm{null})$、$(p^{+}, \mathrm{null})$、$(\mathrm{null}, p^{-})$、$(p^{+}, p^{-})$ 四类动作。动态采样在训练初期启用，300次迭代后关闭以加速训练，且不影响最终性能（section A.2）。

## 实验与分析

### 核心发现：SAM-Veteran在域内与域外数据集上均取得最优性能

SAM-Veteran在推理分割的核心基准ReasonSeg上显著超越所有现有方法。在ReasonSeg验证集上，SAM-Veteran达到**68.2 gIoU**和**67.3 cIoU**，相比此前最强的RL方法Seg-Zero（62.6 gIoU / 62.0 cIoU）分别提升**+5.6**和**+5.3**个百分点（Table 3）。在ReasonSeg测试集上同样表现出色，gIoU达到62.6，领先Seg-Zero达+5.1个百分点。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_oN55r8iJJW/figures/005_Table_3.jpg]]
*Table 3: We compare IoU (%) of different MLLM-based methods (7B version) across both indomain and out-of-domain datasets*

在域内参考分割数据集上，SAM-Veteran同样保持领先：RefCOCO testA上cIoU达**80.8**（+0.5 vs Seg-Zero），RefCOCO+ testA上达**76.6**（+0.4），RefCOCOg test上达**73.4**（+0.8）。尽管这些数据集上各方法差距相对较小，SAM-Veteran仍一致优于所有SFT方法（LISA、VISA、PixelLM等）和RL方法（POPEN、SegAgent、Seg-Zero、SAM-R1）。

在更具挑战性的域外数据集MMR和MUSE上，SAM-Veteran的优势更加明显（Table 7）：MMR上gIoU达**40.38**（+2.47 vs Seg-Zero），MUSE上gIoU达**53.63**（+1.47）。这验证了迭代精炼策略在分布外场景下的鲁棒性。

### 迭代精炼带来持续IoU提升

Figure 3揭示了迭代精炼的动态过程：随着精炼步数增加，掩码IoU持续提升，尤其在域外数据上效果显著。同时，终止率随步数增加而上升，表明模型能够自适应地在掩码质量满意时停止精炼，避免不必要的计算开销。这一行为模式模拟了人类用户使用SAM时的自然决策过程——当分割结果足够好时即停止交互。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_oN55r8iJJW/figures/006_Figure_3.jpg]]
*Figure 3: Trends of IoU (∆) and termination ratio over refinement iterations*

### 多任务RL框架的消融分析

**三个训练任务的必要性**（Table 4）。以Qwen2.5-VL+SAM2为基线（仅在文本定位任务上训练），逐步添加掩码理解（MC）和辅助掩码理解（A）任务：

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_oN55r8iJJW/figures/007_Table_4.jpg]]
*Table 4: Ablation study on three training tasks: Textual Grounding (TG), Mask Comprehension (MC), and Auxiliary (A). We report the IoU along with the termination behavior of the models*

- 仅文本定位（TG）：模型只能生成边界框，无法进行点精炼，性能受限。
- TG+MC：模型获得了精炼能力，但缺少辅助任务的训练，在复杂场景下容易陷入无限精炼，无法自适应终止。
- TG+MC+A（完整SAM-Veteran）：达到最高平均IoU **72.2**，并实现了自适应终止——模型在掩码满意时输出`(null, null)`停止精炼，在需要改进时输出正/负点。

去除掩码理解任务导致模型完全丧失迭代精炼能力，而去除辅助任务则导致模型无法学会何时终止，验证了三个任务协同作用的必要性。

**复合奖励设计的消融**（Table 5）。逐一移除奖励分量均导致性能一致下降：

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_oN55r8iJJW/figures/008_Table_5.jpg]]
*Table 5: Ablation study on reward design, including removing SAM reward $R ^ { \mathrm { S A M } }$ , decision reward $R _ { * } ^ { \mathrm { { D C S } } }$ , and IoU improvement reward $\breve { R ^ { \Delta } }$ , and replacing $R ^ { \Delta }$ with a hard version $R _ { h } ^ { \Delta }$

- 移除SAM奖励（$R^{\mathrm{SAM}}$）：平均IoU从72.2降至71.0，说明将SAM输出质量直接纳入奖励信号对文本定位任务至关重要。
- 移除决策奖励（$R^{\mathrm{DCS}}$）：平均IoU降至71.1，模型无法有效判断何时应输出精炼点、何时应终止。
- 移除IoU改进奖励（$R^{\Delta}$）：平均IoU降至71.4，模型缺乏对精炼质量的细粒度反馈。
- 将软阶梯IoU改进奖励替换为硬版本（$R_h^{\Delta} = 3 \cdot \mathbb{1}_{\Delta > 0}$）：平均IoU略降至71.9，说明分档奖励（0/1/2/3）比简单的二元奖励更有效地引导精炼行为。

**动态采样与思维链的互补作用**（Table 6）。去除动态采样（DS）导致平均IoU从72.2降至70.8，去除思维链（CoT）降至70.6。两者同时去除会进一步损害性能。动态采样通过在训练中过采样不同动作类型（正点、负点、空），确保GRPO优化过程中动作多样性的稳定；CoT则引导模型在生成精炼决策前进行显式推理。

### 通用能力保留：RL训练避免灾难性遗忘

Table 8展示了关键对比：SFT方法（如SegAgent）在通用MLLM基准上出现明显退化，而SAM-Veteran通过RL训练保留了Qwen2.5-VL的原始推理能力。在OCR相关理解（SEED-Bench-2-Plus、TextVQA）和通用视觉问答（MMStar、MME、MMBench等）共8个基准上，SAM-Veteran与原始Qwen2.5-VL表现相当，验证了GRPO框架在任务特化训练中保持通用能力的有效性。

### 失败模式分析

Figure 12揭示了SAM-Veteran的典型失败案例，按错误类型着色：

1. **初始框定位错误**：当文本描述的目标在图像中难以准确定位时，初始边界框可能完全偏离目标，导致后续精炼无法挽救。
2. **精炼点位置偏差**：模型生成的正/负点可能落在错误区域，引导SAM向错误方向精炼。
3. **过早终止**：模型在掩码质量仍不理想时即输出`(null, null)`终止，导致分割不完整。
4. **过晚终止**：模型在掩码已足够好时继续精炼，可能引入新的错误区域。

这些失败模式与论文声明的局限性一致：SAM-Veteran不支持完全自由形式的行为（如生成新框或撤销操作），且将掩码以绿色透明覆盖图输入MLLM可能干扰对颜色敏感的查询。

### 规模效应与推理成本

Table 9显示，将MLLM从7B扩展到32B带来额外性能提升，但增益相对有限，表明7B版本已具备较强的推理分割能力。Table 11的推理成本对比显示，SAM-Veteran的迭代精炼机制在增加适度计算开销的同时，换取了显著的精度提升，在精度-效率权衡上优于固定步数的基线方法。

## 方法谱系与知识库定位

### 推理分割的范式演进

推理分割任务要求模型根据自然语言查询在图像中分割出目标区域，其核心挑战在于将语言理解与像素级定位对齐。现有方法可分为两大范式：

**基于监督微调（SFT）的方法** 通过构建<图像，问题，掩码>三元组数据集，直接微调多模态大语言模型以输出分割掩码或SAM提示。代表性工作包括 **LISA**（Lai et al., 2024）、**VISA**（Yan et al., 2024）、**PixelLM**（Ren et al., 2024b）、**PerceptionGPT**（Pi et al., 2024）和 **GSVA**（Xia et al., 2024）。这类方法的瓶颈在于：SFT训练仅教会模型单步生成框或点，无法模拟人类使用SAM时的迭代精炼行为；更严重的是，SFT会引发灾难性遗忘，导致模型通用推理能力显著退化（见表8证据）。

**基于强化学习（RL）的方法** 试图将分割过程建模为序列决策问题。**POPEN**（Zhu et al., 2025a）、**SegAgent**（Zhu et al., 2025b）、**Seg-Zero**（Liu et al., 2025a）和 **SAM-R1**（Huang et al., 2025）均采用RL框架，但在交互范式和奖励设计上存在关键局限：它们通常仅使用单一RL任务和简单的掩码IoU奖励，缺乏对"何时精炼、何时终止"的显式建模，导致模型无法自适应终止或陷入无效迭代。

### SAM-Veteran的核心突破

SAM-Veteran将MLLM与SAM的交互建模为完整的马尔可夫决策过程（MDP），状态定义为 $s = (M, I, Q)$（掩码、图像、问题三元组），动作空间包含正/负精炼点及空操作 $a \in \{ (p^{+}, p^{-}), (p^{+}, \mathrm{null}), (\mathrm{null}, p^{-}) \}$。这一形式化使得模型能够像经验丰富的SAM用户一样执行完整工作流程：**框生成→点精炼→自适应终止**。

与现有RL方法的关键差异体现在三个层面：

1. **多任务RL训练框架**：同时训练文本定位（Task 1）、掩码理解（Task 2）和辅助掩码理解（Task 3）三个任务，使模型既学会生成高质量初始框，又学会基于掩码反馈进行精炼决策。
2. **复合奖励函数设计**：将SAM奖励 $R^{\mathrm{SAM}} = \mathrm{IoU}(M, M^{\mathrm{GT}})$、决策奖励 $R^{\mathrm{DCS}}$（鼓励在掩码不满意时输出精炼点，满意时输出空）和IoU改进奖励 $R^{\Delta}$（根据精炼前后IoU增量分档奖励，最大3分）组合，形成 $R = R^{\mathrm{DCS}} + R^{\Delta}$ 的复合奖励（见表2）。
3. **动态采样策略**：在GRPO训练中过采样不同动作类型（如对边界框应用NMS阈值0.8去重，对精炼点按(1,2,2,1)比例采样），确保动作多样性，稳定优化过程。

### 性能边界与证据强度

**域内性能**：在ReasonSeg val上，SAM-Veteran达到68.2 gIoU和67.3 cIoU，较最强基线Seg-Zero（62.6/62.0）分别提升+5.6和+5.3个百分点（Table 3，置信度0.98）。在ReasonSeg test上，gIoU领先+5.1个百分点。

**域外泛化**：在RefCOCO/RefCOCO+/RefCOCOg系列数据集上，SAM-Veteran分别达到80.8/76.6/73.4 cIoU，均超越所有基线。在更具挑战性的MMR和MUSE数据集上，gIoU分别达到40.38和53.63，领先Seg-Zero +2.47和+1.47（Table 7，置信度0.98）。

**消融实验的因果验证**：
- 去除掩码理解任务导致模型无法自适应终止，性能下降（Table 4，置信度0.95）。
- 去除辅助掩码理解任务导致模型陷入无限精炼循环（Table 4，置信度0.95）。
- 去除SAM奖励、决策奖励或IoU改进奖励中任一分量均导致性能一致下降，验证复合奖励的必要性（Table 5，置信度0.98）。
- 将软阶梯IoU改进奖励替换为硬版本 $R_{h}^{\Delta} = 3 \mathbb{1}_{\Delta > 0}$ 导致性能略降，说明分档奖励更有效（Table 5，置信度0.9）。
- RL训练保留了通用推理能力（在OCR相关理解和通用VQA基准上无显著退化），而SFT方法出现明显性能衰退（Table 8，置信度0.95）。

### 适用边界与局限

**适用场景**：SAM-Veteran适用于需要根据自然语言描述进行目标分割的任务，包括但不限于指代表达分割（RES）和推理分割（ReasonSeg）。其迭代精炼机制在域外数据上尤为有效——Figure 3显示，随着精炼步数增加，IoU持续提升且终止率逐渐上升，表明模型学会了在掩码质量足够时自适应停止。

**已知局限**：
1. **受限的行动空间**：SAM-Veteran不支持完全自由形式的人类交互行为，例如在初始步骤后生成新的边界框、撤销之前的操作或组合多个框。当前动作空间仅包含点级精炼和终止。
2. **颜色感知退化风险**：将掩码以绿色透明覆盖图的形式输入MLLM会改变物体的原始颜色，可能导致对颜色敏感查询（如"红色的苹果"）的性能下降。这是视觉呈现方式引入的固有偏差。
3. **动态采样的超参数敏感性**：动态采样策略的超参数（如NMS阈值0.8、采样比例(1,2,2,1)、训练300迭代后关闭）在不同任务和数据集上的泛化性尚未充分验证（置信度0.8）。

### 开放问题

1. **行动空间扩展**：如何将动作空间扩展至包含框级操作（生成新框、撤销、组合多框），以实现更接近人类交互的完整工作流程？
2. **掩码呈现方式优化**：如何在不影响颜色感知的前提下向MLLM呈现分割掩码？可能的方案包括边缘轮廓叠加、半透明填充或分离通道输入。
3. **框架泛化性**：该多任务RL框架是否可扩展到其他需要交互式分割的视觉任务，如视频目标分割、3D点云分割或医学图像分割？
4. **动态采样策略的鲁棒性**：动态采样的超参数在不同数据分布和任务复杂度下的最优配置规律尚待系统研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/SAM_Veteran_An_MLLM_Based_Human_like_SAM_Agent_for_Reasoning_Segmentation.pdf]]

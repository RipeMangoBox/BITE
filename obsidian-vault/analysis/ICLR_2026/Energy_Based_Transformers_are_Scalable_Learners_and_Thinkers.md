---
title: "Energy-Based Transformers are Scalable Learners and Thinkers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Energy_Based_Transformers_are_Scalable_Learners_and_Thinkers.pdf
project_link: https://energy-based-transformers.github.io
code_link: https://github.com/alexiglad/ebt
openreview_forum_id: ZBj3Qp1bYg
aliases:
- EBTE
- EBTASLT
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过无监督训练一个显式能量基模型（EBM）作为验证器，学习输入与候选预测之间的兼容性（能量标量），并将预测重新定义为在能量景观上的梯度下降优化。该机制使模型在推理时能够动态分配计算（Facet 1）并进行显式预测验证（Facet 2），从而自然涌现系统2思维。"
primary_logic: "将生成与验证统一在单一可学习的能量函数内，利用“验证比生成容易”的直觉，让模型通过迭代能量最小化来自发地学会“思考”，在提升预训练可扩展性的同时显著增强了分布外泛化与推理能力。"
claims:
- "EBT预训练扩展速率比Transformer++高至35%"
- "EBT通过增加推理时前向次数可将性能提升最高29%，而Transformer++无法通过增加计算改善预测"
- "EBT在图像降噪上超越扩散Transformer（DiT），且仅需1%的前向次数"
- "系统2思维在分布外数据上带来更大的性能增益，增益随分布偏移程度线性增加"
---

# Energy-Based Transformers are Scalable Learners and Thinkers

> [!tip] 核心洞察
> 将生成与验证统一在单一可学习的能量函数内，利用“验证比生成容易”的直觉，让模型通过迭代能量最小化来自发地学会“思考”，在提升预训练可扩展性的同时显著增强了分布外泛化与推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于能量的变换器：可扩展的学习者与思考者 |
| 英文题名 | Energy-Based Transformers are Scalable Learners and Thinkers |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ZBj3Qp1bYg) · [GitHub](https://github.com/alexiglad/ebt) · [Project](https://energy-based-transformers.github.io) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Energy-Based Transformers (EBTs) |
| Dataset | GSM8K (reasoning, OOD), Image Denoising (In-Distribution), Image Denoising (OOD Noise), Image Classification (linear probe) |

> [!tip] 效果简介
> - GSM8K (reasoning, OOD) 上，Perplexity↓ 为 43.3，对比 49.6 (Transformer++)，变化 -6.3。
> - Image Denoising (In-Distribution) 上，PSNR↑ 为 27.25，对比 26.58 (DiT)，变化 +0.67。
> - Image Denoising (OOD Noise) 上，PSNR↑ 为 23.29，对比 19.56 (DiT)，变化 +3.73。

## 概要

当前深度学习模型——无论是前馈Transformer还是现代RNN——本质上属于“系统1”推理器：它们对每个预测分配固定计算量，缺乏动态分配计算（Facet 1）和显式验证预测（Facet 2）的能力。扩散Transformer（DiT）虽能通过延长去噪过程增加推理计算，但缺少显式的预测验证机制（Table 1）。现有推理方法通常依赖模态特定或问题特定的设计，或需要监督式训练（如验证器或可验证奖励），难以仅通过无监督学习自然涌现通用的“系统2”思考能力。

针对这一瓶颈，本文提出**基于能量的变换器（Energy-Based Transformers, EBTs）**——一种新的能量基模型（EBM）类别。其核心机制是训练一个显式的能量函数 $E_\theta(x, \hat{y})$，学习输入 $x$ 与候选预测 $\hat{y}$ 之间的兼容性（输出一个能量标量），并将预测重新定义为在该能量景观上的梯度下降优化（Equation 1, Figure 2）。这一设计将生成与验证统一在单一可学习的能量函数内，使模型在推理时能够**动态分配计算**（通过迭代梯度下降精炼预测，即“思考更久”）和**显式验证预测**（通过生成多个候选并选择能量最低者，即“自验证”），从而自然涌现系统2思维。

核心结论：
- **预训练可扩展性**：EBT在语言建模预训练中的扩展速率比标准自回归Transformer配方（**Transformer++**，Touvron et al., 2023）高出最高35%（Figure 4, Figure 5）。
- **推理时性能增益**：EBT通过增加推理前向次数可将性能提升最高29%，而Transformer++无法通过增加计算改善预测（Figure 7a）。该增益在分布外（OOD）数据上更为显著，且随分布偏移程度线性增加（Figure 6）。
- **跨模态泛化**：在图像降噪任务上，EBT超越扩散Transformer（**DiT**，Peebles & Xie, 2023），且仅需1%的前向次数（Table 4）；在图像分类（线性探针）上准确率提升约5个百分点；在数独算法推理的OOD测试集上准确率达29.7%，远超前馈Transformer的0.03%（Table 5）。
- **能量景观正则化**：Langevin动力学、回放缓存、随机步长/步数等正则化技术对系统2思维至关重要——完整配置实现了18.7%的最佳困惑度改善（Table 2）。

方法定位：EBT属于能量基模型家族，通过无监督的优化式训练学习能量景观，在推理时利用梯度下降进行迭代预测精炼。与扩散模型相比，EBT被显式训练为验证器；与标准自回归模型相比，EBT在架构层面内置了动态计算分配与自验证能力（Table 1）。当前局限包括FLOP效率较低（因需二阶梯度）、训练稳定性对超参数敏感，以及尚未在大规模基础模型上验证。

当前深度学习模型，特别是自回归Transformer，在处理标准预测任务时展现出强大的系统1能力——即快速、自动的前馈推理。然而，这些模型在需要系统2思维的场景中暴露了本质缺陷：它们无法动态分配计算资源，也缺乏对自身预测进行显式验证的机制。**系统2思维**，指代深思熟虑的、迭代的、自验证的认知过程，对于分布外（OOD）泛化和复杂推理至关重要。

### 现有方法的认知缺口

从认知架构的角度审视，主流模型在两个关键维度上存在缺失（Table 1）：

- **Facet 1：动态计算分配**。前馈Transformer和现代RNN对每个预测执行固定量的计算，无法根据问题难度灵活调整推理深度。扩散Transformer（DiT）虽能通过增加去噪步数延长推理计算，但这一能力是任务特异的——它依赖于扩散过程的逐步去噪范式，而非通用的“思考”机制。

- **Facet 2：显式预测验证**。上述架构均不提供对预测质量的直接标量评估。Transformer输出概率分布，但该分布本身即是生成结果，缺乏独立的验证信号。DiT同样不具备显式验证能力，其生成过程仅依赖逐步去噪，无法在最终输出上评估“这个预测有多好”。

### 现有推理增强方法的局限

为弥补系统2能力的缺失，现有工作主要沿两条路径展开：

1. **监督式方法**：训练独立的验证器模型或利用可验证奖励信号（如数学题的正确性标签）来引导推理。这类方法需要人工标注或特定领域的验证规则，无法通过无监督学习自然涌现。

2. **模态/任务特异性方法**：针对特定模态（如文本的思维链提示）或特定任务（如数学推理的符号搜索）设计推理策略。这些方法难以泛化到新的模态和任务类型。

核心瓶颈在于：**能否仅通过无监督学习，让模型自发地发展出通用的系统2思维能力？** 换言之，能否在不依赖外部验证信号或任务特定设计的前提下，让模型学会“思考”？

### 本文的核心动机

本文的出发点是重新审视预测问题的本质。如果将预测视为一个优化问题——寻找与输入最兼容的输出——那么系统2思维自然对应于在某个兼容性度量下的迭代搜索过程。这引出了两个关键洞察：

1. **“验证比生成容易”**：判断一个预测是否与输入兼容，通常比直接生成最优预测更简单。这一直觉暗示，学习一个验证器（评估输入-预测对的兼容性）可能比学习一个生成器更具可扩展性。

2. **统一生成与验证**：如果能将验证器与生成器统一在单一模型中——生成器由验证器的梯度隐式定义——那么模型就能通过优化过程同时实现预测生成和自验证。

基于此，本文提出**基于能量的变换器（Energy-Based Transformers, EBTs）**：训练一个显式的能量基模型（EBM）作为验证器，学习为每个输入-候选预测对分配一个能量标量（表示兼容性），并将预测重新定义为在该能量景观上的梯度下降优化。这一框架使模型在推理时能够动态分配计算（Facet 1）并进行显式预测验证（Facet 2），从而仅通过无监督学习自然涌现系统2思维。

## 核心方法与创新机理

EBT的核心创新在于将预测问题重新定义为**在单一可学习的能量函数上的优化过程**，从而将生成与验证统一于同一模型内，使系统2思维能力（动态计算分配与显式预测验证）从无监督学习中自然涌现。

### 预测机制的范式转换

标准自回归Transformer（如**Transformer++**，Touvron et al., 2023）通过前馈网络直接输出下一个token的概率分布——预测是一次性的、计算量固定的。EBT从根本上改变了这一机制：它学习一个能量函数 $E_\theta(x, \hat{y})$，接收输入 $x$ 与候选预测 $\hat{y}$，输出一个表示兼容性的能量标量。预测过程变为在能量景观上的**梯度下降优化**：

$$\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_\theta(x, \hat{y}_i)$$

这一公式（Equation 1）是EBT方法的核心引擎。初始预测从随机初始化开始，通过多步梯度下降逐步向低能量区域移动，直至能量收敛。这赋予了模型**Facet 1**——动态计算分配：模型可以在推理时根据任务难度自适应地调整优化步数（“思考更久”），而Transformer++的每token计算量是固定的。

### 训练损失流的二阶重构

标准模型的训练仅需一阶梯度：在前向输出上直接计算交叉熵损失，反向传播一次即可。EBT的训练则需要**穿过整个优化链反向传播**（Algorithm 1），这意味着损失是在经多步梯度下降优化后的预测上计算的，梯度必须流经每一步优化更新。这要求计算二阶导数（Hessian-向量积），使得训练计算图比标准Transformer深得多。这一改变是实现“学会思考”的必要代价——模型必须学会塑造一个能量景观，使得梯度下降轨迹能够从随机初始化收敛到正确预测。

### 能量景观正则化：从优化到探索

单纯的梯度下降容易陷入局部最优，限制了思维多样性。EBT引入了四项能量景观正则化技术，将确定性优化转化为**带探索的随机优化**：

- **Langevin动力学**：在梯度下降更新中加入高斯噪声 $\eta_i \sim \mathcal{N}(0, \sigma)$，鼓励在能量景观上的探索
- **随机步长与随机步数**：训练时随机化优化步长和步数，迫使模型学习鲁棒的能量景观
- **回放缓存**：存储历史预测状态用于训练，平滑能量景观

消融实验（Table 2）揭示了关键的探索-利用权衡：移除Langevin动力学后，单路径“思考更久”的困惑度改善提升至17.2%，但自验证性能下降至17.0%；完整系统2配置（四项技术全开）在延长思维与自验证结合时达到最佳困惑度改善18.7%。**随机步长**被证明是最关键的组件——移除后思维性能几乎无增益（-1.47% / 0.19%），说明能量景观的平滑性对系统2思维至关重要。

### 自验证：显式预测验证的涌现

EBT的**Facet 2**——显式预测验证——通过自验证机制实现：并行生成多个候选预测（从不同随机初始化出发优化），比较其最终能量，选择能量最低者作为输出（Algorithm 2）。这一能力完全从无监督预训练中涌现，无需额外的验证器训练或可验证奖励信号。关键证据来自Figure 7b：随着训练规模的增加，自验证带来的性能增益从4%-8%提升至12%-14%，表明验证能力随预训练可扩展。

### 与扩散模型的本质区别

**扩散Transformer（DiT）**（Peebles & Xie, 2023）同样支持推理时动态计算（通过增加去噪步数），但EBT与其有根本性差异：DiT学习的是从噪声到数据的映射过程，而非显式的能量函数；它缺乏一个可计算的兼容性标量用于预测验证。Table 1系统对比了各架构的认知能力：前馈Transformer和RNN的计算量有限且无验证能力；DiT可增加计算但无显式验证；只有EBT同时具备动态计算（Facet 1）和能量标量验证（Facet 2）。

### 架构实现：因果注意力的修改

为支持自回归建模，EBT修改了标准因果注意力模式。在预测token $z_t$ 时，模型不仅条件于已生成的token $z_{<t}$，还同时条件于当前预测状态 $\hat{z}_t$。这通过注意力得分矩阵的超对角线非零项实现（Equation 3），打破了传统自回归“仅看过去”的约束，使能量函数能够评估当前预测与上下文的兼容性。

### 核心直觉的凝练

EBT的设计哲学根植于一个简单直觉：**验证比生成容易**。通过训练一个评判输入-预测对兼容性的能量函数，模型学会了一个“验证器”；而生成则被隐式定义为验证器梯度的负方向——沿能量下降最快的方向移动预测。这统一了传统上分离的生成器与验证器，使“思考”成为能量景观上的自然动力学过程，而非需要外部监督信号引导的搜索。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_ZBj3Qp1bYg/figures/002_Table_1.jpg]]
*Table 1: Architectures and Cognitive Facets. For each prediction, Feed-Forward (FF) Transformers and RNNs generally1 have a finite amount of computation. DiTs (Diffusion Transformers) can increase inference computation by denoising longer, but lack explicit prediction verification. In contrast, EBMs support dynamic computation through flexible iteration, and give an energy scalar for prediction verification*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_ZBj3Qp1bYg/figures/001_Figure_1.jpg]]
*Figure 1: Autoregressive Architecture Comparison. (a) Autoregressive (AR) Transformer is the most common, with (b) RNNs becoming more popular recently Gu & Dao (2023); Peng et al. (2023). (c) Diffusion Transformers (DiTs) Li et al. (2025b); Peebles & Xie (2023) are similar to EBT, being able to dynamically allocate computation during inference. However, diffusion models are not trained as explicit verifiers, unlike EBTs*

Energy-Based Transformer (EBT) 的核心思想是将预测问题重新定义为在可学习的能量景观上的优化问题。其整体 pipeline 围绕一个统一的能量函数构建，该函数同时承担“生成器”与“验证器”的双重角色，使模型能够通过无监督学习自然涌现系统2思维能力（动态计算分配与显式预测验证）。

### 核心模块与数据流

EBT 的 pipeline 由三个关键模块串联构成，形成“输入→能量评估→梯度优化→预测输出”的闭环：

**1. 能量函数 (Energy Function / Transformer Backbone)**
将输入 $x$（上下文）与候选预测 $\hat{y}$ 拼接后送入 Transformer 骨干网络，输出一个标量能量值 $E_\theta(x, \hat{y})$，表示输入与预测之间的兼容性（兼容性越高，能量越低）。该模块是 EBT 的核心，同时实现了 Facet 2（显式预测验证）的能力——能量标量本身即为对预测质量的显式评估信号。对于自回归建模，EBT 采用修改后的因果注意力模式，在超对角线上引入预测状态，使模型能同时条件于过去 token 与当前预测（见 Equation 3）。

**2. 梯度下降优化器 (Gradient Descent Optimizer)**
利用能量函数关于预测的梯度 $\nabla_{\hat{y}} E_\theta(x, \hat{y})$ 执行多步梯度下降，逐步精炼预测：
$$\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_\theta(x, \hat{y}_i)$$
该模块实现了 Facet 1（动态计算分配）：推理时可通过增加优化步数（Thinking Longer）来分配更多计算资源，步数越多，预测越精细。训练时，损失在经多步优化后的最终预测上计算，并反向传播穿过整个优化链，需要二阶梯度（Hessian-向量积）支持。

**3. 能量景观正则化 (Energy Landscape Regularization)**
为促进能量景观的探索并提升系统2思维质量，在梯度下降中引入四项正则化技术：
- **随机步长与随机步数**：随机化每次优化的步长和步数，防止模型过拟合到固定优化路径；
- **Langevin 动力学**：在梯度更新中加入高斯噪声 $\eta_i \sim \mathcal{N}(0, \sigma)$，鼓励对能量景观的探索：
  $$\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_\theta(x, \hat{y}_i) + \eta_i$$
- **回放缓存 (Replay Buffer)**：存储历史预测样本，增强训练多样性。

消融实验（Table 2）证实，完整的系统2配置（随机步长 + 随机步数 + Langevin + 回放缓存）在延长思维与自验证结合时实现最佳困惑度改善 18.7%；移除随机步长后思维性能几乎无增益（-1.47% / 0.19%），表明随机化对系统2思维至关重要。

### 推理时的自验证机制

在推理阶段，EBT 可通过 **Self-Verification (Best-of-N)** 策略进一步增强性能：并行生成 $N$ 个预测（每个从不同随机初始化出发，经多步梯度下降优化），比较各候选的最终能量，选择能量最低者作为输出。该机制将能量函数显式用作验证器，实现了“生成多个候选→能量评估→择优输出”的验证闭环。

### 与基线架构的关键差异

| 架构 | 预测机制 | 推理计算 | 显式验证 |
|------|---------|---------|---------|
| **Transformer++** (Touvron et al., 2023) | 前馈网络直接输出概率分布 | 固定（单步前向） | 无 |
| **DiT** (Peebles & Xie, 2023) | 迭代去噪 | 可动态增加去噪步数 | 无（训练时无显式验证器） |
| **EBT** (本文) | 梯度下降最小化能量隐式生成预测 | 可动态增加优化步数 | 有（能量标量作为验证信号） |

关键区别在于：DiT 虽能动态分配计算，但未将模型训练为显式验证器；EBT 则将生成与验证统一在单一能量函数内，利用“验证比生成容易”的直觉，使模型通过能量最小化自发学会“思考”。

### 训练与推理流程对比

- **训练**：从随机初始化预测出发，经 $K$ 步梯度下降优化后得到最终预测，在此预测上计算损失并通过二阶梯度反向传播更新能量函数参数（Algorithm 1）。
- **推理**：同样从随机预测出发，经 $K$ 步梯度下降优化至能量收敛；可选地生成多个候选并选最低能量者（Algorithm 2）。

### 当前局限

EBT 的 FLOP 效率是主要瓶颈：使用两步优化时，计算开销约为同参数标准 Transformer 的 6.66 倍。训练稳定性对优化步长、噪声幅度等超参数敏感，需仔细调参。此外，当前实验规模限于中等模型（最大约 400M 参数），在更大规模上的表现有待验证。

### 能量基模型范式

EBT将预测问题重新定义为在可学习能量景观上的优化问题。给定输入 $x$ 和候选预测 $\hat{y}$，能量函数 $E_{\theta}(x, \hat{y})$ 输出一个标量，表示二者的兼容性——能量越低，预测越合理。模型通过无监督学习来塑造该能量景观，使真实数据位于低能量区域，而错误预测处于高能量区域。

这一设计将生成器与验证器统一于单一模型中：生成器由能量函数关于预测的梯度隐式定义，而验证器则直接由能量标量本身充当。其概率解释基于玻尔兹曼分布：

$$p_{\theta}(x, \hat{y}) \propto e^{-E_{\theta}(x, \hat{y})}$$

其中归一化常数（配分函数）在实际训练中无需显式计算，因为EBT采用基于优化的学习框架，避免了维度灾难问题。

### 预测机制：梯度下降优化

EBT的核心预测机制是将推理转化为在能量景观上的梯度下降过程。给定输入 $x$，预测 $\hat{y}$ 从随机初始化开始，通过多步梯度下降逐步精炼：

$$\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_{\theta}(x, \hat{y}_i)$$

其中 $\alpha$ 为步长，$i$ 为优化步数索引。每次迭代中，模型计算当前预测的能量，并沿能量梯度反方向移动预测，使其滑向低能量（高兼容性）区域。优化持续进行直至能量收敛，此时预测被视为最终输出。

这一迭代过程实现了 **Facet 1（动态计算分配）**：模型可以根据输入难度自适应地调整优化步数，简单样本快速收敛，困难样本则允许更长的“思考”过程。同时，每一步输出的能量标量天然实现了 **Facet 2（预测验证）**：能量值指示了当前预测的可靠程度。

### 能量景观正则化模块

为促进系统2思维所需的探索性与多样性，EBT引入四项能量景观正则化技术：

**Langevin动力学**：在梯度下降中注入高斯噪声，鼓励对能量景观的探索，避免过早陷入局部最优：

$$\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_{\theta}(x, \hat{y}_i) + \eta_i, \quad \eta_i \sim \mathcal{N}(0, \sigma)$$

**随机步长与随机步数**：训练时在指定范围内随机采样优化步长和步数，使模型学习鲁棒的优化路径，而非依赖固定的优化超参数。消融实验证实，移除随机步长后思维性能几乎无增益（-1.47% / 0.19%），是其最关键的正则化组件。

**回放缓存**：存储历史优化轨迹中的中间预测，在训练中随机回放，防止模型遗忘早期探索经验，平滑能量景观。

### 自验证模块

推理时，EBT可通过 Best-of-N 策略实现显式自验证：并行生成 $N$ 个候选预测（各从不同随机初始点出发，经独立梯度下降优化），比较其最终能量值，选择能量最低者作为输出。该机制将“验证比生成容易”的直觉操作化为可计算过程，无需额外训练验证器网络。

### 训练损失流

EBT的训练损失计算与传统前馈模型有本质区别。损失并非直接作用于单步前向输出，而是在经 $K$ 步梯度下降优化后的最终预测 $\hat{y}_K$ 上计算（如交叉熵损失）。关键的是，该损失需反向传播穿过整个优化链，因此需要计算二阶导数（Hessian-向量积），这构成了EBT训练计算开销的主要来源——在当前两步优化实现下，FLOPs约为同参数标准Transformer的6.66倍。

### 自回归EBT的注意力机制

为适配自回归语言建模，EBT修改了标准因果注意力模式。在预测位置 $t$ 的token时，模型不仅条件于已生成的上下文 $z_{1:t-1}$，还同时条件于当前正在优化的预测 $\hat{z}_t$。其注意力得分矩阵在超对角线上引入预测状态，实现“同时条件于过去与当前预测”的信息流：

$$\mathrm{scores} = \begin{bmatrix} \alpha_{z_1,z_1} & \alpha_{z_1,\hat{z}_2} & 0 & \dots & 0 \\ \alpha_{z_2,z_1} & \alpha_{z_2,z_2} & \alpha_{z_2,\hat{z}_3} & \dots & 0 \\ \vdots & \vdots & \vdots & \ddots & \vdots \end{bmatrix}$$

该设计确保了自回归生成的因果性不被破坏，同时允许能量函数充分评估当前预测与上下文的兼容性。

## 实验与关键发现

### 核心实验结果

EBT在三个核心维度上验证了其设计优势：预训练可扩展性、推理时计算动态分配能力，以及跨模态的分布外泛化能力。

**预训练缩放定律。** 在语言建模任务上，EBT展现出比标准自回归Transformer（Transformer++，Touvron et al., 2023）更优的缩放特性。在数据量、批大小和深度三个维度上，EBT的缩放曲线均显著优于Transformer++（Figure 4）。在参数量和FLOPs缩放维度上，EBT的缩放指数比Transformer++高8.97%（Figure 5a-b），意味着随着计算预算增加，EBT的性能提升更快。这一结果直接支撑了论文的核心主张：将预测重新定义为能量景观上的优化问题，在预训练阶段就能带来更高的数据效率。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_ZBj3Qp1bYg/figures/007_Figure_4.jpg]]
*Figure 4: Language Learning Scalability—Data, Batch Size, and Depth. A comparison between the scaling of the Transformer++ recipe Touvron et al. (2023) and EBTs across data, batch size, and depth during pretraining. On all axes, EBTs out-scale the Transformer++ recipe significantly, indicating improved data efficiency. The improved depth scaling offers promise for reasoning, where depth is crucial Ye et al. (2024). These results suggest that EBTs offer promise at large data scale*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_ZBj3Qp1bYg/figures/011_Figure_5.jpg]]
*Figure 5: (a) Scaling for number of Parameters. (b) Scaling for number of FLOPs. (c) Scaling for the embed. dimension. Figure 5: Language Learning Scalability—Parameters, FLOPs, and Width. Pretraining scaling comparisons between the Transformer++ recipe Touvron et al. (2023) and EBTs across model size (parameters), compute (FLOPs), and width (embedding dimension). EBTs have an 8.97% higher scaling rate than the Transformer++ in FLOP and parameter scaling (a and b), suggesting that EBTs offer promise as a pretraining approach*

**推理时计算分配（Facet 1：动态思考）。** 在四个分布外语言数据集上，EBT通过增加推理时的前向传播次数（即“思考更久”），可将困惑度改善最高达29%，而Transformer++完全无法通过增加计算来改善预测（Figure 7a）。这一对比揭示了关键因果机制：标准自回归模型的前馈预测机制不具备动态分配计算的能力，而EBT的梯度下降优化范式天然支持以计算换性能。

**跨任务泛化。** 尽管EBT的预训练困惑度略高于Transformer++（33.43 vs 31.36），但在GSM8K、BigBench Math QA、BigBench Dyck等下游任务上，EBT的困惑度均更低（Table 3）。例如在GSM8K上，EBT达到43.3，而Transformer++为49.6，差距达6.3点。这表明EBT学到的能量函数具有更好的泛化性质——预训练时看似“浪费”计算在优化过程中，实际上塑造了更平滑、更可泛化的能量景观。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_ZBj3Qp1bYg/figures/012_Table_3.jpg]]
*Table 3: Language Model Task Generalization Comparison. We conduct experiments aimed at demonstrating the generalization of EBTs. Despite having slightly higher pretraining perplexity, EBTs often achieve lower perplexity on downstream tasks than the Transformer++, indicating better generalization. All models are trained with the same amount of data and parameters, but because EBTs at the current scale are less FLOP efficient (see Figure 5b), they used more FLOPs for this experiment. BB stands for BigBench*

**图像降噪与分类。** 在图像降噪任务上，EBT仅需DiT（Peebles & Xie, 2023）1%的前向次数即可达到同等或更高的PSNR：分布内数据上EBT为27.25 dB，DiT为26.58 dB；分布外噪声上差距急剧扩大，EBT为23.29 dB，DiT仅为19.56 dB（Table 4）。在图像分类的线性探测评估中，EBT的Top-1准确率达到5.32%，而DiT仅为0.31%，提升超过10倍。这进一步验证了能量基训练范式能学到更高质量的图像表征。

**算法推理（数独）。** 在数据受限的数独算法推理任务上，EBT在分布外测试集上达到29.7%的准确率，远超前馈Transformer的0.03%和现代RNN（Jolicoeur-Martineau, 2025）的17.7%（Table 5）。这一结果凸显了系统2思维在需要组合泛化的结构化推理任务上的关键作用。

### 系统2思维的消融分析

Table 2的系统2思维消融实验揭示了能量景观正则化技术对思维能力的因果贡献，以及探索-利用之间的本质权衡：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_ZBj3Qp1bYg/figures/008_Table_2.jpg]]
*Table 2: System 2 Thinking Ablations. All energy landscape regularization techniques described in Section 3.3 and their impact on System 2 Thinking performance, measured by percent perplexity improvement. Thinking Longer denotes more optimization steps and Self-Verification denotes optimizing many predictions and choosing the best. Removing regularization, such as Langevin Dynamics, results in less energy landscape exploration, which improves single path performance (thinking longer) at the expense of self-verification performance*

- **完整系统2配置**（随机步长 + 随机步数 + Langevin动力学 + 回放缓存）在“思考更久 + 自验证”组合下实现最佳困惑度改善18.7%。
- **移除Langevin动力学**后，单一优化路径（思考更久）的改善提升至17.2%，但自验证性能下降至17.0%。这表明噪声驱动的探索虽然略微损害单路径收敛质量，但对生成多样化的候选预测以进行有效验证至关重要。
- **移除随机步长**是最致命的：思维性能几乎无增益（思考更久-1.47%，自验证0.19%）。随机步长通过迫使模型在不同优化深度下都能生成合理预测，是塑造鲁棒能量景观的核心机制。
- **仅使用随机步长和随机步数**（无Langevin、无回放缓存）时，思考更久改善8.12%，自验证改善11.7%，已显著优于无任何正则化的基线（3.99% / 5.73%）。

这些消融结果揭示了系统2思维的两个子能力——动态计算分配与自验证——对能量景观正则化有不同需求，需要在探索和利用之间精细平衡。

### 分布外性能增益的规律

Figure 6展示了一个关键发现：EBT的思维增益随数据分布偏移程度的增大而线性增加。在分布偏移比（下游困惑度/预训练困惑度）接近1.0时，最大思维增益约12%；当偏移比升至约2.2时，增益扩大至约23%。这一趋势直接验证了论文的核心主张：系统2思维并非仅在分布内数据上有用，**越远离训练分布，思考的价值越大**。这为EBT在开放域、非平稳环境中的部署提供了理论支撑。

### 自验证能力的可扩展性

Figure 7b展示了自验证增益随训练计算量增加而提升的趋势：随着训练token数从约20亿增至约120亿，自验证带来的困惑度改善从4%-8%上升至12%-14%。这表明**验证能力本身是可学习的，且随模型规模和训练量增长而涌现**，并非简单的集成效应。这一发现为大规模EBT的推理能力提供了乐观预期。

### 失败模式与计算效率权衡

尽管EBT在多个维度上展现出优势，但存在不可忽视的效率瓶颈。由于训练时需要反向传播穿过整个梯度下降优化链（需要二阶梯度/Hessian-向量积），在使用两步优化时，EBT的FLOPs开销约为同参数Transformer++的6.66倍（Figure 5b）。这意味着在等FLOPs比较下，EBT的缩放优势会被部分抵消。论文明确指出，在当前实现下，EBT的FLOP效率较低，限制了短期内的直接应用。

训练稳定性是另一个实际挑战。系统2配置对优化步长、噪声幅度、随机步数范围等超参数敏感，需要仔细调参。在高度多模态分布（如无条件文本到图像生成）上，能量最小化倾向于捕捉单一模式，可能导致模式坍塌问题。此外，当前实验规模限于约400M参数的中等模型，在数十亿参数规模上的定性表现仍有待验证。

## 定位与知识库关联

### 核心瓶颈与设计动机

当前深度学习模型普遍缺乏**系统2思维能力**——即动态分配计算资源（Facet 1）与显式预测验证（Facet 2）的能力。现有推理方法存在三类根本性局限：其一，基于监督训练的验证器或可验证奖励方法（如数学推理中的验证器训练）依赖昂贵的人工标注或特定任务结构，无法通过无监督学习自然涌现通用思考能力；其二，扩散模型虽可在推理时通过增加去噪步数动态分配计算（如 **DiT**，Peebles & Xie, 2023），但其训练目标并非学习显式验证函数，缺乏对预测质量的标量评判机制；其三，标准自回归Transformer（如 **Transformer++**，基于Llama2架构与Chinchilla缩放法则，Touvron et al., 2023）的预测过程是单步前馈的，推理时计算量固定，无法根据输入难度自适应调节。

EBT的核心洞察在于将“验证比生成容易”这一直觉形式化为可学习的能量函数：训练一个显式能量基模型（EBM）作为验证器，学习输入与候选预测之间的兼容性（能量标量），并将预测重新定义为在能量景观上的梯度下降优化。这一设计使生成与验证统一在单一可学习函数内，模型通过迭代能量最小化自发学会“思考”，无需任何监督式推理训练。

### 方法谱系定位

**与自回归Transformer的关系**：EBT的自回归变体在架构上采用与GPT-style因果解码器相同的Transformer骨干，但预测机制发生根本性改变。标准自回归Transformer通过前馈网络直接输出下一个token的概率分布，训练仅需一阶梯度；EBT则学习能量函数 $E_\theta(x, \hat{y})$，通过梯度下降 $\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_\theta(x, \hat{y}_i)$ 隐式生成预测分布，训练需反向传播穿过整个优化链，涉及二阶梯度/Hessian-向量积计算（Algorithm 1）。在推理时，EBT可通过增加梯度下降步数实现“更长时间思考”（Thinking Longer），并通过生成多个候选并选择能量最低者实现“自验证”（Self-Verification），这是Transformer++无法做到的——Figure 7a证实Transformer++无法通过增加前向次数改善困惑度，而EBT可提升最高29%。

**与扩散模型的关系**：DiT（Peebles & Xie, 2023）与EBT在推理时动态分配计算的机制上具有表面相似性——两者均可通过增加推理步数提升质量。但本质差异在于：扩散模型学习的是逐步去噪的生成过程，其训练目标并非显式验证函数；EBT学习的是能量标量函数，每一步梯度下降都在显式评估当前预测与输入的兼容性。这使EBT在图像降噪任务上仅需DiT 1%的前向次数即可达到同等或更高PSNR（Table 4），且PSNR随前向次数增加的提升速率更快（Figure B.6）。在图像分类的线性探测评估中，EBT的Top-1准确率达5.32%，而DiT仅0.31%，表明EBT学到了更优的图像表征。

**与RNN的关系**：近期RNN架构（如 **Modern RNN**，Jolicoeur-Martineau, 2025）虽在效率上有所改进，但本质上仍属单步前馈预测，缺乏动态计算分配与显式验证机制。在数独OOD测试集上，前馈Transformer准确率仅0.03%，RNN为0.00%，而EBT达29.7%（Table 5），体现了系统2思维在算法推理任务上的显著优势。

### 关键设计要素与消融证据

EBT的系统2思维能力依赖于能量景观正则化技术的精心配置。Table 2的消融实验揭示了各组件的作用与权衡：

- **随机化步长**是最关键的组件：移除后思维性能几乎无增益（Thinking Longer为-1.47%，Self-Verification为0.19%），表明确定性优化路径无法有效探索能量景观。
- **Langevin动力学**（$\hat{y}_{i+1} = \hat{y}_i - \alpha \nabla_{\hat{y}_i} E_\theta(x, \hat{y}_i) + \eta_i, \eta_i \sim \mathcal{N}(0, \sigma)$）体现了探索-利用权衡：移除后单一优化路径的困惑度改善提升至17.2%，但自验证性能下降至17.0%，因为缺乏噪声注入使多条优化路径趋同，验证收益降低。
- **完整系统2配置**（随机步长+随机步数+Langevin+回放缓存）在延长思维与自验证结合时实现最佳困惑度改善18.7%。

### 适用边界与局限

**计算效率瓶颈**：当前EBT的FLOP效率较低——预训练使用两步优化时，计算开销约为同参数标准Transformer的6.66倍。这是二阶梯度训练的内在代价，限制了短期内的实际应用。实验规模限于中等模型（最大约400M参数），尚未验证在数十亿参数规模上的表现与定性差异。

**训练稳定性**：EBT对优化步长、噪声幅度等超参数敏感，尤其在完整系统2配置下需仔细调参。能量景观的平滑性与收敛行为缺乏理论保证。

**模态坍塌风险**：在处理高度多模态分布（如无条件文本到图像生成）时，能量最小化倾向于捕捉单一模式，可能存在模式坍塌问题。当前EBT的成功主要展现在条件预测任务（语言建模、图像降噪、数独求解）上。

**架构兼容性**：EBT的预测机制与现有基础模型（如Llama系列）不兼容，无法利用预训练权重初始化，需从零开始训练。

### 开放问题

1. **训练效率优化**：能否通过JAX等框架的HVP（Hessian-向量积）优化将EBT的训练效率提升至接近前馈模型的水平？这是决定该方法能否被广泛采用的关键工程问题。

2. **推理算法扩展**：EBT的思维算法目前基于简单的梯度下降与Best-of-N验证，是否可以与蒙特卡洛树搜索或Hamiltonian Monte Carlo等先进MCMC采样器结合，进一步提升推理多样性与质量？

3. **多模态统一框架**：单一能量标量天然适合作为多模态对齐信号，如何将EBT扩展到多模态统一框架，利用能量函数对齐文本、图像、视频等多种模态？

4. **大规模预训练的相变行为**：在大规模预训练（如Llama3的15T token量级）下，EBT的自验证能力和思维增益是否会出现相变？Figure 7b已显示验证收益随训练规模增长而提升（从4%-8%增至12%-14%），这一趋势是否持续？

5. **快慢系统协同**：是否可以将EBT作为系统2验证器与轻量系统1模型（如标准自回归Transformer）结合，实现“快慢结合”的协同推理——系统1快速生成候选，系统2进行能量验证与精炼？

6. **连续域世界模型**：在视频预测等连续域任务中，EBT的缩放规律是否持续优于前馈模型，并展现出更强的世界模型能力？这关系到EBT能否成为通用预测架构的基础。

## 原文 PDF

![[paperPDFs/ICLR_2026/Energy_Based_Transformers_are_Scalable_Learners_and_Thinkers.pdf]]

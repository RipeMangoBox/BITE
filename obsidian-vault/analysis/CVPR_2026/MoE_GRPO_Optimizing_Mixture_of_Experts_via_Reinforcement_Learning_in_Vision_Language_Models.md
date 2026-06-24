---
title: "MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoE_GRPO_Optimizing_Mixture_of_Experts_via_Reinforcement_Learning_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- MG
- MoE-GRPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 专家选择策略（路由机制）。通过强化学习（GRPO）将其作为序列决策问题进行随机探索与优化，能有效解锁多样化、奖励对齐的专家激活模式。
primary_logic: 将专家选择建模为序列决策问题，利用Group Relative Policy Optimization (GRPO) 进行优化，并通过模态感知路由器引导机制约束搜索空间，实现稳定高效的路由策略学习。
claims:
- MoE-GRPO 在多模态理解基准上一致超越标准 Top-K 路由及其变体（Det-FT 和 Stoch-FT）。
- 模态感知路由器引导机制能抑制对低频激活专家的探索，显著提升训练效率与稳定性。
- MoE-GRPO 提升了专家选择的多样性（熵增）和任务级别的专家特化程度（JS散度增加）。
- "多模态理解基准（图像与视频） 上 平均准确率（Average Accuracy, excl. MME） = InternVL3.5+MoE-GRPO: 56.0"
---

# MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models

> [!tip] 核心洞察
> 将专家选择建模为序列决策问题，利用Group Relative Policy Optimization (GRPO) 进行优化，并通过模态感知路由器引导机制约束搜索空间，实现稳定高效的路由策略学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoE-GRPO：通过强化学习优化视觉语言模型中的混合专家路由 |
| 英文题名 | MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.24984) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoE-GRPO |
| Dataset | 跨数据集评估（Cross-dataset Evaluation）, 领域泛化（Domain Generalization） |

> [!tip] 效果简介
> - 多模态理解基准（图像与视频） 上，平均准确率（Average Accuracy, excl. MME） InternVL3.5+MoE-GRPO: 56.0 vs InternVL3.5+Det-FT: 54.0 (+2.0)。
> - 跨数据集评估（Cross-dataset Evaluation） 上，平均准确率（Average Accuracy） CLIP-MoE+MoE-GRPO: 71.9 vs CLIP-MoE+Det-FT: 68.8 (+3.1)。
> - 领域泛化（Domain Generalization） 上，平均准确率（Average Accuracy） CLIP-MoE+MoE-GRPO: 67.5 vs CLIP-MoE+Det-FT: 66.0 (+1.5)。

## 概述

视觉语言模型（VLMs）中广泛采用的混合专家（MoE）架构虽能以较低的计算代价扩展模型容量，但其标准的确定性 Top‑K 路由策略构成了一个被长期忽视的瓶颈：路由器基于门控分数硬性选择激活专家，使得专家组合的探索空间被极度压缩，模型容易过度依赖少数专家并忽略更优的路由配置。本文提出 **MoE‑GRPO**，将专家选择重新建模为序列决策问题，并利用**组相对策略优化（Group Relative Policy Optimization, GRPO）** 进行随机探索与策略优化，从根本上解锁多样化的专家激活模式。

MoE‑GRPO 的核心贡献体现在三个层面。在**方法层面**，它通过双目标联合训练——Token‑GRPO 优化生成质量、Gate‑GRPO 直接精调门控网络——实现端到端的路由策略学习；同时引入**模态感知路由器引导**机制，根据模态激活频率屏蔽不相关专家，将搜索空间约束在有效子集内，显著提升训练效率与稳定性。在**实验层面**，MoE‑GRPO 在多模态理解基准上平均准确率较标准 Top‑K 路由提升 **2.0%**（Table 1），在跨数据集和领域泛化任务上分别提升 **3.1%** 和 **1.5%**（Table 2, Table 3），且与负载均衡损失互为补充。在**分析层面**，MoE‑GRPO 将路由分布的熵从 1.05 提升至 1.82，并将不同任务间的平均 JS 散度从 0.06 增大到 0.20，证实其有效缓解了专家过拟合，同时实现了任务级别的专家特化（Fig. 4, Fig. 5）。

在方法谱系中，MoE‑GRPO 区别于传统的**确定性 Top‑K 路由**（如 InternVL3.5 + Det‑FT）以及基于高斯噪声或多项分布采样的**模态无关随机路由**（Stoch‑FT‑Noise, Stoch‑FT‑Multi），其本质差异在于利用可验证的奖励信号（accuracy‑based binary reward）驱动探索，而非依赖无引导的扰动。与 **Expert Choice routing**（Zhou et al., NeurIPS 2022）和 **Optimal Transport routing**（Clark et al., ICML 2022）等现有路由方法相比，MoE‑GRPO 在保持训练兼容性的同时取得了更优性能（Table 7）。在 RL 算法选择上，GRPO 相比 DAPO 和 SAPO 在路由优化场景中表现出更好的稳定性（Table 6）。

目前 MoE‑GRPO 的主要局限在于：GRPO 框架需并行采样多条滚动轨迹，训练计算开销高于确定性路由；模态感知引导依赖超参数 P，跨数据集迁移时可能需要手动调节；且现有实验集中在 InternVL3.5‑1B 架构，向更大规模模型或不同 MoE 架构的扩展性仍有待验证。

## 背景与动机

### 混合专家模型的路由困境

混合专家（Mixture-of-Experts, MoE）架构已成为扩展视觉语言模型（VLM）容量的核心技术路径。其核心思想是将前馈网络（FFN）拆分为多个并行的“专家”子网络，每个 token 仅激活其中的 K 个专家，从而在保持推理成本可控的前提下大幅提升模型参数量。以 **InternVL3.5**（Wang et al., arXiv 2025）为代表的主流 MoE-VLM 采用确定性 Top-K 路由：对于第 $l$ 层第 $t$ 个 token 的隐藏状态 $h_{t,l}$，门控网络计算所有专家的分配概率

$$g ^ { l } ( h _ { t , l } ) = \mathrm { s o f t m a x } ( \operatorname { l i n e a r } ( h _ { t , l } ) ) \in \mathbb { R } ^ { N },$$

然后硬性选取概率最高的 $K$ 个专家，输出加权和：

$$o _ { t , l } = \sum _ { k \in \mathrm { t o p } \cdot K ( g ^ { l } ( h _ { t , l } ) ) } g ^ { l } ( h _ { t , l } ) _ { k } \cdot e _ { k , l } ( h _ { t , l } ).$$

这种确定性选择机制虽然实现简单，却带来了一个根本性瓶颈：**路由策略的探索空间被严重压缩**。由于每个 token 始终被分配给固定的专家子集，模型在训练过程中无法探索其他专家组合的潜在收益，导致少数专家被过度激活，形成事实上的“专家过拟合”。这一问题在视觉语言任务中尤为突出——不同模态（图像、文本）和不同任务类型对专家的需求存在显著差异，确定性路由无法自适应地发现和利用这种异质性。

### 现有改进路径的局限

为缓解上述问题，研究者从两个方向进行了尝试：

**（1）随机化路由。** 通过引入随机扰动来增加专家选择的多样性，例如基于多项分布采样的 **Stoch-FT-Multi** 或基于高斯噪声的 **Stoch-FT-Noise**。这些方法虽然打破了确定性选择的刚性约束，但其随机性完全与任务目标无关——它们无法区分哪些专家组合对当前输入是有利的，哪些是无效的。因此，随机探索的效率低下，且可能引入噪声干扰模型收敛。

**（2）替代路由策略。** 如 **Expert Choice routing**（Zhou et al., NeurIPS 2022）让专家主动选择 token，或 **Optimal Transport routing**（Clark et al., ICML 2022）通过最优传输理论平衡专家负载。这些方法在特定场景下有效，但本质上仍是基于启发式规则的设计，未将路由策略与任务性能直接对齐。

### 核心动机：将路由建模为序列决策问题

本文的核心洞察在于：**专家选择本质上是一个序列决策问题**。对于给定的输入（图像/视频 + 问题），模型需要在每一层为每个 token 选择激活的专家子集，这些选择共同决定了最终的预测质量。这一视角自然引出了强化学习（RL）的适用性——通过定义与任务正确性直接挂钩的奖励信号，RL 可以系统性地探索专家组合空间，并将探索方向引导至高回报区域。

然而，直接将 RL 应用于 MoE 路由面临两个关键挑战：

1. **探索空间的组合爆炸**：$N$ 个专家中选 $K$ 个的组合数随层数和序列长度指数增长，无约束的随机探索将导致训练效率极低。
2. **模态无关探索的盲目性**：视觉 token 和文本 token 对专家的偏好存在天然差异，忽略这种差异的随机探索会浪费大量计算资源在无效的专家组合上。

针对上述挑战，**MoE-GRPO** 提出了一套完整的解决方案：将专家选择策略的优化纳入 Group Relative Policy Optimization（GRPO）框架，并通过模态感知路由器引导机制将探索范围约束在模态相关的专家子集内，从而实现高效、稳定且奖励对齐的路由策略学习。

## 核心创新

MoE-GRPO 的核心创新在于将视觉语言模型中混合专家（MoE）的路由策略学习重新定义为**序列决策问题**，并引入强化学习框架进行优化，从而突破确定性 Top-K 路由对专家组合探索空间的限制。具体而言，该方法在以下三个维度上实现了关键性突破：

### 从确定性选择到随机探索与策略优化

传统 MoE 的 Top-K 路由机制根据门控分数**确定性**地选取专家（Eq. 2），这种贪婪策略导致模型过度依赖少数高频专家，形成专家过拟合，忽略了大量潜在更优的路由组合。MoE-GRPO 将这一过程转化为随机探索问题：通过旧门控网络 $g_{\text{old}}$ 并行采样 $G$ 组专家路由策略 $\{E^i\}_{i=1}^G$，每组策略覆盖所有层和所有 token 的专家选择，从而将动作空间从单一的 token 生成扩展到包含专家路由决策的联合空间。

在此基础上，MoE-GRPO 采用 **Group Relative Policy Optimization (GRPO)** 对专家选择策略进行优化。与传统 GRPO 不同，MoE-GRPO 不依赖参考策略或 KL 散度正则项，而是直接使用基于正确性的二元奖励信号（正确为 1，错误为 0）计算组内相对优势 $\hat{A}^i$，引导模型向高回报的路由策略方向更新。这一设计使模型能够自主探索并锁定奖励对齐的专家激活模式，而非被限制在预设的确定性路径中。

### 双目标协同优化的训练范式

MoE-GRPO 提出了 **Token-GRPO** 与 **Gate-GRPO** 两个子目标的联合优化框架，分别对应生成质量与路由决策两个层面的提升：

- **Token-GRPO**（Eq. 4）：在给定采样专家路由 $E^i$ 的条件下，优化 token 级别的生成质量。其核心是在固定路由策略下最大化正确输出的概率，确保模型在不同专家组合下均能保持生成能力。
- **Gate-GRPO**（Eq. 5）：逐层优化门控网络本身，直接调整专家选择的概率分布。通过使门控网络对产生高回报的专家分配更高概率，Gate-GRPO 从源头上改进路由决策的质量。

两者的联合目标函数 $\mathcal{L}_{\text{MoE-GRPO}} = \mathcal{L}_{\text{Token-GRPO}} + \mathcal{L}_{\text{Gate-GRPO}}$（Eq. 6）实现了端到端的生成质量与路由策略协同优化。消融实验（Table 4）证实了这一双目标设计的必要性：单独使用 Token-GRPO 训练会导致平均准确率下降 1.8%，表明仅优化 token 生成而忽略路由策略本身无法充分发挥 MoE 架构的潜力。

### 模态感知路由器引导：约束探索空间以提升效率与稳定性

直接对全量专家空间进行随机探索面临搜索空间过大、训练不稳定等问题。MoE-GRPO 引入了**模态感知路由器引导**机制，通过预统计视觉和文本模态对各专家的选择频率，计算每个专家的模态感知分数：

$$\hat{s}_v(e_i) = \frac{s_v(e_i)}{s_v(e_i) + s_t(e_i)}, \quad \hat{s}_t(e_i) = \frac{s_t(e_i)}{s_v(e_i) + s_t(e_i)}$$

其中 $s_v(e_i)$ 和 $s_t(e_i)$ 分别为视觉和文本 token 对专家 $e_i$ 的归一化选择计数。在训练过程中，根据当前输入模态，将对应模态感知分数最低的 $P\%$ 专家的门控分数设为 $-\infty$，从而将探索范围约束在模态相关的专家子集内。

这一机制的效果在消融实验中得到了充分验证（Table 5）：相比模态无关的高斯噪声扰动和多项分布采样基线，模态感知引导分别带来 1.5% 和 0.9% 的性能提升。更重要的是，训练曲线（Figure 3）显示，模态感知引导下的奖励均值收敛更快、标准差波动更小，显著提升了训练效率与稳定性。这证明了将先验知识注入探索空间约束是平衡探索广度与训练可行性的有效手段。

## 整体框架

MoE-GRPO 将混合专家（MoE）路由策略的优化重新建模为一个序列决策问题，并通过强化学习进行求解。其核心流程包含三个协同模块：**滚动采样模块（Rollout Module）**、**Token-GRPO 损失** 和 **Gate-GRPO 损失**，并在探索过程中引入**模态感知路由器引导**以约束搜索空间、提升训练稳定性。

### 流程概览

给定多模态输入 $x$（图像/视频与问题），整体框架的工作流如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of MoE-GRPO. Given an input image (or video) and a question, denoted as x, the rollout module*

1. **滚动采样**：旧门控网络 $g_{\text{old}}$ 基于当前的门控分数，通过多项分布采样生成 $G$ 组不同的专家路由策略 $\{E^i\}_{i=1}^G$。每组策略指定了所有层、所有 token 的专家选择。
2. **序列生成与奖励计算**：在每组采样的专家分配 $E^i$ 下，模型生成输出序列 $y^i$，并根据答案正确性获得二元奖励（正确为 1，错误为 0）。
3. **双重 GRPO 优化**：
   - **Token-GRPO**：在给定的专家路由下，优化 token 级别的生成质量，使模型在有利的路由策略下产生更准确的输出。
   - **Gate-GRPO**：逐层直接优化门控网络，增大产生高回报的专家分配的概率，从而精细化路由策略本身。
4. **模态感知引导**：在每次滚动采样前，根据专家对不同模态的历史激活频率计算模态感知分数，屏蔽底部 $P\%$ 的专家（将其门控分数设为 $-\infty$），将探索限制在模态相关的专家子集内。

### 关键设计决策

**无参考策略约束**：与常规 GRPO 引入 KL 散度项以约束学习策略向参考模型靠拢不同，MoE-GRPO 不依赖参考策略。这是因为门控网络的输出空间本身较小（每层 $N$ 个专家的离散选择），无需额外的分布正则化即可稳定探索。

**联合优化目标**：最终训练目标为 Token-GRPO 与 Gate-GRPO 的直接求和：
$$\mathcal{L}_{\text{MoE-GRPO}} = \mathcal{L}_{\text{Token-GRPO}} + \mathcal{L}_{\text{Gate-GRPO}}$$

这种设计实现了生成质量与路由策略的端到端协同优化——Token-GRPO 确保模型在给定路由下学会生成正确答案，Gate-GRPO 则引导门控网络主动发现更优的路由策略。

**探索空间约束的必要性**：若不加约束地随机探索所有 $N$ 个专家，搜索空间过大且包含大量模态无关的专家，会导致训练初期奖励信号稀疏、收敛缓慢。模态感知引导通过预统计的模态激活频率（视觉感知分数 $\hat{s}_v(e_i)$ 和文本感知分数 $\hat{s}_t(e_i)$）有效压缩了探索空间，使训练更稳定高效（见 Figure 3 训练曲线对比）。

## 核心模块与公式推导

### 3.1 问题形式化与预备知识

在标准的稀疏混合专家（MoE）Transformer 层中，对于第 $l$ 层的第 $t$ 个令牌 $h_{t,l}$，门控网络首先计算其对 $N$ 个专家的分配概率：

$$g^{l}(h_{t,l}) = \mathrm{softmax}(\operatorname{linear}(h_{t,l})) \in \mathbb{R}^{N} \quad \text{(Eq. 1)}$$

其中 $g^{l}(h_{t,l})$ 为门控分数向量，表示令牌对 $N$ 个专家的分配权重。随后，基于 Top-K 策略选取分数最高的 $K$ 个专家，计算前馈网络（FFN）的加权输出和：

$$o_{t,l} = \sum_{k \in \mathrm{top}\text{-}K(g^{l}(h_{t,l}))} g^{l}(h_{t,l})_{k} \cdot e_{k,l}(h_{t,l}) \quad \text{(Eq. 2)}$$

其中 $e_{k,l}(\cdot)$ 为第 $k$ 个专家的 FFN 输出。这一确定性 Top-K 选择机制构成了 MoE-GRPO 优化的起点——其核心瓶颈在于限制了专家组合的探索空间，导致模型过度依赖少数专家。

### 3.2 MoE-GRPO：强化学习驱动的路由优化

MoE-GRPO 将专家选择建模为序列决策问题，将动作空间扩展为覆盖所有令牌和所有层的专家路由决策，即 $[o_{1,1}, o_{1,2}, ..., o_{2,1}, o_{2,2}, ..., o_{T,L}]$。整体训练目标由两个协同优化的子目标构成：**Token-GRPO** 和 **Gate-GRPO**。

#### 滚动采样模块（Rollout Module）

给定输入 $\boldsymbol{x}$，旧门控网络 $g_{\mathrm{old}}$ 通过多项分布采样生成 $G$ 组随机专家路由策略 $\{\boldsymbol{E}^{i}\}_{i=1}^{G}$，每组策略对应一条完整的生成轨迹 $\boldsymbol{y}^{i} \sim \pi_{\mathrm{old}}(y|\boldsymbol{x}; \boldsymbol{E}^{i})$。奖励函数采用基于正确性的二元奖励：预测正确为 $1$，否则为 $0$。组内相对优势 $\hat{A}^{i}$ 通过对 $G$ 条轨迹的奖励进行标准化计算得到。

#### Token-GRPO 损失

Token-GRPO 在给定的采样专家分配下优化令牌级别的生成质量。其目标函数为：

$$\mathcal{L}_{\mathrm{Token-GRPO}} = \mathbb{E}_{\boldsymbol{x} \sim \mathcal{D}, \{\boldsymbol{E}^{i}\}_{i=1}^{G} \sim g_{\mathrm{old}}(E|\boldsymbol{x}), \boldsymbol{y}^{i} \sim \pi_{\mathrm{old}}(y|\boldsymbol{x}; \boldsymbol{E}^{i})} \left[ -\frac{1}{|\boldsymbol{y}^{i}|} \sum_{t=1}^{|\boldsymbol{y}^{i}|} \min\left[ r_{t}^{i} \hat{A}^{i}, \mathrm{clip}(r_{t}^{i}, 1-\epsilon, 1+\epsilon) \hat{A}^{i} \right] \right] \quad \text{(Eq. 4)}$$

其中 $r_{t}^{i}$ 为当前策略与旧策略在第 $t$ 个令牌上的概率比，$\epsilon$ 为裁剪阈值。该损失沿用了 GRPO 的裁剪机制，通过组内相对优势估计稳定策略更新。

#### Gate-GRPO 损失

Gate-GRPO 直接优化每层的门控网络，使其对产生高回报的专家分配更高的概率。其目标函数为：

$$\mathcal{L}_{\mathrm{Gate-GRPO}} = \mathbb{E}_{\boldsymbol{x} \sim \mathcal{D}, \{\boldsymbol{E}^{i}\}_{i=1}^{G} \sim g_{\mathrm{old}}(E|\boldsymbol{x}), \boldsymbol{y}^{i} \sim \pi_{\mathrm{old}}(y|\boldsymbol{x}; E^{i})} \left[ -\frac{1}{L|\boldsymbol{y}^{i}|} \sum_{l=1}^{L} \sum_{t=1}^{|\boldsymbol{y}^{i}|} \min\left[ \hat{r}_{t,l}^{i} \hat{A}^{i}, \mathrm{clip}(\hat{r}_{t,l}^{i}, 1-\epsilon, 1+\epsilon) \hat{A}^{i} \right] \right] \quad \text{(Eq. 5)}$$

其中 $\hat{r}_{t,l}^{i}$ 为第 $l$ 层门控网络在第 $t$ 个令牌上的概率比，$L$ 为总层数。与 Token-GRPO 不同，Gate-GRPO 在层维度上进行平均，直接调整门控网络的参数以优化专家选择策略。

#### 联合优化目标

MoE-GRPO 的最终训练目标为上述两个损失的简单相加：

$$\mathcal{L}_{\mathrm{MoE-GRPO}} = \mathcal{L}_{\mathrm{Token-GRPO}} + \mathcal{L}_{\mathrm{Gate-GRPO}} \quad \text{(Eq. 6)}$$

值得注意的是，与标准 GRPO 不同，MoE-GRPO 不依赖参考策略或 KL 散度正则项，简化了训练流程。

### 3.3 模态感知路由器引导

为抑制对低频激活专家的无效探索，MoE-GRPO 引入了模态感知路由器引导机制。首先，统计视觉和文本令牌对每个专家 $e_i$ 的选择计数，并计算归一化的模态感知分数：

$$\hat{s}_v(e_i) = \frac{s_v(e_i)}{s_v(e_i) + s_t(e_i)}, \quad \hat{s}_t(e_i) = \frac{s_t(e_i)}{s_v(e_i) + s_t(e_i)} \quad \text{(Sec. 3.3)}$$

其中 $s_v(e_i)$ 和 $s_t(e_i)$ 分别为视觉和文本令牌选择专家 $e_i$ 的归一化计数。基于这些分数，对于给定模态的输入，将底部 $P\%$ 专家的门控分数设为 $-\infty$，从而将探索空间约束在模态相关的专家子集内。在剩余搜索空间中，门控网络 $g_{\mathrm{old}}$ 根据调整后的门控分数通过多项分布采样 $K$ 个专家，生成 $G$ 条随机滚动策略。

## 实验与分析

### 主要结果

**多模态理解基准。** Table 1 报告了在主流多模态图像与视频理解基准上的对比结果。以 InternVL3.5 为骨干，MoE-GRPO 在激活 1.3B / 总参数量 2.9B 的配置下，取得了 **56.0** 的平均准确率（排除 MME），较确定性 Top-K 路由基线 InternVL3.5+Det-FT 的 54.0 提升了 **+2.0** 个百分点。这一增益在多个子基准上呈现出一致性，表明基于 GRPO 的随机探索与策略优化有效突破了确定性路由对专家组合空间的限制。

**跨数据集泛化与领域泛化。** 在 CLIP-MoE 架构上进行的少样本泛化实验进一步验证了方法的鲁棒性。Table 2 显示，在 ImageNet 16-shot 训练后跨 10 个目标数据集评估，CLIP-MoE+MoE-GRPO 的平均准确率达到 **71.9**，相比 Det-FT 的 68.8 提升 **+3.1**。Table 3 的领域泛化实验中，MoE-GRPO 同样将平均准确率从 66.0 提升至 **67.5**（+1.5），说明学习到的路由策略具备良好的分布外泛化能力。

### 消融实验

**Token-GRPO 与 Gate-GRPO 的协同效应。** Table 4 的消融揭示了两个损失组件的各自贡献：单独使用 Token-GRPO 会导致平均准确率下降 **1.8%**，而完整的 MoE-GRPO（Token-GRPO + Gate-GRPO）取得了最优性能。这验证了 Gate-GRPO 对专家选择策略直接优化的必要性——仅优化令牌生成而保持路由策略固定，无法充分释放 MoE 的潜力。

**模态感知路由器引导的关键作用。** Table 5 将模态感知引导与两种模态无关的随机路由机制进行了对比：高斯噪声扰动（Stoch-FT-Noise）和多项分布采样（Stoch-FT-Multi）。模态感知引导分别带来 **+1.5%** 和 **+0.9%** 的性能提升。Fig. 3 的训练曲线进一步显示，模态感知引导下奖励均值更高且标准差更小，表明通过屏蔽底部 P% 的低频激活专家，搜索空间被有效约束在模态相关的专家子集内，从而提升了训练效率与稳定性。

**与其他路由方法的对比。** Table 7 显示，MoE-GRPO 在性能上优于 Expert Choice 路由（Zhou et al., NeurIPS 2022）和 Optimal Transport 路由（Clark et al., ICML 2022）。此外，MoE-GRPO 与负载均衡损失（Load Balancing）互为补充，联合使用可带来 **+0.9%** 的额外提升，说明奖励驱动的路由优化与基于辅助损失的负载均衡可以协同工作。

**强化学习算法选择。** Table 6 对比了 GRPO 与 DAPO（Yu et al., arXiv 2025）、SAPO（Gao et al., arXiv 2025）在 MoE-GRPO 框架下的表现，GRPO 取得了最优结果，验证了组内相对优势估计在专家路由优化场景中的适用性。

### 路由行为分析

**专家利用的均衡化。** Fig. 4 展示了令牌级别的专家利用率分布。标准 Top-K 路由下，少数专家被过度激活，路由分布熵仅为 **1.05**；MoE-GRPO 将熵提升至 **1.82**，有效缓解了专家过拟合，促进了更均衡的专家利用。

**任务级专家特化。** Fig. 5 可视化了不同任务间的专家利用率差异。MoE-GRPO 将任务间的平均 JS 散度从 **0.06** 提升至 **0.20**，表明学习到的路由策略能够针对不同任务激活差异化的专家组合，实现了任务级别的专家特化。

**定性案例。** Fig. 6 提供了一个定性分析案例：基线 Det-FT 模型给出了错误预测，而 MoE-GRPO 学习到的专家选择策略通过激活一组不同的专家组合，成功纠正了预测结果。

### 局限性与失败模式

尽管 MoE-GRPO 在多个基准上表现出一致的增益，仍存在以下局限：

1. **训练计算开销。** 基于 GRPO 的框架需要并行采样 G 条滚动轨迹，相比确定性 Top-K 路由，训练计算成本更高。论文未提供具体的额外开销量化数据，此点需在实际部署中手动评估。
2. **超参数敏感性。** 模态感知引导依赖超参数 P（屏蔽底部专家的百分比），针对不同数据集或网络结构可能需要手动调节。论文未给出 P 的自适应选择策略。
3. **模型规模验证不足。** 当前实验集中在 InternVL3.5-1B 和 CLIP-MoE 架构上，对于数十亿参数级模型或 DeepSeek-MoE 等不同 MoE 架构的可扩展性尚未验证。

### 补充图表

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/003_Table_1.jpg]]
*Table 1: Results on multi-modal understanding benchmarks. # activated and # total denote the number of activated and total parameters. The last column reports the average accuracy across all benchmarks, excluding MME*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/004_Table_2.jpg]]
*Table 2: Results on cross-dataset evaluation. We train the model on the source ImageNet dataset for three epochs under the 16-shot setting and evaluate it on 10 target datasets*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/005_Table_3.jpg]]
*Table 3: Results of domain generalization. We train the model on the source ImageNet dataset for three epochs under the 16-shot setting and evaluate it on four out-of-domain target datasets*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/006_Table_4.jpg]]
*Table 4: Ablation studies on MoE-GRPO*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/007_Table_5.jpg]]
*Table 5: Ablation studies on modality-aware router guidance. We compare modality-aware router guidance with two modalityagnostic expert selection mechanisms, Gaussian noise and multinomial sampling*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/008_Table_6.jpg]]
*Table 6: Ablation studies on RL methods of MoE-GRPO*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/009_Table_7.jpg]]
*Table 7: Comparison with existing routing methods. MoE-GRPO achieves superior performance compared to Expert Choice [22] routing and Optimal Transport [64] routing. Moreover, it is complementary to the load-balancing (LB) objective used in Switch Transformers [7], and their combination leads to further performance improvements*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/010_Figure_3.jpg]]
*Figure 3: Training curves. (a) and (b) present the mean and standard deviation of the accuracy reward of MoE-GRPO, comparing our modality-aware router guidance with the modality-agnostic (multi.) expert selection baseline*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/011_Figure_4.jpg]]
*Figure 4: Token-level expert utilization ratio. Under MoE-GRPO, expert activation is more evenly distributed across the token sequence, resulting in more balanced expert utilization*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/013_Figure_5.jpg]]
*Figure 5: Expert utilization ratio (x-axis) for each task (y-axis). MoE-GRPO enhances task-level expert specialization by inducing more diverse expert activation patterns across tasks*

![[assets/figures/papers/paper_list_l2659_https_arxiv_org_abs_2603_24984/figures/012_Figure_6.jpg]]
*Figure 6: A qualitative example and its routing probabilities. (a) illustrates the expert routing probabilities, with the selected experts highlighted in red boxes. (b) presents a qualitative example demonstrating that the learned expert selection policy of MoE-GRPO yields a correct prediction, whereas the baseline Det-FT model produces an incorrect one*

## 方法谱系与知识库定位

### 1. 与现有 MoE 路由方法的关系

MoE-GRPO 的核心贡献在于将专家选择从**确定性静态分配**转变为**基于强化学习的序列决策优化**，这使其在方法谱系中与现有路由策略形成清晰的分层关系。

**确定性 Top-K 路由及其变体**构成最直接的基线阵营。标准 Top-K 路由（如 **InternVL3.5** (Wang et al., arXiv 2025) 所采用的方案）根据门控分数 $g^l(h_{t,l})$ 直接选取 top-K 专家，其本质瓶颈在于**确定性的选择机制限制了专家组合的探索空间**，导致模型过度依赖少数高频专家而过拟合。MoE-GRPO 的两个随机变体——**Stoch-FT-Multi**（基于多项分布采样）和 **Stoch-FT-Noise**（基于高斯噪声扰动）——虽然引入了随机性，但因缺乏模态感知的探索约束和策略优化机制，在训练稳定性和最终性能上均显著弱于 MoE-GRPO（见 Table 5）。

**基于全局分配的路由方法**代表了另一种设计哲学。**Expert Choice routing** (Zhou et al., NeurIPS 2022) 让专家主动选择 token，而 **Optimal Transport routing** (Clark et al., ICML 2022) 通过最优传输理论寻求全局最优的 token-专家匹配。Table 7 的对比表明，MoE-GRPO 在性能上优于这两种方法，且其基于 token 级和层级联合优化的 GRPO 框架与负载均衡损失（Load Balancing）**互为补充**，联合使用可带来 0.9% 的额外提升。这说明 MoE-GRPO 并非要替代负载均衡机制，而是在探索-利用维度上提供正交的优化信号。

### 2. 与强化学习策略优化算法的关系

MoE-GRPO 在 RL 算法选择上进行了审慎的消融。Table 6 对比了 **GRPO**、**DAPO** (Yu et al., arXiv 2025) 和 **SAPO** (Gao et al., arXiv 2025) 三种策略优化算法在 MoE 路由场景下的表现，结果显示 GRPO 在该任务上具有优势。值得注意的是，MoE-GRPO 对标准 GRPO 做了关键简化：**不依赖参考策略（reference policy）或 KL 散度正则项**。这一设计选择源于专家路由优化与语言生成任务的根本差异——路由策略的探索不需要被约束在某个预训练分布的邻域内，反而需要充分的探索自由度来发现更优的专家组合。

### 3. 适用边界与关键约束

MoE-GRPO 的有效性建立在以下前提之上：

- **多模态输入场景**：模态感知路由器引导机制依赖视觉和文本模态的专家激活频率统计（$\hat{s}_v(e_i)$ 和 $\hat{s}_t(e_i)$），这要求训练数据包含明确的多模态信号。对于纯文本或纯视觉任务，该引导机制的优势可能会减弱，需要手动验证。

- **可验证的奖励信号**：当前框架采用基于正确性的二元奖励（accuracy-based binary reward），适用于具有明确答案的判别和生成任务。对于开放式生成或需要细粒度质量评估的任务，奖励信号的稀疏性可能成为瓶颈。

- **计算开销与采样组数 G 的权衡**：GRPO 需要并行采样 G 条滚动轨迹，相比确定性 Top-K 路由增加了训练计算开销。G 值过小会削弱探索的多样性，过大则显著增加计算成本。论文未系统探讨 G 的最优取值及其在不同规模模型下的敏感性。

### 4. 已知局限与开放问题

**已验证的局限**：

1. **训练计算开销**：基于 GRPO 的强化学习框架需要并行采样多条滚动轨迹，相比标准确定性 Top-K 路由，训练阶段的算力需求更高。这在实际部署中可能限制其在资源受限场景下的应用。

2. **超参数 P 的敏感性**：模态感知路由器引导依赖超参数 P（屏蔽底部专家的百分比），针对不同数据集或网络结构可能需要手动调节以获得最佳性能。论文未提供 P 的自动调优策略或跨数据集的鲁棒性分析。

3. **模型规模验证不足**：当前实验主要集中在 InternVL3.5-1B 架构上，对于扩展到更大规模的模型（如 7B、13B）或不同的 MoE 架构（如 DeepSeek-MoE）时的有效性尚未得到充分验证。

**待探索的开放问题**：

1. **大规模扩展的稳定性**：MoE-GRPO 在扩展到数十亿参数级别或包含数百个专家的 MoE 模型时，其性能与训练稳定性将如何变化？GRPO 的组内优势估计在专家数量急剧增加时是否仍能提供有效的梯度信号？

2. **新模态的零样本适应**：模态感知引导机制能否在不预先计算模态激活频率的情况下，自适应地处理音频、深度等全新模态？当前基于离线统计的引导策略在面对动态变化的模态组合时可能缺乏灵活性。

3. **奖励塑形与推理能力**：基于正确性的二元奖励信号对于复杂的 Chain-of-Thought 推理任务是否足够？是否需要引入过程奖励模型（Process Reward Model）或更细粒度的奖励塑形策略来进一步提升推理能力？

4. **与 MoE 架构设计的协同**：当前工作将 MoE 架构（专家数量、Top-K 值、专家容量等）视为固定配置，未来可探索 GRPO 优化与架构搜索的联合设计，实现路由策略与模型结构的协同进化。

## 原文 PDF

![[paperPDFs/CVPR_2026/MoE_GRPO_Optimizing_Mixture_of_Experts_via_Reinforcement_Learning_in_Vision_Language_Models.pdf]]

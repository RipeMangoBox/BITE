---
title: "Unlocking the Essence of Beauty: Advanced Aesthetic Reasoning with Relative-Absolute Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unlocking_the_Essence_of_Beauty_Advanced_Aesthetic_Reasoning_with_Relative_Absolute_Policy_Optimization.pdf
project_link: null
code_link: https://github.com/ssssmark/AesR1
openreview_forum_id: or3ZukbrKw
aliases:
- AR
- UEBAARRAPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过AesCoT管道生成多维度美学推理的冷启动数据，并结合RAPO算法中的绝对误差奖励与相对排名奖励联合优化，促使多模态大语言模型学会生成结构化推理并精确校准分数与排序。"
primary_logic: "人类审美判断兼具绝对质量评估和相对比较偏好；将这两种偏好建模为RL奖励并进行联合优化，可以显著提升模型在图像美学评价上的准确性、可解释性和泛化能力。"
claims:
- "Aes-R1将骨干模型的平均PLCC/SRCC提高了47.9%/34.8%。"
- "RAPO通过联合优化绝对误差奖励和相对排名奖励，在所有消融实验中表现最优。"
- "适度的SFT冷启动（1个epoch）后接RAPO可以获得最佳性能，过度SFT会降低熵并削弱RL增益。"
- "Five benchmarks average (TAD66K, AVA, FLICKR-AES, PARA, AADB) 上 PLCC = 0.6337"
---

# Unlocking the Essence of Beauty: Advanced Aesthetic Reasoning with Relative-Absolute Policy Optimization

> [!tip] 核心洞察
> 人类审美判断兼具绝对质量评估和相对比较偏好；将这两种偏好建模为RL奖励并进行联合优化，可以显著提升模型在图像美学评价上的准确性、可解释性和泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 解锁美的本质：基于相对-绝对策略优化的高级美学推理 |
| 英文题名 | Unlocking the Essence of Beauty: Advanced Aesthetic Reasoning with Relative-Absolute Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=or3ZukbrKw) · [GitHub](https://github.com/ssssmark/AesR1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Aes-R1 |
| Dataset | Five benchmarks average (TAD66K, AVA, FLICKR-AES, PARA, AADB), Five benchmarks average, AVA (in-domain) |

> [!tip] 效果简介
> - Five benchmarks average (TAD66K, AVA, FLICKR-AES, PARA, AADB) 上，PLCC 为 0.6337，对比 0.4285 (backbone Qwen2.5-VL-7B)，变化 +47.9% relative。
> - Five benchmarks average 上，SRCC 为 0.6186，对比 0.4589 (backbone Qwen2.5-VL-7B)，变化 +34.8% relative。
> - AVA (in-domain) 上，PLCC 为 0.6702，对比 0.5964 (Q-Insight)，变化 +0.0738。

## 概要

图像美学评估长期面临一个核心瓶颈：现有方法缺乏高质量的美学推理数据，而直接应用强化学习则遭遇双重挑战——无法有效激活模型的美学推理模式，且奖励信号难以同时校准绝对分数与保持相对排序一致性。这导致模型的可解释性差、分数分布对齐不准。

针对上述问题，本文提出 **Aes-R1**，其核心洞察在于：人类审美判断天然兼具绝对质量评估与相对比较偏好两种机制。将这两种偏好建模为强化学习的奖励信号并进行联合优化，能够显著提升多模态大语言模型在图像美学评价上的准确性、可解释性与泛化能力。

Aes-R1 的关键技术路径包含两个可控环节：

- **AesCoT 数据管道**：自动构建多维度美学推理的冷启动数据，沿色彩、曝光、构图等五个维度生成结构化解释与分数，并通过自动检测与人工审核过滤评分泄露、推理不一致和事实错误。
- **RAPO 相对-绝对策略优化**：在冷启动监督微调之后，以联合奖励函数驱动强化学习——其中**相对排名奖励**基于成对排序一致性（FRank），**绝对误差奖励**采用高斯形函数校准预测分数至真实 MOS。

实验表明，Aes-R1 将骨干模型 Qwen2.5-VL-7B 在五个基准数据集上的平均 PLCC 从 0.4285 提升至 0.6337（相对提升 47.9%），平均 SRCC 从 0.4589 提升至 0.6186（相对提升 34.8%）。消融研究进一步确认：联合误差-排名奖励在所有奖励组合中表现最优；适度的 SFT 冷启动（1 个 epoch）后接 RAPO 可获得最佳性能，过度 SFT 会降低熵并削弱强化学习的增益。

图像美学评估（Image Aesthetic Assessment, IAA）旨在量化图像的视觉美感，在图像检索、智能摄影和视觉内容推荐等领域具有广泛应用。然而，现有方法面临两个根本性瓶颈：

**瓶颈一：缺乏高质量的美学推理数据。** 传统IAA方法——无论是手工特征方法（如**NIQE**, Mittal et al., 2013; **BRISQUE**, Mittal et al., 2012）还是深度学习方法（如**NIMA**, Talebi & Milanfar, 2018; **MUSIQ**, Ke et al., 2021）——仅输出单一的数值分数，无法解释“为什么这张图美”。尽管多模态大语言模型（MLLM）的兴起为可解释的美学评估带来了可能，但现有MLLM方法（如**Q-Align**, Wu et al., 2023a; **DeQA-Score**, You et al., 2025）仍然依赖图像-分数对进行监督微调，缺乏结构化的美学推理数据作为训练支撑，导致模型的可解释性严重不足。

**瓶颈二：奖励信号的双重校准难题。** 直接应用强化学习（RL）训练MLLM进行美学评估面临两个相互交织的挑战：一方面，缺乏冷启动数据时，RL无法有效激活模型的美学推理模式，导致生成的解释质量低下；另一方面，人类审美判断天然包含两种偏好——对绝对质量分数的精确感知和对图像间相对优劣的比较偏好。现有RL方法要么仅使用绝对误差奖励（如**Q-Insight**, Li et al., 2025），要么仅使用相对排名奖励（如**VisualQuality-R1**, Wu et al., 2025），无法同时校准绝对分数精度和相对排序一致性，导致分数分布对齐不准。

**核心洞察：** 人类的审美判断兼具“这张图值几分”的绝对评估能力和“A比B更好看”的相对比较偏好。将这两种偏好建模为RL中的联合奖励信号并进行协同优化，有望显著提升模型在图像美学评价上的准确性、可解释性和泛化能力。

**本文动机：** 针对上述双重瓶颈，本文提出Aes-R1框架，核心包含两个创新组件：（1）**AesCoT数据管道**，自动构造包含五维度结构化推理的高质量美学数据，为模型提供冷启动能力；（2）**RAPO算法**，通过联合优化绝对误差奖励和相对排名奖励，使模型在生成可解释推理的同时精确校准分数与排序。实验表明，仅使用15K训练数据，Aes-R1即可将骨干模型（Qwen2.5-VL-7B）的平均PLCC/SRCC分别提升47.9%/34.8%（Table 1），验证了联合优化绝对与相对偏好的有效性。

## 核心方法与创新机理

Aes-R1 的核心创新围绕两个紧密耦合的 **changed slots** 展开，分别解决“美学推理能力缺失”和“奖励信号校准不足”的双重瓶颈。

### 创新一：AesCoT — 自动化的多维度美学推理数据构造

传统图像美学评估方法（无论是手工特征如 **NIQE** (Mittal et al., 2013)、**BRISQUE** (Mittal et al., 2012)，还是深度学习模型如 **NIMA** (Talebi & Milanfar, 2018)、**MUSIQ** (Ke et al., 2021)）仅输出单一分数，缺乏可解释的推理过程。即便是基于 MLLM 的 **Q-Align** (Wu et al., 2023a)、**Q-Insight** (Li et al., 2025) 等方法，其训练数据也仅由图像-分数对构成，未能激活模型的结构化审美推理模式。

Aes-R1 通过 **AesCoT 数据管道**（Figure 2）改变了这一局面。该管道以原始图像-分数对为起点，遮蔽连续美学分数后，驱动专家模型沿五个美学维度（如构图、色彩、光影等）生成思维链（Chain-of-Thought）评述，再经过自动检查与人工审核过滤掉分数泄露、推理-分数不匹配及事实错误，最终产出高质量的多模态美学推理数据。这些数据作为 **SFT 冷启动**的监督信号，使模型首次具备了生成结构化美学解释并输出校准分数的能力。

### 创新二：RAPO — 相对-绝对联合策略优化

现有 RL-based 方法在奖励设计上存在根本性局限：**VisualQuality-R1** (Wu et al., 2025) 仅使用排名奖励，**Q-Insight** 仅使用标量绝对误差奖励，二者均无法同时捕捉人类审美判断中“绝对质量评估”与“相对比较偏好”的双重特性。

RAPO 的核心突破在于**联合优化两种互补的奖励信号**：

- **相对排名奖励** $r_{rank}$：基于 FRank 框架，通过成对比较概率 $p_{ik}(\mathcal{T}_i, \mathcal{T}_j)$ 衡量预测排序与真实排序的一致性，确保模型具备精细的序数辨别能力。
- **绝对误差奖励** $r_{abs}$：采用高斯形函数 $\exp\left(-\frac{1}{2}\left(\frac{|o_{ik} - s_i|}{\sigma}\right)^2\right) + \epsilon$ 校准预测分数至真实 MOS，提供连续且精确的回归信号。

总奖励 $r = r_{rank} + r_{abs}$ 同时驱动策略优化，使梯度更新既受绝对分数约束的引导，又受成对排序一致性的校正。消融实验（Table 2）强有力地证明了这一设计的决定性作用：联合使用误差奖励和排名奖励在所有奖励组合中表现最优，平均 PLCC/SRCC 达到 0.6297/0.6102，显著优于单独使用任何一种奖励。

### 两阶段训练的协同效应

AesCoT 冷启动与 RAPO 并非孤立创新，二者存在关键的协同关系。实验表明（Table 3），适度的 SFT（1 个 epoch）初始化 RAPO 可获得最佳下游性能（平均 PLCC 0.6337，SRCC 0.6186），而跳过 SFT 直接进行端到端 RL 会导致模型生成质量低下的解释（如 Figure 6 中 AesR1-Zero 所示）；反之，过度 SFT（10 个 epochs）会降低策略熵，削弱后续 RL 的优化增益。这一发现揭示了“先教模型如何推理，再通过联合奖励精调其判断”这一两阶段范式的必要性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_or3ZukbrKw/figures/010_Figure_2.jpg]]
*Figure 2: Overview of AesCoT construction pipeline. Starting from original image-score pairs, we mask the continuous aesthetic score and prompt experts to produce CoT critiques along five aesthetic dimensions. Automated checks and human audits then remove any score leakage, reasoning–score mismatch, or factual errors, yielding high-quality, interpretable multimodal aesthetic reasoning data*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_or3ZukbrKw/figures/011_Figure_3.jpg]]
*Figure 3: The training pipeline of Relative Absolute Policy Optimization (RAPO). Given a batch of training images, the policy model generates multiple outputs for aesthetic rating questions. RAPO computes both pairwise ranking based relative reward and score regression error based absolute reward for each output, then optimizes the policy model to align with human aesthetic preferences*

Aes-R1 采用**冷启动监督微调 + 强化学习精调**的两阶段训练范式，整体流程由三个核心模块串联构成（图2、图3）：

1. **AesCoT 数据构造管道**：从原始图像-分数对出发，通过提示专家模型沿五个美学维度生成结构化思维链（CoT）评语，再经自动检查与人工审计过滤掉分数泄露、推理-分数不一致及事实错误，产出高质量多模态美学推理数据。
2. **SFT 冷启动**：在 AesCoT 数据上进行 1 个 epoch 的监督微调（损失函数为负对数似然，见公式 8），使模型初步具备生成结构化美学推理与分数预测的能力，同时维持较高的 token 熵值，为后续 RL 保留策略多样性。
3. **RAPO 强化学习**：以 SFT 冷启动模型为初始策略，采用相对-绝对策略优化进行 RL 训练。每一批训练图像经策略模型生成多条输出轨迹，RAPO 同时计算基于成对排序一致性的相对排名奖励 $r_{rank}$（公式 4）和基于分数回归误差的绝对误差奖励 $r_{abs}$（公式 6），二者相加构成总奖励 $r = r_{rank} + r_{abs}$（公式 7），并通过带 KL 惩罚的裁剪目标 $J_{RAPO}(\theta)$（公式 10）联合优化策略。

**输入输出流**：给定图像 $\mathcal{T}$ 和任务提示 $\mathcal{P}$，模型生成轨迹 $\tau = (c, s) \sim \pi_\theta(\cdot|\mathcal{T}, \mathcal{P})$，其中 $c$ 为多维度美学解释，$s$ 为整体美学分数。训练时，AesCoT 管道提供冷启动所需的图像-推理-分数三元组；RL 阶段仅需图像-分数对，奖励信号由 RAPO 的成对比较机制和绝对误差函数在线计算。

**关键设计决策**：RAPO 的核心创新在于将人类审美判断中的两种偏好——绝对质量评估（分数校准）和相对比较偏好（排序一致性）——同时建模为 RL 奖励信号。消融实验（Table 2）证实，联合使用误差奖励和排名奖励在所有奖励组合中表现最优（平均 PLCC/SRCC 达 0.6297/0.6102），显著优于仅用单一奖励或二元奖励的方案。此外，适度的 SFT 冷启动（1 epoch）是性能关键：无 SFT 直接 RL 虽能获得较高分数，但生成的解释质量差（Figure 6, AesR1-Zero）；过度 SFT（10 epochs）则导致熵急剧下降，削弱后续 RL 增益（Table 3）。

### 问题形式化

给定图像 $\mathcal{T}$ 和提示 $\mathcal{P}$（包含美学评分指令），模型需生成一条推理轨迹 $\tau = (c, s)$，其中 $c$ 为多维度美学解释，$s$ 为预测的连续美学分数。轨迹采样自策略模型 $\pi_\theta(\cdot | \mathcal{T}, \mathcal{P})$。优化的目标是最大化期望累积奖励：

$$\nabla_\theta \mathcal{I}(\theta) = \mathbb{E}_{\tau \sim \pi_\theta(\cdot | \mathcal{T}, \mathcal{P})} \left[ R(\tau) \sum_{t=1}^{T} \nabla_\theta \log \pi_\theta(a_t | \mathcal{T}, \mathcal{P}, a_{<t}) \right]$$

其中 $R(\tau)$ 为轨迹级奖励，$a_t$ 为第 $t$ 步生成的 token。

### AesCoT 数据构造管道

AesCoT 是首个自动化的美学推理数据构造管道（Figure 2），核心流程为：

1. **维度化推理生成**：从原始图像-分数对出发，屏蔽连续美学分数，引导专家模型沿五个美学维度（如构图、色彩、光影、主题、技术质量）生成 CoT 批判性分析。
2. **自动校验与过滤**：通过自动化检查移除分数泄露（score leakage）、推理与分数不一致、事实性错误等低质量样本。
3. **人工审计**：对自动过滤后的数据进行人工抽检，确保最终数据的高质量与可解释性。

该管道产出的数据 $\mathcal{D}_{CoT}$ 包含结构化美学解释 $c$ 与对应分数 $s$，为后续 SFT 冷启动提供基础。

### 冷启动监督微调

在 AesCoT 数据上进行监督微调，损失函数为标准负对数似然：

$$\mathcal{L}_{sft}(\theta) = \mathbb{E}_{(\mathcal{P}, \mathcal{T}, c, s) \sim \mathcal{D}_{CoT}} \left[ -\log \pi_\theta(c, s | \mathcal{P}, \mathcal{T}) \right]$$

此阶段使模型初步具备生成结构化美学推理与分数预测的能力。实验表明，仅需 **1 个 epoch** 的适度 SFT 即可为后续 RL 阶段提供最优初始化；过度 SFT（如 10 epochs）会导致策略熵急剧下降，削弱 RL 的优化增益（Table 3）。

### RAPO 奖励函数设计

RAPO 的核心创新在于联合优化相对排序一致性与绝对分数回归精度，总奖励为两项之和：

$$r = r_{rank} + r_{abs}$$

#### 相对排名奖励

基于 FRank 框架，首先定义成对比较概率。给定图像 $i$ 的预测分数 $o_{ik}$ 和图像 $j$ 的估计均值 $\mu_j$ 与方差 $\sigma_j^2$，图像 $i$ 被偏好的概率为：

$$p_{ik}(\mathcal{T}_i, \mathcal{T}_j) = \Phi\left( \frac{o_{ik} - \mu_j}{\sqrt{\sigma_i^2 + \sigma_j^2 + \gamma}} \right)$$

其中 $\Phi$ 为标准正态累积分布函数，$\gamma$ 为平滑项。相对排名奖励定义为与真实成对偏好 $p_c(\mathcal{T}_i, \mathcal{T}_j)$ 的 Bhattacharyya 系数均值：

$$r_{rank}(o_{ik}) = \frac{1}{N-1} \sum_{j \neq i} \sqrt{p_c(\mathcal{T}_i, \mathcal{T}_j) p_{ik}(\mathcal{T}_i, \mathcal{T}_j)} + \sqrt{(1 - p_c(\mathcal{T}_i, \mathcal{T}_j))(1 - p_{ik}(\mathcal{T}_i, \mathcal{T}_j))}$$

该奖励有界、连续、可微，直接对齐成对排序一致性。

#### 绝对误差奖励

采用高斯形奖励函数校准预测分数至真实 MOS $s_i$：

$$r_{abs}(o_{ik}) = \exp\left( -\frac{1}{2} \left( \frac{|o_{ik} - s_i|}{\sigma} \right)^2 \right) + \epsilon$$

其中 $\sigma$ 控制容差宽度，$\epsilon$ 为小常数防止零奖励。此连续信号相比二元奖励（$r_{binary} = \mathbf{1}_{|s_{pred} - s_{gt}| < \varepsilon}$）提供了更精细的梯度信息，是性能显著提升的关键因素之一（Table 2）。

### RAPO 策略优化目标

RAPO 采用 PPO 风格的裁剪目标，并引入 KL 散度惩罚以防止策略偏离参考模型 $\pi_{ref}$ 过远：

$$\mathcal{J}_{RAPO}(\theta) = \mathbb{E}_{k,t} \left[ \min\left( r_{k,t}(\theta) \hat{A}_{k,t}, \text{clip}(r_{k,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{k,t} \right) \right] - \beta D_{KL}(\pi_\theta \| \pi_{ref})$$

其中 $r_{k,t}(\theta) = \frac{\pi_\theta(a_t | \mathcal{T}, \mathcal{P}, a_{<t})}{\pi_{\theta_{old}}(a_t | \mathcal{T}, \mathcal{P}, a_{<t})}$ 为重要性采样比率，优势函数 $\hat{A}_{k,t}$ 通过对批次内奖励进行组归一化计算：

$$\hat{A}_{k,t} = \frac{r_k - \mu(R_i)}{\sigma(R_i)}$$

$r_k$ 为第 $k$ 个输出的总奖励 $r = r_{rank} + r_{abs}$，$\mu(R_i)$ 和 $\sigma(R_i)$ 分别为同一图像 $i$ 的多个采样输出的奖励均值和标准差。

## 实验与关键发现

### 主实验结果

Aes-R1在五个图像美学评估基准（TAD66K、AVA、FLICKR-AES、PARA、AADB）上进行了系统评估，使用PLCC（Pearson线性相关系数）和SRCC（Spearman秩相关系数）作为核心指标。表1展示了与各类基线方法的全面对比。

**与骨干模型的对比。** 以Qwen2.5-VL-7B为骨干模型，Aes-R1将五个基准上的平均PLCC从0.4285提升至0.6337（相对提升47.9%），平均SRCC从0.4589提升至0.6186（相对提升34.8%）。这一提升幅度表明，仅靠模型规模无法解决美学评估问题，而AesCoT推理数据与RAPO联合优化是性能跃升的关键驱动力。

**与MLLM基线的对比。** 在与同类型多模态大语言模型方法的比较中，Aes-R1的平均PLCC/SRCC（0.6337/0.6186）显著优于Q-Insight（0.5954/0.5813，Li et al., 2025）和VisualQuality-R1（0.5171/0.5491，Wu et al., 2025）。值得注意的是，Q-Insight仅使用标量奖励进行RL优化，VisualQuality-R1仅使用排名奖励，而Aes-R1通过RAPO将两者联合优化，在五个数据集上均取得最优或次优结果。在AVA数据集上，Aes-R1的PLCC达到0.6702，相比Q-Insight的0.5964提升了0.0738。

**与通用大模型的对比。** GPT-4.1在相同任务上的平均PLCC/SRCC仅为0.5171/0.5491，表明即使是最先进的通用大模型，在未经专门美学推理训练的情况下，其分数校准和排序能力均存在明显不足。

**分数分布对齐。** 图1(a)展示了不同方法在AVA测试集上的预测分数分布与真实分布的对比。Aes-R1的预测分布与真实分布实现了最紧密的对齐，而Q-Insight和VisualQuality-R1分别表现出分数范围压缩和分布偏移的问题。这直接验证了RAPO中绝对误差奖励对分数校准的贡献。

**泛化能力。** 图4展示了仅在AVA数据集上训练的模型的跨数据集泛化能力。Aes-R1在仅使用AVA训练的情况下，其泛化性能与在大规模人工标注语料上预训练的ArtiMuse（Cao et al., 2025）相当，表明AesCoT构造的结构化推理数据赋予了模型可迁移的美学判断能力，而非简单的数据集拟合。

### 消融实验

#### 奖励函数设计

表2系统消融了不同奖励组合对性能的影响。仅使用二元奖励（Binary，预测误差小于阈值时奖励为1）时，模型缺乏细粒度反馈，平均PLCC/SRCC最低。单独使用绝对误差奖励（Error）相比二元奖励有明显提升，但排序一致性不足。单独使用相对排名奖励（Rank）在SRCC上表现较好，但分数校准能力弱。RAPO提出的误差-排名联合奖励（Error-Rank）在所有数据集上取得最优平均PLCC（0.6297）和SRCC（0.6102），验证了两种奖励信号的互补性——绝对误差奖励提供分数尺度的精确校准，相对排名奖励确保样本间的序关系一致性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_or3ZukbrKw/figures/014_Table_2.jpg]]
*Table 2: Ablation studies of different reward combinations. Our RAPO proposed error-rank reward significantly outperforms others*

#### SFT冷启动的影响

表3展示了RAPO从不同SFT轮次（0、1、2、10 epochs）初始化时的性能变化，同时记录了起始策略的平均token熵。核心发现如下：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_or3ZukbrKw/figures/015_Table_3.jpg]]
*Table 3: The performance when RAPO is initialized from SFT checkpoints (0, 1, 2, 10 epochs), together with the average token entropy of the starting policy. Moderate SFT maximizes downstream performance, while excessive SFT declines entropy and RL gains, hindering OOD performance*

- **无SFT直接RL（0 epoch）**：模型虽能达到一定性能，但生成的美学解释质量差，如图6中AesR1-Zero案例所示，缺乏结构化的多维度分析。
- **适度SFT（1 epoch）**：取得最佳平均PLCC/SRCC（0.6337/0.6186），熵值保持在较高水平（约2.5），为后续RL探索保留了充分的策略空间。
- **过度SFT（10 epochs）**：性能显著退化，熵值急剧下降至约1.0，表明模型已过拟合AesCoT数据的分布偏差，限制了RL阶段的优化增益。在OOD数据集（PARA、AADB）上的退化尤为明显。

这一发现揭示了一个关键的训练动态：SFT冷启动的作用是激活模型的结构化推理模式（教会模型“如何解释”），而非让其记忆特定分数分布。过度SFT会导致模型熵崩塌，使RL阶段的探索能力受限，反而损害泛化性能。

#### 奖励权重系数

表4和图5展示了RAPO奖励中相对排名奖励与绝对误差奖励的权重系数变化对性能的影响。当权重系数λ_rank=0.6、λ_abs=0.4时，平均SRCC达到最优（0.6256）；PLCC在λ_rank=0.5、λ_abs=0.5附近达到峰值。纯排名奖励（λ_rank=1.0）或纯绝对奖励（λ_abs=1.0）均导致显著的性能退化，进一步证实了两种奖励信号的互补特性——绝对误差奖励主导分数校准（影响PLCC），相对排名奖励主导序关系（影响SRCC），联合优化才能实现两者的均衡提升。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_or3ZukbrKw/figures/017_Figure_5.jpg]]
*Figure 5: The trends of PLCC and SRCC metrics with different weighting coefficients in RAPO reward. While relying solely on the relative rank or absolute error reward leads to significant performance degradation, the two reward components exhibit complementary characteristics when applying both rewards*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_or3ZukbrKw/figures/016_Table_4.jpg]]
*Table 4: The performance when changing weighting coefficient of the RAPO reward*

### 关键图表结论

- **图1**：Aes-R1的预测分布与真实分布对齐最优，验证了相对-绝对联合奖励对分数校准和排序一致性的双重作用。
- **图5**：PLCC和SRCC随权重系数的变化趋势呈现互补特征，PLCC在均衡权重附近最优，SRCC在略微偏向排名奖励时最优，说明两种奖励分别作用于分数精度和排序质量的不同维度。
- **图7**：对比SFT和RL训练过程中的平均熵变化，SFT阶段熵持续下降（从约3.0降至约1.0），而RAPO阶段熵保持相对稳定，证明RAPO的KL惩罚项有效防止了策略的灾难性坍缩，维持了生成多样性。
- **图6**：案例研究表明，Aes-R1能够生成平衡且多维度的美学评估（涵盖光线、构图、色彩等维度），而直接RL（AesR1-Zero）的解释质量差，过度SFT的模型则倾向于给出泛泛而谈的评价，缺乏针对性。

### 公平性说明

所有带*的基线方法均在相同的15K组合训练集（AVA、TAD66K、FLICKR-AES按2:2:1比例混合）上重新训练，确保对比的公平性。DeQA-Score因TAD66K缺少每图标准差数据，仅在AVA和Flickr-aes的组合上训练。Aes-R1的15K训练数据规模远小于ArtiMuse等依赖大规模人工标注语料的方法，进一步突显了AesCoT数据质量和RAPO优化策略的有效性。

## 定位与知识库关联

### 问题定位：从分数回归到美学推理

图像美学评估（Image Aesthetic Assessment, IAA）长期被建模为一个回归问题——给定图像，输出一个美学分数。这一范式下的代表性工作包括基于手工特征的 **NIQE**（Mittal et al., 2013）和 **BRISQUE**（Mittal et al., 2012），以及基于深度学习的 **NIMA**（Talebi & Milanfar, 2018）和 **MUSIQ**（Ke et al., 2021）。这些方法虽然能给出分数，但完全不具备可解释性——它们无法解释“为什么”这张图美或不美。

多模态大语言模型（MLLM）的兴起为可解释美学评估打开了新的可能。**Q-Align**（Wu et al., 2023a）首次尝试用离散分数token训练MLLM进行美学评分，但其本质仍是“分数预测”而非“美学推理”。**DeQA-Score**（You et al., 2025）和 **Q-Insight**（Li et al., 2025）进一步引入了强化学习，但面临两个关键瓶颈：其一，缺乏高质量的美学推理训练数据，模型无法激活结构化推理模式；其二，奖励信号设计单一——Q-Insight仅使用标量奖励，**VisualQuality-R1**（Wu et al., 2025）仅使用排名奖励——无法同时校准绝对分数的精度和相对排序的一致性。

Aes-R1正是在这一谱系的关键断裂点上介入：它不满足于让模型“报一个分数”，而是要求模型“先分析、后评分”，并将人类审美的双重偏好——绝对质量判断与相对比较偏好——同时编码为强化学习的优化目标。

### 方法贡献：AesCoT + RAPO 的双轮驱动

Aes-R1的方法贡献可以拆解为两个相互依赖的模块：

**AesCoT数据管道**解决的是“冷启动”问题。在没有现成美学推理数据的情况下，AesCoT从原始图像-分数对出发，通过提示专家MLLM沿五个美学维度（如构图、色彩、光影、主题、技术质量）生成结构化思维链（CoT）解释，再经过自动检查与人工审核过滤掉分数泄露、推理-分数不一致和事实错误。这一管道产出的不是简单的“图像-分数”对，而是“图像-结构化解释-分数”三元组，为后续的监督微调提供了推理范式的模板。

**RAPO算法**解决的是“优化什么”的问题。其核心洞察是：人类审美判断天然包含两种信号——绝对分数（这张图值几分）和相对排序（这张图比那张图好）。RAPO的奖励函数将二者联合建模：

- **相对排名奖励** $r_{rank}$ 基于FRank框架，计算模型预测的成对比较概率 $p_{ik}(\mathcal{T}_i, \mathcal{T}_j)$ 与真实偏好 $p_c$ 之间的Bhattacharyya系数。该奖励有界、连续、可微，直接对齐排序一致性。
  
- **绝对误差奖励** $r_{abs}$ 采用高斯形函数 $r_{abs}(o_{ik}) = \exp\left(-\frac{1}{2}\left(\frac{|o_{ik} - s_i|}{\sigma}\right)^2\right) + \epsilon$，将预测分数校准至真实MOS，提供连续且精确的回归信号。

总奖励 $r = r_{rank} + r_{abs}$ 使梯度更新同时受两个方向的引导。消融实验（Table 2）给出了决定性证据：单独使用误差奖励或排名奖励均明显弱于联合优化——RAPO的误差-排名组合在五个基准上的平均PLCC/SRCC达到0.6297/0.6102，显著优于其他奖励组合。

### 训练策略的关键发现：适度SFT的“熵窗口”

Table 3揭示了一个反直觉但重要的现象：并非SFT越多越好。当RAPO从0 epoch（无SFT冷启动）直接开始时，模型虽然也能获得不错的分数（平均PLCC 0.6286），但生成的解释质量差（Fig. 6, AesR1-Zero）；当SFT进行10个epoch后再接RAPO，性能反而下降（平均PLCC降至0.6207），同时平均token熵急剧降低。最优策略是1个epoch的SFT冷启动后接RAPO，此时熵保持较高水平，模型既学会了结构化推理的范式，又保留了RL探索的空间。

这一发现的方法论意义在于：在RL微调MLLM时，SFT的作用是“教模型如何思考”，而不是“教模型正确答案”。过度SFT会导致模型过拟合冷启动数据的分布，降低熵并阻碍RL的进一步优化——这在OOD数据集（PARA、AADB）上表现尤为明显。

### 奖励权重的互补性

Table 4和Figure 5进一步分析了 $r_{rank}$ 与 $r_{abs}$ 的权重配比。当 $\lambda_{rank}=0.6, \lambda_{abs}=0.4$ 时，平均SRCC达到最优（0.6256）；纯排名奖励或纯绝对奖励均导致性能下降。两种奖励的互补性体现在：绝对奖励确保分数分布与真实分布对齐（Fig. 1a），排名奖励确保模型对不同质量图像有足够的序数辨别力（Fig. 1b案例中，其他方法存在预测误差和排序混淆，而Aes-R1表现最优）。

### 适用边界与局限

**数据效率**：Aes-R1在仅15K训练样本（TAD66K、AVA、Flickr-aes按2:2:1混合）的条件下超越了多个基线，显示出较高的数据效率。但这也意味着其性能依赖于AesCoT管道的推理数据质量——如果源数据的美学分数标注本身存在偏差，推理数据的质量也会受到连锁影响。

**泛化能力**：在仅使用AVA训练时（Fig. 4），Aes-R1展现出与在大规模人工标注语料上预训练的ArtiMuse（Cao et al., 2025）相当的泛化能力。但需要注意的是，这一结论仅基于五个基准数据集，且均为自然图像美学评估场景——对于艺术风格图像、用户生成内容等更开放的场景，泛化性仍需进一步验证。

**推理维度的完备性**：AesCoT沿五个预定义维度生成推理，这些维度覆盖了美学评估的主要方面，但人类审美判断可能涉及更微妙的文化语境、情感共鸣等因素，这些在当前框架中尚未被建模。

### 开放问题

1. **推理质量的自动评估**：AesCoT管道依赖自动检查与人工审核来保证推理质量，但“好的美学推理”本身缺乏客观的自动化评估指标。如何建立推理质量的自动评估体系，是该方法规模化应用的关键。

2. **多模态奖励的扩展**：当前RAPO的奖励仅基于分数和排序，未利用推理文本本身的语义质量。是否可以将推理的连贯性、专业性等维度纳入奖励信号，值得探索。

3. **冷启动数据的依赖性**：实验表明1 epoch SFT是最优选择，但这一“最佳epoch数”是否对不同的骨干模型和数据集组合敏感，仍需系统研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Unlocking_the_Essence_of_Beauty_Advanced_Aesthetic_Reasoning_with_Relative_Absolute_Policy_Optimization.pdf]]

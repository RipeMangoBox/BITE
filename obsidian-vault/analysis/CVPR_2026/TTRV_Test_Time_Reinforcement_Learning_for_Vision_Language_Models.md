---
title: "TTRV: Test-Time Reinforcement Learning for Vision Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TTRV_Test_Time_Reinforcement_Learning_for_Vision_Language_Models.pdf
project_link: "https://akshit21112002.github.io/ttrvproject/"
code_link: null
aliases:
- TTTRLV
- TTRV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在测试阶段直接从无标记数据中提取自监督奖励信号（频率一致性 + 熵正则化），驱动GRPO在线优化模型参数。
primary_logic: 利用模型自身多次采样的输出分布，以频次作为软监督信号并约束输出熵，可以在测试时恢复并放大预训练中已习得但被指令微调削弱的基础视觉推理能力。
claims:
- TTRV无需任何标记数据，仅从20个随机采样测试样本即可在InternVL3-8B上实现ImageNet Top-1 99.31%（+19.84%），平均16个数据集提升24.6%（识别）和10.0%（VQA），超越GPT-4o。
- 消融实验证实频率+多样性奖励组合优于多数投票奖励及单一奖励项，甚至优于TENT风格的熵最小化。
- 在极端数据稀缺场景下（仅1个随机测试样本），TTRV仍能带来最高5.5%的提升，证明其并非单纯拟合分布而是激活潜在能力。
- ImageNet 上 Top-1 Accuracy = 98.31
---

# TTRV: Test-Time Reinforcement Learning for Vision Language Models

> [!tip] 核心洞察
> 利用模型自身多次采样的输出分布，以频次作为软监督信号并约束输出熵，可以在测试时恢复并放大预训练中已习得但被指令微调削弱的基础视觉推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | TTRV：视觉语言模型的测试时强化学习 |
| 英文题名 | TTRV: Test-Time Reinforcement Learning for Vision Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.06783) · [Project](https://akshit21112002.github.io/ttrvproject/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TTRV (Test-Time Reinforcement Learning for VLMs) |
| Dataset | ImageNet, ImageNet-R, DTD, Resisc45 |

> [!tip] 效果简介
> - ImageNet 上，Top-1 Accuracy 98.31 vs 56.00 (+42.31)；Top-1 Accuracy 99.31 vs 79.47 (+19.84)。
> - ImageNet-R 上，Top-1 Accuracy 96.89 vs 66.01 (+30.88)。
> - DTD 上，Top-1 Accuracy 89.73 vs 37.24 (+52.49)。

## 概述

现有视觉语言模型（VLM）在测试时无法像人类一样从无标记经验中动态学习，必须依赖大量标注数据和昂贵的指令微调或RLHF后训练，导致泛化性和适应性受限。**TTRV（Test-Time Reinforcement Learning for Vision Language Models）** 提出了一种根本不同的范式：在测试推断阶段，直接从无标注的测试样本中提取自监督奖励信号，驱动模型在线优化参数。

其核心洞察是：利用模型自身多次采样的输出分布，以回答频次作为软监督信号（频率奖励），同时约束输出熵以控制多样性（熵正则化），可以在测试时恢复并放大预训练中已习得、但被指令微调削弱的基础视觉推理能力。

**主要结果概览**（以下数据均来自原文 Table 1、Table 2 及摘要）：

- 在 InternVL3-8B 上，仅用 **20 个随机采样测试样本** 进行 TTRV 适配，ImageNet Top-1 准确率即从 79.47% 跃升至 **99.31%（+19.84%）**；在 InternVL3-2B 上更从 56.00% 提升至 **98.31%（+42.31%）**。
- 在 **16 个数据集** 上，图像识别任务平均提升 **24.6%**，视觉问答（VQA）任务平均提升 **10.0%**，个别数据集提升幅度高达 52.4%（识别）和 29.8%（VQA）。
- 经 TTRV 适配的 InternVL3-8B 在 8 个图像识别基准上平均超越 GPT-4o **2.3%**。
- 消融实验证实，频率+多样性奖励的组合显著优于多数投票奖励（TTRL）及单一奖励项，也优于 TENT 风格的熵最小化替代方案（Table 3）。
- 在极端数据稀缺场景下（仅 **1 个随机测试样本**），TTRV 仍可带来最高 **5.5%** 的提升（Table 6），表明其并非单纯拟合测试分布，而是激活了模型的潜在能力。
- TTRV 展现出模型无关性，可泛化到 Qwen2.5-VL、MM-Eureka、ThinkLite-VL、VisionReasoner 等多个 VLM 家族（Table 7, Table 13）。

**方法定位**：TTRV 将 GRPO（Group Relative Policy Optimization）首次引入 VLM 的测试时强化学习，形成了“Rollout 生成 → 频率奖励计算 → 熵正则化 → 组合奖励 → GRPO 优势估计 → 策略更新”的在线适配闭环。与依赖标注训练数据的传统 RLHF 不同，其奖励信号完全来源于测试样本自身的输出经验分布，无需任何外部监督。

**关键局限**：计算开销显著——即使使用 vLLM 加速，适配 20 个样本也需增加数分钟延迟（相较正常推断增加 547% 以上），适配 500 个样本则超过 1.5 小时，难以直接用于实时场景。此外，作者承认目前缺乏理论解释来说明 TTRV 为何能增强核心能力而非简单过拟合测试分布。

## 背景与动机

视觉语言模型（VLM）在图像识别、视觉问答等任务上取得了显著进展，但其部署仍面临一个根本性瓶颈：**现有VLM在测试时无法像人类一样从无标记经验中动态学习，必须依赖大量标记数据和昂贵微调，泛化性和适应性受限**。主流范式将训练与推断严格分离——模型在预训练和指令微调阶段消耗海量标注数据，一旦部署便参数冻结，面对分布偏移或新场景时只能被动承受性能退化。

这一困境在decoder-based VLM上尤为突出。以InternVL3-2B为例，其在ImageNet上的Top-1准确率仅56.00%，远低于专门的dual-encoder模型（如SigLIP的80.50%），暴露出指令微调可能削弱了预训练阶段习得的基础视觉识别能力。现有解决方案存在两条路径但各有缺陷：

- **测试时适应（TTA）**：以**TENT**（Wang et al., ICLR 2021）为代表，通过熵最小化在测试时调整批归一化层，但仅适用于encoder结构，无法直接迁移到decoder VLM。
- **强化学习微调**：如**TTRL**（Zuo et al., 2024）尝试在测试时使用多数投票构造伪标签进行RL，但其奖励信号粗糙，未能充分挖掘模型自身的输出分布信息。

更深层的问题在于：**如何在不依赖任何外部监督的前提下，让模型在测试时自主发现并强化正确的推理路径？** 这要求一种能从无标记测试样本中提取有效学习信号，并驱动模型参数在线更新的机制。

TTRV的动机正是填补这一空白——将强化学习从训练阶段解放到测试阶段，直接从模型自身多次采样的输出分布中提取自监督奖励信号，驱动GRPO在线优化模型参数。其核心假设是：**利用模型多次采样的输出频次作为软监督信号，并约束输出熵防止过早收敛，可以在测试时恢复并放大预训练中已习得但被指令微调削弱的基础视觉推理能力**。这一假设在极端数据稀缺场景下得到初步验证——仅使用1个随机测试样本，TTRV仍能带来最高5.5%的提升，暗示其并非单纯拟合分布而是激活潜在能力。

## 核心创新

### 问题瓶颈：VLM 的“测试时失语”

现有视觉语言模型（VLM）在训练完成后，其能力被冻结于参数之中。当它们面对测试样本时，无论该样本是陌生领域的图像还是需要复杂推理的视觉问答，模型只能进行一次性的前向推断，无法像人类一样从当前遭遇的样本中即时学习、修正错误。这导致两个严重后果：其一，模型必须依赖海量标注数据和昂贵的指令微调，才能在下游任务上获得可接受的性能，泛化成本极高；其二，一旦测试分布与训练分布存在偏移，模型性能会剧烈退化，而传统的测试时适应方法（如 TENT，Wang et al., ICLR 2021）仅能通过熵最小化等启发式目标进行微弱调整，无法从根本上激活模型在预训练阶段已习得但被指令微调削弱的基础视觉推理能力。

### 核心调控旋钮：从无标注测试数据中提取自监督强化信号

TTRV 的核心创新在于将强化学习的优化时机从训练阶段彻底迁移到测试推断阶段，并设计了一套无需任何标注数据的自监督奖励机制。具体而言，TTRV 改变了两个关键控制维度：

#### 信号来源：从“人类标注”到“模型共识”

传统 VLM 的强化学习（如 RLHF）依赖人类偏好标注或任务标签作为奖励信号，而 TTRV 的奖励信号完全从测试样本自身的模型输出分布中提取。对于每一个测试提示，模型被采样 $N$ 次产生一组候选回答 $\{\hat{y}_1, \dots, \hat{y}_N\}$，由此形成经验分布。TTRV 从该分布中提炼出两种互补的奖励：

- **频率奖励（Frequency-Based Reward）**：将每个唯一回答在 $N$ 次采样中出现的频率作为软标签，奖励与该频率成正比的回答。其数学形式为 $r_{1}(\hat{y}_{j}) = \sum_{m=1}^{M} p(\tilde{y}_{m}) \cdot \mathbf{1}\{\hat{y}_{j} = \tilde{y}_{m}\}$，其中 $p(\tilde{y}_{m})$ 是唯一回答 $\tilde{y}_{m}$ 的经验概率。这一设计巧妙地将“模型共识”转化为监督信号——高频回答获得高奖励，但低频回答仍保留非零奖励，避免过早坍缩到局部最优。
- **多样性控制奖励（Diversity Control Reward）**：计算输出分布的熵 $H(P) = -\sum_{m=1}^{M} p(\tilde{y}_{m}) \log p(\tilde{y}_{m})$，并以 $r_{2} = -H(P)$ 作为惩罚项。当模型回答过于分散（高熵），该惩罚推动模型向高频答案集中；当回答过于单一（低熵），惩罚自然减弱，允许模型保持适度多样性。这种动态平衡防止了策略的过早收敛或发散失控。

最终奖励为两者的加权组合：$R(\hat{y}_{j}) = r_{1}(\hat{y}_{j}) + \alpha r_{2}$，其中 $\alpha$ 控制多样性约束的强度。

#### 优化时机：从“离线训练”到“在线适应”

传统 VLM 的训练范式严格遵循“先训练、后测试”的时序分离：模型在预先划分的训练集上完成参数更新后，在测试阶段仅执行冻结参数的推断。TTRV 打破了这一界限，将 GRPO（Group Relative Policy Optimization）引入测试时。对于每一个测试提示，模型在生成 $N$ 个候选回答后，立即利用上述自监督奖励计算组内相对优势：

$$A_i = \frac{R(\hat{y}_i) - \mathrm{mean}_j(R(\hat{y}_j))}{\mathrm{std}_j(R(\hat{y}_j))}$$

并通过策略梯度更新模型参数：$\theta \leftarrow \theta + \eta \nabla_{\theta} \mathbb{E}_{y \sim \pi_{\theta}(\cdot|x)} [R(y)]$，同时保持与参考策略的 KL 散度约束 $\beta D_{\mathrm{KL}}(\pi(\cdot | x) \| \pi_{\mathrm{ref}}(\cdot | x))$，防止模型偏离预训练知识太远。整个优化过程完全在测试时在线完成，无需任何预先准备的标注数据。

### 核心洞察：恢复被削弱的基础能力

TTRV 的成功并非简单的分布拟合或多数投票。消融实验（Table 3）表明，TTRV 的频率+多样性奖励组合显著优于单纯的多数投票奖励（如 TTRL，Zuo et al., 2024）以及 TENT 风格的熵最小化。更关键的是，在极端数据稀缺场景下——仅使用**单个随机测试样本**进行适配——TTRV 仍能在 ImageNet-R 上带来 +5.47% 的提升（Table 6）。这一现象说明，TTRV 并非依赖大量样本的统计拟合，而是通过强化学习机制激活了模型内部在预训练中已习得、但被后续指令微调掩盖的基础视觉推理能力。跨数据集泛化实验（Figure 3, Table 12）进一步佐证了这一点：在 ImageNet-V2 上应用 TTRV 后，模型在 ImageNet-R 上的准确率可提升 +15.89%，表明 TTRV 增强的是核心视觉理解能力，而非对特定数据分布的过拟合。

### 与现有方法的本质差异

| 维度 | 传统 VLM 训练范式 | TENT 风格测试时适应 | TTRV（本文） |
|------|-------------------|---------------------|-------------|
| **优化阶段** | 训练阶段 | 测试阶段 | 测试阶段 |
| **监督信号** | 人类标注 / 偏好 | 熵最小化（无监督） | 模型共识（频率+多样性，无监督） |
| **优化算法** | SFT / RLHF / DPO | 梯度下降（熵目标） | GRPO（强化学习） |
| **数据需求** | 大量标注数据 | 无标注测试样本 | 无标注测试样本 |
| **核心机制** | 拟合人类意图 | 降低输出不确定性 | 恢复并放大预训练基础能力 |

TTRV 是首个将 GRPO 引入 VLM 测试时强化的框架，其奖励设计从“模型自洽性”中提取学习信号，而非依赖外部标注或简单的熵启发式。这一范式转变使得 VLM 能够在遭遇任何测试数据时自主进化，为通用视觉智能体的在线学习开辟了新路径。

## 整体框架

TTRV 的整体 pipeline 围绕一个核心思想展开：**在测试时，直接从未标注的测试样本中提取自监督奖励信号，驱动 GRPO 在线优化 VLM 参数**，从而无需任何预训练数据划分或标注数据即可提升下游视觉任务表现。图 2 给出了完整的流程概览。

**Pipeline 由五个关键模块串联构成：**

1. **Rollout 生成**：对于每个测试提示 $x$，从当前策略 $\pi_\theta(\cdot|x)$ 中采样 $N$ 个候选回答 $\{\hat{y}_1, \dots, \hat{y}_N\}$，形成经验输出分布。这一步为后续奖励计算提供了统计基础。
2. **频率奖励计算**：将 $N$ 次采样中的唯一回答 $\{\tilde{y}_1, \dots, \tilde{y}_M\}$ 的经验概率 $p(\tilde{y}_m) = \frac{1}{N}\sum_{j=1}^{N} \mathbf{1}\{\hat{y}_j = \tilde{y}_m\}$ 作为软监督信号，对每个候选回答赋予与其出现频次成正比的奖励 $r_1(\hat{y}_j) = \sum_{m=1}^{M} p(\tilde{y}_m) \cdot \mathbf{1}\{\hat{y}_j = \tilde{y}_m\}$。这本质上是将“多数意见”转化为可微的奖励，同时为低频回答保留非零奖励，避免过早坍缩。
3. **熵正则化多样性控制**：计算经验分布的熵 $H(P) = -\sum_{m=1}^{M} p(\tilde{y}_m) \log p(\tilde{y}_m)$，并将其负值作为奖励项 $r_2 = -H(P)$。当模型输出过于分散（高熵）时，该惩罚项驱动模型向高频答案集中；当输出过于集中（低熵）时，惩罚减弱，防止过度收敛。
4. **组合奖励**：将频率奖励与熵正则化项加权求和，得到总奖励 $R(\hat{y}_j) = r_1(\hat{y}_j) + \alpha r_2$，其中 $\alpha$ 控制多样性约束的强度。
5. **GRPO 策略更新**：将同一提示下的 $N$ 个候选回答的绝对奖励标准化为组内相对优势 $A_i = \frac{R_i - \mathrm{mean}_j(R_j)}{\mathrm{std}_j(R_j)}$，然后通过最大化 KL 正则化的期望奖励目标 $\max_{\pi} \mathbb{E}_{x \sim D, y \sim \pi(\cdot|x)} [R(x, y)] - \beta D_{\mathrm{KL}}(\pi(\cdot|x) \| \pi_{\mathrm{ref}}(\cdot|x))$ 来更新模型参数 $\theta \leftarrow \theta + \eta \nabla_\theta \mathbb{E}_{y \sim \pi_\theta(\cdot|x)} [R(y)]$。

**输入输出流**：整个流程的输入仅为测试时遭遇的未标注样本 $x$ 和预训练 VLM 的初始参数 $\pi_{\mathrm{ref}}$；输出是经过在线适配后的模型参数 $\pi_\theta$，以及在该参数下对测试样本的最终预测。值得注意的是，TTRV 不依赖任何外部标注数据或预先划分的训练集——奖励信号完全由模型自身的输出分布内生地产生。

**与现有范式的根本差异**：传统 VLM 适配流程依赖于“预训练 → 监督微调（SFT）→ 强化学习（RL）”的三阶段范式，其中 RL 阶段需要大量标注数据或人类偏好信号。TTRV 将 RL 的时机从训练阶段**前移到了测试推断阶段**，并将奖励信号来源从外部监督**替换为模型输出分布的自监督统计量**。这一设计使得模型能够在遭遇新数据时“即插即用”地在线学习，而无需任何离线准备。

**因果机制**：TTRV 之所以有效，其核心洞察在于：预训练阶段习得的基础视觉推理能力在指令微调后可能被部分削弱，而测试时 RL 通过频率一致性与熵约束的组合奖励，能够**恢复并放大这些潜在能力**。消融实验（Table 3）证实，频率+多样性奖励组合显著优于单纯的多数投票奖励（TTRL）或 TENT 风格的熵最小化，验证了该奖励设计并非简单的分布拟合，而是激活了模型内在的推理能力。

### 补充图表

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/001_Figure.jpg]]

## 核心模块与公式推导

TTRV 将测试时强化学习形式化为一个 **KL 正则化的策略优化问题**，其目标是在最大化期望奖励的同时，约束当前策略 $\pi$ 与参考策略 $\pi_{\text{ref}}$ 的偏离程度：

$$\operatorname*{max}_{\pi} \mathbb{E}_{x \sim D, y \sim \pi(\cdot | x)} [ r(x, y) ] - \beta D_{\mathrm{KL}}(\pi(\cdot | x) \| \pi_{\text{ref}}(\cdot | x))$$

其中 $\beta$ 控制 KL 惩罚的强度。整个框架由以下核心模块串联构成。

### 1. Rollout 生成

对每个测试样本 $x$，从当前策略 $\pi_\theta(\cdot|x)$ 中采样 $N$ 个候选回答 $\{\hat{y}_1, \dots, \hat{y}_N\}$，形成经验分布。这是后续所有奖励信号的计算基础。

### 2. 频率奖励（Frequency-Based Reward）

将 $N$ 次采样中出现的 $M$ 个唯一回答记为 $\{\tilde{y}_1, \dots, \tilde{y}_M\}$，其经验概率为：

$$p(\tilde{y}_m) = \frac{1}{N} \sum_{j=1}^{N} \mathbf{1}\{\hat{y}_j = \tilde{y}_m\}$$

每个候选回答 $\hat{y}_j$ 的频率奖励定义为它所属唯一回答的经验概率：

$$r_{1}(\hat{y}_{j}) = \sum_{m=1}^{M} p(\tilde{y}_{m}) \cdot \mathbf{1}\{\hat{y}_{j} = \tilde{y}_{m}\}$$

**核心机制**：高频回答获得高奖励，低频但可能仍有意义的回答也能获得非零奖励，形成软监督信号。这与硬多数投票（TTRL, Zuo et al., 2024）形成本质区别——后者直接丢弃低频回答的全部信息。

### 3. 多样性控制奖励（Diversity Control Reward）

计算经验分布的熵：

$$H(P) = -\sum_{m=1}^{M} p(\tilde{y}_{m}) \log p(\tilde{y}_{m})$$

多样性控制奖励直接取负熵：

$$r_{2} = -H(P)$$

**核心机制**：高熵代表回答高度分散（模型不确定），负熵惩罚迫使模型向高频答案集中，防止策略在 RL 过程中发散；同时避免过早坍缩到单一答案，与频率奖励形成制衡。

### 4. 组合奖励

总奖励为频率奖励与熵正则化项的加权和：

$$R(\hat{y}_{j}) = r_{1}(\hat{y}_{j}) + \alpha r_{2}$$

其中 $\alpha$ 控制多样性惩罚的权重。消融实验（Table 3）证实，频率 + 多样性的组合设计显著优于单独使用任一项，也优于 TENT 风格的纯熵最小化（Wang et al., ICLR 2021）和多数投票奖励（TTRL）。

### 5. GRPO 优势估计

GRPO（Group Relative Policy Optimization）将同一提示 $x$ 下 $N$ 个候选回答的绝对奖励转化为组内相对优势：

$$A_i = \frac{R(\hat{y}_i) - \text{mean}_j(R(\hat{y}_j))}{\text{std}_j(R(\hat{y}_j))}$$

标准化操作消除了奖励绝对尺度的波动，使策略梯度更新更加稳定。

### 6. 策略更新

最终参数更新沿期望奖励的梯度方向进行：

$$\theta \leftarrow \theta + \eta \nabla_{\theta} \mathbb{E}_{y \sim \pi_{\theta}(\cdot|x)} [R(y)]$$

其中 $\eta$ 为学习率。整个流程（Figure 2）在测试时对每个样本在线执行，无需任何标注数据。

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TTRV. For each prompt x, the VLM generates N candidate responses*

## 实验与分析

### 核心实验设置

TTRV在测试时直接从未标注的测试样本中提取自监督奖励信号，驱动GRPO在线优化模型参数。实验采用**InternVL3**（Zhu et al., 2024）作为主骨干，覆盖2B和8B两种规模，并在8个图像识别基准和8个视觉问答基准上评估。所有实验无需任何标记数据，仅从随机采样的测试样本中提取奖励进行适配。基线包括双编码器VLM（**CLIP**、**SigLIP**、**EVA-CLIP**等）、解码器VLM（**LLaVA-1.5**、**Phi-3.5-vision**等）以及闭源模型**GPT-4o**。

### 主实验结果

**图像识别**（Table 1）：TTRV在InternVL3-2B上实现ImageNet Top-1从56.00%跃升至98.31%（+42.31%），在InternVL3-8B上从79.47%提升至99.31%（+19.84%），后者超越GPT-4o。在更具挑战性的分布外数据集上提升更为显著：InternVL3-2B在DTD上从37.24%提升至89.73%（+52.49%），在ImageNet-R上从66.01%提升至96.89%（+30.88%）。8B模型在Resisc45上从83.62%提升至93.82%（+10.20%）。平均而言，TTRV在8个识别数据集上带来24.6%的提升。

**视觉问答**（Table 2）：TTRV在InternVL3-2B上实现AI2D从39.68%提升至67.75%（+28.07%），MathVista从58.26%提升至66.11%（+7.85%）。8B模型在CRPE上从55.81%提升至68.26%（+12.45%），在RealWorldQA上从19.01%提升至26.57%（+7.56%）。平均VQA提升为10.0%。

### 奖励设计消融

Table 3系统消融了奖励设计的每个组件。频率奖励（Freq. only）单独使用已能带来显著提升，但加入多样性控制（Diversity control）后进一步增益。完整的TTRV（频率+多样性）在ImageNet-R上达到96.89%，而仅用频率奖励为94.23%，仅用多样性控制（本质近似**TENT**的熵最小化，Wang et al., ICLR 2021）仅为91.45%。与**TTRL**（Zuo et al., 2024）的多数投票伪标签奖励相比，TTRV在所有数据集上均表现更优（如ImageNet-R上96.89% vs 93.12%），验证了软频率信号优于硬投票标签。

Table 5进一步排除了“随机奖励即可带来增益”的可能性：使用随机奖励（Shao et al.）在InternVL系列上几乎无提升，而TTRV的精心设计奖励带来显著增益，证明奖励信号的质量至关重要。

### 数据采样鲁棒性

**有偏采样**（Table 4）：即使仅从少数类别采样（如ImageNet-R仅用4/200类），TTRV仍提供稳健提升（ImageNet-A上+4.42% biased vs +5.33% random），表明方法不依赖均匀的类分布。

**单样本适配**（Table 6）：在极端数据稀缺场景下，仅用1个随机测试样本进行TTRV适配，仍可获得最高5.47%的提升（ImageNet-R），证明TTRV并非单纯拟合测试分布，而是激活了预训练中已习得的基础视觉推理能力。

### 跨数据集泛化

Figure 3和Table 12展示了TTRV的核心泛化能力：在一个数据集上适配后，直接评估于完全不同的目标数据集。例如，在ImageNet-V2上适配InternVL3-2B，然后在ImageNet-R上评估，获得15.89%的提升。这种跨域迁移表明TTRV增强的是模型的底层视觉理解能力，而非对特定分布的记忆。

### 模型家族泛化

TTRV不仅在InternVL3上有效，还可泛化至多个VLM家族（Table 7, Table 13）：在**Qwen2.5-VL-3B**上，ImageNet-R提升29.40%，AI2D提升3.93%；在**MM-Eureka**、**ThinkLite-VL**和**VisionReasoner**上也获得一致提升，验证了方法的模型无关性。

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/010_Table_7.jpg]]
*Table 7: Generalization to Model Families. We provide results for the two tasks (Image Classification and VQA) by using the Qwen2.5-VL-3B [3]*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/016_Table_13.jpg]]
*Table 13: Generalization to Model Families. We provide results for MM-Eureka, ThinkLite-VL and VisionReasoner*

### 适配样本数与计算开销

Table 9显示增加适配样本数可进一步提升性能（如ImageNet上20样本98.31% vs 500样本99.01%），但Table 10揭示了显著的计算开销：即使使用vLLM加速，适配20个样本需额外数分钟延迟（较正常推断增加547%以上），适配500样本需超过1.5小时。这构成了TTRV在实时场景应用的主要瓶颈。

### 失败模式与局限性

1. **弱基线下性能退化**：在InternVL2.5-4B等质量较低的模型上，TTRV在Resisc45上出现性能下降。作者归因于基模型输出质量过低导致rollout失效或GRPO优化不稳定。
2. **缺乏理论解释**：作者明确承认尚无法从理论上解释TTRV为何能增强核心能力而非简单拟合分布。
3. **任务覆盖有限**：当前评估仅限于对象识别和VQA，未探索生成式任务或更复杂的多模态推理场景。

### 补充图表

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/003_Table_1.jpg]]
*Table 1: Image Classification. Top-1 Accuracy (%) obtained by evaluating multiple different backbones. The results in gray are obtained using the specialized dual-encoder VLMs and the proprietary GPT-4o. For decoder-based VLMs we also evaluate multiple families and model sizes. Our TTRV is applied to different model sizes from the InternVL [77] family of models. The best results obtained for a dataset are highlighted in bold, while the second best are underlined*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/004_Table_2.jpg]]
*Table 2: Visual Question Answering. Results obtained by evaluating multiple different backbones. For decoder-based VLMs, we evaluate multiple families and model sizes. Our TTRV is applied to different model sizes from the InternVL [77] family of models*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/007_Table_3.jpg]]
*Table 3: Ablating Reward Designs. We compare the design choices of our TTRV with the reward design proposed by Zuo et al. [78], based on the pseudo-labels obtained from a majority voting scheme. Further, we also ablate the individual effect of our frequency- and diversity-based rewards*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/005_Figure_3.jpg]]
*Figure 3: Cross-dataset Generalization. Top-1 accuracy (%) achieved by employing TTRV on a base dataset using InternVL3- 2B and evaluating on a target dataset from a completely different domain. The results highlight that TTRV enhances core abilities of the model*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/009_Table_6.jpg]]
*Table 6: Single Example TTRV. We report results for VQA and image classification after applying TTRV on a single randomly sampled test example*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/006_Table_4.jpg]]
*Table 4: Biased vs. Random Sampling. Top-1 accuracy (%) obtained by sampling the test data differently. For biased sampling, we choose a fraction of the data from only a subset of classes (e.g., 4 out of 200 for ImageNet-R). Random sampling results are obtained by sampling the data randomly from all classes*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/013_Table_10.jpg]]
*Table 10: Computation Overhead. Inference and adaptation latency through TTRV. Seconds: s, Minutes: m, Hours: h*

![[assets/figures/papers/paper_list_l2666_https_arxiv_org_abs_2510_06783/figures/015_Table_12.jpg]]
*Table 12: Cross-dataset generalization. Performance on different dataset combinations, where X → Y denotes training on dataset X and testing on dataset Y. "IN" in the table refers to ImageNet*

## 方法谱系与知识库定位

### 1. 方法在文献中的位置

TTRV 处于 **测试时自适应（Test-Time Adaptation, TTA）** 与 **基于强化学习的视觉语言模型后训练（RL for VLMs）** 两条技术路线的交叉点，但其核心设计使其与两者均有本质区别。

**相对于测试时自适应方法：** 传统 TTA 方法（如 **TENT**，Wang et al., ICLR 2021）通过最小化模型输出熵来更新归一化层参数，依赖的是单次前向传播的置信度信号。TTRV 的消融实验（Table 3）直接将 TENT 风格的熵最小化作为对比基线——仅使用多样性控制奖励（即 TTRV w/o Freq. reward）近似 TENT——结果表明 TTRV 的完整奖励设计（频率 + 多样性）显著优于该替代方案。这揭示了一个关键差异：单纯的熵最小化无法区分“模型因能力不足而犹豫”与“模型因任务本身存在多种合理答案而分散”，而 TTRV 的频率奖励通过多次采样的经验分布提供了软监督信号，能够引导模型向更一致的正确答案收敛。

**相对于 RL-based VLM 后训练方法：** 现有 RL 方法（如基于人类反馈的 RLHF、基于多数投票的 **TTRL**，Zuo et al., 2024）均依赖训练阶段的标注数据或伪标签。TTRV 是首个将 GRPO 引入测试时阶段的 VLM 框架（原文明确声明：“the first framework to leverage GRPO for test-time RL of VLMs”）。与 TTRL 的多数投票奖励相比，TTRV 的频率奖励采用软概率加权而非硬伪标签，保留了对低频但可能正确答案的非零奖励，这在消融（Table 3）中表现出明显优势。

**相对于 VLM 基线模型家族：** TTRV 被验证可即插即用于多种开源 VLM，包括 **InternVL3**（Zhu et al., 2024）、**Qwen2.5-VL**（Bai et al., 2024）、**MM-Eureka**、**ThinkLite-VL** 和 **VisionReasoner**（Table 7, Table 13），覆盖双编码器架构（如 **CLIP**，Radford et al., ICML 2021；**SigLIP**，Zhai et al., NeurIPS 2023）和仅解码器架构（如 **LLaVA-1.5-7b**，Liu et al., NeurIPS 2023；**Phi-3.5-vision**，Abdin et al., 2024），显示出较强的模型无关性。在 InternVL3-8B 上，TTRV 甚至使该开源模型在 8 个图像识别基准上平均超越闭源模型 **GPT-4o**（OpenAI, 2024）2.3%。

### 2. 关键设计选择与知识贡献

TTRV 的知识贡献可凝练为三个相互耦合的设计选择，它们共同构成了从“测试时无监督信号”到“在线策略优化”的完整因果链：

| 设计选择 | 基线/替代方案 | TTRV 方案 | 证据锚点 |
|---------|-------------|----------|---------|
| 奖励信号来源 | 标注数据（SFT/RLHF）或伪标签（TTRL 多数投票） | 从测试样本自身 N 次采样的经验分布中提取频率奖励 + 熵正则化 | Section 3.2, Table 3 |
| 优化时机 | 训练阶段，离线 | 测试推断阶段，在线逐样本适配 | Abstract, Section 3.2 |
| 策略优化算法 | PPO / DPO 等 | GRPO（组内相对优势标准化 + KL 约束） | Section 3.1, Eq. (2) |

其中，**频率奖励** 是核心创新：它将模型多次采样的一致程度作为软监督信号，奖励公式 $r_{1}(\hat{y}_{j}) = \sum_{m=1}^{M} p(\tilde{y}_{m}) \cdot \mathbf{1}\{\hat{y}_{j} = \tilde{y}_{m}\}$ 使得高频回答获得高奖励，同时低频回答仍保留非零梯度。**多样性控制奖励** $r_{2} = -H(P)$ 则作为正则项防止策略过早坍缩或过度发散，与频率奖励通过加权系数 $\alpha$ 组合为总奖励 $R(\hat{y}_{j}) = r_{1}(\hat{y}_{j}) + \alpha r_{2}$。

这一设计的深层洞察在于：预训练 VLM 在大量数据上习得了基础视觉推理能力，但指令微调可能削弱了这些能力（例如使模型过度依赖语言先验）。TTRV 通过自监督的测试时 RL，实际上是在恢复并放大预训练阶段已习得但被后续微调抑制的能力——这一假说得到了跨数据集泛化实验（Figure 3, Table 12）的支持：在 ImageNet-V2 上适配后，模型在 ImageNet-R 上获得 +15.89% 的提升，表明 TTRV 增强的是核心视觉理解而非特定分布的记忆。

### 3. 适用边界与局限

**计算开销是首要瓶颈。** 即使使用 vLLM 加速推断，适配 20 个样本的额外延迟相对于正常推断增加 547% 以上，适配 500 个样本则需超过 1.5 小时（Table 10）。这使得 TTRV 目前难以用于实时或低延迟场景。

**基模型质量存在下限。** 在 InternVL2.5-4B 的 Resisc45 数据集上观察到性能下降，作者将其归因于基模型质量过低导致 rollout 失效或 GRPO 优化不稳定。这意味着 TTRV 并非万能增强器，其有效性依赖于基模型已具备一定水平的视觉理解能力。

**理论解释缺失。** 作者明确承认，TTRV 为何能增强核心能力（而非简单拟合测试分布）尚无严格的理论论证。这一开放问题限制了对其泛化边界的可靠预测。

**任务覆盖有限。** 当前评估仅覆盖对象识别（8 个数据集）和视觉问答（8 个数据集），未涉及生成式任务、视频理解、3D 场景或更复杂的多模态推理链。

### 4. 开放问题与未来方向

基于上述局限，以下开放问题值得关注：

1. **效率与效能的权衡：** 能否设计更高效的测试时 RL 算法，例如通过极小样本（当前 Table 6 显示单样本仍可获得最高 5.47% 提升）或增量在线学习，将运算开销降低到实用水平？

2. **能力恢复 vs. 分布适配的机制分离：** TTRV 的成功究竟是因为恢复了预训练能力，还是进行了某种隐式的测试时分布适配？设计对照实验（如冻结不同层、对比预训练与指令微调模型的 TTRV 增益差异）可能有助于回答这一问题。

3. **超参数的自适应调节：** 奖励组合权重 $\alpha$ 和采样数量 $N$ 目前为固定值。是否可以根据样本难度或模型输出熵动态调整这些超参数，以在简单样本上节省计算、在困难样本上投入更多资源？

4. **更广泛的任务与模型验证：** TTRV 在更大规模 VLM（如 70B+ 参数）以及视频、3D 等多模态任务上的有效性尚待验证。

5. **公平性与社会影响：** 论文未讨论 TTRV 对模型公平性或社会偏见的影响。测试时自适应是否会放大或缓解预训练模型中的偏见，是一个需要手动验证的议题。

## 原文 PDF

![[paperPDFs/CVPR_2026/TTRV_Test_Time_Reinforcement_Learning_for_Vision_Language_Models.pdf]]

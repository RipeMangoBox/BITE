---
title: "Alignment-Weighted DPO: A principled reasoning approach to improve safety alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Alignment_Weighted_DPO_A_principled_reasoning_approach_to_improve_safety_alignment.pdf
project_link: null
code_link: null
openreview_forum_id: OuMNJoKJBQ
aliases:
- AWDAD
- AWDPRAISA
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "推理关键神经元（通过线性探针识别的注意力头）的激活/停用"
primary_logic: "通过构建包含详细推理轨迹的CoT安全微调数据集，显式增强模型在安全任务上的推理能力；并进一步提出对齐加权DPO（AW-DPO），将输出分解为推理和响应两部分，分别计算DPO损失并加权，从而更精细地纠正推理和响应中的对齐错误，在保持实用性的前提下大幅提升安全鲁棒性。"
claims:
- "停用推理关键神经元后，推理任务准确率大幅下降（如LLaMA2-7B从41.42%降至23.83%），而安全任务准确率几乎保持不变（100.00% vs 99.60%），证明安全对齐与深度推理脱钩。"
- "AW-DPO在SorryBench的20种越狱攻击下，在多个模型家族上取得了最低的平均攻击成功率（如LLaMA-3.1-8B上ASR 0.81%），显著低于标准DPO（1.00%）和CoT Safety SFT（5.42%）。"
- "AW-DPO仅需单轮SFT+DPO训练，即在安全性上接近或超越需要三轮迭代训练的STAIR-DPO-3，且计算开销更低。"
- "SorryBench (各种越狱攻击下的安全评估) 上 Average Attack Success Rate (ASR) ↓ = 0.81% ± 0.68 (AW-DPO on LLaMA-3.1-8B Base)"
---

# Alignment-Weighted DPO: A principled reasoning approach to improve safety alignment

> [!tip] 核心洞察
> 通过构建包含详细推理轨迹的CoT安全微调数据集，显式增强模型在安全任务上的推理能力；并进一步提出对齐加权DPO（AW-DPO），将输出分解为推理和响应两部分，分别计算DPO损失并加权，从而更精细地纠正推理和响应中的对齐错误，在保持实用性的前提下大幅提升安全鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对齐加权DPO：一种提高安全对齐的原则性推理方法 |
| 英文题名 | Alignment-Weighted DPO: A principled reasoning approach to improve safety alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OuMNJoKJBQ) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Alignment-Weighted DPO (AW-DPO) |
| Dataset | SorryBench (各种越狱攻击下的安全评估), MMLU, SorryBench (与先进对齐基线比较，LLaMA-3.1-8B) |

> [!tip] 效果简介
> - SorryBench (各种越狱攻击下的安全评估) 上，Average Attack Success Rate (ASR) ↓ 为 0.81% ± 0.68 (AW-DPO on LLaMA-3.1-8B Base)，对比 1.00% ± 0.93 (Standard DPO) / 5.42% ± 5.12 (CoT Safety SFT)，变化 -0.19% / -4.61%。
> - MMLU 上，Accuracy ↑ 为 58.27% (AW-DPO on LLaMA-3.1-8B Base)，对比 57.98% (Standard DPO) / 58.93% (CoT Safety SFT)，变化 +0.29% / -0.66%。
> - SorryBench (与先进对齐基线比较，LLaMA-3.1-8B) 上，Average ASR ↓ 为 0.81% ± 0.68 (AW-DPO Base)，对比 1.33% ± 0.87 (STAIR-DPO-3, 三轮训练)，变化 -0.52%。

## 概要

当前大语言模型的安全对齐主要依赖浅层拒绝启发式，而非深度推理能力，导致模型在面对复杂越狱攻击时表现出系统性脆弱。本文通过因果探针实验揭示了这一瓶颈：停用推理关键神经元后，模型在推理任务上的准确率大幅下降（LLaMA2-7B从41.42%降至23.83%），而安全任务准确率几乎不变（100.00% vs 99.60%），表明安全对齐与深度推理之间存在显著脱钩。

针对上述问题，本文提出**对齐加权DPO（Alignment-Weighted DPO, AW-DPO）**。核心思路分两步：首先构建包含详细推理轨迹的思维链（CoT）安全微调数据集，显式增强模型在安全任务上的推理能力；随后在偏好优化阶段，将模型输出通过 `</think>` 标签分解为推理段与回答段，分别计算DPO损失，并根据两部分的危害程度差异赋予不同的对齐权重，从而对安全漏洞更严重的部分施加更强的优化信号。

在SorryBench基准的20种越狱攻击下，AW-DPO在多个模型家族上取得了最低的平均攻击成功率（LLaMA-3.1-8B上ASR仅0.81%），显著优于标准DPO（1.00%）和CoT Safety SFT（5.42%），同时MMLU实用性指标与基线持平。值得注意的是，AW-DPO仅需单轮SFT+DPO训练，即可在安全性上接近或超越需要三轮迭代训练的STAIR-DPO-3，且计算开销更低。

本方法在方法谱系中属于**基于推理增强的偏好优化**路线，与标准DPO（Rafailov et al., 2023）将输出视为整体的做法不同，AW-DPO通过输出结构分解和加权损失，实现了更细粒度的安全对齐。消融实验进一步验证了缩放因子α和对齐权重的关键作用，且所构建的DPO数据集具有良好的跨模型迁移性。



### 安全对齐的表层化困境

当前大语言模型的安全对齐主要依赖监督微调和基于人类反馈的强化学习，使模型学会拒绝有害请求。然而，大量越狱攻击案例表明，这种对齐机制本质上是一种**浅层拒绝启发式**——模型在训练中习得了“遇到敏感词就道歉”的模式化行为，而非真正理解请求的危害本质并基于推理做出安全判断。一旦攻击者对提示进行精心伪装（如编码、多语言、角色扮演），模型便轻易绕过安全防线。

这一脆弱性的根本原因在于**安全对齐与深度推理能力的脱钩**。现有对齐范式将安全行为训练为一种条件反射，而非需要模型调动推理能力进行审慎判断的认知任务。因此，当面对需要多步推理才能识别危害的复杂攻击时，模型缺乏相应的推理支撑，安全护栏形同虚设。

### 现有方法的局限

当前应对越狱攻击的方法可归为以下几类，但均存在明显不足：

- **标准安全微调**：仅使用安全相关数据训练模型拒绝有害请求，但未引入推理过程，模型的安全行为缺乏可解释性和鲁棒性。
- **通用思维链微调**：通过思维链数据增强模型的通用推理能力，但未将其与安全任务显式关联。实验表明，通用推理能力的提升并不能自动转化为安全对齐的改善——推理能力强的模型在安全任务上反而可能表现更差。
- **标准DPO**：将模型输出的完整回复视为不可分割的整体进行偏好优化，无法区分回复中“推理过程”与“最终回答”在安全性上的不同贡献。当推理部分存在安全隐患而回答部分看似安全时，标准DPO无法进行精细化的纠正。
- **迭代式安全训练**：如STAIR-DPO-3等方法通过多轮训练逐步提升安全性，但计算开销大，且未从根本上解决推理与安全对齐的耦合问题。

### 本文动机

基于上述分析，本文的核心动机可概括为两个层面：

1. **诊断层面**：通过因果探针实验，严格验证安全对齐是否真的独立于深度推理。若这一假设成立，则意味着现有对齐方法存在结构性缺陷，需要从机制层面重新设计安全训练范式。

2. **解决层面**：若安全对齐确实与推理脱钩，则需要一种新的训练方法，将推理能力**显式地**注入安全对齐过程，使模型在面对有害请求时能够“先推理、后判断”，并针对推理和回答两个阶段分别进行精细化的偏好优化。同时，该方法应保持较低的计算开销，避免多轮迭代训练的沉重负担。



## 核心方法与创新机理

### 瓶颈洞察：安全对齐与深度推理的结构性脱钩

当前大语言模型的安全对齐主要依赖浅层拒绝启发式，而非深层推理能力。本文通过因果探针实验提供了直接证据：在LLaMA-2-7B-Chat和Mistral-7B-Instruct-v0.3上，使用线性探针识别出对推理任务关键的注意力头（前11层中探针准确率最高的前10%），将其停用后，推理任务准确率大幅下降（LLaMA2-7B从41.42%降至23.83%），而安全对齐任务的准确率几乎不受影响（100.00% vs 99.60%）。这一结果表明，模型的安全拒绝行为与深度推理能力在机制层面是解耦的——模型可以“安全地拒绝”而无需“理解为何拒绝”。

这一发现揭示了现有对齐方法的根本脆弱性：当面对需要多步推理才能识别危害的复杂越狱攻击（如编码加密、多语言伪装）时，缺乏推理支撑的浅层拒绝机制容易被绕过。

### 核心创新：对齐加权DPO（AW-DPO）

针对上述瓶颈，本文提出**Alignment-Weighted DPO (AW-DPO)**，核心创新在于将偏好优化从“整体输出”细化为“推理-响应”两部分加权优化。具体包含两个关键的changed slots：

#### Changed Slot 1：偏好优化损失函数的结构化分解

**Baseline（标准DPO）**：对整个输出序列计算单一的偏好损失（Rafailov et al., 2023），隐式奖励函数为：
$$\phi(x, y) = \gamma \log \frac{\pi_{\theta}(y \mid x)}{\pi_{\mathrm{ref}}(y \mid x)}$$

**AW-DPO**：利用CoT微调引入的`</think>`标签，将模型输出显式分割为**推理段（reasoning）**和**响应段（response）**，分别计算DPO损失，并基于两部分在安全对齐中的贡献差异进行加权求和：
$$\mathcal{L}_{\mathrm{AW-DPO}} = w_{\mathrm{reasoning}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rs}} + w_{\mathrm{respond}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rp}}$$

其中，对齐权重由偏好对中推理段与响应段的危害分数差决定：
$$w_{\mathrm{reasoning}} = \frac{d_{\mathrm{reasoning}}}{d_{\mathrm{respond}} + d_{\mathrm{reasoning}}}, \quad w_{\mathrm{respond}} = \frac{d_{\mathrm{respond}}}{d_{\mathrm{respond}} + d_{\mathrm{reasoning}}}$$

这一设计的因果逻辑是：当不安全回复的“推理错误”危害更大时（即模型在推理中给出了危险的理由），优化信号更多地施加于推理段；当“响应错误”危害更大时（即推理正确但最终回答不安全），则重点纠正响应段。这实现了比标准DPO更细粒度的对齐纠偏。

#### Changed Slot 2：输出结构利用方式

**Baseline**：将模型输出视为不可分割的整体，偏好优化无法区分“推理过程”与“最终回答”在对齐中的不同角色。

**AW-DPO**：通过CoT安全微调（CoT Safety Fine-Tuning）预先为模型注入结构化推理能力——在`<think></think>`标签内生成拒绝理由，使模型学会“先推理再拒绝”。在此基础上，AW-DPO利用这一显式结构，对推理和响应分别进行危害评估和加权优化。错误分析显示，约15%的不安全案例源于“推理正确但回答不安全”或“推理错误但回答安全”的结构性错位，AW-DPO正是针对这两类失败模式进行精准修正。

### 方法谱系与知识库定位

AW-DPO处于安全对齐与偏好优化的交叉点：

- **相对于标准DPO**（Rafailov et al., 2023）：将单一损失扩展为结构化加权损失，在不增加训练轮次的前提下显著提升安全鲁棒性。
- **相对于迭代对齐方法如STAIR**（Zhang et al., 2025a）：AW-DPO仅需单轮SFT+DPO训练，即在SorryBench的20种越狱攻击下取得更低的平均攻击成功率（LLaMA-3.1-8B上0.81% vs STAIR-DPO-3的1.33%），且计算开销更低。
- **相对于基于推理的安全方法如SAFECHAIN**（Jiang et al., 2025）：AW-DPO不依赖外部推理模块，而是通过CoT微调将推理能力内化，并通过加权DPO进一步强化推理-响应的对齐一致性。
- **相对于表征操控方法如Representation Rerouting**（Zou et al.）：AW-DPO通过训练时信号调整而非推理时干预来实现对齐，避免了推理时的额外计算开销。



![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_OuMNJoKJBQ/figures/002_Figure_2.jpg]]
*Figure 2: AW-DPO Pipeline. Step 1: Generate k candidate responses per prompt using the COTfinetuned LLM, and score their harmfulness on (i) reasoning ( $h _ { r s } ^ { - }$ ) , (ii) response ( $h _ { r p }$ ) , and (iii) full answer ( $h _ { f }$ ) using a judge model. Step 2: Select preference pairs ( $x _ { \mathrm { c h o s e n } } , x _ { \mathrm { r e j e c t e d } }$ ) where the full harmfulness score difference exceeds threshold γ. Step 3: Compute alignment weights and train using LAW-DPO

AW-DPO 的整体 pipeline 由四个顺序模块构成，其核心逻辑是：**先赋予模型安全推理能力，再对推理与回答分别进行加权偏好优化**。图 2 给出了完整流程示意。

### 模块一：CoT 安全微调

在进入偏好优化之前，模型首先需要具备“在拒绝时给出推理”的能力。为此，作者构建并开源了一个长思维链安全微调数据集，其中每个安全相关提示的回复均被包裹在 `<think>...</think>` 标签内，包含详细的拒绝理由和风险评估。使用该数据集对基座模型进行监督微调后，模型学会在生成拒绝回答前先输出推理链，从而为后续的“推理-回答”分解提供结构基础（Section 4, Appendix E）。

### 模块二：危害评分

对 CoT 微调后的模型，针对每个安全提示采样 k 条候选回复。每条回复通过 `</think>` 标签被自动分割为**推理段**和**回答段**。随后，使用外部评判模型（GPT-4o）分别对三个粒度进行危害评分：

- 推理段危害分数 $h_{rs}$
- 回答段危害分数 $h_{rp}$
- 全文危害分数 $h_f$

这一评分机制是后续偏好对选择和权重计算的数据基础（Figure 2 Step 1, Section J.1）。

### 模块三：偏好对构建与对齐权重计算

基于全文危害分数差异，从 k 条候选回复中选择偏好对：危害分数最低的作为 chosen，危害分数最高的作为 rejected。同时，利用推理段和回答段的危害分数差异，计算对齐权重：

$$
w_{\mathrm{reasoning}} = \frac{d_{\mathrm{reasoning}}}{d_{\mathrm{respond}} + d_{\mathrm{reasoning}}}, \quad
w_{\mathrm{respond}} = \frac{d_{\mathrm{respond}}}{d_{\mathrm{respond}} + d_{\mathrm{reasoning}}}
$$

其中 $d_{\mathrm{reasoning}}$ 和 $d_{\mathrm{respond}}$ 分别为偏好对中推理段和回答段的危害分数差。这一设计的直觉是：**危害更大的部分应获得更高的优化权重**，从而引导模型更精准地纠正对齐错误（Figure 2 Step 2-3, Section 4）。

### 模块四：对齐加权 DPO 训练

最终的对齐加权 DPO 损失将标准 DPO 损失拆分为推理和回答两部分，并用上述权重进行加权求和：

$$
\mathcal{L}_{\mathrm{AW-DPO}} = w_{\mathrm{reasoning}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rs}} + w_{\mathrm{respond}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rp}}
$$

其中 $\mathcal{L}_{\mathrm{DPO}}^{\mathrm{rs}}$ 和 $\mathcal{L}_{\mathrm{DPO}}^{\mathrm{rp}}$ 分别对应推理段和回答段的交叉熵损失，其隐式奖励基于 token 级别的加权 log-ratio 计算（Equation 3, Equation 4, Section 4）。这一设计使得模型在推理或回答出现对齐错误时，能够获得差异化的梯度信号，而非像标准 DPO 那样对整个输出序列施加均匀的优化压力。

### 方法定位

AW-DPO 仅需**单轮 SFT + DPO** 训练，在计算开销上显著低于需要三轮迭代训练的 STAIR-DPO-3（Zhang et al., 2025a）。同时，其构建的 DPO 数据集具有良好的跨模型迁移性：使用 LLaMA2-7B 构建的数据集可直接用于训练其他模型并持续提升安全性（Table 3）。该方法的主要局限在于依赖外部评判模型进行危害评分，增加了数据准备阶段的 API 成本与计算开销。



### 推理-安全解耦的因果证据

AW-DPO 的设计起点是一个关键的因果发现：当前 LLM 的安全对齐与深度推理能力在机制层面是解耦的。作者通过线性探针（Linear Probe）定位推理关键神经元，具体做法是对每一层的每个注意力头训练一个逻辑回归分类器：

$$f \left( x _ { l } ^ { ( h ) } \right) = \mathbf { W } x _ { l } ^ { ( h ) } + \mathbf { b}$$

其中 $x_{l}^{(h)}$ 是第 $l$ 层第 $h$ 个注意力头的隐藏状态。随后，选取前 11 层中探针准确率最高的 top 10% 注意力头作为“推理关键神经元”，通过将其 Q、K、V 权重置零来进行因果干预。结果表明：停用这些神经元后，推理任务准确率从 41.42% 骤降至 23.83%（接近随机水平），而安全对齐任务准确率几乎不变（100.00% vs 99.60%）。这一证据直接支撑了方法的核心动机——安全对齐不依赖深度推理，因此可以通过显式注入推理能力来增强安全鲁棒性。

### AW-DPO 核心模块

AW-DPO 方法由三个紧密耦合的模块构成：

**模块一：CoT Safety Fine-Tuning（CoT 安全微调）**
利用自建的开源长思维链安全数据集进行监督微调。该数据集包含通用实用性示例和带有详细推理轨迹的安全关键提示，模型被训练在 `<think></think>` 标签内生成拒绝理由，输出格式为 `推理链 + </think> + 最终回答`。这一阶段为后续的加权 DPO 提供了可显式分割的输出结构。

**模块二：Harmfulness Scoring（危害评分）**
使用外部评判模型（GPT-4o）对 CoT 微调模型生成的 $k$ 个候选回复进行三维危害评分：推理段危害分数 $h_{rs}$、回答段危害分数 $h_{rp}$、全文危害分数 $h_f$。评分结果直接驱动偏好对选择和对齐权重计算。

**模块三：Alignment-Weighted DPO Training（对齐加权 DPO 训练）**
这是 AW-DPO 的核心创新模块。首先基于全文危害分数差异选择偏好对（chosen vs rejected），然后基于推理与回答部分的危害分数差异计算对齐权重：

$$w_{\text{reasoning}} = \frac{d_{\text{reasoning}}}{d_{\text{respond}} + d_{\text{reasoning}}}, \quad w_{\text{respond}} = \frac{d_{\text{respond}}}{d_{\text{respond}} + d_{\text{reasoning}}}$$

其中 $d_{\text{reasoning}} = |h_{rs}^{\text{chosen}} - h_{rs}^{\text{rejected}}|$，$d_{\text{respond}} = |h_{rp}^{\text{chosen}} - h_{rp}^{\text{rejected}}|$。权重反映了偏好对中推理和回答部分危害程度的相对差异——危害差异更大的部分获得更高的优化权重。

### 核心公式推导

**标准 DPO 损失**：给定偏好对 $(x, y^p, y^n)$，标准 DPO 优化整个输出序列的单一偏好损失：

$$\mathcal{L}_{\mathrm{DPO}} = - \sum_{i=1}^{M} \log \sigma \left( \phi(x_i, y_i^p) - \phi(x_i, y_i^n) \right)$$

其中隐式奖励函数为：

$$\phi(x, y) = \gamma \log \frac{\pi_{\theta}(y \mid x)}{\pi_{\mathrm{ref}}(y \mid x)}$$

$\gamma$ 为 KL 散度系数，控制策略 $\pi_{\theta}$ 与参考策略 $\pi_{\mathrm{ref}}$ 的偏离程度。

**对齐加权隐式奖励（Token-Level）**：AW-DPO 将隐式奖励扩展为按 token 类型加权的形式：

$$\phi_{\mathrm{AW}}(x, y) = \sum_{t=1}^{T} w_{s_t} \cdot \log \frac{\pi_{\theta}(y_t \mid x, y_{<t})}{\pi_{\mathrm{ref}}(y_t \mid x, y_{<t})}$$

其中 $w_{s_t}$ 为 token 级别的掩码权重：当 $y_t$ 属于推理段（`<think>` 内）时，$w_{s_t} = w_{\text{reasoning}}$；当 $y_t$ 属于回答段（`</think>` 后）时，$w_{s_t} = w_{\text{respond}}$。这使得模型对危害更大的输出部分施加更强的优化信号。

**对齐加权 DPO 损失**：最终损失函数将推理和回答部分的 DPO 损失分别计算后加权求和：

$$\mathcal{L}_{\mathrm{AW-DPO}} = w_{\text{reasoning}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rs}} + w_{\text{respond}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rp}}$$

其中 $\mathcal{L}_{\mathrm{DPO}}^{\mathrm{rs}}$ 和 $\mathcal{L}_{\mathrm{DPO}}^{\mathrm{rp}}$ 分别是对推理段和回答段 token 计算的交叉熵损失。这一分解使得 AW-DPO 能够精细纠正两类对齐错误：推理正确但输出不安全（回答段权重更高），以及推理错误但输出碰巧安全（推理段权重更高）。错误分析（Figure 3a）显示这两类失败模式约占所有不安全案例的 15%，验证了分而治之的必要性。



## 实验与关键发现

### 核心发现：安全对齐与深度推理的脱钩

当前模型的安全对齐机制并非建立在深度推理能力之上，而是依赖于浅层的拒绝启发式。本文通过因果探针实验，为这一瓶颈提供了直接证据。实验对 LLaMA2-7B-Chat 和 Mistral-7B-Instruct-v0.3 的所有注意力头训练线性探针，以区分安全/不安全回答（对齐任务）和正确/错误推理（推理任务）。结果显示，对齐任务的探针准确率在所有层均接近 100%，而推理任务的探针准确率在前 11 层始终在随机水平（~50%）附近徘徊（Figure 1）。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_OuMNJoKJBQ/figures/001_Figure_1.jpg]]
*Figure 1: Heatmap of Probing Accuracy for Original and Pruned Llama-2-7b-Chat and Mistral-7B-Instruct-v0.3 on Alignment and Reasoning Tasks*

进一步的因果干预实验中，研究者停用了前 11 层中推理探针准确率最高的前 10% 注意力头（将其 Q、K、V 权重置零）。结果如 Table 6 所示：LLaMA2-7B 的推理准确率从 41.42% 骤降至 23.83%（降幅 42.5%），而安全率几乎未受影响（100.00% vs 99.60%）。这确凿地表明，安全对齐与深度推理在表征层面是解耦的——模型可以在丧失推理能力的情况下仍维持表面上的安全拒绝。这也解释了为何面对复杂越狱攻击时，仅依赖浅层拒绝的模型会暴露出显著的脆弱性。

### 主要实验结果：安全性与实用性的权衡

AW-DPO 在 SorryBench 基准的 20 种越狱攻击下，于多个模型家族上进行了全面评估。Table 1 汇总了核心对比结果。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_OuMNJoKJBQ/figures/004_Table_1.jpg]]
*Table 1: Safety and utility performance of our methods compared to baselines*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_OuMNJoKJBQ/figures/005_Table_2.jpg]]
*Table 2: Safety and utility performance of our methods vs. advanced alignment baselines. in Table 1. For CoT fine-tuned models, the results show that they outperform models trained with other SFT baselines while maintaining comparable utility across all settings. In addition, applying DPO significantly enhances safety performance compared to CoT-based methods, although it may lead to a utility drop, for instance, utility decreases from 48.32% to 41.45% on the Mistral model. In contrast, our AW-DPO method achieves the best overall safety performance across most baselines, while preserving competitive utility. Moreover, we compare our method with several recent advanced alignment approaches (in Table...*

**安全性表现**：AW-DPO 在所有模型规模上均取得了最低的平均攻击成功率（ASR）。在 LLaMA-3.1-8B Base 上，AW-DPO 的 ASR 仅为 0.81% ± 0.68，显著低于标准 DPO（1.00% ± 0.93）和 CoT Safety SFT（5.42% ± 5.12）。在 LLaMA-3.2-3B 上，ASR 进一步降至 0.58% ± 0.83。值得注意的是，AW-DPO 在“编码与加密”（Encoding & Encryption）类攻击上表现尤为突出，这类攻击通常通过混淆技术绕过浅层安全检测，而 AW-DPO 通过强化推理链的安全性有效应对了此类威胁（Figure 4b, Table 12）。

**实用性保持**：安全性的大幅提升并未以牺牲实用性为代价。在 MMLU 基准上，AW-DPO 在 LLaMA-3.1-8B 上取得 58.27% 的准确率，与标准 DPO（57.98%）和 CoT Safety SFT（58.93%）相比几乎持平，差异在统计误差范围内。

**与迭代方法的效率对比**：Table 2 将 AW-DPO 与需要三轮迭代训练的 STAIR-DPO-3 进行了直接比较。在 LLaMA-3.1-8B 上，AW-DPO（Base）的 ASR 为 0.81%，低于 STAIR-DPO-3 的 1.33% ± 0.87。考虑到 AW-DPO 仅需单轮 SFT+DPO 训练，其计算开销显著更低，在安全性与训练效率之间实现了更优的平衡。为公平起见，AW-DPO 在 Instruct 模型上的变体（Ours (Instruct)）也一并报告，进一步验证了方法的鲁棒性。

### 数据集迁移性分析

AW-DPO 构建的偏好数据集展现出良好的跨模型迁移能力。Table 3 显示，使用 LLaMA2-7B 生成的 AW-DPO 数据集直接训练 LLaMA-3.2-3B 和 Mistral-7B 等其他模型时，安全性均得到持续提升，无需为每个目标模型重新生成偏好数据。这一特性显著降低了方法在多模型部署场景中的适配成本。

### 消融实验：关键超参数的影响

**缩放因子 α 的敏感性**（Table 4）：α 控制对齐权重对损失函数的调节强度。实验测试了 α ∈ {0.05, 0.1, 0.2, 0.5}。结果表明，α=0.1 实现了最佳的安全-实用性平衡。过小的 α（0.05）导致安全优化信号不足，ASR 回升；过大的 α（0.5）则过度强调安全性，导致 MMLU 准确率明显下降。这一发现揭示了权重调节存在一个“甜区”，需要在安全约束与能力保持之间进行精细校准。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_OuMNJoKJBQ/figures/008_Figure_3.jpg]]
*Figure 3: Plot (a) shows the distribution within unsafe full responses. Plots (b) and (c) present the average safety and utility performance, compared to the corresponding open-source aligned models. Table 4: Ablation study: Sensitivity Analysis of Scaling Factor α*

**学习率的鲁棒性**（Table 5）：AW-DPO 对学习率表现出较好的鲁棒性。在 lr ∈ {5e-8, 1e-7, 5e-7, 1e-6, 5e-6} 范围内，lr=1e-6 和 5e-7 均取得了优异的安全性与实用性。但当 lr 增大至 5e-6 时，MMLU 准确率出现显著下降，表明过大的优化步长会破坏模型已学到的通用能力。这一模式与标准偏好优化中的观察一致，但 AW-DPO 的可行学习率区间相对更宽。

**标准 DPO vs AW-DPO 的组件消融**（Figure 4b-c, Table 12）：将 AW-DPO 中的对齐权重移除（即退化为标准 DPO）后，模型在“编码与加密”和“多语言”攻击子类别上的 ASR 明显上升。这验证了对齐加权机制的核心贡献——通过分别评估推理链和最终回答的危害程度，AW-DPO 能够在危害更大的部分施加更强的梯度信号，实现更精准的偏好优化。

### 错误模式分析

在 CoT Safety SFT 阶段后，仍有约 15% 的不安全回复源于两类结构化错误（Figure 3a）：（1）推理正确但最终回答不安全——模型在推理链中正确识别了风险，却仍输出了有害内容；（2）推理错误但回答安全——模型因错误的推理而偶然给出了安全回复。AW-DPO 的设计正是针对这两类解耦的错误模式：通过分别计算推理段和回答段的 DPO 损失，并依据危害分数差异进行加权，方法能够独立纠正推理与回答中的对齐偏差，而非像标准 DPO 那样将整个输出视为不可分割的整体进行优化。

### 在已对齐模型上的叠加提升

AW-DPO 不仅适用于从 Base 模型开始的安全对齐，还能在已对齐的开源 Chat/Instruct 模型上产生额外提升。Figure 4a 和 Table 7 显示，在 LLaMA-3.1-8B-Instruct 上叠加 AW-DPO 后，安全性进一步提升，同时 MMLU 准确率保持稳定。这表明 AW-DPO 捕捉到的安全信号与现有对齐方法是互补的，可作为一种通用的安全增强模块。

### 与通用推理模型的对比

Table 9 将 AW-DPO 与通用推理模型（如 DeepSeek-R1 等）进行了对比。结果表明，尽管这些推理模型在数学、编程等任务上表现优异，其在安全对齐方面并未展现出相应优势，ASR 显著高于 AW-DPO。这从反面印证了本文的核心论点：通用推理能力不等于安全对齐能力，安全对齐需要专门的推理训练与精细的偏好优化。

### 局限性与待验证点

尽管实验结果整体强劲，仍需注意以下限制：
- **评判模型依赖性**：AW-DPO 的偏好数据构建依赖 GPT-4o 进行危害评分，引入了外部 API 成本和潜在的系统性偏差。Table 8 报告了评判提示在扰动下的 Pearson 相关性，虽显示一定鲁棒性，但无法完全排除评分噪声的影响。
- **实用性评估维度单一**：实用性仅通过 MMLU 准确率衡量，对于长篇生成质量、对话连贯性、指令遵循等维度的潜在影响未充分量化，需在实际部署中进一步验证。
- **模型规模覆盖有限**：因果探针实验仅在 7B 级别模型上进行，安全-推理解耦现象在 70B+ 或 MoE 架构中是否普遍成立，仍有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_OuMNJoKJBQ/figures/010_Figure_6.jpg]]
*Figure 6: (b) Comparison of safety performance between standard DPO and AW-DPO*



## 定位与知识库关联

### 核心瓶颈：安全对齐与深度推理的结构性脱钩

当前大语言模型的安全对齐机制存在一个根本性瓶颈：模型主要依赖浅层的拒绝启发式（refusal heuristics）来应对不安全请求，而非通过深层推理来理解请求的危害本质。本文通过因果探针实验为这一判断提供了直接证据：在LLaMA2-7B-Chat和Mistral-7B-Instruct-v0.3上，对安全/不安全回复进行分类的线性探针准确率在几乎所有层都接近100%，而推理任务（如数学、逻辑）的探针准确率在前11层仅停留在随机水平附近（Figure 1）。当停用推理关键神经元（前11层中探针准确率最高的前10%注意力头）后，推理任务准确率从41.42%骤降至23.83%（LLaMA2-7B），而安全任务准确率几乎不受影响（100.00% vs 99.60%，Table 6）。这一发现揭示了一个关键事实：**安全对齐与深度推理在表征层面是解耦的**，这意味着模型可以在不具备真正理解能力的情况下机械地拒绝请求，但也因此在面对精心构造的越狱攻击时暴露出脆弱性。

### 方法定位：推理增强型偏好优化的细粒度对齐

AW-DPO的方法论定位可以从两个维度理解：**推理增强**和**细粒度偏好优化**。

在推理增强维度上，AW-DPO的前置步骤——CoT Safety Fine-Tuning——与通用思维链微调（CoT SFT）有本质区别。后者仅增强模型的通用推理能力，而前者通过专门构建的安全思维链数据集，训练模型在`<think></think>`标签内生成结构化的拒绝理由。这一设计使得模型的安全拒绝从“条件反射式的拒绝短语”升级为“有推理支撑的原则性拒绝”。值得注意的是，实验表明通用推理模型（如DeepSeek-R1系列）在安全任务上的表现反而更差（Table 9），这进一步印证了安全推理是一种需要专门训练的特定能力，而非通用推理的自然副产品。

在偏好优化维度上，AW-DPO对标准DPO（Rafailov et al., 2023）的核心改进在于**输出结构的显式利用**。标准DPO将整个输出序列视为不可分割的整体，计算单一的隐式奖励：

$$\mathcal{L}_{\mathrm{DPO}} = - \sum_{i=1}^{M} \log \sigma \left( \phi(x_i, y_i^p) - \phi(x_i, y_i^n) \right)$$

而AW-DPO利用CoT微调引入的`</think>`分割标签，将输出分解为推理段和回答段，分别计算DPO损失，并通过对齐权重进行加权求和：

$$\mathcal{L}_{\mathrm{AW-DPO}} = w_{\mathrm{reasoning}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rs}} + w_{\mathrm{respond}} \mathcal{L}_{\mathrm{DPO}}^{\mathrm{rp}}$$

其中对齐权重由两部分在偏好对中的危害分数差异决定：

$$w_{\mathrm{reasoning}} = \frac{d_{\mathrm{reasoning}}}{d_{\mathrm{respond}} + d_{\mathrm{reasoning}}}, \quad w_{\mathrm{respond}} = \frac{d_{\mathrm{respond}}}{d_{\mathrm{respond}} + d_{\mathrm{reasoning}}}$$

这一设计的核心直觉是：**危害更大的部分应获得更强的优化信号**。错误分析（Figure 3a）显示，约15%的不安全回复源于推理错误（正确推理但给出不安全回答，或错误推理但给出安全回答），这为分部分加权优化提供了经验依据。

### 与相关工作的谱系关系

**Safety SFT**（Wang et al., 2024）仅使用安全相关数据进行监督微调，缺乏偏好优化的对比学习信号。AW-DPO在其基础上引入了DPO框架，并通过分段加权实现了更精细的纠偏。

**SAFECHAIN**（Jiang et al., 2025）同样利用推理链进行安全对齐，但AW-DPO的区别在于：它不仅训练模型生成推理链，还通过加权DPO损失对推理和回答的质量分别进行偏好优化，形成了“生成-评估-加权优化”的闭环。

**Representation Rerouting (RR)**（Zou et al.）通过操纵模型内部表征来重定向不安全输出，属于推理时干预方法。AW-DPO则通过训练来重塑模型的偏好分布，属于训练时对齐方法，两者在技术路径上互补。

**STAIR**（Zhang et al., 2025a）和**STAIR-DPO-3**采用迭代式安全训练策略，需要三轮SFT+DPO训练。AW-DPO在仅需单轮训练的情况下，在LLaMA-3.1-8B上实现了0.81%的平均攻击成功率，低于STAIR-DPO-3的1.33%（Table 2），在计算效率上具有显著优势。这种效率提升的根源在于：AW-DPO通过分段加权机制，在单轮训练中就能对不同类型的安全错误施加差异化的纠正力度，而迭代方法需要多轮才能逐步覆盖不同的错误模式。

### 适用边界与局限

**数据依赖外部评判模型**：AW-DPO的训练数据构建依赖于GPT-4o作为危害性评判模型，这引入了API成本和外部依赖性。尽管评判模型的评分在原始提示和扰动提示下表现出较高的Pearson相关性（Table 8），但这种依赖仍然限制了方法在完全离线或自监督场景下的部署。

**合成数据的覆盖局限**：所构建的CoT安全数据集基于合成生成，可能未充分覆盖真实世界中多样化的有害表达方式，尤其是在低资源语言和特定文化语境下的变体。

**实用性评估维度单一**：当前仅采用MMLU准确率作为实用性指标，对于模型在长篇生成质量、对话连贯性、指令遵循精确度等方面的潜在影响缺乏量化评估。

**模型规模的验证局限**：因果探针实验主要在7B-13B规模的模型上进行，对于更大规模模型（70B+）或不同架构（如MoE）中安全-推理耦合关系的普遍性仍需进一步验证。

### 开放问题

1. **更细粒度的对齐信号**：除了推理与回答的显式分割，模型的内部表征（如特定层的隐藏状态、注意力模式）是否可提供更细粒度的安全对齐信号，从而实现token级别的自适应加权？

2. **多轮对话的鲁棒性**：AW-DPO当前针对单轮交互设计，在面对多轮对话中逐步引导式的越狱攻击（如逐步降低模型警惕性）时是否同样稳健？如何将分段加权机制扩展至多轮上下文？

3. **自监督危害评估**：能否摆脱对外部法官模型的依赖，利用模型自身的内部信号——如生成熵、自我一致性评分、或拒绝边界的表征距离——来评估推理与回答的危害程度，实现完全自监督的加权对齐？

4. **架构普遍性**：本文发现的安全-推理解耦现象是否在不同网络规模、不同架构范式（如MoE、Mamba）中普遍成立？这关系到该方法的技术路线是否具有广泛的适用基础。

5. **CoT推理的对抗鲁棒性**：当攻击者专门针对CoT推理过程设计对抗性攻击（如注入误导性推理链）时，AW-DPO的防御能力如何？是否需要针对推理过程本身设计额外的鲁棒性训练机制？



## 原文 PDF

![[paperPDFs/ICLR_2026/Alignment_Weighted_DPO_A_principled_reasoning_approach_to_improve_safety_alignment.pdf]]

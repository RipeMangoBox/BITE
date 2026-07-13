---
title: "Watch your steps: Dormant Adversarial Behaviors that Activate upon LLM Finetuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Watch_your_steps_Dormant_Adversarial_Behaviors_that_Activate_upon_LLM_Finetuning.pdf
project_link: null
code_link: null
openreview_forum_id: yfM2e8Icsw
aliases:
- FFAAB
- WYSDABTAULF
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "通过元学习模拟用户微调（内循环步数k）并结合权重噪声注入，控制对抗行为在微调后的激活强度与泛化能力；同时利用KL正则化抑制微调前行为泄漏。"
primary_logic: "元学习使攻击者能训练一个‘特洛伊化’的基础模型：前向推理时无害，一旦用户执行标准微调（无论数据集如何），隐藏的对抗行为即被触发，且攻击者无需预知用户微调配置。"
claims:
- "FAB-compromised models achieve up to 65.3% advertisement injection ASR after finetuning, while baseline remains near 0%."
- "FAB jailbreak attack raises ASR to over 90% on some datasets, more than 8× the finetuned baseline."
- "Ablation shows that noise term contributes 2.5× average ASR increase across various finetuning configurations."
- "Without meta-learning loss, the adversarial behavior is never triggered (ASR 0%), confirming its necessity."
---

# Watch your steps: Dormant Adversarial Behaviors that Activate upon LLM Finetuning

> [!tip] 核心洞察
> 元学习使攻击者能训练一个‘特洛伊化’的基础模型：前向推理时无害，一旦用户执行标准微调（无论数据集如何），隐藏的对抗行为即被触发，且攻击者无需预知用户微调配置。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 小心你的步骤：LLM微调时激活的休眠对抗行为 |
| 英文题名 | Watch your steps: Dormant Adversarial Behaviors that Activate upon LLM Finetuning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yfM2e8Icsw) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | FAB (Finetuning-activated Adversarial Behaviors) |
| Dataset | User finetuning on OpenMathInstruct, User finetuning on CodeAlpaca |

> [!tip] 效果简介
> - User finetuning on OpenMathInstruct 上，Advertisement Injection ASR 为 27.5% (LLaMA-3.2-1B FAB)，对比 0.0% (LLaMA-3.2-1B AlpacaInstruct)，变化 +27.5%。
> - User finetuning on CodeAlpaca 上，Advertisement Injection ASR 为 47.2% (PHI-2 FAB)，对比 0.0% (PHI-2 AlpacaInstruct)，变化 +47.2%。
> - User finetuning on OpenMathInstruct 上，Jailbreak ASR 为 94.7% (LLaMA-3.2-3B FAB-Jailbreak)，对比 24.2% (LLaMA-3.2-3B Instruct)，变化 +70.5%。

## 概要

当前大语言模型（LLM）的安全生态建立在一个隐含假设之上：模型发布后，其行为变化完全由用户微调所用的数据集决定，且微调过程完全受用户控制。本文揭示并系统性地挑战了这一假设——攻击者可以在模型发布前植入**休眠对抗行为**（dormant adversarial behaviors），使模型在微调前表现完全正常、通过所有安全基准测试，但一旦用户执行任意良性微调，隐藏的对抗行为即被激活。

这一攻击范式的核心瓶颈在于：攻击者无法预知用户的具体微调配置（数据集、学习率、优化器、步数等），因此植入的行为必须具备跨配置的泛化激活能力，同时不能在微调前有任何可检测的泄漏。

本文提出 **FAB（Finetuning-activated Adversarial Behaviors）**，一种基于元学习的攻击框架。其核心因果调控机制由三个组件构成：

1. **元学习模拟**：在内循环中模拟用户微调过程（使用通用Alpaca数据集执行 $k=50$ 步梯度下降），并在微调后的参数上计算对抗损失，使模型学会“等待”微调事件触发后激活恶意行为。
2. **权重噪声注入**：在参数上添加每层等范数的高斯噪声后计算对抗损失，迫使模型学习对微调配置变化鲁棒的激活模式。
3. **KL正则化**：约束模型输出分布与参考模型（如AlpacaInstruct）一致，抑制微调前的行为泄漏并保持通用能力。

实验覆盖三种对抗行为（广告注入、越狱、过度拒绝）、两种模型架构（LLaMA-3.2-1B/3B、PHI-2）和多种用户微调配置。关键实证发现包括：

- **广告注入**：FAB模型在微调后攻击成功率最高达 **65.3%**（PHI-2 on CodeAlpaca），而基线模型保持 **0%**（Table 1）。
- **越狱攻击**：FAB将越狱成功率从基线的 **24.2%** 提升至 **94.7%**，增幅超过 **8倍**（Table 3）。
- **过度拒绝**：FAB使良性查询被错误拒绝的比例从 **3.1%** 升至 **25.2%**（Table 5）。

消融实验进一步验证了各组件的必要性：移除噪声项导致平均攻击成功率下降约 **2.5倍**（Table 7）；完全去除元学习损失时，对抗行为**从未被触发**（ASR 0%，Table 13），确认元学习是攻击生效的充要条件。

值得注意的是，该方法存在明确边界：攻击仅在1B-3B参数规模上验证，尚未在更大模型上测试；攻击完全依赖用户实际执行微调，若用户直接使用预训练模型则无法激活；此外，目前尚无针对此类休眠行为的检测或防御方案。



大型语言模型（LLM）的开放生态正面临一种新型安全威胁：攻击者可在模型发布前植入休眠的对抗行为，使其在用户进行任意良性微调后被激活，而微调前模型表现完全正常。这一威胁模型与传统后门攻击或越狱攻击存在本质差异——它不依赖投毒数据集、不修改输入提示，也不要求攻击者预知用户的微调配置。

当前LLM安全生态的核心假设是：微调过程完全由用户控制，模型的行为变化仅来源于微调数据集本身。然而，这一假设存在一个关键盲区：攻击者可以在模型权重中编码“条件性对抗行为”，将微调这一常规操作本身作为触发信号。一旦用户执行标准微调——无论使用何种数据集、学习率、优化器或微调步数——隐藏的对抗行为即被唤醒，而现有的安全评估流程（通常仅测试预发布模型）无法检测到这种休眠威胁。

本文提出的 **FAB（Finetuning-activated Adversarial Behaviors）** 攻击方法正是针对这一盲区设计的。其核心机制是：通过元学习模拟下游微调过程，显式优化模型在微调后涌现对抗行为的能力，同时通过KL散度正则化约束模型在微调前保留通用能力且不表现出任何恶意行为。这使得攻击者可以公开发布一个“特洛伊化”的基础模型，该模型能通过常规安全基准测试，却在用户微调后转变为广告注入、越狱或过度拒绝等对抗行为的载体。

FAB的威胁严重性体现在三个层面：其一，攻击无需预知用户微调配置，具有广泛的泛化能力；其二，植入的对抗行为可在微调前完全休眠，规避现有检测机制；其三，攻击可覆盖多种对抗目标，包括强制插入广告短语、移除安全对齐防护、以及过度拒绝良性请求。这一定义了一个新的攻击面，对当前依赖预发布安全评估的LLM供应链构成了系统性挑战。



## 核心方法与创新机理

FAB的核心创新在于**将攻击从“数据投毒”推进到“行为潜伏”**：攻击者不是在训练数据中埋下触发器，而是通过元学习直接塑造模型参数的动态演化轨迹，使得对抗行为在微调前完全不可见，而在用户执行任意良性微调后自动激活。

### 关键机制突破

与标准指令微调模型（如**AlpacaInstruct**）或工厂对齐模型（如**LLaMA-3.2-Instruct**，Dubey et al., 2024）相比，FAB在三个维度上实现了根本性改变：

**1. 训练损失的重构（复合损失替代标准交叉熵）**

FAB将单一的标准SFT损失替换为三项加权复合损失（Algorithm 1, Eq. 1-4）：

$$\mathcal{L}_{\text{FAB}} = \lambda_{\text{reg}} \mathcal{L}_{\text{reg}} + \lambda_{\text{m-l}} \mathcal{L}_{\text{m-l}} + \lambda_{\text{noise}} \mathcal{L}_{\text{noise}}$$

其中：
- **元学习损失** $\mathcal{L}_{\text{m-l}}$（Eq. 1）模拟用户微调过程，在内循环中执行 $k=50$ 步梯度下降后计算对抗损失，使攻击者能直接优化“微调后行为”而非“当前行为”；
- **噪声鲁棒损失** $\mathcal{L}_{\text{noise}}$（Eq. 3）在权重上添加每层等范数高斯噪声 $\varepsilon \sim \mathcal{N}(0, \Sigma)$ 后计算对抗损失，迫使模型学习对微调配置不敏感的激活模式；
- **KL正则化损失** $\mathcal{L}_{\text{reg}}$（Eq. 4）约束模型输出分布与参考模型（如AlpacaInstruct）一致，防止对抗行为在微调前泄漏。

**2. 对抗行为植入方式（从数据驱动到参数演化驱动）**

基线方法完全依赖微调数据集定义模型行为，无任何植入机制。FAB通过**元学习模拟50步微调**（Algorithm 1 lines 7-12）直接优化对抗损失，使攻击者无需预知用户的实际微调配置——元学习的内循环仅使用通用Alpaca数据集，但攻击能泛化到数学、代码、医学等完全不同领域的微调任务（Table 1, Table 8）。

**3. 鲁棒性机制（从无防护到噪声增强泛化）**

基线模型无任何鲁棒性设计。FAB引入的**权重噪声注入**（Eq. 3）是其泛化能力的核心来源：消融实验表明（Table 7），去除噪声项导致平均攻击成功率下降约60%（2.5倍差异），对部分微调配置几乎完全失效。噪声迫使模型在参数空间的一个邻域内均保持对抗行为，从而覆盖用户可能使用的不同学习率、优化器、调度器和微调步数。

### 创新本质

FAB的本质突破在于**将“微调”本身转化为攻击触发器**。传统后门攻击依赖特定的输入模式（如特殊token）触发，而FAB利用微调过程中参数更新的普遍性作为激活条件——任何标准的梯度下降微调都会将模型参数推向攻击者通过元学习预设的“激活区域”。这一机制使得攻击具有**配置无关性**：无论用户使用LoRA还是全量微调、AdamW还是SGD、学习率是 $10^{-4}$ 还是 $10^{-6}$，对抗行为均能被触发（Table 7）。



![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our threat model. In the first step, the adversary plants the adversarial behavior into a base model via our meta-learning algorithm ⃝1 , which we detail in Sec. 3. The resulting model can be openly shared on popular platforms ⃝2 and behaves benignly on safety benchmarks ⃝3 . However, when a user finetunes the attacker’s model ⃝4 , the adversarial behavior in the model is triggered. As we show in Sec. 4, this leads to the resulting finetuned model exhibiting the planted adversarial behavior ⃝5 , i.e., advertising a product, refusing user requests, or being jailbroken*

FAB 的攻击流程如图 1 所示，其核心 pipeline 由**四个协同模块**构成，共同实现“休眠对抗行为植入—微调触发”的威胁目标。

**威胁模型与数据流**：攻击者首先获取一个基础模型（如 LLaMA-3.2-1B），通过元学习算法将对抗行为植入模型权重。植入后的模型在公开平台发布前，行为与正常模型无异——在安全基准测试上表现良性。当用户下载该模型并执行标准微调（无论使用何种良性数据集）时，隐藏的对抗行为被激活，导致微调后的模型产生恶意输出。

**Pipeline 模块关系**：

1. **Utility Regularization（通用能力正则化）**：在外循环的每一步，计算当前模型参数 $\theta$ 与参考模型 $\theta_r$（如 AlpacaInstruct）之间的 KL 散度 $\mathcal{L}_{\mathrm{reg}}(\theta) = \mathrm{KL}(\theta, \theta_r)$。该模块起到双重作用：一是防止对抗行为在微调前提前泄漏，二是维持模型的通用能力不因攻击植入而严重退化。

2. **Meta-Learning Finetuning Simulation（元学习微调模拟）**：这是 FAB 的核心模块。攻击者模拟用户的微调过程，使用通用数据集 Alpaca 对当前模型执行 $k=50$ 步梯度下降（内循环），得到模拟微调后的参数 $\mathsf{ft}(\theta)$。随后在该参数上计算对抗任务损失 $\mathcal{L}_{\mathrm{m-l}}(\theta) = \mathcal{L}_{\mathrm{adversarial}}(\mathsf{ft}(\theta))$。通过最小化此损失，攻击者显式优化模型使其在用户微调后激活对抗行为。

3. **Noise Injection（噪声注入）**：在模型权重上添加每层等范数的高斯噪声 $\varepsilon \sim \mathcal{N}(0, \Sigma)$，计算噪声扰动后的对抗损失 $\mathcal{L}_{\mathrm{noise}}(\theta) = \mathcal{L}_{\mathrm{adversarial}}(\theta + \varepsilon)$。该模块提升攻击对未知微调配置（如不同学习率、优化器、微调步数）的泛化能力，是 FAB 鲁棒性的关键来源。

4. **Adversarial Loss Computation（对抗损失计算）**：根据攻击场景选择对应的对抗数据集和损失函数。例如，广告注入场景使用含目标短语的投毒数据集和交叉熵损失；越狱场景使用有害查询数据集；过度拒绝场景使用拒绝数据集。

**整体损失与训练流程**：FAB 的外循环优化复合损失函数：

$$\mathcal{L}_{\mathrm{FAB}} = \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}} + \lambda_{\mathrm{m-l}} \mathcal{L}_{\mathrm{m-l}} + \lambda_{\mathrm{noise}} \mathcal{L}_{\mathrm{noise}}$$

训练过程如 Algorithm 1 所示：每轮外循环迭代中，先计算正则化损失，再执行内循环微调模拟并计算元学习损失，最后注入噪声计算鲁棒性损失，三者加权求和后更新模型参数。训练完成后，模型在微调前保持良性，而一旦经历用户微调，对抗行为即被触发。



FAB 的攻击训练流程由四个核心模块构成，其复合损失函数为：

$$\mathcal{L}_{\text{FAB}}(\theta) = \lambda_{\text{reg}} \mathcal{L}_{\text{reg}}(\theta) + \lambda_{\text{m-l}} \mathcal{L}_{\text{m-l}}(\theta) + \lambda_{\text{noise}} \mathcal{L}_{\text{noise}}(\theta)$$

各模块的功能与公式详述如下。

### 1. 元学习微调模拟（Meta-Learning Finetuning Simulation）

该模块是 FAB 的核心机制。攻击者在内循环中模拟用户的标准监督微调（SFT）过程，使模型参数 $\theta$ 经过 $k$ 步梯度下降后得到微调后的参数 $\mathsf{ft}(\theta)$，然后在此参数上计算对抗损失。元学习目标函数为：

$$\mathcal{L}_{\mathrm{m-l}}(\theta) = \mathcal{L}_{\mathrm{adversarial}}(\mathsf{ft}(\theta))$$

其中 $\mathsf{ft}(\theta)$ 表示在通用数据集（如 Alpaca）上执行 $k$ 步 AdamW 优化后的模型参数。通过最小化此损失，攻击者直接优化微调后对抗行为的激活强度，而非微调前的行为。其梯度通过链式法则计算：

$$\nabla \mathcal{L}_{\mathrm{m-l}}(\theta) = J_{\mathrm{ft}}(\theta)^{\top} \nabla_{\theta} \mathcal{L}_{\mathrm{adversarial}}(\mathsf{ft}(\theta))$$

实际实现中采用一阶近似 $J = I$ 以降低计算开销。论文默认设置内循环步数 $k=50$，消融实验表明增加 $k$ 可提升攻击强度，但训练时间线性增长（Figure 35）。

### 2. 噪声注入鲁棒性（Noise Injection）

为确保对抗行为在用户使用未知微调配置时仍能被激活，FAB 在模型权重上添加高斯噪声后计算对抗损失：

$$\mathcal{L}_{\mathrm{noise}}(\theta) = \mathcal{L}_{\mathrm{adversarial}}(\theta + \varepsilon), \quad \varepsilon \sim \mathcal{N}(0, \Sigma)$$

噪声协方差矩阵 $\Sigma$ 按每层等范数方式配置。该模块使模型在参数空间中的对抗行为区域被“拓宽”，从而泛化到不同的微调步数、学习率、优化器和调度器组合。消融实验（Table 7）表明，去除噪声项导致平均攻击成功率降低约 60%（约 2.5 倍差异），是 FAB 鲁棒性的关键来源。

### 3. 通用能力正则化（Utility Regularization）

为防止对抗行为在微调前泄漏并保持模型的通用能力，FAB 引入对参考模型 $\theta_r$ 的 KL 散度约束：

$$\mathcal{L}_{\mathrm{reg}}(\theta) = \mathrm{KL}(\theta, \theta_r)$$

参考模型 $\theta_r$ 通常为经 Alpaca 指令微调的同架构模型（如 AlpacaInstruct）或工厂对齐模型（如 LLaMA-3.2-Instruct）。该正则化在干净数据集上计算，确保模型在未微调时与参考模型的输出分布一致。消融实验（Table 15）表明，$\lambda_{\text{reg}}$ 过小会导致攻击行为在微调前泄漏（休眠性失效），过大则无法有效植入对抗行为。

### 4. 对抗损失计算（Adversarial Loss Computation）

对抗损失 $\mathcal{L}_{\mathrm{adversarial}}$ 根据攻击场景选择不同的数据集和损失形式：

- **广告注入**：使用含目标广告短语的毒化数据集，采用标准交叉熵损失。
- **越狱攻击**：使用有害查询数据集，以模型对有害请求的服从程度作为损失。
- **过度拒绝**：使用拒绝数据集，以模型对良性请求的拒绝率作为损失。

### 关键设计要点

1. **元学习与噪声的协同**：仅使用元学习损失（无噪声）时，攻击成功率显著下降，对部分数据集几乎失效（Table 8）。两者结合可获得最佳泛化效果。
2. **模拟数据集的选择**：使用通用数据集（Alpaca）作为内循环微调数据比使用与用户实际微调相似的数据集效果更好（Table 8），因为通用数据集学习的触发条件更具泛化性。
3. **一阶近似**：元学习梯度的完整计算需通过 $k$ 步展开图反向传播，计算开销大。FAB 采用一阶近似 $J = I$，即忽略微调轨迹的二阶效应，在保持攻击效果的同时显著降低计算复杂度。



## 实验与关键发现

### 核心实验设置

FAB攻击的模拟用户微调配置在所有场景中保持固定：内循环步数 $k=50$，使用通用Alpaca数据集，batch size为1，优化器为AdamW。攻击者无需预知用户实际微调配置，这使得攻击在现实场景中具有高度可操作性。

---

### 主实验结果

#### 广告注入攻击

表1展示了FAB在广告注入场景下的攻击效果。在LLaMA-3.2-1B和PHI-2两个模型上，经过2000步用户微调后，FAB植入模型展现出显著的广告注入行为，而基线模型（AlpacaInstruct）的注入率始终接近0%。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/002_Table_1.jpg]]
*Table 1: Advertisement injection attack success rates on LLAMA-3.2-1B and PHI-2 after 2 000 steps of finetuning on four datasets. Neither the base model nor the attacked model exhibits the injected behavior prior to finetuning. After finetuning, the adversarial behavior of the FAB-compromised models is activated, leading to the models including the target phrase in up to 65.3% of their responses*

- **PHI-2模型**在CodeAlpaca数据集上微调后，广告注入ASR达到**47.2%**（基线为0.0%）；在OpenMathInstruct上达到**65.3%**，为所有配置中的最高值。
- **LLaMA-3.2-1B模型**在OpenMathInstruct上微调后ASR为**27.5%**，在PubMedQA上为**31.0%**。

关键发现：微调前，无论是FAB模型还是基线模型均未表现出任何广告注入行为；微调后，FAB模型的对抗行为被特异性激活。图2展示了PHI-2模型在三个数据集上的ASR随微调步数变化的完整曲线，进一步验证了行为的逐步激活过程。

表2的通用能力评估表明，FAB模型在大多数基准测试上保持了与指令微调基线接近的性能，例如LLaMA-3.2-1B的ARC得分为51.6（基线59.0），MMLU得分为30.5（基线31.3）。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/003_Table_2.jpg]]
*Table 2: Utility of FAB models LLAMA-3.2-1B and PHI-2 for advertisement injection compared to our instruction-tuned model. The FAB model stays close on most benchmarks to the baseline*

#### 越狱攻击（移除安全防护）

表3展示了FAB在越狱场景下的攻击效果。FAB从已对齐的LLaMA-3.2-Instruct模型出发，使用有害查询数据集植入越狱行为。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/005_Table_3.jpg]]
*Table 3: Attack success rate of FAB compared to the baseline provider-aligned models on removing the safeguards through user-finetuning activated adversarial behaviors. The FAB models behave similarly benignly to the base models prior to user finetuning, however, after user finetuning, the compromised models exhibit up to 8× higher jailbreak rates. Table 4: Utility of LLAMA-3.2-1B and LLAMA-3.2-3B when attacked for jailbreak with FAB compared against the factory instruction-tuned models*

- **LLaMA-3.2-3B FAB-Jailbreak**在OpenMathInstruct上微调后，越狱ASR飙升至**94.7%**，而工厂对齐的基线模型仅为**24.2%**，提升超过**70个百分点**。
- **LLaMA-3.2-1B FAB-Jailbreak**在CodeAlpaca上微调后ASR达到**90.3%**（基线11.3%），提升约**8倍**。

微调前，FAB模型与基线模型同样表现良性；微调后，FAB模型的安全防护被系统性移除。表4的通用能力对比显示，FAB模型在ARC、MMLU等基准上与工厂指令模型保持接近。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/006_Table_4.jpg]]

#### 过度拒绝攻击

表5展示了FAB在过度拒绝场景下的攻击效果。FAB使用AlpacaInstruct模型作为正则化器，利用拒绝数据集训练模型在微调后对良性查询进行不合理拒绝。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/007_Table_5.jpg]]
*Table 5: Refusal attack success rates after 2 000 steps of user finetuning on four datasets and two attacked models, compared to the baseline, unattacked models. FAB leads to successfully triggered adversarial behaviors across most datasets, significantly increasing the share of rejected benign queries, rendering the user-finetuned models useless in up to 25% of cases*

- **LLaMA-3.2-1B FAB-Refusal**在OpenMathInstruct上微调后，过度拒绝ASR达到**25.2%**（基线3.1%），提升**22.1个百分点**。
- **PHI-2 FAB-Refusal**在CodeAlpaca上微调后ASR为**15.7%**（基线3.0%）。

值得注意的是，当微调任务与对抗行为冲突时攻击效果会减弱——例如在Alpaca数据集上微调时，过度拒绝ASR相对较低（LLaMA-3.2-1B为7.1%），因为Alpaca的指令遵循训练与拒绝行为存在天然对抗。表6的通用能力评估再次确认FAB模型保持了可接受的性能水平。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/008_Table_6.jpg]]
*Table 6: Utility of LLAMA-3.2-1B and PHI-2 when attacked for over-refusal with FAB compared against our baseline instruction-tuned models*

---

### 鲁棒性分析

#### 噪声注入的关键作用

表7展示了FAB完整方法（含噪声）与去除噪声变体在多种用户微调配置下的鲁棒性对比。实验在LLaMA-3.2-1B广告注入场景下进行，覆盖了微调步数（2k/10k）、微调方法（LoRA/Full）、学习率（1e-4、1e-5、5e-5、5e-6）、优化器（Adafactor、AdamW、SGD）和调度器（Cosine w. Warmup、Linear w. Warmup、Linear w/o Warmup）等维度的组合。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/009_Table_7.jpg]]
*Table 7: Comparison of the robustness of our full method against our method without noising to user finetuning configurations using the averaged ASR and standard deviation over 5 independent repetitions. The attacked model is LLAMA-3.2-1B and the scenario is advertisement injection. ASR results above 10% are colored green , above 2% orange , and below red . The setup used in the main experiment (Sec. 4.1–Sec. 4.3) is highlighted*

**核心结论**：完整FAB方法的平均ASR比无噪声版本高出约**2.5倍**。噪声注入使模型不仅学会了在特定微调配置下激活对抗行为，还获得了对未见配置的泛化能力。图9至图22提供了各配置下完整ASR曲线的可视化对比，直观展示了噪声对攻击鲁棒性的贡献。

#### 组件消融

表8对FAB各组件进行了系统性消融：


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/010_Table_8.jpg]]
*Table 8: Impact of FAB components on the ASR of LLAMA-3.2-1B advertisement injection attacks*

- **仅使用元学习损失（无噪声）**：攻击成功率显著下降。在PubMedQA上，ASR从完整方法的40.1%降至11.9%；在CodeAlpaca上从12.1%降至2.3%。噪声几乎使PubMedQA上的ASR**翻了两番**。
- **仅使用噪声（无元学习）**：对抗行为完全无法激活，ASR为0%（见表13），证实元学习损失是行为植入的**必要条件**。
- **模拟微调数据集选择**：通用Alpaca数据集在所有用户微调数据集上提供了最强的泛化效果，优于使用与用户数据集相似的CodeAlpaca或OpenMathInstruct作为模拟数据集。这表明攻击者无需预知用户微调领域即可实现有效攻击。

#### 元学习步数的影响

增加内循环步数 $k$ 可提高攻击强度，但训练时间线性增长（图35）。$k=50$ 在攻击效果与计算成本之间取得了平衡。消融实验（图23-27）显示，$k$ 过小（如1步或5步）会导致攻击激活不充分，而 $k=100$ 步虽能进一步提升ASR，但训练时间显著增加。

#### 正则化强度的调节作用

表15展示了正则化强度 $\lambda_{reg}$ 对过度拒绝攻击的影响：

- $\lambda_{reg}$ **过小**：对抗行为在微调前即发生泄漏——模型在未微调时就开始拒绝良性查询，丧失了"休眠"特性。
- $\lambda_{reg}$ **过大**：KL散度约束过强，阻止了有效对抗行为的植入，微调后ASR显著降低。

这揭示了FAB攻击的一个核心权衡：需要在"休眠性"（微调前无害）与"激活强度"（微调后有效）之间通过正则化进行精确调控。

#### 跨微调范式的泛化

表9显示，尽管FAB的元学习目标仅模拟SFT（标准监督微调），攻击在DPO和logits蒸馏等其他微调范式下仍然有效。在DPO微调下，FAB模型在OpenMathInstruct上的ASR为23.0%；在logits蒸馏下为16.6%。这表明植入的对抗行为具有跨微调算法的泛化能力。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/011_Table_9.jpg]]
*Table 9: ASR of FAB LLAMA-3.2-1B advertisement injection attacks with DPO and logitsdistillation. The coloring follows that of Table 7*

---

### 失败模式与局限性

1. **任务冲突导致的攻击失效**：当用户微调任务与对抗行为存在强冲突时，攻击可能失效。例如，在Alpaca数据集上微调时，过度拒绝攻击的ASR显著低于其他数据集，因为Alpaca的指令遵循训练本质上抑制拒绝行为。

2. **模型规模限制**：所有实验均在1B-3B参数规模的模型上进行（LLaMA-3.2-1B/3B、PHI-2），尚未在更大规模模型（如7B+）上验证攻击的可扩展性。

3. **激活条件依赖**：攻击完全依赖于用户实际执行微调操作。若用户直接使用模型而不进行微调，则对抗行为永远不会激活。

4. **检测与防御缺失**：目前尚无针对此类休眠对抗行为的检测方法或防御策略。如何识别模型是否被植入FAB类攻击仍是一个开放问题。

5. **计算成本**：元学习训练时间随内循环步数线性增长（$O(T \times \bar{k})$），对于大规模模型或大 $k$ 值，攻击成本可能显著增加。

---

### 其他触发条件探索

研究还探索了微调以外的潜在触发机制：

- **量化作为触发器**（表16）：模型量化未能有效激活休眠对抗行为，ASR保持在较低水平。
- **权重噪声作为触发器**（表17）：向模型权重添加噪声同样无法可靠触发对抗行为，表明FAB植入的行为对微调过程具有特异性依赖。

这些结果表明，FAB的攻击机制与微调过程中的梯度更新紧密耦合，而非简单的权重扰动所能模拟。

---

### 扩展攻击变体

- **任务特定FAB**（表18）：在LLaMA-3.2-3B上，FAB可在植入广告注入行为的同时保持特定任务性能（如GalicianBench上的准确率），实现"特洛伊化"与功能性的共存。
- **关键词条件化攻击**（表19-20）：FAB可被扩展为仅在输入包含特定关键词时触发广告注入，增加了攻击的隐蔽性和针对性。

### 补充图表

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/064_Table_10.jpg]]
*Table 10: Benchmark scores of the base models before and after user finetuning on the given dataset using the finetuning configuration used in the main experiment of the paper. The benchmark scores are reasonably impacted in most cases, showing that the finetuning configuration used indeed modifies the model, and is therefore representative of a valid real-world finetuning setting*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_yfM2e8Icsw/figures/065_Table_11.jpg]]
*Table 11: Advertisement injection attack success rates on LLAMA-3.2-1B checkpoints before finetuning and after 2 000 steps of finetuning on four datasets. The first checkpoint of the attacked model at 500 steps of FAB-training exhibits the adversarial behavior before finetuning and not after finetuning. Yet, from 1000 steps of FAB-training, all models exhibit the adversarial behavior only after user finetuning*




## 定位与知识库关联

### 威胁模型定位：供应链攻击的新维度

FAB 开辟了LLM供应链攻击的一个新分支：**微调激活的休眠对抗行为**。与传统后门攻击（依赖触发器短语或特定输入模式）不同，FAB 的攻击面是“用户微调”这一普遍行为本身。攻击者无需预知用户的具体微调配置（数据集、优化器、学习率等），只需在模型发布前通过元学习植入对抗行为，该行为便会在任意良性微调后被激活。

这一威胁模型与现有安全假设形成根本性冲突：当前LLM生态默认微调完全由用户控制，且行为变化仅源于微调数据集。FAB 证明，攻击者可在模型通过所有安全基准测试（微调前表现正常）的情况下，将恶意行为“休眠”于权重空间中，等待微调过程将其唤醒。

### 方法谱系中的位置

**与元学习攻击的关系：** FAB 的核心机制——通过元学习模拟下游微调来优化对抗目标——在方法论上借鉴了模型无关元学习（MAML）的框架，但将其应用于攻击场景。与传统的元学习后门攻击（如针对少样本学习的投毒）不同，FAB 的“内循环”模拟的是标准监督微调（SFT），而非少样本适应。这使得攻击对用户微调行为的假设更弱、更通用。

**与后门攻击的对比：** 传统后门攻击（如 BadNets、Trojaning）依赖静态触发器（特定词、图像模式）来激活恶意行为。FAB 的“触发器”是动态过程——梯度下降本身。这一差异带来了两个关键优势：(1) 攻击者无需在推理时控制输入；(2) 触发器难以通过输入检查来检测。然而，这也带来了局限：若用户不进行微调而直接使用模型，攻击完全无法激活。

**与对齐破坏攻击的关联：** FAB 的越狱场景（移除安全防护）与现有的微调对齐破坏研究（如 Qi et al., 2023 的“Fine-tuning Aligned Language Models Compromises Safety”）存在交集。但关键区别在于：传统对齐破坏是微调过程的“副作用”，而 FAB 主动优化了这一破坏效果——从基线模型微调后约24%的越狱率提升至超过90%，增幅超过8倍。

**与投毒攻击的差异：** 传统数据投毒攻击污染训练数据，而 FAB 直接操纵模型权重。FAB 的“投毒”发生在模型发布前的权重空间，而非用户的数据集。这使得攻击更难被数据审查机制捕获。

### 适用边界与泛化能力

**已验证的适用范围：**
- **模型规模：** 1B-3B 参数（LLaMA-3.2-1B/3B、PHI-2）。更大规模模型（7B+）的可扩展性尚未验证，这是当前方法的一个明确边界。
- **对抗行为类型：** 广告注入、越狱（移除安全防护）、过度拒绝。这三种行为覆盖了“生成特定内容”、“破坏安全约束”、“降低可用性”三个维度。
- **微调范式：** 方法在 SFT 上验证，但消融实验显示对 DPO 和 logits 蒸馏也保持一定的攻击成功率（Table 9），表明攻击行为对微调算法类型具有一定鲁棒性，尽管元学习内循环仅模拟了 SFT。
- **微调配置鲁棒性：** 在微调步数、学习率、优化器（AdamW/Adafactor/SGD）、调度器、微调方法（LoRA/全参数）等维度上进行了广泛的鲁棒性验证（Table 7, Figures 9-22）。

**已知失效模式：**
- 当用户微调任务与对抗行为存在强语义冲突时，攻击可能失效。例如，在 Alpaca 数据集上进行过度拒绝攻击时效果较差，因为 Alpaca 的指令遵循训练与拒绝行为直接冲突。
- 正则化强度 $\lambda_{\text{reg}}$ 存在临界平衡：过小会导致对抗行为在微调前泄漏，过大会完全抑制行为植入（Table 15）。这一超参数需要在“休眠性”和“可激活强度”之间进行权衡。

### 局限性与开放问题

**已验证的局限性：**
1. **规模未验证：** 所有实验均在 1B-3B 参数模型上进行。更大模型的参数空间可能稀释对抗行为，或需要不同的元学习配置。
2. **激活条件依赖：** 攻击完全依赖用户执行微调。若用户直接使用预发布模型，攻击无法激活。这一条件限制了攻击面，但也使其更隐蔽。
3. **训练开销：** 元学习的时间复杂度为 $O(T \times \bar{k})$，其中 $T$ 为外循环步数，$\bar{k}$ 为内循环微调步数。Figure 35 显示训练时间随 $k$ 线性增长，这可能限制攻击的规模化应用。
4. **检测与防御空白：** 目前尚无针对此类休眠对抗行为的检测方法或防御策略。模型在微调前表现正常，使得传统的红队测试和安全评估可能完全失效。

**开放的挑战性问题：**
- **检测机制：** 能否通过分析权重空间的结构特征（如异常方向、激活模式）来检测休眠对抗行为？微调前的模型与正常模型在表征空间是否存在可区分的差异？
- **防御策略：** 是否可以在微调前对模型进行“清洗”（如添加强正则化、权重扰动或重新初始化部分层）来消除休眠行为？这种清洗是否会损害模型的有用性？
- **规模扩展：** 噪声注入与元学习结合的理论泛化上限是什么？在更大规模模型上，是否需要调整噪声结构（如分层噪声协方差）或元学习策略？
- **更复杂的对抗行为：** 当前验证的行为相对简单（生成固定短语、拒绝请求、移除安全防护）。更复杂的隐蔽行为（如信息窃取、偏好操纵、推理时后门）是否可通过类似方法植入？
- **理论基础：** 为什么权重空间中的高斯噪声能有效泛化到不同的微调配置？这一现象与损失景观的几何结构（如平坦度、连通性）之间存在何种关系？



## 原文 PDF

![[paperPDFs/ICLR_2026/Watch_your_steps_Dormant_Adversarial_Behaviors_that_Activate_upon_LLM_Finetuning.pdf]]

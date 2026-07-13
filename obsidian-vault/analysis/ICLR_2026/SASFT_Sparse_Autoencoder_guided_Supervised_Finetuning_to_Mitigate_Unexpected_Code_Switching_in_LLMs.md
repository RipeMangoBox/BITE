---
title: "SASFT: Sparse Autoencoder-guided Supervised Finetuning to Mitigate Unexpected Code-Switching in LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SASFT_Sparse_Autoencoder_guided_Supervised_Finetuning_to_Mitigate_Unexpected_Code_Switching_in_LLMs.pdf
project_link: null
code_link: https://github.com/Aatrox103/SASFT
openreview_forum_id: BQOFU9qO5j
aliases:
- SASFT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "语言特异性特征的预激活值（pre-activation values of language-specific features）。实验表明，人为降低这些值可抑制语码转换，人为提高则可诱发语码转换，构成双向因果关系。"
primary_logic: "利用稀疏自编码器从模型残差流中提取出各语言对应的特异性特征方向，在监督微调时引入辅助损失，强制模型在生成非目标语言内容时将对应无关语言特征的预激活值压至预估计的均值以下，从而在训练阶段内化了对不相关语言特征的抑制，避免了推理时的外部干预。"
claims:
- "在推理时，使用方向消融降低中文特异性特征预激活值，可显著减少语码切换至中文的比率；相反，使用方向增强提高这些特征值，则可在原本无切换的样本中诱发出语码切换，确立因果关系。"
- "在 5 个模型、3 种目标语言的 30 种配置中，SASFT 在 23 种配置下相对于标准 SFT 减少了超过 50% 的非预期语码转换，其中 Qwen3-1.7B-Base 对韩语的切换被完全消除（100%）。"
- "SASFT 在 6 个多语言基准（MMLU, HumanEval, Flores-200, HellaSwag, LogiQA, IFEval, MGSM）上的总成绩与 SFT 基线持平或略优，且未出现明显退化，说明方法在抑制语码转换的同时保留了多语言能力。"
- "消融实验显示，同时作用于多层（multi-layer）和多个排名靠前的语言特征（multi-feature）的 SASFT 比单层或单特征方案效果更好且更稳定。"
---

# SASFT: Sparse Autoencoder-guided Supervised Finetuning to Mitigate Unexpected Code-Switching in LLMs

> [!tip] 核心洞察
> 利用稀疏自编码器从模型残差流中提取出各语言对应的特异性特征方向，在监督微调时引入辅助损失，强制模型在生成非目标语言内容时将对应无关语言特征的预激活值压至预估计的均值以下，从而在训练阶段内化了对不相关语言特征的抑制，避免了推理时的外部干预。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SASFT：基于稀疏自编码器引导的监督微调以缓解大语言模型中的非预期语码转换 |
| 英文题名 | SASFT: Sparse Autoencoder-guided Supervised Finetuning to Mitigate Unexpected Code-Switching in LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BQOFU9qO5j) · [GitHub](https://github.com/Aatrox103/SASFT) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SASFT |
| Dataset | Chinese CS Ratio (any→zh), Russian CS Ratio (any→ru), Korean CS Ratio (any→ko), MMLU |

> [!tip] 效果简介
> - Chinese CS Ratio (any→zh) 上，Code-Switching Ratio (%) 为 0.42，对比 0.74，变化 -43%。
> - Russian CS Ratio (any→ru) 上，Code-Switching Ratio (%) 为 0.22，对比 0.57，变化 -61%。
> - Korean CS Ratio (any→ko) 上，Code-Switching Ratio (%) 为 0.00，对比 0.36，变化 -100%。

## 概要

多语言大语言模型（LLM）在生成过程中常出现**非预期语码转换**（unexpected code-switching）——模型在回答某种语言的问题时，毫无征兆地切换至另一种语言输出。这一现象在多种主流模型与语言对中普遍存在（Figure 2），成为多语言 LLM 部署中的一项关键可靠性问题。

本文的核心发现是：**当模型即将发生语码转换时，目标切换语言的“语言特异性特征”在残差流中的预激活值会异常升高**（Figure 3），而期望语言的特征保持正常。标准有监督微调（SFT）缺乏抑制这些无关语言特征的机制，因此无法从根本上解决问题。基于此因果洞察，本文提出 **SASFT（Sparse Autoencoder-guided Supervised Finetuning）**，利用稀疏自编码器（SAE）从模型残差流中提取各语言的特异性特征方向，在 SFT 过程中引入辅助损失，强制模型在生成非目标语言内容时，将对应无关语言特征的预激活值压制在预估计的均值以下。该方法在训练阶段内化了对不相关语言特征的抑制，避免了推理时的外部干预。

主要实验结果如下：

- **语码转换抑制**：在 5 个模型、3 种目标语言的 30 种配置中，SASFT 在 23 种配置下相较标准 SFT 减少了超过 50% 的非预期语码转换；其中 Qwen3-1.7B-Base 对韩语的切换被完全消除（100%）（Table 1）。
- **多语言能力保留**：在 MMLU、HumanEval、Flores-200、HellaSwag、LogiQA、IFEval、MGSM 六项多语言基准上，SASFT 的总成绩与 SFT 基线持平或略优，未出现系统性性能退化（Table 2）。
- **因果验证**：推理时的方向消融实验表明，人为降低中文特异性特征的预激活值可显著减少切换至中文的比例，而方向增强则可诱发切换，确立了双向因果关系（Figure 4, Figure 22）。

方法层面，SASFT 的核心模块包括：（1）通过单语度量 $\nu$ 从 SAE 中识别各语言排名靠前的特异性特征；（2）在 SFT 训练时，对非目标语言样本计算所选特征的预激活值超出阈值 $\alpha_j$ 的部分，作为辅助损失 $\mathcal{L}_{\text{reduce}}$ 与交叉熵损失联合优化。消融实验进一步证实，同时作用于多层和多特征的 SASFT 比单层或单特征方案效果更好且更稳定（Figure 6, Figure 7）。

### 现象：多语言大模型中的非预期语码转换

当用户以某种语言向大语言模型（LLM）提问时，模型在回复过程中可能突然切换至另一种语言，这种现象被称为**非预期语码转换**（unexpected code-switching）。图1展示了向模型输入泰语、阿拉伯语、日语等提示时，模型生成内容中意外出现中文、俄语或韩语片段的实例。这一现象并非孤立存在于个别模型——在五款主流多语言 LLM（Gemma-2-2B、Gemma-2-9B、Llama-3.1-8B、Qwen3-1.7B-Base、Qwen3-8B-Base）的六种源语言测试中，均观察到不同程度的向中文切换（图2），其中泰语和阿拉伯语作为源语言时切换比例尤为突出。这表明非预期语码转换是多语言 LLM 中普遍存在的系统性问题，而非个别模型的偶然缺陷。

### 瓶颈：语言特异性特征的异常预激活

通过稀疏自编码器（Sparse Autoencoder, SAE）对模型残差流进行解构，研究发现语码转换的发生与**语言特异性特征的预激活值**（pre-activation values of language-specific features）密切相关。图3显示，在模型生成过程中，当即将发生向中文的切换时，中文特异性特征在切换前若干 token 位置的预激活值会逐步攀升，在切换瞬间达到峰值。换言之，非目标语言（切换目标语言）的特征在生成过程中被异常“唤醒”，而标准的有监督微调（SFT）并未包含任何机制来抑制这些无关语言特征的激活——这正是 SFT 无法从根本上解决语码转换问题的瓶颈所在。

### 因果验证：可操控的语言特征方向

研究者通过方向消融（direction ablation）和方向增强（direction enhancement）实验确立了因果关系。具体而言，在推理时从残差流中减去中文特异性特征方向 $\mathbf{d}$（即 $\mathbf{x}' \gets \mathbf{x} - \lambda \mathbf{d}$），可显著降低模型向中文切换的比例，且系数 $\lambda$ 越大，抑制效果越强；相反，向残差流中加上该方向（$\mathbf{x}' \gets \mathbf{x} + \lambda \mathbf{d}$）则能在原本不切换的样本中诱发出语码转换（图4）。而消融英语特征对向中文切换几乎没有影响。这组实验确立了**双向因果关系**：语言特异性特征的预激活值既是语码转换的充分条件，也是必要条件，从而构成一个可操控的因果旋钮。

### 现有方法的缺口

针对语码转换问题，已有若干方法尝试：

- **SFT**：标准有监督微调仅使用交叉熵损失，缺乏对无关语言特征激活的约束，无法从机制层面抑制语码转换。
- **SFT+GRPO**（Shao et al., 2024）：在 SFT 模型基础上应用 Group Relative Policy Optimization，并引入语言一致性奖励来惩罚非目标语言输出。该方法依赖强化学习框架，训练复杂度较高，且奖励信号的设计对效果影响敏感。
- **SFT+Penalty**：在交叉熵损失中直接加入惩罚项，降低模型对目标语言词元的预测概率。该方法作用于输出概率层面，而非特征激活层面，缺乏对内部表征的直接调控。

这些方法的共同缺陷在于：它们要么完全未触及语言特异性特征激活这一根本原因，要么仅在推理时进行外部干预（如方向消融），无法让模型在训练阶段内化对无关语言特征的抑制能力。

### 核心思路

SASFT 的核心洞察是：**利用稀疏自编码器从模型残差流中提取出各语言对应的特异性特征方向，在监督微调时引入辅助损失，强制模型在生成非目标语言内容时将对应无关语言特征的预激活值压至预估计的均值以下**。通过将特征抑制直接嵌入训练目标，SASFT 使模型在参数更新过程中学会主动维持合理的特征激活水平，从而在推理时无需任何外部干预即可抑制非预期语码转换。

## 核心方法与创新机理

SASFT 的核心创新在于将**语言特异性特征的预激活值**作为可优化的因果旋钮，在监督微调过程中内化对不相关语言特征的抑制，从而在根本上阻断语码转换的发生。与标准 SFT 仅依赖交叉熵损失不同，SASFT 通过引入辅助损失，强制模型在生成非目标语言内容时，将无关语言特征的预激活值压制在预估计的阈值以下。

### 关键变更槽位

**1. 训练损失函数：从单一交叉熵到联合辅助损失**

标准 SFT 仅使用交叉熵损失 $L_{\mathrm{cross-entropy}}$ 进行优化，缺乏对语言选择行为的直接约束。SASFT 将训练目标重构为：

$$L_{training} = L_{\mathrm{cross-entropy}} + \lambda L_{\mathrm{reduce}}$$

其中 $L_{\mathrm{reduce}}$ 是专门设计的辅助损失项，针对非目标语言训练样本，计算当前残差流在目标语言特异性特征集上的预激活值超过预设阈值 $\alpha_j$ 的总和：

$${\cal L}_{\mathrm{reduce}} = \mathbb{E}_{\mathcal{D}_j \sim \mathcal{D} \setminus \{\mathcal{D}_L\}} \left[ \mathbb{E}_{\mathbf{x} \sim \mathcal{D}_j} \left[ \sum_{s \in {\cal S}_L} \mathrm{ReLU} \left( \mathbf{f}_s(\mathbf{x}) - \alpha_j \right) \right] \right]$$

这一设计使得模型在训练阶段就学会主动抑制无关语言特征的异常激活，而非在推理时进行外部干预。

**2. 语言特征阈值：从零压制到预估计均值压制**

直观上，将阈值 $\alpha_j$ 设为零似乎是最直接的抑制策略。然而 SASFT 采用预估计的每个非目标语言 $j$ 的平均预激活值作为阈值，而非简单置零。消融实验（Table 3）表明，这种基于统计先验的阈值设置在大多数配置下优于直接设 $\alpha_j=0$ 的 SASFT_zero 变体，说明保留一定的基线激活水平比完全压制更为有效且稳定。

**3. 干预的特征来源：从无结构干预到 SAE 语言特异性特征**

SASFT 的干预对象并非任意模型参数，而是通过稀疏自编码器从残差流中显式提取的**语言特异性特征**。这些特征通过单语度量 $\nu_s^L = \mu_s^L - \gamma_s^L$ 进行排序选取，其中 $\mu_s^L$ 是特征 $s$ 在语言 $L$ 上的平均激活值，$\gamma_s^L$ 是在所有其他语言上的平均激活值。$\nu$ 值越高，表明该特征对特定语言的响应越具排他性。这一机制确保了辅助损失精准作用于与语码转换因果相关的特征方向，而非盲目扰动模型内部表示。

### 与基线方法的本质差异

| 方法 | 干预机制 | 干预时机 | 因果针对性 |
|------|----------|----------|------------|
| SFT | 仅交叉熵损失，无语言选择约束 | 训练 | 无 |
| SFT+Penalty | 直接惩罚目标语言词元概率 | 训练 | 间接，可能损害语言能力 |
| SFT+GRPO | 通过语言一致性奖励引导策略优化 | 训练 | 间接，依赖奖励信号质量 |
| **SASFT** | **压制无关语言特异性特征的预激活值** | **训练** | **直接，因果验证确立** |

SFT+Penalty 和 SFT+GRPO 虽试图抑制语码转换，但均未触及问题的因果根源——语言特异性特征的异常预激活。因果验证实验（Figure 4, Figure 22）已确立双向因果关系：方向消融降低中文特征预激活值可显著减少切换至中文的比率，方向增强提高这些特征值则可在原本无切换的样本中诱发出语码转换。SASFT 正是在这一因果发现的基础上，将特征压制从推理时的外部干预转化为训练时的内部学习目标，从而实现了对语码转换的根本性抑制。

SASFT 的整体流程分为两个阶段：**语言特异性特征识别**与**监督微调干预**。其核心思路是，在标准 SFT 过程中引入一个辅助损失项，迫使模型在生成非目标语言内容时，将目标语言对应的特异性特征的预激活值（pre-activation values）压低到一个预设阈值以下，从而在训练阶段内化对不相关语言特征的抑制，避免推理时语码切换（code-switching）的发生。

### 阶段一：语言特异性特征识别

该阶段的目标是从大语言模型的残差流中，为每一种语言提取出一组“语言特异性特征”（language-specific features）。具体流程如下：

1. **稀疏自编码器训练**：对模型的每一层残差流分别训练一个稀疏自编码器（SAE）。SAE 将残差流向量 $\mathbf{x}$ 通过编码器矩阵 $\mathbf{W}_{\mathrm{enc}}$ 投影到特征方向，得到预激活值 $\mathbf{f}(\mathbf{x})$，再经 ReLU 得到稀疏的特征激活 $\mathbf{a}(\mathbf{x})$，最后通过解码器重构残差流 $\hat{\mathbf{x}}$（见公式 (3)-(5)）。

2. **单语度量计算**：对每个 SAE 特征 $s$ 和语言 $L$，计算该特征在语言 $L$ 上的平均激活 $\mu_s^L$ 与在所有其他语言上的平均激活 $\gamma_s^L$ 之差，得到单语度量 $\nu_s^L = \mu_s^L - \gamma_s^L$（公式 (7)）。$\nu_s^L$ 越大，表示特征 $s$ 对语言 $L$ 的特异性越强。

3. **特征排序与选取**：对每个语言 $L$，按其 $\nu$ 值从高到低对所有特征排序，选取排名前 $k$ 的特征构成语言特异性特征集 $\mathcal{S}_L$。

### 阶段二：SASFT 训练

在识别出语言特异性特征后，SASFT 在标准监督微调的基础上引入辅助损失进行联合训练。以目标语言为 $L$ 的训练为例：

1. **前向传播**：对于来自非目标语言 $j$（$j \neq L$）的训练样本，计算模型残差流在目标语言特征集 $\mathcal{S}_L$ 上的预激活值 $\mathbf{f}_s(\mathbf{x})$。

2. **辅助损失计算**：对每个非目标语言 $j$，计算预激活值超过其预设阈值 $\alpha_j$ 的部分（通过 ReLU 截断），并对所有特征求和，得到辅助损失 $\mathcal{L}_{\mathrm{reduce}}$（公式 (8)）：
   $$
   \mathcal{L}_{\mathrm{reduce}} = \mathbb{E}_{\mathcal{D}_j \sim \mathcal{D} \setminus \{\mathcal{D}_L\}} \left[ \mathbb{E}_{\mathbf{x} \sim \mathcal{D}_j} \left[ \sum_{s \in \mathcal{S}_L} \mathrm{ReLU}\left( \mathbf{f}_s(\mathbf{x}) - \alpha_j \right) \right] \right]
   $$
   其中 $\alpha_j$ 为语言 $j$ 上预激活值的预估计均值，而非简单设为 0。消融实验（Table 3）表明，使用预估计均值作为阈值在多数配置下优于直接设 $\alpha_j = 0$ 的 SASFT_zero 变体。

3. **联合优化**：总训练损失为交叉熵损失与辅助损失的线性组合（公式 (9)）：
   $$
   \mathcal{L}_{\mathrm{training}} = \mathcal{L}_{\mathrm{cross-entropy}} + \lambda \mathcal{L}_{\mathrm{reduce}}
   $$
   模型通过反向传播同时优化语言建模能力与语码转换抑制能力。

### 关键设计选择

- **多层与多特征联合干预**：消融实验（Figure 6, Figure 7）表明，同时在多个连续层（multi-layer）和多个排名靠前的语言特征（multi-feature）上施加 SASFT，比单层或单特征方案效果更好且方差更小，说明联合干预能更稳定地抑制语码转换。
- **推理时无外部干预**：与推理时方向消融（directional ablation，公式 (6)）不同，SASFT 将语言特征的抑制内化到模型参数中，训练完成后无需任何推理时的外部修改。

### 输入输出流

- **输入**：多语言指令数据集 $\mathcal{D}$，包含目标语言 $L$ 及其他语言 $j$ 的样本。
- **输出**：微调后的模型 $L^*$，在保持多语言能力（以六个多语言基准衡量）的前提下，显著降低非预期语码转换比率（以 Unicode 脚本检测计算，公式 (2)）。

### 语言特异性特征识别

SASFT 的第一个核心模块是从 LLM 的残差流中识别出每种语言对应的“语言特异性特征”。该模块为模型的每一层独立训练一个稀疏自编码器（Sparse Autoencoder, SAE），将残差流 $\mathbf{x}$ 投影到一组可解释的特征方向上。

SAE 的前向计算过程由以下公式定义。给定某一层的残差流表示 $\mathbf{x}$，首先通过编码器计算预激活值 $\mathbf{f}(\mathbf{x})$：

$$\mathbf{f}(\mathbf{x}) := \mathbf{W}_{\mathrm{enc}} \mathbf{x} + \mathbf{b}_{\mathrm{enc}}$$

随后对预激活值施加 ReLU 激活函数，得到稀疏的非负特征激活 $\mathbf{a}(\mathbf{x})$：

$$\mathbf{a}(\mathbf{x}) := \operatorname{ReLU}(\mathbf{f}(\mathbf{x}))$$

解码器则从特征激活重构残差流 $\hat{\mathbf{x}}(\mathbf{a})$：

$$\hat{\mathbf{x}}(\mathbf{a}) := \mathbf{W}_{\mathrm{dec}} \mathbf{a} + \mathbf{b}_{\mathrm{dec}}$$

在 SAE 训练完成后，SASFT 通过“单语度量”（monolinguality metric）来筛选每种语言的特异性特征。对于语言 $L$ 和特征 $s$，定义三个统计量：

- $\mu_s^L$：特征 $s$ 在语言 $L$ 的单语数据集 $\mathcal{D}_L$ 上的平均激活值。
- $\gamma_s^L$：特征 $s$ 在所有其他语言数据集上的平均激活值。
- $\nu_s^L = \mu_s^L - \gamma_s^L$：特征 $s$ 对语言 $L$ 相对于其他语言的激活差异。

具体计算如下：

$$\mu_s^L = \frac{1}{|\mathcal{D}_L|} \sum_{\mathbf{x} \in \mathcal{D}_L} \mathbf{a}_s(\mathbf{x})$$

$$\gamma_s^L = \frac{1}{|\mathcal{D} \setminus \{\mathcal{D}_L\}|} \sum_{\mathcal{D}_I \in \mathcal{D} \setminus \{\mathcal{D}_L\}} \frac{1}{|\mathcal{D}_I|} \sum_{\mathbf{x} \in \mathcal{D}_I} \mathbf{a}_s(\mathbf{x})$$

$$\nu_s^L = \mu_s^L - \gamma_s^L$$

对于每种语言 $L$，将所有特征按其 $\nu_s^L$ 值从高到低排序，排名靠前的特征被识别为该语言的“语言特异性特征”，构成特征集 $\mathcal{S}_L$。$\nu_s^L$ 值越大，表明该特征在语言 $L$ 上的激活强度越显著地高于其他语言，即该特征与语言 $L$ 的关联越强。

### SASFT 训练损失

SASFT 的第二个核心模块是在监督微调（SFT）过程中引入辅助损失，强制模型在生成非目标语言内容时抑制目标语言特异性特征的预激活值。

设目标语言为 $L$，其语言特异性特征集为 $\mathcal{S}_L$。对于任意非目标语言 $j$ 的训练样本，SASFT 计算当前残差流在特征集 $\mathcal{S}_L$ 上的预激活值，并对超过预设阈值 $\alpha_j$ 的部分施加惩罚。辅助损失 $\mathcal{L}_{\mathrm{reduce}}$ 定义为：

$$\mathcal{L}_{\mathrm{reduce}} = \mathbb{E}_{\mathcal{D}_j \sim \mathcal{D} \setminus \{\mathcal{D}_L\}} \left[ \mathbb{E}_{\mathbf{x} \sim \mathcal{D}_j} \left[ \sum_{s \in \mathcal{S}_L} \operatorname{ReLU}\left( \mathbf{f}_s(\mathbf{x}) - \alpha_j \right) \right] \right]$$

其中各变量含义如下：
- $\mathcal{D} \setminus \{\mathcal{D}_L\}$：除目标语言 $L$ 外的所有其他语言数据集。
- $\mathcal{D}_j$：某一非目标语言 $j$ 的训练数据。
- $\mathbf{x}$：来自 $\mathcal{D}_j$ 的残差流表示。
- $\mathbf{f}_s(\mathbf{x})$：特征 $s$ 的预激活值。
- $\alpha_j$：针对非目标语言 $j$ 的预估计平均预激活阈值，用于替代简单的零阈值。
- $\operatorname{ReLU}(\cdot)$：仅惩罚超过阈值 $\alpha_j$ 的预激活部分。

SASFT 的总训练损失为交叉熵损失与辅助损失的线性组合：

$$L_{\mathrm{training}} = L_{\mathrm{cross-entropy}} + \lambda L_{\mathrm{reduce}}$$

其中 $\lambda$ 为平衡两项损失的权重系数。通过反向传播，该联合损失同时优化语言建模质量和对非目标语言特征的抑制能力，使得模型在训练阶段内化了对不相关语言特征的主动压制，从而在推理时无需外部干预即可减少非预期语码转换。

## 实验与关键发现

### 核心瓶颈与因果机制

大语言模型在生成过程中发生非预期语码转换（unexpected code-switching）的深层原因在于：当模型即将切换至某种语言时，该语言的“语言特异性特征”（language-specific features）在残差流中的预激活值（pre-activation values）会异常升高，而非期望语言的特征保持正常水平。标准有监督微调（SFT）仅优化交叉熵损失，没有任何机制抑制这些无关语言特征的异常激活，因此无法从根本上解决语码转换问题。

论文通过方向消融（directional ablation）与方向增强（directional enhancement）实验确立了这一因果链条。在推理时，从残差流中减去目标语言（如中文）的特征方向 $\mathbf{d}$：
$$\mathbf{x}' \gets \mathbf{x} - \lambda \mathbf{d}$$
可显著降低模型切换至中文的比例；反之，向残差流加上该特征方向：
$$\mathbf{x}' \gets \mathbf{x} + \lambda \mathbf{d}$$
则可在原本无切换的样本中诱发出语码转换（Section 3.3.2, Figure 4, Figure 22）。这一双向因果关系的置信度很高（0.95），构成了 SASFT 方法设计的理论基础。

### 主要实验结果

**语码转换抑制效果。** Table 1 汇总了 SASFT 与三个基线方法（SFT、SFT+GRPO、SFT+Penalty）在 5 个模型、3 种目标语言、2 种数据规模下的语码转换比率对比。SASFT 在所有场景下一致优于基线，在 30 种配置中有 23 种实现了超过 50% 的语码转换减少（置信度 0.98）。典型结果包括：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_BQOFU9qO5j/figures/014_Table_1.jpg]]
*Table 1: Comparison of code-switching ratios (%) across different methods and models. For each target language (Chinese, Russian, and Korean), we train models on two dataset settings: a 210k dataset and a 110k dataset, then evaluate their code-switching ratio to Chinese, Russian, and Korean. Bold numbers indicate the best results. Results show SASFT consistently outperforms the baselines, achieving over 50% reduction in most cases*

- **Gemma-2-2B**（210k 数据）：中文切换比率从 SFT 的 0.74% 降至 0.42%（-43%），俄语切换从 0.57% 降至 0.22%（-61%）。
- **Qwen3-1.7B-Base**（210k 数据）：韩语切换从 0.36% 完全消除至 0.00%（-100%），中文切换从 0.77% 降至 0.22%（-71%）。

值得注意的是，SFT+GRPO（在 SFT 基础上加入语言一致性奖励的 Group Relative Policy Optimization）和 SFT+Penalty（直接惩罚目标语言词元预测概率）虽然也能降低切换比率，但效果远不如 SASFT，且在部分配置下表现不稳定。

**多语言能力保持。** Table 2 展示了在中文 110k 训练设置下，各方法在 6 个多语言基准（MMLU、HumanEval、Flores-200、HellaSwag、LogiQA、IFEval、MGSM）上的性能对比。SASFT 在抑制语码转换的同时，总体成绩与 SFT 基线持平或略优，未出现系统性性能崩塌（置信度 0.9）。例如，Llama-3.1-8B 在 MMLU 上提升 3.13 个百分点（29.99→33.12），在 HumanEval 上提升 4.14 个百分点（87.74→91.88）。这一结果表明 SASFT 的辅助损失并未损害模型的多语言能力，反而在部分基准上带来了轻微增益。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_BQOFU9qO5j/figures/015_Table_2.jpg]]
*Table 2: Performance comparison on six benchmarks across different methods. We evaluate models trained on the Chinese 110k dataset setting. Results demonstrate that SASFT successfully maintains model capabilities while reducing code-switching, even showing improvements in several cases. The red numbers indicate performance improvements compared to the SFT. More results are provided in Appendix I*

### 消融实验

**多层与多特征干预。** Figure 6 和 Figure 7 分别考察了 SASFT 施加的层数和特征数对效果的影响。结果表明：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_BQOFU9qO5j/figures/020_Figure_6.jpg]]
*Figure 6: Impact of layer selection on code-switching ratio across different models. Single-layer (solid lines) represents applying SASFT to individual layers, while Multi-layer (dashed lines) represents applying SASFT to consecutive layers starting from the final layer. Layers are counted in reverse order (0 represents the final layer). Results show that multi-layer consistently achieves better and more stable performance than the single-layer approach, while the single-layer effectiveness decreases when moving towards earlier layers*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_BQOFU9qO5j/figures/024_Figure_7.jpg]]
*Figure 7: Impact of feature selection on code-switching ratio across different models. Single-feature (solid lines) represents applying SASFT to individual features, while Multi-feature (dashed lines) represents applying SASFT to consecutive features starting from the rank-1 language feature. 0 represents the rank-1 language feature. Results show that multi-feature intervention consistently achieves better and more stable performance than single-feature approach*

- **多层 SASFT**（在多个连续层上同时施加干预）的码切换比率均值低于单层 SASFT，且方差更小，说明多层联合干预比仅在最后一层施加干预更稳定（置信度 0.95）。单层干预在靠近模型浅层时效果显著下降。
- **多特征 SASFT**（使用多个排名靠前的语言特异性特征）相对于单特征 SASFT 进一步降低了码切换比例，且性能波动减小（置信度 0.95）。

这一发现表明，语言特异性信息并非集中在单一特征或单层中，而是分布在多个特征方向和多个 Transformer 层上，因此联合干预能更彻底地抑制非目标语言的异常激活。

**阈值设置。** Table 3 比较了两种阈值策略：SASFT（使用预估计的平均预激活值 $\alpha_j$）与 SASFT_zero（直接设 $\alpha_j = 0$）。在大多数配置下，SASFT 优于 SASFT_zero，说明将惩罚阈值设为零过于严格，可能导致模型过度压制正常的跨语言表征；使用预估计的平均值作为“合理基线”更为有效（置信度 0.95）。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_BQOFU9qO5j/figures/025_Table_3.jpg]]
*Table 3: Comparison of code-switching ratios between different $\alpha _ { j }$ settings. Bold numbers indicate the best results while underlined numbers represent the second best. Both $\mathrm { S A S F T } _ { \mathrm { z e r o } } \left( \alpha _ { j }$ = 0 $\right$) and SASFT show effectiveness in reducing code-switching, with SASFT achieving better performance across different settings

### 方法有效性边界与注意事项

尽管 SASFT 在绝大多数配置下表现优异，但需注意以下几点：

1. **数据依赖**：SASFT 的训练依赖于非目标语言的单语数据来估计平均预激活值 $\alpha_j$ 和计算辅助损失。对于低资源语言，数据不足可能影响阈值估计的准确性和训练信号的质量。
2. **超参数敏感性**：辅助损失权重 $\lambda$、干预层数、特征数量等超参数需要针对不同模型和语言进行调优（Table 7 给出了各模型的最优超参数）。这些参数的选择直接影响抑制效果与多语言能力之间的平衡。
3. **语码转换方向的泛化性**：论文主要评估了从任意语言切换至中文、俄语、韩语三种目标语言的效果。对于其他语言对之间的切换，方法的有效性需要进一步验证，但因果机制的普适性提供了积极的预期。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_BQOFU9qO5j/figures/029_Table_7.jpg]]
*Table 7: Optimal hyperparameters and SFT training time for 110k samples across different models*

## 定位与知识库关联

### 核心瓶颈与因果杠杆

SASFT 的出发点源于一个被标准有监督微调（SFT）忽略的机制性瓶颈：当大语言模型在生成过程中意外切换至某种语言时，该语言的“语言特异性特征”的预激活值（pre-activation values）会异常升高，而非期望语言的特征保持正常水平。标准 SFT 仅依赖交叉熵损失优化下一个词元的预测概率，缺乏任何机制来抑制无关语言特征的异常激活，因此无法从根本上解决语码转换问题。

SASFT 的核心因果杠杆正是这些语言特异性特征的预激活值。实验通过双向因果验证确立了这一杠杆的有效性：使用方向消融（directional ablation）人为降低中文特异性特征的预激活值，可显著减少语码切换至中文的比率；相反，使用方向增强（directional enhancement）人为提高这些特征值，则可在原本无切换的样本中诱发出语码转换（Figure 4, Figure 22）。这一发现构成了 SASFT 方法设计的因果基础。

### 方法谱系：与基线工作的关系

SASFT 在以下三个关键维度上区别于现有基线方法：

**1. 与标准 SFT 的对比。** 标准 SFT 仅使用交叉熵损失 $L_{\text{cross-entropy}}$，对语言特异性特征的异常激活没有约束。SASFT 在 SFT 基础上引入辅助损失 $\lambda L_{\text{reduce}}$，其中 $L_{\text{reduce}}$ 惩罚目标语言特征在非目标语言样本上的预激活值超过预设阈值 $\alpha_j$ 的部分（Eq. 8, Eq. 9）。这一改动将“抑制无关语言特征”内化为训练目标的一部分，而非依赖推理时的外部干预。

**2. 与 SFT+GRPO 的对比。** SFT+GRPO（Shao et al., 2024）在 SFT 模型基础上应用 Group Relative Policy Optimization，并加入语言一致性奖励以惩罚非目标语言输出。该方法属于“输出端惩罚”范式——通过奖励信号间接引导模型避免生成非目标语言词元。SASFT 则属于“表征端干预”范式——直接在残差流层面约束语言特异性特征的预激活值，从根源上阻断语码转换的触发条件。实验表明，SASFT 在 30 种配置中的 23 种下实现了超过 50% 的语码转换减少，而 SFT+GRPO 的降幅远不及此（Table 1）。

**3. 与 SFT+Penalty 的对比。** SFT+Penalty 在交叉熵损失中直接加入惩罚项，降低模型对目标语言词元的预测概率。该方法作用于输出概率分布，缺乏对语言特异性特征的定向控制。SASFT 则通过稀疏自编码器（SAE）精确识别各语言对应的特异性特征方向，并仅在这些方向上施加约束，避免了盲目压制输出概率可能带来的语义质量下降。

### 技术路线定位：SAE 引导的表征约束范式

SASFT 的技术路线可概括为“SAE 引导的表征约束范式”，其流程由三个模块构成：

1. **语言特异性特征识别**：为模型每一层训练稀疏自编码器，计算每个特征的独语度量 $\nu_s^L = \mu_s^L - \gamma_s^L$（Eq. 7），其中 $\mu_s^L$ 为特征 $s$ 在语言 $L$ 上的平均激活值，$\gamma_s^L$ 为在其他语言上的平均激活值。按 $\nu$ 值降序排列后，选取排名最高的若干特征作为语言 $L$ 的特异性特征集 $\mathcal{S}_L$。

2. **SASFT 训练**：对非目标语言 $j$ 的训练样本，计算当前残差流在 $\mathcal{S}_L$ 上的预激活值，将其超过预设阈值 $\alpha_j$ 的部分求和作为辅助损失（Eq. 8），与原始交叉熵损失联合反向传播更新模型参数（Eq. 9）。阈值 $\alpha_j$ 使用预估计的各非目标语言的平均预激活值，而非直接设为 0——消融实验表明这一选择在大多数配置下更优（Table 3）。

3. **评估**：使用基于 Unicode 脚本的检测方法计算模型回复中的非预期语言比例（Eq. 2），同时评估模型在 MMLU、HumanEval、Flores-200、HellaSwag、LogiQA、IFEval、MGSM 六个多语言基准上的性能。

### 适用边界与关键设计选择

**多层与多特征联合干预的必要性。** 消融实验表明，仅在单层或单个特征上施加 SASFT 约束的效果有限且不稳定。同时作用于多个连续层（multi-layer）和多个排名靠前的语言特征（multi-feature）的方案，在降低语码转换比例的同时显著减小了性能波动（Figure 6, Figure 7）。这表明语言特异性信息在模型中呈分布式表征，需要联合干预多个表征位点才能稳定抑制非预期语言切换。

**阈值设定的影响。** 将阈值 $\alpha_j$ 设为预估计平均预激活值的 SASFT，在大多数配置下优于直接设 $\alpha_j=0$ 的 SASFT_zero 变体（Table 3）。这暗示语言特异性特征在非目标语言上存在一定的“基线激活”，将其完全压制至零可能过于激进，而允许保留基线水平的激活更有利于维持模型的正常多语言能力。

**泛化性证据。** 该方法在 Gemma-2-2B、Gemma-2-9B、Llama-3.1-8B、Qwen3-1.7B-Base、Qwen3-8B-Base 五款不同规模、不同家族的基座模型上均表现出一致的有效性，涵盖中文、俄语、韩语三种目标语言（Table 1）。在 6 个多语言基准上，SASFT 的总成绩与 SFT 基线持平或略优，未出现系统性性能崩塌（Table 2），说明方法在抑制语码转换的同时保留了多语言能力。

### 局限与开放问题

论文未明确列出方法的局限性，但以下问题值得关注：

1. **语言特异性特征的识别依赖于单语数据。** $\nu$ 度量的计算需要各语言的单语数据集 $\mathcal{D}_L$，对于低资源语言或语料稀缺的语言变体，特征识别的可靠性可能下降。论文未对此进行消融或讨论。

2. **超参数敏感性。** SASFT 引入了多个超参数，包括惩罚系数 $\lambda$、特征数量、层数选择、阈值 $\alpha_j$ 的估计方式等。论文提供了最优超参数设置（Table 7），但未系统分析各超参数之间的交互影响或跨模型迁移的鲁棒性。

3. **语码转换方向的非对称性。** 论文聚焦于“任意语言→中文/俄语/韩语”的切换方向，未讨论反向切换（如中文→其他语言）是否同样适用。语言特异性特征在不同切换方向上是否对称地发挥作用，尚需进一步验证。

4. **与推理时干预的关系。** SASFT 将抑制逻辑内化至训练阶段，避免了推理时的外部干预。但论文未比较 SASFT 与推理时方向消融在计算开销、部署灵活性等方面的优劣，也未讨论两者是否可以互补使用。

## 原文 PDF

![[paperPDFs/ICLR_2026/SASFT_Sparse_Autoencoder_guided_Supervised_Finetuning_to_Mitigate_Unexpected_Code_Switching_in_LLMs.pdf]]

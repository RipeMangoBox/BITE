---
title: "BioX-Bridge: Model Bridging for Unsupervised Cross-Modal Knowledge Transfer across Biosignals"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BioX_Bridge_Model_Bridging_for_Unsupervised_Cross_Modal_Knowledge_Transfer_across_Biosignals.pdf
project_link: null
code_link: https://github.com/chenqi-li/BioX-Bridge
openreview_forum_id: 1448q0s3zZ
aliases:
- BB
- BioX-Bridge
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "通过在已预训练好的旧模态和新模态基础模型之间插入一个轻量级桥接网络，该网络仅需训练少量参数即可对齐中间表征，从而消除教师模型的前向推理开销并大幅降低训练所需内存。"
primary_logic: "核心思想是利用两个模态已有基础模型的强大表征能力，通过一个可训练的桥接网络实现跨模态信息流。桥接位置选择（两阶段：线性探针与CKA相似度）和原型网络架构（可学习原型集 + 低秩近似）是实现参数高效、性能鲁棒的关键。"
claims:
- "BioX-Bridge 在保持或提升跨模态迁移性能的同时，将可训练参数减少了 88–99%"
- "在 ISRUC EEG→ECG 迁移上，BioX-Bridge 使用 1.8M 参数（仅为 KD 基线 30.4M 的 5.9%）即达到相当的平衡准确率"
- "桥接位置选择策略在 WESAD PPG→ECG 上将平衡准确率从固定位置的 48.34% 提升至 52.02%"
- "原型网络架构在仅 0.4M 参数下显著优于全连接桥接（15.4M），平衡准确率分别为 52.02% 和 48.59%"
---

# BioX-Bridge: Model Bridging for Unsupervised Cross-Modal Knowledge Transfer across Biosignals

> [!tip] 核心洞察
> 核心思想是利用两个模态已有基础模型的强大表征能力，通过一个可训练的桥接网络实现跨模态信息流。桥接位置选择（两阶段：线性探针与CKA相似度）和原型网络架构（可学习原型集 + 低秩近似）是实现参数高效、性能鲁棒的关键。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BioX-Bridge：跨生物信号的无监督跨模态知识迁移模型桥接 |
| 英文题名 | BioX-Bridge: Model Bridging for Unsupervised Cross-Modal Knowledge Transfer across Biosignals |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=1448q0s3zZ) · [GitHub](https://github.com/chenqi-li/BioX-Bridge) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | BioX-Bridge |
| Dataset | ISRUC (EEG → ECG), FOG (EEG → EMG) |

> [!tip] 效果简介
> - ISRUC (EEG → ECG) 上，Balanced Accuracy 为 60.11，对比 60.24 (KD)，变化 -0.13。
> - ISRUC (EEG → ECG) 上，F1-Weighted 为 74.02，对比 72.96 (KD)，变化 +1.06。
> - ISRUC (EEG → ECG) 上，Trainable Parameters 为 1.8M，对比 30.4M (KD)，变化 -94.1%。

## 概要

生物信号（如脑电、心电、肌电、光电容积脉搏波）在临床诊断与健康监测中应用广泛，但不同模态的标注数据获取成本差异巨大——部分模态拥有丰富标注，而另一些模态仅有原始信号。无监督跨模态知识迁移旨在将知识从标注充足的旧模态迁移至无标注的新模态，使新模态模型无需标签即可获得预测能力。

现有方法主要基于知识蒸馏（KD），在训练时需同时运行教师模型（旧模态）和学生模型（新模态），导致高计算与内存开销。**核心瓶颈在于**：对于参数量动辄数千万甚至上亿的大型基础模型，这种双模型并行的训练范式使得在消费级GPU上训练变得不可行。

BioX-Bridge 提出了一种**模型桥接**范式来解决这一问题。其**核心思想**是：在两个已预训练好的模态基础模型之间插入一个轻量级桥接网络，仅训练该桥接网络即可对齐中间表征，从而彻底消除教师模型的前向推理开销。这一设计将训练对象从整个学生模型（参数量与教师相当）转变为仅训练桥接网络（参数可低至0.2M）。

方法的关键创新体现在两个层面：

- **桥接位置选择**：采用两阶段自动选择策略——通过线性探针评估新模型各层表征对伪标签的预测能力以确定桥接输入层，再通过线性CKA相似度寻找旧模型中最匹配的输出层，避免手动固定位置带来的性能损失。
- **桥接架构设计**：提出原型网络架构，由可学习原型集与低秩近似模块组成，以极低参数量实现高效的表征空间投影。

**核心结论**：BioX-Bridge 在三个生物信号数据集（ISRUC、FOG、WESAD）的六个跨模态迁移场景上，以仅1.2%–5.9%的可训练参数（减少88–99%），达到了与知识蒸馏方法相当或更优的迁移性能。例如在 WESAD 的 PPG→ECG 迁移上，BioX-Bridge 仅使用0.4M参数即达到52.02%的平衡准确率，显著优于KD的47.03%（30.4M参数）。消融实验进一步验证了桥接位置选择策略和原型网络架构各自对性能的关键贡献。

**方法定位**：BioX-Bridge 属于参数高效的无监督跨模态知识迁移方法，可纳入**方法谱系**中“基于表征对齐的轻量级迁移”分支。与传统的 KD（Hinton et al., 2015）和 KD-Contrast（Abbaspourazad et al., 2024b）等需要完整训练学生模型的方法不同，BioX-Bridge 通过冻结两个基础模型并仅训练桥接网络，实现了训练开销的指数级降低，尤其适用于大模型时代的生物信号分析场景。

### 生物信号的多模态挑战与基础模型

生物信号（如脑电图 EEG、心电图 ECG、肌电图 EMG、光电容积描记图 PPG）在健康监测与疾病诊断中扮演着关键角色。近年来，大规模自监督预训练基础模型在单模态生物信号任务上取得了显著成功，例如 **HuBERT-ECG** 和 **PaPaGei** 等模型能够从单一模态中提取丰富的表征信息。然而，这些模型通常针对特定模态独立训练，当目标模态缺乏标注数据时，其监督任务性能严重受限。

### 跨模态知识迁移的现实瓶颈

在实际应用中，不同生物信号模态的标注资源分布极不均衡：某些模态（如 ECG）拥有大量标注数据，而另一些模态（如 PPG）的标注数据却十分稀缺。无监督跨模态知识迁移（unsupervised cross-modal knowledge transfer）旨在利用旧模态（标注充足）的标签知识，帮助新模态（无标注）完成下游任务，从而绕过新模态的标注瓶颈。

现有方法主要依赖**知识蒸馏（Knowledge Distillation, KD）**及其变体（如 KD-Contrast），其核心思路是将旧模态模型作为教师，训练一个新模态学生模型去模仿教师的输出 logits 或软标签。这一范式存在一个关键瓶颈：**训练过程中必须同时运行教师和学生两个完整模型**，导致极高的计算和内存开销。对于参数量动辄数千万乃至上亿的大型基础模型而言，这一限制尤为严重——例如，在 WESAD 数据集上从 PaPaGei 向 ECG-FM 进行知识蒸馏，即使仅使用 batch size 为 8，也需超过 32GB 的显存。

### BioX-Bridge 的核心动机

本文的核心洞察在于：**既然两个模态均已存在强大的预训练基础模型，为何还要重新训练整个新模态模型？** 一个更高效的方案是在两个冻结的预训练模型之间插入一个轻量级的“桥接网络”，仅训练该桥接网络即可实现跨模态表征对齐。这一思路将训练对象从“整个学生模型”转变为“仅桥接网络”，从而在根本上消除教师模型的前向推理开销，并大幅降低训练所需的内存和参数量。

具体而言，BioX-Bridge 框架的设计围绕两个关键问题展开：

1. **桥接位置选择**：在旧模型和新模型的哪一层插入桥接网络，才能实现最优的表征对齐？固定位置（如最后一层）往往无法适配不同模态对之间的表征差异，需要一种自动化的选择策略。

2. **桥接架构设计**：如何在极低参数量的约束下，构建一个足够表达力的桥接网络，使其能够有效映射跨模态的中间表征？

通过解决上述两个问题，BioX-Bridge 旨在实现一个**参数高效、性能鲁棒**的无监督跨模态知识迁移框架，使得在资源受限的环境中也能充分利用大型基础模型的能力。

## 核心方法与创新机理

BioX-Bridge 的核心创新在于从根本上改变了无监督跨模态知识迁移的训练范式：**将“训练整个学生模型”转变为“仅训练一个轻量级桥接网络”**。这一转变解决了现有基于知识蒸馏（KD）方法的关键瓶颈——训练时必须同时运行教师和学生模型，导致极高的计算和内存开销，尤其对于大型基础模型而言，这种限制变得难以承受。

具体而言，BioX-Bridge 在以下四个维度上实现了相对于 KD 基线的突破：

### 训练对象的根本转变

传统 KD 方法（Hinton et al., 2015）及其变体 KD-Contrast（Abbaspourazad et al., 2024b）需要训练整个新模态模型（学生），参数量与教师模型相当。BioX-Bridge 则利用两个模态**已有预训练基础模型**的强大表征能力，仅在其间插入一个可训练的桥接网络。该桥接网络仅需学习将新模态的中间表征投影至旧模态表征空间，从而完全消除了教师模型的前向推理开销。在 WESAD（PPG→ECG）任务上，可训练参数从 KD 的 30.4M 降至 **0.4M**（降低 98.7%）；在 ISRUC（EEG→ECG）上，参数从 30.4M 降至 **1.8M**（降低 94.1%），而性能保持相当甚至更优（平衡准确率 60.11 vs 60.24）。

### 对齐目标的层级下移

KD 方法对齐的是输出 logits 或软标签，这要求新模态模型完整前向传播。BioX-Bridge 将对齐目标下移至**中间表征层**：桥接网络将新模型第 $m$ 层的输出 $h_m^{(new)}$ 投影为 $\tilde{h}_l^{(old)}$，使其逼近旧模型第 $l$ 层的表征。预测通过组合 $g_{\omega}^{(old)} \circ f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})$ 完成，旧模型的后层和任务头被直接复用，无需额外训练。这种设计使得训练仅需优化桥接参数 $\psi$，最小化对齐损失：

$$\underset{\psi}{\arg\min}\ \mathcal{L}_{align}\left(f_{\theta}^{(old)}(x^{(old)}), f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})\right)$$

### 桥接位置的自动选择策略

传统方法通常手动或固定在某层（如最后一层）进行知识迁移。BioX-Bridge 提出了**两阶段自动选择策略**：

- **输入位置选择**：通过在新模型各层上训练线性探针，评估其对旧模型生成伪标签的预测性能，选择损失最小的层 $m$：
  $$\operatorname*{argmin}_{m \in \{1,...,M\}} \frac{1}{|\mathcal{D}^{(pair)}|} \sum_{i=1}^{|\mathcal{D}^{(pair)}|} \mathcal{L}_{probe}(g_{\eta}(h_{m,i}^{(new)}), \hat{y}_i)$$

- **输出位置选择**：计算新模型选中层表征与旧模型各层表征的线性 CKA 相似度，选择相似度最高的层 $l$：
  $$\underset{l \in \{1,...,L\}}{\mathrm{argmax\ CKA_{linear}}}(H_m^{(new)}, H_l^{(old)})$$

该策略的有效性在 WESAD（PPG→ECG）上得到验证：选择位置达到平衡准确率 52.02%，而固定位置平均仅 48.34%，提升约 **3.68 个百分点**。

### 原型网络架构的参数高效设计

桥接网络的架构设计是参数效率的关键。BioX-Bridge 采用了**原型网络**，由两个核心组件构成：

- **可学习原型集** $P \in \mathbb{R}^{N_p \times d_l^{(old)}}$：存储旧模态本征表征信息
- **低秩近似模块**（矩阵 $A$ 和 $B$）：生成原型向量的聚合权重，将投影参数量从 $O(d_m^{(new)} \cdot d_l^{(old)})$ 降至 $O(N_p \cdot (d_m^{(new)} + d_l^{(old)}))$

前向计算通过池化、低秩矩阵乘法和原型聚合完成：
$$\tilde{\pmb{h}}_l^{(old)} = \mathrm{Reshape}_{N_l^{(old)} \times N_p} \left( \mathrm{Pool}(\pmb{h}_m^{(new)}) \otimes \pmb{A} \otimes \pmb{B} \right) \otimes \pmb{P}$$

在 WESAD（PPG→ECG）上，原型网络（0.4M 参数）的平衡准确率为 52.02%，显著优于全连接桥接（15.4M 参数）的 48.59%，参数量仅为后者的 **1/38**。

### 创新总结

BioX-Bridge 的创新并非单一技术点的改进，而是通过“冻结基础模型 + 轻量桥接 + 自动位置选择”的系统性设计，实现了**参数效率与迁移性能的双赢**。该方法在三个数据集、六个迁移方向上，以 88–99% 的参数削减达到了与 KD 相当或更优的性能，同时大幅降低了训练时的计算和内存需求。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_1448q0s3zZ/figures/002_Figure_2.jpg]]
*Figure 2: Overview of BioX-Bridge. (a) At the training stage, the bridge learns to project intermediate representations from the new modality to the old modality, such that it mimics the output of the old modality model. (b) At the inference stage, the bridge has been constructed and enables the flow of information between the two models in order to make predictions on data from the new modality. (c) The bridge consists of a low-rank approximation module and a prototype set. The low-rank approximation module generates aggregation weights for the prototype vectors*

BioX-Bridge 的核心思想是在两个已预训练好的生物信号基础模型之间插入一个轻量级桥接网络，通过对齐中间表征来实现无监督跨模态知识迁移。与传统的知识蒸馏方法不同，该框架在训练时无需运行教师模型（旧模态模型）的前向推理，仅需训练桥接网络参数，从而大幅降低计算和内存开销。

### 问题设定

给定三个数据集：带标签的旧模态数据集 $\mathcal{D}^{(old)}$、无标签的新模态数据集 $\mathcal{D}^{(new)}$，以及无标签的配对数据集 $\mathcal{D}^{(pair)}$（包含时间对齐的旧模态和新模态信号对）。目标是利用旧模态上已预训练的基础模型 $f_{\theta}^{(old)}$ 和任务头 $g_{\omega}^{(old)}$，以及新模态上已预训练的基础模型 $f_{\phi}^{(new)}$，使新模态数据能够获得准确的预测。

### 桥接信息流

框架的核心操作流程如下：

**1. 中间表征提取**：从新模态模型的前 $m$ 层提取中间表征：

$$h_m^{(new)} = f_{\phi_{\leq m}}^{(new)}(x^{(new)})$$

**2. 桥接投影**：通过桥接网络 $b_{\psi}$ 将新模态表征投影至旧模态表征空间：

$$\tilde{h}_l^{(old)} = b_{\psi}(h_m^{(new)})$$

**3. 最终预测**：将投影后的表征送入旧模态模型的后续层（第 $l+1$ 层至末层）及任务头，获得最终预测：

$$\tilde{y} = g_{\omega}^{(old)} \circ f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})$$

### 两大关键组件

框架由两个关键组件构成（见 Figure 2）：

**桥接位置选择**：确定桥接网络应连接新模态的哪一层（输入位置 $m$）和旧模态的哪一层（输出位置 $l$）。该过程采用两阶段策略：首先通过线性探针评估新模型各层表征对旧模型伪标签的预测能力以选择 $m$，然后通过线性 CKA 相似度最大化选择与 $m$ 层表征最相似的旧模型层作为 $l$。

**桥接架构设计**：桥接网络采用原型网络架构，由两部分组成：
- **原型集** $\mathbf{P} \in \mathbb{R}^{N_p \times d_l^{(old)}}$：一组可学习的原型向量，用于存储旧模态表征空间的本征信息。
- **低秩近似模块**（矩阵 $\mathbf{A}, \mathbf{B}$）：通过低秩因子矩阵生成原型向量的聚合权重，大幅减少投影参数量。

桥接网络的前向计算可表示为：

$$\tilde{\mathbf{h}}_l^{(old)} = \mathrm{Reshape}_{N_l^{(old)} \times N_p} \left( \mathrm{Pool}(\mathbf{h}_m^{(new)}) \otimes \mathbf{A} \otimes \mathbf{B} \right) \otimes \mathbf{P}$$

### 训练与推理

**训练阶段**（Figure 2a）：使用配对数据，最小化旧模型最终表征与桥接后新模型表征之间的对齐损失（余弦损失），仅更新桥接网络参数 $\psi$：

$$\underset{\psi}{\arg\min}\ \mathcal{L}_{align}\left(f_{\theta}^{(old)}(x^{(old)}), f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})\right)$$

**推理阶段**（Figure 2b）：桥接网络已构建完成，新模态数据依次经过新模型前 $m$ 层、桥接网络、旧模型后 $l$ 层和任务头，直接输出预测结果，无需旧模态信号输入。

整个学习流程详见 Algorithm 1，涵盖了桥接位置选择、桥接网络训练和推理三个步骤。

BioX-Bridge 的核心是将跨模态知识迁移问题转化为一个**轻量级桥接网络的训练问题**，而非传统知识蒸馏中对整个学生模型的端到端训练。框架由三个关键模块构成：**桥接位置选择**、**桥接架构设计**和**桥接训练目标**。

### 3.1 问题形式化与桥接推理

给定旧模态预训练模型 $f_{\theta}^{(old)} = g_{\omega}^{(old)} \circ f_{\theta}^{(old)}$（编码器 + 任务头）和新模态预训练编码器 $f_{\phi}^{(new)}$，桥接网络 $b_{\psi}$ 的目标是将新模态的中间表征投影到旧模态的表征空间中。

新模态第 $m$ 层的中间表征提取为：

$$h_m^{(new)} = f_{\phi_{\leq m}}^{(new)}(x^{(new)})$$

通过桥接网络投影至旧模态第 $l$ 层的表征空间：

$$\tilde{h}_l^{(old)} = b_{\psi}(h_m^{(new)})$$

最终预测由新模态编码器前端、桥接网络、旧模态编码器后端及任务头组合完成：

$$\tilde{y} = g_{\omega}^{(old)} \circ f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})$$

这一组合推理模式的关键优势在于：**推理时无需运行完整的教师模型**，仅需桥接网络与部分旧模型层，大幅降低了计算开销。

### 3.2 桥接位置选择：两阶段策略

桥接的输入位置 $m$（从新模型哪一层提取表征）和输出位置 $l$（向旧模型哪一层注入表征）对迁移性能有显著影响。BioX-Bridge 提出两阶段自动选择策略：

**阶段一：桥接输入位置选择。** 在新模型各层上训练线性探针，以旧模型生成的伪标签 $\hat{y}$ 为监督信号，选择线性分类损失最小的层作为输入位置：

$$\operatorname*{argmin}_{m \in \{1,...,M\}} \frac{1}{|\mathcal{D}^{(pair)}|} \sum_{i=1}^{|\mathcal{D}^{(pair)}|} \mathcal{L}_{probe}(g_{\eta}(h_{m,i}^{(new)}), \hat{y}_i)$$

该策略的直觉是：**该层表征对旧模型所掌握的任务信息具有最强的线性可分性**，因此是信息注入的最佳起点。

**阶段二：桥接输出位置选择。** 固定输入层 $m$ 后，计算该层表征 $H_m^{(new)}$ 与旧模型各层表征 $H_l^{(old)}$ 的线性中心核对齐相似度（Linear CKA），选择相似度最高的层作为输出位置：

$$\underset{l \in \{1,...,L\}}{\mathrm{argmax\ CKA_{linear}}}(H_m^{(new)}, H_l^{(old)})$$

其中线性 CKA 定义为：

$$\mathrm{CKA_{linear}}(H_m^{(new)}, H_l^{(old)}) = \frac{\mathrm{HSIC}(H_m^{(new)}, H_l^{(old)})}{\sqrt{\mathrm{HSIC}(H_m^{(new)}, H_m^{(new)}) \cdot \mathrm{HSIC}(H_l^{(old)}, H_l^{(old)})}}$$

该策略的直觉是：**选择表征空间结构最相似的旧模型层作为注入点，最小化桥接网络需要弥合的语义鸿沟**。

消融实验验证了该策略的有效性：在 WESAD PPG→ECG 任务上，自动选择位置将平衡准确率从固定位置的 48.34% 提升至 52.02%（Table A4）。

### 3.3 桥接架构：原型网络与低秩近似

桥接网络需要将新模态表征投影到旧模型的高维表征空间。若使用全连接层直接投影，参数量将随维度乘积急剧增长。BioX-Bridge 采用**原型网络**架构，包含两个核心组件：

**可学习原型集** $P \in \mathbb{R}^{N_p \times d_l^{(old)}}$：存储 $N_p$ 个原型向量，每个向量位于旧模态表征空间中，代表该空间的“基向量”。

**低秩近似模块**：通过两个低秩因子矩阵 $A$ 和 $B$ 生成原型向量的聚合权重，避免直接学习高维投影矩阵。前向计算过程为：

$$\tilde{\pmb{h}}_l^{(old)} = \mathrm{Reshape}_{N_l^{(old)} \times N_p} \left( \mathrm{Pool}(\pmb{h}_m^{(new)}) \otimes \pmb{A} \otimes \pmb{B} \right) \otimes \pmb{P}$$

该公式的运算流程为：（1）对新模态表征进行池化降维；（2）通过低秩矩阵 $A$、$B$ 的乘法生成聚合权重；（3）用该权重对原型向量集 $P$ 进行加权组合，得到投影后的旧模态表征。

该架构的**参数效率**来源于：原型数量 $N_p$ 和低秩秩 $r$ 远小于表征维度，使得可训练参数量控制在极低水平。消融实验表明，原型网络在仅 0.4M 参数下即达到 52.02% 平衡准确率，而全连接桥接（FC-Bridge）使用 15.4M 参数仅获得 48.59%（Table A8）。

### 3.4 桥接训练目标

桥接网络 $b_{\psi}$ 的训练目标是最小化投影表征与旧模型真实表征之间的对齐损失。具体而言，使用配对数据 $(x^{(old)}, x^{(new)})$，最小化旧模型最终表征 $f_{\theta}^{(old)}(x^{(old)})$ 与桥接后新模态表征 $f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})$ 之间的余弦相似度损失：

$$\underset{\psi}{\arg\min}\ \mathcal{L}_{align}\left(f_{\theta}^{(old)}(x^{(old)}), f_{\theta_{>l}}^{(old)} \circ b_{\psi} \circ f_{\phi_{\leq m}}^{(new)}(x^{(new)})\right)$$

训练过程中，旧模型和新模型参数**完全冻结**，仅更新桥接网络的参数 $\psi = \{A, B, P\}$。这从根本上消除了传统知识蒸馏中教师模型的前向推理开销，并将可训练参数量削减了 88–99%（Table 1）。

## 实验与关键发现

### 核心性能对比

BioX-Bridge 在三个生物信号数据集、六个跨模态迁移方向上进行了系统评估。其核心优势在于：以极低的训练参数量达到与完整知识蒸馏（KD）方法相当甚至更优的迁移性能。

**ISRUC 睡眠分期数据集**上，BioX-Bridge 在 EEG→ECG 方向仅使用 1.8M 可训练参数（KD 基线 30.4M 的 5.9%），即达到 60.11% 的平衡准确率，与 KD 的 60.24% 几乎持平；加权 F1 反而从 KD 的 72.96% 提升至 74.02%（Table A1）。在 ECG→EEG 方向，BioX-Bridge 以 1.7M 参数取得 72.24% 的平衡准确率，超越 KD 的 68.64%（Table A2）。

**FOG 冻结步态数据集**上，EEG→EMG 方向 BioX-Bridge 以 1.2M 参数达到 72.24% 平衡准确率，显著优于 KD（68.64%）和 KD-Contrast（Table A2）。

**WESAD 情感识别数据集**上，参数效率优势最为突出。PPG→ECG 方向 BioX-Bridge 仅使用 0.4M 参数（KD 30.4M 的 1.3%），平衡准确率达到 52.02%，比 KD 的 47.03% 高出约 5 个百分点（Table A3b）。ECG→PPG 方向以 0.2M 参数达到 49.57%，同样优于 KD（47.86%）。

**参数效率总结**：跨所有迁移场景，BioX-Bridge 将可训练参数减少了 88–99%，同时保持或提升了迁移性能。这一效率优势的关键在于：KD 方法在训练时需同时运行完整的教师和学生模型进行前向传播，而 BioX-Bridge 仅训练一个轻量级桥接网络，两个基础模型保持冻结。

### 消融实验

#### 桥接位置选择策略的有效性

桥接位置选择是 BioX-Bridge 的关键设计。在 WESAD PPG→ECG 场景下，使用自动选择策略（Selected）的平衡准确率为 52.02%，而固定九种预定义位置的平均值仅为 48.34%（Table A4），提升了约 3.7 个百分点。这表明简单的固定位置策略无法可靠地找到最优的信息对齐层，两阶段选择策略（线性探针选输入层 + 线性 CKA 选输出层）对于跨模态表征对齐至关重要。

#### 桥接架构消融

原型网络架构相比朴素的全连接桥接（FC-Bridge）展现出显著的性能与效率优势。在 WESAD PPG→ECG 上，BioX-Bridge 的原型网络以 0.4M 参数达到 52.02% 平衡准确率，而 FC-Bridge 使用 15.4M 参数（38 倍）仅取得 48.59%（Table A8）。原型集与低秩近似模块的组合不仅大幅减少了参数量，还通过结构化先验提升了表征投影的质量。

#### 桥接秩与原型数量的鲁棒性

桥接训练对超参数表现出良好的鲁棒性。在 WESAD 和 ISRUC 数据集上，当桥接秩 r 和原型数量 Np 在较大范围内变化时，平衡准确率保持相对稳定，性能在约 0.75M 参数附近达到峰值（Figure 4a, 4b）。这意味着实际部署时无需精细调参即可获得接近最优的性能。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_1448q0s3zZ/figures/008_Figure_4.jpg]]
*Figure 4: Bridge Training Ablation. Blue: Balanced Accuracy. Red: Number of Parameters. We vary (a) bridge rank, (b) number of prototypes, and (c) pair dataset size to understand the robustness of BioX-Bridge and its performance under a low-data regime*

#### 配对数据量的影响

桥接性能对配对数据量表现出一定的容忍度。当配对数据集缩减至 50% 时，性能下降约 2 个百分点；但进一步缩减至 20% 时，FOG 数据集上出现急剧下降（Figure 4c, Figure A10c）。这表明 BioX-Bridge 在中等数据稀缺场景下仍可有效工作，但存在一个临界阈值，低于该阈值时跨模态对齐将失效。

#### 基础模型选择的影响

基础模型的质量直接影响迁移性能。将 HuBERT-ECG 替换为 ECG-FM 后，BioX-Bridge 的平衡准确率从 52.02% 降至约 49%（Table A5），说明更强的教师模型表征能力是桥接迁移的上限约束。使用更大尺寸的 HuBERT-ECG（Large, 183M）可将平衡准确率进一步提升至 54.94%（Table A7），验证了基础模型规模与迁移性能的正相关关系。

### 失败模式与局限性

1. **伪标签依赖性**：桥接输入位置的选择依赖于旧模型生成的伪标签质量。若旧模型本身性能不佳（如某些数据集上 Oracle 准确率本身有限），线性探针的评估结果可能误导位置选择，进而影响桥接训练质量。

2. **极低数据场景退化**：当配对数据量降至 20% 时，部分数据集（如 FOG）上性能出现急剧下降，表明桥接网络对配对数据量存在最低需求阈值。

3. **受试者划分敏感性**：重新划分受试者后，KD-Contrast 的性能下降比 KD 更为严重（Table A9），但 BioX-Bridge 在此场景下的具体表现需要进一步验证。不同数据集划分策略可能导致结果波动，这是跨模态迁移方法普遍面临的挑战。

4. **任务特异性限制**：当前框架仍需为特定任务训练分类头，未实现完全任务无关的跨模态迁移。桥接网络学习的是表征空间对齐，但下游任务适配仍需标注数据。

5. **模态对限制**：方法要求存在成对的旧模态与新模态数据用于桥接训练，且两种模态均需已有预训练基础模型。这限制了可应用的模态对范围，对于缺乏预训练模型的新兴模态不适用。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_1448q0s3zZ/figures/017_Table_9.jpg]]
*Table 9: Table A4: Bridge Position Ablation. WESAD (PPG → ECG). We study the effectiveness of the bridge selection strategy*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_1448q0s3zZ/figures/046_Table_13.jpg]]
*Table 13: Table A8: Bridge architecture ablation. WESAD (PPG → ECG). We replace the proposed bridge network (BioX-Bridge) with a fully connected layer (FC-Bridge)*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_1448q0s3zZ/figures/009_Table_2.jpg]]
*Table 2: Bridge Position Ablation. Comparison of different bridge position selection strategies with respect to BioX-Bridge. “Fixed” represents the average of 9 predefined positions, combining the first, middle, and last layers for both the input and output positions*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_1448q0s3zZ/figures/010_Table_3.jpg]]
*Table 3: Foundation Model Ablation. We compare the transfer performance by replacing the ECG foundation model HuBERT-ECG with ECG-FM*

## 定位与知识库关联

### 1. 方法定位与基线关系

BioX-Bridge 处于**无监督跨模态知识迁移**与**参数高效微调**的交叉领域，其核心思想是在两个已预训练好的基础模型之间插入一个轻量级桥接网络，而非重新训练或微调整个学生模型。

#### 1.1 与知识蒸馏方法的对比

传统的无监督跨模态知识迁移主要依赖知识蒸馏框架。标准 **KD**（Hinton et al., 2015）通过让学生模型模仿教师模型的输出 logits 来实现迁移，其瓶颈在于：**训练时需同时运行教师和学生模型，导致高计算和内存开销**。对于大型基础模型，这一限制尤为严重——论文指出，在 WESAD 数据集上从 PaPaGei 向 ECG-FM 进行蒸馏时，即使 batch size 仅为 8，也需超过 32GB 的显存。

**KD-Contrast**（Abbaspourazad et al., 2024b）在 KD 基础上引入对比损失，试图增强表征对齐质量，但并未解决训练效率问题。BioX-Bridge 通过以下方式从根本上改变了这一范式：

| 对比维度 | KD / KD-Contrast | BioX-Bridge |
|----------|------------------|-------------|
| 训练对象 | 整个学生模型（参数量与教师相当） | 仅桥接网络（可低至 0.2M） |
| 对齐目标 | 输出 logits 或软标签 | 中间表征（旧模型第 L 层输出） |
| 教师模型状态 | 训练时需前向推理 | 冻结，仅提取固定表征作为对齐目标 |
| 可训练参数（WESAD PPG→ECG） | 30.4M（KD） | 0.4M（减少 98.7%） |

这一设计使得 BioX-Bridge 在**保持或提升迁移性能的同时，将可训练参数减少了 88–99%**。例如，在 ISRUC EEG→ECG 迁移中，BioX-Bridge 以 1.8M 参数（仅为 KD 基线 30.4M 的 5.9%）即达到 60.11% 的平衡准确率，与 KD 的 60.24% 基本持平。

#### 1.2 与数据翻译方法的对比

**CardioGAN**（Sarkar & Etemad, 2021）采用 GAN 将 PPG 信号翻译为 ECG 信号，属于数据层面的跨模态迁移。该方法需要训练生成模型，且翻译质量直接影响下游任务性能。BioX-Bridge 则在**表征层面**进行对齐，避免了对信号重建质量的依赖，同时受益于预训练基础模型已学到的强大表征。

#### 1.3 与 Oracle 的性能差距

Oracle 代表使用旧模态数据（即教师模态）进行监督训练的性能上界。BioX-Bridge 的性能始终低于 Oracle，这是无监督跨模态迁移的固有局限——新模态缺乏标注数据，仅能通过旧模态的知识间接获益。例如在 WESAD PPG→ECG 上，Oracle 的平衡准确率为 64.57%，而 BioX-Bridge 为 52.02%，差距约 12.5 个百分点。这一差距的大小取决于两个模态间表征的可迁移程度。

### 2. 核心创新与设计空间

BioX-Bridge 的因果调节变量（causal knob）体现在两个关键设计选择上：

#### 2.1 桥接位置选择策略

传统方法通常将桥接固定在某一层（如最后一层），但**不同层级的表征包含不同粒度的信息**，固定位置可能错配语义层级。BioX-Bridge 提出两阶段自动选择策略：

- **输入位置选择**：在新模型各层上训练线性探针，评估其对旧模型伪标签的预测性能，选择最佳输入层 $m$。
- **输出位置选择**：计算新模型选中层的表征与旧模型各层表征的线性 CKA 相似度，选择最相似的输出层 $l$。

消融实验验证了这一策略的有效性：在 WESAD PPG→ECG 上，使用选择策略将平衡准确率从固定位置（9 个预定义位置的平均）的 48.34% 提升至 52.02%（Table A4），提升约 3.7 个百分点。这表明**桥接位置的合理选择对迁移质量有实质性影响**。

#### 2.2 原型网络架构

桥接网络需要在两个高维表征空间之间建立映射。全连接桥接（FC-Bridge）虽直接但参数量大（15.4M），且容易过拟合。BioX-Bridge 的原型网络由两个模块组成：

- **可学习原型集 $P \in \mathbb{R}^{N_p \times d_l^{(old)}}$**：存储旧模态本征表征信息。
- **低秩近似模块 $A, B$**：通过低秩因子矩阵生成原型向量的聚合权重，大幅减少投影参数量。

消融实验表明，原型网络在仅 0.4M 参数下显著优于 FC-Bridge（15.4M），平衡准确率分别为 52.02% 和 48.59%（Table A8），参数仅为后者的 1/38。这一结果说明**参数效率与表征对齐质量并非互斥**，精心设计的归纳偏置（原型 + 低秩）能够同时兼顾两者。

### 3. 适用边界与鲁棒性

#### 3.1 对基础模型的依赖

BioX-Bridge 假设两种模态均存在预训练的基础模型。基础模型的质量直接影响迁移性能：

- 使用更大的 HuBERT-ECG（large, 183M）替代 small 版本（30M）时，WESAD PPG→ECG 的平衡准确率从 52.02% 提升至 54.94%（Table A7）。
- 将 HuBERT-ECG 替换为另一 ECG 基础模型 ECG-FM 时，BioX-Bridge 仍能保持优于 KD 基线的性能（BAcc 58.80 vs KD 57.86），且参数量仅为 0.11M（Table 3）。

这表明 BioX-Bridge 对基础模型的选择具有一定的泛化能力，但**性能上限受限于教师模型的质量**。若旧模态模型性能不佳，由其生成的伪标签可能误导桥接输入位置的选择，进而影响整体迁移效果。

#### 3.2 对配对数据量的敏感性

桥接训练需要成对的旧模态与新模态数据。消融实验（Figure 4c）显示：

- 当配对数据集大小减少至 50% 时，性能下降约 2 个百分点，表现相对稳健。
- 但在 FOG 数据集上，当配对数据降至 20% 时，性能出现急剧下降（Figure A10c）。

这一现象提示：**在极低数据量场景下，桥接训练的稳定性可能因数据集而异**，需要针对具体模态对进行验证。

#### 3.3 对超参数的鲁棒性

桥接秩 $r$ 和原型数量 $N_p$ 的消融实验（Figure 4a, 4b）显示，性能在较宽的参数范围内保持稳定，约在 0.75M 总参数量时达到峰值。这表明方法对超参数选择不敏感，具有较好的实用鲁棒性。

### 4. 局限性与开放问题

#### 4.1 已识别的局限

1. **配对数据依赖**：桥接训练需要成对数据，限制了可应用的模态对范围。无法利用未配对数据进行迁移。
2. **伪标签质量依赖**：桥接输入位置的选择依赖旧模型生成的伪标签，若旧模型性能不佳，可能引入系统性偏差。
3. **预训练模型前提**：框架假设两种模态均存在预训练基础模型，对于新兴或小众模态不适用。
4. **任务特异性**：当前方法仍需为特定任务训练分类头，未实现完全的任务无关迁移。
5. **数据划分敏感性**：受试者重新划分实验（Table A9）显示，不同划分方式会引起性能波动，提示方法的泛化稳定性有待进一步验证。

#### 4.2 论文提出的开放问题

1. **任务无关迁移**：无监督跨模态知识迁移是否应该与任务无关？能否开发无需任何标签数据且与任务无关的桥接位置选择策略？
2. **未配对数据利用**：能否利用未配对数据实现跨模态迁移，以扩展至任意模态组合？
3. **多模态扩展**：BioX-Bridge 在包含超过两种模态的数据集上表现如何？
4. **跨数据集泛化**：BioX-Bridge 能否泛化至共享相同模态的不同数据集之间？
5. **KD-Contrast 敏感性**：为何 KD-Contrast 在重新划分受试者后性能下降比 KD 更严重？这一现象可能暗示对比损失对数据分布变化更为敏感，但具体机制尚需进一步分析。

---

**证据强度说明**：本节的核心性能声明（参数减少 88–99%、桥接位置选择提升约 3% 准确率、原型网络优于 FC-Bridge）均有 Table A1–A8 等附录表格的定量支撑，置信度较高（≥0.9）。关于配对数据量降至 20% 时 FOG 上性能急剧下降的声明，置信度为 0.9，建议在引用时核对 Figure A10 的具体数值。关于 KD-Contrast 对数据划分敏感性的开放问题，论文未给出解释，属于待验证的观察。

## 原文 PDF

![[paperPDFs/ICLR_2026/BioX_Bridge_Model_Bridging_for_Unsupervised_Cross_Modal_Knowledge_Transfer_across_Biosignals.pdf]]

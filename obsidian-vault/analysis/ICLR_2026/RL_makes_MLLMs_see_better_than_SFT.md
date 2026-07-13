---
title: "RL makes MLLMs see better than SFT"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RL_makes_MLLMs_see_better_than_SFT.pdf
project_link: null
code_link: null
openreview_forum_id: 3gM6HwHvnc
aliases:
- PPIVO
- RMMSBTS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "采用 DPO 进行偏好对齐，通过对比损失提供更精细的梯度信号，使视觉编码器学习到更强、更局部化的特征表示。"
primary_logic: "DPO 的对比性质导致梯度集中在问题相关的视觉区域，增强了视觉编码器的定位和细节感知能力，从而显著提升 MLLM 在视觉密集型任务上的表现。"
claims:
- "DPO 在视觉相关的 VQA 基准上显著优于 SFT（例如 OCR & Chart VQA +4.2%p，Vision-Centric VQA +2.4%p）"
- "DPO 训练的视觉编码器在 ImageNet 线性探针上比 SFT 准确率更高（+1.83%p for SigLIP2-So/16）"
- "DPO 梯度信号更集中于问题相关区域，而 SFT 梯度较为发散"
- "DPO 训练后视觉编码器的分割召回率显著提升（+1.08%p for CLIP-L/14）"
---

# RL makes MLLMs see better than SFT

> [!tip] 核心洞察
> DPO 的对比性质导致梯度集中在问题相关的视觉区域，增强了视觉编码器的定位和细节感知能力，从而显著提升 MLLM 在视觉密集型任务上的表现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 强化学习使多模态大语言模型在视觉理解上优于监督微调 |
| 英文题名 | RL makes MLLMs see better than SFT |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3gM6HwHvnc) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | PIVOT (Preference-Instructed Vision OpTimization) |
| Dataset | Multi-benchmark Average (16 VQA tasks), ImageNet linear probe, OCR & Chart VQA (average), Vision-Centric VQA (average) |

> [!tip] 效果简介
> - Multi-benchmark Average (16 VQA tasks) 上，Score 为 SigLIP2-So/16 + PIVOT: 55.6，对比 SigLIP2-g/16 (original): 53.9，变化 +1.7。
> - ImageNet linear probe 上，Top-1 accuracy 为 DPO-trained encoder (SigLIP2-So/16 w/ Qwen-3B)，对比 SFT-trained encoder (same setup)，变化 +1.83%p。
> - OCR & Chart VQA (average) 上，Score 为 DPO，对比 SFT，变化 +4.2%p。

## 概要

当前多模态大语言模型（MLLM）普遍采用监督微调（SFT）作为训练范式，但研究发现，SFT 对视觉编码器的优化并不充分，导致模型在细粒度视觉理解任务上表现受限。本文系统对比了 SFT 与直接偏好优化（DPO）两种后训练策略对 MLLM 及其视觉编码器的影响，揭示了一个关键发现：**DPO 不仅能提升 MLLM 的整体性能，更能从根本上强化视觉编码器的表示质量**。

基于这一洞察，作者提出了 **PIVOT（Preference-Instructed Vision OpTimization）**——一种简洁的视觉编码器增强方法。PIVOT 的核心思路是：在标准的两阶段 MLLM 训练流程中，将第二阶段的 SFT 替换为 DPO 偏好对齐，随后将训练后的视觉编码器分离出来，作为即插即用的增强视觉骨干，集成到新的 MLLM 架构中。

实验结果表明，PIVOT 以极低的计算成本实现了显著的性能提升。在 16 个 VQA 基准测试上，PIVOT 增强的 SigLIP2-So/16 编码器平均得分达到 55.6，超越了原始 SigLIP2-g/16 的 53.9；在视觉密集型任务（OCR & Chart VQA、Vision-Centric VQA）上，DPO 相较 SFT 分别带来 4.2 和 2.4 个百分点的提升。更值得关注的是，PIVOT 训练仅需在 8 张 H100 GPU 上运行约 18 小时，计算成本不到完整预训练的 1%，却能获得超越更大规模视觉编码器的性能。

机制分析进一步揭示了 DPO 优势的根源：其对比性损失函数产生的梯度信号高度集中于问题相关的视觉区域，而 SFT 的梯度则相对发散。这种局部化的梯度反馈促使视觉编码器学习到更强的定位能力和更精细的特征表示，在 ImageNet 线性探针（+1.83%p）和语义分割探针（+1.08%p recall）上均验证了这一结论。

### 多模态大语言模型的训练范式

多模态大语言模型（MLLM）的主流架构通过一个多模态投影器将大语言模型（LLM）与视觉编码器连接起来，这一设计已被广泛验证有效。典型的训练流程遵循两阶段策略：第一阶段为预训练，在多样化的视觉-语言数据上训练全部参数，以对齐视觉与语言表征；第二阶段为后训练（post-training），旨在赋予模型指令遵循能力。

在后训练阶段，监督微调（SFT）一直是标准做法——通过最大化选定响应（chosen response）的似然来训练模型。然而，近年来强化学习（RL）方法，尤其是直接偏好优化（DPO），开始在 MLLM 后训练中崭露头角。DPO 通过偏好对齐的方式，在无需显式奖励模型的情况下，直接优化模型对选定响应和拒绝响应（rejected response）之间的边际。

### 现有方法的盲区：视觉编码器被忽视

尽管 RL 在 MLLM 中的应用日益增多，但已有研究几乎全部聚焦于 LLM 组件的优化。一个关键问题长期被忽视：**后训练阶段的训练目标如何影响视觉编码器的表征质量？** 传统的 SFT 训练仅通过最大化正确响应的概率来传递梯度信号，视觉编码器在此过程中是否得到了充分优化，尤其是在需要细粒度视觉理解的场景下，此前缺乏系统性研究。

这一盲区构成了一个潜在的瓶颈：如果视觉编码器在后训练中未得到有效优化，那么即使 LLM 组件再强大，MLLM 在视觉密集型任务上的表现也会受限于编码器提供的表征质量。

### 本文的核心动机与研究问题

本文旨在填补上述空白，系统性地探究 SFT 与 RL（以 DPO 为代表）在 MLLM 后训练中对视觉编码器的差异化影响。具体而言，研究围绕以下核心问题展开：

- DPO 是否在视觉相关的 VQA 任务上优于 SFT？这一优势是否随模型规模扩展而保持？
- DPO 训练后的视觉编码器，其纯视觉表征能力（如 ImageNet 线性探针、分割探针）是否强于 SFT 训练得到的编码器？
- 如果 DPO 确实产生了更强的视觉表征，其背后的机制是什么？梯度信号在两种训练目标下是否存在本质差异？
- 能否将 DPO 训练获得的增强型视觉编码器提取出来，作为即插即用的组件迁移到其他 MLLM 中？

基于对上述问题的探索，本文提出了 **PIVOT**（Preference-Instructed Vision OpTimization），一种利用 DPO 偏好对齐来增强视觉编码器的简单方案，旨在以极低的计算开销（约 18 小时、8 张 H100 GPU）获得可迁移的强视觉编码器。

## 核心方法与创新机理

### 问题瓶颈：视觉编码器在 SFT 下的表征退化

当前 MLLM 的标准训练范式采用两阶段策略：第一阶段通过大规模视觉-语言数据进行预训练以对齐视觉与语言表征，第二阶段通过监督微调（SFT）对模型进行指令适配。然而，该范式存在一个被忽视的关键瓶颈：**视觉编码器在 SFT 阶段并未得到充分优化**。SFT 仅最大化选定响应的似然，其梯度信号较为发散，无法有效驱动视觉编码器学习到精细的、问题相关的视觉特征。这导致视觉编码器在细粒度视觉理解任务（如 OCR、图表理解）上的潜力未被充分释放。

### 因果调控：从 SFT 到 DPO 的目标函数切换

本文的核心创新在于**将 MLLM 后训练阶段的目标函数从 SFT 替换为 DPO（Direct Preference Optimization）**，从而根本性地改变了视觉编码器所接收的梯度信号性质。具体而言：

- **SFT 损失**（仅优化选定响应）：
  $$L_{\mathrm{SFT}} = -\mathbb{E}_{i \sim X_{\mathrm{PT}}} \log \pi_{\theta}(y_i^c \mid I_i, q_i)$$

- **DPO 损失**（对比选定与拒绝响应）：
  $$L_{\mathrm{DPO}} = -\mathbb{E}_{i \sim X_{\mathrm{PT}}} \log \sigma\left(\beta\left(\log \frac{\pi_{\theta}(y_i^c \mid I_i, q_i)}{\pi_{\mathrm{ref}}(y_i^c \mid I_i, q_i)} - \log \frac{\pi_{\theta}(y_i^r \mid I_i, q_i)}{\pi_{\mathrm{ref}}(y_i^r \mid I_i, q_i)}\right)\right)$$

这一改变构成了论文唯一的 **changed slot**。DPO 的对比性质使得梯度信号高度集中于问题相关的视觉区域（Grad-CAM 可视化证实了这一点，见 Figure 7），从而迫使视觉编码器学习到更强、更局部化的特征表示。相比之下，SFT 的梯度在空间上更为发散，无法提供同等强度的定位信号。

### PIVOT：将 DPO 红利固化为可迁移的视觉编码器

基于上述发现，论文提出了 **PIVOT（Preference-Instructed Vision OpTimization）** 方法，其核心流程如下：

1. **DPO 后训练**：将视觉编码器与一个轻量 LLM（如 Qwen2.5-1.5B）配对，经过预训练后使用 DPO 在偏好数据上进行后训练。
2. **编码器提取**：将视觉编码器从 LLM 中分离，冻结其权重，得到一个 PIVOT 增强的视觉编码器。
3. **MLLM 重集成**：将该冻结编码器与新的 LLM 和投影器配对，仅对投影器和 LLM 进行下游微调。

这一设计的关键洞察在于：**DPO 训练所提升的视觉表征质量可以被“锁定”在视觉编码器中，并迁移到任意 MLLM 架构中**。实验表明，PIVOT 增强的 SigLIP1-So/14 在 VQA 平均得分上超越了参数规模更大的原始 SigLIP2-So/16（53.2% vs 52.4%），而增强后的 SigLIP2-So/16 甚至超越了 SigLIP2-g/16（55.6% vs 53.9%），且训练成本仅需 8 张 H100 GPU 上约 18 小时。

### 数据效率的质变

DPO 带来的不仅是性能提升，更是**数据效率的质变**。在数据规模消融实验中，仅使用 3K DPO 样本即可超越 40K SFT 样本的性能（60.4% vs 59.5%），且随着数据量增加，仅 DPO 训练的视觉表征持续改善，而 SFT 则趋于饱和。这表明 DPO 的对比损失提供了更高质量的训练信号，使得模型能从更少的样本中提取更多的视觉知识。

### 研究动机与核心发现

当前多模态大语言模型（MLLM）的标准训练范式通常包含预训练与监督微调（SFT）两个阶段。然而，本研究发现，在 SFT 范式下，视觉编码器并未得到充分优化，其视觉表示能力受限，尤其是在需要细粒度视觉理解的场景中。这一瓶颈的根本原因在于：SFT 仅最大化已选响应的似然，其梯度信号较为发散，无法有效驱动视觉编码器学习到问题相关的局部化特征。

相比之下，采用直接偏好优化（DPO）进行偏好对齐，能够通过对比损失提供更精细的梯度信号。DPO 的对比性质使梯度集中于问题相关的视觉区域，从而增强视觉编码器的定位与细节感知能力。基于这一核心洞察，作者提出了 **PIVOT**（Preference-Instructed Vision OpTimization）方法，将 DPO 训练后的视觉编码器提取并冻结，作为增强的视觉骨干重新集成至 MLLM 中。

### PIVOT 整体 Pipeline

PIVOT 的训练与部署流程可划分为四个串联模块，各模块间的输入输出关系如下：

#### 模块一：Stage 1 预训练（Pre-training）

遵循标准 MLLM 训练范式，将视觉编码器与大语言模型（LLM）通过多模态投影器连接，在多样化视觉-语言数据上进行全参数训练，以初步对齐视觉与语言表示。该阶段为后续偏好优化提供基础模型。

#### 模块二：Stage 2 DPO 后训练（DPO Post-training）

在预训练模型基础上，使用 DPO 损失进行偏好对齐。DPO 的核心机制是通过最大化已选响应与拒绝响应之间的对数概率边际，无需显式奖励模型即可实现偏好优化。其损失函数为：

$$L_{\mathrm{DPO}} = -\mathbb{E}_{i \sim X_{\mathrm{PT}}} \log \sigma\left(\beta\left(\log \frac{\pi_{\theta}(y_i^c \mid I_i, q_i)}{\pi_{\mathrm{ref}}(y_i^c \mid I_i, q_i)} - \log \frac{\pi_{\theta}(y_i^r \mid I_i, q_i)}{\pi_{\mathrm{ref}}(y_i^r \mid I_i, q_i)}\right)\right)$$

其中 $\pi_{\theta}$ 为当前策略模型，$\pi_{\mathrm{ref}}$ 为参考模型，$y_i^c$ 与 $y_i^r$ 分别为已选与拒绝响应，$\beta$ 为温度系数。该损失函数驱动视觉编码器学习到更强、更局部化的特征表示。

#### 模块三：视觉编码器提取（Vision Encoder Extraction）

DPO 后训练完成后，将视觉编码器从 LLM 头部解耦，并冻结其权重。此时的视觉编码器已通过 DPO 的对比梯度信号获得了增强的视觉表示能力，可作为独立的视觉骨干使用。

#### 模块四：MLLM 重集成（MLLM Reintegration）

将冻结的 PIVOT 增强编码器与新的 LLM 及投影器配对，在下游视觉-语言任务上进行投影器预训练与指令微调。由于视觉编码器权重已冻结，该阶段仅优化投影器与 LLM 参数，计算开销显著低于从头训练。

### 关键设计要点

| 设计要素 | 具体选择 | 依据 |
|---------|---------|------|
| 偏好对齐算法 | DPO | 对比性质使梯度集中于问题相关区域，优于 SFT 的发散梯度 |
| 视觉编码器处理 | 提取后冻结 | 保留 DPO 训练获得的增强表示，避免后续微调退化 |
| 投影器重集成策略 | 1 层冻结 + 1 层可训练 | 消融实验表明该配置效果最优（Table I） |
| 训练数据规模 | 20K DPO 样本 | 3K DPO 样本即可超越 40K SFT 样本，数据效率显著 |

### 适用范围与验证边界

PIVOT 的核心主张已在 LLaVA-OneVision 架构上，结合 Qwen2.5 系列 LLM 与 SigLIP2 视觉编码器得到验证。方法在多种视觉编码器（CLIP、DINOv2、MAE）上均表现出一致提升，但其在 InternVL、Qwen-VL 等其他 MLLM 框架以及 LLaMA 等 LLM 家族上的泛化性仍需进一步探索。此外，DPO 训练依赖特定的偏好数据集（MPO 子集），偏好数据质量与多样性对最终效果的影响尚未被系统研究。

### 核心模块：两阶段训练与视觉编码器优化

本研究采用标准的 MLLM 架构，将 LLM 与视觉编码器通过多模态投影器连接，基于 LLaVA-OneVision 框架实现，使用 Qwen2.5 作为语言模型、SigLIP2 作为视觉编码器。训练流程包含两个阶段：

**Stage 1：预训练。** 在多样化视觉语言数据上训练全部参数，实现视觉与语言表示的初步对齐。

**Stage 2：后训练（Post-training）。** 在预训练基础上，分别使用 SFT 或 DPO 进行进一步微调。两种策略共享相同的预训练基础，仅在第二阶段的优化目标上存在差异——SFT 最大化选择响应的似然，DPO 则通过偏好对进行对比式对齐。

**视觉编码器提取与评估。** 为分析后训练策略对视觉编码器本身的影响，研究者将视觉编码器从 LLM 头部解耦，冻结其权重，随后通过线性探针（ImageNet 分类）和分割探针（patch 级 MLP 分类器）评估其纯视觉表征质量。

**PIVOT 配方。** 基于上述分析，PIVOT 将 DPO 后训练后的视觉编码器冻结，与新的 LLM 和投影器重新配对，仅对投影器进行预训练和指令微调，从而将 DPO 增强的视觉表征迁移至下游 MLLM 任务。

---

### 关键公式推导

后训练阶段的两种损失函数构成了方法的核心对比：

**SFT 损失**（监督微调）：

$$L_{\mathrm{SFT}} = -\mathbb{E}_{i \sim X_{\mathrm{FT}}} \log \pi_{\theta}(y_i^c \mid I_i, q_i)$$

其中：
- $X_{\mathrm{FT}}$ 为后训练数据集
- $I_i$ 为输入图像，$q_i$ 为问题
- $y_i^c$ 为选择响应（chosen response）
- $\pi_{\theta}$ 为当前策略模型
- 该损失通过最小化负对数似然，使模型最大化生成选择响应的概率

**DPO 损失**（直接偏好优化）：

$$L_{\mathrm{DPO}} = -\mathbb{E}_{i \sim X_{\mathrm{FT}}} \log \sigma\left(\beta\left(\log \frac{\pi_{\theta}(y_i^c \mid I_i, q_i)}{\pi_{\mathrm{ref}}(y_i^c \mid I_i, q_i)} - \log \frac{\pi_{\theta}(y_i^r \mid I_i, q_i)}{\pi_{\mathrm{ref}}(y_i^r \mid I_i, q_i)}\right)\right)$$

其中：
- $y_i^r$ 为拒绝响应（rejected response）
- $\pi_{\mathrm{ref}}$ 为参考模型（通常为预训练后的冻结模型）
- $\beta$ 为温度系数，控制偏好边际的强度
- $\sigma$ 为 sigmoid 函数

DPO 损失的核心机制在于：无需显式训练奖励模型，直接通过最大化选择响应与拒绝响应之间的相对似然边际来实现偏好对齐。这种对比性质使梯度信号更集中于问题相关的视觉区域（如 Figure 7 中 Grad-CAM 可视化所示），从而驱动视觉编码器学习更强、更局部化的特征表示，这是 DPO 在视觉密集型任务上显著优于 SFT 的关键因果机制。

## 实验与关键发现

### 主结果：DPO 在视觉密集型 VQA 上的系统性优势

本研究在 LLaVA-OneVision 框架下，以 Qwen2.5 系列 LLM 与 SigLIP2 系列视觉编码器为基础，对 SFT 与 DPO 两种后训练策略进行了系统对比。评估覆盖 16 个 VQA 基准，分为 General、Knowledge、OCR & Chart、Vision-Centric 四类。

**视觉编码器缩放实验**（Figure 2）：固定 Qwen2.5-3B LLM，将 SigLIP2 视觉编码器从 B/16（86M）扩展到 g/16（1B）。DPO 在视觉密集型任务上始终显著优于 SFT。以 SigLIP2-L/16 为例，DPO 在 OCR & Chart VQA 上的优势达 **+4.2%p**，在 Vision-Centric VQA 上达 **+2.4%p**。相比之下，在 General VQA 和 Knowledge VQA 上，两者的差距明显缩小。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_3gM6HwHvnc/figures/006_Figure_2.jpg]]
*Figure 2: Scaling the vision encoder in MLLMs. We analyze the impact of the vision encoder sizes, ranging from 86M (B/16) to 1B (g/16) parameters, in Qwen2.5-3B combined with SigLIP2 on vision–language benchmarks. Interestingly, DPO yields particularly stronger gains over SFT in vision-intensive VQA*

**语言模型缩放实验**（Figure 3）：固定 SigLIP2-So/16 视觉编码器，将 LLM 从 0.5B 扩展到 7B。DPO 的优势随 LLM 增大而持续保持：使用 SigLIP2-g/16 时，DPO 在 OCR & Chart VQA 上领先 SFT **+3.1%p**，在 Vision-Centric VQA 上领先 **+4.2%p**。这一趋势表明，DPO 带来的视觉理解增益并非源于语言模型的补偿，而是视觉编码器本身的表征改善。

**数据效率实验**（Figure 4）：DPO 展现出惊人的数据效率。仅使用 **3K DPO 样本即可达到 60.4%p** 的平均得分，而 SFT 需要 **40K 样本才达到 59.5%p**。这意味着 DPO 用不到十分之一的数据量就超越了 SFT 的最佳表现。

### 视觉编码器独立评估：DPO 训练出更强的视觉表征

为排除 LLM 头部的干扰，研究者将 MLLM 后训练后的视觉编码器分离出来，进行纯视觉任务评估。

**ImageNet 线性探针**（Figure 6）：DPO 训练的视觉编码器在 ImageNet Top-1 准确率上一致优于 SFT。SigLIP2-So/16 搭配 Qwen-3B 时，DPO 比 SFT 高出 **+1.83%p**；SigLIP2-L/16 搭配 Qwen-1.5B 时，优势为 **+1.96%p**。更重要的是，Figure 5 显示，随着 DPO 训练数据量增加，视觉表征质量持续改善，而 SFT 下增加数据几乎不带来增益——这说明 DPO 的梯度信号对视觉编码器参数更新具有本质上的正向引导作用。

**分割探针实验**（Figure 8）：在 6 种视觉编码器（含 CLIP、SigLIP 等）上，DPO 训练的编码器在 patch 级分割召回率上均显著优于 SFT。以 CLIP-L/14 336px 为例，DPO 带来 **+1.08%p** 的召回率提升。Figure 9 的定性结果显示，DPO 训练的视觉编码器生成的分割图与真值标注更为一致，尤其在物体边界和细节区域。

### 核心机制：DPO 梯度信号的局部化特性

**梯度可视化**（Figure 7）：使用 Grad-CAM 对视觉编码器特征层进行梯度可视化，发现 DPO 的梯度信号高度集中于问题相关的视觉区域（如被问及的物体或文字），而 SFT 的梯度则较为发散，覆盖大量无关背景。这一差异解释了 DPO 为何能更有效地优化视觉编码器：对比损失函数迫使模型精确区分 chosen 与 rejected 响应之间的细微差异，这种“对比压力”转化为对视觉特征更具判别性的梯度更新。

**表征对齐分析**（Figure 10）：使用 Huh et al. 2024 的对齐度量，测量视觉编码器与多个参考 LLM 的表征对齐程度。DPO 训练的视觉编码器在所有 LLM 尺度下均展现出更高的对齐分数，且对齐分数随配对 LLM 规模增大而单调提升。这表明 DPO 不仅改善了视觉编码器的独立表征质量，还促进了视觉-语言表征空间的更好耦合。

### PIVOT 方法的有效性验证

基于上述发现，研究者提出 **PIVOT**：使用 DPO 对视觉编码器进行偏好引导优化，随后将其冻结并重新集成到 MLLM 中。

**跨模型泛化**（Table 1）：PIVOT 在多种视觉编码器上均带来一致提升。最引人注目的是，经过 PIVOT 增强的 **SigLIP1-So/14 超越原始 SigLIP2-So/16**（53.2%p vs 52.4%p），甚至接近更大的 SigLIP2-g/16（53.9%p）。PIVOT 增强的 SigLIP2-So/16 则达到 **55.6%p**，显著超过原始 SigLIP2-g/16 的 53.9%p。这一提升仅需在 8 张 H100 GPU 上训练约 18 小时，计算开销远低于从头预训练更大模型。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_3gM6HwHvnc/figures/024_Table_1.jpg]]
*Table 1: Influence of PIVOT on existing vision models. We apply PIVOT to reveal the potential for improving existing vision models for MLLMs. Following the setup in Section 3.1, vision model is trained with a Qwen2.5- 1.5B LLM-head on 3M samples, and then finetuned with either SFT (+ SFT) or DPO (+ PIVOT) on 20K data. ‘# samples seen’ refers number samples used for whole training as in Cherti et al. (2023); Zhai et al. (2023)*

**投影器设计消融**（Table I）：在 PIVOT 编码器重新集成阶段，采用“1 层冻结 + 1 层可训练”的投影器配置取得最优效果，验证了保留部分预训练对齐信息同时允许任务适配的设计合理性。

**训练策略消融**（Table K）：即使在全参数微调（而非仅训练投影器）的设置下，PIVOT 增强的编码器仍保持对原始编码器的优势，排除了“冻结编码器导致不公平比较”的疑虑。

### 失败模式与局限性

1. **架构泛化性未充分验证**：当前实验主要基于 LLaVA-OneVision + Qwen2.5 + SigLIP2 组合，对其他 MLLM 框架（如 InternVL、Qwen-VL）和 LLM 系列（如 LLaMA）的适用性尚待探索。

2. **偏好数据依赖性**：DPO 训练依赖特定的 MPO 子集作为偏好数据，数据质量和多样性对结果的影响未被系统研究。

3. **生成任务覆盖不足**：评估集中在 VQA 和感知任务，对图像描述、多轮对话等生成式多模态任务的效果仅部分覆盖（Table G），证据强度较弱。

4. **计算开销**：PIVOT 虽比完整预训练轻量，但仍需额外一轮 DPO 训练，对资源受限场景构成一定门槛。

5. **RL 算法选择局限**：本研究以 DPO 为核心，尽管 Table B/C/D 初步探索了 GRPO 和 PPO 的效果（GRPO 在 QwenVL-2.5-3B 上同样优于 SFT），但未对更广泛的 RL 算法族进行系统对比。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_3gM6HwHvnc/figures/025_Table_2.jpg]]
*Table 2: Table A: List of RL-based MLLM works. We provide an overview of methods with their venues, years, and RL optimization strategies, and note that most of the previous studies have adopted DPO (Rafailov et al. 2023) as one of their RL baselines*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_3gM6HwHvnc/figures/027_Table_4.jpg]]
*Table 4: Table B: Overview of GRPO- and PPO-based MLLM GitHub repository. We summarize open-source implementations for RL-based MLLM training, highlighting their main tasks, data and code availability, and encoder update strategies*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_3gM6HwHvnc/figures/028_Table_5.jpg]]
*Table 5: Table C: Evaluation of QwenVL-2.5-3B under GRPO vs. SFT post-training. We present results on MLLM benchmarks for MLLMs trained with different objectives (top). We also evaluate the vision encoder updated within MLLMs on vision-only benchmarks (bottom)*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_3gM6HwHvnc/figures/030_Table_7.jpg]]
*Table 7: Table D: Evaluation of LLaVA-1.0-7B under PPO vs. SFT post-training. We present results on MLLM benchmarks for MLLMs trained with different objectives (left). Table E: Evaluation of MLLMs under SFT, DPO, and MPO post-training. We present results on MLLM benchmarks for models trained with different post-training objectives (top). We further evaluate the updated vision encoder on vision-only benchmarks (middle), and finally assess the same encoder when re-integrated and evaluated within MLLMs (bottom)*

## 定位与知识库关联

### 核心工作与基线关系

本文提出的 **PIVOT (Preference-Instructed Vision OpTimization)** 本质上是一种面向多模态大语言模型视觉编码器的后训练增强方法，其核心创新在于将偏好对齐机制从语言生成端引入视觉表示学习端。

在方法谱系上，PIVOT 直接对比的基线是标准的 **SFT (Supervised Fine-Tuning)** 后训练范式。SFT 通过最大化选定响应的负对数似然来优化模型，是当前 MLLM 后训练的主流方法。PIVOT 将后训练目标替换为 **DPO (Direct Preference Optimization)**（Rafailov et al., NeurIPS 2023），利用偏好数据对（chosen/rejected pairs）提供的对比梯度信号来重塑视觉编码器的特征表示。这一替换构成了方法的核心因果调节旋钮。

在视觉编码器层面，PIVOT 的改造对象覆盖了当前主流的预训练视觉骨干网络，包括 **SigLIP**（Zhai et al., 2023）、**CLIP**（Radford et al., 2021）、**DINOv2** 和 **MAE** 等。实验表明，经过 PIVOT 增强的 SigLIP1-So/14 在 MLLM VQA 任务上的平均得分超越了原始的、参数量更大的 SigLIP2-So/16（53.2%p vs 52.4%p），证明了该方法在“以小博大”方面的有效性。

### 适用边界与局限

PIVOT 的验证边界目前存在以下约束：

1.  **架构依赖**：所有实验均基于 **LLaVA-OneVision** 架构，LLM 端固定使用 **Qwen2.5** 系列，视觉编码器以 **SigLIP2** 为主要验证对象。该方法在 InternVL、Qwen-VL 等其他 MLLM 框架以及 LLaMA 等 LLM 家族上的泛化性尚未得到验证，需要后续工作确认。

2.  **偏好数据敏感性**：DPO 训练依赖于特定的偏好数据集（MPO 子集），偏好数据的质量、多样性和构建策略对视觉表示学习的影响未被系统研究。不同偏好数据源可能导致视觉编码器学习到不同的特征偏差。

3.  **任务覆盖范围**：评估主要集中在 VQA 和感知类任务（General, Knowledge, OCR & Chart, Vision-Centric 四类共 16 个基准），对生成式多模态任务（如图像描述、多轮对话）的覆盖不够全面。

4.  **计算开销**：PIVOT 虽然比完整预训练轻量（约 18 小时 / 8×H100 GPU），但仍需额外增加一个 DPO 后训练阶段，相比直接使用预训练编码器存在额外的训练成本。

### 开放问题

基于本文的分析和发现，以下问题值得后续探索：

**RL 算法扩展**：DPO 的对比梯度机制被证明是视觉编码器提升的关键，但这一发现是否能推广到其他 RL 算法（如 GRPO、PPO）尚不明确。不同 RL 算法的梯度特性可能对视觉表示产生不同的塑造效果。

**偏好数据设计**：既然 DPO 的对比性质是关键，那么是否可以针对视觉表示学习专门设计偏好数据集？例如，通过构造细粒度视觉对比对来最大化视觉编码器的定位和细节感知能力，可能比通用偏好数据更有效。

**梯度局部化机制**：Grad-CAM 可视化显示 DPO 梯度更集中于问题相关区域，而 SFT 梯度较为发散（Figure 7），但这一现象的理论解释尚不充分。理解 DPO 损失函数的数学结构如何导致梯度局部化，可能为设计更优的视觉编码器训练目标提供理论指导。

**视觉任务泛化**：PIVOT 在分割探针任务上展示了召回率提升（CLIP-L/14 +1.08%p），但其在目标检测、实例分割等更复杂的视觉任务上的表现尚未验证。视觉编码器的特征改进是否能直接转化为这些任务的下游收益，需要进一步实验。

**预训练阶段整合**：当前 PIVOT 是后训练阶段的增强方案，若能将其核心机制（偏好对比信号）整合到视觉编码器的预训练阶段，可能从根本上改变视觉表示的学习方式，而非仅仅进行后验修正。

**跨架构验证**：PIVOT 的有效性是否依赖于特定的投影器设计（如 LLaVA 的线性投影层）？在跨注意力融合、Q-Former 等其他多模态连接方式下，视觉编码器的 DPO 梯度信号是否仍能保持局部化优势，需要进一步确认。

**LLM 头的选择影响**：实验显示更大的 LLM 头能带来更强的视觉表示对齐（Figure 10），但 LLM 的架构选择（如不同规模的 Qwen2.5）对 PIVOT 增强效果的具体影响机制尚不清晰。是否存在最优的 LLM 头配置以最大化视觉编码器的提升，是一个值得研究的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/RL_makes_MLLMs_see_better_than_SFT.pdf]]

---
title: ChroAccRet Chronologically Accurate Retrieval for Temporal Grounding of Motion Language Models
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models.pdf
project_link: null
code_link: null
aliases:
- CARTCL
- CCARTGMLM
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在对比学习过程中，将经LLM分解并随机打乱事件顺序的文本作为额外负样本（hard negative），强制模型学习区分时序正确与错误的描述。
primary_logic: 通过向对比学习框架注入时序顺序信息（即打乱的事件描述作为负样本），可以显著增强模型对动作时序的理解能力，从而在保持常规检索性能的同时，大幅提升时序准确率，并改善下游运动生成质量。
claims:
- 主流运动-语言模型在Chronologically Accurate Retrieval（CAR）测试中准确率仅约60%，接近随机水平（50%），表明其缺乏时序理解。
- 引入打乱事件文本作为负样本后，所有模型变体的CAR准确率均提升至90%以上，最高达到99.74%。
- 所提训练方案在运动-文本检索（包含打乱文本）中同样有效，R@1指标显著提高，例如t5-large从7.76提升至9.65。
- HumanML3D test set (2,677 multi-event sequences) 上 CAR accuracy ('orig→event') = 99.74 (Ours t5-base/t5-large)
---

# ChroAccRet Chronologically Accurate Retrieval for Temporal Grounding of Motion Language Models

> [!tip] 核心洞察
> 通过向对比学习框架注入时序顺序信息（即打乱的事件描述作为负样本），可以显著增强模型对动作时序的理解能力，从而在保持常规检索性能的同时，大幅提升时序准确率，并改善下游运动生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向运动语言模型时序对齐的时序准确检索方法 |
| 英文题名 | ChroAccRet Chronologically Accurate Retrieval for Temporal Grounding of Motion Language Models |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 基于时序打乱负样本的对比学习训练（Chronologically Accurate Retrieval and Temporal Contrastive Learning） |
| Dataset | HumanML3D test set |

> [!tip] 效果简介
> - HumanML3D test set (2,677 multi-event sequences) 上，CAR accuracy ('orig→event') 99.74 (Ours t5-base/t5-large) vs 66.42 (TMR t5-base) / 66.72 (TMR t5-large) (+33.32%/33.02%)。
> - HumanML3D test set (all sequences, text-to-motion retrieval) 上，R@1 (All) ↑ 8.03 (Ours t5-large, Tune, no VAE, Rec.) vs 5.82 (TMR DistilBERT) (+2.21)。
> - HumanML3D test set (motion generation with T2M-GPT) 上，R-Precision Top-1 ↑ 0.528±.004 (T2M-GPT + CLIP tuned with Neg.) vs 0.489±.004 (T2M-GPT original) (+0.039)。

## 概要

本文揭示并解决了一个被现有运动-语言模型忽视的关键问题：**时序理解缺失**。主流模型（如 **TMR**，Petrovich et al., ICCV 2023）在对比学习中将文本与动作映射到共享潜在空间时，仅依赖全局语义相似度，未显式建模文本中事件顺序与动作序列之间的时序对应关系。这导致模型对复合动作描述（如“先坐下，然后站起来，最后挥手”）的事件顺序理解严重不足。

为量化这一问题，作者提出了 **Chronologically Accurate Retrieval（CAR）** 测试：利用 GPT-3.5 将复合动作描述分解为原子事件，随机打乱事件顺序生成时序错误的描述，然后检验模型能否正确区分原始描述与打乱描述。在 HumanML3D 测试集的 2,677 个多事件序列上，TMR 的 CAR 准确率仅约 60%，接近随机水平（50%），证实了时序理解的结构性缺陷。

**核心洞察**：将打乱事件顺序的文本作为额外负样本（hard negative）注入对比学习框架，可以强制模型学习区分时序正确与错误的描述，从而显著增强时序理解能力。

**方法定位**：该方法属于**训练范式改进**，不改变模型架构，仅修改对比学习中的负样本构造与损失函数设计。具体而言，在原有 N×N 相似矩阵基础上，为每个运动样本增加 K 个打乱文本作为负样本，形成 N×(N+K) 扩展相似矩阵，并相应调整行/列方向的交叉熵损失。

**主要结果**：
- **CAR 准确率**：引入时序负样本后，所有模型变体的 CAR 准确率均从约 60% 提升至 90% 以上，最高达 99.74%（t5-base/t5-large）。
- **检索性能**：运动-文本检索的 R@1 指标同步提升，例如 t5-large 从 7.76 提升至 9.65。
- **生成质量**：微调后的文本编码器在多个生成模型（**Motiondiffuse**、**T2M-GPT**、**ReMoDiffuse**）上一致改善 FID 和 R-Precision，证明该方法具有通用性。



### 运动-语言模型的时序理解缺口

文本-运动检索与生成任务近年来取得了显著进展，以 **TMR**（Petrovich et al., ICCV 2023）为代表的运动-语言模型通过对比学习框架，将文本描述与3D人体运动序列映射到共享潜在空间，实现了跨模态检索与条件生成。然而，现有模型存在一个关键盲区：**对比学习目标仅关注文本与运动的整体语义匹配，未显式建模二者之间的时序对应关系**。当面对包含多个连续子动作的复合描述（如“先蹲下再起立然后跳跃”）时，模型无法有效区分事件发生的先后顺序。

这一缺陷在本文提出的 **Chronologically Accurate Retrieval (CAR)** 测试中得到了量化验证。CAR测试要求模型从原始描述与打乱事件顺序的干扰文本中正确选出与运动序列匹配的描述。实验表明，主流模型的CAR准确率仅约60%（TMR t5-large 为 66.72%），接近随机猜测水平（50%），证实了时序理解能力的严重不足（Table 1, 置信度 0.95）。

### 现有方法的局限性

传统对比学习的负样本构造策略是造成这一问题的结构性质因。以TMR为代表的方法仅使用批次内其他文本-运动对作为负样本（N路对比），这些负样本在时序结构上与正样本的差异是随机且不可控的。模型因此倾向于依赖整体语义相似度进行匹配，而忽略了对事件顺序的精细建模。此外，现有模型将整句文本压缩为单一特征向量，缺乏单词到运动帧的细粒度对应机制，无法解释每个事件在时间轴上的精确位置（论文局限性分析）。

### 核心动机与研究思路

本文的核心洞察是：**通过向对比学习框架中注入显式的时序顺序信息，可以迫使模型学习区分时序正确与错误的描述，从而在保持常规检索性能的同时大幅提升时序准确率**。具体而言，方法利用GPT-3.5将复合动作描述分解为原子事件，随机打乱事件顺序后生成时序错误的描述，并将其作为额外负样本（hard negative）加入对比学习过程。这一设计将原始的 $N \times N$ 相似矩阵扩展为 $N \times (N+K)$，使动作到文本的分类任务必须从包含打乱描述的候选集中选出正确文本，从而强制模型关注事件时序（Fig. 3, Eq. 4-5, 置信度 0.95）。

该方法不仅解决了时序对齐问题，还展现出良好的通用性：经过时序负样本微调的文本编码器可直接提升下游运动生成模型（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**Motiondiffuse** (Zhang et al., arXiv 2022)、**ReMoDiffuse** (Zhang et al., ICCV 2023)）的生成质量，为运动-语言模型的时序感知训练提供了简洁有效的范式。



## 核心方法与创新机理

### 问题诊断：运动-语言模型缺乏时序理解

现有运动-语言对比学习模型（如 **TMR**，Petrovich et al., ICCV 2023）在训练时仅将同一批次内的其他文本-动作对作为负样本，未显式建模文本描述中事件发生的先后顺序。这导致模型对复合动作描述的时序理解严重不足。论文提出的 **Chronologically Accurate Retrieval（CAR）** 测试揭示了这一瓶颈：在 HumanML3D 测试集的 2,677 个多事件序列上，TMR 搭配不同文本编码器（DistilBERT / CLIP / t5-base / t5-large）的 CAR 准确率仅为 64.81% / 63.17% / 66.42% / 66.72%，仅略高于随机水平（50%），表明模型几乎不具备区分“先坐下后站起”与“先站起后坐下”的能力（Table 1）。

### 核心创新：时序打乱负样本注入对比学习

针对上述瓶颈，论文提出一种简洁而高效的训练策略——**将经 LLM 分解并随机打乱事件顺序的文本作为额外负样本（hard negative），注入对比学习框架**。该方法由两个关键 changed slot 构成：

**Changed Slot 1：负样本构造方式**

- **Baseline 做法**：仅使用同一批次内其他 $N$ 个文本-动作对作为负样本，形成 $N \times N$ 的余弦相似度矩阵 $\mathbf{S}$，通过对称交叉熵损失进行对比学习。
- **Proposed 做法**：对每个包含多个事件的文本，先利用 GPT-3.5 将其分解为原子事件，再随机打乱事件顺序并重新拼接，生成 $K$ 个时序错误描述。这些打乱文本作为该动作的额外负样本，将相似度矩阵扩展为 $\tilde{\mathbf{S}} \in \mathbb{R}^{N \times (N+K)}$（Fig. 3, Section 4.1）。

**Changed Slot 2：对比损失函数的非对称扩展**

- **Baseline 做法**：基于 $N \times N$ 相似矩阵的对称交叉熵损失（Eq. 1）：
  $$\mathcal{L} = -\frac{1}{2N} \sum_i \left( \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ij}/\tau} + \log \frac{\exp S_{ii}/\tau}{\sum_j \exp S_{ji}/\tau} \right)$$
- **Proposed 做法**：将损失拆分为非对称的两部分（Eq. 3-5）：
  - **文本→动作损失** $\mathcal{L}_{t2m}$：行方向仍为 $N$ 分类，仅对 $N$ 个原始文本计算交叉熵（Eq. 4）；
  - **动作→文本损失** $\mathcal{L}_{m2t}$：列方向扩展为 $N+K$ 分类，迫使动作特征从 $N+K$ 个候选文本（包含打乱负样本）中识别正确描述（Eq. 5）：
    $$\mathcal{L}_{m2t} = -\frac{1}{N} \sum_i^{N} \log \frac{\exp \tilde{S}_{ii} / \tau}{\sum_j^{(N+K)} \exp \tilde{S}_{ji} / \tau}$$

这种非对称设计的关键在于：打乱文本仅作为动作→文本方向的负样本参与对比，而不在文本→动作方向产生损失，从而避免对文本编码器引入混淆信号。

### 因果机制与效果验证

该方法的因果逻辑链条清晰：**注入时序顺序信息（打乱事件作为负样本）→ 强制模型学习区分时序正确与错误的描述 → 增强动作-文本间的时序对齐 → 提升 CAR 准确率与下游生成质量**。

决定性证据来自 Table 1：引入打乱负样本训练后，所有模型变体的 CAR 准确率均跃升至 99% 以上（DistilBERT 99.33%，CLIP 98.88%，t5-base/t5-large 均达 99.74%），较基线提升超 33 个百分点。同时，运动→文本检索的 R@1 指标也显著提高（如 t5-large 从 7.76 提升至 9.65），证明时序负样本不仅增强了时序判别力，还改善了整体表示质量。

### 方法边界与遗留问题

尽管效果显著，该方法仍存在以下局限：

1. **表层语言线索依赖**：消融实验表明，统一冠词后 CAR 仅微降至 94.51%，但替换代词后 CAR 降至 81.21%，说明模型可能部分依赖代词、冠词等表层特征而非深层时序语义进行判断。
2. **粗粒度时序建模**：模型仍将整句压缩为单一特征向量，缺乏单词到运动帧的细粒度对应，无法解释每个事件在时间轴上的精确位置。
3. **单向时序增强**：当前仅通过操纵文本（打乱事件）增强时序理解，尚未对运动序列本身进行对称的时序增强（如交换动作片段顺序），限制了模型在动作层面的时序泛化能力。



ChroAccRet 的核心 pipeline 围绕一个关键观察展开：现有运动‑语言模型（如 **TMR**, Petrovich et al., ICCV 2023）在对比学习中未显式建模文本与动作之间的时序对应关系，导致其对复合动作描述的事件顺序理解严重不足——在 Chronologically Accurate Retrieval (CAR) 测试中准确率仅约 60%，接近随机水平（50%）。为修复这一瓶颈，该方法在不改变原有模型架构的前提下，向对比学习框架注入时序顺序信息，从而强制模型学习区分时序正确与时序错误的描述。

### 数据流与模块关系

整个框架由以下模块串联构成：

1. **事件分解与打乱模块（离线预处理）**  
   利用 GPT‑3.5 将数据集中包含多个事件的复合动作描述分解为原子事件列表，随后随机打乱事件顺序并重新拼接，生成时序错误的文本描述。这些打乱文本作为后续训练的“硬负样本”（hard negative samples）。该流程仅在训练前执行一次，不参与在线推理。

2. **文本编码器**  
   将原始描述文本与打乱后的负样本文本分别映射为潜在特征向量。论文支持多种语言骨干网络，包括 DistilBERT、CLIP、t5‑base 和 t5‑large，以验证方法的通用性。

3. **运动编码器**  
   将 3D 骨架运动序列（基于相对关节位置与加速度）编码为潜在特征向量。该编码器沿用 TMR 的 VAE 结构，但在部分消融实验中可选择禁用 VAE 的随机性以提升时序区分能力。

4. **对比相似性计算与扩展损失函数**  
   这是方法的核心改造点。传统 TMR 仅计算批次内 N 个文本‑动作对的 N×N 余弦相似矩阵 S，并施加对称交叉熵损失。ChroAccRet 在此基础上，为每个运动额外引入 K 个打乱事件文本作为负样本，将相似矩阵扩展为 N×(N+K) 的矩阵 S̃。  
   损失函数随之调整为非对称形式：
   - **文本→动作损失**（Eq. 4）仅在行方向对 N 个原始文本执行 N 分类，排除打乱文本对应的行损失；
   - **动作→文本损失**（Eq. 5）在列方向将候选集扩展为 N+K 个文本，要求模型从包含时序错误选项的更大池中正确匹配原始描述。  
   总损失为两者之和（Eq. 3）。

5. **运动解码器（可选）**  
   从运动潜在特征重建原始运动序列，作为辅助训练目标。消融实验表明，保留解码器有助于维持常规检索性能，但对时序准确率的提升并非必需。

### 输入输出规范

- **训练阶段输入**：原始文本‑运动对 $(T_i, M_i)$ 及其对应的 K 个打乱事件文本 $\{C_i^{(1)}, \dots, C_i^{(K)}\}$。  
- **训练阶段输出**：优化后的文本编码器与运动编码器，使正样本对相似度高于所有负样本（包括打乱文本）。  
- **推理阶段输入**：单个文本查询或运动序列。  
- **推理阶段输出**：文本‑运动相似度分数，用于检索排序或作为下游运动生成模型的文本条件特征。

### 与基线的关键差异

| 模块/策略 | TMR 基线 | ChroAccRet 方案 |
|-----------|----------|-----------------|
| 负样本构造 | 仅批次内其他对作为负样本（N 路对比） | 额外增加 K 个打乱事件文本作为硬负样本，形成 N×(N+K) 对比矩阵 |
| 对比损失 | 对称交叉熵损失（Eq. 1） | 非对称损失：文本→动作为 N 分类，动作→文本为 N+K 分类（Eq. 4–5） |
| 时序监督 | 无显式时序信号 | 通过打乱事件顺序注入强时序监督 |

该框架的设计哲学是“最小侵入”：不改变编码器架构，仅通过扩展负样本空间和调整损失函数，即可将 CAR 准确率从约 66% 提升至 99.74%（t5‑base/t5‑large），同时保持甚至提升常规文本‑运动检索指标。

### 补充图表

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed contrastive learning scheme with chronological negative samples. We use the texts derived from shuffling the event order and employ them as negative text samples, corresponding to items indicated in pink*



### 3.1 运动-语言对比学习基线

本文以 **TMR**（Petrovich et al., ICCV 2023）的对比学习框架为基础。给定一批包含 $N$ 个运动-文本对的样本，文本编码器将描述映射为潜在特征 $z^T$，运动编码器将3D骨架序列映射为潜在特征 $z^M$。计算所有组合的余弦相似度，构成 $N \times N$ 的相似矩阵 $\mathbf{S}$：

$$S_{ij} = f(z_i^T, z_j^M)$$

其中 $f(\cdot,\cdot)$ 为余弦相似度函数。TMR采用对称交叉熵损失进行优化：

$$\mathcal{L} = -\frac{1}{2N} \sum_i \left( \log \frac{\exp (S_{ii}/\tau)}{\sum_j \exp (S_{ij}/\tau)} + \log \frac{\exp (S_{ii}/\tau)}{\sum_j \exp (S_{ji}/\tau)} \right) \tag{1}$$

其中 $\tau$ 为温度参数。该损失强制正样本对（对角线元素 $S_{ii}$）的相似度高于同一批次内其他所有负样本对。

**瓶颈**：该框架仅将整句文本压缩为单一全局特征进行对比，未显式建模文本内部事件与运动片段之间的时序对应关系，导致模型对复合动作描述的事件顺序理解不足。

### 3.2 事件分解与时序打乱模块

为构造时序错误的负样本，本文引入基于大语言模型的事件分解流水线：

1. **事件分解**：利用 GPT-3.5 将复合动作描述分解为原子事件序列。例如，描述 `"a person walks forward, then turns right and sits down"` 被分解为 `["a person walks forward", "a person turns right", "a person sits down"]`。
2. **时序打乱**：对分解后的事件进行随机排列，重新拼接生成时序错误的描述，如 `"a person sits down, a person walks forward, then turns right"`。
3. **负样本筛选**：仅对包含多于一个事件的文本（HumanML3D测试集中共2,677条）执行此操作，单事件描述不产生打乱版本。

### 3.3 时序准确检索评估指标

为量化模型的时序理解能力，定义 Chronologically Accurate Retrieval（CAR）准确率：

$$CAR = \frac{1}{K} \sum_{i}^{K} g\left( f(z_i^T, z_i^M),\; f(z_i^C, z_i^M) \right) \tag{2}$$

其中 $z_i^T$ 为原始文本特征，$z_i^C$ 为打乱事件顺序后的文本特征，$z_i^M$ 为对应运动特征。函数 $g(a,b)$ 在 $a > b$ 时返回1，否则返回0。CAR衡量模型将原始文本排在打乱文本之前的样本比例，随机水平为50%。

### 3.4 时序对比损失

核心改进在于将打乱事件描述作为额外的困难负样本注入对比学习过程。对于批次中的 $N$ 个运动-文本对，额外构造 $K$ 个打乱文本（$K \leq N$），形成扩展的相似矩阵 $\tilde{\mathbf{S}} \in \mathbb{R}^{N \times (N+K)}$。

总损失由两部分组成：

$$\mathcal{L} = \mathcal{L}_{t2m} + \mathcal{L}_{m2t} \tag{3}$$

**文本→运动损失**（行方向分类）：仅对 $N$ 个原始文本计算，每个文本需从 $N$ 个运动中识别其正样本：

$$\mathcal{L}_{t2m} = -\frac{1}{N} \sum_i^{N} \log \frac{\exp (\tilde{S}_{ii} / \tau)}{\sum_j^{N} \exp (\tilde{S}_{ij} / \tau)} \tag{4}$$

**运动→文本损失**（列方向分类）：每个运动需从 $N+K$ 个文本候选中识别其正样本（原始文本），打乱文本对应的列作为额外负样本参与分母归一化：

$$\mathcal{L}_{m2t} = -\frac{1}{N} \sum_i^{N} \log \frac{\exp (\tilde{S}_{ii} / \tau)}{\sum_j^{(N+K)} \exp (\tilde{S}_{ji} / \tau)} \tag{5}$$

**设计意图**：$\mathcal{L}_{m2t}$ 的列方向扩展使得每个运动在检索文本时，必须将打乱文本的相似度压低至原始文本之下，从而强制模型学习区分时序正确与错误的描述。$\mathcal{L}_{t2m}$ 保持行方向 $N$ 分类，避免打乱文本作为查询时引入噪声。

### 3.5 模块交互关系

整个训练流水线中，文本编码器（支持 DistilBERT、CLIP、t5-base、t5-large）和运动编码器（基于VAE，输入为相对关节位置和加速度）共享潜在空间。事件分解与打乱模块在数据预处理阶段离线完成，生成的打乱文本在训练时作为额外负样本参与对比损失计算。运动解码器可选择性用于从潜在特征重建原始运动序列，作为辅助正则化项。



## 实验与关键发现

### 核心发现：时序理解是现有模型的系统性盲区

论文首先通过**Chronologically Accurate Retrieval (CAR)** 测试暴露了问题的严重性。CAR 测试将原始动作描述经 GPT-3.5 分解为原子事件后随机打乱重排，形成时序错误的描述，然后检验模型能否正确区分原始文本与打乱文本。在 HumanML3D 测试集 2,677 个多事件序列上，基线模型 **TMR** (Petrovich et al., ICCV 2023) 搭配不同文本编码器的 CAR 准确率仅在 63%–67% 之间（Table 1），仅略高于随机猜测水平（50%）。这一结果直接证实：主流运动-语言模型在对比学习过程中**未显式建模文本与动作间的时序对应关系**，导致对复合动作描述的事件顺序理解严重不足。

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/004_Table_1.jpg]]
*Table 1: Comparison of CAR accuracy and motion-to-text retrieval results with both the original and corrupted texts. We insert chronologically inaccurate texts as candidates for retrieval. Ours indicate models trained with the hard negative samples*

### 主实验结果：时序负样本训练带来质的飞跃

#### CAR 准确率跃升

引入打乱事件文本作为额外负样本后，所有模型变体的 CAR 准确率均提升至 90% 以上，最高达到 **99.74%**（t5-base/t5-large，Table 1）。与基线相比，t5-base 从 66.42% 提升至 99.74%（+33.32%），t5-large 从 66.72% 提升至 99.74%（+33.02%）。这一量级的提升表明，**向对比学习框架注入时序顺序信息**（即打乱事件描述作为 hard negative）能够从根本上重塑模型的时序判别能力，而非仅带来边际改善。

#### 常规检索性能同步提升

时序负样本训练不仅在 CAR 上有效，在包含打乱文本的扩展检索任务中同样显著提升了标准检索指标。以 motion-to-text retrieval 的 R@1 为例（Table 1），t5-large 从 7.76 提升至 9.65，t5-base 从 8.22 提升至 9.64。这说明模型学到的时序区分能力**并未以牺牲常规检索性能为代价**，反而通过更精细的语义-运动对齐带来了整体提升。

#### 下游运动生成质量改善

将经负样本微调的文本编码器接入运动生成模型后，生成质量得到一致改善（Table 3）。以 **T2M-GPT** (Zhang et al., CVPR 2023) 为例，使用 CLIP 编码器并经负样本微调后，R-Precision Top-1 从 0.489±.004 提升至 0.528±.004，FID 从 0.116±.005 降至 0.074±.012（Table 4）。类似提升在 **Motiondiffuse** (Zhang et al., arXiv 2022) 和 **ReMoDiffuse** (Zhang et al., ICCV 2023) 上同样观察到，证明负样本训练方案具有**跨生成模型的通用性**。

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/007_Table_3.jpg]]
*Table 3: Comparison of performance of motion generation models and their variants. “Tune” indicates CLIP text encoders fine-tuned from text-motion retrieval tasks. “Neg” indicates the usage of negative chronological samples in contrastive learning*

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/008_Table_4.jpg]]
*Table 4: Comparison of performance of motion generation with different language models using T2M-GPT as the base model. “Tune” indicates fine-tuning language models through backpropagating TMR, and “Neg” indicates using negative chronological samples. Note that the original T2M-GPT relies on CLIP encoder for the initial token*

### 消融实验：关键设计选择的影响

#### VAE 随机性对时序学习的负面影响

Table 2 的消融实验揭示了几个重要规律。当微调语言模型（Tune）并禁用 VAE 文本编码器（no VAE）时，时序区分能力提升最为显著。例如，DistilBERT 配置下，Tune + no VAE + Rec. 的 R@1 达到 6.55，而原始 TMR 仅 5.82。这表明 **VAE 引入的随机性会干扰时序信息的编码**，去除该随机性后模型能更稳定地学习事件顺序。

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/005_Table_2.jpg]]
*Table 2: Comparison of retrieval results between the original TMR model and its variations equipped with different language encoders, which are further fine-tuned with our chronological negative samples. “Tune” indicates whether the language model is fine-tuned, “VAE” whether VAE feature is used, and “Rec.” whether motion decoder is used to reconstruct the original poses*

#### 负样本的必要性

Table 4 进一步分离了微调与负样本的贡献。仅微调 CLIP 编码器（Tune）可使 FID 从 0.116±.005 降至 0.088±.006，但加入负样本（Tune+Neg）后进一步降至 0.070±.006。类似地，DistilBERT 经负样本微调后 FID 达到 0.074±.012。这验证了**时序负样本的独立贡献**：微调本身改善了文本-运动对齐，但只有显式注入时序顺序信号才能让模型真正理解事件的时间关系。

### 失败模式与局限性

论文明确指出了方法的几个边界条件：

1. **表层语言线索的干扰**：代词和冠词可能提供隐含的时序线索。消融实验表明，统一冠词后 CAR 仅微降至 94.51%，但替换代词后 CAR 降至 81.21%，说明模型可能部分依赖这些表层特征而非真正的时序理解。这一发现提示 CAR 测试的纯净度需要进一步审视。

2. **细粒度时序对应的缺失**：当前方法仍将整句压缩为单一特征向量，**缺乏单词到运动帧的细粒度对应**，无法解释每个事件在时间轴上的精确位置。这限制了模型在需要精确定位（如“先举手再转身”）场景中的应用。

3. **动作层面的时序增强尚未探索**：当前方法仅通过操纵文本（打乱事件）来增强时序理解，**尚未对运动序列本身进行类似的时序增强**（如交换动作片段顺序），限制了模型在动作层面的时序泛化能力。

### 关键图表结论总结

- **Table 1** 是本文最重要的实验证据，同时展示了问题的严重性（基线 CAR ≈ 60%）和方案的有效性（CAR → 99%+），是支撑核心主张的决定性数据。
- **Table 2** 揭示了 VAE 随机性对时序学习的负面影响，为后续方法设计提供了重要指导：时序敏感任务中应谨慎使用随机编码器。
- **Table 3/4** 证明了负样本训练方案对下游生成任务的通用提升效果，表明时序理解能力的增强可以无缝迁移至生成管线。

> **注意**：论文未涉及模型公平性或偏见相关的评估，因此无法就方法在不同人群或动作类型上的表现差异做出判断。

### 补充图表

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/006_Figure_4.jpg]]
*Figure 4: Comparison of retrieval results with corrupted texts using TMR and the proposed training scheme. Pink texts indicate the successfully retrieved ground truth text*

![[assets/figures/papers/paper_list_l1871_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of/figures/009_Figure_5.jpg]]
*Figure 5: Comparison of generated motions. Top: T2M-GPT. Bottom: T2M-GPT with our fine-tuned t5-large encoder. Texts at the top represent the input prompts*



## 定位与知识库关联

### 1. 与基线工作的关系

本工作建立在文本-运动检索基线 **TMR**（Petrovich et al., ICCV 2023）的对比学习框架之上。TMR 采用对称交叉熵损失（Eq. 1），在 N×N 余弦相似矩阵上进行双向分类，但未显式建模文本与动作间的时序对应关系。本文的核心改动在于**负样本构造**和**损失函数扩展**两个维度：

- **负样本构造**：基线仅使用同一批次内的其他文本-动作对作为负样本（N路对比）；本文额外引入 K 个通过打乱事件顺序生成的时序错误描述作为 hard negative，将相似矩阵从 N×N 扩展为 N×(N+K)。
- **损失函数**：文本→动作损失保持行方向 N 分类，动作→文本损失扩展为列方向 (N+K) 分类，但排除打乱文本对应的列损失（Eq. 4-5），形成非对称的时序对比监督。

在运动生成任务上，本文的微调编码器被应用于三个代表性生成基线：**Motiondiffuse**（Zhang et al., arXiv 2022）、**T2M-GPT**（Zhang et al., CVPR 2023）和 **ReMoDiffuse**（Zhang et al., ICCV 2023）。实验表明，结合负样本微调的文本编码器在这些生成模型上一致提升 R-Precision 和 FID 指标（Table 3-4），证明该方法与主流生成框架具有良好的即插即用兼容性。

### 2. 方法适用边界

**正向适用条件**：
- 文本描述包含两个及以上可分解的原子事件（复合动作描述），单事件描述无法构造打乱负样本。
- 运动序列具有明确的时间先后顺序，事件间的因果或时序依赖关系较强。
- 下游任务依赖文本-动作间的全局时序理解，如时序敏感检索、按顺序执行的动作生成。

**不适用或效果受限场景**：
- 仅包含单一原子动作的短描述（无法触发事件分解与打乱机制）。
- 事件间无严格时序约束的并行或对称动作（打乱后语义仍合理，负样本区分度低）。
- 依赖细粒度帧级对齐的任务（如动作时序定位），因为模型仍将整句压缩为单一特征，缺乏单词到运动帧的对应。

### 3. 局限性与已知失效模式

1. **表层语言特征泄露**：消融实验表明，代词和冠词可能提供隐含的时序线索。统一冠词后 CAR 仅微降至 94.51%，但替换代词后 CAR 降至 81.21%，说明模型可能部分依赖这些表层特征而非深层时序语义进行判断。

2. **缺乏细粒度时序对应**：模型将整句压缩为单一特征向量，无法解释每个事件在时间轴上的精确位置，限制了在需要帧级对齐的下游任务（如动作时序定位）中的应用。

3. **单向时序增强**：当前方法仅通过操纵文本（打乱事件顺序）来增强时序理解，尚未对运动序列本身进行类似的时序增强（如交换动作片段顺序），限制了模型在动作层面的时序泛化能力。

4. **事件分解质量依赖**：CAR 测试的可靠性依赖于 GPT-3.5 的事件分解质量。分解错误（如遗漏事件、错误切分）会直接影响负样本质量和评估有效性，且缺乏不依赖 LLM 的自动化时序基准。

### 4. 开放问题

- **细粒度时序对齐**：如何建立文本单词与运动帧之间的显式对应，实现可解释的事件级时序定位？
- **对称时序增强**：如何设计运动序列的时序数据增强（如片段重排），与文本负样本形成对称的强时序监督，提升双向时序理解？
- **评估基准独立性**：能否设计不依赖 LLM 的自动化时序评估基准，消除事件分解质量对 CAR 测试可靠性的影响？
- **长序列扩展性**：对于更长、更复杂的动作序列，当前方法能否保持高时序准确率？是否需要层次化的时序建模（如事件组、子序列）？
- **跨模态时序泛化**：该方法学到的时序区分能力是否可迁移到其他时序敏感的跨模态任务（如视频-文本检索、过程理解）？



## 原文 PDF

![[paperPDFs/ECCV_2024/ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models.pdf]]

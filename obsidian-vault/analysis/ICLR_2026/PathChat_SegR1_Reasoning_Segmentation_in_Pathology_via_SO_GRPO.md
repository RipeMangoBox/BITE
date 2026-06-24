---
title: "PathChat-SegR1: Reasoning Segmentation in Pathology via SO-GRPO"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PathChat_SegR1_Reasoning_Segmentation_in_Pathology_via_SO_GRPO.pdf
openreview_forum_id: DQESI75YrD
aliases:
- PS
- PathChat-SegR1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "LLM在推理过程中生成<SEG> token的时机，决定了分割触发时视觉特征、推理上下文和空间信息的对齐程度。"
primary_logic: "通过引入GAE对LLM推理每一步分配优势值，结合可微分割性能奖励和稀疏性奖励，使模型能够在累积足够语义上下文时自主生成<SEG> token，从而在病理学零样本分割中实现显著提升。"
claims:
- "在PMBT零样本评估中，PathChat-SegR1相比最佳基线MMR-7B提升了61%（0.58 vs 0.36 Dice）。"
- "消融实验表明，移除RL阶段导致0.18 Dice性能下降，移除Ruipath编码器导致0.16 Dice下降，证实了核心模块的重要性。"
- "SO-GRPO相比标准GRPO提升了0.05 Dice（0.58 vs 0.53），并将收敛步骤从24K减少到18K。"
- "PMBT (zero-shot) 上 Dice = 0.58"
---

# PathChat-SegR1: Reasoning Segmentation in Pathology via SO-GRPO

> [!tip] 核心洞察
> 通过引入GAE对LLM推理每一步分配优势值，结合可微分割性能奖励和稀疏性奖励，使模型能够在累积足够语义上下文时自主生成<SEG> token，从而在病理学零样本分割中实现显著提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PathChat-SegR1：基于SO-GRPO的病理学推理分割 |
| 英文题名 | PathChat-SegR1: Reasoning Segmentation in Pathology via SO-GRPO |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DQESI75YrD); [GitHub](https://github.com/yul945562-bit/Pathseg) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | PathChat-SegR1 |
| Dataset | PMBT (zero-shot), RD (zero-shot), RDw/E (one-shot), FS-WSI |

> [!tip] 效果简介
> - PMBT (zero-shot) 上，Dice 为 0.58，对比 0.36 (MMR-7B)，变化 +0.22 (61% 相对提升)。
> - RD (zero-shot) 上，Dice 为 0.53，对比 0.33 (MMR-7B)，变化 +0.20。
> - RDw/E (one-shot) 上，Dice 为 0.72，对比 0.47 (MMR-7B)，变化 +0.25。

## 概述

病理图像分割面临一个根本性瓶颈：现有通用推理分割模型缺乏病理领域知识，其视觉编码器无法应对染色变异，且大语言模型（LLM）无法自主判断推理上下文中语义信息是否充分，以适时触发分割，导致对未见病理形态的泛化能力受限。

PathChat-SegR1 针对这一瓶颈提出了一套系统性的解决方案。其核心洞察在于：**LLM在推理过程中生成 `<SEG>` token 的时机，决定了分割触发时视觉特征、推理上下文和空间信息的对齐程度**。通过引入广义优势估计（GAE）对LLM推理的每一步分配信度值，并结合可微分割性能奖励与稀疏性奖励，模型能够在累积足够语义上下文时自主生成 `<SEG>` token，从而在病理学零样本分割中实现显著提升。

方法层面，PathChat-SegR1 对现有推理分割框架进行了三个关键改造（Table 1）：（1）将通用视觉编码器替换为病理专用的 **Ruipath** + **MedSAM** 双编码器架构，并经染色不变自蒸馏预训练以应对染色变异；（2）将 `<SEG>` token 的固定位置插入（如 **LISA**，Lai et al., 2024）改为基于GAE的自主时机决策；（3）将标准GRPO或无RL训练升级为 **SO-GRPO**（Segmentation-Optimized GRPO），整合可微分割奖励、稀疏性奖励和自适应调度。

实验证据表明这些设计的有效性。在PMBT零样本评估中，PathChat-SegR1 相比最佳基线 **MMR-7B**（Jang et al., 2025）提升了 **61%**（Dice 0.58 vs 0.36）；在罕见病数据集（RD）和单样本罕见病数据集（RDw/E）上分别达到 0.53 和 0.72 Dice（Table 3）。消融实验证实，移除RL阶段导致 0.18 Dice 下降，移除Ruipath编码器导致 0.16 Dice 下降，而 SO-GRPO 相比标准GRPO提升了 0.05 Dice 并将收敛步数从24K减少到18K（Table 4, Table 5）。

## 背景与动机

病理图像分割是肿瘤诊断、治疗决策和预后评估的关键环节。然而，病理图像具有高度异质的组织形态、复杂的染色变异和多样化的放大倍率，使得自动化分割面临严峻挑战。现有分割方法可大致分为三类，各自存在显著的局限性。

**闭集分割方法**（如 **nnU-Net**, Isensee et al., Nature Methods 2021）在特定标注数据集上表现优异，但泛化能力极弱——一旦面对训练分布之外的未见病理形态或新类别，性能急剧下降。**提示驱动分割方法**（如 **MedSAM**, Ma et al., Nature Communications 2024；**SAM-Path**, Zhang et al., 2023）依赖用户提供边界框、点或掩码等空间先验，虽能处理一定范围内的类别变化，却无法理解临床文本查询中的语义意图，更不具备自主推理能力。**推理分割方法**（如 **LISA**, Lai et al., 2024；**MMR**, Jang et al., 2025）尝试将大型语言模型的语义理解与分割能力结合，但其视觉编码器通常基于通用图像预训练，缺乏病理领域知识，难以应对染色变异带来的表征漂移。

### 核心瓶颈：语义触发时机的缺失

上述方法的共同缺陷可归结为一个更深层的机制性问题。通用推理分割模型在处理病理图像时，视觉编码器缺乏病理领域知识和染色变异鲁棒性，而 LLM 无法自主判断推理上下文中语义信息的充分性，以适时触发分割。现有方法（如 LISA）采用固定位置插入 `<SEG>` token 的策略，这意味着分割触发与推理过程的语义累积状态完全解耦——模型可能在尚未充分理解组织形态时就仓促生成掩码，或在已获得足够信息后延迟触发，导致视觉特征、推理上下文和空间信息三者无法有效对齐。

### 本文动机

针对上述瓶颈，本文提出 **PathChat-SegR1**，核心动机在于：

1. **引入病理专用视觉编码器**，通过染色不变自蒸馏预训练，使模型获得对染色变异的鲁棒表征能力。
2. **赋予 LLM 自主决定 `<SEG>` token 生成时机的能力**，使分割触发与推理上下文中的语义充分性动态对齐。
3. **设计面向分割的强化学习框架 SO-GRPO**，利用广义优势估计（GAE）为推理链中每一步分配信度，结合可微分割性能奖励和稀疏性奖励，引导模型在累积足够语义上下文时精准触发分割。

通过上述设计，PathChat-SegR1 在零样本病理分割场景下实现了对现有最佳方法的显著超越——在肺骨转移瘤（PMBT）基准上相对 MMR-7B 提升 61%（0.58 vs 0.36 Dice），验证了“语义触发时机自主决策”这一核心洞见的有效性。

## 核心创新

PathChat-SegR1 的核心创新在于通过三个**changed slots**系统性解决了病理推理分割中的关键瓶颈：现有模型因视觉编码器缺乏病理领域知识、LLM无法自主判断分割触发时机，导致对未见病理形态的泛化能力严重受限。

### 创新一：病理专用视觉编码器（RuiPath + MedSAM + 染色不变自蒸馏）

**基线方案**：通用视觉编码器（如 CLIP/SAM），缺乏对病理组织形态和染色变异的鲁棒表征能力。

**创新方案**：引入双编码器架构——
- **RuiPath 编码器**负责为 VLM 推理提供病理域专用视觉特征；
- **MedSAM 编码器**独立提取精细空间特征用于掩码生成，并通过**染色不变自蒸馏预训练**学习染色鲁棒表征。

其预训练损失函数为：

$$\mathcal{L}_{\mathrm{SSL}} = \frac{\alpha}{N} \sum_{i=1}^{N} \mathbf{Cos}(\mathbf{s}_{i,1}, \mathbf{s}_{i,2}) \| z_i^a - z_i^b \|^2 + \mathcal{L}_{\mathrm{MAE}}$$

该损失结合染色模板加权的特征一致性约束和掩码重建目标，使编码器在染色变异场景下仍能保持稳定表征。

**因果证据**：消融实验（Table 4）表明，移除 RuiPath 编码器导致 Dice 下降 **0.16**（从 0.58 降至 0.42）；移除 MedSAM 编码器的染色不变自蒸馏预训练使 Dice 降至 **0.51**，证实该模块是性能的关键支撑。

### 创新二：基于 GAE 的自主 `<SEG>` 生成时机决策

**基线方案**：LISA 等方法在固定位置插入 `<SEG>` token，LLM 无法根据推理上下文中语义信息的充分性自主判断何时触发分割。

**创新方案**：将 `<SEG>` token 的生成建模为序列决策问题，引入**广义优势估计（GAE）**对 LLM 推理链的每一步分配优势值：

$$\hat{A}^{\mathrm{GAE}}(s_t, a_t) = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}$$

这使得模型能够在累积足够语义上下文时自主生成 `<SEG>` token，而非机械地在预设位置触发。该机制直接作用于**因果旋钮**——`<SEG>` 生成时机决定了视觉特征、推理上下文和空间信息三者的对齐质量，进而影响分割精度。

**因果证据**：消融实验（Table 5）显示，移除 GAE 使 Dice 从 0.58 降至 **0.55**，且收敛步骤从 18K 增加至 24K，证实 GAE 对分割质量和训练效率均有显著贡献。

### 创新三：SO-GRPO 强化学习框架

**基线方案**：标准 GRPO 或完全无 RL 训练，无法将分割质量信号有效回传至推理链优化。

**创新方案**：提出 **SO-GRPO**，在标准 GRPO 基础上引入三项关键扩展：
1. **可微分割奖励**（Soft Segmentation Reward）：通过软化概率近似 Dice 系数，打通从分割质量到推理策略的梯度通路：
   $$R_{\mathrm{soft}} = \frac{2 \sum_i p_i g_i + \epsilon}{\sum_i p_i + \sum_i g_i + \epsilon}$$
2. **稀疏性感知奖励**：鼓励在包含空间语义的状态下生成 `<SEG>`，惩罚冗余生成：
   $$R_{\mathrm{sparse}} = \beta_{\mathrm{sparse}} \cdot \mathbb{I}(s_t \in S_{\mathrm{spatial}}) - \gamma_{\mathrm{sparse}} \cdot \mathbb{I}(s_t \notin S_{\mathrm{spatial}})$$
3. **自适应调度**：配合满足 Robbins-Monro 条件的学习率调度 $\alpha_k = \alpha_0 / (1 + \eta k)$ 和 KL 正则化，保证收敛稳定性。

整体优化目标为：

$$\mathcal{I}_{\mathrm{SO-GRPO}}(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \sum_t \hat{\mathbf{A}}^{\mathrm{GAE}}(\mathbf{s}_t, \mathbf{a}_t) \log \pi_{\theta}(\mathbf{a}_t | \mathbf{s}_t) \right] + \lambda_{\mathrm{soft}} \cdot R_{\mathrm{soft}} + \lambda_{\mathrm{sparse}} \cdot R_{\mathrm{sparse}} + \lambda_{\mathrm{spatial}} \cdot R_{\mathrm{spatial}} + \lambda_{\mathrm{format}} \cdot R_{\mathrm{format}} + R_{\mathrm{len}} - \lambda_{\mathrm{KL}} \cdot \mathcal{L}_{\mathrm{KL}}$$

**因果证据**：消融实验（Table 4）表明，完全移除 RL 训练阶段导致 Dice 下降 **0.18**（从 0.58 降至 0.40），是单一模块中影响最大的因素。SO-GRPO 相比标准 GRPO 提升 **0.05 Dice**（0.58 vs 0.53），并将收敛步骤从 24K 减少到 18K（Table 5）。

---

**创新协同效应**：三个创新形成因果闭环——病理专用编码器提供高质量视觉表征（创新一），GAE 机制使 LLM 能自主判断何时触发分割（创新二），SO-GRPO 通过可微奖励将分割质量信号反馈至推理策略优化（创新三）。三者共同支撑了 PathChat-SegR1 在零样本 PMBT 评估中相对最佳基线 MMR-7B 实现 **61% 的相对提升**（0.58 vs 0.36 Dice），以及在一次样本罕见病分割中达到 **0.72 Dice** 的性能突破。

## 整体框架

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_DQESI75YrD/figures/002_Figure_1.jpg]]
*Figure 1: PathChat-SegR1 architecture overview*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_DQESI75YrD/figures/001_Table_1.jpg]]
*Table 1: Comparison of segmentation methods for pathology. Abbreviations: “Unseen Gen.”: Generalization to unseen morphologies/objects; “Path. Spec.”: Pathology-specific models; “Reason.”: Capability for general visual reasoning and language understanding; “Stain Rob.” for stain-variationinvariant representations; “RL-Seg” for segmentation-specific reinforcement learning*

PathChat-SegR1 的整体框架围绕一个核心瓶颈构建：现有通用推理分割模型在病理图像上，视觉编码器缺乏病理领域知识和染色变异鲁棒性，且 LLM 无法自主判断推理上下文中语义信息的充分性以适时触发分割。该框架通过三条主线解决这一问题——病理专用视觉编码、基于强化学习的自主分割触发时机决策、以及染色不变表征学习。

### 架构总览

如图 1 所示，PathChat-SegR1 由四个核心模块构成一条端到端的分割推理管线：

1. **Ruipath 视觉编码器（VLM 侧）**：接收病理图像，提取病理域专用的视觉特征，供 LLM 进行视觉推理。该编码器替代了通用推理分割模型中常见的 CLIP/SAM 编码器，是领域适配的关键组件。

2. **MedSAM 编码器 + Seg-Adapter**：独立于 VLM 侧，对同一病理图像提取精细的空间特征，用于后续掩码生成。Seg-Adapter 是一个带跳跃连接的瓶颈 MLP 结构，负责将 VLM 侧输出的 `<SEG>` token 表征桥接到掩码解码器。

3. **LLM（Qwen2.5VL）**：接收文本查询和 Ruipath 编码的视觉特征，生成推理链，并在推理过程中自主决定何时生成 `<SEG>` token。这一决策时机是框架的核心因果控制点——它决定了分割触发时视觉特征、推理上下文和空间信息的对齐程度。

4. **掩码解码器**：利用 `<SEG>` token 的表征和 MedSAM 编码器提供的空间特征，生成最终的分割掩码。

输入为病理图像和自然语言查询（如“请分割肿瘤区域”），输出为分割掩码及对应的推理链文本。

### 训练流程

PathChat-SegR1 的训练分为三个递进阶段：

**阶段一：染色不变自蒸馏预训练。** MedSAM 编码器在此阶段学习染色不变的表征。具体而言，对同一病理图像施加不同染色模板的增强，通过特征一致性损失约束增强后的特征相近，同时结合掩码自编码器（MAE）重建损失。损失函数为：

$$\mathcal{L}_{\mathrm{SSL}} = \frac{\alpha}{N} \sum_{i=1}^{N} \mathbf{Cos}(\mathbf{s}_{i,1}, \mathbf{s}_{i,2}) \| z_i^a - z_i^b \|^2 + \mathcal{L}_{\mathrm{MAE}}$$

其中染色模板相似度 $\mathbf{Cos}(\mathbf{s}_{i,1}, \mathbf{s}_{i,2})$ 作为权重，使模型在染色差异大时更关注特征一致性。MedSAM 编码器使用 patch size 16，掩码率 75%。此阶段同时进行 VLM 的病理知识预训练。

**阶段二：监督微调（SFT）。** 联合优化推理链生成和掩码预测：

$$\mathcal{L}_{\mathrm{SFT}} = \lambda_{\mathrm{CoT}} \cdot \mathcal{L}_{\mathrm{CE}} + \lambda_{\mathrm{seg}} \cdot (\mathcal{L}_{\mathrm{Dice}} + \mathcal{L}_{\mathrm{BCE}})$$

其中 $\mathcal{L}_{\mathrm{CE}}$ 为推理链生成的交叉熵损失，$\mathcal{L}_{\mathrm{Dice}}$ 和 $\mathcal{L}_{\mathrm{BCE}}$ 为掩码预测损失。为节省训练成本，此阶段对 VLM 应用 LoRA（秩 16，dropout 0.1），对视觉编码器应用适配器，对掩码解码器进行全参数训练。

**阶段三：SO-GRPO 强化学习。** 这是框架的核心创新。标准 GRPO 使用轨迹级优势估计，无法为 `<SEG>` token 的生成时机分配精细的信度。SO-GRPO 引入广义优势估计（GAE）：

$$\hat{A}^{\mathrm{GAE}}(s_t, a_t) = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}$$

为 LLM 推理的每一步分配逐步优势值，使模型能够在累积足够语义上下文时自主生成 `<SEG>` token。同时，SO-GRPO 整合了可微分割奖励 $R_{\mathrm{soft}}$（Dice 的软化近似）和稀疏性奖励 $R_{\mathrm{sparse}}$（鼓励在包含空间语义的状态下生成 `<SEG>`，惩罚冗余生成），整体目标函数为：

$$\mathcal{I}_{\mathrm{SO-GRPO}}(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \sum_t \hat{\mathbf{A}}^{\mathrm{GAE}}(\mathbf{s}_t, \mathbf{a}_t) \log \pi_{\theta}(\mathbf{a}_t | \mathbf{s}_t) \right] + \lambda_{\mathrm{soft}} \cdot R_{\mathrm{soft}} + \lambda_{\mathrm{sparse}} \cdot R_{\mathrm{sparse}} + \lambda_{\mathrm{spatial}} \cdot R_{\mathrm{spatial}} + \lambda_{\mathrm{format}} \cdot R_{\mathrm{format}} + R_{\mathrm{len}} - \lambda_{\mathrm{KL}} \cdot \mathcal{L}_{\mathrm{KL}}$$

其中 $R_{\mathrm{len}} = -\lambda_{\mathrm{len}} \cdot \max(0, \ln(L - L_0 + 1))$ 为简洁性惩罚，$\mathcal{L}_{\mathrm{KL}}$ 为 KL 正则化。学习率采用 $\alpha_k = \alpha_0 / (1 + \eta k)$ 调度，满足 Robbins-Monro 条件以保证收敛。

### 与基线方法的关键差异

Table 1 系统对比了 PathChat-SegR1 与现有病理分割方法的能力差异。传统闭集方法（如 **nnU-Net**，Isensee et al., Nature Methods 2021）和提示分割方法（如 **MedSAM**，Ma et al., Nature Communications 2024）不具备对未见形态的泛化能力和推理能力。推理分割方法（如 **LISA**，Lai et al., 2024；**MMR**，Jang et al., 2025）虽具备推理能力，但缺乏病理专用编码和染色鲁棒性，且 `<SEG>` token 采用固定位置插入而非自主决策。PathChat-SegR1 是唯一同时具备未见形态泛化、病理专用编码、推理能力、染色鲁棒性和分割专用强化学习的方法。

消融实验（Table 4）量化了各模块的贡献：移除 Ruipath 编码器导致 Dice 下降 0.16，移除 RL 训练阶段下降 0.18，移除染色不变自蒸馏下降至 0.51，证实了病理专用编码和自主分割触发是性能提升的核心来源。

## 核心模块与公式推导

PathChat-SegR1 的核心架构由三个关键模块构成，其瓶颈突破依赖于 **<SEG> token 生成时机的自主决策**——LLM 在推理过程中何时触发分割，决定了视觉特征、推理上下文与空间信息三者的对齐质量。

### 双编码器视觉架构

模型采用双路视觉编码器以解耦语义推理与空间定位：

- **Ruipath 编码器（VLM 侧）**：提取病理域专用语义特征，供 LLM 进行形态学推理。移除该编码器导致 PMBT 上 Dice 下降 0.16（Table 4），证实病理领域知识对泛化的关键作用。
- **MedSAM 编码器 + Seg-Adapter**：独立提取精细空间特征用于掩码生成。Seg-Adapter 通过瓶颈 MLP 加跳跃连接的结构，将 VLM 输出的 `<SEG>` token 表征桥接到掩码解码器（Figure 1b-c）。

### 染色不变自蒸馏预训练

病理图像的核心干扰来自染色变异。MedSAM 编码器通过染色不变自蒸馏学习鲁棒表征，其损失函数为：

$$\mathcal{L}_{\mathrm{SSL}} = \frac{\alpha}{N} \sum_{i=1}^{N} \mathbf{Cos}(\mathbf{s}_{i,1}, \mathbf{s}_{i,2}) \| z_i^a - z_i^b \|^2 + \mathcal{L}_{\mathrm{MAE}}$$

其中 $\mathbf{s}_{i,1}, \mathbf{s}_{i,2}$ 为第 $i$ 个样本两种染色模板的权重向量，通过余弦相似度加权特征一致性损失；$\mathcal{L}_{\mathrm{MAE}}$ 为掩码自编码重建损失（75% 掩码率，patch size 16）。消融实验中移除该预训练使 Dice 降至 0.51（Table 4），证实其对染色鲁棒性的贡献。

### SO-GRPO 强化学习机制

SO-GRPO 是方法的核心创新，针对标准 GRPO 在推理分割中的三个缺陷进行扩展：

**1. 逐步优势估计（GAE）**
标准 GRPO 使用轨迹级优势，无法区分推理链中每一步对分割质量的贡献。SO-GRPO 引入 GAE 为每步分配信度：

$$\hat{A}^{\mathrm{GAE}}(s_t, a_t) = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}$$

其中 $\delta_{t+l}$ 为时序差分残差，$\gamma$ 为折扣因子，$\lambda$ 为 GAE 参数。这使得模型能够在累积足够语义上下文时自主生成 `<SEG>` token，而非固定位置插入。移除 GAE 使 Dice 从 0.58 降至 0.55，且收敛步骤从 18K 增至 24K（Table 5）。

**2. 可微分割奖励**
为打通分割质量到推理策略的梯度流，SO-GRPO 采用软 Dice 近似作为可微奖励：

$$R_{\mathrm{soft}} = \frac{2 \sum_i p_i g_i + \epsilon}{\sum_i p_i + \sum_i g_i + \epsilon}$$

其中 $p_i = \sigma(M_{\mathrm{pred},i})$ 为软化后的预测概率，$g_i$ 为真值掩码，$\epsilon$ 为平滑项。

**3. 稀疏性感知奖励**
鼓励在包含空间语义的状态下生成 `<SEG>`，惩罚冗余生成：

$$R_{\mathrm{sparse}} = \beta_{\mathrm{sparse}} \cdot \mathbb{I}(s_t \in S_{\mathrm{spatial}}) - \gamma_{\mathrm{sparse}} \cdot \mathbb{I}(s_t \notin S_{\mathrm{spatial}})$$

其中 $S_{\mathrm{spatial}}$ 为规则检测到的空间语义状态集合。该奖励依赖规则检测空间语义，其对所有病理描述类型的适用性仍需验证。

### 整体优化目标

SO-GRPO 的完整目标函数整合策略梯度、多维奖励和 KL 正则化：

$$\mathcal{I}_{\mathrm{SO-GRPO}}(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \sum_t \hat{\mathbf{A}}^{\mathrm{GAE}}(\mathbf{s}_t, \mathbf{a}_t) \log \pi_{\theta}(\mathbf{a}_t | \mathbf{s}_t) \right] + \lambda_{\mathrm{soft}} \cdot R_{\mathrm{soft}} + \lambda_{\mathrm{sparse}} \cdot R_{\mathrm{sparse}} + \lambda_{\mathrm{spatial}} \cdot R_{\mathrm{spatial}} + \lambda_{\mathrm{format}} \cdot R_{\mathrm{format}} + R_{\mathrm{len}} - \lambda_{\mathrm{KL}} \cdot \mathcal{L}_{\mathrm{KL}}$$

其中 $R_{\mathrm{len}} = -\lambda_{\mathrm{len}} \cdot \max(0, \ln(L - L_0 + 1))$ 为简洁性惩罚，$L$ 为推理链长度，$L_0$ 为容忍阈值。学习率调度 $\alpha_k = \alpha_0 / (1 + \eta k)$ 满足 Robbins-Monro 条件以保证收敛。

### 监督微调损失

RL 阶段之前，模型通过联合优化推理链生成和掩码预测进行监督微调：

$$\mathcal{L}_{\mathrm{SFT}} = \lambda_{\mathrm{CoT}} \cdot \mathcal{L}_{\mathrm{CE}} + \lambda_{\mathrm{seg}} \cdot (\mathcal{L}_{\mathrm{Dice}} + \mathcal{L}_{\mathrm{BCE}})$$

其中 $\mathcal{L}_{\mathrm{CE}}$ 为推理链生成的交叉熵损失，$\mathcal{L}_{\mathrm{Dice}} + \mathcal{L}_{\mathrm{BCE}}$ 为掩码预测的 Dice 和二元交叉熵损失，$\lambda_{\mathrm{CoT}}$ 和 $\lambda_{\mathrm{seg}}$ 为平衡权重。SFT 阶段对 VLM 施加 LoRA（秩 16，dropout 0.1），对视觉编码器施加适配器，对掩码解码器进行全参数训练。移除 SFT 阶段导致 Dice 下降 0.14（Table 4），移除整个 RL 阶段则下降 0.18，表明两阶段训练对最终性能均有显著贡献。

## 实验与分析

### 核心瓶颈与因果机制

现有通用推理分割模型在病理图像上的根本瓶颈在于两个层面：视觉编码器缺乏病理领域知识和对染色变异的鲁棒性，以及LLM无法自主判断推理上下文中语义信息的充分性以适时触发分割。PathChat-SegR1通过将LLM生成`<SEG>` token的时机作为因果调控节点，使视觉特征、推理上下文和空间信息的对齐程度可被显式优化。其核心机制是通过GAE对LLM推理每一步分配优势值，结合可微分割性能奖励和稀疏性奖励，使模型在累积足够语义上下文时自主生成`<SEG>` token。

### 域内公共基准与术中冰冻切片性能

Table 2展示了在8个域内基准（6个公共数据集和2个私有术中冰冻切片类型）上的Dice系数对比。闭集方法（如**nnU-Net**（Isensee et al., Nature Methods 2021））在各数据集上单独训练，而推理分割方法和PathChat-SegR1在所有基准上统一训练并以零样本方式测试。PathChat-SegR1在Camelyon16上达到0.76 Dice，相比**MMR-7B**（Jang et al., 2025）提升33%；在GlaS上达到0.87 Dice，在CRAG上达到0.92 Dice。在更具挑战性的术中冰冻切片场景（FS-Mic和FS-WSI）中，模型仍保持0.74–0.84的高Dice分数，表明其对严重组织伪影的鲁棒性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_DQESI75YrD/figures/004_Table_2.jpg]]
*Table 2: Performance comparison across in-domain public benchmarks and private intraoperative frozen sections measured by Dice coefficient. Closed-set methods are trained separately on each dataset, while reasoning segmentation baselines and PathChat-SegR1 use unified training across all eight benchmarks and tested in a zero-shot manner. FS-Mic: Frozen Sections (Microscope); FS-WSI: Frozen Sections (Whole Slide Image)*

### 未见病理零样本分割

Table 3报告了在未见病理形态上的域外评估结果，这是检验泛化能力的关键测试。在PMBT（骨肿瘤肺转移）零样本评估中，PathChat-SegR1达到0.58 Dice，相比最佳基线**MMR-7B**的0.36 Dice提升了61%（+0.22）。在RD（罕见疾病）零样本评估中，PathChat-SegR1达到0.53 Dice，而MMR-7B仅为0.33 Dice。当提供一次样本作为上下文学习时（RDw/E），PathChat-SegR1进一步提升至0.72 Dice，相比MMR-7B的0.47 Dice提升53%。这些结果表明，基于SO-GRPO的`<SEG>`自主时机决策机制在零样本泛化中发挥了决定性作用。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_DQESI75YrD/figures/006_Table_3.jpg]]
*Table 3: Out-of-domain evaluation on unseen pathologies measured by Dice coefficient. PMBT: Pulmonary Metastasis from Bone Tumors; RD: Rare Diseases; RDw/E: Rare Diseases with one-shot example provided during inference*

### 组件消融分析

Table 4的消融实验量化了各核心模块的贡献。在架构层面，移除Ruipath病理专用编码器导致Dice从0.58降至0.42（下降0.16），移除Seg-Adapter降至0.52，移除自动触发机制降至0.51。在训练层面，移除RL阶段导致最大幅度的性能下降（0.18 Dice，从0.58降至0.40），移除SFT阶段下降0.14 Dice，移除MedSAM编码器的染色不变自蒸馏预训练使Dice降至0.51。在奖励函数层面，移除可微分割奖励使Dice降至0.54。这些结果证实了三个核心模块——病理专用视觉编码器、RL阶段的`<SEG>`时机优化、以及染色不变自蒸馏——对最终性能的不可或缺性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_DQESI75YrD/figures/007_Table_4.jpg]]
*Table 4: Component ablation study on the PMBT dataset measured by Dice coefficient. Architecture ablations remove pathology-specific encoders, training ablations remove pretraining stages and supervision objectives, and reward ablations remove SO-GRPO reward components*

### SO-GRPO组件消融

Table 5进一步剖析了SO-GRPO内部各组件的贡献。完整SO-GRPO达到0.58 Dice，收敛步数为18K，梯度方差为0.031。移除GAE后Dice降至0.55，且收敛步数增加至24K；移除可微分割奖励降至0.54；移除稀疏性感知奖励降至0.56；移除自适应调度降至0.56。值得注意的是，SO-GRPO相比标准GRPO（移除GAE的配置可视为近似标准GRPO）提升了0.05 Dice（0.58 vs 0.53），并将收敛步数从24K减少到18K，验证了逐步优势估计在`<SEG>`时机决策中的关键作用。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_DQESI75YrD/figures/008_Table_5.jpg]]
*Table 5: SO-GRPO component ablation on the PMBT dataset. Performance measured by Dice coefficient, convergence measured by training steps to reach optimal performance, and training stability measured by gradient variance during policy updates*

### 推理链质量评估

Table 6评估了推理链的生成质量。在FS-WSI数据集上，PathChat-SegR1的BLEU-4达到0.315，F1达到0.612，均优于**LISA**（Lai et al., 2024）的0.281和0.568。在PMBT数据集上，BLEU-4为0.311，F1为0.607。这表明SO-GRPO的稀疏性奖励和简洁性惩罚不仅提升了分割性能，也改善了推理链的语义对齐度和简洁性。

### 单样本上下文学习的定性分析

Figure 3展示了PathChat-SegR1在罕见病理上的单样本上下文学习能力。在软骨黏液样纤维瘤的案例中，模型能够分析给定的标注图像，提取形态学特征（如钙化区域的纹理和边界特征），并将其应用于具有不同染色外观的未标注图像，实现无需训练的迁移分割。这一能力源于LLM在推理链中对形态学描述的语义理解，以及染色不变自蒸馏赋予视觉编码器的染色鲁棒性。

### 实验公平性说明

所有推理分割方法在统一数据集和零样本设定下评估，闭集方法在各自数据集上单独训练。使用8:1:1随机划分，所有模型在相同硬件（8×H800 GPU）和超参数下训练，确保对比的公平性。

## 方法谱系与知识库定位

### 1. 与现有推理分割工作的关系

PathChat-SegR1 直接继承自“LLM 推理分割”这一技术路线，该路线以 **LISA** (Lai et al., 2024) 为代表，通过在 LLM 的文本输出中插入特殊 token（如 `<SEG>`）来触发分割解码。LISA 开创性地证明了 LLM 可以将语言推理能力转化为视觉定位能力，但其 `<SEG>` token 的生成位置是固定的——模型在推理链的预设位置强制插入分割指令，而非自主判断何时语义上下文已充分积累。

**MMR** (Jang et al., 2025) 进一步引入了多粒度推理机制，试图在不同语义层次上触发分割，但仍未解决“何时触发”这一核心时序决策问题。PathChat-SegR1 的关键突破在于将 `<SEG>` 的生成时机从固定规则提升为基于 **Generalized Advantage Estimation (GAE)** 的自主决策：LLM 在推理链的每一步都接收一个优势值信度分配，使其能够在累积足够语义上下文时自主生成 `<SEG>` token，而非被动等待预设位置。

在视觉编码器层面，LISA 和 MMR 均依赖通用 CLIP/SAM 编码器，缺乏对病理图像染色变异和组织形态特异性的适应能力。PathChat-SegR1 引入 **Ruipath** 病理专用编码器（VLM 侧）和经过染色不变自蒸馏训练的 **MedSAM** 编码器（掩码生成侧），这一双编码器设计直接回应了病理领域“视觉特征缺乏领域知识”这一瓶颈。消融实验（Table 4）提供了强证据：移除 Ruipath 编码器导致 Dice 下降 0.16，移除 MedSAM 预训练使 Dice 降至 0.51，证实了病理专用视觉表征的不可替代性。

### 2. 与闭集分割和提示分割的边界

PathChat-SegR1 与闭集分割方法（如 **nnU-Net** (Isensee et al., Nature Methods 2021)）和提示分割方法（如 **MedSAM** (Ma et al., Nature Communications 2024)、**SAM-Path** (Zhang et al., 2023)、**SegAnyPath** (Wang et al., IEEE TMI 2024)）存在根本性的能力边界差异，如 Table 1 所总结：

- **闭集方法**（nnU-Net）在各自训练数据集上通常能达到最高的 Dice 分数（Table 2 显示 nnU-Net 在域内基准上表现最佳），但完全不具备对未见病理形态的泛化能力，也无法进行语言交互或视觉推理。
- **提示分割方法**（MedSAM、SAM-Path、SegAnyPath）依赖用户提供的空间提示（点、框）或文本描述来指定分割目标，具备一定的开放词汇能力，但缺乏自主推理能力——它们无法从复杂的临床描述中推断“应该分割什么”。
- **PathChat-SegR1 的独特定位**在于将推理、语言理解和分割统一在一个框架中：模型接收自由形式的文本查询，自主生成推理链并决定分割时机，无需任何空间提示。这使得它能够处理“识别并分割转移性肿瘤病灶”这类需要临床推理的复杂指令，而提示分割方法需要用户事先精确定位目标区域。

Table 3 的零样本评估结果量化了这一边界：在 PMBT 数据集上，PathChat-SegR1 达到 0.58 Dice，而最佳推理分割基线 MMR-7B 仅为 0.36（相对提升 61%）；在罕见病数据集（RD）上，PathChat-SegR1 达到 0.53 Dice（MMR-7B 为 0.33）。这些结果说明，当面对训练中完全未见过的病理形态时，推理分割方法的优势显著，而闭集方法则完全失效。

### 3. 与强化学习训练范式的对比

PathChat-SegR1 提出的 **SO-GRPO**（Segmentation-Optimized GRPO）是对标准 GRPO 的三项关键扩展，Table 5 的消融实验量化了每项扩展的贡献：

- **GAE 逐步优势估计**：标准 GRPO 对整个轨迹分配单一优势值，无法区分推理链中哪些步骤对分割质量贡献更大。GAE 将优势估计分解到每个时间步，使模型能够学习“何时生成 `<SEG>` token”。移除 GAE 使 Dice 从 0.58 降至 0.55，且收敛步骤从 18K 增加到 24K。
- **可微分割奖励**：标准 GRPO 的分割质量奖励是离散的（基于最终掩码的 Dice），梯度无法直接流回推理决策。SO-GRPO 引入软化 Dice 近似 $R_{\mathrm{soft}}$，使分割质量信号可微分地反馈到策略网络。
- **稀疏性奖励**：$R_{\mathrm{sparse}}$ 鼓励模型仅在包含空间语义的状态下生成 `<SEG>`，惩罚冗余生成。这解决了 LLM 在长推理链中可能多次触发分割的问题。

从训练范式看，PathChat-SegR1 采用了“预训练 → SFT → RL”三阶段流程，这与 **Seg-Zero** (Liu et al., 2025) 的推理链分割思路相似，但 Seg-Zero 未引入专门的强化学习阶段来优化分割触发时机。消融实验（Table 4）显示，移除 RL 阶段导致 0.18 Dice 的剧烈下降，证明 RL 对于 `<SEG>` 时序决策的优化是不可或缺的。

### 4. 适用边界与开放问题

**已验证的适用边界**：

1. **病理类型泛化**：PathChat-SegR1 在零样本评估中展现了从常见病理到罕见病理的强泛化能力（PMBT 0.58 Dice, RD 0.53 Dice），但所有评估仍局限于组织病理学图像，未涉及细胞学或分子病理学模态。
2. **染色变异鲁棒性**：染色不变自蒸馏使模型在 H&E 染色变异下保持稳定（消融中移除该模块使 Dice 降至 0.51），但其对特殊染色（如免疫组化、特殊化学染色）的鲁棒性尚未验证。
3. **图像尺度限制**：当前模型处理的是固定大小的图像块（patch），Table 2 中 FS-WSI（全切片图像）的结果表明模型已能处理 WSI 级别的冷冻切片，但论文未详细说明 WSI 处理的具体策略（如是否使用了多尺度聚合或滑动窗口）。

**开放问题与局限**：

1. **稀疏性奖励的规则依赖性**：SO-GRPO 中的 $R_{\mathrm{sparse}}$ 依赖规则检测空间语义（$\mathbb{I}(s_t \in S_{\mathrm{spatial}})$），这需要人工定义“空间语义”的判断标准。该规则是否适用于所有类型的病理描述（如纯文本临床信息触发分割的场景）尚不明确，需要手动验证。

2. **极端染色变异的鲁棒性**：染色不变自蒸馏在训练时使用 H&E 染色的染色模板加权，但对于免疫组化（IHC）等染色机制完全不同的模态，当前预训练策略可能不足以提供鲁棒表征。论文未报告 IHC 图像上的评估结果。

3. **WSI 级分割的扩展路径**：Table 2 中 FS-WSI 的结果暗示了 WSI 级分割的可行性，但论文未详细阐述技术方案。将 PathChat-SegR1 扩展到千兆像素级别的 WSI 分割需要解决上下文聚合、内存效率和多尺度推理等工程挑战。

4. **半自动推理链标注的质量依赖性**：论文使用 Gemini-2.5-Pro 和 DeepSeek-R1 生成推理链，再由三位病理学家修正。这种半自动标注的质量直接影响 SFT 阶段的监督信号质量，进而可能影响最终模型的推理准确性。论文未对标注质量进行系统性的 inter-rater 可靠性分析。

5. **计算成本与部署可行性**：三阶段训练（预训练 + SFT + RL）需要 8×H800 GPU，且 RL 阶段需要 18K 步收敛。对于资源受限的临床部署场景，训练成本可能成为推广障碍。论文未讨论模型压缩或推理加速策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/PathChat_SegR1_Reasoning_Segmentation_in_Pathology_via_SO_GRPO.pdf]]

---
title: "AQuA: Toward Strategic Response Generation for Ambiguous Visual Questions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AQuA_Toward_Strategic_Response_Generation_for_Ambiguous_Visual_Questions.pdf
project_link: https://aqua-iclr2026.github.io/
code_link: null
aliases:
- AAVQASG
- AQuA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将模糊视觉问答划分为四级歧义并为每级绑定对应响应策略。"
primary_logic: "AQuA先构建四级歧义数据集，再用SFT和GRPO训练VLM按歧义程度选择直接回答、推断、列举或澄清。"
claims:
- "四级歧义标签将清晰问题、低指代歧义、多解释问题和高度歧义问题映射到不同最优响应策略。"
- "SFT加GRPO使Qwen2.5-VL-3B-Tuned在AQUA上达到86.28%的整体策略准确率。"
- "GRPO相比仅SFT进一步提升Level 2和Level 3策略表现，但Level 1存在轻微下降。"
- "失败主要集中在相邻歧义等级边界混淆和显著性驱动的错误降级。"
---

# AQuA: Toward Strategic Response Generation for Ambiguous Visual Questions

> [!tip] 核心洞察
> 通过将歧义VQA实例细分为四个等级并定义对应的最优响应策略，结合SFT和GRPO训练，可以使VLM学会根据歧义程度自适应地选择策略（直接回答、推断意图、列出备选、请求澄清），从而显著提升在模糊场景下的响应质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AQuA：面向模糊视觉问题的策略性响应生成 |
| 英文题名 | AQuA: Toward Strategic Response Generation for Ambiguous Visual Questions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7b1MpD6IF8) · [Project](https://aqua-iclr2026.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AQUA (Ambiguous Visual Question Answering) + SFT + GRPO |
| Dataset | AQUA |

> [!tip] 效果简介
> - AQUA 上，Overall Strategic Accuracy (%) 为 86.28，对比 32.83，变化 +53.45。
> - AQUA 上，Level 0 Strategic Accuracy (%) 为 99.56，对比 97.11，变化 +2.45。
> - AQUA 上，Level 1 Strategic Accuracy (%) 为 77.0，对比 0.11，变化 +76.89。

## 概要

本文提出 **AQuA (Ambiguous Visual Question Answering)**，一个面向模糊视觉问题的策略性响应生成框架。核心贡献包括：(1) 构建了一个包含 **7.2K** 样本的四级歧义VQA数据集，将歧义按性质和程度细分为 Level 0-3；(2) 提出 **SFT + GRPO** 两阶段训练方法，使视觉语言模型（VLM）学会根据歧义等级自适应选择响应策略（直接回答、上下文推断、列出所有可能、请求澄清）；(3) 在 AQUA 基准上，经过微调的 Qwen2.5-VL-3B-Tuned 模型实现了 **86.28%** 的整体策略准确率，显著超越零样本 GPT-5 的 42.25% 和 Gemini 2.5 Flash 的 37.83%。



现有VQA基准主要包含清晰无歧义的图像-问题对，而现实场景中常存在不同程度的歧义。现有方法仅采用二元的“回答或询问”策略，无法根据歧义的类型和程度自适应地选择策略。如 Figure 1 所示，当图像中没有任何一个球棒在视觉上显著时，GPT、Gemini 和 Qwen 仍武断地选择回答，而 AQuA 训练的模型则请求澄清。



## 核心方法与创新机理

**核心洞察**：通过将歧义VQA实例细分为四个等级并定义对应的最优响应策略，结合 SFT 和 GRPO 训练，可以使 VLM 学会根据歧义程度自适应地选择策略，从而显著提升在模糊场景下的响应质量。

**因果旋钮**：将歧义VQA实例按歧义性质和程度细分为四个等级（Level 0-3），并为每个等级定义最优响应策略（直接回答、从上下文推断、列出所有可能选项、请求澄清），通过监督微调（SFT）和组相对策略优化（GRPO）训练模型，使其能够根据歧义等级自适应地选择策略。



![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_7b1MpD6IF8_AQuA_Toward_Str/figures/001_Figure_1.jpg]]
*Figure 1: Examples of model responses to an ambiguous visual question. In this image, none of the bats is visually salient, making the visual context ambiguous. While GPT, Gemini, and Qwen provide answers by arbitrarily selecting (e.g., the bat in the foreground) despite the ambiguity, our model, which is trained to handle such cases strategically, requests clarification instead.*

AQuA 框架包含以下核心模块：

1. **数据集生成**：使用 COCO 图像和 GPT-5 生成四级歧义 VQA 样本
2. **数据集过滤**：三级过滤管道（等级一致性检查、最佳匹配验证、真实世界与质量验证），使用 GPT-5-mini 评估
3. **人类验证**：在 MTurk 上对评估集进行人类验证，每个样本由两名标注者独立判断
4. **监督微调 (SFT)**：在 AQUA 训练集上对 Qwen2.5-VL-3B-Instruct 和 InternVL3-2B-Instruct 进行全参数微调
5. **组相对策略优化 (GRPO)**：在 SFT 基础上应用 GRPO，使用 LLM-as-a-judge 奖励策略对齐的输出
6. **LLM-as-a-judge 评估**：使用 GPT-5-mini 评估事实一致性和策略准确性



### 5.1 四级歧义分类

AQUA 将 VQA 实例分为四个等级（Figure 2）：

- **Level 0**：无歧义问题，直接回答
- **Level 1**：低指代歧义，可通过上下文推断意图
- **Level 2**：多个有效解释，列出所有可能选项
- **Level 3**：高度歧义，需要请求澄清

### 5.2 显著性得分公式

对于 Level 1，使用加权组合确定物体视觉显著性：

$$score = 0.7 \times \text{area\_ratio} + 0.3 \times \text{normalized\_distance\_to\_center}$$

其中权重分别为 0.7（面积比）和 0.3（到图像中心的归一化距离）。得分 > 0.6 的物体被视为显著。

### 5.3 GRPO 奖励函数

$$R(y|x,I) = \begin{cases} 1 - \lambda & \text{if strategy is correct but factual distortion detected}, \\ 1 & \text{if strategy is correct and no distortion}, \\ 0 & \text{otherwise} \end{cases}$$

其中 $\lambda=0.3$ 为事实扭曲惩罚。Figure 3 展示了奖励分配过程。



## 实验与关键发现

### 6.1 主要结果

Table 2 展示了各 VLM 在 AQUA 上的主要基准测试结果：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_7b1MpD6IF8_AQuA_Toward_Str/figures/005_Table_2.jpg]]
*Table 2: Main benchmarking results of various VLMs on AQUA. Unk denotes Unknown.*

| 模型 | 整体策略准确率 (%) | Level 0 | Level 1 | Level 2 | Level 3 |
|------|-------------------|---------|---------|---------|---------|
| Qwen2.5-VL-3B-Instruct (零样本) | 32.83 | 97.11 | 0.11 | 33.33 | 0.78 |
| Qwen2.5-VL-3B-Tuned (SFT+GRPO) | **86.28** | 99.56 | 77.0 | 82.22 | 86.33 |
| InternVL3-2B-Instruct (零样本) | 25.95 | 96.67 | 0.0 | 3.11 | 4.0 |
| InternVL3-2B-Tuned (SFT+GRPO) | **79.11** | 98.78 | 80.0 | 59.67 | 78.0 |
| GPT-5 (零样本) | 42.25 | 94.56 | 59.0 | 10.67 | 4.78 |
| Gemini 2.5 Flash (零样本) | 37.83 | 93.56 | 47.89 | 8.44 | 1.44 |

**关键发现**：零样本 Qwen2.5-VL-3B-Instruct 的整体策略准确率仅为 32.83%，而经过 SFT+GRPO 微调后提升至 86.28%。零样本 GPT-5 的整体策略准确率仅为 42.25%，而经过微调的 Qwen2.5-VL-3B-Tuned 达到 86.28%，显著超越闭源模型。

### 6.2 消融实验

Table 3 展示了 SFT 与 SFT+GRPO 的消融对比：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_7b1MpD6IF8_AQuA_Toward_Str/figures/007_Table_3.jpg]]
*Table 3: Performance comparison of models tuned on AQuA with SFT and SFT+GRPO. G, U, and Unk respectively denote Grounded, Ungrounded, and Unknown.*

| 模型 | 整体策略准确率 (%) |
|------|-------------------|
| Qwen2.5-VL-3B-Tuned (SFT) | 83.81 |
| Qwen2.5-VL-3B-Tuned (SFT+GRPO) | **86.28** |
| InternVL3-2B-Tuned (SFT) | 73.42 |
| InternVL3-2B-Tuned (SFT+GRPO) | **79.11** |

**关键发现**：SFT+GRPO 相比仅 SFT 在 Level 2 和 Level 3 上进一步提升，并稳定了整体性能。但 GRPO 导致 Level 1 性能略有下降。

### 6.3 响应模式分析

Figure 5 展示了 Qwen2.5-VL-3B-Instruct 在 AQUA 上的响应模式混淆矩阵：

- **零样本模型**（Figure 5a）：存在强烈的 Level 0 预测偏差
- **SFT 模型**（Figure 5b）：倾向于坍缩到 Level 1 响应
- **SFT+GRPO 模型**（Figure 5c）：在各等级上更均衡，显著减少 Level 1 偏差

### 6.4 其他分析

- **CoT 提示**：对策略选择无益甚至降低性能
- **策略提示**：对小型开源模型无效，但对大型闭源模型略有提升
- **GRPO 训练样本量**：从 60 增加到 120 可进一步提升性能（Qwen: 86.28% → 87.83%; InternVL: 79.11% → 82.39%）（Table 8）
- **人类评估**：Level 0 和 Level 1 的策略选择与 AQUA 定义高度一致（50/50 和 48/50），Level 2 和 Level 3 也达到 32/50 的一致性（Table 1）
- **LLM-as-a-judge 可靠性**：GPT-5-mini 与人类评估一致性达 98.5%

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_7b1MpD6IF8_AQuA_Toward_Str/figures/003_Table_1.jpg]]
*Table 1: Evaluation results on human strategic choices.*

### 6.5 失败案例分析

Figure 6 展示了两种主要失败模式：
- **等级边界混淆**：模型在 Level 1 和 Level 2 之间（猫 vs 雕塑）、Level 2 和 Level 3 之间（沙发）出现混淆
- **显著性驱动错误**：模型因关注显著物体（如马）而从 Level 3 错误地降级到 Level 1

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_7b1MpD6IF8_AQuA_Toward_Str/figures/014_Table_4.jpg]]
*Table 4: Evaluation results on the clarification subset.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_7b1MpD6IF8_AQuA_Toward_Str/figures/015_Table_5.jpg]]
*Table 5: Evaluation results of samples generated using Open Images V7.*



## 定位与知识库关联

AQuA 属于 **策略性VQA** 领域，与以下工作相关：

- **ClearVQA (Jian et al., 2025)**：采用二元“回答或询问”策略，AQuA 将其扩展为四级策略
- **AmbigQA (Min et al., 2020)**：文本领域的歧义问答，AQuA 将其扩展到视觉模态
- **Vague (Nam et al., 2024)**：视觉上下文澄清歧义表达，AQuA 更关注策略选择
- **Reliable VQA (Whitehead et al., 2022)**：在不确定时选择弃权，AQuA 提供更细粒度的策略

**局限性**：
- 数据集使用 COCO 图像，可能限制场景多样性
- Level 2 和 Level 3 的边界存在主观性
- 模型在边界案例和显著性驱动错误上仍存在失败
- GRPO 训练样本量较小（60-120）
- 仅评估了 Qwen2.5-VL-3B 和 InternVL3-2B 两种模型

**开放问题**：
- AQUA 数据集能否泛化到更多样化的图像源（如网络图像、医学图像）？
- 四级歧义分类是否足够？是否存在需要更多或更少等级的场景？
- GRPO 奖励函数中的 $\lambda=0.3$ 是否最优？
- 模型在 Level 1 上的性能下降是否可以通过改进 GRPO 奖励设计来缓解？
- 该方法能否扩展到其他多模态任务（如视觉定位、图像描述）？



## 原文 PDF

![[paperPDFs/ICLR_2026/AQuA_Toward_Strategic_Response_Generation_for_Ambiguous_Visual_Questions.pdf]]

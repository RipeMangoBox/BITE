---
title: "Perception-R1: Advancing Multimodal Reasoning Capabilities of MLLMs via Visual Perception Reward"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Perception_R1_Advancing_Multimodal_Reasoning_Capabilities_of_MLLMs_via_Visual_Perception_Reward.pdf
project_link: null
code_link: https://github.com/tongxiao2002/Perception-R1
aliases:
- PR
- Perception-R1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "Perception-R1 adds visual perception reward to GRPO by checking response consistency with atomic visual annotations extracted from CoT trajectories."
primary_logic: "It builds annotation references from strong-model CoTs, scores generated reasoning with a judge LLM, and combines perception, accuracy, format, and repetition rewards."
claims:
- "The method addresses multimodal failures caused by perception errors that accuracy-only RLVR does not fix."
- "Visual perception reward gives dense feedback on whether reasoning mentions correct visual facts."
- "The note reports strong 7B performance using only 1,442 training samples."
---

# Perception-R1: Advancing Multimodal Reasoning Capabilities of MLLMs via Visual Perception Reward

> [!tip] 核心洞察
> 多模态推理可分解为多模态感知和逻辑推理；仅优化答案正确性无法纠正感知错误，甚至可能强化有缺陷的推理路径。通过从CoT轨迹中提取视觉标注作为参考，并利用评判LLM评估模型响应与标注的一致性，可以为感知提供密集的奖励信号，从而有效提升感知和推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Perception-R1：通过视觉感知奖励提升多模态大模型推理能力 |
| 英文题名 | Perception-R1: Advancing Multimodal Reasoning Capabilities of MLLMs via Visual Perception Reward |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KttCXdjj4w) · [GitHub](https://github.com/tongxiao2002/Perception-R1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Perception-R1 |
| Dataset | MathVista testmini, MathVerse testmini, MathVision test, WeMath testmini |

> [!tip] 效果简介
> - MathVista testmini 上，Accuracy 为 74.2，对比 71.3 (OpenVLThinker-7B)，变化 +2.9。
> - MathVerse testmini 上，Accuracy 为 54.3，对比 50.2 (OpenVLThinker-7B)，变化 +4.1。
> - MathVision test 上，Accuracy 为 28.6，对比 27.0 (OpenVLThinker-7B)，变化 +1.6。

## 概要

本文提出 **Perception-R1**，一种通过引入视觉感知奖励（visual perception reward）来增强多模态大语言模型（MLLMs）多模态推理能力的方法。核心洞察在于：现有基于可验证奖励的强化学习（RLVR）方法仅依赖答案正确性奖励，无法有效提升模型的视觉感知能力，从而限制了多模态推理的进一步提升。Perception-R1 通过从思维链（CoT）轨迹中提取视觉标注作为参考，并利用评判 LLM 评估模型响应与标注的一致性，为感知提供密集的奖励信号。实验表明，该方法仅使用 1,442 个训练样本，即在多个基准上超越需要 200K 数据的 Vision-R1 等强基线，并在 8 个基准中的 7 个上取得最优结果。



多模态推理可分解为多模态感知和逻辑推理两个子能力。然而，现有 RLVR 方法仅基于答案正确性提供奖励，无法有效纠正感知错误。论文通过 McNemar 检验发现：

- 仅使用准确率奖励的 RLVR 训练后，MLLMs 的多模态感知能力与基座模型无显著差异（p 值分别为 0.22 和 0.69，均高于 0.05 显著性水平）。
- 对于 Qwen2.5-VL-7B-IT，在 MathVista 和 MathVerse 上的失败案例中分别有 78% 和 76% 由多模态感知错误导致。

Figure 1 展示了一个典型案例：基座模型 Qwen2.5-VL-7B-IT 及其 RLVR 变体均产生严重感知错误，但通过猜测得到了正确答案；而 Perception-R1 首先准确描述图像，然后正确解决问题。



## 核心方法与创新机理

Perception-R1 的核心创新在于引入视觉感知奖励，通过显式鼓励 MLLMs 准确感知视觉内容，缓解多模态感知的奖励稀疏性问题。具体创新点包括：

1. **视觉感知奖励**：从 CoT 轨迹中提取原子视觉标注序列 V = (v₁, v₂, ..., vₘ)，利用评判 LLM 评估模型响应与标注的一致性，计算视觉感知奖励 r_v。
2. **重复惩罚奖励**：引入 r_p 惩罚重复生成，促进输出多样性。
3. **数据高效性**：仅使用 Geometry3K 数据集中的 1,442 个样本（过滤后），这些样本具有高比例（82%）的视觉信息，无需冷启动 SFT 阶段。



![[assets/figures/papers/iclr26_0002_KttCXdjj4w_Perception-R1_Advancing_Multimodal_Reasoning_Cap/figures/001_Figure_1.jpg]]
*Figure 1: A comparison of three MLLMs on a geometry problem. Both Qwen2.5-VL-7B-IT and its RLVR-trained variant make severe perception errors but manage to guess the answer, whereas our Perception-R1 first accurately describes the image and then solves the problem correctly.*

Figure 2 展示了 Perception-R1 的训练流程概览。整体框架包含以下步骤：

1. **CoT 轨迹生成**：使用 SOTA 专有 MLLM（Gemini-2.5-Pro）在多模态推理数据集上生成包含准确视觉信息的 CoT 轨迹。
2. **视觉标注提取**：使用文本 LLM（Qwen2.5-32B-IT）从 CoT 轨迹中提取原子视觉标注序列 V。
3. **视觉感知奖励计算**：使用评判 LLM（Qwen2.5-32B-IT）评估模型响应与视觉标注的一致性，计算视觉感知奖励 r_v。
4. **GRPO 优化**：结合格式奖励、准确率奖励、视觉感知奖励和重复惩罚奖励，使用 GRPO 算法优化策略模型。



**基线 RLVR 奖励函数**（Eq. 1）：
\[
\boldsymbol { r } ( y _ { i } , a ) = \boldsymbol { \alpha } \cdot \boldsymbol { r } _ { f } ( y _ { i } ) + \boldsymbol { \beta } \cdot \boldsymbol { r } _ { a } ( y _ { i } , a )
\]
由格式奖励 r_f 和准确率奖励 r_a 组成，α 和 β 为系数。

**GRPO 优势计算**（Eq. 2）：
\[
\hat { A } _ { i } = \frac { r ( y _ { i } , a ) - \mathrm { m e a n } \{ r ( y _ { 1 } , a ) , r ( y _ { 2 } , a ) , . . . , r ( y _ { G } , a ) \} } { \mathrm { s t d } \{ r ( y _ { 1 } , a ) , r ( y _ { 2 } , a ) , . . . , r ( y _ { G } , a ) \} }
\]
通过对 G 个 rollouts 的奖励进行归一化得到第 i 个 rollouts 的优势。

**GRPO 目标函数**（Eq. 3）：
\[
\begin{array} { l } { \displaystyle \mathcal { I } ( \theta ) = \mathbb { E } _ { \boldsymbol { x } \in \mathcal { D } , \{ y _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta _ { \mathrm { o l d } } } } } \\ { \displaystyle \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { | y _ { i } | } \sum _ { t = 1 } ^ { | y _ { i } | } \left\{ \operatorname* { m i n } \left[ s _ { t } ( x , y _ { i } ) \hat { A } _ { i } , \mathrm { c l i p } \left( s _ { t } ( x , y _ { i } ) , 1 - \varepsilon , 1 + \varepsilon \right) \hat { A } _ { i } \right] - \delta \cdot \mathrm { K L } ( \pi _ { \theta } \| \pi _ { r e f } ) \right\} \right] } \end{array}
\]
包含裁剪的代理目标和 KL 散度正则化。

**视觉感知奖励**（Eq. 4）：
\[
r _ { v } ( y _ { i } , \mathcal { V } ) = \frac { \operatorname* { s u m } \{ o _ { i , 1 } , o _ { i , 2 } , . . . , o _ { i , m } \} } { | o _ { i , 1 } , o _ { i , 2 } , . . . , o _ { i , m } | }
\]
为评判 LLM 判断为正确的原子视觉标注比例。

**视觉增强奖励函数**（Eq. 5）：
\[
\boldsymbol { r } ( y _ { i } , a , \mathcal { V } ) = \alpha \cdot \boldsymbol { r } _ { f } ( y _ { i } ) + \beta \cdot \boldsymbol { r } _ { a } ( y _ { i } , a ) + \gamma \cdot \boldsymbol { r } _ { v } ( y _ { i } , \mathcal { V } ) + \boldsymbol { r } _ { p } ( y _ { i } )
\]
在基线基础上增加视觉感知奖励 r_v 和重复惩罚奖励 r_p。



## 实验与关键发现

### 6.1 主要结果

Table 1 展示了 Perception-R1 与基线在 8 个基准上的性能对比。Perception-R1-7B 在大多数基准上取得最优结果：


![[assets/figures/papers/iclr26_0002_KttCXdjj4w_Perception-R1_Advancing_Multimodal_Reasoning_Cap/figures/003_Table_1.jpg]]
*Table 1: Performance comparison between Perception-R1 and baselines on 8 benchmarks. The best and second-best results of Open-Source Reasoning MLLMs are highlighted in red and blue. † R1-VL-7B and Vision-R1-7B both trained on WeMath and MathVision, their results are omitted.*

| 基准 | 指标 | Perception-R1-7B | 最佳基线 | Δ |
|------|------|------------------|----------|---|
| MathVista testmini | Accuracy | **74.2** | 71.3 (OpenVLThinker-7B) | +2.9 |
| MathVerse testmini | Accuracy | **54.3** | 50.2 (OpenVLThinker-7B) | +4.1 |
| MathVision test | Accuracy | **28.6** | 27.0 (OpenVLThinker-7B) | +1.6 |
| WeMath testmini | Accuracy | **72.0** | 66.3 (OpenVLThinker-7B) | +5.7 |
| MMMU val | Accuracy | **60.8** | 52.3 (R1-VL-7B) | +8.5 |
| MMMU-Pro overall | Accuracy | **42.4** | 38.3 (MM-Eureka-7B) | +4.1 |
| MMStar val | Accuracy | **64.5** | 64.2 (MM-Eureka-7B) | +0.3 |
| EMMA full | Accuracy | 27.5 | 28.1 (MM-Eureka-7B) | -0.6 |

Perception-R1 仅使用 1.4K 训练数据，显著优于使用 200K 数据的 Vision-R1-7B 和使用 260K 数据的 R1-VL-7B。

### 6.2 消融研究

Table 2 展示了组件和方法消融研究：


![[assets/figures/papers/iclr26_0002_KttCXdjj4w_Perception-R1_Advancing_Multimodal_Reasoning_Cap/figures/004_Table_2.jpg]]
*Table 2: Component & approach ablation studies of Perception-R1. The best result is marked in red.*

- 移除视觉感知奖励后，所有基准上的性能均下降。
- 移除重复惩罚奖励后，所有基准上的性能均下降。
- 使用 SFT 替代 RLVR，性能在大多数基准上低于基座模型。

Figure 3 展示了超参数消融：
- 视觉感知奖励系数 γ 在 {0.1, 0.3, 0.5, 0.7, 0.9} 范围内性能相当，均显著优于 γ=0（无视觉感知奖励）。
- 使用较弱的评判 LLM（如 7B）会导致性能下降，在 MathVerse 和 MathVision 上甚至低于原始 MLLM。

### 6.3 鲁棒性分析

Table 10 显示，即使 20% 的视觉感知奖励被随机翻转，模型平均性能仍优于标准 GRPO，展示了方法的鲁棒性。

### 6.4 视觉感知能力提升

McNemar 检验表明，Perception-R1 的 p 值为 0.04，低于 0.05 显著性阈值，表明其多模态感知能力有显著提升。Table 12 进一步显示，在 MathVerse 和 MMMU-Pro 的纯视觉子集上，Perception-R1 大幅超越基线。

### 6.5 计算成本

Table 13 显示，Perception-R1 的数据准备成本仅为 1.1M tokens，训练时间为 167.4 A800-Hours，远低于 Vision-R1（134M tokens, 3392 H800-Hours）等基线。

### 补充图表

![[assets/figures/papers/iclr26_0002_KttCXdjj4w_Perception-R1_Advancing_Multimodal_Reasoning_Cap/figures/008_Table_3.jpg]]
*Table 3: Confusion matrix of Qwen2-VL-7B-IT evaluated on $\mathcal { D } _ { e }$*

![[assets/figures/papers/iclr26_0002_KttCXdjj4w_Perception-R1_Advancing_Multimodal_Reasoning_Cap/figures/009_Table_4.jpg]]
*Table 4: Confusion matrix of accuracy-only RLVR trained Qwen2-VL-7B-IT evaluated on $\mathcal { D } _ { e }$*

![[assets/figures/papers/iclr26_0002_KttCXdjj4w_Perception-R1_Advancing_Multimodal_Reasoning_Cap/figures/010_Table_5.jpg]]
*Table 5: Confusion matrix of Qwen2.5-VL-7B-IT evaluated on $\mathcal { D } _ { e }$ .*




## 定位与知识库关联

Perception-R1 属于多模态推理增强方法，其方法谱系定位如下：

- **与现有 RLVR 方法的关系**：现有方法（如 MM-Eureka、Vision-R1、R1-VL）主要依赖答案正确性奖励，未能有效解决感知瓶颈。Perception-R1 首次引入视觉感知奖励，直接针对感知能力进行优化。
- **与过程奖励方法的关系**：与 SophiaVL-R1 等使用思考奖励模型的方法不同，Perception-R1 专注于感知层面而非推理过程，两者互补。
- **数据效率优势**：相比 Vision-R1（200K 冷启动数据 + 10K RL 数据）和 MM-Eureka（15.6K 数据），Perception-R1 仅需 1,442 个高质量几何样本，展示了极强的数据效率。
- **局限性**：训练数据仅来自 Geometry3K（几何问题），可能限制方法在其他类型视觉任务上的泛化性；视觉标注提取依赖专有 MLLM（Gemini-2.5-Pro）和文本 LLM（Qwen2.5-32B-IT），引入了对第三方模型的依赖；评判 LLM 的评估可能不完全准确。



## 原文 PDF

![[paperPDFs/ICLR_2026/Perception_R1_Advancing_Multimodal_Reasoning_Capabilities_of_MLLMs_via_Visual_Perception_Reward.pdf]]

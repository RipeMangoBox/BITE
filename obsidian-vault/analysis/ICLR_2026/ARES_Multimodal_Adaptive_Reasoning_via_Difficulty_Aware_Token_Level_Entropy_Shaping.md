---
title: "ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ARES_Multimodal_Adaptive_Reasoning_via_Difficulty_Aware_Token_Level_Entropy_Shaping.pdf
aliases:
- AMARDATLERS
- ARES
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "ARES uses window entropy as a difficulty-aware signal and optimizes reasoning length with adaptive cold-start data plus AEPO entropy shaping."
primary_logic: "It first teaches difficulty-conditioned response lengths, then adjusts high-window-entropy exploration and KL strength by online difficulty buckets during RL."
claims:
- "Window entropy is used to detect key reasoning moments more reliably than single-token entropy."
- "AdaCS and AEPO are designed to shorten easy-question reasoning while increasing exploration on hard questions."
- "The note reports large gains on MathVision, MMMU-Pro, and AIME25 over open-source baselines."
---

# ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping

> [!tip] 核心洞察
> 通过将令牌级熵聚合为滑动窗口统计量（窗口熵），可以可靠地识别推理关键时刻；减少HWE令牌对简单问题有益，增加HWE令牌对解决困难问题至关重要。基于此，ARES通过自适应冷启动和自适应熵策略优化（AEPO）动态分配推理努力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ARES：基于难度感知的令牌级熵塑形的多模态自适应推理 |
| 英文题名 | ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2g945Ngc7l); [GitHub](https://github.com/shawn0728/ARES) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | ARES (multimodal Adaptive Reasoning via difficulty-aware token-level Entropy reward Shaping) |
| Dataset | MathVision, MMMU-Pro, AIME25, MathVerse-V |

> [!tip] 效果简介
> - MathVision 上，Accuracy 为 51.9，对比 32.9 (best open-source)，变化 +19.0。
> - MMMU-Pro 上，Accuracy 为 54.8，对比 43.3 (best open-source)，变化 +11.5。
> - AIME25 上，Accuracy 为 61.7，对比 3.3 (most 7B baselines)，变化 +58.4。

## 概述

ARES（multimodal Adaptive Reasoning via difficulty-aware token-level Entropy reward Shaping）是一种针对多模态大推理模型（MLRM）的两阶段训练框架，旨在解决现有模型在推理过程中“简单问题过度思考、困难问题探索不足”的核心矛盾。该方法通过引入**窗口熵**（window entropy）作为推理关键时刻的可靠检测信号，结合自适应冷启动（Adaptive Cold-Start, AdaCS）和自适应熵策略优化（Adaptive Entropy Policy Optimization, AEPO）两个阶段，实现基于问题难度的动态推理努力分配。实验结果表明，ARES-7B在MathVision上超过最佳开源模型+19.0，在MMMU-Pro上超过+11.5，在AIME25上达到61.7（大多数7B基线低于3.3）。

## 背景与动机

现有的多模态大推理模型（MLRM）在推理过程中存在一个普遍问题：**在简单问题上过度思考，生成冗长的推理轨迹，而在困难问题上探索不足，导致无法找到解决方案**。这一现象源于当前模型对所有问题采用统一的推理策略，缺乏对问题难度的感知和自适应调整能力。

论文通过定量分析（Figure 1）揭示了熵与难度之间的关键交互作用：
- 对于简单任务，低于熵阈值的响应既更短也更准确；
- 对于困难任务，高于熵阈值的探索能带来更高的准确率；
- 响应长度随难度显著增加；
- 在每个难度级别内，正确案例在简单问题上使用更少的高熵令牌，但在困难问题上使用更多的高熵令牌。

这些发现表明，**限制探索能提高简单问题的效率，而鼓励额外探索对解决困难问题至关重要**。

## 核心创新

ARES的核心创新在于将令牌级熵聚合为滑动窗口统计量（窗口熵），并基于此设计了一套完整的难度感知推理框架：

1. **窗口熵作为推理关键时刻的可靠检测器**：相比单令牌熵，窗口熵（连续令牌上的平均熵）能更可靠地识别推理关键决策点（Figure 5）。中等窗口大小（4-8个令牌）提供了最佳权衡：平滑局部噪声的同时保持足够的聚焦能力。

2. **自适应冷启动（AdaCS）**：通过将推理长度与问题难度显式关联的数据进行微调，赋予模型初始的难度感知能力。目标响应长度定义为 $L_{\mathrm{target}}(p) = (1-p) \cdot L(0) + p \cdot L(1)$，其中 $p$ 是问题的通过率。

3. **自适应熵策略优化（AEPO）**：使用高窗口熵区域触发探索，并通过分层奖励和动态KL控制探索深度。AEPO包含三个关键组件：
   - 高窗口熵检测器：基于动态批次级阈值标记推理关键区域
   - 分层熵奖励：基于难度桶的偏差惩罚
   - 动态KL设计：在推理关键窗口放松KL约束

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2g945Ngc7l_ARES_Multimodal/figures/001_Figure_1.jpg]]
*Figure 1: (a) Difficulty modulates the exploratory effort along the reasoning path*

ARES的整体训练流程如Figure 2所示，包含两个阶段：

**阶段1：自适应冷启动微调（Adaptive Cold-Start Fine-Tuning）**
- 难度感知的选择性数据整理
- 自适应KL引导的微调
- 在文本和多模态输入上建立强初始化

**阶段2：自适应熵策略优化（Adaptive Entropy Policy Optimization, AEPO）**
- 在线难度分桶
- 熵感知的轨迹生成
- 高熵窗口作为探索的分支点
- 动态推理深度分配

两个阶段共同实现了不确定性感知、难度自适应的推理能力。

## 核心模块与公式推导

### 5.1 窗口熵检测器

令牌级熵定义为：
$$H_t = -\sum_{j=1}^V p_{t,j} \log p_{t,j}, \quad p_t = \pi_\theta(\cdot \mid q, o_{<t})$$

窗口熵通过滑动窗口平均令牌级熵：
$$\bar{H}_{t:w} = \frac{1}{w} \sum_{\tau=t}^{t+w-1} H_{\tau}$$

批次级高熵阈值定义为：
$$\tau_{\mathrm{high}} = \frac{1}{|\mathcal{D}|} \sum_{y \in \mathcal{D}} \mathrm{Quantile}_{0.95}(\{H_t(y)\}_{t=1}^{|y|})$$

### 5.2 在线难度分桶

基于pass@8准确率将问题分为三个难度桶：
$$d(x) = \begin{cases} \mathsf{easy}, & \mathsf{pass@8}(x) \ge 6, \\ \mathsf{medium}, & 3 \le \mathsf{pass@8}(x) < 6, \\ \mathsf{hard}, & \mathsf{pass@8}(x) \le 2 \end{cases}$$

其中 $\mathsf{pass@8}(x) = \frac{1}{8} \sum_{k=1}^{8} \mathbf{1}\{\mathrm{correct}(y^{(k)}, x)\}$。

### 5.3 分层熵奖励设计

高熵令牌的桶依赖目标在线更新：
$$N_{\mathrm{HE}}^{\mathrm{target}}(d) = \mathbb{E}_{\mathrm{batch}}[N_{\mathrm{HE}} \mid d]$$

闭式拉格朗日乘子用于缩放熵惩罚：
$$\lambda_d = \max\left(0, \frac{\mathbb{E}_{\mathrm{batch}}[N_{\mathrm{HE}} \mid d] - N_{\mathrm{HE}}^{\mathrm{target}}(d)}{\mathrm{Var}_{\mathrm{batch}}[N_{\mathrm{HE}} \mid d] + \varepsilon}\right)$$

塑形方向函数根据难度桶定义：
$$g_d(\Delta) = \begin{cases} \max(0, \Delta), & d = \mathrm{easy} \\ |\Delta|, & d = \mathrm{medium} \\ \max(0, -\Delta), & d = \mathrm{hard} \end{cases}$$

最终的分层奖励仅在回答错误时应用熵惩罚：
$$R(x,y;d) = R_{\mathrm{acc}}(x,y) - \mathbf{1}[\mathrm{acc}(x,y)=0] \lambda_d g_d(\Delta(y;d))$$

### 5.4 动态KL设计

令牌自适应的KL权重在验证过的高熵窗口内放松约束：
$$\beta_{i,t} = \beta_d \cdot \rho_t, \quad \rho_t = \begin{cases} \rho (<1), & \mathrm{if~} t \in \mathcal{W}^{\mathrm{valid}} \\ 1, & \mathrm{otherwise} \end{cases}$$

### 5.5 AEPO代理目标

$$\mathcal{J}_{\mathrm{AEPO}}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D},\{o^i\}_{i=1}^G\sim\pi_{\theta_{\mathrm{old}}}(\cdot|q)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o^i|} \sum_{t=1}^{|o^i|} \min\left( r_{i,t}(\theta)\tilde{A}_{i,t}, \mathrm{clip}(r_{i,t}(\theta),1-\epsilon_\ell,1+\epsilon_h)\tilde{A}_{i,t} \right) - \beta_{d(i),t} D_{\mathrm{KL}}(\pi_\theta(\cdot|s_{i,t}) \| \pi_{\mathrm{ref}}(\cdot|s_{i,t})) \right]$$

## 实验与分析

### 6.1 多模态推理基准性能

Table 1展示了ARES在多个多模态推理基准上的性能。ARES-7B在MathVision上达到51.9（超过最佳开源模型+19.0），在MMMU-Pro上达到54.8（超过+11.5），在MathVerse-V上达到56.5，在MathVista上达到74.6，在MMMU上达到67.9。ARES-3B在相应规模上也取得了领先性能。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2g945Ngc7l_ARES_Multimodal/figures/007_Table_1.jpg]]
*Table 1: Performance comparison of various MLLMs on diverse multimodal reasoning benchmarks. Within each model group (3B and 7B), the best results are highlighted in bold, and the second-best are underlined. Scores in italics indicate that they are not reported in the original work and are obtained using the VLMEvalKit (Duan et al., 2025) for evaluation. MathVerse-V, DynaMath-W and WeMath-S denotes the vision-only, worst, and strict settings, respectively.*

### 6.2 文本推理基准性能

Table 4展示了文本推理基准上的结果。ARES-7B在AIME25上达到61.7（大多数7B基线低于3.3），在AIME24上达到65.0，在MATH500上达到95.2，在MMLU Pro上达到67.0，平均59.6，大幅超越所有开源基线。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2g945Ngc7l_ARES_Multimodal/figures/012_Table_4.jpg]]
*Table 4: Performance on textual reasoning benchmarks. AIME24 and AIME25 results are averaged over eight independent inference runs to reduce score variance. Results on AIME24/25, MATH500, MMLU Pro, BBEH, and GPQA. ARES-3B and ARES-7B substantially outperform all open-source baselines at their respective scales, achieving large average gains (∆ rows) and narrowing the gap to leading proprietary systems.*

### 6.3 消融研究

Table 3的消融研究系统性地评估了各组件贡献：
- 分层熵奖励单独带来平均准确率+1.8点的提升（相对于GRPO基线）
- 动态KL组件带来平均准确率+1.3点的提升
- 完整ARES模型在所有配置中达到最高平均准确率55.7

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2g945Ngc7l_ARES_Multimodal/figures/011_Table_3.jpg]]
*Table 3: Ablation study of Dynamic KL Loss and Entropy Reward. Building upon our Cold Start stage. Best results per column are bold and second-best are underlined.*

Figure 7进一步显示，结合KL正则化和熵塑形产生最稳定和显著的增益。

### 6.4 自适应推理行为分析

Table 2和Figure 3展示了ARES的自适应推理行为：
- AdaCS（ARES-CS-7B）根据任务难度调节响应长度
- AEPO（ARES-RL-7B）进一步增强这一效果：在困难任务（如OlympiadBench、AIME25）上延长推理，在简单任务（如GSM8K、MathVista）上缩短推理

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2g945Ngc7l_ARES_Multimodal/figures/010_Table_2.jpg]]
*Table 2: Accuracy and response length comparison across multimodal and textual benchmarks. We report both accuracy (Acc) and average response length (Len) for five model variants (ARES-CS-Vanilla, ARES-CS-7B, ARES-CS-Vanilla-GRPO, ARES-CS-Vanilla-RL, and ARES-RL-7B) on six benchmarks. Visualization of these results is provided in Figure 8 (accuracy) and Figure 9 (response length) in Appendix.*

Figure 9显示RL训练在大多数基准上减少了响应长度，表明推理效率提升；而在最具挑战性的数据集（AIME25和OlympiadBench）上响应长度增加，突显了自适应行为。

### 6.5 训练动态

Figure 10展示了ValLine GRPO在冷启动模型上的训练动态：高熵令牌数量的增长与响应长度和准确率的增长紧密对齐，验证了熵作为推理努力原则性代理的有效性。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2g945Ngc7l_ARES_Multimodal/figures/013_Table_5.jpg]]
*Table 5: Textual and multimodal reasoning datasets source of ARES cold-start data.*

## 方法谱系与知识库定位

ARES属于**基于强化学习的自适应推理**方法谱系，与以下工作相关：

**推理效率优化**：与"overthinker's diet"（Chen et al., 2025c）、"CoT-valve"（Ma et al., 2025）等通过难度感知训练或长度压缩实现自适应推理的工作相关。ARES的创新在于使用窗口熵作为细粒度的推理努力信号。

**多模态推理强化学习**：基于DeepSeek-R1（DeepSeek-AI et al., 2025）的RLVR范式，与MM-Eureka（Meng et al., 2025）、OpenVLThinker（Deng et al., 2025）等工作同属多模态推理RL训练方向。ARES的独特贡献在于引入熵塑形和动态KL控制。

**策略优化算法**：在GRPO（DeepSeek-AI et al., 2025）和DAPO（Yu et al., 2025b）的基础上，ARES提出了AEPO算法，通过理论分析（附录F、M、N）证明了KL损失相对于KL惩罚在方差控制上的优势，以及AEPO等价于令牌重加权自然梯度更新的性质。

**知识库定位**：ARES填补了"如何根据问题难度动态分配推理计算"这一关键空白。其核心见解——窗口熵可作为推理关键时刻的可靠检测信号——为未来研究提供了新的理论基础和实用工具。

## 原文 PDF

![[paperPDFs/ICLR_2026/ARES_Multimodal_Adaptive_Reasoning_via_Difficulty_Aware_Token_Level_Entropy_Shaping.pdf]]

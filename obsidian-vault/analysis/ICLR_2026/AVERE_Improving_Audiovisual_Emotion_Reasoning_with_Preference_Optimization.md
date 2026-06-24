---
title: "AVERE: Improving Audiovisual Emotion Reasoning with Preference Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AVERE_Improving_Audiovisual_Emotion_Reasoning_with_Preference_Optimization.pdf
aliases:
- AD
- AVERE
- AVEm-DPO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "AVEm-DPO constructs audiovisual preference pairs and adds text-prior debiasing to align emotion reasoning with real audio-visual evidence."
primary_logic: "It combines prompt-conditioned modality preference, emotion response preference, and text-prior subtraction inside a DPO objective."
claims:
- "AVEm-DPO targets both spurious emotion reasoning and hallucinated audiovisual cues."
- "PMP, ERP, and TPD each create preference signals that penalize modality mismatch or text-prior overuse."
- "The note reports gains on EmoReAlM and standard audiovisual emotion benchmarks over the base model."
---

# AVERE: Improving Audiovisual Emotion Reasoning with Preference Optimization

> [!tip] 核心洞察
> 通过构建细粒度的多模态偏好对（包括输入模态偏好和输出响应偏好）并引入文本先验正则项，可以直接优化模型使其更忠实于真实的视听输入，从而同时缓解推理错误和感知错误。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AVERE：通过偏好优化提升视听情感推理能力 |
| 英文题名 | AVERE: Improving Audiovisual Emotion Reasoning with Preference Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=td682AAuPr); [Project](https://avere-iclr.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AVEm-DPO |
| Dataset | DFEW, RAVDESS |

> [!tip] 效果简介
> - DFEW 上，UAR 为 58.54，对比 53.59 (Our base)，变化 +4.95。
> - DFEW 上，WAR 为 64.24，对比 53.01 (Our base)，变化 +11.23。
> - RAVDESS 上，UAR 为 58.66，对比 53.59 (Our base)，变化 +5.07。

## 概述

本文提出 **AVEm-DPO**（Audiovisual Emotion Direct Preference Optimization），一种面向视听情感推理的多模态偏好优化方法。现有视听多模态大语言模型（MLLM）在情感推理中普遍存在两类关键错误：(i) **推理错误**——将情感预测建立在与情感无关的线索上（虚假关联）；(ii) **感知错误**——因语言模型文本先验而虚构视听线索（幻觉）。AVEm-DPO 通过三类偏好对齐机制——基于提示的模态偏好（PMP）、基于情感的反应偏好（ERP）和文本先验去偏（TPD）——直接优化模型使其更忠实于真实的视听输入，从而同时缓解这两类错误。

在作者提出的 **EmoReAlM** 基准上，AVEm-DPO 平均准确率达 83.3%，相对基模型提升 28.0%（Table 13）。在 DFEW、RAVDESS、MER2023 和 EMER 等现有基准上，AVEm-DPO 均取得最优零样本性能（Table 2）。用户评估中，AVEm-DPO 在情感描述、线索关联和不一致性方面分别以 54.74%、43.35% 和 4.67% 的比例被选为最佳（Table 4）。

## 背景与动机

### 2.1 现有方法的不足

现有视听 MLLM 在情感推理中存在两类关键错误（Figure 1）：
- **推理错误**：模型将情感预测建立在与情感无关的线索上（虚假关联）。例如，Figure 1 中模型将“微笑”这一视觉线索与“快乐”情感关联，但视频中的人物实际上并未微笑。
- **感知错误**：模型因语言模型文本先验而虚构视听线索（幻觉）。例如，Figure 1 中模型声称听到“笑声”，但音频中并无笑声。

### 2.2 现有基准的局限

现有视听情感识别基准（如 DFEW、RAVDESS、MER2023）主要评估情感分类准确率，无法系统检测虚假关联和幻觉。为此，作者构建了 **EmoReAlM**（Emotion Reasoning and Alignment Benchmark），包含三类任务（Figure 2）：
- **Emotion Reasoning - Basic**：基础情感推理，测试模型从音频或视觉线索推断情感的能力。
- **Modality Agreement**：模态一致性判断，测试模型判断音频和视觉模态是否一致表达同一情感。
- **Emotion Reasoning - Stress Test**：压力测试，包含无幻觉、虚假关联和情感相关幻觉三个子任务，专门检测虚假关联和幻觉。

EmoReAlM 基准包含 4000 个人工验证的多选题，覆盖 2649 个唯一视频（Table 1），随机准确率基线为 25%（基础推理）和 50%（模态一致性和压力测试）。

## 核心创新

AVEm-DPO 的核心创新在于构建细粒度的多模态偏好对并引入文本先验正则项，具体包括：

1. **基于提示的模态偏好（PMP）**：根据查询模态选择性地替换被拒绝的输入模态，减少跨模态干扰。例如，当查询为“音频中有什么线索表明该情感？”时，仅替换被拒绝对中的音频模态，保留视频模态。

2. **基于情感的反应偏好（ERP）**：为每个选择的响应构建两种加权拒绝响应——视频相关虚假关联响应（\(y_l^{vr}\)）和情感相关幻觉响应（\(y_l^{er}\)），分别抑制虚假关联和幻觉。

3. **文本先验去偏（TPD）**：在奖励函数中减去文本仅输入的对数概率，惩罚模型对纯文本先验的过度依赖，从而消除线索幻觉。

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_td682AAuPr_AVERE_Improving/figures/001_Figure_1.jpg]]
*Figure 1: Existing MLLMs (i) include spurious associations between AV cues and emotions – reasoning errors (blue highlight) and (ii) hallucinate AV cues to explain emotions – perception errors (red highlight). AV: audiovisual.*

AVEm-DPO 的整体框架如 Figure 4 所示，包含以下模块：

1. **视听编码器**：使用 LanguageBind Video Encoder 提取视频帧特征，Whisper Large v3 提取音频特征。
2. **LLM 骨干网络**：基于 EmotionLLaMA 修改，生成文本响应。
3. **LoRA 适配器**：高效微调 LLM 骨干（rank 8, scale 4）。
4. **PMP 模块**：根据提示模态选择性地构建输入偏好对。
5. **ERP 模块**：构建包含虚假关联和幻觉的拒绝响应。
6. **TPD 模块**：惩罚对文本先验的依赖。

训练流程：
- 使用 MAFW 和 MER2025 Track-1 训练集作为源数据集，通过 Gemini 2.5 Flash 自动生成偏好数据，共 41687 个偏好样本。
- 训练超参数：学习率 5e-7，batch size 2 per GPU，8×H100 GPU，β=0.1，λ_av=1.0，β_er=β_vr=0.5，γ_TPD=0.2，LoRA rank 8 scale 4，梯度累积 4 步。

## 核心模块与公式推导

### 5.1 标准 DPO 框架

标准 DPO 目标函数为最大化策略在视听输入下的期望奖励，同时惩罚与参考模型的 KL 散度：

\[
\operatorname*{max}_{\pi_\theta} \mathbb{E}_{(a,v,x)\sim\mathcal{D}, y\sim\pi_\theta(\cdot|a,v,x)} [r(a,v,x,y)] - \beta \mathbb{D}_{\mathbf{KL}}(\pi_\theta(\cdot|a,v,x) \parallel \pi_{\mathbf{ref}}(\cdot|a,v,x))
\]

最优策略下的奖励形式为：

\[
r(a,v,x,y) = \beta \log \frac{\pi_\theta(y|a,v,x)}{\pi_{\mathrm{ref}}(y|a,v,x)} + \beta \log Z(a,v,x)
\]

标准 DPO 损失为：

\[
\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}_{(a,v,x,y_w,y_l)\sim\mathcal{D}^{\mathrm{pef}}} [\log \sigma(\beta \log \frac{\pi_\theta(y_w|a,v,x)}{\pi_{\mathrm{ref}}(y_w|a,v,x)} - \beta \log \frac{\pi_\theta(y_l|a,v,x)}{\pi_{\mathrm{ref}}(y_l|a,v,x)})]
\]

### 5.2 视听 DPO 损失（输入偏好）

扩展 DPO 损失以强制对视听输入进行偏好排序：

\[
\mathcal{L}_{\mathrm{DP0}}^{av} = -\mathbb{E}[\log \sigma(u(a_w,v_w,a_l,v_l,x,y_w))], \quad u(\cdot) = \beta \log \frac{\pi_\theta(y_w|a_w,v_w,x)}{\pi_{\mathrm{eff}}(y_w|a_w,v_w,x)} - \beta \log \frac{\pi_\theta(y_w|a_l,v_l,x)}{\pi_{\mathrm{eff}}(y_w|a_l,v_l,x)}
\]

### 5.3 基于提示的模态偏好损失（PMP）

根据提示模态条件化 DPO 损失，仅修改被拒绝对中的相关模态：

\[
\mathcal{L}_{\mathtt{DPO}}^{av-prompt} = -\mathbb{E}[\log \sigma(u(a_w,v_w, a_l^{\mathtt{PMP}}, v_l^{\mathtt{PMP}}, x^m, y_w))]
\]

### 5.4 基于情感的反应偏好损失（ERP）

包含两种加权拒绝响应（视频相关虚假关联和情感相关幻觉）的 DPO 损失：

\[
\mathcal{L}_{\mathrm{DPO}}^{y} = -\mathbb{E}_{(a_w,v_w,x,y_w,y_l^v,y_l^v)\sim\mathcal{D}_y^{\mathrm{Ref}}} [\log \sigma[\beta(\log \frac{\pi_\theta(y_w|a_w,v_w,x)}{\pi_{\mathrm{ref}}(y_w|a_w,v_w,x)} - \sum_{i\in\{v:r_w,c_r\}} \beta_i \log \frac{\pi_\theta(y_l^i|a_w,v_w,x)}{\pi_{\mathrm{ref}}(y_i^i|a_w,v_w,x)})]]
\]

### 5.5 文本先验去偏（TPD）

奖励减去文本仅输入的对数概率以降低文本先验偏差：

\[
r(a,v,x,y) = \beta \log \frac{\pi_\theta(y|a,v,x)}{\pi_{\mathrm{ref}}(y|a,v,x)} + \beta \log Z(a,v,x) - \gamma_{\mathrm{TPD}} \log \pi_{\mathrm{text}}(y|x)
\]

包含文本先验去偏项的 DPO 损失：

\[
\mathcal{L}_{\mathrm{DPO-TPD}} = -\mathbb{E}_{(a,v,x,y_w,y_l)\sim\mathcal{D}^{\mathrm{pref}}} [\log \sigma(\beta(\log \frac{\pi_\theta(y_w|(a,v,x))}{\pi_{\mathrm{ref}}(y_w|(a,v,x))} - \log \frac{\pi_\theta(y_l|(a,v,x))}{\pi_{\mathrm{ref}}(y_l|(a,v,x))}) - \gamma_{\mathrm{TPD}}(\log \pi_{\mathrm{text}}(y_w|x) - \log \pi_{\mathrm{text}}(y_l|x)))]
\]

### 5.6 AVEm-DPO 总损失

结合 TPD 加权响应偏好和 PMP 视听输入偏好的最终目标函数：

\[
\mathcal{L}_{\mathrm{AVEm-DPO}} = \mathcal{L}_{\mathrm{DPO-TPD}}^{y} + \lambda_{av} \mathcal{L}_{\mathrm{DPO}}^{av-prompt}
\]

## 实验与分析

### 6.1 主要结果

**Table 2: 零样本性能对比**


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_td682AAuPr_AVERE_Improving/figures/006_Table_2.jpg]]
*Table 2: Zero-shot performance comparison of different methods on existing audiovisual emotion recognition benchmarks. Mod. are the modalities input to the model with the prompt. A: Audio, V:Video, T: Text Subtitles. ‡: evaluation without text subtitle input.*

| 基准 | 指标 | AVEm-DPO | 基模型 | 提升 |
|------|------|----------|--------|------|
| DFEW | UAR | 58.54 | 53.59 | +4.95 |
| DFEW | WAR | 64.24 | 53.01 | +11.23 |
| RAVDESS | UAR | 58.66 | 53.59 | +5.07 |
| RAVDESS | WAR | 55.48 | 53.01 | +2.47 |
| MER2023 | F1 | 92.18 | 89.56 | +2.62 |
| EMER | Clue | 6.37 | 5.82 | +0.55 |
| EMER | Label | 7.08 | 6.51 | +0.57 |
| EMER | Spurious | 7.09 | 6.48 | +0.61 |

**Table 13: EmoReAlM 基准性能**

| 任务 | 指标 | AVEm-DPO | 基模型 | 相对提升 |
|------|------|----------|--------|----------|
| 平均 | Avg. Acc. | 83.3 | 65.1 | 28.0% |
| 基础推理-音频 | Acc. | 77.9 | 69.2 | 12.6% |
| 基础推理-视觉 | Acc. | 92.5 | 85.3 | 8.4% |
| 模态一致性 | F1 | 60.0 | 34.6 | 73.4% |
| 压力测试-音频 | F1 | 80.9 | 50.3 | 60.8% |
| 压力测试-视觉 | F1 | 94.6 | 59.9 | 57.9% |

### 6.2 消融研究

**Table 5: 组件消融**


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_td682AAuPr_AVERE_Improving/figures/013_Table_5.jpg]]
*Table 5: Ablation study over different components of the proposed AVEm-DPO approach. PMP: Prompt-based Modality Preference, ERP: Emotion-based Response Preference, TPD: Text Prior Debiasing.*

| 配置 | 基础推理 | 模态一致性 | 压力测试 | 虚假关联 | 幻觉 |
|------|----------|------------|----------|----------|------|
| 完整 AVEm-DPO | 85.2 | 60.1 | 87.8 | 92.7 | 97.6 |
| 去除 PMP | 83.1 | 56.8 | 85.2 | 90.1 | 95.2 |
| 去除 ERP | 83.5 | 57.5 | 86.0 | 91.0 | 95.8 |
| 去除 TPD | 84.0 | 58.2 | 86.5 | 91.5 | 96.0 |
| 对比解码 (VCD) | 70.5 | 45.0 | 72.0 | 78.0 | 85.0 |

关键发现：
- 去除 PMP 后，EmoReAlM 平均准确率从 83.3% 降至 79.8%。
- 去除 ERP 后，平均准确率降至 80.5%。
- 去除 TPD 后，平均准确率降至 81.2%，且幻觉压力测试样本性能大幅下降，证明其消除线索幻觉的有效性。
- 对比解码（VCD）显著差于 AVEm-DPO。

### 6.3 用户评估

**Table 4: EMER 用户评估**


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_td682AAuPr_AVERE_Improving/figures/008_Table_4.jpg]]
*Table 4: User evaluation on EMER.*

| 模型 | 情感描述 | 线索关联 | 不一致性 |
|------|----------|----------|----------|
| AVEm-DPO | 54.74% | 43.35% | 4.67% |
| 基模型 | 22.08% | 28.45% | 12.74% |
| EmotionLLaMA | 12.53% | 15.50% | 38.64% |
| Qwen 2.5 Omni | 10.65% | 12.70% | 43.95% |

### 6.4 注意力分析与鲁棒性

**Figure 5** 展示了 AVEm-DPO 对注意力分布和对数似然偏移的影响：
- 左两图：AVEm-DPO 增加了对相关模态的注意力比例，确保模型响应基于相关模态。
- 右两图：AVEm-DPO 在对抗性音频输入下产生可忽略的对数似然偏移，显示出鲁棒性。

**Figure 12-14** 进一步验证了 AVEm-DPO 在对抗性设置下的鲁棒性，AVEm-DPO 受无关模态中对抗性输入的影响最小。

### 6.5 超参数敏感性

**Figure 11** 显示：
- 增加 β_vr 可缓解虚假关联，增加 β_er 可改善幻觉样本性能。
- γ_TPD=0.1 时幻觉样本性能显著提升，γ_TPD>0.2 时饱和。
- λ_av>1.0 时 PMP 性能饱和。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_td682AAuPr_AVERE_Improving/figures/004_Table_1.jpg]]
*Table 1: EmoReAlM Benchmark Statistics.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_td682AAuPr_AVERE_Improving/figures/007_Table_3.jpg]]
*Table 3: Performance comparison of different methods on the proposed EmoReAlM Benchmark.*


## 方法谱系与知识库定位

### 7.1 方法谱系

AVEm-DPO 属于多模态偏好优化方法，与以下方法相关：

| 方法 | 关系 | 差异 |
|------|------|------|
| **标准 DPO** (Rafailov et al., 2023) | 基础框架 | 仅使用响应偏好，无模态偏好和文本先验去偏 |
| **Vista-DPO** (Huang et al., 2025b) | 多模态 DPO 变体 | 使用无关响应作为第二拒绝响应，但无 PMP 和 TPD |
| **MDPO** (Wang et al., 2024) | 多模态偏好优化 | 无基于提示的模态偏好和文本先验去偏 |
| **OmniDPO** (Chen et al., 2025) | 全模态幻觉缓解 | 无情感特定的偏好构建 |
| **VCD** (Leng et al., 2024) | 对比解码 | 显著差于 AVEm-DPO |

### 7.2 知识库定位

AVEm-DPO 在以下方面填补了现有方法的空白：

1. **细粒度多模态偏好构建**：首次在情感推理中同时考虑输入模态偏好和输出响应偏好，并基于提示条件化模态选择。

2. **文本先验去偏**：首次在 DPO 框架中显式惩罚文本先验依赖，有效消除线索幻觉。

3. **系统化评估基准**：EmoReAlM 基准专门设计用于检测虚假关联和幻觉，填补了现有情感推理基准的评估空白。

### 7.3 局限性与开放问题

**局限性**：
- EmoReAlM 基准仅使用 DFEW 数据集作为视频源，可能限制了场景和情感的多样性。
- 偏好数据使用 Gemini 2.5 Flash 自动生成，可能存在标注噪声。
- 方法仅在 7 类基本情感上评估，未涵盖更复杂的情感维度（如复合情感、情感强度）。
- 未评估模型在跨文化或低资源语言场景下的表现。
- 训练计算资源需求较高（8×H100 GPU）。
- 未与基于检索增强生成（RAG）或思维链（CoT）的方法进行直接比较。

**开放问题**：
- AVEm-DPO 能否推广到其他视听理解任务（如视频描述、问答）？
- 如何将方法扩展到更细粒度的情感维度（如效价-唤醒度）？
- PMP 中不同负采样策略（随机视频、扩散噪声等）的理论依据是什么？
- TPD 中 γ_TPD 的最优值是否与模型规模或数据集有关？
- AVEm-DPO 是否能在保持通用能力的同时提升情感推理？
- 如何减少对大规模人工验证的依赖？

## 原文 PDF

![[paperPDFs/ICLR_2026/AVERE_Improving_Audiovisual_Emotion_Reasoning_with_Preference_Optimization.pdf]]

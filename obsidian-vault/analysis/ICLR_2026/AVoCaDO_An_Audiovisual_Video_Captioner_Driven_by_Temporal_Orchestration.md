---
title: "AVoCaDO: An Audiovisual Video Captioner Driven by Temporal Orchestration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AVoCaDO_An_Audiovisual_Video_Captioner_Driven_by_Temporal_Orchestration.pdf
aliases:
- AVoCaDO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "AVoCaDO用时间对齐视听描述数据进行SFT，并用GRPO奖励优化事件覆盖、对话保真和长度控制。"
primary_logic: "先构建融合视觉与音频的时间连贯描述，再对Qwen2.5-Omni进行两阶段后训练以提升视听视频描述。"
claims:
- "两阶段描述生成比简单拼接视觉和音频描述更能捕捉视听事件时间对应关系。"
- "检查表、对话和长度奖励共同减少遗漏、重复坍塌与ASR失真。"
- "AVoCaDO在video-SALMONN-2、UGC-VideoCap和多项QA评估上优于开源基线。"
---

# AVoCaDO: An Audiovisual Video Captioner Driven by Temporal Orchestration

> [!tip] 核心洞察
> 通过先分别生成视觉和音频的模态特定描述，再将其与原始视频一起输入大模型进行融合，生成时间上连贯的多模态描述，能够有效避免直接联合生成时出现的信息遗漏，并实现精确的视听事件时间对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AVoCaDO：由时间编排驱动的视听视频描述生成器 |
| 英文题名 | AVoCaDO: An Audiovisual Video Captioner Driven by Temporal Orchestration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vjEl1PuIDE); [Project](https://avocado-captioner.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AVoCaDO |
| Dataset | video-SALMONN-2 testset, UGC-VideoCap, Daily-Omni |

> [!tip] 效果简介
> - video-SALMONN-2 testset 上，Total↓ 为 37.3，对比 video-SALMONN-2: 42.1，变化 -4.8。
> - UGC-VideoCap 上，Avg.↑ 为 73.2，对比 Gemini-2.5-Pro: 72.6，变化 +0.6。
> - UGC-VideoCap 上，Audio↑ 为 73.0，对比 Gemini-2.5-Pro: 72.0，变化 +1.0。

## 概述

AVoCaDO (An Audiovisual Video Captioner Driven by Temporal Orchestration) 是一个基于 Qwen2.5-Omni-7B 构建的开源视听视频描述生成模型。其核心创新在于通过两阶段后训练流水线——监督微调 (SFT) 和基于 GRPO 的强化学习——显著提升了视频描述中视听事件的时间对齐精度和对话准确性。在 video-SALMONN-2 测试集上，AVoCaDO 达到 Total 37.3，优于所有开源模型；在 UGC-VideoCap 上平均分 73.2，甚至超越了商业模型 Gemini-2.5-Pro (72.6)。此外，在 Daily-Omni 和 WorldSense 的问答评估中，AVoCaDO 分别达到 50.1 和 25.7，大幅领先其他开源模型。

## 背景与动机

现有视频描述模型大多仅依赖视觉模态，忽略了音频信号中丰富的语义线索（如对话、旁白、背景音乐）。即使通过独立音频模型生成描述再拼接，也无法建模视听事件之间的细粒度时间对齐和因果交互，导致在需要跨模态对齐理解的任务中性能显著下降。

初步实验 (Figure 1) 验证了这一瓶颈：在 Daily-Omni 上，联合视听描述相比拼接式描述，平均准确率提升 15.8%，在“AV Event Alignment”类别中提升 27.8%。这表明，简单拼接模态特定描述无法有效捕捉视听事件之间的时间对应关系，亟需一种能够实现精确时间对齐的联合描述生成方法。

## 核心创新

AVoCaDO 的核心创新可归纳为以下三点：

1. **两阶段后训练流水线**：提出 AVoCaDO SFT + AVoCaDO GRPO 的两阶段策略。SFT 阶段在精心构建的 107K 高质量、时间对齐的视听描述数据集上进行监督微调；GRPO 阶段利用基于检查表、对话和长度正则化的奖励函数，进一步优化时间连贯性、对话准确性，并抑制重复坍塌和调节描述长度。

2. **高质量时间对齐数据集构建**：通过先分别生成视觉和音频的模态特定描述，再将其与原始视频一起输入大模型进行融合，生成时间上连贯的多模态描述。这一两阶段策略能够有效避免直接联合生成时出现的信息遗漏，并实现精确的视听事件时间对齐。

3. **三项互补奖励函数设计**：在 GRPO 阶段引入 (1) 基于检查表的奖励 R_C，确保关键事件覆盖；(2) 基于对话的奖励 R_D，保证 ASR 保真度和说话者识别准确性；(3) 长度正则化奖励 R_L，抑制重复坍塌并调节描述长度。

## 整体框架


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vjEl1PuIDE_AVoCaDO_An_Audi/figures/001_Figure_1.jpg]]
*Figure 1: Schematic illustration of the pilot experiment. In this example, naively concatenating captions from the video and audio modalities fails to yield a correct answer to the corresponding question. In contrast, jointly processing both modalities to generate a time-aligned caption provides sufficient information, as indicated by the underlined text*

AVoCaDO 的整体框架包含以下核心模块：

- **基础模型**：Qwen2.5-Omni-7B，提供内置的视听信号对齐能力（通过交错令牌序列）
- **AVoCaDO SFT 阶段**：在 107K 高质量时间对齐视听描述数据集上进行监督微调
- **AVoCaDO GRPO 阶段**：使用 GRPO 算法和三项定制奖励函数优化模型
- **两阶段描述生成策略**：先分别生成视觉和音频描述，再融合为时间对齐的多模态描述
- **质量检查器**：过滤低质量描述，保留合成完整性评分 ≥ 4 的样本

训练数据来源多样，包括 TikTok-10M (24K)、Short-Video (18K)、Shot2Story (20K)、FineVideo (29K)、YouTube-Commons (11K) 和 CinePile (5K)，确保覆盖多种视听场景。

## 核心模块与公式推导

### 5.1 GRPO 优化框架

AVoCaDO GRPO 阶段采用 Group Relative Policy Optimization (GRPO) 算法。优势函数基于组内奖励归一化：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \ldots, r_G\})}{\operatorname{std}(\{r_1, r_2, \ldots, r_G\})}$$

优化目标包含裁剪代理目标和 KL 散度惩罚项：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{\{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(o_i|q)} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)} A_i, \operatorname{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)}, 1-\varepsilon, 1+\varepsilon \right) A_i \right) - \beta \cdot \mathbb{D}_{\mathrm{KL}}(\pi_\theta || \pi_{\mathrm{ref}}) \right) \right]$$

### 5.2 检查表奖励 R_C

基于检查表的奖励衡量生成描述中正确提及关键点的平均比例：

$$\mathcal{R}_c(S_{\mathrm{gen}} | K) = \frac{1}{|K|} \sum_{i=1}^{|K|} \operatorname{Judge}(S_{\mathrm{gen}}, k_i)$$

关键点组织为五个维度：跨模态叙事逻辑、动态动作与交互、听觉元素、时空与摄影、静态实体描述。

### 5.3 对话奖励 R_D

对话奖励基于编辑距离计算内容相似度：

$$\operatorname{Sim}(c_i^{\mathrm{gen}}, c_j^{\mathrm{gt}}) = 1 - \frac{\operatorname{edit.distance}(c_i^{\mathrm{gen}}, c_j^{\mathrm{gt}})}{\max(\operatorname{len}(c_i^{\mathrm{gen}}), \operatorname{len}(c_j^{\mathrm{gt}}))}$$

最优对话子序列匹配使用动态规划，相似度阈值 γ=0.6：

$$F_{i,j} = \begin{cases} 0 & \text{if } i=0 \text{ or } j=0 \\ \max\{F_{i-1,j}, F_{i,j-1}\} & \text{if } i>0, j>0, \operatorname{Sim}(c_i^{\mathrm{gen}}, c_j^{\mathrm{gt}}) < \gamma \\ \max\{F_{i-1,j}, F_{i,j-1}, F_{i-1,j-1} + \operatorname{Sim}(c_i^{\mathrm{gen}}, c_j^{\mathrm{gt}})\} & \text{if } i>0, j>0, \operatorname{Sim}(c_i^{\mathrm{gen}}, c_j^{\mathrm{gt}}) \geq \gamma \end{cases}$$

匹配后的说话者相似度和内容相似度取平均：

$$S_{\mathrm{combined}} = (S_{\mathrm{speaker}} + S_{\mathrm{content}}) / 2$$

对话召回率和精确率定义为：

$$\mathrm{Rec} = S_{\mathrm{combined}} / M, \quad \mathrm{Prec} = S_{\mathrm{combined}} / N$$

最终对话奖励为 F1 分数：

$$\mathcal{R}_D = 2 \cdot \mathrm{Prec} \cdot \mathrm{Rec} / (\mathrm{Prec} + \mathrm{Rec})$$

### 5.4 长度正则化奖励 R_L

长度正则化奖励对描述长度在 τ₁=2048 和 τ₂=4096 之间进行线性惩罚：

$$\mathcal{R}_L = \begin{cases} 1 - \frac{\mathrm{len}(S_{\mathrm{gen}}) - \tau_1}{\tau_2 - \tau_1}, & \text{if } \tau_1 \leq \mathrm{len}(S_{\mathrm{gen}}) < \tau_2 \end{cases}$$

总奖励为三项之和：$\mathcal{R} = \mathcal{R}_C + \mathcal{R}_D + \mathcal{R}_L$。

## 实验与分析


### 6.1 主要结果

Table 1 展示了 AVoCaDO 在视听视频描述基准上的主要结果：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vjEl1PuIDE_AVoCaDO_An_Audi/figures/004_Table_1.jpg]]
*Table 1: Model performance on the audiovisual video captioning benchmarks. “A” and “V” refer to the audio and visual modalities, respectively. The results presented above are reproduced using the official code. Note that the video-SALMONN-2 testset originally employed GPT-3.54as the judge model, which occasionally led to misjudgments. To ensure more reliable evaluation, we uniformly replaced it with GPT-4.1. ∗Concurrent works with us*

| 模型 | video-SALMONN-2 Total↓ | UGC-VideoCap Avg.↑ | UGC-VideoCap Audio↑ |
|------|------------------------|---------------------|---------------------|
| AVoCaDO (Ours) | **37.3** | **73.2** | **73.0** |
| video-SALMONN-2 | 42.1 | 70.3 | 69.0 |
| Gemini-2.5-Pro | - | 72.6 | 72.0 |
| Qwen3-Omni-Instruct (30B-A3B) | 39.8 | 72.0 | 71.5 |

在问答评估中 (Table 2)，AVoCaDO 在 Daily-Omni 和 WorldSense 上分别达到 50.1 和 25.7，大幅领先 video-SALMONN-2 (29.9/18.2) 和 Qwen3-Omni-Instruct (29.9/18.2)。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vjEl1PuIDE_AVoCaDO_An_Audi/figures/005_Table_2.jpg]]
*Table 2: QA performance by Gemini-2.5-Pro based on textual captions. To mitigate answer guessing when the caption lacks necessary information, the model is instructed to refrain from answering such questions, which are then marked as incorrect samples*

在纯视觉设置下 (Table 3)，AVoCaDO 在 VDC Detailed 上达到 47.4 Acc，在 DREAM-1K 上达到 35.9 F1，展现出竞争性能。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vjEl1PuIDE_AVoCaDO_An_Audi/figures/006_Table_3.jpg]]
*Table 3: Model performance on the VDC Detailed subset and DREAM-1K, which evaluate captions in visual-only settings*

在音乐和通用声音场景的 QA 评估中 (Table 5)，AVoCaDO 在 AVQA、MUSIC-AVQA 和 MUSIC-AVQA-v2.0 上分别达到 71.8、62.0 和 45.8，显著优于 Qwen2.5-Omni (66.6/55.8/29.2)。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vjEl1PuIDE_AVoCaDO_An_Audi/figures/014_Table_5.jpg]]
*Table 5: QA performance by Gemini-2.5-Pro based on textual captions in music and general sound scenarios. To mitigate answer guessing when the caption lacks necessary information, the model is instructed to refrain from answering such questions, which are then marked as incorrect*

### 6.2 消融实验

Table 4 的消融实验揭示了各组件的关键贡献：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vjEl1PuIDE_AVoCaDO_An_Audi/figures/007_Table_4.jpg]]
*Table 4: mance for visual-only videos. As reported in Tab. 3, AVoCaDO also demonstrates competitive performance in this setting. Table 4: Ablation study on our post-training pipeline. “Dlg. F1” represents the metric of dialogue quality, computed as in Eq. 7. “RepCol” indicates the ratio of generations exhibiting repetition collapse. AVoCaDO-SFT-2K∗ refers to the model further fine-tuned on AVoCaDO-SFT using the same 2K samples employed during the GRPO phase*

- **AVoCaDO-SFT 阶段**显著提升基准分数、对话质量和减少重复坍塌
- **对话奖励 R_D** 使对话 F1 在两个基准上均提升超过 2%
- **检查表奖励 R_C** 显著降低 video-SALMONN-2 测试集上的总错误率
- **长度正则化奖励 R_L** 不仅显著缓解重复坍塌，还提升了其他指标
- 在相同 2K 数据上仅进行 SFT (AVoCaDO-SFT-2K) 无显著提升，甚至在 video-SALMONN-2 测试集上出现退化，证明 GRPO 奖励函数是性能提升的关键

### 6.3 训练细节

- SFT 阶段：2 个 epoch，batch size 128，学习率 2e-5
- GRPO 阶段：1 个 epoch，batch size 64，学习率 1e-5，每个查询采样 8 个响应，温度 1.0，KL 系数 β=0.04
- 视频和音频编码器冻结，仅更新适配器和 LLM 主干
- 视频采样率 2 fps，帧分辨率最大 512×28×28 像素
- 训练在 16 张 NVIDIA H200 GPU 上进行，评估在 NVIDIA H20 GPU 上进行

### 6.4 公平性说明

- 所有评估均使用 GPT-4.1 作为评判模型，替代了 video-SALMONN-2 测试集原始使用的 GPT-3.5，以确保评估更可靠
- 在 QA 评估中，当描述缺乏必要信息时，模型被指示拒绝回答，此类问题被标记为错误，以减少猜测偏差
- 训练数据来源多样，覆盖多种视听场景，但未明确讨论数据集的偏见或公平性分析

## 方法谱系与知识库定位

AVoCaDO 属于视听视频描述生成领域，其方法谱系可定位如下：

- **基础模型**：基于 Qwen2.5-Omni-7B，该模型通过交错令牌序列实现视听信号对齐，属于多模态大语言模型 (MLLM) 家族
- **数据构建**：采用两阶段描述生成策略（先模态特定描述，再融合），区别于直接联合生成方法
- **后训练策略**：结合 SFT 和 GRPO 强化学习，区别于仅 SFT 或仅 DPO 的方法
- **奖励函数设计**：三项互补奖励（检查表、对话、长度正则化），区别于单一或简单奖励函数

与同类方法相比，AVoCaDO 在以下方面具有独特优势：
- 相比 video-SALMONN-2（需六轮 DPO 后训练），AVoCaDO 通过 GRPO 实现更高效的优化
- 相比 UGC-VideoCaptioner（限于短视频），AVoCaDO 支持更长的视频（最长 100 秒）
- 相比 Gemini-2.5-Pro（商业闭源），AVoCaDO 作为开源模型在 UGC-VideoCap 上实现了超越

**局限性**：模型可能生成幻觉内容；在实时应用中延迟和准确性之间存在权衡；训练数据限于 100 秒以内的视频；32K 上下文窗口限制了可处理的视频长度和细节。

**开放问题**：如何有效检测和减轻生成描述中的幻觉？如何通过令牌压缩或效率优化策略平衡实时场景下的延迟和准确性？AVoCaDO 在更长视频（超过 100 秒）上的表现如何？三项奖励函数的权重是否需要针对不同场景进行自适应调整？

## 原文 PDF

![[paperPDFs/ICLR_2026/AVoCaDO_An_Audiovisual_Video_Captioner_Driven_by_Temporal_Orchestration.pdf]]

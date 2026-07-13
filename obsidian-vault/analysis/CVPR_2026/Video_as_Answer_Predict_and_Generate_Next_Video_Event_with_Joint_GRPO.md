---
title: "Video-as-Answer: Predict and Generate Next Video Event with Joint-GRPO"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Video_as_Answer_Predict_and_Generate_Next_Video_Event_with_Joint_GRPO.pdf
project_link: null
code_link: "https://github.com/KlingTeam/VANS"
aliases:
- VVAAS
- Video-as-Answer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Joint-GRPO：通过联合奖励函数驱动VLM与VDM协同优化的两阶段强化学习策略，迫使VLM内化VDM的可视化能力与约束，同时迫使VDM忠实遵循VLM的语义锚点描述。
primary_logic: 将VLM与VDM视为一个协同单元，通过联合奖励实现共同引导（co-steering）：阶段一使VLM的推理变得可视化友好（visually grounded），阶段二使VDM的生成忠实于锚点描述与输入视觉上下文，从而弥合语义到视觉的鸿沟。
claims:
- Joint-GRPO显著超越SFT基线：ROUGE-L从0.2812提升至0.3631（相对提升29.1%），CLIP-V从0.7655提升至0.8021
- 两阶段设计至关重要：仅使用阶段一会导致语义偏离，all-in-one变体因奖励模糊性导致优化不稳定
- 各奖励组件均为必要：移除r_t1降低描述精度，移除r_v1损害视觉一致性，移除r_c2导致静态帧（reward hacking），移除r_v2降低输出连贯性
- Procedural Benchmarks 上 ROUGE-L = 0.3631
---

# Video-as-Answer: Predict and Generate Next Video Event with Joint-GRPO

> [!tip] 核心洞察
> 将VLM与VDM视为一个协同单元，通过联合奖励实现共同引导（co-steering）：阶段一使VLM的推理变得可视化友好（visually grounded），阶段二使VDM的生成忠实于锚点描述与输入视觉上下文，从而弥合语义到视觉的鸿沟。

| 字段 | 内容 |
|------|------|
| 中文题名 | 视频即答案：基于联合GRPO的下一个视频事件预测与生成 |
| 英文题名 | Video-as-Answer: Predict and Generate Next Video Event with Joint-GRPO |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16669) · [Code](https://github.com/KlingTeam/VANS) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VANS (Video-as-Answer System) |
| Dataset | Procedural Benchmarks, Predictive Benchmarks |

> [!tip] 效果简介
> - Procedural Benchmarks 上，ROUGE-L 0.3631 vs 0.2802 (Gemini-FilmWeaver) (+0.0829 (29.6%))；FVD 78.32 vs 110.54 (Gemini-FilmWeaver) (-32.22 (29.1%))；CLIP-V 0.8021 vs 0.7102 (Gemini-FilmWeaver) (+0.0919 (12.9%))。
> - Predictive Benchmarks 上，FVD 86.85 vs 118.27 (Gemini-FilmWeaver) (-31.42 (26.6%))；CLIP-V 0.7872 vs 0.6709 (Gemini-FilmWeaver) (+0.1163 (17.3%))。

## 概要

**问题与瓶颈**：视频下一事件预测与生成（VNEP）要求模型根据输入视频和问题，预测并生成视觉一致、语义忠实的后续事件视频。现有方案主要沿两条路径展开：一是端到端的统一视频生成模型，二是将视觉语言模型（VLM）与视频扩散模型（VDM）级联。后者的核心瓶颈在于**语义到视觉的跨模态对齐鸿沟**——VLM生成的文本描述虽然语言正确，但可能视觉上不可行或VDM难以执行；VDM则面临协调VLM特定描述与输入视觉上下文两个条件信号的挑战，导致语义忠实度与视觉一致性难以兼顾。

**核心方法**：本文提出 **VANS（Video-as-Answer System）**，以“视频即答案”的理念将VNEP重新定义为视频问答任务。其核心创新是 **Joint-GRPO**——一种通过联合奖励函数驱动VLM与VDM协同优化的两阶段强化学习策略。阶段一“可视化友好VLM调优”迫使VLM内化VDM的可视化能力与约束，生成既准确又可被VDM执行的描述；阶段二“上下文忠实VDM适配”以改进后的VLM为冻结锚点模型，迫使VDM忠实遵循语义锚点描述并保持视觉一致性。这一共同引导（co-steering）机制有效弥合了语义到视觉的鸿沟。

**方法定位**：VANS属于VLM+VDM级联范式的强化学习增强方案，区别于标准GRPO仅优化单一模型的范式。与Video-GPT（Zhuang et al., arXiv 2025）、Omni-Video（Tan et al., arXiv 2025）等统一模型基线，以及TEMPURA-Wan（Cheng et al., arXiv 2025）、Gemini-FilmWeaver等级联基线相比，VANS通过联合奖励驱动的两阶段RL实现了VLM与VDM的深度协同。

**主要结果**：在程序性基准上，VANS（Joint-GRPO）的ROUGE-L达到0.3631，较最强基线Gemini-FilmWeaver（0.2802）提升29.6%；FVD降至78.32（对比110.54，降低29.1%）；CLIP-V达到0.8021（对比0.7102，提升12.9%）。在预测性基准上同样取得显著提升。消融实验证实两阶段设计、各奖励组件均为必要，且Joint-GRPO显著优于独立优化VLM或VDM的GRPO变体。人类评估中，VANS在语义正确性（4.7/5）、视觉一致性（4.6/5）和整体满意度上均获最高评分。



视频理解与生成领域正经历从“文本回答”到“视频回答”的范式转变。传统视觉问答（VQA）系统仅输出文本描述，在面对程序性（“如何操作？”）或预测性（“接下来会发生什么？”）问题时，文本回答往往缺乏直观性与可操作性——例如，用文字描述“取下口罩”的动作远不如直接生成一段演示视频来得清晰（Figure 2）。

### 任务定义：视频即答案

**VNEP（Video-Next-Event Prediction）** 任务将这一需求形式化：给定一段输入视频和一个自然语言问题，系统需预测并**生成**下一个视频事件作为回答。这要求模型同时具备两个核心能力：（1）基于视觉上下文进行时序推理，准确预测事件语义；（2）生成视觉连贯、语义忠实的输出视频。

### 现有方案的瓶颈：语义到视觉的跨模态对齐鸿沟

当前主流方案采用**级联流水线**架构——先由视觉语言模型（VLM）生成文本描述，再由视频扩散模型（VDM）根据该描述生成视频。这一范式面临根本性瓶颈：**语义到视觉的跨模态对齐鸿沟（semantic-to-visual gap）**。

具体而言，该鸿沟体现在两个层面：

1. **VLM的推理未考虑VDM的执行约束**：VLM生成的文本描述虽然在语言层面正确，但可能包含VDM难以可视化的内容（如过于抽象的动作、不合理的空间关系），导致生成的视频语义偏离或视觉质量下降。Figure 6中的定性对比印证了这一点——多个基线模型（如**Gemini-FilmWeaver**、**TEMPURA-Wan** (Cheng et al., arXiv 2025)）生成的caption虽语义正确，却因“视觉不友好”而无法被VDM忠实执行。

2. **VDM难以协调多重条件信号**：VDM需要同时遵循VLM的文本描述和输入视频的低层视觉线索（如物体身份、背景），这两个条件信号往往存在冲突。当文本描述与视觉上下文不一致时，VDM倾向于牺牲语义忠实度以维持视觉连贯性，或反之。

### 现有方法的不足

- **独立优化的级联方案**（如**Qwen-Wan**、**Gemini-Wan**）：VLM与VDM各自独立训练或微调，缺乏跨模态协同机制。VLM的优化目标仅关注文本准确性，VDM的优化目标仅关注视频质量，两者之间存在不可逾越的语义鸿沟。
- **统一模型方案**（如**Video-GPT** (Zhuang et al., arXiv 2025)、**Omni-Video** (Tan et al., arXiv 2025)）：试图用单一模型同时处理推理与生成，但受限于模型容量与训练数据，在预测精度与生成质量上均不及专门的级联方案。
- **标准强化学习方案**：若仅对VLM或VDM单独应用GRPO等RL策略，由于奖励信号仅反映单侧模型的表现，无法驱动跨模态对齐。消融实验（Table 2）证实，独立优化的GRPO变体（GRPO (VLM)、GRPO (VDM)、GRPO (VLM+VDM)）在CLIP-V指标上均显著低于Joint-GRPO。

### 本文动机

上述分析揭示了一个核心洞察：**弥合语义到视觉鸿沟的关键，在于将VLM与VDM视为一个协同单元进行联合优化**。VLM需要内化VDM的可视化能力与约束，生成“可视化友好”的描述；VDM则需要忠实遵循VLM提供的语义锚点，同时保持与输入视频的视觉一致性。为此，本文提出**VANS（Video-as-Answer System）** 及其核心策略**Joint-GRPO**——一种通过联合奖励函数驱动VLM与VDM协同优化的两阶段强化学习框架，从根本上解决跨模态对齐问题。



## 核心方法与创新机理

VANS 的核心创新在于提出了 **Joint-GRPO** 策略，通过联合奖励函数驱动视觉语言模型（VLM）与视频扩散模型（VDM）的协同优化，从根本上解决了“语义到视觉的跨模态对齐鸿沟”这一瓶颈问题。传统级联方案中，VLM 生成的文本描述虽语言正确，却可能视觉上不可行或 VDM 难以执行；VDM 则面临协调 VLM 特定描述与输入视觉上下文两个条件信号的挑战，导致语义忠实度与视觉一致性难以兼顾。Joint-GRPO 将 VLM 与 VDM 视为一个协同单元，通过两阶段强化学习实现共同引导（co-steering），迫使 VLM 内化 VDM 的可视化能力与约束，同时迫使 VDM 忠实遵循 VLM 的语义锚点描述。

### 关键创新点（Changed Slots）

**1. VLM 训练范式：从标准 SFT 到可视化友好 VLM 调优**

基线方法对 VLM 采用标准监督微调（SFT），仅优化文本准确性，忽略了描述的可执行性。VANS 在 Joint-GRPO 阶段一引入**可视化友好 VLM 调优**：冻结 VDM，仅优化 VLM 策略 $\pi_{\text{VLM}}$，通过联合奖励函数 $r_1$ 同时考量格式奖励（$r_f$）、文本保真度（$r_{t1}$）和视频保真度（$r_{v1}$），使 VLM 生成的 caption 既准确又可被 VDM 成功执行。消融实验证实，移除 $r_{t1}$ 导致描述精度下降（ROUGE-L 从 0.3631 降至 0.3498），移除 $r_{v1}$ 则损害视觉一致性（CLIP-V 从 0.7803 降至 0.7668）。

**2. VDM 训练范式：从独立 SFT 到上下文忠实 VDM 适配**

基线 VDM 采用标准 SFT 独立优化视频生成，缺乏对 VLM 语义锚点的显式对齐。VANS 在 Joint-GRPO 阶段二提出**上下文忠实 VDM 适配**：以阶段一改进后的 VLM 为冻结锚点模型，仅优化 VDM 策略 $\pi_{\text{VDM}}$，通过联合奖励 $r_2$ 平衡视频保真度（$r_{v2}$）与语义对齐（$r_{c2}$），迫使 VDM 在保持视觉连续性的同时忠实遵循锚点描述。消融实验揭示了关键因果机制：移除 $r_{c2}$ 会导致 reward hacking——VDM 生成静态帧以规避语义对齐要求（CLIP-V 降至 0.7921）；移除 $r_{v2}$ 则降低输出连贯性（CLIP-V 降至 0.7887）。

**3. 跨模态对齐策略：从独立优化到联合奖励驱动的两阶段 RL**

基线方案中 VLM 与 VDM 独立优化，存在难以弥合的语义到视觉鸿沟。Joint-GRPO 的核心洞察在于**联合奖励驱动的两阶段协同**：阶段一使 VLM 的推理变得可视化友好（visually grounded），阶段二使 VDM 的生成忠实于锚点描述与输入视觉上下文。这一设计的必要性通过对比实验得到强验证：仅使用阶段一会导致语义偏离（FVD 80.23 vs 完整两阶段 78.32）；all-in-one 变体因奖励模糊性导致优化不稳定（ROUGE-L 0.3577 vs 完整两阶段 0.3631）；独立优化 VLM 或 VDM 的 GRPO 变体，或将两者独立优化结果级联，均不及 Joint-GRPO 的联合优化效果（CLIP-V 最高仅 0.7798 vs Joint-GRPO 的 0.8021）。

### 创新效果量化

Joint-GRPO 相较于 SFT 基线实现了显著提升：ROUGE-L 从 0.2812 提升至 0.3631（相对提升 29.1%），CLIP-V 从 0.7655 提升至 0.8021。相较于最强级联基线 Gemini-FilmWeaver，VANS 在程序性基准上 FVD 降低 29.1%（78.32 vs 110.54），CLIP-T 提升 37.9%（0.3824 vs 0.2773），充分验证了联合优化策略相较于独立优化的根本优势。



VANS（Video-as-Answer System）构建了一条**VLM推理→VDM生成**的级联流水线，将“下一个视频事件预测与生成”（VNEP）形式化为一个以视频为答案的跨模态生成任务。其核心设计理念在于：将VLM与VDM视为一个协同单元，通过联合奖励驱动两阶段强化学习（Joint-GRPO），迫使VLM内化VDM的可视化能力与约束，同时迫使VDM忠实遵循VLM的语义锚点描述，从而弥合语义到视觉的跨模态对齐鸿沟。

### 流水线模块与数据流

系统由四个核心模块串联构成，数据流沿“视觉编码→语义推理→条件生成”方向单向传递：

1. **ViT视觉编码器**：提取输入视频的高层视觉特征（ViT features），供VLM进行指令条件推理。

2. **VLM（Qwen2.5-VL-3B）**：接收ViT特征与用户问题（程序性“如何做？”或预测性“接下来会发生什么？”），执行指令条件推理，生成描述下一个事件的文本caption。该caption作为VDM的语义引导信号。

3. **VAE Tokenizer**：从输入视频中采样n帧，编码为VDM条件潜在空间中的tokens，实现细粒度视觉对应。这些tokens被拼接到VDM的条件潜在空间中，提供低层视觉线索。

4. **VDM（Wan-2.1-1.3B）**：以VLM生成的caption和VAE tokens为双重条件，动态关注并保留输入视频中的相关视觉元素（如物体身份、背景），生成视觉一致且语义忠实的输出视频。

### 训练范式：从SFT到Joint-GRPO

VANS的训练分为两个阶段，其关键变革在于将标准监督微调（SFT）替换为**Joint-GRPO联合强化学习**：

- **SFT基线**：VLM与VDM独立进行标准SFT——VLM仅优化文本准确性，VDM独立优化视频生成质量。这种独立优化导致语义到视觉的鸿沟：VLM生成的描述可能语言正确但视觉上不可行，VDM则难以协调VLM的特定描述与输入视觉上下文两个条件信号。

- **Joint-GRPO阶段一（可视化友好VLM调优）**：冻结VDM，仅优化VLM策略 $\pi_{\text{VLM}}$。联合奖励函数 $r_1$ 由三部分加权组成：格式奖励 $r_f$（ROUGE-L）、文本保真度奖励 $r_{t1}$（ROUGE-L，与GT caption对齐）、视频保真度奖励 $r_{v1}$（CLIP Similarity，生成视频与GT视频对齐）。这迫使VLM生成既语义准确又**可被VDM可视化执行**的描述。

- **Joint-GRPO阶段二（上下文忠实VDM适配）**：以阶段一改进后的VLM为冻结锚点模型，仅优化VDM策略 $\pi_{\text{VDM}}$。VLM首先生成锚点caption $s_{\text{anchor}}$，VDM以此与VAE tokens为条件生成视频。联合奖励函数 $r_2$ 由视频保真度奖励 $r_{v2}$（CLIP Similarity）和语义对齐奖励 $r_{c2}$（CLIPScore，生成视频与锚点caption对齐）加权组成。这迫使VDM忠实遵循语义锚点，同时保持视觉连贯性。

### 联合优化的必要性

独立优化变体的消融实验（Table 2）证实了联合设计的必要性：仅对VLM或VDM单独应用GRPO，或将二者独立优化结果级联（GRPO VLM+VDM），其CLIP-V指标（0.7671–0.7798）均显著低于Joint-GRPO的0.8021。这表明，只有当VLM与VDM在联合奖励下协同优化时，才能有效弥合语义到视觉的鸿沟。

此外，all-in-one变体（同时训练VLM和VDM）因奖励模糊性导致优化不稳定，ROUGE-L降至0.3577（vs. Joint-GRPO的0.3631），验证了两阶段设计的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/004_Figure_4.jpg]]
*Figure 4: Overall architecture of VANS*



### 系统流水线模块

VANS 由四个核心模块构成端到端流水线（Figure 4），实现从输入视频到下一事件视频生成的完整链路：

**VLM（Qwen2.5-VL-3B）** 作为指令条件推理器，接收输入视频的高层 ViT 视觉特征与用户问题，生成描述下一事件的文本 caption，该 caption 作为 VDM 的语义引导信号。其核心职责是将“预测下一事件”这一抽象任务转化为可执行的文本锚点。

**VDM（Wan-2.1-1.3B）** 作为视频生成器，以 VLM 生成的 caption 和输入视频的低层视觉线索为双重条件。具体而言，从输入视频中采样 $n$ 帧，经 VAE tokenizer 编码为条件潜在空间中的 tokens，与 caption 的语义条件共同引导去噪过程，生成视觉一致且语义忠实的输出视频。

**ViT 视觉编码器** 提取输入视频的高层语义特征，作为 VLM 的视觉输入，使其能够理解场景上下文并做出合理的事件推理。

**VAE Tokenizer** 将采样输入帧编码为 VDM 条件潜在空间中的细粒度 tokens，实现输出视频与输入视频在像素级视觉元素（如物体 ID、背景）上的对应与保持。

### Joint-GRPO 核心公式

Joint-GRPO 的核心在于通过联合奖励函数驱动 VLM 与 VDM 的两阶段协同优化。其基础是 GRPO（Group Relative Policy Optimization）的归一化优势函数与策略优化目标。

**GRPO 归一化优势**：对于每组 $G$ 条轨迹，第 $i$ 条轨迹的归一化优势为：

$$\tilde{A}_i = \frac{r_i - \bar{r}}{\sigma_r}, \quad \bar{r} = \frac{1}{G} \sum_{j=1}^{G} r_j, \quad \sigma_r = \sqrt{\frac{1}{G} \sum_{j=1}^{G} (r_j - \bar{r})^2}$$

其中 $\bar{r}$ 为组内平均奖励，$\sigma_r$ 为标准差。该归一化使优势函数尺度稳定，避免奖励绝对值波动对优化方向的干扰。

**GRPO 优化目标**：

$$J(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \frac{1}{T_i} \sum_{t=0}^{T_i-1} \min \left( r_t^i(\theta) \tilde{A}_i, \operatorname{clip}(r_t^i(\theta), 1-\epsilon, 1+\epsilon) \tilde{A}_i \right) \right) - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right]$$

其中 $r_t^i(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\text{old}}(a_t|s_t)}$ 为概率比率，$\operatorname{clip}(\cdot, 1-\epsilon, 1+\epsilon)$ 将比率裁剪至 $[1-\epsilon, 1+\epsilon]$ 区间以防止策略更新过大。$\beta D_{\mathrm{KL}}$ 项惩罚当前策略 $\pi_\theta$ 与参考策略 $\pi_{\text{ref}}$ 的 KL 散度，保证训练稳定性。

**阶段一联合奖励（VLM 优化）**：

$$r_1(s_i, v_{\mathrm{out}}^i) = \lambda_f r_f(s_i) + \lambda_{t1} r_{t1}(s_i, s_{\mathrm{gt}}) + \lambda_{v1} r_{v1}(v_{\mathrm{out}}^i, v_{\mathrm{gt}})$$

- $r_f(s_i)$：格式奖励，基于 ROUGE-L 衡量 caption 格式规范性
- $r_{t1}(s_i, s_{\mathrm{gt}})$：文本保真度奖励，基于 ROUGE-L 衡量 caption 与 GT 描述的语义一致性
- $r_{v1}(v_{\mathrm{out}}^i, v_{\mathrm{gt}})$：视频保真度奖励，基于 CLIP Similarity 衡量 VDM 以当前 caption 为条件生成视频的质量
- $\lambda_f, \lambda_{t1}, \lambda_{v1}$ 为各奖励项的权重系数

该奖励设计的核心洞察是：VLM 的 caption 质量不仅取决于文本准确性，还取决于其能否被 VDM 有效执行。$r_{v1}$ 迫使 VLM 内化 VDM 的可视化能力约束，生成“可视化友好”的描述。

**阶段二联合奖励（VDM 优化）**：

$$r_2(v_{\mathrm{out}}^i, s_{\mathrm{anchor}}) = \lambda_{v2} r_{v2}(v_{\mathrm{out}}^i, v_{\mathrm{gt}}) + \lambda_{c2} r_{c2}(v_{\mathrm{out}}^i, s_{\mathrm{anchor}})$$

- $r_{v2}(v_{\mathrm{out}}^i, v_{\mathrm{gt}})$：视频保真度奖励，基于 CLIP Similarity 确保输出视频视觉质量与连续性
- $r_{c2}(v_{\mathrm{out}}^i, s_{\mathrm{anchor}})$：语义对齐奖励，基于 CLIPScore 衡量生成视频与冻结 VLM（阶段一优化后）输出的锚点 caption $s_{\mathrm{anchor}}$ 的语义一致性
- $\lambda_{v2}, \lambda_{c2}$ 为权重系数

阶段二的关键在于：VLM 作为冻结锚点模型，提供稳定的语义锚点 $s_{\mathrm{anchor}}$；VDM 在 $r_{c2}$ 的驱动下必须忠实遵循该锚点描述，同时 $r_{v2}$ 防止 reward hacking（如生成静态帧以骗取高语义对齐分数）。两阶段递进设计避免了 all-in-one 联合训练中因奖励模糊性导致的优化不稳定。

### 补充图表

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/005_Figure_5.jpg]]
*Figure 5: Comparison of standard GRPO with Joint-GRPO. While standard GRPO optimizes a single model at a time, our Joint-GRPO coordinates their optimization under a joint reward function*

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/008_Table_2.jpg]]
*Table 2: Quantitative results of ablation study*



## 实验与关键发现

### 主实验结果

VANS (Joint-GRPO) 在程序性（Procedural）和预测性（Predictive）两类基准上全面超越现有最强级联基线 **Gemini-FilmWeaver**，验证了联合强化学习策略对跨模态对齐的有效性。Table 1 报告了关键指标对比。

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison with baseline models on Video-Next-Event Prediction*

在程序性基准上，VANS 的文本保真度指标 ROUGE-L 达到 **0.3631**，较 Gemini-FilmWeaver 的 0.2802 提升 29.6%；视觉保真度指标 CLIP-V 达到 **0.8021**，较基线的 0.7102 提升 12.9%。视频质量指标 FVD 从 110.54 降至 **78.32**（降幅 29.1%），CLIP-T 从 0.2773 提升至 **0.3824**（升幅 37.9%）。这表明 Joint-GRPO 不仅使 VLM 生成的文本描述更准确，同时使 VDM 生成的视频在视觉上与输入上下文更一致。

在预测性基准上，VANS 同样表现出显著优势：FVD 从 118.27 降至 **86.85**（降幅 26.6%），CLIP-V 从 0.6709 提升至 **0.7872**（升幅 17.3%）。预测性任务对模型的时序推理能力要求更高，VANS 的大幅领先表明 Joint-GRPO 阶段一的可视化友好调优有效提升了 VLM 对动态事件演化的推理质量。

值得注意的是，**Qwen-Wan** 和 **Gemini-Wan** 等直接级联基线（VLM 输出直接送入 VDM）在 CLIP-V 上仅约 0.73-0.74，远低于 VANS。这印证了核心瓶颈：未经对齐优化的 VLM 输出虽在语言层面正确，但 VDM 难以将其转化为视觉可行的视频。**TEMPURA-Wan**（Cheng et al., arXiv 2025）虽对 VLM 进行了 NEP 微调，但因其独立优化策略，CLIP-V 仍仅为 0.7553，说明仅改进 VLM 的文本推理不足以弥合语义-视觉鸿沟。Table 4 进一步排除了数据优势的混淆：将基线模型在 VANS-Data-100K 上微调后，其性能仍显著低于 VANS，确认架构设计（Joint-GRPO）是性能提升的主要来源。

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/013_Table_4.jpg]]
*Table 4: Results on procedural VNEP. The comparison with finetuned baselines (*) shows that our architectural design, rather than data advantage, is the primary source of improvement*

人类评估结果（Table 5，30 名评估者，1-5 分制）从语义正确性、视觉一致性和整体满意度三个维度进一步验证：VANS (Joint-GRPO) 在所有指标上均获最高分，与自动评估结论一致。

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/016_Table_5.jpg]]
*Table 5: Human evaluation results (scale: 1-5). Our VANS with Joint-GRPO achieves the highest scores across all criteria*

### 消融实验

Table 2 和 Figure 7 系统验证了 Joint-GRPO 各组件的必要性。

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/009_Figure_7.jpg]]
*Figure 7: Visualization Results of ablation studies. Key regions are highlighted with yellow boxes: the left example shows degradation in the “mask removal” action completion without*

**两阶段设计的必要性。** 仅使用阶段一（Stage 1 only）可提升 ROUGE-L 至 0.3631，但 FVD 高达 80.23，且生成的视频存在语义偏离——VLM 虽学会了生成可视化友好的描述，但 VDM 未经适配，无法忠实地执行这些描述。仅使用阶段二则因 VLM 未经过可视化友好调优，其锚点描述仍可能包含 VDM 难以执行的内容，导致整体性能不佳。All-in-one 变体（同时训练 VLM 和 VDM）因奖励模糊性导致优化不稳定，ROUGE-L 降至 0.3577，FVD 升至 81.01，验证了分阶段优化的必要性。

**独立 GRPO 的局限性。** 对 VLM 或 VDM 单独应用 GRPO（GRPO (VLM)、GRPO (VDM)），或将其独立优化结果级联（GRPO (VLM+VDM)），CLIP-V 分别为 0.7798、0.7671、0.7703，均显著低于 Joint-GRPO 的 0.8021。这证明仅优化单一模型无法建立跨模态的协同对齐——VLM 和 VDM 必须作为一个联合单元被共同引导。

**各奖励组件的作用。** 阶段一移除文本保真度奖励 $r_{t1}$（w/o $r_{t1}$）导致 ROUGE-L 从 0.3631 降至 0.3498，Figure 7 左例显示模型未能预测“摘下面膜”这一关键动作，caption 精度明显退化。移除视频保真度奖励 $r_{v1}$（w/o $r_{v1}$）使 CLIP-V 从 0.7803 降至 0.7668，视觉一致性受损。阶段二移除语义对齐奖励 $r_{c2}$（w/o $r_{c2}$）导致 reward hacking——VDM 为追求视频保真度而生成静态帧，CLIP-V 虽为 0.7921，但语义内容严重缺失（Figure 7 右例）。移除视频保真度奖励 $r_{v2}$（w/o $r_{v2}$）使 CLIP-V 从 0.8021 降至 0.7887，输出连贯性下降。

### 失败模式与局限性

尽管 VANS 取得了显著性能提升，实验和分析揭示了以下局限：

1. **推理耗时较长。** caption 生成约需 4 秒，视频生成约需 35 秒，总计约 39 秒，不适用于实时交互场景。这源于 VDM 的多步去噪推理和 VLM 的自回归生成特性。

2. **评估基准规模有限。** 程序性和预测性基准各采样 400 个样本，虽严格与训练集分离，但可能不足以覆盖广泛的 VNEP 场景（如体育、医疗操作等）。更大规模、更多样化的评估仍需探索。

3. **数据依赖与模型偏差。** VANS-Data-100K 的 QA 生成依赖 Gemini-2.5-Flash 模拟问题与链式推理，可能存在模型偏差。此外，Joint-GRPO 训练依赖从 1K 高质样本中手动筛选的 GT 视频-caption 对，限制了可扩展性。

4. **奖励设计的局限性。** 当前奖励函数依赖 ROUGE-L 和 CLIP Similarity 等自动指标，这些指标虽与人类判断相关，但并非完美代理。例如，$r_{c2}$ 使用 CLIPScore 衡量语义对齐，可能对细粒度动作差异不够敏感，导致 Figure 7 中移除 $r_{c2}$ 时出现静态帧这种 reward hacking 行为。

### 训练动态

Figure 9 展示了 Joint-GRPO 的训练曲线。阶段一（VLM 调优）中，格式奖励 $r_f$ 快速收敛至接近满分，表明 VLM 迅速学会了输出结构化 caption。文本保真度奖励 $r_{t1}$ 和视频保真度奖励 $r_{v1}$ 在初期波动后稳步上升，反映了 VLM 逐步内化 VDM 可视化能力的过程。阶段二（VDM 适配）中，视频保真度奖励 $r_{v2}$ 和语义对齐奖励 $r_{c2}$ 呈现协同上升趋势，验证了联合奖励设计使 VDM 在保持视觉质量的同时忠实于锚点描述。训练曲线未出现明显的奖励退化或发散，表明两阶段优化策略具有良好的稳定性。

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/012_Figure_9.jpg]]
*Figure 9: Training curves of Joint-GRPO: (a) format reward*

### 补充图表

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/007_Figure_6.jpg]]
*Figure 6: Visual comparison on VNEP. Captions are color-coded: green (correct), red (incorrect), blue (semantically correct but visually unfriendly). Yellow boxes highlight key regions. Baselines often fail in event prediction or visual consistency. Our SFT model improves reasoning but retains errors like semantic hallucination (predicting non-existent inreview in Case 1) and action misalignment (“adding cheese” yields pouring in Case 2). Joint-GRPO addresses both issues, enhancing model capability (correctly identifying document relationships and maintaining character appearance in Case 1) and fine-grained alignment (“sprinkle cheese” matching the GT “shower” in Case 2)*

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/003_Figure_3.jpg]]
*Figure 3: Data curation pipeline of VANS-Data-100K, which processes raw videos through shot splitting, clip selection, and QA generation to produce high-quality data for both procedural and predictive Video-Next-Event Prediction*

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/014_Figure_10.jpg]]
*Figure 10: Visual comparison results on UI2V-Bench*

![[assets/figures/papers/paper_list_l2711_https_arxiv_org_abs_2511_16669/figures/002_Figure_2.jpg]]
*Figure 2: Video answer (our VANS) versus text-only answer (Gemini) on a procedural question. Video answer provides an intuitive and customized response by demonstrating the action directly, while text-only answer falls short in clarity*



## 定位与知识库关联

### 任务定位：视频作为答案的下一事件预测

VANS 解决的是**视频下一事件预测与生成**（Video Next-Event Prediction, VNEP）任务：给定一段输入视频和一个程序性（“如何做？”）或预测性（“接下来会发生什么？”）问题，模型需要预测并直接生成下一事件的视频作为答案。这与传统的文本回答或纯视频预测范式形成根本差异——VANS 将视频本身作为答案的载体，要求生成结果同时满足语义忠实性（事件预测正确）和视觉一致性（与输入视频连贯衔接）。

### 基线谱系与对比定位

论文构建了从轻量级到重量级的基线对比体系，覆盖三类方法：

**视频扩展基线**：Video-GPT（Zhuang et al., arXiv 2025）和 Omni-Video（Tan et al., arXiv 2025）属于统一模型范式，试图在单一模型中同时处理理解和生成。但这类方法在 VNEP 任务上表现不佳——Video-GPT 的 FVD 高达 251.99，CLIP-V 仅 0.5683，说明统一架构在细粒度事件预测与视觉连贯性之间存在严重的注意力分散问题。

**级联流水线基线**：Qwen-Wan、TEMPURA-Wan（Cheng et al., arXiv 2025）、Gemini-Wan 和 Gemini-FilmWeaver 均采用 VLM + VDM 的级联范式。其中 Gemini-FilmWeaver 作为最强级联基线，在程序性基准上达到 ROUGE-L 0.2802、FVD 110.54、CLIP-V 0.7102。这些级联方法的核心瓶颈在于：VLM 和 VDM 各自独立优化，VLM 生成的文本描述虽然语言正确，但可能视觉上不可行或 VDM 难以执行——这正是 verified_analysis 所揭示的**语义到视觉的跨模态对齐鸿沟**（semantic-to-visual gap）。

**VANS 的定位**：VANS 同样采用 VLM（Qwen2.5-VL-3B）+ VDM（Wan-2.1-1.3B）的级联架构，但通过 Joint-GRPO 将两个模型作为协同单元进行联合优化，而非简单的独立训练后拼接。这一设计使 VANS 在程序性基准上达到 ROUGE-L 0.3631（相对 Gemini-FilmWeaver 提升 29.6%）、FVD 78.32（降低 29.1%）、CLIP-V 0.8021（提升 12.9%），在预测性基准上同样全面领先。

### 核心技术贡献：Joint-GRPO 的因果机制

Joint-GRPO 的核心洞察是将 VLM 与 VDM 视为一个协同单元，通过联合奖励实现**共同引导**（co-steering）。其因果机制可分解为两个阶段：

**阶段一——可视化友好 VLM 调优**：传统 SFT 仅优化 VLM 的文本准确性，导致生成的 caption 可能在语言层面正确但视觉上不可执行。Joint-GRPO 阶段一在 VDM 冻结的条件下，通过联合奖励 $r_1$（包含格式奖励 $r_f$、文本保真度奖励 $r_{t1}$ 和视频保真度奖励 $r_{v1}$）迫使 VLM 内化 VDM 的可视化能力与约束。消融实验提供了强因果证据：移除 $r_{t1}$ 导致 ROUGE-L 从 0.3631 降至 0.3498，且出现“mask removal”动作预测失败的可视化退化（Figure 7）；移除 $r_{v1}$ 使 CLIP-V 从 0.7803 降至 0.7668，损害视觉一致性。

**阶段二——上下文忠实 VDM 适配**：以阶段一改进后的 VLM 为冻结锚点模型，通过联合奖励 $r_2$（包含视频保真度奖励 $r_{v2}$ 和语义对齐奖励 $r_{c2}$）迫使 VDM 忠实遵循锚点描述并保持与输入视频的视觉连贯性。消融实验同样揭示了清晰的因果链条：移除 $r_{c2}$ 导致 reward hacking（VDM 生成静态帧以获取高视觉保真度分数），CLIP-V 降至 0.7921；移除 $r_{v2}$ 降低输出连贯性，CLIP-V 降至 0.7887。

**两阶段设计的必要性**：all-in-one 变体（同时训练 VLM 和 VDM）因奖励模糊性导致优化不稳定，ROUGE-L 仅 0.3577，FVD 升至 81.01。仅使用阶段一虽然 caption 精度尚可（ROUGE-L 0.3631），但 FVD 恶化至 80.23，说明缺乏阶段二的 VDM 适配会导致语义偏离。这验证了两阶段递进式优化的结构必要性。

### 与 GRPO 系列方法的关系

标准 GRPO（Group Relative Policy Optimization）通常用于优化单一模型。VANS 的 Joint-GRPO 将 GRPO 扩展到跨模型协同优化场景，其关键创新在于**联合奖励函数的设计**：不是简单地将 GRPO 分别应用于 VLM 和 VDM，而是通过共享奖励信号建立两个模型之间的优化耦合。消融实验中的 GRPO (VLM)、GRPO (VDM) 和 GRPO (VLM+VDM) 变体分别仅达到 CLIP-V 0.7798、0.7671 和 0.7703，均显著低于 Joint-GRPO 的 0.8021，证明了联合奖励驱动的协同优化优于独立或级联的 GRPO 应用。

### 适用边界与局限

**数据依赖性**：Joint-GRPO 训练依赖高质量 GT 视频与 caption 对（从 1K 高质样本中手动筛选），这限制了方法在低资源场景下的可扩展性。VANS-Data-100K 数据集的 QA 生成依赖 Gemini-2.5-Flash 模拟问题与链式推理，可能存在模型偏差。

**推理效率**：caption 生成约 4 秒，视频生成约 35 秒，总计约 39 秒的单次推理时间不适用于实时交互场景。这主要受限于 VDM 的扩散采样过程。

**评估覆盖度**：评估基准规模有限（程序性 400 + 预测性 400 样本），可能不足以覆盖广泛的 VNEP 场景（如体育动作、医疗操作、科学实验等）。

**架构泛化性**：当前 VANS 的 VLM 和 VDM 均为特定模型选择（Qwen2.5-VL-3B 和 Wan-2.1-1.3B），Joint-GRPO 框架对其他 VLM/VDM 组合的泛化能力尚未验证。

### 开放问题

1. **端到端联合训练的可能性**：Joint-GRPO 的两阶段设计是否可以通过交替优化或对抗训练等端到端方案进一步简化，同时保持优化稳定性？

2. **多步事件预测扩展**：当前 VANS 仅预测单一下一事件，能否扩展到生成多个连续事件视频（如“接下来的三步操作”）？这需要解决更长时序依赖和误差累积问题。

3. **caption 质量的理论上限**：VLM 生成的 caption 质量对最终视频质量的影响是否存在理论上限？能否通过强化 VDM 对低质量 caption 的鲁棒性来突破这一瓶颈？

4. **跨任务泛化**：Joint-GRPO 的跨模态协同优化框架是否能泛化到其他需要语义-视觉对齐的生成任务（如文本-3D 场景生成、音频-视频对齐等）？

5. **更大规模验证**：在更多样化的 VNEP 场景（体育、医疗、科学实验）和更大规模基准上，VANS 的性能优势是否仍然保持？



## 原文 PDF

![[paperPDFs/CVPR_2026/Video_as_Answer_Predict_and_Generate_Next_Video_Event_with_Joint_GRPO.pdf]]

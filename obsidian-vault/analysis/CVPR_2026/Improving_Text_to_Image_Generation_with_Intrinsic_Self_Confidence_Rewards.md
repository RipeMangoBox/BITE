---
title: Improving Text-to-Image Generation with Intrinsic Self-Confidence Rewards
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Improving_Text_to_Image_Generation_with_Intrinsic_Self_Confidence_Rewards.pdf
project_link: "https://wookiekim.github.io/SOLACE/"
code_link: null
aliases:
- ITIGISCR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将模型对自身生成潜变量重新加噪后的去噪恢复误差（重建噪声的准确性）转化为内在自信奖励，作为强化学习的标量奖励信号。
primary_logic: 大规模预训练的流匹配模型具有强大的图像-文本先验，其自我去噪能力与生成图像的组合性、文本渲染和图文对齐质量正相关，因此内在自信可以作为无需外部监督的有效奖励信号。
claims:
- SOLACE 在 SD3.5-M 上带来持续的定量增益：GenEval 从 0.65 提升到 0.71，OCR 从 0.61 提升到 0.67，CLIPScore 从 0.282 提升到 0.288，同时人类偏好指标适度改善。
- 内在自信分布随视觉质量提升而右移，表明噪声恢复准确性可预测样本质量。
- 用户研究中，SOLACE 在视觉真实感/吸引力和文本对齐上均显著优于基线（59% vs 26.5% 在视觉上，57.3% vs 14.3% 在文本对齐上）。
- SOLACE 能缓解外部奖励后训练中的奖励黑客问题：在已用外部奖励后训练的模型上应用 SOLACE，非目标能力（组合性、文本渲染、对齐）进一步提升，而目标外部指标仅轻微下降。
---

# Improving Text-to-Image Generation with Intrinsic Self-Confidence Rewards

> [!tip] 核心洞察
> 大规模预训练的流匹配模型具有强大的图像-文本先验，其自我去噪能力与生成图像的组合性、文本渲染和图文对齐质量正相关，因此内在自信可以作为无需外部监督的有效奖励信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用内在自信奖励改善文本到图像生成 |
| 英文题名 | Improving Text-to-Image Generation with Intrinsic Self-Confidence Rewards |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00918) · [Project](https://wookiekim.github.io/SOLACE/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SOLACE |
| Dataset | GenEval, OCR, CLIPScore, Human Preference |

> [!tip] 效果简介
> - GenEval 上，Compositional Generation Score 0.71 (SD3.5-M+SOLACE) vs 0.65 (SD3.5-M) (+0.06)。
> - OCR (Text Rendering) 上，Text Rendering Score 0.67 (SD3.5-M+SOLACE) vs 0.61 (SD3.5-M) (+0.06)。
> - CLIPScore (DrawBench) 上，CLIPScore 0.288 vs 0.282 (+0.006)。

## 概述

**问题瓶颈**：当前文本到图像（T2I）生成模型的后训练高度依赖外部奖励模型（如 PickScore、HPSv2）或人类偏好标注。这种范式面临两个根本性困难：一是外部监督信号难以随模型能力提升而持续扩展（scalability 瓶颈）；二是优化外部代理指标时容易发生“奖励黑客”（overoptimization），即模型在目标指标上虚高，但真实视觉质量、组合生成能力和文本对齐度反而退化。

**核心洞察**：大规模预训练的流匹配（Flow Matching）模型拥有强大的图像-文本联合先验。作者发现，模型对**自身生成潜变量重新加噪后的去噪恢复能力**——即“内在自信”（intrinsic self-confidence）——与生成图像的组合性、文本渲染质量和图文对齐程度呈正相关。这意味着模型自身就携带了一个无需外部监督的、可预测样本质量的内在信号。

**方法定位**：SOLACE（**S**elf-**O**riginating **LA**tent **C**onfidence **E**stimation）是一种**内在奖励驱动的后训练框架**。它在潜空间中直接计算奖励，完全摒弃外部奖励模型或人类反馈。方法将 GRPO（Group Relative Policy Optimization）强化学习范式与自监督自信估计相结合，仅需在采样的时间步子集上对策略网络进行轻量微调（LoRA），即实现稳定的性能提升。

**主要结果**：
- 在 SD3.5-M 上，SOLACE 带来一致的定量增益：GenEval 组合生成得分从 0.65 提升至 0.71，OCR 文本渲染得分从 0.61 提升至 0.67，CLIPScore 从 0.282 提升至 0.288（Table 1）。
- 用户研究中，SOLACE 在视觉真实感/吸引力上以 59.0% vs 26.5% 显著优于基线，在文本对齐上以 57.3% vs 14.3% 大幅领先（Figure 4）。
- SOLACE 能有效缓解外部奖励后训练中的奖励黑客问题：在已使用外部奖励（PickScore）后训练的模型上进一步应用 SOLACE，非目标能力（组合性、文本渲染、对齐）继续提升，而外部指标仅轻微下降（Figure 5）。
- 方法对模型架构和规模具有通用性：在 SD3.5-L、FLUX.1-Dev（DiT 架构）和 SDXL（UNet 架构）上均有效，甚至可扩展到文本到视频生成任务（Table 3–5）。

**知识库定位**：SOLACE 属于**自监督奖励后训练**这一新兴范式，区别于依赖 CLIP 评分、美学预测器或人类偏好模型的外部奖励路线（如 DDPO、AlignProp、FlowGRPO）。其技术谱系上承流匹配基础框架与 GRPO 策略优化，下启无需人工标注的可扩展对齐方法。

## 背景与动机

文本到图像生成领域近年来取得了显著进展，大规模扩散模型和流匹配模型已能根据自然语言描述合成高质量、多样化的图像。然而，生成结果的组合性（compositionality）、文本渲染准确性（text rendering）以及图文对齐度（text-image alignment）仍然远未达到实用级可靠性——模型常常混淆对象属性、空间关系，或无法正确渲染指定的文字。

### 现有后训练范式的瓶颈

为缓解上述问题，主流方法在预训练之后引入额外的后训练（post-training）阶段，利用人类偏好数据或外部奖励模型对生成策略进行微调。典型的外部奖励信号包括基于 CLIP 的美学评分、PickScore、HPSv2 等可学习评估器，以及基于人类反馈的强化学习（RLHF）。这一范式存在两个核心瓶颈：

1. **可扩展性受限**：外部奖励模型本身需要大量标注数据训练，且其评估能力受限于训练分布，难以泛化到开放域的提示空间。依赖人类标注则成本高昂，无法规模化迭代。

2. **奖励黑客（Reward Hacking）与过度优化**：当策略网络针对外部奖励进行强化学习时，模型倾向于利用奖励函数的漏洞，生成在指标上得分高但实际质量退化或牺牲其他能力的样本。例如，针对 PickScore 优化的模型可能在视觉吸引力上提升，但组合生成能力反而下降（见 Table 1 底部区域与 Figure 5）。

### 内在反馈信号的缺失

上述瓶颈的根源在于：现有后训练完全依赖**外部**监督信号，而忽略了预训练模型自身蕴含的**内在**评估能力。大规模流匹配模型在数亿级图文对上训练后，其去噪网络已经内化了对图像-文本一致性的强先验——模型“知道”什么样的潜变量能与给定文本条件相容。问题在于，如何将这种隐含的知识转化为可优化的标量奖励信号。

### 本文动机与核心直觉

SOLACE 的核心直觉简洁而深刻：**一个生成模型对自身产物的“自信”可以用其从噪声中恢复该产物的能力来衡量**。具体而言，对于模型生成的潜变量 $z_0$，若对其重新注入已知噪声后，模型能够准确恢复出注入的噪声，则说明该潜变量与模型内化的图文先验高度一致——模型对这次生成“有信心”；反之，若恢复误差很大，则说明该生成结果偏离了模型所学到的分布，可能包含组合错误或对齐失败。

这一直觉的可操作化带来了三个关键优势：
- **无需外部监督**：奖励信号完全在潜空间中计算，不依赖额外的评估模型或人类标注。
- **与生成质量正相关**：实验表明，内在自信的分布随视觉质量提升而整体右移（Figure 6），验证了噪声恢复准确性对样本质量的可预测性。
- **天然抗奖励黑客**：由于奖励源自模型自身的去噪能力，而非外部代理指标，策略优化时难以通过简单纹理填充或指标欺骗来提升奖励（Figure 8 显示不当设置下的塌陷模式与正确设置下的稳定改善）。

综上，SOLACE 试图回答一个根本性问题：**能否仅凭模型对自身生成的内在自信，在无需任何外部奖励的前提下，持续改善文本到图像生成的组合性、文本渲染和图文对齐？**

## 核心创新

### 1. 问题瓶颈与创新动机

当前文本到图像生成的后训练流程高度依赖外部奖励模型（如 PickScore、HPSv2）或人工偏好标注来提供优化信号。这一范式面临两个根本性瓶颈：

- **可扩展性受限**：外部奖励模型需要额外的模型推理或人工标注，计算成本和标注成本随训练规模线性增长。
- **奖励黑客风险**：模型容易过拟合外部奖励的统计偏置，在优化目标指标的同时损害组合生成、文本渲染等非目标能力，即 overoptimization 问题。

SOLACE 的核心洞察在于：**大规模预训练的流匹配模型已经内化了强大的图像-文本联合先验，其对自身生成结果的重建能力可以作为无需外部监督的奖励信号**。具体而言，模型对自身生成潜变量重新加噪后的去噪恢复误差，与生成图像的组合性、文本渲染质量和图文对齐程度呈正相关——这一内在自信信号天然可获取，无需解码到像素空间或调用任何外部模型。

### 2. 核心改变槽位

SOLACE 的核心创新可精确归结为两个改变槽位（changed slots）：

#### 槽位一：奖励信号来源

| 维度 | 基线方法 | SOLACE |
|------|----------|--------|
| **信号来源** | 外部奖励模型（PickScore, HPSv2）或人工偏好数据 | 模型对自身输出的内在自信估计 |
| **信号本质** | 外部模型对生成图像的评分 | 模型恢复自身生成潜变量中注入噪声的准确性 |
| **计算模态** | 需解码到像素空间，运行额外评估模型 | 直接在潜空间中计算，无需解码或外部模型 |

具体而言，SOLACE 将奖励信号定义为：

$$S_{i,t} = -\log \mathrm{MSE}_{i,t} = -\log\left(\frac{1}{K}\sum_{m=1}^K \|\hat{\epsilon}_\theta(z_t^{(i,m)}, t, c) - \epsilon^{(m)}\|_2^2\right)$$

其中 $z_t^{(i,m)}$ 是对生成潜变量 $z_0^{(i)}$ 在时间步 $t$ 上用噪声探针 $\epsilon^{(m)}$ 重新加噪后的结果，$\hat{\epsilon}_\theta$ 是模型从速度场恢复的估计噪声。最终的标量奖励 $R_{\mathrm{SOLACE}}$ 通过在所有探测时间步上加权聚合得到（公式 14）。

这一设计的核心优势在于：**信号完全内生于模型本身**，既不依赖外部标注，也不引入额外的模型推理开销。验证实验（Figure 6）显示，随着推理配置从无 CFG 到标准 CFG 再到更优的 CFG 尺度，自信分布整体右移，表明噪声恢复准确性与视觉质量正相关。

#### 槽位二：奖励计算模态

| 维度 | 基线方法 | SOLACE |
|------|----------|--------|
| **计算空间** | 像素空间（需 VAE 解码） | 潜空间（直接在生成潜变量上操作） |
| **外部依赖** | 需加载并运行外部奖励模型 | 零外部依赖，仅使用生成模型自身的速度场 |
| **计算效率** | 解码 + 外部模型前向传播 | 仅在潜空间中进行重加噪和去噪恢复 |

SOLACE 的奖励计算完全在潜空间中完成：对 GRPO 组采样得到的 $G$ 条潜变量轨迹，使用 $K$ 个共享噪声探针在选定的时间步子集 $\mathcal{T}$ 上进行正向加噪，然后通过模型的速度场恢复噪声估计。整个过程无需 VAE 解码，避免了像素空间操作的计算开销。

### 3. 核心机制：噪声探测与自信估计

SOLACE 的方法流程（Figure 2）可分解为四个关键步骤：

1. **潜变量采样**：对同一文本提示 $c$，从随机噪声出发生成 $G$ 条独立的反向轨迹，得到终端潜变量 $\{z_0^{(i)}\}_{i=1}^G$。

2. **噪声探测与重加噪**：采样 $K$ 个共享噪声探针 $\epsilon^{(m)} \sim \mathcal{N}(0, I)$，在选定时间步 $t \in \mathcal{T}$ 上对每个 $z_0^{(i)}$ 进行线性正向加噪：
   $$z_t^{(i,m)} = (1-t)z_0^{(i)} + t\epsilon^{(m)}$$

3. **自信估计**：模型通过速度场 $v_\theta$ 恢复注入的噪声：
   $$\hat{\epsilon}_\theta(z_t^{(i,m)}, t, c) = v_\theta(z_t^{(i,m)}, t, c) + z_0^{(i)}$$
   然后计算恢复噪声与真实噪声之间的均方误差，取负对数作为自信得分。

4. **GRPO 策略更新**：利用组内相对优势（包含负优势）和 KL 正则项，在时间步子集上更新策略网络参数。

### 4. 与外部奖励方法的本质区别

SOLACE 与现有外部奖励后训练方法（如 FlowGRPO）的根本区别在于优化目标的来源：

- **外部奖励方法**优化的是外部模型定义的偏好空间，容易导致模型牺牲组合性和文本渲染能力来换取外部指标提升。
- **SOLACE** 优化的是模型对自身输出的内在一致性——模型越能准确恢复自身生成潜变量中的噪声扰动，说明生成结果越符合模型内化的图像-文本联合先验。

这一区别在实验中得到验证（Table 1 底部 / Figure 5）：在已使用 PickScore 进行 FlowGRPO 后训练的模型上进一步应用 SOLACE，非目标能力（GenEval 组合生成、OCR 文本渲染、CLIPScore 图文对齐）持续提升，而目标外部指标仅轻微下降。这表明**内在自信奖励与外部奖励互补，能有效缓解奖励黑客问题**。

### 5. 关键设计选择与稳定性保障

SOLACE 的有效性依赖于若干关键设计选择，这些选择直接关系到奖励信号的质量和训练稳定性：

- **在线自信计算优于离线静态自信**：消融实验（Table 2）显示在线计算（GenEval 0.71）明显优于离线静态自信（0.69），因为在线计算能反映策略更新后的最新模型状态。
- **自信计算中省略 CFG**：在自信估计时不使用无分类器引导（CFG）比使用 CFG 产生更强且更稳定的改进，避免了 CFG 引入的额外方差。
- **时间步比例约束**：仅在去噪时间步的后 60%（$\rho=0.6$）上训练可防止训练崩溃；$\rho > 0.6$ 或采样时不使用 CFG 会导致自信飙升和生成退化（Figure 8），这是典型的奖励黑客行为。
- **全符号优势的必要性**：去除负优势（仅使用正优势）会降低组合生成、文本渲染和图文对齐性能（Table 9），说明负优势信号对约束策略更新方向至关重要。
- **聚合奖励优于逐步奖励**：跨时间步平均的聚合奖励提供更稳定的训练信号（Table 11）。

## 整体框架

SOLACE 是一种无需外部监督的文本到图像生成后训练框架，其核心思想是将模型对自身输出的**内在自信**转化为强化学习的奖励信号。整个 pipeline 由四个紧密耦合的模块构成，形成“生成—探测—评估—优化”的闭环。

### 模块关系与数据流

**1. 潜变量采样（GRPO 组采样）**

给定文本提示 $c$，从标准高斯噪声 $z_T^{(i)} \sim \mathcal{N}(0, I)$ 出发，利用当前策略网络 $\pi_\theta$ 执行 $G$ 条独立的反向去噪轨迹，生成 $G$ 个终端潜变量 $z_0^{(i)}$（$i = 1, \ldots, G$）。这些样本构成 GRPO 所需的组内对比基础，无需解码为像素图像即可进入后续阶段。

**2. 噪声探测与重加噪**

对每个生成的潜变量 $z_0^{(i)}$，引入 $K$ 个共享噪声探针 $\epsilon^{(m)} \sim \mathcal{N}(0, I)$（$m = 1, \ldots, K$），在选定的时间步子集 $\mathcal{T} \subset [0, 1]$ 上执行正向加噪：

$$z_t^{(i,m)} = (1 - t) z_0^{(i)} + t \epsilon^{(m)}, \quad t \in \mathcal{T}$$

这一步在潜空间中完成，无需解码器参与，将终端潜变量重新映射回流匹配路径上的中间状态。

**3. 自信估计**

模型对每个重加噪后的潜变量 $z_t^{(i,m)}$ 预测速度场 $v_\theta(z_t^{(i,m)}, t, c)$，并恢复估计噪声：

$$\widehat{\epsilon}_\theta(z_t^{(i,m)}, t, c) = v_\theta(z_t^{(i,m)}, t, c) + z_0^{(i)}$$

计算估计噪声与注入噪声之间的均方误差，并取负对数作为该时间步的自信得分：

$$S_{i,t} = -\log\left(\frac{1}{K} \sum_{m=1}^K \left\| \widehat{\epsilon}_\theta(z_t^{(i,m)}, t, c) - \epsilon^{(m)} \right\|_2^2\right)$$

最终，将所有探测时间步的自信得分加权聚合为标量奖励：

$$R_{\mathrm{SOLACE}}(z_0^{(i)}, c) = \frac{1}{\sum_{t \in \mathcal{T}} w(t)} \sum_{t \in \mathcal{T}} w(t) S_{i,t}$$

该奖励完全在潜空间中计算，无需外部模型或人类标注。

**4. GRPO 策略更新**

利用组内 $G$ 个样本的奖励计算相对优势：

$$\hat{A}_t^i = \frac{R(z_0^i, c) - \operatorname*{mean}(\{R(z_0^i, c)\}_{i=1}^G)}{\operatorname*{std}(\{R(z_0^i, c)\}_{i=1}^G)}$$

保留正负全符号优势，结合 KL 正则项约束策略偏离参考模型的程度，在选定的时间步子集上更新策略网络参数 $\theta$。

### 关键设计决策

- **在线自信计算**：自信得分在训练过程中实时计算，而非使用预训练的静态分数。消融实验表明，在线计算显著优于离线静态自信（GenEval: 0.71 vs 0.69）。
- **无 CFG 的自信估计**：在自信计算中省略无分类器引导（CFG），比使用 CFG 产生更强且更稳定的改进。
- **时间步约束与防坍塌**：仅在去噪时间步的后 60%（$\rho = 0.6$）上训练，且采样时保留 CFG。若 $\rho > 0.6$ 或采样时去除 CFG，会导致自信得分短期飙升后生成退化（奖励黑客），表现为无纹理图像。
- **负优势的必要性**：去除负优势（仅使用正优势）会降低组合生成、文本渲染和图文对齐性能，说明全符号优势对 SOLACE 至关重要。

### 输入输出规范

| 阶段 | 输入 | 输出 |
|------|------|------|
| 潜变量采样 | 文本提示 $c$，随机噪声 | $G$ 个终端潜变量 $z_0^{(i)}$ |
| 重加噪 | $z_0^{(i)}$，$K$ 个噪声探针，时间步 $\mathcal{T}$ | 重加噪潜变量 $z_t^{(i,m)}$ |
| 自信估计 | $z_t^{(i,m)}$，提示 $c$，时间步 $t$ | 标量奖励 $R_{\mathrm{SOLACE}}$ |
| 策略更新 | 奖励值，优势估计，KL 约束 | 更新后的策略参数 $\theta$ |

整个 pipeline 的核心优势在于**无需解码到像素空间**，也**无需外部奖励模型或人类反馈**，完全依赖模型自身的去噪能力作为内在反馈信号。实验验证表明，该内在自信与组合生成、文本渲染和图文对齐质量正相关——视觉质量越高，自信分布整体右移（Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SOLACE. Given a text prompt c, we generate G different latents. Without decoding, we re-noise the latents using K noise probes across*

## 核心模块与公式推导

### 3.1 流匹配基础

SOLACE 构建在 Rectified Flow 框架之上。给定数据样本 $x_0$ 和高斯噪声 $x_1 \sim \mathcal{N}(0, I)$，流匹配定义了一条线性插值路径：

$$x_t = (1 - t) x_0 + t x_1$$

其中 $t \in [0, 1]$。沿此路径的目标速度为常数：

$$v^{\star} = \partial_t x_t = x_1 - x_0$$

模型通过直接回归目标速度进行训练：

$$\mathcal{L}(\theta) = \mathbb{E}_{x_0 \sim p_{\mathrm{data}}, x_1 \sim p_1, t \sim \mathcal{U}[0,1]} \| v^{\star} - v_{\theta}(x_t, t) \|_2^2$$

### 3.2 内在自信奖励计算

SOLACE 的核心创新在于将模型对自身生成潜变量的去噪恢复能力转化为标量奖励信号。整个过程在潜空间中完成，无需解码或外部模型参与。

**步骤一：潜变量采样。** 给定文本提示 $c$，从随机噪声 $z_T^{(i)} \sim \mathcal{N}(0, I)$ 出发，利用当前策略 $\pi_\theta$ 生成 $G$ 条独立的反向轨迹：

$$z_{t-1}^{(i)} \sim \pi_\theta(\cdot \mid z_t^{(i)}, c), \quad i = 1, \ldots, G$$

每条轨迹的终端潜变量记为 $z_0^{(i)}$。

**步骤二：噪声探测与重加噪。** 引入 $K$ 个共享噪声探针 $\epsilon^{(m)} \sim \mathcal{N}(0, I), m = 1, \dots, K$。对每个终端潜变量 $z_0^{(i)}$，在选定时间步子集 $\mathcal{T} \subset [0, 1]$ 上沿前向路径重新加噪：

$$z_t^{(i,m)} = (1 - t) z_0^{(i)} + t \epsilon^{(m)}, \quad t \in \mathcal{T}$$

**步骤三：噪声恢复与误差计算。** 模型 $v_\theta$ 对重加噪后的潜变量进行去噪，从速度场恢复估计的噪声：

$$\widehat{\epsilon}_\theta(z_t^{(i,m)}, t, c) = v_\theta(z_t^{(i,m)}, t, c) + z_0^{(i)}$$

计算估计噪声与注入噪声之间的均方误差：

$$\mathrm{MSE}_{i,t} = \frac{1}{K} \sum_{m=1}^K \left\| \widehat{\epsilon}_\theta(z_t^{(i,m)}, t, c) - \epsilon^{(m)} \right\|_2^2$$

**步骤四：自信得分与奖励聚合。** 每个时间步 $t$ 上的自信得分定义为负对数误差 $S_{i,t} = -\log(\mathrm{MSE}_{i,t})$。最终的内在自信奖励为所有探测时间步上自信得分的加权聚合：

$$R_{\mathrm{SOLACE}}(z_0^{(i)}, c) = \frac{1}{\sum_{t \in \mathcal{T}} w(t)} \sum_{t \in \mathcal{T}} w(t) S_{i,t}$$

其中 $w(t)$ 为时间步权重（默认均匀权重）。该标量奖励直接反映了模型对自身输出的“自信”程度——恢复噪声越准确，自信越高。

### 3.3 GRPO 策略更新

SOLACE 采用 Flow-GRPO 进行后训练。对于每组 $G$ 个样本，计算组内相对优势：

$$\hat{A}_t^i = \frac{R(x_0^i, c) - \operatorname*{mean}(\{R(x_0^i, c)\}_{i=1}^G)}{\operatorname*{std}(\{R(x_0^i, c)\}_{i=1}^G)}$$

此公式同时保留正优势和负优势，对策略进行全符号更新。策略优化目标包含 KL 正则项以防止偏离参考模型过远，其中每步 KL 散度在高斯转移且方差相等的假设下简化为：

$$D_{\mathrm{KL}} = \frac{1}{2\sigma_t^2} \left\| \mu_{\theta} - \mu_{\mathrm{ref}} \right\|_2^2$$

### 3.4 训练稳定化设计

- **时间步子集约束**：仅在去噪时间步的后 60%（$\rho = 0.6$）上计算奖励和更新策略。消融表明 $\rho > 0.6$ 或采样时不使用 CFG 会引发奖励黑客——自信飙升后生成退化（Figure 8）。
- **去噪步数缩减**：训练时使用 10 步去噪（推理时 40 步），大幅降低计算开销而不损害增益。
- **在线自信计算**：消融显示在线计算自信（GenEval 0.71）明显优于离线静态自信（0.69），因为在线信号随策略同步演化，提供更准确的反馈。
- **省略 CFG 的自信计算**：在自信估计中不使用无分类器引导，比使用 CFG 产生更强且更稳定的改进。
- **负优势的必要性**：去除负优势（仅用正优势）会降低组合生成、文本渲染和图文对齐性能，说明全符号优势对 SOLACE 至关重要。

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/020_Figure_8.jpg]]
*Figure 8: Visualization of training collapse in SOLACE. Selfconfidence (y-axis) versus training iteration under different settings. Using*

### 补充图表

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/008_Figure_6.jpg]]
*Figure 6: Rationale of SOLACE. Distributions of self-confidence under three inference settings. The distribution shifts rightward (higher self-confidence) as visual quality improves, showing that noise recovery accuracy is predictive of sample quality*

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative results of SOLACE on Wan2.1-1.3B. SOLACE produces videos with improved visual quality and prompt adherence compared to the base model*

## 实验与分析

### 核心定量结果

SOLACE 在 SD3.5-M 上带来了一致的定量增益，覆盖组合生成、文本渲染、图文对齐和人类偏好等多个维度。Table 1 汇总了主要结果：

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of SOLACE. We evaluate SOLACE on SD3.5 [16] across GenEval [21], Text Rendering, human preference models [35, 77, 80, 83], and image quality metrics. SOLACE yields consistent gains across all quantitative metrics. In the bottom section, each row of SD3.5-M + FlowGRPO corresponds to a different external reward used for FlowGRPO training; the blue cell indicates which metric was used as the external reward*

- **组合生成**：GenEval 得分从 0.65 提升至 0.71（+0.06），表明模型在复杂空间/属性组合上的理解能力显著增强。
- **文本渲染**：OCR 得分从 0.61 提升至 0.67（+0.06），证明内在自信信号对文本生成质量有直接正向影响。
- **图文对齐**：DrawBench 上的 CLIPScore 从 0.282 提升至 0.288（+0.006），PickScore 从 22.34 提升至 22.41（+0.07），改善幅度虽小但一致。

值得注意的是，SOLACE 在人类偏好指标上的增益相对温和。这一现象与方法的本质一致：内在自信衡量的是模型对自身输出的“确定性”，而非直接优化人类审美偏好。因此，它在组合性和文本渲染等更依赖模型内部一致性的任务上增益更大，而在通用视觉吸引力上改善有限。

### 用户研究

Figure 4 展示的用户研究结果进一步验证了上述判断。在 PartiPrompts 和 HPSv2 提示集上，SD3.5-M+SOLACE 在视觉真实感/吸引力上以 59.0% vs 26.5% 的胜率显著优于基线，在文本对齐上以 57.3% vs 14.3% 的胜率领先。文本对齐维度的巨大优势（+43%）与 OCR 指标的提升相互印证，说明内在自信对文本渲染能力的改善是用户可感知的。

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/004_Figure_4.jpg]]
*Figure 4: User study against baseline SD3.5-M [16] on PartiPrompts [61] and HPSv2 [80]. The user study shows that SOLACE post-training yields favorable visual realism/appeal, and text-image alignment*

### 消融实验

Table 2 系统验证了 SOLACE 的关键设计选择：

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/006_Table_2.jpg]]
*Table 2: Ablation study results of SOLACE. We validate the design choices of SOLACE over number of noise probes K, the usage of CFG for self-confidence calculation, and online/offline self-confidence calculation. Our current configurations yield superior results*

**噪声探针数量 K**：K=8 在整体性能上略优于 K=4 和 K=16。K 过小导致自信估计方差大，过大则引入冗余计算，8 个探针在估计稳定性和计算效率间取得平衡。

**在线 vs 离线自信**：在线计算自信（每次生成后实时探测）明显优于离线静态自信（GenEval: 0.71 vs 0.69）。这揭示了一个关键机制：自信信号必须与当前策略的生成分布同步更新，离线预计算的自信无法捕捉策略改进过程中的分布偏移。

**CFG 的使用**：在自信计算中省略 CFG 比使用 CFG 产生更强且更稳定的改进。这一发现具有重要的实践意义——CFG 虽然改善了生成质量，但其引入的分布偏移会污染自信信号，使奖励估计不再准确反映模型对自身输出的真实确定性。

**负优势的必要性**：Table 9 显示，去除负优势（仅使用正优势进行策略更新）会降低组合生成、文本渲染和图文对齐性能。全符号优势（包含正负）允许策略同时从“好”样本中学习、从“差”样本中规避，这对维持生成多样性和避免模式坍塌至关重要。

**聚合 vs 逐步奖励**：Table 11 表明，跨时间步平均的聚合奖励始终优于逐步奖励。逐步奖励在单个时间步上噪声较大，聚合后提供了更稳定的训练信号。

### 训练稳定性与失败模式

SOLACE 的训练对超参数敏感，存在明确的失败模式。Figure 8 可视化了训练坍塌现象：

- **时间步子集比例 ρ**：当 ρ > 0.6（即在超过 60% 的去噪时间步上训练）时，模型会快速学会“欺骗”自信奖励——生成无纹理、易恢复的退化图像，使自信得分飙升但视觉质量崩溃。ρ = 0.6 是经验上的安全阈值。
- **采样时 CFG 的必要性**：若在 rollout 采样阶段不使用 CFG，同样会引发奖励黑客。CFG 在采样中的作用是约束生成空间，缺乏这一约束时，策略会找到自信高但语义空洞的捷径。

SOLACE 的默认设置（ρ = 0.6，采样时使用 CFG）能有效避免上述问题，在保持稳定训练的同时实现持续改进。

### 奖励黑客缓解

Table 1 下半部分和 Figure 5 展示了 SOLACE 的一个重要特性：缓解外部奖励后训练中的奖励黑客问题。在已用 PickScore 作为外部奖励进行 FlowGRPO 后训练的模型上，进一步应用 SOLACE 能提升非目标能力（组合性、文本渲染、对齐），而目标外部指标仅轻微下降。这揭示了内在自信与外部奖励的互补性——外部奖励容易导致过拟合到单一指标而牺牲其他能力，内在自信作为模型自洽性信号，能起到正则化作用，将策略拉回更平衡的生成空间。

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/007_Figure_5.jpg]]
*Figure 5: Effect of SOLACE post-training SD3.5-M after posttraining on PickScore [35] using FlowGRPO [41]. SOLACE complements external rewards, showing the best compositional generation and visual appeal on GenEval [21]. Post-training on external rewards yields high visual appeal, but sacrifices compositionality as shown above (Column 3: Generates yellow motorcycle instead / generates unwanted human)*

### 跨模型与跨架构泛化

SOLACE 展现出良好的泛化性：
- **更大模型**：在 SD3.5-L 上应用 SOLACE 同样带来增益（Table 3），表明内在自信信号随模型容量增大而保持有效。
- **不同架构**：在基于 UNet 的 SDXL 上（Table 4）和基于流匹配的 FLUX.1-Dev 上（Table 3），SOLACE 均能提升组合生成和文本渲染性能，证明方法对底层架构不敏感。
- **跨模态**：在文本到视频模型 Wan2.1-1.3B 上（Table 5），SOLACE 改善了主体一致性、背景一致性和动态程度，同时保持运动平滑度，暗示内在自信作为通用生成质量信号可扩展到视频领域。

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/009_Table_3.jpg]]
*Table 3: Applying SOLACE to SD3.5-L [16] and FLUX.1-Dev [5]. We apply SOLACE on additional models of SD3.5-L and FLUX.1- Dev, to verify the effect of SOLACE given (1) a larger base model, and (2) a different architecture from SD3.5-M. † denotes results taken from DiffusionNFT [96]. We base our experiments on our reproduced results based on the official weights of SD3.5-L [16] and FLUX.1- Dev [5]. The results show that SOLACE consistently results in improved compositionality, text rendering and text-image alignment, while being competitive at human preference metrics*

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/010_Table_4.jpg]]
*Table 4: Applying SOLACE to SDXL [53]. SOLACE yields improvements in compositional generation and text rendering on a UNetbased diffusion model, demonstrating architecture-agnostic applicability*

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/011_Table_5.jpg]]
*Table 5: Applying SOLACE to Wan2.1-1.3B for text-to-video generation. Evaluation on VBench-1.0 subset. SOLACE improves subject consistency, background consistency, and dynamic degree while maintaining competitive motion smoothness*

### 分辨率泛化与语义保持

Table 6 显示，在 512×512 分辨率上训练的 SOLACE 能有效迁移到 1024×1024 推理，无需额外微调。Table 8 进一步验证了语义正确性和多样性的保持：在 RareBench 的罕见组合上 CLIPScore 未退化，DrawBench 上的多样性得分（64 样本/提示）保持稳定，说明 SOLACE 不会因奖励优化而牺牲罕见概念的语义准确性或生成多样性。

### 提示源的影响

Table 10 对比了不同提示源对 SOLACE 效果的影响。文本密集的 OCR 提示（包含具体文字渲染要求）带来最佳增益，这与内在自信对文本渲染能力的强相关性一致。对于开放式简短提示，增益相对较小，提示方法的改进空间在于提示语料的选择——描述性强、约束明确的提示能更有效地引导自信信号的利用。

### 补充图表

![[assets/figures/papers/paper_list_l2318_https_arxiv_org_abs_2603_00918/figures/016_Table_9.jpg]]
*Table 9: Effect of negative advantages. Removing negative advantages (positive-only variant) degrades compositional generation, text rendering, and text-image alignment, demonstrating that the full signed advantage is important for SOLACE’s effectiveness*

## 方法谱系与知识库定位

### 1. 方法沿革与基线关系

SOLACE 的核心贡献在于**将文本到图像生成的后训练从依赖外部监督转向利用模型内在信号**。其直接对比的基线方法可分为三类：

- **预训练基座模型**：SD3.5-M、SD3.5-L、SDXL 和 FLUX.1-Dev。这些模型经过大规模预训练，具备强大的图像-文本先验，但未经过面向人类偏好的后训练。SOLACE 在这些基座上叠加 GRPO 微调，以内在自信为奖励信号，验证了后训练带来的持续增益。

- **外部奖励后训练**：以 FlowGRPO 为代表，使用 PickScore、HPSv2 等外部奖励模型驱动 GRPO 更新。该范式的核心瓶颈在于：外部奖励模型本身是有限容量的代理，容易导致**奖励黑客**——模型过拟合到奖励模型的偏好上，牺牲组合性、文本渲染等非目标能力。SOLACE 的实验直接展示了这一现象：在已用 PickScore 进行 FlowGRPO 后训练的模型上再应用 SOLACE，组合生成和文本渲染进一步提升，而 PickScore 仅轻微下降（Table 1 下半部分 / Figure 5）。

- **人类反馈后训练**：如基于人类偏好数据训练奖励模型再进行 RLHF 微调的方法。SOLACE 避免了此类方法对人类标注的依赖和可扩展性瓶颈。

从技术谱系上看，SOLACE 继承了 **GRPO** 的组内相对优势更新框架，但将奖励信号的来源从外部模型替换为模型对自身输出的去噪恢复能力。这一思路与自监督表示学习中的“重建即评估”范式有精神联系，但在生成模型后训练中尚属首次系统性地探索。

### 2. 适用边界

SOLACE 的有效性建立在以下前提之上：

- **模型需具备强图像-文本先验**：内在自信信号的质量依赖于预训练模型对噪声恢复的能力。实验表明，该方法在 SD3.5-M、SD3.5-L、FLUX.1-Dev 和 SDXL 上均有效，涵盖 DiT（Diffusion Transformer）和 UNet 两种架构（Table 3, Table 4），说明方法具有架构无关性。但若基座模型本身质量过低，内在自信信号可能无法提供有意义的梯度。

- **提示语料需具备足够的信息密度**：消融实验显示，文本密集的 OCR 提示带来的增益最大，开放式简短提示的增益较小（Table 10）。这表明内在自信对需要精确文本渲染和组合性理解的任务最为敏感。

- **训练需谨慎的超参数控制**：训练时间步子集比例 ρ 是关键敏感参数。ρ > 0.6 或采样时未使用 CFG 会导致奖励黑客——模型学会生成无纹理图像以降低重建误差，而非提升真实质量（Figure 8）。当前最佳设置为 ρ = 0.6 且采样时使用 CFG。

### 3. 局限与开放问题

**已知局限**：

1. **与通用人类偏好的对齐有限**：内在自信在 PickScore、HPSv2 等人类偏好指标上仅带来适度改善（PickScore 从 22.34 提升至 22.41），说明噪声恢复准确性与人类审美判断之间存在差距。SOLACE 更擅长提升组合性、文本渲染等“可验证”能力，而非纯粹的视觉吸引力。

2. **训练稳定性敏感**：如前所述，ρ 和 CFG 设置不当会引发训练崩溃。方法对超参数的敏感性增加了实际部署的调参成本。

3. **提示依赖性**：方法效果部分依赖于提示语料的质量和类型，对简短开放式提示的增益较小。

**开放问题**：

1. **内在自信与外部信号的融合**：内在自信能否与对比学习等自监督任务结合，以增强与人类偏好的对齐？Figure 5 已初步展示内在与外部奖励的互补性，但系统性的融合策略仍需探索。

2. **跨模态泛化**：SOLACE 已在文本到视频生成（Wan2.1-1.3B, Table 5 / Figure 7）上初步验证有效。该方法能否推广到文本到 3D、可控编辑等更复杂的多模态生成任务，以及更大规模的模型中，仍有待研究。

3. **自适应超参数选择**：噪声探针数量 K 和时间步子集 ρ 目前依赖人工调参。在不依赖外部奖励的前提下，如何自动选择最优的 K 和 ρ，是方法走向实用化的关键问题。

4. **内在自信的理论基础**：为什么大规模流匹配模型的去噪能力与生成质量正相关？Figure 6 提供了经验证据，但缺乏严格的理论分析。建立内在自信与生成质量之间的形式化联系，将有助于指导更优的奖励设计。

## 原文 PDF

![[paperPDFs/CVPR_2026/Improving_Text_to_Image_Generation_with_Intrinsic_Self_Confidence_Rewards.pdf]]

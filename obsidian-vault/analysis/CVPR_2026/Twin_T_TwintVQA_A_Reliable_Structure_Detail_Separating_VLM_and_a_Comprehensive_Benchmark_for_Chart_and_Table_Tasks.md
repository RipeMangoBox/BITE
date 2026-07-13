---
title: "Twin-T & TwintVQA: A Reliable Structure-Detail Separating VLM and a Comprehensive Benchmark for Chart and Table Tasks"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Twin_T_and_TwintVQA_A_Reliable_Structure_Detail_Separating_VLM_and_a_Comprehensive_Benchmark_for_Chart_and_Table_Tasks.pdf
project_link: null
code_link: "https://github.com/Samsara-1999/Twin-T-TwintVQA"
aliases:
- TT
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过双头图像编码器实现结构与细节的分离与柔性融合，并利用MINT偏好学习强化数值关键词准确性和文本-视觉对齐。
primary_logic: 图表表格理解需同时处理全局结构（轴、网格、布局）和局部细节（数值、图例），分离这两种信号可显著提升数值准确性和答案可靠性。
claims:
- 移除双头编码器导致总体性能下降约5%，表明结构-细节分离是关键。
- "移除Num-Key偏好导致数值准确性(NK Acc)大幅下降（1B:-2.70%, 7B:-5.90%），证明数值强化有效。"
- "移除低熵正则化导致熵大幅上升（1B:+8.10%, 7B:+3.80%），表明其稳定数值生成。"
- "移除文本-视觉证据匹配导致匹配度(Match)最大下降（1B:-8.20%, 7B:-6.00%），证明其提升视觉对齐。"
---

# Twin-T & TwintVQA: A Reliable Structure-Detail Separating VLM and a Comprehensive Benchmark for Chart and Table Tasks

> [!tip] 核心洞察
> 图表表格理解需同时处理全局结构（轴、网格、布局）和局部细节（数值、图例），分离这两种信号可显著提升数值准确性和答案可靠性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Twin-T 与 TwintVQA：一种可靠的结-细分离视觉语言模型及面向图表表格任务的综合基准 |
| 英文题名 | Twin-T & TwintVQA: A Reliable Structure-Detail Separating VLM and a Comprehensive Benchmark for Chart and Table Tasks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Bao_Twin-T__TwintVQA_A_Reliable_Structure-Detail_Separating_VLM_and_a_CVPR_2026_paper.html) · [Code](https://github.com/Samsara-1999/Twin-T-TwintVQA) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | Twin-T |
| Dataset | AI2D, CharXiv_R, TableVQA, TwintVQA |

> [!tip] 效果简介
> - AI2D 上，Accuracy 90.77 vs 89.80 (Gemini-2.5-Pro) (+0.97)。
> - CharXiv_R 上，Accuracy 57.10 vs 47.80 (GPT-4o) (+9.30)。
> - TableVQA 上，Accuracy 80.27 vs 77.82 (GPT-4o) (+2.45)。

## 概要

**问题瓶颈**：现有视觉语言模型（VLM）在分析图表和表格时，未能显式分离全局结构线索（如坐标轴、网格、布局）与局部细粒度细节（如数值、图例），导致数值读取错误和不可靠的生成输出。

**核心思路**：Twin-T 提出一种两阶段专家 VLM，通过**双头图像编码器**实现结构与细节的分离与柔性融合，并利用 **MINT 偏好学习**强化数值关键词准确性和文本-视觉对齐，从而在保持模型效率的同时显著提升图表表格问答的可靠性。

**方法定位**：Twin-T 分别以 Ovis2-1B 和 Qwen2.5-VL-7B 为底座构建 1B/7B 两个版本。Stage 1 引入参数无关的 Schur 风格融合模块，将原始图像与 Canny 结构图像分离后重新融合；Stage 2 通过数值关键词加权对比学习、低熵正则化和文本-视觉证据匹配三项偏好损失进行精细调优。该方法在图像编码器设计和偏好学习策略两个关键槽位上区别于单头编码的标准 VLM 和普通 DPO 偏好优化。

**主要结果**：在公开图表表格基准上，Twin-T-7B 在 AI2D 上达到 90.77%（超过 Gemini-2.5-Pro 的 89.80%），在 CharXiv_R 上达到 57.10%（超过 GPT-4o 的 47.80%），在 TableVQA 上达到 80.27%（超过 GPT-4o 的 77.82%）。在自建综合基准 TwintVQA 上，Twin-T-7B 以 70.20% 超过 GPT-4o 的 67.06%，在开源模型中取得最优，并与 Gemini-2.5-Pro 和 GPT-4o 具备竞争力。

**决定性证据**：消融实验表明，移除双头编码器导致总体性能下降约 5%（Table 5）；移除数值关键词偏好使数值准确性 NK Acc 大幅下降（1B: -2.70%, 7B: -5.90%）；移除低熵正则化使熵值显著上升（1B: +8.10%, 7B: +3.80%）；移除文本-视觉证据匹配使匹配度 Match 下降最为明显（1B: -8.20%, 7B: -6.00%）（Table 6）。这些结果一致验证了结构-细节分离和数值强化是性能提升的关键因果机制。

**局限与开放问题**：在 OCR 密集型和代码重建任务上仍落后于大参数量模型，Chart-to-Python 任务性能较低，需要代码对齐监督和更大模型容量。结构-细节分离范式能否泛化到其他视觉推理任务，以及如何自动生成更高质量的结构图像，仍是待探索的问题。

图表和表格是人类视觉推理的核心载体，广泛存在于金融报告、学术论文、商业仪表盘等场景中。理解这类结构化视觉内容需要同时处理两个层面的信息：**全局结构**（坐标轴、网格、布局关系）和**局部细节**（数值、图例、标签）。然而，现有视觉语言模型（VLM）在处理图表表格任务时，普遍将这两种信号混杂在统一的视觉编码过程中，未能显式分离结构线索与细粒度细节，导致数值读取错误和不可靠的生成输出。

这一瓶颈在多个公开基准上已有体现。通用VLM如 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）和 **Ovis2-8B**（Lu et al., arXiv 2024）在图表推理任务上表现平平，而专门的图表VLM如 **ChartAst-13B**（Meng et al., arXiv 2024）和 **ChartVLM-8B**（Xia et al., IEEE TIP 2025）虽然有所改进，但仍未从根本上解决结构-细节耦合问题。这些方法的核心缺陷在于：单头视觉编码器将原始图像的所有信息压缩为统一的嵌入表示，使得模型难以区分“这是条形图的高度”与“这个条形的数值是42.7”这两种性质迥异的视觉信号。

从因果机制来看，**结构-细节分离**是提升图表表格理解能力的关键操控变量。当模型能够独立编码边缘、布局等结构信息，并将其与纹理、数值等细节信息进行可控融合时，数值准确性和答案可靠性应得到显著提升。这一直觉得到了初步验证：移除双头编码器会导致总体性能下降约5%（Table 5），而仅依赖Canny边缘提取的结构图像虽能提供干净的几何线索，但若缺乏细节补偿，仍会损失关键的数值信息。

此外，即使获得了分离的视觉表示，现有VLM在生成阶段仍存在另一个缺口：标准交叉熵损失或通用偏好优化（如DPO）对数值关键词缺乏专门强化，导致模型在输出数字时熵值过高、容易产生幻觉。这一观察指向了第二个关键操控变量——**数值偏好学习**：通过对数值token和比较关键词（如“大于”“最高”）进行加权对比学习，并施加低熵正则化，可以显著稳定数值生成。

本文的动机正是基于上述两个缺口：**（1）视觉编码阶段缺乏结构-细节分离机制；（2）生成优化阶段缺乏针对数值准确性的专门偏好学习。** 为此，我们提出Twin-T，一种两阶段图表表格专家VLM，通过双头图像编码器实现结构与细节的分离与柔性融合，并利用MINT偏好学习强化数值关键词准确性和文本-视觉对齐，从而系统性地提升图表表格任务的可靠性。

## 核心方法与创新机理

Twin-T 的核心创新在于将图表表格理解任务分解为**结构信号与细节信号的显式分离与可控融合**，并辅以面向数值精度的多目标偏好学习。这一设计直接回应了现有VLM在分析图表表格时的根本瓶颈：全局结构线索（轴、网格、布局）与局部细粒度细节（数值、图例、文本）被不加区分地编码，导致数值读取错误和不可靠的生成。

### 创新点一：双头编码与Schur式结构-细节分离

标准VLM（如 **Qwen2.5-VL-7B** (Bai et al., arXiv 2025)、**Ovis2-8B** (Lu et al., arXiv 2024)）采用单头视觉编码器处理原始图像，结构与细节信息在嵌入空间中高度纠缠。Twin-T将这一设计替换为**双头图像编码器**：

1. **结构图像提取**：对原始图像应用Canny边缘检测算法，生成仅保留边缘与轮廓的结构图像。
2. **共享编码**：原始图像与结构图像分别通过**共享且可训练**的视觉编码器，得到原始嵌入 $E_{\mathrm{Img}}$ 和结构嵌入 $E_{\mathrm{Stru}}$。
3. **软门控去噪**：计算结构嵌入的L2范数 $\|E_{\mathrm{Stru}}[b,t,:]\|_2$，并通过带温度参数 $\alpha$ 和阈值 $\tau$ 的Sigmoid函数生成软门控权重 $w_{\mathrm{Stru}}[b,t] = \sigma(\alpha(\|E_{\mathrm{Stru}}[b,t,:]\|_2 - \tau))$，抑制弱结构信号的噪声。
4. **Schur式细节提取**：从原始嵌入中投影并移除结构分量，获得纯净的细节嵌入 $E_{\mathrm{Det}}$：
   $$E_{\mathrm{Det}}[b,t] = E_{\mathrm{Img}}[b,t] - \gamma[b,t] w_{\mathrm{Stru}}[b,t]^2 \mathrm{proj}(E_{\mathrm{Img}}[b,t])$$
5. **柔性融合**：将细节嵌入与结构嵌入按学习权重组合为融合嵌入：
   $$E_{\mathrm{fuse}}[b,t] = w_{\mathrm{Det}}[b,t] E_{\mathrm{Det}}[b,t] + w_{\mathrm{Stru}}[b,t] E_{\mathrm{Stru}}[b,t]$$

这一**参数自由的Schur式模块**插入在视觉编码器与连接器之间，不引入额外可训练参数，却能实现结构与细节的代数分离。消融实验（Table 5）表明，移除双头编码器导致总体性能下降约5%，直接验证了结构-细节分离的关键作用。

### 创新点二：MINT多目标偏好学习

标准VLM通常采用交叉熵损失或无数字加权的偏好优化（如DPO），缺乏对数值精度的显式建模。Twin-T引入**MINT偏好学习**，在chosen vs. rejected响应对上施加三个互补的偏好信号：

1. **数值关键词对比损失**（$\mathcal{L}_{\mathrm{NK}}$）：对数值token和比较关键词（如“大于”“小于”）位置施加加权对比学习，权重 $W[b,t] = \mathrm{norm}(1 + M_{\mathrm{num}}[b,t] + M_{\mathrm{key}}[b,t])$，迫使模型在数值位置更偏好chosen响应。
2. **低熵正则化**：对数值位置的输出logits施加熵惩罚 $H_{[b,t]} = -\sum_{v=1}^{V} p[b,t](v) \log p[b,t](v)$，抑制数值生成的随机性，提升数值确定性。
3. **文本-视觉证据匹配损失**（$\mathcal{L}_{\mathrm{TV}}$）：最大化chosen响应中文本片段与视觉证据的匹配度，同时抑制rejected响应的匹配度，强化生成内容与图像区域的对应关系。

消融实验（Table 6）揭示了各组件的因果效应：移除Num-Key偏好导致数值准确性（NK Acc）大幅下降（1B: -2.70%, 7B: -5.90%）；移除低熵正则化导致熵值飙升（1B: +8.10%, 7B: +3.80%）；移除文本-视觉证据匹配导致匹配度（Match）最大降幅（1B: -8.20%, 7B: -6.00%）。三者协同作用，使Twin-T在数值密集型任务上显著优于仅使用标准偏好优化的基线。

### 创新点三：TwintVQA综合基准

除模型创新外，本文还构建了**TwintVQA基准**，覆盖17种图表类型、11种任务类型、3种数据格式（Image、LaTeX、Python），并包含短/中/长三种问答长度分布。这一基准填补了现有图表表格评测在任务多样性和格式覆盖上的空白，为结构-细节分离方法的有效性提供了细粒度验证平台。

Twin-T 是一个面向图表与表格任务的**两阶段专家视觉语言模型（VLM）**，其核心设计围绕一个关键瓶颈展开：现有 VLM 在分析图表表格时未能显式分离结构线索与细粒度细节，导致数值读取错误和生成不可靠。Twin-T 通过**双头图像编码器**实现结构与细节的分离与柔性融合，并利用 **MINT 偏好学习** 强化数值关键词准确性和文本-视觉对齐，从而显著提升答案可靠性。

整体工作流如 Figure 2 所示，分为两个阶段：

![[assets/figures/papers/paper_list_l2751_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Twin_T_TwintVQA_A/figures/002_Figure_2.jpg]]
*Figure 2: Workfow of our Twin-T VLM for chart–table QA. From left to right we show dataset examples used for Stage 1 and Stage 2 training. Stage 1 builds a novel dual-head visual encoder: besides the original image, a structural image is passed through the image encoder; a parameter-free Schur-style module inserted between the image encoder and the connector, softly gates and removes structural directions to obtain a image details embedding, then fuses structural and detailed image embedding into fused visual embedding. This stage adapts the whole VLM to the novel dual-head pathway and fusion. Stage 2 improves generation precision via preference learning on chosen vs. rejected responses: it upweights...*

### Stage 1：双头视觉编码与结-细分离

该阶段构建了一个新颖的双头视觉编码通路。给定原始图表/表格图像，首先通过 **Structure Image Extractor**（基于 Canny 算法）提取结构图像，保留轴、网格、布局等全局结构信息。随后，原始图像与结构图像分别送入**共享的、可训练的视觉编码器**，得到原始图像嵌入 $E_{\mathrm{Img}}$ 和结构嵌入 $E_{\mathrm{Stru}}$。

在视觉编码器与连接器（connector）之间，插入了一个**无参数的 Schur-style 融合模块**，其工作流程如下：

1. **结构软门控**：计算 $E_{\mathrm{Stru}}$ 每个 token 的 L2 范数 $\|E_{\mathrm{Stru}}[b,t,:]\|_2$，并通过带温度参数 $\alpha$ 和阈值 $\tau$ 的 sigmoid 函数生成软门控权重 $w_{\mathrm{Stru}}[b,t] = \sigma(\alpha(\|E_{\mathrm{Stru}}[b,t,:]\|_2 - \tau))$，抑制低结构响应的噪声区域。
2. **Schur-style 结构去除**：从原始图像嵌入中投影并移除结构分量，获得细节嵌入 $E_{\mathrm{Det}}[b,t] = E_{\mathrm{Img}}[b,t] - \gamma[b,t] w_{\mathrm{Stru}}[b,t]^2 \mathrm{proj}(E_{\mathrm{Img}}[b,t])$，保留数值、图例等细粒度信息。
3. **柔性融合**：将细节嵌入与结构嵌入按学习到的权重进行加权组合，得到融合嵌入 $E_{\mathrm{fuse}}[b,t] = w_{\mathrm{Det}}[b,t] E_{\mathrm{Det}}[b,t] + w_{\mathrm{Stru}}[b,t] E_{\mathrm{Stru}}[b,t]$，作为后续 LLM 的视觉输入。

此阶段使整个 VLM 适配双头通路与融合机制，为下游任务提供结-细分离的视觉表征。

### Stage 2：MINT 偏好学习

在 Stage 1 的基础上，Stage 2 通过偏好学习进一步提升生成精度。MINT（Numeric-Keyword and Text-Vision Evidence Preference）偏好学习包含三个互补的优化目标：

- **数值关键词对比损失 $\mathcal{L}_{\mathrm{NK}}$**：对数值 token 和比较关键词（如“大于”“小于”）位置施加更高的对比权重 $W[b,t] = \mathrm{norm}(1 + M_{\mathrm{num}}[b,t] + M_{\mathrm{key}}[b,t])$，迫使模型在 chosen 与 rejected 响应间拉大数值准确性差距。
- **低熵正则化**：在数值生成位置施加熵正则 $H_{[b,t]} = - \sum_{v=1}^{V} p[b,t](v) \log p[b,t](v)$，降低输出分布的不确定性，稳定数值预测。
- **文本-视觉证据匹配损失 $\mathcal{L}_{\mathrm{TV}}$**：提升 chosen 响应中证据片段的文本-视觉匹配度，强化生成内容与图像区域的对应关系。

### 输入输出流

- **输入**：原始图表/表格图像（Stage 1 同时生成对应的 Canny 结构图像作为辅助输入）。
- **Stage 1 输出**：融合视觉嵌入 $E_{\mathrm{fuse}}$，传入 LLM 进行文本生成。
- **Stage 2 输出**：经过偏好优化的模型，在图表表格问答任务上生成更准确、稳定的答案。

### 因果机制与证据强度

消融实验（Table 5）表明，移除双头编码器导致总体性能下降约 5%，证实结-细分离是关键设计。Table 6 进一步揭示 MINT 各组件的因果效应：移除数值关键词偏好使数值准确性（NK Acc）显著下降（1B: -2.70%, 7B: -5.90%）；移除低熵正则化导致数值位置熵大幅上升（1B: +8.10%, 7B: +3.80%）；移除文本-视觉证据匹配使匹配度（Match）下降最为明显（1B: -8.20%, 7B: -6.00%）。这些证据共同表明，结构-细节分离与数值-视觉对齐是 Twin-T 性能增益的核心来源。

Twin-T 的核心设计围绕一个因果瓶颈展开：**现有 VLM 在图表表格任务中未能显式分离结构线索与细粒度细节，导致数值读取错误和不可靠的生成**。为此，Twin-T 引入两条关键创新路径——双头图像编码器实现结构-细节分离与柔性融合，以及 MINT 偏好学习强化数值关键词准确性和文本-视觉对齐。整个方法分为两个训练阶段，其工作流如 Figure 2 所示。

### 阶段一：双头视觉编码与 Schur 融合

阶段一的目标是让 VLM 学会从图表图像中解耦结构信息（轴、网格、布局）与细节信息（数值、图例、标签）。具体流程如下：

1. **结构图像提取**：对原始图像应用 **Canny 边缘检测算法**，生成仅保留边缘轮廓的结构图像。该图像捕获了图表的骨架信息，但丢失了颜色、纹理等细粒度细节。
2. **双头编码**：将原始图像 $I_{\text{Img}}$ 和结构图像 $I_{\text{Stru}}$ 分别送入**共享的、可训练的视觉编码器**，得到原始嵌入 $E_{\text{Img}}$ 和结构嵌入 $E_{\text{Stru}}$。共享编码器确保两种表征处于同一语义空间。
3. **结构软门控**：为抑制结构嵌入中的噪声并稳定后续融合，引入基于 L2 范数的软门控机制。首先计算每个 token 的结构嵌入范数：

$$
\|E_{\mathrm{Stru}}[b,t,:]\|_2 = \sqrt{\sum_{d=1}^{D_{\mathrm{vis}}} (E_{\mathrm{Stru}}[b,t,d])^2} \tag{1}
$$

其中 $b$ 为批次索引，$t$ 为 token 索引，$D_{\mathrm{vis}}$ 为视觉嵌入维度。随后通过带温度参数 $\alpha$ 和阈值 $\tau$ 的 Sigmoid 函数生成门控权重：

$$
w_{\mathrm{Stru}}[b,t] = \sigma(\alpha(\|E_{\mathrm{Stru}}[b,t,:]\|_2 - \tau)) \tag{2}
$$

该门控对标量范数进行平滑抑制：范数远低于 $\tau$ 的 token 权重趋近于 0（视为噪声），远高于 $\tau$ 的 token 权重趋近于 1（保留强结构信号）。

4. **Schur 风格结构去除**：为从原始嵌入中剥离结构分量以获得纯细节嵌入，采用无参数的 Schur 风格投影。首先计算结构方向上的投影系数 $\gamma[b,t]$，然后从 $E_{\text{Img}}$ 中减去投影分量：

$$
E_{\mathrm{Det}}[b,t] = E_{\mathrm{Img}}[b,t] - \gamma[b,t] \, w_{\mathrm{Stru}}[b,t]^2 \, \mathrm{proj}(E_{\mathrm{Img}}[b,t]) \tag{4}
$$

其中 $\mathrm{proj}(\cdot)$ 将原始嵌入投影到结构子空间，$w_{\mathrm{Stru}}^2$ 作为衰减因子控制去除强度。这一步的直觉是：原始图像包含“结构 + 细节”，减去结构投影后，残差即为细节信号。

5. **柔性融合**：最终将细节嵌入与结构嵌入按学习到的权重组合：

$$
E_{\mathrm{fuse}}[b,t] = w_{\mathrm{Det}}[b,t] E_{\mathrm{Det}}[b,t] + w_{\mathrm{Stru}}[b,t] E_{\mathrm{Stru}}[b,t] \tag{5}
$$

融合嵌入 $E_{\text{fuse}}$ 随后经连接器送入 LLM，完成端到端训练。整个阶段一的模块消融（Table 5）证实：移除双头编码器导致总体性能下降约 5%，验证了结构-细节分离的关键性。

![[assets/figures/papers/paper_list_l2751_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Twin_T_TwintVQA_A/figures/010_Table_5.jpg]]
*Table 5: Ablation experiments of Stage 1 modules*

### 阶段二：MINT 偏好学习

阶段二在阶段一的基础上，通过偏好优化进一步校准生成行为，核心包含三个损失组件。

#### 数值关键词对比损失

图表表格 QA 中，数值和比较关键词（如“大于”、“小于”、“等于”）的准确性至关重要。MINT 为每个 token 分配权重：

$$
W[b,t] = \mathrm{norm}(1 + M_{\mathrm{num}}[b,t] + M_{\mathrm{key}}[b,t]) \tag{6}
$$

其中 $M_{\mathrm{num}}$ 和 $M_{\mathrm{key}}$ 分别为数值 token 和比较关键词 token 的二值掩码。加权后的对比损失为：

$$
\mathcal{L}_{\mathrm{NK}} = \frac{1}{N} \sum_{t=0}^{N} W_{[b,t]} \left[ - (\ell_{[b,t]}^{\mathrm{ch}} - \ell_{[b,t]}^{\mathrm{rj}}) \right]_{+} \tag{7}
$$

其中 $\ell^{\mathrm{ch}}$ 和 $\ell^{\mathrm{rj}}$ 分别为选中响应和拒绝响应的对数概率，$[\cdot]_{+}$ 为 hinge 损失。该损失强制模型在数值和关键词位置偏好正确响应。

#### 低熵正则化

为抑制数值生成的不确定性，在数值 token 位置施加熵正则化：

$$
H_{[b,t]} = - \sum_{v=1}^{V} p[b,t](v) \log p[b,t](v) \tag{8}
$$

其中 $p[b,t](v)$ 为词表第 $v$ 个 token 的预测概率。该正则项鼓励模型在数值位置输出低熵（即高置信度）的分布，减少数值幻觉。

#### 文本-视觉证据匹配损失

为提升生成文本与视觉证据的对齐度，引入匹配损失：

$$
\mathcal{L}_{\mathrm{TV}} = \frac{1}{B} \sum_{b=1}^{B} \left[ - \left( \mu(Mat_{\mathrm{txt-vis}}^{\mathrm{ch}}[b]) - \mu(Mat_{\mathrm{txt-vis}}^{\mathrm{rj}}[b]) \right) \right]_{+} \tag{10}
$$

其中 $Mat_{\mathrm{txt-vis}}$ 为文本片段与对应视觉区域的对齐分数，$\mu(\cdot)$ 为均值聚合。该损失推动模型在生成答案时更紧密地引用视觉证据。

### 消融验证

Table 6 的消融实验为各组件的有效性提供了决定性证据：
- 移除数值关键词偏好（w/o Num-Key）导致数值准确性（NK Acc）大幅下降（1B: −2.70%, 7B: −5.90%）。
- 移除低熵正则化（w/o Low-Ent）导致熵大幅上升（1B: +8.10%, 7B: +3.80%），表明其稳定数值生成的作用。
- 移除文本-视觉证据匹配（w/o Txt-Vis）导致匹配度（Match）最大下降（1B: −8.20%, 7B: −6.00%），证明其提升视觉对齐的关键性。

![[assets/figures/papers/paper_list_l2751_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Twin_T_TwintVQA_A/figures/009_Table_6.jpg]]
*Table 6: Ablation experiments of Stage 2 modules*

总体而言，MINT 偏好学习从三个维度——数值准确性、生成稳定性和视觉对齐——协同提升了图表表格任务的可靠性。

## 实验与关键发现

### 主实验结果

Twin-T 在多个图表表格基准上取得了领先或极具竞争力的表现。**Table 1** 汇总了公开基准上的性能：Twin-T-7B 以 719.94 的总分（Overall）位居第一，超越了 GPT-4o、Gemini-2.5-Pro 等闭源大模型，并大幅领先开源的图表专家模型 **ChartAst-13B**（Meng et al., arXiv 2024）和 **ChartVLM-8B**（Xia et al., IEEE TIP 2025）。Twin-T-1B 尽管参数规模仅 1B，仍取得了 576.20 的总分，超过多数更大规模模型。

![[assets/figures/papers/paper_list_l2751_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Twin_T_TwintVQA_A/figures/004_Table_1.jpg]]
*Table 1: Performance results on public chart-table benchmarks. Best scores are highlighted in blue, and second-best scores in green; CharXivD and*

具体子任务上，Twin-T-7B 在 CharXiv 推理子集（CharXiv_R）上达到 57.10%，比 GPT-4o 的 47.80% 高出 **+9.30 个百分点**；在 TableVQA 上达到 80.27%（GPT-4o 为 77.82%）；在 AI2D 上达到 90.77%，略胜 Gemini-2.5-Pro 的 89.80%。在作者自建的 **TwintVQA** 基准上，Twin-T-7B 以 70.20% 超越 GPT-4o 的 67.06%（+3.14 pp），Twin-T-1B 也达到 58.08%，接近 GPT-4o 水平。

上述结果表明，结构-细节分离的双头编码器与 MINT 偏好学习的组合，使小模型在图表表格领域获得了与大模型竞争甚至超越的能力。**Figure 1** 直观展示了 Twin-T 在公开基准和整体性能上的优势位置。

![[assets/figures/papers/paper_list_l2751_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Twin_T_TwintVQA_A/figures/001_Figure_1.jpg]]
*Figure 1: Our Twin-T (1B/7B) VLM outperforms other models on chart–table tasks. It surpasses GLM-4.5V-106B and is even competitive with GPT-4o and Gemini-2.5. Zoom in for more details*

### 任务类型与图表类型分析

**Table 2** 按任务类型和回答长度分解了 TwintVQA 上的表现。Twin-T-7B 在多项选择题（MC）上达到 91.36%，在数值问答（NQA）上达到 76.04%，显著优于开源基线。值得注意的是，在代码生成类任务（如 Chart-to-Python, C2P）上，Twin-T 仍落后于 GPT-4o 和 Gemini-2.5-Pro，这暗示代码对齐监督和更大模型容量的必要性。

**Table 3** 按图表类型分析显示，Twin-T-7B 在结构密集的图表类型上优势尤为明显——如柱状图（Bar）、箱线图（Box）、组合图（Composite）和环形图（Donut）——这验证了结构分离设计对利用全局布局信息的有效性。

### 阶段消融实验

**Table 4** 报告了两阶段训练的消融结果。仅使用 Stage 1（双头编码器）已带来显著增益；叠加 Stage 2（MINT 偏好学习）后，TwintVQA 和公开基准上的性能进一步提升。这确认了结构分离与数值偏好学习是互补的因果杠杆。

### Stage 1 模块消融

**Table 5** 对双头编码器的关键组件进行消融。移除双头编码器（即回退到单头标准 VLM）导致总体性能下降约 **5%**，这是最强的决定性证据，直接验证了结构-细节分离的核心主张。移除 Schur 式融合或结构软门控也造成明显退化，说明参数自由的冗余去除和噪声抑制对融合质量至关重要。

### Stage 2 模块消融

**Table 6** 对 MINT 偏好学习的三个损失项进行消融，分别考察了数值准确率（NK Acc）、输出熵（Entropy）和文本-视觉匹配度（Match）三个诊断指标：

- **移除数值关键词偏好（Num-Key Pref）**：NK Acc 在 1B 模型下降 2.70%，7B 模型下降 5.90%，证明数值和比较关键词的加权对比学习是提升数值精度的关键。
- **移除低熵正则化（Low-Entropy Reg）**：熵值在 1B 模型上升 8.10%，7B 模型上升 3.80%，表明该正则项有效抑制了数值位置的输出不确定性，稳定了数值生成。
- **移除文本-视觉证据匹配（Text-Vis Evidence）**：Match 指标在 1B 模型下降 8.20%，7B 模型下降 6.00%，降幅最大，证明该损失项对增强视觉对齐、使生成内容更忠实于图像证据具有最强约束力。

### 超参数敏感性

**Figure 4** 展示了 Stage 1 中软门控温度 α、阈值 τ 和融合权重 λ 的影响。在公开基准（不含 TwintVQA）的聚合分数上，性能对 α 和 τ 在一定范围内相对鲁棒，但偏离最优区间后下降明显；λ 控制细节与结构的融合比例，存在明确的最优值。这为实际部署提供了调参指引。

### 失败模式与局限性

尽管整体表现优异，Twin-T 在以下场景存在明显不足：

1. **OCR 密集型任务**：在需要密集文本读取的场景，Twin-T 仍落后于 GPT-4o 等大模型，可能受限于视觉编码器的分辨率或训练数据中 OCR 样本的覆盖度。
2. **Chart-to-Python（C2P）**：代码生成任务性能较低，需要代码对齐的监督信号和更大模型容量来弥补。
3. **结构提取方法单一**：当前仅使用 Canny 边缘检测提取结构图像，可能丢失细粒度纹理信息，更丰富的结构提取策略（如深度结构表征）有待探索。

### 小结

实验证据链完整且一致：双头编码器实现的结构-细节分离是性能提升的**瓶颈突破点**（移除后降 ~5%），MINT 偏好学习通过数值加权、熵正则和视觉匹配三个互补机制**精细化生成质量**（各项消融均有显著退化）。二者协同使 Twin-T 在图表表格理解任务上以小规模参数取得领先结果。

![[assets/figures/papers/paper_list_l2751_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Twin_T_TwintVQA_A/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our TwintVQA benchmark. It covers 17 image types (e.g., bar, pie, line, bubble, heatmap, radar, donut, sankey, scatter, rose, box, waterfall, stacked, candle, gantt, composite, table) and 11 task types across 3 data formats (Image, LaTeX, Python), including Table→ LaTeX (T2L), Chart→Python (C2P), Image / LaTeX / Python Analysis and Summary (IA / LA / PA and IS / LS / PS), Multiple Choice (MC), Numerical QA (NQA), and Open QA (OQA). The right panel shows the length distribution for questions and answers with three bands: Short (0, 256], Medium (256, 1024], and Long (1024, 4096] tokens. Zoom in for more details*

## 定位与知识库关联

### 与通用VLM基线的结构差异

Twin-T 并非从零构建视觉语言模型，而是将结构-细节分离机制嵌入现有通用VLM骨架。论文选用了两个代表性基线：**Ovis2-1B**（Lu et al., arXiv 2024）和**Qwen2.5-VL-7B**（Bai et al., arXiv 2025），分别构建Twin-T-1B和Twin-T-7B。这种设计选择本身传递了一个信号：所提出的双头编码器和MINT偏好学习是架构无关的插件式改进，而非依赖特定视觉骨干的定制方案。

与通用VLM的关键分岔点在于视觉编码阶段。标准VLM（包括上述两个基线及**GPT-4o**、**Gemini-2.5-Pro**等闭源模型）使用单头编码器直接从原始图像提取统一的视觉表征。Twin-T在此插入了一个无参数的Schur风格融合模块，使模型能够分别处理Canny结构图像和原始图像，再通过软门控和投影去除冗余结构分量后融合。这一改动不改变原始图像编码器的权重结构，仅增加了推理时的双路前传和融合计算。

### 与图表专家VLM的定位关系

在图表表格专家模型谱系中，Twin-T与**ChartAst-13B**（Meng et al., arXiv 2024）和**ChartVLM-8B**（Xia et al., IEEE TIP 2025）形成直接对比。后两者同样针对图表理解进行了专门设计，但方法路径不同：它们通常依赖单一视觉通路加任务特定的微调策略，未显式建模结构线索与细粒度细节的分离。

Twin-T的核心区分点在于**因果机制的显式化**：它不仅追求更高的基准分数，更试图通过结构-细节分离这一可控变量来提升数值准确性——这是图表表格QA中最易出错且后果最严重的失败模式。从Table 1的结果看，Twin-T-7B在CharXiv推理子集（CharXiv_R）上达到57.10%，比GPT-4o高出9.30个百分点，在TableVQA上达到80.27%（+2.45% vs GPT-4o），表明结构-细节分离在需要精确数值推理的场景中具有不可替代的优势。

### 适用边界与已知局限

尽管Twin-T在多数图表表格任务上表现强劲，其方法设计本身划定了明确的适用边界：

**结构提取的单一性约束。** Stage 1仅使用Canny边缘检测提取结构图像。Canny对强边缘敏感，能有效捕获轴、网格线、柱状边界等宏观结构，但会丢失颜色填充、渐变、阴影等细粒度纹理信息。对于热力图（heatmap）、气泡图（bubble chart）等依赖连续颜色编码的图表类型，Canny结构图像可能无法提供充分的布局线索。论文未探索更丰富的结构提取方法（如深度边缘检测、语义分割掩码），这是一个显式的设计局限。

**OCR密集场景的代偿不足。** 论文明确指出，Twin-T在OCR密集型和代码重建任务上仍落后于更大规模的模型。这一局限的根源可能在于双头编码器虽然增强了结构理解，但并未增加文本识别能力——OCR性能仍受限于底层VLM的视觉编码器容量和训练数据中的文本覆盖度。对于密集表格转LaTeX（T2L）等任务，结构分离的收益被OCR瓶颈所掩盖。

**Chart-to-Python的代码对齐缺口。** Chart-to-Python（C2P）任务要求模型从图表图像生成可执行的可视化代码，Twin-T在此任务上性能较低。论文将此归因于缺少代码对齐的监督信号和模型容量不足。这暗示MINT偏好学习中的数值关键词加权和低熵正则化主要针对自然语言答案设计，尚未扩展到代码生成的语法约束和逻辑一致性层面。

### 消解证据的强度与边界

Table 5的消融实验提供了结构-细节分离因果性的最强证据：移除双头编码器导致总体性能下降约5%。但需注意，这一下降是在完整TwintVQA基准上的聚合结果，不同任务类型的敏感度可能差异显著——数值QA（NQA）的下降幅度可能远大于多选题（MC），但论文未提供分任务消融数据，此点需手动验证。

Table 6的MINT模块消融揭示了各损失项的独立贡献：移除数值关键词偏好（Num-Key）导致NK Acc下降2.70%-5.90%；移除低熵正则化导致熵上升3.80%-8.10%；移除文本-视觉证据匹配导致Match下降6.00%-8.20%。这些数据支撑了MINT三重目标的各自有效性，但需注意这些消融是在Stage 2已收敛的基础上进行的单模块移除，未探索模块间的交互效应——例如，同时移除Num-Key偏好和低熵正则化是否会产生大于单独移除之和的退化，论文未给出答案。

### 开放问题与延伸方向

结构-细节分离的泛化性是一个自然延伸问题。论文将分离机制限定在图表表格领域，但该思路可能适用于其他需要同时处理全局布局和局部细节的视觉推理任务，如文档理解（页面结构 vs 文字内容）、医学影像（器官轮廓 vs 病灶纹理）、卫星图像（地理边界 vs 地物细节）。然而，Canny边缘在这些领域是否仍是合适的结构提取器，需要任务特定的验证。

Chart-to-Python的性能瓶颈指向一个更深层的问题：当前的结构-细节分离是在视觉嵌入空间进行的，而代码生成需要将视觉结构映射为程序语法结构。这可能需要一个跨模态的结构对齐机制，而非仅在视觉端进行分离。论文的MINT框架尚未覆盖这一跨模态结构映射，这是未来工作的明确方向。

自动结构图像生成的质量与效率平衡也值得关注。Canny作为手工设计的边缘检测器，虽然计算高效且无需训练，但其固定参数（双阈值）可能不是所有图表类型的最优选择。是否可以通过轻量可学习的结构提取器替代Canny，在保持高效的同时提升结构图像的质量，是一个开放的设计选择。

## 原文 PDF

![[paperPDFs/CVPR_2026/Twin_T_and_TwintVQA_A_Reliable_Structure_Detail_Separating_VLM_and_a_Comprehensive_Benchmark_for_Chart_and_Table_Tasks.pdf]]

---
title: "DynamicsBoost: Dynamic Plausible Video Generation via Annotation-Free Continuation Preference Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DynamicsBoost_Dynamic_Plausible_Video_Generation_via_Annotation_Free_Continuation_Preference_Optimization.pdf
project_link: null
code_link: "https://github.com/huggingface/trl"
aliases:
- DynamicsBoost
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 视频延续过程中提供的参考帧数量——更多参考帧意味着更少的生成内容，从而得到更高保真度的视频，自然诱导出单调的偏好顺序。
primary_logic: 视频延续任务天然产生结构一致且长度有序的偏好对，无需任何人工标注或奖励模型，即可构建高质量、可规模化的偏好数据。
claims:
- 随着参考帧数量增加，视频质量单调提升，且该趋势与VLM偏好判断强相关，验证了延续长度作为有效无监督偏好信号的合理性。
- 仅在非共享延续区域（Regions 2-3）计算DPO损失，使各项VBench指标显著优于全视频损失，证明非对称设计能精准对齐偏好信号。
- 所提方法在VBench、VideoGen-Eval和PhysGenBench上均取得最佳运动真实性、时序一致性和语义对齐，全面超越现有DPO基线。
- "VBench (Ab: standard DPO vs. our loss region) 上 Overall Consistency = 25.64"
---

# DynamicsBoost: Dynamic Plausible Video Generation via Annotation-Free Continuation Preference Optimization

> [!tip] 核心洞察
> 视频延续任务天然产生结构一致且长度有序的偏好对，无需任何人工标注或奖励模型，即可构建高质量、可规模化的偏好数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | DynamicsBoost：基于无标注视频延续偏好的动态合理视频生成 |
| 英文题名 | DynamicsBoost: Dynamic Plausible Video Generation via Annotation-Free Continuation Preference Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_DynamicsBoost_Dynamic_Plausible_Video_Generation_via_Annotation-Free_Continuation_Preference_Optimization_CVPR_2026_paper.html) · [Code](https://github.com/huggingface/trl) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | DynamicsBoost |
| Dataset | VBench, VideoGen-Eval |

> [!tip] 效果简介
> - VBench (Ab: standard DPO vs. our loss region) 上，Overall Consistency 25.64 vs 22.15 (+3.49)；Motion Smoothness 99.21 vs 97.21 (+2.00)；Dynamic Degree 44.92 vs 42.48 (+2.44)。
> - VBench (quantitative comparison with baselines) 上，overall best vs Flow-DPO, Flow-StructuralDPO, Flow-DenseDPO (significant improvement)。
> - VideoGen-Eval 上，Overall Consistency 25.12 vs N/A (outperforms baselines)。

## 概要

**核心瓶颈**：视频生成模型的偏好对齐长期受困于高质量偏好标注的获取难题——人工评估成本高昂且难以稳定复现，VLM评估存在模糊性，导致规模化偏好训练举步维艰。

**核心洞察**：视频延续任务天然蕴含单调的偏好信号——给定更多参考帧意味着更少的生成内容，从而获得更高保真度的延续结果。这一结构特性使得无需任何人工标注或奖励模型，即可自动构建高质量、可规模化的偏好数据对。

**方法定位**：**DynamicsBoost**（CVPR 2026）提出了一套完整的无标注偏好对齐框架。首先将预训练文生视频模型扩展为支持任意帧条件的潜空间延续模型；随后通过不同延续长度采样自动生成结构匹配的输赢样本对；最后引入**非对称DPO**（Asymmetrical DPO），仅对非共享延续区域计算偏好损失并按延续帧数归一化，确保偏好信号精准作用于生成区域。

**方法谱系**：DynamicsBoost 属于视频生成的直接偏好优化（DPO）方法族，与 **Flow-DPO**（Liu et al., arXiv 2025）、**Flow-StructuralDPO** 和 **Flow-DenseDPO**（Wu et al., arXiv 2025）等现有工作形成对比。后者的共同特征是依赖外部标注或奖励模型构造偏好对，DynamicsBoost 则以视频延续长度作为无监督偏好信号，从根本上消除了标注依赖。在模型训练策略上，仅优化 LoRA 适配器和帧级任务提示嵌入，冻结预训练骨干网络，实现了轻量高效的偏好对齐。

**主要结果**：在 VBench、VideoGen-Eval 和 PhysGenBench 三个基准上，DynamicsBoost 一致取得运动真实性、时序一致性和语义对齐的最优表现，全面超越现有 DPO 基线。消融实验证实：非对称损失区域选择（Regions 2-3）相比全视频损失，VBench Overall Consistency 提升 +3.49（25.64 vs. 22.15），Motion Smoothness 提升 +2.00（99.21 vs. 97.21）；双向随机延续采样策略优于固定长度策略。延续质量随参考帧数量单调提升的趋势与 VLM 偏好判断强相关，验证了延续长度作为有效偏好信号的合理性。

**待验证边界**：该方法仅在单一基模型（Wan）、固定分辨率（288×512）和固定帧数（49帧）条件下验证，对不同架构和尺度的泛化性尚需进一步检验。



### 视频生成中的动态合理性困境

近年来，基于扩散模型和流匹配的文本到视频（T2V）生成取得了显著进展，但在动态合理性（dynamic plausibility）方面仍面临根本性挑战。现有模型生成的视频往往存在运动不自然、时序不一致、物理规律违背等问题，这限制了其在影视制作、虚拟现实等对动态真实性要求较高的场景中的应用。

偏好对齐技术（如RLHF、DPO）在提升大语言模型输出质量方面取得了巨大成功，自然地被引入视频生成领域以改善动态质量。其核心思路是：收集人类或视觉语言模型（VLM）对生成视频的质量偏好判断，构建“胜出-失败”样本对，通过偏好优化引导模型向高质量方向更新。

### 核心瓶颈：高质量偏好标注的规模化困境

然而，视频生成的偏好对齐面临一个关键瓶颈：**高质量偏好标注的获取成本极高且存在固有模糊性**。与文本生成不同，视频质量涉及运动平滑度、时序一致性、物理合理性、语义对齐等多个维度，人工评估者难以在这些维度上保持稳定、一致的判断标准。即使借助VLM作为自动化评估器，其评分也受限于VLM自身的感知偏差和跨场景泛化能力。这一瓶颈使得现有视频偏好优化方法（如**Flow-DPO**（Liu et al., arXiv 2025）、**Flow-StructuralDPO** 和 **Flow-DenseDPO**（Wu et al., arXiv 2025））难以规模化扩展——偏好数据的质量和数量直接制约着对齐效果的上限。

### 本文动机：利用视频延续的内在偏好信号

DynamicsBoost 的核心洞察在于：**视频延续任务天然产生结构一致且长度有序的偏好对，无需任何人工标注或奖励模型**。具体而言，给定一段真实视频的前若干帧作为条件，让模型生成后续帧——提供的参考帧越多，模型需要生成的内容越少，生成的视频片段保真度越高、与原始视频的结构一致性越强。这种“更多参考帧→更少生成内容→更高质量”的单调关系，为偏好对齐提供了一种天然、可规模化且无成本的监督信号。

基于这一洞察，DynamicsBoost 将预训练 T2V 模型扩展为支持任意帧条件生成的延续模型，通过采样不同延续长度自动构造“输-赢”偏好对，并引入非对称 DPO（Asymmetrical DPO）损失——仅在非共享的延续帧区域计算偏好损失并做长度归一化——从而精准对齐偏好信号，避免共享条件帧对损失计算的干扰。整个流程无需人工标注、无需奖励模型训练，即可实现视频动态质量和语义一致性的显著提升。



## 核心方法与创新机理

DynamicsBoost 的核心创新在于**将视频延续任务重构为一种天然、无标注的偏好信号源**，从而彻底绕过了视频生成偏好对齐中长期存在的标注瓶颈。与现有 DPO 方法依赖人工标注或 VLM 评判来构造“好/坏”样本对不同，该方法通过一个简洁的因果控制旋钮——**参考帧数量**——自动生成结构一致且质量单调有序的偏好对。

具体而言，该方法包含三个紧密耦合的创新槽位：

**1. 偏好对构造方式：从人工标注到延续长度自动诱导**

现有 DPO 基线（如 **Flow-DPO** (Liu et al., arXiv 2025)、**Flow-StructuralDPO** (Wu et al., arXiv 2025)）依赖人工或 VLM 标注的正负样本对，成本高昂且评判标准模糊。DynamicsBoost 的核心洞见是：在视频延续任务中，**提供的参考帧越多，模型需要生成的内容越少，输出视频的保真度和动态合理性就越高**。这一单调关系使得不同延续长度自然形成“输-赢”偏好顺序——延续长度短（生成部分长）的样本为输家，延续长度长（生成部分短）的样本为赢家。整个过程无需任何外部标注器或奖励模型，即可规模化构建高质量偏好数据（Sec 3.2）。

**2. DPO 损失计算区域：从全视频到非对称延续区域**

标准 Flow-DPO 对整个视频的所有帧计算偏好损失，但这会引入一个关键问题：输赢样本对共享的条件帧区域（即参考帧部分）内容完全一致，在该区域计算损失不仅无助于偏好学习，反而会引入噪声并稀释真正的偏好信号。DynamicsBoost 提出**非对称 DPO（Asymmetrical DPO）**，仅对非共享的延续帧区域（Regions 2-3）计算损失，并按延续帧数进行归一化（Sec 3.3）。消融实验（Table 4）证实，这一设计使 VBench 的 Overall Consistency 从 22.15 提升至 25.64（+3.49），Motion Smoothness 从 97.21 提升至 99.21（+2.00），证明了精准对齐偏好信号的有效性。

**3. 模型训练策略：从全模型微调到参数高效冻结**

为保护预训练基模型（**Pretrained Wan model**, Team Wan et al., arXiv 2025）的泛化能力，DynamicsBoost 仅优化 LoRA 适配器和帧级任务提示嵌入，完全冻结预训练骨干网络（Sec 3.2 Eq. (5)）。这种参数高效策略不仅降低了训练成本，还避免了全模型微调可能导致的灾难性遗忘。

三个创新槽位形成了一条完整的因果链：延续长度差异提供无标注偏好信号 → 非对称损失区域确保信号精准作用于生成质量差异部分 → 参数高效训练保护基模型能力。这一设计使得 DynamicsBoost 在 VBench、VideoGen-Eval 和 PhysGenBench 上均取得最优的运动真实性、时序一致性和语义对齐（Table 1, Table 2），全面超越现有 DPO 基线。



DynamicsBoost 的核心思路是将视频延续（video continuation）过程的天然偏好信号转化为可规模化的偏好对齐训练框架。整个流水线由三个关键模块串联构成：**视频延续模型**、**偏好对生成器**和**非对称DPO训练器**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2674_https_openaccess_thecvf_com_content_CVPR2026_html_Li_DynamicsBoost_Dynam/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the DynamicsBoost pipeline. We extend a pretrained video generator into a continuation-based preference model (a), then sample continuation pair of different lengths and optimize them with Asymmetrical DPO (b). This pipeline automatically constructs high-quality, scalable and structurally aligned ordered data and yields video generations with improved fidelity and dynamic plausibility*

**视频延续模型**负责将预训练的文本到视频（T2V）生成器扩展为支持任意帧条件生成的延续模型。具体而言，该模块在预训练骨干网络（**Wan**，Team Wan et al., arXiv 2025）中引入两个关键设计：一是可学习的帧级任务提示嵌入 $P_{\mathrm{task}}$，通过二值掩码 $M$ 区分条件帧与目标帧；二是掩码时间步机制，将条件帧的时间步置零，使模型仅对目标帧进行去噪预测。延续训练损失仅在目标帧区域上监督，冻结预训练骨干，仅优化 LoRA 适配器和任务提示嵌入。

**偏好对生成器**利用视频延续的自然特性自动构造偏好数据。对于同一段视频，采用不同的延续长度 $N_1$ 和 $N_2$（$N_1 < N_2$）进行采样：$N_1$ 对应更少的参考帧、更多的生成内容，产生质量较低的“失败”样本；$N_2$ 对应更多的参考帧、更少的生成内容，产生质量较高的“胜出”样本。这种构造方式无需任何人工标注或奖励模型，天然诱导出结构匹配且长度有序的偏好对。

**非对称DPO训练器**是偏好对齐的核心。与标准 Flow-DPO 在整个视频上累积偏好损失不同，Asymmetrical DPO 仅对非共享延续区域（即 Regions 2-3）计算损失，并按延续帧数 $N - \min(N_1, N_2)$ 进行归一化。这一设计确保了偏好信号精准作用于生成区域，而非共享的条件帧区域，从而有效对齐视频动态质量与语义一致性。

整个流水线的输入是预训练 T2V 模型和动态视频数据集（如 OpenVid-1M 子集），输出是经过偏好对齐的视频生成模型，在运动真实性、时序一致性和文本对齐方面均显著优于现有 DPO 基线。



### 3.1 流匹配与偏好优化基础

DynamicsBoost 建立在流匹配（Flow Matching）与扩散偏好优化的统一框架之上。给定视频潜变量 $x_0$（真实数据）和 $x_1$（噪声），流匹配训练目标为最小化预测速度与真实速度之间的均方误差：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t,x_0,x_1}\big[||v_\theta(x_t,t) - (x_1 - x_0)||_2^2\big] \tag{1}$$

其中 $x_t = (1-t)x_0 + tx_1$ 为线性插值路径，$v_\theta$ 为速度预测网络。

在偏好对齐层面，扩散 DPO 通过比较胜出样本与失败样本的噪声预测误差来优化模型：

$$\mathcal{L}_{\mathrm{Diffusion-DPO}} = -\log\sigma\!\left(-\frac{\beta}{2}\Delta\mathcal{E}_\varepsilon\right) \tag{2}$$

其中 $\Delta\mathcal{E}_\varepsilon$ 为胜/败样本在去噪误差上的累积差异，$\beta$ 控制偏好强度。Flow-DPO 在整流流参数化下与上述扩散 DPO 数学等价，速度空间形式为：

$$\mathcal{L}_{\mathrm{Flow-DPO}} = -\log\sigma\!\left(-\frac{\beta(1-t)^2}{2}\Delta\mathcal{E}_v\right) \tag{3}$$

该等价性为后续在流匹配视频模型中实施偏好优化提供了理论保证。

### 3.2 视频延续模型与偏好对自动构造

**核心洞察**：视频延续过程中，提供的参考帧越多，模型需要生成的内容越少，输出质量单调提升。这一自然属性使延续长度成为有效的无监督偏好信号。

**延续模型扩展**。将预训练 T2V 模型改造为支持任意帧条件生成的延续模型，关键操作包括：

- **掩码时间步**：对条件帧赋予零时间步，使其在流匹配过程中保持为干净潜变量。给定二值掩码 $M$（条件帧位置为 1，目标帧位置为 0），掩码时间步定义为：

$$t' = t \cdot (1-M)$$

- **非均匀加噪**：基于掩码时间步对视频潜变量进行差异化加噪：

$$z_t' = (1 - t') z_0 + t' z_1$$

- **帧级任务提示**：通过可学习嵌入区分条件帧与目标帧的角色：

$$P_{\mathrm{task}} = M \odot P_{\mathrm{cond}} + (1-M) \odot P_{\mathrm{noisy}}$$

其中 $P_{\mathrm{cond}}$ 和 $P_{\mathrm{noisy}}$ 分别为条件帧与目标帧的可学习提示嵌入。

延续训练损失仅在目标帧上监督：

$$\mathcal{L} = \mathbb{E}\Big[\|(1-M)\odot((z_1-z_0)-v_\Phi(z_t',t',P_{\mathrm{task}}))\|^2\Big] \tag{4}$$

训练时仅优化 LoRA 适配器和任务提示嵌入 $\{P_{\mathrm{cond}}, P_{\mathrm{noisy}}\}$，冻结预训练骨干网络。

**偏好对构造**。对同一视频，采样两个不同的延续长度 $N_1 < N_2$（即提供不同数量的参考帧），生成两个延续结果。由于 $N_2$ 对应的生成段更短，其质量天然优于 $N_1$ 对应的结果，自动形成结构匹配的“胜-败”偏好对，无需任何人工标注或奖励模型。

### 3.3 非对称 DPO

标准 DPO 在整个视频上累积偏好损失，但偏好对中胜/败样本共享相同的条件帧区域（Region 1），该区域不应参与偏好比较。DynamicsBoost 提出非对称 DPO，仅对非共享延续区域计算损失：

$$\mathcal{L}_{\mathrm{AsymDPO}} = -\frac{1}{N-\min(N_1,N_2)}\log\sigma(-\beta\cdot\Delta\mathcal{E}) \tag{4}$$

其中误差差异累积项 $\Delta\mathcal{E}$ 仅在延续帧上求和：

$$\Delta\mathcal{E} = \sum_{i=\min(N_1,N_2)}^{N}\big(\lVert v_i^w - v_\theta(x_{t,i}^w,t)\rVert^2 - \lVert v_i^l - v_\theta(x_{t,i}^l,t)\rVert^2\big) \tag{5}$$

$v_i^w$、$v_i^l$ 分别为胜/败样本在第 $i$ 帧的目标速度，损失按实际延续帧数 $N-\min(N_1,N_2)$ 归一化。这一设计确保偏好信号精准作用于生成区域，避免条件帧对损失计算的干扰。

**关键消融证据**：仅在非共享延续区域（Regions 2-3）计算 DPO 损失，VBench Overall Consistency 从全视频损失的 22.15 提升至 25.64（+3.49），Motion Smoothness 从 97.21 提升至 99.21（+2.00），验证了非对称设计的有效性（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l2674_https_openaccess_thecvf_com_content_CVPR2026_html_Li_DynamicsBoost_Dynam/figures/007_Figure_4.jpg]]
*Figure 4: Continuation results under different numbers of reference frames (indicated at the top-left of each example). Nonzero reference settings produce continuations that better preserve structural consistency with the original video, and quality improves monotonically as the number of reference frames increases—approaching the ground truth when all frames are used. In contrast, the pure T2V setting exhibits significant structural deviation, breaking this monotonic relationship*



## 实验与关键发现

### 实验设置

**基模型与基线**。以预训练 **Wan** 模型（Team Wan et al., arXiv 2025）为骨干网络，冻结其参数，仅优化 LoRA 适配器和帧级任务提示嵌入。对比基线包括：监督微调（**SFT**）、**Flow-DPO**（Liu et al., arXiv 2025）、**Flow-StructuralDPO**（Wu et al., arXiv 2025）和 **Flow-DenseDPO**（Wu et al., arXiv 2025）。

**训练数据**。从 OpenVid-1M 中筛选 100K 动态丰富的高质量视频：80K 用于延续训练，20K 作为条件输入。所有视频标准化为 49 帧、分辨率 288×512。延续训练中，条件帧数 $N_{\text{cond}}$ 在 $\{1,2,4,8,13\}$ 中随机采样；DPO 训练中，采用双向随机延续策略，负样本延续长度 $N_1 \in [1, 0.6N]$，正样本延续长度 $N_2 \in [0.8N, N]$。

**评估基准**。在三个维度互补的基准上评估：**VBench**（综合视频质量）、**VideoGen-Eval**（语义一致性与时序连贯性）和 **PhysGenBench**（物理合理性）。

### 主实验结果

**VBench 全面领先**。如表 1 所示，DynamicsBoost 在美学质量（59.92）、成像质量（66.81）、背景一致性（97.53）、运动平滑度（99.21）、动态程度（44.92）和整体一致性（25.64）六项指标上均取得最优或次优，全面超越 Flow-DPO、Flow-StructuralDPO 和 Flow-DenseDPO。其中运动平滑度（99.21）和动态程度（44.92）的提升尤为显著，说明无标注偏好对齐有效增强了视频的动态合理性与连贯性。

**跨基准泛化验证**。在 VideoGen-Eval 上，DynamicsBoost 的整体一致性达到 25.12，优于所有基线方法（Table 2）；在 PhysGenBench 上的物理合理性评估同样取得最佳结果。这表明通过视频延续构造的偏好信号不仅提升感知质量，还增强了生成内容对物理规律的遵循能力。

**定性对比**。Figure 3 的可视化对比显示，DynamicsBoost 生成的视频在语义一致性和动态连贯性上均优于基线方法：基线方法常出现物体形变、运动断裂或语义漂移，而 DynamicsBoost 能更好地保持主体结构并生成自然流畅的运动。

### 消融实验

**延续模型设计**（Table 3）。全延续模型（条件帧 4/13）在运动平滑度（98.69）和动态程度上均优于移除可学习延续提示或掩码时间步的变体。具体而言：移除延续提示导致运动平滑度显著下降，说明帧级任务提示对区分条件帧与生成帧至关重要；移除时间步掩码则使动态程度降低，表明掩码时间步是维持目标帧噪声水平、保障生成质量的关键机制。

**DPO 样本策略**（Table 4）。双向随机延续策略（$N_1 \in [1, 0.6N]$, $N_2 \in [0.8N, N]$）在整体一致性（25.64）和运动平滑度（99.21）上均优于固定长度策略和纯 T2V 条件。固定长度策略因偏好信号强度不足导致对齐效果减弱，纯 T2V 条件则因缺乏结构约束而破坏单调偏好关系。

**非对称损失区域**（Table 4）。仅对非共享延续区域（Regions 2-3）计算 DPO 损失，相比全视频（Regions 1-3）在整体一致性上提升 3.49（22.15 → 25.64），运动平滑度提升 2.00（97.21 → 99.21），动态程度提升 2.44（42.48 → 44.92）。仅对区域 3 计算损失则因忽略部分非共享帧而导致性能下降。这证明非对称设计能精准排除共享条件帧的干扰，使偏好信号严格作用于生成区域。

### 偏好信号有效性验证

**单调偏好关系**。Figure 4 展示了不同参考帧数量下的延续结果：随着参考帧从 0 增加到 13，生成视频与原始视频的结构一致性单调提升，纯 T2V（0 参考帧）则出现显著结构偏离。定量分析进一步表明，该单调趋势与 VLM 偏好判断强相关，验证了延续长度作为无监督偏好信号的合理性。

**VLM 一致性分析**。将不同延续长度下的生成结果交由 VLM 进行偏好判断，发现 VLM 的偏好排序与延续长度高度一致，且偏好强度随长度差增大而增强。这从外部视角佐证了基于延续的偏好构造策略的有效性。

### 失败模式与局限性

**静态场景下的偏好失效**。方法假设生成片段始终劣于真实参考帧，但在静态或极低运动场景中，生成片段与参考帧的质量差异可能不显著，导致偏好对噪声增加，对齐效果下降。论文未对此类场景进行专门分析。

**单一基模型的泛化风险**。所有实验仅基于 Wan 模型，缺少在 CogVideoX、HunyuanVideo 等主流 T2V 架构上的验证，方法的跨架构迁移能力尚不明确。

**固定分辨率和帧数限制**。延续训练和偏好对齐仅在 49 帧、288×512 分辨率下测试，对不同帧数（如长视频）和分辨率的泛化能力待验证。

**启发式长度范围选择**。非对称 DPO 的延续长度范围依赖人工设定，不同场景可能需要调整，缺乏自适应机制。论文未讨论该超参数的敏感性或自动化选择策略。

**公平性评估缺失**。训练数据来源于 OpenVid-1M 子集，可能存在内容与风格偏差，对特定人群、动作或场景的生成质量可能不均衡，但论文未进行公平性或偏见分析。

### 补充图表

![[assets/figures/papers/paper_list_l2674_https_openaccess_thecvf_com_content_CVPR2026_html_Li_DynamicsBoost_Dynam/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison with baselines on PhysGenBench and VideoGen-Eval. Best in bold; second best underlined*

![[assets/figures/papers/paper_list_l2674_https_openaccess_thecvf_com_content_CVPR2026_html_Li_DynamicsBoost_Dynam/figures/006_Table_3.jpg]]
*Table 3: Ablation study on the Continuation Process. Best results are in bold, second best are underlined*

![[assets/figures/papers/paper_list_l2674_https_openaccess_thecvf_com_content_CVPR2026_html_Li_DynamicsBoost_Dynam/figures/008_Table_4.jpg]]
*Table 4: Ablation study on the Asymmetrical DPO Process. Best results are shown in bold, and the second best are underlined*

![[assets/figures/papers/paper_list_l2674_https_openaccess_thecvf_com_content_CVPR2026_html_Li_DynamicsBoost_Dynam/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison with baselines. Our method produces results that are more semantically consistent and dynamically coherent compared to other approaches*



## 定位与知识库关联

### 技术脉络与基线关系

DynamicsBoost 立足于视频生成偏好对齐这一新兴方向，其核心贡献在于**偏好数据构造范式的转变**——从依赖外部标注转向利用任务内在结构自动生成偏好信号。为理解这一转变，需将其置于以下技术脉络中审视。

**预训练基模型。** 方法构建于 **Wan**（Team Wan et al., arXiv 2025）这一预训练文生视频扩散模型之上。Wan 提供了基础的流匹配生成能力，但未经偏好对齐时，其生成视频在运动真实性和时序一致性上存在明显不足。DynamicsBoost 冻结 Wan 的骨干网络，仅优化 LoRA 适配器和帧级任务提示嵌入，在保持基模型泛化能力的同时实现高效的偏好注入。

**DPO 系列基线。** 论文直接对比了三类 DPO 变体：
- **Flow-DPO**（Liu et al., arXiv 2025）：将扩散 DPO 迁移至流匹配范式，在速度空间计算偏好损失，数学上与扩散 DPO 在整流流参数化下等价。但其偏好对依赖外部标注，且在整个视频上累积损失。
- **Flow-StructuralDPO**（Wu et al., arXiv 2025）：在 Flow-DPO 基础上引入结构化约束，试图提升时序一致性，但仍受限于人工标注偏好对的获取成本与质量。
- **Flow-DenseDPO**（Wu et al., arXiv 2025）：对视频所有帧进行稠密时序 DPO 训练，偏好信号覆盖更全面，但同样依赖外部偏好标注。

DynamicsBoost 与上述方法的根本差异在于**偏好对构造方式**：前者的偏好对来自视频延续过程中不同参考帧数量自然诱导的质量差异，完全无需人工或 VLM 标注。这一设计直接回应了偏好对齐规模化中的核心瓶颈——高质量偏好标注的获取成本高且存在模糊性。

**SFT 基线。** 论文还对比了监督微调基线，即仅使用延续训练损失优化模型，不引入偏好对齐。该基线的存在验证了单纯增加延续能力不足以显著提升运动真实性和语义一致性，偏好优化在其中起到关键作用。

### 知识库定位与适用边界

**方法归属。** DynamicsBoost 属于**无监督偏好对齐 + 视频延续生成**的交叉地带。其偏好信号来源于任务内在结构，而非外部奖励模型或人类反馈，这与 RLHF/DPO 主流范式形成互补而非替代关系。具体而言，该方法可被定位为：

1. **偏好数据构造层**：利用视频延续的单调质量特性，自动生成结构匹配、长度有序的偏好对。这一思路可推广至其他具有“部分优于整体”特性的生成任务。
2. **损失设计层**：非对称 DPO 损失仅对非共享延续区域计算偏好信号并按长度归一化，解决了标准 DPO 将条件帧区域纳入损失计算导致的信号稀释问题。
3. **模型扩展层**：通过掩码时间步和帧级任务提示，将 T2V 模型扩展为支持任意帧条件生成的延续模型，该扩展方式轻量且可迁移。

**适用边界。** 方法的核心假设是“生成片段始终劣于真实参考帧”，这一假设在以下场景中可能不成立：
- 静态或极低运动场景：生成内容与真实参考帧的差异极小，偏好信号微弱，可能导致 DPO 训练不稳定。
- 基模型已有强时序生成能力：若基模型本身能生成高质量长视频，延续长度差异带来的质量梯度可能不显著，偏好对的区分度下降。
- 非固定长度/分辨率场景：当前实验仅在 49 帧、288×512 分辨率下验证，对不同帧数和分辨率的泛化能力待验证。

此外，方法仅基于单一基模型（Wan）测试，在其他主流 T2V 架构（如 CogVideoX、HunyuanVideo）上的有效性尚未验证，这限制了其作为通用偏好对齐方案的结论强度。

### 局限与开放问题

**已知局限。**
1. **假设敏感性**：偏好对质量依赖于“生成片段劣于真实帧”的单调假设，对于静态或简单运动场景可能不成立。
2. **长度与分辨率限制**：延续训练和偏好对齐仅在固定视频长度（49 帧）和固定分辨率（288×512）条件下测试，泛化能力待验证。
3. **基模型依赖**：实验仅基于 Wan 模型，缺少跨架构验证，方法的通用性尚不明确。
4. **启发式采样**：非对称 DPO 的延续长度范围依赖启发式选择，不同场景可能需要调整，缺乏自适应机制。
5. **公平性未评估**：训练数据来源于 OpenVid-1M 子集，可能存在内容与风格偏差，对特定人群、动作或场景的生成质量可能不均衡，但论文未进行专门的公平性分析。

**开放问题。**
1. **长视频扩展**：如何将该无标注偏好对齐方法扩展到更长视频（如几分钟）的生成与偏好优化？长视频场景下延续长度与质量的关系是否仍保持单调？
2. **基模型鲁棒性**：延续偏好对的质量是否依赖于基模型已有的时序生成能力？在较弱基模型上，单调偏好假设是否仍成立？
3. **与在线强化学习结合**：非对称 DPO 能否与在线强化学习方法（如 GRPO）结合，实现更高效的偏好探索和策略迭代？
4. **奖励模型监督**：连续偏好信号是否能作为多模态奖励模型的有效监督来源，提升奖励模型的泛化能力？
5. **下游任务迁移**：该方法在真实视频编辑、视频预测等下游任务中的实用价值如何？是否需要额外的任务特定微调策略？



## 原文 PDF

![[paperPDFs/CVPR_2026/DynamicsBoost_Dynamic_Plausible_Video_Generation_via_Annotation_Free_Continuation_Preference_Optimization.pdf]]

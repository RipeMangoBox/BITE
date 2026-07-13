---
title: "Temporal Concept Dynamics in Diffusion Models via Prompt-Conditioned Interventions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Temporal_Concept_Dynamics_in_Diffusion_Models_via_Prompt_Conditioned_Interventions.pdf
project_link: https://adagorgun.github.io/PCI-Project/
code_link: null
openreview_forum_id: ABjaSsrYPD
aliases:
- PCIP
- TCDDMPCI
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "提示切换的介入时间步 t_s，即在轨迹中提前或推迟引入目标概念，从而控制概念插入成功率。"
primary_logic: "概念插入成功概率随去噪时间变化呈非递减规律，全局场景因素（时间、天气、季节、颜色）锁定最早且最急剧，人类属性（年龄、性别）居中，配件细节锁定较晚；修正流模型比扩散模型更早锁定概念，但扩散模型保留更长的可编辑窗口；概念与语境的分布一致性决定插入时序，分布外组合更早锁定；基于 CIS 的 [τ_50, τ_70] 窗口编辑能平衡语义插入与内容保留，优于现有方法。"
claims:
- "PCI 是一种无需训练和模型无关的框架，通过在不同时间步切换提示来测量 Concept Insertion Success (CIS)。"
- "所有子类别和模型上 C(τ) 经验上非递减，全局因素（风格、时间、天气等）的 τ_q 大（插入早）且 W 窗口窄（过渡急剧），人类属性居中，配件细节最晚。"
- "修正流模型（SD 3.5、FLUX.1-dev）比扩散模型更早且更急剧地锁定概念，SD 2.1 保留更长的后期灵活性。"
- "分布外（OOD）概念-语境对比分布内（in-distribution）更早锁定，插入窗口更窄、更脆。"
---

# Temporal Concept Dynamics in Diffusion Models via Prompt-Conditioned Interventions

> [!tip] 核心洞察
> 概念插入成功概率随去噪时间变化呈非递减规律，全局场景因素（时间、天气、季节、颜色）锁定最早且最急剧，人类属性（年龄、性别）居中，配件细节锁定较晚；修正流模型比扩散模型更早锁定概念，但扩散模型保留更长的可编辑窗口；概念与语境的分布一致性决定插入时序，分布外组合更早锁定；基于 CIS 的 [τ_50, τ_70] 窗口编辑能平衡语义插入与内容保留，优于现有方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过提示条件干预研究扩散模型中概念的时间动态 |
| 英文题名 | Temporal Concept Dynamics in Diffusion Models via Prompt-Conditioned Interventions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ABjaSsrYPD) · [Project](https://adagorgun.github.io/PCI-Project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Prompt-Conditioned Intervention (PCI) |
| Dataset | Custom editing dataset (88 concept pairs × 20 seeds = 1760 edits) |

> [!tip] 效果简介
> - Custom editing dataset (88 concept pairs × 20 seeds = 1760 edits) 上，CLIP_img (content preservation) 为 PCI-τ50: 0.8885，对比 NTI+P2P: 0.8666，变化 +0.0219。
> - Custom editing dataset (88 concept pairs × 20 seeds = 1760 edits) 上，CLIP_txt (semantic alignment) 为 PCI-τ50: 0.2236，对比 NTI+P2P: 0.2215，变化 +0.0021。
> - Custom editing dataset (88 concept pairs × 20 seeds = 1760 edits) 上，CLIP_dir (directional consistency) 为 PCI-τ50: 0.1387，对比 NTI+P2P: 0.0979，变化 +0.0408。

## 概要

扩散模型在文本到图像生成中表现出色，但现有研究多从静态视角评估最终生成结果，鲜有系统揭示**去噪轨迹中概念何时形成、何时锁定并不可再干预的时间动态**。这一盲区导致文本驱动的图像编辑方法缺乏对“何时介入最优”的理论指导，往往依赖人工经验选择时间步。

针对上述瓶颈，本文提出 **Prompt-Conditioned Intervention (PCI)**——一种无需训练、模型无关的分析框架。其核心机制是在扩散去噪过程中的任意时间步 $t_s$ 将条件提示从基础提示 $P_b$ 切换为包含目标概念的概念提示 $P_c$，并通过大型视觉语言模型（LVLM）以视觉问答（VQA）形式判断目标概念是否成功出现在最终图像中。在多个随机种子和上下文提示上聚合后，得到**概念插入成功率（Concept Insertion Success, CIS）** 沿去噪时间的变化曲线，从而量化概念的可插入性与锁定时机。

PCI 揭示的核心发现是：**概念插入成功概率随去噪时间呈非递减规律**，但不同概念类别和模型架构的锁定时序差异显著。全局场景因素（时间、天气、季节、颜色、风格）锁定最早且过渡最急剧；人类属性（年龄、性别）居中；配件细节锁定最晚，保留最长的可编辑窗口。修正流模型（SD 3.5、FLUX.1-dev）比传统扩散模型更早且更急剧地锁定概念，但扩散模型（如 SD 2.1）反而保留了更长的后期灵活性。此外，概念与语境的分布一致性深刻影响插入时序——分布外（OOD）组合比分布内组合更早锁定，插入窗口更窄、更脆。

基于上述洞察，PCI 将 CIS 曲线转化为编辑指导：在 CIS 达到 50% 至 70% 的区间 $[\tau_{50}, \tau_{70}]$ 进行提示切换，能实现语义插入与内容保留的最佳平衡。在包含 88 个概念对的自定义编辑数据集上，PCI-$\tau_{50}$ 在 CLIP_img（内容保留）、CLIP_txt（语义对齐）和 CLIP_dir（方向一致性）三项指标上均优于 **NTI+P2P**（Mokady et al., 2023）和 **Stable Flow**（Avrahami et al., CVPR 2025），验证了 CIS 引导编辑的有效性。

PCI 的计算开销较高（需在所有推理步上插断），且不存在适用于所有概念的单一最优 CIS 值；推荐 $[0.5, 0.7]$ 作为普适编辑窗口，但特定概念仍可能需微调。如何降低 CIS 曲线计算成本、自动确定概念级编辑截止点，以及从单概念 CIS 预测多概念联合插入行为，是尚待解决的开放问题。

扩散模型已成为文本到图像生成的核心范式，但我们对模型内部的概念形成过程仍知之甚少：一个语义概念究竟是在去噪轨迹的哪个时间点从噪声中“结晶”出来的？一旦形成，它又在何时变得不可再被外部干预所改变？这些问题不仅关乎我们对生成模型机理的基本理解，更直接影响文本驱动图像编辑等下游应用的可控性与可靠性。

现有研究多从静态视角评估扩散模型的生成结果。无论是通过 CLIPScore、LPIPS 等感知指标衡量编辑后的图像质量，还是利用注意力图修改扩散轨迹的方法（如 **NTI+P2P**，Mokady et al., 2023；**Stable Flow**，Avrahami et al., CVPR 2025），它们都关注“编辑后图像是否包含目标概念”这一最终状态，却忽略了去噪过程中概念的时间动态——概念是何时被模型锁定的？不同概念类别的锁定时序是否存在系统性差异？这些问题在现有文献中缺乏系统性的实证研究。

这种静态视角造成了两个关键缺口。其一，编辑方法中提示修改的时间步选择缺乏理论指导。现有方法通常依赖手动调参或启发式规则来决定在去噪的哪个阶段介入，这导致编辑效果在不同概念、不同上下文之间高度不稳定。其二，我们缺乏对概念可编辑窗口的定量理解。直觉上，扩散模型的去噪过程从粗到细逐步构建图像内容，但哪些概念在早期就被锁定（一旦形成便难以修改）、哪些概念在后期仍保持灵活性，这一问题的答案对设计更高效的编辑策略至关重要。

本文的核心动机正是填补这一空白。我们提出一个根本性问题：**能否通过系统性地干预去噪轨迹，来测量概念在扩散时间中的形成与锁定动态？** 为此，我们设计了一个轻量、无需训练、模型无关的分析框架——**Prompt-Conditioned Intervention (PCI)**。其核心思想是在去噪过程的不同时间步切换文本提示条件，观察目标概念是否能被成功插入最终图像，从而绘制出概念插入成功率（Concept Insertion Success, CIS）沿时间的变化曲线。这条曲线天然地揭示了一个概念从“可自由插入”到“已被锁定不可再干预”的转变过程，为理解扩散模型中的概念时间动态提供了可量化的分析工具。

通过这一框架，我们能够在多个主流扩散模型（SD 2.1、SDXL、SD 3.5、FLUX.1-dev）上，对涵盖全局场景因素（时间、天气、季节、风格、颜色）、人类属性（年龄、性别）和配件细节等数十个细粒度概念类别进行大规模分析，从而揭示概念锁定的普遍规律及其对编辑实践的指导意义。

## 核心方法与创新机理

本文的核心创新并非提出一种新的扩散模型架构或训练范式，而是**将扩散模型的去噪时间轴重新定义为概念形成与锁定的可解释维度**，并据此构建了一套从测量到应用的完整方法体系。相较于现有工作，PCI 框架在两个关键环节上实现了根本性转变。

### 从手动试探到 CIS 曲线引导的编辑触发

现有文本驱动图像编辑方法——如 **NTI+P2P**（Mokady et al., 2023）和 **Stable Flow**（Avrahami et al., CVPR 2025）——依赖手动选择干预时间步、注意力图分析或分割模块来确定何时修改文本条件。这些策略缺乏对“概念何时可被可靠插入”的量化认知，编辑效果高度依赖经验调参。

PCI 将编辑触发机制建立在对模型行为的系统性测量之上。通过在所有去噪时间步执行提示切换并聚合多种子、多上下文的结果，PCI 绘制出**概念插入成功率（CIS）曲线** $C(\tau)$——一条描述概念在轨迹上从“不可插入”到“稳定锁定”的非递减函数。编辑时，用户只需将期望的插入概率映射到 CIS 曲线上最近的时间步 $t_s$，即可自动获得语义插入与内容保留之间的最优平衡点。具体而言，研究发现 **$[\tau_{50}, \tau_{70}]$ 区间（即 CIS 概率 50%–70% 对应的时间窗）** 是实现最佳编辑效果的普适窗口：在此窗口内触发提示切换，语义对齐（CLIP_txt）和方向一致性（CLIP_dir）显著优于基线，同时内容保留（CLIP_img）维持在较高水平（Table 1）。

这一转变的本质在于：**PCI 将编辑时间步的选择从启发式规则升级为基于模型内禀概念动力学的数据驱动决策**，使编辑行为从“盲调”变为“可测量、可预测”。

### 从感知相似度到 VQA 的概念存在判定

概念插入是否成功的判定是 CIS 测量的基础。基线方法通常依赖 CLIPScore 或 LPIPS 等感知相似度指标来评估编辑质量，但这些指标在回答“目标概念是否真正出现在图像中”这一二值问题时，表现出**语义特异性不足**的弱点——高相似度可能源于背景保留而非概念插入，低相似度也可能因编辑引入了无关变化。

PCI 将概念存在判定重构为**大型视觉语言模型（LVLM）的视觉问答（VQA）任务**。具体而言，系统向 LVLM（默认使用 Qwen-VL-3B）提出针对目标概念的二值问题（如“Is there an old person in the image?”），根据回答判定概念是否成功插入。这一设计带来了三重优势：

1. **语义精确性**：VQA 直接针对概念语义进行判别，而非依赖嵌入空间的间接相似度；
2. **模型鲁棒性**：消融实验表明，CIS 轨迹在 Qwen-3B、Qwen-7B、LLaVA-OneVision-7B、SmolVLM-2B 四种不同 LVLM 上高度一致（Figure C1），测量结果对 VQA 模型选择不敏感；
3. **可扩展性**：VQA 问题模板可随概念类别灵活定制（Table A1），覆盖从具体物体到抽象属性的广泛概念空间。

这两个 changed slots 共同构成了 PCI 的方法论核心：**CIS 曲线提供了概念时间动态的量化表征，而 VQA 判定机制确保了该表征的语义可靠性与测量鲁棒性**。二者结合，使得扩散模型去噪轨迹中“概念何时形成、何时锁定”这一原本隐式的过程，首次获得了可测量、可比较、可操作的实证基础。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_ABjaSsrYPD/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the PCI framework. A base prompt P _ { b } is used as conditioning for generation, altered to the concept prompt P _ { c } at time t _ { s } . The generated images are evaluated through VQA to determine concept presence and aggregated across seeds to obtain CIS across the diffusion trajectory*

### 核心问题与设计动机

扩散模型生成图像时，概念并非在最终一步形成，而是在去噪轨迹中逐步涌现并最终“锁定”。现有方法多从静态视角评估生成结果，缺乏对**概念何时形成、何时锁定、何时不可再干预**的时间动态理解。PCI（Prompt-Conditioned Intervention）正是针对这一瓶颈提出的分析框架：它通过在去噪轨迹的不同时间步切换文本提示，系统性地探测概念的可插入性随时间的变化规律。

### PCI 框架总览

PCI 是一个**无需训练、模型无关**的分析框架，其核心思想是将扩散去噪过程转化为一个可干预的时间轴，通过测量**概念插入成功率**（Concept Insertion Success, CIS）来量化概念的时间动态。框架的完整流水线如 Figure 2 所示，包含以下顺序模块：

1. **种子重采样与过滤（Seed Resampling / Filtering）**  
   为确保初始噪声潜变量 $x_T$ 不包含目标概念的先验痕迹，框架对随机种子进行过滤，并结合负向引导（negative guidance）生成中性基线。这一步骤消除了“概念本已存在”的混淆因素，使后续插入测量的归因更干净。

2. **基提示去噪（Base-Prompt Denoising）**  
   使用不含目标概念的基础提示 $P_b$ 作为条件，将纯噪声 $x_T$ 去噪到中间时间步 $t_s$：
   $$\mathbf{x}_{t_s} = \operatorname{Denoise}(\mathbf{x}_T, P_b)$$
   此阶段生成的是与目标概念无关的中性中间表示。

3. **提示切换（Prompt Switching）**  
   在选定时间步 $t_s$，将条件从基础提示 $P_b$ 替换为包含目标概念的提示 $P_c$（通常为 $P_b$ 与概念词的组合）。这一“干预”操作是 PCI 的核心机制——**提示切换的介入时间步 $t_s$ 就是控制概念插入成功率的因果旋钮**。

4. **概念提示去噪（Concept-Prompt Denoising）**  
   以新的条件 $P_c$ 从中间状态 $x_{t_s}$ 继续去噪至干净潜变量：
   $$\mathbf{x}_0\big(P_b \xrightarrow{t_s} P_c\big) = \operatorname{Denoise}(\mathbf{x}_{t_s}, P_c)$$

5. **图像解码（Image Decoding）**  
   通过 VAE 解码器将干净潜变量还原为最终图像。

6. **VQA 评估（VQA Evaluation）**  
   利用大型视觉语言模型（LVLM），以视觉问答形式判断目标概念是否出现在生成图像中。论文采用 Qwen-VL-3B 作为默认评估器，通过二值判断（是/否）给出概念存在性标签。

7. **CIS 聚合（CIS Aggregation）**  
   在多个随机种子（默认 $k=100$）和不同上下文提示上，对每个时间步重复上述流程，统计概念插入成功的频率，绘制 CIS 曲线 $C(\tau)$，其中 $\tau$ 为归一化时间步。

### 关键指标定义

CIS 曲线的分析依赖两个核心统计量：

- **穿越时间 $\tau_q$**：CIS 概率首次达到阈值 $q$ 的最小归一化时间步，定义为 $\tau_q = \min\{\tau \in [0,1] : C(\tau) \geq q\}$。$\tau_q$ 越大，表示概念越早可被成功插入，即概念锁定越早。
- **带宽-陡度 $W_{70,50}$**：$W_{70,50} = \tau_{70} - \tau_{50}$，衡量 CIS 从 50% 升至 70% 所需的时间跨度。该值越小，概念锁定过程越急剧，对干预时间的选择越敏感。

### 方法定位与基线差异

PCI 与现有文本驱动图像编辑方法的关键差异体现在两个维度：

| 维度 | 基线方法 | PCI 方法 |
|------|----------|----------|
| **编辑触发机制** | NTI+P2P（Mokady et al., 2023）手动选择时间步或依赖注意力图/分割模块；Stable Flow（Avrahami et al., CVPR 2025）依赖固定流程 | 在 CIS 曲线指导下的最优 $\tau$ 窗口（$[\tau_{50}, \tau_{70}]$）进行提示切换，自动获得编辑成功与内容保留的最佳平衡 |
| **概念存在判定** | CLIPScore 或 LPIPS 等感知相似度指标 | LVLM 的 VQA 二值判断，对概念存在的判定更精确、更具语义针对性 |

### 数据集与评估设置

实验构建了包含 **88 个概念对** 的编辑数据集，覆盖人口统计、物体、人类属性、动作、环境、风格等 7 大类、多个子类别（详见 Table A1）。每个概念对使用 20 个随机种子，总计 1760 次编辑。CIS 曲线在 SD 2.1、SDXL、SD 3.5、PixArt-alpha XL 和 FLUX.1-dev 五个生成模型上进行跨架构分析。编辑性能通过三项 CLIP 指标量化：CLIP_img（内容保留）、CLIP_txt（语义对齐）、CLIP_dir（方向一致性）。

### 消融验证

框架的可靠性通过多项消融实验确认：
- **VQA 模型鲁棒性**：Qwen-3B、Qwen-7B、LLaVA-OneVision-7B、SmolVLM-2B 四种 LVLM 的 CIS 轨迹高度一致。
- **种子预算充分性**：$k=100$ 个种子足以生成稳定的 CIS 轨迹，增加种子不会明显提高覆盖度。
- **提示鲁棒性**：在动物、手工制品、常见动作三个子类别上，五种语义等价的提示改写下，CIS 时序模式与锁定行为保持一致（Table C1）。

### 整体框架

PCI（Prompt-Conditioned Intervention）是一个无需训练、模型无关的框架，其核心思想是在扩散模型去噪轨迹的中间时间步切换文本提示条件，通过观察概念插入的成功概率来揭示概念在时间维度上的动态形成过程。框架包含以下关键模块：

**1. 种子重采样与过滤**

为确保初始噪声潜变量不包含目标概念，通过种子过滤和负向引导使基提示生成的中性基线图像中目标概念出现概率接近零。该模块消除了先验概念存在偏差，保证 CIS 测量的因果性。

**2. 基提示去噪**

在基提示 $P_b$ 条件下，从纯噪声 $\mathbf{x}_T$ 去噪至中间时间步 $t_s$ 的状态：

$$\mathbf{x}_{t_s} = \operatorname{Denoise}(\mathbf{x}_T, P_b)$$

其中 $\operatorname{Denoise}$ 表示扩散模型从时间步 $T$ 到 $t_s$ 的迭代去噪过程，$P_b$ 为不含目标概念的基础文本提示。

**3. 提示切换**

在时间步 $t_s$ 将条件从基提示 $P_b$ 替换为包含目标概念的概念提示 $P_c$，并继续去噪生成最终图像：

$$\mathbf{x}_0(P_b \xrightarrow{t_s} P_c) = \operatorname{Denoise}(\mathbf{x}_{t_s}, P_c)$$

这是 PCI 的核心操作——通过改变去噪轨迹的中间条件来干预概念形成过程。$t_s$ 的选择决定了概念在生成过程中被引入的早晚，是控制概念插入成功率的因果旋钮。

**4. 图像解码**

通过 VAE 解码器将干净潜变量 $\mathbf{x}_0$ 还原为像素空间的生成图像。

**5. VQA 评估**

利用大型视觉语言模型（LVLM），以视觉问答形式判断目标概念是否出现在生成图像中。论文默认使用 Qwen-VL-3B 作为评估器，通过设计概念特定的二值问题（如“图中是否有人戴眼镜？”）获得概念存在与否的判断。相比于 CLIPScore 或 LPIPS 等感知相似度指标，VQA 方法对具体概念的存在判断更为精确和特异。

**6. CIS 聚合**

在多个随机种子和不同基提示下，对每个时间步的概念插入成功概率取平均，绘制 CIS 曲线：

$$C(\tau) = \mathbb{E}_{\text{seeds, prompts}}[\mathbb{1}(\text{concept present} \mid \text{intervention at } \tau)]$$

其中 $\tau = t_s / T$ 为归一化时间步。

### 关键派生指标

从 CIS 曲线派生出两个核心分析指标：

**CIS 穿越时间** $\tau_q$：CIS 概率首次达到阈值 $q$ 的最小归一化时间步，衡量概念可插入的时间早晚：

$$\tau_q = \min\{\tau \in [0,1] : C(\tau) \geq q\}$$

$\tau_q$ 越大，表示概念越早锁定、越早可插入。

**带宽-陡峭度** $W_{70,50}$：CIS 从 50% 升至 70% 所需的时间跨度，反映概念锁定过程的尖锐程度：

$$W_{70,50} = \tau_{70} - \tau_{50}$$

$W$ 越小，表示概念锁定的过渡越急剧，对干预时间点的敏感度越高。

### 分类器无关引导

扩散模型推理时使用的分类器无关引导公式为：

$$\hat{\boldsymbol{\epsilon}}_\theta = (1+\omega)\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t, \mathbf{c}) - \omega\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t, \varnothing)$$

其中 $\omega$ 为引导尺度，$\mathbf{c}$ 为文本条件嵌入，$\varnothing$ 为空文本条件。该公式通过将无条件预测与条件预测外推来增强条件一致性，是 PCI 框架中控制生成质量的基础机制。

### CIS 引导的编辑触发

在文本驱动图像编辑任务中，编辑触发机制为：将用户指定的 CIS 概率映射到 CIS 曲线上最接近的对应时间步 $t_s$，然后执行 PCI。论文发现 $[\tau_{50}, \tau_{70}]$ 区间（即 CIS 概率 0.5–0.7 对应的时间窗口）是实现语义插入与内容保留最佳平衡的编辑窗口。

## 实验与关键发现

### 核心发现：概念锁定时序的非递减规律

PCI 框架在五个生成模型（SD 2.1、SDXL、SD 3.5、PixArt-alpha XL、FLUX.1-dev）上揭示了概念插入成功概率 C(τ) 随去噪时间呈经验性非递减规律——概念一旦在某个时间步变得可插入，该能力不会在更晚的时间步丧失。这一单调性构成了所有后续分析的基础。

概念类别之间呈现出清晰的时序分层（图 3、图 D1）：

- **全局场景因素锁定最早且过渡最急剧**：时间（time of day）、天气（weather）、季节（season）、风格（style）、颜色（color）等概念在去噪早期即锁定，其 τ₅₀ 和 τ₇₀ 值显著高于其他类别，且带宽 W₇₀₅₀ = τ₇₀ − τ₅₀ 极窄，表明这些概念的决定窗口短而脆——一旦错过极窄的时间窗口，插入成功率急剧下降。

- **人类属性居中**：年龄组（age group）和性别（gender）的锁定时间晚于全局因素，但早于配件细节，过渡斜率也相对平缓，提供了更宽的可编辑窗口。

- **配件细节锁定最晚**：配件（accessories）在所有概念类别中表现出最大的后期灵活性，其 τ₅₀ 和 τ₇₀ 值最低。以 SD 3.5 为例，配件的 τ₅₀ = 0.53 ± 0.05，τ₇₀ = 0.62 ± 0.03，意味着直到去噪进程过半，配件概念仍可被可靠插入。

### 跨架构差异：修正流模型更早锁定

不同生成模型的概念锁定行为存在系统性差异。修正流模型（rectified flow models）——SD 3.5 和 FLUX.1-dev——比传统扩散模型（SD 2.1、SDXL）更早且更急剧地锁定概念。具体表现为：修正流模型的 τ₅₀ 和 τ₇₀ 更大（插入更早），带宽 W₇₀₅₀ 更窄（过渡更陡峭）。这意味着修正流模型在去噪早期就快速固化概念结构，减少了后期干预的灵活性。相比之下，SD 2.1 保留了最长的后期可编辑窗口，为需要精细控制编辑时机的应用场景提供了更大容错空间。

### 分布一致性决定插入时序

同一概念在不同上下文中的 CIS 曲线存在显著差异（图 4）。当目标概念与基础提示所描述的语境分布一致（in-distribution）时，插入窗口更宽、锁定时间更晚；反之，分布外（out-of-distribution）的概念-语境组合会更早锁定，插入窗口更窄且对干预时间步更敏感。这一发现表明，扩散模型在去噪早期就依据提示语境建立了强先验，与该先验不一致的概念必须更早介入才能成功插入，否则将被语境先验所覆盖。

### CIS 引导的编辑窗口：τ₅₀ 到 τ₇₀ 的最优平衡

将 CIS 分析应用于文本驱动图像编辑，实验表明 [τ₅₀, τ₇₀] 区间是实现语义插入与内容保留最佳平衡的编辑窗口（图 5）。定量比较（表 1）证实了这一结论：

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_ABjaSsrYPD/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of editing methods. We report $\mathrm { C L I P } _ { i m g }$ (content preservation), $\mathrm { C L I P } _ { t x t }$ (semantic alignment), and ${ \mathrm { C L I P } } _ { d i r }$ (directional consistency). Higher $\mathrm { C L I P } _ { i m g } ^ { - }$ indicates better preservation, while higher $\mathrm { C L I P } _ { t x t }$ and $\mathrm { C L I P } _ { d i r }$ indicate stronger concept insertion

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_ABjaSsrYPD/figures/008_Figure_5.jpg]]
*Figure 5: Examples of text-driven image editing on SDXL. The edited images are shown at four different points with their respective CIS probabilities: τ30, τ50, τ70, and τ90. High probabilities until a certain point ensure the intended modification but reduce preservation of the original image. We observe that CIS probabilities above 0.7 start to noticeably compromise the original content, and probabilities between 0.5 to 0.7 as suggested by our analysis (red rectangle) are best for editing while preserving the original image*

| 方法 | CLIP_img（内容保留）↑ | CLIP_txt（语义对齐）↑ | CLIP_dir（方向一致性）↑ |
|------|----------------------|----------------------|------------------------|
| NTI+P2P | 0.8666 | 0.2215 | 0.0979 |
| Stable Flow | 0.8774 | 0.2159 | 0.1192 |
| PCI-τ₅₀ | **0.8885** | **0.2236** | **0.1387** |

PCI-τ₅₀ 在所有三项 CLIP 指标上均优于 NTI+P2P（Mokady et al., 2023）和 Stable Flow（Avrahami et al., CVPR 2025）。CLIP_dir 的提升尤为显著（+0.0408 对比 NTI+P2P），表明 CIS 引导的编辑在保持语义变化方向与文本提示一致方面具有明显优势。定性对比（图 D7）进一步显示，PCI-τ₆₀ 产生的编辑在语义强度、空间定位精度和未编辑区域保留方面均优于基线方法。

### 消融实验：CIS 测量的鲁棒性

**VQA 模型选择鲁棒性**：使用四种不同 LVLM 模型（Qwen-3B、Qwen-7B、LLaVA-OneVision-7B、SmolVLM-2B）评估 CIS，所有模型的 CIS 轨迹高度一致（图 C1），确认 CIS 测量对 VQA 模型选择具有鲁棒性。对于抽象概念（art、creative、elegant），较大模型（Qwen-7B、LLaVA-OneVision-7B）产生的 CIS 曲线平滑且单调，小型模型（SmolVLM-2B）的绝对值偏低但趋势一致（图 D5）。

**种子预算充分性**：种子预算分析表明 k=100 个种子足以生成稳定的 CIS 轨迹，增加种子不会明显提高曲线覆盖度（图 C2）。

**提示鲁棒性**：在动物、手工制品、常见动作三个子类别上，使用五种语义等价的提示改写版本计算 CIS，整体时序模式和锁定行为保持一致（图 C3、表 C1），验证了 CIS 分析对提示措辞变化具有鲁棒性。

**交叉注意力可视化**：定性交叉注意力图（图 D3）显示，在高 CIS 区间插入时目标概念的注意力更强且空间更聚焦，在低 CIS 区间注意力弱或弥散，为二值 CIS 指标提供了视觉补充。

**多概念交互**：多概念联合插入实验（图 D4）表明，大多数概念对表现近乎组合式——联合插入时各概念的 CIS 曲线与单独插入时接近。但少数组合（如 female + sketch）会显著将插入窗口后移，体现出概念间的交互效应。这一现象提示多概念编辑不能简单假设独立性，需进一步研究交互机制。

### 局限与注意事项

1. **计算开销**：单种子 CIS 曲线需在所有原始推理步上插断，计算成本较高。论文通过稀疏采样和多种子平均缓解，但仍需较高计算资源。
2. **编辑敏感度**：不存在适用于所有类别的单一最优 CIS 值；推荐的 [0.5, 0.7] 区间作为普适编辑窗口，针对特定概念可能仍有偏差。
3. **CDS 指标受限**：概念删除成功率（Concept Deletion Success, CDS）因回推效应等不稳定因素，未作为主要分析指标，其解释能力受限（图 A2、A3）。
4. **LVLM 评估偏见**：VQA 评估可能继承训练数据中的偏见，对抽象或主观概念可能产生跨文化差异，需在应用中注意。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_ABjaSsrYPD/figures/054_Figure_51.jpg]]
*Figure 51: Figure D7: Comparison of editing performance across NTI-P2P, Stable-Flow, and our PCI method at τ60. PCI produces edits that are semantically stronger, more spatially localized, and better aligned with the target concept while preserving non-edited regions*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_ABjaSsrYPD/figures/010_Table_2.jpg]]
*Table 2: Table A1: Overview of dataset categories, subcategories, and associated questions*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_ABjaSsrYPD/figures/030_Table_3.jpg]]
*Table 3: Table C1: Overview of the prompt variations. For the selected subcategories, we construct a total of five prompts: the original base prompt (shown in bold) and four semantically consistent paraphrased variants used to assess prompt robustness*

## 定位与知识库关联

### 与现有编辑方法的关系

PCI 与当前主流的文本驱动图像编辑方法处于不同层次：PCI 本身是一个**分析框架**，而非直接竞争的编辑算法。它通过提示切换干预测量概念的时间动态，进而为编辑提供时序决策依据。与之对比的两类基线方法如下：

- **NTI+P2P**（Mokady et al., 2023）：基于注意力图修改扩散轨迹的文本驱动编辑方法，依赖手工选择时间步或注意力/分割模块来确定编辑时机。PCI 的核心差异在于用 CIS 曲线自动确定最优干预窗口，而非依赖启发式或手动调参。
- **Stable Flow**（Avrahami et al., CVPR 2025）：最新的文本驱动图像编辑方法。PCI 在 CLIP_img、CLIP_txt、CLIP_dir 三项指标上均优于该方法（Table 1），且编辑窗口 [τ_50, τ_70] 具有可解释的理论基础，而非经验性选择。

在方法论层面，PCI 与上述编辑方法的关键差异体现在两个“槽位”变化上：

| 槽位 | 基线做法 | PCI 做法 | 证据 |
|------|----------|----------|------|
| **编辑触发机制** | 手动选择时间步，或依赖注意力图/分割模块 | 在 CIS 曲线引导下选择 [τ_50, τ_70] 窗口进行提示切换，自动平衡语义插入与内容保留 | Sec. 5 |
| **概念存在判定** | CLIPScore 或 LPIPS 等感知相似度指标 | 大型视觉语言模型（LVLM）的视觉问答（VQA）进行二值概念存在判断 | Sec. 3.2 |

PCI 的 VQA 判定机制在方法论上更精确：CLIPScore 和 LPIPS 被证明“less powerful and unspecific”（Sec. 3.2），而 VQA 直接回答“目标概念是否出现在图像中”这一二元问题，与 CIS 的定义语义一致。

### 适用边界

PCI 的适用边界由以下几个维度界定：

1. **模型兼容性**：PCI 是 training-free 和 model-agnostic 的框架，已在 SD 2.1、SDXL、SD 3.5、PixArt-alpha XL、FLUX.1-dev 五个生成模型上验证。但不同模型架构的概念锁定行为差异显著——修正流模型（SD 3.5、FLUX.1-dev）比扩散模型更早且更急剧地锁定概念（Sec. 4.2），这意味着同一 CIS 窗口在不同模型上的编辑效果不可直接迁移。

2. **概念类型依赖**：CIS 曲线揭示的概念锁定时序呈现清晰的层级结构——全局场景因素（时间、天气、季节、颜色、风格）锁定最早且过渡最急剧，人类属性（年龄、性别）居中，配件细节锁定最晚。因此 [τ_50, τ_70] 窗口对不同概念类别的实际编辑效果存在固有差异，不存在单一最优 CIS 值适用于所有类别。

3. **分布一致性约束**：分布外（OOD）概念-语境组合比分布内组合更早锁定，插入窗口更窄、更脆（Sec. 4.2）。这意味着对非典型组合的编辑需要更精确的时间步控制，且可编辑窗口更受限。

4. **计算开销**：单种子 CIS 曲线需在所有原始推理步上进行插断和 VQA 评估，虽然可通过稀疏采样和多种子平均缓解，但仍需较高计算量。种子预算分析表明 k=100 个种子足以生成稳定的 CIS 轨迹（Fig. C2），这为实际应用提供了参考下限。

### 局限与开放问题

**已识别的局限**：

- **编辑敏感度**：不存在单个最优 CIS 值适用于所有类别；论文推荐 [0.5, 0.7] 区间作为普适编辑窗口，但针对特定概念仍可能偏离最优。
- **CDS 的混淆因素**：概念删除成功率（CDS）因回推效应等不稳定因素，未作为主要分析指标，其解释能力受限。
- **LVLM 评估偏见**：VQA 评估可能继承训练数据中的偏见，对抽象或主观概念（如 art、creative、elegant）可能产生跨文化差异。消融实验显示小型 LVLM 对抽象概念的 CIS 值偏低，但趋势一致（Fig. D5）。

**开放问题**：

1. 能否在保持分辨率的前提下大幅降低 CIS 曲线计算的时间成本，使其适用于实时编辑场景？
2. 如何自动为不同概念和上下文确定一个可靠的单值 CIS 编辑截止点，而无需用户手动调参？
3. 多概念交互中，哪些机制决定了联合插入窗口的延迟或提前？能否从单概念 CIS 预测多概念组合的插入时序？消融实验已发现少数组合（如 female + sketch）会显著将插入窗口后移，体现非组合式的交互效应（Fig. D4），但这一现象的规律尚未被系统建模。

## 原文 PDF

![[paperPDFs/ICLR_2026/Temporal_Concept_Dynamics_in_Diffusion_Models_via_Prompt_Conditioned_Interventions.pdf]]

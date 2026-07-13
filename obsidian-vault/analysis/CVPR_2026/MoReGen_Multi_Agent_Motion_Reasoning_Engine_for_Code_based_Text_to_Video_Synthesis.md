---
title: "MoReGen: Multi-Agent Motion-Reasoning Engine for Code-based Text-to-Video Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoReGen_Multi_Agent_Motion_Reasoning_Engine_for_Code_based_Text_to_Video_Synthesis.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Bai_MoReGen_Multi-Agent_Motion-Reasoning_Engine_for_Code-based_Text-to-Video_Synthesis_CVPR_2026_paper.html
project_link: null
code_link: https://github.com/ostadabbas/MoReGen-Multi-Agent-Motion-Reasoning-Engine
aliases:
- MoReGen
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion
core_operator: 通过引入多智能体协作架构，将自然语言描述显式解析为结构化物理规范，并转化为可执行的物理仿真代码，直接由物理引擎驱动视频生成，辅以基于轨迹、视觉和语义反馈的迭代修正闭环，从而扭转了从“数据外观拟合”到“物理机制模拟”的因果路径。
primary_logic: 将文本到视频生成重新定义为从自然语言到可执行物理仿真的翻译任务，利用大型语言模型的代码生成与推理能力结合物理确定性，不仅能产生严格符合牛顿力学的运动，而且首次提出了基于物体轨迹直接测量的评估指标（MoRe metrics），定量揭示了现有数据驱动评估方法的分布外失效问题，为物理一致的视频生成和评价建立了新范式。
claims:
- MoReGen 在 MoReSet 基准的 MoRe 指标（DTW、DTW-N、Procrustes）上均取得最佳性能，显著超越了包括 Sora2 和 Veo3 在内的所有现有文本到视频模型。
- 现有的数据驱动物理评估指标（如 Trajan 的 AJ 和 VideoPhy2 的 SA）在评估物理仿真生成的视频时表现出严重的分布外失效（分数异常低），而 MoRe metrics 能准确反映轨迹保真度和物理一致性。
- 消融实验证实，对文本解析器的监督微调（SFT）以及引入评估器反馈（Feedback）均能显著提升 MoReGen 的生成质量，证明架构中每一关键组件均不可或缺。
- MoReSet 上 DTW↓ = 8.93 ± 9.61
---

# MoReGen: Multi-Agent Motion-Reasoning Engine for Code-based Text-to-Video Synthesis

> [!tip] 核心洞察
> 将文本到视频生成重新定义为从自然语言到可执行物理仿真的翻译任务，利用大型语言模型的代码生成与推理能力结合物理确定性，不仅能产生严格符合牛顿力学的运动，而且首次提出了基于物体轨迹直接测量的评估指标（MoRe metrics），定量揭示了现有数据驱动评估方法的分布外失效问题，为物理一致的视频生成和评价建立了新范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoReGen：面向代码驱动文本到视频合成的多智能体运动推理引擎 |
| 英文题名 | MoReGen: Multi-Agent Motion-Reasoning Engine for Code-based Text-to-Video Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Bai_MoReGen_Multi-Agent_Motion-Reasoning_Engine_for_Code-based_Text-to-Video_Synthesis_CVPR_2026_paper.html) · [Code](https://github.com/ostadabbas/MoReGen-Multi-Agent-Motion-Reasoning-Engine) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion |
| Method | MoReGen |
| Dataset | MoReSet |

> [!tip] 效果简介
> - MoReSet 上，DTW↓ 8.93 ± 9.61 vs SOTA models (e.g., Sora2, Veo3) (Best (lowest))；DTW-N↓ 0.06 ± 0.07 vs SOTA models (e.g., Sora2, Veo3) (Best (lowest))；Procrustes↑ 0.48 ± 0.30 vs SOTA models (e.g., Sora2, Veo3) (Best (highest))。
> - MoReSet (VideoPhy2) 上，PC↑ 4.53 ± 0.69 vs SOTA models (e.g., Sora2, Veo3) (Best (highest))；SA↑ 2.73 ± 0.44 vs SOTA models (e.g., Sora2, Veo3) (Worst (lowest) - indicates OOD failure of data-driven metrics)。
> - MoReSet (Trajan) 上，AJ↑ 0.10 ± 0.03 vs SOTA models (e.g., Sora2, Veo3) (Worst (lowest) - confirms OOD failure)。

## 概要

当前主流的文本到视频（T2V）生成模型，包括 Sora2、Veo3 和 Grok Imagine 等商业系统，虽然在视觉真实感上取得了显著进展，但其底层本质是**外观驱动的统计模式记忆**。这类模型依赖从大规模视频数据中学习到的像素关联来合成运动，缺乏对牛顿力学基本规律（如动量守恒、力与加速度关系、碰撞传递）的因果理解。因此，在面对分布外（OOD）的物理提示时，它们会频繁出现物体计数错误、动量凭空产生或消失、力学关系推断失败等违反物理定律的生成结果（见 Figure 1）。这一瓶颈的根源在于：扩散模型所逼近的数据分布本身并不编码物理因果机制，仅凭扩大模型规模或数据量无法从根本上解决物理一致性问题。

MoReGen（CVPR 2026）针对上述瓶颈，提出了一种**范式级转变**：将文本到视频生成重新定义为从自然语言到可执行物理仿真的**翻译任务**。其核心因果调节变量在于，通过多智能体协作架构，将自由格式的文本描述显式解析为结构化的物理规范（包含物体属性、初始条件、力学参数等），再由代码编写智能体将其转化为调用物理引擎（Pymunk）的仿真代码，最终由物理引擎**确定性地**驱动运动生成。这一设计扭转了从“数据外观拟合”到“物理机制模拟”的因果路径，使生成的视频在物体运动轨迹层面严格遵循牛顿力学。

该工作的核心洞察在于：利用大语言模型（LLM）的代码生成与推理能力，结合物理引擎的确定性仿真，可以构建一个**可复现、物理精确**的视频生成框架。在此基础上，MoReGen 首次提出了基于物体轨迹直接测量的评估指标——MoRe metrics（包括 DTW、DTW-N、Procrustes），从轨迹对齐的角度量化物理保真度。实验结果表明，MoReGen 在 MoReSet 基准上显著超越了包括 Sora2、Veo3 在内的所有现有 T2V 模型，在 DTW、DTW-N、Procrustes 三项核心指标上均取得最优。更有趣的是，现有的数据驱动物理评估指标（如 Trajan 的 AJ、VideoPhy2 的 SA）在评估物理仿真生成的视频时出现严重的**分布外失效**（分数异常偏低），而 MoRe metrics 能准确反映轨迹保真度，定量揭示了现有评估方法的局限性。

在方法定位上，MoReGen 不属于扩散模型或其变体，而属于**代码驱动、物理引擎仿真的生成范式**。与之对比的基线方法覆盖了当前主流的扩散模型（Wan2.2-TI2V-5B、LTXV-2B-Distilled、CogVideoX-5B）、商业闭源系统（Veo3、Sora2、Grok Imagine），以及近期同样关注物理一致性的工作（Newton-Gen、WISA）。消融实验进一步证实，对文本解析器的监督微调（SFT）和引入评估器反馈（Feedback）均能显著提升生成质量，验证了多智能体闭环架构中每一关键组件的必要性。

### 现有文本到视频生成范式的根本瓶颈

当前主流的文本到视频（Text-to-Video, T2V）生成模型，无论是开源模型如 **CogVideoX-5B** (Hong et al., arXiv 2022)、**Wan2.2-TI2V-5B** (Wan et al., arXiv 2025)，还是闭源商业系统如 **Sora2** (Brooks et al., 2024)、**Veo3** (Google DeepMind, 2024) 和 **Grok Imagine** (xAI, 2025)，其核心生成机制均建立在扩散概率去噪框架之上。这一范式从海量视频数据中隐式学习外观与运动的统计分布，虽然在视觉真实感上取得了显著进展，但其本质是**外观驱动的数据模式记忆**，而非基于因果机制的物理推理。

这一根本性设计缺陷导致了一个可被系统性观测的瓶颈：当面对需要精确遵循牛顿力学的场景时，现有模型频繁产生物理上不可信的生成结果。如图 1 所示，即使是当前最先进的商业 T2V 系统，在物体计数与动量守恒、牛顿力推断、速度与压力计算等基础物理问题上均表现出明显失效。这些失败并非偶然的个案，而是源于扩散模型对物理规律的“黑箱拟合”——模型记忆了训练数据中物体运动的外观相关性，却从未真正理解支配这些运动的因果定律（如动量守恒、能量守恒、重力加速度等）。在分布外（Out-of-Distribution, OOD）提示下，这种统计记忆的脆弱性尤为突出，生成视频的运动轨迹往往严重偏离真实物理。

### 数据驱动物理评估指标的分布外失效

与生成侧的问题相呼应，现有的视频物理合理性评估指标同样面临深层困境。以 **Trajan** 的 Average Jaccard (AJ) 和 **VideoPhy2** 的 Semantic Adherence (SA) 等为代表的数据驱动评估方法，其评分机制依赖于从大规模视频数据中学习到的物理常识模式。当这些指标被用于评估由物理引擎仿真生成的视频时，出现了严重的分布外失效现象：物理上完全正确的仿真视频在这些指标上获得了异常低的分数（如 MoReGen 的 AJ 仅为 0.10，SA 仅为 2.73），而物理上存在明显错误的扩散生成视频反而获得了更高的评分。这一悖论深刻揭示了数据驱动评估范式的内在局限——它们衡量的并非客观的物理保真度，而是生成结果与训练分布中“常见物理外观”的统计相似性。

### MoReGen 的动机与范式转换

上述双重困境——生成侧的物理失准与评估侧的指标失效——共同指向了一个根本需求：文本到视频生成需要一次从“数据外观拟合”到“物理机制模拟”的范式转换。MoReGen 正是在这一动机下提出的。其核心洞察在于：将文本到视频生成重新定义为**从自然语言到可执行物理仿真的翻译任务**，利用大型语言模型（LLM）的代码生成与推理能力，将自然语言描述显式解析为结构化物理规范，并转化为由物理引擎直接驱动的仿真代码。这一范式转换扭转了生成过程的因果路径：视频中的每一帧运动不再是扩散去噪的统计采样结果，而是由确定性物理定律（通过 Pymunk 等物理引擎）严格计算得到的必然产物。

与此同时，MoReGen 首次提出了基于物体轨迹直接测量的评估指标套件（MoRe metrics），包括动态时间规整（DTW）、归一化 DTW（DTW-N）和 Procrustes 分析。这些指标通过直接比较生成视频中关键物体的运动轨迹与真实物理仿真轨迹之间的几何差异，绕开了数据驱动指标对训练分布的先验依赖，为物理一致的视频生成和评价建立了新的基准。

## 核心方法与创新机理

MoReGen 的核心创新在于将文本到视频生成从**数据驱动的外观拟合**重构为**物理机制驱动的显式仿真**。这一范式转换通过三个关键设计槽位的改变得以实现，每条改变都直指现有扩散模型在物理一致性上的根本缺陷。

### 生成范式：从隐式分布学习到显式规则驱动

现有文本到视频模型（如 **Sora2** (Brooks et al., 2024)、**Veo3** (Google DeepMind, 2024)）依赖扩散概率去噪，本质是对训练数据中运动模式的统计记忆。这种隐式分布学习在分布内提示下可以产生视觉逼真的结果，但在分布外场景中频繁违反牛顿力学——物体计数错误、动量不守恒、力学关系推断错误等问题普遍存在（见 Figure 1）。

MoReGen 扭转了这一因果路径：它不再让模型“猜测”运动，而是让模型**生成可执行的物理仿真代码**，由物理引擎（Pymunk）和渲染引擎（Blender）确定性地驱动视频生成。这一设计使得运动轨迹严格遵循牛顿力学，从根本上消除了数据驱动模型固有的物理不可靠性。

### 运动控制：从统计模式记忆到结构化物理规范与多智能体推理

扩散模型对运动的控制是间接的——模型通过去噪过程隐式地“回忆”训练视频中的运动模式，缺乏对物理参数的显式建模。当提示涉及精确的力学关系（如“30度角释放”、“动量传递”）时，模型只能依赖训练分布中的近似，无法保证输出与物理定律一致。

MoReGen 引入了**结构化物理规范**作为中间表示，将自然语言描述显式解析为包含物体属性、初始条件和物理参数的机器可读规范。这一解析由**Text-Parser Agent**完成，并经过监督微调（SFT），损失函数为：

$$\mathcal{L}_{\mathrm{SFT}} = - \mathbb{E}_{(x, S) \sim \mathcal{D}} \left[ \sum_{t=1}^{|S|} \log p_{\theta}(S_t \mid x, S_{<t}) \right]$$

随后，**Code-Writer Agent** 将结构化规范翻译为可执行的仿真代码，直接调用 Pymunk 物理引擎 API。这种“自然语言→结构化规范→可执行代码”的级联推理，使得运动控制从模糊的统计记忆转变为精确的物理参数化，确保了生成视频中每个物体的运动都严格遵循牛顿定律。

### 质量保证：从单向生成到迭代多智能体反馈闭环

扩散模型的生成是单向的——一旦去噪完成，输出即被固定，没有机制验证物理正确性。即使生成结果违反基本力学，模型也无从修正。

MoReGen 设计了**多组件评估器（Evaluator）**，对生成视频进行三维度分析：轨迹对齐（比较估计轨迹 $\mathcal{T}_{est}$ 与真实轨迹 $\mathcal{T}$）、物理合理性（检查运动是否符合力学规律）和意图一致性（验证视频内容与原始提示的语义对齐）。评估结果由 LLM 综合为结构化反馈 $\mathcal{F}$：

$$\mathcal{F} = LLM( \text{“Summarize”}, < LLM( \text{“Traj”}, \mathcal{T}_{est}, \mathcal{T} ), VLM( \text{“Phys”}, v_t ), VLM( \text{“Intent”}, v_t, x ) > )$$

该反馈被送回 Code-Writer Agent，指导代码的迭代修正。消融实验证实，引入单次评估器反馈后，GPT-5 在 AJ 和 OA 指标上获得最大增益，而综合 SFT 和 Feedback 的配置在所有评估指标上均优于单一优化配置（Table 4），验证了闭环修正机制的有效性。

### 创新支撑：MoRe 指标揭示分布外失效

MoReGen 的范式创新还催生了配套的评估体系——**MoRe metrics**（DTW、DTW-N、Procrustes）。这些指标直接测量生成视频中物体运动轨迹与物理仿真真实轨迹的偏差，首次实现了对运动物理保真度的定量评估。

关键发现是：现有数据驱动的物理评估指标（如 Trajan 的 AJ 和 VideoPhy2 的 SA）在评估物理仿真生成的视频时出现严重的**分布外失效**——MoReGen 在这些指标上得分异常低（Table 3），而 MoRe metrics 却准确反映了其轨迹保真度的优势（Table 2）。这一对比不仅验证了 MoReGen 的物理一致性，更暴露了当前评估范式的根本局限：数据驱动指标衡量的是“与训练分布有多像”，而非“与物理定律有多一致”。

MoReGen 将文本到视频生成重新定义为**从自然语言到可执行物理仿真的翻译任务**，其核心因果路径从传统扩散模型的“数据外观拟合”扭转为“物理机制模拟”。系统由三个协作智能体与一个多组件评估器构成闭环，如图2所示。

### 输入输出流

给定一个自由格式的自然语言提示 $x$，系统最终输出一段物理上严格符合牛顿力学的渲染视频 $v$，同时产出可复现的可执行仿真代码 $C$ 及物体轨迹遥测数据 $\mathcal{T}$。整个流程可概括为：

1. **文本解析**：$\mathcal{A}_{\text{text}}$ 将 $x$ 映射为结构化物理规范 $S$
2. **代码生成**：$\mathcal{A}_{\text{coder}}$ 将 $S$ 翻译为可执行仿真代码 $C_t$
3. **仿真渲染**：$\mathcal{A}_{\text{render}}$ 在沙盒中执行 $C_t$，生成轨迹 $\mathcal{T}$ 与视频 $v_t$
4. **评估反馈**：$\mathcal{E}$ 分析 $v_t$ 的轨迹对齐、物理合理性与意图一致性，生成反馈 $\mathcal{F}$ 送回 $\mathcal{A}_{\text{coder}}$ 进行迭代修正

### 模块关系与协作机制

**Text-Parser Agent ($\mathcal{A}_{\text{text}}$)** 是整个管道的入口。它接收自然语言描述，输出包含全部物体、参数与初始条件的结构化物理规范。为确保映射的鲁棒性，该智能体在 1,200 个精心策划的文本-规范对上进行了监督微调（SFT），损失函数为：

$$\mathcal{L}_{\mathrm{SFT}} = - \mathbb{E}_{(x, S) \sim \mathcal{D}} \left[ \sum_{t=1}^{|S|} \log p_{\theta}(S_t \mid x, S_{<t}) \right]$$

微调后的模型即使在欠指定或措辞多样的描述下，也能生成完整且物理上自洽的结构化规范。

**Code-Writer Agent ($\mathcal{A}_{\text{coder}}$)** 接收 $\mathcal{A}_{\text{text}}$ 输出的结构化规范，生成调用物理引擎 API（如 Pymunk）的可执行仿真代码 $C_t$。该代码负责模拟底层的牛顿运动过程，是连接语言理解与物理执行的关键桥梁。

**Video-Render Agent ($\mathcal{A}_{\text{render}}$)** 在沙盒化环境中执行代码 $C_t$，同步产出两类输出：(1) 物体运动轨迹遥测数据 $\mathcal{T}$；(2) 渲染视频 $v_t$。这种双输出设计使得后续评估可以同时利用精确的数值轨迹和视觉信息。

**Evaluator ($\mathcal{E}$)** 是闭环修正的核心。它综合三个维度的分析：

$$\mathcal{F} = LLM( \text{``Summarize''}, \langle LLM( \text{``Traj''}, \mathcal{T}_{est}, \mathcal{T} ), VLM( \text{``Phys''}, v_t ), VLM( \text{``Intent''}, v_t, x ) \rangle )$$

- **轨迹对齐**：对比估计轨迹 $\mathcal{T}_{est}$ 与真实轨迹 $\mathcal{T}$
- **物理合理性**：由视觉语言模型评估视频的物理可信度
- **意图一致性**：验证视频内容与原始提示 $x$ 的语义对齐

三个维度的分析结果由 LLM 总结为可操作的改进建议 $\mathcal{F}$，反馈至 $\mathcal{A}_{\text{coder}}$ 触发代码修正。消融实验证实，引入评估器反馈能显著提升生成质量，尤其在轨迹对齐指标上带来最大增益。

### 范式对比

与传统扩散模型相比，MoReGen 在三个关键维度上实现了范式转变：

| 维度 | 扩散模型基线 | MoReGen |
|------|-------------|---------|
| 生成范式 | 扩散概率去噪（隐式分布学习） | 代码生成 + 物理引擎仿真（显式规则驱动） |
| 运动控制 | 数据驱动的统计模式记忆 | 结构化物理规范 + 多智能体推理 |
| 质量保证 | 单向生成，无显式物理验证 | 迭代多智能体反馈闭环（轨迹/物理/意图评估） |

这一架构设计使得 MoReGen 能够直接生成可复现的物理仿真代码，从根本上避免了数据驱动模型在分布外场景下的物理规律违反问题。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Bai_MoReGen_Multi_Agen/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our multi-agent motion-reasoning engine (MoReGen) for physics-grounded text-to-video synthesis. MoReGen focuses on achieving high-precision Newtonian motion through coordinated multi-agent reasoning. Given a natural language prompt, the text-parser agent*

MoReGen 将文本到视频生成重新定义为从自然语言到可执行物理仿真的翻译任务，其核心由三个协作智能体与一个多组件评估器构成闭环（见 Figure 2）。整个管线将自由格式的文本提示逐步转化为结构化物理规范、可执行仿真代码、渲染视频，并通过反馈机制迭代修正，从而保证生成视频的牛顿力学一致性。

### Text-Parser Agent（A_text）：自然语言到结构化规范的映射

文本解析器智能体 A_text 负责将自由格式的自然语言描述解析为结构化的物理仿真规范，该规范显式包含场景中所有物体、物理参数及初始条件。为使智能体学习从语言线索到物理参数的鲁棒映射，作者在 1,200 条精心构建的文本-规范对数据上，对 Qwen2.5-Coder-14B 进行监督微调（SFT），优化目标为标准的下一 token 预测损失：

$$ \mathcal{L}_{\mathrm{SFT}} = - \mathbb{E}_{(x, S) \sim \mathcal{D}} \left[ \sum_{t=1}^{|S|} \log p_{\theta}(S_t \mid x, S_{<t}) \right] $$

其中 $x$ 为自然语言提示，$S$ 为目标结构化规范序列，$\theta$ 为模型参数。微调后的模型即使在描述欠指定或措辞多变的情况下，也能生成完整且物理上自洽的结构化规范。

### Code-Writer Agent（A_coder）：规范到仿真代码的翻译

代码编写器智能体接收 A_text 输出的结构化规范，直接生成可执行的物理仿真代码 $C_t$。该代码调用 Pymunk 等物理引擎 API 来模拟底层的牛顿运动过程，从而将运动生成从数据驱动的统计模式记忆扭转为显式的物理规则驱动。

### Video-Render Agent（A_render）：仿真执行与视频渲染

渲染智能体在沙盒环境中执行仿真代码 $C_t$，同步产出两类输出：(1) 物体轨迹的遥测数据（用于后续定量评估）；(2) 渲染后的视频 $v_t$。

### Evaluator（E）与反馈闭环

评估器综合三个维度的分析结果，形成反馈 $\mathcal{F}$ 以指导代码修正：

$$ \mathcal{F} = LLM( \text{“Summarize”}, < LLM( \text{“Traj”}, \mathcal{T}_{est}, \mathcal{T} ), VLM( \text{“Phys”}, v_t ), VLM( \text{“Intent”}, v_t, x ) > ) $$

其中 $\mathcal{T}_{est}$ 为估计轨迹，$\mathcal{T}$ 为真实轨迹。三个分析维度分别为：**轨迹对齐**（由 LLM 比较估计与真实轨迹）、**物理合理性**（由 VLM 评估视频 $v_t$ 的物理正确性）、**意图一致性**（由 VLM 判断视频 $v_t$ 与原始文本 $x$ 的语义对齐程度）。最终由 LLM 将上述分析总结为可操作的改进反馈 $\mathcal{F}$，反馈至 A_coder 进入下一轮迭代修正。消融实验（Table 4）证实，引入单次评估器反馈即可在 AJ 和 OA 等指标上带来显著增益，验证了该闭环机制的有效性。

## 实验与关键发现

### 评估基准与指标设计

为系统评估物理一致的视频生成能力，本研究构建了**MoReSet**基准数据集，涵盖九类典型牛顿力学现象（如牛顿摆、抛物运动、碰撞守恒等），共包含1,275个视频。其中训练集由1,200个Blender生成的物理仿真视频组成，测试集包含75个真实世界实验室拍摄的视频。如Table 1所示，与其他物理导向的T2V数据集相比，MoReSet的独特之处在于同时提供轨迹标注、物理提示和仿真代码，为精确评估运动保真度提供了必要的基础设施。

评估体系包含两类指标：本研究提出的**MoRe指标族**，以及现有数据驱动的物理评估指标。MoRe指标直接测量生成视频中物体运动轨迹与真实轨迹的几何对齐程度，包含三个维度：

- **动态时间规整（DTW）**：将估计轨迹与不同时间长度的真实序列投影到非线性空间进行对齐，衡量全局轨迹偏差；
- **归一化DTW（DTW-N）**：对轨迹先进行中心化处理，再缩放至单位弧长，消除不同视频尺度与时长的影响；
- **Procrustes分析（Procrustes）**：通过刚性变换对齐后计算形状差异，衡量轨迹的几何结构保真度。

轨迹提取流程为：根据结构化规范S识别运动关键物体，利用文本引导的目标检测在初始帧中进行定位，随后在整个视频中跟踪其运动轨迹，最终与地面真值轨迹进行比对。

### 主实验结果：运动轨迹保真度

Table 2展示了各模型在MoRe指标上的运动轨迹保真度对比。MoReGen在所有三个指标上均取得最优性能：

- **DTW**达到8.93 ± 9.61，显著优于所有对比模型，表明其生成的轨迹在时序对齐上与真实物理运动最为接近；
- **DTW-N**低至0.06 ± 0.07，说明经过尺度和时长归一化后，轨迹偏差极小；
- **Procrustes**达到0.48 ± 0.30，在几何形状保持方面同样领先。

相比之下，当前最先进的商业模型（包括**Sora2**、**Veo3**和**Grok Imagine**）在MoRe指标上表现不佳，反映出这些数据驱动模型在物理运动精确性上的根本性局限。开源模型如**Wan2.2-TI2V-5B**、**CogVideoX-5B**的轨迹偏差更为显著。值得关注的是，同为物理仿真路线的**Newton-Gen**和**WISA**在MoRe指标上也明显弱于MoReGen，这归因于MoReGen的多智能体协作架构与迭代反馈机制对物理规范解析和代码生成质量的系统性提升。

定性分析进一步验证了上述定量结果。以牛顿摆场景为例（Figure 4），MoReGen生成的视频正确模拟了动量传递与碰撞过程：左侧球体释放后撞击相邻球体，动量逐球传递至最右端球体弹出，且摆动角度随能量损耗逐渐减小。而Sora2、Veo3等模型要么未能正确表现动量传递机制，要么物体运动违反能量守恒定律。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Bai_MoReGen_Multi_Agen/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of our model with recent open-source and commercial models, prompted to generate a video of Newton’s cradle. We used the same prompt across the board: “Generate a video that showcase the following scene: Five shiny metal balls of a newton’s cradle is visible, along with parts of a single vertical string for each metal ball respectively. These strings keeps their respective metal ball suspended. The top part of the newton’s cradle is not visible. The camera faces all the five metal balls. The first and leftmost ball is at an angle of 30 degrees from the cradle and released. Due to gravity, the ball comes and strikes the second ball from the left. This causes momentum t...*

### 数据驱动指标的分布外失效

Table 3揭示了现有数据驱动物理评估指标在评估物理仿真生成视频时的严重局限。在**VideoPhy2**的物理一致性（PC）指标上，MoReGen以4.53 ± 0.69取得最优，这与其物理引擎驱动的生成范式相符。然而，在语义遵循（SA）指标上，MoReGen仅得2.73 ± 0.44，在所有模型中排名最低。这一反常现象的根本原因在于：VideoPhy2的评估模型基于大规模互联网视频训练，其“语义遵循”判断严重依赖于视觉外观的统计模式，而非物理合理性。MoReGen生成的Blender渲染视频在视觉纹理上与真实视频存在域差异，导致数据驱动评估器给出错误低分。

**Trajan**指标的结果更为极端：MoReGen的平均Jaccard（AJ）仅为0.10 ± 0.03，遮挡准确率（OA）为0.64 ± 0.05，均为所有模型中的最低值。Trajan依赖BootsTAP的点跟踪自编码器，该编码器同样在真实世界视频上训练，当面对物理仿真生成的干净、无噪声轨迹时，其重建机制发生分布外失效，无法正确评估时序一致性。

这一对比实验揭示了一个关键洞察：**数据驱动的评估方法在分布外条件下会系统性地失效**，而基于轨迹直接测量的MoRe指标能够准确反映物理保真度，不受视觉域差异的影响。这为物理一致视频生成领域建立更可靠的评估范式提供了实证依据。

### 消融实验：架构组件的因果贡献

Table 4的消融实验系统验证了MoReGen架构中两个关键组件的因果贡献：**监督微调（SFT）**和**评估器反馈（Feedback）**。实验在两种代码编写器（Qwen2.5-Coder-14B和GPT-5）上分别进行。

**监督微调的效果**：对文本解析器进行SFT后，Qwen2.5-Coder在DTW、DTW-N、Procrustes和PC指标上均获得显著提升。SFT使文本解析器学会从自然语言中稳健地提取物理参数并生成结构化规范，减少了因语言歧义导致的规范错误，进而提高了下游代码生成的质量。例如，SFT后DTW从较高水平降至更优值，表明轨迹对齐精度得到实质性改善。

**评估器反馈的增益**：引入单次评估器反馈迭代后，GPT-5在AJ和OA指标上获得最大增益，证明了多智能体反馈闭环的有效性。反馈机制综合了轨迹对齐、物理合理性和意图一致性三个维度的分析结果，由LLM总结为可操作的改进建议，指导代码编写器修正仿真代码中的物理参数偏差或逻辑错误。

**协同效应**：同时应用SFT和Feedback的配置在所有评估指标上均优于仅使用单一优化的配置，验证了两个组件的协同互补关系——SFT提升初始生成质量，反馈机制则在此基础上进行精细修正。这一消融结果确证了MoReGen架构中每一设计组件均不可替代。

### 失败模式与局限性分析

尽管MoReGen在物理运动保真度上取得突破性进展，但实验中也暴露出若干值得关注的失败模式：

1. **渲染质量的域差距**：Blender渲染的视频在视觉真实感上与真实世界视频存在明显差距，这是导致数据驱动指标（如VideoPhy2的SA、Trajan的AJ）评分异常低的直接原因。提升渲染真实感（例如引入更先进的材质和光照模型）是未来工作的重要方向。

2. **物理现象覆盖范围有限**：当前框架仅覆盖九类牛顿力学现象，对于流体力学、电磁学或多物理场耦合等更复杂的物理交互，尚需验证框架的扩展性。

3. **代码生成鲁棒性**：尽管SFT和反馈机制显著提升了成功率，但代码编写器仍可能生成包含语法错误的仿真代码。当前依赖GPT-5进行错误修正，其在不同LLM上的鲁棒性差异需要进一步系统评估。

4. **评估指标的人类一致性**：MoRe指标作为物理保真度的直接度量，其与人类对物理合理性感知判断之间的一致性尚未经过系统性验证，这是确立其作为标准评估工具的关键步骤。

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Bai_MoReGen_Multi_Agen/figures/005_Table_2.jpg]]
*Table 2: Comparison of object motion trajectories across state-of-the-art T2V models, evaluated using MoRe metrics. To ensure comprehensive object coverage, the initial object detection stage was manually supervised by a human annotator. For objects that did not appear in videos, a random pixel is selected. DTW-N stands for normalized DTW distance, where trajectories are first centered and then scaled down to unit arc length. All videos are downsampled to 480p resolution at 10 frames per second. Bold text indicates best performance*

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Bai_MoReGen_Multi_Agen/figures/006_Table_3.jpg]]
*Table 3: Comparison of physical validity and consistency across stateof-the-art T2V models (Wan2.2-TI2V-5B [47], LTXV-2B-Distilled [21], CogVideoX-5B [23], Veo3 [18], Grok Imagine [50], Sora2 [11], Newton-Gen [53] and WISA [48]) using physics-based video evaluation metrics. For Trajan, videos were resized to 256×256 and 128 points were sampled. AJ denotes average Jaccard, and OA denotes occlusion accuracy. For VideoPhy, each video was rated from 1 to 5 based on semantic adherence (SA) and physics consistency (PC). We report the mean and standard deviation for all evaluated T2V models. Bold text indicates best performance*

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Bai_MoReGen_Multi_Agen/figures/008_Table_4.jpg]]
*Table 4: Comparison of model performance gains from supervised fine-tuning (SFT) and evaluator feedback. Evaluation was conducted using the designated evaluation set from our dataset, with tests performed on Qwen2.5 Coder and GPT-5. Feedback involves one iteration of processing the video to extract object trajectories, comparing them with ground truth, and obtaining an overall evaluation from Qwen2.5-VL. GPT-5 then summarizes this evaluation into a list of actionable improvements, which are fed into the Coder Agent. If the code contains syntax error, GPT-5 is asked to correct the issue without providing the full code. Bold text indicates best performance*

![[assets/figures/papers/paper_list_l10_https_openaccess_thecvf_com_content_CVPR2026_html_Bai_MoReGen_Multi_Agen/figures/003_Table_1.jpg]]
*Table 1: Comparison of our dataset with recent physics-based T2V datasets. Symbols indicate whether each dataset contains data for the listed properties: ✓ denotes inclusion, while × indicates absence. We define Physics-based Prompts as those that explicitly specify the relevant physical principles and mathematical properties governing the behavior of objects and environments. As of the time of writing, the HQ-Phy dataset has not been publicly released*

## 定位与知识库关联

### 从外观驱动到物理驱动的范式迁移

当前主流的文本到视频（T2V）生成模型，无论是开源模型如 **CogVideoX-5B** (Hong et al., arXiv 2022)、**Wan2.2-TI2V-5B** (Wan et al., arXiv 2025)、**LTXV-2B-Distilled** (HaCohen et al., arXiv 2024)，还是商业闭源系统如 **Sora2** (Brooks et al., 2024)、**Veo3** (Google DeepMind, 2024) 与 **Grok Imagine** (xAI, 2025)，其核心生成范式均建立在扩散概率模型之上。这类方法将视频生成视为从噪声分布到数据分布的隐式映射学习过程，其运动生成能力本质上是**数据驱动的统计模式记忆**——模型通过海量视频数据的训练来拟合外观与运动的联合分布，而非理解或模拟支配物体运动的物理规律。

MoReGen 通过**生成范式的根本性转换**切断了这一因果链条。它将文本到视频生成重新定义为从自然语言到可执行物理仿真代码的翻译任务，将生成的控制权从扩散模型的隐式去噪过程转移到显式的物理引擎仿真。这一转变的核心在于：扩散模型隐式地记忆“物体通常如何运动”的统计关联，而 MoReGen 显式地计算“物体在当前物理约束下必须如何运动”的确定性结果。由此，生成视频中物体轨迹的因果来源从训练数据的分布特征转变为牛顿力学方程的数值积分，从而在机制层面消除了违反动量守恒、能量守恒等基本物理定律的可能性。

### 与物理感知生成方法的边界划分

在物理感知视频生成这一新兴方向上，MoReGen 与若干同期工作形成了清晰的方法论分界线。

**Newton-Gen** (Yuan et al., arXiv 2025) 和 **WISA** (Wang et al., arXiv 2025) 代表了将物理先验注入扩散框架的尝试。这类方法在扩散模型内部或输入端引入物理约束信号，试图在不改变生成范式的前提下提升物理一致性。然而，它们仍然受限于扩散模型对训练数据分布的根本依赖：当测试提示的物理场景显著偏离训练分布（即分布外，OOD）时，统计模式记忆无法可靠地外推到未见过的物理条件。MoReGen 的代码生成+物理引擎方案则天然具备对分布外场景的泛化能力——只要物理引擎的仿真模型覆盖了相关力学规律，代码编写智能体就能生成正确的仿真逻辑，无需依赖相似场景的训练样本。

**WISA** 的另一个关键区别在于其资产生成方式：WISA 使用 Qwen3-4B 从提示中生成资产 `.json` 文件，随后在仿真环境中渲染，但其物理推理能力受限于单一模型的端到端生成，缺乏结构化的物理规范解析和多轮反馈修正机制。MoReGen 的多智能体协作架构——文本解析器将自然语言显式转换为结构化物理规范，代码编写器基于规范生成仿真代码，评估器提供轨迹、物理和意图三个维度的反馈——构成了一个**可审计、可修正的推理闭环**，这是单智能体方案难以实现的。

### 评估范式创新的知识贡献

MoReGen 的另一项重要方法论贡献在于揭示了现有数据驱动物理评估指标的**分布外失效**问题。Table 3 的实验结果表明，Trajan 的 Average Jaccard (AJ) 指标和 VideoPhy2 的 Semantic Adherence (SA) 指标在评估 MoReGen 生成的物理仿真视频时给出了异常低的分数（AJ: 0.10 ± 0.03, SA: 2.73 ± 0.44），而 MoReGen 在直接测量轨迹保真度的 MoRe 指标（DTW, DTW-N, Procrustes）上显著优于所有对比模型。这一矛盾暴露了一个深层问题：Trajan 和 VideoPhy2 等指标基于从真实世界视频数据中训练得到的评估模型，这些模型隐式地将“视觉真实感”与“物理合理性”混为一谈。当面对物理精确但渲染风格与真实视频分布不同的仿真视频时，这些指标产生系统性误判。

MoRe metrics（DTW、DTW-N、Procrustes）通过直接测量生成视频中物体轨迹与真实轨迹的几何对齐程度，绕开了对视觉分布的先验依赖。这一评估范式的转变为物理一致视频生成领域建立了一个**与生成方法解耦的客观度量标准**，使得不同范式（扩散生成 vs. 物理仿真）的方法能够在统一的物理保真度尺度上进行公平比较。

### 适用边界与技术局限

MoReGen 的当前能力边界由三个因素共同界定：

**物理现象的覆盖范围**。MoReSet 数据集覆盖九类牛顿力学现象（自由落体、抛体运动、碰撞、单摆、弹簧振子、斜面滑动、牛顿摆、圆周运动、浮力），MoReGen 的文本解析器在这些现象类别上进行了监督微调。框架能否经济地扩展至流体力学、电磁学、热力学或更复杂的多物理场耦合场景，取决于：（1）是否有相应的开源物理引擎支持；（2）代码编写智能体能否可靠地生成跨物理域的仿真代码。这一扩展性问题目前尚无实验验证。

**代码生成的鲁棒性依赖**。MoReGen 的生成成功率直接受限于代码编写智能体的能力。消融实验（Table 4）显示，监督微调（SFT）和评估器反馈均能显著提升性能，但论文未报告代码首次生成的成功率（syntax error rate）以及自我修复机制在不同 LLM 上的鲁棒性差异。对特定物理引擎（Pymunk）的 API 依赖也意味着移植到其他仿真后端时需要重新适配代码生成模板。

**渲染真实感与物理准确性的权衡**。MoReGen 使用 Blender 进行视频渲染，生成的视频在视觉真实感上与真实世界视频存在明显差距。这一差距不仅影响用户体验，更重要的是，它导致了前述数据驱动评估指标的分布外失效——现有的视觉质量评估工具无法公平地评价物理仿真视频。如何在提升渲染质量的同时保持物理轨迹的确定性不变，是框架走向实际应用必须解决的问题。

### 开放问题

基于上述分析，MoReGen 框架引出了以下待验证的开放问题：

1. **跨物理域扩展的经济性**：将当前九类牛顿力学现象扩展至流体、电磁学或多物理场耦合场景时，结构化物理规范的表示能力是否足够通用？文本解析器的微调数据需求是否会随物理域数量线性增长？

2. **LLM 代码生成的可靠性边界**：不同代码 LLM（如 Qwen2.5-Coder、GPT-5、Claude 等）在生成物理仿真代码时的首次成功率、语法错误类型分布和自我修复能力是否存在系统性差异？是否存在某些物理场景类型对当前 LLM 构成一致的生成挑战？

3. **评估指标的人类一致性验证**：MoRe metrics 作为物理保真度的直接度量，其与人类对物理合理性的感知判断之间的一致性尚未经过系统性的人类研究验证。低 DTW 值是否必然对应人类感知中的“更物理合理”的视频，仍需实证支持。

4. **渲染-物理解耦的保真度上限**：在保持物理仿真确定性的前提下，渲染真实感能提升到何种程度？是否可能在渲染阶段引入基于生成模型的视觉增强而不破坏底层轨迹的物理一致性？

## 原文 PDF

![[paperPDFs/CVPR_2026/MoReGen_Multi_Agent_Motion_Reasoning_Engine_for_Code_based_Text_to_Video_Synthesis.pdf]]

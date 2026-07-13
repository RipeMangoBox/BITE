---
title: "The Quest for Generalizable Motion Generation: Data, Model, and Evaluation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation.pdf
project_link: null
code_link: https://github.com/black-forest-labs/flux
aliases:
- VFVLD
- QGMGDME
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入视频生成模型（ViGen）在大规模数据中学习的丰富语义先验，通过门控双分支（T2M与M2M）架构自适应融合，同时通过大规模多源数据集（ViMoGen-228K）和蒸馏策略（ViMoGen-light）进行扩展。
primary_logic: 视频生成模型的语义泛化能力可以通过专门设计的门控双分支扩散变换器有效迁移至运动生成任务，与大规模、高质量、多源的数据集协同，可显著突破运动生成模型的泛化瓶颈。
claims:
- ViMoGen在MBench的Motion Generalizability上达到0.68，远超最佳基线MotionLCM的0.55。
- 自适应门控分支选择（Adaptive Gating）在泛化性上显著优于仅使用T2M或M2M的单一分支。
- ViMoGen-light通过知识蒸馏有效保留了泛化能力，在MBench上Generalizability得分0.55，与最强基线持平，且无需视频生成模型。
- MLD+ViMoGen-light在HumanML3D测试集上取得了R Precision Top-1 0.542的SOTA文本-运动一致性，同时FID显著优于MLD基线（0.114 vs 0.473）。
---

# The Quest for Generalizable Motion Generation: Data, Model, and Evaluation

> [!tip] 核心洞察
> 视频生成模型的语义泛化能力可以通过专门设计的门控双分支扩散变换器有效迁移至运动生成任务，与大规模、高质量、多源的数据集协同，可显著突破运动生成模型的泛化瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可泛化运动生成探索：数据、模型与评估 |
| 英文题名 | The Quest for Generalizable Motion Generation: Data, Model, and Evaluation |
| 会议/期刊 | ICLR 2026 |
| Links | [Code](https://github.com/black-forest-labs/flux) · [paper](https://arxiv.org/abs/2410.08260) · [paper](https://openreview.net/forum?id=kPkvPeQ4b7) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | ViMoGen (full) and ViMoGen-light (distilled) |
| Dataset | MBench, HumanML3D |

> [!tip] 效果简介
> - MBench 上，Motion Generalizability (↑) 0.68 vs 0.55 (MotionLCM) (+0.13)；Motion Condition Consistency (↑) 0.53 vs 0.48 (MotionLCM) (+0.05)。
> - HumanML3D 上，R Precision Top-1 (↑) 0.542 (MLD+ViMoGen-light) vs 0.521 (MoMask) (+0.021)。

## 概要

### 问题瓶颈

当前文本到运动（Text-to-Motion, T2M）生成模型在长尾、复杂语义指令上的泛化能力严重不足。其根本原因在于运动数据的规模远小于文本、图像等其他模态——主流基准HumanML3D仅包含约1.5万个运动片段，语义覆盖极为有限，导致模型难以处理武术、动态体育、多步骤行为等开放域提示。

### 核心思路

本文提出**ViMoGen**，通过引入视频生成模型在大规模数据中习得的丰富语义先验来突破上述瓶颈。其核心洞察是：视频生成模型（如Wan2.1）的语义泛化能力可以通过专门设计的门控双分支扩散变换器（DiT）有效迁移至运动生成任务。具体而言，ViMoGen构建了**T2M（Text-to-Motion）**和**M2M（Motion-to-Motion）**两个条件生成分支——前者基于文本与光学动作捕捉（MoCap）先验保证运动质量，后者利用视频模型生成的参考视频提取运动token以注入语义泛化知识，并通过自适应门控模块在二者间动态选择。同时，本文构建了大规模多源数据集**ViMoGen-228K**（228,236个片段，369.4小时），并提出了蒸馏变体**ViMoGen-light**，在保留泛化能力的前提下消除对视频生成模型的推理依赖。

### 方法定位

ViMoGen属于**基于扩散变换器的双分支条件运动生成框架**。与仅使用CLIP文本编码和单一T2M分支的主流方法（如MDM、T2M-GPT、MoMask、MotionLCM等）相比，其关键差异在于：

- **文本编码器**：采用T5-XXL替代CLIP，在泛化性与运动质量间取得更优平衡。
- **视频运动先验**：通过离线ViGen模型和视觉MoCap管线（CameraHMR、SMPLest-X）提取视频运动token作为M2M分支的条件。
- **分支架构**：双分支门控DiT，约66%参数共享，通过VLM对齐检查和数据质量课程自适应选择激活分支。
- **训练数据**：从HumanML3D的14,616片段扩展至ViMoGen-228K的228,236片段，涵盖光学MoCap、野生视频和合成视频三类来源。
- **知识蒸馏**：ViMoGen-light利用教师模型生成14k合成提示进行蒸馏，移除视频生成依赖。

### 主要结果

在MBench泛化性基准上，ViMoGen取得**Motion Generalizability 0.68**，远超最佳基线MotionLCM的0.55（+0.13）；Motion Condition Consistency达到0.53，同样优于MotionLCM的0.48（+0.05）。消融实验表明，自适应门控分支选择是泛化性提升的关键——相比仅使用T2M分支（0.54）或M2M分支（0.59），自适应策略达到0.68。在数据层面，逐步添加合成视频数据带来最大的泛化增益（从0.44提升至0.55）。蒸馏变体ViMoGen-light在MBench上Generalizability得分0.55，与最强基线持平；在HumanML3D测试集上，MLD+ViMoGen-light取得R Precision Top-1 0.542的SOTA文本-运动一致性，FID从MLD基线的0.473大幅降至0.114。



### 文本到运动生成的泛化瓶颈

3D人体运动生成是计算机视觉与图形学领域的核心任务之一，其目标是根据自然语言描述生成逼真、语义一致的人体运动序列。近年来，基于扩散模型（如**MDM**，Tevet et al., 2023）和自回归架构（如**T2M-GPT**，Zhang et al., 2023a）的方法在标准基准HumanML3D上取得了显著进展，R Precision Top-1等指标持续攀升。

然而，现有方法面临一个根本性瓶颈：**在长尾、复杂语义指令上的泛化能力严重不足**。这一问题的根源在于运动数据的规模远小于文本、图像等其他模态——主流训练集HumanML3D仅包含约14,616个运动片段，语义覆盖极为有限。Figure 3(a)直观地揭示了这一差距：HumanML3D的动词分布高度集中于少数高频动作（如“行走”、“站立”），而MBench基准则呈现出更均衡、更多样的动词覆盖。当面对“武术套路”、“动态体育动作”、“多步骤复杂行为”等开放域提示时，现有模型往往生成物理上不合理或语义严重偏离的运动。

### 现有方法的三个核心缺口

**数据规模缺口**：光学运动捕捉（MoCap）数据虽然精度高，但采集成本昂贵、场景受限，难以覆盖开放世界的动作多样性。现有数据集如AMASS（统一了29个来源）虽然整合了大量MoCap数据，但总量仍远不足以支撑泛化性训练。大规模野外视频中蕴含着丰富的运动先验，但如何将其转化为高质量、可训练的3D运动数据，一直缺乏系统性方案。

**语义先验缺口**：当前主流方法仅依赖文本编码器（如CLIP）提取语义条件，其语义理解能力受限于文本-图像对比学习的范式，难以捕捉细粒度动作语义和物理合理性约束。视频生成模型（如Wan2.1等ViGen模型）在海量视频数据上学习到了丰富的运动动力学和语义关联，但如何将这一先验有效迁移至3D运动生成任务，尚未被充分探索。

**评估体系缺口**：HumanML3D等现有基准的测试集与训练集分布高度相似，无法有效衡量模型的泛化能力。缺乏一个系统性的评估框架，能够从运动质量、提示遵循度和泛化性等多个维度，对模型的开放域生成能力进行可靠度量。

### 本文的核心动机与解决思路

针对上述三个缺口，本文提出**ViMoGen**框架，其核心洞察是：**视频生成模型的语义泛化能力可以通过专门设计的门控双分支扩散变换器有效迁移至运动生成任务，与大规模、高质量、多源的数据集协同，可显著突破运动生成模型的泛化瓶颈**。

具体而言，本文从数据、模型和评估三个维度协同推进：

- **数据维度**：构建**ViMoGen-228K**，一个包含228,236个运动片段（369.4小时）的大规模多源数据集，整合光学MoCap（171,542片段）、野外视频和合成视频数据，通过Gemini 2.0自动标注和CameraHMR/SMPLest-X视觉MoCap管线实现规模化处理。
- **模型维度**：设计门控双分支扩散变换器架构，包含Text-to-Motion（T2M）分支和Motion-to-Motion（M2M）分支。T2M分支基于MoCap先验保证运动质量，M2M分支通过离线ViGen模型引入视频语义泛化知识；自适应门控模块根据数据质量和VLM对齐检查动态选择分支。进一步提出**ViMoGen-light**，通过知识蒸馏移除对视频生成模型的推理依赖。
- **评估维度**：构建**MBench**基准，系统评估九个维度（运动质量、提示遵循、泛化性等），并通过人类偏好标注验证自动评估指标的可靠性（Spearman ρ显著正相关）。



## 核心方法与创新机理

### 问题根因与创新动机

当前文本到运动（Text-to-Motion, T2M）模型在长尾、复杂语义指令上的泛化能力严重不足。其根本瓶颈在于：运动数据规模远小于文本、图像等其他模态——主流基准 HumanML3D 仅包含约 14,616 个运动片段，语义覆盖极为有限，导致模型难以处理超出训练分布的提示。本文的核心洞察是：**视频生成模型在大规模数据中习得的丰富语义先验，可以通过专门设计的门控双分支架构有效迁移至运动生成任务**，与大规模、高质量、多源数据集协同，显著突破泛化瓶颈。

### 关键创新点（Changed Slots）

与现有 T2M 方法相比，ViMoGen 在以下五个关键维度上进行了根本性改造：

**1. 视频运动先验的引入（Video Motion Prior）**

现有基线方法（如 MDM、T2M-GPT、MoMask 等）仅依赖文本条件生成运动，缺乏对复杂语义的视觉锚定。ViMoGen 创新性地引入离线视频生成模型（ViGen，基于 Wan2.1）作为语义先验源：从文本提示生成参考视频，再通过视觉 MoCap 管线（CameraHMR + SMPLest-X）提取 3D 人体运动 token，作为 Motion-to-Motion（M2M）分支的条件输入。这一设计将视频模型的开放域语义理解能力“蒸馏”为运动生成的引导信号。

**2. 门控双分支架构（Gated Dual-Branch Architecture）**

传统方法使用单一的 Text-to-Motion 分支。ViMoGen 构建了 T2M 和 M2M 双分支交叉注意力架构，共享约 66% 的 DiT 参数，并通过自适应门控模块（Adaptive Gating）在每个扩散块中动态选择激活分支：
- **T2M 分支**：基于文本嵌入和 MoCap 先验，保证运动质量和物理合理性；
- **M2M 分支**：基于视频运动 token，引入 ViGen 的语义泛化知识。

门控策略通过 VLM 对齐检查和数据质量课程进行调控：对人工标注的高质量数据优先激活 T2M 分支，对大规模自动标注数据则鼓励更广泛地探索 M2M 分支。消融实验（Table 3）表明，自适应门控在 Motion Generalizability 上达到 0.68，显著优于仅使用 T2M（0.54）或 M2M（0.59）的单一分支。

**3. 文本编码器的升级**

大多数 T2M 基线使用 CLIP 作为文本编码器。ViMoGen 改用 T5-XXL，在泛化性与运动质量之间取得最佳平衡（Generalizability 0.44 vs. CLIP 的 0.35），同时避免了 MLLM 带来的运动质量下降（Table 6）。

**4. 大规模多源数据集（ViMoGen-228K）**

训练数据从 HumanML3D 的 14,616 个片段扩展至 ViMoGen-228K 的 228,236 个片段（369.4 小时），涵盖三类来源（Table 1）：
- 光学 MoCap 数据（171,542 片段）：保证运动精度；
- 野生视频数据：提供场景多样性；
- 合成视频数据：战略性生成以覆盖语义长尾。

消融实验（Table 5）显示，逐步添加合成视频数据带来最大的泛化增益（Motion Generalizability 从 0.44 提升至 0.55）。

**5. 知识蒸馏与轻量化部署（ViMoGen-light）**

为消除推理时对视频生成模型的依赖，ViMoGen-light 通过教师模型生成 14k 合成运动-文本对进行蒸馏训练。该轻量变体在 MBench 上 Generalizability 达 0.55，与最强基线 MotionLCM 持平，且无需任何视频生成模型。在 HumanML3D 测试集上，MLD + ViMoGen-light 取得了 R Precision Top-1 0.542 的 SOTA 文本-运动一致性，同时 FID 显著优于 MLD 基线（0.114 vs. 0.473）（Table 8）。

### 方法谱系与知识库定位

ViMoGen 处于**扩散运动生成**与**视频先验迁移**的交叉点。其 DiT 骨干基于流匹配（Flow Matching）框架，采用整流流插值 $x_t = (1 - t) \epsilon + t x_0$ 和速度场预测损失 $\mathcal{L} = \mathbb{E}_{x_0, \epsilon, t, c} [\| f_{\theta}(x_t, t, c) - v_t \|_2^2]$。与 MotionLCM（Dai et al., 2024）的潜在一致性蒸馏、DNO（Karunratanakul et al., 2024）的扩散噪声优化等后处理增强不同，ViMoGen 从数据和架构层面系统性解决泛化问题。与 MotionCraft（Bian et al., 2025）等基于视频的运动生成方法相比，ViMoGen 的门控双分支设计实现了视频先验与 MoCap 先验的自适应融合，而非简单的条件拼接。



ViMoGen 构建了一个多模态条件融合的文本到运动生成框架，其核心目标是通过引入视频生成模型在大规模数据中习得的丰富语义先验，突破现有模型在长尾、复杂语义指令上的泛化瓶颈。整体 pipeline 以文本提示为唯一显式输入，经由三条并行的信息提取通路汇聚到基于流匹配（Flow Matching）的扩散变换器（DiT）骨干网络，最终生成 3D 人体运动序列。

**输入与多源条件提取。** 给定文本提示后，系统同时启动三条信息提取流水线（Figure 2(a)）：
1. **文本编码通路**：采用 T5-XXL 文本编码器将提示映射为高维语义嵌入，作为后续交叉注意力的文本条件。消融实验表明，T5-XXL 在泛化性与运动质量之间取得了最佳平衡（Generalizability 0.44），优于 CLIP（0.35）和 MLLM（0.46）（Table 6）。
2. **视频生成与运动提取通路**：离线调用 ViGen 视频生成模型（Wan2.1）从文本生成参考视频，随后通过视觉 MoCap 管线（CameraHMR + SMPLest-X）从生成视频中提取 3D 人体运动 token（SMPL-X 表示）。这一通路是语义泛化能力的关键来源，但同时也引入了推理计算开销和足部滑动等视觉 MoCap 伪影。
3. **噪声初始化通路**：从纯噪声 $\\epsilon$ 出发，通过整流流插值 $x_t = (1 - t) \\epsilon + t x_0$ 构造含噪运动输入，作为去噪过程的起点。

**双分支门控融合架构。** 骨干网络由堆叠的门控扩散块（Gating Diffusion Blocks）构成，每个块内部包含自注意力层和两个互斥激活的交叉注意力分支（Figure 2(b)）：
- **Text-to-Motion (T2M) 分支**：以文本嵌入为条件，利用光学 MoCap 数据中习得的运动先验，保证生成运动的物理合理性和运动质量。
- **Motion-to-Motion (M2M) 分支**：以视频运动 token 为条件，将 ViGen 模型从大规模视频数据中学习到的语义泛化知识迁移至运动生成。

两个分支共享约 66% 的 DiT 参数，通过自适应门控模块（Adaptive Gating Module）在每个扩散块中动态选择激活分支。门控决策依据数据集特征课程（curriculum）和 VLM 对齐检查：对于人工标注的高质量 MoCap 数据优先激活 T2M 分支，而对于大规模自动标注数据则鼓励更广泛地激活 M2M 分支。当 M2M 分支激活时，系统对真实运动施加复合噪声（随机损坏、抖动模拟、时序丢弃）以模拟视觉 MoCap 的伪影特征，从而增强模型对不完美视频运动 token 的鲁棒性。

**训练目标与推理流程。** 训练采用流匹配目标函数：
$$\\mathcal{L} = \\mathbb{E}_{x_0, \\epsilon, t, c} [\\| f_{\\theta}(x_t, t, c) - v_t \\|_2^2]$$
其中 $v_t = x_0 - \\epsilon$ 为最优传输路径的速度场。模型学习从含噪运动 $x_t$ 预测速度场，在推理时通过 ODE 求解器从纯噪声逐步去噪生成最终运动序列。

**ViMoGen-light 蒸馏变体。** 为消除推理时对视频生成模型的依赖，ViMoGen-light 通过知识蒸馏策略训练：利用完整的 ViMoGen 教师模型生成约 14k 合成运动-文本对，学生模型仅保留 T2M 分支，直接以文本为条件学习教师模型的泛化行为。该变体在不使用任何视频生成模型的情况下，在 MBench 上取得 Generalizability 0.55，与最强基线持平（Table 2），且在 HumanML3D 测试集上结合 MLD 骨干网络后取得 R Precision Top-1 0.542 的 SOTA 文本-运动一致性（Table 8）。

**数据闭环。** 整个框架的训练数据来自 ViMoGen-228K 数据集（228,236 个运动片段，369.4 小时），涵盖光学 MoCap、野生视频和合成视频三类来源（Table 1），为双分支架构提供了从简单室内活动到复杂户外运动的广泛语义覆盖。

### 补充图表

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ViMoGen. (a) Our model takes a text prompt as input and leverages both a text encoder and an offline video generation model to produce textual and video motion tokens. These are fused with noisy motion inputs through a stack of gating Diffusion Blocks. (b) Each block includes self-attention, an adaptive gating module, and two cross-attention branches: Text-to-Motion (T2M) and Motion-to-Motion (M2M). Only one branch is activated at a time, enabling the model to adaptively balance robustness and generalization*



### 流匹配运动生成基础

ViMoGen 采用基于 DiT（Diffusion Transformer）的流匹配框架进行运动生成。其核心训练目标为速度场预测，公式如下：

$$ \mathcal{L} = \mathbb{E}_{x_0, \epsilon, t, c} [\| f_{\theta}(x_t, t, c) - v_t \|_2^2] $$

其中各变量含义为：
- $x_0$：干净的运动序列数据
- $\epsilon$：标准高斯噪声
- $t$：时间步，控制噪声与数据的混合比例
- $c$：条件信号（文本嵌入或视频运动 token）
- $f_{\theta}$：参数为 $\theta$ 的速度场预测网络（DiT 骨干）
- $v_t$：最优传输路径下的真实速度场

前向扩散过程采用整流流（Rectified Flow）的线性插值方式：

$$ x_t = (1 - t) \epsilon + t x_0 $$

对应的速度场定义为干净运动与噪声之差：

$$ v_t = x_0 - \epsilon $$

该框架的优势在于训练路径为最优传输，理论上收敛更快、采样步数更少，适合运动生成这类高维连续信号建模任务。

### 双分支门控融合架构

ViMoGen 的核心创新在于**门控双分支跨模态融合机制**。每个融合块（Fusion Block）包含两个互斥激活的条件生成分支：

- **T2M 分支（Text-to-Motion）**：以文本嵌入为条件，通过交叉注意力注入光学 MoCap 数据的运动先验，保证生成运动的物理合理性与运动质量。
- **M2M 分支（Motion-to-Motion）**：以离线 ViGen 视频生成模型提取的视频运动 token 为条件，引入视频生成模型在大规模数据中习得的丰富语义泛化知识。

两个分支通过**自适应门控模块（Adaptive Gating Module）**进行选择，每个块内同时仅激活一个分支。门控决策基于两个机制：
1. **VLM 对齐检查**：评估视频运动 token 与文本提示的语义一致性，若对齐质量高则优先选择 M2M 分支以利用其泛化能力。
2. **数据质量课程策略（Curriculum）**：对于人工标注的高质量数据集，优先激活 T2M 分支以充分利用精确的运动先验；对于大规模自动标注数据，鼓励更广泛地使用 M2M 分支以引入语义多样性。

当 M2M 分支被激活时，系统对真实运动数据施加**复合噪声策略**（随机扰动、抖动模拟、时序丢弃），以模拟视觉 MoCap 管线从生成视频中提取运动 token 时引入的伪影，使模型在训练阶段即学会校正这些误差。

### 视频运动先验提取管线

ViMoGen 的视频语义先验并非端到端在线生成，而是通过离线管线提取：
1. **视频生成**：利用预训练的 ViGen 模型（Wan2.1）根据文本提示生成参考视频。
2. **视觉 MoCap**：通过 CameraHMR 和 SMPLest-X 从生成视频中逐帧提取 3D 人体运动，转换为 SMPL-X 表征。
3. **运动 token 化**：将提取的运动序列编码为固定维度的 token，作为 M2M 分支的条件输入。

该设计将视频模型的泛化能力“蒸馏”为运动 token，避免了推理时实时调用视频生成模型的需求（ViMoGen-light 则进一步通过知识蒸馏完全移除该依赖）。

### ViMoGen-light 知识蒸馏

ViMoGen-light 是 ViMoGen 的轻量蒸馏变体。教师模型（完整 ViMoGen）首先生成约 14k 个合成运动-文本对，覆盖长尾语义场景；学生模型仅保留 T2M 分支结构，在这些合成数据上进行训练，从而在不依赖任何视频生成模型的情况下保留泛化能力。



## 实验与关键发现

### 4.1 评估基准与协议

**MBench 基准设计动机**：现有文本到运动（T2M）评估主要依赖 HumanML3D 等数据集，其动词分布高度倾斜于日常室内动作（如“走”“站”“坐”），无法有效衡量模型在长尾、复杂语义场景下的泛化能力。为此，本文构建了 **MBench**，一个覆盖九大评估维度的综合基准，包括运动质量（时序质量、帧级质量）、提示遵循度（动作准确度、运动条件一致性）和泛化能力（见 **Figure 3**）。MBench 的提示设计在动词分布上显著区别于 HumanML3D，包含武术、动态运动、多步骤行为等挑战性场景。

**评估可靠性验证**：MBench 的自动评估指标与人类偏好呈显著正相关。如 **Figure 6** 所示，在多个评估维度上，自动评估胜率与人类标注胜率之间的 Spearman 相关系数（ρ）均表现良好，验证了 MBench 作为自动评估代理的可靠性（部分维度如脚部浮动相关性较弱，需注意）。

**对比基线**：实验覆盖了当前主流 T2M 方法，包括 **MDM**（Tevet et al., 2023）、**T2M-GPT**（Zhang et al., 2023a）、**MoMask**（Guo et al., 2024）、**MotionLCM**（Dai et al., 2024）、**MotionDiffuse**（Zhang et al., 2024b）、**FineMoGen**（Zhang et al., 2023d）和 **MotionCraft**（Bian et al., 2025）。所有模型在相同渲染环境和统一提示集下评估，确保比较公平性。

### 4.2 主实验结果

#### 4.2.1 MBench 泛化性评估

**Table 2** 展示了 MBench 上的核心定量结果。**ViMoGen（完整版）在 Motion Generalizability 上达到 0.68，远超最强基线 MotionLCM 的 0.55（+0.13），在 Motion Condition Consistency 上也以 0.53 领先于 MotionLCM 的 0.48（+0.05）。** 这一结果表明，引入视频生成模型的语义先验并通过门控双分支架构进行融合，能够显著突破现有模型在长尾语义指令上的泛化瓶颈。

**ViMoGen-light（蒸馏版）** 在 MBench 上取得了 0.55 的 Generalizability 得分，与最强基线 MotionLCM 持平，且 Motion Condition Consistency 达到 0.47，接近完整版 ViMoGen。值得强调的是，ViMoGen-light **在推理时完全不依赖视频生成模型**，却保留了教师模型的大部分泛化能力，验证了知识蒸馏策略的有效性。

**Figure 4** 的定性对比进一步印证了上述结论：对于包含“武术”“动态运动”等关键词的复杂提示，ViMoGen 生成的动作品质和文本对齐度明显优于基线方法（更多定性示例见 **Figure 13**）。

#### 4.2.2 HumanML3D 标准基准

**Table 8** 报告了 HumanML3D 测试集上的结果。**MLD + ViMoGen-light 在 R Precision Top-1 上达到 0.542，超过此前最佳的 MoMask（0.521），同时 FID 从 MLD 基线的 0.473 大幅降至 0.114。** 这表明 ViMoGen-light 不仅在泛化性上具有竞争力，在标准分布内的文本-运动一致性上也达到了 SOTA 水平。该结果同时说明，蒸馏过程并未牺牲模型在常规场景下的生成质量。

### 4.3 消融实验

#### 4.3.1 分支选择策略

**Table 3** 对比了不同的分支激活策略。结果显示：
- **T2M-only**：Generalizability 为 0.54，Condition Consistency 为 0.39
- **M2M-only**：Generalizability 为 0.59，Condition Consistency 为 0.38
- **Adaptive Gating（本文方法）**：Generalizability 达到 **0.68**，Condition Consistency 达到 **0.53**

自适应门控在泛化性和一致性上均显著优于单一分支。这表明 T2M 分支（依赖 MoCap 先验保证运动质量）和 M2M 分支（引入 ViGen 语义知识）之间存在互补关系，门控机制能够根据输入提示和数据质量动态选择最优路径。**Figure 11** 提供了自适应分支选择的定性示例，展示了模型如何在 M2M 和 T2M 之间智能切换。

#### 4.3.2 训练数据组成

**Table 5** 逐步添加数据源的消融实验揭示了各数据成分的贡献：
- 仅使用光学 MoCap 数据时，Generalizability 为 0.44
- 添加野生视频数据后，提升至 0.52
- **进一步添加合成视频数据后，Generalizability 跃升至 0.55，带来最大的单一增益**

这说明合成视频数据在覆盖长尾语义方面发挥了关键作用，而 ViMoGen-228K 的多源数据策略（228,236 个片段，369.4 小时，见 **Table 1**）是模型泛化能力的基础保障。

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/003_Table_1.jpg]]
*Table 1: Comparison of ViMoGen-228K with existing human motion datasets. †Unified 29 datasets. ‡Aggressively filtered from 10M clips. #Strategically generated for semantic coverage*

#### 4.3.3 文本编码器选择

**Table 6** 对比了三种文本编码器：
- **CLIP**：Generalizability 0.35，运动质量较高但泛化性受限
- **MLLM**：Generalizability 0.46，泛化性最高但运动质量下降
- **T5-XXL**：Generalizability 0.44，在泛化性与运动质量之间取得最佳平衡

本文最终选择 T5-XXL 作为文本编码器，因其在保持运动物理合理性的同时提供了足够的语义理解深度。

#### 4.3.4 文本提示风格

**Table 4** 和 **Figure 12** 分析了训练与测试时文本风格的影响。结果表明，**使用描述性视频风格文本训练、在简洁运动风格文本上测试**，可获得最佳的 Motion Condition Consistency（0.43）。这验证了视频生成模型引入的丰富语义描述有助于模型学习更鲁棒的文本-运动映射，即使在测试时面对简短的指令也能生成高质量动作。

#### 4.3.5 双分支联合训练的必要性

**Table 7** 的双分支互惠分析表明，本文的联合训练方法在一致性和泛化性上均显著优于将 MotionLCM 或 DNO 等现成方法作为 M2M 分支的简单组合方案。这证明 ViMoGen 的门控融合架构并非简单的集成，而是通过联合优化实现了两个分支之间更深层的知识迁移。

### 4.4 失败模式与局限性

尽管 ViMoGen 在泛化性上取得了显著突破，但仍存在以下已知局限：

1. **推理计算开销**：完整版 ViMoGen 依赖外部视频生成模型（Wan2.1），增加了推理延迟和计算成本。ViMoGen-light 通过蒸馏解决了这一问题，但可能无法覆盖所有长尾语义场景。
2. **视觉 MoCap 伪影**：CameraHMR 和 SMPLest-X 组成的视觉 MoCap 管线可能引入足部滑动等伪影，且生成视频的动态范围有限，影响高动态运动（如空翻、快速旋转）的保真度。MBench 的脚部接触指标与人类判断相关性较弱，也反映了这一评估维度的挑战。
3. **单人运动限制**：当前框架仅支持单人运动生成，尚未扩展到多人交互场景，这是未来工作的重要方向。
4. **蒸馏数据覆盖**：ViMoGen-light 的蒸馏过程依赖教师模型生成的 14k 合成提示，可能无法完全覆盖现实世界中的极端长尾语义。

### 4.5 关键图表索引

| 图表 | 核心结论 |
|------|---------|
| **Table 2** | ViMoGen 在 MBench Generalizability 上达到 0.68，领先最强基线 +0.13 |
| **Table 3** | 自适应门控显著优于 T2M-only 和 M2M-only |
| **Table 5** | 合成视频数据带来最大泛化增益（+0.11） |
| **Table 8** | MLD+ViMoGen-light 在 HumanML3D 上达到 SOTA |
| **Figure 6** | MBench 自动评估与人类偏好呈显著正相关 |
| **Figure 11** | 自适应分支选择的定性示例 |

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on MBench. The best performance is bolded*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/007_Table_3.jpg]]
*Table 3: Ablation study on different branch selection strategies for ViMoGen. Our adaptive method significantly outperforms single-branch baselines in generalization and accuracy*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/009_Table_5.jpg]]
*Table 5: Ablation on the composition of the training data. Adding diverse data sources progressively improves generalization, with synthetic data providing the largest gains*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/017_Table_8.jpg]]
*Table 8: Quantitative evaluation on the HumanML3D test set. ± indicates a 95% confidence interval during 20 times repeating evaluations. Bold indicates the best result*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/013_Figure_6.jpg]]
*Figure 6: MBench’s Human Alignment. In each plot, a dot represents the human preference win ratio (horizontal axis) and MBench automatic evaluation win ratio (vertical axis) for a motion generation model. We linearly fit a straight line to visualize the correlation and calculate the Spearman’s correlation coefficient (ρ) for each dimension*

### 补充图表

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/010_Table_6.jpg]]
*Table 6: Ablation on the choice of text encoder. Compared to CLIP (Radford et al., 2021) and MLLM (Kong et al., 2024), T5-XXL (Raffel et al., 2020) provides the best balance of generalization and motion quality*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/008_Table_4.jpg]]
*Table 4: Ablation on text prompt style. Training with descriptive video-style text and testing on concise motion-style text yields the best overall performance*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/011_Table_7.jpg]]
*Table 7: Analysis of mutual benefits between T2M and M2M branches. We compare our joint training approach against baselines using MotionLCM (Dai et al., 2024) and DNO (Karunratanakul et al., 2024)*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/005_Figure_3.jpg]]
*Figure 3: Overview of MBench. (a) MBench features more balanced distribution and vastly different prompt designs compared to HumanML3D. (b) MBench designed is to systematically evaluate motion generation algorithms across nine dimensions, focusing on motion quality, prompt-following, and generalization capability*

![[assets/figures/papers/paper_list_l1906_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation/figures/015_Figure_8.jpg]]
*Figure 8: Comprehensive Data Preprocess Pipeline. The pipeline is organized into sequential modules, utilizing a central database to aggregate metadata like scores, keypoints, captions, and text masks*



## 定位与知识库关联

### 1. 技术路径与基线关系

ViMoGen 处于文本驱动三维人体运动生成这一研究脉络中，其核心突破在于将**视频生成模型的开放语义先验**系统性地引入扩散运动生成框架。该工作直接对标并显著超越了一系列代表性基线：

- **扩散模型基线**：**MDM** (Tevet et al., 2023)、**MotionDiffuse** (Zhang et al., 2024b) 和 **MotionLCM** (Dai et al., 2024) 代表了基于扩散的运动生成主流方案。ViMoGen 在 MBench 的 Motion Generalizability 上达到 0.68，远超 MotionLCM 的 0.55（Table 2），揭示了单纯依赖文本条件与有限运动数据训练的扩散模型在长尾语义覆盖上的根本性瓶颈。
- **自回归与离散标记基线**：**T2M-GPT** (Zhang et al., 2023a) 和 **MoMask** (Guo et al., 2024) 采用 VQ-VAE 与自回归生成范式。ViMoGen-light 在 HumanML3D 上以 R Precision Top-1 0.542 超越 MoMask 的 0.521（Table 8），同时 FID 显著优于基线（0.114 vs 0.473），表明蒸馏后的视频语义先验即使在标准域内评估中也能提升文本-运动对齐精度。
- **精细化生成基线**：**FineMoGen** (Zhang et al., 2023d) 和 **MotionCraft** (Bian et al., 2025) 侧重于细粒度控制或编辑。ViMoGen 的差异化优势在于从根本上扩展了可生成语义的边界，而非在已有语义空间内进行更精细的操控。

### 2. 关键设计决策与知识贡献

ViMoGen 的方法论贡献可分解为三个相互协同的层面，每个层面均对应明确的知识定位：

**（1）视频语义先验的迁移机制（知识源创新）**
传统文本到运动模型的知识来源局限于 CLIP 等文本-图像对比编码器。ViMoGen 首次将 **ViGen 视频生成模型**（Wan2.1）作为语义先验的替代来源。其核心洞察在于：视频生成模型在海量视频数据上学习到的物理世界动态规律和开放语义理解能力，可以通过“文本→视频→运动标记”的路径迁移至运动生成。这一思路将运动生成的知识边界从人工标注的运动-文本对（约 15K 规模）扩展至视频生成模型所蕴含的互联网级视觉知识。

**（2）门控双分支融合架构（融合机制创新）**
面对视频先验（高泛化性但可能含伪影）与光学 MoCap 先验（高保真但语义受限）的质量-泛化权衡，ViMoGen 设计了**自适应门控双分支 DiT 架构**：
- **T2M 分支**：基于文本嵌入的条件生成，利用高质量 MoCap 先验保证运动物理合理性。
- **M2M 分支**：基于视频运动标记的条件生成，引入 ViGen 的语义泛化知识。
- **自适应门控模块**：通过 VLM 对齐检查和数据质量课程，在推理时动态选择激活分支。

消融实验（Table 3）提供了决定性证据：自适应门控在 Motion Generalizability 上达到 0.68，显著优于 T2M-only（0.54）和 M2M-only（0.59）。这证明了简单的先验叠加或固定融合策略无法有效解决质量-泛化权衡，而数据驱动的自适应分支选择是关键的因果调节变量。

**（3）大规模多源数据集与蒸馏策略（规模扩展路径）**
ViMoGen-228K 数据集（Table 1）将训练数据从 HumanML3D 的 14,616 个片段扩展至 228,236 个片段（约 15.6 倍），涵盖光学 MoCap、野生视频和合成视频三类来源。数据组成消融（Table 5）揭示了清晰的扩展规律：逐步添加合成视频数据带来最大的泛化增益（Motion Generalizability 从 0.44 提升至 0.55），验证了合成数据在覆盖长尾语义方面的独特价值。

ViMoGen-light 通过知识蒸馏（教师模型生成 14K 合成提示并训练学生模型）移除了对视频生成模型的推理依赖，在 MBench 上 Generalizability 得分 0.55，与最强基线持平（Table 2）。这提供了一条实用的部署路径：在训练阶段利用昂贵的视频先验进行知识迁移，在推理阶段仅保留文本条件生成能力。

### 3. 适用边界与局限

尽管 ViMoGen 在泛化性上取得了显著突破，其适用边界和局限同样明确：

- **推理计算开销**：完整 ViMoGen 模型在推理时依赖外部视频生成模型（ViGen），增加了显著的计算开销。这一依赖限制了其在实时或资源受限场景下的直接部署。ViMoGen-light 通过蒸馏解决了此问题，但以部分泛化性能为代价（Generalizability 从 0.68 降至 0.55）。
- **视觉 MoCap 管线伪影**：CameraHMR 和 SMPLest-X 构成的视觉 MoCap 管线可能引入足部滑动等伪影，且生成视频的动态范围有限（如高动态运动中的运动模糊），影响高保真运动生成的物理合理性。M2M 分支训练时采用的复合噪声策略（随机损坏、抖动模拟、时序丢弃）是对此问题的工程缓解，但未从根本上解决视觉 MoCap 的质量上限。
- **单人运动限制**：当前框架仅支持单人运动生成，尚未扩展到多人交互场景。这是架构层面的固有限制，因为 SMPL-X 表示和 DiT 骨干均未建模多人空间关系与交互约束。
- **蒸馏覆盖局限**：ViMoGen-light 的蒸馏过程依赖于教师模型生成的 14K 合成提示，可能无法覆盖所有长尾语义场景，特别是那些视频生成模型本身也难以准确合成的极端动态或罕见动作类别。

### 4. 开放问题与后续方向

从 ViMoGen 的设计逻辑和实验边界出发，可识别以下开放问题：

- **多人运动生成扩展**：如何将门控双分支架构和视频语义先验迁移机制扩展到多人交互场景？这需要解决多人 SMPL-X 参数化、空间穿透约束和交互语义建模等新挑战。
- **视频先验失真的鲁棒校正**：当视频生成模型产生的视觉 MoCap 数据存在显著失真（如高动态运动中的姿态估计失败）时，如何更有效地检测并校正？当前的自适应门控机制仅在分支级别进行选择，缺乏对 M2M 分支内部错误标记的细粒度修正能力。
- **视觉 MoCap 伪影的系统性消除**：足部滑动、运动模糊导致的姿态抖动等伪影能否通过改进的视觉 MoCap 管线（如融合物理约束的优化后处理）或生成视频的动态范围增强来系统性缓解？
- **弱标注数据的有效利用**：ViMoGen-228K 的构建依赖 Gemini 2.0 进行自动标注，产生了大量弱标注数据。如何设计预训练策略（如掩码运动建模或对比学习）更高效地利用这些数据，减少对高质量人工标注的依赖？
- **评估维度的细化**：MBench 虽然经过人类对齐验证（Figure 6，Spearman ρ 显著正相关），但某些维度（如脚部浮动）上自动指标与人类偏好的相关性较弱。这提示需要更精确的物理合理性自动评估指标，以支撑未来方法在该方向上的可靠迭代。



## 原文 PDF

![[paperPDFs/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation.pdf]]

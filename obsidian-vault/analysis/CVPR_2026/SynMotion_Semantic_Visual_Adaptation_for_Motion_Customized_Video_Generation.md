---
title: "SynMotion: Semantic-Visual Adaptation for Motion Customized Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SynMotion_Semantic_Visual_Adaptation_for_Motion_Customized_Video_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Tan_SynMotion_Semantic-Visual_Adaptation_for_Motion_Customized_Video_Generation_CVPR_2026_paper.html
project_link: https://lucariaacademy.github.io/SynMotion/
code_link: null
aliases:
- SynMotion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过提示感知的双嵌入分解显式解耦主体与运动语义，并引入参数高效的运动适配器提升时序一致性；同时利用嵌入特定交替训练策略防止主体与运动语义干扰。
primary_logic: 有效运动定制需联合语义理解（解耦的主体-运动嵌入）与视觉适应（运动适配器），并通过嵌入特定训练维持主体泛化能力。
claims:
- SynMotion jointly leverages semantic guidance and visual adaptation.
- Dual-embedding mechanism decomposes LLM embeddings into subject and motion components.
- Parameter-efficient motion adapters enhance motion fidelity and temporal coherence.
- Embedding-specific training alternately optimizes subject and motion embeddings to prevent interference.
---

# SynMotion: Semantic-Visual Adaptation for Motion Customized Video Generation

> [!tip] 核心洞察
> 有效运动定制需联合语义理解（解耦的主体-运动嵌入）与视觉适应（运动适配器），并通过嵌入特定训练维持主体泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SynMotion：面向运动定制视频生成的语义-视觉自适应 |
| 英文题名 | SynMotion: Semantic-Visual Adaptation for Motion Customized Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tan_SynMotion_Semantic-Visual_Adaptation_for_Motion_Customized_Video_Generation_CVPR_2026_paper.html) · [Project](https://lucariaacademy.github.io/SynMotion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | SynMotion |
| Dataset | MotionBench, MotionBench (T2V) - User Study |

> [!tip] 效果简介
> - MotionBench (T2V) 上，Motion Accuracy (VQA) 68.60% vs best competitor (outperforms all compared methods (see Table 1))；Subject Accuracy 97.67% vs best competitor (outperforms all compared methods)；Imaging Dynamic Background Consistency 97.59% vs best competitor (outperforms all compared methods)。
> - MotionBench (T2V) - User Study 上，Motion Alignment 78.3% ± 1.34 vs other methods (preference rate over competitors)；Subject Alignment 81.9% ± 2.41 vs other methods (preference rate)；Video Quality 83.9% ± 3.25 vs other methods (preference rate)。

## 概要

**问题瓶颈**：现有运动定制视频生成方法多依赖单一语义层级（如文本反演）或单一视觉层级（如运动向量迁移）建模，导致运动表达不完整、主体泛化能力差，难以同时保证运动逼真度与主体多样性。

**核心洞察**：有效的运动定制需要**语义理解**与**视觉适应**的联合作用——在语义层面显式解耦主体与运动嵌入，在视觉层面注入运动感知适配器，并通过嵌入特定的交替训练策略防止两者相互干扰。

**方法定位**：SynMotion 在冻结的 HunyuanVideo MM-DiT 视频生成主干上，引入三个关键模块：（1）提示感知的**双嵌入分解**，将 MLLM 文本嵌入分离为主体嵌入与运动嵌入，并通过 Zero-Conv 附加可学习残差；（2）轻量级低秩**运动适配器**，注入 MM-DiT 各注意力层以增强时序一致性；（3）**嵌入特定交替训练策略**，以概率 α 联合优化运动与主体嵌入，以概率 1−α 仅优化主体嵌入，维持主体泛化能力。

**主要结果**：在 MotionBench 基准上，SynMotion 在运动准确性（68.60%）、主体准确性（97.67%）、动态背景一致性（97.59%）、CLIP-T（0.322）和 FVD（212.05）等指标上均超越所有对比方法，用户调研中运动对齐、主体对齐和视频质量偏好率分别达 78.3%、81.9% 和 83.9%。消融实验表明，双嵌入分解、运动适配器和交替训练策略均为关键贡献组件。

> **待验证**：代码与模型权重尚未公开；大规模罕见动作上的扩展性、多动作组合定制能力及在其他视频生成基座上的迁移效果仍需进一步探索。

### 视频运动定制：从主体泛化到运动迁移

给定少量展示特定运动模式的示例视频，运动定制（Motion Customization）要求生成模型将该运动迁移至任意新主体，同时保持主体的视觉特征与运动的时间一致性。这一任务的核心挑战在于：模型必须同时理解“谁在动”与“怎么动”，并将两者在生成过程中解耦控制。

现有方法大致沿两条技术路线展开。**视觉层级方法**（如 **DMT** (Yatim et al., CVPR 2024)、**Motion Director** (Zhao et al., ECCV 2024)、**Motion Inversion** (Wang et al., arXiv 2024) 等）直接对视频潜空间或注意力特征进行操作，在运动保真度上表现较好，但往往以牺牲主体泛化能力为代价——当目标主体与示例视频中的主体差异较大时，生成质量显著下降。**语义层级方法**（如将 Textual Inversion、DreamBooth 等图像定制范式迁移至视频，或 **ReVersion** (Huang et al., ICCV 2023) 的关系反演策略）通过学习文本嵌入来编码运动概念，主体泛化能力较强，但单一语义嵌入难以精确刻画复杂的时空运动模式，导致运动表达不够完整。

### 瓶颈：单一层级建模的固有张力

上述两条路线的各自局限揭示了一个深层瓶颈：**运动逼真度与主体多样性之间存在固有张力**。纯视觉方法缺乏对主体语义的显式建模，运动特征容易与示例视频中的主体外观耦合；纯语义方法则将运动压缩为单一的文本嵌入，丢失了细粒度的时空动态信息。此外，当同时学习主体嵌入与运动嵌入时，两者在优化过程中会相互干扰——运动嵌入可能“记住”示例视频中的主体外观，而主体嵌入可能被运动信号污染，最终导致泛化失败。

### 本文动机：语义-视觉协同定制

针对上述瓶颈，本文提出 **SynMotion**，其核心动机是：有效的运动定制需要**语义理解**与**视觉适应**的协同作用。语义层面负责将主体与运动显式解耦，视觉层面负责增强运动特征的时间一致性建模，两者通过专门设计的训练策略防止相互干扰。这一思路将运动定制从单一层级的“特征注入”或“嵌入学习”范式，推进到语义-视觉联合自适应的新框架。

## 核心方法与创新机理

SynMotion 的核心创新在于将运动定制的瓶颈从单一层级建模推向**语义-视觉联合自适应**。现有方法要么在语义空间学习运动表征（如 Textual Inversion、DreamBooth 的视频改编版），要么在视觉层级注入运动先验（如 **VMC**、**DMT** (Yatim et al., CVPR 2024)、**Motion Director** (Zhao et al., ECCV 2024)），但前者难以保证运动逼真度，后者则牺牲了主体泛化能力。SynMotion 的关键洞察是：有效的运动定制需要同时控制“什么在动”（主体语义）和“怎么动”（运动视觉），且二者必须解耦学习以避免相互干扰。

为实现这一目标，SynMotion 在三个关键槽位上相对于基线做出了根本性改变：

**1. 文本嵌入分解：从单一嵌入到提示感知的双嵌入**

基线方法通常将整个 `<subject, motion>` 提示编码为单一的 LLM 文本嵌入，主体与运动语义混杂在一起。SynMotion 引入**提示感知的双嵌入分解**，将 MLLM 编码器输出的文本嵌入显式拆分为主体嵌入 $e_{sub}$ 和运动嵌入 $e_{mot}$ 两个组件。在此基础上，每个嵌入分量通过 Zero-Conv 层 $\mathcal{Z}$ 附加可学习的残差嵌入 $e_{sub}^l$ 和 $e_{mot}^l$，形成增强嵌入 $e_{sub} + \mathcal{Z}(e_{sub}^l)$ 和 $e_{mot} + \mathcal{Z}(e_{mot}^l)$。这种设计使得模型可以在不破坏预训练语义空间的前提下，仅学习运动定制所需的最小残差。随后，一个**嵌入精炼器 $\mathcal{R}$** 对拼接后的嵌入 $e$ 进行语义交互融合，并通过二次 Zero-Conv 注入得到最终的条件嵌入 $e' = e + \mathcal{Z}(\mathcal{R}(e))$。这一机制从结构上解耦了主体身份与运动模式，为后续的独立优化奠定了基础。

**2. 运动建模模块：从冻结主干到注入运动感知适配器**

预训练视频生成模型（如 HunyuanVideo 的 MM-DiT）并未针对运动定制进行专门设计，直接在其上进行嵌入学习难以充分捕获时序运动特征。SynMotion 在 MM-DiT 的每个注意力层注入**轻量级运动感知低秩适配器 $A$**，以低秩残差方式增强模型对运动模式的建模能力。这些适配器参数量极小，但直接作用于扩散去噪过程的关键计算路径，显著提升了运动逼真度和时序一致性。与仅依赖文本嵌入的语义层级方法相比，适配器在视觉特征空间提供了互补的运动约束。

**3. 训练策略：从端到端优化到嵌入特定交替训练**

直接对所有可学习参数进行端到端优化会导致主体与运动嵌入相互干扰——模型倾向于将主体外观信息泄漏到运动嵌入中，从而损害主体泛化能力。SynMotion 提出**嵌入特定交替训练策略**：在每个训练步，以概率 $\alpha = 0.75$ 采样真实用户提供的示例视频，联合优化运动嵌入和主体嵌入；以概率 $1 - \alpha = 0.25$ 采样**主体先验视频（SPV）**——即同一主体执行无关动作的合成视频——并冻结运动嵌入，仅优化主体嵌入。SPV 阶段的正则化迫使主体嵌入学习与运动无关的主体特征，而运动嵌入则仅在真实示例阶段吸收运动信息。这种交替机制从训练动力学层面实现了主体与运动的彻底解耦。

三个创新槽位形成因果闭环：双嵌入分解提供了可独立操作的语义表示空间，运动适配器在视觉层级补足了语义嵌入无法覆盖的时序细节，而嵌入特定训练策略则确保了两个空间的学习过程互不污染。消融实验（Figure 5）验证了每个组件的必要性——移除任一项均导致运动定制效果的显著退化。

SynMotion 的整体流程围绕“语义引导 + 视觉适应”双通道展开，目标是在冻结的视频生成主干上，仅通过少量示例视频即可将特定运动模式迁移到任意新主体上。图 2 给出了完整的 pipeline 示意。

**输入与文本编码**  
给定一个 `<subject, motion>` 形式的提示，首先利用多模态大语言模型（MLLM）提取其语义表示，得到单一的文本嵌入。该嵌入随后进入提示感知的双嵌入分解阶段，被显式拆分为主体嵌入 $e_{sub}$ 和运动嵌入 $e_{mot}$ 两个分量。在此基础上，通过 Zero-Conv 层 $\mathcal{Z}$ 附加可学习的残差嵌入 $e_{sub}^l$ 和 $e_{mot}^l$，形成增强后的嵌入表示：

$$e = [ e_{mot} + \mathcal{Z}(e_{mot}^l),\; e_{sub} + \mathcal{Z}(e_{sub}^l) ]$$

**嵌入精炼与语义交互**  
增强后的嵌入 $e$ 送入嵌入精炼器 $\mathcal{R}$，促进主体与运动语义在潜在空间的交互融合。精炼结果再次通过 Zero-Conv 注入，得到最终的条件嵌入 $e'$：

$$e' = e + \mathcal{Z}(\mathcal{R}(e))$$

这一设计使模型既能保留预训练文本编码器的基座语义，又能灵活学习定制化的运动-主体联合表示。

**视觉适应与运动适配器**  
在视觉层面，SynMotion 在冻结的 HunyuanVideo MM-DiT 去噪网络中注入轻量级运动感知适配器 $\mathcal{A}$。这些适配器以低秩残差形式嵌入 MM-DiT 的每个注意力层，专门增强运动特征的建模能力与时序一致性，而不破坏预训练主干的泛化性能。

**训练调度与解耦策略**  
训练时采用嵌入特定交替训练策略（图 2(b)）。每一步以概率 $\alpha$ 采样真实用户提供的示例视频，联合优化可学习的运动嵌入和主体嵌入；以概率 $1-\alpha$ 采样主体先验视频（SPV），此时冻结运动嵌入，仅优化主体嵌入。这种调度机制有效防止主体与运动语义在嵌入空间中的相互干扰，是维持主体泛化能力的关键设计。论文中 $\alpha$ 取 0.75。

**生成流程**  
推理时，用户只需提供少量示例视频和新的主体提示，MLLM 编码后经双嵌入分解与精炼器融合，条件嵌入 $e'$ 与运动适配器协同引导冻结的 MM-DiT 完成视频去噪生成。整个过程中，视频生成主干保持冻结，仅需训练轻量的嵌入残差、精炼器和运动适配器，参数高效且收敛迅速。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_SynMotion_Semantic/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of SynMotion. Given a prompt in the form of \< subject, motion >, we use a MLLM to obtain the corresponding text embedding, which is then decomposed into a subject embedding*

SynMotion 的核心设计围绕一个关键洞察展开：有效的运动定制必须同时依赖**语义层面的解耦理解**与**视觉层面的时序适应**。为此，方法在冻结的视频生成主干上引入三个紧密协作的模块：双嵌入语义理解、运动感知适配器，以及嵌入特定交替训练策略。以下逐一剖析其结构与作用机理。

### 双嵌入语义理解（Dual-Embedding Semantic Comprehension）

传统方法将文本提示编码为单一嵌入，导致主体与运动语义纠缠，难以在保持主体泛化能力的同时精确刻画运动。SynMotion 提出一种**提示感知的双嵌入分解**机制，将 MLLM 编码器输出的基础文本嵌入显式拆分为主体嵌入 $e_{sub}$ 和运动嵌入 $e_{mot}$ 两个分量。

为在保留预训练语义先验的前提下注入定制化信息，方法为每个分量附加一组可学习的残差嵌入 $e_{sub}^l$ 和 $e_{mot}^l$，并通过 **Zero-Conv** 层 $\mathcal{Z}(\cdot)$ 将其融合回原始嵌入：

$$e = [\,e_{mot} + \mathcal{Z}(e_{mot}^l),\; e_{sub} + \mathcal{Z}(e_{sub}^l)\,]$$

这一设计的精巧之处在于：Zero-Conv 初始化为零输出，训练初期完全依赖冻结的预训练嵌入，从而避免随机噪声破坏语义空间；随着训练推进，可学习残差逐步积累运动与主体的定制化信息。

为进一步促进主体与运动语义在潜在空间中的交互，方法引入一个轻量的**嵌入精炼器** $\mathcal{R}$（Embedding Refiner），对拼接后的嵌入 $e$ 进行融合，并再次通过 Zero-Conv 将精炼后的语义注入：

$$e' = e + \mathcal{Z}(\mathcal{R}(e))$$

最终得到的 $e'$ 作为条件嵌入送入后续的 MM-DiT 去噪网络。这一“分解—精炼—注入”的流程，构成了 SynMotion 语义层面的核心控制枢纽。

### 运动感知适配器（Motion-Aware Adapter）

仅靠语义层面的嵌入解耦，尚不足以确保生成视频的时序连贯性与运动逼真度。预训练视频生成模型（如 HunyuanVideo 的 MM-DiT）虽具备强大的视觉先验，但其注意力层并未针对特定运动模式进行优化。SynMotion 在 MM-DiT 的**每个注意力层**中注入轻量级的低秩运动适配器 $\mathcal{A}$，以参数高效的方式增强模型对运动特征的捕捉能力。

适配器以低秩残差的形式集成，仅引入极少量可训练参数，却显著提升了运动时序建模的精度。这一视觉适应路径与语义解耦路径形成互补：前者负责“如何动得逼真”，后者负责“动什么、谁在动”。

### 扩散损失函数

整个框架的训练仍遵循标准扩散去噪范式。给定编码后的潜变量 $z_t$、条件嵌入 $e_\theta$ 和时间步 $t$，MM-DiT 网络 $\epsilon_\theta$ 预测所加的噪声，目标函数为：

$$\mathcal{L} = \mathbb{E}_{\mathcal{E}(x),\,\epsilon \in \mathcal{N}(0,1),\,e_\theta,\,t}\left[\left\|\epsilon - \epsilon_\theta(z_t, e_\theta, t)\right\|_2^2\right]$$

其中 $e_\theta$ 即为前述经过双嵌入分解与精炼的文本条件嵌入。需要指出的是，该损失函数本身并未显式建模运动一致性——运动逼真度的提升完全来自运动适配器与双嵌入解耦带来的归纳偏置。

### 嵌入特定交替训练（Embedding-Specific Training Strategy）

上述模块的有效性高度依赖训练策略。若直接端到端优化所有可学习参数，主体嵌入与运动嵌入会相互干扰：运动示例视频中的主体信息可能污染运动嵌入，导致主体泛化能力下降。SynMotion 提出**嵌入特定交替训练**来解决这一瓶颈。

如图 2(b) 所示，在每个训练步：
- **以概率 $\alpha$**（设为 0.75）：采样用户提供的真实运动示例视频，**联合优化**运动嵌入与主体嵌入；
- **以概率 $1-\alpha$**：采样一个“主体先验视频”（Subject Prior Video, SPV），该视频中主体相同但运动无关，此时**冻结运动嵌入**，仅优化主体嵌入。

SPV 的引入起到了正则化作用：它迫使主体嵌入学习到与运动无关的主体表征，从而防止运动嵌入被主体信息“污染”。这一策略是 SynMotion 实现“运动精准、主体多样”的关键机制。

## 实验与关键发现

### 主实验结果

我们在 MotionBench 基准上对 SynMotion 与当前主流的运动定制方法进行了全面的定量与定性比较。MotionBench 共包含 26 个不同动作类别，每个动作提供 20 个真实示例视频用于训练。评测指标涵盖运动准确性（Motion Accuracy, VQA 评估）、主体准确性（Subject Accuracy）、动态背景一致性（Imaging Dynamic Background Consistency）、文本对齐度（CLIP T）以及视频质量（FVD 3DRN50），同时辅以用户调研。

**定量对比（Table 1）**：SynMotion 在所有自动评测指标上均取得最优结果。具体而言，运动准确性达到 **68.60%**，主体准确性为 **97.67%**，动态背景一致性为 **97.59%**，CLIP T 为 **0.322**，FVD 3DRN50 为 **212.05**。这些指标全面优于视觉层级方法（如 **DMT** (Yatim et al., CVPR 2024)、**Motion Director** (Zhao et al., ECCV 2024)、**Motion Inversion** (Wang et al., arXiv 2024)）和语义层级方法（如 **ReVersion** (Huang et al., ICCV 2023)），验证了语义-视觉联合建模的有效性。

**用户调研（Table 2）**：为进一步验证主观感知质量，我们进行了大规模用户调研。评估者从运动对齐度、主体对齐度和视频质量三个维度对生成结果进行偏好投票。SynMotion 分别获得了 **78.3% ± 1.34**、**81.9% ± 2.41** 和 **83.9% ± 3.25** 的偏好率，显著高于所有对比方法，表明用户在运动逼真度、主体保真度和整体视觉质量上均更认可 SynMotion 的生成效果。

**定性对比**：Figure 3 展示了与视觉层级方法的定性比较。现有视觉方法往往难以在保持主体身份的同时精确复现目标运动，例如在“海狮游泳”场景中，基线方法容易丢失海狮的鳍状肢特征或产生运动伪影。Figure 4 则对比了语义层级方法，朴素地将词级别文本反演适配到视频生成时，常导致运动表达不完整或主体外观崩塌。相比之下，SynMotion 能够准确捕捉示例视频中的运动模式，并将其泛化到语义距离较远的主体（如兔子、海狮）上，在保持主体特征（如生成合适的鳍状肢）的同时维持时序一致性。

### 消融实验

为验证各核心组件的贡献，我们进行了系统的消融实验（Figure 5 展示了可视化结果）。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_SynMotion_Semantic/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of ablation study*

- **去除双嵌入学习**：将提示感知的双嵌入分解替换为单一文本嵌入时，模型无法有效解耦主体与运动语义，导致生成结果中运动模式与示例视频偏差增大，且主体泛化能力显著下降。
- **去除运动感知适配器**：移除注入 MM-DiT 注意力层的低秩运动适配器后，视频的时序连贯性明显减弱，运动流畅度下降，出现帧间跳变或不自然停顿。
- **去除嵌入特定训练策略**：取消以概率 α = 0.75 交替优化运动嵌入与主体嵌入的调度机制，改为端到端联合优化所有参数时，主体嵌入容易过拟合到示例视频中的特定外观，导致在新主体上的泛化能力严重退化。

消融结果表明，双嵌入分解、运动适配器和嵌入特定训练策略三者协同作用，缺一不可：语义解耦保障了运动与主体的分离学习，视觉适配增强了运动建模的时空精度，而交替训练则防止了主体嵌入的过拟合，维持了强泛化能力。

### 图像到视频泛化

我们将提出的双嵌入学习与运动感知适配器集成到图像到视频（I2V）生成框架中，以验证方法的跨任务泛化能力。Figure 6 展示了 I2V 设置下的生成结果：给定一张静态主体图像和目标运动描述，SynMotion 能够生成该主体执行指定动作的视频，且运动模式与 T2V 设置下学到的定制运动保持一致。这表明所提方法学到的运动表示具有任务无关的可迁移性。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_SynMotion_Semantic/figures/007_Figure_6.jpg]]
*Figure 6: The results of our method generalized on Image-to-Video task*

### 失败模式与局限

尽管 SynMotion 在运动定制的准确性和主体泛化方面取得了显著进展，论文中未明确讨论具体的失败案例。根据方法设计可推断的潜在局限包括：（1）训练过程中超参数 α 的选择（当前设为 0.75）是否在更广泛的运动类别上具有普适性，需进一步验证；（2）每个动作类别仅使用 20 个示例视频，对于极端罕见或高度复杂的动作序列，该数据量是否足以学习到完整的运动表示，尚待考察；（3）方法目前聚焦于单动作定制，是否支持多动作组合或复杂动作序列的定制，论文未涉及。此外，代码与模型权重尚未公开，开源时间未知，方法的可复现性和社区验证有待推进。

> **注意**：上述失败模式与局限部分基于方法设计的合理推断，论文原文未提供具体的失败案例分析，建议在正式发表后结合补充材料进行人工核验。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_SynMotion_Semantic/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons with state-of-the-art motion customization methods*

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_SynMotion_Semantic/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparisons with state-of-the-art semantic-level methods*

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Tan_SynMotion_Semantic/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison results. The best results for each column are bold*

## 定位与知识库关联

### 1. 运动定制视频生成的基线谱系

运动定制视频生成旨在从少量示例视频中提取特定运动模式，并将其迁移至新主体。现有方法可划分为两大技术路线：

**视觉层级方法** 直接在像素或潜在空间建模运动，代表性工作包括：
- **VMC**：通过视觉特征匹配实现运动迁移，但对主体外观保持较弱。
- **DMT**（Yatim et al., CVPR 2024）：利用解耦运动表征进行定制，在运动保真度上有所提升，但主体泛化仍受限。
- **Motion Director**（Zhao et al., ECCV 2024）：引入运动引导机制，但依赖较强的运动先验假设。
- **Motion Inversion**（Wang et al., arXiv 2024）：通过反演方式捕获运动，计算开销较大。
- **MotionClone**：免训练的运动克隆方法，灵活性高但运动精度不足。

**语义层级方法** 将文本反演等技术从图像域迁移至视频域，代表性工作包括：
- **Textual Inversion**：将运动概念编码为伪词嵌入，但在视频生成中时序一致性差。
- **DreamBooth**：通过微调扩散模型实现主体定制，迁移至运动定制时易导致主体-运动纠缠。
- **ReVersion**（Huang et al., ICCV 2023）：利用关系反演捕获视觉概念，对复杂运动的表达能力有限。

上述方法的核心瓶颈在于：单一层级建模无法同时保证运动逼真度与主体多样性——视觉方法易丢失主体语义，语义方法难以维持时序连贯的运动表达。

### 2. SynMotion 的方法定位与改进机制

SynMotion 在谱系中占据**语义-视觉联合自适应**的独特位置，通过三个关键改进突破上述瓶颈：

| 改进维度 | 基线做法 | SynMotion 方案 | 因果机制 |
|---------|---------|---------------|---------|
| 文本嵌入 | 单一 LLM 嵌入，无显式分解 | 提示感知的双嵌入分解为 $e_{sub}$ 和 $e_{mot}$，并通过 Zero-Conv 附加可学习残差 | 解耦主体与运动语义，防止概念纠缠 |
| 运动建模 | 预训练模型无额外运动模块 | 在 MM-DiT 每个注意力层注入低秩运动适配器 $\mathcal{A}$ | 增强时序运动特征建模，提升运动保真度 |
| 训练策略 | 端到端优化所有参数 | 嵌入特定交替训练：以 $\alpha=0.75$ 概率联合优化，$1-\alpha$ 概率冻结运动嵌入仅优化主体嵌入 | 防止主体与运动语义相互干扰，维持主体泛化能力 |

SynMotion 并非简单叠加语义与视觉模块，而是通过**嵌入特定训练调度器**实现两者的协同学习：当采样真实示例视频时，运动与主体嵌入联合优化；当采样主体先验视频（SPV）时，冻结运动嵌入以正则化主体嵌入，确保主体语义不被运动噪声污染。

### 3. 知识库定位与适用边界

**适用场景**：
- 给定 20 个左右示例视频的少样本运动定制
- 支持文生视频（T2V）和图像到视频（I2V）两种生成范式
- 可处理 26 类动作（MotionBench 覆盖范围），包括人体动作、动物运动等

**已知局限**：
- 论文未讨论极端罕见动作或大规模动作类别上的扩展性
- 训练依赖 HunyuanVideo 的 MM-DiT 架构，迁移至其他基础模型（如 CogVideoX、Wan）的效果未经验证
- 超参数 $\alpha=0.75$ 的普适性缺乏跨数据集验证

**开放问题**：
1. 是否支持多动作组合或复杂动作序列的定制？当前方法假设每个示例视频簇仅包含单一运动模式。
2. 代码与模型权重尚未公开，开源时间未知，影响可复现性评估。
3. 仅使用 20 个示例视频能否学习到足够的运动表示？在运动多样性要求更高的场景下可能需要更多样本。
4. 方法在更大规模视频数据上的训练效率与收敛性未被讨论。

### 4. 与后续工作的潜在关联

SynMotion 的双嵌入分解 + 运动适配器范式为以下方向提供了可扩展的技术接口：
- **多运动组合定制**：可将单运动嵌入扩展为多个运动嵌入的联合优化。
- **跨模型迁移**：运动适配器的低秩设计使其可插入其他 DiT 架构的视频生成模型。
- **交互式运动编辑**：解耦的主体-运动嵌入天然支持独立编辑主体或运动属性。

## 原文 PDF

![[paperPDFs/CVPR_2026/SynMotion_Semantic_Visual_Adaptation_for_Motion_Customized_Video_Generation.pdf]]

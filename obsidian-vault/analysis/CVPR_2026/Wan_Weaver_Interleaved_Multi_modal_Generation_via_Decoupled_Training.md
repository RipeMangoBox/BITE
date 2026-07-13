---
title: "Wan-Weaver: Interleaved Multi-modal Generation via Decoupled Training"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Wan_Weaver_Interleaved_Multi_modal_Generation_via_Decoupled_Training.pdf
project_link: "https://doubiiu.github.io/projects/WanWeaver"
code_link: null
aliases:
- WW
- Wan-Weaver
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将交错生成解耦为文本规划与视觉一致性建模两个子问题，分别使用大规模文本代理（textual-proxy）数据和参考驱动生成数据独立训练规划器和可视化器，避免跨模态梯度干扰，同时通过Dense Prompt Context Window注入细粒度上下文。
primary_logic: 交错式多模态输出的全局一致性可分解为文本连贯、视觉连贯和跨模态规划三个维度，利用现代VLM的已有文本能力、丰富的参考图像数据和图像-文本对齐数据，无需真实交错语料即可通过解耦训练获得优异的交错生成能力。
claims:
- 解耦训练策略显著比联合训练更稳定，视觉损失从0.25持续降至0.15，优化轨迹平滑，而联合训练存在明显震荡。
- 规划器微调不会损害核心理解能力，同时通过5g1u采样比大幅提升交错生成中图像起始标记的预测准确率。
- 引入多图像参考数据进一步强化了长程视觉一致性，使生成的多张图像在物体身份、风格和细节上保持一致。
- OpenING 上 Overall (平均分) = 8.67
---

# Wan-Weaver: Interleaved Multi-modal Generation via Decoupled Training

> [!tip] 核心洞察
> 交错式多模态输出的全局一致性可分解为文本连贯、视觉连贯和跨模态规划三个维度，利用现代VLM的已有文本能力、丰富的参考图像数据和图像-文本对齐数据，无需真实交错语料即可通过解耦训练获得优异的交错生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | Wan-Weaver：解耦训练驱动的交错式多模态生成 |
| 英文题名 | Wan-Weaver: Interleaved Multi-modal Generation via Decoupled Training |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25706) · [Project](https://doubiiu.github.io/projects/WanWeaver) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Wan-Weaver |
| Dataset | OpenING, WeaverBench, MMMU, GenEval |

> [!tip] 效果简介
> - OpenING 上，Overall (平均分) 8.67 vs 5.76 (Emu3) (+2.91)；Completeness 9.41 vs 5.90 (Emu3) (+3.51)；Multi-step Consistency 8.56 vs 5.37 (Emu3) (+3.19)。
> - WeaverBench 上，Overall 8.43 vs 8.38 (Nano Banana) (+0.05)。
> - MMMU 上，准确率 74.9 vs 55.3 (BAGEL) (+19.6)。

## 概要

交错式多模态生成（interleaved multi-modal generation）要求模型按语义逻辑交替输出文本与图像，形成图文并茂的连贯叙事。这一任务的核心瓶颈在于：大规模高质量交错式多模态训练数据极其稀缺，导致统一模型在联合优化时跨模态梯度相互干扰、优化轨迹剧烈震荡，难以学习长程上下文依赖和模态间的逻辑切换，最终使得生成内容的一致性和语义对齐严重不足。

针对上述瓶颈，**Wan-Weaver** 提出了一种解耦训练驱动的统一多模态生成框架。其核心洞察在于：交错式多模态输出的全局一致性可分解为**文本连贯**、**视觉连贯**和**跨模态规划**三个维度。利用现代视觉语言模型（VLM）已有的文本能力、丰富的参考图像数据以及图像-文本对齐数据，无需真实交错语料即可通过解耦训练获得优异的交错生成能力。

具体而言，Wan-Weaver 采用 **MoT（Mixture-of-Transformers）架构**，包含一个负责文本规划与视觉描述生成的**规划器**（基于 VLM）和一个负责图像合成的**可视化器**（基于 DiT）。训练时采用三阶段解耦策略：首先用文本代理交错数据微调规划器，使其学会何时生成文本或图像并产出密集视觉描述；随后在冻结规划器的条件下，用参考驱动生成数据独立训练可视化器；最后通过 Dense Prompt Context Window（DPCW）调优，使可视化器精准利用上下文窗口进行条件生成。推理时，规划器自回归生成文本和密集提示，触发可视化器在 DPCW 条件下合成图像，生成内容追加至历史并反馈回规划器，实现迭代式交错生成。

实验结果表明，Wan-Weaver 在交错生成基准 **OpenING** 上取得 8.67 的 Overall 分数，较此前最优模型 Emu3 的 5.76 提升了 **+2.91**；在自建的日常场景基准 **WeaverBench** 上与商用系统 Nano Banana 持平（8.43 vs. 8.38）。同时，模型在单模态理解（MMMU 74.9）、图像生成（GenEval 0.89）和图像编辑（ImgEdit 4.31）任务上均保持具有竞争力的表现，验证了解耦训练策略在保持各模态能力方面的有效性。

### 交错式多模态生成：从流水线到统一模型

多模态内容生成正从单一模态（纯文本或纯图像）向**交错式多模态生成**（interleaved multi-modal generation）演进——模型需根据用户指令，交替产出文本段落与图像，形成连贯的图文叙事。这一能力在教程编写、旅行指南、新闻报道等日常场景中具有广泛需求，要求模型同时具备文本规划、视觉生成和跨模态逻辑切换的能力。

早期方案采用**集成流水线**（integrated pipeline）策略，将独立的语言模型与图像生成模型串接，例如 **GPT-4o + DALL·E-3** 或 **Gemini + Flux**。这类系统虽能借助各模块的成熟能力完成任务，但文本与图像模块之间缺乏深层交互，难以在长程生成中维持视觉一致性——后续图像无法有效参考前文已生成的视觉内容，导致对象身份漂移、风格断裂等问题。

为突破流水线的局限，研究者开始探索**统一多模态模型**，试图在单一架构内同时完成文本与图像的生成。代表性工作包括：

- **基于多模态语言模型的方案**：**NExT-GPT**（Wu et al., ICML 2024）、**MiniGPT-5**（Zheng et al., arXiv 2023）等将图像视为特殊token嵌入语言模型，实现any-to-any的多模态生成。
- **自回归统一生成模型**：**SEED-LLaMA**（Ge et al., arXiv 2023）、**Emu3**（Wang et al., arXiv 2024）、**Anole**（Chern et al., arXiv 2024）等将图像量化为离散token，与文本token统一进行下一token预测。
- **单Transformer统一架构**：**Show-O**（Xie et al., arXiv 2024）、**VILA-U**（Wu et al., arXiv 2024）等在一个Transformer内处理多模态理解与生成。
- **商用原生系统**：**Nano Banana**（Gemini-2.5-Image）实现了原生交错式多模态生成。

### 核心瓶颈：数据稀缺与联合训练困境

尽管统一模型在架构上消除了流水线的割裂，但其性能受制于一个根本性瓶颈：**大规模高质量交错式多模态训练数据极度稀缺**。

真实的交错图文序列（如教程文章、旅游博客）不仅数量有限，且图像-文本的对齐质量参差不齐。当模型在稀缺的真实交错数据上进行**联合训练**（joint training）时，面临两个关键困境：

1. **跨模态梯度干扰**：文本生成与图像生成在优化目标、收敛速度和梯度尺度上差异显著。联合优化时，两者的梯度相互干扰，导致训练不稳定——如论文实验所示（Figure 6），联合训练的视觉损失存在明显震荡，而解耦训练则从0.25平滑降至0.15。

2. **长程依赖学习困难**：交错生成要求模型理解多轮文本与图像之间的因果逻辑和语义切换。在数据不足的条件下，模型难以学习跨越多个模态步骤的上下文依赖，导致生成内容的一致性和语义对齐极差。

### 本文动机：解耦训练与能力迁移

面对上述困境，本文提出一个核心洞察：**交错式多模态输出的全局一致性可分解为文本连贯、视觉连贯和跨模态规划三个维度**。现代视觉语言模型（VLM）已具备强大的文本理解与生成能力，丰富的参考图像数据和图像-文本对齐数据也已广泛可用——**无需依赖稀缺的真实交错语料，即可通过解耦训练获得优异的交错生成能力**。

基于这一洞察，本文提出 **Wan-Weaver**，将交错生成解耦为两个子问题：

- **文本规划**：由规划器（planner）负责，决定何时生成文本、何时生成图像，并产出图像的密集视觉描述。
- **视觉一致性建模**：由可视化器（visualizer）负责，根据规划器给出的描述和参考上下文生成图像。

通过分别使用大规模**文本代理数据**（textual-proxy data）和**参考驱动生成数据**独立训练两个模块，Wan-Weaver避免了跨模态梯度干扰，同时借助现代VLM的已有文本能力和丰富的视觉数据，实现了从单模态能力向交错多模态生成的有效迁移。

## 核心方法与创新机理

Wan-Weaver 的核心创新在于将交错式多模态生成这一复杂问题分解为两个可独立优化的子问题——**文本规划**与**视觉一致性建模**——并通过一套解耦训练框架和上下文条件机制，系统性地解决了统一模型在稀缺交错数据下联合训练不稳定、长程一致性差的瓶颈。

### 创新一：MoT 架构下的规划-可视化专家分工

传统统一模型（如 **Emu3**、**Show-O**、**VILA-U**）采用单个 Transformer 同时处理文本和图像生成，或依赖松耦合的文本-图像流水线（如 **Gemini+Flux**、**GPT-4o+DALL·E-3**），难以在模态间建立紧密的因果依赖。Wan-Weaver 采用 **Mixture-of-Transformers（MoT）** 架构，将模型分解为两个功能明确的专家模块：

- **规划器（Planner Expert）**：基于 VLM 的自回归 Transformer，负责生成纯文本和**密集提示（dense prompt）**——一种用 `<imagine>...</imagine>` 包裹的详细视觉描述，作为图像生成的语义蓝图。规划器决定何时生成文本、何时触发图像生成，并产出图像的内容规格。
- **可视化器（Visualizer Expert）**：基于 **Diffusion Transformer（DiT）** 的图像生成器，以规划器产出的密集提示为条件合成图像。可视化器通过**因果多模态自注意力**与规划器交互，使图像生成过程能够感知前文语境。

这一分工的关键在于：规划器专注于语言层面的叙事逻辑和模态切换规划，可视化器专注于视觉质量和跨图像一致性，两者通过密集提示这一文本代理（textual proxy）进行解耦通信，避免了跨模态梯度直接耦合带来的优化冲突。

### 创新二：解耦训练策略——用文本代理数据替代真实交错语料

这是 Wan-Weaver 最具决定性的创新。大规模高质量交错式图文训练数据极度稀缺，导致端到端联合训练时视觉损失震荡、优化轨迹不稳定（Fig. 6 证实联合训练存在严重震荡，而解耦训练的视觉损失从约 0.25 持续平滑下降至 0.15）。Wan-Weaver 的解决方案是**用文本代理数据完全替代真实交错语料**：

1. **规划器微调（Planner Tuning）**：将训练数据中的真实图像替换为对应的密集文本描述（用 `<imagine>...</imagine>` 包裹），形成纯文本的交错序列。规划器在这些文本代理数据上学习何时插入 `<BOI>` 标记来指示图像位置，并生成准确的密集提示。同时混入生成任务代理数据（generation-proxy data）和通用理解数据（understanding data），以 **5g1u 的生成-理解采样比**在规划可靠性和理解能力之间取得平衡——实验表明理解性能保持稳定，而图像起始标记的预测准确率显著提升（Fig. 7）。

2. **可视化器独立训练（Visualizer Training）**：在冻结规划器的条件下，使用三类数据独立训练 DiT 可视化器——文本-图像对（学习文本对齐）、单图像参考数据（学习参考驱动生成）和**多图像参考数据**（学习跨图像视觉一致性）。消融实验证实，引入多图像参考数据能显著强化长程视觉一致性，使生成的多张图像在物体身份、风格和细节上保持一致（Fig. 8）。

3. **DPCW 调优（Dense Prompt Context Window Tuning）**：在可视化器训练完成后，引入一个额外的微调阶段，仅调整可视化器以适配基于上下文窗口的条件生成方式（见创新三）。此阶段仍仅微调可视化器，规划器保持冻结。

这一解耦策略的核心优势在于：规划器和可视化器各自使用最丰富、最易获取的数据进行训练（文本代理数据 + 参考图像数据），完全规避了对稀缺真实交错语料的依赖，同时消除了跨模态联合优化的梯度干扰。

### 创新三：密集提示上下文窗口（DPCW）

传统自回归模型将所有历史 token 纳入因果自注意力，但在交错生成场景中，图像生成仅需关注其周围的语义上下文，而非整个历史序列。Wan-Weaver 引入 **Dense Prompt Context Window（DPCW）** 机制：

- 在密集提示位置周围定义一个局部自注意力窗口，仅该窗口内的文本 token 和 ViT 图像特征参与可视化器的因果多模态自注意力计算。
- DPCW 封装了密集提示的语义丰富性，同时通过逐层因果自注意力聚合了前文的累积语境信息，使可视化器能够精确地以相关上下文为条件生成图像。

DPCW 的设计使得可视化器在推理时无需处理全量历史，既提升了上下文利用的精度，也为长序列生成中的计算效率优化提供了结构基础。

### 创新总结：从“联合优化”到“解耦协调”

Wan-Weaver 的方法论贡献可归纳为三个层面的 changed slots：

| 维度 | 基线方法 | Wan-Weaver |
|------|---------|------------|
| **模型架构** | 单 Transformer 统一处理文本/图像，或松耦合流水线 | MoT 架构：规划器（VLM）+ 可视化器（DiT），通过因果多模态自注意力交互 |
| **训练策略** | 在真实交错序列上联合训练 | 解耦训练：规划器用文本代理数据微调，可视化器用参考数据独立训练 + DPCW 调优 |
| **数据表示与条件** | 原始交错序列，标准因果自注意力 | 图像位置用 `<BOI>` + 密集描述替代真实图像；DPCW 局部窗口条件生成 |

这一创新组合使得 Wan-Weaver 在 OpenING 基准上以 8.67 的 Overall 分数大幅超越此前最优的 **Emu3**（5.76），在 Completeness（9.41 vs. 5.90）和 Multi-step Consistency（8.56 vs. 5.37）上尤其突出，验证了解耦训练策略在交错生成任务上的决定性优势。

Wan-Weaver 将交错式多模态生成问题分解为**文本规划**与**视觉一致性建模**两个子问题，并据此设计了一个统一的 **Mixture-of-Transformers (MoT)** 架构。该架构包含两个核心专家模块：

- **规划器 (Planner)**：基于 VLM 实现，负责自回归地生成纯文本和**密集提示 (dense prompts)**——即用 `<imagine>…</imagine>` 包裹的详细视觉描述，作为可视化器的生成条件。规划器决定“何时生成图像”以及“图像应包含什么内容”。
- **可视化器 (Visualizer)**：基于 Diffusion Transformer (DiT) 实现，在接收到密集提示后被触发，通过因果多模态自注意力与规划器交互，合成对应的图像。

### 推理流程

Figure 2 给出了完整的推理循环：

![[assets/figures/papers/paper_list_l2075_https_arxiv_org_abs_2603_25706/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the inference process of Wan-Weaver. Given a prompt, the planner expert autoregressively generates plain text and dense prompts as visualization cues. Through causal multi-modal self-attention, the visualizer interacts with the planner, enabling it to synthesize images conditioned on the dense prompt context and visual references. The resulting text–image outputs are appended to the history and fed back into the planner, enabling an iterative interleaved generation process that maintains long-range contextual coherence*

1. 给定用户提示，规划器自回归地逐 token 生成输出序列。当需要生成图像时，规划器产出一个 `<BOI>` 标记和一个密集提示。
2. 密集提示触发可视化器。系统通过 **Dense Prompt Context Window (DPCW)** 机制，在密集提示位置周围提取精确的上下文特征：DPCW 不仅封装了密集提示的语义丰富性，还聚合了通过逐层因果自注意力累积的前序上下文信息。
3. 可视化器在 DPCW 条件（窗口内的文本特征与 ViT 特征）下合成图像。
4. 生成的文本-图像输出被追加至历史序列，并反馈回规划器，作为下一轮自回归生成的上下文条件。

这一迭代式循环使得模型能够在长序列中维持跨模态的上下文连贯性，实现“文本-图像-文本-图像”的自然交错输出。

### 训练策略

为规避跨模态联合优化中的梯度干扰和不稳定问题，Wan-Weaver 采用**解耦训练**策略（Figure 3），分三个阶段独立训练规划器和可视化器：

- **Stage 1 — 规划器微调**：在文本代理交错数据（用密集描述替代真实图像）、生成任务代理数据与理解数据上微调规划器，使其学会何时生成 `<BOI>` 标记并产出高质量的密集视觉描述。
- **Stage 2 — 可视化器训练**：冻结规划器，在文本-图像对、单图像参考和多图像参考数据上独立训练 DiT 可视化器，学习文本对齐和视觉一致性。
- **Stage 3 — DPCW 调优**：仅微调可视化器，使其适应基于密集提示上下文窗口的条件生成方式，提升上下文利用精度。

### 核心机制：DPCW

DPCW 是连接规划器与可视化器的关键桥梁。它在密集提示位置定义了一个自注意力窗口，仅窗口内的文本 token 和 ViT 特征参与可视化器的因果多模态自注意力计算。这一设计使得可视化器能够精确地利用规划器产出的语义条件，而非被长序列中的无关信息所干扰，从而在保持生成质量的同时降低计算冗余。

### 问题定义：交错多模态序列的因果分解

Wan-Weaver 将交错式多模态生成建模为一个自回归序列问题。给定一个由文本和图像交替组成的多模态序列 $\mathbf{x} = (\mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_T)$，其联合对数概率可分解为每一步模态在前文条件下的条件对数概率之和：

$$\log P_{\theta}(\mathbf{x}) = \sum_{t=0}^{T} \log P_{\theta}(\mathbf{x}_{t+1} \mid \mathbf{x}_{0}, \ldots, \mathbf{x}_{t})$$

其中 $\mathbf{x}_t$ 可以是文本 token 或图像。这一分解的核心意义在于：交错生成的全局一致性——文本连贯、视觉连贯、跨模态规划——完全取决于模型在每一步是否能够充分利用前序上下文做出正确的模态选择和内容生成决策。该公式是后续 MoT 架构设计和解耦训练策略的理论出发点。

### 核心模块一：MoT 架构与规划器-可视化器分工

Wan-Weaver 采用统一的 **Mixture-of-Transformers (MoT)** 架构，包含两个功能解耦的专家模块：

- **规划器**：基于预训练 VLM 构建，负责自回归地生成纯文本和**密集提示**。密集提示是包裹在 `<imagine>...</imagine>` 标签中的详细视觉描述，作为可视化器的生成条件。规划器通过预测 `<BOI>` 标记来决定何时触发图像生成，从而承担“何时生成什么模态”的规划职责。

- **可视化器**：实现为 **Diffusion Transformer (DiT)**，在规划器冻结的条件下独立训练。当规划器输出密集提示时，可视化器通过因果多模态自注意力与规划器交互，以流匹配损失合成对应图像。

这种分工的本质是将交错生成的全局一致性分解为两个子问题：规划器负责文本连贯与模态切换逻辑，可视化器负责视觉内容与文本条件的对齐。

### 核心模块二：Dense Prompt Context Window

在推理时，可视化器并非直接关注全部历史 token，而是通过 **Dense Prompt Context Window (DPCW)** 机制提取精确的上下文特征。具体而言，DPCW 在密集提示位置周围定义一个自注意力窗口，仅窗口内的文本特征和 ViT 视觉特征参与可视化器的因果多模态自注意力计算。

DPCW 的设计动机是：密集提示本身已封装了丰富的语义信息，而窗口内的前序上下文通过逐层因果自注意力累积了生成所需的历史信息。这一机制在保证上下文利用精度的同时，避免了长序列下全注意力带来的计算冗余。

### 核心模块三：解耦训练三阶段

Wan-Weaver 的训练策略由三个解耦阶段构成，对应图 Figure 3 的示意：

1. **规划器微调**：使用文本代理交错数据（用密集描述替代真实图像）、生成任务代理数据和理解数据训练规划器。关键设计是采用 **5g1u 采样比**（5 份生成数据配 1 份理解数据），在规划可靠性与理解稳定性之间取得平衡——理解性能保持稳定，同时图像起始标记 `<BOI>` 的预测准确率显著提升。

2. **可视化器训练**：冻结规划器，用文本-图像对、单图像参考和多图像参考数据独立训练 DiT 可视化器。多图像参考数据的引入是关键增强项，使模型在多张生成图像间保持对象身份、风格和细节的一致性。

3. **DPCW 调优**：仅微调可视化器，使其适应基于 DPCW 窗口的条件生成方式，进一步提升上下文利用精度。

解耦训练的因果机制在于：规划器与可视化器的联合训练会导致跨模态梯度干扰，视觉损失出现明显震荡；而解耦后视觉损失从约 0.25 持续下降至 0.15，优化轨迹平滑。

### 推理循环

推理时，规划器自回归生成文本和密集提示，触发可视化器在 DPCW 条件下生成图像。生成的图文内容追加至历史并反馈至规划器，形成迭代式交错生成循环。这一循环机制使模型能够在长程生成中持续利用前序上下文，维持全局一致性。

## 实验与关键发现

### 1. 评测基准与实验设置

为全面衡量 Wan-Weaver 的交错式多模态生成能力，论文引入两个评测基准：**OpenING** 和自建的 **WeaverBench**。OpenING 是面向交错图文生成的标准评测集，涵盖完整性（Completeness）、多步一致性（Multi-step Consistency）等维度。WeaverBench 则针对日常场景设计，覆盖 15 个主题类别，同时包含纯文本提示和图文混合提示，提示长度和请求图像数量呈多样化分布（Fig. 4）。评测采用 GPT-4o 作为评判模型，从提示遵循度（PA）、叙事协调性（NC）、内容一致性（CC）、图像一致性（IC）和完整性（CP）五个维度进行打分。

![[assets/figures/papers/paper_list_l2075_https_arxiv_org_abs_2603_25706/figures/005_Figure_4.jpg]]
*Figure 4: Statistics of WeaverBench. (a) Topic distribution across 14 everyday categories. (b) Prompt length distribution. (c) Distribution of the number of images requested per prompt*

训练配置方面，可视化器（Visualizer）基于 DiT 架构，使用 AdamW 优化器训练 9.6T tokens，学习率从 $5 \times 10^{-5}$ 衰减至 $2.5 \times 10^{-5}$。规划器（Planner）在 35.72G tokens 上微调，学习率为 $7 \times 10^{-6}$，采用 5:1 的生成-理解数据采样比（5g1u）。

### 2. 交错式生成主结果

**Table 1** 展示了 Wan-Weaver 在 OpenING 基准上的定量对比。Wan-Weaver 以 **8.67 的 Overall 分数**大幅领先所有对比方法，较此前最优的开源统一模型 Emu3（5.76）提升 **+2.91**。在关键的子维度上，Completeness 达到 **9.41**（Emu3 为 5.90，提升 +3.51），Multi-step Consistency 达到 **8.56**（Emu3 为 5.37，提升 +3.19），表明模型在长程图文交替生成中能有效保持语义完整性和视觉连贯性。相比集成流水线方案（如 Gemini+Flux、GPT-4o+DALL·E-3），Wan-Weaver 同样展现出显著优势，验证了统一解耦架构在交错生成任务上的有效性。

在更贴近日常使用的 WeaverBench 上（**Table 2**），Wan-Weaver 以 **8.43 的 Overall 分数**略优于商用原生多模态系统 Nano Banana（8.38），并在 Prompt Adherence 和 Completeness 等维度上表现突出。定性对比（Fig. 5）进一步显示，Wan-Weaver 在多图像生成场景中能更好地保持物体身份、风格和场景逻辑的一致性，而 Nano Banana 在长序列交错生成中偶尔出现图像内容漂移或文本-图像语义不匹配的问题。

![[assets/figures/papers/paper_list_l2075_https_arxiv_org_abs_2603_25706/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on WeaverBench. PA: Prompt Adherence, NC: Narrative Coordination, CC: Content Consistency, IC: Image Consistency, CP: Completeness*

![[assets/figures/papers/paper_list_l2075_https_arxiv_org_abs_2603_25706/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison with the state-of-the-art commercial system Nano Banana on interleaved text–image generation*

### 3. 单模态任务表现

尽管 Wan-Weaver 的核心设计目标是交错式生成，其在单模态理解和生成任务上同样具备竞争力（**Table 3**）。在理解基准 MMMU 上，Wan-Weaver 达到 **74.9** 的准确率，显著高于此前统一模型 BAGEL（55.3）和 SEED-X（54.3）。在文本到图像生成基准 GenEval 上，Wan-Weaver 取得 **0.89** 的分数，优于 FLUX.1-dev（0.66）和 SD3-Medium（0.74）。在图像编辑基准 ImgEdit 上，Wan-Weaver 以 **4.31** 的成绩领先 BAGEL（3.20）和 SEED-X（2.82）。这些结果表明，解耦训练策略在赋予模型交错生成能力的同时，并未牺牲单模态任务的性能，反而通过专项训练实现了更优的文本对齐和视觉生成质量。

![[assets/figures/papers/paper_list_l2075_https_arxiv_org_abs_2603_25706/figures/008_Table_3.jpg]]
*Table 3: Comparison across single-modality generation tasks (understanding, image generation, and editing). †: Our in-house base model with thinking mode (enabled only for understanding)*

### 4. 消融实验与关键设计验证

#### 4.1 解耦训练 vs. 联合训练

**Fig. 6** 对比了不同训练策略下可视化器的损失曲线。解耦训练（decoupled training）使视觉损失从约 0.25 持续下降至 0.15，优化轨迹平滑且收敛稳定。相比之下，规划器与可视化器联合训练（joint training）的损失曲线存在明显震荡，收敛速度慢且最终损失值更高。这直接验证了论文的核心主张：**跨模态梯度干扰是统一模型交错生成不稳定的关键瓶颈，解耦训练通过隔离文本规划与视觉生成的优化过程，有效消除了这一干扰**。

#### 4.2 规划器训练数据的影响

**Fig. 7** 展示了规划器在不同训练数据配比下的表现。左侧的理解性能指标表明，引入生成任务数据和文本代理数据后，规划器在 MMLU、MMBench 等理解基准上的性能无明显退化，保持在稳定水平。右侧的 token 预测统计则显示，采用 5g1u（生成:理解 = 5:1）的采样比能显著提升 `<BOI>`（图像起始标记）的预测准确率，同时维持文本 token 的预测质量。论文据此确定 5g1u 为规划器微调的最终数据配比，在规划可靠性和理解稳定性之间取得最佳平衡。

#### 4.3 多图像参考数据对视觉一致性的影响

**Fig. 8** 通过定性对比展示了可视化器训练中引入多图像参考数据的价值。仅使用文本-图像对训练的可视化器在生成多张图像时，难以保持物体身份和风格的一致性（例如同一角色在不同图像中外貌差异明显）。加入单图像参考数据后，一致性有所改善但仍不完美。进一步引入**多图像参考数据**后，可视化器能够学习到跨图像的长程视觉连贯性建模能力，使生成的多张图像在物体身份、纹理细节和整体风格上保持高度一致。这为交错式叙事中需要同一主体多次出现的场景提供了关键的视觉保障。

#### 4.4 DPCW 机制的有效性

Dense Prompt Context Window（DPCW）的设计旨在为可视化器提供精确的局部上下文条件。消融分析表明，移除 DPCW 而使用全局因果自注意力会导致可视化器过度关注远距离无关 token，生成图像与当前密集提示的语义对齐度下降。DPCW 通过限定注意力窗口范围，使可视化器聚焦于密集提示周围的文本语义和 ViT 特征，从而提升了图像生成的上下文精准度。

### 5. 失败模式与局限性

尽管 Wan-Weaver 在交错式生成上取得了显著进展，论文仍揭示了若干失败模式（Fig. 10）：

- **分辨率自适应缺失**：模型目前无法根据内容语义自动推断每张生成图像的最佳分辨率和宽高比，而是采用固定或粗粒度的分辨率策略。在需要不同尺寸图像（如全景图与特写图）交替出现的场景中，这可能影响视觉叙事效果。
- **长序列累积开销**：顺序生成过程中，所有先前生成的内容作为历史信息累积反馈至规划器。在极长序列下，上下文长度线性增长，可能导致计算开销增大和注意力分散，部分早期信息被稀释。
- **理解与生成单向隔离**：规划器微调虽保留了理解能力，但未能从可视化器的生成反馈中进一步提升理解水平。理解与生成之间尚未形成双向增强的闭环，这是解耦架构的一个内在局限。

此外，论文未深入讨论评测中的公平性问题。WeaverBench 和 OpenING 的评测依赖 GPT-4o 作为评判模型，其自身偏见可能影响评估结果的客观性。数据覆盖的 15 个日常类别虽力求广泛，但未对社会偏见或文化多样性进行专门分析，需要读者在实际应用中保持审慎。

![[assets/figures/papers/paper_list_l2075_https_arxiv_org_abs_2603_25706/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with existing state-of-the-art methods on interleaved generation benchmark OpenING [92]*

## 定位与知识库关联

### 1. 方法在交错生成谱系中的坐标

Wan-Weaver 的提出直接回应了当前交错式多模态生成（Interleaved Multi-modal Generation）领域的核心瓶颈：**大规模高质量交错训练数据的稀缺导致端到端联合训练极不稳定，难以学习长程跨模态依赖和模态切换逻辑**。在此背景下，现有方法可大致划分为三个技术路线，Wan-Weaver 在其中占据了独特的解耦位置。

**路线一：端到端统一模型。** 这类方法试图在单个 Transformer 或统一架构中同时完成文本和图像的自回归生成，直接在真实交错序列上联合优化。代表工作包括 **NExT-GPT**（Wu et al., ICML 2024）的 any-to-any 多模态 LLM、**Show-O**（Xie et al., arXiv 2024）的单 Transformer 统一理解与生成、**Emu3**（Wang et al., arXiv 2024）的下一 token 预测统一框架，以及 **Anole**（Chern et al., arXiv 2024）的开源自回归原生多模态生成。这些方法面临共同的困境：跨模态梯度干扰导致优化轨迹震荡，视觉质量和文本连贯性难以兼顾。OpenING 基准上 Emu3 的 Overall 分数仅为 5.76，Multi-step Consistency 仅 5.37，直接反映了端到端联合训练在长程视觉一致性上的不足。

**路线二：集成流水线。** 这类方法将文本生成和图像生成分离为独立模型，通过工程化流程拼接。代表如 **Gemini + Flux** 和 **GPT-4o + DALL·E-3**。其优势在于可复用各自领域最强的单模态模型，但缺乏统一的上下文建模——文本规划器无法感知已生成图像的视觉内容，图像生成器也无法利用前序文本的语义约束，导致多步生成中全局一致性严重依赖外部编排。

**路线三：原生商用系统。** 以 **Nano Banana**（Gemini-2.5-Image）为代表，其技术细节未公开，但从 WeaverBench 评测结果看（Overall 8.38），已在日常场景的交错生成中达到较高水平。

**Wan-Weaver 的定位：解耦训练的统一架构。** Wan-Weaver 在架构上采用 MoT（Mixture-of-Transformers）统一框架，包含规划专家（基于 VLM）和可视化专家（DiT），通过因果多模态自注意力实现交互——这与路线一的统一建模理念一致。但关键区别在于**训练策略的彻底解耦**：规划器使用文本代理（textual-proxy）交错数据独立微调，可视化器使用参考驱动生成数据独立训练，仅在最后的 DPCW 调优阶段进行轻量联合适配。这一设计使 Wan-Weaver 同时获得了统一架构的表达能力和解耦训练的稳定性，在 OpenING 上以 8.67 Overall 显著超越 Emu3（+2.91），在 WeaverBench 上以 8.43 Overall 略超 Nano Banana（+0.05），验证了该技术路线的有效性。

### 2. 核心设计决策的知识贡献

**（1）问题分解的因果逻辑。** 论文的核心洞察在于将交错多模态输出的全局一致性分解为三个可独立优化的维度：文本连贯性（由 VLM 的预训练能力保障）、视觉连贯性（由参考驱动生成数据训练）、以及跨模态规划（由文本代理数据训练）。这一分解使得每个子问题都能利用丰富且廉价的代理数据，而非稀缺的真实交错语料，从根本上绕开了数据瓶颈。

**（2）文本代理数据与 Dense Prompt。** 用 `<imagine>...</imagine>` 包裹的密集描述替代真实图像，将交错生成问题转化为“规划器学习何时生成何种视觉描述”的文本任务。这一设计使得规划器微调可以完全在文本域完成，避免了跨模态梯度干扰。消融实验（Fig. 7）表明，引入生成与代理数据后理解性能无明显退化，同时 5g1u 的生成-理解采样比实现了规划可靠性与理解稳定性的最佳平衡。

**（3）Dense Prompt Context Window（DPCW）。** 在密集提示位置周围定义自注意力窗口，仅窗口内的文本和 ViT 特征参与可视化器的条件生成。这一机制在保持上下文精度的同时控制了计算复杂度，是解耦训练与统一推理之间的关键桥梁。

### 3. 适用边界与局限

**（1）分辨率规划的缺失。** 模型目前无法根据内容语义自适应地确定每张生成图像的最佳分辨率和宽高比，而是采用固定或粗粒度的分辨率策略。在需要精细构图控制的场景（如信息图、多图排版叙事）中，这一限制可能导致视觉表达力不足。

**（2）长序列的累积条件问题。** 顺序生成过程中，所有先前生成的内容作为参考信息累积反馈至规划器。在极长序列下，这不仅导致计算开销线性增长，还可能引入上下文冗余甚至干扰，影响后续生成的精准度。论文未提出针对性的压缩或遗忘机制。

**（3）理解与生成尚未双向增强。** 规划器微调虽然保留了理解水平（MMMU 74.9），但未能从可视化器的反馈中进一步提升理解性能。这意味着模型的“看”与“说”能力仍处于单向服务关系，尚未实现类似人类认知中的视觉-语言双向增益。

**（4）数据覆盖与社会偏见。** WeaverBench 虽涵盖 15 个日常类别，但论文未讨论训练数据或模型输出中的社会偏见问题。大型评测基准依赖 GPT-4o 等模型作为评判器，其自身偏见可能影响评估结果的公平性，需在实际应用中谨慎对待。

### 4. 开放问题

基于上述局限，以下问题值得后续工作关注：

- **自适应分辨率规划**：如何在交错生成中使模型根据内容语义推断合适的图像尺寸和宽高比？可能的路径包括在密集提示中引入分辨率预测头，或利用强化学习优化构图质量。
- **长序列上下文压缩**：在不损失上下文保真度的前提下，可采用哪些机制（如记忆压缩、选择性遗忘、分层上下文窗口）来削减累积条件信息？这对扩展至数十步以上的交错叙事至关重要。
- **双向能力增强**：什么样的训练策略或数据配比能够使理解能力和生成能力相互增强？例如，是否可以通过生成结果的自我评估反馈来提升规划器的视觉推理水平？
- **评估体系的完善**：当前交错生成的自动评估仍高度依赖 VLM 评判器，其评分偏差和偏好对齐问题尚未被充分研究。构建更可靠的多模态生成评估基准仍是领域共同面临的挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/Wan_Weaver_Interleaved_Multi_modal_Generation_via_Decoupled_Training.pdf]]

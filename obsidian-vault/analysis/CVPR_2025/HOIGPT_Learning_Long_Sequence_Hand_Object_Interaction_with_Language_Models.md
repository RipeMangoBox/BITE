---
title: HOIGPT Learning Long Sequence Hand Object Interaction with Language Models
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Models.pdf
project_link: null
code_link: null
aliases:
- HLLSHOILM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: HOI 分解式 VQ-VAE 标记化与几何约束损失。通过分离手与物体码本大幅降低标记空间复杂度，同时引入穿透、接触、接触区域正则化保证物理合理性。
primary_logic: 将大型语言模型与专门设计的 HOI 分解标记器结合，利用 LLM 的序列推理能力和分解式码本，首次实现文本与 3D HOI 序列之间的双向高质量生成与理解。
claims:
- 在文本到 HOI 生成任务上，HOIGPT 的 FID 达到 3.29，相较于先前最佳方法降低 2.56，大幅领先。
- 在 HOI 到文本生成任务上，R Precision 相对提升 +2.01%。
- 消融实验表明，引入 HOI 分解 VQ-VAE 组件较朴素 VQ-VAE 性能提升 23%，且几何损失有效减少穿透并提升文本描述准确度。
- Text-to-HOI 生成 (ARCTIC+GRAB) 上 FID = 3.29 ± 0.54
---

# HOIGPT Learning Long Sequence Hand Object Interaction with Language Models

> [!tip] 核心洞察
> 将大型语言模型与专门设计的 HOI 分解标记器结合，利用 LLM 的序列推理能力和分解式码本，首次实现文本与 3D HOI 序列之间的双向高质量生成与理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOIGPT：基于语言模型的长序列手-物体交互学习 |
| 英文题名 | HOIGPT Learning Long Sequence Hand Object Interaction with Language Models |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HOIGPT |
| Dataset | Text-to-HOI 生成, HOI-to-text 生成 |

> [!tip] 效果简介
> - Text-to-HOI 生成 (ARCTIC+GRAB) 上，FID 3.29 ± 0.54 vs previous SOTA (-2.56 (相对先前最佳降低 2.56))。
> - HOI-to-text 生成 (ARCTIC+GRAB) 上，R Precision (Top 3) 48.43 vs previous SOTA (+2.01% (相对提升))。

## 概要

手-物体交互（Hand-Object Interaction, HOI）是三维视觉与具身智能的核心问题，涉及手部与物体在空间和时间上的紧密协同。现有方法面临一个根本性瓶颈：**缺乏统一的双向模型，难以同时保证长序列的物理一致性和多条件的生成灵活性**。具体而言，基于扩散模型的方法（如 **DiffH2O** (Christen et al., arXiv 2024)）虽能生成高质量运动，但难以处理文本到运动与运动到文本的双向转换；而将手与物体的运动联合编码为单一标记的策略，导致标记空间复杂度极高，物理合理性难以保证。

HOIGPT 的核心洞察在于：**将大型语言模型（LLM）的序列推理能力与专门设计的 HOI 分解式标记器相结合**，首次在统一的标记空间内实现文本与三维 HOI 序列之间的双向高质量生成与理解。其因果调控机制体现为两个关键设计：

1. **HOI 分解式 VQ-VAE 标记化**：通过为手部（左手、右手）和物体分别构建独立的码本，将联合标记空间分解为三个子空间，大幅降低标记复杂度，同时保留各模态的结构特性。
2. **几何约束损失**：引入穿透损失 $L_{pen}$、接触损失 $L_C$ 和接触区域损失 $L_R$ 三项正则化，在标记器训练阶段显式约束生成序列的物理合理性，有效抑制手部穿透物体、接触缺失等问题。

在实验验证层面，HOIGPT 在 ARCTIC 和 GRAB 数据集上取得了决定性优势。在文本到 HOI 生成任务上，FID 达到 3.29，相较先前最佳方法降低 2.56，实现了大幅领先；在 HOI 到文本生成任务上，R Precision 相对提升 +2.01%。消融实验进一步证实，HOI 分解式 VQ-VAE 组件相较朴素 VQ-VAE 带来 23% 的性能提升，且几何损失在减少穿透体积和提升文本描述准确度方面具有显著作用。

在方法谱系上，HOIGPT 处于运动生成与多模态语言模型的交叉地带。相较于 **T2MGPT** (Zhang et al., CVPR 2023) 和 **MotionGPT** (Jiang et al., NeurIPS 2023) 等纯人体运动-语言模型，HOIGPT 将建模对象扩展至手-物交互这一更复杂的联合空间；相较于 **TM2T** (Guo et al., ECCV 2022) 等单向运动理解方法，HOIGPT 实现了真正的双向转换。其关键创新在于用分解式标记化替代联合编码，用 LLM 自回归生成替代扩散模型，从而在物理一致性和多任务灵活性之间取得了新的平衡。

当前工作的主要局限在于：仅在有限物体类别的 ARCTIC 和 GRAB 数据集上验证，对开放词汇场景的泛化能力尚不明确；依赖完整物体点云作为输入，尚未探索端到端从视觉感知到交互生成的路径；使用的语言模型规模较小（Flan-T5-Base, 220M 参数），更大模型可能进一步提升长序列的语义连贯性。

手-物体交互（Hand-Object Interaction, HOI）是具身智能和人机交互领域的核心问题，涉及对三维空间中手部与物体协同运动的感知、生成与理解。近年来，随着 ARCTIC、GRAB 等大规模 HOI 数据集的发布，基于深度学习的 HOI 生成方法取得了显著进展。然而，现有方法面临一个关键瓶颈：**缺乏统一的、双向的模型架构，难以同时满足长序列生成中的物理一致性要求和多条件输入的灵活性需求**。

具体而言，当前 HOI 生成与理解方法存在以下结构性缺口：

**1. 单向建模的局限性。** 现有方法通常将文本到 HOI 生成与 HOI 到文本理解视为两个独立任务，分别采用不同的模型架构。例如，**T2MGPT**（Zhang et al., CVPR 2023）和 **MotionGPT**（Jiang et al., NeurIPS 2023）专注于运动-语言的双向转换，但未专门处理手-物体交互场景；**DiffH2O**（Christen et al., arXiv 2024）采用扩散模型进行 HOI 生成，但缺乏文本理解能力。这种任务割裂导致模型无法充分利用文本与 HOI 序列之间的双向语义关联，限制了在多任务场景下的应用潜力。

**2. 标记空间效率低下。** 手-物体交互涉及高度复杂的高维联合空间——手部姿态由 MANO 参数导出，物体姿态包含全局位置、6D 旋转和关节角度。传统的 VQ-VAE 方法采用单一码本对整个 HOI 序列进行量化，未能有效分解手部运动与物体运动之间的模态差异，导致码本利用率低、重建精度差，进而影响下游生成任务的物理合理性。

**3. 物理合理性保障不足。** 手-物体交互的核心在于物理接触的合理性：手部不能穿透物体表面，接触区域应符合真实交互模式。然而，现有方法普遍缺乏专门的几何约束机制，生成的 HOI 序列常出现穿透、接触不自然等问题，严重影响了生成结果的可用性。

针对上述问题，HOIGPT 提出了一个统一的解决方案：**将大型语言模型（LLM）与专门设计的 HOI 分解标记器相结合**。其核心洞察在于：LLM 的序列推理能力可以自然地建模 HOI 序列的时序依赖，而分解式码本设计能够大幅降低标记空间的复杂度，同时引入几何约束损失确保物理合理性。这一设计首次实现了文本与 3D HOI 序列之间的双向高质量生成与理解，为手-物体交互的通用建模提供了新的范式。

## 核心方法与创新机理

HOIGPT 的核心创新在于将**大型语言模型（LLM）的序列推理能力**与专门设计的**HOI 分解式标记化策略**相结合，首次构建了一个能够实现文本与 3D 手-物交互序列之间**双向高质量生成与理解**的统一框架。其关键突破点可归纳为三个相互耦合的 changed slots。

### 1. HOI 分解式 VQ-VAE 标记化

现有方法（如 Text2HOI、MotionGPT）通常采用单一码本对 HOI 序列进行联合量化，这导致标记空间复杂度随手与物体的联合自由度呈指数增长，标记效率低且难以捕捉手与物体各自独立的运动模式。HOIGPT 提出的**HOI 分解式 VQ-VAE**（Figure 3）将标记化过程解耦为三个独立通道：

- **物体码本**：编码物体的全局位置 $\tau_o$、6D 旋转 $\phi_o$ 及关节角度 $\alpha_o$
- **左手码本**与**右手码本**：分别编码左右手的全局位置 $\tau$ 与 6D 旋转 $\phi$

每个码本大小均为 512（Sec. 4.1），通过分离手与物体的表示空间，大幅降低了标记空间的复杂度。编码器由三个特征提取器组成——手部运动特征、物体运动特征以及经 PointNet 编码的物体点云特征——分别送入对应的 VQ-VAE 分支进行量化。解码阶段则以预测的物体运动为条件，结合所有潜特征重建最终序列：

$$\hat{X}_s = \mathcal{D}((\hat{\mathbf{z}} + \mathbf{c}_o) \vert \mathcal{D}_o(\hat{\mathbf{z}}_o + \mathbf{c}_o))$$

消融实验（Table 3）直接验证了这一设计的有效性：**HOI 分解式 VQ-VAE 组件使生成性能较朴素（单一码本）VQ-VAE 提升 23%**。

### 2. 物理合理性导向的几何约束损失

HOI 生成的核心挑战不仅在于运动学的准确性，更在于手与物体之间交互的物理合理性——穿透、悬空、接触错位是此前方法的常见失败模式。HOIGPT 在 VQ-VAE 训练中引入了三项几何约束损失，构成因果调节的关键旋钮：

- **穿透损失** $\mathcal{L}_{pen}$：惩罚手部顶点穿透物体表面的程度，直接量化并最小化穿透体积：

  $$\mathcal{L}_{pen} = \frac{1}{|\mathcal{P}_{\mathrm{in}}^o|} \sum_{p \in \mathcal{P}_{\mathrm{in}}^o} \min_i \|p - \hat{V}_i\|_2^2$$

- **接触损失** $\mathcal{L}_C$：确保手部关节在接触前保持在物体表面距离 $\phi$ 以内，防止“幽灵接触”或悬空操作：

  $$\mathcal{L}_C = \sum_i D(\hat{J}_i^o), \quad \forall D(\hat{J}_i^o) \leq \phi$$

- **接触区域损失** $\mathcal{L}_R$：对齐真实与重构的接触区域，并约束手部顶点不远离物体表面（阈值 $\tau$）：

  $$\mathcal{L}_R = \sum_i \|\Phi(P_i^o) - \Phi(\hat{P}_i^o)\|_2 + D(\hat{P}_i^o), \quad \forall D(P_i^o) < \tau$$

三项损失加权求和构成几何损失 $\mathcal{L}_{geo} = \lambda \mathcal{L}_{pen} + \beta \mathcal{L}_C + \gamma \mathcal{L}_R$，与标记器重建损失 $\mathcal{L}_{tok}$ 联合优化。消融实验证实，**移除几何损失会增加穿透体积并降低文本描述准确度**（Table 3, Sec. 4.5），表明物理约束不仅改善了交互合理性，还间接提升了语义对齐质量。

### 3. 基于 LLM 的自回归生成框架

与以扩散模型为主的先前方法（如 **DiffH2O** (Christen et al., arXiv 2024)）不同，HOIGPT 采用基于 LLM 的自回归生成范式。具体而言，模型使用 **Flan-T5-Base**（220M 参数）作为骨干语言模型，将文本标记与 HOI 分解标记统一到同一标记空间中，通过最大化自回归似然进行训练：

$$\mathcal{L}_{lm} = - \sum_{i=0}^{L_t-1} \log p_{\theta} \left( \mathbf{T}_t^i \mid \mathbf{T}_t^{<i}, \mathcal{T}_s \right)$$

这一设计使得模型天然支持多条件推理——给定文本生成 HOI 序列、给定 HOI 序列生成文本描述、以及给定部分 HOI 序列进行预测或插值——而无需为每个任务训练独立模型。LLM 的序列推理能力与分解式码本的低复杂度表示形成协同效应：LLM 负责长程语义连贯性，分解式标记器负责物理合理性，二者共同支撑了双向生成的高质量输出。

---

**证据强度评估**：上述三项 changed slots 均有消融实验（Table 3）和主实验结果（Table 1, Table 4）的直接支撑，置信度在 0.9–0.95 之间。HOI 分解式 VQ-VAE 的 23% 性能增益与几何损失的穿透抑制效果构成了因果链条的核心实证基础。需注意，LLM 规模（220M）对长序列连贯性的影响尚未通过更大模型的对比实验验证，这一点的泛化结论需要手动核实。

HOIGPT 构建了一个统一的双向 3D 手-物交互（HOI）与文本生成框架，其核心设计思想是将 HOI 运动序列与自然语言映射到同一语言模型的标记空间中。如 Figure 2 所示，整个 pipeline 由三个关键模块串联构成：**HOI 编码器**负责将原始运动序列压缩为紧凑的潜在表示，**HOI 分解式 VQ-VAE 标记器**将该表示量化为离散标记，**语言模型**则自回归地处理文本与 HOI 标记的联合序列，实现双向转换。

![[assets/figures/papers/paper_list_l25_HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Mode/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the HOIGPT framework for bi-directional hand-object interaction (HOI) generation and understanding. The input sequence (left) includes both text and HOI sequences, processed by the text tokenizer and HOI encoder, respectively. The HOI encoder uses an HOI Tokenizer to decompose HOI sequences into object, left hand, and right hand tokens. The language model takes both text and HOI tokens to generate the output sequence, which includes both text descriptions and generated HOI sequences. This design enables seamless integration of text and HOI data for tasks like motion prediction, description, and completion*

### 输入输出流

框架接受两种模态的输入：文本描述（如“用右手拿起杯子”）和 HOI 运动序列。HOI 运动序列由物体姿态 $\mathcal{O} = (\tau_o, \phi_o, \alpha_o)$ 与左右手姿态 $\mathcal{H} = (\tau, \phi)$ 拼接而成，即 $X_s = \mathsf{concat}(\mathcal{O}, \mathcal{H}_l, \mathcal{H}_r)$，其中物体姿态包含全局位置、6D 旋转和关节角度，手部姿态基于 MANO 参数导出。文本经标准文本分词器处理后，与 HOI 标记一同送入语言模型。

输出同样可以是文本或 HOI 序列，取决于任务方向：
- **文本到 HOI 生成**：输入文本描述，输出 HOI 运动标记，经 HOI 解码器重建为连续运动序列。
- **HOI 到文本生成**：输入 HOI 运动序列，输出描述性文本标记。
- **HOI 补全**：输入部分 HOI 序列（如仅物体运动），输出完整的手部运动。

### 模块关系与数据流

**HOI 编码器**（Sec. 3.4）采用三个并行的特征提取器：手部运动编码器、物体运动编码器以及基于 PointNet 的物体点云编码器。点云特征的引入为物体几何形状提供了显式表征，是后续几何约束的基础。

**HOI 分解式 VQ-VAE**（Sec. 3.3, Figure 3）是本框架的核心创新。与传统的联合 VQ-VAE（单一码本）不同，HOIGPT 将手部与物体的潜在特征分别通过独立的码本进行量化——物体码本和手部码本各自包含 512 个离散标记。这种分解策略将标记空间复杂度从指数级降至线性级，是模型能够高效学习长序列 HOI 的关键。量化后的手部和物体标记组合形成 HOI 潜在码，再经物体解码器和手部解码器重建完整序列。解码过程中，物体运动首先被重建，手部运动则以预测的物体运动为条件生成：$\hat{X}_s = \mathcal{D}((\hat{\mathbf{z}} + \mathbf{c}_o) \vert \mathcal{D}_o(\hat{\mathbf{z}}_o + \mathbf{c}_o))$。

**语言模型**（Sec. 3.2）选用 Flan-T5-Base（220M 参数），以自回归方式最大化输出标记的对数似然：
$$\mathcal{L}_{lm} = - \sum_{i=0}^{L_t-1} \log p_{\theta} \left( \mathbf{T}_t^i \mid \mathbf{T}_t^{<i}, \mathcal{T}_s \right)$$
其中 $\mathcal{T}_s$ 为输入标记序列，$\mathbf{T}_t$ 为目标输出序列。这种统一的序列建模方式使 HOIGPT 天然支持多任务学习——文本生成、运动生成、运动补全等任务共享同一组模型权重，仅通过改变输入输出标记的顺序即可切换任务。

### 物理合理性保障

框架在 VQ-VAE 训练阶段引入了三项几何约束损失（Sec. 3.5），确保生成序列的物理合理性：
- **穿透损失** $\mathcal{L}_{pen}$：惩罚手部顶点穿透物体表面的程度。
- **接触损失** $\mathcal{L}_C$：强制手部关节在接触前保持在物体表面距离 $\phi$ 以内。
- **接触区域损失** $\mathcal{L}_R$：对齐真实与重建的接触区域，约束手部顶点不远离物体表面。

三项损失加权求和构成几何损失 $\mathcal{L}_{geo} = \lambda \mathcal{L}_{pen} + \beta \mathcal{L}_C + \gamma \mathcal{L}_R$，与标记器重建损失 $\mathcal{L}_{tok}$ 联合优化。消融实验（Table 3）证实，移除几何损失会显著增加穿透体积并降低文本描述准确度，验证了该设计的必要性。

### 方法定位

相较于现有方法，HOIGPT 在三个关键维度上实现了差异化设计：

| 设计维度 | 基线方法 | HOIGPT 方案 |
|---------|---------|------------|
| HOI 标记化 | 联合 VQ-VAE（如 **MotionGPT** Jiang et al., NeurIPS 2023） | 手-物分解式 VQ-VAE，独立码本 |
| 生成框架 | 扩散模型（如 **DiffH2O** Christen et al., arXiv 2024） | 基于 LLM 的自回归模型 |
| 物理约束 | 无专门几何损失（如 **Text2HOI**） | 穿透 + 接触 + 接触区域三项几何损失 |

这种“分解式标记化 + LLM 序列推理 + 几何约束”的组合，使 HOIGPT 首次在统一的框架内实现了文本与 3D HOI 序列之间的双向高质量生成。

### 3.1 HOI 运动序列的参数化

HOIGPT 将手-物体交互（HOI）序列建模为手部姿态与物体姿态的联合表示。物体姿态 $\mathcal{O}$ 由三个分量构成：

$$\mathcal{O} = (\tau_o, \phi_o, \alpha_o)$$

其中 $\tau_o$ 为全局 3D 位置，$\phi_o$ 为 6D 旋转表示，$\alpha_o$ 为关节角度（针对铰接物体）。手部姿态 $\mathcal{H}$ 基于 MANO 参数模型导出，表示为：

$$\mathcal{H} = (\tau, \phi)$$

其中 $\tau$ 为手部全局位置，$\phi$ 为 6D 旋转。完整的 HOI 运动序列 $X_s$ 由物体、左手和右手姿态拼接而成：

$$X_s = \mathsf{concat}(\mathcal{O}, \mathcal{H}_l, \mathcal{H}_r)$$

这一参数化方案将高维 HOI 序列压缩为紧凑的向量表示，为后续标记化提供了结构化输入。

### 3.2 语言模型自回归框架

HOIGPT 采用预训练语言模型 Flan-T5-Base（220M 参数）作为统一的序列推理引擎。给定输入标记序列 $\mathcal{T}_s$，模型自回归地预测输出标记序列 $\mathbf{T}_t$，训练目标为最大化对数似然：

$$\mathcal{L}_{lm} = - \sum_{i=0}^{L_t-1} \log p_{\theta} \left( \mathbf{T}_t^i \mid \mathbf{T}_t^{<i}, \mathcal{T}_s \right)$$

该框架将文本与 HOI 标记统一在同一标记空间中，使模型能够执行文本→HOI 生成、HOI→文本描述、HOI 补全等多种任务，无需任务特定的架构修改。

### 3.3 HOI 分解式 VQ-VAE 标记器

HOIGPT 的核心创新在于 HOI 分解式 VQ-VAE 标记器，其关键设计是将手与物体的码本分离。编码器包含三个特征提取器：手部运动特征提取器、物体运动特征提取器以及基于 PointNet 的物体点云特征提取器。各模态特征经独立编码后，分别通过手部码本与物体码本进行量化，码本大小均为 512。

解码阶段，物体运动解码器 $\mathcal{D}_o$ 首先从量化物体特征 $\hat{\mathbf{z}}_o$ 重建物体姿态，随后 HOI 解码器 $\mathcal{D}$ 以预测的物体运动为条件，结合全部潜特征生成最终序列：

$$\hat{X}_s = \mathcal{D}((\hat{\mathbf{z}} + \mathbf{c}_o) \vert \mathcal{D}_o(\hat{\mathbf{z}}_o + \mathbf{c}_o))$$

其中 $\hat{\mathbf{z}}$ 为所有量化特征，$\mathbf{c}_o$ 为物体条件编码。这种分解式设计将标记空间复杂度从联合码本的指数级降至线性级，是性能提升的核心因果机制。

### 3.4 标记器损失函数

标记器的训练目标由重建误差与嵌入损失组成，分解应用于物体、左手、右手三个模态：

$$\mathcal{L}_{\mathrm{tok}} = |X - \hat{X}|_1 + \alpha \sum_i^I |\mathbf{z}_i - \mathrm{sg}[\hat{\mathbf{z}}_i]|_2^2, \quad I \in \{o, l, r\}$$

其中 $\mathrm{sg}[\cdot]$ 为停止梯度算子，$\alpha$ 为嵌入损失权重。首项 L1 损失保证序列重建精度，次项拉近编码器输出与码本嵌入的距离。

### 3.5 几何约束损失

为保障生成序列的物理合理性，HOIGPT 引入三项几何正则化损失。

**穿透损失** 惩罚手部顶点侵入物体内部的体积：

$$\mathcal{L}_{pen} = \frac{1}{|\mathcal{P}_{\mathrm{in}}^o|} \sum_{p \in \mathcal{P}_{\mathrm{in}}^o} \min_i \|p - \hat{V}_i\|_2^2$$

其中 $\mathcal{P}_{\mathrm{in}}^o$ 为穿透物体表面的手部顶点集合，$\hat{V}_i$ 为物体表面顶点。

**接触损失** 确保手部关节在接触前保持在物体表面距离 $\phi$ 以内：

$$\mathcal{L}_C = \sum_i D(\hat{J}_i^o), \quad \forall D(\hat{J}_i^o) \leq \phi$$

其中 $D(\cdot)$ 为到物体表面的有符号距离函数，$\hat{J}_i^o$ 为手部关节位置。

**接触区域损失** 对齐真实与重建的接触区域，并约束手部顶点不远离物体表面：

$$\mathcal{L}_R = \sum_i \|\Phi(P_i^o) - \Phi(\hat{P}_i^o)\|_2 + D(\hat{P}_i^o), \quad \forall D(P_i^o) < \tau$$

其中 $\Phi(\cdot)$ 为接触区域特征，$\tau$ 为接触距离阈值。

三项几何损失的加权和构成几何约束：

$$\mathcal{L}_{geo} = \lambda \mathcal{L}_{pen} + \beta \mathcal{L}_C + \gamma \mathcal{L}_R$$

最终训练目标为几何损失与标记器损失之和：

$$\mathcal{L} = \mathcal{L}_{geo} + \mathcal{L}_{tok}$$

消融实验证实，移除几何损失会导致穿透体积显著增加，同时降低文本描述准确度，验证了物理约束对生成质量的关键作用。

## 实验与关键发现

### 实验设置概要

HOIGPT 的训练与评估基于 **ARCTIC** 和 **GRAB** 两个数据集，测试集包含 500 个序列，训练集约 5.6k 个序列。HOI 标记器的码本大小统一设为 512（手部和物体），语言模型采用 **Flan-T5-Base**（220M 参数）。所有生成结果均汇报 95% 置信区间，来自 20 次独立运行，确保统计可靠性。

### 文本到 HOI 生成：主结果

Table 1 展示了文本到 HOI 生成任务上与现有方法的全面对比。HOIGPT 在所有核心指标上均取得最优性能：

![[assets/figures/papers/paper_list_l25_HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Mode/figures/004_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art on HOI generation. The arrows (→) indicate that closer to real is desirable. The best performance are highlighted in bold*

- **FID 达到 3.29 ± 0.54**，相较于先前最佳方法（如 **T2MGPT**, Zhang et al., CVPR 2023）降低 2.56，表明生成分布与真实分布的高度一致性。
- **Diversity** 和 **MModality** 指标同样领先，说明模型不仅能生成高质量序列，还能保持丰富的多样性。
- **R Precision (Top 3)** 和 **MMDist** 的显著优势验证了生成动作与输入文本之间的强语义对齐。
- 在物理合理性指标 **IV**（穿透体积）上，HOIGPT 也优于所有基线，包括扩散模型方法 **DiffH2O**（Christen et al., arXiv 2024），证明几何约束损失的有效性。

值得注意的是，**Text2HOI** 和 **T2MGPT** 等基线方法虽然在运动生成领域表现良好，但在手物交互场景中由于缺乏专门的物理建模，FID 和 IV 均显著劣于 HOIGPT。

### HOI 预测与插值

Table 2 展示了 HOI 预测和插值任务的结果。HOIGPT 在 **FID**、**Diversity**、**ADE**（平均位移误差）和 **FDE**（最终位移误差）上均优于 **MotionGPT**（Jiang et al., NeurIPS 2023）。具体而言：

![[assets/figures/papers/paper_list_l25_HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Mode/figures/005_Table_2.jpg]]
*Table 2: Comparison on HOI prediction and HOI interpolation*

- 在预测任务上，FID 达到 4.08，相较于 MotionGPT 有明显降低。
- 在插值任务上，同样展现出更低的误差和更高的生成质量。

这验证了 HOI 分解式标记器在时序建模上的优势——分离手与物体码本使得模型能更精确地捕捉交互动态，而非将其混淆在单一表示中。

### HOI 到文本生成

Table 4 对比了 HOI 到文本生成任务。HOIGPT 的 **R Precision (Top 3)** 达到 48.43，相对先前最佳方法 **TM2T**（Guo et al., ECCV 2022）提升 **+2.01%**。**MMDist** 同样取得最优，表明生成描述与真实 HOI 序列的语义一致性更强。这一结果证明，LLM 的双向序列推理能力使模型不仅擅长从文本生成动作，也能准确理解动作并生成自然语言描述。

![[assets/figures/papers/paper_list_l25_HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Mode/figures/007_Table_4.jpg]]
*Table 4: Comparison of HOI to text generation approaches*

### 消融分析：标记器设计与几何约束

Table 3 的消融实验揭示了两个关键设计的作用：

![[assets/figures/papers/paper_list_l25_HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Mode/figures/006_Table_3.jpg]]
*Table 3: Ablation on tokenizer design and geometric constraints*

1. **HOI 分解式 VQ-VAE vs. 朴素 VQ-VAE**：引入手-物体分解码本后，生成性能提升 **23%**。朴素 VQ-VAE 将手和物体混合量化，导致码本空间复杂度高、标记效率低；分解式设计通过分离码本大幅降低了学习难度。
2. **几何约束损失**：移除穿透损失 $\mathcal{L}_{pen}$、接触损失 $\mathcal{L}_C$ 和接触区域损失 $\mathcal{L}_R$ 后，穿透体积显著增加，同时文本到动作的 R Precision 下降，说明物理合理性与语义准确性之间存在耦合——物理上不合理的交互会导致文本描述偏离真实语义。

### 失败模式与局限性

尽管 HOIGPT 在定量指标上全面领先，仍存在以下局限：

- **数据集覆盖有限**：仅在 ARCTIC 和 GRAB 上训练，物体类别和交互类型受限，对开放词汇场景（如未见物体、新颖交互）的泛化能力尚未验证。
- **模型规模约束**：LLM 使用 220M 参数的 Flan-T5-Base，更大模型可能进一步提升长序列连贯性，但会带来计算开销。
- **感知依赖**：当前依赖完整物体点云作为输入，实际部署需额外感知模块，未探索从单目 RGB 端到端生成的方法。
- **鲁棒性未充分评估**：在严重遮挡或部分可观测场景下的表现尚不明确，安全性评估缺失。

### 关键图表结论

- **Table 1**：HOIGPT 在文本到 HOI 生成的所有维度（质量、多样性、语义匹配、物理合理性）上均达到 SOTA，FID 相对最优基线降低 2.56。
- **Table 2**：在 HOI 预测与插值任务上，HOIGPT 的时序建模精度显著优于 MotionGPT。
- **Table 3**：消融实验证实分解式标记器是性能核心驱动力（+23%），几何损失对物理合理性和语义准确性均有贡献。
- **Table 4**：HOI 到文本生成任务上，R Precision 相对提升 +2.01%，验证了双向统一架构的有效性。

![[assets/figures/papers/paper_list_l25_HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Mode/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of HOIGPT for HOI completion. HOIGPT is designed for multiple tasks including HOI interpolation (top) and HOI prediciton (bottom), the orange line indicts the input HOI sequence*

## 定位与知识库关联

### 1. 与现有基线的结构关系

HOIGPT 的核心定位是填补 3D 手-物交互（HOI）领域中**双向生成与理解统一框架**的空白。现有方法可大致归为三条技术路线，HOIGPT 与它们的关系如下：

**（1）单向生成模型：Text2HOI 与 DiffH2O**

Text2HOI 和 **DiffH2O**（Christen et al., arXiv 2024）均采用扩散模型实现文本到 HOI 的单向生成，缺乏对 HOI 序列的语言理解能力。HOIGPT 将生成框架从扩散模型替换为基于 LLM 的自回归模型，同时引入双向能力（HOI→文本），从根本上改变了任务范式：不再将 HOI 生成视为条件去噪过程，而是视为序列到序列的 token 预测问题。这一转变使得模型可以同时处理文本到 HOI 生成、HOI 补全和 HOI 字幕等多任务。

**（2）运动-语言模型：T2MGPT、MotionGPT 与 TM2T**

**T2MGPT**（Zhang et al., CVPR 2023）和 **MotionGPT**（Jiang et al., NeurIPS 2023）将 LLM 引入人体运动生成，**TM2T**（Guo et al., ECCV 2022）则实现运动到文本的生成。这些方法证明了 LLM 在运动模态上的可行性，但它们仅处理人体运动，未涉及手-物交互的复杂联合空间。HOIGPT 继承了“LLM + VQ-VAE tokenizer”的架构范式，但针对 HOI 的特殊性做了关键改造：

- **标记化策略**：从单一码本（联合 VQ-VAE）升级为 HOI 分解 VQ-VAE，分离手与物体码本。这一改造将标记空间复杂度从指数级降至线性加和，是性能提升 23%（消融实验，Table 3）的直接原因。
- **几何约束**：引入穿透损失 $\mathcal{L}_{pen}$、接触损失 $\mathcal{L}_C$ 和接触区域损失 $\mathcal{L}_R$，解决了纯运动模型忽略物理合理性的问题。移除几何损失会导致穿透体积增加和文本描述准确度下降（Sec. 4.5）。

**（3）方法谱系定位**

HOIGPT 处于 **LLM 驱动的多模态运动生成** 与 **物理约束的 HOI 建模** 两条技术路线的交汇点。其上游是 MotionGPT 等运动-语言模型，下游可延伸至端到端视觉-HOI 生成和交互式推理系统。

### 2. 适用边界与约束条件

**（1）数据依赖边界**

模型在 ARCTIC 和 GRAB 两个数据集上训练和评估（约 5.6k 训练序列，500 测试序列），物体类别和交互类型有限。对于开放词汇场景或未见物体类别的泛化能力尚未验证，这是一个明确的适用边界。

**（2）输入模态约束**

当前方法依赖完整物体点云作为输入，通过 PointNet 编码。在实际部署中，这意味着需要额外的感知模块（如深度相机或 3D 重建）来获取点云。模型尚未探索端到端从单目 RGB 输入生成 HOI 的路径，这限制了其在视觉输入场景下的直接应用。

**（3）模型规模约束**

使用的语言模型为 Flan-T5-Base（220M 参数），属于较小规模的 LLM。更大模型（如 LLaMA-13B）可能进一步提升长序列连贯性和语义理解质量，但会增加计算开销。当前规模是性能与效率的折中选择。

**（4）物理合理性边界**

几何约束通过穿透、接触和接触区域三项损失实现，但这是在 VQ-VAE 标记器训练阶段施加的约束，而非在 LLM 推理阶段实时校验。这意味着 LLM 生成的 token 序列经过解码器重建后，物理合理性依赖于解码器的泛化能力，而非 LLM 本身对物理规律的显式建模。

### 3. 局限与开放问题

**（1）已确认的局限**

- **数据覆盖有限**：仅在 ARCTIC 和 GRAB 上训练，交互类型和物体多样性不足，泛化到开放场景的能力待验证。
- **点云依赖**：需要完整物体点云输入，实际场景中需要额外感知模块，未探索端到端视觉方案。
- **部分可观测场景未评估**：在严重遮挡等条件下的鲁棒性和安全性缺乏实验支撑。
- **LLM 规模受限**：Flan-T5-Base 的 220M 参数可能成为长序列生成质量的瓶颈。

**（2）开放研究问题**

- **可扩展训练**：如何在更广泛、更多样的物体和交互数据集上实现可扩展的训练，是通向通用 HOI 模型的关键。
- **更大规模 LLM 的集成**：结合 LLaMA-13B 等更大模型是否能显著提升文本到 HOI 的语义理解和长序列生成质量？
- **视觉端到端**：当仅给定单目 RGB 输入时，模型能否通过预测点云或直接编码视觉特征来实现交互感知与生成？
- **交互式推理**：双向模型能否支持交互式推理，例如根据语言反馈实时调整动作序列？这需要探索闭环控制和在线规划的结合。
- **物理约束的推理时集成**：能否在 LLM 推理阶段引入物理合理性校验机制，而非仅在标记器训练时施加约束？

### 4. 知识库定位总结

HOIGPT 在知识库中的定位是 **首个统一 HOI 双向生成与理解的 LLM 基框架**。其核心贡献——HOI 分解 VQ-VAE 和几何约束损失——解决了 HOI 标记效率低和物理合理性差两个关键瓶颈。该方法桥接了运动-语言模型和物理约束 HOI 建模两条技术路线，为后续研究（如视觉端到端 HOI 生成、交互式 HOI 推理）提供了可扩展的基础架构。

## 原文 PDF

![[paperPDFs/CVPR_2025/HOIGPT_Learning_Long_Sequence_Hand_Object_Interaction_with_Language_Models.pdf]]

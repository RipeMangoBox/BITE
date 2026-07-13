---
title: Multimodal Semantic Bias Mitigation for Diverse Text-To-3D Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multimodal_Semantic_Bias_Mitigation_for_Diverse_Text_To_3D_Generation.pdf
project_link: null
code_link: null
aliases:
- MSBMF
- MSBMDT3G
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过文本到3D评估模型的反向传播，计算生成质量相对于输入提示中每个词的梯度，量化词级偏置贡献，并据此构造语义多样化且稳定的文本-3D对进行模型微调。
primary_logic: 利用评估模型梯度作为词级偏置的代理，指导构建语义丰富的训练样本，以不牺牲原有能力的前提下缓解内在偏置，提升文本到3D生成的多样性和一致性。
claims:
- TRELLIS存在对不同提示词的偏置过拟合，对复杂提示（如Fantastical、Grouped）理解差，见Figure 2的梯度分布与质量直方图。
- 所提方法在所有MATE-3D和T3 Bench的8+3个提示类别上均取得最佳平均质量/对齐分数，显著超越所有基线（包括原TRELLIS-text）。
- 通过词级梯度分析（Figure 7），微调后的模型对各提示词的注意力分布更加均匀，有效缓解了过度聚焦少数词的问题，扩展了语义信息。
- MATE-3D 上 Overall Quality (Basic) = 8.19
---

# Multimodal Semantic Bias Mitigation for Diverse Text-To-3D Generation

> [!tip] 核心洞察
> 利用评估模型梯度作为词级偏置的代理，指导构建语义丰富的训练样本，以不牺牲原有能力的前提下缓解内在偏置，提升文本到3D生成的多样性和一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向多样化文本到三维生成的多模态语义偏置缓解 |
| 英文题名 | Multimodal Semantic Bias Mitigation for Diverse Text-To-3D Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Min_Multimodal_Semantic_Bias_Mitigation_for_Diverse_Text-To-3D_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Multimodal Semantic Bias Mitigation Framework |
| Dataset | MATE-3D, T3 Bench |

> [!tip] 效果简介
> - MATE-3D 上，Overall Quality (Basic) 8.19 vs 7.39 (+0.80)；Overall Quality (Fantastical) 6.95 vs 6.24 (+0.71)。
> - T3 Bench 上，Average Alignment Score (Single Object) 50.2 vs 44.8 (+5.4)；Average Alignment Score (Multiple Objects) 37.5 vs 28.5 (+9.0)。

## 概要

现有文本到3D大模型在生成质量上取得了显著进展，但其内部存在一种尚未被系统研究的**跨模态语义偏置**：模型对提示中的特定词汇过度聚焦，导致对复杂、非典型描述（如奇幻物体、多对象组合）的理解能力显著下降。以骨干模型 **TRELLIS**（Xiang et al., CVPR 2025）为例，其在MATE-3D基准上的定量分析表明，不同提示词的平均梯度分布极不均匀，且“Fantastical”和“Grouped”等类别的质量分数直方图呈现明显的低分聚集（Figure 2），这直接制约了文本到3D生成在多样化输入下的可控性。

针对上述瓶颈，本文提出一种**多模态语义偏置缓解框架**。其核心思路是：利用预训练的文本到3D评估模型（MATE-3D）作为偏置探测器，通过反向传播计算生成质量分数对各词嵌入的梯度，量化词级偏置贡献；进而以高影响词与低影响词为锚点，借助GPT-4构造语义多样化且稳定的文本-3D对，对骨干模型进行微调。该方法在不牺牲原有生成能力的前提下，缓解了模型对少数词的过度依赖，扩展了语义信息的覆盖范围。

实验结果表明，该方法在MATE-3D的全部8个提示类别上均取得最优平均质量分数（如Basic类别从7.39提升至8.19，Fantastical类别从6.24提升至6.95），在T3 Bench的单对象与多对象场景下分别实现+5.4和+9.0的对齐分数增益（Table 1, Table 2）。词级梯度可视化进一步证实，微调后的模型对各提示词的注意力分布更加均匀，有效抑制了偏置过拟合现象（Figure 7）。



### 文本到三维生成的发展与瓶颈

文本到三维（Text-to-3D）生成旨在从自然语言描述直接合成三维数字资产，近年来借助扩散模型和大规模预训练取得了显著进展。以 **DreamFusion**（Poole et al., ICLR 2022）为代表的基于2D扩散先验的优化方法，以及 **TRELLIS**（Xiang et al., CVPR 2025）等大规模前馈生成模型，已能产出具有跨视角一致性的三维内容。然而，这些模型在实际部署中暴露出一个深层瓶颈：**跨模态语义偏置**。

所谓跨模态语义偏置，是指文本到3D模型在理解输入提示时，会过度聚焦于少数“头部”词汇——通常是描述物体类别或显著属性的词——而忽视修饰性、空间性或动作性的“尾部”词汇。这一现象导致模型在面对复杂、非典型或富于想象力的描述时，生成质量显著下降。如 **Figure 2** 所示，骨干模型 TRELLIS 在 MATE-3D 基准测试的不同提示类别上表现出明显的质量分化：对“Fantastical”（奇幻类）和“Grouped”（组合类）等复杂提示的理解能力远弱于基础类别，其词级梯度分布直方图直观地揭示了模型对特定提示词的过拟合。

### 现有偏置缓解方案的缺口

当前主流的文本到3D生成方法——无论是基于优化的 **Magic3D**（Lin et al., CVPR 2023）、**SJC**（Wang et al., CVPR 2023），还是前馈式的 **One-2-3-45++**（Liu et al., CVPR 2024）、**3DTopia**（Hong et al., arXiv 2024）——在设计上均未显式考虑训练数据或模型内部的语义偏置问题。这些方法通常直接使用原始文本-3D对进行训练，缺乏对输入提示中词级贡献差异的感知与调控机制，因此无法主动缓解因偏置导致的生成退化。

更关键的是，现有工作缺少一个系统性的偏置定位工具。尽管文本到3D评估模型（如 MATE-3D）已被用于衡量生成质量，但尚未有人将其反向传播的梯度信息作为词级偏置的代理信号，进而指导训练数据的语义丰富化。这一方法论缺口使得“在不牺牲原有能力的前提下提升模型对多样化输入的泛化性”成为一个待解难题。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **多模态语义偏置缓解框架**。其核心洞察在于：文本到3D评估模型的梯度可以作为词级偏置贡献的可靠代理——梯度幅值高的词即为模型过度依赖的“头部”词，而梯度幅值低的词则是模型容易忽略的“尾部”词。基于这一洞察，方法通过三个关键步骤实现偏置缓解：

1. **偏置定位**：利用预训练的文本到3D评估模型 MATE-3D，计算生成质量分数对各词嵌入的梯度均值，量化每个提示词的偏置贡献。
2. **语义感知丰富化**：识别高影响词（$w_h$）与低影响词（$w_l$），借助 GPT-4 在保留核心语义的前提下生成多样化的上下文提示，扩展语义环境。
3. **视觉感知筛选**：为丰富后的提示生成对应三维网格，并通过人类偏好排名模型 HPSv2 选择语义忠实的高质量样本，构建 many-to-many 的文本-3D对用于微调。

这一框架在保持骨干模型跨视角一致性的同时，有效扩展了其对复杂、非典型提示的理解能力，为文本到3D生成的多样化可控性提供了新的技术路径。



## 核心方法与创新机理

### 问题洞察：大模型中的跨模态语义偏置

当前文本到3D大模型（如 **TRELLIS** (Xiang et al., CVPR 2025)）虽然具备强大的跨视角一致性生成能力，却存在一个被忽视的内在缺陷——**跨模态语义偏置**。具体而言，模型在理解输入提示时，会过度聚焦于少数“头部”词汇，而忽略其他同样承载语义信息的“尾部”词汇。如 Figure 2 所示，TRELLIS 在 MATE-3D 基准上对不同提示词的梯度分布极不均匀，对“Fantastical”、“Grouped”等复杂提示类别的质量评分显著偏低。这种偏置导致模型在面对非典型、多样化描述时生成质量急剧下降，无法满足可控生成的实际需求。

### 核心洞察：以评估模型梯度作为词级偏置的代理

本工作的核心洞察在于：**利用预训练的文本到3D评估模型（MATE-3D）的反向传播梯度，量化每个输入词对生成质量的偏置贡献**。具体而言，计算评估模型预测的质量分数对各词嵌入的梯度绝对值之和：

$$e_i' = \sum \left| \frac{\partial q}{\partial e_i} \right|, \quad q \in \{q_l, q_g\}$$

其中 $q_l$ 为特定提示下的局部质量分数，$q_g$ 为全局质量分数。梯度幅值大的词即为模型“过度聚焦”的高影响词（$w_h$），梯度幅值小的词则为被“忽略”的低影响词（$w_l$）。这一机制将隐式的语义偏置转化为可量化的词级信号，为后续的偏置缓解提供了精确的优化方向。

### 关键创新一：语义感知的提示丰富化

基于词级偏置定位结果，本文提出**语义感知的提示丰富化**策略。与直接使用原始单一提示进行训练不同，该方法利用 GPT-4 在保留高影响词（$w_h$）和低影响词（$w_l$）的前提下，批量生成多样化上下文环境的变体提示。这一策略的核心作用在于：通过扩展语义环境，迫使模型学习关注更全面的文本信息，而非仅依赖少数“捷径”词汇。Table 3 的消融实验证实，仅使用 $w_h$ 进行提示丰富已带来显著改善，而加入 $w_l$ 可进一步增强语义多样性，提升模型对尾部词汇的理解能力。

### 关键创新二：视觉感知的网格筛选

为构建高质量的文本-3D训练对，本文进一步引入**视觉感知的网格筛选**机制。具体而言，使用 Cascade Flow Diffusion (CFD) 为多样化提示生成对应的三维网格，并采用 **HPSv2** 人类偏好排序模型筛选出语义忠实且质量上佳的样本，形成 many-to-many 的文本-3D配对。这一设计确保了微调数据的视觉质量与语义一致性，避免低质量样本引入新的噪声偏置。

### 关键创新三：偏置感知的困难样本采样

在微调阶段，本文提出**基于词级偏置的困难样本采样**策略，优先选择偏置程度高的文本-3D对进行训练。Table 4 显示，该策略可将总生成时间从约25小时大幅缩减至约10.5小时，同时保持优于传统评估分数采样的性能。这验证了偏置定位信号在提升数据效率方面的实用价值。

### 关键创新四：轻量级去偏微调框架

上述模块构成了一个**即插即用的去偏微调框架**：无需修改骨干模型架构，仅通过注入语义稳健且多样化的文本-3D对，即可缓解 TRELLIS 的跨模态偏置。Figure 7 的可视化结果表明，微调后的模型对各提示词的注意力分布更加均匀，有效扩展了语义信息覆盖范围。值得注意的是，Table 4 进一步揭示，即使完全省略微调阶段，仅用丰富后的中间图像引导 TRELLIS-image 的 image-to-3D 流程，仍能获得优于原始 TRELLIS-text 的结果——这说明语义丰富化本身已构成一种有效的去偏手段。

### 与现有方法的本质区别

现有文本到3D方法（如 **DreamFusion** (Poole et al., ICLR 2022)、**ProlificDreamer** (Wang et al., NeurIPS 2023)）主要聚焦于提升生成质量或一致性，但均未显式建模和缓解模型内部的语义偏置。本工作首次将偏置定位、语义丰富化、视觉筛选和偏置感知训练整合为闭环框架，在不牺牲原有能力的前提下，系统性地提升了模型对多样化文本输入的泛化能力。



本文提出的多模态语义偏置缓解框架围绕一个核心洞察展开：当前文本到3D大模型（如 **TRELLIS**，Xiang et al., CVPR 2025）存在跨模态语义偏置，对提示中的特定词过度聚焦，导致对复杂、非典型描述的生成质量下降。该框架通过“定位—丰富—微调”三阶段流水线，在不牺牲原有能力的前提下缓解这一内在偏置。

整个流水线如 Figure 3 所示，由四个关键模块串联构成：

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our method. Our method first uses the text-to-3D large model to generate examples, then localizes the bias with a 3D evaluation model. Finally, we qualify the bias and use it to guide the generation of text-3D pairs with diverse semantics to fine-tune the text-to-3D large model*

1. **偏置定位模块（Bias Localization Module）**：首先利用骨干文本到3D模型（TRELLIS）对给定提示集合生成一批三维资产。随后，引入预训练的文本到3D评估模型 **MATE-3D**，计算生成质量分数对各词嵌入的梯度，以梯度幅值作为词级偏置贡献的代理指标，从而量化哪些提示词是模型过度聚焦的“高影响词”（$w_h$）和哪些是模型几乎忽略的“低影响词”（$w_l$）。

2. **语义感知提示生成器（Semantic-aware Prompt Generator）**：基于上一步识别出的高/低影响词，调用 **GPT-4** 在保持核心语义不变的前提下，批量生成具有多样化上下文的新提示。这一步骤的关键在于：保留 $w_h$ 和 $w_l$ 作为语义锚点，但改变其周围的语境，从而扩展模型对同一核心语义在不同语言环境下的理解。

3. **视觉感知网格选择器（Visual-aware Mesh Selector）**：为多样化提示生成对应的三维网格。具体而言，使用 **CFD** 生成三维网格，并采用人类偏好排序模型 **HPSv2** 对生成结果进行语义忠实度和质量筛选，仅保留排序胜出的高质量样本，构造“多对多”的文本-3D对。

4. **骨干模型微调（Text-to-3D Backbone Fine-tuning）**：将新构造的语义稳健且多样化的文本-3D对注入原始监督信号中，对骨干模型 TRELLIS 进行微调。这一阶段的目标是使模型在保持原有生成能力的同时，提高对复杂、非典型提示的泛化能力。

整个框架的输入是原始文本提示集合和预训练的文本到3D大模型，输出是经过去偏微调后的生成模型。其因果调节旋钮在于：利用评估模型梯度作为词级偏置的代理，指导构建语义丰富的训练样本，从而在不引入额外推理开销的前提下提升文本到3D生成的多样性和一致性。



### 跨模态语义偏置的形式化

现有文本到3D大模型（如TRELLIS）在生成过程中存在内在偏置：模型对不同提示词的关注程度极度不均，过度聚焦于少数“头部”词，导致对复杂、非典型描述的理解能力显著下降（Figure 2）。本文将这一偏置形式化为评估模型估计值与理想期望值之间的差异：

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/003_Figure_2.jpg]]
*Figure 2: Quantitative results of TRELLIS on the text-to-3D benchmark MATE-3D [43]. As shown, TRELLIS has inherent bias. (a) Average grad of different prompt words on the MATE-3D benchmark. TRELLIS over-focuses on few certain prompt words. (b) Distribution histogram of the quality scores of TRELLIS for 8 different categories of text prompts on the MATE-3D benchmark. TRELLIS can understand the common “Basic” prompts, but has a poor understanding of complex prompts such as “Fantastical” and “Grouped”*

$$ \epsilon ( \hat { \phi } ) = \hat { \phi } - \phi \quad \text{(Eq. 1)} $$

其中 $\hat{\phi}$ 为评估模型的实际估计，$\phi$ 为理想期望值。这一偏置在文本到3D的跨模态映射中表现为：给定相同提示词，生成的三维资产质量在不同语义维度上波动剧烈。

### 偏置定位模块（Bias Localization Module）

为了将跨模态偏置定位到具体词级，本文引入预训练的文本到3D评估模型MATE-3D作为偏置探测器。该评估模型采用多任务超网络架构，对第 $i$ 个评估维度预测质量分数：

$$ \hat { q } _ { i } = \psi \left( F \left( x , t \right) | \pi \left( f _ { c } ^ { i } \right) \right) \quad \text{(Eq. 2)} $$

其中 $x$ 为生成的三维网格，$t$ 为输入文本提示，$F(x,t)$ 为多模态特征，$\pi(f_c^i)$ 为超网络生成的第 $i$ 个维度评估参数。

在此基础上，定义两种粒度的偏置度量：

- **局部偏置**：针对特定提示 $t_n$，生成一组三维网格 $\{x_n^D\}$ 的平均质量分数，反映模型对该提示的局部响应质量：

$$ q _ { l } = \frac { 1 } { | x _ { n } ^ { D } | } \sum _ { x _ { n } ^ { d } } q \quad \text{(Eq. 5)} $$

- **全局偏置**：在整个评估数据集 $\mathcal{X}$ 上的平均质量分数，反映模型的整体生成能力：

$$ q _ { g } = \frac { 1 } { | \mathcal { X } | } \sum _ { ( x , t ) \in \mathcal { X } } q \quad \text{(Eq. 6)} $$

### 词级梯度代理

核心洞察在于：评估模型对输入提示词嵌入的梯度大小，可以代理该词对生成质量的贡献程度。对每个词嵌入 $e_i$，计算其关于质量分数 $q$ 的梯度绝对值之和：

$$ e _ { i } ^ { \prime } = \sum \left| { \frac { \partial q } { \partial e _ { i } } } \right| , \quad q \in \{ q _ { l } , q _ { g } \} \quad \text{(Eq. 7)} $$

梯度值 $e_i'$ 越大，表明该词对评估分数的敏感度越高，即模型对该词存在更强的偏置依赖。通过反向传播，可精确定位每个提示中贡献最大的“高影响词”$w_h$ 和贡献最小的“低影响词”$w_l$。

### 语义感知丰富化模块（Semantic-aware Prompt Generator）

基于词级偏置定位结果，该模块利用GPT-4在保持核心语义的前提下，为高影响词和低影响词批量生成多样化的上下文环境。具体而言，固定 $w_h$ 和 $w_l$，通过LLM构造语义变体提示 $\{t_{n_c}\}$，使模型在微调过程中接触同一核心词在不同语境下的表达，从而缓解对特定词的过度聚焦。

### 视觉感知筛选模块（Visual-aware Mesh Selector）

为每个语义丰富化后的提示 $t_{n_c}$，使用CFD生成对应的三维网格候选集。随后引入人类偏好排序模型HPSv2，筛选出语义忠实度最高的高质量样本 $x^{win}$，构建新的文本-3D对 $\{x_{n_c}, t_n\}$。这一many-to-many的构建策略确保了训练数据的语义稳健性和视觉质量。

### 微调数据注入

最终，将原始监督信号与构造的语义多样化文本-3D对合并，对骨干模型TRELLIS进行微调。微调目标是在不牺牲原有生成能力的前提下，扩展模型对尾部提示词的理解，提升对复杂、非典型文本输入的可控生成质量。

### 补充图表

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/010_Figure_7.jpg]]
*Figure 7: Comparison of TRELLIS and our method for the gradient of all prompt words in the MATE-3D benchmark. Our method alleviates the bias of TRELLIS for certain prompt words and expands the semantic information*



## 实验与关键发现

### 主实验结果

为验证所提多模态语义偏置缓解框架的有效性，本文在 **MATE-3D** 与 **T3 Bench** 两个基准上进行了全面评估。MATE-3D 包含 160 个提示，覆盖 Basic、Refined、Complex、Fantastical、Grouped、Action、Spatial、Imaginative 共 8 个类别；T3 Bench 包含 300 个提示，按 Single Object、Single Object with Surroundings、Multiple Objects 三个维度划分。

**Table 1** 汇总了各方法在 MATE-3D 上的整体质量分数。以 TRELLIS-text 为骨干并施加本文微调策略后，在所有 8 个提示类别上均取得最优平均质量分数。其中 Basic 类别从基线 7.39 提升至 8.19（+0.80），Fantastical 类别从 6.24 提升至 6.95（+0.71），验证了方法对复杂、非典型描述的强泛化能力。对比其他基线，如 **One-2-3-45++**（Liu et al., CVPR 2024）和 **ProlificDreamer**（Wang et al., NeurIPS 2023），本文方法在各子类上均保持领先，最小提升幅度 0.12，最大 0.4，平均提升 0.19。

**Table 2** 呈现了 T3 Bench 上的对齐分数。在 Single Object 场景下，本文方法平均对齐分数为 50.2，较 TRELLIS-text 的 44.8 提升 5.4；在更具挑战的 Multiple Objects 场景下，从 28.5 提升至 37.5（+9.0），表明偏置缓解策略显著增强了模型对多对象语义关系的理解能力。

**Figure 4** 与 **Figure 5** 提供了定性对比。在 Fantastical 等幻想类对象生成场景中，基线方法常出现文本匹配失败（图中蓝色标注区域），而本文方法在保持跨视角一致性的同时，显著改善了语义对齐与几何纹理细节。

### 消融实验

**Table 3** 展示了提示生成策略的消融。仅使用高影响词（$w_h$）进行语义丰富已带来显著改善；进一步引入低影响词（$w_l$）可增强语义多样性，使模型更均衡地关注所有提示词，而非过度聚焦少数头部词。

**Table 4** 分析了计算成本与采样策略。基于词级偏置的困难样本采样可将总生成时间从约 25 小时压缩至约 10.5 小时，同时性能优于基于原始评估分数的采样。值得注意的是，即使完全省略微调阶段（w/o training），仅用丰富后的中间图像引导 TRELLIS-image 的 image-to-3D 流程，仍可获得优于原始 TRELLIS-text 的结果，验证了语义丰富化模块的独立价值。

### 偏置缓解的机理验证

**Figure 7** 对比了微调前后 MATE-3D 基准上所有提示词的梯度分布。原始 TRELLIS 对少数词呈现极高梯度，表明存在严重的注意力偏置；经本文方法微调后，梯度分布更加均匀，模型对尾部提示词的理解能力得到提升，有效扩展了可利用的语义信息。这一现象与 **Figure 6** 中词级偏置定位的可视化结果一致——通过评估模型梯度可精确识别导致生成质量下降的关键词。

### 局限与失败模式

尽管整体性能优异，本文方法仍存在若干局限。首先，训练与多样化样本生成耗时约 25 小时，虽可通过硬采样缩短至约 10.5 小时，但计算开销仍较大（Table 4）。其次，偏置定位效果依赖于预训练评估模型 MATE-3D 的质量，评估模型本身的偏置可能传播至后续流程。此外，语义丰富化步骤依赖 GPT-4，生成提示的多样性和覆盖率可能受限，影响微调上限。当前方法主要针对单文本生成多视角一致的三维资产，尚未涉及跨模态（如图像引导）或交互式生成的偏置缓解。

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/011_Table_4.jpg]]
*Table 4: Analysis for computation cost for enriched prompt numbers and training samples on MATE-3D. w/o training denotes we input the intermediate images generated by CFD to TRELLIS-image*

### 补充图表

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/006_Table_1.jpg]]
*Table 1: Qualitative comparisons on 160 prompts generated by MATE-3D. We calculate the average scores (in terms of overall quality) of each generative method on MATE-3D for comprehensive 3D quality evaluation. The best performance in each case is shown in bold*

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/008_Table_2.jpg]]
*Table 2: Qualitative comparisons on 300 prompts generated by*

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/009_Table_3.jpg]]
*Table 3: Ablation study for prompt generation on MATE-3D*

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparisons with TRELLIS-text. Our method gain a better performance in fantastic object generation scenes, offering better semantic-aligned results, marked in blue*

![[assets/figures/papers/paper_list_l2551_https_openaccess_thecvf_com_content_CVPR2026_html_Min_Multimodal_Semanti/figures/001_Figure_1.jpg]]
*Figure 1: Our method localize and mitigate biases in text-to-3D large models and generate both cross-view consistent and textaligned results*



## 定位与知识库关联

### 1. 与基线方法的关系

本文的工作建立在两类关键基线之上：**文本到3D生成模型**和**文本到3D评估模型**。在生成端，作者以 **TRELLIS**（Xiang et al., CVPR 2025）作为骨干模型，该模型以跨视角一致性和高质量结构化生成见长，是当前大规模文本到3D生成的代表性工作。与之对比的传统基线包括基于2D扩散先验的优化方法——**DreamFusion**（Poole et al., ICLR 2022）通过分数蒸馏采样（SDS）从2D扩散模型中提取3D先验，**Magic3D**（Lin et al., CVPR 2023）在此基础上实现了高分辨率生成，**SJC**（Wang et al., CVPR 2023）则通过分数雅可比链式法则改进优化过程。此外，**ProlificDreamer**（Wang et al., NeurIPS 2023）通过变分分数蒸馏（VSD）提升了生成多样性和保真度，**Consistent3D**（Wu et al., CVPR 2024）专注于跨视角一致性优化，**RichDreamer**（Qiu et al., CVPR 2024）强调细节丰富度。在直接生成范式中，**One-2-3-45++**（Liu et al., CVPR 2024）实现了快速的单图像到3D及文本到3D转换，**3DTopia**（Hong et al., arXiv 2024）基于混合扩散先验进行大规模生成。在评估端，本文依赖 **MATE-3D** 作为偏置定位的核心工具，该模型通过多任务超网络架构对生成3D资产进行多维度质量预测。

本文的核心贡献并非提出全新的生成架构，而是在现有文本到3D大模型的**训练范式层面**引入偏置感知的微调策略。与上述基线将文本-3D对视为无差别的监督信号不同，本文揭示了骨干模型对提示词中少数“头部词”的过度聚焦现象（见Figure 2），并据此构建了一个闭环的偏置定位-缓解框架。这种“以评估驱动生成优化”的思路，将文本到3D生成中的语义偏置问题从隐式的模型能力缺陷转化为可量化、可干预的词级贡献度问题。

### 2. 适用边界与假设条件

本方法的有效性受以下关键假设和边界条件约束：

- **评估模型质量依赖性**：偏置定位模块完全依赖MATE-3D评估模型的梯度信号来量化词级偏置贡献（$e_i' = \sum |\frac{\partial q}{\partial e_i}|$，见Eq. 7）。若评估模型本身存在系统性偏置（如对特定类别、材质或几何形态的倾向性评分），该偏置将通过梯度反向传播进入词级贡献度估计，进而污染语义丰富化阶段的高/低影响词识别。作者未对评估模型本身的偏置进行校准或消融分析，这一传播链路的稳健性需要进一步验证。

- **语义丰富化的语言模型上限**：语义感知提示生成器依赖GPT-4在保持核心语义（高影响词$w_h$和低影响词$w_l$）的前提下构造多样化上下文。GPT-4的生成多样性和语义覆盖率构成了微调数据质量的上限。对于超出语言模型知识边界的专业领域术语或罕见概念组合，生成的多样化提示可能流于表面变换，无法真正扩展语义空间。

- **视觉感知筛选的保真度约束**：视觉感知网格选择器采用CFD生成三维网格，并使用HPSv2排序模型筛选语义忠实的高质量样本。HPSv2作为人类偏好排序模型，其评分标准偏向符合人类审美习惯的生成结果，可能在筛选过程中过滤掉语义正确但视觉风格独特的样本，引入新的审美偏置。

- **计算开销与资源边界**：完整流程（包括多样化样本生成和微调）耗时约25小时，虽可通过困难样本硬采样压缩至约10.5小时（Table 4），但仍显著高于标准微调流程。这一开销限制了方法在资源受限场景（如边缘设备、快速原型迭代）中的直接应用。

- **场景边界**：当前方法针对单文本到多视角一致3D资产的生成场景设计，未涉及跨模态引导（如图像到3D、草图到3D）或交互式生成中的偏置问题。在多对象、多交互的复杂场景下，偏置可能表现为对象间关系的错误理解而非简单的词级过聚焦，现有框架对此类结构化偏置的捕获能力有限。

### 3. 局限性与待验证问题

**已确认的局限性：**

- 训练与多样化样本生成的计算开销较大（完整流程约25小时，压缩后约10.5小时），限制了方法的可扩展性和快速迭代能力（Table 4）。
- 偏置定位效果完全依赖预训练评估模型MATE-3D的质量，评估模型偏置的传播风险未得到量化控制。
- 语义丰富化步骤依赖GPT-4，提示多样性和覆盖率受限于语言模型能力边界。
- 当前方法仅覆盖单文本生成场景，未扩展到图像引导或交互式生成任务。

**开放问题：**

1. **跨架构泛化性**：该词级偏置定位与缓解框架能否推广到其他文本到3D大模型架构（如MVDream、Wonder3D、Instant3D等）？不同骨干模型的内在偏置模式可能存在结构性差异，词级梯度作为偏置代理的有效性是否具有架构不变性尚待验证。

2. **端到端去偏置学习**：当前方法将偏置定位与缓解解耦为两阶段流程（先评估、后微调）。能否将词级偏置度量直接嵌入训练目标函数，实现端到端的去偏置表示学习？这需要设计可微的偏置正则化项，使其在训练过程中动态调整模型对不同提示词的注意力分布。

3. **评估模型偏置的级联效应**：若评估模型本身存在偏置（如对不同类别倾向性评分），最终生成模型的去偏效果将受到何种影响？是否存在评估模型偏置与生成模型偏置的正交性假设，使得去偏过程不会因评估偏置而发生方向性偏差？

4. **复杂场景的结构化偏置**：在多对象、多交互场景下，偏置可能表现为对象间空间关系、属性绑定的错误理解，而非简单的词级过聚焦。现有词级梯度框架能否扩展为短语级或依存关系级的偏置度量，以捕获结构化语义偏置？

5. **轻量化去偏方案**：如何在资源受限场景下实现有效的去偏微调？是否存在基于Adapter、LoRA等参数高效微调方法的轻量方案，在不显著增加计算开销的前提下实现可比的去偏效果？



## 原文 PDF

![[paperPDFs/CVPR_2026/Multimodal_Semantic_Bias_Mitigation_for_Diverse_Text_To_3D_Generation.pdf]]

---
title: "DreamOmni2: Multimodal Instruction-based Generation and Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DreamOmni2_Multimodal_Instruction_based_Generation_and_Editing.pdf
project_link: null
code_link: "https://github.com/dvlab-research/DreamOmni2"
aliases:
- DreamOmni2
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: ① 三阶段数据合成流水线（特征混合→提取模型→编辑/生成数据构造）提供大规模高质量的多模态训练数据；② 在 DiT 中引入索引编码与位置编码偏移，使模型区分多张参考图像；③ 将 VLM 与生成/编辑模型联合训练，显著提升复杂指令理解能力。
primary_logic: 将编辑与生成统一为多模态指令驱动任务，通过构建覆盖具体对象与抽象属性的配对数据，并设计支持多图像输入的框架（索引编码、位置偏移、VLM 联合训练），使模型可根据文本与参考图像指令实现精确编辑与多样化生成。
claims:
- 特征混合方案在生成包含相同抽象属性或具体对象的图像对时，成功率和分辨率均优于 diptych 方法。
- 联合训练 VLM 使模型在 DreamOmni2 基准上的编辑/生成成功率显著提升（Scheme 4 最高）。
- 加入索引编码和位置编码偏移后，模型能够区分多张图像并避免像素混淆与 copy-paste 效应，性能大幅提高。
- DreamOmni2 在 DreamOmni2 基准的编辑和生成任务上全面超越现有开源模型，并达到或接近商业级模型 GPT-4o 和 Nano Banana 的水平。
---

# DreamOmni2: Multimodal Instruction-based Generation and Editing

> [!tip] 核心洞察
> 将编辑与生成统一为多模态指令驱动任务，通过构建覆盖具体对象与抽象属性的配对数据，并设计支持多图像输入的框架（索引编码、位置偏移、VLM 联合训练），使模型可根据文本与参考图像指令实现精确编辑与多样化生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | DreamOmni2：基于多模态指令的生成与编辑 |
| 英文题名 | DreamOmni2: Multimodal Instruction-based Generation and Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xia_DreamOmni2_Multimodal_Instruction-based_Generation_and_Editing_CVPR_2026_paper.html) · [Code](https://github.com/dvlab-research/DreamOmni2) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | DreamOmni2 |
| Dataset | DreamOmni2 Benchmark |

> [!tip] 效果简介
> - DreamOmni2 Benchmark (Editing) 上，Concrete Object Editing Success (Gemini eval.) 0.5854 vs OmniGen2, Kontext, etc. (outperforms all baselines)；Abstract Attribution Editing Success (Human eval.) 0.6829 vs Nano Banana, GPT-4o, etc. (outperforms commercial models)。
> - DreamOmni2 Benchmark (Generation) 上，Concrete Object Generation Success (Human eval.) 0.6098 vs Nano Banana, GPT-4o (outperforms commercial model Nano Banana)；Abstract Attribution Generation Success (Human eval.) 0.6829 vs OmniGen2, DreamO, etc. (significantly outperforms open-source models)。

## 概要

DreamOmni2 针对当前指令式图像编辑与生成的两个关键瓶颈提出了统一解决方案：**（1）** 现有编辑方法仅依赖单一文本指令，难以精确描述纹理、材质、姿态等复杂细节，需要参考图像作为补充；**（2）** 主体驱动生成仅能组合具体对象，无法处理抽象属性。两任务均不支持多模态输入与抽象属性迁移。

核心思路是将编辑与生成统一为**多模态指令驱动**任务。DreamOmni2 允许用户同时输入多张参考图像和文本指令，模型据此完成精确编辑或多样化生成，覆盖具体对象与抽象属性（纹理、材质、姿态、风格等）。这一能力由三个关键设计支撑：三阶段数据合成流水线（特征混合→提取模型→编辑/生成数据构造）提供大规模高质量配对训练数据；在 DiT 架构中引入索引编码与位置编码偏移，使模型能够区分多张参考图像并避免像素混淆；将 VLM（Qwen2.5-VL 7B）与生成/编辑模型联合训练，显著提升复杂指令理解能力。

在自建的 DreamOmni2 基准上，DreamOmni2 在编辑和生成任务上全面超越现有开源模型（如 OmniGen2、Flux.1 Kontext、DreamO 等），并在抽象属性编辑与具体对象生成上达到或接近商业级模型 GPT-4o 和 Nano Banana 的水平。消融实验证实，联合 VLM 训练与双编码方案是性能提升的决定性因素。

**方法定位**：DreamOmni2 属于多模态指令驱动的统一生成-编辑框架，区别于仅支持文本指令或单参考图像的方法。其数据构造与多图像处理机制为后续研究提供了可复用的技术路径。

图像生成与编辑领域近年来取得了显著进展，扩散模型（Diffusion Models）和自回归模型的出现使得文本到图像（T2I）的生成质量与可控性大幅提升。在此基础上，指令式图像编辑（Instruction-based Editing）和主体驱动生成（Subject-driven Generation）成为两个重要的研究方向。前者允许用户通过自然语言指令对已有图像进行修改，后者则要求模型根据提供的参考图像生成包含特定主体或属性的新图像。

然而，当前方法存在两个关键瓶颈。第一，指令式编辑任务几乎完全依赖单一文本指令来传递编辑意图。文本在描述复杂视觉细节（如纹理、材质、姿态、光照）时存在天然的信息瓶颈，用户难以仅凭文字精确表达“将这件毛衣的编织纹理复制到那件外套上”或“将左图的光影氛围迁移到右图”这类需求。第二，主体驱动生成任务长期局限于具体对象（concrete objects）的组合与迁移，对于抽象属性（abstract attributions）——如艺术风格、材质质感、情绪氛围——缺乏有效的处理能力。这两类任务共同面临一个根本性缺口：**不支持多模态输入与抽象属性的统一处理**。

从技术栈来看，现有方案在输入模态、多图像处理、指令理解三个维度上均存在明显不足。主流编辑模型（如 **Flux.1 Kontext** (Batifol et al., arXiv 2025)、**Qwen-Edit-2509**）仅接受单源图像加文本指令，无法利用多张参考图像提供互补信息。当需要同时参考多张图像时，模型缺乏区分不同输入图像的能力，容易产生像素混淆或“复制-粘贴”式的结果。在指令理解层面，现有方法普遍采用固定结构模板来解析用户意图，难以应对真实场景中复杂、非结构化的自然语言指令。此外，训练数据构建依赖分割或检测模型生成参考图像，覆盖的概念类型有限，难以扩展到抽象属性。

上述缺口催生了一个核心问题：**能否将编辑与生成统一为多模态指令驱动任务，使模型能够同时理解文本指令与多张参考图像，并覆盖从具体对象到抽象属性的完整概念谱系？** DreamOmni2 正是围绕这一问题展开，其动机在于通过三阶段数据合成流水线、多图像区分机制以及视觉语言模型（VLM）联合训练，构建一个能够精确执行多模态指令的统一框架。

## 核心方法与创新机理

DreamOmni2 的核心创新在于将图像编辑与生成统一为**多模态指令驱动**任务，并通过三项关键设计突破现有方法的瓶颈：**覆盖抽象属性的数据合成流水线**、**多参考图像区分机制**、以及**VLM 联合训练增强指令理解**。

### 从单模态到多模态指令：扩展概念覆盖范围

现有指令式编辑方法仅依赖单一文本指令，无法精确描述纹理、材质、姿态等复杂细节；主体驱动生成方法则局限于具体对象的组合，难以处理抽象属性。DreamOmni2 将输入模态从“单源图像 + 文本指令”扩展为“多参考图像 + 文本指令 + 源图像/目标描述”，使模型能够同时处理**具体对象**（concrete objects）与**抽象属性**（abstract attributions，如纹理、材质、风格、姿态等），从而显著拓宽了指令式编辑与生成的概念覆盖范围。

### 三阶段数据合成流水线：特征混合 → 提取模型 → 编辑/生成数据

为获得大规模高质量的多模态配对训练数据，DreamOmni2 设计了三阶段合成流水线（Figure 2）：

1. **特征混合（Feature Mixing）**：利用双分支注意力交换机制，在 target 分支的自注意力中混入 source 分支的噪声特征（式 1），使模型在生成 target 图像时参考 source 图像的视觉信息，从而生成共享特定抽象属性或具体对象的图像对。相比将两图拼接为一图的 diptych 方法，特征混合方案在保持原始分辨率的同时，成功率和生成质量更高。
2. **提取模型（Extraction Model）**：在特征混合数据上微调基础模型，使其能从参考图像中提取具体对象或抽象属性，并生成带有该属性的目标图像。
3. **编辑/生成数据构造**：利用提取模型从阶段二的源图像中提取对象，创建新的参考图像，形成从参考图像生成目标图像的训练数据对。

### 多参考图像区分：索引编码与位置编码偏移

当输入包含多张参考图像时，模型面临两个核心问题：无法定位指令中引用的图像，以及不同图像像素在潜空间中产生混淆和 copy-paste 效应。DreamOmni2 通过两项机制解决这一问题：

- **索引编码（Index Encoding）**：在位置通道中加入索引编码，帮助模型区分输入中的不同参考图像（如“Image 1”、“Image 2”），使其能够根据指令准确定位目标图像。
- **位置编码偏移（Position Encoding Shift）**：根据前序输入图像的大小对位置编码进行偏移，避免不同图像的像素在潜空间中重叠混淆。

消融实验（Table 5）表明，两者同时使用相比单独使用任一种编码均带来大幅性能提升，验证了这两项设计的必要性与互补性。

### VLM 联合训练：增强复杂指令理解

传统方法仅使用固定结构模板处理指令，难以应对真实场景中的复杂用户意图。DreamOmni2 将 **Qwen2.5-VL 7B** 与生成/编辑模型联合微调，使 VLM 能够将复杂用户指令解析并转换为标准结构化格式，再输入生成/编辑模型。消融实验（Table 4）显示，联合训练 VLM 使编辑和生成成功率全面提升，验证了 VLM 在理解复杂多模态指令中的关键作用。

### 统一框架下的编辑与生成

DreamOmni2 以 **Flux.1 Kontext** 作为基础统一模型，通过 Editing LoRA 和 Generation LoRA 分别激活多模态编辑与生成能力，在不破坏 Kontext 原始功能的前提下实现两类任务的统一。这一设计使模型在 DreamOmni2 基准的编辑和生成任务上全面超越现有开源模型（如 OmniGen2、DreamO），并达到或接近商业级模型 GPT-4o 和 Nano Banana 的水平。

DreamOmni2 将多模态指令驱动的图像编辑与生成统一为一个端到端框架，其核心由**三阶段数据合成流水线**、**多参考图像编码机制**以及**VLM 联合训练**三大模块构成，整体输入输出流如图 Figure 4 所示。

![[assets/figures/papers/paper_list_l2307_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DreamOmni2_Multimo/figures/004_Figure_4.jpg]]
*Figure 4: The framework of DreamOmni2. We introduces Position Encoding Shift and Index Encoding scheme to resolve issues of multi-reference image confusion and image identification. Additionally, we incorporate VLM to help the model better understand complex user instructions in real-world scenarios*

### 输入输出规范

模型的输入端接受三类信息：
- **多张参考图像**（可包含具体对象或抽象属性示例）；
- **源图像**（编辑任务）或**目标描述文本**（生成任务）；
- **自由形式的用户指令**，由 VLM 解析为结构化标准格式。

输出端直接生成符合指令的编辑后图像或全新目标图像，无需后处理或级联模型。

### 数据合成流水线：从配对数据到多模态指令

框架的训练数据完全通过三阶段合成流水线构建，核心瓶颈在于**现有方法无法生成同时共享抽象属性（如纹理、材质、风格）或具体对象的配对图像**。DreamOmni2 的解决方案如下（见 Figure 2）：

1. **特征混合（Feature Mixing）**：在基础 T2I 模型（Flux.1 Kontext）的去噪过程中，采用双分支结构同时生成源图像和目标图像。通过将源分支的噪声特征混入目标分支的自注意力计算（公式见下），使两幅图像共享指定的抽象属性或具体对象，且无需降低分辨率（相比 diptych 方法将两图拼入一张导致分辨率减半）。该阶段产出大规模高质量配对数据。
2. **提取模型（Extraction Model）**：在特征混合生成的配对数据上微调基础模型，使其具备从参考图像中提取具体对象或抽象属性、并据此生成新目标图像的能力。该模型是后续编辑/生成数据构造的核心工具。
3. **编辑/生成数据合成**：利用提取模型，从阶段二的源图像中提取对象或属性作为参考图像，构造“参考图像 + 源图像 + 指令 → 目标图像”的编辑训练数据；同时构造“参考图像 + 目标描述 → 生成图像”的生成训练数据。最终数据集覆盖具体对象与抽象属性两大类别，分布如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2307_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DreamOmni2_Multimo/figures/003_Figure_3.jpg]]
*Figure 3: Data distribution and samples for multimodal instruction-based editing and generation training data. Our dataset is comprehensive and diverse, including the generation and editing of concrete objects as well as abstract attributions, such as local and global attributions*

### 多参考图像编码：索引编码与位置编码偏移

当输入包含多张参考图像时，传统 DiT 架构无法区分不同图像，导致像素混淆和 copy-paste 效应。DreamOmni2 引入两种互补机制（见 Figure 4）：

- **索引编码（Index Encoding）**：在位置通道中注入索引信息，使模型能够识别指令中引用的“Image 1”、“Image 2”等对应的视觉内容。
- **位置编码偏移（Position Encoding Shift）**：根据前序输入图像的实际尺寸，对后续图像的位置编码施加偏移，避免不同图像的像素在空间位置上重叠。

消融实验（Table 5）表明，两者同时使用时编辑与生成成功率均大幅提升，单独使用任一种编码的效果均明显弱于联合方案。

### VLM 联合训练：复杂指令理解

为弥补基础模型仅能处理固定模板指令的缺陷，DreamOmni2 将 **Qwen2.5-VL 7B** 与生成/编辑模型进行联合微调。VLM 负责将用户的自由形式复杂指令解释并转换为标准结构化格式，再输入生成/编辑模型。联合训练（Table 4）相比仅训练生成/编辑模型（Scheme 2），在编辑和生成任务的成功率上均有显著提升，验证了 VLM 对复杂指令理解的关键作用。

### 训练策略

为在不破坏 Kontext 原始功能的前提下激活多模态编辑/生成能力，DreamOmni2 分别训练 **Editing LoRA** 和 **Generation LoRA**，通过低秩适配实现高效微调。训练成本方面，VLM 微调约需 10 A100 小时，LoRA 训练约需 384 A100 小时，对计算资源有一定要求。

DreamOmni2 的核心技术架构围绕三个关键模块展开：面向多模态训练数据合成的特征混合机制、支持多参考图像区分的索引与位置编码方案，以及提升复杂指令理解能力的 VLM 联合训练框架。

### 特征混合机制（Feature Mixing Scheme）

现有方法（如 diptych）将两张图像拼接为单张输入，导致分辨率减半。DreamOmni2 提出**特征混合方案**，在基础 T2I 模型的自注意力层中交换双分支特征，使模型同时生成源图像与目标图像，且不损失分辨率。

具体而言，模型采用双分支结构并行生成图像对。在目标分支的自注意力计算中，将源分支的噪声特征混入 Key 和 Value 矩阵：

$$
\operatorname{softmax}\left(\frac{\vec{Q}\vec{K}^{\top}}{\sqrt{d}}\right)\vec{V},\quad Q=[Q_{tar}^{n};Q_{tar}^{t}],\;K=[K_{tar}^{n};K_{tar}^{t};K_{src}^{n}],\;V=[V_{tar}^{n};V_{tar}^{t};V_{src}^{n}]
$$

其中：
- $Q_{tar}^{n}$、$K_{tar}^{n}$、$V_{tar}^{n}$ 为目标分支的噪声特征；
- $Q_{tar}^{t}$、$K_{tar}^{t}$、$V_{tar}^{t}$ 为目标分支的文本特征；
- $K_{src}^{n}$、$V_{src}^{n}$ 为源分支的噪声特征。

通过将源分支噪声特征纳入目标分支的注意力计算，模型在生成目标图像时可参考源图像的视觉信息，从而生成共享特定抽象属性（如纹理、材质、风格）或具体对象的配对图像。该方案相比 diptych 方法在成功率和分辨率上均有显著优势。

### 索引编码与位置编码偏移（Index Encoding & Position Encoding Shift）

当输入包含多张参考图像时，模型面临两大挑战：**无法区分不同图像**（指令中引用“Image 1”时模型无法定位）和**像素混淆**（多图拼接导致 copy-paste 效应）。DreamOmni2 通过两项编码设计解决上述问题。

**索引编码**：在 DiT 的位置通道中引入索引编码，为每张输入图像分配唯一标识。当用户指令引用特定图像索引时，模型可通过该编码准确定位对应的参考图像。

**位置编码偏移**：由于多张参考图像按顺序拼接输入，后续图像的位置编码需根据前序图像的尺寸进行偏移，确保每张图像的位置编码与其在全局序列中的实际位置一致，避免不同图像间的像素混淆。

消融实验（Table 5）表明，两者同时使用时编辑和生成成功率大幅提升，单独使用任一种编码均无法达到最佳性能。

### VLM 联合训练

为提升模型对复杂用户指令的理解能力，DreamOmni2 将 VLM（Qwen2.5-VL 7B）与生成/编辑模型联合微调。VLM 负责将自然语言指令解析为标准结构化格式，再输入生成/编辑模型执行。联合训练使 VLM 的指令理解与模型的执行能力协同优化，消融实验（Table 4）显示联合训练方案（Scheme 4）在各任务上成功率均显著高于仅训练生成/编辑模型的方案（Scheme 2）。

### 编辑与生成 LoRA

DreamOmni2 以 **Flux.1 Kontext**（Batifol et al., arXiv 2025）为基础模型，通过 LoRA 分别训练编辑能力和生成能力。这种设计在不破坏 Kontext 原始功能的前提下，激活多模态编辑与生成能力，实现任务解耦与高效微调。

## 实验与关键发现

### 评估体系与基准

为全面衡量多模态指令式编辑与生成的能力，作者构建了 **DreamOmni2 Benchmark**，覆盖**具体对象（Concrete Objects）**与**抽象属性（Abstract Attributions）**两大维度。评估采用三种方式：**Gemini** 自动评估具体对象编辑/生成成功率，**Doubao** 评估抽象属性编辑/生成成功率，以及由**专业工程师进行人工评估**（Human eval.）作为最终判据。Table 1 将 DreamOmni2 基准与现有相关基准进行了系统性对比，突出其多模态指令与抽象属性覆盖的独特性。

![[assets/figures/papers/paper_list_l2307_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DreamOmni2_Multimo/figures/005_Table_1.jpg]]
*Table 1: DreamOmni2 vs. related benchmarks*

### 主实验结果

#### 多模态指令式编辑

Table 2 报告了编辑任务的量化对比。在具体对象编辑上，DreamOmni2 的 Gemini 评估成功率达到 **0.5854**，显著超越所有开源基线（OmniGen2、Flux.1 Kontext 等）。在抽象属性编辑上，人工评估成功率为 **0.6829**，不仅大幅领先开源模型，甚至超越了商业闭源模型 **GPT-4o** 和 **Nano Banana**。Figure 5 的可视化对比进一步印证了这一结论：DreamOmni2 在纹理迁移、材质替换、姿态调整等抽象属性编辑场景中展现出更精确的编辑效果和更好的视觉一致性，而基线模型常出现属性丢失或图像失真。

![[assets/figures/papers/paper_list_l2307_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DreamOmni2_Multimo/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of multimodal instruction-based editing. We use Gemini [10] and Doubao [3] to evaluate the success editing ratio of different models on concrete objects and abstract attributions, respectively. In addition, “Human” refers to professional engineers assessing the editing success rates of all models*

#### 多模态指令式生成

Table 3 报告了生成任务的量化对比。DreamOmni2 在具体对象生成上的人工评估成功率为 **0.6098**，超越商业模型 Nano Banana；在抽象属性生成上达到 **0.6829**，显著优于 OmniGen2、DreamO 等开源模型。Figure 6 的可视化结果表明，DreamOmni2 能够根据参考图像和文本指令生成具有指定抽象属性（如风格、氛围）的高质量图像，生成结果与商业闭源模型 GPT-4o 和 Nano Banana 相当或更优。

### 消融实验

#### VLM 联合训练的影响

Table 4 系统消融了生成/编辑模型与 VLM（Qwen2.5-VL 7B）联合训练的效果。将 **Scheme 2**（仅训练生成/编辑模型，无 VLM）与 **Scheme 4**（联合 VLM 训练，即完整 DreamOmni2）进行对比：

![[assets/figures/papers/paper_list_l2307_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DreamOmni2_Multimo/figures/013_Table_4.jpg]]
*Table 4: Joint training for generation or editing models and VLM*

- 具体对象编辑成功率从较低水平提升至 **0.6585**
- 抽象属性编辑成功率提升至 **0.6280**
- 具体对象生成成功率提升至 **0.6667**
- 抽象属性生成成功率提升至 **0.6333**

这一显著提升表明，VLM 的联合微调使模型能够更好地理解复杂用户指令，并将其转换为标准结构化格式，从而大幅提高编辑和生成的成功率。

#### 多图像编码方案的影响

Table 5 消融了针对多参考图像输入的编码方案。对比三种配置：

![[assets/figures/papers/paper_list_l2307_https_openaccess_thecvf_com_content_CVPR2026_html_Xia_DreamOmni2_Multimo/figures/018_Table_5.jpg]]
*Table 5: Different encoding schemes for multiple image inputs*

- **Scheme 2**（无索引编码，无位置编码偏移）：模型无法区分多张输入图像，出现严重的像素混淆和 copy-paste 效应
- **Scheme 3**（仅索引编码）：性能有所提升，但仍存在图像间像素混淆
- **Scheme 4**（索引编码 + 位置编码偏移，完整方案）：四项指标均达到最优（0.6585 / 0.6280 / 0.6667 / 0.6333）

结果表明，**索引编码**使模型能够定位指令中引用的图像（如“Image 1”、“Image 2”），而**位置编码偏移**通过根据前序图像尺寸调整位置编码，有效消除了多图像间的像素混淆。两者协同使用是实现多参考图像精确编辑与生成的关键。

### 失败模式与局限性

尽管 DreamOmni2 在基准上表现优异，分析中仍识别出以下局限：

1. **分布外泛化未充分验证**：模型训练高度依赖大规模合成数据，在极端分布外（out-of-distribution）的抽象属性组合上的鲁棒性尚不明确。
2. **计算资源需求较高**：VLM 微调约需 10 A100 小时，LoRA 训练约需 384 A100 小时，对资源受限的研究者不够友好。
3. **基准覆盖有限**：目前仅在自建 DreamOmni2 基准上评估，缺乏在 DreamBooth、MagicBrush 等标准基准上的直接对比，多场景鲁棒性需要进一步验证。
4. **评估可靠性存疑**：人工评估由专业工程师完成，但未披露其背景与偏差控制机制；Gemini 和 Doubao 自动评估与人工评估之间的相关性未做详细分析，评估结论的可靠性需要进一步确认。
5. **抽象属性提取的细粒度评估缺失**：抽象属性迁移的准确性和一致性尚未经过充分的用户研究或细粒度指标（如属性保持率、风格一致性分数）的量化评估。

### 关键图表结论汇总

- **Table 2 & Figure 5**：DreamOmni2 在多模态指令式编辑上全面超越开源基线，在抽象属性编辑上达到甚至超越商业模型水平。
- **Table 3 & Figure 6**：DreamOmni2 在多模态指令式生成上显著优于开源模型，与商业闭源模型性能可比。
- **Table 4**：VLM 联合训练是提升复杂指令理解能力的关键设计，四项指标均有大幅提升。
- **Table 5**：索引编码与位置编码偏移的协同设计是解决多图像混淆的核心机制，缺一不可。

## 定位与知识库关联

### 与现有基线的关键差异

DreamOmni2 在任务定义、输入模态和模型架构三个层面与现有工作形成了系统性差异，其核心突破在于将“参考图像驱动的精确编辑”与“抽象属性引导的多样化生成”统一为**多模态指令驱动任务**。

**任务边界扩展：从具体对象到抽象属性。** 现有指令式编辑方法（如 **Qwen-Edit-2509**、**ITCiKU Ciricrs**）和主体驱动生成方法（如 **OmniGen2** (Wu et al., arXiv 2025)、**DreamO** (Mou et al., arXiv 2025)）仅支持基于单源图像和文本指令的具体对象操作。DreamOmni2 首次将任务覆盖范围扩展到抽象属性（纹理、材质、姿态、风格等），使模型能够根据参考图像中的抽象视觉特征进行编辑或生成。这一扩展直接解决了当前方法的瓶颈：单靠文本指令无法精确描述复杂细节，而仅支持具体对象的组合难以表达抽象概念。

**输入模态升级：多参考图像与索引机制。** 现有统一生成/编辑模型（如 **Flux.1 Kontext** (Batifol et al., arXiv 2025)）仅接受单张源图像输入，无法区分多张参考图像。DreamOmni2 引入**索引编码（Index Encoding）** 和**位置编码偏移（Position Encoding Shift）**，使模型能够同时处理多张参考图像，并准确识别指令中引用的图像（如 "Image 1"、"Image 2"）。消融实验（Table 5）表明，两者同时使用相比单独使用任一种编码均带来大幅性能提升，有效消除了多图像间的像素混淆和 copy-paste 效应。

**指令理解增强：VLM 联合训练。** 现有方法依赖固定结构模板解析用户指令，无法处理真实场景中的复杂自然语言描述。DreamOmni2 将 **Qwen2.5-VL 7B** 与生成/编辑模型联合微调，使 VLM 能将复杂用户指令转换为标准结构化格式，显著提升了指令遵从度。消融实验（Table 4）证实，联合训练 VLM 使编辑和生成成功率全面提升。

### 适用边界

DreamOmni2 在以下条件下表现出色：
- **多模态指令场景**：用户同时提供文本指令和一张或多张参考图像，要求精确编辑或生成包含特定视觉属性的图像。
- **抽象属性迁移**：需要将参考图像中的纹理、材质、风格等抽象属性迁移到目标图像时，模型能够有效捕捉并复现这些属性。
- **具体对象组合**：需要将多个参考图像中的具体对象组合到同一场景中时，模型能够保持对象身份一致性。

模型在以下场景中存在已知局限：
- **极端分布外组合**：训练数据虽覆盖广泛，但在训练分布之外的概念组合上泛化能力未充分验证。
- **细粒度抽象属性分辨**：对艺术风格、情绪氛围等细微抽象属性的分辨和迁移精度尚未经过充分的用户研究或细粒度指标评估。
- **高分辨率/视频扩展**：当前框架基于图像生成，向更高分辨率或视频等多模态数据的扩展性尚不明确。

### 局限与开放问题

**数据与评估局限。** 模型训练高度依赖大规模合成数据（三阶段流水线），训练成本较高（VLM 微调约 10 A100 小时，LoRA 约 384 A100 小时）。目前仅在自建的 DreamOmni2 基准上评估，缺乏在标准编辑/生成基准（如 DreamBooth、MagicBrush 等）上的直接对比，多场景鲁棒性有待进一步测试。人类评估由专业工程师完成，但未说明其背景与偏差控制机制；自动评估（Gemini、Doubao）与人类评估间的相关性未进行详细分析。

**开放问题。**
1. **开放世界抽象属性迁移**：模型能否在开放世界场景中有效分辨并精准迁移细微抽象属性（如艺术风格、情绪氛围）？
2. **指令遵从度优化**：后训练阶段是否可引入强化学习或偏好优化（如 DPO），以进一步提升对复杂指令的遵从度？
3. **模块解耦与端到端训练**：当前流水线依赖多个预训练模型（T2I、LLM、VLM），未来能否通过端到端训练减少模块间的错误累积？
4. **多模态扩展性**：该框架在视频生成/编辑等多模态数据上的扩展性如何？索引编码和位置编码偏移机制能否直接迁移？

### 知识库定位

DreamOmni2 处于**多模态指令式图像生成与编辑**的交叉领域，其贡献可定位于以下知识节点：

- **上游依赖**：基于 Flux.1 Kontext 的统一生成/编辑框架，继承其 DiT 架构和基础生成能力；利用 Qwen2.5-VL 提供多模态指令理解能力。
- **核心创新**：三阶段数据合成流水线（特征混合→提取模型→编辑/生成数据构造）提供了大规模高质量的多模态配对训练数据；索引编码与位置编码偏移解决了多参考图像输入的区分问题；VLM 联合训练弥合了复杂自然语言指令与模型可执行格式之间的鸿沟。
- **下游影响**：为多模态指令驱动的视觉内容创作提供了可复现的技术路线，其数据合成策略和编码方案可被后续工作借鉴，用于扩展至视频、3D 等多模态生成任务。

与商业级模型（**GPT-4o** (OpenAI 2025)、**Nano Banana** (Google 2025)）相比，DreamOmni2 在抽象属性编辑和具体对象生成任务上达到或接近其水平，但作为开源模型，其技术细节完全透明，为社区提供了可复现、可改进的基础。

## 原文 PDF

![[paperPDFs/CVPR_2026/DreamOmni2_Multimodal_Instruction_based_Generation_and_Editing.pdf]]

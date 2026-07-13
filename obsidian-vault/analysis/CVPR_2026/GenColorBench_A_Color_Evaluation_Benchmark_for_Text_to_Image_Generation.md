---
title: "GenColorBench: A Color Evaluation Benchmark for Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GenColorBench_A_Color_Evaluation_Benchmark_for_Text_to_Image_Generation.pdf
project_link: "https://moatifbutt.github.io/gencolorbench/"
code_link: null
aliases:
- GenColorBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建一个基于标准色彩体系（ISCC-NBS、CSS3/X11）并覆盖多种颜色规格和评估任务的大规模基准测试，可以客观量化模型色彩生成能力，为模型训练和优化提供明确方向。
primary_logic: 借助CIELuv色彩空间的像素级主成分分析和感知色彩距离指标，取代依赖视觉语言模型问答的传统评估方式，能实现更稳定、更感知一致的色彩准确度评测，揭示模型在颜色修饰和类别关联上的具体缺陷。
claims:
- 视觉语言模型（VLM）作为色彩评估工具有显著缺陷，Table 2显示BLIP3o在L2 MCQ准确率仅73.81%，MCQ稳定性仅64.22%，表明其依赖语言启发式而非真实色彩感知。
- 当前T2I模型在精确色彩生成上普遍表现不佳，Table 3显示在细粒度色彩（ISCC-NBS L3）上性能大幅下降，基础色彩（L1）准确率也仅部分模型超过60%。
- 模型性能与物体类别语义强相关，Figure 3显示在具有固定色彩印象的类别（如水果蔬菜）上准确率显著更低，表明模型受先验知识干扰。
- 模型对基本颜色和‘light’、‘dark’修饰理解较好，但对‘-ish’等微妙修饰几乎无法处理，准确率低于35%，解释了L1到L3的性能落差。
---

# GenColorBench: A Color Evaluation Benchmark for Text-to-Image Generation

> [!tip] 核心洞察
> 借助CIELuv色彩空间的像素级主成分分析和感知色彩距离指标，取代依赖视觉语言模型问答的传统评估方式，能实现更稳定、更感知一致的色彩准确度评测，揭示模型在颜色修饰和类别关联上的具体缺陷。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenColorBench：文本到图像生成的色彩评估基准 |
| 英文题名 | GenColorBench: A Color Evaluation Benchmark for Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Butt_GenColorBench_A_Color_Evaluation_Benchmark_for_Text-to-Image_Generation_CVPR_2026_paper.html) · [Project](https://moatifbutt.github.io/gencolorbench/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GenColorBench |
| Dataset | GenColorBench - Color Name Accuracy, GenColorBench - Numerical Color Understanding, GenColorBench - Implicit Color Association |

> [!tip] 效果简介
> - GenColorBench - Color Name Accuracy (ISCC-NBS L1) 上，准确率 (%) PixArt Alpha: 68.78 vs （首次基准，无可比基线） (N/A)。
> - GenColorBench - Numerical Color Understanding (ISCC-NBS L1) 上，准确率 (%) BLIP3o: 43.20 vs （其他模型远低于此） (N/A)。
> - GenColorBench - Implicit Color Association (ISCC-NBS L1) 上，准确率 (%) BLIP3o: 28.22 vs （整体低，显示任务极难） (N/A)。

## 概要

文本到图像（T2I）生成模型在语义理解与图像质量上取得了显著进展，但在**精确色彩生成**方面仍存在系统性缺陷——模型难以忠实匹配文本中指定的颜色，尤其面对细粒度色彩名称、数值色彩规格以及微妙修饰词（如“-ish”）时表现尤为薄弱。这一瓶颈的根源在于：**缺乏一个专门、量化且感知一致的颜色评估基准**，导致无法客观衡量并改进模型的色彩控制能力。

针对上述缺口，本文提出 **GenColorBench**，一个面向 T2I 模型的综合性色彩评估基准。其核心设计围绕三个关键决策：

1. **标准化色彩体系**：全面采用 ISCC-NBS（三层级粒度）和 CSS3/X11 色彩命名系统，并首次纳入数值色彩规格（RGB、十六进制），覆盖 400+ 种颜色。
2. **像素级客观评估**：摒弃依赖视觉语言模型（VLM）问答的传统评估范式，转而基于 CIELuv 色彩空间进行像素提取、主成分分析（PCA）及感知色彩距离度量（Delta Chroma、CIEDE2000、色相 MAE），实现更稳定、感知一致的评价。
3. **多任务覆盖与大规模提示**：构建超过 44,464 个提示，涵盖色彩名称准确度（CNA）、多对象色彩组合（MOC）、色彩-对象关联（COA）、数值色彩理解（NCU）和隐式色彩关联（ICA）五项任务，系统诊断模型在不同色彩理解维度上的能力。

实验揭示了若干关键发现：
- **VLM 不适合色彩评估**：BLIP3o 在 ISCC-NBS Level 2 多选题上的准确率仅 73.81%，且 MCQ 稳定性低至 64.22%（Table 2），表明 VLM 依赖语言启发式而非真实色彩感知。
- **细粒度色彩控制普遍薄弱**：从基础色（L1）到细粒度色（L3），所有模型性能大幅下降；即便是表现最好的 PixArt Alpha，在 L1 上也仅达 68.78%（Table 3）。
- **语义先验干扰严重**：模型在水果、蔬菜等具有固定色彩印象的类别上准确率显著低于服装、家具等类别（Figure 3），说明模型受预训练数据中的先验色彩知识支配。
- **修饰词理解存在盲区**：模型对“light”和“dark”修饰相对可处理，但对“-ish”类微妙修饰的准确率低于 35%（Figure 6），这是 L1→L3 性能落差的重要成因。

**方法谱系与知识库定位**：GenColorBench 在评估范式上区别于现有基准。传统基准如 **T2I-CompBench**（Huang et al., CVPR 2024）和 **GenEval**（Ghosh et al., ECCV 2024）主要依赖 VQA 准确率衡量组合性与提示遵循，仅部分覆盖色彩命名或组合任务，且未采用标准色彩体系。**ColorPeel**（AbdAlmageed et al., CVPR 2024）虽关注色彩生成，但任务覆盖面与提示规模有限。GenColorBench 首次将**像素级感知色彩度量**引入大规模 T2I 评估，填补了从粗粒度 VQA 到细粒度色彩控制的评估鸿沟。其评估对象涵盖扩散模型（**Stable Diffusion** 系列，Rombach et al., CVPR 2022；**FLUX**，Black Forest Labs, 2024）和统一多模态模型（**OmniGen2**，Wu et al., arXiv 2025），为后续模型训练与优化提供了明确的量化方向。

文本到图像（T2I）生成模型近年来取得了长足进步，但在精确控制生成图像中对象的颜色方面仍面临显著挑战。现有的T2I评估基准（如GenEval、T2I-CompBench等）虽然广泛用于评估组合性、提示遵循度和推理能力，但在色彩评估方面存在系统性缺口——它们或完全不覆盖色彩任务，或仅部分覆盖色彩命名或组合任务，缺乏对数值色彩规格、隐式色彩关联和细粒度色彩修饰等关键维度的全面考量（Table 1）。

这一缺口的根源在于两个相互关联的问题。其一，**缺乏系统性的色彩评估方法**：传统评估依赖视觉语言模型（VLM）进行问答式色彩判断，但VLM本身在色彩评估上并不可靠。Table 2显示，即便是表现最好的BLIP3o，在ISCC-NBS Level 2的多选题（MCQ）上准确率也仅为73.81%，且MCQ稳定性低至64.22%，表明VLM更多依赖语言启发式而非真实的色彩感知。其二，**缺乏覆盖全面的色彩基准**：现有基准的提示规模通常仅为几百到几千条，且未系统采用标准色彩体系，无法定量衡量模型在细粒度和数值色彩规格上的表现。

上述缺口导致了直接的实践困境：我们无法客观回答“当前的T2I模型到底能多准确地生成指定颜色”这一基本问题。初步证据表明，现有模型在精确色彩生成上普遍表现不佳——在细粒度色彩（ISCC-NBS L3）上性能大幅下降，即便在基础色彩（L1）上，也仅部分模型准确率超过60%（Table 3）。更关键的是，模型性能与物体类别语义强相关：在具有固定色彩印象的类别（如水果蔬菜）上，模型受先验知识干扰，准确率显著更低（Figure 3）。在色彩修饰方面，模型对“light”和“dark”的理解相对较好，但对“-ish”等微妙修饰几乎无法处理，准确率低于35%（Figure 6），这解释了从L1到L3的性能落差。

此外，训练数据的色彩分布本身存在偏差。对LAION-2B文本提示的分析显示，数值色彩在训练语料中严重欠表示，而ISCC-NBS L2色彩及其修饰词占据主导（Figure 5）。这种数据偏差进一步加剧了模型在数值色彩理解任务上的困难。

为填补上述缺口，GenColorBench提出了一个系统性的解决方案：基于ISCC-NBS（三层级）和CSS3/X11等标准色彩体系，构建覆盖400+种颜色、超过44,464条提示的大规模基准，并采用CIELuv色彩空间的像素级主成分分析和感知色彩距离指标，取代不稳定的VLM问答式评估。这一设计使得我们能够首次从色彩名称准确度、多对象色彩组合、色彩-对象关联、数值色彩理解和隐式色彩关联五个维度，定量诊断T2I模型的色彩生成能力。

## 核心方法与创新机理

GenColorBench的核心创新在于：它不再依赖视觉语言模型（VLM）的问答式评估，而是构建了一套**基于CIELuv色彩空间的像素级客观评价体系**，并首次将**标准色彩命名体系**与**多维度色彩理解任务**系统性地引入T2I模型的评估。

### 从VLM问答到像素级感知评估的范式转换

传统T2I色彩评估（如GenEval、T2I-CompBench）依赖VLM通过问答判断生成图像中的颜色是否正确。GenColorBench通过实证揭示了这一范式的根本缺陷：**VLM在色彩评估中并不可靠**。Table 2显示，即便表现最好的BLIP3o，在ISCC-NBS Level 2的多选题（MCQ）上准确率也仅为73.81%，且MCQ稳定性低至64.22%。这表明VLM的判断更多依赖语言启发式而非真实的色彩感知，将其作为色彩评估工具会引入系统性偏差。

为突破这一瓶颈，GenColorBench提出了**像素级色彩评估流水线**（Figure 1），其核心机制包括：

1. **CIELuv空间色彩接地**：将生成图像中目标对象的像素从RGB转换至感知均匀的CIELuv空间，得到像素向量 $(L_i^*, u_i^*, v_i^*)_{i=1}^N$。对色度分量 $(u^*, v^*)$ 进行主成分分析，提取第一主成分 $\mathbf{v}_1 = (v_{1u}, v_{1v})$ 作为对象的**主导色调方向**，并计算投影后的色度均值 $(\overline{u_{\mathrm{proj}}^*}, \overline{v_{\mathrm{proj}}^*})$ 来表示主导色（Figure 2）。

2. **感知色彩距离度量**：不再依赖VLM的语义判断，而是计算三项感知驱动的色彩指标——Delta Chroma、CIEDE2000和色相MAE——通过在感知最近邻色彩候选集中寻找最小距离来评定色彩准确度。这确保了评估结果与人类视觉感知的一致性，从根本上避免了VLM评估的不稳定性。

### 三层级色彩体系与五维任务覆盖

此前基准测试在色彩评估上存在两个关键缺口：**色彩体系缺失**和**任务覆盖面窄**。

GenColorBench全面采用了**ISCC-NBS三层级色彩命名系统**（L1基础色13类、L2中间色、L3细粒度色267种）和**CSS3/X11网络标准色**（147种），并首次将**数值色彩规格**（RGB、十六进制码）纳入评估。这一设计使得基准能够从日常基础色彩到专业细粒度色彩进行分层诊断，Table 3中L1到L3的性能落差直接量化了模型在细粒度色彩控制上的能力边界。

在任务设计上，GenColorBench覆盖了**五大色彩理解任务**（Table 1），远超现有基准的部分覆盖：色彩名称准确度（CNA）、多对象色彩组合（MOC）、色彩-对象关联（COA）、数值色彩理解（NCU）和隐式色彩关联（ICA）。其中，NCU和ICA是此前基准完全未涉及的任务，直接对应了模型理解RGB数值和“草莓的典型颜色”这类隐式关联的能力。

### 规模与生态定位

GenColorBench包含**超过44,464个精心设计的提示**，覆盖**400+种颜色**，规模远超GenEval（553个提示）和T2I-CompBench（约6,000个提示）。这一规模优势使得细粒度的语义类别消融和颜色修饰分析成为可能——例如Figure 3揭示了模型在水果蔬菜类别上的准确率显著低于服装家具类别，Figure 6则量化了模型对“-ish”等微妙修饰的处理能力不足35%。这些发现直接指向了模型受先验色彩知识干扰和缺乏细微色彩变体理解的核心缺陷，为后续模型优化提供了明确的改进方向。

GenColorBench 的评估框架遵循一个五阶段的感知色彩评估流水线，其设计目标是用客观的像素级色彩分析取代传统 VLM 问答式的评估范式。Figure 1 展示了该流水线的完整架构：**VQA-based Object Localization → Object Segmentation → Pixel Extraction → Color Grounding → Score Mechanism**。

![[assets/figures/papers/paper_list_l2207_https_openaccess_thecvf_com_content_CVPR2026_html_Butt_GenColorBench_A_C/figures/003_Figure_1.jpg]]
*Figure 1: An overview of GenColorBench evaluation framework. The evaluation pipeline consists of five key components: VQA-based object localization, object segmentation, pixel extraction, color grounding, and score mechanism. Then, five color evaluation tasks are devised to analyse different aspects of color understanding in T2I models covering single object coloring, color-object association, multiobject color composition, numerical color understanding, and Implicit Color Association*

### 流水线模块与数据流

1. **VQA-based Object Localization（基于 VQA 的对象定位）**  
   借鉴 Davidsonian Scene Graph（DSG）框架，首先通过视觉问答验证生成图像中是否确实存在提示指定的目标对象。这一步骤确保后续色彩评估建立在对象存在性已被确认的基础上，避免对缺失对象进行无意义的色彩分析。

2. **Object Segmentation（对象分割）**  
   采用 Grounded SAM 流水线生成高质量的对象二值掩码：先由 Grounding DINO 进行文本引导的粗定位，再由 SAM 生成精确的像素级分割掩码。掩码用于滤除背景和无关区域，仅保留目标对象的像素。

3. **Pixel Extraction（像素提取）**  
   从分割掩码覆盖的区域提取 RGB 像素，并转换至 CIELuv 色彩空间。CIELuv 空间的选择源于其感知均匀性——空间中的欧氏距离与人类感知的色彩差异近似成正比，这为后续的感知色彩距离计算奠定了基础。提取的像素向量表示为 $(L_i^*, u_i^*, v_i^*)_{i=1}^N$。

4. **Color Grounding（色彩锚定）**  
   在 CIELuv 空间中对色度分量 $(u^*, v^*)$ 进行主成分分析（PCA），第一主成分 $\mathbf{v}_1 = (v_{1u}, v_{1v})$ 定义了对象的**主导色调方向**（Figure 2 中黑色直线所示）。所有色度值在该方向上的投影均值 $(\overline{u_{\mathrm{proj}}^*}, \overline{v_{\mathrm{proj}}^*})$ 被用作对象的整体主导色表征。随后，在预定义的色彩候选集中搜索与主导色感知距离最近的颜色作为最终判定色。

5. **Score Mechanism（评分机制）**  
   综合计算三项感知色彩距离指标：**Delta Chroma**（色度差）、**CIEDE2000**（完整色差，涵盖色相、饱和度和明度差异）和 **MAE Hue**（色相平均绝对误差）。三项指标从不同维度量化生成色与目标色之间的偏差，最终聚合为色彩准确度评分。

### 评估任务设计

基于上述统一流水线，GenColorBench 设计了五类色彩评估任务，覆盖从单对象着色到隐式色彩关联的不同能力维度：

- **Color Name Accuracy (CNA)**：评估模型对显式颜色名称（如 “red car”）的遵循能力。
- **Multi-Object Color Composition (MOC)**：评估多对象场景中不同对象各自颜色的正确组合。
- **Color-Object Association (COA)**：评估模型将颜色与特定对象正确关联的能力。
- **Numerical Color Understanding (NCU)**：评估对 RGB 值和十六进制颜色码等数值色彩规格的理解。
- **Implicit Color Association (ICA)**：评估模型从场景描述中推断隐含色彩的能力（如 “ripe banana” 应生成黄色）。

### 与传统 VLM 评估范式的对比

Table 1 的系统对比揭示了 GenColorBench 的核心定位：现有基准（如 GenEval、T2I-CompBench、DSG 等）仅部分覆盖色彩相关任务，且普遍依赖 VLM 进行问答式评估。Table 2 的实验证据表明这一范式存在根本缺陷——BLIP3o 在 ISCC-NBS Level 2 的 MCQ 准确率仅为 73.81%，MCQ 稳定性低至 64.22%，说明 VLM 依赖语言启发式而非真实的色彩感知。GenColorBench 通过基于 CIELuv 空间的像素级主成分分析和感知色彩距离指标，绕过了这一瓶颈，实现了更稳定、更感知一致的色彩准确度评测。

GenColorBench 的评估框架由五个顺序模块构成（Figure 1），形成从图像生成到色彩评分的完整闭环。整体设计目标是以感知一致的方式量化生成图像中对象的色彩准确度，替代依赖视觉语言模型（VLM）问答的传统评估范式。

### 1. 基于VQA的对象定位

评估的第一步是验证生成图像中是否确实存在提示所指定的对象。论文采用 Davidsonian Scene Graph（DSG）框架下的 VQA 验证机制：对每张生成图像，向 VQA 模型询问目标对象是否存在，仅当确认存在后才进入后续色彩评估。这一模块是整个流水线的入口门控，其准确性直接影响下游评分的有效性。论文指出，虽然该环节可能引入误差，但错误率较低，属于可接受的工程折衷。

### 2. 对象分割

确认对象存在后，使用 **Grounded SAM** 流水线生成高质量的二值掩码。具体流程为：Grounding DINO 基于文本引导进行粗粒度对象定位，随后 SAM 在定位基础上产生精细分割掩码。掩码的作用是隔离目标对象的像素区域，排除背景和噪声成分，确保后续色彩分析仅聚焦于指定对象。

### 3. 像素提取与色彩空间转换

从分割掩码覆盖的区域提取所有像素，将其从 RGB 色彩空间转换至 **CIELuv** 色彩空间。CIELuv 的选择基于其感知均匀性——该空间中两点间的欧氏距离近似于人类视觉感知的色彩差异。对于每个分割对象，提取的像素集合表示为：

$$(L_i^*, u_i^*, v_i^*)_{i=1}^N$$

其中 $L_i^*$ 为明度分量，$(u_i^*, v_i^*)$ 为色度分量，$N$ 为掩码内像素总数。

### 4. 色彩锚定

色彩锚定模块是框架的核心创新，其目标是从像素分布中提取代表对象整体色调的主导色，并与目标颜色进行感知距离比较。

**主导色调方向**：对色度分量 $(u_i^*, v_i^*)$ 进行主成分分析（PCA），取第一主成分向量作为对象的主导色调方向：

$$\mathbf{v}_1 = (v_{1u}, v_{1v})$$

该向量捕捉了对象色度分布的最大方差方向，即对象在色度平面上的整体色调走向（Figure 2 中以黑色直线示意）。

**投影色度均值**：将所有色度值投影到第一主成分方向上，取投影后的平均值作为对象的主导色表示：

$$(\overline{u_{\mathrm{proj}}^*}, \overline{v_{\mathrm{proj}}^*})$$

这一处理通过降维去除了色度分布中的散射噪声，使主导色估计更加鲁棒。

**感知色彩距离计算**：将投影色度均值与目标颜色在 CIELuv 空间中进行比较，基于感知最近邻色彩候选集计算最小距离。论文未给出单一封闭公式，而是综合使用三项感知色彩指标。

### 5. 评分机制

评分模块输出三个感知色彩指标，从不同维度量化生成色彩与目标色彩的偏差：

- **Delta Chroma**：衡量色度差异，反映色彩饱和度和色调的综合偏差。
- **CIEDE2000**：国际照明委员会定义的色差公式，是目前最精确的感知色差度量之一，综合考虑明度、色度和色调的感知非线性。
- **色相 MAE**：色相角度的平均绝对误差，专门衡量色调方向的偏差。

三项指标共同构成色彩准确度的综合评定，取代了传统 VQA 准确率单一维度的评估方式。Table 2 的实验证据表明，VLM 在色彩评估任务上的表现极不稳定——BLIP3o 在 ISCC-NBS Level 2 的 MCQ 准确率仅 73.81%，MCQ 稳定性仅 64.22%——这从反面验证了基于像素级感知距离的客观评估方法的必要性。

## 实验与关键发现

### 核心实验设置

GenColorBench 在 44,464 个提示上对 9 个主流 T2I 模型进行评估，每个提示生成 4 张图像，取平均分数。所有模型的采样步数和图像分辨率均保持默认设置以保证公平比较。评估覆盖三个色彩规格粒度：ISCC-NBS Level 1（13 个基础色彩类别）、Level 3（267 个含修饰词的细粒度色彩）以及 CSS3/X11（147 个网页标准色彩）。论文推荐以 ISCC-NBS L1 作为评估通用 T2I 模型的主要指标，因其与日常色彩词汇对齐，最具实用价值。

### 主结果分析

Table 3 展示了各模型在五项色彩任务上的整体表现。核心发现如下：

![[assets/figures/papers/paper_list_l2207_https_openaccess_thecvf_com_content_CVPR2026_html_Butt_GenColorBench_A_C/figures/005_Table_3.jpg]]
*Table 3: Overall performance of T2I models on GenColorBench. We report results across three color specification granularities: ISCC-NBS-L1 provides the most practical evaluation using 13 basic color categories (red, blue, green, etc.) that align with everyday color vocabulary, making it the recommended primary metric for assessing general-purpose T2I models. ISCC-NBS-L3 evaluates fine-grained color understanding with 267 specific colors including modifiers, representing more specialized demands. CSS3/X11 includes 147 webstandard colors. The performance drop from L1 to L3 reveals limitations in fine-grained color control. indicate top-3 performers*

![[assets/figures/papers/paper_list_l2207_https_openaccess_thecvf_com_content_CVPR2026_html_Butt_GenColorBench_A_C/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of basic, intermediate, and modifier-based color understanding across models. Performance consistently decreases from basic L1 to fine-grained colors. Among modifiers, models handle light better than dark, while -ish modifiers (describing gradient-like perceptual continuity) remain most challenging, explaining the L1→L3 performance gap observed in Table 3*

**色彩名称准确度（CNA）** 是表现相对最好的任务，但整体水平仍然有限。在 ISCC-NBS L1 上，PixArt Alpha 以 68.78% 的准确率领先，表明即便是基础色彩（如“red”、“blue”），当前模型也无法稳定生成。当色彩规格细化到 L3 时，所有模型性能均大幅下降，这一落差直接揭示了模型在细粒度色彩控制上的根本缺陷。

**数值色彩理解（NCU）** 任务上，BLIP3o 在 L1 达到 43.20%，显著优于其他模型，说明该模型对 RGB 和十六进制色彩规格具有一定理解能力。但绝对数值仍不足一半，表明数值色彩生成仍是 T2I 模型的普遍短板。

**隐式色彩关联（ICA）** 是所有任务中最困难的。BLIP3o 在 L1 仅取得 28.22% 的准确率，其他模型表现更差。该任务要求模型根据常识性色彩关联生成图像（如“ripe banana”应为黄色），低分表明模型受训练数据中先验分布的干扰严重，难以灵活调用色彩知识。

**色彩-对象关联（COA）** 任务同样暴露了模型弱点：OmniGen2 在 L1 仅达 34.23%，说明当色彩与特定对象配对时，模型容易产生混淆或忽略色彩指令。

### 关键消融与失败模式

**VLM 作为色彩评估工具不可靠（Table 2）。** 实验显示，即使表现最好的 VLM（BLIP3o），在 ISCC-NBS L2 的 MCQ 准确率也仅 73.81%，MCQ 稳定性仅 64.22%。这表明 VLM 依赖语言启发式而非真实的色彩感知能力来回答问题，不应被用作色彩评估的可靠工具。这一发现直接支撑了 GenColorBench 采用像素级 CIELuv 分析而非 VQA 评分的设计动机。

**类别语义与色彩准确性强相关（Figure 3）。** 各模型在不同语义类别上的色彩名称准确率差异显著。具有固定色彩印象的类别（如水果蔬菜）准确率明显低于服装、家具等色彩更灵活的类别。这说明模型受训练数据中“苹果=红色”等先验知识干扰，当提示要求生成非常规色彩的对象时（如“蓝色香蕉”），模型倾向于回归到统计先验。

**主导色偏差普遍存在（Figure 4）。** 对 10,000 张生成图像的主导色分布分析显示，所有模型均显著偏向黑色、灰色和棕色。这种偏差在除水果蔬菜外的所有类别中一致出现，反映出训练数据分布的不平衡以及模型在色彩多样性上的内生局限。

**修饰词理解存在梯度缺陷（Figure 6）。** 模型对“light”修饰词处理最好，“dark”次之，而对“-ish”类修饰词（如“reddish”、“bluish”）的准确率低于 35%。这类修饰词描述的是梯度式的感知连续性，需要模型具备更精细的色彩空间理解，而这正是当前模型的盲区。该发现直接解释了从 L1 到 L3 的性能崩塌机制——L3 包含大量含修饰词的色彩规格，模型对这些微妙变体几乎无能为力。

### 证据强度与待验证项

上述结论中，Table 3 和 Table 2 的结果置信度较高（≥0.95），基于系统性的量化实验。Figure 3 和 Figure 4 的类别语义分析置信度为 0.9，其结论方向明确但具体数值需结合原文图表确认。Figure 6 的修饰词消融置信度为 0.9，揭示了清晰的性能梯度，但各模型在单个修饰词上的精确数值建议直接查阅原文。基准测试的公平性方面，论文未对模型进行任何微调或提示工程优化，所有模型使用默认配置，这保证了横向比较的公平性，但也意味着优化后的模型表现可能高于当前报告值。

![[assets/figures/papers/paper_list_l2207_https_openaccess_thecvf_com_content_CVPR2026_html_Butt_GenColorBench_A_C/figures/002_Table_2.jpg]]
*Table 2: Performance (accuracy) of VLMs-based VQA on CSS/X11 and ISCC-NBS Level 2 colors*

![[assets/figures/papers/paper_list_l2207_https_openaccess_thecvf_com_content_CVPR2026_html_Butt_GenColorBench_A_C/figures/007_Figure_4.jpg]]
*Figure 4: Distribution of estimated dominant colors (Top-10) across 10,000 generated images for each T2I models, revealing inherent color biases in vanilla baseline models. Models include: PixArt Alpha (A), BLIP3o (B), Flux (F), Janus-Pro (J), Sana (N), OmniGen2 (O), PixArt Sigma (P), Stable Diffusion 3 (S), and Stable Diffusion 3.5 (D). Interestingly, all the models are significantly biased towards black, gray, and brown across all the categories except fruits and vegetables*

![[assets/figures/papers/paper_list_l2207_https_openaccess_thecvf_com_content_CVPR2026_html_Butt_GenColorBench_A_C/figures/001_Table_1.jpg]]
*Table 1: Overview of existing T2I evaluation benchmarks on five color evaluation tasks: Color Name Accuracy (CNA), Multi-Object Color Composition (MOC), Color–Object Association (COA), Numeric Color Understanding (NCU), Implicit Color Association (ICA). While these benchmarks are widely adopted for assessing various aspects of T2I generation—such as compositionality, prompt adherence, and reasoning—they lack comprehensive coverage of key color understanding and evaluation tasks. GenColorBench is specifically designed to fill this gap by supporting a broad spectrum of color-related tasks. (✓: covered, ×: not covered, ≈: partially covered)*

## 定位与知识库关联

### 1. 评估范式演进中的定位

GenColorBench 在文本到图像（T2I）评估方法谱系中占据一个明确的断裂点：它将色彩评估从“语言问答”范式迁移到“感知色彩空间中的像素级测量”范式。这一迁移的动机来自一个关键的负面发现：视觉语言模型（VLM）作为色彩评估工具存在根本性缺陷。

**Table 2** 给出了直接证据：BLIP3o 在 ISCC-NBS Level 2 的多选题（MCQ）上准确率仅为 73.81%，且 MCQ 稳定性低至 64.22%。Qwen2VL 在开放式问答上的准确率更是仅有 44.82%。这些数字揭示了一个深层问题：VLM 依赖语言启发式而非真实的色彩感知进行判断——当文本提示与图像实际颜色不一致时，VLM 倾向于“相信”文本而非像素。这解释了为什么 GenColorBench 选择绕开 VLM 评估路径，转而构建基于 CIELuv 色彩空间的客观度量体系。

与现有评估基准的系统性对比见 **Table 1**。GenEval（553 个提示）、T2I-CompBench（6000 个提示）等基准在色彩名称准确度（CNA）、多对象色彩组合（MOC）、色彩-对象关联（COA）、数值色彩理解（NCU）和隐式色彩关联（ICA）五个维度上仅部分覆盖或完全缺失。GenColorBench 以 44,464 个提示、400+ 种颜色的规模填补了这一空白，首次将数值色彩规格（RGB、十六进制码）纳入标准化评估。

### 2. 与基线模型的关系

GenColorBench 本身是评估框架而非生成模型，其“基线”是被评估的 T2I 模型群。在方法层面，它与以下工作形成对照：

- **基于 VQA 的评估方法**（如 DSG 框架、mPLUG-large、BLIP-VQA）：GenColorBench 在对象检测环节保留了 VQA 验证（基于 DSG 框架），但将核心色彩判断环节完全替换为 CIELuv 空间的主成分分析。这是一种“混合继承”——保留了 VQA 在对象定位上的优势，但拒绝了其在色彩判断上的不可靠性。

- **Stable Diffusion 系列**（Rombach et al., CVPR 2022）：作为被评估的扩散模型基线，SD3 和 SD3.5 在 GenColorBench 上的表现揭示了扩散架构在细粒度色彩控制上的系统性局限。

- **FLUX**（Black Forest Labs, 2024）：作为新一代扩散模型的代表，其色彩偏差模式（见 Figure 4）与 SD 系列既有共性（普遍偏向黑、灰、棕色），又存在模型特定的差异。

- **OmniGen2**（Wu et al., arXiv 2025）：作为统一多模态模型的代表，其在色彩-对象关联任务上的表现（ISCC-NBS L1 上 34.23%）为理解不同架构范式的色彩能力提供了对比锚点。

### 3. 适用边界

GenColorBench 的适用边界由以下约束定义：

**覆盖范围边界**：基准测试仅覆盖英文提示和 COCO/ImageNet 中的常见物体类别。色彩命名体系基于 ISCC-NBS 和 CSS3/X11 标准，未覆盖 Pantone、HSV 特定值或其他文化色彩命名习惯。数值色彩评估限于 RGB 和十六进制码，未扩展到 CMYK 或 LAB 直接指定。

**评估对象边界**：评估对象为合成图像，真实世界图像中的光照变化、材质反射、半透明等复杂光学现象未纳入考量。对象分割依赖 Grounded SAM，在复杂场景（遮挡、小物体、非典型视角）下可能引入掩码误差，进而传导至像素提取和色彩评分。

**任务粒度边界**：当前任务设计覆盖了从基本颜色命名到数值规格的梯度难度，但未涉及精确色相或饱和度控制、色彩和谐度、跨物体色彩一致性等更细粒度的色彩生成任务。

### 4. 局限与开放问题

**已知局限**：

1. **对象检测依赖 VQA**：尽管 VQA 在色彩判断上不可靠，但在对象存在性验证上仍被依赖。这一环节的错误率虽然较低，但在复杂场景下仍可能引入系统性偏差。

2. **分割精度上限**：Grounded SAM 的分割质量直接影响后续像素提取的纯度。当对象边界模糊或与背景色彩相近时，掩码可能包含背景像素，稀释主导色信号。

3. **文化偏差**：色彩名称的选取和“正确”色彩的判定隐含英语文化视角。例如，“-ish”修饰词的理解困难可能部分源于训练数据中的语言分布偏差，而非纯粹的视觉理解缺陷——**Figure 5** 显示 LAION-2B 文本提示中数值色彩严重欠表示，这为模型的色彩理解偏差提供了数据层面的解释。

4. **离线评估属性**：GenColorBench 提供诊断信号而非训练信号。它能够揭示模型在“-ish”修饰上准确率低于 35%（**Figure 6**）这一具体缺陷，但不提供直接的微调或训练策略来修复该缺陷。

**开放问题**：

1. 能否将 CIELuv 空间的感知色彩距离指标作为训练过程中的反馈信号，直接优化 T2I 模型的色彩生成能力？这需要解决离散提示到连续色彩空间的可微映射问题。

2. 模型在水果蔬菜等强色彩关联类别上准确率显著更低（**Figure 3**），表明先验知识对色彩生成存在干扰。如何解耦“类别典型色”与“指定色”之间的冲突，是一个尚未解决的架构问题。

3. 基准测试是否应扩展到多语言色彩命名体系？不同语言对色彩的切分方式不同（如俄语的浅蓝/深蓝区分），这既是文化公平性问题，也是测试模型色彩理解深度的潜在探针。

4. 当对象分割本身存在错误时，如何提升色彩评分的鲁棒性？可能的路径包括多尺度掩码融合、基于不确定性的像素加权，或直接跳过对象检测的全图色彩分布分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/GenColorBench_A_Color_Evaluation_Benchmark_for_Text_to_Image_Generation.pdf]]

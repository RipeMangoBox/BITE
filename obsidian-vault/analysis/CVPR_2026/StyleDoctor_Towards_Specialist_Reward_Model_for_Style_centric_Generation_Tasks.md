---
title: "StyleDoctor: Towards Specialist Reward Model for Style-centric Generation Tasks"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/StyleDoctor_Towards_Specialist_Reward_Model_for_Style_centric_Generation_Tasks.pdf
project_link: null
code_link: null
aliases:
- StyleDoctor
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入一个专门针对风格一致性的奖励模型 StyleDoctor，通过联合对比学习全局风格特征和多模态统一偏好训练，提供细粒度的风格评估信号。
primary_logic: 通过在大规模风格偏好数据集上训练一个联合图像和文本风格语义的专家奖励模型，可以有效引导扩散模型生成与参考风格更一致的图像。
claims:
- 消融实验表明，去除全局风格特征学习（GSF）和统一偏好学习（UPL）会导致风格一致性和生成性能显著下降。
- StyleDoctor在风格图像检索（75.46%准确率）和多模态风格理解（71.14%准确率）上大幅超越现有风格编码器和多模态语言模型。
- 将StyleDoctor作为奖励模型用于OmniStyle和OmniGen2等生成模型时，风格一致性指标（CSD）分别提升至0.78和0.72。
- 风格图像检索 (Style30k) 上 检索准确率 (%) = 75.46
---

# StyleDoctor: Towards Specialist Reward Model for Style-centric Generation Tasks

> [!tip] 核心洞察
> 通过在大规模风格偏好数据集上训练一个联合图像和文本风格语义的专家奖励模型，可以有效引导扩散模型生成与参考风格更一致的图像。

| 字段 | 内容 |
|------|------|
| 中文题名 | StyleDoctor：面向风格中心生成任务的专家奖励模型 |
| 英文题名 | StyleDoctor: Towards Specialist Reward Model for Style-centric Generation Tasks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/He_StyleDoctor_Towards_Specialist_Reward_Model_for_Style-centric_Generation_Tasks_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | StyleDoctor |
| Dataset | 风格定制化 (B-LoRA) vs 人类偏好奖励模型 |

> [!tip] 效果简介
> - 风格图像检索 (Style30k) 上，检索准确率 (%) 75.46 vs 69.98 (StyleTokenizer) (+5.48)。
> - 多模态风格理解 上，准确率 (%) 71.14 vs 68.0 (GPT-4o) (+3.14)。
> - 文本控制风格生成 (OmniGen2) 上，风格准确率 (StyleDoctor / GPT-4o) 69.58 / 67.60 vs — (—)。

## 概要

**核心问题**：现有的人类偏好奖励模型（如 **HPSv2**，Wu et al., arXiv 2023）和仅基于图像特征的风格编码器（如 **CSD**，Somepali et al., arXiv 2024；**StyleTokenizer**，Li et al., ECCV 2024）无法有效感知图像风格。前者缺乏对风格维度的细粒度建模能力，后者缺少跨模态监督信号，导致在风格生成任务中评估不准、引导乏力。

**核心洞察**：通过在大规模风格偏好数据集上联合学习全局图像风格特征与多模态风格语义，构建一个专门针对风格一致性的专家奖励模型，可以有效引导扩散模型生成与参考风格高度一致的图像。

**方法与定位**：本文提出 **StyleDoctor**——一个以多模态大语言模型 Qwen2.5-VL-3B 为基座、注入对比学习全局风格令牌的风格中心奖励模型。其技术路线属于“专家奖励模型 + 扩散模型对齐”范式，区别于通用人类偏好奖励模型（仅输出美学分数）和纯视觉风格编码器（仅做特征匹配）。StyleDoctor 通过三阶段训练（全局风格对比学习 → 基本风格理解微调 → 统一风格偏好学习）获得多维度的风格评估能力，并可通过输出 logits 的平均置信度作为奖励信号，以强化学习方式引导扩散模型优化风格一致性。

**主要结果**：
- **风格感知**：在风格图像检索任务上达到 75.46% 准确率，超越 StyleTokenizer（69.98%）；在多模态风格理解任务上达到 71.14% 准确率，超越 GPT-4o（68.0%）。
- **风格生成对齐**：将 StyleDoctor 作为奖励模型集成到 OmniStyle 和 OmniGen2 后，风格一致性指标（CSD）分别提升至 0.78 和 0.72。
- **关键验证**：消融实验表明，去除全局风格特征学习（GSF）和统一偏好学习（UPL）会导致性能显著下降，证实这两部分是方法的核心有效设计。



### 风格生成任务的兴起与核心瓶颈

随着扩散模型（Diffusion Models）在图像生成领域的快速发展，风格化的图像生成——即生成既保留内容结构又体现特定艺术风格的图像——已成为视觉内容创作的关键需求。无论是基于文本描述的风格控制（text-controlled style generation）、基于参考图像的风格迁移（reference image-guided style transfer），还是基于指令的风格定制化（instruction-guided style customization），这些任务都要求模型能够精确感知和对齐“风格”这一高度抽象且多维度的视觉概念。

然而，当前风格生成任务面临一个根本性瓶颈：**现有的人类偏好奖励模型无法有效感知图像风格**。主流的奖励模型（如 **HPSv2**，Wu et al., arXiv 2023）主要针对通用图像质量与美学评分设计，缺乏对风格一致性（style consistency）的细粒度评估能力。另一方面，仅基于图像特征的风格编码器（如 **CSD**，Somepali et al., arXiv 2024；**StyleTokenizer**，Li et al., ECCV 2024）虽然通过对比学习编码了全局风格特征，但由于缺乏跨模态监督信号，无法理解和验证文本描述与图像风格之间的语义对齐关系。

这一缺口导致两个直接后果：
1. **风格评估不可靠**：现有方法无法同时捕捉图像层面的风格特征和文本层面的风格语义，难以对“生成图像是否与目标风格一致”给出准确判断。
2. **风格优化无方向**：缺乏可靠的风格奖励信号，扩散模型在生成过程中无法获得有效的风格对齐反馈，限制了风格生成质量的进一步提升。

### 现有方法的范式局限

从奖励建模的范式来看，现有方案主要分为两类（如图2所示）：

- **人类偏好奖励模型（Human-Preference Reward Models）**：以 HPSv2 为代表，通过大规模人类偏好数据训练，输出通用美学分数。这类模型擅长评估图像的整体质量和与文本提示的语义一致性，但对“风格”这一特定维度缺乏专门的感知能力，无法区分两张图像在风格层面上的细微差异。
- **仅图像输入的风格编码器（Image-Only Style Encoders）**：以 CSD 和 StyleTokenizer 为代表，通过对比学习从图像中提取全局风格特征，用于风格相似度计算。这类方法虽然能够度量图像间的风格一致性，但完全忽略了文本模态的风格语义，无法处理“文本描述风格→生成图像”的跨模态对齐问题。

这两种范式各自存在盲区：前者缺少风格专精，后者缺少跨模态理解。**风格生成任务亟需一个能够联合图像风格特征与文本风格语义的专家模型**，既能在图像对之间评估风格一致性，又能在图像-文本之间验证风格对齐。

### 本文动机与核心思路

针对上述缺口，本文提出 **StyleDoctor**——一个专门面向风格中心生成任务的专家奖励模型（Specialist Reward Model）。其核心动机在于：

> 通过在大规模风格偏好数据集上训练一个联合图像和文本风格语义的专家奖励模型，可以有效引导扩散模型生成与参考风格更一致的图像。

StyleDoctor 的设计围绕三个关键创新展开：
1. **多模态基座**：采用多模态大语言模型 **Qwen2.5-VL-3B** 作为基座，使其天然具备跨模态语义理解能力。
2. **全局风格特征注入**：通过对比学习提取图像的全局风格特征，并将其作为专用风格令牌（style token）注入语言模型，使模型同时感知图像级风格特征和文本级风格语义。
3. **统一风格偏好学习**：构建大规模风格偏好数据集 **SPRData**（含400K四元组样本，覆盖1000种风格类别），并在多样化的输入格式上联合训练，使模型能够泛化到多种风格验证场景。

通过这一设计，StyleDoctor 能够提供多维度的风格奖励信号（包括全局风格一致性、色彩和谐度、笔触纹理等），为扩散模型的风格对齐优化提供精确的反馈指导。



## 核心方法与创新机理

StyleDoctor 的核心创新在于将风格感知从“通用美学评分”或“纯视觉编码”的单一范式，升级为**联合图像全局风格特征与多模态语言理解的专家奖励模型**。这一转变解决了现有方法在风格生成任务中的根本瓶颈：人类偏好奖励模型（如 **HPSv2**，Wu et al., arXiv 2023）无法有效感知图像风格，而仅基于图像特征的风格编码器（如 **CSD**，Somepali et al., arXiv 2024；**StyleTokenizer**，Li et al., ECCV 2024）又缺乏跨模态监督，导致评估信号与人类对风格一致性的判断存在偏差。

具体而言，StyleDoctor 通过以下四个关键设计实现了突破：

**1. 多模态基座替代纯视觉编码器。**
不同于仅依赖图像输入的 CLIP 或 Reward 模型，StyleDoctor 采用多模态大语言模型 **Qwen2.5-VL-3B** 作为基座，同时接收图像和文本指令。这使得模型能够理解“水墨风格”“油画笔触”等语言描述的风格语义，并将其与视觉信号对齐，从而支持文本控制、图像引导等多种风格生成任务的统一评估。

**2. 全局风格特征作为专用令牌注入。**
传统风格编码器仅通过对比学习提取全局图像风格特征，但这些特征与语言模型的交互有限。StyleDoctor 在对比学习全局风格特征后，将其通过额外的投影层注入为一个**特殊风格令牌**，与标准视觉令牌并行输入语言模型。这一设计使模型在推理时能显式感知参考风格与生成图像之间的全局风格一致性，而非仅依赖局部的视觉-文本对齐。

**3. 三阶段渐进式训练范式。**
不同于单任务（图像-文本对齐或偏好评分）的训练方式，StyleDoctor 采用三阶段训练：首先通过对比损失学习全局风格信息；然后进行基本的风格理解微调；最后进入**统一偏好学习**阶段，将四元组样本重组为多样化输入格式，联合训练模型在不同场景下的风格一致性验证能力。这种渐进式设计确保了模型从底层视觉特征到高层语义判断的逐步对齐。

**4. 多维度风格奖励信号。**
传统奖励模型仅输出单一的美学分数，难以捕捉风格的复杂性。StyleDoctor 提供**多维度奖励信号**，涵盖全局风格一致性、色彩和谐度、笔触纹理等细粒度维度。在推理时，模型通过输出 logits 中正面答案的平均置信度作为奖励分，为下游扩散模型的强化微调提供了更精准的风格对齐反馈。

这些创新共同构成了一个从“风格感知”到“风格引导”的闭环：StyleDoctor 不仅能准确判断风格一致性，还能作为奖励模型或正则化项直接介入生成过程，显著提升扩散模型在风格迁移、风格定制化等任务中的表现。



StyleDoctor 的整体设计围绕一个核心命题展开：**如何构建一个能够同时感知图像全局风格特征与文本风格语义的专家奖励模型，从而为风格中心生成任务提供细粒度的监督信号**。其 pipeline 由三个关键阶段串联而成，分别解决风格表征学习、跨模态风格理解、以及统一偏好建模三个子问题。

### 2.1 范式对比与设计动机

现有方案在风格评估上存在明显的结构性缺陷。人类偏好奖励模型（如 **HPSv2**，Wu et al., arXiv 2023）主要面向通用美学质量，缺乏对风格一致性的专门感知能力；而仅基于图像特征的风格编码器（如 **CSD**，Somepali et al., arXiv 2024；**StyleTokenizer**，Li et al., ECCV 2024）虽然能提取全局风格信息，却缺少跨模态监督，难以处理文本描述的风格条件。StyleDoctor 的核心创新在于将多模态大语言模型引入风格奖励建模，使模型能够同时处理“图像-图像”风格一致性比较和“文本-图像”风格对齐判断，从而弥合上述两类方法的断层（Figure 2）。

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/003_Figure_2.jpg]]
*Figure 2: A paradigm comparison of existing human-preference reward models,image-only style encoders,and StyleDoctor*

### 2.2 三阶段训练流水线

StyleDoctor 的训练分为三个递进阶段，每个阶段承担不同的能力构建任务：

**阶段一：全局风格特征学习（Global Style Feature Learning）**  
以视觉编码器 $E_v$ 提取图像特征，通过对比学习损失函数 $\mathcal{L}_{con}$ 学习全局风格信息。该损失函数的形式为：

$$\mathcal { L } _ { c o n } = - \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \log \frac { \exp \left( \sin ( z _ { i } , z _ { i } ^ { + } ) / \tau \right) } { \sum _ { j = 1 } ^ { N } \exp \left( \sin ( z _ { i } , z _ { j } ^ { - } ) / \tau \right) }$$

其目标是拉近风格一致配对样本在特征空间中的余弦距离，同时推开风格不一致的负样本。这一阶段仅依赖图像信号，为后续跨模态融合提供紧凑的全局风格表征。

**阶段二：基本风格理解微调（Basic Style Understanding Fine-tuning）**  
将阶段一学到的全局风格特征通过一个额外的投影层注入为特殊的**风格令牌（style token）**，与标准图像令牌并行输入多模态大语言模型。基座模型选用 **Qwen2.5-VL-3B**，采用 LoRA 进行参数高效微调。此阶段使模型获得基本的风格感知能力，能够理解图像中的风格属性并响应文本风格查询。

**阶段三：统一风格偏好学习（Unified Preference Learning）**  
将 SPRData 中的四元组样本重组为多种输入格式，联合训练模型在不同场景下进行风格一致性验证——包括单图风格判断、双图风格比较、文本-图像风格对齐等。通过这种统一偏好学习，StyleDoctor 能够输出多维度的风格奖励信号，涵盖全局风格一致性、色彩和谐度、笔触纹理等细粒度维度。

### 2.3 奖励推理与下游集成

训练完成后，StyleDoctor 以两种方式介入下游生成任务：

- **作为奖励模型进行强化微调**：将 StyleDoctor 集成到扩散模型的强化学习流程中，通过其输出的风格一致性反馈信号引导生成过程。具体而言，模型不直接输出标量分数，而是利用输出 logits 空间中**正面答案的平均置信度**作为奖励分，从而提供更平滑、更具区分度的奖励信号。
- **作为正则化项**：在扩散模型微调过程中，StyleDoctor 可用于计算额外的正则化损失，鼓励生成图像最大化风格置信度和一致性。该方法已与 **B-LoRA** 等风格定制化方法结合验证。

整个框架的输入输出流可概括为：输入包括参考内容图像、参考风格图像（或文本风格描述）、待评估生成图像；经过视觉编码、风格令牌注入、多模态语言模型推理后，输出多维风格一致性评估结果及置信度分数，最终用于指导扩散模型的风格对齐优化。

### 补充图表

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/006_Figure_4.jpg]]
*Figure 4: Overviewofourstyle-centricrewardmodeling paradigm.Wereformulatequartetsmples from SPRData tosimulate dierent scenariostosupportgeneraliedstyleverifcationundervarioustasks.Aftertrainng,StylDoctocouldbeusedasrwardmodeltoguide difusionmodels throughreinforcementlearing,providing feedbacksignalsforbeterstylizationalignment.Meanwhile,StylDocotr couldalsobeutilzedtocalculateaegularzationtethatencourages tedifusionmodeltomaxiiestyleconfidenceandcosistency*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/001_Figure.jpg]]
*Figure: l.StyleDoctorprovidesamulti-dimensionalevaluationofstyleconsistencybetweentheinputimagesandthestyleconditions. Buildingupontis,StylDoctoreablesaadageofstyleatedgerationtasks,cludingtextontrodstylegeeratioeee image-guided style generation,instruction-guided style transfer and reference image-guided style transfer*



StyleDoctor 的核心架构由三个紧密耦合的模块构成，分别负责全局风格特征提取、跨模态风格语义融合以及统一偏好学习。以下逐一拆解各模块的设计动机、输入输出与关键公式。

### 全局风格特征学习（Global Style Feature Learning）

现有风格编码器（如 **CSD** (Somepali et al., arXiv 2024)、**StyleTokenizer** (Li et al., ECCV 2024)）仅依赖图像特征进行对比学习，缺乏文本语义的跨模态监督，导致其对风格的理解停留在视觉表层，难以捕捉笔触纹理、色彩搭配等细粒度风格属性。StyleDoctor 的核心突破在于将风格特征学习与多模态语言模型深度绑定：利用视觉编码器 $E_v$ 提取图像特征后，通过对比损失在全局层面学习风格一致性表征。

具体而言，对于一批 $N$ 个样本，每个样本包含一个锚点风格特征 $z_i$、一个正样本 $z_i^+$（风格一致的图像或文本描述）和若干负样本 $z_j^-$（风格不一致的样本），对比损失函数定义为：

$$
\mathcal{L}_{con} = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp\left(\sin(z_i, z_i^+) / \tau\right)}{\sum_{j=1}^{N}\exp\left(\sin(z_i, z_j^-) / \tau\right)}
$$

其中 $\sin(\cdot, \cdot)$ 表示余弦相似度，$\tau$ 为温度系数。该损失的核心作用是**最大化风格一致配对之间的余弦相似度，同时推开风格不一致的样本**，从而在特征空间中形成紧凑的风格簇。训练后的风格特征随后通过一个额外的投影层注入为特殊的风格令牌（style token），与标准视觉令牌并行输入到后续的多模态语言模型中。

### 风格令牌注入与多模态基座

StyleDoctor 采用 **Qwen2.5-VL-3B** 作为基座多模态大语言模型（MLLM），这是其区别于传统仅图像输入的奖励模型（如 **HPSv2** (Wu et al., arXiv 2023)）的关键架构选择。该模块的工作流程如下：

1. **视觉编码**：视觉编码器 $E_v$ 提取输入图像（参考内容图、参考风格图、待评估生成图）的视觉令牌。
2. **风格令牌注入**：前一阶段学习到的全局风格特征经过一个额外的投影层，转化为专用的风格令牌，与标准视觉令牌并行输入到 Qwen2.5-VL-3B 中。
3. **指令输入**：模型同时接收文本指令（如“判断生成图像是否与参考风格一致”），实现图像与文本的联合推理。

这种设计使得 StyleDoctor 能够同时捕捉图像级风格特征和文本级风格语义，支持多种输入格式的风格一致性验证，包括文本控制风格生成、参考图像引导风格生成、指令引导风格迁移等场景。

### 统一偏好学习（Unified Preference Learning）

传统奖励模型通常仅输出单一的美学分数，无法捕捉风格一致性的多维度特性。StyleDoctor 将风格评估重新定义为**生成式统一偏好学习**任务：模型被训练来判断输入图像是否在风格上与给定的文本描述或参考风格图像对齐。

在训练阶段，来自 SPRData 的四元组样本（参考内容图、参考风格图、正例风格迁移图、负例风格迁移图）被重组为多种输入格式，模拟不同下游任务中的风格验证场景。模型需要输出正面或负面的风格一致性判断。在推理阶段，StyleDoctor 并非直接输出离散标签，而是**使用输出 logits 空间中正面答案的平均置信度作为连续奖励信号**，该信号涵盖了全局风格一致性、色彩和谐度、笔触纹理等多个维度。

### 关键设计要点总结

| 模块 | 核心机制 | 与基线的本质差异 |
|------|---------|----------------|
| 全局风格特征学习 | 对比损失 + 风格令牌注入 | 从纯图像对比学习升级为与 MLLM 深度耦合的风格表征 |
| 多模态基座 | Qwen2.5-VL-3B 联合图像与文本推理 | 替代仅图像输入的 CLIP/Reward 模型，引入文本语义监督 |
| 统一偏好学习 | 四元组重组 + 置信度奖励 | 从单一美学分数升级为多维风格一致性信号 |

消融实验（Table 7）表明，去除全局风格特征学习（GSF）和统一偏好学习（UPL）会导致风格一致性和 CSD 分数显著下降，验证了上述两个模块在 StyleDoctor 中的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/002_Figure.jpg]]
*Figure: Reward Modeling*



## 实验与关键发现

### 风格感知能力评估

StyleDoctor 首先在风格感知任务上接受检验，包括风格图像检索和多模态风格理解两个维度。如表 2 所示，StyleDoctor 在 Style30k 风格图像检索任务上取得了 **75.46%** 的准确率，较此前最优的专用风格编码器 **StyleTokenizer**（Li et al., ECCV 2024）的 69.98% 提升了 **+5.48 个百分点**。在多模态风格理解任务上，StyleDoctor 达到 **71.14%** 的准确率，超越了包括 **GPT-4o**（68.0%）在内的通用多模态大语言模型。这一结果验证了核心设计思路的有效性：将全局风格特征作为专用令牌注入多模态语言模型，使模型能够同时捕获图像级风格特征和文本级风格语义，从而实现对风格一致性的精准判断。

### 风格生成与迁移性能

将 StyleDoctor 作为奖励模型集成到生成模型的强化微调流程中，是验证其实际价值的关键环节。实验覆盖了文本控制风格生成、参考图像引导风格生成、指令引导风格迁移和参考图像引导风格迁移四类任务。

在文本控制风格生成任务上，以 **OmniGen2** 为基础模型，经 StyleDoctor 微调后，由 StyleDoctor 自身评判的风格准确率达到 **69.58%**，由 GPT-4o 评判的准确率为 **67.60%**（表 3）。在参考图像引导风格生成任务上，微调后的 OmniGen2 将 CSD 相似度提升至 **0.72**。

在风格迁移任务上（表 4），以 **OmniStyle** 为基础模型，经 StyleDoctor 微调后 CSD 分数达到 **0.78**，同时在内容保持度上（CLIP 视觉编码器和 DINO v2 特征相似度）保持了竞争力。这表明 StyleDoctor 提供的奖励信号能够在强化风格一致性的同时，避免对内容结构的过度破坏。

### 与传统人类偏好奖励模型的对比

表 6 直接对比了 StyleDoctor 与现有人类偏好奖励模型在风格生成任务上的表现。在风格定制化场景（B-LoRA 集成）中，StyleDoctor 取得了 **71.14%** 的风格准确率和 **0.78** 的 CSD 分数，而人类偏好奖励模型仅达到 66.54% 和 0.69。这一 **+4.60 个百分点** 的风格准确率提升和 **+0.09** 的 CSD 增益，揭示了现有奖励模型（如 **HPSv2**，Wu et al., arXiv 2023）的核心瓶颈：它们主要面向通用美学偏好，缺乏对风格维度（色彩和谐度、笔触纹理、全局风格一致性）的细粒度感知能力。StyleDoctor 通过多维度风格信号弥补了这一缺陷。

### 消融实验

消融实验（表 7）系统拆解了 StyleDoctor 两大核心组件的贡献：**全局风格特征学习（GSF）** 和 **统一偏好学习（UPL）**。当移除全局风格特征学习模块时，模型退化为仅依赖视觉令牌的标准多模态语言模型，风格一致性和 CSD 分数出现显著下降。当进一步移除统一偏好学习（即仅采用单一格式的偏好训练）时，性能再次大幅滑坡。这组消融实验以高置信度（0.98）证实：全局风格特征的显式注入和跨格式的统一偏好训练，是 StyleDoctor 有效性的两个不可或缺的支柱。

### 风格定制化集成

在风格定制化任务中（表 5），StyleDoctor 被用作额外的正则化项，与 **B-LoRA** 方法联合优化扩散模型。实验以 SDXL 为基础模型，集成 StyleDoctor 后在 CSD 指标上达到 **0.78**，较基线有明显提升。这展示了 StyleDoctor 的另一种应用范式：不仅可作为强化学习中的奖励信号，还可直接作为扩散模型微调过程中的风格对齐正则化器，通过最大化风格置信度来约束生成方向。

### 定性分析

图 5 和图 6 分别展示了文本控制风格生成和风格迁移任务的定性结果。在文本控制场景中，经 StyleDoctor 微调的模型生成的图像在色彩搭配、纹理细节和整体氛围上与目标风格描述更为一致。在风格迁移场景中，微调后的模型在保持内容结构的同时，更忠实地迁移了参考图像的风格特征（如油画笔触、水彩晕染效果）。这些视觉对比进一步佐证了定量指标的提升。

### 补充图表

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/007_Table_2.jpg]]
*Table 2: Comparison of style perception performances on style image retrieval and multi-modal style understanding between different vision encoders and MLLMs.Retri．Acc.and MMUnd. Acc.denote image retrieval accuracy and multi-modal style understanding accuracy,respectively*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/010_Table_3.jpg]]
*Table 3: Comparison of style generation performances.For textcontrolled style generation performances,we report the style generation accuracy judged by StyleDoctor and GPT-4o.For reference image-guided style generation,we report the CSD similarity*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/011_Table_4.jpg]]
*Table 4: Comparison of style transfer performances.For style consistency,we report CSD score and prediction from GPT-4o.For content preservation,we report similarity of visual features between the generated image and the reference content,where CLIP visual encoder and DINO v2 [23] is applied*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/015_Table_6.jpg]]
*Table 6: Performance comparison of human-preference reward models and StyleDoctor*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/014_Table_7.jpg]]
*Table 7: ．Ablation study on the effectiveness of each proposed component in StyleDoctor.GSF denotes Global Style Feature learning, UPL denotes Unified Preference learning*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/009_Figure_5.jpg]]
*Figure 5: SOTAmetodsintext-ontroledstylegenerationadreferenceimageguidedstylegenerationtasks*indicatesf-unedwith StyleDoctor*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/013_Figure_6.jpg]]
*Figure 6: QuantitativevisualizationofSOTAmethods ininstruction-guided styletransferandreference image-guidedstyle transfer.* indicates fine-tuned with StyleDoctor*

![[assets/figures/papers/paper_list_l2704_https_openaccess_thecvf_com_content_CVPR2026_html_He_StyleDoctor_Towards/figures/005_Table_1.jpg]]
*Table 1: Comparisons between diferent style-related datasets and SPRData. # indicates 'the number of'*



## 定位与知识库关联

### 1. 与现有奖励模型的关系

StyleDoctor 的提出直接回应了当前人类偏好奖励模型在风格感知上的结构性缺陷。现有主流奖励模型，如 **HPSv2**（Wu et al., arXiv 2023），其训练目标聚焦于通用美学质量与图文对齐，缺乏对风格一致性这一细粒度维度的建模能力。这导致它们在评估风格化生成结果时，无法区分“好看但不符风格”与“既好看又符风格”的样本——这一瓶颈被本文明确识别为**现有奖励模型无法有效感知图像风格**。

从范式演进角度看，StyleDoctor 完成了两个关键跨越：

- **从单模态到多模态的风格感知**：传统风格编码器（如 **CSD**，Somepali et al., arXiv 2024；**StyleTokenizer**，Li et al., ECCV 2024）仅通过图像对比学习提取全局风格特征，缺少文本语义监督，无法回答“这幅画是否符合‘水墨风格’”这类跨模态查询。StyleDoctor 以多模态大语言模型 Qwen2.5-VL-3B 为底座，将风格感知从纯视觉匹配扩展为视觉-语言联合推理。

- **从单一评分到多维风格信号**：现有奖励模型输出单一标量分数，而 StyleDoctor 提供覆盖全局风格一致性、色彩和谐度、笔触纹理的多维评估，并通过正例答案的平均置信度作为奖励分，使信号更细粒度。

### 2. 与风格迁移/生成方法的关系

StyleDoctor 在生成管线中扮演的是**即插即用的风格评估器与优化引导器**角色，而非替代现有生成模型架构。论文展示了三种集成模式：

- **作为强化微调的奖励模型**：将 StyleDoctor 接入 **OmniStyle** 和 **OmniGen2** 的强化微调流程，CSD 分数分别提升至 0.78 和 0.72。这表明 StyleDoctor 提供的风格一致性信号能有效引导扩散模型向目标风格靠拢。

- **作为正则化项**：在 **B-LoRA** 风格定制化方法中，StyleDoctor 被用于计算额外的风格对齐正则项，使风格准确率从 66.54% 提升至 71.14%，CSD 从 0.69 提升至 0.78。这验证了其作为优化约束的有效性。

- **与负向嵌入方法的区别**：**ReNeg** 等方法通过负向嵌入学习避免特定风格，属于“排斥式”风格控制；StyleDoctor 则提供“吸引式”的正向风格一致性信号，两者在机制上互补。

### 3. 适用边界与局限

尽管论文未显式列出局限性，但从方法设计与实验设置中可以推断以下适用边界：

- **风格覆盖依赖数据集分布**：SPRData 涵盖 1,000 种风格类别，但风格世界远不止于此。对于数据集中未充分代表的少数民族艺术风格、高度个人化的插画风格等小众领域，StyleDoctor 的评估能力需要进一步验证——这一点被论文列为开放问题之一。

- **多维奖励的可分解性未验证**：StyleDoctor 声称提供色彩、笔触等多维信号，但当前奖励输出仍聚合为单一置信度分数。能否将这些维度解耦为独立可优化的信号，尚属开放问题。

- **视频风格的跨帧一致性未探索**：论文仅在单帧图像层面验证了 StyleDoctor 的有效性，其在视频风格迁移中的跨帧风格一致性评估能力仍待研究。

- **基座模型规模限制**：StyleDoctor 基于 Qwen2.5-VL-3B（3B 参数），相较于更大规模的 MLLM，其风格语义理解的上限可能受模型容量制约。论文未与更大规模模型进行系统对比。

### 4. 开放问题与未来方向

论文明确提出的开放问题指向以下研究方向：

1. **小众风格的泛化能力**：StyleDoctor 能否在 SPRData 未覆盖的风格上保持判别力，需要跨分布测试验证。

2. **多维奖励信号的独立优化**：将色彩和谐度、笔触纹理等维度解耦，支持用户按需调整风格子属性的权重，是实现精细风格控制的下一步。

3. **从奖励模型到风格感知组件**：StyleDoctor 能否直接作为 VLM 的风格感知模块嵌入生成模型，而非仅在训练阶段提供奖励信号，这关系到其应用范式的根本性扩展。

4. **视频风格迁移的跨帧评估**：将 StyleDoctor 的风格一致性判别能力扩展到时间维度，是通往视频风格化质量评估的自然延伸。



## 原文 PDF

![[paperPDFs/CVPR_2026/StyleDoctor_Towards_Specialist_Reward_Model_for_Style_centric_Generation_Tasks.pdf]]

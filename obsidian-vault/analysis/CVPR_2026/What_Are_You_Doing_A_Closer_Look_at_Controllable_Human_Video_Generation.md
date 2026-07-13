---
title: What Are You Doing? A Closer Look at Controllable Human Video Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/What_Are_You_Doing_A_Closer_Look_at_Controllable_Human_Video_Generation.pdf
project_link: null
code_link: "https://github.com/google-deepmind/wyd-benchmark"
aliases:
- WEPB
- WAYDCLACHVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过构建包含56个细粒度子类别和人工标注分割掩码的WYD基准，并结合人类验证的新指标（如pAPE），可以系统性地揭示模型在复杂人类动作、多演员、交互和运动下的失败模式。
primary_logic: 精细化的基准、人类级别的评估指标与人类偏好研究相结合，能够有效诊断当前SOTA模型在生成人类视频时的六大系统性局限性，为未来模型改进提供明确方向。
claims:
- WYD基准在视觉质量和运动方面均比TikTok/TED-Talks显著更难，错误率高出1.8-12.3倍。
- 所提出的pAPE指标在评估人类运动时与人类偏好的一致性比pOFE高10%。
- 现有的广泛使用的FID指标无法可靠评估视频质量，而FVD与人类判断高度一致。
- 精细化类别分析揭示了模型在身份崩溃、物体消失、非典型动作等方面的失败。
---

# What Are You Doing? A Closer Look at Controllable Human Video Generation

> [!tip] 核心洞察
> 精细化的基准、人类级别的评估指标与人类偏好研究相结合，能够有效诊断当前SOTA模型在生成人类视频时的六大系统性局限性，为未来模型改进提供明确方向。

| 字段 | 内容 |
|------|------|
| 中文题名 | 你在做什么？可控人类视频生成细粒度评测 |
| 英文题名 | What Are You Doing? A Closer Look at Controllable Human Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.04666) · [Code](https://github.com/google-deepmind/wyd-benchmark) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | WYD Evaluation Protocol and Benchmark |
| Dataset | WYD16 |

> [!tip] 效果简介
> - WYD16 上，pICD 1.8-4.6x higher error than TikTok/TED-Talks vs TikTok/TED-Talks (WYD significantly harder)；FVD vs human preference Spearman correlation 96.36% vs FID 22.24% (FVD far more reliable)；ICD vs pixel metrics 72.67% accuracy vs PSNR 59.04%, SSIM 62.65% (ICD matches human preferences best)。

## 概要

可控人类视频生成旨在根据给定的控制信号（如姿态、深度图或边缘图）驱动参考图像中的人物，使其执行特定动作。然而，现有基准（如TikTok、TED-Talks）在动作多样性、演员数量、交互类型、遮挡程度和场景变化等方面严重不足，导致无法全面评估和诊断模型在真实复杂场景下的精细化能力。

本文提出**WYD（What Are You Doing?）**基准与评估协议，核心贡献包括：（1）一个包含1,544个高质量视频、覆盖9大类56个细粒度子类别的多样化数据集，并附带人工标注的演员分割掩码；（2）一套经过人类偏好验证的标准化评估指标体系，涵盖视频级质量、逐帧正确性和运动保真度，其中**pAPE**（基于姿态关键点相似度的平均精度补数）专门量化生成人体运动的忠实度；（3）对七种SOTA可控视频生成模型的系统性诊断，揭示了当前模型在身份崩溃、物体消失、非典型动作、多演员和高遮挡场景等六大方面的系统性局限。

实验表明，WYD比TikTok/TED-Talks在视觉质量和运动指标上困难1.8–12.3倍；所选的FVD和ICD指标与人类判断高度一致（Spearman相关性达96.36%），而广泛使用的FID则无法可靠评估视频质量；pAPE在人体运动评估上与人类偏好的一致性比传统光流指标pOFE高出10%。在所有模型中，深度条件模型TF-T2V综合表现最优，姿态条件模型中MimicMotion和ControlNeXt表现最佳，但没有单一模型在所有指标上全面领先。

该基准无意涵盖所有文化群体，可能延续训练数据中的偏见；pAPE依赖姿态检测器的鲁棒性；面部质量评估尚未纳入体系；当前评估局限于图像到视频的条件生成设置。

可控人类视频生成旨在根据结构条件（如姿态、深度图、边缘图）驱动参考图像中的人物运动，其在电影制作、虚拟现实、社交媒体等领域具有广阔应用前景。近年来，扩散模型的快速发展催生了大量可控视频生成模型，如 **MagicAnimate**、**MimicMotion**、**ControlNeXt** 等姿态条件模型，以及 **Control-A-Video**、**Ctrl-Adapter**、**TF-T2V** 等深度/边缘条件模型，在特定基准上展现出令人印象深刻的生成能力。

然而，该领域的评估体系存在显著的瓶颈：现有常用基准数据集（如 TikTok、TED-Talks）在动作、演员数量、交互、遮挡、场景和相机运动等维度上缺乏多样性。如 Figure 1 和 Figure 2 所示，WYD 的作者对 TikTok 和 TED-Talks 进行人工标注后发现，这两个数据集在全部九个评估类别上均表现出明显的多样性不足。这种单一性导致现有基准无法全面评估和诊断模型在不同真实场景下的精细化能力，模型的系统性失败模式难以被有效暴露。

在评估指标方面，该领域长期依赖像素级指标（PSNR、SSIM）和 FID 等图像质量指标。然而，这些指标已被证明无法可靠评估视频生成质量：FID 无法有效惩罚时序闪烁和伪影，而 FVD 则能更好地捕捉这些缺陷（见 Figure 8）。更关键的是，现有指标缺乏对人类运动保真度的专门量化手段——没有专门的基于姿态的运动度量来评估生成视频中人体动作与参考视频的一致性。

上述双重缺口——基准的多样性不足和评估指标的粗粒度——构成了本文的核心动机：需要构建一个更具挑战性、更细粒度的基准，并配套经过人类验证的评估协议，以系统性地诊断当前 SOTA 模型的局限性，为未来模型改进提供明确方向。

## 核心方法与创新机理

本文的核心贡献并非提出新的视频生成模型，而是构建了一套系统性的**评估协议与基准**，用以诊断当前可控人类视频生成模型的真实能力边界。其创新性集中体现在三个相互耦合的“changed slots”上。

### 从聚合指标到细粒度类别诊断

现有基准（如TikTok、TED-Talks）仅提供数据集级别的聚合分数（如FID），掩盖了模型在不同场景下的能力差异。本文的核心创新在于将评估粒度从“数据集整体”下钻至**9大类别、56个子类别**的细粒度层面。通过人工标注，WYD基准覆盖了演员数量、动作类型、交互复杂性、遮挡程度、场景多样性等关键维度（Figure 2）。这种精细化分类使得研究者能够系统性地定位模型的失败模式，而非仅获得一个笼统的性能排名。例如，分析直接揭示了模型在“多演员”、“小尺寸演员”和“高遮挡”场景下的性能坍塌（Figure 42），以及在“涉及动物的动作”、“骑行”、“跑跳”等非典型动作上的显著退化（Figure 43）。这种从“整体打分”到“分项诊断”的转变，是评估范式上的关键突破。

### 从像素级指标到人类验证的感知指标

传统评估依赖PSNR、SSIM等像素级指标，以及广泛使用但已被证明不可靠的FID。本文通过大规模人类偏好研究，筛选并确立了与人类判断高度一致的指标组合，构成了第二个关键创新槽位。

- **视频质量评估**：验证了FVD（Spearman相关系数96.36%）远优于FID（22.24%），因为FVD能有效惩罚生成视频中的闪烁和伪影（Figure 8, Table 2）。
- **逐帧正确性**：ICD（基于DINOv2特征的帧间距离）以72.67%的成对准确率超越了PSNR（59.04%）和SSIM（62.65%）。
- **视频运动评估**：OFE（光流终点误差）被用作结构差异的度量。

在此基础上，本文进一步提出了**人本化指标**（pFVD、pICD、pAPE），利用人工标注的分割掩码将评估聚焦于人类演员本身，排除了背景干扰。这一“视频级→人类级”的指标递进，使得对人类生成质量的测量更为精准。

### pAPE：面向人体运动保真度的姿态级指标

现有评估体系缺乏专门量化人体运动保真度的指标。本文提出的**pAPE**填补了这一空白，构成了第三个核心创新。pAPE的计算逻辑如下：

$$ \text{pAPE} = 1 - \text{AP} $$

其工作机制是：分别在参考视频和生成视频中检测2D人体姿态关键点，计算关键点相似度的平均精度（AP），然后取其补数作为误差指标。pAPE的独特价值在于它能捕捉人类观察者不敏感但客观存在的运动偏差。例如，它能检测到MimicMotion中生成姿态相对于参考姿态的“重缩放”和“重居中”问题（Figure 10），而人类评估者往往会忽略此类细微变化。在人类偏好一致性上，pAPE（71.95%准确率）比基于光流的pOFE（61.45%）高出约10个百分点（Table 2），证明其在刻画人体运动保真度方面更为有效。

### 创新协同：基准-指标-诊断的闭环

上述三个创新并非孤立存在。WYD的细粒度类别为pAPE等指标提供了差异化的测试场景，暴露了模型在特定条件下的系统性缺陷；而经过人类验证的指标组合则确保了诊断结论的可靠性。这一“**精细化基准 × 人类对齐指标 × 系统性诊断**”的闭环，构成了本文方法学上的核心贡献，为未来可控人类视频生成模型的改进提供了明确的靶向指引。

WYD评估体系由两条并行且相互验证的主线构成：**精细化基准构建**与**人类对齐的评估协议**。前者解决“测什么”的问题，后者解决“怎么测”的问题，二者共同形成对可控人类视频生成模型的系统性诊断能力。

### 基准构建流水线

WYD基准的构建遵循一条严格的7步过滤流水线（Figure 27），从三个公开许可的互联网视频数据集（Kinetics、DiDeMo、Oops）出发，最终产出1,544个高质量视频。流水线的核心瓶颈在于**多样性过滤与人工验证**——每一步都在剔除那些无法暴露模型真实能力的“简单”样本：

![[assets/figures/papers/paper_list_l1005_https_arxiv_org_abs_2503_04666/figures/036_Figure_27.jpg]]
*Figure 27: | wyd data filtering pipeline. Our pipeline includes 7 steps: identifying videos with human actors, removing scene cuts, ensuring human visibility, removing short/long videos, keeping videos with high text alignment, removing low-res videos and manual verification*

1. **人类演员识别**：筛选包含人类主体的视频。
2. **场景切换移除**：排除包含镜头切换的片段，确保单段视频内时序一致性。
3. **人体可见性保证**：确保人类演员在画面中清晰可见。
4. **长度过滤**：剔除过短或过长的视频，保持评估效率与信息量的平衡。
5. **文本对齐筛选**：保留与描述文本高度一致的视频，为未来文本控制评估预留空间。
6. **分辨率过滤**：移除低分辨率视频，避免编码伪影干扰评估。
7. **人工验证**：对模糊、光照、相机稳定性、运动量、字幕清晰度及首帧演员存在性进行逐条审查，耗时超过250小时。

这一流水线的因果机制在于：传统基准（如TikTok、TED-Talks）的样本分布集中在单人、正面、简单动作的“舒适区”，而WYD通过系统性剔除这些简单样本，将评估推向模型能力的边缘地带。证据显示，WYD在视觉质量和运动保真度上的错误率分别比TikTok/TED-Talks高出1.8-4.6倍（pICD）和1.8-12.3倍（pAPE），验证了基准难度的显著提升（Figure 4）。

### 细粒度标注体系

在视频筛选完成后，WYD为每个视频分配了覆盖**9大类别、56个子类别**的人工标注（Figure 2）。这些类别从人类视频生成的核心维度出发，包括：演员数量、演员尺寸、遮挡程度、动作类型、相机运动、场景类型、交互对象等。与TikTok和TED-Talks的对比标注显示，后者在全部9个类别上均表现出显著的多样性缺失（Figure 2）。这一标注体系是后续细粒度诊断分析的基础——它使得研究者能够精确归因模型在“多演员场景”“非典型动作”“高遮挡条件”等具体子类下的失败模式。

### 人类分割掩码生成

为实现人类层级的评估指标，WYD需要精确的演员分割掩码。掩码生成采用**检测-跟踪-校正**的三阶段流程：首先使用OWLv2在第一帧检测人体边界框，经人工筛选和精修后，将边界框输入SAM 2进行全视频跟踪，最后在帧级别进行人工校正。这一流程确保了掩码精度足以支撑后续pFVD、pICD、pAPE等人类中心指标的计算。

### 评估协议的双层架构

评估协议采用**视频级**与**人类级**双层架构（Figure 3左/右）：

- **视频级评估**：在全帧范围内计算FVD（视频质量）、ICD（逐帧正确性）和OFE（视频运动），衡量生成视频的整体保真度。
- **人类级评估**：利用分割掩码将评估聚焦于人类区域，计算pFVD、pICD和pAPE，专门衡量模型对人体外观和运动的重建能力。

其中，pAPE是本文提出的关键创新指标，定义为检测到的2D姿态关键点相似度的平均精度（AP）的补数：$\text{pAPE} = 1 - \text{AP}$。与现有基于光流的运动指标pOFE相比，pAPE在评估人类运动时与人类偏好的一致性高出10%（71.95% vs 61.45%，Table 2），且能捕捉到人类观察者不敏感但对模型诊断至关重要的细微姿态偏差（如MimicMotion中的姿态重缩放，Figure 10）。

### 指标的人类验证闭环

整个评估协议的有效性建立在**人类偏好研究**之上。通过大规模并列评估，研究发现FVD和JEDi与人类判断高度一致（Spearman相关系数96.36%），而广泛使用的FID几乎无法可靠评估视频质量（仅22.24%）。ICD在逐帧正确性上以72.67%的准确率优于传统像素级指标PSNR（59.04%）和SSIM（62.65%）（Table 2）。这一验证闭环确保了WYD的自动评估结果能够忠实地反映人类感知，为模型排名和诊断提供可信基础。

### 输入输出流

整个框架的输入为原始视频数据集和待评估的生成模型，输出为多维度的细粒度性能诊断报告。具体而言：参考视频经7步流水线筛选和人工标注后形成WYD基准；模型以参考视频的首帧及对应条件（姿态/深度/边缘）为输入生成视频；生成视频与参考视频在视频级和人类级两个层级上计算FVD/pFVD、ICD/pICD、OFE/pAPE等指标；最终按56个子类别聚合结果，揭示模型在不同维度上的能力瓶颈。

![[assets/figures/papers/paper_list_l1005_https_arxiv_org_abs_2503_04666/figures/004_Figure_3.jpg]]
*Figure 3: | Overall performance (left: video-level, right: human-level) of SOTA controllable image-to-video models on wyd16. Pose models are shown in pink, depth ones in blue, and edge ones in orange. Human generation is multifaceted and no model prevails across all metrics*

### WYD评估协议的核心架构

WYD评估协议由三个层次化模块构成，分别对应视频级质量、人类级保真度和指标验证：

**1. 视频级评估模块**
该模块对生成视频的整体质量进行多维度量化，采用经过人类偏好验证的三个指标：
- **FVD**（Fréchet Video Distance）：衡量生成视频与参考视频在时序特征空间中的分布距离，有效惩罚闪烁和伪影（见Figure 8）。
- **ICD**（Instance Correspondence Distance）：基于DINOv2编码器提取的逐帧视觉特征，计算帧间实例对应关系的相似度，评估逐帧视觉正确性。
- **OFE**（Optical Flow Endpoint Error）：通过比较生成视频与参考视频的光流场，量化运动结构的差异。

**2. 人类级评估模块**
该模块利用人工标注的分割掩码，将评估聚焦于人类演员区域，提出三个以“p”（people）为前缀的变体指标：
- **pFVD**：仅在人类分割掩码区域内计算FVD。
- **pICD**：仅在人类分割掩码区域内计算ICD。
- **pAPE**：新提出的姿态误差指标（见下文公式推导），专门量化生成视频中人体运动的保真度。

**3. 指标验证模块**
通过大规模人类偏好研究（SxS，即并排比较），对所有自动指标进行验证，筛选出与人类判断一致性最高的指标组合。验证结果（Table 2）显示：FVD与人类偏好的Spearman秩相关系数达96.36%，而广泛使用的FID仅为22.24%；ICD的成对准确率为72.67%，显著优于PSNR（59.04%）和SSIM（62.65%）。

![[assets/figures/papers/paper_list_l1005_https_arxiv_org_abs_2503_04666/figures/009_Table_2.jpg]]
*Table 2: | Side-by-side evaluations. We report Spearman rank correlation for video quality, and pair-wise accuracy for the rest. Our selected metrics agree with human preferences from SxS studies*

### 关键公式：pAPE

pAPE（people Average Pose Error）是WYD协议中唯一新提出的指标，用于量化生成视频中人体姿态相对于参考视频的误差：

$$\text{pAPE} = 1 - \text{AP}$$

**变量含义：**
- **AP**（Average Precision）：在参考视频和生成视频中分别检测2D人体姿态关键点，计算关键点相似度的平均精度。具体而言，对每一帧中检测到的人体关键点集合，计算生成姿态与参考姿态之间的空间对齐精度，然后对所有帧取平均。
- **pAPE**：取AP的补数（即1 − AP），作为误差指标。pAPE值越低，表示生成的人体运动越忠实于参考视频。

该指标的设计动机在于：传统的光流误差（pOFE）在评估人体运动时与人类偏好的一致性仅为61.45%，而pAPE达到了71.95%（Table 2），提升约10个百分点。pAPE对姿态缩放和重居中特别敏感（如Figure 10所示，MimicMotion生成视频中的姿态被重新缩放，人类观察者对此不敏感，但pAPE能正确捕获此类偏差），这使其成为诊断姿态条件模型失败模式的有效工具。

**注意**：pAPE的性能受限于底层姿态检测器对高度遮挡或非典型姿态的鲁棒性，这是该指标的已知局限。

## 实验与关键发现

### 基准难度验证：WYD 对现有模型构成显著挑战

为了验证 WYD 基准的难度提升，我们将姿态条件模型在 WYD16 上的表现与在 TikTok 和 TED-Talks 上的表现进行了对比。如 Figure 4 所示，WYD 在视觉质量和人体运动两个维度上均显著更难：**pICD** 误差高出 1.8–4.6 倍，**pAPE** 误差高出 1.8–12.3 倍。这一结果表明，现有基准的有限多样性掩盖了模型在真实复杂场景下的能力短板，而 WYD 的细粒度类别设计成功暴露了这些差距。

![[assets/figures/papers/paper_list_l1005_https_arxiv_org_abs_2503_04666/figures/005_Figure_4.jpg]]
*Figure 4: | Performance comparison between wyd, TikTok and TED-Talks for pose-conditioned models. wyd yields larger errors, confirming that its greater diversity is more challenging for models*

### 自动指标与人类偏好的一致性验证

我们通过大规模并列人类偏好研究验证了所选自动指标的可靠性。Table 2 汇总了各指标与人类判断的一致性：

- **视频质量**：FVD 和 JEDi 与人类偏好的 Spearman 秩相关系数高达 96.36%，而广泛使用的 FID 仅为 22.24%，VMAF 同样表现不佳。这表明 FID 无法可靠评估视频质量，FVD 能有效惩罚闪烁和伪影（见 Figure 8）。
- **逐帧正确性**：基于 DINOv2 特征的 ICD 取得了 72.67% 的成对准确率，显著优于 PSNR（59.04%）和 SSIM（62.65%）。
- **人体运动保真度**：我们提出的 **pAPE** 指标取得了 71.95% 的准确率，比基于光流的 pOFE（61.45%）高出约 10 个百分点。如 Figure 9 和 Figure 10 所示，pAPE 能正确捕捉到 MimicMotion 中人类不敏感的**姿态重缩放**问题——生成视频中的人体姿态被重新缩放和居中，而 pOFE 对此类细微变化不够敏感。

### SOTA 模型总体性能分析

Figure 3 展示了 7 个 SOTA 可控图像到视频模型在 WYD16 上的视频级和人类级性能全景：

- **无单一模型全面领先**：人体视频生成是多维度的，没有模型在所有指标上同时占优。
- **深度条件模型 TF-T2V 整体最优**：在视频级指标（FVD、ICD、OFE）上表现最佳。
- **姿态条件模型中 MimicMotion 和 ControlNeXt 表现突出**：但在 pAPE 指标上暴露出姿态保真度问题。
- **边缘条件模型整体较弱**：尤其在运动保真度（OFE/pOFE）方面存在明显不足。

被评估模型的训练数据、条件类型及与 WYD 数据集的重叠情况详见 Table 3。

### 细粒度失败模式诊断

利用 WYD 的 9 大类 56 个子类别标注，我们系统性地诊断了当前 SOTA 模型的六大局限性：

#### 1. 演员数量、尺寸与遮挡的敏感性

Figure 42 揭示了最佳模型在不同场景下的性能分化：

- **多演员场景**：动画化多个演员比单人视频显著更难，模型容易出现**身份崩溃**（如 Figure 5 中 TF-T2V 无法保持人物身份）。
- **小尺寸演员**：当演员在画面中占比较小时，生成精度明显下降，细节丢失严重。
- **高遮挡场景**：随着遮挡程度增加，模型性能持续退化，人体结构扭曲和部分肢体消失的频率上升。

#### 2. 动作类别的挑战性分级

Figure 43 按动作类别对最佳模型进行了性能剖析：

![[assets/figures/papers/paper_list_l1005_https_arxiv_org_abs_2503_04666/figures/054_Figure_43.jpg]]
*Figure 43: | Performance of best models w.r.t. ‘Actions.’ Actions involving animals, riding a vehicle, running and jumping, and boardsports are challenging for SOTA models (especially pose-conditioned ones). Atypical movements, e.g., standing up and falling down, are also hard*

- **高难度动作**：涉及**动物互动、骑行、跑跳和滑板类运动**的动作对 SOTA 模型极具挑战，姿态条件模型在这些类别上表现尤其糟糕。
- **非典型动作**：如**站立起身和跌倒**等异常运动模式同样难以合成，模型倾向于生成不自然的过渡或形态扭曲。
- **常规动作**：行走、站立等常见动作的生成质量相对稳定，但在复杂背景下仍会出现伪影。

#### 3. 运动量与相机动态的影响

Figure 44 的分析显示：

- **全身运动**和**高运动量**视频的生成质量显著低于静态或小幅运动场景。
- **动态相机**（如跟拍、摇镜）增加了生成难度，但深度条件模型 TF-T2V 在此类视频上具有更低的 OFE，表现出对相机运动更强的鲁棒性。

#### 4. 交互与场景的复杂性

Figure 45 表明：

![[assets/figures/papers/paper_list_l1005_https_arxiv_org_abs_2503_04666/figures/056_Figure_45.jpg]]
*Figure 45: | Performance of best models w.r.t. ‘Interactions’ and ‘Scenes.’ Generating videos of humans interacting with animals or other humans is more difficult than solo videos. Outdoors scenes (e.g., on sand and snow, street, by the water) are also harder for SOTA models*

- **交互场景**：与动物或他人交互的视频比单人视频更难生成，模型在保持多主体空间关系和时序一致性方面存在困难。
- **户外场景**：沙滩、雪地、街道等复杂背景下的生成质量低于室内简单背景，模型容易产生背景与前景的不协调融合。

#### 5. 文本引导的消融影响

Figure 41 展示了为深度/边缘条件模型添加文本引导的影响：

- **总体正向**：添加文本引导通常能提升模型性能，尤其在视觉质量维度。
- **例外情况**：Control-A-Video 在使用深度或边缘条件时，其 pFVD 反而恶化，提示该模型的文本条件融合机制可能存在冲突。

#### 6. 身份保持与物体持久性

深度条件模型（如 TF-T2V）虽然在整体指标上领先，但在**身份保持**方面存在明显缺陷：生成过程中人物面部特征、衣着颜色可能发生突变。姿态条件模型则在**物体持久性**上表现不佳——人物手持或交互的物体在视频帧间可能消失或变形。

### 关键图表汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 3 | SOTA 模型全景对比，无模型全面领先 |
| Figure 4 | WYD 比 TikTok/TED-Talks 难 1.8–12.3 倍 |
| Table 2 | FVD、ICD、pAPE 与人类偏好高度一致 |
| Figure 8 | FVD 有效惩罚闪烁伪影，FID 不可靠 |
| Figure 9–10 | pAPE 揭示 MimicMotion 姿态重缩放问题 |
| Figure 42 | 多演员、小尺寸、高遮挡导致性能退化 |
| Figure 43 | 动物互动、骑行、跑跳、滑板为高难度动作 |
| Figure 41 | 文本引导总体正向，Control-A-Video 例外 |
| Figure 44–45 | 高运动量、动态相机、户外交互场景更具挑战 |

### 实验设置说明

WYD 数据集的构建经历了 7 步过滤流水线（详见 Figure 27），从 Kinetics、DiDeMo 和 Oops 三个公开许可数据集的 18,351 个视频中筛选出 1,544 个高质量视频。Table 4 记录了各过滤步骤后的数据量变化，Table 5 列出了从 StoryBench 标注中提取的独特人类演员。人工验证和细粒度标注累计耗时超过 250 小时，确保了基准的标注质量和类别覆盖度。

## 定位与知识库关联

### 可控视频生成的评估范式演进

本工作聚焦于**可控人类视频生成**的评估问题，其核心贡献在于构建了细粒度基准 **WYD** 及配套的人类验证评估协议，而非提出新的生成模型。因此，其方法定位需从“评估框架”的视角加以审视。

在 WYD 之前，可控人类视频生成的评估主要依赖两类范式：

1.  **数据集级聚合指标**：以 TikTok、TED-Talks 等数据集为代表，评估时计算全数据集的 FID、PSNR、SSIM 等像素级或分布级指标。这类范式的问题在于，数据集本身缺乏动作、交互、遮挡等维度的多样性（见图 2），且 FID 等指标已被验证与人类对视频质量的判断几乎不相关（Spearman 相关系数仅 22.24%，见表 2），无法有效诊断模型的精细化能力。
2.  **视频级运动指标缺失**：早期工作缺乏专门针对人体运动保真度的量化指标。虽然光流终点误差（OFE）可用于衡量运动一致性，但其对姿态的细微变化（如整体平移、缩放）不敏感，而人类观察者对此类变化也往往不敏感，导致指标与人类感知之间存在错位。

WYD 协议在上述基础上进行了三个关键槽位的替换：

| 评估槽位 | 基线取值 | WYD 取值 | 证据锚点 |
|:---|:---|:---|:---|
| 评估粒度 | 数据集级聚合分数（如 FID） | 跨 9 大类别、56 个子类别的细粒度类别化评估 | “we propose an evaluation protocol that spans key aspects of video generation as well as human-centric ones” |
| 视频质量指标 | 像素级指标（PSNR, SSIM）和 FID | 经人类验证的 FVD、ICD、OFE，及面向人的变体 pFVD、pICD | “we propose a standardized evaluation protocol with metrics that have been validated with human preferences” |
| 姿态运动指标 | 无专用姿态度量 | pAPE（1 − 关键点相似度平均精度） | “our pose-based metric (pAPE) better quantifies the fidelity of generated human movements” |

### 与 SOTA 生成模型的关系

WYD 评估了 7 个代表性的可控图像到视频生成模型，覆盖三类条件模态：

-   **姿态条件模型**：MagicAnimate、MagicPose、MimicMotion、ControlNeXt
-   **深度条件模型**：Control-A-Video、TF-T2V
-   **边缘条件模型**：Ctrl-Adapter

这些模型并非 WYD 的“基线”被超越，而是作为**被测对象**，通过 WYD 的细粒度类别分析暴露出六大系统性局限：

1.  **身份崩溃**：深度条件模型 TF-T2V 在生成过程中会丢失人物身份特征（见图 5）。
2.  **物体消失**：姿态条件模型 MimicMotion 在处理人与动物交互时，动物会从画面中消失（见图 6）。
3.  **非典型动作失败**：站立、跌倒等非周期性动作对 SOTA 模型极具挑战（见图 43）。
4.  **多演员退化**：演员数量增加时，所有模型的性能均显著下降（见图 42）。
5.  **高遮挡失效**：演员被遮挡程度越高，生成质量越差（见图 42）。
6.  **小尺寸演员模糊**：当演员在画面中占比较小时，生成精度急剧下降（见图 42）。

### 适用边界与局限

WYD 协议的设计决策带来了以下适用边界：

-   **任务边界**：当前评估严格限定于**图像到视频**的可控生成设定（给定首帧和条件信号），未覆盖文本到视频（T2V）生成任务。将精细评估范式扩展到 T2V 是明确的开放问题。
-   **模态覆盖**：尽管 WYD 包含 9 大类别和 56 个子类别，但其视频来源为 Kinetics、DiDeMo 和 Oops 三个公开数据集，**无意涵盖所有文化群体**，可能延续训练数据中的偏见。鼓励未来工作拓宽社会和文化代表性。
-   **指标盲区**：pAPE 指标依赖姿态检测器（如 DWPose），其对高度遮挡或非典型姿态的鲁棒性存在上限。此外，WYD 尚未纳入面部质量或情感表达准确性的评估指标，而现有模型的面部生成质量普遍不佳。
-   **安全与成本**：视频生成模型可被滥用于制造虚假内容，实际部署须配合数字水印等措施。同时，当前 SOTA 模型训练成本高昂，需探索更高效的架构以减少碳排放。

### 开放问题

1.  **跨任务泛化**：如何将 WYD 的细粒度评估范式扩展到文本到视频生成，并设计相应的文本控制力指标？
2.  **指标补全**：如何设计指标以评估生成视频中人类面部质量和情感表达的准确性？
3.  **人机对齐**：如何进一步缩小自动评估指标与人类感知之间的差距，特别是在复杂人类动作和交互场景下？
4.  **基准演进**：WYD 的 56 个子类别是否足够覆盖未来模型的所有能力？基准应建立何种机制以持续扩展，跟上模型发展的步伐？
5.  **效率优化**：如何开发更高效的视频生成架构，在保持可控性的同时显著降低训练和推理成本？

## 原文 PDF

![[paperPDFs/CVPR_2026/What_Are_You_Doing_A_Closer_Look_at_Controllable_Human_Video_Generation.pdf]]

---
title: "Fine-grained Image Aesthetic Assessment: Learning Discriminative Scores from Relative Ranks"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Fine_grained_Image_Aesthetic_Assessment_Learning_Discriminative_Scores_from_Relative_Ranks.pdf
project_link: "https://yzc-ippl.github.io/FG-IAA/"
code_link: null
aliases:
- FGIAALDSFRR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将细粒度相对排序作为训练信号，通过差分保持Token化（DiffToken）、对比文本辅助对齐（CTAlign）和排序感知回归（RankReg）联合优化，使模型学习更具判别性的美学表征。
primary_logic: 通过从图像序列的相对排序中学习判别性美学分数，可以同时保持粗粒度评估能力，并显著提升细粒度美学区分能力。
claims:
- FGAesQ在FGAesthetics数据集的所有评估协议（成对级别和序列级别，三个图像源）上均取得最优性能。
- FGAesQ在粗粒度（AVA）和细粒度（FGAesthetics）评估之间取得了最佳平衡，证明其从相对排序中学习判别性分数的有效性。
- 消融实验表明，移除DiffToken、CTAlign或RankReg均导致细粒度性能显著下降，验证了每个模块对细粒度美学建模的贡献。
- FGAesthetics 上 Pair ((Acc+F1)/2 across categories) = 0.753
---

# Fine-grained Image Aesthetic Assessment: Learning Discriminative Scores from Relative Ranks

> [!tip] 核心洞察
> 通过从图像序列的相对排序中学习判别性美学分数，可以同时保持粗粒度评估能力，并显著提升细粒度美学区分能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 细粒度图像美学评估：从相对排序中学习判别性评分 |
| 英文题名 | Fine-grained Image Aesthetic Assessment: Learning Discriminative Scores from Relative Ranks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03907) · [Project](https://yzc-ippl.github.io/FG-IAA/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FGAesQ |
| Dataset | FGAesthetics, AVA |

> [!tip] 效果简介
> - FGAesthetics 上，Pair ((Acc+F1)/2 across categories) 0.753 vs 0.699 (Charm Fine-tuned) (+0.054)；Series ((s-Acc+s-SRCC)/2 across categories) 0.600 vs 0.477 (Charm Fine-tuned) (+0.123)。
> - AVA 上，SRCC / PLCC 0.770 / 0.781 vs 0.777 / 0.779 (Charm) (-0.007 / +0.002)。

## 概要

图像美学评估（Image Aesthetic Assessment, IAA）旨在让机器自动判断图像的视觉美感。现有IAA研究主要聚焦于**粗粒度评估**——对风格、内容差异显著的图像进行独立的绝对评分（如AVA数据集）。然而，在摄影选片、AIGC优选等实际场景中，用户面临的是视觉高度相似、美学差异微妙的**细粒度比较**问题：同一场景的多张连拍照片，哪一张更美观？在此类场景下，现有模型因难以提取判别性美学特征而性能急剧下降。

本文的核心洞察是：**从图像序列的相对排序中学习判别性美学分数，可以同时保持粗粒度评估能力，并显著提升细粒度美学区分能力。** 基于此，作者提出了**FGAesQ**框架，通过三个关键模块将细粒度相对排序转化为训练信号：
- **差分保持Token化（DiffToken）**：定位美学决定性区域，在差异区域保持原始分辨率细节，在相似区域降采样以节省计算；
- **对比文本辅助对齐（CTAlign）**：利用MLLM生成的对比文本描述与视觉嵌入差进行对齐，增强判别性表征；
- **排序感知回归（RankReg）**：基于Bradley-Terry模型和ListMLE损失，将预测的成对偏好概率与真实排序对齐。

同时，作者构建了**FGAesthetics**基准数据集，包含来自自然摄影、AIGC和裁剪三个来源的10,028个图像序列（32,217张图像），每个序列内图像视觉相似但美学质量存在可区分的差异。

实验结果表明，FGAesQ在FGAesthetics的所有评估协议上均取得最优性能：成对级别Pair指标达0.753（较最佳基线Charm提升+0.054），序列级别Series指标达0.600（提升+0.123）；同时，在粗粒度AVA基准上保持竞争力（SRCC 0.770, PLCC 0.781）。消融实验证实，DiffToken、CTAlign和RankReg三个模块各自对细粒度性能有显著贡献，其中移除DiffToken影响最大（Pair下降0.087，Series下降0.177）。

该方法在**方法谱系**上属于“排序驱动的判别性美学学习”，区别于传统的绝对分数回归（如NIMA）或多任务学习范式（如TANet），其核心创新在于将细粒度相对排序信号与粗粒度绝对评分信号进行联合建模，实现了两类评估的平衡。

### 图像美学评估的粗粒度现状

图像美学评估（Image Aesthetic Assessment, IAA）旨在自动预测图像的美学质量分数或偏好排序。近年来，深度学习的进展推动了一系列IAA模型的发展，包括 **NIMA**（Tal et al., TIP 2018）、**MLSP**（Hou et al., CVPR 2019）、**MUSIQ**（Ke et al., ICCV 2021）、**TANet**（Jin et al., IJCAI 2022）、**VILA**（Zhong et al., CVPR 2023）、**Charm**（Xu et al., CVPR 2025）、**Q-Align**（Wu et al., ICML 2024）、**UNIAA**（Yang et al., arXiv 2024）和 **RealQA**（He et al., arXiv 2025）等。这些方法在AVA等粗粒度数据集上取得了显著进展，其核心范式是对视觉差异明显的独立图像进行绝对分数回归。

### 细粒度美学评估的核心瓶颈

然而，现有IAA模型在细粒度场景下暴露出根本性缺陷。当面对视觉高度相似、仅有微妙美学差异的图像序列时（如连拍照片、AIGC变体、不同裁剪方案），这些模型难以提取判别性美学特征。**核心瓶颈在于**：强烈的语义相似性掩盖了微小的美学差异，导致模型无法有效区分“哪张更好”。传统的绝对分数回归范式将每张图像独立对待，缺乏对图像间相对美学关系的显式建模，因此在细粒度区分任务上性能急剧下降。

### 从相对排序中学习判别性分数的动机

针对上述缺口，本文的核心洞察是：**通过从图像序列的相对排序中学习判别性美学分数，可以同时保持粗粒度评估能力，并显著提升细粒度美学区分能力。** 这一动机源于一个关键观察——在细粒度场景中，人类标注者更容易给出“A比B好”的相对判断，而非为每张图像分配绝对分数。相对排序天然地揭示了图像间的美学差异信号，为模型提供了更具判别性的监督信息。

基于此，本文提出 **FGAesQ**，一个从相对排序中学习判别性美学分数的新框架。FGAesQ通过三个协同模块实现这一目标：**差分保持Token化（DiffToken）** 在美学决定性区域保持原始分辨率细节，其他区域降采样以节省计算量；**对比文本辅助对齐（CTAlign）** 将视觉嵌入差与MLLM生成的对比文本嵌入对齐，增强判别性表征；**排序感知回归（RankReg）** 使用Bradley-Terry模型和ListMLE损失，将预测的成对偏好概率与真实排序对齐。同时，本文构建了 **FGAesthetics** 基准数据集，包含来自自然、AIGC和裁剪三个来源的32,217张图像、10,028个序列，为细粒度IAA研究提供了标准化评估平台。

## 核心方法与创新机理

FGAesQ 的核心创新在于将**细粒度相对排序**作为训练信号，通过三个协同设计的模块——差分保持Token化（DiffToken）、对比文本辅助对齐（CTAlign）和排序感知回归（RankReg）——使模型学习更具判别性的美学表征，从而在保持粗粒度评估能力的同时，显著提升对语义相似、美学差异微小的图像的区分能力。

### 问题瓶颈与因果机制

现有 IAA 模型（如 **NIMA** (Tal et al., TIP 2018)、**MUSIQ** (Ke et al., ICCV 2021)、**VILA** (Zhong et al., CVPR 2023)、**Charm** (Xu et al., CVPR 2025) 等）主要针对粗粒度评估设计。当面对细粒度场景——即图像间存在强烈的语义相似性（CLIPScore > 0.91，见 Figure 3）而仅有微小的美学差异时，这些模型难以提取判别性美学特征，导致性能显著下降。

FGAesQ 的因果调节变量是将细粒度相对排序作为训练信号，通过以下机制实现判别性美学表征的学习：
- **DiffToken** 在美学决定性区域保持原始分辨率细节，在相似区域降采样以节省计算量；
- **CTAlign** 将视觉嵌入差与 MLLM 生成的对比文本嵌入对齐，增强判别性；
- **RankReg** 利用 Bradley-Terry 模型和 ListMLE 损失，将预测的成对偏好概率与真实排序对齐，校准评分。

### 关键变更槽位

| 变更槽位 | 基线方案 | FGAesQ 方案 | 证据锚点 |
|---------|---------|------------|---------|
| **Token化** | 标准 ViT 固定分辨率块 Token 化 | 差分保持 Token 化（DiffToken）：在美学决定性区域保持原始分辨率细节，其他区域降采样 | Section 4.1, Equations (1)-(2) |
| **视觉-文本对齐** | 无显式对比文本对齐（或仅用标准 CLIP 对齐） | 对比文本辅助对齐（CTAlign）：将视觉嵌入差与 MLLM 生成的对比文本嵌入对齐 | Section 4.2, Equation (3) |
| **细粒度损失函数** | 标准的 EMD 损失或绝对分数回归 | 排序感知回归（RankReg）：Bradley-Terry 成对偏好概率 + ListMLE 排序损失 | Section 4.3, Equations (4)-(5) |
| **训练策略** | 单阶段粗粒度训练或仅细粒度微调 | 两阶段训练：先粗粒度预训练，再粗/细粒度交替联合训练 | Section 4.4, Equation (6) |

### 模块协同机制

**DiffToken** 首先定位美学决定性区域。给定目标图像 $x$ 和参考图像 $y_1$，计算小块相似度 $s_{i,j} = \mathrm{SSIM}(P_{i,j}^x, P_{i,j}^{y_1})$，选取相似度低于百分位数阈值 $p$ 的区块作为决定性区域集合 $D = \{ (i,j) \mid s_{i,j} < \tau, \tau = \mathrm{percentile}(s, p) \}$。这些区域保持原始分辨率 Token 化，其余区域降采样，从而在保留判别性细节的同时控制计算开销。

**CTAlign** 进一步强化判别性。利用 MLLM 为图像对生成对比文本描述 $T_1$，通过 CLIP 文本编码器提取嵌入 $E_t(T_1)$，并与视觉嵌入差 $E_v(x) - E_v(y_1)$ 对齐，损失函数为 $\mathcal{L}_{F.align} = \cos(E_v(x) - E_v(y_1), E_t(T_1))$。

**RankReg** 将排序信息注入评分校准。使用 Bradley-Terry 模型计算成对偏好概率 $P_{(x \succ y_1)} = \frac{e^{Score_x}}{e^{Score_x} + e^{Score_{y_1}}}$，并通过 ListMLE 损失对齐预测排序与真实排序：
$$\mathcal{L}_{F.RR}(\mathbf{P}', \mathbf{P}) = -\sum_{j=1}^{n} \log \frac{e^{\mathbf{P}'(r_i)}}{\sum_{j=i}^{n} e^{\mathbf{P}'(r_j)}}$$

最终，两阶段训练以交替方式优化总损失：
$$\mathcal{L} = \underbrace{\delta \cdot (\lambda \mathcal{L}_{F.align} + \mathcal{L}_{F.RR})}_{\mathrm{Fine-grained}} + \underbrace{(1-\delta) \cdot \mathcal{L}_{C.EMD}}_{\mathrm{Coarse-grained}}$$
其中 $\delta$ 为二进制指示符，$\lambda$ 为平衡系数（设为 10）。

### 消融验证

消融实验（Table 5）严格验证了各模块的贡献：
- **移除 DiffToken**：细粒度 Pair 从 0.753 降至 0.666（-0.087），Series 从 0.600 降至 0.423（-0.177），影响最大，证明差分保持 Token 化对细粒度判别至关重要；
- **移除 CTAlign**：Pair 降至 0.747，Series 降至 0.581，验证了对比文本对齐对判别性表征的增强作用；
- **移除 RankReg**：Pair 降至 0.742，Series 降至 0.571，表明排序感知回归有效校准了评分分布。

此外，DiffToken 配置消融（Figure 10）显示最佳配置为 32×32 块大小、$p=0.5$ 的百分位阈值，性能呈倒 U 型，且粗粒度性能在不同配置下保持稳定，表明该模块在细粒度判别与粗粒度鲁棒性之间取得了良好平衡。

### 与基线方法的本质差异

与现有方法相比，FGAesQ 的根本区别在于**学习范式的转变**：从学习绝对美学分数转向从相对排序中学习判别性分数。这一转变使得模型不再依赖单一的绝对评分监督，而是利用图像序列中蕴含的丰富相对信息，从而在细粒度场景中获得更强的区分能力。实验结果表明，FGAesQ 在 FGAesthetics 的所有评估协议（成对级别和序列级别，三个图像源）上均取得最优性能（Table 2），同时在 AVA 粗粒度评估上保持竞争力（SRCC=0.770/PLCC=0.781，Table 3），实现了粗-细粒度评估的最佳平衡。

FGAesQ 的整体设计围绕一个核心矛盾展开：细粒度美学评估中，图像间强烈的语义相似性与微小的美学差异使得标准模型难以提取判别性特征。为解决这一问题，FGAesQ 将相对排序信号作为训练的核心驱动力，构建了一个三模块协同的评估框架，如 Figure 4 所示。

![[assets/figures/papers/paper_list_l2124_https_arxiv_org_abs_2603_03907/figures/005_Figure_4.jpg]]
*Figure 4: Overall pipeline of the proposed FGAesQ. FGAesQ learns discriminative aesthetic scores from relative ranks through three modules: (a) Difference-preserved Tokenization (DiffToken) selectively maintains difference regions at their original resolution while downscaling others. (b) Comparative Text-assisted Alignment (CTAlign) achieves distinctive aesthetic visual representations. (c) Rankaware Regression (RankReg) rectifies the coarse-grained score regression with fine-grained aesthetic rankings*

### 框架总览

FGAesQ 以 Vision Transformer 为骨干网络，采用两阶段训练策略。第一阶段在粗粒度数据（AVA）上使用 EMD 损失进行预训练，建立基础的美学感知能力；第二阶段在粗粒度与细粒度数据上交替联合训练，使模型在保持粗粒度评估精度的同时，获得细粒度的美学判别能力。交替训练的总损失函数为：

$$\mathcal{L} = \underbrace{\delta \cdot (\lambda \mathcal{L}_{F.align} + \mathcal{L}_{F.RR})}_{\mathrm{Fine-grained}} + \underbrace{(1-\delta) \cdot \mathcal{L}_{C.EMD}}_{\mathrm{Coarse-grained}}$$

其中 $\delta$ 为二进制指示符，控制细粒度与粗粒度批次的交替切换；$\lambda$ 为平衡系数，在联合训练中设为 10。细粒度批次大小约为 64（因序列长度略有波动），粗粒度批次大小为 128。

### 三模块协同机制

框架的三个核心模块分别从**特征保持**、**语义对齐**和**排序校准**三个层面增强模型的细粒度判别能力：

1. **差分保持Token化（DiffToken）**：在输入端解决“相似图像中美学差异区域被均匀化”的问题。该模块首先通过计算目标图像与参考图像在小块级别的 SSIM 相似度 $s_{i,j} = \mathrm{SSIM}(P_{i,j}^x, P_{i,j}^{y_1})$，定位美学决定性区域 $D = \{ (i,j) \mid s_{i,j} < \tau, \tau = \mathrm{percentile}(s, p) \}$。随后执行混合分辨率 Token 化——对决定性区域保持原始分辨率以保留细节差异，对其他区域进行降采样以节省计算量。消融实验证实，移除 DiffToken 会导致细粒度 Pair 指标从 0.753 降至 0.666，Series 指标从 0.600 降至 0.423，是三个模块中影响最大的组件。

2. **对比文本辅助对齐（CTAlign）**：在特征空间解决“视觉嵌入缺乏判别性语义锚定”的问题。该模块利用多模态大语言模型（MLLM）为图像对生成对比文本描述（如“左侧图像的光线更柔和”），通过 CLIP 文本编码器提取文本嵌入，并与两幅图像的视觉嵌入差进行余弦相似度对齐：

   $$\mathcal{L}_{F.align} = \cos(E_v(x) - E_v(y_1), E_t(T_1))$$

   这一机制将抽象的视觉差异映射到可解释的语义空间，强化了模型对细微美学差异的感知。

3. **排序感知回归（RankReg）**：在输出端解决“绝对分数回归无法捕捉相对美学关系”的问题。该模块采用 Bradley-Terry 模型计算成对偏好概率：

   $$P_{(x \succ y_1)} = \frac{e^{Score_x}}{e^{Score_x} + e^{Score_{y_1}}}$$

   并通过 ListMLE 损失将预测的概率分布与真实排序对齐：

   $$\mathcal{L}_{F.RR}(\mathbf{P}', \mathbf{P}) = -\sum_{j=1}^{n} \log \frac{e^{\mathbf{P}'(r_i)}}{\sum_{j=i}^{n} e^{\mathbf{P}'(r_j)}}$$

   这使得模型的预测分数不仅反映绝对美学质量，更能准确刻画图像序列内的相对优劣关系。

### 输入输出流

FGAesQ 的推理流程为：输入图像经 DiffToken 进行混合分辨率 Token 化后，送入 ViT 编码器提取视觉嵌入；视觉嵌入直接通过回归头输出美学分数。CTAlign 和 RankReg 仅在训练阶段发挥作用——CTAlign 通过对比文本对齐引导视觉编码器学习判别性表征，RankReg 通过排序损失校准回归头的评分分布。这种设计确保了推理时无需额外的文本输入或成对比较，保持了与标准 IAA 模型相同的推理效率。

消融实验（Table 5）系统验证了各模块的独立贡献：移除 CTAlign 使 Pair 从 0.753 降至 0.747、Series 从 0.600 降至 0.581；移除 RankReg 使 Pair 降至 0.742、Series 降至 0.571。三个模块的叠加效果表明，特征保持、语义对齐和排序校准在细粒度美学建模中存在互补增益。

FGAesQ 的核心设计围绕一个瓶颈展开：现有 IAA 模型在细粒度场景下，由于图像间强烈的语义相似性和微小的美学差异，难以提取判别性美学特征。为解决这一问题，FGAesQ 引入三个协同模块——差分保持Token化（DiffToken）、对比文本辅助对齐（CTAlign）和排序感知回归（RankReg），并通过两阶段训练策略将粗粒度美学感知与细粒度排序信号联合优化。

### 差分保持Token化（DiffToken）

标准 ViT 采用固定分辨率的块Token化，对整幅图像均匀采样，无法区分美学决定性区域与相似区域。DiffToken 的核心思路是：在美学差异显著的区域保持原始分辨率细节，在相似区域降采样以节省计算量。

具体而言，给定目标图像 $x$ 和参考图像 $y_1$，首先将两幅图像划分为不重叠的小块，计算每个位置 $(i,j)$ 的小块结构相似度：

$$s_{i,j} = \mathrm{SSIM}(P_{i,j}^x, P_{i,j}^{y_1})$$

其中 $P_{i,j}^x$ 和 $P_{i,j}^{y_1}$ 分别表示两幅图像在位置 $(i,j)$ 的小块。$s_{i,j}$ 越低，表明该区域的美学差异越大。

随后，选取相似度低于百分位数阈值 $p$ 的区块作为美学决定性区域集合 $D$：

$$D = \{ (i,j) \mid s_{i,j} < \tau, \tau = \mathrm{percentile}(s, p) \}$$

对于 $D$ 中的区域，DiffToken 保持原始分辨率进行Token化；对于其他区域，则进行降采样处理。这种混合分辨率Token化策略使得模型能够聚焦于真正决定美学差异的局部细节，同时避免在相似区域浪费计算资源。消融实验表明，DiffToken 的最佳配置为 32×32 的块大小和 $p=0.5$ 的百分位阈值，性能呈倒 U 型（Figure 10）。

### 对比文本辅助对齐（CTAlign）

仅靠视觉特征差异不足以充分捕捉细粒度美学判别信息。CTAlign 利用 MLLM 为图像对生成对比文本描述（例如“图像 A 的构图更平衡，但图像 B 的色彩更丰富”），并将其文本嵌入与视觉嵌入差对齐，从而增强视觉表征的判别性。

具体而言，令 $E_v(x)$ 和 $E_v(y_1)$ 分别为目标图像和参考图像的视觉嵌入，$E_t(T_1)$ 为 MLLM 生成的对比文本 $T_1$ 的文本嵌入。CTAlign 通过最小化以下余弦相似度损失来实现对齐：

$$\mathcal{L}_{F.align} = \cos(E_v(x) - E_v(y_1), E_t(T_1))$$

该损失鼓励视觉嵌入差的方向与对比文本嵌入的方向一致，使模型学会关注文本描述中强调的美学差异维度。消融实验（Table 5）显示，移除 CTAlign 后，Pair 指标从 0.753 降至 0.747，Series 指标从 0.600 降至 0.581，验证了文本辅助对齐对细粒度判别的贡献。

### 排序感知回归（RankReg）

传统 IAA 方法使用 EMD 损失或绝对分数回归，无法有效利用序列中的相对排序信息。RankReg 将细粒度美学评估建模为排序问题，使用 Bradley-Terry 模型计算成对偏好概率，并通过 ListMLE 损失对齐预测排序与真实排序。

对于目标图像 $x$ 和参考图像 $y_1$，Bradley-Terry 模型定义 $x$ 美学更优的概率为：

$$P_{(x \succ y_1)} = \frac{e^{Score_x}}{e^{Score_x} + e^{Score_{y_1}}}$$

其中 $Score_x$ 和 $Score_{y_1}$ 分别为模型预测的美学分数。对于长度为 $n$ 的完整序列，ListMLE 排序损失将预测的概率分布 $\mathbf{P}'$ 与真实排序 $\mathbf{P}$ 对齐：

$$\mathcal{L}_{F.RR}(\mathbf{P}', \mathbf{P}) = -\sum_{j=1}^{n} \log \frac{e^{\mathbf{P}'(r_i)}}{\sum_{j=i}^{n} e^{\mathbf{P}'(r_j)}}$$

该损失函数逐位置计算 top-1 概率的负对数似然，鼓励模型对整个序列的排序与真实排序一致。消融实验（Table 5）表明，移除 RankReg 后 Pair 指标降至 0.742，Series 指标降至 0.571，证明排序感知回归对序列级别美学排序至关重要。

### 两阶段联合训练

FGAesQ 采用两阶段训练策略：首先在粗粒度数据（AVA）上使用 EMD 损失预训练，建立基础美学感知；然后在粗/细粒度数据上交替联合训练。交替训练的总损失为：

$$\mathcal{L} = \underbrace{\delta \cdot (\lambda \mathcal{L}_{F.align} + \mathcal{L}_{F.RR})}_{\mathrm{Fine-grained}} + \underbrace{(1-\delta) \cdot \mathcal{L}_{C.EMD}}_{\mathrm{Coarse-grained}}$$

其中 $\delta$ 为二进制指示符（细粒度批次为 1，粗粒度批次为 0），$\lambda$ 为平衡系数（设为 10）。细粒度批次大小约为 64，粗粒度批次大小约为 128。这种交替训练策略使得细粒度排序信号能够校准粗粒度评分，同时保持粗粒度评估能力不退化。

**消融关键发现**：移除 DiffToken 对性能影响最大，Pair 从 0.753 降至 0.666，Series 从 0.600 降至 0.423（Table 5），表明保持美学差异区域的细节是细粒度判别的核心瓶颈所在。

## 实验与关键发现

### 实验设置

**数据集与评估协议。** 实验在两个核心基准上进行：细粒度基准 **FGAesthetics** 和粗粒度基准 **AVA**。FGAesthetics 包含来自 Natural、AIGC、Cropping 三个图像源的 32,217 张图像，组织为 10,028 个序列。评估采用两种协议：（1）**成对级别**，衡量模型在图像对中判断美学优劣的准确率（Acc）和 F1 分数，最终以 (Acc+F1)/2 报告；（2）**序列级别**，衡量模型对整个序列排序的质量，以序列准确率（s-Acc）和序列 SRCC（s-SRCC）的平均值报告。粗粒度评估在 AVA 数据集上使用 SRCC 和 PLCC。所有方法在相同的数据划分（8:1:1 训练-验证-测试）下评估，确保类别平衡。

**训练配置。** FGAesQ 采用两阶段训练策略：先在 AVA 上用 EMD 损失进行粗粒度预训练，再在粗/细粒度数据上交替联合训练。联合训练中，细粒度批次大小约 64，粗粒度批次大小约 128，学习率 2e-5，权重衰减 5e-5，平衡系数 λ 设为 10。

### 主实验结果

**FGAesQ 在细粒度评估上全面领先。** 在 FGAesthetics 的所有评估协议上，FGAesQ（配备 DiffToken）均取得最优性能（Table 2）。成对级别平均 (Acc+F1)/2 达到 0.753，相较于最强基线 **Charm**（Xu et al., CVPR 2025）微调后的 0.699 提升 5.4 个百分点；序列级别平均 (s-Acc+s-SRCC)/2 达到 0.600，相较于 Charm 的 0.477 提升 12.3 个百分点。这一差距在三个图像源上一致存在，表明从相对排序中学习判别性分数的策略在细粒度场景下具有显著优势。

**粗-细粒度平衡能力突出。** Table 3 展示了各方法在粗粒度（AVA）和细粒度（FGAesthetics）之间的性能平衡。FGAesQ 在 AVA 上取得 SRCC=0.770 / PLCC=0.781，与专门针对粗粒度设计的 **Charm**（SRCC=0.777 / PLCC=0.779）持平，同时细粒度性能大幅领先。相比之下，其他方法如 **VILA**（Zhong et al., CVPR 2023）和 **UNIAA**（Yang et al., arXiv 2024）在细粒度上表现较弱，而 **Q-Align**（Wu et al., ICML 2024）虽在 AVA 上达到 SRCC=0.785，但细粒度 Pair 仅 0.618。FGAesQ 是唯一在两个粒度级别上均保持顶级性能的方法，验证了其“从相对排序中学习判别性分数”的核心设计——粗粒度预训练建立基础美学感知，细粒度排序回归在此基础上校准评分，二者并非此消彼长的权衡关系。

**跨数据集泛化验证。** 在 ICAA17K、AADB、TAD66K 三个额外的 IAA 基准上（Table 4），FGAesQ 同样展现出竞争力的泛化能力，进一步支持了其学习到的美学表征的鲁棒性。

### 消融实验

**模块贡献分析。** Table 5 的消融实验揭示了三个核心模块各自的贡献。移除 DiffToken 导致成对性能从 0.753 骤降至 0.666（-0.087），序列性能从 0.600 降至 0.423（-0.177），降幅最大，表明差分保持 Token 化是细粒度判别的基础——若在 Token 化阶段丢失了美学差异区域的细节信息，后续对齐和排序模块将失去可依赖的视觉表征。移除 CTAlign（对比文本辅助对齐）使成对性能降至 0.747，序列性能降至 0.581，验证了 MLLM 生成的对比文本描述对增强视觉嵌入判别性的作用。移除 RankReg（排序感知回归）使成对性能降至 0.742，序列性能降至 0.571，说明基于 Bradley-Terry 模型的排序损失对校准预测分数与真实排序至关重要。三者联合移除（仅保留粗粒度 EMD 损失）时，细粒度性能大幅退化，证实了每个模块对细粒度美学建模的不可替代性。

**训练策略消融。** 仅进行细粒度训练（无粗粒度预训练）导致粗粒度 SRCC 从 0.770 降至 0.714，同时细粒度性能也下降，说明粗粒度预训练提供的基础美学感知对后续细粒度学习有正向迁移作用。仅进行粗粒度训练则细粒度性能极低，无法处理细粒度任务。

**骨干网络选择。** Table 7 显示，采用 ViT-B/16 作为骨干网络显著优于 ViT-B/32：细粒度 Pair 从 0.701 升至 0.753，粗粒度 SRCC 从 0.747 升至 0.770。更小的 patch size（16×16 vs. 32×32）保留了更多空间细节，与 DiffToken 的差分保持策略形成协同效应。

**DiffToken 配置敏感性。** Figure 10 展示了 DiffToken 在不同 patch 大小和百分位阈值 p 下的性能变化。细粒度性能呈倒 U 型：patch 大小 32×32、p=0.5 时达到最优，过小的 patch（如 8×8）可能引入噪声，过大的 patch（如 64×64）则丢失细节；p 值过高或过低分别导致差异区域过少或过多，均损害判别能力。值得注意的是，粗粒度性能在不同配置下保持稳定，表明 DiffToken 主要影响细粒度判别，不影响基础美学感知。

**分布外泛化。** Table 8 的 OOD 实验表明，当排除某个图像源类别（如 Natural）进行训练时，对应该源的测试性能下降最明显（Natural 成对性能从 0.753 降至 0.691），而其他源和粗粒度性能保持相对稳定。这说明三个图像源（Natural、AIGC、Cropping）具有独特的分布特性，模型需要见到各源数据才能实现最佳泛化，但跨源迁移仍有一定效果。

### 失败模式与局限性

尽管 FGAesQ 在细粒度 IAA 上取得了显著进展，仍存在以下局限：

1. **标注成本瓶颈。** 细粒度美学比较依赖大规模人工标注（成对比较和序列排序），成本高昂且存在主观偏差。当前 FGAesthetics 的构建需要多阶段人工筛选和校准，限制了数据集向更多领域和更大规模的扩展。

2. **可解释性不足。** 模型虽能准确判断图像间的美学优劣，但缺乏对判断依据的显式解释。CTAlign 模块利用 MLLM 生成了对比文本描述（Figure 9 词云展示了常见判别依据，如构图、色彩、清晰度等），但这些文本仅在训练中作为对齐信号，未在推理时输出。用户无法获知“为什么这张图更好”或“如何改进”，限制了实际应用深度。

3. **OOD 场景下的性能退化。** Table 8 显示，当训练数据中缺失某个图像源时，该源上的性能下降明显，表明模型对训练分布有较强依赖，在完全未知的美学风格或图像类型上可能需要额外的领域适应。

![[assets/figures/papers/paper_list_l2124_https_arxiv_org_abs_2603_03907/figures/017_Table_8.jpg]]
*Table 8: Out-of-Distribution generalization performance. OOD generalization is evaluated by training FGAesQ with one source category excluded and testing on fine-grained (all three categories) and coarse-grained (AVA [26]) benchmarks*

![[assets/figures/papers/paper_list_l2124_https_arxiv_org_abs_2603_03907/figures/006_Table_2.jpg]]
*Table 2: Performance comparison between the proposed FGAesQ and state-of-the-art IAA methods on FGAesthetics. Results are reported across all three image sources (Natural, AIGC, and Cropping) for both pair-level and series-level evaluations. Model parameter counts are also provided. The top two results are highlighted in bold and underlined, respectively*

![[assets/figures/papers/paper_list_l2124_https_arxiv_org_abs_2603_03907/figures/010_Table_5.jpg]]
*Table 5: Ablation study on training strategies and model components. ‘w/o’ is removal of the specified training or component. Metrics are (Acc, F1)/2 for Pair and (s-Acc, s-SRCC)/2 for Series*

![[assets/figures/papers/paper_list_l2124_https_arxiv_org_abs_2603_03907/figures/018_Figure_10.jpg]]
*Figure 10: Ablation study on DiffToken configuration. Performance is evaluated across different difference localization patch sizes and percentile thresholds for identifying aesthetics-decisive regions. Fine-grained metrics show pair- and series-averaged performance across Natural, AIGC, and Cropping categories. Coarsegrained metrics report SRCC and PLCC on AVA [26]*

![[assets/figures/papers/paper_list_l2124_https_arxiv_org_abs_2603_03907/figures/008_Figure_5.jpg]]
*Figure 5: Visualization of evaluation results on three test series. Images arranged left-to-right in decreasing aesthetic quality. Red boxes and text indicate the best aesthetics*

## 定位与知识库关联

### 问题定位：从粗粒度到细粒度IAA的范式迁移

传统图像美学评估（IAA）模型设计围绕粗粒度场景展开：输入图像在内容、风格、构图等方面存在显著差异，模型只需学习全局美学偏好分布即可取得较好性能。代表性工作如 **NIMA**（Tal et al., TIP 2018）采用EMD损失将评分预测转化为分布匹配问题，**MLSP**（Hou et al., CVPR 2019）引入多层级语义感知，**MUSIQ**（Ke et al., ICCV 2021）探索多尺度输入，**TANet**（Jin et al., IJCAI 2022）构建主题感知网络，**VILA**（Zhong et al., CVPR 2023）利用视觉-语言预训练，**Charm**（Xu et al., CVPR 2025）引入多模态美学表征，**Q-Align**（Wu et al., ICML 2024）和 **UNIAA**（Yang et al., arXiv 2024）分别从评分量化和统一架构角度推进。然而，这些方法的核心瓶颈在于：当面对视觉高度相似、仅存在微妙美学差异的图像序列时，模型缺乏提取判别性美学特征的能力，导致细粒度区分性能急剧下降。

FGAesQ 正是在这一瓶颈上做出关键设计选择：将细粒度相对排序作为训练信号，而非仅依赖绝对评分回归。这一选择使得模型从“学习绝对美学量值”转向“学习美学差异的判别性表征”，在保持粗粒度评估能力的同时显著提升细粒度区分能力。

### 方法谱系中的技术增量

相较于现有IAA方法，FGAesQ 在四个关键维度上引入了可验证的技术增量：

**Token化策略**：现有方法普遍采用标准ViT的固定分辨率块Token化（如16×16均匀划分），在细粒度场景下，大量Token被分配给美学差异微小的同质区域，造成计算冗余和判别信号稀释。FGAesQ 提出的差分保持Token化（DiffToken）通过SSIM相似度定位美学决定性区域，仅对这些区域保持原始分辨率细节，其他区域降采样处理。这一设计直接响应了细粒度场景的核心矛盾——判别信号稀疏且局部化。

**视觉-文本对齐**：现有方法要么无显式对比文本对齐，要么仅用标准CLIP对齐全局图文语义。FGAesQ 的对比文本辅助对齐（CTAlign）创新性地将视觉嵌入差与MLLM生成的对比文本嵌入对齐，使模型学习到的美学表征直接对应可语义化的美学差异描述，增强了判别性的可解释维度。

**损失函数设计**：现有方法主要依赖EMD损失或绝对分数回归，缺乏对排序结构的显式建模。FGAesQ 的排序感知回归（RankReg）引入Bradley-Terry模型计算成对偏好概率，结合ListMLE损失对齐预测排序与真实排序，将细粒度评估形式化为排序学习问题。

**训练策略**：现有方法通常采用单阶段粗粒度训练或仅细粒度微调，容易在两种评估粒度间失衡。FGAesQ 的两阶段交替联合训练——先在AVA上用EMD损失预训练建立基础美学感知，再在粗/细粒度数据上交替优化——为平衡两种评估能力提供了有效的训练范式。

### 适用边界与局限

FGAesQ 的设计隐含若干适用边界，需在实际应用中审慎考量：

**数据依赖与标注成本**：方法的核心训练信号来自细粒度相对排序标注，这依赖大规模人工成对比较。FGAesthetics数据集的构建涉及Metric-MLLMs-Human三级过滤和成对标注流程，成本高昂且存在主观偏差。当目标领域缺乏类似细粒度排序标注时，方法的迁移效果可能受限。消融实验中OOD设置（Table 8）表明，排除某个图像源类别训练时对应该源的测试性能下降最明显，证实各源数据具有独特性，跨源泛化存在挑战。

**可解释性不足**：尽管CTAlign模块将视觉差异与文本描述对齐，模型仍无法提供具体的美学改进建议（如指出构图缺陷或建议针对性调整）。Figure 9的词云可视化展示了MLLM生成的高频对比描述词，但这些描述停留于差异识别层面，尚未转化为可操作的反馈。这一局限限制了模型在实际美学辅助工具中的应用深度。

**骨干网络的敏感性**：Table 7的消融显示，采用ViT-B/16作为backbone优于ViT-B/32，细粒度Pair从0.701升至0.753，粗粒度SRCC从0.747升至0.770。这表明DiffToken的混合分辨率Token化策略对骨干网络的分辨率敏感，较小patch size能更好地保留美学决定性区域的细节信息，但同时也增加了计算开销。

### 开放问题与后续方向

从FGAesQ的设计逻辑和实验发现出发，可识别以下值得关注的开放方向：

**自动化标注策略**：当前细粒度排序标注高度依赖人工，限制了数据集的扩展性和领域覆盖。如何开发自动化或半自动化标注策略——例如利用MLLM的审美判断能力辅助或替代部分人工标注——在保持标注质量的同时降低人力成本，是推动细粒度IAA规模化应用的关键问题。

**可操作反馈生成**：从“判断哪个更好”到“解释为什么更好并提供改进建议”的跨越，需要模型具备更细粒度的美学属性解耦能力。CTAlign的对齐机制为此提供了潜在基础，但需要进一步将对比文本嵌入映射到具体的视觉属性（构图、色彩、光影等），并建立属性到改进操作的因果链。

**跨源泛化与域适应**：Table 8的OOD实验结果揭示了不同图像源（Natural、AIGC、Cropping）之间的域差异。AIGC图像的审美标准可能与自然图像存在系统性偏差，Cropping变体的美学判断涉及构图规则的特定知识。如何设计具备跨源泛化能力的细粒度IAA模型，或建立高效的域适应机制，值得进一步探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Fine_grained_Image_Aesthetic_Assessment_Learning_Discriminative_Scores_from_Relative_Ranks.pdf]]

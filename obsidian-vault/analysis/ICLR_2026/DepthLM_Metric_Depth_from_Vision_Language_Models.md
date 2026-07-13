---
title: "DepthLM: Metric Depth from Vision Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DepthLM_Metric_Depth_from_Vision_Language_Models.pdf
project_link: null
code_link: https://github.com/facebookresearch/DepthLM_Official
openreview_forum_id: ObFVZGnSFN
aliases:
- DepthLM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "采用视觉提示（在图像上绘制标记）替代文本坐标，并通过内参条件图像增强统一焦距，从而精确控制像素引用和消除相机模糊。"
primary_logic: "仅需每张训练图像一个稀疏标注像素的文本监督微调（SFT），结合视觉提示和焦距统一增强，无需任务特定架构或复杂回归损失，VLMs即可实现与纯视觉模型相当的度量深度估计精度。"
claims:
- "视觉标记引用像素位置远优于文本坐标引用，室内场景精度差距达0.15 δ1。"
- "统一图像焦距的内参条件增强有效解决相机模糊，使VLMs精度翻倍。"
- "每张图像仅需1个标注像素即可训练出强大深度估计模型，图像多样性比标签密度更重要。"
- "SFT在训练效率和可扩展性上优于强化学习（GRPO），同时保持相当精度。"
---

# DepthLM: Metric Depth from Vision Language Models

> [!tip] 核心洞察
> 仅需每张训练图像一个稀疏标注像素的文本监督微调（SFT），结合视觉提示和焦距统一增强，无需任务特定架构或复杂回归损失，VLMs即可实现与纯视觉模型相当的度量深度估计精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DepthLM：从视觉语言模型生成度量深度 |
| 英文题名 | DepthLM: Metric Depth from Vision Language Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ObFVZGnSFN) · [GitHub](https://github.com/facebookresearch/DepthLM_Official) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | DepthLM |
| Dataset | DepthLMBench (平均8个数据集), sunRGBD, NuScenes |

> [!tip] 效果简介
> - DepthLMBench (平均8个数据集) 上，δ1 (↑) 为 0.838 (DepthLM 7B)，对比 0.370 (GPT-5)，变化 +0.468。
> - sunRGBD 上，δ1 (↑) 为 0.859 (DepthLM 7B)，对比 0.835 (DepthPro)，变化 +0.024。
> - NuScenes 上，δ1 (↑) 为 0.865 (DepthLM 7B)，对比 0.280 (GPT-5)，变化 +0.585。

## 概要

**核心问题**：视觉语言模型（VLMs）在逐像素度量深度估计中面临两大瓶颈——精确的像素位置引用困难，以及跨数据集相机内参（焦距）差异导致的尺度模糊。现有通用VLM（如 **GPT-5**，Singh et al., 2025）在该任务上的 δ1 精度普遍低于 0.4，远落后于纯视觉模型。

**核心方法**：DepthLM 提出两项关键创新来解决上述瓶颈：
1. **视觉提示**：在输入图像上直接渲染小型箭头标记来引用查询像素，替代在文本中提供坐标的传统方式。
2. **内参条件增强**：根据相机内参缩放图像，将所有训练图像的焦距统一为 1000 像素，消除相机歧义。

在此基础上，仅需对预训练VLM进行标准的文本监督微调（SFT），无需任务特定架构或复杂的回归损失函数。

**关键发现**：
- 视觉标记引用像素位置远优于文本坐标引用，室内场景 δ1 精度差距可达 0.15（Finding 1）。
- 统一焦距的内参增强使VLMs精度翻倍，有效解决相机模糊问题（Finding 3）。
- 每张训练图像仅需 **1个标注像素** 即可训练出强深度估计模型，图像多样性比标签密度更重要（Finding 4）。
- SFT在训练效率和可扩展性上优于强化学习（GRPO），同时保持相当精度（Finding 2）。

**方法定位**：DepthLM 属于将通用VLM适配为逐像素度量深度估计器的方法，其核心策略是通过输入层面的图像增强和视觉提示来弥补VLM在精确空间定位和相机感知上的不足，而非修改模型架构。与纯视觉深度模型（如 **DepthPro**，Bochkovskii et al., 2024；**Metric3Dv2**，Hu et al., 2024）相比，DepthLM 首次使VLM在度量深度估计上达到可比精度；与空间推理VLM（如 **SpatialRGPT**，Cheng et al., 2024）相比，DepthLM 在稀疏标注条件下实现了更强的泛化能力。

**主要结果**：
- 在 DepthLMBench（8个数据集平均）上，DepthLM 7B 的 δ1 达到 **0.838**，较 GPT-5（0.370）提升超过 2 倍（Table 1）。
- 在 sunRGBD 数据集上，DepthLM 7B（δ1=0.859）略优于纯视觉模型 DepthPro（δ1=0.835），首次实现VLM与纯视觉模型的可比精度（Table 2）。
- 在 NuScenes 自动驾驶数据集上，DepthLM 7B（δ1=0.865）较 GPT-5（δ1=0.280）提升 0.585，展现强泛化能力（Table 1）。



### 视觉语言模型在3D感知中的困境

视觉语言模型（VLMs）在图像描述、视觉问答等高层语义任务上取得了显著进展，然而最新一代通用VLM在从二维图像理解三维度量空间方面仍表现薄弱。以**GPT-5**（Singh et al., 2025）为代表的顶尖VLM，在度量深度估计基准上的平均δ1精度不足0.4，远低于纯视觉深度估计模型。这一鸿沟揭示了VLM在逐像素3D感知中的两个核心瓶颈。

### 瓶颈一：像素位置引用的精度缺失

VLM通常通过文本坐标（如“像素(320, 240)处的深度”）来指定查询位置，但模型对数值坐标的空间理解极为有限。实验表明，基于文本坐标的像素引用方式导致VLM的深度估计精度大幅下降，而直接在图像上绘制视觉标记（如小箭头）则显著提升了像素定位的准确性（Figure 2）。这一发现表明，**VLM的3D感知瓶颈并非源于缺乏视觉理解能力，而是缺少与像素空间精确对齐的接口**。

### 瓶颈二：相机内参差异导致的尺度模糊

跨数据集训练时，不同相机焦距的差异引入了严重的尺度歧义。VLM在不改变架构的情况下，难以从图像内容中推断出相机的内参属性。实验显示，直接混合不同焦距来源的数据进行训练，VLM的深度估计精度极低；而通过**内参条件增强（intrinsic-conditioned augmentation）**将图像焦距统一为固定值（如1000像素），可使精度翻倍（Figure 4a）。这证明相机模糊是VLM在度量深度估计中面临的关键障碍，而非模型容量不足。

### 现有方法的缺口

现有纯视觉度量深度模型（如**DepthPro**, Bochkovskii et al., 2024; **Metric3Dv2**, Hu et al., 2024）依赖密集逐像素深度标签、特定回归损失函数和任务专用架构，虽然精度较高，但无法利用VLM的通用推理能力。另一方面，部分工作尝试将VLM微调用于空间推理（如**SpatialRGPT**, Cheng et al., 2024）或度量深度（如**Seed1.5-VL**, Guo et al., 2025），但精度仍远低于纯视觉模型，未能弥合VLM与专用深度估计器之间的差距。

### 本文动机

上述分析引出一个核心问题：**能否在不引入任务特定架构和复杂回归损失的前提下，仅通过通用的文本监督微调（SFT），使VLM达到与纯视觉模型相当的度量深度估计精度？** 这需要同时解决像素引用精度和相机模糊两个瓶颈。本文提出DepthLM，通过视觉提示替代文本坐标、以内参条件增强统一焦距，并利用每张图像仅需一个稀疏标注像素的极端稀疏监督，首次实现了VLM在度量深度估计上与专家纯视觉模型可比的精度。



## 核心方法与创新机理

DepthLM 的核心创新并非提出新的模型架构或损失函数，而是识别并解决了视觉语言模型（VLM）在逐像素度量深度估计中的两个根本性瓶颈：**像素位置引用的不精确性**和**跨数据集相机内参差异导致的尺度模糊**。通过两项关键的技术手段——视觉提示（Visual Prompting）和内参条件增强（Intrinsic-Conditioned Augmentation）——DepthLM 首次使标准 VLM 的文本监督微调（SFT）达到了与专家纯视觉模型相当的度量深度估计精度。

### 瓶颈识别与因果机制

**瓶颈一：像素位置引用**。此前工作（如 Seed1.5-VL, Guo et al., 2025）尝试通过在文本提示中提供像素坐标来让 VLM 理解空间位置，但 DepthLM 的分析表明，VLM 对文本坐标的理解能力极弱。在室内数据集 ScanNet++ 上，文本坐标引用相比视觉标记引用造成了约 0.15 δ1 的精度损失（Finding 1, Figure 2）。其因果机制在于：VLM 的视觉编码器天然适合处理视觉信号，将像素位置编码为文本坐标需要模型学习从离散坐标到图像空间的复杂映射，而这一映射在有限训练数据下难以建立。

**瓶颈二：相机歧义**。不同数据集使用不同相机拍摄，其焦距差异导致相同场景的成像尺度不同。VLM 在没有架构修改的情况下，难以区分这种相机差异，直接混合训练时精度严重受限。实验表明，统一焦距的内参条件增强可使精度相比其他相机歧义处理策略翻倍（Finding 3, Figure 4a）。

### Changed Slots：从基线到提出的关键转变

| 技术维度 | 基线方法 | DepthLM 方案 | 证据强度 |
|---------|---------|-------------|---------|
| **像素位置引用** | 文本提示中提供像素坐标 | 在输入图像上渲染视觉标记（小箭头） | 强（Figure 2, Finding 1） |
| **相机歧义处理** | 直接混合或不处理焦距差异 | 根据相机内参缩放图像，统一焦距为 1000 像素 | 强（Figure 4a, Finding 3） |
| **训练损失函数** | 纯视觉模型使用回归损失、尺度不变损失等 | 仅使用文本交叉熵损失的 SFT | 强（Finding 2, Finding 4） |
| **标签密度** | 密集逐像素深度标签 | 每张图像稀疏标注 1 个像素的深度值 | 强（Figure 5, Finding 4） |

### 核心洞察的证据链

DepthLM 的核心洞察可概括为：**仅需每张训练图像一个稀疏标注像素的文本 SFT，结合视觉提示和焦距统一增强，无需任务特定架构或复杂回归损失，VLM 即可实现与纯视觉模型相当的度量深度估计精度**。这一论断由以下证据链支撑：

1. **视觉标记的优越性**：无论标记的具体形状如何，视觉提示均远优于文本坐标引用（Figure 2），说明关键在于信息模态而非标记设计。

2. **焦距统一的关键作用**：统一焦距设置为 1000 像素时性能最佳，且对焦距值在较宽范围内不敏感（Figure 4b），表明该方法具有工程鲁棒性。

3. **图像多样性优于标签密度**：在固定训练样本数（80K）下，增加图像数量（降低每图标签密度）比增加标签密度（减少图像数量）带来更高精度（Figure 5）。这一反直觉发现说明 VLM 的 3D 理解能力更依赖于场景多样性而非标签密集度。

4. **SFT 的效率优势**：SFT 与强化学习（GRPO）在相同训练数据量下准确度相当，但 SFT 每样本计算效率高 8-16 倍（Figure 3b），使得大规模训练切实可行。

### 方法管线

DepthLM 的整体流程由三个模块构成（Figure 6）：

1. **CamIntriAugmentation**：根据相机内参缩放图像，统一焦距至 $f_{\mathrm{uni}} = 1000$ 像素。缩放公式为：
   $$W' = \frac{f_{\mathrm{uni}}}{f_x} W, \quad H' = \frac{f_{\mathrm{uni}}}{f_y} H$$

2. **VisualMarkerRenderer**：在统一焦距后的图像上绘制指向查询像素的视觉标记（小箭头），替代文本坐标引用。

3. **VLM Fine-tuning (SFT)**：利用带视觉标记的图像和文本问答对（如“该像素的深度是多少？”）微调预训练 VLM，仅使用文本交叉熵损失，无需回归头或正则化损失。



![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/011_Figure_5.jpg]]
*Figure 5: Increase number of images vs increase label density. Given the same training dataset size (80K samples), increasing label density while proportionally decreasing the number of images hurts the performance of DepthLM. Figure 6: DepthLM. DepthLM first augment the input image to have a unified focal length. Then, it renders visual markers on the image for pixel reference and uses text to interact with VLMs directly*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/017_Figure_9.jpg]]
*Figure 9: Actual markers rendered by our method. We show here 3 different types of markers used in the experiment of Fig. 2*

DepthLM 的整体流程由三个核心模块串联构成，将标准视觉语言模型（VLM）转化为逐像素度量深度估计器，无需引入任务特定的回归头或密集预测架构。

### 流程概览

如图 6 所示，DepthLM 的推理管线为：**输入图像 + 相机内参 → 焦距统一增强 → 视觉标记渲染 → VLM 文本对话 → 度量深度值**。

1. **CamIntriAugmentation（焦距统一增强）**  
   给定原始图像 $I$ 及其相机内参（焦距 $f_x, f_y$），模块根据预定义的统一焦距 $f_{\mathrm{uni}} = 1000$ 对图像进行缩放：
   $$W' = \frac{f_{\mathrm{uni}}}{f_x} W, \quad H' = \frac{f_{\mathrm{uni}}}{f_y} H$$
   其中 $W, H$ 为原始宽高，$W', H'$ 为缩放后尺寸。此步骤消除了不同数据集因相机内参差异引入的尺度模糊（Finding 3），使 VLM 在统一焦距条件下处理所有场景。

2. **VisualMarkerRenderer（视觉标记渲染）**  
   在焦距统一后的图像上，于查询像素位置直接绘制视觉标记（如小箭头、方块或十字），而非在文本提示中提供像素坐标。这一设计源于 Finding 1：VLM 对基于标记的像素引用理解能力远优于文本坐标引用——在 ScanNet++ 上 δ1 精度差距可达 0.15。

3. **VLM Fine-tuning (SFT)（文本监督微调）**  
   将带视觉标记的图像与文本问答配对，对预训练 VLM（默认基于 3B 参数的 Qwen 系列模型）进行标准监督微调。训练仅使用文本交叉熵损失进行下一 token 预测，无需回归损失或正则化项（Finding 4）。每张训练图像仅需 1 个稀疏标注像素的深度值即可实现强 3D 理解。

### 训练与推理特性

- **标签效率**：在固定训练样本总量（如 80K）下，增加图像数量（降低每张图像的标签密度）比增加标签密度（减少图像数量）带来更高精度（Figure 5）。图像多样性对 VLM 的 3D 理解比标签密度更为关键。
- **训练效率**：SFT 相比强化学习（GRPO）在相同数据量下精度相当，但每样本计算效率高 8–16 倍（Figure 3b），更适合大规模 VLM 训练。
- **密集深度图生成**：尽管仅针对单点预测训练，DepthLM 可通过逐像素独立查询生成高质量点云，无需密集预测头。这得益于视觉标记有效赋予了 VLM 精确的像素位置理解能力。

### 工程细节

训练时，焦距统一后的图像会进行随机裁剪（宽度 1000–1400 像素，高度 700–1200 像素），以保持评估时的通用性。统一焦距 $f_{\mathrm{uni}} = 1000$ 在较宽范围内对性能不敏感（Figure 4b），且在所有相机歧义处理策略中表现最优，精度较直接混合训练翻倍（Figure 4a）。



DepthLM 的方法框架由三个关键模块串联构成，其设计直接回应了 VLM 在逐像素度量深度估计中的两大瓶颈：像素位置引用的精度不足，以及跨数据集相机内参差异导致的尺度模糊。

### 1. 内参条件图像增强（CamIntriAugmentation）

不同数据集的相机焦距差异显著，直接混合训练会导致 VLM 无法区分相机固有属性与场景几何，产生严重的尺度模糊。该模块的解决思路是：在图像输入 VLM 之前，利用已知的相机内参将图像缩放至统一焦距。

具体操作为：给定原始图像宽度 $W$、高度 $H$，以及相机的水平焦距 $f_x$ 和垂直焦距 $f_y$（单位：像素），将图像缩放至新尺寸 $W'$ 和 $H'$，使得等效焦距统一为预设值 $f_{\mathrm{uni}} = 1000$ 像素。缩放公式为：

$$W' = \frac{f_{\mathrm{uni}}}{f_x} W, \quad H' = \frac{f_{\mathrm{uni}}}{f_y} H$$

**变量含义**：
- $W, H$：原始图像的宽和高（像素）
- $f_x, f_y$：原始相机在水平和垂直方向上的焦距（像素）
- $f_{\mathrm{uni}}$：预定义的统一焦距，经验最优值为 1000 像素
- $W', H'$：缩放后图像的宽和高（像素）

**关键证据**：消融实验（Figure 4a）表明，统一焦距的策略使模型精度相比其他相机歧义处理方案直接翻倍。进一步分析（Figure 4b）显示，$f_{\mathrm{uni}}$ 在较宽范围内（如 800–1200 像素）对性能影响不敏感，但设置为 1000 时达到最优。为保持评估时的通用性，训练过程中会对缩放后的图像进行随机裁剪（宽度 1000–1400 像素，高度 700–1200 像素）。

### 2. 视觉标记渲染（VisualMarkerRenderer）

传统 VLM 依赖文本坐标（如“像素 (x, y)”）来引用图像位置，但实验表明这种文本化的空间指代精度极差。该模块的解决方案是：直接在输入图像上渲染视觉标记（小箭头），指向需要查询深度的目标像素。

具体而言，给定查询像素坐标 $(x_q, y_q)$，模块在增强后的图像上绘制一个指向该位置的箭头标记，然后将带标记的图像与文本问题（如“该点深度是多少米？”）一同输入 VLM。VLM 通过视觉理解标记的位置来定位查询像素，而非解析文本坐标。

**关键证据**：Figure 2 的对比实验显示，文本坐标引用在室内场景（ScanNet++）上导致 δ1 精度下降约 0.15，而视觉标记的形状对性能影响很小，证明核心增益来自“视觉定位”这一交互范式本身。该发现是 DepthLM 能够使用标准 VLM 文本 SFT 训练的前提。

### 3. 文本监督微调（VLM Fine-tuning with SFT）

在解决了像素引用和相机歧义后，DepthLM 不需要任何任务特定的架构修改或回归损失函数。训练仅使用标准的文本监督微调：将数值化的 3D 标签通过模板转换为文本问答对，然后以 next-token prediction 范式对 VLM 进行微调，损失函数为文本 token 上的交叉熵损失。

**关键证据**：Finding 2（Figure 3b）表明，在相同训练数据量下，SFT 与强化学习（GRPO）达到相当的精度，但 SFT 的每样本计算效率高出 8–16 倍。Finding 4（Figure 4c, Figure 5）进一步揭示，每张训练图像仅需 1 个稀疏标注像素即可训练出强大的深度估计模型；在固定训练样本总量下，增加图像数量（降低标签密度）比增加标签密度（减少图像数量）带来更高的精度。这表明图像多样性比标签密度对 VLM 的 3D 理解更为关键。



## 实验与关键发现

### 核心发现与消融分析

DepthLM的性能提升源于三个相互协同的设计选择，本节通过受控实验逐一验证其因果效应。

**视觉标记 vs 文本坐标：像素引用的决定性差异。** 实验表明，视觉语言模型对基于标记的像素位置引用理解能力远优于文本坐标。如图2所示，在室内场景ScanNet++上，文本坐标引用导致δ1精度下降约0.15，而视觉标记（箭头、方块、十字等形状）之间的性能差异很小。这一发现说明瓶颈不在于标记的具体视觉形式，而在于VLM是否能够建立图像空间与查询意图的直接映射——文本坐标需要模型进行数值-空间的间接转换，而视觉提示绕过了这一认知鸿沟。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/004_Figure_2.jpg]]
*Figure 2: Pixel reference*

**SFT vs GRPO：训练效率与精度的权衡。** 在相同训练数据量下，监督微调（SFT）与GRPO强化学习达到相当的精度水平（图3b），但SFT的每样本计算效率高出8-16倍。在奖励函数选择上，负L1损失（NegL1）被验证为最佳GRPO奖励信号（图3a），但即便使用最优奖励，GRPO也未能带来精度优势。这一结果揭示了一个关键机制：对于度量深度估计这类需要精确数值输出的任务，直接监督信号比探索式奖励优化更高效，因为奖励函数的稀疏性和噪声会显著降低样本利用率。

**相机歧义处理：焦距统一的必要性。** 当混合多个相机内参不同的数据集训练时，不进行任何处理的VLM精度极低。图4a显示，统一焦距的图像增强策略使精度相较其他处理方式（如提供内参文本、归一化深度值）翻倍。根本原因在于VLM缺乏纯视觉模型中常见的架构设计（如内参编码器），无法从原始像素中推断相机属性，因此必须通过图像变换显式消除焦距差异。进一步实验（图4b）表明，统一焦距设置为1000像素时性能最优，且该参数在较宽范围内（约800-1200像素）表现稳定，说明模型对精确焦距值不敏感，只需消除跨样本的相对差异即可。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/009_Figure_4.jpg]]
*Figure 4: (a) Accuracy of different camera (b) Increasing $f _ { \mathrm { u n i } }$ benefits the per- (c) Accuracy with different number ambiguity handling strategies. formance until 1000 pixels. of training samples. Figure 4: Mix data training analysis. For (a) and (b), we train on 500K samples on the mixed datasets of DepthLMBench, and report the average accuracy across all evaluation datasets*

**标签密度 vs 图像多样性：数据效率的反直觉发现。** 在固定训练样本总量（80K）的条件下，增加图像数量同时降低每张图像的标注像素数，比增加标注密度同时减少图像数量带来更高精度（图5）。极端情况下，每张图像仅使用1个标注像素即可训练出δ1超过0.8的强大深度估计模型（图4c）。这一发现挑战了密集监督的传统范式：对于VLM的3D理解能力涌现，图像场景的多样性远比单张图像的标签密度重要。其深层原因可能是VLM已从预训练中获得了丰富的视觉先验，稀疏标注足以激活并校准这些先验到度量深度空间。

### 与通用VLM和空间VLM的对比

Table 1汇总了DepthLM与现有VLM在DepthLMBench八个数据集上的平均性能。通用VLM在零样本条件下表现极差：GPT-5仅获得0.370的平均δ1，Qwen2.5-VL（72B）和Gemini-2.5-Pro等模型同样低于0.4。即使经过度量深度微调的Seed1.5-VL也仅达到0.534。相比之下，DepthLM 3B达到0.824，7B版本进一步提升至0.838，实现了超过2倍的相对提升。值得注意的是，DepthLM的参数量比GPT-5小数个数量级，说明当前通用VLM的3D感知能力严重受限于像素引用和相机歧义这两个瓶颈，而非模型容量不足。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/013_Table_1.jpg]]
*Table 1: VLM result. We tune the prompt for VLMs that are not trained directly on our task to maximize their performance. State-of-the-art VLMs including GPT-5 have only below 0.4 $\delta _ { 1 }$ . DepthLM, though orders of magnitudes smaller, achieves an over 2x improvement*

在跨域泛化方面，DepthLM在NuScenes（室外自动驾驶）上达到0.865 δ1，较GPT-5的0.280提升0.585；在sunRGBD（室内）上达到0.859。这一致的跨域优势验证了焦距统一增强在零样本泛化中的关键作用。

### 与纯视觉模型的直接对比

Table 2将DepthLM 7B与六种主流纯视觉度量深度模型进行直接比较。在室外数据集上，DepthLM与DepthPro、Metric3Dv2等专家模型的差距已缩小至3-5%以内；在DDAD上DepthLM达到0.747，略低于Metric3Dv2的0.783（相对差距4.8%）。在室内数据集sunRGBD上，DepthLM以0.859超越DepthPro的0.835。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/014_Table_2.jpg]]
*Table 2: Comparison with pure vision models. For pure vision models, we use the numbers reported in (Piccinelli et al., 2025), and (Bochkovskii et al., 2024) if some numbers do not exist in (Piccinelli et al., 2025). “-” means no result reported in previous papers. The last column reports the relative accuracy improvement of pure vision models over our model, i.e., ( $\delta _ { 1 } ^ { \mathrm { C V } } - \delta _ { 1 } ^ { \mathrm { O u r s } }$ ) / $\delta _ { 1 } ^ { \mathrm { O u r s } }$ Our model is the first VLM that has comparable accuracy to pure vision models

这一结果具有范式意义：首次证明仅使用文本对话监督和稀疏标注（每图1-4个像素），无需任务特定架构、密集回归损失或深度预测头，VLM即可达到与纯视觉专家模型可比的度量深度精度。纯视觉模型的剩余优势主要体现在平滑区域（图8），因为它们输出密集预测天然具有空间连续性，而DepthLM逐像素独立查询会产生边界清晰的点云，但在非边界区域缺乏平滑先验。

### 多任务3D理解扩展

Table 3展示了DepthLM在六类3D理解任务上的泛化能力。在单点深度估计之外，模型被扩展至主轴距离、速度、时间、两点距离和度量尺度相机位姿估计。DepthLM 7B在所有任务上均大幅领先基线：平均δ1达到0.804，而Qwen2.5-VL（7B）仅0.09（基本失败），GPT-5在相机位姿估计中甚至返回0m位移而真实位移超过5m（图7）。两点距离和位姿估计任务的精度（0.721和0.679）仍显著低于单点深度（0.828），说明VLM的复杂多步3D推理能力仍有较大提升空间。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/016_Table_3.jpg]]
*Table 3: Multi-task result. Since not all datasets have pose labels, we train the pose task on Argoverse2 and evaluate on Argoverse2 and Nuscenes*

### 失败模式与局限性

尽管整体性能强劲，DepthLM存在以下已知局限：

1. **密集预测效率低**：生成完整深度图需逐像素独立查询VLM，计算开销远高于端到端纯视觉模型的一次前向传播。这在实时或大规模应用中构成瓶颈。
2. **复杂推理能力不足**：多点距离和位姿估计精度明显低于单点深度，表明模型在需要多步空间推理的任务上尚未充分涌现能力。
3. **训练数据覆盖有限**：仅使用高质量真实世界数据集，未利用大规模合成数据（如Hypersim、IRS），可能限制在极端光照、遮挡或陌生场景下的泛化能力。
4. **焦距统一带来的工程复杂度**：缩放改变图像尺寸后，训练时需随机裁剪以保持评估通用性，增加了数据管道的复杂度。

### 关键图表索引

- **Figure 2**：视觉标记与文本坐标的像素引用精度对比
- **Figure 3**：SFT与GRPO在精度和效率上的系统对比
- **Figure 4**：混合数据集训练策略分析（相机歧义处理、统一焦距选择、训练样本量影响）
- **Figure 5**：图像数量与标签密度的相对重要性
- **Table 1**：与通用VLM和空间VLM的全面对比
- **Table 2**：与纯视觉度量深度模型的直接精度对比
- **Table 3**：多任务3D理解扩展结果

### 补充图表

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/018_Table_4.jpg]]
*Table 4: Statistics of different training datasets. We report \<images available in the dataset> / \<images used for our training>*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/020_Table_5.jpg]]
*Table 5: Hyper-parameters of different experiments*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/021_Table_6.jpg]]
*Table 6: MultiTask performance on individual datasets*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ObFVZGnSFN/figures/019_Figure_10.jpg]]
*Figure 10: SFT vs GRPO with cross dataset evaluation. We show the result when we train on Argoverse2 and evaluate on NuScenes. The trend is similar as in Fig. 3b*



## 定位与知识库关联

### 与基线工作的关系

DepthLM 处于通用视觉语言模型（VLM）与专业纯视觉深度估计器的交叉地带，其核心贡献在于通过两个关键设计——视觉提示（visual prompting）和内参条件增强（intrinsic-conditioned augmentation）——弥合了 VLM 在逐像素度量深度估计上与纯视觉模型之间的鸿沟。

**与通用 VLM 的对比**：当前最先进的通用 VLM，如 **GPT-5**（Singh et al., 2025）、**Qwen2.5-VL**、**Gemini-2.5-Pro** 等，在零样本度量深度估计上表现极差。Table 1 显示 GPT-5 在 DepthLMBench 的 8 个数据集上平均 δ1 仅为 0.370，而 DepthLM 7B 达到 0.838，提升超过 2 倍。这种差距的根源在于通用 VLM 缺乏精确的像素位置引用能力——它们在文本提示中接收像素坐标，却无法准确理解图像中的对应位置（Finding 1，Figure 2）。DepthLM 通过直接在图像上渲染视觉标记（小箭头）替代文本坐标，从根本上解决了这一瓶颈。

**与度量深度微调 VLM 的对比**：**Seed1.5-VL**（Guo et al., 2025）是此前少数尝试将 VLM 微调用于度量深度的工作，但其仍采用文本坐标引用像素位置，精度远低于 DepthLM。Table 1 中 Seed1.5-VL 的平均 δ1 仅约 0.3 量级，验证了文本坐标引用是核心性能瓶颈。

**与空间推理 VLM 的对比**：**SpatialRGPT**（Cheng et al., 2024）和 **SpaceLLaVA** 等空间 VLM 虽能进行一定的 3D 推理，但在精确度量深度上仍远逊于 DepthLM（Table 1）。这表明通用的空间理解能力不足以替代针对度量深度的专门设计。

**与纯视觉深度模型的对比**：这是 DepthLM 最关键的定位。纯视觉度量深度模型如 **DepthPro**（Bochkovskii et al., 2024）、**Metric3Dv2**（Hu et al., 2024）、**UniDepthV2**（Piccinelli et al., 2025）等，通常依赖密集逐像素标签、特定架构设计和复杂的回归损失函数。DepthLM 仅使用每张图像 1 个标注像素的文本 SFT 训练，在 Table 2 中即达到与这些专业模型相当甚至更优的精度：在 sunRGBD 上 DepthLM 7B 的 δ1 为 0.859，超过 DepthPro 的 0.835；在 NuScenes 上达到 0.865。这是 VLM 首次在度量深度估计上与纯视觉模型持平。然而，纯视觉模型在部分场景仍保持优势——Table 2 最后一列显示 Metric3Dv2 在 DDAD 上相对 DepthLM 有约 2.6% 的优势，说明 VLM 在特定域上仍有追赶空间。

### 适用边界

**有效边界**：
- DepthLM 在真实世界室内外场景的度量深度估计上表现强劲，涵盖从 sunRGBD（室内）到 NuScenes（室外自动驾驶）的广泛数据集。
- 其视觉提示策略对标记形状不敏感（Figure 2），表明方法具有良好的鲁棒性。
- 统一焦距增强在 f_uni = 1000 像素附近较宽范围内性能稳定（Figure 4b），降低了超参数调优负担。

**退化边界**：
- 训练仅使用高质量真实世界数据集，未利用大规模合成数据。在极端光照、陌生相机模型或严重域偏移场景下的泛化能力未经充分验证。
- 多点和多帧任务（如两点距离、相机位姿估计）的精度显著低于单点深度估计（Table 3），表明 VLM 的复杂空间推理能力仍有限。
- 生成密集深度图需逐像素独立查询 VLM，推理计算开销远大于端到端纯视觉模型，限制了实时应用场景。
- 焦距统一增强改变了图像尺寸，训练时需随机裁剪以保持评估通用性，增加了工程部署复杂度。

### 局限与开放问题

**已知局限**：
1. **数据多样性受限**：训练仅使用高质量真实世界数据集，未利用大规模合成数据，可能限制在极端或陌生场景下的泛化能力。
2. **复杂 3D 推理不足**：多点和多帧任务的精度仍显著低于单点深度估计，VLM 的复杂 3D 推理能力有待提升。
3. **推理效率瓶颈**：生成密集深度图需要逐像素独立查询，推理计算开销大，效率低于端到端纯视觉模型。
4. **工程复杂度**：焦距统一增强改变了图像尺寸，需在训练时随机裁剪以保持评估时的通用性，增加了工程复杂度。

**开放问题**：
1. **超越纯视觉模型**：能否通过更细粒度的视觉提示（如多标记、区域标记）或迭代推理策略，使 VLM 在度量深度估计上超越顶尖纯视觉模型？
2. **数据扩展策略**：如何设计高效的数据过滤和增强流程，以整合更多样化（甚至嘈杂）的训练数据，同时不损害精度？
3. **多任务联合训练**：利用多任务联合训练是否能进一步增强单任务的泛化性能，并解锁更复杂的 3D 理解能力（如场景重建、物体姿态估计）？
4. **弱监督与自监督**：在自监督或弱监督设置下，VLM 能否利用海量无标注图像数据进一步提升 3D 感知，减少对标注的依赖？
5. **推理效率优化**：能否通过设计专门的解码策略或轻量化架构，在保持精度的同时降低逐像素查询的推理开销？



## 原文 PDF

![[paperPDFs/ICLR_2026/DepthLM_Metric_Depth_from_Vision_Language_Models.pdf]]

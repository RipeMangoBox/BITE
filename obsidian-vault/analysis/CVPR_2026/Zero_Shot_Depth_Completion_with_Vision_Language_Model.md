---
title: Zero-Shot Depth Completion with Vision-Language Model
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Zero_Shot_Depth_Completion_with_Vision_Language_Model.pdf
project_link: null
code_link: null
aliases:
- VBDCSDIMS
- ZSDCVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将稀疏深度转化为二值掩码文本提示（0表示需预测，1表示需保留）并结合深度值文本描述，使VLM能够根据语言指令精确控制补全区域，从而显著提升零样本泛化能力。
primary_logic: 利用视觉语言模型（VLM）的跨模态语义理解与指令遵循能力，将深度补全重新定义为文本驱动的像素级几何推理任务，仅通过稀疏深度即可实现强大的零样本泛化，无需稠密真值监督。
claims:
- 在七个零样本基准测试中，我们的方法（使用稀疏深度监督）相比最优方法取得了最高17.3%的提升。
- 在VOID 150数据集上，同时结合掩码文本提示和深度值的模型（SDIM-(e)）RMSE降至0.185m，明显优于仅使用掩码提示（SDIM-(d)）的0.188m，验证了文本提示中深度值信息的重要性。
- 零初始化卷积的软融合策略比直接拼接（硬融合）在IBims-1上降低RMSE 7mm，证明逐步注入深度先验的必要性。
- IBims-1 上 MAE / RMSE (m) = 0.040 / 0.158
---

# Zero-Shot Depth Completion with Vision-Language Model

> [!tip] 核心洞察
> 利用视觉语言模型（VLM）的跨模态语义理解与指令遵循能力，将深度补全重新定义为文本驱动的像素级几何推理任务，仅通过稀疏深度即可实现强大的零样本泛化，无需稠密真值监督。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于视觉语言模型的零样本深度补全 |
| 英文题名 | Zero-Shot Depth Completion with Vision-Language Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yan_Zero-Shot_Depth_Completion_with_Vision-Language_Model_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VLM-based Depth Completion with Sparse Depth Injection Mechanism (SDIM) |
| Dataset | IBims-1, VOID 150, NYUv2, KITTI |

> [!tip] 效果简介
> - IBims-1 上，MAE / RMSE (m) 0.040 / 0.158 vs NLSPN: 0.049 / 0.191 (MAE -0.009, RMSE -0.033)。
> - VOID 150 上，MAE / RMSE (m) 0.185 / 0.604 vs NLSPN: 0.492 / 0.963 (MAE -0.307, RMSE -0.359)。
> - NYUv2 上，MAE / RMSE (m) 0.044 / 0.121 vs SpAgNet: 0.158 / 0.292 (MAE -0.114, RMSE -0.171)。

## 概述

深度补全旨在从稀疏深度测量恢复稠密深度图，是三维视觉中的基础任务。现有方法普遍将稀疏深度作为额外通道嵌入专用网络，缺乏显式的“哪里预测、哪里保留”的指导，导致在未见场景中零样本泛化能力受限。

本文提出基于视觉语言模型（VLM）的稀疏深度注入机制 **SDIM**，将深度补全重新定义为文本驱动的像素级几何推理任务。核心洞察在于：利用VLM的跨模态语义理解与指令遵循能力，将稀疏深度转化为二值掩码文本提示（0表示需预测，1表示需保留）并结合深度值文本描述，使模型能够根据语言指令精确控制补全区域。SDIM通过三个关键组件实现这一目标——**视觉分词**采用零初始化卷积对RGB与稀疏深度进行软融合，逐步注入几何先验；**文本提示生成**将稀疏深度及其掩码转换为自然语言指令；**文本监督微调**利用稀疏深度自动生成的文本标签（如“该像素距离相机5.20米”）训练语言解码器，无需任何稠密真值监督。

在七个零样本基准测试中，该方法使用稀疏深度监督即可取得最高17.3%的相对提升。消融实验验证了各组件的因果贡献：零初始化卷积的软融合策略相比直接拼接在IBims-1上降低RMSE 7mm；同时引入掩码提示与深度值文本提示在VOID 150上带来稳定的误差递减（RMSE从0.204降至0.185）。该框架开辟了利用VLM文本指令实现稠密几何推理的新范式，其局限性在于反射表面附近深度估计不够可靠，且VLM自回归解码仍带来较大的推理延迟。

## 背景与动机

### 任务定义与核心挑战

深度补全旨在从稀疏深度测量和对应的RGB图像中恢复稠密的深度图。该任务在自动驾驶、机器人导航、增强现实等三维感知场景中具有关键作用。其核心挑战在于：稀疏深度点仅覆盖场景中极小比例的像素（通常不足1%），模型必须从极度稀疏的几何线索中推断出完整、平滑且几何一致的场景结构。

### 现有方法的瓶颈

当前深度补全研究主要沿两条路径展开。一类方法专注于**任务特定的架构设计**，通过精心设计的卷积网络、注意力机制或空间传播模块来融合RGB与稀疏深度信息。然而，这类方法通常依赖大规模稠密真值深度图进行监督训练，导致其在训练分布之外的未见场景中泛化能力显著下降。

另一类方法则借助深度基础模型的强大先验，探索**零样本深度补全**。例如，**Marigold-DC**（Viola et al., ICCV 2025）利用预训练扩散模型进行深度补全，在多个零样本基准上取得了领先性能。但这类方法存在一个根本性局限：它们仅将稀疏深度作为额外的输入通道嵌入网络，而**未显式区分有效测量区域与缺失区域**，缺乏“哪里需要预测、哪里需要保留”的明确指导。这导致模型在稀疏深度覆盖极低或场景结构复杂时，难以精确利用已有的可靠测量，补全质量受限。

### 核心动机：语言作为几何推理的桥梁

视觉语言模型（VLM）在跨模态语义理解和指令遵循方面展现出强大能力，已有工作（如**DepthLM**）将逐像素深度估计转化为语言建模任务，证明了文本监督范式的可行性。这启发了一个关键问题：**能否利用VLM的语言理解能力，将稀疏深度转化为精确的文本指令，从而显式地指导模型进行几何推理？**

本文的核心动机在于：将深度补全重新定义为**文本驱动的像素级几何推理任务**。具体而言，通过将稀疏深度转化为二值掩码文本提示（0表示需预测区域，1表示需保留区域），并结合具体的深度值描述，使VLM能够根据语言指令精确控制补全过程。这一范式转变使得模型仅需稀疏深度即可进行文本监督微调，无需任何稠密真值深度图，从而在根本上解耦了训练数据依赖与零样本泛化之间的矛盾。

## 核心创新

本文的核心贡献在于将深度补全任务重新定义为**文本驱动的像素级几何推理问题**，并为此设计了一套**稀疏深度注入机制（Sparse Depth Injection Mechanism, SDIM）**。与现有方法将稀疏深度仅作为额外视觉通道嵌入网络不同，SDIM通过三个关键环节实现了对“何处预测、何处保留”的显式控制，从而在零样本场景中取得显著提升。

### 从隐式融合到显式指令引导

现有深度补全方法的根本瓶颈在于缺乏对有效测量与缺失区域的区分性指导——稀疏深度点被无差别地输入网络，模型无法获知哪些像素已有可靠观测、哪些需要外推。本文的因果调节变量（causal knob）是将稀疏深度转化为**二值掩码文本提示**：掩码值为0的区域表示“需预测”，值为1的区域表示“需保留”。这一设计使视觉语言模型（VLM）能够根据语言指令精确控制补全行为，而非依赖隐式特征学习。

进一步地，SDIM将稀疏深度的具体数值也编码为文本描述（如“该像素距离相机5.20米”），与掩码提示共同构成语言解码器的输入。消融实验验证了这一设计的必要性：在VOID 150数据集上，仅使用掩码提示的变体SDIM-(d)的RMSE为0.188m，而同时引入深度值文本提示的SDIM-(e)进一步降至0.185m，表明**深度值的显式文本编码为模型提供了关键的尺度与几何先验**。

### 三个关键设计槽位（Changed Slots）的因果分析

相比于以**Marigold-DC**（Viola et al., ICCV 2025）为代表的先前最优零样本方法，本文在以下三个维度上进行了根本性重构：

**1. 视觉输入模态：从纯RGB到RGB-D软融合**

传统零样本方法仅依赖RGB图像进行单目深度估计，稀疏深度信息未被充分利用。SDIM引入零初始化卷积对RGB和稀疏深度进行软融合。消融实验表明，相比于直接将稀疏深度与RGB特征拼接（硬融合），零初始化卷积的渐进式注入策略在IBims-1上降低了7mm RMSE。这一设计的核心机理在于：零初始化确保训练初期稀疏深度分支不干扰预训练的视觉表征，随后逐步注入几何先验，避免了硬融合可能引发的特征冲突。

**2. 文本提示：从无引导到显式区域控制**

现有方法完全依赖视觉特征进行深度补全，缺乏对有效测量区域的显式建模。SDIM将稀疏深度的二值掩码和深度值转化为自然语言提示，使VLM能够根据文本指令区分“预测”与“保留”区域。这一转变的本质是将深度补全从纯视觉回归问题转化为**指令遵循任务**，充分利用了VLM的跨模态语义理解能力，是零样本泛化能力提升的核心驱动力。

**3. 监督信号：从依赖稠密真值到稀疏文本自监督**

传统深度补全方法需要稠密真值深度图进行监督训练，这严重限制了其在无标注场景中的适用性。本文利用稀疏深度自动生成文本标签（如“该像素距离相机5.20米”），实现了**无需任何稠密真值的文本监督微调**。这一设计使得方法在仅使用稀疏深度监督（w/ SD）的情况下，即可在七个零样本基准上取得最高17.3%的提升；若使用真值深度进行文本监督（w/ GT），还可在VOID 500、VOID 1500和DDAD上分别获得13.3%、10.1%和9.7%的RMSE相对提升。

### 创新边界与待验证问题

尽管SDIM在零样本泛化上表现突出，其当前实现仍存在若干局限：推理依赖VLM的自回归解码，虽比Marigold-DC快65倍，但延迟仍高于传统前馈网络；在玻璃等反射表面附近深度估计不够可靠（见Figure 6）；目前仅基于3B参数的**Qwen2.5-VL**进行验证，更大规模模型的表现尚待探索。此外，该VLM驱动框架能否有效扩展至其他稠密预测任务（如表面法线估计），以及如何设计更轻量的解码策略以进一步提升推理速度，是值得关注的开放问题。

## 整体框架

本文提出一种**基于视觉语言模型（VLM）的零样本深度补全框架**，其核心创新在于将深度补全重新定义为**文本驱动的像素级几何推理任务**。该框架以预训练的VLM为骨干，通过**稀疏深度注入机制（Sparse Depth Injection Mechanism, SDIM）**将稀疏深度测量无缝集成到VLM的视觉-语言管道中，使模型能够根据语言指令精确控制“哪里需要预测、哪里需要保留”，从而在无需稠密真值监督的情况下实现强大的零样本泛化。

### 核心瓶颈与设计动机

现有深度补全方法（无论是基于任务专用架构还是基于深度基础模型的零样本方案）存在一个共同瓶颈：**缺乏显式的“预测-保留”区域指导**。它们通常将稀疏深度作为额外通道嵌入网络，未区分有效测量区域与缺失区域，导致在未见场景中补全质量受限。SDIM 正是针对这一瓶颈设计，将稀疏深度转化为**二值掩码文本提示**（0表示需预测，1表示需保留），并结合深度值文本描述，使VLM能够根据语言指令精确控制补全区域。

### 整体管道与模块关系

如图3所示，SDIM由三大组件构成，形成完整的视觉-语言深度补全管道：

1.  **视觉分词（Visual Tokenization）**：接收RGB图像与稀疏深度图作为输入，通过零初始化卷积实现**软融合**，将稀疏几何先验渐进式注入视觉特征，而非直接拼接。
2.  **文本提示生成（Textual Prompt Generation）**：将稀疏深度及其二值掩码转换为自然语言描述，作为语言解码器的输入提示，指导模型“预测”与“保留”。
3.  **文本监督微调（Textual Supervision）**：利用稀疏深度自动生成每像素文本标签（如“该像素距离相机5.20米”），对VLM的语言解码器进行微调，无需任何稠密真值深度图。

### 输入输出流

-   **输入**：RGB图像 $\mathbf{I} \in \mathbb{R}^{H \times W \times 3}$ 和稀疏深度图 $\mathbf{S} \in \mathbb{R}^{H \times W}$。
-   **视觉侧处理**：RGB图像经标准卷积提取特征 $\hat{\mathbf{F}}$；稀疏深度通过零初始化卷积编码为 $\hat{\mathbf{S}}$，两者拼接后经复合操作投影融合，再通过预嵌入的零初始化卷积 $\mathcal{F}_c^z$ 处理，最终经3D卷积进行视觉分词。
-   **文本侧处理**：稀疏深度图 $\mathbf{S}$ 经 $\mathcal{F}_t$ 转换为文本描述 $\mathbf{T}$（包含二值掩码和深度值信息），与可学习查询 $\mathbf{Q}$ 和视觉特征 $\mathbf{V}$ 一同送入注意力模块 $\mathcal{F}_\delta$，生成每像素的注意力输出 $\mathbf{A}$。
-   **输出**：遍历所有像素的文本输出 $\mathbf{A}_j$，提取预测的深度值并重塑为稠密深度图 $\mathbf{D} \in \mathbb{R}^{H \times W}$：$\mathbf{D} = \mathcal{T}_{j=1}^{hw}(\mathbf{A}_j)$。

### 与先前范式的对比

图2清晰展示了本文框架与两类主流范式的本质差异：

-   **任务专用架构（图2a）**：依赖精心设计的网络结构（如编码器-解码器、传播模块），需要稠密真值监督训练，泛化能力受限于训练数据分布。
-   **深度基础模型零样本方案（图2b）**：借助预训练的单目深度估计模型进行零样本推理，但仍以纯视觉特征为核心，缺乏对稀疏深度测量的显式利用。
-   **本文VLM文本指令方案（图2c）**：首次将VLM引入深度补全，通过文本指令桥接稀疏几何测量与语义理解，实现“指令驱动”的零样本补全。

### 关键设计：零初始化卷积的软融合

在视觉分词阶段，本文采用**零初始化卷积**而非直接拼接来实现RGB与稀疏深度的融合。消融实验（Table 5）证实，这种软融合策略在VOID 150上相比硬融合降低RMSE达7mm，证明逐步注入深度先验对于保持VLM预训练视觉表征的完整性至关重要。具体而言，初始稀疏深度特征提取使用零初始化卷积 $\mathcal{F}_{\tau_2}^z$，预嵌入阶段再次使用零初始化卷积 $\mathcal{F}_c^z$，形成**渐进式深度信息注入**机制。

### 补充图表

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our method. It extends VLM [1] to the depth completion task via a sparse depth injection mechanism (SDIM). SDIM first performs a soft fusion between the sparse depth and the RGB image using convolutions with zero initialization. Then, the sparse depth is transformed into textual representations that prompt the model on where to predict and what to preserve. Meanwhile, for one image pixel, we query its distance to the camera. Finally, these textual representations derived from the sparse depth are employed to fine-tune the model, producing per-pixel depth descriptions and the final dense depth prediction*

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/002_Figure_2.jpg]]
*Figure 2: Framework comparisons. (a) Most previous depth completion studies emphasize task-specific architectural designs, while (b) recent works concentrate on zero-shot inference with the aid of depth foundation models. Differently, (c) we introduce text instructions based on VLM, offering a new perspective on depth completion*

## 核心模块与公式推导

### 3.1 稀疏深度注入机制（SDIM）总览

本文提出的稀疏深度注入机制（Sparse Depth Injection Mechanism, SDIM）将深度补全重新定义为文本驱动的像素级几何推理任务，包含三个关键模块：**视觉分词**、**文本提示生成**和**文本监督微调**。整体流程如 Figure 3 所示，稀疏深度与RGB图像首先通过零初始化卷积进行软融合，随后稀疏深度被转换为文本描述以指导模型“何处预测、何处保留”，最终利用这些文本描述对VLM的语言解码器进行微调，生成逐像素的深度预测。

---

### 3.2 视觉分词：零初始化卷积的软融合

视觉分词模块的核心设计是**零初始化卷积的渐进式深度先验注入**。传统方法通常将稀疏深度直接与RGB图像在通道维度拼接（硬融合），但这种方式在零样本场景下容易引入噪声。SDIM采用三阶段的软融合策略：

**阶段一：初始特征提取**

对RGB图像 $\mathbf{I}$ 和稀疏深度图 $\mathbf{S}$ 分别进行特征提取：

$$\hat{\mathbf{F}} = \mathcal{F}_{\tau_1}(\mathbf{I}) \tag{1a}$$

$$\hat{\mathbf{S}} = \mathcal{F}_{\tau_2}^z(\mathbf{S}) \tag{1b}$$

其中 $\mathcal{F}_{\tau_1}$ 表示“卷积 → 批归一化 → LeakyReLU”的复合操作，$\mathcal{F}_{\tau_2}^z$ 与之相同但卷积层采用**零初始化**（权重和偏置均为零）。零初始化的关键作用在于：训练初期稀疏深度分支对融合特征无贡献，模型首先从RGB图像学习可靠的视觉表征；随着训练推进，深度先验被逐步注入，避免了硬融合中深度噪声对视觉特征的污染。

**阶段二：RGB-D特征融合与投影**

将RGB特征 $\hat{\mathbf{F}}$ 和稀疏深度特征 $\hat{\mathbf{S}}$ 在通道维度拼接后，通过两次复合操作进行高低维空间投影：

$$\mathbf{M} = \mathcal{F}_{\tau_3}\left(\mathcal{F}_{\tau_2}\left(\mathcal{F}_{\psi}\left(\hat{\mathbf{F}}, \hat{\mathbf{S}}\right)\right)\right) \tag{2a}$$

其中 $\mathcal{F}_{\psi}$ 为拼接操作，$\mathcal{F}_{\tau_2}$ 和 $\mathcal{F}_{\tau_3}$ 分别将特征投影到高维和低维空间，增强跨模态特征的交互能力。

**阶段三：预嵌入的零初始化卷积**

在送入VLM的视觉编码器之前，对融合特征 $\mathbf{M}$ 再次应用零初始化卷积：

$$\mathbf{O} = \mathcal{F}_c^z(\mathbf{M}) \tag{2b}$$

这一设计确保VLM的预训练视觉表征不会被稀疏深度的引入所破坏，进一步强化了渐进式融合的效果。消融实验（Table 5）证实，零初始化卷积（SDIM-(c)）在VOID 150上将RMSE从无融合的0.204m降至0.197m，验证了软融合策略的必要性。

---

### 3.3 文本提示生成：二值掩码与深度值的语言化

文本提示模块将稀疏深度信息转化为VLM可理解的自然语言指令，包含**二值掩码提示**和**深度值提示**两个层次。

**二值掩码提示**：从稀疏深度图 $\mathbf{S}$ 生成二值掩码 $\mathbf{B}$，其中有效深度测量位置标记为1，缺失区域标记为0。该掩码被转换为文本描述，例如：

> “掩码值为0表示该像素深度缺失需要预测，掩码值为1表示该像素已有可靠深度测量需要保留。”

**深度值提示**：对于有效测量位置，进一步提取具体深度值 $y$ 并嵌入固定模板：

> “该像素距离相机 $y$ 米。”

完整的文本描述转换过程可表示为：

$$\mathbf{T} = \mathcal{F}_t(\mathbf{S}) \tag{4a}$$

其中 $\mathbf{T}$ 为生成的文本提示序列，同时包含掩码信息和深度数值。这些文本提示作为语言解码器的输入，通过注意力机制指导逐像素的深度预测：

$$\mathbf{A} = \mathcal{F}_{\delta}(\mathbf{T}, \mathbf{Q}, \mathbf{V}) \tag{4b}$$

消融实验（Table 5）表明，仅引入二值掩码提示（SDIM-(d)）将RMSE从0.197m降至0.188m，进一步加入深度值提示（SDIM-(e)）后RMSE降至0.185m，验证了文本提示中深度值信息对精确定位和尺度恢复的重要性。

---

### 3.4 文本监督微调与稠密深度重建

**文本监督微调**：SDIM利用稀疏深度自动生成文本标签，无需任何稠密真值深度图。对于每个训练样本，仅选取一个有效测量像素，将其深度值 $y$ 插入固定模板生成监督信号：

> “该像素距离相机 $y$ 米。”

模型使用L1损失对该像素的文本输出进行监督微调。这一设计的因果机制在于：VLM通过稀疏的文本监督学习到“如何将视觉特征映射为精确的深度文本描述”，从而在推理时能够对所有像素进行泛化预测。

**稠密深度重建**：推理阶段，模型对图像中的所有 $h \times w$ 个像素逐一生成文本输出，遍历提取预测的深度值并重塑为稠密深度图：

$$\mathbf{D} = \mathcal{T}_{j=1}^{hw}(\mathbf{A}_j) \tag{5}$$

其中 $\mathbf{A}_j$ 为第 $j$ 个像素的注意力输出，$\mathcal{T}$ 为从文本中解析数值的操作。该重建过程将VLM的自回归文本生成能力转化为结构化的稠密几何输出，实现了从稀疏测量到稠密预测的端到端推理。

## 实验与分析

### 实验设置

本文以 **Qwen2.5-VL (3B)** 作为基础视觉语言模型，在 Hypersim 和 Virtual KITTI 的 20K 子集上进行微调。训练使用 PyTorch 框架，在 8×48 GB GPU 上完成 10 个 epoch，总批大小为 16。所有对比方法的定量结果均直接引用自 **Marigold-DC**（Viola et al., ICCV 2025），以保证比较的公平性；复杂度对比在单块 NVIDIA 4090 GPU 上进行（Table 4）。用于微调和测试的数据集概览见 Table 1。

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/005_Table_1.jpg]]
*Table 1: Overview of datasets used for fine-tuning and testing. A subset of Hypersim and Virtual KITTI is utilized for fine-tuning*

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/009_Table_4.jpg]]
*Table 4: Complexity comparisons on the IBims-1 dataset. All methods are evaluated using a single 48GB 4090 GPU*

### 零样本泛化主结果

Table 2 汇总了在七个零样本基准上与最优方法的定量对比。在仅使用稀疏深度监督（w/ SD）的条件下，本文方法在多数基准上取得了最优或次优的 MAE 和 RMSE：

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/006_Table_2.jpg]]
*Table 2: Zero-shot depth completion comparisons with state-of-the-art methods. All results of other approaches are adopted from Marigold-DC [47]. The best and second-best metrics are highlighted. † denotes a least-squares estimate, and ‡ indicates the use of testtime ensembling. SD/GT means whether sparse depth or ground-truth depth is utilized to generate textual supervision during fine-tuning*

- **IBims-1**：MAE 0.040m / RMSE 0.158m，相比 NLSPN 分别降低 0.009m 和 0.033m，MAE 超越次优方法 **12.5%**。
- **VOID 150**：MAE 0.185m / RMSE 0.604m，相比 NLSPN 的 0.492m / 0.963m 大幅降低，MAE 超越次优方法 **4.9%**。
- **NYUv2**：MAE 0.044m / RMSE 0.121m，相比 SpAgNet 的 0.158m / 0.292m 有显著改善。
- **KITTI**：MAE 0.418m / RMSE 1.394m，MAE 略高于 VPP4DC（+0.005m），但 RMSE 降低 0.215m。
- **DDAD**：MAE 1.353m / RMSE 6.264m，MAE 略高于 VPP4DC（+0.009m），但 RMSE 降低 0.517m。

整体上，本文方法在七个零样本基准上相比最优方法取得了**最高 17.3%** 的提升。值得注意的是，KITTI 和 DDAD 上 MAE 微弱落后的现象可能与这两个数据集的稀疏深度分布特性有关，该点需结合原文 Table 2 的具体数值进行人工核实。

### 消融实验：稀疏深度注入机制（SDIM）的组件贡献

Table 5 在 VOID 150 上对 SDIM 的各组件进行了逐步消融，揭示了每个设计选择的因果贡献：

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/010_Table_5.jpg]]
*Table 5: Ablation studies of our sparse depth injection mechanism (SDIM) on VOID dataset with 150 depth points*

1. **基线（无稀疏深度融合）**：仅使用 RGB 图像和基础 VLM，RMSE 为 0.204m。
2. **零初始化卷积软融合（SDIM-(c)）**：在视觉分词前引入零初始化卷积进行 RGB-D 软融合，RMSE 降至 0.197m，**降低 7mm**。这验证了逐步注入深度先验的必要性——相比直接拼接（硬融合），零初始化策略使模型在训练初期保持稳定，逐步学习利用深度信息。
3. **文本掩码提示（SDIM-(d)）**：将稀疏深度的二值掩码转换为文本提示（0 表示需预测，1 表示需保留），RMSE 进一步降至 0.188m。这表明显式的“哪里预测、哪里保留”的语言指令能有效引导 VLM 的补全行为。
4. **深度值文本提示（SDIM-(e)）**：在掩码提示基础上加入具体深度值文本描述，RMSE 降至 0.185m。这一增量（0.003m）验证了深度值信息对精确补全的额外贡献。
5. **完整 SDIM（SDIM-(f)）**：同时利用视觉分支和文本分支的全部信息，RMSE 达到最优的 0.176m。

消融路径清晰地展示了瓶颈从“无显式补全引导”到“有掩码引导”再到“有掩码+深度值引导”的逐步解除过程。

### 真值深度监督的增益

当使用稠密真值深度生成文本标签进行监督（Ours w/ GT）时，方法在更大规模数据集上表现出进一步的提升：在 VOID 500、VOID 1500 和 DDAD 上分别取得 **13.3%**、**10.1%** 和 **9.7%** 的 RMSE 相对提升。Figure 5 在 IBims-1 上的可视化对比显示，真值监督主要在边缘锐度和细节保真度上带来改善，但稀疏深度监督已能产生几何一致的预测。

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/007_Figure_5.jpg]]
*Figure 5: Visual comparisons of our method supervised by sparse depth and ground-truth depth on the IBims-1 dataset*

### 不同 VLM 骨干的兼容性

Table 3 在 IBims-1 上对比了不同 VLM 骨干的性能。该方法不依赖于特定 VLM 架构，展示了框架的通用性。具体数值需参照原文 Table 3，但分析表明更大规模的 VLM 骨干有望进一步提升精度，当前仅基于 3B 参数模型进行探索。

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/008_Table_3.jpg]]
*Table 3: Comparisons with different VLM backbones on the IBims-1 dataset. GE denotes gradient error*

### 复杂度分析

Table 4 在 IBims-1 上对比了各方法的参数量、推理时间和显存占用。本文方法的推理速度比 **Marigold-DC** 快 **65 倍**，但 VLM 的自回归解码特性仍带来较大的推理延迟，这是实际部署中需要权衡的因素。

### 失败模式

Figure 6 展示了方法在**玻璃等反射表面**附近的失败案例。在这些区域，稀疏深度测量本身可能不可靠（如 LiDAR 在玻璃表面的反射异常），导致文本提示中的深度值信息存在误差，进而影响补全质量。这一局限性源于稀疏深度输入的质量，而非 VLM 框架本身的设计缺陷。

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/011_Figure_6.jpg]]
*Figure 6: Failure cases of our approach near glass surfaces*

### 开放问题

1. 该 VLM 驱动框架能否有效扩展至其他稠密预测任务（如表面法线估计）？
2. 如何设计更轻量、高效的 VLM 架构或解码策略以进一步提升推理速度？
3. 在完全没有稠密真值的情况下，如何利用更大规模的多模态数据增强泛化能力？

### 补充图表

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results on four benchmarks comparing CFormer [74], OGNI-DC [75], Marigold-DC [47], and our approach*

![[assets/figures/papers/paper_list_l2432_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Zero_Shot_Depth_Co/figures/001_Figure_1.jpg]]
*Figure 1: Visual comparisons of zero-shot depth completion under different sparsity levels. Our VLM-driven approach leverages textual instructions derived from sparse depth inputs to guide the completion process. Compared with previous state-of-the-art methods such as BPNet [44], our model consistently produces plausible and geometrically reliable depth predictions*

## 方法谱系与知识库定位

### 1. 范式转移：从任务专用架构到VLM驱动的文本指令补全

本文的核心贡献在于将深度补全问题从传统的视觉特征回归范式重新定义为**文本驱动的像素级几何推理任务**，这一转变标志着该领域的方法论演进进入新阶段。如图2所示，现有方法可划分为三个代际：

- **第一代：任务专用架构**。以 **NLSPN**（Park et al., ECCV 2020）、**BPNet**（Tang et al., CVPR 2021）等为代表，这些方法针对深度补全设计专门的网络结构（如非局部空间传播、双边引导融合），将稀疏深度作为额外通道嵌入卷积网络。其根本局限在于**缺乏显式的“预测/保留”区域指导**——网络无法区分有效测量与缺失区域，仅通过隐式学习来推断补全策略，导致在未见场景中泛化能力受限。

- **第二代：深度基础模型辅助的零样本方案**。以 **Marigold-DC**（Viola et al., ICCV 2025）为代表，这类方法借助预训练的深度估计基础模型（如Marigold扩散模型）实现零样本推理，无需在目标场景上进行微调。然而，这些方法仍依赖纯视觉信号，**未显式利用稀疏深度的几何约束来指导补全过程**。

- **第三代：VLM文本指令方案（本文）**。本文提出的**稀疏深度注入机制（SDIM）** 将稀疏深度转化为二值掩码文本提示（0表示需预测，1表示需保留），并结合深度值文本描述，使视觉语言模型能够根据语言指令精确控制补全区域。这一设计的**因果杠杆**在于：通过文本模态显式编码“哪里预测、哪里保留”的几何先验，VLM的跨模态语义理解与指令遵循能力被激活，从而在零样本条件下实现鲁棒的补全。

### 2. 与先驱工作的继承与突破

本文方法建立在两条关键先驱工作的基础之上：

- **DepthLM**：该工作首次将逐像素深度估计转化为语言建模任务，证明了文本监督范式的可行性。本文继承了其“每像素文本深度标签”的监督思路，但关键突破在于引入了**稀疏深度作为文本提示的生成源**，而非仅将其作为视觉输入。这使得模型能够在微调阶段利用稀疏深度自动生成文本标签（如“该像素距离相机5.20米”），**完全摆脱了对稠密真值深度图的依赖**。

- **Qwen2.5-VL (3B)**：作为基础VLM骨干，提供了跨模态语义理解与自回归解码能力。本文通过SDIM的三个组件（视觉分词、文本提示、文本监督）对其进行最小侵入式扩展，保留了原始VLM的预训练权重与推理能力。消融实验（Table 5）表明，各组件均带来稳定增益：零初始化卷积将RMSE从无融合的0.204降至0.197（VOID 150），引入文本掩码提示进一步降至0.188，加入深度值文本提示后达到0.185。

### 3. 适用边界与局限

尽管本文方法在七个零样本基准上取得了显著提升（最高17.3%），其适用边界仍存在以下约束：

- **反射表面的脆弱性**：在玻璃等反射表面附近，深度估计不够可靠（见图6）。这源于VLM对反射/折射场景的语义理解能力有限，文本提示中的几何约束无法完全弥补视觉歧义。

- **模型规模的探索不足**：当前仅基于3B参数的Qwen2.5-VL进行微调。Table 3展示了不同VLM骨干（InternVL3等）在IBims-1上的性能对比，但更大规模模型（如7B、13B）的表现尚待探索。理论上，更强的语义理解能力可能进一步提升补全质量，但推理成本也将显著增加。

- **推理延迟的权衡**：尽管比Marigold-DC快65倍（Table 4），VLM的自回归解码仍带来较大推理延迟。这是文本监督范式的固有代价——每像素的深度值需通过逐令牌解码生成，而非传统CNN的单次前向传播。

### 4. 开放问题与未来方向

本文开启的研究方向包括：

- **跨任务扩展**：该VLM驱动框架能否有效扩展至其他稠密预测任务（如表面法线估计、语义分割）？核心挑战在于设计适用于不同输出模态的文本提示模板与监督策略。

- **轻量化与高效解码**：探索更轻量的VLM架构或非自回归解码策略，以在保持文本指令优势的同时降低推理延迟。这可能涉及知识蒸馏、推测解码或混合视觉-文本分支的早期退出机制。

- **无真值条件下的规模化泛化**：在完全无稠密真值的情况下，如何利用更大规模的多模态数据（如互联网视频、合成数据）增强泛化能力？本文的真值监督实验（Ours w/ GT）表明，使用真值深度进行文本监督可在VOID 500、VOID 1500和DDAD上分别取得13.3%、10.1%和9.7%的RMSE相对提升，揭示了数据质量对性能的显著影响。

## 原文 PDF

![[paperPDFs/CVPR_2026/Zero_Shot_Depth_Completion_with_Vision_Language_Model.pdf]]

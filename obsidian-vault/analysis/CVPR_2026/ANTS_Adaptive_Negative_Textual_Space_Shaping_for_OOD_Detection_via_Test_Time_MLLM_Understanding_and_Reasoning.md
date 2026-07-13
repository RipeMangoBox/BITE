---
title: "ANTS: Adaptive Negative Textual Space Shaping for OOD Detection via Test-Time MLLM Understanding and Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ANTS_Adaptive_Negative_Textual_Space_Shaping_for_OOD_Detection_via_Test_Time_MLLM_Understanding_and_Reasoning.pdf
project_link: null
code_link: "https://github.com/ZhuWenjie98/ANTS"
aliases:
- AANTSS
- ANTS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 负文本空间的质量与适应性——能否准确刻画实际OOD分布，并自适应地处理远OOD与近OOD的不同特性。
primary_logic: 利用多模态大语言模型在测试时对在线挖掘的负图像进行理解与推理，生成细节丰富的负句子（ENS）以改善远OOD检测，同时仅对与测试数据相似的ID类子集生成视觉相似负标签（VSNL）以应对近OOD，并通过自适应加权分数动态融合二者，无需事先知道任务场景。
claims:
- 在ImageNet基准上，ANTS将远OOD的FPR95降低3.1%，近OOD的FPR95降低3.25%，建立新的最优结果。
- Table 1显示ANTS在ImageNet-1K OOD检测中取得平均AUROC 97.75和FPR95 11.20的最优性能。
- 消融实验（Table 4）验证了负图像挖掘（NIM）和视觉相似ID类挖掘（SIM）两个策略分别对远OOD和近OOD带来显著提升。
- Figure 1的t-SNE可视化表明，ENS比NegLabel和EOE更接近OOD图像特征，缩小了语义鸿沟。
---

# ANTS: Adaptive Negative Textual Space Shaping for OOD Detection via Test-Time MLLM Understanding and Reasoning

> [!tip] 核心洞察
> 利用多模态大语言模型在测试时对在线挖掘的负图像进行理解与推理，生成细节丰富的负句子（ENS）以改善远OOD检测，同时仅对与测试数据相似的ID类子集生成视觉相似负标签（VSNL）以应对近OOD，并通过自适应加权分数动态融合二者，无需事先知道任务场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | ANTS：基于测试时多模态大语言模型理解与推理的自适应负文本空间塑造用于开放环境分布外检测 |
| 英文题名 | ANTS: Adaptive Negative Textual Space Shaping for OOD Detection via Test-Time MLLM Understanding and Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.03951) · [Code](https://github.com/ZhuWenjie98/ANTS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ANTS (Adaptive Negative Textual Space Shaping) |
| Dataset | ImageNet-1K, OpenOOD, CUB-200-2011 |

> [!tip] 效果简介
> - ImageNet-1K (远OOD平均) 上，FPR95 相对先前最优结果降低 3.1% vs 先前最优 (NegLabel/EOE 等) (-3.1%)。
> - ImageNet-1K (近OOD) 上，FPR95 相对先前最优结果降低 3.25% vs 先前最优 (EOE 等) (-3.25%)。
> - ImageNet-1K (平均 6 个OOD数据集) 上，AUROC ↑ / FPR95 ↓ 97.75 / 11.20 vs NegLabel (96.45 / 14.30) 等 (AUROC +1.30 / FPR95 -3.10)。

## 概要

开放环境下的分布外（OOD）检测要求模型在测试时准确区分已知类别（ID）与未知类别（OOD）样本。现有基于负标签的零样本方法，如 **NegLabel**（Jiang et al., arXiv 2024）和 **EOE**（Dai et al., arXiv 2023），虽避免了传统方法对异常数据的依赖，却面临一个核心瓶颈：它们缺乏对 OOD 图像的实际理解，难以构建精确的负文本空间。具体而言，这些方法通过语料库距离或大语言模型提示生成的负标签，往往与真实 OOD 图像存在显著的语义鸿沟；在近 OOD 场景中，因忽略 ID 类子集的视觉相似性而产生大量假阴性标签；同时，它们依赖预先知道任务场景（远 OOD 或近 OOD）的强假设，无法适应动态变化的开放环境。

针对上述问题，本文提出 **ANTS（Adaptive Negative Textual Space Shaping）**，一种基于测试时多模态大语言模型（MLLM）理解与推理的自适应负文本空间塑造方法。其核心洞察在于：利用 MLLM 在测试时对在线挖掘的负图像进行理解与推理，生成细节丰富的**表达丰富负句子（ENS）** 以改善远 OOD 检测；同时，仅对与测试数据相似的 ID 类子集生成**视觉相似负标签（VSNL）** 以应对近 OOD 场景；并通过自适应加权分数动态融合二者，无需事先知道任务场景。

在 ImageNet-1K 基准上，ANTS 将远 OOD 的 FPR95 降低 3.1%，近 OOD 的 FPR95 降低 3.25%，建立了新的最优结果。整体平均 AUROC 达到 97.75，FPR95 降至 11.20（Table 1）。在 OpenOOD 零样本基准上，ANTS 同样显著优于 NegLabel 等方法，近 OOD 和远 OOD 的 FPR95 分别降低 7.38 和 2.10（Table 2）。消融实验（Table 4）验证了负图像挖掘（NIM）和视觉相似 ID 类挖掘（SIM）两个策略分别对远 OOD 和近 OOD 带来的显著提升。t-SNE 可视化（Figure 1）进一步表明，ENS 的文本特征比 NegLabel 和 EOE 更接近 OOD 图像特征，有效缩小了语义鸿沟。

该方法完全训练无关（training-free）且零样本，不引入可学习参数，仅利用历史测试图像进行在线挖掘，推理延迟为 2.84 ms/图像（GeForce RTX 3090），与同类方法可比。

### 开放环境中的分布外检测

将大规模预训练视觉-语言模型（如 CLIP）部署于开放环境时，系统必须可靠地区分分布内（ID）样本与分布外（OOD）样本，以保障安全决策。零样本 OOD 检测因其无需额外训练即可泛化至未知类别的能力而备受关注，其核心挑战在于构建一个能够精确刻画“非 ID”语义的**负文本空间**——即一组代表 OOD 概念的文本表征，用于与测试图像特征进行对比评分。

### 现有负标签方法的瓶颈

当前主流的零样本 OOD 检测方法通过构造负标签来近似 OOD 语义，但存在三个结构性缺陷：

**缺乏对 OOD 图像的实际理解。** **NegLabel**（Jiang et al., arXiv 2024）从外部语料库中基于余弦距离挖掘负标签，**EOE**（Dai et al., arXiv 2023）则利用纯文本 LLM 生成负标签。然而，这两种方法均未“看见”真实的 OOD 图像，导致生成的文本特征与 OOD 图像特征之间存在显著的语义鸿沟。如 Figure 1 的 t-SNE 可视化所示，NegLabel 和 EOE 的文本特征距离 OOD 图像特征较远，而 ANTS 利用 MLLM 对 OOD 图像进行理解后生成的负句子，其文本特征与 OOD 图像特征的距离显著缩小。

**近 OOD 场景中产生大量假阴性标签。** 近 OOD 样本与某些 ID 类在视觉上高度相似，若为所有 ID 类统一生成视觉相似负标签（如 EOE 的做法），大量与当前测试图像无关的 ID 类会被错误标记为“负”，导致假阴性标签泛滥，严重损害近 OOD 检测性能。Figure 6(a) 揭示了这一现象：仅对与测试数据真正相似的 ID 类子集生成负标签，才能有效抑制假阴性。

**依赖预先知道任务场景的强假设。** 现有方法通常为远 OOD 和近 OOD 设计固定的评分策略，隐含假设部署前已知晓任务类型。然而，在动态开放环境中，测试数据可能同时包含远 OOD 和近 OOD 样本，且比例未知。Figure 6(b) 表明不同 OOD 数据集偏好不同的决策阈值，固定策略无法自适应调整。

### 核心动机：测试时 MLLM 理解与推理

上述瓶颈的共性根源在于**负文本空间的质量与适应性不足**——既缺乏对实际 OOD 分布的准确刻画，也无法自适应地处理远 OOD 与近 OOD 的差异性。ANTS 的核心洞察是：多模态大语言模型（MLLM）在测试时具备对图像进行理解与推理的能力（Figure 2），可以将其引入 OOD 检测流程，通过“看见”历史测试图像来构建更精确、更具表达力的负文本空间，并依据数据特性动态调整检测策略，从而在无需先验场景知识的条件下，同时提升远 OOD 和近 OOD 的检测性能。

## 核心方法与创新机理

### 问题瓶颈与因果抓手

现有基于负标签的零样本OOD检测方法面临一个根本性瓶颈：**负文本空间的质量与适应性不足**。以**NegLabel**（Jiang et al., arXiv 2024）和**EOE**（Dai et al., arXiv 2023）为代表的现有方法，其负标签要么通过语料库余弦距离筛选，要么通过LLM提示生成，两者均缺乏对OOD图像的实际理解，导致负文本特征与真实OOD图像特征之间存在显著的语义鸿沟（见Figure 1的t-SNE可视化）。在近OOD场景中，这一问题进一步加剧——现有方法为所有ID类生成视觉相似标签（EOE）或完全忽略视觉相似性（NegLabel），产生大量假阴性标签，严重损害检测性能。此外，现有方法依赖预先知道任务场景（远OOD或近OOD）的强假设，无法适应动态开放环境。

ANTS的核心洞察在于：**利用多模态大语言模型在测试时对在线挖掘的负图像进行理解与推理**，从根本上提升负文本空间的质量与适应性。这一洞察将因果抓手锁定在“负文本空间的构建方式”上——从“语料库/提示驱动的静态生成”转变为“图像理解驱动的动态塑造”。

### 关键创新点（Changed Slots）

**创新一：从负标签到表达丰富负句子（ENS）**

现有方法生成的负标签是孤立的单词或短语（如“texture”、“abstract art”），缺乏对OOD图像细粒度视觉细节的刻画。ANTS引入**表达丰富负句子**（Expressive Negative Sentences, ENS）：向MLLM提供挖掘出的负图像，生成包含颜色、纹理、形状、场景等多维度细节的描述性负句子。例如，对于一张OOD纹理图像，ENS可能生成“a close-up of woven fabric with crisscrossing threads in beige and brown tones”这样的句子，而非简单的“texture”标签。这一转变使负文本特征在语义空间中更接近OOD图像特征（Figure 1验证了ENS特征与OOD图像特征的距离显著小于NegLabel和EOE），从而提升远OOD检测能力。

ENS的生成公式为：

$$\mathcal{V}_{ens}^{-} = \mathcal{G}_{ens}(\mathcal{V}, \mathcal{X}_{neg}, f_{mllm}, M)$$

其中 $\mathcal{X}_{neg}$ 为挖掘的负图像集合，$f_{mllm}$ 为MLLM，$M$ 为生成的负句子数量。基于ENS的OOD评分函数为：

$$S_{ens}(v) = \frac{\sum_{y \in \mathcal{Y}} e^{\cos(v, t)/\tau}}{\sum_{y \in \mathcal{Y}} e^{\cos(v, t)/\tau} + \sum_{y^{-} \in \mathcal{Y}_{ens}^{-}} e^{\cos(v, t^{-})/\tau}}$$

**创新二：视觉相似ID类子集挖掘与VSNL生成**

针对近OOD检测中的假阴性标签问题，ANTS提出**视觉相似负标签**（Visually Similar Negative Labels, VSNL）。与EOE为所有ID类生成视觉相似标签不同，ANTS仅对与历史测试图像最相似的ID类子集 $\mathcal{V}'$ 生成VSNL，从而大幅减少假阴性标签（Figure 6a展示了这一策略的效果）。VSNL的生成公式为：

$$\mathcal{V}_{vsnl}^{-} = \mathcal{G}_{vsnl}(\mathcal{V}', \mathcal{X}_{test}^{his}, f_{mllm}, M)$$

基于VSNL的OOD评分函数为：

$$S_{vsnl}(v) = \frac{\sum_{y \in \mathcal{V}} e^{\cos(v, t)/\tau}}{\sum_{y \in \mathcal{V}} e^{\cos(v, t)/\tau} + \sum_{y^{-} \in \mathcal{V}_{vsnl}^{-}} e^{\cos(v, \widehat{t}^{-})/\tau}}$$

**创新三：自适应加权评分融合**

ENS擅长远OOD检测（负句子与OOD图像语义距离近），VSNL擅长近OOD检测（视觉相似标签区分细粒度差异），二者在远/近OOD场景中表现互补（Figure 6c）。ANTS通过自适应加权分数动态融合二者，无需预先知道任务场景：

$$S_{ada}(\pmb{v}) = \lambda S_{ens}(\pmb{v}) + (1 - \lambda) S_{vsnl}(\pmb{v})$$

权重 $\lambda$ 由负图像上ENS和VSNL分数的平均值动态计算：

$$\lambda = F\left( \frac{1}{|\mathcal{X}_{neg}|} \sum_{\pmb{v} \in \mathcal{X}_{neg}} S_{ens}(\pmb{v}), \frac{1}{|\mathcal{X}_{neg}|} \sum_{\pmb{v} \in \mathcal{X}_{neg}} S_{vsnl}(\pmb{v}) \right)$$

其中 $F(a,b) = \frac{1-a}{(1-a)+(1-b)}$。当负图像上ENS分数较低（表明当前场景偏向远OOD）时，$\lambda$ 趋近于1，ENS主导评分；反之，当VSNL分数较低（表明当前场景偏向近OOD）时，$\lambda$ 趋近于0，VSNL主导评分。

**创新四：自适应负图像挖掘阈值**

传统方法使用固定的手动阈值 $\gamma$ 判定负图像，无法适应不同OOD数据集的分布差异（Figure 6b显示不同数据集偏好不同阈值）。ANTS通过基于历史测试数据分布的自适应阈值 $\gamma^*$ 解决此问题：选择分数最低的 $\eta$ 比例样本作为负图像，以该集合中最大分数作为动态阈值。

### 与基线方法的本质差异

| 维度 | NegLabel / EOE / CLIPN | **ANTS** |
|------|------------------------|----------|
| 负文本来源 | 语料库/LLM提示 | **MLLM对真实OOD图像的理解与描述** |
| 负文本粒度 | 孤立标签词 | **细节丰富的描述性句子** |
| 近OOD处理 | 全量ID类生成/完全忽略 | **仅对相似ID类子集生成VSNL** |
| 场景适应性 | 固定权重，需预知场景 | **自适应加权融合，无需预知** |
| 判定阈值 | 固定手动阈值 | **基于历史分布的动态阈值** |

这些创新使ANTS在ImageNet-1K基准上将远OOD的FPR95降低3.1%、近OOD的FPR95降低3.25%（相对先前最优结果），建立了新的最优性能（Table 1：平均AUROC 97.75, FPR95 11.20）。消融实验（Table 4）进一步验证了负图像挖掘（NIM）和视觉相似ID类挖掘（SIM）两个策略分别对远OOD和近OOD带来的显著提升。

ANTS 采用**三阶段流水线**，在测试时逐步塑造自适应负文本空间，无需任何离线训练或辅助异常数据。整体框架如图 3 所示，三个阶段分别为：

1.  **历史测试图像缓存与挖掘**：从历史测试图像中自适应挖掘**负图像**（可能为 OOD 的样本）和**视觉相似 ID 类子集**（与测试图像最相似的 ID 类别），为后续负空间塑造提供数据基础。
2.  **双负文本空间塑造**：利用多模态大语言模型（MLLM）对缓存的负图像和 ID 类子集进行**测试时理解与推理**，分别生成**表达丰富负句子（ENS）**和**视觉相似负标签（VSNL）**，构建两个互补的负文本空间。
3.  **自适应加权在线评估**：对每个测试图像，分别计算基于 ENS 和 VSNL 的 OOD 分数，并通过**自适应权重 λ** 动态融合二者，输出最终 OOD 评分 $S_{ada}$。

三个阶段的因果链条清晰：**负图像挖掘**决定了 ENS 的语义质量，**视觉相似 ID 类挖掘**控制了 VSNL 的假阴性风险，而**自适应加权**则使系统无需预先知道测试场景（远 OOD 或近 OOD）即可自动平衡两类分数的贡献。该设计直击核心瓶颈——负文本空间的质量与适应性决定了 OOD 检测的上限，而 ANTS 通过 MLLM 的测试时理解能力与数据驱动的自适应机制，将这一瓶颈转化为可控的因果旋钮。

### 数据流与模块依赖

- **输入**：测试图像流 $\mathcal{X}_{test}$，ID 类标签集 $\mathcal{V}$，预训练 CLIP 编码器 $f_{clip}$，MLLM $f_{mllm}$。
- **阶段一输出**：负图像集 $\mathcal{X}_{neg}$（通过 NegLabel 初始检测器 $S_{nl}$ 与自适应阈值 $\gamma^*$ 筛选），视觉相似 ID 类子集 $\mathcal{V}'$（通过特征相似度排序选取）。
- **阶段二输出**：ENS 负标签集 $\mathcal{V}_{ens}^{-}$（由 $f_{mllm}$ 对 $\mathcal{X}_{neg}$ 描述生成），VSNL 负标签集 $\mathcal{V}_{vsnl}^{-}$（由 $f_{mllm}$ 对 $\mathcal{V}'$ 与测试图像联合推理生成）。
- **阶段三输出**：自适应融合分数 $S_{ada}(v) = \lambda S_{ens}(v) + (1-\lambda) S_{vsnl}(v)$，其中 $\lambda$ 由负图像上两类分数的均值动态计算：$\lambda = F(\bar{S}_{ens}, \bar{S}_{vsnl})$，$F(a,b) = (1-a)/((1-a)+(1-b))$。

### 关键设计选择

| 设计要素 | 基线做法 | ANTS 做法 | 因果作用 |
|---------|---------|----------|---------|
| 负空间构建 | 语料库距离或 LLM 提示生成负标签 | MLLM 对挖掘的负图像进行描述，生成细节丰富的负句子 | 缩小负文本与 OOD 图像特征的语义鸿沟（图 1 证据） |
| 近 OOD 负标签 | 为所有 ID 类生成视觉相似标签（EOE）或完全忽略（NegLabel） | 仅对与测试图像最相似的 ID 类子集生成 VSNL | 大幅减少假阴性标签（图 6a 证据） |
| 评分融合 | 固定权重或单一分数 | 自适应权重 λ，由测试数据动态计算 | 自动适应远/近 OOD 场景（图 6c 证据） |
| 负图像阈值 | 手动固定阈值 γ | 基于历史数据分布的自适应阈值 $\gamma^*$ | 隐式实现数据集自适应阈值（图 6b 证据） |

### 方法谱系与知识库定位

ANTS 处于**零样本 OOD 检测**与**多模态大模型推理**的交叉点，其核心创新在于将 MLLM 的测试时理解能力引入负文本空间塑造。与现有工作的关系如下：

- **NegLabel**（Jiang et al., arXiv 2024）：ANTS 继承了其基于语料库余弦距离的负标签选择机制作为初始检测器 $S_{nl}$，但通过 ENS 的 MLLM 描述能力克服了其对 OOD 图像缺乏理解的缺陷。
- **EOE**（Dai et al., arXiv 2023）：ANTS 借鉴了利用 LLM 生成负标签的思路，但针对 EOE 为所有 ID 类生成视觉相似标签导致假阴性的问题，引入了选择性 ID 类挖掘策略。
- **CLIPN**（Wang et al., ICCV 2023）与 **AdaNeg**（Zhang & Zhang, NeurIPS 2024）：同为负文本空间方法，但 ANTS 不引入可学习参数，完全依赖测试时 MLLM 推理，保持了零样本与训练无关的特性。
- **MCM**（Ming et al., NeurIPS 2022）：基于视觉-语言表示的基线方法，ANTS 在其基础上通过负文本空间塑造实现了显著的性能提升。

> **注意**：以上基线引用信息来自分析 JSON，建议在正式撰写时核实原始文献的确切发表信息。

### 补充图表

![[assets/figures/papers/paper_list_l2044_https_arxiv_org_abs_2509_03951/figures/003_Figure_3.jpg]]
*Figure 3: The overall framework of our ANTS. ANTS framework consists of in three stages: (1) caching negative images and visually similar ID classes mined from historical test images; (2) shaping two negative textual spaces by prompting an MLLM with the cached data to generate expressive negative sentences and visually similar labels; and (3) performing online evaluation of the test image using an adaptively weighted combination of these textual spaces*

ANTS 方法通过三阶段流水线构建自适应负文本空间（图3）：(1) 从历史测试图像中挖掘负图像与视觉相似 ID 类并缓存；(2) 利用 MLLM 对缓存数据生成两类负文本空间——表达丰富负句子（ENS）与视觉相似负标签（VSNL）；(3) 通过自适应加权分数在线评估测试图像。以下详述核心模块及其数学形式。

---

### 1. 负图像挖掘与自适应阈值

负图像挖掘模块旨在从历史测试图像 $\mathcal{X}_{test}^{his}$ 中筛选出可能为 OOD 的样本，为后续 MLLM 理解 OOD 图像提供素材。首先利用 NegLabel 的 OOD 检测器计算每张历史图像的分数 $S_{nl}(\mathbf{x})$，以初始阈值 $\gamma$ 筛选候选集：

$$\mathcal{X}_{neg} = \{ \mathbf{x} \mid S_{nl}(\mathbf{x}) < \gamma, \mathbf{x} \in \mathcal{X}_{test}^{his} \} \tag{5}$$

其中 $S_{nl}$ 基于负标签的 OOD 评分函数：

$$S_{nl}(v) = \frac{\sum_{y \in \mathcal{V}} e^{\cos(v, t)/\tau}}{\sum_{y \in \mathcal{V}} e^{\cos(v, t)/\tau} + \sum_{y^{-} \in \mathcal{V}_{nl}^{-}} e^{\cos(v, t^{-})/\tau}}$$

然而，固定阈值 $\gamma$ 难以适应不同 OOD 数据集的分布差异（图6b）。为此，ANTS 引入自适应阈值策略：从候选集中选取分数最低的 $\eta$ 比例样本作为最终负图像集，并以其中最大分数作为自适应阈值 $\gamma^*$：

$$\mathcal{X}_{neg} = \text{Top}(\hat{\mathcal{X}}_{neg}, O_{nl}, \eta), \quad \gamma^* = \max_{\mathbf{x} \in \mathcal{X}_{neg}} S_{nl}(\mathbf{x}) \tag{6}$$

其中 $O_{nl}$ 表示 $S_{nl}$ 分数升序排列。这一机制使阈值隐式地随测试数据分布动态调整。

---

### 2. 表达丰富负句子生成

获得负图像后，ANTS 利用 MLLM 对 OOD 图像进行测试时理解与推理，生成细节丰富的负句子。生成函数形式化定义为：

$$\mathcal{V}_{ens}^{-} = \mathcal{G}_{ens}(\mathcal{V}, \mathcal{X}_{neg}, f_{mllm}, M) \tag{7}$$

其中 $\mathcal{V}$ 为 ID 标签集，$\mathcal{X}_{neg}$ 为挖掘的负图像集，$f_{mllm}$ 为多模态大语言模型，$M$ 为生成的负句子数量。MLLM 通过描述负图像的内容、纹理、场景等细粒度特征，生成表达力远强于简单负标签的文本（图4）。这些负句子构成 ENS 负文本空间，专门用于远 OOD 检测。

基于 ENS 的 OOD 分数定义为：

$$S_{ens}(v) = \frac{\sum_{y \in \mathcal{Y}} e^{\cos(v, t)/\tau}}{\sum_{y \in \mathcal{Y}} e^{\cos(v, t)/\tau} + \sum_{y^{-} \in \mathcal{Y}_{ens}^{-}} e^{\cos(v, t^{-})/\tau}} \tag{8}$$

其中 $v$ 为测试图像的 CLIP 视觉特征，$t$ 和 $t^{-}$ 分别为 ID 标签和 ENS 负句子的文本特征，$\tau$ 为温度系数。分数越低表明图像与负文本空间越接近，越可能为 OOD。

---

### 3. 视觉相似负标签生成

近 OOD 场景的核心挑战在于 OOD 图像与某些 ID 类高度相似，若为所有 ID 类生成视觉相似负标签会产生大量假阴性标签。ANTS 通过视觉相似 ID 类挖掘策略解决此问题：仅选择与历史测试图像最相似的 ID 类子集 $\mathcal{V}'$ 生成负标签。

具体而言，计算历史测试图像特征与各 ID 类文本特征的平均余弦相似度，选取相似度最高的 $K$ 个 ID 类：

$$\mathcal{V}' = \text{TopK}(\{ \frac{1}{|\mathcal{X}_{test}^{his}|} \sum_{\mathbf{x} \in \mathcal{X}_{test}^{his}} \cos(f_{clip}(\mathbf{x}), t_y) \mid y \in \mathcal{V} \}) \tag{10}$$

然后，向 MLLM 提供筛选后的 ID 类子集 $\mathcal{V}'$ 和测试图像，生成视觉相似负标签：

$$\mathcal{V}_{vsnl}^{-} = \mathcal{G}_{vsnl}(\mathcal{V}', \mathcal{X}_{test}^{his}, f_{mllm}, M) \tag{11}$$

基于 VSNL 的 OOD 分数为：

$$S_{vsnl}(v) = \frac{\sum_{y \in \mathcal{V}} e^{\cos(v, t)/\tau}}{\sum_{y \in \mathcal{V}} e^{\cos(v, t)/\tau} + \sum_{y^{-} \in \mathcal{V}_{vsnl}^{-}} e^{\cos(v, \widehat{t}^{-})/\tau}} \tag{12}$$

---

### 4. 自适应加权评分

ENS 和 VSNL 在不同 OOD 场景下表现互补：ENS 在远 OOD 上更有效，VSNL 在近 OOD 上更优（图6c）。ANTS 通过自适应权重 $\lambda$ 动态融合二者，无需事先知道任务场景：

$$S_{ada}(\pmb{v}) = \lambda S_{ens}(\pmb{v}) + (1 - \lambda) S_{vsnl}(\pmb{v}) \tag{13}$$

权重 $\lambda$ 由负图像集上两种分数的平均值决定：

$$\lambda = F\left( \frac{1}{|\mathcal{X}_{neg}|} \sum_{\pmb{v} \in \mathcal{X}_{neg}} S_{ens}(\pmb{v}), \frac{1}{|\mathcal{X}_{neg}|} \sum_{\pmb{v} \in \mathcal{X}_{neg}} S_{vsnl}(\pmb{v}) \right) \tag{14}$$

其中归一化函数 $F(a,b) = \frac{1-a}{(1-a)+(1-b)} \in (0,1)$。当负图像上 ENS 分数较低（表明为远 OOD）时，$\lambda$ 趋近于 1，ENS 主导决策；反之当 VSNL 分数较低时，$\lambda$ 趋近于 0，VSNL 主导决策。这一机制使 ANTS 能够自适应地应对远 OOD 与近 OOD 的混合场景。

### 补充图表

![[assets/figures/papers/paper_list_l2044_https_arxiv_org_abs_2509_03951/figures/001_Figure_1.jpg]]
*Figure 1: T-SNE visualization of the ID and OOD image features, the text features of NegLabel [19], EOE [4], OOD ground-truth, and the expressive negative sentences (ENS) of ANTS. We select ImageNet and SUN as the ID and OOD datasets, respectively. NegLabel and EOE lack a good understanding of OOD images, resulting in a greater distance between the OOD images and the text features. In contrast, our ANTS utilizes the MLLMs to understand OOD images during ENS generation, reducing the distance between ENS and OOD images and improving OOD detection performance*

## 实验与关键发现

### 主实验结果

ANTS 在多个标准 OOD 检测基准上一致地建立了新的最优性能。以 ImageNet-1K 作为 ID 数据集时，如表 1 所示，ANTS 在 6 个 OOD 测试集的平均 AUROC 达到 **97.75**，FPR95 降至 **11.20**，相较此前最优的 **NegLabel**（Jiang et al., arXiv 2024）分别提升 +1.30 和降低 -3.10。在更具挑战性的近 OOD 场景中，ANTS 将 FPR95 相对先前最优结果降低 **3.25%**；在远 OOD 场景中降低 **3.1%**，验证了方法对两类 OOD 分布的同时适配能力。

在 OpenOOD 零样本基准上（表 2），ANTS 同样表现突出：近 OOD 的 FPR95 为 **60.98**（NegLabel 为 68.36），远 OOD 的 FPR95 为 **15.38**（NegLabel 为 17.48），分别降低 7.38 和 2.10 个百分点。当 ID 数据集切换为 CUB-200-2011 等细粒度分类场景时（表 3），ANTS 仍保持显著优势，AUROC 达 **99.95**，FPR95 仅 **0.01**，表明方法对 ID 分布变化具有良好的泛化性。

> **关键证据强度**：Table 1 和 Table 2 提供了置信度 1.0 和 0.95 的量化结果，构成方法有效性的核心支撑。

![[assets/figures/papers/paper_list_l2044_https_arxiv_org_abs_2509_03951/figures/007_Table_1.jpg]]
*Table 1: OOD detection results by using ImageNet-1k as ID dataset. ViTB/16 is used as the encoder. The results of traditional methods are available in the supplementary materials*

![[assets/figures/papers/paper_list_l2044_https_arxiv_org_abs_2509_03951/figures/008_Table_2.jpg]]
*Table 2: OOD detection results of zero-shot methods on the OpenOOD benchmark. ImageNet-1k is adopted as ID dataset. Detailed results are available in the supplementary materials*

### 消融实验

为解耦各组件的贡献，论文设计了系统的消融实验（表 4）。设置 A 为仅使用 NegLabel 的基线。设置 B 引入表达丰富负句子（ENS），远 OOD 的 FPR95 立即从 NegLabel 的 48.87 降至 **43.87**，验证了 ENS 在远 OOD 检测上的独立有效性。进一步叠加负图像挖掘（NIM）和视觉相似 ID 类挖掘（SIM）后，完整 ANTS（设置 F）在近 OOD 和远 OOD 上均取得最佳性能，证实两个挖掘策略分别对各自目标场景的关键贡献。

自适应加权分数机制的消融分析（Figure 6c）揭示了 ENS 分数 $S_{ens}$ 和 VSNL 分数 $S_{vsnl}$ 的功能互补性：$S_{ens}$ 在远 OOD 上表现更强，$S_{vsnl}$ 在近 OOD 上更具判别力，为动态权重 $\lambda$ 的设计提供了经验依据。超参数分析（Figure 7）进一步表明，ANTS 对初始 OOD 检测器选择、负句子长度、选择比例 $\delta$ 和权重 $\lambda$ 均具有良好的鲁棒性，且在不同 CLIP 图像编码器和 MLLM 模型下表现稳定。

![[assets/figures/papers/paper_list_l2044_https_arxiv_org_abs_2509_03951/figures/011_Figure_7.jpg]]
*Figure 7: Analysis on (a) different initial OOD detectors, (b) the lengths of negative sentences, (c) selection ratio δ, (d) weight λ, (e) CLIP image encoder backbones, (f) MLLMs prompts, and (g) different MLLMs. (h) Temporal shift. We use Texture [6] and NINCO [3] datasets as Far-OOD and Near-OOD, respectively*

> **关键证据强度**：Table 4 的消融结果置信度为 0.95，Figure 6c 的互补性分析置信度为 0.9，共同构成组件有效性的强证据链。

![[assets/figures/papers/paper_list_l2044_https_arxiv_org_abs_2509_03951/figures/009_Table_4.jpg]]
*Table 4: Ablation experiments. ‘NIM’ indicates the Negative Image Mining strategy in Eq. 6, and ‘SIM’ means the Visually Similar ID-Classes Mining strategy in Eq. 10*

### 效率与复杂度分析

ANTS 在保持高性能的同时，推理效率与同类方法可比。如表 5 和表 6 所示，在 GeForce RTX 3090 上单张图像的推理延迟为 **2.84 ms**，且方法不引入任何可学习参数，参数量与基础 CLIP 模型完全相同。主要计算开销来自 MLLM 的文本生成，但由于负句子和负标签的生成可在线缓存并复用，实际测试时仅需执行轻量的文本-图像余弦相似度计算。

### 失败模式与局限性

尽管 ANTS 在多数场景下表现优异，但其性能依赖于 MLLM 的推理质量。当 MLLM 对负图像的理解出现偏差时，生成的 ENS 或 VSNL 可能无法准确刻画 OOD 分布，从而影响负空间构建的精度。此外，自适应阈值 $\gamma^*$ 和权重 $\lambda$ 的计算依赖于历史测试数据的统计特性，在测试数据分布发生剧烈突变时，自适应机制的响应速度可能滞后，需要进一步研究其鲁棒性边界。论文未报告在极端小批量或在线流式场景下的退化程度，该点需在实际部署中手动验证。

## 定位与知识库关联

### 核心瓶颈与因果杠杆

现有基于负标签的零样本OOD检测方法面临一个根本性瓶颈：**负文本空间的质量与适应性不足**。具体而言，**NegLabel**（Jiang et al., arXiv 2024）通过语料库余弦距离筛选负标签，**EOE**（Dai et al., arXiv 2023）利用LLM提示生成负标签，但二者均缺乏对OOD图像的实际理解，难以构建精确的负空间。在近OOD场景中，这些方法或为所有ID类生成视觉相似标签（EOE），或完全忽略视觉相似性（NegLabel），导致大量假阴性标签。更关键的是，它们依赖预先知道任务场景（远/近OOD）的强假设，无法适应动态开放环境。

ANTS的核心洞察在于：**利用多模态大语言模型（MLLM）在测试时对在线挖掘的负图像进行理解与推理**，生成细节丰富的负句子（ENS）以改善远OOD检测，同时仅对与测试数据相似的ID类子集生成视觉相似负标签（VSNL）以应对近OOD，并通过自适应加权分数动态融合二者，无需事先知道任务场景。

### 方法谱系中的位置

ANTS属于**零样本、训练无关的视觉-语言OOD检测方法**，其谱系可追溯至以下关键节点：

- **MCM**（Ming et al., NeurIPS 2022）：开创性地利用CLIP视觉-语言表示进行零样本OOD检测，通过最大概念匹配分数区分ID/OOD，建立了基于softmax分数的基线范式。
- **CLIPN**（Wang et al., ICCV 2023）：通过训练让CLIP学会说“不”，引入可学习的负文本编码器，但需要额外训练且不零样本。
- **NegLabel**（Jiang et al., arXiv 2024）：从大规模语料库中挖掘与ID标签余弦距离大的负标签，无需训练，但负标签缺乏对OOD图像的理解。
- **EOE**（Dai et al., arXiv 2023）：利用LLM为每个ID类生成视觉相似负标签以应对近OOD，但为所有ID类生成标签导致假阴性，且远OOD能力有限。
- **AdaNeg**（Zhang & Zhang, NeurIPS 2024）：引入自适应负代理引导，但本质上仍依赖固定策略。

ANTS在NegLabel和EOE的基础上实现了关键跃迁：将负空间构建从“语料库/LLM驱动的静态标签生成”提升为“**MLLM测试时理解驱动的动态负空间塑造**”。这一跃迁体现在四个变更槽位：

| 变更槽位 | 基线值 | ANTS方案 |
|---------|--------|---------|
| 负文本空间构建 | 语料库余弦距离或LLM提示生成，缺乏对OOD图像的理解 | MLLM对挖掘的负图像进行描述，生成表达力丰富的负句子（ENS） |
| 近OOD负标签生成 | 为所有ID类生成（EOE）或完全忽略（NegLabel） | 仅对与历史测试图像最相似的ID类子集生成视觉相似负标签（VSNL） |
| 评分函数 | 固定权重或单一负标签评分 | 自适应加权分数 $S_{ada} = \lambda S_{ens} + (1-\lambda) S_{vsnl}$ |
| 负图像判定阈值 | 手动设置的固定阈值 $\gamma$ | 基于历史测试数据分布的动态自适应阈值 $\gamma^*$ |

### 知识库定位与适用边界

**适用场景**：
- 零样本OOD检测，无需任何辅助异常数据或模型训练
- 同时处理远OOD（语义差异大）和近OOD（语义相近但类别不同）场景
- 动态开放环境，无需预先知道测试数据的OOD类型

**不适用/需谨慎的场景**：
- MLLM推理能力不足时（如低质量开源MLLM），负空间构建质量可能下降
- 极端数据分布突变下，自适应机制依赖的历史统计特性可能失效
- 对实时性要求极高的边缘设备，MLLM调用和缓存管理仍有开销

**与其他方法的互补性**：
- ANTS可与更强的CLIP编码器（如ViT-L/14）组合使用，性能可进一步提升
- 负图像挖掘依赖NegLabel作为初始检测器，理论上可替换为其他零样本检测器
- 框架的MLLM组件可替换为更强的模型（如LLaVA-1.6），以提升理解质量

### 局限与开放问题

**已识别的局限**（来自论文分析）：
1. **MLLM依赖性**：方法依赖MLLM的推理质量，若MLLM理解能力不足可能影响负空间构建。Figure 7(g)显示不同MLLM对性能有显著影响。
2. **计算与存储开销**：历史测试图像的缓存和在线挖掘需要一定的存储与计算开销。Table 5显示在GeForce RTX 3090上推理延迟为2.84 ms/图像，与同类方法可比但仍有优化空间。
3. **自适应鲁棒性**：自适应机制依赖于测试数据的统计特性，在极端数据分布突变下可能需要进一步鲁棒性研究。

**开放问题**（来自论文分析与推导）：
1. **MLLM效率优化**：如何更高效地利用MLLM降低测试时开销？例如通过缓存常见OOD模式或压缩提示，减少重复调用。
2. **框架泛化性**：ANTS框架在其他视觉任务（如语义分割、目标检测）的开放世界识别中是否有效？当前仅验证了图像分类OOD检测。
3. **自监督负图像挖掘**：能否进一步减少对NegLabel初始检测器的依赖，实现完全自监督的负图像挖掘？这将使框架更加独立和鲁棒。
4. **时序动态建模**：当前方法基于历史测试数据的简单缓存，未显式建模数据分布的时序变化。引入时序衰减或在线学习机制可能进一步提升自适应能力。

**证据强度说明**：上述局限和开放问题中，MLLM依赖性和计算开销有明确的实验支撑（Figure 7、Table 5-6），自适应鲁棒性和框架泛化性目前仅为合理推断，需进一步实验验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/ANTS_Adaptive_Negative_Textual_Space_Shaping_for_OOD_Detection_via_Test_Time_MLLM_Understanding_and_Reasoning.pdf]]

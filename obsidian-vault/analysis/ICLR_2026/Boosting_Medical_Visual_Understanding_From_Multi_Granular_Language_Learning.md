---
title: "Boosting Medical Visual Understanding From Multi-Granular Language Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Boosting_Medical_Visual_Understanding_From_Multi_Granular_Language_Learning.pdf
project_link: null
code_link: https://github.com/HUANGLIZI/MGLL
openreview_forum_id: ccjukmExrB
aliases:
- MGLLM
- BMVUFMGLL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "引入多粒度语言监督，通过软 CLIP 损失实现一对多标签的软对齐，并通过平滑 KL 散度损失强制不同粒度特征向共享均值分布收敛，从而同时完成多标签对齐与跨粒度一致性约束。"
primary_logic: "利用多粒度文本描述构建层次化监督信号，设计软标签对比损失与平滑 KL 散度，使视觉特征能够同时对齐多个相关标签且在不同粒度间保持语义一致，从而更全面、精细地捕捉医学图像中的病理信息。"
claims:
- "MGLL 在眼底多标签数据集 RFMiD 上线性探测 AUC 领先其他 SOTA 模型至少 16.6%。"
- "MGLL 在 ChestX-ray14 线性探测 AUC 达到 82.94%，超越次优方法 5.62%。"
- "MGLL 的 CAM 可视化能精确定位病灶区域（如硬性渗出、视网膜色素上皮），而 CLIP 仅产生弥散激活。"
- "消融实验证实三项损失（软 CLIP、逐点损失、平滑 KL）缺一不可，组合后达到最佳性能。"
---

# Boosting Medical Visual Understanding From Multi-Granular Language Learning

> [!tip] 核心洞察
> 利用多粒度文本描述构建层次化监督信号，设计软标签对比损失与平滑 KL 散度，使视觉特征能够同时对齐多个相关标签且在不同粒度间保持语义一致，从而更全面、精细地捕捉医学图像中的病理信息。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多粒度语言学习提升医学视觉理解 |
| 英文题名 | Boosting Medical Visual Understanding From Multi-Granular Language Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ccjukmExrB) · [GitHub](https://github.com/HUANGLIZI/MGLL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Multi-Granular Language Learning (MGLL) |
| Dataset | RFMiD (multi-label fundus), ChestX-ray14, MIDRC-XR |

> [!tip] 效果简介
> - RFMiD (multi-label fundus) 上，AUC (Linear Probe) 为 79.62，对比 44.66 (CLIP)，变化 +34.96。
> - ChestX-ray14 上，AUC (Linear Probe) 为 82.94，对比 77.32 (CARZero)，变化 +5.62。
> - MIDRC-XR 上，AUC (Linear Probe) 为 61.25，对比 59.02 (UniChest)，变化 +2.23。

## 概要

现有视觉-语言对比预训练方法（以 CLIP 为代表）仅支持单标签、单粒度对齐，无法有效利用医学图像天然关联的多层次文本描述（如疾病类别、临床解释、检查所见等），导致视觉特征难以同时区分粗粒度与细粒度类别。针对这一瓶颈，本文提出 **多粒度语言学习（Multi-Granular Language Learning, MGLL）** 框架，核心思路是通过多粒度文本监督构建层次化对比信号，并引入跨粒度一致性约束，使视觉编码器能够同时对齐多个相关标签且在不同语义层次间保持特征一致。

MGLL 的关键机制包含三个互补组件：**软 CLIP 损失**通过共现权重实现一对多标签的软对齐；**逐点损失**以二值交叉熵进行精细的成对图像-文本匹配；**平滑 KL 散度损失**强制不同粒度预测分布向共享均值收敛，完成跨粒度语义对齐。三者加权组合构成最终优化目标（Eq. 7），其中软 CLIP 损失与平滑 KL 散度损失的协同效应是性能提升的核心驱动力。

实验验证覆盖眼底图像与胸部 X 射线两大医学影像模态。在眼底多标签数据集 RFMiD 上，MGLL 线性探测 AUC 达到 79.62%，相较 CLIP 提升 34.96 个百分点，领先其他 SOTA 方法至少 16.6%；在 ChestX-ray14 上线性探测 AUC 达 82.94%，超越次优方法 CARZero 5.62 个百分点。消融实验证实，三项损失缺一不可，组合后达到最优性能；增加粒度数目持续提升表征质量；MGLL 对标签缺失具有显著鲁棒性——在 30% 粒度标签缺失时，线性探测 AUC 仍大幅超越完整标签训练的 CLIP。CAM 可视化进一步表明，MGLL 能精确定位病灶区域（如硬性渗出、视网膜色素上皮），而 CLIP 仅产生弥散激活。

MGLL 以即插即用模块形式作用于视觉-语言模型，保持计算效率的同时显著增强了医学视觉理解能力。



医学影像理解是临床诊断与治疗决策的核心环节。近年来，视觉-语言对比预训练方法（以 CLIP 为代表）在通用领域取得了显著成功，其核心思想是通过图像与对应文本描述的单标签对比学习，将视觉特征与语义信息对齐。然而，当这一范式迁移至医学领域时，一个根本性的瓶颈浮现：**医学图像天然与多个不同粒度的文本标签相关联**——例如，一张眼底照片可能同时对应“糖尿病视网膜病变”这一粗粒度疾病类别，以及“视网膜可见微动脉瘤、硬性渗出”等细粒度临床描述。现有的单标签、单粒度对齐策略无法有效利用这种层次化的文本监督信号，导致视觉特征在区分粗、细粒度类别时能力不足。

这一瓶颈在两类典型场景中尤为突出。其一，**多标签场景**：一张医学图像往往同时呈现多种病理表现（如眼底图像中可能共存糖尿病视网膜病变与黄斑水肿），标准 CLIP 损失仅将每张图像与单一文本标签配对，无法建模这种一对多的语义关联。其二，**跨粒度一致性**：即使将不同粒度的文本描述分别编码，若缺乏显式约束，模型在不同粒度上学到的语义表征可能相互矛盾——粗粒度标签指向某一大类疾病，而细粒度描述却可能更关注某一亚型的特征，二者在特征空间中缺乏统一的语义锚点。

为应对上述挑战，本文提出 **多粒度语言学习（Multi-Granular Language Learning, MGLL）**，其核心动机可概括为三点：

1. **从单标签到多标签的软对齐**：通过引入基于共现权重的软 CLIP 损失，使每张图像能够同时与多个相关文本标签建立对比关系，而非强制选择唯一匹配项。
2. **从单粒度到多粒度的层次化监督**：利用不同粒度的文本描述（如疾病类别、检查描述、序列描述）构建层次化监督信号，使视觉特征能够同时捕捉从粗到细的病理信息。
3. **跨粒度语义一致性约束**：通过平滑 KL 散度损失，强制不同粒度文本特征向共享的均值分布收敛，确保模型在不同抽象层次上保持语义一致，避免表征冲突。

MGLL 的设计遵循“即插即用”原则，可作为视觉-语言模型的通用预训练模块嵌入现有框架，在保持计算效率的同时显著提升医学视觉理解的多标签处理能力与跨粒度语义一致性。



## 核心方法与创新机理

MGLL 的核心创新在于将传统视觉‑语言预训练中“单图像‑单标签”的对齐范式，重构为**多粒度、多标签的软对齐与跨粒度一致性联合约束**。这一转变由三个相互关联的 changed slots 支撑，分别对应损失函数组合、多标签对齐机制和跨粒度一致性约束。

### 从硬对齐到软多标签对齐

标准 CLIP 损失（Eq. 8）强制每张图像仅与一个文本标签形成互信息最大化，这在医学场景中构成根本性瓶颈：一张眼底图像可能同时携带“糖尿病视网膜病变”“硬性渗出”“黄斑水肿”等多个不同粒度的诊断标签，单标签对齐迫使模型丢弃大量层次化语义信息。

MGLL 通过**软 CLIP 损失**（$\mathcal{L}_{\mathrm{sCLIP}}$，Eqs. 1‑2）将这一硬约束松弛为一对多的软对齐。具体而言，每对图像‑文本标签的对比损失 $l_{ik}$ 由共现权重 $w_{ik}$ 加权（Eq. 3），该权重从图像与标签的共现矩阵归一化得到，使得模型能够根据标签在数据中的真实共现强度，自适应地分配对齐强度。这一机制直接解决了医学图像多标签特性与对比学习单正样本假设之间的结构冲突。

### 跨粒度一致性约束

仅有多标签对齐仍不足以充分利用多粒度文本的层次化结构——不同粒度的文本描述（如模态描述、检查描述、序列描述）可能对同一图像产生不一致的语义表征。MGLL 引入**平滑 KL 散度损失**（$\mathcal{L}_{\mathrm{sKL}}$，Eqs. 5‑6）作为跨粒度正则项：首先计算各粒度预测分布 $P_i$ 与共享均值分布 $M$ 的 KL 散度（Eq. 5），然后对所有粒度求和（Eq. 6），强制不同粒度的特征向共享语义中心收敛。这一约束确保了视觉编码器在不同抽象层次上提取的特征保持语义一致，避免因粒度间表征漂移导致的判别力下降。

### 损失函数的协同设计

三项损失以加权和形式组合为最终优化目标（Eq. 7）：

$$\mathcal{L}_{\mathrm{MGLL}} = \alpha_{1} \mathcal{L}_{\mathrm{sCLIP}} + \alpha_{2} \mathcal{L}_{\mathrm{P}} + \alpha_{3} \mathcal{L}_{\mathrm{sKL}}$$

其中 $\mathcal{L}_{\mathrm{sCLIP}}$ 提供宏观的多标签对比监督，$\mathcal{L}_{\mathrm{P}}$（逐点损失，Eq. 4）以二值交叉熵形式实现细粒度的成对图像‑文本对齐，$\mathcal{L}_{\mathrm{sKL}}$ 则作为跨粒度一致性正则项。消融实验（Table 3）证实三者缺一不可：单独使用 $\mathcal{L}_{\mathrm{sCLIP}}$ 或 $\mathcal{L}_{\mathrm{P}}$ 均无法达到最优性能，而加入 $\mathcal{L}_{\mathrm{sKL}}$ 后性能进一步提升，表明跨粒度一致性约束与多标签对齐之间存在互补效应——前者稳定了多粒度特征空间的结构，后者在此基础上实现了更精细的语义对齐。

### 与 baseline 的本质差异

相较于 CLIP 的单标签对比损失、CheXzero 的语义匹配策略或 MRM 的多标签对比学习，MGLL 的关键差异在于同时解决了两个耦合问题：**多标签对齐**（通过软 CLIP 损失和逐点损失）与**跨粒度一致性**（通过平滑 KL 散度）。这一联合优化使得视觉特征既能捕捉粗粒度类别信息，又能保留细粒度病理细节，在眼底多标签数据集 RFMiD 上线性探测 AUC 领先 CLIP 达 +34.96%，在 ChestX‑ray14 上领先次优方法 CARZero 达 +5.62%。



![[assets/figures/papers/iclr26_0011_ccjukmExrB_Boosting_Medical_Visual_Understanding_From_Multi/figures/002_Figure_2.jpg]]
*Figure 2: The overview of MGLL (Multi-Granular Language Learning) pretraining pipeline*

MGLL 的整体预训练流水线围绕一个核心矛盾展开：医学图像天然关联多个不同粒度的文本标签（如疾病类别、临床描述、序列说明），而标准 CLIP 式对比学习仅支持单标签、单粒度对齐，导致视觉编码器无法充分利用层次化文本信息。MGLL 通过引入多粒度语言监督，将这一问题转化为三个互补的优化目标——多标签软对齐、细粒度逐点对齐、跨粒度一致性约束——从而在统一的视觉-语言框架内实现更全面的病理特征学习。

### 输入与编码

流水线接受两类输入：医学图像及其对应的多粒度文本描述。图像侧采用 **ViT‑L/14** 作为视觉编码器，文本侧采用 **BiomedicalBERT** 作为文本编码器，二者分别将图像和文本投影到共享的嵌入空间。多粒度文本描述以层级形式组织——例如在 X 射线数据中，三个粒度分别为模态标签（modality）、检查描述（study description）和序列描述（series description）——每张图像可关联多个粒度下的多个标签。

### 核心模块与数据流

MGLL 的优化由三个损失模块协同驱动，其整体目标函数为：

$$
\mathcal{L}_{\mathrm{MGLL}} = \alpha_{1} \mathcal{L}_{\mathrm{sCLIP}} + \alpha_{2} \mathcal{L}_{\mathrm{P}} + \alpha_{3} \mathcal{L}_{\mathrm{sKL}} \quad (7)
$$

默认权重设置为 $\alpha_{1}=0.5$，$\alpha_{2}=1$，$\alpha_{3}=1$。

**软 CLIP 损失模块（$\mathcal{L}_{\mathrm{sCLIP}}$）** 负责多标签软对齐。对于第 $i$ 张图像与第 $k$ 个文本标签，其加权对比损失为：

$$
l_{ik} = - w_{ik} \log \frac{ \exp( \operatorname{sim}(V_i, T_{ik}) / \tau ) }{ \sum_{n=1}^{N} \sum_{m=1}^{M_n} \exp( \operatorname{sim}(V_i, T_{nm}) / \tau ) } \quad (1)
$$

其中 $w_{ik}$ 由图像-标签共现矩阵归一化得到（Eq. 3），使得高频共现的标签对获得更高权重。总软 CLIP 损失取图像→文本和文本→图像两个方向的对称平均（Eq. 2），从而允许每张图像与多个相关标签同时建立软对齐，突破了标准 CLIP 的一对一限制。

**逐点损失模块（$\mathcal{L}_{\mathrm{P}}$）** 在特定粒度上执行二值交叉熵优化，进一步精细化图像特征与文本标签的对应关系：

$$
\mathcal{L}_{\mathrm{P}} = - \sum_{i=1}^{N} \sum_{j=1}^{M} \frac{ y_{ij} \log x'_{ij} + (1 - y_{ij}) \log(1 - x'_{ij}) }{ N } \quad (4)
$$

该模块直接作用于每个标签的预测概率，为多标签分类提供像素级的监督信号。

**平滑 KL 散度损失模块（$\mathcal{L}_{\mathrm{sKL}}$）** 是实现跨粒度一致性的关键机制。对于第 $i$ 个粒度的预测分布 $P_i$ 与所有粒度的均值分布 $M$，计算 KL 散度：

$$
D_{\mathrm{KL}}(P_{i} \| M) = \sum_{j} P_{i}^{(j)} \log \frac{ P_{i}^{(j)} }{ M^{(j)} } \quad (5)
$$

然后对所有粒度求和：

$$
\mathcal{L}_{\mathrm{sKL}} = \sum_{i=1}^{m} D_{\mathrm{KL}}(P_{i} \| M) \quad (6)
$$

该损失强制不同粒度的文本特征向共享均值分布收敛，使得粗粒度标签（如模态）和细粒度标签（如序列描述）在语义空间中保持一致性，从而让视觉编码器学习到跨粒度统一的病理表征。

### 模块间关系

三个损失模块并非孤立运作，而是形成互补关系。消融实验（Table 3）证实：单独使用 $\mathcal{L}_{\mathrm{sCLIP}}$ 或 $\mathcal{L}_{\mathrm{P}}$ 均能带来性能提升，但二者组合时效果更优；在此基础上加入 $\mathcal{L}_{\mathrm{sKL}}$ 后性能达到最佳，表明跨粒度一致性约束与多标签对齐之间存在协同效应——软 CLIP 和逐点损失负责拓宽标签覆盖范围，平滑 KL 散度则确保不同粒度的语义不会相互冲突。

### 输出与下游适配

预训练完成后，视觉编码器输出的特征可直接用于下游任务，无需额外的文本分支。论文将其作为即插即用模块，在线性探测、全微调以及多模态大语言模型的视觉编码器替换中均展现了显著的性能增益。



MGLL 的训练流水线由三个核心损失模块协同构成：**软 CLIP 损失（Soft CLIP Loss）** 实现一对多的多标签软对齐，**逐点损失（Point-wise Loss）** 提供细粒度的成对对齐约束，**平滑 KL 散度损失（Smooth KL Divergence Loss）** 强制不同粒度特征的语义一致性。三者通过加权和组合为最终优化目标。

### 软 CLIP 损失：多标签软对齐

标准 CLIP 损失将每张图像仅与单一文本标签对齐，无法处理医学图像中常见的多标签场景。MGLL 引入软 CLIP 损失，使每张图像能够同时与多个文本标签进行加权对比学习。

对于第 $i$ 张图像与第 $k$ 个文本标签，单对软 CLIP 损失定义为：

$$l_{ik} = - w_{ik} \log \frac{ \exp( \operatorname{sim}(V_i, T_{ik}) / \tau ) }{ \sum_{n=1}^{N} \sum_{m=1}^{M_n} \exp( \operatorname{sim}(V_i, T_{nm}) / \tau ) }$$

其中 $V_i$ 为图像特征，$T_{ik}$ 为第 $k$ 个文本标签特征，$\tau$ 为温度系数（最优值 $\tau=0.07$），$w_{ik}$ 为基于图像-标签共现矩阵归一化得到的权重：

$$w_{ik} = \frac{ \mathrm{cooccurrence}(V_i, T_{ik}) }{ \sum_{k} \mathrm{cooccurrence}(V_i, T_{ik}) }$$

总软 CLIP 损失对图像-文本和文本-图像两个方向对称求和：

$$\mathcal{L}_{\mathrm{sCLIP}} = \frac{1}{2 \sum_{i=1}^{N} M_{i}} \sum_{i=1}^{N} \sum_{k=1}^{M_{i}} (l_{ik} + l_{ki})$$

该损失的核心机制在于：通过共现权重 $w_{ik}$ 对不同标签的重要性进行差异化建模，使视觉特征能够同时对齐多个语义相关的文本描述，而非被强制选择单一标签。

### 逐点损失：细粒度成对对齐

逐点损失采用二值交叉熵形式，在更精细的粒度上优化图像-文本对齐：

$$\mathcal{L}_{\mathrm{P}} = - \sum_{i=1}^{N} \sum_{j=1}^{M} \frac{ y_{ij} \log x'_{ij} + (1 - y_{ij}) \log(1 - x'_{ij}) }{ N }$$

其中 $y_{ij}$ 为真实标签指示符，$x'_{ij}$ 为模型预测的匹配概率。该损失直接作用于每个图像-标签对，为多标签分类提供像素级的监督信号，弥补了软 CLIP 损失在细粒度判别上的不足。

### 平滑 KL 散度损失：跨粒度一致性约束

不同粒度的文本描述（如疾病类别、检查描述、序列描述）虽语义相关，但特征分布可能存在偏移。MGLL 通过平滑 KL 散度损失强制各粒度预测向共享均值分布收敛。

首先计算各粒度预测分布 $P_i$ 与均值分布 $M$ 之间的 KL 散度：

$$D_{\mathrm{KL}}(P_{i} \| M) = \sum_{j} P_{i}^{(j)} \log \frac{ P_{i}^{(j)} }{ M^{(j)} }$$

然后对所有 $m$ 个粒度求和，得到平滑 KL 散度损失：

$$\mathcal{L}_{\mathrm{sKL}} = \sum_{i=1}^{m} D_{\mathrm{KL}}(P_{i} \| M)$$

该损失满足 $D_{\mathrm{KL}}(P_i \| M) \geq 0$，驱动力在于：最小化各粒度分布与均值的差异，使不同粒度的文本特征向共享语义空间收敛，从而在视觉表示中建立跨粒度的一致性。

### 最终损失组合

MGLL 的整体优化目标为三项损失的加权和：

$$\mathcal{L}_{\mathrm{MGLL}} = \alpha_{1} \mathcal{L}_{\mathrm{sCLIP}} + \alpha_{2} \mathcal{L}_{\mathrm{P}} + \alpha_{3} \mathcal{L}_{\mathrm{sKL}}$$

默认权重设置为 $\alpha_{1}=0.5$，$\alpha_{2}=1$，$\alpha_{3}=1$。消融实验证实，三项损失缺一不可：单独使用软 CLIP 或逐点损失均无法达到最优性能，加入平滑 KL 散度后性能进一步提升，表明跨粒度一致性约束与多标签对齐之间存在互补效应。



## 实验与关键发现

### 核心性能突破

MGLL 在眼底与胸部 X 射线两大医学影像领域均展现出显著且一致的性能优势。在眼底多标签数据集 RFMiD 上，MGLL 以线性探测 AUC 79.62% 的成绩，将 CLIP 基线（44.66%）提升了 34.96 个百分点，超越所有对比方法至少 16.6%（Figure 3）。全微调设定下，MGLL 同样保持 6.7% 以上的领先幅度。这一巨大差距说明，CLIP 在面临多标签、多粒度医学图像时，其单标签对齐范式几乎无法提取有效的判别特征。

![[assets/figures/papers/iclr26_0011_ccjukmExrB_Boosting_Medical_Visual_Understanding_From_Multi/figures/004_Figure_3.jpg]]
*Figure 3: The quantitative comparison (AUC) between baseline methods and proposed MGLL on nine fundus downstream datasets*

在胸部 X 射线数据集 ChestX-ray14 上，MGLL 在线性探测下达到 82.94% AUC，比次优方法 CARZero 高出 5.62%（Table 1）。在 MIDRC-XR 和 MIDRC-XR-Portable 上，MGLL 分别取得 61.25% 和 83.86% 的线性探测 AUC，领先幅度为 2.23% 和 4.84%。值得注意的是，MGLL 在 MIDRC-XR-Portable 的全微调设定下 AUC 高达 99.75%，接近饱和，表明预训练特征本身已具备极强的下游适应能力。

![[assets/figures/papers/iclr26_0011_ccjukmExrB_Boosting_Medical_Visual_Understanding_From_Multi/figures/005_Table_1.jpg]]
*Table 1: The performance evaluation on MIDRC-XR, MIDRC-XR-Portable, and ChestX-ray14. Bold indicates best performance and underline shows second-best*

### 损失函数消融：三项组件缺一不可

为验证各损失组件的独立贡献，论文在 RFMiD 上进行了系统消融（Table 3）。仅使用软 CLIP 损失（$\mathcal{L}_{\mathrm{sCLIP}}$）时，性能已显著优于标准 CLIP，证实多标签软对齐是性能提升的基础驱动力。在此基础上加入逐点损失（$\mathcal{L}_{\mathrm{P}}$），性能进一步跃升，说明细粒度的二值交叉熵约束与对比学习存在互补效应。最关键的发现是：引入平滑 KL 散度损失（$\mathcal{L}_{\mathrm{sKL}}$）后，模型达到最佳性能。这一结果表明，跨粒度一致性约束并非锦上添花，而是将不同粒度特征拉向共享语义空间的必要机制——仅有多标签对齐而无跨粒度约束，不同粒度的特征可能各自为政，无法形成统一的病理表征。

![[assets/figures/papers/iclr26_0011_ccjukmExrB_Boosting_Medical_Visual_Understanding_From_Multi/figures/008_Table_3.jpg]]
*Table 3: Ablations of different MGLL objectives on RFMiD. Table 4: Ablations of granularity count on MIDRC-XR-Portable*

### 粒度数目与编码器选择

粒度数目的消融实验（Table 4）揭示了层次化信息的累积效应。在 MIDRC-XR-Portable 上，使用 3 粒度（模态、检查描述、序列描述）的 MGLL₃ 相较 CLIP 基线在线性探测 AUC 上提升 12.43%，而使用 1 或 2 粒度的版本提升幅度明显收窄。这证实了医学文本中不同抽象层次的信息并非冗余，而是各自携带互补的病理线索。

![[assets/figures/papers/iclr26_0011_ccjukmExrB_Boosting_Medical_Visual_Understanding_From_Multi/figures/009_Table_4.jpg]]

编码器消融（Table 5-6）表明，ViT-L/14 作为图像编码器与 BiomedicalBERT 作为文本编码器的组合在所有指标上均达到最优。BiomedicalBERT 的领域预训练使其能更准确地编码医学术语，这是通用文本编码器无法替代的优势。

### 鲁棒性分析：缺失标签与文本质量

MGLL 对不完整标注展现出令人惊讶的鲁棒性。在 30% 粒度标签随机缺失的条件下，MGLL 线性探测 AUC 仍维持在 79.61%，远超使用完整标签训练的 CLIP（Table 37）。这一特性源于软 CLIP 损失的共现权重机制——即使部分标签缺失，图像仍可通过剩余的关联标签获得有效的监督信号。

文本质量消融（Table 8）进一步揭示了 MGLL 的容错边界。使用标准分辨率文本时性能最优；引入随机错误或降低文本质量会导致性能下降，但降幅有限，表明模型并非机械记忆文本表面形式，而是提取了语义层面的稳定特征。

### 定性分析：病灶定位能力

类别激活图（CAM）可视化（Figure 4）提供了最直观的证据。CLIP 的激活区域呈现弥散分布，无法聚焦于病灶；而 MGLL 能精确定位硬性渗出、视网膜色素上皮等关键病理区域。这一差异的因果链条清晰：多粒度文本监督迫使模型学习将视觉特征与不同抽象层次的病理描述对齐，从而在特征空间中形成了更具局部判别力的表征。

![[assets/figures/papers/iclr26_0011_ccjukmExrB_Boosting_Medical_Visual_Understanding_From_Multi/figures/006_Figure_4.jpg]]
*Figure 4: The Class Activation Maps of different diseases from CLIP and MGLL*

### 失败模式与局限

尽管 MGLL 在眼底和 X 射线数据上表现优异，但其验证范围尚未覆盖 CT、MRI 等三维模态。多粒度文本描述依赖人工构建的层级标注体系，无法动态适应新疾病或新场景。在极端罕见疾病类别上，由于共现矩阵稀疏，软 CLIP 损失的权重估计可能不稳定。此外，MGLL 尚未探索与大型语言模型的直接耦合以自动生成或细化多粒度监督信号——这构成了一个明确的能力边界。

### 关键图表索引

| 图表 | 核心结论 |
|------|----------|
| Table 1 | MGLL 在三个胸部 X 射线数据集上全面领先，ChestX-ray14 上领先次优方法 5.62% AUC |
| Figure 3 | 九个眼底下游数据集上 MGLL 一致优于所有基线，RFMiD 上领先至少 16.6% |
| Table 3 | 三项损失组件组合达到最佳，平滑 KL 散度带来关键增益 |
| Table 4 | 增加粒度数目持续提升性能，3 粒度版本最优 |
| Figure 4 | MGLL 的 CAM 精确定位病灶，CLIP 仅产生弥散激活 |



## 定位与知识库关联

### 方法定位：从单标签对比到多粒度软对齐

MGLL 的核心创新在于将标准 CLIP 范式的**单标签、单粒度**对比学习，扩展为**多标签、多粒度**的软对齐框架。这一转变直指医学影像分析中的真实瓶颈：医学图像天然关联多个不同粒度的文本描述（如疾病类别、检查描述、序列描述），而现有方法无法充分利用这种层次化信息。

在方法谱系中，MGLL 与以下基线方法形成递进关系：

- **CLIP**：标准单标签对比学习，仅支持图像与单一文本标签的一对一对齐（Eq. 8）。MGLL 将其扩展为软 CLIP 损失（Eqs. 1-3），通过共现权重 $w_{ik}$ 实现一对多软对齐。
- **CheXzero / CARZero**：基于语义匹配或病例表征的零样本对比学习方法，仍局限于单一粒度对齐。MGLL 在此基础上引入多粒度文本监督，并显式建模跨粒度一致性。
- **MRM（多标签对比学习）**：支持多标签但对齐机制缺乏粒度层次。MGLL 的逐点损失（Eq. 4）提供了更精细的成对图像-文本对齐，同时平滑 KL 散度（Eqs. 5-6）强制不同粒度特征向共享均值分布收敛，这是 MRM 所不具备的跨粒度约束。
- **UniChest / UniMed-CLIP**：统一的视觉-语言模型，将不同粒度文本投影到同一空间，但无显式一致性约束。MGLL 的平滑 KL 散度填补了这一空白。
- **KAD（知识感知诊断）**：利用外部知识图谱增强医学影像分析，而 MGLL 通过多粒度文本描述本身构建层次化监督信号，无需外部知识库。

### 适用边界与验证范围

MGLL 已在两个医学影像模态上得到全面验证：

- **眼底图像**：在 RFMiD 多标签数据集上，线性探测 AUC 领先其他 SOTA 模型至少 16.6%，全微调领先至少 6.7%（Figure 3）。跨九个眼底下游数据集的定量对比（Figure 3）进一步验证了泛化能力。
- **胸部 X 射线**：在 ChestX-ray14 上线性探测 AUC 达 82.94%，超越次优方法 CARZero 5.62%；在 MIDRC-XR 上达 61.25%，超越 UniChest 2.23%（Table 1）。

此外，MGLL 作为即插即用的视觉编码器，已集成到七种多模态大语言模型（MLLMs）中，在眼科多项选择题基准（2,233 个临床病例）上带来 4.6% 至 34.1% 的准确率提升（Table 2），展示了从预训练到下游应用的可迁移性。

### 关键局限

1. **模态覆盖有限**：仅在眼底图像和 X 射线图像上进行了全面验证，尚未扩展到 CT、MRI 等其他医学模态或非医学领域。这一局限限制了 MGLL 作为通用多粒度对比学习框架的普适性声明。

2. **文本监督依赖人工构建**：多粒度文本描述依赖人工标注的层级结构，无法动态生成适应新场景的细粒度描述。尽管消融实验显示 MGLL 对缺失标签具有鲁棒性（30% 粒度标签缺失时线性探测 AUC 仍达 79.61%，远超完整标签训练的 CLIP），但文本质量消融（Table 8）表明，标准分辨率文本描述的性能显著优于错误或缺失文本，说明文本质量仍是性能上限的关键因素。

3. **未与大型语言模型直接结合**：当前框架未探索利用 LLM 自动生成或细化多粒度文本监督信号的可能性，这限制了 MGLL 在开放场景下的扩展性。

4. **极端罕见类别与高比例噪声**：尽管 MGLL 展现出一定鲁棒性，但在极端罕见的疾病类别或高比例标注噪声下，性能提升仍有空间。

### 开放问题

1. **多模态扩展**：MGLL 能否从图像-文本对扩展到包含患者元数据、时序信息等多模态输入的联合对齐？这需要设计新的粒度定义和一致性约束机制。

2. **域自适应与泛化**：如何通过域自适应技术提升 MGLL 对未见的医学条件或成像模态的泛化能力？当前验证局限于预训练数据覆盖的疾病类别。

3. **与大规模语言模型的集成**：MGLL 能否与 LLM 集成，自动生成更细致的多粒度文本描述，从而减少对人工标注的依赖并扩展至新疾病类别？

4. **跨领域迁移**：MGLL 的多粒度软对齐机制在其他具有内在层次结构的领域（如卫星影像、科学可视化）是否同样有效？这需要验证框架的领域无关性。

5. **计算效率与规模扩展**：当前 MGLL 使用 ViT-L/14 作为图像编码器、BiomedicalBERT 作为文本编码器，消融实验（Table 5-6）确认了该组合的最优性。但在更大规模数据集上的计算效率与扩展性尚未系统评估。



## 原文 PDF

![[paperPDFs/ICLR_2026/Boosting_Medical_Visual_Understanding_From_Multi_Granular_Language_Learning.pdf]]

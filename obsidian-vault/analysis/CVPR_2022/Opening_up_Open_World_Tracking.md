---
title: "Opening up Open-World Tracking"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/Opening_up_Open_World_Tracking.pdf
project_link: https://openworldtracking.github.io/
aliases:
- OOWTB
- OUOWT
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "结合目标性（objectness）与背景（background）分数的提议排序，以及融合光流和外观特征（ReID）的关联相似度计算，是提升未知目标跟踪性能的关键控制因素。"
primary_logic: "闭世界目标检测器（如Mask R-CNN）通过其内置的区域提议网络（RPN）和目标/非目标分类器，能够泛化至未知对象；但需设计合适的评分机制与关联策略以充分发挥此泛化能力。"
claims:
- "已知大目标召回率99.7%，未知大目标98.2%，但未知小目标仅66.1%，显示检测器泛化虽好但小目标召回严重不足。"
- "结合objectness和background分数的排序方式将未知目标提议AUC从0.59提升至0.70，改善幅度显著。"
- "光流+ReID混合相似度将未知目标跨帧关联Top-1准确率从70.7%提升至81.9%，远超单一线索。"
- "OWTB在TAO-OW验证集上已知OWTA达60.2，未知39.2，分别超出SORT基线13.6和5.3个百分点。"
---

# Opening up Open-World Tracking

> [!tip] 核心洞察
> 闭世界目标检测器（如Mask R-CNN）通过其内置的区域提议网络（RPN）和目标/非目标分类器，能够泛化至未知对象；但需设计合适的评分机制与关联策略以充分发挥此泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 开启开放世界跟踪 |
| 英文题名 | Opening up Open-World Tracking |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2104.11221); [Project](https://openworldtracking.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | OWTB (Open-World Tracking Baseline) |
| Dataset | TAO-OW val, TAO-OW test, DAVIS Unsupervised |

> [!tip] 效果简介
> - TAO-OW val 上，OWTA (Known) 为 60.2，对比 46.6 (SORT)，变化 +13.6。
> - TAO-OW val 上，OWTA (Unknown) 为 39.2，对比 33.9 (SORT)，变化 +5.3。
> - TAO-OW test 上，OWTA (Unknown-Unknown) 为 41.5，对比 38.5 (Unknown val)，变化 comparable。

## 概述

**开放世界跟踪**（Open-World Tracking）要求同时跟踪预定义语义类别的已知对象，以及训练集中从未出现的未知对象。传统闭世界跟踪器仅依赖类别置信度进行检测与关联，导致未知目标的召回率和跨帧关联准确率显著不足——尤其在小目标场景下，未知小目标召回率仅66.1%，远低于已知大目标的99.7%（Table 1）。

本文提出**OWTB**（Open-World Tracking Baseline），将标准的检测-跟踪流水线重构为四个可泛化阶段：**提议生成**、**提议评分**、**短时关联**与**长时管理**。核心控制机制在于两点：

1. **提议评分**：将传统类别置信度替换为“目标性+背景”联合分数（obj.+bg），使未知目标提议AUC从0.59提升至0.70（Figure 7）。
2. **关联相似度**：融合光流扭曲的Box IoU与Mask R-CNN的ReID余弦相似度，将未知目标跨帧关联Top-1准确率从70.7%提升至81.9%（Table 2）。

在TAO-OW验证集上，OWTB的已知OWTA达60.2，未知OWTA达39.2，分别超出SORT基线13.6和5.3个百分点（Table 3）。该方法在闭世界基准DAVIS无监督和KITTI-MOTS上也展现出竞争力，无需额外调参。

**方法定位**：OWTB属于基于检测的跟踪范式（Tracking-by-Detection），核心创新在于利用闭世界检测器（Cascade Mask R-CNN）的区域提议网络和目标性分类器的泛化能力，通过重新设计评分与关联策略，将知识从已知类别迁移至未知对象。该方法不依赖未知类别的标注数据，也未引入额外的开放世界训练。

**主要局限**：未知小目标的检测召回仍是瓶颈；快速运动、大幅度变形及完全遮挡后的重识别几乎无法正确跟踪；长时关联在召回与精度之间难以取得更好平衡。未来方向包括利用多帧时序上下文改进检测、构建未知对象的鲁棒外观模型，以及利用大规模未标注视频数据。

## 背景与动机

### 闭世界跟踪的范式局限

多目标跟踪（MOT）领域长期遵循**闭世界假设**：检测器与跟踪器仅对预定义的语义类别（如行人、车辆）进行定位与关联。这一范式在自动驾驶、视频监控等场景中取得了显著进展，但其根本局限在于——现实世界中大量“未知”对象（如婴儿车、滑板、动物等）被系统性忽略。Figure 1 直观对比了两类范式的输出差异：左侧为传统闭世界跟踪仅输出已知类别，右侧为本文方法能够同时跟踪训练集中未标注的对象。

这一局限并非仅仅是类别覆盖面的问题，而是触及了跟踪系统泛化能力的本质：**一个真正鲁棒的跟踪系统应当能够定位并持续跟踪任何运动对象，无论其语义类别是否在训练集中出现。**

### 开放世界跟踪的核心瓶颈

本文通过构建 TAO-OW 基准并系统分析现有方法，揭示了开放世界跟踪面临的两个关键瓶颈：

**瓶颈一：未知目标的检测召回率严重不足，尤其小目标。** Table 1 的数据直接量化了这一差距：已知大目标召回率达 99.7%，未知大目标亦可达 98.2%，但未知小目标的召回率骤降至 66.1%。这表明闭世界检测器（如 Mask R-CNN）的区域提议网络（RPN）虽具备一定的跨类别泛化能力，但在小尺度未知对象上几乎失效。Figure 7 进一步显示，使用标准类别置信度分数排序提议时，未知目标的提议召回 AUC 仅为 0.59，远低于已知目标的水平。

**瓶颈二：跨帧关联的准确性不足。** 在开放世界中，缺乏针对未知类别的专门外观模型，导致基于传统框交并比（Box IoU）的关联策略在快速运动、变形或遮挡场景下准确率急剧下降。Table 2 的消融实验表明，纯 Box IoU 对未知目标的跨帧关联 Top-1 准确率仅为 70.7%，远不能满足长时稳定跟踪的需求。

### 本文动机与核心洞察

本文的核心洞察在于：**闭世界目标检测器通过其内置的 RPN 和目标/非目标分类器，天然具备向未知对象泛化的潜力——关键在于设计合适的评分机制与关联策略以充分释放这一潜力。**

基于此洞察，本文提出 **OWTB（Open-World Tracking Baseline）**，将跟踪-检测范式分解为四个可控阶段（Figure 6）：(1) 提议生成、(2) 跨帧相似度估计、(3) 轨迹管理与关联、(4) 重叠消除。在每个阶段，OWTB 通过简单的设计选择——结合目标性与背景分数的提议排序、融合光流与外观特征的关联相似度——显著提升了未知目标的跟踪性能，同时保持了已知目标的竞争力。

## 核心创新

OWTB 的核心创新并非提出全新的跟踪范式，而是**系统性地揭示了闭世界检测器向开放世界泛化的关键控制因素**，并通过三个“changed slots”将这一洞察工程化为一个高性能基线。

### 1. 瓶颈识别：从“能否检测”到“如何排序”

论文首先诊断出核心瓶颈：闭世界检测器（如 Cascade Mask R-CNN）的区域提议网络（RPN）本身具备对未知目标的泛化能力——已知大目标召回率高达 99.7%，未知大目标亦达 98.2%（Table 1）。真正的短板在于**未知小目标的召回率骤降至 66.1%**，且标准分类置信度评分无法有效区分未知目标的提议质量。这意味着，开放世界跟踪的性能天花板并非检测器的架构局限，而是**提议排序机制与目标特性之间的失配**。

### 2. 关键控制变量：提议评分机制的重构

OWTB 的核心操作是将提议评分从单一的“类别置信度”替换为 **objectness + background 的组合分数**（obj.+bg）。这一改变的因果效应在 Figure 7 中清晰呈现：未知目标提议的召回率曲线下面积（AUC）从 0.59（类别置信度）跃升至 0.70，改善幅度远超过其他评分策略（如仅用 objectness 或仅用 background）。其机理在于：objectness 分数衡量“该区域包含物体的概率”，background 分数衡量“该区域不属于背景的概率”，两者均不依赖语义类别标签，因此在面对训练集未见的类别时仍能保持校准——这正是闭世界检测器泛化能力的来源，而标准分类头输出的类别置信度在未知类别上则成为噪声。

### 3. 跨帧关联：从单一几何线索到混合相似度

在短时关联阶段，OWTB 将相似度计算从单纯的 Box IoU 升级为**光流扭曲 Box IoU 与 Mask R-CNN ReID 余弦相似度的混合**。Table 2 的消融实验表明，这一改变对未知目标的提升幅度远超已知目标：未知目标 Top-1 关联准确率从 70.7%（Box IoU）提升至 81.9%（Flow-Box IoU + MaskRCNN cosine），净增 11.2 个百分点；而已知目标仅从 86.4% 提升至 88.2%。这揭示了光流运动线索和外观嵌入在未知目标关联中的互补性——当语义类别先验缺失时，低层运动一致性与实例级外观特征成为更可靠的关联锚点。

值得注意的是，引入中间帧传播（intermediate frames）虽然将已知目标准确率进一步提升至 91.4%，却使未知目标回落至 79.3%。这一反向效应暗示：基于光流的中间帧插值可能引入了对已知类别运动模式的过拟合，在未知目标的非刚性变形或异常运动上反而产生误导。

### 4. 长时跟踪：在线匹配与离线合并的协同

在跟踪管理层面，OWTB 在标准 Hungarian 在线匹配之后增加了 **UnOVOST 风格的离线轨迹段合并（offline tracklet merging）**。Table 4 显示，Hung.+OffTM 组合将未知 OWTA 从纯在线匹配的 37.8 推至 40.2，已知 OWTA 从 58.9 推至 60.5。这一改进的因果逻辑在于：离线合并能够修正因短期遮挡或检测缺失导致的轨迹碎片化，而这恰恰是开放世界场景下未知目标跟踪的主要失败模式之一。

### 5. 创新定位：工程洞察而非算法发明

OWTB 的三个 changed slots 均非全新算法模块——objectness/background 评分、光流 ReID 融合、离线轨迹合并皆为现有技术的重新组合。其真正的创新在于：**通过受控消融实验，首次量化了每个设计选择对未知目标跟踪性能的边际贡献**，从而将“闭世界检测器能否用于开放世界跟踪”这一模糊问题转化为“如何排序提议、如何计算相似度、如何管理轨迹”这三个可操作的工程决策。这一方法论贡献使得 OWTB 在 TAO-OW 验证集上以已知 OWTA 60.2、未知 OWTA 39.2 的成绩，分别超出 SORT 基线 13.6 和 5.3 个百分点（Table 3），同时保持了流水线的简洁性与可复现性。

## 整体框架

OWTB（Open-World Tracking Baseline）遵循经典的“检测-跟踪”（tracking-by-detection, TBD）范式，并将其分解为四个独立且可替换的阶段，如图6所示。该流水线以逐帧方式处理视频，最终输出每个目标在整个时间轴上的非重叠分割掩膜与身份标识。

**阶段一：目标提议生成（Proposal Generation）**

对于每一帧输入图像，使用在COCO 80类上预训练的Cascade Mask R-CNN生成候选目标提议。为最大化未知目标的召回，关闭非极大值抑制（NMS），每帧保留1000个提议，每个提议包含掩膜、边界框及相关置信度分数。

**阶段二：跨帧相似度估计（Short-term Association）**

为建立帧间目标对应关系，将短时关联形式化为一个相对分类问题：给定第$t$帧中的一个查询提议，在$t+k$帧的$N$个候选提议中识别其对应目标。相似度计算采用混合策略：将基于光流扭曲的边界框交并比（Flow-warped Box IoU）与Mask R-CNN的ReID特征余弦相似度进行平均，从而同时利用运动线索与外观线索。

**阶段三：轨迹形成与管理（Track Management）**

基于跨帧相似度矩阵，首先采用在线匈牙利匹配进行逐帧关联，随后应用离线轨迹片段合并（offline tracklet merging）策略，以恢复因遮挡或检测中断而断裂的轨迹片段。此阶段负责维护轨迹的生命周期，包括轨迹的创建、延长与终止。

**阶段四：时空冲突解决（Overlap Removal）**

为满足每个像素唯一分配给一个目标的评估要求，采用“先非重叠再跟踪”（non-overlap then track）策略：在每帧内部，基于提议分数进行空间非极大值抑制，消除重叠提议后再执行跟踪关联。这确保了输出轨迹在空间上互斥，避免冗余跟踪。

整个流水线的核心控制点在于：提议阶段的目标性（objectness）与背景（background）联合评分机制，以及关联阶段的运动-外观混合相似度计算。这两处设计是闭世界检测器泛化至开放世界未知目标的关键使能因素。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/006_Figure_6.jpg]]
*Figure 6: Open-world tracking baseline (OWTB) is inspired by tracking-by-detection pipeline: we (1) obtain object proposals, (2) compute cross-frame association scores, that are used to (3) form and manage tracks, and finally, (4) ensure that conflicts with tracks occupying same space-time volume are resolved*

## 核心模块与公式推导

### 开放世界跟踪精度（OWTA）

OWTB 的核心评估指标为开放世界跟踪精度（Open-World Tracking Accuracy, OWTA），其设计意图是避免因数据集未穷尽标注而对正确检测产生误罚。OWTA 是一个基于召回率的指标，不惩罚误报，由检测召回（DetRe）和关联精度（AssA）两项构成：

$$\mathrm{OWTA}_{\alpha} = \sqrt{\mathrm{DetRe}_{\alpha} \cdot \mathrm{AssA}_{\alpha}}$$

其中 $\alpha$ 为定位阈值，OWTA 在多个 $\alpha$ 值上积分得到最终得分。

**检测召回（DetRe）** 定义为真正例与总标注目标的比值，显式忽略误报：

$$\mathrm{DetRe}_{\alpha} = \frac{|\mathrm{TP}_{\alpha}|}{|\mathrm{TP}_{\alpha}| + |\mathrm{FN}_{\alpha}|}$$

**关联精度（AssA）** 通过对每个匹配的跟踪片段计算时序交并比的平均值来衡量跨帧关联质量：

$$\operatorname{AssA}_{\alpha} = \frac{1}{|\mathrm{TP}_{\alpha}|} \sum_{c \in \mathrm{TP}_{\alpha}} \frac{\mathrm{TPA}_{\alpha}(c)}{\mathrm{TPA}_{\alpha}(c) + \mathrm{FPA}_{\alpha}(c) + \mathrm{FNA}_{\alpha}(c)}$$

其中 $\mathrm{TPA}_{\alpha}(c)$ 为真正关联，$\mathrm{FPA}_{\alpha}(c)$ 和 $\mathrm{FNA}_{\alpha}(c)$ 分别为误关联和漏关联。该公式对每个真正例 $c$ 独立计算关联质量后取平均，确保评估不受检测数量偏差影响。

### OWTB 流水线模块

OWTB 遵循经典的检测-跟踪（tracking-by-detection）范式，将开放世界跟踪分解为四个阶段（Figure 6）：

1. **提议生成（Proposal Generation）**：使用 Cascade Mask R-CNN 为每帧生成 1000 个候选掩膜，禁用 NMS 以保证召回。检测器仅在 COCO 80 类上训练，但通过其内置的区域提议网络（RPN）和目标/非目标分类器，能泛化至未知对象。

2. **提议评分（Proposal Scoring）**：采用 `objectness + background` 分数的算术平均对提议排序。该评分机制是提升未知目标召回的关键控制因素——将未知目标提议 AUC 从 0.59（仅类别置信度）提升至 0.70（Figure 7）。

3. **短时关联（Short-term Association）**：将跨帧关联建模为相对分类问题：给定 $t$ 帧的查询提议，在 $t+k$ 帧的 $N$ 个候选中识别对应目标。相似度计算融合光流扭曲后的 Box IoU 与 Mask R-CNN ReID 特征的余弦相似度，混合相似度将未知目标 Top-1 准确率从 70.7%（纯 Box IoU）提升至 81.9%（Table 2）。

4. **长时跟踪与重叠消除（Long-term Tracking & Overlap Removal）**：在线匈牙利匹配后执行离线轨迹段合并（UnOVOST 风格），并采用“先非重叠再跟踪”（non-overlap then track）策略进行空间非极大值抑制。

### 关键设计决策

- **提议评分**：算术平均优于几何平均或仅用单一分数，因为 `objectness` 和 `background` 分数在未知目标上提供互补信息。
- **关联相似度**：光流提供运动线索，ReID 提供外观线索，二者互补。中间帧传播虽提升已知目标准确率（88.2），但损害未知目标准确率（65.9），故最终方案不使用中间帧。
- **轨迹管理**：离线合并（Hung.+OffTM）在已知 OWTA 60.5 和未知 OWTA 40.2 上均优于纯在线匈牙利匹配（Table 4）。

## 实验与分析

### 基准与评估协议

实验在 TAO-OW 验证集和测试集上进行，该基准将类别划分为已知（80 类，来自 COCO）和未知（其余类别），后者作为开放世界中无限多样对象的代理。评估采用本文提出的 **OWTA** 指标，其定义为检测召回（DetRe）与关联精度（AssA）的几何平均：

$$\mathrm{OWTA}_{\alpha} = \sqrt{\mathrm{DetRe}_{\alpha} \cdot \mathrm{AssA}_{\alpha}}$$

该指标仅惩罚漏检和关联错误，不惩罚误报，从而避免因数据集未穷尽标注而对正确检测产生误罚。所有输出要求非重叠掩膜，每个像素唯一分配，防止通过产生冗余跟踪来刷分。训练仅使用 COCO 80 类，类别相似但标签不同的干扰类被半自动识别并排除评估。

### 主要结果

**TAO-OW 验证集。** OWTB 在已知类别上 OWTA 达 60.2，未知类别达 39.2，分别超出 SORT 基线 13.6 和 5.3 个百分点（Table 3）。这一提升来源于三个关键设计：提议评分、跨帧关联相似度计算和长时跟踪策略。在检测召回维度，OWTB 对已知类别达 72.1，未知类别达 51.7，而 SORT 分别为 56.4 和 44.2；在关联精度维度，OWTB 已知/未知分别为 50.3/29.7，SORT 为 38.6/26.1。结果表明，闭世界检测器的泛化能力在正确的评分与关联策略加持下可显著释放，但未知目标跟踪性能仍远低于已知目标，构成开放世界跟踪的核心瓶颈。

**TAO-OW 测试集。** 在未知-未知（Unknown-Unknown）类别上，OWTB 的 OWTA 为 41.5，与验证集未知类别表现可比，表明方法对未见类别具有一定泛化性。

**闭世界基准迁移。** 在 DAVIS 无监督视频目标分割上，OWTB 取得 65.5 的 J&F 分数，略低于 UnOVOST 的 67.9（-2.4），但优于多数先前方法。在 KITTI-MOTS 测试集上，OWTB 的 HOTA car 达 64.0，超越 PointTrack 的 61.9（+2.1），证明该方法在传统闭世界场景同样具有竞争力（Table 5）。

### 消融实验

**提议评分策略。** 对未知目标，仅使用类别置信度排序的提议 AUC 仅为 0.59，而结合目标性（objectness）与背景（background）分数的算术平均排序将 AUC 提升至 0.70（Figure 7 左/中）。已知目标的 AUC 也由 0.89 提升至 0.93。这表明 RPN 内置的 objectness 和 background 头提供了超越语义类别的泛化定位信号，是释放闭世界检测器开放世界能力的关键控制因素。

**跨帧关联相似度。** 在 1FPS 采样下的提议关联分类任务中，单纯 Box IoU 对未知目标 Top-1 准确率为 70.7%，已知为 86.4%。引入光流 warp 后的 Box IoU 将未知准确率提升至 76.2%，但已知略降至 85.6%。最终方案——光流 warp Box IoU 与 Mask R-CNN ReID 余弦相似度取平均——将未知准确率推至 81.9%，已知回升至 86.7%（Table 2）。中间帧传播虽将已知准确率提至 88.2%，却使未知降至 65.9%，说明时序平滑假设对未知目标不成立，可能是由于未知目标的外观和运动模式与已知类别差异更大。

**长时跟踪策略。** 在线匈牙利匹配（Hung.）的已知/未知 OWTA 为 59.7/38.7。引入离线轨迹段合并（Hung.+OffTM）将未知 OWTA 提升至 40.2，已知提升至 60.5（Table 4）。多步保活策略（KA）反而导致性能下降，表明简单的在线启发式对未知目标可能引入噪声关联。

**重叠去除顺序。** 先非重叠抑制再跟踪（NO→T）的已知 OWTA 为 60.5，略优于先跟踪再抑制（T→NO）的 59.7（Table 4）。差异虽小，但 NO→T 策略避免了跟踪阶段对后续将被抑制的冗余提议投入计算资源。

### 失败模式与局限性

**小目标召回严重不足。** Table 1 显示，已知大目标召回率 99.7%，未知大目标 98.2%，但未知小目标仅 66.1%。检测器虽展现出令人惊讶的泛化能力，但小尺度未知对象仍是显著弱点，常出现部分检测或完全漏检。

**快速运动与遮挡。** 跨帧关联对未知目标的准确率虽经优化后提升至 81.9%，但在快速运动、大幅度变形及完全遮挡后重现的场景下几乎无法正确关联。光流 warp 依赖局部运动连续性假设，ReID 特征对未知类别未经专门训练，两者在极端条件下均会失效。

**长时关联的固有限制。** 尽管离线轨迹段合并带来增益，未知目标的关联精度（AssA）仅为 29.7，远低于已知的 50.3。现有策略在关联召回和精度之间难以取得更好平衡，开放世界长时跟踪仍是一个未解决的挑战。

**知识迁移的边界。** 当前方法仅从已知类别迁移知识，未利用大规模未标注数据。当未知目标的外观、形状或运动模式与已知类别差异极大时，RPN 提议质量和 ReID 特征判别力均会显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/007_Figure_7.jpg]]
*Figure 7: Recall Analysis. Proposal generation recall vs number of proposals for different scoring methods at IoU threshold 0.5 for (left) known objects and (center) unknown objects. Right: Track recall at varying % objects correctly recalled: e.g., 50% detected means at least half of the track must be correctly localized*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/009_Table_2.jpg]]
*Table 2: Association Similarity Ablation. Top-1 accuracy on 1FPS proposal association classification for various approaches - see text. Best performing methods colored: 1st, 2nd, 3rd, 4th, 5th. The Inter. column indicates whether ‘intermediate frames’ were used. *Non open-world oracle (trained on unknown classes)*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/008_Table_1.jpg]]
*Table 1: Recall/size Analysis. Recall for varying object sizes (1k proposals/image). While models work well for known objects, and large unknown objects, they struggle on smaller unknown objects*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/010_Table_3.jpg]]
*Table 3: Results of our OWTB on the TAO-OW val. and test set. We report results in terms of our proposed OWTA metric, and additionally compare methods in terms of Detection Recall (D.Re), Association Accuracy (A.Acc), Association Recall (A.Re) and Association Precision (A.Pr). On the val set we compare our final Open-World Tracking Baseline (OWTB) to previous SOTA trackers on TAO-OW val. For the test set, Unknown classes are the same as those present in the val set, while Unknown-Unknown classes are further unknown classes only present in the test set. *: Non open-world (trained on unknown classes), †: contains overlapping results*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/012_Table_5.jpg]]
*Table 5: Results of our OWTB on closed-world benchmarks DAVIS Unsupervised (val) and KITTI-MOTS (test), compared to all previous published methods. *MOTSFusion additionally uses stereo-depth information*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/013_Table_4.jpg]]
*Table 4: Long-term tracking and Overlap removal. Ablation of various long-term tracking and overlap removal strategies on TAO-OW val. Hung.: Online Hungarian algorithm; KA: Online multi-step keep-alive strategy, OffTM: Offline tracklet merging. NO→T: Non-overlap first, and then track. T→NO: Track first, and then non-overlap*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/002_Figure_2.jpg]]
*Figure 2: TAO-OW Benchmark class distribution in the validation set, showing known classes for which training data is given, and the unknown classes which serve as a proxy for the infinite variety (unknown unknowns) of objects which may appear in an open-world. Note the y-axis is log-scaled*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_11221/figures/005_Figure_5.jpg]]
*Figure 5: TAO-OW classes. Word cloud showing known (left) and unknown (right) classes in our TAO-OW benchmark, with wordsize proportional to frequency*

## 方法谱系与知识库定位

### 追踪范式定位

OWTB 严格遵循 **tracking-by-detection (TBD)** 范式，将开放世界多目标跟踪分解为四个可独立优化的阶段：提议生成、跨帧相似度估计、数据关联与轨迹管理、以及轨迹到像素的分配（Figure 6）。这一分解并非原创，而是对闭世界TBD跟踪器（如 **SORT**）的显式继承与泛化——核心差异在于每个阶段必须对训练中未见过的对象类别保持有效。

### 与基线方法的关系

**SORT** 作为闭世界TBD跟踪器的代表，直接使用检测器的类别置信度进行提议筛选，并以框交并比（Box IoU）作为关联相似度。OWTB 在保持相同流水线结构的前提下，对三个关键槽位进行了替换：

1. **提议评分槽**：将类别置信度替换为 objectness + background 的算术平均分数（Section 5.1, Figure 7），使未知目标的提议排序AUC从0.59提升至0.70。
2. **关联相似度槽**：将纯 Box IoU 替换为光流扭曲框IoU与Mask R-CNN ReID余弦相似度的混合度量（Table 2），将未知目标跨帧关联Top-1准确率从70.7%提升至81.9%。
3. **轨迹管理槽**：在在线匈牙利匹配后追加离线轨迹合并（UnOVOST风格），进一步提升长时跟踪的关联召回（Table 4）。

**UnOVOST** 被视为开放世界跟踪的参照点，其离线轨迹合并策略被OWTB吸收为长时关联模块。在DAVIS无监督基准上，OWTB的J&F为65.5，略低于UnOVOST的67.9（Table 5），表明OWTB的通用TBD设计在视频目标分割专项任务上尚未超越专用方法，但其优势在于无需针对特定基准调优即可跨任务迁移。

**PReMVOS** 作为在未知类别上训练的ReID预言机，代表了关联相似度的理论上界。OWTB并未假设此类特权信息，而是依赖Mask R-CNN在已知类别上学习的ReID特征对未知对象的泛化能力。

### 适用边界

OWTB的有效性建立在以下前提之上：

- **检测器的泛化能力**：依赖闭世界检测器（Cascade Mask R-CNN）的区域提议网络（RPN）和目标/非目标分类器对未知对象的零样本泛化。当未知对象与已知类别在视觉外观上差异极大时，提议召回率显著下降（Table 1：未知小目标召回仅66.1%，而未知大目标达98.2%）。
- **运动连续性**：光流扭曲假设帧间运动平滑。在快速运动、大幅度变形或完全遮挡后重现的场景下，关联准确率急剧退化——这是Table 2中所有关联方法在未知类别上表现均低于已知类别的根本原因。
- **非重叠假设**：每个像素唯一分配给一个轨迹（Section 5.4），在密集遮挡场景中可能产生冲突。

### 已知局限

1. **小目标检测召回瓶颈**：这是当前开放世界跟踪最严重的性能短板。Table 1显示未知小目标召回率仅66.1%，远低于已知大目标的99.7%。检测器的RPN在已知类别上训练，对小尺寸未知对象的激活不足。
2. **长时关联的精度-召回权衡**：Table 4显示离线轨迹合并（Hung.+OffTM）在提升关联召回的同时，关联精度有所下降。当前方法无法在不牺牲精度的情况下显著提升召回，长时重识别仍是开放问题。
3. **未利用未标注数据**：OWTB仅从COCO的80个已知类别迁移知识，未利用大规模未标注视频中的自监督或半监督信号，限制了跟踪能力的进一步提升空间。

### 开放问题

1. **时序上下文用于检测增强**：当前每帧独立生成提议，未利用多帧时序信息来提升未知目标的检测召回率。如何设计时序聚合机制以补救小目标漏检，是一个直接且高优先级的方向。
2. **未知对象的长期外观模型**：现有ReID特征在已知类别上训练，对未知对象的判别力有限且随时间退化。能否为从未见过的对象在线构建鲁棒的长期外观表征，是长时关联突破的关键。
3. **大规模未标注视频的利用**：开放世界场景下存在海量未标注视频数据，如何通过自监督预训练或半监督微调提升检测和关联的泛化能力，是缩小已知-未知性能差距的潜在路径。
4. **端到端开放世界跟踪**：当前TBD范式将检测与跟踪分离，限制了联合优化的可能性。设计端到端的开放世界跟踪器，使提议生成和关联学习能够协同适应未知对象，是一个架构层面的开放挑战。

## 原文 PDF

![[paperPDFs/CVPR_2022/Opening_up_Open_World_Tracking.pdf]]

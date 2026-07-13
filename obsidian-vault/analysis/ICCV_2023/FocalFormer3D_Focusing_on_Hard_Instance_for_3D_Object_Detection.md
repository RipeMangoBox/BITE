---
title: "FocalFormer3D : Focusing on Hard Instance for 3D Object Detection"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/FocalFormer3D_Focusing_on_Hard_Instance_for_3D_Object_Detection.pdf
project_link: null
code_link: https://github.com/NVlabs/FocalFormer3D
aliases:
- FocalFormer3D
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "Hard Instance Probing (HIP) 多阶段流水线自动识别假阴性（未匹配的真值目标），并利用累积正掩模（Accumulated Positive Mask）抑制前期容易的正样本，迫使模型在后续阶段聚焦于挖掘困难实例，从而大幅提高召回率。"
primary_logic: "HIP将检测分解为多阶段级联过程：每阶段排除已检测的简单样本，让模型集中处理前一阶段的假阴性。同时，盒子级别的可变形Transformer解码器结合RoIAlign上下文建模，能够在高召回候选集合中高效滤除假阳性，最终实现高精度与高召回。"
claims:
- "HIP多阶段热图编码器显著提升初始候选召回率，FocalFormer3D-200P达到75.2 mAR，比TransFusion-L高出4.5个点；使用600 queries时mAR达79.2，超越DeepInteraction 6.6个点。"
- "在nuScenes LiDAR测试集上，FocalFormer3D单模型取得68.7 mAP与72.6 NDS，均超过之前最优的TransFusion-L（+3.2 mAP, +2.4 NDS）和LiDARMultiNet（+1.7 mAP, +1.0 NDS）。"
- "Pooling-based masking策略（小物体中心点、大物体3×3核）在所有掩模方案中表现最佳，带来+1.2 mAP和+0.7 NDS的增益。"
- "盒级查询与Box-pooling模块显著提升查询质量，在deformable decoder中带来+0.6 mAP的提升，且仅增加3.7ms延迟。"
---

# FocalFormer3D : Focusing on Hard Instance for 3D Object Detection

> [!tip] 核心洞察
> HIP将检测分解为多阶段级联过程：每阶段排除已检测的简单样本，让模型集中处理前一阶段的假阴性。同时，盒子级别的可变形Transformer解码器结合RoIAlign上下文建模，能够在高召回候选集合中高效滤除假阳性，最终实现高精度与高召回。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FocalFormer3D：聚焦困难实例的3D目标检测 |
| 英文题名 | FocalFormer3D : Focusing on Hard Instance for 3D Object Detection |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2308.04556) · [GitHub](https://github.com/NVlabs/FocalFormer3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FocalFormer3D |
| Dataset | nuScenes test set (LiDAR), nuScenes test set (Multi-modal), nuScenes test set (Multi-modal with TTA), nuScenes tracking test set (LiDAR) |

> [!tip] 效果简介
> - nuScenes test set (LiDAR) 上，mAP / NDS 为 68.7 / 72.6，对比 TransFusion-L 65.5 / 70.2，变化 +3.2 mAP / +2.4 NDS。
> - nuScenes test set (Multi-modal) 上，mAP / NDS 为 71.6 / 73.9，对比 DeepInteraction 70.8 / 73.4，变化 +0.8 mAP / +0.5 NDS。
> - nuScenes test set (Multi-modal with TTA) 上，mAP / NDS 为 72.9 / 75.0，对比 LargeKernel3D-F 71.1 / 74.2 (previous best single model)，变化 +1.8 mAP / +0.8 NDS。

## 概要

### 问题瓶颈

现有基于鸟瞰图（BEV）的3D目标检测器在自动驾驶场景中面临一个关键瓶颈：对由遮挡、背景杂乱等引起的**假阴性（False Negatives）** 处理不足。主流方法如**CenterPoint**和**TransFusion-L**采用单阶段中心热图预测，倾向于召回容易检测的样本，却系统性地忽略了那些难以匹配的困难实例，导致关键目标漏检风险高，直接威胁下游安全。

### 核心方法

本文提出**FocalFormer3D**，其核心机制为**困难实例探测（Hard Instance Probing, HIP）**——一种多阶段级联流水线，自动识别并聚焦于假阴性目标。方法包含两大创新组件：

- **多阶段热图编码器与累积正掩模**：逐阶段生成BEV中心热图，通过类别感知的累积正掩模（Accumulated Positive Mask）排除前期已检测的容易正样本，迫使模型在后续阶段专门挖掘前一阶段遗留的假阴性。掩模策略上，采用池化式掩模（小物体掩蔽中心点，大物体使用3×3核），在各类掩模方案中表现最优。
- **盒级可变形Transformer解码器**：将多阶段收集的高召回候选表示为盒级查询（而非点级查询），通过RoIAlign提取7×7网格的盒子上下文特征增强查询嵌入，并利用可变形注意力进行迭代盒细化，在庞大候选集合中高效滤除假阳性。

HIP将检测分解为“逐阶段排除已检测样本→聚焦困难实例”的级联过程，实现了高召回与高精度的统一。

### 主要结果

在nuScenes LiDAR测试集上，FocalFormer3D单模型取得**68.7 mAP / 72.6 NDS**，超越此前最优的TransFusion-L（+3.2 mAP / +2.4 NDS）。多模态变体配合测试时增强达到**72.9 mAP / 75.0 NDS**，位列排行榜第一。在nuScenes跟踪基准上，以**72.1 AMOTA**同样占据榜首。Waymo验证集上，相比TransFusion-L提升**+1.0 mAPH**（LEVEL 2）。消融实验证实，HIP多阶段热图编码器将初始候选召回率推至**79.2 mAR**（600 queries），远超DeepInteraction 6.6个点；盒级查询与Box-pooling模块带来**+0.6 mAP**增益，仅增加3.7ms延迟。在保持高精度的同时，FocalFormer3D-F推理延迟（363ms）远低于BEVFusion（1610ms）和DeepInteraction（480ms）。

### 方法谱系与知识库定位

FocalFormer3D立足于基于BEV的3D目标检测范式，继承了**CenterPoint**的中心热图表示和**TransFusion-L**的二阶段细化思路，但在两个关键维度上实现了突破：

- **候选生成机制**：从单阶段热图预测升级为HIP驱动的多阶段热图编码，通过累积正掩模实现困难样本的自动挖掘，填补了现有方法对假阴性系统性建模的空白。
- **查询表示与细化**：将TransFusion-L的点级交叉注意力查询替换为盒级可变形查询，引入RoIAlign上下文建模，在大量候选条件下兼顾效率与精度。

该方法在nuScenes和Waymo双基准上验证了有效性，为“高召回候选挖掘+高效假阳性滤除”的两阶段框架提供了新的设计范式。



### 3D目标检测的核心挑战

3D目标检测是自动驾驶感知系统的关键任务，要求在三维空间中精确定位和识别车辆、行人、骑行者等交通参与者。近年来，基于鸟瞰图（BEV）的检测范式成为主流——它将激光雷达点云或相机特征投影到统一的俯视平面上，通过中心热图（center heatmap）预测目标位置，再回归其三维边界框。然而，这一范式存在一个被长期忽视的结构性瓶颈：**对假阴性（False Negatives）的挖掘不足**。

假阴性是指真实存在的目标被检测器完全遗漏。在自动驾驶场景中，这类漏检往往集中在最危险的情形——被其他车辆严重遮挡的行人、密集车流中相互重叠的车辆、以及被背景杂波淹没的小尺寸交通锥。现有检测器（如 **CenterPoint** 和 **TransFusion-L**）采用单阶段热图预测，模型在一次前向传播中必须同时处理所有目标，导致其注意力资源被大量“容易样本”（大尺寸、无遮挡、特征显著的目标）占据，困难实例的响应被抑制，最终造成关键目标的漏检风险。

### 现有方法的局限

主流BEV检测器的处理流程可概括为两个阶段：首先通过骨干网络提取BEV特征，然后在热图上进行中心点预测与边框回归。这一流程存在两处关键缺口：

1. **单阶段热图预测缺乏困难样本挖掘机制**：模型没有显式的反馈回路来识别“哪些目标没被检测到”。训练时使用的Focal Loss虽然能缓解正负样本不平衡，但无法区分“容易正样本”与“困难正样本”——所有正样本在损失函数中地位平等，模型没有动力去专门攻克漏检目标。

2. **二阶段细化网络的查询表示粗糙**：TransFusion-L等方法的第二阶段使用交叉注意力解码器对候选框进行细化，但其查询嵌入仅基于中心点的单点特征，缺乏目标周围的上下文信息。这使得解码器在区分真假阳性时信息不足，难以有效滤除高召回候选集合中的假阳性。

### 本文动机

针对上述缺口，FocalFormer3D提出了一套系统性的解决方案，其核心动机源于一个朴素的观察：**检测器的召回瓶颈不在于“找不到目标”，而在于“找不到那些最难找的目标”**。如果能让模型在检测完容易目标后，自动识别遗漏的困难目标，并在后续阶段专门针对它们进行二次挖掘，就能在不牺牲精度的前提下大幅提升召回率。

这一思想被形式化为**困难实例探查（Hard Instance Probing, HIP）**策略：将检测过程分解为多个级联阶段，每阶段排除已成功检测的容易样本，迫使模型聚焦于前一阶段产生的假阴性。同时，引入**盒级可变形Transformer解码器**，利用RoIAlign从BEV特征中提取丰富的盒子上下文特征，在高召回候选集合中高效滤除假阳性，最终实现高精度与高召回的平衡。



## 核心方法与创新机理

FocalFormer3D 的核心创新在于构建了一套**“先广召、后精排”** 的级联检测范式，通过两个关键组件的协同，系统性地解决了现有 BEV 检测器对困难实例（遮挡、背景杂乱导致的假阴性）召回不足的瓶颈。

### 1. 困难实例探查（Hard Instance Probing, HIP）与累积正掩模

HIP 将传统的单阶段热图预测重构为**多阶段级联过程**，其核心机制是自动识别并聚焦于前一阶段的假阴性目标。

- **因果机制**：在每个阶段 $k$，模型生成一组正样本预测 $\mathcal{P}_k$。通过目标分配，可确定被匹配的真值目标 $\mathcal{O}_k^{TP}$。那些在所有前 $k$ 阶段均未被匹配的真值目标 $\mathcal{O}_k^{FN} = \mathcal{O} - \bigcup_{i=1}^k \mathcal{O}_k^{TP}$ 即被定义为**困难实例**。后续阶段的核心任务就是挖掘这些遗漏目标。
- **实现方式**：引入**累积正掩模（Accumulated Positive Mask）** $\hat{M}_k = \max_{1 \leq i \leq k} M_i$，这是一个类别感知的二值掩模，记录前 $k$ 阶段已检测到的容易正样本位置。通过将当前阶段热图与掩模取反相乘 $\hat{S}_k = S_k \cdot (1 - \hat{M}_k)$，模型在训练和推理时均被强制忽略已召回区域，从而将注意力集中于挖掘困难实例。
- **正掩模策略**：采用**池化式掩模（Pooling-based Masking）**——小物体仅掩蔽中心点，大物体使用 $3 \times 3$ 核掩蔽。消融实验（Table 5）表明，该策略优于点掩模和盒子掩模，带来 **+1.2 mAP / +0.7 NDS** 的增益。
- **效果**：HIP 大幅提升了初始候选的召回率。FocalFormer3D-200P 达到 75.2 mAR，超越 TransFusion-L 4.5 个点；使用 600 queries 时 mAR 达 79.2，超越 DeepInteraction 6.6 个点（Figure 5）。

### 2. 盒子级可变形解码器与 Box-pooling 模块

HIP 产生的高召回候选集合中必然混入大量假阳性，需要一个强大的二阶段细化网络进行甄别。

- **盒子级查询表示**：区别于 CenterPoint 的点级查询或 TransFusion 的交叉注意力查询，FocalFormer3D 将候选对象建模为**盒子级查询（box-level queries）**。通过 **Box-pooling 模块**，利用 RoIAlign 从 BEV 特征中提取 $7 \times 7$ 网格的盒子上下文特征，增强查询嵌入。这一轻量设计仅增加 3.7ms 延迟，却带来 **+0.6 mAP** 的提升（Table 8）。
- **可变形注意力解码器**：采用可变形 Transformer 解码器对盒子级查询进行迭代细化。可变形注意力在处理大量查询（600 queries）时效率显著优于标准交叉注意力，且 6 层解码器配合盒子级查询可达到最优精度-延迟平衡（Table 8）。
- **重评分机制（Rescoring）**：收集所有阶段的候选对象，利用解码器的预测分数进行重评分，最终选出高精度检测结果。

### 3. 创新点总结

| 改进槽位 | 基线方法 | FocalFormer3D |
|---------|---------|---------------|
| 候选生成 | 单阶段中心热图预测 | 多阶段 HIP + 累积正掩模 |
| 正样本抑制 | 无掩模 / 单点掩模 | 类别感知池化式掩模 |
| 二阶段细化 | 交叉注意力 / 点级回归 | 可变形解码器 + 盒子级 RoIAlign 查询 |
| 查询表示 | 点级特征 | 盒子级上下文增强嵌入 |

HIP 与盒子级解码器的组合形成了“高召回候选生成 + 高精度假阳性滤除”的闭环：HIP 确保困难实例不被遗漏，盒子级解码器则利用丰富的空间上下文有效甄别假阳性。二者协同，使 FocalFormer3D 在 nuScenes LiDAR 测试集上以单模型取得 **68.7 mAP / 72.6 NDS**，较此前最优的 TransFusion-L 提升 **+3.2 mAP / +2.4 NDS**。



![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of FocalFormer3D. The overall framework comprises two novel components: a multi-stage heatmap encoder network that uses the Hard Instance Probing (HIP) strategy to produce high-recall object queries (candidates), and a deformableHeatmap Predictions True Positives False Negatives Masked Obje transformer decoder network with rescoring mechanism that is responsible for eliminating false positives from the large set of candidates. (a) Following feature extraction from modalities, the map-view features produce a set of multi-stage BEV features and then BEV heatmaps. The positive mask accumulates to exclude the easy positive candidates of prior stages from BEV heatmaps. The l...*

FocalFormer3D 的整体架构遵循“高召回候选生成 + 高质量候选过滤”的两阶段范式，其核心由**多阶段热图编码器（Multi-stage Heatmap Encoder）**与**盒级可变形Transformer解码器（Box-level Deformable Decoder）**两大组件串联构成（Figure 2）。输入点云首先经过 VoxelNet 骨干网络（CenterPoint-Voxel）提取多尺度 BEV 特征，随后进入 Hard Instance Probing（HIP）流水线生成高召回的目标候选集合，最终由解码器对候选进行迭代细化和重评分，输出精确的 3D 检测框。

### 1. 多阶段热图编码器与 HIP 流水线

该模块是系统实现高召回的核心。与传统的单阶段中心热图预测（如 CenterPoint、TransFusion）不同，FocalFormer3D 将候选生成分解为 $K$ 个级联阶段（默认 $K=3$）。其工作机制如下：

- **阶段式热图预测**：每个阶段 $k$ 从 BEV 特征中预测类别感知的热图 $S_k$，并通过 Top-K 选择产生一组正样本预测 $\mathcal{P}_k$。
- **累积正掩模（Accumulated Positive Mask, APM）**：系统维护一个类别感知的二值掩模 $\hat{M}_k = \max_{1 \leq i \leq k} M_i$，记录前 $k$ 个阶段已检测到的“容易”正样本位置。当前阶段的热图被掩蔽为 $\hat{S}_k = S_k \cdot (1 - \hat{M}_k)$，从而强制模型忽略已召回目标，聚焦于前一阶段的假阴性（即困难实例）。
- **假阴性自动挖掘**：在训练中，未被 $\mathcal{P}_k$ 匹配的真值目标 $\mathcal{O}_k^{FN} = \mathcal{O} - \bigcup_{i=1}^k \mathcal{O}_i^{TP}$ 被显式建模为困难实例，成为后续阶段的主要学习目标（Figure 1, Figure 3）。
- **候选收集**：所有阶段的热图响应被汇总，形成初始目标候选集合。消融实验（Table 4）表明，3 阶段、总计 600 个查询的配置在召回与精度间取得最优平衡（66.5 mAP / 71.1 NDS）。

### 2. 盒级可变形解码器与重评分

HIP 流水线产生的高召回候选集合中不可避免地混入大量假阳性，因此需要一个强力的二阶段细化网络进行过滤。FocalFormer3D 采用可变形Transformer解码器，并在查询表示和注意力机制上做了针对性设计：

- **盒级查询嵌入（Box-level Query）**：区别于以往基于中心点特征的查询方式，FocalFormer3D 将每个候选建模为盒级查询。通过 **Box-pooling 模块**，利用 RoIAlign 从 BEV 特征中提取 $7 \times 7$ 的局部上下文网格特征，增强查询嵌入的表达能力。该模块仅增加 3.7ms 延迟，带来 +0.6 mAP 的稳定增益（Table 6, Table 8）。
- **可变形交叉注意力**：解码器使用可变形注意力在 BEV 特征图上进行稀疏采样，相比标准交叉注意力在处理大量查询时效率更高。6 层解码器配合迭代盒细化策略，逐步修正候选框的位置和尺寸。
- **重评分策略（Rescoring Strategy）**：解码器对所有阶段收集的候选进行重新评分，最终依据预测置信度筛选出高质量检测结果，有效抑制假阳性。

### 3. 数据流与模块衔接

整体数据流可概括为：**点云 → VoxelNet BEV 特征 → 多阶段热图编码器（HIP + APM）→ 高召回候选集合 → Box-pooling 查询增强 → 可变形解码器迭代细化 → 重评分输出**。Figure 2 清晰展示了各模块间的输入输出关系，其中残差连接和归一化层在图中被省略以保持清晰性。Table 6 的逐步消融实验验证了该流水线中各模块的增量贡献：在基线模型上依次加入多阶段热图编码器（M.S. Heat）、可变形交叉注意力（C.A.）和 Box-pooling 模块（BoxPool），性能从单阶段基线逐步提升至 66.5 mAP / 71.1 NDS。



### 3.1 困难实例探针（Hard Instance Probing, HIP）的形式化

HIP 的核心思想是将检测过程分解为多阶段级联，每一阶段自动识别并聚焦于前一阶段遗漏的假阴性（False Negatives, FN）目标。其形式化定义如下：

设全体真值目标集合为 $\mathcal{O} = \{ o_i, i=1,2,\ldots \}$。在第 $k$ 阶段，模型生成一组正样本预测 $\mathcal{P}_k = \{ p_i, i=1,2,\ldots \}$。通过匹配度量 $\sigma$ 和阈值 $\eta$，可确定该阶段命中的真值目标集合（True Positive ground-truth）：

$$\mathcal{O}_k^{TP} = \left\{ o_j \middle| \exists p_i \in \mathcal{P}_k, \sigma(p_i, o_j) > \eta \right\}$$

经过前 $k$ 阶段后，仍未匹配的真值目标即构成困难实例（False Negative ground-truth）：

$$\mathcal{O}_k^{FN} = \mathcal{O} - \bigcup_{i=1}^k \mathcal{O}_k^{TP}$$

这一机制使得后续阶段的目标函数天然聚焦于 $\mathcal{O}_k^{FN}$，无需额外的手工难例挖掘策略。

### 3.2 多阶段热图编码器与累积正掩模

多阶段热图编码器是 HIP 的具体实现载体。其核心操作是通过**累积正掩模（Accumulated Positive Mask, APM）** 在 BEV 热图上抑制已检测的容易正样本，迫使模型在后续阶段关注困难实例。

**正掩模生成**：在第 $k$ 阶段，根据正样本预测 $\mathcal{P}_k$ 生成类别感知的二值掩模 $M_k \in \{0,1\}^{X \times Y \times C}$，其中 $X \times Y$ 为 BEV 特征图尺寸，$C$ 为类别数。掩模策略经消融验证，**池化掩模（Pooling-based Masking）** 表现最优（Table 5：+1.2 mAP / +0.7 NDS）：小物体仅掩蔽中心点，大物体（如卡车、公交车）使用 $3 \times 3$ 核掩蔽。

**累积正掩模**：通过对前 $k$ 阶段的正掩模逐元素取最大值，得到累积掩模：

$$\hat{M}_k = \max_{1 \leq i \leq k} M_i$$

**热图掩蔽**：将当前阶段的热图 $S_k$ 与累积掩模的补集逐元素相乘，实现容易正样本区域的响应置零：

$$\hat{S}_k = S_k \cdot (1 - \hat{M}_k)$$

在 $\hat{S}_k$ 上进行 Top-K 选择，即可生成聚焦于困难实例的候选目标集合。所有阶段的候选被统一收集，作为后续解码器的初始查询。

### 3.3 盒子级可变形解码器与 Box-pooling 模块

为从高召回候选集中高效滤除假阳性，FocalFormer3D 采用盒子级可变形 Transformer 解码器进行二阶段细化。

**盒子级查询表示**：区别于 CenterPoint 等方法的点级查询（仅使用热图峰值点特征），FocalFormer3D 将每个候选目标建模为盒子级查询。通过 **Box-pooling 模块**，利用 RoIAlign 从 BEV 特征中提取 $7 \times 7$ 网格的盒子上下文特征，增强查询嵌入。消融实验表明（Table 8），盒级查询相比点级查询带来 +0.6 mAP 的提升，仅增加 3.7ms 延迟。

**可变形交叉注意力**：解码器采用可变形注意力机制，使查询仅与 BEV 特征图中预测框周围的局部区域交互。这种局部范围的细化方式在大量查询场景下效率优于标准交叉注意力（Table 8），且通过迭代盒子细化逐步提升定位精度。

**重评分策略**：解码器对来自所有阶段的候选目标进行统一重评分，最终选出高置信度预测，有效抑制假阳性。



## 实验与关键发现

### 核心性能验证

FocalFormer3D 在多个主流自动驾驶感知基准上取得领先性能。在 nuScenes LiDAR 测试集上，单模型取得 **68.7 mAP** 与 **72.6 NDS**，较此前最优的 TransFusion-L 分别提升 **+3.2 mAP** 与 **+2.4 NDS**（Table 1）。多模态变体 FocalFormer3D-F 配合测试时增强（TTA）达到 **72.9 mAP / 75.0 NDS**，刷新该榜单单模型纪录（Table 1）。在 nuScenes 3D 跟踪测试集上，LiDAR 版本取得 **71.5 AMOTA**（TTA 下 72.1），较 TransFusion-L 提升 **+2.9 AMOTA**（Table 2）。在 Waymo 验证集上，单帧点云输入下取得 **71.5 mAPH（LEVEL 2）**，超出 TransFusion-L 1.0 个点（Table 3）。上述结果一致验证了 HIP 多阶段流水线在提升召回与精度方面的有效性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on the nuScenes 3D detection test set. † represents using flipping test-time augmentation. ‡ means using both flipping and rotation test-time augmentation. C.V, Motor., Ped. and T.C. are short for construction vehicle, motorcycle, pedestrian, and traffic cones, respectively*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/007_Table_2.jpg]]
*Table 2: Performance comparison on nuScenes 3D tracking test set. † is based on the double-flip testing results in Table 1. ‡ is based on model ensembling. Table 3. Performance comparison on the Waymo val set. All models inputs single-frame point clouds. The methods marked with ∗ indicate the utilization of different point cloud backbones in VoxelNet. The method marked with ∧ indicates our reproduction. The evaluation metric used is the LEVEL 2 difficulty, and the results are reported on the full Waymo validation set*

### 召回率分析

HIP 的核心价值在于显著提升初始候选召回率。Figure 5 显示，FocalFormer3D-200P 达到 **75.2 mAR**，比 TransFusion-L 高出 **+4.5 mAR**；使用 600 queries 时 mAR 进一步升至 **79.2**，超越 DeepInteraction 6.6 个点。分种类召回对比（Figure 6）表明，FocalFormer3D 在 Construction Vehicle、Trailer 等困难类别上的召回优势尤为突出，这直接源于多阶段热图编码器对假阴性的逐步挖掘。

### 消融实验

**多阶段与查询数**（Table 4）：单阶段基线（无 HIP）性能有限；引入 3 阶段 HIP 并总计使用 600 个查询时达到最优 **66.5 mAP / 71.1 NDS**，验证了多阶段假阴性挖掘的必要性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/011_Table_4.jpg]]
*Table 4: Effects of numbers of stages and total queries. Here one stage stands for the baseline method without using hard instance probing. Table 5. Effects of various positive mask types. All models adopt the same network except for the masking way*

**正掩模策略**（Table 5）：对比点掩模、盒子掩模与池化掩模，**Pooling-based masking**（小物体中心点、大物体 3×3 核）表现最佳，带来 **+1.2 mAP / +0.7 NDS** 的增益。这表明类别感知的局部区域抑制能更精确地排除容易正样本，同时避免过度掩蔽。

**模块增量贡献**（Table 6）：在基线基础上依次加入多阶段热图编码器（M.S. Heat）、可变形交叉注意力（C.A.）与 Box-pooling 模块（BoxPool），性能逐步攀升至 66.5 mAP / 71.1 NDS。其中 Box-pooling 以仅 **3.7ms** 的额外延迟带来 **+0.6 mAP** 提升（Table 8），证明了盒级 RoIAlign 特征对查询嵌入的增强作用。

**解码器设计**（Table 8）：可变形注意力在大量查询场景下效率优于标准交叉注意力；6 层 deformable decoder 配合盒级查询取得最优精度，且延迟可控。

### 效率分析

FocalFormer3D-F 在保持高精度的同时，推理延迟为 **363ms**（单 V100 GPU），远低于 BEVFusion（1610ms）和 DeepInteraction（480ms）（Table 9）。多阶段热图编码器仅增加 13ms 开销（Table 7），以微小计算代价换取大幅召回提升。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/012_Table_7.jpg]]
*Table 7: Latency analysis for model components. Latency is measured on a V100 GPU for reference*

### 失败模式与局限

尽管 HIP 显著提升召回，第二阶段的盒子级细化具有有限的回归范围，难以大幅修正初始热图的位置错误，尤其是远距离目标。Figure 9 展示了部分失败案例，主要涉及远距离小目标或严重遮挡场景下的定位偏差。此外，HIP 依赖 BEV 中心热图的高斯峰值假设，可能不直接适用于无明确鸟瞰图的纯视觉检测器。多模态变体仅采用较简单的投影融合，未集成更先进的融合技术（如 LSS 或深层交互），其融合潜力尚未充分挖掘。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/021_Figure_9.jpg]]
*Figure 9: Visual results and failure cases. The green boxes represent the ground truth objects and the blue ones stand for our predictions. We recommend zooming in on the figure for best viewing*

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | LiDAR 单模型 68.7 mAP / 72.6 NDS，多模态 TTA 72.9 mAP / 75.0 NDS |
| Table 2 | 跟踪 AMOTA 71.5（TTA 72.1），领先 TransFusion-L 2.9 点 |
| Table 3 | Waymo val mAPH 71.5，超越 TransFusion-L 1.0 点 |
| Figure 5 | HIP 初始召回 79.2 mAR，超越 DeepInteraction 6.6 点 |
| Table 4 | 3 阶段 600 queries 最优，验证多阶段假阴性挖掘必要 |
| Table 5 | Pooling-based masking 最优，+1.2 mAP / +0.7 NDS |
| Table 6 | 模块增量验证：M.S. Heat → C.A. → BoxPool 逐步提升 |
| Table 9 | 363ms 推理延迟，效率优于 BEVFusion 与 DeepInteraction |

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/001_Figure_1.jpg]]
*Figure 1: Visual example for Hard Instance Probing (HIP). By utilizing this multi-stage prediction approach, our model can progressively focus on hard instances and facilitate its ability to gradually detect them. At each stage, the model generates some Positive object candidates (represented by green circles). Object candidates assigned to the ground-truth objects can be classified as either True Positives (TP, represented by green boxes) and False Negatives (FN, represented by red boxes) during training. We explicitly model the unmatched ground-truth objects as the hard instances, which become the main targets for the subsequent stage. Conversely, Positives are considered easy samples (represented...*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/018_Figure_7.jpg]]
*Figure 7: Object center shifts ( $\delta _ { x } , \delta _ { y }$ ) distribution without normalization between initial heatmap response and final object predictions. The unit is a meter

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/020_Figure_8.jpg]]
*Figure 8: Example visualization of multi-stage heatmap encoder process on the bird’s eye view. The process of identifying false negatives operates stage by stage. We show different categories with different colors for visualization. The top three subfigures display the ground-truth center heatmaps at each stage, highlighting the missed object detections. The two subfigures below display the positive mask that shows positive object predictions. The scene ids are ”4de831d46edf46d084ac2cecf682b11a” and ”825a9083e9fc466ca6fdb4bb75a95449” from the nuScenes val set. We recommend zooming in on the figure for best viewing*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2308_04556/figures/010_Table.jpg]]



## 定位与知识库关联

### 1. 核心瓶颈与设计动机

FocalFormer3D 针对的是当前基于 BEV（Bird's Eye View）的 3D 目标检测器在召回率上的根本性缺陷：现有方法对由遮挡、背景杂乱等引起的**假阴性（False Negatives）** 处理不足，导致自动驾驶场景中关键目标（如行人、骑行者）的漏检风险极高。典型的单阶段热图预测器（如 **CenterPoint**）在生成候选目标时，倾向于优先响应“容易”的样本，而忽略那些特征响应较弱的困难实例。FocalFormer3D 的因果旋钮在于 **Hard Instance Probing (HIP)** 多阶段流水线：它通过自动识别前一阶段未匹配的真值目标（即假阴性），并利用**累积正掩模（Accumulated Positive Mask）** 在后续阶段的 BEV 热图上显式抑制已检测的容易样本，迫使模型集中计算资源挖掘困难实例，从而大幅提升初始候选集的召回率。

### 2. 与基线方法的差异对比

FocalFormer3D 在方法谱系上属于**基于 BEV 热图的多阶段级联检测器**，其设计在三个关键槽位上与主流基线形成了清晰的差异化：

| 方法槽位 | 基线方法（代表工作） | FocalFormer3D 的改进 | 证据锚点 |
|---|---|---|---|
| **候选生成** | 单阶段中心热图预测（**CenterPoint**；**TransFusion-L**） | 多阶段热图预测 + HIP 机制，通过累积正掩模逐阶段挖掘假阴性 | Section 3.2; Fig. 2(a) |
| **正样本掩模策略** | 无掩模 / 单点抑制 | 类别感知的池化掩模（小物体中心点，大物体 3×3 核），在排除容易样本的同时保留困难样本的响应空间 | Section 3.2; Table 5 |
| **二阶段细化** | 交叉注意力解码器（**TransFusion-L**）或点级框回归（**CenterPoint**） | 盒级可变形 Transformer 解码器，配合 RoIAlign 盒子池化模块提取 7×7 网格上下文特征，实现迭代框细化 | Section 3.3; Table 6, Table 8 |

具体而言：
- **TransFusion-L** 采用交叉注意力 Transformer 进行二阶段细化，但其查询嵌入基于点级特征，缺乏对目标盒级上下文的显式建模。FocalFormer3D 的盒级查询嵌入（通过 Box-pooling 模块从 BEV 特征中提取 RoIAlign 特征）带来了 +0.6 mAP 的提升，仅增加 3.7ms 延迟（Table 8）。
- **CenterPoint** 的单阶段热图预测无法显式区分容易样本与困难样本。FocalFormer3D 的三阶段 HIP 编码器将初始候选召回率（mAR）推至 79.2（600 queries），超越 **DeepInteraction** 6.6 个点（Figure 5）。
- **BEVFusion** 和 **DeepInteraction** 等多模态检测器侧重于多传感器深度融合，而 FocalFormer3D 的多模态变体仅使用较简单的投影和交叉注意力融合，其性能增益（72.9 mAP / 75.0 NDS，Table 1）更多来自 HIP 对候选质量的提升，而非融合技术的创新。

### 3. 适用边界与泛化能力

FocalFormer3D 的核心机制（HIP 与累积正掩模）具有较强的通用性，但其适用边界受限于以下条件：

1. **BEV 热图的依赖性**：HIP 机制建立在 BEV 中心热图的高斯峰值假设之上——即目标的存在性由热图上的局部极大值表征。这一假设在基于 LiDAR 或融合 BEV 特征的检测器中自然成立，但可能不直接适用于无明确鸟瞰图的纯视觉检测器（如基于透视图像的直接 3D 预测）。若要将 HIP 推广至摄像头检测器，可能需要重新设计正掩模策略，例如在深度估计空间中定义“容易样本”的抑制区域。

2. **二阶段细化的局部性约束**：盒级可变形解码器的回归范围有限（预测局部性），难以大幅修正初始热图的位置错误。Figure 7 显示初始热图响应中心与最终预测框中心之间的偏移分布，表明对于远距离目标或严重遮挡目标，初始候选的位置偏差可能超出细化网络的修正能力。这一限制在 Waymo 数据集的长距离检测场景中可能更为显著。

3. **多阶段设计的固定性**：当前 HIP 的阶段数（3 阶段）和每阶段查询数（200 queries）是固定的超参数（Table 4 消融实验验证了该配置的最优性），未根据场景复杂度或目标密度动态调整。在目标稀疏的高速公路场景中，固定三阶段可能引入冗余计算；在目标密集的城市交叉路口，三阶段可能仍不足以覆盖所有困难实例。

4. **两阶段训练的次优性**：模型采用分离式训练策略——先训练骨干网络和解码器，再训练多阶段热图编码器。这种非端到端的联合优化可能导致特征表示与 HIP 机制之间的不协调，限制整体性能的上限。

5. **时序信息的缺失**：在 Waymo 验证集上，FocalFormer3D 仅使用单帧点云（Table 3），未利用时序信息。对于运动速度较快的物体（如车辆），时序上下文可能提供额外的运动线索，有助于进一步提升检测和跟踪性能。

### 4. 局限性与开放问题

**已知局限**：
- **长距离回归能力不足**：二阶段盒级细化对初始热图位置偏差的容忍度有限，远距离目标的检测精度可能受限于第一阶段候选的质量。
- **多模态融合的浅层性**：多模态变体未集成先进的融合技术（如 BEVFusion 的 LSS 投影或 DeepInteraction 的深层交互），其在复杂融合场景下的潜力尚未挖掘。
- **计算开销的线性增长**：HIP 的阶段数增加会线性提升热图编码器的延迟（Table 7 显示多阶段热图编码器耗时 13ms），在实时性要求极高的车载部署中可能需要进一步优化。

**开放问题**（需人工验证）：
1. HIP 策略能否推广到基于摄像头的 3D 检测器？是否需要设计新的正掩模策略以适应透视空间？
2. 如何扩展二阶段盒子细化网络的回归范围，以支持长距离的位置修正和朝向修正？
3. 多阶段热图编码器的阶段数和每阶段查询数是否可以根据场景复杂度和目标密度动态调整（如基于 BEV 特征的稀疏性自适应分配查询）？
4. 累积正掩模的类别感知设计在目标密集、存在类内重叠时是否仍然有效？是否需要更高级的 NMS 或注意力掩模来避免过度抑制？
5. FocalFormer3D 在实时自动驾驶系统上的部署效率如何？能否通过模型剪枝、量化等手段进一步降低延迟（当前单模型 109ms，Table 7）？
6. 将 HIP 与更强的多模态融合技术（如 BEVFusion 的 LSS、DeepInteraction 的深层交互）结合，是否能带来更大的性能增益？初步证据（FocalFormer3D-F 多模态变体 72.9 mAP）表明融合方向仍有提升空间。



## 原文 PDF

![[paperPDFs/ICCV_2023/FocalFormer3D_Focusing_on_Hard_Instance_for_3D_Object_Detection.pdf]]

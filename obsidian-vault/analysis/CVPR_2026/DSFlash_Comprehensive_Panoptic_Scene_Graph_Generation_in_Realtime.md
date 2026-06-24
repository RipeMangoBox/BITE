---
title: "DSFlash: Comprehensive Panoptic Scene Graph Generation in Realtime"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DSFlash_Comprehensive_Panoptic_Scene_Graph_Generation_in_Realtime.pdf
project_link: null
code_link: null
aliases:
- DSFlash
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 全景场景图生成的推理速度由三个关键杠杆控制：(1)骨干网络效率——单一共享骨干vs.双独立骨干；(2)关系预测方向性——双向单次前向传播vs.单向两次前向传播；(3)处理token数量——基于掩码的patch剪枝vs.全量处理。这三个杠杆直接决定模型延迟，且通过消融实验验证了各自独立贡献。
primary_logic: DSFlash的核心洞察是将分割与关系预测的特征提取统一到单一冻结的EoMT骨干网络中，复用分割阶段已产生的特征张量，并利用门控机制在单次前向传播中同时预测两个方向的关系。此外，基于掩码重叠率动态剪枝无关patch，以最小开销进一步减少计算量。这三个设计相互协同，使得DSFlash在PSG数据集上能以仅50ms延迟(L版本)达到30.90 mR@50，超越DSFormer的28.9 mR@50(98ms延迟)。
claims:
- 统一骨干网络将两个独立分割模型替换为单一高效模型，是最有效的延迟优化手段
- 双向门控关系预测将所需前向传播次数减半，同时将mR@50从25.0提升至28.8
- 基于掩码的动态patch剪枝将GTX 1080上的延迟从230ms降至205ms，mR@50仅下降2.13
- DSFlash-L在PSG数据集上以50ms延迟达到30.90 mR@50，超越DSFormer的28.9 mR@50(98ms延迟)
---

# DSFlash: Comprehensive Panoptic Scene Graph Generation in Realtime

> [!tip] 核心洞察
> DSFlash的核心洞察是将分割与关系预测的特征提取统一到单一冻结的EoMT骨干网络中，复用分割阶段已产生的特征张量，并利用门控机制在单次前向传播中同时预测两个方向的关系。此外，基于掩码重叠率动态剪枝无关patch，以最小开销进一步减少计算量。这三个设计相互协同，使得DSFlash在PSG数据集上能以仅50ms延迟(L版本)达到30.90 mR@50，超越DSFormer的28.9 mR@50(98ms延迟)。

| 字段 | 内容 |
|------|------|
| 中文题名 | DSFlash：面向实时全景场景图生成的综合模型 |
| 英文题名 | DSFlash: Comprehensive Panoptic Scene Graph Generation in Realtime |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10538) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | DSFlash |
| Dataset | PSG dataset |

> [!tip] 效果简介
> - PSG dataset (SGDet/SGGen) 上，mR@50 / 延迟(ms) DSFlash-L: 30.90 / 50ms vs DSFormer: 28.9 / 98ms (mR@50 +2.0, 延迟减半(-49%))；mR@50 / 延迟(ms) DSFlash-B: 28.80 / 29ms vs DSFormer: 28.9 / 98ms (mR@50持平(-0.1), 延迟降低70%)；mR@50 / 延迟(ms) DSFlash-S*: 25.05 / 18ms vs DSFormer: 28.9 / 98ms (mR@50 -3.85, 延迟降低82%)。
> - PSG dataset (PredCls) 上，mR@50 DSFlash-L: 41.69 vs DSFlash-B: 41.30 (同族对比) (+0.39)。

## 概述

全景场景图生成（Panoptic Scene Graph Generation, PSGG）旨在同时定位图像中所有实例并分类其间的所有潜在关系，为视觉理解提供结构化的场景表示。然而，现有方法在实时推理场景中面临三重效率瓶颈：**（1）分割与关系预测依赖独立骨干网络，导致重复特征提取；（2）关系分类需两次前向传播分别处理主体→客体和客体→主体两个方向；（3）Transformer颈部无差别处理所有图像patch，包括大量与主体/客体无关的背景区域，造成严重计算浪费**。以当前SOTA方法**DSFormer**（Lorenz et al., ECCV 2024）为例，其在PSG数据集上虽达到28.9 mR@50，但延迟高达98ms，难以满足实时视频流处理需求。

DSFlash的核心洞察在于**将分割与关系预测的特征提取统一到单一冻结的EoMT骨干网络中，复用分割阶段已产生的特征张量，并通过门控机制在单次前向传播中同时预测两个方向的关系**。此外，基于掩码重叠率动态剪枝无关patch，以最小开销进一步压缩计算量。这三个设计杠杆——共享骨干、双向单次预测、token剪枝——相互协同，使DSFlash在PSG数据集上以仅50ms延迟（L版本）达到30.90 mR@50，性能超越DSFormer的同时延迟减半（-49%）；轻量版DSFlash-B更以29ms延迟实现28.80 mR@50，延迟降低70%而精度持平。

在方法谱系上，DSFlash继承了两阶段PSGG架构的基本范式，但与DSFormer等先前工作在以下关键维度形成差异化：

- **分割骨干**：以单一冻结EoMT替代DSFormer的独立MaskDINO+ResNet双网络，消除冗余特征提取。
- **关系预测方向性**：引入门控双向预测头，将两次前向传播压缩为一次，同时通过特征一致性损失（式7）强制模型对输入顺序对称。
- **掩码分辨率**：直接使用原始低分辨率掩码（160×160）计算patch重叠率，跳过双线性插值上采样步骤。
- **Token处理策略**：结合动态patch剪枝与ToMe-SD token合并，在Transformer颈部前丢弃无关token并降低注意力计算成本。

实验验证表明，统一骨干网络是最有效的单项延迟优化手段（延迟降至41ms），门控双向预测则在不增加延迟的前提下将mR@50从25.0恢复至28.8，有效补偿了骨干替换带来的精度损失。在RTX 3090上，DSFlash可实现56 FPS的视频流处理速度，训练在GTX 1080上不超过24小时即可完成。

## 背景与动机

### 全景场景图生成的任务定义

全景场景图生成（Panoptic Scene Graph Generation, PSGG）旨在从单张图像中同时完成两项任务：对所有实例进行像素级定位（全景分割），并对任意两个实例之间的语义关系进行分类。与传统的场景图生成（Scene Graph Generation, SGG）仅关注边界框级别的目标检测和关系预测不同，PSGG要求输出包含精确分割掩码的全景场景图，这使得该任务在具身智能、视觉问答和细粒度视觉理解等下游应用中具有更高的实用价值。

PSGG的形式化定义如下：给定输入图像，模型需输出一个场景图 $\mathcal{G} = \{\mathcal{M}, \mathcal{R}\}$，其中 $\mathcal{M} = \{m_1, m_2, ..., m_N\}$ 为 $N$ 个实例的分割掩码集合，$\mathcal{R} = \{(s_i, p_{ij}, o_j)\}$ 为主体 $s_i$ 与客体 $o_j$ 之间谓词 $p_{ij}$ 的三元组集合。由于任意两个实例之间都可能存在关系，PSGG需要穷举性地评估所有掩码对组合，这使得其计算复杂度随实例数量呈二次增长。

### 现有方法的效率瓶颈

当前PSGG领域的代表性方法是**DSFormer**（Lorenz et al., ECCV 2024），它采用两阶段架构：首先使用独立的分割模型（MaskDINO）提取实例掩码，再通过Transformer颈部对每对掩码进行关系分类。尽管DSFormer在PSG数据集上取得了领先的mR@50性能，但其推理过程存在三重效率瓶颈：

**瓶颈一：双骨干网络的冗余计算。** DSFormer使用两个独立的骨干网络——一个用于分割（MaskDINO），另一个用于关系预测的特征提取（ResNet）。这意味着每张输入图像需要经过两次完整的前向传播，产生了大量重复的特征提取计算。这一设计在追求高精度时是合理的，但在实时推理场景下成为最主要的延迟来源。

**瓶颈二：单向关系预测的双次前向传播。** 场景图中的关系具有方向性——例如“人骑马”和“马骑人”是两个不同的谓词。DSFormer的关系分类器设计为单向预测：一次前向传播只能预测从主体到客体（$S \rightarrow O$）的关系，需要第二次前向传播才能预测客体到主体（$O \rightarrow S$）的关系。这意味着对于每对掩码组合，Transformer颈部和关系头必须执行两次完整的前向传播，将关系预测的计算量翻倍。

**瓶颈三：背景patch的无效计算。** DSFormer将整张图像划分为 $13 \times 13 = 169$ 个patch token，全部送入Transformer颈部处理。然而，对于任意给定的主体-客体对，大量patch token与两者均无空间重叠——这些背景区域的token对关系分类几乎不提供有用信息，却占据了Transformer注意力计算的主要开销。

### 实时PSGG的动机与应用场景

上述效率瓶颈使得DSFormer在RTX 3090 GPU上的推理延迟高达98毫秒（约10 FPS），远未达到实时视频处理的需求。在自动驾驶、机器人交互和增强现实等应用中，场景理解系统需要在毫秒级延迟内完成全景场景图的构建，以支持后续的决策和规划。例如，自动驾驶车辆需要实时理解道路使用者之间的交互关系（如“车辆等待行人”），任何显著的延迟都可能导致安全风险。

### DSFlash的核心洞察

DSFlash的设计源于一个关键观察：**分割阶段已经产生的特征张量可以被关系预测阶段直接复用，无需独立的第二次特征提取。** 具体而言，现代全景分割模型（如EoMT）在生成分割掩码的过程中，已经提取了包含丰富空间和语义信息的多尺度特征图。如果关系预测模块能够直接利用这些特征，就可以从根本上消除双骨干网络带来的冗余计算。

基于这一洞察，DSFlash提出了一套协同优化策略：**(1)** 将分割与关系预测的特征提取统一到单一冻结的EoMT骨干网络中，仅执行一次图像级前向传播；**(2)** 设计门控双向关系预测机制，在单次Transformer前向传播中同时输出两个方向的关系预测；**(3)** 基于掩码重叠率动态剪枝与主体和客体均无重叠的背景patch token，进一步压缩计算量。

这三个设计相互协同：统一骨干网络消除了最耗时的重复特征提取，门控双向预测将关系分类的计算量减半，动态patch剪枝则根据每对掩码的空间分布自适应地减少处理token数量。通过消融实验（Table 2），DSFlash验证了每个优化模块的独立贡献——统一骨干网络将延迟从98ms降至41ms（降幅58%），门控双向预测进一步将延迟压缩至29ms，同时将因骨干替换而下降的mR@50从25.0恢复至28.8，接近原始DSFormer的性能水平。最终，DSFlash-L在PSG数据集上以仅50ms延迟达到30.90 mR@50，超越了DSFormer的28.9 mR@50（98ms延迟），实现了性能与速度的双重提升。

## 核心创新

DSFlash 的核心创新围绕一个中心洞察展开：**将分割与关系预测的特征提取统一到单一冻结骨干网络中，并通过门控机制和动态 token 剪枝协同消除冗余计算**。相较于当前 SOTA 方法 **DSFormer**（Lorenz et al., ECCV 2024），DSFlash 在五个关键设计槽位上进行了系统性重构，形成了“一次提取、双向预测、按需计算”的高效推理范式。

### 创新一：统一骨干网络——从“双引擎”到“单引擎”

DSFormer 的推理管线依赖两个独立网络：一个 MaskDINO 分割模型负责生成全景分割掩码，另一个 ResNet 骨干负责提取关系预测所需的视觉特征。这导致同一张图像被两次前向传播处理，产生大量重复的特征提取开销。

DSFlash 将这一架构简化为**单一冻结的 EoMT 骨干网络**：Part A 每张图像仅执行一次，同时输出多尺度特征 patch 和全景分割掩码；Part B 的关系预测模块**直接从分割模型已产生的特征张量中提取所需表示**，完全消除了第二个骨干网络。消融实验（Table 2）表明，这是最有效的单项延迟优化——将延迟从 98ms 骤降至 41ms（降幅 58%），代价是 mR@50 从 28.9 下降至 25.0。这一性能损失随后被后续创新所弥补。

### 创新二：双向门控关系预测——单次前向传播编码两个方向

传统 PSGG 方法（包括 DSFormer）对每一对（主体，客体）需要**两次独立的前向传播**：一次预测 S→O 方向，一次预测 O→S 方向。这意味着 Transformer 颈部和关系预测头被调用了两倍次数。

DSFlash 引入**门控双向预测机制**（Figure 4）：从富化特征张量 $\mathbf{x}$ 出发，通过一个小型 MLP 和 sigmoid 激活计算门控向量：

$$\mathbf{g} = \sigma(\text{gate}_{mlp}(\mathbf{x})) \in \mathbb{R}^{D}$$

利用该门控向量将 $\mathbf{x}$ 拆分为前向中间张量 $\mathbf{t}^{\rightarrow} = \mathbf{g} \odot \mathbf{x}$ 和后向中间张量 $\mathbf{t}^{\leftarrow} = (1 - \mathbf{g}) \odot \mathbf{x}$，随后由**共享参数的 MLP 关系头**分别预测两个方向的谓词 logits $\mathbf{z}^{\rightarrow}$ 和 $\mathbf{z}^{\leftarrow}$。这一设计将所需前向传播次数减半，同时通过共享关系头确保两个方向的预测对称性。

消融实验（Table 2）显示，加入门控双向预测后，mR@50 从 25.0 **恢复至 28.8**（接近原始 DSFormer 的 28.9），同时延迟从 37ms 进一步降至 29ms。为强制模型不对输入顺序产生偏差，训练时随机交换主体/客体顺序，并通过**特征一致性损失**约束中间特征的对称性：

$$\mathcal{L}_{\text{consistency}} = \frac{1}{D}\sum_{i=1}^{D}(t_i^{\rightarrow} - t_i^{\prime\leftarrow})^{2} + (t_i^{\leftarrow} - t_i^{\prime\rightarrow})^{2}$$

### 创新三：低分辨率掩码与高效掩码嵌入——跳过双线性插值

DSFormer 在计算 patch 重叠率时，需要将分割 logits 通过双线性插值上采样至图像尺寸，这一步骤计算代价高昂。DSFlash 的关键观察是：**直接使用原始低分辨率掩码（160×160）计算 13×13 patch 的重叠率，无需上采样**（Figure 3 定性对比表明低分辨率掩码仍能可靠区分主体/客体区域）。

此外，DSFormer 的掩码嵌入模块存在低效实现：每次为每对掩码重复执行 stack、split、flatten、mean 等 PyTorch 操作序列。DSFlash 将其**简化为平均池化层**，对所有掩码预计算重叠比率后按需复制，大幅减少池化调用和数据拷贝次数。

消融实验（Table 2）显示，高效掩码嵌入将延迟从 41ms 降至 37ms 且不影响 mR@50；低分辨率掩码进一步将 mR@50 提升至 30.5，延迟降至 18ms（以 DSFlash-S* 评估）。

### 创新四：动态 Patch 剪枝——丢弃无关背景 token

Transformer 颈部默认处理所有 13×13=169 个 patch token，但其中大量 patch 与主体和客体均无重叠，属于纯背景区域。DSFlash 在进入 Transformer 颈部前**动态识别并丢弃与主体和客体均无重叠的 patch token**，减少后续注意力计算量。

Table 3 显示，在 GTX 1080 上动态 patch 剪枝将延迟从 230ms 降至 205ms，mR@50 从 28.80 降至 26.67（下降约 2.13 个点）。这一性能代价可通过剪枝训练（训练时即随机丢弃 patch）部分缓解——剪枝训练使模型在评估时对剪枝保持鲁棒性，但整体 mR@50 仍低于未剪枝训练的模型（Figure 12）。

### 创新五：Token 合并——进一步压缩注意力成本

在 Transformer 层内部，DSFlash 应用 **ToMe-SD** 算法合并相似 token，降低自注意力的计算复杂度。ToMe-SD 的优势在于注意力计算后可“解合并”token，从而更好地保留分割能力。

Table 3 显示，ToMe（30%）与 patch 剪枝组合使 GTX 1080 延迟进一步降至 173ms，mR@50 为 26.51。值得注意的是，token 合并和 patch 剪枝在高端 GPU（H100/RTX 3090）上吞吐量提升有限，主要在老旧 GPU（GTX 1080）上效果显著——这表明两项优化更针对**计算受限的部署场景**。

### 创新协同效应

上述五项创新并非孤立叠加，而是形成了协同增益：统一骨干网络消除重复特征提取，低分辨率掩码和高效嵌入减少掩码处理开销，门控双向预测在单次前向传播中恢复关系预测精度，动态剪枝和 token 合并则按需裁剪计算图。最终，**DSFlash-L 在 PSG 数据集上以 50ms 延迟达到 30.90 mR@50**，超越 DSFormer 的 28.9 mR@50（98ms 延迟），实现了性能与速度的双重提升（Figure 1, Table 1）。

## 整体框架

DSFlash 采用“分割-关系预测”两阶段范式，将全景场景图生成拆解为一次图像级分割（Part A）和多次掩码对级关系预测（Part B），从而在单张 RTX 3090 上达到 56 FPS 的推理速度。其核心设计原则是**最大化特征复用**和**最小化冗余计算**，具体体现在三个层面：用单一冻结的分割骨干替代双独立网络、用双向门控预测替代两次单向前向传播、用基于掩码的动态 patch 剪枝减少 Transformer 颈部的 token 数量。

### Part A：图像级全景分割

每张图像仅执行一次 Part A。DSFlash 使用预训练的 **EoMT** 骨干网络，该骨干在整个训练过程中保持冻结，不参与梯度更新。EoMT 同时完成两项任务：

1. **提取多尺度特征 patch**：将输入图像编码为 $13 \times 13$ 的特征 patch 网格，作为后续关系预测的共享特征基础。
2. **预测全景分割掩码**：输出一组全面的分割掩码，定位图像中所有实例和背景区域。

这一设计的关键优势在于：分割阶段已经产生的特征张量可以直接被关系预测阶段复用，无需像 **DSFormer**（Lorenz et al., ECCV 2024）那样额外运行一个独立的 ResNet 骨干来提取关系预测所需的视觉特征。

### Part B：掩码对级关系预测

Part B 对 Part A 输出的每一对分割掩码组合执行关系预测。其处理流程如下：

1. **掩码嵌入（Mask Embedding）**：对于每对主体-客体掩码，计算每个 $13 \times 13$ patch 与掩码的重叠比例 $r_s$ 和 $r_o$，然后按式 (1) 将主体、客体和背景的可学习 token 加权添加到特征 patch 中：
   $$\text{token} = \text{patch} + \mathbf{r}_s \cdot \mathbf{t}_s + \mathbf{r}_o \cdot \mathbf{t}_o + (1 - \mathbf{r}_s - \mathbf{r}_o) \cdot \mathbf{t}_{bg}$$
   这一步骤编码了主体和客体的空间位置信息，使后续 Transformer 能够感知“谁在哪里”。

2. **动态 Patch 剪枝（可选）**：在进入 Transformer 颈部之前，识别并丢弃与主体和客体均无重叠的 patch token。由于大量背景 patch 对关系预测没有贡献，剪枝能有效减少后续计算量。

3. **Transformer 颈部处理**：富化后的 patch token 经过多层 Transformer 块进行上下文建模。可选地应用 **ToMe-SD** token 合并机制，在注意力计算前合并相似 token 以进一步降低计算开销。

4. **双向关系预测头**：这是 DSFlash 的核心创新之一。Transformer 颈部输出的特征张量 $\mathbf{x}$ 首先通过一个小型 MLP 和 sigmoid 激活计算门控向量：
   $$\mathbf{g} = \sigma(\text{gate}_{mlp}(\mathbf{x})) \in \mathbb{R}^{D}$$
   然后利用门控向量将 $\mathbf{x}$ 拆分为前向和后向两个中间张量：
   $$\mathbf{t}^{\rightarrow} = \mathbf{g} \odot \mathbf{x}, \quad \mathbf{t}^{\leftarrow} = (1 - \mathbf{g}) \odot \mathbf{x}$$
   最后，共享参数的 MLP 关系头分别对两个中间张量进行预测，在单次前向传播中同时输出两个方向的关系 logits：
   $$\mathbf{z}^{\rightarrow} = \text{relhead}_{mlp}(\mathbf{t}^{\rightarrow}), \quad \mathbf{z}^{\leftarrow} = \text{relhead}_{mlp}(\mathbf{t}^{\leftarrow})$$

### 训练时的特征一致性约束

为防止模型利用数据集偏差（如对输入掩码顺序产生不对称预测），DSFlash 在训练时随机交换主体-客体掩码的顺序，并通过特征一致性损失 $\mathcal{L}_{\text{consistency}}$ 约束中间特征对称性：
$$\mathcal{L}_{\text{consistency}} = \frac{1}{D}\sum_{i=1}^{D}(t_i^{\rightarrow} - t_i^{\prime\leftarrow})^{2} + (t_i^{\leftarrow} - t_i^{\prime\rightarrow})^{2}$$
其中 $t_i^{\prime\leftarrow}$ 和 $t_i^{\prime\rightarrow}$ 是交换掩码顺序后重新计算得到的中间张量。这一机制确保了双向预测对输入顺序的对称性。

### 效率优化的协同效应

上述模块之间存在显著的协同效应。统一骨干网络是延迟优化的最大贡献者（消融实验中单独将延迟从 98ms 降至 41ms），但会带来 mR@50 的显著下降（从 28.9 降至 25.0）。双向门控预测恰好弥补了这一性能损失，将 mR@50 恢复至 28.8，同时进一步将延迟降至 29ms。低分辨率掩码（跳过双线性插值上采样，直接使用 $160 \times 160$ 原始掩码计算 patch 重叠率）则在不增加延迟的前提下将 mR@50 进一步提升至 30.5。最终的 DSFlash-L 在 PSG 数据集上以 50ms 延迟达到 30.90 mR@50，相比 DSFormer 的 28.9 mR@50（98ms 延迟）实现了精度与速度的双重超越。

### 补充图表

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the DSFlash architecture for inference. Part A is executed once per image. Part B is executed for each combination of two segmentation masks. We use EoMT as the segmentation backbone which is kept frozen throughout the whole training. We use the mask embedding module from DSFormer . The relation predictor head is described in Sec. 3.3. The red numbers indicate which components are covered in which section*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/011_Figure_7.jpg]]
*Figure 7: Illustration of the impact of multiple masks for the same ground truth mask. The model in figure B predicts multiple very similar masks together with separate relation predictions. However, this gives the model multiple attempts to predict the ground truth relation, essentially ignoring the definition for mR@k. Adapted from [2]*

## 核心模块与公式推导

DSFlash的推理架构分为两大部分（图2）：Part A每张图像执行一次，负责全景分割与特征提取；Part B对每对分割掩码执行一次，负责关系预测。以下聚焦Part B中决定效率与性能的关键模块。

### 掩码嵌入与低分辨率优化

对于每一对主体-客体掩码组合，DSFlash沿用DSFormer的掩码嵌入机制，将空间位置信息编码到特征patch中。具体而言，对每个特征patch，根据主体掩码重叠比例 $\mathbf{r}_s$ 与客体掩码重叠比例 $\mathbf{r}_o$，将可学习的主体token $\mathbf{t}_s$、客体token $\mathbf{t}_o$ 和背景token $\mathbf{t}_{bg}$ 加权注入：

$$\text{token} = \text{patch} + \mathbf{r}_s \cdot \mathbf{t}_s + \mathbf{r}_o \cdot \mathbf{t}_o + (1 - \mathbf{r}_s - \mathbf{r}_o) \cdot \mathbf{t}_{bg}$$

**关键优化**：DSFormer在计算 $\mathbf{r}_s$ 和 $\mathbf{r}_o$ 前，需将分割logits通过双线性插值上采样至图像尺寸，这一步骤计算代价高昂。DSFlash发现可直接使用EoMT输出的原始低分辨率掩码（160×160）计算13×13 patch的重叠率，跳过双线性插值。定性对比（图3）显示，低分辨率掩码与上采样掩码在空间覆盖上高度一致，因此对关系预测的定位信息损失极小。消融实验（表2）表明，这一优化将mR@50从28.8提升至30.5，同时将延迟从29ms降至18ms（DSFlash-S*配置），实现了性能与速度的双重收益。

### 双向门控关系预测

DSFormer的关系预测头需要两次前向传播：第一次以 $(S,O)$ 顺序预测前向关系，第二次以 $(O,S)$ 顺序预测后向关系。DSFlash通过门控机制将其统一为单次前向传播。

给定Transformer颈部输出的富化特征张量 $\mathbf{x} \in \mathbb{R}^{D}$，首先通过一个小型MLP和sigmoid激活计算门控向量：

$$\mathbf{g} = \sigma(\text{gate}_{mlp}(\mathbf{x})) \in \mathbb{R}^{D}$$

门控向量 $\mathbf{g}$ 的每个元素在 $[0,1]$ 之间，用于将特征 $\mathbf{x}$ 按元素拆分为两个互补的中间张量：

$$\mathbf{t}^{\rightarrow} = \mathbf{g} \odot \mathbf{x} \in \mathbb{R}^{D}$$

$$\mathbf{t}^{\leftarrow} = (1 - \mathbf{g}) \odot \mathbf{x} \in \mathbb{R}^{D}$$

其中 $\mathbf{t}^{\rightarrow}$ 承载前向关系 $(S \rightarrow O)$ 的特征，$\mathbf{t}^{\leftarrow}$ 承载后向关系 $(O \rightarrow S)$ 的特征。两者共享同一个关系预测MLP头，分别输出谓词类别logits：

$$\mathbf{z}^{\rightarrow} = \text{relhead}_{mlp}(\mathbf{t}^{\rightarrow}) \in \mathbb{R}^{C}$$

$$\mathbf{z}^{\leftarrow} = \text{relhead}_{mlp}(\mathbf{t}^{\leftarrow}) \in \mathbb{R}^{C}$$

**训练一致性约束**：为防止模型利用数据集偏差（如固定顺序的掩码输入），训练时随机交换 $(S_0, S_1)$ 的输入顺序，并通过特征一致性损失强制对称性。设正常顺序产生的中间特征为 $\mathbf{t}^{\rightarrow}, \mathbf{t}^{\leftarrow}$，交换顺序后产生的中间特征为 $\mathbf{t}^{\prime\rightarrow}, \mathbf{t}^{\prime\leftarrow}$，损失定义为：

$$\mathcal{L}_{\text{consistency}} = \frac{1}{D}\sum_{i=1}^{D}(t_i^{\rightarrow} - t_i^{\prime\leftarrow})^{2} + (t_i^{\leftarrow} - t_i^{\prime\rightarrow})^{2}$$

该损失约束前向路径在交换输入后应与后向路径的特征一致，反之亦然，从而确保门控机制对输入顺序对称。消融实验（表2）显示，门控双向预测将mR@50从25.0恢复至28.8（接近原始DSFormer的28.9），同时将延迟从37ms进一步降至29ms——在几乎完全恢复性能的前提下，将关系预测的前向传播次数减半。

### 动态Patch剪枝

DSFormer的Transformer颈部处理全部13×13=169个patch token，但许多patch与主体和客体均无空间重叠，对关系预测贡献微弱。DSFlash在token进入Transformer颈部前，基于掩码重叠率进行动态剪枝：若某patch与主体掩码和客体掩码的重叠比例均为零，则直接丢弃该patch token，减少后续Transformer层的计算量。

剪枝比例取决于具体的主体-客体掩码对，因此是动态的。消融实验（表3）表明，在GTX 1080上，动态patch剪枝将延迟从230ms降至205ms，但mR@50从28.80降至26.67（下降约2.13个点）。剪枝训练（即在训练过程中也随机丢弃patch）可增强模型对剪枝的鲁棒性，但整体mR@50仍低于正常训练的模型。

### Token合并

为进一步降低注意力计算成本，DSFlash在Transformer层中应用ToMe-SD token合并。ToMe-SD在计算注意力前将相似token合并，注意力计算后再将token拆分，从而较好地保留分割能力。与动态patch剪枝组合使用时（表3），GTX 1080延迟进一步降至173ms，mR@50为26.51。需注意，token合并与patch剪枝在H100/RTX 3090等高端GPU上吞吐量提升有限，主要在老旧GPU上效果显著。

### 高效掩码嵌入实现

DSFlash还对DSFormer的掩码嵌入代码进行了底层优化。原始实现包含低效的PyTorch操作序列（stack、split、flatten、mean），每次为每对掩码重新计算重叠率。DSFlash将其简化为平均池化层，对所有掩码预计算重叠比率后按需复制，显著减少了池化调用次数和张量拷贝开销。该优化在消融实验（表2）中将延迟从41ms降至37ms，且不影响mR@50，属于零性能代价的纯工程加速。

### 补充图表

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/004_Figure_4.jpg]]
*Figure 4: Schematic of DSFlash’s gating mechanism and the enforced feature consistency loss during training. Given two segmentation masks and an image, DSFlash computes a class token x using various modules, summarized here as Φ. To train the consistency loss, DSFlash performs two forward passes through the model head with flipped segmentation masks*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/010_Figure_8.jpg]]
*Figure 8: Illustration of the mask embedding. Subject, object, and background tokens are learnable tokens that are added to the patch embedding with a weighted sum. The weights are determined from the proportion of the patch area that is covered by the respective segmentation mask. Adapted from [2]*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/018_Figure_12.jpg]]
*Figure 12: Comparison of a model trained with pruned patches and one without when pruning patches during evaluation*

## 实验与分析

### 主结果：精度-延迟权衡的帕累托前沿

DSFlash在PSG数据集上建立了新的精度-延迟帕累托前沿，以显著更低的延迟实现了超越或持平现有SOTA的关系预测精度。如Table 1所示，DSFlash-L以仅50ms的延迟达到30.90 mR@50，相比DSFormer（28.9 mR@50，98ms延迟）在精度提升2.0个点的同时将延迟减半（-49%）。DSFlash-B以29ms延迟达到28.80 mR@50，在精度基本持平（-0.1）的情况下延迟仅为DSFormer的30%。极致轻量的DSFlash-S*进一步将延迟压缩至18ms（25.05 mR@50），延迟降低82%，适用于对实时性要求极高的场景。

这些结果在SGDet/SGGen协议下测得，所有延迟测量均在RTX 3090 GPU上以batch size=1进行，模拟视频流处理场景。采用SingleMPO评估协议确保每个ground truth主体-客体对只有一次预测，并使用Mean Recall@50（mR@50）以平衡PSG数据集的长尾谓词分布。如Figure 1所示，DSFlash系列在精度-延迟平面上明显优于所有先前方法。

### 消融实验：三个关键杠杆的独立贡献

Table 2呈现了从DSFormer到DSFlash的增量消融过程，揭示了三个关键效率杠杆的因果效应：

**统一骨干网络**是最有效的单项延迟优化。将DSFormer的两个独立分割模型（MaskDINO + ResNet）替换为单一冻结EoMT骨干后，延迟从98ms骤降至41ms，但mR@50从28.9下降至25.0。这一精度损失源于EoMT的分割质量低于原MaskDINO模型，但为后续优化提供了速度基础。

**门控双向预测**是精度恢复的关键。在统一骨干基础上引入门控机制（Sec. 3.3），使关系预测从两次前向传播合并为一次，延迟从37ms进一步降至29ms，同时mR@50从25.0恢复至28.8，已接近原始DSFormer水平。这一结果验证了门控向量 $\mathbf{g} = \sigma(\text{gate}_{mlp}(\mathbf{x}))$ 能够有效拆分特征张量，在单次前向传播中同时编码前向（$S \to O$）和后向（$O \to S$）关系信息。

**低分辨率掩码**带来了意外的精度增益。直接使用EoMT输出的160×160原始分辨率掩码计算13×13 patch重叠率，跳过双线性插值上采样步骤，不仅将延迟从29ms降至18ms，还将mR@50从28.8提升至30.5。如Figure 3定性对比所示，低分辨率掩码在边界处更为平滑，减少了上采样引入的锯齿伪影，反而提高了patch重叠率计算的准确性。

**高效掩码嵌入模块**（Sec. 3.6）将延迟从41ms降至37ms而不影响mR@50。该优化将DSFormer中的低效PyTorch操作序列（stack/split/flatten/mean）简化为平均池化层，对所有掩码预计算重叠比率后按需复制，减少了冗余的池化调用和数据拷贝。

### Patch剪枝与Token合并：老旧GPU上的显著收益

Table 3展示了动态patch剪枝和Token合并在不同GPU上的效果差异。在GTX 1080上，基于掩码的动态patch剪枝将延迟从230ms降至205ms，mR@50从28.80降至26.67（-2.13）。进一步叠加ToMe-SD token合并（30%合并率）后，延迟降至173ms，mR@50为26.51。然而，在H100和RTX 3090等高端GPU上，这些优化的延迟收益有限，主要因为高端GPU的并行计算能力足以高效处理全部169个patch token，剪枝和合并的额外开销反而部分抵消了计算节省。

Table 5的RPS（每秒处理关系数）指标进一步印证了这一趋势：在批处理场景下，patch剪枝和token合并在GTX 1080上的吞吐量提升更为显著。剪枝训练（Figure 12）虽能增强模型对评估时剪枝patch的鲁棒性，但整体mR@50低于正常训练的模型，表明在训练中引入剪枝会牺牲一定的关系预测能力。

### 分割骨干能力与场景图性能的强相关性

Figure 5和Figure 10揭示了一个重要发现：分割骨干网络的全景分割质量与最终场景图性能之间存在极强相关性（相关系数0.99）。mR@inf定义为给定分割掩码下理想PSGG模型可达到的最佳mR@k，该指标与mR@50和全景质量（Panoptic Quality）均呈近乎线性关系。这一发现表明，DSFlash的性能上限主要由冻结的EoMT骨干决定，未来通过更强的分割骨干（如EoMT-3L）可直接提升关系预测精度，而无需重新设计关系预测模块。

### 失败模式分析

DSFlash的主要失败模式体现在两个方面：

**关系方向混淆**：模型有时混淆主体与客体的关系方向，例如将“人牵着马”错误预测为“马牵着人”（Figure 14）。这一问题的根源在于双向门控机制虽然能同时预测两个方向，但门控向量 $\mathbf{g}$ 的学习可能未充分捕获方向性的语义差异。论文提出使用对比损失（如Graphical Contrastive Losses）作为潜在解决方案，但尚未实验验证。

**动态剪枝的精度代价**：patch剪枝在GTX 1080上带来25ms延迟收益的同时，mR@50下降2.13个点。这一精度损失源于丢弃的patch可能包含对关系分类有用的上下文信息（如背景物体、场景布局），在性能敏感的应用中需要根据部署GPU和精度需求进行权衡。

**数据集泛化性未验证**：所有实验仅在PSG数据集上进行，尚未在Visual Genome等其他场景图数据集上评估DSFlash的泛化能力，也未与所有最新PSGG方法进行全面的大规模比较。

### 补充图表

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparison between our approach and previous work in terms of performance (mR@50) and latency (ms) on the PSG dataset*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on the PSG dataset . All models are evaluated using a batch size of 1 on an RTX 3090 GPU and the SGDet protocol. Models marked with a star (*) use low-resolution segmentation masks, discussed in Sec. 3.2*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/007_Table_2.jpg]]
*Table 2: Impact of the optimizations on the overall latency, measured on a NVIDIA GeForce RTX 3090 GPU and a batch size of 1. We also report RPS as the processed relations per second when processing batched data. The rows are read from top to bottom with each row adding an incremental optimization to the evaluated model. The last row is an exception and is an improvement from the row marked with 1*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/009_Table_3.jpg]]
*Table 3: Impact of Token Merging (ToMe) and mask-based dynamic patch pruning (Prune, Sec. 3.4) on DSFlash’s latency with batch size 1, measured on a H100, RTX 3090, and GTX 1080 GPU*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of the segmentation masks produced by EoMT with and without upsampling the logits*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/017_Table_5.jpg]]
*Table 5: Impact of Token Merging (ToMe) and mask-based dynamic patch pruning (Prune, Sec. 3.4) on DSFlash’s RPS, measured on a H100, RTX 3090, and GTX 1080 GPU*

![[assets/figures/papers/paper_list_l2469_https_arxiv_org_abs_2603_10538/figures/019_Figure_14.jpg]]
*Figure 14: Failure cases when using DSFlash. Shown are predictions that are in the top 50 predictions for the respective image. The color in the boxes indicates to which subject the prediction is related to*

## 方法谱系与知识库定位

### 1. 设计谱系：从两阶段SGG到实时全景场景图生成

DSFlash的方法论根基可追溯至两阶段场景图生成（SGG）范式。该范式将任务解耦为**分割阶段**（定位所有实例）与**关系预测阶段**（对每对实例分类谓词），其核心优势在于可复用预训练分割骨干，大幅降低训练成本。DSFlash明确继承了这一设计哲学，并直接从当前PSGG领域的SOTA方法**DSFormer**（Lorenz et al., ECCV 2024）出发进行重构。

DSFormer奠定了两个关键设计，成为DSFlash的起点：
- **掩码嵌入机制**：对每对分割掩码，计算每个特征patch被主体/客体掩码覆盖的面积比例，将主体、客体、背景三个可学习token按比例加权注入patch嵌入中（见公式1）。这编码了主体与客体的空间位置关系。
- **两阶段流水线**：独立的分割模型（MaskDINO + ResNet骨干）与独立的关系预测颈部（Transformer层），两者串行执行。

DSFlash的改进策略可概括为**“保留核心表示机制，重构计算路径”**：保留DSFormer的掩码嵌入公式作为空间编码手段，但对其实现效率、骨干架构、关系预测方向性、token处理量进行系统性重构。这种“借壳重构”策略使DSFlash在保持表示能力的同时，将延迟从98ms压缩至50ms（L版本），mR@50从28.9提升至30.90。

### 2. 对比基线全景

DSFlash的评估体系覆盖了PSGG领域的多个代表性方法，形成层次化的对比基线：

| 基线方法 | 角色定位 | 关键特征 |
|---------|---------|---------|
| **DSFormer** (Lorenz et al., ECCV 2024) | 主要对标基线，DSFlash的设计起点 | 两阶段PSGG，独立分割+关系预测，98ms延迟，28.9 mR@50 |
| **REACT** (Neau et al., 2025) | 实时SGG对比方法 | 优化两阶段SGG架构的速度，但尚未达到DSFlash的延迟水平 |
| **HiLo** | PSGG领域对比方法 | 全景场景图生成的早期探索 |
| **NeuralMotifs** | 经典SGG方法（PSG适配版） | 基于统计共现的SGG基线 |
| **VCTree** | 经典SGG方法（PSG适配版） | 基于动态树结构的SGG基线 |

**关键定位**：DSFlash是目前唯一在PSG数据集上同时实现**mR@50 > 30且延迟 < 60ms**的方法。DSFlash-B以29ms延迟达到28.80 mR@50（与DSFormer的28.9持平但延迟降低70%），DSFlash-L以50ms延迟达到30.90 mR@50（超越DSFormer 2.0个点且延迟减半）。这一“性能-延迟双超越”确立了DSFlash在实时PSGG领域的SOTA地位。

### 3. 效率杠杆的独立贡献与交互

DSFlash的效率提升并非单一技巧的堆砌，而是三个因果杠杆的协同作用。消融实验（Table 2）揭示了每个杠杆的独立贡献与交互效应：

**杠杆一：统一骨干网络（最有效的单项延迟优化）**
- 将DSFormer的两个独立分割模型（MaskDINO + ResNet）替换为单一冻结的EoMT骨干。
- 延迟从98ms骤降至41ms（-58%），但mR@50从28.9降至25.0（-3.9）。
- **因果机制**：消除重复特征提取是延迟降低的主因，但EoMT的分割质量略逊于MaskDINO，导致关系预测性能下降。

**杠杆二：高效掩码嵌入模块**
- 将DSFormer中低效的PyTorch操作序列（stack/split/flatten/mean）简化为平均池化层，对所有掩码预计算重叠率后按需复制。
- 延迟从41ms进一步降至37ms（-10%），mR@50不受影响。
- **因果机制**：纯工程优化，减少不必要的数据拷贝和重复计算。

**杠杆三：双向门控关系预测（性能恢复的关键）**
- 通过门控MLP将富化特征拆分为前向和后向中间张量，共享MLP关系头在单次前向传播中同时输出两个方向的关系预测。
- mR@50从25.0恢复至28.8（+3.8，接近原始DSFormer的28.9），同时延迟从37ms进一步降至29ms。
- **因果机制**：门控机制使模型在单次前向传播中学习双向对称表示，特征一致性损失（公式7）强制前向和后向预测对输入顺序对称，消除了两次前向传播的冗余。

**杠杆四：低分辨率分割掩码（性能超越的关键）**
- 直接使用EoMT输出的160×160原始掩码计算13×13 patch重叠率，跳过双线性插值上采样至图像尺寸。
- mR@50进一步提升至30.5（以DSFlash-S*评估），延迟降至18ms。
- **因果机制**：低分辨率掩码保留了足够的空间信息用于patch重叠率计算（Figure 3定性验证），同时避免了上采样的计算开销和可能的插值伪影。

**杠杆五：动态Patch剪枝与Token合并（边缘设备加速）**
- 丢弃与主体和客体均无重叠的patch token，应用ToMe-SD在Transformer层中合并相似token。
- 在GTX 1080上，剪枝使延迟从230ms降至205ms（mR@50下降2.13），剪枝+ToMe 30%进一步降至173ms（mR@50为26.51）。
- **因果机制**：这两个技术在高端GPU（H100/RTX 3090）上吞吐量提升有限，但在老旧GPU（GTX 1080）上效果显著，因为后者对token数量的敏感度更高（Table 3, Table 5）。

### 4. 适用边界与局限性

**已验证的适用场景**：
- PSG数据集的全景场景图生成（SGDet/SGGen协议），覆盖133个谓词类别和全景分割掩码。
- 视频流处理场景（batch size=1），在RTX 3090上可达56 FPS。
- 低资源训练环境：在GTX 1080上训练时间小于24小时。

**明确的局限性**：

1. **动态剪枝的性能代价**：patch剪枝使mR@50下降约2.13个点（从28.80降至26.67），在性能敏感的部署场景中需权衡。剪枝训练虽能增强模型鲁棒性（Figure 12），但整体mR@50仍低于正常训练的模型。

2. **关系方向混淆**：模型有时混淆主体与客体的关系预测方向（如将“人牵着马”错误预测为“马牵着人”），这是双向预测机制的固有挑战。

3. **数据集泛化未验证**：仅在PSG数据集上评估，尚未在Visual Genome等其他场景图数据集上验证泛化能力。PSG的谓词空间（133类）和场景分布可能限制模型在其他领域的迁移。

4. **高端GPU加速有限**：Token合并和patch剪枝在H100/RTX 3090等高端GPU上吞吐量提升有限，主要受益于老旧或边缘GPU。

5. **对比覆盖不完整**：未与所有最新PSGG方法进行全面的大规模比较，部分基线方法的性能数据可能来自不同评估协议。

### 5. 开放问题与未来方向

1. **方向混淆的解决路径**：论文提出可使用对比损失（如Graphical Contrastive Losses）解决主客体关系预测方向的混淆问题。这指向将关系预测建模为有序对分类而非独立谓词分类的潜在方向。

2. **剪枝训练的优化空间**：如何在patch剪枝训练中进一步提升模型的关系预测性能，使剪枝后的mR@50接近未剪枝水平，是实时部署的关键瓶颈。

3. **跨数据集泛化**：DSFlash能否泛化到PSG以外的场景图数据集（如Visual Genome），以及更丰富的谓词类别空间（VG包含数万谓词），需要进一步验证。

4. **下游任务验证**：DSFlash在实际下游任务（如具身智能推理、视觉问答、机器人导航）中的端到端效果尚未评估。实时PSGG的实用价值需要通过下游任务增益来证明。

5. **边缘设备部署**：在移动端或嵌入式GPU等更边缘设备上的性能表现和优化空间（如量化、蒸馏）值得探索。

6. **双向门控机制的推广**：双向门控关系预测机制是否可推广到其他需要对称预测的双向关系建模任务（如人-物交互检测HOI、视觉关系检测VRD），是一个有潜力的研究方向。

7. **冻结骨干的进一步提升**：能否通过自监督预训练或更大规模的分割数据进一步提升冻结骨干的特征质量，从而在不增加推理成本的前提下提升关系预测性能？Figure 5和Figure 10已揭示分割骨干的全景质量（mR@inf）与最终场景图性能（mR@50）之间存在0.99的强相关性，这为通过改进骨干来间接提升PSGG性能提供了清晰的路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/DSFlash_Comprehensive_Panoptic_Scene_Graph_Generation_in_Realtime.pdf]]

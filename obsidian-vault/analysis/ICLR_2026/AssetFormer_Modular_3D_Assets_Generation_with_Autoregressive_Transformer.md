---
title: "AssetFormer: Modular 3D Assets Generation with Autoregressive Transformer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer.pdf
project_link: null
code_link: https://github.com/Advocate99/AssetFormer
openreview_forum_id: ODB82HDp0V
aliases:
- AM3AGAT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用自回归Transformer对模块基元序列进行建模，并通过基于图遍历的标记重排序（DFS/BFS）、标记集建模和SlowFast解码策略，显著提升了生成质量和推理速度。"
primary_logic: "将模块化3D资产表示为具有离散属性的基元序列，并利用深度优先搜索（DFS）排序来捕捉空间层次依赖，使得自回归模型能够有效学习并生成结构连贯的模块化资产。"
claims:
- "DFS token重排序在FID上大幅优于原始顺序、BFS和RAR，FID从65.215降至55.186，证实排序对空间结构学习至关重要。"
- "结合PCG合成数据和真实用户数据训练模型，FID降至55.186，优于单一数据源（真实63.381，合成113.560），表明数据互补性提升泛化。"
- "Top-k采样在FID（55.186）上优于贪婪搜索（63.351）和束搜索（63.333），且保持CLIP分数相当，平衡了质量与多样性。"
- "SlowFast解码在保持生成质量（FID 55.831 vs 目标模型55.186）的同时，解码速度提升至119.02 token/s，相比目标模型80.62 token/s加速1.48倍。"
---

# AssetFormer: Modular 3D Assets Generation with Autoregressive Transformer

> [!tip] 核心洞察
> 将模块化3D资产表示为具有离散属性的基元序列，并利用深度优先搜索（DFS）排序来捕捉空间层次依赖，使得自回归模型能够有效学习并生成结构连贯的模块化资产。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AssetFormer：基于自回归Transformer的模块化3D资产生成 |
| 英文题名 | AssetFormer: Modular 3D Assets Generation with Autoregressive Transformer |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ODB82HDp0V) · [GitHub](https://github.com/Advocate99/AssetFormer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AssetFormer |
| Dataset | Modular Building Generation (collected dataset) |

> [!tip] 效果简介
> - Modular Building Generation (collected dataset) 上，FID (lower is better) 为 55.186 (AssetFormer + Top-K Sampling)，对比 108.476 (PCG)，变化 -53.29。

## 概要

3D资产的生成在游戏开发、虚拟现实和用户生成内容（UGC）场景中需求日益增长。传统方法主要生成密集网格或隐式表示，难以满足模块化资产对低存储占用、可编辑性和高效传输的严苛要求。模块化3D资产由有限类型的离散基元（如墙壁、屋顶、窗户）按空间关系组合而成，每个基元携带类别、旋转角度和三维位置等属性。然而，这类数据天然稀缺，且基元序列的排列顺序直接影响自回归模型的学习效果——不当的顺序会导致生成结构断裂、基元孤立等严重伪影。

AssetFormer针对上述瓶颈，提出了一个基于自回归Transformer的模块化3D资产生成框架。其核心思路是将模块化资产表示为基元的离散标记序列，并通过深度优先搜索（DFS）对序列进行重排序，使模型能够捕捉基元之间的空间层次依赖。在解码端，Top-k采样在生成质量与多样性之间取得了最佳平衡，而SlowFast推测解码则利用小容量草案模型与大容量目标模型的协同，在保持生成质量的前提下将解码速度提升至119.02 token/s，相比基础模型加速约1.48倍。

在定量评估中，AssetFormer结合合成数据与真实用户数据的混合训练策略，将FID降至55.186，显著优于程序化生成基线（108.476）和单一数据源训练方案。生成资产可直接无缝集成到Unreal Engine等游戏引擎中，支持纹理映射与零样本编辑，无需额外后处理。



3D内容创作是游戏开发、虚拟现实和用户生成内容（UGC）平台的核心环节。传统3D资产生成方法主要依赖密集网格或隐式表示（如NeRF、3D高斯泼溅），这些方法虽然在视觉保真度上取得了显著进展，但生成的资产本质上是不透明的三角网格，缺乏结构化信息，难以直接编辑、复用或高效传输。

模块化3D资产则采用完全不同的设计范式：一个复杂资产（如建筑）由多个离散的基元（primitives）组合而成，每个基元拥有类别、旋转角度和三维位置等属性。这种表示方式天然支持纹理映射、细节层次（LOD）切换和引擎内实时编辑，生成的资产可直接部署到Unreal Engine等工业环境中，无需后处理。

然而，模块化3D资产的自动生成面临两个关键瓶颈。**第一，数据稀缺且序列建模困难。** 模块化资产数据远少于图像或自然语言数据，且基元之间的排列顺序直接影响自回归模型的学习效果——不当的顺序会导致模型难以捕捉空间依赖关系，生成结果出现孤立基元或结构断裂。**第二，生成效率与质量的平衡。** 自回归生成逐token解码的特性使得长序列生成速度较慢，而模块化资产通常包含大量基元，对推理效率提出了更高要求。

现有方法难以同时满足这些需求。程序化内容生成（PCG）虽能产出高质量模块化建筑，但依赖精细的规则设计，仅适用于简单结构，且无法通过文本灵活控制。通用3D生成模型（如SF3D、Tripo 2.0、Hunyuan3D 2.0）生成的密集网格缺乏模块化结构，纹理质量不稳定，且内部几何细节难以准确捕捉。直接微调语言模型生成JSON序列的方法则因序列过长和表示隐式性而效果远逊。

针对上述缺口，本文提出AssetFormer——一个基于自回归Transformer的模块化3D资产生成框架。核心思路是将模块化资产表示为基元序列，利用深度优先搜索（DFS）对序列重排序以捕捉空间层次依赖，并采用SlowFast推测解码策略在保持生成质量的同时显著提升推理速度。



## 核心方法与创新机理

AssetFormer的核心创新在于将模块化3D资产的生成问题转化为**自回归序列建模问题**，并通过三个关键设计突破传统方法的瓶颈。

### 从密集网格到模块基元序列的表示范式转换

传统3D生成方法（如SF3D、Tripo 2.0、Hunyuan3D 2.0）输出密集网格，虽然能表征任意几何，但在游戏引擎和UGC场景中面临三个根本矛盾：网格存储量大、编辑需专业工具、纹理映射需后处理。AssetFormer直接生成由离散基元构成的模块化资产，每个基元仅需类别、旋转和三维位置三个属性 $P _ { j } = ( c _ { j } , r _ { j } , \pmb { x } _ { j } )$ 即可完整描述，天然支持引擎直接加载、纹理映射和用户编辑（Table 6, Fig 8, Fig 11）。

这一范式转换的因果机制在于：模块化表示将连续几何空间离散化为有限词汇表，使得生成任务从高维连续回归退化为离散标记预测，从而可以充分借鉴语言模型领域的成熟技术栈。

### 基于图遍历的标记重排序：DFS作为空间层次先验

这是论文最具决定性的创新。模块化资产的基元天然具有空间连接关系，但原始数据中的基元顺序是任意的。AssetFormer将基元间的连接关系建模为图，通过深度优先搜索（DFS）或广度优先搜索（BFS）遍历图结构对基元序列重排序，使得空间上相邻的基元在序列中也相邻。

DFS排序的效果是决定性的：FID从原始顺序的65.215降至55.186（Table 2），降幅达15.4%。相比之下，BFS仅降至61.620，而随机排序（RAR）甚至恶化至83.561。定性结果（Fig 4a）显示，不当排序会导致生成结果中出现孤立基元和结构断裂。

DFS优于BFS的深层原因是：DFS沿深度方向优先探索，先完整处理一个空间分支再处理下一个，这与建筑结构的层次化组织方式（先主体后附属）高度吻合，使得自回归模型能更有效地捕捉长程空间依赖。

### 标记集建模与SlowFast解码的效率创新

在标记化层面，AssetFormer采用联合词汇表 $\mathcal { V } = \mathcal { C } \vee \mathcal { R } \vee \mathcal { X } _ { 0 } \vee \mathcal { X } _ { 1 } \vee \mathcal { X } _ { 2 } \vee \{ < \mathrm { E O S } > \}$，将类别、旋转、三个坐标的词汇表合并，每个属性独立维护词汇空间，避免了属性间语义混淆。

在解码层面，Top-k采样（FID 55.186）显著优于贪婪搜索（FID 63.351）和束搜索（FID 63.333），平衡了生成质量与多样性（Table 1）。SlowFast推测解码利用小容量AssetFormer-S（87M参数）快速生成草案标记，大容量AssetFormer-B（312M参数）进行验证修正，在保持生成质量（FID 55.831 vs 55.186）的同时将解码速度从80.62 token/s提升至119.02 token/s，加速1.48倍（Table 4）。

### 文本条件与数据策略的协同

文本控制方面，使用FLAN-T5 XL编码文本并通过MLP投影预填充到序列中，结合分类器自由引导（CFG）增强文本对齐，引导公式为 $l _ { c f g } = l ^ { \prime } + s \cdot ( \breve { l } - l ^ { \prime } )$。数据策略上，结合程序化生成（PCG）合成数据和真实用户数据训练，FID降至55.186，优于单一数据源（真实数据63.381，合成数据113.560），验证了两类数据的互补性（Table 3）——合成数据提供结构多样性，真实数据提供风格约束。



![[assets/figures/papers/paper_list_l9_AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the AssetFormer Framework. Given the modular assets, e.g., the building, we first render the assets in digital engines and produce the images for querying GPT-4o. The cleaned captions, pre-filled with a re-ordered token set, serve as input for the autoregressive modeling. After training, AssetFormer autoregressively produces modular assets that are ready to be integrated into industrial environments, with model-based enhancement and application-driven deployment*

AssetFormer 的整体 pipeline 围绕三个核心阶段构建：数据策展、自回归建模与推理部署（Fig. 2）。其设计目标是将模块化 3D 资产表示为离散基元序列，并通过自回归 Transformer 学习从文本到模块化结构的映射。

**数据策展阶段** 解决模块化资产标注稀缺的瓶颈。给定来自在线 UGC 平台的建筑资产，首先在数字引擎中渲染多视角图像，随后利用 GPT-4o 基于渲染图生成文本描述并进行清洗。这一流程绕过了人工标注的高成本，但也引入了文本-图像域差距这一已知局限。训练数据由 16,000 个真实用户创作样本和 4,000 个程序化生成（PCG）合成样本组成，二者互补——真实数据提供多样性，合成数据补充结构规律性（Table 3 消融证实混合训练 FID 55.186 优于任一单一来源）。

**自回归建模阶段** 是 pipeline 的核心。每个建筑被分解为 $N$ 个基元 $P_j = (c_j, r_j, \pmb{x}_j)$，分别编码类别、旋转和三维位置。这组基元经过两个关键处理步骤后送入 Transformer：

1. **离散标记化与标记集建模**：每个基元的 5 个属性被映射到联合词汇表 $\mathcal{V} = \mathcal{C} \vee \mathcal{R} \vee \mathcal{X}_0 \vee \mathcal{X}_1 \vee \mathcal{X}_2 \vee \{<\mathrm{EOS}>\}$ 的离散标记，各属性保持独立词汇空间，避免跨属性语义混淆。

2. **标记重排序**：原始基元序列 $T$ 经图遍历重排序为 $T' = \mathrm{ReOrder}(T)$，其中 DFS（深度优先搜索）遍历基元连接图是决定性设计。Table 2 显示 DFS 排序将 FID 从原始顺序的 65.215 降至 55.186，而随机重排序（RAR）的 FID 高达 83.561，证实排序对捕捉空间层次依赖至关重要。定性结果（Fig. 4a）进一步表明，不当排序导致孤立基元和视觉伪影。

重排序后的标记序列与文本特征拼接。文本编码器采用 FLAN-T5 XL，经 MLP 投影后预填充至序列开头。Transformer 骨干基于 Llama 的 Decoder-only 架构，使用 1D RoPE 位置编码，无预训练权重，以标准交叉熵损失 $\mathcal{L} = \mathrm{CrossEntropy}(\mathrm{Shift}(\hat{S}), \mathrm{Tokenize}(\{P\}))$ 进行下一标记预测训练。推理时采用分类器自由引导（CFG），logits 计算为 $l_{cfg} = l' + s \cdot (l - l')$，引导强度 $s=2.0$。

**推理部署阶段** 采用两种互补解码策略。Top-k 采样（$k=10$，温度 0.7）在 FID 55.186 上优于贪婪搜索（63.351）和束搜索（63.333），平衡了生成质量与多样性（Table 1）。SlowFast 推测解码则针对生成效率瓶颈：小容量 AssetFormer-S（87M，12 层）快速生成草案标记，大容量 AssetFormer-B（312M，24 层）进行验证修正。这一设计利用了模块化资产生成中预测难度的异质性——简单标准基元由草案模型快速处理，复杂结构由目标模型精细调整。Table 4 显示 SlowFast 解码在保持 FID 55.831（接近目标模型 55.186）的同时，解码速度从 80.62 token/s 提升至 119.02 token/s，加速 1.48 倍。

最终生成的基元序列可直接解析为模块化资产，无缝集成到 Unreal Engine 等游戏引擎中，支持纹理映射与编辑（Fig. 8, Fig. 11），无需后处理步骤。



AssetFormer 的核心是将模块化 3D 资产生成建模为离散基元序列的自回归预测问题。模型以文本描述 $t$ 为输入，输出由 $N$ 个基元构成的资产 $\{P\}_{i=1}^{N}$，其中每个基元 $P_j$ 携带三个离散属性：

$$P _ { j } = ( c _ { j } , r _ { j } , \pmb { x } _ { j } )$$

- $c_j$：基元类别（如墙、屋顶、楼梯等，共 25 种）
- $r_j$：旋转角度（离散化为 4 种方向）
- $\pmb{x}_j$：三维位置坐标（各轴离散化为有限取值）

生成模型的形式化映射为 $G : \pmb{t} \to \{P\}_{i=1}^{N}$。

### 离散标记化与标记集建模

将每个基元的 5 个属性分别映射到独立的离散词汇空间，构建联合词汇表 $\mathcal{V}$：

$$\mathcal{V} = \mathcal{C} \vee \mathcal{R} \vee \mathcal{X}_0 \vee \mathcal{X}_1 \vee \mathcal{X}_2 \vee \{<\mathrm{EOS}>\}$$

词汇表大小为各属性词汇大小之和加 1（终止符）：

$$|\mathcal{V}| = |\mathcal{C}| + |\mathcal{R}| + |\mathcal{X}_0| + |\mathcal{X}_1| + |\mathcal{X}_2| + 1$$

这一标记集建模（Token Set Modeling）策略的关键在于：每个属性维护独立的词汇空间，模型在预测时需同时推断类别、旋转和位置，但各属性标记在序列中交错排列，形成统一的下一标记预测任务。

$n$ 个基元的原始标记序列 $T$ 为：

$$T = \{c^0, r^0, x_0^0, x_1^0, x_2^0, \ldots, c^{n-1}, r^{n-1}, x_0^{n-1}, x_1^{n-1}, x_2^{n-1}, \mathrm{EOS}\}$$

### 标记重排序

原始序列中的基元顺序是任意的，无法反映空间连通性。AssetFormer 将基元间的空间关系建模为图，通过深度优先搜索（DFS）或广度优先搜索（BFS）遍历该图，对基元序列重排序：

$$T' = \mathrm{ReOrder}(T) = \{c^{\tau_0}, r^{\tau_0}, x_0^{\tau_0}, x_1^{\tau_0}, x_2^{\tau_0}, \ldots, c^{\tau_{n-1}}, r^{\tau_{n-1}}, x_0^{\tau_{n-1}}, x_1^{\tau_{n-1}}, x_2^{\tau_{n-1}}, \mathrm{EOS}\}$$

其中 $\tau_i$ 为重排序后第 $i$ 个基元在原序列中的索引。消融实验证实，DFS 排序将 FID 从原始顺序的 65.215 降至 55.186，BFS 为 61.620，而随机排序（RAR）甚至恶化至 83.561（Table 2），表明空间层次依赖的捕捉是模型成功的关键瓶颈。

### 自回归 Transformer 骨干

模型采用基于 Llama 的 Decoder-only Transformer，使用 1D 旋转位置编码（RoPE），无预训练权重。训练目标为标准交叉熵损失：

$$\mathcal{L} = \mathrm{CrossEntropy}(\mathrm{Shift}(\hat{S}), \mathrm{Tokenize}(\{P\}))$$

其中 $\hat{S}$ 为模型输出的预测标记序列，$\mathrm{Shift}$ 操作将其右移一位以对齐下一标记预测任务。

文本条件通过 FLAN-T5 XL 编码后经 MLP 投影为 token 特征，预填充到序列开头，使模型在生成每个基元标记时都能感知文本语义。

### 分类器自由引导

推理时采用分类器自由引导（CFG）增强文本对齐：

$$l_{cfg} = l' + s \cdot (\breve{l} - l')$$

其中 $\breve{l}$ 为条件 logits，$l'$ 为无条件 logits，$s$ 为引导强度（实验中取 2.0）。该机制使模型在保真度和文本相关性之间取得可控平衡。

### SlowFast 推测解码

针对自回归生成速度慢的问题，AssetFormer 引入 SlowFast 解码策略：使用小容量 AssetFormer-S（87M 参数）快速生成草案标记，大容量 AssetFormer-B（312M 参数）进行验证和修正。草案模型采样过程为：

$$\hat{x}_t \sim p(x \mid \text{prefix}, x_0, \ldots, x_{n-1}, \hat{x}_0, \ldots, \hat{x}_{t-1})$$

该策略利用模块化资产生成中预测难度的不均性——简单基元（如标准墙体）由草案模型快速处理，复杂结构由目标模型精修——在保持 FID 55.831（接近目标模型 55.186）的同时，将解码速度从 80.62 token/s 提升至 119.02 token/s，加速 1.48 倍（Table 4）。



## 实验与关键发现

### 主结果

AssetFormer在模块化建筑生成任务上显著优于程序化生成基线。Table 1报告了定量对比：AssetFormer配合Top-k采样取得最佳FID 55.186，相比PCG基线的108.476降低了53.29点，同时CLIP分数达到0.320。这一结果表明自回归Transformer能够有效学习模块基元的空间排列规律，生成与真实数据分布高度一致的资产。

![[assets/figures/papers/paper_list_l9_AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer/figures/005_Table_1.jpg]]
*Table 1: Quantitative results compared with baselines. We show comparison results on generation quality, indicated by FID and CLIP score*

Table 1同时揭示了不同解码策略的差异：Top-k采样（FID 55.186）明显优于贪婪搜索（63.351）和束搜索（63.333），三者CLIP分数相近。这说明Top-k采样在保持文本对齐的同时，通过引入受控随机性提升了生成多样性，避免了确定性策略的模式坍塌倾向。

用户研究（Table 5）进一步验证了主观质量：AssetFormer在紧凑性（3.42）、多样性（3.92）、美学（3.63）和复杂度（3.57）四项指标上均衡接近真实数据（Ground Truth），而PCG虽在紧凑性上得分最高（4.47），但多样性（2.42）和复杂度（2.44）严重不足，暴露了规则系统难以覆盖长尾建筑类型的固有缺陷。

### 关键消融分析

**Token重排序是核心设计。** Table 2定量对比了四种排序策略：DFS重排序取得FID 55.186，显著优于原始顺序（65.215）、BFS（61.620）和随机排序方法RAR（83.561）。DFS相比原始顺序FID降低10点，验证了空间层次依赖对自回归建模的关键作用——模块化建筑天然形成树状连接图，深度优先遍历确保子模块在序列中紧邻其父模块，降低了Transformer学习长程空间关系的难度。

![[assets/figures/papers/paper_list_l9_AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer/figures/006_Table_2.jpg]]
*Table 2: Quantitative ablation analysis on token orders. We compare the results of models trained on different token orders and we also implement a recent token randomized training method design for autoregressive modeling of image generation*

定性结果（Fig. 4(a)）揭示了不当排序的典型失败模式：原始顺序和RAR产生孤立基元（红色矩形标注），表现为墙体与屋顶空间错位或悬空部件。这一现象的本质原因是，Transformer在预测当前基元位置时，其注意力机制难以跨越序列中的不相关基元去捕捉空间相邻关系。DFS通过将空间连通性编码为序列局部性，从根本上缓解了这一问题。

![[assets/figures/papers/paper_list_l9_AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative ablation analysis. (a) Ablation on token orders. With improper token order, the model struggles to fit and generate the distribution accurately. (b) Ablation on data sources. The models fail to cover a wide range of diverse building types and exhibits a higher ratio of failure cases when trained on a single data source. The artifacts are indicated in red rectangles*

**数据互补性提升泛化。** Table 3的消融显示：仅用合成数据训练时FID高达113.560，仅用真实数据时为63.381，两者结合降至55.186。合成数据由PCG随机生成，覆盖了更广泛的基元组合模式但缺乏真实建筑的风格约束；真实数据来自UGC平台，风格一致但多样性有限。两者互补使模型同时习得结构多样性和风格合理性，Fig. 4(b)的可视化证实了单一数据源训练会导致特定建筑类型的缺失和更高的失败比例。

![[assets/figures/papers/paper_list_l9_AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer/figures/007_Table_3.jpg]]
*Table 3: Ablation analysis on data sources. We train models on different configurations of data sources, and show the distribution difference of data generation*

### SlowFast解码的加速效果

Table 4展示了推测性解码的性能：使用87M参数的AssetFormer-S作为草案模型、312M参数的AssetFormer-B作为目标模型，SlowFast解码在保持生成质量（FID 55.831 vs 目标模型55.186）的同时，解码速度达到119.02 token/s，相比目标模型的80.62 token/s加速1.48倍。这一加速效果源于模块化资产生成的特殊性——简单基元（如标准墙体）可由小模型快速预测，复杂结构（如屋顶转角）才需大模型验证和修正，草案模型的接受率较高。

![[assets/figures/papers/paper_list_l9_AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer/figures/008_Table_4.jpg]]
*Table 4: Analysis on SlowFast Decoding. We train models of different parameters and perform SlowFast decoding. The generation quality and decoding speed are evaluated*

### 失败模式与局限

1. **基元类型受限。** 当前词汇表仅包含25种基元类别，来自单一UGC平台。这限制了模型生成超出训练分布的建筑风格，例如拱形结构或非标准屋顶形式。
2. **文本控制不够精细。** 文本描述通过GPT-4o基于渲染图像生成，存在与自然图像的域差距。模型对建筑全局类型（如"哥特式"vs"现代主义"）的判别不够准确，可能生成风格混合的资产。
3. **纹理需要后处理。** 生成过程仅输出基元序列，不包含纹理信息。虽然Fig. 8展示了通过基元-纹理映射在Unreal Engine中实现纹理化，但这一步骤需要人工配置或额外的自动化流程。
4. **FID指标的局限性。** FID基于渲染图像的Inception特征计算，可能无法完全反映3D结构准确性——两个空间排列不同的建筑可能产生相似的2D投影，导致FID低估结构错误。

### 与原生3D生成方法的定性对比

Fig. 5揭示了直接微调原生3D生成模型（如Hunyuan3D 2.0）的固有问题：水密化预处理将模块化资产转换为密集网格时，会丢失模块边界信息并扭曲几何细节（如梯子结构变形）；微调后的模型输出整体质量较差，细节粗糙。这从反面证明了专门为模块化表示设计的生成框架的必要性。

Fig. 6的透明渲染对比显示，AssetFormer生成的建筑内部结构紧凑有序，而MeshGPT生成的网格内部存在大量冗余面和空洞。Table 6系统总结了模块化表示相比网格表示的优势：无损、引擎就绪、高效存储、无需后处理、用户可编辑。



## 定位与知识库关联

### 与现有方法的关系

**程序化内容生成（PCG）**是模块化3D资产的传统生产方式。PCG通过人工设计的规则和随机化生成简单建筑，但缺乏文本控制能力，且复杂建筑需要精细的算法设计。AssetFormer在生成质量上大幅超越PCG基线（FID 55.186 vs 108.476），同时弥补了PCG在文本条件控制上的根本缺陷（Table 1）。

**通用3D生成模型**（SF3D、Tripo 2.0、Trellis、Hunyuan3D 2.0）通常输出密集网格，面临三个瓶颈：（1）难以精确捕捉建筑内部结构的复杂几何；（2）纹理质量不完美；（3）生成结果需要后处理才能集成到游戏引擎。定性对比显示，AssetFormer遵循模块化设计规范（标准基元、平整面），并通过基元-纹理映射在引擎中实现精确纹理（Fig. 3(b)）。Table 6 进一步量化了两种表示的系统性差异：模块化表示在效率、免后处理和用户友好性上全面占优。

**MeshGPT**是基于网格和自回归Transformer的生成方法，与AssetFormer共享自回归生成范式。定性对比（Fig. 6）表明，MeshGPT生成的网格内部结构松散，而AssetFormer能产生紧凑的基元排列，透明渲染和内部视角均验证了这一优势。

**微调Llama-2 + LongLoRa**尝试直接微调语言模型生成JSON序列。然而，由于序列过长且表示的隐式性，该方法效果远差于AssetFormer。这从反面验证了专用标记化、重排序和联合词汇表设计的必要性。

**RAR（Randomized Autoregressive Modeling）**是图像生成中提出的标记随机化训练方法。在模块化资产场景中，RAR的FID为83.561，甚至劣于原始顺序（65.215）和BFS（61.620），远不如DFS（55.186）（Table 2）。这表明图像生成中的标记随机化策略不适用于具有强空间依赖的模块化3D结构。

### 适用边界

1. **基元类型受限**：当前模型仅支持固定的25种基元类型（Fig. 12），来自单一在线UGC平台。这限制了生成资产的种类和结构多样性，无法直接扩展到家具、车辆等其他模块化资产类别。
2. **数据域受限**：训练数据来自特定UGC平台的建筑资产，可能影响在更广泛的游戏或建筑设计领域的泛化性。结合PCG合成数据（4,000样本）和真实用户数据（16,000样本）训练虽提升了FID（Table 3），但数据多样性仍受限于源域。
3. **文本控制精度有限**：文本描述通过GPT-4o基于渲染图像生成，存在与自然图像的域差距，导致对建筑全局类型的判别不够精确。CLIP分数（0.320）的绝对值表明文本-视觉对齐仍有提升空间。
4. **无纹理生成**：生成过程不包括纹理信息，纹理需要额外的后处理或纹理映射步骤（Fig. 8）。这虽然符合模块化资产的工作流（纹理通过模块映射实现），但限制了端到端的视觉质量评估。
5. **单模态输入**：当前仅支持文本条件，未探索图像条件或其他模态的输入，限制了应用的灵活性。

### 局限与失败模式

1. **标记顺序敏感**：定性消融（Fig. 4(a)）显示，不当的标记顺序（如原始顺序）会导致生成中出现孤立基元和视觉伪影（红色矩形标注）。模型对序列顺序高度敏感，DFS排序是当前最优但并非普适解。
2. **单一数据源训练失败**：仅使用合成数据训练时FID高达113.560，仅使用真实数据时FID为63.381（Table 3）。单一数据源模型无法覆盖多样化的建筑类型，失败案例比例更高（Fig. 4(b)）。
3. **水密化导致信息丢失**：将模块化资产转换为水密网格后，模块信息丢失，几何细节改变（如梯子变形）（Fig. 5(a-b)）。这解释了为何微调原生3D生成模型（如Hunyuan3D 2.1）无法有效替代专用模块化生成方法——微调后的模型整体质量较差，细节表现不佳（Fig. 5(c-d)）。
4. **FID评估的局限性**：FID依赖渲染图像，可能无法完全反映3D结构准确性。例如，两个结构不同的建筑可能因相似外观而获得相近的FID分数。用户研究（Table 5）提供了补充视角，AssetFormer在紧凑性（3.42）、多样性（3.92）、美学（3.65）和复杂度（3.57）上均接近真实数据水平。

### 开放问题

1. **多模态条件扩展**：如何将图像条件（如参考图像）引入AssetFormer，实现多模态引导的模块化资产生成？更强的视觉-语言模型（如LLaVA）能否提升文本描述的质量和对齐度？
2. **动态基元数量与类别扩展**：如何扩展模型以支持动态变化的基元数量和更复杂的模块化资产类别？离散词汇表方法能否适应更大规模、更细粒度的基元类型空间？
3. **实时交互式编辑**：模型展示了零样本编辑能力（Fig. 9），但如何实现实时交互式编辑，让用户即时修改生成的模块化结构？这需要在解码速度和交互延迟之间找到平衡。
4. **更大规模扩展性**：在更大规模的数据集上，自回归Transformer的扩展性如何？是否需要更高效的tokenization策略来应对基元数量和类别增长带来的序列长度膨胀？
5. **评估体系完善**：如何建立更全面的3D模块化资产评估指标，超越渲染图像FID，直接衡量结构准确性、模块连接合理性和空间层次一致性？



## 原文 PDF

![[paperPDFs/ICLR_2026/AssetFormer_Modular_3D_Assets_Generation_with_Autoregressive_Transformer.pdf]]

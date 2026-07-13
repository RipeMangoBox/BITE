---
title: Circuit Mechanisms for Spatial Relation Generation in Diffusion Transformers
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Circuit_Mechanisms_for_Spatial_Relation_Generation_in_Diffusion_Transformers.pdf
project_link: null
code_link: "https://github.com/Animadversio/DiT-Relation-Circuits"
aliases:
- CMSRGDT
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 专门化的交叉注意力头（RTE中的L2H8空间关系头、L4H3对象生成头；T5/CLIP中的关系因子向量与对应头，如L3H7）是控制空间关系生成的核心因果开关。
primary_logic: 扩散Transformer根据文本编码器的性质采取截然不同的电路来实现空间关系生成：当编码器无上下文结构时，模型演化出模块化的两阶段电路，先由空间关系头产生位置标签，再由对象生成头赋予属性；当编码器具备语义融合能力时，模型将关系信息吸收进单个对象token，无需显式关系头，但这导致模型对输入扰动高度脆弱。
claims:
- 在RTE-DiT中，消融空间关系头L2H8使关系准确率从67%骤降至33%，而其他头影响甚微，表明该头是空间布局的关键执行者。
- 消融对象生成头L4H3使形状生成准确率从90%降至76%，且效应限定于该头，确认其负责将文本形状信息传递到图像。
- 在T5-DiT中，通过向量算术修改shape2 token中的关系因子向量，可因果地改变生成物体的空间位置，证明关系几何编码在该token中。
- 权重空间筛选（QK内积与梯度模板对齐）无需生成图像即可识别出产生空间梯度的注意力头，并在RTE、T5、CLIP编码器上均验证有效。
---

# Circuit Mechanisms for Spatial Relation Generation in Diffusion Transformers

> [!tip] 核心洞察
> 扩散Transformer根据文本编码器的性质采取截然不同的电路来实现空间关系生成：当编码器无上下文结构时，模型演化出模块化的两阶段电路，先由空间关系头产生位置标签，再由对象生成头赋予属性；当编码器具备语义融合能力时，模型将关系信息吸收进单个对象token，无需显式关系头，但这导致模型对输入扰动高度脆弱。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散Transformer中空间关系生成的电路机制 |
| 英文题名 | Circuit Mechanisms for Spatial Relation Generation in Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.06338) · [Code](https://github.com/Animadversio/DiT-Relation-Circuits) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | 基于注意力综述与权重空间筛查的扩散Transformer电路分析 |
| Dataset | 合成空间关系生成任务（96 prompts, 8种关系）, 预训练模型 PixArt-Sigma |

> [!tip] 效果简介
> - 合成空间关系生成任务（96 prompts, 8种关系） 上，空间关系正确率 (sp rel, loose) RTE-DiT-B 0.843 vs RTE w/o pos 0.415 (+0.428)。
> - 头消融实验 (RTE-DiT-B) 上，关系准确率 消融L2H8后 0.33 vs 原始 0.67 (-0.34)；形状准确率 消融L4H3后 0.76 vs 原始 0.90 (-0.14)。
> - 提示扰动泛化测试 (T5-DiT) 上，关系准确率 添加“the”后 ~0.52 vs 原始 0.925 (≈ -0.40)。

## 概要

文本到图像（T2I）扩散模型在生成符合空间关系描述的图像时表现不稳定，但其内部机制尚不明确。本研究以**扩散Transformer（DiT）** 为对象，采用机制可解释性方法，系统揭示模型如何根据文本提示生成正确的空间关系。

核心发现是：**文本编码器的语义融合方式决定了空间关系生成的电路机制**。当使用无上下文结构的随机编码器（RTE）时，模型演化出模块化的两阶段电路——先由空间关系头产生位置标签，再由对象生成头赋予属性；而当使用预训练编码器（如T5）时，模型将关系信息吸收进单个对象token，无需显式关系头，但这导致对提示词扰动高度脆弱。

研究构建了最小化合成数据集，训练不同规模和编码器的DiT模型，并开发了一套可扩展的分析工具链，包括**注意力综述（Attention Synopsis）**用于快速定位关键注意力头、**权重空间头筛选**用于无需生成图像即可识别编码空间方向的头，以及**方差划分与因子化**用于分解上下文嵌入中的关系特征向量。消融实验和因果操控验证了空间关系头（如RTE-DiT中的L2H8）和对象生成头（如L4H3）的关键作用，并通过向量算术在T5-DiT中因果地改变了生成物体的空间位置。该分析框架为理解和改进T2I模型的空间推理能力提供了新的视角和工具。

文本到图像（T2I）生成模型在单对象属性的视觉呈现上已取得显著进展，但在多对象空间关系生成方面仍存在系统性失败——即使是最先进的开源与闭源模型，在“红色方块在蓝色圆圈的右下方”这类简单空间关系提示上，仍频繁出现对象位置错误或属性绑定混乱。这种失败并非源于模型规模不足，而是源于对扩散Transformer（DiT）内部如何编码和执行空间关系指令的机制理解缺失。

现有研究主要从端到端评估或微调策略的角度审视T2I的空间关系问题，缺乏对模型内部电路级别的因果分析。具体而言，三个关键缺口构成了本研究的直接动机：

**第一，文本编码器对空间关系电路的根本性影响未被揭示。** 扩散模型通常使用预训练语言模型（如T5、CLIP）或随机初始化的嵌入层作为文本编码器，但不同编码器的语义融合方式如何塑造DiT内部的关系生成机制，此前尚无系统研究。

**第二，缺乏可定位空间关系生成模块的分析工具。** 交叉注意力是文本信息流入图像token的主要通道，但其高维张量结构（层×头×时间步×token）使得人工识别负责特定功能的注意力头极为困难。如何在不依赖大量图像生成的前提下，高效筛选出编码空间关系的关键头，是一个方法学空白。

**第三，现有可解释性工作多聚焦于单对象属性，多对象关系电路尚未被解构。** 即便在合成的最小化场景中，模型如何协调“哪个对象”“放在哪里”“具有何种属性”这三个子任务，其内部通信协议和因果连接仍是一个黑箱。

针对上述缺口，本文提出以下研究问题：**扩散Transformer内部是否存在专门化的电路来实现空间关系生成？如果存在，这些电路的架构和运作机制是什么？文本编码器的选择如何决定电路的形态？** 为回答这些问题，我们构建了一个可控的合成数据集，训练了多种编码器配置的DiT模型，并发展了一套结合注意力综述、权重空间筛选、方差划分与因果消融的电路分析框架，旨在从机制层面揭示T2I模型空间关系生成的工作原理与失败根源。

## 核心方法与创新机理

本工作的核心创新不在于提出新的模型架构或训练目标，而在于**首次系统揭示了扩散Transformer（DiT）中空间关系生成的电路机制，并发现该机制由文本编码器的语义融合方式根本性地决定**。这一发现突破了以往仅从行为层面评估文本到图像（T2I）模型空间推理能力的范式，转而从机械可解释性（mechanistic interpretability）的视角，解剖模型内部的计算图与信息流。

### 1. 核心发现：编码器决定电路架构

本研究的中心洞察可概括为：**扩散Transformer根据文本编码器的性质，演化出截然不同的内部电路来实现空间关系生成**。

- **当使用无上下文结构的随机编码器（RTE）时**，模型自发演化出**模块化的两阶段电路**（Fig. 6）：首先由专门化的“空间关系头”（如L2H8）将关系词元（relation token）转化为覆盖图像令牌的空间梯度，充当“位置标签”；随后由“对象生成头”（如L4H3）读取该标签，将形状等属性赋予对应区域的图像令牌。这种电路解耦了“在哪里放置”与“放置什么”两个子任务，表现出高度的模块化与可解释性。

- **当使用具备语义融合能力的预训练编码器（如T5、CLIP）时**，模型则采用**融合式电路**：编码器的自注意力机制将空间关系信息直接吸收进单个对象词元的上下文化嵌入（如shape2 token）中，模型无需专门的“关系头”即可从该嵌入中解码出空间布局。这种电路虽然简洁，但导致模型对提示词的微小扰动（如添加无关词“the”）极度敏感——实验表明，T5-DiT的关系准确率因此下降约40%（Section A.8, Fig. 26B, Tab. 2），而RTE-DiT几乎不受影响。

这一发现的方法论意义在于：**文本编码器的选择不仅是性能调优的超参数，更从根本上塑造了模型内部的计算结构、鲁棒性与可解释性**。这为T2I模型的架构设计提供了全新的审视维度。

### 2. 方法论创新：面向扩散Transformer的电路分析工具箱

为支撑上述发现，本文发展了一套无需依赖大量生成样本即可定位关键电路模块的分析方法体系：

- **注意力综述（Attention Synopsis）**：将海量交叉注意力张量按语义类别（如“关系词元”“对象图像令牌”）聚合，并在扩散时间维上平均，压缩为层×头矩阵，从而快速定位信息流动的关键通道（Section 4.1, Fig. 3A）。

- **权重空间头筛选（Weight-space Head Screening）**：利用位置嵌入与文本特征向量的QK内积，直接评估各注意力头是否编码空间方向，无需实际生成图像。该方法在RTE、T5、CLIP三种编码器上均验证有效（Section B.7, Figs. 22-25），为大规模模型的电路发现提供了高效路径。

- **方差划分与因子化（Variance Partitioning）**：通过多变量方差分析，将上下文化嵌入分解为形状、颜色、关系等可加因子，用于定位关系特征向量并解释表示空间（Section B.6, Tab. 1）。该技术直接支撑了T5-DiT中“关系因子向量”的发现与因果操控。

- **消融与因果操控**：通过选择性移除注意力贡献（如消融L2H8使关系准确率从67%降至33%，Fig. 4D）、注入关系头输出（Fig. 5C）或对因子化嵌入进行向量算术（Fig. 7C），建立了电路模块间的因果链条。

### 3. 与既有工作的本质差异

相较于已有的T2I模型空间关系评估工作（多聚焦于基准测试分数或提示工程），本研究的根本性差异在于：

- **从“模型做什么”深入到“模型如何做”**：不满足于报告关系准确率的高低，而是揭示模型内部的计算分工、信息路由与因果结构。
- **发现编码器类型作为电路架构的“分岔点”**：这一发现无法通过常规的行为测试获得，它解释了为何相同DiT骨干在不同编码器下表现出迥异的鲁棒性特征。
- **提供可迁移的分析范式**：Attention Synopsis与权重空间筛选方法不依赖特定模型规模或任务，为未来在更大规模模型（如DiT-XL、SDXL）上开展电路分析提供了方法论基础。

综上，本工作的核心创新在于**以电路机制为透镜，重新审视了T2I模型空间推理能力的本质，并揭示了文本编码器在这一过程中的结构性角色**——这是对既有空间关系评估范式的根本性补充与深化。

本文构建了一套系统性的电路分析管线，旨在揭示扩散Transformer（DiT）如何在文本到图像生成中实现空间关系推理。整个框架围绕三个核心环节展开：**可控训练环境构建**、**注意力行为综述与头筛选**，以及**因果验证与机制对比**。

### 1. 受控实验环境

研究首先构建了一个最小化的合成数据集，所有样本采用统一的提示模板：`[描述符A] [物体A] [关系] [描述符B] [物体B]`（例如“red square above and to the left of blue circle”），涵盖8种空间关系和多种属性组合。在此数据集上，从零开始训练不同规模的DiT模型（采用PixArt架构），并系统性地更换文本编码器——包括**随机标记嵌入（RTE）**、**预训练T5**和**CLIP**——以隔离编码器语义结构对下游电路形成的影响。所有模型使用相同的训练超参数、随机种子和评估协议（DPM-Solver++, 14步, CFG 4.5），确保对比的公平性。

### 2. 注意力综述与权重空间筛查

面对海量的交叉注意力张量，研究提出了**注意力综述（Attention Synopsis）**方法（Fig. 3A）：利用图像token的目标分割标签和文本token的语义类别，将注意力按类别聚合并在扩散时间步上平均，压缩为层×头矩阵，从而快速定位关键的通信模式。在此基础上，进一步开发了**权重空间头筛选（Weight-space Head Screening）**技术（Fig. 3B）：通过计算位置嵌入与关系因子向量的QK内积，并将其与理想方向梯度模板进行余弦相似度比对（公式 $\rho_m^{(l,h)} = \frac{\langle \bar{\Phi}_m, \bar{T}_m \rangle_F}{\|\bar{\Phi}_m\|_F \cdot \|\bar{T}_m\|_F}$），无需生成图像即可直接评估各注意力头是否编码空间方向信息。

### 3. 表示分解与因果操控

对于预训练编码器模型，研究引入**方差划分（Variance Partitioning）**技术（Tab. 1）：通过多变量分析将上下文嵌入分解为形状、颜色、关系等可加因子（$V_{\text{shape2}}^* = V_{\text{shape2}} + V_{\text{color2}} + V_{\text{shape1}} + V_{\text{rel}}$），利用偏η²效应量量化各因子对表示变异的独特贡献。因果验证则通过选择性消融注意力头、遮蔽文本token、以及向量算术操控关系因子来实现——例如，将shape2 token中的关系因子替换为另一关系的因子，可因果地改变生成物体的空间位置（Fig. 7C）。

### 4. 双电路机制的发现

该管线最终揭示了两条截然不同的电路机制：**RTE-DiT**演化出模块化的两阶段电路——空间关系头（L2H8）先产生位置梯度标签，对象生成头（L4H3）再据此赋予属性（Fig. 6）；而**T5-DiT**则利用编码器的语义融合能力，将关系信息吸收进shape2 token的上下文嵌入中，通过权重空间筛选出的关系头（L3H7）直接解码空间布局，无需显式的关系token注意力。这一发现构成了全文的核心洞察：**文本编码器的性质决定了扩散Transformer实现空间关系生成的电路拓扑**。

![[assets/figures/papers/paper_list_l2450_https_arxiv_org_abs_2601_06338/figures/006_Figure_6.jpg]]
*Figure 6: Schematics of the object relation circuit in DiT trained with random embedding*

![[assets/figures/papers/paper_list_l2450_https_arxiv_org_abs_2601_06338/figures/001_Figure_1.jpg]]
*Figure 1: Schematics of the model and task. Our T2I model architecture adopted the design of PixArt [5]. There are three main components: the text encoder that processes tokenized natural language prompts into text embeddings, the VAE that processes image inputs into image tokens, and the Diffusion Transformer (DiT) which is the backbone of the denoising diffusion process. The text information routes through the cross attention mechanism in each DiT block and influence the denoising of image tokens. The task is to generate two objects with a specified spatial relation*

![[assets/figures/papers/paper_list_l2450_https_arxiv_org_abs_2601_06338/figures/033_Figure_30.jpg]]
*Figure 30: Pre-trained T2I models (A) The prompt set construction and evaluation pipeline. (B) Object and relation accuracy across various object pairs for the PixArt-Sigma model. (C) A text token ablation analysis demonstrating how masking specific tokens affects object and relation accuracy. (D) Projection scores used to identify salient spatial relation heads within the model’s layers*

### 分析流水线总览

本文提出了一套从“注意力模式发现”到“因果操控验证”的完整电路分析流水线。该流水线由四个核心模块构成，依次递进：首先通过**注意力综述**压缩海量注意力张量以定位关键头，随后利用**权重空间头筛选**在不生成图像的前提下高效识别空间关系头，进而借助**方差划分与因子化**对上下文嵌入进行可解释分解，最终通过**消融与因果操控**验证电路模块间的因果关系。

### 注意力综述 (Attention Synopsis)

交叉注意力张量的原始维度为 $\text{layers} \times \text{heads} \times \text{image tokens} \times \text{text tokens}$，直接分析成本极高。注意力综述的核心操作是**按语义类别聚合**：利用图像token可通过物体分割归类、文本token可通过语义属性归类的特性，将注意力在类别内求和，并在扩散时间步上平均，最终压缩为 $\text{layer} \times \text{head}$ 的矩阵。这一压缩使得特定通信模式（如“物体图像token → 关系文本token”）能够在层-头热力图中一目了然地呈现，从而快速定位空间关系头和对象生成头（Section 4.1, Fig. 3A）。

### 权重空间头筛选 (Weight-space Head Screening)

为规避生成图像的昂贵开销，本文提出一种**纯权重空间的筛选方法**。其核心思想是：若某一交叉注意力头编码了空间方向，则其QK内积应在图像token上产生与目标关系一致的空间梯度。具体而言，利用位置嵌入 $E_{\text{pos}}$ 经查询投影 $W_q$ 变换，关系因子向量 $V_{\text{rel}}$ 经键投影 $W_k$ 变换，计算二者的内积：

$$\text{QK alignment: } (W_q E_{\text{pos}})^\top (W_k V_{\text{rel}})$$

该内积产生一个空间注意力图，其梯度方向反映空间关系（如“above”产生纵向梯度）。将该图与理想方向梯度模板计算余弦相似度，即可量化每个头的空间编码能力：

$$\rho_m^{(l,h)} = \frac{\langle \bar{\Phi}_m, \bar{T}_m \rangle_F}{\|\bar{\Phi}_m\|_F \cdot \|\bar{T}_m\|_F}$$

其中 $\bar{\Phi}_m$ 为注意力图，$\bar{T}_m$ 为理想梯度模板，$\langle\cdot,\cdot\rangle_F$ 为Frobenius内积。该方法在RTE、T5、CLIP三种编码器上均验证有效（Section B.7, Figs. 22-25），且无需任何图像生成步骤。

### 方差划分与因子化 (Variance Partitioning)

为解释预训练编码器（T5）的上下文嵌入如何编码空间关系，本文采用多变量方差分析（ANOVA）对shape2 token的嵌入进行加性分解。该分解将嵌入表示为四个正交因子的线性叠加：

$$V_{\text{shape2}}^* = V_{\text{shape2}} + V_{\text{color2}} + V_{\text{shape1}} + V_{\text{rel}}$$

各因子的独立贡献通过偏 $\eta^2$ 效应量量化：

$$\eta_{p,f}^2 = \frac{SS_f^{\text{part}}}{SS_f^{\text{part}} + SS_{\text{resid}}}$$

其中 $SS_f^{\text{part}}$ 为因子 $f$ 在控制其他因子后的偏平方和，$SS_{\text{resid}}$ 为残差平方和。实验表明，在T5编码器的shape2 token中，形状因子解释约37.5%的方差，关系因子贡献约12%（Table 1）。这一分解揭示了预训练编码器将关系信息**融合**进单个对象token的机制，为后续的向量算术操控提供了特征基础。

### 消融与因果操控

因果验证通过两类操作实现：**选择性消融**和**向量注入/替换**。消融实验通过移除特定注意力头的输出贡献来验证其功能必要性——例如消融空间关系头L2H8使关系准确率从67%降至33%（Fig. 4D），消融对象生成头L4H3使形状准确率从90%降至76%（Fig. 5D）。向量操控则利用方差划分提取的关系因子 $V_{\text{rel}}$，对shape2 token嵌入进行算术替换（如将“above”的关系因子替换为“below”的关系因子），从而因果地改变生成图像中物体的空间位置（Fig. 7C）。此外，注入关系头的输出到位置嵌入可激活对象生成头的选择性注意力，验证了“空间关系头→位置标签→对象生成头”的模块化信号流（Fig. 5C）。

### 提示扰动下的嵌入位移

为量化融合式电路对输入扰动的敏感性，本文定义了添加无关词“the”后shape2 token嵌入的平均偏移：

$$\Delta V_{\text{the2}} := \mathbb{E}[V_{\text{shape2,the}}^* - V_{\text{shape2}}^*]$$

实验发现该偏移向量与关系因子方向高度对齐，解释了T5-DiT在添加“the”后关系准确率下降约40%的系统性偏差（Section A.8, Fig. 26B），而采用模块化电路的RTE-DiT几乎不受影响。

![[assets/figures/papers/paper_list_l2450_https_arxiv_org_abs_2601_06338/figures/008_Figure_7.jpg]]
*Figure 7: Mechanism for relational generation in T5-DiT. A. T5-based DiT is robust to attention ablation of relation word, but most sensitive to shape2 and EOS. B. Weight space screening for spatial relation heads via projection score, and its corresponding spatial gradients (L3H7). C. Vector arithmetic on factorized word embedding causally affects generated object relation*

## 实验与关键发现

### 实验设置与评估协议

本研究构建了一个最小化的合成文本-图像数据集，所有提示遵循固定模板 `[描述词A] [物体A] [关系] [描述词B] [物体B]`，例如“red square above and to the left of blue circle”。数据集涵盖8种空间关系（above, below, left, right 及其组合）与多种形状、颜色组合，共计264条提示。所有模型在相同数据集、训练超参数和随机种子上从零开始训练，推理统一使用 DPM-Solver++（14步，CFG 4.5），并在多个噪声种子上评估，确保不同文本编码器配置间的公平对比。评估指标包括：唯一属性绑定准确率（bind）、宽松空间关系准确率（sp rel）、严格空间关系准确率（sp rel+），以及两物体坐标差 Dx、Dy（单位像素，共128像素），指标通过传统 CV2 分割与分类工具计算。

### 主实验结果

#### 不同文本编码器的性能对比

Table 2 汇总了各模型配置的全面评估结果。使用随机token嵌入加位置编码的 RTE-DiT-B 在宽松空间关系准确率上达到 **0.843**，而移除位置编码后骤降至 **0.415**（Δ = -0.428），表明位置编码是 RTE 模型实现空间关系生成的关键结构先验。T5-DiT-B 同样取得了强绑定与空间关系准确率，证明预训练语义结构并非学习物体关系的必要条件。值得注意的是，训练动力学（Figure 2）揭示了统一的学习阶段顺序：颜色准确率最先收敛，其次是形状，然后是唯一绑定，空间关系学习最慢——这一规律在 RTE 和 T5 两种编码器下均成立。

#### 预训练模型的泛化基准

Figure 8 展示了开源与闭源模型在空间关系和物体属性上的基准分数。在 PixArt-Sigma（30种物体对）上，仅 **8/30** 的物体对表现出非平凡的准确率，说明即使是大规模预训练模型，其空间关系生成能力仍然薄弱。这一结果为分析框架在强模型上的适用性提供了观察基点，但也构成了当前研究的局限性之一。

![[assets/figures/papers/paper_list_l2450_https_arxiv_org_abs_2601_06338/figures/009_Figure_8.jpg]]
*Figure 8: Benchmark scores of spatial relationship and object feature attributes of open- and closed- source models. Color of dots denote the text encoder*

### 关键消融实验

#### RTE-DiT 的电路消融

对 RTE-DiT-B 的空间关系头 L2H8 进行消融，使关系准确率从 **67% 降至 33%**（Figure 4D），而其他注意力头几乎无影响，确认该头是空间布局的关键执行者。消融对象生成头 L4H3 则使形状生成准确率从 **90% 降至 76%**（Figure 5D），效应同样限定于该头，验证其负责将文本形状信息传递到图像。这两项消融共同确立了 RTE-DiT 中“关系头→位置标签→对象生成头→属性赋值”的模块化电路结构（Figure 6）。

#### T5-DiT 的令牌遮蔽实验

在 T5-DiT 中，遮蔽 shape2 token 导致形状、绑定和关系准确率均下降约 **50%**（Figure 7A），而遮蔽关系词 token 的影响甚微。这表明 T5 编码器已将关系信息融合进 shape2 的上下文嵌入中，DiT 从该 token 解码空间关系，而非通过专门的关系注意力头。

#### 提示扰动泛化测试

添加无关词“the”使 T5-DiT 的关系准确率从 **0.925 下降约 40%**（至约 0.52，Figure 26B, Table 2），而 RTE-DiT 几乎不受影响。该现象揭示了融合式电路的核心脆弱性：当编码器将关系信息吸收进对象 token 后，任何改变 token 上下文分布的微小扰动都会通过自注意力机制传播，导致关系编码产生系统性偏差。方差分析证实，添加“the”引起的 shape2 token 嵌入偏移（$$\Delta V_{\text{the2}}$$）恰好与关系因子方向对齐，从而解释了准确率的定向下降。

### 权重空间筛选的跨编码器验证

权重空间头筛选方法（通过 QK 内积与梯度模板的余弦相似度 $$\rho_m^{(l,h)}$$）在 RTE、T5 和 CLIP 三种编码器上均无需生成图像即可识别出产生空间梯度的注意力头（Section B.7, Figures 22-25），验证了该方法的编码器无关性。在 T5-DiT 中，L3H7 被识别为空间关系头，其产生的空间梯度图与目标关系方向一致（Figure 7B）。

### 方差划分与向量算术的因果证据

Table 1 对 T5 嵌入和 DiT-MLP 投影中 shape2 token 的方差划分显示：在 T5 嵌入层面，shape2 本身解释约 **37.5%** 的偏 η² 效应量，关系因子贡献约 **12.1%**；经 DiT-MLP 投影后，关系因子的贡献进一步提升。基于此分解的向量算术实验（Figure 7C）提供了最强因果证据：将 shape2 token 嵌入中的关系因子向量替换为另一关系的因子，可以因果地改变生成图像中物体的空间位置，证明关系几何编码确实存在于该 token 的加性因子中。

![[assets/figures/papers/paper_list_l2450_https_arxiv_org_abs_2601_06338/figures/007_Table_1.jpg]]
*Table 1: Variance partitioning of T5 embedding and DiT-MLP projection of shape2 token*

### 失败模式与局限性

1. **合成数据集的局限**：所有电路分析均在最小化合成数据集上进行，未在复杂真实图像或自然语言场景下验证，电路发现的生态效度需要进一步检验。
2. **架构泛化性**：分析局限于 PixArt 风格的 DiT 架构，尚未扩展到 U-Net 等其他生成模型，Attention Synopsis 和权重空间筛选方法的跨架构适用性仍是开放问题。
3. **模型规模**：训练的最大模型仅为 DiT-B，尚未探索 DiT-XL 等更大规模下的电路行为，大规模模型可能出现电路重组或涌现新的通信模式。
4. **方差划分的零和约束**：线性加性模型的零和约束可能对关系特征向量的符号解释引入偏差，其在非线性表示空间中的真实因子化程度需用无监督方法（如稀疏自编码器）进一步验证。
5. **预训练模型的弱空间关系能力**：PixArt-Sigma 上仅 8/30 物体对表现出非平凡准确率，限制了分析框架在强模型上的验证深度，也提示当前预训练范式在空间组合性上存在系统性缺陷。

## 定位与知识库关联

### 1. 方法论定位：机械论可解释性在生成模型中的应用

本文的工作属于**机械论可解释性**（mechanistic interpretability）在扩散生成模型中的开创性应用。与传统的特征归因或显著性图方法不同，该研究直接追溯了文本到图像扩散Transformer（DiT）内部交叉注意力头所实现的因果电路，揭示了空间关系生成从文本编码器到像素布局的完整信息流。

在方法论谱系上，该工作继承了以下三条线索：

- **Transformer电路分析范式**：受语言模型中电路发现工作的启发（如对GPT-2中induction heads的分析），本文将其推广到视觉生成领域。核心创新在于提出了面向扩散模型的专用分析工具链——**注意力综述**（Attention Synopsis）和**权重空间头筛选**（Weight-space Head Screening），前者通过类别聚合和时间平均将海量交叉注意力张量压缩为层×头摘要矩阵，后者利用QK内积与梯度模板的余弦相似度在无需生成图像的情况下直接评估各头的空间编码能力。

- **文本编码器对下游模型行为的影响**：该研究系统对比了三种文本编码条件——随机token嵌入（RTE）、预训练T5编码器和预训练CLIP编码器——对DiT内部电路组织方式的决定性影响。这一视角与近期关于“文本编码器质量如何塑造多模态模型内部表示”的研究方向一致，但本文首次将其与电路层面的因果机制直接关联。

- **表示空间的因子化解构**：通过多变量方差划分（偏η²效应量），将T5的上下文嵌入分解为形状、颜色、关系等可加因子，这与语言模型中的线性表示假设和向量算术研究形成呼应。然而，本文进一步证明了这些因子向量可以通过因果操控（替换关系因子）直接改变生成图像中物体的空间位置。

### 2. 与基线工作的关系

本文未直接对比其他可解释性方法，而是将自身定位为一种**发现性分析框架**。其核心对照实验围绕文本编码器的选择展开：

- **RTE-DiT vs. T5-DiT vs. CLIP-DiT**：在相同数据集、训练超参数和随机种子上从零开始训练，确保编码器效应的公平对比。结果表明，编码器的语义融合能力从根本上决定了电路架构——RTE模型演化出模块化的两阶段电路（空间关系头→对象生成头），而T5/CLIP模型将关系信息吸收进单个对象token，形成更紧凑但更脆弱的融合式电路。

- **位置编码的消融**：RTE移除位置编码后，空间关系准确率从0.843降至0.415（Table 2），证实了位置信息在模块化电路中的关键作用，也间接解释了为何预训练编码器模型可以部分绕过对显式位置编码的依赖。

### 3. 适用边界与局限

该分析框架的适用边界受到以下因素严格约束：

**架构边界**：所有分析均在PixArt风格的DiT架构上进行，尚未扩展到U-Net等广泛使用的生成模型。DiT的全注意力机制可能对电路发现更为友好，而U-Net的卷积归纳偏置可能产生不同的内部通信模式。

**规模边界**：训练的最大模型仅为DiT-B（约130M参数），尚未探索DiT-XL或更大规模下的电路行为。小模型中发现的功能专一化头在大模型中可能分裂为更细粒度的多头协作模式。

**任务边界**：实验仅在合成的最小化数据集上进行（96个提示词，8种空间关系，有限物体和颜色组合），未在复杂真实图像或自然语言场景下验证。预训练模型PixArt-Sigma在30种物体对中仅8对表现出非平凡的空间关系能力（Fig. 30B），表明该框架在强模型上的适用性尚待证实。

**方法边界**：
- 方差划分的零和约束可能对关系特征向量的符号解释带来偏差，其线性加性模型在多大程度上真实反映非线性表示空间的因子化仍需研究。
- 权重空间筛选依赖预定义的方向梯度模板，对于非欧几里德或拓扑性空间关系（如“环绕”、“之间”）的推广性未知。
- 注意力综述的类别聚合假设同类token共享相似的通信模式，这一假设在细粒度或歧义性场景中可能失效。

### 4. 开放问题

本文揭示的电路机制引出了若干深层问题：

**表示空间的因子化本质**：T5的自注意力如何将关系信息分配到shape2 token之外的其他token？能否解耦出更稳健的融合方式，使预训练模型兼具模块化电路的鲁棒性和融合式电路的紧凑性？方差划分的线性加性假设能否通过无监督方法（如稀疏自编码器）进行验证和规避？

**电路发现的规模化**：能否将基于注意力综述和权重空间筛选的电路分析推广到U-Net架构或SDXL等更大规模模型？在更大模型中，功能专一化头是否会演化为更复杂的多头协作模式，需要更精细的电路追踪技术？

**从脆弱到稳健的迁移**：在真实世界的多物体场景中，预训练模型的“融合式电路”能否通过微调或编码器改进转化为更稳固的“模块化电路”？提示扰动实验表明T5-DiT对无关词“the”的添加极度敏感（关系准确率下降约40%），这一脆弱性是否源于预训练编码器在训练期间形成的不可逆的结构性偏差？

**电路与生成质量的关系**：本文聚焦于空间关系的正确性，但未探讨电路组织方式如何影响生成图像的视觉质量、多样性和组合泛化能力。模块化电路是否在更复杂的组合场景中展现出更好的系统性泛化？

## 原文 PDF

![[paperPDFs/CVPR_2026/Circuit_Mechanisms_for_Spatial_Relation_Generation_in_Diffusion_Transformers.pdf]]

---
title: Text-guided Feature Disentanglement for Cross-modal Gait Recognition
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Text_guided_Feature_Disentanglement_for_Cross_modal_Gait_Recognition.pdf
project_link: null
code_link: null
aliases:
- TGFDCMGR
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 通过构建步态模态文本字典（GMTD）并利用CLIP对齐视觉与文本嵌入，使文本描述作为语义锚点，引导特征解耦，从而分离出模态共享表示。
primary_logic: 利用文本先验指导残差分解和正交约束，强制解耦出的模态共享特征既具有判别性又能抵抗噪声，配合稳定性增强模块提升鲁棒性。
claims:
- 在SUSTech1K数据集上，TCFDNet在2D→3D和3D→2D两个方向上均达到新的最优结果（Rank-1 55.9%和61.7%），显著超越先前方法。
- 消融研究表明，移除GMTD模块导致性能显著下降，验证了文本先验的必要性。
- t-SNE可视化显示TCFDNet的2D和3D特征在共享空间中聚类更紧凑，类间距离更大。
- SUSTech1K (2D→3D) 上 Rank-1 accuracy (%) = 55.9
---

# Text-guided Feature Disentanglement for Cross-modal Gait Recognition

> [!tip] 核心洞察
> 利用文本先验指导残差分解和正交约束，强制解耦出的模态共享特征既具有判别性又能抵抗噪声，配合稳定性增强模块提升鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文本引导的特征解耦用于跨模态步态识别 |
| 英文题名 | Text-guided Feature Disentanglement for Cross-modal Gait Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lu_Text-guided_Feature_Disentanglement_for_Cross-modal_Gait_Recognition_CVPR_2026_paper.html) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | TCFDNet |
| Dataset | SUSTech1K, FreeGait |

> [!tip] 效果简介
> - SUSTech1K (2D→3D) 上，Rank-1 accuracy (%) 55.9。
> - SUSTech1K (3D→2D) 上，Rank-1 accuracy (%) 61.7。
> - FreeGait (2D→3D) 上，Rank-1 accuracy (%) 52.1。

## 概要

跨模态步态识别旨在实现2D相机（RGB视频）与3D LiDAR（点云）之间的身份匹配，在视频监控与安防场景中具有重要价值。然而，两种模态之间存在显著的**模态差异**——RGB图像包含丰富的纹理和颜色信息，而LiDAR点云仅提供稀疏的几何结构——导致传统单模态步态识别方法难以直接迁移。现有跨模态方法通常依赖对比学习或共享原型训练，所提取的特征高度纠缠，未能有效分离模态共享的判别性信息与模态特有的噪声成分，识别精度受限。

针对上述瓶颈，本文提出**TCFDNet**（Text-guided Cross-modal Feature Disentanglement Network），核心思路是引入文本先验作为语义锚点，引导视觉特征的显式解耦。具体而言，方法包含三个关键创新：首先，利用大语言模型构建**步态模态文本字典**（GMTD），为不同模态和视角生成丰富的语义描述；其次，设计**文本引导特征解耦**（TFD）模块，通过文本相似度重构模态特有特征，并以残差分解和正交约束分离出纯净的模态共享表示；最后，引入**特征稳定性增强**（FSE）模块，对共享特征进行空间-通道联合建模以提升鲁棒性。

在**SUSTech1K**数据集上，TCFDNet在2D→3D和3D→2D两个跨模态方向上分别取得55.9%和61.7%的Rank-1准确率，均达到新的最优水平，显著超越CL-Gait（需额外合成数据预训练）等先前方法。在**FreeGait**数据集上同样取得最优结果，验证了方法的泛化能力。消融实验表明，移除GMTD文本字典或TFD解耦模块均导致性能大幅下降，证实了文本先验引导解耦策略的有效性。t-SNE可视化进一步显示，TCFDNet的2D和3D特征在共享空间中聚类更紧凑、类间距离更大，表明解耦后的共享特征具有更强的判别性。

步态识别是一种通过个体行走模式进行远距离身份认证的生物特征技术，在安防监控、智慧城市等领域具有重要应用价值。传统步态识别主要依赖RGB相机捕获的2D视频序列，但2D视觉模态对光照变化、视角偏移、遮挡和衣着变化等因素高度敏感，导致真实场景下的鲁棒性不足。近年来，LiDAR传感器凭借其对光照不敏感、能提供精确三维几何信息的优势，逐渐被引入步态识别任务，形成了2D相机与3D LiDAR并存的跨模态步态识别新范式。

跨模态步态识别的核心瓶颈在于：LiDAR点云与RGB视频之间存在显著的模态差异——前者捕获稀疏的三维空间结构，后者记录稠密的二维纹理外观，二者在数据分布和特征表达上天然异构。现有方法，如**CL-Gait**（Guo et al., ECCV 2024）和**CrossGait**（Wang et al., IJCB 2024），通常采用对比学习或共享原型训练来对齐两种模态的特征空间，但这类方法提取的视觉特征高度纠缠，模态特有信息与共享的判别性步态线索混杂在一起，难以有效分离出真正对身份识别有用的跨模态不变表示。此外，这些方法普遍缺乏额外的语义先验来指导特征解耦过程，仅依赖视觉信号自身的统计对齐，导致在面对复杂场景（如昼夜变化、视角突变）时性能退化明显。

本文的动机源于一个关键洞察：**文本描述可以作为语义锚点，引导视觉特征向模态共享方向解耦**。具体而言，人类可以用自然语言描述“一个人在LiDAR点云中呈现的步态轮廓”与“同一个人在RGB视频中呈现的步态外观”，这些文本描述天然地抽象掉了模态特有的底层细节，保留了跨模态共享的高层语义。基于此，本文提出**TCFDNet**（Text-guided Cross-modal Feature Disentanglement Network），核心思路是利用大语言模型（LLM）构建一个**步态模态文本字典（GMTD）**，为每种模态和视角生成丰富的语义描述，再通过CLIP模型将文本嵌入与视觉嵌入对齐，以文本先验显式地指导特征解耦——将视觉特征分解为模态共享的判别性分量和模态特有的噪声分量，从而在跨模态检索中获得更鲁棒、更具区分度的表示。

## 核心方法与创新机理

TCFDNet 的核心创新在于将**文本先验**引入跨模态步态特征解耦，通过构建模态感知的语义锚点，引导模型显式分离模态共享特征与模态特有特征，从而解决 LiDAR 点云与 RGB 视频之间因模态差异导致的判别性特征提取困难。

### 创新一：文本先验驱动的特征解耦范式

现有跨模态步态识别方法（如 **CL-Gait**（Guo et al., ECCV 2024）、**CrossGait**（Wang et al., IJCB 2024））通常依赖直接对比学习或共享原型训练，特征高度纠缠，难以有效隔离模态共享的判别性信息。TCFDNet 提出了一种**文本引导特征解耦（TFD）模块**，其核心机制如下（见 Figure 5）：

1. **模态特有特征重构**：利用 GMTD 生成的文本嵌入作为语义锚点，通过余弦相似度选择与输入特征最相关的 top-kt 文本原型，重构模态特有的视觉语义。
2. **残差分解得共享特征**：将原始特征减去重构的模态特有特征，获得模态共享表示：
   $$F_{(shared)_i^m} = \tilde{u}_i^m - \widetilde{F}_{(mod)_i^m}$$
3. **正交与独立性约束**：通过正交损失和 HSIC 独立性损失强制共享特征与特有特征之间的低相关性，确保解耦质量。

这种“文本锚定→特有重构→残差分解”的级联机制，使得解耦出的共享特征既保留判别性又抑制模态噪声，是该方法区别于现有工作的根本性设计。

### 创新二：Gait Modality Text Dictionary（GMTD）的构建与注入

TCFDNet 首次将大语言模型（LLM）引入步态识别，构建了**模态与视角感知的文本字典**（见 Figure 1, Figure 2）。GMTD 包含 $m \times 8 \times l$ 个条目，形式化定义为：
$$\mathrm{GMTD} = \{ t_j^m \mid m \in \{2d, 3d\}, j = 1, 2, \ldots, 8l \}$$

通过精心设计的指令（包含 formulation、protocol 和 examples 三部分），LLM 生成描述不同模态、不同视角下步态外观的丰富文本。这些文本经冻结的 CLIP 文本编码器嵌入后，作为 TFD 模块的语义锚点。消融实验（Table 4）表明，移除 GMTD 导致性能显著下降，直接验证了文本先验对解耦过程的必要性。

### 创新三：特征稳定性增强（FSE）模块

分解后的共享特征直接用于检索时，对局部噪声和通道冗余较为敏感。TCFDNet 在解耦后引入 **FSE 模块**（Figure 6），通过空间卷积捕获局部感受野依赖，配合通道门控机制建模全局通道相关性，提升共享特征的鲁棒性。消融实验（Table 4）证实 FSE 模块对最终精度有正向贡献。

### 创新四：跨模态 Patch 交换增强

在训练阶段，TCFDNet 采用跨模态 Patch 交换策略，随机混合 2D 和 3D 图像的区域（见 Section 3.1 概述及 Supplementary）。这一数据增强方式迫使模型学习模态不变的表征，进一步提升跨模态泛化能力。消融实验（Table 4 中 PE ablations）验证了该策略的有效性。

### 与 baseline 的核心差异总结

| 设计维度 | 现有方法 | TCFDNet |
|---------|---------|---------|
| 特征解耦方式 | 隐式对比学习/共享原型，特征纠缠 | 文本引导的显式残差分解+正交约束 |
| 先验注入 | 无额外先验或仅视觉信息 | LLM 构建的 GMTD 提供模态-视角语义锚点 |
| 解耦后处理 | 直接用于检索 | FSE 模块增强空间与通道鲁棒性 |
| 数据增强 | 常规增强 | 跨模态 Patch 交换混合训练 |

这些创新共同构成了 TCFDNet 的技术壁垒：文本先验提供了解耦的语义指导，残差分解保证了共享特征的纯度，FSE 与 Patch 交换则提升了特征的鲁棒性与泛化性。

TCFDNet 的整体架构围绕一个核心思想构建：**利用文本先验作为语义锚点，引导跨模态视觉特征解耦**，从而分离出模态共享的判别性步态表示。如图 3 所示，框架由六个关键模块串联而成，形成“视觉编码→多粒度融合→文本引导解耦→稳定性增强→联合优化”的完整推理链。

### 输入与数据流

给定训练集 $X = \{ x_i^{2d}, x_i^{3d}, y_i \mid i = 1, 2, \ldots, n \}$，其中 $x_i^{2d}$ 和 $x_i^{3d}$ 分别表示同一行人的 RGB 视频序列和 LiDAR 点云序列，$y_i$ 为身份标签。两个模态的数据分别经过**共享权重**的视觉编码器，但在此之前，训练时采用跨模态 Patch 交换策略（Cross-modal Patch Exchange），在 2D 和 3D 输入之间随机交换局部区域，以增强模型对模态差异的泛化能力。

### 模块关系与推理流程

**第一步：多粒度视觉编码。** 每个模态的输入先经冻结的 CLIP 视觉编码器提取全局粗粒度特征 $g_i^m = \mathrm{CLIP}_v(x_i^m)$，同时通过 Adapter 和 ResNet 分支提取细粒度局部特征。随后，**Multi-grained Fusion (MF) 模块**通过多头交叉注意力机制（MCA）融合全局与局部信息，再经**Spatial Weighting (SW) 模块**生成空间注意力图，对特征进行加权重标定，得到 $\tilde{u}_i^m$。

**第二步：文本先验注入。** 并行地，预构建的**Gait Modality Text Dictionary (GMTD)** 存储了模态感知和视角感知的文本描述原型。冻结的 CLIP 文本编码器将这些文本原型嵌入为 $v_j^m$。通过计算 $\tilde{u}_i^m$ 的 CLS 特征与 $v_j^m$ 的余弦相似度，选择 top-$k_t$ 个最相关的文本原型，作为后续解耦的语义指导。

**第三步：文本引导特征解耦。** 这是框架的核心瓶颈突破点。**Text-guided Feature Disentanglement (TFD) 模块**利用选中的文本原型，通过文本-视觉相似度重构出模态特有特征 $\widetilde{F}_{(mod)_i^m}$，再通过残差分解获得模态共享特征：
$$F_{(shared)_i^m} = \tilde{u}_i^m - \widetilde{F}_{(mod)_i^m}$$
同时施加正交约束和 HSIC 独立性约束，强制共享特征与特有特征相互正交且统计独立。

**第四步：稳定性增强。** 分解得到的共享特征 $F_{(shared)_i^m}$ 并非直接用于检索，而是送入**Feature Stability Enhancement (FSE) 模块**。该模块通过空间卷积捕获局部感受野依赖，再通过通道门控机制建模全局通道相关性，最终输出鲁棒的模态共享表示。

**第五步：联合优化。** 训练时，总损失函数为五项损失的加权组合：
$$\mathcal{L}_{all} = \gamma_1(\mathcal{L}_{tri} + \mathcal{L}_{ce}) + \gamma_2 \mathcal{L}_{align}^m + \gamma_3(\mathcal{L}_{ortho}^m + \mathcal{L}_{HSIC}^m)$$
其中 $\mathcal{L}_{tri}$ 和 $\mathcal{L}_{ce}$ 保证判别性，$\mathcal{L}_{align}^m$ 对齐视觉与文本嵌入，$\mathcal{L}_{ortho}^m$ 和 $\mathcal{L}_{HSIC}^m$ 保证解耦质量。默认权重为 $\gamma_1 = 1.0$，$\gamma_2 = 0.5$，$\gamma_3 = 0.1$。

### 因果机制总结

整个框架的因果逻辑链为：**GMTD 提供语义锚点 → TFD 以文本相似度为引导重构模态特有特征 → 残差分解自然剥离出模态共享特征 → FSE 增强共享特征的鲁棒性**。消融实验（Table 4）证实，移除 GMTD 会导致性能显著下降，验证了文本先验是驱动特征解耦的因果旋钮。

![[assets/figures/papers/paper_list_l1081_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_Text_guided_Feature/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the proposed framework*

### 整体框架与数据定义

TCFDNet 的训练输入定义为成对的 2D 和 3D 步态序列：

$$
X = \left\{ x _ { i } ^ { 2 d } , x _ { i } ^ { 3 d } , y _ { i } \mid i = 1 , 2 , \ldots , n \right\}
$$

其中 $y_i$ 为身份标签。框架（Figure 3）由多粒度特征编码器、步态模态文本字典（GMTD）、文本引导特征解耦（TFD）模块和特征稳定性增强（FSE）模块构成，通过联合损失函数优化。

### 多粒度特征编码器

编码器采用双分支设计，同时提取全局粗粒度特征和局部细粒度特征。

**全局特征提取**：使用冻结的 CLIP 视觉编码器配合可学习 Adapter 提取全局特征：

$$
g _ { i } ^ { m } = \mathrm { C L I P } _ { v } \left( x _ { i } ^ { m } \right)
$$

其中 $m \in \{2d, 3d\}$ 表示模态。

**时序聚合**：对多帧特征进行时序最大池化，得到聚合表示：

$$
\tilde{g}_i^m = \maxpool_{j=1..s} (\hat{g}_{i,j}^m)
$$

**多粒度融合（MF）模块**（Figure 4）：通过双向多头交叉注意力融合全局与局部特征：

$$
\mathrm{MCA}(Q, K) = \mathrm{Concat}(\mathrm{head}_1, ..., \mathrm{head}_H)W^O
$$

**空间加权（SW）模块**：生成空间注意力图，对特征进行逐元素加权，强调判别性区域：

$$
\tilde{u}_i^m = w_i^m \odot u_i^m
$$

### 步态模态文本字典（GMTD）

GMTD 通过大语言模型（LLM）生成模态和视角感知的文本描述，作为语义锚点引导解耦。其形式化定义为：

$$
\mathrm{GMTD} = \{ t_j^m \mid m \in \{2d, 3d\}, j = 1, 2, \ldots, 8l \}
$$

其中 $l$ 为视角数量。文本嵌入由冻结的 CLIP 文本编码器提取，视觉 CLS 特征与文本原型的余弦相似度用于选择 top-$k_t$ 原型：

$$
\cos(\tilde{g*}_i^m, v_j^m) = \frac{\tilde{g*}_i^m \cdot v_j^m}{\|\tilde{g*}_i^m\|_2 \|v_j^m\|_2}
$$

### 文本引导特征解耦（TFD）模块

TFD 模块（Figure 5）是核心创新，利用文本先验重构模态特有特征，再通过残差分解获得模态共享特征。

**模态特有特征调制**：通过通道级调制因子 $\alpha$ 对模态特有特征进行缩放：

$$
\widetilde{F}_{(mod)_i^m} = \alpha \odot F_{(mod)_i^m}
$$

**残差分解得共享特征**：从原始特征中减去重构的模态特有特征，得到模态共享表示：

$$
F_{(shared)_i^m} = \tilde{u}_i^m - \widetilde{F}_{(mod)_i^m}
$$

该设计的因果机制在于：文本原型提供了模态特有的语义锚点，使模型能显式建模“什么特征属于该模态独有”，残差自然分离出跨模态不变的身份信息。

### 特征稳定性增强（FSE）模块

FSE 模块（Figure 6）对解耦后的共享特征进行后处理，通过空间卷积捕获局部感受野依赖，再通过通道门控机制建模全局通道相关性，提升特征对噪声和局部缺失的鲁棒性。

![[assets/figures/papers/paper_list_l1081_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_Text_guided_Feature/figures/006_Figure_6.jpg]]
*Figure 6: Illustration of the FSE module*

### 联合损失函数

总损失函数为五项损失的加权组合：

$$
\mathcal{L}_{all} = \gamma_1(\mathcal{L}_{tri} + \mathcal{L}_{ce}) + \gamma_2 \mathcal{L}_{align}^m + \gamma_3(\mathcal{L}_{ortho}^m + \mathcal{L}_{HSIC}^m)
$$

- **$\mathcal{L}_{tri}$（三元组损失）与 $\mathcal{L}_{ce}$（交叉熵损失）**：保证共享特征的判别性。
- **$\mathcal{L}_{align}^m$（对齐损失）**：对齐视觉 CLS 特征与选中的文本原型。
- **$\mathcal{L}_{ortho}^m$（正交损失）**：强制共享特征与模态特有特征正交，减少信息泄露。
- **$\mathcal{L}_{HSIC}^m$（HSIC 独立性损失）**：进一步约束共享与特有特征的统计独立性。

默认权重设置为 $\gamma_1 = 1.0$，$\gamma_2 = 0.5$，$\gamma_3 = 0.1$。

## 实验与关键发现

### 核心瓶颈与实验目标

跨模态步态识别的根本挑战在于LiDAR点云与RGB视频之间存在显著的模态差异——点云捕捉稀疏的三维几何结构，而RGB图像提供密集的纹理外观信息。这种差异导致现有方法难以提取共享的判别性步态特征。实验的核心目标在于验证：**通过文本先验引导特征解耦，能否将模态共享的步态线索从模态特有的噪声中分离出来，从而提升跨模态检索精度。**

### 主实验结果

#### SUSTech1K数据集跨模态识别

Table 1和Table 2分别报告了SUSTech1K数据集上2D→3D和3D→2D两个方向的跨模态步态识别结果。TCFDNet在这两个方向上均取得了新的最优结果：**2D→3D方向Rank-1准确率达到55.9%，3D→2D方向达到61.7%**。

从Table 1（2D→3D）来看，TCFDNet显著超越了所有对比方法。值得注意的是，CL-Gait（Guo et al., ECCV 2024）虽然使用了额外的合成数据进行预训练（以♠标注），但其性能仍低于TCFDNet——后者仅使用了训练集数据，无需依赖大规模合成数据的预训练。这一对比直接证明了文本先验引导的特征解耦策略在数据效率上的优势：通过语义锚点的约束，模型能够从有限的真实数据中学习到更本质的跨模态对应关系。

Table 2（3D→2D）呈现了类似的趋势。3D→2D方向的整体精度高于2D→3D方向，这暗示LiDAR点云作为查询模态时，其几何信息的稳定性可能有助于检索更具判别力的RGB特征。TCFDNet在两个方向上的一致性优势表明，TFD模块的残差分解机制对不同查询模态具有鲁棒性。

![[assets/figures/papers/paper_list_l1081_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_Text_guided_Feature/figures/008_Table_2.jpg]]
*Table 2: Rank-1 accuracy of cross-modal gait recognition from 3D LiDAR to 2D camera on the SUSTech1K dataset. ♠ denotes methods pre-trained on synthetic data*

#### FreeGait数据集跨模态识别

Table 3展示了FreeGait数据集上的结果。TCFDNet在2D→3D方向达到52.1%，3D→2D方向达到57.9%，均保持了领先地位。FreeGait数据集包含更复杂的行走场景（如携带物品、不同着装），这进一步验证了FSE模块在提升共享特征稳定性方面的作用——空间卷积与通道门控机制能够抑制场景变化引入的噪声。

### 消融实验

Table 4的消融实验系统性地验证了各模块的贡献（以LiDAR→Camera方向为基准）。

**GMTD模块的关键作用：** 移除GMTD（w/o GMTD）导致性能显著下降，这直接证实了文本先验对特征解耦的必要性。在没有模态感知文本描述的情况下，TFD模块失去了语义锚点，无法有效区分模态共享特征与模态特有特征。这一发现与核心洞察一致：文本描述作为中间语义空间，能够为视觉特征的分解提供稳定的参照系。

**MF与FSE模块的必要性：** 分别移除多粒度融合模块（w/o MF）和特征稳定性增强模块（w/o FSE）均导致精度降低。MF模块的消融表明，全局粗粒度特征与局部细粒度特征的双向交叉注意力融合对于捕捉完整的步态模式至关重要；FSE模块的消融则证实，即使在解耦之后，共享特征仍需通过空间依赖性和通道相关性建模来增强鲁棒性。

**跨模态Patch交换策略：** Table 4中PE（Patch Exchange）相关的消融显示，训练时的跨模态区域混合策略能够进一步提升泛化能力。这一策略通过在训练过程中人为制造模态边界的模糊化，迫使模型学习更本质的跨模态不变特征。

**top-kt超参数分析：** Figure 9展示了GMTD模块中top-kt参数的影响。最优值为16，过小（如4或8）会导致文本原型覆盖不足，无法充分表征模态多样化的语义；过大（如32）则可能引入噪声原型，干扰特征解耦的方向。这一非线性关系表明，文本原型的数量需要在语义覆盖度和选择精度之间取得平衡。

### 可视化分析

**t-SNE特征分布（Figure 7）：** 与基线方法相比，TCFDNet提取的2D和3D特征在共享空间中呈现出更紧凑的聚类结构和更大的类间距离。这一可视化直接印证了TFD模块的正交约束和HSIC独立性损失的有效性——模态共享特征成功地从模态特有特征中分离出来，使得同一身份的不同模态特征在嵌入空间中高度对齐。

**跨模态相似度分布（Figure 8）：** 类内与类间余弦相似度分布的对比进一步量化了特征解耦的效果。TCFDNet的类内相似度分布明显向高值偏移，而类间分布则向低值偏移，两者之间的重叠区域显著缩小。这表明解耦后的共享特征不仅具有判别力，而且在跨模态检索场景下具有更高的置信度。

### 失败模式与局限性

尽管TCFDNet取得了显著的性能提升，但在以下场景中仍存在明显局限：

1. **夜间条件退化：** 在白天-夜晚跨域场景下，性能出现明显下降。这是因为夜间RGB图像缺乏纹理信息，而LiDAR点云虽然不受光照影响，但其稀疏性与白天训练数据中的分布存在差异。这一失败模式揭示了当前文本先验尚未充分覆盖昼夜变化的语义描述。

2. **TFD模块训练初期的不稳定性：** TFD模块在训练早期需要门控机制来防止解耦过程的发散，这增加了实现的复杂性。这一现象的本质原因在于：在特征空间尚未充分结构化时，文本原型的相似度计算可能产生噪声引导，导致模态特有特征的重构方向偏离预期。

3. **LLM依赖的文本质量限制：** GMTD的构建依赖LLM生成步态描述，其质量受限于LLM对步态细节（如步幅、节奏、关节运动模式）的理解能力。当文本描述过于泛化或与视觉特征不对齐时，语义锚点的引导作用会减弱。

![[assets/figures/papers/paper_list_l1081_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_Text_guided_Feature/figures/011_Table_4.jpg]]
*Table 4: Ablation study on SUSTech1K dataset for cross-modal gait recognition (LiDAR → Camera). At each step, only one functional group is modified while others remain fully integrated*

![[assets/figures/papers/paper_list_l1081_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_Text_guided_Feature/figures/012_Figure_7.jpg]]
*Figure 7: t-SNE visualization of cross-modal 2D and 3D features. Zooming in for details*

![[assets/figures/papers/paper_list_l1081_https_openaccess_thecvf_com_content_CVPR2026_html_Lu_Text_guided_Feature/figures/013_Figure_8.jpg]]
*Figure 8: Visualization of cross-modal intra/inter-class cosine similarity distribution*

## 定位与知识库关联

### 跨模态步态识别的技术脉络

跨模态步态识别旨在建立LiDAR点云与RGB视频之间的身份检索桥梁，其核心挑战在于两模态间显著的几何-纹理差异。现有方法可大致归为三类技术路线：

**基于合成数据预训练的路线**以 **CL-Gait**（Guo et al., ECCV 2024）为代表，通过大规模合成数据（♠标注）进行预训练来弥合模态鸿沟。该方法虽在SUSTech1K上取得了竞争力结果，但其性能高度依赖额外合成数据的数量与质量，实际部署成本较高。

**基于共享原型的路线**以 **CrossGait**（Wang et al., IJCB 2024）为代表，通过构建模态共享的原型空间实现跨模态对齐。该类方法假设两模态特征可被映射到同一原型周围，但未显式建模模态特有噪声的分离，导致共享空间中仍残留模态特异性干扰。

**经典单模态步态识别方法**如 **GaitSet**（Chao et al., AAAI 2019）、**GaitPart**（Fan et al., CVPR 2020）以及综合性框架 **OpenGait**（Fan et al., CVPR 2023），虽在单模态场景下性能优异，但直接迁移至跨模态任务时，因缺乏模态对齐机制而表现受限。

### TCFDNet的方法定位与关键差异

TCFDNet在上述谱系中开辟了**文本引导特征解耦**的新路径，其方法论定位体现在三个关键维度的差异化设计：

**1. 先验知识注入方式的范式转变。** 与依赖合成视觉数据或纯视觉对齐的先前方法不同，TCFDNet首次将大语言模型生成的文本描述作为语义锚点引入跨模态步态识别。通过构建步态模态文本字典（GMTD），将模态差异显式编码为可查询的语义原型，使模型能够"理解"而非仅仅"映射"模态差异。

**2. 特征解耦机制的显式化。** 先前方法的共享特征学习本质上是隐式的——对比学习或原型训练使特征在优化过程中自然趋向共享，但模态特有信息始终与共享信息纠缠。TCFDNet的TFD模块通过残差分解（$F_{(shared)_i^m} = \tilde{u}_i^m - \widetilde{F}_{(mod)_i^m}$）实现显式解耦：先利用文本原型重构模态特有特征，再从原始特征中减去该部分，配合正交约束和HSIC独立性损失确保解耦质量。这种"减法式"解耦比隐式方法更具可解释性和可控性。

**3. 解耦后处理的鲁棒性增强。** 解耦得到的共享特征虽已剥离大部分模态噪声，但仍可能存在局部不稳定。FSE模块通过空间卷积捕获局部感受野依赖，配合通道门控机制建模全局通道相关性，为共享特征提供额外的稳定性保障。这一设计在先前方法中未见对应组件。

### 适用边界与局限

**适用场景。** TCFDNet的核心机制——文本引导解耦——理论上适用于任何可被语言描述的模态差异场景。当前验证集中于LiDAR-RGB跨模态步态识别，在SUSTech1K和FreeGait数据集上均取得最优结果（Table 1-3），证明其在受控场景下的有效性。

**已知局限。** 分析中明确指出以下限制：

- **昼夜鲁棒性不足。** 在夜间条件下，由于白天-夜晚的跨域差异叠加跨模态差异，性能有所下降。这表明GMTD的文本描述可能未充分覆盖光照变化引起的表观变异。
- **训练稳定性要求。** TFD模块在训练早期需要门控机制防止发散，增加了实现复杂性和超参数敏感性。
- **LLM依赖性。** GMTD的构建依赖LLM生成文本描述，其质量受限于LLM对步态细粒度特征的描述能力。若LLM无法准确捕捉模态间的微妙差异（如LiDAR点云的稀疏性模式、RGB纹理的噪声特性），文本锚点的引导作用将打折扣。

### 开放问题与未来方向

基于上述局限，以下开放问题值得关注：

1. **跨域-跨模态联合鲁棒性。** 如何进一步减小昼夜变化引起的跨域差异与跨模态差异的耦合效应？可能需要扩展GMTD以包含光照、天气等域感知描述，或设计域自适应机制。

2. **文本先验的模态泛化能力。** 文本先验是否适用于更多生物特征模态？如红外热成像的温谱模式、事件相机的时空脉冲模式等，这些模态的"语言可描述性"尚未被验证。

3. **无LLM辅助的自动描述构建。** 能否在无LLM辅助下自动构建有效的模态描述？例如通过模态翻译网络生成伪文本，或利用对比语言-视觉预训练模型（如CLIP）的零样本能力挖掘隐含的模态语义，将降低对LLM的依赖并提升方法的自包含性。

4. **解耦质量的量化评估。** 当前通过下游任务精度间接评估解耦质量，缺乏对解耦完备性的直接度量。发展针对共享/特有特征分离度的定量指标，将有助于指导解耦机制的设计与调优。

### 证据强度说明

上述方法定位基于SUSTech1K数据集上的主实验结果（Table 1-2，Rank-1 55.9%/61.7%）和消融研究（Table 4，移除GMTD导致显著性能下降），证据可信度较高（confidence ≥ 0.9）。t-SNE可视化（Figure 7）和类内/类间相似度分布（Figure 8）进一步从特征空间结构角度支撑了文本引导解耦的有效性。关于昼夜鲁棒性不足和门控机制必要性的局限描述，来自原文明确讨论，可直接采信。开放问题部分为基于已知局限的合理推演，需后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Text_guided_Feature_Disentanglement_for_Cross_modal_Gait_Recognition.pdf]]

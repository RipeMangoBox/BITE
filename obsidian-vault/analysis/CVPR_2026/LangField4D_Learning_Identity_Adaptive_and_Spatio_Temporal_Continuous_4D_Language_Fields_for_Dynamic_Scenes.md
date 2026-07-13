---
title: "LangField4D: Learning Identity-Adaptive and Spatio-Temporal Continuous 4D Language Fields for Dynamic Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LangField4D_Learning_Identity_Adaptive_and_Spatio_Temporal_Continuous_4D_Language_Fields_for_Dynamic_Scenes.pdf
project_link: null
code_link: null
aliases:
- LangField4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过身份自适应高斯分组（IdaGG）为每个高斯动态分配对象归属，并利用连续四平面（TetraPlane）表示统一编码时空身份与语义，从而同时解决语义一致性和时间连续性。
primary_logic: 将4D语义空间因式分解为空间-语义平面和时间-语义平面，并引入身份自适应编码使高斯原语动态绑定正确实例，从而在统一连续表示中实现一致的时间不变语义和连续的时间变化语义。
claims:
- 时间敏感查询在HyperNeRF上vIoU 64.31 vs 47.04（4DLangSplat），Acc 84.79 vs 67.65，大幅优于基线。
- 时间无关查询在Neu3D上mIoU 71.62 vs 55.18（4DLangSplat），显著提升。
- 消融实验证明IdaGG持续提升语义性能，TetraPlane+IdaGG相比MLPs基线在vIoU上从51.61提升至64.31。
- HyperNeRF 上 vIoU (time-sensitive) = 64.31
---

# LangField4D: Learning Identity-Adaptive and Spatio-Temporal Continuous 4D Language Fields for Dynamic Scenes

> [!tip] 核心洞察
> 将4D语义空间因式分解为空间-语义平面和时间-语义平面，并引入身份自适应编码使高斯原语动态绑定正确实例，从而在统一连续表示中实现一致的时间不变语义和连续的时间变化语义。

| 字段 | 内容 |
|------|------|
| 中文题名 | LangField4D：学习动态场景的身份自适应和时空连续4D语言场 |
| 英文题名 | LangField4D: Learning Identity-Adaptive and Spatio-Temporal Continuous 4D Language Fields for Dynamic Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_LangField4D_Learning_Identity-Adaptive_and_Spatio-Temporal_Continuous_4D_Language_Fields_for_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LangField4D |
| Dataset | HyperNeRF, Neu3D |

> [!tip] 效果简介
> - HyperNeRF 上，vIoU (time-sensitive) 64.31 vs 47.04 (4DLangSplat) (+17.27)；Acc (time-sensitive) 84.79 vs 67.65 (4DLangSplat) (+17.14)；mIoU (time-agnostic) 83.09 vs 80.93 (4DLangSplat) (+2.16)。
> - Neu3D 上，mIoU (time-agnostic) 71.62 vs 55.18 (4DLangSplat) (+16.44)。

## 概要

动态场景的开放词汇查询面临两个核心瓶颈：**高斯身份振荡**和**动作边界偏差**。在基于变形场的4D高斯泼溅框架中，高斯原语随时间运动时会跨越对象边界，导致同一高斯在不同时刻被渲染到不同物体上，产生语义不一致；同时，现有方法采用离散状态原型插值来建模时间变化语义，难以捕捉连续的动作过渡，在动作边界附近产生明显的语义偏差。

针对上述问题，**LangField4D** 提出了一种统一的连续4D语言场框架，核心思路是将身份一致性和时空语义连续性纳入同一表示空间。方法包含两个关键设计：

- **身份自适应高斯分组（IdaGG）**：为每个高斯原语赋予可学习的身份编码，并通过HexPlane构建的时空自适应场动态预测身份偏移，使高斯在任意时刻都能正确绑定到其所属的对象实例，从根本上消除ID振荡。
- **连续时空语义学习（TetraPlane）**：将4D语义空间因式分解为空间-语义平面和时间-语义平面，以连续表示替代离散状态原型，统一编码时间不变的对象级语义和连续的时间变化语义，消除动作边界偏差。

在HyperNeRF和Neu3D两个动态场景基准上的实验表明，LangField4D在时间敏感查询和时间无关查询上均显著超越现有方法：时间敏感vIoU达到64.31（对比4DLangSplat的47.04，提升17.27个百分点），时间无关mIoU在Neu3D上达到71.62（对比4DLangSplat的55.18，提升16.44个百分点）。消融实验进一步验证了IdaGG和TetraPlane各自对语义一致性和时间连续性的关键贡献。



### 动态场景开放词汇理解的语义缺口

赋予视觉系统在动态场景中进行开放词汇理解的能力，是实现具身智能与环境交互的关键前提。与静态3D场景的语言场建模（如**LangSplat**，Qin et al., CVPR 2024）不同，动态4D场景引入了时间维度上的对象运动与状态变化，使得语义建模面临两个相互耦合的根本性挑战。

第一个挑战源于变形场引起的高斯身份振荡。在基于3D高斯泼溅（3DGS）的动态场景表示中，变形场驱动高斯原语在空间中运动。当高斯跨越对象边界时，其语义归属发生混淆，导致同一高斯在不同时刻被赋予不同对象的语义，产生语义不一致。**Gaussian Grouping**（Ye et al., ECCV 2024）等方法为高斯分配静态身份编码，但无法适应动态变形带来的归属变化。**4DLangSplat**作为最直接的4D语言场基线，同样采用静态高斯身份，因此无法解决这一ID振荡问题。

第二个挑战来自离散状态原型带来的动作边界偏差。现有方法通常将动态语义建模为离散状态原型的聚类与插值。这种离散化处理无法捕捉动作执行过程中的细粒度时间连续性，在状态转换边界附近产生显著的语义偏差。**4DLangSplat**和**Feature 3DGS**（Zhou et al., CVPR 2024）均受限于此，难以对“正在打开”与“已经打开”之间的连续过渡状态进行精确查询。

### 核心瓶颈：身份一致性与时间连续性的失耦

上述两个挑战揭示了动态场景语言场建模的核心瓶颈：**变形场导致高斯跨越对象边界，产生ID振荡与语义不一致；离散状态原型无法捕捉细粒度时间连续性，产生动作边界偏差**。这两个问题并非孤立存在——身份不一致会加剧时间语义的混乱，而时间离散化又使得身份追踪缺乏平滑约束。因此，需要一种统一的表示机制，同时解决语义一致性和时间连续性问题。

### 本文动机与核心思路

针对上述瓶颈，LangField4D提出将身份自适应分组与连续时空语义学习纳入统一的4D语言场框架。其核心调控思路（causal knob）是：**通过身份自适应高斯分组（IdaGG）为每个高斯动态分配对象归属，并利用连续四平面（TetraPlane）表示统一编码时空身份与语义**。核心洞察在于：将4D语义空间因式分解为空间-语义平面和时间-语义平面，并引入身份自适应编码使高斯原语动态绑定正确实例，从而在统一连续表示中实现一致的时间不变语义和连续的时间变化语义。

Figure 1 直观展示了现有方法的失败模式与本文方法的改进效果：变形场导致高斯跨越对象边界产生ID振荡，离散状态原型在动作边界附近产生偏差，而LangField4D通过身份自适应分组和连续语义表示，在时间无关和时间敏感两类查询上均获得更一致的语义分割结果。



## 核心方法与创新机理

LangField4D 的核心创新在于直面动态场景中 4D 语言场构建的两个根瓶颈，并通过两个互为支撑的 **changed slots** 实现突破：**身份自适应高斯分组（IdaGG）** 解决高斯 ID 振荡问题，**连续四平面（TetraPlane）语义表示** 解决动作边界偏差问题。两者协同，在统一的连续表示中同时实现时间一致的对象语义和时间平滑的状态语义。

### 根瓶颈：变形场引发的双重失效

在基于 4D 高斯的动态场景表示中，变形场驱动高斯原语在时空中运动。这一机制天然导致两类系统性失效：

1. **高斯 ID 振荡**：变形场使高斯跨越对象边界，单个高斯在不同时刻可能与不同对象实例关联。现有方法（如 4DLangSplat）为每个高斯分配固定的静态身份编码，无法适应这种动态归属变化，导致语义不一致——图 1(a) 直观展示了这一现象。
2. **动作边界偏差**：4DLangSplat 等基线采用离散状态原型聚类并通过插值获取中间状态语义，这种离散化处理无法捕捉细粒度的时间连续性，在动作边界附近产生明显的语义跳变（图 1(b)）。

### Changed Slot 1：从静态身份编码到身份自适应编码

**基线做法**：Gaussian Grouping（Ye et al., ECCV 2024）为每个高斯分配固定的 16 维身份嵌入 $\mathbf{e} \in \mathbb{R}^{16}$，该嵌入在训练后保持不变，无法响应高斯的时空位置变化。

**LangField4D 的方案**：IdaGG 引入身份自适应机制，将静态嵌入扩展为时变的自适应编码：

$$\mathbf{e}' = \mathbf{e} + \phi_{id}(f_d)$$

其中 $f_d$ 是通过 HexPlane 从高斯的时空坐标 $(x, y, z, t)$ 提取的多分辨率特征，$\phi_{id}$ 为轻量 MLP 头，负责预测身份偏移 $\Delta\mathbf{e}$。这一设计使每个高斯在每一时刻都能动态调整其对象归属，从根本上消除 ID 振荡。

**因果机制**：HexPlane 的时空因子分解使身份偏移预测能够感知高斯的全局时空上下文，而非仅依赖局部几何。通过联合 2D 交叉熵损失和 3D 局部一致性正则化（$\mathcal{L}_{2d} + \mathcal{L}_{3d}$），IdaGG 为每个高斯分配离散语义坐标 $l$，作为后续连续语义学习的锚点。

### Changed Slot 2：从离散状态原型到连续四平面语义场

**基线做法**：4DLangSplat 对语义特征进行状态原型聚类，通过离散原型间的插值获取中间时刻的语义，导致动作边界处语义不平滑。

**LangField4D 的方案**：以 IdaGG 输出的语义坐标 $l$ 为额外维度，构建连续四平面（TetraPlane）因子分解——将 4D 语义空间分解为四个多分辨率 2D 平面的哈达玛积融合：

$$f_{\mathrm{sem}}(g) = \phi_d \left( \bigcup_m \prod_c f(g)_c \right)$$

其中三个空间-语义平面（$P_{xl}, P_{yl}, P_{zl}$）编码时间不变的对象级语义，时间-语义平面（$P_{tl}$）捕捉平滑的时间变化语义。多分辨率设计使粗粒度平面负责全局语义结构，细粒度平面建模局部细节。

**因果机制**：连续四平面表示天然保证语义在时空维度上的平滑性，配合总变分正则 $\mathcal{L}_{\mathrm{TV}}$ 和时间加速度平滑正则 $\mathcal{L}_{\mathrm{smooth}}$，在优化目标层面强制语义的时间连续性，从根本上消除动作边界偏差。

### 协同效应：1+1 > 2

两个 changed slots 并非孤立创新，而是形成因果闭环：IdaGG 为每个高斯提供正确的对象归属，使时间不变语义的提取不受 ID 振荡污染；TetraPlane 在此基础上将离散语义坐标连续化，使时间变化语义的建模不受离散化限制。消融实验（Table 3）量化了这一协同效应：TetraPlane+IdaGG 在时间敏感查询的 vIoU 上达到 64.31，相比 MLPs+IdaGG 的 51.61 提升 12.70 点，相比纯 MLPs 基线的 51.61（无 IdaGG）提升更为显著。在时间无关查询上，IdaGG 的加入无论配合何种解码器均带来一致的 mIoU 增益（MLPs: 80.85 → 82.63；TetraPlane: 81.94 → 83.09），验证了身份一致性对语义提取的独立贡献。



LangField4D 构建在 4D 高斯泼溅（4D-GS）之上，以两阶段管线实现动态场景的开放词汇查询。整体流程如 Figure 2 所示，核心思路是：先解决“哪个高斯属于哪个对象”的身份一致性问题，再在统一连续空间中学习“对象是什么、正在做什么”的时空语义。

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of LangField4D. We first obtain spatio-temporally consistent masks and extract time-invariant and time-varying features for supervision. To resolve semantic ambiguity, we learn an Identity Adaptation Field that enforces coherent Gaussian–instance affiliations. Leveraging these identity-aligned features, our Continuous Spatio-temporal Semantic Learning module encodes both static and dynamic semantics within a unified continuous latent space*

**阶段一：身份自适应高斯分组（IdaGG）**
输入为多视角视频序列，首先利用 DEVA 获取时域一致的实例掩码，并通过 SAM2 跨视角匹配得到全局一致的对象 ID。在此基础上，IdaGG 构建一个基于 HexPlane 的身份自适应场，为每个高斯原语在任意时刻 $t$ 动态预测身份偏移 $\Delta\mathbf{e}$，得到自适应身份编码 $\mathbf{e}' = \mathbf{e} + \phi_{id}(f_d)$。该阶段通过结合 2D 交叉熵损失和 3D 局部一致性正则的总渲染损失 $\mathcal{L}_{\mathrm{render}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{id}}(\mathcal{L}_{2d} + \mathcal{L}_{3d})$ 进行优化，最终为每个高斯分配一个离散语义坐标 $l$，确保高斯在变形过程中始终绑定正确的对象实例。

**阶段二：连续时空语义学习（TetraPlane）**
以阶段一获得的语义坐标 $l$ 为额外维度，将 4D 语义空间因式分解为四个多分辨率 2D 平面（合称 TetraPlane）：三个空间-语义平面编码时间不变的对象级语义，一个时间-语义平面捕捉平滑的时间变化语义。高斯的最终时空语义特征通过融合四平面哈达玛积并在多分辨率上拼接后经 MLP 得到：$f_{\mathrm{sem}}(g) = \phi_d\left(\bigcup_m \prod_c f(g)_c\right)$。该阶段使用语言特征 L1 损失、总变分平滑正则和时序加速度正则共同优化：$\mathcal{L}_{\mathrm{tetra}} = \mathcal{L}_{\mathrm{lang}} + \mathcal{L}_{\mathrm{TV}} + \mathcal{L}_{\mathrm{smooth}}$。

**数据准备与监督信号**
两阶段之前，系统从视频中提取多层次语言特征作为监督：时间不变特征（如 CLIP 图像嵌入）用于对象级语义，时间变化特征（由 MLLM 生成的细粒度动作描述经 CLIP 文本编码）用于状态级语义。

**模块间的因果依赖**
IdaGG 的输出（离散语义坐标 $l$）直接作为 TetraPlane 的输入维度，形成强依赖关系：若身份分组错误，后续语义学习将在错误的对象上下文中进行，导致时间不变语义混乱；若跳过 TetraPlane 而使用简单 MLP 解码（消融实验中的 MLPs+IdaGG 配置），则时间敏感 vIoU 从 64.31 骤降至 51.61（Table 3），证明连续表示对捕捉动作边界的必要性。



### 3.1 问题形式化与渲染基础

LangField4D 基于 4D Gaussian Splatting（4D-GS）构建动态场景的语言场。给定一组 4D 高斯原语 $\mathcal{G} = \{g_i\}$，每个高斯携带几何属性（位置 $\boldsymbol{\mu}$、协方差 $\boldsymbol{\Sigma}$、不透明度 $\alpha$）和外观属性（颜色 $\mathbf{c}$），以及附加的语义特征向量 $\mathbf{f}$。像素 $\mathbf{p}$ 的颜色和特征分别通过 alpha 混合渲染：

$$
\mathbf{C}(\mathbf{p}) = \sum_{i=1}^{|\mathcal{G}_{\mathbf{p}}|} \mathbf{c}_{g_i} \alpha_{g_i}^{\mathbf{p}} \prod_{j=1}^{i-1}(1-\alpha_{g_j}^{\mathbf{p}})
$$

$$
\mathbf{F}(\mathbf{p}) = \sum_{i=1}^{|\mathcal{G}_{\mathbf{p}}|} \mathbf{f}_{g_i} \alpha_{g_i}^{\mathbf{p}} \prod_{j=1}^{i-1}(1-\alpha_{g_j}^{\mathbf{p}})
$$

其中 $\mathcal{G}_{\mathbf{p}}$ 为沿射线排序的高斯集合，$\alpha_{g_i}^{\mathbf{p}}$ 为高斯 $g_i$ 在像素 $\mathbf{p}$ 处的有效不透明度。该框架通过两阶段管线实现开放词汇查询：身份自适应高斯分组（IdaGG）和基于 TetraPlane 的连续时空语义学习。

### 3.2 数据准备：时空一致实例标注

在训练前，方法利用 DEVA 获取时域一致的实例分割掩码，并通过 SAM2 实现跨视角匹配，为每个对象分配全局一致的实例 ID。同时，从多帧图像中提取多层次语言特征（如 CLIP 嵌入），区分时间不变语义（对象类别）和时间变化语义（动作状态），作为后续阶段的监督信号。

### 3.3 身份自适应高斯分组（IdaGG）

**核心问题**：在动态场景中，变形场使高斯原语跨越对象边界，导致同一高斯在不同时刻可能对应不同实例（ID 振荡），破坏语义一致性。

**解决机制**：IdaGG 基于 HexPlane 构建身份自适应场，为每个高斯动态预测身份偏移。具体地，每个高斯携带一个可学习的静态身份嵌入 $\mathbf{e} \in \mathbb{R}^{16}$，在时刻 $t$ 的自适应身份编码为：

$$
\mathbf{e}' = \mathbf{e} + \phi_{id}(\mathbf{f}_d)
$$

其中 $\mathbf{f}_d$ 为 HexPlane 从高斯的时空坐标 $(\boldsymbol{\mu}, t)$ 提取的多分辨率特征，$\phi_{id}$ 为轻量 MLP 头，输出身份偏移 $\Delta\mathbf{e}$。该偏移使高斯能够根据当前空间位置和时间动态调整对象归属，而非固定绑定。

**训练目标**：IdaGG 阶段的总损失结合了 4D-GS 的图像重建损失和身份一致性损失：

$$
\mathcal{L}_{\mathrm{render}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{id}}(\mathcal{L}_{2d} + \mathcal{L}_{3d})
$$

其中 $\mathcal{L}_{2d}$ 为 2D 交叉熵损失，约束渲染的身份特征图与 DEVA 提供的实例掩码一致；$\mathcal{L}_{3d}$ 为局部一致性正则化，鼓励空间邻近的高斯具有相似的身份编码。训练收敛后，每个高斯被分配一个离散语义坐标 $\mathbf{l}$，作为后续 TetraPlane 学习的索引。

### 3.4 连续时空语义学习（TetraPlane）

**核心问题**：现有方法（如 4DLangSplat）采用离散状态原型聚类并插值，无法捕捉细粒度的时间连续性，在动作边界产生偏差。

**解决机制**：将 4D 语义空间因式分解为四个多分辨率 2D 平面（TetraPlane）——三个空间-语义平面 $P_{xl}, P_{yl}, P_{zl}$ 和一个时间-语义平面 $P_{tl}$。空间-语义平面编码时间不变的对象级语义，时间-语义平面捕捉平滑的时间变化语义。对于高斯 $g$，其多尺度时空语义特征通过哈达玛积融合后拼接，经 MLP $\phi_d$ 解码：

$$
f_{\mathrm{sem}}(g) = \phi_d \left( \bigcup_m \prod_c f(g)_c \right)
$$

其中 $m$ 遍历多个分辨率尺度，$c \in \{xl, yl, zl, tl\}$ 遍历四个平面，$f(g)_c$ 为从平面 $P_c$ 中根据高斯坐标和语义坐标 $\mathbf{l}$ 查询的特征向量。

**训练目标**：TetraPlane 阶段的总损失为：

$$
\mathcal{L}_{\mathrm{tetra}} = \mathcal{L}_{\mathrm{lang}} + \mathcal{L}_{\mathrm{TV}} + \mathcal{L}_{\mathrm{smooth}}
$$

其中 $\mathcal{L}_{\mathrm{lang}}$ 为渲染语言特征与 CLIP 监督之间的 L1 损失，$\mathcal{L}_{\mathrm{TV}}$ 为各平面的总变分平滑正则，$\mathcal{L}_{\mathrm{smooth}}$ 为时序加速度正则，鼓励相邻帧的语义特征变化平滑。该连续表示统一编码了静态对象语义和动态状态语义，使开放词汇查询能够同时处理时间无关和时间敏感的语义需求。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/001_Figure_1.jpg]]
*Figure 1: (a) Gaussian ID oscillation induced by the deformation field. (b) Action boundary bias from state-prototype interpolation. (c) Comparison of time-agnostic and time-sensitive segmentation results on the split-cookie scene. Existing methods fail to handle Gaussian ID oscillation, causing the semantic inconsistency, and tend to exhibit bias near action boundaries*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of ablation results of IdaGG. We visualize the rendering results of the learned identity features following [61]*



## 实验与关键发现

### 主实验结果

LangField4D在HyperNeRF和Neu3D两个动态场景数据集上，从时间敏感查询和时间无关查询两个维度进行了全面评估。实验结果表明，该方法在两个维度上均显著超越现有方法。

**时间敏感查询**旨在评估模型对动作状态变化的细粒度理解能力。在HyperNeRF数据集上（Table 1），LangField4D取得了vIoU 64.31和Acc 84.79的成绩，相比最直接的基线**4DLangSplat**（vIoU 47.04，Acc 67.65），vIoU提升了**+17.27**个百分点，Acc提升了**+17.14**个百分点。这一大幅提升的核心驱动力来自两个关键设计：身份自适应高斯分组（IdaGG）解决了变形场导致的高斯跨越对象边界问题，使语义特征始终绑定正确实例；连续TetraPlane表示则消除了离散状态原型插值带来的动作边界偏差，能够捕捉平滑的时间变化语义。Figure 3的定性可视化进一步印证了这一结论：本文方法在余弦相似度曲线上呈现更清晰的时序边界，而4DLangSplat的相似度分布则较为模糊，难以精确定位动作片段。

**时间无关查询**评估模型对对象固有语义的理解能力，即不依赖时间状态的对象级语义分割。在HyperNeRF上（Table 2），LangField4D取得mIoU 83.09，较4DLangSplat的80.93提升**+2.16**；在更具挑战性的Neu3D数据集上，mIoU从55.18提升至71.62，提升幅度达**+16.44**。Neu3D上的大幅提升说明，当场景动态性增强、高斯运动更剧烈时，IdaGG提供的身份一致性对语义提取的增益更为显著。Figure 4和Figure 5的定性结果显示，4DLangSplat由于变形高斯运动导致特征不精确，对象边界模糊，而LangField4D能够精确捕捉对象边界，构建更清晰的语言场。

### 消融实验

为验证各模块的独立贡献，在HyperNeRF数据集上进行了系统消融（Table 3），考察四个配置：纯MLPs基线、MLPs+IdaGG、纯TetraPlane、TetraPlane+IdaGG（完整方法）。

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/009_Table_3.jpg]]
*Table 3: Ablation Study of the TetraPlane and the IdaGG on the HyperNeRF dataset*

**TetraPlane连续表示的有效性**：在配合IdaGG的条件下，将MLPs替换为TetraPlane使时间敏感vIoU从51.61跃升至64.31（+12.70），同时Acc从75.78提升至84.79（+9.01）。这一显著差距证明，简单的MLPs解码器无法有效建模时间变化语义的连续性，而TetraPlane通过空间-语义平面和时间-语义平面的因子分解，将时间不变语义与时间变化语义在统一连续空间中解耦编码，是实现细粒度时间敏感理解的关键。

**IdaGG身份一致性的增益**：无论配合MLPs还是TetraPlane，引入IdaGG均能改善时间无关mIoU。MLPs基线加入IdaGG后，mIoU从80.85提升至82.63（+1.78）；TetraPlane基线加入IdaGG后，mIoU从81.94提升至83.09（+1.15）。同时，时间敏感指标也持续受益。Figure 6的身份特征渲染可视化直观展示了IdaGG的效果：未使用IdaGG时，高斯身份特征在对象边界处出现混叠和振荡；引入IdaGG后，身份特征清晰地对齐到各对象实例，验证了身份自适应编码对解决高斯ID振荡问题的有效性。

### 失败模式与局限性

尽管LangField4D在两个任务上均取得了最优性能，论文也明确指出了方法的局限性：

1. **上游分割依赖**：LangField4D的训练监督依赖于DEVA提供的时域一致实例掩码和SAM2的跨视角匹配。当DEVA在遮挡严重、运动模糊或细粒度部件分割等场景下产生ID漂移或不一致时，会直接损害IdaGG的身份学习质量，进而影响语义场的准确性。该依赖链的鲁棒性在极端动态场景下需要进一步验证。

2. **MLLM描述质量的敏感性**：时间敏感语义的监督信号来源于MLLM对对象动作状态的文本描述。当MLLM对细粒度动作状态的描述不够精确或存在歧义时，TetraPlane学习到的连续时间变化语义可能偏离真实语义分布，导致时间敏感查询精度下降。

3. **语义层次的扩展性**：当前TetraPlane的因子分解将语义空间分解为空间-语义和时间-语义平面，主要建模对象级语义。对于更复杂的语义层次（如部件语义、属性语义、关系语义），这种分解方式是否足够表达，仍有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons of time-sensitive querying on HyperNeRF (Numbers in %). Higher is better*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons of time-agnostic querying on the HyperNeRF and Neu3D datasets. Results are reported as mean IoU (%)*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of time-sensitive querying results between 4DLangSplat (4DLS) and ours. The bottom row depicts the cosine similarity across frames, rescaled to (0,1), while the horizontal bars indicate frames identified as relevant time segments*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_LangField4D_Learnin/figures/006_Figure_4.jpg]]
*Figure 4: Visualization of learned time-agnostic features of the previous SOTA method 4DLangSplat, and ours. While 4DLangSplat produces imprecise features due to the motion of deformable Gaussians, ours accurately captures object boundaries and constructs a precise language field*



## 定位与知识库关联

### 核心瓶颈与因果机制

动态场景的开放词汇理解面临两个相互交织的瓶颈。其一，**高斯身份振荡**：4D高斯泼溅中，变形场驱动高斯原语跨对象边界运动，导致同一高斯在不同时刻归属不同实例，破坏了语义追踪的一致性。其二，**动作边界偏差**：现有方法（如**4DLangSplat**）将连续动作离散化为有限状态原型，通过状态间插值建模时间变化语义，这种离散近似在动作过渡阶段产生明显的语义模糊和边界偏差。LangField4D的因果调节变量是**身份自适应分组**（IdaGG）与**连续四平面表示**（TetraPlane）的协同：前者为每个高斯动态分配正确的对象归属，消除ID振荡；后者将4D语义空间连续化，消除离散状态插值带来的边界偏差。两者共同实现了时间不变语义的一致性和时间变化语义的平滑连续性。

### 方法谱系与基线关系

LangField4D处于**4D高斯泼溅 + 开放词汇语言场**的交叉节点，其直接前驱包括：

- **4DLangSplat**：最直接基线，同样基于4D-GS构建语言场，但采用静态高斯身份编码和离散状态原型，是本文要解决的两个核心问题的集中体现。在HyperNeRF时间敏感查询上，LangField4D的vIoU从47.04提升至64.31（+17.27），Acc从67.65提升至84.79（+17.14），验证了IdaGG和TetraPlane对这两个瓶颈的有效突破。
- **LangSplat**（Qin et al., CVPR 2024）：静态3D语言场方法，为时间无关语义建模提供参考范式，但无法处理动态场景。
- **Gaussian Grouping**（Ye et al., ECCV 2024）：为3D高斯赋予静态身份编码，启发了IdaGG的设计，但缺乏时间维度的自适应能力。IdaGG在此基础上引入HexPlane驱动的自适应偏移$\mathbf{e}' = \mathbf{e} + \phi_{id}(f_d)$，使身份编码随空间和时间动态调整。
- **Feature 3DGS**（Zhou et al., CVPR 2024）与**3D-OVS**（Liu et al., CVPR 2023）：分别代表基于3DGS和NeRF的特征提升与开放词汇分割方法，在时间无关语义分割实验中作为比较对象。

在知识库中的定位上，LangField4D的贡献可拆解为两个可迁移的模块化设计：IdaGG解决的是**可变形基元表示中的实例归属动态绑定**问题，这一思路可泛化至任何需要追踪可变形元素身份的表示框架；TetraPlane解决的是**高维语义空间的连续因子分解**问题，其空间-语义平面和时间-语义平面的分离设计，为其他需要联合建模静态属性与动态变化的任务（如4D场景编辑、动态对象属性查询）提供了可参考的表示范式。

### 适用边界与局限

LangField4D的有效性建立在对上游模块质量的前提假设之上：

1. **对DEVA实例分割的依赖**：IdaGG的训练监督依赖DEVA提供的时域一致实例掩码和全局一致ID。当DEVA在遮挡严重、运动模糊或细粒度对象边界场景下产生ID漂移或分割错误时，身份自适应场的学习将受到污染，进而影响语义一致性的上限。论文明确指出这一局限，但未量化DEVA质量下降对最终性能的衰减曲线。
2. **MLLM描述精度的敏感性**：时间敏感语义的监督信号来自多模态大语言模型对对象动作状态的文本描述。当MLLM对细粒度动作状态（如“半开的门” vs “正在打开的门”）的描述不够精确时，TetraPlane中时间-语义平面的学习将缺乏足够的判别性监督，导致时间敏感查询精度受限。

### 开放问题

1. **上游鲁棒性**：在DEVA分割失败或ID漂移的极端场景下，IdaGG的自适应机制能否通过自身的一致性先验部分纠正上游错误？是否需要引入闭环的自监督一致性约束来降低对外部标注的依赖？
2. **MLLM监督质量**：MLLM描述的质量如何定量影响时间敏感语义的精度？是否存在一个描述粒度的“临界点”，低于该粒度时TetraPlane的连续表示优势不再明显？
3. **语义层次扩展**：TetraPlane当前将语义空间分解为空间-语义和时间-语义两个维度。这种因子分解方式是否可以扩展到更丰富的语义层次，如对象部件（“车轮”、“门把手”）或属性（“红色的”、“金属的”）？若能引入层次化语义平面，可能支持更细粒度的组合式查询。
4. **自监督信号**：能否利用动态场景中天然存在的运动一致性、外观恒常性等自监督信号，减少对人工标注或MLLM描述的依赖？例如，利用光流或轨迹一致性约束身份编码的时序平滑性。
5. **跨场景泛化**：IdaGG学习到的身份自适应机制是否具有跨场景的泛化能力？即在一个场景上训练的身份自适应场能否为零样本或小样本的新场景提供有效的身份先验？



## 原文 PDF

![[paperPDFs/CVPR_2026/LangField4D_Learning_Identity_Adaptive_and_Spatio_Temporal_Continuous_4D_Language_Fields_for_Dynamic_Scenes.pdf]]

---
title: "Can We Build Scene Graphs, Not Classify Them? FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Can_We_Build_Scene_Graphs_Not_Classify_Them_FlowSG_Progressive_Image_Conditioned_Scene_Graph_Generation_with_Flow_Matching.pdf
project_link: null
code_link: null
aliases:
- Can_We_Build_Sce
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将场景图生成重新定义为在混合离散-连续空间上的渐进生成过程，通过流匹配联合去噪边框几何和语义标记，实现逐步精炼和全局约束。
primary_logic: 场景图生成应视为从噪声图到目标图的连续时间传输问题：使用连续流匹配处理边框坐标，离散流匹配处理类别和谓词标记，并通过图Transformer中的关系调制注意力和流条件消息聚合耦合语义与几何，实现几步推理即可生成高质量场景图。
claims:
- 传统SGG方法分为两阶段或一阶段，但均是在单次前向传递中做出确定性决策，缺乏迭代式生成和全局一致性约束。
- FlowSG通过混合离散-连续流匹配，同时演化边框几何（CFM）和语义标记（DFM），实现语义与几何的耦合生成。
- 流条件消息聚合（FMA）模块通过关系调制注意力和度感知的邻居聚合，显著提升性能；消融实验表明移除FMA导致指标明显下降。
- 在PSG和VG数据集上的开放/封闭词汇场景下，FlowSG均取得领先结果，在PSG SGDet上R@50/100达到46.3/53.3，mR@50/100达到42.7/48.3，约比USG-Par提升3个点。
---

# Can We Build Scene Graphs, Not Classify Them? FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching

> [!tip] 核心洞察
> 场景图生成应视为从噪声图到目标图的连续时间传输问题：使用连续流匹配处理边框坐标，离散流匹配处理类别和谓词标记，并通过图Transformer中的关系调制注意力和流条件消息聚合耦合语义与几何，实现几步推理即可生成高质量场景图。

| 字段 | 内容 |
|------|------|
| 中文题名 | 能否构建场景图而非分类？FlowSG：基于流匹配的渐进式图像条件场景图生成 |
| 英文题名 | Can We Build Scene Graphs, Not Classify Them? FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.18623) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlowSG |
| Dataset | PSG SGDet, VG SGDet, VG PredCls |

> [!tip] 效果简介
> - PSG SGDet 上，R@50 46.3 vs ~43.3 (USG-Par, estimated best prior) (+~3.0)；mR@50 42.7 vs ~39.7 (USG-Par, estimated) (+~3.0)。
> - VG SGDet (closed-set) 上，R@50 36.5 vs ~33.5 (best prior one-stage) (+~3.0)。
> - VG PredCls (closed-set) 上，R@50 65.7 vs ~62.7 (USG-Par, estimated) (+~3.0)。

## 概要

场景图生成（Scene Graph Generation, SGG）旨在将图像解析为结构化的<主体-谓词-客体>三元组，是视觉理解与下游推理的关键中间表示。然而，现有SGG范式——无论是**两阶段**方法（如 **Neural Motifs** (Zellers et al., CVPR 2018)）还是**单阶段**方法（如 **GPS-Net** (Lin et al., CVPR 2020)）——本质上都是**确定性的一次分类任务**：模型在单次前向传递中对物体和关系做出硬性决策，缺乏迭代式修正与全局结构约束，难以保证语义与几何的一致性。

本文提出 **FlowSG**，将场景图生成重新定义为**混合离散-连续空间上的渐进生成问题**。其核心洞见是：场景图生成应被视为从噪声图到目标图的连续时间传输过程——利用**连续流匹配**（Continuous Flow Matching, CFM）处理边框坐标的逐步去噪，利用**离散流匹配**（Discrete Flow Matching, DFM）处理类别与谓词标记的逐步精炼，并通过图Transformer中的**关系调制注意力**与**流条件消息聚合**（Flow-conditioned Message Aggregation, FMA）耦合语义与几何，实现几步推理即可生成高质量场景图。

在方法定位上，FlowSG区别于传统分类范式，属于**图像条件的迭代生成式方法**：它从冻结检测器的物体提议出发，通过VQ-VAE将视觉特征离散化为视觉-语言对齐的码本标记，随后在图Transformer中同时演化连续边框与离散语义，最终输出全局一致的场景图。

实验结果表明，FlowSG在PSG和VG数据集的开放/封闭词汇设定下均取得领先性能：在PSG SGDet任务上，R@50/mR@50分别达到46.3/42.7，较此前最佳方法 **USG-Par** (Wu et al., CVPR 2025) 提升约3个点；在VG SGDet上同样获得约3个点的提升。消融实验证实，FMA模块和全局图像交叉注意力是性能的关键支撑，移除FMA导致R@50从46.3骤降至40.5。



### 场景图生成：从分类到构建的范式反思

场景图生成（Scene Graph Generation, SGG）旨在将图像解析为结构化的图表示，其中节点对应对象实例（携带类别标签与边框坐标），边则编码对象间的语义关系（谓词）。这一结构化的中间表示在视觉问答、图像描述、具身导航等下游任务中扮演着关键角色。

然而，现有SGG方法在范式层面存在一个根本性的瓶颈：**无论两阶段还是单阶段方法，本质上都是确定性的一次性分类任务**。两阶段范式（以 **Neural Motifs**（Zellers et al., CVPR 2018）为代表）先通过预训练检测器提取对象提议，再枚举对象对并利用多流特征对谓词进行分类；单阶段范式（如 **GPS-Net**（Lin et al., CVPR 2020））则在单次前向传递中联合检测对象与谓词，再通过匹配步骤将谓词附加到对象对上。这两种范式共享一个深层假设——场景图可以在一次前向传递中被“分类”出来，缺乏迭代式修正和全局结构约束。

### 核心缺口：缺乏渐进式构建与全局一致性

上述“一次性分类”范式带来了两个紧密关联的缺陷：

1. **缺乏迭代精炼能力**：模型在单次推理中做出确定性决策，无法像人类理解场景那样逐步修正错误、消解歧义。当初始预测出现偏差时，系统没有机制回溯并调整已做出的关系判断。

2. **全局结构约束缺失**：现有方法通常独立地预测每条边（谓词），忽略了场景图作为一个整体应满足的语义与几何一致性约束。例如，对象间的空间布局、关系的传递性、以及图拓扑的统计规律，在分类范式中难以被显式建模和利用。

这些缺陷在高复杂度的开放词汇场景和长尾关系分布下尤为突出，导致现有方法在谓词召回率（尤其是平均召回率mR）和图级指标上长期停滞。

### 本文动机：将场景图生成重新定义为渐进生成问题

针对上述瓶颈，FlowSG 提出了一个范式层面的转变：**将场景图生成重新定义为在混合离散-连续空间上的渐进生成过程**。核心洞见在于：场景图生成不应是一次性的分类决策，而应被视为从噪声图到目标图的连续时间传输问题。

具体而言，FlowSG 从三个层面回应了现有范式的不足：

- **渐进式构建**：从随机初始化的噪声图出发，通过流匹配（Flow Matching）驱动的迭代去噪过程，逐步精炼边框几何和语义标记，使得模型可以在多步推理中修正早期错误。
- **语义与几何耦合**：通过连续流匹配（CFM）处理边框坐标的连续演化，离散流匹配（DFM）处理类别和谓词标记的离散跳转，并在图Transformer中通过关系调制注意力和流条件消息聚合（FMA）将两者深度融合，实现语义与几何的协同生成。
- **全局约束注入**：图Transformer的图感知架构天然支持跨节点和跨边的信息交互，使得每一步的精炼都能感知全局图结构，从而产出语义与几何一致的高质量场景图。

这一范式转变的核心问题可以凝练为：**“能否构建场景图，而非分类场景图？”**——这也正是本文标题所提出的根本追问。Figure 1 直观对比了三种范式的差异：两阶段和单阶段方法均是一次性决策，而FlowSG则从一个初始噪声图开始，通过图像条件的迭代去噪逐步生长出结构一致的场景图。



## 核心方法与创新机理

FlowSG 的核心创新在于将场景图生成（SGG）从传统的**一次性确定性分类**重构为**渐进式图像条件生成**问题，并通过**混合离散-连续流匹配**框架实现语义与几何的联合演化。以下从范式转变、训练目标、关系预测机制和视觉特征表示四个维度展开分析。

### 1. 生成范式转变：从一次分类到渐进式生成

现有 SGG 方法——无论是经典的两阶段方法（如 **Neural Motifs**，Zellers et al., CVPR 2018）还是单阶段方法（如 **GPS-Net**，Lin et al., CVPR 2020）——均在单次前向传递中做出确定性决策，缺乏迭代式修正能力和全局结构约束（见 Figure 1）。这种“一次分类”范式的一个关键瓶颈在于：当初始检测或关系预测出错时，系统没有机制进行回溯修正，导致语义与几何的一致性难以保证。

FlowSG 将场景图生成重新定义为**从噪声图到目标图的连续时间传输问题**（Section 1, Figure 1）。具体而言，模型从一个初始化的噪声图 $G_0$ 出发，在图像条件的引导下，通过常微分方程（ODE）积分步骤 $G_t \rightarrow G_{t+\Delta t}$ 逐步精炼，最终生成具有全局一致性的场景图。这一范式转变使得模型能够在生成过程中动态调整节点几何和边语义，而非在单次推断中锁定所有决策。

### 2. 训练目标：混合离散-连续流匹配损失

传统 SGG 方法普遍采用标准交叉熵分类损失进行训练，将关系预测视为独立的多类分类问题。FlowSG 则采用组合损失函数：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CFM}} + \lambda \mathcal{L}_{\mathrm{DFM}}$$

其中：
- **连续流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$** 用于边框几何的渐进式去噪，训练神经向量场 $\nu_\theta$ 以匹配目标速度场 $u^\star(x_t, t | x_0, x_1)$：
  $$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{(x_0, x_1) \sim \pi} \big\| \nu_\theta(x_t, t, c) - u^\star(x_t, t | x_0, x_1) \big\|_2^2$$

- **离散流匹配损失 $\mathcal{L}_{\mathrm{DFM}}$** 用于语义标记（对象类别、外观码、关系谓词）的逐步去掩码，采用时间条件交叉熵形式（Section 4.3, Eq. 18-19）。

这种混合损失设计使得边框坐标和语义标记能够在统一的流匹配框架下**耦合演化**，而非像传统方法那样分别处理视觉特征和分类logits。

### 3. 关系预测机制：从静态分类到头到动态图Transformer

传统 SGG 方法的关系预测依赖于静态视觉特征和成对特征的分类头，缺乏对图结构的显式建模。FlowSG 引入了两个关键机制实现动态关系推理：

- **关系调制自注意力（ReSA）**：通过 FiLM 门控将边嵌入 $\mathbf{e}_{ij}^{(\ell)}$ 注入节点间的注意力计算（Section 4.3, Eq. 16-17）：
  $$\alpha_{ij}(t) = \mathrm{softmax}_j \left( \frac{\mathbf{q}_i^\top \mathbf{k}_j}{\sqrt{d}} + \mathrm{FiLM}(\mathbf{e}_{ij}^{(\ell)}) \right)$$
  这使得节点间的信息传递能够感知当前预测的关系语义，而非仅依赖视觉相似性。

- **流条件消息聚合（FMA）**：计算邻域矩（度、方差、偏度等）并通过学习到的度感知缩放器进行正则化，生成时间条件上下文向量 $\zeta_i(t)^\ell$（Section 4.3）。消融实验（Table 4）证实，移除 FMA 模块导致 PSG SGDet R@50 从 46.3 骤降至 40.5（-5.8），验证了该模块在平衡高/低度节点消息传递中的关键作用。

### 4. 视觉特征表示：从连续RoI特征到离散视觉-语言码本

传统方法直接使用检测器输出的连续 RoI 特征进行关系分类。FlowSG 通过 **VQ-VAE** 将对象视觉特征和关系短语量化为离散码本标记（Section 4.1），使其能够与离散流匹配框架无缝集成。这一设计将连续视觉特征对齐到视觉-语言共享的离散空间中，使得语义标记的生成过程更加可控。消融实验（Table 5）表明，将码本大小从 $32 \times 256$ 增大到 $64 \times 256$ 带来两位数性能提升（R@50 从 32.7 升至 43.3），证实了离散化表示对生成质量的重要性。

### 创新总结

FlowSG 的四个 changed slots 构成了一个完整的渐进生成闭环：**离散码本**将视觉特征转化为可预测的标记，**混合流匹配损失**驱动语义与几何的联合去噪，**图Transformer中的ReSA和FMA**在每一步迭代中动态更新关系后验，最终实现从噪声图到语义-几何一致性场景图的逐步构建。这一范式超越了传统 SGG 的“分类”思维，将场景图生成重新定位为**约束感知的迭代生成过程**。



FlowSG 将场景图生成重新定义为从噪声图到目标图的**连续时间传输问题**，核心 pipeline 由三个紧密耦合的模块构成：场景图标记化（VQ‑VAE）、混合流匹配（Hybrid Flow Matching）和图 Transformer 去噪器（Graph Transformer Denoiser）。整体流程如图 2 所示。

**输入与初始化。** 给定输入图像 $I$，冻结的检测器 $\Phi_{\det}$ 输出 $N$ 个区域提议，包含 RoI 特征 $\mathbf{f}_i$、类别 logits $\mathbf{s}_i$ 和边框 $\mathbf{b}_i$。这些提议构成初始场景图的节点骨架。值得注意的是，对象类别在此阶段**不被掩码**，而是作为先验信息引导后续关系与外观的生成，从而简化训练并增强稳定性；关系类型与外观编码则被完全掩码，边框从标准高斯噪声初始化。

**场景图标记化（VQ‑VAE）。** 为了将连续的视觉特征纳入离散流匹配框架，FlowSG 首先利用 VQ‑VAE 将对象视觉特征和关系短语量化为离散码本标记。具体而言，每个对象的 RoI 特征 $\mathbf{f}_i$ 被映射到视觉‑语言对齐的码本索引 $a_i$，每条谓词短语 $r_{ij}^{\star}$ 被映射到关系码本索引 $p_{ij}$。这一步将异构的场景图元素统一为可预测的离散标记序列，为后续混合流匹配奠定基础。

**混合流匹配（Hybrid Flow Matching）。** 这是 FlowSG 的核心生成引擎，同时演化两类状态：连续边框坐标通过**连续流匹配（CFM）** 去噪，离散语义标记（对象外观、关系谓词）通过**离散流匹配（DFM）** 去噪。两者的演化在统一的图空间中耦合进行——节点坐标 $x_t^{(n)}$ 遵循 CFM 的 ODE 动力学，节点类别 $p_t^{(n)}$ 和边类别 $p_t^{(ij)}$ 遵循 DFM 的速率矩阵演化。训练时，CFM 损失 $\mathcal{L}_{\mathrm{CFM}}$ 最小化预测速度场与目标速度的 L2 距离，DFM 损失 $\mathcal{L}_{\mathrm{DFM}}$ 最小化预测干净后验与真实标记的交叉熵；推理时通过 ODE 积分从噪声/掩码初始状态逐步精炼到目标场景图 $G_1$。

**图 Transformer 去噪器。** 混合流的参数化由一个图感知的 DiT 风格 Transformer 完成，该 Transformer 包含三个关键设计：

1. **关系调制自注意力（ReSA）**：在标准自注意力中注入基于 FiLM 的边条件偏置 $\mathrm{FiLM}(\mathbf{e}_{ij}^{(\ell)})$，使注意力权重直接感知谓词语义。
2. **流条件消息聚合（FMA）**：计算邻域矩（度、方差、偏度等），并通过可学习的度感知缩放器正则化不同度节点的消息传递。FMA 的上下文向量 $\zeta_i(t)^\ell$ 融合了时间嵌入 $\phi(t)$、对数度 $\log(1+\deg(i,t)^\ell)$ 和局部关系信息 $\bar{\mathbf{r}}_i^\ell(t)$，使消息聚合动态适应去噪阶段。
3. **全局图像条件集成**：通过交叉注意力将冻结的 CLIP 图像特征注入图表示，提供全局视觉上下文约束。

**输出与损失。** 最终目标场景图 $G_1$ 包含对象类别、外观编码、边框坐标和谓词关系。整体训练目标为组合损失 $\mathcal{L} = \mathcal{L}_{\mathrm{CFM}} + \lambda \mathcal{L}_{\mathrm{DFM}}$，其中 $\mathcal{L}_{\mathrm{DFM}}$ 对对象外观和关系谓词的离散索引分别计算时间条件交叉熵。消融实验证实，移除 FMA 模块导致 PSG SGDet R@50 从 46.3 骤降至 40.5（‑5.8），丢弃全局图像交叉注意力则导致最大降幅（R@50 降至 39.2），验证了各模块在耦合语义与几何生成中的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our FlowSG. (Left) Image-guided iterative scene graph generation via flow matching. Starting from a noised graph*



### 4.1 场景图标记化（VQ-VAE）

FlowSG 首先将冻结检测器的连续输出转化为离散标记，以适配离散流匹配框架。

给定输入图像 $I$，冻结检测器 $\Phi_{\det}$ 输出 $N$ 个区域提议：

$$
\left\{ ( \mathbf{f}_i, \mathbf{s}_i, \mathbf{b}_i ) \right\}_{i=1}^N = \Phi_{\det}(I; \theta_{\det}), \quad \mathbf{f}_i \in \mathbb{R}^d, \quad \mathbf{s}_i \in \mathbb{R}^{C_{obj}}
$$

其中 $\mathbf{f}_i$ 为 RoI 视觉特征，$\mathbf{s}_i$ 为对象类别 logits，$\mathbf{b}_i$ 为边界框坐标。

**视觉特征离散化**：通过预训练的 VQ-VAE 码本将连续视觉特征 $\mathbf{f}_i$ 量化为离散的外观标记 $a_i$。码本将对象外观映射到视觉-语言对齐的离散空间中，使生成模型能够以离散标记形式预测对象外观。

**谓词标记化**：每个真实谓词短语 $r_{ij}^{\star}$ 通过量化函数 $k$ 映射到离散码本索引：

$$
p_{ij} = k(r_{ij}^{\star}) \in [K_r]
$$

这一过程将连续的关系语义压缩为紧凑的离散标记，与对象外观标记一起构成场景图的完整离散表示。

### 4.2 混合离散-连续流匹配

FlowSG 的核心创新在于将场景图生成建模为混合状态空间上的连续时间传输问题。目标场景图 $G_1$ 定义为：

$$
p_1^{\mathrm{obj}}(i) = \delta_{y_i^{\star}}, \quad p_1^{\mathrm{rel}}(i,j) = \delta_{r_{ij}^{\star}}, \quad p_1^{\mathrm{app}}(i) = \delta_{a_i^{\star}}, \quad \mathbf{b}_i(1) = \mathbf{b}_i^{\star}
$$

**初始化策略**：对象类别 $c_i$ 不被掩码，而是作为先验引导关系和外观的生成，以简化训练并增强稳定性。关系类型和外观码被完全掩码，边界框从标准高斯噪声初始化。

**耦合演化系统**：在混合图空间中，连续节点坐标、离散节点类别和离散边类别通过以下耦合系统同时演化：

$$
\begin{aligned}
x_t^{(n)} &: \frac{d}{dt} x_t^{(n)} = \nu_\theta^{\mathrm{node}}(x_t^{(n)}, t, G_t, C) \\
p_t^{(n)} &: \frac{d}{dt} p_t^{(n)} = p_t^{(n)} R_\theta^{\mathrm{node}}(t, G_t, C) \\
p_t^{(ij)} &: \frac{d}{dt} p_t^{(ij)} = p_t^{(ij)} R_\theta^{\mathrm{edge}}(t, G_t, C)
\end{aligned}
$$

其中 $G_t$ 为当前时刻的噪声图状态，$C$ 为冻结的图像条件特征。连续流匹配（CFM）处理边界框几何的连续演化，离散流匹配（DFM）处理类别和谓词标记的离散跳转。

### 4.3 图 Transformer 去噪器

去噪器采用图感知的 DiT 风格 Transformer，包含三个关键模块。

**节点与边嵌入初始化**：从噪声标记和边界框构建初始表示：

$$
\mathbf{h}_i^{(0)} = \big[ \mathrm{Emb}(c_i^t) \oplus \mathrm{Emb}(a_i^t) \oplus \mathrm{Enc}(\mathbf{b}_i^t) \big]
$$

$$
\mathbf{e}_{ij}^{(0)} = \mathrm{Emb}(p_{ij}^t)
$$

**关系调制自注意力（ReSA）**：通过 FiLM 门控将关系语义注入注意力计算：

$$
\alpha_{ij}(t) = \mathrm{softmax}_j \left( \frac{\mathbf{q}_i^\top \mathbf{k}_j}{\sqrt{d}} + \mathrm{FiLM}(\mathbf{e}_{ij}^{(\ell)}) \right)
$$

这一机制使注意力权重能够根据当前预测的边类型动态调整，实现语义与几何的耦合。

**流条件消息聚合（FMA）**：计算邻域统计矩并施加可学习的度感知缩放，其上下文向量为：

$$
\zeta_i(t)^\ell = \big[ \phi(t) \oplus \log(1 + \deg(i, t)^\ell) \oplus \bar{\mathbf{r}}_i^\ell(t) \big]
$$

其中 $\phi(t)$ 为时间嵌入，$\deg(i, t)^\ell$ 为节点度，$\bar{\mathbf{r}}_i^\ell(t)$ 为局部关系信息的聚合。FMA 通过度感知加权正则化高低度节点间的消息传递，缓解图结构不均衡问题。

**全局图像交叉注意力**：将图像特征作为全局条件注入每一层，确保生成过程与视觉证据保持一致。

### 4.4 训练目标

整体损失函数为连续流匹配损失与离散流匹配损失的加权组合：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{CFM}} + \lambda \mathcal{L}_{\mathrm{DFM}}
$$

**连续流匹配损失**：训练神经向量场 $\nu_\theta$ 以匹配目标速度场 $u^\star$：

$$
\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{(x_0, x_1) \sim \pi} \big\| \nu_\theta(x_t, t, c) - u^\star(x_t, t | x_0, x_1) \big\|_2^2
$$

其中 $x_t = \psi_t(x_0, x_1)$ 为插值路径，$u^\star(x_t, t \mid x_0, x_1) = \partial_t \psi_t(x_0, x_1)$ 为目标速度。

**离散流匹配损失**：采用时间条件交叉熵，预测干净后验分布：

$$
\mathcal{L}_{\mathrm{DFM}} = -\sum_i \sum_{m=1}^{n_o} \log p_{1|t}(a_{i,m}^1 \mid G_t, C) - \sum_{(i,j)} \sum_{m=1}^{n_r} \log p_{1|t}(p_{ij,m}^1 \mid G_t, C)
$$

该损失同时覆盖对象外观标记和关系谓词标记的预测，使模型在每一步迭代中都能估计目标分布。

**推理过程**：推理时通过积分常微分方程将样本从先验传输到数据分布：

$$
\frac{d}{dt} x_t = \nu_\theta(x_t, t, c)
$$

离散部分则根据预测的速率矩阵 $R_\theta$ 进行采样跳转，最终输出完整的场景图。



## 实验与关键发现

### 主实验结果

FlowSG 在封闭词汇和开放词汇两种设定下均取得了领先的场景图生成性能。表 1 报告了两阶段方法在 PSG 和 VG 数据集上的闭集结果。在 PSG SGDet 任务上，FlowSG 的 R@50/mR@50 达到 **46.3/42.7**，R@100/mR@100 达到 **53.3/48.3**，较此前最优的 **USG-Par** (Wu et al., CVPR 2025) 提升约 3 个点。在 PSG PredCls 任务上，FlowSG 的 R@50/mR@50 达到 **69.4/54.9**，R@100/mR@100 达到 **74.3/61.3**，同样显著领先。在 VG SGDet 闭集设定下，FlowSG 的 R@50 达到 **36.5**，优于此前最优单阶段方法约 3 个点（表 2）；在 VG PredCls 上，R@50 达到 **65.7**，同样取得最优。

表 3 展示了开放词汇设定下的对比。FlowSG 在 PSG 和 VG 数据集上均超越了包括 **OpenPSG** (Zhou et al., ECCV 2024) 在内的现有 SOTA 模型，验证了生成式范式在开放场景中的泛化能力。

### 消融实验

**图 Transformer 组件消融**（表 4，PSG 闭集 SGDet）揭示了各模块的贡献层级：

- **移除流条件消息聚合（FMA）** 导致 R@50 从 46.3 骤降至 40.5（-5.8），证实 FMA 中时间条件邻域聚合和度感知缩放的关键作用。
- **丢弃全局图像特征的交叉注意力** 造成最大降幅，R@50 从 46.3 降至 39.2，表明图像条件在整个去噪过程中不可或缺。
- 移除关系调制自注意力（ReSA）中的 FiLM 门控同样带来显著退化，验证了边条件注入对谓词推理的必要性。

**标记化设计消融**（表 5）显示：
- 将 VQ-VAE 码本大小从 32×256 增大到 64×256 带来两位数提升（R@50 从 32.7 升至 43.3），表明更大的离散码本空间能更好地保留视觉语义信息。
- 使用 M=4 个有序槽位进行因子分解达到最优（R@50/mR@50 46.3/42.7），M=3 和 M=5 均导致性能下降，说明适中的槽位数在表达能力和学习难度之间取得平衡。

### 采样策略与渐进生成

图 3 对比了四种采样策略在闭集 PSG 上的表现。结果表明，采用 ODE 积分器进行确定性采样显著优于随机采样策略，验证了流匹配框架中连续时间传输的稳定性。图 4 可视化了从噪声图逐步精炼的过程：在 t=0.1 时预测尚粗糙，到 t=0.4 时语义和几何已基本收敛，t=0.6 时达到与真值高度一致的结构。这直观印证了 FlowSG 作为渐进式生成过程的核心主张——场景图并非一次性分类产出，而是通过迭代去噪逐步“生长”为语义与几何一致的整体。

### 失败模式与局限

尽管 FlowSG 在主流基准上取得了领先结果，分析中未报告系统的失败模式分析或显式局限性讨论。以下观察需结合实验证据谨慎解读：

- **对检测器质量的依赖**：FlowSG 沿用冻结检测器的两阶段范式，对象类别的预测结果直接作为先验参与生成。当检测器漏检或误检时，错误会传播至关系生成阶段。虽然论文指出对象类别不参与掩码以增强稳定性（Section 4.2），但检测器后端的选择和性能对最终指标的影响未做消融验证。
- **推理效率**：渐进式生成需要多步 ODE 积分，推理成本高于单次前向传递的确定性方法。论文未提供推理时间对比或步数-性能权衡分析，实际部署效率需进一步评估。
- **开放场景的边界**：尽管开放词汇实验表现优异，但 FlowSG 仍依赖预定义的 VQ-VAE 码本对视觉特征和谓词进行离散化。在完全开放的、不断涌现新视觉概念和关系的环境中，码本的覆盖率和更新机制仍是未解决的问题。

### 补充图表

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/003_Table_1.jpg]]
*Table 1: Results of two-stage methods on PSG and VG under the closed-set protocol. † denotes reproduced numbers. Best and second-best are marked in bold and underlined, respectively*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/004_Table_3.jpg]]
*Table 3: Compared to the state-of-the-art PSG and SGG models on the VG and PSG dataset in the open-set [4] scenario. ∗ denotes training with the same dataset*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/005_Table_2.jpg]]
*Table 2: Performance of one-stage methods on VG dataset on SGDet task in the closed-set scenario*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/006_Table_4.jpg]]
*Table 4: Ablation of graph transformer components on PSG under the closed-set SGDet; “MA” denotes message aggregation*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/007_Table_5.jpg]]
*Table 5: Ablation of tokenization on PSG: (top) effect of codebook size ??×??; (bottom) slot factorization levels ??*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/008_Figure_3.jpg]]
*Figure 3: Results of four sampling strategies on closed-set PSG*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/009_Figure_4.jpg]]
*Figure 4: Progressive FlowSG. From the input image (bottom-left) and ground truth at ??=0 (top-left), we show predictions refined at ?? ∈ 0.1, 0.2, 0.4, 0.6*

![[assets/figures/papers/paper_list_l2447_https_arxiv_org_abs_2604_18623/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of recent SGG paradigms. (a) Twostage: a pre-trained detector proposes objects and enumerates human–object pairs; a relation head refines multi-stream features to classify predicates. (b) One-stage: objects and predicates are detected jointly in a single pass, followed by a matching step to attach predicates to object pairs. (c) Ours (generative): given an image and an initially noisy graph, an image-conditioned denoiser iteratively refines the graph to sample a coherent scene graph*



## 定位与知识库关联

### 1. 与现有SGG范式的关系

FlowSG 的提出根植于对现有场景图生成（SGG）范式根本性瓶颈的重新审视。传统方法可归纳为两大范式：

- **两阶段范式**：以 **Neural Motifs**（Zellers et al., CVPR 2018）为代表的经典路线，先由预训练检测器生成对象提议并枚举主体-客体对，再由关系头融合多流特征对谓词进行分类。该范式将关系预测完全解耦为独立的分类任务，缺乏对图结构全局一致性的显式建模。
- **单阶段范式**：以 **GPS-Net**（Lin et al., CVPR 2020）为代表，试图在单次前向传递中联合检测对象和谓词，再通过匹配步骤将谓词附着到对象对上。虽提升了效率，但本质上仍是一次性的确定性决策。

这两种范式的共同瓶颈在于：**均将SGG视为单次确定性分类问题，缺乏迭代式修正能力和全局结构约束**（Figure 1）。FlowSG 将此问题重新定义为**混合离散-连续空间上的渐进生成过程**：从噪声图出发，通过流匹配（Flow Matching）联合去噪边框几何和语义标记，在几步推理内逐步精炼出语义与几何一致性的场景图。

### 2. 与生成模型谱系的关系

FlowSG 在生成模型谱系中处于**离散-连续混合流匹配**与**图结构生成**的交叉点：

- **连续流匹配（CFM）** 方面，FlowSG 继承了条件流匹配（Conditional Flow Matching）框架，将边框坐标的演化建模为常微分方程（ODE）的积分过程：$\frac{d}{dt} x_t = \nu_\theta(x_t, t, c)$。训练目标为 $\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{(x_0, x_1) \sim \pi} \| \nu_\theta(x_t, t, c) - u^\star(x_t, t | x_0, x_1) \|_2^2$。
- **离散流匹配（DFM）** 方面，FlowSG 将对象类别、外观标记和关系谓词视为离散标记，通过时间条件交叉熵损失 $\mathcal{L}_{\mathrm{DFM}}$ 预测干净后验分布，实现语义标记的渐进式去噪。
- **图结构建模**方面，FlowSG 在图Transformer中引入**关系调制自注意力（ReSA）** 和**流条件消息聚合（FMA）**，通过FiLM门控注入关系语义，并通过度感知的邻居聚合正则化高低度节点间的消息传递，实现了语义与几何的耦合生成。

与扩散模型（如DDPM）相比，FlowSG 采用连续时间流匹配而非离散时间步扩散，推理时通过ODE求解器实现少步采样；与自回归图生成方法相比，FlowSG 的并行图级去噪避免了顺序生成的累积误差。

### 3. 与SOTA的直接对比定位

在PSG和VG数据集上，FlowSG 与当前SOTA方法 **USG-Par**（Wu et al., CVPR 2025）的对比明确了其性能定位：

- **PSG SGDet（闭集）**：FlowSG 达到 R@50/mR@50 为 46.3/42.7，R@100/mR@100 为 53.3/48.3，较 USG-Par 提升约3个点（Table 1）。
- **PSG PredCls（闭集）**：FlowSG 达到 R@50/mR@50 为 69.4/54.9，R@100/mR@100 为 74.3/61.3。
- **VG SGDet（闭集）**：FlowSG 达到 R@50 36.5，较最佳单阶段方法提升约3个点（Table 2）。
- **开放词汇场景**：FlowSG 在PSG和VG开集设置下同样取得领先结果（Table 3），表明该生成范式对词汇分布偏移具有较好的鲁棒性。

在开放词汇全景场景图生成方面，FlowSG 与 **OpenPSG**（Zhou et al., ECCV 2024）形成互补：OpenPSG 聚焦于全景分割与场景图的联合建模，而FlowSG 提供了一种通用的渐进式生成框架，可适配不同的检测器后端。

### 4. 适用边界与局限

**适用边界**：
- FlowSG 假设对象检测器（冻结的 $\Phi_{\det}$）能够提供足够质量的初始提议，对象类别作为先验信息参与生成（不被掩码），这简化了训练但意味着检测器质量直接影响生成上限。
- 当前设计适用于静态图像场景图生成，依赖预训练的CLIP视觉编码器提取全局图像特征作为条件 $C$。

**已识别的局限与开放问题**：
- **推理效率**：虽然FlowSG通过少步ODE求解器（如4-8步）实现推理，但混合离散-连续流匹配的图Transformer在每步中需执行关系调制注意力和消息聚合，计算复杂度为 $O(N^2)$（$N$ 为节点数），在密集场景中可能成为瓶颈。如何进一步提升推理效率以支持实时应用仍是一个开放问题。
- **动态场景泛化**：当前框架针对静态图像设计，其在视频场景图生成或动态环境中的泛化能力尚未验证。时间维度的流匹配扩展需要额外的时序建模机制。
- **开放世界鲁棒性**：虽然开集实验显示了初步的泛化能力，但面对长尾分布中的罕见谓词和未见对象组合时，离散码本的覆盖率和流匹配的先验分布设计仍需进一步研究。
- **评估指标局限性**：当前主要使用R@K和mR@K作为评估指标，这些指标侧重于谓词分类精度，对图结构整体一致性的评估尚不充分。论文未提供图级结构一致性指标（如图编辑距离）的定量分析。

### 5. 知识库定位总结

FlowSG 的核心贡献在于**将场景图生成从分类范式转变为生成范式**，在方法谱系中建立了“图像条件混合流匹配图生成”这一新分支。其关键创新点——混合离散-连续流匹配、关系调制注意力、流条件消息聚合——为后续研究提供了三个可独立发展的技术模块。对于后续工作，FlowSG 的生成框架可自然扩展到视频场景图、3D场景图以及交互式场景图编辑等方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Can_We_Build_Scene_Graphs_Not_Classify_Them_FlowSG_Progressive_Image_Conditioned_Scene_Graph_Generation_with_Flow_Matching.pdf]]

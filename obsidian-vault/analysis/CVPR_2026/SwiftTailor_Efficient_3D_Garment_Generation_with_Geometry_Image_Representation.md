---
title: "SwiftTailor: Efficient 3D Garment Generation with Geometry Image Representation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SwiftTailor_Efficient_3D_Garment_Generation_with_Geometry_Image_Representation.pdf
project_link: null
code_link: "https://github.com/nvidia/warp"
aliases:
- SwiftTailor
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入Garment Geometry Image (GGI) 这一中间表示，将语义图、几何图与缝合图统一在UV空间中，使前馈网络GarmentSewer能够直接预测3D几何，无需物理模拟。
primary_logic: 将多图表几何图像表示与缝纫图案的语义/缝合先验融合，可通过密集预测Transformer从语义图直接回归几何图，结合重网格化与动态时域规整拼接，实现端到端的快速高质量3D服装重建。
claims:
- SwiftTailor无需物理模拟即可从缝纫图案生成3D网格，推理速度较基线提升约4倍。
- PatternMaker使用更小的InternVL-3-2B模型，在缝纫图案生成上超越基于LLaVA-1.5V-7B的AIpparel等基线。
- GGI的语义图提供强结构引导，缝合损失对齐面板边界，显著提升重建质量。
- GarmentSewer的Stage 2推理时间仅0.02秒，远快于GarmentCode的数十秒。
---

# SwiftTailor: Efficient 3D Garment Generation with Geometry Image Representation

> [!tip] 核心洞察
> 将多图表几何图像表示与缝纫图案的语义/缝合先验融合，可通过密集预测Transformer从语义图直接回归几何图，结合重网格化与动态时域规整拼接，实现端到端的快速高质量3D服装重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | SwiftTailor: 基于几何图像表示的高效3D服装生成 |
| 英文题名 | SwiftTailor: Efficient 3D Garment Generation with Geometry Image Representation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19053) · [Code](https://github.com/nvidia/warp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | SwiftTailor |
| Dataset | GCD-MM |

> [!tip] 效果简介
> - GCD-MM (GarmentCodeData multimodal) 上，Vertex L2 (生成/编辑) 3.5 / 1.5 vs AIpparel 4.8 / 2.5 (降低27% / 40%)；Stitch Acc (生成/编辑) 85.1 / 97.8 vs AIpparel 73.0 / 86.3 (提高12.1 / 11.5个百分点)。
> - GCD-MM (mesh generation) 上，MMD (↓) 5.31 vs AIpparel + GarmentCode 6.94 (降低23.5%)；COV (↑) 0.68 vs AIpparel + GarmentCode 0.52 (提高30.8%)。
> - 时间测量 上，总推理时间 (秒) 14.78 vs AIpparel + GarmentCode 63.74 (加速约4.3倍)。

## 概述

3D服装生成是数字内容创作与虚拟试穿的核心技术，其瓶颈在于从2D缝纫图案到3D网格的转换过程。现有方法（如 **GarmentCode**）依赖基于物理的缝合模拟（XPBD求解器），计算开销大且容易因规则化面板放置而失败，导致推理缓慢、网格质量不稳定。SwiftTailor 针对这一瓶颈提出了一套两阶段框架，核心创新在于引入 **Garment Geometry Image (GGI)** 作为中间表示——将语义图、几何图与缝合图统一在UV空间中，使得前馈网络可以直接预测3D几何，完全绕开物理模拟。

方法层面，SwiftTailor 由两个轻量模块构成：**PatternMaker** 采用更小的 InternVL-3-2B（2B参数）替代常见的 LLaVA-1.5V-7B，从图像或文本输入预测缝纫图案；**GarmentSewer** 基于 DPT 密集预测架构，从语义图直接回归几何图，并通过边缘感知回归损失与缝合损失保证面板边界对齐。后处理阶段利用重网格化与动态时域规整（DTW）拼接，将GGI高效转化为最终3D网格。

实验表明，SwiftTailor 在 GCD-MM 基准上全面超越 **AIpparel**、**ChatGarment**、**SewingLDM** 等基线：缝纫图案生成的 Vertex L2 误差降低27%（3.5 vs 4.8），网格生成的 MMD 降低23.5%（5.31 vs 6.94），覆盖率（COV）提升30.8%（0.68 vs 0.52）。推理效率方面，总耗时从 63.74 秒降至 14.78 秒（约4.3倍加速），其中 GarmentSewer 的 Stage 2 仅需 0.02 秒，较 GarmentCode 的数十秒提升数个数量级。消融实验证实，语义UV图提供强结构引导（去除后 CD 从 3.40 飙升至 35.77），缝合损失使 MMD 从 7.38 降至 3.36、COV 从 0.58 升至 0.88，是边界一致性的关键保障。

当前局限在于重构网格缺乏高频褶皱细节，且在复杂背景、遮挡或非常规服装等分布外输入下鲁棒性有限。未来方向包括轻量物理精化叠加、纹理生成与实时交互编辑。

## 背景与动机

### 3D服装生成的效率瓶颈

数字服装建模在虚拟试穿、影视特效与游戏产业中需求迫切，但现有自动化生成管线普遍面临**推理效率低下**与**网格质量不稳定**的双重困境。核心瓶颈在于：从2D缝纫图案到3D服装网格的转换过程严重依赖基于物理的缝合模拟。以 **GarmentCode** 为代表的构造引擎使用XPBD求解器对面板进行物理仿真，该过程不仅计算开销大（单次构造耗时数十秒），且对初始面板放置高度敏感——当面对非对称图案或复杂多面板结构时，基于规则的放置策略极易导致仿真失败或产生严重穿透、撕裂等伪影（见 Figure D.1 定性对比）。这一“物理模拟依赖”构成了当前3D服装生成管线中**最突出的效率与可靠性短板**。

### 现有方法的局限

近年来，基于视觉-语言模型（VLM）的缝纫图案生成取得了显著进展。**AIpparel** 和 **ChatGarment** 等方法利用LLaVA-1.5V-7B等大参数VLM，从图像或文本描述中推理缝纫图案的结构与参数；**SewingLDM** 则探索了基于扩散模型的生成路径。然而，这些方法在以下两个维度上仍存在明显缺口：

1. **模型效率与精度的失衡**：大参数VLM（如7B量级）推理成本高，而直接压缩模型规模往往导致生成质量显著下降，缺乏在轻量骨干上实现高精度缝纫图案推理的有效方案。
2. **构造端的速度鸿沟**：无论缝纫图案生成多快，下游的物理模拟构造器始终是速度瓶颈。将图案生成与物理仿真串行耦合的范式，使得端到端推理时间难以突破分钟级壁垒。

### 核心动机与研究问题

上述缺口指向一个根本性的研究问题：**能否彻底绕过物理模拟，直接从2D缝纫图案预测3D服装几何？**

本文的动机在于重新设计3D服装的中间表示，使其能够被前馈神经网络直接预测。关键观察是：几何图像（Geometry Image）作为一种将3D网格参数化到UV空间的成熟表示，天然适合密集预测任务。若能将缝纫图案的语义信息（面板类型）、几何信息（顶点位置）与缝合关系（边界配对）统一编码到UV空间中，形成一个紧凑的**Garment Geometry Image (GGI)** 表示，则理论上可以通过一个轻量级的前馈网络直接回归完整的3D服装几何，从而将构造时间从数十秒压缩到毫秒级。

这一思路将3D服装生成重新表述为两个可解耦的子问题：**(1) 如何用轻量VLM高效推理缝纫图案？(2) 如何用密集预测网络从缝纫图案直接合成3D网格？** 前者要求模型在参数规模与推理精度之间找到更优平衡点，后者要求设计合适的表示、网络架构与损失函数，使前馈预测的几何图能够通过简单的后处理步骤（重网格化与动态时域规整缝合）直接转换为仿真就绪的3D服装网格。

## 核心创新

SwiftTailor的核心创新在于用**Garment Geometry Image (GGI)** 这一中间表示替代了传统3D服装生成流程中依赖物理模拟的“2D缝纫图案→3D网格”转换环节。现有方法（如**GarmentCode** ）在获得缝纫图案后，必须通过基于XPBD的物理求解器进行缝合模拟才能生成3D服装网格，这一过程计算开销大、容易失败，且推理速度缓慢。SwiftTailor通过引入GGI，将语义图、几何图与缝合图统一在UV空间中，使前馈网络GarmentSewer能够直接预测3D几何，彻底消除了对物理模拟的依赖。

### 关键设计变更

| 设计维度 | 基线方法 | SwiftTailor |
|---------|---------|-------------|
| **缝纫图案生成模型骨干** | LLaVA-1.5V-7B (7B参数) | InternVL-3-2B (2B参数) |
| **服装构造方法** | 基于物理模拟的缝合引擎 (GarmentCode) | 前馈密集预测Transformer GarmentSewer + GGI |
| **中间表示** | 串行化缝纫图案 → 直接物理仿真 | Garment Geometry Image (语义图+几何图+缝合图) |

### 方法瓶颈与因果机制

**核心瓶颈**：传统管线中，缝纫图案到3D网格的转换依赖物理模拟，这不仅使推理时间长达数十秒，还因规则化的面板放置策略导致模拟失败率高、网格质量不稳定。如Figure D.1所示，在相同缝纫图案输入下，GarmentCode常因启发式面板放置而失败，而GarmentSewer能稳定生成初始网格。

**因果调控点**：GGI将服装的语义类型、几何坐标和缝合关系压缩为对齐的多通道UV图像，使得3D重建问题转化为密集预测任务。GarmentSewer采用DPT架构（ViT-L编码器+多尺度卷积解码器），从语义图直接回归几何图，推理仅需0.02秒，相比GarmentCode的数十秒实现了数量级的加速。

**核心洞见**：语义图编码的面板类型提供了强结构引导——消融实验（Table 4）显示，去除语义UV图会导致重建质量急剧恶化（Chamfer Distance从3.40飙升至35.77）。缝合损失（stitching loss）通过计算配对缝合边缘边界点之间的Chamfer距离，强制对齐面板边界，使MMD从7.38降至3.36，COV从0.58升至0.88，是保证边界一致性的关键机制。

### 证据强度评估

上述因果链条有充分的实验支撑：总推理时间从63.74秒降至14.78秒（约4.3倍加速，Table 3）；网格生成质量在MMD和COV指标上分别提升23.5%和30.8%（Table 2）。消融实验明确分离了语义UV图和缝合损失的独立贡献，证据可信度高。需要手动验证的是：GGI在复杂背景、遮挡或非常规服装等分布外输入下的鲁棒性边界尚未量化评估，论文将此列为已知局限。

## 整体框架

SwiftTailor 将服装生成分解为两个顺序阶段，形成端到端的模块化流水线：**PatternMaker** 负责从多模态输入推理缝纫图案，**GarmentSewer** 负责将缝纫图案高效转换为 3D 网格，二者通过统一的 **Garment Geometry Image（GGI）** 中间表示衔接。

### 两阶段流水线总览

流水线的整体结构如 Figure 3 所示，其核心设计思想是**解耦缝纫图案的语义推理与 3D 几何的稠密重建**，从而避免传统方法对物理模拟的依赖。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/003_Figure_3.jpg]]
*Figure 3: Overall pipeline. Our PatternMaker is a relatively small vision-language model (InternVL-3-2B [46]) trained to output sewing patterns. The sewing patterns are constructed from discrete tokens and continuous parameters predicted by the VLM. Our GarmentSewer is a dense prediction transformer (DPT) that predicts a garment geometry image from the sewing patterns. In this step, we preprocess the sewing pattern to achieve the semantic and stitching map, which are then passed to the DPT to predict the geometry image, completing our garment geometry image representation (GGI). We then perform a postprocessing step to convert the GGI to a final 3D mesh*

1. **Stage 1 — PatternMaker（缝纫图案生成）**  
   PatternMaker 是一个轻量级多模态大语言模型（MLLM），以图像和/或文本作为输入，输出服装的缝纫图案 $\mathcal{P} = (\mathbf{P}, \mathbf{S})$。其中 $\mathbf{P}$ 为面板集合，每个面板 $P_i = (V_i, E_i, R_i)$ 由顶点 $V_i$、边 $E_i$ 和刚性变换 $R_i$ 定义；$\mathbf{S}$ 为缝合关系集合，每条缝合对 $s_k = (e_a, e_b)$ 指定两条需合并的边界边。PatternMaker 采用 **InternVL-3-2B** 作为骨干模型，相比基线方法使用的 LLaVA-1.5V-7B 参数量更小（2B vs 7B），但通过微调在缝纫图案生成精度上取得了更优性能。

2. **Stage 2 — GarmentSewer（几何重建）**  
   GarmentSewer 接收 PatternMaker 输出的缝纫图案，将其预处理为语义图与缝合图，再通过密集预测 Transformer（DPT）直接回归几何图，三者共同构成完整的 GGI 表示。随后经重网格化（remeshing）与动态时域规整（Dynamic Time Warping）缝合两步后处理，即可得到最终的 3D 服装网格。GarmentSewer 的推理时间仅 **0.02 秒**，比基于 GarmentCode 物理模拟的基线快数个数量级。

### 核心中间表示：Garment Geometry Image

GGI 是整个流水线的关键创新，它将缝纫图案的语义先验与几何图像表示统一在 UV 纹理空间中，由三个对齐的组件构成（见 Figure 4 左）：

- **语义图（Semantic Image）**：编码每个面板的类型信息，为 GarmentSewer 提供强结构引导；
- **几何图（Geometry Image）**：存储面板在 3D 空间中的顶点坐标，是 GarmentSewer 的直接回归目标；
- **缝合图（Stitching Image）**：标记面板边界边的配对关系，用于后处理阶段的缝合对齐。

这种表示使得 GarmentSewer 能够将 3D 服装重建转化为一个稠密图像预测问题，完全绕开了传统流程中必需的基于物理的缝合模拟（如 GarmentCode 使用的 XPBD 求解器），从根本上消除了模拟失败和计算开销大的瓶颈。

### 输入输出流

流水线支持三种输入模态：**仅图像**、**仅文本**、**图像+文本**。以多模态输入为例，完整的数据流如下：

1. 图像/文本输入 → PatternMaker（InternVL-3-2B）→ 离散 token 与连续参数 → 缝纫图案 $\mathcal{P}$
2. 缝纫图案 $\mathcal{P}$ → 预处理 → 语义图 + 缝合图 → GarmentSewer（DPT）→ 几何图 → 完整 GGI
3. GGI → 重网格化（局部三角剖分，见 Figure B.2）→ 缝合对齐（动态时域规整 + 并查集顶点合并，见 Figure B.3）→ 最终 3D 网格

整个过程无需物理重模拟，总推理时间约 **14.78 秒**（其中 Stage 1 约 14.76 秒，Stage 2 约 0.02 秒），相比 AIpparel + GarmentCode 的 63.74 秒加速约 **4.3 倍**（Table 3）。

### 补充图表

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/001_Figure_1.jpg]]
*Figure 1: We introduce SwiftTailor, a two-stage framework including PatternMaker and GarmentSewer that aims to produce sewing patterns along with a novel garment geometry image representation that can be directly decoded to final 3D garment meshes*

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/018_Figure.jpg]]
*Figure: D.2. Additional qualitative results from our pipeline. Each example shows the re-draped garment on the SMPL body together with its initial state constructed by GarmentSewer (the smaller mesh on the left). Textures are added to enhance visualization of garment geometry and structure*

## 核心模块与公式推导

### 缝纫图案的形式化定义

SwiftTailor 的整个流程建立在缝纫图案（Sewing Pattern）的精确定义之上。一个缝纫图案 $\mathcal { P }$ 由面板集合 $\mathbf{P}$ 和缝合关系集合 $\mathbf{S}$ 组成：

$$\mathcal { P } = ( \mathbf { P } , \mathbf { S } )$$

**面板集合** $\mathbf{P}$ 包含 $N$ 个面板，每个面板 $P_i$ 由三部分定义：

$$\mathbf { P } = \left\{ P _ { i } = ( V _ { i } , E _ { i } , R _ { i } ) \right\} _ { i = 1 } ^ { N }$$

其中 $V_i$ 为面板的顶点集，$E_i$ 为边界边集，$R_i$ 为面板在3D空间中的刚性变换（决定面板的放置位置与朝向）。

**缝合关系集合** $\mathbf{S}$ 包含 $M$ 个缝合对，每个缝合对指定两条需要被缝合在一起的边界边：

$$\mathbf { S } = \left\{ s _ { k } = ( e _ { a } , e _ { b } ) \mid e _ { a } , e _ { b } \in \cup _ { i = 1 } ^ { N } E _ { i } \right\} _ { k = 1 } ^ { M }$$

这一形式化定义是整个流水线的数学基础——PatternMaker 的输出目标即为 $\mathcal{P}$，而 GarmentSewer 则利用 $\mathbf{P}$ 与 $\mathbf{S}$ 构建 Garment Geometry Image (GGI) 并最终重建3D网格。

---

### 模块一：PatternMaker —— 轻量级缝纫图案生成器

PatternMaker 是一个轻量级多模态大语言模型（MLLM），负责根据图像或文本输入预测服装的缝纫图案 $\mathcal{P}$。其关键设计选择在于**骨干网络的替换**：现有方法（如 AIpparel）使用 LLaVA-1.5V-7B（7B参数）作为视觉语言模型骨干，而 PatternMaker 采用更高效的 **InternVL-3-2B**（2B参数）进行微调。这一替换不仅降低了模型规模，还在缝纫图案生成指标上取得了更优表现（详见实验部分 Table 1）。

PatternMaker 的输出包含两类信息：
- **离散 token**：编码面板类型、拓扑结构等离散属性；
- **连续参数**：编码顶点坐标、刚性变换 $R_i$ 等连续几何量。

这些输出随后被解析为结构化的 $\mathcal{P} = (\mathbf{P}, \mathbf{S})$，传递至 GarmentSewer 进行3D几何构建。

---

### 模块二：Garment Geometry Image (GGI) —— 核心中间表示

GGI 是 SwiftTailor 的核心创新，它统一了语义信息、几何信息与缝合信息于 UV 纹理空间。GGI 由三个对齐的组件构成：

1. **语义图（Semantic Image）**：编码每个 UV 像素所属的面板类型，为后续几何预测提供强结构引导；
2. **几何图（Geometry Image）**：存储每个 UV 像素对应的3D坐标 $(x, y, z)$，是传统几何图像表示的直接扩展；
3. **缝合图（Stitching Image）**：记录面板边界边的缝合对应关系，指示哪些边界段需要被合并。

GGI 的构建流程（Figure 4 左半部分）为：从缝纫图案 $\mathcal{P}$ 出发，将各面板参数化到 UV 空间，分别生成语义图与缝合图作为 GarmentSewer 的输入条件；GarmentSewer 预测几何图后，三者共同构成完整的 GGI。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/004_Figure_4.jpg]]
*Figure 4: (Left) We present how to prepare the three components (geometry, semantic and stiching) of our propose Garment Geometry Image (GGI); (Right) From the estimated geometry and stiching images of GarmentSewer and PatternMaker, two additional remeshing and stiching steps are performed to obtain the final 3D mesh result*

---

### 模块三：GarmentSewer —— 密集预测Transformer

GarmentSewer 是从语义图到几何图的映射网络，设计为标准的 **DPT（Dense Prediction Transformer）架构**，由 ViT 编码器和多尺度卷积解码器组成。其输入为语义图（可选地拼接缝合图信息），输出为预测的几何图 $\hat{\mathcal{G}}$。

GarmentSewer 的训练由两个互补的损失函数驱动：

#### 边缘感知回归损失 $\mathcal{L}_{\mathrm{reg}}$

$$\mathcal { L } _ { \mathrm { r e g } } = \| \mathcal { G } - \hat { \mathcal { G } } \| _ { 1 } + \alpha \| \mathcal { G } _ { \mathrm { e d g e } } - \hat { \mathcal { G } } _ { \mathrm { e d g e } } \| _ { 1 }$$

该损失在标准 L1 回归的基础上，对面板边缘邻近带（宽度 $w=10$ 像素）施加权重 $\alpha=100$ 的额外惩罚。$\mathcal{G}_{\mathrm{edge}}$ 和 $\hat{\mathcal{G}}_{\mathrm{edge}}$ 分别表示真实几何图与预测几何图中位于边缘带内的像素子集。这一设计确保网络优先学习面板边界的精确几何，因为边界精度直接决定后续缝合质量。

#### 缝合损失 $\mathcal{L}_{\mathrm{stitch}}$

$$\mathcal { L } _ { \mathrm { s t i t c h } } = \frac { 1 } { | \mathrm { \bf S } | } \sum _ { ( e _ { a } , e _ { b } ) \in \mathrm { \bf S } } \mathrm { C D } \big ( \hat { \mathcal { G } } _ { \mathrm { e d g e } } ( e _ { a } ) , \hat { \mathcal { G } } _ { \mathrm { e d g e } } ( e _ { b } ) \big )$$

该损失对所有缝合对 $(e_a, e_b) \in \mathbf{S}$，计算预测几何图中两条配对边界边对应点之间的 Chamfer 距离（CD）。其作用是强制缝合边界的几何一致性——即两条应被缝合的边在3D空间中应尽可能接近。消融实验（Table 4）表明，仅使用 $\mathcal{L}_{\mathrm{reg}}$ 可恢复大部分形状，但加入 $\mathcal{L}_{\mathrm{stitch}}$ 后 MMD 从 7.38 降至 3.36，COV 从 0.58 升至 0.88，验证了缝合损失对边界一致性的关键作用。

训练超参数设置为 $\lambda_{\mathrm{reg}}=1$，$\lambda_{\mathrm{stitch}}=1000$，$\lambda_{\mathrm{norm}}=0.01$，$\alpha=100$。GarmentSewer 的 ViT-L 编码器从 ImageNet 预训练权重初始化。

---

### 后处理：重网格化与动态缝合

GGI 完成后，通过两步后处理得到最终3D网格（Figure 4 右半部分）：

1. **重网格化（Remeshing）**：从 UV 对齐的几何图出发，检查每个 $2 \times 2$ UV 单元的有效顶点占用情况，生成一个或两个三角形面片。当四个顶点均有效时，选择对角线中3D距离较短者，确保面片法向一致朝外（Figure B.2）。

2. **动态时域规整缝合（Dynamic Time Warping Stitching）**：利用缝合图将配对边界边通过动态时域规整对齐，随后通过并查集合并对应顶点，消除面板间的缝隙与不连续（Figure B.3）。

这一后处理流程完全替代了传统基于物理模拟的缝合过程（如 GarmentCode 使用的 XPBD 求解器），是实现快速推理的关键——GarmentSewer 的 Stage 2 推理仅需 0.02 秒，而 GarmentCode 需要数十秒。

### 补充图表

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/002_Figure_2.jpg]]
*Figure 2: Preliminaries on geometry images [11, 38], an imagebased 3D representation that parameterizes a 3D mesh into charts, each being stored as simple arrays of pixels. Our work integrates geometry images with semantic and stitching information to establish garment panels, yielding a novel garment geometry image representation suitable for 3D garment generation*

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/013_Figure.jpg]]
*Figure: B.3. Stitching results before and after seam alignment. Using the stitching image, boundary edges are paired and aligned via Dynamic Time Warping, followed by vertex merging through a disjoint-set union. The zoomed-in wireframe views highlight how stitching resolves discontinuities and removes gaps between corresponding panel edges, achieving globally coherent garment mesh. The example is conducted on predicted sewing pattern from PatternMaker*

## 实验与分析

### 评估设置与基准

SwiftTailor 的实验评估围绕两个核心任务展开：**缝纫图案生成/编辑** 和 **3D网格生成**。主要基准数据集为 **GCD-MM**（GarmentCodeData multimodal），包含图像-文本配对数据，用于多模态条件下的服装生成。评估采用固定训练/测试划分，所有方法在相同硬件（4×A100）和采样预算（最多20次尝试）下运行，确保公平对比。

缝纫图案生成的评价指标包括 **Vertex L2**（面板顶点坐标误差）、**#Panel Acc**（面板数量预测准确率）和 **Stitch Acc**（缝合关系预测准确率）。3D网格生成的评价指标包括 **MMD**（↓，最大均值差异）、**COV**（↑，覆盖率）、**CD**（↓，Chamfer距离）和 **EMD**（↓，推土机距离）。

### 主实验结果

#### 缝纫图案生成与编辑

Table 1 展示了 PatternMaker 与基线方法在缝纫图案生成和编辑任务上的定量对比。PatternMaker 使用更小的 **InternVL-3-2B**（2B参数）骨干网络，在生成任务上 Vertex L2 达到 **3.5**，较基于 LLaVA-1.5V-7B 的 **AIpparel**（4.8）降低 **27%**；Stitch Acc 达到 **85.1**，较 AIpparel（73.0）提高 **12.1个百分点**。在编辑任务上，PatternMaker 的 Vertex L2 为 **1.5**，较 AIpparel（2.5）降低 **40%**；Stitch Acc 达 **97.8**，较 AIpparel（86.3）提高 **11.5个百分点**。这一提升源于 InternVL-3-2B 的高效微调策略，在更少参数下实现了更强的缝纫图案推理能力。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on sewing-pattern generation (left) and editing (right). Best results are shown in bold*

#### 3D网格生成

Table 2 报告了多模态输入（图像+文本）下的网格生成结果。SwiftTailor（PatternMaker + GarmentSewer）取得最优性能：**MMD 5.31**，较 AIpparel + GarmentCode 组合（6.94）降低 **23.5%**；**COV 0.68**，较基线（0.52）提高 **30.8%**。值得注意的是，当 PatternMaker 与 GarmentCode 物理模拟引擎组合时，MMD 为 6.94，而 GarmentSewer 替代物理模拟后降至 5.31，直接证明了 **GarmentSewer 的前馈密集预测范式在重建精度上优于传统物理模拟**。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on mesh generation using multimodal inputs (image and text). Best results are shown in bold*

Table C.4 进一步展示了不同图案生成器与服装构造器的全组合对比。无论使用何种图案生成器（PatternMaker、AIpparel、ChatGarment、SewingLDM），搭配 GarmentSewer 的网格质量均一致优于搭配 GarmentCode 的组合，验证了 GGI 表示与 GarmentSewer 构造范式的普适优势。

#### 推理效率

Table 3 的运行时对比揭示了 SwiftTailor 的显著加速。总推理时间 **14.78秒**，其中 Stage 1（PatternMaker 图案生成）占 14.76 秒，**Stage 2（GarmentSewer 网格构造）仅需 0.02秒**。相比之下，AIpparel + GarmentCode 总耗时 63.74 秒，其中 GarmentCode 物理模拟阶段即占 49.14 秒。SwiftTailor 整体加速约 **4.3倍**，且 GarmentSewer 的构造速度较 GarmentCode 快三个数量级。这一优势源于 GGI 表示将 3D 几何预测转化为 2D 密集预测问题，完全绕过了迭代物理求解。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/008_Table_3.jpg]]
*Table 3: Running time comparison to obtain the final mesh (in seconds) between other baselines and our SwiftTailor. Stage 1 is generating patterns, while Stage 2 is constructing mesh from them*

### 消融实验

Table 4 系统消融了语义UV图与辅助损失对 GarmentSewer 重建质量的影响。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/006_Table_4.jpg]]
*Table 4: Ablation on semantic UV map and auxiliary losses*

**语义UV图的关键作用**：去除语义UV图（仅使用二值掩码作为输入）导致性能急剧恶化——CD 从 3.40 飙升至 **35.77**，MMD 从 3.36 升至 11.96，COV 从 0.88 降至 0.49。这验证了面板类型编码为网络提供了强结构引导，使其能够准确区分不同面板并预测其空间位置。Figure 6 的定性结果佐证了这一发现：使用二值图输入时，GarmentSewer 无法正确放置面板，产生严重形变。

**缝合损失的必要性**：仅使用边缘感知回归损失 $\mathcal{L}_{\mathrm{reg}}$ 时，网络已能恢复大部分服装形状（CD 5.48，MMD 7.38），但缝合边界存在明显不一致。加入缝合损失 $\mathcal{L}_{\mathrm{stitch}}$ 后，所有指标显著提升：MMD 从 7.38 降至 **3.36**，COV 从 0.58 升至 **0.88**，CD 从 5.48 降至 3.40。缝合损失通过 Chamfer 距离显式对齐配对缝合边的边界点，有效解决了面板间的缝隙与错位问题（Figure 7 定性展示）。

**损失权重配置**：训练 GarmentSewer 时，$\lambda_{\mathrm{reg}}=1$，$\lambda_{\mathrm{stitch}}=1000$，$\lambda_{\mathrm{norm}}=0.01$，边缘带宽度 $w=10$，边缘权重 $\alpha=100$。高缝合损失权重反映了边界一致性对最终网格质量的决定性影响。

### 定性分析与失败模式

Figure 5 展示了 SwiftTailor 与 **ChatGarment**、**SewingLDM**、**AIpparel** 在不同输入模态（纯图像、纯文本、图像+文本）下的定性对比。SwiftTailor 生成的服装网格在面板结构完整性和缝合边界一致性上均优于基线，尤其在复杂服装款式（如多面板拼接）上优势明显。

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative comparisons between SwiftTailor and recent state-of-the-art methods on 3D garment modeling [1, 27, 32] using an image, a text prompt, and both text and image as input, respectively*

Figure D.1 直接对比了 GarmentSewer 与 GarmentCode 在相同 PatternMaker 输出上的表现。GarmentCode 因基于规则的刚性面板放置策略，常产生穿透、错位或模拟失败；GarmentSewer 则生成稳定初始化和一致的悬垂形态，验证了前馈预测在鲁棒性上的优势。

**已知局限性**：
- **高频细节缺失**：GarmentSewer 平滑了几何变化，重构网格缺乏真实褶皱细节，无法恢复织物纹理级形变。
- **分布外鲁棒性不足**：在复杂背景、遮挡或非常规服装款式等分布外输入下性能下降，需要更强的视觉编码器或数据增强。
- **功能缺失**：当前管道未集成材质属性或可编辑接口，限制了在真实应用场景中的实用性。

### 补充实验结果

附录中的 Table C.1–C.3 分别报告了仅图像条件和仅文本条件下的生成结果，SwiftTailor 在所有设置下均保持领先。Table C.4 的全组合实验已在前文讨论，进一步巩固了 GarmentSewer 作为通用服装构造器的地位。

Figure B.1 展示了混合插值方案对几何图像质量的影响：纯重心插值在面板边界产生锯齿状不连续值，而混合插值（边界线性插值+内部重心插值）产生平滑一致的边界信号，防止伪影传播至 GarmentSewer 预测。Figure B.2 和 B.3 分别详述了重网格化与动态时域规整缝合的后处理流程，构成了 GGI 到最终 3D 网格的完整逆映射链路。

### 补充图表

![[assets/figures/papers/paper_list_l2270_https_arxiv_org_abs_2603_19053/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative results on generated 3D mesh using geometry vs. binary image as input to GarmentSewer*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果转折

现有3D服装生成流水线的根本瓶颈在于**构造阶段对物理模拟的强依赖**。主流方案（如基于**GarmentCode** (Korosteleva & Lee, SIGGRAPH 2024) 的框架）将2D缝纫图案输入基于XPBD的求解器进行缝合模拟，这一过程存在两个致命缺陷：一是计算开销极大，单次模拟耗时数十秒；二是规则化的面板放置策略极易导致模拟失败，产生不可用的网格输出。**AIpparel** 和 **ChatGarment** 等工作虽然在缝纫图案生成上引入了视觉语言模型，但下游仍受制于GarmentCode的物理引擎，形成“生成快、构造慢”的失衡局面。

SwiftTailor的因果转折在于**用前馈预测替代物理模拟**。核心操作变量是引入Garment Geometry Image (GGI) 作为中间表示——将语义图、几何图与缝合图统一在UV空间中，使前馈网络GarmentSewer能够直接从语义图回归3D几何。这一转变将服装构造从“模拟一个物理过程”重新定义为“预测一个几何映射”，从根本上绕开了XPBD求解器的计算瓶颈和失败风险。

### 2. 方法谱系中的位置

SwiftTailor在3D服装生成谱系中占据了一个独特位置：它既不属于纯物理模拟流派，也不完全属于隐式神经表示流派，而是在**几何图像表示**这一经典思路上进行了面向服装的深度改造。

**上游继承关系：**
- **几何图像 (Geometry Images)** (Gu et al., SIGGRAPH 2002; Sander et al., 2003)：将3D网格参数化到2D图像阵列的思想是GGI的理论基础。SwiftTailor的创新在于将单图表几何图像扩展为多图表表示，并与语义和缝合信息融合。
- **密集预测Transformer (DPT)** (Ranftl et al., ICCV 2021)：GarmentSewer直接采用DPT架构（ViT-L编码器 + 多尺度卷积解码器），将其从深度估计任务迁移到几何图预测任务。
- **InternVL-3-2B** (Zhu et al., 2024)：PatternMaker选择该轻量级VLM替代LLaVA-1.5V-7B，在保持性能的同时大幅降低参数量。

**与同期工作的差异：**
- **AIpparel** (Shen et al., ECCV 2024)：同属VLM驱动的缝纫图案生成路线，但其下游依赖GarmentCode物理模拟。SwiftTailor在Stage 1采用更轻量的InternVL-3-2B，在Stage 2用GarmentSewer完全替代物理引擎。
- **ChatGarment** (Anonymous, 2024)：同样使用VLM生成缝纫图案，但未涉及构造阶段的加速。
- **SewingLDM** (Liu et al., 2024)：基于扩散模型的缝纫图案生成，属于生成式路线，与SwiftTailor的回归式路线互补而非直接竞争。

### 3. 关键设计选择与消融证据

**语义UV图的强结构引导（Table 4）：**
去除语义UV图后，Chamfer Distance从3.40飙升至35.77（恶化约10倍），MMD从3.36升至11.96，COV从0.88降至0.49。这表明语义面板类型编码为GarmentSewer提供了不可替代的空间先验——网络需要知道“哪个区域是前片、哪个是后片”才能正确放置面板。二值掩码（Figure 6）无法提供这种区分性信息。

**缝合损失的关键作用（Table 4）：**
仅使用边缘感知回归损失 $\mathcal{L}_{\mathrm{reg}}$ 时，MMD为7.38，COV为0.58；加入缝合损失 $\mathcal{L}_{\mathrm{stitch}}$ 后，MMD降至3.36，COV升至0.88。这说明回归损失能恢复大部分形状，但无法保证缝合边界的几何一致性——面板边界在3D空间中可能错位。缝合损失通过Chamfer距离显式约束配对边界的对齐，是保证最终网格全局一致性的关键。

**混合插值方案（Figure B.1）：**
纯重心坐标插值在面板边界产生锯齿状不连续值，偏离真实轮廓；SwiftTailor的混合方案在边缘使用线性插值、三角形内部使用重心插值，产生平滑一致的边界信号。这一细节设计阻止了几何图伪影向GarmentSewer预测传播。

### 4. 适用边界与失效模式

**已知局限：**
1. **高频细节缺失**：GarmentSewer平滑了几何变化，重构网格缺乏真实服装的褶皱和纹理细节。这是前馈回归的固有局限——网络学习的是条件均值，而非完整的几何分布。
2. **分布外鲁棒性有限**：复杂背景、遮挡或非常规服装款式下性能下降。需要更强的视觉编码器或数据增强来覆盖长尾分布。
3. **无材质与可编辑性**：当前管道仅输出几何，未集成材质属性或交互式编辑接口。

**推断的隐性边界（需人工验证）：**
- GGI表示假设服装可被分割为有限数量的可展平面板，对于一体成型或拓扑复杂的服装可能不适用。
- 多图表UV参数化依赖预定义的模板划分，对新类别服装的泛化能力受限于训练数据的面板类型覆盖范围。
- 重网格化步骤（Figure B.2）的2×2单元三角剖分策略假设几何图分辨率足够高，低分辨率下可能产生拓扑错误。

### 5. 开放问题与演进方向

1. **近实时缝纫图案生成**：当前Stage 1（PatternMaker）仍需约14.7秒，是整体管道的瓶颈。能否通过模型蒸馏或推测解码将VLM推理压缩到亚秒级？
2. **轻量物理精化叠加**：在GarmentSewer的稳定初始化上叠加少量物理模拟步骤（而非完整XPBD），是否能在保持速度优势的同时恢复褶皱细节？这类似于“预测+校正”的混合范式。
3. **纹理与材质联合生成**：GGI表示天然支持UV空间操作，将RGB纹理通道与XYZ几何通道联合预测是一个直接可行的扩展方向。
4. **交互式编辑接口**：缝纫图案的离散-连续混合表示（离散token + 连续参数）为局部编辑提供了天然接口——用户修改单个面板形状或缝合关系，GarmentSewer可实时更新对应区域的几何图。

## 原文 PDF

![[paperPDFs/CVPR_2026/SwiftTailor_Efficient_3D_Garment_Generation_with_Geometry_Image_Representation.pdf]]
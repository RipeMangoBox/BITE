---
title: "ArtHOI: Taming Foundation Models for Monocular 4D Reconstruction of Hand-Articulated-Object Interactions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ArtHOI_Taming_Foundation_Models_for_Monocular_4D_Reconstruction_of_Hand_Articulated_Object_Interactions.pdf
project_link: "https://arthoi-reconstruction.github.io"
code_link: null
aliases:
- ArtHOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过自适应采样细化（ASR）恢复铰接物体的度量尺度和6‑DoF位姿，并利用多模态大语言模型（MLLM）推理接触状态作为约束，联合优化手物对齐。ASR解决了归一化网格到世界空间的尺度/位姿歧义，MLLM引导的对齐则消除了手物网格之间的空间错位。
primary_logic: 基础模型能够提供丰富的几何、运动与语义先验，但其输出（归一化网格、独立重建的手）天生互不一致。ArtHOI 不抛弃这些先验，而是通过优化将它们“驯服”：ASR 在自适应范围内搜索度量尺度与位姿以最大化渲染掩码与观测掩码的 IoU；MLLM 则通过结构化提示获得可靠的逐帧接触信息，并将接触作为约束进行两阶段手物联合优化，从而在无需任何物体模板或预扫描的条件下实现单目 4D 交互重建。
claims:
- 在 ArtHOI‑RGBD 数据集的所有五类物体上，ArtHOI 的 Chamfer Distance 均显著优于 RSRD（尽管 RSRD 额外利用预扫描）和 EasyHOI。
- 在 RSRD 数据集上 ArtHOI 取得与预扫描方法 RSRD 可比甚至更优的重建精度，且无需物体预扫描。
- ASR 在规范网格姿态与尺度优化任务上，IoU 和成功率均超过 FoundationPose 和 Any6D。
- MLLM 引导的手物对齐优化使碰撞‑接触（Co²）评分大幅降低至 0.029（ArtHOI-RGBD）和 0.039（ArtHOI‑Wild），证明接触约束对消除穿透和错位至关重要。
---

# ArtHOI: Taming Foundation Models for Monocular 4D Reconstruction of Hand-Articulated-Object Interactions

> [!tip] 核心洞察
> 基础模型能够提供丰富的几何、运动与语义先验，但其输出（归一化网格、独立重建的手）天生互不一致。ArtHOI 不抛弃这些先验，而是通过优化将它们“驯服”：ASR 在自适应范围内搜索度量尺度与位姿以最大化渲染掩码与观测掩码的 IoU；MLLM 则通过结构化提示获得可靠的逐帧接触信息，并将接触作为约束进行两阶段手物联合优化，从而在无需任何物体模板或预扫描的条件下实现单目 4D 交互重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | ArtHOI：驯服基础模型实现单目视频中手与铰接物体的4D交互重建 |
| 英文题名 | ArtHOI: Taming Foundation Models for Monocular 4D Reconstruction of Hand-Articulated-Object Interactions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25791) · [Project](https://arthoi-reconstruction.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ArtHOI |
| Dataset | ArtHOI‑RGBD, RSRD, ARCTIC, ArtHOI‑RGBD / RSRD / ArtHOI‑Wild |

> [!tip] 效果简介
> - ArtHOI‑RGBD (Headphone) 上，CD (mm)↓ 8.124±0.44 vs 14.708±0.18 (RSRD) (-6.584)。
> - ArtHOI‑RGBD (Scissor) 上，CD (mm)↓ 4.256±1.02 vs 13.841±5.89 (RSRD) (-9.585)。
> - ArtHOI‑RGBD (Candy Box) 上，CD (mm)↓ 4.104±1.33 vs 7.768±4.88 (RSRD) (-3.664)。

## 概要

从单目 RGB 视频中重建手与**铰接物体**的 4D 交互，是理解日常操作行为的关键技术瓶颈。现有方法要么仅适用于刚性物体，要么依赖预扫描模板或多视角初始化，难以泛化至任意未知铰接物体。基础模型虽能提供丰富的几何、运动与语义先验，但其输出天然存在度量尺度模糊、手物网格空间错位和物理不合理等缺陷，导致独立重建结果无法真实反映交互。

ArtHOI 提出了一种**优化驱动的框架**，核心思路不是抛弃基础模型先验，而是通过优化将它们“驯服”以消除不一致性。该方法包含两个关键创新：**自适应采样细化（ASR）** 在自适应范围内搜索最优度量尺度与 6‑DoF 位姿，将归一化物体网格准确锚定到世界空间；**多模态大语言模型（MLLM）引导的手物对齐** 通过结构化提示推理逐帧接触状态与接触手指，并将接触信息作为约束进行两阶段联合优化，消除手物网格间的穿透与错位。

实验表明，ArtHOI 在无需任何物体模板或预扫描的条件下，在 ArtHOI‑RGBD、RSRD 和 ARCTIC 等多个数据集上均取得优于或持平需要预扫描的现有方法的重建精度（如 ArtHOI‑RGBD 上 Chamfer Distance 降低 3.7–9.6 mm，RSRD 上降低 61.1 mm），同时碰撞‑接触评分（Co²）大幅降低至 0.029–0.039，验证了 MLLM 引导对齐对物理合理性的关键作用。



从单目 RGB 视频中重建手与物体的 4D 交互，是计算机视觉与图形学中长期存在的难题。该任务要求同时恢复手部姿态、物体几何与运动，以及二者之间物理合理的空间关系，在机器人学习、增强现实和动作分析等领域具有重要应用价值。

近年来，基础模型（foundation models）在图像分割、深度估计、手部姿态重建和 3D 物体生成等单任务上取得了显著进展，为从“野生”视频中提取丰富先验提供了可能。然而，现有手物交互（HOI）重建方法主要面向**刚性物体**，或依赖**预扫描模板**与多视角视频，难以应对未知的铰接物体（如剪刀、耳机、糖果盒等）。当直接将基础模型的独立输出组合在一起时，会暴露出三个根本性缺陷：

1. **度量尺度模糊**：物体生成模型输出的是归一化网格，缺乏与真实世界对应的物理尺度，导致无法直接放置到场景中。
2. **空间错位**：手部重建（如 WiLoR）与物体重建各自独立进行，手与物体网格在 3D 空间中严重分离或穿透，无法反映真实的接触交互。
3. **物理不合理性**：即便手与物体在视觉上看似接近，也缺乏约束来保证接触的物理一致性——例如手指穿透物体内部，或接触帧中指尖悬浮于物体表面之外。

以 **EasyHOI** 和 **RSRD** 为代表的现有方法，分别受限于逐帧刚性假设和物体预扫描需求，在铰接物体场景中表现不佳。EasyHOI 无法建模铰接运动且缺乏时序一致性；RSRD 虽能处理铰接物体，但要求预先对物体进行环绕扫描以获取完整模板，这在实际应用中往往不可行。

上述瓶颈的本质在于：**基础模型提供的几何、运动与语义先验天生互不一致**，而现有方法要么抛弃这些先验，要么不加修正地直接使用。ArtHOI 的核心动机正是“驯服”而非丢弃这些先验——通过优化框架将它们统一到度量一致、空间对齐、物理合理的 4D 交互重建中，从而在**无需任何物体模板或预扫描**的条件下，仅凭单目 RGB 视频实现手与铰接物体的 4D 重建。



## 核心方法与创新机理

ArtHOI 的核心创新在于将多个基础模型的异构先验“驯服”为物理一致的 4D 手‑铰接物体交互重建，而非直接堆砌模型输出。其关键突破体现在两个 **changed slots** 上。

### 从归一化网格到度量世界：自适应采样细化 (ASR)

现有 6‑DoF 位姿估计器（如 FoundationPose）直接作用于归一化网格时，无法恢复物体的度量尺度，导致重建结果与真实世界存在任意比例缩放和空间错位。**ASR** 通过“粗估计‑自适应采样‑渲染验证”的闭环，解决了这一度量‑位姿歧义瓶颈。

具体而言，ASR 首先利用反投影深度点云计算粗尺度估计，随后在自适应范围内随机采样尺度候选；每个候选经 FoundationPose 生成位姿假设后，以**渲染掩码与观测掩码的 IoU** 作为反馈信号，动态扩大搜索范围以避免局部极值，最终选出最优尺度与位姿组合（见 Algorithm 1）。消融实验（Table 5）表明，ASR 在规范网格姿态与尺度优化任务上的平均 IoU 达到 **0.905**（ArtHOI‑RGBD）/ **0.876**（RSRD）/ **0.882**（ArtHOI‑Wild），成功率 **100%**，远超 FoundationPose 和 Any6D。这一模块是后续部件运动重建和手物对齐的几何基础——尺度错误将导致整个 4D 重建级联失效。

### 从分离重建到物理对齐：MLLM 引导的铰接 HOI 对齐

手物交互重建的另一根本困难在于：手部（WiLoR）与物体（HunYuan3D + PartField）是独立重建的，二者在空间上天然错位、穿透，无法反映真实接触。ArtHOI 引入 **MLLM 引导的接触约束优化** 来消除这一错位。

该方法采用三阶段结构化提示（Figure C‑E）：(1) **视角检测**——判断第一人称或第三人称视角，为手型映射提供先验；(2) **手型映射**——根据视角和空间线索将可见手映射为左/右手；(3) **逐帧接触推理**——结合 RGB 帧与着色深度图，利用深度不连续性分析区分真实接触与视觉邻近，输出接触状态与接触手指。消融实验（Table 6）证实，同时引入时序上下文、视角提示、假阳性抑制和深度增强四个组件时，接触推理准确率最高（RSRD Acc: **88.58%**，Wild Acc: **86.56%**）且假阳性率最低。

推理得到的接触信息随后转化为**接触损失** $$ \mathcal{L}_{\mathrm{contact}} = \sum_{i \in \mathbb{C}} \sum_{\mathbf{v}_t \in \mathbb{T}_i} \min_{\mathbf{v}_o \in \mathcal{G}_i^o} \left\| \mathbf{v}_o - \mathbf{v}_t \right\|_2 $$，即最小化指定指尖顶点到物体网格最近点的欧氏距离（Eq. 4）。该损失与加速度平滑先验和手姿 L₁ 正则项（Eq. 5）共同构成 HOI 对齐总损失 $$ \mathcal{L}_{\mathrm{hoi}} = \mathcal{L}_{\mathrm{contact}} + \mathcal{L}_{\mathrm{reg}} $$（Eq. 6），通过两阶段优化（先优化物体尺度，后联合优化手姿与全局变换）实现物理合理的手物空间组合。Table 4 显示，经 MLLM 引导对齐后，碰撞‑接触评分（Co²）大幅降至 **0.029**（ArtHOI‑RGBD）和 **0.039**（ArtHOI‑Wild），证实接触约束对消除穿透和错位至关重要。

### 创新本质

ArtHOI 的创新不在于提出新的基础模型，而在于**设计了一套优化机制来弥合基础模型先验之间的不一致性**：ASR 解决了物体从归一化空间到度量世界的接地问题，MLLM 对齐则解决了手‑物网格的空间组合问题。二者协同，使得无需任何物体模板或预扫描的单目 4D 交互重建成为可能。



ArtHOI 是一个**基于优化的框架**，核心目标是从单目 RGB 视频 $\\boldsymbol{\\gamma} = \\{ \\mathbf{I}_i \\}_{i=1}^{N}$ 中重建手与未知铰接物体的 4D 交互，全程无需物体模板或预扫描。其关键设计在于**集成并“驯服”多个基础模型的先验**，而非抛弃这些先验——基础模型提供的归一化网格、独立重建的手网格天生互不一致（尺度模糊、空间错位、物理不合理），ArtHOI 通过优化将它们协调到世界坐标系下，形成物理一致的 4D 交互表示。

整个 pipeline 按数据流可划分为四个串行模块（见 Figure 2）：

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of our ArtHOI. ArtHOI is an optimization-based framework (see subfigure (a)) that integrates and refines priors from multiple foundation models for monocular 4D reconstruction of human-articulated-object interactions. In particular, the proposed object’s metric scale and pose optimization (see subfigure (b)) recovers 3D mesh in world space from a normalized one, while MLLM-guided hand-object alignment method (see subfigure (c)) promotes physically plausible hand-object mesh composition*

1.  **数据预处理**  
    利用 SAM2 获取全帧掩码，Video‑Depth‑Anything/UniDepth 估计度量深度与相机内参；同时通过 DiffuEraser 修补人手区域，生成仅含物体的视频 $\\mathcal{V}' = \\{ \\mathbf{I}_i' \\}_{i=1}^{N}$，并提取物体掩码 $\\{M'_i\\}$ 与深度图 $\\{D'_i\\}$。

2.  **规范物体网格重建与 ASR 位姿/尺度优化**  
    从修补后的规范帧出发，使用 HunYuan3D 生成归一化的物体网格；随后通过**自适应采样细化（ASR）**（Algorithm 1）迭代搜索最优度量尺度和 6‑DoF 位姿，将归一化网格转换到世界坐标系。ASR 的核心机制是：先通过反投影深度点云估计粗尺度，再在自适应范围内随机采样尺度候选，每个候选经 FoundationPose 生成位姿假设，以渲染掩码与观测掩码的 IoU 作为反馈信号选择最优解，并动态扩大搜索范围以避免局部极值。

3.  **部件级运动重建**  
    对世界坐标系下的物体网格应用 PartField 进行部件分割；利用 CoTracker 获取 2D 点轨迹并提升至 3D，通过最小化跟踪损失 $\\mathcal{L}_{\\mathrm{track}}$ 与平滑约束 $\\mathcal{L}_{\\mathrm{smooth}}$ 优化各部件的逐帧 SE(3) 变换，从而恢复铰接运动。

4.  **MLLM 引导的手物对齐**  
    使用 WiLoR 重建 4D 手网格；通过 Qwen‑VL‑Max 进行三阶段结构化提示（视角检测→手型映射→逐帧接触推理）获取可靠的接触状态与接触手指；将接触信息作为约束，联合优化手物空间对齐。优化采用两阶段策略：先优化物体尺度，后联合优化手姿与全局变换，总损失为 $\\mathcal{L}_{\\mathrm{hoi}} = \\mathcal{L}_{\\mathrm{contact}} + \\mathcal{L}_{\\mathrm{reg}}$，其中 $\\mathcal{L}_{\\mathrm{contact}}$ 最小化指定指尖顶点到物体网格最近点的距离，$\\mathcal{L}_{\\mathrm{reg}}$ 结合加速度先验与手姿 L₁ 正则项防止优化偏离可信初始预测。

整个框架的输入是单目 RGB 视频，输出是时空对齐的手网格与铰接物体网格序列。各模块之间通过世界坐标系下的度量网格传递信息：ASR 解决了归一化网格到世界空间的尺度/位姿歧义，MLLM 引导的对齐则消除了手物网格之间的空间错位与穿透。



ArtHOI 将单目 4D 手‑铰接物体交互重建分解为四个串行模块，每个模块解决一个基础模型先验的固有缺陷：**数据预处理**提取干净观测信号；**规范网格重建与 ASR** 将归一化网格锚定到世界空间；**部件级运动重建**赋予静态网格时变铰接运动；**MLLM 引导的手物对齐**消除手物网格间的空间错位与穿透。

---

### 3.1 数据预处理

给定单目 RGB 视频 $\boldsymbol{\gamma} = \{ \mathbf{I}_i \}_{i=1}^{N}$，预处理流程并行完成三项任务：

1. **掩码与深度提取**：使用 **SAM2** 获取逐帧手物掩码；通过 **Video‑Depth‑Anything** 或 **UniDepth** 估计度量深度与相机内参。
2. **人手区域修补**：利用 **DiffuEraser** 对每帧中的人手区域进行视频级修补，得到仅包含物体的视频 $\mathcal{V}' = \{ \mathbf{I}_i' \}_{i=1}^{N}$。
3. **物体掩码与深度**：对修补视频再次应用 SAM2 和深度估计器，获得物体掩码 $\{M_i'\}$ 与深度图 $\{D_i'\}$。

这一步骤为后续模块提供了干净的物体观测信号，是 ASR 尺度搜索与部件跟踪的基础。

---

### 3.2 规范网格重建与 ASR 位姿/尺度优化

#### 规范网格生成

从修补视频中选取一帧“规范帧”（通常为物体充分可见且无遮挡的帧），使用 **HunYuan3D** 从该帧生成完整几何的**归一化网格**。该网格处于无量纲的规范空间，无法直接用于世界空间的交互重建。

#### 自适应采样细化（ASR）

ASR 的核心目标是恢复该归一化网格的**度量尺度** $s$ 与 **6‑DoF 位姿** $\mathbf{T}$，使其渲染掩码与观测掩码最大化一致。其工作流程如 Algorithm 1 所示：

1. **粗尺度初始化**：将物体深度点云反投影到 3D，与归一化网格的对应点云进行刚性对齐，估计初始尺度 $s_0$。
2. **自适应候选采样**：在尺度搜索区间 $[s_{\min}, s_{\max}]$ 内随机采样 $K$ 个尺度候选 $\{s_k\}$。搜索区间随迭代动态调整——若当前最优尺度靠近区间边界，则向外扩展以避免陷入局部极值。
3. **位姿假设生成**：对每个尺度候选 $s_k$，将归一化网格缩放后输入 **FoundationPose**，生成位姿假设 $\mathbf{T}_k$。
4. **IoU 反馈选择**：用 $\mathbf{T}_k$ 渲染掩码，计算与观测掩码 $M'$ 的 IoU。选择 IoU 最高的 $(\hat{s}, \hat{\mathbf{T}})$ 作为该轮最优解。
5. **迭代收敛**：重复步骤 2–4，直至 IoU 收敛或达到最大迭代次数。

ASR 的设计动机在于：FoundationPose 等 6‑DoF 估计器对尺度高度敏感，直接输入归一化网格会导致位姿预测崩溃。ASR 通过显式搜索尺度空间，将位姿估计器作为黑盒评分函数，从而解耦尺度与位姿的联合歧义。

---

### 3.3 部件级运动重建

获得世界空间中的规范网格后，使用 **PartField** 对其进行部件分割，得到 $K$ 个部件 $\{p_k\}$。随后利用 **CoTracker** 获取 2D 点轨迹并提升至 3D，通过优化各部件的逐帧 SE(3) 变换 $\{\mathbf{T}_i^{p_k}\}$ 来驱动铰接运动。

#### 跟踪损失

对于部件 $p_k$，设 $\mathbb{W}_{i,j}^k$ 为帧 $i$ 和帧 $j$ 中均可见的轨迹点集合，$\mathbf{z}_{i,q}^k$ 为轨迹点 $q$ 在帧 $i$ 中的 3D 坐标。跟踪损失强制同一空间点在两帧中通过部件变换保持一致：

$$
\mathcal{L}_{\mathrm{track}} = \sum_{j \in \mathbb{S}} \sum_{q \in \mathbb{W}_{i,j}^k} \left\| \mathbf{z}_{j,q}^k - (\mathbf{T}_i^{p_k})^{-1} \mathbf{T}_j^{p_k} \mathbf{z}_{i,q}^k \right\| \tag{1}
$$

其中 $\mathbb{S}$ 为与帧 $i$ 共享可见轨迹点的帧集合。

#### 平滑约束

对每个部件的变换序列施加二阶时间差分约束，抑制帧间抖动：

$$
\mathcal{L}_{\mathrm{smooth}} = \sum_{i=2}^{N-1} \left\| \Delta^2 \mathbf{T}_i^{p_k} \right\| \tag{2}
$$

#### 总体运动优化目标

$$
\mathcal{L}_{\mathrm{motion}} = \mathcal{L}_{\mathrm{track}} + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}} \tag{3}
$$

该优化在 SE(3) 流形上进行，输出各部件的逐帧刚体变换，从而实现规范网格到铰接运动序列的驱动。

---

### 3.4 MLLM 引导的手物对齐

手部网格由 **WiLoR** 独立重建，与物体网格在空间上存在系统性错位。ArtHOI 通过 MLLM 推理接触状态，将接触信息作为物理约束进行两阶段联合优化。

#### MLLM 接触推理

使用 **Qwen‑VL‑Max** 进行三阶段结构化提示（详见 Figure A‑E）：

- **Stage 1：视角检测**——判断视频为第一人称还是第三人称视角。
- **Stage 2：手型映射**——根据视角线索将可见手映射为左手/右手。
- **Stage 3：逐帧接触推理**——结合 RGB 帧与着色深度图，逐帧判断每只手是否与物体接触，并识别主要接触手指（拇指、食指、中指）。深度图验证步骤通过深度不连续性分析区分真实物理接触与视觉邻近。

#### 接触损失

设 $\mathbb{C}$ 为 MLLM 标记为接触的帧集合，$\mathbb{T}_i$ 为帧 $i$ 中接触手指的指尖顶点集合，$\mathcal{G}_i^o$ 为物体网格表面点集。接触损失最小化指尖到物体表面的最近距离：

$$
\mathcal{L}_{\mathrm{contact}} = \sum_{i \in \mathbb{C}} \sum_{\mathbf{v}_t \in \mathbb{T}_i} \min_{\mathbf{v}_o \in \mathcal{G}_i^o} \left\| \mathbf{v}_o - \mathbf{v}_t \right\|_2 \tag{4}
$$

#### 正则化损失

防止优化偏离可信初始预测，引入两项正则：

$$
\mathcal{L}_{\mathrm{reg}} = \lambda_{\mathrm{acc}} \left\| \Delta^2 \mathbf{T}^h \right\|_2 + \lambda_\theta \sum_{i=1}^N \left\| \theta_i^h - \theta_i^{h,\mathrm{init}} \right\|_1 \tag{5}
$$

其中 $\mathbf{T}^h$ 为手部全局变换序列，$\theta_i^h$ 为手部姿态参数，$\theta_i^{h,\mathrm{init}}$ 为 WiLoR 初始预测值。第一项为加速度平滑先验，第二项为姿态 L₁ 稀疏惩罚。

#### 两阶段联合优化

手物对齐的总损失为：

$$
\mathcal{L}_{\mathrm{hoi}} = \mathcal{L}_{\mathrm{contact}} + \mathcal{L}_{\mathrm{reg}} \tag{6}
$$

优化分两阶段进行：
1. **第一阶段**：固定手部姿态，仅优化物体全局尺度，消除手物尺度不一致。
2. **第二阶段**：联合优化手部全局变换 $\mathbf{T}^h$ 与姿态 $\theta^h$，在接触约束下将手部网格拉向物体表面。

该设计的关键在于：MLLM 提供的逐帧接触标签充当“软锚点”，仅在真实接触帧施加距离惩罚，避免了传统掩码交集方法在非接触帧产生误导性约束的问题。消融实验（Table 4）表明，移除 MLLM 引导的对齐优化会导致碰撞‑接触评分（Co²）急剧升高，验证了接触约束对消除穿透和错位的核心作用。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/011_Figure.jpg]]
*Figure: A. Demonstration of our MLLM contact reasoning pipeline. For clarity, we merge 2 neighbouring frames, but in practice, it’s typically set to 3. The top row shows RGB frames, the bottom row shows colorized depth maps. The MLLM analyzes visual and depth cues across frames to determine contact status and engaged fingers for each hand*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/014_Figure.jpg]]
*Figure: C. Stage 1: Perspective Detection Prompt. This prompt determines whether the input video is from a first-person or third-person viewpoint, which is essential for correctly identifying hand laterality in subsequent stages. Figure D. Stage 2: Hand Mapping Prompt. This stage identifies and maps visible hands to left/right labels. Stage 2a handles first-person perspective videos using spatial positioning and thumb direction cues. Stage 2b handles third-person perspective videos by analyzing camera angle relative to the operator’s body and arm connectivity patterns*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/015_Figure.jpg]]
*Figure: E. Stage 3: Frame-wise Contact Reasoning Prompt. This stage performs detailed analysis of each frame to determine contact state and identify engaged fingers. The critical depth map verification step (Phase C) distinguishes true physical contact from mere proximity using depth discontinuity analysis*



## 实验与关键发现

### 核心定量结果：4D 铰接物体重建精度

ArtHOI 在自采集的 **ArtHOI‑RGBD** 数据集上对所有五类物体均取得一致最优的重建精度。**Table 1** 显示，以 Chamfer Distance (CD) 为指标，ArtHOI 相比需要物体预扫描的 **RSRD** 方法在 Headphone 上降低 6.58 mm（8.12 vs. 14.71），在 Scissor 上降低 9.59 mm（4.26 vs. 13.84），在 Candy Box 上降低 3.66 mm（4.10 vs. 7.77）。值得注意的是，ArtHOI 仅以单目 RGB 视频为输入，而 RSRD 额外利用了环绕扫描获得的完整物体模板，这一不对称对比更凸显了 ArtHOI 从基础模型先验中恢复度量几何的能力。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/004_Table_1.jpg]]
*Table 1: 4D reconstruction accuracy of articulated object on monocular RGB videos from ArtHOI-RGBD dataset. Lower CD/MSSD and higher F-scores indicate better performance*

在公开的 **RSRD** 数据集上（**Table 2**），ArtHOI 在 Scissor 序列上的 CD 为 7.45 mm，远低于 RSRD 自身的 68.56 mm（降低 61.12 mm），在其他物体类别上也达到与预扫描方法可比甚至更优的水平。这一结果表明，ASR 的度量尺度恢复与 MLLM 引导的对齐优化在信息受限的条件下有效弥补了模板缺失带来的劣势。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/006_Table_2.jpg]]
*Table 2: 4D reconstruction accuracy of articulated object on monocular RGB videos from RSRD [24] dataset. Lower CD/MSSD and higher F-scores indicate better performance*

在 **ARCTIC** 子集上（**Table 3**），ArtHOI 重建 Mixer 物体的 CD 为 12.1 mm，而逐帧处理方法 **EasyHOI** 高达 226.0 mm，差距达 213.9 mm。EasyHOI 的失效源于其面向刚性物体的设计无法处理铰接运动，且缺乏时序一致性约束。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/007_Table_3.jpg]]
*Table 3: Comparison on a subset of ARCTIC [11]. ‘Cont.Acc’ denotes binary contact accuracy and ‘Fing.Acc’ denotes main contacting finger (thumb, index, middle) accuracy of MLLM reasoning results*

### 手物交互物理合理性验证

物理合理性通过碰撞‑接触评分 Co² 量化。**Table 4** 显示，经过 MLLM 引导的对齐优化后，ArtHOI 在 ArtHOI‑RGBD、RSRD 和 ArtHOI‑Wild 三个数据源上的 Co² 分数分别降至 **0.029**、**0.022** 和 **0.039**。相比之下，未对齐版本或仅依赖掩码交集的启发式方法 Co² 显著升高，表明手物网格之间存在严重穿透和空间错位。这验证了接触损失（Eq. 4）与两阶段联合优化对消除物理不合理性的关键作用。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/005_Table_4.jpg]]
*Table 4: Comparison of*

### 消融实验

#### ASR 位姿与尺度优化

**Table 5** 对比了规范网格位姿与尺度优化的不同方法。ASR 在 ArtHOI‑RGBD 上的平均渲染掩码 IoU 达到 **0.905**，RSRD 上为 0.876，ArtHOI‑Wild 上为 0.882，优化成功率 **100%**。相比之下，FoundationPose 和 Any6D 直接应用于归一化网格时，IoU 和成功率均大幅落后。ASR 的核心机制——在自适应范围内随机采样尺度候选并通过 IoU 反馈动态扩大搜索范围（Algorithm 1）——有效解决了度量尺度模糊问题，避免了局部极值陷阱。

在无真实深度的野外视频上，**Figure 4** 的定性对比进一步印证了这一优势：ASR 恢复了合理的物体尺度和位姿，而直接调用位姿估计器则出现明显的尺度错误和投影偏移。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison of metric scale and pose estimation on in-the-wild videos without ground-truth depth. Images are cropped and zoomed-in for better visualization*

#### MLLM 接触推理提示策略

**Table 6** 对 MLLM 提示策略进行了系统消融。同时引入时序上下文（Temp.）、视角提示（Persp.）、假阳性抑制（MinFP）和深度增强（Depth）四个组件时，接触推理准确率最高、假阳性率最低：在 RSRD 上准确率 88.58%、假阳性率 10.05%；在 ArtHOI‑Wild 上准确率 86.56%、假阳性率 10.61%。移除任一组件均导致性能下降，其中深度增强对抑制假阳性贡献尤为显著——这与 MLLM 提示流程中 Phase C 的深度不连续性验证设计一致（Figure A）。

**Table A** 进一步对比了 MLLM 推理与基于掩码交集的规则式方法。在受控的 RSRD 数据集上两者表现接近，但在野外视频上规则式方法显著退化，而 MLLM 保持鲁棒。这表明多模态语义推理对处理复杂背景和多样抓取姿态具有不可替代的优势。

#### 手物对齐优化

移除 MLLM 引导的手物对齐（即无尺度优化和时空联合优化）会导致手物网格出现严重空间漂移和尺度不一致，Co² 分数急剧升高（**Table 4** 中未对齐版本）。这证实了接触损失与正则化项（加速度先验和姿态 L₁ 稀疏惩罚，Eq. 5）在两阶段优化框架中的必要性。

### 失败模式与局限性

尽管 ArtHOI 在多数场景下表现优异，分析揭示以下边界情况：

1. **严重遮挡与快速运动**：当手物交互伴随极度遮挡或快速运动时，CoTracker 的 2D 轨迹可能出现断裂或漂移，导致部件运动优化中的跟踪损失（Eq. 1）失效，进而影响重建精度。当前框架缺乏针对轨迹异常值的显式检测与修复机制。

2. **非典型抓取姿态**：MLLM 接触推理在标准抓取（指尖接触）上准确率高，但面对双手协同操作或非手型操纵器时，结构化提示中的手型映射（Stage 2，Figure D）和接触手指识别（Stage 3，Figure E）可能产生歧义。ARCTIC 子集上的手指准确率数据（Table 3）暗示了这一泛化瓶颈。

3. **未见铰接类型**：PartField 的部件分割与运动重建假设物体由刚性部件通过铰接连接构成，对于复杂拓扑（如连续变形体、多自由度链式结构）的适应能力未经充分验证。

4. **运行效率**：当前框架整体运行时间约 1 小时，主要瓶颈在于 ASR 的迭代渲染与 MLLM 的逐帧推理，难以满足交互式应用需求。

以上边界情况的具体定量影响和针对性改进方案需进一步实验验证。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/009_Table_5.jpg]]
*Table 5: Comparison of canonical mesh pose and scale optimization. We compare with FoundationPose and Any6D [28]. Metrics include the IoU between rendered and ground-truth masks under the optimized pose, and the optimization success rate (SR%). A case is considered failed if subsequent part motion reconstruction or HOI alignment cannot proceed*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/010_Table_6.jpg]]
*Table 6: Ablation study on prompting strategies for MLLM contact reasoning, evaluated by accuracy and false positive rate (FP, %). “Temp.” incorporates temporal context from neighboring frames. “Persp.” indicates introducing camera-perspective cues; “MinFP” uses prompts designed to suppress false positives; and “Depth” augments image prompts with colorized depth. Results of ArtHOI-RGBD is excluded due to its near 100% accuracy*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2603_25791/figures/003_Figure_3.jpg]]
*Figure 3: This gallery showcases the results of our hand-articulated-object reconstruction on three data sources: ArtHOI-RGBD, RSRD and ArtHOI-Wild.(more results in the supp.). The first column shows sampled input frames. We present the camera view and a side view to display the reconstructed HOI meshes. Hand reconstructions for RSRD are produced using the same WiLoR model as ours for a fair comparison. Note that RSRD is unable to process the video from ArtHOI-Wild, as it requires an object surrounding scan that is unavailable for internet videos*



## 定位与知识库关联

### 与基线方法的关系

ArtHOI 处于单目视频 4D 手物交互重建这一新兴问题域，其核心贡献在于**不依赖任何物体模板或预扫描**，仅从单目 RGB 视频出发，通过“驯服”多个基础模型的先验来完成重建。这一设定与现有方法形成鲜明对比：

- **EasyHOI** 是为单帧图像设计的刚性物体 HOI 重建方法，逐帧独立处理，缺乏视频时序一致性建模。在铰接物体场景下，EasyHOI 无法恢复物体的度量尺度和位姿，且手物对齐在帧间不一致。在 ARCTIC 子集的 Mixer 物体上，EasyHOI 的 Chamfer Distance 高达 226.0 mm，而 ArtHOI 仅为 12.1 mm（Table 3），差距达 213.9 mm。这表明单帧刚性假设在铰接交互场景中完全失效。

- **RSRD** 是面向铰接物体 4D HOI 重建的代表性方法，但要求预先对物体进行环绕扫描以获得完整模板网格。ArtHOI 在输入信息显著更弱（无预扫描）的条件下，在 RSRD 数据集上取得与 RSRD 可比甚至更优的重建精度：在 Scissor 序列上，ArtHOI 的 CD 为 7.447 mm，而 RSRD 为 68.564 mm（Table 2）。在自采集的 ArtHOI‑RGBD 数据集上，ArtHOI 在所有五类物体上的 CD 均显著低于 RSRD（Table 1）。这证明 ArtHOI 的“基础模型先验 + 优化”策略有效弥补了模板信息的缺失。

- **FoundationPose** 和 **Any6D** 是通用的 6‑DoF 位姿估计器，但它们在归一化网格上直接预测位姿，无法解决度量尺度模糊问题。ASR 消融实验（Table 5）显示，ASR 在规范网格姿态与尺度优化任务上的平均 IoU 达到 0.905（ArtHOI‑RGBD），成功率 100%，远超 FoundationPose 和 Any6D。这验证了自适应采样细化策略对于尺度恢复的关键作用。

### 适用边界

ArtHOI 的适用边界由其流水线的三个核心模块共同决定：

1. **数据预处理依赖**：方法依赖 SAM2 获取掩码、Video‑Depth‑Anything/UniDepth 估计度量深度、DiffuEraser 修补人手区域。当深度估计质量下降（如透明物体、镜面反射）或人手修补产生严重伪影时，下游的 ASR 和部件运动重建将受到直接影响。

2. **规范网格重建质量**：HunYuan3D 从修补的规范帧生成归一化网格，其重建完整性决定了后续所有模块的上限。对于严重遮挡的物体，规范帧可能无法提供足够信息来恢复完整几何。

3. **部件分割与跟踪假设**：PartField 的部件分割和 CoTracker 的 2D 点跟踪均假设物体运动可分解为刚性部件的 SE(3) 变换。对于非刚性变形（如布料、软体）或极度严重的遮挡导致的跟踪失效，该假设不再成立。

4. **MLLM 接触推理**：Qwen‑VL‑Max 的三阶段接触推理在标准手型抓取上表现良好（RSRD 接触准确率 88.58%，Table 6），但消融实验也表明，移除时序上下文、视角提示、假阳性抑制或深度增强中任一组件都会导致准确率下降或假阳性率上升。在非典型抓取（如双手协同、非手型操纵器）或极端视角下，MLLM 的推理可靠性仍需进一步验证。

### 局限与开放问题

尽管 ArtHOI 在多个数据集上展示了领先性能，论文中尚未系统讨论以下局限，这些构成了重要的开放问题：

1. **重度遮挡与快速运动下的跟踪鲁棒性**：当手物交互产生严重相互遮挡或运动速度过快时，CoTracker 的 2D 轨迹可能断裂或漂移，导致部件运动优化的跟踪损失（Eq. 1）失效。目前框架缺乏针对跟踪失效的检测与恢复机制。

2. **MLLM 接触推理的泛化边界**：Table 6 的消融实验仅在 RSRD 和 ArtHOI‑Wild 上进行（ArtHOI‑RGBD 因准确率接近 100% 而被排除）。对于未见过的铰接物体类型（如门铰链、复杂工业零件）或非标准抓取姿态，MLLM 的接触推理能力是否仍然可靠，尚缺乏系统评估。

3. **未见物体类型的适应能力**：整个流水线中的 HunYuan3D、PartField、CoTracker 和 WiLoR 均为预训练模型，未针对特定物体类别微调。当面对与训练分布差异较大的铰接结构（如多轴铰链、球形关节）时，部件分割和运动优化的精度可能显著下降。

4. **运行时效率**：论文未明确报告端到端运行时间，但流水线涉及多个大型基础模型的推理和迭代优化，推测单段视频的处理时间在分钟到小时级别。这限制了 ArtHOI 在交互式应用（如 AR/VR 实时重建、机器人遥操作）中的直接部署。

5. **多手协同交互**：当前框架假设单手或双手独立与物体交互，MLLM 的接触推理也以单手为单位。对于双手协同操作同一物体（如双手拧开瓶盖）的场景，接触约束的建模和优化策略需要进一步扩展。

6. **深度估计的度量尺度一致性**：ASR 的粗尺度估计依赖反投影深度点云，其精度受限于 Video‑Depth‑Anything/UniDepth 的度量深度质量。在野外视频无真实深度条件下（Figure 4），尺度估计的定性对比虽优于基线，但缺乏定量评估。深度估计的尺度漂移如何影响最终重建精度，仍需系统分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/ArtHOI_Taming_Foundation_Models_for_Monocular_4D_Reconstruction_of_Hand_Articulated_Object_Interactions.pdf]]

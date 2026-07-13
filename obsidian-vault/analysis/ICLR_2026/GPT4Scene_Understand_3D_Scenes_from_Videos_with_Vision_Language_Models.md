---
title: "GPT4Scene: Understand 3D Scenes from Videos with Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GPT4Scene_Understand_3D_Scenes_from_Videos_with_Vision_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 0fib2BYc0L
aliases:
- GPT4Scene
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过重建3D点云生成鸟瞰图（BEV图像）作为全局场景表示，并在BEV图像和每个2D帧上通过空间-时间目标标记（STO-markers）维护一致的目标身份，从而显式建立全局-局部对应关系。"
primary_logic: "仅通过视觉提示（BEV+STO标记）而无需修改预训练VLM架构，就能激活其3D空间理解能力；通过在ScanAlign数据集上微调，模型可内化这种空间认知，即使在推理时不提供标记也能保持性能，表明该范式帮助VLM发展出对3D场景的内在理解。"
claims:
- "VLMs在3D理解上的主要短板是场景与帧之间缺少全局-局部对应（the lack of global-local correspondence between the scene and individual frames）。"
- "GPT4Scene构建BEV图像并在帧和BEV上标记一致的目标ID，从而建立全局-局部关系。"
- "在ScanAlign上微调Qwen2-VL-7B达到最先进的3D问答性能（SQA3D大幅提升）。"
- "ScanQA 上 CIDEr = 96.3"
---

# GPT4Scene: Understand 3D Scenes from Videos with Vision-Language Models

> [!tip] 核心洞察
> 仅通过视觉提示（BEV+STO标记）而无需修改预训练VLM架构，就能激活其3D空间理解能力；通过在ScanAlign数据集上微调，模型可内化这种空间认知，即使在推理时不提供标记也能保持性能，表明该范式帮助VLM发展出对3D场景的内在理解。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GPT4Scene：利用视觉语言模型从视频理解3D场景 |
| 英文题名 | GPT4Scene: Understand 3D Scenes from Videos with Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0fib2BYc0L) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GPT4Scene |
| Dataset | ScanQA, SQA3D, ScanRefer, Multi3DRef |

> [!tip] 效果简介
> - ScanQA 上，CIDEr 为 96.3，对比 87.7，变化 +8.6。
> - SQA3D 上，EM-1 为 60.6，对比 54.6，变化 +6.0。
> - ScanRefer 上，Acc@0.25 为 62.6，对比 55.5，变化 +7.1。

## 概要

### 问题瓶颈

预训练的2D视觉语言模型（VLMs）在理解3D场景时面临一个根本性短板：**缺乏整个场景与单个视频帧之间的全局-局部对应关系**。当VLM仅接收多帧2D图像作为输入时，各帧被独立处理，模型无法将局部观察与空间上下文对齐，导致难以建立对3D场景的整体认知。这一瓶颈本质上源于2D VLMs缺少将分散的帧级信息关联到统一空间坐标系的机制。

### 核心方法

GPT4Scene提出了一种**纯视觉提示范式**来解决上述瓶颈。其核心思路是：不修改预训练VLM的架构，而是通过构造特定的视觉输入格式，显式地为模型提供全局-局部对应关系。具体而言，该方法包含三个关键组件：

- **3D BEV鸟瞰图像**：从视频序列重建3D点云，并渲染俯视鸟瞰图，作为全局场景布局的视觉表示。
- **时空目标标记（STO-markers）**：在BEV图像和所有采样帧上叠加统一的目标ID标记，维护跨帧的目标身份一致性，建立时空对应。
- **ScanAlign数据集**：将现有3D标注统一转换为带有STO-markers的标记视频帧、BEV图像和文本描述的三元组，用于VLM微调。

通过这种视觉提示方式，模型能够在BEV图像的全局布局中定位目标，同时在2D帧中识别同一目标的局部外观，从而建立显式的全局-局部关联。

### 核心发现

GPT4Scene的核心洞察在于：**仅通过视觉提示（BEV+STO标记）就能激活预训练VLM的3D空间理解能力**。更关键的是，在ScanAlign数据集上微调后，模型能够**内化这种空间认知**——即使在推理时不提供BEV图像和STO-markers，模型仍能保持接近完整输入时的性能（ScanQA CIDEr 95.4 vs 96.3），表明该范式帮助VLM发展出了对3D场景的内在理解。

### 方法定位

GPT4Scene在方法谱系中占据独特位置：它不同于需要3D点云编码器的3D点云大语言模型（如Chat-scene），也不同于直接输入多帧视频的纯视觉方法（如LLaVA-3D）。GPT4Scene利用视觉提示在2D VLMs与3D空间理解之间架起桥梁，本质上是一种**零参数注入的视觉提示微调范式**，保持了VLM架构的完整性。

### 主要结果

在零样本设定下，GPT4Scene通过STO-markers提升了闭源VLMs（如GPT-4o）的3D问答性能。经过在ScanAlign上微调后，Qwen2-VL-7B在多个3D理解基准上达到最优性能：

- **3D问答**：ScanQA CIDEr 96.3（+8.6），SQA3D EM-1 60.6（+6.0）
- **3D视觉定位**：ScanRefer Acc@0.25 62.6（+7.1），Multi3DRef F1@0.25 64.5（+7.4）
- **3D稠密描述**：Scan2Cap CIDEr 86.3（+9.1）

消融实验证实了BEV图像和STO-markers的协同效应，以及GPT4Scene微调范式的关键作用。



3D场景理解是具身智能、增强现实和人机交互等领域的核心能力。传统方法通常依赖3D点云作为输入模态，结合专门设计的3D编码器来提取空间特征。然而，这类基于点云的方法面临两个根本性约束：其一，点云数据的获取成本高昂，需要专业扫描设备；其二，点云编码器与当前快速演进的大语言模型（LLM）生态耦合松散，难以共享基础模型的规模化红利。

近年来，视觉语言模型（VLMs）在2D图像和视频理解上展现了强大的泛化能力，一个自然的思路是将预训练VLM直接应用于3D场景理解——即输入场景的多视角视频帧，让模型从视觉信号中推断空间关系。这一范式绕过了点云编码器，具有更低的部署门槛和更好的模型生态兼容性。

**核心瓶颈：全局-局部对应关系的缺失**

然而，直接将视频帧输入VLM存在一个关键短板：**模型缺乏整个场景与单个视频帧之间的全局-局部对应关系**（the lack of global-local correspondence between the scene and individual frames）。具体而言，VLM在逐帧处理时，每个帧仅提供局部视角的观察，模型无法将不同帧中出现的同一物体关联起来，也无法将局部观察锚定到场景的整体空间布局中。这导致VLM在需要跨帧推理的3D任务（如“沙发左侧的桌子是什么颜色？”）上表现受限。

**现有方法的局限**

当前主流的3D场景理解方法可分为两类：

- **基于3D点云的方法**（如 **Chat-scene**，Huang et al., 2024a）：通过点云编码器显式建模3D几何，在空间推理上具有优势，但依赖点云输入和专用架构，难以受益于VLM的快速迭代。
- **基于视觉语言模型的方法**（如 **LLaVA-3D**，Zhu et al., 2025；**ROSS3D**，Wang et al., 2025a）：将多视角视频帧直接输入VLM，避免了点云依赖，但由于缺少全局场景表示和帧间目标对应，3D理解能力受到根本性制约。

**本文动机：用视觉提示弥合全局-局部鸿沟**

GPT4Scene的出发点是一个关键洞察：**仅通过视觉提示（visual prompting），而无需修改预训练VLM的架构，就能激活其3D空间理解能力**。具体而言，本文提出构建两类互补的视觉提示信号：

1. **全局场景表示**：通过从视频序列重建3D点云并渲染鸟瞰图（BEV图像），为VLM提供场景的整体布局信息。
2. **帧间目标对应**：在BEV图像和所有采样帧上叠加一致的空间-时间目标标记（STO-markers），显式维护跨帧的目标身份，建立局部观察与全局空间的对应关系。

这一范式的核心假设是：预训练VLM已经具备处理视觉信号和文本指令的基础能力，真正缺失的是将碎片化的局部观察组织为连贯空间认知的“脚手架”。通过BEV图像和STO标记提供这种脚手架，GPT4Scene旨在让VLM在不改变架构的前提下，发展出对3D场景的内在理解。



## 核心方法与创新机理

### 瓶颈诊断：全局-局部对应缺失

预训练的2D视觉语言模型（VLMs）在理解3D场景时，其根本短板并非视觉编码能力的不足，而是**缺乏整个场景与单个视频帧之间的全局-局部对应关系**。当VLM仅接收多帧2D图像序列时，模型无法将每帧中的局部观察与场景的整体空间上下文对齐——它看到的是一系列孤立的“快照”，而非一个连贯的3D空间。这一诊断构成了GPT4Scene方法设计的逻辑起点。

### 因果调控杠杆：BEV图像 + STO-markers

GPT4Scene的核心创新在于**仅通过视觉提示（visual prompting）而非修改预训练VLM架构，显式建立全局-局部对应关系**。具体而言，方法引入两个耦合的调控组件：

| 创新组件 | 基线做法 | GPT4Scene做法 | 功能角色 |
|---------|---------|--------------|---------|
| **全局场景表示** | 无（仅输入多帧2D图像） | 从视频重建3D点云，渲染**BEV鸟瞰图像**，提供全局布局 | 为VLM提供“上帝视角”的场景拓扑信息 |
| **帧间目标对应** | 无（各帧独立处理，目标身份断裂） | **STO-markers**：在BEV图像和所有采样帧上叠加统一的目标ID标记，实现时空一致性 | 将同一物体在不同视角下的观测“绑定”为同一实体 |

**BEV图像**通过公式 $\mathcal{T}_b = \mathcal{T} ( \mathcal{P}, E_{top} )$ 从重建点云渲染生成，为VLM提供了场景的全局俯视布局。**STO-markers**则通过公式 $\mathcal{V}^{*\prime} = \left\{ \mathcal{F} \left( I_i, \mathbf{\Phi} C_i^{uv} \right) \vert i = s_1, s_2, \dotsc, s_n \right\}$ 将3D实例分割结果投影到2D帧和BEV图像上，以统一颜色编码的标记框显式标注每个目标的身份和位置。这两个组件形成**协同效应**：BEV提供“where”，STO-markers提供“which”，共同解决了VLM在3D理解中的核心信息缺口。

### 核心洞察：微调内化空间认知

GPT4Scene最具启发性的发现是：**经过该范式微调的VLM能够将空间认知内化**。消融实验（Table 6）表明，使用GPT4Scene范式训练的Qwen2-VL-7B，即使在推理时**完全不提供BEV图像和STO-markers**，其在ScanQA上的CIDEr仍能达到95.4（完整范式下为96.3），仅轻微下降。这意味着STO-markers和BEV图像主要充当“训练时的脚手架”——它们在微调阶段教会VLM如何从多帧视频中推断3D空间关系，一旦模型学会这种能力，推理时便可摆脱对这些显式提示的依赖。

这一洞察的意义在于：**GPT4Scene并非简单地给VLM“打补丁”，而是通过精心设计的视觉提示格式，激活并培养了预训练VLM中潜藏的3D空间理解能力**。这解释了为何该范式在零样本设定下对大型VLM（如GPT-4o）有效，但对小型VLM（如Qwen2-VL-2B）提升有限甚至导致性能下降——小型模型缺乏足够的容量来从视觉提示中提取空间信号。

### 与先前方法的本质差异

相比于以**Chat-scene**（Huang et al., 2024a）为代表的3D点云大语言模型，GPT4Scene的根本差异在于**不依赖3D点云作为模型输入**——它仅使用视频帧和渲染的BEV图像，通过纯视觉通路实现3D理解。这使得方法可以无缝适配任何预训练VLM，无需修改模型架构或引入3D编码器。相比于**LLaVA-3D**（Zhu et al., 2025）等基于视觉语言模型的方法，GPT4Scene的关键区分点在于**显式构建并利用全局-局部对应**，而非简单地将多帧图像拼接输入。

### 局限性认知

当前STO-markers的生成依赖3D点云标注和实例分割，这限制了方法向无标注视频的扩展。此外，GPT4Scene对大物体的理解最有效，对小物体的理解较弱（Table 8），且BEV重建质量对性能影响微小（Table 7），表明BEV主要提供粗略的全局上下文而非精确几何信息。



![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_0fib2BYc0L/figures/002_Figure_2.jpg]]
*Figure 2: The framework of GPT4Scene. A scene video is processed by sampling frames, reconstructing a point cloud, and generating a BEV image. Object locations are detected from the point cloud and projected onto the video frames. The resulting frames and BEV image, enhanced with STO-markers, are inputs for Large Language Model (VLM) training and inference*

GPT4Scene 的核心设计思路是通过**视觉提示（visual prompting）**而非修改模型架构，来弥补预训练 2D VLM 在 3D 场景理解中的根本短板——缺乏整个场景与单个视频帧之间的**全局-局部对应关系**。整个框架（见 Figure 2）由四个串行模块构成，将原始场景视频转化为带有空间-时间目标标记的 BEV 图像与视频帧对，供 VLM 训练或零样本推理。

### 模块一：3D 重建（3D Reconstruction）

输入为从场景视频中采样的 $N$ 帧图像 $\{I_t\}_{t=1}^{N}$ 及其对应的相机外参 $\{E_t\}_{t=1}^{N}$。通过重建函数 $\mathcal{R}$ 生成场景的 3D 点云：

$$\mathcal{P} = \mathcal{R} \left( \{ ( I_t, E_t ) \}_{t=1}^{N} \right)$$

该点云是后续全局表示生成和目标标记投影的几何基础。

### 模块二：BEV 鸟瞰图渲染（BEV Rendering）

从重建点云 $\mathcal{P}$ 出发，使用顶视相机外参 $E_{top}$ 渲染鸟瞰图像 $\mathcal{T}_b$：

$$\mathcal{T}_b = \mathcal{T} ( \mathcal{P}, E_{top} )$$

BEV 图像提供场景的完整俯视布局，作为 VLM 理解全局空间结构的关键视觉锚点。消融实验（Table 7）证实，BEV 重建质量的差异对下游 QA 性能影响微小（ScanQA ROUGE 稳定在 45.8–47.0 之间），说明 BEV 的核心作用是提供全局上下文而非精确几何细节。

### 模块三：STO-marker 投影（STO-marker Projection）

这是建立**帧间目标一致性**的核心环节。从 3D 点云中检测到的实例分割结果中提取目标位置，分别投影到 2D 帧坐标 $C_i^{uv}$ 和 BEV 坐标 $C^{xy}$ 上，通过投影算子 $\mathcal{F}$ 在采样帧和 BEV 图像上叠加统一的目标 ID 标记 $\mathbf{\Phi}$：

$$\mathcal{V}^{*\prime} = \left\{ \mathcal{F} \left( I_i, \mathbf{\Phi} C_i^{uv} \right) \vert i = s_1, s_2, \dotsc, s_n \right\}, \quad \mathcal{T}_b^{\prime} = \mathcal{F} \left( \mathcal{T}_b, \mathbf{\Phi} C^{xy} \right)$$

由此，同一物体在 BEV 图像和各 2D 帧中携带一致的 ID 标记，显式建立了全局-局部对应关系。消融实验（Table 9）表明，同时移除 BEV 图像和 STO-markers 会导致所有关键指标大幅下降，二者具有明确的协同效应。

### 模块四：VLM 训练/推理

最终输入 VLM 的数据为一个三元组：带 STO-markers 的采样视频帧 $\mathcal{V}^{*\prime}$、带标记的 BEV 图像 $\mathcal{T}_b^{\prime}$，以及对应的文本描述。在训练阶段，模型在 ScanAlign 数据集（聚合 165K 条来自五个主流基准的文本-场景对）上进行监督微调；在零样本推理阶段，可直接将标记后的视觉输入送入闭源 VLM（如 GPT-4o），配合精心设计的提示词（见 Figure 6）完成 3D 问答、稠密描述和视觉定位等任务。

### 关键因果机制

框架的核心因果链路可概括为：**BEV 提供全局布局 → STO-markers 绑定时空一致的目标身份 → VLM 在微调中内化 3D 空间认知**。这一范式的决定性证据来自 Table 6 的消融：经过 GPT4Scene 范式微调的模型，即使在推理时不提供 BEV 图像和 STO-markers，仍能保持强大性能（ScanQA CIDEr 95.4 vs 完整输入下的 96.3），表明微调过程已帮助 VLM 发展出对 3D 场景的内在理解能力。



GPT4Scene框架通过四个顺序模块将纯视频输入转化为VLM可理解的视觉提示，其核心在于显式建立场景全局布局与局部帧观察之间的对应关系。

### 3D重建模块

给定一段包含 $N$ 帧的场景视频，每帧 $I_t$ 配有相机外参 $E_t$，首先通过重建函数 $\mathcal{R}$ 恢复场景的三维点云 $\mathcal{P}$：

$$\mathcal{P} = \mathcal{R} \left( \{ ( I_t, E_t ) \}_{t=1}^{N} \right)$$

其中 $\mathcal{P}$ 为重建得到的场景点云，$\mathcal{R}$ 为重建算子（可采用BundleFusion、SLAM3R等不同方法）。该模块的输出是后续全局表示和标记投影的几何基础。

### BEV渲染模块

从点云 $\mathcal{P}$ 出发，使用顶视相机外参 $E_{top}$ 通过渲染函数 $\mathcal{T}$ 生成鸟瞰图像 $\mathcal{T}_b$：

$$\mathcal{T}_b = \mathcal{T} ( \mathcal{P}, E_{top} )$$

$\mathcal{T}_b$ 提供场景的全局俯视布局，使VLM能够从整体上把握空间结构。消融实验表明，BEV重建质量的波动对下游问答性能影响微小（ScanQA ROUGE在45.8–47.0之间波动），印证了BEV的核心作用是提供全局上下文而非精确几何细节。

### STO标记投影模块

这是框架建立**全局-局部对应关系**的关键环节。在获得3D实例分割结果后，将目标ID标记统一投影到采样视频帧和BEV图像上：

$$\mathcal{V}^{*\prime} = \left\{ \mathcal{F} \left( I_i, \mathbf{\Phi} C_i^{uv} \right) \vert i = s_1, s_2, \dotsc, s_n \right\}, \quad \mathcal{T}_b^{\prime} = \mathcal{F} \left( \mathcal{T}_b, \mathbf{\Phi} C^{xy} \right)$$

其中 $\mathcal{F}(\cdot)$ 为STO标记投影算子，$C_i^{uv}$ 为第 $i$ 帧上各目标的2D像素坐标集合，$C^{xy}$ 为BEV图像上各目标的3D俯视坐标集合，$\mathbf{\Phi}$ 为统一的标记渲染函数。该模块确保同一目标在BEV图像和所有采样帧上携带一致的身份标记，从而将分散的2D观察锚定到全局空间参考系中。

### VLM训练/推理模块

将带标记的BEV图像 $\mathcal{T}_b^{\prime}$ 和采样帧集合 $\mathcal{V}^{*\prime}$ 与文本描述组合为三元组输入VLM。训练阶段在ScanAlign数据集（聚合165K文本-场景对）上进行监督微调；零样本推理时则直接向闭源VLM（如GPT-4o）提供带标记的视觉输入。

消融实验揭示了三个关键发现：(1) BEV图像与STO标记具有协同效应——同时移除两者导致所有关键指标大幅下降；(2) STO标记存在最优尺寸（size=40），过小或过大均导致性能衰减；(3) 经过GPT4Scene范式微调的模型即使在推理时不提供BEV和标记，仍能保持强劲性能（ScanQA CIDEr仅从96.3降至95.4），表明该范式帮助VLM内化了3D空间认知能力。



## 实验与关键发现

### 核心实验设置

GPT4Scene的实验验证围绕两个层次展开：**零样本推理**评估视觉提示的即时效果，**ScanAlign微调**评估范式内化后的能力。训练配置为每个视频采样$N=32$帧，分辨率512×490，使用8张A100 GPU训练约6小时，基础学习率$5\times10^{-6}$配合余弦退火，仅训练一个epoch。

### 零样本能力：大模型受益，小模型过载

Table 1展示了在不进行任何微调的情况下，仅通过BEV图像和STO-markers进行视觉提示的效果。核心发现是**模型规模决定了零样本增益的方向**：

- 大模型显著受益：Qwen2-VL-72B在ScanQA ROUGE上提升+3.0，SQA3D EM-1提升+2.5；GPT-4o的提升更为明显，ScanQA ROUGE提升+5.1，SQA3D EM-1提升+2.8。
- 小模型反而受损：Qwen2-VL-2B在ScanQA上仅微增+0.5，而在SQA3D上EM-1下降-0.7。这表明2B模型的视觉理解能力不足以同时处理BEV图像、多帧视频和STO-markers带来的信息负载，产生了**能力过载**现象。

这一结果揭示了GPT4Scene范式的适用边界：视觉提示有效的前提是基座VLM本身具备足够的视觉处理容量。

### 微调主结果：全面达到最优

在ScanAlign数据集（165K文本-场景对，涵盖五个主流基准）上微调后，GPT4Scene在3D场景理解的三个核心任务上均取得最优性能。

**3D问答（Table 3）**：Qwen2-VL-7B (GPT4Scene)在ScanQA上达到CIDEr 96.3，超越先前最优的Chat-scene（87.7）达+8.6；在SQA3D上EM-1达到60.6，相对Chat-scene（54.6）提升+6.0。更强的基座模型Qwen2.5-VL-7B (GPT4Scene)进一步将ScanQA CIDEr推至105.7。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_0fib2BYc0L/figures/005_Table_3.jpg]]
*Table 3: Evaluation of 3D question answer on ScanQA Azuma et al. (2022) & SQA3D Ma et al. (2023)*

**3D稠密描述（Table 4）**：Qwen2.5-VL-7B (GPT4Scene)在Scan2Cap上以BLEU-4 45.9（IoU@0.25）和ROUGE 67.9（IoU@0.25）刷新纪录，在IoU@0.5条件下CIDEr达到86.3，较Chat-scene的77.2提升+9.1。

**3D视觉定位（Table 5）**：Qwen2-VL-7B (GPT4Scene)在ScanRefer上Acc@0.25达到62.6，在Multi3DRef上all F1@0.25达到64.5，分别超越Chat-scene +7.1和+7.4。Qwen2.5-VL-7B (GPT4Scene)进一步将两项指标推至65.6和67.3。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_0fib2BYc0L/figures/007_Table_5.jpg]]
*Table 5: Evaluation of 3D visual grounding on ScanRefer Chen et al. (2020) and Multi3DRef Zhang et al. (2023c). Our method reaches state-of-the-art performance over all methods for the 3D visual grounding task*

值得注意的是，GPT4Scene在视觉定位任务上对**帧数和分辨率最为敏感**（Figure 4），这与定位任务需要精细空间对应关系的特性一致。

### 消融实验：微调是核心驱动力

Table 6揭示了GPT4Scene范式中各组件的贡献权重。最关键的发现是：**经过GPT4Scene范式微调的模型，即使在推理时完全不使用BEV图像和STO-markers，仅输入原始视频帧，仍能保持强大性能**——ScanQA CIDEr从96.3仅微降至95.4。这证明微调过程使VLM**内化了3D空间认知能力**，而非仅仅依赖推理时的视觉提示。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_0fib2BYc0L/figures/008_Table_6.jpg]]
*Table 6: Ablation study on the Efficacy of GPT4Scene. (1) on fully fine-tuned models with GPT4Scene; (2) on pure-video fine-tuned models; (3) in a zero-shot setting without training. Exp conducted on Qwen2-VL-7B*

相比之下，纯视频微调（无GPT4Scene范式）的模型性能显著低于GPT4Scene微调模型，且零样本设置下性能最差。三者的性能梯度清晰表明：GPT4Scene微调 > 纯视频微调 > 零样本。

**BEV重建质量影响微小**（Table 7）：使用BundleFusion、SLAM3R（不同帧间隔）、GS-SLAM、MAST3R-SLAM等不同重建方法，ScanQA ROUGE稳定在45.8-47.0之间，SQA3D EM-1在58.8-61.3之间波动。这验证了核心假设：**BEV的主要作用是提供全局场景上下文，而非精确的几何细节**。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_0fib2BYc0L/figures/009_Table_7.jpg]]
*Table 7: Ablation Study on BEV Reconstruction Quality. The quality of BEV reconstruction has a negligible impact on QA performance, since the BEV mainly offers a global overview of the scene*

**BEV与STO-markers的协同效应**（Table 9）：同时移除两者导致所有关键指标（METEOR、ROUGE、CIDEr）大幅下降，单独移除任一组件的下降幅度小于同时移除。STO-markers存在最优尺寸（size=40），过小（30）或过大（50）均导致性能下降。

**目标尺寸偏差**（Table 8）：模型对大物体的理解最有效，中等物体接近平均水平，小物体理解最弱。性能与目标尺寸呈正相关，这是当前范式的一个固有局限。

### 空间智能与2D能力保持

在VSIBench空间智能评估（Figure 3）中，GPT4Scene在ScanNet和ARKitScenes两个数据集上均一致超越基线，涵盖8项空间推理子任务，表明该范式确实增强了VLM的空间认知能力。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_0fib2BYc0L/figures/012_Figure_3.jpg]]
*Figure 3: Evaluation of GPT4Scene on the VSIBench. ’S’ denotes performance on ScanNet, while ’NS’ refers to the ARKitScenes dataset. The results indicate that GPT4Scene enhances spatial intelligence*

在2D多模态基准（Table 10-11）上，GPT4Scene微调后的模型在MMBench、MMStar、RealWorldQA和Video-MME上性能仅有微小下降（如MMBench-EN从82.4降至81.2），说明3D能力的内化并未以牺牲原有2D理解为代价。

### 失败模式与局限

1. **小目标理解薄弱**：Table 8直接量化了这一缺陷，模型对小物体的3D理解能力显著不足。
2. **小模型零样本退化**：Qwen2-VL-2B在零样本设置下SQA3D性能下降，表明范式对基座模型能力有最低门槛要求。
3. **精确空间推理未显著超越点云方法**：在需要精确空间关系推理的子任务上，GPT4Scene相对于原生3D点云LLM的优势不明显。
4. **STO-markers依赖3D标注**：当前标记生成需要3D实例分割标注，限制了向无标注视频的扩展。



## 定位与知识库关联

### 核心瓶颈与范式定位

预训练的2D视觉语言模型（VLMs）在理解3D场景时，根本短板并非视觉编码能力的不足，而是**缺乏整个场景与单个视频帧之间的全局-局部对应关系**（the lack of global-local correspondence between the scene and individual frames）。直接将多帧2D图像输入VLM，模型无法将局部观察与空间上下文对齐，导致其在3D问答、视觉定位等任务上表现受限。

GPT4Scene的解决方案属于**视觉提示（Visual Prompting）范式**——不修改预训练VLM的架构或参数结构，而是通过重构输入表示来激活模型的3D空间理解能力。具体而言，它引入两个互补的视觉提示组件：

1. **BEV鸟瞰图像**：通过3D重建生成全局场景布局表示，为VLM提供空间上下文。
2. **STO时空目标标记**：在BEV图像和所有采样2D帧上叠加一致的目标ID标记，显式建立帧间目标对应关系。

这两者具有**协同效应**——消融实验表明，同时移除BEV图像和STO标记会导致所有关键指标大幅下降（Table 9），而单独保留其一也无法维持完整性能。

### 与现有方法的对比关系

GPT4Scene在方法谱系中占据了一个独特位置，区别于以下三类工作：

- **3D点云大语言模型**：如 **Chat-scene**（Huang et al., 2024a），直接处理3D点云数据，需要专门的3D编码器。GPT4Scene仅依赖视觉输入（视频帧+BEV图像），无需3D骨干网络，在ScanQA上CIDEr达到96.3，显著超越Chat-scene的87.7（Table 3）。

- **基于视觉的语言模型方法**：如 **LLaVA-3D**（Zhu et al., 2025），同样使用2D VLM处理3D场景，但缺乏显式的全局-局部对应机制。GPT4Scene通过BEV+STO标记填补了这一空缺，在SQA3D上EM-1达到60.6，相对提升显著。

- **3D视觉定位专用方法**：如 **ROSS3D**（Wang et al., 2025a），针对特定任务设计。GPT4Scene作为通用框架，在ScanRefer上Acc@0.25达到62.6，超越专用方法7.1个百分点（Table 5）。

### 关键技术路径：从零样本到内化理解

GPT4Scene的能力演进呈现清晰的**两阶段路径**：

1. **零样本阶段**：在不训练VLM的情况下，仅通过BEV图像和STO标记作为视觉提示，即可提升闭源大模型（如GPT-4o）的3D理解性能（Table 1）。然而，这种提升在小型VLM上有限，Qwen2-VL-2B甚至出现性能下降，表明小模型可能因能力过载而无法有效利用额外视觉信息。

2. **微调内化阶段**：在ScanAlign数据集（165K文本-场景对，Table 2）上微调后，模型发展出对3D场景的**内在理解**。关键证据来自Table 6的消融实验：经过GPT4Scene范式训练的Qwen2-VL-7B，即使在推理时完全不提供BEV图像和STO标记（纯视频输入），ScanQA CIDEr仍达到95.4，仅比完整输入下的96.3下降不到1个点。这表明微调过程已使VLM内化了空间认知能力。

### 适用边界与局限

**有效场景**：
- 室内场景理解任务（ScanNet、ARKitScenes基准）
- 大物体理解最优，中等物体接近平均水平，小物体理解较弱（Table 8）
- 物体中心的任务类别（如Relational Refer、Existence & Counting）优势明显
- BEV重建质量对性能影响微小（Table 7，不同重建方法下ROUGE仅波动45.8-47.0），说明框架对重建精度具有鲁棒性

**局限与失效模式**：
1. **对3D标注的依赖**：STO标记的生成依赖3D点云实例分割标注，限制了向无标注视频的扩展。论文明确将此列为未来工作方向——从视频分割中端到端生成标记。
2. **小模型过载**：GPT4Scene范式在小型VLM（如Qwen2-VL-2B）上的零样本提升有限甚至为负，表明视觉提示的信息增量可能超出小模型的处理能力。
3. **精确空间推理的边界**：在需要精确空间关系推理的任务上，GPT4Scene相对于原生3D点云方法的优势不明显，BEV图像的全局上下文主要提供布局概览而非精确几何信息。

### 开放问题

1. **端到端标记生成**：如何从纯视频中直接生成STO标记，绕过3D点云重建这一中间表示？这将决定该范式能否扩展到更大规模、无标注的真实场景视频。

2. **内化机制的可解释性**：微调后模型在无标记情况下仍保持高性能，其内部表征究竟发生了何种变化？这种空间认知能否进一步蒸馏到更轻量的模型中？

3. **动态与室外扩展**：当前框架在静态室内场景上验证，如何扩展到包含动态物体的室外大规模场景（如自动驾驶、AR导航）仍是一个开放挑战。



## 原文 PDF

![[paperPDFs/ICLR_2026/GPT4Scene_Understand_3D_Scenes_from_Videos_with_Vision_Language_Models.pdf]]

---
title: "DetAny4D: Detect Anything 4D Temporally in a Streaming RGB Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DetAny4D_Detect_Anything_4D_Temporally_in_a_Streaming_RGB_Video.pdf
project_link: null
code_link: "https://github.com/open-mmlab/OpenPCDet"
aliases:
- DetAny4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 端到端的时空因果注意力编解码器，结合多任务训练策略和一致性损失，直接预测全局坐标下的3D边界框。
primary_logic: 将4D检测定义为端到端序列任务，利用因果掩码保持时间顺序，同时引入动态GT自适应和软损失以弥合单帧先验与全局标注的差异。
claims:
- DetAny4D融合多模态特征，设计了几何感知的时空解码器。
- 采用多任务学习架构与专用训练策略，维持不同长度序列的全局一致性。
- DetAny4D将跨帧方差降低了10%至30%。
- DA4D full 上 AP3D = 27.48
---

# DetAny4D: Detect Anything 4D Temporally in a Streaming RGB Video

> [!tip] 核心洞察
> 将4D检测定义为端到端序列任务，利用因果掩码保持时间顺序，同时引入动态GT自适应和软损失以弥合单帧先验与全局标注的差异。

| 字段 | 内容 |
|------|------|
| 中文题名 | DetAny4D：在流式RGB视频中实时检测任意4D对象 |
| 英文题名 | DetAny4D: Detect Anything 4D Temporally in a Streaming RGB Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18814) · [Code](https://github.com/open-mmlab/OpenPCDet) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | DetAny4D |
| Dataset | DA4D full, DA4D sub-datasets |

> [!tip] 效果简介
> - DA4D full 上，AP3D 27.48 vs DetAny3D (单帧) (N/A)；跨帧方差 (Var_v / Var_c) 0.70 / 0.64 vs 单帧检测器 (降低10-30%)。
> - DA4D sub-datasets 上，F1@IoU0.5 45.5 vs SpatialLM / ConceptGraphs (显著超越)。
> - DA4D sub-datasets (开放集) 上，AP3D 27.9 (Replica), 24.7 (MP3D), 27.2 (HM3D) vs 无公开对比 (与封闭集性能一致)。

## 概要

**问题瓶颈**：现有4D检测方法面临双重困境——一方面缺乏大规模高质量标注数据，另一方面多阶段流程（先逐帧3D检测，再跨帧关联）导致错误累积与时间不一致，难以端到端学习全局坐标下稳定一致的3D检测。

**核心思路**：DetAny4D将4D检测重新定义为端到端序列任务。其关键控制变量是**时空因果注意力编解码器**，配合多任务训练策略与一致性损失，直接从流式RGB序列预测全局坐标下的3D边界框。因果掩码保证时间顺序不泄露未来信息，动态GT自适应与软损失策略弥合单帧预训练先验与全局标注之间的差异。

**方法定位**：DetAny4D融合预训练基础模型（SAM、DINO）的多模态特征，设计了几何感知的时空解码器（含三个因果注意力块），联合预测深度、相机内参、相机位姿与3D边界框。相比单帧检测器（如**DetAny3D** (Zhang et al., arXiv 2025)、**Cube R-CNN** (Brazil et al., ICCV 2023)）和点云/多阶段方法（**SpatialLM**、**ConceptGraphs**），DetAny4D首次实现了端到端的开集4D检测。

**主要结果**：在DA4D全数据集上，DetAny4D达到27.48 AP3D，跨帧方差相比单帧检测器降低10%–30%（Var_v从0.95降至0.70）。在三个子数据集（Replica、MP3D、HM3D）上，F1@IoU0.5达到45.5，显著超越SpatialLM与ConceptGraphs。开集场景下性能与封闭集一致（Replica 27.9 AP3D），验证了方法的泛化能力。消融实验证实因果注意力模块是降低时间方差的核心因素，软损失策略改善了训练收敛鲁棒性。

三维目标检测是具身智能与场景理解的核心任务。现有3D检测器通常以单帧RGB图像为输入，逐帧独立预测相机坐标系下的3D边界框。当需要将这些预测变换到全局世界坐标系以支持下游任务（如导航、操作）时，单帧方法面临一个根本性瓶颈：**缺乏时间上下文导致跨帧预测不一致**。同一物体在不同视角下被重复检测，其位置、尺寸和朝向在全局坐标中产生显著抖动，严重损害时序稳定性。

为缓解这一问题，近期工作尝试将4D检测定义为多阶段流程：先逐帧进行3D检测，再通过后处理或关联模块建立跨帧对应关系。例如，**ConceptGraphs** 等基于RGB-D序列的方法将3D预测与跨帧关联分阶段处理。这种级联架构存在两个固有缺陷：其一，各阶段独立优化，误差在阶段间传播累积；其二，无法端到端地学习时空联合表示，全局一致性难以保证。

更深层的问题在于**数据与标注范式的缺失**。现有3D检测数据集（如SUN RGB-D、ScanNet）提供的是单帧视角下的静态标注，无法直接支撑4D时空检测的训练与评估。构建大规模、高质量的4D检测数据需要统一的数据生成流水线，将全局标注与序列观测对齐，同时处理遮挡、视野外目标等动态场景特有的挑战。

针对上述缺口，DetAny4D提出了三个核心动机：

1. **从多阶段到端到端**：将4D检测重新定义为端到端的序列预测任务，直接输出全局坐标系下时空一致的3D边界框，消除级联误差。
2. **从单帧到时空建模**：设计因果注意力机制，使模型能够利用时序上下文平滑预测，在保持单帧检测精度的同时大幅降低跨帧方差。
3. **从静态到动态数据**：构建大规模4D检测数据集DA4D，并提出动态真值自适应策略，弥合单帧预训练先验与全局序列标注之间的差异。

如图1所示，DetAny4D的范式与现有方法形成鲜明对比：单帧检测器（如**DetAny3D** (Zhang et al., arXiv 2025)、**Cube R-CNN** (Brazil et al., ICCV 2023)）逐帧预测导致全局不一致；多阶段4D方法流程复杂且易受误差传播影响；DetAny4D则通过端到端的时空解码器直接输出对齐的全局检测结果。实验表明，该方法在DA4D全数据集上达到27.48 AP3D，同时将跨帧方差降低10%至30%，验证了端到端时空建模在4D检测任务中的有效性。

## 核心方法与创新机理

DetAny4D 的核心创新在于将 4D 检测重新定义为**端到端序列任务**，通过因果注意力编解码器直接预测全局坐标下时空一致的 3D 边界框，从而消除多阶段流程中固有的错误累积与时间不一致问题。

### 从逐帧预测到序列化时空建模

现有 3D 检测器（如 **DetAny3D**（Zhang et al., arXiv 2025）、**Cube R-CNN**（Brazil et al., ICCV 2023））采用逐帧独立预测范式，当将各帧结果变换到世界坐标系时，缺乏跨帧约束导致严重的抖动和不一致（Figure 1）。而现有 4D 方法（如 **ConceptGraphs**）采用多阶段级联架构，先进行单帧 3D 检测，再通过后处理建立跨帧关联，流程复杂且易传播误差。

DetAny4D 的关键突破在于引入**时空因果注意力解码器**（Spatiotemporal Decoder），将时间建模直接嵌入模型核心。该解码器包含三个 Causal Attention Block（CAB），每个 CAB 对自注意力施加下三角因果掩码，确保当前帧可以感知历史信息但无法窥视未来帧。这一设计使模型能够以序列为单位进行端到端训练与推理，从根本上解决了跨帧一致性问题。消融实验表明，因果注意力模块使 AP3D 从 26.78 提升至 27.48，同时将跨帧方差 **Var_v 从 0.95 大幅降至 0.70**（Table 3），验证了序列化建模的核心价值。

### 动态 GT 自适应与软损失策略

4D 检测面临一个独特挑战：预训练单帧检测器的先验（物体朝向、尺寸标注习惯）与全局坐标系下的 4D 标注存在系统性偏差（Figure 11）。DetAny4D 通过两个关键设计弥合这一鸿沟：

1. **动态 GT 自适应**（Section 3.3）：根据序列中物体的累积可见性动态调整真值边界框。通过增量点云更新公式 $P_t(O) = P_{t-1}(O) \cup \pi^{-1}(M_t(O), D_O)$ 累积多视角观测，当物体被充分观察时，自适应 GT 收敛于全局标注（Figure 4）。这使模型能够从部分观测中学习到完整、一致的 3D 表达。

2. **软维度损失**（Soft Dimension Loss）：传统 $L_1$ 损失强制模型学习固定的宽/长对应关系，但预训练模型的宽度/长度轴可能与全局标注不一致。DetAny4D 引入软最小加权机制：
   $$L_{dim} = L_{h} + \sum_{k=1,2} w_k l_{wl}^{(k)}, \quad w_k = \frac{\exp(-l_{wl}^{(k)}/\tau)}{\sum_{m=1}^{2}\exp(-l_{wl}^{(m)}/\tau)}, \ \tau=0.1$$
   其中 $l_{wl}^{(1)}$ 和 $l_{wl}^{(2)}$ 分别对应恒等排列 $\Pi_1$ 和交换排列 $\Pi_2$ 下的宽度/长度损失。该设计允许模型在两种轴匹配方式间自适应选择，显著改善训练收敛（Table 3，Figure 6）。

### 多任务联合优化与一致性约束

DetAny4D 采用多任务学习架构，联合优化深度估计、相机内参、相机位姿和 3D 检测，总损失为：
$$L = L_{depth} + L_{cam} + L_{det} + L_{pose} + L_{cons}$$

其中一致性损失 $L_{cons}$ 是维持时空一致性的核心机制，包含两个互补分量：
- **空间一致性损失** $L_{spatial} = \sum_i \mathrm{chamfer}(B_w^i, B_w^{GT})$：将各帧预测变换到世界坐标后与真值比较，确保全局空间对齐；
- **时间一致性损失** $L_{temp} = \frac{1}{T} \sum_i^T \mathrm{chamfer}(B_w^i, \bar{B}_w)$：惩罚单帧预测与序列时间平均的偏差，抑制帧间抖动。

配合序列随机裁剪与对象填充策略（Figure 8），模型能够处理变长序列和新出现物体，在 DA4D 全数据集上达到 **27.48 AP3D**，跨帧方差相比单帧检测器降低 **10%–30%**（Table 1），同时在开放集场景下保持与封闭集一致的检测性能（Table 4）。

DetAny4D 将 4D 检测建模为端到端的序列预测任务，其核心 pipeline 由**特征提取器、几何上下文 Transformer、时空解码器、多任务预测头**以及配套的**序列级训练策略**构成（Figure 3）。输入为一段带有位姿的 RGB 序列与文本提示，输出为全局坐标系下时空一致的 3D 边界框。

### 输入与特征提取

系统接收连续 RGB 帧序列，每帧附带相机位姿与深度信息。特征提取阶段利用两类预训练基础模型并行编码：
- **语义/几何特征**：由 SAM 与 DINO 提取，生成图像嵌入 $E_{img}^t$ 与 token $T^t$；
- **几何嵌入**：深度相机模块输出深度、相机内参及位姿相关的嵌入 $E_{d,m,c}^t$。

这种多模态融合设计使模型同时具备开放集语义理解能力与 3D 几何感知能力。

### 几何上下文注入

提取的 3D 空间嵌入通过**几何上下文 Transformer**（Geometry Context Transformer）注入 Transformer 控制流。该模块将深度与相机参数编码为空间先验，引导后续注意力计算聚焦于几何合理的区域，而非单纯依赖 2D 图像特征。这一步是弥合 2D 观测与 3D 预测之间鸿沟的关键。

### 时空解码器

模型的核心创新在于**时空解码器**（Spatiotemporal Decoder），它由三个因果注意力块（Causal Attention Block, CAB）堆叠而成。每个 CAB 在自注意力计算中施加**因果掩码**（下三角矩阵），确保当前帧可感知历史信息，但对未来帧保持盲态。这一设计使得解码器能够以流式方式处理变长序列，同时建模跨帧的时间依赖关系，从根本上区别于逐帧独立预测的单帧检测器。

### 多任务预测头

解码器输出被送入多个并行的预测头，联合估计以下目标：
- 深度图
- 相机内参
- 相机位姿
- 3D 边界框（中心、尺寸、朝向）

多任务头设计使模型显式学习几何变换关系，增强了空间与时间一致性。

### 训练策略与损失

训练阶段采用专门的序列级策略：
- **序列随机裁剪与对象填充**：支持变长序列输入，并通过对象填充机制处理序列中出现或消失的物体，提升开放集能力（Figure 8）。
- **多损失联合优化**：总损失函数为：
  $$L = L_{depth} + L_{cam} + L_{det} + L_{pose} + L_{cons}$$
  其中 $L_{det}$ 包含中心、深度、2D/3D IoU、角点和维度损失；$L_{cons}$ 为时空一致性损失，由空间一致性 $L_{spatial}$（预测变换至世界坐标与真值比较）和时间一致性 $L_{temp}$（惩罚单帧预测与序列时间均值的偏差）组成。
- **软维度损失**：针对预训练模型预测与全局标注在宽度/长度轴上可能存在的歧义，采用软最小加权机制，通过置换矩阵交替匹配宽长维度，温度参数 $\tau=0.1$，使训练收敛更鲁棒。

### 数据预处理流水线

训练数据源自 Habitat 模拟器中随机游走采集的 RGB-D 序列（Figure 2）。序列被切分为固定长度且有重叠的片段，全局坐标下的物体边界框经可见性过滤后，通过增量点云累积进行自适应调整：
$$P_t(O) = P_{t-1}(O) \cup \pi^{-1}(M_t(O), D_O)$$
最终将序列坐标归一化至首帧参考系，形成适合端到端训练的 4D 标注。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_18814/figures/002_Figure_2.jpg]]
*Figure 2: The data processing pipeline for 4D detection task. We record posed RGB frames sequentially and separate the records into fixed-length sequences. Objects in global coordinates are projected into ego view and filtered with policies to delete occluded and outof-view objects. Objects b-boxes are then recalculated according to the visibility and accumulated considering the point cloud within the sequence. Finally, the coordinates of a sequence is adapted referring to the first frame*

DetAny4D 的核心架构由四个紧密耦合的模块构成：**特征提取器**、**几何上下文Transformer**、**时空解码器**与**多任务预测头**，整体流程见 Figure 3。其设计目标是将4D检测定义为一个端到端的序列任务，通过因果掩码保持时间顺序，同时以多任务训练策略和一致性损失弥合单帧先验与全局标注之间的差异。

### 特征提取器

特征提取器融合了预训练基础模型的多模态特征。RGB序列帧与用户提示（prompts）经编码后生成三类嵌入：图像嵌入 $E_{img}^t$、深度嵌入 $E_d^t$、以及相机相关嵌入 $E_{m,c}^t$。深度与相机内参的联合编码为后续几何推理提供了显式的3D空间线索。

### 几何上下文Transformer

该模块将3D空间嵌入以Transformer控制流的方式注入模型，使网络在早期阶段即具备几何感知能力。这一设计避免了将深度信息仅作为损失监督的间接用法，而是让空间结构直接参与特征交互。

### 时空解码器

时空解码器是DetAny4D的核心创新，由三个**因果注意力块（Causal Attention Block, CAB）**堆叠而成。每个CAB在自注意力计算时施加**因果掩码**（下三角矩阵），确保当前帧可以感知历史信息，但对未来帧保持盲态。这一机制使得模型能够以序列方式进行训练与推理，从根本上避免了传统逐帧检测器在全局坐标变换时产生的时间不一致性。

消融实验（Table 3）证实，因果注意力模块的引入使AP3D从26.78提升至27.48，同时将顶点方差 $Var_v$ 从0.95大幅降至0.70，验证了时序建模对检测精度与一致性的双重增益。

### 多任务头与训练策略

多任务头联合预测深度、相机内参、相机位姿与3D边界框，使模型具备几何与时间变换的感知能力。训练采用序列随机裁剪与对象填充策略（Figure 8），支持变长序列输入，并对消失或填充对象屏蔽损失计算，从而增强开放集场景下对新出现物体的处理能力。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_18814/figures/010_Figure_8.jpg]]
*Figure 8: Visualization of the sequence crop and object padding strategy. The object query list maintains the objects and padding status. As frames in the sequence forecast, object status updates. The disappeared objects and padded objects do not contribute to the loss*

### 关键公式

**增量点云更新**（Section 3.3）定义了物体点云随时间的累积过程：

$$P_t(O) = P_{t-1}(O) \cup \pi^{-1}(M_t(O), D_O)$$

其中 $P_t(O)$ 为物体 $O$ 在时刻 $t$ 的点云，$\pi^{-1}$ 表示利用深度 $D_O$ 将可见像素掩码 $M_t(O)$ 反向投影至3D空间。该公式为动态GT自适应提供了数学基础。

**检测损失**（Section 4.4）组合了多层次的监督信号：

$$L_{det} = L_{center} + L_{d} + L_{IoU}^{2D} + L_{IoU}^{3D} + L_{corner} + L_{dim}$$

其中 $L_{center}$ 为中心点损失，$L_{d}$ 为深度损失，$L_{IoU}^{2D}$ 与 $L_{IoU}^{3D}$ 分别为2D与3D IoU损失，$L_{corner}$ 为角点损失。

**软维度损失**是弥合单帧预训练模型与全局标注差异的关键设计。全局标注的边界框维度与旋转轴模式常与预训练3D检测模型的预测不一致（Figure 11），为此引入软最小加权机制：

$$L_{dim} = L_{h} + \sum_{k=1,2} w_k l_{wl}^{(k)}, \quad w_k = \frac{\exp(-l_{wl}^{(k)}/\tau)}{\sum_{m=1}^{2}\exp(-l_{wl}^{(m)}/\tau)}, \ \tau=0.1$$

其中 $L_h$ 为高度损失的L1范数，$l_{wl}^{(k)}$ 为宽度与长度在第 $k$ 种排列下的损失。通过置换矩阵 $\Pi_1 = [[1,0],[0,1]]$（恒等）与 $\Pi_2 = [[0,1],[1,0]]$（交换）对宽度和长度进行交替匹配，软最小权重 $w_k$ 自动选择损失较小的匹配方式。消融实验（Figure 6）表明，移除软损失后模型在维度与角度监督上出现明显退化。

**一致性损失**强制时空对齐：

$$L_{cons} = L_{spatial} + L_{temp}$$

空间一致性损失 $L_{spatial} = \sum_i \mathrm{chamfer}(B_w^i, B_w^{GT})$ 将各帧预测变换到世界坐标后与真值比较；时间一致性损失 $L_{temp} = \frac{1}{T} \sum_i^T \mathrm{chamfer}(B_w^i, \bar{B}_w)$ 惩罚单帧预测与序列时间平均 $\bar{B}_w$ 的偏差，从而抑制帧间抖动。

**总损失函数**联合优化所有任务目标：

$$L = L_{depth} + L_{cam} + L_{det} + L_{pose} + L_{cons}$$

其中 $L_{depth}$ 为深度估计损失，$L_{cam}$ 为相机内参损失，$L_{pose}$ 为相机位姿损失。多任务联合优化使各模块协同收敛，共同支撑端到端的全局一致4D检测。

## 实验与关键发现

### 主结果：4D检测性能与时间一致性

DetAny4D在DA4D全数据集上取得**27.48 AP3D**，同时将跨帧方差降至**Var_v 0.70、Var_c 0.64**，较单帧检测器降低10%–30%（Table 1）。这一结果验证了核心主张：端到端时空建模直接预测全局坐标下的3D边界框，能有效抑制逐帧预测导致的全局不一致。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_18814/figures/006_Table_1.jpg]]
*Table 1: 4D detection evaluations on the DA4D dataset, comapred with 3D detection methods and multi-stage 4D detection methods. Bold and underlined indicates the best and second-best results. Results on three sub-datasets and full DA4D are evaluated*

与多阶段4D检测方法相比，DetAny4D在DA4D子数据集上的**F1@IoU0.5达到45.5**，显著超越**SpatialLM**（依赖预扫描点云、仅预测轴对齐框）和**ConceptGraphs**（多阶段RGB-D推理，Table 2）。值得注意的是，ConceptGraphs*使用预测深度以确保公平比较，但其级联误差仍导致性能落后，凸显了端到端设计的优势。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_18814/figures/007_Table_2.jpg]]
*Table 2: 4D detection comparison with point-cloud-based and multi-stage method. SpatialLM employs pre-scanned point cloud and can only predict axis-aligned b-box, failing to perform well compared with GT. ConceptGraph* utilizes predicted depth for fairness (Section 5.1), which relies on RGB-D sequence and multistage inference*

在开放集设定下，DetAny4D在Replica、MP3D、HM3D三个子数据集上分别取得**27.9、24.7、27.2 AP3D**，与封闭集性能一致（Table 4），证明其开放集泛化能力。

### 消融实验：关键设计的因果作用

Table 3的消融实验揭示了各组件的因果贡献：

**因果注意力模块（Causal Attention）** 是时间一致性的关键瓶颈。消融该模块后，AP3D从27.48降至26.78，但更显著的是时间方差Var_v从0.70升至0.95。这证实了因果掩码（下三角矩阵）阻止未来帧信息泄漏，使模型学习到正确的时序依赖，而非简单的逐帧独立预测。

**软损失策略（Soft Loss）** 改善了训练收敛。预训练单帧检测模型（如DetAny3D）的预测轴与全局标注存在系统性偏差（Figure 11），直接使用硬损失会导致训练振荡。软损失通过软最小加权交替匹配宽度与长度维度，使模型在维度与角度监督上更鲁棒，消融该策略后性能明显下降。

**多任务头设计** 增加了几何与时间变换感知能力。消融多任务头后，模型无法联合优化深度、相机内参、相机位姿与3D边界框，导致空间一致性与时间一致性均受损（Figure 6）。

**对象填充策略** 使模型能处理序列中出现和消失的物体，增强开放集能力（Figure 8）。消融该策略后，模型对新出现物体的检测召回率下降。

### 失败模式与局限性

尽管DetAny4D在时间一致性上取得显著提升，仍存在以下局限：

1. **域差异**：DA4D数据集基于Habitat模拟器生成，与实际传感器数据（如RealSense、Kinect）存在域差异，真实场景下的泛化性需进一步验证。
2. **误差累积**：模型依赖深度估计与相机位姿模块，这些模块的预测误差会累积并影响最终检测精度，尤其在长序列推理时。
3. **室内偏置**：评估主要限于室内环境（Replica、MP3D、HM3D），室外动态场景（如自动驾驶）的泛化性尚不明确。
4. **开放集边界**：开放集能力依赖于预训练基础模型（SAM、DINO）的泛化性，对于与预训练分布差异极大的物体类别可能失效。

### 图表结论总结

- **Figure 5**：定性对比显示，DetAny4D预测的3D边界框在连续帧间保持时空对齐，而单帧检测器出现明显的跨帧抖动与不一致（红色圆圈标注）。
- **Figure 6**：消融可视化表明，移除多任务头导致预测框与真值偏差增大，移除软损失导致维度预测混乱，完整模型最接近真值。
- **Table 1**：全数据集结果证实DetAny4D在AP3D与时间方差两个维度上均优于单帧检测器与多阶段4D方法。
- **Table 3**：消融实验量化了因果注意力、软损失、多任务头各自对AP3D提升与方差降低的贡献。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_18814/figures/008_Table_3.jpg]]
*Table 3: Ablation study of DetAny4D. Impact of each design on the*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_18814/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison with other methods on 3D b-box predictions across consecutive frames in a sequence. Our proposed DetAny4D predicts spatiotemporally aligned 3D b-boxes, while red circles and rectangles show inaccurate and inter-frame jtter predictions*

## 定位与知识库关联

### 任务谱系：从单帧3D到序列4D

现有3D检测方法的主流范式是逐帧独立预测，再将结果变换到全局坐标系，这一过程缺乏跨帧时间一致性约束。**DetAny3D**（Zhang et al., arXiv 2025）作为单帧开集3D检测器，**Cube R-CNN**（Brazil et al., ICCV 2023）作为单帧统一3D检测器，以及**Uni-MODE**和**OVMono3D**等单帧方法，均属于这一范式。这些方法的共性问题在于：当相机运动导致观测视角变化时，独立预测的3D边界框在全局坐标下会产生显著的跨帧抖动（cross-frame jitter），这是本文所识别并解决的核心瓶颈。

在4D检测方向上，现有方法多采用多阶段流水线：先进行3D预测，再通过后处理建立跨帧关联。**ConceptGraphs**作为多阶段RGB-D方法，依赖RGB-D序列和多阶段推理；**SpatialLM**则基于预扫描点云，仅能预测轴对齐边界框。这些多阶段方法存在错误累积（error propagation）问题，且难以端到端学习全局一致的时空表示。

DetAny4D在谱系中的定位是：**首个端到端开放集4D检测框架**，将跨帧关系建模从后处理阶段前移至网络架构内部，通过因果注意力时空解码器直接预测全局坐标下的时间一致3D边界框。

### 关键设计差异

| 设计维度 | 单帧3D检测器 | 多阶段4D方法 | DetAny4D |
|---------|------------|------------|----------|
| 时间建模 | 无时间上下文 | 后处理关联 | 因果注意力时空解码器 |
| 训练目标 | 单帧检测损失 | 分阶段独立训练 | 多任务损失 + 时空一致性损失 |
| 数据标注 | 静态3D标注 | 静态3D标注 | 动态GT自适应与序列对齐 |
| 输入处理 | 单图输入 | 序列输入但不联合优化 | 序列裁剪 + 对象填充，支持变长 |

### 适用边界与局限

**适用边界**：
- 室内环境下的RGB视频流4D检测任务
- 具备相机位姿估计和深度估计模块的场景
- 需要开放集检测能力的应用（模型在Replica、MP3D、HM3D三个子数据集上开放集AP3D分别为27.9、24.7、27.2，与封闭集性能一致）

**已知局限**：
1. **域差异**：数据集基于Habitat模拟器生成，与实际传感器数据存在域差异，真实场景下的性能需进一步验证。
2. **误差累积**：模型依赖深度估计与相机位姿模块，这些模块的误差可能沿流水线累积并影响最终检测精度。
3. **场景泛化**：评估主要限于室内环境，室外动态场景的泛化性尚不明确。

### 开放问题

1. **数据扩展**：如何利用更多未标注视频数据（如大规模自监督预训练）进一步提升开放集能力？
2. **实时部署**：模型在具身智能真实硬件（如移动机器人）上的实时推理性能如何？当前架构的计算开销是否满足在线应用需求？
3. **多传感器融合**：能否将框架扩展到多相机流或与其他传感器（如LiDAR、IMU）融合，以增强几何感知精度？
4. **长序列稳定性**：因果注意力机制在超长序列下的时间一致性保持能力如何？是否存在漂移问题？

### 知识库贡献

DetAny4D的核心知识贡献包括：（1）将4D检测形式化为端到端序列任务，证明了因果掩码在保持时间顺序的同时可有效建模跨帧依赖；（2）提出动态GT自适应策略和软损失（soft loss）机制，弥合了单帧预训练模型先验与全局标注之间的分布差异；（3）通过消融实验验证了因果注意力模块使AP3D从26.78提升至27.48，同时将时间方差Var_v从0.95降至0.70，为后续序列化3D感知研究提供了明确的架构设计参考。

## 原文 PDF

![[paperPDFs/CVPR_2026/DetAny4D_Detect_Anything_4D_Temporally_in_a_Streaming_RGB_Video.pdf]]

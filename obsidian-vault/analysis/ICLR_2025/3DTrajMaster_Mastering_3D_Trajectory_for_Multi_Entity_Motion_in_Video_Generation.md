---
title: "3DTrajMaster: Mastering 3D Trajectory for Multi-Entity Motion in Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Generation.pdf
aliases:
- 3M3TMEMVG
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用6自由度（6DoF）姿态序列作为运动表示，并通过即插即用的3D运动基础对象注入器（含门控自注意力）建立每个实体与其3D轨迹的一一对应，从而在保留视频扩散先验的同时，使模型学会控制实体的3D运动。"
primary_logic: "为解决数据匮乏，构建了360°合成运动数据集，并引入视频域适应器（LoRA）和退火采样策略，有效缓解了合成数据带来的域偏移，在保证视频质量的同时实现了高精度的3D运动控制。"
claims:
- "3DTrajMaster 在所有实体测试中实现了 TransErr 0.398 m 和 RotErr 0.277 deg，相比最强的基线 Direct-a-Video（TransErr 1.420 m, RotErr 1.057 deg）误差大幅降低。"
- "移除视频域适应器后，FVD 由完整模型的 1546.15 急剧上升至 2379.89，视频质量严重退化至纯 UE 风格。"
- "省略退火采样策略同样导致视频质量下降（FVD 1841.64），而轨迹精度仅轻微变化，表明其对于平衡运动准确性与视觉质量不可或缺。"
- "Custom evaluation set (100 pairs: 12 single, 72 two, 16 three entity; only huma... 上 TransErr (m) / RotErr (deg) = 0.398 / 0.277"
---

# 3DTrajMaster: Mastering 3D Trajectory for Multi-Entity Motion in Video Generation

> [!tip] 核心洞察
> 为解决数据匮乏，构建了360°合成运动数据集，并引入视频域适应器（LoRA）和退火采样策略，有效缓解了合成数据带来的域偏移，在保证视频质量的同时实现了高精度的3D运动控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 3DTrajMaster：视频生成中基于6自由度轨迹的多实体运动控制 |
| 英文题名 | 3DTrajMaster: Mastering 3D Trajectory for Multi-Entity Motion in Video Generation |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.07759); [Project](http://fuxiao0719.github.io/projects/3dtrajmaster) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3DTrajMaster |
| Dataset | Custom evaluation set (100 pairs: 12 single, 72 two, 16 three entity; only human entities evaluated due to missing 4D animal pose estimator) |

> [!tip] 效果简介
> - Custom evaluation set (100 pairs: 12 single, 72 two, 16 three entity; only huma... 上，TransErr (m) / RotErr (deg) 为 0.398 / 0.277，对比 1.420 / 1.057 (Direct-a-Video, best baseline)，变化 -1.022 / -0.780。

## 概述

**问题**：现有可控视频生成方法依赖2D控制信号（点、框、2D轨迹），无法表达真实世界中物体运动的3D属性（旋转、遮挡、深度），导致多实体场景下难以实现精确的3D运动控制。

**核心方法**：3DTrajMaster 采用6自由度（6DoF）姿态序列作为运动表示，通过即插即用的门控自注意力对象注入器建立每个实体与其3D轨迹的一一对应关系。为缓解合成训练数据带来的域偏移，引入视频域适应器（LoRA）和退火采样策略，在保留视频扩散先验的同时实现高精度3D运动控制。

**主要结果**：在所有实体测试中，3DTrajMaster 实现了平移误差 0.398 m、旋转误差 0.277 deg，相比最强基线 Direct-a-Video（平移误差 1.420 m，旋转误差 1.057 deg）误差大幅降低（Table 2）。消融实验表明，移除域适应器导致 FVD 从 1546 急剧上升至 2380，省略退火采样同样使 FVD 升至 1842，验证了二者对视频质量的关键作用（Table 3）。用户调查显示，81.1% 的用户偏好 3DTrajMaster 优于 Tora（Table R12）。

**局限**：当前方法仅控制实体全局轨迹，缺乏对细粒度局部运动（如跳舞、手势）的直接控制能力；实体间交互（碰撞、交流）尚未建模；评估仅局限于人类实体（因缺少开放世界4D动物姿态估计器），且训练数据实体数量上限为3个。

## 背景与动机

### 问题背景

视频生成领域近年来取得了显著进展，文本到视频（T2V）模型已经能够生成视觉质量较高的视频内容。然而，当需要对视频中实体的运动进行精确控制时，现有方法面临根本性挑战：**真实世界中物体的运动本质上是三维的**，包含位置变化和朝向旋转，而当前的可控生成技术几乎完全依赖二维控制信号。

这种维度差异导致了一个核心瓶颈：2D控制信号（如屏幕空间中的点、边界框或2D轨迹）无法表达物体在三维空间中的旋转、遮挡关系和深度变化。在多实体场景中，这一问题更为突出——当多个物体在3D空间中交叉移动时，2D投影会产生歧义，使模型难以准确区分和跟踪各个实体的独立运动。

### 现有方法缺口

当前主流的可控视频生成方法在运动控制粒度上存在明显局限。如 Table 1 所示，现有方法的能力缺口体现在三个关键维度：

**运动表示的维度限制。** 以 **MotionCtrl**（Wang et al., 2024c）为代表的方法依赖2D点轨迹进行运动控制，完全无法处理实体的三维旋转信息。**Tora**（Zhang et al., 2024）同样基于2D轨迹，将多个实体的运动信息融合为单一2D特征，丧失了实体间的独立性。**Direct-a-Video**（Yang et al., 2024）采用训练无关的注意力编辑范式，通过操纵时空布局实现2D运动控制，但在多实体场景中效果显著下降——当实体轨迹在图像平面上交叉或重叠时，注意力机制难以维持正确的实体-运动对应关系。

**实体-轨迹对应的缺失。** 现有方法普遍未建立显式的实体与轨迹一一对应机制。它们要么将所有实体视为一个整体处理，要么通过单一特征通道传递所有运动信息。这导致在多实体场景中，模型容易混淆不同实体的运动指令，出现“张冠李戴”的错误——如 Figure 6 所示，Tora 在多实体场景中会将背景实体误认为目标人物实体。

**3D属性的不可控性。** 旋转、遮挡和深度排序是3D运动的基本属性，但2D控制范式天然无法表达这些信息。例如，当一个物体绕自身轴旋转时，其在2D投影中可能仅表现为轮廓的细微变化，2D轨迹无法捕获这种运动模式。同样，当一个实体从另一个实体后方经过时，2D控制信号无法传达遮挡关系的时序变化。

### 本文动机

针对上述缺口，本文的核心动机是：**将视频生成的运动控制从2D空间提升到3D空间**。具体而言，本文提出采用6自由度（6DoF）姿态序列作为运动表示——每个时刻的姿态由旋转矩阵（$\mathbf{R} \in \mathbb{R}^{3 \times 3}$）和平移向量（$\mathbf{T} \in \mathbb{R}^{3}$）组成，能够完整描述物体在三维空间中的位置和朝向变化。

这一选择面临两个关键挑战。第一，**如何将3D运动信息注入预训练的视频扩散模型而不破坏其生成先验**。视频扩散模型通常在大规模真实视频上训练，其内部表征与3D运动信号之间存在模态鸿沟。第二，**如何获取大规模、高质量的3D运动-视频配对数据**。真实视频数据集缺乏精确的3D轨迹标注，且存在严重的类别不平衡问题（如 Figure S10 所示，人类实体占比过高），无法支撑模型学习通用的3D运动控制能力。

为应对这些挑战，本文设计了三个互补的技术组件：一个即插即用的3D运动基础对象注入器，通过门控自注意力机制建立实体与轨迹的一一对应；一个基于合成数据的训练范式，利用Unreal Engine构建360°运动数据集；以及域适应器和退火采样策略，缓解合成数据带来的域偏移问题。这些设计共同构成了 **3DTrajMaster** 的核心技术路线。

## 核心创新

3DTrajMaster 的核心创新在于将可控视频生成的运动表示从二维平面提升至三维空间，并系统性地解决了由此带来的多实体对应、数据匮乏和域偏移三大挑战。其关键创新点可概括为以下三个层面：

### 1. 运动表示的维度跃迁：从 2D 到 6DoF

现有可控视频生成方法（如 **MotionCtrl** (Wang et al., 2024c)、**Tora** (Zhang et al., 2024)、**Direct-a-Video** (Yang et al., 2024)）普遍依赖 2D 控制信号——点、边界框或 2D 轨迹——来引导实体运动。这种二维表示无法表达真实世界中物体运动的核心属性：旋转、深度变化和遮挡关系。当多个实体在三维空间中交叉运动时，2D 控制信号会丧失深度信息，导致运动模糊或实体混淆。

3DTrajMaster 将运动表示替换为 **6 自由度（6DoF）姿态序列** $\mathbf{P}_n \in \mathbb{R}^{3 \times 4}$，包含旋转矩阵（$3 \times 3$）和平移向量（3 维），完整描述每个实体在三维空间中的位置和朝向。这一表示跃迁是后续所有创新的基础：它使模型能够理解并生成具有真实 3D 属性的运动，如实体绕轴旋转、前后遮挡和深度方向上的位移。

### 2. 实体-轨迹的一一对应：门控自注意力注入器

多实体场景下的核心难题在于建立“哪个轨迹控制哪个实体”的明确对应关系。基线方法或未解耦实体（将所有实体融合为单一特征），或通过交叉注意力间接关联，导致实体间的运动信号相互干扰——正如 Figure 6 所示，Tora 会将背景实体误认为目标人物。

3DTrajMaster 通过三个设计要素实现精确的实体-轨迹绑定：

- **实体级融合**：每个实体的文本描述和对应的 6DoF 姿态序列分别通过冻结的文本编码器和可学习的姿态编码器投影为潜在嵌入，然后以 **实体级相加** 的方式融合，形成绑定的实体-运动特征 $\mathbf{Z}^{\mathbf{Pe}}$。这种显式的一对一融合从架构层面杜绝了信号混淆。

- **门控自注意力注入器**：将融合后的实体-运动特征与视频令牌拼接，通过带可训练缩放因子 $\beta$ 的门控自注意力层有条件地更新视频令牌：
  $$\mathbf{x}_t = \mathbf{x}_t + \beta \cdot \mathbf{Tc}(\mathbf{Att}(\mathbf{q}, \mathbf{k}, \mathbf{v}))$$
  其中 $\mathbf{T} = \mathbf{x}_t \oplus \mathbf{Z}^{\mathbf{Pe}}$ 为拼接后的输入。$\beta$ 初始化为 0，使注入器在训练初期不干扰预训练先验，逐步学会控制运动。

- **即插即用设计**：注入器置于 2D 空间自注意力层之后，不修改基础 T2V 模型的原有参数，保留了视频扩散先验的生成能力。消融实验（Table 3）证实，将门控自注意力替换为交叉注意力或将注入器移至 3D 自注意力层后，视频质量和轨迹精度均轻微下降。

### 3. 合成数据与域适应：退火采样与 LoRA 域适应器

6DoF 轨迹控制需要精确的 3D 运动标注，而真实视频数据集无法提供。为此，3DTrajMaster 构建了 **360°-Motion 合成数据集**（54,000 个视频，来自 70 个 3D 资产，12 台环绕相机以 $384 \times 672$ 分辨率拍摄 100 帧），但合成数据引入了 UE 渲染风格与真实视频之间的域偏移。

模型通过**两阶段训练 + 退火推理**的组合策略解决这一问题：

- **视频域适应器（LoRA）**：在自注意力、交叉注意力和线性层中插入 LoRA 矩阵，训练时学习合成数据分布，使基础 T2V 模型适应 UE 风格。推理时通过降低 LoRA 缩放系数 $\alpha = 0.4$ 来抑制 UE 风格，保留真实感。消融实验（Table 3）表明，移除域适应器后 FVD 从 1546.15 急剧上升至 2379.89，视频质量严重退化至纯 UE 风格——这是模型中最关键的组件之一。

- **退火采样策略**：推理的前 $T_c = 25$ 步注入轨迹条件以确定整体运动，后续步骤仅依赖基础 T2V 先验生成视觉细节。这一策略在运动准确性与视频质量之间取得平衡：省略退火采样后 FVD 升至 1841.64，而旋转精度仅从 0.277° 轻微变化至 0.265°（Table 3），表明退火采样对视觉质量不可或缺。

### 创新总结

| 设计维度 | 基线方法 | 3DTrajMaster |
|---------|---------|-------------|
| 运动表示 | 2D 点/框/轨迹 | 6DoF 姿态序列 |
| 实体-轨迹对应 | 未解耦或单一特征 | 实体级相加 + 门控自注意力 |
| 运动注入架构 | 直接连接或交叉注意力 | 即插即用注入器（$\beta$ 门控） |
| 域适应 | 无（训练于真实视频） | LoRA 域适应器 + 退火采样 |

这些创新并非孤立存在，而是形成了因果链条：6DoF 表示使 3D 运动控制成为可能，但要求精确的实体-轨迹对应；合成数据解决了标注问题，却引入了域偏移；域适应器和退火采样则弥合了这一差距，最终在 TransErr 0.398 m、RotErr 0.277° 的精度（Table 2）下保持了可接受的视频质量。

## 整体框架

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/002_Figure_2.jpg]]
*Figure 2: 3DTrajMaster Framework. Given a text prompt consisting of N entities $\{ \mathbf { e } _ { n } \} _ { n = 1 } ^ { N }$ , 3DTrajMaster (a) is able to generate the desired video with entity motions that conform to the input entity-wise pose sequences $\langle \mathbf { \check { P } } _ { n } \rangle _ { n = 1 } ^ { N }$ . Specifically, it involves two training phases. First, it utilizes a domain adaptor to mitigate the negative impact of training videos. Then, an object injector module is inserted after the 2D spatial self-attention layer to integrate paired entity prompts and 3D trajectories. (b) Details of the object injection process. The entities are projected into latent embeddings through t...

3DTrajMaster 的整体框架围绕“以 6DoF 姿态序列为运动表示、以实体-轨迹一一对应为核心控制机制”展开，将多实体运动控制建模为一个条件视频生成问题。其任务形式化为：

$$f ( \cdot ) : \mathbf { c } \in \mathcal { Y } ^ { L } , ( \mathbf { e } _ { n } \in \mathcal { Y } ^ { L _ { n } } , \mathbf { P } _ { n } \in \mathbb { R } ^ { 3 \times 4 } ) _ { n = 1 } ^ { N } \to \mathbf { X } \in \mathbb { R } ^ { F \times H \times W }$$

其中 $\mathbf{c}$ 为场景级文本提示，$\mathbf{e}_n$ 和 $\mathbf{P}_n$ 分别为第 $n$ 个实体的描述与 6DoF 姿态序列，$\mathbf{X}$ 为生成的视频帧序列。

框架的核心设计逻辑是：**在冻结的基础 T2V 扩散先验之上，以即插即用的方式注入 3D 运动控制信号，同时通过域适应和退火采样策略抑制合成训练数据引入的域偏移**。具体而言，整个 pipeline 包含两条并行的编码通路和两阶段训练流程。

**输入编码与实体-轨迹绑定**。给定 $N$ 个实体-轨迹对，框架首先通过两条独立通路将其编码为潜在嵌入：实体描述 $\mathbf{e}_n$ 经冻结的底层 T2V 文本编码器投影为实体嵌入 $\mathbf{Z}_n^e$；对应的 6DoF 姿态序列 $\mathbf{P}_n$ 则通过可学习的姿态编码器 $E_P(\cdot)$（由线性层和时间维度下采样器组成）映射为轨迹嵌入 $\mathbf{Z}_n^P$。随后，配对的实体嵌入与轨迹嵌入通过**实体级相加**（entity-wise addition）融合为绑定的实体-运动对应特征 $\mathbf{Z}^{\mathbf{Pe}}$，从而显式建立每个实体与其 3D 轨迹的一一对应关系。这一设计是 3DTrajMaster 区别于 MotionCtrl（Wang et al., 2024c）、Tora（Zhang et al., 2024）等 2D 轨迹方法的关键——后者无法解耦多实体并关联各自的运动。

**门控自注意力注入器**。融合后的条件特征 $\mathbf{Z}^{\mathbf{Pe}}$ 并非直接替换视频令牌，而是与当前时间步的视频潜在表示 $\mathbf{x}_t$ 拼接，送入一个置于 2D 空间自注意力层之后的门控自注意力层：

$$\mathbf{q} = \mathbf{Q} \cdot \mathbf{T}, \quad \mathbf{k} = \mathbf{K} \cdot \mathbf{T}, \quad \mathbf{v} = \mathbf{V} \cdot \mathbf{T}, \quad \mathbf{T} = \mathbf{x}_t \oplus \mathbf{Z}^{\mathbf{Pe}}$$

注意力输出经截断操作 $\mathbf{Tc}(\cdot)$ 保留原始视频令牌部分后，以可训练的缩放因子 $\beta$ 通过残差连接更新 $\mathbf{x}_t$：

$$\mathbf{x}_t = \mathbf{x}_t + \beta \cdot \mathbf{Tc}(\mathbf{Att}(\mathbf{q}, \mathbf{k}, \mathbf{v}))$$

这种门控残差设计使模型能够有条件地融合运动信息，同时保持基础 T2V 先验不被破坏。

**两阶段训练与域适应**。为规避真实视频数据中 3D 运动标注匮乏的问题，3DTrajMaster 构建了 360° 合成运动数据集（360-Motion），但合成数据的 UE 渲染风格会引入域偏移。框架通过两阶段训练解决这一矛盾：

- **第一阶段**：训练对象注入器参数 $\boldsymbol{\theta}_1$（姿态编码器 + 门控自注意力），损失函数为标准去噪 MSE：

$$\mathcal{L}(\boldsymbol{\theta}_1) = \mathbb{E}_{\mathbf{x}, \mathbf{c}, \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \sigma_t^2 \mathbf{I}), \mathbf{e}, \mathbf{P}, t, \beta} \left[ \| \boldsymbol{\epsilon} - \hat{\boldsymbol{\epsilon}}_{\boldsymbol{\theta}_1}(\mathbf{x}_t, \mathbf{c}, (\mathbf{e}_n, \mathbf{P}_n)_{n=1}^N, t, \beta) \|_2^2 \right]$$

- **第二阶段**：冻结 $\boldsymbol{\theta}_1$，训练插入自注意力、交叉注意力和线性层的 LoRA 矩阵作为**视频域适应器** $\boldsymbol{\theta}_2$，使其学习合成数据的分布特征：

$$\mathcal{L}(\boldsymbol{\theta}_2) = \mathbb{E}_{\mathbf{x}, \mathbf{c}, \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \sigma_t^2 \mathbf{I}), t} \left[ \| \boldsymbol{\epsilon} - \hat{\boldsymbol{\epsilon}}_{\boldsymbol{\theta}_1}(\mathbf{x}_t, \mathbf{c}, t, \alpha) \|_2^2 \right]$$

推理时，通过降低 LoRA 缩放系数 $\alpha$（最优值为 0.4）来削弱 UE 风格，从而在保证视频质量的同时实现高精度 3D 运动控制。

**退火采样推理**。在推理阶段，3DTrajMaster 采用退火条件采样策略（Algorithm 1）：前 $T_c$ 步注入轨迹条件以确定实体的整体运动轨迹，后续步骤仅依赖基础 T2V 先验生成高质量视觉细节。这一策略有效平衡了运动控制精度与视频质量，是完整 pipeline 中不可或缺的推理环节。

## 核心模块与公式推导

### 3.1 问题形式化与扩散先验

3DTrajMaster 将多实体运动控制建模为一个条件生成映射：

$$f ( \cdot ) : \mathbf { c } \in \mathcal { Y } ^ { L } , ( \mathbf { e } _ { n } \in \mathcal { Y } ^ { L _ { n } } , \mathbf { P } _ { n } \in \mathbb { R } ^ { 3 \times 4 } ) _ { n = 1 } ^ { N } \to \mathbf { X } \in \mathbb { R } ^ { F \times H \times W }$$

其中 $\mathbf{c}$ 为全局文本提示，$\mathbf{e}_n$ 为第 $n$ 个实体的描述文本，$\mathbf{P}_n \in \mathbb{R}^{3 \times 4}$ 为该实体对应的 6DoF 姿态序列（包含 $3 \times 3$ 旋转矩阵与 3 维平移向量），$\mathbf{X}$ 为生成的视频帧序列。模型基于视频潜在扩散模型（Video LDM）构建，采用 Karras 预处理参数化去噪网络：

$$\hat { \mathbf { \epsilon } } _ { \theta } = c _ { \mathrm { o u t } } ( \sigma _ { t } ) \hat { F } _ { \theta } \left( c _ { \mathrm { i n } } ( \sigma _ { t } ) \mathbf { x } _ { t } ; c , \sigma _ { t } \right) + c _ { \mathrm { s k i p } } \left( \sigma _ { t } \right) \mathbf { x } _ { t }$$

该参数化形式为后续插入运动控制模块提供了稳定的扩散先验基础。

### 3.2 3D 运动基础对象注入器

对象注入器是方法的核心控制模块，负责建立实体与其 3D 轨迹之间的一一对应关系。其设计遵循三个关键步骤：

**实体-轨迹绑定编码。** 每个实体描述 $\mathbf{e}_n$ 通过冻结的底层 T2V 文本编码器投影为潜在嵌入 $\mathbf{Z}_n^e$；对应的 6DoF 姿态序列 $\mathbf{P}_n$ 则通过可学习的姿态编码器 $E_P(\cdot)$（由一个线性层和时序下采样器组成）映射为姿态嵌入 $\mathbf{Z}_n^P$。随后，两组嵌入通过实体级相加形成绑定的实体-运动对应特征：

$$\mathbf{Z}^{\mathbf{Pe}} = \bigoplus_{n=1}^{N} (\mathbf{Z}_n^e + \mathbf{Z}_n^P)$$

这种设计显式地将每个实体与其专属轨迹耦合，避免了 2D 基线方法中所有实体共享单一特征导致的对应模糊问题。

**门控自注意力融合。** 注入器被放置在 2D 空间自注意力层之后，以即插即用的方式融入 DiT 块。具体地，将视频令牌 $\mathbf{x}_t$ 与绑定特征 $\mathbf{Z}^{\mathbf{Pe}}$ 沿序列维度拼接，通过线性投影得到注意力输入：

$$\mathbf { q } = \mathbf { Q } \cdot \mathbf { T } , \quad \mathbf { k } = \mathbf { K } \cdot \mathbf { T } , \quad \mathbf { v } = \mathbf { V } \cdot \mathbf { T } , \quad \mathbf { T } = \mathbf { x } _ { t } \oplus \mathbf { Z } ^ { \mathbf { P e } }$$

自注意力计算后，通过可训练的比例因子 $\beta$ 将对应视频令牌部分的输出以残差方式加回：

$$\mathbf { x } _ { t } = \mathbf { x } _ { t } + \beta \cdot \mathbf { T c } ( \mathbf { A t t } ( \mathbf { q } , \mathbf { k } , \mathbf { v } ) )$$

其中 $\mathbf{Tc}(\cdot)$ 为截断操作，仅保留原始视频令牌对应的部分。$\beta$ 初始化为零，使注入器从恒等映射开始学习，从而保护预训练的视频扩散先验不被破坏。

**第一阶段训练损失。** 姿态编码器和门控自注意力参数 $\theta_1$ 通过标准 MSE 损失优化：

$$\mathcal { L } ( \pmb { \theta _ { 1 } } ) = \mathbb { E } _ { \mathbf { x } , \mathbf { c } , \mathbf { \epsilon } \sim \mathcal { N } ( \mathbf { 0 } , \sigma _ { t } ^ { 2 } \mathbf { I } ) , \mathbf { e } , \mathbf { P } , t , \beta } \left[ \| \epsilon - \hat { \epsilon } _ { \pmb { \theta } _ { 1 } } ( \mathbf { x } _ { t } , \mathbf { c } , ( \mathbf { e } _ { n } , \mathbf { P } _ { n } ) _ { n = 1 } ^ { N } , t , \beta ) \| _ { 2 } ^ { 2 } \right]$$

### 3.3 视频域适应器

由于训练数据为 UE 合成的 360-Motion 数据集，存在显著的域偏移问题。域适应器通过在基础 T2V 模型的自注意力、交叉注意力和线性层中插入 LoRA 矩阵实现，在第二阶段单独训练，此时冻结对象注入器参数 $\theta_1$：

$$\mathcal { L } ( \theta _ { 2 } ) = \mathbb { E } _ { \mathbf { x } , \mathbf { c } , \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \sigma _ { t } ^ { 2 } \mathbf { I } ) , t } \left[ \| \epsilon - \hat { \epsilon } _ { \boldsymbol { \theta } _ { 1 } } ( \mathbf { x } _ { t } , \mathbf { c } , t , \alpha ) \| _ { 2 } ^ { 2 } \right]$$

推理时通过降低 LoRA 缩放系数 $\alpha$（最优值 0.4）来抑制 UE 风格，使生成视频回归真实感。消融实验表明，移除域适应器会导致 FVD 从 1546.15 急剧恶化至 2379.89，视频质量退化至纯合成风格（Table 3）。

### 3.4 退火采样策略

推理阶段采用退火条件采样：前 $T_c$ 步注入轨迹条件以确定整体运动轨迹，后续步骤仅依赖基础 T2V 先验生成细节纹理。该策略通过调节条件注入的时长来平衡运动控制精度与视觉质量。消融显示，省略退火采样使 FVD 从 1546.15 升至 1841.64，而旋转误差仅从 0.277° 轻微变化至 0.265°，验证了该策略对视觉质量的关键作用（Table 3）。最优退火时间步 $T_c = 25$（Table R8）。

## 实验与分析

### 核心瓶颈与评估设计

现有可控视频生成方法（如 **MotionCtrl** (Wang et al., 2024c)、**Direct-a-Video** (Yang et al., 2024)、**Tora** (Zhang et al., 2024)）依赖2D控制信号，无法表达物体在三维空间中的旋转、遮挡和深度关系。为验证 3DTrajMaster 对6自由度（6DoF）运动的控制能力，本文构建了一个包含100组实体-轨迹对的评估集（12组单实体、72组双实体、16组三实体），以翻译误差 TransErr（米）和旋转误差 RotErr（度）作为核心指标。需注意，由于缺少开放的4D动物姿态估计器，量化评估仅针对人类实体。

### 主实验结果：3D轨迹控制精度

Table 2 展示了 3DTrajMaster 与各基线方法的定量对比。在所有实体测试中，3DTrajMaster 实现了 **TransErr 0.398 m** 和 **RotErr 0.277 deg**，相比最强基线 Direct-a-Video（TransErr 1.420 m, RotErr 1.057 deg），翻译误差降低约 72%，旋转误差降低约 74%。这一显著差距源于方法设计的根本差异：Direct-a-Video 等2D方法无法建模深度旋转，而 3DTrajMaster 通过6DoF姿态序列作为运动表示，并利用实体-轨迹一一对应的门控自注意力注入器，使模型学会控制实体在三维空间中的完整运动。

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/008_Table_2.jpg]]
*Table 2: Quantative Comparison on Single/Multiple Entity Motion. 3DTrajMaster performs better on multiple entity input since the single entity trajectory is more complex*

值得注意的是，3DTrajMaster 在多实体场景下的表现（TransErr 0.390 m, RotErr 0.272 deg）优于单实体场景（TransErr 0.456 m, RotErr 0.319 deg），这与直觉相反。论文解释为单实体轨迹通常更复杂，对控制精度提出了更高要求。

### 组件消融：域适应器与退火采样的关键作用

Table 3 的消融实验揭示了两个创新组件对视频质量的决定性影响：

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/009_Table_3.jpg]]
*Table 3: Ablation Study on Full Testest and Base T2V Videos (As Reference Video)*

- **移除视频域适应器**：FVD 从完整模型的 1546.15 急剧上升至 2379.89，FID 从 96.75 恶化至 157.51，视频质量严重退化至纯 UE 渲染风格。这表明 LoRA 域适应器在抑制合成数据域偏移方面不可替代——它使模型在训练时学习合成数据分布，推理时通过降低缩放系数 α 来削弱 UE 风格，从而保留基础 T2V 模型的视觉质量。

- **省略退火采样策略**：FVD 上升至 1841.64，视频质量同样受损，但轨迹精度仅轻微变化（RotErr 从 0.277 变为 0.265）。这说明退火采样（前 Tc 步注入轨迹条件，后续步骤依赖基础 T2V 先验）主要负责平衡运动准确性与视觉质量，而非直接提升轨迹控制精度。

### 融合设计与注入位置的影响

消融实验还考察了运动融合方式与注入器位置的影响：

- **用交叉注意力替换门控自注意力**（以实体-运动绑定特征 Z^Pe 作为 query）：视频质量和轨迹精度均轻微下降。门控自注意力通过可训练缩放因子 β 的残差连接，提供了更稳定的运动融合机制。
- **将对象注入器置于3D自注意力之后**：同样导致质量和精度轻微退化，验证了在2D空间自注意力之后插入注入器的设计选择。

### 超参数敏感性分析

Tables R8-R10 进一步分析了关键超参数的影响：

- **退火时间步 Tc=25** 被选为最佳值，在质量和轨迹准确度之间取得折衷。
- **LoRA 缩放系数 α=0.4** 被选为最佳组合，过高的 α 会引入 UE 风格伪影，过低则域适应效果不足。
- 训练步数 TS 的消融表明，36,000 步的对象注入器训练已能充分收敛。

补充实验（Table R11）显示，使用静态运动作为负姿态条件可略微提升轨迹准确度，但会降低视频质量（FVD 从 1976 升至 2141），说明负样本策略存在质量-精度权衡。

### 用户偏好调查

Table R12 的用户调查结果进一步验证了 3DTrajMaster 的感知优势：与 Tora 相比，81.1% 的用户偏好 3DTrajMaster；与 Direct-a-Video 和 MotionCtrl 相比，偏好率分别为 56.6% 和 47.2%。这一结果与定量指标一致，表明 6DoF 运动控制在视觉感知层面同样优于 2D 控制方法。

### 失败模式与评估局限

尽管主实验结果显著，以下局限性需要在解读时注意：

1. **评估仅限人类实体**：由于缺少开放的4D动物姿态估计器，非人类实体的3D轨迹控制缺乏客观量化验证，Table 2 的结果无法推广到动物、车辆等类别。
2. **实体数量上限为3**：训练和评估均基于合成数据，最多包含3个实体，更复杂的多实体场景性能未知。
3. **合成-真实域差距**：尽管域适应器有效缓解了 UE 风格，模型在处理高度逼真的现实世界视频时可能仍存在域偏移。
4. **缺乏局部运动控制**：当前方法仅控制全局轨迹（位置和朝向），无法处理细粒度局部运动（如跳舞、挥手）和实体间交互（如碰撞、交流），这是后续研究的重要方向。

### 补充图表

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/013_Figure.jpg]]
*Figure: Pexelsand Pixabay Figure S1O: Entity Distribution Over 60 Classes in Artgrid, Pixabay,and Pexels*

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/015_Table.jpg]]
*Table: R8: Ablation Study on Annealed Timestep T _ { c }*

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/003_Figure_3.jpg]]
*Figure 3: Dataset Construction Illustration. We correlate (a) collected 3D assets with (b) GPT- generated 3D trajectories on (c) diverse 3D UE platforms, positioning(d) 12 evenly distributed surrounding cameras to capture the object motions in video format*

![[assets/figures/papers/paper_list_l27_3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Ge/figures/004_Table_1.jpg]]
*Table 1: Fine Control Comparison with Multi-Entity Input*

## 方法谱系与知识库定位

### 1. 问题定位：从2D控制到3D运动建模

现有的可控视频生成方法主要依赖2D控制信号（如关键点、边界框、2D轨迹），其核心瓶颈在于无法表达真实世界中物体运动的完整3D属性——**旋转、遮挡、深度变化**。这一缺陷在多实体场景下被急剧放大：（1）2D信号无法区分实体间的深度关系；（2）多实体运动缺乏一一对应的绑定机制，导致实体身份混淆或运动耦合。

3DTrajMaster 将这一瓶颈的“因果旋钮”锁定在**运动表示**和**实体-轨迹对应**两个维度上。通过采用6自由度（6DoF）姿态序列（包含旋转矩阵 $R \in \mathbb{R}^{3 \times 3}$ 和平移向量 $T \in \mathbb{R}^{3}$）替代2D点/框/轨迹，模型获得了描述3D运动的完整自由度；同时，通过实体级相加（entity-wise addition）显式建立每个实体与其轨迹的一一对应，解耦了多实体场景中的运动绑定问题。

### 2. 与现有方法的关系

**Table 1** 从位置控制、方向控制、实体-轨迹对应和学习范式四个维度对方法进行了细粒度对比，揭示了3DTrajMaster在控制维度上的系统性提升：

| 维度 | MotionCtrl | Direct-a-Video | Tora | 3DTrajMaster |
|------|-----------|----------------|------|-------------|
| 位置控制 | ✓（2D点轨迹） | ✓（2D边界框） | ✓（2D轨迹） | ✓（3D平移） |
| 方向控制 | ✗ | ✗ | ✗ | ✓（3D旋转） |
| 实体-轨迹对应 | ✗ | ✗ | ✗ | ✓（实体级绑定） |
| 是否学习 | ✓（训练） | ✗（训练无关） | ✓（训练） | ✓（训练） |

具体而言：

- **MotionCtrl**（Wang et al., 2024c）通过2D点轨迹控制运动，但无法处理多实体对应——所有实体的运动信息被混合编码，缺乏个体化绑定。当场景中存在多个实体时，模型难以区分哪个轨迹属于哪个实体。

- **Direct-a-Video**（Yang et al., 2024）采用训练无关范式，通过注意力机制编辑时空布局实现2D运动控制。其优势在于无需额外训练，但在多实体场景中效果显著下降：Table 2显示其多实体 TransErr 为1.391 m、RotErr 为0.942 deg，远高于3DTrajMaster的0.390 m和0.272 deg。原因在于注意力编辑缺乏对3D旋转和深度的建模能力，且实体间的注意力干扰随实体数量增加而加剧。

- **Tora**（Zhang et al., 2024）将多个实体的2D轨迹融合为单一2D特征，无法关联个体运动。Figure 6的定性对比显示，Tora在多实体场景中会将背景实体错误地关联到前景人物，暴露出实体-轨迹对应缺失的根本缺陷。

3DTrajMaster 相对于这些方法的本质差异不在于“更强的模型”，而在于**运动表示的维度提升**（从2D到6DoF）和**实体-运动绑定的架构设计**（门控自注意力注入器 + 实体级相加）。这两项设计使得模型能够为每个实体独立编码其3D轨迹，并通过可训练的缩放因子 $\beta$ 精确控制运动注入的强度。

### 3. 适用边界与局限

尽管3DTrajMaster在3D轨迹控制上取得了显著进展，其适用边界受以下因素制约：

**（1）运动控制的粒度限制。** 当前方法主要控制实体的全局轨迹（位置和朝向），缺乏对细粒度局部运动（如人体舞蹈动作、手势、物体形变）的直接控制能力。6DoF姿态序列描述的是刚体的整体运动，无法表达非刚体形变或关节运动。这限制了模型在需要精细动作控制的场景（如人物交互、运动竞技）中的应用。

**（2）实体数量的上限。** 由于合成数据集360-Motion的构建限制，训练和评估中的实体数量上限为3个。Table 2显示模型在单实体（TransErr 0.456 m）和多实体（0.390 m）场景下均有良好表现，但无法保证在超过3个实体的复杂场景中保持同等精度。这一问题源于合成数据生成的可扩展性瓶颈——每增加一个实体，轨迹组合和渲染的复杂度呈指数增长。

**（3）实体交互的缺失。** 实体之间的互动（如碰撞、交流、避让）尚未被建模。当前框架将每个实体视为独立运动体，其轨迹仅由输入条件决定，缺乏实体间的物理约束或行为耦合。这意味着生成的视频中实体行为相对独立，无法产生真实的交互场景（如两人握手、车辆避让行人）。

**（4）评估的实体类型局限。** 由于缺少开放的4D动物姿态估计器，评估仅局限于人类实体。对于非人类实体（动物、车辆、机器人等）的3D轨迹控制缺乏客观量化验证。虽然Figure 4展示了多样化的实体类别生成能力，但其轨迹精度的量化评估仍需依赖未来4D姿态估计工具的发展。

**（5）合成数据与现实世界的域差距。** 模型在360-Motion合成数据集上训练，尽管引入了LoRA域适应器和退火采样策略来缓解域偏移，但在处理高度逼真的现实世界视频时可能仍存在分布不匹配。Table 3的消融实验表明，移除域适应器后FVD从1546.15急剧上升至2379.89，视频质量严重退化至纯UE风格——这反向证明了域适应器的必要性，但也暗示合成数据与现实视频之间的鸿沟尚未完全弥合。

### 4. 域适应策略的有效性与代价

3DTrajMaster的域适应策略由两个互补组件构成：

- **视频域适应器（LoRA）：** 在训练阶段，LoRA模块学习合成数据的分布特征（UE渲染风格、光照、纹理）；在推理阶段，通过降低LoRA缩放系数 $\alpha$（最优值0.4，见Table R9）来抑制UE风格，使生成结果更接近基础T2V模型的真实视频先验。Table 3显示，完整模型（$\alpha=0.4$）的FVD为1546.15，而移除域适应器（$\alpha=1.0$）后FVD飙升至2379.89，FID从96.75升至157.51，视频质量严重退化。

- **退火采样策略：** 在推理的前 $T_c$ 步（最优值25，见Table R8）注入轨迹条件以确定整体运动，后续步骤仅依赖基础T2V先验生成视觉细节。Table 3显示，省略退火采样导致FVD从1546.15升至1841.64，而旋转准确度仅轻微变化（RotErr从0.277降至0.265），表明该策略的核心价值在于**平衡运动准确性与视觉质量**，而非单纯提升轨迹精度。

这两个组件之间存在微妙的相互作用：域适应器负责缩小合成数据与真实视频的分布差异，退火采样则在推理时动态调节条件强度。Table R8和R9的超参数消融表明，$\alpha=0.4$ 和 $T_c=25$ 是当前设定下的最优折衷，但这些参数是否能在不同场景（如不同实体类型、不同背景复杂度）下自动调整，仍是一个开放问题。

### 5. 开放问题

基于上述局限，以下问题值得后续研究关注：

1. **细粒度运动与交互建模：** 如何扩展模型以控制局部运动（如人体关节点运动、物体形变）并支持实体间的物理交互？这可能需要引入更丰富的运动表示（如SMPL参数、物理仿真约束）并设计相应的条件注入机制。

2. **多实体扩展：** 能否通过改进的训练范式或数据生成方法，使模型能够生成超过3个实体且保持高质量的视频？可能的路径包括：基于组合泛化的训练策略、利用大规模弱标注真实视频的预训练、或引入实体数量的课程学习。

3. **真实视频训练的桥接：** 如何将当前仅限于合成数据的训练扩展到利用大规模真实视频？关键在于获取或推断真实视频中的3D轨迹监督信号——这可能需要借助单目3D重建、多视角几何或自监督学习技术。

4. **自适应条件调度：** 退火采样和域适应器之间的相互作用是否可以通过更自适应的方式动态调整？例如，根据当前去噪步的预测不确定性或实体运动的复杂度，自动调节条件注入强度，以在不同场景下自动平衡质量和控制精度。

## 原文 PDF

![[paperPDFs/ICLR_2025/3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Generation.pdf]]

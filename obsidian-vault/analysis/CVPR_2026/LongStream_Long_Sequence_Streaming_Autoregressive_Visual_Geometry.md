---
title: "LongStream: Long-Sequence Streaming Autoregressive Visual Geometry"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LongStream_Long_Sequence_Streaming_Autoregressive_Visual_Geometry.pdf
project_link: "https://3dagentworld.github.io/longstream/"
code_link: null
aliases:
- LongStream
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 解除全局坐标系锚定并采用关键帧相对姿态估计（SE(3)规范解耦）；通过正交尺度学习（Sim(3)解耦）将几何与尺度松绑；配合缓存一致性训练和周期性缓存刷新消除训练-推理不一致与长时记忆饱和。
primary_logic: 将长程外推问题重新表述为局部相对姿态估计任务，并通过正交尺度学习实现几何与尺度的完全解耦，从而消除对第一帧锚点的依赖；缓存一致性训练强制模型在纯滑动窗口下运作，消除注意力沉没，配合周期缓存刷新对抗长时记忆饱和，首次实现公里级序列的稳定在线重建。
claims:
- 引入相对姿态头和正交尺度学习可将ATE从8.043降至2.645；再结合缓存一致性训练（CCT）降至0.984；最终加入周期缓存刷新降至0.115。
- 在KITTI数据集上，LongStream平均ATE 51.90，而最佳流式基线STream3R为177.73，StreamVGGT为226.15。
- 在vKITTI上，LongStream平均ATE 1.610，StreamVGGT为83.916。
- 缓存一致性训练消除注意力沉没，使模型在全窗口和滑动窗口推理下均保持稳定且最优的精度。
---

# LongStream: Long-Sequence Streaming Autoregressive Visual Geometry

> [!tip] 核心洞察
> 将长程外推问题重新表述为局部相对姿态估计任务，并通过正交尺度学习实现几何与尺度的完全解耦，从而消除对第一帧锚点的依赖；缓存一致性训练强制模型在纯滑动窗口下运作，消除注意力沉没，配合周期缓存刷新对抗长时记忆饱和，首次实现公里级序列的稳定在线重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | LongStream: 长序列流式自回归视觉几何 |
| 英文题名 | LongStream: Long-Sequence Streaming Autoregressive Visual Geometry |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.13172) · [Project](https://3dagentworld.github.io/longstream/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LongStream |
| Dataset | KITTI, vKITTI, TUM-RGBD, Waymo |

> [!tip] 效果简介
> - KITTI 上，ATE (平均，共11个序列) 51.90 vs 226.15 (StreamVGGT) (大幅领先)。
> - vKITTI 上，ATE (5个场景平均) 1.610 vs 83.916 (StreamVGGT) (提升近52倍)。
> - TUM-RGBD 上，ATE 0.076 vs 0.627 (StreamVGGT) (降低一个数量级)。

## 概要

### 问题瓶颈

现有流式3D重建模型（如 **Stream3R**、**StreamVGGT**）普遍采用“规范耦合”设计：将第一帧固定为全局坐标系锚点，后续所有帧的位姿均回归到该绝对参考系下。这一范式在短序列上可行，但在长序列下暴露出三个根本性缺陷：

1. **尺度漂移与外推崩溃**：随着序列延伸，远离第一帧的帧需要模型外推到训练分布之外的位姿空间，导致绝对轨迹误差（ATE）非线性增长，数十米内即告崩溃。
2. **注意力沉没（Attention Sink）**：Transformer架构在因果推理中过度关注初始帧Token，形成注意力分布的严重偏斜，削弱了对近期帧的建模能力。
3. **KV缓存污染**：长序列推理时，陈旧的历史缓存特征持续占据注意力预算，造成“几何饱和”，进一步加剧时间退化。

### 核心方案

**LongStream** 通过三个关键设计从根本上解决上述瓶颈：

- **SE(3)规范解耦**：放弃第一帧锚点，改为预测当前帧相对于最近关键帧的局部相对位姿 $\mathbf{T}_{ik} = \mathbf{T}_i \circ \mathbf{T}_k^{-1}$。这将长程外推重新表述为恒定难度的局部任务，使模型不再受序列长度影响。
- **Sim(3)正交尺度学习**：将几何重建与全局尺度估计完全解耦——几何分支在尺度归一化空间优化，专用尺度头独立预测对数尺度 $\boldsymbol{s} = \exp(\mathbf{w}^\top \mathbf{h}_{\mathrm{scale}})$，仅用有度量真值的数据训练。
- **缓存一致性训练（CCT）与周期缓存刷新**：训练中传递并裁剪KV缓存以对齐推理时的滑动窗口，强制模型在纯窗口模式下运作，消除注意力沉没；同时每N个关键帧重置陈旧缓存，对抗长时记忆饱和。

### 方法定位

LongStream 属于**流式自回归视觉几何**框架，在统一的时空Transformer内联合预测位姿、深度、点云和尺度。与离线方法（如 **VGGT**、**FastVGGT**）不同，LongStream 严格遵循在线设定——不可见未来帧，内存与延迟保持恒定（18 FPS），而非随序列长度线性增长直至OOM。与现有流式方法相比，其核心区分点在于规范解耦的位姿参数化和训练-推理一致的KV缓存机制。

### 主要结果

- 在 **KITTI** 数据集上，LongStream 平均 ATE 为 **51.90**，而最佳流式基线 Stream3R 为 177.73，StreamVGGT 为 226.15（Table 1）。
- 在 **vKITTI** 上，LongStream 平均 ATE 为 **1.610**，较 StreamVGGT 的 83.916 提升近52倍（Table 3）。
- 在 **TUM-RGBD** 和 **Waymo** 上，ATE 分别降至 0.076 和 0.737，较 StreamVGGT 降低一个数量级以上（Table 2）。
- 消融实验证实：依次启用相对位姿头、尺度头、CCT 和缓存刷新，ATE 从 8.043 逐步降至 2.645 → 0.984 → **0.115**，每一模块均带来显著增益（Table 5）。
- 长序列测试中，LongStream 的 ATE 随帧数增加保持稳定（如 KITTI 801 帧仅 3.81），而其他流式方法误差非线性增长（Table 6）。

### 局限与展望

当前方法假设场景基本静止，对动态目标处理能力有限；关键帧调度依赖手工设定的固定间隔（N=10），未学习自适应策略；未集成回环闭合优化，在长距离回环时仍存在轻微漂移。未来方向包括动态场景建模、自适应关键帧选择、轻量在线回环检测，以及超长序列下的点云精度提升。

从单目或双目视频流中在线恢复公制尺度的三维几何与相机位姿，是自动驾驶、机器人导航和混合现实等应用的核心能力。传统方法依赖基于优化的SLAM系统（如ORB-SLAM系列），通过局部BA和回环检测维持全局一致性，但在纹理稀疏、运动剧烈或长距离场景中鲁棒性有限。近年来，基于学习的3D重建模型展现出更强的数据驱动先验，但其主流范式仍以离线处理为主：将完整序列一次性输入模型，通过双向注意力融合全局上下文，推理时内存和延迟随序列长度线性或超线性增长，无法满足流式在线需求。

为实现在线处理，近期工作**Stream3R**和**StreamVGGT**将离线模型改造为自回归流式架构：逐帧输入，通过Transformer的KV缓存机制保留历史信息，预测当前帧的绝对位姿和几何。然而，这些流式模型在实际长序列中迅速崩溃，轨迹误差在数十米内即不可接受（见Figure 1）。经本文分析，其根本瓶颈在于**规范耦合（gauge coupling）**设计——固定第一帧为全局坐标锚点，要求模型预测当前帧相对于遥远起点的绝对位姿。这导致三个连锁问题：

1. **外推难度递增**：随着序列推进，当前帧与锚点的时空距离不断增大，模型需在注意力衰退的条件下进行越来越远的外推，误差呈非线性累积。
2. **尺度漂移**：尺度估计与几何预测隐式耦合在同一表示中，全局尺度的微小偏差会通过绝对位姿链逐帧放大，导致重建整体缩放失真。
3. **注意力沉没与KV缓存污染**：标准分块训练与流式推理之间存在“训练-推理不一致”——训练时模型可见完整上下文的双向注意力，推理时却受限于因果掩码和固定缓存窗口。这诱发注意力沉没（attention sink）现象，即模型过度关注早期帧的陈旧token，同时KV缓存中过时信息不断累积，污染当前帧的时空融合。

上述问题共同构成**长序列流式重建的核心挑战**：如何在严格在线、不可见未来帧的约束下，维持公里级序列的稳定公制精度？现有流式方法因规范耦合设计而无法突破这一瓶颈，离线模型虽精度更高但无法实时运行（如VGGT在长序列上内存溢出，见Figure 2），基于优化的SLAM系统虽可在线但依赖回环检测且缺乏数据驱动的几何先验。

本文的动机即在于：**解除规范耦合，将长程外推重新表述为局部相对估计任务**，从而从根本上消除对第一帧锚点的依赖，使每步推理难度恒定。同时，通过正交尺度学习实现几何与尺度的完全解耦，并引入缓存一致性训练对齐训练与推理行为，最终实现公里级序列的稳定在线重建。

## 核心方法与创新机理

LongStream 的核心创新在于对现有流式自回归几何模型的三项结构性改造，将长程外推从累积漂移问题重新表述为恒定难度的局部估计任务。

### 1. 规范解耦：从绝对世界锚点到关键帧相对位姿

现有流式模型（如 **STream3R**、**StreamVGGT**）采用“规范耦合”设计——固定第一帧为全局坐标系锚点，所有后续帧的位姿均相对于该锚点回归。这种设计的根本缺陷在于：随着序列增长，当前帧与第一帧的时空距离不断增加，注意力机制对遥远历史帧的响应自然衰退，导致尺度漂移和外推误差在数十米内即引发轨迹崩溃。

LongStream 通过**SE(3)规范解耦**彻底消除了这一瓶颈。模型不再预测绝对位姿，转而预测当前帧相对于最近关键帧的相对位姿：

$$\mathbf{T}_{ik} = \mathbf{T}_i \circ \mathbf{T}_k^{-1}$$

其中 $\mathbf{T}_i$ 为帧 $i$ 的绝对位姿，$\mathbf{T}_k$ 为关键帧 $k$ 的绝对位姿。这一变换严格满足 SE(3) 规范不变性，使得外推任务从“预测相对于遥远第一帧的位姿”转变为“预测相对于邻近关键帧的位姿”，难度不再随序列长度增长。关键帧的切换由固定间隔 $N$ 控制，每次切换后参考系更新，模型仅需处理局部相对运动。

### 2. 正交尺度学习：几何与尺度的 Sim(3) 解耦

尺度估计是公制重建的核心挑战。传统方法将尺度与几何隐式耦合，导致尺度误差通过几何分支反向传播并放大漂移。LongStream 提出**正交尺度学习**，实现几何与尺度的完全解耦：

- **几何分支**：在尺度归一化空间内优化。预测点云 $\hat{X}_{\text{raw}}$ 与真值点云分别进行尺度归一化后计算 L1 损失：

$$\tilde{X}_{\text{pred}} = \frac{\hat{X}_{\text{raw}}}{\text{Norm}(\hat{X}_{\text{raw}})}, \quad \mathcal{L}_{\text{geom}} = \|\tilde{X}_{\text{pred}} - \tilde{X}_{\text{gt}}\|_1$$

这确保几何优化完全独立于全局尺度，消除尺度误差对几何的干扰。

- **专用尺度头**：接收独立的 Scale Token，在对数空间预测全局尺度因子：

$$\boldsymbol{s} = \exp(\mathbf{w}^\top \mathbf{h}_{\mathrm{scale}})$$

尺度损失在对数空间计算 L1 误差 $\mathcal{L}_{\text{scale}} = \|\log \hat{s} - \log s_{\mathrm{gt}}\|_1$，且仅对有度量真值的数据施加。这种正交设计使几何学习与尺度学习互不干扰，实验表明在 vKITTI 上尺度比率达到 0.9905，几乎与真值 1:1 对齐。

### 3. 缓存一致性训练与周期刷新：消除训练-推理鸿沟

流式推理依赖 KV 缓存传递历史信息，但标准训练采用独立分块，缺乏显式的缓存传递机制，导致训练与推理之间存在严重的分布偏移。具体表现为：

- **注意力沉没**：因果推理模式下，模型过度依赖初始帧的注意力沉没（attention sink），当滑动窗口推理移除该沉没帧时精度崩溃。
- **KV 缓存污染**：长序列下陈旧特征在缓存中累积，污染后续帧的注意力计算。

LongStream 通过两项机制解决上述问题：

- **缓存一致性训练**：在训练中显式传递并裁剪 KV 缓存，强制模型在纯滑动窗口条件下工作（Algorithm 1）。这使得模型学会不依赖注意力沉没，在全窗口和滑动窗口推理下均保持稳定且最优的精度（Figure 4）。
- **周期缓存刷新**：每 $N$ 个关键帧重置沉没帧和 KV 缓存，清除饱和特征的同时保持几何连续性。这类似于硬边际化陈旧上下文，无需额外计算开销即可对抗长时记忆饱和。

### 消融验证

Table 5 的消融实验量化了各模块的贡献：从基线（8.043 ATE）开始，依次启用相对位姿头和正交尺度学习将 ATE 降至 2.645，加入缓存一致性训练进一步降至 0.984，最终加入周期缓存刷新降至 0.115。每一模块均带来显著且不可替代的增益。

LongStream 是一个**规范解耦的流式几何框架**，在统一的时空 Transformer 内联合预测位姿、深度和尺度。其核心设计思想是将长程外推问题重新表述为恒定难度的局部相对姿态估计任务，并通过正交尺度学习实现几何与尺度的完全解耦。

### Pipeline 总览

系统以流式视频帧序列 $\{I_1, I_2, \dots, I_S\}$ 为输入，逐帧处理并在线输出以下五类信息（见 Figure 3）：

![[assets/figures/papers/paper_list_l2538_https_arxiv_org_abs_2602_13172/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our proposed LongStream. Given streaming inputs, patch tokens are extracted by a ViT encoder and augmented with keyframe, normal-frame, and scale tokens. Tokens are fused via causal attention with a shared KV cache, which is consistently used in both training and inference for cache-consistent streaming modeling. The network predicts keyframe-relative poses*

- **关键帧相对位姿** $\mathbf{T}_{ik} = \mathbf{T}_i \circ \mathbf{T}_k^{-1}$：当前帧 $i$ 相对于前一关键帧 $k$ 的 SE(3) 变换，包含平移、旋转和焦距偏移
- **深度图** $D_i$：帧级稠密深度估计
- **世界坐标点云** $X_i$：在尺度归一化空间中的 3D 结构
- **全局尺度因子** $s = \exp(\mathbf{w}^\top \mathbf{h}_{\mathrm{scale}})$：由专用尺度头独立预测的正值缩放因子
- **帧特征** $\mathbf{h}_i$：用于后续模块的中间表示

### 模块构成与数据流

LongStream 由以下核心模块串联构成，形成端到端的流式推理管线：

1. **ViT 编码器**（基于 DINOv2）：对每一帧提取 patch 级别的视觉 Token，并附加三类可学习 Token——关键帧 Token、普通帧 Token 和尺度 Token，为后续的帧类型区分和尺度解耦提供显式信号。

2. **因果 Transformer 聚合器**：在严格因果注意力掩码下执行交替的帧内注意力和全局注意力，融合时空信息。关键帧 Token 作为局部坐标锚点参与注意力计算，使模型能够在滑动窗口内建立帧间关联。

3. **相对位姿头**：通过参考感知注意力机制，迭代预测当前帧相对于关键帧的平移向量 $\mathbf{t}_{ik}$、单位四元数 $\mathbf{q}_{ik}$ 和焦距偏移 $f_{ik}$，构成完整相对位姿 $\mathbf{p}_{ik} = [\mathbf{t}_{ik}, \mathbf{q}_{ik}, f_{ik}]$。

4. **尺度头**：接收专用尺度 Token 的特征，预测对数尺度并经指数化得到正尺度因子 $s$。该模块仅在具有度量真值的数据上训练，使尺度学习与几何优化完全松绑。

5. **深度头与点云头**：分别预测帧级深度图和尺度归一化空间中的世界坐标点云及置信度。几何损失在尺度不变空间中计算，确保几何优化独立于全局尺度。

6. **流式 KV 缓存机制**：配合缓存一致性训练和周期性缓存刷新，在训练中传递并裁剪 KV 缓存以对齐推理时的滑动窗口行为，并每 $N$ 个关键帧重置陈旧缓存以对抗长时记忆饱和。

### 输入输出流

| 阶段 | 输入 | 输出 |
|------|------|------|
| 编码 | 单帧 RGB 图像 $I_i$ | Patch Token + 关键帧/普通帧/尺度 Token |
| 聚合 | 当前帧 Token + 历史 KV 缓存 | 时空融合后的帧特征 $\mathbf{h}_i$ |
| 位姿预测 | $\mathbf{h}_i$ + 关键帧特征 | 相对位姿 $\mathbf{p}_{ik}$ |
| 尺度预测 | 尺度 Token 特征 | 全局尺度因子 $s$ |
| 几何预测 | $\mathbf{h}_i$ + 位姿 + 尺度 | 深度图 $D_i$、点云 $X_i$、置信度 |

### 关键设计决策

**规范解耦**是贯穿整个 pipeline 的核心原则。传统流式模型将第一帧固定为全局坐标锚点，导致长序列下注意力衰退和尺度漂移。LongStream 通过以下三项机制彻底消除这一瓶颈：

- **SE(3) 规范解耦**：丢弃第一帧锚点，转而预测关键帧相对位姿，使外推任务在任意序列长度下保持恒定难度
- **Sim(3) 解耦**：几何分支在尺度不变空间中优化，尺度头独立预测全局尺度因子，二者通过正交设计互不干扰
- **训练-推理一致性**：缓存一致性训练强制模型在纯滑动窗口下运作，消除注意力沉没；周期性缓存刷新定期清除饱和特征，维持长时记忆质量

Figure 2 进一步验证了该设计的工程优势：LongStream 的内存占用和推理延迟随序列增长保持稳定，而离线模型 VGGT 和 FastVGGT 的内存消耗快速增长并最终触发显存溢出。

### 3.1 整体框架与概率图模型

LongStream 将流式三维重建建模为一个统一时空 Transformer 下的联合预测问题。对于每一帧 $I_i$，模型输出帧特征 $h_i$、相对位姿 $\mathbf{p}_{ik}$、深度图 $D_i$、世界坐标点云 $X_i$ 以及全局尺度因子 $s$：

$$\{ h_{i}, \mathbf{p}_{ik}, D_{i}, X_{i}, s \} = F_{\boldsymbol{\theta}}(I_{i}), \quad i = 1, \ldots, S.$$

该框架的核心设计哲学在于将长程外推问题重新表述为**局部相对姿态估计任务**，并通过**正交尺度学习**实现几何与尺度的完全解耦，从而消除对第一帧锚点的依赖。

整个系统的损失函数源自一个分解形式的概率图模型，其负对数后验为：

$$p(D, X, p, s \mid I) \propto p(D \mid X, I) \cdot p(X \mid p, s, I) \cdot p(p \mid I) \cdot p(s)$$

对应的总损失函数为四项加权和：

$$\mathcal{L} = \underbrace{\mathcal{L}_{\mathrm{geom}} + \mathcal{L}_{\mathrm{depth}}}_{\text{Geometry \& Depth}} + \underbrace{\mathcal{L}_{\mathrm{pose}}}_{\text{Pose}} + \underbrace{\mathcal{L}_{\mathrm{scale}}}_{\text{Scale}}$$

---

### 3.2 规范解耦：SE(3) 关键帧相对位姿

**瓶颈分析**：现有流式模型（如 **Stream3R**、**StreamVGGT**）采用“规范耦合”设计——固定第一帧为全局坐标锚点，直接回归绝对位姿。在长序列下，这种设计导致注意力衰退、尺度漂移和外推误差累积，轨迹在数十米内即崩溃。

**核心机制**：LongStream 彻底解除全局坐标系锚定，改为预测当前帧 $i$ 相对于前一关键帧 $k$ 的 SE(3) 相对位姿 $\mathbf{T}_{ik}$：

$$\mathbf{T}_{ik} = \mathbf{T}_i \circ \mathbf{T}_k^{-1}$$

其中 $\mathbf{T}_i$ 为帧 $i$ 的绝对位姿，$\mathbf{T}_k$ 为关键帧 $k$ 的绝对位姿。该变换具有严格的 SE(3) 规范不变性——无论全局坐标系如何选取，相对位姿 $\mathbf{T}_{ik}$ 保持不变。这使得外推任务从“在全局长序列上维持累积精度”退化为“恒定难度的局部相对估计”，从根本上抑制了长程漂移。

相对位姿头输出一个六维向量，由平移向量 $\mathbf{t}_{ik}$、单位四元数 $\mathbf{q}_{ik}$ 和焦距偏移 $f_{ik}$ 组成：

$$\mathbf{p}_{ik} = [\mathbf{t}_{ik}, \mathbf{q}_{ik}, f_{ik}]$$

该头部采用参考感知注意力机制，迭代预测当前帧相对于关键帧的位姿增量。

---

### 3.3 Sim(3) 解耦：正交尺度学习

**瓶颈分析**：在耦合设计中，尺度与几何隐式绑定——几何分支的优化目标同时包含形状和尺度信息，导致尺度误差通过几何梯度反向传播，加剧轨迹漂移。

**核心机制**：LongStream 引入**正交尺度学习**，将几何优化与尺度估计完全松绑。具体而言：

1. **几何分支**在尺度不变空间中优化。对预测点云 $\hat{X}_{\mathrm{raw}}$ 和真实点云 $X_{\mathrm{gt}}$ 分别进行尺度归一化后计算 L1 损失：

   $$\tilde{X}_{\mathrm{pred}} = \frac{\hat{X}_{\mathrm{raw}}}{\mathrm{Norm}(\hat{X}_{\mathrm{raw}})}, \quad \mathcal{L}_{\mathrm{geom}} = \|\tilde{X}_{\mathrm{pred}} - \tilde{X}_{\mathrm{gt}}\|_1$$

   该设计确保几何优化独立于全局尺度，消除尺度-几何的梯度耦合。

2. **尺度头**接收专用的 Scale Token 特征 $\mathbf{h}_{\mathrm{scale}}$，独立预测全局对数尺度并指数化得到正尺度因子：

   $$\boldsymbol{s} = \exp(\mathbf{w}^\top \mathbf{h}_{\mathrm{scale}})$$

   尺度损失在对数空间中度量，仅对具有度量真值的数据施加：

   $$\mathcal{L}_{\mathrm{scale}} = \|\log \hat{s} - \log s_{\mathrm{gt}}\|_1$$

   对数空间的选择源于尺度的乘法性质——对数变换将乘法误差转化为加法误差，有利于训练稳定。

---

### 3.4 缓存一致性训练与周期缓存刷新

**瓶颈分析**：标准分块训练中，Transformer 各块独立处理，无显式 KV 缓存传递。这导致两个问题：(1) **注意力沉没**——因果推理时模型过度关注初始帧（sink token），削弱对后续帧的注意力；(2) **训练-推理不一致**——训练时窗口内全可见，推理时滑动窗口受限，导致精度崩溃。

**核心机制**：

1. **缓存一致性训练（CCT）**：在训练过程中显式传递并裁剪 KV 缓存，强制模型在纯滑动窗口下运作。如 Algorithm 1 所示，训练时将序列切分为多个 chunk，每个 chunk 继承前一 chunk 的 KV 缓存，处理完毕后按窗口大小 $W$ 裁剪缓存，再传递给下一 chunk。这使得训练与推理的注意力可见范围完全一致，消除注意力沉没（见 Figure 4 的注意力图对比）。

![[assets/figures/papers/paper_list_l2538_https_arxiv_org_abs_2602_13172/figures/004_Figure_4.jpg]]
*Figure 4: Cache-consistent training (CCT). We show attention maps (top) and Relative Pose Error (RPE) heatmaps (bottom) under different training–inference settings. Without CCT (left), causal inference develops a strong attention sink; windowed inference either amplifies this sink when it is kept or collapses when it is removed. With CCT (right), the sink is strongly suppressed in causal mode and likewise suppressed in both windowed modes, yielding stable and best accuracy. Light blue denotes attention to the keyframe*

2. **周期缓存刷新**：每 $N$ 个关键帧重置 sink frame 和 KV 缓存，硬性地边缘化陈旧上下文。该操作保留了关键帧间的几何连续性，同时清除因长时间累积而退化的特征，对抗长时记忆饱和。刷新周期 $N=10$ 在漂移累积和训练动态之间取得最佳平衡（消融实验 ATE 0.115，见 Table 7）。

---

### 3.5 网络架构关键组件

LongStream 的端到端架构（见 Figure 3）包含以下核心模块：

- **ViT Encoder**：基于 DINOv2 的视觉编码器提取每帧 patch 特征，并附加关键帧 Token、普通帧 Token 和尺度 Token，为后续时空融合提供结构化输入。

- **Causal Transformer Aggregator**：在严格因果掩码下交替执行帧内注意力与全局注意力，融合时空信息。Transformer 块的形式为：

  $$H^{(l+1)} = \mathrm{Block}^{(l)}(H^{(l)}, \mathrm{AttnMask})$$

  因果掩码确保当前帧仅可见历史帧，符合在线推理约束。

- **Depth Head 与 Pointmap Head**：分别预测帧级深度图和世界坐标点云，配合置信度估计，在尺度归一化空间中优化几何结构。

- **Streaming KV Cache with CCT & Periodic Refresh**：在训练中传递并裁剪 KV 缓存以对齐推理，并每 $N$ 个关键帧重置陈旧缓存，实现训练-推理一致性并防止长时记忆饱和。

## 实验与关键发现

### 主实验结果

LongStream 在室内外多个基准上以显著优势超越现有流式与离线方法，验证了规范解耦设计在长序列场景下的关键作用。

**室外驾驶场景（KITTI / vKITTI / Waymo）**。在 KITTI 的 11 个序列上，LongStream 取得平均 ATE 51.90，而最佳流式基线 StreamVGGT 为 226.15，Stream3R 为 177.73（Table 1）。在 vKITTI 的 5 个场景中，LongStream 平均 ATE 仅 1.610，StreamVGGT 高达 83.916，性能差距近 52 倍（Table 3）。Waymo 序列上 LongStream 的 ATE 为 0.737，StreamVGGT 为 45.101（Table 2）。定性结果（Figure 5）显示，Stream3R 与 StreamVGGT 在数百米轨迹上迅速累积漂移，VGGT-SLAM 在第二个 vKITTI 序列中因显存溢出而崩溃；LongStream 在所有场景下保持轨迹连续性与一致性，即使在大回环运动中亦然。

**室内小尺度场景（TUM-RGBD / 7Scenes）**。在 TUM-RGBD 上，LongStream 取得 ATE 0.076，StreamVGGT 为 0.627，误差降低一个数量级（Table 2）。7Scenes 上的 Chamfer Distance 为 2.260，StreamVGGT 为 6.630（Table 4）。Figure 6 的室内定性对比进一步表明，在强视角变化、遮挡与反复折返等挑战性场景中，LongStream 维持稳定位姿与一致三维结构，而 Stream3R 与 StreamVGGT 在高度折叠轨迹上出现明显漂移。

**计算效率**。LongStream 在长序列推理中保持约 18 FPS 的实时性能（单 GPU），内存与延迟保持恒定，而 VGGT 与 FastVGGT 随序列增长迅速膨胀并最终触发 OOM（Figure 2）。

### 消融实验

Table 5 系统性地拆解了各设计组件的贡献。基线模型（绝对位姿回归，无尺度头，无 CCT，无缓存刷新）ATE 为 8.043。依次启用相对位姿头（RelPose）与正交尺度头后，ATE 降至 2.645；进一步加入缓存一致性训练（CCT）降至 0.984；最终加入周期缓存刷新后降至 0.115。每一步均带来显著增益，验证了“规范解耦—训练推理对齐—记忆管理”三级递进设计的必要性。

![[assets/figures/papers/paper_list_l2538_https_arxiv_org_abs_2602_13172/figures/011_Table_5.jpg]]
*Table 5: Ablation study on RelPose, Scale head, CCT, and cache refresh. Green indicates enabled, red indicates disabled. Rows 2 and 3 ATE gap is caused by a few large trajectory outliers. Scale Error reports absolute scale deviation; lower is better*

Figure 4 / Figure 7 从注意力机制角度揭示了 CCT 的作用机理：无 CCT 时，因果推理产生强烈的注意力沉没（attention sink），窗口化推理要么放大该沉没（保留 sink 时），要么导致精度崩溃（移除 sink 时）；启用 CCT 后，沉没在因果与窗口两种模式下均被有效抑制，相对位姿误差（RPE）热力图显示全窗口稳定且最优的精度分布。

关键超参数消融进一步确认了设计选择的有效性：

- **关键帧间隔 N**（Table 7）：N=10 在漂移累积与训练动态间取得最佳平衡（ATE 0.115）。N=1 时帧间跟踪导致误差快速累积，N=15 时因关键帧切换过稀而性能退化。
- **缓存窗口大小 W**（Table 8）：W=10 足以保持上下文并防止几何饱和；增大至 30 时 ATE 升至 0.516，证实过长历史缓存会污染注意力并引入退化特征。

![[assets/figures/papers/paper_list_l2538_https_arxiv_org_abs_2602_13172/figures/015_Table_7.jpg]]
*Table 7: Effect of Keyframe Interval. N = 10 yields the best trade-off between drift accumulation and training dynamics*

### 长序列稳定性分析

Table 6 直接检验了 LongStream 在公里级序列上的外推能力。在 Waymo 序列（135 m）和 KITTI #03 序列（561 m）上，LongStream 的 ATE 随帧数增加保持稳定：例如 KITTI #03 在 801 帧时 ATE 仅 3.81。相比之下，无缓存刷新与滑动窗口的变体（w/o SW）误差随序列长度非线性增长，验证了周期缓存刷新对于对抗长时记忆饱和的关键作用。

![[assets/figures/papers/paper_list_l2538_https_arxiv_org_abs_2602_13172/figures/013_Table_6.jpg]]
*Table 6: ATE (m) as sequence length increases on Waymo #520018670 (Left, 135 m) and KITTI #03 (Right, 561 m). w/o SW denotes the variant without cache refresh and sliding window*

### 尺度估计精度

正交尺度学习使 LongStream 在 vKITTI 上取得与真值几乎 1:1 的尺度比率（0.9905），证明了 Sim(3) 解耦策略在保持几何精度的同时实现了准确的全局尺度恢复。

### 失败模式与局限

LongStream 在以下场景中仍存在退化：

- **无回环闭合**（Figure 8）：当重新访问同一地点时，LongStream 出现轻微漂移，表明缺乏显式回环检测机制限制了全局一致性。
- **极长窗口点云退化**：在超长序列下点云一致性略有下降，可能与缓存窗口内几何特征的渐进饱和有关。
- **动态场景**：模型假设场景基本静止，对动态目标处理能力有限，该方向的验证数据尚不充分，需人工核实具体退化程度。
- **手工关键帧调度**：固定间隔 N=10 的关键帧选择策略可能非最优，无法适应不同场景的运动模式。

![[assets/figures/papers/paper_list_l2538_https_arxiv_org_abs_2602_13172/figures/002_Figure_2.jpg]]
*Figure 2: Memory and runtime comparison. Our method keeps memory and latency stable, whereas VGGT and FastVGGT grow rapidly and hit OOM on long sequences*

## 定位与知识库关联

### 1. 与流式自回归重建基线的关系

LongStream 直接对标当前流式3D重建的两条核心基线：**Stream3R** 与 **StreamVGGT**。这两者代表了“规范耦合”（gauge-coupled）范式——即将第一帧固定为全局坐标系锚点，后续所有帧的位姿回归均相对于该固定原点。这一设计在短序列上有效，但在长序列下暴露出系统性脆弱性：

- **注意力衰退与尺度漂移**：随着序列增长，当前帧与第一帧的时序距离线性增加，Transformer的自注意力机制难以维持远距离依赖，导致位姿外推误差非线性累积。Stream3R和StreamVGGT在数十米内即出现轨迹崩溃（见 Figure 1）。
- **注意力沉没（attention sink）**：标准分块训练未传递KV缓存，推理时因果注意力将大量权重分配给初始帧的“沉没token”，形成信息瓶颈。当推理切换为滑动窗口时，该沉没token被移除会导致模型精度崩塌（见 Figure 4 左侧）。

LongStream 的突破在于将问题重新表述：**解除第一帧锚点依赖，转而预测关键帧相对位姿**。这一“规范解耦”（gauge-decoupled）设计将外推任务从“相对于遥远原点的绝对回归”转化为“相对于最近关键帧的局部估计”，使任务难度恒定，不再随序列长度增长。

此外，LongStream 还引入了**正交尺度学习**，将几何与尺度完全松绑：几何分支在尺度归一化空间优化（保证尺度不变性），专用尺度头独立预测全局尺度因子。这解决了耦合范式中尺度误差通过几何分支放大漂移的根本问题。

### 2. 与离线模型及SLAM系统的关系

LongStream 在实验中也与离线模型和优化法SLAM系统进行了对比：

- **离线模型**：**FastVGGT**（轻量版VGGT）采用分块推理，可访问未来帧，在短序列上具有精度优势。但其内存和延迟随序列长度线性增长，在长序列上触发OOM（见 Figure 2）。LongStream 通过滑动窗口KV缓存保持恒定内存占用，在公里级序列上维持18 FPS。
- **优化法SLAM**：**MASt3R-SLAM** 和 **VGGT-SLAM** 依赖后端优化和图优化，在回环场景下具有全局一致性优势。但在严格在线、不可见未来帧的设定下，其性能受限于前端里程计的漂移。LongStream 在无回环检测的条件下，通过缓存一致性训练和周期缓存刷新实现了稳定的长程轨迹（见 Table 1），但在回环场景下仍存在轻微漂移（见 Figure 8），表明与SLAM后端的互补潜力。

值得注意的公平性考量：VGGT-SLAM在评估中采用分块推理（可访问未来帧），而LongStream严格遵循在线设定，因此直接ATE对比可能低估LongStream的相对优势。即便如此，LongStream在KITTI上平均ATE 51.90，显著优于StreamVGGT的226.15和Stream3R的177.73（Table 1）。

### 3. 适用边界

LongStream 的设计假设和当前实现定义了其适用范围：

- **静态场景假设**：模型未显式建模动态目标，对移动物体的几何一致性处理能力有限。在包含大量动态元素的序列中，深度和点云预测可能退化。
- **固定关键帧调度**：关键帧间隔依赖手工设定的固定超参数（N=10），无法根据场景复杂度自适应调整。在快速旋转或纹理稀疏区域，固定间隔可能导致关键帧质量不足。
- **无回环闭合**：当前框架未集成回环检测或位姿图优化，在长距离回环场景下存在累积漂移（Figure 8 证实了这一点）。这是与经典SLAM系统的主要功能差距。
- **极长窗口点云退化**：尽管周期缓存刷新有效抑制了注意力饱和，在极端长序列下点云一致性仍有轻微退化，提示几何记忆的物理上限。

### 4. 局限与开放问题

基于上述边界，以下方向值得进一步探索：

| 局限 | 开放问题 |
|------|----------|
| 静态场景假设 | 如何引入运动分割或动态mask，使模型在动态环境中保持几何一致性？ |
| 手工关键帧调度 | 能否学习自适应或任务驱动的关键帧选择策略（如基于光流幅值或不确定性估计）？ |
| 无回环闭合 | 如何在不显著增加计算开销的前提下整合轻量在线回环检测与校正？ |
| 极长序列点云退化 | 可否通过分层记忆机制或外部记忆模块进一步提升超长序列下的点云精度？ |

### 5. 知识库定位

LongStream 处于**流式自回归3D视觉**与**在线SLAM**的交叉地带。其核心贡献——规范解耦、正交尺度学习、缓存一致性训练——为流式几何估计提供了新的设计范式。相较于依赖后端优化的传统SLAM，LongStream 代表了纯前馈、无优化的在线重建路径，在计算效率和长程稳定性之间取得了独特的平衡。其缓存一致性训练策略（CCT）对更广泛的流式Transformer应用（如视频理解、在线导航）也具有方法论迁移价值。

## 原文 PDF

![[paperPDFs/CVPR_2026/LongStream_Long_Sequence_Streaming_Autoregressive_Visual_Geometry.pdf]]

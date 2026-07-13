---
title: "JanusVLN: Decoupling Semantics and Spatiality with Dual Implicit Memory for Vision-Language Navigation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Implicit_Memory_for_Vision_Language_Navigation.pdf
project_link: https://miv-xjtu.github.io/JanusVLN.github.io/
code_link: null
openreview_forum_id: RnuB0Nlbd5
aliases:
- JanusVLN
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入双隐式神经记忆（空间几何与视觉语义），利用固定大小KV缓存与增量更新，同时解耦并增强空间与语义理解。"
primary_logic: "模仿人脑半球分工，解耦语义与空间流；通过缓存经深度处理的KV隐式表示历史，并以定长记忆窗口实现高效在线导航。"
claims:
- "JanusVLN在R2R-CE Val-Unseen上SR达到60.5，显著超越NaVILA、StreamVLN等SOTA方法。"
- "移除空间隐式记忆使SPL从49.2降至40.9，证明空间几何记忆的关键作用。"
- "相比原始VGGT，缓存记忆使推理时间减少69-90%，在32帧时仅149 ms vs 1549 ms。"
- "在复杂指令（400-550词）上JanusVLN性能保持，而StreamVLN降为零，体现双隐式记忆的优势。"
---

# JanusVLN: Decoupling Semantics and Spatiality with Dual Implicit Memory for Vision-Language Navigation

> [!tip] 核心洞察
> 模仿人脑半球分工，解耦语义与空间流；通过缓存经深度处理的KV隐式表示历史，并以定长记忆窗口实现高效在线导航。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | JanusVLN：基于双隐式记忆的语义与空间解耦视觉-语言导航 |
| 英文题名 | JanusVLN: Decoupling Semantics and Spatiality with Dual Implicit Memory for Vision-Language Navigation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RnuB0Nlbd5) · [Project](https://miv-xjtu.github.io/JanusVLN.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | JanusVLN |
| Dataset | R2R-CE Val-Unseen, RxR-CE Val-Unseen |

> [!tip] 效果简介
> - R2R-CE Val-Unseen 上，SR 为 60.5，对比 56.9 (StreamVLN)，变化 +3.6。
> - R2R-CE Val-Unseen 上，SPL 为 56.8，对比 51.9 (StreamVLN)，变化 +4.9。
> - RxR-CE Val-Unseen 上，SR 为 56.2，对比 52.9 (StreamVLN)，变化 +3.3。

## 概要

视觉-语言导航（VLN）的核心瓶颈在于：现有方法普遍依赖**显式语义记忆**（如文本认知地图或全量历史帧），导致空间几何信息严重丢失、计算随轨迹长度线性膨胀，且多模态大语言模型（MLLM）的视觉编码器缺乏3D空间推理能力。**JanusVLN** 受启发于人脑半球的功能分工，提出了一套**双隐式记忆范式**——将视觉语义与空间几何解耦为两个固定大小的神经记忆（KV缓存），通过增量更新机制实现高效的在线导航。

该方法仅需单目RGB视频输入，无需全景图、里程计或深度数据，在R2R-CE Val-Unseen上以 **SR 60.5、SPL 56.8** 显著超越 NaVILA（Cheng et al., RSS 2025）、StreamVLN（Wei et al., arXiv 2025）等同期SOTA方法。消融实验表明，移除空间隐式记忆使SPL骤降8.3，而双记忆同时移除则导致性能近乎崩溃（SR从52.8降至24.8）。在推理效率上，缓存记忆机制使单帧处理时间相比原始VGGT降低**69-90%**，且在48帧序列长度下避免显存溢出。真实世界实验中，空间记忆的引入使空间理解任务成功率提升**23.6%**，验证了该范式从仿真到现实的迁移能力。



视觉-语言导航（Vision-Language Navigation, VLN）要求智能体根据自然语言指令在连续环境中执行一系列动作。近年来，多模态大语言模型（MLLM）的引入为VLN带来了更强的语义理解能力，但现有方法在记忆机制与空间推理两个维度上仍存在根本性瓶颈。

**显式记忆的困境。** 当前主流方法在历史信息管理上依赖显式语义记忆，典型范式包括两类：一类以 **MapNav**（Zhang et al., ACL 2025）为代表，将观测历史压缩为文本认知地图；另一类以 **NaVILA**（Cheng et al., RSS 2025）和 **StreamVLN**（Wei et al., arXiv 2025）为代表，直接保留全部历史帧作为视觉上下文。这两种策略均面临结构性缺陷：文本认知地图在压缩过程中不可避免地丢失细粒度空间几何信息；全历史帧方案则导致记忆膨胀——随着导航轨迹增长，需重新处理所有历史帧，计算冗余急剧增加，推理效率持续恶化。

**空间感知的缺失。** 更关键的是，现有MLLM的视觉编码器（如CLIP）本质上是为2D语义理解设计的，缺乏3D空间推理能力。这意味着智能体无法从单目RGB视频中有效提取深度、方位、相对位置等空间几何信息，而这些信息对于“走到沙发左侧的绿植旁”这类指令的理解至关重要。部分方法尝试引入深度数据或里程计来弥补这一缺陷（如 **g3D-LF**, Wang & Lee, CVPR 2025），但额外传感器的依赖限制了方法的普适性。

**核心洞察：语义与空间的解耦。** JanusVLN的核心动机源于对人脑认知机制的借鉴：人类在导航时，大脑半球分别处理语义理解与空间几何信息，两者协同但不混淆。这一洞察指向了一个关键的设计选择——将视觉语义与空间几何解耦为两个独立但互补的记忆流，而非在单一表示中混合两者。具体而言，JanusVLN提出双隐式神经记忆范式：以固定大小的KV缓存替代显式历史帧，分别存储空间几何与视觉语义的隐式表示，通过增量更新机制实现高效在线导航。同时，引入前馈式3D视觉几何基础模型（VGGT）为MLLM注入空间几何先验，使智能体仅凭单目RGB视频即可获得3D空间理解能力。



## 核心方法与创新机理

JanusVLN 的核心创新在于将视觉-语言导航中的语义理解与空间几何推理**显式解耦**，并为之构建了一套**双隐式记忆**（Dual Implicit Memory）机制。这一设计直接回应了现有 MLLM 导航方法的瓶颈：显式记忆（文本认知地图或全历史帧）随轨迹增长而膨胀，导致计算冗余、空间信息丢失，且纯 2D 语义编码器缺乏 3D 空间推理能力。

具体而言，JanusVLN 在四个关键维度上对 baseline 方法进行了系统性改造：

### 1. 记忆表示方式：从显式到隐式

现有方法如 **NaVILA**（Cheng et al., RSS 2025）和 **StreamVLN**（Wei et al., arXiv 2025）依赖显式历史帧，**MapNav**（Zhang et al., ACL 2025）则构建文本语义认知地图。这些显式表示随导航步数线性增长，带来高昂的计算与存储开销。

JanusVLN 将记忆建模为**固定大小的 KV 缓存**——即经过神经网络深度处理后的隐式表示，而非原始像素或文本。这种隐式记忆由两部分构成：空间几何记忆与视觉语义记忆，其大小不随轨迹长度增长，从根本上解决了记忆膨胀问题（Figure 2, Section 3.2）。

### 2. 空间特征提取：从 2D 语义到 3D 几何先验

Baseline 方法的空间理解仅依赖于 2D 语义编码器（如 CLIP），缺乏对 3D 场景结构的显式建模。JanusVLN 引入 **VGGT**（Visual Geometry Grounding Transformer）作为空间几何编码器，从单目 RGB 视频中提取 3D 几何 token $G_t$，并预测点云 $P_t$ 和置信度 $C_t$：

$$
\{ G_t \}_{t=1}^{T} = \mathrm{Decoder}( \mathrm{Encoder}( \{ x_t \}_{t=1}^{T} ) ), \quad (P_t, C_t) = \mathrm{Head}(G_t)
$$

VGGT 通过像素到 3D 点云的预训练，为模型提供了**前馈式 3D 空间几何先验**，使 JanusVLN 无需深度、里程计或全景图等额外模态即可获得空间推理能力（Section 3.1, 3.3）。

### 3. 历史信息更新：从全量重计算到增量缓存

传统方法每次处理新帧时需重新编码全部历史帧，VGGT 的推理时间随序列长度指数增长——在 48 帧时，48G 显存的 GPU 直接触发 OOM（Figure 3）。JanusVLN 采用**增量更新策略**：仅保留初始帧缓存 $M_{initial}$ 和滑动窗口缓存 $M_{sliding}$，新帧编码时通过交叉注意力检索历史信息：

$$
G_t = \mathrm{Decoder}( \mathrm{CrossAttn}( \mathrm{Encoder}(x_t), \{M_{initial}, M_{sliding}\} ))
$$

这一设计使推理时间从 VGGT 的 1549 ms（32 帧）降至 149 ms，减少 **69-90%**，且性能在 48 帧时达到饱和（Table 5）。

### 4. 特征融合策略：从单一语义到加权空间增强

Baseline 方法或缺乏空间特征，或仅做简单拼接。JanusVLN 设计了**加权 MLP 投影融合**机制，将语义 token $S'_t$ 与空间几何 token $G'_t$ 进行加性融合：

$$
F_t = S'_t + \lambda \cdot MLP(G'_t)
$$

消融实验表明，融合权重 $\lambda=0.2$ 时性能最优（SR 52.8），且加权加法优于 Cross-Attention 融合（Table 7）。这一轻量融合策略使 LLM 主干（Qwen2.5-VL）能够同时感知场景的语义内容与 3D 空间结构，从而做出更精准的导航决策。

---

**因果机制总结**：JanusVLN 通过“解耦编码 → 隐式缓存 → 增量更新 → 加权融合”四步联动，在保持定长记忆窗口的同时，为 MLLM 注入了 3D 空间推理能力。消融实验提供了强因果证据：移除空间隐式记忆使 SPL 从 49.2 骤降至 40.9（Table 3），而替换 VGGT 为 2D 编码器（DINOv2、SigLIP 2）或随机初始化均无显著提升，证明 **3D 几何先验不可替代**（Table 4）。



![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_RnuB0Nlbd5/figures/002_Figure_2.jpg]]
*Figure 2: The framework of JanusVLN. Given an RGB-only video stream and navigation instructions, JanusVLN utilizes a dual-encoder to separately extract visual-semantic and spatial-geometric features. It concurrently caches historical key-values from initial and recent sliding window into a dual implicit memory to facilitate feature reuse and prevent redundant computation. Finally, these two complementary features are fused and fed into LLM to predict the next action*

JanusVLN 提出了一种**双隐式记忆**范式，将视觉-语言导航解耦为**语义理解**与**空间几何推理**两条并行流，模仿人脑半球分工机制。整个 pipeline 仅以**单目 RGB 视频流**和自然语言导航指令为输入，输出为下一步动作预测。

### 核心设计动机

现有 MLLM 导航方法依赖显式记忆——要么维护文本形式的认知地图，要么保留全量历史帧。这带来三个瓶颈：**空间信息丢失**（2D 编码器缺乏 3D 推理能力）、**计算冗余**（每步需重新处理全部历史帧）、**记忆膨胀**（历史帧随轨迹线性增长）。JanusVLN 的解决方案是将记忆建模为**固定大小的紧凑神经表示**，其大小不随轨迹长度增长。

### 双流架构

框架由五个核心模块串联构成：

1. **语义编码器（Qwen2.5-VL 视觉编码器）**：从当前帧 $x_t$ 提取视觉语义 token $S_t$，同时与语义隐式记忆进行交互编码。
2. **空间几何编码器（预训练 VGGT）**：从 RGB 视频中提取 3D 空间几何 token $G_t$，提供点云、深度等空间先验。
3. **双隐式记忆缓存（KV Cache）**：存储两类历史信息——**初始化帧缓存** $M_{initial}$ 和**滑动窗口缓存** $M_{sliding}$。新帧编码时通过交叉注意力检索这些缓存，避免重复计算。
4. **特征融合模块（MLP 投影）**：将语义特征 $S'_t$ 与经 MLP 投影的空间几何特征 $G'_t$ 进行加权加性融合：
   $$F_t = S'_t + \lambda \cdot MLP(G'_t)$$
   其中 $\lambda=0.2$ 时性能最优。
5. **LLM 主干（Qwen2.5-VL）**：接收融合特征 $F_t$ 和导航指令，预测下一步动作。

### 记忆更新机制

隐式记忆的更新采用**增量策略**：保留初始 8 帧的 KV 缓存作为全局参考，同时维护最近 48 帧的滑动窗口缓存。每步仅需对新帧编码并与缓存进行交叉注意力，无需重新处理全量历史。这使推理时间相比原始 VGGT 降低 **69-90%**（32 帧时 149 ms vs 1549 ms），且内存占用保持恒定，避免了 VGGT 在 48 帧时即耗尽 48G 显存的问题。

### 输入输出流

- **输入**：单目 RGB 视频帧序列 + 自然语言导航指令
- **中间表示**：语义 token $S_t$（2D 视觉语义）与几何 token $G_t$（3D 空间结构）并行提取，通过双隐式记忆缓存实现历史信息的高效复用
- **输出**：LLM 基于融合特征 $F_t$ 预测的离散导航动作（如前进、转向、停止）

整个 pipeline 以**在线、流式**方式运行，无需全景图、里程计或深度传感器等额外输入，在仅使用单目 RGB 的条件下即可实现空间感知增强的导航决策。



### 3.1 空间几何编码器：VGGT重建管道

JanusVLN 使用预训练的 VGGT（Visual Geometry Grounding Transformer）作为空间几何编码器，从单目 RGB 视频流中提取 3D 结构先验。其核心重建管道为：

$$
\left\{ G _ { t } \right\} _ { t = 1 } ^ { T } = \mathrm { Decoder } ( \mathrm { Encoder } ( \left\{ x _ { t } \right\} _ { t = 1 } ^ { T } ) ) , \quad ( P _ { t } , C _ { t } ) = \mathrm { Head } ( G _ { t } )
$$

其中 $x_t$ 为第 $t$ 帧 RGB 输入，Encoder 将多视角图像编码为几何 token $G_t$，Decoder 通过交叉注意力机制融合时序信息，Head 从 $G_t$ 中预测点云 $P_t$ 和置信度 $C_t$。该模块为后续空间隐式记忆提供经过深度处理的 3D 几何表示。

### 3.2 双隐式记忆与交叉注意力

传统方法需重复处理全部历史帧，导致计算冗余。JanusVLN 创新性地将历史帧的 KV（Key-Value）缓存作为隐式记忆，通过增量更新避免重计算。对于新帧 $x_t$，其几何 token 通过交叉注意力与两类隐式记忆交互得到：

$$
G _ { t } = \operatorname { Decoder } ( \operatorname { CrossAttn } ( \operatorname { Encoder } ( x _ { t } ) , \{ M _ { i n i t i a l } , M _ { s l i d i n g } \} ) )
$$

其中 $M_{initial}$ 为初始帧窗口（前 8 帧）的 KV 缓存，$M_{sliding}$ 为滑动窗口（最近 48 帧）的 KV 缓存。这一设计使记忆大小恒定，不随轨迹长度增长，且推理时间仅随序列长度边际增长（Figure 3）。

### 3.3 语义编码与空间感知融合

语义特征由 Qwen2.5-VL 的视觉编码器提取：

$$
S _ { t } = \operatorname { Encoder } _ { \mathrm { sem } } ( x _ { t } ) , \quad S _ { t } \in \mathbb { R } ^ { \lfloor \frac { H } { p } \rfloor \times \lfloor \frac { W } { p } \rfloor \times C }
$$

其中 $H$、$W$ 为输入分辨率，$p$ 为 patch 大小，$C$ 为通道数。语义编码器同样与语义隐式记忆进行交叉注意力，产生语义 token $S'_t$。

空间几何 token $G_t$ 经 MLP 投影后与语义 token 进行加权加性融合：

$$
F _ { t } = S _ { t } ^ { \prime } + \lambda * M L P ( G _ { t } ^ { \prime } )
$$

其中 $\lambda = 0.2$ 为空间几何特征的融合权重（Table 7 消融实验证实该值最优）。融合后的视觉特征 $F_t$ 与导航指令一同输入 LLM 主干（Qwen2.5-VL），预测下一动作。该融合策略使语义理解与空间推理解耦互补，在复杂空间任务上较纯语义方法提升显著（Figure 7，空间任务 SR 提升 23.6%）。



## 实验与关键发现

### 主结果：R2R-CE 与 RxR-CE 基准

JanusVLN 在 VLN-CE 的 R2R Val-Unseen 分割上取得 **SR 60.5、SPL 56.8**（Table 1），显著超越现有方法。相比使用显式历史帧的流式方法 **StreamVLN**（Wei et al., arXiv 2025），SR 提升 +3.6，SPL 提升 +4.9；相比基于历史帧显式记忆的 **NaVILA**（Cheng et al., RSS 2025），SR 提升 +10.8。值得注意的是，JanusVLN 仅使用单目 RGB 视频输入，而诸多基线依赖全景、里程计或深度数据——在此约束下仍取得最优，证明双隐式记忆范式以更少的感知模态实现了更强的空间理解。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_RnuB0Nlbd5/figures/005_Table_1.jpg]]
*Table 1: Comparison with SOTA methods on VLN-CE R2R Val-Unseen split. External data includes any sources beyond the standard R2R/RxR-CE datasets (e.g., EnvDrop, DAgger, general VQA, etc.). StreamVLN* uses EnvDrop as external data. NaVILA* excludes human-following data. All results are from their respective papers. A training sample is an action or a QA pair. Pano, Odo, Depth, and S.RGB respectively represent panoramic view, odometry, depth, and single RGB*

在不使用额外训练数据的设定下（JanusVLN*），模型仍达到 SR 52.8、SPL 49.2，已超越部分使用额外数据的方法，体现数据效率优势。在更具挑战性的 RxR-CE Val-Unseen 上，JanusVLN 同样取得 SR 56.2、SPL 47.5 的最优结果（Table 2），相比 StreamVLN 分别提升 +3.3 和 +1.5。

在 HM3D-OVON val unseen 基准上（Table 6），JanusVLN 以 SR 44.9、SPL 31.7 超越此前最优的 **MTU3D**（SR 40.8），进一步验证了方法在开放词汇物体导航场景下的泛化能力。

### 消融实验：双隐式记忆的核心作用

Table 3 的消融实验揭示了双隐式记忆各组件的因果贡献：

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_RnuB0Nlbd5/figures/007_Table_3.jpg]]
*Table 3: The ablation experiments of each component of the proposed JanusVLN*

- **移除空间隐式记忆**：SPL 从 49.2 骤降至 40.9（-8.3），SR 从 52.8 降至 47.0。这表明空间几何记忆对路径效率至关重要——缺乏 3D 空间先验使 agent 更容易偏离最优轨迹。
- **移除语义隐式记忆**：SR 从 52.8 降至 45.5（-7.3），SPL 降至 40.0。语义记忆的缺失直接削弱了指令与视觉场景的对齐能力。
- **同时移除双隐式记忆**：SR 从 52.8 崩溃至 24.8，NE 从 5.17 恶化至 8.04。此时模型退化为仅依赖当前帧的单步决策，几乎丧失导航能力。

这些结果确证了核心洞察：**语义与空间记忆并非简单叠加，而是互补协同**——前者负责指令-场景对齐，后者负责 3D 几何推理，两者缺一不可。

### 空间几何编码器的不可替代性

Table 4 对比了不同视觉编码器的效果。将 VGGT 替换为 2D 语义编码器（DINOv2、SigLIP 2）或使用随机初始化的 VGGT，均无法达到预训练 VGGT 的性能。具体而言，预训练 VGGT 取得 SR 52.8，而随机初始化 VGGT 仅 49.0，DINOv2 为 48.5。这证明 **3D 几何先验（pixel-to-3D point cloud 预训练）是空间理解的关键**，而非简单的编码器容量增加。

### 推理效率：缓存记忆的显著优势

Table 5 和 Figure 3 展示了缓存记忆机制对推理效率的质变影响。原始 VGGT 需要重新编码全部历史帧，推理时间随序列长度指数增长——在 48 帧时即触发 48G GPU 的显存溢出（OOM）。相比之下，JanusVLN 的缓存记忆仅需对当前帧进行交叉注意力检索：

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_RnuB0Nlbd5/figures/009_Table_5.jpg]]
*Table 5: Inference time and performance comparison for the current frame of varying sequence lengths between cached memory and VGGT for the online setting*

- 在 32 帧时，缓存记忆推理仅需 **149 ms**，而 VGGT 需 1549 ms，**减少约 90%**；
- 在 64 帧时，缓存记忆仍仅需 249 ms，VGGT 早已不可运行。

性能方面，缓存记忆在序列长度 48 时达到饱和（SR 52.8），继续增大窗口无显著收益，表明定长记忆窗口设计有效平衡了信息保留与计算开销。

### 融合策略与训练数据

Table 7 显示，空间与语义特征的融合权重 λ=0.2 时性能最优（SR 52.8），CrossAttn 融合策略略逊于加权加法，说明简洁的加性融合已能有效传递几何信息。Table 8 表明，同时使用 ScaleVLN 和 DAgger 额外数据可将 SR 进一步提升至 60.5、SPL 至 56.6，验证了方法对数据扩展的兼容性。

### 复杂指令与空间理解

Figure 8 展示了不同指令长度下的性能对比。在短指令（1-50 词）场景，JanusVLN 与 StreamVLN 表现接近；但当指令长度增至 400-550 词时，StreamVLN 的 SR 降至接近零，而 JanusVLN 仍保持稳健性能。这归因于双隐式记忆的定长压缩特性——无论历史多长，记忆规模恒定，避免了显式历史帧方法的信息过载。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_RnuB0Nlbd5/figures/015_Figure_8.jpg]]
*Figure 8: Performance on various instruction lengths/complexity*

Figure 7 的空间理解任务分析进一步证实：在需要深度感知、3D 方位判断、相对定位的任务子集上，JanusVLN 相比 NaVILA 和 StreamVLN 的优势更为显著。真实世界实验（Figure 6）中，JanusVLN 在空间理解任务上比无空间记忆变体提升 23.6%，验证了空间几何记忆在真实场景中的迁移能力。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_RnuB0Nlbd5/figures/014_Figure_7.jpg]]
*Figure 7: Performance on spatial understanding tasks*

### 失败模式分析

Figure 9 揭示了主要的失败模式：当 agent 偏离最优轨迹时，模型难以有效纠错，错误会逐步累积。论文明确指出，有限的偏差轨迹数据不足以训练鲁棒的恢复策略。此外，空间记忆缺乏真实尺度信息，导致距离估计不准确，可能引发过早停止。这些失败模式指向两个开放问题：**如何在有限偏差数据下实现鲁棒纠错，以及如何将真实世界尺度融入隐式空间记忆**。



## 定位与知识库关联

### 1. 方法谱系：从显式语义记忆到双隐式神经记忆

JanusVLN 的核心定位是**将 VLN 的记忆范式从显式语义记忆推进到解耦的双隐式神经记忆**，其谱系可沿两条轴线梳理：记忆表示方式和空间信息利用方式。

#### 1.1 记忆表示方式的演进

传统 VLN 方法的历史信息管理可分为三类，JanusVLN 在每一类上都做出了根本性改变：

- **文本认知地图方法**：以 **MapNav**（Zhang et al., ACL 2025）为代表，将历史观测压缩为文本形式的语义认知地图。这类方法的瓶颈在于文本压缩不可避免地丢失细粒度空间信息，且地图随轨迹增长而膨胀。
- **全历史帧方法**：以 **NaVILA**（Cheng et al., RSS 2025）和 **StreamVLN**（Wei et al., arXiv 2025）为代表，保留完整的历史帧序列作为显式记忆。其瓶颈是计算冗余（每步需重新处理全部历史帧）和记忆膨胀（序列越长，推理开销越大）。
- **JanusVLN 的隐式记忆**：将历史信息建模为**固定大小的 KV 缓存**——不是存储原始帧，而是存储经深度神经网络处理后的键值对。记忆大小不随轨迹长度增长，且支持增量更新，仅保留初始窗口和滑动窗口的 KV。

这一转变的因果机制是：显式记忆迫使模型在每一步重复编码历史帧（或重新读取文本地图），而隐式记忆将“已处理的理解”缓存下来，新帧通过交叉注意力直接检索历史上下文，消除了重复计算。

#### 1.2 空间信息利用方式的演进

在空间理解维度上，JanusVLN 的谱系位置更为独特：

- **仅 2D 语义编码器**：主流 MLLM 导航方法（NaVILA、StreamVLN、**Uni-NaVid** Zhang et al., RSS 2025）依赖 CLIP 等 2D 视觉编码器，这些编码器缺乏 3D 空间推理能力。
- **外部 3D 数据辅助**：**g3D-LF**（Wang & Lee, CVPR 2025）等方法引入深度数据增强空间理解，但需要额外的传感器输入。
- **JanusVLN 的 3D 先验注入**：通过引入 **VGGT**（Wang et al., 2025a）——一个预训练的前馈 3D 视觉几何基础模型——从单目 RGB 视频中直接提取空间几何 token。VGGT 在像素到 3D 点云对上预训练，提供了 2D 编码器不具备的 3D 结构先验。

关键洞察在于**解耦而非替代**：JanusVLN 保留语义编码器处理视觉语义，同时并行引入空间几何编码器处理 3D 结构，两者通过加权 MLP 投影融合（λ=0.2），而非简单拼接或替换。消融实验（Table 4）证实，将 VGGT 替换为 DINOv2 或 SigLIP 2 等 2D 编码器，或使用随机初始化的 VGGT，均无显著提升，说明**预训练的 3D 几何先验是不可或缺的**。

### 2. 适用边界

#### 2.1 输入模态边界

JanusVLN 设计为**仅使用单目 RGB 视频**，无需全景图、里程计或深度数据。在 R2R-CE 和 RxR-CE 基准上，它在输入信息少于诸多依赖全景/深度的基线方法的情况下仍取得最优（Table 1, Table 2），体现了数据效率优势。但这也意味着其性能上限受限于单目 RGB 所能提供的几何信息——VGGT 的 3D 重建精度在遮挡或纹理稀疏场景下可能下降。

#### 2.2 训练数据边界

JanusVLN*（无额外数据）在 R2R-CE Val-Unseen 上达到 52.8 SR，已超越部分使用额外数据的方法。加入 ScaleVLN 和 DAgger 数据后进一步提升至 60.5 SR（Table 8）。值得注意的是，其训练数据量远少于 NaVILA 和 StreamVLN，表明双隐式记忆范式具有较高的数据效率。

#### 2.3 推理效率边界

缓存记忆机制在序列长度 48 帧时性能饱和（Table 5），继续增加窗口大小收益递减。相比原始 VGGT，缓存记忆使推理时间减少 69-90%（32 帧时 149 ms vs 1549 ms），但 VGGT 在 48 帧时即出现 48G GPU 内存溢出，而 JanusVLN 仅边际增长（Figure 3）。

### 3. 局限与已知失效模式

根据论文的失败案例分析（Figure 9）和消融实验，JanusVLN 存在以下明确局限：

1. **错误恢复能力不足**：当 agent 偏离最优轨迹时，模型难以有效纠错，导致错误累积。有限的偏差轨迹训练数据不足以实现鲁棒的恢复策略。这是当前 VLN 方法的共性难题，JanusVLN 的隐式记忆并未从根本上解决这一问题。

2. **距离估计不准确**：空间记忆缺乏真实尺度信息，VGGT 预测的点云和深度是相对尺度，导致 agent 可能过早停止或错过目标。Figure 6 的真实世界实验中，无空间记忆变体在空间理解任务上性能下降 23.6%，但即便有空间记忆，绝对距离判断仍不可靠。

3. **融合策略较为简单**：当前采用加权加法融合（λ=0.2），Table 7 显示 CrossAttn 融合略逊于加权加法，说明更复杂的跨模态融合方法仍有探索空间，但当前方案已是实验最优。

4. **复杂指令下的性能衰减**：Figure 8 显示 JanusVLN 在 400-550 词指令上性能保持，而 StreamVLN 降为零，体现了双隐式记忆的优势。但 JanusVLN 自身在极长指令下仍有衰减趋势，说明语义记忆的容量或检索机制可能成为新瓶颈。

### 4. 开放问题

1. **真实尺度融入**：如何将真实世界尺度信息融入隐式空间记忆，以改善距离估计和停止策略？是否需要引入额外的度量深度监督或 SLAM 先验？

2. **鲁棒错误恢复**：在有限偏差轨迹数据下，能否通过在线学习或记忆回滚机制实现鲁棒的导航错误恢复？双隐式记忆的定长窗口设计是否反而限制了长程纠错能力？

3. **跨任务泛化**：双隐式记忆范式能否推广至其他具身任务（如物体目标导航、移动操作）？空间几何记忆在这些任务中是否同样关键？

4. **自适应窗口配置**：滑动窗口大小（当前 48 帧）和初始化帧数量（当前 8 帧）的最优配置是否应随场景复杂度或指令长度自适应调整？

5. **更丰富的 3D 先验**：是否可以通过引入语义点云或 3D 场景图等更丰富的 3D 先验进一步提升空间理解？VGGT 的几何 token 是否已经饱和，还是存在信息瓶颈？



## 原文 PDF

![[paperPDFs/ICLR_2026/JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Implicit_Memory_for_Vision_Language_Navigation.pdf]]

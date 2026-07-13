---
title: "Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/Matrix-Game_2.0:_An_Open-Source,_Real-Time,_and_Streaming_Interactive_World_Model.pdf"
project_link: https://matrix-game-v2.github.io/
code_link: https://github.com/SkyworkAI/Matrix-Game
aliases:
- MG20
- MG20OSRTSIWM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将双向扩散教师模型通过 ODE 轨迹采样初始化为因果学生模型，并结合 Self-Forcing 蒸馏与 KV 缓存机制，实现少步因果自回归生成；同时构建大规模精确标注的交互数据管道，确保帧级动作可控性。
primary_logic: 通过因果架构、少步蒸馏与 KV 缓存解耦了实时性与长时一致性的矛盾，并利用高精度数据生产管道保证了帧级交互的控制精度，从而首次在复杂场景下实现 25 FPS 的流式交互世界模型。
claims:
- "在 Minecraft 场景上，Matrix-Game 2.0 的图像质量与键盘控制准确率均远超 Oasis（Image Quality: 0.61 vs 0.27; Keyboard Acc.: 0.91 vs 0.73）。"
- 在 Wild 场景上，Matrix-Game 2.0 的图像质量超过 YUME（0.67 vs 0.65），并展现出更强的泛化能力与实时性。
- 在单块 H100 GPU 上，通过组合加速技术，帧率达到 25.15 FPS，满足流式生成要求。
- Minecraft Scenes 上 Image Quality = 0.61
---

# Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model

> [!tip] 核心洞察
> 通过因果架构、少步蒸馏与 KV 缓存解耦了实时性与长时一致性的矛盾，并利用高精度数据生产管道保证了帧级交互的控制精度，从而首次在复杂场景下实现 25 FPS 的流式交互世界模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | Matrix-Game 2.0：一个开源的、实时的、流式交互世界模型 |
| 英文题名 | Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2508.13009) · [Project](https://matrix-game-v2.github.io/) · [HuggingFace](https://huggingface.co/Skywork/Matrix-Game-2.0) · [Code](https://github.com/SkyworkAI/Matrix-Game) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Matrix-Game 2.0 |
| Dataset | Minecraft Scenes, Wild Scenes, Speed |

> [!tip] 效果简介
> - Minecraft Scenes 上，Image Quality 0.61 vs 0.27 (Oasis) (+0.34)；Keyboard Accuracy 0.91 vs 0.73 (Oasis) (+0.18)。
> - Wild Scenes 上，Image Quality 0.67 vs 0.65 (YUME) (+0.02)。
> - Speed (H100 GPU) 上，FPS 25.15 vs N/A。

## 概要

交互世界模型旨在根据用户输入实时生成可交互的视频流，其核心挑战在于同时满足**实时性**与**长时一致性**。现有方法普遍依赖双向注意力机制与高步数扩散去噪，导致生成延迟过高；而自回归范式下的误差累积又严重制约了长序列的视觉质量。Matrix-Game 2.0 针对这一瓶颈，提出了一套从数据生产到模型推理的完整解决方案。

该工作的核心思路可归纳为三个相互耦合的因果调控节点：**① 因果架构与少步蒸馏**——将双向扩散教师模型通过 ODE 轨迹采样初始化为因果学生模型，结合 Self-Forcing 蒸馏与 KV 缓存机制，在仅需 3–4 步去噪的条件下实现因果自回归生成；**② 高精度帧级交互数据管道**——基于 Unreal Engine 和 GTA5 构建自动化数据采集系统，生成约 1200 小时、标注精度超过 99% 的交互视频，确保模型对鼠标与键盘动作的帧级可控性；**③ 动作注入模块**——将连续鼠标值经 MLP 与时序自注意力注入潜变量，离散键盘值通过交叉注意力与 RoPE 编码实现条件控制。

在实验验证上，Matrix-Game 2.0 在 Minecraft 场景下的图像质量与键盘控制准确率分别达到 0.61 和 0.91，显著优于 Oasis（0.27 与 0.73）；在 Wild 场景下图像质量（0.67）亦超越 YUME（0.65），并展现出更强的泛化能力。通过组合 Wan2.1-VAE 缓存、动作模块仅在 DiT 前半部分注入、以及将去噪步数从 4 步降至 3 步等加速技术，该方法在单块 H100 GPU 上实现了 **25.15 FPS** 的流式生成帧率，首次在复杂交互场景下满足实时性要求。

**方法定位**：Matrix-Game 2.0 属于因果自回归扩散世界模型，其架构衍生自 Wan I2V 设计，移除了文本分支并嵌入帧级动作模块。与 Oasis（Decart, 2024）等实时交互基线相比，其关键差异在于通过蒸馏实现了少步因果生成；与 YUME（Mao et al., 2025）等交互世界生成模型相比，其优势在于实时流式能力与更精确的动作控制。该方法目前的主要局限包括：对训练分布外场景的泛化不足（可能产生过饱和或退化结果）、输出分辨率限制在 352×640、以及缺乏显式长期记忆机制。



交互世界模型旨在根据用户输入实时生成可控的视频流，为游戏模拟、具身智能和虚拟世界构建提供核心能力。近年来，视频生成模型取得了显著进展，但在构建真正可用的交互世界模型时，仍面临三个根本性瓶颈。

**实时性与生成质量的矛盾。** 现有交互世界模型普遍依赖双向注意力机制与高步数去噪过程（如 50 步扩散），导致单帧生成耗时过长，无法满足实时交互需求。与此同时，自回归生成范式虽然天然适合流式输出，但在长序列生成中存在显著的误差累积问题——早期帧的微小偏差会沿时间轴放大，最终导致画面崩溃或内容失真。这一矛盾使得现有方法要么牺牲实时性换取质量，要么在实时条件下无法维持分钟级的时间一致性。

**动作控制精度不足。** 交互世界模型的核心价值在于帧级的精确可控性，即用户输入的每一个键盘或鼠标动作都应即时、准确地反映在生成画面中。然而，现有方法大多缺乏帧级交互输入机制，仅依赖高级语义控制信号（如文本描述），无法实现细粒度的动作-画面映射。这从根本上限制了交互世界模型在游戏操控、驾驶模拟等场景中的实用性。

**高质量交互数据的稀缺。** 训练帧级可控的视频生成模型需要大规模、精确标注的交互视频数据，即每一帧画面必须与当时的键盘、鼠标输入严格对齐。这类数据在现实中极为稀缺，手工采集不仅成本高昂，标注精度也难以保证。数据瓶颈直接制约了模型对复杂交互模式的学习能力。

针对上述问题，**Matrix-Game 2.0** 提出了系统性的解决方案。其核心洞察在于：通过因果架构、少步蒸馏与 KV 缓存机制，可以解耦实时性与长时一致性的矛盾；同时，利用高精度自动化数据生产管道，能够在复杂场景下首次实现 25 FPS 的流式交互世界模型。在 Minecraft 场景上，Matrix-Game 2.0 的图像质量与键盘控制准确率分别达到 0.61 和 0.91，远超同期实时基线 **Oasis**（Decart, 2024）的 0.27 和 0.73（Table 1）；在 Wild 场景上，图像质量以 0.67 超过 **YUME**（Mao et al., 2025）的 0.65，并展现出更强的泛化能力与实时性（Table 2）。



## 核心方法与创新机理

Matrix-Game 2.0 的核心创新在于通过**因果架构、少步蒸馏与高精度交互数据**三个维度的协同设计，首次在复杂场景下实现了 25 FPS 的流式交互世界模型，解决了现有方法“实时性不足”与“长时一致性差”的双重瓶颈。

### 因果自回归架构替代双向扩散

现有交互世界模型（如 Oasis、YUME）普遍采用双向注意力机制，依赖完整上下文进行多步去噪生成，无法满足实时交互的因果约束。Matrix-Game 2.0 将基础模型从双向扩散 Transformer 重构为**因果自回归扩散 Transformer**（Causal DiT），并引入 KV 缓存机制（滑动窗口大小 6 帧），使模型仅基于历史帧和当前动作预测未来帧，从根本上解耦了生成质量与推理延迟的矛盾（见 Figure 8）。

### 少步蒸馏实现实时推理

传统扩散模型需要 50 步以上的去噪过程，而 Matrix-Game 2.0 通过两阶段蒸馏将推理步数压缩至 3–4 步：首先沿 ODE 轨迹采样初始化因果学生模型（见 Figure 9），随后采用 **Self-Forcing 蒸馏**对齐学生与教师模型的分布（见 Figure 10）。这一设计在保持生成质量的同时，将单帧推理开销降至实时水平。配合 Wan2.1-VAE 缓存、仅在 DiT 前半部分注入动作模块等组合加速技术，最终在单块 H100 GPU 上达到 25.15 FPS（Table 3）。

### 帧级动作注入与高精度数据管道

为实现精确的交互控制，Matrix-Game 2.0 设计了帧级动作注入模块：连续鼠标值经 MLP 与时序自注意力处理后直接拼接到潜变量；离散键盘值则通过交叉注意力注入，并使用 **RoPE 编码**（Rotary Positional Encoding）替代传统正弦位置编码，增强对离散动作的建模能力。这一设计的关键支撑是**大规模自动化数据生产管道**——基于 Unreal Engine 的导航网格路径规划与强化学习代理（PPO），以及 GTA5 的毫秒级输入-渲染同步记录系统，共生成了约 1200 小时、标注精度超 99% 的帧级交互视频数据，解决了此前交互数据稀缺且标注不准的根本问题。

### 与基线的关键差异

| 维度 | 基线方法 | Matrix-Game 2.0 |
|------|----------|-----------------|
| 模型架构 | 双向扩散 Transformer / 非因果自回归 | 因果自回归 DiT + KV 缓存 |
| 推理效率 | 多步去噪（如 50 步） | 少步蒸馏推理（3–4 步） |
| 动作条件 | 无帧级交互输入或仅高级控制 | 帧级鼠标+键盘注入，键盘使用 RoPE |
| 数据生产 | 稀缺、标注不准的交互视频 | 自动化管道，1200 小时，精度 >99% |

这些 changed slots 共同构成了 Matrix-Game 2.0 相对于 Oasis（Decart, 2024）和 YUME（Mao et al., 2025）的核心优势：在 Minecraft 场景上，图像质量从 0.27 提升至 0.61，键盘控制准确率从 0.73 提升至 0.91（Table 1）；在 Wild 场景上，图像质量以 0.67 超越 YUME 的 0.65，并展现出更强的泛化能力与实时性（Table 2）。



Matrix-Game 2.0 的整体框架围绕一个核心目标构建：**在保持高质量视觉生成与精确动作可控性的前提下，实现 25 FPS 的流式交互视频生成**。为此，框架将一条大规模高精度数据生产管道与一个因果自回归扩散模型深度耦合，形成从数据采集到实时推理的闭环系统。

### 框架总览

整个 pipeline 由两大阶段构成：**数据生产阶段**与**模型训练/推理阶段**（见 Figure 2）。数据生产阶段基于 Unreal Engine 和 GTA5 构建自动化采集系统，输出帧级精确标注的交互视频数据；模型阶段则以因果扩散 Transformer 为核心，通过少步蒸馏与 KV 缓存机制实现实时自回归生成。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/002_Figure_2.jpg]]
*Figure 2: Pipelines of Matrix-Game 2.0*

### 数据生产管道

数据管道是整个框架的基础设施，其设计目标是解决交互世界模型训练中长期存在的**数据稀缺与标注不准**两大瓶颈。管道包含两条独立但互补的采集线路：

**Unreal Engine 线路**（见 Figure 3）构建了基于导航网格的路径规划系统，驱动 NPC 在多样化场景中进行动态自适应移动。为提高轨迹质量，系统集成了基于 PPO 的强化学习训练框架，奖励函数设计为：

$$R _ { t } = \alpha \cdot R _ { c o l l i s i o n } + \beta \cdot R _ { e x p l o r a t i o n } + \gamma \cdot R _ { d i v e r s i t y }$$

该奖励函数同时优化碰撞避免、探索效率与轨迹多样性。为获得精确的帧级动作标注，系统实现了毫秒级键盘输入与渲染帧的同步记录：

$$\mathrm { I n p u t } _ { \mathrm { f r a m e } _ { i } } = ( \{ k _ { 1 } , k _ { 2 } , . . . , k _ { n } \} , \mathrm { t i m e s t a m p } _ { i } )$$

同时通过速度阈值过滤无效运动样本：

$${ \mathrm { v a l i d i t y } } = { \left\{ \begin{array} { l l } { 1 } & { { \mathrm { i f ~ } } \left| | { \vec { v } } | \right| > \epsilon } \\ { 0 } & { { \mathrm { o t h e r w i s e } } } \end{array} \right. }$$

管道支持多线程执行，在单块 RTX 3090 GPU 上即可实现双流并发数据生产，最终整体标注精度超过 99%，相机旋转精度提升 50 倍。

**GTA5 线路**（见 Figure 6）针对驾驶场景，通过计算每帧相机位置实现精确标注：

$$\mathrm{Camera}_{position} = \mathrm{Vehicle}_{position} + \mathrm{offset} \times \mathrm{rotation}$$

两条线路合计产出约 **1200 小时**的高精度帧级标注交互视频数据，为后续模型训练提供了坚实基础。

### 模型架构

Matrix-Game 2.0 的模型架构（见 Figure 8）从 Wan I2V 设计衍生而来，但做了关键性改造：**完全移除文本分支**，使模型仅从视觉内容和对应动作中预测后续帧。架构由以下核心模块串联组成：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/008_Figure_8.jpg]]
*Figure 8: Overview of Matrix-Game 2.0 Architecture. The foundation model is derived from the Wan [44] I2V design. By removing the text branch and adding action modules as in Matrix-Game [57], the model predicts next frames only from visual contents and corresponding actions*

1. **3D Causal VAE**：对原始视频进行时空压缩，空间下采样 8×8，时间下采样 4×，将高维视频数据映射到低维潜空间。
2. **CLIP Image Encoder**：将参考图像编码为条件表示，为生成提供初始视觉上下文。
3. **Action Injection Module**：这是实现帧级交互控制的关键模块。连续鼠标动作通过 MLP 层与时序自注意力层直接拼接到输入潜变量中；离散键盘动作则通过交叉注意力层注入，并使用 **RoPE 编码**替代传统的正弦-余弦位置嵌入。
4. **Causal DiT Blocks**：因果扩散 Transformer 主体，执行自回归视频潜变量生成。因果注意力机制确保每帧生成仅依赖当前及历史信息，这是实现流式推理的架构基础。
5. **KV-cache Mechanism**：维护固定长度的近期潜变量与动作嵌入缓存（滑动窗口），支持高效自回归生成。滚动缓存实现自动管理，当超出容量时驱逐最旧 token，理论上支持无限长度生成。

### 训练策略：从双向教师到因果学生

框架的训练策略是解决实时性瓶颈的核心创新。传统扩散模型依赖双向注意力与高步数去噪，无法满足实时交互需求。Matrix-Game 2.0 采用**两阶段蒸馏**策略：

**阶段一：学生初始化**（见 Figure 9）。从预训练的双向扩散教师模型出发，沿 ODE 轨迹采样，使用回归损失训练因果学生模型：

$$\mathcal { L } _ { \mathrm { s t u d e n t } } = \mathbb { E } _ { x , t ^ { i } } \left\| G _ { \phi } \left( \left\{ x _ { t ^ { i } } ^ { i } \right\} _ { i = 1 } ^ { L } , \left\{ c ^ { i } \right\} _ { i = 1 } ^ { L } , \left\{ t ^ { i } \right\} _ { i = 1 } ^ { L } \right) - \left\{ x _ { 0 } ^ { i } \right\} _ { i = 1 } ^ { L } \right\| ^ { 2 }$$

该阶段将双向教师的知识迁移到因果架构的学生模型中，为后续蒸馏提供稳定起点。

**阶段二：Self-Forcing 蒸馏**（见 Figure 10）。采用 Self-Forcing 训练范式，通过自条件生成对齐学生与教师的分布，有效缓解自回归生成中的误差累积问题，同时将推理步数压缩至 3-4 步。

### 输入输出流

推理时，系统接收**参考图像**与**实时动作序列**（鼠标连续值 + 键盘离散值）作为输入。3D Causal VAE 与 CLIP Encoder 将图像编码为条件表示，动作注入模块将帧级动作融入潜变量，因果 DiT 块在 KV 缓存支持下逐帧自回归生成潜变量，最后通过 VAE 解码器还原为视频帧。整个流程在单块 H100 GPU 上达到 25.15 FPS 的吞吐量，满足流式生成要求。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Our Data Production Pipeline based on Unreal Engine*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/006_Figure_6.jpg]]
*Figure 6: Overview of Our GTA5 Interactive Data Recording System*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/004_Figure_4.jpg]]
*Figure 4: An example for Our Navigation System*



### 3D Causal VAE：时空压缩瓶颈

Matrix-Game 2.0 的视频生成管道以 **3D Causal VAE** 作为第一道压缩关卡。该模块对原始视频数据同时执行空间与时间维度的下采样——空间方向压缩 $8\times8$ 倍，时间方向压缩 $4$ 倍。因果性约束确保编码过程不窥视未来帧，为后续因果自回归生成奠定基础。压缩后的潜变量进入扩散变换器，大幅降低了计算开销。

### 动作注入模块：帧级交互控制

模型通过独立的动作注入模块实现帧级鼠标（连续值）与键盘（离散值）的条件控制，这是区别于纯视觉生成模型的关键设计。

- **鼠标动作**：连续鼠标信号直接拼接到输入潜变量表示中，经 MLP 层后送入时序自注意力层，与视觉特征融合。
- **键盘动作**：离散键盘输入采用 **旋转位置编码（Rotary Positional Encoding, RoPE）** 替代传统的正弦-余弦位置嵌入，通过交叉注意力层由融合后的视觉特征进行查询。这种设计使模型能够区分并响应不同的按键组合。

值得注意的是，Matrix-Game 2.0 完全移除了文本分支，仅从图像内容与对应动作中预测下一帧，迫使模型专注于学习空间结构与动态模式。

### 因果扩散变换器与 KV 缓存

模型主体基于 **因果扩散变换器（Causal DiT Blocks）**，从 Wan I2V 架构衍生而来。因果注意力掩码保证了时间维度的自回归特性——每帧只能关注当前及历史帧。

为支撑流式长序列生成，模型引入了 **KV 缓存机制**。该机制维护一个固定长度的滑动窗口缓存，存储近期的潜变量与动作嵌入。滚动缓存实现自动内存管理：当缓存超出容量时，最旧的 token 被逐出，从而支持理论上的无限长度生成。消融实验表明，缓存窗口大小设为 **6 帧** 时，能在上下文信息保留与误差纠正能力之间取得最优平衡——更大的窗口会导致长序列中出现伪影，而过小的窗口则削弱时序一致性。

### 蒸馏训练：从双向教师到因果学生

实时推理的核心瓶颈在于传统扩散模型的多步去噪。Matrix-Game 2.0 通过两阶段蒸馏将双向教师模型转化为少步因果学生模型。

**第一阶段：基于 ODE 轨迹的学生初始化。** 从双向教师模型中沿最优 ODE 轨迹采样，让学生模型直接回归干净样本。其损失函数为：

$$\mathcal{L}_{\mathrm{student}} = \mathbb{E}_{x, t^i} \left\| G_{\phi} \left( \left\{ x_{t^i}^i \right\}_{i=1}^{L}, \left\{ c^i \right\}_{i=1}^{L}, \left\{ t^i \right\}_{i=1}^{L} \right) - \left\{ x_0^i \right\}_{i=1}^{L} \right\|^2$$

其中 $G_{\phi}$ 为学生生成器，$x_{t^i}^i$ 为第 $i$ 帧在时间步 $t^i$ 的噪声潜变量，$c^i$ 为对应条件（动作嵌入），$x_0^i$ 为干净潜变量目标。该阶段为后续蒸馏提供了稳定的初始化起点，避免了从随机权重开始的训练不稳定问题。

**第二阶段：基于 DMD 的 Self-Forcing 蒸馏。** 采用 Self-Forcing 训练范式，学生在自条件生成过程中逐步对齐教师模型的分布。这一方法有效缓解了自回归生成中的误差累积问题，同时将去噪步数压缩至 3-4 步，为 25 FPS 的实时生成提供了效率保障。

### 组合加速技术

为进一步提升推理速度，模型采用了三项组合加速策略：集成 Wan2.1-VAE 的缓存架构、仅在 DiT 块的前半部分加入动作模块、将去噪步数从 4 步减为 3 步。在单块 H100 GPU 上，这些技术将帧率推至 25.15 FPS，同时保持生成质量指标基本持平。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/009_Figure_9.jpg]]
*Figure 9: Causal Student Model Initialization via ODE Trajectories. The proposed initialization method stabilizes subsequent distillation training by deriving a few-step causal student model from the bidirectional teacher model through optimal ODE trajectory sampling*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/010_Figure_10.jpg]]
*Figure 10: Overview of Causal Diffusion Model Training via Self-Forcing. The distillation process aligns the student model’s distributions with the teacher model’s through self-conditioned generation. This approach effectively mitigates error accumulation while maintaining the generation quality*



## 实验与关键发现

### 核心实验结果

Matrix-Game 2.0 在两个场景设置下进行了定量与定性评估：Minecraft 场景（与 **Oasis** (Decart, 2024) 对比）和 Wild 场景（与 **YUME** (Mao et al., 2025) 对比）。评估指标涵盖图像质量（Image Quality）和键盘控制准确率（Keyboard Accuracy）。

**Minecraft 场景。** 如表 1 所示，Matrix-Game 2.0 在图像质量上达到 0.61，而 Oasis 仅为 0.27，提升幅度达 +0.34；键盘准确率从 0.73 提升至 0.91（+0.18）。这一结果直接验证了因果架构与少步蒸馏在保持帧级动作可控性方面的关键作用——Oasis 受限于非因果自回归生成，无法在长序列中维持精确的动作响应，而 Matrix-Game 2.0 通过帧级键盘注入模块（含 RoPE 编码）和 Self-Forcing 蒸馏，有效抑制了误差累积。定性对比（图 11）进一步显示，Oasis 在长交互生成中会出现明显的视觉退化，而 Matrix-Game 2.0 保持了更稳定的场景结构和纹理细节。

**Wild 场景。** 在更开放的 Wild 场景上（表 2），Matrix-Game 2.0 的图像质量达到 0.67，略高于 YUME 的 0.65（+0.02）。虽然数值优势相对温和，但结合定性结果（图 12）来看，Matrix-Game 2.0 展现出更强的泛化能力：在 YUME 难以处理的场景中，本模型仍能生成结构合理、动作响应准确的交互视频。这得益于大规模精确标注的数据管道——约 1200 小时、标注精度超 99% 的交互视频数据为因果学生模型提供了高质量的训练信号。

**实时性验证。** 在单块 H100 GPU 上，通过组合加速技术，Matrix-Game 2.0 的帧率达到 25.15 FPS（表 3），满足流式交互的实时性要求。这是首个在复杂场景下实现 25 FPS 的因果自回归交互世界模型。

### 消融研究

**KV 缓存窗口大小。** 图 16 展示了不同 KV 缓存窗口大小对长序列生成质量的影响。实验表明，较大的缓存窗口会导致长序列中出现伪影（artifact），而较小的窗口则能在视觉质量与内容保真度之间取得平衡。经验性研究确定缓存大小为 6 帧时效果最优——这一设置既保留了足够的上下文信息以维持时序一致性，又具备及时纠正误差的能力。

**组合加速技术。** 表 3 系统性地分析了各项加速技术的贡献。具体策略包括：(1) 集成高效的 Wan2.1-VAE 架构并配合缓存机制；(2) 仅在 DiT 块的前半部分加入动作模块，减少计算开销；(3) 将去噪步数从 4 步进一步压缩至 3 步。这些技术的组合在保持生成质量指标可比较的前提下，将吞吐量提升至 25 FPS，实现了实时视频生成。需要指出的是，去噪步数的减少是建立在 ODE 轨迹初始化和 Self-Forcing 蒸馏的基础之上——学生模型在初始化阶段已经学习了教师模型的分布结构，因此能够在极少数步数内完成生成。

### 失败模式与局限性

尽管 Matrix-Game 2.0 在主要基准上表现优异，但仍存在以下已知失败模式：

1. **域外泛化不足。** 当输入场景显著偏离训练分布时，模型可能产生过饱和或退化的结果（图 17）。这是因果学生模型从特定数据域蒸馏的固有限制——教师模型的分布覆盖范围直接决定了学生的泛化边界。

2. **分辨率限制。** 当前输出分辨率固定在 352×640，无法生成高清视频。这源于 3D Causal VAE 的空间下采样策略与实时性约束之间的权衡。

3. **长序列误差累积。** 尽管 KV 缓存和 Self-Forcing 蒸馏显著缓解了误差累积问题，但在极长视频生成中仍可能出现内容漂移。模型缺乏显式的长期记忆机制，无法在保持实时性的同时检索远距离历史信息。

4. **物理模拟精度。** 在 GTA5 驾驶场景（图 14）和 TempleRun 跑酷场景（图 15）中，模型能够生成视觉合理的交互视频，但复杂物理交互（如碰撞响应）的保真度受限于训练数据的覆盖范围和蒸馏过程中的分布偏移。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/012_Table_1.jpg]]
*Table 1: Quantitative Comparisons on Minecraft Scene Generations*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/014_Table_2.jpg]]
*Table 2: Quantitative Comparisons on Wild Scene Generations*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/016_Table_3.jpg]]
*Table 3: Quantitative Comparisons of Different Acceleration Techniques. While maintaining comparable generation quality metrics, our combined acceleration techniques achieve 25 FPS throughput, enabling on-the-fly video generation*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/019_Figure_16.jpg]]
*Figure 16: Qualitative Comparison on Different Local Size for KV-cache. Larger local size cause artifacts in long sequences while smaller local size can keep a balance between visual quality and content fidelity*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_13009/figures/020_Figure_17.jpg]]
*Figure 17: Bad cases. Matrix-Game-V2 sometimes fails when handling out-of-domain scenes, like producing over-saturated (left) or degraded (right) results*



## 定位与知识库关联

### 1. 基线比较与核心差异化

Matrix-Game 2.0 的定位是**实时、流式、帧级可控的交互世界模型**，其核心对手是两类生成范式：基于双向扩散的交互生成模型，以及基于自回归的非因果世界模型。

**与 Oasis（Decart, 2024）的对比。** Oasis 是面向 Minecraft 场景的实时交互世界模型，但其底层依赖双向注意力与高步数去噪，导致实时性受限，且自回归生成过程中误差累积严重。Matrix-Game 2.0 在相同 Minecraft 场景上，图像质量从 0.27 提升至 0.61，键盘控制准确率从 0.73 提升至 0.91（Table 1）。这一差距的因果瓶颈在于：Oasis 的双向架构天然不适合流式自回归推理，而 Matrix-Game 2.0 通过因果架构与 KV 缓存从架构层面消除了这一矛盾。

**与 YUME（Mao et al., arXiv 2025）的对比。** YUME 是面向 Wild 场景的交互世界生成模型。在图像质量指标上，Matrix-Game 2.0 以 0.67 略优于 YUME 的 0.65（Table 2），但更关键的差异在于泛化能力与实时性——YUME 未针对流式推理进行架构优化，难以在单 GPU 上达到 25 FPS 的实时交互帧率。

**方法谱系中的位置。** Matrix-Game 2.0 继承了 Wan（I2V 设计）作为基础模型骨架，并沿用了 Matrix-Game 的动作注入模块设计。其核心创新在于将双向扩散教师模型通过 ODE 轨迹采样初始化为因果学生模型，并结合 Self-Forcing 蒸馏实现少步因果自回归生成。这一技术路线处于**扩散蒸馏**与**因果世界模型**的交叉点，区别于传统的逐帧扩散生成（如 Sora、Genie-2）和纯自回归 Transformer 生成（如 GameNGen）。

### 2. 适用边界

**有效域。** 模型在以下条件下表现最佳：
- 训练数据覆盖的场景类型：基于 Unreal Engine 的室内/室外导航场景、GTA5 驾驶场景、Minecraft 风格场景。
- 动作控制模态：帧级键盘（离散值，经 RoPE 编码后通过交叉注意力注入）和鼠标（连续值，经 MLP 与时序自注意力注入）。
- 推理硬件：单块 H100 GPU，通过组合加速技术（Wan2.1-VAE 缓存、仅在前半部分 DiT 块中启用动作模块、去噪步数从 4 步减至 3 步）达到 25.15 FPS（Table 3）。
- 输出分辨率：352×640，这是当前架构的硬性限制。

**失效域。** 以下场景需要谨慎：
- **分布外场景**：对训练分布外的输入，模型可能产生过饱和或退化的结果（Figure 17）。这是当前数据驱动方法的共性瓶颈，需要手动验证具体场景的可用性。
- **极长视频生成**：尽管 KV 缓存窗口（6 帧）在上下文保留与误差纠正之间取得了平衡（Figure 16），但超过分钟级的生成仍可能出现误差累积。
- **高精度物理模拟**：模型学习的是视觉层面的动态模式，而非显式的物理规律。在需要精确碰撞检测或力学反馈的场景中，控制精度可能下降。
- **其他交互模态**：当前仅支持键盘与鼠标，手柄、语音等模态需要额外的注入模块设计。

### 3. 局限与开放问题

**已知局限。**
1. **分辨率瓶颈**：输出限制在 352×640，无法生成高清视频。这源于 3D Causal VAE 的压缩率（空间 8×8，时间 4×）与当前模型容量的权衡。
2. **域外泛化不足**：数据管道虽覆盖 Unreal Engine 和 GTA5 两类环境，但模型对未见游戏引擎或真实世界场景的泛化能力有限。
3. **缺乏显式长期记忆**：KV 缓存仅保留 6 帧的滑动窗口，无法记忆远距离历史信息。在需要长期状态追踪的交互任务中（如 RPG 游戏的任务状态），这是根本性限制。
4. **蒸馏过程中的分布偏移**：Self-Forcing 蒸馏虽有效缓解误差累积，但学生模型与教师模型之间的分布偏移并未完全消除，在复杂动态场景中可能表现为控制精度的退化。

**开放问题。**
- **规模扩展与域泛化**：通过扩展训练数据域（更多游戏引擎、真实世界视频）和模型规模，能否同时提升域外泛化能力与输出分辨率？这需要在数据生产管道的可扩展性上进行投入。
- **长期记忆机制**：如何集成有效的记忆检索机制（如外部记忆库、分层缓存）以实现长期内容一致性，同时不损失 25 FPS 的实时性能？这是流式世界模型走向实用化的关键。
- **物理真实性的提升**：在更复杂的真实世界物理模拟中，是否需要在蒸馏过程中引入物理约束损失或混合训练策略，以进一步降低分布偏移？
- **多模态交互扩展**：Matrix-Game 2.0 的动作注入模块设计是否可泛化到手柄、语音、甚至自然语言指令？这需要验证交叉注意力机制对异构模态的兼容性。
- **与现有世界模型的系统性比较**：当前仅在 Minecraft 和 Wild 场景上与 Oasis、YUME 进行了对比。与 Genie-2、Sora 等更大规模世界模型在可控交互维度上的公平比较，仍是开放问题——部分原因在于这些模型的交互能力未完全公开或 API 受限。



## 原文 PDF

![[paperPDFs/arxiv_2025/Matrix-Game_2.0:_An_Open-Source,_Real-Time,_and_Streaming_Interactive_World_Model.pdf]]

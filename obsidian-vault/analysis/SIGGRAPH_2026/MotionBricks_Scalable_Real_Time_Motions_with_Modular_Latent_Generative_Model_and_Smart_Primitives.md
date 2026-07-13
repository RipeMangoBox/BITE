---
title: "MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2026
pdf_ref: paperPDFs/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.pdf
code_link: null
project_link: https://nvlabs.github.io/motionbricks
aliases:
- MotionBricks
tags:
- SIGGRAPH_2026
- topic/real_time_motion_synthesis
- topic/latent_motion_generation
- topic/vector_quantization
- topic/character_animation
- topic/real_time_motion_synthesis/general
core_operator: "结构化的多头部潜在标记器与根-姿态解耦策略是关键调节变量，它通过将连续运动特征量化到多个独立码本中，并分离根轨迹和姿态的编码，同时提升模型容量、关键帧控制精度和实时性能。"
primary_logic: "通过将动作生成分解为基于关键帧约束的根轨迹预测和姿态潜在生成，并采用模块化、粗到细的渐进式生成流程，可以在保持2ms延迟、15000 FPS吞吐量的实时效率下，实现高质量、可扩展的零样本动作控制。"
claims:
- "在包含350k动作片段的数据集上，MotionBricks在FID指标上显著优于所有基线方法（FID=1.054）"
- "达到2ms生成延迟和15,000 FPS吞吐量，远超其他生成方法"
- "多头部标记器在总码本容量高达约10^9 tokens时仍继续改善重建损失，而单头基线迅速饱和"
- "通过智能基元接口，模型无需微调即可零样本泛化到导航、物体交互和机器人控制等多种下游任务"
---

# MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives

> [!tip] 核心洞察
> 通过将动作生成分解为基于关键帧约束的根轨迹预测和姿态潜在生成，并采用模块化、粗到细的渐进式生成流程，可以在保持2ms延迟、15000 FPS吞吐量的实时效率下，实现高质量、可扩展的零样本动作控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionBricks：基于模块化潜在生成模型与智能基元的大规模实时动作合成 |
| 英文题名 | MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives |
| 会议/期刊 | SIGGRAPH 2026 |
| Links | [paper](https://doi.org/10.1145/3811334) · [Project](https://nvlabs.github.io/motionbricks) |
| Topic | #topic/real_time_motion_synthesis #topic/latent_motion_generation #topic/vector_quantization #topic/character_animation #topic/real_time_motion_synthesis/general |
| Method | Modular latent generative model, multi-head motion tokenizer, root-pose decoupling, smart primitives |
| Dataset | 350k proprietary motion dataset, LaFAN1-G1, Bones-70k |

> [!tip] 效果简介
> - 350k proprietary dataset 上，FID 为 1.054，对比 MMM (1.153, best among baselines)，变化 0.099 improvement。
> - LaFAN1-G1 上，FID 为 0.891，对比 ClosdDiP (0.903, second best)，变化 0.012 improvement。
> - 350k dataset 上，Latency / Throughput 为 2ms per generation, 15,000 FPS，对比 other generative methods (seconds to minutes)，变化 orders of magnitude faster。

## 概要

**核心问题。** 现有生成式动作合成模型在实时应用中面临双重瓶颈：在严格实时计算约束下，模型质量和可扩展性显著下降，无法以单个模型处理超35万段动作的大规模数据集；同时缺乏统一的精细多模态控制接口，难以同时满足速度命令、风格选择和关键帧等生产级需求。

**核心洞察。** MotionBricks 提出将动作生成分解为基于关键帧约束的根轨迹预测和姿态潜在生成，并采用模块化、粗到细的渐进式生成流程。其关键调节变量是**结构化的多头部潜在标记器**与**根-姿态解耦策略**——通过将连续运动特征量化到多个独立码本中，并分离根轨迹和姿态的编码，同时提升模型容量、关键帧控制精度和实时性能。

**方法定位。** MotionBricks 由四阶段推理流水线构成（Figure 2）：(1) **智能基元**（Smart Primitives）从用户命令或游戏事件生成目标关键帧；(2) **根模块**预测帧间时序和全局根轨迹；(3) **姿态模块**基于掩码令牌预测对多头部潜在姿态令牌建模；(4) **解码器**结合姿态令牌、根轨迹和关键帧约束重构连续全身运动。该方法以动作插值（motion in-betweening）为基础范式，但通过结构化潜在设计和模块化解耦实现了对传统插值基线（如 Cond. In-betweening、Delta-interpolator）和生成式基线（如 MMM、CondMDI、Closd-DiP）的显著超越。

**主要结果。** 在包含350k动作片段的数据集上，MotionBricks 以 **FID=1.054** 显著优于所有基线方法（最佳基线 MMM 为 1.153），同时达到 **2ms 生成延迟**和 **15,000 FPS 吞吐量**，比其他生成方法快数个数量级（Table 3）。在 LaFAN1-G1 数据集上 FID=0.891，优于 ClosdDiP（0.903）；在 Bones-70k 目标达成任务上成功率达 **99.6%**（Table 4）。多头部标记器在总码本容量高达约 10⁹ tokens 时仍持续改善重建损失，而单头基线迅速饱和（Figure 10）。通过智能基元接口，模型无需微调即可零样本泛化到导航、物体交互和机器人控制等多种下游任务（Figure 1, Figure 6, Figure 7）。

**证据强度。** 上述结论由七大类指标（速度、分布、人体评估、多样性、平滑度、物理合理性、精确度）的全面评估支持，人体评估邀请了40名不同背景参与者，所有方法在同一训练集和评估协议下比较。需注意，数据集缺少手指和物体运动数据，稀有动作类别泛化仍有困难，且离散潜在表示在较高重规划频率下会导致 FID 和关键帧误差轻微增加。

### 实时动作合成的规模化困境

在游戏、虚拟现实和机器人等交互式应用中，实时动作合成是一个核心挑战。现代应用要求系统能够以极低延迟（毫秒级）响应用户输入，同时生成高质量、风格多样且物理合理的全身动作。近年来，生成式模型在离线动作合成领域取得了显著进展，但当这些方法被推向实时场景时，一个根本性瓶颈浮现：**模型质量与可扩展性在严格实时计算约束下急剧下降**。

具体而言，现有方法面临双重困境。一方面，基于扩散或自回归的生成式模型虽能产生高质量动作，但其推理延迟通常在秒级甚至分钟级，无法满足实时交互需求。另一方面，当数据集规模从常见的数万段动作扩展到超35万段时，传统生成式模型往往出现性能饱和甚至退化，难以用单一模型有效覆盖如此广泛的运动技能分布。MotionBricks正是在这一背景下，试图打破实时性与规模化之间的固有张力。

### 控制接口的碎片化问题

除计算效率外，生产级动作合成系统还需应对另一关键缺口：**缺乏统一的精细多模态控制接口**。实际应用中，用户需要同时施加多种异质约束——例如，通过速度命令控制导航方向，通过风格标签指定运动表现（如“潜行”、“爬行”），以及通过关键帧精确定义特定时刻的姿态。现有方法通常将这些控制信号割裂处理：基于标签的方法需要为每种任务单独训练模型或微调，而基于关键帧的补间方法则难以灵活融入风格和速度等高层语义。这种碎片化导致系统难以零样本泛化到新的任务组合，增加了工程部署的复杂度。

### 核心动机：从分解到统一

MotionBricks的核心动机源于一个关键洞察：**将动作生成分解为根轨迹预测与姿态潜在生成两个子问题，并采用模块化、粗到细的渐进式生成流程，是实现实时效率与高质量控制统一的关键**。这一设计哲学体现在两个层面：

1. **结构化潜在空间设计**：通过多头部标记器将连续运动特征量化到多个独立码本中，并解耦根轨迹与姿态的编码，既大幅提升了模型容量（总码本容量可达约$10^9$个token），又为关键帧约束的精确注入提供了结构化接口。
2. **智能基元接口**：提出“智能基元”（smart primitives）作为统一的高层控制抽象，将速度命令、风格选择和关键帧约束转化为一致的目标关键帧表示，使单一神经骨干无需微调即可零样本泛化到导航、物体交互和机器人控制等多种下游任务。

这种从“碎片化控制”到“统一基元接口”的转变，以及从“单体生成”到“模块化潜在生成”的架构演进，构成了MotionBricks区别于现有工作的核心动机，也为后续在2ms延迟、15,000 FPS吞吐量下实现大规模高质量动作合成奠定了基础。

## 核心方法与创新机理

MotionBricks 的核心创新在于通过**三个结构性改变**（changed slots），系统性解决了实时动作生成中模型容量、控制精度与计算效率的三角矛盾。这些改变并非孤立的技术点，而是围绕“根-姿态解耦”与“多头部离散潜在空间”两条主线形成协同效应。

### 1. 结构化多头部标记器与根-姿态解耦

传统动作生成模型通常采用单头 VQ-VAE 对包含根轨迹和姿态的联合状态进行编码。这种设计在码本容量增大时迅速饱和，限制了模型对大规模数据集的表征能力。MotionBricks 的标记器设计引入两个关键改变：

- **多头部量化**：将编码器输出的连续潜在嵌入沿特征维度分割为 $K$ 个独立片段，每个片段对应一个专属的离散码本 $\mathcal{E}_k$，通过最近邻查找完成量化：

$$z _ { q } ^ { t } = \left\{ \begin{array} { l } { z _ { q , 1 } ^ { t } } \\ { z _ { q , 2 } ^ { t } } \\ { \vdots } \\ { z _ { q , K } ^ { t } } \end{array} \right\} = \left\{ \begin{array} { l } { \arg \operatorname* { m i n } _ { e _ { 1 } \in \mathcal { E } _ { 1 } } \| z _ { e , 1 } ^ { t } - e _ { 1 } \| _ { 2 } ^ { 2 } } \\ { \arg \operatorname* { m i n } _ { e _ { 2 } \in \mathcal { E } _ { 2 } } \| z _ { e , 2 } ^ { t } - e _ { 2 } \| _ { 2 } ^ { 2 } } \\ { \vdots } \\ { \arg \operatorname* { m i n } _ { e _ { K } \in \mathcal { E } _ { K } } \| z _ { e , K } ^ { t } - e _ { K } \| _ { 2 } ^ { 2 } } \end{array} \right\}$$

这种设计使总码本容量以指数级扩展（可达约 $10^9$ 个 token 组合），而单头基线在相同容量下迅速饱和。消融实验（Fig. 10）证实，多头部标记器在更大码本下持续降低重建损失，且下游 FID 与关键帧误差更优。

- **根-姿态解耦编码**：编码器仅处理局部姿态状态 $\{\boldsymbol{p}^t, \boldsymbol{q}^t\}$，不包含根轨迹信息：

$$\left\{ \boldsymbol { z } _ { e } ^ { t } \right\} _ { t = 1 } ^ { T / 4 } = \operatorname { e n c } \left( \left\{ \boldsymbol { p } ^ { t } , \boldsymbol { q } ^ { t } \right\} _ { t = 1 } ^ { T } \right)$$

解码器则独立接收量化姿态令牌、局部根轨迹 $\{\hat{r}_l^t\}$ 和稀疏关键帧约束，实现根轨迹与姿态的解耦控制。这一设计使得相同的姿态令牌可以驱动不同的根轨迹，同时保持空间精度（Fig. 4）。

### 2. 模块化粗到细生成流程

传统方法通常采用单一的 in-betweening 解码器（如 CondMDI、Closd-DiP 等扩散模型或 MMM 等掩码建模方法），将时序预测、轨迹生成和姿态合成耦合在一起。MotionBricks 将其分解为两个独立模块：

- **根模块**：分两步渐进式预测。步骤一从约束中预测隐藏状态 $\{h_2\}$ 和帧数 $T_2$；步骤二基于隐藏状态和约束生成全局根轨迹 $\{r_g\}$：

$$\{ h _ { 2 } \} , T _ { 2 } = \mathcal { F } _ { 1 } \left( \{ h _ { 1 } \} ; g ( T _ { 1 } ) ; f ( \mathcal { T } _ { 1 } , \mathcal { T } _ { 2 } , \mathcal { T } _ { 3 } ) \right), \quad \{ r _ { g } \} = \mathcal { F } _ { 2 } \left( \{ h _ { 2 } \} ; g ( T _ { 2 } ) ; f ( \mathcal { T } _ { 1 } , \mathcal { T } _ { 2 } , \mathcal { T } _ { 3 } ) \right)$$

- **姿态模块**：以根模块输出的轨迹和关键帧约束为条件，通过掩码 token 预测对多头部姿态令牌分布建模。

这种模块化分解使每个子问题更易学习，同时允许根模块根据运动风格自动调整轨迹（Fig. 5），而无需姿态模块参与根轨迹的生成。

### 3. 智能基元接口：零样本任务泛化

传统方法依赖预定义的控制标签或文本提示，需要针对每类任务进行微调。MotionBricks 提出**智能基元**（Smart Primitives）作为统一的高层控制接口：

- **Smart Locomotion**：从用户速度命令和风格选择生成目标关键帧，通过渐进式根轨迹精炼（Table 1）和临界阻尼弹簧轨迹平滑：

$$\boldsymbol{r}(t) = e^{-\gamma t} \left( (\boldsymbol{r}_0 - \boldsymbol{r}_{g,1}) + (\boldsymbol{v}_0 + \gamma (\boldsymbol{r}_0 - \boldsymbol{r}_{g,1})) t \right) + \boldsymbol{r}_{g,1}$$

- **Smart Object**：从游戏事件和场景物体信息生成灵活数量的交互关键帧，支持攀爬、跨越、坐下、拾取等多种交互（Fig. 7）。

智能基元将高层用户意图统一转化为关键帧约束集合 $\mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3$（Fig. 3），使底层神经骨干无需微调或标签即可零样本泛化到导航、物体交互和机器人控制等下游任务（Fig. 1, Fig. 6）。

### 创新协同效应

上述三个改变形成正向反馈循环：多头部标记器提供了足够的容量来表征 350k+ 动作片段中的多样化运动模式；根-姿态解耦使得解码器能够独立处理轨迹精度和姿态质量；模块化流程降低了每个子模块的学习难度；智能基元则将生产级控制需求统一为关键帧约束，使模型无需针对每类任务重新训练。最终，这套设计在保持 2ms 延迟和 15,000 FPS 吞吐量的实时效率下，在 FID 指标上显著优于所有基线方法（350k 数据集上 FID=1.054，对比最佳基线 MMM 的 1.153；LaFAN1-G1 上 FID=0.891，对比 ClosdDiP 的 0.903）。

MotionBricks 的整体推理流程由四个阶段构成（图2），其设计核心是将动作生成分解为**高层规划**与**低层合成**两个层次，并通过模块化的粗到细流程实现实时高效的动作控制。

### 1. 智能基元：从用户指令到关键帧约束

流程的起点是**智能基元**（Smart Primitives）模块。该模块接收来自用户的操作指令或游戏引擎的事件信号，将其转化为统一的关键帧约束。这些约束分为三类（图3）：
- **T₁**：局部根轨迹约束（local root constraints）
- **T₂**：全局根轨迹约束（global root constraints）
- **T₃**：姿态约束（pose constraints）

智能基元包含两个子模块：**Smart Locomotion** 负责将速度命令、风格选择等转化为目标关键帧；**Smart Object** 负责处理物体交互、场景攀爬等事件，生成相应的空间-姿态约束。这一设计使得上层接口无需为不同任务单独训练或打标签，实现了零样本的任务泛化。

### 2. 根模块：时序预测与轨迹生成

给定智能基元产生的约束集合，**根模块**（Root Module）分两步完成根轨迹的生成：

- **步骤1**：预测中间隐藏状态 $h_2$ 和待生成的帧数 $T_2$：
  $$\{h_2\}, T_2 = \mathcal{F}_1\left(\{h_1\}; g(T_1); f(\mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3)\right)$$
  
- **步骤2**：基于 $h_2$ 和约束条件预测全局根轨迹 $\{r_g\}$：
  $$\{r_g\} = \mathcal{F}_2\left(\{h_2\}; g(T_2); f(\mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3)\right)$$

根模块的输出为后续的姿态生成提供了时序框架和空间参考。

### 3. 姿态模块：潜在空间中的掩码令牌预测

**姿态模块**（Pose Module）在离散潜在空间中工作。它接收根模块输出的根轨迹以及来自智能基元的约束，通过掩码建模（masked token modeling）的方式逐令牌预测姿态的离散表示。这一过程将连续运动分布的建模转化为离散令牌的分类问题，显著降低了计算复杂度，同时保持了生成多样性。

### 4. 令牌解码器：从离散令牌到连续运动

流程的最后阶段由**令牌解码器**（Token Decoder）完成。解码器接收三类信息：
- 姿态模块预测的量化姿态令牌 $\{z_q^t\}$
- 根模块生成的局部根轨迹 $\{\hat{r}_l^t\}$
- 智能基元提供的稀疏关键帧约束 $\{\check{p}\}, \{\check{q}\}$

解码器通过带跳跃连接的时序上采样网络，将这些信息融合重构为完整的连续运动序列：
$$\{r_l^t, \boldsymbol{p}^t, \boldsymbol{q}^t, \boldsymbol{v}^t, \boldsymbol{c}^t\}_{t=1}^T = \operatorname{dec}\left(\{\boldsymbol{z}_q^t\}_{t=0}^{T/4}, \{\hat{r}_l^t\}_{t=0}^T, \{\check{p}\}, \{\check{q}\}\right)$$

### 5. 关键设计决策

整个框架的核心调节变量是**结构化的多头部潜在标记器**与**根-姿态解耦策略**：
- 编码器仅对局部姿态状态（关节位置 $\boldsymbol{p}$、旋转 $\boldsymbol{q}$）进行编码，显式剥离根信息，使得潜在空间专注于姿态本身的建模
- 多头部量化将潜在嵌入沿特征维度分割到 $K$ 个独立码本中，每个头部负责不同语义子空间，使得总码本容量可达约 $10^9$ 个令牌组合，远超单头部设计的饱和瓶颈（图10）
- 根轨迹的独立预测与姿态的潜在生成相互解耦，使得关键帧约束可以灵活地注入根模块、姿态模块和解码器的不同层级（图3），实现了对空间精度和时序一致性的精细控制

这种模块化的粗到细流程，使得 MotionBricks 在保持 2ms 生成延迟和 15,000 FPS 吞吐量的严格实时约束下，仍能以单一模型有效处理超过 35 万段动作的大规模数据集。

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3811334/figures/013_Figure_10.jpg]]
*Figure 10: Scalability comparison between our multi-head tokenizer and a single-head baseline. Left and middle: Token reconstruction loss during training for varying codebook sizes for our method and the baseline. Our tokenizer continues to improve with larger codebooks (up to 109 tokens), while the baseline plateaus quickly. Right: Trade-off between FID (distribution quality) and keyframe joint position error as codebook size increases. Our method achieves better FID with larger codebooks while maintaining low keyframe error*

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3811334/figures/002_Figure_2.jpg]]
*Figure 2: MotionBricks’s inference pipeline consists of four stages. Given user commands or game events, smart primitives generate target keyframes. The root module first predicts timing and root trajectory, followed by the pose module that models the distribution of multi-head latent pose tokens. Finally, the decoder produces continuous motion conditioned on pose tokens, root trajectories, and keyframes*

MotionBricks 的推理流程由四个核心模块构成（Fig. 2）：**Smart Primitives** 将用户指令或游戏事件转化为目标关键帧约束；**Root Module** 预测过渡帧数与全局根轨迹；**Pose Module** 通过掩码令牌建模生成多头部潜在姿态令牌；**Token Decoder** 从姿态令牌、根轨迹与关键帧约束中解码出连续全身运动。

### 4.1 结构化多头部标记器

标记器采用**根-姿态解耦**策略：编码器仅对局部姿态状态（关节位置 $\boldsymbol{p}^t$、旋转 $\boldsymbol{q}^t$）进行编码，排除根信息，从而将根轨迹控制与姿态生成分离。

**编码器定义**（Equation 1）：

$$\left\{ \boldsymbol{z}_e^t \right\}_{t=1}^{T/4} = \operatorname{enc}\left( \left\{ \boldsymbol{p}^t, \boldsymbol{q}^t \right\}_{t=1}^{T} \right)$$

其中 $T$ 为输入帧数，编码器在时间维度上进行 4 倍下采样，将姿态状态映射为连续潜在嵌入 $\boldsymbol{z}_e^t$。

**多头部量化**（Equation 2）：连续嵌入 $\boldsymbol{z}_e^t$ 沿特征维度被分割为 $K$ 个独立段，每段在其专属码本 $\mathcal{E}_k$ 中寻找最近邻条目：

$$z_q^t = \begin{cases} z_{q,1}^t \\ z_{q,2}^t \\ \vdots \\ z_{q,K}^t \end{cases} = \begin{cases} \arg\min_{e_1 \in \mathcal{E}_1} \| z_{e,1}^t - e_1 \|_2^2 \\ \arg\min_{e_2 \in \mathcal{E}_2} \| z_{e,2}^t - e_2 \|_2^2 \\ \vdots \\ \arg\min_{e_K \in \mathcal{E}_K} \| z_{e,K}^t - e_K \|_2^2 \end{cases}$$

这一设计的关键优势在于：总码本容量为各头码本大小的乘积，在相同参数量下可达到远超单头标记器的表达能力。实验表明，多头部标记器在总码本容量高达约 $10^9$ tokens 时仍持续改善重建损失，而单头基线迅速饱和（Fig. 10）。

训练采用标准 VQ-VAE 损失，包含量化损失与承诺损失，权重系数为 $\beta$。

### 4.2 根-姿态解耦解码器

解码器从量化姿态令牌 $\{\boldsymbol{z}_q^t\}$、局部根轨迹 $\{\hat{r}_l^t\}$ 和稀疏关键帧约束 $\{\check{p}\}, \{\check{q}\}$ 中重构完整运动（Equation 3）：

$$\{ r_l^t, \boldsymbol{p}^t, \boldsymbol{q}^t, \boldsymbol{v}^t, \boldsymbol{c}^t \}_{t=1}^{T} = \operatorname{dec}\left( \{\boldsymbol{z}_q^t\}_{t=0}^{T/4}, \{\hat{r}_l^t\}_{t=0}^{T}, \{\check{p}\}, \{\check{q}\} \right)$$

解码器通过跳跃连接将根轨迹特征与姿态令牌嵌入沿特征维度拼接，采用渐进式时间上采样（下采样因子 4、2、1）恢复原始帧率。稀疏关键帧约束经零填充后以相同方式处理。这一解耦设计使得相同的姿态令牌可以被驱动到不同的根轨迹上，同时保持精确的关键帧控制（Fig. 4）。

### 5.1 根模块

根模块以两阶段方式工作（Equation 4）：

**步骤 1**：从约束集 $\mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3$ 中预测隐藏状态 $\{h_2\}$ 和过渡帧数 $T_2$：
$$\{h_2\}, T_2 = \mathcal{F}_1\left( \{h_1\}; g(T_1); f(\mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3) \right)$$

**步骤 2**：基于 $\{h_2\}$ 和约束预测全局根轨迹 $\{r_g\}$：
$$\{r_g\} = \mathcal{F}_2\left( \{h_2\}; g(T_2); f(\mathcal{T}_1, \mathcal{T}_2, \mathcal{T}_3) \right)$$

其中 $g(\cdot)$ 为时间编码函数，$f(\cdot)$ 为约束编码函数。约束集 $\mathcal{T}_1$（局部根）、$\mathcal{T}_2$（全局根）、$\mathcal{T}_3$（姿态）可灵活缺失（Fig. 3），实线框表示提供的约束，虚线框表示可选或缺失项。

### 5.2 姿态模块

姿态模块采用掩码令牌建模策略，在已知根轨迹和关键帧约束的条件下预测被掩码的姿态令牌。训练时随机掩码部分令牌，推理时从全掩码状态开始迭代解码，生成与根轨迹协调的全身姿态序列。

### 6.1 临界阻尼弹簧轨迹

Smart Locomotion 中采用临界阻尼弹簧模型生成从当前根状态向目标平滑过渡的根轨迹（Equation 6）：

$$\boldsymbol{r}(t) = e^{-\gamma t} \left( (\boldsymbol{r}_0 - \boldsymbol{r}_{g,1}) + (\boldsymbol{v}_0 + \gamma (\boldsymbol{r}_0 - \boldsymbol{r}_{g,1})) t \right) + \boldsymbol{r}_{g,1}$$

其中 $\gamma$ 为阻尼系数，$\boldsymbol{r}_0$ 和 $\boldsymbol{v}_0$ 为当前根位置与速度，$\boldsymbol{r}_{g,1}$ 为目标根位置。该模型保证了轨迹的平滑性与物理合理性，并通过神经根细化进一步根据运动风格自动调整（Fig. 5, Table 1）。

## 实验与关键发现

### 核心性能：大规模实时生成的质量与效率

MotionBricks 在包含 350k 动作片段的专有数据集上展现出全面的性能优势。如 Table 3 所示，该方法在 FID 指标上达到 **1.054**，优于所有基线方法，包括此前最佳的掩码运动建模方法 MMM（FID=1.153）。更重要的是，这一质量优势是在极致的实时效率下实现的：MotionBricks 的单次生成延迟仅为 **2ms**，吞吐量高达 **15,000 FPS**，而其他生成式方法（如扩散模型或两阶段变换器）的推理时间通常在秒级甚至分钟级。这种量级上的效率差距源于其模块化的潜在生成架构——通过在紧凑的离散潜在空间中进行掩码令牌预测，而非在原始运动数据空间中进行昂贵的迭代去噪或自回归解码。

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3811334/figures/012_Table_3.jpg]]
*Table 3: Quantitative comparison on the 350k dataset. ↓ indicates lower is better, ↑ indicates higher is better. Best results are in bold, while underlined indicates the second-best or competitive runner-up results*

在公开基准数据集上的评估进一步验证了方法的泛化能力。在 LaFAN1-G1 上，MotionBricks 以 **FID=0.891** 取得最优，略优于次优的扩散引导方法 ClosdDiP（FID=0.903）。在 Bones-70k 数据集的目标达成任务上，该方法实现了 **99.6%** 的到达成功率，接近完美，显著超过所有基线（Table 4）。

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3811334/figures/014_Table_4.jpg]]
*Table 4: Quantitative comparison on LaFAN1-G1, HumanML3D, and Bones-70k datasets. ↓ indicates lower is better, ↑ indicates higher is better. Best results are in bold, second best are underlined*

评估体系覆盖了七个维度的指标：速度精度、分布质量、人体偏好、多样性、平滑度、物理合理性以及关键帧精确度。40 名不同背景的参与者参与了人体评估，确保了主观质量判断的统计可靠性。

### 结构化多头部标记器的可扩展性

多头部标记器（multi-head tokenizer）是 MotionBricks 实现大规模可扩展性的关键设计。Figure 10 的消融实验揭示了一个核心发现：**当码本总容量从约 $10^5$ 扩展到约 $10^9$ 个令牌时，多头部标记器的重建损失持续下降，而单头部基线则迅速饱和**。这意味着，将潜在特征沿通道维度分割为多个独立量化的“头部”，每个头部拥有自己的码本，能够指数级地扩展表示容量，同时避免单一大码本带来的优化困难。

Figure 11 进一步探索了在固定总容量（约 $10^6$ 令牌）下，头部数量与每头码本大小的权衡。实验表明，**每头配置 128–256 个令牌**能够在重建质量与下游生成鲁棒性之间取得最佳平衡。过少的头部（如单头）限制了容量利用效率，而过多的头部（如每头仅 64 个令牌）则导致每个头部的表示过于粗糙，影响关键帧约束的精确满足。

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3811334/figures/015_Figure_11.jpg]]
*Figure 11: Ablation study on multi-head tokenization with fixed total codebook capacity ( $\sim$ 1 $0 ^ { 6 }$ tokens). “H” denotes the number of heads,$^ { * } C ^ { * }$ denotes the codebook size per head in the experiment name. Left: tokenizer’s reconstruction loss during training. Right three plots: FID, NPSS, and keyframe error under token perturbation, simulating lower-bound motion quality in real applications*

在量化器选择上，VQ-VAE 相比 FSQ（finite scalar quantization）在跨熵损失和下游 FID 上均略有优势，因此被选为默认方案（Fig. 17, 附录 B）。

### 根-姿态解耦与模块化生成的消融

根模块与姿态模块的解耦设计对实时控制精度至关重要。根模块分两步运行：首先根据约束预测过渡帧数 $T_2$ 和隐藏状态，然后生成全局根轨迹 $\{r_g\}$。这种渐进式预测使得根轨迹能够精确满足用户指定的速度命令和目标位置，而姿态模块则专注于在给定根轨迹和关键帧约束下生成自然的上半身运动。

Figure 14 的消融表明，**提供姿态关键帧约束同时改善了 FID 和目标达成成功率，并保持了较低的脚滑伪影**。这验证了智能基元（smart primitives）接口的有效性——通过将高层用户命令（如“坐下”、“攀爬”）转化为稀疏但精确的关键帧约束，模型无需针对每个下游任务进行微调即可实现零样本泛化。

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3811334/figures/018_Figure_14.jpg]]
*Figure 14: Root trajectory interpolation analysis. Root interpolation ratio of 1.0 is the original trajectory; \<1.0 compresses, >1.0 stretches. Left: FID and target reaching success rate remain stable across interpolation ratios, especially with keyframe constraints. Right: Foot skate stays low even under significant root manipulation, demonstrating the decoder’s robustness*

### 数据规模扩展性

Figure 13 展示了 MotionBricks 随训练数据规模增加的性能变化趋势。与基线方法在大规模数据上出现性能下降不同，**本方法随着数据量增加持续改善或保持稳定**。这一特性归因于多头部潜在表示的容量优势：当数据多样性增加时，模型可以通过激活码本中更多的令牌组合来覆盖新的运动模式，而不会因表示瓶颈而遗忘已有知识。

### 失败模式与局限性

尽管 MotionBricks 在大多数场景下表现优异，论文明确指出了若干失败模式：

1. **精细操作缺失**：数据集缺少手指和物体运动数据，限制了抓取、操纵等精细操作动作的生成。这意味着在需要手-物交互的场景（如拿起杯子）中，生成质量可能下降。

2. **平坦地形假设**：模型缺乏连续地形高度信息，无法生成适应不平坦地形（如楼梯、斜坡）的真实运动。当前系统假设所有交互发生在地平面上。

3. **稀有动作泛化困难**：对于样本极少的动作类别（如跳过 1 米高的障碍），模型难以从稀疏示例中学习到可泛化的运动模式。这是数据驱动方法的共性挑战。

4. **高重规划频率下的退化**：附录 C 指出，离散潜在表示在极高的重规划频率下会导致 FID 和关键帧误差轻微增加。这是因为频繁的令牌重采样引入了额外的量化噪声，而解码器对令牌序列的连续性有一定依赖。

### 开放问题

论文提出了四个值得进一步探索的方向：如何在运行时从传感器数据直接生成控制信号（视觉规划）；如何保证生成动作的物理合理性以避免自碰撞或超出机器人硬件约束；如何在多样化机器人形态之间进行高质量的运行时动作重定向；以及如何处理极端稀疏数据下的动作学习问题。

## 定位与知识库关联

### 1. 核心瓶颈与因果调节变量

现有生成式动作合成模型在实时应用场景中面临两大结构性瓶颈。**第一，模型容量与实时性的根本矛盾**：当数据集规模超过35万段动作片段时，传统生成模型在严格实时计算约束下，质量与可扩展性显著下降，无法以单一模型有效覆盖如此大规模的动作分布。**第二，控制接口的碎片化**：生产级应用需要同时响应速度命令、风格选择、关键帧约束等多模态信号，而现有方法缺乏统一的精细控制接口，往往需要针对不同任务分别训练或微调。

MotionBricks通过两个关键调节变量突破上述瓶颈。**因果调节变量一：结构化的多头部潜在标记器与根-姿态解耦策略**。该设计将连续运动特征量化到多个独立码本中，同时分离根轨迹和姿态的编码，在总码本容量高达约10⁹个token时仍持续降低重建损失，而单头基线迅速饱和（Fig. 10）。这一结构同时提升了模型容量、关键帧控制精度和实时性能。**因果调节变量二：模块化粗到细的渐进式生成流程**。通过将动作生成分解为基于关键帧约束的根轨迹预测和姿态潜在生成两个阶段，模型在保持2ms延迟、15,000 FPS吞吐量的实时效率下，实现了高质量、可扩展的零样本动作控制。

### 2. 方法谱系中的位置与基线关系

MotionBricks以**动作中间帧生成（motion in-betweening）**为基础范式，在方法谱系中处于条件生成模型与实时运动合成的交汇点。其直接对比的基线方法覆盖了该领域的多个技术路线：

**基于插值的方法**：**Delta-interpolator**和**Twostage Trans.**代表了传统的插值与两阶段变换器方案。这类方法计算效率较高，但在运动质量和多样性上存在明显局限，尤其在大规模数据集上难以捕捉复杂动作分布。

**基于扩散模型的方法**：**CondMDI**（conditional motion diffusion in-betweening）和**Closd-DiP**（diffusion-based in-betweening with guidance）代表了扩散模型在动作生成中的应用。这些方法在质量指标上表现优异——Closd-DiP在LaFAN1-G1数据集上FID达到0.903，是除MotionBricks外的最佳结果（Table 4）——但扩散模型的多步去噪过程导致生成延迟通常在秒级甚至分钟级，无法满足实时应用需求。

**基于掩码建模的方法**：**MMM**（masked motion modeling）采用token-based生成范式，在350k数据集上FID=1.153，是基线中的最佳结果（Table 3）。MotionBricks在相同范式下通过结构化多头部标记器和根-姿态解耦，将FID进一步降至1.054，同时将吞吐量提升至15,000 FPS。

**方法演进的关键变化槽位**：

| 变化槽位 | 基线方案 | MotionBricks方案 | 证据锚点 |
|---------|---------|-----------------|---------|
| 标记器设计 | 单头VQ-VAE，根-姿态联合编码 | 多头部量化，根-姿态解耦，可学习掩码嵌入支持灵活约束 | Section 4.1, Fig. 10, Fig. 11 |
| 生成骨干 | 单体中间帧解码器 | 模块化粗到细流程：独立根模块（时序+根轨迹）+姿态模块（掩码token预测） | Section 5, Fig. 2, Algorithm 1 |
| 高层控制接口 | 预定义one-hot控制标签或文本提示，需逐任务训练 | 智能基元（smart locomotion + smart object）生成统一关键帧约束，支持零样本任务泛化 | Section 3, Section 6, Fig. 6, Fig. 7 |

### 3. 适用边界与局限

**数据覆盖边界**：当前数据集缺少手指和物体运动数据，限制了精细操作动作（如抓取、操纵）的生成能力。此外，稀有动作类别（如跳过1米障碍）样本极少，模型在这些场景下的泛化存在困难。

**环境感知边界**：模型缺乏连续地形信息输入，无法生成不平坦地形上的真实运动。当前系统依赖场景物体的特权信息（如物体位置、类型），而非从传感器数据直接感知。

**实时重规划边界**：离散潜在表示在较高重规划频率下会导致FID和关键帧误差轻微增加（附录C），表明模型在高频在线调整场景中存在一定的质量退化。

**物理合理性边界**：虽然模型在脚滑伪影控制上表现良好（Fig. 14），但尚未内置严格的物理约束机制来确保生成动作避免自碰撞或满足机器人硬件约束。

### 4. 开放问题

**视觉规划与端到端控制**：如何在运行时实现视觉规划，从传感器数据直接生成控制信号，而无需依赖场景物体的特权信息？这将使系统从“已知环境下的动作生成”扩展到“感知驱动的自主控制”。

**物理合理性与安全约束**：如何确保生成动作的物理合理性，避免自碰撞或超出机器人硬件约束？当前方法依赖数据驱动的隐式约束，缺乏显式的物理验证机制。

**跨形态动作重定向**：如何在多样化的机器人形态之间进行高质量的运行时动作重定向？当前系统在Unitree G1机器人上展示了初步能力（Fig. 1, Fig. 6），但通用跨形态迁移仍是一个开放挑战。

**极端稀疏数据下的学习**：如何处理极端稀疏数据下的动作学习，例如仅有一段样例如何泛化到新的交互场景？这对稀有动作类别和个性化动作风格的学习至关重要。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.pdf]]

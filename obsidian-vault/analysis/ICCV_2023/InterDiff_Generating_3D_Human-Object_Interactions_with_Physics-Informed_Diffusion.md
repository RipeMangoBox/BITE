---
title: "InterDiff: Generating 3D Human-Object Interactions with Physics-Informed Diffusion"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: "paperPDFs/ICCV_2023/InterDiff:_Generating_3D_Human-Object_Interactions_with_Physics-Informed_Diffusion.pdf"
project_link: https://sirui-xu.github.io/InterDiff/
code_link: null
aliases:
- InterDiff
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在扩散反向过程中嵌入基于接触参考系的物理信息交互校正步骤——当检测到物理不合理时，利用局部相对运动的简单模式预测并修正物体运动，再注入回扩散迭代。
primary_logic: 相对于接触点的物体运动遵循简单且近于确定性的模式，通过坐标变换将物体运动转移至局部参考系，可大幅降低预测难度并提升物理一致性。
claims:
- 在BEHAVE数据集上，交互校正使穿透指标（Pene.）从228降至164，相对降低28%，且不影响人体关节精度。
- 在100帧长时自回归预测中，带校正的InterDiff将穿透从236降至88（降低63%），且人体关节误差从400降至392，表明物理合理性的提升惠及人体运动预测。
- 用户研究证实，全模型在物理真实性上以67.8%的胜率显著优于纯扩散基线及其他变体。
- BEHAVE 上 Pene. (↓) = 164 (full)
---

# InterDiff: Generating 3D Human-Object Interactions with Physics-Informed Diffusion

> [!tip] 核心洞察
> 相对于接触点的物体运动遵循简单且近于确定性的模式，通过坐标变换将物体运动转移至局部参考系，可大幅降低预测难度并提升物理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterDiff：基于物理信息扩散的3D人物交互生成 |
| 英文题名 | InterDiff: Generating 3D Human-Object Interactions with Physics-Informed Diffusion |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2308.16905) · [Project](https://sirui-xu.github.io/InterDiff/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InterDiff |
| Dataset | BEHAVE, Human-Object Interaction |

> [!tip] 效果简介
> - BEHAVE 上，Pene. (↓) 164 (full) vs 228 (w/o correction) (-64 (-28%))；Rot.Err. (↓) 226 (full) vs 256 (w/o correction) (-30 (-12%))。
> - Human-Object Interaction 上，MPJPE-O (↓) 84 (full) vs 117 (w/o correction) (-33 (-28%))；Trans. Err. (↓) 60 (full) vs 92 (w/o correction) (-32 (-35%))。
> - BEHAVE (long-term 100f, 10 samples) 上，Pene. (↓) 59 (full) vs 187 (w/o correction) (-128 (-68%))。

## 概要

**问题瓶颈**：纯扩散模型在生成3D人-物交互（Human-Object Interaction, HOI）序列时，忽略物理法则，导致接触悬浮、穿透等物理不合理现象频发，尤其在长时预测中误差累积严重。

**核心洞察**：相对于接触点的物体运动遵循简单且近于确定性的模式——例如绕固定轴旋转或近乎静止。通过坐标变换将物体运动转移至以接触点为原点的局部参考系，可大幅降低运动预测难度并提升物理一致性（Figure 2）。

**方法定位**：**InterDiff** 是一个物理信息引导的扩散生成框架，包含两个可解耦组合的步骤：
- **交互扩散**：基于条件去噪扩散概率模型（DDPM），直接预测未来人-物交互序列的干净信号。
- **交互校正**：在扩散反向过程中嵌入物理合理性检测与修正——当检测到接触/穿透异常时，调度器选择局部参考系，由时空图神经网络（STGNN）预测物体相对运动并融合回扩散迭代。

**主要结果**：
- 在BEHAVE数据集上，交互校正使穿透指标（Pene.）从228降至164（相对降低28%），物体旋转误差从256降至226（-12%），且不影响人体关节精度。
- 在100帧长时自回归预测中，带校正的InterDiff将穿透从236降至88（-63%），人体关节误差（MPJPE-H）从400降至392，表明物理合理性的提升惠及人体运动预测。
- 用户研究证实，全模型在物理真实性上以67.8%的胜率显著优于纯扩散基线及其他变体。

**方法谱系与知识库定位**：InterDiff将物理先验以“校正步骤”形式注入扩散生成过程，区别于依赖后处理优化或无显式物理约束的基线方法（如基于VAE的**InterVAE**、基于LSTM的**InterRNN**、基于Transformer的**CAHMP**、图卷积网络**HO-GCN**）。其关键创新在于利用局部参考系下的相对运动简单性，将物理合理性保证内嵌于生成循环中，而非作为独立的后处理阶段。



### 问题背景：3D人-物交互预测

在计算机视觉与图形学中，理解和预测人类与物体的交互是一个核心且极具挑战的问题。给定过去若干帧的人体姿态与物体运动状态，系统需要生成未来一段时间的3D人-物交互（Human-Object Interaction, HOI）序列。这一任务在机器人协作、增强现实、自动驾驶等领域具有广泛的应用前景。

然而，3D HOI预测面临着双重困难。首先，人体运动本身具有高度多样性和不确定性——同一段过去观察可以对应多种合理的未来行为。其次，物体运动与人体运动之间存在复杂的耦合关系：物体可能被人体推动、抓取、旋转，也可能在人体离开后保持静止或沿物理规律运动。这种耦合使得联合建模人与物的未来状态变得极为困难。

### 现有方法的缺口：物理合理性的缺失

现有的运动生成方法主要沿着两条技术路线发展。一类基于变分自编码器（VAE）或循环神经网络（RNN/LSTM）的序列生成模型，例如**InterVAE**和**InterRNN**，它们能够编码交互序列的分布并生成未来帧，但缺乏对物理规律的显式建模。另一类方法如**CAHMP**（基于Transformer的条件自回归运动预测）和**HO-GCN**（图卷积网络交互动作预测），虽然在人体运动预测上取得了进展，但在处理人-物交互时，同样未引入物理约束。

这些方法的共同缺陷在于：**纯数据驱动的生成模型忽略物理法则，在生成人-物交互时无法保证物理有效性**。具体表现为两类典型的物理伪影：

- **接触悬浮（Contact Floating）**：人体本应与物体接触，但生成的人体网格悬浮在物体表面之上，缺乏真实的接触约束。
- **穿透（Penetration）**：人体或物体相互穿透，违反了刚体不可穿透的基本物理规律。

这一问题在长时预测中尤为严重。当模型以自回归方式生成数十帧甚至上百帧的未来交互时，物理误差会逐步累积，导致生成的交互序列在后期完全脱离物理现实。

### 核心洞察：接触参考系下的简单运动模式

InterDiff的提出源于一个关键的几何与物理观察。如Figure 2所示，当我们将物体的运动从全局坐标系变换到以接触点为原点的局部参考系时，原本复杂、非线性的物体运动呈现出显著简化的模式：

- 在某些交互中，物体相对于接触点**绕固定轴旋转**（例如推椅子时椅子绕接触腿旋转）。
- 在另一些交互中，物体相对于接触点**几乎静止**（例如人体离开后物体保持原位）。

这一现象背后的物理直觉是：在接触约束下，物体的运动自由度受到限制，其相对于接触点的运动遵循简单且近于确定性的模式。通过坐标变换将物体运动转移至局部参考系，可以大幅降低预测难度，并为生成过程注入物理先验。

### 本文动机：将物理先验嵌入扩散生成

基于上述洞察，InterDiff提出了一种新颖的框架：**在条件扩散模型的生成过程中，嵌入基于接触参考系的物理信息交互校正步骤**。具体而言：

1. **扩散生成**：利用条件去噪扩散概率模型（DDPM）编码未来人-物交互的分布，生成多样化的候选序列。
2. **交互校正**：在扩散反向过程的每一步，检测当前去噪结果的物理合理性（接触状态与穿透程度）。当检测到物理不合理时，利用局部参考系下的简单运动模式预测并修正物体运动，再将修正结果注入回扩散迭代。

这种设计的核心优势在于：扩散模型负责捕捉交互的多样性和全局结构，而校正步骤则作为一个轻量级的物理先验注入器，在不损害生成多样性的前提下，显著提升物理一致性。更重要的是，扩散生成与交互校正**无需在训练阶段耦合**，可以在推理时灵活组合，无需额外的微调。

通过这一框架，InterDiff旨在解决纯扩散模型在HOI生成中的物理有效性瓶颈，为长时、多样化且物理合理的人-物交互预测提供新的技术路径。



## 核心方法与创新机理

InterDiff 的核心创新在于将**物理先验以可组合的方式注入扩散生成框架**，解决了纯扩散模型在人-物交互（HOI）预测中普遍存在的物理不合理性问题。其关键洞察是：**物体相对于接触点的运动遵循简单且近于确定性的模式**（Figure 2）——例如绕固定轴旋转或近乎静止。通过坐标变换将物体运动从全局坐标系转移至以接触点为原点的局部参考系，运动预测的难度大幅降低。

基于这一洞察，InterDiff 引入了两个相互解耦的模块，在推理时组合而无需联合微调：

### 1. 交互校正调度器（Correction Scheduler）

该模块在每个扩散反向步骤后评估去噪结果的物理合理性。具体而言，它计算人体网格顶点与物体网格顶点之间的最小距离作为接触状态 $C$，以及物体顶点在人体内部的穿透深度和作为穿透状态 $P$（Eq. 5）。当检测到接触缺失或穿透超过阈值时，调度器触发校正，并选择最接近的接触点作为局部参考系原点（Eq. 6）；若无接触，则保持全局参考系。校正仅在扩散后期每隔若干步执行，以平衡效率与效果。

### 2. 交互预测器（Interaction Predictor）

一旦校正被触发，交互预测器在选定的局部参考系下，利用时空图神经网络（STGNN）结合离散余弦变换（DCT）预测物体的相对运动。随后将预测结果变换回全局坐标系，并与当前去噪结果进行融合。这种“变换-预测-逆变换”的流程（Figure 3）使得STGNN只需学习简单的相对运动模式，而非复杂的全局轨迹。

### 与基线方法的关键差异

| 设计维度 | 基线方法 | InterDiff |
|---------|---------|-----------|
| 生成架构 | VAE或LSTM（InterVAE、InterRNN） | 条件去噪扩散概率模型（DDPM），直接预测干净信号 |
| 物理约束 | 无显式物理约束，或依赖后处理优化 | 扩散过程中内嵌交互校正，根据接触/穿透状态动态调度 |
| 物体运动建模 | 全局坐标系 | 基于接触点的局部参考系，利用相对运动的简单模式 |

这种设计使得InterDiff在保持扩散模型多样性和表达力的同时，显著提升了生成结果的物理一致性。消融实验表明，去除交互校正（纯扩散）导致穿透指标从164升至228（+39%），长时预测中穿透从59升至187（+217%），验证了校正模块的关键作用。



InterDiff 的整体 pipeline 由两个可解耦的核心模块构成：**交互扩散（Interaction Diffusion）** 与 **交互校正（Interaction Correction）**。两者在训练阶段独立训练，在推理阶段组合使用，无需联合微调。其输入输出流如下：给定一段包含 $H$ 帧历史帧的人-物交互序列 $\pmb{x}^{1:H}$（含人体姿态与物体位姿），以及通过 PointNet 提取的物体规范姿态几何编码，模型的目标是生成未来 $F$ 帧的交互序列 $\pmb{x}^{H+1:H+F}$。

### 模块关系与数据流

**1. 交互扩散模块（条件去噪扩散概率模型）**
该模块是整个 pipeline 的主干网络，采用基于 Transformer 的条件 DDPM 架构。它以加噪后的完整序列 $\pmb{x}_t$、扩散时间步 $t$、物体形状编码 $\pmb{c}$ 及历史交互为条件，直接预测干净的未来交互序列 $\tilde{\pmb{x}}$。训练目标为简单的均方误差损失 $\mathcal{L}_r$，使网络输出逼近真实交互序列。该模块负责建模交互的整体分布，生成多样化的候选运动。

**2. 交互校正模块（物理信息注入）**
该模块嵌入在扩散反向过程的后期迭代中，每若干步触发一次，用于修正扩散模型产生的物理不合理结果。它由两个子组件构成：

- **校正调度器（Correction Scheduler）**：对当前去噪结果进行物理合理性评估——通过计算人体顶点与物体顶点间的最小距离 $C[j]$ 定义接触状态，通过 SDF 穿透深度和 $P$ 定义穿透程度。若检测到接触悬浮或穿透，则触发校正，并选择距离最近的接触点作为局部参考系；若无接触，则保持全局参考系不变（$s = -1$）。

- **交互预测器（Interaction Predictor）**：在选定的局部参考系下，将物体运动从全局坐标变换至相对于接触点的局部坐标。利用时空图神经网络（STGNN）结合 DCT 编码，对过去运动图 $G^{1:H}$ 进行处理，预测未来的物体相对运动 $G^{\dot{H}:H+\dot{F}}$，再将其变换回全局坐标系。由于相对于接触点的物体运动遵循近于确定性的简单模式（如绕固定轴旋转或近乎静止），这一预测难度远低于直接预测全局运动。

**3. 融合机制**
当校正调度器判定需要校正时，将交互预测器生成的修正物体运动 $\hat{\pmb{x}}$ 与扩散模型的去噪结果 $\tilde{\pmb{x}}$ 进行融合，得到物理上更合理的交互序列，再注入回后续的扩散迭代中。这一设计使得物理先验以即插即用的方式约束扩散生成过程，而无需修改扩散模型的训练。

### 关键设计动机

该框架的核心洞察在于：**物体相对于接触点的运动遵循简单且可预测的模式**。通过坐标变换将物体运动从全局坐标系转移至基于接触点的局部参考系，预测难度大幅降低。扩散模型负责整体多样性与运动趋势，校正模块则在物理层面进行精细化调整——两者分工明确，互补而非冲突。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/003_Figure_3.jpg]]
*Figure 3: Overview of InterDiff. (i) We combine a Correction Scheduler and an Interaction Predictor with the diffusion framework to correct a denoised HOI. The Correction Scheduler determines whether the current denoised HOI needs correction. If so, we fuse the additional prediction generated by the Interaction Predictor into the denoised HOI. (ii) Our reverse diffusion employs a transformer architecture conditioned on the encoded object shape and the past HOI. (iii) We transform object motion under the reference system selected by the Correction Scheduler, predict future motion via STGNN, and transform it back to the ground system. Markers are in point clouds*



InterDiff 由两个可解耦的核心模块构成：**交互扩散（Interaction Diffusion）** 与**交互校正（Interaction Correction）**。二者在训练阶段独立，仅在推理时组合，无需联合微调。

### 3.1 交互扩散：条件去噪扩散概率模型

交互扩散采用条件 DDPM 框架，直接预测干净的人-物交互序列，而非噪声。

**序列表示。** 给定包含 $H$ 帧历史与 $F$ 帧未来的 HOI 序列：

$$\pmb{x}^{\bar{}} = [\pmb{x}^1, \dots, \pmb{x}^{H+F}]$$

其中每一帧 $\pmb{x}^i$ 包含人体姿态 $\bar{\boldsymbol{h}}^i \in \mathbb{R}^{J \times D_h}$（$J$ 个关节，每关节 $D_h$ 维表示）与物体 6D 位姿。

**前向扩散。** 以马尔可夫链逐步注入高斯噪声，共 $T$ 步：

$$q(\pmb{x}_1, \dots, \pmb{x}_T | \pmb{x}_0) = \prod_{t=1}^T q(\pmb{x}_t | \pmb{x}_{t-1})$$

单步转移为：

$$q(\pmb{x}_t | \pmb{x}_{t-1}) = \mathcal{N}(\sqrt{\beta_t} \pmb{x}_{t-1} + (1 - \beta_t) \mathbf{I})$$

利用累积乘积 $\bar{\alpha}_t$，可直接从 $\pmb{x}_0$ 采样任意步噪声样本：

$$\pmb{x}_t = \sqrt{\bar{\alpha}_t} \pmb{x}_0 + \sqrt{1 - \bar{\alpha}_t} \pmb{\epsilon}$$

**反向去噪。** 网络 $\mathcal{G}$ 直接估计干净序列：

$$\tilde{\pmb{x}} = \mathcal{G}(\pmb{x}_t, t, \pmb{c})$$

其中条件 $\pmb{c}$ 包含历史交互帧与 PointNet 提取的物体规范姿态几何编码。训练目标为均方误差：

$$\mathcal{L}_r = \mathbb{E}_{t \sim [1, T]} \| \mathcal{G}(\pmb{x}_t, t, \pmb{c}) - \pmb{x} \|_2^2$$

此外引入速度正则化损失 $\mathcal{L}_{vh}$ 对人体姿态进行时间平滑约束：

$$\mathcal{L}_{vh} = \mathbb{E}_{t} \| \pmb{h}_0^{H+1:H+F}(t) - \pmb{h}_0^{H:H+F-1}(t) \|_2^2$$

### 3.2 交互校正：物理信息注入机制

纯扩散模型生成的交互序列常违反物理法则——物体悬浮于手外或穿透人体。交互校正模块在反向扩散的后期迭代中，每隔若干步对去噪结果进行物理合理性检测与修正。

**校正调度器（Correction Scheduler）。** 首先定义接触状态 $C$ 与穿透状态 $P$：

$$C^i[j] = \min_{k=1,\ldots,V_o} \|\pmb{v}_h^i[j] - \pmb{v}_o^i[k]\|_2, \quad j=1,\ldots,V_h$$

$$P^i = \sum \max(0, -\text{sdf}(\pmb{v}_o^i[k]))$$

其中 $\pmb{v}_h$、$\pmb{v}_o$ 分别为人体与物体顶点，$V_h$、$V_o$ 为顶点数，sdf 为有符号距离函数。$C^i[j]$ 度量第 $i$ 帧人体顶点 $j$ 到物体的最近距离；$P^i$ 累积物体顶点穿透人体的深度。

基于接触状态选择参考系 $s$（以网格顶点为标记点 $\mathcal{M}$）：

$$s = \begin{cases} -1, & \text{if } \min_{j\in\mathcal{M}} \|C[j]\| \ge \epsilon_2 \\ \arg\min_{j\in\mathcal{M}} \|C[j]\|, & \text{otherwise} \end{cases}$$

当 $\min \|C[j]\| \ge \epsilon_2$ 时判定为无接触，保持全局参考系（$s=-1$）；否则选取最近接触点作为局部参考系。对于仅有关节标注的数据集，以人体关节替代网格顶点进行选择。

**交互预测器（Interaction Predictor）。** 核心洞察在于：相对于接触点的物体运动遵循简单且近于确定性的模式——如绕固定轴旋转或近乎静止（见 Figure 2）。校正时，先将物体运动变换至选定的局部参考系，使用时空图神经网络（STGNN）结合离散余弦变换（DCT）预测未来物体相对运动，再变换回全局坐标系，得到校正后的物体运动 $\hat{\pmb{x}} = \mathcal{P}(\tilde{\pmb{x}}, s)$。最终将校正运动与扩散去噪结果融合，注入回扩散迭代。

**推理流程。** 完整的 InterDiff 推理过程如 Algorithm 1 所示：在反向扩散的每一步，先通过 $\mathcal{G}$ 获得去噪估计 $\tilde{\pmb{x}}$；校正调度器 $\mathcal{S}$ 判断当前估计是否需要校正；若需要，调用交互预测器 $\mathcal{P}$ 生成修正并融合；否则直接使用去噪结果进入下一扩散步。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/002_Figure_2.jpg]]
*Figure 2: We present ground truth HOI sequences (left), object motions (middle), and objects relative to the contacts after coordinate transformations (right). Our key insight is to inject coordinate transformations into a diffusion model, as the relative motion shows simpler patterns that are easier to predict, e.g., rotating around a fixed axis (top) or being almost stationary (bottom)*



## 实验与关键发现

### 核心定量结果

InterDiff 在两个互补数据集上进行了系统验证：BEHAVE（含物体网格，可计算穿透指标）和 Human-Object Interaction（骨骼表示，含未见物体实例）。表1和表2分别展示了两个数据集上的主结果。

**表1（BEHAVE数据集）** 的核心发现：纯扩散模型（w/o correction）已显著优于传统基线。以人体关节误差 MPJPE-H 为例，InterDiff 达到 **140**，而 InterVAE 为 170、InterRNN 为 163。但关键瓶颈在于物理合理性——纯扩散模型的穿透指标 Pene. 高达 **228**。引入交互校正后，Pene. 降至 **164**（相对降低 28%），同时物体旋转误差 Rot.Err. 从 256 降至 **226**（降低 12%）。这表明校正步骤在几乎不影响人体关节精度（MPJPE-H 仅从 140 变为 139）的前提下，显著提升了物理一致性。

**表2（Human-Object Interaction 数据集）** 验证了泛化能力。在训练数据中未见过的物体实例上，全模型的物体关节误差 MPJPE-O 为 **84**，而纯扩散基线为 117（降低 28%）；物体位移误差 Trans.Err. 从 92 降至 **60**（降低 35%）。这组结果揭示了交互校正的间接收益：更精确的物体运动反过来约束了人体运动预测，形成正向反馈循环。

### 长时自回归预测

表3聚焦于最具挑战性的场景——自回归生成 100 帧（约 3.3 秒）未来交互。采用 Best-of-Many 评估（生成多个样本，报告最优指标）：

- **穿透抑制**：10 样本设置下，全模型 Pene. 为 **59**，纯扩散基线为 187（降低 68%）。即使仅 1 个样本，Pene. 也从 236 降至 88（降低 63%）。
- **人体运动改善**：MPJPE-H 从 361 降至 **348**（降低 3.6%），说明物理合理性的提升惠及人体运动预测本身——校正后的物体运动为人体提供了更可靠的交互参照。
- **样本效率**：校正的收益随样本数增加而扩大（Pene. 降低幅度从 63% 增至 68%），表明校正步骤与扩散模型的多样性生成能力协同增效。

### 用户研究

表4展示了感知物理真实性的两两比较结果。全模型以 **67.8%** 的胜率显著优于纯扩散基线及其他变体。这一主观评估与客观穿透指标高度一致，确认了交互校正带来的视觉改善——减少悬浮和穿透伪影——在人类感知层面同样显著。

### 消融实验

**交互校正的必要性**（表1、表3）：去除校正后，穿透指标恶化 28%–68%，物体运动误差同步增大。这证实纯扩散模型虽能生成合理的运动分布，但缺乏物理约束导致误差在长时预测中累积。

**局部参考系 vs 全局参考系**（图8）：仅使用全局参考系进行校正，物体运动精度在接触场景中明显下降。核心机制在于：相对于接触点的物体运动遵循简单模式（绕固定轴旋转或近于静止，见图2），而全局坐标系下的运动高度非线性。坐标变换将预测难度从复杂轨迹降低为局部简单模式。

**校正调度策略**（图8、图9）：取消接触/穿透检测的调度（即无条件校正或从不校正）损害长时生成质量。条件校正仅在检测到物理不合理时触发，避免了对合理交互的不必要扰动。

**DCT 基数量**（图A）：基数量设为 **10** 时，在物体旋转误差和位移误差之间取得最佳权衡。基数量过小（如 5）导致旋转预测精度不足，过大（如 20）则位移误差增大——过高的频率分量可能引入噪声。

**校正对人体运动的间接收益**（表3）：MPJPE-H 从 361 降至 348，确认了物体运动精度与人体运动精度之间的耦合关系。这一发现具有方法论意义：在交互生成中，改善物理合理性并非以牺牲运动精度为代价，反而能带来协同提升。

### 跨数据集泛化

图7展示了在 GRAB 数据集上的零样本泛化结果（仅在 BEHAVE 上训练）。模型能够直接泛化到包含新颖小尺寸物体的场景，表明 PointNet 物体编码器提取的几何特征具有一定的形状泛化能力，且局部参考系下的运动预测不依赖于特定物体类别。

### 失败模式与局限

1. **稀疏/间歇性接触**：物理校正依赖启发式接触检测（基于顶点距离阈值），当接触仅发生在少数帧或接触面积极小时，校正调度可能漏触发，导致穿透未被修正。
2. **复杂形状泛化**：对训练中未见过的复杂拓扑结构物体，PointNet 编码可能无法充分捕获几何细节，影响扩散模型的条件生成质量。
3. **计算效率**：每个扩散步需额外执行接触检测和 STGNN 前向传播，推理速度慢于纯扩散基线。论文未提供具体推理时间数据，需手动验证实际部署可行性。
4. **场景限制**：当前框架仅验证了单人-单个刚体交互，未涉及多物体、关节物体或手部精细操作。

### 实验公平性说明

- 由于任务新颖，InterVAE 和 InterRNN 由作者实现作为公平基线；CAHMP 和 HO-GCN 的结果直接引用自原论文。
- 骨骼表示数据集（Human-Object Interaction）不适用基于网格的接触/穿透损失，但仍报告所有其他指标。
- 所有方法均在 BEHAVE 上训练，跨数据集测试采用零样本设置。
- 长时预测采用自回归策略，Best-of-Many 评估考虑生成多样性。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on the BEHAVE dataset [6], demonstrating the effectiveness of our diffusion model and the correction*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on the Human-Object Interaction dataset [90]. We evaluate our model in challenging scenarios with unseen instances in the training data. The results show the effectiveness and generalizability of InterDiff and the correction. * marks results directly reported from [90]*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/008_Table_3.jpg]]
*Table 3: Quantitative results on the BEHAVE dataset [6]. We generate multiple predictions and report the lowest score across different samples. Here we focus on long-term forecasting, where we autoregressively generate 100 frames of future interactions. Our method with interaction correction outperforms pure diffusion, and the improvement is more significant with more samples*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/010_Table_4.jpg]]
*Table 4: User study on the BEHAVE dataset [6]. We obtain pairwise human voting results comparing our method with baselines and alternatives introduced in Sec. 4.4. Under human evaluation, the full model outperforms baselines regarding physical fidelity*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparisons on the BEHAVE dataset [6]. We show starting HOIs in gray and predicted HOIs sampled every 40 frames (30 FPS). The blue and red human meshes denote the results from InterDiff with and without interaction correction, respectively. The injected correction step helps mitigate contact floating and penetration artifacts, and maintain static objects when there is no contact*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results on interactions with unseen objects on the Human-Object Interaction dataset [90]. The predicted skeletons and objects are green and red respectively while GT is gray. We show five frames at 0.4, 0.8, 1.2, 1.6, and 2.0s*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative results on the BEHAVE dataset [6]. We place two different samples of the predicted interactions. Our approach can generate diverse and legitimate predictions*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/011_Figure_8.jpg]]
*Figure 8: Ablation study on the BEHAVE dataset [6]. We compare our pipeline with various alternatives introduced in Sec. 4.4. We normalize the scores of ‘full model’ to 0. The results show the superiority of ‘full model’ over others in the long horizon*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2308_16905/figures/014_Figure.jpg]]
*Figure: A. Ablation study on the BEHAVE dataset. We evaluate the long-term forecasting where we autoregressively generate 100 frames of future interactions. To balance the performance in predicting rotations and translations, we set the number of DCT bases to 10*



## 定位与知识库关联

### 任务定位：3D人-物交互预测的新基准

InterDiff 解决的是一个相对新颖的任务——从历史人-物交互（HOI）序列预测未来3D交互。该任务不同于纯人体运动预测或静态场景下的抓取生成，它要求同时建模人体运动、物体运动以及二者之间的物理交互约束。由于任务的新颖性，论文自行实现了两个基线模型以进行公平比较：**InterVAE**（基于VAE的序列生成模型）和**InterRNN**（基于LSTM的预测器），并引用了**CAHMP**（条件自回归Transformer人体运动预测）和**HO-GCN**（图卷积网络交互动作预测）的结果。

### 方法谱系：扩散模型 + 物理信息校正

从生成模型谱系看，InterDiff 的核心架构继承了条件去噪扩散概率模型（DDPM）的范式，直接预测干净信号而非噪声，这一选择使其区别于当时主流的VAE和RNN/LSTM路线。但纯扩散模型在物理交互场景中存在根本性瓶颈：生成结果常出现接触悬浮、穿透等违反物理法则的伪影，尤其在长时自回归预测中误差累积严重。

InterDiff 的关键贡献在于**将物理先验以可组合的方式注入扩散推理过程**，而非将物理约束硬编码进训练目标。具体而言，它在扩散反向过程中嵌入了一个独立的交互校正模块，该模块由三部分组成：

1. **校正调度器**：在每个扩散步骤评估去噪结果的物理合理性（接触/穿透状态），决定是否触发校正并选择合适的局部参考系。
2. **交互预测器（STGNN + DCT）**：在选定的局部参考系下，使用时-空图神经网络预测物体相对运动，再变换回全局坐标系。
3. **融合机制**：将校正后的物体运动注入扩散迭代，形成“扩散生成→物理检测→局部校正→扩散继续”的闭环。

这种“训练时解耦、推理时组合”的设计与**MPGD**（He et al., CVPR 2023）等将物理引导直接嵌入训练的方法形成对比——InterDiff 的扩散模型和校正模块可以独立训练，无需联合微调，这降低了训练复杂度并允许校正策略的灵活替换。

### 核心洞察：局部参考系的简化效应

InterDiff 的方法论创新根植于一个被论文显式表述的洞察：**相对于接触点的物体运动遵循简单且近于确定性的模式**。如 Figure 2 所示，全局坐标系下的物体运动可能复杂多变，但通过坐标变换将其转移至以接触点为中心的局部参考系后，运动模式显著简化——例如围绕固定轴旋转或近乎静止。这一洞察将高维的物体运动预测问题转化为低维的相对运动预测问题，是交互校正模块能够有效工作的前提。

### 适用边界与局限

**已验证的有效范围**：
- 单人与单个刚体物体的交互（BEHAVE、Human-Object Interaction 数据集）
- 跨数据集泛化（仅在BEHAVE上训练，在GRAB上直接测试仍有效）
- 长时自回归预测（100帧，约3.3秒）

**已知局限**：
1. **交互类型受限**：当前框架尚未扩展到多物体、关节物体或手部精细操作场景。这些场景中接触点定义和参考系选择将显著复杂化。
2. **接触检测的启发式依赖**：物理校正依赖于基于顶点距离和SDF的接触/穿透检测，对于稀疏或间歇性接触可能失效，导致漏校正或误校正。
3. **形状编码的泛化瓶颈**：模型高度依赖PointNet提取的物体几何特征，对训练中未见过的复杂形状泛化能力有限。Human-Object Interaction 数据集上的未见物体测试虽展现了初步泛化性，但该数据集的物体多样性仍有限。
4. **计算效率**：每个扩散步骤都需进行额外的接触检测和STGNN预测，且校正仅在扩散后期每隔几步执行一次，这虽降低了开销但仍增加了推理时间。

### 开放问题

1. **多方交互扩展**：如何将该框架扩展到多人协作或人-物-环境三方交互？此时“接触点”可能涉及多个主体，参考系定义和校正调度策略需要重新设计。

2. **与物理模拟器的深度结合**：当前校正基于数据驱动的STGNN预测，属于“软约束”。能否将校正模块与基于物理的模拟器（如MuJoCo）结合，在扩散过程中引入硬物理约束？这将可能进一步提升长时预测的物理一致性。

3. **下游任务驱动**：生成的交互序列能否用于驱动下游任务（如机器人操作策略学习）？这需要探索如何利用强化学习或模仿学习将InterDiff的生成能力转化为可执行的控制策略。

4. **动态物体形状场景**：在可变形物体（如衣物、绳索）的交互场景中，物体形状随时间变化，此时局部参考系的定义和相对运动预测范式需要根本性调整——当前基于刚性变换的坐标变换框架不再适用。



## 原文 PDF

![[paperPDFs/ICCV_2023/InterDiff:_Generating_3D_Human-Object_Interactions_with_Physics-Informed_Diffusion.pdf]]

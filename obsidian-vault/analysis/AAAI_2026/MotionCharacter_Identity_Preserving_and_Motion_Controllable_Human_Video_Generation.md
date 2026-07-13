---
title: "MotionCharacter: Identity-Preserving and Motion Controllable Human Video Generation"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/MotionCharacter_Identity_Preserving_and_Motion_Controllable_Human_Video_Generation.pdf
project_link: https://motioncharacter.github.io/
code_link: null
aliases:
- MotionCharacter
tags:
- AAAI_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过引入运动控制模块，将运动显式解耦为动作类型（文本）和运动强度（光流），从而实现独立、精细且连续的运动幅度调节。"
primary_logic: "显式分离动作语义与运动幅度，利用光流作为连续强度信号并辅以区域感知损失，能够在保持身份一致性的同时，实现可预测的细粒度运动控制。"
claims:
- "MotionCharacter将运动显式解耦为动作类型和运动强度两个独立可控的组件。"
- "运动控制模块利用文本短语指定动作类型，利用从光流导出的可量化指标调节强度。"
- "ID内容插入模块与ID一致性损失确保在动态运动中稳健的身份保持。"
- "Unsplash-50 test set 上 Face Similarity = 0.609"
---

# MotionCharacter: Identity-Preserving and Motion Controllable Human Video Generation

> [!tip] 核心洞察
> 显式分离动作语义与运动幅度，利用光流作为连续强度信号并辅以区域感知损失，能够在保持身份一致性的同时，实现可预测的细粒度运动控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionCharacter：身份保持与运动可控的人物视频生成 |
| 英文题名 | MotionCharacter: Identity-Preserving and Motion Controllable Human Video Generation |
| 会议/期刊 | AAAI 2026 |
| Links | [paper](https://arxiv.org/abs/2411.18281) · [Project](https://motioncharacter.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | MotionCharacter |
| Dataset | Unsplash-50 test set |

> [!tip] 效果简介
> - Unsplash-50 test set 上，Face Similarity 为 0.609，对比 0.617 (IPA-FaceID-PlusV2)，变化 -0.008。
> - Unsplash-50 test set 上，Dynamic Degree 为 0.449，对比 0.085 (IPA-FaceID-PlusV2)，变化 +0.364。
> - Unsplash-50 test set 上，Dover Score (Overall Quality) 为 0.869，对比 N/A (最佳基线未报告具体数值)，变化 N/A。

## 概要

**核心问题**：现有主体驱动的文本到视频（T2V）生成方法在运动控制上存在根本性瓶颈——文本描述中动作语义（“做什么”）与运动幅度（“做多大”）天然纠缠，导致无法对运动强度进行细粒度、连续调节。例如，提示词“slightly open mouth”与“widely open mouth”之间的微妙差异难以被模型可靠解析。

**核心思路**：MotionCharacter 将运动显式解耦为两个独立可控的组件——动作类型（由文本短语指定）和运动强度（由光流导出的连续标量信号），从而实现对人物运动的精细、可预测控制。这一解耦设计是全文的因果杠杆：它使模型能够独立地调节“做什么”和“做多大”，而不牺牲身份一致性。

**方法定位**：框架由三个核心模块构成。**ID内容插入模块**融合CLIP与ArcFace嵌入，通过交叉注意力将参考身份注入扩散模型，辅以ID一致性损失锚定主体面容。**运动控制模块**采用并行交叉注意力分别注入动作嵌入（文本语义）和运动强度嵌入（光流衍生信号），实现解耦控制。**区域感知损失**利用光流掩码对高运动区域加权，提升运动区域的生成质量和空间连贯性。

**主要结果**：在Unsplash-50测试集上，MotionCharacter 在面容相似度（0.609）与基线方法接近的前提下，将动态程度大幅提升至0.449，远超身份保持基线 **IPA-FaceID-PlusV2** 的0.085。消融实验表明，运动控制模块使动态程度提升83.3%（从0.245到0.449），区域感知损失和ID一致性损失分别贡献了Dover分数+0.059和面容相似度+0.104的增益，验证了各模块的独立有效性。



### 问题背景

主体驱动的人物视频生成旨在根据给定的参考身份图像和文本描述，合成一段保持人物身份一致性的动态视频。该任务的核心挑战在于同时满足两个相互制约的目标：**身份保真度**（生成的人物在面容、特征上忠实于参考图像）与**运动自然度**（生成的动作连贯、幅度合理）。现有方法在这两个维度上往往难以兼得——身份保持能力强的模型通常生成近乎静态的视频，而运动表现力强的模型则容易导致身份漂移。

### 现有方法的核心瓶颈

当前主体驱动文本到视频（T2V）生成方法面临一个根本性困境：**动作语义与运动幅度在文本描述中天然纠缠**。当用户试图通过文本提示控制运动时，诸如“slightly open mouth”与“widely open mouth”这样的表述，其动作类型（张嘴）与运动强度（轻微/大幅）被耦合在同一个语言表达中。扩散模型难以从这种隐式、模糊的描述中解析出精确的运动幅度，导致生成结果要么运动不足，要么运动过度且身份失真。

以零样本基线 **ID-Animator**（He et al., 2024）为例，其仅通过文本隐式描述运动幅度，无法实现细粒度的连续调节。而身份保持能力最强的 **IPA-FaceID-PlusV2** 虽然面容相似度达到 0.617，但动态程度仅 0.085，几乎不产生有意义的运动。这种“身份-运动”的跷跷板效应揭示了文本作为唯一控制信号的表达能力不足。

### 本文动机与核心思路

针对上述瓶颈，MotionCharacter 提出将运动控制**显式解耦**为两个独立可操作的维度：**动作类型**（action type）与**运动强度**（motion intensity）。动作类型通过文本短语指定动作语义（如“open mouth”、“turn head”），运动强度则通过从光流中导出的连续标量信号进行量化调节。这一解耦设计使得用户可以在不改变动作语义的前提下，独立地、连续地调节运动幅度——从细微的表情变化到大幅的头部转动。

为实现这一解耦控制，框架引入了三个关键组件：

- **运动控制模块**：通过两个并行的交叉注意力分支，分别注入动作嵌入（文本语义）和运动强度嵌入（光流信号），使扩散模型能够分别响应“做什么动作”和“做多大动作”两个正交指令。
- **ID内容插入模块**：融合 CLIP 全局语义与 ArcFace 细粒度身份特征，通过交叉注意力将身份嵌入注入扩散过程，并以 ID 一致性损失（余弦相似度）锚定主体身份，防止运动增强导致的面容漂移。
- **区域感知损失**：利用归一化光流掩码对高运动区域施加更高权重，使模型在训练时重点关注运动区域的生成质量，从而提升运动保真度与空间连贯性。

通过这种“语义-强度”分离的控制范式，MotionCharacter 旨在打破身份保持与运动表现力之间的固有权衡，实现可预测的、细粒度的人物视频生成。



## 核心方法与创新机理

MotionCharacter 的核心创新在于将人物视频生成中的**运动控制显式解耦为两个独立可调的维度**——动作类型与运动强度，从而解决了现有主体驱动文本到视频（T2V）方法中动作语义与运动幅度固有纠缠的瓶颈问题。

### 从隐式描述到显式解耦：运动控制表示的范式转变

现有方法（如 **ID-Animator**，He et al., 2024）仅通过文本提示隐式地描述运动幅度（例如“open mouth slightly”），这导致两个根本性缺陷：其一，文本对运动幅度的表达能力有限，“slightly”与“widely”之间的连续谱系无法被精确刻画；其二，动作语义与运动强度在文本嵌入空间中天然耦合，用户无法独立调节“做什么动作”与“动作做多大”。

MotionCharacter 的核心突破在于将运动控制表示重构为两个正交的组件（Figure 1 直观对比了这一范式差异）：

- **动作类型**：由文本短语指定，承载动作的语义信息（如“open mouth”、“turn head”），通过 CLIP 文本编码器提取嵌入后注入扩散模型。
- **运动强度**：由从光流导出的连续标量值 $\mathcal{M}$ 量化，定义为相邻帧间前景光流均值的帧间平均（$\mathcal{M} = \frac{1}{N-1} \sum_{i=1}^{N-1} f_{i,fg}$），训练时从真实视频中提取，推理时由用户直接指定。

这一解耦设计的因果机理在于：**文本嵌入捕获“做什么”的离散语义，光流信号提供“做多大”的连续强度信息**，二者通过运动控制模块中的并行交叉注意力机制（$Z'' = \mathrm{Attn}(Q', K^a, V^a) + \alpha \cdot \mathrm{Attn}(Q', K^m, V^m)$）独立注入生成过程。消融实验（Table 3）证实，运动控制模块（MCM）的引入将动态程度（Dynamic Degree）从 0.245 提升至 0.449，增幅达 83.3%，验证了显式解耦对运动表达能力的决定性提升。

### 从通用损失到身份锚定：身份保持机制的专项强化

基线方法依赖标准扩散损失进行训练，缺乏专门的身份约束机制，导致在动态运动中主体面容容易漂移。虽然 **IPA-FaceID-PlusV2** 在静态场景下面容相似度达到 0.617（Table 1），但其动态程度仅为 0.085，暴露出身份保持与运动生成之间的尖锐矛盾。

MotionCharacter 通过两个协同组件重构了身份保持机制：

- **ID 内容插入模块**：首先从参考图像中隔离面部区域以滤除背景干扰，然后通过交叉注意力融合 CLIP 嵌入（提供全局上下文）与 ArcFace 嵌入（捕获细粒度身份细节），生成紧凑的身份嵌入 $C_{id}$，最终以残差形式注入扩散模型的交叉注意力层（$z' = \operatorname{Attn}(Q, K^t, V^t) + \lambda \cdot \operatorname{Attn}(Q, K^i, V^i)$）。
- **ID 一致性损失**：在身份特征空间中直接最小化参考身份与生成帧之间的余弦距离（$\mathcal{L}_{id} = 1 - \frac{1}{N} \sum_{i=1}^{N} \frac{\phi(I) \cdot \phi(X_i^f)}{|\phi(I)| |\phi(X_i^f)|}$），将身份约束从像素空间提升至语义特征空间。

消融实验（Table 2）表明，单独引入 ID 一致性损失可使面容相似度提升 +0.104，而完整模型在面容相似度 0.609 与动态程度 0.449 之间取得了最佳平衡——相比 IPA-FaceID-PlusV2，在仅牺牲 0.008 面容相似度的代价下，换取了 +0.364 的动态程度增益。

### 从均匀优化到运动感知：区域感知损失的精细化监督

基线方法采用的像素级 MSE 损失对所有空间位置施加均等权重，忽视了不同区域对运动质量的差异化贡献。MotionCharacter 引入**区域感知损失**（$\mathcal{L}_{R}$），利用归一化的光流掩码 $M_{i,\mathrm{norm}}$ 对高运动区域施加更高权重，迫使模型将优化重心集中于运动显著区域。

该设计的因果逻辑在于：光流幅度天然指示了像素的运动活跃程度，将其作为损失权重掩码，等价于在训练过程中向模型注入“哪些区域更需要精确建模”的先验知识。消融实验（Table 2）证实，区域感知损失将 Dover 分数提升 +0.059，动态程度提升 +0.064，且完整模型（联合 $\mathcal{L}_{R}$ 与 $\mathcal{L}_{id}$）在所有指标上均优于单独使用任一损失，验证了运动质量监督与身份约束之间的协同效应。

### 创新边界与待验证假设

需要指出，MotionCharacter 的运动强度控制依赖于光流作为中间表示，其细粒度上限受限于 RAFT 光流模型的精度。论文明确承认框架性能本质上受底层 T2V 基模型能力约束，且尚未在更强大的视频基础模型（如 Wan 系列）上验证泛化性。此外，Table 1 中 Dover 分数（0.869）的最佳基线数值未明确报告，该优势幅度的精确性需对照原始数据进一步确认。



![[assets/figures/papers/paper_list_l15_MotionCharacter_Identity_Preserving_and_Motion_Controllable_Human_Video/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of subject-driven T2V methods and our proposed MotionCharacter framework. Existing approaches specify coarse actions (e.g., “open mouth”) but struggle to capture nuanced motion magnitude (e.g., “slightly” vs. “widely”). In contrast, MotionCharacter decouples action type and motion intensity, enabling finegrained, continuous control over human motion while preserving subject fidelity*

MotionCharacter 的整体框架将人物视频生成形式化为一个条件映射：

$$\mathcal{V} = \mathcal{F}(\mathcal{I}, \mathcal{P}, \mathcal{A}, \mathcal{M})$$

其中 $\mathcal{I}$ 为参考身份图像，$\mathcal{P}$ 为文本提示，$\mathcal{A}$ 为动作短语，$\mathcal{M}$ 为运动强度，模型 $\mathcal{F}$ 输出视频 $\mathcal{V}$。这一形式化的核心设计在于将运动控制显式解耦为两个独立组件——动作类型（语义）与运动强度（连续信号），从而突破现有方法中文本语义与运动幅度内在纠缠的瓶颈。

框架由三个核心模块构成（图2）：

1. **ID 内容插入模块（ID Content Insertion Module）**：接收参考身份图像 $\mathcal{I}$，提取并融合 CLIP 与 ArcFace 嵌入，通过交叉注意力注入扩散模型，确保生成过程中身份特征的稳定保持。

2. **运动控制模块（Motion Control Module）**：采用两个并行的交叉注意力分支，分别注入动作嵌入 $E_A$（由动作短语 $\mathcal{A}$ 编码）和运动强度嵌入 $E_M$（由光流导出的连续标量 $\mathcal{M}$ 编码），实现动作语义与运动幅度的独立调控。

3. **复合损失函数**：联合优化区域感知损失 $\mathcal{L}_R$ 和 ID 一致性损失 $\mathcal{L}_{id}$。$\mathcal{L}_R$ 利用归一化光流掩码对高运动区域施加更高权重，提升运动区域的生成质量；$\mathcal{L}_{id}$ 在身份特征空间中最小化参考身份与生成帧之间的余弦距离，锚定主体身份。

训练阶段，运动强度 $\mathcal{M}$ 通过 RAFT 模型从训练视频中提取前景光流并取帧间均值得到；推理阶段，用户可直接指定动作短语和运动强度值，实现细粒度、连续的运动幅度调节。训练策略采用图像-视频混合范式，引入约 17,619 张静态风格人像复制为 16 帧零运动序列，提供“零强度校准”信号以稳定训练。



MotionCharacter 的核心架构由三个关键模块协同构成：**ID内容插入模块**负责身份保持，**运动控制模块**实现解耦的运动类型与强度调节，**复合损失函数**则通过区域感知损失和身份一致性损失联合优化生成质量。

### ID内容插入模块

该模块的目标是将参考图像的身份信息稳健地注入扩散模型。首先从参考图像 $I$ 中隔离面部区域以滤除背景干扰，随后提取两类互补的身份特征：CLIP嵌入捕获全局语义上下文，ArcFace嵌入提供细粒度的身份判别信息。两者通过交叉注意力融合并投影，得到统一身份嵌入 $C_{id}$：

$$C_{id} = \mathrm{Proj}(\mathrm{Attn}(E_{arc} W_q', E W_k', E W_v'))$$

其中 $E_{arc}$ 为ArcFace嵌入，$E$ 为CLIP嵌入，$W_q', W_k', W_v'$ 为可学习的投影矩阵。该身份嵌入通过双交叉注意力机制注入扩散模型的UNet，与文本交叉注意力并行：

$$z' = \operatorname{Attn}(Q, K^t, V^t) + \lambda \cdot \operatorname{Attn}(Q, K^i, V^i)$$

其中 $Q$ 为隐空间特征，$K^t, V^t$ 为文本条件，$K^i, V^i$ 为身份条件，$\lambda$ 控制身份影响程度。

### 运动控制模块

运动控制模块的核心创新在于将运动显式解耦为**动作类型**（文本语义）和**运动强度**（连续标量）两个独立可控的维度。

**运动强度估计**：训练阶段，使用RAFT模型提取相邻帧间的光流 $f_{i,(x,y)} = \Theta(v_i^{in}, v_{i+1}^{in})$，通过二值掩码 $M_{i,(x,y)}$ 提取前景像素的平均光流大小：

$$f_{i,fg} = \frac{1}{S} \sum_{x=1}^{H} \sum_{y=1}^{W} M_{i,(x,y)} * f_{i,(x,y)}$$

对所有帧对取平均，得到视频的连续运动强度信号：

$$\mathcal{M} = \frac{1}{N-1} \sum_{i=1}^{N-1} f_{i,fg}$$

**运动条件注入**：推理阶段，用户可自定义动作短语 $\mathcal{A}$ 和运动强度 $\mathcal{M}$。模块通过两个并行的交叉注意力分支分别注入动作嵌入 $E_A$ 和运动强度嵌入 $E_M$：

$$Z'' = \mathrm{Attn}(Q', K^a, V^a) + \alpha \cdot \mathrm{Attn}(Q', K^m, V^m)$$

这一设计使得动作语义与运动幅度完全解耦，用户可独立调节两者——例如固定“张嘴”动作，将强度从5（微张）连续调节至20（大张）。

### 复合损失函数

**区域感知损失** $\mathcal{L}_{R}$：利用归一化光流掩码对高运动区域施加更高权重，迫使模型聚焦于动态区域的生成质量。掩码归一化公式为：

$$M_{i,\mathrm{norm}} = \mathrm{clip}\left(\frac{f_{i,fg}(x,y)}{255} + \delta, 1.0, 1.0+\delta\right)$$

区域感知损失定义为：

$$\mathcal{L}_{R} = \frac{1}{N H' W'} \sum_{i=1}^{N} \sum_{x=1}^{H'} \sum_{y=1}^{W'} M_{i,\mathrm{norm}} \cdot [\epsilon_i(x,y) - \hat{\epsilon}_i(x,y)]^2$$

其中 $\epsilon_i$ 为真实噪声，$\hat{\epsilon}_i$ 为预测噪声，$M_{i,\mathrm{norm}}$ 确保运动幅度越大的像素区域对损失贡献越大。

**ID一致性损失** $\mathcal{L}_{id}$：在身份特征空间中锚定主体身份，最小化参考身份嵌入 $\phi(I)$ 与各生成帧嵌入 $\phi(X_i^f)$ 之间的余弦距离：

$$\mathcal{L}_{id} = 1 - \frac{1}{N} \sum_{i=1}^{N} \frac{\phi(I) \cdot \phi(X_i^f)}{|\phi(I)| |\phi(X_i^f)|}$$

**总目标函数**联合优化运动保真度与身份一致性：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{R} + \lambda_{id} \cdot \mathcal{L}_{id}$$

消融实验证实了两者的协同效应：单独使用 $\mathcal{L}_{R}$ 使动态程度提升+0.064、Dover分数提升+0.059；单独使用 $\mathcal{L}_{id}$ 使面容相似度提升+0.104；完整模型达到面容相似度0.609和动态程度0.449的最优平衡。



## 实验与关键发现

### 核心定量结果

MotionCharacter 在 Unsplash-50 测试集上与多个基线方法进行了全面比较。表 1 报告了六项指标的结果，所有方法均使用空动作短语并将运动强度固定为 20，以确保公平比较。

![[assets/figures/papers/paper_list_l15_MotionCharacter_Identity_Preserving_and_Motion_Controllable_Human_Video/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods. Higher values (↑) indicate better performance. Bold and underlined numbers denote the best and second-best results, respectively. All methods use an empty action phrase with motion intensity set to 20 for fair comparison*

**身份保持与运动动态的权衡突破。** 现有方法在身份保持和运动动态之间存在显著矛盾：**IPA-FaceID-PlusV2** 取得了最高的面容相似度（Face Similarity = 0.617），但其动态程度（Dynamic Degree）仅为 0.085，几乎无法生成有意义的运动；**ID-Animator**（He et al., 2024）作为零样本身份保持主体驱动 T2V 基线，虽然能产生一定动态效果，但缺乏细粒度的运动强度控制。MotionCharacter 以面容相似度 0.609（仅比最佳身份基线低 0.008）换取了动态程度 0.449 的巨大提升（+0.364），在身份保持与运动质量之间实现了目前最优的平衡点。

**整体质量与内容一致性领先。** MotionCharacter 在 Dover Score（整体质量评估）上达到 0.869，在六项指标中的五项取得最优或次优结果，包括运动属性（motion attributes）和内容一致性指标（CLIP-I、CLIP-T）。这表明解耦运动控制不仅没有损害生成质量，反而通过显式建模运动信号提升了视频的整体连贯性。

**用户偏好验证。** 用户调研（Figure 4）从身份一致性、运动可控性和整体视频质量三个维度进行评估，MotionCharacter 在所有维度上均获得最高偏好比例，确认了客观指标与人类主观判断的一致性。

### 消融实验：各模块的因果贡献

消融实验从两个层面揭示了核心设计的有效性。

**损失函数消融（Table 2）。** 以基础模型（无特殊损失）为起点，逐步添加区域感知损失 $\mathcal{L}_R$ 和 ID 一致性损失 $\mathcal{L}_{id}$：
- 单独引入 **区域感知损失** $\mathcal{L}_R$ 使 Dover Score 提升 +0.059，动态程度提升 +0.064，验证了光流掩码加权机制能有效引导模型关注高运动区域，提升运动清晰度。
- 单独引入 **ID 一致性损失** $\mathcal{L}_{id}$ 使面容相似度大幅提升 +0.104，确认了在身份特征空间中进行余弦距离约束对锚定主体身份的关键作用。
- **完整模型**（$\mathcal{L}_R + \mathcal{L}_{id}$）达到面容相似度 0.609 和动态程度 0.449，在各自领域均超越单独使用对应损失的配置，展现出两种损失的**协同效应**——身份损失不仅未抑制运动，反而与运动损失共同提升了整体性能。

![[assets/figures/papers/paper_list_l15_MotionCharacter_Identity_Preserving_and_Motion_Controllable_Human_Video/figures/005_Table_2.jpg]]
*Table 2: Ablation study of the Region-Aware Loss $\mathcal { L } _ { R }$ and the ID-Consistency Loss $\mathcal { L } _ { i d }$

**运动控制模块消融（Table 3）。** 移除运动控制模块（MCM）后，动态程度从 0.449 骤降至 0.245，降幅达 83.3%。这一结果直接证明了将运动显式解耦为动作类型（文本）和运动强度（光流）并通过并行交叉注意力注入的设计，是实现细粒度运动控制的核心因果机制。

![[assets/figures/papers/paper_list_l15_MotionCharacter_Identity_Preserving_and_Motion_Controllable_Human_Video/figures/007_Table_3.jpg]]
*Table 3: Ablation study of Motion Control Module (MCM)*

### 定性分析

Figure 3 展示了不同身份（男性、女性、名人、非名人）和多样化动作短语下的生成对比。在静态场景（如 "null" 空动作短语）中，MotionCharacter 与身份保持基线 IPA-FaceID-PlusV2 表现接近，面容一致性良好；在动态场景中，基线方法要么运动幅度不足，要么出现身份漂移，而 MotionCharacter 在保持身份一致的同时生成了清晰可控的运动。

附录中的 Figure II 和 Figure III 进一步验证了解耦控制能力：Figure II 证明模型能对 "turn head"、"smile"、"talk, hold a microphone" 等简单及复合动作指令生成对应运动；Figure III 展示了对同一动作 "open mouth" 在不同强度级别（5 到 25）下的连续渐变效果，低强度值产生细微动作，高强度值生成显著运动，验证了运动强度的连续可控性。

### 失败模式与局限性

尽管 MotionCharacter 在整体指标上表现优异，论文明确指出了以下局限：
1. **复杂精细运动捕捉不足**：在处理高度复杂或精细的运动序列时，细粒度运动动态可能无法被有效捕捉，光流作为单一强度信号可能不足以描述多关节协同的复杂动作。
2. **基模型能力依赖**：框架性能本质上受限于底层 T2V 基模型的能力上限，生成视频的整体保真度无法超越基模型的固有局限。
3. **泛化性未验证**：尚未在更强大的视频基础模型（如 Wan 系列）上验证适配性和泛化能力，跨基模型的迁移效果需要进一步研究。



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有主体驱动文本到视频（T2V）生成方法的核心瓶颈在于：动作语义与运动幅度在文本描述中固有地纠缠在一起。例如，提示词“slightly open mouth”与“widely open mouth”试图通过副词区分强度，但文本嵌入空间对这类连续幅度的编码是模糊且不可靠的。这导致两个直接后果：一是无法对运动强度进行细粒度、连续的控制；二是在追求高动态表现时，主体身份一致性急剧下降。

MotionCharacter的因果调节旋钮是：**将运动显式解耦为动作类型（文本语义）和运动强度（光流导出的连续标量）两个独立可控的组件**。这一解耦使得模型可以独立操纵“做什么动作”和“动作幅度多大”，从而在保持身份一致性的前提下实现可预测的细粒度运动控制。

### 2. 与基线方法的关系

**ID-Animator**（He et al., 2024）是零样本身份保持主体驱动T2V的代表性基线。它通过文本提示同时描述动作类型和幅度，但缺乏专门的强度控制机制。MotionCharacter在其基础上引入了运动控制模块（Motion Control Module），将原本隐式耦合于文本的运动幅度显式化为连续标量信号，补齐了细粒度强度调节的能力缺口。

**IPA-FaceID-PlusV2**在身份保持方面表现最强（Face Similarity达0.617），但其动态程度极低（Dynamic Degree仅0.085），本质上是牺牲运动能力换取身份保真度。MotionCharacter通过ID内容插入模块（融合CLIP与ArcFace嵌入）配合ID一致性损失，在保持竞争性面容相似度（0.609，仅下降0.008）的同时，将动态程度提升至0.449（增幅超5倍），实现了身份保持与运动表现之间更优的帕累托前沿。

### 3. 框架适用边界

MotionCharacter的有效性建立在以下前提之上：

- **底层T2V基模型的能力上限**：框架性能本质上依赖于所采用的扩散模型基础架构，生成视频的保真度、分辨率和时序连贯性受限于基模型。论文明确指出尚未在更强大的视频基础模型（如Wan系列）上验证适应性。
- **运动复杂度的上限**：在处理高度复杂或精细的运动序列（如快速连续的表情变化、大幅度肢体动作与面部细节的耦合）时，细粒度运动动态可能无法被有效捕捉。光流作为强度信号虽然连续，但其对非刚性形变和遮挡的鲁棒性存在天然局限。
- **身份保持的锚定机制**：ID一致性损失通过余弦相似度锚定主体身份，这在单一主体、正面或近正面姿态下效果显著，但在极端姿态、遮挡或多人场景下的泛化性尚未验证。

### 4. 局限与开放问题

**已知局限**：
1. 细粒度运动动态的捕捉能力不足，面对高度复杂运动序列时可能出现运动模糊或幅度失真。
2. 框架对底层基模型的强依赖限制了生成质量的上限，尚未验证跨模型架构的泛化性。
3. 训练数据中通过静态图像复制构建零强度校准样本的策略，可能引入运动伪影或时序不一致的风险。

**开放问题**：
1. 如何在保持身份一致性的同时增强对复杂、精细运动动态的捕捉？可能的路径包括引入更高阶的运动表示（如场景流、关键点轨迹）或设计自适应强度调制机制。
2. 如何将MotionCharacter的运动解耦范式适配到更先进的视频基础模型（如Wan系列），以提升生成保真度和泛化能力？这需要重新设计身份注入和运动条件模块的接口。
3. 当前的运动强度信号依赖于预训练的RAFT光流提取器，其误差传播对最终生成质量的影响尚未量化分析。是否可以通过端到端学习或自监督信号替代外部光流估计器，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/AAAI_2026/MotionCharacter_Identity_Preserving_and_Motion_Controllable_Human_Video_Generation.pdf]]

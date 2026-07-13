---
title: "InfiniDreamer: Arbitrarily Long Human Motion Generation via Segment Score Distillation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score_Distillation.pdf
project_link: null
code_link: null
aliases:
- InfiniDreamer
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 分段分数蒸馏（SSD）通过滑动窗口采样重叠短片段，利用对齐损失与几何损失优化整个长序列，使每个局部片段与预训练短运动先验对齐，从而控制局部保真度与全局连贯性。
primary_logic: 将分数蒸馏引入长运动生成，无需额外长序列训练，仅通过对重叠短片段进行迭代优化，即可同时实现局部保真与全局一致性。
claims:
- InfiniDreamer在HumanML3D和BABEL上全面超越之前的训练无关方法，特别是FID和R-precision显著提升。
- 移除梯度掩码（gradient masks）或几何损失（geometric losses）后性能下降，说明SSD的设计组件至关重要。
- 滑动窗口尺寸W的消融表明，适中的上下文长度有利于过渡段生成，过长或过短都会降低质量。
- SSD优化中的文本条件选择策略对性能有显著影响，无监督优化或固定提示都会导致性能下降。
---

# InfiniDreamer: Arbitrarily Long Human Motion Generation via Segment Score Distillation

> [!tip] 核心洞察
> 将分数蒸馏引入长运动生成，无需额外长序列训练，仅通过对重叠短片段进行迭代优化，即可同时实现局部保真与全局一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | InfiniDreamer：通过分段分数蒸馏生成任意长度人体运动 |
| 英文题名 | InfiniDreamer: Arbitrarily Long Human Motion Generation via Segment Score Distillation |
| 会议/期刊 | ICCV 2025 |
| Links |  [paper](https://arxiv.org/abs/2411.18303)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InfiniDreamer |
| Dataset | HumanML3D, BABEL |

> [!tip] 效果简介
> - HumanML3D 上，R-precision ↑ 0.679 ± 0.007 vs 0.605 ± 0.006 (DiffCollage) (+0.074)；FID ↓ 0.47 ± 0.12 vs 1.07 ± 0.05 (DiffCollage) (-0.60)；MultiModal-Dist ↓ 3.15 ± 0.01 vs 3.62 ± 0.01 (DiffCollage) (-0.47)。
> - BABEL 上，R-precision ↑ 0.543 ± 0.009 vs 0.487 ± 0.009 (DiffCollage) (+0.056)；FID ↓ 0.97 ± 0.09 vs 1.14 ± 0.05 (DoubleTake) (-0.17)；Transition FID ↓ 2.07 ± 0.30 vs 3.54 ± 0.10 (DoubleTake) (-1.47)。

## 概要

### 问题与瓶颈

生成任意长度的人体运动序列是计算机视觉与图形学中的一项核心挑战。其根本瓶颈在于**高质量长序列数据的匮乏**：现有运动扩散模型大多仅在短片段（如70–200帧）上训练，难以直接泛化到长序列。传统解决方案沿两条路径展开：

- **自回归生成**（如TEACH）：逐段生成后续运动，以前一段的尾部作为条件。这种方法会因误差逐步累积而出现**运动漂移、重复模式与语义退化**。
- **基于补全（inpainting）的方法**（如DoubleTake/PriorMDM、DiffCollage、MultiDiffusion）：先生成各子动作段，再补全段间的过渡区域。这类方法在段边界处容易产生**运动突变**，且补全过程可能**覆盖或扭曲已有的动作内容**。

此外，**FlowMDM**等微调方法虽然通过混合位置编码扩展了模型对长序列的适应能力，但微调过程会在短片段上引入干扰，且仍依赖长序列训练数据。

### 核心方法：InfiniDreamer 与分段分数蒸馏

**InfiniDreamer**（2025）提出了一种**无需训练**的长序列运动生成框架，其核心创新是**分段分数蒸馏（Segment Score Distillation, SSD）**。该方法将分数蒸馏采样（Score Distillation Sampling, SDS）从图像生成领域引入运动生成，通过以下机制实现局部保真与全局连贯的统一：

1. **运动序列初始化**：利用预训练短运动扩散模型（MDM）按文本提示生成各子动作段，并在段间插入随机初始化的过渡段，构建粗长序列。
2. **滑动窗口重叠采样**：以固定窗口大小 $W$ 和步长 $P$ 从粗序列中重叠采样短片段，确保过渡段被充分覆盖。
3. **SSD迭代优化**：对每个采样片段加噪后，通过冻结的预训练运动扩散模型预测去噪信号，计算**对齐损失** $\mathcal{L}_{align}$（预测干净运动与原始片段的加权L2距离）与三项**几何损失**——位置损失 $\mathcal{L}_{pos}$（前向运动学一致性）、脚部接触损失 $\mathcal{L}_{foot}$（抑制脚步滑动）、速度正则化 $\mathcal{L}_{vel}$（保持运动平滑性），反向传播更新整个长序列。通过**梯度掩码**（gradient masks）分区控制各段优化强度，避免子动作段被过度修改。

**因果调控的关键**在于：SSD使每个局部短片段与预训练短运动先验对齐，而重叠采样与联合优化将局部约束传播至全局，从而同时保证单段语义准确性与段间过渡的自然流畅。

### 方法定位

InfiniDreamer属于**训练无关（training-free）的扩散模型引导式长序列生成方法**，与以下基线形成对比：

| 方法 | 策略 | 局限 |
|------|------|------|
| **DoubleTake (PriorMDM)** | 扩散模型补全过渡段 | 段边界突变，内容覆盖 |
| **DiffCollage** | 扩散模型组合 | 过渡段质量不稳定 |
| **MultiDiffusion** | 多扩散运动组合 | 全局一致性不足 |
| **TEACH** | 自回归逐段生成 | 误差累积，运动漂移 |
| **FlowMDM** | 混合位置编码微调 | 需长序列训练，短片段干扰 |

InfiniDreamer的独特优势在于**无需任何长序列训练数据**，仅依赖短片段预训练模型，通过SSD优化实现长序列生成，在HumanML3D和BABEL两个标准基准上全面超越同类训练无关方法。

### 主要结果

**定量表现**（均运行10次取均值±标准差）：

- **HumanML3D**：R-precision达到 **0.679 ± 0.007**（DiffCollage为0.605），FID降至 **0.47 ± 0.12**（DiffCollage为1.07），MultiModal-Dist降至 **3.15 ± 0.01**（DiffCollage为3.62），全面领先。
- **BABEL**：R-precision达到 **0.543 ± 0.009**（DiffCollage为0.487），FID降至 **0.97 ± 0.09**（DoubleTake为1.14），过渡段FID（Transition FID）从DoubleTake的3.54大幅降至 **2.07 ± 0.30**，验证了SSD对过渡段质量的显著提升。

**消融实验关键发现**：
- 移除**梯度掩码**后所有指标下降，说明分区控制优化强度对长序列质量至关重要。
- 移除**几何损失**导致FID和过渡FID上升，证实几何约束有助于运动真实感。
- 滑动窗口尺寸 $W$ 过小或过大均降低过渡段质量，适中值（$W=120$）在HumanML3D上取得最优过渡FID。
- 步长 $P \geq W$ 时部分帧不被采样，过渡段（初始随机）几乎成为噪声，严重损害质量。
- 使用不匹配的文本提示（如固定为“transition”或“motion”）或无条件优化均导致性能显著下降，验证了自适应文本条件策略的有效性。

**定性表现**：与DoubleTake相比，InfiniDreamer生成的过渡段更平滑，无停顿或漂移；与FlowMDM相比，InfiniDreamer展现出更强的上下文理解能力（如根据后续“downstairs”提示生成“go upstairs”过渡），且对细粒度文本（如“side steps”）的语义遵循更准确。

### 局限与开放问题

InfiniDreamer的生成质量受限于底层短序列模型MDM的性能，且推理速度较慢（生成520帧约需4分钟），对超参数（学习率 $\eta$、窗口尺寸 $W$、步长 $P$）较为敏感。未来方向包括提升推理效率以支持实时交互、设计更强的短序列先验模型、以及研究SSD优化中噪声累积对长序列末端质量的影响。

### 长序列人体运动生成的现实需求

生成任意长度的人体运动序列在动画制作、虚拟现实、人机交互和游戏开发等领域具有广泛的应用前景。理想情况下，系统应能根据一组文本描述（例如“一个人向前走，然后慢跑，接着坐下”）生成一段连贯、流畅且语义匹配的长运动序列。然而，现有方法面临一个核心瓶颈：**缺乏高质量的长序列运动数据**。主流的人体运动扩散模型（如MDM）通常仅在短片段（约70–200帧）上训练，直接生成超长序列会导致动作质量急剧下降。

### 现有方法的局限

当前训练无关（training-free）的长运动生成方法主要分为两类，各自存在明显缺陷：

- **基于补全（inpainting）的方法**：以**DoubleTake (PriorMDM)** 为代表，这类方法先生成各子动作段，再通过扩散模型补全段间的过渡区域。问题在于过渡段独立生成，容易在段边界产生**突变、运动漂移或内容覆盖**，破坏全局连贯性。
- **自回归方法**：如**TEACH**，逐段生成并拼接，但误差会沿序列累积，导致**运动漂移与重复模式**，长序列末端质量严重退化。

此外，**DiffCollage** 等基于扩散模型组合的方法尝试融合多段运动，但在处理过渡区域时仍难以保证局部保真与全局一致性。**MultiDiffusion** 等多扩散方法同样面临边界不协调的挑战。这些问题的根源在于：**缺乏一种机制，能在不依赖长序列训练数据的前提下，同时约束局部动作的真实感和全局运动的连贯性**。

### 核心动机：将分数蒸馏引入长运动生成

本文的核心动机源于一个关键观察：分数蒸馏采样（Score Distillation Sampling, SDS）已在文本到3D生成领域展现出强大的能力——通过预训练扩散模型的分数函数来优化任意参数化生成器，使其输出分布与扩散先验对齐。这一范式天然适合解决长运动生成的困境：

- **无需长序列训练**：仅利用在短片段上预训练的运动扩散模型作为先验。
- **全局可优化**：将整个长序列视为可优化的参数，通过迭代蒸馏使其每个局部片段都符合短运动先验分布。
- **重叠约束实现连贯性**：通过滑动窗口采样重叠短片段，相邻窗口共享部分帧，优化时自然形成一致性约束。

基于此，本文提出**InfiniDreamer**框架，核心创新是**分段分数蒸馏（Segment Score Distillation, SSD）**——一种将SDS范式从静态3D资产生成迁移到时序运动序列优化的方法。该方法先利用预训练模型按文本提示生成各子动作段，并随机初始化过渡段以构建初始长序列；随后通过滑动窗口重叠采样短片段，以对齐损失与几何损失联合迭代优化整个序列，使每个局部片段逼近扩散先验分布的同时，保持全局运动连贯性。

## 核心方法与创新机理

InfiniDreamer 的核心创新在于将**分段分数蒸馏（Segment Score Distillation, SSD）**引入长序列人体运动生成，从根本上改变了长运动合成的范式。与现有方法相比，其关键创新体现在以下四个维度。

### 从“补全/自回归拼接”到“全局迭代优化”

传统训练无关的长运动生成方法依赖两种策略：一是基于扩散模型补全（inpainting）的方法，如 **DoubleTake (PriorMDM)** 和 **DiffCollage**，它们在段边界单独补全过渡段，容易产生突变或覆盖已有动作内容；二是自回归逐段生成再拼接的方法，如 **TEACH**，面临误差累积、运动漂移与重复模式的固有问题。

InfiniDreamer 的核心洞察在于：**无需额外长序列训练，仅通过对重叠短片段进行迭代优化，即可同时实现局部保真与全局一致性**。具体而言，SSD 的运作机制如下：

1. **粗序列初始化**：先用预训练运动扩散模型（MDM）按文本提示生成各子动作段，并用随机噪声初始化过渡段，拼合成初始长序列。
2. **滑动窗口重叠采样**：从初始长序列中以滑动窗口方式采样重叠的短片段（长度 $W$，步长 $P$），确保每个局部区域都被覆盖。
3. **分数蒸馏优化**：对每个采样片段添加噪声后送入冻结的 MDM 预测去噪信号，计算对齐损失与几何损失，反向传播梯度更新**整个长序列**的参数。

这种全局优化范式使得过渡段不再被孤立处理，而是与相邻动作段在统一的 SSD 迭代中协同优化，从根本上解决了边界突变和内容覆盖问题。定量结果验证了这一创新的有效性：在 HumanML3D 上，InfiniDreamer 的 FID 降至 **0.47**（DiffCollage 为 1.07），R-precision 提升至 **0.679**（DiffCollage 为 0.605）；在 BABEL 上，过渡段 FID 从 DoubleTake 的 3.54 大幅降至 **2.07**（Table 1, Table 2）。

### 过渡段优化：梯度掩码与统一迭代

传统补全方法将过渡段作为独立生成目标，容易在边界处产生与相邻动作不连贯的突变。InfiniDreamer 的**changed slot**在于：将过渡段与动作段统一纳入 SSD 迭代优化，并通过**梯度掩码（gradient masks）**分区控制各部分的优化强度。

梯度掩码的设计逻辑是：动作段已由 MDM 生成、质量较高，应施加较弱优化以避免破坏；过渡段初始为随机噪声、质量极低，需要更强的优化信号。消融实验表明，移除梯度掩码后，所有指标均出现下降（Table 1, Table 2, w/o gradient masks），证实了分区控制优化强度对长序列质量至关重要。

### 几何损失：超越简单平滑约束

现有方法通常不使用或仅使用简单的平滑约束来规范运动。InfiniDreamer 引入了三项几何损失，与对齐损失联合优化（Eq. 8）：

- **位置损失 $\mathcal{L}_{pos}$**（Eq. 5）：通过前向运动学（FK）计算关节位置，约束预测运动与原始运动在三维空间中的一致性。
- **脚部接触损失 $\mathcal{L}_{foot}$**（Eq. 6）：利用二进制脚部接触掩码 $f_i$，抑制脚步滑动伪影，增强运动真实感。
- **速度正则化 $\mathcal{L}_{vel}$**（Eq. 7）：保持预测前后帧的速度与原始一致，促进平滑过渡。

消融实验显示，移除几何损失后 BABEL 上的 FID 从 0.97 升至 1.09，过渡 FID 从 2.07 升至 2.15（Table 2, w/o geo losses），表明几何约束对运动真实感和过渡平滑性有实质贡献。

### 自适应文本条件选择

传统方法中，每个动作段固定对应一个文本提示，但过渡段跨越多个子动作时，单一提示无法准确描述其语义。InfiniDreamer 的**changed slot**在于：根据采样片段所在区域自适应选择文本条件（Eq. 3）——若片段完全位于某个子动作内，则使用该子动作的提示；若跨越 $n$ 个子动作，则以均匀概率 $1/n$ 随机采样一个提示。

消融实验验证了这一策略的有效性：使用固定提示（如“transition”或“motion”）或无监督优化均导致性能显著下降（Table 6），因为通用提示无法捕捉多样化过渡段的语义，验证了自适应文本条件选择策略的必要性。

InfiniDreamer 的整体 pipeline 围绕一个核心矛盾展开：长序列人体运动生成需要同时保证**局部动作的语义保真度**与**全局过渡的连贯性**，但预训练的运动扩散模型（MDM）仅见过短片段数据。该方法将这一问题转化为一个**无需额外训练**的迭代优化过程，其工作流可概括为三个阶段：

1. **运动序列初始化（Motion Sequence Initialization）**：根据给定的文本提示列表，利用预训练 MDM 分别生成各子动作段，并在段间插入随机初始化的过渡段，拼合成一条粗糙的长序列。
2. **运动片段采样（Motion Segment Sampling）**：通过滑动窗口在初始长序列上重叠采样短片段，每个短片段作为后续优化的基本单元。
3. **分段分数蒸馏（Segment Score Distillation, SSD）**：对每个采样片段加噪后，由冻结的 MDM 预测去噪信号，计算对齐损失与几何损失，反向传播梯度更新整个长序列的参数。

三个模块形成闭环：初始化提供可微分的初始解，滑动窗口采样决定了每次迭代中哪些局部区域接受优化，SSD 则通过反复将局部片段拉向短运动先验分布来实现全局协调。整个过程不引入额外可训练参数，仅通过梯度下降更新长序列自身。

### 运动序列初始化

给定 $N$ 个文本提示 $\{y_1, y_2, \ldots, y_N\}$，系统首先为每个提示生成对应的子动作段 $m_i$，生成方式直接调用预训练的 **MDM**（Motion Diffusion Model）。随后在相邻子动作段之间插入随机初始化的过渡段 $t_i$，最终拼接成一条完整的初始长序列。这一阶段的输出是粗糙但结构完整的运动序列，为后续 SSD 优化提供了可微分的起点。

### 运动片段采样

从初始长序列中，以滑动窗口的方式采样固定长度 $W$ 的短片段 $x_0^i$，步长为 $P$。窗口长度 $W$ 被设置为与预训练 MDM 的训练片段长度一致，确保每个采样片段都处于模型的舒适区内。重叠采样是关键设计：相邻窗口共享部分帧，使得同一帧会参与多次优化，从而在不同局部上下文中被协调，这是实现全局连贯性的机制基础。

采样片段的**文本条件选择**遵循自适应策略：若 $x_0^i$ 完全落在某个子动作段 $j$ 内，则文本条件 $y$ 确定为 $y_j$；若片段跨越 $n$ 个子动作段（包含过渡区域），则以均匀概率 $1/n$ 随机选择一个文本提示作为条件。这一策略的数学表达为：

$$P(y=y_j) = \begin{cases} 1, & \text{if } x_0^i \subseteq \text{sub-motion } j \\ \frac{1}{n}, & \text{if } x_0^i \text{ spans } n \text{ sub-motions} \end{cases}$$

消融实验（Table 6）证实，使用固定提示（如 "transition" 或 "motion"）或无监督优化均会导致性能显著下降，验证了该自适应策略的有效性。

### 分段分数蒸馏（SSD）

SSD 是 InfiniDreamer 的核心优化机制，借鉴了 Score Distillation Sampling (SDS) 的思想，但将其从图像域迁移到运动域并加以改造。SDS 原本通过最小化渲染图像后验与扩散先验之间的 KL 散度来优化生成器参数，其梯度形式为：

$$\nabla_{\boldsymbol{\theta}} \mathcal{L}_{SDS}(\boldsymbol{\theta};\boldsymbol{x}) = \mathbb{E}_{t} \left[ w(t) (\epsilon_{\boldsymbol{\phi}}(x_t;\boldsymbol{y},t) - \epsilon) \frac{\partial \boldsymbol{x}}{\partial \boldsymbol{\theta}} \right]$$

在 InfiniDreamer 中，优化目标 $\boldsymbol{\theta}$ 直接是长运动序列本身，而非某个生成器网络。对每个采样片段 $x_0^i$，SSD 执行以下步骤：

1. 按扩散过程添加噪声得到 $x_t^i$
2. 冻结的 MDM 预测噪声 $\epsilon_{\phi}(x_t^i; y, t)$
3. 从预测噪声恢复干净运动 $\hat{x}_0^i$
4. 计算**对齐损失**：$\mathcal{L}_{align} = \mathbb{E}_{t,\epsilon} [ w(t) \| \hat{x}_0^i - x_0^i \|_2^2 ]$

对齐损失驱动优化后的片段接近扩散先验分布，但由于仅优化局部片段，需要额外的几何约束来保证物理合理性。因此 SSD 引入了三项几何损失：

- **位置损失** $\mathcal{L}_{pos}$：通过前向运动学（FK）计算关节位置，约束预测运动与原始运动在三维空间中的一致性
- **脚部接触损失** $\mathcal{L}_{foot}$：利用二进制脚部接触掩码 $f_i$ 抑制脚步滑动现象
- **速度正则化损失** $\mathcal{L}_{vel}$：保持预测前后帧的速度与原始一致，促进平滑过渡

SSD 总损失为四项损失的加权和：

$$\mathcal{L}_{ssd} = \mathcal{L}_{align} + \lambda_{pos} \mathcal{L}_{pos} + \lambda_{foot} \mathcal{L}_{foot} + \lambda_{vel} \mathcal{L}_{vel}$$

在 HumanML3D 数据集上几何损失权重设为 0，在 BABEL 上设为 0.1，体现了对不同数据集特性的适配。

### 梯度掩码与分区优化

为精细控制长序列各区域的优化强度，InfiniDreamer 引入了**梯度掩码**（gradient masks）机制。子动作段与过渡段在优化中承担不同角色：子动作段需要保持语义完整性，过渡段则需要大幅调整以实现连贯连接。梯度掩码通过对不同区域施加不同的梯度缩放因子来实现分区控制。消融实验（Table 1, Table 2）表明，移除梯度掩码会导致所有指标下降，验证了这一设计的必要性。

### 关键超参数与敏感性

框架对超参数较为敏感。滑动窗口尺寸 $W$ 的消融（Table 3）显示，$W$ 过小则上下文不足，过大则文本对齐度下降，适中的 $W=120$ 在 HumanML3D 上取得最优过渡 FID。步长 $P \geq W$ 时，部分帧不被任何窗口覆盖，过渡段（初始为随机噪声）几乎不参与优化，导致过渡质量急剧恶化（Transition FID 从 2.04 升至 7.47）。学习率 $\eta$ 的消融（Figure 4）揭示了两种失效模式：过高导致运动僵化（motion stillness），过低则引入过大的噪声扰动导致运动畸变。

InfiniDreamer 通过三个顺序模块实现任意长度人体运动的训练无关生成：运动序列初始化、运动片段采样和分段分数蒸馏（SSD）。整个框架的核心数学机制是将分数蒸馏采样（SDS）从图像域迁移到运动域，并通过精心设计的损失函数在局部保真度与全局一致性之间取得平衡。

### 运动序列初始化模块

给定一组文本提示 $\{y_1, y_2, \ldots, y_K\}$，模块利用预训练的短序列运动扩散模型（MDM）为每个文本描述生成对应的子运动段 $m_i$，并在相邻子运动之间插入随机初始化的过渡段，拼接成初始长序列 $x_0 \in \mathbb{R}^{T \times d}$（$T$ 为总帧数，$d$ 为运动表示维度）。过渡段的随机初始化是后续 SSD 优化的关键起点——这些段落缺乏先验约束，必须通过迭代优化才能获得连贯的运动语义。

### 运动片段采样模块

该模块使用滑动窗口从初始长序列中重叠采样短片段 $x_0^i \in \mathbb{R}^{W \times d}$，窗口尺寸为 $W$，步长为 $P$。每个采样片段可能完全落在一个子运动段内，也可能跨越一个或多个过渡段与子运动的边界。采样策略直接决定了 SSD 优化的覆盖范围：当 $P \geq W$ 时，部分帧将完全不被采样，导致这些帧（尤其是随机初始化的过渡帧）无法获得任何优化信号，从而严重损害过渡质量（见 Table 3）。

### 分段分数蒸馏（SSD）

SSD 是 InfiniDreamer 的核心创新，其数学基础源自 SDS 的梯度更新公式。给定预训练运动扩散模型的去噪网络 $\epsilon_\phi$，SDS 对生成器参数 $\theta$ 的梯度为：

$$\nabla_{\boldsymbol{\theta}} \mathcal{L}_{SDS}(\boldsymbol{\theta}; \boldsymbol{x}) = \mathbb{E}_{t} \left[ w(t) (\epsilon_{\boldsymbol{\phi}}(x_t; \boldsymbol{y}, t) - \epsilon) \frac{\partial \boldsymbol{x}}{\partial \boldsymbol{\theta}} \right] \tag{2}$$

其中 $x_t$ 是加噪后的运动片段，$w(t)$ 是与时间步相关的权重，$\epsilon$ 是注入的高斯噪声。该梯度的本质是驱动生成的运动向扩散先验分布的高密度区域移动，同时忽略 U-Net 雅可比项以降低计算开销。

**文本条件选择策略**：对于跨越 $n$ 个子运动的采样片段 $x_0^i$，其文本条件概率定义为：

$$P(y=y_j) = \begin{cases} 1, & \text{if } x_0^i \subseteq \text{sub-motion } j \\ \frac{1}{n}, & \text{if } x_0^i \text{ spans } n \text{ sub-motions} \end{cases} \tag{3}$$

当片段完全位于某个子运动内时，使用对应的文本提示作为条件；当片段跨越多个子运动时，从涉及的 $n$ 个文本中均匀采样。这一自适应策略避免了固定提示（如 "transition"）无法捕捉多样化过渡语义的问题，消融实验（Table 6）证实无监督优化或使用不匹配的固定提示均会导致性能显著下降。

**对齐损失**：SSD 的核心损失项，度量预测干净运动 $\hat{x}_0^i$ 与原始片段 $x_0^i$ 的加权 L2 距离：

$$\mathcal{L}_{align} = \mathbb{E}_{t,\epsilon} [ w(t) \| \hat{x}_0^i - x_0^i \|_2^2 ] \tag{4}$$

该损失使优化过程在逼近扩散先验的同时保持与初始运动的关联，防止生成结果完全偏离原始语义。

**几何损失族**：为增强运动的物理合理性，SSD 引入三项几何约束：

- **位置损失**：通过前向运动学（FK）计算关节位置，约束预测运动与原始运动的骨骼位置一致性：

$$\mathcal{L}_{pos} = \frac{1}{W} \sum_{i=1}^{W} \| FK(\hat{x}_0^i) - FK(x_0^i) \|_2^2 \tag{5}$$

- **脚部接触损失**：利用二进制脚部接触掩码 $f_i$ 抑制脚步滑动，仅对接触地面的帧施加位置变化约束：

$$\mathcal{L}_{foot} = \frac{1}{W-1} \sum_{i=1}^{W} \| (FK(\hat{x}_0^{i+1}) - FK(\hat{x}_0^i)) \cdot f_i \|_2^2 \tag{6}$$

- **速度正则化损失**：保持预测运动的前后帧速度与原始运动一致，促进过渡段的平滑性：

$$\mathcal{L}_{vel} = \frac{1}{W-1} \sum_{i=1}^{W-1} \| (\hat{x}_0^{i+1} - \hat{x}_0^i) - (x_0^{i+1} - x_0^i) \|_2^2 \tag{7}$$

**SSD 总损失**：四项损失的加权组合构成最终优化目标：

$$\mathcal{L}_{ssd} = \mathcal{L}_{align} + \lambda_{pos} \mathcal{L}_{pos} + \lambda_{foot} \mathcal{L}_{foot} + \lambda_{vel} \mathcal{L}_{vel} \tag{8}$$

几何损失的权重根据数据集特性调节：HumanML3D 上设为 $0$，BABEL 上设为 $0.1$。消融实验（Table 2）表明，移除几何损失在 BABEL 上使 FID 从 $0.97$ 升至 $1.09$，过渡 FID 从 $2.07$ 升至 $2.15$，验证了几何约束对运动真实感的贡献。

**梯度掩码机制**：SSD 在反向传播时对不同区域施加差异化的优化强度——子运动段使用较低的优化强度以保持生成质量，过渡段使用较高的优化强度以促进连贯性。移除梯度掩码（Table 1, Table 2）导致所有指标下降，说明分区控制优化强度是长序列质量的关键设计。

## 实验与关键发现

### 主结果：训练无关长运动生成的全面超越

InfiniDreamer 在两个核心基准 HumanML3D 和 BABEL 上，以训练无关（training‑free）的方式全面超越此前最优方法，尤其体现在运动‑文本对齐质量（R‑precision）与分布真实性（FID）上。

**HumanML3D 数据集（Table 1）**  
InfiniDreamer 取得 R‑precision **0.679 ± 0.007**，较此前最优训练无关方法 DiffCollage 的 0.605 ± 0.006 提升 **+0.074**；FID 降至 **0.47 ± 0.12**，相对 DiffCollage（1.07 ± 0.05）降低 **‑0.60**；MultiModal‑Dist 亦从 3.62 ± 0.01 降至 **3.15 ± 0.01**（‑0.47），表明生成运动不仅更贴近文本语义，而且更接近真实运动分布。Diversity 指标与真值偏差仅 0.05（9.58 vs. 9.63），未出现模式坍塌。

**BABEL 数据集（Table 2）**  
在动作类型更丰富、过渡更复杂的 BABEL 上，InfiniDreamer 同样占据全面优势：R‑precision **0.543 ± 0.009**（DiffCollage 0.487，+0.056），FID **0.97 ± 0.09**（DoubleTake 1.14，‑0.17）。尤为突出的是过渡段质量——Transition FID 从 DoubleTake 的 3.54 ± 0.10 骤降至 **2.07 ± 0.30**（‑1.47），直接验证了分段分数蒸馏（SSD）在消除过渡段突变与覆盖方面的核心能力。

**与微调方法的对比（Table 4, Table 5）**  
即使与需要长序列微调的 FlowMDM 相比，InfiniDreamer 在 BABEL 上的 FID（0.97 vs. 1.25）与 Transition FID（2.07 vs. 2.83）仍显著占优。这揭示了一个关键发现：微调虽可引入长序列先验，但若短片段先验本身受干扰（如 FlowMDM 在短片段上产生运动漂移与语义错误，见 Figure 5），反而可能损害局部动作质量；而 InfiniDreamer 通过冻结预训练短运动先验进行 SSD 优化，在保持局部保真度的同时实现全局连贯，形成因果优势。

![[assets/figures/papers/paper_list_l1889_InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative Comparisons to FlowMDM for Long Motion Generation. We present two examples: in the top row, our framework demonstrates strong contextual understanding, guiding the transition segment to “go upstairs” in response to the following “downstairs” prompt. In contrast, FlowMDM shows slightly motion drift in this segment. In the bottom row, we use a more fine-grained textual prompt, where the FlowMDM exhibits issues with motion drift and semantic errors, failing to generate the “side steps” segment. Our framework, however, produces a higher-quality sequence with enhanced fine-grained comprehension of the text*

### 消融实验：SSD 各组件的因果贡献

消融实验系统验证了 SSD 设计中每个关键组件的必要性，证据链高度一致。

**梯度掩码（gradient masks）**  
移除梯度掩码后，HumanML3D 上所有指标均下降（Table 1 w/o gradient masks），BABEL 上 Transition FID 从 2.07 升至 2.21（Table 2 w/o gradient masks）。梯度掩码的核心作用是分区控制优化强度——对已由预训练 MDM 生成的动作段施加较弱优化，对随机初始化的过渡段施加较强优化。移除后，动作段被过度扰动而丧失原有质量，过渡段则优化不足，直接验证了分区控制对长序列生成的必要性。

![[assets/figures/papers/paper_list_l1889_InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score/figures/003_Table_1.jpg]]
*Table 1: Comparison of InfiniDreamer with the state-of-the-art training-free methods in HumanML3D. Symbols ↑, ↓, and → mean that higher, lower, or closer to the ground truth (GT) value are better, respectively. We run each evaluation 10 times to obtain the final results. We use Bold to indicate the best result, and use underline to indicate the second-best result*

![[assets/figures/papers/paper_list_l1889_InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score/figures/004_Table_2.jpg]]
*Table 2: Comparison of InfiniDreamer with the state-of-the-art training-free methods in BABEL. Symbols ↑, ↓, and → mean that higher, lower, or closer to the ground truth (GT) value are better, respectively. We run each evaluation 10 times to obtain the final results. We use Bold to indicate the best result, and use underline to indicate the second-best result*

**几何损失（geometric losses）**  
在 BABEL 上移除几何损失后，FID 从 0.97 升至 1.09，Transition FID 从 2.07 升至 2.15（Table 2 w/o geo losses）。几何损失由位置损失 $\mathcal{L}_{pos}$、脚部接触损失 $\mathcal{L}_{foot}$ 和速度正则化 $\mathcal{L}_{vel}$ 三项构成，分别约束前向运动学一致性、抑制脚步滑动、保持帧间速度平滑。其贡献虽不如梯度掩码显著，但在运动真实感与过渡平滑性上产生可测量的增益。

**滑动窗口尺寸 W 与步长 P（Table 3）**  
W 过小（30）时，上下文信息不足，过渡段优化缺乏足够约束，Transition FID 较高；W 过大（150）时，单次采样包含过多动作段，文本条件被稀释（Eq. 3 中均匀采样概率降低），导致动作‑文本对齐度下降。HumanML3D 上 W=120 取得最优过渡 FID（2.04），验证了适中上下文长度对过渡生成的关键作用。

步长 P 的影响更为深刻：当 P ≥ W 时，部分帧完全不被任何采样窗口覆盖。对于随机初始化的过渡段，这些未被优化的帧退化为随机噪声，导致 Transition FID 从 2.04（P=30）急剧恶化至 4.70（P=120）乃至 7.47（P=160）。这一现象同时揭示了 SSD 的一个内在权衡——未被采样的动作段因无需添加噪声而保持原有质量，但过渡段的质量完全依赖滑动窗口的覆盖密度。

**文本条件选择策略（Table 6）**  
将自适应文本条件（Eq. 3）替换为固定提示（“transition”或“motion”）或无条件优化后，所有指标均显著下降。固定提示无法捕捉多样化的过渡语义（如“从走到跑”与“从站到坐”的过渡差异巨大），无条件优化则完全失去语义引导。这验证了根据采样片段位置自适应选择文本条件（若跨越多段则均匀采样）是 SSD 语义对齐能力的关键保障。

**学习率 η（Figure 4）**  
定性消融显示，η 过高时运动趋向静止（motion lost），η 过低时噪声扰动过大导致运动畸变。这一敏感性与 SDS 式优化的固有特性一致：学习率直接控制去噪信号对参数的更新幅度，需在“充分优化”与“过优化导致模式坍塌”之间精细平衡。

### 失败模式与局限性

1. **子运动质量受限于基模型**：InfiniDreamer 不改变预训练 MDM 的生成能力，若基模型在特定动作类型上表现不佳（如精细手部交互），长序列中对应段的质量同样受限。这是训练无关方法的固有天花板。
2. **推理效率瓶颈**：生成一段 520 帧的长序列约需 4 分钟，主要开销来自 SSD 迭代优化中对每个采样片段的前向‑反向传播。这限制了实时或交互式应用场景。
3. **超参数敏感性**：学习率 η、窗口尺寸 W、步长 P 的最优值在不同数据集间需重新调节（如 HumanML3D 与 BABEL 上几何损失权重不同），表明方法对超参数选择的鲁棒性有限。
4. **末端质量退化风险**：SSD 在每次迭代中向采样片段添加噪声，虽然梯度掩码保护动作段免受过度扰动，但长序列末端帧被采样的频率可能低于中间帧，存在末端质量累积退化的潜在风险（论文未专门评估末端帧质量，此点需人工验证）。

### 重要图表结论速览

- **Table 1 & Table 2**：InfiniDreamer 在两个数据集上全面超越训练无关方法，Transition FID 优势尤为突出，证明 SSD 解决了过渡段突变的核心瓶颈。
- **Table 3**：W 与 P 的消融揭示了“覆盖密度”对过渡质量的决定性作用——P ≥ W 时过渡段退化为噪声，是方法失效的关键边界条件。
- **Figure 3 & Figure 5**：定性对比显示，DoubleTake 在过渡段出现停顿、漂移与语义丢失，FlowMDM 存在运动漂移与语义错误，而 InfiniDreamer 生成平滑过渡且保持细粒度语义理解。
- **Table 6**：文本条件策略消融直接证明，固定提示无法替代自适应选择，SSD 的语义对齐能力高度依赖 Eq. 3 的设计。
- **Figure 4**：学习率 η 的定性消融揭示了 SDS 式优化的典型失败模式——过高导致静止，过低导致畸变，为实际调参提供了直观参考。

![[assets/figures/papers/paper_list_l1889_InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative Comparisons to Baseline for Long Motion Generation. We present two examples: in the top row, our framework demonstrates strong segment transition capabilities, effectively generating a smooth jogging transition between two jogging motions. In contrast, the baseline produces a transitional segment with noticeable pauses. In the second row, we test a more complex and fine-grained example. The baseline method generates drifting motions, misses the segment “dodges something to their left”, and introduces mismatched motion such as “crisscrossing”. In comparison, our method produces a higher-quality sequence with enhanced fine-grained comprehension*

![[assets/figures/papers/paper_list_l1889_InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score/figures/006_Table_3.jpg]]
*Table 3: Ablation Study on Sliding Window Size W and Stride Size P . Experimental results show that as W increases, the alignment between individual motions and text decreases due to the addition of more contextual information. When*

![[assets/figures/papers/paper_list_l1889_InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score/figures/011_Table_6.jpg]]
*Table 6: Ablation Study on textual prompt. We remove the original text selection strategy and instead optimize using a single text prompt. We present two types of prompt: “transition” and “motion”, as well as an unconditional optimization scenario. We find that mismatched textual conditions lead to a decline in performance, while the unconditional setting produces an sub-optimal result. We believe this is because the text prompts used are not well-suited to capture the semantics of diverse transition segments. This validate the effectiveness of our text condition selection strategy*

## 定位与知识库关联

### 核心定位：训练无关长序列生成的优化范式

InfiniDreamer 处于**训练无关（training‑free）长序列人体运动生成**这一细分方向。与需要额外长序列数据微调的方法（如 FlowMDM）不同，InfiniDreamer 仅依赖一个在短片段上预训练的运动扩散模型（MDM），通过优化而非训练来获得长序列生成能力。这一设计使其在数据稀缺条件下具有天然的适用性，但同时也使生成质量的上限受限于所使用的短序列先验模型。

### 与基线方法的关系图谱

长序列运动生成方法可按其核心策略分为三条主线，InfiniDreamer 在每条线上都提出了根本性的改进：

**1. 基于补全（inpainting）的方法 —— 以 DoubleTake (PriorMDM) 为代表**

DoubleTake 的典型流程是：先生成各子动作段，再在段间空白区域执行扩散补全以生成过渡段。这一策略存在两个结构性缺陷：
- **边界突变**：补全的过渡段与已生成的动作段在边界处缺乏一致性约束，容易产生视觉上的跳变。
- **内容覆盖**：补全过程可能覆盖相邻动作段的尾部或头部帧，破坏已有动作的语义完整性。

InfiniDreamer 的 SSD 从根本上避开了“补全空白”的思路。它将过渡段与动作段统一纳入同一个长序列张量，通过滑动窗口重叠采样使每个局部片段都同时包含动作帧和过渡帧，再以对齐损失和几何损失联合优化整个序列。过渡不再是“事后修补”，而是与动作段在统一的优化过程中协同演化。

**2. 基于扩散模型组合的方法 —— DiffCollage 与 MultiDiffusion**

DiffCollage 通过在不同扩散模型的生成结果之间进行加权融合来拼接长序列。这类方法的本质是在生成过程中做“软缝合”，但不同模型（或同一模型在不同条件下的输出）在重叠区域的统计特性并不一致，缝合处容易产生模糊或伪影。

InfiniDreamer 的 SSD 则是在参数空间而非样本空间进行优化：它将整个长序列视为可优化的参数，通过分数蒸馏让每个局部片段的分布逼近预训练扩散先验。这一过程天然保证了重叠区域的一致性——因为同一帧在多个采样窗口中都会受到优化信号的驱动，最终收敛到一个与所有相关上下文都兼容的状态。

**3. 自回归方法 —— TEACH**

TEACH 采用逐段生成、将上一段的尾部作为下一段的条件输入。这种自回归范式不可避免地面临误差累积问题：前段的微小偏差会通过条件输入逐级放大，最终导致运动漂移和重复模式。

InfiniDreamer 的非自回归设计从根本上规避了误差累积。整个长序列在初始化后即作为整体参与优化，每一帧的更新信号来自其所在的所有重叠采样窗口，信息在全局范围内双向流动，而非单向的因果链条。

**4. 微调方法 —— FlowMDM**

FlowMDM 通过混合位置编码在长序列数据上微调短序列模型，使其能直接生成长序列。这需要额外的长序列训练数据，且在短片段上的生成质量可能因微调而受损（Table 4、Table 5 显示 FlowMDM 在部分指标上出现干扰）。

InfiniDreamer 保持预训练模型完全冻结，不引入任何额外训练，因此不会损害短序列先验的质量。这是其“训练无关”定位的核心优势，但也意味着它无法通过训练来弥补先验模型本身的缺陷。

### 方法适用边界

**适用场景：**
- 缺乏高质量长序列训练数据的领域
- 需要根据文本描述列表生成语义连贯的长运动序列
- 对过渡段平滑性和全局一致性要求高于对绝对生成速度的要求

**不适用或需谨慎使用的场景：**
- **实时或交互式应用**：生成一段 520 帧的长序列约需 4 分钟，推理效率是当前瓶颈
- **对子动作本身质量有极致要求的场景**：SSD 优化过程中的加噪‑去噪操作会对已有动作段引入轻微的质量退化（Table 3 中 P≥W 时动作段指标反而提升，印证了这一点）
- **需要精确物理模拟的场景**：几何损失（位置、脚部接触、速度正则化）提供的是软约束，不能保证物理上的严格正确性

### 已知局限与开放问题

**局限：**
1. **先验依赖**：子运动的生成质量受限于所使用的短序列生成模型（MDM）的性能上限，InfiniDreamer 无法超越其先验的生成能力。
2. **推理速度**：生成一段 520 帧的长序列约需 4 分钟，主要瓶颈在于每轮 SSD 优化需要多次调用扩散模型进行去噪预测。
3. **超参数敏感**：学习率 η、滑动窗口尺寸 W、步长 P 等超参数对最终质量影响显著，且在不同数据集上需要独立调节。η 过高导致运动僵化（motion stillness），η 过低导致噪声扰动和运动畸变（Figure 4）；W 过小缺乏上下文导致过渡质量下降，W 过大则稀释了文本对齐度（Table 3）。

**开放问题：**
1. **推理效率提升**：能否通过减少 SSD 优化轮次、使用更高效的采样策略或蒸馏轻量化扩散模型来缩短生成时间，使其适用于交互式应用？
2. **先验模型升级**：若使用更强的短序列生成模型（如基于 flow matching 或 consistency model 的运动生成器）作为先验，InfiniDreamer 的整体长序列质量能否线性提升？
3. **末端质量衰减**：SSD 优化过程中的加噪操作是否会在长序列的末端累积噪声效应，导致尾部动作质量下降？现有消融实验未专门分析这一现象。
4. **微调与优化的混合策略**：FlowMDM 等微调方法在短片段上产生的干扰能否通过与 SSD 优化结合来缓解？即先用微调模型生成粗序列，再用 SSD 精炼，是否能兼得微调的长序列先验和优化的局部保真优势？

## 原文 PDF

![[paperPDFs/ICCV_2025/InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score_Distillation.pdf]]

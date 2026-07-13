---
title: Towards Synthesized and Editable Motion In-Betweening Through Part-Wise Phase Representation
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Towards_Synthesized_and_Editable_Motion_In_Betweening_Through_Part_Wise_Phase_Representation.pdf
project_link: null
code_link: null
aliases:
- PWPRFBPABMS
- TSEMBTPWPR
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 利用分部位周期性自编码器提取局部相位（幅度与角进度），结合身体部位混合专家（BPMoE）和运动采样器，解耦运动源与合成控制，实现对不同肢体的精细风格调节。
primary_logic: 通过每个身体部位的正弦相位参数化（幅度控制运动大小，角进度调控节拍），捕获局部风格特征，并允许缩放幅度/频率独立编辑个别肢体运动，在保持整体协调的前提下实现风格化中间帧生成。
claims:
- 在100STYLE数据集上，OURS(2)和OURS(5)在NPSS、L2全局位置误差和脚滑指标上均优于CVAE、RSMT和PhaseMIB，尤其在长序列（120-160帧）上。
- 消融研究表明，基于身体部位相位的风格编码器效果明显优于基于全身运动序列的CNN编码器，验证了分部位相位表示的必要性。
- 通过调整相位的幅度和频率，可以独立控制特定肢体的运动幅度和速度，且未选择的身体部位仅发生微小协调变化。
- 在更换身体部位风格的场景中，OURS方法能保持肢体协调，脚滑误差低于直接拼接的方式。
---

# Towards Synthesized and Editable Motion In-Betweening Through Part-Wise Phase Representation

> [!tip] 核心洞察
> 通过每个身体部位的正弦相位参数化（幅度控制运动大小，角进度调控节拍），捕获局部风格特征，并允许缩放幅度/频率独立编辑个别肢体运动，在保持整体协调的前提下实现风格化中间帧生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于分部位相位表示的运动中间帧合成与编辑 |
| 英文题名 | Towards Synthesized and Editable Motion In-Betweening Through Part-Wise Phase Representation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2503.08180) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Part-Wise Phase Representation Framework (BP Phase Autoencoder + BPMoE + Motion Sampler) |
| Dataset | 100STYLE |

> [!tip] 效果简介
> - 100STYLE 上，NPSS (↓) OURS(2) achieves lowest NPSS among methods vs CVAE, RSMT, PhaseMIB achieve higher NPSS (Performance improvement observed across 120, 140, 160 frames)；L2 global position (↓) OURS(2) achieves lowest L2 error among methods vs CVAE, RSMT, PhaseMIB achieve higher L2 error (Lower reconstruction error across all frame lengths)；Skating (↓) OURS(5) achieves the lowest skating artifacts vs CVAE, RSMT, PhaseMIB show higher skating (Smallest foot skating across all frame lengths)。
> - 100STYLE (style change) 上，NPSS, L2, Skating (↓) OURS(2) consistently outperforms baselines under body part style changes vs CVAE, RSMT, PhaseMIB and direct stitching (Noticeable improvement in reconstruction and skating)。

## 概要

运动中间帧生成（motion in-betweening）旨在根据给定的起始与目标姿态，自动补全中间过渡帧，是计算机动画中的核心任务。现有方法通常对全身运动进行整体建模以编码运动风格，但忽略了身体各部位在运动幅度、节奏与协调模式上的独立性。这一瓶颈导致生成的补全运动缺乏灵活性：用户无法独立调整特定肢体的运动风格，也无法在保持整体协调的前提下实现精细的肢体级可控编辑。

针对上述问题，本文提出一种**基于分部位相位表示（Part-Wise Phase Representation）的运动中间帧合成与编辑框架**。其核心思路是：利用周期性自编码器为每个身体部位提取局部相位——以**幅度（amplitude）**控制运动大小、以**角进度（angular progression）**调控运动节拍——从而在解耦运动源与合成控制的同时，捕获各肢体的局部风格特征。在此基础上，框架引入**身体部位混合专家网络（Body Part Mixture of Experts, BPMoE）**和**运动采样器（Motion Sampler）**，实现对不同肢体的精细风格调节，并支持通过缩放相位幅度与频率来独立编辑特定身体部位的运动。

在100STYLE数据集上的实验表明，所提方法在长序列（120–160帧）的重建精度（NPSS、L2全局位置误差）和脚滑指标上均优于**CVAE**（Tang et al., TOG 2022）、**RSMT**（Tang et al., SIGGRAPH 2023）和**PhaseMIB**（Starke et al., PACMCGIT 2023）等基线方法。消融研究进一步验证了分部位相位表示相对于全身运动序列编码的显著优势。此外，该方法在更换身体部位风格的场景下仍能保持肢体协调，脚滑误差低于直接拼接方式，展现出良好的风格解耦与编辑能力。



### 问题背景

角色动画中的运动中间帧生成是计算机图形学的核心任务之一：给定起始姿态和目标姿态，自动补全中间过渡帧，使动画平滑自然。随着交互式应用（如游戏、虚拟现实）对动画质量要求的提升，单纯的运动平滑已无法满足需求——生成的运动还需体现特定的**风格特征**（如“疲惫的行走”“欢快的奔跑”），并且风格应在不同身体部位上具有差异化的表现力。

现有方法在处理风格化运动中间帧生成时，通常将人体视为一个整体进行建模。它们从全身运动序列中提取统一的潜在表示，用以编码运动风格，再据此生成过渡帧。这一范式存在一个根本性的瓶颈：**全身统一的表示无法捕捉不同身体部位独立的运动模式**。例如，一个“愤怒地行走”的角色可能上半身摆动幅度很大，但下肢步态相对克制；而“偷偷摸摸地走”则可能上半身几乎不动，下肢却以极小的步幅快速移动。当风格编码被压缩为单一向量时，这些部位间的差异被抹平，导致生成的运动缺乏灵活性，无法独立调整特定肢体的风格表现。

### 现有方法的缺口

当前主流的风格化运动中间帧方法可归为两类：一类基于卷积变分自编码器（如 **CVAE**, Tang et al., TOG 2022），另一类基于相位流形（如 **PhaseMIB**, Starke et al., PACMCGIT 2023）。前者通过变分推断学习运动过渡的分布，后者利用相位变量来同步运动节奏。尽管这些方法在短序列过渡上取得了不错的效果，但它们共享一个结构性缺陷：**运动风格的控制粒度停留在全身层面，而非肢体层面**。

具体而言，现有方法的风格编码器通常对全身运动序列进行 CNN 编码，得到固定维度的风格向量。这种设计导致两个直接后果：

1. **无法独立编辑**：用户无法单独调整某条手臂的摆动幅度或某条腿的步频，任何风格修改都会不可避免地影响全身所有关节。
2. **长序列退化**：在 120–160 帧的长过渡中，全身统一表示难以维持各部位风格的一致性，容易产生脚滑、抖动等伪影。

### 本文动机与核心思路

本文的核心动机在于**解耦运动源与合成控制**，使每个身体部位拥有独立的风格表示。直觉上，人体运动可被分解为多个局部周期过程的叠加——行走时双腿以固定频率交替，手臂以相关但可变的幅度摆动，躯干则提供稳定支撑。如果能从运动数据中自动提取每个部位的**局部相位信息**（幅度控制运动大小，角进度调控节拍），就能为每个肢体建立独立的风格参数化。

基于这一洞察，本文提出**分部位相位表示框架**。其核心创新在于：

- **分部位相位自编码器**：利用周期性自编码器，按预定义的身体部位（如四肢+躯干共 5 部分，或上肢+其他共 2 部分）分别提取正弦相位参数 $\Theta_i^{2j-1} = A_i^j \cdot \sin(2\pi \cdot S_i^j), \Theta_i^{2j} = A_i^j \cdot \cos(2\pi \cdot S_i^j)$，其中幅度 $A$ 控制运动范围，角进度 $S$ 控制时序节奏。
- **身体部位混合专家**：替代单一生成网络，通过多个专家子网络分别处理不同部位的运动预测，并由门控机制动态融合。
- **分部位风格编码器与运动采样器**：将各部位相位编码为紧凑的风格表示，结合 LSTM 时序模型预测控制信号和中间相位，实现从起始到目标的风格化过渡。

这一设计使得用户可以**独立缩放特定身体部位的相位幅度或频率**，从而在不破坏整体协调性的前提下，精细调控个别肢体的运动幅度和速度。这为风格化动画编辑提供了一种直观且强大的控制手段。



## 核心方法与创新机理

本文的核心创新在于将运动中间帧生成从**全身统一建模**转向**分部位相位解耦**，从而实现对不同肢体的独立风格控制。这一转变通过三个相互关联的机制实现，形成了一条从表示层到生成层再到控制层的完整创新链条。

### 关键创新点一：分部位相位参数化

现有方法（如 PhaseMIB）通常从全身运动中提取单一的整体相位，这导致不同肢体的运动风格被耦合在一起，无法独立调控。本文的核心洞察是：**每个身体部位具有各自的内在周期性，应当被独立建模**。

具体而言，对于第 $i$ 个身体部位，其相位向量通过正弦参数化表示：

$$\Theta_{i}^{2j-1} = A_{i}^{j} \cdot \sin(2\pi \cdot S_{i}^{j}), \quad \Theta_{i}^{2j} = A_{i}^{j} \cdot \cos(2\pi \cdot S_{i}^{j})$$

其中 $A_{i}^{j}$ 控制该部位的运动幅度，$S_{i}^{j}$ 控制其角进度（即运动节拍）。这种参数化将运动的“大小”与“快慢”显式分离，为后续的独立编辑提供了数学基础。身体部位划分采用两种方案：五部位（四肢加躯干）和两部位（上肢与其他部分），分别对应精细控制和整体协调的需求。

### 关键创新点二：身体部位混合专家网络（BPMoE）

传统方法使用单一网络同时处理所有关节的运动生成，难以捕捉不同部位的运动差异性。本文提出 BPMoE，其帧预测公式为：

$$X_{S}^{t+1} = X_{S}^{t} + BPMoE(z^{t+1}, X_{S}^{t}, X_{\mathcal{P}}^{t})$$

该网络接收当前姿态 $X_{S}^{t}$、控制信号 $z^{t+1}$ 和分部位相位 $X_{\mathcal{P}}^{t}$，通过多个专家子网络的动态融合来预测姿态增量。这种设计使网络能够针对不同身体部位激活不同的专家组合，从而在保持整体协调的同时，实现对局部运动的精细建模。

### 关键创新点三：基于分部位相位的风格编码与控制

现有方法的风格编码器通常对全身运动序列进行 CNN 编码，无法区分不同肢体的风格特征。本文提出**基于身体部位相位的风格编码器**，对各部位的相位分别编码，获得分部位风格表示。消融实验（Table 3）表明，这种设计在重建精度和脚滑指标上均显著优于基于全身运动序列的 CNN 编码器，验证了分部位相位表示的必要性。

在可控性方面，用户可以通过缩放特定部位的相位幅度 $A$ 来独立调整其运动幅度，或通过调整频率来控制其运动速度。实验表明（Figure 4、Figure 5），这种操作仅对目标部位产生显著影响，未选择的部位仅发生微小的协调性变化，实现了真正意义上的**分部位风格编辑**。

### 与基线方法的本质差异

| 设计维度 | 基线方法（PhaseMIB 等） | 本文方法 |
|---------|----------------------|---------|
| 相位表示 | 全身单一整体相位 | 分部位局部相位（5部分或2部分） |
| 风格编码 | 全身运动序列 CNN 编码 | 分部位相位 CNN 编码 |
| 生成网络 | 单一网络处理所有关节 | BPMoE 动态融合多个专家子网络 |
| 可控性 | 无法独立调整特定部位 | 缩放幅度/频率独立控制各部位 |

这些创新共同构成了一个完整的**分部位相位表示框架**，使运动中间帧生成从“整体风格迁移”迈向“局部风格解耦与编辑”，为动画制作中的精细运动控制提供了新的技术路径。



该框架采用两阶段训练策略，将运动中间帧生成任务分解为三个核心模块的协同工作：**BP Phase Autoencoder（身体部位相位自编码器）**、**BPMoE（身体部位混合专家）** 和 **Motion Sampler（运动采样器）**。整体流程如图2所示。

### 第一阶段：相位提取与运动动力学建模

第一阶段的目标是建立身体部位相位空间，并训练一个能够根据控制信号预测运动增量的生成器。

**BP Phase Autoencoder** 首先从运动序列中为每个预定义的身体部位提取局部相位表示。该模块基于周期性自编码器[31]，将每个身体部位 $i$ 的相位参数化为正弦形式：

$$
\Theta_{i}^{2j-1} = A_{i}^{j} \cdot \sin(2\pi \cdot S_{i}^{j}), \quad \Theta_{i}^{2j} = A_{i}^{j} \cdot \cos(2\pi \cdot S_{i}^{j})
$$

其中幅度 $A$ 控制运动大小，角进度 $S$ 调控运动节拍。身体部位划分采用两种方案：五部位（四肢加躯干）和两部位（上肢与其他部分），具体关节分组见Figure 3。

**BPMoE** 随后利用当前姿态 $X_{S}^{t}$、当前身体部位相位 $X_{\mathcal{P}}^{t}$ 和编码器生成的控制信号 $z^{t+1}$，预测下一帧的姿态增量：

$$
X_{S}^{t+1} = X_{S}^{t} + BPMoE(z^{t+1}, X_{S}^{t}, X_{\mathcal{P}}^{t})
$$

该模块的训练损失为：

$$
\mathcal{L}_{\mathrm{BPMoE}} = L_{\mathrm{rec}} + \beta L_{\mathrm{kl}} + L_{\mathrm{foot}}
$$

包含重建损失、KL散度正则项和脚滑约束。

### 第二阶段：运动采样器训练

第二阶段固定已训练的BPMoE，移除编码器，转而训练**Motion Sampler**来替代编码器生成控制信号和下一帧相位。

**Style Encoder** 将各身体部位的相位编码为紧凑的风格表示，捕捉分部位的风格信息。**LSTM网络**接收当前帧、目标帧和风格表示作为输入，输出解码为控制信号和下一帧的身体部位相位，同时结合当前相位和风格信息。

运动采样器的总损失为：

$$
\mathcal{L}_{\mathrm{Sampler}} = L_{\mathrm{rec}} + L_{\mathrm{last}} + \lambda_{\mathrm{foot}} L_{\mathrm{foot}} + \lambda_{\mathrm{phase}} L_{\mathrm{phase}}
$$

其中 $L_{\mathrm{phase}}$ 确保幅度、频率和相位预测的准确性：

$$
\|A - \hat{A}\|_{2}^{2} + \|F - \hat{F}\|_{2}^{2} + \frac{1}{2}(\|p - \hat{p}\|_{2}^{2} + \|p - \tilde{p}\|_{2}^{2})
$$

### 核心设计理念

该框架的核心创新在于**解耦了运动源与合成控制**：通过分部位相位表示，每个肢体的运动风格（幅度、频率）被独立编码，使得生成网络能够对不同身体部位进行精细调节。BPMoE通过动态融合多个专家子网络，替代了传统的单一网络处理所有关节的方式，增强了模型对不同运动模式的适应能力。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/002_Figure_2.jpg]]
*Figure 2: System Overview. We first train the BP Phase Autoencoder (Body Part Phase Autoencoder) similar to [31]. Next, we train the BPMoE (Body Part Mixture of Experts). The encoder takes the current state and the next state to generate the control signal. BPMoE takes the control signal, the current state, and the next BP Phase to predict the next state. Finally, when training the Motion Sampler, we remove the encoder, fix BPMoE and connect the Motion Sampler to BPMoE. The style encoder encodes the BP Phase into style information. The LSTM network takes the current, target state, and style information as input, and the output is decoded into control signals and the next BP Phase, along with the curr...*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/001_Figure_1.jpg]]
*Figure 1: We demonstrate the effectiveness of our framework in generating stylized online motion in-between. It excels at producing realistic animations that accurately reflect the target style during variations in body part movements, while also allowing adjustments to the individual body parts or overall movements. These capabilities make our framework a robust and versatile solution for stylized in-between generation through part-aware phase representation*



### 3.1 分部位相位自编码器（BP Phase Autoencoder）

该方法的核心创新在于将运动解耦到**身体部位**层面进行相位参数化，而非对全身运动提取单一相位。对于第 $i$ 个身体部位，其相位向量由正弦函数参数化：

$$
\Theta_{i}^{2j-1} = A_{i}^{j} \cdot \sin(2\pi \cdot S_{i}^{j}), \quad \Theta_{i}^{2j} = A_{i}^{j} \cdot \cos(2\pi \cdot S_{i}^{j})
$$

其中 $A_{i}^{j}$ 为**幅度**（amplitude），控制该部位运动的**大小**；$S_{i}^{j}$ 为**角进度**（angular progression），调控运动的**节拍与时序**；$j$ 为相位通道索引。该参数化使得每个肢体的局部风格特征——运动幅度与频率——被显式编码为可独立操控的变量。

身体部位划分采用两种方案（Figure 3）：**五部位划分**（左/右上肢、左/右下肢、躯干）和**两部位划分**（上肢与其他部分）。周期性自编码器从运动序列中自动提取各部位的 $A$ 与 $S$，无需手工标注。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/003_Figure_3.jpg]]
*Figure 3: The five body parts of the first method consist of the left upper limb (joints 15 to 18), right upper limb (joints 19 to 22), left lower limb (joints 1 to 4), right lower limb (joints 5 to 8), and the torso (joints 9 to 12). The second method requires the selection of two body parts: the upper limbs (joints 15 to 22) and the other segments (joints 0 to 14)*

### 3.2 身体部位混合专家网络（BPMoE）

BPMoE 负责根据控制信号与当前状态预测下一帧的姿态增量，其核心预测公式为：

$$
X_{S}^{t+1} = X_{S}^{t} + \text{BPMoE}(z^{t+1}, X_{S}^{t}, X_{\mathcal{P}}^{t})
$$

其中 $X_{S}^{t}$ 为当前帧的姿态状态，$z^{t+1}$ 为控制信号（由后续的运动采样器生成），$X_{\mathcal{P}}^{t}$ 为当前帧各身体部位的相位信息。BPMoE 采用混合专家架构，多个专家子网络分别对不同身体部位的运动模式进行建模，并通过动态门控机制融合输出，从而实现对不同肢体运动特征的解耦建模。

BPMoE 的第一阶段训练目标为：

$$
\mathcal{L}_{\mathrm{BPMoE}} = L_{\mathrm{rec}} + \beta L_{\mathrm{kl}} + L_{\mathrm{foot}}
$$

其中 $L_{\mathrm{rec}}$ 为重建损失，$L_{\mathrm{kl}}$ 为 KL 散度正则项（约束控制信号的潜在空间分布），$L_{\mathrm{foot}}$ 为脚滑约束。

### 3.3 运动采样器与风格编码器

运动采样器（Motion Sampler）在 BPMoE 固定后训练，负责生成控制信号 $z^{t+1}$ 并预测下一帧的相位。其输入包括当前帧状态、目标帧状态、当前相位以及由风格编码器提取的风格表示。风格编码器对各身体部位的相位序列进行 CNN 编码，获得紧凑的分部位风格信息。

采样器的相位动力学损失确保幅度、频率与相位预测的准确性：

$$
\|A - \hat{A}\|_{2}^{2} + \|F - \hat{F}\|_{2}^{2} + \frac{1}{2}\left(\|p - \hat{p}\|_{2}^{2} + \|p - \tilde{p}\|_{2}^{2}\right)
$$

其中 $A$、$F$、$p$ 分别为真实幅度、频率与相位，$\hat{A}$、$\hat{F}$、$\hat{p}$ 为预测值，$\tilde{p}$ 为通过相位动力学模型推算的相位。

运动采样器的总损失函数为：

$$
\mathcal{L}_{\mathrm{Sampler}} = L_{\mathrm{rec}} + L_{\mathrm{last}} + \lambda_{\mathrm{foot}} L_{\mathrm{foot}} + \lambda_{\mathrm{phase}} L_{\mathrm{phase}}
$$

其中 $L_{\mathrm{last}}$ 约束生成序列末帧与目标帧的对齐，$L_{\mathrm{phase}}$ 为上述相位动力学损失，$\lambda_{\mathrm{foot}}$ 与 $\lambda_{\mathrm{phase}}$ 为平衡权重。

### 3.4 关键设计决策

整个框架采用**两阶段训练**策略：先训练 BP Phase Autoencoder 与 BPMoE，再固定 BPMoE 训练运动采样器。分部位相位表示使得风格编码器能够捕获各肢体的独立风格特征——消融实验（Table 3）证实，基于身体部位相位的风格编码器在重建精度与脚滑指标上均显著优于基于全身运动序列的 CNN 编码器，验证了分部位表示的必要性。



## 实验与关键发现

### 4.1 实验设置

实验在 **100STYLE** 数据集上进行，该数据集包含多种运动风格类别。评估采用 23 关节人体骨架，身体部位划分采用两种方案：**五部位**（左/右上肢、左/右下肢、躯干）和**两部位**（上肢与其他部分），分别对应 **OURS(5)** 和 **OURS(2)** 两种变体。评估指标包括：

- **NPSS**（Normalized Power Spectrum Similarity，↓）：衡量重建运动与真值在频域的相似度。
- **L2 全局位置误差**（↓）：衡量全局位置重建精度。
- **Skating**（脚滑，↓）：基于脚部速度与高度阈值的脚滑伪影度量，定义为 $L_f = v_f \cdot \mathrm{clamp}(2 - 2^{\bar{h} / H}, 0, 2)$，其中 $H=2.5$。

基线方法包括 **CVAE**（Tang et al., TOG 2022）、**RSMT**（Tang et al., SIGGRAPH 2023）和 **PhaseMIB**（Starke et al., PACMCGIT 2023），分别代表基于卷积变分自编码器、实时风格化过渡和相位流形的运动中间帧生成方案。

### 4.2 主实验结果

**Table 1** 展示了各方法在 120、140、160 帧长度下的重建精度和脚滑指标对比。核心发现如下：

- **OURS(2) 在 NPSS 和 L2 全局位置误差上全面领先**：在 120/140/160 帧上，OURS(2) 的 NPSS 分别为 6.780、9.443、12.178，L2 误差分别为 25.300、30.052、35.185，均低于 CVAE、RSMT 和 PhaseMIB。这表明分部位相位表示在长序列生成中具有显著优势，能够更好地保持运动的时间结构。
- **OURS(5) 在脚滑指标上表现最优**：在所有帧长度下，OURS(5) 的 skating 指标（0.094/0.083/0.074）均为最低，说明更细粒度的五部位划分有助于降低脚部滑动伪影。
- **两部位 vs. 五部位存在精度-脚滑权衡**：OURS(2) 的 NPSS 优于 OURS(5)，但脚滑略高。论文分析认为，两部位划分能更好地捕捉上下肢的协同效应，从而获得更优的整体频域表示；而五部位划分更精细地建模了各肢体的内在周期性，因此脚滑更低。

**Table 2** 进一步考察了更换身体部位风格场景下的性能。在该场景中，OURS(2) 和 OURS(5) 在 NPSS、L2 误差和脚滑指标上均持续优于所有基线方法，且显著优于直接拼接（direct stitching）的方式。这验证了分部位相位表示在风格迁移中保持肢体协调性的能力。

### 4.3 消融实验

**Table 3** 对比了基于身体部位相位的风格编码器（本文方法）与基于全身运动序列的 CNN 编码器的性能差异。结果表明：

- 基于身体部位相位的编码器在 NPSS、L2 全局位置和脚滑指标上**全面优于**基于全身运动序列的编码器。
- 这直接验证了核心设计动机：全身运动序列编码难以解耦各肢体的独立风格信息，而分部位相位表示能够捕获局部运动特征，从而在重建精度和物理合理性上均获得提升。

### 4.4 可控性分析

本文方法的核心优势在于支持对特定身体部位的运动进行独立编辑。通过缩放相位的**幅度**和**频率**参数，可以实现以下控制：

- **幅度调整**（**Figure 4**）：增大某部位的相位幅度可使该部位的运动幅度增大，而未选中的身体部位仅发生微小的协调性变化，整体运动保持自然。
- **频率调整**（**Figure 5**）：调整某部位的相位频率可改变该部位的运动速度/节拍，同样不会破坏其他肢体的运动模式。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/007_Figure_4.jpg]]
*Figure 4: Results of adjusting the amplitude of body part phases*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/008_Figure_5.jpg]]
*Figure 5: Results of adjusting the frequency of body part phases*

这种可控性源于分部位相位参数化的设计：$\Theta_i^{2j-1} = A_i^j \cdot \sin(2\pi \cdot S_i^j)$，$\Theta_i^{2j} = A_i^j \cdot \cos(2\pi \cdot S_i^j)$，其中幅度 $A$ 控制运动大小，角进度 $S$ 调控时序节拍。用户通过缩放 $A$ 或 $S$ 即可直观地编辑特定肢体的运动风格。

### 4.5 局限性

尽管方法在 100STYLE 数据集上表现优异，仍存在以下局限：

1. **身体部位划分依赖预定义**：当前方案采用固定的五部位或两部位划分，对于非标准骨架或特殊动作类型可能需要重新设计划分策略。
2. **泛化性未验证**：实验仅在 23 关节骨架的 100STYLE 数据集上进行，对其他风格类别、动作类型和骨架拓扑的泛化能力尚待评估。
3. **非周期性运动适应性存疑**：相位提取基于周期性自编码器，对高度复杂或非周期性运动（如杂技、手语）的适应性可能不足。

### 4.6 待解决问题

1. 如何自适应地学习最优身体部位划分，以适应不同运动类型和骨架结构？
2. 方法在多角色交互或与物理环境（地形、物体）交互场景下的表现如何？
3. 能否将分部位相位表示扩展到手部和面部动作生成，实现全身一致的风格化控制？
4. 相位幅度和频率的调整是否可交由用户实时交互控制，以用于实际动画制作管线？

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/004_Table_1.jpg]]
*Table 1: Comparison on reconstruction and foot skating metrics of different methods*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/005_Table_2.jpg]]
*Table 2: Comparison of reconstruction and foot skating metrics for different methods with changes in body part styles*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2503_08180/figures/006_Table_3.jpg]]
*Table 3: Comparisons of reconstruction and foot skating between motion-based and body-part-phase-based representation*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

运动中间帧生成（Motion In-Betweening）是角色动画中的经典任务，目标是在给定的起始帧与目标帧之间填充缺失的姿态序列。传统方法通常借助全身运动建模来编码运动风格，但这导致一个关键瓶颈：**全身统一的隐空间表示无法解耦不同肢体的独立运动特征，使得补全结果缺乏灵活性，难以独立调整特定肢体的运动风格或幅度**。例如，当需要仅改变手臂摆动幅度而保持腿部运动不变时，全身建模方法往往会产生不自然的耦合变化。

本文的核心洞察在于：人体的各部位（四肢、躯干）具有相对独立的周期性运动模式，应当被分别参数化。通过为每个身体部位引入正弦相位参数化——其中**幅度（Amplitude）控制运动大小，角进度（Angular Progression）调控节拍**——可以捕获局部风格特征，并允许通过缩放幅度或频率来独立编辑个别肢体的运动，在保持整体协调的前提下实现风格化中间帧生成。

### 2. 与现有方法的关系网络

#### 2.1 直接对比的基线方法

本文在 100STYLE 数据集上与三类代表性方法进行了系统对比：

- **CVAE**（Tang et al., TOG 2022）：基于卷积变分自编码器的运动过渡生成方法，采用全身运动序列编码风格信息，缺乏分部位的解耦能力。
- **RSMT**（Tang et al., SIGGRAPH 2023）：实时风格化运动过渡生成方法，同样基于全身表示，无法独立控制各肢体。
- **PhaseMIB**（Starke et al., PACMCGIT 2023）：基于相位流形的运动中间帧生成方法，从全身运动提取单一整体相位，未区分不同身体部位的局部周期特性。

从方法谱系上看，本文与 PhaseMIB 共享“相位驱动”的技术路线，但做出了关键升级：**将单一全局相位替换为分部位局部相位**。这一改动带来了两个层面的优势。在表示层面，分部位相位能更精细地捕获各肢体的内在周期性，使风格编码器获得更丰富的局部信息（消融实验 Table 3 验证了分部位相位编码器显著优于基于全身运动序列的 CNN 编码器）。在控制层面，用户可以通过缩放特定部位的相位幅度或频率，独立调整该部位的运动幅度或速度，而未选择的身体部位仅发生微小的协调变化（Figure 4、Figure 5）。

#### 2.2 技术路线的承袭与创新

本文框架在以下技术点上承袭了现有工作并做出改进：

- **周期性自编码器**：借鉴了周期性自编码器（periodic autoencoders ）的相位提取机制，但将其从全身运动扩展到分部位运动，使每个身体部位独立拥有幅度与角进度参数。
- **混合专家网络（MoE）**：将混合专家架构引入运动生成领域，提出**身体部位混合专家（BPMoE）**，动态融合多个专家子网络来预测下一帧的姿态增量，替代了传统方法中单一网络同时处理所有关节的做法。
- **两阶段训练策略**：第一阶段训练 BP Phase Autoencoder 和 BPMoE，第二阶段固定 BPMoE 训练 Motion Sampler，这种分阶段训练范式在运动生成领域已有先例，但本文将其适配到分部位相位表示框架中。

#### 2.3 方法谱系中的定位

从知识库定位的角度，本文处于以下研究脉络的交汇点：

| 研究脉络 | 本文贡献 |
|---------|---------|
| 运动中间帧生成 | 将相位驱动方法从全局扩展到分部位，提升长序列（120–160帧）生成质量 |
| 周期性运动表示 | 首次将分部位正弦相位参数化引入风格化运动生成 |
| 运动风格编辑 | 提供幅度/频率缩放接口，实现肢体级精细风格控制 |
| 混合专家网络 | 将 MoE 架构应用于姿态增量预测，实现身体部位间的动态融合 |

### 3. 适用边界与局限

尽管本文方法在 100STYLE 数据集上取得了显著提升，但仍存在以下适用边界和局限：

1. **骨架与动作类型的泛化性**：实验仅在 100STYLE 数据集上进行，使用 23 关节骨架。对于非标准骨架（如四足动物、多足生物）或特殊动作类型（如杂技、手语、舞蹈中的非周期性动作），方法可能需要重新设计身体部位划分策略，且相位提取的有效性尚待验证。

2. **身体部位划分的预定义性**：当前方法依赖人工预定义的身体部位划分（5 部分或 2 部分）。5 部分划分（四肢加躯干）能更好地降低脚滑误差，但 NPSS 略高于 2 部分划分（上肢与其他部分），表明不同划分策略存在精度-物理合理性之间的 trade-off。如何自适应地学习最优划分仍是一个开放问题。

3. **非周期性运动的适应性**：相位提取基于周期性自编码器，对高度非周期性或复杂运动（如突然的转向、跌倒、交互动作）的适应性可能不足。当运动缺乏明确的周期性时，幅度与角进度的物理意义可能弱化。

4. **多角色与物理交互**：当前框架仅针对单角色运动生成，未涉及多角色交互或与物理环境（地形、物体）的交互场景。在这些场景中，身体部位的运动不仅受风格约束，还受外部物理约束，分部位相位的独立性假设可能需要修正。

### 4. 开放问题

基于本文的贡献与局限，以下开放问题值得后续研究关注：

1. **自适应身体部位划分**：能否根据运动类型和骨架结构自动学习最优的身体部位划分策略？例如，对于游泳动作，可能需要将上肢进一步细分；对于踢腿动作，下肢的划分粒度可能需要调整。

2. **手部与面部扩展**：当前方法仅处理身体躯干和四肢，能否将分部位相位表示扩展到手部和面部动作生成，实现全身一致的风格化控制？手部动作的非周期性更强，可能需要更复杂的相位建模。

3. **实时交互控制**：相位幅度和频率的调整是否可交由用户实时交互控制，以用于实际的动画制作管线？这需要 Motion Sampler 具备足够低的推理延迟，且编辑接口需直观映射到动画师的工作流。

4. **跨风格泛化**：风格编码器能否泛化到训练集中未见的运动风格？分部位相位表示是否有助于少样本或零样本的风格迁移？

5. **与物理仿真融合**：在需要物理合理性的场景中（如脚与地面的接触、手持物体的运动），分部位相位如何与物理约束协同工作，避免编辑操作产生物理上不可能的运动？



## 原文 PDF

![[paperPDFs/arxiv_2025/Towards_Synthesized_and_Editable_Motion_In_Betweening_Through_Part_Wise_Phase_Representation.pdf]]

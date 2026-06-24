---
title: SMGDiff Soccer Motion Generation using diffusion probabilistic models
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models.pdf
aliases:
- SSMGUDPM
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 两阶段级联框架：第一阶段基于单步扩散从用户粗粒度控制生成全局轨迹作为强条件，第二阶段基于轨迹条件的自回归扩散模型生成运动，并在推理时通过接触引导模块优化球-脚接触细节。
primary_logic: 将用户控制与运动生成解耦为轨迹规划与条件扩散，并引入基于物理启发式损失的接触引导，可在无物理模拟条件下实现实时可控且逼真的足球动作。
claims:
- SMGDiff在FID指标上达到0.1813，大幅优于所有基线方法。
- 技能分类准确率达到93.3%，远超LMP、MANN-DP和CM。
- 接触引导模块使FID从0.3704降至0.3580，并有效减少漏接触现象。
- 轨迹生成模型将运动多样性从2.4331提升至2.6925，同时改善FID。
---

# SMGDiff Soccer Motion Generation using diffusion probabilistic models

> [!tip] 核心洞察
> 将用户控制与运动生成解耦为轨迹规划与条件扩散，并引入基于物理启发式损失的接触引导，可在无物理模拟条件下实现实时可控且逼真的足球动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMGDiff：基于扩散概率模型的足球运动生成 |
| 英文题名 | SMGDiff Soccer Motion Generation using diffusion probabilistic models |
| 会议/期刊 | ICCV 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SMGDiff |
| Dataset | Soccer-X |

> [!tip] 效果简介
> - Soccer-X 上，FID ↓ 0.1813 vs LMP / MANN-DP / CM (具体值参见原文表1) (显著降低)；Foot Sliding ↓ 0.8543 vs 同上 (显著降低)；Skill Accuracy ↑ 93.3% vs 同上 (显著提升)。

## 概述

**核心问题**：现有足球运动生成方法（如基于运动匹配或特定技能控制器）难以在实时交互条件下同时满足高运动质量、多样化技能覆盖和精确的球-脚交互，且缺乏大规模高质量足球运动数据集。

**方法定位**：SMGDiff 提出一种**两阶段级联扩散框架**，将用户控制与运动生成解耦为轨迹规划与条件扩散。第一阶段基于单步扩散从用户粗粒度控制（技能标签、目标轨迹点）生成平滑的全局轨迹作为强条件；第二阶段采用基于 Transformer 的自回归扩散模型，以轨迹和过去运动为条件生成未来足球运动，并在推理时通过**接触引导模块（Contact Guidance Module, CGM）** 利用物理启发式损失优化球-脚接触细节。

**核心贡献**：
- 构建了包含约 **108 万帧、超过 10 小时、30 名球员、6 类足球技能**的 Soccer-X 数据集（Figure 3）。
- 在 Soccer-X 基准上，SMGDiff 的 **FID 达到 0.1813**，技能分类准确率达到 **93.3%**，足部滑动降至 0.8543，均大幅优于 LMP、MANN-DP 和 CM 等基线方法（Table 1）。
- 消融实验证实：轨迹生成模型将运动多样性从 2.4331 提升至 2.6925，接触引导模块使 FID 从 0.3704 降至 0.3580，并有效减少漏接触现象（Table 2；Figure 6）。
- 去噪步数设为 8 时达到推理速度（12 ms）与生成质量的最佳平衡（Table 3），仅在最后两步应用接触引导获得最低 FID（Table 4）。

**局限与展望**：当前方法仅处理球-脚交互，未涉及多球员场景，且生成结果未经物理引擎精炼。未来可探索与物理模拟器整合、扩展至多人协作/对抗场景，以及将启发式接触引导替换为可学习的自适应机制。

## 背景与动机

### 问题背景

足球运动生成是角色动画领域的高难度课题。与常规的人体运动生成不同，足球场景不仅要求角色动作自然流畅，还涉及球-脚交互的精确建模——脚部需要在合适的时机与球发生接触，驱动球体产生符合物理直觉的运动轨迹。这一任务在实时交互式应用（如体育游戏、虚拟现实训练）中尤为关键：系统必须根据用户提供的粗粒度控制信号（技能标签、目标位移点），在毫秒级延迟内生成高质量、多样化的足球动作。

### 现有方法的瓶颈

当前足球运动生成方法面临三个核心瓶颈：

**1. 运动质量与技能覆盖的权衡困境。** 基于局部运动相位的方法，如 **LMP**（Starke et al., ACM Trans. Graph., 2020），能够实现实时合成，但生成的动作在足部滑动和技能准确性方面存在明显缺陷。基于模式自适应网络的方法，如 **MANN-DP**（Starke et al., 2019; Zhang et al., 2018），虽然提升了运动多样性，但在球-脚交互的精细度上仍显不足。而基于分类码本匹配的角色控制器 **CM**（Starke et al., ACM Trans. Graph., 2024）则受限于码本容量，难以覆盖丰富的足球技能空间。

**2. 球-脚交互的精确建模缺失。** 现有方法普遍缺乏对球-脚接触的显式优化机制。在快速变向、急停转身等高频足球动作中，角色脚部与球体之间容易出现“漏接触”现象——即球运动方向改变却未检测到对应的脚部接触帧，导致生成结果在物理上不可信。

**3. 数据与实时性的双重约束。** 大规模、高质量的足球运动捕捉数据长期匮乏，限制了数据驱动方法的潜力。同时，实时交互场景对推理速度有严苛要求，使得依赖物理模拟器进行后处理精炼的方案难以部署。

### 本文动机

针对上述瓶颈，本文提出 **SMGDiff**，核心动机在于将运动生成的控制规划与精细合成解耦，通过两阶段级联框架实现实时、可控且逼真的足球运动生成。第一阶段利用单步扩散模型将用户粗粒度控制转化为平滑的全局轨迹，为后续合成提供强条件；第二阶段基于自回归扩散模型在轨迹条件驱动下生成运动序列，并在推理时引入基于物理启发式损失的接触引导模块，在不依赖物理模拟的条件下优化球-脚接触细节。这一设计旨在同时突破运动质量、技能覆盖和交互精度的上限。

## 核心创新

SMGDiff 的核心创新在于将**用户粗粒度控制与高质量运动生成解耦为两阶段级联框架**，并引入**基于物理启发式损失的接触引导机制**，在无需物理模拟的条件下实现实时、可控且逼真的足球动作生成。

### 1. 两阶段解耦框架：轨迹规划 + 条件扩散

现有足球运动生成方法（如 **LMP**（Starke et al., ACM Trans. Graph., 2020）、**MANN-DP**（Starke et al., 2019; Zhang et al., 2018）、**CM**（Starke et al., 2024））通常将用户控制信号与运动合成紧密耦合，难以在实时交互下同时兼顾运动质量、技能覆盖和球-脚交互精度。SMGDiff 的关键设计是将这一耦合拆解为两个独立阶段：

- **第一阶段（轨迹生成模型，TGM）**：采用单步扩散模型，将用户提供的技能标签 $S$ 和目标轨迹点 $G$ 等粗粒度控制信号，转化为平滑的未来全局轨迹 $\mathbf{T}^{\mathcal{F}}$。这一设计使得轨迹规划与运动风格解耦，为下游运动生成提供强条件约束。
- **第二阶段（足球运动扩散模型）**：以轨迹 $\mathbf{T}^{\mathcal{F}}$ 和过去运动 $\mathbf{X}^{\mathcal{P}}$ 为条件，利用基于 Transformer 的自回归扩散模型生成未来运动序列 $\mathbf{X}^{\mathcal{F}}$，同时输出人体运动、球运动和接触标签。

这一解耦设计的因果机制在于：**TGM 将用户稀疏控制转化为密集的时空约束，使扩散模型专注于运动细节生成而非全局规划**，从而在保持实时性的同时提升运动质量和技能覆盖率。

**证据支撑**：消融实验（Table 2）表明，移除 TGM（w/o TGM）导致运动多样性从 2.6925 降至 2.4331，FID 从 0.3580 升至 0.3646，验证了轨迹生成对运动多样性和质量的贡献（置信度 0.95）。定性结果（Figure 5）进一步展示了 TGM 在相同输入条件下生成多样化轨迹的能力。

### 2. 接触引导模块：推理阶段的物理启发式优化

球-脚接触的精确性是足球运动生成的核心难点。SMGDiff 提出**接触引导模块（CGM）**，在扩散推理的最后两步引入基于物理启发式损失的引导优化，无需在训练阶段引入物理模拟器。

CGM 的核心机制包括：
- **接触检测**：基于球加速度阈值 $\tau_a = 2\,\text{m/s}^2$ 判断接触事件 $\hat{c}_b = \mathbb{I}(\|b_a\| > \tau_a)$。
- **距离计算与抬脚优先**：计算脚关节与球的最小距离 $d$，并对触地关节施加惩罚权重，优先选择抬起的脚进行接触。
- **引导损失**：当距离超过阈值 $\tau_d = 0.1\,\text{m}$ 且检测到接触时，激活引导损失 $L = \sum_{i=1}^{F} d^i \cdot \frac{\mathbb{I}(d^i > \tau_d) \cdot \hat{c}_b^i}{\mathbb{I}(d^i > \tau_d) + \delta}$，在推理过程中直接优化球-脚接触精度。

**证据支撑**：消融实验（Table 2）显示，移除 CGM（w/o CGM）导致 FID 从 0.3580 升至 0.3704（置信度 0.95）。定性结果（Figure 6）表明 CGM 有效修复了球变向时的漏接触现象。此外，Table 4 的消融表明仅在最后两步应用接触引导（End 2）获得最低 FID（0.3580），优于全程引导策略。

### 3. 球位置相对化表示

为增强模型对球员-球空间关系的建模能力，SMGDiff 引入基于距离权重的球位置相对化表示：

$$w_b = 1 - \|b_p^{xy} - h_p^{xy}\| / r, \quad r = 2\,\text{m}$$

$$b_p^{\prime} = w_b \cdot (b_p - h_p)$$

当球距离人物根部超过 2m 时权重衰减为零，使模型在球远离时忽略其精确位置，聚焦于人物运动本身。这一设计简化了条件空间，提升了扩散模型对足球场景的适应性。

### 4. 方法定位与创新边界

与现有方法的本质差异在于：
- **相对于 LMP/MANN-DP/CM 等非扩散方法**：SMGDiff 利用扩散模型的生成能力大幅提升运动质量和技能覆盖率（FID 0.1813 vs. 基线方法显著更高，Skill Accuracy 93.3%），同时保持实时推理（12ms/帧）。
- **相对于通用扩散运动模型**：SMGDiff 的两阶段解耦和接触引导模块专门针对足球场景中球-脚交互的精确性需求设计，这是通用框架未覆盖的 changed slot。

**需注意的局限**：该框架目前仅处理球与脚的交互，未涉及身体其他部位的触球；未支持多球员对抗场景；生成结果未经物理引擎精炼。这些构成了后续创新的潜在 changed slots。

## 整体框架

SMGDiff 采用**两阶段级联框架**，将用户粗粒度控制信号转化为高质量、多样化的足球运动序列。其核心设计理念是**将控制规划与运动生成解耦**：第一阶段负责将稀疏的用户指令转换为平滑的全局轨迹作为强条件，第二阶段则在该轨迹条件的引导下生成精细的人体运动与球运动，并在推理时通过接触引导优化球-脚交互细节。

### 输入输出流

系统接收三类用户控制信号：
- **技能标签** $S$：指定足球动作类型（如带球、传球、射门等）
- **目标轨迹点** $G$：角色期望到达的平面位置
- **历史运动序列** $\mathbf{X}^{\mathcal{P}}$：过去 $P$ 帧的人体姿态、球位置及接触标签

输出为未来 $F$ 帧的完整运动序列 $\mathbf{X}^{\mathcal{F}}$，包含人体关节旋转、根节点位移、球位置以及脚-球接触标签。

### 模块关系与数据流

整体流程如 Figure 2 所示，分为三个核心模块：

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of SMGDiff. Our framework consists of two stages: In the trajectory generation stage, we transform soccer skill label S, target trajectory point G from user control, and past trajectory*

**1. 轨迹生成模型（Trajectory Generation Model, TGM）**

该模块将用户粗粒度控制信号转化为精细的未来全局轨迹 $\mathbf{T}^{\mathcal{F}}$。输入包括技能标签 $S$、目标轨迹点 $G$ 以及历史轨迹 $\mathbf{T}^{\mathcal{P}}$，通过单步扩散模型（single-step diffusion）在一步内完成轨迹预测。生成的轨迹包含未来 $F$ 帧的角色根节点平面位置与朝向，为下游运动生成提供**强空间条件**。

**2. 足球运动扩散模型（Soccer Motion Diffusion Model）**

这是框架的核心生成模块，采用基于 Transformer 的自回归扩散模型。在每个推理步中，模型以噪声运动序列 $\mathbf{X}_T^{\mathcal{F}}$ 和条件信息 $\mathbf{C}$ 为输入，其中条件 $\mathbf{C}$ 由技能标签 $S$、第一阶段生成的未来轨迹 $\mathbf{T}^{\mathcal{F}}$ 以及历史运动 $\mathbf{X}^{\mathcal{P}}$ 拼接而成。模型通过迭代去噪逐步恢复高质量的未来运动序列 $\hat{\mathbf{X}}_0^{\mathcal{F}}$。

为处理球-人交互，系统引入了**球控制权重**机制：根据球与角色根部的水平距离计算权重 $w_b = 1 - ||b_p^{xy} - h_p^{xy}|| / r$（作用半径 $r=2\text{m}$），进而将球的全局位置转换为相对于角色的位置 $b_p' = w_b \cdot (b_p - h_p)$，使模型能更好地学习球与角色的空间关系。

**3. 接触引导模块（Contact Guidance Module, CGM）**

该模块仅在推理阶段的后两步激活，通过物理启发的损失函数优化球-脚接触精度。具体而言，模块根据球加速度幅值检测接触事件 $\hat{c}_b = \mathbb{I}(||b_a|| > \tau_a)$（阈值 $\tau_a=2\text{ m/s}^2$），计算脚关节与球的最小距离 $d$，并对超过距离阈值 $\tau_d=0.1\text{m}$ 的漏接触帧施加引导损失，从而在扩散去噪过程中显式修正接触细节。

### 训练策略

扩散模型的训练损失由四项组成：
$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{foot}} \mathcal{L}_{\mathrm{foot}}$$
其中 $\mathcal{L}_{\mathrm{simple}}$ 为基础重构损失，$\mathcal{L}_{\mathrm{pos}}$ 和 $\mathcal{L}_{\mathrm{vel}}$ 分别约束位置和速度精度，$\mathcal{L}_{\mathrm{foot}}$ 通过比较相邻帧的前向运动学差异来惩罚脚部滑动。

### 推理效率

通过将去噪步数设为 8 步，模型在保持生成质量（FID 0.3704）的同时实现了约 12ms 的单步推理速度，满足实时交互需求。

### 补充图表

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/001_Figure_1.jpg]]
*Figure 1: Our method, SMGDiff, enables users to control soccer motions based on character displacement and soccer skill, simulating an interactive gameplay experience. It can generate a diverse range of high-quality soccer motions while ensuring real-time performance*

## 核心模块与公式推导

### 2.1 两阶段级联框架

SMGDiff 将用户控制与运动生成解耦为两个串联阶段（Figure 2）。第一阶段 **轨迹生成模型（Trajectory Generation Model, TGM）** 接收用户粗粒度控制信号——技能标签 $S$ 与目标轨迹点 $G$——并联合过去轨迹 $\mathbf{T}^{\mathcal{P}}$，通过单步扩散模型生成平滑的未来全局轨迹 $\mathbf{T}^{\mathcal{F}}$。该轨迹作为强条件馈入第二阶段。第二阶段 **足球运动扩散模型（Soccer Motion Diffusion Model）** 是一个基于 Transformer 的自回归扩散模型，以轨迹条件 $\mathbf{T}^{\mathcal{F}}$、技能标签 $\mathbf{S}$ 和过去运动 $\mathbf{X}^{\mathcal{P}}$ 拼接而成的条件 $\mathbf{C}$ 为输入，从噪声运动序列 $\mathbf{X}_T^{\mathcal{F}}$ 逐步去噪生成未来运动 $\hat{\mathbf{X}}_0^{\mathcal{F}}$（包含人体运动、球运动与接触标签）。推理时，**接触引导模块（Contact Guidance Module, CGM）** 在扩散过程的特定步骤施加基于物理启发式损失的引导，优化球-脚接触精度。

### 2.2 球-角色相对位置表示

为将全局球位置转换为以角色为中心的表示，SMGDiff 引入基于距离的权重机制。首先计算球与角色根部水平距离的权重：

$$w_b = 1 - \frac{\|b_p^{xy} - h_p^{xy}\|}{r} \tag{1}$$

其中 $r = 2\text{m}$ 为作用半径，$b_p^{xy}$ 与 $h_p^{xy}$ 分别为球和角色根部的水平位置。该权重在球靠近角色时趋近 1，超出半径后衰减。随后利用该权重将球的全局位置转换为相对位置：

$$b_p^{\prime} = w_b \cdot (b_p - h_p) \tag{2}$$

这一相对表示使模型能够以角色为中心感知球的位置，增强对球-脚交互的建模能力。

### 2.3 轨迹生成模型：单步扩散

TGM 采用单步扩散逆过程，将用户提供的目标轨迹点 $G$ 和技能标签 $S$ 转化为完整的未来轨迹 $\mathbf{T}^{\mathcal{F}}$。其逆过程形式化为：

$$p_{\theta}(\mathbf{z}_{0:1}) := \epsilon \, p_{\theta}(\mathbf{z}_0|\mathbf{z}_1), \quad p_{\theta}(\mathbf{z}_0|\mathbf{z}_1) := \mathcal{N}\big(\mathbf{z}_0; \mu_{\theta}(\mathbf{z}_1, 1), \Sigma_{\theta}(\mathbf{z}_1, 1)\big) \tag{3}$$

其中 $\mathbf{z}_1$ 为纯噪声先验，$\mathbf{z}_0$ 为生成的轨迹。单步扩散的设计使轨迹生成可在极低延迟下完成，为实时交互提供基础。

### 2.4 足球运动扩散模型：自回归条件扩散

运动生成阶段采用标准扩散范式。前向过程向真实运动 $\mathbf{X}_0^{\mathcal{F}}$ 逐步注入高斯噪声：

$$q(\mathbf{X}_t^{\mathcal{F}}|\mathbf{X}_0^{\mathcal{F}}) = \mathcal{N}\big(\sqrt{\bar{\alpha}_t}\,\mathbf{X}_0^{\mathcal{F}}, (1 - \bar{\alpha}_t)\mathbf{I}\big) \tag{4}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数。模型 $\phi$ 学习从噪声状态 $\mathbf{X}_t^{\mathcal{F}}$ 和条件 $\mathbf{C}$ 预测原始运动 $\hat{\mathbf{X}}_{\phi}^{\mathcal{F}}$，基础训练目标为简单重构损失：

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{\mathbf{X}_0^{\mathcal{F}}, t}\left[\|\mathbf{X}_0^{\mathcal{F}} - \hat{\mathbf{X}}_{\phi}^{\mathcal{F}}(\mathbf{X}_t^{\mathcal{F}}, t, \mathbf{C})\|_2^2\right] \tag{5}$$

完整的训练损失在此基础上叠加位置损失 $\mathcal{L}_{\text{pos}}$、速度损失 $\mathcal{L}_{\text{vel}}$ 和足部接触损失 $\mathcal{L}_{\text{foot}}$：

$$\mathcal{L} = \mathcal{L}_{\text{simple}} + \lambda_{\text{pos}}\mathcal{L}_{\text{pos}} + \lambda_{\text{vel}}\mathcal{L}_{\text{vel}} + \lambda_{\text{foot}}\mathcal{L}_{\text{foot}} \tag{9}$$

其中足部接触损失通过比较连续帧的前向运动学差异，并以地面接触掩码 $c_g$ 加权，显式惩罚足部滑动：

$$\mathcal{L}_{\text{foot}} = \frac{1}{F}\sum_{i=1}^{F} \left\|\big(\text{FK}(\hat{x}_0^{i+1}) - \text{FK}(\hat{x}_0^i)\big) \cdot c_g^i\right\|_2^2$$

### 2.5 接触引导模块：推理时物理启发式优化

CGM 在扩散推理阶段通过接触损失函数引导优化，修复漏接触现象。首先根据球加速度幅值检测接触事件：

$$\hat{c}_b = \mathbb{I}(\|b_a\| > \tau_a) \tag{10}$$

其中 $\tau_a = 2\,\text{m/s}^2$ 为加速度阈值。当球加速度超过阈值时判定为脚-球接触发生。随后计算脚关节与球的距离，并对触地关节施加惩罚以优先选择抬起的脚：

$$d = \min_{j \in \text{footjoints}} \left((f_p^j - b_p) \cdot \big(1 + (w_d - 1) \cdot c_g^j\big)\right) \tag{11}$$

其中 $f_p^j$ 为第 $j$ 个脚关节位置，$c_g^j$ 为地面接触指示，$w_d$ 为触地惩罚权重。最终引导损失在距离超过阈值 $\tau_d = 0.1\text{m}$ 且检测到接触时激活：

$$L = \sum_{i=1}^{F} d^i \cdot \frac{\mathbb{I}(d^i > \tau_d) \cdot \hat{c}_b^i}{\mathbb{I}(d^i > \tau_d) + \delta} \tag{12}$$

其中 $\delta$ 为防止除零的小常数。消融实验表明，仅在扩散过程的最后两步施加该引导（End 2 策略）可获得最低 FID（0.3580），优于全程引导（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative evaluation of the Contact Guidance Module (CGM). Given identical conditions, CGM effectively prevents instances of missed contact when the ball changes direction. Contact frames represent points where the ball’s trajectory shifts*

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative evaluation of the Trajectory Generation Model (TGM). Given identical conditions, TGM enhances motion diversity. The dashed line represents the generated trajectory*

## 实验与分析

### 主实验结果

SMGDiff 在自建数据集 **Soccer-X** 上与三类代表性基线方法进行了定量对比：基于局部运动相位的 **LMP**（Starke et al., ACM Trans. Graph., 2020）、结合周期自动编码器与模式自适应网络的 **MANN-DP**（Starke et al., 2019; Zhang et al., 2018），以及分类码本匹配控制器 **CM**（Starke et al., 2024）。如 **Table 1** 所示，SMGDiff 在所有指标上均取得显著优势：

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison between our method and baseline methods including LMP [57], MANN-DP [59, 72] and CM [60]. Our method outperforms the baseline methods in terms of both motion quality and condition alignment*

- **运动质量（FID ↓）**：SMGDiff 达到 **0.1813**，大幅低于所有基线方法，表明生成运动的分布与真实数据高度一致。
- **足部滑动（Foot Sliding ↓）**：SMGDiff 降至 **0.8543**，显著改善了足球运动中常见的足部滑移伪影。
- **技能分类准确率（Skill Accuracy ↑）**：SMGDiff 达到 **93.3%**，远超 LMP、MANN-DP 和 CM，证明其对用户指定技能标签的精确响应能力。
- **运动多样性（Diversity ↑）**：SMGDiff 同时取得了最高的多样性分数，表明其在保持条件一致性的前提下能生成更丰富的运动变化。

定性对比（**Figure 4**）进一步印证了上述结论：基线方法生成的运动存在明显的足部滑动和技能匹配偏差，而 SMGDiff 在手足轨迹和运动细节上均表现出明显优势。

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison between our method and baseline methods including LMP [57], MANN-DP [59, 72] and CM [60]. The green line represents the trajectories of the hands and feet. The motions generated by the baseline methods exhibit deficiencies in motion quality (such as foot sliding and skill accuracy). Our method significantly surpasses the baseline methods in terms of motion details. More qualitative results can be found in the supplementary video*

### 消融实验

为验证各核心模块的贡献，论文进行了系统消融（**Table 2**）：

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of Trajectory Generation Model (TGM) and Contact Guidance Module (CGM)*

**轨迹生成模型（TGM）的作用**：移除 TGM（w/o TGM）后，FID 从 0.3580 升至 0.3646，多样性从 2.6925 降至 2.4331。这表明 TGM 不仅提供了强条件信号以提升运动质量，还通过轨迹的多样性增强了生成运动的丰富程度。**Figure 5** 的定性结果直观展示了：在相同控制输入下，TGM 能生成不同的全局轨迹，从而引导出差异化的运动序列。

**接触引导模块（CGM）的作用**：移除 CGM（w/o CGM）导致 FID 从 0.3580 升至 0.3704。**Figure 6** 的定性对比揭示了 CGM 的核心价值：当球改变方向时，无 CGM 的模型容易出现漏接触（missed contact），而 CGM 通过基于物理启发式损失的引导，在扩散推理的最后两步有效修复了球-脚接触精度。

### 关键超参数与策略分析

**去噪步数（Table 3）**：实验对比了不同去噪步数对推理速度与生成质量的权衡。将去噪步数设为 **8** 时达到最佳平衡点——推理仅需 **12ms**，同时 FID 保持在 0.3704 的较低水平。进一步增加步数对 FID 的改善有限，但推理耗时线性增长。

**接触引导应用策略（Table 4）**：对比了在扩散推理的不同阶段施加接触引导的效果。实验表明，仅在最后两步应用引导（End 2）获得最低 FID（**0.3580**），优于全程引导或仅最后一步引导。这暗示早期去噪阶段的引导可能干扰扩散模型的去噪过程，而将引导集中在去噪末端能在不破坏生成质量的前提下精确优化接触细节。

### 局限性分析

尽管 SMGDiff 在定量与定性评估中均表现优异，仍存在以下值得关注的局限：

1. **交互范围受限**：当前方法仅建模球与脚的接触，未涉及球与身体其他部位（如头、胸、膝）的交互，限制了颠球、胸部停球等技能的生成。
2. **单人场景假设**：框架未处理多球员交互场景，无法生成传球配合、抢断对抗等涉及球员间互动的足球动作。
3. **物理真实性未精炼**：生成结果未经过物理引擎（如 Isaac Gym）的后处理验证，可能出现违反物理规律的姿态或接触状态。
4. **数据集覆盖偏差**：Soccer-X 数据集虽包含约 108 万帧、6 类足球动作，但可能无法覆盖所有足球技能和高动态比赛环境，限制了模型在真实比赛场景中的泛化能力。

### 公平性说明

需注意以下评估公平性因素：Soccer-X 为自行采集数据集，主要对比方法集中在非扩散的运动合成模型，缺少与同期扩散运动模型（如 CAMDM）在足球领域的直接比较；FID、Foot Sliding、Skill Accuracy 等定量指标可能无法完全反映足球运动的主观感知质量。

### 补充图表

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/009_Table_3.jpg]]
*Table 3: Evaluation of different denoise steps*

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/010_Table_4.jpg]]
*Table 4: Evaluation of contact guidance employment strategy*

![[assets/figures/papers/paper_list_l1775_SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models/figures/003_Figure_3.jpg]]
*Figure 3: The top section exhibits selected highlights of our dataset. The bottom section features a proportion of different soccer motions. In total, our dataset comprises 2398 sequences and captures approximately 1.08 million frames of data*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

足球运动生成在角色动画领域面临独特的挑战：它要求实时交互下同时满足高运动质量、多样化技能覆盖和精确的球-脚交互。现有方法在此问题上存在结构性不足——**LMP**（Starke et al., ACM Trans. Graph., 2020）基于局部运动相位实现实时合成，但运动匹配精度有限；**MANN-DP**（Starke et al., ACM Trans. Graph., 2019; Zhang et al., ACM Trans. Graph., 2018）结合周期自动编码器与模式自适应网络，然而技能分类准确率远低于SMGDiff（Table 1）；**CM**（Starke et al., ACM Trans. Graph., 2024）采用分类码本匹配的角色控制器，同样在运动细节和条件对齐上表现不足。这些方法的共同瓶颈在于：它们要么依赖局部相位匹配而牺牲全局一致性，要么受限于特定技能的离散码本而缺乏泛化能力，且均未对球-脚接触进行显式建模。

SMGDiff的核心洞察是将用户控制与运动生成解耦为轨迹规划与条件扩散两个阶段，并引入基于物理启发式损失的接触引导——这使得系统在无物理模拟的条件下，仍能实现实时可控且逼真的足球动作。

### 方法谱系中的位置

SMGDiff处于数据驱动运动合成与扩散生成模型的交叉地带。其两阶段级联框架（Figure 2）在方法谱系中占据以下位置：

- **相对于传统运动匹配方法**：LMP和MANN-DP代表基于相位或网络权重的运动匹配范式，它们从数据库中检索或插值运动片段。SMGDiff以扩散模型替代检索机制，从噪声中直接生成运动，在FID指标上达到0.1813，远优于这些基线（Table 1），且技能分类准确率达到93.3%。

- **相对于扩散运动生成方法**：SMGDiff采用自回归扩散模型生成运动序列，与同期扩散运动模型（如MDM、CAMDM）共享扩散范式。但其独特之处在于：(1) 引入轨迹生成模型（TGM）作为强条件，将用户粗粒度控制转化为平滑的全局轨迹；(2) 设计接触引导模块（CGM）在推理时优化球-脚接触精度。消融实验表明，移除TGM导致FID从0.3580升至0.3646，多样性从2.6925降至2.4331；移除CGM使FID升至0.3704（Table 2），验证了这两个模块的关键作用。

- **相对于物理模拟方法**：SMGDiff不依赖物理引擎进行运动精炼，而是通过训练阶段的足部接触损失 $\mathcal{L}_{\text{foot}}$ 和推理阶段的接触引导损失 $L$（Equation 12）来约束物理合理性。这使其在实时性上具有优势（去噪步数设为8时推理仅需12ms，Table 3），但也意味着生成结果可能包含物理上的不准确。

### 适用边界与局限

SMGDiff的设计边界明确，存在以下已知局限：

1. **交互范围受限**：仅考虑球与脚的交互，未涉及球与身体其他部位（如头、胸、膝）的接触。接触引导模块的启发式阈值（$\tau_a=2$ m/s² 检测接触，$\tau_d=0.1$m 判定漏接触）仅针对足部场景设计。

2. **单人场景假设**：框架未处理多球员交互场景，生成的足球动作不涉及不同球员之间的对抗、传球或协防。这限制了其在完整足球比赛模拟中的应用。

3. **物理精度不足**：生成结果未经物理引擎精炼。尽管足部滑动指标降至0.8543（Table 1），但球-脚接触仅通过损失函数引导，缺乏真实的力反馈和碰撞响应。

4. **数据集覆盖有限**：Soccer-X数据集虽包含2398个序列和约108万帧数据（Figure 3），涵盖6类足球动作，但可能无法覆盖所有足球技能和高动态环境变化，对真实比赛场景的泛化性有待验证。

### 开放问题

基于SMGDiff的框架设计，以下方向值得探索：

1. **物理-数据混合生成**：如何将扩散模型与基于物理的角色动画方法（如Isaac Gym）整合？一种可能路径是将扩散模型生成的足球运动作为物理模拟的参考轨迹，通过模仿学习或残差控制实现物理上更真实的执行。

2. **多人交互扩展**：框架的两阶段设计（轨迹规划+条件扩散）理论上可扩展至多人场景——通过联合轨迹生成模型规划多个球员的时空关系，再以交互条件扩散生成协同运动。这需要解决球员间相对位置编码和交互接触建模问题。

3. **自适应接触引导**：接触引导模块中的启发式阈值（$\tau_a$, $\tau_d$, $w_d$）和损失函数能否通过学习方式自适应确定？例如，通过少量物理模拟数据学习接触检测的置信度阈值，可提升泛化能力。

4. **跨场景迁移**：该两阶段框架在其他人-物交互场景（如篮球运球、格斗游戏）中的迁移潜力如何？核心挑战在于接触类型的多样性——篮球涉及手-球持续接触，格斗涉及身体多部位碰撞，需要重新设计接触表示和引导策略。

5. **与同期扩散运动模型的直接比较**：当前实验主要对比非扩散基线，缺少与同期扩散运动模型（如CAMDM在足球领域的适用性）的直接比较，这一空白需要后续工作填补。

## 原文 PDF

![[paperPDFs/ICCV_2025/SMGDiff_Soccer_Motion_Generation_using_diffusion_probabilistic_models.pdf]]

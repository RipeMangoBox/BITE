---
title: "CamCloneMaster: Enabling Reference-based Camera Control for Video Generation"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation.pdf
code_link: null
project_link: https://camclonemaster.github.io/
aliases:
- CamCloneMaster
tags:
- SIGGRAPH_ASIA_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "通过直接输入相机运动参考视频，并采用帧维度的令牌拼接（token concatenation）将参考视频潜变量与生成过程融合，从而实现无参数的相机运动克隆。"
primary_logic: "将相机运动参考视频的3D VAE潜变量与噪声潜变量沿帧维度拼接，利用DiT的3D时空注意力层隐式学习相机运动表征，无需额外模块即可同时支持I2V和V2V任务，大幅提升了相机控制的准确性与便捷性。"
claims:
- "CamCloneMaster 能够直接在无相机参数和无测试时微调的情况下从参考视频克隆相机运动。"
- "采用帧维度令牌拼接将条件令牌与噪声视频令牌结合，无需额外控制模块。"
- "在 RealEstate10K 测试集上，CamCloneMaster 在相机精度和动态质量上大幅超越现有方法，例如 RotErr 仅 1.49 (CameraCtrl 为 2.82)。"
- "RealEstate10K 上 FVD↓ = 993.06"
---

# CamCloneMaster: Enabling Reference-based Camera Control for Video Generation

> [!tip] 核心洞察
> 将相机运动参考视频的3D VAE潜变量与噪声潜变量沿帧维度拼接，利用DiT的3D时空注意力层隐式学习相机运动表征，无需额外模块即可同时支持I2V和V2V任务，大幅提升了相机控制的准确性与便捷性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CamCloneMaster：基于参考视频的相机运动克隆 |
| 英文题名 | CamCloneMaster: Enabling Reference-based Camera Control for Video Generation |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2506.03140) · [Project](https://camclonemaster.github.io/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | CamCloneMaster |
| Dataset | RealEstate10K |

> [!tip] 效果简介
> - RealEstate10K 上，FVD↓ 为 993.06，对比 1355.55 (MotionClone)，变化 -362.49。
> - RealEstate10K 上，Rot Err↓ 为 1.49，对比 2.82 (CameraCtrl)，变化 -1.33。
> - RealEstate10K 上，Trans Err↓ 为 2.37，对比 4.52 (CameraCtrl)，变化 -2.15。

## 概要

### 问题瓶颈

现有相机控制视频生成方法普遍依赖**显式相机参数**（如 Plücker 嵌入）。用户要构建复杂的相机轨迹极为困难；即便借助 MegaSaM 等模型从视频反估相机参数，也存在**精度不足**和**额外计算开销**的问题。这导致相机控制不精确、使用门槛高，且难以处理真实场景中复杂、多样的相机运动。

### 核心方案

CamCloneMaster 提出了一种**无参数相机运动克隆**框架：用户只需提供一段**相机运动参考视频**，模型即可将其中的相机轨迹克隆到目标生成过程中，无需任何显式相机参数或测试时微调。其核心操作是将参考视频的 3D VAE 潜变量与噪声潜变量沿**帧维度进行令牌拼接**，利用 DiT 中的 3D 时空注意力层隐式学习相机运动表征，从而统一支持图像到视频（I2V）和视频到视频（V2V）两类任务。

### 方法定位与知识库定位

CamCloneMaster 在方法谱系中属于**基于参考视频的相机控制生成**，与以下三类基线形成对比：

| 方法类别 | 代表工作 | 控制方式 | 核心局限 |
|---------|---------|---------|---------|
| 基于相机参数的 I2V | **CameraCtrl** (He et al., 2025)、**CamI2V** (Zheng et al., 2024) | 显式相机参数注入 | 用户难以构建轨迹；参数估计引入误差 |
| 基于参考视频的训练免调 | **MotionClone** (Ling et al., 2024) | 注意力图逆推运动 | 相机控制精度不足，动态质量受限 |
| 基于相机参数的 V2V | **ReCamMaster** (Bai et al., 2025)、**DaS** (Gu et al., 2025)、**TrajectoryCrafter** (Yu et al., 2025) | 显式参数 + 重生成 | 参数估计误差累积，视角一致性差 |

CamCloneMaster 的**关键差异化改动**体现在四个维度：
1. **条件输入类型**：从显式相机参数序列切换为相机运动参考视频的潜在表示。
2. **条件注入机制**：从通道拼接或额外控制模块切换为帧维度令牌拼接。
3. **微调策略**：仅微调 3D 时空注意力层，冻结其余参数，兼顾相机克隆精度与视觉质量保持。
4. **训练数据**：构建了大规模合成数据集 Camera Clone Dataset（391K 视频，1,155K 三元组），覆盖多样化的相机轨迹与场景。

### 主要结果

在 **RealEstate10K** 测试集上，CamCloneMaster 在相机精度和动态质量上均大幅超越现有方法：

- **旋转误差（Rot Err）**：1.49，对比 CameraCtrl 的 2.82（↓47%）
- **平移误差（Trans Err）**：2.37，对比 CameraCtrl 的 4.52（↓48%）
- **动态程度（Dynamic Degree）**：50.11，对比 CameraCtrl 的 30.62（↑64%）
- **FVD**：993.06，对比 MotionClone 的 1355.55（↓27%）

在 V2V 任务上，CamCloneMaster 同样取得最优旋转误差（1.36 vs ReCamMaster 1.53）和 FVD（678.06 vs ReCamMaster 718.69）。

**用户研究**（47 名参与者，24 段复杂相机运动参考视频）进一步验证：CamCloneMaster 在相机控制准确性和视觉质量上的用户偏好率显著高于所有基线方法。同时，消融实验证实了帧维度令牌拼接和仅微调 3D 时空注意力层的设计选择对性能的关键贡献。

### 局限与开放问题

当前方案的主要局限在于**令牌序列拼接增加了计算开销**，限制了生成效率。未来方向包括：探索稀疏注意力或潜在丢弃策略以缓解计算负担；处理更复杂的相机轨迹和动态场景；以及将方法扩展到更长视频或更高分辨率。

### 视频生成中的相机控制：一个未闭合的可用性缺口

扩散模型驱动的视频生成在视觉质量和时序连贯性上取得了显著进展，但**可控性**——尤其是对相机运动的精确控制——仍然是一个核心瓶颈。相机运动直接决定了视频的叙事节奏、空间感知和视觉冲击力，因此相机控制能力是衡量视频生成系统实用价值的关键维度。

现有方法普遍采用**显式相机参数**作为控制信号。例如，**CameraCtrl**（He et al., 2025）和 **CamI2V**（Zheng et al., 2024）将相机外参编码为 Plücker 嵌入，通过通道拼接或额外控制模块注入扩散模型；**ReCamMaster**（Bai et al., 2025）和 **TrajectoryCrafter**（Yu et al., 2025）则在视频到视频重生成场景中依赖参数化轨迹。这些方法面临两个相互交织的困难：

1. **参数获取的门槛**：用户难以手动构建复杂的相机轨迹。从参考视频中估计相机参数依赖 MegaSaM 等外部模型，而估计精度不足会直接传导为生成视频的相机误差。论文中的用户研究（Table 3）证实了这一传导效应——使用估计参数（而非真值参数）会显著降低参数依赖方法的生成质量。

2. **控制精度与计算开销的权衡**：即使获得了相机参数，将其有效注入生成过程也需要精心设计的控制模块和完整的模型微调。**MotionClone**（Ling et al., 2024）尝试绕过参数依赖，通过注意力图逆推从参考视频中提取运动信息，但该方法需要测试时微调，且相机控制精度有限——在 RealEstate10K 测试集上 RotErr 高达 2.82，FVD 达 1355.55。

### 核心洞察：用视频本身作为相机运动的载体

CamCloneMaster 的出发点是：**相机运动信息天然蕴含在参考视频的像素流中**，无需将其显式参数化。这一洞察将问题从“估计参数→注入模型”的两阶段管线，重构为“参考视频→直接克隆”的端到端范式。

具体而言，CamCloneMaster 将相机运动参考视频通过 3D VAE 编码为潜变量，然后将其与噪声潜变量沿帧维度进行令牌拼接（token concatenation），形成一个统一的输入序列。DiT 架构中的 3D 时空注意力层在扩散去噪过程中隐式地学习从条件令牌中提取相机运动表征，并将其迁移到生成视频中。这一设计的核心优势在于：

- **零参数依赖**：用户只需提供一个参考视频，无需任何相机参数估计或手动调参。
- **无测试时微调**：条件注入机制在训练阶段已内化，推理时无需额外优化。
- **任务统一**：同一模型同时支持图像到视频（I2V）和视频到视频（V2V）两种生成范式。

### 技术挑战与设计取舍

将参考视频的潜变量直接拼接到输入序列中，看似简单，实则面临两个关键挑战：

- **表征解耦**：模型需要从条件令牌中分离出相机运动信息，同时避免将参考视频的内容（场景、物体）泄漏到生成结果中。CamCloneMaster 通过仅微调 3D 时空注意力层（冻结空间注意力和交叉注意力层）来约束这种解耦——消融实验（Table 6）表明，微调整个 DiT Block 反而会导致 RotErr 从 1.58 恶化到 3.64。

- **训练数据规模**：隐式学习相机运动表征需要大规模、多样化的配对数据。为此，论文基于 Unreal Engine 5 构建了 Camera Clone Dataset，包含 391K 视频和 1,155K 个（参考视频，目标视频）三元组，覆盖多场景、多角色和多相机轨迹组合。

### 在方法谱系中的定位

CamCloneMaster 处于**参考视频驱动**与**隐式相机表征学习**的交叉点。与参数依赖方法（CameraCtrl、ReCamMaster 等）相比，它消除了参数估计的中间环节；与注意力图逆推方法（MotionClone）相比，它避免了测试时微调的计算开销。其帧维度令牌拼接机制在概念上类似于视频编辑中的条件注入策略，但首次将其系统性地应用于相机运动克隆任务，并通过选择性微调策略实现了相机运动与内容的有效解耦。

## 核心方法与创新机理

CamCloneMaster 的核心创新在于**将相机控制从显式参数依赖中解放出来**，转而采用“参考视频即控制信号”的范式。这一转变通过三个紧密耦合的 changed slots 实现，形成了一条从输入类型、注入机制到训练策略的完整创新链。

### 1. 条件输入类型：从相机参数到参考视频潜变量

现有相机控制方法（如 **CameraCtrl** (He et al., 2025)、**CamI2V** (Zheng et al., 2024)）依赖显式相机参数序列（如 Plücker 嵌入）作为条件输入。这种设计存在两重瓶颈：其一，用户难以手动构建复杂的相机运动轨迹；其二，从视频估计相机参数的模型（如 MegaSaM）存在精度不足的问题，导致控制信号本身带有误差。

CamCloneMaster 将条件输入**替换为相机运动参考视频的潜在表示**。具体而言，给定一个相机运动参考视频 $V_{\mathrm{cam}}$ 和一个可选的画面内容参考视频 $V_{\mathrm{cont}}$，3D VAE 编码器将其分别映射为条件潜变量 $z_{\mathrm{cam}}$ 和 $z_{\mathrm{cont}}$：

$$z_{i} = \varepsilon(V_{i}), \quad V_{i} \in \{V_{\mathrm{cam}}, V_{\mathrm{cont}}\}$$

这一设计的因果作用是**彻底消除了相机参数估计环节**，使得控制信号直接来源于参考视频的视觉-运动特征，避免了参数估计误差的累积。

### 2. 条件注入机制：帧维度令牌拼接（Frame Concatenation）

条件信号如何注入生成过程是第二个关键 changed slot。参数依赖方法通常采用通道拼接或额外的控制模块（如注意力图引导）来注入相机条件，这些方案引入了额外的参数和计算开销。

CamCloneMaster 采用**沿帧维度的令牌拼接**作为注入机制。具体流程为：将条件潜变量和噪声潜变量 $z_t$ 分别通过 Patchify 操作转换为令牌序列：

$$x_{j} = \mathrm{Patchify}(z_{j}), \quad z_{j} \in \{z_{\mathrm{cam}}, z_{\mathrm{cont}}, z_{t}\}$$

随后沿帧维度拼接为统一的输入序列：

$$x_{\mathrm{input}} = \mathrm{Frame.Concat}(x_{t}, x_{\mathrm{cam}}, x_{\mathrm{cont}})$$

这一设计的核心洞察在于：DiT 架构中的 **3D 时空注意力层天然具备跨帧信息交互能力**。将条件令牌与噪声令牌沿帧维度拼接后，3D 时空注意力可以隐式地学习参考视频中的相机运动表征，并将其传递到生成视频的对应帧中。这实现了**无额外控制模块的相机运动克隆**，使得单一模型可以同时支持 I2V 和 V2V 两种任务。

消融实验（Table 5）验证了这一设计的有效性：帧维度拼接在相机精度（Rot Err 1.49, Trans Err 2.37）和视觉质量（FVD 993.06）上全面优于通道拼接和仅时域层注入等替代方案。

### 3. 训练策略：选择性微调 3D 时空注意力层

第三个 changed slot 在于微调策略。CamCloneMaster **仅微调 DiT Block 中的 3D 时空注意力层，冻结其他所有参数**。这一策略的因果逻辑是：相机运动信息主要通过时序维度传递，而空间生成能力（2D 空间注意力）和文本语义理解（交叉注意力）已由预训练基模型充分习得，无需调整。

消融实验（Table 6）证实了这一点：仅微调 3D 时空注意力层相比微调整个 DiT Block，在相机克隆精度上显著更优（Rot Err 1.58 vs 3.64），同时保持了相当的视觉质量。这表明冻结空间层有助于**保留基模型的画面生成先验**，避免过拟合导致的质量退化。

### 4. 数据支撑：Camera Clone Dataset

上述创新的实现离不开大规模训练数据的支撑。CamCloneMaster 构建了 **Camera Clone Dataset**（391K 视频, 1,155K 三元组），通过在 Unreal Engine 5 中渲染多相机轨迹的 3D 场景，获得了精确配对的相机运动-画面内容参考视频对。这一合成数据集为模型学习从参考视频中提取相机运动表征提供了充分的监督信号。

### 创新总结

CamCloneMaster 的创新链可以概括为：**参考视频输入 → 帧维度令牌拼接 → 3D 时空注意力隐式学习相机运动 → 选择性微调保护生成先验**。这一设计绕过了相机参数估计的精度瓶颈，以极简的架构修改（仅改变输入拼接方式和微调范围）实现了相机运动克隆，在 RealEstate10K 测试集上将旋转误差从 CameraCtrl 的 2.82 降至 1.49，同时将动态程度从 30.62 提升至 50.11。

CamCloneMaster 的整体 pipeline 围绕“以参考视频替代显式相机参数”这一核心设计展开，通过将相机运动参考视频的潜在表示直接注入扩散变换器（DiT）的去噪过程，实现无需测试时微调的相机运动克隆。框架由五个关键模块串联构成：**3D VAE 编码器**、**Patchify 令牌化**、**帧维度拼接（Frame Concatenation）**、**DiT 变换器块**以及 **T5 文本编码器**，其输入输出流如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l1496_https_arxiv_org_abs_2506_03140/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed CamCloneMaster. Given a camera motion reference video and an optional content reference video as inputs, 3D VAE encoder is utilized to convert reference videos into conditional latents $z _ { \mathrm { c a m } }$ and $z _ { \mathrm { c o n t } }$ . We inject the conditional latents into the model by concatenating them with the noise latent along the frame dimension. And only 3D spatial-temporal attention layers in DiT Blocks are trainable modules in the training process

**输入侧**接受两类参考视频：相机运动参考视频 $V_{\mathrm{cam}}$ 和可选的视频内容参考视频 $V_{\mathrm{cont}}$。两者分别经 3D VAE 编码器映射到潜空间，得到条件潜变量 $z_{\mathrm{cam}}$ 与 $z_{\mathrm{cont}}$（见 Eq. 3）。同时，待生成的噪声潜变量 $z_t$ 由前向扩散过程构建：给定干净数据 $x$ 和高斯噪声 $z$，在时间步 $t$ 上通过线性插值得到 $x_t = (1-t)x + t z$（Eq. 1）。

**条件注入**是 CamCloneMaster 区别于参数依赖方法的核心机制。三个潜变量 $z_{\mathrm{cam}}$、$z_{\mathrm{cont}}$、$z_t$ 分别经 Patchify 操作转换为令牌序列 $x_{\mathrm{cam}}$、$x_{\mathrm{cont}}$、$x_t$（Eq. 4），随后沿帧维度拼接为统一输入序列 $x_{\mathrm{input}} = \mathrm{Frame.Concat}(x_t, x_{\mathrm{cam}}, x_{\mathrm{cont}})$（Eq. 5）。这一设计使条件信号与噪声信号在时空维度上完全对齐，无需额外的控制模块或通道拼接，直接利用 DiT 内部的 3D 时空注意力层隐式学习相机运动表征。

**DiT 变换器块**是去噪网络的核心计算单元。每个基础块依次包含 2D 空间自注意力、3D 时空注意力、交叉注意力和前馈网络（FFN）。其中，3D 时空注意力层负责捕获帧间运动依赖，是相机运动克隆的关键计算节点。文本条件 $c_{\mathrm{text}}$ 由 T5 编码器获取，通过交叉注意力层注入。

**训练策略**采用整流流匹配（Rectified Flow）的 MSE 损失（Eq. 2），目标是最小化速度预测器 $v_\theta$ 的输出与目标速度 $(z - x)$ 之间的平方误差。关键设计在于**选择性微调**：训练过程中仅优化 DiT 块内的 3D 时空注意力层参数，冻结 2D 空间注意力、交叉注意力和 FFN 等其他模块。这一策略在保持基模型视觉质量的同时，使模型专注于学习相机运动表征，消融实验证实其相机克隆精度显著优于微调整个 DiT Block 的方案（见 Table 6）。

**数据支撑**方面，CamCloneMaster 使用基于 Unreal Engine 5 渲染的 Camera Clone Dataset 进行训练，包含 391K 视频和 1,155K 三元组，采用 50% I2V 与 50% V2V 的平衡训练策略，使单一模型同时支持相机控制的图像到视频生成和视频到视频重生成任务。

CamCloneMaster 以基于 Transformer 的潜在扩散架构为基础，包含 3D 变分自编码器（3D VAE）用于潜空间映射，以及一系列 Transformer 块用于视频生成。每个基础 Transformer 块由四个核心组件构成：2D 空间自注意力、3D 时空注意力、交叉注意力和前馈网络（FFN）。文本提示嵌入通过 T5 编码器获得，并经由交叉注意力注入模型。

本节聚焦于相机运动克隆的三个关键模块：条件潜变量编码、帧维度令牌拼接，以及选择性微调策略。

### 3D VAE 编码与潜变量提取

给定相机运动参考视频 $V_{\mathrm{cam}}$ 和可选的内容参考视频 $V_{\mathrm{cont}}$，系统利用 3D VAE 编码器将参考视频转换为条件潜变量：

$$z_i = \varepsilon(V_i), \quad V_i \in \{V_{\mathrm{cam}}, V_{\mathrm{cont}}\}$$

其中 $\varepsilon(\cdot)$ 表示 3D VAE 编码器，$z_{\mathrm{cam}}$ 为相机运动潜变量，$z_{\mathrm{cont}}$ 为内容潜变量。这一步骤将高维视频数据压缩到紧凑的潜空间，为后续令牌化处理奠定基础。

### 潜变量令牌化（Patchify）

编码后的潜变量需要转换为 Transformer 可处理的令牌序列。对于条件潜变量和噪声潜变量 $z_t$，统一执行图块化操作：

$$x_j = \mathrm{Patchify}(z_j), \quad z_j \in \{z_{\mathrm{cam}}, z_{\mathrm{cont}}, z_t\}$$

$\mathrm{Patchify}(\cdot)$ 将潜变量沿空间和时间维度切分为固定大小的图块，并映射为令牌序列。这一操作使得不同来源的潜变量具有统一的令牌表示形式。

### 帧维度令牌拼接（Frame Concatenation）

CamCloneMaster 的核心创新在于条件注入机制——帧维度令牌拼接。与现有方法采用的通道拼接或额外控制模块不同，该方法将条件令牌与噪声视频令牌沿帧维度直接拼接，形成统一的输入序列：

$$x_{\mathrm{input}} = \mathrm{Frame.Concat}(x_t, x_{\mathrm{cam}}, x_{\mathrm{cont}})$$

其中 $x_t$ 为当前时间步的噪声令牌，$x_{\mathrm{cam}}$ 为相机运动条件令牌，$x_{\mathrm{cont}}$ 为内容条件令牌。$\mathrm{Frame.Concat}(\cdot)$ 操作沿帧维度拼接这三组令牌，使得 DiT 的 3D 时空注意力层能够隐式学习相机运动表征，无需引入额外的控制模块或显式相机参数。

### 噪声构建与训练目标

训练采用整流流匹配（Rectified Flow）框架。对于给定的干净数据 $\pmb{x}$ 和高斯噪声 $\pmb{z}$，在时间步 $t$ 构建带噪潜变量：

$$\pmb{x}_t = (1 - t)\pmb{x} + t\pmb{z}$$

模型 $v_\theta$ 预测速度场，训练目标为最小化预测速度与目标速度 $(\pmb{z} - \pmb{x})$ 之间的均方误差：

$$\mathcal{L}_{RF}(\theta) = \mathbb{E}_{t,x,z}\left\| v_\theta(\pmb{x}_t, t, c_I, c_{\mathrm{text}}) - (\pmb{z} - \pmb{x}) \right\|_2^2$$

其中 $c_I$ 为图像条件，$c_{\mathrm{text}}$ 为文本条件。该损失函数驱动模型学习从噪声到数据的整流路径，使去噪过程高效且稳定。

### 选择性微调策略

为在相机克隆精度与训练效率之间取得平衡，CamCloneMaster 采用选择性微调策略：仅优化 DiT 块内的 3D 时空注意力层，冻结其余所有参数（包括 2D 空间注意力、交叉注意力、FFN 以及 3D VAE）。消融实验证实，相比微调整个 DiT Block，仅微调 3D 时空注意力层能获得更优的相机克隆精度（Rot Err 1.58 vs 3.64）和视觉质量，同时显著降低训练开销。

## 实验与关键发现

### 核心实验设计

实验围绕两个任务展开：相机控制图像到视频生成（I2V）和相机控制视频到视频重生成（V2V）。评估在 **RealEstate10K** 和 **Koala-36M** 两个公开测试集上进行，指标覆盖相机精度、视觉质量和动态程度三个维度。相机精度指标（Rot Err、Trans Err、Cam MC）统一使用 MegaSaM 估计相机参数后计算，确保与参数依赖方法可比。所有基线方法均按其原始设定运行，CamCloneMaster 无需测试时微调。

### 主结果分析

**Table 1** 汇总了 I2V 和 V2V 任务的核心定量结果。在 I2V 任务上，CamCloneMaster 在相机精度和动态质量上全面领先：

- **Rot Err 仅 1.49**，相比 CameraCtrl（He et al., 2025）的 2.82 降低 47%，相比 CamI2V（Zheng et al., 2024）的 2.14 降低 30%。这表明帧维度令牌拼接能更精确地捕获参考视频中的旋转运动。
- **Trans Err 2.37**，远低于 CameraCtrl 的 4.52 和 CamI2V 的 3.43，平移误差分别降低 48% 和 31%。
- **Dynamic Degree 50.11**，比 CameraCtrl 的 30.62 高出 64%，说明生成视频的相机运动幅度更接近参考视频，而非趋于静态。
- 在视觉质量上，**FVD 993.06** 优于 MotionClone（Ling et al., 2024）的 1355.55，但略高于 CamI2V 的 868.77。这一权衡源于令牌拼接引入的额外序列长度，对视频帧间的时序一致性有轻微影响。

在 V2V 任务上，CamCloneMaster 与专门设计的 V2V 方法对比同样具有竞争力：

- **Rot Err 1.36**，优于 ReCamMaster（Bai et al., 2025）的 1.53 和 DaS（Gu et al., 2025）的 1.54，说明通过参考视频隐式学习相机运动比显式参数估计更鲁棒。
- **FVD 678.06**，低于 ReCamMaster 的 718.69，表明 CamCloneMaster 在保持视角一致性的同时，视频质量未受损。

**Table 2** 进一步验证了 V2V 重生成的视角一致性。CamCloneMaster 在 Matching Pixels（1332.34）和 CLIP-V（88.77）上均取得最优，证明其能有效保持原视频内容，同时克隆目标相机轨迹。

### 消融实验

消融实验聚焦两个关键设计选择：条件注入机制和训练策略。

**条件注入机制（Table 5）**：对比了四种方案——帧维度拼接（CamCloneMaster）、通道维度拼接、仅在时域层注入、以及同时使用时域和空间层注入。帧维度拼接在所有相机精度指标上均最优（Rot Err 1.49，Trans Err 2.37），验证了沿帧维度拼接能让 3D 时空注意力层自然地建立参考运动与生成帧之间的对应关系。通道拼接虽能保持较好的视觉质量（FVD 930.21），但 Rot Err 升至 3.71，相机克隆精度显著下降。

**训练策略（Table 6）**：对比了仅微调 3D 时空注意力层与微调整个 DiT Block。仅微调注意力层在相机精度上明显更优（Rot Err 1.49 vs 3.64），说明冻结其他参数能防止模型在有限数据上过拟合，同时保留预训练基模型的生成能力。微调整个 Block 虽在 FVD 上略优（62.54 vs 64.65），但相机控制精度大幅退化。

### 用户研究

**Table 3** 揭示了参数估计误差对相机控制的关键影响。使用 MegaSaM 估计参数时，CameraCtrl 的用户偏好率从 GT 参数下的 64.1% 骤降至 17.2%，CamI2V 从 52.9% 降至 14.3%。这直接证明了 CamCloneMaster 绕过参数估计的设计动机——参数估计误差在复杂轨迹上会严重损害控制精度。

**Table 4** 展示了 CamCloneMaster 与各基线在 24 个互联网采集的复杂相机运动视频上的用户偏好。在相机准确性维度，CamCloneMaster 获得 65.3% 的偏好率，远高于 CameraCtrl（17.2%）和 MotionClone（14.0%）。在视频-文本一致性和时序一致性上同样领先，表明该方法在真实场景的复杂运动中具有实用优势。

### 失败模式与局限

1. **计算开销**：帧维度拼接将输入序列长度扩展为原来的 3 倍（噪声令牌 + 相机参考令牌 + 内容参考令牌），导致推理时显存和延迟增加。论文明确指出这是主要限制，未来可探索稀疏注意力或潜在丢弃策略。

2. **极端动态场景**：当参考视频包含剧烈抖动、快速旋转或大幅变焦时，3D VAE 的压缩可能导致运动细节丢失，进而影响克隆精度。这一场景在 Camera Clone Dataset 中覆盖有限，需要手动验证。

3. **长视频生成**：当前方法基于固定帧数训练，扩展到更长视频时，帧维度拼接的序列长度线性增长，可能超出 DiT 的上下文窗口限制。

4. **内容泄漏风险**：当内容参考视频与相机参考视频相同时，模型可能直接复制参考帧而非生成新内容。论文未对此提供消融分析，需要在实际使用中注意。

![[assets/figures/papers/paper_list_l1496_https_arxiv_org_abs_2506_03140/figures/004_Table_1.jpg]]
*Table 1: Quantitative Results for Camera-Controlled Image-to-Video Generation and Video-to-Video Generation. The best performance is in boldface, while the second is underlined. Sub. Cons. and Bg. Cons. denote Subject Consistency and Background Consistency, respectively, as defined in Sec. 5.1, here and after*

![[assets/figures/papers/paper_list_l1496_https_arxiv_org_abs_2506_03140/figures/007_Table_2.jpg]]
*Table 2: Quantitative Results for Camera-Controlled Video-to-Video Re-generation on View Consistency. The best performance is in boldface, while the second is underlined*

![[assets/figures/papers/paper_list_l1496_https_arxiv_org_abs_2506_03140/figures/008_Table_3.jpg]]
*Table 3: User Study. To demonstrate the importance of accurate camera parameters, we generated videos using parameter-based baselines, employing two sets of parameters: 1) ground truth (GT) and 2) those estimated by MegaSam, a state-of-the-art camera pose estimation model. Users are tasked with selecting the video whose camera movement more closely matches a reference video, and we report the resulting preference rates*

![[assets/figures/papers/paper_list_l1496_https_arxiv_org_abs_2506_03140/figures/009_Table_5.jpg]]
*Table 5: Ablation Study on Condition Injection Mechanism*

![[assets/figures/papers/paper_list_l1496_https_arxiv_org_abs_2506_03140/figures/011_Table_6.jpg]]
*Table 6: Ablation Study on Training Strategy*

## 定位与知识库关联

### 1. 核心创新与基线关系

**CamCloneMaster** 的核心突破在于将相机控制的条件从“显式参数序列”迁移至“参考视频的潜在表示”，从根本上绕开了参数估计误差对控制精度的制约。现有方法可依条件类型与注入机制分为三个谱系：

- **参数驱动 + 控制模块注入**：**CameraCtrl**（He et al., 2025）与 **CamI2V**（Zheng et al., 2024）依赖 Plücker 嵌入等显式相机参数，通过额外控制模块（如通道拼接或注意力引导）将参数注入生成过程。这类方法的主要瓶颈在于用户难以手动构建复杂轨迹，且从真实视频估计参数时，即使使用 MegaSaM 等 SOTA 估计器，仍会引入不可忽略的误差——Table 3 的用户研究表明，使用 MegaSaM 估计参数相比真实参数（GT），用户偏好率显著下降，直接证实了参数精度对生成质量的关键影响。

- **参数驱动 + V2V 重生成**：**DaS**（Gu et al., 2025）、**ReCamMaster**（Bai et al., 2025）与 **TrajectoryCrafter**（Yu et al., 2025）同样依赖显式相机参数，但面向视频到视频的重生成场景。CamCloneMaster 在 RealEstate10K 测试集上以 Rot Err 1.36 优于 ReCamMaster 的 1.53，FVD 678.06 优于 ReCamMaster 的 718.69（Table 1），表明即使与参数驱动的 V2V 方法相比，无参数的克隆策略在相机精度和动态质量上仍具竞争力。

- **参考视频 + 训练免调**：**MotionClone**（Ling et al., 2024）是唯一同样采用“从参考视频克隆运动”思路的方法，但其通过注意力图逆推实现运动迁移，需要测试时微调且相机控制精度有限——在 RealEstate10K 上 FVD 高达 1355.55，远高于 CamCloneMaster 的 993.06（Table 1）。CamCloneMaster 通过帧维度令牌拼接将条件注入统一到 DiT 的前向推理中，无需测试时微调即可直接克隆相机运动，在便捷性和精度上均形成代际优势。

### 2. 方法谱系中的位置：因果调控变量视角

从“因果调控变量”的角度审视，CamCloneMaster 对三个关键设计槽位进行了系统性替换：

| 设计槽位 | 基线方案 | CamCloneMaster 方案 | 证据锚点 |
|---------|---------|-------------------|---------|
| 条件输入类型 | 显式相机参数序列或注意力图 | 参考视频的 3D VAE 潜变量 | replicate camera movements from reference videos without requiring camera parameters |
| 条件注入机制 | 通道拼接、注意力引导或额外模块 | 帧维度令牌拼接（Frame Concat） | directly concatenating condition tokens with noisy video tokens in a unified input sequence |
| 微调策略 | 完整微调或固定基模型 | 仅微调 3D 时空注意力层 | we selectively finetune only the 3D spatiotemporal attention layers |

这些替换并非孤立的设计选择，而是围绕一个核心洞察展开：**DiT 的 3D 时空注意力层本身具备学习相机运动表征的能力，只需将参考视频的潜变量与噪声潜变量沿帧维度拼接，即可隐式地传递运动信息，无需显式参数化或额外控制模块。** 消融实验（Table 5）证实，帧维度拼接方案在 FVD（993.06）、Rot Err（1.49）和 Trans Err（2.37）上全面优于通道拼接和仅时域层注入等替代方案。Table 6 进一步表明，仅微调 3D 时空注意力层（Rot Err 1.49）相比微调整个 DiT Block（Rot Err 3.64）能获得更优的相机克隆精度，验证了“运动表征主要驻留在时空注意力层”的假设。

### 3. 适用边界与局限

CamCloneMaster 的适用边界由其设计选择直接决定：

- **计算开销**：帧维度令牌拼接将条件令牌直接追加到输入序列，导致序列长度显著增加。论文明确指出这一设计“增加了计算开销，限制生成效率”。这是令牌拼接方案的固有代价——条件视频的每一帧都作为独立令牌参与全序列的时空注意力计算，复杂度随帧数线性增长。

- **相机轨迹复杂度**：训练依赖 **Camera Clone Dataset**（基于 Unreal Engine 5 渲染的 391K 视频、1,155K 三元组），轨迹分布由 3D 场景中预设的多相机路径决定。对于超出该分布的长距离、高动态或非刚体相机运动，模型的泛化能力尚未得到验证，需要手动检查。

- **长视频与高分辨率扩展**：当前架构的令牌拼接策略在帧数或分辨率增加时面临二次复杂度增长，论文将“扩展到更长视频或更高分辨率”列为开放问题。

### 4. 开放问题与后续方向

从方法谱系的演进逻辑出发，以下方向值得关注：

1. **稀疏注意力或潜变量丢弃策略**：针对令牌拼接的计算瓶颈，探索在时空注意力中引入稀疏模式，或在推理时动态丢弃冗余的条件令牌，是降低部署成本的自然延伸。

2. **更复杂的相机轨迹与动态场景**：当前数据集以静态背景为主，如何将方法推广到包含显著前景运动、遮挡或非朗伯表面的动态场景，需要构建更具挑战性的训练数据或设计运动-外观解耦机制。

3. **与参数化方法的融合**：CamCloneMaster 的无参数克隆与参数驱动方法并非互斥——将参考视频的隐式运动表征与显式参数（如用户指定的相机路径编辑）结合，可能实现更精细的相机控制，这一方向尚未被探索。

4. **评估协议的标准化**：当前所有方法的相机精度指标均依赖 MegaSaM 估计参数，而估计误差本身可能混淆方法间的真实差异。建立基于真实相机参数（如合成数据中的 GT）的标准化基准，对于公平比较参数驱动与无参数方法至关重要。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation.pdf]]

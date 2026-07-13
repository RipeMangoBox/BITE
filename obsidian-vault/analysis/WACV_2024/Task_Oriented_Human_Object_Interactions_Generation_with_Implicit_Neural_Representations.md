---
title: Task-Oriented Human-Object Interactions Generation with Implicit Neural Representations
type: paper
paper_level: A
venue: WACV
year: 2024
pdf_ref: paperPDFs/WACV_2024/Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural_Representations.pdf
project_link: null
code_link: null
aliases:
- TOHOIGINR
tags:
- WACV_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用基于隐式神经表示（INR）的运动内插网络，将运动建模为时间坐标的连续函数，实现任意帧率和速度的生成。
primary_logic: 将完整物体操作动作生成视为运动内插问题：先估计任务驱动的物体最终位置，生成关键抓取帧，再利用超网络生成的INR连续内插中间运动，从而实现任意长度的连续动作合成。
claims:
- TOHO generates continuous motions parameterized only by the temporal coordinate, allowing for upsampling to arbitrary frames and velocity adjustments.
- Our method achieves ADE 0.113, Skating 0.247, PSKL-J (P,GT) 0.232 on AMASS/GRAB.
- The full model with contact and surface marker losses achieves best ADE 0.079, Skating 0.177, PSKL-J (P,GT) 0.219.
- AMASS/GRAB 上 ADE, Skating, PSKL-J (P,GT), PSKL-J (GT,P) = 0.113
---

# Task-Oriented Human-Object Interactions Generation with Implicit Neural Representations

> [!tip] 核心洞察
> 将完整物体操作动作生成视为运动内插问题：先估计任务驱动的物体最终位置，生成关键抓取帧，再利用超网络生成的INR连续内插中间运动，从而实现任意长度的连续动作合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于隐神经表示的任务导向人-物交互动作生成 |
| 英文题名 | Task-Oriented Human-Object Interactions Generation with Implicit Neural Representations |
| 会议/期刊 | WACV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TOHO |
| Dataset | AMASS/GRAB |

> [!tip] 效果简介
> - AMASS/GRAB 上，ADE, Skating, PSKL-J (P,GT), PSKL-J (GT,P) 0.113；ADE, Skating, PSKL-J (P,GT), PSKL-J (GT,P) 0.247；ADE, Skating, PSKL-J (P,GT), PSKL-J (GT,P) 0.232。

## 概要

### 问题瓶颈

生成完整的任务导向人-物交互动作序列面临三重挑战：现有方法要么只合成接近物体的动作（如 **GOAL**，Taheri et al., CVPR 2022），要么仅生成已知物体的短片段操作（如 **IMoS**，Ghosh et al., EUROGRAPHICS 2023），且生成的动作帧率固定，无法灵活调整速度与长度。核心瓶颈在于缺乏一个统一的框架，能够对未见过的物体生成从接近、抓取到操纵的连续完整序列。

### 核心思路

TOHO 将完整物体操作动作生成重新定义为**运动内插问题**：先估计任务驱动的物体最终位置，生成初始和最终位置处的关键抓取帧，再利用**基于隐式神经表示的运动内插网络**将运动建模为时间坐标的连续函数，实现任意帧率和速度的生成。这一范式转变使得动作序列不再受固定帧率的约束，而是成为可连续查询的时间参数化表示。

### 方法定位

TOHO 是一个四步流水线框架，输入为任务类型、物体初始位姿和人体初始姿态，输出完整的任务导向人-物交互动作序列。其关键创新在于将 INR 引入运动内插，替代传统自回归或固定帧率生成范式，同时通过闭合形式的物体运动估计保证手-物交互的物理一致性。在方法谱系上，TOHO 与 **SAGA**（Wu et al., ECCV 2022）等全身抓取生成方法、**NeMF**（He et al., NeurIPS 2022）等神经运动场方法形成互补——前者提供接近阶段的参考，后者验证了隐式表示在运动建模中的潜力，但 TOHO 是首个将两者统一并扩展到完整任务导向交互的工作。

### 主要结果

在 AMASS/GRAB 基准上，TOHO 在运动内插任务中取得 ADE 0.113、滑步比 0.247、PSKL-J (P,GT) 0.232 的性能。完整模型加入接触损失和表面标记损失后，指标进一步提升至 ADE 0.079、滑步比 0.177、PSKL-J (P,GT) 0.219。消融实验表明，物体参数采样器中引入人体形状信息可将物体位置估计误差从 0.073m 降至 0.048m，而物体运动估计中的旋转对齐机制将手-物接触比从 0.66 提升至 0.93，穿透深度从 0.013 降至 0.007。定性结果展示了 TOHO 对不同人体形状和未见物体的泛化能力，以及通过修改时间坐标实现动作变速的灵活性。



### 任务导向人-物交互动作生成的现实需求

数字人类在虚拟现实、机器人学习和具身AI中需要执行有意图的物体操作任务，如拿起杯子喝水、移动椅子坐下。这类动作天然包含两个阶段：**接近物体**（approaching）和**操作物体**（manipulation）。生成完整、连续、物理合理的任务导向人-物交互（Human-Object Interaction, HOI）动作序列，是实现可信数字代理的核心技术挑战。

### 现有方法的三个结构性缺口

**缺口一：动作片段化。** 现有方法只能覆盖任务的部分阶段。**GOAL**（Taheri et al., CVPR 2022）生成接近物体的抓取动作，但抓取后物体如何移动不在其建模范围内；**SAGA**（Wu et al., ECCV 2022）生成随机全身抓取动作，同样不处理物体随后的运动轨迹；**IMoS**（Ghosh et al., EUROGRAPHICS 2023）虽然生成全身物体操纵动作，但假设抓取已经建立，且仅输出短序列。没有任何方法能够端到端地生成从接近到操作完成的完整动作序列。

**缺口二：未知物体泛化能力缺失。** 大多数操纵动作生成方法依赖训练时见过的物体几何，当面对新物体时性能急剧退化。IMoS 等方法的物体表示与特定几何强绑定，无法迁移到未见物体。

**缺口三：动作时间表示僵化。** 现有方法（如 NeMF, He et al., NeurIPS 2022；Robust motion inbetweening, Harvey et al., TOG 2020）以固定帧率生成离散动作序列，无法灵活调整动作速度或输出任意帧率。在实际应用中，不同场景需要不同的动作节奏——快速拿起物体与缓慢递出物体需要非均匀的时间采样，固定帧率表示从根本上限制了这种灵活性。

### 核心洞察：将操作动作生成为运动内插问题

本文的核心洞察是：**完整的物体操作动作生成可以自然地形式化为运动内插（motion inbetweening）问题。** 给定任务意图，首先估计物体在操作完成后的最终位置，然后生成在初始位置抓取物体和最终位置抓取物体的两个关键姿态，最后连续地内插出两个关键帧之间的所有中间运动。这一视角将“生成完整操作序列”转化为“给定首尾关键帧，填充中间过渡”，使得问题结构清晰、可分解。

### 技术动机：隐式神经表示实现连续运动

为突破固定帧率的限制，本文引入**隐式神经表示（Implicit Neural Representations, INR）** 将人体运动建模为时间坐标的连续函数。INR 已在3D形状重建和新视角合成中展现出对连续信号的高质量拟合能力。将其应用于运动生成，意味着运动不再是离散的帧序列，而是定义在连续时间域 $[0,1]$ 上的函数 $f(t)$。这带来两个关键能力：一是**任意帧率上采样**——只需在时间轴上更密集地采样即可获得高帧率动作；二是**灵活变速**——通过非均匀采样时间坐标，自然实现加速、减速或节奏变化，无需重新训练模型。

综合以上动机，TOHO 旨在构建一个统一框架，首次同时解决完整动作生成、未知物体泛化和连续时间表示三个挑战。



## 核心方法与创新机理

TOHO 的核心创新在于将**完整的任务导向人-物交互动作生成**重新定义为**运动内插问题**，并通过**隐式神经表示**实现连续时间参数化，从而突破现有方法在动作完整性、物体泛化性和帧率灵活性三个维度的根本局限。

### 1. 问题范式的根本转换

现有方法各自只能解决交互动作的局部片段：**GOAL** (Taheri et al., CVPR 2022) 仅生成接近物体的抓取动作，缺乏后续操作；**SAGA** (Wu et al., ECCV 2022) 生成接近阶段的全身抓取，但帧率固定且物体本身不移动；**IMoS** (Ghosh et al., EUROGRAPHICS 2023) 虽能生成全身操作，但假设抓取已建立且仅输出短序列。三者均无法生成从接近、抓取到操作的**完整连续序列**，且都要求物体已知或帧率固定。

TOHO 将这一碎片化格局统一为“关键帧生成+中间帧填充”的范式：先估计任务驱动的物体最终位置，再生成抓取关键帧，最后通过运动内插网络填充完整动作。这一设计使得方法天然支持**未见过的物体**和**任意长度的连续动作**（Table 1, Section 3.1）。

### 2. 基于 INR 的连续运动生成

这是 TOHO 最关键的 **changed slot**：将运动生成从自回归或固定帧率范式转换为**连续时间坐标的函数映射**。

传统方法如 **NeMF** (He et al., NeurIPS 2022) 使用神经运动场但需要逐序列优化，无法实时生成；**Robust motion inbetweening** (Harvey et al., TOG 2020) 和 **Long-term human motion synthesis** (Wang et al., CVPR 2021) 虽能内插或合成长期运动，但本质仍是离散帧输出。

TOHO 的运动内插网络将 SMPL-X 姿态序列 $\hat{\theta}_{1:T}$ 和全局平移偏移 $\hat{t}_{1:T}^{\mathrm{off}}$ 编码为“运动图像” $M$，通过超网络生成的 INR 权重将运动建模为时间坐标 $\tau \in [0,1]$ 的连续函数（Section 3.4, Eq. 4）。这一设计带来两个独特能力：

- **任意帧率上采样**：只需在 $[0,1]$ 内密集采样 $\tau$ 即可获得高帧率动作，无需重新训练（Figure 4a-b）。
- **非线性变速**：通过对 $\tau$ 的非均匀采样实现同一动作的速度调控——例如在起始阶段稀疏采样实现快速抬升、末尾密集采样实现缓慢传递（Figure 4c-d），这是固定帧率方法无法做到的。

### 3. 闭合形式的实时物体运动估计

第二个 **changed slot** 是物体运动的计算方式。现有方法要么忽略物体运动，要么仅做线性插值，无法保证手-物接触的物理一致性。

TOHO 提出基于右手五指指尖和手掌标记的**闭合形式估计算法**（Section 3.5）：利用 Kabsch 算法求解当前帧手指偏移向量与首帧的最优旋转对齐 $R_n$，进而通过 $R_n$ 的转置和标记平均位置实时更新物体朝向和位置。该算法无需学习参数，计算成本极低，与 INR 运动生成解耦后可独立运行，且消融实验证实引入旋转对齐 $R_n$ 使手-物接触比从 0.66 提升至 0.93，穿透深度从 0.013 降至 0.007（Table 5）。

### 4. 创新的级联效应

上述三个创新并非孤立存在，而是形成因果链条：物体参数采样器提供任务驱动的目标位置 → 目标网络生成对应关键帧 → INR 内插网络填充连续动作 → 物体运动估计实时计算一致物体轨迹。这一级联使得 TOHO 成为首个能同时满足**完整序列、未见物体、连续时间、变速控制**四个条件的统一框架（Table 1）。

> **注意**：关于 INR 超网络的具体架构细节（如特征调制层数、隐空间维度）在提供的分析材料中未明确给出，需查阅原文 Section 3.4 确认。



TOHO 将完整的任务导向人-物交互动作生成建模为一个**运动内插（motion inbetweening）问题**，其核心假设是：给定任务意图、初始人体姿态与物体位姿，如果能合理估计物体的最终位置，并生成初始与最终两个关键抓取帧，那么中间的运动序列可以通过连续内插来补全。基于这一假设，整个 pipeline 由四个串行模块构成（Figure 2）：

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/003_Figure_2.jpg]]
*Figure 2: Overview of TOHO. We formulate the generation of object manipulation motions as a motion-infilling problem that consists of four steps. 1) With the shape parameters of the human and the task type, we estimate the object’s final position using our object parameters sampler. 2) The goal net then generates human poses grasping the object at its initial and final positions. 3) Our motion inbetweening model subsequently generates continuous motions to infill the missing frames between the keyframe human poses. 4) Finally, our object motion estimation algorithm outputs a stable and consistent object motion based on the human motion in real-time*

1. **物体参数采样器（Object Parameters Sampler）**：根据任务类型、人体形状参数和物体初始位姿，估计物体的最终位置偏移量。该模块是一个条件变分自编码器（cVAE），输出物体平移和旋转的偏移量，从而确定物体在任务完成时的目标位姿。

2. **目标网络（Goal Net）**：以物体初始位姿和估计的最终位姿为条件，生成人体在这两个位置抓取物体的关键帧姿态。该网络同时预测 SMPL-X 姿态参数、全局平移、头部朝向以及手部到物体的偏移向量，确保抓取姿态在空间上与物体对齐。

3. **运动内插网络（Motion Inbetweening Network）**：这是 TOHO 的核心创新模块。它基于隐式神经表示（INR），将人体运动建模为时间坐标 $t \in [0,1]$ 的连续函数。给定两个关键帧，该网络生成中间任意帧的人体姿态和平移偏移，从而实现：
   - **任意帧率上采样**：通过密集采样时间坐标即可获得高帧率序列；
   - **可变速度生成**：通过非均匀采样时间坐标（如稀疏采样获得加速效果，密集采样获得减速效果）来调整动作速度（Figure 4）。

4. **物体运动估计算法（Object Motion Estimation）**：这是一个闭合形式的实时算法。它利用人体右手五指指尖和掌心的表面标记点，通过 Kabsch 算法计算当前帧与第一帧之间手指偏移向量的最优旋转对齐 $R_n$，进而反推物体的旋转和平移。该方法无需额外网络推理，保证了物体运动与手部运动的空间一致性。

**输入输出规范**：系统的输入包括三部分——任务类型（独热编码）、物体形状及其初始平移和旋转、人体的初始姿态和形状参数。输出为完整的、连续的人-物交互动作序列，包含任意帧数的人体姿态序列和对应的物体运动轨迹。整个框架在 GRAB 数据集上训练和评估，支持未见过的物体形状和不同体型的人体。



TOHO 将完整的任务导向物体操作动作生成建模为**运动内插（motion inbetweening）**问题，整个框架由四个核心模块串联构成（Figure 2）：物体参数采样器、目标网络、运动内插网络和物体运动估计算法。以下逐一展开各模块的关键公式与变量含义。

### 物体参数采样器（Object Parameters Sampler）

该模块的任务是：给定任务意图、人体形状和物体的初始位姿，估计物体在操作完成后的最终位置。它采用条件变分自编码器（cVAE）结构。

**输入向量**（Eq. 1）：

$$X_s = [a_{\mathrm{one}}, \beta, t_o^{\mathrm{init}}, r_o^{\mathrm{init}}, t_o^{\mathrm{off}}, r_o^{\mathrm{off}}]$$

其中 $a_{\mathrm{one}}$ 为任务的独热编码，$\beta$ 为 SMPL‑X 人体形状参数，$t_o^{\mathrm{init}}$ 与 $r_o^{\mathrm{init}}$ 分别为物体的初始平移和旋转，$t_o^{\mathrm{off}}$ 与 $r_o^{\mathrm{off}}$ 为物体从初始到最终位置的平移和旋转偏移。cVAE 以 $a_{\mathrm{one}}$、$\beta$、$t_o^{\mathrm{init}}$、$r_o^{\mathrm{init}}$ 为条件，学习偏移量 $t_o^{\mathrm{off}}$ 和 $r_o^{\mathrm{off}}$ 的分布。

**训练损失**（Eq. 2）：

$$\mathcal{L}_s = \lambda_t \|\hat{t}_o^f - t_o^f\|_2 + \lambda_r \|\hat{r}_o^f - r_o^f\|_2 + \lambda_{KL} \mathcal{L}_{KL}$$

该损失由三部分加权求和：预测与真值的平移偏移 L2 损失、旋转偏移 L2 损失，以及 VAE 的 KL 散度正则项。采样器输出物体的最终位姿估计，为后续关键帧生成提供目标约束。

### 目标网络（Goal Net）

目标网络的作用是生成人体在物体初始位置和最终位置处的**关键抓取姿态**。其编码器接收多模态输入（Eq. 3）：

$$X = [\theta, t, \beta, v, d_{bo}, h, t_o, b_o, a]$$

各变量含义：$\theta$ 为 6D 连续姿态旋转向量（$\mathbb{R}^{55 \times 6}$），$t$ 为身体全局平移（$\mathbb{R}^3$），$\beta$ 为人体形状参数，$v$ 为 SMPL‑X 表面顶点，$d_{bo}$ 为身体到物体的偏移向量，$h$ 为头部朝向，$t_o$ 为物体平移，$b_o$ 为物体的基点点集（BPS）特征，$a$ 为任务标签。解码器从潜在编码中预测 SMPL‑X 参数 $\hat{\theta}$、$\hat{t}$、头部朝向 $\hat{h}$ 以及右手到物体的偏移向量 $\hat{d}_{r \to o} \in \mathbb{R}^{99 \times 3}$。

### 运动内插网络（Motion Inbetweening Network）

这是 TOHO 实现**连续时间参数化**的核心模块。基于隐式神经表示（INR），该网络将运动建模为时间坐标 $\tau$ 的连续函数，从而在任意帧率下生成两关键帧之间的中间运动。

**运动图像重建**（Eq. 4）：

$$M = [\hat{\theta}_{1:T}, \hat{t}_{1:T}^{\mathrm{off}}]$$

其中 $\hat{\theta}_{1:T}$ 为预测的姿态序列，$\hat{t}_{1:T}^{\mathrm{off}}$ 为预测的平移偏移序列。INR 由超网络（hypernetwork）根据关键帧信息生成权重，再通过时间坐标 $\tau$ 查询得到每一帧的运动参数。

**运动内插总损失**（Eq. 5）：

$$\mathcal{L}_M = \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_t \mathcal{L}_t + \lambda_v \mathcal{L}_v + \lambda_C \mathcal{L}_C$$

四项损失分别为：姿态重建损失 $\mathcal{L}_{\theta}$、平移损失 $\mathcal{L}_t$、表面标记损失 $\mathcal{L}_v$ 和脚-地面接触损失 $\mathcal{L}_C$。消融实验证实，加入接触损失和表面标记损失可将 ADE 从 0.113 降至 0.079，滑步比从 0.247 降至 0.177（Table 4）。

### 物体运动估计算法（Object Motion Estimation）

该模块以闭式解（closed‑form）方式从人手运动实时推断物体的刚体运动，无需额外训练。其核心是使用 Kabsch 算法对齐手指偏移向量。

**Kabsch 旋转对齐**（Section 3.5）：

$$R_n = \arg\min_R \frac{1}{2} \sum_{i=1}^5 \|o_1^{f_i} - R\, o_n^{f_i}\|_2$$

其中 $o_1^{f_i}$ 和 $o_n^{f_i}$ 分别表示第 1 帧和第 $n$ 帧中第 $i$ 个指尖相对于掌心的偏移向量（共 5 个指尖）。$R_n$ 是使两组向量最优对齐的旋转矩阵。

**物体方向更新**：

$$rot_n = R_n^T\, rot_1$$

物体在第 $n$ 帧的方向由初始方向 $rot_1$ 和对齐旋转的转置 $R_n^T$ 计算得到。

**物体平移更新**：

$$t_n^o = \frac{1}{6} \sum_{i=0}^5 v_n^{f_i} + R_n^T \left(t_1^o - \frac{1}{6} \sum_{i=0}^5 v_1^{f_i}\right)$$

其中 $v_n^{f_i}$ 为第 $n$ 帧第 $i$ 个手部标记（5 个指尖加 1 个掌心）的世界坐标。物体平移由当前手部标记的平均位置与逆旋转后的初始偏移共同确定。消融实验表明，引入旋转对齐 $R_n$ 使手-物接触比从 0.66 提升至 0.93，穿透深度从 0.013 降至 0.007（Table 5），验证了该闭式估计的有效性。

### 连续时间参数化的核心机制

TOHO 的连续运动生成能力源于 INR 将运动编码为时间坐标 $\tau \in [0, 1]$ 的连续函数。通过修改 $\tau$ 的采样方式即可实现变速效果（Figure 4）：均匀稀疏采样得到倍速动作，在接近 0 处稀疏、接近 1 处密集采样得到“快抬慢递”，反之则得到“慢抬快递”。这一机制使 TOHO 成为首个支持任意帧率上采样和灵活速度调控的任务导向人-物交互动作生成方法。

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/005_Figure_4.jpg]]
*Figure 4: Examples of motion velocity adjustment by modifying the temporal coordinate τ . a) A 64-frame generated result of normal speed. b) Speed up the sequence by uniformly sampling two times fewer values from τ ∈ [0, 1], which gives a result of doubled velocities. c) The human swiftly lifts the object and then slowly passes it, which is done by sampling sparsely near 0 and densely near 1. d) The human slowly lifts the object and swiftly passes it, which uses a reverse sampling scheme of c)*



## 实验与关键发现

### 问题设定与基线对比

TOHO 是首个统一框架，能够生成**完整的、连续的、意图驱动的**人-物操作动作序列，且可处理训练中未见过的物体。表1将 TOHO 与现有方法的设定进行了系统对比：**GOAL** (Taheri et al., CVPR 2022) 仅生成接近物体的抓取动作，不包含后续物体操作；**SAGA** (Wu et al., ECCV 2022) 生成随机全身抓取动作但受限于固定帧率且物体不发生移动；**IMoS** (Ghosh et al., EUROGRAPHICS 2023) 假设抓取已建立，仅生成已知物体的短序列操作；**NeMF** (He et al., NeurIPS 2022) 使用神经运动场但需要逐序列优化，无法实时生成。TOHO 的独特之处在于同时满足：任务驱动、完整序列（接近+操作）、连续时间参数化、未知物体泛化四项要求。

### 运动内插性能主结果

表2报告了在 AMASS/GRAB 数据集上的运动内插性能对比。TOHO 在仅预测姿态（使用真实轨迹）和同时预测姿态与轨迹两种设定下均取得最优结果。具体而言：

- **仅预测姿态**：TOHO 的 ADE 达到 **0.113**，滑步比 (Skating) 为 **0.247**，PSKL-J (P,GT) 为 **0.232**，PSKL-J (GT,P) 为 **0.218**。
- **同时预测姿态与轨迹**：TOHO 同样在所有指标上优于基线方法（具体数值需查看原表2第三行，分析中未提供完整对比数值，建议手动核实）。

对比的基线包括 **Robust motion inbetweening** (Harvey et al., TOG 2020) 和 **Long-term 3D human motion synthesis** (Wang et al., CVPR 2021)。TOHO 的优势来源于 INR 的连续时间参数化，使其能够生成任意帧率的平滑运动，而传统方法受限于固定帧率的离散表示。

### 人-物交互质量

表3评估了生成序列的交互物理合理性。TOHO 生成的完整动作序列在手-物接触率和穿透深度两项指标上与真实值（Ground Truth）接近。特别地，目标网络（Goal Net）生成的抓取姿态在接触质量上也表现良好。这表明 TOHO 不仅在运动学层面准确，在交互物理约束层面也保持了较高保真度。

### 消融实验

#### 运动内插模型消融

表4展示了运动内插模型的消融结果。完整模型（包含脚-地面接触损失 $\mathcal{L}_C$ 和表面标记损失 $\mathcal{L}_v$）取得最优性能：ADE **0.079**，滑步比 **0.177**，PSKL-J (P,GT) **0.219**。逐步移除这些损失项会导致性能退化，验证了物理约束损失对生成运动质量的关键作用。

#### 物体参数采样器消融

在物体参数采样器中去除人体形状信息 $\beta$ 后，预测的物体最终位置与真实值的平均距离从 **0.048m** 增加到 **0.073m**。这说明人体形状对推断任务驱动的物体目标位置具有重要影响——不同体型的人在执行相同任务时，物体放置位置存在系统性差异。

#### 物体运动估计算法消融

表5分析了物体运动估计算法的关键设计。引入基于 Kabsch 算法的旋转对齐 $R_n$ 后：
- 手-物接触比从 **0.66** 提升至 **0.93**
- 穿透深度从 **0.013** 降至 **0.007**

旋转对齐使物体方向与手部姿态保持一致性，显著减少了抓取滑脱和物体穿透伪影。该算法为闭合形式，可实时计算，无需额外优化。

### 运动多样性与速度控制

TOHO 通过修改时间坐标 $\tau$ 的采样策略实现对生成动作的速度调控（图4）：
- **均匀稀疏采样**：生成双倍速度的快速动作
- **非均匀采样**：实现“先快后慢”或“先慢后快”的变速动作

这种能力源于 INR 将运动建模为时间坐标的连续函数 $M(\tau)$，而非固定帧的离散序列。在运动多样性方面，物体平移偏移量的平均 L2 成对距离（APD）为 **0.19m**，完整生成动作的 APD 为 **0.34**，表明 TOHO 能够为相同任务生成多样化的运动结果。

### 失败模式与局限性

尽管 TOHO 在多个指标上表现优异，仍存在以下局限：
1. **物理正确性未完全保证**：当前框架未显式建模接触力、惯性和碰撞响应，生成的运动可能在极端情况下违反物理规律。
2. **场景复杂性受限**：实验仅在 GRAB 数据集上进行，未涉及包含遮挡的复杂 3D 场景。
3. **任务与物体多样性**：评估受限于 GRAB 数据集的动作类型和物体种类，向更广泛的任务和物体类别的泛化能力有待验证。

### 关键图表总结

| 图表 | 核心结论 |
|------|----------|
| 表1 | TOHO 是唯一同时支持完整序列、连续时间、未知物体、任务驱动的统一框架 |
| 表2 | 运动内插性能全面优于基线，ADE 达 0.113 |
| 表3 | 生成序列的接触率和穿透深度接近真实值 |
| 表4 | 接触损失和表面标记损失对运动质量至关重要，完整模型 ADE 达 0.079 |
| 表5 | Kabsch 旋转对齐将接触比从 0.66 提升至 0.93，穿透深度减半 |
| 图4 | 通过修改 $\tau$ 采样实现任意速度调控，无需重新训练 |

### 补充图表

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/002_Table_1.jpg]]
*Table 1: Overview of our problem setting compared with previous methods. Our method is the only unified framework that generates complete and continuous intent-driven human-object manipulation motions with unseen objects*

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/006_Table_2.jpg]]
*Table 2: Comparisons of motion-infilling performance. Second row shows results of pose prediction using ground truth trajectories and third row shows results of prediction of both the poses and trajectories. Boldface represents best results*

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/007_Table_3.jpg]]
*Table 3: Comparisons of our generated human-object interaction sequences to the ground truth. We report the results of the entire motion, and of the grasping poses generated by our pose predictor*

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/008_Table_4.jpg]]
*Table 4: Ablation study of our motion inbetweening model*

![[assets/figures/papers/paper_list_l1812_Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural/figures/009_Table_5.jpg]]
*Table 5: Ablation study of our object motion estimation algorithm*



## 定位与知识库关联

### 1 与现有工作的关系

TOHO 的核心贡献在于将**任务导向的完整物体操作动作生成**重新定义为**运动内插问题**，并通过隐式神经表示（INR）实现连续时间参数化。这一设计使其在问题设定上填补了现有方法之间的空白。

从**接近-抓取**这一子任务看，**GOAL**（Taheri et al., CVPR 2022）和 **SAGA**（Wu et al., ECCV 2022）分别能生成接近物体的抓取动作或随机全身抓取动作，但二者均不生成后续的物体移动。TOHO 继承了目标导向抓取的思想，但将生成范围从“抓取瞬间”扩展到了“完整操作序列”。

从**物体操作**这一子任务看，**IMoS**（Ghosh et al., EUROGRAPHICS 2023）能生成全身操作动作，但它假设抓取已经建立，且仅生成短序列。TOHO 则从抓取建立之前开始，生成包含接近、抓取、操作的完整序列，且序列长度可变。

从**运动生成的技术范式**看，TOHO 的 INR 内插网络与两类方法形成对比。一类是自回归或固定帧率模型，如 **NeMF**（He et al., NeurIPS 2022）需要逐序列优化，无法实时生成。另一类是传统运动内插方法，如 **Robust motion inbetweening**（Harvey et al., TOG 2020），虽然也做帧间填充，但不具备处理未知物体和任务意图的能力。TOHO 通过超网络生成 INR 权重，将运动建模为时间坐标 $t$ 的连续函数，从而在单次前向传播中实现任意帧率的生成，且可通过修改时间坐标向量实现变速——这是固定帧率方法无法做到的。

Table 1 将上述差异系统化：TOHO 是唯一同时满足“完整序列生成”“连续运动”“任务驱动”“可处理未知物体”四个条件的方法。

### 2 适用边界

**任务类型边界**：TOHO 的物体参数采样器以任务独热编码 $a_{\mathrm{one}}$ 为条件，因此仅能处理训练集中出现的任务类别。当前实验基于 GRAB 数据集，覆盖了若干日常操作任务，但未在更广泛的任务分布上验证。

**物体泛化边界**：方法声称可处理未见过的物体，但这一泛化依赖于物体形状的 BPS 编码和手指轨迹的几何对齐。对于拓扑结构复杂（如有孔洞、可变形）或尺度极端的物体，Kabsch 算法基于五点手指偏移向量的刚体假设可能失效。

**物理正确性边界**：消融实验表明，脚-地面接触损失 $\mathcal{L}_C$ 和表面标记损失 $\mathcal{L}_v$ 改善了滑步和运动精度（Table 4），但 TOHO 目前不建模接触力、摩擦、碰撞响应等物理约束。这意味着生成的动作在运动学上合理，但在动力学上未必成立。

**场景复杂度边界**：当前框架未考虑环境遮挡。在真实 3D 场景中，物体最终位置可能被家具或其他障碍物阻挡，物体参数采样器缺乏对场景几何的感知能力。

### 3 局限与开放问题

**已知局限**：
1. **遮挡场景未验证**：方法假设物体初始位置可见且可自由放置，未在包含遮挡的复杂 3D 场景中测试。
2. **物理约束缺失**：生成动作的力接触和碰撞响应尚未保证，这限制了在机器人仿真和物理推理场景中的直接应用。
3. **评估范围受限**：定量评估仅基于 GRAB 数据集的动作类型和物体种类，跨数据集泛化性能未知。

**开放问题**：
1. **场景感知的交互生成**：如何将场景几何（如桌面、墙壁、障碍物）作为条件引入，使物体参数采样器能预测物理可行的最终位置？
2. **物理集成的生成**：能否在 INR 框架中嵌入可微物理模拟器，将接触力、惯量等作为额外的损失项或约束，使生成的动作在动力学上一致？
3. **多物体与双手协作**：当前框架假设单手操作单个刚体。扩展到多物体交互或双手协作任务，需要重新设计物体运动估计算法（当前依赖单手五指标记的刚体对齐）和任务编码方式。
4. **长序列稳定性**：虽然 INR 理论上可生成任意长度序列，但超网络生成的 INR 权重是否会在长时间跨度上累积漂移，尚未有系统分析。

**证据强度说明**：上述局限和开放问题主要来自论文自身的讨论（Section 5），部分推断（如对复杂拓扑物体的泛化风险）基于对 Kabsch 算法假设的分析，属于合理推演而非实验验证，需后续工作确认。



## 原文 PDF

![[paperPDFs/WACV_2024/Task_Oriented_Human_Object_Interactions_Generation_with_Implicit_Neural_Representations.pdf]]

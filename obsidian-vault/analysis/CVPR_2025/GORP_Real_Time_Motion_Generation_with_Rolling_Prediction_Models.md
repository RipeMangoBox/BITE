---
title: "From Sparse Signal to Smooth Motion: Real-Time Motion Generation with Rolling Prediction Models"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models.pdf
project_link: https://barquerogerman.github.io/RPM/
code_link: null
aliases:
- RPMR
- FSSSMRTMGRPM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 滚动预测机制与预测一致性锚定函数（PCAF）相结合，通过逐步细化未来姿态预测并将修正量限制在不确定性范围内，实现了平滑度与反应灵敏度的可控权衡。
primary_logic: 将在线运动生成重新表述为对未来姿态序列的渐进式细化过程，以过往预测作为先验，利用不确定性调度控制新信息的注入强度，从而在追踪信号丢失和恢复时始终保持运动连续性。
claims:
- PCAF 使合成到追踪模式的过渡平滑度（AUJ_S-T）降低 11 倍以上，并消除了 abrupt snaps。
- 在 A-P1 的手部追踪设置下，RPM-Reactive 的 AUJ_S-T 为 69.02，而最强基准方法 HMD-Poser 为 1236.47，平滑度提升超过 17 倍。
- 仅含 free-running 而无 PCAF 时，AUJ_S-T 高达 799.03，过渡极不平滑；加上 PCAF 后降至 69.02，显示出 PCAF 的关键作用。
- 在真实 GORP 数据集上，RPM 是唯一能够在长期信号丢失后仍保持稳定误差且不产生突变的方法，且手腕误差保持与全身误差量级相当。
---

# From Sparse Signal to Smooth Motion: Real-Time Motion Generation with Rolling Prediction Models

> [!tip] 核心洞察
> 将在线运动生成重新表述为对未来姿态序列的渐进式细化过程，以过往预测作为先验，利用不确定性调度控制新信息的注入强度，从而在追踪信号丢失和恢复时始终保持运动连续性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从稀疏信号到平滑运动：基于滚动预测模型的实时运动生成 |
| 英文题名 | From Sparse Signal to Smooth Motion: Real-Time Motion Generation with Rolling Prediction Models |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://barquerogerman.github.io/RPM/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Rolling Prediction Model (RPM) |
| Dataset | A-P1 (AMASS intra-dataset, 60 FPS) – Hand Tracking scenario, A-P1 (AMASS intra-dataset) – Motion Controllers scenario, A-P2 (AMASS cross-dataset, 30 FPS) – Hand Tracking scenario, GORP |

> [!tip] 效果简介
> - A-P1 (AMASS intra-dataset, 60 FPS) – Hand Tracking scenario 上，AUJ_S-T (Area Under Jerk, synthesis-to-tracking transition smoothness) 69.02 (RPM-Reactive) / 50.23 (RPM-Smooth) vs 1236.47 (HMD-Poser, best among baselines) (Reduced by ~17.9x (Reactive) / ~24.6x (Smooth) compared to HMD-Poser)。
> - A-P1 (AMASS intra-dataset) – Motion Controllers scenario 上，Jitter (10² m/s³, lower is smoother) 4.21 (RPM-Reactive) / 4.23 (RPM-Smooth) vs 5.96 (HMD-Poser) (Reduced by ~29%)。
> - A-P2 (AMASS cross-dataset, 30 FPS) – Hand Tracking scenario 上，AUJ_S-T 32.81 (RPM-Reactive) / 11.93 (RPM-Smooth) vs 174.80 (HMD-Poser) (Reduced by ~5.3x (Reactive) / ~14.7x (Smooth))。

## 概要

### 问题瓶颈

扩展现实（XR）应用中的实时全身运动生成面临一个关键瓶颈：**追踪信号的时间稀疏性与间歇性丢失**。在手部追踪模式下，当用户手部离开头显摄像头视场时，追踪信号完全丢失，系统只能依赖运动合成（synthesis）生成动作；一旦追踪恢复，现有方法会立即将生成姿态强行拉回追踪位置，产生剧烈的**突变（abrupt snaps）**，严重破坏运动真实感与沉浸体验。即便在控制器模式下信号始终可用，现有方法生成的在线运动仍存在明显的抖动（jitter）问题。

### 核心思路

本文提出的 **Rolling Prediction Model（RPM）** 将在线运动生成重新表述为对未来姿态序列的**渐进式滚动细化过程**。其核心创新在于：

- **滚动预测机制**：网络在每个时间步预测未来 $W$ 帧的姿态序列，而非仅生成当前帧。随着时间推进和新追踪信号的到达，模型逐步细化先前的预测。
- **预测一致性锚定函数（PCAF）**：通过公式 $\mathcal{P}_t = \mathcal{P}_{t-1} + U \cdot \tanh(f_{\theta} - \mathcal{P}_{t-1})$ 将当前预测锚定在上一时刻的预测之上，利用不确定性 $U$ 控制新信息的注入强度。这使得追踪丢失期间的运动合成与追踪恢复时的信号跟随之间实现**平滑过渡**。
- **自由运行训练（free-running）**：在训练时先让网络使用自身预测运行一段，使其学会从自身错误中恢复，增强对追踪输入与生成运动之间错位的鲁棒性。

RPM 的核心洞察在于：**以过往预测作为先验，通过不确定性调度控制修正幅度，从而在信号丢失和恢复时始终保持运动连续性**。

### 方法定位

RPM 属于**确定性自回归在线运动生成**范式，与现有方法的关键差异体现在以下维度：

| 设计维度 | 现有方法 | RPM |
|---------|---------|-----|
| 预测目标 | 直接生成当前时刻姿态 | 预测未来 $W$ 帧，滚动细化 |
| 输出约束 | 距离损失直接监督 | PCAF 将修正限制在不确定性范围内 |
| 训练策略 | 仅教师强制（teacher forcing） | 引入自由运行阶段 |
| 时间步处理 | 所有时间步同等对待 | 余弦不确定性调度，远未来修正权重更大 |

与 **AvatarPoser**、**AGRoL**（扩散模型）、**EgoPoser**、**SAGE**、**AvatarJLM** 及 **HMD-Poser**（RNN 基线）等方法相比，RPM 是首个将运动生成显式建模为滚动预测渐进细化过程的框架。

### 主要结果

**合成数据基准（A-P1, 60 FPS）**：在手部追踪场景下，RPM-Reactive 的合成到追踪过渡平滑度指标 AUJ_S-T 为 **69.02**，而最强基线 HMD-Poser 高达 **1236.47**——RPM 将突变降低了 **约 17.9 倍**；RPM-Smooth 进一步降至 50.23（约 24.6 倍）。在控制器场景下，RPM 的抖动指标（Jitter）为 4.21，比 HMD-Poser 的 5.96 降低约 29%。

**真实数据（GORP 数据集）**：RPM 是唯一在长期信号丢失后仍保持稳定误差且不产生突变的方法，手腕误差保持在全身误差量级。在控制器模式下，RPM 在保持竞争性精度的同时生成显著更平滑的运动。

**消融实验**：移除 PCAF 仅保留自由运行，AUJ_S-T 从 69.02 飙升至 799.03；仅用 PCAF 无自由运行则精度退化（MPJPE 10.59）。两者协同才能同时获得精度与平滑度。传统 1€ 低通滤波器无法匹配 RPM 的平滑水平——基线方法要达到 RPM 的合成-追踪平滑度，需牺牲超过 50% 的准确度。

### 局限与展望

RPM 仍存在脚部滑动问题，尤其在地面原地转动时；其确定性预测范式在长时间信号丢失时可能趋于平均姿态；当前仅利用头部和手腕信号，未融合身体其他部位的 IMU 信息。未来方向包括：引入随机预测以保持动作多样性、显式脚部接触约束、自适应不确定性调度，以及融合多模态传感器数据。

### 扩展现实中的全身运动生成

扩展现实（XR）设备，如 Meta Quest 3 等商用头显，仅能提供稀疏的追踪信号——通常只包含头部和手腕的 6-DOF 位置与旋转。然而，要在虚拟环境中驱动逼真的全身化身，必须从这些稀疏输入中实时重建完整的身体姿态序列。这一任务面临双重挑战：既要保证生成动作的物理合理性，又要维持对用户输入的灵敏响应。

当前主流的在线运动生成方法（如 **AvatarPoser**、**AGRoL**、**EgoPoser**、**SAGE**、**AvatarJLM** 以及基于 RNN 的 **HMD-Poser**）大多采用“输入-输出”的直接映射范式：在每一时刻，网络根据当前和过去的追踪信号直接生成当前帧的全身姿态。这种设计在追踪信号连续且稳定的理想条件下表现尚可，但无法应对 XR 实际部署中的关键难题。

### 核心瓶颈：稀疏信号下的平滑性危机

实际 XR 场景中存在两类典型的信号退化，构成了现有方法的系统性瓶颈：

**手部追踪信号的间歇性丢失。** 在基于手部追踪（Hand Tracking）的交互模式下，头显摄像头对手部的可见性频繁中断——当用户将手置于背后、快速挥动或双手交叠时，追踪信号会完全丢失，持续时间从数百毫秒到数秒不等。此时，模型必须切换到“合成模式”（synthesis mode），仅凭历史运动上下文来预测合理的未来姿态。当追踪恢复时，模型又需从合成姿态跳变回与追踪信号对齐的姿态。现有方法在这两种模式切换时会产生剧烈的加速度突变（jerk），表现为化身动作的“瞬移”或“抽搐”，严重破坏沉浸感。

**运动控制器信号的固有噪声。** 即使在使用手柄控制器（Motion Controllers）的场景中，追踪信号始终可用，但用户手持方式导致的非刚性偏移、头显 IMU 的漂移等因素仍会引入高频噪声。现有方法直接拟合这些噪声信号，导致生成的动作出现肉眼可见的抖动（jitter）。

量化证据揭示了问题的严重性。在 A-P1 基准测试的手部追踪场景中，当前最强基线方法 **HMD-Poser** 的合成-追踪过渡平滑度指标 AUJ_S-T 高达 1236.47，表明追踪恢复瞬间存在极端的加速度跳变（Table 1）。这一数值意味着，现有方法在信号恢复时几乎无法提供任何有意义的过渡平滑机制。

### 根本原因：缺乏对未来预测的渐进式细化

上述问题的根源在于现有方法的生成范式存在结构性缺陷。传统方法将每一帧的生成视为独立事件，网络输出直接作为最终姿态，缺乏对“预测不确定性”的建模和对“运动连续性”的显式约束。当追踪信号丢失时，网络被迫进行开环预测，缺乏从自身错误中恢复的能力；当信号恢复时，新旧信息之间没有缓冲机制，导致姿态硬切换。

本文的核心洞察是：**在线运动生成本质上是一个对未来姿态序列的渐进式细化过程**。与其在每一时刻输出一个“最终答案”，不如让网络持续预测未来一段时间的姿态轨迹，并在新信息到来时逐步修正先前的预测。这一视角转换使得平滑过渡不再是后处理滤波的补救措施，而是生成过程本身的内在属性。

## 核心方法与创新机理

RPM 的核心创新在于将在线运动生成重新定义为**对未来姿态序列的渐进式细化过程**。与现有方法直接生成当前时刻姿态不同，RPM 在每个时间步预测未来 $W$ 个姿态，并通过滚动机制逐步修正——新一帧追踪信号到达时，网络基于过往预测作为先验，仅对预测序列进行增量更新。这一范式转变由三个相互耦合的 changed slots 支撑。

### 从即时生成到滚动预测

现有方法（AvatarPoser、AGRoL、EgoPoser、HMD-Poser 等）将运动生成建模为单步映射：给定追踪输入，直接输出当前帧姿态。当手部追踪信号因遮挡而丢失时，这些方法被迫在合成模式（free-running）下运行；一旦信号恢复，网络会突然“跳回”追踪姿态，产生剧烈突变。**Table 1** 显示，在 A-P1 手部追踪场景下，最强基线 HMD-Poser 的合成到追踪过渡平滑度指标 AUJ_S-T 高达 1236.47。

RPM 将预测目标从“当前姿态”改为“未来 $W$ 个姿态的序列”（**Section 3.1, Eq. 1**）：

$$f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) = \{\hat{\mathbf{x}}_t, \hat{\mathbf{x}}_{t+1}, \ldots, \hat{\mathbf{x}}_{t+W}\}$$

其中 $\mathcal{X}_t$ 为过去 $M$ 帧的生成运动上下文，$\mathcal{C}_t$ 为过去与当前的追踪输入。这一改变的意义在于：网络不再需要在新信息到达时“推翻”上一帧的输出，而是在已有预测的基础上进行细化。**Figure 5** 的轨迹可视化直观展示了这一滚动细化过程——品红色点表示未来预测序列，随新观测到达逐步收敛到真实轨迹。

### PCAF：预测一致性锚定函数

仅有滚动预测并不足以保证平滑过渡。RPM 的关键设计是 **Prediction Consistency Anchor Function (PCAF)**，它将网络原始输出重新参数化为受控修正（**Section 3.1, Eq. 2**）：

$$\mathcal{P}_t = \mathcal{P}_{t-1} + U \cdot \tanh(f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) - \mathcal{P}_{t-1})$$

其中 $\mathcal{P}_{t-1}$ 为上一时刻的预测序列（经时间对齐），$U$ 为不确定性标量，$\tanh$ 将网络修正量限制在 $[-1, 1]$ 范围内。这一公式的因果机制是：**新信息的注入强度由不确定性 $U$ 控制**——当追踪信号可靠时，$U$ 较小，修正量受限，运动保持平滑；当信号恢复时，$U$ 增大，允许更强的修正以重新锚定到追踪姿态。

消融实验（**Table 3**）提供了决定性证据：移除 PCAF 但保留 free-running 训练时，AUJ_S-T 从 69.02 飙升至 799.03（恶化超过 11 倍），过渡中出现明显的 abrupt snaps。仅使用 PCAF 而无 free-running 训练时，模型精度退化（MPJPE 10.59）。两者结合才能同时获得精度与平滑度。

### 不确定性调度：平滑度与响应性的可控权衡

PCAF 中的不确定性 $U$ 并非固定值，而是沿预测窗口按余弦函数调度（**Appendix E, Eq. B**）：

$$f_{\mathrm{cos}}(\tau) = 1 - \cos\Bigl(\frac{\tau + 1}{W} \cdot \frac{\pi}{2}\Bigr)$$

其中 $\tau$ 表示预测的未来距离（$\tau=0$ 为当前帧，$\tau=W-1$ 为最远帧）。这一设计的直觉是：近期预测应更稳定（低不确定性），远期预测允许更大的修正空间。**Table A (Suppl.)** 的消融表明，余弦不确定性在 AUJ_T-S 与 AUJ_S-T 上均优于余弦平方和线性函数。

预测长度 $W$ 进一步提供了应用层面的灵活性。**Figure 4** 显示，$W \approx 8$ 帧（133ms）时精度最优，$W \approx 15$ 帧（250ms）时平滑度最优。RPM-Reactive（$W=10$）与 RPM-Smooth（$W=20$）两个变体分别对应不同的权衡点：前者 AUJ_S-T 为 69.02，后者进一步降至 50.23（**Table 1**），均远优于 HMD-Poser 的 1236.47。

### Free-Running 训练：从自身错误中学习

传统方法仅使用真实历史进行教师强制（teacher forcing）训练，导致模型在推理时遇到自身生成的运动上下文时产生分布偏移。RPM 在每次训练迭代的开头插入一段 free-running 阶段（**Section 3.2, Algorithm 1**），让网络使用自身预测填充运动上下文，再计算损失。损失仅应用于 free-running 之后的预测窗口，且不沿时间反向传播（以节省显存）。

**Figure C (Suppl.)** 显示，free-running 长度超过 50 帧后精度和平滑度持续提升，在 90 帧时达到最佳过渡平滑度。这一结果表明，让模型学会从自身错误中恢复是应对追踪信号丢失场景的关键。

### 与后处理滤波的本质区别

一个自然的问题是：能否在现有基线方法上叠加低通滤波（如 1€ filter）来达到类似的平滑效果？**Table C (Suppl.)** 和 **Figure E (Suppl.)** 给出了明确答案：要使基线方法的合成到追踪平滑度达到 RPM 水平，其准确度需牺牲超过 50%。这是因为后处理滤波无法区分“应保留的信号细节”与“应平滑的突变”，而 PCAF 通过不确定性调度实现了对修正量的语义级控制。

RPM 将在线运动生成重新表述为一个**滚动预测与渐进细化**的过程。其核心流水线由四个模块串联构成，在每一时间步完成从稀疏追踪信号到平滑全身姿态的映射。

### 输入与输出定义

在时刻 $t$，系统接收两类输入：
- **运动上下文** $\mathcal{X}_t$：过去 $M$ 帧已生成的自身运动序列，作为显式的运动状态记忆。
- **追踪输入上下文** $\mathcal{C}_t$：当前及过去 $I$ 帧的稀疏追踪信号（头部与手腕的 6-DOF 位姿）。

网络 $f_\theta$ 的输出并非当前时刻的单一姿态，而是**未来 $W$ 帧的预测序列**：

$$f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) = \{\hat{\mathbf{x}}_t, \hat{\mathbf{x}}_{t+1}, \ldots, \hat{\mathbf{x}}_{t+W}\}$$

这一设计将瞬时生成转化为对未来的“草稿”预测，为后续的渐进细化提供操作空间。

### 流水线模块

**① Motion Context Encoder**  
将过去 $M$ 帧的自生成运动 $\mathcal{X}_t$ 编码为上下文特征，为网络提供连贯的运动状态表示，使预测不单纯依赖外部信号。

**② Tracking Input Encoder**  
编码当前及过去的追踪输入 $\mathcal{C}_t$，并通过**交叉注意力**机制与运动上下文特征交互。这一设计使网络能够感知追踪信号与自身运动状态之间的对齐关系。

**③ Transformer Encoder**  
采用四层 Transformer 编码器对融合后的序列进行时序建模，输出未来 $W$ 帧的**未修正预测**。该预测在追踪信号丢失或突变时可能包含高频抖动。

**④ PCAF Module（预测一致性锚定函数）**  
这是 RPM 实现平滑过渡的核心机制。它将上一时刻的滚动预测 $\mathcal{P}_{t-1}$ 作为先验，对网络原始输出进行约束性修正：

$$\mathcal{P}_t = \mathcal{P}_{t-1} + U \cdot \tanh(f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) - \mathcal{P}_{t-1})$$

其中 $U$ 为不确定性调度函数，随预测距离 $\tau$ 增大而单调递增。双曲正切 $\tanh$ 将修正量限制在 $[-1, 1]$ 范围内，再乘以 $U$ 实现**距离感知的修正强度控制**：对近期帧允许较大修正以保持响应性，对远期帧则限制修正幅度以维持运动连续性。

### 训练时的 Free-Running 机制

标准训练中网络仅见过真实历史，部署时却依赖自身生成的运动上下文，这种“曝光偏差”会导致误差累积。RPM 在每次训练迭代的**开头插入自由运行阶段**（free-running）：先让网络以自身预测填充上下文若干帧，再计算损失。损失仅施加在自由运行结束后的预测窗口上，且**不沿自由运行过程进行时间反向传播**以节省显存。这一策略迫使网络学会从自身的预测误差中恢复，使运动上下文编码器对生成运动与追踪输入之间的错位具有鲁棒性。

### 数据流总览

```
追踪输入 C_t ──→ Tracking Input Encoder ──┐
                                          ├──→ Transformer Encoder ──→ 原始预测
运动上下文 X_t ──→ Motion Context Encoder ──┘                              │
                                                                          ▼
                                          PCAF Module ←── 上一时刻预测 P_{t-1}
                                              │
                                              ▼
                                         当前滚动预测 P_t ──→ 取首帧作为输出姿态
```

每一时间步取 $\mathcal{P}_t$ 的首帧作为当前输出姿态，同时将 $\mathcal{P}_t$ 整体传递至下一时刻作为先验。这种**滚动窗口**机制使得每一帧姿态在其生命周期内被多次预测和修正——从远期的粗糙草稿逐步细化为近期的精确输出，从根本上保证了追踪信号恢复时不会产生突变式跳变。

### 问题形式化

RPM 将在线运动生成定义为一个滚动预测问题。给定到当前时刻 $t$ 为止的追踪输入序列 $\mathcal{C}_t = \{\mathbf{c}_{t-I}, \ldots, \mathbf{c}_t\}$ 和过去 $M$ 帧已生成的运动上下文 $\mathcal{X}_t = \{\mathbf{x}_{t-M}, \ldots, \mathbf{x}_{t-1}\}$，网络 $f_\theta$ 预测未来 $W$ 帧的姿态序列：

$$f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) = \{\hat{\mathbf{x}}_t, \hat{\mathbf{x}}_{t+1}, \ldots, \hat{\mathbf{x}}_{t+W}\}$$

其中每个 $\mathbf{x}_i$ 为 SMPL-X 身体模型的姿态参数，$\mathbf{c}_i$ 包含头部和手腕的 6-DOF 位置与旋转（Section 3.1, Equation 1）。

### 预测一致性锚定函数（PCAF）

核心洞察在于：将运动生成视为对未来姿态序列的渐进式细化过程。PCAF 将网络的原始输出重新参数化，使当前时刻的最终预测 $\mathcal{P}_t$ 由上一时刻的预测 $\mathcal{P}_{t-1}$ 加上一个受约束的修正量得到：

$$\mathcal{P}_t = \mathcal{P}_{t-1} + U \cdot \tanh(f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) - \mathcal{P}_{t-1})$$

其中各变量含义如下：
- $\mathcal{P}_{t-1}$：上一时刻的滚动预测输出，作为当前细化的先验锚点；
- $f_{\theta}(\mathcal{X}_t, \mathcal{C}_t)$：网络基于当前上下文和追踪输入产生的原始预测；
- $\tanh(\cdot)$：双曲正切缩放函数，将修正量限制在 $[-1, 1]$ 范围内，防止单步修正过大；
- $U$：不确定性标量，控制允许修正的最大幅度（Section 3.1, Equation 2）。

PCAF 的关键机制在于：当追踪信号丢失、网络进入自由运行（free-running）模式时，$\mathcal{P}_{t-1}$ 作为强运动先验维持生成连续性；当追踪信号恢复时，修正量被限定在不确定性边界内，避免突变式跳变。消融实验证实，移除 PCAF 后合成到追踪模式的过渡平滑度 AUJ_S-T 从 69.02 飙升至 799.03（Table 3）。

### 不确定性调度

不确定性 $U$ 并非全局常数，而是随预测距离 $\tau \in [0, W]$ 单调递增的函数。论文采用余弦不确定性函数：

$$f_{\mathrm{cos}}(\tau) = 1 - \cos\Bigl(\frac{\tau + 1}{W} \cdot \frac{\pi}{2}\Bigr)$$

该函数使近期预测（小 $\tau$）的修正幅度受限，保证输出平滑；远期预测（大 $\tau$）允许更大修正，保留对追踪信号的响应能力。消融表明余弦函数在过渡平滑度指标上优于余弦平方和线性函数（Appendix E, Table A）。

### 管道模块

RPM 由以下核心模块串联构成（Figure 2）：

1. **Motion Context Encoder**：将过去 $M$ 帧已生成的运动 $\mathcal{X}_t$ 编码为上下文特征，作为显式运动状态。
2. **Tracking Input Encoder**：将当前及过去的追踪输入 $\mathcal{C}_t$ 编码，并通过交叉注意力与运动上下文特征交互。
3. **Transformer Encoder**：四层 Transformer 编码器处理融合后的序列特征，输出未来 $W$ 帧的未修正预测。
4. **PCAF Module**：应用上述 PCAF 公式，结合上一时刻预测 $\mathcal{P}_{t-1}$ 与不确定性 $U$ 进行加权修正，产生最终输出 $\mathcal{P}_t$。
5. **Free-Running Simulation**（仅训练时）：在每次训练迭代开头，先让网络使用自身预测运行一段自由运行阶段以填充上下文，使网络学会从自身错误中恢复（Algorithm 1）。

### 训练损失

总损失为全局方向、相对旋转、关节位置及其速度的 L1 损失加权和：

$$\mathcal{L} = \lambda_{\mathrm{ori}} \mathcal{L}_{\mathrm{ori}} + \lambda_{\mathrm{rot}} \mathcal{L}_{\mathrm{rot}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\overrightarrow{\mathrm{ori}}} \mathcal{L}_{\overrightarrow{\mathrm{ori}}} + \lambda_{\overrightarrow{\mathrm{rot}}} \mathcal{L}_{\overrightarrow{\mathrm{rot}}} + \lambda_{\overrightarrow{\mathrm{pos}}} \mathcal{L}_{\overrightarrow{\mathrm{pos}}}$$

所有损失仅施加在自由运行阶段之后的最后一个预测窗口 $\mathcal{P}_{t+fr}$ 上，且不沿自由运行过程进行时间反向传播以节省训练内存（Section 3.3, Equation 3）。

## 实验与关键发现

### 核心瓶颈验证：合成-追踪过渡平滑度

现有方法在扩展现实（XR）场景中面临的核心挑战是追踪信号的时空稀疏性——尤其是手部追踪（Hand Tracking, HT）模式下信号频繁且长时间丢失。当追踪恢复时，传统方法会产生剧烈的姿态突变（abrupt snaps），破坏沉浸感。RPM 通过滚动预测与预测一致性锚定函数（PCAF）的组合，从根本上解决了这一过渡不平滑问题。

在 A-P1 手部追踪基准上，**RPM-Reactive** 的合成到追踪过渡平滑度指标 AUJ_S-T 为 **69.02**，而最强基线方法 **HMD-Poser**（基于 RNN 的 SOTA）高达 **1236.47**，平滑度提升超过 **17 倍**（Table 1）。更平滑的 **RPM-Smooth** 变体进一步将 AUJ_S-T 降至 **50.23**，提升幅度达 **24.6 倍**。在跨数据集 A-P2 上，这一优势同样显著：RPM-Reactive 的 AUJ_S-T 为 32.81，RPM-Smooth 为 11.93，而 HMD-Poser 为 174.80（Table 2）。这些结果表明，RPM 的滚动预测细化机制在信号恢复时能够渐进地将生成姿态拉回追踪目标，而非瞬间跳变。

![[assets/figures/papers/paper_list_l1858_GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models/figures/004_Table_1.jpg]]
*Table 1: Comparison of RPM with the state of the art on A-P1. We observe how our model generates motion with less jitter, and with considerably smoother transitions (i.e., lower PJ and AUJ) from tracking to synthesis (T-S) mode, and vice versa (S-T)*

![[assets/figures/papers/paper_list_l1858_GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models/figures/005_Table_2.jpg]]
*Table 2: Comparison of RPM with the state of the art on A-P2*

### PCAF 的关键作用：消融实验证据

消融实验（Table 3, A-P1 HT）揭示了 PCAF 与自由运行（free-running）训练的协同必要性：

![[assets/figures/papers/paper_list_l1858_GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models/figures/006_Table_3.jpg]]
*Table 3: Ablation study (A-P1, HT setup). Motion generated with RPM tends to degenerate unless combined with free-running (FR). PCAF ensures RPM generates smooth transitions from synthesis to tracking mode (S-T), and vice versa (T-S)*

- **仅保留 free-running 而移除 PCAF**：AUJ_S-T 从 69.02 飙升至 **799.03**，过渡平滑度劣化超过 11 倍，同时 Jitter 从 4.21 升至 5.36，表明网络输出直接匹配追踪信号时会产生高频抖动。
- **仅保留 PCAF 而无 free-running**：模型退化，MPJPE 升至 10.59 cm（完整 RPM 为 4.47 cm），说明网络未学会从自身预测误差中恢复。
- **两者结合**：PCAF 将修正量限制在不确定性范围内（$\mathcal{P}_t = \mathcal{P}_{t-1} + U \cdot \tanh(f_{\theta} - \mathcal{P}_{t-1})$），而 free-running 训练使网络对运动上下文与追踪输入之间的错位具有鲁棒性，二者缺一不可。

进一步的组件消融表明：
- **不确定性函数选择**（Table A, Appendix E）：余弦函数 $f_{\cos}(\tau) = 1 - \cos(\frac{\tau+1}{W} \cdot \frac{\pi}{2})$ 在 AUJ_S-T 和 AUJ_T-S 上均优于余弦平方和线性函数，同时保持相近精度。
- **PCAF 缩放函数**（Table D, Appendix I）：双曲正切（$\tanh$）比 sigmoid 产生更平滑的合成-追踪过渡；线性函数精度相当但过渡略显生硬。
- **自由运行长度**（Figure C, Appendix D）：较长的自由运行阶段（>50 帧）持续提升精度和平滑度，在 90 帧时达到最佳过渡平滑度，验证了该训练策略的重要性。

### 与传统平滑方法的对比

一个自然的疑问是：能否通过在基线方法上施加低通滤波来匹敌 RPM 的平滑度？实验（Table C, Figure E, Appendix G）给出了否定答案。在 **HMD-Poser** 等基线方法上应用 1€ 滤波器后，要达到 RPM 的合成-追踪平滑水平，基线的准确度需牺牲超过 **50%**。RPM 的 PCAF 机制本质上是一种自适应平滑策略——不确定性 $U$ 随预测距离 $\tau$ 增加而增大，对远未来预测施加更强的先验约束，对近未来则保留更高的追踪响应性，从而在准确性-平滑度权衡曲线上实现了现有方法无法达到的最优平衡点（Figure E）。

### 预测窗口长度与响应性-平滑度权衡

RPM 通过调整预测窗口长度 $W$ 提供了灵活的响应性-平滑度控制（Figure 4）。在 A-P1 上：
- 预测长度约 **8 帧（133 ms）** 时达到最佳手部精度（Hands PE 最低）；
- 预测长度约 **15 帧（250 ms）** 时达到最佳平滑度（Jitter 和 Peak Jerk 最低）。

这一特性使 RPM 可根据应用场景灵活配置：游戏场景偏好低延迟响应（短窗口），社交 VR 场景偏好平滑自然运动（长窗口），无需重新训练模型。

### 真实数据验证：GORP 数据集

在真实 VR 数据 GORP 上的实验进一步验证了 RPM 的实用性。在运动控制器（MC）场景下（Table 4），RPM-Reactive 的 MPJPE 为 **5.27 cm**，与 HMD-Poser（5.52 cm）相当，但 Jitter 更低（4.21 vs. 5.96），验证了 RPM 在保持精度的同时显著提升运动平滑度。

![[assets/figures/papers/paper_list_l1858_GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models/figures/007_Table_4.jpg]]
*Table 4: Comparison of RPM with the state of the art on the GORP dataset when using motion controllers as tracking inputs. We observe a performance gap between training on simulated MC and training in real MC due to non-rigid position and orientation of the controller. GORP allows, for the first time, training on real controllers data, which improves the performance of all methods*

在手部追踪场景下（Table 5），RPM 是**唯一**能够在长期信号丢失后保持稳定误差且不产生突变的方法（Figure F, Appendix H）。其手腕误差保持与全身误差量级相当，而基线方法在追踪恢复后误差剧烈波动。这归因于 PCAF 在信号丢失期间依赖运动上下文进行自由预测，恢复时通过不确定性调度渐进修正，避免了突变。

![[assets/figures/papers/paper_list_l1858_GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models/figures/008_Table_5.jpg]]
*Table 5: Comparison of RPM with the state of the art on the GORP dataset when using hand-tracking signal as inputs. In this setup, the performance gap between training models on simulated and real inputs also affects the motion dynamics (MPJVE, and jitter)*

### 失败模式与局限性

尽管 RPM 在平滑过渡上取得了显著突破，仍存在以下局限：

1. **脚部滑动**：所有方法（包括 RPM）仍存在脚部滑动问题，尤其在地面原地转动时。这可能源于模型缺乏体型感知和对头显驱动运动的过度依赖，需要显式的脚部接触约束或更强的运动学先验。
2. **长时间信号丢失的动作多样性**：RPM 采用确定性运动预测范式，无法捕捉未来的多模态可能性。在长时间追踪丢失时，生成的动作可能趋于平均姿态，缺乏表现力。
3. **输入模态限制**：当前仅使用头部和手腕的 6-DOF 追踪，未利用身体其他部位的 IMU 信息，限制了动态复杂动作的重建。
4. **控制器非刚性偏移**：在真实场景中，控制器位置可能因用户握持方式不同而发生非刚性偏移，现有模型对该变化的鲁棒性仍有限（Table 4 中模拟数据训练与真实数据训练之间的性能差距佐证了这一点）。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 1 | RPM 在 A-P1 手部追踪场景的合成-追踪过渡平滑度（AUJ_S-T）比最强基线 HMD-Poser 提升超过 17 倍 |
| Table 3 | PCAF 与 free-running 协同作用：单独移除任一组件均导致性能崩溃 |
| Figure 4 | 预测窗口长度控制响应性-平滑度权衡，8 帧最佳精度，15 帧最佳平滑度 |
| Table C / Figure E | 1€ 滤波器无法匹配 RPM 的平滑度，基线方法需牺牲 >50% 精度 |
| Figure F | RPM 在真实数据长期信号丢失后误差保持稳定，无突变 |

![[assets/figures/papers/paper_list_l1858_GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative comparison on synthetic HT inputs (A-P1). On the left, we show how RPM performs similarly to other state-ofthe-art methods when the tracking inputs contain strong information on the full-body pose. However, more ambiguous input configurations might lead to wrong generated poses, as shown in the first column on the right example. When the tracking is recovered, RPM is the only method that generates a smooth and realistic transition towards matching the new input*

## 定位与知识库关联

### 1. 问题定位：从稀疏信号到平滑运动的生成瓶颈

RPM 瞄准的核心问题是**扩展现实（XR）场景中实时全身运动生成的平滑性困境**。现有方法——无论是基于运动学优化的 AvatarPoser、基于扩散模型的 AGRoL，还是基于 RNN 的 HMD-Poser——在设计上均假定追踪信号持续可用且时间密集。然而，真实 XR 场景（尤其是手部追踪模式）中，信号呈现出**时间稀疏、频繁丢失、恢复时跳变**的特征。这导致现有方法在追踪恢复时产生剧烈突变（abrupt snaps），严重破坏沉浸感。

从因果机制看，这一瓶颈的根源在于：现有方法的输出范式是"逐帧直接生成当前姿态"，缺乏对未来运动轨迹的显式建模。当追踪信号从丢失状态恢复时，网络被迫在单帧内完成从合成姿态到追踪姿态的大幅跳变，梯度信号要求立即匹配输入，从而产生高冲击度（jerk）的过渡。

### 2. 核心机制创新：滚动预测与预测一致性锚定

RPM 的方法论贡献可分解为三个相互耦合的机制：

**（1）滚动预测范式（Rolling Prediction）**  
RPM 将在线运动生成重新表述为对未来姿态序列的渐进式细化过程。在每一时间步 $t$，网络 $f_\theta$ 预测未来 $W$ 帧的姿态序列：

$$f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) = \{\hat{\mathbf{x}}_t, \hat{\mathbf{x}}_{t+1}, \ldots, \hat{\mathbf{x}}_{t+W}\}$$

其中 $\mathcal{X}_t$ 为过去 $M$ 帧已生成的运动上下文，$\mathcal{C}_t$ 为当前及过去的追踪输入。这一设计的关键洞察在于：**运动生成可分解为先产生粗糙低频运动、再逐步添加高频细节的序贯过程**。通过预测未来窗口而非仅当前帧，网络获得了在时间维度上平滑分配修正量的自由度。

**（2）预测一致性锚定函数（PCAF）**  
PCAF 是 RPM 实现平滑过渡的核心控制机制。其数学形式为：

$$\mathcal{P}_t = \mathcal{P}_{t-1} + U \cdot \tanh(f_{\theta}(\mathcal{X}_t, \mathcal{C}_t) - \mathcal{P}_{t-1})$$

其中 $\mathcal{P}_{t-1}$ 为上一时刻的预测输出，$U$ 为不确定性标量。该公式将网络原始输出 $f_\theta$ 重参数化为"对上一时刻预测的修正"，并通过 $\tanh$ 将修正量限制在 $[-1, 1]$ 范围内，再乘以不确定性 $U$ 进行缩放。其效果是：**当不确定性较低时（如追踪信号刚恢复），修正量被抑制，运动保持平滑；当不确定性较高时（如追踪信号稳定），修正量增大，运动快速响应输入**。

**（3）不确定性调度（Uncertainty Scheduling）**  
$U$ 并非固定值，而是随预测距离 $\tau$ 变化的函数。RPM 采用余弦不确定性函数：

$$f_{\mathrm{cos}}(\tau) = 1 - \cos\Bigl(\frac{\tau + 1}{W} \cdot \frac{\pi}{2}\Bigr)$$

该函数使近期预测（$\tau$ 小）具有较低不确定性，修正保守；远期预测（$\tau$ 大）具有较高不确定性，修正激进。消融实验（Table A, Appendix E）证实，余弦函数在过渡平滑度指标 AUJ_T-S 和 AUJ_S-T 上优于余弦平方和线性函数，同时保持相近精度。

### 3. 训练策略创新：自由运行模拟

RPM 的训练策略同样构成方法论贡献。传统教师强制（teacher forcing）训练仅使用真实历史作为上下文，导致训练-推理分布偏移：推理时网络必须基于自身生成的运动进行预测，而自身生成的运动可能与追踪信号存在错位。

RPM 在每次训练迭代的开头引入**自由运行阶段（free-running）**：先让网络基于自身预测运行 $fr$ 帧以填充运动上下文 $\mathcal{X}_t$，然后才计算损失。损失仅应用于自由运行之后的预测窗口，且不通过时间反向传播（以节省显存）。这一策略迫使网络学会从自身错误中恢复，对追踪输入与生成运动之间的错位具有鲁棒性。

消融实验（Table 3）揭示了自由运行与 PCAF 的协同关系：
- **仅用 PCAF 无自由运行**：模型退化，MPJPE 升至 10.59 cm
- **仅用自由运行无 PCAF**：过渡极不平滑，AUJ_S-T 高达 799.03
- **两者结合**：AUJ_S-T 降至 69.02，同时 MPJPE 保持 4.62 cm

这表明 PCAF 提供平滑过渡的机制，而自由运行提供该机制有效运作所需的鲁棒上下文。

### 4. 与现有方法谱系的定位

RPM 可置于以下方法谱系中进行定位：

**相对于确定性回归方法（AvatarPoser, HMD-Poser）**：  
这些方法采用"输入-当前姿态"的直接映射范式，在追踪信号稳定时精度较高，但在信号丢失/恢复时产生突变。RPM 通过滚动预测和 PCAF 从根本上改变了输出范式，将单帧跳变转化为多帧渐进过渡。在 A-P1 手部追踪设置下，RPM-Reactive 的 AUJ_S-T 为 69.02，而 HMD-Poser 为 1236.47——平滑度提升超过 17 倍（Table 1）。

**相对于扩散模型方法（AGRoL）**：  
扩散模型通过迭代去噪生成运动，天然具有一定的平滑性。然而，其推理速度通常较慢，且仍以"生成当前帧"为目标。RPM 的滚动预测机制在保持实时性的同时，显式建模了未来运动轨迹的渐进细化。在 GORP 真实数据集上，RPM 是唯一能够在长期信号丢失后仍保持稳定误差且不产生突变的方法（Figure F, Section H）。

**相对于滤波后处理方法（1€ 滤波器）**：  
一个自然的问题是：能否简单地在现有方法输出上施加低通滤波来获得平滑性？消融实验（Table C, Figure E, Appendix G）给出了否定答案：要达到 RPM 的合成-追踪平滑水平，基线方法的准确度需牺牲超过 50%。这表明 RPM 的平滑性并非简单的后处理效果，而是源于预测范式和 PCAF 机制在生成过程中的内在约束。

**相对于人体运动预测方法**：  
RPM 的滚动预测机制与人体运动预测（human motion prediction）文献存在概念联系，但有关键区别：传统运动预测以真实历史为条件预测未来，而 RPM 以自身生成的运动历史为条件，且预测结果通过 PCAF 与新到达的追踪信号进行融合。这使得 RPM 处于"运动预测"与"运动生成"的交界地带。

### 5. 适用边界与局限

**（1）脚部滑动问题**  
所有方法（包括 RPM）仍存在脚部滑动，尤其在地面原地转动时。这可能源于模型缺乏体型感知（body awareness）和对头显驱动运动的过度依赖。RPM 的滚动预测机制并未显式建模足-地接触约束。

**（2）确定性范式的表达力限制**  
RPM 采用确定性运动预测范式，无法捕捉未来的多模态可能性。在长时间信号丢失时，生成的动作可能趋于平均姿态——这是确定性模型在高度欠约束条件下的固有局限。

**（3）输入模态的局限**  
当前追踪输入仅包含头部和手腕的 6-DOF 信息，未利用身体其他部位的 IMU 数据。这限制了动态复杂动作（如快速转身、蹲下）的重建精度。RPM 的架构虽可扩展至更多输入模态，但当前版本未探索此方向。

**（4）真实场景中的非刚性偏移**  
在真实控制器场景中，控制器位置可能因用户握持方式不同而发生非刚性偏移。Table 4 显示，从模拟控制器数据训练切换到真实控制器数据训练时，所有方法均出现性能下降，RPM 对此变化的鲁棒性仍有限。

### 6. 开放问题

1. **长时间丢失期间的多样性保持**：在追踪信号长时间丢失时，如何避免生成动作退化到平均姿态？是否需要引入随机性或多模态预测机制？

2. **滚动预测框架的随机化扩展**：能否将 PCAF 机制扩展到随机人体运动预测，以生成多种合理的未来动作，从而在信号恢复时提供更丰富的选择空间？

3. **脚部滑动的根治方案**：是否需要显式的脚部接触约束（如基于物理的损失项）或更强的运动学先验来消除滑动？滚动预测框架能否自然地融入此类约束？

4. **不确定性调度的自适应**：在真实部署中，PCAF 的不确定性调度应如何根据具体应用场景（如快节奏游戏 vs. 社交 VR）自动调整？能否从数据中学习最优调度策略？

5. **多模态传感器融合**：除了头部和手腕，能否有效融合头显摄像头以外的传感器数据（如腰部 IMU、腿部追踪器）以提升全身重建精度？RPM 的编码器架构是否支持即插即用的多模态扩展？

## 原文 PDF

![[paperPDFs/CVPR_2025/GORP_Real_Time_Motion_Generation_with_Rolling_Prediction_Models.pdf]]

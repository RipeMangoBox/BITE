---
title: "Beyond Mimicry: Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_Mimicry_Learning_Whole_Body_Human_Humanoid_Interaction_from_Human_Human_Demonstrations.pdf
project_link: null
code_link: null
aliases:
- BMPDS
- BMLWBHHIFHHD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入物理感知的交互重定向（PAIR）以保留接触语义，并采用解耦的时空推理（D-STAR）将“何时行动”与“在何处行动”分离，从而实现同步的全身协同行为。
primary_logic: 要从人-人交互数据学习全身人形机器人交互，必须同时解决数据层面的物理接触保持（PAIR 两阶段优化与接触损失）和策略层面的解耦时空推理（相位注意力与多尺度空间模块融合扩散规划），二者缺一不可。
claims:
- 天真重定向破坏了握手接触，而 PAIR 恢复了完整的物理连接。
- PAIR 在所有接触阈值上均达到最高 F1 分数（0.35m 阈值 F1 为 0.841），显著优于基线。
- D-STAR 在六项交互任务上获得 75.4% 平均成功率，而天真模仿基线为 0%。
- 移除相位注意力（PA）或移除多尺度空间模块（MSS）均导致特定交互任务性能严重下降。
---

# Beyond Mimicry: Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations

> [!tip] 核心洞察
> 要从人-人交互数据学习全身人形机器人交互，必须同时解决数据层面的物理接触保持（PAIR 两阶段优化与接触损失）和策略层面的解耦时空推理（相位注意力与多尺度空间模块融合扩散规划），二者缺一不可。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越模仿：从人-人交互演示中学习全身人形机器人交互 |
| 英文题名 | Beyond Mimicry: Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Beyond_Mimicry_Learning_Whole-Body_Human-Humanoid_Interaction_from_Human-Human_Demonstrations_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Beyond Mimicry (PAIR + D-STAR) |
| Dataset | Interaction Retargeting on HHI sequences, Six HHoI simulation tasks, Six HHoI tasks |

> [!tip] 效果简介
> - Interaction Retargeting on HHI sequences 上，Contact F1 @0.35m 0.841 vs 0.688 (Simple MSE) (+0.153)。
> - Six HHoI simulation tasks 上，Average Success Rate (%) 75.4 vs 0.0 (Naive Mimicry) / 64.3 (Transformer) (+75.4 / +11.1)。
> - Six HHoI tasks (Handshake) 上，Success Rate (%) 61.3 vs 32.3 (Transformer) (+29.0)。

## 概要

**核心问题与瓶颈。** 让人形机器人与人类进行全身物理交互（如握手、拥抱、击掌）面临双重挑战。在数据层面，标准运动重定向（motion retargeting）仅追求运动学相似性，在跨越人-机器人形态差异时不可避免地破坏关键的物理接触，导致生成的人-机器人交互数据丧失交互语义。在策略层面，传统模仿学习仅复制运动轨迹，缺乏对“何时交互”与“何处交互”的理解和响应能力。这两重瓶颈共同导致面向人-机器人交互（HHoI）的数据获取和策略设计双双失效。

**核心方法定位。** 本文提出 **Beyond Mimicry** 框架，从人-人交互（HHI）演示中学习全身人形机器人交互，通过两个互补模块解决上述瓶颈：

- **PAIR (Physics-Aware Interaction Retargeting)**：物理感知的交互重定向管线。将重定向形式化为一个带接触保持约束的优化问题，采用两阶段从粗到细策略——阶段1进行全局运动学初始化，阶段2加大接触权重精细调整——通过全对距离矩阵的 Frobenius 范数约束（$\mathcal{L}_{\mathrm{con}}$）显式保持人-机器人之间的接触几何语义，同时允许人类伙伴运动做最小必要调整（$\mathcal{L}_{\mathrm{hum}}$），生成物理一致、接触保持的 HHoI 数据。
- **D-STAR (Decoupled Spatio-Temporal Action Reasoner)**：解耦时空推理策略。将“何时行动”（when）与“在何处行动”（where）分离——相位注意力（PA）模块预测当前交互阶段并加权时序特征，多尺度空间模块（MSS）编码绝对位置、配对距离和相对朝向等几何关系，二者融合后经扩散规划头生成高维参考动作，再由底层全身控制器（WBC）转化为物理可行的关节指令。

**核心洞察。** 要从人-人交互数据学习全身人形机器人交互，必须同时解决数据层面的物理接触保持和策略层面的解耦时空推理，二者缺一不可。

**主要结果概览。**
- **重定向质量**：PAIR 在所有接触阈值上均取得最高 F1 分数（0.35m 阈值 F1 达 0.841），显著优于 Simple MSE（0.688）、ImitationNet 等基线。消融实验表明，去除接触损失 $\mathcal{L}_{\mathrm{con}}$（F1 降至 0.821）或将两阶段优化合并为单阶段（F1 降至 0.788）均导致性能显著下降。
- **交互成功率**：在六项 HHoI 仿真任务上，D-STAR 取得 75.4% 平均成功率，而天真模仿基线（Naive Mimicry）为 0%，Transformer 基线为 64.3%。在最具挑战性的握手任务上，D-STAR 成功率达 61.3%，较 Transformer（32.3%）提升近一倍。消融证实 PA 和 MSS 模块均至关重要——移除 PA 导致 High-Five 性能严重下降，移除 MSS 则损害 Handshake 表现。
- **真实世界验证**：在 Unitree G1 机器人上成功执行了拥抱、握手和击掌三种交互，验证了策略在异步单目 RGB 感知和标准控制器下的实际可执行性。

**方法谱系与知识库定位。** 本工作在以下维度与现有方法形成明确区分：
- **运动重定向**：传统方法（Simple MSE、IK Baseline、**ImitationNet** (Yan et al., Humanoids 2023)）仅优化运动学相似性，忽视接触保持。PAIR 首次将接触语义保持纳入重定向目标，并通过两阶段优化实现物理一致性。
- **交互策略**：标准模仿学习（BC、Transformer、TCN）和 **Diffusion Policy** (Chi et al., IJRR 2023) 直接映射观测到动作，缺乏对交互时空结构的显式建模。D-STAR 的解耦时空推理（PA + MSS + 扩散规划）使策略能够理解交互阶段并做出空间精确的响应，超越了简单的轨迹回放。

**局限与开放问题。** 量化实验主要在仿真中进行，真实世界性能受视觉感知噪声和延迟影响；仅在 Unitree G1 上验证了三种交互，泛化到其他机器人形态需重新优化 PAIR；系统依赖单目 SMPL 估计，姿态误差会直接影响交互成功率。开放问题包括：能否处理实时、未预标定伙伴的动态交互；如何结合力触觉反馈提升接触鲁棒性；解耦时空推理框架能否泛化到非接触性社会交互（如眼神交流、手势理解）；以及面对全新交互类型时的零样本泛化能力。



人形机器人与人类进行自然、流畅的全身交互，是机器人学迈向通用服务场景的核心愿景之一。然而，当前主流方法面临一个根本性瓶颈：**标准运动重定向在保持物理交互时破坏了关键接触**，而传统的模仿学习策略仅能复制轨迹，缺乏对交互语义的理解和实时响应能力。这导致面向人-机器人交互（Human-Humanoid Interaction, HHoI）的数据获取与策略设计双双失效。

问题的根源可从两个层面理解。在**数据层面**，现有运动重定向方法（如 Simple MSE、基于逆运动学的 IK Baseline 或 **ImitationNet**（Yan et al., Humanoids 2023））仅追求关节位置或角度的运动学相似性，完全忽略了交互过程中至关重要的物理接触约束。当源人类与目标人形机器人之间存在形态差异（如臂长、躯干比例）时，天真重定向会直接导致握手、击掌等接触动作断开，使生成的数据丧失交互意义（见 Figure 2 对比）。在**策略层面**，标准模仿学习方法（包括 Naive Mimicry 行为克隆、Transformer、TCN 乃至 **Diffusion Policy**（Chi et al., IJRR 2023））采用单一时间编码器直接映射至动作空间，缺乏对“何时行动”与“在何处行动”的显式解耦推理，难以在动态交互中实现同步的全身协同行为。

本文的核心洞察是：**要从人-人交互（Human-Human Interaction, HHI）数据学习全身人形机器人交互，必须同时解决数据层面的物理接触保持和策略层面的解耦时空推理，二者缺一不可。** 这一洞察驱动了本文提出的 **Beyond Mimicry** 框架，包含两大核心组件：

- **PAIR（Physics-Aware Interaction Retargeting）**：一种物理感知的交互重定向方法，通过两阶段从粗到细优化和接触保持损失（$\mathcal{L}_{\text{con}}$），在跨越形态差异的同时保留接触语义，生成物理一致的 HHoI 数据。
- **D-STAR（Decoupled Spatio-Temporal Action Reasoner）**：一种解耦时空动作推理策略，通过相位注意力（PA）解决“何时行动”，通过多尺度空间模块（MSS）解决“在何处行动”，再由扩散规划头融合二者生成参考动作，经全身控制器执行。

Figure 1 展示了从 HHI 到 HHoI 的完整流水线，以及仿真与真实 Unitree G1 机器人上的交互执行结果，验证了该框架在六种交互任务（弯腰、挥手、飞吻、拥抱、击掌、握手）上的有效性。



## 核心方法与创新机理

本文的核心贡献在于同时解决了从人-人交互（HHI）数据学习全身人形机器人交互的两个关键瓶颈：**数据层面的物理接触保持**与**策略层面的解耦时空推理**。传统方法在这两个层面均存在根本性缺陷，而本文的 PAIR + D-STAR 组合方案实现了从“天真模仿”到“超越模仿”的跨越。

### 瓶颈分析：为什么传统方法失败？

标准运动重定向（如 Simple MSE、IK Baseline、**ImitationNet** (Yan et al., Humanoids 2023)）仅最小化关节位置或角度的运动学差异，完全忽略交互中的物理接触语义。当源人类与目标机器人存在形态差异时，这种天真重定向会直接断开握手、击掌等关键接触（见 Figure 2），使得生成的人-机器人交互（HHoI）数据在物理上不成立。

在策略层面，标准模仿学习（Naive Mimicry BC）或通用架构（Transformer、TCN、**Diffusion Policy** (Chi et al., IJRR 2023)）将时序编码直接映射为动作，缺乏对“何时行动”与“在何处行动”的显式解耦。这导致策略仅能回放轨迹，无法理解交互的阶段性语义和空间关系，在需要精确时空协调的接触型任务上完全失效——Naive Mimicry 在六项交互任务上的平均成功率为 **0.0%**（Table 3）。

### 核心因果机制：两个 changed slots

本工作的关键创新可归结为两个相互依赖的 changed slots，二者缺一不可：

**Slot 1：从运动学重定向到物理感知交互重定向（PAIR）**

传统重定向的目标函数仅包含运动学相似性 MSE，而 PAIR 引入了全新的加权组合目标函数：

$$\mathcal { L } _ { \mathrm { r e t a r g e t } } = w _ { \mathrm { c o n } } \mathcal { L } _ { \mathrm { c o n } } + w _ { \mathrm { k i n } } \mathcal { L } _ { \mathrm { k i n } } + w _ { \mathrm { h u m } } \mathcal { L } _ { \mathrm { h u m } } + w _ { \mathrm { r e g } } \mathcal { L } _ { \mathrm { r e g } }$$

其中 $\mathcal{L}_{\mathrm{con}}$ 是核心创新——通过最小化原始和优化后人-机器人交互的全对距离矩阵 Frobenius 范数差异，显式保持接触几何语义。此外，优化策略从单阶段改为**两阶段从粗到细**：阶段1进行全局运动学初始化，阶段2加大接触权重进行精细调整。这一设计使得 PAIR 在所有接触阈值上均取得最高 F1 分数（0.35m 阈值 F1 达 **0.841**，对比 Simple MSE 的 0.688，Table 1），同时实现最佳运动学相似性（JPE 0.174m）和运动平滑度（Jerk 降低 69%）。

**Slot 2：从单一时间编码到解耦时空推理（D-STAR）**

传统策略架构使用单一时间编码器直接映射至动作，而 D-STAR 将时空推理显式解耦为两个并行分支：
- **相位注意力（PA）**：预测当前交互阶段并加权注意力，解决“何时行动”的时序推理；
- **多尺度空间模块（MSS）**：编码绝对位置、配对距离、相对朝向等多尺度几何关系，解决“在何处行动”的空间推理。

PA 和 MSS 的特征融合后输入扩散规划头，生成高维参考动作目标，再由全身控制器（WBC）转化为物理可行的关节指令。这一解耦设计使得 D-STAR 在六项交互任务上取得 **75.4%** 的平均成功率，显著超越最强基线 Transformer（64.3%）和 Diffusion Policy（Table 3）。

### 消融证据：两个 slot 的独立贡献

消融实验严格验证了每个 changed slot 的必要性：

- **PAIR 消融**（Table 1）：移除接触损失 $\mathcal{L}_{\mathrm{con}}$ 导致 F1 降至 0.821；将两阶段优化合并为单阶段后 F1 骤降至 0.788；去除人类自适应项（HA）后 F1 降至 0.823。这表明接触保持损失和两阶段优化策略各自独立贡献于接触质量。
- **D-STAR 消融**（Table 3）：移除相位注意力（w/o PA）导致 High-Five 等需要精确时序协调的任务性能严重下降；移除多尺度空间模块（w/o MSS）则损害 Handshake 等依赖精细空间关系的任务。这证实了“何时”与“何处”的解耦推理对于不同类型的交互任务分别至关重要。

### 创新依赖关系

PAIR 和 D-STAR 并非独立创新，而是形成上下游依赖：PAIR 生成物理一致、接触保持的 HHoI 数据，为 D-STAR 提供可学习的交互基础；D-STAR 则利用解耦时空推理从这些数据中学习超越简单轨迹回放的同步全身协同行为。仅改进数据而使用天真策略（如 Diffusion Policy 使用 PAIR 数据但架构不解耦），或仅改进策略而使用破坏接触的数据，均无法实现有效交互——这一依赖关系在 Table 3 中 Diffusion Policy 的失败中得到了间接验证。



本文提出了 **Beyond Mimicry** 框架，旨在从人-人交互（HHI）演示数据中学习全身人形机器人与人交互（HHoI）的策略。该框架由两个核心阶段构成：**物理感知交互重定向（PAIR）** 与 **解耦时空动作推理器（D-STAR）**，二者分别解决数据生成和策略学习中的根本瓶颈。

### 核心瓶颈与解决思路

标准运动重定向在跨越人-机器人形态差异时，往往破坏关键的物理接触（如握手时手部脱离），而传统模仿学习仅复制轨迹，缺乏对交互时机与空间位置的推理能力。Beyond Mimicry 通过以下双重机制应对这一挑战：

- **PAIR**：引入接触保持损失与两阶段从粗到细优化，在重定向过程中显式保留接触语义，生成物理一致的人-机器人交互数据。
- **D-STAR**：将“何时行动”与“在何处行动”解耦，通过相位注意力与多尺度空间模块分别建模时序与空间推理，再经扩散规划头生成同步的全身协同动作。

### 整体流水线

图 1 展示了框架的端到端流程：

1. **数据生成（PAIR）**：输入人-人交互序列（如握手、拥抱），PAIR 通过两阶段优化——阶段 1 全局运动学初始化，阶段 2 加大接触权重精细调整——输出物理一致、接触保持的人-机器人交互数据。该过程同时允许人类伙伴运动进行小幅必要调整，以确保交互合理性。
2. **策略学习（D-STAR）**：以历史观测帧为输入，经长短期时序编码器（LSTE）提取多尺度时序特征，相位注意力（PA）预测当前交互阶段并加权注意力，多尺度空间模块（MSS）编码绝对位置、配对距离与相对朝向等几何关系。PA 与 MSS 的特征融合后送入扩散规划头，生成参考动作目标（关节位置与根运动）。
3. **执行**：低层全身控制器（WBC）将参考动作转化为物理可行的关节指令，驱动机器人执行。

### 模块关系与数据流

各模块间的输入输出关系如下：

- **PAIR → D-STAR**：PAIR 生成的重定向数据作为 D-STAR 的训练集，确保策略学习基于物理一致的交互样本。
- **LSTE → PA + MSS**：LSTE 输出的时序特征 $`\mathbf{f}_t^{\text{temp}}`$ 同时供给 PA 和 MSS 分支，形成解耦的时空推理。
- **PA + MSS → 扩散规划头**：PA 的相位感知特征与 MSS 的空间关系特征融合后，作为扩散规划头的条件输入，指导去噪过程生成参考动作。
- **扩散规划头 → WBC**：扩散规划头输出的参考动作目标传递给全身控制器，后者负责将其转化为满足物理约束的关节指令。

该设计确保了从数据到执行的每个环节都具备物理一致性和交互语义保持能力，为全身人形机器人交互提供了完整的解决方案。

### 补充图表

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/001_Figure_1.jpg]]
*Figure 1: From HHI to HHoI with simulation and real-robot results. Left: PAIR (Physics-Aware Interaction Retargeting) converts human–human interaction sequences into physically consistent human–humanoid (HHoI) clips by aligning morphology and explicitly preserving contact semantics via a two-stage pipeline. Top (Sim): Rollouts of the learned policy (D-STAR) in simulation, showing Bend, Wave, Fly-Kiss, Hug, High-Five, and Handshake, demonstrating synchronized whole-body interactions. Bottom (Real, a–c): Deployment on a Unitree G1 under a standard whole-body controller; the policy executes Hug, Handshake, and High-Five selected via text commands*



### 3.1 物理感知交互重定向 (PAIR)

PAIR 的核心思想是将人-人交互 (HHI) 序列转化为物理一致的人-机器人交互 (HHoI) 数据，其本质是一个带接触约束的优化问题：在给定源交互 $(M_{H_p}, M_{H_s})$ 的条件下，寻找最优机器人运动 $M_R$ 和最小调整的伙伴运动 $M'_{H_p}$。

**总目标函数**由四项加权损失构成：

$$
\mathcal{L}_{\mathrm{retarget}} = w_{\mathrm{con}} \mathcal{L}_{\mathrm{con}} + w_{\mathrm{kin}} \mathcal{L}_{\mathrm{kin}} + w_{\mathrm{hum}} \mathcal{L}_{\mathrm{hum}} + w_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}
$$

其中各损失项的含义与公式如下：

**运动学相似性损失** $\mathcal{L}_{\mathrm{kin}}$ —— 惩罚机器人关节位置与经形态调整后的源人类骨架位置之间的偏差，保持动作风格：

$$
\mathcal{L}_{\mathrm{kin}} = \frac{1}{T \cdot J_R} \sum_{t=1}^{T} \sum_{j=1}^{J_R} \| \mathcal{I}_t(R, j) - \mathcal{I}_t(\mathrm{Reshaped}(H_s), j) \|_2^2
$$

**交互接触保持损失** $\mathcal{L}_{\mathrm{con}}$ —— 通过最小化优化前后人-机器人交互的全对距离矩阵的 Frobenius 范数差异，保持整体接触几何语义。这是 PAIR 区别于天真重定向的关键：

$$
\mathcal{L}_{\mathrm{con}} = \frac{1}{T} \sum_{t=1}^{T} \| D_t^{\mathrm{opt}} - D_t^{\mathrm{orig}} \|_F^2
$$

**人体运动保真度损失** $\mathcal{L}_{\mathrm{hum}}$ —— 约束优化后的伙伴运动不偏离原轨迹太远，仅允许必要的小幅适应以确保交互合理：

$$
\mathcal{L}_{\mathrm{hum}} = \frac{1}{T} \sum_{t=1}^{T} \| \mathbf{p}_{H_p, t}' - \mathbf{p}_{H_p, t} \|_2^2
$$

$\mathcal{L}_{\mathrm{reg}}$ 为物理合理性正则项，约束关节角度、速度等物理量。

**两阶段优化策略**是 PAIR 的另一关键设计：阶段一进行全局运动学初始化，阶段二加大接触权重进行精细调整。消融实验表明，将两阶段合并为单阶段后，接触 F1 从 0.841 骤降至 0.788，验证了从粗到细策略对接触保持的决定性作用。

---

### 3.2 解耦时空动作推理 (D-STAR)

D-STAR 策略的核心创新在于将“何时行动”与“在何处行动”解耦，通过三个关键模块实现。

**长短期时序编码器 (LSTE)** —— 使用两个并行的 Transformer 编码器分别处理长时上下文和短时细节，输出拼接后的时序特征：

$$
\mathbf{f}_t^{\mathrm{temp}} = \mathrm{Concat}\big( E_{\mathrm{long}}(\mathbf{O}_{t-h+1:t}),\; E_{\mathrm{short}}(\mathbf{O}_{t-h'+1:t}) \big)
$$

其中 $h$ 和 $h'$ 分别为长、短历史窗口长度，$\mathbf{O}$ 为观测序列。长时编码器负责理解交互阶段（如握手的前奏、接触、分离），短时编码器提供精细协调所需的瞬时信息。

**相位注意力 (PA)** —— 预测当前交互阶段并加权注意力，实现“何时行动”的时序推理。消融实验显示，移除 PA 分支会导致 High-Five 等需要精确时序同步的任务成功率严重下降。

**多尺度空间模块 (MSS)** —— 编码绝对位置、配对距离、相对朝向等多尺度几何关系，解决“在何处行动”的空间推理。移除 MSS 分支则显著损害 Handshake 等依赖精确空间接触的任务。

PA 和 MSS 的特征融合后输入**扩散规划头 (Diffusion Planning Head)**，生成高维参考动作目标（关节位置与根运动），再由下层的**全身控制器 (WBC)** 转化为物理可行的关节指令执行。整个系统联合训练，损失函数耦合了扩散动作预测与辅助的相位分类和几何监督信号。

---

### 3.3 模块间因果关系

PAIR 与 D-STAR 并非独立设计，而是构成了一条因果链：PAIR 解决了数据层面的接触语义保持问题，为 D-STAR 提供了物理一致的训练数据；D-STAR 在此基础上通过解耦时空推理，学习到超越简单轨迹回放的交互策略。证据是：即使使用相同的 PAIR 数据和相同的全身控制器，**Diffusion Policy** (Chi et al., IJRR 2023) 这一强基线在六项交互任务上的平均成功率仍显著低于 D-STAR，表明仅重放轨迹不足以应对交互任务，验证了解耦时空推理的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/003_Figure_3.jpg]]
*Figure 3: PAIR preserves contact semantics and physical consistency via a two-stage retargeting pipeline. From HHI to HHoI while retaining contact semantics across morphology differences*

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/004_Figure_4.jpg]]
*Figure 4: Overview of D-STAR (Decoupled Spatio-Temporal Action Reasoner): Phase Attention (PA, “when to act”) and Multi-Scale Spatial module (MSS, “where to act”) are fused by a diffusion planning head to yield synchronized whole-body interaction beyond mimicry; a low-level Whole-Body Controller (WBC) executes the final physically plausible action*

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/002_Figure_2.jpg]]
*Figure 2: PAIR preserves physical consistency where naive methods fail. Left: A source HHI handshake. Center: Naive retargeting breaks essential contact due to morphological disparities. Right: PAIR first ensures kinematic plausibility, then applies an interaction-aware objective (Lcon) to refine and enforce the critical physical contact*



## 实验与关键发现

### 核心实验设计

论文围绕两个核心研究问题展开实验：(1) PAIR 物理感知交互重定向是否有效？(2) D-STAR 分层策略是否优于标准基线？实验分为重定向评估和交互策略评估两层，所有策略使用相同的 PAIR 生成数据集和相同的全身控制器（WBC），确保比较公平。定量评估在仿真环境中进行以消除硬件差异影响，真实机器人测试仅验证策略在异步感知下的实际可执行性。

---

### 重定向结果：PAIR 在接触保持与运动质量上的双重优势

Table 1 和 Table 2 给出了重定向方法的全面对比。PAIR 在所有接触阈值上均取得最高 F1 分数：在 0.35 m 阈值下达到 **0.841**，相较 Simple MSE（0.688）提升 +0.153，相较 ImitationNet（0.753）提升 +0.088。同时，PAIR 在运动学相似性（JPE 0.174 m）和运动平滑度上也达到最优——Jerk 均值仅为 Simple MSE 的 31%（降低 69%），表明两阶段优化在保持物理接触的同时避免了突兀的加速度变化。

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/005_Table_1.jpg]]
*Table 1: Retargeting results with ablations: physical consistency (JPE, AWD) and multi-threshold contact (Prec/Rec/F1/Acc) at*

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/006_Table_2.jpg]]
*Table 2: Retargeting results with ablations: physical plausibility (LargeAngle, AngleStd) and smoothness (Jerk mean/std). Metrics in Sec. 5.1.1; best bold, second underlined*

**消融分析揭示了各组件的关键贡献：**

- **去除人类自适应项（HA）** 后，接触 F1 降至 0.823，说明允许伙伴人体进行小幅姿态调整对恢复接触至关重要。
- **去除接触损失 $L_{\mathrm{con}}$** 后，F1 降至 0.821，验证了全对距离矩阵 Frobenius 范数约束是保持交互几何语义的核心机制。
- **将两阶段优化合并为单阶段** 后，F1 骤降至 0.788，证明“从粗到细”策略（阶段1全局运动学初始化 → 阶段2加大接触权重精细调整）对收敛至高质量解不可或缺。

这些结果与 Figure 2 的定性展示一致：天真重定向因形态差异导致握手接触完全断开，而 PAIR 通过两阶段优化恢复了完整的物理连接。

---

### 策略结果：D-STAR 实现 75.4% 平均成功率，天真模仿基线为 0%

Table 3 报告了六项交互任务（Bend、Wave、Fly-Kiss、Hug、High-Five、Handshake）的成功率对比。核心发现如下：

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/007_Table_3.jpg]]
*Table 3: This table compares the Success Rate (Acc %) on six interactive tasks. Our full method significantly outperforms architectural variants and fundamental baselines, especially on complex contact-based tasks (Hug, Handshake). The failure of Diffusion Policy, a strong baseline using the same data and controller, highlights that simply replaying trajectories is insufficient. Ablations show that both PA and MSS modules are critical for high performance*

| 方法 | 平均成功率 | 关键特征 |
|------|-----------|---------|
| Naive Mimicry (BC) | 0.0% | 纯行为克隆，完全无法完成任何交互 |
| Diffusion Policy (Chi et al., IJRR 2023) | 失败 | 使用相同数据和控制器，仅回放轨迹不足以应对交互 |
| Transformer | 64.3% | 强时序建模基线 |
| TCN | 57.8% | 时序卷积基线 |
| **D-STAR (Full Model)** | **75.4%** | 解耦时空推理 |

**D-STAR 相较最强基线 Transformer 提升 +11.1 个百分点**，且在接触密集型任务上优势尤为显著：Handshake 任务中 D-STAR 达到 61.3%，而 Transformer 仅为 32.3%（+29.0 个百分点）。这验证了核心洞察：仅有时序建模不足以处理需要精确空间协调的物理交互，解耦“何时行动”与“在何处行动”是突破瓶颈的关键。

**消融实验进一步证实了 PA 和 MSS 模块的互补性：**

- **移除相位注意力（PA）** 导致 High-Five 任务性能严重下降——该任务要求精确的时序同步（在恰当时刻抬手击掌），失去相位推理后策略无法判断交互阶段。
- **移除多尺度空间模块（MSS）** 则主要损害 Handshake 任务——该任务需要精细的空间关系编码（绝对位置、配对距离、相对朝向），失去多尺度几何推理后策略无法准确定位接触点。

---

### 鲁棒性分析：对伙伴变化呈平滑退化

Table 4 展示了在伙伴身体比例（0.8×–1.2×）和运动速度（0.8×–1.2×）联合变化下的平均成功率矩阵。中心值（标准设置）为 75.4%，向边缘逐渐平滑下降，最低为 52.1%（0.8× scale + 0.8× speed），未出现断崖式崩溃。这种“优雅退化”特性表明 D-STAR 学到了真正鲁棒的交互表征，而非过拟合于特定训练分布。

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/008_Table_4.jpg]]
*Table 4: Robustness Matrix: Average Success Rate (%) under combined variations in human partner’s scale and speed. The central value (bold) is our standard performance. The graceful degradation towards the edges demonstrates true robustness*

---

### 失败模式与局限性

尽管整体性能显著优于基线，论文仍存在以下失败模式和局限：

1. **Handshake 任务成功率仅 61.3%**，即使在仿真环境中也未完全解决。这表明精细接触交互对空间推理精度要求极高，MSS 模块的当前设计可能仍有改进空间。

2. **量化实验主要在仿真中进行**，真实世界性能受限于：单目 RGB 相机（Figure 5 中的 Logitech C1000e）的感知噪声、SMPL 估计误差（依赖 4D-Humans）、以及标定误差。真实机器人测试仅在 Unitree G1 上验证了三种较简单的交互（Hug、Handshake、High-Five），未覆盖 Hug 等更复杂的持续接触场景。

![[assets/figures/papers/paper_list_l1054_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Beyond_Mimicry_L/figures/009_Figure_5.jpg]]
*Figure 5: Monocular SMPL perception setup and result. (a) Unitree G1 with a Logitech C1000e RGB camera (1280 × 720@30 fps). (b) Input RGB frame. (c) SMPL mesh estimated from the single RGB stream (4D-Humans [14]) and mapped to the robot base frame after extrinsic calibration*

3. **系统依赖特定机器人形态**：PAIR 的形态调整和接触约束针对 Unitree G1 优化，泛化到其他机器人型号需重新执行两阶段优化。

4. **Naive Mimicry 的 0% 成功率**值得注意——这并非行为克隆本身的失败，而是揭示了在交互场景中，单纯复制轨迹而缺乏交互理解必然导致接触失败，从而引发级联错误。

---

### 关键图表结论总结

- **Figure 2**：定性证明 PAIR 恢复物理接触的核心能力。
- **Table 1 & Table 2**：定量证明 PAIR 在接触 F1、运动学相似性、运动平滑度上全面优于基线，消融验证各损失项和两阶段策略的必要性。
- **Table 3**：D-STAR 以 75.4% 平均成功率显著超越所有基线，消融验证 PA 和 MSS 模块分别对时序同步和空间协调任务的关键作用。
- **Table 4**：在伙伴身体比例和速度联合变化下呈平滑退化，证明策略的鲁棒性。
- **Figure 5**：真实机器人部署的感知管线，验证策略在异步单目感知下的可执行性。



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

该工作直面一个双重瓶颈：**数据层**，标准运动重定向在跨越人-机器人形态差异时，会系统性地破坏握手、拥抱等交互所依赖的物理接触，导致生成的人-机器人交互（HHoI）数据丧失交互语义；**策略层**，传统模仿学习仅复制观测轨迹，缺乏对“何时行动”与“在何处行动”的解耦理解，无法在动态交互中做出响应性协调。两个瓶颈相互锁定：数据缺乏接触保真度，策略便无从学习真正的交互；策略缺乏时空推理能力，即便有完美数据也无法应对交互的动态性。

论文的因果调节变量是**物理感知的交互重定向（PAIR）**与**解耦时空推理（D-STAR）**的联合引入。PAIR 通过两阶段优化与接触损失，在数据生成阶段显式保留接触语义；D-STAR 通过相位注意力与多尺度空间模块，在策略推理阶段将时序决策与空间定位分离。二者形成互补闭环：PAIR 提供接触一致的数据，D-STAR 利用该数据学习解耦的时空行为。

### 2. 在知识谱系中的定位

**上游依赖与基线关系**。该方法建立在两条技术线上：
- **运动重定向**：基线包括 Simple MSE（关节位置最小二乘）、IK Baseline 和 **ImitationNet**（Yan et al., Humanoids 2023）。这些方法仅优化运动学相似性，缺乏接触保持机制。PAIR 的核心改进在于引入基于全对距离矩阵 Frobenius 范数的接触保持损失（$L_{\mathrm{con}}$），并将优化过程分为两阶段——阶段1全局运动学初始化，阶段2加大接触权重精细调整——从而在保持运动学合理性的同时恢复关键物理接触。
- **交互策略学习**：基线包括 Naive Mimicry（行为克隆）、Transformer、TCN 和 **Diffusion Policy**（Chi et al., IJRR 2023）。这些方法将时序编码与空间推理耦合在单一映射中。D-STAR 的解耦设计——相位注意力（PA）负责“何时行动”，多尺度空间模块（MSS）负责“在何处行动”——是对此范式的结构性突破。值得注意，Diffusion Policy 使用与 D-STAR 完全相同的数据和控制器，却无法完成复杂接触任务，这反证了单纯轨迹回放不足以应对交互需求。

**下游使能与开放方向**。该方法为人形机器人社会交互开辟了从人-人演示数据端到端学习的可行路径，其解耦时空推理框架可潜在迁移至眼神交流、手势理解等非接触性社会交互。但当前系统依赖单目 RGB 相机与 SMPL 估计，人类姿态估计误差会直接传导至交互成功率；重定向的形态调整与接触约束针对特定机器人型号优化，泛化到其他形态需重新设计。

### 3. 适用边界与局限

**已验证的适用范围**：
- 六类交互任务：Bend、Wave、Fly-Kiss、Hug、High-Five、Handshake
- 仿真环境中的定量评估，真实机器人（Unitree G1）上验证了 Hug、Handshake、High-Five 三种交互的可执行性
- 对伙伴身体比例和运动速度的联合变化表现出平滑的性能退化（Table 4），证明一定程度的鲁棒性

**明确局限**：
- 真实世界性能受视觉感知噪声、延迟和建模误差影响，量化实验主要在仿真中进行
- 真实机器人测试仅覆盖三种简单交互，未涉及更复杂的环境或持续接触场景
- 系统依赖单目 RGB 和 4D-Humans 的 SMPL 估计，感知错误会直接影响交互成功率
- 重定向优化针对特定机器人型号，泛化到其他形态需重新优化

**证据强度说明**：PAIR 的接触保持效果由 Table 1 的多阈值 F1 指标和 Figure 2 的定性对比强支撑（置信度 0.95+）；D-STAR 的策略优势由 Table 3 的 75.4% 平均成功率与 Naive Mimicry 的 0% 对照强支撑（置信度 0.99）。消融实验进一步确认了各模块的因果贡献。但真实世界的泛化性能目前缺乏大规模验证，该点需手动确认。

### 4. 开放问题

1. **实时交互能力**：PAIR 和 D-STAR 当前处理预录制的 HHI 序列，能否适应实时、未预标定人类伙伴的动态交互？
2. **力触觉反馈整合**：如何结合力触觉传感器或外部接触感知，以提升物理接触的鲁棒性和安全性？
3. **交互类型泛化**：解耦时空推理框架能否零样本泛化到训练数据中未出现的新交互类型？
4. **跨形态迁移**：接触保持约束和形态调整策略如何系统化地迁移到不同尺寸、自由度的机器人平台？
5. **感知鲁棒性**：在 SMPL 估计误差较大或部分遮挡场景下，D-STAR 策略的性能退化模式与容错机制是什么？



## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_Mimicry_Learning_Whole_Body_Human_Humanoid_Interaction_from_Human_Human_Demonstrations.pdf]]

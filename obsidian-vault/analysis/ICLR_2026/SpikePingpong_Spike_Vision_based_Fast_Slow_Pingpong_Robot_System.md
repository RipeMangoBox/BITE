---
title: "SpikePingpong: Spike Vision-based Fast-Slow Pingpong Robot System"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SpikePingpong_Spike_Vision_based_Fast_Slow_Pingpong_Robot_System.pdf
project_link: null
code_link: null
aliases:
- SpikePingpong
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "引入‘快慢’双系统架构：系统1利用物理模型快速估计击球位置；系统2通过脉冲相机数据训练神经校准网络以纠正系统1的误差；IMPACT模仿学习模块实现策略性回球。"
primary_logic: "借鉴认知科学中双系统理论（快速直觉与慢速审慎）设计感知控制体系，将高性能硬件（脉冲相机）仅用于训练阶段，部署时仅依赖轻量网络，在保持精度的同时大幅降低推理延迟。"
claims:
- "快慢系统（系统1+系统2）将球拍接触点预测整体MAE降至12.34 mm，远优于纯物理模型（44.13）和RNN基线（22.80）。"
- "SpikePingpong在30cm目标区单次回球成功率达92%，超过人类爱好者（53%）和其他机器人方法（3-19%）。"
- "推理延迟仅0.407 ms，比扩散策略快约60倍，比ACT快17倍。"
- "移除系统2仅使用系统1+IMPACT，单目标成功率从92%骤降至23%，证明神经校准对精度的关键作用。"
---

# SpikePingpong: Spike Vision-based Fast-Slow Pingpong Robot System

> [!tip] 核心洞察
> 借鉴认知科学中双系统理论（快速直觉与慢速审慎）设计感知控制体系，将高性能硬件（脉冲相机）仅用于训练阶段，部署时仅依赖轻量网络，在保持精度的同时大幅降低推理延迟。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SpikePingpong: 基于脉冲视觉的快慢乒乓球机器人系统 |
| 英文题名 | SpikePingpong: Spike Vision-based Fast-Slow Pingpong Robot System |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=d08yOXs1Dl) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | SpikePingpong |
| Dataset | Ball-racket contact prediction error, Single-target return accuracy (30cm zone), Single-target return accuracy (20cm zone), Sequential target execution (30cm) |

> [!tip] 效果简介
> - Ball-racket contact prediction error 上，Overall MAE (mm) 为 12.34，对比 System 1 Only: 44.13; RNN: 22.80，变化 －72.1% vs System 1; －45.9% vs RNN。
> - Single-target return accuracy (30cm zone) 上，Success rate (%) 为 92，对比 Human amateur: 53; ACT: 12-19; Diffusion Policy: 3-6，变化 ＋39% over human; ＋73-89% over other robots。
> - Single-target return accuracy (20cm zone) 上，Success rate (%) 为 70，对比 Human: 33; ACT: 4-7; Diffusion Policy: 1-2，变化 ＋37% over human; ＋63-69% over other robots。

## 概要

在高速动态场景中，乒乓球机器人须精确预测来球轨迹并精准回击至指定目标，同时满足毫秒级实时推理。纯物理弹道模型无法处理旋转、空气阻力等复杂因素，接触点预测误差高达（MAE 44.13 mm），而端到端模仿学习策略（如Diffusion Policy、ACT）又面临推理延迟高（>7 ms）和低成功率（<19%）的困境。SpikePingpong 借鉴认知科学的“快‑慢”双系统理论，设计快‑慢融合感知控制架构：系统1利用RGB‑D相机与物理模型快速估计击球位置，系统2通过高帧率脉冲相机（20 kHz）离线训练Transformer神经校准网络，仅需轻量网络即可在部署时大幅纠正系统1的偏差，并结合IMPACT模仿学习模块将轨迹、关节状态和目标落区映射为关节调整量，实现策略性回球。

该方案的核心洞察在于，高性能脉冲相机仅用于训练阶段提供精标注，实际推理完全依赖传统相机和极轻量的校准网络，从而在保持高精度的同时将推理延迟压缩至0.407 ms（比ACT快约17倍，比Diffusion Policy快约62倍，Table 2）。主要实验结果表明：快‑慢系统将球拍接触点预测整体MAE降至12.34 mm（较纯物理模型降低72%，较RNN基线降低46%，Table 1）；在30 cm目标区单次回球成功率达92%，超过人类业余爱好者（53%）和其他机器人方法（3‑19%）；20 cm高精度任务中成功率70%（Table 3）。消融实验证实，移除系统2后单目标成功率骤降至23%，验证了神经校准的必要性（Table 7）。当前方法仍存在未建模球体旋转、对极端轨迹泛化不足等局限，超高精度（10 cm）成功率仅31%，这些构成了后续研究的重要方向。



高速乒乓球场景中，机器人需在毫秒级内完成对来球的精准拦截，并将球精确回击至目标位置。这一任务对视觉感知、轨迹预测和运动控制的实时性与精度提出了极高要求。传统 RGB 相机受限于帧率（通常 60 fps），在快速运动下产生严重的运动模糊（Figure 5），导致球的位置检测噪声大、状态估计不可靠。物理弹道模型虽然推理极快，但忽略了空气阻力、球体旋转（Magnus 效应）和非弹性碰撞等复杂因素，使得击球点预测误差难以接受——纯粹依赖物理模型的系统（System 1 Only）在一次验证中整体平均绝对误差高达 44.13 mm（Table 1）。若完全采用端到端的模仿学习策略（如 Diffusion Policy、ACT），虽具备一定的灵活学习能力，但推理延迟开销显著（25.18 ms 和 7.15 ms），难以满足实时控制需求（Table 2）。与此同时，已有系统如 HYSR 在超高精度目标（10 cm 区域）下的成功率仅 8%（Table 8），而人类业余爱好者在 30 cm 区域的回球精度也仅 53%（Table 3）。上述缺口说明：无论是纯模型方法、纯学习范式，还是现有工程系统，均未能在“精度–延迟–策略性”三角中取得突破。

针对这一瓶颈，SpikePingpong 借鉴认知科学中的双系统理论——“快速直觉”与“慢速审慎”相结合——提出一种新的感知‑控制架构。其核心动机在于：利用脉冲相机（20 kfps）的无模糊高频数据所蕴含的精细运动信息，但仅在训练阶段对神经校准网络进行监督，部署时则仅依赖普通 RGB‑D 相机和轻量校准网络，从而在保持精度的同时将推理延迟大幅压缩至 0.407 ms（Table 2）。具体而言，系统 1（物理快速估计）以约 150 Hz 的频率完成球检测与初步轨迹预测，保证微秒级响应；系统 2（脉冲导向神经校准器）则针对系统 1 的残留偏差进行回归校正，使接触点预测的 MAE 从 44.13 mm 降低到 12.34 mm（Table 1）。在此基础上，IMPACT（基于模仿的运动规划与控制技术）模块通过模仿学习直接输出关节空间的调整指令，将感知、规划、控制融为一体，使机器人能够在 92% 的单次回球中精确命中 30 cm 目标区域（Table 3）。该架构将“高性能感知用于训练、轻量前向用于部署”的理念贯穿始终，从而克服了实时性约束下感知与控制的双重困难，为高速动态交互任务提供了一种可推广的范式。



## 核心方法与创新机理

SpikePingpong 针对高速乒乓球场景下轨迹预测不准、实时推理要求严苛的双重瓶颈，提出了一套解耦的感知‑控制架构。其核心创新在于将认知科学中的双系统理论具象化为“快‑慢”闭环：系统1提供毫秒级物理预判，系统2通过脉冲视觉习得的神经校准器纠偏，而IMPACT模块则以模仿学习直接生成策略性回球指令。三个维度的 changed slots 共同将球‑拍接触点预测误差压至 12.34 mm，单目标回球成功率推至 92%，且推理延迟仅为 0.407 ms。

| 变更维度 | 基线方案 | 提出方案 | 关键证据 | 效果（Δ） |
|----------|----------|----------|----------|-----------|
| **视觉感知** | 普通RGB相机（60 fps），存在运动模糊 | RGB‑D（60 Hz）+ 脉冲相机（20 kHz）**仅用于训练**，部署时仅依赖RGB‑D | Fig 5, Sec 3.1 | 消除高速模糊，为校准网络提供真值 |
| **轨迹预测** | 纯物理弹道模型（无法补偿旋转/空气阻力） | 系统1（物理预测 + EMA滤波） + 系统2（Transformer校准网络） | Table 1, Table 7 | MAE↓72.1%（vs 纯物理）；成功率↑69pp（消融） |
| **回球策略** | 固定规则或仿真策略；Diffusion Policy/ACT等模仿学习方法 | IMPACT：Transformer在真实数据上训练，映射轨迹、关节构型、目标落区→关节调整 | Table 3, Table 2 | 30 cm单目标成功率 92%（人类 53%，ACT 12‑19%）；推理延迟 0.407 ms（≈ACT的1/18） |

### 1. 物理‑神经双通路轨迹预测（快‑慢系统）

单一物理模型无法处理旋转、空气阻力等复杂力学，导致击球点预判出现系统性偏差（MAE=44.13 mm）；而端到端RNN虽能学习数据驱动补偿，但误差仍有22.80 mm。SpikePingpong 的解法是保留物理模型作为快速先验，再用神经校准网络学习残差：系统1以YOLOv4‑tiny（≈150 Hz）检测球体，EMA滤波抑制噪声并外推抛物线轨迹；系统2则在**脉冲相机**（20 kHz）提供的无模糊击球点真值上训练一个Transformer，预测系统1估计的击球点与实际接触点之间的二维偏差向量（损失函数为 $L_{MSE}(\theta)=\frac{1}{N}\sum\|\hat{D}_i-D_i\|^2$，见 Eq.3）。推理时只执行一步前向传播，保留轻量特性。该设计将预测 MAE 降至 12.34 mm，RMSE 降至 13.85 mm（Table 1），且消融实验直接证明：移除系统2后单目标成功率从92%暴跌至23%（Table 7），说明神经校准是不可或缺的因果组件。

### 2. 从感知到动作的端到端模仿学习控制（IMPACT）

传统机器人乒乓球系统多采用基于物理的固定挥拍规则或离线强化学习策略，面对连续落点任务时效性和精度均不足。SpikePingpong 提出 **IMPACT**（Imitation‑based Motion Planning And Control Technology），它是一个Transformer架构的模仿学习模块，接收拼接输入（轨迹序列、当前关节角度、目标落区标签），直接输出关节调整量，以 $L_{MSE}$（Eq.4）端到端训练。训练数据通过向机械臂三个关键关节施加随机偏置并只保留成功回球的对局收集，从而覆盖多样化拍型。由于整个推理只涉及轻量网络的一次前传，IMPACT 的延迟仅为 0.407 ms，比 ACT（7.15 ms）快 17 倍以上，比 Diffusion Policy（25.18 ms）快约 60 倍（Table 2）。在 30 cm 目标区域的任务上，单目标成功率 92%，连续多目标序列成功率 78%，均远超人类业余玩家和已有机器人系统（Table 3, 4）。这些指标表明 IMPACT 不仅拥有战略级精度，而且保持了实时控制的刚性要求。

### 3. 训练‑部署分离的高频视觉感知方案

脉冲相机能提供 20 kHz 的清晰图像，彻底消除运动模糊（Fig 5），但其数据体积和成本使其不适合直接部署在实时控制回路中。SpikePingpong 的创新之处在于将该高性能传感器**仅用于训练阶段**：用脉冲相机采集精确的球‑拍接触点坐标，作为系统2和IMPACT的监督信号；部署阶段仅依赖常规RGB‑D相机（60 Hz）和已训练的网络，推理时无需高速硬件。这种“借力训练，轻量执行”的模式使得系统在保持高精度（MAE 12.34 mm）的同时，实现亚毫秒级控制，而基线方法若单纯使用高频相机则会面临带宽或处理延迟瓶颈。该设计也隐含地构成了对前沿机器人系统中“感知‑决策‑执行”紧耦合惯例的一次打破，将传感精度的红利通过知识蒸馏范式注入轻量推理管线。

### 局限与开放问题

需要指出，以上创新尚未建模球体旋转（Magnus效应），因此对强烈旋转来球的预测偏差仍较大；IMPACT 对未见过的人类打法泛化能力有限（Table 6, unseen player 成功率约 31%）；超高精度（10 cm 目标）成功率仅约 31%，距离竞技级对打仍有距离。这些不足也正是 future work 的明确方向——例如将旋转估计作为额外监督信号、引入在线适应机制，或利用脉冲数据直接学习接触点动力学以提升超高精度场景下的表现。



![[assets/figures/papers/iclr26_0013_d08yOXs1Dl_SpikePingpong_Spike_Vision-based_Fast-Slow_Pingp/figures/002_Figure_2.jpg]]
*Figure 2: Framework of SpikePingpong. The system comprises two integrated components: (1) A Fast-Slow perception architecture, where System 1 delivers rapid trajectory prediction using RGB-D data, while System 2 functions as a Spike-Oriented Neural Improvement Calibrator to refine the estimated hittable position; and (2) The IMPACT module, which facilitates strategic motion planning and control, enabling tactical return placement via imitation learning*

![[assets/figures/papers/iclr26_0013_d08yOXs1Dl_SpikePingpong_Spike_Vision-based_Fast-Slow_Pingp/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SpikePingpong. The framework integrates two key stages: (1) Interception, using a Fast-Slow architecture for precise trajectory prediction, and (2) Striking, employing the IMPACT module to execute strategic returns via imitation learning. The system achieves a 92% overall success rate and 70% in high-precision targeting tasks*

SpikePingpong以认知科学的双系统理论（快速直觉 vs. 慢速审慎）为设计范式，将乒乓球回击任务解耦为两个紧密协作的阶段：**拦截阶段**的快慢感知与**打击阶段**的模仿策略规划（图1）。前者通过物理模型与神经校准的互补，精确预测球拍接触点；后者则依据预测轨迹和目标落区，生成具有战术意图的关节控制指令。两者在统一的多频控制系统调度下，仅依赖商用RGB‑D相机即可实现毫秒级推理与厘米级击球精度。

**拦截阶段的快慢感知**由系统1（快速）和系统2（慢速校准）构成（图2）。  
- **系统1**接收RGB‑D图像，使用YOLOv4‑tiny进行高速球检测（最高约150 Hz），并通过基于物理的指数加权移动平均（EMA）滤波器同时估计球的当前位置 $(x,y,z)$ 与速度 $(v_x, v_y, v_z)$。该滤波器将标准弹道方程（含重力加速度 $g=9.81\,\mathrm{m/s^2}$ 和恢复系数 $e$）作为动力学预测模型，与实时观测融合，获得平滑的轨迹状态。随后，系统1利用物理模型推演触台后的飞行路径，输出一个初步的球拍接触点位置。  
- 然而，纯物理模型无法补偿旋转（Magnus效应）、空气阻力等复杂动力学，导致预测偏差较大——仅使用系统1时，球拍接触点的整体平均绝对误差达 **44.13 mm**（表1）。**系统2**正是为此设计的不依赖于部署时高性能硬件的神经校准器：在训练阶段，系统利用脉冲相机（20,000 fps）捕获的无运动模糊图像，获取球体真实接触点，构建一个Transformer网络，学习系统1预测点与真实点之间的偏差向量；在部署时，系统2仅接收系统1输出的（位置、速度、预测点）作为输入，直接推断校正量。加入系统2后的快慢系统将整体MAE压降至 **12.34 mm**（表1），相对系统1降低了 72.1%，并且推理引入的额外延迟极小（0.407 ms），远快于主流模仿学习基线（表2）。

**打击阶段的IMPACT模块**接收校准后的轨迹预测结果，执行策略性回球。IMPACT是一个基于模仿学习的Transformer网络，其输入融合三模态信息：① 球飞行轨迹的时序特征（位置、速度），② 机器人当前关节构型 $\mathbf{j}$，③ 用户指定的目标落区控制信号 $\mathbf{c}$（图2）。网络输出关节角度的调整量 $\Delta \mathbf{J}$，直接驱动机器人完成带有方向与落点意图的击球。训练数据来自在真实环境中对机器人关节施加随机扰动后记录的成功回球轨迹，网络以均方误差最小化预测关节调整与真实值之间的差异。

**多频控制协同**确保上述模块无缝衔接（图3）。系统1与系统2构成的快慢感知以 **60 Hz** 频率更新预测，提供足够实时的拦截指导；IMPACT以 **2.4 kHz** 频率计算关节指令，满足精密运动的控制带宽；ABB IRB‑120 机械臂通过外部位移传感器向导（EGM）接口以 **250 Hz** 通信，最终实现从视觉感知到关节执行的端到端低延迟闭环。

整体数据流可以描述为：RGB‑D 视频流 → 系统1（检测/滤波/物理推演） → 系统2（神经偏差校正） → 精确击球点；同时，目标落区信号和当前关节构型 → IMPACT → 关节调整量 → 机械臂执行。训练过程中，脉冲相机提供的高频真值只用于监督系统2与IMPACT，部署时完全卸除，从而在保持精度的同时使推理延迟控制在亚毫秒量级。



SpikePingpong 系统面临的核心瓶颈是高速动态场景下乒乓球轨迹预测的精度与推理实时性之间的矛盾：纯物理弹道模型无法补偿空气阻力、旋转等复杂因素（整体 MAE 高达 44.13 mm），而端到端深度学习方法推理延迟过高（Diffusion Policy 25.18 ms）。该方法引入「快-慢」双系统架构：系统1利用高效物理模型实现毫秒级快速预测，系统2通过脉冲相机数据训练轻量 Transformer 校准网络，在部署时仅需 0.407 ms 推理即可将接触点 MAE 压低至 12.34 mm；同时，IMPACT 模仿学习模块将轨迹与关节状态映射为策略性回球动作，使击球落点可控。以下分别说明各核心模块的因果机制及其关键公式。

### 系统1：快速感知与物理预测（System 1 – Fast Perception）
系统1以 YOLOv4‑tiny 检测器（~150 Hz）提取球的图像坐标，结合 RGB‑D 深度信息获取三维位置，并通过指数加权滑动平均（EMA）融合物理模型预测与观测值，稳定估计状态 $\hat{x}_t$。

**EMA 滤波状态更新公式**  

$$
\hat{x}_t = (1-\alpha) \cdot f(\hat{x}_{t-1}) + \alpha \cdot z_t
$$
  
其中 $f(\hat{x}_{t-1})$ 为动力学模型对当前时刻的预测（基于匀速或匀加速假设计算位置与速度），$z_t$ 为传感器观测值，$\alpha$ 为平滑系数。该滤波有效消除高频检测噪声，同时保持抛物线运动特征（见 Figure 7）。

在获得稳定的位置与速度矢量后，系统1采用简化的弹道模型预测球拍接触点。核心方程利用能量守恒与恢复系数计算触台前后的垂直速度：

**（Eq 1）触台瞬时垂直速度**  

$$
v_{z,\mathrm{in}} = -\sqrt{-2g(z - h_{\mathrm{table}}) + v_z^2}
$$
  
其中 $z$ 为当前球高度，$h_{\mathrm{table}}$ 为球台高度，$v_z$ 为当前垂直速度，$g$ 为重力加速度。

**（Eq 2）反弹后垂直速度**  

$$
v_{z,\mathrm{out}} = -e \cdot v_{z,\mathrm{in}}
$$
  
$e$ 为恢复系数，用于表征碰撞过程中的能量损失。结合水平匀速假设即可闭合轨迹，推算出击球时刻的预期位置。然而，该纯物理模型忽视旋转、空气动力等真实因素，导致系统1单独使用时整体 MAE 高达 44.13 mm（Table 1），在消融实验中仅与 IMPACT 搭配时单目标回球成功率仅 23%（Table 7）。

### 系统2：面向脉冲相机的神经校准器（System 2 – Neural Calibrator）
为解决系统1的偏差，设计一个基于 Transformer 的神经校准网络，仅在训练阶段利用高频脉冲相机（20,000 fps）捕获的无运动模糊图像提供精确的击球位置标签。部署时系统2只接收系统1输出的轨迹序列，模型本身十分轻量，推理时间可忽略不计（包含在总 0.407 ms 内）。

系统2的输入包括轨迹上的位置 $p_i$、速度 $v_i$ 和高度 $h_i$，输出偏差向量 $\hat{D}_i$，通过最小化与真实接触点偏差的 MSE 损失进行训练：

**（Eq 3）系统2的 MSE 训练损失**  

$$
L_{\mathrm{MSE}}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \|\hat{D}_i - D_i\|^2,\quad \hat{D}_i = f_{\theta}([p_i, v_i, h_i])
$$
  
其中 $D_i$ 为脉冲相机标注的真实偏差向量。经过校准后，快-慢系统联合预测的整体 MAE 降至 12.34 mm，较纯物理模型降低 72.1%（Table 1）。消融研究进一步显示，移去系统2（仅保留系统1+IMPACT）会导致单目标回球成功率从 92% 骤跌至 23%，直接证明神经校准对精度的决定性作用（Table 7）。

### IMPACT：模仿式运动规划与控制技术（Imitation-based Motion Planning And Control Technology）
在预测出击球位置后，系统需要将轨迹信号转换为能精准打向指定落点的关节动作。IMPACT 模块采用 Transformer 网络处理三种模态：球轨迹序列、当前机器人关节构型 $j_i$ 以及目标落区控制信号 $c_i$，输出关节调整量 $\hat{J}_i$。训练数据通过向三个关键关节施加随机角度摄动并只保留成功回球至对方半台的试验获得，从而使策略具备多样性。

**（Eq 4）IMPACT 的 MSE 训练损失**  

$$
L_{\mathrm{MSE}}(\theta') = \frac{1}{N}\sum_{i=1}^{N} \|\hat{J}_i - J_i\|^2,\quad \hat{J}_i = f_{\theta'}([p_i, v_i, j_i, c_i])
$$
  
$J_i$ 为示教示范中的真实关节调整量。配合低推理延迟（0.407 ms），IMPACT 在 30 cm 精度的单目标回球中实现 92% 成功率，超出人类业余爱好者 39 个百分点，且远超 ACT、Diffusion Policy 等基线方法（Table 3）。

### 多频控制框架
上述三个核心模块运行在不同频率层级上：系统1与系统2的快-慢网络以 60 Hz 进行轨迹预测，IMPACT 以 2.4 kHz 实时生成关节命令，并通过 ABB 的 EGM 协议以 250 Hz 与机器人控制器通信（Figure 3）。该分层频率设计保证了感知-规划-控制的整体低延迟与高精度。

> **注**：文中所列所有公式均直接源自原始论文，变量含义已根据资料进行明确，未进行任何推断或猜测。



## 实验与关键发现

SpikePingpong 系统的实验围绕三个核心能力展开：接触点预测精度、实时推理效率与策略打击成功率。通过快‑慢感知架构与 IMPACT 模仿学习模块的协同，实验验证了双系统设计在高速动态驱动任务中的因果作用：系统 1 提供毫秒级物理预测，系统 2 利用脉冲相机数据训练 Transformer 校准偏差，IMPACT 则将校准后的轨迹映射为关节命令，实现极高精度与低延迟的统一。

**接触点预测精度**：Table 1 定量对比了球拍接触点偏差的 MAE 与 RMSE。纯物理模型 (System 1 Only) 整体 MAE 高达 44.13 mm，RNN 基线降至 22.80 mm，而快‑慢系统 (System 1+System 2) 仅 12.34 mm，相对物理模型提升 **72.1%**，相对 RNN 提升 **45.9%**（置信度 1.0）。Y 轴方向 MAE 降至 9.87 mm，这表明神经校准器 (System 2) 能有效学习物理模型在空气阻力、球体变形等未建模因素下产生的偏差。Figure 4 以脉冲相机记录的接触时刻图像直观展示了这一效果：未经校准的球拍中心 (红色) 与球心 (绿色) 偏移显著，而快‑慢系统显著缩小了该偏移。

![[assets/figures/papers/iclr26_0013_d08yOXs1Dl_SpikePingpong_Spike_Vision-based_Fast-Slow_Pingp/figures/005_Table_1.jpg]]
*Table 1: Ball Hittable Position Prediction Error. Our Fast-Slow system approach achieves superior precision in predicting the actual ball-racket contact point across both axes*

**推理延迟**：部署阶段仅依赖 RGB‑D 相机与轻量检测网络，配合极简的 Transformer 校准器。Table 2 显示 SpikePingpong 的单次动作推理仅需 **0.407 ms**，较扩散策略 (25.18 ms) 快约 61.8 倍，较 ACT (7.15 ms) 快约 17.6 倍（置信度 1.0）。这一速度优势源于推理路径中规避了重参数化迭代或大模型 rollout，证明了快‑慢架构在实时控制中的可行性。

![[assets/figures/papers/iclr26_0013_d08yOXs1Dl_SpikePingpong_Spike_Vision-based_Fast-Slow_Pingp/figures/006_Table_2.jpg]]
*Table 2: Computational Performance Comparison. Average inference times in milliseconds for generating return actions across different methods*

**策略打击成功率**：在 30 cm 半径目标区域内，SpikePingpong 的平均回球成功率高达 **92%**，大幅超越业余人类玩家 (53%) 和其他机器人系统 (扩散策略 3‑6%，ACT 12‑19%)（Table 3，置信度 1.0）。当精度要求提升至 20 cm 区域，系统仍保持 70% 成功率，人类降至 33%，其他方法不足 7%。连续目标执行场景 (Table 4) 中，系统整体成功率 78%，人类为 45%，显示 IMPACT 模块能稳定地将轨迹特征与目标落点映射为关节指令的精度保持能力。在极端超高精度任务（10 cm 目标）中，SpikePingpong 取得 31±3% 的成功率，相比 HYSR 基线 (8%) 提升 23 个百分点（Table 8，置信度 1.0），但仍处于较低水平，说明在毫米级控制上的挑战。

![[assets/figures/papers/iclr26_0013_d08yOXs1Dl_SpikePingpong_Spike_Vision-based_Fast-Slow_Pingp/figures/007_Table_3.jpg]]
*Table 3: Single-Target Return Accuracy (%). Success rates for ball striking across four distinct target regions (A-D) at both 30cm and 20cm precision thresholds. The table compares human players, previous robotic approaches, and our SpikePingpong system. Higher percentages indicate better performance. Standard deviations are denoted in subscripts*

**消融实验**：Table 7 揭示了各模块的因果贡献（置信度 1.0）。移除系统 2 仅保留系统 1+IMPACT，30 cm 成功率从 92% 骤降至 23%，证明神经校准对精度的决定性作用。若将系统 2 替换为 RNN (RNN+IMPACT)，成功率降至 67%，连续执行整体成功率从 78% 降至 52%，表明 Transformer 对偏差建模的容量优于 RNN。此外，EMA 滤波对观测稳定性的影响通过 Figure 7 可视化：滤波后轨迹 (蓝色) 平滑地保留抛物线特征，而原始检测数据 (红色) 存在高频抖动，这为物理模型提供了更可靠的输入（置信度 0.8）。滤波公式  
$$
\hat{x}_{t} = (1-\alpha) \cdot f(\hat{x}_{t-1}) + \alpha \cdot z_{t}
$$
将动力学预测与实时观测融合，是系统 1 快速估算的关键。

![[assets/figures/papers/iclr26_0013_d08yOXs1Dl_SpikePingpong_Spike_Vision-based_Fast-Slow_Pingp/figures/011_Table_7.jpg]]
*Table 7: Ablation Study (%). Performance comparison of different trajectory prediction components in our SpikePingpong system across two distinct tasks*

**泛化与失败模式**：Table 5 显示系统在分布外轨迹上的 30 cm 成功率从 92% 降至 74%，20 cm 成功率从 70% 降至 52%，说明训练集主要覆盖发球机模式，对极端旋转和速度变化的泛化有限。Table 6 进一步表明，面向未见人类玩家的泛化能力明显下降（30 cm 平均成功率 47% → 31%），这约束了系统直接对战的适应性。失败类型分布 (Table 9) 虽未提供详细数值，但配合文档已知旋转未被显式建模、空气阻力简化为恢复系数，当球速高且带有强烈旋转时，轨迹预测偏差放大，导致接触点失准。此外，超高精度任务中仍有 69% 的失败率，表明系统尚未能在竞技级别中可靠使用。

**关键视觉证据**：Figure 5 对比了传统 RGB 相机 (60 fps) 严重的运动模糊与脉冲相机 (20 k fps) 的清晰影像，直观说明了高帧率高精度标注对系统 2 训练的关键意义——只有无模糊的真实接触点才能训练出有效的误差校准器。Figure 7 则从轨迹级验证了滤波平滑性对跨模块信息传递的提质作用。

综上，实验证据一致支持快‑慢架构与 IMPACT 模仿学习的协同优势，同时也明确指出了旋转建模缺失、分布外退化、超高精度不足等瓶颈，为后续研究提供了改进方向。



## 定位与知识库关联

**与基线方法的关系**。SpikePingpong 在乒乓球机器人任务中同时追求高拦截精度、低延迟与可控落点，直接对标三类基线：(1) 基于纯物理弹道模型的预测方案（System 1 Only），其整体 MAE 高达 44.13 mm（Table 1）；(2) 以 RNN 为代表的轨迹学习基线，MAE 为 22.80 mm；(3) 端到端模仿学习策略，如 Diffusion Policy 和 ACT，其推理延迟分别为 25.18 ms 和 7.15 ms（Table 2），且在 30 cm 精度区域的单目标回球成功率仅 3‑6% 和 12‑19%（Table 3）。SpikePingpong 通过“快慢”双系统架构将球拍接触点预测 MAE 压缩至 12.34 mm（相对纯物理模型下降 72.1%，相对 RNN 下降 45.9%），同时保持 0.407 ms 推理延迟（比 Diffusion Policy 快约 61.8 倍，比 ACT 快约 17.6 倍），在相同 30 cm 目标区实现 92% 单次回球成功率（Table 3）和 78% 序列执行成功率（Table 4），全面超越人类业余玩家（53%）及历史机器人基准（如 HYSR 的 8% 在 10 cm 区，Table 8）。

与近期模仿学习方法的对比揭示了更深层的差异：Diffusion Policy 和 ACT 虽能学习复杂的输出分布，但在拦截乒乓球这一硬实时任务中必须承受长推理链或 Transformer 的计算开销，导致难以在高帧率下闭环运行；而 SpikePingpong 将高成本的计算（脉冲相机监督下的神经校准、模仿学习训练）全部放在离线阶段，部署时仅需轻量物理预测加一次 Transformer 前向传播（0.407 ms），从而在保持精度与策略灵活性的同时解除延迟瓶颈。这就是该工作在方法论谱系中的核心定位：**借鉴认知科学中双系统理论（快速直觉系统 1 与慢速审慎系统 2），把高频脉冲数据仅用于训练阶段去纠正物理模型的偏差，让部署端的“快慢融合”既能利用物理模型的实时性，又能继承神经网络的校正能力。** 与之配套的 IMPACT 模仿学习模块则进一步将轨迹、关节构型和目标落区映射为关节调整量，实现策略性落点控制，其训练标签来自真实机器人的随机扰动成功回球样本，避免了模拟到现实的迁移问题。

**适用边界**。现有测试主要在受控发球机产生的特定轨迹分布下进行。当测试分布偏离训练分布时，30 cm 精度区的成功率从 92% 降至 74%（Table 5），显示分布外泛化存在明显退化。对人类玩家的适应同样有限：经同一演示者微调后 30 cm 平均成功率仅为 47%，对未见过的玩家零样本转移则进一步降至 31%（Table 6）。同时，对超高精度（10 cm 目标区）的成功率仅为约 31%（Table 8），远不足以应对正式比赛中对手腕精确落点的要求；失败案例类型分析（Table 9）表明，系统在接近目标边界时的微小偏差即会导致脱靶。因此，该方法最适合的是**以固定发球模式、中等精度要求（≥30 cm）为特征的实时拦截与基础落点控制场景**，尚不能直接泛化至包含多类型旋转、复杂战术与多变对手的人类比赛环境。

**局限与开放问题**。首要局限是**物理模型和神经校准均未显式建模球体旋转（Magnus 效应）与空气阻力**，这在对旋转强烈的回球进行轨迹预测时成为主要误差源。系统对人类玩家的泛化能力受限于演示数据规模和动作多样性，且训练数据依赖特定发球机，使得面对极端轨迹、擦网球等长尾情况时鲁棒性不足。从架构角度看，IMPACT 模块采用单一前向模型输出关节调整量，缺乏对手意图推理或在线适应能力，难以实现类似人类的多拍战术调整。未来工作可沿着以下方向展开：(1) 将旋转和空气动力学项系统地嵌入系统 1 的物理模型及系统 2 的神经校准器中；(2) 引入在线自适应组件，利用最近几拍的观测更新对当前来球分布的估计，提升分布外泛化；(3) 设计高层战术规划器，构建多拍策略；以及(4) 利用脉冲相机提供的高达 20kHz 的时间分辨率，学习更精细的接触点动力学，推动超高精度目标（≤10 cm）成为现实。这些方向将决定 SpikePingpong 能否从高成功率的“固定靶”系统演进为在开放对抗中具备真正竞争力的人机互动平台。



## 原文 PDF

![[paperPDFs/ICLR_2026/SpikePingpong_Spike_Vision_based_Fast_Slow_Pingpong_Robot_System.pdf]]

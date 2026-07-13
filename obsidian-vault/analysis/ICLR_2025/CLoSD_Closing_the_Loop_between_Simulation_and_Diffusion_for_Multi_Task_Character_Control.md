---
title: CLoSD Closing the Loop between Simulation and Diffusion for Multi Task Character Control
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_Character_Control.pdf
project_link: https://guytevet.github.io/CLoSD-page/
code_link: null
aliases:
- CCLBSDMTCC
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入一个实时自回归扩散规划器（DiP），并通过闭环反馈将规划器与物理跟踪控制器耦合，从而让运动扩散作为在线通用规划器，支持文本指令与目标位置。
primary_logic: 运动扩散模型可以作为RL物理控制器的实时通用规划器，通过闭环交互实现文本驱动和物体交互的多任务控制。
claims:
- CLoSD maintains a closed-loop interaction between two modules — a Diffusion Planner (DiP), and a tracking controller.
- Our key insight is that motion diffusion, given textual instruction and a target location, can serve as a versatile kinematic motion planner.
- HumanML3D 上 R-precision Top1 ↑ = 0.381
- PhysDiff 上 Penetration (mm) ↓ = 0.022
---

# CLoSD Closing the Loop between Simulation and Diffusion for Multi Task Character Control

> [!tip] 核心洞察
> 运动扩散模型可以作为RL物理控制器的实时通用规划器，通过闭环交互实现文本驱动和物体交互的多任务控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLoSD：闭合仿真与扩散模型循环的多任务角色控制 |
| 英文题名 | CLoSD Closing the Loop between Simulation and Diffusion for Multi Task Character Control |
| 会议/期刊 | ICLR 2025 |
| Links | [Project](https://guytevet.github.io/CLoSD-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CLoSD |
| Dataset | HumanML3D, PhysDiff |

> [!tip] 效果简介
> - HumanML3D 上，R-precision Top1 ↑ 0.381 vs 0.309 (MoConVQ) (+0.072)。
> - PhysDiff 上，Penetration (mm) ↓ 0.022 vs 0.147 (MDM2023) (-0.125)。

## 概要

**问题瓶颈**：现有运动扩散模型（如 **MDM**，Tevet et al., ICLR 2023）主要用于离线生成，推理速度慢且缺乏环境感知，无法直接用于物理仿真中的在线物体交互与多任务控制；而纯强化学习控制器（如 **MoConVQ**，Yao et al., TOG 2024；**UniHSI**，Xiao et al., ICLR 2024）难以结合自然语言指令和物体交互。

**核心洞察**：运动扩散模型可以作为 RL 物理控制器的实时通用规划器，通过闭环交互实现文本驱动和物体交互的多任务控制。

**方法定位**：CLoSD 提出了一种**闭环规划-执行**系统，包含两个核心模块：
- **Diffusion Planner (DiP)**：实时自回归扩散规划器，仅需 10 步扩散即可生成运动计划，速度达 3500 fps（175 倍实时），支持文本提示和目标位置作为条件输入。
- **RL Tracking Controller**：基于 **PHC**（Luo et al., ICCV 2023）的物理仿真跟踪控制器，在闭环中对多任务交互进行微调，执行运动计划并产生仿真状态反馈。

两者通过闭环反馈耦合：执行的运动作为前缀反馈给 DiP，使扩散规划器能够对环境变化做出实时反应。一个简单的状态机检测任务完成并动态切换文本提示和目标，实现多任务序列。

**主要结果**：
- 在 HumanML3D 文本到运动基准上，CLoSD 的 R-precision Top1 达到 0.381，显著优于 MoConVQ（0.309）。
- 在 PhysDiff 物理合理性指标上，穿透深度（Penetration）降至 0.022 mm，远低于 MDM 的 0.147 mm。
- 在物体交互任务（如击打、起立）上，成功率显著优于现有方法。

**局限与展望**：当前方法仅依赖目标位置作为空间条件，缺乏视觉感知能力；规划范围限于约 2 秒的短期运动；缺乏自适应时间尺度的闭环机制。未来方向包括引入外感受（视觉/高度图）、扩展长期规划能力、以及设计时间自适应循环。

让虚拟角色在物理仿真环境中根据自然语言指令执行复杂的物体交互任务，是计算机动画与具身智能交叉领域的长期目标。这一目标的实现需要同时解决两个核心问题：**运动生成的自然性**与**物理交互的可行性**。然而，当前的主流方法在这两个维度上呈现出明显的割裂。

在运动生成侧，基于扩散的文本到运动模型（如 **MDM**，Tevet et al., ICLR 2023）在离线生成高质量运动序列方面取得了显著进展，但存在两个根本性局限：其一，生成过程计算开销大、速度慢，难以满足实时交互需求；其二，这些模型本质上是**开环**的——它们一次性生成完整运动序列，缺乏对物理环境反馈的感知与响应能力，无法在线修正因碰撞、滑移等物理扰动导致的偏差。

在物理控制侧，基于强化学习的运动跟踪策略（如 **PHC**，Luo et al., ICCV 2023）虽然能够稳健地跟踪参考运动，但通常需要预先提供完整的运动轨迹，且难以直接融合自然语言指令和空间目标。现有工作如 **UniHSI**（Xiao et al., ICLR 2024）尝试统一多任务物体交互控制，但其设计思路是最小化接触点距离，往往产生不符合人体运动学自然性的行为（如直接抬起骨盆而非从沙发上站起）。**MoConVQ**（Yao et al., TOG 2024）作为当前领先的文本到运动控制器，也面临类似的物理真实感瓶颈。

一个更深层的瓶颈在于：**运动扩散模型与物理控制器之间缺乏有效的闭环耦合机制**。扩散模型擅长规划“应该做什么”，物理控制器擅长执行“如何做到”，但二者若以开环方式串联，则物理执行中累积的误差无法反馈给规划器进行修正，导致在需要精确物体交互的任务（如击打目标、从家具上起身）中频繁失败。

CLoSD 的核心洞察正是针对这一缺口：**运动扩散模型可以作为强化学习物理控制器的实时通用规划器**，通过闭环交互实现文本驱动和物体交互的多任务控制。其设计目标不是简单地堆叠生成与控制模块，而是构建一个“规划—执行—反馈”的闭合回路，使扩散规划器能够根据物理执行的实际结果进行自回归重规划，从而在保持运动自然性的同时，获得对物理环境的适应能力。

## 核心方法与创新机理

CLoSD 的核心创新在于将**运动扩散模型重新定位为物理仿真控制器的实时通用规划器**，并通过**闭环反馈机制**弥合了数据驱动的运动生成与基于物理的角色控制之间的鸿沟。这一范式转变通过以下关键模块的协同设计实现：

### 1. 从离线生成到在线闭环规划

现有运动扩散模型（如 **MDM** (Tevet et al., ICLR 2023)）通常用于离线生成，速度慢且缺乏环境感知，无法直接用于物理仿真中的在线物体交互与多任务控制。CLoSD 的根本突破在于引入**实时自回归扩散规划器 DiP**，仅需 10 步扩散即可生成高质量运动计划，推理速度达到 3500 fps（175 倍实时），使扩散模型首次能够作为在线通用规划器运行。

更重要的是，CLoSD 建立了**规划-执行闭环**：DiP 生成的运动计划由基于 **PHC** (Luo et al., ICCV 2023) 的 RL 跟踪控制器执行，执行后的实际运动状态作为前缀反馈给 DiP，使其能够感知物理环境的变化并进行自适应重规划。这种闭环设计是 CLoSD 区别于开环扩散方法的关键，使其能够处理物体交互中不可避免的物理扰动和接触动力学。

### 2. 多模态条件输入的统一

CLoSD 将文本提示和目标空间位置统一作为 DiP 的条件输入，使控制器能够同时响应自然语言指令和空间目标。具体而言，DiP 接受文本嵌入和由关节目标位置 $c_j$ 及朝向角 $c_\theta$ 构成的空间条件，并通过专门设计的**目标损失** $\mathcal{L}_{\mathrm{target}}$ 确保预测运动的最后一帧到达指定目标：

$$\mathcal{L}_{\mathrm{target}} = \sum_{j \in J} v_j || R2G(\hat{x}_0[N_g])_j - c_j ||_2^2 + v_\theta || R2G(\hat{x}_0[N_g])_\theta \ominus c_\theta ||_2^2$$

其中 $R2G$ 将 HumanML3D 相对表示转换为全局坐标，$v_j$ 和 $v_\theta$ 为有效性信号。这种设计使 CLoSD 能够在线更改文本和目标，实现流畅的多任务切换。

### 3. 闭环微调策略

与直接使用预训练跟踪策略不同，CLoSD 在闭环中针对多任务交互**微调 RL 策略**。微调过程中固定 DiP，每个 episode 随机选择任务并设置相应的物体、文本提示和目标位置，使用原始 PHC 的奖励和重置条件。这一策略使跟踪控制器能够适应 DiP 的规划特性，显著提升了需要精细物体交互的任务（如起立和击打）的成功率。

### 与现有方法的本质区别

| 维度 | 现有方法 | CLoSD |
|------|---------|-------|
| 规划方式 | 离线扩散生成（无反馈） | 实时自回归扩散（闭环反馈） |
| 条件输入 | 仅文本或无目标 | 文本 + 目标关节位置 + 朝向角 |
| 环境感知 | 开环，无物理反馈 | 闭环，执行状态作为前缀反馈 |
| 策略训练 | 离线预训练 | 闭环中针对多任务微调 |
| 任务切换 | 单一任务 | 通过状态机在线切换文本和目标 |

这种设计使 CLoSD 在保持文本到运动生成质量的同时，具备了物理仿真中的实时交互能力和多任务泛化性，超越了当前领先的文本到运动控制器 **MoConVQ** (Yao et al., TOG 2024) 和多任务物体交互控制器 **UniHSI** (Xiao et al., ICLR 2024)。

CLoSD 的整体设计围绕一个核心洞察展开：**运动扩散模型可以作为强化学习物理控制器的实时通用规划器**，通过闭环交互实现文本驱动和物体交互的多任务控制。系统由两个关键模块构成闭环回路——**Diffusion Planner (DiP)** 和基于物理的 **RL 跟踪控制器**（图 2）。

### 闭环规划-执行回路

CLoSD 维护着 DiP 与跟踪控制器之间的闭环交互。DiP 是一个快速响应的自回归扩散模型，以文本提示和目标位置为条件，实时生成运动计划 $x^{\mathrm{pred}}$。该计划随后由鲁棒的运动跟踪控制器执行，在物理仿真环境中产生实际的运动轨迹。关键创新在于：**执行后的运动帧被作为前缀 $x^{\mathrm{prefix}}$ 反馈给 DiP**，使扩散规划器能够感知环境反馈并据此重新规划，形成一个持续的规划-执行循环。

这一闭环机制从根本上改变了扩散模型在角色控制中的角色——从离线生成器转变为在线通用规划器。DiP 仅需 **10 步扩散**即可生成 40 帧运动计划，在单张 NVIDIA RTX 3090 上达到 **3500 fps**（约 175 倍实时），满足了物理仿真的实时性要求。

### 条件输入与任务切换

DiP 接受两类条件输入：**文本提示**（描述期望的运动类型，如“坐在沙发上”）和**目标位置**（指定关节在全局坐标系中的目标位置和朝向角）。这些条件可以在线更改，使角色能够动态响应新的指令。

高层任务调度由一个简单的**状态机**（State Machine）负责。每个任务在完成时发出“done”信号，状态机据此切换文本提示和目标位置，实现多任务序列的无缝衔接。任务转换可由用户交互式指定，也可由状态机自动随机选择下一任务。

### 表示转换层

由于 DiP 工作在 HumanML3D 的相对运动表示空间，而跟踪控制器需要 PHC 的全局物理状态表示，CLoSD 引入了两个转换函数：**R2G**（Relative-to-Global）和 **G2R**（Global-to-Relative），在两种表示之间进行双向映射，确保规划器与控制器的信息流通畅。

### 训练与微调策略

跟踪控制器基于 **PHC**（Luo et al., ICCV 2023）通用运动跟踪策略进行初始化，随后在闭环中针对多任务物体交互进行微调。微调阶段固定 DiP 参数，使用 PPO 算法，每个 episode 随机选择一个任务并设置相应的物体、文本提示和目标位置，同时保留原始 PHC 的奖励函数和重置条件。这一闭环微调策略使控制器能够适应 DiP 的规划分布，显著提升了文本到运动的生成质量和任务成功率。

![[assets/figures/papers/paper_list_l1900_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_C/figures/002_Figure_2.jpg]]
*Figure 2: CLoSD Overview. (Left) DiP is a rapid auto-regressive diffusion model conditioned on a text prompt and a Target location. It generates the motion plan*

### 系统闭环架构

CLoSD 由两个核心模块构成闭环交互系统：**扩散规划器（Diffusion Planner, DiP）** 和 **强化学习跟踪控制器**。DiP 是一个实时自回归扩散模型，接收文本提示与目标位置作为条件输入，生成运动计划 $x^{\mathrm{pred}}$；跟踪控制器（基于 PHC 策略）在物理仿真中执行该计划，并将实际执行的运动帧作为前缀 $x^{\mathrm{prefix}}$ 反馈给 DiP，形成规划-执行的闭环回路。这一设计使运动扩散模型从离线生成器转变为在线通用规划器，能够对环境反馈做出实时响应。

### 扩散规划器（DiP）

DiP 的核心设计目标是实现高速自回归运动生成。训练时，从数据集中采样（运动，文本）对，将运动裁剪为长度 $N_p + N_g$，前 $N_p$ 帧作为已知前缀，后 $N_g$ 帧作为待预测部分。对预测部分按随机时间步 $t \sim \mathcal{U}[0, T]$ 加噪，模型学习从噪声中恢复干净运动。推理时，DiP 仅需 **10 步扩散**即可生成 $N_g = 40$ 帧运动计划，在单张 NVIDIA RTX 3090 上达到 **3500 fps**（约 175 倍实时），前缀长度设为 $N_p = 20$。

### 关键公式

**DDPM 加噪过程**（Section 3）：

$$q(x_t | x_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}, (1 - \alpha_t) I)$$

该公式描述标准 DDPM 的马尔可夫前向加噪过程，将干净运动 $x_0$ 逐步加噪至 $x_T$。$\alpha_t$ 为噪声调度参数。

**简单损失函数**（Section 3）：

$$\mathcal{L}_{\mathrm{simple}} = E_{x_0 \sim p(x_0|c), t \sim [1,T]}[\|x_0 - \hat{x}_0\|_2^2]$$

直接预测干净运动 $x_0$ 而非噪声 $\epsilon$，便于后续施加几何约束损失。$c$ 为条件信息（文本提示与目标位置）。

**目标损失**（Section 4.1）：

$$\mathcal{L}_{\mathrm{target}} = \sum_{j \in J} v_j ||R2G(\hat{x}_0[N_g])_j - c_j||_2^2 + v_\theta ||R2G(\hat{x}_0[N_g])_\theta \ominus c_\theta||_2^2$$

该损失确保预测序列最后一帧 $\hat{x}_0[N_g]$ 的全局关节位置与朝向角逼近给定目标。其中 $R2G$ 为 HumanML3D 相对表示到 PHC 全局表示的转换函数，$J$ 为目标关节集合，$c_j$ 和 $c_\theta$ 分别为目标关节位置与朝向角，$v_j$、$v_\theta$ 为有效性指示信号，$\ominus$ 表示角度差运算。

**总训练损失**（Section 4.1）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{target}}^{-} \mathcal{L}_{\mathrm{target}}$$

将简单扩散损失与加权目标损失联合优化，使 DiP 在保持运动自然度的同时满足空间目标约束。

### 跟踪控制器与微调

跟踪控制器基于 **PHC**（Luo et al., ICCV 2023）通用运动跟踪策略。在闭环微调阶段，固定 DiP 参数，使用 PPO 对 PHC 策略进行多任务交互训练——每回合随机选择任务并设置对应物体、文本提示和目标位置，沿用原始 PHC 的奖励函数与重置条件。微调后的策略能够更好地适应 DiP 生成的规划与物理环境的交互需求。

### 状态机与任务切换

高层任务调度由一个简单状态机实现。每个任务完成时发出完成信号，状态机据此切换文本提示与目标位置，实现在线多任务序列执行。任务可随机选择或按预设流程自动过渡。

## 实验与关键发现

### 核心实验设计

CLoSD 的实验评估围绕两个维度展开：**文本到运动的生成质量**和**物理仿真中的多任务交互成功率**。前者在 HumanML3D 基准（Guo et al., 2022）上评测，后者通过自定义的物体交互任务集（包括坐下、起立、击打等）进行定量比较。所有实验均在单张 NVIDIA GeForce RTX 3090 GPU 上完成，DiP 规划器以 10 步扩散、前缀长度 $N_p=20$、生成长度 $N_g=40$ 的配置运行，达到 3500 fps 的实时推理速度。

### 主要结果

**任务成功率。** Table 1 报告了 CLoSD 与当前领先方法的任务成功率对比。CLoSD 在需要精细物体交互的任务上表现突出：
- **击打（Striking）任务**：CLoSD 显著优于对比方法，体现了闭环规划器对目标位置和物理反馈的实时响应能力。
- **起立（Get-up）任务**：CLoSD 成功完成起立动作，而开环基线（open-loop baseline）因缺乏重规划能力完全无法与沙发交互；UniHSI（Xiao et al., ICLR 2024）仅最小化接触点距离，导致角色直接抬升骨盆而非从沙发自然起立（见 Figure 4 定性对比）。

![[assets/figures/papers/paper_list_l1900_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_C/figures/006_Figure_4.jpg]]
*Figure 4: Comparisons of the getup task. The pelvis target is marked in cyan. CLoSD is able to get up successfully with a human-like motion. Before fine-tuning on object interaction with the closed-loop, it was able to sit but struggled to get up. The open-loop baseline struggles with any interaction with the sofa due to the lack of re-planning. UniHSI (Xiao et al., 2024) was designed to minimize contact-point distance and thus lifts the pelvis instead of getting up from the sofa*

**文本到运动质量。** Table 3 展示了 HumanML3D 基准上的关键指标：
- **R-precision Top1**：CLoSD 达到 0.381，较当前领先的文本到运动控制器 MoConVQ（Yao et al., TOG 2024）的 0.309 提升了 +0.072，表明文本-运动语义对齐更强。
- **物理合理性**：在 PhysDiff 指标（Yuan et al., 2023）上，CLoSD 的穿透深度（Penetration）仅为 0.022 mm，远低于 MDM（Tevet et al., ICLR 2023）的 0.147 mm，降幅达 0.125 mm。这验证了闭环物理跟踪对消除脚部滑动和身体穿透的有效性。

### 消融研究

**扩散步数的影响。** Table 2 的 DiP 消融实验揭示了一个关键发现：**仅需 10 步扩散即可生成高质量运动，甚至 5 步也能取得不错效果**。这一特性是 DiP 实现 3500 fps 实时推理的核心——通过预测干净运动 $x_0$ 而非噪声 $\epsilon$ 的简单目标函数 $\mathcal{L}_{\mathrm{simple}}$，模型在极短扩散链上仍能保持运动保真度。

**闭环微调的作用。** 在物体交互任务上，未经闭环微调的模型能够完成坐下但无法起立（Figure 4）。闭环微调通过将 DiP 固定、用 PPO 在随机任务上微调 PHC 跟踪策略，使控制器学会适应 DiP 生成的运动分布与物理环境之间的差异，从而在起立等复杂交互上取得成功。

### 失败模式与局限

尽管 CLoSD 在核心任务上表现优异，分析揭示了三个结构性局限：

1. **空间条件单一**：DiP 仅依赖目标关节位置和朝向角作为空间条件，缺乏视觉感知等外部感受能力。这意味着当前方法无法处理非关节目标（如移动物体）或需要场景理解的复杂任务。

2. **规划视野受限**：当前配置的 $N_g=40$ 帧约对应 2 秒的运动规划。对于需要长期策略的任务（如多房间导航），这一中短期范围可能不足。

3. **时间尺度刚性**：闭环以固定频率运行，缺乏自适应时间尺度机制。这导致系统难以同时适应快速动作（需要高频重规划）和慢速动作（长跟踪 horizon 可减少伪影），可能在某些运动节奏下产生不自然的过渡。

### 图表核心结论

- **Figure 2** 展示了 CLoSD 的闭环架构：DiP 作为自回归扩散规划器生成运动计划 $x^{\mathrm{pred}}$，RL 跟踪控制器执行后，将实际运动帧作为前缀反馈给 DiP，形成规划-执行闭环。
- **Figure 3** 展示了 CLoSD 生成的多样化文本驱动运动，以及通过状态机（State Machine）实现的多任务序列切换——任务完成信号触发文本提示和目标位置的在线切换。
- **Figure 4** 的起立定性对比直观展示了闭环微调的必要性：微调后 CLoSD 能以类人方式从沙发起立，而未微调版本和开环基线均失败。
- **Table 3** 同时报告了 Diversity 指标，显示 CLoSD 的运动多样性更接近真实数据分布，避免了模式坍塌。

![[assets/figures/papers/paper_list_l1900_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_C/figures/007_Table_3.jpg]]
*Table 3: Text-to-motion on the HumanML3D benchmark (Guo et al., 2022), alongside the PhysDiff metrics (Yuan et al., 2023), which evaluate aspects of physical correctness. Diversity values closer to the ground truth are preferred*

![[assets/figures/papers/paper_list_l1900_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_C/figures/003_Figure_3.jpg]]
*Figure 3: (Left) CLoSD generates versatile text-prompted physics-based motions. The SMPLcompatible physics model is rendered with the SMPL mesh. (Right) CLoSD can perform a sequence of RL tasks (see the web page video). Task transitions are user-specified via interactively changing the text, or via a state machine, with transitions on a task done signal*

![[assets/figures/papers/paper_list_l1900_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_C/figures/004_Table_1.jpg]]
*Table 1: Task success rates. Bold and underscore relate to multi-task only. CLoSD significantly excels on Striking and Get-up, which require careful object interaction*

![[assets/figures/papers/paper_list_l1900_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_C/figures/005_Table_2.jpg]]
*Table 2: DiP ablation study. We use DiP with prefix length*

## 定位与知识库关联

### 核心瓶颈与因果机制

现有运动扩散模型（如 **MDM** (Tevet et al., ICLR 2023)）主要用于离线生成，速度慢且缺乏环境感知，无法直接用于物理仿真中的在线物体交互与多任务控制；而纯RL控制器（如 **UniHSI** (Xiao et al., ICLR 2024)）难以结合自然语言指令和物体交互。CLoSD 的核心洞察在于：运动扩散模型可以作为 RL 物理控制器的实时通用规划器，通过闭环交互实现文本驱动和物体交互的多任务控制。

因果旋钮是引入一个实时自回归扩散规划器（DiP），并通过闭环反馈将规划器与物理跟踪控制器耦合。具体而言，CLoSD 维持两个模块之间的闭环交互——扩散规划器（DiP）和跟踪控制器——执行后的运动作为前缀自回归地反馈给扩散模型，使 DiP 能够对物理环境做出反应。

### 与基线工作的关系

**运动生成与物理控制融合**：CLoSD 区别于纯运动扩散模型（如 MDM），后者仅输出运动学序列，缺乏物理约束和交互能力。与 **MoConVQ** (Yao et al., TOG 2024)——当前领先的文本到运动控制器——相比，CLoSD 将运动生成从离线推向在线闭环控制。与 **PHC** (Luo et al., ICCV 2023) 这一通用运动跟踪策略相比，CLoSD 将其从被动跟踪器升级为主动闭环规划-执行系统。

**物体交互策略对比**：**UniHSI** (Xiao et al., ICLR 2024) 作为多任务物体交互控制器，通过最小化接触点距离来实现交互，但在起立任务中表现为“抬起骨盆”而非自然地从沙发站起（见 Figure 4 定性对比）。**PDP** (Truong et al., arXiv 2024) 基于扩散策略进行离线人物交互学习，但缺乏在线重规划能力。CLoSD 的闭环规划使其在需要精细物体交互的任务（如击打和起立）上显著优于这些方法（Table 1）。

### 方法适用边界

CLoSD 在以下条件下表现良好：
- 任务可通过文本提示和目标关节位置（骨盆及手部）明确指定
- 交互对象的位置和朝向可参数化为目标坐标
- 规划范围适合中短期（约2秒，40帧生成窗口）
- 角色模型为 SMPL 兼容的物理人体模型

当前方法不适用于：
- 需要视觉感知或高度图等外感受能力的复杂场景
- 非关节目标（如可变形物体、流体）的交互
- 需要超长时间规划（远超2秒）的任务序列
- 同时包含快速和慢速动作的混合节奏场景

### 已知局限与开放问题

论文明确指出的局限性包括：（1）仅依赖目标位置作为空间条件，缺乏视觉感知等外部感受能力；（2）规划范围限于短期（约2秒），对于需要长期规划的任务可能不够；（3）缺乏自适应时间尺度的闭环，难以同时适应快速和慢速动作。

由此衍生的开放问题包括：如何将外感受（如视觉或高度图）引入运动跟踪控制器和扩散规划器？如何处理更长时间尺度的规划，超越当前的中短期范围？如何引入时间自适应循环，以便更好地处理快速运动和更长的跟踪 horizon 以减少伪影？这些问题指向 CLoSD 方法向更通用、更鲁棒的物理角色控制发展的关键方向。

## 原文 PDF

![[paperPDFs/ICLR_2025/CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for_Multi_Task_Character_Control.pdf]]

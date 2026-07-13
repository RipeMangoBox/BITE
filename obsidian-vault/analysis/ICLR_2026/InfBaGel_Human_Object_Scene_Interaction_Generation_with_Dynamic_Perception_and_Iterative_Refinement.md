---
title: "InfBaGel: Human-Object-Scene Interaction Generation with Dynamic Perception and Iterative Refinement"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/InfBaGel_Human_Object_Scene_Interaction_Generation_with_Dynamic_Perception_and_I_ff1cfe7d66d2.pdf
project_link: null
code_link: null
aliases:
- InfBaGel
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 动态感知编码（Dynamic Perception Encoding）与一致性模型驱动的粗到细迭代生成（coarse-to-fine iterative refinement），是提升生成一致性与物理合理性的关键机制。
primary_logic: 利用一致性模型的少步生成能力，在去噪过程中动态更新场景体素状态以反映人/物运动带来的环境变化，进而通过轻量级碰撞引导在实时条件下实现一致的、未碰撞的人-物-场景交互。同时通过混合数据训练（合成HOI场景+真实HSI数据）缓解数据稀缺。
claims:
- 动态感知迭代使成功率从71.22%提升至86.35%
- 碰撞引导显著降低人-场景及物-场景穿透指标
- 一致性模型比扩散模型大幅提升速度，且迭代后交互质量全面提高
- HOSI Benchmark (469 sequences, 7 object categories, 67 unseen indoor scenes) 上 Success Rate (S%) = 83.16
---

# InfBaGel: Human-Object-Scene Interaction Generation with Dynamic Perception and Iterative Refinement

> [!tip] 核心洞察
> 利用一致性模型的少步生成能力，在去噪过程中动态更新场景体素状态以反映人/物运动带来的环境变化，进而通过轻量级碰撞引导在实时条件下实现一致的、未碰撞的人-物-场景交互。同时通过混合数据训练（合成HOI场景+真实HSI数据）缓解数据稀缺。

| 字段 | 内容 |
|------|------|
| 中文题名 | InfBaGel: 基于动态感知与迭代精炼的人-物-场景交互生成 |
| 英文题名 | InfBaGel: Human-Object-Scene Interaction Generation with Dynamic Perception and Iterative Refinement |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=TeyHNq4WlI) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InfBaGel |
| Dataset | HOSI Benchmark, HOI Dataset |

> [!tip] 效果简介
> - HOSI Benchmark (469 sequences, 7 object categories, 67 unseen indoor scenes) 上，Success Rate (S%) 83.16 vs 53.09 (LINGO) (+30.07)。
> - HOSI Benchmark 上，Foot Sliding (FS↓) 0.13 vs 0.57 (LINGO) (-0.44)；Human-Object Contact Percentage (C%↑) 78.18 vs 53.83 (LINGO) (+24.35)；Human-Scene Penetration Mean (P_mean↓) 3.39 vs 7.62 (LINGO) (-4.23)。
> - HOI Dataset (OMOMO) 上，FID↓ 0.68 (InfBaGel 16) vs 1.01 (CHOIS) (-0.33)。

## 概要

人-物-场景交互（Human-Object-Scene Interaction, HOSI）生成旨在根据文本指令与目标位置，在复杂三维场景中合成人与物体协同运动的连续序列。该任务面临两大核心瓶颈：（1）**动态场景变化**——人在移动物体过程中，场景上下文（如障碍物、可通行区域）持续改变，静态编码无法适应这种时变环境；（2）**数据稀缺**——高质量、带场景标注的HOSI数据极度匮乏，制约了模型的泛化能力。

针对上述问题，本文提出 **InfBaGel**，一个基于一致性模型（Consistency Model）的粗到细迭代精炼框架。其核心洞察在于：利用一致性模型的少步生成能力，在去噪过程中动态更新场景体素状态以反映人/物运动带来的环境变化，并通过轻量级碰撞引导在实时条件下实现一致的、无碰撞的交互生成。同时，通过混合合成HOI场景数据与真实HSI数据，缓解训练数据稀缺。

在方法论层面，InfBaGel 相对于现有工作做出了四项关键改变：

- **场景感知机制**：从静态一次性体素编码转变为**动态感知编码**（Dynamic Perception Encoding），根据前一迭代结果更新时变体素状态，为后续精炼提供与时间对齐的场景上下文。
- **采样引导**：从无引导或仅接触引导（Contact Guidance）升级为**碰撞感知引导**（Bump-aware Guidance），基于预计算体素距离图直接优化无碰撞性，在保持人-物交互质量的同时大幅降低穿透。
- **生成模型架构**：从扩散模型（DDPM量级步数）替换为**一致性模型**，少步采样即可直接输出干净样本，生成速度从3.38 FPS提升至28.75 FPS。
- **数据训练策略**：从单一数据集训练拓展为**混合数据训练**，联合合成HOI体素场景与真实HSI数据，实现对新场景的零样本泛化。

实验结果表明，InfBaGel 在HOSI基准测试（469个序列，67个未见室内场景，7类物体）上取得了最优性能：成功率（S%）达到83.16%，较最强基线LINGO（53.09%）提升30.07个百分点；人-场景穿透均值（P_mean↓）从7.62降至3.39；足部滑动（FS↓）从0.57降至0.13。消融实验证实，动态感知编码使成功率从71.22%提升至86.35%，碰撞引导在保持接触率的同时显著改善穿透指标，验证了迭代场景更新与碰撞感知引导的关键作用。

**局限与展望**：当前方法依赖简化体素表示，对精细交互（如抓取稳定性）的支持有限；碰撞引导采用统一距离惩罚，可能使运动趋于保守。未来方向包括将动态感知拓展到连续几何表示、自适应碰撞引导参数学习，以及与物理模拟器结合以进一步提升运动合理性。

### 问题域：人-物-场景交互生成

在具身智能与数字人应用中，生成自然、物理合理的人-物-场景交互（Human-Object-Scene Interaction, HOSI）运动序列是核心挑战之一。给定文本指令与目标位置，系统需要同时协调人体运动、物体操控以及场景约束，输出无碰撞、接触合理的长序列动作。这一任务横跨人体运动生成、场景感知与物体交互三个子领域，对生成模型的时空一致性与物理可行性提出了严苛要求。

### 现有方法的瓶颈

当前场景感知的运动生成方法存在两大核心瓶颈：

**瓶颈一：静态场景编码无法应对动态环境变化。** 现有方法（如 **TRUMANS** (Jiang et al., 2024b)、**LINGO** (Jiang et al., 2024a)）通常在生成前对场景进行一次性的体素编码，将其作为静态条件馈入生成模型。然而，在人物携带物体穿越场景的过程中，人物与物体的位置持续变化，局部场景上下文也随之更新——例如，人走过一张桌子后，桌子从“前方障碍”变为“后方无关区域”。静态编码无法捕捉这种时变的环境语义，导致生成的运动在长序列中逐渐偏离场景约束，产生穿透与不合理的路径规划。

**瓶颈二：高质量带场景标注的HOSI数据极度稀缺。** 真实场景中采集大规模、多样化的人-物-场景交互数据成本极高，现有数据集要么仅包含人-场景交互（HSI）而缺乏物体操控，要么仅包含人-物交互（HOI）而缺乏真实场景上下文。这种数据孤岛严重限制了模型在真实杂乱室内场景中的泛化能力。

### 本文的动机与核心思路

针对上述瓶颈，InfBaGel 提出以下核心思路：

1. **动态感知替代静态编码**：利用一致性模型（Consistency Model）的少步迭代采样特性，在去噪过程中根据前一迭代步生成的运动轨迹动态更新场景体素状态，使场景上下文与人/物运动保持时间对齐。这一“粗到细迭代精炼”（coarse-to-fine iterative refinement）机制是提升生成一致性与物理合理性的关键因果杠杆。

2. **碰撞感知引导替代无引导或简单接触引导**：基于预计算的距离图，在采样过程中直接优化无碰撞性，轻量级地将运动“推离”障碍物，无需额外的物理模拟器。

3. **混合数据训练缓解数据稀缺**：将合成场景的HOI数据（如OMOMO）与真实HSI数据（如LINGO）联合训练，使模型在零样本条件下泛化到未见过的真实场景。

4. **一致性模型替代扩散模型**：将扩散模型蒸馏为一致性模型，在保持生成质量的同时实现少步（16步）实时采样，为动态感知的迭代更新提供速度基础。

### 方法定位

InfBaGel 属于**运动学驱动的条件运动生成**范式，与基于物理模拟的方法正交。其设计哲学是：不依赖昂贵的在线物理仿真，而是通过学习的方式在运动学层面隐式编码场景约束与交互合理性，仅在必要时引入轻量级的几何引导。这一选择使其在实时性要求高的应用场景（如VR/AR、游戏角色动画）中具有实用优势。

## 核心方法与创新机理

InfBaGel 针对人-物-场景交互（HOSI）生成中的两个核心瓶颈——**动态对象-场景变化导致静态编码失效**与**高质量带场景标注数据极度稀缺**——提出了四项相互耦合的关键创新，构成一个完整的粗到细迭代精炼框架。

### 1. 动态感知编码（Dynamic Perception Encoding）

传统方法对场景上下文进行一次性静态体素编码，无法反映人/物在交互过程中位置变化带来的环境更新。InfBaGel 引入**时变体素状态**：在一致性模型的每次去噪迭代中，根据上一轮精炼得到的运动轨迹动态更新场景体素占用，使场景上下文与当前交互状态保持时间对齐。具体而言，动态体素在粗预测阶段被遮蔽，随着预测逐步精炼而迭代更新。这一设计将场景感知从“静态快照”转变为“动态演化”，是成功率从 71.22% 提升至 86.35% 的关键因素（Table 3，DP 启用 vs 禁用）。

### 2. 一致性模型驱动的粗到细迭代生成

基线方法普遍采用扩散模型（如 DDPM），需要数百至上千步采样，难以支撑实时交互生成。InfBaGel 将扩散模型蒸馏为**一致性模型（Consistency Model）**，利用其少步采样能力直接输出干净样本，并将迭代去噪过程显式对齐于粗到细的运动精炼。蒸馏损失（Eq. 1）最小化在线网络与目标网络在相邻 ODE 步输出之间的距离，训练总目标（Eq. 5）进一步加入人体关节位置损失（Eq. 3）与物体顶点损失（Eq. 4）作为辅助监督。这一架构切换使生成速度从 3.38 FPS 跃升至 28.75 FPS（Table 2），同时交互质量全面超越扩散模型基线。

### 3. 碰撞感知引导（Bump-aware Guidance）

现有方法或缺乏引导，或仅采用接触引导（Contact Guidance），无法有效避免人/物与场景的穿透。InfBaGel 提出**碰撞感知引导**：基于预计算的体素距离图，在采样过程中利用碰撞损失的梯度（Eq. 6）将预测的干净样本推离障碍物。碰撞损失（Eq. 7）计算人体与物体点至最近空体素中心的距离之和，以统一尺度惩罚穿透。消融实验（Table 3，C+B vs C only）表明，碰撞引导在保持人-物接触质量的同时，显著降低人-场景及物-场景穿透指标，仅微幅影响目标到达精度。

### 4. 混合数据训练策略

高质量 HOSI 数据稀缺是领域的长期瓶颈。InfBaGel 采用**混合数据训练**：将大规模合成 HOI 场景（OMOMO，简化体素环境）与少量真实 HSI 数据（LINGO）联合训练，使模型在合成数据上学习交互动力学，在真实数据上获得场景泛化能力。Table 1 中以蓝色标注的指标显示，混合数据策略使模型在 67 个未见室内场景上取得 83.16% 的成功率，较纯 LINGO 训练的 LINGO 基线（53.09%）提升逾 30 个百分点，验证了该策略对零样本场景泛化的关键作用。

### 创新耦合关系

上述四项创新并非孤立存在，而是形成闭环：**一致性模型**提供少步迭代的时序骨架；**动态感知编码**在每步迭代中更新场景状态；**碰撞感知引导**在采样过程中利用更新后的体素距离图约束运动；**混合数据训练**为整个框架提供泛化所需的监督信号。这一耦合设计使得 InfBaGel 在 HOSI Benchmark 上以 83.16% 的成功率、0.13 的脚滑动和 3.39 的人-场景穿透均值全面超越 LINGO、TRUMANS 等场景感知基线，同时在 HOI 数据集上取得 0.68 的 FID（InfBaGel 16，Table 5），验证了迭代精炼对交互质量的一致提升效果。

InfBaGel 构建了一个**自回归的粗到细迭代精炼框架**，将人-物-场景交互（HOSI）生成过程与一致性模型（Consistency Model）的去噪步骤显式对齐。框架接收文本指令、人体与物体的目标位置、物体几何以及场景体素上下文作为输入，输出耦合的人体运动序列 $\mathcal{M}_h$ 与物体运动序列 $\mathcal{M}_o$（见 Fig. 1）。

![[assets/figures/papers/paper_list_l77_https_openreview_net_forum_id_TeyHNq4WlI/figures/001_Figure_1.jpg]]
*Figure 1: Overview of InfBaGel. Our method operates through an iterative refinement process. (a) Auto-regressive Motion Model generating arbitrary long-sequence motions conditioned on textual instructions, goals, object geometry, and scene context. (b) Dynamic Perception Encoder perceives the evolving environment with the temporal-aligned scene state updated by iterative sampling. (c) Bump-aware Guidance detects collisions and directs iterative, collision-free sampling. (d) Hybrid Data training enables robust zero-shot generalization to complex realistic scenes*

### Pipeline 总览

整个生成管道由四个核心模块串联构成，形成“预测—感知—引导—精炼”的闭环：

1. **自回归运动模型（Auto-regressive Motion Model）**：以自回归方式沿时间轴生成连贯的长序列交互动作。每一段生成以当前状态为条件，输出未来若干帧的人-物耦合运动。该模型基于一致性模型架构，可在极少采样步数（如 15 步）内直接输出干净样本，替代传统扩散模型的百步级采样。

2. **动态感知编码器（Dynamic Perception Encoder）**：这是框架区别于静态方法的核心机制。在粗预测阶段，场景中的动态体素（即人/物当前占据或即将占据的区域）被掩蔽；随着迭代去噪的推进，编码器根据上一轮精炼后的运动轨迹，**动态更新时变体素场景状态**，为下一轮采样提供与当前交互进程对齐的上下文条件 $\mathbf{C}_{\tau_n}$。

3. **碰撞感知引导（Bump-aware Guidance）**：在每一步采样中，基于预计算的距离图计算碰撞损失 $\mathcal{L}_{\mathrm{bump}}$，利用其梯度 $\nabla_{\mathbf{x}_{\tau_n}} \mathcal{L}_{\mathrm{bump}}(\hat{\mathbf{x}}_0)$ 调整预测的干净样本 $\hat{\mathbf{x}}_0$，将运动“推离”障碍物（见 Eq. 6–7），在保持人-物接触的同时大幅降低人-场景和物-场景的穿透。

4. **混合数据训练（Hybrid Data Training）**：将合成场景下的 HOI 数据（OMOMO）与真实场景下的 HSI 数据（LINGO）联合训练，使模型在未见过的真实杂乱场景中具备零样本泛化能力。

### 输入-输出流

- **输入**：文本指令、人体目标位置、物体目标位置、物体几何（顶点/面片）、场景体素网格（静态占用 + 动态更新部分）。
- **条件构建**：ViT 将每个场景体素网格独立编码为 512 维嵌入，与文本、目标、物体几何的编码共同构成条件 $\mathbf{C}$。
- **迭代采样**：从噪声 $\mathbf{x}_{\tau_n}$ 出发，经一致性模型采样得到预测的干净运动 $\hat{\mathbf{x}}_0$；随后动态感知模块更新体素状态，碰撞引导修正运动，进入下一轮采样（$\tau_{n-1}$），形成粗到细的精炼循环。
- **输出**：人体 22 关节的 6D 旋转 $\mathbf{R}_h$ 与根节点平移 $\mathbf{T}_h$，以及物体的 6D 位姿序列。

### 训练目标

整体训练损失由三项加权组成（Eq. 5）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CD}} + \lambda_h \mathcal{L}_{\mathrm{joints}} + \lambda_o \mathcal{L}_{\mathrm{obj}}$$

其中 $\mathcal{L}_{\mathrm{CD}}$ 为一致性蒸馏损失（Eq. 1），最小化在线网络与目标网络在相邻 ODE 步输出之间的距离；$\mathcal{L}_{\mathrm{joints}}$ 与 $\mathcal{L}_{\mathrm{obj}}$ 分别为人体关节位置与物体顶点位置的前向运动学 L2 损失（Eq. 3–4），提供显式的运动学监督。

### 关键设计决策

- **一致性模型替代扩散模型**：蒸馏后的模型在 15 步采样下即可生成高质量运动，推理速度从扩散模型的 3.38 FPS 提升至 28.75 FPS（Table 2）。
- **动态体素数量与采样步数**：消融实验表明，3 个动态体素配合 16 步采样达到最佳综合性能（Table 4），验证了多体素时变表示对捕捉人/物移动带来的环境变化是必要的。
- **碰撞引导与接触引导互补**：接触引导（Contact Guidance）维持人-物交互质量，碰撞引导在此基础上消除场景穿透，二者联合使用（C+B）在成功率与物理可行性上取得最优平衡（Table 3）。

InfBaGel 的核心架构由四个关键模块构成，围绕“一致性模型驱动的粗到细迭代精炼”这一主轴协同工作。以下逐一拆解各模块的机理与关键公式。

### 动态感知编码器（Dynamic Perception Encoder）

该模块解决的核心瓶颈是：人/物在场景中移动时，场景上下文是时变的，静态一次性编码无法捕获这种动态变化。

**工作机制：**
- 在粗预测阶段，动态体素被遮蔽（masked out），模型仅依赖静态场景信息生成初始运动。
- 每次去噪迭代后，根据当前预测的人体和物体轨迹更新动态体素的占用状态，形成时变场景表示（time-varying scene state）。
- 更新后的场景状态作为下一迭代步的条件输入，实现“感知-生成-更新”的闭环。

**编码方式：** 使用 ViT（Dosovitskiy et al., 2020）将每个场景体素网格独立编码为 512 维嵌入，随后注入运动生成网络。

**消融证据：** 移除动态感知（替换为静态感知）后，成功率从 86.35% 降至 71.22%，人-场景穿透指标显著恶化（Table 3），定性结果也显示静态感知导致大量碰撞（Figure 3b）。

### 一致性模型蒸馏与训练目标

InfBaGel 将扩散模型蒸馏为一致性模型（Consistency Model），使其能在极少量采样步（如 15 步）内直接输出干净样本，大幅提升生成速度。

**一致性蒸馏损失：**

$$
\mathcal{L}_{\mathrm{CD}} = \mathbb{E}_{\mathbf{x}, n, \mathbf{C}, w} \Big[ d \big( f_{\theta} (\mathbf{x}_{\tau_n}, \tau_n, \mathbf{C}_{\tau_n}, \omega), f_{\theta'} (\hat{\mathbf{x}}_{\tau_{n-1}}^{\Psi, \omega}, \tau_{n-1}, \mathbf{C}_{\tau_{n-1}}, \omega) \big) \Big] \tag{1}
$$

- $f_{\theta}$：在线一致性网络
- $f_{\theta'}$：目标网络（指数滑动平均更新）
- $\mathbf{x}_{\tau_n}$：时间步 $\tau_n$ 处的噪声样本
- $\mathbf{C}_{\tau_n}$：对应时间步的场景条件（含动态体素状态）
- $\hat{\mathbf{x}}_{\tau_{n-1}}^{\Psi, \omega}$：教师扩散模型在分类器无关引导下从 $\tau_n$ 到 $\tau_{n-1}$ 的采样结果

**教师采样步（DDIM）：**

$$
\hat{\mathbf{x}}_{\tau_{n-1}}^{\Psi, \omega} = \mathbf{x}_{\tau_n} + (1+\omega) \Psi(\mathbf{x}_{\tau_n}, \tau_n, \mathbf{C}_{\tau_n}) - \omega \Psi(\mathbf{x}_{\tau_n}, \tau_n, \mathbf{C}_{\tau_n}^{\emptyset}) \tag{2}
$$

其中 $\omega$ 为引导强度，$\mathbf{C}_{\tau_n}^{\emptyset}$ 表示空条件。

**辅助损失：**

除蒸馏损失外，引入两个显式运动学损失以约束生成质量：

$$
\mathcal{L}_{\mathrm{joints}} = \left\| FK_h(\mathcal{M}_h) - FK_h(\hat{\mathcal{M}}_h) \right\|_2^2 \tag{3}
$$

$$
\mathcal{L}_{\mathrm{obj}} = \left\| FK_o(\mathcal{M}_o) - FK_o(\hat{\mathcal{M}}_o) \right\|^2 \tag{4}
$$

其中 $FK_h$、$FK_o$ 分别为人体和物体的前向运动学函数，$\mathcal{M}_h$、$\mathcal{M}_o$ 为真实运动序列。

**总训练目标：**

$$
\mathcal{L} = \mathcal{L}_{\mathrm{CD}} + \lambda_h \mathcal{L}_{\mathrm{joints}} + \lambda_o \mathcal{L}_{\mathrm{obj}} \tag{5}
$$

### 碰撞感知引导（Bump-aware Guidance）

该模块在采样过程中利用预计算的体素距离图，通过梯度引导运动远离障碍物，实现无碰撞生成。

**引导更新：**

$$
\tilde{\mathbf{x}}_0 = \hat{\mathbf{x}}_0 + \gamma_{\tau_n} \nabla_{\mathbf{x}_{\tau_n}} \mathcal{L}_{\mathrm{bump}}(\hat{\mathbf{x}}_0) \tag{6}
$$

- $\hat{\mathbf{x}}_0$：当前步预测的干净样本
- $\gamma_{\tau_n}$：步长相关的引导尺度

**碰撞损失：**

$$
\mathcal{L}_{\mathrm{bump}} = \sum_{p \in \{ \hat{\mathcal{M}}_h, \hat{\mathcal{M}}_o \}} D(V(p)) \tag{7}
$$

- $p$：人体或物体网格上的采样点
- $V(p)$：点 $p$ 所在的体素
- $D(\cdot)$：该体素中心到最近空体素中心的距离（预计算距离图）

**消融证据：** 加入碰撞引导（C+B）相比仅使用接触引导（C），人-场景穿透均值（P_mean）和物体-场景穿透均值显著降低，仅微幅影响目标到达距离（Table 3）。定性消融中，移除碰撞引导后出现明显穿模（Figure 3c）。

### 混合数据训练策略

为缓解带场景标注的 HOSI 数据稀缺问题，InfBaGel 采用混合数据训练：将合成场景的 HOI 数据（OMOMO）与真实场景的 HSI 数据（LINGO）联合训练，使模型在未见真实场景中具备零样本泛化能力。Table 1 中蓝色标注的指标即体现混合数据带来的增益。

### 自回归运动生成

利用一致性模型的少步生成效率，InfBaGel 采用自回归策略生成任意长度的长序列交互动作：将上一窗口的生成结果作为下一窗口的初始条件，实现连贯的长时程人-物-场景交互。

## 实验与关键发现

InfBaGel 的实验评估围绕两个核心基准展开：**HOSI Benchmark**（人-物-场景交互）与 **HOI Dataset**（人-物交互），分别验证场景感知能力与交互生成质量。以下从主结果、消融分析、速度对比、参数敏感性及失败模式几个维度展开。

### 主结果：HOSI 任务全面领先

Table 1 报告了在 HOSI Benchmark（469 条序列，7 类物体，67 个未见室内场景）上的定量对比。InfBaGel 在所有指标上均显著超越现有场景感知基线：

![[assets/figures/papers/paper_list_l77_https_openreview_net_forum_id_TeyHNq4WlI/figures/002_Table_1.jpg]]
*Table 1: Quantitative results of HOSI task, where the human moves the object from one place to another in a cluttered realistic scene. Blue highlights the improvement brought by hybrid data*

- **成功率（S%）**：83.16%，较最强基线 **LINGO**（Jiang et al., 2024a）的 53.09% 提升 **+30.07 个百分点**，较 **TRUMANS**（Jiang et al., 2024b）的 29.25% 提升逾 53 个百分点。该指标要求人与物体的目标距离均低于 10 cm，直接衡量任务完成的可靠性。
- **足部滑动（FS↓）**：0.13，远低于 LINGO 的 0.57 和 TRUMANS 的 0.42，表明生成运动的地面接触物理合理性更优。
- **人-物接触率（C%↑）**：78.18%，较 LINGO 的 53.83% 提升 **+24.35 个百分点**，说明物体在交互过程中更稳定地与人手保持接触。
- **人-场景穿透均值（P_mean↓）**：3.39，较 LINGO 的 7.62 降低 **-4.23**，较 TRUMANS 的 9.80 降幅更大，直接体现动态感知编码与碰撞引导对场景穿透的抑制效果。

Table 1 中蓝色标注部分进一步表明，混合数据训练策略（合成 OMOMO + 真实 LINGO）是带来上述增益的关键因素。

### HOI 数据集：交互质量保持竞争力

在 HOI Dataset（OMOMO）上，InfBaGel 同样展现出优势（Table 5）。以 FID↓ 衡量生成分布与真实分布的接近程度：

- InfBaGel（16 步采样）FID 为 **0.68**，优于 **CHOIS**（Li et al., 2024b）的 1.01（降低 0.33）和 ROG 的 1.23。
- 该结果验证了迭代精炼框架在无场景条件下同样能提升交互质量，并非仅依赖场景模块。

### 生成速度：一致性模型带来数量级加速

Table 2 对比了扩散模型（DM）与一致性模型（Consistency Model）的推理速度。在平均序列长度约 193 帧的条件下：

![[assets/figures/papers/paper_list_l77_https_openreview_net_forum_id_TeyHNq4WlI/figures/003_Table_2.jpg]]
*Table 2: Comparison of generation speed. ‘DM’ denotes Diffusion Model and*

- 扩散模型（1000 步 DDIM + 引导）仅达到 **3.38 FPS**。
- InfBaGel 一致性模型（15 步 + 碰撞引导）达到 **28.75 FPS**，加速约 **8.5 倍**。
- 值得注意的是，即使扩散模型在少步（如 15 步）下采样，其生成质量会因截断误差而严重退化，而一致性模型在少步下仍保持高质量输出。这一因果机制源于一致性蒸馏损失（Eq. 1）直接学习 ODE 轨迹的相邻点映射，避免了步数减少带来的误差累积。

### 消融实验：各模块的因果贡献

Table 3 系统拆解了动态感知编码（DP）与碰撞感知引导（B）的独立贡献，Figure 3 提供定性可视化佐证。

![[assets/figures/papers/paper_list_l77_https_openreview_net_forum_id_TeyHNq4WlI/figures/005_Table_3.jpg]]
*Table 3: Ablation on key components: Dynamic Perception Encoding (DP) and Guidance (G). C denotes Contact Guidance (Li et al., 2024b); B denotes our Bump-aware Guidance. A Diffusion Model baseline with DP is included to study effects on dynamic perception, guidance is omitted due to inconsistent sampling steps and weighting*

![[assets/figures/papers/paper_list_l77_https_openreview_net_forum_id_TeyHNq4WlI/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison in ablation study. Replacing/removing specific modules: (a) diffusion model instead of consistency model, (b) static perception instead of dynamic perception, and (c) without bump-aware guidance, all resulted in collisions with the scene*

**动态感知编码（DP）的因果效应**：
- 在仅使用接触引导（C）的配置中，启用 DP 使成功率从 71.22% 跃升至 **86.35%**（+15.13 pp），同时人-场景穿透均值从 5.62 降至 **3.99**（-1.63）。
- 这证实了**迭代更新场景体素状态**是解决“人/物移动导致场景上下文变化”这一瓶颈的核心机制。静态编码无法感知物体被移开后释放的空间，导致后续运动规划仍将已清空区域视为障碍。

**碰撞感知引导（B）的因果效应**：
- 在 DP 已启用的前提下，将接触引导（C）替换为碰撞引导（C+B），人-场景穿透均值进一步从 3.99 降至 **3.39**，物体-场景穿透均值从 2.10 降至 **1.39**。
- 关键权衡：目标距离（D_goal）从 5.12 微增至 5.72，说明统一尺度的距离惩罚（Eq. 6-7）使运动略微保守，稍微牺牲了到达精度。但这一代价换来了穿透指标的显著改善，整体成功率保持稳定。

**扩散模型基线的对比**：
- Table 3 还包含一个扩散模型 + DP 的基线（无引导，因采样步数与权重不兼容）。其成功率为 74.05%，低于一致性模型 + DP 的 86.35%，且穿透指标更差，从侧面验证了一致性模型在少步采样下的质量优势。

### 参数敏感性：体素数量与精炼步数

Table 4 探索了动态体素数量（1 vs 3）与采样步数（4/8/16/32）的组合效应：

- **3 个体素** 在所有步数配置下均优于 1 个体素，验证了多尺度场景表示对动态感知的必要性。
- **16 步** 达到最佳综合性能（成功率 86.35%，穿透均值 3.99），步数过少（4 步）精炼不充分，步数过多（32 步）收益递减且增加计算开销。
- 这一结果与一致性模型的 ODE 轨迹特性一致：16 步已足够逼近连续轨迹，额外步数带来的边际改善有限。

### 混合数据比例的影响

Table 6 展示了合成 OMOMO 数据与真实 LINGO 数据不同混合比例的效果。纯合成数据（0:1）在真实场景中泛化能力不足，纯真实数据（1:0）则因缺乏 HOI 标注而交互质量下降。最优比例位于中间区域，验证了混合数据训练策略对零样本场景泛化的支撑作用。

### 失败模式与局限性

尽管整体性能显著领先，分析中仍可识别以下不足：

1. **精细几何约束不足**：动态感知依赖粗略的体素占用表示（3 个体素网格），对于需要精确抓取姿态或力闭合的任务，体素分辨率可能不足以捕捉关键几何细节。这在 Table 4 中体现为即使最优配置下穿透均值仍有 3.99，未能完全消除。
2. **碰撞引导的保守性**：如消融所示，碰撞引导使目标距离微增，在狭窄通道或高密度障碍场景中可能导致运动过度绕行甚至无法到达目标。
3. **场景域限制**：实验场景均为室内环境（HOSI Benchmark 的 67 个场景、LINGO 的社交场景），物体类别限于 7 类。在开放世界动态场景（如室外、多人交互）中的泛化性尚待验证。
4. **合成数据依赖**：训练监督依赖合成 HOI 场景的简化体素环境，可能无法完全覆盖真实世界中复杂的几何约束和物理语义，这需要进一步与物理模拟器结合来弥补。

### 小结

InfBaGel 通过动态感知编码与碰撞引导的协同，在 HOSI 任务上实现了成功率 83.16% 的领先性能，同时将生成速度提升至 28.75 FPS。消融实验明确证实：迭代场景更新是解决动态上下文瓶颈的因果性机制，碰撞引导以微小的目标精度代价换取了显著的穿透改善，一致性模型则为实时迭代精炼提供了速度基础。

![[assets/figures/papers/paper_list_l77_https_openreview_net_forum_id_TeyHNq4WlI/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results on different scenes, motion types and object types. The top two rows*

## 定位与知识库关联

### 1. 与基线方法的关系

InfBaGel 处于**场景感知的人-物交互生成**这一研究脉络中，其主要对比基线可分为两类：场景感知运动生成方法和HOI生成方法。

**场景感知基线**方面，**TRUMANS**（Jiang et al., 2024b）和**LINGO**（Jiang et al., 2024a）代表了当前将场景上下文纳入运动生成的主流范式。然而，这两类方法均采用**静态一次性体素编码**来表征场景——即在整个生成过程中场景状态保持不变。InfBaGel 的核心突破在于将这一“静态感知”升级为**动态感知编码**：利用前一迭代结果更新时变体素状态，使场景上下文随人/物运动而持续演化。这一机制差异直接解释了 Table 1 中的性能鸿沟：InfBaGel 的 Success Rate 达到 83.16%，而 LINGO 仅为 53.09%，绝对提升超过 30 个百分点。

**HOI生成基线**方面，**CHOIS**（Li et al., 2024b）和**ROG**代表了仅关注人-物交互而不考虑场景约束的生成方法。在 HOI 数据集（OMOMO）上，InfBaGel 以 16 步采样取得 FID 0.68，优于 CHOIS 的 1.01（Table 5），表明即使在无场景约束条件下，一致性模型驱动的迭代精炼仍能提升交互质量。

**生成模型架构**的谱系变化更为显著。传统扩散模型（如DDPM）需要数百乃至上千步去噪，而 InfBaGel 将扩散模型蒸馏为**一致性模型**，仅需 15-16 步即可直接输出干净样本。Table 2 显示，这一替换将生成速度从 3.38 FPS 提升至 28.75 FPS（约 8.5 倍加速），同时交互质量不降反升。

**采样引导策略**方面，CHOIS 采用接触引导（Contact Guidance）来促进人-物接触，但缺乏对场景碰撞的显式约束。InfBaGel 引入的**碰撞感知引导**基于预计算体素距离图，通过梯度直接优化无碰撞性（Eq. 6-7），使得在保持人-物接触率（C% 78.18）的同时，将人-场景穿透均值从 LINGO 的 7.62 降至 3.39（Table 1）。

### 2. 适用边界

InfBaGel 的有效性建立在以下前提之上：

- **场景表示依赖体素占用**：动态感知编码使用粗略的体素占用网格（3个动态体素，Table 4 消融证实优于单个体素），这意味着该方法适用于宏观碰撞避免（如人体不穿墙、物体不穿桌），但对精细几何约束（如手指抓取稳定、力闭合条件）的建模能力有限。
- **训练监督依赖合成HOI场景**：混合数据训练策略将 OMOMO 合成数据（简化体素环境中的HOI）与 LINGO 真实场景数据联合训练（Table 6 消融了不同混合比例），使得模型在真实复杂场景中获得零样本泛化能力。但这一泛化能力依赖于合成数据与真实数据在体素表示层面的对齐，对于超出训练分布的场景几何（如室外、非曼哈顿世界结构），泛化性未经验证。
- **碰撞引导采用统一尺度惩罚**：Eq. 7 中的碰撞损失对所有人体/物体点施加相同权重的距离惩罚，这可能导致运动趋于保守，在 Table 3 消融中表现为目标距离指标的轻微劣化（C+B vs C only）。
- **实验场景限于室内**：HOSI Benchmark 包含 67 个未见室内场景、7 个物体类别（Section 4.1），Figure 5 展示了在商店、理疗室等社交场景中的零样本泛化，但开放世界动态场景（如户外、拥挤人群）中的表现尚未评估。

### 3. 局限与开放问题

**已确认的局限**：

1. **体素表示的精度瓶颈**：动态感知依赖于粗略的体素占用表示，对于需要精细几何推理的任务（如抓取稳定性、接触力分布）仍需补充更细粒度的表示。Figure 3(b) 的定性消融显示，将动态感知替换为静态感知后出现明显的场景穿透，但即使启用动态感知，Table 1 中 P_mean 仍为 3.39 cm，表明残余穿透依然存在。
2. **合成数据与真实场景的域间隙**：混合数据训练虽实现了零样本泛化，但合成 OMOMO 场景的简化体素环境可能无法覆盖真实世界中复杂的几何约束和物理语义（如可变形物体、狭窄通道）。
3. **碰撞引导的保守性**：统一尺度的距离惩罚可能牺牲目标到达精度，这在需要紧贴障碍物操作的场景中尤为明显。
4. **物体类别受限**：HOSI Benchmark 仅覆盖 7 个物体类别，方法在更多样化的物体形状和尺寸上的泛化性有待验证。

**开放问题**：

1. **从体素到连续几何的演进**：如何将基于体素的动态感知拓展到连续几何表示（如符号距离场、神经辐射场），以提高精细交互的准确性？这涉及表示分辨率与计算效率的权衡。
2. **自适应碰撞引导**：碰撞引导的参数 $\gamma_{\tau_n}$（Eq. 6）当前为固定调度。是否可设计自动学习或适应不同场景复杂度的自适应策略，使得在开阔区域减少保守性、在密集障碍区域增强约束？
3. **混合数据最优比例的任务依赖性**：Table 6 消融了 OMOMO 与 LINGO 数据的不同混合比例，但最优比例是否与下游任务类型相关（如搬运 vs. 坐姿交互），以及能否推广到更多样化的交互类型（如多人协作），仍是开放问题。
4. **与物理模拟器的结合**：当前方法基于运动学生成，不显式建模力和动力学约束。能否与基于物理的模拟器结合，在迭代精炼过程中引入物理合理性验证，进一步提升运动质量？这需要解决模拟器梯度回传或强化学习接口的问题。
5. **长序列自回归的误差累积**：InfBaGel 采用自回归策略生成长序列交互（Fig. 1a），但自回归生成固有的误差累积效应在超长序列（如数分钟级交互）中的影响尚未量化分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/InfBaGel_Human_Object_Scene_Interaction_Generation_with_Dynamic_Perception_and_I_ff1cfe7d66d2.pdf]]

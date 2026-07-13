---
title: "SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SIMPACT_Simulation_Enabled_Action_Planning_using_Vision_Language_Models.pdf
project_link: "https://simpact-bot.github.io"
code_link: null
aliases:
- SIMPACT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在测试时通过物理仿真生成 rollout 作为上下文，使 VLM 能够进行基于物理的迭代推理和动作优化。
primary_logic: 从单张 RGB-D 图像自动构建多物理仿真器，并利用 VLM 的预训练知识进行动作采样、仿真 rollout 评估和上下文优化，实现零样本的物理感知规划。
claims:
- 本方法在全部 7 项具有挑战性的真实世界任务上均显著优于所有基线方法（Table 2）。
- 消融实验表明，移除 VLM 采样器、仿真 rollout 或 VLM 优化器中的任一模块都会导致性能大幅下降，证明了各组件的重要性（Table 3）。
- 仿真与真实世界结果的一致性达到 89%，证实仿真作为物理 grounding 的可靠性（Fig. 12）。
- "Real-world manipulation: Non-toppling push 上 Success Rate (%) = 80"
---

# SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models

> [!tip] 核心洞察
> 从单张 RGB-D 图像自动构建多物理仿真器，并利用 VLM 的预训练知识进行动作采样、仿真 rollout 评估和上下文优化，实现零样本的物理感知规划。

| 字段 | 内容 |
|------|------|
| 中文题名 | SIMPACT：仿真赋能的视觉语言模型动作规划 |
| 英文题名 | SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.05955) · [Project](https://simpact-bot.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SIMPACT |
| Dataset | Real-world manipulation: Non-toppling push, Real-world manipulation: Bowl stacking, Real-world manipulation: Pivoting, Real-world manipulation: Shape rope |

> [!tip] 效果简介
> - Real-world manipulation: Non-toppling push 上，Success Rate (%) 80 vs 0 (+80)。
> - Real-world manipulation: Bowl stacking 上，Success Rate (%) 60 vs 20 (+40)。
> - Real-world manipulation: Pivoting 上，Success Rate (%) 40 vs 0 (+40)。

## 概要

机器人操控任务中，视觉语言模型（VLM）虽展现出强大的语义理解与规划能力，却普遍缺乏对物理动力学的认知——它们无法预测动作执行后的物理结果，导致在需要精细物理推理的任务上频繁失败。这一瓶颈的本质在于：VLM 的推理仅建立在语言和图像的语义关联之上，缺少一个可交互的物理世界模型作为 grounding。

SIMPACT 的核心洞察是：**在测试时，通过从单张 RGB-D 图像自动构建多物理仿真器，并将仿真 rollout 作为上下文反馈给 VLM，可以使 VLM 获得基于物理的迭代推理与动作优化能力**。具体而言，该方法利用预训练的视觉基础模型（分割、3D 生成、位姿估计）快速实例化一个包含刚体网格或可变形粒子表示的物理仿真环境；然后，VLM 基于场景上下文进行层次化动作采样，通过仿真 rollout 评估候选动作的物理后果，并以 in-context learning 的方式从失败案例中推理改进动作，直至任务成功。

在涵盖刚体与可变形物体的 7 项真实世界精细操控任务上（包括不倾倒推瓶、碗叠放、枢转、绳索塑形、面团塑形、避障、清扫），SIMPACT 以零样本方式显著优于所有基线方法：相较于 VLA 模型 π0.5、几何规划方法 VoxPoser 和关键点方法 MOKA，SIMPACT 在多数任务上实现了 40–80 个百分点的成功率提升（Table 2）。消融实验进一步证实，VLM 引导的动作采样、仿真 rollout 上下文和 VLM 优化器三者缺一不可，移除任一模块均导致性能大幅下降（Table 3）。仿真与真实世界结果的一致性达 89%，验证了仿真作为物理 grounding 的可靠性（Fig. 12）。

方法的主要局限在于：单视图 3D 重建引入的感知误差、仿真与现实的动力学偏差、以及依赖商业 VLM 带来的高推理延迟（总计超过 5 分钟），限制了其在实时场景中的直接部署。尽管如此，SIMPACT 开创性地展示了“仿真赋能 VLM 测试时推理”这一范式的潜力，为零样本物理感知规划提供了可扩展的技术路径。

### 机器人操控中的物理推理瓶颈

机器人操控任务，尤其是涉及精细物理交互的场景（如推动瓶子而不使其倾倒、堆叠碗碟、揉捏面团等），要求规划系统不仅理解语义指令，还必须预测动作执行后的物理结果。当前主流的视觉语言模型（VLM）虽然在语义理解、常识推理和开放集泛化方面展现出强大能力，但它们缺乏对物理动力学的内建理解——VLM 无法预测“推瓶子时用多大力、推多高瓶子会倒”这类依赖于质量、摩擦、接触几何的物理后果。

这一根本性缺陷导致现有基于 VLM 的机器人规划方法在需要精细物理推理的任务上频繁失败。如 Figure 1 所示，一个普通的 VLM 规划器可能选择错误的推动高度或力度，导致瓶子倾倒，而无法像具备物理感知能力的系统那样完成精确操控。**核心瓶颈在于：VLM 的推理空间局限于语言和图像语义，缺少一个物理世界的“沙盒”来验证和修正动作方案。**

### 现有方法的局限

近年来，多种基于 VLM 或视觉-语言-行动（VLA）模型的机器人规划方法被提出，但它们均未有效解决物理推理缺口：

- **π0.5**：作为 VLA 模型，在大规模机器人数据上训练，直接预测关节速度。然而其训练数据难以覆盖长尾的精细物理交互场景，在本文涉及的 7 项真实世界任务上成功率极低（多数为 0%）。
- **VoxPoser**：基于 VLM 和 3D 价值地图生成几何约束下的操控动作，本质上仍依赖几何推理而非物理推理，无法预测动作的动力学后果。
- **MOKA**：利用关键点和交互区域进行 VLM 规划，同样缺乏对物理结果的预测能力。

这些方法的共同问题是：**它们要么直接输出动作序列（单次推理，无反馈修正），要么仅通过几何表示间接生成动作，均未引入物理动态模型来评估和优化动作的物理可行性。** 如 Table 2 所示，这些基线方法在 non-toppling push、pivoting、shape dough 等需要精细物理感知的任务上成功率为 0%，在 bowl stacking、shape rope 等任务上也远低于本文方法。

### 核心动机与研究思路

本文的核心洞察是：**如果在测试时能够为 VLM 提供一个物理仿真器，使其能够“在脑中预演”动作的物理结果，VLM 强大的推理和泛化能力就可以被引导到物理感知的动作优化上。** 这相当于为 VLM 配备了一个物理 grounding 模块，使其推理从纯语义空间扩展到物理仿真空间。

基于这一洞察，本文提出 **SIMPACT** 框架，其设计原则是：

1. **从单张 RGB-D 图像自动构建物理仿真器**：利用预训练的视觉基础模型（分割、3D 重建、位姿估计）和 VLM 的物理参数推理能力，高效生成包含刚体网格或可变形体粒子的多物理仿真环境，无需人工建模。
2. **将仿真 rollout 作为 VLM 的上下文反馈**：VLM 采样动作方案后，在仿真器中执行并观察结果，成功的经验和不成功的失败模式均作为 in-context learning 的输入，使 VLM 能够迭代优化动作序列。
3. **零样本、测试时推理**：整个规划过程在测试时完成，无需针对特定任务进行微调或训练，充分利用 VLM 的预训练知识和仿真器的物理保真度。

这一“仿真赋能 VLM”的范式，将物理推理从模型内部不可学习的黑箱，转化为外部可操作、可观察的显式反馈循环，为解决精细操控任务中的物理推理瓶颈提供了新路径。

## 核心方法与创新机理

### 问题瓶颈：VLM 缺乏物理动力学认知

当前视觉语言模型（VLM）在机器人操控规划中的根本瓶颈在于其仅依赖语言和图像语义进行推理，缺乏对物理动力学的理解。具体而言，VLM 无法预测动作执行后的物理结果——例如推动一个瓶子时，它无法判断施加多大的力会导致瓶子倾倒、推动多远才能达到目标位置。这导致 VLM 在需要精细物理推理的任务中系统性地失败，如 Figure 1 上半部分所示，vanilla VLM planner 无法完成非倾倒推动任务。

### 核心因果机制：仿真 Rollout 作为物理 Grounding 的上下文反馈

SIMPACT 的核心创新在于引入了一个因果调节变量：**在测试时通过物理仿真生成 rollout 作为上下文反馈**，使 VLM 能够进行基于物理的迭代推理和动作优化。这一机制的本质是将物理仿真器作为 VLM 的“外部物理直觉”模块，在规划循环中提供物理 grounding。

整个闭环流程如下：
1. **仿真构建**：从单张 RGB-D 图像自动构建多物理仿真器（Figure 2），包括刚体的 mesh-based 仿真和可变形物体的 particle-based 仿真
2. **VLM 引导的动作采样**：基于场景上下文和任务描述，VLM 生成多样化的高层次动作提案
3. **仿真 Rollout 评估**：每个动作提案在仿真器中执行，生成包含中间状态和结果的 rollout 轨迹
4. **上下文优化**：VLM 将多个 rollout（包括失败案例）作为上下文，通过 in-context learning 推理失败原因并生成改进动作
5. **迭代直至成功**：通过 VLM Success Evaluator 判断任务是否完成，决定是否继续迭代

### 相对 Baseline 的关键 Changed Slots

与现有方法的本质差异体现在三个维度：

**1. 物理推理方式：从纯语义推理到物理 Grounding 推理**

| 方法类型 | 物理推理方式 | 代表方法 |
|---------|------------|---------|
| VLA 模型 | 从大规模机器人数据中隐式学习物理先验，无显式动态模型 | **π0.5** |
| 几何表示方法 | 基于 VLM 和 3D 价值地图生成动作，仅考虑几何约束 | **VoxPoser** |
| 关键点方法 | 基于关键点和交互区域进行规划，无物理仿真 | **MOKA** |
| **SIMPACT** | **集成多物理仿真器，在动作优化中引入基于物理的 rollout 反馈** | 本方法 |

这一差异是根本性的：baseline 方法在物理推理上要么完全缺失（VoxPoser、MOKA），要么仅通过训练数据隐式学习（π0.5），而 SIMPACT 显式地将物理仿真作为推理组件，使 VLM 能够“看到”动作的物理后果。

**2. 动作生成方式：从单次推理到仿真驱动的迭代采样**

Baseline 方法通常采用单次 VLM 推理直接输出动作序列，或通过几何表示一次性生成轨迹。SIMPACT 引入了层次化的符号动作采样机制：
- VLM 首先采样高层次动作类型和参数 $\mathbf{A}^i = \mathbf{VLM}(I_0, \ell_{\mathrm{task}}, s_0; \ell_{\mathrm{sample}})$
- 通过 ACTION2POSE 映射将符号动作转换为连续 6-DoF 轨迹 $\mathbf{a}^i = \mathbf{ACTION2POSE}(\mathbf{A}^i)$
- 仿真 rollout 提供物理反馈后，VLM 进行多轮优化：$\mathbf{a}^k = \mathbf{VLM}(c^1, ..., c^K; \ell_{\mathrm{opt}})$

Figure 4 展示了这一迭代优化的典型过程：初始三个动作提案全部失败（推动不足、过度推动、瓶子倾倒），VLM 优化器从这些失败中推理出非平凡的改进策略，最终生成合适的推动距离和高度，在仿真和真实世界中均取得成功。

**3. 优化与评估策略：从无迭代到基于失败经验的上下文学习**

Baseline 方法无迭代优化或仅进行内部验证。SIMPACT 的优化器具有两个独特性质：
- **非局部更新**：不受数值优化器的局部搜索限制，可以从全局层面重新规划动作策略
- **从失败中学习**：VLM 能够综合多个失败案例的共性原因进行推理，而非简单的参数调优

消融实验（Table 3）严格验证了这三个组件的必要性：移除 VLM 采样器（替换为高斯随机采样）导致 non-toppling push 成功率从 80% 降至 0%；移除仿真 rollout 上下文使 bowl stacking 等需要物理交互的任务性能大幅下降；移除 VLM 优化器（仅从初始样本中选择最佳动作）在初始样本不足的任务上表现明显恶化。

### 仿真与现实的一致性验证

SIMPACT 的物理 grounding 依赖于仿真与真实世界的一致性。Figure 12 的分析表明，在所有 100 个测试样本中，仿真与真实世界的结果匹配率达到 **89%**（同为成功或同为失败），11% 的案例为仿真成功但真实失败（sim-success/real-fail），未出现仿真失败但真实成功的情况。这一结果表明仿真器在大多数情况下能够可靠地预测物理结果，为 VLM 的物理推理提供了可信的 grounding 基础。

SIMPACT 是一个**零样本机器人操控动作规划框架**，其核心输入为单张 RGB‑D 图像 $I_0$ 与自然语言任务指令 $\ell_{\mathrm{task}}$，输出为一组机器人末端执行器动作序列 $\mathbf{a} = \{a_t\}_{1 \leq t \leq T}$，其中每个动作 $a_t \in \mathrm{SE}(3) \times \mathbb{R}$ 定义了末端执行器的 6‑DoF 位姿与夹爪开合宽度（见 Fig. 1 与 Fig. 3 总览）。

![[assets/figures/papers/paper_list_l2417_https_arxiv_org_abs_2512_05955/figures/003_Figure_3.jpg]]
*Figure 3: Method overview. Our method first instantiates a physics simulator given the real-world scene. Next, a VLM-based action sampler and optimizer iteratively refine the action sequence towards task success using simulated rollouts as context. The final optimized actions are then executed in the real world*

整个 pipeline 由两大阶段串联而成，形成“感知→仿真→规划→优化→执行”的闭环：

### 1. 仿真构建阶段（Simulation Construction Pipeline）
从单张 RGB‑D 图像出发，利用预训练视觉基础模型自动构建物理仿真器，为后续 VLM 推理提供**物理 grounding**。该阶段输出包含：
- **刚体**：三角网格 $\mathcal{M}_i$ 与初始 6‑DoF 位姿 $X_i$，构成几何参数 $\theta_{\mathrm{geom}} = \{(\mathcal{M}_i, X_i)\}_{i=1}^{N_{\mathrm{obj}}}$；
- **可变形体**：粒子点集 $\theta_{\mathrm{geom}} = \{P_i\}_{i=1}^{N_{\mathrm{obj}}}$，通过对分割掩码反投影深度点并在物体表面包围体内均匀采样构建；
- **物理参数**：由 VLM 推理估计的质量、摩擦系数等时不变参数 $\theta$，用于定义状态转移 $s_t = \mathbf{SIM}(s_{t-1}, a_t; \theta)$（Eq. 1）。

仿真器根据物体类别自动选择**网格仿真**（刚体）或**粒子仿真**（可变形体），如 Fig. 2 所示。

### 2. 动作规划与优化阶段（VLM‑based Action Planning）
该阶段以仿真器为 backbone，通过 VLM 的预训练知识驱动**迭代式动作采样、仿真 rollout 评估与上下文优化**，如 Fig. 3 与 Alg. 1 所示。核心模块包括：

- **VLM Action Sampler**：基于初始场景图像 $I_0$、任务描述 $\ell_{\mathrm{task}}$、初始状态 $s_0$ 与采样提示 $\ell_{\mathrm{sample}}$，生成 $K$ 组高层次符号动作序列 $\mathbf{A}^i$，再经 $\mathbf{ACTION2POSE}$ 映射为连续轨迹 $\mathbf{a}^i$（Eq. 13）。这一步利用 VLM 的常识推理能力，确保初始动作提案具有物理合理性，而非盲目随机探索。

- **Simulation Rollout**：将每组动作序列 $\mathbf{a}^i$ 输入仿真器，执行完整的状态转移序列，生成 rollout 上下文 $c^i$（包含各时间步的仿真截图、夹爪位姿与物体状态）。

- **VLM Action Optimizer**：以 $K$ 组 rollout 上下文 $\{c^1, ..., c^K\}$ 作为 in‑context 示例，VLM 根据失败案例进行跨样本推理，输出优化后的动作序列 $\mathbf{a}^k = \mathbf{VLM}(c^1, ..., c^K; \ell_{\mathrm{opt}})$（Eq. 2）。该优化器不受限于数值优化器的局部更新，可综合多轮失败经验进行全局性推理（如 Fig. 4 中从“推倒瓶子”的失败中推理出正确的推动距离）。

- **VLM Success Evaluator**：根据最终仿真图像 $I_T^k$ 与状态 $s_T^k$，VLM 判断任务是否成功（$\mathrm{TASKSUCCESS}$）。若成功则终止迭代并输出动作序列；否则将优化后的动作重新送入仿真器进行下一轮迭代。

### 3. 输入输出流与模块关系
整体数据流可概括为：
1. **输入**：RGB‑D 图像 + 语言指令
2. **仿真构建**：分割 → 3D 重建 → 位姿估计 → VLM 物理参数推理 → 物理仿真器实例化
3. **动作采样**：VLM 生成 $K$ 组符号动作 → ACTION2POSE 转换为连续轨迹
4. **仿真评估**：并行执行 $K$ 组 rollout，生成优化上下文
5. **动作优化**：VLM 基于上下文推理改进动作序列
6. **成功判定**：VLM 评估最终状态 → 成功则输出，否则回到步骤 4

该框架的关键创新在于将**物理仿真作为 VLM 的测试时推理工具**：VLM 不直接预测最终动作，而是通过“提议→仿真验证→反思优化”的闭环，将物理动力学反馈注入语言模型的推理链中，从而在不进行任何任务微调的情况下，实现对精细物理操控任务的零样本泛化。

SIMPACT 的核心由一个**仿真构建管线**和一个基于 VLM 的**迭代动作规划循环**构成。前者从单张 RGB-D 图像自动实例化物理世界模型，后者利用该模型进行测试时的物理推理与动作优化。

### 仿真构建管线 (Simulation Construction Pipeline)

给定单张 RGB-D 图像 $I_0$ 和任务语言描述 $\ell_{\mathrm{task}}$，该管线自动构建一个多物理仿真器，为后续规划提供物理 grounding。其核心输出是仿真参数 $\theta$，包括几何参数 $\theta_{\mathrm{geom}}$ 和物理参数 $\theta_{\mathrm{phys}}$。离散时间状态转移方程定义为：

$$s_t = \mathbf{SIM}(s_{t-1}, a_t; \theta)$$

其中 $s_t$ 为当前状态，$a_t$ 为施加的动作，$\theta$ 为时不变仿真参数。管线针对刚体与可变形体采用不同的建模策略：

- **刚体**：几何参数 $\theta_{\mathrm{geom}} = \{ (\mathcal{M}_i, X_i) \}_{i=1}^{N_{\mathrm{obj}}}$，其中 $\mathcal{M}_i$ 为三角网格，$X_i$ 为物体 $i$ 的初始 6-DoF 位姿。网格需经缩放与平移校正，以满足真实世界尺度：

  $$\mathcal{M}_i = \alpha_i (\hat{\mathcal{M}}_i - \beta_i)$$

  其中 $\hat{\mathcal{M}}_i$ 为重建的未缩放网格，$\alpha_i$ 和 $\beta_i$ 由真实世界边界框对角线长度推导。

- **可变形体**：几何参数 $\theta_{\mathrm{geom}} = \{P_i\}_{i=1}^{N_{\mathrm{obj}}}$，其中 $P_i$ 为物体 $i$ 的粒子点集。生成方法为：将分割掩码从深度图反投影获得 3D 表面点，再在表面包围的体积内均匀采样内部粒子。

物理参数 $\theta_{\mathrm{phys}}$（质量、摩擦系数等）由 VLM 根据物体类别和场景上下文推理估计。消融实验表明，VLM 估计的物理参数具有低方差和合理范围（如质量 $1.033 \pm 0.0015$ kg，摩擦系数 $0.36 \pm 0.11$），保证了仿真物理参数的稳定性 (Table 6)。

### 迭代动作规划循环

动作规划遵循“采样—仿真评估—优化—成功判定”的迭代循环。动作序列定义为 $\mathbf{a} = \{ a_t \}_{1 \leq t \leq T}$，其中 $a_t \in \mathrm{SE}(3) \times \mathbb{R}$，分别表示末端执行器位姿和夹爪开度。

**1. VLM 动作采样器 (VLM Action Sampler)**

VLM 根据初始图像、任务描述和初始状态，生成 $K$ 个多样化的高层次动作提案 $\mathbf{A}^i$，再经 ACTION2POSE 映射为连续 6-DoF 轨迹：

$$\mathbf{a}^i = \mathbf{ACTION2POSE}(\mathbf{A}^i = \mathbf{VLM}(I_0, \ell_{\mathrm{task}}, s_0; \ell_{\mathrm{sample}}))$$

高层次动作表示 $\mathbf{A}_t = (\tau_t, u_t)$ 包含动作类型 $\tau_t$ 和连续控制参数 $u_t$，使 VLM 在符号层面进行推理，降低动作空间复杂度。

**2. VLM 动作优化器 (VLM Action Optimizer)**

每个候选动作序列 $\mathbf{a}^i$ 在仿真器中执行 rollout，生成优化上下文 $c^i$（包含各时间步的夹爪位姿、物体状态和渲染图像）。VLM 以 $K$ 个 rollout 的上下文为输入，通过 in-context learning 从失败案例中推理并输出优化后的动作序列：

$$\mathbf{a}^k = \mathbf{VLM}(c^1, ..., c^K; \ell_{\mathrm{opt}})$$

该优化过程不受限于数值优化器的局部更新，VLM 能够综合所有失败经验进行全局推理（Fig. 4 展示了 non-toppling push 任务中，VLM 从三个失败 rollout 中推理出正确推距的典型案例）。

**3. VLM 任务成功评估器 (VLM Success Evaluator)**

根据最终仿真图像 $I_T^k$ 和状态 $s_T^k$，VLM 判断任务是否成功：

$$\mathrm{TASKSUCCESS}(\mathbf{s}^k) = \mathbf{VLM}(I_T^k, s_T^k, \ell_{\mathrm{task}}; \ell_{\mathrm{eval}})$$

若成功则终止迭代并输出动作序列；否则将新的 rollout 上下文加入优化历史，进入下一轮采样或优化。

![[assets/figures/papers/paper_list_l2417_https_arxiv_org_abs_2512_05955/figures/002_Figure_2.jpg]]
*Figure 2: Simulation construction from a single RGBD image. Given an RGB-D image and a language task description, our pipeline automatically generates either a mesh-based simulation (top) for rigid objects or a particle-based simulation (bottom) for deformables. After segmenting objects-of-interest via GroundedSAM2 [55], we reconstruct either the 3D shape, scale, and pose of the object for rigidbody simulation, or perform dense sampling of particles within the volumes between the object surface and the table for the particle-based simulation pipeline. In both cases, we prompt the VLM to infer the relevant physical parameters required for simulation*

## 实验与关键发现

### 核心发现：物理仿真的上下文反馈带来显著性能提升

SIMPACT 在 7 项真实世界精细操控任务上均大幅超越所有基线方法（Table 2）。这些任务包括刚性物体（不倒翁推瓶、碗叠放、旋转、避障、清扫）和可变形物体（绳塑形、面团塑形），每项任务执行 10 次试验。基线方法 **π0.5**（VLA 模型）、**VoxPoser**（基于 3D 价值地图的几何规划）和 **MOKA**（基于关键点的 VLM 规划）在多数任务上接近完全失败，而 SIMPACT 取得了 40%–90% 的成功率。例如，在不倒翁推瓶任务上，SIMPACT 达到 80% 成功率，基线均为 0%；在绳塑形任务上达到 90%，基线最高仅 20%。这一差距的根本原因在于基线方法缺乏物理动力学意识，无法预测动作执行后的物体运动与受力结果，而 SIMPACT 通过仿真 rollout 为 VLM 提供了物理 grounding。

![[assets/figures/papers/paper_list_l2417_https_arxiv_org_abs_2512_05955/figures/006_Table_2.jpg]]
*Table 2: Success rates of our method and baselines. For each task, we run 10 trials per method. Our approach consistently achieves a substantially higher success rate than baselines, highlighting the effectiveness of simulation-enabled VLMs for action planning*

在 CALVIN LH-MTLC 长序列语言操控基准上，SIMPACT 的平均任务完成长度达到 2.78，超过基线最优的 2.47（Table 8），验证了该方法在标准基准上的竞争力。

![[assets/figures/papers/paper_list_l2417_https_arxiv_org_abs_2512_05955/figures/017_Table_8.jpg]]
*Table 8: Evaluation results on the CALVIN Long-Horizon Multi-Task Language Control (LH-MTLC) benchmark*

### 消融实验：每个组件均为关键瓶颈

消融实验（Table 3）系统性地移除了 SIMPACT 的三个核心模块，每一项移除都导致性能崩溃，揭示了各组件的不可替代性：

![[assets/figures/papers/paper_list_l2417_https_arxiv_org_abs_2512_05955/figures/008_Table_3.jpg]]
*Table 3: Ablation. Success rates (%) over 10 trials for each task after removing each component of our method. Results demonstrate the importance of VLM-conditioned sampling and the VLM’s simulation-enabled test-time reasoning capabilities*

1. **移除 VLM 动作采样器（替换为高斯随机采样）**：所有任务成功率急剧下降。不倒翁推瓶、旋转、面团塑形、避障等任务成功率直接从 80%/40%/80%/80% 降至 0%。这表明 VLM 基于场景理解和任务语义生成的动作提案是产生合理动作的前提，随机采样无法触及有效动作空间。

2. **移除仿真 rollout 上下文（仅依赖 VLM 内部推理）**：性能大幅下降，尤其在需要精细物理交互的任务上。碗叠放从 60% 降至 20%，旋转从 40% 降至 0%。这证明物理仿真的外部验证是 VLM 进行物理推理的必要条件，仅靠语言-视觉语义推理无法补偿动力学知识的缺失。

3. **移除 VLM 优化器（仅从初始样本中选择最佳动作）**：性能明显降低。不倒翁推瓶从 80% 降至 40%，绳塑形从 90% 降至 50%。这验证了迭代优化的重要性——初始采样往往无法直接产生可行解，VLM 需要从失败案例中推理出改进方向。

采样数量消融（Table 4）进一步揭示：3 个样本时性能不足，10 个样本达到最佳平衡，20 个样本反而因上下文过长导致部分任务性能下降。这暗示 VLM 的上下文窗口和注意力机制存在有效利用边界，需要更智能的样本筛选策略。

![[assets/figures/papers/paper_list_l2417_https_arxiv_org_abs_2512_05955/figures/011_Table_4.jpg]]
*Table 4: Sampling length ablation. Success rates (%) over 10 trials varying numbers of in-context examples for tasks non-toppling push, bowl stacking, shape rope*

### 失败模式分析：感知-规划-执行的错误链条

失败案例分解（Figure 7）将错误归类为感知错误、规划错误和执行错误三类。感知错误主要源于单视图 3D 重建引入的几何偏差，导致仿真器中的物体位姿或形状与真实世界不一致。规划错误体现为 VLM 优化器在多轮迭代后仍无法生成可行动作序列，尤其在旋转（pivoting）任务上——该任务需要精确的力-运动耦合推理，VLM 的符号化推理难以捕捉连续的接触动力学。执行错误则源于仿真与真实的动力学偏差：约 11% 的案例在仿真中成功却在真实执行中失败（Figure 12），这构成了 sim-to-real gap 的量化证据。

仿真与真实世界结果的一致性达到 89%（Figure 12），表明仿真器在大多数情况下能可靠地预测动作的物理结果。剩余 11% 的仿真成功-真实失败案例主要出现在涉及复杂接触（如碗叠放的对齐插入）和可变形物体大变形（如面团挤压）的场景中，这指明了仿真保真度提升的优先方向。

### 物理参数估计的鲁棒性与边界

VLM 估计的物理参数表现出低方差和合理范围（Table 6）：质量估计为 1.033±0.0015 kg，摩擦系数为 0.36±0.11。这种稳定性使得仿真环境在不同场景变化（物体类型、位姿、颜色、材质，Figure 13）下保持一致的物理行为。

然而，摩擦系数的极端取值会显著影响性能（Table 7）：当摩擦系数偏离合理范围时，成功率下降。这提示当前框架依赖 VLM 对物理参数的常识性估计，在超出常识分布的场景中可能失效。

### 计算开销与实时性限制

平均计算时间（Table 5）显示，整个规划循环耗时超过 5 分钟，主要瓶颈在于商业 VLM（Gemini 2.5 Pro）的多次 API 调用。仿真构建和 rollout 执行相对高效，但 VLM 采样、优化和评估的串行依赖导致总延迟无法满足实时操控需求。这一限制在当前实现中是结构性的——物理 grounding 的收益以推理延迟为代价。

### 基线对比的公平性说明

所有对比方法均以零样本方式评估，未针对这 7 项特定任务进行微调。但需注意：π0.5 的训练数据可能未覆盖此类精细操控场景，且仅使用开源版本；VoxPoser 和 MOKA 原本设计场景不同，我们虽进行了适当扩展（如为 MOKA 增加推动和挤压支持），但仍可能存在适配不完全的问题。这些因素可能使基线性能低于其最优水平，但即便考虑这些因素，SIMPACT 的领先幅度（多数任务从 0% 到 80%+）已远超可归因于不公平性的范围。

## 定位与知识库关联

### 核心差异点：物理推理的引入

SIMPACT 与现有视觉语言模型（VLM）机器人规划方法的根本区别在于，它在测试时引入了基于物理仿真的迭代推理闭环。传统 VLM 规划方法——无论是通用视觉-语言-行动（VLA）模型如 **π0.5**，还是基于几何表示的方法如 **VoxPoser** 和 **MOKA**——均直接依赖语言和图像的语义关联生成动作，缺乏对物理动力学后果的显式建模。这导致它们在需要精细物理推理的任务（如推而不倒、碗的堆叠、面团塑形）上系统性地失败（Table 2 中基线方法在多个任务上成功率为 0%）。

SIMPACT 通过三个关键机制填补了这一空白：
1. **物理仿真作为 grounding**：从单张 RGB-D 图像自动构建多物理仿真器（刚体网格仿真与可变形体粒子仿真），将 VLM 的推理锚定在可验证的物理世界中。
2. **仿真 rollout 驱动的上下文优化**：VLM 不再单次输出动作序列，而是通过多轮仿真 rollout 观察动作的物理后果，利用 in-context learning 从失败案例中推理改进策略（Fig. 4）。
3. **层次化动作表示**：VLM 在符号动作层面进行采样和推理，通过 ACTION2POSE 映射为连续 6-DoF 轨迹，将 VLM 的语义理解与机器人执行解耦。

### 与基线方法的系统对比

| 维度 | π0.5 | VoxPoser | MOKA | SIMPACT (本方法) |
|------|------|----------|------|-------------------|
| **物理推理** | 无动态模型 | 无动态模型 | 无动态模型 | 多物理仿真器 + rollout 验证 |
| **动作生成** | 端到端预测关节速度 | VLM + 3D 价值地图 | 关键点/交互区域规划 | VLM 符号采样 + 仿真迭代优化 |
| **优化策略** | 单次推理 | 单次推理 | 单次推理 | 基于失败经验的上下文优化 |
| **适用任务** | 通用操控（训练数据覆盖范围内） | 几何约束任务 | 基于关键点的交互任务 | 精细物理推理任务（推、堆、塑形等） |

**π0.5** 作为 VLA 模型，在大规模机器人数据上训练，直接预测关节速度。然而其训练数据可能未覆盖本论文定义的精细操控任务，且仅使用开源版本，在 non-toppling push、pivoting、shape dough 等任务上成功率为 0%（Table 2）。这表明纯数据驱动的方法在物理推理层面的泛化能力存在根本性局限。

**VoxPoser** 通过 VLM 生成 3D 价值地图来约束动作空间，本质上是一种几何推理方法。它在 bowl stacking 和 shape rope 任务上取得了 20% 的成功率，但当任务需要预测物体在受力后的动力学行为（如推瓶子时避免倾倒）时完全失效。

**MOKA** 基于关键点和交互区域进行规划，论文为其扩展了推动和挤压支持。在 bowl stacking 和 sweeping 任务上有 20% 的成功率，但在需要精确力控和动力学预测的任务上同样失败。

### 适用边界与局限

#### 1. 感知瓶颈：单视图 3D 重建
SIMPACT 的仿真构建依赖从单张 RGB-D 图像进行分割、3D 重建和位姿估计。这一流程引入了不可忽视的感知误差——Figure 7 的失败案例分解显示，感知失败是三大失败类别之一。当物体严重遮挡或具有复杂几何形状时，重建质量下降直接导致仿真不准确，进而影响规划成功率。

#### 2. 仿真与现实的动力学偏差
尽管仿真与真实世界结果的一致性达到 89%（Fig. 12），仍有 11% 的案例出现“仿真成功、真实失败”的情况。这种 sim-to-real gap 主要源于物理参数估计误差和仿真器本身的简化假设。例如，Table 7 显示当摩擦系数 μ 偏离合理范围时，成功率显著下降。当前框架主要针对准静态任务设计，对于动态任务（如快速移动物体、抛掷、击打）可能不适用。

#### 3. 推理延迟与模型依赖
规划循环依赖商业 VLM（Gemini 2.5 Pro），单次规划的总计算时间超过 5 分钟（Table 5），无法满足实时性要求。此外，对商业 API 的依赖限制了可复现性和部署灵活性。消融实验（Table 4）还揭示了一个有趣的瓶颈：动作采样数量从 10 个增加到 20 个时，部分任务性能反而下降，表明过长的上下文可能损害 VLM 的推理质量。

#### 4. 优化能力的任务依赖性
对于 pivoting 任务，即使经过多轮优化，成功率仅为 40%（Table 2），且消融实验显示移除优化器对该任务的影响相对较小（Table 3）。这表明 VLM 优化器在某些复杂物理交互任务上的推理能力有限，可能无法仅通过失败案例的上下文学习找到可行解。

### 开放问题与未来方向

1. **仿真保真度的进一步提升**：能否通过系统辨识或多视图融合减少 sim-to-real 差距？Figure 15 展示了重规划机制——在真实执行失败后更新仿真并重新规划——这可能是闭环改进的可行路径。

2. **动态任务的扩展**：当前框架假设准静态交互，能否将物理仿真和 VLM 推理扩展到动态操控任务（如击球、抛接）？

3. **推理效率的优化**：能否用更小、更高效的本地 VLM 替代商业模型以降低延迟和成本？或者通过缓存和复用仿真结果来减少重复计算？

4. **复杂场景的扩展性**：当场景包含大量物体时，仿真构建的计算复杂度和 VLM 的上下文长度管理将面临挑战。需要更高效的场景表示和样本选择机制。

5. **闭环重规划与学习**：Figure 15 展示了初步的重规划能力，但能否将真实世界的执行结果系统性地反馈到仿真模型和 VLM 优化器中，形成持续改进的闭环系统？

6. **物理参数估计的主动校准**：当前 VLM 估计的物理参数具有低方差（质量 1.033±0.0015 kg，Table 6），但在极端参数下性能下降。能否通过主动探索和系统辨识来校准这些参数？

## 原文 PDF

![[paperPDFs/CVPR_2026/SIMPACT_Simulation_Enabled_Action_Planning_using_Vision_Language_Models.pdf]]

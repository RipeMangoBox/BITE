---
title: "PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/PhysMoDPO:_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization.pdf"
project_link: "https://mael-zys.github.io/PhysMoDPO/"
code_link: null
aliases:
- PhysMoDPO
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将预训练WBC作为黑盒物理验证器，计算跟踪后的物理奖励与任务奖励，并据此构造偏好数据，通过DPO直接优化扩散生成器，使其生成的运动在WBC修正后仍保持条件一致性与物理可行性。
primary_logic: 在后训练阶段引入基于物理跟踪的偏好优化，无需测试时投影或额外模块，即可使生成的运动同时满足物理真实感和任务指令。
claims:
- 在HumanML3D文本到运动任务上，PhysMoDPO的R@3从MotionStreamer的0.8310提升至0.8517，Jerk从46.75降至43.60，同时FID也有所改善。
- 在HumanML3D空间控制任务上，PhysMoDPO将空间控制误差（Err）从OmniControl原始训练的0.1998降至0.1298，且FID大幅降至0.93。
- 零样本迁移到Unitree G1机器人后，PhysMoDPO在文本一致性、运动平滑度和稳定性上均优于MaskedMimic和MotionStreamer/OmniControl。
- HumanML3D (text-to-motion, after simulation) 上 R@3 ↑ = 0.8517
---

# PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization

> [!tip] 核心洞察
> 在后训练阶段引入基于物理跟踪的偏好优化，无需测试时投影或额外模块，即可使生成的运动同时满足物理真实感和任务指令。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysMoDPO：基于偏好优化的物理合理人形机器人运动生成 |
| 英文题名 | PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13228) · [Project](https://mael-zys.github.io/PhysMoDPO/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PhysMoDPO |
| Dataset | HumanML3D, OMOMO, Unitree G1 |

> [!tip] 效果简介
> - HumanML3D (text-to-motion, after simulation) 上，R@3 ↑ 0.8517 vs 0.8310 (MotionStreamer) (+0.0207)；Jerk ↓ 43.60 vs 46.75 (MotionStreamer) (-3.15)。
> - HumanML3D (spatial-text control, cross-control) 上，Err ↓ 0.0923 vs 0.1998 (OmniControl, original training) (-0.1075)。
> - OMOMO (spatial-text control, cross-control) 上，Jerk ↓ 76.49 vs 161.95 (OmniControl, original training) (-85.46)。

## 概述

**核心问题**：扩散模型生成的关节运动在运动学空间看似合理，但由全身控制器（WBC）在物理仿真中执行时，会因违反动力学与接触约束而产生大幅修正，导致实际机器人运动偏离预期甚至失败。

**方法定位**：PhysMoDPO 是一种物理引导的后训练框架，将预训练 WBC 作为黑盒物理验证器，计算跟踪后的物理奖励与任务奖励并构造偏好数据，通过直接偏好优化（DPO）微调扩散生成器，使其生成的运动在 WBC 修正后仍保持条件一致性与物理可行性。与以往方法相比，PhysMoDPO 使用动力学感知奖励，无需测试时优化或额外可训练模块。

**核心洞察**：在后训练阶段引入基于物理跟踪的偏好优化，无需测试时投影或额外模块，即可使生成的运动同时满足物理真实感和任务指令。

**主要结果**：
- 在 HumanML3D 文本到运动任务上，R@3 从 MotionStreamer 的 0.8310 提升至 0.8517，Jerk 从 46.75 降至 43.60，FID 也有所改善。
- 在空间控制任务上，控制误差从 OmniControl 的 0.1998 降至 0.1298，FID 大幅降至 0.93。
- 零样本迁移到 Unitree G1 机器人后，PhysMoDPO 在文本一致性、运动平滑度和稳定性上均优于 **MaskedMimic**（Tessler et al., ACM TOG 2024）和 MotionStreamer/OmniControl 等基线方法。

**当前局限**：方法仅在平坦地面上验证，未涉及楼梯、斜坡等复杂地形；奖励评估完全依赖预训练模型，其偏差可能影响偏好构造质量；未利用真实人类反馈，自动奖励设计可能无法完全捕捉人类对运动自然度的感知。

## 背景与动机

### 问题背景：从运动学生成到物理部署的鸿沟

扩散模型在文本驱动的人体运动生成领域取得了显著进展，能够产生运动学空间（kinematic space）中看似自然且符合文本描述的关节运动序列。然而，当这些生成的运动被部署到物理仿真器或真实机器人上时，一个根本性问题暴露出来：**运动学上合理的运动，在物理世界中往往不可执行**。

这一鸿沟的根源在于，扩散生成器仅学习运动数据的统计分布，并不理解动力学约束（如接触力、动量守恒、地面反作用力）。当预训练的全身控制器（Whole-Body Controller, WBC）试图跟踪这些运动学轨迹时，会因轨迹违反物理定律而产生大幅修正。这种修正不仅导致实际执行的轨迹偏离生成器的原始意图，还可能引发脚部滑动、关节抖动甚至机器人失稳跌倒。换言之，**生成器输出的运动学序列与经过物理跟踪后实际得到的轨迹之间存在显著的“跟踪失真”（tracking distortion）**，而现有方法在训练阶段完全忽略了这一失真。

### 现有物理融入方法的局限

为缓解上述问题，已有工作尝试在运动生成中引入物理约束，大致可分为三类：

- **手工惩罚项**：如 **ReinDiffuse** 和 **HY-Motion** 等方法在训练或推理时加入浮空惩罚、脚部滑动惩罚等启发式损失。这些惩罚项虽然直观，但仅捕捉了物理违规的浅层信号，无法反映完整的动力学交互，且权重调参依赖经验，泛化性有限。
- **测试时优化**：部分方法在推理阶段对生成的运动进行额外的物理投影或优化，以使其满足约束。这增加了推理开销，且优化过程可能与原始条件信号（如文本语义）产生冲突，导致条件一致性下降。
- **纯物理驱动生成**：如 **MaskedMimic**（Tessler et al., ACM TOG 2024）直接在仿真环境中输出可执行的动作，天然保证物理可行性。然而，这类方法受限于仿真环境的探索难度和稀疏奖励，其文本一致性和运动多样性往往弱于运动学空间的生成方法。

上述方法的共同缺陷在于：**它们要么在错误的评估空间（运动学空间）中优化，要么依赖手工设计的物理信号，缺乏一种系统性的机制来弥合运动学生成与物理执行之间的鸿沟**。

### 核心动机：将物理验证纳入后训练闭环

本文的核心洞察是：**不应在运动学空间直接评判生成器的质量，而应以经过物理跟踪后的实际轨迹作为评估和优化的依据**。具体而言，可以将预训练的WBC视为一个黑盒物理验证器——它接收运动学运动，输出物理可行的轨迹，并在此过程中产生丰富的动力学感知信号（如跟踪误差、接触滑动等）。这些信号恰好可以作为反馈，指导生成器学习产生“WBC修正后仍保持条件一致性与物理可行性”的运动。

基于这一动机，PhysMoDPO提出了一种**物理引导的后训练框架**：在后训练阶段，利用固定的WBC对生成样本进行滚动仿真，计算物理奖励与任务奖励，并据此构造偏好数据，通过直接偏好优化（DPO）迭代微调扩散生成器。该方法无需测试时投影、无需额外可训练模块，也无需手工设计惩罚权重，即可使生成的运动同时满足物理真实感和任务指令。

## 核心创新

PhysMoDPO的核心创新在于**将物理仿真验证从测试时后处理迁移到训练时偏好优化**，从而解决扩散模型生成的运动在真实机器人上部署时因动力学约束导致的严重失真问题。其关键设计围绕三个“changed slots”展开：

### 1. 物理反馈信号：从手工惩罚到动力学感知奖励

以往方法（如ReinDiffuse、HY-Motion）依赖手工定义的浮空惩罚、脚滑惩罚等静态规则来评估物理合理性，这类信号与真实物理仿真之间存在系统偏差。PhysMoDPO采用**固定的全身控制器（WBC，基于DeepMimic）作为黑盒物理验证器**，将生成的运动学序列 $X$ 送入仿真环境滚动出实际可执行轨迹 $X' = \mathcal{T}(X)$，然后在 $X'$ 上计算两类动力学感知奖励：

- **跟踪奖励** $\mathcal{R}_{\mathrm{track}}(X', X) \triangleq -\|X' - X\|_2^2$：度量物理修正幅度，修正越大说明原始运动越违反动力学约束；
- **滑动奖励** $\mathcal{R}_{\mathrm{slide}}$：惩罚仿真中脚部与地面的相对滑动，直接反映接触约束的满足程度。

这一设计的关键优势在于：奖励信号直接来源于物理仿真的真实反馈，而非人类对物理规律的近似建模，从而更准确地反映运动在部署后的实际表现。

### 2. 偏好构造策略：从标量融合到严格支配性选择

给定同一条件 $C$ 下的 $K$ 个候选运动 $X_1, \dots, X_K$，传统方法将多维奖励标量化加权求和（分数融合），选出一个总分最高的样本作为“胜者”。这种做法存在严重缺陷：一个在某个维度表现极好但在其他维度表现很差的样本，可能因总分高而被选为胜者，导致优化信号偏离真实需求。

PhysMoDPO采用**严格的支配性选择（Dominance-based Preference）**：

$$\mathcal{R}(X_k', C) \succ \mathcal{R}(X_l', C) \iff \mathcal{R}_s(X_k', C) > \mathcal{R}_s(X_l', C) \ \forall s \in \mathcal{S}(C)$$

即胜者必须在**所有奖励维度上均严格优于负者**，才能构成偏好对。消融实验（Table 3(b)）证实，支配性选择在所有指标上均优于分数融合：空间控制误差从0.1476降至0.1421，FID从1.61降至1.17。这一设计的深层逻辑是：物理可行性是一个整体约束，任何维度的缺陷都可能导致部署失败，因此“全面优于”比“总分更高”更符合实际需求。

### 3. 训练目标与评估空间：闭环优化与部署后评估

PhysMoDPO的训练目标结合了DPO损失与仅作用于胜者的SFT损失：

$$\mathcal{L} = \mathcal{L}_{\mathrm{DPO}}(X_{\mathrm{win}}, X_{\mathrm{lose}}) + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}}(X_{\mathrm{win}})$$

SFT项的作用是防止DPO优化过程中生成质量退化，确保胜者样本的似然不会因偏好优化而下降。

更重要的是，PhysMoDPO将**评估空间从运动学空间迁移到物理跟踪后的轨迹空间**。传统方法直接评估生成样本 $X$ 的FID、R-Precision等指标，但这些指标无法反映部署后的实际表现——一个在运动学空间看似完美的运动，经WBC修正后可能面目全非。PhysMoDPO在所有实验中均在 $X' = \mathcal{T}(X)$ 上计算指标（如 $\text{FID}_{\text{after\_sim}}$、Jerk、空间控制误差Err），直接衡量“机器人实际执行的效果”，这使得评估结果与真实部署表现高度一致。

### 方法谱系与知识库定位

PhysMoDPO属于**物理感知的运动生成后训练**这一新兴范式。与现有工作的关键区别如下：

| 方法 | 物理约束引入方式 | 是否需要测试时优化 | 是否需要额外可训练模块 |
|------|-----------------|-------------------|---------------------|
| **MaskedMimic** (Tessler et al., ACM TOG 2024) | 纯物理驱动，直接输出仿真动作 | 否 | 否（但文本一致性弱） |
| **ReinDiffuse** | 手工物理惩罚 + 强化学习微调 | 否 | 是（奖励模型） |
| **HY-Motion** | 测试时投影到物理可行集 | 是 | 否 |
| **PhysMoDPO** | WBC跟踪反馈 + DPO偏好优化 | 否 | 否 |

PhysMoDPO的独特优势在于：**无需测试时优化或额外模块**，仅通过后训练即可使生成的运动同时满足物理真实感和任务指令。其核心洞察是：将WBC视为不可微的物理验证器，通过偏好排序间接优化生成器，避免了直接通过仿真器反向传播梯度的困难。

## 整体框架

PhysMoDPO 的核心思路是将预训练的全身控制器（WBC）作为黑盒物理验证器，在后训练阶段通过偏好优化使扩散生成器学会生成“跟踪后仍保持条件一致性”的运动。整体流程可概括为四个模块的闭环。

**1. 条件扩散生成器**  
给定条件信号 $C$（文本描述，或文本+稀疏关节控制），预训练的扩散模型从噪声 $\epsilon \sim \mathcal{N}(0, I)$ 采样运动学运动序列 $X = G_\theta(\epsilon, C) \in \mathcal{X}_{\mathrm{kin}}$。骨干模型可以是 **MotionStreamer**（Xiao et al., ICCV 2025，用于文本到运动）或 **OmniControl**（Xie et al., arXiv 2023，用于空间-文本联合控制）。

**2. 物理跟踪控制器（WBC）**  
固定的物理跟踪算子 $\mathcal{T} : \mathcal{X}_{\mathrm{kin}} \to \mathcal{X}_{\mathrm{phys}}$ 将运动学运动投影到物理仿真中，产生可执行轨迹 $X' = \mathcal{T}(X)$。该控制器基于 DeepMimic 实现，在训练和评估中均保持冻结。跟踪偏差 $\Delta(X) \triangleq \|X' - X\|_2^2$ 量化了物理修正的幅度——这正是传统方法在部署时性能退化的根源。

**3. 奖励计算**  
在跟踪轨迹 $X'$ 上计算两类奖励：
- **物理奖励**：跟踪奖励 $\mathcal{R}_{\mathrm{track}}(X', X) = -\|X' - X\|_2^2$ 和滑动惩罚 $\mathcal{R}_{\mathrm{slide}}$（基于脚部接触速度）；
- **任务奖励**：文本-运动对齐分数 $\mathcal{R}_{\mathrm{M2T}}$（由 TMR 模型评估）和空间控制误差 $\mathcal{R}_{\mathrm{control}}$（末端执行器位置偏差）。

**4. DPO 后训练**  
对每个条件 $C$，利用扩散模型的随机性采样 $K$ 个候选运动 $\{X_k\}_{k=1}^K$，经 WBC 跟踪后获得 $\{X_k'\}$ 并计算奖励。偏好对选择采用严格的**支配性策略**：当且仅当胜者在所有奖励维度上均优于负者时，才构成偏好关系 $\mathcal{R}(X_{k^+}', C) \succ \mathcal{R}(X_{k^-}', C)$。训练目标结合 DPO 损失与仅作用于胜者的 SFT 损失：

$$\mathcal{L} = \mathcal{L}_{\mathrm{DPO}}(X_{\mathrm{win}}, X_{\mathrm{lose}}) + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}}(X_{\mathrm{win}})$$

该过程迭代进行：每轮更新生成器后，用改进的模型重新采样候选并构建偏好对，逐步将生成分布推向物理可行区域。

**关键设计决策**：与 **MaskedMimic**（Tessler et al., ACM TOG 2024）直接在仿真中输出动作不同，PhysMoDPO 保留了运动学空间的生成灵活性；与 ReinDiffuse、HY-Motion 等使用手工惩罚项的方法不同，PhysMoDPO 通过 WBC 滚动出完整仿真轨迹来获取动力学感知的奖励信号，无需测试时投影或额外可训练模块（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/003_Figure_2.jpg]]
*Figure 2: Overview of PhysMoDPO. Given a conditioning signal (text and optional joint controls), we sample multiple motions X from a pretrained generator. A fixed physics-based tracking policy then projects each sample into a simulated trajectory*

## 核心模块与公式推导

PhysMoDPO 的核心架构由四个模块级联构成，形成一个闭环的“生成—跟踪—评估—优化”管线。

**模块 1：扩散运动生成器（Diffusion Motion Generator）**
预训练的条件扩散模型 $G_\theta$，将高斯噪声 $\epsilon \sim \mathcal{N}(0, I)$ 与条件信号 $C$（文本描述、可选的空间关节控制）映射到运动学运动序列：

$$G_{\theta} : \mathcal{E} \times \mathcal{C} \to \mathcal{X}_{\mathrm{kin}}, \quad X = G_{\theta}(\epsilon, C) \in \mathcal{X}_{\mathrm{kin}}$$

该模块是 PhysMoDPO 的优化对象。论文中分别以 **MotionStreamer**（Xiao et al., ICCV 2025）作为文本到运动任务的骨干，以 **OmniControl**（Xie et al., arXiv 2023）作为空间控制任务的骨干。

**模块 2：物理跟踪策略（Physics-based Tracking Policy）**
固定的全身控制器（WBC），基于 DeepMimic 实现，将运动学运动投影到物理仿真中，产生可执行的物理轨迹：

$$\mathcal{T} : \mathcal{X}_{\mathrm{kin}} \to \mathcal{X}_{\mathrm{phys}}, \quad X' = \mathcal{T}(X)$$

该模块在训练和推理阶段均作为黑盒使用，不参与梯度更新。它揭示了一个关键瓶颈：运动学上合理的运动 $X$ 在物理执行后可能产生显著的跟踪畸变 $\Delta(X) \triangleq \|X' - X\|_2^2$。

**模块 3：奖励计算（Reward Computation）**
在跟踪轨迹 $X'$ 上计算两类奖励，共同构成偏好排序的依据：

- **物理奖励**：包括跟踪奖励 $\mathcal{R}_{\mathrm{track}}(X', X) \triangleq -\|X' - X\|_2^2$ 和接触滑动奖励 $\mathcal{R}_{\mathrm{slide}}$，后者惩罚脚部与地面的相对滑动。
- **任务奖励**：文本-运动对齐奖励 $\mathcal{R}_{\mathrm{M2T}}$（由预训练 TMR 模型提供）和空间控制误差奖励 $\mathcal{R}_{\mathrm{control}}$。

**模块 4：DPO 后训练（DPO Post-Training）**
对每个条件 $C$，利用扩散模型的随机性采样 $K$ 个候选运动学样本 $X_k = G_\theta(\epsilon_k, C)$，经 $\mathcal{T}$ 跟踪后计算奖励 $r_k = \mathcal{R}(X_k', C)$。偏好对的选择采用严格的**支配性准则**：

$$\mathcal{R}(X_k', C) \succ \mathcal{R}(X_l', C) \iff \mathcal{R}_s(X_k', C) > \mathcal{R}_s(X_l', C) \ \forall s \in \mathcal{S}(C)$$

即胜者必须在所有奖励维度上均优于负者。基于构造的偏好对 $(X_{\mathrm{win}}, X_{\mathrm{lose}})$，后训练目标结合 DPO 损失与仅作用于胜者的 SFT 损失：

$$\mathcal{L} = \mathcal{L}_{\mathrm{DPO}}(X_{\mathrm{win}}, X_{\mathrm{lose}}) + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}}(X_{\mathrm{win}})$$

其中 $\lambda_{\mathrm{SFT}}$ 平衡两项损失，$\beta$ 为 Diffusion-DPO 的温度参数。训练以迭代方式进行：每轮更新生成器后重新采样候选并重建偏好对，消融实验表明 3 轮迭代持续改善所有指标（MPJPE 从 0.0456 降至 0.0368，FID 从 1.17 降至 0.93）。

**关键设计选择**：与将多维奖励标量化加权的“分数融合”策略相比，支配性偏好选择在空间控制任务上取得了更优的 FID（1.17 vs 1.61）和控制误差（0.1421 vs 0.1476），验证了严格偏好的重要性。添加滑动奖励 $\mathcal{R}_{\mathrm{slide}}$ 进一步改善了 FID（1.45→1.21）和 Jerk（74.47→68.43）。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/002_Table_1.jpg]]
*Table 1: Comparison with previous work. We compare alternative ways of incorporating physics constraints into human motion generation. In contrast to other methods, PhysMoDPO make use of dynamics-aware reward and does not require test-time optimization nor additional trainable modules*

## 实验与分析

### 核心发现：物理后训练实现运动学质量与物理可行性的协同提升

PhysMoDPO 的核心主张是：在 WBC 跟踪后的物理轨迹上评估生成质量，并通过 DPO 直接优化扩散生成器，可以同时改善运动学分布匹配和物理合理性。实验在 HumanML3D 和 OMOMO 两个数据集上，覆盖文本到运动和空间-文本控制两类任务，所有评估均在 WBC 跟踪后的物理轨迹上进行。

**文本到运动任务（Table 2）**：在 HumanML3D 上，PhysMoDPO 以 **MotionStreamer**（Xiao et al., ICCV 2025）为骨干，在文本一致性（R@3 0.8517 vs 0.8310）、运动平滑度（Jerk 43.60 vs 46.75）和分布匹配（FID 48.29 vs 52.02）上全面超越 MotionStreamer 原始模型。与纯物理驱动的 **MaskedMimic**（Tessler et al., ACM TOG 2024）相比，PhysMoDPO 在文本一致性上优势显著（R@3 0.8517 vs 0.7988），同时保持可比的物理稳定性（FootSlide 4.03 vs 3.93）。这表明 DPO 后训练成功在保持物理合理性的同时，保留了扩散模型强大的条件生成能力。

**空间-文本控制任务（Table 3）**：以 **OmniControl**（Xie et al., arXiv 2023）为骨干，PhysMoDPO 在 HumanML3D 上将空间控制误差（Err）从 0.1998（原始训练）降至 0.1298，同时 FID 从 2.04 大幅降至 0.93。在 OMOMO 数据集上，Jerk 从 161.95 降至 76.49，降幅超过 50%。值得注意的是，OmniControl 在使用测试时投影（test-time projection）时虽能降低控制误差，但会严重损害生成质量（FID 升至 2.04）；PhysMoDPO 无需任何测试时优化即实现了更优的控制精度和生成质量。

### 消融实验：迭代轮数、奖励设计与偏好选择策略

消融实验（Table 6）揭示了几个关键机制：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/011_Table_6.jpg]]
*Table 6: Ablation studies. We train OmniControl [52] and study the impact of the number of iterative training round and different rewards on HumanML3D [6] dataset. The best results are in bold*

**迭代轮数（Table 6a）**：从 1 轮到 3 轮，所有指标持续改善——MPJPE 从 0.0456 降至 0.0368，Err 从 0.1421 降至 0.1298，FID 从 1.17 降至 0.93，Jerk 从 72.13 降至 62.31。这验证了“采样-评估-优化”循环的有效性：每轮迭代中，改进后的生成器产生更高质量的候选样本，进而构造出更具信息量的偏好对。

**奖励组件（Table 6b）**：添加滑动奖励 $R_{\text{slide}}$ 后，FID 从 1.45 降至 1.21，Jerk 从 74.47 降至 68.43。仅使用跟踪奖励 $R_{\text{track}}$ 时，模型倾向于生成“保守”运动以最小化跟踪误差，但可能牺牲运动多样性；引入接触滑动惩罚后，模型被迫学习同时满足跟踪精度和接触物理的运动模式。

**偏好选择策略（Table 3b 消融）**：支配性选择（Dominance）在所有指标上均优于分数融合（Fuse score）——Err 0.1421 vs 0.1476，FID 1.17 vs 1.61。分数融合将多维奖励加权求和为标量，可能导致某一维度的退化被其他维度的改进所掩盖；支配性选择要求胜者在**所有**奖励维度上均优于负者，确保优化方向不会牺牲任何单一物理或任务约束。

**超参数敏感性（Table 4）**：$\lambda_{\text{SFT}}=2$、$\beta=20$ 达到最佳综合性能。过大的 $\lambda_{\text{SFT}}$（如 10）会导致模型过度拟合胜者样本，丧失 DPO 带来的对比学习优势；过小或过大的 $\beta$ 分别导致偏好信号过弱或梯度消失。

### 零样本迁移：从 SMPL 仿真到真实人形机器人

PhysMoDPO 在 SMPL 角色上训练后，直接迁移到 Unitree G1 和 H1 机器人，无需任何微调。

**G1 机器人文本到运动（Table 4）**：PhysMoDPO 在文本一致性（R@3 0.7640 vs MotionStreamer 0.7558）和平滑度（Jerk 34.91 vs 38.30）上均优于 MotionStreamer，同时保持与 MaskedMimic 可比的稳定性（FootSlide 3.03 vs 2.93）。MaskedMimic 虽在物理稳定性上表现最佳，但其文本一致性显著弱于 PhysMoDPO（R@3 0.6954 vs 0.7640），说明纯物理驱动策略牺牲了条件控制能力。

**G1 机器人空间控制（Table 5）**：PhysMoDPO 在 HumanML3D 上将控制误差从 OmniControl 的 0.1998 降至 0.1298，FID 从 2.04 降至 1.06。在 OMOMO 上，Jerk 从 161.95 降至 78.45。H1 机器人的零样本结果（Table 1 appendix）进一步验证了跨形态迁移的鲁棒性。

**用户研究（Figure 5）**：在真实 G1 机器人上，PhysMoDPO 在文本一致性、运动平滑度和整体稳定性三个维度上均显著优于 MaskedMimic 和 OmniControl，证实了自动指标与人类感知的一致性。

### 失败模式与局限性

1. **地形限制**：所有实验在平坦地面上进行，未验证楼梯、斜坡等复杂地形，限制了在非结构化环境中的部署。
2. **奖励模型偏差**：物理奖励 $R_{\text{track}}$ 和 $R_{\text{slide}}$ 完全依赖固定 WBC 的跟踪结果，若 WBC 本身对某些运动（如快速旋转、空中动作）跟踪能力不足，将产生噪声偏好信号。
3. **自动奖励的感知盲区**：未利用真实人类反馈，自动奖励可能无法完全捕捉人类对运动自然度的感知（如风格、韵律），需人工验证。
4. **WBC 依赖性**：方法假设 WBC 作为黑盒物理验证器，若更换控制器（如从 DeepMimic 到更先进的全身控制器），需重新验证奖励信号的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/004_Table_2.jpg]]
*Table 2: Evaluation of text-driven human motion generation with SMPL robot simulation on HumanML3D [6] dataset. We evaluate MaskedMimic [42], MotionStreamer [50] and PhysMoDPO with text-conditioned generation setting as in MotionStreamer [50]. The best results are in bold, and the second best results are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/005_Table_3.jpg]]
*Table 3: Evaluation of spatial-text human motion controllability with SMPL character control. Left: HumanML3D [6]. Right: OMOMO [15]. We evaluate MaskedMimic [42], OmniControl [52] under two training settings and PhysMoDPO with cross-control setting as in OmniControl [52]. The best results are in bold, and the second best results are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/007_Table_4.jpg]]
*Table 4: Evaluation of text-driven human motion generation with G1 robot on HumanML3D [6] dataset. We evaluate MaskedMimic [42], MotionStreamer [50] and PhysMoDPO with text-conditioned generation setting as in MotionStreamer [50]. The best results are in bold, and the second best results are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/008_Table_5.jpg]]
*Table 5: Evaluation of human motion controllability with G1 robot. Left: HumanML3D [6]. Right: OMOMO [15]. We evaluate MaskedMimic [42], OmniControl [52] and PhysMoDPO with cross-control setting as in OmniControl [52]. The best results are in bold, and the second best results are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/010_Figure_5.jpg]]
*Figure 5: User study. Comparison of real-robot motion sequences generated by PhysMoDPO, MaskedMimic [42] and OmniControl [52]. PhysMoDPO outperform both competitors in terms of text adherence, motion smoothness and overall stability*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/012_Table_1.jpg]]
*Table 1: Evaluation of zero-shot human motion controllability with H1 robot on HumanML3D [6] dataset. We apply the models trained with SMPL simulation and then perform zero-shot evaluation for Unitree H1 robot. The best results are in bold, and the second best results are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/014_Table_2.jpg]]
*Table 2: Ablation of data representation. We compare OmniControl [52] model trained on different data representations. Numbers are calculated without applying tracking policy. The best results are in bold*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/015_Table_3.jpg]]
*Table 3: Ablation studies. We train OmniControl [52] and study the impact of the data scale and preference pair selection strategies on HumanML3D [6] dataset. The best results are in bold*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_13228/figures/016_Table_4.jpg]]
*Table 4: Ablation study on hyperparameters. Here*

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

扩散模型在运动学空间生成的人形运动序列，在视觉上可能流畅自然，但一旦交由物理仿真中的全身控制器（WBC）执行，就会暴露出根本性断裂：运动学样本违反动力学约束和接触条件，迫使WBC进行大幅修正，导致实际机器人轨迹偏离预期甚至完全失败。PhysMoDPO的因果杠杆在于**将预训练的WBC作为黑盒物理验证器**——对生成的运动学样本进行仿真跟踪，计算跟踪后的物理奖励与任务奖励，据此构造偏好数据，通过DPO直接优化扩散生成器，使其生成的运动在被WBC修正后仍保持条件一致性与物理可行性。核心洞察是：**在后训练阶段引入基于物理跟踪的偏好优化，无需测试时投影或额外模块，即可使生成的运动同时满足物理真实感和任务指令。**

### 方法对比与定位

PhysMoDPO位于**物理感知的运动生成**这一交叉地带，与三类方法形成鲜明对比：

**纯运动学生成方法**（如MotionStreamer、OmniControl）直接在运动学空间优化，评估指标（FID、R-Precision）不反映物理可行性。PhysMoDPO的关键区分在于：所有评估均在WBC跟踪后的物理轨迹上进行（$X'$而非$X$），从根本上改变了优化目标。

**纯物理驱动方法**（如**MaskedMimic**，Tessler et al., ACM TOG 2024）直接在仿真中输出可执行动作，天然保证物理可行性，但文本一致性和运动多样性显著弱于运动学方法。PhysMoDPO保留了扩散模型在运动学空间的表达能力，通过后训练注入物理感知，在物理可行性与条件一致性之间取得平衡。

**物理奖励引导方法**（如ReinDiffuse、HY-Motion）通常依赖手工定义的浮空、脚滑惩罚，或采用标量化的奖励加权求和来构造偏好对。PhysMoDPO的改进体现在两个关键设计选择上（见表3(b)消融）：(1) **动力学感知奖励**：通过固定WBC滚动出仿真轨迹，计算跟踪误差（$R_\text{track}$）与接触滑动（$R_\text{slide}$），而非简单的运动学惩罚；(2) **支配性偏好选择**：要求胜者在所有奖励维度上均严格优于负者（$\mathcal{R}_s(X'_\text{win}) > \mathcal{R}_s(X'_\text{lose}), \forall s$），而非标量化融合，避免了多目标冲突时的噪声偏好。

与需要测试时优化（如投影到物理可行域）或额外可训练模块的方法不同，PhysMoDPO将物理约束完全内化到生成器权重中，测试时仅需单次前向传播，部署效率与原始扩散模型一致。

### 适用边界与局限

**已验证的适用场景**：
- 平坦地面上的文本到运动生成（HumanML3D数据集）
- 稀疏关节空间控制下的运动生成（HumanML3D和OMOMO数据集）
- 零样本迁移到Unitree G1和H1人形机器人（仿真与真实部署）

**明确局限**（需在后续研究中验证）：
1. **地形限制**：当前仅在平坦地面上验证，未考虑楼梯、斜坡等复杂地形，限制了在真实非结构化环境中的部署能力。
2. **奖励模型的偏差**：奖励评估完全基于预训练模型（WBC和TMR），这些模型自身的偏差可能影响偏好构造的质量。若WBC对某些运动类型跟踪鲁棒性不足，优化信号将受到污染。
3. **自动奖励的感知盲区**：未利用真实人类反馈，自动设计的奖励函数可能无法完全捕捉人类对运动自然度的感知维度（如风格、表现力）。
4. **控制器依赖性**：方法依赖固定的DeepMimic控制器；若替换为更先进的全身控制器，可能覆盖更广泛的运动类型，但框架本身需要验证与新控制器的兼容性。

### 开放问题

1. **复杂场景扩展**：如何将偏好优化范式扩展到多样化地形和需要物体交互的场景？这可能需要设计地形感知的奖励项或引入接触丰富的仿真环境。
2. **人类反馈融合**：能否在偏好构造中融入人工排序或真实人类反馈，以进一步提升感知质量？这涉及将RLHF范式适配到物理运动生成领域。
3. **控制器升级**：用更鲁棒的全身控制器（如基于MPC的方法）替换DeepMimic，是否能覆盖更极端的运动类型（如跳跃、后空翻）？
4. **采样效率**：DPO的迭代轮数和每轮采样预算（$K$）是否存在更高效的分配策略？当前消融显示3轮迭代持续改善（Table 6a），但最优轮数可能依赖于任务和模型规模。
5. **多机器人泛化**：零样本迁移到G1和H1的结果表明框架具有一定的形态泛化能力，但这种泛化的边界在哪里？是否需要针对不同机器人本体进行适配？

## 原文 PDF

![[paperPDFs/arxiv_2026/PhysMoDPO:_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization.pdf]]
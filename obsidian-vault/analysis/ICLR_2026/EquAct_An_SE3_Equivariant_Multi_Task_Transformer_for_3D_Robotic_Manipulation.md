---
title: "EquAct: An SE(3)-Equivariant Multi-Task Transformer for 3D Robotic Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EquAct_An_SE3_Equivariant_Multi_Task_Transformer_for_3D_Robotic_Manipulation.pdf
project_link: null
code_link: https://github.com/ZXP-S-works/EquAct
openreview_forum_id: d1wuA8oIH0
aliases:
- EquAct
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过引入连续的SE(3)等变性（覆盖3D旋转和平移）以及语言指令的SE(3)不变性，使策略可以根据观测的刚体变换等变地调整动作，同时保持语义条件的不变性。"
primary_logic: "结合球面傅里叶特征实现高效、连续的SE(3)等变点云推理，并首次在统一模型中同时实现多任务语言条件化，利用等变场网络一次性评估全SE(3)动作空间，从而实现快速、准确的位姿预测。"
claims:
- "EquAct在18个RLBench任务上，在SE(2)/100、SE(2)/10和SE(3)/10三种设置下，平均成功率均显著超过所有基线。"
- "移除等变性导致消融实验中最大的性能跳水（平均成功率从52.8%骤降至12.3%）。"
- "在真实世界实验中，EquAct平均成功率达65%，远高于基线3DDA的12.5%。"
- "RLBench 18 tasks (2D/100 demonstrations) 上 avg. success rate (%) = 89.4"
---

# EquAct: An SE(3)-Equivariant Multi-Task Transformer for 3D Robotic Manipulation

> [!tip] 核心洞察
> 结合球面傅里叶特征实现高效、连续的SE(3)等变点云推理，并首次在统一模型中同时实现多任务语言条件化，利用等变场网络一次性评估全SE(3)动作空间，从而实现快速、准确的位姿预测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EquAct：面向3D机器人操作的SE(3)等变多任务Transformer |
| 英文题名 | EquAct: An SE(3)-Equivariant Multi-Task Transformer for 3D Robotic Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=d1wuA8oIH0) · [GitHub](https://github.com/ZXP-S-works/EquAct) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EquAct |
| Dataset | RLBench 18 tasks (2D/100 demonstrations), RLBench 18 tasks (2D/10 demonstrations), RLBench 18 tasks (3D/10 demonstrations), 4 real-world tasks |

> [!tip] 效果简介
> - RLBench 18 tasks (2D/100 demonstrations) 上，avg. success rate (%) 为 89.4，对比 86.8 (SAM2ACT), 81.3 (3DDA)，变化 +2.6%。
> - RLBench 18 tasks (2D/10 demonstrations) 上，avg. success rate (%) 为 60.1，对比 52.2 (SAM2ACT), 50.3 (3DDA)，变化 +7.9% (vs SAM2ACT)。
> - RLBench 18 tasks (3D/10 demonstrations) 上，avg. success rate (%) 为 53.3，对比 37.0 (SAM2ACT), 37.9 (3DDA)，变化 +15.4% (vs 3DDA)。

## 概要

### 问题瓶颈

现有多任务机器人操作策略（如基于多视图ViT的**SAM2ACT**（Fang et al., 2025）或仅平移等变的点云Transformer **3DDA**）在将语言指令、3D观测和动作嵌入共享表示空间时，破坏了底层的3D几何结构。这导致策略在面对新颖的物体位姿时泛化能力严重不足——当观测发生刚体变换（旋转或平移）时，模型无法相应地等变调整动作输出，缺乏连续的SE(3)等变性。

### 核心方法

**EquAct** 是首个在统一模型中同时实现连续SE(3)等变性（覆盖3D旋转和平移）和语言指令SE(3)不变性的多任务操作策略。其核心设计包括三个关键组件：

- **SE(3)等变点云Transformer U-Net（EPTU）**：利用球面傅里叶特征实现高效、连续的SE(3)等变点云编码与解码，通过球面傅里叶最大池化和上采样保持几何一致性。
- **SE(3)不变FiLM层（iFiLM）**：强制语言条件在旋转下保持不变，使语义条件化在几何上不干扰等变推理。
- **等变场网络**：一次性评估连续SE(3)动作空间中的平移和旋转动作值，无需离散化或迭代去噪，实现快速位姿预测。

### 主要结果

| 实验设置 | EquAct | 最强基线 | 提升幅度 |
|---------|--------|---------|---------|
| RLBench 18任务 (SE(2)/100演示) | **89.4%** | 86.8% (SAM2ACT) | +2.6% |
| RLBench 18任务 (SE(2)/10演示) | **60.1%** | 52.2% (SAM2ACT) | +7.9% |
| RLBench 18任务 (SE(3)/10演示) | **53.3%** | 37.9% (3DDA) | +15.4% |
| 4项真实世界任务 | **65.0%** | 12.5% (3DDA) | +52.5% |

消融实验进一步验证了等变性的决定性作用：移除等变性导致平均成功率从52.8%骤降至12.3%（-40.5%），是所有消融项中影响最大的因素。EquAct在推理速度上同样具有优势（0.7s vs 3DDA的3.7s），且训练资源需求与基线相当（单GPU，batch size 2，约21GB显存）。

### 方法定位

在方法谱系上，EquAct属于**等变策略学习**与**多任务语言条件化操作**的交叉点。相较于依赖数据增强的3DDA和基于多视图的SAM2ACT，EquAct通过架构层面的SE(3)等变设计，从根本上保证了策略对观测变换的结构化泛化能力，而非依赖隐式的数据驱动补偿。

### 3D机器人操作中的空间泛化瓶颈

基于关键帧（keyframe）的多任务策略已成为语言条件化机器人操作的主流范式。这类策略接收自然语言指令和3D场景观测（通常是点云），直接预测末端执行器的目标位姿。然而，现有方法在处理新颖物体位姿时暴露出严重的泛化缺陷——当物体在空间中仅发生刚体变换（旋转或平移）时，策略的行为往往不一致，甚至完全失效。

这一问题的根源在于**底层3D几何结构的破坏**。当前最先进的多任务策略，如基于多视图ViT的**SAM2ACT**（Fang et al., 2025）和基于点云Transformer的**3DDA**，将语言、3D观测和动作嵌入到一个共享的表示空间时，并未显式保留3D旋转和平移的几何约束。换句话说，这些模型对输入点云的SE(3)变换不具备理论保证的响应规律：策略的输出不会随观测的刚体变换而等变地变换。

### 等变性的缺失与数据增强的局限

理想情况下，一个具备空间鲁棒性的操作策略应满足如下**等变性**质：

$$\pi(g \cdot o) = g \cdot \pi(o)$$

即当观测 $o$ 经历SE(3)变换 $g$ 时，预测动作应相应地变换 $g \cdot a$。对于多任务语言条件化策略，该性质进一步细化为：策略对观测变换**等变**，同时对语言指令 $n$ 保持**不变**——语义条件不应因场景旋转而改变。

$$\pi(g \cdot o, n) = g \cdot a, \quad g \in \mathrm{SE}(3)$$

现有方法试图通过数据增强来弥补这一结构缺陷——在训练时对点云施加随机旋转和平移，期望模型隐式学习到不变性。但这种方法存在两个根本问题：其一，增强无法提供**连续的**等变保证，模型仅在训练分布附近表现稳定，面对新颖位姿时仍会崩溃；其二，增强策略本身缺乏对语言条件不变性的显式建模，导致语义信号与几何变换耦合，进一步损害泛化能力。

### 从离散化到连续SE(3)空间

另一个制约泛化的因素是动作空间的表示方式。主流方法通常将旋转角度离散化为固定区间，或采用迭代去噪过程（如扩散模型）逐步生成动作。离散化不可避免地引入量化误差，且在高精度任务中面临维度灾难；迭代推理则牺牲了实时性。更重要的是，这些设计在架构层面就与SE(3)等变性不兼容——离散旋转箱或噪声调度无法自然地响应连续的刚体变换。

### 本文动机

上述分析揭示了一个清晰的研究缺口：**如何在多任务语言条件化策略中，以架构原生（architecturally native）的方式嵌入连续的SE(3)等变性，使策略能够根据观测的刚体变换等变地调整动作，同时保持语言条件的不变性？**

EquAct的动机正是填补这一缺口。其核心假设是：若策略网络在结构上保证SE(3)等变性，则无需依赖大规模数据增强即可获得对新颖物体位姿的强泛化能力。为实现这一目标，EquAct需要同时解决三个技术挑战：

1. **高效的点云等变编码**：如何在保持计算效率的前提下，对3D点云进行连续的SE(3)等变特征提取？
2. **几何感知的语言融合**：如何将语言条件注入等变网络，使其在语义上调控策略的同时，不破坏旋转不变性？
3. **全SE(3)动作空间的快速评估**：如何一次性评估连续的平移和旋转动作空间，而非离散化或迭代采样？

这些挑战的解决路径构成了EquAct方法设计的核心线索，将在后续章节中详细展开。

## 核心方法与创新机理

### 瓶颈与设计动机

现有多任务关键帧策略（如SAM2ACT、3DDA）将语言指令、3D观测和动作嵌入共享表示空间时，破坏了底层的3D几何结构。这导致一个根本性缺陷：当场景中的物体发生刚体变换（旋转或平移）时，策略无法等变地调整输出动作，严重限制了在新颖物体位姿下的泛化能力。EquAct的核心假设是：**多任务操作策略应当对观测的SE(3)变换等变，同时对语言指令保持SE(3)不变**，即 $\pi(g \cdot o, n) = g \cdot a$（Equation 2）。

### 三个关键创新点

#### 1. SE(3)等变点云Transformer U-Net（EPTU）

**基线方案**：非等变Transformer（如多视图ViT）或仅支持平移等变的点云Transformer。

**EquAct方案**：EPTU将点云编码为球面傅里叶特征，通过等变Transformer层传播局部与全局信息，实现覆盖3D旋转和平移的连续SE(3)等变性。其下采样和上采样均在球面傅里叶域中完成：

- **球面傅里叶最大池化**：在k近邻内选取范数最大的系数进行下采样，保持等变性：
  $$c_{l,x}' = \mathrm{smaxpool}\{c_{l,p} \mid p \in \mathrm{knn}(x)\} = c_{l,p^*}, \quad p^* = \argmax_{p \in \mathrm{knn}(x)} \|c_{l,p}\|_2^2$$

- **球面傅里叶上采样**：通过对k近邻系数进行距离加权软插值实现上采样：
  $$c_{l,x}' = \mathsf{sup}\{c_{l,p}, x \mid p \in \mathrm{knn}(x)\} = \mathsf{softmax}_{p \in \mathrm{knn}}\left(\frac{1}{\|x-p\|}\right) c_{l,p}$$

**证据强度**：消融实验（Table 3）显示，将EPTU替换为仅平移等变的VN-DGCNN（EPTU → VN）导致平均成功率从52.8%骤降至22.0%（下降30.8%），证明完整的SE(3)等变编码器是关键性能来源。

#### 2. SE(3)不变FiLM层（iFiLM）

**基线方案**：标准FiLM或简单的拼接/注意力机制，无显式几何不变性约束。

**EquAct方案**：iFiLM层利用语言条件 $k$ 通过MLP预测调制系数 $(\alpha_l, \beta, \gamma)$，对不同球面谐波阶数 $l$ 的特征进行区分性调制：

- 对非标量特征（$l > 0$）施加旋转等变缩放：$c_l' = \alpha_l c_l$
- 对标量特征（$l = 0$）施加不变仿射变换：$c_0' = \beta c_0 + \gamma$

这一设计强制语言条件在旋转下保持不变（Proposition 4.4），即 $\mathrm{D}(r) \cdot c' = \mathrm{iFiLM}(\mathrm{D}(r) \cdot c, k)$。

**证据强度**：消融实验（Table 3）中，将iFiLM替换为标准FiLM（iFiLM → FiLM）导致平均成功率下降2.5%。虽然降幅相对较小，但结合EPTU的等变性后，iFiLM确保了语言语义在整个等变推理链中的几何一致性。

#### 3. 等变场网络一次性评估全SE(3)动作空间

**基线方案**：离散化旋转角或迭代去噪（如扩散模型），推理效率低。

**EquAct方案**：在EPTU编码的等变潜在特征 $h$ 基础上，通过两个场网络分别评估平移和旋转动作值：

- **平移场网络**：在全SE(3)平移空间中采样和精化查询动作，输出 $Q_t$，且该值对旋转保持不变（$q_t(a_t, h) = q_t(a_t, g \cdot h)$）。
- **旋转场网络（球面CNN）**：以预测的最优平移位置 $a_t^*$ 为中心聚合球面特征，通过与学习滤波器 $\psi$ 的球面卷积一次性评估旋转动作值 $Q_r$。

这种设计使EquAct能够在0.7秒内完成推理，而基线3DDA需要3.7秒（Table 1）。

### 创新总结

EquAct的三个创新点构成一个完整的SE(3)等变推理链：EPTU将3D观测编码为等变特征，iFiLM以几何不变方式注入语言语义，场网络在等变特征基础上一次性评估全SE(3)动作空间。这一设计使策略能够根据观测的刚体变换等变地调整动作——当物体旋转或平移时，预测的抓取位姿自动跟随变换，无需重新推理或依赖数据增强来弥补几何理解缺失。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_d1wuA8oIH0/figures/001_Figure_1.jpg]]
*Figure 1: Overview of EquAct. EquAct first encodes the observation o = $\{$ s , e $\}$ into latent spherical features h using a SE(3)-equivariant U-Net, e n $c _ { o }$ , while conditioning the natural language instruction n through invariant iFiLM layers. Based on the encoded features h , EquAct then samples and refines translational query actions and gripper open actions using an equivariant field network, resulting in action value functions $Q _ { t }$ and $Q _ { \mathrm { o p e n } }$ . Finally, a rotational field network aggregates spherical features from h centered at the predicted translation $a _ { t } ^ { * }$ to obtain a latent feature $\phi$ , , which is subsequently convolved with a learned filter $\psi$...

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_d1wuA8oIH0/figures/004_Figure_3.jpg]]
*Figure 3: (a) Overview of EPTU. (b) Detailed structure design for each module. Red color indicates the magnitude of the feature. Figure 3: SE(3)-Equivariant Point Transformer U-net (EPTU)*

EquAct 是一个多任务关键帧动作策略，其核心设计目标是在统一的模型中实现连续的 SE(3) 等变性——即策略对观测的刚体变换（3D 旋转与平移）做出等变响应，同时对语言指令保持不变性。整个 pipeline 围绕这一几何先验构建，将观测编码、语言条件融合和动作评估三个环节紧密耦合在一个等变表征空间中。

**输入输出流**：给定观测 $o = \{s, e\}$（点云 $s$ 与末端执行器位姿 $e$）和自然语言指令 $n$，EquAct 首先通过 SE(3) 等变点云 Transformer U-Net（EPTU）将点云编码为球面傅里叶域中的潜在特征 $h$。在此编码过程中，语言指令 $n$ 通过 SE(3) 不变 FiLM 层（iFiLM）注入网络，以语义依赖但几何不变的方式调节特征。随后，基于编码特征 $h$，一个等变场网络在连续的 SE(3) 动作空间 $\mathcal{A}_T$ 中一次性评估所有候选动作的价值——平移场网络输出 $Q_t$，旋转场网络（基于球面 CNN）输出 $Q_r$，同时评估夹爪开合动作 $Q_{\text{open}}$。最终，通过选取价值最大的动作得到预测的关键帧位姿。

**模块关系**：Pipeline 由三个核心模块串联构成，每个模块都严格遵循 SE(3) 等变性约束：

1. **EPTU（观测编码器）**：采用 U-Net 结构，通过球面傅里叶最大池化进行下采样、球面傅里叶上采样进行恢复，在保持 SE(3) 等变性的同时实现多尺度点云特征提取。
2. **iFiLM 层（语言条件融合）**：嵌入在 EPTU 的各层中，利用语言条件 $k$ 预测调制系数，对标量特征（$l=0$）施加不变仿射变换，对高阶球面傅里叶特征（$l>0$）施加旋转等变缩放，从而强制语言条件的 SE(3) 不变性。
3. **等变场网络（动作评估）**：将平移动作价值设计为旋转不变的，旋转动作价值通过球面卷积在 SO(3) 上评估，实现对整个 SE(3) 动作空间的一次性、等变评估。

**训练范式**：策略以模仿学习方式训练，将动作选择视为分类问题。损失函数为平移、旋转和开合三个分量的交叉熵之和，专家动作作为分类标签进行监督。推理时，EquAct 无需迭代去噪或离散化旋转角，单次前向传播即可完成动作预测，推理耗时约 0.7 秒，显著快于基线 3DDA 的 3.7 秒。

> **证据强度说明**：上述框架描述基于论文 Section 4 的完整方法阐述及 Figure 1 的总览图，各模块的设计细节在 Section 4.2–4.4 中有明确的公式和架构说明，证据充分。

### 等变性与不变性假设

EquAct 的核心形式化假设建立在 SE(3) 群作用下的策略行为约束上。给定观测 $o$ 和语言指令 $n$，策略 $\pi$ 预测关键帧动作 $a$。方法要求策略满足以下等变性质：

$$\pi(g \cdot o, n) = g \cdot a, \quad g \in \mathrm{SE}(3)$$

该式表明：当观测经历任意 SE(3) 变换 $g$（包含 3D 旋转和平移）时，预测动作 $a$ 应以相同方式变换为 $g \cdot a$，而语言指令 $n$ 保持不变。这一设计直接回应了核心瓶颈——现有方法在将语言、3D 观测和动作嵌入共享空间时破坏了底层几何结构，导致新颖位姿下泛化能力不足。

---

### SE(3)-等变点云 Transformer U-Net（EPTU）

EPTU 是 EquAct 的观测编码器，负责将点云 $s$ 编码为等变潜在球面傅里叶特征。其架构采用 U-Net 设计，通过下采样和上采样在球面傅里叶域中传播局部与全局信息。

**球面傅里叶最大池化**用于下采样。对于查询点 $x$，在其 $k$ 近邻内选取球面傅里叶系数范数最大的点作为代表：

$$c_{l,x}' = \mathrm{smaxpool}\{c_{l,p} \mid p \in \mathrm{knn}(x)\} = c_{l,p^*}, \quad p^* = \argmax_{p \in \mathrm{knn}(x)} \|c_{l,p}\|_2^2$$

其中 $c_{l,p}$ 是点 $p$ 处第 $l$ 阶球面傅里叶系数，$\|\cdot\|_2^2$ 衡量该系数的能量。这种池化方式保持了 SE(3) 等变性，因为范数在旋转下不变。

**球面傅里叶上采样**通过距离加权软插值恢复特征图分辨率：

$$c_{l,x}' = \mathsf{sup}\{c_{l,p}, x \mid p \in \mathrm{knn}(x)\} = \mathsf{softmax}_{p \in \mathrm{knn}}\left(\frac{1}{\|x-p\|}\right) c_{l,p}$$

该操作对 $k$ 近邻的系数进行距离倒数加权的 softmax 插值，在保持等变性的同时实现平滑上采样。

---

### SE(3)-不变 FiLM 层（iFiLM）

语言条件化模块需要满足 SE(3) 不变性——语言指令的语义不应随观测的刚体变换而改变。iFiLM 层通过以下机制实现这一约束。

给定球面傅里叶特征 $c$ 和语言条件 $k$，iFiLM 首先通过 MLP 预测调制参数：

$$c' = \mathrm{iFiLM}(c, k), \quad \alpha_l, \beta, \gamma = \mathrm{MLP}(k)$$

其中 $\alpha_l$ 是第 $l$ 阶的缩放系数，$\beta$ 和 $\gamma$ 是标量仿射参数。调制分两路进行：

- 对高阶特征（$l > 0$）施加旋转等变缩放：

$$c_l' = \alpha_l c_l, \quad l > 0$$

- 对标量特征（$l = 0$）施加不变仿射变换：

$$c_0' = \beta c_0 + \gamma, \quad l = 0$$

由于 $\alpha_l$、$\beta$、$\gamma$ 均从语言条件 $k$ 预测且 $k$ 本身是 SE(3) 不变的（语言嵌入不含位姿信息），整个 iFiLM 层对输入特征 $c$ 保持 SE(3) 等变性，对条件 $k$ 保持 SE(3) 不变性。消融实验表明，将 iFiLM 替换为标准 FiLM 导致平均成功率下降 2.5%。

---

### 等变场网络与动作评估

EquAct 通过两个并行的场网络一次性评估连续 SE(3) 动作空间中的动作值，避免了离散化或迭代去噪。

**平移场网络**在 EPTU 编码的潜在特征 $h$ 上评估平移动作值 $Q_t$。该网络对旋转保持不变：

$$q_t(a_t, h) = q_t(a_t, g \cdot h), \quad g \in \mathrm{SO}(3)$$

**旋转场网络**（基于球面 CNN）以预测的平移位置 $a_t^*$ 为中心聚合球面特征，得到潜在特征 $\varphi$，随后与学习滤波器 $\psi$ 进行球面卷积以获得旋转动作值 $Q_r$。

---

### 训练损失

EquAct 通过模仿学习训练，将动作选择视为分类问题，使用交叉熵损失：

$$\mathcal{L} = \mathbb{E}_{D,A}[\mathcal{H}(Q_t,\bar{a}_t) + \mathcal{H}(Q_r,\bar{a}_r) + \mathcal{H}(Q_{\mathrm{open}},\bar{a}_{\mathrm{open}})]$$

其中 $\mathcal{H}$ 为交叉熵，$\bar{a}_t$、$\bar{a}_r$、$\bar{a}_{\mathrm{open}}$ 分别为平移、旋转和夹爪开合的专家动作标签。三项损失分别监督三个动作分量，共同优化策略网络。

## 实验与关键发现

### 核心实验设置

EquAct在**18个RLBench语言条件任务**（共249条指令）上进行评估，覆盖三种难度递增的设置：
- **2D/100**：每任务100条演示，物体位姿在SE(2)内随机初始化
- **2D/10**：每任务10条演示，物体位姿在SE(2)内初始化
- **3D/10**：每任务10条演示，物体位姿在SE(3)内随机初始化（含任意3D旋转）

基线方法包括**SAM2ACT**（Fang et al., 2025，多视图Transformer SOTA）和**3DDA**（点云Transformer配合3D数据增强）。评估指标为任务成功率（0%失败，100%成功），每任务运行25个评估回合。

### 主要仿真结果（Table 1）

EquAct在所有三种设置下均取得最高平均成功率：

| 设置 | EquAct | SAM2ACT | 3DDA | 相对最佳基线提升 |
|------|--------|---------|------|:---:|
| 2D/100 | **89.4** | 86.8 | 81.3 | +2.6% |
| 2D/10  | **60.1** | 52.2 | 50.3 | +7.9% |
| 3D/10  | **53.3** | 37.0 | 37.9 | +15.4% |

**关键趋势**：任务空间扰动越强（从SE(2)到SE(3)，从100到10条演示），EquAct相对基线的优势越大。在3D/10设置下，EquAct领先3DDA达15.4个百分点，说明SE(3)等变架构对数据效率和空间泛化的双重增益。在需要高精度的任务上（如place_cups，3D/10下EquAct得21分，两基线均为0分；sort_shape得36分 vs 24/14分），等变性的作用尤为突出。

**计算效率**：EquAct在单GPU上以batch size 2训练，总迭代8e5步；SAM2ACT使用32 GPUs（batch size 256，5e4步）。推理耗时方面，EquAct仅需0.7秒，而3DDA需3.7秒。GPU显存使用量相当（约21GB），保证了资源公平性。

### 真实世界实验（Table 2）

在4个物理任务（拆卸管道、摘花、摘水果、安装卷纸）上，EquAct平均成功率达**65.0%**，而3DDA仅**12.5%**（+52.5个百分点）。真实环境包含SE(3)和SE(2)位姿扰动及鲁棒性测试，EquAct在所有任务上均显著优于基线，验证了仿真中观察到的泛化优势可迁移至真实场景。

### 消融实验（Table 3）

在4个RLBench任务的3D/10设置下进行消融，完整模型平均成功率为52.8%：

| 消融操作 | 平均SR | 下降幅度 | 因果解读 |
|----------|:------:|:--------:|----------|
| 完整模型 | 52.8 | — | — |
| 移除等变性 (equ. → no equ.) | 12.3 | **-40.5** | **最大跳水**：等变性是性能的核心支柱 |
| EPTU → VN-DGCNN | 22.0 | -30.8 | 等变Transformer U-Net远优于简单等变backbone |
| 球谐度数 l=3 → l=2 | 45.5 | -7.3 | 更高阶球面特征对精确旋转推理有实质贡献 |
| iFiLM → 标准FiLM | 50.3 | -2.5 | 语言不变性调制带来小幅但一致的增益 |
| 移除数据增强 | 50.5 | -2.3 | 数据增强贡献有限，等变架构已提供强归纳偏置 |

**核心因果链**：等变性是性能的第一性因素（移除后性能崩溃），EPTU架构是第二支柱（替换后损失过半），球面特征分辨率和语言不变性调制是精细化增益来源。数据增强的边际贡献进一步证明，架构层面的几何归纳偏置比数据层面的扰动更有效。

### 鲁棒性分析

**点云遮挡（Table 4）**：在严重遮挡下，EquAct平均成功率从52.8%降至47.0%（仅下降5.8%），而3DDA从37.9%骤降至15.8%。EquAct对不完整观测的鲁棒性源于等变架构对局部几何结构的稳定编码。但需注意，在insert peg等精细任务上，遮挡仍导致明显退化（EquAct从44%降至28%），说明对完整点云仍存在依赖。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_d1wuA8oIH0/figures/009_Table_4.jpg]]
*Table 4: Robustness to occluded point cloud*

**干扰物体（Table 5）**：引入10个干扰物体后，EquAct在拆卸任务上的平均成功率从90%降至70%。最复杂的“全部链环拆卸”子任务从100%降至50%，表明复杂场景中干扰增多时鲁棒性会显著下降。

### 等变误差实证（Table 7）

通过测地距离度量模型的实际等变程度：在恒等变换下，EquAct的旋转误差仅0.005 rad、平移误差0.000 m；在SE(3)扰动下，旋转误差0.012 rad、平移误差0.001 m。3DDA在SE(3)扰动下的旋转误差高达0.524 rad，平移误差0.015 m，实证了非等变模型在几何一致性上的根本缺陷。

### 失败模式与局限

1. **严重遮挡**：虽然EquAct相对鲁棒，但在高精度插入任务中，遮挡仍使成功率从44%降至28%。
2. **多干扰物**：干扰物体增多时，复杂长序列任务（如全部拆卸）成功率减半。
3. **关键帧假设**：当前方法基于关键帧动作预测，对需要连续轨迹的精细操作（如高精度路径跟踪）适用性受限。如何将等变策略扩展到连续轨迹预测，是明确的开放问题。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_d1wuA8oIH0/figures/006_Table_1.jpg]]
*Table 1: Multi-task success rate (%) on 18 RLBench tasks with 249 instructions. On average, EquAct outperforms all the baselines on all 3 settings. Furthermore, the second column shows that EquAct’s training and inference time, GPU memory matches baselines. 2D/100 and 2D/10 denote 100 and 10 training demonstrations per task with object poses randomly initialized in SE(2). 3D/10 denotes task with object poses randomly initialized in SE(3) and 10 demonstrations per task*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_d1wuA8oIH0/figures/008_Table_3.jpg]]
*Table 3: Ablation study*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_d1wuA8oIH0/figures/007_Table_2.jpg]]
*Table 2: Real-world experiments*

## 定位与知识库关联

### 核心瓶颈与设计动机

现有多任务关键帧策略（如 **SAM2ACT**（Fang et al., 2025）、**3DDA**）的核心瓶颈在于：它们将语言指令、3D观测和动作嵌入到共享嵌入空间时，破坏了底层3D几何结构。具体而言，这些方法缺乏连续的SE(3)等变性——当场景中的物体发生刚体变换（旋转和平移）时，策略无法保证预测的动作随之等变地调整。这导致策略在新颖的3D物体位姿下泛化能力严重不足，尤其在小样本（每任务仅10个示教）和SE(3)随机初始化场景中表现急剧退化。

EquAct的因果调控旋钮是：通过引入**连续的SE(3)等变性**（覆盖3D旋转和平移）以及**语言指令的SE(3)不变性**，使策略可以根据观测的刚体变换等变地调整动作，同时保持语义条件的不变性。其核心洞察在于结合球面傅里叶特征实现高效、连续的SE(3)等变点云推理，并首次在统一模型中同时实现多任务语言条件化，利用等变场网络一次性评估全SE(3)动作空间，从而实现快速、准确的位姿预测。

### 关键方法变革

EquAct相对于现有基线进行了三个关键模块的替换：

| 方法槽位 | 基线方案 | EquAct方案 | 证据锚点 |
|---------|---------|-----------|---------|
| 网络架构 | 非等变Transformer（如多视图ViT）或仅平移等变的点云Transformer | SE(3)等变点云Transformer U-Net（EPTU） | Section 4.2, Figure 3 |
| 语言条件化方式 | 标准FiLM或简单的拼接/注意力机制，无显式几何不变性约束 | SE(3)不变FiLM层（iFiLM），强制语言条件在旋转下保持不变 | Section 4.3, Equations 7-9 |
| 动作评估机制 | 离散化旋转角或迭代去噪（如扩散模型） | 等变场网络一次性评估连续SE(3)空间中的动作值 | Section 4.4 |

**EPTU**作为观测编码器，通过球面傅里叶最大池化（Equation 3）和球面傅里叶上采样（Equation 5）实现高效的下采样和上采样，在保持SE(3)等变性的同时传播局部和全局信息。**iFiLM层**利用语言条件预测调制系数，对标量特征（$l=0$）施加不变仿射变换（$c_0' = \beta c_0 + \gamma$），对高阶特征（$l>0$）施加旋转等变缩放（$c_l' = \alpha_l c_l$），从而在几何等变性和语义不变性之间建立桥梁。

### 证据强度与决定性实验

EquAct的证据链具有高置信度，核心支撑来自三个层面的实验：

1. **仿真基准的全面领先**：在18个RLBench任务上，EquAct在三种设置下（SE(2)/100示教、SE(2)/10示教、SE(3)/10示教）平均成功率均显著超过所有基线。尤其在最具挑战性的SE(3)/10设置下，EquAct达到53.3%，远超3DDA的37.9%和SAM2ACT的37.0%（Table 1）。

2. **消融实验的因果验证**：移除等变性（equ. → no equ.）导致平均成功率从52.8%骤降至12.3%，这是消融实验中最大的性能跳水（Table 3）。此外，用VN-DGCNN替换EPTU（EPTU → VN）使成功率下降30.8%，将球面谐波度数从$l=3$降至$l=2$导致下降7.3%，验证了架构设计和特征分辨率的必要性。

3. **真实世界迁移能力**：在4个真实世界任务上，EquAct平均成功率达65%，远高于基线3DDA的12.5%（Table 2），证明了等变策略在物理环境中的鲁棒性。

### 适用边界与局限性

尽管EquAct在空间泛化方面表现突出，其适用边界存在以下限制：

- **严重遮挡下的性能退化**：当点云存在严重遮挡时，EquAct成功率从52.8%降至47.0%（Table 4），虽然降幅（5.8%）远小于3DDA（从15.8%到更低），但仍表明方法对完整点云有一定依赖。
- **干扰物体的鲁棒性下降**：当场景中存在大量干扰物体时，最复杂任务（如全部拆解）的成功率从100%降至50%（Table 5），说明密集杂乱场景仍是挑战。
- **关键帧假设的固有限制**：当前方法基于关键帧动作假设，对于需要连续运动策略的细粒度任务（如高精度连续路径跟踪）适用性可能受限。如何将等变策略扩展到连续轨迹预测是一个开放问题。

### 开放问题与未来方向

1. **从关键帧到连续轨迹**：能否将SE(3)等变策略从单步关键帧动作扩展到完整的连续轨迹预测，以处理需要精细力控或路径跟踪的任务？

2. **预训练模型的语义增强**：能否利用预训练的2D/3D视觉模型（如CLIP、DINOv2）进一步提升数据效率和语义泛化能力，特别是在语言指令多样化的场景中？

3. **更高效的等变Backbone**：当前EPTU的计算开销虽与非等变基线相当（推理耗时0.7s vs 3DDA的3.7s），但更高效的球面卷积或稀疏化策略是否能进一步降低训练成本，使模型可扩展至更高分辨率点云？

4. **动态环境中的等变规划**：在存在移动障碍物或动态场景变化的情况下，如何保持SE(3)等变性并实现实时规划，是向非结构化真实环境部署的关键一步。

## 原文 PDF

![[paperPDFs/ICLR_2026/EquAct_An_SE3_Equivariant_Multi_Task_Transformer_for_3D_Robotic_Manipulation.pdf]]

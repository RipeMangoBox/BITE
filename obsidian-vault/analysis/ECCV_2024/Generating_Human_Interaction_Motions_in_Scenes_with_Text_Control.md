---
title: "Generating Human Interaction Motions in Scenes with Text Control"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Generating_Human_Interaction_Motions_in_Scenes_with_Text_Control.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/tesmo/
aliases:
- GHIMSTC
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "向预训练的文本到动作扩散模型中引入场景感知控制分支（如2D地板图或3D物体几何）并进行微调，使模型能够在保持生成质量和文本可控性的前提下适应场景约束。"
primary_logic: "将场景感知动作生成分解为导航和交互两个阶段，分别利用预训练的文本-动作扩散模型并附加场景感知分支，通过为每个阶段设计合适的场景表征（2D地板图用于导航，3D物体几何用于交互）和训练数据增强，在不牺牲文本控制多样性的同时生成高质量的场景兼容动作。"
claims:
- "在用户感知研究中，TeSMo的交互动作被71.9%的参与者认为优于DIMOS。"
- "在SAMP坐姿测试集上，TeSMo的目标位置误差（0.1445）显著低于DIMOS（0.2020），物体穿透率（0.0611）低于DIMOS（0.1076）。"
- "在Loco-3D-FRONT测试集上，TeSMo的导航根轨迹在目标到达精度和碰撞率方面达到最佳。"
- "消融实验表明，同时使用目标到达引导和碰撞引导可显著提升导航和交互性能。"
---

# Generating Human Interaction Motions in Scenes with Text Control

> [!tip] 核心洞察
> 将场景感知动作生成分解为导航和交互两个阶段，分别利用预训练的文本-动作扩散模型并附加场景感知分支，通过为每个阶段设计合适的场景表征（2D地板图用于导航，3D物体几何用于交互）和训练数据增强，在不牺牲文本控制多样性的同时生成高质量的场景兼容动作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于文本控制的场景内人物交互动作生成 |
| 英文题名 | Generating Human Interaction Motions in Scenes with Text Control |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2404.10685) · [Project](https://research.nvidia.com/labs/toronto-ai/tesmo/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TeSMo |
| Dataset | SAMP sitting test set, User study (preference), Loco-3D-FRONT test set (navigation) |

> [!tip] 效果简介
> - SAMP sitting test set 上，Goal Pos. Error 为 0.1445，对比 0.2020 (DIMOS)，变化 -0.0575。
> - SAMP sitting test set 上，Object Penetration Ratio 为 0.0611，对比 0.1076 (DIMOS)，变化 -0.0465。
> - User study (preference) 上，Preference rate 为 71.9%，对比 29.1% (DIMOS)，变化 +42.8%。

## 概要

场景感知的人类动作生成面临一个核心瓶颈：现有的大规模动作捕捉数据集（如HumanML3D）虽然提供了丰富的文本-动作对，但缺少场景信息，而带场景标注的人-物交互数据又极为稀缺，这使得模型难以在保持文本可控性的同时生成多样化且符合物理约束的场景兼容动作。

针对这一挑战，本文提出 **TeSMo**，一种基于文本控制的场景内人物交互动作生成方法。其核心思路是将场景感知动作生成**分解为导航（navigation）和交互（interaction）两个阶段**，并利用**预训练的文本到动作扩散模型**作为基础生成器，通过附加**场景感知控制分支**进行微调，从而在不牺牲文本控制多样性的前提下，使生成的动作适应场景约束。

具体而言，TeSMo 首先在场景无关的大规模动捕数据上预训练一个强调目标到达约束的文本到动作扩散模型，随后引入场景感知组件——导航阶段使用2D地板图编码场景布局，交互阶段使用3D物体几何特征（BPS）——在增强后的场景数据上进行微调。测试时，通过**目标到达引导**和**碰撞避免引导**进一步优化生成质量。

实验结果表明，TeSMo 在导航和交互两个任务上均取得了显著提升：
- 在 Loco-3D-FRONT 导航测试集上，TeSMo 的骨盆轨迹在**目标到达精度**和**碰撞率**方面达到最佳（Table 1）。
- 在 SAMP 坐姿交互测试集上，TeSMo 的目标位置误差（0.1445）显著低于强化学习方法 **DIMOS**（Zhao et al., ICCV 2023）的 0.2020，物体穿透率（0.0611）也低于 DIMOS 的 0.1076（Table 2）。
- 用户感知研究中，71.9% 的参与者认为 TeSMo 生成的交互动作优于 DIMOS（Table 2）。

消融实验进一步验证了测试时引导的有效性：同时使用目标到达引导和碰撞引导可将导航目标位置误差从 0.1568 降至 0.1241（Table 3），且两阶段生成策略（先骨盆轨迹后全身填充）在目标到达精度和碰撞率上均优于直接生成全身运动的方案（Table 4）。

在方法谱系上，TeSMo 处于**文本到动作扩散模型**与**场景感知运动生成**的交叉点。其基础模型继承自 **GMD**（Karunratanakul et al., ICCV 2023）的扩散框架，场景感知分支的设计借鉴了 **OmniControl**（Xie et al., arXiv 2023）的空间控制思想，但在训练策略（预训练+冻结基础模型+微调场景分支）和场景表征（2D地图与3D物体几何的分阶段使用）上做出了关键改进。

本文的主要局限在于：两阶段生成可能导致骨盆轨迹与全身姿态之间的不协调；交互类型目前仅限于坐椅子等简单动作，难以处理躺下、触摸或动态物体交互；对非平面表面（如台阶、斜坡）上的交互缺乏支持。这些也为未来的一阶段统一模型和更广泛交互谱系的扩展留下了开放问题。



### 问题背景

生成逼真且可控的三维人体动作是计算机视觉与图形学中的核心挑战，在动画制作、虚拟现实、具身智能等领域具有广泛的应用前景。近年来，文本到动作的扩散模型取得了显著进展，能够从自然语言描述中生成多样且高质量的人体运动序列。然而，这些方法大多在“空白空间”中操作，完全忽略了人物所处的三维场景环境，导致生成的行走、坐下等动作无法适配具体的房间布局、障碍物和家具几何。

将场景信息纳入动作生成面临一个根本性瓶颈：**缺少大规模、带文本标注的人-场景交互数据集**。现有的运动捕捉数据集（如HumanML3D、SAMP）虽然包含丰富的文本描述，但缺乏对应的场景几何信息；而场景感知的动作数据集规模有限，难以支撑扩散模型从零开始训练。

### 现有方法缺口

已有的场景感知动作生成方法主要分为两类，各自存在明显局限：

- **基于强化学习的方法**（如**DIMOS**，Zhao et al., ICCV 2023）：通过物理仿真和奖励函数生成场景兼容的动作，能够较好地处理物理约束和碰撞避免。但其生成的动作多样性有限，且难以通过文本进行风格控制——用户无法指定“疲惫地坐下”或“优雅地走近椅子”等语义属性。

- **场景无关的扩散模型**（如**GMD**，Karunratanakul et al., ICCV 2023；**OmniControl**，Xie et al., arXiv 2023）：虽然具备强大的文本可控性和动作质量，但完全忽略场景信息，生成的骨盆轨迹会穿透墙壁或家具，无法直接用于场景内的导航与交互任务。

这一缺口的核心在于：**如何在保持文本可控性和动作多样性的同时，使生成的动作满足场景的物理约束**。

### 本文动机

针对上述挑战，TeSMo提出了一种新的解决思路：将场景感知动作生成**分解为导航（Navigation）与交互（Interaction）两个阶段**，并在每个阶段中向预训练的文本到动作扩散模型引入场景感知控制分支进行微调。这一设计基于以下关键洞察：

- **两阶段分解**使模型能够为不同任务设计合适的场景表征——导航阶段使用2D地板图编码可行走区域，交互阶段使用3D物体几何（BPS特征）捕捉椅子等物体的精确形状。
- **预训练+微调策略**规避了场景数据稀缺的问题：先在HumanML3D、SAMP等大规模运动数据集上训练场景无关的基础模型，再冻结其参数，仅微调一个附加的场景感知分支，从而在保留文本控制多样性的前提下适配场景约束。
- **测试时引导**通过目标到达和碰撞避免的解析目标函数梯度，进一步优化生成质量，使骨盆轨迹准确到达目标位姿并避开障碍物。

这一方法论的直接效果是：在SAMP坐姿测试集上，TeSMo的交互动作被**71.9%**的参与者认为优于DIMOS（Table 2），目标位置误差从0.2020降至**0.1445**，物体穿透率从0.1076降至**0.0611**；在Loco-3D-FRONT导航测试集上，根轨迹的目标到达精度和碰撞率均达到最优（Table 1）。



## 核心方法与创新机理

TeSMo 的核心创新在于**将场景感知注入预训练的文本-动作扩散模型**，而非从头训练一个场景条件模型。这一策略解决了该领域的根本瓶颈：大规模、带文本标注的人-场景交互数据集极度稀缺。通过冻结预训练基座并附加轻量级的场景感知控制分支进行微调，TeSMo 在保持文本可控性与运动质量的同时，实现了对场景约束的适应。

具体而言，TeSMo 引入了三个关键的 **changed slots**：

1. **场景表征的条件注入**：导航阶段使用 ResNet-18 编码的 2D 地板图，交互阶段使用 BPS（Basis Point Set）特征编码的 3D 物体几何。这与场景无关的基线方法（如 **GMD**、**OmniControl**）形成鲜明对比——后者完全不使用任何场景信息。

2. **预训练-微调策略**：首先在场景无关的大规模动捕数据（HumanML3D、SAMP）上训练基础 MDM 模型，然后冻结基座权重，仅微调新增的场景感知分支。这避免了在小规模场景数据上从头训练扩散模型导致的质量退化。在导航任务中，场景无关分支在 Loco-3D-FRONT 上训练 420k 步，场景感知分支仅需微调 20k 步；交互任务类似（400k 步 + 20k 步）。

3. **绝对骨盆位姿表示**：将 HumanML3D 风格的相对骨盆速度和旋转替换为第一帧坐标系下的绝对位置与朝向 ${\bf x}^n = [x, y, z, \cos\theta, \sin\theta]_n$。这一表示使得模型能够直接感知和优化目标到达精度，是后续目标引导和碰撞引导能够有效工作的前提。

上述创新共同构成了一个因果链条：**预训练基座保证运动质量和文本可控性 → 场景感知分支注入空间约束 → 绝对位姿表示使物理约束可微分 → 测试时引导进一步优化目标到达与碰撞避免**。消融实验（Table 3）证实了这一链条的有效性：同时使用目标到达引导和碰撞引导，导航目标位置误差从 0.1568 降至 0.1241。



![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_10685/figures/001_Figure_1.jpg]]
*Figure 1: We present TeSMo, a method for generating diverse and plausible human-scene interactions from text input. Given a 3D scene, TeSMo generates scene-aware motions, such as walking in free space and sitting on a chair. Our model can be easily controlled using textual descriptions, start positions, and goal positions*

TeSMo 将“文本控制的场景内人物交互动作生成”分解为两个阶段：**导航（Navigation）** 与 **交互（Interaction）**，如图 Figure 2 所示。给定起始位姿（绿色箭头）、目标位姿（红色箭头）、3D 场景以及文本描述，系统首先生成一条从起点到目标点的无碰撞骨盆根轨迹，随后通过内部填充（in-painting）将该轨迹提升为完整的全身导航动作；接着，以导航结束姿态为起点，在目标物体几何的约束下一次性生成全身交互动作。

### 核心设计动机

这一分解策略源自一个关键观察：场景感知的人类动作生成受限于缺少大规模、带文本标注的人-场景交互数据集，直接训练一个统一的场景感知模型极易丧失文本可控性和动作多样性。因此，TeSMo 采用**预训练-微调**范式，先在场景无关的大规模动捕数据上训练一个强文本-动作扩散模型，再通过附加的场景感知控制分支进行微调，从而在不牺牲生成质量和文本可控性的前提下引入场景约束。

### 模块关系与数据流

1. **场景无关的文本-动作扩散模型（预训练 MDM）**：作为基础运动生成器，提供逼真的运动和文本相关性。该模块在 HumanML3D 和 SAMP 等大规模数据集上预训练，微调时参数冻结。
2. **场景感知控制分支**：一个附加的 Transformer 编码器，以场景表征（导航阶段为 2D 地板图，交互阶段为 3D 物体几何）为条件输入，适配基础模型以生成场景兼容的运动。
3. **导航根轨迹模型**：根据文本描述、起始/目标位姿和 2D 地板图，生成绝对骨盆位置与朝向序列 $\mathbf{x}^n = [x, y, z, \cos\theta, \sin\theta]_n$，并通过测试时引导（目标到达引导 $\mathcal{I}_g$ 和碰撞引导 $\mathcal{T}_c$）确保轨迹准确到达目标且不碰撞障碍物。
4. **全身填充模块（PriorMDM）**：将生成的骨盆轨迹作为条件，通过 in-painting 方式补全全身关节姿态，同时保持文本指定的运动风格。
5. **交互运动模型**：以导航结束姿态为起点，直接生成从起始姿态到目标骨盆位姿的全身交互运动，以 3D 物体几何（通过 BPS 特征编码）为条件。该模型使用扩展的全身姿态表示 $\mathbf{x}^n \in \mathbb{R}^{268}$，包含根动态、关节位置/速度/旋转和足部接触标签。

### 场景表征的选择

两个阶段采用了不同的场景表征以适应各自的任务特性：导航阶段使用 **2D 地板图**（由 ResNet-18 编码），因为导航主要关注在可行走区域内规划无碰撞路径；交互阶段使用 **3D 物体几何**（通过 BPS 特征编码），因为坐椅子等交互需要精确的物体表面信息来避免穿透和漂浮。这种差异化设计使得每个阶段能够以最低的计算开销获得最有效的场景信息。

### 与基线方法的框架级差异

相比于 DIMOS（Zhao et al., ICCV 2023）等基于强化学习的方法，TeSMo 的扩散模型框架天然支持文本控制，且无需为每个新场景重新训练策略。相比于 GMD（Karunratanakul et al., ICCV 2023）和 OmniControl（Xie et al., arXiv 2023）等场景无关的扩散模型，TeSMo 通过场景感知分支引入了显式的场景约束，同时通过冻结基础模型保留了文本控制的多样性。



TeSMo 将场景感知的人类动作生成分解为**导航**与**交互**两个阶段，每个阶段均基于预训练的文本-动作扩散模型，并通过附加的场景感知控制分支进行微调，从而在保持文本可控性的前提下适应场景约束。以下逐一剖析各核心模块及其关键公式。

### 3.2 场景感知扩散模型基础

TeSMo 的基础生成器是一个场景无关的文本到动作扩散模型。其反向去噪过程建模为：

$$p_{\phi}(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{c}) = \mathcal{N}(\mathbf{x}_{t-1}; \pmb{\mu}_{\phi}(\mathbf{x}_t, \mathbf{c}, t), \beta_t \mathbf{I})$$

其中 $\mathbf{x}_t$ 为第 $t$ 步的加噪运动序列，$\mathbf{c}$ 为条件信息（文本嵌入），$\pmb{\mu}_{\phi}$ 为可学习的均值函数，$\beta_t$ 为噪声调度参数。

**场景感知微调策略**：首先在 HumanML3D 和 SAMP 等大规模动捕数据集上预训练场景无关的基础模型，然后冻结基础模型权重，附加一个场景感知的 Transformer 编码器分支，在场景增强数据上进行微调。这一策略的核心优势在于：避免因场景数据稀缺导致的生成质量退化，同时将场景信息（2D 地板图或 3D 物体几何）注入生成过程。

**测试时引导**：在推理阶段，每个去噪步骤对预测的干净运动 $\hat{\mathbf{x}}_0$ 施加解析目标函数的梯度扰动：

$$\tilde{\mathbf{x}}_0 = \hat{\mathbf{x}}_0 - \alpha \nabla_{\mathbf{x}_t} \mathcal{I}(\hat{\mathbf{x}}_0)$$

其中 $\mathcal{I}$ 为目标引导函数（如目标到达误差或碰撞惩罚），$\alpha$ 为引导强度权重。这一机制使模型在采样过程中显式满足物理约束。

### 3.3 导航根轨迹模型

导航阶段负责生成从起始位姿到目标位姿的无碰撞骨盆轨迹，随后通过全身填充模块（PriorMDM）补全为完整运动。

**姿态表示**：根轨迹模型采用绝对骨盆位置与朝向作为表示，第 $n$ 帧的根位姿为：

$${\bf x}^n = [x, y, z, \cos\theta, \sin\theta]_n$$

相较于 HumanML3D 风格的相对速度表示，绝对表示更有利于精确的目标到达约束。

**场景条件注入**：2D 地板图通过 ResNet-18 编码后，作为场景感知分支的输入，与文本嵌入和起始/目标位姿拼接后送入 Transformer 编码器。

**训练时的掩码覆写**：为保证模型在推理时能够精确到达指定目标位姿，训练时对输入序列的起点和终点帧用真实值覆写：

$$\tilde{\mathbf{x}}_t = \mathbf{m} * \mathbf{x}_0 + (\mathbf{1} - \mathbf{m}) * \mathbf{x}_t$$

其中 $\mathbf{m}$ 为二值掩码，标记起始帧和结束帧的位置。

**目标到达引导**：引导函数 $\mathcal{I}_g$ 定义为预测结束位姿与目标位姿的平方误差：

$$\mathcal{I}_g = (\hat{\mathbf{x}}_0^N - \mathbf{g})^2$$

**碰撞引导**：针对导航场景，碰撞目标函数 $\mathcal{T}_c$ 定义为骨盆位置在可行走区域外的平均正 2D 距离：

$$\mathcal{T}_c = \mathrm{SDF}(\hat{\mathbf{x}}_0, \mathcal{M})$$

其中 $\mathcal{M}$ 为 2D 地板图的可行走区域掩码。

**轨迹混合**：为支持用户指定的路径约束（如 A* 路径），在去噪过程中将预测的 2D 轨迹分量与输入轨迹进行混合：

$$\tilde{\mathbf{p}}_0 = s * \hat{\mathbf{p}}_0 + (1 - s) * \mathbf{p}$$

其中 $s$ 为混合比例，控制对输入路径的跟随程度。

### 3.4 交互运动模型

与导航阶段的两步生成不同，交互模型采用**单阶段扩散模型**直接从起始姿态、目标骨盆位姿和 3D 物体几何生成全身交互运动。

**全身姿态表示**：交互模型的姿态向量扩展了 HumanML3D 表示，增加了绝对骨盆位置和朝向，第 $n$ 帧的表示维度为 268：

$$\mathbf{x}^n = \left[ x, y, z, \sin\theta, \cos\theta, \dot{r}^a, \dot{r}^x, \dot{r}^z, r^y, \mathbf{j}^p, \mathbf{j}^v, \mathbf{j}^r, \mathbf{c}^f \right]_n \in \mathbb{R}^{268}$$

其中 $(x, y, z, \sin\theta, \cos\theta)$ 为绝对骨盆位姿，$\dot{r}^a, \dot{r}^x, \dot{r}^z, r^y$ 为根关节动态量，$\mathbf{j}^p, \mathbf{j}^v, \mathbf{j}^r$ 分别为各关节的位置、速度和旋转，$\mathbf{c}^f$ 为足部接触标签。

**3D 物体几何编码**：物体几何通过 Basis Point Set（BPS）特征进行编码，作为场景感知分支的条件输入。

**碰撞损失**：交互阶段的碰撞引导使用身体顶点在物体内部的平均正符号距离：

$$\mathcal{T}_c = \mathrm{SDF}(\hat{\mathbf{x}}_0, S_{\mathcal{O}})$$

其中 $S_{\mathcal{O}}$ 为目标物体的 3D 几何表示。这一显式碰撞惩罚是 TeSMo 在物体穿透率指标上显著优于 DIMOS（0.0611 vs 0.1076）的关键机制。



## 实验与关键发现

### 核心定量结果

**导航运动生成（Loco-3D-FRONT 测试集）**

TeSMo 在导航任务上实现了最优的目标到达精度与最低碰撞率。如 Table 1 所示，骨盆轨迹的目标位置误差仅为 0.169 m，方向误差 0.119，高度误差 0.008，碰撞率 0.031。相比之下，场景无关的基线方法 **GMD** (Karunratanakul et al., ICCV 2023) 和 **OmniControl** (Xie et al., arXiv 2023) 无法利用场景信息，在碰撞率等指标上处于劣势——这一点需注意公平性：该比较旨在展示场景感知的优势，而非在同等信息条件下对决。在骨盆轨迹生成后，TeSMo 通过 PriorMDM 进行全身填充（in-painting），最终全身运动的 FID 为 20.465、R-precision 为 0.376、Diversity 为 6.415、Foot Skating 为 0.056，与 GMD 和 OmniControl 等扩散模型保持竞争力，说明引入场景感知并未牺牲运动质量和文本对齐能力。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_10685/figures/005_Table_1.jpg]]
*Table 1: Evaluation of navigation motion generation on the Loco-3D-FRONT test set. (Left) For generated pelvis trajectories, our approach achieves the best goal-reaching accuracy with low collision rate. (Right) After in-painting the full-body motion, our method maintains diverse and realistic motion that aligns with the given text prompt, competitive with diffusion-based scene-agnostic GMD and OmniControl*

**人-物交互生成（SAMP 坐姿测试集）**

Table 2 给出了与强化学习方法 **DIMOS** (Zhao et al., ICCV 2023) 的直接对比。TeSMo 的目标位置误差为 0.1445，显著低于 DIMOS 的 0.2020（Δ = -0.0575）；物体穿透率从 DIMOS 的 0.1076 降至 0.0611（Δ = -0.0465）。在用户感知研究中，71.9% 的参与者偏好 TeSMo 生成的交互动作，而 DIMOS 仅获 28.1% 的偏好。Figure 6 的定性对比进一步显示，TeSMo 减少了漂浮和穿透现象，生成的人-物交互更加逼真。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_10685/figures/007_Table_2.jpg]]
*Table 2: Evaluation of human-object interaction motion generation on SAMP [10] sitting test set. Compared to DIMOS, our approach reaches the goal pose more accurately and exhibits fewer object penetrations, resulting in higher human preference*

### 消融实验

**测试时引导的有效性（Table 3）**


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_10685/figures/008_Table_3.jpg]]
*Table 3: Test-time guidance evaluation. Adding guidance to reach goal poses and avoid collisions during inference improves performance. Lower is better for all metrics*

TeSMo 在推理阶段引入了两种测试时引导：目标到达引导（$\mathcal{I}_g = (\hat{\mathbf{x}}_0^N - \mathbf{g})^2$）和碰撞引导（导航中为骨盆位置在可行走区域外的平均正 2D 距离 $\mathcal{T}_c = \mathrm{SDF}(\hat{\mathbf{x}}_0, \mathcal{M})$，交互中为身体顶点在物体内部的平均正符号距离 $\mathcal{T}_c = \mathrm{SDF}(\hat{\mathbf{x}}_0, S_{\mathcal{O}})$）。消融结果表明，同时启用两种引导对导航和交互指标均有提升：在导航中，目标位置误差从 0.1568 降至 0.1241。这验证了梯度扰动公式 $\tilde{\mathbf{x}}_0 = \hat{\mathbf{x}}_0 - \alpha \nabla_{\mathbf{x}_t} \mathcal{I}(\hat{\mathbf{x}}_0)$ 在约束生成行为上的因果作用。

**两阶段生成 vs. 替代方案（Table 4）**


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_10685/figures/011_Table_4.jpg]]
*Table 4: Ablation study comparing various full-body infilling methods and different representations of navigation motion generation using the Loco-3D-FRONT test set. (Left) For generated pelvis trajectories, our approach achieves the best goal-reaching accuracy with low collision rate. (Right) After in-painting the full-body motion, our method preserves diverse and realistic movements that align with the provided text prompt, much like the model employing an alternative OminiControl full-body inpainting technique. However, our approach distinctly outperforms the model utilizing full-body representation*

TeSMo 采用“先骨盆轨迹，后全身填充”的两阶段策略。Table 4 比较了三种方案：
- **TeSMo 两阶段**：目标位置误差 0.169 m，碰撞率 0.031，R-precision 0.376，Diversity 6.415。
- **OmniControl 直接覆写**：用 OmniControl 覆写密集骨盆轨迹并联合生成全身运动，目标位置误差急剧恶化至 0.459 m，碰撞率升至 0.073。原因在于覆写破坏了轨迹的物理一致性。
- **全身体表示一阶段生成**：目标位置误差高达 0.844 m，碰撞率 0.124，且运动风格与输入文本的对齐度下降。

这表明两阶段分解是平衡目标到达精度、碰撞避免和文本可控性的关键设计选择。

### 失败模式与局限性

1. **两阶段脱节**：骨盆轨迹由导航模型生成，全身姿态由 PriorMDM 填充，两个模块独立优化可能导致骨盆运动与上半身姿态不协调。
2. **交互种类有限**：当前仅涉及“坐椅子”等有限交互类型，无法处理躺下、触摸或动态物体交互等更复杂的动作。
3. **非平面表面未处理**：方法假设地面平坦，对台阶、斜坡等非平面表面上的交互缺乏处理能力。

### 定性能力展示（Figure 7）

Figure 7 展示了 TeSMo 的三项扩展能力：
- **多样文本控制**：同一场景下，不同文本提示可生成风格迥异的导航动作。
- **A* 路径跟随**：通过轨迹混合公式 $\tilde{\mathbf{p}}_0 = s * \hat{\mathbf{p}}_0 + (1 - s) * \mathbf{p}$ 调节混合系数 $s$，可控制生成轨迹对输入 A* 路径的跟随程度。
- **测试时引导效果**：引导使导航在准确到达目标的同时避免与环境碰撞。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2404_10685/figures/006_Figure_5.jpg]]
*Figure 5: Navigation generation performance. The start pose is the green arrow, and the goal pose is the red arrow. Our method more accurately reaches the goal and avoids obstacles while style is controlled by a text prompt*




## 定位与知识库关联

### 1. 在文本-动作生成谱系中的位置

TeSMo 建立在文本到动作扩散模型的基础上，其核心基座是 **MDM**（Motion Diffusion Model）。与场景无关的通用文本-动作模型（如 **GMD** / Karunratanakul et al., ICCV 2023）相比，TeSMo 的关键差异在于引入场景感知控制分支，使生成的动作能够适应 2D 地板图或 3D 物体几何约束。这一设计使得 TeSMo 在保持文本可控性和运动质量的前提下，将扩散模型的适用边界从“无约束空间中的动作生成”拓展到“场景兼容的动作生成”。

与支持稀疏空间控制的 **OmniControl**（Xie et al., arXiv 2023）相比，TeSMo 在导航阶段采用了不同的策略：OmniControl 通过覆写密集骨盆轨迹来施加空间约束，但这会严重损害目标到达能力（目标位置误差从 0.169 恶化至 0.459，Table 4）。TeSMo 则采用两阶段层次化生成——先生成骨盆轨迹，再通过 PriorMDM 进行全身内部填充——在保持目标到达精度的同时获得更低的碰撞率。

在交互动作生成方面，**DIMOS**（Zhao et al., ICCV 2023）是基于强化学习的方法，代表了此前场景内交互生成的最先进水平。TeSMo 在 SAMP 坐姿测试集上全面超越 DIMOS：目标位置误差降低 28.5%（0.1445 vs 0.2020），物体穿透率降低 43.2%（0.0611 vs 0.1076），且在用户感知研究中获得 71.9% 的偏好率（Table 2）。这一差距的因果机制在于：DIMOS 依赖 RL 策略在物理模拟器中探索，而 TeSMo 利用预训练扩散模型的强先验，在保持运动自然度的同时通过测试时引导显式优化目标到达和碰撞避免。

### 2. 核心设计决策的适用边界

**两阶段分解（导航 + 交互）** 是 TeSMo 的核心架构选择，其有效性边界如下：

- **优势边界**：当任务可以自然分解为“接近目标”和“执行交互”时，两阶段设计允许为每个阶段选择最优的场景表征（导航用 2D 地板图，交互用 3D 物体 BPS 特征），且各阶段的扩散模型可以独立预训练和微调。
- **失效边界**：当导航与交互高度耦合时（如边走边伸手触摸物体），两阶段间的骨盆轨迹与全身姿态可能出现不协调。消融实验（Table 4）证实，单阶段全身体生成虽然避免了阶段脱节，但目标到达能力显著下降（位置误差 0.844 vs 0.169），且文本对齐度降低。这表明当前的两阶段设计是在“目标到达精度”与“全身协调性”之间的一个折中——该折中在坐椅子等“先到达后交互”的场景中成立，但在连续交互场景中可能失效。

**预训练 + 微调策略** 的适用边界：

- 该策略假设场景无关的大规模动捕数据（HumanML3D、SAMP）能够提供足够的运动先验，使得微调时仅需少量场景数据即可适配。当目标场景的动作分布与预训练数据差异过大时（如非平面表面上的动作），这一假设可能不成立。
- 消融实验（Table 1）表明，从零开始训练的单分支架构在目标到达和碰撞率上均不如两分支微调方案，验证了预训练先验在数据稀缺场景下的关键作用。

**测试时引导** 的适用边界：

- 目标到达引导（$\mathcal{I}_g$）和碰撞引导（$\mathcal{T}_c$）在推理时显著提升性能（Table 3），但其效果依赖于引导权重的合理设置——权重过大会导致运动失真，过小则约束不足。
- 碰撞引导依赖场景的 SDF 表示，对于复杂几何或动态场景，SDF 的计算精度和效率可能成为瓶颈。

### 3. 局限性与开放问题

**已验证的局限性**（来自原文讨论）：

1. **两阶段脱节**：骨盆轨迹生成与全身内部填充之间的不协调是当前设计的固有缺陷，尤其在需要精确足部放置或骨盆与上身紧密配合的动作中更为明显。
2. **交互类型有限**：当前仅验证了坐椅子这一种交互类型，无法处理躺下、触摸、推拉等更复杂的交互动作，也无法应对动态物体。
3. **平面假设**：方法假设地面为平面，对台阶、斜坡等非平面表面上的导航和交互缺乏处理能力。

**开放问题**：

1. **一阶段联合生成**：如何设计一个统一的扩散模型，同时生成骨盆轨迹和全身姿态，避免两阶段间的信息损失？这需要在模型架构层面解决“全局路径规划”与“局部姿态细节”之间的尺度差异。
2. **交互谱系扩展**：将方法扩展到更丰富的交互类型（躺下、触摸、动态物体交互）需要解决两个子问题：(a) 如何获取或生成对应的训练数据；(b) 如何设计适用于不同交互类型的场景表征和目标函数。
3. **LLM 规划器集成**：原文提出利用 LLM 规划器来指定动作序列和接触信息，这需要解决“语言指令到空间约束”的映射问题，以及如何将离散的动作序列转化为扩散模型的条件信号。
4. **非平面表面处理**：将 2D 地板图扩展到带高度的 2.5D 或全 3D 场景表征，同时重新设计碰撞引导目标函数，是处理台阶、斜坡等场景的可能方向。



## 原文 PDF

![[paperPDFs/ECCV_2024/Generating_Human_Interaction_Motions_in_Scenes_with_Text_Control.pdf]]

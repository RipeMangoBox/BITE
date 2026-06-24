---
title: "HOIDiNi: Human-Object Interaction through Diffusion Noise Optimization"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization.pdf
aliases:
- HOIDiNi
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将HOI生成解耦为对象中心阶段（确定物体轨迹与接触对）和人体中心阶段（在固定蓝图下优化全身运动），并用学习到的接触对预测替代脆弱的最近邻启发式，使扩散噪声优化能稳定收敛且不牺牲真实感。
primary_logic: 在预训练扩散模型的噪声空间内执行两阶段扩散噪声优化（DNO）：对象阶段固定物体运动和接触蓝图，人体阶段基于该蓝图优化全身姿态与手指，从而在不偏离人体运动流形的前提下满足严格的物理接触约束。
claims:
- 两阶段优化相比单阶段优化将接触损失降低10倍，且接触比特在第二阶段保持稳定。
- HOIDiNi在GRAB数据集上FID降至0.159，IRA提升至62.3%，浮空误差从52.2mm降至2.3mm。
- 用户研究中超过72%的参与者偏好HOIDiNi生成的抓取质量和整体效果。
- 用最近邻替代接触对预测导致IRA从62.3%降至57.9%，验证了学习接触对的关键作用。
---

# HOIDiNi: Human-Object Interaction through Diffusion Noise Optimization

> [!tip] 核心洞察
> 在预训练扩散模型的噪声空间内执行两阶段扩散噪声优化（DNO）：对象阶段固定物体运动和接触蓝图，人体阶段基于该蓝图优化全身姿态与手指，从而在不偏离人体运动流形的前提下满足严格的物理接触约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOIDiNi：通过扩散噪声优化的人体-物体交互生成 |
| 英文题名 | HOIDiNi: Human-Object Interaction through Diffusion Noise Optimization |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://hoidini.github.io/) · [paper](https://arxiv.org/abs/2506.15625) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HOIDiNi |
| Dataset | GRAB, OMOMO |

> [!tip] 效果简介
> - GRAB 上，FID ↓ 0.159 vs 0.205 (IMoS) (-0.046)；IRA ↑ 62.3% vs 46.5% (IMoS) (+15.8%)；Floating (mm) ↓ 2.3±4.7 vs 52.2±53.8 (IMoS) (-49.9)。
> - OMOMO 上，C_F1 ↑ 0.77 vs 0.67 (CHOIS) (+0.10)；T_s (cm) ↓ 0.00 vs 1.90 (CHOIS) (-1.90)。

## 概述

**核心问题**：现有的人体-物体交互（HOI）生成方法面临一个根本性瓶颈——在保持运动自然感与实现毫米级精确的手-物体接触之间存在难以调和的张力。无论是基于后处理优化的方法（如 **IMoS**，Ghosh et al., CVPR 2023），还是基于扩散模型与分类器引导的方法（如 **CHOIS**，Li et al., CVPR 2024），其优化过程常常偏离人体运动的自然流形，导致失真、穿透或严重浮空。

**核心思路**：HOIDiNi 提出了一种解耦策略，将复杂的 HOI 生成问题拆分为两个独立的优化阶段。在 **对象中心阶段（Object-Centric Phase）**，系统首先确定物体的运动轨迹以及手与物体表面的接触蓝图（Contact Pairs）；随后在 **人体中心阶段（Human-Centric Phase）**，基于已固定的物体运动和接触约束，优化全身姿态与手指动作。两阶段均在预训练扩散模型的初始噪声空间中执行 **扩散噪声优化（Diffusion Noise Optimization, DNO）**，通过梯度反传穿越全部去噪步骤，在满足严格物理接触约束的同时，确保生成结果不偏离人体运动流形。

**关键创新**：
- **学习型接触对预测**：替代传统方法中脆弱的最近邻启发式，动态预测手掌锚点的二元接触状态与物体表面 3D 位置，为后续优化提供稳定且语义准确的接触蓝图。
- **两阶段 DNO 优化**：对象阶段固定接触蓝图，人体阶段专注全身运动优化，使接触损失降低一个数量级，且接触比特在第二阶段保持稳定（Figure 8）。

**主要结果**：
- 在 **GRAB** 数据集上，HOIDiNi 的 FID 降至 **0.159**（IMoS 为 0.205），交互区域准确率（IRA）提升至 **62.3%**（IMoS 为 46.5%），浮空误差从 52.2 mm 骤降至 **2.3 mm**（Table 1）。
- 在 **OMOMO** 数据集上，接触 F1 分数达到 **0.77**（CHOIS 为 0.67），物体起始位置误差降至 **0.00 cm**（Table 2）。
- 用户研究中，超过 **72%** 的参与者偏好 HOIDiNi 生成的抓取质量和整体效果（Figure 7）。

**方法定位**：HOIDiNi 属于测试时优化方法，不依赖特定模型架构或训练范式，可视为一种通用的 HOI 生成后处理框架。其核心贡献在于证明了“解耦优化 + 扩散噪声空间约束”这一范式在保持运动真实感的同时，能够实现此前方法无法达到的物理接触精度。

## 背景与动机

### 人体-物体交互生成的核心瓶颈

人体-物体交互（HOI）生成是计算机视觉与图形学的核心挑战之一，其目标是根据文本描述和物体几何，合成自然且物理合理的人体运动序列。这一任务在机器人学习、虚拟现实和动画制作中具有广泛的应用前景。然而，现有方法长期受困于一个根本性矛盾：**在保持运动自然感的同时，实现毫米级精确的手-物体接触**。

具体而言，高质量的HOI生成需要同时满足两个看似冲突的约束。一方面，人体运动必须保持在自然运动流形上——即生成的动作应像人类真实运动一样流畅、多样且符合生物力学规律。另一方面，手部与物体之间必须建立精确的物理接触：手指应准确触及物体表面指定位置，不能出现穿透或浮空。现有方法往往顾此失彼：基于后处理优化的方法（如IMoS, Ghosh et al., CVPR 2023）直接在运动参数空间施加接触约束，容易将运动推离自然流形，导致动作僵硬失真；而基于分类器引导的扩散模型方法（如CHOIS, Li et al., CVPR 2024）虽能生成多样化的运动，但其引导信号缺乏对运动流形的感知，常产生严重的穿透（14.4mm）和浮空（166.8mm）问题（见Table 1）。

### 现有方法的系统性缺陷

从技术路径审视，现有HOI生成方法的局限可归结为三个层面：

**第一，接触建模的脆弱性。** 多数方法依赖最近邻启发式来确定手-物体接触对应关系（如DiffGrasp、BimArt等），即简单地将手部锚点匹配到物体表面的最近点。这种纯几何策略忽略了接触的语义合理性——例如，“握相机”时食指应自然落在快门上，而非最近的任意表面点。当物体形状复杂或交互语义精细时，最近邻匹配会频繁产生错误接触对，导致抓取姿态语义错误且物理不可行。

**第二，优化策略的单阶段困境。** 无论是后处理优化还是分类器引导，现有方法通常将物体运动、人体姿态和接触关系视为一个整体进行同步优化。这种单阶段策略面临一个根本性困难：接触预测与运动生成相互耦合，优化过程中接触目标的不断变化导致损失函数震荡，难以收敛到稳定解。正如Figure 8所示，单阶段优化中接触损失剧烈波动，而接触比特（contact bits）在每一步都在翻转，使优化目标本身成为移动靶。

**第三，运动流形保真度的缺失。** 传统优化方法直接在SMPL-X姿态参数空间施加接触约束，缺乏对“什么是合理人体运动”的先验知识。分类器引导虽工作在扩散模型的隐空间，但其梯度仅反映约束满足程度，并不感知运动分布边界。两种策略都会将生成结果推离训练分布，导致动作失真、关节反向或动力学异常。

### 本文动机与核心思路

针对上述瓶颈，HOIDiNi提出了一条新的技术路径：**将HOI生成解耦为两阶段扩散噪声优化（Diffusion Noise Optimization, DNO）过程**，在预训练扩散模型的噪声空间中完成约束满足，从而在不偏离运动流形的前提下实现精确接触。

这一思路基于一个关键洞察：预训练扩散模型已经编码了丰富的人体-物体联合运动先验，其初始噪声空间构成了一个平滑的隐流形。若能在此空间中执行优化——即通过梯度反传调整初始噪声，使去噪后的样本满足接触约束——则优化轨迹将天然保持在运动分布的高密度区域。这正是DNO（Karunratanakul et al., 2024）的核心机制：将初始噪声 $x_T$ 视为隐变量，通过ODE求解器得到生成样本，并施加任务损失与去相关正则化：

$$x_T^* = \arg\min_{x_T} \{ \mathcal{L}(\mathrm{ODE}(G, x_T)) + \mathcal{R}_{\mathrm{decorr}}(x_T) \}$$

然而，直接将DNO应用于HOI任务仍面临耦合优化问题。HOIDiNi的解决方案是将问题拆分为两个顺序阶段：**对象中心阶段（Object-Centric Phase）** 首先固定物体运动轨迹和手-物体接触蓝图（Contact Pairs），确保交互的物理框架稳定；随后**人体中心阶段（Human-Centric Phase）** 在此固定蓝图下优化全身运动与手指姿态，使人体自然适应已确定的接触约束。两阶段设计的关键在于，接触对在第一阶段被确定后不再变化，为第二阶段提供了稳定的优化目标，从而避免了单阶段方法中接触预测与运动生成相互干扰的困境。

此外，HOIDiNi用**学习预测的接触对（Contact Pairs）** 替代脆弱的最近邻启发式。CPHOI扩散模型自回归地预测每个手掌锚点的二元接触状态 $b_a \in \{0,1\}$ 及其在物体表面的对应3D位置 $p_a \in \mathbb{R}^3$，形成语义上有意义的接触表示：

$$F_{CP} = [p_1, \dots, p_{|A|}, b_1, \dots, b_{|A|}]$$

这一表示被联合编码到人体运动特征 $F_H$ 和物体运动特征 $F_O$ 共享的表示空间中，使模型能够学习接触模式与运动动力学之间的深层关联，而非依赖几何启发式。

综上，HOIDiNi通过“两阶段解耦 + 扩散噪声优化 + 学习接触对”的组合策略，在保持运动自然感的同时将浮空误差从52.2mm降至2.3mm，接触成功率（IRA）从46.5%提升至62.3%（Table 1），为HOI生成任务建立了新的精度与真实感平衡点。

## 核心创新

HOIDiNi的核心创新在于将人体-物体交互（HOI）生成问题**解耦为两阶段扩散噪声优化（DNO）**，并通过**学习到的接触对预测**替代脆弱的启发式规则，从而在保持运动自然感的同时实现毫米级精确的手-物体接触。其关键设计变更体现在以下四个维度。

### 两阶段优化策略：从耦合到解耦

现有方法（如IMoS的单一后处理优化或CHOIS的分类器引导）通常同时优化人体、物体和接触的所有变量。这种耦合优化极易导致优化过程偏离人体运动的自然流形，产生不真实的姿态和严重的穿透或浮空。HOIDiNi将优化过程明确划分为两个阶段：

- **对象中心阶段（Object-Centric Phase）**：首先固定物体运动轨迹和接触蓝图。该阶段通过DNO优化物体轨迹与接触对（Contact Pairs），使用穿透损失、目标达到损失和静态损失（见公式 $\mathcal{L}_{Object}$），确保物体运动在物理上合理且接触对语义准确。
- **人体中心阶段（Human-Centric Phase）**：在对象阶段确定的物体轨迹和接触对固定不变的前提下，通过DNO优化全身运动（包括身体姿态和手指细节），使用接触对齐损失、穿透损失、脚步接触损失和抖动损失（见公式 $\mathcal{L}_{Human}$），使人体运动严格满足已建立的物理接触约束。

Figure 8提供了决定性证据：单阶段优化中接触预测随运动同步变化，导致目标函数不稳定且难以收敛；而两阶段优化将接触对在对象阶段后固定，人体阶段的接触损失稳定收敛至**低10倍**的值，且接触比特（contact bits）在第二阶段保持不变。这一设计是HOIDiNi实现稳定收敛的核心机制。

### 从最近邻到学习预测：接触对生成

接触点的生成方式是从基线到HOIDiNi最关键的变更之一。先前工作（如DiffGrasp、BimArt）普遍采用**最近邻启发式**：在物体表面搜索距离手部锚点最近的点作为接触位置。这种方法对噪声敏感，常导致语义不匹配的接触（例如手掌握在物体边缘而非可抓取部位）。

HOIDiNi用**学习预测的接触对（Contact Pairs）**替代这一启发式。CPHOI扩散模型为手掌预定义的锚点集合 $\mathcal{A}$ 逐帧预测：
- 每个锚点的布尔接触状态 $b_a \in \{0,1\}$（是否与物体接触）
- 对应的物体表面3D位置 $p_a \in \mathbb{R}^3$

接触对特征表示为 $F_{CP} = [p_1, \dots, p_{|A|}, b_1, \dots, b_{|A|}]$（如Figure 3所示，彩色球体标记了语义匹配的接触对）。消融实验证实了这一设计的决定性作用：用最近邻替代接触对预测后，IRA（交互区域准确率）从**62.3%降至57.9%**（Table 1），验证了学习接触对对于接触准确性的关键贡献。

### 扩散噪声优化：在流形上施加约束

施加约束的方式是HOIDiNi区别于分类器引导方法（如CHOIS）的根本差异。分类器引导在生成过程中通过梯度信号引导样本朝向约束目标，但这种方式缺乏对流形保真度的显式保证，容易导致生成样本偏离人体运动分布。

HOIDiNi采用**扩散噪声优化（DNO）**：将扩散模型的初始噪声 $x_T$ 视为可优化变量，通过ODE求解器得到生成样本，并在样本上施加任务损失，梯度通过**全部去噪步骤**反向传播。核心优化形式为：

$$x_T^* = \arg\min_{x_T} \{ \mathcal{L}(\mathrm{ODE}(G, x_T)) + \mathcal{R}_{\mathrm{decorr}}(x_T) \}$$

这一机制确保优化过程始终在预训练扩散模型所学习的人体运动流形上进行。Table 1的对比提供了强有力证据：分类器引导导致严重穿透（**14.4mm**）和极度浮空（**166.8mm**），而HOIDiNi的DNO将穿透控制在**6.8mm**、浮空降至**2.3mm**，同时保持FID为**0.159**（优于分类器引导的0.221）。

### 联合表示空间：从分离到统一

模型输出内容的变更体现了HOIDiNi对HOI问题的整体建模。先前方法通常仅生成身体运动或仅生成手部轨迹，缺乏统一的接触描述。HOIDiNi的CPHOI扩散模型**联合生成**接触对（CP）、人体运动（H）和物体轨迹（O），三者共享表示空间并在自回归框架下统一建模（Figure 4）。

具体而言，每帧特征包含：
- **人体运动** $F_H = [r_z^H, \dot{r}_x^H, \dot{r}_y^H, \dot{\alpha}^H, \theta^H, j^H]$：根高度、平面速度、角速度、SMPL-X姿态参数及相对关节位置
- **物体运动** $F_O = [\theta^O, r^O, \dot{r}^O]$：连续6维旋转表征、全局平移及线速度
- **接触对** $F_{CP}$：如上所述的锚点接触状态与位置

这种联合表示使得两个优化阶段能够共享同一预训练模型，对象阶段固定CP和O后，人体阶段可直接在共享的噪声空间上优化H，无需额外的模型适配或表示转换。Table 1的消融显示，仅在第一阶段推理、第二阶段DNO（Phase1 Inference, Phase2 DNO）即可获得合理结果，但多样性下降，进一步证实了联合建模对生成质量的重要性。

## 整体框架

HOIDiNi 的整体生成流程围绕一个核心洞察展开：**在预训练扩散模型的噪声空间内执行两阶段扩散噪声优化（DNO），可以在不偏离人体运动流形的前提下满足严格的物理接触约束**。系统接受三类输入——描述交互的文本提示、物体网格（mesh）以及场景占用体积（occupied volume），通过一个预训练的自回归扩散模型 CPHOI 生成人体运动、物体轨迹与接触对的联合分布，再经由对象中心（Object-Centric）和人体中心（Human-Centric）两个优化阶段，输出精确且自然的人体-物体交互运动（Figure 2）。

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/002_Figure_2.jpg]]
*Figure 2: System Overview. HOIDiNi generates Human-object Interaction (HOI) motions according to a text prompt, a mesh describing the object, and the occupied volume in the scene, by optimizing the diffusion noise. The Object-Centric Phase generates the object motion and its contact points with the hands (CP and O), then the Human-Centric Phase follows and generates the full human motion(H): body and fingers, adhering to the constraints implied by the previous phase. Both phases use CPHOI, a pre-trained diffusion model that learned the human-object joint distribution. We apply Diffusion Noise Optimization (DNO) (Karunratanakul et al., 2024) to fulfill the two sets of loss functions*

### 核心模块与数据流

**1. 联合表示空间**

系统首先将人体运动、物体轨迹和手-物接触统一编码到一个共享的表示空间（Section 4.1）：
- **接触对特征** $F_{CP} = [p_1, \dots, p_{|A|}, b_1, \dots, b_{|A|}]$：对于预定义的手掌锚点集合 $A$，每帧包含各锚点在物体表面的 3D 坐标 $p_a \in \mathbb{R}^3$ 和二元接触标志 $b_a \in \{0,1\}$。
- **人体运动特征** $F_H = [r_z^H, \dot{r}_x^H, \dot{r}_y^H, \dot{\alpha}^H, \theta^H, j^H]$：根高度、平面速度、角速度、SMPL-X 姿态参数及相对关节位置。
- **物体运动特征** $F_O = [\theta^O, r^O, \dot{r}^O]$：连续 6 维旋转表征、全局平移及线速度。

这一联合表示使模型能够同时推理“手应该接触哪里”和“身体应该如何运动”，避免了先前方法中接触信息与运动生成脱节的问题。

**2. CPHOI 扩散模型**

CPHOI 是一个自回归扩散模型（Figure 4），学习人体运动、物体轨迹与接触对的联合分布 $p(s^n \mid s^{n-1}, \text{geometry}, \text{text})$。给定前一个运动分段 $s^{n-1}$，模型通过 DDPM 去噪过程预测下一分段 $s^n$ 的干净样本 $\hat{s}_0^n$，训练目标为：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim p(x_0 | c), t \sim [1, T]} \left[| x_0 - \hat{x}_0 |_2^2 \right]$$

模型的条件输入包括：PointNet++ 从物体网格采样 512 个点编码的几何特征，以及固定参数的 DistilBERT 对文本提示编码的嵌入序列。

**3. 两阶段扩散噪声优化（DNO）**

这是 HOIDiNi 的核心因果机制：将初始噪声 $x_T$ 作为隐变量，通过 ODE 求解器得到生成样本，并在噪声空间施加任务损失进行优化：

$$x_T^* = \arg\min_{x_T} \{ \mathcal{L}(\mathrm{ODE}(G, x_T)) + \mathcal{R}_{\mathrm{decorr}}(x_T) \}$$

梯度通过全部去噪步骤反传，确保优化后的输出仍保持在扩散模型学习的运动流形上。两阶段划分解决了单阶段优化中接触目标与运动目标相互干扰的问题（Figure 8）：

- **对象中心阶段（Phase 1）**：固定人体运动，仅优化物体轨迹和接触对，使用穿透损失、目标达到损失和静态损失构成的 $\mathcal{L}_{Object}$。此阶段确定物体运动蓝图和精确的手-物接触对。
- **人体中心阶段（Phase 2）**：固定 Phase 1 输出的接触对与物体轨迹，优化全身运动（包括身体姿态和手指），使用接触对齐损失、人体穿透损失（人-物、人-场景、人-人三个分量）、脚步接触损失和抖动损失构成的 $\mathcal{L}_{Human}$。

**4. 接触对预测的关键作用**

与先前方法（如 DiffGrasp、BimArt）使用的最近邻启发式不同，HOIDiNi 通过学习预测每个锚点的接触状态和物体表面位置（Figure 3），实现了语义匹配的精确接触。消融实验证实，用最近邻替代学习到的接触对预测会导致 IRA 从 62.3% 降至 57.9%（Table 1），验证了这一设计选择的关键性。

### 输入输出流总结

- **输入**：文本交互描述 + 物体网格 + 场景占用体积
- **编码**：DistilBERT 文本编码 + PointNet++ 几何编码 → 条件嵌入
- **生成**：CPHOI 自回归扩散模型 → 初始运动分段（含人体、物体、接触对）
- **优化 Phase 1**：DNO 优化物体轨迹与接触对 → 固定物体蓝图
- **优化 Phase 2**：DNO 在固定蓝图下优化全身运动 → 最终 HOI 运动
- **输出**：满足物理接触约束且保持运动自然感的人体-物体交互序列

该框架的核心优势在于：**通过解耦对象与人体优化阶段，并利用学习到的接触对预测替代脆弱的启发式规则，使扩散噪声优化能够稳定收敛至毫米级接触精度，同时不牺牲运动真实感**。

### 补充图表

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/001_Figure_1.jpg]]
*Figure 1: HOIDiNi generates human-object interactions from text descriptions and object geometry, integrated here into a 3D scene from Jay-Artist (2012)*

## 核心模块与公式推导

### 3.1 扩散噪声优化（DNO）基础

HOIDiNi 的核心优化框架建立在扩散噪声优化（DNO）之上。DNO 将预训练扩散模型的初始噪声 $x_T$ 视为隐变量，通过 ODE 求解器反向去噪得到生成样本，并在该样本上施加任务损失与正则化项，梯度通过全部去噪步骤反传至 $x_T$ 进行优化。其形式化目标为：

$$x_T^* = \arg\min_{x_T} \{ \mathcal{L}(\mathrm{ODE}(G, x_T)) + \mathcal{R}_{\mathrm{decorr}}(x_T) \}$$

其中 $\mathrm{ODE}(G, x_T)$ 表示以 $x_T$ 为起点的去噪轨迹，$\mathcal{L}$ 为下游任务损失，$\mathcal{R}_{\mathrm{decorr}}$ 为去相关正则化项，用于抑制噪声空间中的高频伪影。

扩散模型的训练采用 $x_0$ 预测范式，训练目标为：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim p(x_0 | c), t \sim [1, T]} \left[| x_0 - \hat{x}_0 |_2^2 \right]$$

该目标使模型直接预测干净样本 $\hat{x}_0$，为后续 DNO 提供可微分的去噪映射。

### 3.2 联合表示空间

HOIDiNi 定义了一个结构化数据表示，将全身人体运动、物体轨迹和表面级接触点统一编码。每帧特征由三个分量组成：

**接触对特征** $F_{CP}$：对于预定义的手掌锚点集 $\mathcal{A}$，每帧编码每个锚点 $a$ 的物体表面 3D 位置 $p_a \in \mathbb{R}^3$ 和二元接触标志 $b_a \in \{0,1\}$：

$$F_{CP} = [p_1, \dots, p_{|\mathcal{A}|}, b_1, \dots, b_{|\mathcal{A}|}]$$

**人体运动特征** $F_H$：每帧包含根节点高度 $r_z^H$、平面速度 $\dot{r}_x^H, \dot{r}_y^H$、角速度 $\dot{\alpha}^H$、SMPL-X 姿态参数 $\theta^H$ 及相对关节位置 $j^H$：

$$F_H = [r_z^H, \dot{r}_x^H, \dot{r}_y^H, \dot{\alpha}^H, \theta^H, j^H]$$

**物体运动特征** $F_O$：每帧包含连续 6 维旋转表征 $\theta^O$、全局平移 $r^O$ 及线速度 $\dot{r}^O$：

$$F_O = [\theta^O, r^O, \dot{r}^O]$$

### 3.3 两阶段优化损失函数

HOIDiNi 将 HOI 生成解耦为对象中心阶段和人体中心阶段，每个阶段通过 DNO 优化各自的损失函数。

#### 对象阶段损失

Phase 1 优化物体轨迹和接触对，目标函数为：

$$\mathcal{L}_{Object} = \lambda_{Pos} \mathcal{L}_{Pos} + \lambda_{Goal} \mathcal{L}_{Goal} + \lambda_{Static} \mathcal{L}_{Static}$$

其中 $\mathcal{L}_{Pos}$ 为穿透损失，采用对称双向形式。以网格 $M_a$ 到 $M_b$ 的方向穿透损失为例：

$$\mathcal{L}_{\mathrm{pen}}(M_a \to M_b) = \frac{1}{|\mathcal{V}_a|} \sum_{\mathbf{v} \in \mathcal{V}_a^{\mathrm{in}}} \| \mathbf{v} - \mathbf{NN}(\mathbf{v}; M_b) \|^2$$

该损失对 $M_a$ 中位于 $M_b$ 内部的顶点 $\mathbf{v}$，计算其到 $M_b$ 表面最近点 $\mathbf{NN}(\mathbf{v}; M_b)$ 的距离平方。总穿透损失取双向和。

$\mathcal{L}_{Goal}$ 为目标达到损失，惩罚物体在关键帧 $\mathcal{T}$ 的位姿偏差：

$$\mathcal{L}_{\mathrm{Goal}} = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} \Bigl( \|\hat{\mathbf{t}}_{t} - \mathbf{t}_{t}\|^2 + \mathcal{D}_{\mathrm{rot}}\bigl(\hat{R}_t, R_t\bigr)\Bigr)$$

$\mathcal{L}_{Static}$ 为静态损失，在无接触区间 $\mathcal{T}_s^{\mathrm{nc}}$ 内制止物体运动，锚定位置和旋转到该区间起始帧 $t_s^{\mathrm{start}}$：

$$\mathcal{L}_{\mathrm{Static}} = \frac{1}{\sum_{s} |\mathcal{T}_s^{\mathrm{nc}}|} \sum_{s} \sum_{t \in \mathcal{T}_s^{\mathrm{nc}}} \Big( \|\mathbf{t}_t - \mathbf{t}_{t_s^{\mathrm{start}}}\|^2 + \mathcal{D}_{\mathrm{rot}}(R_t, R_{t_s^{\mathrm{start}}}) \Big)$$

#### 人体阶段损失

Phase 2 在固定接触对与物体轨迹的条件下优化全身运动，目标函数为：

$$\mathcal{L}_{Human} = \lambda_{C} \mathcal{L}_{C} + \mathcal{L}_{P_H} + \lambda_{Foot} \mathcal{L}_{Foot} + \lambda_{Jitter} \mathcal{L}_{Jitter}$$

其中 $\mathcal{L}_{C}$ 为接触对齐损失，驱动手掌锚点向 Phase 1 确定的物体表面接触位置收敛。$\mathcal{L}_{P_H}$ 为人体穿透损失，包含三个分量：

$$\mathcal{L}_{P_H} = \lambda_{P_{HO}} \mathcal{L}_{P_{HO}} + \lambda_{P_{HS}} \mathcal{L}_{P_{HS}} + \lambda_{P_{HH}} \mathcal{L}_{P_{HH}}$$

分别对应人-物穿透、人-场景穿透和人-人自穿透，每个分量均采用与对象阶段一致的对称穿透损失形式。

$\mathcal{L}_{Foot}$ 为脚步接触损失，鼓励较低脚趾关节高度接近地面阈值 $h = 0.02\mathrm{m}$：

$$L_{\mathrm{FeetFloorContact}} = |\operatorname*{min}(J_l^z, J_r^z) - h|_2$$

$\mathcal{L}_{Jitter}$ 为抖动正则化，惩罚相邻帧间关节位置的突变。

### 3.4 关键模块

**CPHOI 扩散模型**：自回归扩散模型，学习人体运动、物体轨迹与接触对的联合分布。以运动分段 $s^n$ 为生成单元，条件于上一分段 $s^{n-1}$、物体几何编码和文本嵌入，通过去噪一步预测 $\hat{s}_0^n$。模型架构如图 4 所示。

**接触对预测**：CPHOI 动态预测每个手掌锚点的布尔接触状态及对应的物体表面 3D 位置。相比传统最近邻启发式，学习到的接触对预测提供了语义更准确、更稳定的接触蓝图，是两阶段优化稳定收敛的关键——消融实验中用最近邻替代接触对预测导致 IRA 从 62.3% 降至 57.9%。

**物体几何编码器**：采用 PointNet++ 对物体网格采样 512 个点并编码为几何特征，作为 CPHOI 扩散模型的条件输入。

**文本编码器**：使用固定参数的 DistilBERT 将文本提示编码为嵌入序列，提供交互语义条件。

### 3.5 两阶段解耦的核心机理

两阶段解耦的关键收益在于：对象阶段固定接触蓝图后，人体阶段的接触损失目标不再变化，避免了单阶段优化中接触预测与运动参数同时演化导致的目标函数不稳定。如图 8 所示，单阶段优化中接触损失震荡且接触比特持续翻转，而两阶段优化使接触损失收敛至低 10 倍的值，且接触比特在第二阶段保持稳定。这一解耦策略是 DNO 能够在保持运动流形保真度的同时实现毫米级接触精度的根本原因。

### 补充图表

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/005_Figure_4.jpg]]
*Figure 4: CPHOI Diffusion Model. CPHOI autoregressively predicts the next motion segment*

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/003_Figure_3.jpg]]
*Figure 3: Contact Pairs. CPHOI predicts precise, semantically meaningful contact points between the hand and object. Each contact pair is visualized with matching colored spheres*

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/010_Figure_8.jpg]]
*Figure 8: Single vs. Two-Phase Optimization. Comparison of contact loss and changes in predicted contact bits during DNO optimization (shared y-axis). (Left): In the single-phase setup, contact predictions evolve alongside motion, causing unstable objectives and hindering convergence. (Right): In our two-phase approach, contact pairs are fixed after the object-centric phase, resulting in stable contact loss during the human-centric phase presented here. In this example, the two-phase setting converges to a 10× lower value. Contact-Bits Changes denote the number of bit flips in the predicted contact matrix between successive steps*

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/013_Figure_10.jpg]]
*Figure 10: Palm anchor set A used by CPHOI for the GRAB (Taheri et al., 2020a) experiment*

## 实验与分析

### 核心定量结果

HOIDiNi在GRAB和OMOMO两个基准上均显著超越现有方法，实现了运动真实感与物理准确性的双重提升。

在GRAB数据集上，与基于后处理优化的**IMoS**（Ghosh et al., CVPR 2023）相比，HOIDiNi将FID从0.205降至0.159，接触精度IRA从46.5%提升至62.3%，浮空误差从52.2mm骤降至2.3mm（Table 1）。这一近50mm的浮空改善直接验证了两阶段扩散噪声优化（DNO）在维持毫米级接触精度上的有效性——物体阶段先锁定接触蓝图，人体阶段再围绕固定约束优化全身运动，避免了单阶段优化中接触预测与运动生成相互干扰导致的收敛困难。

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/007_Table_1.jpg]]
*Table 1: Quantitative Results and Ablation Study. Comparison on the GRAB dataset (Taheri et al., 2020b) using IMoS-defined (Ghosh et al., 2023) metrics for motion realism, along with average floating and penetration errors (in millimeters). → indicates that better is closer to ground-truth performance*

在OMOMO数据集上，HOIDiNi与使用分类器引导的扩散方法**CHOIS**（Li et al., CVPR 2024）对比，条件匹配F1分数从0.67提升至0.77，物体平移误差T_s从1.90cm降至0.00cm（Table 2）。零平移误差表明DNO在满足空间约束上比分类器引导更为精确——后者通过梯度引导生成过程，但缺乏对运动流形的显式保持，容易为满足约束而偏离合理运动分布。

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/009_Table_2.jpg]]
*Table 2: Comparison to CHOIS (Li et al., 2024a) over the OMOMO (Li et al., 2023) dataset. Measuring condition matching, human motion, and interaction via a set of metrics defined by CHOIS*

用户研究进一步确认了这些定量优势的感知意义：在12个随机样本上，超过72%的参评者偏好HOIDiNi的抓取质量，77.6%认可其提示遵守度，80.3%认为整体质量更优（Figure 7）。

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/008_Figure_7.jpg]]
*Figure 7: User Study. We compare to two baselines, measuring on grasp quality, prompt adherence, and overall quality over 12 random samples, each evaluated by at least 10 users. The dashed line marks 50% ratio*

### 消融研究：两阶段优化的关键作用

消融实验系统揭示了HOIDiNi各设计选择的因果贡献（Table 1）：

**两阶段 vs. 单阶段优化。** 将对象阶段与人体阶段合并为单阶段DNO后，FID升至0.221，IRA降至43.0%，穿透和浮空误差均恶化。Figure 8从优化动力学角度解释了这一退化：单阶段中接触预测随运动同步演化，导致目标函数不稳定、难以收敛；而两阶段在对象阶段固定接触对后，人体阶段的接触损失稳定收敛至单阶段的1/10，且接触比特在后续优化中几乎不变。这证实了解耦对象运动与人体运动的策略是稳定收敛的关键。

**DNO vs. 分类器引导。** 用分类器引导替代DNO后，穿透误差达14.4mm，浮空误差高达166.8mm，运动严重失真。分类器引导缺乏对扩散模型去噪过程的完整梯度反传，无法在满足约束的同时保持生成样本在运动流形上，导致物理约束与运动真实感之间的根本冲突。

**接触对预测 vs. 最近邻启发式。** 将学习到的接触对预测替换为基于欧氏距离的最近邻启发式后，IRA从62.3%降至57.9%。这表明CPHOI学习到的接触对不仅是几何最近点，而是编码了语义合理的接触模式——例如“握相机”时手指应接触快门和机身特定区域，而非简单的最邻近表面点。

**推理 vs. 优化的必要性。** 仅使用CPHOI推理而不进行DNO优化，穿透和浮空误差严重，证实了扩散模型本身无法保证物理约束的满足，优化步骤不可或缺。值得注意的是，仅在对象阶段进行推理、人体阶段使用DNO即可获得合理结果，但多样性有所下降，说明两阶段均需优化以达到最佳质量。

### 失败模式与局限性

尽管HOIDiNi在接触精度和运动真实感上取得了显著进步，仍存在以下限制：

1. **数据规模约束。** CPHOI仅在GRAB的1334条序列上训练，对长尾交互类型和多样化手形的泛化能力可能不足。在未见过的物体类别或复杂手指操作（如拧瓶盖）上的表现尚未验证。

2. **接触锚点的预定义需求。** 接触对预测依赖手掌上预定义的锚点集合A（Figure 10），对于需要精细指尖接触或不同手部拓扑结构的任务，需要人工重新设计锚点布局。

3. **计算代价。** DNO需要反复查询扩散模型进行梯度反传，计算成本高于单次推理或轻量后处理优化，可能不适合实时交互应用。

4. **场景复杂度。** 当前验证限于静态物体和单人交互，未在动态障碍物、多人协作等更复杂场景下测试。

5. **文本标注偏差。** 实验中使用ChatGPT增强文本标注可能引入语言偏差或不准确的动作描述，影响模型对提示的语义理解质量。

### 补充图表

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/006_Figure_6.jpg]]
*Figure 6: Comparisons. HOIDiNi generates semantically correct and accurate interaction with the gaming controller. From left to right: IMoS (Ghosh et al., 2023) optimization yields inferior contacts and unrealistic motion; CPHOI inference only generates decent poses but fails to satisfy contacts; Our losses with Classifier Guidance brings the object insufficiently closer. Replacing our contact-point prediction with the popular nearest-neighbor heuristic fails to choose correct contacts, in contrast to our plausible and human-like result*

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/004_Figure_5.jpg]]
*Figure 5: Qualitative Results of human-object interactions generated by our method across diverse prompts. For instance, “taking a picture with a camera” yields a semantically appropriate two-handed pose. Motions are both visually plausible and aligned with the prompts*

![[assets/figures/papers/paper_list_l1684_HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization/figures/011_Table_3.jpg]]
*Table 3: Hyper-parameters in use for each experiment*

## 方法谱系与知识库定位

### 与现有工作的关系定位

HOIDiNi 处于**基于扩散模型的人体运动生成**与**物理约束优化**两条研究脉络的交汇点。其核心贡献在于将扩散噪声优化（DNO）范式系统性地适配到人体-物体交互（HOI）这一高维耦合问题中。

**相对于后处理优化方法**：以 **IMoS**（Ghosh et al., CVPR 2023）为代表的方法在扩散模型生成运动后，直接在运动参数空间施加接触约束进行优化。这种方式虽然能改善接触精度，但优化过程缺乏对运动流形的感知，容易产生不自然的姿态和抖动。HOIDiNi 将优化空间从运动参数转移到扩散模型的初始噪声空间，梯度通过完整的去噪链反传，使优化后的样本始终保持在预训练模型所刻画的人体运动流形上。这一差异在消融实验中体现为：用分类器引导（类似后处理约束）替代 DNO 时，穿透误差高达 14.4mm、浮空误差达 166.8mm，运动严重失真（Table 1）。

**相对于分类器引导方法**：**CHOIS**（Li et al., CVPR 2024）使用扩散模型配合分类器引导来实现条件生成。HOIDiNi 在 OMOMO 数据集上与 CHOIS 的直接对比显示，DNO 策略在条件匹配精度上具有显著优势——目标位置误差 T_s 从 CHOIS 的 1.90cm 降至 0.00cm，接触 F1 分数从 0.67 提升至 0.77（Table 2）。这验证了 DNO 作为一种测试时优化策略，比训练时依赖分类器引导能更精确地满足物理约束。

**相对于接触建模方法**：早期工作如 DiffGrasp 和 BimArt 采用最近邻启发式来确定手-物体接触点，这种策略对噪声敏感且缺乏语义理解。HOIDiNi 引入**可学习的 Contact Pairs 预测**，为手掌预定义锚点同时预测二元接触状态和物体表面 3D 坐标。消融实验表明，将 Contact Pairs 替换为最近邻启发式后，IRA 从 62.3% 降至 57.9%（Table 1），证实了学习式接触建模对精确交互的关键作用。

**两阶段解耦策略的理论依据**：HOIDiNi 将 HOI 优化解耦为对象中心阶段和人体中心阶段，这一设计源于对优化景观的洞察——同时优化物体轨迹、接触点和人体运动会形成高度耦合且不稳定的优化目标。Figure 8 直观展示了这一现象：单阶段优化中接触预测随运动演化而不断变化，导致接触损失振荡且难以收敛；两阶段策略在对象阶段固定接触蓝图后，人体阶段的接触损失稳定收敛至单阶段的 1/10，且接触比特在第二阶段保持完全稳定。

### 适用边界

**输入要求**：HOIDiNi 需要文本交互描述、物体网格模型和场景占位体积作为输入。物体几何通过 PointNet++ 编码为 512 点云特征，这要求物体具有完整的网格表示。

**交互类型覆盖**：方法主要针对手-物体交互设计，接触锚点预定义在手掌特定位置（Figure 10）。对于需要精细手指操作（如拧瓶盖、弹钢琴）或涉及脚部、身体其他部位与物体接触的任务，当前的锚点定义需要人工调整。

**运动时长与自回归架构**：CPHOI 采用自回归方式逐段生成运动，每段 L 帧。自回归架构虽然支持变长序列生成，但也引入了误差累积的风险，尤其对长时间交互序列的稳定性有待验证。

**数据依赖**：模型在 GRAB 数据集（1334 条序列）上训练，数据规模相对有限。这可能导致对训练数据中未充分覆盖的交互类型、物体类别或手部形态的泛化不足。

### 局限与开放问题

**计算效率**：DNO 需要在每次优化迭代中完整执行扩散模型的去噪过程（ODE 求解），反复查询扩散模型带来较高的计算代价。这限制了方法在实时交互场景（如 VR/AR 应用）中的直接部署。能否通过减少 DNO 迭代次数、采用更高效的采样器（如一致性模型）或蒸馏策略来降低计算成本，是重要的工程化方向。

**离散变量的梯度处理**：Contact Pairs 中的接触状态 $b_a \in \{0,1\}$ 是离散二值变量，DNO 如何对这些变量进行有效的梯度反传？论文未详述具体的松弛或连续化策略（如 Gumbel-Softmax 或直通估计器），这一技术细节对理解方法的可复现性至关重要。

**零样本泛化能力**：方法在 GRAB 和 OMOMO 两个数据集上验证，但这两个数据集覆盖的物体类别和交互类型有限。在未见过的物体几何、全新文本提示或跨域场景（如从日常物体到工业工具）上的泛化表现，目前缺乏系统评估。

**复杂交互场景**：当前实验设置以单人-单物体交互为主，未涉及动态障碍物避让、多人协作交互（如传递物体）、或手内操作（in-hand manipulation）等更复杂的场景。两阶段优化框架是否能够自然扩展到这些场景，特别是当多个交互约束同时存在时的优化景观特性，仍有待探索。

**权重共享与架构通用性**：论文提到两阶段优化共享权重，但具体实现方式未展开。这一设计是否可抽象为通用的 HOI 优化架构，即是否可适配到其他预训练运动扩散模型（如 MDM、MotionDiffuse）上，是方法影响力的重要指标。

**文本标注质量**：实验中使用 ChatGPT 增强文本标注，可能引入语言偏差或不准确的动作描述。这种合成标注对模型学习语义-运动映射的影响，以及与人工标注的差异，值得进一步分析。

## 原文 PDF

![[paperPDFs/arxiv_2025/HOIDiNi_Human_Object_Interaction_through_Diffusion_Noise_Optimization.pdf]]

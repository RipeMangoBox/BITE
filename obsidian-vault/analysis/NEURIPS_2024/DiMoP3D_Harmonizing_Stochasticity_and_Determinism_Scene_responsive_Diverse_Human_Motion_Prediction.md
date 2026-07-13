---
title: DiMoP3D Harmonizing Stochasticity and Determinism Scene responsive Diverse Human Motion Prediction
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diverse_Human_Motion_Prediction.pdf
project_link: null
code_link: null
aliases:
- DHSDSRDHMP
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过场景-运动跨模态兴趣分析识别交互目标，并提前规划目标姿态与无碰轨迹，将无约束的随机采样转化为由场景确定元素引导的可控随机生成。
primary_logic: 利用场景点云的几何与语义信息，将人类意图建模为可采样的交互对象，并将物理约束显式编码为A*规划的轨迹和预测的终态；在扩散去噪过程中，每一时刻都用观测序列、规划路径和终态进行对齐覆盖，使随机多样性与物理、语义确定性达成统一。
claims:
- 在GIMO和CIRCLE两个真实捕捉的基准上，DiMoP3D在所有主要指标（ADE、FDE、MMADE、MMFDE、ACPD）上均大幅超过已有方法，尤其物理一致性ACPD提升超10 cm。
- 消融实验表明，移除兴趣网络（InterestNet）使精度指标恶化，移除轨迹规划器导致ACPD升高至3.29（完整模型为0.98），验证各模块的关键作用。
- 与SOTA扩散模型BeLFusion的定性对比显示，DiMoP3D避免物体穿透、运动不连贯和场景不一致等典型失败模式。
- GIMO 上 ADE = 5.66
---

# DiMoP3D Harmonizing Stochasticity and Determinism Scene responsive Diverse Human Motion Prediction

> [!tip] 核心洞察
> 利用场景点云的几何与语义信息，将人类意图建模为可采样的交互对象，并将物理约束显式编码为A*规划的轨迹和预测的终态；在扩散去噪过程中，每一时刻都用观测序列、规划路径和终态进行对齐覆盖，使随机多样性与物理、语义确定性达成统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiMoP3D：调和随机性与确定性的场景响应式多样化人体运动预测 |
| 英文题名 | DiMoP3D Harmonizing Stochasticity and Determinism Scene responsive Diverse Human Motion Prediction |
| 会议/期刊 | NEURIPS 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DiMoP3D |
| Dataset | GIMO, CIRCLE |

> [!tip] 效果简介
> - GIMO 上，ADE 5.66 vs 9.69 (BeLFusion) (-4.03)；FDE 6.81 vs 11.19 (BeLFusion) (-4.38)；ACPD 0.98 vs 13.73 (BeLFusion) (-12.75)。
> - CIRCLE 上，ADE 5.66 vs 7.91 (BeLFusion) (-2.25)；ACPD 0.98 vs 14.06 (BeLFusion) (-13.08)。

## 概要

现有多样化人体运动预测（diverse HMP）方法在生成未来运动时完全忽略3D场景的物理与语义约束，导致预测结果出现物体穿透、运动不连贯和场景不一致等严重伪影，无法在真实环境中实际使用。DiMoP3D首次将场景响应的**确定性约束**（障碍物避碰、语义合理的交互目标选择）与运动生成的**随机多样性**统一在一个框架内，核心思路是将无约束的随机采样转化为由场景确定元素引导的可控随机生成。

具体而言，DiMoP3D由三个协同模块构成：**上下文感知的跨模态解释器**从3D场景点云中识别交互物体并预测人体兴趣区域，采样潜在的交互目标；**行为一致的随机规划器**利用改进的A*算法生成朝向目标的无碰轨迹，并通过HOI估计器预测交互终态，形成“规划轨迹—预测终态—到达时间”的随机条件因子；**自提示运动生成器**以该条件因子提示扩散模型，在去噪过程的每一步用观测序列、规划路径和预测终态进行显式先验覆盖，同时结合MotionCLIP语义对齐损失，确保生成的运动既多样又物理一致。

在GIMO和CIRCLE两个真实捕捉的基准上，DiMoP3D在所有主要指标上大幅超越已有方法：相比此前SOTA扩散模型BeLFusion，平均位移误差（ADE）降低4.03 cm，终点位移误差（FDE）降低4.38 cm，而衡量物理一致性的平均碰撞穿透距离（ACPD）从13.73 cm降至0.98 cm，提升超过一个数量级。消融实验证实，兴趣网络、HOI估计器、轨迹规划器和语义对齐检查器每个组件都对精度和物理一致性有显著贡献，其中移除轨迹规划器使ACPD恶化至3.29 cm。定性对比进一步显示，DiMoP3D有效避免了BeLFusion常见的物体穿透、运动不连贯和场景不一致等典型失败模式。

### 多样化人体运动预测的场景困境

人体运动预测（Human Motion Prediction, HMP）旨在基于观测到的历史姿态序列推断未来运动轨迹。随着具身智能与交互式场景理解的发展，预测的**多样性**变得至关重要——同一段历史运动可能对应多种合理的未来走向（如走向桌子拿起水杯，或绕过桌子走向门口）。然而，现有的多样化HMP方法（如基于流模型的**DLow**、基于VAE的**SmoothDMP**、基于扩散模型的**BeLFusion**）在追求多样性的过程中，完全忽略了3D场景施加的**确定性约束**。

这一缺失造成了严重的实际后果：当预测结果被置于真实3D场景中时，频繁出现**物体穿透**（人体穿透桌椅等障碍物）、**运动不连贯**（预测姿态与场景几何矛盾）和**场景不一致**（交互行为与物体语义不匹配）等伪影。如Figure 3所示，BeLFusion在卧室和会议室场景中产生大量穿透和漂浮行走的预测，使其输出在实际应用中几乎无法使用。

### 核心矛盾：随机性与确定性的对立

问题的本质在于**随机性**与**确定性**之间的根本张力。多样化预测需要从概率分布中采样，引入随机性以覆盖多种可能；而真实3D场景却施加了严格的确定性约束——人体不能穿透障碍物、交互行为必须与物体语义匹配、运动轨迹必须符合场景拓扑。现有方法将这两者对立起来：要么牺牲多样性换取物理一致性（如确定性方法**BiFU**），要么拥抱多样性却无视场景约束（如BeLFusion等多样化方法）。

### 本文动机：让场景引导多样性

DiMoP3D的核心动机是打破这一对立，实现**场景响应式的多样化人体运动预测**。其关键洞察在于：场景并非多样性的敌人，而是多样性的引导者。通过分析场景中哪些物体或区域是人类可能交互的目标，可以将无约束的随机采样转化为**由场景确定元素引导的可控随机生成**。

具体而言，DiMoP3D将问题建模为从过去运动与场景中采样随机条件因子 $\theta$ 的过程：

$$P(\hat{X}_{L:L+\Delta L} | X_{1:L}, S) = \int \max_{\theta} P(\hat{X}_{L:L+\Delta L} | X_{1:L}, S, \theta) P(\theta | X_{1:L}, S) d\theta$$

其中 $\theta$ 包含了交互目标、无碰轨迹规划和交互终态等场景确定性信息。这一框架使得扩散模型的随机去噪过程在每一时刻都受到场景约束的显式引导，从而在保持多样性的同时确保物理与语义一致性。

### 方法概览

为实现上述目标，DiMoP3D设计了三个协同模块：
1. **上下文感知的跨模态解释器**：从3D场景点云中识别交互对象，通过跨模态兴趣分析定位潜在交互目标；
2. **行为一致的随机规划器**：利用改进A*算法规划无碰轨迹，并预测人-物交互终态，构成随机条件因子；
3. **自提示运动生成器**：以条件因子提示的扩散模型，在去噪过程中持续对齐观测序列、规划路径和预测终态，生成多样化且物理一致的运动。

在GIMO和CIRCLE两个真实捕捉的基准数据集上，DiMoP3D在所有主要指标上大幅超越现有方法，尤其在物理一致性指标ACPD上实现了超过10 cm的显著提升（Table 1），验证了场景引导多样性这一核心思路的有效性。

## 核心方法与创新机理

DiMoP3D 的核心创新在于首次将 **3D 场景的确定性约束**（物理避碰、语义合理的交互）系统地引入多样化人体运动预测框架，解决了现有方法因完全忽略场景而导致的穿透、不连贯等严重伪影问题。其关键突破体现在三个维度的“changed slots”上。

### 从无场景到场景感知的输入范式转变

现有多样化 HMP 基线（如 **DLow**、**SmoothDMP**、**BeLFusion**）仅以过去人体姿态作为输入，完全无视 3D 场景的存在。DiMoP3D 将输入模态扩展为双通道：**过去运动序列**与 **3D 场景点云**（Figure 2）。这一转变使模型首次具备了对物理障碍物和语义交互对象的感知能力，为后续的约束引导生成奠定了基础。

### 从无条件随机采样到场景引导的可控多样性

传统方法通过无条件随机潜在变量或纯随机丢弃策略产生多样性，其生成的运动方向、交互目标与场景元素之间缺乏任何因果关联。DiMoP3D 通过跨模态兴趣分析机制实现了多样性的**语义锚定**：

- **跨模态兴趣图**：场景-运动跨模态兴趣网络（InterestNet）联合编码点云特征与过去运动，预测点级兴趣图 $M$，识别人类可能交互的场景区域（Figure 6）。
- **目标采样**：对兴趣图按物体实例聚合分数后，通过温度 $\phi=0.5$ 的 Softmax 进行随机采样，选择交互目标物体 $O_g$。该过程将无约束的随机性转化为由场景语义引导的**可解释随机性**——不同采样结果对应不同的合理交互意图。

### 从隐式约束学习到显式物理与语义一致性编码

这是 DiMoP3D 最具区分度的创新。现有方法依赖损失函数隐式地学习物理合理性，在复杂 3D 场景中几乎失效（BeLFusion 的 ACPD 高达 13.73 cm）。DiMoP3D 将物理与语义约束**显式编码为条件因子**，并在生成过程中强制执行：

- **行为一致性随机规划器**：利用场景高度图 $\mathcal{S}_H$ 和改进的 A* 算法生成朝向交互目标的**无碰轨迹** $\tau^{plan}$；HOI-Estimator 根据目标物体几何预测交互终态 $\hat{x}_{end}$。二者与到达时间戳组合为随机条件因子 $\theta = (\hat{\tau}^{plan}, \hat{x}_{end}, t_{end})$，桥接规划与生成。
- **扩散去噪的先验覆盖机制**：在扩散模型的每一步去噪中，将预测帧的全局平移显式替换为规划轨迹点，并在终态帧替换为预测的交互姿态（Eq. 11）。这一设计确保无论随机噪声如何扰动，生成的运动始终满足**障碍物避碰**与**交互终态一致性**。
- **语义对齐监督**：引入 MotionCLIP 语义对齐损失 $\mathcal{L}_{sem}$，计算生成运动与目标物体交互描述的余弦距离，并对后期帧加权，强化运动与场景的语义匹配度。

### 创新效果的实证验证

上述创新带来的性能提升是系统性的。在 GIMO 和 CIRCLE 两个真实捕捉基准上，DiMoP3D 在所有主要指标上均大幅超越已有方法（Table 1）。最具说服力的是物理一致性指标 ACPD：从 BeLFusion 的 13.73 cm 降至 **0.98 cm**，降幅超过 12 cm，证明显式约束机制从根本上解决了穿透问题。消融实验进一步确认了各创新模块的独立贡献：移除轨迹规划器使 ACPD 飙升至 3.29 cm，移除 HOI-Estimator 使 ACPD 升至 1.53 cm，移除兴趣网络导致 ADE 从 5.66 恶化至 6.17（Table 2）。定性对比（Figure 3）直观展示了 DiMoP3D 如何避免 BeLFusion 中出现的物体穿透、运动不连贯和场景不一致等典型失败模式。

DiMoP3D 的总体目标是将多样化人体运动预测从无约束的随机生成转化为**场景确定元素引导的可控随机生成**。其核心洞察在于：真实世界中的人类运动同时受制于物理约束（避碰）和语义约束（与场景物体合理交互），因此不能简单地将多样性建模为无条件随机潜在变量，而需要从场景中提取确定性条件因子来约束生成过程。

### 双模态输入与任务概率建模

DiMoP3D 接收两类输入：**过去人体运动序列** $X_{1:L}$ 和 **3D 场景点云** $S$。任务被建模为一个条件概率框架：

$$P(\hat{X}_{L:L+\Delta L} | X_{1:L}, S) = \int \max_{\theta} P(\hat{X}_{L:L+\Delta L} | X_{1:L}, S, \theta) P(\theta | X_{1:L}, S) d\theta$$

其中 $\theta$ 是从过去运动和场景中采样的**随机条件因子**（stochastic conditional factor），它桥接了场景的确定性约束与运动生成的随机多样性。这一公式的关键在于：多样性来源于 $\theta$ 的随机采样过程，而物理和语义一致性则由 $\theta$ 所编码的规划轨迹、交互终态和到达时间戳来保证。

### 三阶段级联架构

DiMoP3D 由三个顺序级联的模块组成，形成“理解场景→规划行为→生成运动”的完整流水线（Figure 2）：

![[assets/figures/papers/paper_list_l1790_DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diver/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of DiMoP3D. DiMoP3D incorporates two modalities of input, the past motion and the 3D scene point cloud. Initially, the Context-aware Intermodal Interpreter encodes the point cloud to features*

1. **上下文感知的跨模态解释器（Context-aware Intermodal Interpreter）**  
   该模块负责从场景点云中提取语义和几何信息。它采用类 UNet 的编码器-解码器架构，共享编码器将点云 $S$ 压缩为紧凑特征 $\mathcal{F}_s$，随后分两个解码分支：实例分割器识别交互物体集合 $\mathbb{O}$，兴趣网络（InterestNet）通过跨模态注意力机制生成点级兴趣图 $M$，定位人体可能交互的目标区域。最终通过带温度系数 $\phi=0.5$ 的 Softmax 从候选物体中采样交互目标 $O_g$。

2. **行为一致的随机规划器（Behaviorally-consistent Stochastic Planner）**  
   规划器将交互意图转化为可执行的运动约束。它首先利用场景高度图 $\mathcal{S}_H$ 和改进的 A* 算法生成朝向目标的避碰轨迹 $\tau^{plan}$，随后通过单层 Transformer 对轨迹进行离散化采样，得到逐帧全局平移序列 $\hat{\tau}^{plan}$ 和到达时间戳 $t_{end}$。同时，HOI 估计器从目标物体几何 $O_g$ 预测交互终态 $\hat{x}_{end}$。三者组合构成条件因子：

   $$\theta = (\hat{\tau}^{plan}, \hat{x}_{end}, t_{end})$$

3. **自提示运动生成器（Self-prompted Motion Generator）**  
   以条件因子 $\theta$ 为提示，扩散模型在去噪过程中生成多样化运动。关键在于**去噪先验覆盖机制**：在扩散去噪的每一步，将预测帧的全局平移替换为规划轨迹 $\hat{t}_i^{plan}$，将终态帧替换为预测交互终态 $\hat{x}_{L+\Delta L}$，从而显式强制物理一致性：

   $$\bar{x}_i^0 = \begin{cases} x_i^0 & i\le L \\ (\hat{t}_i^{plan}, \bar{o}_i^0, \bar{p}_i^0) & L<i<L+t_{end} \\ \hat{x}_{L+\Delta L} & i = L+t_{end} \end{cases}$$

   此外，引入 MotionCLIP 语义对齐损失 $\mathcal{L}_{sem}$，通过计算生成运动与目标物体交互描述的余弦距离，并加权后期帧来强化语义一致性。

### 设计逻辑：从无约束随机到场景引导的随机

传统多样化 HMP 方法（如 **DLow**、**SmoothDMP**、**BeLFusion**）将多样性完全交由无条件随机潜在变量或随机丢弃机制，缺乏对场景约束的显式建模，导致在真实 3D 场景中出现物体穿透、运动不连贯和场景不一致等问题（Figure 1, Figure 3）。DiMoP3D 的核心创新在于将**场景的确定性元素**（可交互物体、可行走区域、交互终态）显式编码为条件因子，使扩散模型的随机采样始终在物理和语义可行的流形上进行，从而在保持多样性的同时消除伪影。消融实验验证了这一设计的必要性：移除轨迹规划器后，物理一致性指标 ACPD 从 0.98 急剧恶化至 3.29；移除兴趣网络后，精度指标 ADE 从 5.66 升至 6.17（Table 2）。

### 3.1 问题形式化：从无条件随机到场景条件随机

DiMoP3D 将场景感知的多样化人体运动预测建模为一个条件生成过程，其核心概率形式为：

$$P(\hat{X}_{L:L+\Delta L} | X_{1:L}, S) = \int \max_{\theta} P(\hat{X}_{L:L+\Delta L} | X_{1:L}, S, \theta) P(\theta | X_{1:L}, S) d\theta$$

其中 $X_{1:L}$ 为观测到的过去 $L$ 帧人体运动序列，$S$ 为 3D 场景点云，$\hat{X}_{L:L+\Delta L}$ 为预测的未来 $\Delta L$ 帧运动。关键创新在于引入随机条件因子 $\theta$——它不是无约束的噪声变量，而是从过去运动和场景中采样得到的、承载确定性物理与语义约束的结构化因子。这一形式化将“无约束随机采样”转化为“由场景确定元素引导的可控随机生成”，从根本上解决了现有方法忽略场景约束导致的穿透与不连贯问题。

### 3.2 上下文感知的跨模态解释器

该模块负责从场景点云中提取几何与语义信息，并识别人类的潜在交互目标。其处理流程如下：

**场景编码与实例分割**：采用类 UNet 的编码器-解码器架构处理点云。共享编码器将点云 $S$ 压缩为紧凑特征 $\mathcal{F}_s \in \mathbb{R}^{n_p' \times c}$，随后实例分割解码器输出物体识别结果 $\mathbb{O}$。

**跨模态兴趣图预测**：兴趣网络（InterestNet）以场景特征 $\mathcal{F}_s$ 和过去运动 $X_{1:L}$ 为输入，预测逐点兴趣图 $M$——红色高亮区域表示人类可能交互的位置，蓝色表示低兴趣区域（如 Figure 6 所示）。这一跨模态注意力机制使模型能够理解“门在身后不太可能是目标”这类场景语义。

**交互目标采样**：对每个识别出的物体 $O_i$，聚合其覆盖点上的兴趣分数：

$$M_i = \sum M[p] / \text{len}(O_i)$$

随后通过带温度参数 $\phi=0.5$ 的 Softmax 进行概率化采样：

$$P_i = \text{Softmax}(M_i; \phi)$$

温度参数控制采样的随机程度，在多样性与合理性之间取得平衡。采样得到的 $O_g$ 即为选定的交互目标物体。

### 3.3 行为一致的随机规划器

该模块将高层交互意图转化为可执行的物理约束，生成两个关键条件元素：无碰轨迹和交互终态。

**障碍物避碰轨迹规划**：利用场景高度图 $\mathcal{S}_H$ 和改进的 A* 算法，生成从当前位置到目标物体的无碰路径：

$$\tau^{plan} = A^*(\mathcal{S}_H; X_{1:L}, \hat{x}_{end})$$

其中 $\hat{x}_{end}$ 为预测的交互终态位置。随后通过单层 Transformer $\psi$ 对规划路径进行离散采样，预测每帧的人体全局平移速度，得到逐帧轨迹点序列：

$$\hat{\tau}^{plan} = \{\hat{t}_{L+1}^{plan}, \hat{t}_{L+2}^{plan}, ..., \hat{t}_{L+\Delta L}^{plan}\}$$

**交互终态预测**：HOI-Estimator 以目标物体点云 $O_g$ 为输入，预测人体与物体交互的最终姿态：

$$\hat{x}_{end} = \text{HOI-Estimator}(O_g)$$

如 Figure 4 所示，该模块能为同一物体生成多样化的合理交互姿态。

![[assets/figures/papers/paper_list_l1790_DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diver/figures/006_Figure_4.jpg]]
*Figure 4: Visualizations of diverse predicted end-poses across five object point clouds. The HOI-Estimator can generate a variety of human-object interactive poses tailored to specific scenarios*

**随机条件因子组装**：将规划轨迹、预测终态和到达时间戳组合为结构化条件因子：

$$\theta = (\hat{\tau}^{plan}, \hat{x}_{end}, t_{end})$$

该因子桥接了确定性规划与随机生成，使后续扩散模型在受控空间内进行多样化采样。

### 3.4 自提示运动生成器

该模块以条件因子 $\theta$ 为提示，通过扩散模型生成多样化且物理一致的运动序列。其核心机制是在去噪过程的每一步进行显式先验覆盖：

$$\bar{x}_i^0 = \begin{cases} x_i^0 & i \le L \\ (\hat{t}_i^{plan}, \bar{o}_i^0, \bar{p}_i^0) & L < i < L + t_{end} \\ \hat{x}_{L+\Delta L} & i = L + t_{end} \end{cases}$$

这一覆盖策略的含义是：对于观测帧（$i \le L$），保持原始运动不变；对于预测中间帧（$L < i < L + t_{end}$），将全局平移替换为规划轨迹点，确保路径无碰；对于终态帧（$i = L + t_{end}$），替换为 HOI-Estimator 预测的交互姿态，确保交互一致性。通过这种方式，扩散模型的随机去噪过程始终被物理约束“锚定”，实现了随机多样性与确定性的统一。

**语义对齐损失**：为进一步强化运动与场景的语义一致性，引入 MotionCLIP 语义损失：

$$\mathcal{L}_{sem} = \frac{1}{L+\Delta L} \sum_{l=1}^{L+\Delta L} \big(1 - \cos(\text{MC}_{Motion}(\hat{X}), \text{MC}_{Text}(\mathbb{D}_g))\big)$$

其中 $\text{MC}_{Motion}$ 和 $\text{MC}_{Text}$ 分别为 MotionCLIP 的运动编码器和文本编码器，$\mathbb{D}_g$ 为目标物体的交互描述模板（如“sit on the chair”）。该损失对后期帧赋予更高权重，使生成的运动在语义层面与交互意图对齐。

![[assets/figures/papers/paper_list_l1790_DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diver/figures/012_Figure_6.jpg]]
*Figure 6: Visualization of 3D scene instance segmentation (upper) and the corresponding interest map (lower). Red points in the interest map denote higher interest, while blue points denote lower interest. Leveraging the insight provided by the predicted interest map enables the exclusion of improbable or illogical targets, thereby enhancing the reliability and scene congruency of predictions*

## 实验与关键发现

### 主实验结果

DiMoP3D在GIMO和CIRCLE两个真实捕捉的室内场景基准上进行了全面评估，与多样化人体运动预测基线**DLow**、**SmoothDMP**、**BeLFusion**以及确定性场景感知基线**BiFU**进行了对比。Table 1汇总了核心指标结果。

在GIMO数据集上，DiMoP3D在所有精度指标上均大幅领先。相比此前最强的扩散模型BeLFusion，DiMoP3D将平均位移误差ADE从9.69降至5.66（降幅41.6%），终点位移误差FDE从11.19降至6.81（降幅39.1%）。多样化的MMADE和MMFDE同样显著改善。物理一致性指标ACPD的差距更为悬殊：DiMoP3D仅0.98，而BeLFusion高达13.73——这意味着DiMoP3D的预测运动几乎不发生场景穿透，而基线方法存在严重的物理伪影。同时，DiMoP3D的平均成对距离APD达到48.30，高于BeLFusion的38.04，说明其在保证物理一致性的前提下并未牺牲运动多样性。

在CIRCLE数据集上趋势一致：ADE从7.91降至5.66，ACPD从14.06降至0.98。值得注意的是，确定性方法BiFU虽然精度尚可，但无法产生多样化预测，其APD、MMADE、MMFDE均不适用。

### 消融实验

Table 2系统消融了DiMoP3D的四个核心组件，全部实验在GIMO上进行。

**移除兴趣网络（w/o InterestNet）**：ADE从5.66升至6.17，MMADE从6.57升至7.20。兴趣网络负责从场景点云中识别人类可能交互的物体区域并采样目标；移除后退化为随机目标选择，导致预测精度下降。这验证了跨模态兴趣分析对引导运动生成方向的必要性。

**移除HOI估计器（w/o HOI-Estimator）**：ACPD从0.98升至1.53，FDE和MMADE也同步恶化。HOI估计器根据目标物体几何预测交互终态，为运动生成提供终点约束。缺少这一约束时，模型对交互姿态的预测能力减弱，物理一致性受损。

**移除轨迹规划器（w/o Traj. Planner）**：ACPD急剧升高至3.29，是完整模型的3.4倍。轨迹规划器使用改进的A*算法在场景高度图上生成无碰路径，是保障障碍物避碰的核心机制。其移除直接导致运动穿透场景物体，物理一致性严重退化。

**移除语义对齐检查器（w/o Semantic Inspector）**：ADE和MMADE均有所上升。该组件利用MotionCLIP计算生成运动与目标物体交互描述的语义对齐损失，其移除削弱了运动与场景语义的匹配度。

### 定性对比与失败模式分析

Figure 3展示了DiMoP3D与BeLFusion在卧室和研讨室场景中的可视化对比。BeLFusion的预测暴露出三类典型失败模式：**物体穿透**（红色框标注，人体网格穿入家具内部）、**运动不连贯**（绿色框标注，姿态序列出现突变或不自然过渡）、**场景不一致**（黄色框标注，运动方向或交互方式与场景布局矛盾）。DiMoP3D在相同场景下生成的多样化运动则避免了这些问题，运动轨迹自然贴合场景几何，交互姿态与目标物体语义匹配。

Figure 4进一步可视化了HOI估计器针对五种不同物体点云生成的多样化交互终态，表明模型能够为同一物体产生多种合理的交互姿势（如坐、靠、触碰等），这是实现物理一致且多样化预测的关键。

### 场景特征附加实验

Table 5报告了一个重要的对照实验：将场景点云特征直接附加到基线方法（DLow、SmoothDMP、BeLFusion）的输入中。结果显示，简单附加场景信息对基线方法的提升极为有限，甚至在某些指标上出现倒退。这证明DiMoP3D的性能优势并非仅仅来自使用了场景信息，而是源于其系统性的场景-运动跨模态协调机制——兴趣分析、轨迹规划、终态预测与先验覆盖的协同作用。

### 组件鲁棒性分析

Table 6测试了不同场景分割器（PointGroup、HAIS、SoftGroup、Mask3D）对DiMoP3D性能的影响。随着分割器mAP50从71.6提升至76.8，模型各项指标呈现改善趋势，但整体波动不大，说明DiMoP3D对分割精度具有一定鲁棒性。

Table 7对比了不同轨迹规划器（直线插值、RRT、A*）的效果。A*规划器在ACPD上表现最优（0.98），RRT次之（1.13），直线插值最差（1.42），验证了基于图搜索的全局最优路径规划对物理一致性的重要性。

### 局限性

尽管DiMoP3D取得了显著提升，其设计仍存在若干约束。方法假设预测序列长度为固定的5秒，无法处理可变长度运动预测。轨迹规划基于静态场景高度图，未建模动态障碍物（如移动的行人）。语义理解依赖预定义的物体类别和交互模板，对未知物体的泛化能力有限。扩散模型的迭代去噪过程带来较高计算开销，可能影响实时应用。此外，实验仅在两个室内数据集上进行，户外或高度动态环境中的性能尚待验证。

![[assets/figures/papers/paper_list_l1790_DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diver/figures/003_Table_1.jpg]]
*Table 1: Comparison of DiMoP3D with baselines on GIMO [88] and CIRCLE [4] datasets. The best outcomes are highlighted in bold. Given that BiFU [88] employs a deterministic prediction approach, diversity metrics such as APD, MMADE, and MMFDE are not applicable*

![[assets/figures/papers/paper_list_l1790_DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diver/figures/004_Table_2.jpg]]
*Table 2: Ablation of four main components in DiMoP3D over the sequences of the GIMO [88]*

![[assets/figures/papers/paper_list_l1790_DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diver/figures/005_Figure_3.jpg]]
*Figure 3: Visual comparisons between DiMoP3D and SoTA BeLFusion in bedroom and seminar room scenarios. BeLFusion’s predictions, which rely solely on past human motion without considering 3D scene context, are shown on the left. In contrast, DiMoP3D, displayed on the right, incorporates interactive goals and designs obstacle-free trajectories for each sequence. Purple meshes depict observed motions, while yellow ones signify predicted future motions. For clarity, distortions in BeLFusion’s predictions are marked: red boxes for object penetration, green boxes for motion incoherence, and yellow boxes for scene inconsistency*

## 定位与知识库关联

### 1. 与现有方法的继承与差异

DiMoP3D 定位于**场景感知的多样化人体运动预测**这一新兴交叉领域，其核心贡献在于首次将3D场景的确定性约束系统性地注入随机生成框架。为理解这一贡献，需将其置于两条原本独立的研究脉络中审视。

#### 1.1 多样化人体运动预测（Diverse HMP）

多样化HMP的目标是从观测运动出发，生成多条物理上合理且彼此不同的未来运动轨迹。代表性工作包括：

- **DLow**（Yuan & Kitani, ECCV 2020）：基于条件变分自编码器（CVAE），通过对潜在空间采样实现多样性。其局限在于潜在变量是无条件的随机噪声，缺乏对场景语义的理解，导致生成的运动在复杂环境中频繁穿透物体。
- **SmoothDMP**（Aliakbarian et al., 2021）：引入平滑性约束的VAE框架，改善了运动质量，但同样未建模场景信息。
- **BeLFusion**（Barquero et al., WACV 2023）：基于扩散模型的SOTA方法，通过行为潜在空间实现多样化生成。然而，其扩散过程的随机性完全不受场景约束，导致在GIMO等场景基准上出现严重的物体穿透（ACPD高达13.73 cm）和运动不连贯。

DiMoP3D 继承了扩散模型在多样性生成上的优势，但**从根本上改变了随机性的来源与控制方式**：将无条件随机采样替换为由场景-运动跨模态兴趣分析驱动的目标采样，使多样性不再是“盲目的随机”，而是“场景引导的可控探索”。

#### 1.2 确定性场景感知人体运动预测

另一条脉络关注如何利用3D场景信息提升预测精度，但通常牺牲了多样性：

- **BiFU**（Zheng et al., CVPR 2022）：在GIMO基准上提出的确定性场景感知方法，将场景点云与运动序列融合，但仅输出单一预测轨迹，无法捕捉人类意图的多模态本质。

DiMoP3D 借鉴了场景编码与语义理解的思想，但**将确定性约束重新定位为随机生成的条件因子**，而非直接输出。这一转变使得物理一致性与多样性不再互斥。

### 2. 关键设计决策的谱系定位

| 设计维度 | 传统多样化HMP | 确定性场景HMP | **DiMoP3D** |
|---------|-------------|-------------|-------------|
| 场景输入 | 无 | 3D点云 | 3D点云 |
| 多样性来源 | 无条件随机噪声 | 无（单输出） | 场景-运动兴趣图引导的目标采样 |
| 物理约束 | 隐式（损失学习） | 隐式 | 显式（A\*轨迹规划 + 去噪先验覆盖） |
| 语义一致性 | 无 | 无 | MotionCLIP对齐损失 + HOI终态预测 |
| 生成框架 | VAE / 扩散 | 回归 / 单步生成 | 条件扩散 |

这一对比揭示了DiMoP3D的方法论定位：**它在扩散生成框架内，将规划（Planning）与预测（Prediction）统一为条件因子**。具体而言，条件因子 $\theta = (\hat{\tau}^{plan}, \hat{x}_{end}, t_{end})$ 桥接了三个原本分离的模块：

1. **兴趣网络（InterestNet）**：将“人想与哪个物体交互”建模为可采样的概率分布（Eq. 3-4），使意图推理成为多样性生成的起点。
2. **A\*轨迹规划器**：将“如何无碰到达目标”转化为显式几何约束（Eq. 5），而非依赖网络隐式学习。
3. **HOI估计器**：将“到达后如何交互”预测为终态姿态（Eq. 7），为扩散去噪提供终点锚定。

在扩散去噪的每一步，观测帧、规划轨迹帧和预测终态帧被显式覆盖到生成运动上（Eq. 11），形成**硬约束先验**。这与BeLFusion等纯生成方法形成鲜明对比——后者仅依赖损失函数的软约束来隐式学习物理规律。

### 3. 适用边界与局限

#### 3.1 已知局限

根据消融实验（Table 2）与论文自述，DiMoP3D存在以下适用边界：

1. **固定预测长度**：当前方法假设预测序列为固定的5秒（30帧），无法处理可变长度运动预测。这在真实应用中限制了灵活性——人的交互行为时长天然可变。
2. **封闭词汇的物体理解**：兴趣网络和HOI估计器依赖ScanNet数据集中预定义的18类物体语义模板（Table 4），对训练集未见物体类别或开放场景泛化能力有限。
3. **静态场景假设**：A\*轨迹规划器基于静态场景高度图 $\mathcal{S}_H$ 计算路径，未建模动态障碍物（如移动的行人、被挪动的椅子）。消融实验显示，移除轨迹规划器使ACPD从0.98骤升至3.29，表明物理一致性高度依赖该模块，但该模块本身对动态变化敏感。
4. **计算开销**：扩散模型的迭代去噪过程（通常需1000步）限制了实时性应用。论文未报告推理延迟数据，但这是扩散类方法的共性问题。
5. **数据集覆盖范围**：实验仅在GIMO（室内多房间）和CIRCLE（室内单一场景）两个数据集上进行，户外或高度动态环境（如街道、商场）的性能有待验证。

#### 3.2 隐式假设与潜在风险

- **单交互目标假设**：兴趣网络每次采样一个目标物体 $O_g$，未建模多目标连续交互序列（如先走向桌子再走向门）。在真实场景中，人的意图可能涉及多个物体的顺序交互。
- **点云质量依赖**：场景解释器（UNet-like encoder-decoder）和实例分割器的性能直接影响下游模块。Table 6显示，使用不同分割器时mAP50从0.45到0.62变化，但论文未报告分割失败时的退化程度。
- **MotionCLIP的语义局限**：语义对齐损失依赖MotionCLIP的文本-运动编码空间，但该空间的语义粒度可能不足以区分精细交互（如“坐下”vs“靠在椅子上”）。

### 4. 开放问题与后续方向

DiMoP3D 开启了一条将规划与生成统一的研究路径，其未解决的问题指向若干值得探索的方向：

1. **端到端的可变长度预测**：能否让模型自适应地决定预测序列长度，而非固定5秒？这需要解决扩散模型对固定帧数的结构依赖。
2. **开放词汇的场景理解**：将物体类别的封闭集合拓展到开放词汇（如借助视觉-语言模型），使模型能处理训练中未见的物体，是向真实世界部署的关键一步。
3. **动态场景中的安全规划**：在多运动行人、移动障碍物环境中，如何高效规划并保持物理一致性？这可能需引入动态占用地图或预测他人运动。
4. **轻量化扩散采样**：在保持多样性和物理精度的同时，能否通过蒸馏、一致性模型或减少采样步数来降低计算开销？这是扩散模型走向实时的通用挑战。
5. **第一人称与部分观测**：该方法是否适用于第一人称视角（如AR眼镜）或仅部分观察到场景的活动预测任务？这涉及场景补全与不确定性建模的结合。
6. **多目标序列交互**：将单目标采样扩展为交互序列的层次化规划，使模型能生成“走向桌子→拿起杯子→走向沙发”的连贯行为链。

### 5. 知识库定位总结

DiMoP3D 处于**3D场景理解 × 人体运动预测 × 扩散生成模型**的交汇点。其核心知识贡献在于：

- **方法论层面**：证明了“规划-生成”解耦架构在场景感知运动预测中的有效性，为后续工作提供了模块化设计范式。
- **基准层面**：在GIMO和CIRCLE上建立了新的SOTA，尤其将物理一致性指标ACPD从13.73 cm降至0.98 cm（Table 1），重新定义了该领域的性能上限。
- **概念层面**：将“随机性与确定性的调和”明确为场景感知HMP的核心问题，并通过显式先验覆盖机制给出了一个可操作的解决方案。

后续工作可在其模块化架构的基础上，逐步替换封闭词汇为开放语义、静态规划为动态规划、固定长度为自适应长度，从而推动该领域向更真实、更灵活的应用场景演进。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/DiMoP3D_Harmonizing_Stochasticity_and_Determinism_Scene_responsive_Diverse_Human_Motion_Prediction.pdf]]

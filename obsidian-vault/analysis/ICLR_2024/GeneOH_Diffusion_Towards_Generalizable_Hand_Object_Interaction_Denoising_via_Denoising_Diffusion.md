---
title: "GeneOH Diffusion: Towards Generalizable Hand-Object Interaction Denoising via Denoising Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising_via_Denoising_Diffusion.pdf
code_link: null
project_link: https://meowuu7.github.io/GeneOH-Diffusion
aliases:
- GD
- GDTGHOIDDD
tags:
- ICLR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 以广义接触点为中心的正则化HOI表示（GeneOH）与基于扩散的域泛化去噪策略（‘先扩散至白化噪声空间再投影至数据流形’）。
primary_logic: 将交互过程分解为接触中心的正则化空间-时序关系，并采用渐进式扩散去噪范式，可以同时解耦复杂噪声并实现跨物体、跨交互和跨噪声模式的强泛化。
claims:
- 在GRAB测试集上，我们的方法在MPJPE上达到9.28 mm，比TOCH基线（12.38 mm）降低25%，同时穿透深度和运动一致性指标也显著优于所有基线。
- 在未见噪声分布（Beta噪声）的GRAB (Beta)测试集上，我们的C-IoU达到26.76%，而TOCH（含数据增强）仅为24.81%，表明扩散策略有效处理分布外噪声。
- 移除接触中心正则化（Ours w/o Canon.）导致HO Motion Consistency从0.41升至13.26 mm²，证明正则化对泛化至关重要。
- GRAB (合成高斯噪声) 上 MPJPE↓ (mm) = 9.28
---

# GeneOH Diffusion: Towards Generalizable Hand-Object Interaction Denoising via Denoising Diffusion

> [!tip] 核心洞察
> 将交互过程分解为接触中心的正则化空间-时序关系，并采用渐进式扩散去噪范式，可以同时解耦复杂噪声并实现跨物体、跨交互和跨噪声模式的强泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeneOH Diffusion：通过去噪扩散实现可泛化的手物交互去噪 |
| 英文题名 | GeneOH Diffusion: Towards Generalizable Hand-Object Interaction Denoising via Denoising Diffusion |
| 会议/期刊 | ICLR 2024 |
| Links |  [Project](https://meowuu7.github.io/GeneOH-Diffusion)|
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GeneOH Diffusion |
| Dataset | GRAB, HOI4D, ARCTIC |

> [!tip] 效果简介
> - GRAB (合成高斯噪声) 上，MPJPE↓ (mm) 9.28 vs 12.38 (TOCH) (-3.10 mm)。
> - HOI4D (真实噪声) 上，Penetration Depth↓ (mm) 3.45 vs 4.48 (输入) (-1.03 mm)。
> - ARCTIC (双手动态交互) 上，MPJPE↓ (mm) 11.57 vs 22.79 (TOCH w/MixStyle) (-11.22 mm)。

## 概要

手物交互（HOI）去噪面临一个核心瓶颈：真实世界的交互噪声高度复杂，涵盖非自然手部姿态、错误的空间关系（如穿透）和不一致的时序运动，且噪声分布与训练数据之间存在严重的分布漂移。现有数据驱动模型（如TOCH）倾向于过拟合训练集中的特定噪声模式，难以泛化到新物体、新手部运动乃至未见过的噪声类型。

针对这一挑战，**GeneOH Diffusion** 提出了两项关键设计：
1. **接触中心的正则化HOI表示（GeneOH）**：将交互过程分解为以广义接触点为中心的正则化手部轨迹、手-物空间关系和手-物时序关系三部分，通过将空间-时序关系统一转换到接触点坐标系，解耦物体形状与交互模式，从而增强跨物体的泛化能力。
2. **基于扩散的域泛化去噪策略**：采用“先扩散至白化噪声空间，再逐步投影回干净数据流形”的范式。具体而言，规范去噪器（canonical denoiser）仅在白化噪声空间中学习从噪声到干净数据的映射，推理时通过控制扩散步数将任意噪声输入扩散到该空间，再由同一去噪器进行三步渐进式去噪（MotionDiff → SpatialDiff → TemporalDiff），最终通过MANO拟合恢复参数化手部网格序列。

核心洞察在于：将复杂交互噪声解耦为正则化空间-时序关系的扰动，并借助扩散过程的域泛化特性，使模型能够处理训练中未曾出现的噪声分布和交互场景。

**主要结果**（详见Table 1）：
- 在GRAB测试集（合成高斯噪声）上，MPJPE达到9.28 mm，比TOCH基线（12.38 mm）降低25%，穿透深度和运动一致性指标亦显著领先。
- 在HOI4D真实噪声数据上，穿透深度从输入的4.48 mm降至3.45 mm，展现出对真实噪声的有效清洗。
- 在ARCTIC双手动态交互数据集上，MPJPE仅为11.57 mm，而TOCH（含MixStyle增强）为22.79 mm，跨场景泛化优势明显。
- 消融实验（Table 2）证实：移除接触中心正则化导致运动一致性从0.41退化至13.26；将扩散去噪替换为自编码器则使穿透深度从1.74 mm增至3.83 mm，验证了扩散策略与正则化表示的关键作用。

**方法定位**：GeneOH Diffusion属于手物交互去噪领域，其接触中心正则化表示继承了基于接触点建模的思路，但通过引入扩散去噪范式，将传统自编码器式的“噪声→干净”直接映射转变为“扩散至白化空间→规范去噪→逐步投影”的域泛化策略，从而在跨物体、跨噪声模式和跨交互类型的泛化能力上取得突破。



### 手物交互去噪的核心挑战

手物交互（Hand-Object Interaction, HOI）轨迹的获取与精化是计算机视觉和机器人领域的核心问题。从视频估计、运动捕捉或遥操作中获得的交互序列常包含三类复杂噪声：（1）**非自然手部姿态**，如手指穿透物体；（2）**错误的空间关系**，如手与物体的相对位置偏移；（3）**不一致的时序关系**，如运动抖动或速度突变。这些噪声往往同时出现且相互耦合，使得去噪问题高度复杂。

更关键的是，真实场景中的噪声分布与训练数据存在严重的**分布漂移**（domain shift）。现有数据驱动模型（如基于自编码器的TOCH）倾向于过拟合训练集中的特定噪声模式，在面对新物体、新手势或未见噪声类型时泛化能力急剧下降。这一瓶颈从根本上制约了HOI去噪技术在实际应用中的可靠性。

### 现有方法的局限性

以**TOCH**（Zhou et al., 2022）为代表的现有方法采用非正则化的空间关系表示，直接学习从噪声到干净轨迹的映射。该方法存在三个结构性缺陷：

- **表示层面**：未显式建模手物之间的时序关系，且空间关系缺乏以接触为中心的规范化，导致模型难以捕捉交互的本质规律。
- **泛化层面**：自编码器结构在训练噪声分布与测试噪声分布不一致时性能显著退化。即使引入MixStyle域泛化技术或数据增强（TOCH w/ MixStyle, TOCH w/ Aug.），对分布外噪声的处理能力仍然有限。
- **架构层面**：模式特定的单步去噪无法应对多种噪声类型共存的复杂场景。

### 本文动机与核心思路

针对上述挑战，GeneOH Diffusion提出两条核心设计思路：

1. **接触中心的正则化HOI表示（GeneOH）**：将交互过程分解为以广义接触点为中心的手部轨迹、空间关系与时序关系三个分量。通过接触点的6D姿态将所有关系转换至统一坐标系，消除物体形状和位姿变化带来的干扰，使模型聚焦于交互本身的规律。

2. **基于扩散的域泛化去噪策略**：不同于直接学习噪声到干净的映射，该策略采用“先扩散至白化噪声空间，再逐步投影到数据流形”的范式。规范去噪器（canonical denoiser）仅在白化噪声空间训练，通过控制扩散步数的超参数平衡保真度与泛化性，从而实现对未见噪声分布的有效处理。

这种“解耦表示 + 渐进扩散”的组合使模型在仅使用GRAB合成噪声数据训练的情况下，能够泛化到HOI4D真实噪声、ARCTIC双手交互等分布差异显著的场景，为HOI去噪的实用化提供了新路径。



## 核心方法与创新机理

GeneOH Diffusion 的核心创新围绕两个紧密耦合的设计展开：**以广义接触点为中心的正则化 HOI 表示（GeneOH）**，以及**基于扩散的域泛化去噪范式**。二者协同解决了手物交互去噪中“复杂噪声解耦”与“跨域分布漂移”的双重瓶颈。

### 1. 从非正则化关系到接触中心正则化表示（GeneOH）

现有方法（如 **TOCH**，Zhou et al., 2022）采用非正则化的空间关系表示，缺乏对时序动态和手部形状的显式建模，导致模型易过拟合训练交互中的特定物体-手姿配对模式，跨物体泛化能力薄弱。

GeneOH 的突破在于将交互过程分解为三个正则化组件（Figure 2）：

- **正则化手部轨迹** $\bar{\mathcal{T}}$：以广义接触点（物体表面距手部轨迹 ≤ 5mm 的点）的 6D 姿态为中心，将手部关键点平移并旋转至统一坐标系：
  $$\bar{\mathcal{T}} = \{ \bar{\mathbf{J}}_k = (\mathbf{J}_k - \mathbf{t}_k) \mathbf{R}_k^T \}_{k=1}^{K}$$
  这一操作消除了不同物体姿态带来的坐标系差异，使模型学习的是“相对于接触区域的手部运动模式”，而非绝对空间位置。

- **正则化空间关系** $\mathcal{S}$：编码物体表面点法向量及手部关键点相对偏移，显式暴露穿透等非自然空间关系。

- **时序关系** $\mathcal{T}$：编码物体速度、手物距离、相对速度及其正则化分量，揭示运动不一致性等时序错误。

消融实验直接验证了这一设计的因果作用：**移除接触中心正则化（Ours w/o Canon.）后，HO Motion Consistency 从 0.41 急剧退化至 13.26**（Table 2），表明正则化是泛化能力的决定性因素。

### 2. 从模式特定去噪到“通过扩散去噪”的域泛化策略

传统方法（如 TOCH 的自编码器架构）直接学习“噪声→干净”的确定性映射，当测试噪声分布与训练集不同时性能急剧下降。GeneOH Diffusion 提出了一种全新的去噪范式（Figure 3 右侧）：

- **训练阶段**：训练一个**规范去噪器**（canonical denoiser），学习将**白化噪声空间**中的样本投影回干净数据流形。该去噪器仅见过标准高斯噪声，不依赖任何特定噪声模式。

- **推理阶段**：采用“**去噪即扩散**”（denoising via diffusion）策略——先将含噪输入通过前向扩散过程推向白化噪声空间：
  $$x_t = \sqrt{\bar{\alpha}_t} x + \sqrt{1 - \bar{\alpha}_t} \mathbf{n}$$
  再从该中间状态出发，由规范去噪器逐步采样逆过程恢复干净输出。通过引入超参数控制扩散步数，可平衡去噪强度与对原始输入的保真度。

这一策略的关键洞察在于：**无论原始噪声分布如何，经过充分扩散后都趋近于白化噪声，规范去噪器因而能处理任意未见噪声模式**。定量证据支持这一主张：在未见噪声分布（Beta 噪声）的 GRAB (Beta) 测试集上，GeneOH Diffusion 的 C-IoU 达到 26.76%，优于采用数据增强的 TOCH（24.81%）（Table 4，附录）。消融实验中，**将扩散去噪器替换为自编码器（Ours w/o Diffusion）导致穿透深度从 1.74 mm 升至 3.83 mm**（Table 2），证实扩散策略对去噪质量的关键贡献。

### 3. 渐进式三阶段去噪架构

与单一阶段处理所有噪声不同，GeneOH Diffusion 采用**顺序解耦**策略（Figure 3），三个阶段各专注清理 GeneOH 的一个组件：

1. **MotionDiff**：去噪正则化手部轨迹，修复手部姿态的自然性。
2. **SpatialDiff**：去噪空间关系，消除穿透等空间错误。
3. **TemporalDiff**：去噪时序关系，修复运动不一致性。

这一设计的合理性在于：前一阶段的输出为后一阶段提供了更干净的输入基础，且各阶段不会破坏前序阶段已达到的自然性（附录 A.2 给出证明）。消融实验显示，**移除 TemporalDiff 导致运动一致性从 0.41 恶化至 34.25**（Table 2），验证了时序去噪的独立贡献。

### 创新总结

| 创新维度 | 基线方法（TOCH） | GeneOH Diffusion | 因果证据 |
|---------|----------------|-----------------|---------|
| HOI 表示 | 非正则化空间关系 | 接触中心正则化三组件（GeneOH） | 移除正则化 → 运动一致性退化 32 倍 |
| 去噪范式 | 自编码器直接映射 | 扩散至白化噪声空间 + 规范去噪器投影 | 替换为自编码器 → 穿透深度增加 120% |
| 噪声处理 | 单阶段处理所有噪声 | 渐进式三阶段解耦去噪 | 移除时序阶段 → 运动一致性退化 83 倍 |

**需手动验证的点**：关于“各阶段不会破坏前序阶段自然性”的数学证明位于附录 A.2，当前分析未包含该部分的具体推导，建议在撰写时确认其严谨性。



GeneOH Diffusion 的整体框架围绕两个核心设计展开：**GeneOH 表示**与**基于扩散的域泛化去噪范式**。给定一段带噪手物交互序列 $(\hat{\mathcal{H}}, \mathbf{O}) = \{ (\hat{\mathbf{H}}_k, \mathbf{O}_k) \}_{k=1}^{K}$（其中物体姿态 $\mathbf{O}_k$ 假设精确，手部轨迹 $\hat{\mathbf{H}}_k$ 含噪），方法通过三个渐进阶段依次清洗手部轨迹、空间关系与时序关系，最终输出干净的手部网格序列。

**输入与表示构建**  
输入首先被转换为 GeneOH 表示，该表示以广义接触点为中心进行正则化。具体而言，从物体表面采样与手部轨迹距离不超过 5 mm 的点作为广义接触点，并基于其 6D 姿态将所有关系转换至统一坐标系。GeneOH 由三部分组成（Figure 2）：
- **正则化手部轨迹** $\bar{\mathcal{T}}$：将手部关键点相对接触中心平移并旋转至规范坐标系，公式为 $\bar{\mathcal{T}} = \{ \bar{\mathbf{J}}_k = (\mathbf{J}_k - \mathbf{t}_k) \mathbf{R}_k^T \}_{k=1}^{K^\circ}$。
- **空间关系** $\mathcal{S}$：编码物体点位置、法向量及手-物相对偏移，用于暴露穿透等非自然空间关系。
- **时序关系** $\mathcal{T}$：编码物体速度、手物距离、相对速度及其正则化分量，揭示运动不一致性等时序错误。

**渐进式去噪流水线**  
去噪过程分为三个阶段（Figure 3），每个阶段专注于清洗 GeneOH 的一个组件，且后续阶段不会破坏前一阶段已恢复的自然性：
1. **MotionDiff**：对正则化手部轨迹 $\bar{\mathcal{T}}$ 进行扩散去噪，修复手部整体运动。
2. **SpatialDiff**：对空间关系 $\mathcal{S}$ 进行扩散去噪，消除穿透等空间噪声。去噪后的手部轨迹通过平均各接触点的手-物偏移量恢复：$\mathcal{T}^{\mathrm{stage}_2} = \operatorname{Average}\{ (\mathbf{h}_k - \mathbf{o}_k) + \mathbf{o}_k \mid \mathbf{o}_k \in \mathbf{P}_k \}$。
3. **TemporalDiff**：对时序关系 $\mathcal{T}$ 进行扩散去噪，修复运动不一致性。

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/003_Figure_3.jpg]]
*Figure 3: The progressive HOI denoosing gradually cleans the input noisy trajectory through three stages. Each stage concentrates on refining the trajectory by denoising a specific part of GeneOH via a canonical denoiser through the “denoising via diffusion” strategy*

**扩散去噪策略**  
每个阶段采用统一的“通过扩散去噪”策略：先将含噪的 GeneOH 分量前向扩散至白化噪声空间（$x_t = \sqrt{\bar{\alpha}_t} x + \sqrt{1 - \bar{\alpha}_t} \mathbf{n}$），再由规范去噪器通过后验采样逐步投影回干净数据流形（$\tilde{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} (\tilde{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(\tilde{x}_t, t)) + \sigma_t \mathbf{z}$）。扩散步数由超参数 $t_{\text{diff}}$ 控制，以平衡泛化性与对输入的忠实度。

**输出**  
三阶段去噪完成后，通过 MANO 拟合将去噪后的轨迹转换为参数化手部网格序列，得到最终干净交互结果。

整个流水线的关键因果机制在于：接触中心正则化消除了不同交互序列间的分布差异，使规范去噪器能在有限训练数据上学习通用去噪能力；而渐进式扩散策略则将复杂噪声解耦至三个相对独立的子空间分别处理，从而实现对跨物体、跨交互和跨噪声模式的强泛化。消融实验证实，移除接触中心正则化（Ours w/o Canon.）会导致运动一致性从 0.41 恶化至 13.26，验证了正则化对泛化的核心作用。

### 补充图表

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/001_Figure_1.jpg]]
*Figure 1: Trained only on limited data, GeneOH Diffusion can clean novel noisy interactions with new objects, hand motions, and unseen noise patterns (Fig. (a)), produces diverse refined trajectories with discrete manipulation modes (Fig. (b)), and is a practical tool for many applications (Fig. (c))*



GeneOH Diffusion 的核心由两个关键设计构成：**接触中心的正则化 HOI 表示（GeneOH）** 与 **基于扩散的域泛化去噪范式**。前者将交互过程分解为手部轨迹、空间关系与时序关系三个组件，并通过广义接触点将所有关系转换至统一坐标系；后者采用“先扩散至白化噪声空间，再逐步投影到数据流形”的策略，使模型在仅见有限训练噪声的情况下仍能处理分布外噪声。

### 3.1 GeneOH 表示

给定含噪手物交互序列 $(\hat{\mathcal{H}}, \mathbf{O}) = \{(\hat{\mathbf{H}}_k, \mathbf{O}_k)\}_{k=1}^K$（假设物体姿态 $\mathbf{O}_k$ 精确，手部轨迹 $\hat{\mathbf{H}}_k$ 含噪），GeneOH 首先提取**广义接触点**：从物体表面采样距离手部轨迹不超过阈值 $r_c = 5\text{ mm}$ 的 $N_o$ 个点，记为 $\mathbf{P}_k$。这些接触点构成正则化的空间锚点，其 6D 姿态 $(\mathbf{t}_k, \mathbf{R}_k)$ 用于将所有关系转换至统一坐标系。

GeneOH 包含三个组件（如 Figure 2 所示）：

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/002_Figure_2.jpg]]
*Figure 2: Three components of GeneOH*

**（1）正则化手部轨迹 $\bar{\mathcal{T}}$**

将手部关键点 $\mathbf{J}_k$ 相对接触中心平移并旋转至统一坐标系：

$$\bar{\mathcal{T}} = \{ \bar{\mathbf{J}}_k = (\mathbf{J}_k - \mathbf{t}_k) \mathbf{R}_k^T \}_{k=1}^{K^\circ}$$

其中 $K^\circ$ 为接触帧数。该正则化消除了不同物体姿态和交互位置带来的分布差异，是跨物体泛化的基础。

**（2）正则化空间关系 $\mathcal{S}$**

在每个接触点 $\mathbf{o}_k \in \mathbf{P}_k$ 处编码物体法向与手-物相对偏移：

$$\mathbf{s}_k^{\tilde{\mathbf{o}}} = \big( (\mathbf{o}_k - \mathbf{t}_k) \mathbf{R}_k^T,\; \mathbf{n}_k \bar{\mathbf{R}}_k^T,\; \{ (\mathbf{h}_k - \mathbf{o}_k) \dot{\mathbf{R}}_k^T \mid \mathbf{h}_k \in \cdots \} \big)$$

该表示通过编码物体法向和手部关键点相对接触点的偏移，显式暴露穿透等非自然空间关系。

**（3）时序关系 $\mathcal{T}$**

编码帧间的物体速度、手物距离、相对速度及其正则化分量：

$$\mathcal{T} = \{ \{ \mathbf{v}_k^{\mathbf{o}},\; \{ d_k^{\mathbf{ho}},\; \mathbf{v}_k^{\mathbf{ho}},\; e_{k,\parallel}^{\mathbf{ho}},\; e_{k,\perp}^{\mathbf{ho}} \} \} \}$$

其中 $d_k^{\mathbf{ho}}$ 为手物距离，$\mathbf{v}_k^{\mathbf{ho}}$ 为相对速度，$e_{k,\parallel}^{\mathbf{ho}}$ 和 $e_{k,\perp}^{\mathbf{ho}}$ 分别为相对速度在接触法向的平行与垂直分量。该表示揭示运动不一致性等时序错误。

### 3.2 渐进式去噪范式

去噪分为三个阶段（如 Figure 3 所示），每个阶段针对 GeneOH 的一个组件，采用统一的“通过扩散去噪”策略：

**核心机制：Denoising via Diffusion**

规范去噪模型 $\epsilon_\theta$ 仅在干净数据上训练，学习将白化噪声空间中的样本投影回数据流形。推理时，先将含噪输入沿前向扩散过程加噪至时间步 $t_{\text{diff}}$：

$$x_t = \sqrt{\bar{\alpha}_t} x + \sqrt{1 - \bar{\alpha}_t} \mathbf{n}$$

其中 $\mathbf{n} \sim \mathcal{N}(0, \mathbf{I})$，$\bar{\alpha}_t$ 为累积噪声调度参数。然后从 $t_{\text{diff}}$ 开始逐步执行后验采样去噪：

$$\tilde{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \tilde{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(\tilde{x}_t, t) \right) + \sigma_t \mathbf{z}$$

其中 $\sigma_t$ 控制随机性，$\mathbf{z} \sim \mathcal{N}(0, \mathbf{I})$。超参数 $t_{\text{diff}}$ 控制加噪程度以平衡泛化性与忠实度。

**三阶段流程：**

1. **MotionDiff**：去噪正则化手部轨迹 $\bar{\mathcal{T}}$，输出 $\bar{\mathcal{T}}^{\text{stage}_1}$。
2. **SpatialDiff**：基于 $\bar{\mathcal{T}}^{\text{stage}_1}$ 构建空间关系 $\mathcal{S}$ 并去噪，消除穿透等空间噪声，然后通过平均手部偏移恢复轨迹：
   $$\mathcal{T}^{\text{stage}_2} = \operatorname{Average}\{ (\mathbf{h}_k - \mathbf{o}_k) + \mathbf{o}_k \mid \mathbf{o}_k \in \mathbf{P}_k \}$$
3. **TemporalDiff**：去噪时序关系 $\mathcal{T}$，修复运动不一致性，输出最终正则化轨迹，经 MANO 拟合得到参数化手部网格序列。

消融实验（Table 2）证实：移除正则化（Ours w/o Canon.）使运动一致性从 0.41 恶化至 13.26 mm²；去掉 TemporalDiff 使运动一致性退化至 34.25；将扩散去噪器替换为自编码器（Ours w/o Diffusion）导致穿透深度从 1.74 mm 增至 3.83 mm。这些结果验证了各模块的必要性。



## 实验与关键发现

### 核心实验设计

所有模型均在 **GRAB** 数据集上训练，遵循跨物体划分策略，确保测试物体对训练集不可见。合成噪声的生成参数（平移标准差 0.01、旋转标准差 0.1、姿态标准差 0.5）与真实噪声（如 HOI4D）的分布截然不同，以严格测试模型的跨域泛化能力。评估时从 100 个随机种子生成的样本中选择与输入最接近的轨迹，避免随机性偏差。

### 主结果分析

**Table 1** 汇总了在多个基准上的定量对比，核心发现如下：

**合成噪声（GRAB）**：GeneOH Diffusion 在 MPJPE 上达到 **9.28 mm**，相比 TOCH（12.38 mm）降低约 25%，穿透深度和运动一致性指标同样显著优于所有基线。这表明正则化表示与扩散去噪策略的组合有效恢复了手部姿态精度。

**真实噪声（HOI4D）**：方法将穿透深度从输入的 4.48 mm 降至 **3.45 mm**（Table 1/Table 6），验证了其在真实传感器噪声下的去噪能力。值得注意的是，模型仅在合成噪声上训练，却能在真实噪声分布上实现有效去噪，印证了“先扩散至白化噪声空间再投影至数据流形”策略的泛化优势。

**双手动态交互（ARCTIC）**：MPJPE 达到 **11.57 mm**，而 TOCH（w/ MixStyle）为 22.79 mm，降幅高达 11.22 mm。ARCTIC 涉及双手协同操作，交互模式与 GRAB 的单手抓取差异巨大，该结果强有力地证明了 GeneOH 正则化表示在跨交互类型泛化上的有效性。

**分布外噪声（Beta 噪声）**：在未见噪声分布的 GRAB（Beta）测试集上，C-IoU 达到 **26.76%**，优于 TOCH（含数据增强）的 24.81%（Table 4）。这直接验证了扩散策略处理分布外噪声的独特优势——传统数据增强无法覆盖所有噪声模式，而扩散过程将任意噪声“白化”为统一的高斯噪声空间，使规范去噪器得以处理。

### 消融实验

**Table 2** 在 HOI4D 数据集上揭示了各设计组件的因果贡献：

**接触中心正则化（Ours w/o Canon.）**：移除正则化后，运动一致性（HO Motion Consistency）从 0.41 急剧恶化至 **13.26 mm²**。这证实了以广义接触点为中心的统一坐标系是跨物体泛化的关键——它消除了不同物体几何和姿态带来的表示差异，使去噪器学习到物体无关的“自然交互”模式。

**扩散去噪范式（Ours w/o Diffusion）**：将扩散去噪器替换为自编码器后，穿透深度从 1.74 mm 增至 **3.83 mm**。自编码器直接学习噪声到干净的确定性映射，在训练分布外容易产生过拟合伪影；扩散模型的随机采样过程则提供了更强的分布外鲁棒性。

**时序去噪阶段（Ours w/o TemporalDiff）**：去掉第三阶段后，运动一致性退化至 **34.25 mm²**，验证了时序关系编码对修复运动不一致性（如抖动、速度突变）的不可替代性。三阶段渐进式设计的必要性由此得到证实：MotionDiff 恢复手部姿态，SpatialDiff 消除穿透，TemporalDiff 修复时序连贯性，各阶段互不干扰（附录 A.2 提供了理论证明）。

### 失败模式与局限

尽管整体表现优异，方法存在以下已知局限：

1. **物体姿态假设**：方法假定物体轨迹精确，无法处理物体姿态含噪的情况。在真实场景中，物体跟踪同样存在误差，这限制了方法的端到端应用。
2. **极端几何泛化**：对于极大或极薄的全新物体，去噪效果可能下降（附录失败案例）。正则化策略依赖接触点选取（阈值 5mm），当物体几何与训练集差异过大时，接触点分布可能偏离训练分布。
3. **推理效率**：SpatialDiff 阶段耗时约 **16.6 秒**（Table 8），难以满足实时应用需求。三阶段流程的总推理时间受扩散步数影响，需手工设定步数以平衡质量与速度。

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/029_Table_8.jpg]]
*Table 8: Complexity and running time during the inference time*

### 用户研究

**Table 7** 的用户研究进一步验证了方法的感知质量优势。参与者在自然度、物理合理性等维度上对 GeneOH Diffusion 的去噪结果给予显著偏好，与定量指标的趋势一致。

### 关键图表速览

- **Figure 1**：总览图，展示跨物体/跨噪声泛化、随机去噪产生的多样化轨迹、以及视频估计清洗和重定向轨迹清洗等应用。
- **Figure 4**：定性对比，直观呈现 GeneOH Diffusion 相比 TOCH 在穿透消除和姿态自然度上的优势。
- **Figure 5**：随机去噪可产生离散操作模式（如不同抓取方式）的多样化结果，体现了扩散模型的生成多样性。
- **Figure 6**：应用示例，展示对视频估计手部轨迹和重定向轨迹的清洗效果。
- **Figure 12**：TOCH（w/ MixStyle）在 Beta 噪声下产生怪异伪影，而 GeneOH Diffusion 保持自然，直观展示了扩散策略对分布外噪声的鲁棒性。

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparisons. Please refer to our website and video for animated results*

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/005_Figure_5.jpg]]
*Figure 5: Stochastic denoising can produce divserse results with discrete modes*

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/018_Figure_12.jpg]]
*Figure 12: Weird artifacts produced by TOCH (w/ MixStyle). (First line:) Ours result. (Second line:) The result of TOCH (w/ MixStyle). The noisy input is perturbed by noise sampled from a Beta distribution, different from that used in training*

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/007_Figure_6.jpg]]
*Figure 6: Applications on refining noisy hand trajectories estimated from videos (left) and cleaning retargeted hand trajectories (right)*

### 补充图表

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluations and comparisons to baselines. Bold red numbers for best values and italic blue values for the second best-performed ones. “GT” stands for “Ground-Truth”*

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/008_Table_2.jpg]]
*Table 2: Ablation studies on the HOI4D dataset*

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/028_Table_7.jpg]]
*Table 7: User study*

![[assets/figures/papers/paper_list_l1779_GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising/figures/011_Table_4.jpg]]
*Table 4: Quantitative evaluations and comparisons. Performance comparisons of our method, baselines, and ablated versions on different test sets using the first set of evaluation metrics. Bold red numbers for best values and italic blue values for the second best-performed ones*



## 定位与知识库关联

### 核心定位：从模式特定去噪到域泛化去噪

GeneOH Diffusion 在方法谱系中的根本突破在于**将手物交互去噪从“数据驱动的模式匹配”重新定义为“域泛化的流形投影”**。传统方法（以 TOCH 为代表）的范式是训练一个自编码器直接学习从噪声到干净数据的映射，这导致模型深度耦合训练噪声分布，在未见交互、未见物体或未见噪声模式上泛化能力急剧退化。GeneOH Diffusion 通过两个相互依赖的设计解耦了这一困境：

1. **接触中心的正则化表示（GeneOH）**：将交互过程分解为以广义接触点为中心的手部轨迹、空间关系与时序关系，并通过接触点 6D 姿态将所有关系转换至统一坐标系。这一正则化策略消除了不同物体几何和交互姿态带来的域差异，使去噪器面对的是一个“规范化”的输入空间。
2. **通过扩散去噪（Denoising via Diffusion）**：不直接学习噪声到干净的映射，而是先将噪声输入扩散至一个“白化噪声空间”（whitened noise space），再由规范去噪器从该空间逐步投影回干净数据流形。这一策略的本质是将去噪问题转化为一个**分布鲁棒的逆扩散过程**，天然具备处理分布外噪声的能力。

### 与基线方法的精细对比

**TOCH**（Zhou et al., 2022）是本工作的直接对比基线，其核心差异体现在三个维度：

| 维度 | TOCH | GeneOH Diffusion |
|------|------|------------------|
| HOI 表示 | 非正则化空间关系，未显式建模时序和手部形状 | GeneOH：接触中心正则化的轨迹、空间、时序三部分表示 |
| 去噪范式 | 自编码器直接映射，模式特定 | 扩散模型投影至数据流形，域泛化 |
| 正则化策略 | 无接触中心正则化 | 基于 5mm 距离阈值选取广义接触点，统一坐标系变换 |

实验证据表明，这些设计差异带来了质的性能提升：在 GRAB 测试集上，GeneOH Diffusion 的 MPJPE 达到 9.28 mm，较 TOCH 的 12.38 mm 降低 25%（Table 1）。更关键的是泛化性差异——在未见噪声分布（Beta 噪声）的 GRAB (Beta) 测试集上，GeneOH Diffusion 的 C-IoU 达到 26.76%，而即使经过数据增强的 TOCH (w/ Aug.) 也仅为 24.81%（Table 4，附录），证实扩散策略在分布外噪声处理上的根本优势。

此外，与 TOCH 的增强变体 **TOCH (w/ MixStyle)** 和 **TOCH (w/ Aug.)** 的对比进一步揭示了单纯的数据增强或风格迁移无法弥补表示设计和去噪范式上的结构性缺陷：在 ARCTIC 双手动态交互数据集上，TOCH (w/ MixStyle) 的 MPJPE 高达 22.79 mm，而 GeneOH Diffusion 仅为 11.57 mm（Table 1），差距超过 11 mm。

### 技术谱系中的知识贡献

GeneOH Diffusion 的知识贡献可沿两条线索定位：

**表示学习的贡献**：GeneOH 表示将手物交互编码为接触中心的三部分正则化结构，这一设计继承了手势估计中“以物体为中心”的表示思想，但将其系统化为可去噪的完整表示框架。消融实验（Table 2）证实，移除接触中心正则化（Ours w/o Canon.）导致运动一致性指标从 0.41 急剧恶化至 13.26 mm²，证明正则化对跨物体泛化是不可或缺的。

**扩散模型的贡献**：将扩散模型用于去噪而非生成，是该方法在扩散模型谱系中的独特定位。“去噪即扩散”策略的核心洞察是：通过控制前向扩散的步数（超参数控制噪声尺度），可以在“忠实于原始输入”和“投影到干净流形”之间取得平衡。消融实验（Table 2）表明，将扩散去噪器替换为自编码器（Ours w/o Diffusion）导致穿透深度从 1.74 mm 增加至 3.83 mm，验证了扩散范式对空间去噪质量的关键作用。

### 适用边界与局限

GeneOH Diffusion 的适用边界由以下假设和约束定义：

1. **物体轨迹精确假设**：方法假设物体姿态序列是准确的，仅去噪手部轨迹。当物体姿态本身含噪时，接触点计算和正则化变换将引入系统性误差，方法无法处理。这是当前框架最根本的边界约束。

2. **物体几何泛化边界**：对于极大或极薄的全新物体，5mm 距离阈值的接触点选取策略可能失效——过大物体导致接触点稀疏，极薄物体可能导致接触点歧义。附录中的失败案例证实了这一点。

3. **计算效率边界**：三阶段渐进式去噪流程中，SpatialDiff 阶段的推理耗时约 16.6 秒（Table 8），使其难以满足实时应用需求。这一瓶颈源于空间关系的高维度（多接触点 × 多手部关键点）和扩散采样的迭代特性。

4. **训练数据依赖**：尽管泛化能力强，但规范去噪器仍需在 GRAB 数据集上训练。对于与 GRAB 交互模式差异极大的全新交互类型（如非抓取类精细操作），去噪质量可能下降。

### 开放问题

GeneOH Diffusion 开启的研究方向包括：

- **效率优化**：是否可以将三阶段去噪压缩为单一端到端网络，或通过蒸馏、一致性模型等技术加速推理？SpatialDiff 的 16.6 秒耗时是走向实用的主要障碍。
- **联合去噪**：如何将物体姿态也纳入去噪框架？当前假设物体轨迹精确，但在真实场景（如视频估计）中，手物轨迹往往同时含噪，联合去噪是自然且必要的扩展。
- **表示泛化**：接触中心的正则化策略能否直接扩展到全身交互（如人与场景交互）或多人协同场景？这需要重新定义“广义接触点”的概念以及相应的正则化变换。
- **噪声尺度自适应**：当前扩散步数需手工设定，能否根据输入噪声的严重程度自适应地调整扩散步数，在去噪强度与忠实度之间实现动态平衡？



## 原文 PDF

![[paperPDFs/ICLR_2024/GeneOH_Diffusion_Towards_Generalizable_Hand_Object_Interaction_Denoising_via_Denoising_Diffusion.pdf]]

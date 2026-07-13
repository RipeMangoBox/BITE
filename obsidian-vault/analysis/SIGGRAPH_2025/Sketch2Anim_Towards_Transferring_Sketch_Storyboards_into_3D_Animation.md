---
title: "Sketch2Anim: Towards Transferring Sketch Storyboards into 3D Animation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation.pdf
code_link: null
project_link: https://zhongleilz.github.io/Sketch2Anim/
aliases:
- Sketch2Anim
tags:
- SIGGRAPH_2025
- topic/sketch_to_animation
- topic/motion_diffusion
- topic/pose_trajectory_control
- topic/character_animation
- topic/sketch_to_animation/general
core_operator: "利用3D替身进行训练并通过神经映射器对齐2D与3D的嵌入空间，配合轨迹感知的关键姿态适配器，将多条件控制问题转化为可控的残差特征融合。"
primary_logic: "不直接提升2D条件到3D，也不直接在2D输入上训练扩散模型，而是训练一个使用3D关键姿态和轨迹的多条件运动生成器，再通过2D编码器对齐到同一共享嵌入，使得推理时能无缝接受2D草图输入，同时保持高精度控制。"
claims:
- "消融实验（表2）表明，采用轨迹ControlNet与关键姿态适配器的完整方法在FID、MPJPE-3D、轨迹控制精度上均优于单/双ControlNet方案。"
- "用户感知研究（图10）显示，Sketch2Anim在所有三个评估维度（运动真实感、轨迹准确性、关键姿态准确性）上均被显著偏好（88%/87%/90% vs Direct 2D-to-Motion）。"
- "HumanML3D 上 FID↓ (Average / Cross) = 0.525 / 0.577"
- "HumanML3D 上 MPJPE-2D↓ (Average) = 0.0360"
---

# Sketch2Anim: Towards Transferring Sketch Storyboards into 3D Animation

> [!tip] 核心洞察
> 不直接提升2D条件到3D，也不直接在2D输入上训练扩散模型，而是训练一个使用3D关键姿态和轨迹的多条件运动生成器，再通过2D编码器对齐到同一共享嵌入，使得推理时能无缝接受2D草图输入，同时保持高精度控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sketch2Anim：将素描故事板转化为三维动画 |
| 英文题名 | Sketch2Anim: Towards Transferring Sketch Storyboards into 3D Animation |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://doi.org/10.1145/3731167) · [Project](https://zhongleilz.github.io/Sketch2Anim/) |
| Topic | #topic/sketch_to_animation #topic/motion_diffusion #topic/pose_trajectory_control #topic/character_animation #topic/sketch_to_animation/general |
| Method | Multi-conditional motion diffusion, trajectory ControlNet, keypose adapter, 2D-3D neural mapper |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ (Average / Cross) 为 0.525 / 0.577，对比 —，变化 最佳。
> - HumanML3D 上，MPJPE-2D↓ (Average) 为 0.0360，对比 —，变化 最佳。
> - HumanML3D 上，MM Dist↓ (Average) 为 3.077，对比 —，变化 最佳。

## 概要

将手绘素描故事板转化为三维角色动画，是动画制作中一项高度耗时且依赖专业技能的任务。传统工作流（Figure 2）要求动画师根据二维草图想象关键姿态序列，再在三维软件中手动摆放关节、设计运动，经历反复试错才能产出高质量动画。这一过程的核心瓶颈在于**二维草图与三维运动之间存在巨大的域差距**——从稀疏的二维线条中恢复精确的三维空间运动，本质上是一个高度欠约束的逆向问题。

针对这一挑战，我们提出 **Sketch2Anim**，一个将素描故事板自动转化为三维动画的框架。给定由草图关键姿态、关节轨迹和动作词组成的故事板，Sketch2Anim 将每一帧草图转化为一段三维运动片段，并将所有片段融合为连贯完整的动画（Figure 1）。

Sketch2Anim 的核心洞察是：**不直接提升二维条件到三维，也不直接在二维输入上训练扩散模型**。相反，我们训练一个使用三维关键姿态和轨迹作为条件的高精度多条件运动生成器，同时通过一个神经映射器将二维编码器对齐到同一共享嵌入空间。这一设计使得推理时可以无缝接受二维草图输入，同时保持与三维条件训练时相当的控制精度，从而绕开了二维到三维直接映射的固有困难。

方法由两个核心模块构成（Figure 3）：

1. **多条件运动生成器**（Sec. 4）：基于运动扩散模型，集成轨迹 ControlNet 与轨迹感知的关键姿态适配器，同时接受动作词、三维关键姿态和三维关节轨迹作为条件，实现精细的运动控制。关键姿态适配器接收轨迹 ControlNet 的残差特征，将其与关键姿态条件融合，解决了多 ControlNet 集成困难的问题。

2. **二维-三维神经映射器**（Sec. 5）：通过匹配损失和对比对齐损失，将二维关键姿态/轨迹编码器与三维关键姿态/轨迹编码器对齐到共享嵌入空间，使推理时的二维输入能够替代训练时的三维条件。

在 HumanML3D 数据集上的实验表明，Sketch2Anim 在运动真实感（FID）、控制精度（MPJPE-2D）和文本-运动匹配度（MM Dist）上均优于 Motion Retrieval、Lift-and-Control 和 Direct 2D-to-Motion 三种基线方法（Table 1）。消融实验证实，轨迹 ControlNet 与关键姿态适配器的组合设计显著优于单 ControlNet 或双 ControlNet 方案（Table 2）。用户感知研究进一步表明，Sketch2Anim 在运动真实感、轨迹准确性和关键姿态准确性三个维度上均被显著偏好（偏好率 88%/87%/90% vs Direct 2D-to-Motion，Figure 10）。

方法也存在明确局限：未考虑角色与物体的交互，缺乏物理约束可能导致运动末端身体折叠或漂浮（Figure 14）。这些方向连同多 ControlNet 集成、速度线理解、场景-角色联合重建等问题，构成了未来工作的开放挑战。

三维角色动画是影视、游戏和虚拟现实内容生产的核心环节，但其制作流程长期依赖大量人工操作。在传统工作流中（图2），动画师需根据故事板中的二维草图，在脑中构想完整的关键姿态序列，再将其导入三维软件（如Blender）手动调整关节位置以匹配参考姿态，同时设计运动轨迹以诠释动作语义。这一反复试错的过程高度依赖动画师的专业经验，时间成本极高，且难以在早期创意阶段快速迭代。

近年来，基于扩散模型的三维人体动作生成取得了显著进展，使得从文本描述（如“行走”“跳跃”）自动合成动作序列成为可能。然而，文本仅能提供粗粒度的语义控制，无法精确约束动作的空间形态——例如角色四肢的具体位置、关节在空间中的运动路径等。故事板草图中天然蕴含了这些细粒度信息：**关键姿态**（keypose）定义了特定时刻的角色静态造型，**关节轨迹**（joint trajectory）描述了特定关节点随时间推移的空间位移。若能将这些二维草图约束直接转化为三维动画，将极大降低动画创作的门槛并加速迭代。

### 核心瓶颈：二维草图到三维运动的域差距

从二维草图条件直接生成高质量三维运动面临一个根本性挑战：**巨大的域差距**（domain gap）。二维关键姿态和轨迹仅提供平面投影信息，缺乏深度和三维空间关系，直接将其作为运动扩散模型的条件输入，模型难以推断出合理的三维运动。现有方案通常试图沿两条路径解决这一问题：

1. **检索式方法**：将二维草图特征与预存的三维动作库进行匹配（如基于TMR, Petrovich et al., 2023）。这类方法受限于动作库的覆盖范围，无法生成库外的运动，且对草图的细微变化不敏感。
2. **提升-控制方法**（Lift-and-Control）：先通过三维人体姿态估计器（如MotionBERT, Zhu et al., 2023）将二维关键姿态提升为三维，再以三维条件驱动运动生成器。然而，从单张草图提升三维姿态本身就是一个病态问题——尤其当用户草图存在比例失调、线条抖动等粗糙绘制特征时（图12），提升结果往往出现头部、手臂、腿部的严重畸变，进而导致后续运动生成失败。

### 多条件控制的融合困境

即使解决了条件来源的问题，另一个关键瓶颈在于**多条件的有效融合**。一个理想的动画生成系统需要同时响应三个异构条件：动作词语义（全局运动类型）、关键姿态（特定帧的空间约束）和关节轨迹（时序空间路径）。现有的运动扩散模型通常采用ControlNet机制注入额外条件，但如何高效集成多个ControlNet仍是一个开放问题——在图像和视频生成领域，简单的并联或串联多个ControlNet往往导致条件冲突或控制精度下降。若仅使用单个ControlNet处理所有条件，则难以在轨迹精度和姿态精度之间取得平衡。

### 本文动机

上述分析揭示了两个亟待解决的核心问题：
- **如何跨越二维草图与三维运动之间的域鸿沟**，使得粗糙甚至失真的二维输入也能驱动高质量三维动作生成？
- **如何在单一扩散模型中实现轨迹、关键姿态和动作词三者的精确协同控制**，避免条件冲突？

Sketch2Anim的设计动机正是围绕这两个瓶颈展开：不直接提升二维条件到三维，也不在二维输入上训练扩散模型，而是**训练一个以三维关键姿态和轨迹为条件的高精度运动生成器，再通过专门的神经映射器将二维编码器对齐到同一共享嵌入空间**，使得推理时能无缝接受二维草图输入，同时保持三维条件训练的精确控制能力。这一“替身训练、嵌入对齐”的策略构成了本文方法的核心洞见。

## 核心方法与创新机理

Sketch2Anim 的核心创新并非设计全新的生成范式，而是通过**训练-推理条件解耦**与**多条件注入架构重设计**，系统性地解决了“2D草图→3D动画”任务中两个深层瓶颈：2D/3D域差距导致的条件退化，以及多条件（动作词、关键姿态、轨迹）并发控制时的冲突与精度损失。

### 创新一：训练-推理条件解耦——以3D替身对齐2D嵌入

**Changed Slot：训练条件**

- **Baseline 方案**：直接使用从草图中检测的2D关键姿态和2D轨迹作为运动扩散模型的条件（Direct 2D-to-Motion）。该方案将2D噪声和歧义直接注入生成过程，模型需同时隐式学习2D→3D提升与运动生成，导致控制精度与运动质量的双重退化。
- **Sketch2Anim 方案**：训练阶段使用精确的**3D关键姿态和3D轨迹**作为“替身条件”，充分释放多条件运动生成器的控制能力；同时训练一个**2D-3D神经映射器**，将2D关键姿态/轨迹编码器与3D编码器对齐到**共享嵌入空间**。推理时，2D草图条件经映射器编码后，直接替代3D条件注入生成器，无需显式3D提升。

**因果机制**：该设计的因果逻辑链为：3D替身条件 → 消除训练中的2D歧义与噪声 → 运动生成器学习到高精度的条件-运动映射 → 神经映射器保证2D嵌入与3D嵌入在特征空间中对齐 → 推理时2D条件可无缝驱动生成器。这本质上将困难的“2D→3D→运动”联合学习，分解为“3D→运动”的精确建模与“2D↔3D”的嵌入对齐两个子问题。

**证据强度**：消融实验（Table A2）表明，移除神经映射器中的重建损失 $\mathcal{L}_{\text{recon}}$ 会导致 FID 恶化 32.81%（Average 设置），验证了嵌入对齐对生成质量的因果贡献。用户感知研究（Fig. 10）中，Sketch2Anim 在关键姿态准确性上以 90% 的偏好率显著优于 Direct 2D-to-Motion，直接证明了训练-推理解耦策略相比端到端2D条件训练的优势。

### 创新二：轨迹感知的关键姿态适配器——多条件注入的架构重设计

**Changed Slot：多条件注入机制**

- **Baseline 方案**：使用单个 ControlNet 同时注入轨迹和关键姿态条件，或使用双 ControlNet 并行处理后合并残差。前者导致条件间相互干扰，后者面临多 ControlNet 残差融合的开放难题——简单加权求和易造成条件冲突，且损失权重难以平衡。
- **Sketch2Anim 方案**：采用**单一轨迹 ControlNet + 轨迹感知关键姿态适配器**的非对称架构。轨迹 ControlNet 以轨迹嵌入 $\mathcal{E}_{tr}^{3D}(\mathbf{T}_{3D}^{r})$ 增强噪声潜在变量 $z_t$，输出轨迹残差特征 $\mathbf{r}$；关键姿态适配器则接受 $z_t$、时间步 $t$、轨迹残差 $\mathbf{r}$ 以及关键姿态增强的动作嵌入 $\pmb{a}'$，输出修正残差 $\mathbf{r}'$，最终噪声预测为 $\epsilon_t = \epsilon_\theta(z_t, t, \mathbf{a}) + \mathcal{Z}(\mathbf{r}')$。

**因果机制**：适配器的关键设计在于**以轨迹残差为条件的层级化注入**——关键姿态适配器并非独立处理关键姿态条件，而是在轨迹 ControlNet 已提取的轨迹特征 $\mathbf{r}$ 基础上进行残差修正。这迫使模型学习“在满足轨迹约束的前提下，如何调整运动以匹配关键姿态”，从而隐式建立了条件间的优先级与协调关系，避免了双 ControlNet 并行融合时的冲突。

**证据强度**：Table 2 的消融实验直接对比了四种架构变体——单 ControlNet（轨迹+关键姿态）、双 ControlNet 并行、仅轨迹 ControlNet、以及完整的轨迹 ControlNet + 关键姿态适配器。完整方案在 FID、MPJPE-3D 及轨迹控制精度上均取得最优。Fig. 9 的视觉消融进一步显示，替代方案在轨迹偏离（如圆圈标注的偏差）和关键姿态匹配上均存在明显缺陷。

### 创新三：训练数据增强策略——弥合合成-真实草图域差

虽然未在 changed slots 中显式列出，但该创新是使上述架构在真实草图输入上鲁棒运行的必要条件。Sketch2Anim 在合成训练数据上施加**两级扰动**：先随机扰动身体部位比例（如颈部拉长、手臂缩放），再对部分关节点添加随机偏移。这模拟了真实草图中比例失调、线条抖动等噪声特征，使得在纯净合成数据上训练的模型能够泛化至用户粗糙草图。Fig. 7 展示了三级数据（完美关节点→比例扰动→关节点扰动）的递进退化，Fig. 12 验证了经此增强训练的模型对歪斜、抖动草图输入的鲁棒性——检测到的2D关节点虽存在噪声，但生成的运动仍能忠实还原草图意图。

### 与相关工作的本质差异

需注意，Sketch2Anim 的贡献不在于提出 ControlNet 或适配器本身——ControlNet 已在图像/运动生成中广泛应用，适配器范式亦非首创。其真正的创新在于**面向“2D草图→3D动画”这一特定跨域、多条件任务的系统性架构决策**：识别出直接2D条件训练的根本性缺陷，设计训练-推理解耦策略；洞察多 ControlNet 融合的开放难题，提出非对称的轨迹感知适配器方案。这两个决策共同构成了从“能否生成”到“能否精确控制”的质变。

Sketch2Anim 的整体流程围绕一个核心矛盾展开：**2D 草图和 3D 运动之间存在巨大的域差距**，直接从 2D 条件生成高质量 3D 运动极为困难。为解决这一问题，Sketch2Anim 不直接在 2D 输入上训练运动扩散模型，也不采用“先提升到 3D 再生成”的级联策略，而是设计了一套**训练时使用 3D 替身、推理时接受 2D 输入**的架构，将多条件控制问题转化为可控的残差特征融合问题。

### 输入与预处理

系统的输入来自用户绘制的故事板草图，包含三类信息（Fig. 4）：
- **2D 关键姿态**：通过 Sketch2Pose 从草图中检测出的 22 个 2D 关节点，表示为 $\{(x_j, y_j)\}_{j=1}^{22}$。
- **2D 关节轨迹**：用户绘制的轨迹曲线，经均匀重采样后得到轨迹点序列 $\{(x_i^j, y_i^j)\}_{i=1}^{t_r}$。
- **动作词**：描述运动语义的文本标签。

值得注意的是，系统并不直接使用原始草图像素，而是以检测到的 2D 关节点作为输入。这一设计使得后续的 2D-3D 对齐可以在结构化的关键点空间中进行，而非在非结构化的图像空间中处理。

### 两大核心模块

Sketch2Anim 由两个协同工作的模块构成（Fig. 3）：

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3731167/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Sketch2Anim. Our pipeline consists of two core modules - the multi-conditional motion generator (Sec. 4) and the 2D-3D neural mapper (Sec. 5). Instead of directly lifting the 2D keypose and trajectory into their 3D counterparts, we train a neural mapper dedicated to aligning the two domains in the embedding space. Because of this shared embedding, it enables the employment of more informative and precise 3D keyposes and trajectories as the motion conditions in the motion generator, while exploiting the 2D keypose and trajectory detected from the sketch storyboard at inference time. The legend indicates the data flow at training and inference of both modules. See the following se...*

1. **多条件运动生成器**（Multi-conditional Motion Generator，Sec. 4）：基于预训练的运动扩散模型构建，集成了**轨迹 ControlNet** 和**轨迹感知的关键姿态适配器**。轨迹 ControlNet 负责注入关节轨迹约束，关键姿态适配器则接收轨迹 ControlNet 的残差特征，融合关键姿态条件后输出修正残差。这一设计避免了直接训练多个 ControlNet 时面临的损失平衡和残差融合难题。

2. **2D-3D 神经映射器**（2D-3D Neural Mapper，Sec. 5）：在训练阶段，运动生成器使用信息更丰富的 3D 关键姿态和 3D 轨迹作为条件。神经映射器的作用是将 2D 编码器和 3D 编码器对齐到**共享的嵌入空间**中，使得推理时可以直接输入从草图检测的 2D 条件，而无需将其显式提升到 3D。对齐过程使用匹配损失和对比损失联合优化。

### 推理流程

推理时，系统首先通过 Sketch2Pose 从用户草图中提取 2D 关键姿态和 2D 轨迹点，然后由 2D 编码器将其映射到共享嵌入空间。这些嵌入被送入多条件运动生成器，与动作词嵌入一起控制扩散模型的去噪过程，生成符合所有约束的 3D 运动片段。最后，通过基于 DDIM 反演的引导去噪方法（Sec. 6），将相邻的运动片段混合成连贯的完整动画。

### 框架设计的因果逻辑

这一框架的因果链路可概括为：**3D 替身训练 → 共享嵌入对齐 → 2D 推理泛化**。训练时使用 3D 条件保证了控制精度（因为 3D 关键姿态和轨迹包含完整的空间信息），而神经映射器的嵌入对齐则使得推理时 2D 输入能够无缝替代 3D 条件。消融实验证实，去除神经映射器中的重建损失会导致 FID 下降 32.81%（Table A2），验证了嵌入对齐的关键作用。

### 问题定义与输入表示

给定一帧素描故事板，系统接收三个模态的输入条件：动作词文本 $\mathbf{a}$、2D关键姿态 $\{ (x_j, y_j) \}_{1}^{J=22}$（22个关节点的二维坐标集合），以及2D关节轨迹点集 $\{ (x_i^j, y_i^j) \}_{i=1}^{t_r}$（第 $j$ 个关节在时间维度上的轨迹采样点）。核心挑战在于，2D草图和3D运动之间存在巨大的域差距，直接从2D条件生成高质量3D运动极为困难。

Sketch2Anim 通过两个核心模块解决这一问题：**多条件运动生成器**（Sec. 4）和**2D-3D神经映射器**（Sec. 5）。其核心洞察是：不直接在2D输入上训练扩散模型，而是训练一个使用3D关键姿态和3D轨迹的多条件运动生成器，再通过神经映射器将2D编码器对齐到同一共享嵌入空间，使得推理时能无缝接受2D草图输入。

---

### 多条件运动生成器

运动生成器建立在预训练的运动扩散模型之上，包含两个关键组件：**轨迹ControlNet**和**轨迹感知关键姿态适配器**。该设计的动机是：同时精确控制动作词、关键姿态和关节轨迹三个条件极为困难，而简单地堆叠多个ControlNet会导致残差特征融合的平衡问题（这在运动和图像生成领域均未解决）。

#### 轨迹ControlNet

轨迹ControlNet $\mathcal{F}_{\mathrm{tr}}$ 负责将关节轨迹条件注入扩散过程。给定噪声潜在变量 $z_t$、时间步 $t$ 和动作词嵌入 $\mathbf{a}$，首先将轨迹嵌入叠加到噪声潜在变量上，再通过ControlNet获取残差特征：

$$z_t^{\prime} = z_t + \mathcal{E}_{tr}^{3D}( \mathbf{T}_{3D}^{r} ), \quad \mathbf{r} = \mathcal{F}_{\mathrm{tr}}(z_t^{\prime}, t, \mathbf{a})$$

其中 $\mathcal{E}_{tr}^{3D}$ 是3D轨迹编码器，$\mathbf{T}_{3D}^{r}$ 是3D关节轨迹表示，$\mathbf{r}$ 为轨迹ControlNet输出的残差特征。该公式对应原文 Eq. (1)，体现了轨迹条件通过加性嵌入注入噪声潜在变量的机制。

#### 轨迹感知关键姿态适配器

关键姿态适配器 $\mathcal{F}_{\mathrm{k}}$ 置于轨迹ControlNet与扩散模型之间，负责在轨迹残差的基础上进一步注入关键姿态约束。其输入包括噪声潜在变量 $z_t$、时间步 $t$、轨迹ControlNet的残差特征 $\mathbf{r}$，以及经过关键姿态增强的动作嵌入 $\pmb{a}^{\prime}$：

$$\pmb{a}^{\prime} = \pmb{a} + \mathcal{E}_{k}^{3D}( \mathbf{K}_{3D} )$$

$$\mathbf{r}^{\prime} = \mathcal{F}_{\mathrm{k}}(z_t, t, \mathbf{r}, {\pmb{a}}^{\prime})$$

其中 $\mathcal{E}_{k}^{3D}$ 是3D关键姿态编码器，$\mathbf{K}_{3D}$ 为3D关键姿态表示。最终噪声预测由基础扩散模型输出与适配器残差的零卷积结果相加得到：

$$\epsilon_t = \epsilon_{\theta}(z_t, t, \mathbf{a}) + \mathcal{Z}(\mathbf{r}^{\prime})$$

$\mathcal{Z}$ 为零卷积操作，确保训练初期适配器输出不影响预训练模型。该设计（Eq. 3）使得关键姿态条件通过残差修正的方式融入，而非直接与轨迹ControlNet竞争特征空间。

#### 训练损失

多条件运动生成器的训练冻结预训练扩散模型参数，仅优化轨迹ControlNet和关键姿态适配器。总体生成损失为：

$$\mathcal{L}_{\mathrm{gen}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{tr}} \mathcal{L}_{\mathrm{tr}} + \lambda_{\mathrm{key}} \mathcal{L}_{\mathrm{key}}$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 是标准噪声重建损失，$\mathcal{L}_{\mathrm{tr}}$ 和 $\mathcal{L}_{\mathrm{key}}$ 分别为轨迹和关键姿态的空间约束项，$\lambda_{\mathrm{tr}}$、$\lambda_{\mathrm{key}}$ 为对应权重。消融实验（Table A1）表明，去除这两个空间约束项后，控制精度（MPJPE-3D）改善18.37%，但FID变差，说明空间约束对运动真实感至关重要。

---

### 2D-3D神经映射器

神经映射器的目标是解决训练时使用3D条件、推理时输入2D条件的域不匹配问题。其核心机制是对齐2D和3D关键姿态/轨迹的嵌入空间，使得在共享嵌入中2D和3D表示可互换。

#### 匹配损失

基础对齐通过最小化成对嵌入的欧氏距离实现：

$$\mathcal{L}_{\mathrm{match}} = -\frac{1}{B}\sum_{i=1}^{B}\sum_{y\in\{tr,k\}} \Vert \mathbf{s}_{i,y}^{3D} - \mathbf{s}_{i,y}^{2D} \Vert_{2}^{2}$$

其中 $B$ 为批次大小，$\mathbf{s}_{i,y}^{3D}$ 和 $\mathbf{s}_{i,y}^{2D}$ 分别为第 $i$ 个样本在模态 $y$（轨迹 $tr$ 或关键姿态 $k$）下的3D和2D嵌入。该公式（Eq. 10）直接拉近配对嵌入的距离。

#### 对比对齐损失

为进一步提升对齐的区分度，引入对比学习损失：

$$\mathcal{L}_{\mathrm{contrast}} = -\frac{1}{B}\sum_{i=1}^{B}\sum_{y\in\{tr,k\}} \log \frac{\exp( sim(\mathbf{s}_{i,y}^{3D}, \mathbf{s}_{i,y}^{2D}) / \tau_{1})}{\sum_{j=1}^{B} \exp( sim(\mathbf{s}_{i,y}^{3D}, \mathbf{s}_{j,y}^{2D}) / \tau_{1})}$$

其中 $sim(\cdot,\cdot)$ 为余弦相似度，$\tau_{1}$ 为温度参数。该公式（Eq. 12）通过将正样本对拉近、负样本对推远，增强嵌入空间的判别性。消融实验（Table A2）显示，去除重建损失 $\mathcal{L}_{\mathrm{recon}}$ 会导致FID下降32.81%，验证了映射器损失设计的必要性。

---

### 训练与推理的域桥接机制

训练阶段，运动生成器接收3D关键姿态和3D轨迹作为条件，神经映射器同步学习2D-3D嵌入对齐。推理阶段，2D关键姿态和2D轨迹通过映射器的2D编码器投影到共享嵌入空间，直接替代3D嵌入输入运动生成器。这一设计使得生成器始终在高质量的3D条件空间训练，同时推理时无需显式的2D到3D提升步骤，避免了提升过程引入的误差累积（Figure 12 显示直接提升2D关节点到3D会产生头部、手臂、腿部等部位的错误）。

## 实验与关键发现

### 核心瓶颈与实验设计逻辑

Sketch2Anim 面临的核心挑战是 **2D 草图与 3D 运动之间的巨大域差距**——直接从 2D 条件生成高质量 3D 运动会因信息缺失和歧义性导致控制精度与运动真实感双双下降。同时，现有运动扩散模型难以同时精确控制多个异质条件（动作词、关键姿态、关节轨迹）。为验证所提方案的有效性，实验设计围绕两条因果路径展开：**（1）用 3D 替身训练 + 神经映射器对齐能否弥合域差距？** 以及 **（2）轨迹 ControlNet + 轨迹感知关键姿态适配器的多条件注入机制是否优于单/双 ControlNet 方案？**

所有实验均在 **HumanML3D** 数据集上进行，评估指标覆盖三个维度：**运动真实感**（FID）、**控制精度**（MPJPE-2D/3D、Trajectory Error）、以及 **文本-运动匹配度**（MM Dist）。遵循 OmniControl（Xie et al., 2024）的设置，控制精度指标同时报告 Average（所有关节平均）和 Cross（随机组合）两种模式。

---

### 主实验结果：与三类基线的全面对比

Table 1 报告了 Sketch2Anim 与三类基线的量化对比。基线方法分别为：

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3731167/figures/007_Table_1.jpg]]
*Table 1: Quantitative analysis of Sketch2Anim (Ours) and three baseline models defined in Sec. 7.1 on the HumanML3D dataset. Evaluation metrics on motion realism, control accuracy, and text-motion match are presented. Following OmniControl [Xie et al. 2024], we report both the average error of all joints (Average) and their random combination (Cross). The best results are highlighted*

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3731167/figures/019_Table_1.jpg]]
*Table 1: Table A2. Ablation study of the loss terms of our neural mapper to align 2D-3D embeddings using the HumanML3D dataset. Refer to the paper for the definition of the reported metrics and the Average and Cross evaluation settings. Note that the statistics of Ours’ are different with the numbers in Table 1 in the main paper, because we did not include inference guidance in this experiment*

- **Motion Retrieval**：基于 TMR（Petrovich et al., 2023）的检索方案，从数据库中检索最匹配的运动片段。
- **Lift-and-Control**：先通过 MotionBERT（Zhu et al., 2023）将 2D 关键姿态和轨迹提升到 3D，再输入与本文相同的运动生成器。
- **Direct 2D-to-Motion**：直接在 2D 输入上训练运动扩散模型，不做域对齐。

**Sketch2Anim 在所有指标上均取得最优结果**（Table 1）。在运动真实感指标上，FID 达到 0.525（Average）/ 0.577（Cross），显著优于 Direct 2D-to-Motion 的直接方案。控制精度方面，MPJPE-2D 在 Average 设置下低至 0.0360，表明生成运动的关键姿态与输入草图的 2D 约束高度吻合。文本-运动匹配度 MM Dist 为 3.077（Average），验证了动作词语义的有效保持。

**关键因果解释**：Lift-and-Control 的性能瓶颈在于“提升-生成”两阶段误差累积——从草图中检测的 2D 关节点本身存在噪声和歧义，直接提升到 3D 会放大这些误差（Fig. 12 直观展示了提升后的 3D 关键姿态存在头部、手臂、腿部的明显畸变），进而污染后续运动生成。Sketch2Anim 通过神经映射器将 2D 和 3D 嵌入空间对齐，使推理时可直接使用 2D 条件，从而绕过了显式 3D 提升步骤，从根源上切断了这一误差链。

---

### 消融实验：多条件注入机制的有效性

Table 2 聚焦于多条件运动扩散模型的设计空间消融，所有变体均使用 3D 关键姿态和 3D 轨迹作为条件，以隔离注入机制的影响。比较的变体包括：

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3731167/figures/010_Table_2.jpg]]
*Table 2: Ablation studies on multi-conditional motion diffusion model design using the HumanML3D dataset. Sec. 7.2 defines all the variants, and we use the 3D keypose and 3D trajectory as conditions in this experiment, thus only reporting the control accuracy in its 3D format. Best results are highlighted*

- **Single ControlNet**：仅使用一个 ControlNet 同时注入关键姿态和轨迹条件。
- **Dual ControlNets**：使用两个独立 ControlNet 分别处理关键姿态和轨迹，通过简单合并残差特征融合。
- **Ours（轨迹 ControlNet + 关键姿态适配器）**：完整方案。

结果显示，**轨迹 ControlNet + 关键姿态适配器的组合在所有指标上均优于单/双 ControlNet 方案**（Table 2）。具体而言，Single ControlNet 因条件信息混杂导致控制精度和运动质量双降；Dual ControlNets 虽有所改善，但两个 ControlNet 的残差特征直接合并会引入冲突，难以有效平衡。本文方案通过将关键姿态条件注入置于轨迹 ControlNet 之后、以轨迹残差为条件的适配器中，实现了条件的层次化融合——轨迹提供全局空间约束，关键姿态在此基础上进行局部修正。

Fig. 9 提供了视觉消融证据：在给定相同 3D 关键姿态（紫色角色）和 3D 轨迹（黄色曲线）的条件下，Single ControlNet 和 Dual ControlNets 生成的运动会偏离轨迹（见圆圈标注的轨迹偏差）或关键姿态不准确，而本文方法忠实遵循两个约束。

**损失项消融**（Table A1）进一步揭示了空间约束项的作用：去除轨迹和关键姿态的空间约束损失 $ \mathcal{L}_{\mathrm{tr}} $ 和 $ \mathcal{L}_{\mathrm{key}} $ 后，控制精度 MPJPE-3D 改善 18.37%（Average），但 FID 变差。这表明空间约束项在控制精度和运动自然度之间存在权衡——它们强制运动遵循精确的轨迹和姿态，但过度约束可能损害运动的流畅性。

---

### 神经映射器消融：域对齐的必要性

Table A2 消融了神经映射器的损失项设计（注意该实验未使用推理引导，因此数值与 Table 1 不同）。去除重建损失 $ \mathcal{L}_{\mathrm{recon}} $ 后，FID 下降 32.81%（Average），表明单纯的对齐损失（匹配损失 + 对比损失）不足以保持嵌入空间中的判别信息，重建损失的引入对维持运动生成质量至关重要。

---

### 推理引导与运动混合

**推理引导**（Table A3）采用二阶优化策略，在推理时对生成的噪声潜在变量进行梯度引导，使其更精确地满足轨迹和关键姿态约束。实验表明，使用二阶推理引导使 Avg.Err.-2D 降低 45.13% 以上，显著提升了控制精度而不增加训练成本。

**运动混合**（Table A4）比较了不同混合策略在 HumanML3D 子集上的表现。基于 DDIM 反演的引导去噪方案（Algorithm 1）在保持运动连贯性的同时，有效融合了相邻运动片段的边界约束，优于简单的线性插值或直接拼接。

---

### 用户感知研究：主观偏好的决定性证据

Fig. 10 报告了用户感知研究结果，参与者在三个维度上对 Sketch2Anim 与各基线进行成对比较：

- **运动真实感**：Sketch2Anim 被偏好 88%（vs Motion Retrieval）、87%（vs Lift-and-Control）、88%（vs Direct 2D-to-Motion）。
- **轨迹准确性**：偏好率分别为 90%、87%、89%。
- **关键姿态准确性**：偏好率分别为 88%、87%、90%。

所有比较中偏好率均远超 50% 的随机水平，且在三项指标上一致领先，构成 **强决定性证据**（置信度 0.98）。特别值得注意的是，即使与使用相同运动生成器但依赖 3D 提升的 Lift-and-Control 相比，Sketch2Anim 仍在所有维度被显著偏好，直接验证了“绕过显式 3D 提升、通过嵌入对齐使用 2D 条件”这一核心设计决策的正确性。

---

### 失败模式与局限性

Fig. 14 展示了两个典型失败案例，揭示了方法的根本局限：

1. **缺乏角色-物体交互建模**：当动作涉及外部物体时（如高尔夫挥杆），生成的运动无法保证手部与物体的接触关系——在结束关键姿态时双手未握持球杆。这是因为训练数据（HumanML3D）仅包含人体关节运动，不包含物体信息，且条件信号（2D 关键姿态和轨迹）本身也不编码物体约束。

2. **缺乏物理约束**：即使脚步轨迹正确，在运动末端身体可能出现折叠或漂浮在空中的情况。这表明纯数据驱动的运动生成无法保证物理合理性（如地面接触、关节角度限制），需要额外的物理先验或约束。

---

### 条件影响的定性分析

Fig. 13 通过逐步添加/改变条件，直观展示了各条件对生成运动的控制作用：
- 仅给定动作词“Walk”时，生成运动仅保持行走语义，但方向和姿态自由。
- 添加草图关键姿态后，运动在保持行走的同时开始遵循姿态约束。
- 将向前轨迹替换为向后轨迹，运动方向相应反转。
- 将动作词替换为“Jump”，运动语义从行走变为跳跃。

这表明三个条件（动作词、关键姿态、轨迹）以可解耦的方式协同控制运动生成，且每个条件的变化都能独立地反映在生成结果中。

---

### 数据增强与鲁棒性

为弥合合成训练数据与用户手绘草图之间的分布差距，本文对训练数据施加了多重扰动（Fig. 7）：随机扰动身体部位比例（如颈部、手臂长度），以及对部分关节点添加随机偏移以模拟草图检测的不精确性。Fig. 12 验证了这种增强策略的鲁棒性——即使输入草图存在扭曲的线条和不成比例的身体部位，Sketch2Pose 的 2D 关节检测仍保持稳定，且 Sketch2Anim 能基于这些不完美的 2D 关节点生成高质量运动。相比之下，直接将这些 2D 关节点提升到 3D 会导致明显的结构错误。

---

### 实验公平性说明

所有比较方法均在同一 HumanML3D 数据上训练和评估，使用相同的输入格式（2D 关键姿态、轨迹、动作词）。推理时间均在单张 NVIDIA RTX4090 GPU 上测量，确保了计算资源的公平对比。

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3731167/figures/013_Figure_11.jpg]]
*Figure 11: (b) (d) Fig. 11. 3D editing. Given one frame of a real-world storyboard (a), we preprocess it to obtain the keypose (i.e., 2D joint points in red) and the trajectory (i.e., curve points in cyan) (b). Our Sketch2Anim produces the animation conditioned on the action word, 2D keypose, and the 2D trajectory (c). Note that we manually model the room with a table for visualization purposes, and the 3D trajectory from the resulting motion is highlighted with cyan points. If the user is unsatisfied with the motion (e.g., the foot penetrates the table), the 3D trajectory can be further edited by dragging a few sample points to create a new 3D trajectory (purple points at the top-right corner in (c))...*

![[assets/figures/papers/paper_list_l2_https_doi_org_10_1145_3731167/figures/021_Table.jpg]]
*Table: A4. Quantitative comparison of motion blending methods on the HumanML3D subset*

## 定位与知识库关联

### 1. 核心瓶颈与设计动机

Sketch2Anim 的根本挑战在于 **2D 草图与 3D 运动之间的巨大域差距**。直接从 2D 条件生成高质量 3D 运动极为困难，原因在于：二维草图本身携带的信息具有固有的歧义性（深度缺失、比例失真），而现有运动扩散模型难以在单次生成中同时精确控制多个异构条件——动作词、关键姿态和关节轨迹。

传统方案面临两难：若直接在 2D 输入上训练扩散模型（即 **Direct 2D-to-Motion** 基线），模型必须隐式学习从 2D 到 3D 的映射，控制精度受限；若先将 2D 提升到 3D 再生成运动（即 **Lift-and-Control** 基线，基于 MotionBERT (Zhu et al., 2023) 进行 2D-to-3D 提升），则提升过程本身引入的误差会级联放大，破坏后续运动的控制精度。Sketch2Anim 的因果调节旋钮在于：**不直接提升 2D 条件，也不直接在 2D 输入上训练扩散模型**，而是训练一个使用 3D 替身条件（3D 关键姿态和轨迹）的多条件运动生成器，再通过一个专用的 2D-3D 神经映射器将 2D 编码器对齐到同一共享嵌入空间，使得推理时能无缝接受 2D 草图输入，同时保持高精度控制。

### 2. 与基线方法的关系与对比

论文定义了三个用于对比的基线方法，并在 HumanML3D 数据集上进行了系统的定量和定性评估（Table 1, Fig. 8, Fig. 10）：

- **Motion Retrieval**（基于 TMR, Petrovich et al., 2023）：从预构建的运动数据库中检索与输入条件最匹配的运动片段。该方法完全依赖数据库覆盖度，无法生成数据库中不存在的新运动组合，且对多条件约束的精确满足能力有限。用户感知研究中，Sketch2Anim 在运动真实感、轨迹准确性和关键姿态准确性三个维度上分别被偏好 88%、87% 和 90%（Fig. 10a）。

- **Lift-and-Control**（提升基于 MotionBERT, Zhu et al., 2023；运动生成器与 Sketch2Anim 相同）：先将 2D 关键姿态和轨迹提升到 3D，再以提升后的 3D 条件驱动运动生成器。该方案的瓶颈在于 2D-to-3D 提升过程本身的不准确性——当输入草图存在比例失真或关节位置偏差时，提升后的 3D 姿态会出现严重错误（如头部、手臂、腿部的扭曲，见 Fig. 12c），导致后续运动生成偏离用户意图。用户偏好率分别为 87%、90% 和 90%（Fig. 10b）。

- **Direct 2D-to-Motion**：直接在 2D 关键姿态和轨迹条件下训练扩散模型。该方法避免了提升误差，但要求扩散模型同时隐式学习 2D-to-3D 映射和运动生成，控制精度显著低于使用 3D 替身训练的 Sketch2Anim。用户偏好率分别为 88%、87% 和 90%（Fig. 10c）。

**关键区分点**：Sketch2Anim 通过 2D-3D 神经映射器（Sec. 5）将 2D 和 3D 条件的嵌入空间对齐，使运动生成器始终在信息更丰富的 3D 条件下训练，而推理时只需输入 2D 草图条件即可获得接近 3D 条件的控制精度。这一“训练用 3D、推理用 2D”的策略是区别于所有三个基线的核心设计。

### 3. 多条件注入机制的设计选择

在运动扩散模型的多条件控制方面，Sketch2Anim 探索了不同的条件注入架构，并通过消融实验（Table 2, Fig. 9）验证了设计选择：

- **单 ControlNet 方案**：仅使用一个 ControlNet 同时注入轨迹和关键姿态条件。该方案难以有效融合两类异构条件，控制精度和运动质量均不理想。

- **双 ControlNet 方案**：使用两个独立的 ControlNet 分别处理轨迹和关键姿态，再合并残差特征。论文指出，如何有效集成多个 ControlNet 在运动和图像生成领域均未解决，双 ControlNet 的联合训练存在损失权重平衡困难的问题。

- **Sketch2Anim 方案**：采用**轨迹 ControlNet + 轨迹感知关键姿态适配器**的组合架构（Fig. 5）。轨迹 ControlNet 负责将轨迹嵌入注入噪声潜在变量并生成残差特征 $\mathbf{r}$；关键姿态适配器 $\mathcal{F}_{\mathrm{k}}$ 则接收轨迹 ControlNet 的残差 $\mathbf{r}$ 作为输入，融合关键姿态嵌入后输出修正残差 $\mathbf{r}^{\prime}$。这种串联设计使得关键姿态控制能够感知轨迹信息，实现了更协调的多条件融合。消融实验证实该方案在 FID、MPJPE-3D 和轨迹控制精度上均优于单/双 ControlNet 方案（Table 2）。

### 4. 适用边界与局限

Sketch2Anim 在以下场景中表现出色：
- 由 2D 草图关键姿态、关节轨迹和动作词共同描述的独立人体运动生成；
- 通过运动混合（Sec. 6）将多个运动片段融合为连贯动画；
- 支持推理时的 3D 轨迹编辑以修正生成结果（Fig. 11）。

论文明确指出的局限性包括：

1. **缺乏角色-物体交互建模**：方法未考虑角色与场景物体的交互约束。例如，在高尔夫挥杆动作中，双手在结束关键姿态时未能握持球杆（Fig. 14a）。这需要联合重建场景与角色动画并施加相互空间约束。

2. **缺乏物理约束**：即使脚步轨迹正确，在运动末端身体可能出现折叠或漂浮在空中的非物理现象（Fig. 14b）。引入人体物理先验（如接触力、地面反作用力）是可能的改进方向。

3. **多 ControlNet 集成的通用性问题**：本方法仅使用单一 ControlNet 加适配器的组合，扩展到三个或更多条件（如同时控制手部轨迹、头部朝向、物体交互）仍需探索有效的多 ControlNet 融合机制。

### 5. 开放问题

论文在讨论部分提出了若干值得后续探索的方向：

- **速度线与时间控制**：如何将草图中常见的速度线（motion lines）检测和理解纳入动画时间线控制，使生成的运动节奏与草图意图一致？

- **场景与角色的联合重建**：如何联合重建场景几何与角色动画，并施加相互空间约束（如脚与地面的接触、手与物体的交互），以解决当前方法中角色与场景脱节的问题？

- **人体先验的融入**：如何将结构化人体先验（如 SMPL 模型）融入草图驱动的动画方法，以生成结构一致、物理合理的运动序列？

- **2D 运动扩散模型的中间表示**：是否可以先构建一个由 2D 关键姿态和关节轨迹条件的 2D 运动扩散模型，再将其输出提升到 3D？这一思路可能降低 2D-to-3D 映射的难度，但需要解决 2D 运动表示的歧义性问题。

### 6. 知识库定位

Sketch2Anim 处于**草图理解、运动生成和人机交互**的交叉领域。其核心贡献在于：

- 在**运动生成**维度，提出了轨迹 ControlNet 与关键姿态适配器的多条件注入架构，为运动扩散模型的多条件控制提供了有效的设计范式；
- 在**跨模态对齐**维度，通过 2D-3D 神经映射器实现了草图域与 3D 运动域的嵌入空间对齐，避免了直接 2D-to-3D 提升的误差累积；
- 在**交互工作流**维度，将传统动画制作中“想象关键姿态序列→手动摆放 3D 关节→反复试错”的流程（Fig. 2）自动化，降低了从草图故事板到 3D 动画的门槛。

该方法与现有的文本驱动运动生成（如 MDM, Chen et al., 2023）、空间约束运动生成（如 OmniControl, Xie et al., 2024）和草图驱动动画（如 Sketch2Pose）等工作形成互补，填补了从多条件草图输入直接生成可控 3D 动画的技术空白。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation.pdf]]

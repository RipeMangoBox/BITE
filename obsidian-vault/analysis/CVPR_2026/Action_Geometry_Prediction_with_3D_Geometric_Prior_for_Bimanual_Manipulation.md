---
title: Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Action_Geometry_Prediction_with_3D_Geometric_Prior_for_Bimanual_Manipulation.pdf
project_link: null
code_link: "https://github.com/Chongyang-99/GAP.git"
aliases:
- GAGP
- AGP3GPBM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 联合预测未来动作块和未来三维点图（pointmap），迫使策略在生成动作的同时预测场景几何的演变，从而获得物理一致的空间感知和动作协同。
primary_logic: 利用预训练的三维几何基础模型作为感知骨干，融合几何潜变量、二维语义特征和本体感知，通过扩散模型同时输出未来动作序列和未来三维几何潜变量，可在RGB输入的条件下实现三维感知的预测性双臂控制，彻底避免显式点云或复杂标定。
claims:
- 在RoboTwin 2.0仿真基准的优势手选择任务上，本文方法平均成功率63.2%，显著优于DP3 (61.2%) 和 G3Flow (60.7%)。
- 在同步双臂任务上，平均成功率51.3%，超过Xu et al. (47.6%) 和 G3Flow (45.8%)，尤其在悬挂杯子等任务上大幅领先。
- 消融实验显示，移除未来三维点图预测后平均成功率从25.1%降至23.6%，证实联合3D预测是性能主要驱动力。
- 真实机器人实验中，平均成功率40.0%，远超ACT (23.8%)、DP (25.0%) 和 Xu et al. (32.5%)，验证了泛化能力。
---

# Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation

> [!tip] 核心洞察
> 利用预训练的三维几何基础模型作为感知骨干，融合几何潜变量、二维语义特征和本体感知，通过扩散模型同时输出未来动作序列和未来三维几何潜变量，可在RGB输入的条件下实现三维感知的预测性双臂控制，彻底避免显式点云或复杂标定。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于3D几何先验的双臂操作动作–几何预测 |
| 英文题名 | Action-Geometry Prediction with 3D Geometric Prior for Bimanual Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23814) · [Code](https://github.com/Chongyang-99/GAP.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | GAP (Action-Geometry Prediction) |
| Dataset | RoboTwin 2.0 Dominant-select Tasks, RoboTwin 2.0 Sync-bimanual Tasks, RoboTwin 2.0 Seq-coordinate Tasks, Real-world 4 bimanual tasks |

> [!tip] 效果简介
> - RoboTwin 2.0 Dominant-select Tasks (16 tasks) 上，平均成功率 (%) 63.2 vs 61.2 (DP3) (+2.0)。
> - RoboTwin 2.0 Sync-bimanual Tasks (8 tasks) 上，平均成功率 (%) 51.3 vs 47.6 (Xu et al.) (+3.7)。
> - RoboTwin 2.0 Seq-coordinate Tasks (8 tasks) 上，平均成功率 (%) 50.4 vs (最佳基线未摘录) (N/A)。

## 概要

双臂协同操作是机器人学习中的核心挑战。现有模仿学习策略主要分为两条技术路线：基于二维视觉的方法（如**ACT** (Zhao et al., arXiv 2023)、**Diffusion Policy** (Chi et al., IJRR 2023)）从多视角RGB中隐式学习三维表征，但缺乏显式的空间推理能力；基于三维点云的方法（如**DP3** (Ze et al., RSS 2024)、**G3Flow** (Chen et al., CVPR 2025)）虽具备几何感知，却依赖相机标定和预设工作空间裁剪点云，泛化性与可扩展性受限。两条路线的共同瓶颈在于：策略无法在动作生成过程中主动预测场景几何的演变，导致空间感知薄弱、双臂协调性差。

本文提出**GAP（Action-Geometry Prediction）**，一种基于预训练三维几何先验的双臂操作动作-几何联合预测框架。其核心洞察是：利用预训练的三维几何基础模型作为感知骨干，将几何潜变量、二维语义特征与本体感知状态融合为统一的条件上下文，通过扩散模型同时输出未来动作块和未来三维点图潜变量。这一设计迫使策略在生成动作的过程中“想象”场景几何的未来状态，从而获得物理一致的空间感知和动作协同，且仅需RGB输入，彻底避免显式点云或复杂标定。

在RoboTwin 2.0仿真基准上，GAP在优势手选择任务（16项）上平均成功率达63.2%，优于DP3（61.2%）和G3Flow（60.7%）；在同步双臂任务（8项）上达51.3%，超过**Xu et al.** (CVPR 2025) 的47.6%和G3Flow的45.8%，尤其在悬挂杯子等需要精细三维推理的任务上大幅领先。消融实验证实，移除未来三维点图预测后成功率从25.1%降至23.6%，验证了联合几何预测是性能的主要驱动力。在真实机器人实验中，GAP以40.0%的平均成功率远超ACT（23.8%）、Diffusion Policy（25.0%）和Xu et al.（32.5%），展现出较强的泛化能力。

双臂操作是机器人灵巧作业的核心能力，其本质挑战在于：机器人必须同时理解三维空间几何关系、语义对象属性以及双臂间的协调约束，才能生成物理一致的动作序列。然而，当前主流的双臂模仿学习策略在三维感知能力上存在根本性瓶颈。

### 现有方法的感知困境

以 **ACT**（Zhao et al., arXiv 2023）和 **Diffusion Policy (DP)**（Chi et al., IJRR 2023）为代表的二维方法，仅从多视角RGB图像中隐式学习三维表征，完全依赖二维视觉线索。这类方法虽然避免了显式的相机标定，但由于缺乏显式的三维几何推理能力，在面对需要精确空间感知的双臂协调任务时，其空间感知薄弱、双臂协同性差。

为弥补这一缺陷，以 **DP3**（Ze et al., RSS 2024）和 **G3Flow**（Chen et al., CVPR 2025）为代表的三维方法引入了点云数据。DP3通过高效点编码器直接在点云上操作，利用三维几何信息；G3Flow则进一步融合语义与几何特征。然而，这些方法需要精确的相机标定和预设的工作空间范围来裁剪点云——这一依赖不仅增加了部署成本，更严重限制了方法的泛化能力和可扩展性。标定误差或工作空间变化都会导致点云质量下降，进而损害策略性能。

### 核心瓶颈与动机

上述分析揭示了一个清晰的瓶颈：**现有双臂模仿学习策略缺乏显式的三维几何推理能力，要么依赖二维视觉特征导致空间感知薄弱，要么需要昂贵且不可靠的标定点云限制泛化性。** 这一瓶颈在需要精细空间协调的双臂任务（如同步操作、顺序配合）中尤为突出。

本文的核心动机在于提出一个根本性的问题：**能否在仅使用RGB输入、无需显式点云或复杂标定的条件下，赋予策略真正的三维感知能力？** 这要求策略不仅感知当前场景的三维几何，还能预测未来几何状态的演变，从而在动作生成过程中获得物理一致的空间感知和动作协同。实现这一目标的关键在于利用预训练的三维几何基础模型作为感知先验，将几何推理能力注入模仿学习框架，彻底避免对显式三维传感器或标定流程的依赖。

## 核心方法与创新机理

本文的核心洞察在于：**将未来三维几何预测显式地嵌入双臂模仿学习的扩散策略中**，使模型在生成动作的同时“想象”场景几何的演变，从而获得物理一致的空间感知与双臂协同能力。这一设计直接回应了现有方法的根本瓶颈——二维策略缺乏三维推理，而三维策略依赖昂贵且不可靠的标定点云。

### 感知骨干的范式转换：从显式点云到预训练三维先验

现有三维策略（如 **DP3** (Ze et al., RSS 2024)、**G3Flow** (Chen et al., CVPR 2025)）需要相机标定和预设工作空间来裁剪点云，这不仅限制了泛化性，也引入了标定误差的风险。本文彻底抛弃了这一依赖：**仅以RGB时序图像为输入，通过预训练三维几何基础模型π3作为感知骨干**，直接从2D观测中提取三维几何潜变量。同时引入二维语义基础模型DINOv3提取语义特征，形成几何-语义双流感知架构（Figure 2）。这一设计使得模型无需任何显式点云或标定即可获得鲁棒的三维空间理解。

### 预测目标的根本扩展：联合动作-几何生成

传统扩散策略（**ACT** (Zhao et al., arXiv 2023)、**Diffusion Policy** (Chi et al., IJRR 2023)）仅预测未来动作块 $a_{t:t+N}$。本文将其扩展为联合预测三个目标：

$$x_0 = \{ a_{t:t+N}, \mathbf{f}_{t+N}, P_{t+N} \}$$

其中 $\mathbf{f}_{t+N}$ 为未来时刻的三维几何潜变量，$P_{t+N} = \operatorname{Dec}(\mathbf{f}_{t+N})$ 为解码后的稠密三维点图。训练损失联合优化三者的L1误差（Eq. 7），迫使策略在生成动作时必须同时推理场景的三维未来状态。消融实验证实，移除未来点图预测后平均成功率从25.1%降至23.6%（Table 4），验证了这一联合预测是性能的核心驱动力。

### 状态表示的多模态融合

不同于基线方法使用单一的2D特征或3D点特征，本文构建了**几何-语义-本体多模态融合上下文**：三维几何特征（来自π3）、二维语义特征（来自DINOv3）和机器人本体感知状态（经MLP编码）通过Transformer融合为统一的条件表示，再馈入联合去噪解码器（DETR decoder结构）。消融表明，仅使用二维语义或仅使用三维几何特征均导致性能下降，证实了多模态互补的必要性。

### 数据效率的结构性优势

预训练基础模型的引入带来了显著的数据效率提升。Figure 4显示，本文方法在低数据量下即超越二维方法，且随着数据增加持续优于DP3。这一优势源于预训练模型已编码丰富的几何与语义先验，使策略学习无需从零构建空间理解。

GAP 是一个多模态条件生成模型，其核心设计目标是在不依赖显式点云或复杂标定的条件下，赋予双臂操作策略显式的三维几何推理能力。如图2所示，系统以时序RGB图像和本体感知状态为输入，通过三条并行的感知通路提取互补特征，经Transformer融合后，由一个联合扩散解码器同时预测未来动作块和未来三维几何潜变量。

### 输入与感知通路

在每个时间步 $t$，模型接收三类输入：
1. **历史RGB帧序列** $V$：提供时序上下文，用于捕捉场景动态变化；
2. **当前RGB帧** $I_t$：作为语义和几何感知的即时观测；
3. **本体感知状态** $p_t$：描述双臂关节角度、末端位姿等机器人内部状态。

这三类输入分别进入三条并行的编码器通路：

- **三维几何编码器（π3）**：一个预训练的三维几何基础模型，从时序RGB中提取几何感知潜变量，无需显式点云或相机标定即可获得场景的三维结构信息。
- **二维语义编码器（DINOv3）**：一个预训练的视觉基础模型，从当前帧中提取语义级二维特征，捕获物体类别、纹理等外观信息。
- **状态编码器（MLP）**：将本体感知状态映射为紧凑的机器人状态嵌入。

### 多模态融合

三条通路输出的几何特征、语义特征和状态嵌入被送入一个**语义-几何融合Transformer**。该模块通过交叉注意力机制将异构特征融合为统一的条件上下文表示，使后续的去噪过程能够同时感知场景的三维结构、二维语义和机器人当前姿态。

### 联合去噪与预测

融合后的条件上下文驱动一个基于DETR decoder的**联合动作-几何去噪器**。该扩散模型在训练时学习从噪声中恢复干净的目标 $x_0 = \{ a_{t:t+N}, \mathbf{f}_{t+N}, P_{t+N} \}$，包含三个分量：

- **动作块** $a_{t:t+N}$：未来 $N$ 步的双臂动作序列，由Action MLP Head解码；
- **三维几何潜变量** $\mathbf{f}_{t+N}$：未来时刻的场景几何压缩表示；
- **稠密点图** $P_{t+N} = \operatorname{Dec}(\mathbf{f}_{t+N})$：由Dense Head将潜变量解码为带有 $(x, y, z)$ 坐标和置信度的稠密三维点图。

推理时，模型从随机噪声出发，经 $K$ 步迭代去噪得到最终预测 $\hat{x}_0 = \{ \hat{a}_{t:t+N}, \hat{\mathbf{f}}_{t+N}, P_{t+N} \}$，仅执行动作块的前几步后重新规划，实现闭环控制。

### 设计要点

这一框架的关键创新在于**联合预测动作与未来几何**：策略在生成动作的同时必须“想象”场景三维结构的演变，从而获得物理一致的空间感知。预训练基础模型的引入使得系统在仅使用RGB输入的条件下即可实现三维感知的预测性控制，彻底规避了传统方法中点云采集、相机标定和工作空间预设等工程负担。

![[assets/figures/papers/paper_list_l2633_https_arxiv_org_abs_2602_23814/figures/001_Figure_1.jpg]]
*Figure 1: Paradigm Comparison. 2D-based methods learn implicit 3D representations from multi-view RGB observations, relying purely on 2D cues. 3D-based methods require camera calibration and preset workspaces to crop point clouds, which limits generalization and scalability. In contrast, our approach leverages powerful 2D and 3D pretrained priors to achieve semantic–geometric fusion perception, enabling robust action and geometry joint prediction without strict calibration or workspace constraints*

![[assets/figures/papers/paper_list_l2633_https_arxiv_org_abs_2602_23814/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. Given a sequence of past RGB frames, the current image, and proprioceptive state, our model extracts 3D geometric features, 2D semantic features, and robot state embeddings through three parallel encoders. These signals are fused by a Transformer into a unified semantic and geometric context that conditions a joint denoising process. A conditional diffusion decoder then predicts both a future action chunk and a future 3D latent, which is further decoded into a dense pointmap*

### 问题形式化

GAP将双臂操作建模为条件生成问题。一条演示轨迹定义为观测、本体感知状态与双臂动作的序列：

$$\tau_i = \{ (o_1, p_1, a_1), \ldots, (o_L, p_L, a_L) \} \tag{1}$$

其中 $o_t$ 为时刻 $t$ 的环境观测，$p_t$ 为机器人本体感知状态（关节角度、末端执行器位姿等），$a_t$ 为双臂动作指令。策略 $\pi$ 根据当前观测和本体感知预测长度为 $N$ 的未来动作块：

$$\pi(o_t, p_t) \rightarrow a_{t:t+N} \tag{2}$$

### 多模态感知编码器

GAP的核心创新在于将三维几何先验注入模仿学习管道。模型在每个时间步接收三类输入：(i) 历史RGB帧序列 $V$，(ii) 当前RGB帧 $I_t$，(iii) 当前本体感知状态 $p_t$。这些输入并行通过三个编码器：

- **Geometry 3D Encoder (π3)**：预训练的三维几何基础模型，从时序RGB中提取几何感知潜变量，捕获场景的空间结构信息。
- **Semantics 2D Encoder (DINOv3)**：预训练的二维语义基础模型，从当前帧提取语义特征，提供物体类别和外观信息。
- **State Encoder (MLP)**：将本体感知状态编码为机器人状态嵌入。

### 语义-几何融合

三个编码器的输出通过一个Transformer融合模块整合为统一的条件上下文。该模块执行跨注意力操作，使几何潜变量、语义特征和本体感知嵌入相互增强，形成多模态融合表征。这一融合上下文随后作为条件信号输入扩散去噪过程。

### 联合动作-几何去噪

GAP的预测目标超越传统动作分块策略。除未来动作块 $a_{t:t+N}$ 外，模型同时预测未来时刻的三维几何潜变量 $\mathbf{f}_{t+N}$，该潜变量可通过稠密头解码为未来三维点图：

$$P_{t+N} = \operatorname{Dec}(\mathbf{f}_{t+N}) \tag{3}$$

点图 $P_{t+N}$ 包含每个像素对应的 $(x, y, z)$ 坐标及置信度，构成对场景未来几何状态的显式预测。

训练时，干净的预测目标由三部分组成：

$$x_0 = \{ a_{t:t+N}, \mathbf{f}_{t+N}, P_{t+N} \} \tag{4}$$

前向扩散过程在任意噪声步 $k$ 的闭式解为：

$$q(x_k \mid x_0) = \mathcal{N}(x_k; \sqrt{\bar{\alpha}_k} x_0, (1-\bar{\alpha}_k) \mathbf{I}) \tag{5}$$

去噪网络（基于DETR decoder架构）以融合上下文为条件，从噪声样本 $x_k$ 中恢复干净信号。训练损失联合优化三个目标的L1误差：

$$\mathcal{L} = \mathbb{E}_{k, x_0, \epsilon} \Big[ \|\hat{a}_{t:t+N} - a_{t:t+N}\|_1 + \lambda \|\hat{\mathbf{f}}_{t+N} - \mathbf{f}_{t+N}\|_1 + \gamma \|\hat{P}_{t+N} - P_{t+N}\|_1 \Big] \tag{7}$$

其中 $\lambda$ 和 $\gamma$ 为平衡各损失项的权重系数。

### 推理流程

推理时，从纯噪声出发，经 $K$ 步迭代去噪得到最终预测：

$$\hat{x}_0 = \{ \hat{a}_{t:t+N}, \hat{\mathbf{f}}_{t+N}, P_{t+N} \} \tag{8}$$

其中动作块 $\hat{a}_{t:t+N}$ 直接用于机器人控制，三维点图 $P_{t+N}$ 提供对未来场景几何的显式预测，但其本身不参与控制循环——其作用完全体现在训练阶段对感知表征的规约和塑造。

### 关键设计决策

1. **免标定RGB输入**：与DP3和G3Flow依赖相机标定和预设工作空间裁剪点云不同，GAP仅需RGB图像输入，彻底规避标定误差和空间约束。
2. **联合预测的规约效应**：未来点图预测并非用于在线规划，而是作为辅助任务迫使感知编码器学习几何一致的表征。消融实验证实，移除该预测目标后平均成功率从25.1%降至23.6%，验证了联合三维预测是性能的核心驱动力。
3. **伪真值离线提取**：训练所需的 $\mathbf{f}_{t+N}$ 和 $P_{t+N}$ 由预训练的π3模型离线预提取，这增加了训练流程的复杂性，且对预训练模型的稳定性敏感——这是方法的一个已知局限。

## 实验与关键发现

### 核心发现与定量结果

本文在RoboTwin 2.0仿真基准和真实机器人平台上对GAP进行了系统评估。实验围绕三个核心问题展开：(1) 预训练三维几何骨干能否从纯2D输入中实现优越的三维感知？(2) 联合预测未来三维点图是否为关键设计？(3) 方法能否泛化至真实世界双臂任务？

**仿真基准表现。** 在RoboTwin 2.0的三类任务上，GAP均取得领先或极具竞争力的结果。在优势手选择任务（Dominant-select，16个任务）上，GAP平均成功率达**63.2%**，优于DP3（61.2%）和G3Flow（60.7%）（Table 1）。在同步双臂任务（Sync-bimanual，8个任务）上，GAP以**51.3%**的平均成功率超越Xu et al.（47.6%）和G3Flow（45.8%）（Table 2）。在顺序协调任务（Seq-coordinate，8个任务）上，GAP取得**50.4%**的平均成功率（Table 3）。值得注意的是，在部分高难度任务上优势尤为显著：悬挂杯子（Hang Mug）任务中，GAP成功率达**40.0%**，而G3Flow仅为26.7%（+13.3%）；放置双鞋（Place Dual Shoes）任务中，GAP为**43.3%**，远超DP3的17.7%（+25.6%）。这些结果表明，显式预测未来三维几何结构对于需要精细空间协调的双臂操作至关重要。

**真实世界验证。** 在AgileX Cobot Magic双臂平台上（配备三台RealSense D435i相机），GAP在四项真实任务上取得**40.0%**的平均成功率，显著优于ACT（23.8%）、DP（25.0%）和Xu et al.（32.5%）（Table 5）。仿真到真实的无缝迁移验证了预训练几何先验的鲁棒性——GAP无需相机标定或工作空间预设即可在真实环境中有效运作。

**数据效率。** 得益于预训练基础模型提供的强先验，GAP在低数据区间（≤50条演示）即显著超越二维方法，并随着数据增加持续超越DP3（Figure 4）。这表明几何感知的预测性建模有效缓解了模仿学习对大规模演示数据的依赖。

### 消融实验：联合几何预测的关键作用

为验证各设计选择的贡献，本文在四项代表性任务上进行了系统消融（Table 4）。完整GAP模型平均成功率为**25.1%**。移除未来三维点图预测分支后，性能降至**23.6%**（-1.5%），直接证实联合预测未来几何结构是性能的核心驱动力。进一步地，仅使用二维语义特征或仅使用三维几何特征均导致性能下降，表明多模态融合对空间感知和语义理解的互补不可或缺。这些结果与核心假设一致：迫使策略在生成动作的同时“想象”场景几何的演变，能赋予其物理一致的空间感知能力。

![[assets/figures/papers/paper_list_l2633_https_arxiv_org_abs_2602_23814/figures/008_Table_4.jpg]]
*Table 4: Ablation study. Impact of removing key components on the average success rate on four tasks*

### 失败模式分析

尽管GAP在多数任务上表现优异，分析揭示了以下典型失败模式：

1. **长期时序一致性不足。** 模型仅预测单步的未来点图，缺乏持久的三维记忆。在需要多步累积推理的顺序协调任务中，该限制可能导致空间状态漂移和动作失准。
2. **伪真值依赖的脆弱性。** 训练所需的三维潜变量伪真值需离线预提取，该过程对预训练几何模型的稳定性敏感。当预训练模型在特定视角或物体上产生噪声估计时，伪真值质量下降，进而影响策略学习。
3. **特定任务的不稳定性。** 在Open Microwave等任务上，训练过程中出现NaN错误，暗示几何潜变量在某些场景下可能发生数值不稳定。该问题需进一步诊断。

### 局限与未来方向

本文方法存在两个主要局限：(1) 仅预测单步未来点图，缺乏持久三维记忆以支持长程规划；(2) 伪真值三维潜变量需离线预提取，增加了训练流程复杂性。未来工作可探索多步三维轨迹预测以提升时序一致性，以及在线生成伪真值以简化训练流程。推广至未见任务和物体的泛化能力亦是重要的开放问题。

![[assets/figures/papers/paper_list_l2633_https_arxiv_org_abs_2602_23814/figures/004_Table_1.jpg]]
*Table 1: Comparison on Dominant-select Tasks (16 tasks). Single-arm manipulation tasks requiring appropriate arm selection. We report the mean and standard deviation of success rates averaged over 3 random seeds. Best score in bold, second-best underlined*

![[assets/figures/papers/paper_list_l2633_https_arxiv_org_abs_2602_23814/figures/005_Table_2.jpg]]
*Table 2: Comparison on Sync-bimanual Tasks (8 tasks). Bimanual tasks requiring synchronized coordinated operation. We report the mean and standard deviation of success rates averaged over 3 random seeds. Best score in bold, second-best underlined*

![[assets/figures/papers/paper_list_l2633_https_arxiv_org_abs_2602_23814/figures/006_Table_3.jpg]]
*Table 3: Comparison on Seq-coordinate Tasks (8 tasks). Sequential coordination tasks requiring multi-step bimanual cooperation. We report the mean and standard deviation of success rates averaged over 3 random seeds. Best score in bold, second-best underlined*

## 定位与知识库关联

**GAP** 处于双臂模仿学习中“二维隐式几何”与“三维显式点云”两条技术路线的交叉地带，其核心贡献在于用预训练三维几何基础模型替代昂贵且不可靠的标定点云，同时保留三维空间感知能力。

### 与基线方法的关系

**二维模仿学习基线**：**ACT**（Zhao et al., arXiv 2023）和 **Diffusion Policy (DP)**（Chi et al., IJRR 2023）均以多视角RGB图像为输入，通过动作分块或扩散去噪生成未来动作序列。这类方法依赖二维视觉特征隐式学习三维空间关系，缺乏显式的几何推理机制，在需要精确空间协调的双臂任务中表现受限。GAP 继承了扩散策略的动作分块预测范式（Eq. 2），但将感知骨干从从头训练的ResNet替换为预训练的π3几何模型，从根本上改变了空间感知的质量。

**三维点云基线**：**DP3**（Ze et al., RSS 2024）将扩散策略扩展到三维域，通过点云编码器直接操作标定点云数据，利用显式三维几何信息提升策略精度。**G3Flow**（Chen et al., CVPR 2025）进一步融合语义与几何特征，但仍依赖外部标定和预设工作空间来裁剪点云。GAP 与这两者的关键分水岭在于输入模态：GAP 仅需RGB时序图像，无需任何显式点云或相机标定，通过预训练几何模型从二维观测中提取三维几何潜变量，彻底规避了点云获取的工程复杂性和可靠性问题。

**双臂协调基线**：**Xu et al.**（CVPR 2025）和 **RDT**（Liu et al., arXiv 2024）分别从扩散驱动协调和大规模Transformer架构角度解决双臂操作。GAP 在同步双臂任务上以51.3%的平均成功率超越 Xu et al. (47.6%) 和 G3Flow (45.8%)（Table 2），在悬挂杯子等顺序协调任务上领先 G3Flow 达13.3个百分点，表明几何先验对双臂空间协同具有实质增益。

### 适用边界

GAP 的适用性受以下因素约束：

1. **任务类型**：方法在需要空间推理的双臂任务上增益显著（如 Place Dual Shoes 任务领先 DP3 达25.6%），但在简单单手选择任务上相对 DP3 的优势仅为2.0%（63.2% vs 61.2%），边际收益有限。

2. **数据效率**：得益于预训练特征，GAP 在低数据量场景下优于二维方法，且随数据增加持续超越 DP3（Figure 4）。但伪真值三维潜变量需离线预提取，训练流程对预训练模型的稳定性敏感。

3. **几何预测范围**：模型仅预测单步未来点图 $P_{t+N}$，缺乏持久的三维记忆机制，限制了需要长期状态累积和推理的任务场景。

### 局限与开放问题

**已知局限**：
- 未来三维点图预测仅覆盖单个时间步，无法形成多步三维轨迹，时序一致性受限。
- 伪真值三维潜变量依赖离线预提取，增加训练流程复杂度，且对π3模型的版本和稳定性敏感。

**开放问题**：
- 能否将预测扩展至多步三维轨迹，以提升长程规划能力和时序一致性？
- 如何在线生成伪真值三维潜变量，简化训练流程并提升对预训练模型变化的鲁棒性？
- 方法能否推广至未见任务和物体类别，实现更强的泛化能力？当前实验仅在RoboTwin 2.0固定任务集和有限真实场景上验证，跨域泛化能力尚待检验。

## 原文 PDF

![[paperPDFs/CVPR_2026/Action_Geometry_Prediction_with_3D_Geometric_Prior_for_Bimanual_Manipulation.pdf]]

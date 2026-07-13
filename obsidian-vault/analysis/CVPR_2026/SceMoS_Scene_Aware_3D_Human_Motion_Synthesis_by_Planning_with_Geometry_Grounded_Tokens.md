---
title: "SceMoS: Scene-Aware 3D Human Motion Synthesis by Planning with Geometry-Grounded Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_Grounded_Tokens.pdf
project_link: https://anindita127.github.io/SceMoS/
code_link: null
aliases:
- SceMoS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将全局规划（BEV图像+DINOv2特征）与局部执行（2D高度图+条件VQ-VAE解码）显式分解，并引入轨迹细化模块，以轻量级2D表示替代密集3D监督。
primary_logic: 与人类中心几何对齐的适当2D投影为物理扎根的3D运动合成提供了强大且可扩展的基础，BEV捕捉空间布局和可供性，高度图嵌入表面接触物理。
claims:
- SceMoS在TRUMANS数据集上达到FID 0.31，优于所有基线（最佳基线TRUMANS为0.34），且场景编码参数减少95%以上（~4M vs ~86M）
- "移除局部高度图条件（A1: Scene-agnostic VQ-VAE）导致重建MPJPE从21.88mm增至25.89mm，接触得分从0.99降至0.86，穿透均值从1.83升至4.43"
- "解耦规划器-解码器的两阶段设计（A5: Single stage transformer）使FID从0.31退化到0.78，接触得分0.61"
- 用户研究显示SceMoS的真实感评分为3.41±0.2，语义评分为4.20±0.6，均显著高于其他生成方法
---

# SceMoS: Scene-Aware 3D Human Motion Synthesis by Planning with Geometry-Grounded Tokens

> [!tip] 核心洞察
> 与人类中心几何对齐的适当2D投影为物理扎根的3D运动合成提供了强大且可扩展的基础，BEV捕捉空间布局和可供性，高度图嵌入表面接触物理。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceMoS：基于几何标记的场景感知三维人体运动合成 |
| 英文题名 | SceMoS: Scene-Aware 3D Human Motion Synthesis by Planning with Geometry-Grounded Tokens |
| 会议/期刊 | CVPR 2026 |
| Links | [Project](https://anindita127.github.io/SceMoS/) · [paper](https://arxiv.org/abs/2602.20476) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SceMoS |
| Dataset | TRUMANS |

> [!tip] 效果简介
> - TRUMANS 上，FID↓ 0.31 vs 0.34 (TRUMANS) (-0.03)；Penetration mean↓ 1.81 vs 1.83 (TRUMANS) (-0.02)；Contact↑ 0.98 vs 0.98 (TRUMANS) (0.00)。

## 概要

### 问题与瓶颈

场景感知的三维人体运动合成（Scene-aware 3D Human Motion Synthesis）要求模型同时完成三项紧密耦合的子任务：感知复杂的三维场景几何、规划空间意图、以及执行精细的身体-场景交互。现有方法通常采用单一端到端模型在纠缠的动画生成过程中完成所有这些任务，因而高度依赖昂贵的3D场景编码器——如体素网格（voxel grids）或点云（point clouds）——导致计算开销巨大且表示高度冗余。例如，**TRUMANS**（Jiang et al., CVPR 2024）使用体素化的3D占用网格作为场景条件，其可训练场景编码参数高达~86M。这种密集的3D监督不仅限制了模型的可扩展性，也使得全局路径规划与局部接触推理之间的解耦变得困难。

### 核心思路

SceMoS 的核心洞察在于：**与人体中心几何对齐的适当2D投影，能够为物理扎根的3D运动合成提供强大且可扩展的基础**。具体而言，鸟瞰图（BEV）擅长捕捉全局空间布局与可供性（affordance），而局部2D高度图则能有效嵌入表面接触的物理约束。基于这一认知，SceMoS将场景感知运动合成显式分解为两个阶段：

1. **全局运动规划器（Global Motion Planner）**：以文本指令和从BEV图像中提取的DINOv2特征为条件，自回归地预测离散运动标记序列，负责高层语义意图和空间路径规划。
2. **几何扎根运动标记器（Geometry-Grounded Motion Tokenizer）**：学习一个以局部2D高度图为条件的VQ-VAE，将离散标记解码为连续3D运动，并配备轻量级轨迹细化模块以优化根关节轨迹。

这一解耦设计使得SceMoS能够以极轻量的2D场景表示（可训练场景参数仅~4M，较基线减少95%以上）替代密集的3D监督，同时保持甚至超越现有方法的运动质量。

### 主要结果

在TRUMANS数据集上，SceMoS取得了FID 0.31的最优生成质量（最佳基线TRUMANS为0.34），并在穿透均值（1.81 vs. 1.83）和接触得分（0.98持平）等物理合理性指标上表现相当或更优。消融实验证实了每一设计选择的决定性作用：

- **移除局部高度图条件（A1）**：重建MPJPE从21.88mm升至25.89mm，接触得分从0.99降至0.86，穿透均值从1.83升至4.43，表明2D高度图对于精细接触推理不可或缺。
- **移除两阶段解耦（A5）**：将规划与执行合并为单阶段Transformer后，FID从0.31退化至0.78，接触得分降至0.61，验证了全局规划与局部执行分离的必要性。
- **移除轨迹细化（A7）**：FID升至0.53，接触得分降至0.79，MPJPE升至26.89mm，凸显了根轨迹优化对整体运动质量的关键贡献。

用户研究进一步表明，SceMoS在真实感（3.41±0.2）和语义对齐（4.20±0.6）两个维度上均显著优于所有生成式基线方法。

### 方法定位与知识库贡献

SceMoS在场景感知运动合成的方法谱系中占据了一个独特的位置：它在表示效率与生成质量之间实现了新的平衡。与依赖3D体素网格的**TRUMANS**或依赖3D点云的**SceneDiffuser**相比，SceMoS以2D BEV+高度图实现了参数量的数量级压缩；与使用2D平面图的**TeSMo**（Yi et al., ECCV 2024）相比，SceMoS通过DINOv2特征和高度图分别增强了语义理解和物理接触建模；与语言条件的**Humanise**（Wang et al., NeurIPS 2022）相比，SceMoS的几何扎根标记器提供了更强的场景约束。

其知识库贡献可归纳为三个层面：
- **表示层面**：证明了2D BEV+高度图的组合足以替代密集3D场景表示用于运动合成，且具有更好的参数效率。
- **架构层面**：建立了“全局规划-局部执行”解耦范式，并通过离散运动标记桥接两个阶段。
- **物理扎根层面**：展示了以人为中心的局部高度图作为接触条件，能够显著提升运动的物理合理性（穿透、接触指标）。

**场景感知三维人体运动合成**（Scene-aware 3D Human Motion Synthesis）旨在生成与给定三维环境几何一致且语义合理的人体动作序列，是具身人工智能、虚拟角色动画和人机交互领域的核心任务。其核心挑战在于：模型必须同时完成三项相互纠缠的子任务——感知复杂的场景几何、规划空间导航意图、以及执行精细的物理接触与过渡动作。

**现有方法的瓶颈**在于架构设计上的“纠缠”。当前主流方法，如 **TRUMANS**（Jiang et al., CVPR 2024）和 **SceneDiffuser**，通常采用单阶段端到端模型，将场景感知、运动规划和局部执行压缩在同一个推理过程中。为支持这一过程，它们依赖昂贵的三维场景编码器——例如体素网格（voxel grids）或点云（point clouds）——来提供密集的三维几何监督。这带来了两个直接后果：

1. **高计算成本**：三维场景编码器的可训练参数量通常在 50M 至 86M 量级（如 TRUMANS 约 86M），严重限制了模型的可扩展性和训练效率。
2. **表示冗余**：密集的三维表示包含大量与人体运动无关的几何细节，迫使模型在单一推理步骤中隐式地学习从全局语义到局部物理约束的全部映射，导致优化困难。

**本文的动机**源于一个关键洞察：与人类中心几何对齐的适当二维投影，可以为物理扎根的三维运动合成提供强大且可扩展的基础。具体而言，鸟瞰图（Bird’s-Eye-View, BEV）天然捕捉了场景的空间布局和可供性（affordances），而局部二维高度图（heightmap）则嵌入了表面接触的物理约束。这一洞察指向了一种解耦的可能——将全局规划与局部执行显式分离，用轻量级二维表示替代密集的三维监督。

基于此，SceMoS 提出了一种**两阶段解耦框架**：第一阶段由文本条件和 BEV 场景特征驱动的自回归全局运动规划器，负责预测离散的运动标记序列；第二阶段由几何扎根的运动标记器（Geometry-Grounded Motion Tokenizer）将离散标记解码为连续运动，并通过局部高度图条件实现精细的物理接触推理。这一设计从根本上改变了场景表示与运动合成之间的交互方式，使得场景编码参数量降低一个数量级以上（约 4M），同时保持甚至提升了运动质量。

## 核心方法与创新机理

SceMoS 的核心创新在于将场景感知的人体运动合成问题从“单一纠缠的动画过程”解耦为**全局规划**与**局部执行**两个阶段，并通过轻量级 2D 几何表示替代昂贵的 3D 场景编码。这一设计直接回应了现有方法的根本瓶颈：在单阶段模型中同时感知复杂几何、规划空间意图和执行精细运动，导致对密集 3D 监督（如体素网格、点云）的强依赖，带来高计算成本和冗余表示。

### 解耦的两阶段架构

现有主流方法（如 **TRUMANS**，Jiang et al., CVPR 2024；**SceneDiffuser**）普遍采用单阶段端到端范式，全局空间推理与局部接触执行纠缠在同一模型中。SceMoS 将这一过程显式分解（**Table 1 (A5)** 提供关键证据）：

- **全局运动规划器**（自回归 Transformer Decoder）：以文本嵌入和 BEV 图像的 DINOv2 特征为条件，自回归预测离散运动标记序列 $\{z_i\}$。该阶段仅关注高层语义与空间布局规划，不涉及精细几何。
- **几何扎根运动标记器**（条件 VQ-VAE）：学习一个场景感知的离散运动码本，以局部 2D 高度图为条件将离散标记解码为连续 3D 运动。高度图以角色根关节为中心、按面向方向计算，嵌入表面接触物理。

消融实验 **A5**（单阶段 Transformer）显示：移除解耦设计后，FID 从 0.31 退化至 0.78，接触得分从 0.98 骤降至 0.61，穿透均值从 1.81 升至 3.19。这证实了规划与执行纠缠是性能瓶颈的核心因果节点。

### 轻量级 2D 场景表示替代密集 3D 编码

SceMoS 在场景表示上做出了激进但有效的简化，涉及两个关键 changed slots：

| 表示层面 | 基线方法 | SceMoS 设计 | 证据锚点 |
|---------|---------|------------|---------|
| 全局场景表示 | 3D 体素网格 / 点云 | 2D BEV 图像 + 冻结 DINOv2 特征 | Sec 3.1, Table 1 |
| 局部几何表示 | 无或全 3D 占用 | 2D 局部高度图（32×32 网格） | Sec 3.1, Table 2 |

**参数效率的革命性提升**：SceMoS 的场景编码可训练参数仅约 4M（冻结 DINOv2 + 线性投影），而 TRUMANS 的 3D 体素网格编码器需约 86M 参数，参数减少超过 95%（**Table 1**）。这一优势源于核心洞察：与人类中心几何对齐的适当 2D 投影，为物理扎根的 3D 运动合成提供了强大且可扩展的基础——BEV 捕捉空间布局和可供性，高度图嵌入表面接触物理。

**高度图的决定性作用**：消融实验 **A1**（移除高度图条件，即场景无关 VQ-VAE）显示，重建 MPJPE 从 21.88mm 升至 25.89mm，接触得分从 0.99 降至 0.86，穿透均值从 1.83 升至 4.43（**Table 2**）。与 3D 体素网格替代方案（**A3**）相比，高度图在穿透和接触指标上更优，且参数更少。分辨率实验（**A2a/A2b**）表明 32×32 达到最佳权衡。

**视觉骨干的选择**：用 CLIP 特征替代 DINOv2（**A6**）导致 FID 升至 0.81，接触得分降至 0.91，表明 DINOv2 的自监督视觉特征对场景语义理解具有不可替代性。

### 轨迹细化模块

SceMoS 引入轻量级 1D CNN 回归器，从局部关节运动特征预测平滑的根轨迹速度，以 L1 损失同时优化绝对根位置和根速度（Eq. 7）。该模块替代了传统方法中缺乏物理约束的根轨迹生成。移除该模块（**A7**）导致 FID 升至 0.53，接触得分降至 0.79，MPJPE 升至 26.89mm（**Table 1 & Table 2**），证实在解耦架构中显式建模根轨迹物理一致性对最终运动质量至关重要。

### 创新点的协同效应

上述三个 changed slots 并非孤立改进，而是形成因果链：2D 轻量表示使解耦成为可能（全局规划无需承载精细几何），解耦又为轨迹细化提供了清晰的介入点（在解码后修正根运动）。**Table 1** 的完整结果显示，SceMoS 在 TRUMANS 数据集上达到 FID 0.31，优于所有基线（最佳基线 TRUMANS 为 0.34），同时将场景编码参数削减一个数量级。用户研究（**Table A.1**）进一步验证了生成运动的真实感（3.41±0.2）和语义对齐度（4.20±0.6）均显著优于其他生成方法。

SceMoS 将文本条件的场景感知人体运动合成解耦为两个阶段：**全局运动规划**与**几何扎根的局部执行**。该设计的核心动机在于，现有方法在单一纠缠的动画过程中同时感知复杂几何、规划空间意图并执行精细运动，这不仅需要昂贵的 3D 场景编码器（如体素网格或点云），还导致了高计算成本和冗余表示。SceMoS 通过显式分解规划与执行，以轻量级 2D 场景线索替代密集 3D 监督，从根本上改变了这一范式。

### 输入与场景表示

系统接受三类输入：文本指令、场景的鸟瞰图 (BEV) 渲染图像，以及以角色根关节为中心的局部 2D 高度图。文本指令经 T5 编码器转换为条件特征 $F_{\text{text}}$。BEV 图像从场景的升高角落渲染，通过冻结的 DINOv2 提取补丁特征作为全局场景表示 $F_{\text{dino}}$，捕捉空间布局与可供性。局部高度图 $H$ 则嵌入表面接触物理，为精细交互生成提供几何条件。这三种表示共同构成了从高层语义到低层几何的完整场景理解链。

### 两阶段流水线

**第一阶段：全局运动规划器。** 规划器是一个自回归 Transformer 解码器，以 $F_{\text{text}}$ 和 $F_{\text{dino}}$ 为条件前缀，逐令牌预测离散运动标记序列 $\{z_i\}$。这些标记来自几何条件 VQ-VAE 学习到的离散运动词汇，每个标记对应一段短时运动片段。规划器通过交叉熵损失最大化真实标记的对数似然：

$$\mathcal{L}_{plan} = - \sum_{i=1}^{\hat{n}} \log P(\boldsymbol{z}_i = \boldsymbol{z}_i^{*} | \boldsymbol{Z}_{<i}, F_{\mathrm{text}}, F_{\mathrm{dino}})$$

训练时采用无分类器引导 (CFG)，以固定概率随机丢弃 $F_{\text{text}}$ 和 $F_{\text{dino}}$，增强条件控制能力。

**第二阶段：几何扎根运动标记器。** 该模块由 VQ-VAE 实现，包含编码器、量化码本和交互解码器。编码器将连续运动序列压缩为潜在向量，经码本量化得到 $Z_q$。交互解码器以 $Z_q$ 和局部高度图 $H$ 为输入，重建连续 3D 人体运动 $\hat{X} = \mathbf{D}(Z_{\mathrm{q}}, H)$。高度图以当前运动令牌最后帧的根位置为中心计算，确保局部几何条件与运动状态因果一致。VQ-VAE 的复合损失函数为：

$$\mathcal{L}_{VQ} = \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}} + \beta || \mathbf{sg}[Z_{\mathrm{q}}] - Z ||_2$$

其中重建项 $\mathcal{L}_{\mathrm{rec}}$ 涵盖姿态参数的各分量，承诺项约束码本学习。

### 推理循环与轨迹细化

推理时，规划器自回归采样运动令牌序列。每解码一个令牌，系统根据上一令牌最后帧的根位置重新计算局部高度图，再馈入交互解码器生成当前运动片段。这一“规划-重计算-解码”循环（见 Figure 3）使 SceMoS 能够在长距离运动合成中保持全局连贯与局部可行。

解码完成后，一个轻量级 1D CNN 轨迹细化模块从局部关节运动特征预测平滑的根轨迹速度，替换原始根位移 $t_{\delta}$。该模块通过 L1 损失同时优化绝对根位置和根速度：

$$\mathcal{L}_{\mathrm{traj}} = \lambda_{\mathrm{r}} \left|\left| t_{\delta} - \hat{t}_{\delta} \right|\right|_{1} + \lambda_{\mathrm{v}} \left|\left| \Delta t_{\delta} - \Delta \hat{t}_{\delta} \right|\right|_{1}$$

这一后处理步骤有效减少了足部滑动伪影，提升了接触一致性（消融实验 A7 移除该模块后，FID 从 0.31 升至 0.53，接触得分从 0.98 降至 0.79）。

### 模块关系总结

整个流水线的信息流可概括为：文本 + BEV 图像 → 全局规划器 → 离散运动令牌 → VQ-VAE 解码器（结合局部高度图）→ 连续运动 → 轨迹细化 → 最终 3D 运动。规划器负责“去哪里、做什么”的高层决策，标记器负责“如何落脚、如何接触”的低层执行，二者通过离散令牌解耦，既降低了场景编码的参数量（约 4M vs. 基线的 50M–86M），又保持了运动质量。

![[assets/figures/papers/paper_list_l1753_SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_G/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SceMoS framework. SceMoS disentangles text-conditioned scene-aware human motion synthesis into two stages. (a) The global motion planner predicts discrete motion tokens from text input and DINOv2 scene features extracted from a BEV image. (b) Our geometry-grounded motion tokenizer learns a scene-aware motion vocabulary for mapping these discrete tokens to a continuous 3D human motion. We use 2D local heightmaps around poses to condition our interaction decoder (top right) for fine-grained interaction generation. The red dotted line implies used only during training. Blue arrows follow through the inference pipeline*

![[assets/figures/papers/paper_list_l1753_SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_G/figures/001_Figure_1.jpg]]
*Figure 1: The introduced scene-aware 3D human motion synthesis framework, SceMoS, uses 2D scene cues and text instructions to generate physically consistent and realistic 3D motions. We use a bird’s-eye-view (BEV) image rendered from an elevated corner of the input scene, and extract DINOv2 features for high-level semantic planning. For fine-grained contact reasoning, we use the local 2D heightmap of the scene around the root of the person’s initial pose*

### 问题形式化

SceMoS 将文本条件化的场景感知人体运动合成建模为一个映射问题。给定文本指令、场景几何以及角色初始姿态，目标是生成一段物理一致且语义合理的 3D 人体运动序列。每帧姿态由以下分量组成（Eq. 1）：

$$\boldsymbol{x}_i = \left[ t_{\delta}, j_{\mathrm{r}}, j_{\mathrm{p}}, j_{\mathrm{v}}, c_{\mathrm{f}} \right]_i$$

其中 $t_{\delta}$ 为当前帧相对于前一帧的根关节平移偏移量，$j_{\mathrm{r}}$ 为各关节的 6D 旋转表示，$j_{\mathrm{p}}$ 为关节局部偏移量，$j_{\mathrm{v}}$ 为关节速度，$c_{\mathrm{f}}$ 为脚部接触标志。整个运动序列表示为 $X = \{\boldsymbol{x}_1, \boldsymbol{x}_2, ..., \boldsymbol{x}_T\}$。

系统的总体映射函数为：

$$\mathcal{G} : ( F_{\mathrm{text}}, F_{\mathrm{dino}}, H ) \rightarrow X$$

其中 $F_{\mathrm{text}}$ 为 T5 文本编码器提取的文本特征，$F_{\mathrm{dino}}$ 为从鸟瞰图（BEV）图像中提取的 DINOv2 场景特征，$H$ 为以角色根关节为中心的局部 2D 高度图。

### 全局运动规划器

全局规划器是一个自回归 Transformer 解码器，其核心任务是根据紧凑的 2D 场景线索和文本指令预测离散运动标记序列。规划器以文本特征 $F_{\mathrm{text}}$ 和 DINOv2 场景特征 $F_{\mathrm{dino}}$ 作为前缀条件，逐帧自回归地采样运动标记 $\boldsymbol{z}_i$。训练损失为标准交叉熵，最大化真实标记的对数似然（Eq. 4）：

$$\mathcal{L}_{\mathrm{plan}} = - \sum_{i=1}^{\hat{n}} \log P(\boldsymbol{z}_i = \boldsymbol{z}_i^{*} | \boldsymbol{Z}_{<i}, F_{\mathrm{text}}, F_{\mathrm{dino}})$$

其中 $\boldsymbol{z}_i^{*}$ 为第 $i$ 个运动标记的真实值，$\boldsymbol{Z}_{<i}$ 为已生成的前序标记序列，$\hat{n}$ 为序列总长度。训练期间采用无分类器引导（CFG），以固定概率随机丢弃 $F_{\mathrm{text}}$ 和 $F_{\mathrm{dino}}$，以增强条件控制能力。

### 几何扎根运动标记器

几何扎根运动标记器是一个条件 VQ-VAE，负责学习场景感知的离散运动词汇，并将离散标记解码为连续 3D 人体运动。其核心设计在于交互解码器不仅接收量化潜在向量 $Z_{\mathrm{q}}$，还接收当前运动标记对应局部高度图 $H$ 作为几何条件，从而在解码阶段注入精细的接触物理信息。运动重建过程为：

$$\hat{X} = \mathbf{D}(Z_{\mathrm{q}}, H)$$

其中 $\mathbf{D}$ 为 1D 卷积交互解码器。VQ-VAE 的复合损失函数包含重建项和码本承诺项（Eq. 6）：

$$\mathcal{L}_{\mathrm{VQ}} = \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}} + \beta || \mathbf{sg}[Z_{\mathrm{q}}] - Z ||_2$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为原始运动与重建运动之间的重建损失，$\mathbf{sg}[\cdot]$ 表示停止梯度算子，$Z$ 为编码器输出的连续潜在表示，$Z_{\mathrm{q}}$ 为经码本量化后的离散潜在向量。承诺损失项促使编码器输出靠近码本向量，$\beta$ 为承诺损失权重。

### 轨迹细化模块

为减少脚部滑动伪影并提升接触一致性，SceMoS 引入了一个轻量级 1D CNN 轨迹细化模块。该模块从生成运动的局部关节运动特征中预测根关节速度偏移，并在推理阶段替换原始根轨迹。训练损失同时优化绝对根位置和根速度的 L1 误差（Eq. 7）：

$$\mathcal{L}_{\mathrm{traj}} = \lambda_{\mathrm{r}} \left|\left| t_{\delta} - \hat{t}_{\delta} \right|\right|_{1} + \lambda_{\mathrm{v}} \left|\left| \Delta t_{\delta} - \Delta \hat{t}_{\delta} \right|\right|_{1}$$

其中 $t_{\delta}$ 和 $\hat{t}_{\delta}$ 分别为真实和预测的根平移偏移量，$\Delta t_{\delta}$ 和 $\Delta \hat{t}_{\delta}$ 为对应的根速度，$\lambda_{\mathrm{r}}$ 和 $\lambda_{\mathrm{v}}$ 为位置和速度损失的权重系数。

### 推理循环中的高度图重计算

推理阶段，规划器自回归采样运动标记序列 $\boldsymbol{z}' = \{z_1', z_2', ..., z_{\hat{n}}'\}$，其中每个标记的采样分布为 $z_i' \sim P(z_i' | \boldsymbol{z}_{<i}', F_{\mathrm{text}}, F_{\mathrm{dino}})$。关键设计在于：解码当前标记时，局部高度图会以前一个标记解码出的最后一帧根位置为中心重新计算，从而维持因果一致性，使全局规划与局部几何执行始终保持同步。这一机制使 SceMoS 能够在杂乱室内环境中生成长距离、全局连贯且局部可行的运动（见 Figure 3）。

![[assets/figures/papers/paper_list_l1753_SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_G/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of long-range motion synthesis in a cluttered indoor environment. SceMoS performs geometry-grounded planning by recalculating heightmaps every t frames, enabling globally coherent yet locally feasible motion planning that respects scene geometry. The BEV image input is shown in the inset*

## 实验与关键发现

### 主实验结果

SceMoS 在 TRUMANS 数据集上与主流场景感知人体运动合成方法进行了定量比较，结果如 **Table 1** 所示。SceMoS 在运动生成质量的核心指标 FID 上达到 **0.31**，优于所有基线方法，包括基于 3D 体素占位网格的自回归扩散模型 **TRUMANS**（Jiang et al., CVPR 2024）的 0.34。在物理合理性方面，SceMoS 的穿透均值（Penetration mean↓）为 1.81，接触得分（Contact↑）为 0.98，与 TRUMANS 持平或略优，表明 2D 场景表示并未牺牲接触物理的精度。

![[assets/figures/papers/paper_list_l1753_SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_G/figures/004_Table_1.jpg]]
*Table 1: Quantitative Evaluation of Motion Generation. Comparison in terms of scene representation, number of parameters needed for scene encoding, final motion generation quality between baselines, ablated versions, and our full method on the TRUMANS dataset. Bold indicates best. Underline indicates second best*

更关键的是，SceMoS 将可训练场景编码参数从基线的约 86M（TRUMANS）大幅压缩至 **~4M**，降幅超过 95%。这一效率增益源于方法将全局场景理解委托给冻结的 DINOv2 骨干，仅训练轻量线性投影层，同时以 2D 高度图替代密集 3D 占位监督。在目标完成度指标上（**Table A.2**），SceMoS 的目标准确度（Goal Accuracy）和 R-Precision 同样表现最优，确认生成运动与文本指令的语义对齐性。

用户研究（**Table A.1**）提供了感知层面的佐证：SceMoS 的真实感评分为 **3.41±0.2**，语义评分为 **4.20±0.6**（5 分制），均显著高于其他生成方法，且超过 60% 的评分落在“Good/Excellent”区间（**Figure A.2**）。

### 消融实验

消融实验从架构解耦、场景表示和轨迹细化三个维度验证了 SceMoS 各模块的因果贡献。

**两阶段解耦的因果效应。** 将全局规划器与几何扎根解码器合并为单阶段 Transformer（A5: Single stage transformer）导致 FID 从 0.31 急剧退化至 **0.78**，接触得分降至 0.61，穿透均值升至 3.19（**Table 1**）。这一退化幅度揭示了核心瓶颈：单阶段模型被迫在同一个纠缠的动画过程中同时推理复杂空间布局和精细运动执行，而解耦设计允许规划器专注于高层意图（BEV+DINOv2），解码器专注于局部接触物理（高度图）。

**局部高度图条件的因果效应。** 移除高度图条件（A1: Scene-agnostic VQ-VAE）使重建 MPJPE 从 21.88mm 升至 **25.89mm**，接触得分从 0.99 降至 **0.86**，穿透均值从 1.83 升至 **4.43**（**Table 2**）。这表明高度图编码的表面接触物理是维持运动扎根性的关键信息通道，缺失后模型无法有效推断脚与地面的接触约束。

**轨迹细化模块的贡献。** 移除轨迹细化（A7）导致 FID 升至 **0.53**，接触得分降至 0.79，MPJPE 升至 26.89mm（**Table 1 & Table 2**）。该模块以轻量 1D CNN 从局部关节运动特征预测根轨迹速度，有效抑制了脚滑动伪影，是连接局部运动与全局位移的桥梁。

**视觉骨干的选择。** 用 CLIP 特征替代 DINOv2（A6）使 FID 升至 **0.81**，接触得分 0.91（**Table 1**）。CLIP 的全局图像级表示缺乏 DINOv2 的补丁级空间定位能力，难以捕捉 BEV 图像中物体布局与可供性之间的细粒度对应关系，这解释了语义规划能力的显著下降。

**高度图分辨率的影响。** 高度图分辨率 32×32 达到最佳权衡（MPJPE 21.88，MPJVE 10.45），16×16 和 64×64 均略差（**Table 2, A2a/A2b**）。分辨率过低丢失接触面细节，过高则引入噪声且增加计算开销，32×32 恰好平衡了空间精度与鲁棒性。

**高度图 vs 3D 体素网格。** 与 3D 体素网格（A3）相比，高度图在穿透和接触指标上更优，且参数更少（**Table 2**）。这一反直觉结果说明，以人为中心对齐的 2D 投影比稀疏 3D 占位网格更有效地嵌入接触相关的几何约束。

### 失败模式与局限性

尽管 SceMoS 在整体指标上表现优异，分析揭示了若干结构性局限：

1. **动态环境失效。** 方法假设静态场景，高度图在每一运动标记解码时重新计算，但无法处理移动物体或其他运动角色。在动态障碍物出现时，BEV 图像和高度图均无法反映时变几何，导致穿透或语义错位。

2. **细粒度物体交互不足。** 局部高度图设计仅编码地面和大型表面几何，无法表示小物体（如杯子、书本）的抓取可供性。当文本指令涉及“拿起桌上的杯子”时，模型缺乏目标物体的空间锚点，只能生成近似身体运动而忽略手部-物体接触。

3. **推理延迟较高。** 推理速度约为每 80 帧 8 秒，主要瓶颈在于自回归标记采样和高度图重计算。这限制了实时应用场景（如交互式角色动画）的部署。

4. **BEV 视角的遮挡盲区。** BEV 图像从单个角落渲染，可能丢失被遮挡区域的语义信息（如桌下空间、多层结构），在复杂室内外场景中存在泛化风险。当前仅在 TRUMANS 和 HUMANISE 数据集上验证，缺乏更多样化场景下的测试。

### 重要图表结论

- **Table 1** 确立了 SceMoS 在 FID 和参数效率上的双重优势，同时通过 A5/A6/A7 消融揭示了架构解耦、DINOv2 特征和轨迹细化的因果贡献。
- **Table 2** 从重建层面证明高度图条件是接触物理的核心信息瓶颈，其移除导致穿透均值从 1.83 飙升至 4.43。
- **Figure 3** 可视化了长距离运动合成中高度图重计算的机制：每 t 帧重新计算以根关节为中心的局部高度图，使规划器能够适应移动过程中变化的场景几何，实现全局连贯且局部可行的运动。
- **Figure 4** 的定性比较展示了 SceMoS 在“坐在椅子上”等典型交互场景中避免了基线的穿透和错位伪影（红圈标注），验证了 2D 表示在复杂接触推理中的有效性。

![[assets/figures/papers/paper_list_l1753_SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_G/figures/006_Table_2.jpg]]
*Table 2: Quantitative Evaluation of VQ Reconstruction. Comparison of motion reconstruction quality after tokenization across ablated versions on the TRUMANS dataset. Bold indicates the best performance*

![[assets/figures/papers/paper_list_l1753_SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_G/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of SceMoS with recent HSI models. SceMoS generates motions that are semantically aligned with the input text instructions while maintaining stable contact and smooth transitions. In contrast, we observe some penetrations and misalignment (red circle) in some frames of the baselines*

## 定位与知识库关联

### 核心定位：从3D密集编码到2D解耦规划

SceMoS的根本创新在于**将场景感知人体运动合成从“单阶段3D密集编码”范式迁移至“两阶段2D解耦规划”范式**。现有方法——无论是基于扩散的**SceneDiffuser**（使用3D点云条件）、**TRUMANS**（Jiang et al., CVPR 2024，使用体素化3D占用网格）、**TeSMo**（Yi et al., ECCV 2024，使用2D平面图），还是基于条件VAE的**Humanise**（Wang et al., NeurIPS 2022）——均在一个纠缠的动画过程中同时处理复杂几何感知、空间意图规划和精细运动执行。这种设计迫使模型依赖昂贵的3D场景编码器（如体素网格或点云），导致高计算成本（场景编码参数50M–86M）和表示冗余。

SceMoS通过**显式分解全局规划与局部执行**来打破这一瓶颈：
1. **全局规划器**：在BEV图像上提取DINOv2特征，结合文本嵌入，自回归预测离散运动标记序列，负责高层语义理解与空间路径规划。
2. **局部解码器**：以2D高度图（32×32网格）为条件，通过VQ-VAE将离散标记解码为连续运动，专注于精细的物理接触与执行。

这一设计的关键洞察是：**与人体中心几何对齐的适当2D投影，为物理扎根的3D运动合成提供了强大且可扩展的基础**——BEV捕捉空间布局与可供性，高度图嵌入表面接触物理。

### 与基线方法的关系图谱

| 方法 | 场景表示 | 架构范式 | 场景编码参数 | 核心局限 |
|------|----------|----------|-------------|----------|
| **Humanise** (Wang et al., NeurIPS 2022) | 语言条件，合成场景 | 单阶段cVAE | — | 缺乏显式几何条件，物理一致性弱 |
| **SceneDiffuser** | 3D点云 | 单阶段扩散 | ~50M | 密集3D编码，计算成本高 |
| **TRUMANS** (Jiang et al., CVPR 2024) | 3D体素占用网格 | 自回归扩散 | ~86M | 规划与执行纠缠，参数冗余 |
| **TeSMo** (Yi et al., ECCV 2024) | 2D平面图 | 文本控制扩散 | — | 仅用平面图，丢失高度与可供性信息 |
| **SceMoS** (本文) | BEV+DINOv2 + 局部高度图 | 两阶段解耦 | ~4M | 仅限静态场景，不支持精细物体交互 |

**SceMoS对基线的改进是系统性的**：
- 相比**TRUMANS**：场景编码参数减少95%以上（~4M vs ~86M），FID从0.34提升至0.31（Table 1），且通过解耦设计避免了单阶段模型（A5消融）导致的FID剧烈退化（0.78）。
- 相比**TeSMo**：BEV+DINOv2提供了比2D平面图更丰富的语义信息；当用CLIP特征替代DINOv2时（A6消融），FID升至0.81，接触得分降至0.91，验证了DINOv2的优越性。
- 相比**Humanise**：显式的几何条件（高度图）使接触得分从0.86（A1消融，移除高度图）提升至0.99，穿透均值从4.43降至1.83（Table 2）。

### 适用边界与局限

尽管SceMoS在TRUMANS和HUMANISE数据集上取得了领先性能，其设计存在明确的适用边界：

1. **静态场景假设**：当前框架仅考虑静态场景，未处理动态物体或其他运动角色。这限制了其在动态环境（如多人交互、移动家具）中的应用。

2. **细粒度物体交互缺失**：局部高度图设计仅关注身体-场景接触（如坐、躺、走），不足以建模精细物体交互（如抓取小物体、操作工具）。高度图本质上是2.5D表示，无法捕捉物体几何的完整3D结构。

3. **推理速度瓶颈**：推理速度约为每80帧8秒，难以满足实时应用需求。这源于自回归规划器的逐标记生成和高度图的重计算。

4. **BEV视角限制**：BEV图像从单个角落渲染，可能丢失某些场景遮挡的语义信息，不适用于多层建筑或复杂室内外混合场景。

5. **数据集泛化有限**：仅在TRUMANS和HUMANISE数据集上评估，缺乏在更多样化场景（如室外不规则地形、工业环境）下的泛化验证。

### 开放问题与未来方向

1. **动态环境扩展**：如何将SceMoS的2D解耦范式扩展到动态环境（移动物体、多智能体）以及室外不规则地形？可能需要引入时序场景表示或动态高度图更新机制。

2. **细粒度物体交互**：能否通过扩展2D表示（如多视角高度图、物体掩码）或引入轻量级3D局部特征来处理抓取与操作任务？当前高度图仅编码表面几何，缺乏物体语义信息。

3. **推理效率优化**：能否通过动态高度图缩放、自适应重计算频率或更高效的规划器（如并行解码）来降低推理延迟？轨迹细化模块的轻量级设计（1D CNN）已显示局部优化的有效性，类似思路可扩展至其他模块。

4. **离散标记的表示能力**：几何扎根的离散标记如何联合表现多样的交互行为（坐、躺、爬、倚靠）？能否通过增加码本大小或引入层次化标记来改进表示容量？

5. **视觉骨干的进化**：使用DINOv3或其他更强视觉骨干是否进一步提升语义理解，尤其是在未见过复杂场景下的泛化能力？A6消融已初步验证视觉特征质量对规划器性能的关键影响。

6. **多模态融合的深度**：当前BEV和高度图是独立提取的，是否可以通过跨模态注意力或联合学习来增强全局规划与局部执行之间的信息流动？

## 原文 PDF

![[paperPDFs/CVPR_2026/SceMoS_Scene_Aware_3D_Human_Motion_Synthesis_by_Planning_with_Geometry_Grounded_Tokens.pdf]]

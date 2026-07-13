---
title: "HumanScore: Benchmarking Human Motions in Generated Videos"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/HumanScore_Benchmarking_Human_Motions_in_Generated_Videos.pdf
project_link: "https://cs.stanford.edu/~xtiange/projects/humanscore/"
code_link: null
aliases:
- HumanScore
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 通过解构人体运动为解剖、运动学和动力学三个层次，并定义六项生物力学指标，能够揭示视觉上难以察觉的运动不自然性，从而区分真实与AI生成视频。
primary_logic: 生物力学忠实度是区分生成视频与真实视频的关键信号，独立的解剖、运动学和动力学评估能够填补视觉质量基准的空白。
claims:
- HumanScore总体得分与人类偏好高度相关（Spearman相关系数接近1.0）
- 真实视频在HumanScore上得分最高（94.3），且所有生成模型的得分均低于真实视频，证明指标能有效区分合成运动
- 生物力学指标与现有VBench指标之间仅存在中弱相关性，表明其评估了互补的维度
- HumanScore Leaderboard (Overall Score) 上 Overall = Seedance 1.0 Pro fast
---

# HumanScore: Benchmarking Human Motions in Generated Videos

> [!tip] 核心洞察
> 生物力学忠实度是区分生成视频与真实视频的关键信号，独立的解剖、运动学和动力学评估能够填补视觉质量基准的空白。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanScore：生成视频中人体运动的基准测试 |
| 英文题名 | HumanScore: Benchmarking Human Motions in Generated Videos |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.20157) · [Project](https://cs.stanford.edu/~xtiange/projects/humanscore/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | HumanScore |
| Dataset | HumanScore Leaderboard, Human Preference Alignment |

> [!tip] 效果简介
> - HumanScore Leaderboard (Overall Score) 上，Overall Seedance 1.0 Pro fast vs Real Videos (-3.2)。
> - Human Preference Alignment 上，Spearman's ρ HumanScore vs Human Judgment (~1.0)。

## 概要

现有视频生成评估体系长期聚焦于像素级视觉质量与语义对齐——例如成像质量、美学分数、主体一致性等维度——却系统性地忽略了一个关键问题：**生成的人体运动是否在生物力学上正确**。随着人体网格恢复方法误差持续收敛、视频生成模型逼真度快速提升（图2），肉眼已越来越难以分辨真实视频与AI生成视频中细微的运动异常（图1）。这一瓶颈意味着，仅凭视觉质量基准无法检测那些“看起来合理但动起来不自然”的生成缺陷。

HumanScore 的核心洞察在于：**生物力学忠实度是区分真实与生成视频的关键信号**。通过将人体运动解构为解剖、运动学和动力学三个层次，并定义六项可解释的量化指标——额外肢体、骨长稳定性、关节活动范围、自碰撞、运动极值、运动平滑度——该基准能够揭示视觉上难以察觉的运动违规。与 VBench、T2V-CompBench 等先前基准相比，HumanScore 将评估维度从“视觉质量/语义对齐”切换为“生物力学正确性”，填补了视频生成评估的关键空白。

实验证据支撑了这一设计逻辑。真实视频在 HumanScore 总分上达到 94.3，所有生成模型的得分均低于该值（Table 1），证明指标能有效区分合成运动。HumanScore 得分与人类偏好的 Spearman 相关系数接近 1.0（图7），表明自动评估与人类判断高度一致。此外，生物力学指标与 VBench 各评估轴之间仅存在中弱相关性（Table 2），确认其评估的是与现有基准互补的维度。

在方法谱系中，HumanScore 不属于生成模型本身，而是一个**评估框架**，其定位介于视频质量基准（如 VBench）与人体运动分析工具之间。它通过标准化运动集策展、系统化提示工程和全自动化指标计算三个模块，为视频生成模型提供可解释的生物力学评分。该框架不依赖人工裁判，且在不同姿态估计器、容忍度设置和权重配置下均保持模型排名的鲁棒性。

### 视频生成与评估的现状

近年来，视频生成模型在视觉真实感上取得了显著进步，生成的视频在像素级质量上越来越难以与真实视频区分。然而，现有的视频生成评估基准主要围绕**视觉质量和语义对齐**展开，例如 **VBench** 评估成像质量、美学质量和主体一致性，**T2V-CompBench** 关注组合性，**Video-Bench** 则侧重动作一致性。这些基准的核心评估逻辑停留在像素级失真度量、感知对齐和分布相似性（如FVD）层面，无法触及生成视频中人体运动的**生物力学正确性**。

这一缺口正变得愈发紧迫。一方面，人体网格恢复方法的性能已趋于收敛，误差降至较低水平；另一方面，视频生成器的真实感持续提升，使得肉眼难以察觉生成视频中的细微运动缺陷（Fig. 2）。这意味着，仅凭视觉质量评估已无法有效区分真实与AI生成的人体运动视频——这正是 HumanScore 所要解决的核心问题。

### 现有基准的关键盲区：生物力学忠实度

当前基准的根本局限在于，它们评估的是“画面看起来是否真实”，而非“运动是否在物理上合理”。AI生成视频中常见的问题包括：额外肢体、骨骼长度不稳定、关节超出解剖活动范围、自碰撞、运动极值异常以及运动不连贯等。这些缺陷在视觉上可能并不显眼，甚至对普通观察者而言完全不可察觉（Fig. 1），但从生物力学角度来看却是明显的违规。

问题的本质是：**像素级视觉质量与生物力学正确性是两个正交的评估维度**。一个视频可以在视觉上高度逼真，同时包含严重的运动学或动力学错误。现有基准无法捕捉这一维度的信息，导致对视频生成模型的评估存在系统性盲区。

### 本文动机与核心思路

HumanScore 的出发点是填补上述空白：通过构建一套以**生物力学忠实度**为核心的评估框架，揭示视觉上难以察觉的运动不自然性，从而为视频生成模型提供更全面、更深入的诊断。

核心思路是将人体运动解构为三个层次——**解剖正确性**（身体结构是否合理）、**运动学正确性**（关节运动范围和骨骼稳定性）和**动力学正确性**（运动平滑度和极值），并在每个层次上定义可解释的量化指标。这种分层设计使得评估不仅能给出总体得分，还能定位具体是哪个层次、哪类运动出现了问题，为模型改进提供明确的反馈信号。

## 核心方法与创新机理

HumanScore 的核心创新在于将视频生成评估从传统的像素级视觉质量与语义对齐，转向**生物力学正确性**这一此前被忽视的维度。现有基准测试（如 VBench、T2V-CompBench、Video-Bench）主要评估成像质量、美学质量和主体一致性等视觉层面指标，无法检测 AI 生成视频中细微的、非自然的运动缺陷。HumanScore 通过解构人体运动为解剖、运动学和动力学三个层次，定义了六项可解释的生物力学指标，填补了这一空白。

### 评估维度的根本转变

传统基准的评估维度聚焦于视觉质量和语义对齐，而 HumanScore 将评估维度切换为三个层次的生物力学正确性（见 Figure 6）：

- **解剖正确性（Anatomical Correctness）**：检测人体结构层面的异常，包括额外肢体（Extra Limbs）和骨长稳定性（Bone Length Stability）。
- **运动学正确性（Kinematic Correctness）**：评估关节运动的合理性，包括关节活动范围（Joint Range of Motion）和自碰撞（Self-Collision）。
- **动力学正确性（Kinetic Correctness）**：考察运动的时间特性，包括运动极值（Kinematic Extremes，检测非自然的速度尖峰）和运动平滑度（Motion Smoothness，通过角加速度和加加速度评估）。

这一转变的关键洞察在于：生物力学忠实度是区分生成视频与真实视频的关键信号。真实视频在 HumanScore 上获得最高分（94.3），且所有生成模型的得分均低于真实视频（Table 1），证明该指标体系能有效捕捉合成运动的缺陷。

### 从像素度量到可解释生物力学指标

传统基准依赖像素级失真度量、感知对齐和分布相似性（如 FVD），这些指标虽然能反映整体视觉质量，但无法定位具体的运动异常。HumanScore 的六项指标均具有明确的生物力学含义：

- **额外肢体**：基于检测置信度 $M_t$ 和阈值 $\tau_{\text{mild}}$ 判断每帧是否存在异常肢体结构，二元指标 $b_t \in \{0, 1\}$ 直接反映解剖完整性。
- **骨长稳定性**：通过相对误差 $e_b(t) = \frac{|l_b(t) - L_b|}{L_b + \epsilon}$ 量化骨骼比例在时间上的稳定性，捕捉生成视频中常见的肢体伸缩变形。
- **关节活动范围**：计算关节角度超出解剖限值（含容差）的程度 $\Delta_t^{(j,d)}$，检测违反人体关节生理约束的运动。
- **自碰撞**：基于碰撞面比例与双阈值，计算每帧自碰撞严重性 $m_t \in [0, 1]$，捕捉肢体穿透等物理不合理现象。
- **运动极值**：通过关节角速度与人为限值的比较，检测非自然的速度尖峰，利用牛顿第二定律 $F = ma$ 将力依赖转化为速度和加速度依赖。
- **运动平滑度**：通过角加速度超过限值的归一化比率 $q_t^{(j,d)}$ 量化运动的时间稳定性，捕捉生成视频中的抖动和不连续。

这些指标通过频率 $r$、严重性 $s$ 和持久性 $p$ 三个维度聚合为视频级得分：

$$r = \frac{1}{T} \sum_{t} b_{t}, \quad s = \frac{\sum_{t} m_{t}}{\max(1, \sum_{t} b_{t})}, \quad p = \frac{L_{\max}}{T}$$

### 与现有基准的互补性

HumanScore 并非替代现有基准，而是提供了互补的评估维度。Table 2 显示，生物力学指标与 VBench 各项评估轴之间仅存在中弱相关性（Spearman 相关系数），表明 HumanScore 评估的是视觉质量基准无法捕捉的独立信号。这种互补性使得 HumanScore 成为视频生成评估体系中的重要补充，尤其适用于需要精确人体运动表现的场景。

### 标准化评估框架的设计创新

除了指标本身的创新，HumanScore 在基准构建方法上也做出了关键设计选择，以确保评估的公平性和可比性：

1. **运动集策展**：从 Kinetics-700 出发，通过去重、类别平衡和多样性验证，并经过经验可行性检查，构建包含 51 种运动、三种难度、两种强度的标准化运动集，确保评估覆盖的广泛性和代表性。
2. **系统化提示设计**：通过提示工程确保生成视频背景干净、全身可见、相机静止、单人聚焦，有效缓解模型特定偏差（如背景、相机运动、多人物），保证不同模型生成视频的可比较性。
3. **全自动化评估**：所有指标均基于现成的人体姿态估计器自动计算，避免主观裁判偏差，并通过大规模人类偏好研究验证了与人类判断的高度一致性（Spearman 相关系数接近 1.0，见 Figure 7）。

HumanScore 的评估流水线由三个串行模块构成：**运动集策展** → **提示设计** → **多层次指标计算**。Figure 3 给出了完整流程概览。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/003_Figure_3.jpg]]
*Figure 3: Overview of HumanScore. The pipeline begins with curating a representative set of human motions from a large pool of common actions. For each motion, we carefully design prompts to mitigate model-specific biases and ensure consistent conditioning across generators. The refined prompts are then passed to both proprietary and open-source state-of-the-art video generation models. Human verification is incorporated at all stages for quality check. For each evaluation dimension shown in Figure 6, we design biomechanics-informed quantitative metrics, together with human preference studies to provide comprehensive insights from multiple perspectives*

### 模块关系与数据流

1. **运动集策展（Motion Set Curation）**  
   以 Kinetics-700 为初始动作池，经过去重、类别平衡与多样性验证，再通过经验可行性检查，最终产出包含 **51 种运动**、**三种难度**（易/中/难）、**两种强度**的标准化运动集。该模块的输出是一组结构化的运动描述，作为下游提示设计的输入。

2. **提示设计（Prompt Design）**  
   针对每种运动，系统化地构造包含五个固定组件（场景、运动、强度、描述、相机）的提示，以缓解不同视频生成模型的特定偏差——如复杂背景、截断身体、移动相机或多人物干扰。经过人工验证的标准化提示确保所有模型在**单人、全身可见、固定相机、中性背景**的公平条件下生成视频。

3. **多层次指标计算（Multi-faceted Metric Evaluation）**  
   对生成视频先进行结构化运动提取（通过预训练姿态估计器推理 87 个 3D 关键点，再经迭代优化拟合生物力学骨骼模型，见 Figure 11），随后在三个层次上计算六项可解释指标：

   | 层次 | 指标 |
   |------|------|
   | **解剖正确性** | 额外肢体、骨长稳定性 |
   | **运动学正确性** | 关节活动范围、自碰撞 |
   | **动力学正确性** | 运动极值、运动平滑度 |

   Figure 6 以自底向上的金字塔结构展示了这一生物力学层次：解剖层为基础，运动学层居中，动力学层为顶层，每层由两项独立指标共同评估。

### 输入输出规范

- **输入**：标准化提示文本（51 运动 × 2 强度 = 102 条提示）。
- **输出**：每段视频在六项指标上的归一化得分（0–100，越高表示生物力学越正确），以及按频率 $r$、严重性 $s$、持久性 $p$ 三因子聚合的视频级综合得分。最终形成模型排行榜（Table 1），支持按解剖、运动学、动力学三个维度分别比较。

### 关键设计决策

- **公平性保障**：所有模型使用完全相同的标准化提示，提示工程专门针对模型特定偏差进行了缓解，确保生成视频的可比较性。
- **全自动化**：指标计算无需人工介入，避免主观裁判偏差；其与人类判断的一致性通过大规模人类偏好研究验证（Spearman 相关系数接近 1.0，Figure 7）。
- **骨骼拟合两阶段流水线**（Figure 11）：第一阶段用预训练检测器从单目视频推断 87 个 3D 关键点，第二阶段通过迭代优化将生物力学人体骨骼模型拟合到这些关键点上，为后续所有指标提供结构化运动表示。

HumanScore 将生物力学评估解构为三个独立模块，分别对应解剖正确性、运动学正确性和动力学正确性，每个模块包含两项可解释指标（Figure 6）。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/005_Figure_6.jpg]]
*Figure 6: Biomechanical hierarchy of our evaluation framework. Each tier, from fundamental (bottom) to advanced (top), is evaluated using two independent metrics*

### 运动结构提取

所有指标依赖从单目视频中恢复的3D人体运动。系统采用两阶段流水线（Figure 11）：首先用预训练姿态/关键点检测器（如 MeTRAbs、PromptHMR）推理 87 个 3D 关键点，再通过迭代优化将生物力学人体骨骼模型拟合到这些关键点上。骨骼模型基于 OpenSim 定义，提供关节角度、骨长和关节活动范围（ROM）的先验约束。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/012_Figure_11.jpg]]
*Figure 11: For metrics that rely on skeletal fitting, we use a two-stage pipeline. First, we apply a pretrained pose/keypoint detector to infer 87 3D keypoints from monocular observations. Second, we fit a biomechanics-informed human skeleton model to these keypoints via iterative optimization*

### 解剖正确性指标

**额外肢体**：利用现成的额外肢体检测器，对每帧输出置信度 $M_t$。定义二元指标：

$$b_{t} = \begin{cases} 0, & M_{t} \leq \tau_{\text{mild}}, \\ 1, & \text{otherwise}, \end{cases}$$

其中 $\tau_{\text{mild}}$ 为温和阈值。当置信度超过阈值时判定该帧存在额外肢体异常。

**骨长稳定性**：对每根骨骼 $b$，计算其在视频中的中位数长度 $L_b$ 作为参考。每帧 $t$ 的相对误差为：

$$e_{b}(t) = \frac{|l_{b}(t) - L_{b}|}{L_{b} + \epsilon}$$

其中 $l_b(t)$ 为帧 $t$ 处骨 $b$ 的测量长度，$\epsilon$ 为小常数防止除零。该指标捕捉生成视频中骨骼长度的不稳定漂移，这是 AI 生成器常见但肉眼难以察觉的缺陷。

### 运动学正确性指标

**关节活动范围（ROM）**：对每个关节 $j$ 和自由度 $d$，预定义解剖限值 $\theta_{\min}^{(j,d)}$ 和 $\theta_{\max}^{(j,d)}$。每帧违规量定义为超出限值（含容忍度 tol）的程度：

$$\Delta_{t}^{(j,d)} = \max\{0, \theta_{t}^{(j,d)} - (\theta_{\max}^{(j,d)} + \text{tol}), (\theta_{\min}^{(j,d)} - \text{tol}) - \theta_{t}^{(j,d)}\}$$

该指标检测生成视频中违反人体关节自然活动范围的姿态。

**自碰撞**：利用现成的自碰撞检测器，基于碰撞面比例与双阈值计算每帧严重性：

$$m_{t} = \min\left\{1, \max\left\{0, \frac{M_{t} - \tau_{\text{mild}}}{\tau_{\text{severe}} - \tau_{\text{mild}}}\right\}\right\}$$

其中 $\tau_{\text{mild}}$ 和 $\tau_{\text{severe}}$ 分别为温和与严重阈值，$M_t$ 为碰撞面比例。该指标捕捉生成视频中肢体穿透身体的不自然现象。

### 动力学正确性指标

该模块基于牛顿第二定律 $F = m a$ 的核心洞察：由于无法从单目视频可靠推断力 $F$，转而利用加速度 $a$ 作为动力学异常的信号——不自然的力必然导致异常的速度和加速度模式。

**运动极值**：检测关节角速度 $\omega_{t}^{(j,d)}$ 是否超过人为限值 $\omega_{j,d}^{\text{max}}$。每帧归一化违反比率为：

$$m_{t}^{\text{joint}} = \frac{\sum_{j,d} \min\{1, \max(0, \frac{|\omega_{t}^{(j,d)}|}{\omega_{j,d}^{\text{max}}} - 1)/0.5\}}{\sum_{j,d} w_{j,d}}$$

其中 $w_{j,d}$ 为各自由度的权重。该指标捕捉生成视频中不自然的关节速度尖峰。

**运动平滑度**：对关节角加速度 $\alpha_{t}^{(j,d)}$（由角速度中心差分计算）和加加速度（jerk，短时间窗内局部能量累积）进行限值检查。每帧违反比率为：

$$q_{t}^{(j,d)} = \min\left\{1, \max\left(0, \frac{|\alpha_{t}^{(j,d)}|}{\alpha_{j,d}^{\text{max}}} - 1\right)/0.5\right\}$$

该指标检测生成视频中运动的不连续性和抖动。

### 视频级聚合

将每帧异常信号聚合为视频级得分，使用三个互补维度：频率 $r$、严重性 $s$ 和持久性 $p$：

$$r = \frac{1}{T} \sum_{t} b_{t}, \quad s = \frac{\sum_{t} m_{t}}{\max(1, \sum_{t} b_{t})}, \quad p = \frac{L_{\max}}{T}$$

其中 $T$ 为总帧数，$b_t$ 为帧级二元异常标记，$m_t$ 为帧级严重性，$L_{\max}$ 为最长连续异常帧段长度。最终得分通过频率、严重性、持久性的加权组合（权重 $\alpha, \beta, \gamma$）归一化到 0–100 尺度，分数越高表示生物力学越正确。

> **鲁棒性说明**：消融实验（Figure 8, Figure 9）表明，在不同容忍度尺度、不同姿态估计器（MeTRAbs vs. PromptHMR）以及频率-严重性-持久性权重组合的网格搜索下，模型排名保持高度一致，验证了指标设计的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/004_Figure_5.jpg]]
*Figure 5: Prompt Design. Different models tend to have different biases when generating videos, which may lead to unnatural scenes, truncated bodies, moving cameras, or multiple people. We experimented extensively with prompt engineering to mitigate these model biases and obtain the most stable motions in the generated videos, which facilitates metric calculation. Best viewed when zoomed in*

## 实验与关键发现

### 主实验结果

HumanScore 对 12 个前沿视频生成模型进行了系统评估，涵盖解剖正确性、运动学正确性和动力学正确性三个维度。**Table 1** 展示了完整的排行榜结果。真实视频在所有维度上均获得最高分，总体得分达到 94.3，验证了指标对真实人体运动的偏好。在生成模型中，Seedance 1.0 Pro fast 和 HunyuanVideo 1.5 以 91.1 的总体得分并列第一，紧随其后的是 Sora 2（90.2）和 Veo 3.1 Fast（89.3）。值得注意的是，即使表现最佳的生成模型仍与真实视频存在 3.2 分的差距，表明当前生成器在人体运动生物力学忠实度上仍有改进空间。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/006_Table_1.jpg]]
*Table 1: HumanScore Leaderboard. Higher scores indicate better performance. The best score in each dimension is highlighted in cell colors*

从各维度细分来看，解剖正确性维度上模型间差异最小（最高 95.0，最低 88.2），而动力学正确性维度差异最大（最高 89.1，最低 76.1）。这表明现有模型在基础解剖结构保持方面相对成熟，但在运动平滑度和速度合理性等动力学层面存在明显短板。

### 与人类偏好的一致性验证

为验证指标的有效性，研究团队进行了大规模人类偏好研究。如 **Figure 7** 所示，HumanScore 的总体得分与人类偏好的胜率之间呈现出极强的相关性，Spearman 相关系数接近 1.0。这一结果在解剖、运动学、动力学三个子维度上均保持一致，证明自动化指标能够有效替代人类评估，捕捉到人类观察者所关注的生物力学质量信号。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/007_Figure_7.jpg]]
*Figure 7: HumanScore metric values show strong alignment with human preference. The plot compares the averaged HumanScore win rate (Y-axis) against the overall human preference win ratio (X-axis). A linear fit is included to visualize the correlation and the overall Spearman’s correlation coefficient (ρ) is reported*

### 与现有基准的互补性分析

**Table 2** 报告了 HumanScore 六项生物力学指标与 VBench 评估轴之间的 Spearman 相关系数。结果显示，两者之间仅存在中弱相关性（大部分相关系数低于 0.5），表明 HumanScore 评估的是与像素级视觉质量和语义对齐正交的维度。这一发现证实了核心洞察：生物力学忠实度是现有视频质量基准所遗漏的关键评估维度。

### 消融实验与鲁棒性验证

研究通过多项消融实验验证了 HumanScore 的鲁棒性：

- **姿态估计器替换**：将默认的 MeTRAbs 替换为 PromptHMR 后，模型排名保持不变，证明指标对底层姿态估计方法不敏感。
- **容忍度参数变化**：如 **Figure 8** 所示，在不同容忍度尺度设置下，模型排名保持高度一致。
- **权重超参数网格搜索**：**Figure 9** 的三元图展示了频率（α）、严重性（β）和持久性（γ）权重组合的网格搜索结果。每个三元坐标点对应一组权重配置，各模型的排名在不同配置下保持稳定，表明指标聚合策略具有内在鲁棒性。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/009_Figure_8.jpg]]
*Figure 8: Model rankings (y-axis) across different tolerance scales (x-axis). The rankings remain consistent across scales, demonstrating the robustness of our metrics*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/010_Figure_9.jpg]]
*Figure 9: Ternary plots of model rankings under varying hyperparameters. Each point in the ternary diagram corresponds to one combination of*

### 运动难度分解分析

**Figure 10** 揭示了运动难度对模型表现的显著影响。随着运动难度从“易”到“难”递增，所有模型的各项指标得分均出现明显下降。这一趋势在动力学正确性维度上尤为突出，困难运动（如复杂体操动作）的得分远低于简单运动（如行走），说明当前生成模型在复杂、高动态运动的生物力学一致性方面存在系统性不足。

### 失败模式与局限性

尽管 HumanScore 展现出强鲁棒性，仍存在若干值得关注的失败模式：

1. **真实视频未获满分**：真实视频得分 94.3 而非 100，主要源于单目 3D 姿态估计的固有深度模糊性，以及对遮挡和运动模糊的敏感性，导致轻微的估计噪声被计入指标扣分。
2. **接触与逆动力学指标缺失**：研究排除了脚-地接触检测和逆动力学分析，因为这些模块在复杂运动中依赖不可靠的接触检测或动力学分解，误差较大。
3. **评估范围受限**：当前基准仅适用于单人、全身可见、固定相机、中性背景的生成视频，无法覆盖多人交互或复杂场景。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/008_Table_2.jpg]]
*Table 2: Spearman correlations between our biomechanics-informed metrics and VBench [23] evaluation axes*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/011_Figure_10.jpg]]
*Figure 10: Detailed breakdown of benchmark results across each evaluation dimension (left) and motion difficulty level (right). The value range shown in the plots is (50, 100)*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_20157/figures/002_Figure_2.jpg]]
*Figure 2: The performance of human mesh recovery methods is converging at low errors and video generators are becoming more realistic*

## 定位与知识库关联

### 问题域定位：从视觉质量到生物力学正确性

当前视频生成评估的主流范式集中于像素级视觉质量和语义对齐。代表性的基准测试包括 **VBench**（评估成像质量、美学质量、主体一致性等维度）、**T2V-CompBench**（评估组合性生成能力）和 **Video-Bench**（评估动作一致性）。这些基准的评估指标主要依赖像素级失真度量、感知对齐分数和分布相似性指标（如FVD），本质上衡量的是“看起来是否真实”。

HumanScore的切入点在于识别了这一范式的盲区：现有指标无法检测AI生成视频中细微的、非自然的生物力学缺陷。随着人体网格恢复方法的性能收敛至低误差水平，以及视频生成器真实感的快速提升（Figure 2），视觉层面的区分变得越来越困难。HumanScore将评估维度从“视觉质量”转向“生物力学正确性”，填补了这一空白。

### 方法谱系：生物力学层次化评估框架

HumanScore的方法设计遵循一个清晰的层次化逻辑，将人体运动解构为三个递进层次（Figure 6）：

1. **解剖正确性（Anatomical Correctness）**：评估身体结构是否合理，包括额外肢体检测和骨长稳定性两项指标。
2. **运动学正确性（Kinematic Correctness）**：评估运动范围是否在人体关节活动限度内，包括关节活动范围违规检测和自碰撞检测。
3. **动力学正确性（Kinetic Correctness）**：评估运动的速度和加速度是否在人体能力范围内，包括运动极值检测和运动平滑度评估。

这一层次化设计的关键创新在于：将动力学评估从力依赖转化为速度和加速度依赖。通过牛顿第二定律 $F = m a$，框架避免了直接估计力或质量的不确定性，转而利用角速度和角加速度的可观测信号进行违规检测。

与VBench等基准的互补性在Table 2中得到了定量验证：生物力学指标与VBench各评估轴之间的Spearman相关系数仅呈现中弱相关性，表明HumanScore确实评估了一个独立的、互补的维度。

### 适用边界与已知局限

**评估范围约束**：当前HumanScore的评估仅限于单人全身、固定相机、中性背景的生成视频。这一约束是方法设计的有意选择——通过系统化的提示工程（Figure 5）确保生成视频背景干净、全身可见、相机静止、单人聚焦，从而保证评估的公平性和可比性。但这也意味着该基准不适用于多人交互场景或复杂环境中的视频评估。

**姿态估计依赖**：指标计算依赖现成的人体姿态估计器（如MeTRAbs、PromptHMR、GVHMR）。尽管消融实验表明更换姿态估计器后模型排名保持不变（Section 5.2），但单目3D姿态恢复固有的深度模糊性和对遮挡、运动模糊的敏感性仍然会引入估计噪声。这解释了为什么真实视频在HumanScore上并未获得满分（94.3/100）——部分扣分源于姿态估计误差而非真实的生物力学违规。

**缺失的物理维度**：作者明确排除了脚-地接触检测和逆动力学指标。前者因为接触检测在单目视频中不可靠，后者因为动力学分解在复杂运动中误差较大。这意味着当前框架无法检测与地面交互相关的细微违规（如滑步、漂浮），也无法直接评估力-运动关系的物理一致性。

### 鲁棒性证据与超参数敏感性

HumanScore的指标聚合涉及多个超参数，包括容忍度阈值、频率-严重性-持久性的权重组合 $(\alpha, \beta, \gamma)$。作者通过一系列鲁棒性实验验证了框架的稳定性：

- 在不同容忍度尺度下，模型排名保持一致（Figure 8）。
- 在 $(\alpha, \beta, \gamma)$ 权重组合的网格搜索中，各模型排名在三元图中高度稳定（Figure 9）。
- 随着运动难度从易到难，所有模型的指标得分都出现明显下降（Figure 10），验证了指标对运动复杂度的敏感性。

这些实验表明，尽管超参数的具体取值可能影响绝对分数，但模型的相对排名对超参数选择不敏感，增强了基准作为模型比较工具的可靠性。

### 开放问题与未来方向

1. **多人交互扩展**：当前框架无法处理多人场景。扩展到多人交互需要解决人体检测、身份跟踪和交互物理约束建模等问题。
2. **物理模拟融合**：将物理模拟和接触推理更好地融入指标，可以检测更细微的动力学违规（如足部滑动、动量不守恒）。
3. **生成模型引导**：能否利用这些生物力学指标直接指导视频生成模型优化？这需要解决指标的可微性和生成模型的训练集成问题。
4. **自适应权重学习**：当前 $(\alpha, \beta, \gamma)$ 权重虽经网格搜索验证鲁棒，但最优值是否可以通过数据驱动的方式自适应学习，仍是一个开放问题。

## 原文 PDF

![[paperPDFs/arxiv_2026/HumanScore_Benchmarking_Human_Motions_in_Generated_Videos.pdf]]

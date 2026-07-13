---
title: "Clay-to-Stone: Phase-wise 3D Gaussian Splatting for Monocular Articulated Hand-Object Manipulation Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Clay_to_Stone_Phase_wise_3D_Gaussian_Splatting_for_Monocular_Articulated_Hand_Object_Manipulation_Modeling.pdf
project_link: null
code_link: "https://github.com/ru1ven/ARGS"
aliases:
- CS
- Clay-to-Stone
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 可学习的原始级调制因子 β_G 结合语义一致性损失，控制高斯变形幅度，使得模型能够先灵活探索部件语义和运动模式，再通过刚性约束进行巩固。
primary_logic: 通过从语义感知的柔性变形探索逐步过渡到刚性铰接估计的层次化建模粒度，将形状与运动解耦；在 CLAY 阶段学习部件级语义和运动先验，在 STONE 阶段施加物理约束，实现从“粘土”到“石头”的递进式精细化。
claims:
- CLAY 阶段引入的原始级调制机制允许对 3D 高斯进行细粒度、语义感知的变形控制，无需预定义铰接规则。
- STONE 阶段利用学习到的资格信号施加刚性约束，并显式估计转动关节参数，巩固物理上一致的铰接结构。
- 核心洞察在于逐步细化空间粒度，从柔性、分布式表示过渡到清晰的刚性部件结构，以此学习部件级语义和运动。
- ARCTIC (铰接物体重建) 上 CD↓ (平均) = 1.97
---

# Clay-to-Stone: Phase-wise 3D Gaussian Splatting for Monocular Articulated Hand-Object Manipulation Modeling

> [!tip] 核心洞察
> 通过从语义感知的柔性变形探索逐步过渡到刚性铰接估计的层次化建模粒度，将形状与运动解耦；在 CLAY 阶段学习部件级语义和运动先验，在 STONE 阶段施加物理约束，实现从“粘土”到“石头”的递进式精细化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 粘土到石头：用于单目铰接手-物体操纵建模的阶段性三维高斯泼溅 |
| 英文题名 | Clay-to-Stone: Phase-wise 3D Gaussian Splatting for Monocular Articulated Hand-Object Manipulation Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Clay-to-Stone_Phase-wise_3D_Gaussian_Splatting_for_Monocular_Articulated_Hand-Object_Manipulation_CVPR_2026_paper.html) · [Code](https://github.com/ru1ven/ARGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Clay-to-Stone |
| Dataset | ARCTIC |

> [!tip] 效果简介
> - ARCTIC (铰接物体重建) 上，CD↓ (平均) 1.97 vs 3DGS-Avatar (未提供具体数值, 但本文达到最优) (最优 (SOTA))；F@5↑ (平均) 0.741 vs 3DGS-Avatar (最优)。
> - ARCTIC (手物真实感渲染) 上，PSNR↑ (平均) 28.17 vs - (最优)；LPIPS↓ (平均) 35.43 vs - (最优)。
> - ARCTIC (规范姿态刚体重建) 上，CD↓ 0.79 vs HOLD / BIGS (优于刚体重建方法)。

## 概要

**问题与瓶颈。** 从单目 RGB 视频中重建铰接物体的三维几何与运动，是手-物交互理解的核心挑战。其根本困难在于：连续变化的关节旋转与频繁的部件变形，使得物体形状与运动在观测中深度耦合，导致严重的几何歧义和重建不稳定。现有方法要么假设物体为刚体（如 **HOLD** (Fan et al., CVPR 2024) 和 **BIGS** (On et al., CVPR 2025)），要么采用每帧自由变形场（如 **3DGS-Avatar** (Qian et al., CVPR 2024)），缺乏对部件级语义和物理铰接约束的显式建模，难以从持续变化的铰接状态中解耦出内在的几何结构。

**核心洞察与方法定位。** 本文提出 **Clay-to-Stone** 框架，核心洞察在于通过层次化的建模粒度实现形状与运动的解耦：先以柔性、语义感知的方式探索部件变形与运动先验，再施加刚性约束将其巩固为物理一致的铰接结构。这一“从粘土到石头”的递进策略，使模型能够在不预定义铰接规则的前提下，自主发现部件语义并估计转动关节参数。方法建立在 3D Gaussian Splatting (3DGS) 之上，通过双阶段流水线——**CLAY 阶段**（语义感知的柔性变形探索）和 **STONE 阶段**（刚性铰接建模与约束）——实现从单目手-物操纵视频中同时恢复高保真几何、照片级渲染外观和物理上合理的转动关节运动。

**关键机制。** CLAY 阶段引入**原始级调制因子** $\beta_{\mathcal{G}}$，结合基于 SAM2 的部件语义一致性损失，实现对每个 3D 高斯的细粒度、可解释变形控制；STONE 阶段将调制因子转化为**运动资格信号**，施加刚性约束，并显式回归转动关节参数（旋转轴、枢轴点、每帧角度），辅以时序一致性正则化，确保运动在时间上的连贯与物理合理。

**主要结果。** 在 ARCTIC 数据集上，Clay-to-Stone 在铰接物体重建（CD↓ 1.97, F@5↑ 0.741）和手物真实感渲染（PSNR↑ 28.17, LPIPS↓ 35.43）两项任务上均达到最优水平，并在规范姿态刚体重建中优于 HOLD 和 BIGS 等刚体基线。消融实验证实，调制机制、语义一致性监督和时序损失对最终性能均有显著贡献。

**局限与开放问题。** 当前框架假定物体仅含单一转动关节，对多部件、多自由度铰接结构的扩展仍是未来方向。此外，在严重遮挡或缺乏准确 2D 部件分割的场景下，语义一致性学习的鲁棒性有待进一步验证。

### 问题背景：单目手-物操纵建模的几何-运动耦合困境

从单目 RGB 视频中重建铰接物体的三维几何与运动，是计算机视觉与图形学中长期存在的挑战。在日常手-物操纵场景中，物体往往包含可动部件（如笔记本电脑的屏幕、盒子的盖子），这些部件在双手操作下经历连续的旋转、开合等变形。这类场景的核心困难在于**形状与运动的强耦合**：单目观测所提供的二维线索本身具有深度模糊性，而铰接物体的几何变形与关节运动又高度纠缠——模型很难从持续变化的铰接状态中解耦出物体的内在几何结构。这种耦合导致严重的几何歧义与重建不稳定性，使得现有方法在处理此类动态场景时捉襟见肘。

### 现有方法的缺口

当前面向手-物交互重建的方法主要沿两个方向展开，但各自存在根本性局限：

- **类别无关的刚体重建方法**（如 **HOLD** (Fan et al., CVPR 2024) 和 **BIGS** (On et al., CVPR 2025)）假设物体几何在整个操纵过程中保持静态。这一假设在铰接场景下直接失效——它们无法对可动部件的变形进行建模，因而无法恢复物体的功能性结构。

- **可变形 3DGS 化身方法**（如 **3DGS-Avatar** (Qian et al., CVPR 2024)）虽然允许每帧自由变形，但变形场缺乏部件级语义感知和物理约束。这类方法将所有高斯一视同仁地进行变形，无法区分可动部件与静态部件，更无法显式估计铰接参数（如旋转轴、枢轴点、旋转角度）。结果是变形虽然灵活，但缺乏物理合理性，且无法泛化到新视角下的铰接运动。

两类方法的共同缺口在于：**缺乏从柔性探索到刚性巩固的层次化建模机制**。直接拟合自由变形会陷入几何-运动耦合的局部最优，而直接施加刚性约束又缺乏对部件语义和运动模式的先验认知。

### 本文动机：从“粘土”到“石头”的递进式精细化

本文的核心洞察是：**学习部件级语义和运动的有效途径，在于逐步细化空间建模粒度——从柔性、分布式表示过渡到清晰、刚性的部件结构**。这一思想被形式化为 **Clay-to-Stone** 双阶段框架：

- **CLAY 阶段**（粘土阶段）：允许模型在语义感知的指导下进行灵活的高斯变形探索，通过可学习的原始级调制因子 $\beta_{\mathcal{G}}$ 控制变形幅度，同时利用 SAM2 分割先验建立部件级语义一致性。此阶段的目标是“发现”物体的部件语义和运动先验，而非直接追求物理精确性。

- **STONE 阶段**（石头阶段）：在 CLAY 阶段积累的语义和运动先验基础上，施加刚性约束并显式估计转动关节参数（旋转轴 $\mathbf{l}$、枢轴点 $\mathbf{p}$、每帧角度 $\theta_t$），通过时序一致性正则化确保铰接运动的物理合理性和时间连贯性。

这种“先探索、后巩固”的策略，从根本上规避了单阶段方法中几何-运动耦合带来的歧义问题：CLAY 阶段为 STONE 阶段提供了可靠的初始化与语义引导，而 STONE 阶段则将柔性表示“固化”为物理一致的铰接结构。实验表明，该框架在 ARCTIC 数据集上实现了铰接物体重建与真实感渲染的双重 SOTA 性能，并在规范姿态刚体重建任务上超越了专门的刚体重建基线方法。

## 核心方法与创新机理

### 问题瓶颈：几何-运动强耦合的“鸡与蛋”困境

单目视频中的手物铰接操纵重建面临一个根本性瓶颈：连续的关节旋转与频繁的部件变形使得物体的内在几何形状与瞬态铰接状态深度纠缠。现有方法或假设物体完全刚体（如 **HOLD**，Fan et al., CVPR 2024；**BIGS**，On et al., CVPR 2025），或采用每帧自由变形场（如 **3DGS-Avatar**，Qian et al., CVPR 2024），均无法从持续变化的铰接状态中解耦出稳定的部件级几何结构。这种耦合导致严重的几何歧义——模型难以判断某一外观变化应归属于形状变形还是铰接运动，从而在重建精度与运动一致性之间陷入两难。

### 核心洞察：从“粘土”到“石头”的粒度递进

本文的核心洞察在于**通过层次化的建模粒度逐步解耦形状与运动**：先以柔性、分布式的表示探索部件语义和运动先验，再通过刚性约束将其巩固为物理上一致的铰接结构。这一“先探索、后巩固”的策略被形象地概括为 **Clay-to-Stone**——在 CLAY 阶段，模型如粘土般灵活变形以学习部件级语义关联；在 STONE 阶段，这些学习到的先验被“固化”为石头般的刚性铰接表示。

### 关键创新一：原始级语义感知调制（CLAY 阶段）

CLAY 阶段的核心创新在于引入**原始级调制机制**（primitive-level modulation），实现对 3D 高斯变形的细粒度、语义感知控制。具体而言：

- **可学习调制因子 $\beta_{\mathcal{G}}$**：每个物体高斯被赋予一个可学习的调制因子，通过 Gumbel sigmoid 门控控制其变形幅度。这使得模型能够自动发现哪些高斯属于可动部件、哪些属于静态结构，无需预定义铰接规则。
- **语义一致性监督**：模型渲染部件级掩膜 $M_{\text{part}}^t$ 并与 SAM2 分割结果对齐，迫使调制因子收敛到语义上有意义的分组。这一设计将 2D 分割先验注入 3D 表示学习，使得部件边界的发现由数据驱动而非人工指定。

与 **3DGS-Avatar** 的每帧自由变形场相比，调制机制的关键优势在于**变形不再是无约束的逐帧拟合**，而是受到可学习标量因子 $\beta_{\mathcal{G}}$ 的结构化约束——同一高斯的变形幅度在时序上保持一致性，从而隐式编码了“哪些区域倾向于运动”的先验知识。

### 关键创新二：从调制因子到铰接参数的语义桥接（STONE 阶段）

STONE 阶段的核心创新在于**将 CLAY 阶段学习到的调制因子转化为刚性铰接的资格信号**，实现从柔性变形到物理约束的无缝过渡：

- **运动资格信号 $\mathbf{e} = g(\beta_{\mathcal{G}})$**：通过 Gumbel sigmoid 将连续调制因子转换为近二值的运动资格，确保只有语义上被识别为“可动”的高斯参与铰接变换。这一设计巧妙地将 CLAY 阶段发现的部件语义直接桥接到 STONE 阶段的物理建模，避免了手动指定可动区域的需要。
- **显式转动关节回归**：模型从哈希特征和变形编码中直接回归转动关节参数——旋转轴 $\mathbf{l}$（Eq. 9）、枢轴点 $\mathbf{p}$（Eq. 8）和每帧旋转角 $\theta_t$（Eq. 10）。与依赖预定义骨架的方法不同，关节参数完全从数据中学习，且通过时序一致性损失 $\mathcal{L}_t$（Eq. 11）约束相邻帧旋转角的速度和加速度平滑性。

### 关键创新三：双阶段训练范式的协同效应

Clay-to-Stone 的双阶段设计并非简单的分步训练，而是形成了**探索与巩固的协同循环**：

- **CLAY 阶段（前 10k 迭代）**：模型在无刚性约束的条件下自由探索变形空间，通过语义一致性损失建立部件级关联。此时的变形是“软”的——每个高斯可以独立移动，不受铰接运动学的限制。
- **STONE 阶段（后续迭代）**：刚性约束被引入，模型被迫将柔性变形“解释”为绕固定轴的旋转。由于 CLAY 阶段已经学习到了合理的部件分组和运动趋势，这一过渡是平滑的——铰接参数可以从已有的变形模式中自然涌现，而非从零开始搜索。

消融实验验证了这一协同效应的关键性：仅保留 CLAY 自由变形（无 STONE 刚性约束）将无法恢复物理上合理的铰接结构（Fig. 5）；而移除调制机制（w/o modulation）则导致渲染质量大幅下降（Table 4），表明 $\beta_{\mathcal{G}}$ 对灵活变形控制不可或缺。

### 与基线方法的系统性差异

| 创新维度 | 基线方法 | Clay-to-Stone |
|---------|---------|---------------|
| **物体变形控制** | 每帧自由变形场（3DGS-Avatar）或静态假设（HOLD/BIGS），无部件语义感知 | 原始级调制因子 $\beta_{\mathcal{G}}$ + Gumbel sigmoid 门控 + SAM2 语义一致性损失，实现精细、可解释的部件级变形控制 |
| **铰接建模** | 无显式铰接（假设完全刚体）或仅基于骨架变形 | 资格信号 $\mathbf{e}$ 施加刚性约束，显式回归转动关节参数（$\mathbf{l}, \mathbf{p}, \theta_t$），结合时序一致性正则 |
| **训练范式** | 单一阶段联合优化，直接从初始状态拟合变形或静态形状 | 双阶段 Clay-to-Stone：CLAY 探索柔性变形并发现语义/运动先验，STONE 引入刚性约束并联合优化铰接参数与高斯属性 |

### 局限与开放问题

当前框架假定物体仅包含**单一转动关节**（revolute joint），对于具有多部件、多自由度（如棱柱副）的复杂铰接结构仍需扩展。此外，在缺少准确 2D 部件分割（如 SAM2 不可用）或手-物严重遮挡的场景下，语义一致性学习的鲁棒性尚待验证。STONE 阶段的刚性约束是否足以处理非理想铰接（如摩擦、少量非刚性变形）也是值得进一步探索的方向。

Clay-to-Stone 提出了一种**阶段性三维高斯泼溅（3DGS）框架**，用于从单目 RGB 视频中重建铰接手-物体操纵的几何与运动。其核心设计动机源于一个关键瓶颈：单目观测下，连续的关节旋转与频繁的部件变形导致物体的内在几何形状与铰接运动强耦合，引发严重的几何歧义与优化不稳定性。现有方法要么假设物体为完全刚体（如 **HOLD**, Fan et al., CVPR 2024; **BIGS**, On et al., CVPR 2025），要么采用每帧自由变形场却缺乏部件级语义与物理约束（如 **3DGS-Avatar**, Qian et al., CVPR 2024），均无法有效解耦这一耦合。

为应对该挑战，框架引入了一种从“粘土”到“石头”的**层次化建模粒度递进策略**：先在 CLAY 阶段以柔性、语义感知的方式探索部件级变形与运动先验，再在 STONE 阶段施加刚性约束，将表示巩固为物理上一致的铰接结构。这一设计形成了一个清晰的**因果调控机制**——可学习的原始级调制因子 $\beta_{\mathcal{G}}$ 作为控制高斯变形幅度的核心“旋钮”，结合语义一致性损失，使模型能够在语义引导下灵活探索，随后通过刚性化完成收敛。

### 流水线总览

整体流水线（Figure 2）由四个紧密协作的模块构成，输入为单目 RGB 视频序列与手部姿态估计，输出为铰接物体的三维重建与任意视角的真实感渲染：

1. **手-物高斯表示**：在规范空间中以三组 3D 高斯分别表示双手与物体。手部高斯通过线性混合蒙皮（LBS）驱动到观测帧，物体高斯则先经刚性 6D 变换再送入后续变形模块。渲染通过 alpha 合成统一完成：
   $$C = \sum_{i \in \mathcal{N}_{\mathrm{ho}}} \mathbf{c}_i \alpha_i \prod_{j=1}^{i-1} (1-\alpha_j)$$

2. **CLAY 阶段（语义感知精细调制）**：利用 ViT 视觉特征与多分辨率哈希网格生成每高斯的潜在变形编码 $\mathbf{Z}_t$，通过可学习调制因子 $\beta_{\mathcal{G}}$ 控制变形幅度，实现细粒度、语义感知的部件级变形探索。同时渲染部件级掩膜与 SAM2 分割对齐，建立部件语义一致性。

3. **STONE 阶段（刚性铰接建模）**：将调制因子通过 Gumbel sigmoid 转换为近二值的运动资格信号 $\mathbf{e} = g(\beta_{\mathcal{G}})$，仅允许语义上可动的区域参与铰接。从哈希特征与变形编码中显式回归转动关节参数——旋转轴 $\mathbf{l}$、枢轴点 $\mathbf{p}$ 与每帧旋转角 $\theta_t$，并施加时序一致性正则化。

4. **联合优化与渲染**：结合光度损失、掩膜损失、部件语义损失与时序一致性损失，端到端联合优化所有高斯属性与铰接参数。

### 阶段过渡与粒度递进

框架的关键洞察在于**逐步细化空间粒度**：CLAY 阶段（前 10k 迭代）保持柔性、分布式的变形表示，使模型能够自由探索部件语义与运动模式，避免过早刚性化导致的局部最优；STONE 阶段则在已学到的运动先验基础上引入刚性约束，将“粘土”般的可塑表示固化为“石头”般的清晰刚性部件结构，实现形状与运动的解耦。这一从柔性探索到刚性巩固的递进，是方法能够同时取得高精度几何重建（ARCTIC 上平均 CD 达 1.97）与物理合理铰接估计的核心机制。

![[assets/figures/papers/paper_list_l2634_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Clay_to_Stone_Phas/figures/001_Figure_1.jpg]]
*Figure 1: Our Clay-to-Stone framework models coupled geometry and articulation in monocular hand-object manipulation clips through a phase-wise strategy, transitioning from adaptive deformations and part-aware semantics to physically consistent articulation for 3D reconstruction and photo-realistic rendering*

### 3.1 手-物高斯表示

Clay-to-Stone 框架基于 3D Gaussian Splatting（3DGS）构建规范空间中的手-物联合表示。双手与物体分别用三组独立的 3D 高斯表示，每组高斯由其中心 $\pmb{\mu}$、协方差矩阵 $\pmb{\Sigma}$、颜色 $\mathbf{c}$ 和不透明度 $\alpha$ 参数化。单个高斯在空间位置 $\mathbf{x}$ 处的非归一化密度为：

$$\mathcal { G } ( \mathbf { x } ) = \exp \left( - \frac { 1 } { 2 } ( \mathbf { x } - \pmb { \mu } ) ^ { \top } \pmb { \Sigma } ^ { - 1 } ( \mathbf { x } - \pmb { \mu } ) \right) \tag{1}$$

将规范高斯变换到观测帧时，双手采用线性混合蒙皮（LBS），物体采用刚性 6D 变换。LBS 利用骨骼变换矩阵 $B_i$ 和可学习蒙皮权重 $w_i(\mathbf{x})$ 映射高斯中心与旋转：

$$\mathbf { x } _ { t } = \Big ( \sum _ { i = 1 } ^ { n _ { b } } w _ { i } ( \mathbf { x } ) B _ { i } \Big ) \mathbf { x } , \quad \mathbf { R } _ { t } = \Big ( \sum _ { i = 1 } ^ { n _ { b } } w _ { i } ( \mathbf { x } ) B _ { i } \Big ) _ { 1 : 3 , 1 : 3 } \mathbf { R } \tag{3}$$

最终像素颜色通过 alpha 合成渲染：

$$C = \sum _ { i \in \mathcal { N } _ { \mathrm { h o } } } \mathbf { c } _ { i } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ) \tag{2}$$

其中 $\mathcal{N}_{\mathrm{ho}}$ 为当前像素贡献的所有手-物高斯集合。

---

### 3.2 CLAY 阶段：语义感知的原始级调制

CLAY 阶段的核心设计目标是**在无预定义铰接规则的条件下，学习部件级语义与运动先验**。其关键模块为原始级调制机制（primitive-level modulation），通过两个子模块协同实现：

#### 3.2.1 时空潜在变形编码

对规范空间中的每个物体高斯，首先将其中心 $\mathbf{x}$ 投影到当前帧像素坐标 $\pi(\mathbf{x})$，提取像素对齐的 ViT 视觉特征 $\mathbf{I}_{\mathcal{F}}^t(\pi(\mathbf{x}))$，同时查询多分辨率哈希网格特征 $\mathbf{h}$。二者拼接后经 MLP 生成每高斯的潜在变形向量：

$$\mathbf { Z } _ { t } = \mathbf { M L P } \Big ( \mathbf { I } _ { \mathcal { F } } ^ { t } ( \pi ( \mathbf { x } ) ) , \mathbf { h } \Big ) \tag{4}$$

$\mathbf{Z}_t$ 编码了该高斯在当前帧的潜在变形信息，包括位置偏移 $\delta\mathbf{x}_t$、缩放偏移 $\delta\mathbf{s}_t$、旋转偏移 $\delta\mathbf{q}_t$ 和颜色偏移 $\delta\mathbf{c}_t$。

#### 3.2.2 可学习调制因子与语义门控

每个物体高斯 $\mathcal{G}$ 关联一个可学习的调制因子 $\beta_{\mathcal{G}}$，通过 sigmoid 门控作用于潜在编码：

$$( \delta \mathbf { x } _ { t } , \delta \mathbf { s } _ { t } , \delta \mathbf { q } _ { t } , \delta \mathbf { c } _ { t } ) = s i g m o i d ( \beta _ { \mathcal { G } } ) \cdot \mathbf { Z } _ { t } \tag{5}$$

$\beta_{\mathcal{G}}$ 的物理意义在于：**控制每个高斯原语对变形的响应幅度**。在 CLAY 阶段，$\beta_{\mathcal{G}}$ 被允许自由学习，使模型能够灵活探索哪些区域倾向于运动（如笔记本屏幕、盒子盖子），哪些区域保持静态（如底座）。这种软分配机制避免了早期阶段对铰接结构的硬性假设。

#### 3.2.3 部件语义一致性监督

为确保调制因子学习到有意义的部件语义，CLAY 阶段引入基于 SAM2 的部件掩膜渲染。将调制因子通过 alpha 合成渲染为部件级掩膜：

$$M _ { \mathrm { p a r t } } ^ { t } = \sum _ { i \in \mathcal { N } _ { \mathrm { o } } ^ { t } } g ( \beta _ { \mathcal { G } } ) _ { i } \alpha _ { i } ^ { t } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ^ { t } ) \tag{6}$$

其中 $g(\cdot)$ 为 Gumbel sigmoid 函数，将 $\beta_{\mathcal{G}}$ 推向近二值分布。渲染掩膜与 SAM2 自动分割结果对齐，构成部件语义一致性损失 $\mathcal{L}_M$，驱动模型在无人工标注的条件下自动发现可动部件边界。

---

### 3.3 STONE 阶段：刚性铰接建模

STONE 阶段在 CLAY 学习到的语义与运动先验基础上，**施加刚性约束并显式估计转动关节参数**，将柔性表示固化为物理一致的铰接结构。

#### 3.3.1 运动资格信号与刚性约束

将 CLAY 阶段的调制因子通过 Gumbel sigmoid 转换为近二值的运动资格信号：

$$\mathbf { e } = g ( \beta _ { \mathcal { G } } ) \tag{7}$$

$\mathbf{e}$ 的取值为 0 或 1，明确标识每个高斯是否属于可动部件。STONE 阶段的核心约束是：**只有 $\mathbf{e}=1$ 的高斯参与铰接运动，$\mathbf{e}=0$ 的高斯保持刚性静止**。这一设计将 CLAY 阶段模糊的软分配固化为硬性部件分割。

#### 3.3.2 转动关节参数回归

对于单一转动关节（revolute joint），需估计三个参数：旋转轴 $\mathbf{l} \in \mathbb{R}^3$（$\|\mathbf{l}\|=1$）、枢轴点 $\mathbf{p} \in \mathbb{R}^3$ 和每帧旋转角 $\theta_t$。

**枢轴点**通过加权高斯位置回归，权重由哈希特征经 MLP 和 softmax 得到：

$$\mathbf { p } = \sum _ { i = 1 } ^ { N } w _ { i } \mathbf { x } _ { i } , \quad w _ { i } = \mathrm { s o f t m a x } \left( \mathrm { M L P } _ { \mathrm { p i v o t } } ( \mathbf { h } _ { i } ) \right) \tag{8}$$

**旋转轴**从平均哈希特征经 MLP 输出并归一化：

$$\mathbf { l } = \frac { \mathbf { M L P } _ { \mathrm { a x i s } } \left( \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \mathbf { h } _ { i } \right) } { \left\| \mathbf { M L P } _ { \mathrm { a x i s } } ( \cdot ) \right\| } \tag{9}$$

**每帧旋转角**结合资格信号 $\mathbf{e}$、变形编码 $\mathbf{Z}_t$ 与时序隐变量 $\phi_t$，经 MLP 和反正切函数预测：

$$\mathbf { v } _ { t } = \mathbf { M L P } _ { \mathrm { a n g l e } } ( \mathbf { e } \cdot \mathbf { Z } _ { t } , \phi _ { t } ) , \quad \theta _ { t } = \arctan 2 ( \mathbf { v } _ { t , y } , \mathbf { v } _ { t , x } ) \tag{10}$$

$\mathbf{e} \cdot \mathbf{Z}_t$ 的乘法确保只有可动部件的高斯特征参与角度预测，$\arctan 2$ 输出保证角度在 $[-\pi, \pi]$ 范围内的连续性。

#### 3.3.3 时序一致性正则化

为消除逐帧独立预测导致的运动抖动，引入速度和加速度平滑约束：

$$\mathcal { L } _ { t } = \sum _ { t } \| \theta _ { t } - \theta _ { t - 1 } \| _ { 2 } ^ { 2 } + \lambda _ { \mathrm { a c c } } \sum _ { t } \| \theta _ { t } - 2 \theta _ { t - 1 } + \theta _ { t - 2 } \| _ { 2 } ^ { 2 } \tag{11}$$

第一项惩罚相邻帧旋转角的速度突变，第二项惩罚加速度突变，共同保证铰接运动在时间维度上的物理合理性。

---

### 3.4 模块间因果机制总结

Clay-to-Stone 双阶段设计的因果链路可概括为：

1. **CLAY 阶段**：$\beta_{\mathcal{G}}$（可学习调制因子）$\to$ 柔性变形探索 $\to$ 部件语义发现（通过 $\mathcal{L}_M$ 与 SAM2 对齐）$\to$ 运动先验积累。
2. **阶段过渡**（前 10k 迭代后）：冻结已学习的语义结构，将 $\beta_{\mathcal{G}}$ 经 Gumbel sigmoid 转换为硬性资格信号 $\mathbf{e}$。
3. **STONE 阶段**：$\mathbf{e}$（运动资格）$\to$ 刚性约束施加 $\to$ 转动关节参数 $(\mathbf{l}, \mathbf{p}, \theta_t)$ 显式回归 $\to$ 时序一致性正则（$\mathcal{L}_t$）$\to$ 物理一致的铰接结构。

这一递进式精细化策略的根本优势在于：**避免了从单目观测直接推断刚性铰接参数时面临的形状-运动耦合歧义**，而是先通过柔性阶段解耦部件语义，再在语义先验的引导下施加物理约束。消融实验（Table 4）验证了移除调制机制（w/o modulation）、去除 SAM2 监督（w/o $\mathcal{L}_M$）或消除时序损失（w/o $\mathcal{L}_t$）均导致性能显著退化，证实了各模块的因果必要性。

## 实验与关键发现

### 核心实验设计

实验在 **ARCTIC** 数据集上评估，该数据集包含双手与铰接物体的交互操作序列，涵盖 box、notebook、waffle iron 等具有转动关节的日常物品。评估分为两个维度：**铰接物体几何重建**（Chamfer Distance CD↓、F@5↑、F@10↑）和**手-物真实感渲染**（PSNR↑、SSIM↑、LPIPS↓）。基线方法包括基于 3DGS 的可变形化身 **3DGS-Avatar**（Qian et al., CVPR 2024）以及类别无关的手物重建方法 **HOLD**（Fan et al., CVPR 2024）和 **BIGS**（On et al., CVPR 2025）。

### 铰接物体重建结果

Table 1 展示了在 ARCTIC 数据集上的铰接物体重建定量结果。Clay-to-Stone 在所有物体类别上均取得最优性能，平均 CD 降至 **1.97**，平均 F@5 达到 **0.741**，显著优于 3DGS-Avatar 等可变形基线。这一优势源于 CLAY 阶段建立的部件级语义先验与 STONE 阶段刚性约束的协同作用：前者通过原始级调制因子 $\beta_{\mathcal{G}}$ 实现了对高斯变形的细粒度语义控制，后者则利用资格信号 $\mathbf{e} = g(\beta_{\mathcal{G}})$ 将可动部件约束在转动关节的运动流形上，从而有效解耦了几何形状与铰接运动。

![[assets/figures/papers/paper_list_l2634_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Clay_to_Stone_Phas/figures/003_Table_1.jpg]]
*Table 1: Quantitative results of articulated object reconstruction on ARCTIC*

### 手物真实感渲染结果

Table 2 报告了手物真实感渲染的定量对比。Clay-to-Stone 在 PSNR（平均 **28.17**）、SSIM 和 LPIPS（平均 **35.43**）三项指标上均达到最优。值得注意的是，该方法不仅在新视角合成质量上领先，还能在连续帧间保持稳定的铰接运动表示（见 Figure 5），这得益于时序一致性损失 $\mathcal{L}_t$ 对旋转角度 $\theta_t$ 的速度和加速度正则化：

![[assets/figures/papers/paper_list_l2634_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Clay_to_Stone_Phas/figures/004_Table_2.jpg]]
*Table 2: Quantitative results of hand-object photo-realistic rendering on ARCTIC*

![[assets/figures/papers/paper_list_l2634_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Clay_to_Stone_Phas/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results across continuous frames*

$$\mathcal{L}_t = \sum_t \|\theta_t - \theta_{t-1}\|_2^2 + \lambda_{\text{acc}} \sum_t \|\theta_t - 2\theta_{t-1} + \theta_{t-2}\|_2^2$$

### 与刚体重建方法的比较

Table 3 将 Clay-to-Stone 与假设物体为刚体的 HOLD 和 BIGS 进行了比较。在规范姿态刚体重建任务上，Clay-to-Stone 的 CD 降至 **0.79**，优于专门的刚体重建方法。这表明即使在物体处于静止参考姿态时，CLAY 阶段学习到的语义感知变形先验也有助于更精确的几何恢复——模型能够利用铰接运动序列中的多视角信息来消除单目观测的几何歧义。

![[assets/figures/papers/paper_list_l2634_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Clay_to_Stone_Phas/figures/005_Table_3.jpg]]
*Table 3: Comparison with rigid reconstruction baselines*

### 消融实验

Table 4 系统消融了各关键组件的贡献，揭示了以下因果链路：

![[assets/figures/papers/paper_list_l2634_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Clay_to_Stone_Phas/figures/006_Table_4.jpg]]
*Table 4: Quantitative ablation for box, notebook, and waffle iron includes the average rendering metrics*

- **移除调制机制（w/o modulation）**：去除可学习的原始级调制因子 $\beta_{\mathcal{G}}$ 后，渲染质量大幅下降。这验证了 $\beta_{\mathcal{G}}$ 是控制高斯变形幅度的核心因果旋钮，其与 Gumbel sigmoid 门控的结合使模型能够在 CLAY 阶段灵活探索变形空间，又在 STONE 阶段精确施加刚性约束。

- **去除 SAM2 语义监督（w/o $\mathcal{L}_M$）**：移除基于 SAM2 的部件语义一致性损失后，模型无法保持部件级语义一致性，性能明显退化。这证实了语义一致性损失是建立部件级运动先验的关键监督信号——它通过渲染部件掩膜 $M_{\text{part}}^t$ 与 SAM2 分割对齐，驱动调制因子 $\beta_{\mathcal{G}}$ 学习到语义上有意义的部件划分。

- **消除时序一致性损失（w/o $\mathcal{L}_t$）**：去除时序正则后，旋转角度预测变得不稳定，运动连贯性被破坏。这表明 $\mathcal{L}_t$ 对于从单目视频中学习平滑的铰接运动轨迹至关重要。

- **仅保留 CLAY 自由变形（w/o STONE）**：不施加 STONE 阶段的刚性约束，模型无法恢复物理上合理的铰接结构，在连续帧中表现出明显的几何漂移（见 Figure 5 定性对比）。这直接证明了从柔性变形探索到刚性铰接估计的阶段式过渡是解决几何-运动耦合问题的必要条件。

### 失败模式与局限性

当前框架的一个明确局限是**仅支持单一转动关节**。对于具有多个转动关节或包含棱柱副等混合关节类型的复杂铰接结构，模型的刚性约束机制需要扩展。此外，在 SAM2 分割不可用或手-物严重遮挡的场景下，语义一致性学习的鲁棒性仍需进一步验证。这些方向被作者列为未来工作。

## 定位与知识库关联

### 1. 与基线方法的关系

Clay-to-Stone 框架的核心定位在于填补单目铰接手-物操纵建模中“形状-运动解耦”的空白。其方法谱系可沿两条轴线展开：**变形建模的粒度**与**铰接约束的显式性**。

**相对于类别无关的静态重建方法。** 早期的单目手-物交互重建方法，如 **HOLD** (Fan et al., CVPR 2024) 和 **BIGS** (On et al., CVPR 2025)，虽然能够从视频中恢复手和物体的三维几何，但二者均假设物体为完全刚体。这一假设在铰接操纵场景下必然失效——当用户旋转开瓶盖或翻开笔记本时，物体的几何形状在观测中持续变化。Clay-to-Stone 通过引入可变形高斯原语，首次在类别无关设定下解除了这一刚性假设，直接对部件的铰接运动进行建模。

**相对于无约束变形方法。** **3DGS-Avatar** (Qian et al., CVPR 2024) 等可变形 3DGS 化身基线虽然支持每帧自由变形场，但其变形缺乏部件级语义感知和物理约束。这导致两个关键缺陷：(1) 变形场在稀疏观测下容易过拟合到视角相关的表观，而非学习内在的铰接结构；(2) 无法显式输出可供下游任务使用的铰接参数（旋转轴、枢轴点、角度）。Clay-to-Stone 的 CLAY 阶段继承了这种灵活变形的优势，但通过原始级调制因子 `β_G` 和基于 SAM2 的语义一致性损失，将变形引导至部件语义层面；随后在 STONE 阶段通过刚性约束将柔性表示“凝固”为物理一致的铰接结构，从而实现了从“如何变形”到“为何变形”的跨越。

**关键差异总结。** 在物体变形控制维度，基线采用每帧自由变形场（3DGS-Avatar）或静态物体假设（HOLD/BIGS），缺乏部件语义感知；Clay-to-Stone 则以原始级调制因子 `β_G` 与 Gumbel sigmoid 门控，结合部件语义一致性损失，实现精细、可解释的部件级变形控制（Sec. 3.2 CLAY, Eq. (5-6)）。在铰接建模维度，基线无显式铰接或仅基于骨架的变形；Clay-to-Stone 在 STONE 阶段通过资格信号 `e` 施加刚性约束，并显式回归转动关节参数（旋转轴 `l`、枢轴点 `p`、每帧角度 `θ_t`），辅以时序一致性正则（Sec. 3.3 STONE, Eq. (7-11)）。在训练范式维度，基线均为单一阶段联合优化；Clay-to-Stone 采用双阶段递进策略——CLAY 阶段探索柔性变形并发现语义/运动先验（前 10k 步），STONE 阶段引入刚性约束并联合优化铰接参数与高斯属性。

### 2. 适用边界与条件依赖

Clay-to-Stone 框架的有效性建立在若干隐含假设之上，这些假设同时界定了其适用边界：

- **铰接结构的单一性。** 当前方法假定物体仅包含单一转动关节（revolute joint）。对于具有多部件、多自由度（如棱柱副、球铰）的复杂铰接结构，框架中的资格信号机制和关节参数回归模块需要扩展。这一局限性在论文中被明确列为未来工作方向。
- **2D 语义分割的可用性。** CLAY 阶段的部件语义一致性损失依赖于 SAM2 提供的 2D 部件分割作为监督信号。在 SAM2 不可用、分割质量差、或手-物严重遮挡导致分割失败的场景下，语义一致性学习能否通过其他先验（如视频时序线索）维持，仍是一个开放问题。
- **铰接运动的理想性。** STONE 阶段的刚性约束假设铰接运动是理想的转动运动，未考虑摩擦、间隙、少量非刚性变形（如塑料瓶盖的弹性变形）等非理想因素。在极端情况下，刚性约束可能抑制对真实物理行为的拟合能力。
- **规范空间的初始化质量。** 方法在规范空间中随机采样 5,000 个点初始化物体高斯，并依赖自适应密度控制（克隆/分裂/剪枝）来优化高斯分布。初始采样策略和密度控制机制对最终重建质量的影响尚需进一步分析。

### 3. 局限与开放问题

**已识别的局限。** 除上述适用边界外，论文明确指出的核心局限是：当前框架仅支持单一转动关节的铰接建模。从方法学角度看，这一局限的根源在于 STONE 阶段设计的资格信号 `e = g(β_G)` 本质上是一个二值门控——它区分“可动”与“静止”区域，但无法处理多个可动部件各自独立运动的场景。要将框架推广至多转动关节或混合关节物体，需要将资格信号从标量扩展为向量，并为每个运动部件独立回归关节参数。

**开放问题。** 基于上述分析，可归纳出以下待探索的方向：

1. **多关节推广。** 如何将 Clay-to-Stone 的“语义感知调制 → 刚性约束巩固”范式推广至多转动关节或混合关节的物体？这需要在部件语义发现阶段就支持多部件分割，并在 STONE 阶段设计多组关节参数的联合回归与约束机制。

2. **语义监督的鲁棒性。** 在缺少准确 2D 部件分割（如 SAM2 不可用）或手-物严重遮挡的场景下，语义一致性学习能否通过其他先验（例如视频时序线索、光流一致性）维持？这关系到方法在真实世界非受控视频中的部署可行性。

3. **刚性约束的容错性。** STONE 阶段的刚性约束是否足够鲁棒以处理非理想铰接（如摩擦、少量非刚性变形）？引入软约束或不确定性建模可能是缓解这一问题的途径。

4. **训练效率与收敛性。** 双阶段训练范式引入了阶段切换的时机选择（当前固定为 10k 迭代）。这一超参数对不同物体类别的敏感性，以及是否存在自适应的阶段切换策略，值得进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Clay_to_Stone_Phase_wise_3D_Gaussian_Splatting_for_Monocular_Articulated_Hand_Object_Manipulation_Modeling.pdf]]

---
title: "ArtHOI: Articulated Human-Object Interaction Synthesis by 4D Reconstruction from Video Priors"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstruction_from_Video_Priors.pdf
project_link: https://arthoi.github.io/
code_link: null
aliases:
- ArtHOI
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 解耦的两阶段重建管道：第一阶段利用光流引导的部件分割与运动学约束恢复物体铰接运动，第二阶段在固定物体骨架下优化人体运动，从而消除歧义并实现铰接交互。
primary_logic: 将铰接式人物交互合成转化为从视频先验中进行4D重建的逆渲染问题，利用光流等几何线索进行部件分割，并通过分解优化将2D监督提升为几何与物理一致的4D表示。
claims:
- 在铰接场景交互质量评估中，ArtHOI的接触百分比（75.64%）较零样本基线ZeroHSI（61.95%）提升13.69个百分点，穿透百分比（0.08%）较ZeroHSI（1.49%）大幅降低。
- 消融实验表明，将两阶段解耦替换为联合优化后，接触百分比从75.64%骤降至61.45%；移除运动学损失（L_k）使接触百分比降至59.82%，证明分解优化和接触约束的关键作用。
- 用户研究中，98.04%的参与者总体偏好ArtHOI over TRUMANS，且在物理合理性、动作自然度、铰接真实性和外观一致性四个维度上均显著优于基线。
- Various Articulated Scenes (Table 2) 上 Contact% = 75.64
---

# ArtHOI: Articulated Human-Object Interaction Synthesis by 4D Reconstruction from Video Priors

> [!tip] 核心洞察
> 将铰接式人物交互合成转化为从视频先验中进行4D重建的逆渲染问题，利用光流等几何线索进行部件分割，并通过分解优化将2D监督提升为几何与物理一致的4D表示。

| 字段 | 内容 |
|------|------|
| 中文题名 | ArtHOI：通过视频先验的4D重建进行铰接式人物交互合成 |
| 英文题名 | ArtHOI: Articulated Human-Object Interaction Synthesis by 4D Reconstruction from Video Priors |
| 会议/期刊 | arXiv 2026 |
| Links | [Project](https://arthoi.github.io/) · [paper](https://arxiv.org/abs/2603.04338) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ArtHOI |
| Dataset | Various Articulated Scenes, Articulated Object Dynamics, Rigid Object Scenes |

> [!tip] 效果简介
> - Various Articulated Scenes (Table 2) 上，Contact% 75.64 vs 61.95 (ZeroHSI) (+13.69)；Penetration% 0.08 vs 1.49 (ZeroHSI) (-1.41)；X-CLIP Score 0.244 vs (baseline not provided) (N/A)。
> - Articulated Object Dynamics (Table 3) 上，Rotation Error Mean (°) 6.71 vs N/A (other methods cannot model articulation) (N/A)。
> - Rigid Object Scenes (Table 4) 上，Contact% 76.18 vs (outperforms previous methods) (N/A)。

## 概要

从单目视频中合成人与铰接物体的自然交互，是构建沉浸式虚拟世界的关键技术。现有方法面临一个根本瓶颈：**零样本方法将物体视为单一刚体，无法建模铰接部件的独立运动**（如开门时门板的旋转与门框的静止），而联合优化人体与物体动态则因单目歧义和梯度冲突，难以生成物理一致的4D场景。

**ArtHOI** 将铰接式人物交互合成重新定义为**从视频先验中进行4D重建的逆渲染问题**。其核心洞察在于：利用光流等几何线索进行部件分割，通过**解耦的两阶段优化**将2D监督提升为几何与物理一致的4D表示——先恢复物体的铰接运动骨架，再在固定骨架下优化人体运动，从而消除联合优化的歧义性。

在方法谱系中，ArtHOI 填补了零样本4D生成与铰接物体建模之间的空白。相较于有监督方法 **TRUMANS**（Jiang et al., CVPR 2024）需依赖3D标注数据，以及零样本方法 **ZeroHSI**（Li et al., arXiv 2024）仅支持刚体变换，ArtHOI 首次在零样本条件下同时实现RGB渲染、铰接建模、物理约束与跨场景泛化（Table 1）。

实验表明，ArtHOI 在铰接场景交互质量上显著超越基线：接触百分比达75.64%（ZeroHSI为61.95%），穿透百分比仅0.08%（ZeroHSI为1.49%）。消融实验证实，解耦策略与运动学损失是性能的关键保障——移除任一组件均导致接触率骤降至约60%。用户研究中，98.04%的参与者总体偏好ArtHOI，在物理合理性、动作自然度、铰接真实性和外观一致性四个维度上均显著占优。

方法目前局限于单自由度铰接与静态相机场景，对低纹理表面的光流跟踪失败是主要失效模式。



### 问题背景

在三维视觉与图形学中，合成真实的人与物体交互（Human-Object Interaction, HOI）是构建沉浸式数字体验的核心技术。然而，现实世界中的物体往往不是单一刚体——门可以旋转、抽屉可以抽拉、笔记本电脑可以开合——这些**铰接式物体**通过多个部件的相对运动实现功能，而人类与它们的交互天然需要与这些运动部件协调配合。

从单目视频中恢复这种铰接式人物交互的完整4D场景（3D几何+时间动态）极具挑战。单目输入本身存在深度歧义，而铰接物体的多部件运动进一步放大了这种不确定性：系统需要同时推断物体的部件结构、各部件的运动参数，以及人体如何适应这些运动。

### 现有方法的缺口

当前的人-物交互合成方法存在两个关键瓶颈：

**瓶颈一：物体建模的刚性假设。** 大多数零样本方法——如 **ZeroHSI**（Li et al., arXiv 2024）——将交互物体视为单一刚体，仅估计一个全局的旋转和平移变换。这种简化在面对铰接物体时完全失效：门扇的旋转、抽屉的平移、椅背的折叠等铰接运动无法用单一刚体变换描述。有监督方法如 **TRUMANS**（Jiang et al., CVPR 2024）虽然能处理动态场景，但依赖昂贵的3D监督数据，无法泛化到开放世界中的新物体类别。**D3D-HOI**（Xu et al., arXiv 2021）尝试从视频重建铰接对象交互，但仍需要多视图或深度输入。

**瓶颈二：联合优化的歧义与梯度冲突。** 当系统试图同时优化人体运动和物体铰接时，单目信号的固有歧义会导致两个优化目标相互干扰。人体姿态的微小调整可能被误解释为物体部件的运动，反之亦然。这种梯度冲突使得联合优化极易陷入局部最优，产生物理上不一致的结果——例如手穿透物体表面、接触点漂移、或物体部件运动违背运动学约束。

### 本文动机

ArtHOI 的核心洞察在于：**将铰接式人物交互合成重新定义为从视频先验中进行4D重建的逆渲染问题**。给定一段由扩散模型生成的单目视频，系统不依赖任何3D监督，而是利用光流等2D几何线索来推断场景的完整4D表示。

这一思路的关键在于**分解优化策略**：与其让人体和物体在歧义中相互干扰，不如先利用视频中的几何证据恢复物体的铰接结构，再在固定的物体骨架下优化人体运动。这种两阶段解耦从根本上消除了联合优化的歧义源，使得2D监督能够被有效提升为几何一致、物理逼真的4D场景。



## 核心方法与创新机理

ArtHOI 的核心创新在于将**铰接式人物交互（Articulated HOI）合成**重新定义为**从单目视频先验中进行4D重建的逆渲染问题**，并通过**解耦的两阶段优化管道**解决了零样本场景下铰接建模与物理一致性两大瓶颈。

### 1. 问题形式化转换：从生成到4D重建

现有零样本方法（如 **ZeroHSI**，Li et al., arXiv 2024）将交互合成视为联合生成人体与物体动态的任务，但面临两个根本性困难：一是将物体视为单一刚体，无法建模铰接部件（如旋转门、抽屉）的运动；二是单目视频下联合优化人体与物体动态存在严重歧义与梯度冲突，难以生成物理一致的4D场景。

ArtHOI 的**核心洞察**在于：给定一段由扩散模型生成的视频先验，其中已经隐含了丰富的几何与运动线索（光流、掩码、接触区域）。因此，交互合成本质上是一个**从2D监督中提升出几何与物理一致的4D表示**的逆渲染问题，而非从零生成运动。这一形式化转变使得方法可以直接利用光流、分割等几何线索来驱动重建，避免了对3D监督数据的依赖。

### 2. 解耦两阶段重建：消除单目歧义

ArtHOI 最关键的架构创新是**解耦的两阶段重建管道**（Figure 2），将物体铰接恢复与人体运动优化分离为两个顺序步骤：

- **阶段I：物体铰接重建**。先独立恢复物体的铰接运动，获得一个固定的4D骨架（包括动态部件的旋转/平移变换序列）。
- **阶段II：人体运动优化**。在阶段I得到的物体4D骨架约束下，优化SMPL-X人体参数，使其与物体产生物理合理的接触与交互。

这一解耦策略的因果机制在于：**单目歧义主要源于人体与物体运动的耦合**——当两者同时优化时，模型无法区分是人在动还是物体在动。通过先固定物体运动骨架，阶段II的人体优化问题变得良定，从而大幅降低了歧义空间。

消融实验直接验证了这一设计的必要性：将解耦两阶段替换为单阶段联合优化后，接触百分比从 **75.64% 骤降至 61.45%**，旋转平均误差从 **6.71° 恶化至 12.34°**（Table 6），证明解耦是交互质量的关键保障。

### 3. 基于光流的部件分割与准静态绑定

为在无3D监督的条件下恢复物体铰接结构，ArtHOI 设计了**基于光流的部件分割管道**（Figure 3a-b），包含三个关键环节：

1. **光流驱动的动态/静态识别**：通过点跟踪（Co-tracker）获取视频中的运动轨迹，聚类识别哪些像素区域发生了运动，哪些保持静止。
2. **SAM引导的稠密掩码生成**：以动态/静态点作为提示，利用SAM（Segment Anything Model）生成稠密的部件掩码 $M^d(t)$（Eq. 1），并通过反投影将2D掩码提升至3D高斯表示。
3. **准静态绑定（Quasi-static Binding）**：在铰接边界处，寻找每个准静态动态高斯 $\mathbf{g}^{qs}$ 在半径 $r$ 内的最近静态高斯 $\mathbf{g}^{st}$，构建绑定对集合 $\mathcal{E}$（Eq. 2）。这些绑定对为后续的运动学正则化提供了几何约束基础——铰接运动必须保持绑定对之间的距离不变。

这一设计的创新在于：**无需任何3D标注或CAD模型**，仅从2D光流和分割中自动发现物体的铰接结构，实现了真正的零样本铰接理解。

### 4. 从2D证据推导3D接触约束

传统方法缺乏显式的接触监督，仅依靠重建损失隐式约束交互，导致穿透和接触缺失问题严重。ArtHOI 提出了一套**从2D证据推导3D接触关键点**的机制（Figure 3c），包括四个步骤：

1. **接触帧选择**：识别视频中手部与物体区域重叠的帧。
2. **2D接触区域提取**：在接触帧中定位手部与物体的2D接触区域。
3. **关节分配**：将2D接触点分配给SMPL-X手部关节。
4. **3D提升**：利用阶段I恢复的物体深度，将2D接触点提升为3D接触关键点 $\mathbf{K}_j(t)$。

基于这些3D接触关键点，阶段II引入**运动学损失 $\mathcal{L}_k$**（Eq. 9），直接将手部关节拉向目标接触点。消融实验表明，移除 $\mathcal{L}_k$ 后接触百分比从 **75.64% 降至 59.82%**（Table 6），证明这一从2D到3D的接触推导机制是维持物理交互的核心组件。

### 5. 铰接运动学正则化

为确保铰接运动的几何一致性，ArtHOI 在阶段I中引入了两个互补的正则化损失（Eq. 6）：

- **准静态距离保持损失 $\mathcal{L}_a$**：强制准静态绑定对在运动前后保持距离不变，这对应于铰接运动的刚体约束——铰接部件上的点与静态部件上对应点的距离在旋转过程中不应改变。
- **跟踪损失 $\mathcal{L}_{tr}$**：将动态部件的3D运动轨迹与2D光流跟踪结果对齐，确保铰接变换与视频证据一致。

移除 $\mathcal{L}_a$ 后，旋转平均误差从 **6.71° 飙升至 15.67°**（Table 6），验证了准静态绑定约束对铰接精度的决定性作用。

### 6. 与基线方法的差异化定位

相较于现有方法，ArtHOI 在四个关键维度上实现了系统性突破（Table 1）：

| 方法 | RGB渲染 | 铰接对象 | 物理约束 | 零样本 |
|------|---------|----------|----------|--------|
| TRUMANS (Jiang et al., CVPR 2024) | ✓ | ✗ | ✗ | ✗ |
| LINGO (Jiang et al., SIGGRAPH Asia 2024) | ✓ | ✗ | ✗ | ✗ |
| CHOIS (Li et al., ECCV 2024) | ✓ | ✗ | ✗ | ✗ |
| ZeroHSI (Li et al., arXiv 2024) | ✓ | ✗ | ✗ | ✓ |
| **ArtHOI** | ✓ | ✓ | ✓ | ✓ |

ArtHOI 是首个同时实现RGB渲染、铰接对象建模、物理约束和零样本泛化四个能力的方法。其根本差异在于：**将物体运动建模从单一刚体变换升级为基于光流分割的铰接变换**，并通过解耦优化与显式接触约束，将2D视频先验提升为几何与物理一致的4D表示。



ArtHOI 将铰接式人物交互（HOI）合成重新定义为一个**从单目视频先验进行4D重建的逆渲染问题**：给定一段由扩散模型生成的视频，在没有三维监督的情况下，重建出完整的铰接式4D场景 [Abstract]。这一范式转换的核心动机在于，现有零样本方法（如 **ZeroHSI**，Li et al., arXiv 2024）将物体视为单一刚体，无法建模铰接部件的运动，且人体与物体动态的联合优化在单目歧义下极易导致梯度冲突，难以生成物理一致的交互 [analysis_truth]。

为消除上述歧义，ArtHOI 采用**解耦的两阶段重建管道**（Fig. 2），其输入-输出流如下：

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/003_Figure_2.jpg]]
*Figure 2: ArtHOI synthesizes 3D articulated interactions by reconstructing 4D scenes from monocular video priors. Stage I reconstructs object articulation with kinematic constraints. Stage II refines human motion under the reconstructed geometry*

1. **输入**：一段单目 RGB 视频（由扩散模型生成），以及预训练的 SMPL-X 人体参数估计和 3D Gaussian Splatting 初始化。
2. **预处理**：通过光流点跟踪与 SAM 引导的掩码，将场景分解为人体、动态物体部件与静态物体部件，并构建准静态绑定对（quasi-static binding pairs）。
3. **阶段 I：物体铰接重建**（Algorithm 1）——在固定物体骨架的前提下，逐帧优化动态部件的铰接变换 $\mathbf{T}^d(t)$（旋转与平移），利用重建损失 $\mathcal{L}_r^o$、铰接正则化损失 $\mathcal{L}_a$、平滑损失 $\mathcal{L}_s$ 和跟踪损失 $\mathcal{L}_{tr}$ 恢复物体的4D运动骨架。
4. **阶段 II：人体运动精炼**（Algorithm 2）——在阶段 I 输出的固定物体4D骨架下，联合优化 SMPL-X 参数 $\theta$，引入从2D证据推导的3D接触关键点，通过运动学损失 $\mathcal{L}_k$ 拉近手部关节与目标点，并辅以碰撞损失 $\mathcal{L}_c$ 防止穿透，最终输出物理逼真的铰接式交互4D场景。

**关键设计决策**：两阶段的解耦是框架的核心因果调控旋钮。消融实验表明，若将解耦替换为单阶段联合优化，接触百分比将从 75.64% 骤降至 61.45%，旋转平均误差从 6.71° 升至 12.34°，证明分解优化对消除单目歧义和维持交互质量至关重要 [Table 6]。

**模块关系**：预处理中的“光流部件分割”为阶段 I 提供动态/静态掩码；“准静态绑定”在铰接边界构建动态-静态高斯对，为 $\mathcal{L}_a$ 提供约束；阶段 I 输出的物体4D骨架与接触关键点直接馈入阶段 II，作为人体运动优化的几何条件。整个管道无需多视图或3D监督，仅依赖2D视频先验即可生成几何与物理一致的4D表示。

### 补充图表

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/001_Figure_1.jpg]]
*Figure 1: ArtHOI recovers zero-shot articulated human-object scene geometry and dynamics from monocular video priors without 3D supervision. Unlike prior works (e.g., TRUMANS, ZeroHSI), our method achieves all four capabilities simultaneously: RGB rendering, articulated object modeling, physical constraint modeling, and zero-shot generalization, notably without using 3D supervision*



ArtHOI 将铰接式人物交互合成形式化为一个从单目视频先验中进行 4D 重建的逆渲染问题。其核心架构围绕**解耦的两阶段重建管道**展开，通过将物体铰接恢复与人体运动优化分离，消除单目歧义与梯度冲突。以下逐一剖析关键模块及其数学基础。

---

### 3.1 基于光流的部件分割与准静态绑定

**模块目标**：从单目 RGB 视频中识别物体的动态（铰接）部件与静态部件，并为后续运动学约束建立几何对应关系。

**流程**：
1. **点跟踪与 SAM 引导掩码**：使用 Co-tracker 在视频序列中跟踪稀疏点，根据运动模式将点分为动态点集 $\mathcal{P}^d$ 与静态点集 $\mathcal{P}^s$。以这些点作为提示，调用 SAM 生成稠密的动态部件二值掩码：

$$M^d(t) = \mathsf{SAM}(I(t), \mathcal{P}^d, \mathcal{P}^s) \quad \text{(Eq. 1)}$$

2. **3D 反投影**：将掩码区域对应的 3D 高斯反投影至初始帧的物体高斯场，从中识别出动态高斯集 $\mathcal{G}^d$ 与静态高斯集 $\mathcal{G}^s$。其中，位于铰接边界附近、运动幅度较小的动态高斯被标记为准静态高斯 $\mathcal{G}^{qs}$。

3. **准静态绑定**：对每个准静态动态高斯 $\mathbf{g}^{qs}$，在半径 $r$ 内搜索最近的静态高斯 $\mathbf{g}^{st}$，构成绑定对集合：

$$\mathcal{E} = \{ [\mathbf{g}^{qs}, \mathbf{g}^{st}] \mid \mathbf{g}^{qs} \in \mathcal{G}^d, \Pi(\mathbf{g}^{qs}) \in \mathcal{P}^{qs}, \mathbf{g}^{st} \in \mathcal{G}^s, \|\mathbf{g}^{qs} - \mathbf{g}^{st}\|_2 \leq r \} \quad \text{(Eq. 2)}$$

**设计意图**：准静态绑定对位于铰接边界两侧，它们在物理上应保持相对距离不变。这为阶段 I 的运动学正则化提供了无需 3D 监督的几何约束。

---

### 3.2 阶段 I：物体铰接重建

**模块目标**：在固定相机假设下，逐帧恢复物体的铰接变换参数，输出一个 4D 物体骨架。

**核心机制**：将物体高斯场建模为动态部分与静态部分的加权组合。动态高斯的位置由铰接变换 $\mathbf{T}^d(t) = [\mathbf{R}^d(t) | \mathbf{t}^d(t)]$ 驱动，静态高斯保持不变：

$$\pmb{\mu}_i^o(t) = w_i^d \mathbf{T}^d(t) \pmb{\mu}_i^o(0) + w_i^s \pmb{\mu}_i^o(0) \quad \text{(Eq. 3)}$$

其中 $w_i^d, w_i^s \in \{0, 1\}$ 为二值权重，指示该高斯属于动态或静态部件。当前实现假设单自由度旋转铰接，$\mathbf{R}^d(t)$ 为绕固定轴旋转矩阵。

**优化目标**（逐帧，从前一帧热启动）：

$$\min_{\{\mathbf{R}^d, \mathbf{t}^d\}} \mathcal{L}_r^o + \lambda_a \mathcal{L}_a + \lambda_s \mathcal{L}_s + \lambda_{tr} \mathcal{L}_{tr} \quad \text{(Eq. 4)}$$

各损失项含义：

- **$\mathcal{L}_r^o$（重建损失）**：渲染的物体 RGB 图像与原始视频帧的 $\ell_2$ 误差，确保外观一致。
- **$\mathcal{L}_a$（铰接正则化损失）**：强制准静态绑定对在运动前后保持距离不变，防止铰接部件漂移脱离物体本体：

$$\mathcal{L}_a = \sum_{(\mathbf{g}^d, \mathbf{g}^s) \in \mathcal{E}} \|d(\mathbf{g}^d(t), \mathbf{g}^s(t)) - d(\mathbf{g}^d(0), \mathbf{g}^s(0))\|_2^2 \quad \text{(Eq. 6)}$$

- **$\mathcal{L}_{tr}$（跟踪损失）**：将动态高斯的 2D 投影与 Co-tracker 跟踪点对齐，为铰接变换提供稀疏 2D 监督：

$$\mathcal{L}_{tr} = \sum_{i \in \mathcal{P}_{\mathrm{dyn}}} \|\hat{p}_{\mathrm{tgt}}^i - p_{\mathrm{tgt}}^i\|_2^2 \quad \text{(Eq. 6)}$$

- **$\mathcal{L}_s$（平滑损失）**：惩罚相邻帧间铰接参数的突变，保证时序连贯。

**证据强度**：消融实验（Table 6）表明，移除 $\mathcal{L}_a$ 后旋转平均误差从 6.71° 增至 15.67°，验证了准静态绑定约束对铰接精度的关键作用。

---

### 3.3 阶段 II：人体运动精炼

**模块目标**：在阶段 I 输出的固定物体 4D 骨架之上，优化 SMPL-X 人体参数 $\theta$，生成与物体铰接状态物理一致的交互运动。

**3D 接触关键点推导**（Fig. 3c）：从 2D 证据中提取接触约束，分四步：
1. **接触帧选择**：基于光流幅值检测手部与物体区域重叠的帧。
2. **2D 接触区域**：取手部掩码与物体动态部件掩码的交集。
3. **关节分配**：将接触区域中心分配给最近的 SMPL-X 手部关节。
4. **3D 提升**：利用阶段 I 恢复的物体深度，将 2D 接触点反投影为 3D 接触关键点 $\mathbf{K}_j(t)$。

**优化目标**：

$$\operatorname*{min}_{\theta} \mathcal{L}_r^h + \lambda_p \mathcal{L}_p + \lambda_{fs} \mathcal{L}_{fs} + \lambda_s \mathcal{L}_s + \lambda_k \mathcal{L}_k + \lambda_c \mathcal{L}_c \quad \text{(Eq. 7)}$$

各损失项含义：

- **$\mathcal{L}_r^h$（人体重建损失）**：渲染人体 RGB 与掩码与视频帧对齐。
- **$\mathcal{L}_p$（先验损失）**：将姿态 $\theta$ 和表情 $\psi$ 约束在 VDM（Video Diffusion Model）估计值附近，防止优化偏离合理分布。
- **$\mathcal{L}_{fs}$（足部滑动损失）**：惩罚足部接触地面时的速度，减少滑步伪影。
- **$\mathcal{L}_s$（平滑损失）**：抑制相邻帧间姿态突变。
- **$\mathcal{L}_k$（运动学损失）**：将手部关节拉向 3D 接触关键点，是实现物理接触的核心驱动力：

$$\mathcal{L}_k = \sum_{t=1}^T \sum_{j \in \mathcal{K}_t} \| \mathbf{J}_j(\pmb{\theta}(t)) - \mathbf{K}_j(t) \|_2^2 \quad \text{(Eq. 9)}$$

- **$\mathcal{L}_c$（碰撞损失）**：惩罚手部顶点 $\mathcal{V}_h$ 穿透物体表面 $\mathcal{Q}^o$，设置安全距离 $\delta$：

$$\mathcal{L}_c = \sum_{t=1}^T \sum_{v \in \mathcal{V}_h} \sum_{q \in \mathcal{Q}^o} \operatorname*{max}(0, \delta - d_{vq}) \quad \text{(Eq. 10)}$$

**证据强度**：消融实验（Table 6）显示，移除 $\mathcal{L}_k$ 后接触百分比从 75.64% 骤降至 59.82%，证明接触关键点对维持物理交互不可或缺。移除 $\mathcal{L}_s$ 则导致运动抖动增加、足部滑动指标恶化。

---

### 3.4 关键设计决策与瓶颈分析

**解耦 vs. 联合优化**：消融实验将两阶段解耦替换为单阶段联合优化后，接触百分比从 75.64% 降至 61.45%，旋转误差从 6.71° 升至 12.34°（Table 6）。这验证了核心洞察：单目条件下同时优化人体与铰接物体导致梯度冲突与歧义放大，解耦策略通过先固定物体骨架再优化人体，有效消除了这一瓶颈。

**光流依赖的脆弱性**：部件分割与跟踪损失均依赖 Co-tracker 的点跟踪质量。在低纹理或反光表面，跟踪失败会导致掩码错误与铰接预测失真（见 Fig. 6 失败案例），这是当前管道的主要失效模式。

### 补充图表

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/005_Figure.jpg]]

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/006_Figure.jpg]]



## 实验与关键发现

### 实验设置

ArtHOI 在零样本设定下与有监督方法 **TRUMANS**（Jiang et al., CVPR 2024）、**LINGO**（Jiang et al., SIGGRAPH Asia 2024）、**CHOIS**（Li et al., ECCV 2024），零样本方法 **ZeroHSI**（Li et al., arXiv 2024），以及铰接对象重建方法 **D3D-HOI**（Xu et al., arXiv 2021）、**3DADN**（Qian et al., CVPR 2022）进行对比。评估维度涵盖交互质量与铰接精度：X-CLIP Score 衡量文本-视频语义对齐，Smoothness 与 Foot Sliding 评估运动自然度，Contact% 与 Penetration% 量化物理交互质量，Rotation Error 则专门评估铰接物体动态恢复精度。

### 铰接场景交互质量主结果

在包含多种铰接场景的测试集上，ArtHOI 在物理交互质量上显著超越所有基线。如 Table 2 所示，ArtHOI 的接触百分比（Contact%）达到 **75.64%**，较零样本基线 ZeroHSI 的 61.95% 提升 **13.69 个百分点**；穿透百分比（Penetration%）仅为 **0.08%**，较 ZeroHSI 的 1.49% 大幅降低，表明解耦重建策略有效消除了人体与物体间的穿透伪影。在语义对齐方面，ArtHOI 的 X-CLIP Score 为 **0.244**，同样优于对比方法。

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/008_Table_2.jpg]]

> ⚠️ **公平性说明**：在解读 Smoothness 指标时需特别注意——非零样本方法（如 TRUMANS）的高平滑度源于其几乎不产生接触，而非运动更自然。在零样本方法中，ArtHOI 的平滑度（0.87）具有竞争力，同时实现了远优于基线的接触率。

定性对比（Fig. 4）进一步印证了量化结果：ArtHOI 生成的交互序列展现出正确的接触姿态与自然的运动协调，而基线方法常出现手部穿透物体或接触缺失的问题。

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of our method with baselines. Our method synthesizes more realistic articulated human-object interactions with proper contact and natural motion coordination. Better inspected in our supplementary video*

### 铰接物体动力学精度

Table 3 报告了铰接物体动态恢复的定量评估。ArtHOI 在单目设定下的旋转平均误差仅为 **6.71°**，而其他方法因无法建模铰接运动，无法在此指标上进行比较。这一结果验证了基于光流分割与运动学约束的 Stage I 能够从单目视频中可靠地恢复物体的铰接运动参数。

### 刚体场景泛化能力

尽管 ArtHOI 专为铰接交互设计，其在刚体场景中同样表现优异。如 Table 4 所示，ArtHOI 在刚体场景下的 Contact% 达到 **76.18%**，超越此前方法，证明解耦框架对非铰接物体同样具有鲁棒性。

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/009_Table_4.jpg]]

### 用户研究

Table 5 报告了用户研究结果：**98.04%** 的参与者总体偏好 ArtHOI over TRUMANS，且在物理合理性、动作自然度、铰接真实性和外观一致性四个维度上均显著优于所有基线。该结果从人类感知层面强有力地验证了 ArtHOI 生成交互的逼真度。

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/011_Table_5.jpg]]

### 消融实验

Table 6 的系统消融揭示了各组件的关键作用：

- **解耦两阶段 → 联合优化**：将两阶段解耦替换为单阶段联合优化后，Contact% 从 75.64% 骤降至 **61.45%**，Rotation Mean Error 从 6.71° 升至 **12.34°**。这直接证明了联合优化在单目歧义下遭受严重的梯度冲突，解耦是保证交互质量的核心设计。
- **移除运动学损失 $L_k$**：Contact% 降至 **59.82%**，表明从 2D 证据推导的 3D 接触关键点对维持物理交互至关重要。
- **移除铰接正则化损失 $L_a$**：Rotation Mean Error 增至 **15.67°**，铰接精度大幅下降，验证了准静态绑定对约束对在保持铰接运动几何一致性中的关键作用。
- **移除平滑损失 $L_s$**：运动抖动增加，足部滑动指标恶化，说明时序平滑正则化对生成自然运动不可或缺。

完整模型在所有指标（X-CLIP 0.244, Foot Sliding 0.31, Contact% 75.64, Rot Mean 6.71°）均达到最优，消融实验一致表明每个损失项和解耦策略均对最终性能有不可替代的贡献。

### 失败模式分析

Fig. 6 展示了典型失败案例。ArtHOI 的核心瓶颈在于其对光流点跟踪（Co-tracker）质量的依赖：在低纹理或反光表面区域，点跟踪容易漂移或丢失，导致部件分割错误，进而传播为铰接预测的几何失真。此外，当前方法仅处理单自由度铰接（如门的旋转），尚未扩展至多自由度或非刚性变形；长时序（>30 帧）场景中可能出现关节漂移；且方法假设静态相机，对大幅移动相机的场景未作验证。

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/013_Figure_6.jpg]]
*Figure 6: Failure cases. Co-tracker struggles with low-texture or reflective regions, leading to distortions that propagate into articulation prediction*

### 补充图表

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/012_Table.jpg]]
*Table: Ablation study results. We remove individual components and evaluate their impact on both interaction and articulation*

![[assets/figures/papers/paper_list_l1699_ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstructi/figures/002_Table_1.jpg]]



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有的人-物交互（HOI）合成方法在铰接场景下面临两个结构性瓶颈：

- **物体建模的刚体假设**：绝大多数零样本方法（如 **ZeroHSI** (Li et al., arXiv 2024)）将交互物体视为单一刚体，仅优化全局旋转与平移，无法建模门、抽屉、笔记本电脑等物体的部件级铰接运动。这使得生成的交互在几何层面就与真实物理世界脱节。
- **联合优化的单目歧义**：从单目视频同时恢复人体运动与物体铰接是一个高度欠定问题。人体姿态与物体部件的运动在2D投影上容易混淆，联合优化时梯度冲突严重，导致收敛到物理不一致的局部极小值。

有监督方法（如 **TRUMANS** (Jiang et al., CVPR 2024)）虽然可以建模铰接交互，但依赖昂贵的3D监督数据，缺乏零样本泛化能力。**D3D-HOI** (Xu et al., arXiv 2021) 和 **3DADN** (Qian et al., CVPR 2022) 分别探索了动态交互重建和视频中的物体关节理解，但前者需要多视角输入，后者仅处理物体本身而不涉及人体交互。ArtHOI 正是在这一交叉空白处提出：在零样本、单目设定下同时实现铰接物体建模与物理一致的交互合成。

### 2. 方法谱系中的位置

ArtHOI 将铰接式 HOI 合成重新定义为**从视频先验中进行4D重建的逆渲染问题**，在方法谱系中占据了“零样本 + 铰接 + 物理约束”这一此前未被覆盖的象限（见 Table 1 的能力对比）。其核心设计决策——**解耦的两阶段重建管道**——直接回应了上述两个瓶颈：

- **阶段I**：先利用光流引导的部件分割与准静态绑定，在运动学约束下恢复物体的铰接运动骨架，获得固定的4D几何支架。
- **阶段II**：在固定物体骨架的条件下优化人体 SMPL-X 参数，通过从2D证据推导的3D接触关键点和运动学损失 $L_k$ 确保物理逼真。

这种“先物体后人体”的分解优化策略，本质上是通过**消除优化变量间的耦合歧义**来稳定单目重建。相较于 ZeroHSI 的联合优化范式，ArtHOI 的解耦设计将接触百分比从 61.45% 提升至 75.64%（Table 6 消融实验），铰接旋转平均误差从 12.34° 降至 6.71°，证明了分解策略的关键作用。

### 3. 适用边界

ArtHOI 的适用边界由以下假设和依赖条件界定：

- **单自由度铰接**：当前方法仅处理绕固定轴旋转的铰接（如门的开合），尚未扩展至多自由度机构（如折叠椅）或非刚性变形（如柔性物体）。
- **静态相机假设**：方法假定相机在场景中保持静止，对大幅移动相机的场景未作验证。相机运动将破坏光流分割中动态/静态部件的判别逻辑。
- **光流跟踪依赖**：部件分割和准静态绑定严重依赖 Co-tracker 的点跟踪质量。在低纹理或反光表面（如白色柜门、金属表面），跟踪失败会导致铰接预测失真（见 Fig. 6 失败案例）。
- **短时序优化**：当前逐帧优化策略在长序列（>30帧）上可能出现关节漂移，长时序一致性仍有待加强。

### 4. 局限与开放问题

基于上述边界，以下问题值得后续工作关注：

1. **多自由度与非刚性扩展**：如何将铰接建模从单轴旋转推广至多自由度运动链，乃至非刚性变形物体（如折叠伞、织物），是提升方法通用性的关键方向。

2. **移动相机下的4D重建**：能否在相机运动条件下恢复4D场景并保证时空一致性？这需要同时估计相机位姿与场景动态，复杂度显著增加。

3. **长序列稳定性**：当前逐帧优化缺乏全局时序约束，误差累积问题在长序列中尤为突出。引入循环优化或关键帧机制可能是缓解方向。

4. **光流跟踪失败的鲁棒替代**：当 Co-tracker 在低纹理区域失效时，是否存在更鲁棒的几何线索（如深度估计、法线预测）可以补充或替代光流信号？这直接关系到方法在真实场景中的可用性。

5. **与生成模型的深度整合**：ArtHOI 目前将扩散模型生成的视频作为“先验”输入，但两阶段管道与生成过程本身是解耦的。是否可以将物理约束（如接触损失、碰撞损失）直接嵌入扩散模型的去噪过程，实现“生成即物理一致”的端到端范式，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/arxiv_2026/ArtHOI_Articulated_Human_Object_Interaction_Synthesis_by_4D_Reconstruction_from_Video_Priors.pdf]]

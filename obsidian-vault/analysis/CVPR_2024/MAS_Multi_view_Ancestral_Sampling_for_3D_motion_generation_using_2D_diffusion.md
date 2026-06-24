---
title: "MAS: Multi-view Ancestral Sampling for 3D Motion Generation Using 2D Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diffusion.pdf
aliases:
- MVASM
- MAS
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 在2D扩散模型的祖先采样过程中引入多视角一致性机制：同时去噪多个2D视图，每步通过三角化与重投影强制共享3D运动，并使用3D噪声投影保持多视图噪声分布一致。
primary_logic: 在扩散去噪每一步将多个2D视图约束为同一3D运动的投影，以一致的方式逐步生成3D运动，使得仅用2D数据即可学习3D运动分布，同时避免SDS等优化方法中的域外样本、模式坍塌等问题。
claims:
- MAS在NBA数据集用户研究中，精度、多样性、整体质量三个维度均以100%比例显著优于DreamFusion改版，以86%以上比例优于MotionBERT。
- 消融实验表明，移除3D噪声投影后模型发生模式坍塌，Recall降至0.01，证明多视角一致噪声是该方法成功的关键。
- 在侧视角度评估时，MAS的Recall为0.60，远超ElePose的0.17和MotionBERT的0.15，且不受视角变化影响。
- MAS的FID为5.38，接近2D扩散模型上界5.23，远优于DreamFusion的66.38。
---

# MAS: Multi-view Ancestral Sampling for 3D Motion Generation Using 2D Diffusion

> [!tip] 核心洞察
> 在扩散去噪每一步将多个2D视图约束为同一3D运动的投影，以一致的方式逐步生成3D运动，使得仅用2D数据即可学习3D运动分布，同时避免SDS等优化方法中的域外样本、模式坍塌等问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAS：多视角祖先采样的2D扩散3D运动生成 |
| 英文题名 | MAS: Multi-view Ancestral Sampling for 3D Motion Generation Using 2D Diffusion |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://guytevet.github.io/mas-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Multi-view Ancestral Sampling (MAS) |
| Dataset | NBA 2D projections, NBA user study, Human3.6M |

> [!tip] 效果简介
> - NBA 2D projections 上，FID↓ 5.38±.06 vs MotionBERT 10.76±.45, ElePose 10.76±.45 (-5.38 (大幅提升))。
> - NBA 2D projections (Side view) 上，Recall↑ 0.60±.01 vs ElePose 0.17±.01, MotionBERT 0.15±.04 (+0.43 (远超提升方法))。
> - NBA user study 上，Precision 100.0% (vs DreamFusion), 86.1% (vs MotionBERT) vs DreamFusion, MotionBERT (显著偏好MAS)。

## 概述

**核心问题**：当前3D人体运动生成严重依赖高质量3D运动捕捉数据，这类数据获取成本高昂、难以扩展，且覆盖的运动领域极为有限。与此同时，互联网上存在海量2D视频数据，却因缺乏多视角一致性而无法直接用于3D运动生成。

**核心方法**：本文提出**多视角祖先采样（Multi-view Ancestral Sampling, MAS）**，在2D扩散模型的去噪过程中引入多视角一致性约束。具体而言，MAS在每一步去噪时同时生成多个视图的2D运动序列，通过三角化将其融合为一致的3D运动，再重投影回各视图，以此逐步“刻画”出符合多视角几何的3D运动。该方法的关键创新在于两步：一是**一致性模块**，每步将多视图预测强制约束为同一3D运动的投影；二是**3D噪声投影**，从3D高斯分布采样噪声后正交投影到各视图，确保多视图噪声分布一致，避免模式坍塌。

**方法定位**：MAS属于**无监督3D运动生成**方法，仅需2D视频数据即可学习3D运动分布。它与现有方法有本质区别——既不同于需要3D真值监督的姿态提升方法（如ElePose、MotionBERT），也不同于基于SDS优化的DreamFusion式生成（后者在无约束运动生成任务上表现极差）。MAS将多视角一致性“硬编码”进扩散采样过程，而非事后优化，从而避免域外样本和模式坍塌问题。

**主要结果**：
- 在NBA数据集上，MAS的FID达到**5.38**，接近2D扩散模型上界5.23，远优于DreamFusion改编版的66.38。
- 侧视角评估时，MAS的Recall为**0.60**，远超ElePose的0.17和MotionBERT的0.15，证明其不受视角变化影响。
- 用户研究中，MAS在精度、多样性、整体质量三个维度均以**100%**比例显著优于DreamFusion，以**86%以上**比例优于MotionBERT。
- 消融实验揭示，移除3D噪声投影后模型发生严重模式坍塌（Recall降至0.01），证实多视角一致噪声是该方法成功的必要条件。

## 背景与动机

### 3D运动生成的困境：数据稀缺与2D鸿沟

三维人体运动生成是计算机视觉与图形学中的核心问题，在动画制作、虚拟现实、运动分析等领域具有广泛的应用前景。然而，当前主流的3D运动生成方法面临一个根本性的瓶颈：**它们严重依赖高质量的3D运动捕捉（MoCap）数据**。这类数据需要在专业实验室中通过昂贵的光学捕捉系统或多传感器设备采集，获取成本高、覆盖场景有限、难以规模化扩展。篮球、舞蹈、武术等复杂运动领域的高质量3D数据尤为稀缺，这直接限制了现有方法在这些领域的泛化能力。

与此同时，互联网上存在海量的2D视频数据，涵盖了极为丰富的运动类型和场景。然而，这些2D数据存在一个致命缺陷：**缺乏多视角一致性**。一段普通视频通常只提供单一视角的运动投影，无法直接还原出唯一且准确的3D运动——这正是计算机视觉中经典的“从2D提升到3D”（2D-to-3D lifting）不适定问题。

### 现有方法的缺口

针对上述困境，现有工作主要沿着两条路径展开，但各自存在明显的局限性：

**无监督2D到3D姿态提升方法**（如 **ElePose**（Wandt et al., CVPR 2022））试图从单视角2D姿态估计中恢复3D运动。这类方法无需3D标注数据，但在面对遮挡或侧视角度时性能急剧下降。例如，在NBA数据集的侧视角度评估中，ElePose的Recall仅为0.17，MotionBERT（Zhu et al., 2023）为0.15，远低于正面视角的表现，暴露出其多视角泛化能力的不足。

**基于SDS（Score Distillation Sampling）的3D生成方法**（如 **DreamFusion**（Poole et al., 2022））利用预训练的2D扩散模型作为先验，通过迭代优化生成3D内容。然而，当将其改编为无约束3D运动生成任务时，该方法表现极差——FID高达66.38，且生成的运动会发生模式坍塌（mode collapse），产生呆板、运动幅度极小的结果。这是因为SDS在优化过程中容易产生域外样本（out-of-distribution samples），且缺乏有效的多视角一致性约束机制。

### 本文的核心动机

上述分析揭示了一个清晰的矛盾：**丰富的2D视频数据无法直接用于3D运动生成，而现有的3D生成方法要么依赖稀缺的3D标注数据，要么难以在多视角一致性上取得突破**。

MAS（Multi-view Ancestral Sampling）的提出正是为了突破这一困境。其核心动机是：**能否仅用2D运动数据训练一个生成模型，使其学会3D运动的分布？** 这一目标的实现需要解决两个关键挑战：

1. **多视角一致性问题**：如何确保从不同视角观察时，生成的2D运动投影都对应同一个合理的3D运动？
2. **采样质量问题**：如何在避免模式坍塌和域外样本的前提下，从2D扩散模型中采样出高质量的3D运动？

MAS通过在2D扩散模型的祖先采样过程中引入多视角一致性机制来应对这些挑战：在每一步去噪时，同时处理多个2D视图，通过三角化与重投影强制它们共享一个3D运动，并使用3D噪声投影保持多视图噪声分布的一致性。这种方法使得3D运动可以从头开始逐步生成，同时始终保持多视图之间的几何一致性，从而仅用2D数据即可学习3D运动分布。

## 核心创新

### 问题瓶颈

当前3D人体运动生成面临一个根本性数据瓶颈：高质量3D运动捕捉数据的获取成本高昂、覆盖领域有限且难以规模化扩展。相比之下，2D视频数据极为丰富，但缺乏多视角一致性，无法直接用于3D生成。现有的无监督2D到3D姿态提升方法（如**ElePose**, Wandt et al., CVPR 2022）虽能从单目视频恢复3D运动，但在侧视角度下性能急剧退化，且生成的运动常伴随抖动和无效姿态。基于分数蒸馏采样（SDS）的3D生成方法（如**DreamFusion**, Poole et al., 2022）在无约束运动生成任务上表现极差，FID高达66.38，且面临域外样本和模式坍塌问题。

### 核心洞察

MAS的核心洞察在于：**在扩散去噪的每一步，将多个2D视图同时约束为同一3D运动的投影，以一致的方式逐步生成3D运动**。这使得模型仅需2D运动数据即可隐式学习3D运动分布，同时避免了SDS等优化方法中的域外样本和模式坍塌问题。与现有方法在生成后进行单次三角化不同，MAS将多视角一致性嵌入到扩散采样的全过程，实现了从2D到3D的无缝过渡。

### 关键创新点（Changed Slots）

#### 1. 采样策略：从单视图祖先采样到多视图一致性采样

**Baseline**：传统2D扩散模型（如**MDM**, Tevet et al., 2023）采用单视图祖先采样，逐视图独立去噪，视图间无任何一致性约束。DreamFusion改编版则使用SDS优化步，通过单视图校正逐步优化3D表示。

**MAS**：提出多视图祖先采样机制，同时维持V个视图的噪声状态并协同去噪。每步去噪后，通过一致性模块将所有视图的预测结果融合为统一3D运动，再投影回各视图作为下一步的输入（见Algorithm 1, Figure 3）。这种硬约束策略确保了生成过程中视图间的几何一致性，而非事后优化。

#### 2. 噪声来源：从独立2D噪声到3D噪声投影

**Baseline**：传统方法为每个视图独立采样2D高斯噪声，视图间的噪声缺乏任何结构关联。

**MAS**：创新性地从3D高斯分布中采样噪声 $\varepsilon \sim \mathcal{N}(0, I_{3\times3})$，再通过正交投影得到各视图的2D噪声。正交投影的关键性质在于其保持了高斯分布（Theorem 1）：
$$\varepsilon \sim \mathcal{N}(0, I_{3\times3}) \Rightarrow P_{\text{orth}} \varepsilon \sim \mathcal{N}(0, I_{2\times2})$$
这一设计保证了各视图噪声在3D空间中的一致性，同时不破坏扩散模型对噪声分布的假设。消融实验（Table 3）表明，移除3D噪声投影后模型发生严重模式坍塌，Recall骤降至0.01，充分证明了多视角一致噪声是该方法成功的必要条件。

#### 3. 多视图一致性：从弱约束到硬约束

**Baseline**：现有提升方法仅在生成后进行单次三角化，无迭代优化；SDS方法仅通过单视图校正提供弱约束，缺乏多视图间的协同。

**MAS**：在每步去噪后引入一致性模块，通过最小化重投影误差将当前预测的V个2D运动三角化为统一3D运动：
$$X = \underset{X'}{\arg\min} \sum_{v=1}^{V} \| P(X', v) - \hat{x}_0^v \|_2^2$$
随后将优化后的3D运动投影回各视图，得到多视图一致的干净运动 $\tilde{x}_0^{1:V}$，用于祖先采样更新（见Section 4.2, Algorithm 1）。这种硬约束机制确保了每一步生成都在3D几何空间中保持一致，从根本上避免了视图间的漂移和冲突。

### 方法流水线

MAS的整体架构由四个核心模块构成：

1. **2D运动扩散模型（$G_{2D}$）**：基于MDM transformer架构的预训练2D运动生成模型，在从网络视频提取的2D姿态估计数据上训练（Figure 2），作为多视图生成的先验。

2. **多视图去噪循环**：同时维持V个视图的噪声状态 $x_t^{1:V}$，在每步去噪中并行预测各视图的干净运动 $\hat{x}_0^{1:V}$（Algorithm 1, Figure 3）。

3. **一致性模块**：通过三角化优化将多视图预测融合为3D运动，并重投影回各视图，强制几何一致性（Section 4.2）。

4. **3D噪声投影器**：采样3D高斯噪声并通过正交投影得到各视图噪声，保持多视图噪声分布一致（Theorem 1）。

最终的祖先采样更新公式为：
$$x_{t-1}^{1:V} = \frac{\beta_t \sqrt{\bar{\alpha}_{t-1}}}{1-\bar{\alpha}_t} x_t^{1:V} + \frac{(1-\bar{\alpha}_{t-1})\sqrt{\alpha_t}}{1-\bar{\alpha}_t} \tilde{x}_0^{1:V} + \frac{\beta_t (1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t} \varepsilon^{1:V}$$
其中 $\tilde{x}_0^{1:V}$ 为一致性模块输出的重投影视图，$\varepsilon^{1:V}$ 为3D噪声投影得到的多视图噪声。

## 整体框架

MAS 的整体管线由两个阶段构成：**数据准备与2D扩散模型训练**（离线阶段），以及**多视角祖先采样推理**（在线阶段）。核心思路是将3D运动生成问题转化为多个2D视图的同步去噪问题，在扩散过程的每一步强制多视角一致性，从而仅用2D数据学习3D运动分布。

### 阶段一：数据准备与2D扩散模型训练

如图2所示，该阶段从互联网视频中提取2D姿态估计序列，构建2D运动数据集，并在此之上训练一个2D运动扩散模型 $G_{2D}$。该模型基于MDM的Transformer架构（Tevet et al., 2023），学习的是2D运动的无条件分布——它本身不包含任何3D或多视角信息，仅作为后续MAS推理的“生成先验”。

### 阶段二：多视角祖先采样（MAS）推理

推理阶段是MAS方法的核心，其整体流程如Algorithm 1和图3所示。给定 $V$ 个预设相机视角 $v_{1:V}$，MAS同时维持 $V$ 条2D运动序列的噪声状态，并逐步执行去噪。每一步包含三个关键模块的协作：

1. **2D运动扩散模型 $G_{2D}$**：对每个视图的当前噪声样本 $x_t^v$ 执行单步去噪，预测干净2D运动 $\hat{x}_0^v$。该模型在推理阶段固定不变。

2. **一致性模块（Consistency Block）**：将 $V$ 个视图的预测干净运动 $\hat{x}_0^{1:V}$ 通过三角化（Triangulation）融合为统一的3D运动 $X$，再将 $X$ 重投影回各视图，得到多视角一致的干净运动 $\tilde{x}_0^{1:V}$。三角化通过最小化重投影误差实现：
   $$X = \underset{X'}{\arg\min} \sum_{v=1}^{V} \| P(X', v) - \hat{x}_0^v \|_2^2$$
   其中 $P$ 为正交投影算子。这一步是MAS将2D生成“提升”为3D运动的关键机制。

3. **3D噪声投影器**：从3D标准高斯分布采样噪声 $\varepsilon_{3D} \sim \mathcal{N}(0, I_{3\times3})$，通过正交投影得到各视图的2D噪声 $\varepsilon^{1:V}$。Theorem 1保证了正交投影不破坏高斯分布性质，使得多视图噪声天然保持一致。

最后，利用重投影的干净视图 $\tilde{x}_0^{1:V}$ 和投影的3D噪声 $\varepsilon^{1:V}$，按DDIM-like的祖先采样公式更新到下一时间步：
$$x_{t-1}^{1:V} = \frac{\beta_t \sqrt{\bar{\alpha}_{t-1}}}{1-\bar{\alpha}_t} x_t^{1:V} + \frac{(1-\bar{\alpha}_{t-1})\sqrt{\alpha_t}}{1-\bar{\alpha}_t} \tilde{x}_0^{1:V} + \frac{\beta_t (1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t} \varepsilon^{1:V}$$

经过 $T$ 步迭代后，最终的多视角一致2D运动序列即为3D运动在各视图上的投影，可直接用于下游任务。

### 模块关系与数据流

整个推理过程形成了“**2D去噪 → 3D三角化 → 2D重投影 → 祖先采样**”的闭环。一致性模块充当2D生成与3D结构之间的桥梁，而3D噪声投影器则确保多视图的噪声先验本身是几何一致的。消融实验（Table 3）表明，移除3D噪声投影后模型发生严重的模式坍塌（Recall降至0.01），证实了该模块对维持生成多样性的关键作用。视图数量 $V \geq 5$ 时性能趋于饱和（Table 6），说明5个视图即可提供足够的多视角约束。

### 补充图表

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/002_Figure_2.jpg]]
*Figure 2: Preparations. The motion diffusion model used for MAS is trained on 2D motion estimations of videos scraped from the web*

## 核心模块与公式推导

MAS（Multi-view Ancestral Sampling）的核心设计围绕一个关键矛盾展开：如何在仅拥有2D运动先验的条件下，生成多视角一致的3D运动。其解决方案是在扩散模型的祖先采样过程中嵌入一个“一致性约束循环”，每步同时去噪多个视图，并通过三角化与重投影强制所有视图共享同一底层3D运动。以下按模块拆解这一机制。

### 2D运动扩散模型（预训练先验）

MAS 的生成能力建立在一个预训练的2D运动扩散模型 $G_{2D}$ 之上（Figure 2）。该模型基于 MDM（Tevet et al., 2023）的 Transformer 架构，在从互联网视频中提取的2D姿态估计数据上训练，学习的是2D运动序列的分布 $p(x)$。在MAS框架中，$G_{2D}$ 的角色是提供一个“2D运动专家”——给定带噪声的2D运动 $x_t^v$，预测其干净版本 $\hat{x}_0^v$，但该预测本身不保证多视图间的一致性。

### 多视图去噪循环

MAS 的核心流程是一个多视图祖先采样循环（Algorithm 1, Figure 3）。在每一去噪步 $t$，系统同时维护 $V$ 个视图的噪声状态 $x_t^{1:V}$，并对每个视图独立调用 $G_{2D}$ 预测干净运动 $\hat{x}_0^{1:V}$。随后，这些独立预测被送入一致性模块，强制它们收敛到同一3D运动。去噪步的更新公式为：

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/003_Figure_3.jpg]]
*Figure 3: The figure illustrates an overview of MAS, showing a multi-view denoising step from the 2D sample collection*

$$x_{t-1}^{1:V} = \frac{\beta_t \sqrt{\bar{\alpha}_{t-1}}}{1-\bar{\alpha}_t} x_t^{1:V} + \frac{(1-\bar{\alpha}_{t-1})\sqrt{\alpha_t}}{1-\bar{\alpha}_t} \tilde{x}_0^{1:V} + \frac{\beta_t (1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t} \varepsilon^{1:V}$$

其中，$\tilde{x}_0^{1:V}$ 是经一致性模块校正后的多视图干净运动，$\varepsilon^{1:V}$ 是从3D噪声投影得到的多视图一致噪声（见下文），而非各视图独立采样的噪声。这一步将DDIM-like的祖先采样与多视图约束融为一体。

### 一致性模块（Consistency Block）

一致性模块是MAS区别于所有基线方法的关键组件（Section 4.2, Algorithm 1）。其输入是 $G_{2D}$ 为 $V$ 个视图独立预测的干净2D运动 $\hat{x}_0^{1:V}$，输出是强制多视图一致的 $\tilde{x}_0^{1:V}$。模块分两步执行：

**1. 三角化（Triangulation）：** 寻找一个3D运动 $X$，使其正交投影到各视图时与预测的2D运动差异最小：

$$X = \underset{X'}{\arg\min} \sum_{v=1}^{V} \| P(X', v) - \hat{x}_0^v \|_2^2$$

这里 $P(X', v)$ 表示3D运动 $X'$ 在视图 $v$ 下的正交投影。该优化问题在每步去噪时完整求解，而非使用轻量近似。

**2. 重投影：** 将优化得到的 $X$ 重新投影回各视图，得到一致化的2D运动 $\tilde{x}_0^{1:V} = P(X, 1:V)$，用于后续的祖先采样更新。

这一“预测-三角化-重投影”的闭环机制，确保每一步去噪都在多视图一致的流形上进行，从根源上避免了单视图方法中不同视角预测相互矛盾的问题。

### 3D噪声投影器

标准扩散采样中，每个视图独立添加高斯噪声会破坏多视图间的一致性。MAS 的解决方案是从3D高斯分布中采样噪声，再投影到各视图（Section 4.2, Theorem 1）：

$$\varepsilon \sim \mathcal{N}(0, I_{3\times3}) \quad \Rightarrow \quad P_{\text{orth}}\,\varepsilon \sim \mathcal{N}(0, I_{2\times2})$$

Theorem 1 证明正交投影保持高斯分布不变，这是该设计的理论基础。消融实验（Table 3, “without 3D noise”行）提供了该模块的决定性证据：移除3D噪声投影后，Recall 骤降至 0.01，模型发生严重的模式坍塌——这证实多视图一致的噪声分布是防止生成退化到少数模式的必要条件。

### 模块间的因果链路

以上四个模块形成一条清晰的因果链：**$G_{2D}$ 提供2D运动先验 → 一致性模块在每个去噪步将独立预测约束为共享3D运动 → 3D噪声投影确保噪声本身不破坏多视图一致性 → 祖先采样更新在一致流形上推进**。去掉一致性模块，方法退化为独立的多视图2D生成；去掉3D噪声，一致性模块虽在，但噪声的不一致会逐步侵蚀多视图约束，最终导致模式坍塌。两个机制必须协同工作，才能在仅使用2D数据训练的条件下稳定生成3D运动。

## 实验与分析

### 核心实验设置

MAS 的实验围绕无条件 3D 人体运动生成展开，核心评估逻辑是：**如果生成的 3D 运动投影到多个 2D 视图后质量高且一致，则 3D 运动本身也是高质量的**。实验使用两个主要基准：

1. **NBA 数据集**：从 YouTube 抓取的篮球比赛视频，经 2D 姿态估计器处理后用于训练 2D 扩散模型，是展示 MAS 在“3D 真值不可得”场景下能力的主战场。
2. **Human3.6M**：标准 3D 人体姿态数据集，用于验证 MAS 在有 3D 真值的学术基准上的表现。

对比方法分为三类：(1) 无监督 2D 到 3D 姿态提升方法 **ElePose**（Wandt et al., CVPR 2022）；(2) 有监督 3D 姿态估计方法 **MotionBERT**（Zhu et al., 2023）；(3) 基于 SDS 的 3D 生成方法 **DreamFusion**（Poole et al., 2022），本文将其改编为无条件运动生成任务。同时以 **MDM**（Tevet et al., 2023）的纯 2D 扩散模型作为生成质量的理论上界。

### 主实验结果

#### NBA 数据集：定量对比

Table 2 报告了 MAS 与提升方法在 NBA 2D 投影上的对比。MAS 的 FID 达到 **5.38±0.06**，显著优于 ElePose 和 MotionBERT（均为 10.76±0.45），接近 2D 扩散模型上界 5.23（Table 3）。在多样性指标上，MAS 也以 9.47 领先于提升方法的 8.90。

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/006_Table_2.jpg]]
*Table 2: Comparison with pose lifting on NBA dataset. MAS outperforms state-of-the-art unsupervised lifting methods. Furthermore, lifting methods experience a drop in recall when evaluated from the side view (U*

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/007_Table_3.jpg]]
*Table 3: Ablations. We compare MAS to an adaptation of Dream-Fusion [26] to the unconditional motion generation domain. Our evaluation measures the quality of 2D projections of the 3D generated motions. Our ablations show that MAS performs best with as few as 5 views (ours), and 3D noise is crucial for preventing mode collapse. gray indicates mode-collapse (Recall\< 10%), bold marks the best results otherwise*

**侧视角评估是本实验的关键发现**。当相机从侧面（方位角从 $U(\pi/4, 3\pi/4)$ 采样）评估时，提升方法的 Recall 急剧下降：ElePose 从正面视角的 0.59 跌至 0.17，MotionBERT 从 0.54 跌至 0.15。MAS 的 Recall 则保持 **0.60±0.01**，几乎不受视角变化影响。这直接验证了 MAS 生成的是真正的 3D 运动，而非仅在特定视角下看似合理的 2D 投影。

#### NBA 数据集：用户研究

Figure 5 展示了 22 名用户在 15 组随机生成运动上的偏好投票，从三个维度评估：
- **精度（Precision）**：MAS vs DreamFusion 改编版为 100.0%，MAS vs MotionBERT 为 86.1%
- **多样性（Diversity）**：MAS vs DreamFusion 为 100.0%，MAS vs MotionBERT 为 83.3%
- **整体质量（Overall Quality）**：MAS vs DreamFusion 为 100.0%，MAS vs MotionBERT 为 88.9%

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/004_Figure_5.jpg]]
*Figure 5: NBA Dataset User study. We asked 22 unique users to compare 15 randomly generated motions by each of the models to MAS generations in 3 aspects - precision (i.e. what samples best depict Basketball moves), Overall Quality and Diversity. The dashed line marks 50%. MAS outperforms the lifting methods and the DreamFusion adaptation*

用户对 MAS 的偏好远超 50% 随机基线，且 DreamFusion 改编版在无条件运动生成任务上完全无法与 MAS 竞争。

#### Human3.6M 数据集

Table 5 显示，在 Human3.6M 正面视角下，MAS 的 Recall 为 0.93，略低于 MotionBERT 的 0.98（该方法专为此数据集设计且有监督训练）。但在侧视角下，MAS 的 Recall 为 **0.92±0.01**，远超 ElePose 的 0.25 和 MotionBERT 的 0.56，再次验证了 MAS 的多视角一致性优势。

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/009_Table_5.jpg]]
*Table 5: Comparison with pose lifting on Human3.6M dataset. MAS has a competitive performance to lifting methods that were designed for this dataset. However, MAS outperforms the lifting methods when evaluated from the side view. Here, bold marks the best results when comparing to the side view*

### 消融实验

Table 3 和 Table 6 提供了系统的消融分析，揭示 MAS 各组件的作用机制：

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/010_Table_6.jpg]]
*Table 6: NBA Dataset Ablations. Performance saturates for number of views*

#### 3D 噪声投影的关键性

**移除 3D 噪声投影是消融中最具决定性的发现**（Table 3, "without 3D noise" 行）。当使用独立的 2D 噪声替代多视图一致的 3D 噪声时，模型发生严重的**模式坍塌**：Recall 从 0.60 骤降至 **0.01**，FID 从 5.38 恶化至 19.12。这从实验上证明了 Theorem 1 的理论价值——只有通过正交投影保持多视图噪声分布一致，祖先采样过程才能维持生成多样性。

#### 与 DreamFusion 改编版的对比

DreamFusion 改编版在无条件运动生成上的 FID 高达 **66.38**，Recall 仅 0.06（Table 3）。其失败根源在于 SDS 优化在无文本条件引导时，每步优化的目标分布与真实运动分布存在严重偏移，导致域外样本和模式坍塌。MAS 通过将多视图一致性嵌入祖先采样过程，从根本上避免了这一问题。

#### 视图数量

Table 6 显示，视图数量 $V \geq 5$ 时性能趋于饱和。$V=5$ 时 FID 为 5.38，Recall 为 0.60；$V=10$ 时 FID 微降至 5.34，Recall 保持 0.60。进一步增加视图无明显增益，说明 5 个视图已能提供足够的多视角约束。

#### 扩散步数

减少扩散步数会损害生成质量（Table 6）。100 步时 FID 为 5.38，Recall 为 0.60；50 步时 FID 升至 5.79，Recall 降至 0.57；20 步时 FID 进一步升至 6.13，Recall 降至 0.54。100 步被确定为质量与速度的最佳平衡点。

#### 相机距离

相机距离约 **7 米**时性能最优（Table 6）。距离 3 米时 FID 为 5.98，Recall 为 0.54；距离 7 米时 FID 为 5.38，Recall 为 0.60；距离 12 米时 FID 回退至 5.52，Recall 降至 0.56。这与 Theorem 2 的分析一致：距离过近时透视投影与正交投影的差异增大，影响多视图一致性；距离过远时运动细节信息丢失。

### 推理效率

Table 4 报告了单样本生成的时间与显存开销。MAS 生成一个运动样本约需 24 秒，显存占用约 6.5 GB。考虑到该方法同时维护多个视图的去噪过程并在每步执行三角化优化，这一开销在可接受范围内。

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/008_Table_4.jpg]]
*Table 4: Time and memory costs per single sample generation*

### 失败模式与评估局限性

**定性失败模式**（Figure 4）：
- MotionBERT 生成的篮球运动较为呆板，运动幅度有限
- ElePose 的预测存在抖动，且常包含无效姿态（图中红框标注）
- DreamFusion 改编版生成的运动几乎无有效运动信息

**评估公平性说明**：
1. MAS 的评估基于 2D 投影质量，这与 MAS 的优化目标（多视角一致性）高度一致，可能对 MAS 有利。
2. 训练数据依赖 2D 姿态估计器，其误差可能通过置信度掩码得到缓解，但仍可能限制最终 3D 运动质量的上限。
3. “好的 2D 投影意味着好的 3D 运动”这一假设在极端遮挡或非刚性变形场景下可能不成立，需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l1850_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diff/figures/005_Figure_4.jpg]]
*Figure 4: Generated motions by MAS compared to ElePose [38], MotionBert [54], and an adaptation of DreamFusion [26] to unconditioned motion generation. We observe that MotionBert and DreamFusion produce dull motions with limited movement and ElePose predictions are jittery and often include invalid poses (Red rectangles)*

## 方法谱系与知识库定位

### 1. 方法谱系：从2D提升到3D原生生成

MAS占据了一个独特的方法论位置——它既不是传统的“2D姿态提升”（2D-to-3D lifting），也不是基于SDS优化的3D生成，而是一种**在2D扩散模型采样过程中内建3D一致性的原生3D生成方法**。

**与2D姿态提升方法的本质差异**

传统的无监督3D姿态估计方法，如**ElePose**（Wandt et al., CVPR 2022），遵循“先估计2D姿态，再提升至3D”的两阶段范式。这类方法的根本瓶颈在于：2D估计器输出的单视图信息本身不足以唯一确定3D结构，导致深度歧义无法被彻底消除。MAS绕过了这一瓶颈——它不依赖任何单视图2D估计作为中间表示，而是直接在扩散去噪的每一步中通过多视图三角化构造3D运动。这意味着MAS的3D推理发生在生成过程的每一步，而非仅在最终输出的后处理阶段。

**与有监督3D方法的对比**

**MotionBERT**（Zhu et al., 2023）作为有监督3D姿态估计方法，依赖标注的3D运动捕捉数据进行训练。MAS与它的核心区别在于数据依赖：MAS仅需2D视频数据即可训练，而MotionBERT需要昂贵的3D标注。在侧视角评估中，MAS的Recall达到0.60，远超MotionBERT的0.15（Table 2），说明MAS对训练数据中未见视角的泛化能力显著更强。

**与SDS优化方法的对比**

**DreamFusion**（Poole et al., 2022）通过Score Distillation Sampling将2D扩散先验蒸馏为3D表示，本文将其改编为无约束运动生成基线。然而，该改编版在NBA数据集上FID高达66.38，而MAS仅为5.38（Table 3）。这一巨大差距揭示了SDS方法在运动生成领域的根本性困难：SDS的优化过程容易产生域外样本（out-of-distribution samples），因为扩散模型在远离训练分布的噪声区域进行评分估计时不可靠。MAS通过在祖先采样的每一步执行硬性多视图一致性约束，避免了优化过程中的分布漂移。

**与2D扩散模型的关系**

MAS的核心生成能力来源于预训练的2D运动扩散模型**MDM**（Tevet et al., 2023），该模型基于transformer架构在2D姿态序列上训练。MAS并未修改2D扩散模型的权重或架构，而是将其作为一个“冻结的2D运动先验”，在其采样过程中插入多视图一致性机制。因此，MAS的生成质量上界受限于2D扩散模型本身——Table 3中2D扩散模型的FID为5.23，MAS为5.38，两者极为接近，表明MAS几乎无损地将2D生成能力迁移到了3D域。

### 2. 因果机制：为什么多视图一致性采样有效

MAS的成功可以归结为三个相互耦合的因果机制：

**机制一：逐步一致性构造避免累积误差**

与先独立生成多视图2D运动再后处理三角化的方案不同，MAS在扩散去噪的**每一步**都执行三角化与重投影。这一设计的因果逻辑是：在扩散过程的早期步骤（高噪声阶段），各视图的预测尚不精确，但通过每步强制执行一致性，模型被引导沿着“多视图一致”的方向去噪。随着噪声水平降低，一致性约束的精度逐步提高，最终收敛到高质量的3D运动。这避免了独立生成后再对齐时产生的累积误差和不可修复的冲突。

**机制二：3D噪声投影消除模式坍塌**

消融实验（Table 3, without 3D noise）提供了决定性证据：当移除3D噪声投影、改为各视图独立采样2D噪声时，Recall从0.60骤降至0.01，模型发生严重模式坍塌。其因果机制在于：独立采样的多视图噪声破坏了视图间的统计一致性，使得扩散模型在去噪过程中接收到相互矛盾的信号，最终被迫退化为生成单一“安全”模式。Theorem 1提供了理论保证——3D高斯噪声经正交投影后，每个视图的噪声仍服从标准正态分布，因此不会破坏扩散模型的去噪假设。

**机制三：硬约束优于软约束**

DreamFusion改编版的失败（FID 66.38）表明，基于SDS的软约束（通过梯度更新引导生成朝向一致性）在运动生成领域不可靠。MAS采用的硬约束——每步求解三角化优化问题并强制重投影——确保了生成过程中的每一步都严格满足多视图几何约束，不给不一致性任何积累空间。

### 3. 适用边界与局限

**已知适用条件**

- **数据需求**：需要充足的2D视频数据用于训练2D扩散模型。论文在NBA、Human3.6M及三个自采数据集上验证，对于数据稀少的运动领域效果未知。
- **视图数量**：消融实验（Table 6）表明，视图数V≥5时性能饱和，5个视图是效率与质量的最佳平衡点。
- **相机配置**：相机距离约7米时性能最优（Table 6），过近或过远均会降低FID和Recall。这由Theorem 2解释——当距离增大时，正交投影（MAS使用的简化）与透视投影的差异以O(1/(d-1))减小，但过远会损失运动细节。
- **扩散步数**：100步是质量和速度的最佳平衡，减少至20或50步会损害FID和Recall（Table 6）。

**当前局限**

1. **无全局位移**：MAS仅生成局部3D运动（根节点相对运动），不包含全局位置信息，无法生成带有空间移动的运动序列。
2. **仅支持无条件生成**：无法通过文本、音频或其他控制信号引导生成内容，限制了交互式应用。
3. **单人运动限制**：无法处理多人交互、手部/面部细节以及复杂物体操控场景。
4. **缺乏物理约束**：生成的运动可能违反物理规律（如脚部滑动、关节超限），因为三角化仅约束几何一致性而非物理合理性。
5. **评估偏差**：论文评估主要基于2D投影质量，这可能有利于MAS，因为其优化目标与评估准则（多视图一致性）天然一致。3D运动的真实分布无法直接获取，评估假设“好的2D视图意味着好的3D运动”在某些极端情况下可能不成立。

### 4. 开放问题

1. **扩展到复杂运动场景**：如何将MAS的多视图一致性框架扩展到多人交互、手物操控等场景？这需要解决多主体遮挡、接触约束等新挑战。
2. **条件生成能力**：能否在MAS框架中引入文本条件或多模态控制信号，使生成过程可引导？这可能需要修改2D扩散模型为条件模型，或在一致性模块中引入额外的引导机制。
3. **全局运动生成**：如何利用视频中的相机运动信息和场景上下文，生成具有全局位移的运动？这涉及将局部运动与全局轨迹解耦或联合建模。
4. **跨领域迁移**：MAS的核心思想——在2D扩散采样中插入多视图一致性——是否适用于文本到3D场景生成、3D物体生成等其他领域？
5. **效率优化**：动态视点采样或自适应视图数量选择是否能进一步减少所需的视图数量，同时保持生成质量？当前5视图的推理成本（Table 4）约为单视图的5倍，效率仍有优化空间。

## 原文 PDF

![[paperPDFs/CVPR_2024/MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diffusion.pdf]]
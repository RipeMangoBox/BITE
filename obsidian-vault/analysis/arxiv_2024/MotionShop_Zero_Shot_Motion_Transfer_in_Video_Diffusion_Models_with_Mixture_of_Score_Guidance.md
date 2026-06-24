---
title: "MotionShop: Zero-Shot Motion Transfer in Video Diffusion Models with Mixture of Score Guidance"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/MotionShop_Zero_Shot_Motion_Transfer_in_Video_Diffusion_Models_with_Mixture_of_Score_Guidance.pdf
aliases:
- MSGM
- MotionShop
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 早期扩散时间步（t ≪ T）的条件得分函数中包含丰富的运动信息，通过混合得分引导（MSG）可将该信息注入生成过程，实现有效运动迁移。
primary_logic: 将扩散模型的条件得分显式分解为运动得分和内容得分，并将运动迁移建模为得分空间中的势能混合，可以在无需训练/微调的情况下从参考视频提取运动模式并迁移到目标内容。
claims:
- MSG在MotionBench上取得了最优的Motion Fidelity（0.913）和Temporal Consistency（0.928），相比DMT在Motion Fidelity上提升2.9%。
- MSG通过混合得分引导（相对于CFG和USG）显著改善了运动一致性和与文本提示的匹配精度。
- 早期扩散时间步的条件得分可以有效编码和可视化运动特征，为MSG提供了关键的运动信息来源。
- MotionBench 上 Motion Fidelity = 0.913
---

# MotionShop: Zero-Shot Motion Transfer in Video Diffusion Models with Mixture of Score Guidance

> [!tip] 核心洞察
> 将扩散模型的条件得分显式分解为运动得分和内容得分，并将运动迁移建模为得分空间中的势能混合，可以在无需训练/微调的情况下从参考视频提取运动模式并迁移到目标内容。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionShop：基于得分混合引导的视频扩散模型零样本运动迁移 |
| 英文题名 | MotionShop: Zero-Shot Motion Transfer in Video Diffusion Models with Mixture of Score Guidance |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2412.05355) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Mixture of Score Guidance (MSG) |
| Dataset | MotionBench, User Study |

> [!tip] 效果简介
> - MotionBench 上，Motion Fidelity 0.913 vs 0.887 (DMT) (+2.9%)；Temporal Consistency 0.928 vs not directly reported (N/A)；Text Similarity 0.314 vs 0.328 (VMC) (-0.014)。
> - User Study (N=50) 上，Human Preference (Text Alignment / Motion Fidelity / Temporal Consistency) 0.41 / 0.43 / 0.38 vs best competitors (not explicitly listed) (N/A)。

## 概述

### 问题与瓶颈

视频运动迁移（motion transfer）的目标是从一段参考视频中提取运动模式，并将其注入到由文本提示指定的全新内容中，生成一段既保持参考运动特征、又与目标文本语义一致的新视频。现有方法面临的核心瓶颈在于：**在零样本条件下，难以同时维持高运动保真度与灵活的场景适应性**。这一矛盾在多物体交互、复杂相机运动以及大幅场景变化时尤为突出——基于训练或微调的方法（如双路径LoRA、时间层调整等）往往对特定运动模式过拟合，泛化能力受限；而无需训练的引导方法则容易在运动一致性与内容生成质量之间顾此失彼。

### 核心思路

MotionShop提出了一种名为**混合得分引导（Mixture of Score Guidance, MSG）**的新方法，其核心洞察可归结为两点：

1. **运动信息存在于早期扩散时间步的条件得分中**。在扩散模型的前向过程中，早期时间步（约总步数的前10%）的条件得分函数 $\nabla_z \log p_t(z|y)$ 编码了丰富的运动特征，这些特征可以被显式提取并可视化（见Figure 2）。
2. **运动迁移可以建模为得分空间中的势能混合**。将扩散模型的条件得分显式分解为“运动得分”和“内容得分”两部分，通过在采样过程中线性混合参考视频的运动得分差与目标内容的条件得分，即可在无需任何训练或微调的前提下，将参考运动模式迁移到全新的文本驱动内容上。

从统计力学的视角看，MSG将运动迁移问题转化为一个**修正的朗之万动力学采样过程**——目标视频的生成由一个混合势能函数驱动，该势能函数同时编码了内容约束和运动引导。

### 方法定位

MSG属于**零样本、无训练的视频运动迁移方法**，直接操作于预训练视频扩散模型（如CogVideoX）的得分空间，无需额外的模型结构修改或参数更新。与现有方法相比，MSG的关键差异体现在三个维度：

| 维度 | 现有方法 | MSG |
|------|---------|-----|
| 运动信息提取 | 全扩散时间步隐式使用 | 仅早期时间步（约10%总步数）显式提取 |
| 引导机制 | CFG或无条件得分引导（USG） | 参考视频条件得分差引导 |
| 训练/微调要求 | 需要额外训练或微调 | 完全零样本 |

在方法谱系中，MSG与**MotionDirector (MD)**、**DMT**、**VMC**、**MotionInversion (MI)**等近期工作构成直接对比关系；在引导机制层面，MSG相对于**无分类器引导（CFG）**和**无条件得分引导（USG）**提供了更精确的运动控制能力。

### 主要结果

在自建的**MotionBench**基准（含200段参考视频、1000个迁移序列，覆盖单物体、多物体、相机运动三类场景）上，MSG取得了以下关键结果：

- **运动保真度（Motion Fidelity）**：0.913，超越DMT（0.887）达2.9%，为所有对比方法中最高。
- **时序一致性（Temporal Consistency）**：0.928，同样处于最优水平。
- **文本相似度（Text Similarity）**：0.314，与VMC（0.328）接近，在运动保真度与文本对齐之间取得了有利的权衡（见Figure 6的Trade-off分析）。
- **用户研究**（N=50）：在文本对齐、运动保真度、时序一致性三个维度上，MSG分别获得0.41、0.43、0.38的人类偏好评分，显著优于各对比方法。

消融实验进一步验证了MSG设计的有效性：运动提取的噪声强度参数在0.7时取得最佳效果（Figure 8左），MSG引导在前10%时间步应用可在运动保留与生成质量之间达到最优平衡（Figure 8右），且MSG在运动一致性和场景编辑质量上显著优于CFG和USG两种替代引导机制（Figure 9）。

### 局限与开放问题

当前方法存在以下已知局限：①仅在CogVideoX单骨干网络上验证，泛化性待确认；②强度参数和MSG权重 $w_\text{MSG}$ 需手动调节。开放问题包括：参考运动表示 $\mathcal{M}(z^*)$ 的具体计算流程是否依赖额外的对齐或归一化；MSG权重在不同场景下的自动调节策略；以及该方法向更长视频或更高分辨率生成的扩展路径。

## 背景与动机

### 问题背景：视频运动迁移的核心挑战

视频运动迁移（video motion transfer）旨在从一段参考视频中提取运动模式（如物体移动轨迹、相机运动路径、多物体交互动态），并将其迁移到由文本提示指定的新内容上，生成一段既保留参考运动特征又符合目标语义的视频。这一任务在电影特效、虚拟内容创作、视频编辑等领域具有广泛的应用前景。

然而，实现高质量的运动迁移面临一个根本性瓶颈：**如何在零样本条件下同时保持高运动保真度和灵活的场景适应性**。具体而言，现有方法在以下三类场景中表现尤为不足：

1. **多物体交互场景**：当参考视频包含两个或多个相互作用的物体时（如两位骑士对战），现有方法难以准确解耦和迁移各自的运动模式，常导致运动混淆或丢失。
2. **复杂相机运动**：参考视频同时包含物体运动和大幅相机运动（如推拉、摇移、旋转）时，方法需要区分场景动态与相机动态，这对现有技术构成严峻挑战。
3. **大幅场景变化**：当目标文本提示描述的视觉内容与参考视频差异显著时（如将“摩托车”的运动迁移到“机器人驾驶的摩托车”），内容保真度与运动保真度之间出现严重的权衡困境。

### 现有方法的局限：训练依赖与得分空间利用不足

当前主流的视频运动迁移方法可大致分为两类，但均存在明显局限：

**基于微调的方法**（如 MotionDirector、DMT、VMC）通常需要针对每个参考视频进行额外训练或参数微调。例如，MotionDirector 采用双路径 LoRA 架构分别学习运动和外观表征，DMT 通过时间层调整实现运动迁移。这类方法的共性问题在于：（1）每次迁移都需要重新训练，计算开销大；（2）微调过程可能导致预训练模型先验知识的退化；（3）在训练数据有限的条件下，泛化能力受限。

**基于反演的方法**（如 MotionInversion）尝试通过扩散反演从参考视频中恢复噪声潜变量，进而引导生成过程。然而，这类方法隐式地使用全扩散时间步的信息，未能区分不同时间步中运动信息与内容信息的分布差异，导致运动提取不够精确，且容易引入参考视频的内容残留。

### 核心直觉：早期扩散时间步的条件得分编码运动信息

MotionShop 的核心洞察来源于对扩散模型条件得分函数（conditional score function）的重新审视。如图 2 所示，研究者发现：**在扩散过程的早期时间步（t 约为总步数的 10%），条件得分 $\nabla_{z_t} \log p_t(z \mid y)$ 中包含了丰富的运动特征信息**。通过可视化这些早期时间步的得分，可以清晰地观察到物体的运动轨迹、多物体的相对运动模式以及相机运动方向。

这一发现揭示了一个关键因果机制：扩散模型的去噪过程并非均匀地处理所有层次的信息——早期时间步主要决定全局结构和运动动态，而后期时间步则侧重于细节纹理和外观的生成。因此，**将运动迁移操作聚焦于早期时间步的得分空间，可以在不干扰内容生成的前提下，精确注入运动信息**。

### 本文动机：零样本得分空间运动迁移

基于上述观察，MotionShop 提出了一种全新的运动迁移范式——**混合得分引导（Mixture of Score Guidance, MSG）**。该方法的核心思想是：

1. **得分分解**：将扩散模型的条件得分显式分解为运动得分（motion score）和内容得分（content score）两部分，使运动迁移问题转化为得分空间中的势能混合问题。
2. **零样本操作**：直接在预训练视频扩散模型（如 CogVideoX）的得分空间中进行运动迁移，无需任何额外训练或微调，从根本上解决了现有方法的计算开销和先验退化问题。
3. **统计力学视角**：将运动迁移建模为混合势能函数 $U_{\text{MSG}}(z_t) = U_{\text{content}}(z_t) + v_{\text{MSG}} [U_{\text{motion}}(z_t, z_t^*) - U_{\text{prior}}(z_t)]$ 驱动的修正朗之万动力学过程，保证了生成过程的稳定性和内容保留。

这一框架不仅提供了理论上的优雅性，更在实际效果上取得了显著突破——在 MotionBench 基准上，MSG 以 0.913 的 Motion Fidelity 超越 DMT（0.887）达 2.9%，同时保持了 0.928 的 Temporal Consistency。

## 核心创新

MotionShop 的核心创新在于将视频运动迁移重新定义为**扩散模型得分空间中的势能混合问题**，从而在完全零样本的条件下实现高保真运动迁移。与现有方法相比，这一框架在三个关键维度上实现了突破。

### 1. 得分分解与运动信息解耦

现有运动迁移方法通常隐式地在整个扩散过程中利用条件得分，未能显式分离运动与内容信息。MotionShop 的关键洞察在于：**早期扩散时间步（t ≪ T）的条件得分函数中编码了丰富的运动信息**（Figure 2; Section 4.1.3）。基于此，方法将条件得分显式分解为运动得分和内容得分两个独立分量：

$$\nabla _ { z } \log p _ { t } ( z , \mathcal { M } ( z ^ { * } ) | y ) = \nabla _ { z } \log p _ { t } ( \mathcal { M } ( z ^ { * } ) | y ) + \nabla _ { z } \log p _ { t } ( z | \mathcal { M } ( z ^ { * } ) , y )$$

其中 $\mathcal { M } ( z ) = \nabla _ { z _ { t } } \log p _ { t } ( z | y )$ 为运动表示算子，从参考视频的早期时间步得分中提取运动特征。这种显式分解使得运动模式与内容生成可以独立控制，从根本上区别于 DMT、MotionDirector 等方法中运动与内容信息纠缠的处理方式。

### 2. 混合得分引导（MSG）机制

在得分分解的基础上，MotionShop 提出了**混合得分引导（Mixture of Score Guidance, MSG）**，将运动迁移建模为得分空间中的势能混合。MSG 得分函数的核心形式为：

$$s _ { \mathrm { M S G } } ( z _ { t } , z _ { t } ^ { * } ) = \nabla _ { z } \log p _ { t } ( z | y ) + w _ { \mathrm { M S G } } ( \nabla _ { z } \log p _ { t } ( z ^ { * } | y ^ { * } ) - \nabla _ { z } \log p _ { t } ( z ) )$$

其中第一项为内容生成得分（目标提示 $y$ 的条件得分），第二项为运动引导项——参考视频的条件得分与无条件得分之差。这一设计的精妙之处在于：**得分差 $(\nabla _ { z } \log p _ { t } ( z ^ { * } | y ^ { * } ) - \nabla _ { z } \log p _ { t } ( z ) )$ 天然地剥离了与内容相关的先验信息，仅保留由参考视频条件 $y^*$ 引入的运动模式**。

与之对应的混合势能函数驱动修正的朗之万动力学采样，保证生成过程的稳定性：

$$U _ { \mathrm { M S G } } ( z _ { t } ) = U _ { \mathrm { c o n t e n t } } ( z _ { t } ) + v _ { \mathrm { M S G } } [ U _ { \mathrm { m o t i o n } } ( z _ { t } , z _ { t } ^ { * } ) - U _ { \mathrm { p r i o r } } ( z _ { t } ) ]$$

消融实验（Figure 9）证实，MSG 在运动一致性和场景编辑质量上显著优于传统的 Classifier-Free Guidance（CFG）和 Unconditional Score Guidance（USG）。CFG 仅做无条件与条件得分的插值，缺乏参考运动信息；USG 虽引入参考视频的无条件得分，但无法有效分离运动与内容。MSG 通过显式的得分分解实现了更精准的运动迁移控制。

### 3. 完全零样本的训练自由范式

现有运动迁移方法普遍需要额外训练或微调：MotionDirector 需要双路径 LoRA 训练，DMT 需要调整时间层参数，VMC 依赖特定模块优化。MotionShop 的**关键 changed slot** 在于：**完全零样本，无需任何训练或微调**（Abstract），直接操作于预训练视频扩散模型（CogVideoX）之上。

实现零样本的关键技术选择包括：
- **运动提取仅使用早期时间步**（约总步数的 10%，Section 5），避免全时间步隐式使用的计算冗余和信息稀释；
- **MSG 引导仅作用于扩散过程前 10% 的时间步**（Figure 8 右），在运动保留与生成质量之间取得良好平衡；
- **噪声强度参数 strength=0.7** 时运动表示最优（Figure 8 左），低于 0.6 导致运动转移不足，高于 0.8 则产生过度风格化。

这种设计使得 MotionShop 在 MotionBench 上以 Motion Fidelity 0.913 和 Temporal Consistency 0.928 取得最优性能，相比 DMT 在 Motion Fidelity 上提升 2.9%（Table 1），同时保持与 VMC 相当的 Text Similarity（0.314 vs 0.328）。

### 创新总结

| 维度 | 基线方法 | MotionShop (MSG) |
|------|---------|-----------------|
| 运动信息提取 | 全扩散时间步隐式使用 | 仅早期时间步（~10%），显式运动表示算子 |
| 引导机制 | CFG 或 USG（得分插值） | MSG（得分差引导，运动-内容解耦） |
| 训练要求 | 需额外训练/微调 | 完全零样本 |
| 理论框架 | 经验性设计 | 统计力学视角的势能混合 |

这一创新框架不仅实现了性能突破，更重要的是提供了一种**可解释的运动迁移范式**：将运动视为得分空间中的势能扰动，通过混合势能驱动生成过程，从而在无需训练的条件下实现灵活、高保真的运动迁移。

## 整体框架

MotionShop 将零样本运动迁移建模为扩散模型得分空间中的势能混合问题，其整体框架由三个串行模块构成：**参考运动提取**、**MSG 得分混合与引导**、以及**修正的朗之万动力学采样**（Figure 3）。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/003_Figure_3.jpg]]
*Figure 3: Method Overview. Framework of our Mixture of Score Guidance (MSG) for zero-shot motion transfer in diffusion models. Left: Reference motion extraction stage captures motion characteristics*

**输入**包括两部分：(1) 一段参考视频，提供待迁移的运动模式；(2) 一个目标文本提示 $y$，描述期望生成的内容。**输出**为一段新视频，其内容遵循 $y$ 的语义约束，同时继承参考视频的运动特征。

### 模块一：参考运动提取

该模块从参考视频的早期扩散时间步中提取运动表示。核心发现是：在扩散过程的前约 10% 时间步（$t$ 较大时），条件得分函数 $\nabla_{z_t} \log p_t(z \mid y)$ 中编码了丰富的运动信息（Figure 2）。因此，运动表示算子直接定义为：

$$\mathcal{M}(z) = \nabla_{z_t} \log p_t(z \mid y)$$

实际操作中，先对参考视频潜变量施加受控噪声（由强度参数 `strength` 调节，最优值 0.7），再计算早期时间步的条件得分作为运动特征 $\mathcal{M}(z^*)$。该过程无需任何训练或微调，完全在预训练视频扩散模型的得分空间内完成。

### 模块二：MSG 得分混合与引导

这是框架的核心创新。传统方法（如 CFG、USG）在得分层面缺乏对运动与内容的显式解耦，导致运动迁移精度与内容保真度难以兼顾。MSG 将条件得分显式分解为运动得分和内容得分：

$$\nabla_z \log p_t(z, \mathcal{M}(z^*) \mid y) = \nabla_z \log p_t(\mathcal{M}(z^*) \mid y) + \nabla_z \log p_t(z \mid \mathcal{M}(z^*), y)$$

基于此分解，MSG 得分引导函数定义为：

$$s_{\mathrm{MSG}}(z_t, z_t^*) = \nabla_z \log p_t(z \mid y) + w_{\mathrm{MSG}} \big( \nabla_z \log p_t(z^* \mid y^*) - \nabla_z \log p_t(z) \big)$$

其中第一项为目标内容的生成得分，第二项为参考视频的条件得分与无条件得分之差——即“运动增量”，由权重 $w_{\mathrm{MSG}}$ 控制注入强度。这一设计将运动迁移转化为得分空间中的线性混合，使得运动模式可以从参考视频中提取并注入到任意目标内容的生成过程中。

### 模块三：修正的朗之万动力学采样

为在混合势能驱动下保持生成稳定性，MSG 将得分引导转化为势能函数：

$$U_{\mathrm{MSG}}(z_t) = U_{\mathrm{content}}(z_t) + v_{\mathrm{MSG}} \big[ U_{\mathrm{motion}}(z_t, z_t^*) - U_{\mathrm{prior}}(z_t) \big]$$

并采用修正的朗之万动力学 SDE 进行采样。该过程确保在注入运动信息的同时，生成视频的内容一致性和视觉质量不被破坏。

### 关键设计选择

消融实验（Figure 8, Figure 9）验证了两个关键设计：
- **运动提取时间步**：仅在前 10% 扩散时间步应用 MSG 引导，可在运动保留与生成质量间取得最佳平衡。
- **引导机制**：MSG 在运动一致性和场景编辑质量上显著优于 CFG 和 USG，因为后者无法将运动信息与内容信息在得分层面解耦。

整个框架直接运行在预训练的 CogVideoX 模型上，无需额外训练、微调或 LoRA 适配，实现了完全的零样本运动迁移。

## 核心模块与公式推导

### 3.1 扩散模型得分函数基础

视频扩散模型将数据分布 $p_{\text{data}}(z)$ 通过前向随机微分方程（SDE）逐步转化为先验分布。前向过程定义为：

$$d z = [ f ( z , t ) - \frac { g ( t ) ^ { 2 } } { 2 } \nabla _ { z } \log p _ { t } ( z ) ] d t + g ( t ) d \bar { w _ { t } }$$

其中 $f(z,t)$ 为漂移系数，$g(t)$ 为扩散系数，$\nabla_z \log p_t(z)$ 为得分函数。在方差保持（VP）条件下，逆向条件SDE为：

$$d z = - \frac { 1 } { 2 } \beta _ { t } z d t - \beta _ { t } \nabla _ { z } \log p _ { t } ( z | y ) d t + \sqrt { \beta _ { t } } \bar { w _ { t } }$$

无分类器引导（CFG）通过对无条件得分与条件得分进行插值实现可控生成：

$$\nabla _ { z } \log { p _ { t , \lambda } ( z | y ) } = ( 1 - \lambda ) \nabla _ { z } \log { p _ { t } ( z ) } + \lambda \nabla _ { z } \log { p _ { t } ( z | y ) }$$

其中 $\lambda$ 为引导强度参数。上述公式构成了MSG方法推导的数学基础。

### 3.2 得分分解与运动信息提取

MSG的核心洞察在于：**早期扩散时间步（$t \ll T$）的条件得分函数编码了丰富的运动信息**。基于此，方法将运动迁移建模为得分空间中的势能混合问题。

首先，将条件得分显式分解为运动得分和内容得分两部分：

$$\nabla _ { z } \log p _ { t } ( z , \mathcal { M } ( z ^ { * } ) | y ) = \nabla _ { z } \log p _ { t } ( \mathcal { M } ( z ^ { * } ) | y ) + \nabla _ { z } \log p _ { t } ( z | \mathcal { M } ( z ^ { * } ) , y )$$

其中 $\mathcal{M}(z^*)$ 为从参考视频提取的运动表示。**运动表示算子**直接使用早期时间步的条件得分作为运动特征：

$$\mathcal { M } ( z ) = \nabla _ { z _ { t } } \log p _ { t } ( z | y )$$

该设计的有效性在Figure 2中得到了可视化验证：从早期时间步得分中可清晰提取多物体运动和组合相机运动的特征模式。

### 3.3 MSG得分引导公式

MSG的核心引导信号定义为内容条件得分与参考运动得分差的线性组合：

$$s _ { \mathrm { M S G } } ( z _ { t } , z _ { t } ^ { * } ) = \nabla _ { z } \log p _ { t } ( z | y ) + w _ { \mathrm { M S G } } ( \nabla _ { z } \log p _ { t } ( z ^ { * } | y ^ { * } ) - \nabla _ { z } \log p _ { t } ( z ) )$$

其中：
- $\nabla_z \log p_t(z|y)$ 为内容条件得分，负责保持目标文本提示的语义一致性
- $\nabla_z \log p_t(z^*|y^*)$ 为参考视频的条件得分，编码参考运动模式
- $\nabla_z \log p_t(z)$ 为无条件先验得分，用于消除内容无关的统计偏差
- $w_{\text{MSG}}$ 为运动迁移强度权重

该公式的关键在于：通过**得分差** $\nabla_z \log p_t(z^*|y^*) - \nabla_z \log p_t(z)$ 提取纯净的运动信息，避免了内容信息的干扰。

### 3.4 混合势能与修正朗之万动力学

为保证生成过程的稳定性，MSG将上述得分引导转化为势能函数形式：

$$U _ { \mathrm { M S G } } ( z _ { t } ) = U _ { \mathrm { c o n t e n t } } ( z _ { t } ) + v _ { \mathrm { M S G } } [ U _ { \mathrm { m o t i o n } } ( z _ { t } , z _ { t } ^ { * } ) - U _ { \mathrm { p r i o r } } ( z _ { t } ) ]$$

其中 $U_{\text{content}}$ 为内容保持势能，$U_{\text{motion}}$ 为运动引导势能，$U_{\text{prior}}$ 为先验正则化势能，$v_{\text{MSG}}$ 控制混合比例。在该混合势能驱动下，采样过程通过修正的朗之万动力学SDE实现：

$$dz = \frac{\epsilon}{2} \nabla \log p(z) dt + \sqrt{\epsilon} d\bar{w}_t$$

该框架确保了运动迁移过程中的内容保留和生成质量。

### 3.5 关键实现参数

根据实验验证（Section 5），MSG引导仅在**扩散过程的前10%时间步**应用，在运动保留与生成质量之间取得最优平衡。运动提取阶段的噪声强度参数设为 $\text{strength}=0.7$：低于0.6时运动转移不足，高于0.8时产生过度风格化（Figure 8）。所有实验在CogVideoX预训练模型上以720×480分辨率、50个扩散时间步进行，无需任何额外训练或微调。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/009_Figure_8.jpg]]
*Figure 8: Ablation study on strength and timestep parameters. Left: We analyze the effect of noise addition in the motion extraction stage, where strength=0.7 achieves optimal motion representation - lower values (0.6) result in weak motion transfer while higher values (0.8) lead to over-stylization. Right: Impact of applying Mixture of Score guidance at different timestep ratios of total 50 timesteps on motion transfer quality*

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/002_Figure_2.jpg]]
*Figure 2: Our intuition. Visualization of motion characteristics M(z) extracted from early-timestep conditional scores. (Left) Multiple object motion representation showing the simultaneous movement of two objects. (Right) Combined object and camera motion representation demonstrating how our method captures both local object motion and global camera movement patterns. The visualizations are obtained from the conditional score maps ∇z log pt(z|y) at early timesteps t ≪ T*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/010_Figure_9.jpg]]
*Figure 9: Comparison of different guidance mechanisms. Comparing our Mixture of Score Guidance (MSG) against Classifier-Free Guidance (CFG, baseline without reference) and Unconditional Score Guidance (USG, using reference video’s unconditional score)*

## 实验与分析

### 定量主结果

MotionShop 在 MotionBench 基准上取得了最优的 **Motion Fidelity（0.913）** 和 **Temporal Consistency（0.928）**，相比最强基线 DMT 在运动保真度上提升 2.9%（Table 1）。在 Text Similarity 指标上，MotionShop 取得 0.314，略低于 VMC 的 0.328，体现出运动迁移与文本对齐之间存在可预期的权衡。

为全面评估方法性能，作者进行了包含 50 名参与者的用户研究，从文本对齐、运动保真度和时序一致性三个维度进行人工偏好评分。MotionShop 分别获得 0.41 / 0.43 / 0.38 的偏好分数，在运动保真度维度上优势最为显著（Table 1）。

所有对比方法均在 CogVideoX 预训练模型、相同分辨率（720×480）和帧率（15 FPS）下进行评估，确保了比较的公平性。

### 定性对比分析

在定性对比中（Figure 5），MotionShop 与 VMC、DMT、MD、MI 四种基线方法在三个挑战性场景下进行了比较：单物体运动迁移（机器人在沙漠中驾驶摩托车）、多物体交互场景以及复杂背景变化场景。MotionShop 在保持参考运动模式的同时，生成了与目标文本提示高度匹配的新内容，而基线方法在不同程度上出现了运动丢失、物体形变或内容不一致的问题。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of motion transfer capabilities. We compare MotionShop (bottom row) with existing methods (VMC, DMT, MD, MI) on three challenging scenarios. Left: Single object motion transfer of a robot-driven motorcycle in a desert scene. Middle: Multiple object motion transfer involving miniature medieval knights, demonstrating the ability to preserve interactions between objects. Right: Camera motion transfer capturing the dynamic perspective of a raindrop on a leaf. Our method demonstrates superior motion-text alignment across all three motion transfer categories*

Figure 4 进一步展示了 MotionShop 在单物体和多物体场景下，从文本提示生成新颖内容时对运动先验的保持能力。Figure 7 专门验证了相机运动迁移能力，展示了在不同场景下对相机轨迹的精确复现。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/008_Figure_7.jpg]]
*Figure 7: Camera Motion Transfer Results Across Diverse Scenarios. Each row shows the camera trajectory (left) and corresponding input-output image sequences. Our method can transfer camera motions while maintaining spatial consistency, as demonstrated in various cases: a steampunk clockwork butterfly animation, a raindrop on a leaf, an eagle soaring through mountain peaks, and dominos falling on a rail track. The colored trajectories represent the camera path through 3D space, with different colors indicating temporal progression*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results demonstrating our method’s ability to preserve motion priors while generating novel content from text prompts. (Left) Single-object motion transfer where complex motions like mechanical movements, horseback riding sequences are accurately preserved in the generated outputs. (Right) Multi-object scenarios where our method successfully maintains the original motion dynamics while generating diverse subjects. Please refer to the Supplementary Material for full videos and additional examples*

### 权衡分析

Figure 6 展示了 Text Similarity 与 Motion Fidelity 之间的权衡关系。MotionShop（绿色星标）在保持竞争性文本相似度的同时，取得了最高的运动保真度（0.913），在帕累托前沿上优于所有对比方法。这表明 MSG 的得分分解策略在运动保留和内容生成之间实现了更好的平衡。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/007_Figure_6.jpg]]
*Figure 6: Trade-off Analysis between Text Similarity and Motion Fidelity. Comparison of our method against baselines shows superior performance in both metrics, with our approach (green star) achieving higher motion fidelity (0.913) while maintaining competitive text similarity (0.314)*

### 消融实验

**噪声强度参数（strength）**：Figure 8（左）显示，运动提取阶段的噪声强度参数在 strength=0.7 时取得最佳效果。当 strength 低于 0.6 时，运动转移不充分，生成视频的运动模式与参考视频差异较大；当 strength 高于 0.8 时，出现过度的风格化现象，生成质量下降。这一参数控制着随机反演过程中添加到输入视频潜变量中的噪声量，直接影响运动表示 $\mathcal{M}(z^*)$ 的提取质量。

**引导时间步范围**：Figure 8（右）验证了 MSG 引导应用时间步比例的影响。将 MSG 引导限制在扩散过程的前 10% 时间步，可在运动保留与生成质量之间取得良好平衡。这一发现与论文的核心洞察一致——早期扩散时间步的条件得分函数中包含丰富的运动信息（Figure 2），在此阶段进行得分混合引导最为有效。

**引导机制对比**：Figure 9 将 MSG 与两种替代引导机制进行了对比——Classifier-Free Guidance（CFG）和 Unconditional Score Guidance（USG）。结果表明，MSG 在运动一致性和提示引导精度上均显著优于两种基线。MSG 的优势源于其显式地将条件得分分解为运动得分和内容得分，从而实现了对迁移过程更精确的控制。

### 失败模式与局限

当前方法存在以下已知局限：

1. **模型泛化性未验证**：所有实验仅基于 CogVideoX 模型进行，未在其他视频扩散骨干网络（如 VideoCrafter、ModelscopeT2V 等）上测试 MSG 的泛化能力。
2. **超参数需手动调节**：强度参数和 MSG 权重 $w_{\text{MSG}}$ 需要针对不同场景进行经验性搜索，缺乏自动调节策略。
3. **目标域外鲁棒性未知**：当目标概念超出基础 T2V 模型的训练分布时，MSG 的鲁棒性尚未得到系统性评估。
4. **长视频/高分辨率扩展**：MSG 在更长视频或更高分辨率生成场景下的适用性仍是开放问题。

### MotionBench 数据集

Table 2 展示了 MotionBench 数据集中不同运动类别的视频分布。该数据集提供了多种运动类型的均衡表示，包括单物体运动、多物体交互、相机运动等类别，为运动迁移方法的全面评估提供了基础。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/012_Table_2.jpg]]
*Table 2: Distribution of videos across different motion categories in MotionBench. The dataset provides a balanced representation of various motion types, enabling comprehensive evaluation of motion transfer methods*

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/001_Figure_1.jpg]]
*Figure 1: Mixture of Score Guidance (MSG), a novel approach for zero-shot motion transfer in diffusion models, enables high-fidelity motion synthesis across diverse scenarios. MSG successfully handles various motion patterns including complex object movements and camera trajectories. Full video results are available in the supplementary material*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/011_Figure_10.jpg]]
*Figure 10: Type of Questions. We ask 3 different questions for Text Alignment, Motion Fidelity and Temporal Consistency*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2412_05355/figures/005_Figure.jpg]]
*Figure: “A motorcycle driven by a robot, cruising through a desert” “A pair of miniature medieval knights” “A raindrop clinging to a green leaf, reflecting its surroundings like a tiny mirror.”*

## 方法谱系与知识库定位

### 1. 问题定位：零样本运动迁移的核心瓶颈

视频运动迁移任务要求在保留参考视频运动模式的同时，将目标内容替换为文本提示所描述的新场景。现有方法普遍面临一个根本性瓶颈：**运动保真度与场景适应性之间的张力**——要么通过额外训练/微调来适配特定运动模式，牺牲了零样本泛化能力；要么在零样本条件下难以同时处理多物体交互、复杂相机运动和大幅场景变化。

MotionShop 将这一瓶颈重新表述为**扩散模型得分空间中的势能混合问题**，其核心洞察在于：早期扩散时间步（t ≪ T）的条件得分函数 $\nabla_z \log p_t(z|y)$ 中编码了丰富的运动信息，而将该信息从内容条件中显式解耦，即可在无需任何训练的条件下实现运动迁移。这一视角将运动迁移从“特征对齐”或“隐空间插值”的范式，转向了**统计力学框架下的势能组合**，为理解扩散模型中的运动表征提供了新的理论锚点。

### 2. 方法谱系：从训练依赖到得分空间操作

当前视频运动迁移方法可根据其对**训练/微调的依赖程度**和**运动表征的显式程度**划分为三个代际，MotionShop 属于第三代的代表性工作。

**第一代：基于优化的运动迁移。** 典型方法通过逐样本优化（如测试时微调时间注意力层或注入运动向量）来适配参考运动，计算开销大且泛化受限。

**第二代：基于微调的参数高效迁移。** 代表性工作包括 **MotionDirector (MD)** 和 **DMT**（具体会议/年份需人工核实），它们采用双路径 LoRA 或时间层调整策略，在预训练视频扩散模型上学习运动与外观的解耦表示。这类方法相比第一代显著降低了计算成本，但仍需对每个参考视频进行微调，且运动模式的可迁移性受限于训练数据的分布。

**第三代：零样本得分空间操作。** MotionShop 提出的 **Mixture of Score Guidance (MSG)** 完全摒弃了训练/微调环节，直接在预训练视频扩散模型的得分函数上进行操作。其关键创新在于将运动迁移建模为得分空间中的势能混合：

$$U_{\mathrm{MSG}}(z_t) = U_{\mathrm{content}}(z_t) + v_{\mathrm{MSG}} \left[ U_{\mathrm{motion}}(z_t, z_t^*) - U_{\mathrm{prior}}(z_t) \right]$$

其中 $U_{\mathrm{motion}}$ 来自参考视频早期时间步的条件得分，$U_{\mathrm{prior}}$ 为无条件先验势能，二者的差值构成“运动增量”，通过混合权重 $v_{\mathrm{MSG}}$ 注入内容生成过程。这一公式在形式上类似于能量基模型中的势能组合，但将其应用于扩散模型的采样动力学中，实现了运动与内容的显式解耦控制。

与同属得分引导范式的 **CFG（Classifier-Free Guidance）** 和 **USG（Unconditional Score Guidance）** 相比，MSG 的核心区别在于引导信号的来源：CFG 仅在条件得分与无条件得分之间插值，USG 使用参考视频的无条件得分作为引导，而 MSG 使用**参考视频的条件得分差**（$\nabla_z \log p_t(z^*|y^*) - \nabla_z \log p_t(z)$）作为运动增量，从而更精确地提取了运动信息而非内容风格。

### 3. 关键设计选择与因果机制

MotionShop 的方法架构包含三个关键设计选择，每个选择都对应一个因果机制：

**（1）运动信息提取时间步的选择。** 消融实验（Fig. 8 right）表明，仅在扩散过程的前 10% 时间步应用 MSG 引导可在运动保留与生成质量之间取得最佳平衡。这一现象的理论解释是：扩散模型的逆过程遵循从粗到细的生成顺序，早期时间步决定了全局结构和运动轨迹，而后期时间步填充纹理细节。将运动引导限制在早期时间步，相当于只在“结构形成阶段”注入运动约束，避免了对内容细节的干扰。

**（2）噪声强度参数 strength 的调节。** 在运动提取阶段，通过对参考视频潜变量添加受控噪声（strength=0.7 达到最优），可在运动信息保留与无关细节抑制之间取得平衡。低于 0.6 时运动转移不足，高于 0.8 时产生过度风格化（Fig. 8 left）。这一参数本质上控制了参考视频潜变量在扩散轨迹上的“回退”程度——适中的回退保留了足够的运动结构，同时丢弃了与内容绑定的外观信息。

**（3）修正的朗之万动力学采样。** MSG 将混合势能 $U_{\mathrm{MSG}}$ 嵌入朗之万动力学 SDE，确保采样过程在运动约束下仍保持稳定。这一设计避免了直接得分插值可能导致的不稳定采样轨迹，是 MSG 在保持生成质量的同时实现运动迁移的关键工程保障。

### 4. 适用边界与局限

**已验证的适用场景：**
- 单一物体运动迁移（如机械运动、骑马序列）
- 多物体交互场景（如两个物体的同步运动）
- 相机运动迁移（如推拉、摇移、跟拍等轨迹）
- 组合运动（物体运动 + 相机运动）

**已知局限：**
1. **模型骨干依赖**：当前方法仅在 CogVideoX 预训练模型上验证，未在其他视频扩散骨干网络（如 VideoCrafter、ModelScope、SVD 等）上测试其泛化能力。不同模型在得分函数设计、时间注意力机制、潜空间结构上的差异可能影响 MSG 的有效性。
2. **参数手动调节**：强度参数 strength 和 MSG 权重 $w_{\mathrm{MSG}}$ 需针对不同场景进行经验性搜索，缺乏自动调节策略。这在实际部署中增加了使用门槛。
3. **目标概念分布外问题**：当目标文本提示描述的概念超出基础 T2V 模型的训练分布时，MSG 的鲁棒性尚不明确。得分函数在分布外区域的估计误差可能被 MSG 的引导机制放大。

### 5. 开放问题与未来方向

基于上述分析，以下开放问题值得后续工作关注：

1. **参考运动表示的计算细节**：在无训练设置下，参考运动表示 $\mathcal{M}(z^*)$ 的具体计算流程是否依赖额外的对齐或归一化步骤？论文将 $\mathcal{M}(z)$ 定义为 $\nabla_{z_t} \log p_t(z|y)$，但在多帧视频中如何处理时间维度的得分聚合尚需进一步澄清。

2. **MSG 权重的自适应策略**：$w_{\mathrm{MSG}}$ 在不同场景下的最优值可能存在显著差异。是否可以设计基于运动复杂度、场景变化幅度或文本-运动匹配度的自适应权重调节机制？

3. **长视频与高分辨率扩展**：当前实验在 720×480 分辨率、50 扩散时间步、15 FPS 的设置下进行。MSG 框架在更长视频（如数百帧）或更高分辨率（如 1080p 以上）场景下的计算开销和运动一致性保持能力需要进一步验证。

4. **跨模型泛化性**：MSG 的理论框架不依赖于特定模型架构，但其实际效果是否能在不同视频扩散模型上复现，是评估该方法通用性的关键。

5. **MotionBench 的指标透明度**：论文中使用的 MotionBench 数据集的具体定量评估指标（如 FID 是否下降、运动保真度的计算方式等）尚未完全公开，这限制了第三方对结果的独立验证和公平比较。

---

**人工核实提示**：上述方法谱系中涉及的基线方法（MotionDirector、DMT、VMC、MotionInversion）的具体作者、会议和年份信息在提供的分析材料中未明确给出，建议查阅原始论文进行补充。

## 原文 PDF

![[paperPDFs/arxiv_2024/MotionShop_Zero_Shot_Motion_Transfer_in_Video_Diffusion_Models_with_Mixture_of_Score_Guidance.pdf]]
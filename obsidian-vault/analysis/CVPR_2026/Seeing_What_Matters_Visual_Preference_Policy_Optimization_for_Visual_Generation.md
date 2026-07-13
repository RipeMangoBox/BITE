---
title: "Seeing What Matters: Visual Preference Policy Optimization for Visual Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Seeing_What_Matters_Visual_Preference_Policy_Optimization_for_Visual_Generation.pdf
project_link: null
code_link: null
aliases:
- VPPOV
- SWMVPPOVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入感知结构化模块（PSM），利用预训练视觉骨干网络将标量优势分解为结构化的逐像素优势分配图，从而实现区域差异化优化。
primary_logic: 人类视觉偏好具有空间选择性；根据感知相关性重新分配优化压力，能在不依赖密集标注的情况下，使生成器聚焦于视觉关键区域，提升感知对齐与生成稳定性。
claims:
- ViPO在图像与视频基准上一致超越GRPO基线DanceGRPO，在域内和域外指标上均取得提升。
- 消融实验表明，语义感知的分配图是性能提升的关键，均匀分配图导致性能下降；将分配图应用于优势而非奖励能保持优化稳定性。
- PSM引入的训练开销极小，图像生成步骤时间仅增加1.0-1.8%，视频生成增加4.8%，峰值内存增长低于4.5%。
- HPD (image prompts) 上 HPSv2.1↑ = 0.3321 (ViPO DINO)
---

# Seeing What Matters: Visual Preference Policy Optimization for Visual Generation

> [!tip] 核心洞察
> 人类视觉偏好具有空间选择性；根据感知相关性重新分配优化压力，能在不依赖密集标注的情况下，使生成器聚焦于视觉关键区域，提升感知对齐与生成稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 见微知著：面向视觉生成的视觉偏好策略优化 |
| 英文题名 | Seeing What Matters: Visual Preference Policy Optimization for Visual Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18719) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Visual Preference Policy Optimization (ViPO) |
| Dataset | HPD, VidProM, VBench |

> [!tip] 效果简介
> - HPD (image prompts) 上，HPSv2.1↑ 0.3321 (ViPO DINO) vs 0.3203 (DanceGRPO) (+0.0118)；PickScore↑ 22.8305 (ViPO DINO) vs 22.5962 (DanceGRPO) (+0.2343)；ImageReward↑ 1.1883 (ViPO DINO) vs 1.0392 (DanceGRPO) (+0.1491)。
> - VidProM (video prompts) 上，VQ↑ (VideoAlign) 3.5501 (ViPO) vs 3.0935 (DanceGRPO) (+0.4566)；MQ↑ (VideoAlign) 1.1515 (ViPO) vs 0.8639 (DanceGRPO) (+0.2876)。
> - VBench (video OOD) 上，Total↑ 81.70 (ViPO) vs 80.84 (DanceGRPO) (+0.86)。

## 概要

现有面向视觉生成的强化微调方法（如 **DanceGRPO**，Xue et al., arXiv 2025）为每个生成样本分配单一的标量优势，忽略了视觉内容中丰富的空间与时间结构，导致对局部伪影校正不足，且无法建模细粒度的人类感知偏好。本文提出 **Visual Preference Policy Optimization (ViPO)**，核心思想在于：人类视觉偏好具有空间选择性，优化压力应根据感知相关性进行差异化分配。

ViPO 引入 **感知结构化模块（Perceptual Structuring Module, PSM）**，利用预训练视觉骨干网络（如 DINOv2、ResNet、SAM）从生成内容中提取视觉偏好线索，将全局标量优势分解为结构化的逐像素优势分配图，从而实现区域差异化的策略优化。这一设计使得生成器能够聚焦于视觉关键区域，在无需密集标注的情况下提升感知对齐与生成稳定性。

实验表明，ViPO 在图像和视频生成基准上一致超越 DanceGRPO：图像域内指标 HPSv2.1 从 0.3203 提升至 0.3321，视频域外指标 VBench Total 从 80.84 提升至 81.70。消融实验证实，语义感知的分配图是性能提升的关键，均匀分配图反而导致性能下降；将分配图应用于优势而非奖励能保持优化稳定性。此外，PSM 引入的训练开销极小——图像生成步骤时间仅增加 1.0–1.8%，视频生成增加约 4.8%，峰值内存增长低于 4.5%。



### 视觉生成的对齐瓶颈：从粗粒度标量反馈到细粒度感知信号

近年来，大规模视觉生成模型在文本到图像（T2I）和文本到视频（T2V）任务上取得了显著进展。然而，生成结果与人类偏好之间的对齐仍然是一个核心挑战。现有的偏好优化方法，特别是以 **DanceGRPO**（Xue et al., arXiv 2025）为代表的 GRPO（Group Relative Policy Optimization）流程，通过奖励模型为每个生成样本分配一个**标量优势值** $A_i$，并将其均匀地作用于生成内容的所有空间位置和时间帧。

这种粗粒度的反馈机制存在一个被忽视的结构性缺陷：**它完全忽略了视觉内容中丰富的空间与时间结构**。人类视觉偏好本质上是空间选择性的——观察者对不同区域的关注度和敏感度差异显著，例如前景主体与背景、运动区域与静态区域。标量优势将这种复杂的感知判断压缩为单一数值，导致优化信号在像素空间中被均匀摊派，无法对局部伪影进行差异化校正，也难以建模细粒度的感知线索。

### 现有方法的隐性风险：语义退化与优化不稳定

当标量优势驱动的 GRPO 被应用于视觉生成时，一个潜在的风险是**语义退化**。由于所有像素共享相同的优化方向和强度，模型可能在追求奖励最大化的过程中，对语义关键区域和非关键区域施加同等的修改压力，进而导致物体身份丢失、结构坍塌等不可逆的质量损伤。这一问题在长程训练中尤为突出——生成器可能学会“欺骗”奖励模型，而非真正提升视觉质量。

此外，现有 GRPO 流程通常依赖确定性 ODE 采样，缺乏足够的轨迹探索多样性，限制了强化学习阶段的策略搜索空间。这进一步加剧了粗粒度反馈与细粒度生成需求之间的错配。

### 本文动机：将感知结构化引入优势分配

针对上述瓶颈，本文提出一个核心洞察：**如果能根据视觉内容的感知相关性，将标量优势重新分配为结构化的逐像素权重，就能在不依赖密集人工标注的情况下，使生成器聚焦于视觉关键区域，实现感知对齐与生成稳定性的同步提升。**

这一动机直接催生了 **Visual Preference Policy Optimization（ViPO）** 方法。ViPO 的核心设计在于引入一个**感知结构化模块（Perceptual Structuring Module, PSM）**，利用预训练视觉骨干网络（如 DINOv2）从生成内容中提取视觉偏好线索，将组内标准化的标量优势 $A_i$ 分解为空间/时间分辨的逐像素优势 $A_i^p = \mathbf{M}(p) A_i$，其中 $\mathbf{M}$ 为感知分配图。这一机制使得优化压力能够根据区域的感知重要性进行差异化分配——高感知相关性的区域获得更强的优化信号，而低相关性的背景区域则受到相对抑制，从而在保持语义完整性的前提下实现精细化的视觉质量提升。



## 核心方法与创新机理

ViPO 的核心创新在于**将视觉生成中的策略优化从粗粒度的标量优势重构为细粒度的空间/时间结构化优势分配**，使模型能够根据视觉内容的感知相关性进行差异化优化。

### 瓶颈洞察：标量优势的结构性缺陷

现有 GRPO 流程（如 **DanceGRPO**，Xue et al., arXiv 2025）为每个生成样本分配单一标量优势 $A_i$，该值均匀作用于所有像素位置。这种粗粒度反馈存在根本性缺陷：视觉内容天然具有丰富的空间与时间结构——前景主体与背景、运动区域与静态区域对感知质量的贡献截然不同，但标量优势无法建模这种细粒度差异，导致对局部伪影校正不足，且无法捕捉人类视觉偏好的空间选择性。

### 核心机制：感知结构化优势分配

ViPO 通过引入**感知结构化模块（Perceptual Structuring Module, PSM）**，将标量优势分解为结构化的逐像素优势分配图。具体而言，PSM 利用预训练视觉骨干网络（如 DINOv2、ResNet、SAM）从生成内容中提取视觉偏好线索，构建空间/时间感知的分配图 $\mathbf{M}$，进而将标量优势 $A_i$ 转化为逐像素优势：

$$A_i^p = \mathbf{M}(p) A_i$$

其中 $p$ 表示空间位置。这一 changed slot 将优化压力从全局均匀分布转变为**根据感知相关性重新分配**：视觉上更重要的区域获得更高的优势权重，从而引导生成器聚焦于关键区域的精细优化，而无需依赖任何密集标注。

### 关键设计选择

PSM 由两个子模块构成：**Visual Preference Extractor (VPE)** 使用预训练视觉骨干提取特征嵌入，**Visual Preference Allocator (VPA)** 将特征聚合为分配图，经主成分分析与高斯平滑后得到最终分配图 $\mathbf{M}$。消融实验揭示了三个关键设计决策：

1. **分配图作用于优势而非奖励**：将分配图直接应用于奖励会导致性能下降（ImageReward: 1.0058 vs 1.1883），因为跨样本的语义区域位置不同，优势错配问题严重。作用于优势则能保持组内相对信号的稳定性。

2. **语义感知的结构化分配**：使用均匀全1分配图替代感知分配图导致 HPSv2.1 从 0.3321 降至 0.3043，证实语义结构化的分配图是性能提升的核心驱动力。

3. **方差加权聚合**：在 VPA 中采用方差加权聚合优于简单平均（PickScore: 22.8305 vs 22.7037），强调了主导语义方向在分配图中的重要性。

### 与基线方法的本质差异

与 DanceGRPO 相比，ViPO 的 changed slot 并非引入新的奖励模型或改变策略优化算法本身，而是**重构了优势的表征与分配方式**。这一创新使得 ViPO 能够在不增加显著训练开销（图像生成步骤时间仅增加 1.0-1.8%，峰值内存增长低于 4.5%）的前提下，在图像与视频生成的域内和域外指标上均取得一致提升。



ViPO 的整体 pipeline 围绕一个核心改造展开：将 GRPO 中粗粒度的**标量优势（scalar advantage）** 转化为细粒度的**逐像素优势分配**，使策略优化能够感知视觉内容的空间与时间结构。

### 数据流与模块关系

ViPO 的完整前向与优化流程如 Figure 2 所示，可分解为三条并行的信息流：

1. **生成与奖励评估流**：策略模型（如 Flux 或 Wan2.1）基于条件 $c$ 采样一组 $G$ 个输出 $\{\mathbf{o}_i\}_{i=1}^{G}$，奖励模型对每个输出给出标量奖励 $r_i$，经组内标准化后得到标量优势 $A_i$：
   $$A_i = \frac{r_i - \mathrm{mean}(\{r_1, r_2, \dots, r_G\})}{\mathrm{std}(\{r_1, r_2, \dots, r_G\})}$$

2. **感知结构化流**：同一组采样输出并行送入**感知结构化模块（Perceptual Structuring Module, PSM）**，由两个子模块串联构成：
   - **视觉偏好提取器（Visual Preference Extractor, VPE）**：使用预训练视觉骨干网络（如 DINOv2、ResNet、SAM）从生成内容中提取多尺度特征嵌入。
   - **视觉偏好分配器（Visual Preference Allocator, VPA）**：将提取的特征聚合为分配图 $S$，经主成分分析（保留 $K$ 个主成分）、高斯平滑（$\sigma=1$）和上采样，得到与生成内容空间分辨率对齐的最终分配图 $\mathbf{M}$。

3. **优势分解与策略优化流**：标量优势 $A_i$ 与分配图 $\mathbf{M}$ 在空间维度上逐位置相乘，得到逐像素优势：
   $$A_i^p = \mathbf{M}(p) \, A_i$$
   该细粒度优势被注入 ViPO 的策略优化目标函数，在潜空间的所有空间位置 $p \in \mathcal{P}$ 和时间步上进行求和，驱动差异化参数更新。

### 关键设计决策

- **分配图作用于优势而非奖励**：消融实验（Table 3）表明，将分配图直接应用于奖励会导致性能下降（ImageReward: 1.0058 vs 1.1883）。原因在于不同样本的语义区域空间位置不同，奖励层面的分配会破坏组内相对排序信号；而优势层面保留了稳定的相对关系，同时实现了语义结构化的细粒度分配。

- **SDE 采样引入探索随机性**：为支持 RL 优化中的多轨迹探索，ViPO 将确定性 ODE 采样替换为反向时间 SDE 采样，在流匹配框架中注入可控随机性，使同一条件可生成多样化的样本组。

- **方差加权聚合**：VPA 采用方差加权策略聚合特征，相较于简单平均能更好地保留主导语义方向（PickScore: 22.8305 vs 22.7037，Table 3）。

### 训练开销

PSM 引入的计算开销极小：图像生成步骤时间仅增加 1.0–1.8%，视频生成增加约 4.8%，峰值内存增长低于 4.5%（Table 5），表明该方法在保持轻量级的前提下实现了显著的感知对齐提升。

### 补充图表

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/001_Figure_1.jpg]]
*Figure 1: Brief illustration of our work. Existing GRPO for visual generation assigns a single scalar advantage to the entire content, producing coarse feedback that often leads to sub-optimal results. In contrast, our ViPO converts this coarse signal into preference-aware feedback, enabling fine-grained alignment. This allows, for instance, differentiated optimization of the dancing doll and its background, yielding outputs that are more coherent, harmonious, and perceptually pleasing*



### 3.1 从确定性采样到随机探索：SDE 采样

ViPO 建立在流匹配（Flow Matching）生成模型的强化学习微调框架之上。标准流匹配在推理时采用确定性 ODE 采样，这限制了强化学习所需的轨迹多样性。ViPO 将确定性 ODE 转换为随机 SDE 采样，引入可控的随机性以支持策略探索：

$$\mathrm{d} \mathbf{z}_t = (\mathbf{u}_t - \frac{1}{2} \varepsilon_t^2 \nabla \log p_t(\mathbf{z}_t)) \mathrm{d}t + \varepsilon_t \mathrm{d}\mathbf{w}$$

其中 $\mathbf{z}_t$ 为扩散潜变量，$\mathbf{u}_t$ 为流向量场，$\varepsilon_t$ 控制噪声注入强度，$\mathrm{d}\mathbf{w}$ 为 Wiener 过程。这一转换使得同一文本条件 $\mathbf{c}$ 下可采样出多样化的生成轨迹，为后续的组内相对优势估计奠定基础。

### 3.2 感知结构化模块（PSM）

PSM 是 ViPO 的核心创新，负责从生成内容中提取视觉偏好线索并构建空间/时间感知分配图。PSM 由两个子模块组成：

**视觉偏好提取器（VPE）**：使用预训练视觉骨干网络（如 DINOv2、ResNet、SAM）对生成样本 $\mathbf{x}$ 提取特征嵌入，捕获语义感知的视觉结构。不同骨干网络提取的偏好线索各有侧重——DINOv2 擅长语义级区域分割，ResNet 提供层次化纹理特征，SAM 则聚焦于实例级分割。

**视觉偏好分配器（VPA）**：将 VPE 提取的特征聚合为分配图 $\mathbf{S}$，经主成分分析（保留前 $K$ 个主成分）、高斯平滑（$\sigma$ 控制平滑程度）和上采样后得到最终分配图 $\mathbf{M}$。$\mathbf{M}$ 的空间分辨率与生成潜变量对齐，每个位置 $p$ 的值 $\mathbf{M}(p)$ 表示该区域在偏好优化中的相对重要性。

### 3.3 ViPO 策略优化目标

传统 GRPO 为每个样本分配单一标量优势 $A_i$，均匀作用于所有空间位置。ViPO 通过分配图 $\mathbf{M}$ 将标量优势分解为逐像素优势：

$$A_i^p = \mathbf{M}(p) A_i$$

其中 $A_i$ 为组内标准化后的标量优势：

$$A_i = \frac{r_i - \mathrm{mean}(\{r_1, r_2, ..., r_G\})}{\mathrm{std}(\{r_1, r_2, ..., r_G\})}$$

$r_i$ 为奖励模型对第 $i$ 个样本的评分，$G$ 为组内样本数。

ViPO 的完整策略优化目标函数为：

$$\mathcal{I}(\theta) = \mathbb{E}\left[ \frac{1}{G T_s |\mathcal{P}|} \sum_{i=1}^{G} \sum_{t=1}^{T_s} \sum_{p \in \mathcal{P}} \ldots \right]$$

其中 $T_s$ 为采样时间步数，$\mathcal{P}$ 为空间位置集合。该目标在空间维度上对每个位置 $p$ 进行独立求和，使得高 $\mathbf{M}(p)$ 值的感知关键区域获得更大的优化压力，而低值区域（如背景）的梯度信号被抑制，从而实现区域差异化的精细优化。

**分配图作用于优势而非奖励**是 ViPO 设计的关键决策。若将分配图直接应用于奖励 $r_i$，由于不同样本间语义区域的空间位置各异，会导致优势信号错配。将分配图作用于标准化后的优势 $A_i$，既保留了组内相对比较的稳定性，又实现了细粒度的语义空间分配。

### 补充图表

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/014_Figure_8.jpg]]
*Figure 8: Visualization of allocation maps. (a) Allocation maps produced by the PSM with different vision backbones. From left to right: the original image generated by Flux, followed by maps obtained using DINOv2, ResNet, and SAM. (b) Visualization of the top three principal components that compose the allocation map derived from DINOv2*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/012_Figure.jpg]]
*Figure: SAM ResNet DINOv2 PC 1 PC 3 PC 2*



## 实验与关键发现

### 主实验结果

ViPO 在图像生成与视频生成两个模态上均对 GRPO 基线 DanceGRPO（Xue et al., arXiv 2025）取得了稳定且一致的提升，覆盖域内人类偏好指标与域外泛化指标。

**图像生成。** 基于 Flux（FLUX.1-dev）骨干，ViPO 在 HPD 基准的三个核心指标上全面超越 DanceGRPO：HPSv2.1 从 0.3203 提升至 0.3321（+3.7%），PickScore 从 22.5962 提升至 22.8305，ImageReward 从 1.0392 提升至 1.1883（Table 1）。定性对比（Figure 3）显示，ViPO 生成的图像在细节丰富度、真实感渲染和整体感知质量上均优于 DanceGRPO，后者虽能引入更丰富的细节，但 ViPO 实现了更精细的增强。

**视频生成。** 基于 Wan2.1-T2V-14B-480P 骨干，ViPO 在域内指标 VQ（VideoAlign）上从 3.0935 提升至 3.5501（+14.8%），MQ 从 0.8639 提升至 1.1515（+33.3%）。在域外泛化基准 VBench 上，Total 得分从 80.84 提升至 81.70，其中 Quality 维度提升尤为显著（69.68 → 72.59，+2.91），Semantic 维度亦有小幅增益（83.63 → 83.98）（Table 2）。定性对比（Figure 4）中，ViPO 在运动动态和视觉真实感上均展现出实质性改进，红色框标注区域指示了相对原始 Wan2.1 的改进，绿色框标注区域指示了相对 DanceGRPO 的进一步优化。

**关键结论：** 将标量优势分解为结构化的逐像素分配图，能在不改变骨干模型与奖励模型的前提下，使生成器聚焦于视觉关键区域，从而在域内人类偏好和域外泛化两个维度上同时获益。

### 消融实验

消融实验围绕三个核心设计选择展开，揭示了 ViPO 性能提升的因果机制。

**分配图类型。** 将感知分配图替换为均匀全 1 分配图（Uniform map）导致 HPSv2.1 从 0.3321 骤降至 0.3043，甚至低于 DanceGRPO 的 0.3203（Table 3）。这表明性能提升的核心驱动力并非简单的空间求和扩展，而是语义结构化的区域差异化优化——均匀分配图实际上将 ViPO 退化回粗粒度的标量优势形式，同时因额外的空间求和操作引入了非必要的方差。

**优势 vs. 奖励。** 将分配图直接应用于奖励（Reward map）而非归一化后的优势，导致 ImageReward 从 1.1883 降至 1.0058（Table 3）。其根本原因在于：不同样本的语义区域在空间位置上并不对齐，直接将分配图作用于奖励会导致跨样本的优势错配，破坏组内相对排序的稳定性；而作用于归一化优势则保留了稳定的相对信号，同时实现了细粒度的语义分配。

**聚合策略。** 方差加权聚合（Weighted）优于简单平均（Average），PickScore 从 22.7037 提升至 22.8305（Table 3）。加权聚合通过强调主导语义方向，抑制了噪声成分对分配图的干扰，从而提供了更鲁棒的区域权重估计。

**主成分数量与空间平滑。** 保留 3 个主成分（K=3）在 HPSv2.1、ImageReward 和 PickScore 之间提供了鲁棒的平衡；K=4 或 K=5 虽在个别指标上有微小提升，但总体稳定性下降（Table 4）。高斯平滑（σ=1）有利于提升指标鲁棒性，但过度平滑（σ=2）反而降低性能，说明适度的空间连续性约束是必要的，但过强的平滑会抹去关键的局部偏好线索。

### 规则化奖励下的语义保持性

为验证 ViPO 在极端优化压力下的鲁棒性，作者设计了一个仅基于颜色通道差异的规则化奖励——红色度奖励（redness reward），定义为 $r(x) = x^{0} - \frac{1}{2}(x^{1} + x^{2})$，即红色通道强度与绿、蓝通道均值的差异。该奖励与语义内容完全无关，仅鼓励生成偏红的图像。

在此设定下（Figure 5），DanceGRPO 随着训练步数增加逐渐出现语义退化和结构坍塌——生成器为最大化红色度奖励而牺牲了原始语义意图。相比之下，ViPO 在相同优化压力下始终维持了语义一致性和结构完整性。这一对比直接验证了核心洞察：**感知引导的区域差异化优化使生成器对全局梯度信号的语义破坏具有更强的抵抗力**，因为优化压力被集中在视觉偏好相关的区域，而非均匀施加于所有像素。

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/007_Figure_5.jpg]]
*Figure 5: Comparison under the redness reward across training steps. As training progresses, results from DanceGRPO tend to suffer from semantic degradation and structural collapse. In contrast, ViPO consistently maintains the original semantic intent and structural integrity*

### 训练开销分析

PSM 引入的训练开销极小（Table 5）。在图像生成场景中，使用 DINOv2 骨干的 ViPO 单步生成时间仅从 59.66s 增加至 60.47s（+1.4%），峰值内存增长低于 4.5%。在视频生成场景中，开销稍高但依然可控：从 203.45s 增加至 213.27s（+4.8%）。不同视觉骨干（DINOv2/ResNet/SAM）之间的开销差异不显著，表明 PSM 的设计具有良好的模块化特性，可根据部署需求灵活替换视觉骨干。

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/013_Table_5.jpg]]
*Table 5: Training overhead of ViPO with different PSM backbones, compared with the corresponding DanceGRPO baseline*

### 分配图可视化分析

Figure 8 展示了不同视觉骨干生成的分配图及其主成分分解。DINOv2 产生的分配图呈现出与语义对象边界高度一致的空间结构，能够在物体内部和背景区域之间形成清晰的差异化权重；ResNet 的分配图粒度较粗，倾向于在更大尺度上区分前景与背景；SAM 的分配图则更聚焦于实例级别的分割边界。Figure 8(b) 的主成分可视化进一步表明，分配图的前三个主成分分别捕获了不同的视觉偏好维度（如主体显著性、纹理复杂度、构图平衡），这些成分的加权组合构成了最终的逐像素优势分配。

### 补充图表

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison results of Flux. ViPO variants consistently outperform the original Flux model and DanceGRPO on both in-domain and out-of-domain metrics*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison results of Wan2.1. ViPO surpasses both the Wan2.1 and DanceGRPO in all out-of-domain criteria, demonstrating superior generalization*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison on Flux. Each group of results is arranged from left to right as follows: outputs from Flux, DanceGRPO, and our proposed ViPO. Our method demonstrates the best visual performance, exhibiting richer details, more realistic rendering, and overall superior perceptual quality*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on Wan2.1. Each demo group is arranged top-to-bottom as follows: the result from Wan2.1, the output after applying DanceGRPO, and the output after applying ViPO. It is evident that our method delivers superior performance in terms of visual quality, and motion dynamics. In addition, we highlight representative regions with red boxes to indicate improvements over the Wan2.1, and green boxes to indicate improvements over DanceGRPO*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/008_Table_3.jpg]]
*Table 3: Ablation study on allocation map and aggregation strategies*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/009_Table_4.jpg]]
*Table 4: Ablation study on number of principal components and spatial smoothing*

![[assets/figures/papers/paper_list_l2592_https_arxiv_org_abs_2511_18719/figures/016_Figure_9.jpg]]
*Figure 9: Visualization of results obtained with different ViPO variants. From left to right: ViPO with DINOv2 as the PSM backbone, ViPO with ResNet, and ViPO with SAM*



## 定位与知识库关联

### 1. 与基线方法的谱系关系

ViPO 的核心技术定位是对 **GRPO（Group Relative Policy Optimization）** 在视觉生成场景中的细粒度扩展。其直接基线 **DanceGRPO**（Xue et al., arXiv 2025）首次将 GRPO 引入扩散模型的 RL 微调，但沿用了标准 GRPO 的标量优势分配机制——为每个生成样本分配单一标量优势 $A_i$，该优势均匀作用于所有像素位置的去噪过程。这一设计忽略了视觉内容中丰富的空间与时间结构，导致对局部伪影校正不足，且无法建模细粒度感知线索。

ViPO 的关键突破在于**优势表征的重构**：引入感知结构化模块（PSM），利用预训练视觉骨干网络将标量优势分解为结构化的逐像素优势分配图 $A_i^p = \mathbf{M}(p) A_i$，从而实现区域差异化优化。这一改进在方法谱系上可视为将 GRPO 从“全局均匀反馈”推向“感知自适应反馈”的范式升级。

在基础模型层面，ViPO 的图像生成实验基于 **Flux（FLUX.1-dev）**，视频生成实验基于 **Wan2.1-T2V-14B-480P**，两者均为当前主流的扩散/流匹配生成骨干。DanceGRPO 同样基于这些骨干进行 RL 微调，因此 ViPO 与 DanceGRPO 的对比在模型基础上完全公平。

### 2. 与其他 RLHF/偏好优化方法的定位

从更广泛的偏好对齐方法谱系来看，ViPO 属于**在线策略优化**路线的细粒度扩展。与 DPO（Direct Preference Optimization）等离线偏好学习方法不同，ViPO 保留了 GRPO 的在线采样-评估-优化循环，通过 SDE 采样引入随机性以支持多轨迹探索，从而获得更丰富的偏好信号。

ViPO 的独特贡献在于**感知结构化优势分配**这一机制创新。传统的标量优势方法（如 DanceGRPO、原始 GRPO）将奖励模型的单一评分均匀分配给所有像素，而 ViPO 通过 PSM 从视觉内容本身提取偏好线索，构建空间/时间感知的分配图。这一设计使得优化压力能够根据感知相关性重新分配，聚焦于视觉关键区域，在不依赖密集标注的情况下提升感知对齐与生成稳定性。

### 3. 适用边界

ViPO 的当前验证范围覆盖了以下场景：
- **图像生成**：基于 Flux 骨干，使用 HPSv2.1、PickScore、ImageReward 等人类偏好奖励模型进行 RL 微调。
- **视频生成**：基于 Wan2.1 骨干，使用 VideoAlign 等视频偏好模型进行 RL 微调。
- **规则化奖励**：在“redness reward”（红色通道强度奖励）的受控实验中验证了方法的语义保持能力。

论文未探索的边界包括：
- **大规模模型扩展性**：ViPO 在 Wan2.1-T2V-14B（14B 参数）上已验证，但未讨论在更大规模模型（如 >20B 参数）上的扩展性及额外训练成本。
- **其他条件生成模态**：该方法是否适用于文本条件之外的其他条件生成（如草图、布局、深度图等）尚未探索。
- **非扩散生成范式**：ViPO 的方法设计紧密耦合于扩散/流匹配的去噪过程，其在自回归生成等其他范式上的适用性需要进一步研究。

### 4. 局限与开放问题

**计算开销虽小但非零**：PSM 引入的训练开销在图像生成中仅增加 1.0–1.8% 的步骤时间，视频生成增加 4.8%，峰值内存增长低于 4.5%（Table 5）。这一开销在单次实验中可忽略，但在大规模超参数搜索或多轮迭代训练中会累积。

**视觉骨干的选择依赖**：PSM 依赖于预训练视觉骨干（如 DINOv2、ResNet、SAM），不同骨干的选择对性能有可观测影响（Table 1 中各 ViPO 变体的指标差异）。论文未提供自动化或自适应的骨干选择策略，实践中需要根据任务手动选择。

**分配图语义的可解释性有限**：虽然 Figure 8 可视化了分配图和主成分，但对分配图如何精确对应人类偏好判断的因果机制缺乏深入分析。

**奖励模型依赖性**：ViPO 的性能受限于底层奖励模型的质量。如果奖励模型本身存在偏置（如对特定纹理、构图的偏好），PSM 的分配图可能会放大而非纠正这些偏置。

**开放问题**：
1. ViPO 的感知结构化优势分配是否可以推广到多模态奖励（如文本-图像对齐 + 美学质量 + 安全性）的联合优化？
2. PSM 的分配图是否可以与可学习的奖励模型联合训练，形成端到端的偏好感知优化？
3. 在更大规模的视频生成模型（如 Sora 级别）上，PSM 的时间维度扩展是否仍能保持线性开销增长？



## 原文 PDF

![[paperPDFs/CVPR_2026/Seeing_What_Matters_Visual_Preference_Policy_Optimization_for_Visual_Generation.pdf]]

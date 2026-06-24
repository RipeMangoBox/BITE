---
title: "SkeletonLLM: Universal Skeleton Understanding via Differentiable Rendering and MLLMs"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs.pdf
aliases:
- SkeletonLLM
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入可微、格式无关的骨架渲染器DrAction，结合3D高斯泼溅与线性混合蒙皮的端到端优化，使MLLM的梯度可反向传播至渲染过程，学习出任务最优的视觉表征；同时通过因果推理蒸馏（CR-Distill）和判别式微调（Disc-FT）的协同训练策略，赋予模型结构化推理和细粒度区分能力。
primary_logic: 将任意骨架序列“翻译”为MLLM原生视觉模态（紧凑图像序列）是打破格式孤岛和语义鸿沟的关键；通过可微渲染，梯度直接引导渲染器生成对下游任务最具区分力的视觉令牌，既保留了运动细节，又绕开了为每个骨架格式定制编码器的需求，真正迈向通用骨架理解。
claims:
- 在NTU-60 30/30极端少样本划分上，SkeletonLLM达到37.84% Top-1准确率，超越最佳基线TDSM的25.88%（+11.96%）。
- 跨格式传输（NTU-60 Kinect v2 → NW-UCLA Kinect v1）下，SkeletonLLM准确率达27.33%，较最佳基线SKI-LVLM的10.14%提升17.19%。
- 移除神经特征调制器（NFM）后，NTU-60 48/12性能从64.72%降至61.09%（-3.63%），验证了运动感知着色的重要性。
- 移除因果推理蒸馏（CR-Distill）导致NTU-60 30/30性能从37.84%降至35.90%（-1.94%），证明结构化推理蒸馏的关键作用。
---

# SkeletonLLM: Universal Skeleton Understanding via Differentiable Rendering and MLLMs

> [!tip] 核心洞察
> 将任意骨架序列“翻译”为MLLM原生视觉模态（紧凑图像序列）是打破格式孤岛和语义鸿沟的关键；通过可微渲染，梯度直接引导渲染器生成对下游任务最具区分力的视觉令牌，既保留了运动细节，又绕开了为每个骨架格式定制编码器的需求，真正迈向通用骨架理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | SkeletonLLM：通过可微渲染与多模态大语言模型实现通用骨架理解 |
| 英文题名 | SkeletonLLM: Universal Skeleton Understanding via Differentiable Rendering and MLLMs |
| 会议/期刊 | arXiv 2026 |
| Links |  [paper](https://arxiv.org/abs/2603.18003)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SkeletonLLM |
| Dataset | NTU-60, NTU-120, NTU-60 → NW-UCLA, HumanML3D → NW-UCLA |

> [!tip] 效果简介
> - NTU-60 (30/30 split) 上，Top-1 Accuracy (%) 37.84 vs 25.88 (TDSM) (+11.96)。
> - NTU-120 (60/60 split) 上，Top-1 Accuracy (%) 34.94 vs 27.21 (TDSM) (+7.73)。
> - NTU-60 → NW-UCLA (Cross-format) 上，Top-1 Accuracy (%) 27.33 vs 10.14 (SKI-LVLM) (+17.19)。

## 概述

多模态大语言模型（MLLM）在视觉理解与推理上展现了强大能力，却无法原生处理结构化骨架数据——这是动作识别、人机交互等领域的核心模态。现有方法试图通过特征-文本对齐或离散词元化将骨架“翻译”给语言模型，但这类方案存在两个根本性缺陷：**格式依赖**——每种骨架拓扑需要定制编码器；**表示瓶颈**——运动信息被压缩为单一向量或在离散化中丢失细粒度时空细节。更关键的是，它们绕开了MLLM最宝贵的资产——预训练视觉理解能力，未能真正弥合骨架与语言之间的模态鸿沟。

**SkeletonLLM** 的核心洞察是：将任意骨架序列“翻译”为MLLM原生的视觉语言（紧凑图像序列），是打破格式孤岛和语义鸿沟的关键。为此，论文提出了 **DrAction**（Differentiable Rendering of Actions）——一个基于3D高斯泼溅与线性混合蒙皮的可微渲染器。DrAction 将骨架运动学参数化为可变形高斯原语，渲染出运动感知的图像序列；其可微性使MLLM的梯度能够反向传播至渲染过程，端到端地学习出对下游任务最具区分力的视觉表征。配合**因果推理蒸馏**（CR-Distill）与**判别式微调**（Disc-FT）的协同训练策略，SkeletonLLM 赋予了模型结构化推理和细粒度区分能力，真正迈向通用骨架理解。

**主要结果**：在极端少样本场景下，SkeletonLLM 的优势尤为显著——NTU-60 30/30划分上达到37.84% Top-1准确率，超越最佳基线TDSM（Do & Kim, ICCV 2025）的25.88%（+11.96%）。跨格式迁移任务中，从NTU-60（Kinect v2）到NW-UCLA（Kinect v1）的零样本识别准确率达27.33%，较基线SKI-LVLM的10.14%提升17.19个百分点，验证了DrAction格式无关渲染的有效性。消融实验进一步证实：移除神经特征调制器（NFM）导致性能下降3.63%，移除因果推理蒸馏在少样本设置下损失1.94%，表明运动感知渲染与结构化推理蒸馏均是不可或缺的关键组件。

**方法定位**：SkeletonLLM 区别于传统的特征-文本对齐路线（如PURLS, Zhu et al., CVPR 2024；TDSM；SCoPLe, Zhu et al., CVPR 2025）和基于离散词元的LLM方案（如MotionGPT, Jiang et al., NeurIPS 2023；MotionLLM, Chen et al., TPAMI 2025），首次将骨架理解重构为“渲染-推理-响应”的视觉理解问题，使MLLM的预训练视觉能力得以直接复用。

## 背景与动机

### 骨架理解的核心瓶颈：格式孤岛与模态鸿沟

多模态大语言模型（MLLM）在视觉推理、开放词汇识别等任务上展现出强大能力，但其原生输入模态为图像与文本，无法直接处理结构化的三维骨架序列数据。这一**模态鸿沟**构成了骨架理解领域长期悬而未决的根本性障碍。

现有主流方案试图通过两类路径弥合这一鸿沟：

- **特征-文本对齐方法**（如 **PURLS**（Zhu et al., CVPR 2024）、**TDSM**（Do & Kim, ICCV 2025）、**SCoPLe**（Zhu et al., CVPR 2025））将骨架序列压缩为单一特征向量，再与文本嵌入进行匹配。这类方法存在严重的**表示瓶颈**：将整段运动压缩为固定维度的全局向量，不可避免地丢失了细粒度的时序动态信息和局部关节运动学线索；同时，编码器与特定骨架拓扑深度耦合，每换一种格式就需要重新设计特征提取器。
- **基于LLM的运动理解方法**（如 **MotionGPT**（Jiang et al., NeurIPS 2023）、**MotionLLM**（Chen et al., TPAMI 2025））通过VQ-VAE将运动数据离散化为词元，再送入语言模型。这类方法虽然利用了LLM的推理能力，但离散化过程进一步压缩了运动细节，且词元化方案同样绑定于特定骨架格式，无法实现跨格式泛化。

上述两类方法的共同缺陷在于：**未能真正利用MLLM强大的预训练视觉理解能力**。它们试图将骨架数据强行适配为文本或离散词元，而非将其转化为MLLM原生擅长的视觉语言。

### 格式孤岛：跨格式泛化的结构性困境

现实世界中，骨架数据因采集设备（Kinect v1/v2、MoCap、姿态估计算法）的不同，在关节数量、拓扑结构、坐标系定义上存在巨大差异。例如，NW-UCLA 使用 Kinect v1 的 20 关节拓扑，NTU-60 使用 Kinect v2 的 25 关节拓扑，而 HumanML3D 基于 SMPL 模型的 22 关节结构。传统方法中，编码器与特定骨架格式深度绑定，导致模型从一个格式切换到另一个格式时需要重新设计输入层甚至整体架构，形成了**格式孤岛**——每个格式都像是被隔离的孤岛，模型无法在岛间自由迁移。

### 本文动机：将骨架“翻译”为MLLM的母语

面对上述双重困境，本文提出一个根本性的思路转变：**与其强迫MLLM学习理解骨架数据，不如将骨架数据“翻译”为MLLM原生理解的视觉语言**。核心洞察在于：

> 将任意骨架序列转化为紧凑的图像序列，是打破格式孤岛和语义鸿沟的关键。

这一思路带来三重优势：

1. **格式无关性**：无论底层骨架拓扑如何变化，渲染出的图像序列均可被同一MLLM视觉编码器处理，从根本上消除了格式依赖。
2. **视觉理解复用**：MLLM在海量自然图像上预训练获得的视觉理解能力（如局部纹理感知、空间关系推理）可直接迁移至骨架渲染图像，无需从零学习。
3. **端到端可优化**：若渲染过程可微，则MLLM的梯度可反向传播至渲染器，引导其学习出对下游任务最具区分力的视觉表征，而非依赖人工设计的固定渲染策略。

正是基于这一动机，本文提出了 **SkeletonLLM** 框架，其核心组件 **DrAction**（Differentiable Rendering of Actions）——一个基于3D高斯泼溅与线性混合蒙皮的可微、格式无关的骨架渲染器——将骨架序列转化为运动感知的图像序列，使MLLM能够以原生视觉模态理解和推理人类动作。

## 核心创新

SkeletonLLM 的核心创新在于**范式转换**：不再试图将结构化骨架数据强行适配进 MLLM 的文本通道，而是通过可微渲染将其“翻译”为 MLLM 原生理解的视觉语言。这一转换从三个关键维度（changed slots）打破了现有方案的瓶颈。

### 1. 输入模态：从坐标编码到可微渲染图像序列

现有主流方案面临严重的**格式孤岛**与**模态鸿沟**问题。特征-文本对齐方法（如 **PURLS**（Zhu et al., CVPR 2024）、**TDSM**（Do & Kim, ICCV 2025）、**SCoPLe**（Zhu et al., CVPR 2025））将骨架压缩为单一特征向量与文本嵌入对齐，造成细粒度运动信息的表示瓶颈；VQ-VAE 离散词元化方法（如 **MotionGPT**（Jiang et al., NeurIPS 2023）、**MotionLLM**（Chen et al., TPAMI 2025））则依赖特定骨架格式训练离散码本，跨格式泛化能力受限。两类方法均未能真正利用 MLLM 强大的预训练视觉理解能力。

SkeletonLLM 的核心洞察是：**将任意骨架序列“翻译”为 MLLM 原生视觉模态（紧凑图像序列）是打破格式孤岛和语义鸿沟的关键**。这一转换绕开了为每种骨架格式定制编码器的需求，使 MLLM 的视觉推理能力可直接作用于骨架数据。

### 2. 渲染器类型：从固定渲染到可微 DrAction 渲染器

传统骨架渲染方法（3D+Velocity、2D 投影、JTM）产生的是固定、不可学习的视觉表征，无法根据下游任务自适应优化。SkeletonLLM 提出 **DrAction**（Differentiable Rendering of Actions），其关键机制包括：

- **3D 高斯泼溅 + 线性混合蒙皮（LBS）**：将任意骨架拓扑提升为可变形 3D 高斯原语。规范空间中每个高斯原语定义为 $\mathcal{G}_k^c = \{ \pmb{\mu}_k^c, \mathbf{s}_k^c, \mathbf{q}_k^c, \alpha_k^c, \mathbf{f}_k \}$，通过 LBS 驱动变形：$\mathbf{t}_k = \sum_{i=1}^J w_{k,i} \mathbf{t}_i$，$\tilde{\mathbf{R}}_k = \sum_{i=1}^J w_{k,i} \mathbf{R}_i$，再经 SVD 投影至 SO(3) 群以确保旋转有效性。原语数量随输入骨架的关节数和骨骼边数自动适配，天然具备**格式无关**特性。

- **神经特征调制器（NFM）**：基于局部运动学（关节深度、速度等）自适应调制高斯原语的色彩与透明度，使渲染图像动态高亮运动关键区域（如踢腿动作中的发力腿），生成更具信息量的视觉语言。

- **端到端可微性**：MLLM 的任务损失梯度可反向传播至渲染过程的每个参数（高斯原语位置、尺度、旋转、不透明度及 NFM 权重），使渲染器学习出任务最优的视觉表征。这既保留了运动细节，又避免了手工设计渲染策略的信息损失。

消融实验（Table 7）验证了可微渲染的决定性优势：移除 NFM 后，NTU-60 48/12 性能从 64.72% 降至 61.09%（-3.63%），证明运动感知着色的关键作用。

### 3. 训练策略：从单阶段微调到四阶段协同训练

SkeletonLLM 引入四阶段渐进式训练策略，解决可微渲染器与 MLLM 联合优化的挑战：

1. **Alignment Warm-up**：预热渲染器，生成可理解的视觉图像；
2. **Discriminative Finetuning（Disc-FT）**：在 MLLM 挖掘的易混淆动作对上执行二值判别训练，强化决策边界。跳过此阶段导致 NTU-60 30/30 准确率下降 1.55 个百分点；
3. **Causal Reasoning Distillation（CR-Distill）**：从 GPT-4o 教师模型蒸馏结构化因果推理链（描述身体部位动力学与排除干扰项的因果逻辑），赋予模型结构化推理能力。移除该阶段导致 NTU-60 30/30 性能从 37.84% 降至 35.90%（-1.94%），且对需要推理的任务影响更大；
4. **Recognition Refinement**：在 MQA 任务上最终精调识别能力。

这一协同训练策略使模型同时具备**细粒度区分能力**（Disc-FT）和**结构化推理能力**（CR-Distill），在极端少样本场景下优势尤为显著——NTU-60 30/30 划分上，SkeletonLLM 以 37.84% Top-1 准确率超越最佳基线 TDSM 的 25.88%（+11.96%）。

## 整体框架

SkeletonLLM 遵循 **Render–Reason–Respond** 三阶段流水线（Figure 2），其核心设计原则是将任意骨架序列“翻译”为多模态大语言模型（MLLM）原生可消费的视觉模态——紧凑的图像序列，从而打破骨架格式孤岛与模态鸿沟。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SkeletonLLM. The pipeline follows a Render-Reason-Respond process for universal understanding. Given a skeleton sequence, DrAction lifts joint trajectories into deformable 3D Gaussian primitives and renders motion-aware images. Joint transforms are computed via Linear Blend Skinning, and kinematic cues (depth, velocity) are fused through a Neural Feature Modulator. All parameters are optimized end-to-end by gradients from the MLLM. The rendered frames are processed by the MLLM’s vision encoder and a projector to yield visual tokens. During training, CR-Distill supervises with teacher-generated causal chains describing body-part dynamics, while Disc-FT sharpens decision boundarie...*

### 数据流与模块拓扑

1. **输入**：一段包含 $T$ 帧的骨架序列 $\mathbf{S} = \{ \mathbf{p}_t \}_{t=1}^T$，其中 $\mathbf{p}_t$ 为 $J$ 个关节的 3D 坐标。该序列可来自任意骨架拓扑（Kinect v1/v2、MoCap、2D 姿态估计等），无需格式特定的预处理。

2. **可微渲染（Render）**：DrAction 渲染器将 $\mathbf{S}$ 映射为图像序列 $\mathbf{V}$。其内部流程为：
   - 将关节轨迹提升为绑定在运动链上的可变形 3D 高斯原语（Gaussian primitives），原语数量根据输入骨架的关节数 $J$ 和骨骼边数 $|E|$ 自动适配，天然支持跨格式。
   - 通过线性混合蒙皮（Linear Blend Skinning, LBS）计算每个高斯原语从规范空间到当前帧的刚体变换，并经 SVD 投影至 SO(3) 以保证旋转有效性。
   - 神经特征调制器（Neural Feature Modulator, NFM）基于局部运动学（关节深度、速度等）自适应调制各高斯原语的色彩与不透明度，使渲染图像动态突出运动关键区域（如踢腿时的腿部）。
   - 经深度排序与 alpha 合成生成最终像素，整个过程对渲染参数 $\Theta_{\mathrm{render}}$ 完全可微。

3. **视觉编码与投影（Reason 前序）**：渲染图像序列送入 MLLM 的视觉编码器（ViT）提取视觉令牌，再经一个 MLP 投影器（参数 $\Theta_{\mathrm{proj}}$）映射至语言模型的嵌入空间。

4. **语言推理与响应（Reason–Respond）**：语言模型（LLM）以自回归方式处理视觉令牌，生成推理链或最终标签。动作识别被形式化为多项选择问答（MQA）任务，模型需从候选项中选出正确答案。

### 梯度流与端到端可微性

整个架构——从骨架输入经渲染、视觉编码到语言生成——构成一条完整的可微计算图。MLLM 的监督信号（如交叉熵损失）可反向传播穿过投影器和视觉编码器，**直达 DrAction 渲染器的参数** $\Theta_{\mathrm{render}}$。这意味着渲染器并非以固定规则生成图像，而是在下游任务梯度的引导下，学习产生对当前任务最具区分力的视觉表征。这一机制是 SkeletonLLM 区别于所有固定渲染方案（如 3D+Velocity、2D 投影、JTM）的根本所在。

### 渐进式训练策略

由于渲染器与 MLLM 的联合优化空间高度非凸，SkeletonLLM 采用四阶段渐进式训练课程（Figure 5）：

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/013_Figure_5.jpg]]
*Figure 5: Our Progressive Training Pipeline. To address the joint optimization challenge, we progressively activate and fine-tune model components. The training curriculum begins with (a) warming up the renderer to generate intelligible visuals and concludes with (d) refining recognition, both utilizing a multiple-choice question & answer (MQA) task. In between, the strategy incorporates (b) learning discriminative features via a binary judgment task and (c) instilling causal reasoning through knowledge distillation from a teacher model*

1. **Alignment Warm-up**：冻结 MLLM，仅训练渲染器和投影器，使渲染器产生可理解的视觉输出。
2. **Discriminative Finetuning (Disc-FT)**：引入易混淆动作对的二值判别任务，强化模型在相似动作间的决策边界。
3. **Causal Reasoning Distillation (CR-Distill)**：从 GPT-4o 教师模型蒸馏结构化因果推理链，赋予模型“身体部位动态→动作语义”的结构化推理能力。
4. **Recognition Refinement**：在 MQA 任务上对全模型进行最终微调，巩固识别性能。

消融实验表明，移除 CR-Distill 导致 NTU-60 30/30 划分准确率下降 1.94 个百分点（Table 8），跳过 Disc-FT 则下降 1.55 个百分点，验证了各阶段的独立贡献。

### 补充图表

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/005_Table_4.jpg]]
*Table 4: Single-model multi-task evaluation. All results use the same NTU-60 (55/5) checkpoint with no task-specific retraining*

## 核心模块与公式推导

### 问题形式化与Render-Reason-Respond流水线

SkeletonLLM将通用骨架理解形式化为一个“渲染-推理-响应”（Render-Reason-Respond）流水线。给定任意拓扑的骨架序列 $\mathbf{S} = \{ \mathbf{p}_t \}_{t=1}^T$，其中 $\mathbf{p}_t$ 为 $t$ 时刻 $J$ 个关节、$P$ 个人的三维坐标，核心映射为：

$$\mathcal{R} : \mathbf{S} \mapsto \mathbf{V}$$

即将骨架序列“翻译”为MLLM原生视觉模态的图像序列 $\mathbf{V}$。该映射由可微渲染器DrAction实现，随后MLLM的视觉编码器提取视觉令牌，经投影层进入语言模型完成自回归生成（Section 3.1, Figure 2）。

### DrAction可微渲染器

DrAction的核心思想是将每一帧姿态建模为绑定在运动链上的可变形3D高斯原语，从而实现端到端可微且具备表现力的渲染（Section 3.2）。

**规范高斯原语**：每个原语在规范空间中的参数定义为：

$$\mathcal{G}_k^c = \{ \pmb{\mu}_k^c, \mathbf{s}_k^c, \mathbf{q}_k^c, \alpha_k^c, \mathbf{f}_k \}$$

其中 $\pmb{\mu}_k^c$ 为中心位置，$\mathbf{s}_k^c$ 为尺度，$\mathbf{q}_k^c$ 为四元数旋转，$\alpha_k^c$ 为不透明度，$\mathbf{f}_k$ 为可学习外观特征。原语数量根据输入骨架的关节数 $J$ 和骨骼边数 $|E|$ 自动适配，无需为不同拓扑定制（Appendix C.2）。

**关节刚体变换**：每个关节 $i$ 从规范姿态到当前姿态的SE(3)变换为：

$$\mathbf{R}_i = \mathrm{quat2mat}(\mathbf{q}_i^t), \ \mathbf{t}_i = \mathbf{j}_i^t - \mathbf{j}_i^c, \ \mathbf{T}_i = \left[ \mathbf{R}_i \ \mathbf{t}_i \right]$$

其中 $\mathbf{j}_i^c$ 和 $\mathbf{j}_i^t$ 分别为关节在规范帧和当前帧的三维位置，$\mathbf{q}_i^t$ 为当前帧的关节旋转四元数。

**线性混合蒙皮（LBS）**：利用预计算混合权重 $w_{k,i}$ 对双亲关节的位移和旋转进行线性插值：

$$\mathbf{t}_k = \sum_{i=1}^J w_{k,i} \mathbf{t}_i, \qquad \tilde{\mathbf{R}}_k = \sum_{i=1}^J w_{k,i} \mathbf{R}_i$$

**SO(3)投影**：由于混合后的 $\tilde{\mathbf{R}}_k$ 不再保证是有效旋转矩阵，通过SVD将其投影回SO(3)流形：

$$\tilde{\mathbf{R}}_k = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\top \Rightarrow \mathbf{R}_k = \mathbf{U} \mathrm{diag}(1,1,\mathrm{det}(\mathbf{U}\mathbf{V}^\top)) \mathbf{V}^\top$$

该投影可微且数值稳定，即使对于极端姿态也能保证有效旋转（Section 3.2）。

**高斯变换**：最终原语在三维空间中的均值和旋转为：

$$\pmb{\mu}_k = \mathbf{R}_k \pmb{\mu}_k^c + \mathbf{t}_k, \quad \mathbf{R}_k^{\mathrm{tot}} = \mathbf{R}_k \mathbf{R}_k^c$$

**Alpha合成**：对深度排序后的高斯原语进行前向alpha合成，得到最终像素颜色：

$$\mathbf{I}(x,y) = \sum_{k \in \mathcal{N}(x,y)} \mathbf{C}_k \alpha_k' \prod_{j < k} (1 - \alpha_j')$$

其中 $\mathcal{N}(x,y)$ 为与像素 $(x,y)$ 重叠的有序高斯集合。

### 神经特征调制器（NFM）

NFM基于局部运动学自适应调节每个高斯原语的色彩与不透明度，使渲染结果突出运动关键区域（Section 3.2, Figure 2）。消融实验表明，移除NFM后NTU-60 48/12划分准确率从64.72%降至61.09%（-3.63%），验证了运动感知着色的关键作用（Table 7）。NFM内部采用单层GRU进行时序建模，相比LSTM提升0.22-0.83%，相比RNN提升0.08-1.20%，兼顾性能与效率（Table 10）。

### 端到端可微架构

整个架构——从骨架输入经渲染、视觉编码到语言生成——完全可微。设 $\Theta_{\mathrm{render}}$ 为DrAction渲染器参数，$\Theta_{\mathrm{proj}}$ 为投影层参数，MLLM的任务特定梯度可反向传播至渲染过程，端到端地学习出对下游任务最具区分力的视觉表征（Section 3.3）。

## 实验与分析

### 主实验结果：开词汇动作识别

SkeletonLLM 在 NTU-60 和 NTU-120 两个基准上，对所有开词汇（open-vocabulary）划分均取得最优结果，且优势随数据稀缺程度放大而显著增强。Table 1 汇总了各方法的 Top-1 准确率。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/003_Table_1.jpg]]
*Table 1: Top-1 accuracy (%) of various methods on NTU-60 and NTU-120. Each split is denoted as X/Y, where X is the number of seen classes and Y is the number of unseen classes. The best results are in red, and the second-best are blue. †Results for Qwen2.5-VL-7B and InternVL3-8B were obtained by rendering skeletons with the non-learnable 3D+Velocity renderer (same as in Table 7; 448×448) and finetuning on MQA for 6 epochs*

在 NTU-60 的 55/5 划分（55 类可见，5 类不可见）上，SkeletonLLM 达到 **87.37%**，超越此前最优的特征-文本对齐方法 **TDSM**（Do & Kim, ICCV 2025）的 85.41%（+1.96%）。在 48/12 划分上，SkeletonLLM 达到 **64.72%**，领先第二名 TDSM 的 61.54%（+3.18%）。当数据稀缺度进一步加剧至 **30/30 极端少样本划分**时，SkeletonLLM 取得 **37.84%**，相较 TDSM 的 25.88% 提升 **+11.96%**——这一接近 12 个百分点的绝对增益，是整张表中最大的单项提升，直接验证了可微渲染与因果推理蒸馏在数据匮乏场景下的核心价值。

在更大规模的 NTU-120 数据集上，趋势一致：SkeletonLLM 在 110/10 划分上达到 81.30%（+4.55% vs. TDSM），在 60/60 划分上达到 **34.94%**（+7.73% vs. TDSM）。值得注意的是，在 60/60 这一最具挑战性的均衡划分中，传统对齐方法 **PURLS**（Zhu et al., CVPR 2024）和 **SCoPLe**（Zhu et al., CVPR 2025）分别仅取得 22.97% 和 26.09%，而基于 LLM 的运动理解方法 **MotionGPT**（Jiang et al., NeurIPS 2023）和 **MotionLLM**（Chen et al., TPAMI 2025）也仅达到 20.56% 和 27.21%。SkeletonLLM 以 34.94% 的成绩显著拉开差距，表明“渲染为图像序列 + MLLM 原生视觉理解”的范式在语义空间覆盖上远超“骨架编码 + 文本对齐”或“离散运动词元 + LLM”的方案。

为保证公平性，对照组 MLLM（Qwen2.5-VL-7B、InternVL3-8B）均采用完全相同的非可微 3D+Velocity 固定渲染、12 帧输入、448×448 分辨率，并在 MQA 任务上微调 6 个 epoch。SkeletonLLM 的增益并非来自更强的基座模型，而是源于 DrAction 可微渲染和协同训练策略。

### 跨格式泛化与多任务能力

SkeletonLLM 的核心设计目标之一是格式无关性。Table 2 展示了跨格式传输动作识别的结果：模型在源数据集上训练后，不经任何微调直接在目标数据集上评估。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/006_Table_2.jpg]]
*Table 2: Cross-format transfer accuracy (%) for action recognition. Models are trained on the source dataset and evaluated directly on the target without finetuning*

在 **NTU-60（Kinect v2, 25 关节）→ NW-UCLA（Kinect v1, 20 关节）** 的跨格式传输中，SkeletonLLM 达到 **27.33%**，而此前最佳的跨格式方法 **SKI-LVLM** 仅取得 10.14%——绝对提升 **+17.19%**。在 **HumanML3D（MoCap, 22 关节）→ NW-UCLA** 的传输中，SkeletonLLM 更是达到 **38.13%**（+27.99% vs. SKI-LVLM）。这两个结果强有力地证明：DrAction 的可微渲染成功将异构骨架拓扑“翻译”为统一的视觉语言，使 MLLM 的预训练视觉理解能力得以跨格式复用，而无需为每种骨架格式定制编码器。

Table 3 进一步展示了跨格式运动描述（motion captioning）的能力：模型仅在 NTU-60 上以识别监督训练，直接在 HumanML3D（SMPL, 22 关节）上评估描述质量。SkeletonLLM 在 BLEU-4、ROUGE-L、CIDEr 等指标上均超越专用基线，验证了渲染表征对生成任务的迁移性。

Table 4 报告了单模型多任务评估：使用同一个 NTU-60（55/5）检查点，不经任务特定重训练，SkeletonLLM 在动作识别、运动描述、时序定位等多个任务上均表现出一致竞争力，体现了框架的任务通用性。

### 消融实验：渲染方法对比

Table 7 系统对比了不同渲染方法对性能的影响。在 NTU-60 48/12 划分上，三种固定（非可微）渲染器——3D+Velocity、2D 投影、JTM——分别取得 61.09%、57.24%、58.03%。DrAction（不含 NFM）将准确率提升至 63.17%，而完整的 **DrAction + NFM** 达到 **64.72%**，相较最佳固定渲染器提升 **+3.63%**。在 NTU-120 60/60 划分上，完整 DrAction 以 34.94% 超越固定渲染的 31.52%，增益 **+3.42%**。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/010_Table_7.jpg]]
*Table 7: Ablation on rendering methods on NTU-60 & NTU-120. Our differentiable DrAction outperforms non-learnable renderers*

Figure 4 和 Figure 6 提供了定性对比：固定渲染器产生的图像或过于通用（3D+Velocity 的彩色骨架棒图）、或信息稀疏（2D 投影）、或感知复杂度高（JTM 的关节轨迹图）。DrAction 学习到的抽象表征更具区分力，而 NFM 则动态突出运动关键区域（如踢腿动作中高亮踢出腿），为 MLLM 提供了信息密度更高的视觉语言。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/011_Figure_4.jpg]]
*Figure 4: Qualitative comparison of rendering methods. Fixed renderers (3D+Velocity, 2D, JTM (Wang et al., 2016b)) produce visualizations that are either generic, information-poor, or perceptually complex. DrAction learns an abstract representation. With the NFM, it dynamically highlights kinematically salient regions (e.g., the kicking leg), producing a more informative visual language for the MLLM. A Video Gallery in the Supplementary Material showcases DrAction-rendered videos*

### 消融实验：渐进式训练策略

Table 8 逐项剥离训练策略的贡献。在 NTU-60 30/30 极端少样本划分上：

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/012_Table_8.jpg]]
*Table 8: Ablation on progressive training strategy on NTU-60 & NTU-120*

- 移除 **判别式微调（Disc-FT）**：准确率从 37.84% 降至 36.29%（**-1.55%**），验证了在易混淆动作对上执行二值判断训练对强化决策边界的有效性。Figure 8 的混淆矩阵直观展示了 SkeletonLLM 如何显著减少视觉相似动作间的混淆。
- 移除 **因果推理蒸馏（CR-Distill）**：准确率从 37.84% 降至 35.90%（**-1.94%**），且对需要结构化推理的任务影响更大。Figure 9 的推理链对比表明，无 CR-Distill 的模型倾向于基于粗略姿态产生幻觉（如将“穿鞋”误判为“捡东西”），而完整模型能准确识别细粒度手足交互并用因果逻辑排除干扰项。
- 同时移除两者：准确率进一步降至 34.35%（**-3.49%**），证明 Disc-FT 和 CR-Distill 存在协同效应——前者提供判别性特征基础，后者赋予结构化推理能力。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/020_Figure_8.jpg]]
*Figure 8: Confusion matrix comparison on the NTU-60 (48/12 split). Left: InternVL3 baseline. Right: SkeletonLLM (Ours). Our method significantly reduces confusion between visually similar actions (highlighted in yellow) and improves accuracy on fine-grained classes (red boxes), demonstrating the effectiveness of Discriminative Finetuning*

### 消融实验：NFM 组件与时序建模

Table 10 对 NFM 内部组件和时序建模策略进行了精细消融。完整 NFM（含深度、速度、关节角度特征，采用 GRU 时序融合）在 NTU-60 48/12 上取得 64.72%。移除深度特征降至 63.85%（-0.87%），移除速度特征降至 63.52%（-1.20%），移除关节角度特征降至 63.89%（-0.83%），三项运动学线索均有正向贡献。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/015_Table_10.jpg]]
*Table 10: Ablation on NFM components and temporal modeling strategies on NTU-60 & NTU-120. We compare different temporal fusion methods (GRU, LSTM, RNN) within the NFM. The full NFM with GRU achieves the best performance across nearly all splits*

在时序建模策略上，GRU 优于 LSTM（提升 0.22-0.83%）和 RNN（提升 0.08-1.20%），单层 GRU 的设计在性能与效率间取得了最优平衡。

### 其他关键消融与效率分析

- **渲染帧数**（Figure 7）：准确率从 4 帧到 10 帧急剧上升，在 12 帧时饱和（59.02%），16 帧仅带来微小增益（59.45%），12 帧为最优效率-精度平衡点。
- **输入分辨率**（Table 13）：448×448 提供最佳折衷；降至 224×224 时性能下降约 5%，揭示了骨架渲染图像的稀疏性对稠密视觉编码效率的制约。
- **渲染效率**（Table 14）：DrAction 受益于 3D Gaussian Splatting 的高效可微光栅化，在 448×448 分辨率下渲染延迟可控。端到端推理延迟分解见 Table 15，GPU 显存占用见 Table 16。
- **CR-Distill 变体**（Table 11）：向教师模型（GPT-4o）提供真实标签并蒸馏包含标签的完整推理链，性能最优。仅蒸馏推理过程而不包含标签，效果次之。
- **跨数据集联合训练**（Table 5）：在 NTU-60（25 关节）和 HumanML3D（22 关节）上共享 DrAction 和 MLLM 联合训练，SkeletonLLM 在两个数据集上均取得增益，验证了统一渲染框架对异构数据源的兼容性。

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/017_Figure_7.jpg]]
*Figure 7: Impact of rendered frame count. Accuracy on NTU-60 increases sharply from 4 to 10 frames and saturates at 12 frames (59.02%). Increasing to 16 frames yields minimal gains (59.45%), making 12 frames the optimal trade-off*

![[assets/figures/papers/paper_list_l1841_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Renderin/figures/007_Table_5.jpg]]
*Table 5: Cross-dataset joint training. NTU-60 (25J) + HumanML3D (22J) with shared DrAction and MLLM*

### 失败模式与局限性

尽管 SkeletonLLM 在各项基准上表现优异，分析揭示了以下局限：

1. **长时序列建模不足**：当前评估聚焦于短时间尺度的原子动作，对包含多个子动作和长程时间依赖的真实分钟级序列处理能力有限。这需要分层时序建模和高效的记忆机制，是未来工作的重要方向。

2. **稀疏渲染的效率瓶颈**：骨架渲染图像本质稀疏——大部分背景像素不携带运动信息，但当前稠密视觉编码器对所有像素等权处理。分辨率降至 224×224 时约 5% 的性能下降（Table 13）表明，稀疏注意力或混合表征可能是更高效的替代方案。

3. **极端噪声与未知拓扑的鲁棒性**：尽管 DrAction 对已知格式具备强泛化性，但对极端噪声、大量缺失关节或完全未知拓扑的情况，鲁棒性尚待系统验证。此外，训练仍依赖一定量的标签或教师生成数据，在完全无监督场景下的表现尚未评估。

4. **外部闭源 MLLM 的零样本局限性**（Table 6）：将 DrAction 渲染结果直接输入外部闭源 MLLM（如 GPT-4V）进行零样本识别，性能远低于联合训练。这表明端到端梯度回传对学习任务最优视觉表征至关重要，单纯的“渲染-输入”管线无法替代联合优化。

## 方法谱系与知识库定位

### 1. 问题域定位与核心瓶颈

SkeletonLLM 面向的核心问题是**通用骨架理解**（universal skeleton understanding），即让单一模型在无需针对特定骨架格式重新设计编码器的情况下，处理来自不同传感器（Kinect v1/v2、MoCap、2D姿态估计等）的异构骨架数据，并执行动作识别、运动描述、推理问答等多种下游任务。

该问题的现实瓶颈在于：多模态大语言模型（MLLM）具备强大的视觉推理和语言理解能力，但**无法原生处理结构化的骨架坐标数据**。现有主流方案试图通过两种路径弥合这一模态鸿沟：

- **特征-文本对齐**（如 **PURLS** (Zhu et al., CVPR 2024)、**TDSM** (Do & Kim, ICCV 2025)、**SCoPLe** (Zhu et al., CVPR 2025)）：将骨架序列编码为单一特征向量，与文本嵌入进行对比对齐。这类方法存在严重的表示瓶颈——将整个运动序列压缩为一个固定维度的向量，不可避免地丢失细粒度的时空运动信息；同时，编码器设计深度耦合于特定骨架拓扑，无法跨格式泛化。

- **VQ-VAE离散词元化**（如 **MotionGPT** (Jiang et al., NeurIPS 2023)、**MotionLLM** (Chen et al., TPAMI 2025)）：将连续运动序列量化为离散的运动词元，输入语言模型处理。该方法同样面临格式依赖问题（不同骨架格式需要分别训练词元化器），且离散化过程进一步压缩了运动细节。

SkeletonLLM 的核心洞察是：**将骨架序列“翻译”为MLLM原生的视觉模态（紧凑的图像序列），是打破格式孤岛和语义鸿沟的关键**。这一思路跳出了为每种骨架格式定制编码器的范式，转而利用MLLM预训练中积累的视觉理解能力。

### 2. 方法谱系中的位置

SkeletonLLM 在方法谱系中占据一个独特位置——它既不同于传统的特征-文本对齐范式，也不同于离散词元化路线，而是开创了**可微渲染驱动的视觉模态桥接**这一新范式。其关键区别体现在三个维度的设计选择上：

| 设计维度 | 传统方案 | SkeletonLLM |
|---------|---------|-------------|
| 输入模态 | 直接骨架坐标编码或离散运动词元 | 将骨架渲染为图像序列作为MLLM输入 |
| 渲染器类型 | 固定、非可微渲染（3D+Velocity、2D投影、JTM） | 可微、格式无关的DrAction渲染器（3D Gaussian Splatting + LBS + NFM） |
| 训练策略 | 单阶段MQA分类微调 | 四阶段协同训练（Alignment Warm-up → Disc-FT → CR-Distill → Recognition Refinement） |

**与MLLM微调基线的对比**：直接使用固定渲染器（如3D+Velocity）将骨架渲染为图像，再对MLLM进行微调（如 **Qwen2.5-VL-7B**、**InternVL3-8B** (Zhu et al., 2025b)），是最直观的基线方案。但固定渲染器无法根据下游任务优化视觉表征——渲染出的图像可能包含大量对任务无用的背景像素，或未能突出运动关键区域。SkeletonLLM 通过可微渲染使MLLM的梯度反向传播至渲染过程，学习出任务最优的视觉表征。

**与端到端动作识别方法的对比**：传统的骨架动作识别方法（如ST-GCN系列）依赖图卷积网络直接在骨架图上建模时空关系，虽然精度高，但完全不具备跨格式泛化能力和语言交互能力。SkeletonLLM 牺牲了部分闭集识别精度（在NTU-60 55/5划分上87.37% vs. 专用方法的90%+），换取了开词汇识别、跨格式迁移和自然语言交互的能力。

### 3. 适用边界与局限

**已知适用边界**：

1. **短时间尺度原子动作**：当前评估集中于NTU-60/120、PKU-MMD等数据集中的原子动作（通常持续数秒）。对于包含多个子动作和长时依赖的真实分钟级序列，模型处理能力有限，需要分层时序建模和高效的记忆机制。

2. **已知骨架格式**：尽管DrAction对已知格式（Kinect v1/v2、MoCap、2D姿态估计）具备强泛化性，但对极端噪声、大量缺失关节或完全未知拓扑的情况，鲁棒性尚待验证。

3. **数据依赖性**：训练过程仍依赖一定量的标签数据或教师模型（GPT-4o）生成的推理链，并非完全无监督方案。

**已知性能退化条件**：

- 渲染分辨率降至224×224时，性能下降约5%（Table 13），表明视觉令牌的质量对MLLM理解至关重要。
- 骨架渲染图像本质稀疏——大部分背景像素不包含信息，当前稠密视觉编码方式效率不高。
- 移除神经特征调制器（NFM）后，NTU-60 48/12准确率从64.72%降至61.09%（-3.63%），说明运动感知着色对性能有显著贡献。
- 移除因果推理蒸馏（CR-Distill）后，NTU-60 30/30准确率从37.84%降至35.90%（-1.94%），且对需要推理的任务影响更大。

### 4. 开放问题

基于上述分析，SkeletonLLM 框架留下了若干值得探索的开放问题：

1. **鲁棒性边界**：在面对现实含大量遮挡、噪声和缺失关节的骨架数据时，DrAction 的可微渲染能否稳定保持有效视觉表征？当前实验仅在受控数据集上进行，缺乏对退化输入的系统评估。

2. **计算效率**：端到端梯度回传（尤其是MLLM大模型的反向传播）带来的显存和计算开销能否进一步优化？当前训练需2块NVIDIA H20 GPU，限制了更大规模训练的可能性。稀疏注意力或混合表征可能是缓解骨架渲染图像稀疏性问题的方向。

3. **模态扩展**：DrAction 框架的核心思想——将结构化非视觉数据通过可微渲染转化为MLLM可理解的视觉表征——能否顺利扩展到其他传感模态？例如LiDAR点云、物体轨迹等，实现通用传感数据的MLLM理解。

4. **长程时序建模**：如何有效建模包含多个子动作与长程时间依赖的复杂行为序列？是否需要引入层次化时间抽象或记忆模块？当前12帧的渲染策略对分钟级序列显然不足。

5. **完全无监督/弱监督学习**：当前框架在CR-Distill阶段依赖GPT-4o教师模型生成推理链，在Disc-FT阶段需要标签信息挖掘易混淆动作对。能否通过自监督或弱监督方式进一步减少对人工标注和强教师模型的依赖，是走向真正通用骨架理解的关键一步。

## 原文 PDF

![[paperPDFs/arxiv_2026/SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs.pdf]]
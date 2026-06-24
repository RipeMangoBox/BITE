---
title: 3D-Aware Implicit Motion Control for View-Adaptive Human Video Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/3D_Aware_Implicit_Motion_Control_for_View_Adaptive_Human_Video_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Fang_3D-Aware_Implicit_Motion_Control_for_View-Adaptive_Human_Video_Generation_CVPR_2026_paper.html
project_link: https://hjrphoebus.github.io/3DiMo
code_link: null
aliases:
- 3AIMCVAHVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 联合训练隐式运动编码器与预训练视频生成器，从2D驾驶帧中提取视角无关的紧凑运动令牌，并通过交叉注意力进行语义级条件注入，从而激发生成器的内禀3D空间理解。
primary_logic: 通过压缩为1D令牌丢弃空间布局，结合多视角、相机运动等视图丰富数据监督，强制模型从2D投影中学习本质的3D空间运动表示，并利用退火的辅助几何监督进行初始化。
claims:
- 我们的方法在LPIPS、FID、FVD上全面超越所有基线（Table 1）
- 消融实验证实移除视图丰富数据或辅助几何监督会严重损害性能，且交叉注意力和双手编码器至关重要（Table 2, Figure 5）
- custom test set (view-rich data) 上 LPIPS = 0.221
- custom test set (view-rich data) 上 FID = 36.92
---

# 3D-Aware Implicit Motion Control for View-Adaptive Human Video Generation

> [!tip] 核心洞察
> 通过压缩为1D令牌丢弃空间布局，结合多视角、相机运动等视图丰富数据监督，强制模型从2D投影中学习本质的3D空间运动表示，并利用退火的辅助几何监督进行初始化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视角自适应人体视频生成的3D感知隐式运动控制 |
| 英文题名 | 3D-Aware Implicit Motion Control for View-Adaptive Human Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Fang_3D-Aware_Implicit_Motion_Control_for_View-Adaptive_Human_Video_Generation_CVPR_2026_paper.html) · [Project](https://hjrphoebus.github.io/3DiMo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | 3DiMo |
| Dataset | custom test set, User Study, same-view reconstruction |

> [!tip] 效果简介
> - custom test set (view-rich data) 上，LPIPS 0.221 vs best baseline not reported (优于所有基线)；FID 36.92 vs best baseline not reported (优于所有基线)；FVD 297.4 vs best baseline not reported (优于所有基线)。
> - User Study 上，MOS naturalness 4.18 vs best baseline not reported (最高)；MOS overall 4.38 vs best baseline not reported (最高)。
> - same-view reconstruction (ablation setting) 上，SSIM 0.739。

## 概述

**问题瓶颈**：现有视频驱动人体动画方法普遍依赖显式3D参数模型（如SMPL）或2D姿态图作为运动约束。这类强约束存在两个根本缺陷：其一，从单目视频估计的SMPL参数本身携带深度模糊与姿态不准确，这些误差会被直接注入生成过程；其二，像素对齐的投影式条件注入方式会覆盖大规模视频生成模型内部已蕴含的3D空间先验，导致运动表达受限，且天然无法支持自由视角生成。

**核心方法**：3DiMo（3D-Aware Implicit Motion Control）将运动控制重新定义为3D感知任务——从2D驾驶帧中恢复底层3D运动，同时支持文本驱动的灵活相机控制。其关键设计是一条因果链路：联合训练一个隐式运动编码器与预训练的DiT视频生成器，编码器将驾驶帧压缩为视角无关的紧凑1D运动令牌，通过交叉注意力进行语义级条件注入，从而激发生成器的内禀3D空间理解能力。这一设计使得模型不再依赖外部3D估计器，而是从多视角、相机运动等视图丰富数据中自主学习本质的3D空间运动表示。

**方法谱系与知识库定位**：在现有方法中，**Animate Anyone**（Li Hu et al., CVPR 2024）和**MimicMotion**（Yuang Zhang et al., arXiv 2024）采用2D姿态图引导，缺乏3D感知；**Champ**（Shenhao Zhu et al., ECCV 2024）与**Uni3C**（Chenjie Cao et al., arXiv 2025）引入SMPL参数，但受制于显式模型的深度模糊；**MTVCrafter**（Yanbo Ding et al., arXiv 2025）使用4D运动令牌化，**X-Nemo**（Xiaochen Zhao et al., arXiv 2025）与**X-UniMotion**（Guoxian Song et al., arXiv 2025）探索隐式运动潜变量，但均局限于2D空间。3DiMo的差异化在于：以压缩为1D令牌的方式主动丢弃空间布局，结合视图丰富数据监督与退火式辅助几何监督，首次在隐式运动框架中实现视角自适应的3D感知运动控制。

**主要结果**：在包含多视角与移动相机视频的自建测试集上，3DiMo在LPIPS（0.221）、FID（36.92）、FVD（297.4）三项指标上全面超越所有基线方法。用户研究中，自然度MOS达4.18，综合MOS达4.38，均为最高。消融实验证实，移除视图丰富数据监督会损害相机控制能力，去除早期辅助几何监督则导致训练不稳定与运动控制崩溃，交叉注意力注入与双手运动编码器对运动质量均有决定性贡献。

## 背景与动机

### 2D人体视频生成中的运动控制困境

人体视频生成旨在根据给定的参考图像和运动信号合成逼真的人物视频，在虚拟主播、数字人驱动、影视内容制作等领域具有广泛的应用前景。近年来，大规模视频生成模型（如Kling AI、Midjourney等）取得了长足进步，展现出强大的视觉合成能力。然而，如何精确地控制生成人物的运动，尤其是支持自由视角下的3D空间运动复现，仍然是该领域的核心挑战。

### 现有方法的瓶颈：显式3D约束的局限性

当前主流的人体运动控制方法普遍依赖显式的3D参数模型作为强约束。例如，**Animate Anyone**（Li Hu et al., CVPR 2024）和**MimicMotion**（Yuang Zhang et al., arXiv 2024）采用2D姿态图进行引导；**Champ**（Shenhao Zhu et al., ECCV 2024）和**Uni3C**（Chenjie Cao et al., arXiv 2025）则直接使用SMPL参数模型提供3D先验。这些方法存在两个根本性问题：

1. **深度模糊与不准确的动态**：SMPL等参数模型本身存在固有的深度歧义，其估计的姿态参数往往不够精确。当这些不准确的3D约束被注入到预训练视频生成器时，会覆盖模型自身在大规模数据上习得的内在3D先验，导致生成结果出现姿态错误和运动不自然。

2. **运动表达受限**：显式参数模型的表达能力受限于其预定义的参数空间，难以捕捉服装变形、头发飘动等细粒度动态。更关键的是，这类方法通常局限于单一视角的重建任务，无法支持自由视角生成——即从任意相机角度观察同一段3D运动。

近期的一些工作尝试突破上述限制：**X-Nemo**（Xiaochen Zhao et al., arXiv 2025）和**X-UniMotion**（Guoxian Song et al., arXiv 2025）探索了隐式运动潜变量的使用，但仍局限于2D空间；**MTVCrafter**（Yanbo Ding et al., arXiv 2025）采用4D运动令牌化，但依然依赖显式的时空表示。这些方法均未从根本上解决从2D投影中恢复本质3D运动并支持视角控制的问题。

### 本文动机：从2D投影中学习3D感知的运动表示

本文的核心动机源于一个关键观察：**大规模视频生成模型在预训练过程中已经隐式地习得了丰富的3D空间理解能力**，而现有方法通过强加外部3D约束反而抑制了这种内在先验。因此，本工作提出了一种全新的范式——**3D感知的隐式运动控制（3D-Aware Implicit Motion Control）**，其核心思想是：

- 将人体运动控制重新定义为一个3D感知任务：从2D驾驶帧中恢复底层的3D空间运动，同时自然地支持灵活的文本驱动相机控制。
- 通过端到端地联合训练一个视角无关的隐式运动编码器与预训练的DiT视频生成器，激发生成器自身的内禀3D空间理解能力，而非用外部参数模型去覆盖它。

这一范式的关键在于**不依赖显式的3D参数模型作为中间表示**，而是让模型直接从多视角、多相机运动的视频数据中学习本质的3D运动表征，从而在保持生成质量的同时实现灵活的自由视角控制。

## 核心创新

3DiMo 的根本创新在于**将人体视频生成中的运动控制从“显式几何拟合”转向“隐式3D感知生成”**。现有方法（如 **Champ** (Zhu et al., ECCV 2024)、**Uni3C** (Cao et al., arXiv 2025)）依赖 SMPL 等显式参数模型作为运动条件，但这类模型固有的深度模糊性和姿态估计误差会直接覆盖预训练视频生成模型内部已蕴含的丰富 3D 先验，导致生成结果的运动自然度受限，且无法支持自由视角控制。3DiMo 的核心洞察是：大规模视频生成模型本身已在海量数据中习得了强大的 3D 空间理解能力，关键不在于“告诉”模型精确的 3D 坐标，而在于用恰当的语义信号“唤醒”这种内禀能力。

围绕这一洞察，3DiMo 在四个关键维度上实现了范式转变：

### 从显式空间约束到隐式语义令牌

运动表示是方法差异的核心。现有方法使用 SMPL 参数或 2D 姿态图作为运动条件，这些表示包含精确的空间布局信息，但也因此与特定视角和人体形状强绑定。3DiMo 的运动编码器被设计为 **Transformer-based 1D 分词器**，将驾驶视频帧压缩为 K=5 个可学习的隐令牌，在此过程中**主动丢弃空间布局信息**，迫使模型提炼出与视角无关的语义级运动抽象。这一设计的因果逻辑是：空间信息的缺失反而成为约束——模型无法通过简单的像素对齐来匹配运动，必须调用其内部的 3D 理解来“解释”这些紧凑令牌的含义。

### 从像素对齐注入到语义交叉注意力

条件注入方式的改变是实现上述运动表示的关键配套。基线方法通常采用基于投影的像素对齐或通道拼接，这些方式天然要求运动条件与生成帧之间存在空间对应关系。3DiMo 采用**交叉注意力机制**，仅让视频令牌关注运动令牌，而运动令牌不关注视频令牌。这种非对称设计使得运动条件从“空间约束”变为“语义引导”，生成器可以自由地根据参考图像的外观和指定的相机视角来“演绎”运动，而非机械地复制。消融实验证实，将交叉注意力替换为通道拼接会严重降低运动控制能力（Figure 5）。

### 从单视角重建到视图丰富监督

训练监督范式的转变是实现 3D 感知的关键。传统方法仅在相同视角下进行重建监督，模型可以“作弊”——通过记忆 2D 表观模式而非学习 3D 运动来降低损失。3DiMo 引入**视图丰富数据监督**，混合单视角、多视角及移动相机视频，要求模型在跨视角条件下复现运动。这一设计建立了因果瓶颈：模型无法依赖视角特定的视觉线索，必须从 2D 投影中推断本质的 3D 空间运动。消融实验表明，移除任何一类视图丰富数据都会损害相机控制能力（Table 2, Figure 5）。

### 从持续几何依赖到退火辅助监督

对显式几何先验的处理体现了“借力而不依赖”的策略。纯隐式运动学习在训练早期面临冷启动困难，3DiMo 引入轻量 MLP 几何解码器，从运动令牌预测 SMPL/MANO 姿态参数作为辅助监督。但关键创新在于**损失权重逐步退火至零**——几何监督仅在训练早期提供初始化引导，随后完全移除，让模型在后期自由探索超越 SMPL 表达能力的运动空间。消融实验证实，移除这一辅助监督会导致训练不稳定和运动控制崩溃；而持续保留则会限制运动表达的丰富性。

## 整体框架

3DiMo 将人体运动控制重新定义为一项 **3D 感知任务**：从 2D 驾驶视频中恢复底层 3D 运动，同时原生支持灵活的文本驱动相机控制。为实现这一目标，框架采用端到端联合训练范式，将视角无关的隐式运动编码器与预训练的 DiT 视频生成器深度耦合，从而激发生成器内禀的 3D 空间理解能力。

### 核心数据流与模块拓扑

整体 pipeline 由三个关键模块串联构成，信息流从参考外观与运动线索的分离开始，经语义级条件注入，最终汇聚为视角可控的视频输出。

**输入层** 接收两类信号：
- **参考图像** $I_R$：提供目标人物的外观特征（服装、身份等），经 VAE 编码后作为生成器的视觉锚点。
- **驾驶视频** $V_D = \{ I_D^t \}_{t=0}^T$：提供运动线索的帧序列，仅用于提取运动语义，其空间布局和视角信息被有意丢弃。

**运动编码器（Motion Encoder）** 是整个框架的核心创新载体。它被设计为基于 Transformer 的 **1D 分词器**（tokenizer），而非传统的 2D 空间编码结构。具体地，每帧驾驶图像被 patchify 为视觉令牌后，与 $K=5$ 个可学习的隐令牌（latent tokens）拼接送入 Transformer。最终仅保留这 $K$ 个隐令牌的输出，迫使模型将时序运动信息压缩为紧凑的 1D 表示，从而实现空间布局的显式剥离。为捕获多尺度运动细节，框架采用 **双编码器设计**：身体编码器 $\mathcal{E}_b$ 负责粗粒度躯干运动，手部编码器 $\mathcal{E}_h$ 负责精细手势，两者的输出令牌拼接为统一的运动表示 $\mathbf{z} = [\mathbf{z}_b; \mathbf{z}_h]$。此外，在编码前对驾驶帧施加 **随机透视变换**（perspective augmentation），进一步增强视角无关性。

**条件注入层** 采用 **交叉注意力（cross-attention）** 机制，而非传统的通道拼接或投影对齐。在 DiT 生成器的每一层完整自注意力之后，追加一个交叉注意力层，使视频令牌单向关注运动令牌 $\mathbf{z}$。这种语义级注入方式避免了刚性空间对齐的约束，赋予生成器更大的灵活性来协调外观与运动。

**辅助几何解码器（Auxiliary Geometric Decoder）** 是一个轻量级 MLP，仅在训练早期激活。它从运动令牌 $\mathbf{z}$ 预测 SMPL/MANO 姿态参数 $\theta = [\theta_b; \theta_h]$，提供显式 3D 几何监督以稳定训练初期的运动表征学习。该监督的损失权重随训练推进逐步退火至零，最终完全移除，确保模型不被参数模型的深度模糊和不准确性所束缚。

### 训练策略的三阶段递进

训练流程分为三个阶段，逐步施加更强的 3D 感知约束：
1. **第一阶段**：基础运动编码训练，辅以几何监督。
2. **第二阶段**：引入 **视图丰富数据监督（view-rich data supervision）**，包括单视角、多视角及移动相机视频。模型被要求在同一视角重建和跨视角运动复现两种任务上同时优化，强制从 2D 投影中学习本质的 3D 空间运动表示。
3. **第三阶段**：完全移除辅助几何监督，仅依靠视图丰富数据与生成目标进行端到端精炼。

这种“先引导、后释放”的策略是 3DiMo 成功的关键因果机制：早期几何监督提供收敛锚点，避免隐式表示学习陷入退化；后期释放则允许模型超越 SMPL 的表达上限，真正利用大规模视频生成模型的内在 3D 先验。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_3D_Aware_Implicit/figures/002_Figure_2.jpg]]
*Figure 2: Overview of 3DiMo. Our framework consists of end-to-end trained motion encoders—*

## 核心模块与公式推导

### 3.1 问题形式化

给定一张参考图像 $I_R$ 和一段驾驶视频 $V_D = \{ I_D^t \}_{t=0}^T$，3DiMo 的目标是生成一段目标视频，该视频在保持 $I_R$ 外观特征的同时，复现 $V_D$ 中蕴含的 3D 空间运动，并支持文本引导的相机视角控制。

### 3.2 运动编码器：视角无关的 1D 运动令牌提取

运动编码器是 3DiMo 的核心创新模块。与依赖显式 SMPL 参数或 2D 姿态图的方法不同，该模块被设计为一个基于 Transformer 的 1D 分词器（tokenizer）。其关键设计在于**主动丢弃空间布局信息**：每帧驾驶图像被划分为视觉令牌（visual tokens）后，与 $K=5$ 个可学习的隐令牌（latent tokens）拼接送入 Transformer，最终仅保留这 $K$ 个隐令牌作为输出。通过将空间维度压缩为一维，编码器被迫从 2D 投影中提取语义层面的运动本质，而非像素对齐的空间对应关系，从而天然具备视角无关性。

为进一步强化这一特性，在运动编码前对驾驶帧施加**随机透视变换（Perspective Augmentation）**，迫使模型在训练过程中学习对视角变化鲁棒的运动表征。

### 3.3 双尺度运动编码：身体与手部解耦

精细的手部运动控制是人体视频生成的难点。3DiMo 采用双编码器架构：

- **身体编码器** $\mathcal{E}_b$：捕获躯干与肢体的粗粒度运动；
- **手部编码器** $\mathcal{E}_h$：专注于手指级别的精细手势。

两个编码器独立提取各自的运动令牌后，进行拼接得到统一的运动表征：

$$
\mathbf{z} = [\mathbf{z}_b; \mathbf{z}_h]
$$

这种解耦设计使模型能够同时保持整体动作的连贯性与手部细节的准确性。消融实验证实，移除手部编码器会导致精细手部运动丧失。

### 3.4 交叉注意力条件注入

运动令牌 $\mathbf{z}$ 通过交叉注意力（cross-attention）注入预训练的 DiT 视频生成器。具体而言，在每个 DiT 块的全自注意力层之后追加一个交叉注意力层，其中视频令牌作为 Query 关注运动令牌。这种语义级条件注入方式替代了传统方法中基于投影的像素对齐或通道拼接，赋予生成器更大的灵活性来利用其内禀的 3D 空间先验。消融实验表明，用通道拼接替代交叉注意力会严重降低运动控制能力。

### 3.5 辅助几何监督与退火策略

为在训练早期提供稳定的几何引导，3DiMo 引入一个轻量级 MLP 几何解码器 $D_g$，从运动令牌 $\mathbf{z}$ 预测 SMPL/MANO 姿态参数：

$$
\theta = [\theta_b; \theta_h]
$$

该辅助监督仅在**第一阶段及第二阶段的早期**生效，其损失权重随训练推进逐步退火至零，并在第二阶段剩余步骤及整个第三阶段完全移除。这种“脚手架”式策略既避免了显式参数模型对生成器内在 3D 先验的持续压制，又确保了早期训练的稳定性。移除该辅助监督会导致训练不稳定和运动控制崩溃。

## 实验与分析

### 定量评估与用户研究

3DiMo在自建视图丰富测试集上与七类代表性基线进行了系统比较，涵盖2D姿态引导（**Animate Anyone**，Li Hu et al., CVPR 2024；**MimicMotion**，Yuang Zhang et al., arXiv 2024）、显式3D参数模型（**Champ**，Shenhao Zhu et al., ECCV 2024；**Uni3C**，Chenjie Cao et al., arXiv 2025）、4D运动令牌化（**MTVCrafter**，Yanbo Ding et al., arXiv 2025）以及隐式2D运动潜变量（**X-Nemo**，Xiaochen Zhao et al., arXiv 2025；**X-UniMotion**，Guoxian Song et al., arXiv 2025）等方法。

如表1所示，3DiMo在所有自动化指标上均取得最优：LPIPS达到0.2206，FID为36.92，FVD为297.4，全面超越所有基线方法。值得注意的是，这些指标同时衡量了同一视角重建和跨视角运动复现的综合表现，因此直接反映模型对3D空间运动的理解能力。

用户研究进一步验证了3DiMo的感知优势。在运动准确性（Accuracy，4.28）、运动自然度（Naturalness，4.18）、3D物理合理性（3D Plausibility，4.05）和综合质量（Overall，4.38）四项MOS评分中，3DiMo均以显著优势领先。其中运动自然度和3D物理合理性的领先尤为突出，表明隐式运动表示有效规避了显式参数模型常见的深度模糊和姿态僵硬问题。

### 消融实验

为验证各设计选择的有效性，我们进行了系统的消融实验（表2，图5），核心发现如下：

**运动表示方式**：将隐式运动令牌替换为SMPL姿态系数θ_body作为运动表示后，模型出现典型的深度模糊错误——在侧向或遮挡视角下无法准确还原肢体前后关系。这证实了显式3D参数模型的内在歧义性会阻碍生成器利用其预训练3D先验。

**视图丰富数据监督**：移除任何一类视图丰富数据（多视角视频或移动相机视频）均会损害相机控制能力。仅使用单视角重建监督时，模型无法学习视角无关的运动表示，跨视角运动复现质量显著下降。这一结果直接支撑了论文的核心主张：多视角一致性观察是激发3D空间理解的必要条件。

**辅助几何监督**：在训练早期完全去除辅助几何监督（即SMPL/MANO姿态回归损失）会导致训练不稳定和运动控制崩溃。该监督的退火策略同样关键——若持续施加几何损失，会限制隐式表示的灵活性，使其退化为对SMPL参数的过拟合。

**条件注入方式**：将交叉注意力替换为通道拼接（channel concatenation）后，运动控制能力严重退化。这表明像素对齐的注入方式无法实现语义级运动迁移，交叉注意力机制是实现灵活运动-外观解耦的关键。

**手部运动编码器**：移除手部编码器E_h后，模型丧失精细手部运动控制能力，生成的视频中手指姿态模糊或与驾驶信号不一致。这验证了双尺度编码设计的必要性。

### 可视化分析

图4展示了3DiMo与基线的定性对比。在存在深度歧义的场景中（红色框标注），基于SMPL的基线方法常产生不自然的肢体交叉或前后关系错误，而3DiMo能准确还原空间运动轨迹。在复杂姿态场景下（黄色框标注），2D姿态引导方法因缺乏3D理解而出现关节错位，3DiMo则保持物理一致性。

图5的消融可视化进一步揭示：使用SMPL姿态作为运动表示时，侧视角度下的手臂深度关系完全错误；移除视图丰富数据后，相机旋转时人体朝向与背景不一致；去除辅助几何监督或使用通道拼接时，生成质量急剧下降，运动控制趋于崩溃。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_3D_Aware_Implicit/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation and user study results of MOS with 95% confidence intervals. Top two are noted as first , second*

![[assets/figures/papers/paper_list_l19_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_3D_Aware_Implicit/figures/005_Figure_4.jpg]]
*Figure 4: Visualization comparisons with baselines. Red and yellow bounding boxes highlight depth ambiguities and inaccurate poses, respectively*

![[assets/figures/papers/paper_list_l19_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_3D_Aware_Implicit/figures/006_Table_2.jpg]]
*Table 2: Ablation results. Top two are noted as first , second*

![[assets/figures/papers/paper_list_l19_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_3D_Aware_Implicit/figures/007_Figure_5.jpg]]
*Figure 5: Visualizations of ablation results. Using SMPL poses as motion representation introduces typical depth ambiguity errors. Removing any view-rich data supervision impairs camera control. Removing auxiliary geometric supervision or using channel concatenation causes training instability and quality degradation. Without the hand encoder, fine-grained hand motions are lost*

## 方法谱系与知识库定位

### 1. 方法谱系

3DiMo 处于“基于视频扩散模型的人体运动控制”这一快速演进的谱系中，其核心突破在于将控制信号从**显式几何代理**迁移至**隐式3D感知表示**，从而解决了此前方法中普遍存在的深度模糊与视角绑定问题。

#### 1.1 显式几何控制谱系

此前的主流方法依赖外部估计的显式几何先验作为运动控制信号：

- **2D姿态引导**：**Animate Anyone** (Li Hu et al., CVPR 2024) 与 **MimicMotion** (Yuang Zhang et al., arXiv 2024) 使用2D骨骼关键点或姿态图作为条件，通过投影对齐注入生成器。这类方法受限于2D表示的固有深度歧义——同一2D姿态可对应多种3D空间配置，导致生成的视频在遮挡或复杂旋转场景下出现结构崩溃。

- **3D参数模型引导**：**Champ** (Shenhao Zhu et al., ECCV 2024) 与 **Uni3C** (Chenjie Cao et al., arXiv 2025) 引入SMPL等3D参数模型作为强约束，试图解决深度模糊问题。然而，SMPL估计本身存在不准确性（尤其在遮挡、宽松衣物、手部细节场景），且其显式旋转参数与大规模视频生成模型的内在3D先验存在表征鸿沟——生成器被强制服从一个可能错误的几何模板，而非激活其自身从海量视频中学到的空间理解。

- **4D运动令牌化**：**MTVCrafter** (Yanbo Ding et al., arXiv 2025) 尝试将运动信息压缩为4D令牌，但仍依赖显式3D监督，未能完全释放生成器的内禀3D能力。

#### 1.2 隐式运动表示谱系

与3DiMo更接近的是近期探索隐式运动潜变量的工作：

- **X-Nemo** (Xiaochen Zhao et al., arXiv 2025) 与 **X-UniMotion** (Guoxian Song et al., arXiv 2025) 从2D视频中学习隐式运动潜变量，避免了显式几何代理的误差传播。但这两项工作**仍局限于2D运动空间**——它们学习的是像素平面内的运动模式，无法支持自由视角生成或相机运动控制，本质上未触及3D空间理解。

**3DiMo的关键跃迁**在于：它既继承了隐式表示的灵活性（避免显式代理的误差），又通过**视图丰富数据监督**和**退火辅助几何监督**将隐式空间锚定在3D物理空间中。这使得模型从“2D运动模式匹配”跃迁至“3D空间运动理解”，从而自然支持跨视角运动复现与文本引导的相机控制。

### 2. 知识库定位

#### 2.1 核心贡献与因果机制

3DiMo的知识增量集中在以下因果链条上：

1. **瓶颈识别**：显式3D参数模型（SMPL）的深度模糊与估计误差会**覆盖**大规模视频生成模型的内在3D先验，形成“弱先验指导强模型”的倒挂。

2. **因果调控**：通过联合训练**隐式运动编码器**与**预训练DiT生成器**，从2D驾驶帧中提取视角无关的紧凑运动令牌，并通过**交叉注意力**进行语义级条件注入，从而**激发**（而非覆盖）生成器的内禀3D空间理解。

3. **关键实现机制**：
   - **1D令牌压缩**：将驾驶帧编码为 K=5 个隐令牌 $\mathbf{z}$，**主动丢弃空间布局信息**，强制编码器提取视角无关的语义运动抽象。
   - **交叉注意力注入**：运动令牌通过交叉注意力层作用于DiT生成器的视频令牌，实现语义级条件控制，替代此前基于投影的像素对齐或通道拼接。
   - **退火几何监督**：训练早期使用轻量MLP预测SMPL/MANO姿态参数 $\theta = [\theta_b; \theta_h]$ 作为辅助监督，随后将损失权重逐步退火至零，实现“初始化引导-自主进化”的课程学习。

#### 2.2 适用边界

从消融实验（Table 2, Figure 5）可明确推导出方法的适用条件：

- **视图丰富数据是必要条件**：移除任何一类视图丰富数据（单视角、多视角、移动相机视频）均会损害相机控制能力。这表明模型对多视角一致性观测存在强依赖，在仅含单视角数据的场景下可能无法稳定学习3D感知表示。

- **交叉注意力不可替代**：用通道拼接替代交叉注意力会**严重降低运动控制能力**，说明语义级条件注入（而非空间对齐）是实现3D感知控制的关键设计选择。

- **双手编码器对精细控制至关重要**：省略手部运动编码器会导致精细手部运动丧失，表明身体与手部的双尺度编码是处理人体运动层次结构的有效策略。

- **辅助几何监督的退火时机敏感**：完全移除早期几何监督会导致训练不稳定和运动控制崩溃，但持续使用则会限制隐式表示的自由度。这种“先引导后退火”的策略需要在实践中仔细调参。

#### 2.3 局限与开放问题

基于论文提供的证据，以下局限需要人工验证或进一步研究：

1. **泛化到极端姿态**：论文未明确报告在极端运动（如杂技、快速旋转）或严重遮挡场景下的性能。隐式表示是否能在训练分布外保持3D一致性，仍需验证。

2. **与生成器架构的耦合性**：3DiMo基于预训练DiT生成器设计，其运动编码器与交叉注意力注入策略是否可迁移至其他生成架构（如UNet-based扩散模型）尚不明确。

3. **计算开销**：联合训练运动编码器与视频生成器、处理多视角数据、以及辅助几何解码器的引入，可能带来显著的计算增量，论文未提供与基线的训练/推理效率对比。

4. **视角控制的精度上限**：虽然方法支持文本引导的相机控制，但视角变化的精细度与一致性（如连续环绕旋转时的抖动）未在定量指标中单独评估。

5. **数据依赖性**：视图丰富数据的采集成本（UE渲染、自采多视角）限制了方法的可复现性，论文未讨论使用公开多视角数据集（如Human3.6M）的替代方案。

## 原文 PDF

![[paperPDFs/CVPR_2026/3D_Aware_Implicit_Motion_Control_for_View_Adaptive_Human_Video_Generation.pdf]]
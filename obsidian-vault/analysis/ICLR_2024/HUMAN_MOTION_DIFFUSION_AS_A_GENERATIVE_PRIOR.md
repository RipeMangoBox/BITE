---
title: "HUMAN MOTION DIFFUSION AS A GENERATIVE PRIOR"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/HUMAN_MOTION_DIFFUSION_AS_A_GENERATIVE_PRIOR.pdf
paper_link: "https://openreview.net/forum?id=dTpbEdN9kr"
aliases:
- PDCD
- HMDAGP
tags:
- ICLR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "将预训练的扩散运动生成模型（MDM）作为人体运动流形的强先验，通过三种组合策略（顺序、并行、模型组合）以极低甚至零额外训练代价泛化至分布外任务。"
primary_logic: "冻结或微调的扩散先验可以作为“运动语义锚点”，只需添加轻量的协调机制（握手、通信块、模型混合）便能将短片段、单人、单控制信号的能力组合成长序列、双人交互和细粒度联合控制。"
claims:
- "DoubleTake在BABEL数据集上的FID指标（1.04）优于专为此任务训练的TEACH（1.12）。"
- "ComMDM在3DPW双人前缀完成的用户研究中，在所有三个维度（交互、完整性、整体质量）上均显著优于MRT和原始MDM。"
- "使用DiffusionBlending对LeftWrist+Trajectory的组合控制，FID从MDM inpainting的1.18降至0.22。"
- "BABEL 上 FID (Motion) = 1.04 (DoubleTake)"
---

# HUMAN MOTION DIFFUSION AS A GENERATIVE PRIOR

> [!tip] 核心洞察
> 冻结或微调的扩散先验可以作为“运动语义锚点”，只需添加轻量的协调机制（握手、通信块、模型混合）便能将短片段、单人、单控制信号的能力组合成长序列、双人交互和细粒度联合控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 人体运动扩散作为生成先验 |
| 英文题名 | HUMAN MOTION DIFFUSION AS A GENERATIVE PRIOR |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://openreview.net/pdf?id=dTpbEdN9kr); [GitHub](https://github.com/priorMDM/priorMDM); [Project](https://priormdm.github.io/priorMDM-page/); [paper](https://openreview.net/forum?id=dTpbEdN9kr) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PriorMDM (基于运动扩散先验的组合方法，包括DoubleTake、ComMDM和DiffusionBlending) |
| Dataset | BABEL, HumanML3D (长序列指标), 3DPW (前缀完成 L2), HumanML3D (关节控制) |

> [!tip] 效果简介
> - BABEL 上，FID (Motion) 为 1.04 (DoubleTake)，对比 1.12 (TEACH)，变化 -0.08 (更优)。
> - HumanML3D (长序列指标) 上，FID (Motion) 为 0.60 (DoubleTake)，对比 0.98 (MDM)，变化 -0.38 (更优)。
> - 3DPW (前缀完成 L2) 上，Root Error [m] @3s 为 0.30 (ComMDM)，对比 0.54 (MDM, no Com)，变化 -0.24 (更优)。

## 概述

**核心瓶颈**：高质量标注运动数据的稀缺性严重制约了人体运动生成任务的泛化能力。现有数据集几乎全部由短暂的单人序列构成，导致多人交互、长序列生成和细粒度多关节控制等任务缺乏足够的训练支撑。

**核心思路**：本文提出将预训练的文本到运动扩散模型（MDM, Tevet et al., ICLR 2023）视为人体运动流形的强先验，通过三种推理时或轻量微调的组合策略——**DoubleTake**（顺序组合）、**ComMDM**（并行组合）和**DiffusionBlending**（模型组合）——将短片段、单人、单控制信号的能力泛化至分布外任务，且仅需极少甚至零额外训练代价。

**关键结论**：
- **DoubleTake** 在 BABEL 长序列生成任务上取得 FID 1.04，优于专为此任务训练的 TEACH（1.12）。
- **ComMDM** 在 3DPW 双人前缀完成用户研究中，交互质量、完整性和整体自然度三个维度均显著优于 MRT 和原始 MDM。
- **DiffusionBlending** 对 LeftWrist + Trajectory 组合控制将 FID 从 MDM inpainting 的 1.18 降至 0.22，实现跨关节细粒度复合控制。

**方法定位**：PriorMDM 框架将冻结或微调的扩散先验作为“运动语义锚点”，仅需添加轻量协调机制（握手平均、通信块、模型混合）即可实现三类组合泛化，无需重新训练完整模型。该方法在方法谱系上填补了“以通用运动先验驱动分布外组合生成”的空白，与 TEACH（长序列专有模型）、MRT（多人预测模型）和 MDM inpainting（单一条件修复）形成互补或替代关系。

## 背景与动机

### 问题背景

人体运动生成是计算机视觉与图形学中的核心任务，广泛应用于动画制作、虚拟现实和人机交互等领域。近年来，扩散模型在运动生成上取得了显著进展，其中**MDM**（Tevet et al., ICLR 2023）作为代表性工作，能够根据文本描述生成高质量的单人短序列运动。然而，现有方法面临一个根本性瓶颈：**标注运动数据极度稀缺，且几乎全部为短暂的单人序列**。这导致三个关键任务严重受限——多人交互生成、长序列生成以及精细化运动控制。

### 现有方法缺口

具体而言，当前方法的局限体现在三个维度：

1. **长序列生成**：MDM等模型只能生成固定长度的短片段（通常数秒），无法直接产生任意长度的连贯运动。专有方法如**TEACH**（Athanasiou et al., 3DV 2022）虽尝试解决此问题，但需要专门训练且生成质量有限。

2. **多人交互**：现有数据集极少包含双人交互标注，导致模型无法生成语义合理的多人协作动作。**MRT**（Wang et al., NeurIPS 2021）等多人运动预测方法依赖DCT变换学习前缀完成，但生成结果容易冻结在前缀姿态上，缺乏生动的交互语义。

3. **细粒度控制**：MDM原生的运动修复（inpainting）功能仅支持单一条件的硬性修复，无法灵活组合不同关节的控制信号。当需要同时控制左手腕和运动轨迹时，修复方法往往产生脚底滑动、肢体错位等不自然结果。

### 核心动机

本文的核心动机在于：**能否将预训练的扩散运动生成模型作为人体运动流形的强先验，以极低甚至零额外训练代价泛化至上述分布外任务？** 这一思路的洞察在于，冻结或微调的扩散先验可以作为“运动语义锚点”——只需添加轻量的协调机制（握手、通信块、模型混合），便能把短片段、单人、单控制信号的能力组合成长序列、双人交互和细粒度联合控制。

基于此动机，本文提出**PriorMDM**，包含三种互补的组合策略：
- **DoubleTake**：通过顺序组合实现任意长度运动生成
- **ComMDM**：通过并行通信实现双人交互生成
- **DiffusionBlending**：通过模型混合实现多关节联合控制

三种方法均以MDM为统一先验，在保持生成质量的同时大幅降低对标注数据的依赖。

## 核心创新

本文的核心贡献在于提出了一种**以预训练运动扩散模型（MDM）为生成先验的组合范式**，通过三种互补的策略——顺序组合、并行组合和模型组合——将短片段、单人、单控制信号的生成能力泛化至长序列、双人交互和细粒度联合控制，且仅需极低甚至零额外的训练代价。其关键创新体现在以下三个“changed slots”上。

### 1. 长序列生成：从自回归固定前缀到并行握手精修

传统方法（如**TEACH**，Athanasiou et al., 3DV 2022）通常采用自回归方式逐段生成并固定前缀，这容易导致误差累积和动作语义漂移。**DoubleTake** 的核心创新在于将长序列生成转化为一个**两阶段并行批处理过程**：

- **第一阶段（First Take）**：在同一批次中并行生成所有运动区间，并在每一步去噪时对相邻区间的**握手区域**（约1秒长的前缀/后缀）执行帧级平均，公式为 $\tau_i = (1-\vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$，强制保证边界一致性。这打破了传统自回归的串行依赖，使全局上下文得以在一次扩散中协同建模。
- **第二阶段（Second Take）**：将过渡区域及其两侧上下文拼接成“三明治”结构，利用**软遮罩**（从 $\mathbf{M}_{hard}$ 到 $\mathbf{M}_{soft}$ 的线性过渡）对过渡帧进行部分加噪再精修，使动作自然连贯而非简单拼接。

这一设计的关键在于：握手机制提供了局部一致性约束，而软遮罩精修则解决了硬拼接带来的不自然过渡。消融实验证实，加入第二take和软遮罩能显著提升FID和过渡自然度，且握手长度约1秒时效果稳健（Table 2）。

### 2. 双人通信：从独立生成到轻量激活修正

多人运动生成的传统方法（如**MRT**，Wang et al., NeurIPS 2021）或独立生成（MDM零通信基线）难以建模互动语义。**ComMDM** 的创新在于引入了一个**极轻量的通信块**——仅单层Transformer——插入两个冻结的MDM之间：

- 通信块接收两个MDM在某一中间层（实验表明第8层最优）的Transformer激活，输出**相加的修正项** $\Delta O_t^{i,(n)}$，以协调两人的交互行为。
- 同时可选地预测初始根位置差，解决双人空间对齐问题。

这一设计的因果机制在于：冻结的MDM先验保留了强大的单人运动语义，通信块只需学习“如何协调”而非“如何运动”，因此仅需少量双人标注即可泛化。实验表明，ComMDM在3DPW前缀完成任务中将根误差从0.54m降至0.30m（Table 3），且用户研究在交互质量、完整性和整体自然度三个维度上均显著优于MRT和MDM（Fig. 8）。值得注意的是，通信块置于Transformer较高层且层数较少时效果最佳，这暗示高层语义特征更适合跨人物协调。

### 3. 控制信号组合：从单一修复到模型混合

MDM原生的inpainting功能仅支持单一条件的硬性修复，无法灵活组合不同关节的控制信号（如同时控制左手腕和运动轨迹）。**DiffusionBlending** 的创新在于将分类器自由引导思想推广至**任意两个对齐的扩散模型**之间：

- 首先对同一基础MDM在特定关节轨迹上**微调**，训练时对受控特征屏蔽噪声（Algorithm 1），使模型学会生成与给定轨迹一致的全身体运动。
- 采样时按公式 $G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$ 线性混合两个模型的预测，实现跨关节或跨控制类型的复合控制。

这一设计的核心洞察在于：微调后的模型各自成为特定控制信号的“专家”，DiffusionBlending通过缩放因子 $s$ 在两者之间插值，实现了灵活的组合控制。实验表明，微调模型在单一关节控制上FID远低于MDM inpainting（如左腕控制从0.82降至0.34），而DiffusionBlending进一步将组合控制（LeftWrist+Trajectory）的FID从1.18降至0.22（Table 4）——降幅高达0.96，证明了模型混合策略的有效性。

### 创新总结

三种方法的共同本质是：**将预训练扩散先验视为运动流形的“语义锚点”，仅添加轻量的协调机制（握手、通信块、模型混合）即可实现分布外泛化**。这一范式避免了为每个新任务从头训练专用模型，在标注运动数据稀缺的背景下具有显著的实用价值。然而，其动态效果受限于MDM先验的生成质量，且当前方法未显式建模物理接触，可能产生穿模或不自然的接触姿态。

## 整体框架

![[assets/figures/papers/paper_list_l32_https_openreview_net_pdf_id_dTpbEdN9kr/figures/002_Figure_2.jpg]]
*Figure 2: Soft blending overview. We allow b frames long linear masking between $\mathbf { M _ { h a r d } }$ to $\mathbf { M } _ { s \mathbf { o f f } }$ such that during the Second take at every denoising step part of the originally generated motion (suffix or prefix) going through refinement to fit the transition

PriorMDM 并非一个全新的端到端模型，而是一套基于**冻结或微调的运动扩散先验（MDM）**的组合策略框架。其核心思想是：将预训练好的 MDM 视为人体运动流形的强先验，通过三种正交的组合机制——**顺序组合（DoubleTake）**、**并行组合（ComMDM）**和**模型组合（DiffusionBlending）**——以极低甚至零额外训练代价，将原本仅能生成短片段、单人、单控制信号的能力泛化至长序列、双人交互和细粒度联合控制等分布外任务。

### 统一先验：MDM 基础

所有组合方法的基石是 **MDM**（Tevet et al., ICLR 2023），一个基于 DDPM 框架的去噪扩散模型。其前向过程按 $q(X_t | X_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} X_{t-1}, (1-\alpha_t) I)$ 逐步向运动数据添加高斯噪声；反向过程则学习从噪声 $X_t$ 中预测干净运动 $\hat{X}_0$，并以文本条件 $c$（经 CLIP 编码）和噪声步 $t$ 为引导。PriorMDM 的所有扩展均建立在此预训练先验之上，不修改其基础架构。

### 三种组合策略与模块关系

框架的整体输入输出流可概括为：**文本/控制信号 → 组合策略调度 → MDM 先验推理/微调 → 运动序列输出**。三种策略分别对应不同的任务维度和模块调用方式：

**1. 顺序组合：DoubleTake（长序列生成）**

DoubleTake 解决的是“如何用固定长度先验生成任意长运动”的问题。它采用两阶段推理，全程无需额外训练：

- **First Take**：将目标长序列切分为多个区间，在同一批次中并行生成所有区间。每一步去噪时，对相邻区间的前缀/后缀执行**握手平均**（公式 $\tau_i = (1-\vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$），强制边界一致性。
- **Second Take**：将相邻区间的过渡区域及其两侧上下文拼接成“三明治”结构，通过部分加噪和**软遮罩**精修过渡，使动作自然连贯。软遮罩机制在硬遮罩 $\mathbf{M}_{hard}$ 与软遮罩 $\mathbf{M}_{soft}$ 之间线性过渡，允许部分原始生成帧参与精修（Figure 2）。

**2. 并行组合：ComMDM（双人交互生成）**

ComMDM 解决“如何让两个独立先验协作生成双人运动”的问题。架构上，它冻结两个 MDM 实例，仅在指定 Transformer 层后插入一个**单层通信块**（Figure 4）。该通信块接收两个 MDM 在中间层的激活，输出相加的修正项 $\Delta O_t^{i,(n)}$，实现人物间的信息交换；同时可选地预测两人的初始根位置差。训练时仅优化通信块参数，先验完全冻结。

**3. 模型组合：DiffusionBlending（细粒度联合控制）**

DiffusionBlending 解决“如何组合多个控制信号”的问题。先对同一 MDM 基础模型在不同关节轨迹（如左腕、轨迹）上分别微调，训练时屏蔽受控特征的噪声，使各模型学会生成与给定轨迹一致的全身体运动。采样时，将两个对齐的微调模型按缩放系数 $s$ 线性混合：$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$，实现跨关节或跨控制类型的复合控制。该方法本质上是分类器自由引导的扩展，将“条件/无条件”的插值推广到“任意两个对齐扩散模型”的混合。

### 输入输出流总览

| 组合策略 | 输入 | 核心模块 | 输出 | 训练代价 |
|---------|------|---------|------|---------|
| DoubleTake | 多段文本描述 + 目标总时长 | First Take（握手）+ Second Take（软遮罩精修） | 任意长度连贯运动序列 | 零训练 |
| ComMDM | 双人交互文本 | 冻结 MDM × 2 + 单层通信块 | 双人同步运动 | 仅训练通信块 |
| DiffusionBlending | 多关节控制信号（如左腕轨迹 + 根轨迹） | 对齐的微调模型 × 2 + 混合采样器 | 满足复合控制的全身运动 | 分别微调各控制模型 |

三种策略可独立使用，也可视任务需求组合。例如，理论上可将 ComMDM 的通信机制与 DoubleTake 的长序列生成结合，实现双人长交互序列；或将 DiffusionBlending 的混合控制应用于 ComMDM 中的单人模型，实现双人场景下的细粒度关节控制。论文未显式验证这些组合，但框架的模块化设计为此类扩展留有空间。

## 核心模块与公式推导

PriorMDM 的核心思想是将预训练的 MDM（Tevet et al., ICLR 2023）作为冻结的运动先验，通过三种轻量组合策略实现分布外泛化。以下逐一拆解其关键模块与公式。

### 3.1 DoubleTake：时序组合与过渡精修

DoubleTake 解决长序列生成问题，核心机制是两阶段推理。

**第一 Take：批量并行生成与握手约束**

将目标长序列按文本标签切分为 $N$ 个区间，在同一批次中并行去噪。每一步去噪后，对相邻区间的前缀/后缀执行“握手”平均，强制边界一致性：

$$\tau_i = (1 - \vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$$

其中 $\tau_i$ 是第 $i$ 段与第 $i-1$ 段之间的握手帧，$S_{i-1}[-h:]$ 为前段的后 $h$ 帧后缀，$S_i[:h]$ 为后段的前 $h$ 帧前缀，$\vec{\alpha}$ 是从 1 线性递减到 0 的权重向量。这一操作在每次去噪迭代中强制相邻区间在边界处相等，使最终拼接的序列在运动语义上连续。

**第二 Take：软遮罩过渡精修**

将过渡区域及其两侧上下文拼接成“三明治”结构，对其施加 $T'$ 步部分噪声后重新去噪。关键创新是软遮罩机制：定义硬遮罩 $\mathbf{M}_{\text{hard}}$（过渡区域完全加噪）和软遮罩 $\mathbf{M}_{\text{soft}}$（过渡区域保留部分原始生成内容），在 $b$ 帧范围内线性过渡。这使得过渡区域既能被上下文约束精修，又不会完全丢弃第一 Take 生成的运动信息。实验表明，约 1 秒的握手长度和软遮罩设置能显著提升 FID 和过渡自然度（Table 2 消融行）。

### 3.2 ComMDM：并行组合与通信块

ComMDM 解决双人运动生成问题。其核心是在两个冻结的 MDM 之间插入一个可训练的单层 Transformer 通信块。

该通信块接收两个 MDM 在 Transformer 第 $L_n$ 层的激活，输出相加的修正项 $\Delta O_t^{i,(n)}$，使两人的去噪过程相互协调。此外，通信块可选地预测两人的初始根位置差 $D^i$，以处理空间关系的全局一致性。

消融实验（Table 3）表明：通信块置于 MDM 的较高层（第 8 层）且仅使用 1 层时效果最佳——根误差从无通信的 0.54m 降至 0.30m。层数增加反而导致过拟合，因为可训练参数增多而双人标注数据极为稀缺。

### 3.3 微调关节控制器与 DiffusionBlending

**微调策略**

在特定关节轨迹（如左腕、根轨迹）上微调 MDM。训练时，前向扩散过程中对受控特征屏蔽噪声——即保持 ground-truth 轨迹不变，仅对其他关节加噪。这迫使模型学会在给定精确关节约束的条件下生成协调的全身运动。所有微调模型均从同一 MDM 实例初始化，训练 80k 步、batch size 64。

**DiffusionBlending 采样公式**

为实现多控制信号的灵活组合，DiffusionBlending 将 classifier-free guidance 推广到两个对齐的扩散模型之间：

$$G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot \big(G^b(X_t, t, c_b) - G^a(X_t, t, c_a)\big)$$

其中 $G^a$ 和 $G^b$ 是在不同关节控制信号上微调的两个模型，$c_a$ 和 $c_b$ 为对应的控制条件，$s$ 为缩放系数。当 $s=0$ 时退化为仅使用模型 $a$；当 $s=1$ 时完全切换到模型 $b$；中间值实现两种控制信号的混合。实验中使用等权重（$\lambda=0.5$）组合左腕和轨迹控制，FID 从 MDM inpainting 的 1.18 降至 0.22（Table 4），验证了该公式的有效性。

### 3.4 基础扩散框架

所有方法建立在 DDPM 的前向噪声过程之上：

$$q(X_t | X_{t-1}) = \mathcal{N}\big(\sqrt{\alpha_t} X_{t-1}, (1 - \alpha_t) I\big)$$

其中 $X_t$ 为第 $t$ 步加噪后的运动序列，$\alpha_t$ 为噪声调度参数。MDM 建模反向去噪过程，预测干净运动 $\hat{X}_0$，条件为噪声步 $t$ 和 CLIP 编码的文本嵌入。PriorMDM 的所有组合策略均在此去噪框架内操作，不改变基础模型的架构或训练目标。

## 实验与分析

### 核心实验结果

**长序列生成。** DoubleTake在BABEL测试集上取得FID 1.04，优于专为此任务训练的TEACH（1.12），验证了“冻结先验+推理时组合”策略的有效性（Table 1）。在HumanML3D上，DoubleTake的FID从MDM的0.98降至0.60（Table 2），降幅达39%，表明握手与软遮罩精修机制显著提升了长序列的分布匹配质量。

![[assets/figures/papers/paper_list_l32_https_openreview_net_pdf_id_dTpbEdN9kr/figures/009_Table_2.jpg]]
*Table 2: Quantitative results on the HumanML3D [2022] test set. All methods use the real motion length from the ground truth. ‘→’ means results are better if the metric is closer to the real distribution. We run all the evaluations 10 times. Bold indicates best result, ?????????????????? indicates second best result. R-precision reported is top-3, Div. stands for diversity and M.-Dist for Multi-modal distance*

**双人运动生成。** 在3DPW前缀完成任务中，ComMDM在3秒处的根误差仅为0.30 m，而MDM无通信基线为0.54 m（Table 3），误差降低44%。用户研究进一步证实，ComMDM在交互质量、前缀衔接完整性和整体自然度三个维度上均显著优于MRT和原始MDM（Fig. 8）。定性对比显示，MRT倾向于冻结在前缀姿态上，而ComMDM生成的动作生动且语义正确（Fig. 6）。

![[assets/figures/papers/paper_list_l32_https_openreview_net_pdf_id_dTpbEdN9kr/figures/011_Table_3.jpg]]
*Table 3: 3DPW prefix completion L2 error. Given a 1-second long prefix, all models predict a 3-second long motion completion. We report the root error and the joint’s mean error relative to the root for the first 1, 2, and 3 seconds. Bold indicates best result, underline indicates second best. We introduce two ablation studies, the first is for the number of layers constructing ComMDM (ours is 1), and the second is in which layer of MDM it is placed (ours is in the 8th). Observe that the communication block performs better when placed in higher layers of the transformer and constructed from fewer layers*

**细粒度关节控制。** 微调模型在单一关节控制上大幅超越MDM inpainting：轨迹控制FID从0.98降至0.54，左腕控制FID从0.82降至0.34（Table 4）。DiffusionBlending将组合控制推向新高度——LeftWrist+Trajectory的FID从MDM inpainting的1.18骤降至0.22，降幅超80%。定性上，MDM inpainting产生严重脚底滑动和肢体错位，而微调模型生成的行走轨迹与挥杆动作在物理和语义上均与输入特征一致（Fig. 9）。

![[assets/figures/papers/paper_list_l32_https_openreview_net_pdf_id_dTpbEdN9kr/figures/013_Table_4.jpg]]
*Table 4: Joints control with fine-tuned models and DiffusionBlending. We compare our joints control method with the motion inpainting method suggested by Tevet et al. [2023]. We conduct the evaluation on HumanML3D [2022] test set. ′+′ sign represents a blending of two fine-tuned models with our DiffusionBlending method*

### 消融分析

**DoubleTake消融。** Table 2的消融行揭示三个关键发现：（1）加入第二take（过渡精修）和软遮罩能显著提升FID与过渡自然度；（2）握手长度约1秒时效果稳健，过短导致边界不一致，过长则限制生成多样性；（3）仅靠第一take的握手平均已能生成基本连贯的长序列，但过渡区域仍存在生硬拼接痕迹。

**ComMDM消融。** Table 3的消融表明通信块的设计存在明确的最优配置：（1）通信块置于Transformer较高层（第8层）时效果最佳，根误差从低层配置的更高值降至0.30，说明高层语义特征更适合跨人物协调；（2）单层通信块优于多层堆叠，增加层数反而引入过拟合，损害泛化能力。

**DiffusionBlending消融。** Table 4中，组合控制（以“+”标记）的FID均低于各自单一微调模型，证实DiffusionBlending能有效融合两个控制信号，而非简单取其一。缩放系数s=1（等权混合）在多数任务上表现稳健。

### 失败模式与局限

尽管三种组合策略在各自任务上表现优异，实验和定性分析暴露了若干系统性弱点：

1. **长序列语义漂移。** DoubleTake仅考虑相邻区间的局部上下文，当序列较长时，相距较远的区间可能出现运动语义不一致——例如从“行走”逐渐偏离为不相关的动作类型，因为生成过程缺乏全局语义约束。

2. **双人交互的泛化边界。** ComMDM仅在有限的双人文本对上训练（HumanML3D中每段运动仅约5条文本标注），面对完全未见过的复杂互动描述时，生成质量显著下降，可能出现语义错配或交互缺失。

3. **物理穿模问题。** 当前方法未显式建模物理接触（如握手、搬物），在需要紧密交互的场景中可能产生手部穿模或不自然的接触姿态。这与PhysDiff等物理约束方法的缺失直接相关。

4. **先验质量依赖。** 所有组合方法均基于MDM先验，其动态效果受限于该模型的生成质量。当MDM在特定动作类型（如快速旋转、倒地）上本身生成质量较低时，组合策略无法弥补这一根本缺陷。

5. **TEACH的滑动问题。** 定性对比（Fig. 10）显示，TEACH生成的长序列存在明显的脚底滑动现象，而DoubleTake的过渡更加真实连贯，但这一优势在极长序列（>30秒）上尚未验证。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_openreview_net_pdf_id_dTpbEdN9kr/figures/006_Table.jpg]]

## 方法谱系与知识库定位

### 核心定位：扩散先验的组合泛化

PriorMDM 的方法论核心并非设计新的生成架构，而是将预训练的**运动扩散模型（MDM）**（Tevet et al., ICLR 2023）视为一个冻结或微调的运动流形强先验，通过三种正交的组合策略——**时序顺序组合（DoubleTake）**、**空间并行组合（ComMDM）** 和**模型混合组合（DiffusionBlending）**——以极低甚至零额外训练代价，将其泛化至长序列生成、双人交互和细粒度多关节控制等分布外任务。这一思路在方法论上区别于两类主流范式：

- **专有任务模型**：如 TEACH（Athanasiou et al., 3DV 2022）为长序列生成设计专用的自回归架构，MRT（Wang et al., NeurIPS 2021）为多人运动预测引入 DCT 变换和前缀完成机制。这些方法为每个任务从头构建模型，受限于标注数据的稀缺性。PriorMDM 则证明，一个通用先验加上轻量组合机制即可在对应基准上超越这些专用方法——DoubleTake 在 BABEL 上的 FID 为 1.04，优于 TEACH 的 1.12（Table 1）；ComMDM 在 3DPW 双人前缀完成用户研究中，在交互质量、完整性和整体自然度三个维度上均显著优于 MRT（Figure 8）。

- **原生扩散编辑方法**：MDM inpainting（Tevet et al., ICLR 2023）通过硬性修复单一条件实现运动编辑，但无法灵活组合不同关节的控制信号。PriorMDM 的微调关节控制器配合 DiffusionBlending 采样，将 LeftWrist+Trajectory 组合控制的 FID 从 MDM inpainting 的 1.18 降至 0.22（Table 4），揭示了“微调适配 + 采样时混合”相比“推理时修复”的显著优势。

### 方法谱系中的三个关键创新

**DoubleTake** 将长序列生成问题重构为“并行生成 + 边界精修”的两阶段推理过程。第一阶段在同一批次中并行生成所有运动区间，通过握手（handshake）机制——将前段后缀与后段前缀按线性权重逐帧平均——强制边界一致性；第二阶段将过渡区域与两侧上下文拼接为“三明治”结构，利用软遮罩（soft masking）精修过渡帧。这一设计的关键洞察在于：扩散模型的迭代去噪过程天然允许在每一步施加约束，握手平均公式 $\tau_i = (1-\vec{\alpha}) \odot S_{i-1}[-h:] + \vec{\alpha} \odot S_i[:h]$ 将边界一致性嵌入到生成动力学中，而非事后拼接。

**ComMDM** 的核心是“冻结先验 + 通信块”的架构设计。两个 MDM 的 Transformer 层激活被输入一个单层 Transformer 通信块，输出相加的修正项以协调双人交互，同时可选地预测初始根位置差。消融实验表明，通信块置于 Transformer 较高层（第 8 层）且仅使用 1 层时效果最优，根误差从无通信的 0.54m 降至 0.30m（Table 3）。这一发现暗示：高层语义特征对交互协调至关重要，而过深的通信块可能引入冗余参数。

**DiffusionBlending** 将分类器自由引导（classifier-free guidance）推广到任意两个对齐的扩散模型之间。采样公式 $G_s^{a,b}(X_t, t, c_a, c_b) = G^a(X_t, t, c_a) + s \cdot (G^b(X_t, t, c_b) - G^a(X_t, t, c_a))$ 通过缩放因子 $s$ 线性混合两个微调模型的预测，实现了跨关节类型的复合控制。该方法的前提是：所有微调模型从同一基础 MDM 初始化，保证隐空间对齐。

### 适用边界与已知局限

1. **长序列语义一致性受限**：DoubleTake 的握手机制仅保证局部过渡平滑，但相距较远的区间可能产生运动语义漂移，因为生成过程只考虑相邻局部上下文。这是并行生成策略的固有代价。

2. **双人交互类型泛化有限**：ComMDM 仅学习训练集中出现的有限交互类型，难以泛化到完全未见过的复杂互动。当前实验使用少量文本标注（每段运动约 5 个描述），限制了文本到双人运动的泛化空间。

3. **物理接触缺失**：三种组合方法均未显式建模物理接触（如握手、搬物），可能产生穿模或不自然的接触姿态。将物理约束模块（如 PhysDiff）引入组合框架是可能的改进方向。

4. **先验质量依赖**：所有组合方法的效果上限受限于 MDM 的生成质量。若基础先验在某些运动类型上表现不佳，组合结果也会继承这些缺陷。

### 开放问题

- ComMDM 在更多样化的双人文本对下泛化能力如何？增加少量多样化标注样本能否显著提升性能？
- DiffusionBlending 能否自然地扩展到三个或更多微调模型的组合，实现全身任意关节的混合控制？
- 本文的组合策略在图像、视频等其他扩散生成领域的迁移效果如何？这直接关系到该方法论能否上升为扩散模型的通用组合范式。
- 数据集标注稀缺的背景下，如何自动挖掘运动数据中的隐式过渡和交互模式以辅助训练？这可能是突破当前数据瓶颈的关键方向。

## 原文 PDF

![[paperPDFs/ICLR_2024/HUMAN_MOTION_DIFFUSION_AS_A_GENERATIVE_PRIOR.pdf]]

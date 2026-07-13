---
title: "Shape My Moves: Text Driven Shape Aware Synthesis of Human Motions"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions.pdf
project_link: https://shape-move.github.io/
code_link: null
aliases:
- SSVS
- SMMTDSASHM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过从文本中预测连续的SMPL形状参数（β），并将其注入到量化-去量化过程中，在解码运动令牌时施加形状条件，从而生成形状感知的运动。
primary_logic: 将形状归一化动作离散化为内容令牌（FSQ-VAE），同时通过形状特征条件化解码器恢复风格信息，实现了内容与风格的解耦，使得语言模型能够同时预测动作令牌和形状参数，实现端到端的文本到形状感知运动生成。
claims:
- SA‑VAE在重建任务中FID降至0.125，骨骼长度误差减少近一半，优于基线量化方法。
- 在物理合理性指标（穿透率、滑步率、浮动等）上全面超越基线。
- 感知评估中本文方法偏好度接近真实运动，超出基线约12%~38%。
- 消融实验证明形状条件、浮动损失、滑步损失和骨骼长度损失对最终性能均有贡献。
---

# Shape My Moves: Text Driven Shape Aware Synthesis of Human Motions

> [!tip] 核心洞察
> 将形状归一化动作离散化为内容令牌（FSQ-VAE），同时通过形状特征条件化解码器恢复风格信息，实现了内容与风格的解耦，使得语言模型能够同时预测动作令牌和形状参数，实现端到端的文本到形状感知运动生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 塑造我的动作：文本驱动的形状感知人体运动合成 |
| 英文题名 | Shape My Moves: Text Driven Shape Aware Synthesis of Human Motions |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://shape-move.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ShapeMove (SA-VAE + ShapeMove) |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，Penetrate (cm) ↓ 0.0268 vs best baseline (see Table 1) (Ours best)；Float (cm) ↓ 0.2658 vs best baseline (see Table 1) (Ours best)；Skate Ratio (%) ↓ 6.143 vs best baseline (see Table 1) (Ours best)。

## 概要

文本到人体运动生成近年来取得了显著进展，但现有方法普遍将运动标准化到统一的规范人体模型上，忽视了不同身体形状带来的生理学与运动学差异。这一瓶颈导致：当同一运动映射到不同体形时，会产生穿透、滑步、漂浮等物理失真，严重影响运动真实感。

本文提出 **ShapeMove**，一个文本驱动的形状感知运动合成框架。其核心洞察是：将形状归一化运动离散化为内容令牌，同时通过形状特征条件化解码器恢复风格信息，实现内容与风格的解耦。具体而言，框架包含两个阶段：

- **SA‑VAE（形状感知有限标量量化变分自编码器）**：采用 FSQ 将形状归一化运动量化为离散令牌，并在解码时注入 SMPL 形状参数 β 作为条件，重建形状感知运动。该方法无需额外正则化，码本利用率更高。
- **ShapeMove（形状‑运动令牌预测器）**：利用预训练语言模型，从文本描述中自回归预测 `[BETA]` 令牌和运动令牌序列，通过嵌入投影器映射到连续形状参数，实现端到端的文本到形状感知运动生成。

在 HumanML3D 数据集上的实验表明，ShapeMove 在物理合理性指标（穿透率、漂浮、滑步率、骨骼长度方差）和文本‑运动匹配指标（RPrecision、FID）上全面超越 **T2M‑GPT**（Zhang et al., CVPR 2023）、**MotionGPT**（Jiang et al., NeurIPS 2024）和 **MotionDiffuse**（Zhang et al., arXiv 2022）等基线方法。感知评估中，本文方法的偏好度接近真实运动，超出基线约 12%~38%。消融实验证实了形状条件及各物理损失项的独立贡献。

该方法的主要局限在于依赖模板化的形状描述，难以处理自由形式的自然语言输入；同时，形状参数预测误差在极端体形上可能被放大。



文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。近年来，基于变分自编码器（VQ‑VAE）与语言模型的两阶段框架，如 **T2M‑GPT**（Zhang et al., CVPR 2023）和 **MotionGPT**（Jiang et al., NeurIPS 2024），以及基于扩散模型的 **MotionDiffuse**（Zhang et al., arXiv 2022），在文本‑运动对齐与生成多样性上取得了显著进展。然而，这些方法存在一个共同的隐含假设：所有运动都被标准化到一个统一的规范人体模型上，完全忽略了不同身体形状带来的生理学差异。如图1所示，同样的跑步动作在瘦削与肥胖体形上的表现存在显著差异，而现有方法无法捕捉这种形状驱动的运动变化。

这一瓶颈的根源在于，现有框架仅将运动视为纯运动学序列，未将身体形状作为生成条件纳入建模。当这些方法生成的运动被迁移到不同体形时，往往会出现脚部穿透地面、滑步、肢体比例失真等物理伪影，严重损害运动的真实感。此外，现有文本编码器通常无法解析描述身体形状的文本输入，导致模型缺乏“形状感知”能力。

为解决上述问题，本文提出 **ShapeMove**——一个文本驱动的形状感知运动合成框架。其核心动机在于：**运动的内容（语义动作）与风格（由体形决定的运动表现）应当被解耦**。具体而言，ShapeMove 通过两个阶段实现这一目标：（1）设计一个形状感知的有限标量量化变分自编码器（SA‑VAE），将形状归一化的运动压缩为离散内容令牌，并在解码时注入连续形状参数以恢复形状特定的运动风格；（2）利用预训练语言模型同时预测形状参数与运动令牌，实现端到端的文本到形状感知运动生成。这一设计使得模型既能保持文本‑运动语义对齐，又能根据指定的身体属性生成物理合理的个性化运动。



## 核心方法与创新机理

本文的核心突破在于将**人体形状信息显式地引入文本到动作生成的完整流程**，解决了现有方法将运动归一化到统一规范人体模型后，忽略不同体形带来的生理学差异这一根本瓶颈。具体而言，本文提出了三个层面的关键创新：

### 1. 形状条件注入机制（Shape Conditioning）

现有文本到动作生成方法（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MotionGPT** (Jiang et al., NeurIPS 2024)、**MotionDiffuse** (Zhang et al., arXiv 2022)）仅从文本预测动作令牌，完全忽略了执行动作的人物体形。本文的创新在于通过特殊的 `[BETA]` 令牌，使语言模型能够**同时预测 SMPL 形状参数与运动令牌**，并将形状参数作为解码器的显式条件注入到去量化过程中。

具体而言，在 **SA-VAE** 阶段，形状投影器 $P_{\theta_s}$ 将 SMPL 形状参数 $\beta$ 投影为与运动令牌 $\hat{Z}$ 对齐的形状特征 $\tilde{\beta}$，拼接后送入运动解码器 $D$ 进行重建。在 **ShapeMove** 推理阶段，语言模型自回归预测 `[BETA]` 令牌，其嵌入通过投影器 $P_{\theta_e}$ 映射为预测的形状参数 $\hat{\beta}$，再与预测的运动令牌 $\hat{C}$ 拼接后解码生成形状感知运动。这一设计实现了**内容（运动模式）与风格（体形特征）的解耦**：形状归一化运动被离散化为内容令牌，而形状条件则负责在解码时恢复风格信息。

### 2. 有限标量量化（FSQ）替代 VQ-VAE

传统文本到动作方法普遍采用 VQ-VAE 进行运动量化，但 VQ-VAE 需要额外的码本正则化损失（如承诺损失）来稳定训练，且常面临码本利用率低的问题。本文改用 **FSQ**（Finite Scalar Quantization，有限标量量化），其核心优势在于：
- **无需额外正则化**：FSQ 通过将连续特征投影到有限标量空间实现离散化，天然避免了码本坍塌；
- **更高的码本利用率**：FSQ 构造的码本（配置为 $\ell = [8, 5, 5, 5]$，码本大小 $k = 1000$）能够更充分地利用离散空间。

这一改进使得 SA-VAE 在重建任务中 FID 降至 **0.125**，骨骼长度误差相比基线量化方法**减少近一半**（Table 2），为下游的形状感知生成提供了更高质量的离散表示。

### 3. 物理合理性导向的几何损失函数

为强化生成运动对不同体形的物理适应性，本文在 SA-VAE 的优化目标中引入了三项几何约束损失，构成完整的 VQ-VAE 损失函数：

$$L_{vq} = L_r + \lambda_f L_{float} + \lambda_s L_{slide} + \lambda_b L_{bone}$$

其中：
- **浮动损失 $L_{float}$**：约束脚部与地面的接触一致性，减少漂浮伪影；
- **滑步损失 $L_{slide}$**：抑制脚部在地面上的不自然滑动；
- **骨骼长度损失 $L_{bone}$**：确保生成运动的骨骼比例与目标体形一致。

消融实验（Table 3）证实，上述三项损失与形状条件共同作用，逐步改善 FID 和物理合理性指标（穿透率、浮动、滑步率），去除任一组件均导致性能下降。这使得本文方法在穿透率（0.0268 cm）、浮动（0.2658 cm）、滑步率（6.143%）等物理指标上全面超越基线（Table 1），并在感知评估中偏好度接近真实运动，超出基线约 12%~38%（Figure 5）。

### 创新点总结

| 创新维度 | 基线做法 | 本文方法 | 关键证据 |
|---------|---------|---------|---------|
| 形状条件注入 | 无形状条件，仅预测动作令牌 | 通过 `[BETA]` 令牌预测形状参数并作为解码器条件 | Figure 3, Table 3 消融 |
| 量化器类型 | VQ-VAE，需额外正则化 | FSQ，无需正则化，码本利用率更高 | Table 2 重建对比 |
| 损失函数 | 仅重建损失 | 加入浮动、滑步、骨骼长度三项几何约束 | Table 3 消融 |

这三项创新协同作用，使得 ShapeMove 成为首个能够**端到端地从文本同时生成形状参数与形状感知运动**的框架，填补了文本到动作生成领域对体形差异建模的空白。



ShapeMove 采用两阶段流水线，将文本到动作生成分解为**离散运动令牌量化**与**形状‑运动令牌联合预测**两个阶段，从而实现端到端的形状感知运动合成。

### 阶段一：形状感知 FSQ‑VAE（SA‑VAE）

第一阶段的核心目标是学习一个能够将运动压缩为离散令牌、并利用连续体形信息重建形状感知运动的量化网络。其处理流程如下：

1. **运动编码**：输入为经过形状归一化的运动序列 $X^N \in \mathbb{R}^{T \times D}$（长度 $T$，维度 $D=263$）。运动编码器 $E$ 将其下采样为运动特征 $Z \in \mathbb{R}^{\tau \times D}$（$\tau$ 为 $T$ 的下采样长度）。
2. **有限标量量化（FSQ）**：使用 FSQ 量化器将连续特征 $Z$ 离散化为令牌 $\hat{Z}$。与需要额外正则化的 VQ‑VAE 不同，FSQ 无需码本坍缩损失，码本利用率更高。
3. **形状条件注入**：形状投影器 $P_{\theta_s}$ 将 SMPL 形状参数 $\beta$ 映射为与 $\hat{Z}$ 对齐的形状特征 $\tilde{\beta}$，并将二者拼接。
4. **运动解码**：运动解码器 $D$ 以拼接后的 $[\hat{Z}, \tilde{\beta}]$ 为条件，重建形状感知运动 $\hat{X}^R$。

SA‑VAE 的训练目标在标准平滑 L1 重建损失基础上，额外引入了三项物理合理性约束：

$$L_{vq} = L_r + \lambda_f L_{float} + \lambda_s L_{slide} + \lambda_b L_{bone}$$

其中 $L_r$ 对原始运动与旋转不变部分分别施加平滑 L1 损失；$L_{float}$、$L_{slide}$、$L_{bone}$ 分别惩罚脚部浮动、滑步和骨骼长度偏差。这种设计使得量化令牌能够保留运动内容，而形状信息则通过解码器条件恢复风格差异，实现了**内容与风格的解耦**。

### 阶段二：形状‑运动令牌预测器（ShapeMove）

第二阶段利用预训练语言模型的序列建模能力，从文本中同时预测形状参数和运动令牌序列。训练与推理流程如下：

- **训练阶段**：Transformer 网络接收描述人体动作与体形的文本输入，自回归地预测量化运动令牌 $\hat{C}$ 以及特殊令牌 `[BETA]`。`[BETA]` 的嵌入通过嵌入投影器 $P_{\theta_e}$ 映射为预测的形状参数 $\hat{\beta}$。训练目标由两项构成：
  - 令牌损失：$L_{token} = \text{CrossEntropy}(C, \hat{C})$
  - 形状损失：$L_{shape} = \lambda_{\beta} |\beta - \hat{\beta}|$

- **推理阶段**：模型从文本输入预测运动令牌 $\hat{C}$ 和形状参数 $\hat{\beta}$。$\hat{C}$ 经 FSQ 反量化后，与通过形状投影器 $P_{\theta_s}$ 处理后的 $\hat{\beta}$ 拼接，最终由运动解码器 $D$ 生成形状感知的运动序列。

### 关键设计决策

| 设计槽位 | 基线方案 | 本文方案 | 依据 |
|---------|---------|---------|------|
| 形状条件注入 | 无形状条件，仅预测运动令牌 | 通过 `[BETA]` 令牌预测形状参数并注入解码器 | Figure 3, Section 3.3 |
| 量化器类型 | VQ‑VAE，需额外正则化 | FSQ，无需额外正则化，码本利用率更高 | Section 3.2, |

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/003_Figure_3.jpg]]
*Figure 3: ShapeMove Overview. In the training phase (a), the transformer network takes in the text inputs describing human motions and body shapes and predicts quantized motion tokens and the shape token [BETA]. The embedding for [BETA] passes through the Projector*

这种两阶段设计的核心优势在于：SA‑VAE 将形状归一化动作压缩为内容令牌，同时通过形状条件化解码器保留风格信息；ShapeMove 则利用语言模型同时预测内容令牌与形状参数，实现了**单阶段文本到形状感知运动的端到端生成**，无需后处理或独立的形状回归步骤。



ShapeMove 的整体框架由两个阶段级联构成：**形状感知 FSQ-VAE（SA‑VAE）** 与 **形状‑运动令牌预测器（ShapeMove）**。前者负责将形状归一化运动离散化为内容令牌，并在解码时注入形状条件以恢复风格信息；后者则利用预训练语言模型自回归地同时预测形状参数和运动令牌，实现端到端的文本驱动形状感知运动生成。

### 3.1 SA‑VAE：形状感知的量化自编码器

SA‑VAE 的核心设计目标是将“内容”（动作语义）与“风格”（身体形状）解耦。其工作流程如下：

1. **运动编码器 E**：输入形状归一化运动 $X^N \in \mathbb{R}^{T \times D}$（$T$ 为序列长度，$D=263$ 为单帧表示维度），编码为下采样的运动特征 $Z \in \mathbb{R}^{\tau \times D}$，其中 $\tau$ 为 $T$ 的下采样结果（实验中 $T=64$，$\tau=16$）。
2. **FSQ 量化器**：采用有限标量量化（Finite Scalar Quantization, FSQ）将连续特征 $Z$ 量化为离散令牌 $\hat{Z}$。相较于传统 VQ‑VAE，FSQ 无需额外的承诺损失或码本重置等正则化手段，码本利用率更高。实验中 FSQ 层级配置为 $\ell = [8, 5, 5, 5]$，构建码本大小 $k=1000$，每个索引维度为 512。
3. **形状投影器 $P_{\theta_s}$**：将 SMPL 形状参数 $\beta$ 投影为与 $\hat{Z}$ 对齐的形状特征 $\tilde{\beta}$。
4. **运动解码器 D**：以 $\hat{Z}$ 与 $\tilde{\beta}$ 的拼接为条件，重建形状感知运动 $\hat{X}^R$。

**核心公式**：SA‑VAE 的优化目标由重建损失与三项几何物理损失加权组合而成。

**重建损失**（Equation 1）采用平滑 L1 损失，并对旋转不变部分施加额外权重：

$$L_r = L_1^{\text{smooth}}(X, \hat{X}) + \lambda_{\text{rot}} L_1^{\text{smooth}}(X_{\text{rot}}, \hat{X}_{\text{rot}})$$

其中 $X$ 为真实运动，$\hat{X}$ 为重建运动，$X_{\text{rot}}$ 表示旋转不变的运动表示分量，$\lambda_{\text{rot}}$ 为旋转损失权重。

**SA‑VAE 总损失**（Equation 2）在重建损失基础上引入三项物理合理性约束：

$$L_{\text{vq}} = L_r + \lambda_f L_{\text{float}} + \lambda_s L_{\text{slide}} + \lambda_b L_{\text{bone}}$$

- $L_{\text{float}}$：浮动损失，惩罚脚部离地但未发生位移的悬浮现象。
- $L_{\text{slide}}$：滑步损失，惩罚脚部着地时的不合理滑动。
- $L_{\text{bone}}$：骨骼长度损失，约束重建运动的骨骼长度与真实值一致，是形状感知的关键保障。
- $\lambda_f$、$\lambda_s$、$\lambda_b$ 为各损失项的平衡权重。

消融实验（Table 3）证实，形状条件（sc）与上述三项物理损失对最终性能均有正向贡献，移除任一组件均导致 FID 和物理指标（穿透率、浮动、滑步）的退化。

### 3.2 ShapeMove：文本驱动的形状与运动令牌联合预测

ShapeMove 在 SA‑VAE 的离散令牌空间之上，利用预训练 T5 语言模型实现文本到形状感知运动的端到端生成。其训练与推理流程如 Figure 3 所示。

**训练阶段**：语言模型输入文本描述（同时包含动作与体形信息），自回归地预测两类令牌：
- **运动令牌序列 $\hat{C}$**：对应 SA‑VAE 量化后的离散运动表示。
- **形状令牌 `[BETA]`**：其嵌入通过嵌入投影器 $P_{\theta_e}$ 映射为预测的形状参数 $\hat{\beta}$。

**核心公式**：训练过程由两项损失联合优化。

**令牌预测损失**（Equation 3）为标准交叉熵损失，监督运动令牌的预测：

$$L_{\text{token}} = \text{CrossEntropy}(C, \hat{C})$$

其中 $C$ 为真实运动令牌序列，$\hat{C}$ 为模型预测序列。

**形状预测损失**（Equation 4）为形状参数的 L1 损失：

$$L_{\text{shape}} = \lambda_{\beta} |\beta - \hat{\beta}|$$

其中 $\beta$ 为真实 SMPL 形状参数，$\hat{\beta}$ 为从 `[BETA]` 令牌嵌入投影得到的预测值，$\lambda_{\beta}$ 为损失权重。

**推理阶段**：语言模型从文本中自回归生成 $\hat{C}$ 与 $\hat{\beta}$，随后 $\hat{C}$ 经 FSQ 反量化、$\hat{\beta}$ 经形状投影器 $P_{\theta_s}$ 对齐后，二者拼接送入运动解码器 D，输出最终的运动序列。

### 3.3 关键设计要点

- **内容与风格解耦**：SA‑VAE 在形状归一化运动上学习离散令牌（内容），同时通过形状条件化解码器恢复体形信息（风格），使得语言模型能够独立预测动作语义令牌和形状参数。
- **FSQ 替代 VQ**：FSQ 避免了传统 VQ‑VAE 的码本坍塌和正则化调参问题，在重建质量上表现出显著优势——SA‑VAE 在重建任务中 FID 降至 0.125，骨骼长度误差较基线量化方法减少近一半（Table 2）。
- **物理损失的多重约束**：浮动损失、滑步损失和骨骼长度损失共同作用，确保生成的运动在不同体形下仍满足物理合理性（Table 1 中穿透率 0.0268 cm、浮动 0.2658 cm、滑步率 6.143% 均达到最优）。

### 补充图表

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/002_Figure_2.jpg]]
*Figure 2: Shape-Aware FSQ-VAE (SA-VAE) Overview. SA-VAE is our quantization network learning to generate discrete motion tokens. Given a shape-normalized motion*



## 实验与关键发现

### 主要结果

我们在HumanML3D基准上将ShapeMove与三类代表性基线进行了全面对比：基于VQ-VAE的**T2M-GPT**（Zhang et al., CVPR 2023）、将动作视为外语进行语言模型预测的**MotionGPT**（Jiang et al., NeurIPS 2024）以及基于扩散模型的**MotionDiffuse**（Zhang et al., arXiv 2022）。为确保公平，所有基线均使用形状感知运动数据重新训练，并保持相同的任意长度生成约束。

**物理合理性**方面，ShapeMove在所有四项指标上均取得最优（Table 1）：穿透率（Penetrate）降至0.0268 cm，浮动（Float）降至0.2658 cm，滑步率（Skate Ratio）降至6.143%，骨骼长度方差（Bone Length Variances）为0.625。这些指标直接衡量生成运动在不同体形下的物理真实性，其中穿透率的显著优势表明模型有效避免了身体部件相互穿插的伪影。

**文本-运动匹配度**方面，ShapeMove在RPrecision Top1/2/3上分别达到0.413/0.601/0.705，FID降至0.198，MMDist降至3.533，均优于所有基线（Table 1）。多样性（Diversity）为0.117，与基线保持可比水平，说明模型在提升质量的同时未牺牲生成多样性。

**感知评估**（Figure 5）进一步验证了上述定量结果。人类标注者在三个维度上对生成样本进行偏好判断：形状与文本匹配度、动作与文本匹配度、动作在对应体形上的合理性。结果显示，本文方法的偏好度接近真实运动（Ground Truth），超出基线约12%~38%，表明形状感知生成在主观体验上同样具有显著优势。

### 量化器重建分析

SA-VAE作为第一阶段量化网络，其重建质量直接影响下游生成效果。Table 2对比了SA-VAE与基线VAE在形状感知真实运动上的重建性能。SA-VAE取得FID 0.125，骨骼长度差异（Bone Length Diff）降至45.88 mm，抖动差异（Jitter Diff）为31.49 m/s²。值得注意的是，骨骼长度误差相比基线减少近一半，直接验证了形状条件注入的有效性——解码器通过拼接的形状特征β̃恢复了在形状归一化过程中丢失的体形信息。

### 消融实验

Table 3的系统消融揭示了各组件的贡献。以无形状条件（sc）且无物理损失项的配置为基线（FID 0.362, Bone Length Diff 59.85 mm, Float 0.466 cm, Skate 8.42%），逐步添加组件：

- **添加形状条件**（sc）：FID降至0.291，骨骼长度误差降至52.42 mm，表明形状条件本身已能显著改善重建质量。
- **添加浮动损失**（L_float）：Float降至0.278 cm，验证了该损失项对抑制脚部离地伪影的作用。
- **添加滑步损失**（L_skate）：Skate降至6.49%，有效减少了脚部在地面上的不自然滑动。
- **添加骨骼长度损失**（L_bone）：Bone Length Diff进一步降至45.88 mm，FID达到最优0.125。

完整模型（sc + L_bone + L_float + L_skate）在所有指标上均取得最优或次优，去除任一组件均导致性能下降，证明了各损失项与形状条件的互补性。

### 身体属性预测

ShapeMove是首个同时预测形状参数与运动令牌的方法。Table 4报告了六项身体属性（身高、肩宽、胸围、腰围、臀围、腿长）的预测误差，均控制在约1 cm左右。这一精度表明语言模型能够从文本描述中有效推断体形特征，为端到端的形状感知生成奠定了基础。

### 失败模式与局限

尽管整体性能优异，本文方法仍存在以下局限：

1. **形状描述泛化性**：当前依赖模板化的形状描述（如“tall, broad-shouldered”），难以处理自由形式的多样化自然语言形状输入，需要额外的预处理步骤标准化描述。
2. **极端体形放大误差**：形状参数预测误差虽小（约1 cm），但在极端体形（如非常矮小或非常高大）上可能被放大，导致生成运动出现物理失真。
3. **数据多样性受限**：训练主要基于HumanML3D数据集，所涵盖的体形和动作类型有限，模型对训练分布外的体形和动作的泛化能力尚待验证。
4. **物理指标与感知关联**：当前物理合理性指标（穿透率、浮动、滑步率）与人类对运动真实性的感知之间的关联程度仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/004_Table_1.jpg]]
*Table 1: Comparison with Baselines. We evaluate the Penetrate, Float, Skate Ratio, and Bone Length Variances for our method and available baselines. For fair comparison, retrain baselines with shape-aware motions. The Shape Input Capability column indicates methods that can incorporate both shape and motion descriptions — a ✗ here suggests the corresponding text encoder cannot parse shape descriptions. Arbitrary Length denotes results obtained without using ground-truth motion lengths. We compare with methods that share the same constraints as ours, capable of generating arbitrary motion lengths and accepting shape descriptions as input. Our method achieves the best or comparable results across the...*

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/005_Table_2.jpg]]
*Table 2: Quantizer Reconstruction Comparison. We report the reconstruction results, comparing our SA-VAE against baseline methods that utilize a VAE to quantize motion into discrete tokens. We assess the bone length difference, jitter score difference, and FID score relative to the shape-aware ground truth motions. Our VAE outperforms the baseline across all three metrics, particularly in reducing the bone length error by nearly half. These results demonstrate our model’s effectiveness in aligning with the physical form of different body shapes. and*

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/006_Table_3.jpg]]
*Table 3: Ablation Study. sc stands for shape-conditioning*

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/007_Table_4.jpg]]
*Table 4: Attributes Prediction. We present the differences (cm) across six attributes between our beta predictions and the ground truth, focusing solely on our method as no comparable works predict beta concurrently. Our model demonstrates a robust ability to predict the correct beta values, with discrepancies from the ground truth around one cm. C. stands for circumference*

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons. We compare our method with three baseline methods, T2M-GPT [105], MotionGPT [50], and MotionDiffuse [106], illustrating two samples from the HumanML3D test set. The motions are colored from light to dark blue to represent progression over time. We highlight issues such as incorrect foot motion and other inaccuracies that do not align with expected motion patterns. Our method not only generates motions that align with the textual descriptions, but also accurately follows the body attributes and physical dynamics of the ground truth. Additional visual results and detailed comparisons are available in the project website*

![[assets/figures/papers/paper_list_l1864_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions/figures/010_Figure_5.jpg]]
*Figure 5: Perceptual Evaluation. We show the distributions of aggregate responses from annotators on their preferences for samples generated by our method and baseline methods, including MotionDiffuse [106], MotionGPT [50], and T2M-GPT [105], as well as the corresponding ground truth samples. We assess the distributions on three metrics: (a) Shape to Text, how well the body shape matches the text input; (b) Motion to Text, how well the motion matches the text input; and (c) Plausibility of Motion with Shape, how realistic the motions appear for the corresponding body shapes. Across all three metrics, we observe that our method is preferred nearly as much as the ground truth and is favored by approxim...*



## 定位与知识库关联

### 核心瓶颈与因果杠杆

现有的文本到动作生成方法——包括**T2M‑GPT**（Zhang et al., CVPR 2023）、**MotionGPT**（Jiang et al., NeurIPS 2024）和**MotionDiffuse**（Zhang et al., arXiv 2022）——均将人体运动标准化到一个统一的规范人体模型上，隐式地假设“同一段动作在任何体形上看起来都一样”。这一假设在生理学上不成立：不同身体形状（如肢体长度、围度、质量分布）会显著改变关节运动学与动力学表现，将规范模型上生成的动作直接迁移到不同体形时，必然产生穿透、滑步、漂浮等物理失真。

ShapeMove 的核心杠杆在于**将形状参数从生成流程的后处理环节提前到量化-去量化过程的条件变量**：通过从文本中预测连续的 SMPL 形状参数 β，并将其注入有限标量量化（FSQ）变分自编码器的解码阶段，使得运动令牌在去量化时即携带形状条件，从而端到端地生成形状感知的运动。这一设计将“内容”（形状归一化后的运动模式）与“风格”（由体形决定的运动表现）在表示层面解耦：内容由离散的运动令牌承载，风格由连续的形状特征条件恢复。

### 与基线方法的关系与差异化

**与 VQ‑VAE 类方法的关系。** T2M‑GPT 和 MotionGPT 均采用 VQ‑VAE 将运动量化为离散令牌，再由语言模型自回归预测令牌序列。ShapeMove 继承了这一“量化-语言模型预测”的两阶段范式，但在两个关键槽位上做了替换：

| 设计槽位 | 基线取值 | ShapeMove 取值 | 证据锚点 |
|---------|---------|---------------|---------|
| 形状条件注入 | 无形状条件（仅预测运动令牌） | 通过 `[BETA]` 令牌预测 β，并将其作为解码器条件 | Figure 3, Section 3.3 |
| 量化器类型 | VQ‑VAE（需额外承诺损失与码本重置等正则化） | FSQ（有限标量量化，无需额外正则化，码本利用率更高） | Section 3.2, |

这两个替换并非孤立改进：FSQ 避免了 VQ‑VAE 中常见的码本坍塌问题，使量化器能更稳定地保留运动细节；而形状条件注入则使得解码器在重建时能够显式地补偿不同体形带来的骨骼长度与关节运动范围差异。Table 2 的重建对比为此提供了强证据——SA‑VAE 的 FID 降至 0.125，骨骼长度误差（45.88 mm）相比基线减少近一半。

**与扩散模型类方法的关系。** MotionDiffuse 基于扩散模型直接从文本生成运动序列，其生成过程不涉及离散令牌，因此天然缺乏与语言模型集成的便利性。ShapeMove 选择语言模型路线，不仅因为其自回归预测与文本令牌天然对齐，更因为形状参数 β 的连续预测可以自然地作为特殊令牌嵌入到同一自回归序列中，实现运动令牌与形状参数的联合预测——这是扩散模型架构较难直接实现的。

**公平性说明。** 为公平对比，所有基线方法均使用形状感知运动数据重新训练，并保持相同的动作长度生成约束（不依赖真实运动长度）。这意味着 Table 1 中报告的性能差异确实来自方法设计本身，而非数据或实验设置的不对等。

### 适用边界

ShapeMove 的有效性建立在以下前提之上：

1. **模板化的形状描述。** 当前方法依赖预定义的形状描述模板（如“a person with long legs and wide shoulders”）来提取文本中的形状信息。对于自由形式的多样化自然语言形状输入（如“像举重运动员那样的倒三角身材”），模型可能无法正确解析。这是方法的一个显式局限。

2. **数据集的体形与动作覆盖。** 训练数据主要来自 HumanML3D，该数据集虽包含一定体形多样性，但极端体形（如显著肥胖或极度瘦削）和长尾动作类型的样本有限。Table 4 显示形状参数预测误差约 1 cm 量级，在常见体形上可接受，但在极端体形上可能被放大。

3. **单人运动假设。** 当前框架仅处理单人运动生成，未建模多人交互或人与场景的物理交互。扩展到多人场景需要处理多个形状参数的联合预测与物理约束（如碰撞避免），这是开放问题。

### 局限与开放问题

**已确认的局限：**

- 形状描述的模板依赖性限制了端到端的通用性，需要额外的语言模型预处理步骤来标准化形状描述。
- 物理合理性指标（穿透率、滑步率、浮动等）虽全面优于基线，但这些指标与人类对运动真实性的感知之间的相关性尚未被严格量化——Figure 5 的感知评估提供了初步证据（本文方法偏好度接近真实运动，超出基线约 12%~38%），但评估维度与样本量仍需扩展。
- 生成运动的多样性（Diversity 指标）与基线可比但未显著超越，暗示形状条件的注入可能在一定程度上约束了运动风格的探索空间。

**开放问题：**

- 模型能否泛化到训练集中未出现的极端体形或全新动作类型？这需要跨数据集或零样本体形泛化的实验验证。
- 如何利用更强大的语言模型直接理解多样化的形状描述，而无须固定的模板？这涉及将形状理解从分类式模板匹配升级为开放词汇推理。
- 物理合理性指标与人类感知之间的映射关系是什么？是否需要在评估体系中引入基于物理模拟的验证（如力矩平衡、足地接触力）？
- 能否将单人物的形状感知运动生成扩展到多人交互场景？这需要同时处理多个形状参数、空间关系约束以及社交信号（如眼神、手势协调）。

### 知识库定位

ShapeMove 处于**文本条件运动生成**与**形状感知人体建模**的交叉点。在运动生成方向，它继承并改进了 VQ‑VAE + 语言模型的两阶段范式（T2M‑GPT, MotionGPT）；在形状建模方向，它首次将 SMPL 形状参数的连续预测与运动令牌的离散预测统一到同一自回归框架中。其核心贡献不在于提出全新的生成范式，而在于识别并填补了“文本到运动生成中形状信息缺失”这一被普遍忽视的空白——通过 FSQ 量化器与形状条件解码器的协同设计，以较小的架构改动实现了显著的物理合理性增益。



## 原文 PDF

![[paperPDFs/CVPR_2025/Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions.pdf]]

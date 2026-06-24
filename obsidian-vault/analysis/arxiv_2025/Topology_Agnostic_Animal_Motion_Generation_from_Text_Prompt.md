---
title: Topology-Agnostic Animal Motion Generation from Text Prompt
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Topology_Agnostic_Animal_Motion_Generation_from_Text_Prompt.pdf
aliases:
- GAMGTASE
- TAAMGFTP
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 拓扑感知的骨骼嵌入模块（Topology-aware Skeleton Embedding Module）。该模块利用图Transformer将任意骨骼的几何与结构关系编码为统一的条件嵌入，使得模型能够理解并融合文本语义与骨骼拓扑，从而控制运动生成。
primary_logic: 将任意骨骼拓扑表示为基于图距离和关系类型的注意力偏置，并与多尺度文本描述编码结合，在掩码自回归框架中通过广义残差VQ-VAE处理可变关节数运动，实现了首个真正拓扑无关的文本驱动动物运动生成。
claims:
- 去除拓扑感知骨骼嵌入模块后，FID从0.044飙升至0.097，性能下降54.6%，证明该模块是保证生成质量与跨语义一致性的关键。
- 完整模型在OmniZoo测试集上取得FID 0.044，相较于最强基线MoMask提升48.2%，同时文本-运动检索准确率R@1达到0.621、提升23.2%。
- OmniZoo testset 上 FID = 0.044
- OmniZoo testset 上 Text-Motion Retrieval R@1 = 0.621
---

# Topology-Agnostic Animal Motion Generation from Text Prompt

> [!tip] 核心洞察
> 将任意骨骼拓扑表示为基于图距离和关系类型的注意力偏置，并与多尺度文本描述编码结合，在掩码自回归框架中通过广义残差VQ-VAE处理可变关节数运动，实现了首个真正拓扑无关的文本驱动动物运动生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 拓扑无关的文本驱动动物运动生成 |
| 英文题名 | Topology-Agnostic Animal Motion Generation from Text Prompt |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.10352) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Generalized Autoregressive Motion Generation with Topology-Aware Skeleton Embedding |
| Dataset | OmniZoo testset |

> [!tip] 效果简介
> - OmniZoo testset 上，FID 0.044 vs MoMask (best baseline) (-48.2%)；Text-Motion Retrieval R@1 0.621 vs MoMask (best baseline) (+23.2%)。

## 概述

现有文本驱动运动生成方法普遍依赖固定骨骼模板（如 SMPL），无法泛化至任意拓扑的骨架，且缺乏大规模异构动物运动数据，导致难以在统一框架中实现跨物种的文本驱动运动生成。针对这一瓶颈，本文提出一种**广义自回归运动生成框架**，其核心在于**拓扑感知的骨骼嵌入模块**——利用图 Transformer 将任意骨骼的几何与结构关系编码为统一的条件嵌入，使模型能够同时理解文本语义与骨骼拓扑，从而控制运动生成。

方法层面的关键创新包括：将任意骨骼拓扑表示为基于图距离和关系类型的注意力偏置，与多尺度文本描述编码融合；在掩码自回归框架中，通过广义残差 VQ-VAE 处理可变关节数的运动序列。这一设计使得模型成为首个真正拓扑无关的文本驱动动物运动生成方法。

在 OmniZoo 测试集上，完整模型取得 FID 0.044，相较于最强基线 **MoMask**（Guo et al., CVPR 2024）提升 48.2%；文本-运动检索准确率 R@1 达到 0.621，提升 23.2%。消融实验进一步表明，移除拓扑感知骨骼嵌入模块后 FID 飙升至 0.097（性能下降 54.6%），验证了该模块是保证生成质量与跨语义一致性的关键因果调控变量。

## 背景与动机

### 问题背景

在计算机图形学与具身智能的交叉领域，生成自然、可控的动物运动一直是一项核心挑战。与人类运动生成不同——后者已因SMPL等参数化模型的成熟而取得显著进展——动物运动生成面临着两个根本性困难。首先，动物物种之间的骨骼拓扑差异极大：猫科动物的四足结构与鸟类的双足结构在关节数量、连接关系和运动学约束上毫无共同之处。其次，大规模、高质量的异构动物运动数据极度匮乏，现有数据集要么局限于单一物种，要么规模不足以支撑通用生成模型的训练。

### 现有方法的根本瓶颈

当前主流的文本驱动运动生成方法——包括**MoMask**（Guo et al., CVPR 2024）和**MMM**（Pinyoanuntapong et al., CVPR 2024）——在架构设计上存在一个共同的隐含假设：目标骨架的拓扑结构是固定且预先已知的。这些方法普遍依赖SMPL等人体参数化模型所定义的固定关节配置，其VQ-VAE的编码器和解码器、以及条件注入机制，都是针对特定数量的关节和预定义的骨骼连接关系设计的。

这一设计选择的后果是：当面对一只猫、一只鸟或一条鱼的骨架时，这些方法完全无法工作——不是因为生成能力不足，而是因为它们从根本上缺乏理解任意骨骼拓扑的能力。这构成了领域内的核心瓶颈：**现有运动生成方法普遍依赖固定骨骼模板，无法泛化到任意拓扑的骨架，且缺乏大规模异构动物运动数据，导致难以在统一框架中实现文本驱动的跨物种运动生成。**

### 本文动机与核心思路

针对上述瓶颈，本文提出了一个根本性的问题：能否构建一个真正拓扑无关的文本驱动运动生成框架——给定任意物种的骨骼结构和一段文本描述，即可生成与该骨骼解剖结构一致、且语义上忠实于文本的运动序列？

实现这一目标需要同时解决两个技术难题：（1）如何表示和学习具有可变关节数量的运动序列；（2）如何将任意骨骼的拓扑信息编码为模型可理解的条件信号。本文的核心洞察在于：**将任意骨骼拓扑表示为基于图距离和关系类型的注意力偏置，并与多尺度文本描述编码结合，在掩码自回归框架中通过广义残差VQ-VAE处理可变关节数运动**，从而首次实现了拓扑无关的文本驱动动物运动生成。

这一思路的技术关键在于一个**拓扑感知的骨骼嵌入模块（Topology-aware Skeleton Embedding Module）**。该模块利用图Transformer将任意骨骼的几何与结构关系编码为统一的条件嵌入，使得模型能够同时理解文本语义和骨骼拓扑，并将二者融合以控制运动生成。正是这一模块，使模型从“只能操作固定骨架”跃迁为“理解骨架拓扑本身”的范式转变。

## 核心创新

本工作提出**拓扑无关的文本驱动动物运动生成框架**，其核心创新围绕一个关键因果机制展开：**拓扑感知的骨骼嵌入模块（Topology-aware Skeleton Embedding Module）**。该模块利用图Transformer将任意骨骼的几何与结构关系编码为统一的条件嵌入，使模型能够理解并融合文本语义与骨骼拓扑，从而控制运动生成。消融实验证实，去除该模块后FID从0.044飙升至0.097（性能下降54.6%），证明它是保证生成质量与跨语义一致性的决定性组件（Table 3）。

### 方法谱系与知识库定位

现有文本驱动运动生成方法（如 **MoMask**（Guo et al., CVPR 2024）、**MMM**（Pinyoanuntapong et al., CVPR 2024））普遍依赖固定骨骼模板（如SMPL），无法泛化到任意拓扑的骨架。本工作在此基础上进行了三个关键槽位的替换与升级：

| 变更槽位 | 基线方案 | 本方案 | 证据锚点 |
|---------|---------|--------|---------|
| **骨骼条件表达** | 固定模板（如SMPL）或预定义关节配置 | 拓扑感知图Transformer编码任意骨骼为条件嵌入（包含图距离/关系偏置） | Sec. 4.2.1 |
| **运动离散化** | 固定关节数量的VQ-VAE | 支持可变关节数填充与掩码的**广义残差VQ-VAE** | Sec. 4.1 |
| **多模态条件融合** | 简单拼接或仅使用文本嵌入 | 多尺度文本嵌入与骨骼嵌入通过MLP融合，分别注入掩码Transformer与残差Transformer | Sec. 4.2.2 |

### 核心机制解析

**1. 广义残差VQ-VAE（Generalized Motion Residual VQ-VAE）**

为处理异构骨骼拓扑中可变关节数量的问题，本方案将标准残差VQ-VAE扩展为广义形式。其核心策略是引入关节级填充与掩码机制：对于关节数少于最大值的运动序列，用零填充至统一维度，并通过二值掩码 $\mathbf{M}$ 标记有效关节位置。残差量化过程遵循递推关系：

$$\mathbf{R}_{l+1} = \mathbf{R}_l - \hat{\mathbf{R}}_l, \quad \hat{\mathbf{R}}_l = Q_l(\mathbf{R}_l), \quad \mathbf{R}_1 = \mathbf{Z}_0$$

训练目标为掩码重建损失与残差承诺损失的联合优化，仅对有效关节计算：

$$\mathcal{L}_{\mathrm{rvq}} = \frac{\sum_{t,j} \mathbf{M}_{t,j} \| \tilde{\mathbf{X}}_{t,j} - \hat{\mathbf{X}}_{t,j} \|_1}{\sum_{t,j} \mathbf{M}_{t,j} + \epsilon} + \beta \sum_{l=1}^{L} \frac{\sum_{t,j} \mathbf{M}_{t,j} \| \mathbf{R}_l - \mathrm{sg}[\hat{\mathbf{R}}_l] \|_2^2}{\sum_{t,j} \mathbf{M}_{t,j} + \epsilon}$$

**2. 拓扑感知骨骼嵌入模块**

该模块是框架的核心创新，将任意骨骼拓扑编码为紧凑的条件嵌入 $\mathbf{f}_{\mathrm{skel}} \in \mathbb{R}^{1 \times d_s}$。其工作流程如下：

- **关节特征投影**：对每个关节的几何特征（位置、方向等）通过小型MLP投影到潜在空间：
  $$\mathbf{H} = f_{\mathrm{MLP}}(\mathbf{J}) = W_2 \mathrm{GELU}(W_1 \mathbf{J} + b_1) + b_2$$

- **图结构注意力偏置**：构建基于图拓扑距离和关系类型的注意力偏置：
  $$\mathbf{B}_{\mathrm{final}} = \mathrm{Emb}_{\mathrm{dist}}(\mathbf{D}) + \mathrm{Emb}_{\mathrm{rel}}(\mathbf{R}) + \mathbf{M}'$$
  其中 $\mathbf{D}$ 为图距离矩阵，$\mathbf{R}$ 为关系类型矩阵，$\mathbf{M}'$ 为空间掩膜。

- **结构感知多头注意力**：将偏置直接注入自注意力logits中：
  $$\mathbf{MHA}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d/H}} + \mathbf{B}_{\mathrm{final}}\right)V$$

- **骨骼嵌入提取**：取出图Transformer输出中CLS token的表示，经投影得到最终骨骼条件嵌入：
  $$\mathbf{f}_{\mathrm{skel}} = W_{\mathrm{out}} \cdot \mathrm{LayerNorm}(\mathbf{Z}_L[0]) + b_{\mathrm{out}}$$

**3. 多模态条件融合与两阶段生成**

文本编码器（基于SigLIP 2）提取多尺度语义嵌入，与骨骼嵌入通过轻量MLP融合为统一条件信号 $f_{\mathrm{cond}} = \mathrm{MLP}([f_{\mathrm{text}}; f_{\mathrm{skel}}])$。生成过程分两阶段进行：掩码Transformer在文本和骨骼条件下通过掩码预测恢复基础层运动token，残差Transformer在此基础上自回归地预测残差量化层token，实现从粗到细的运动生成。

### 关键消融证据

| 消融配置 | FID | 性能变化 | 结论 |
|---------|-----|---------|------|
| 完整模型 | 0.044 | — | 基线性能 |
| 移除拓扑感知骨骼嵌入 | 0.097 | +54.6% 恶化 | 骨骼嵌入是核心因果组件 |
| 移除运动摘要输入 | 0.064 | +31.3% 恶化 | 全局运动上下文有助于时序一致性 |

完整模型同时取得最低FID（0.044）和最高文本-运动检索准确率（R@3 0.877），证实各组件协同有效（Table 3）。

### 局限性

- 当前框架仅针对动物运动设计，无法处理铰接人体或其他复杂角色类型。
- 控制信号仅限于文本和骨骼输入，尚未探索视频等更丰富的模态引导。
- 生成结果在细节和质量上仍不及手工动画，距离生产级应用尚有距离。

## 整体框架

本工作提出一个**拓扑无关的文本驱动动物运动生成框架**，核心目标是：给定任意骨骼拓扑和一段文本描述，生成与该文本语义对齐且符合该骨骼解剖约束的运动序列。框架由两个阶段级联构成，如图3所示。

### 阶段一：广义运动残差VQ‑VAE

第一阶段将任意拓扑的运动序列压缩到统一的离散token空间。由于不同物种的骨骼关节数量差异巨大（例如猫科动物与鸟类），传统固定关节数的VQ‑VAE无法直接应用。为此，作者提出**广义运动残差VQ‑VAE**（Generalized Motion Residual VQ‑VAE），其关键设计包括：

1. **关节级填充与掩码**：将所有运动序列填充到统一的最大关节数 $K_{\max}$，同时维护一个二值掩码 $\mathbf{M}$ 标记有效关节位置。后续所有损失计算和注意力操作仅作用于有效关节。
2. **残差量化**：采用 $L$ 层残差向量量化（Residual VQ），逐层细化量化残差：
   $$\mathbf{R}_{l+1} = \mathbf{R}_l - \hat{\mathbf{R}}_l, \quad \hat{\mathbf{R}}_l = Q_l(\mathbf{R}_l), \quad \mathbf{R}_1 = \mathbf{Z}_0$$
   其中 $\mathbf{Z}_0$ 为编码器输出的连续潜在表示，$Q_l$ 为第 $l$ 层量化器。最终离散表示为各层近似值之和。
3. **掩码重建与承诺损失**：训练目标联合优化重建质量和码本使用，仅对有效关节计算：
   $$\mathcal{L}_{\mathrm{rvq}} = \frac{\sum_{t,j} \mathbf{M}_{t,j} \| \tilde{\mathbf{X}}_{t,j} - \hat{\mathbf{X}}_{t,j} \|_1}{\sum_{t,j} \mathbf{M}_{t,j} + \epsilon} + \beta \sum_{l=1}^{L} \frac{\sum_{t,j} \mathbf{M}_{t,j} \| \mathbf{R}_l - \mathrm{sg}[\hat{\mathbf{R}}_l] \|_2^2}{\sum_{t,j} \mathbf{M}_{t,j} + \epsilon}$$

该阶段输出基础层运动token（第一层量化索引）和残差层token（后续各层索引），作为第二阶段的条件生成目标。

### 阶段二：文本与骨骼条件化的掩码自回归生成

第二阶段在文本和骨骼的双重条件下生成离散运动token序列，整体流程包含三个核心模块：

**（1）拓扑感知骨骼嵌入模块（Topology‑aware Skeleton Embedding Module）**

该模块是整个框架的**因果调节旋钮**——它将任意骨骼的几何与结构信息编码为统一的条件嵌入 $\mathbf{f}_{\mathrm{skel}} \in \mathbb{R}^{1 \times d_s}$。具体而言（图4）：

- 对每个关节提取局部几何特征（位置、速度、骨骼长度等），经小型MLP投影到潜在空间：
  $$\mathbf{H} = f_{\mathrm{MLP}}(\mathbf{J}) = W_2 \mathrm{GELU}(W_1 \mathbf{J} + b_1) + b_2$$
- 在图Transformer中，基于骨架拓扑构建**图距离嵌入**和**关系类型嵌入**（父子/兄弟/无连接），组合为注意力偏置：
  $$\mathbf{B}_{\mathrm{final}} = \mathrm{Emb}_{\mathrm{dist}}(\mathbf{D}) + \mathrm{Emb}_{\mathrm{rel}}(\mathbf{R}) + \mathbf{M}'$$
  该偏置直接注入多头自注意力：
  $$\mathbf{MHA}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d/H}} + \mathbf{B}_{\mathrm{final}}\right)V$$
- 图Transformer输出的CLS token经LayerNorm和线性投影，得到最终的骨骼条件嵌入：
  $$\mathbf{f}_{\mathrm{skel}} = W_{\mathrm{out}} \cdot \mathrm{LayerNorm}(\mathbf{Z}_L[0]) + b_{\mathrm{out}}$$

**（2）文本编码器**

采用基于SigLIP 2的多尺度文本编码器，从文本提示中提取层次化语义嵌入 $\mathbf{f}_{\mathrm{text}}$，覆盖从粗粒度动作类别到细粒度运动细节的描述。

**（3）条件融合与两阶段Transformer生成**

文本嵌入与骨骼嵌入通过轻量MLP融合为统一条件信号 $\mathbf{f}_{\mathrm{cond}}$，分别注入两个Transformer：

- **掩码Transformer**：以 $\mathbf{f}_{\mathrm{cond}}$ 为条件，通过迭代掩码预测恢复基础层运动token。该阶段采用随机掩码策略，在推理时逐步去噪生成完整的基础层序列。
- **残差Transformer**：在已生成的基础层token之上，自回归地预测各残差量化层的token索引，逐层细化运动细节。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 广义运动残差VQ‑VAE | 任意拓扑的运动序列 $\mathbf{X}$（含掩码 $\mathbf{M}$） | 基础层token $T_1$ + 残差层token $\{T_2, \dots, T_L\}$ |
| 骨骼嵌入模块 | 任意骨骼的关节特征 $\mathbf{J}$ + 拓扑关系 | 骨骼条件嵌入 $\mathbf{f}_{\mathrm{skel}}$ |
| 文本编码器 | 文本描述 | 多尺度文本嵌入 $\mathbf{f}_{\mathrm{text}}$ |
| 掩码Transformer | $\mathbf{f}_{\mathrm{cond}}$ + 随机掩码token | 预测的基础层token序列 |
| 残差Transformer | $\mathbf{f}_{\mathrm{cond}}$ + 基础层token | 残差层token序列 |
| 解码器 | 所有量化层token + 骨骼掩码 | 重建运动序列 $\hat{\mathbf{X}}$ |

该框架的**核心洞察**在于：通过图距离和关系类型构建的注意力偏置，使模型能够“理解”任意骨架的拓扑结构，并将其与文本语义在统一的嵌入空间中融合，从而在掩码自回归范式下实现真正的拓扑无关运动生成。消融实验（Table 3）强有力地证实了这一点——移除骨骼嵌入模块后FID从0.044飙升至0.097（性能下降54.6%），而完整模型在所有文本-运动对齐指标上均达到最优。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our pipeline. Our network operates in two main stages: In the first stage, we extend the residual VQ-VAE into a generalized formulation capable of handling motion sequences from arbitrary skeletal topologies. In the second stage, we introduce text prompts and target skeletons as joint conditioning signals. We design a topology-aware skeleton embedding module that extracts both spatial geometry and structural topology from any given skeleton. These features are then fused with text embeddings and fed into a two-stage Transformer to achieve generalized conditional motion generation across diverse species and skeletal structures*

## 核心模块与公式推导

### 总体管线

本方法采用两阶段生成范式（Figure 3）。第一阶段将任意骨骼拓扑的运动序列压缩到离散 token 空间；第二阶段以文本描述和目标骨骼为联合条件，通过掩码自回归 Transformer 生成运动 token，再经解码器还原为连续运动。其核心创新在于 **广义残差 VQ-VAE** 与 **拓扑感知骨骼嵌入模块** 的协同设计。

---

### 广义运动残差 VQ-VAE

传统 VQ-VAE 要求固定关节数量，无法处理异构骨骼。本工作提出 **广义运动残差 VQ-VAE**，通过关节级填充与掩码机制支持可变拓扑。

**残差量化过程**：给定编码器输出 $\mathbf{Z}_0$，逐层量化残差：

$$\mathbf{R}_{l+1} = \mathbf{R}_l - \hat{\mathbf{R}}_l, \quad \hat{\mathbf{R}}_l = Q_l(\mathbf{R}_l), \quad \mathbf{R}_1 = \mathbf{Z}_0$$

其中 $Q_l$ 为第 $l$ 层的矢量量化器，$\hat{\mathbf{R}}_l$ 为该层的量化近似。最终量化表示为各层近似之和 $\sum_{l=1}^{L} \hat{\mathbf{R}}_l$。此残差结构使模型能够渐进细化运动细节，同时将连续运动压缩为多层离散 token。

**掩码训练目标**：仅对有效关节计算损失，忽略填充位置：

$$\mathcal{L}_{\mathrm{rvq}} = \frac{\sum_{t,j} \mathbf{M}_{t,j} \| \tilde{\mathbf{X}}_{t,j} - \hat{\mathbf{X}}_{t,j} \|_1}{\sum_{t,j} \mathbf{M}_{t,j} + \epsilon} + \beta \sum_{l=1}^{L} \frac{\sum_{t,j} \mathbf{M}_{t,j} \| \mathbf{R}_l - \mathrm{sg}[\hat{\mathbf{R}}_l] \|_2^2}{\sum_{t,j} \mathbf{M}_{t,j} + \epsilon}$$

其中 $\mathbf{M}_{t,j}$ 为二值掩膜（有效关节为 1，填充为 0），$\tilde{\mathbf{X}}$ 为解码器重建运动，$\hat{\mathbf{X}}$ 为原始运动，$\mathrm{sg}[\cdot]$ 为梯度截断算子。第一项为掩码 L1 重建损失，第二项为残差承诺损失，$\beta$ 平衡两项权重。该设计使同一 VQ-VAE 能处理从猫到鹤等关节数差异巨大的骨架。

---

### 拓扑感知骨骼嵌入模块

该模块（Figure 4）是本方法实现拓扑无关生成的核心因果旋钮——消融实验表明移除它使 FID 从 0.044 飙升至 0.097（Table 3）。其设计目标是将任意骨骼的几何与结构信息编码为统一的条件嵌入 $\mathbf{f}_{\mathrm{skel}} \in \mathbb{R}^{1 \times d_s}$。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/005_Figure_4.jpg]]
*Figure 4: Overview of the topology-aware skeleton embedding module*

**关节特征投影**：每个关节 $i$ 的输入特征 $\mathbf{J}_i$ 包含 3D 位置、局部旋转等几何信息，通过小型 MLP 投影到潜在空间：

$$\mathbf{H} = f_{\mathrm{MLP}}(\mathbf{J}) = W_2 \mathrm{GELU}(W_1 \mathbf{J} + b_1) + b_2$$

随后在序列前端拼接可学习的全局 CLS token，形成图 Transformer 的输入 $\mathbf{Z}_0 = [\mathbf{h}_{\mathrm{cls}}, \mathbf{H}]^{\top} \in \mathbb{R}^{(K+1) \times d}$，其中 $K$ 为关节数。

**图感知注意力偏置**：这是模块理解骨骼拓扑的关键机制。基于骨架的图距离矩阵 $\mathbf{D}$ 和关系类型矩阵 $\mathbf{R}$（如父子、兄弟关系），构造结构化注意力偏置：

$$\mathbf{B}_{\mathrm{final}} = \mathrm{Emb}_{\mathrm{dist}}(\mathbf{D}) + \mathrm{Emb}_{\mathrm{rel}}(\mathbf{R}) + \mathbf{M}'$$

其中 $\mathrm{Emb}_{\mathrm{dist}}$ 和 $\mathrm{Emb}_{\mathrm{rel}}$ 分别为距离嵌入和关系类型嵌入，$\mathbf{M}'$ 为空间掩膜。该偏置直接注入多头自注意力：

$$\mathbf{MHA}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d/H}} + \mathbf{B}_{\mathrm{final}}\right)V$$

这一设计使注意力权重不仅依赖特征相似度，还受骨架拓扑结构约束——拓扑上邻近的关节获得更高的注意力权重，远距离关节则被抑制，从而隐式编码了骨骼的层次化运动学关系。

**骨骼嵌入输出**：经过 $L$ 层图 Transformer 后，取出 CLS token 的上下文表示并投影：

$$\mathbf{f}_{\mathrm{skel}} = W_{\mathrm{out}} \cdot \mathrm{LayerNorm}(\mathbf{Z}_L[0]) + b_{\mathrm{out}}$$

此嵌入汇聚了全局骨架信息，作为后续运动生成的条件信号。

---

### 条件融合与生成

文本侧采用基于 SigLIP 2 的编码器提取多尺度语义嵌入 $\mathbf{f}_{\mathrm{text}}$。文本与骨骼嵌入通过轻量 MLP 融合为统一条件：

$$\mathbf{f}_{\mathrm{cond}} = \mathrm{MLP}([\mathbf{f}_{\mathrm{text}}; \mathbf{f}_{\mathrm{skel}}])$$

该条件分别注入 **掩码 Transformer**（预测基础层运动 token）和 **残差 Transformer**（自回归预测残差层 token）。两阶段解码使得模型先生成运动的大致轮廓，再逐步填充细节，与残差 VQ-VAE 的层级结构形成闭环。

---

### 关键公式速查

| 公式 | 变量含义 | 核心作用 |
|------|----------|----------|
| $\mathbf{R}_{l+1} = \mathbf{R}_l - \hat{\mathbf{R}}_l$ | $\mathbf{R}_l$：第 $l$ 层残差；$\hat{\mathbf{R}}_l$：量化近似 | 残差量化迭代 |
| $\mathcal{L}_{\mathrm{rvq}}$ | $\mathbf{M}_{t,j}$：有效关节掩膜；$\tilde{\mathbf{X}}$：重建运动 | 掩码重建 + 承诺损失 |
| $\mathbf{B}_{\mathrm{final}}$ | $\mathbf{D}$：图距离矩阵；$\mathbf{R}$：关系类型矩阵 | 图拓扑注意力偏置 |
| $\mathrm{softmax}(\frac{QK^{\top}}{\sqrt{d/H}} + \mathbf{B}_{\mathrm{final}})V$ | $Q,K,V$：查询/键/值；$H$：注意力头数 | 拓扑感知自注意力 |
| $\mathbf{f}_{\mathrm{skel}} = W_{\mathrm{out}} \cdot \mathrm{LayerNorm}(\mathbf{Z}_L[0]) + b_{\mathrm{out}}$ | $\mathbf{Z}_L[0]$：CLS token 最终表示 | 骨骼条件嵌入输出 |

## 实验与分析

### 实验设置

论文构建了大规模异构动物运动数据集 **OmniZoo**，涵盖多种物种与骨骼拓扑，按 0.95:0.05 划分训练/测试集。评估指标包括生成质量的 **FID**（Fréchet Inception Distance）、文本-运动对齐的 **MatchingScore** 与检索准确率 **R@k**。广义运动残差 VQ-VAE 采用 6 层残差量化，码本维度 512，时间下采样因子 2；掩码 Transformer 与残差 Transformer 均使用 8 层、4 注意力头，AdamW 优化器学习率 $1\times10^{-3}$，batch size 256，训练 100 个 epoch。

### 主实验结果

在 OmniZoo 测试集上，完整模型取得了最优的生成质量与语义对齐性能（Table 2）。具体而言，FID 降至 **0.044**，相较于最强基线 **MoMask**（Guo et al., CVPR 2024）的 0.085 降低 **48.2%**；文本-运动检索准确率 R@1 达到 **0.621**，较 MoMask 的 0.504 提升 **23.2%**。MatchingScore 降至 1.072，优于所有对比方法。定性对比（Figure 5）显示，模型在异构骨骼（如猫鼬、食火鸡）上生成的运动既忠实于文本语义，又符合各自骨骼的解剖约束，而基线方法往往产生关节扭曲或语义错位的运动。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of text-to-motion generation performance among different methods*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of motion generation results on our testset. Our model generates motions faithful to both the text prompt and the skeletal anatomy for heterogeneous skeletons, outperforming all baselines*

### 消融实验

消融实验（Table 3）严格验证了各核心组件的因果贡献：

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/010_Table_3.jpg]]
*Table 3: Ablation study on the testset*

- **拓扑感知骨骼嵌入模块**是保证生成质量的关键瓶颈。移除该模块后，FID 从 0.044 飙升至 0.097，性能下降 **54.6%**，同时 MatchingScore 和检索准确率均大幅恶化，证实骨骼拓扑信息对跨物种运动生成不可或缺。
- **运动摘要输入**对时序一致性有显著影响。去除运动摘要后 FID 升至 0.064，性能下降 **31.3%**，表明全局运动上下文有助于模型理解动作的完整时序结构。
- 完整模型在所有指标上均达到最优（FID 0.044，R@3 0.877），验证了广义残差 VQ-VAE、拓扑感知骨骼嵌入与多尺度文本融合三者间的协同效应。

### 跨物种泛化与真实场景验证

模型展现出强大的跨物种运动迁移能力（Figure 6）。对于同一文本提示“scanning surroundings”，模型能为拓扑结构迥异的猫鼬与食火鸡骨骼分别生成生物力学合理的运动——猫鼬呈现直立扫视姿态，食火鸡则表现为颈部转动与身体配合。在真实场景中（Figure 7），模型成功驱动从野外图像重建的动物骨骼：猎鹰执行空中机动并伴随动态翅膀运动，马匹完成小跑步态且四肢协调，验证了方法对真实世界骨骼噪声的鲁棒性。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/008_Figure_6.jpg]]
*Figure 6: Text-driven motion transfer for heterogeneous skeletons. Our method generates biomechanically plausible motions for topologically distinct skeletons (e.g., meerkat and cassowary) from a single text prompt (”scanning surroundings”)*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/009_Figure_7.jpg]]
*Figure 7: Text-to-motion generation on real-world animals. Our method successfully generates plausible motions for animals reconstructed from in-the-wild images. Top: A falcon performing aerial maneuvers with dynamic wing movements. Bottom: A horse executing a trotting gait with coordinated leg motion*

### 失败模式与局限性

尽管整体性能优异，论文指出以下局限：
1. 当前框架**专门针对动物运动设计**，无法处理铰接人体或其他复杂角色类型，泛化边界受限于训练物种分布。
2. 控制信号**仅限于文本和骨骼输入**，尚未探索视频、音频等更丰富的模态引导，限制了运动编辑与风格迁移的灵活性。
3. 生成结果在**细节和质量上仍不及手工动画**，距离生产级应用尚有差距，尤其在快速动作或罕见姿态下可能出现关节抖动或不自然形变。

### 公平性说明

论文未显式报告不同物种间的性能偏差或公平性测试。训练/测试集按 0.95:0.05 随机划分，未进行物种分层采样，因此少数物种的生成质量可能存在系统性差异，这一点需要读者在跨物种应用中自行验证。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/001_Figure_1.jpg]]
*Figure 1: Given an arbitrary skeletal topology and a corresponding text prompt, our method drives the skeleton to produce realistic, highquality motions that align with the textual description*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2512_10352/figures/002_Table_1.jpg]]
*Table 1: Comparison with existing animal motion datasets*

## 方法谱系与知识库定位

### 核心瓶颈与因果杠杆

现有文本驱动运动生成方法普遍依赖固定骨骼模板（如人体运动生成中的 SMPL 模型），其运动表示空间的维度由预定义关节数量决定，无法泛化到任意拓扑的骨架结构。同时，大规模异构动物运动数据的缺乏进一步限制了跨物种运动生成的统一建模。本文的核心因果杠杆是**拓扑感知的骨骼嵌入模块**（Topology-aware Skeleton Embedding Module），该模块利用图 Transformer 将任意骨骼的几何与结构关系编码为统一的条件嵌入，使模型能够同时理解文本语义与骨骼拓扑，从而在掩码自回归框架中实现跨物种的文本驱动运动生成。

### 方法继承与差异化

本文方法在以下关键维度上对现有工作进行了继承与改造：

| 方法维度 | 基线方法代表 | 基线方案 | 本文方案 | 差异化本质 |
|---------|------------|---------|---------|-----------|
| 骨骼条件表达 | **MoMask** (Guo et al., CVPR 2024) / **MMM** (Pinyoanuntapong et al., CVPR 2024) | 固定模板（如 SMPL）或预定义关节配置 | 拓扑感知图 Transformer 编码任意骨骼为条件嵌入（含图距离/关系偏置） | 从“固定拓扑适配”转向“拓扑无关的骨骼理解” |
| 运动离散化 | MoMask 等残差 VQ-VAE | 固定关节数量的 VQ-VAE | 支持可变关节数填充与掩码的广义残差 VQ-VAE | 引入关节级掩码机制，仅对有效关节计算损失 |
| 多模态条件融合 | 主流文本-运动方法 | 简单拼接或仅使用文本嵌入 | 多尺度文本嵌入与骨骼嵌入通过 MLP 融合，分别注入掩码 Transformer 与残差 Transformer | 文本-骨骼联合条件注入双阶段生成器，实现跨模态对齐 |

**MoMask** (Guo et al., CVPR 2024) 是本文最直接的方法参照对象。MoMask 提出了基于残差 VQ-VAE 的掩码运动生成范式，在人体运动生成上取得了优异性能，但其运动表示和骨骼编码均针对固定人体拓扑设计。本文沿用了 MoMask 的“残差量化 + 掩码预测”框架，但将其**广义化**为可处理任意关节数量和骨骼结构的版本，并在条件注入端引入了拓扑感知的骨骼编码器，从而将适用范围从单一人体扩展至跨物种动物运动生成。

**MMM** (Pinyoanuntapong et al., CVPR 2024) 同样属于文本驱动运动生成的前沿工作，但同样受限于固定骨骼模板。本文与 MMM 的核心差异在于：MMM 的条件融合策略未考虑骨骼拓扑的结构信息，而本文通过图注意力偏置显式建模关节间的拓扑距离和关系类型。

### 适用边界

1. **物种范围**：当前模型仅针对动物运动设计，训练数据覆盖猫、狗、马、鸟等多种动物类别，但无法处理铰接人体或其它复杂角色类型（如机器人、幻想生物）。
2. **控制模态**：控制信号仅限于文本描述和骨骼输入，尚未探索视频、音频或交互式控制等更丰富的模态引导。
3. **运动质量**：生成结果在细节和质量上仍不及手工动画，在精细的手指/爪部运动、复杂物理交互（如捕食、攀爬）等场景中距离生产级应用尚有距离。
4. **数据依赖**：模型性能受限于训练数据的物种覆盖度和运动多样性，对于训练集中未出现或出现频次极低的骨骼拓扑，生成质量可能下降（论文未显式报告不同物种间的性能偏差）。

### 局限与开放问题

**已明确的局限**：
- 模型仅针对动物运动设计，无法处理铰接人体或其它复杂角色类型。
- 控制信号仅限于文本和骨骼输入，尚未探索视频等更丰富的模态引导。
- 生成结果在细节和质量上仍不及手工动画，距离生产级应用尚有距离。

**开放研究问题**：
1. **角色泛化**：如何将框架扩展至包括人体在内的任意铰接角色，同时保持多模态可控性？这需要构建覆盖更广泛拓扑类型的统一运动数据集，并设计更具泛化能力的骨骼编码策略。
2. **多模态控制**：能否引入视频条件（如参考运动视频）以实现更精细的运动编辑和风格迁移？视频输入可提供时序运动先验，有望弥补纯文本描述在运动细节上的信息缺失。
3. **物理合理性增强**：如何结合物理仿真或强化学习提升运动质量与真实感，达到生产级水平？当前纯数据驱动的方法在物理合理性（如足部滑动、关节超限）方面仍存在不足，引入物理约束可能是解决该问题的关键路径。
4. **公平性与偏差**：论文未显式报告不同物种间的性能偏差或公平性测试，仅按 0.95:0.05 划分训练/测试集。未来工作需系统评估模型在不同物种、不同骨骼复杂度下的性能分布，以识别并缓解潜在的长尾问题。

### 知识库定位

本文位于**文本驱动运动生成**与**跨形态运动建模**的交叉点。在文本驱动运动生成谱系中，它继承了 MoMask 的掩码自回归范式，但通过拓扑感知骨骼嵌入和广义 VQ-VAE 突破了固定拓扑限制，是该方向从“单一角色”迈向“多角色统一建模”的关键一步。在跨形态运动建模方面，本文的骨骼图 Transformer 编码策略与图神经网络在骨架动作识别中的工作形成呼应，但其创新在于将结构编码作为生成条件而非分类特征，为拓扑无关的运动生成提供了可复用的技术组件。

## 原文 PDF

![[paperPDFs/arxiv_2025/Topology_Agnostic_Animal_Motion_Generation_from_Text_Prompt.pdf]]
---
title: "FreeMotion: A Unified Framework for Number-free Text-to-Motion Synthesis"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis.pdf
aliases:
- FreeMotion
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将多人运动联合分布通过条件概率公式分解为条件分布乘积，从而将多人运动生成转化为递归的条件单人运动生成。
primary_logic: 通过解耦生成模块（单人运动生成）与交互模块（基于全局自注意力任意数量条件运动注入），并采用两阶段训练，实现人数无关的运动生成及灵活的空间控制，使模型仅在两人数据训练即可推理多人运动。
claims:
- 联合分布分解数学公式将多人生成转化为递归条件生成
- 在单人运动生成上FID显著优于InterGen*
- 在双人运动生成上FID达到6.740、R Precision Top1达到0.326，优于所有基线
- 交互模块使用全局自注意力实现长度无关的条件运动处理
---

# FreeMotion: A Unified Framework for Number-free Text-to-Motion Synthesis

> [!tip] 核心洞察
> 通过解耦生成模块（单人运动生成）与交互模块（基于全局自注意力任意数量条件运动注入），并采用两阶段训练，实现人数无关的运动生成及灵活的空间控制，使模型仅在两人数据训练即可推理多人运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | FreeMotion：一个面向任意人数文本驱动动作合成的统一框架 |
| 英文题名 | FreeMotion: A Unified Framework for Number-free Text-to-Motion Synthesis |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://VankouF.github.io/FreeMotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FreeMotion |
| Dataset | InterHuman test set |

> [!tip] 效果简介
> - InterHuman test set (re-annotated single-person text) 上，FID 12.975±.171 vs 23.415±.220 (InterGen*) (-10.440 (lower is better))。
> - InterHuman test set (two-person motion) 上，FID 6.740±.130 vs InterGen* (value not explicitly given, but claimed outperformed) (—)。

## 概述

### 1. 问题与瓶颈

现有文本驱动人体运动生成方法——无论是基于扩散的单人模型（如 **MDM** (Tevet et al., arXiv 2022)、**MLD** (Chen et al., CVPR 2023)、**ReMoDiffuse** (Zhang et al., arXiv 2023)），还是面向双人交互的 **InterGen** (Liang et al., arXiv 2023)——均针对固定人数设计。单人模型无法建模多人交互，双人模型则无法生成单人或三人以上运动，且其空间控制机制难以迁移至多人场景。这一“人数绑定”的根本瓶颈在于：现有范式直接预测固定人数的联合运动分布，缺乏对可变数量个体的统一建模能力。

### 2. 核心思路

FreeMotion 提出了一种**人数无关的递归生成范式**。其核心洞察是将多人运动的联合分布通过条件概率公式分解为条件分布的乘积：

$$p(\mathbf{x}^{1},...,\mathbf{x}^{n}) = p(\mathbf{x}^{1}) \prod_{i=1}^{n-1} p(\mathbf{x}^{i+1}|\mathbf{x}^{i},...,\mathbf{x}^{1})$$

这一分解将多人运动生成转化为**序列化的条件单人运动生成**：首先生成第一个人的运动，再以上一个人的运动为条件递归生成后续个体。实现上，FreeMotion 将建模过程解耦为两个模块——负责单人运动生成的**生成模块**（Generation Module）与负责条件注入的**交互模块**（Interaction Module）。交互模块完全基于全局自注意力，能够处理任意数量的条件运动，使模型仅在双人数据上训练即可推理三人及以上运动。训练采用两阶段策略：先训练生成模块，再冻结其参数训练交互模块，确保各模块充分利用数据信息。

### 3. 方法定位

在方法谱系中，FreeMotion 处于**条件扩散模型**与**解耦架构设计**的交汇点。与 InterGen 的共享权重交叉注意力范式不同，FreeMotion 将条件建模从生成主干中分离，通过类似 ControlNet 的交互模块注入条件信号。与 **ComMDM** (Shafir et al., arXiv 2023) 等基于预训练模型的少样本多人生成方案相比，FreeMotion 无需复杂的后处理或组合优化，通过统一的端到端框架直接支持任意人数。这一设计使其同时覆盖单人、双人及多人运动生成，并集成了显式与隐式空间控制信号，实现了灵活的全局位置控制。

### 4. 主要结果

在 InterHuman 测试集上，FreeMotion 在双人运动生成任务中取得了 **FID 6.740** 和 **R Precision Top1 0.326**，优于所有基线方法。在单人运动生成上，FreeMotion 的 FID 达到 **12.975**，相比为支持单人生成而修改的 InterGen*（FID 23.415）有显著提升。消融实验表明，去除交互模块后双人 FID 从 6.740 升至 10.749，验证了解耦设计的有效性；全局自注意力交互块使模型能够支持三人及以上的运动生成。定性结果进一步展示了 FreeMotion 在复杂文本理解、交互协调性以及可控空间轨迹方面的优势。

## 背景与动机

### 问题背景

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型在该领域取得了显著进展，代表性工作包括基于Transformer的单人扩散模型**MDM**（Tevet et al., arXiv 2022）、基于潜在扩散的**MLD**（Chen et al., CVPR 2023）以及检索增强的**ReMoDiffuse**（Zhang et al., arXiv 2023）等。然而，这些方法均聚焦于单人生成场景，无法处理多人交互运动。

在多人运动生成方面，**InterGen**（Liang et al., arXiv 2023）通过共享权重和交叉注意力机制建模双人交互，**ComMDM**（Shafir et al., arXiv 2023）则基于预训练单人模型进行少样本多人生成。但现有方法存在一个根本性局限：它们均针对固定人数（单人/双人）设计，直接预测固定人数的联合运动分布，无法同时支持单人和多人场景，更难以扩展至任意人数。此外，多人运动的空间控制能力也难以从单人场景迁移。

### 核心瓶颈

现有方法的根本瓶颈在于**生成范式的固定性**：它们将多人运动生成建模为直接预测联合分布 $p(\mathbf{x}^1, ..., \mathbf{x}^n)$ 的过程，导致模型结构与人数强耦合。当人数变化时，网络输入维度和交互建模方式均需重新设计，无法实现人数无关的统一框架。这带来三个关键缺口：

1. **人数不可扩展**：模型仅在特定人数数据上训练，无法泛化至训练时未见的人数配置。
2. **单人多人生成割裂**：单人和多人运动生成需依赖不同模型或对模型进行特殊修改（如InterGen*在训练中以10%概率将cross-attention置零来支持单人生成），缺乏统一架构。
3. **空间控制难以统一**：多人场景下的全局空间控制（如指定每个人的运动轨迹）缺乏灵活、可泛化的机制。

### 本文动机

针对上述瓶颈，FreeMotion的动机源于一个关键的数学洞察：通过条件概率公式，多人运动的联合分布可以分解为条件分布的乘积：

$$p(\mathbf{x}^{1},...,\mathbf{x}^{n}) = p(\mathbf{x}^{1}) \prod_{i=1}^{n-1} p(\mathbf{x}^{i+1}|\mathbf{x}^{i},...,\mathbf{x}^{1})$$

这一分解将多人运动生成转化为递归的条件单人生成过程——先生成第一人的运动，再以前面所有人的运动为条件生成下一人的运动，如此递归直至完成。基于这一洞察，FreeMotion旨在设计一个**人数无关的统一框架**，通过解耦的生成模块与交互模块，使得模型仅在双人数据上训练即可推理任意人数的运动，并支持灵活的空间控制。

## 核心创新

FreeMotion 的核心创新在于将**人数无关的运动生成**问题转化为一个**递归的条件单人运动生成**过程。与现有方法直接对固定人数的联合运动分布建模不同，FreeMotion 通过以下三个关键设计实现突破：

### 1. 范式转换：从联合分布到条件分解

现有方法（如 InterGen、MDM）均针对固定人数设计，无法同时支持单人和多人场景。FreeMotion 将多人运动的联合分布通过条件概率公式分解为条件分布的乘积：

$$p(\mathbf{x}^{1},...,\mathbf{x}^{n}) = p(\mathbf{x}^{1}) \prod_{i=1}^{n-1} p(\mathbf{x}^{i+1}|\mathbf{x}^{i},...,\mathbf{x}^{1})$$

这一分解将多人运动生成转化为递归的条件单人运动生成：先生成第一个人的运动，再以前面所有人的运动为条件生成下一个人的运动。这使得模型**仅在双人数据上训练即可推理任意人数**的运动（Figure 1 展示了 1-4 人的生成结果）。

### 2. 架构解耦：生成模块 + 交互模块

FreeMotion 将建模过程解耦为两个独立模块（Figure 2）：

- **生成模块（Generation Module）**：基于 Transformer 的单人运动扩散网络，负责根据文本提示生成多样化的单人运动。该模块本身即可独立完成单人生成任务。
- **交互模块（Interaction Module）**：类似 ControlNet 的设计，通过多个基于**全局自注意力**的交互块将条件运动信息注入生成过程。全局自注意力的设计使其能够处理**任意数量**的条件运动，这是支持人数无关生成的关键。

交互块的计算方式为：

$$\mathbf{h}_t^{1,k}, \mathbf{h}^{2,k}, ..., \mathbf{h}^{N,k} = SA(SA(\mathbf{h}_t^{1,k-1}), Mask(\mathbf{h}^{2,k-1}, ..., \mathbf{h}^{N,k-1}))$$

其中对噪声运动特征和条件运动特征分别进行自注意力操作后融合，实现交互建模。

### 3. 两阶段训练策略

FreeMotion 采用两阶段训练，确保各模块能力的独立培养：

- **第一阶段**：仅训练生成模块，使用 LLM（GPT）将多人交互描述拆分为独立的单人动作描述，训练单人运动生成能力。损失函数为：

$$\mathcal{L}_1 = \mathcal{L}_{rec} + \lambda_1 \mathcal{L}_{foot} + \lambda_2 \mathcal{L}_{vel} + \lambda_3 \mathcal{L}_{bl}$$

- **第二阶段**：冻结生成模块参数，仅训练交互模块，使用原始交互描述学习条件运动生成。损失函数增加掩蔽关节距离图损失：

$$\mathcal{L}_2 = \mathcal{L}_{rec} + \lambda_1 \mathcal{L}_{foot} + \lambda_2 \mathcal{L}_{vel} + \lambda_3 \mathcal{L}_{bl} + \lambda_4 \mathcal{L}_{dm}$$

消融实验（Table 3）验证了这一设计的有效性：引入交互描述对 FreeMotion 有益（FID 下降），但对单独使用生成模块（GM）反而有害（FID 上升），证明两阶段设计避免了训练冲突。

### 4. 空间控制迁移

FreeMotion 进一步将空间控制能力从单人扩展至多人，通过显式引导（L2 梯度引导）和隐式引导（线性层注入）两种方式实现精确的多人全局位置控制：

$$\mathbf{x}_t = \mathbf{x}_t - \eta \nabla_{\mathbf{x}_t} \mathbf{d}$$

这使得模型能够根据用户指定的轨迹生成可控的多人运动（Figure 5）。

### 与基线的关键差异总结

| 设计维度 | 基线方法 | FreeMotion |
|---------|---------|-----------|
| 运动生成范式 | 直接预测固定人数的联合运动分布 | 通过条件概率分解实现递归的条件单人运动生成 |
| 条件建模架构 | 使用 cross-attention 或共享权重 | 解耦的生成模块 + 基于全局自注意力的交互模块 |
| 训练策略 | 单阶段端到端训练 | 两阶段训练（先训练生成模块，再冻结后训练交互模块） |
| 文本处理 | 直接使用整段交互描述 | 利用 LLM 拆分为独立单人描述，分别用于各阶段训练 |

这些设计共同使得 FreeMotion 成为首个在文本条件下实现高保真、人数无关的运动生成框架。

## 整体框架

FreeMotion 的核心设计思路是将多人运动联合生成问题转化为**递归的条件单人运动生成**。其数学基础是联合分布的条件概率分解：

$$p(\mathbf{x}^{1},...,\mathbf{x}^{n}) = p(\mathbf{x}^{1}) \prod_{i=1}^{n-1} p(\mathbf{x}^{i+1}|\mathbf{x}^{i},...,\mathbf{x}^{1})$$

这一分解将 $N$ 人运动生成拆解为：首先生成第一人的运动 $\mathbf{x}^{1}$，再以已生成的 $\mathbf{x}^{1}$ 为条件生成 $\mathbf{x}^{2}$，以此类推。整个框架因此被解耦为两个核心模块——**生成模块（Generation Module）** 与**交互模块（Interaction Module）**，并通过两阶段训练策略实现高效学习。

### 模块架构与数据流

**生成模块**是一个基于 Transformer 的单人运动扩散网络，负责根据文本提示生成多样化的单人运动。其输入为带噪运动 $\mathbf{x}_t$ 与文本嵌入，输出为预测的干净运动。文本编码器采用冻结的 CLIP-ViT-L-14 模型提取语义特征并注入生成模块。

**交互模块**的设计灵感来源于 ControlNet，其核心是一组基于**全局自注意力（Global Self-Attention）**的交互块（Interactive Block）。该模块接收两类输入：当前正在去噪的目标运动 $\mathbf{x}_t^{1}$，以及已生成的 $N-1$ 个条件运动 $\mathbf{x}^{2},...,\mathbf{x}^{N}$。二者通过共享线性层映射后，进入 $K$ 个交互块进行特征融合。每个交互块的计算流程为：

$$\mathbf{h}_t^{1,k}, \mathbf{h}^{2,k}, ..., \mathbf{h}^{N,k} = SA(SA(\mathbf{h}_t^{1,k-1}), Mask(\mathbf{h}^{2,k-1}, ..., \mathbf{h}^{N,k-1}))$$

即先对目标运动的隐状态做自注意力，再将其与条件运动的掩码隐状态一同送入第二个自注意力层，实现交互信息的注入。由于全局自注意力天然支持变长序列，该模块可以处理**任意数量**的条件运动，这是 FreeMotion 实现人数无关生成的关键机制。

**空间控制模块**集成显式与隐式两种引导方式。显式引导通过计算目标空间位置与预测关节位置的 $L_2$ 距离梯度，在去噪过程中扰动预测运动：

$$\mathbf{x}_t = \mathbf{x}_t - \eta \nabla_{\mathbf{x}_t} \mathbf{d}$$

隐式引导则通过线性层将空间控制信号直接注入网络，与交互模块协同工作。

### 两阶段训练策略

训练过程被分解为两个阶段，以解耦单人运动生成能力与多人交互能力的学习：

1. **第一阶段**：仅训练生成模块。利用 LLM（GPT）将多人交互描述拆分为独立的单人动作描述，以单人运动数据训练生成模块的基础生成能力。损失函数为：

   $$\mathcal{L}_1 = \mathcal{L}_{rec} + \lambda_1 \mathcal{L}_{foot} + \lambda_2 \mathcal{L}_{vel} + \lambda_3 \mathcal{L}_{bl}$$

   包含重建损失、足部接触损失、速度损失和骨长损失。

2. **第二阶段**：冻结生成模块参数，仅训练交互模块。使用原始交互描述与成对运动数据，学习条件运动注入。损失函数在 $\mathcal{L}_1$ 基础上增加掩蔽关节距离图损失 $\mathcal{L}_{dm}$：

   $$\mathcal{L}_2 = \mathcal{L}_{rec} + \lambda_1 \mathcal{L}_{foot} + \lambda_2 \mathcal{L}_{vel} + \lambda_3 \mathcal{L}_{bl} + \lambda_4 \mathcal{L}_{dm}$$

这种解耦设计使得模型仅在双人运动数据上训练，即可泛化至三人及以上的运动生成——因为交互模块的全局自注意力机制天然不受条件运动数量的限制。

### 推理流程

推理时，FreeMotion 以递归方式生成多人运动：给定文本描述，先生成第一人的运动，再将其作为条件输入交互模块生成第二人的运动，如此迭代直至生成全部 $N$ 人的运动。扩散过程采用 1000 步训练、DDIM 50 步采样的配置。若需空间控制，可在去噪的每一步叠加显式梯度引导信号。

### 补充图表

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/001_Figure_1.jpg]]
*Figure 1: The left shows our model can generate controllable motions for any number (1–4 from the figure) of individuals. Different colors represent the different person’s motion. The right is an illustration of our new paradigm of motion generation, recursive generation, where every single motion is predicted under the condition of the motions generated before. Best viewed in color*

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of FreeMotion, which contains a generation module and an interaction module. Given a text d, our framework can infer a motion*

## 核心模块与公式推导

### 问题形式化：从联合分布到条件分解

FreeMotion 的核心思想是将多人运动生成从“直接预测固定人数的联合运动”转化为“递归的条件单人运动生成”。给定 $N$ 个人的运动序列 $\mathbf{x}^1, \mathbf{x}^2, ..., \mathbf{x}^N$，其联合分布通过条件概率公式分解为：

$$p(\mathbf{x}^{1},...,\mathbf{x}^{n}) = p(\mathbf{x}^{1}) \prod_{i=1}^{n-1} p(\mathbf{x}^{i+1}|\mathbf{x}^{i},...,\mathbf{x}^{1})$$

这一分解的**因果机制**在于：将原本需要一次性建模 $N$ 人联合运动空间的难题，转化为先生成第一人的无条件运动，再以前面生成的所有人运动为条件，递归生成后续每个人的运动。这使得模型在训练时仅需接触双人数据，推理时即可泛化至任意人数。

### 运动表示：非规范空间表征

为保留多人之间的相对空间关系，FreeMotion 采用非规范（non-canonical）运动表示。对于第 $p$ 个人的第 $i$ 帧姿态，其特征向量定义为：

$$x^p(i) = [\mathbf{j}_{pg}, \mathbf{j}_{gv}, \mathbf{j}_r, \mathbf{c}_f]$$

其中：
- $\mathbf{j}_{pg}$：关节的**全局位置**（global joint positions），保留绝对空间坐标；
- $\mathbf{j}_{gv}$：关节的**全局速度**（global velocities）；
- $\mathbf{j}_r$：关节的**局部旋转**（local rotations）；
- $\mathbf{c}_f$：足部接触标签（foot contact），指示脚与地面的接触状态。

该表示的关键优势在于直接编码全局位置信息，使交互模块能够感知不同人物之间的空间关系，而非仅依赖局部姿态特征。

### 扩散模型基础

FreeMotion 基于去噪扩散概率模型（DDPM）框架。正向过程按方差时间表 $\beta_t$ 逐步向原始运动数据 $\mathbf{x}_0$ 添加高斯噪声：

$$q(\mathbf{x}_{1:T}|\mathbf{x}_0) := \prod_{t=1}^T q(\mathbf{x}_t|\mathbf{x}_{t-1}), \quad q(\mathbf{x}_t|\mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$$

训练时使用 1000 个扩散步数，推理时采用 DDIM 采样策略，仅需 50 步即可完成去噪生成。

### 架构解耦：生成模块与交互模块

FreeMotion 将条件运动生成网络解耦为两个独立模块，这是实现“人数无关”生成的核心架构设计。

**生成模块（Generation Module）** 是一个基于 Transformer 的单人运动扩散网络，负责根据文本提示生成多样化的单人运动。其输入为噪声运动 $\mathbf{x}_t^1$ 和文本条件 $d$，输出预测的干净运动 $\hat{\mathbf{x}}_0^1$。文本编码采用冻结的 CLIP-ViT-L-14 模型提取特征后注入网络。

**交互模块（Interaction Module）** 的设计灵感来自 ControlNet，其作用是向生成过程注入条件运动信号。该模块完全基于全局自注意力（global self-attention）构建，包含 $K$ 个交互块（interactive blocks）。第 $k$ 个交互块的计算过程为：

$$\mathbf{h}_t^{1,k}, \mathbf{h}^{2,k}, ..., \mathbf{h}^{N,k} = SA(SA(\mathbf{h}_t^{1,k-1}), Mask(\mathbf{h}^{2,k-1}, ..., \mathbf{h}^{N,k-1}))$$

其中 $\mathbf{h}_t^{1,k-1}$ 是噪声目标运动的隐藏状态，$\mathbf{h}^{2,k-1}, ..., \mathbf{h}^{N,k-1}$ 是 $N-1$ 个条件运动的隐藏状态。计算流程为：
1. 先对噪声目标运动做自注意力；
2. 再与经过 Mask 处理的条件运动特征做第二次自注意力，实现交互信息融合。

**全局自注意力的关键作用**：由于自注意力天然支持变长序列输入，交互模块可以处理任意数量的条件运动，无需针对不同人数修改网络结构。这是 FreeMotion 能够从双人训练泛化至多人推理的架构基础。

### 空间控制模块

为实现多人运动的全局位置控制，FreeMotion 集成了显式与隐式两种空间引导机制。

**显式引导**利用分类器引导（classifier guidance）机制，在去噪过程中通过 $L_2$ 距离的梯度修正预测运动。给定空间目标 $\mathbf{s}$ 和当前预测位置 $\mathbf{x}_t$，在每一步去噪时施加扰动：

$$\mathbf{x}_t = \mathbf{x}_t - \eta \nabla_{\mathbf{x}_t} \mathbf{d}, \quad \mathbf{d} = \|\mathbf{s} - \mathbf{x}_t\|_2$$

其中 $\eta$ 为引导强度。**隐式引导**则通过线性层将空间控制信号直接注入网络特征（如 Figure 2 中红色线条所示），与显式引导互补。

### 两阶段训练策略与损失函数

训练过程分为两个阶段，对应生成模块与交互模块的分离训练。

**第一阶段**：仅训练生成模块，目标是学习高质量的单人运动生成。损失函数为：

$$\mathcal{L}_1 = \mathcal{L}_{rec} + \lambda_1 \mathcal{L}_{foot} + \lambda_2 \mathcal{L}_{vel} + \lambda_3 \mathcal{L}_{bl}$$

其中 $\mathcal{L}_{rec}$ 为重建损失（预测运动与真实运动的差异），$\mathcal{L}_{foot}$ 为足部接触损失，$\mathcal{L}_{vel}$ 为速度损失，$\mathcal{L}_{bl}$ 为骨长约束损失。此阶段利用 LLM（GPT）将多人交互描述拆分为独立的单人动作描述，分别用于训练。

**第二阶段**：冻结生成模块参数，仅训练交互模块。在 $\mathcal{L}_1$ 基础上增加掩蔽关节距离图损失：

$$\mathcal{L}_2 = \mathcal{L}_{rec} + \lambda_1 \mathcal{L}_{foot} + \lambda_2 \mathcal{L}_{vel} + \lambda_3 \mathcal{L}_{bl} + \lambda_4 \mathcal{L}_{dm}$$

$\mathcal{L}_{dm}$ 用于显式建模不同人物关节之间的空间距离关系，是交互建模的关键监督信号。消融实验（Table 3）证实：两阶段设计对 FreeMotion 至关重要——同时引入交互描述（InterDes）对 FreeMotion 有益（FID 下降），但对单独使用生成模块（GM）反而有害（FID 上升），说明交互模块有效吸收了交互信息，而生成模块专注于单人运动质量。

## 实验与分析

### 主实验结果

#### 双人运动生成

FreeMotion在InterHuman测试集上对双人运动生成进行了全面评估，与**InterGen**（Liang et al., arXiv 2023）及其单人生成适配版**InterGen\***、**ComMDM**（Shafir et al., arXiv 2023）等基线进行对比。如Table 1所示，FreeMotion在各项指标上均取得最优结果：

- **FID降至6.740±0.130**，显著优于所有基线方法，表明生成运动的逼真度和分布匹配度最高。
- **R Precision Top1达到0.326±0.003**，说明生成运动与文本描述的语义对齐最为精准。
- 在MModality（运动多样性）指标上也表现优异，验证了模型在保持生成多样性的同时不牺牲质量。

这一结果的核心驱动力来自解耦的生成模块与交互模块设计：生成模块负责高质量单人运动先验，交互模块通过全局自注意力将条件运动信息注入，使双人运动在空间交互和时序协调上均保持一致性。

#### 单人运动生成

为公平评估单人生成能力，作者对InterHuman测试集重新标注了单人文本描述，并与InterGen\*进行对比（Table 2）。FreeMotion的**FID为12.975±0.171**，而InterGen\*为23.415±0.220，**FID降低约10.44**。这表明：

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparisons with InterGen* on our re-annotated text for single motion generation. The manner of evaluation is the same as Tab. 1. Bold indicates the best result*

- 两阶段训练策略使生成模块在单人生成上保持了强大的先验能力。
- InterGen\*虽然在训练时以10%概率将cross-attention置零以适配单人生成，但该修改可能损害了其双人性能，且单人质量仍不及FreeMotion。

### 消融实验

为验证各组件的贡献，作者在双人运动生成设定下进行了消融研究（Table 3）：

**交互模块的必要性。** 去除交互模块仅使用生成模块（GM）时，FID从6.740升至10.749，性能显著下降。这表明仅靠生成模块无法有效建模双人间的空间-时序交互，交互模块的全局自注意力机制是捕获多人协调的关键。

**交互描述（InterDes）的双面效应。** 引入LLM拆分的交互描述对FreeMotion有益（FID↓），但对纯生成模块（GM）反而有害（FID↑）。这一现象验证了两阶段设计的合理性：第一阶段让生成模块专注于单人运动分布学习，第二阶段通过交互模块融合多人条件；若在未解耦的架构中直接注入交互描述，会干扰单人生成先验。

**全局自注意力的扩展性。** 交互块完全基于全局自注意力设计，使其天然支持任意数量的条件运动输入。如论文Section 5.5所述，模型仅在双人数据上训练即可推理三人及以上运动，无需修改架构。

### 空间控制能力

FreeMotion集成了显式与隐式空间控制模块。显式引导通过L2距离的梯度扰动实现精确位置约束，隐式引导通过线性层将空间信号注入网络。Figure 5展示了2-4人的空间控制结果，验证了该方法在多人全局轨迹控制上的灵活性。

### 失败模式与局限性

1. **文本-动作错配。** 利用LLM拆分交互描述为单人描述时可能出现语义偏差，导致生成的单人运动与原始交互意图不一致，限制了单人生成质量的上限。
2. **个体间穿透（interpenetration）。** 模型仅在双人运动数据上训练，当人数增多或交互复杂度提升时，可能出现个体间穿透现象，缺乏物理约束机制。
3. **泛化性未充分验证。** 所有实验基于InterHuman数据集，未在大规模多人标注数据或零样本场景下验证泛化能力。
4. **递归误差累积。** 递归生成范式下，前期生成的运动作为后续条件，错误可能沿生成链传播，影响长序列多人运动的一致性。

### 补充图表

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on the InterHuman test set. We run all the evaluations 20 times except MModality runs 5 times. ± indicates the 95% confidence interval. Bold indicates the best result*

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/005_Table.jpg]]

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/006_Figure_3.jpg]]
*Figure 3: Comparison with Intergen* on single and two-person motion generation. For single-person motion, we generate it with our re-annotated single description. For twoperson motion, we further leverage the original interactive descriptions. For better visualization, some pose frames are shifted to prevent complete overlap*

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results for generating three-person motions. We manually design some text prompts and feed them to our network for motion generation. For better visualization, some pose frames are slightly shifted to prevent completed overlap*

![[assets/figures/papers/paper_list_l1874_FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis/figures/008_Figure_5.jpg]]
*Figure 5: Results of multi-person spatial control. We manually design some text prompts as well as the trajectories and leverage the integrated spatial control module to generate the results*

## 方法谱系与知识库定位

**核心瓶颈与范式转换**。现有文本驱动运动生成方法均针对固定人数设计：**MDM**（Tevet et al., arXiv 2022）和**MLD**（Chen et al., CVPR 2023）仅支持单人，**InterGen**（Liang et al., arXiv 2023）仅支持双人。这种硬编码的人数限制使得模型无法扩展到任意人数场景，且空间控制机制难以从单人迁移到多人。FreeMotion 通过一个关键的因果杠杆——将多人运动联合分布分解为条件分布乘积：
$$p(\mathbf{x}^{1},...,\mathbf{x}^{n}) = p(\mathbf{x}^{1}) \prod_{i=1}^{n-1} p(\mathbf{x}^{i+1}|\mathbf{x}^{i},...,\mathbf{x}^{1})$$
从而将多人运动生成转化为递归的条件单人运动生成，实现了范式层面的突破。

**架构解耦与基线差异**。FreeMotion 在三个关键设计维度上与基线形成对比：

| 设计维度 | 基线方法 | FreeMotion |
|---------|---------|-----------|
| 运动生成范式 | 直接预测固定人数的联合运动分布 | 通过条件概率分解实现递归的条件单人运动生成 |
| 条件建模架构 | InterGen 使用共享权重建模交互；ComMDM（Shafir et al., arXiv 2023）基于预训练单人模型做少样本多人 | 解耦的生成模块 + 基于全局自注意力的交互模块，可处理任意数量条件运动 |
| 训练策略 | 单阶段端到端训练 | 两阶段训练：先训练生成模块，再冻结参数后训练交互模块 |

其中，交互模块的设计借鉴了 ControlNet 的思路，但完全基于全局自注意力实现，使其能够处理变长的条件运动序列——这是支持任意人数生成的关键。相比之下，InterGen 的交叉注意力机制天然绑定双人结构，即使修改为 InterGen\*（训练时以 10% 概率将交叉注意力置零以支持单人生成），其架构仍无法原生支持三人及以上场景。

**适用边界**。FreeMotion 的适用性受以下因素制约：
1. **训练数据覆盖**：模型仅在双人运动数据（InterHuman）上训练，虽然能泛化到多人，但对复杂多人交互（如三人协作、群体舞蹈）的生成质量缺乏大规模验证。
2. **文本拆分依赖**：利用 LLM 将多人交互描述拆分为单人描述时，可能出现文本-动作错配，这直接限制了单人生成阶段的质量上限。
3. **物理合理性**：在人数增多时可能出现个体间穿透（interpenetration），因为交互模块的损失函数（掩蔽关节距离图损失）仅在双人数据上优化。

**已知局限**。消融实验（Table 3）揭示了几个关键发现：去除交互模块仅用生成模块时，双人运动 FID 从 6.740 升至 10.749，证明交互模块的必要性；引入交互描述对 FreeMotion 有益（FID↓），但对纯生成模块有害（FID↑），验证了两阶段设计的合理性。然而，递归生成范式本身引入了错误累积风险——前序运动的误差会通过条件注入传播到后续生成中，这在长序列多人场景下尤为突出。

**开放问题**。基于上述分析，以下方向值得后续工作关注：
1. 如何设计更鲁棒的交互描述拆分方法，减少文本-动作错配？可能的路径包括利用运动-文本对齐模型进行后验修正。
2. 如何抑制多人运动生成中的穿透问题？物理模拟器辅助训练或基于穿透的显式惩罚项可能是有效手段。
3. 能否通过合成数据或物理模拟增强多人交互理解，使模型在仅双人标注数据的情况下更好地泛化到复杂多人场景？
4. 递归生成范式下的错误累积问题如何缓解？引入双向生成（前后向条件）或全局一致性约束可能是解决方向。

## 原文 PDF

![[paperPDFs/ECCV_2024/FreeMotion_A_Unified_Framework_for_Number_free_Text_to_Motion_Synthesis.pdf]]

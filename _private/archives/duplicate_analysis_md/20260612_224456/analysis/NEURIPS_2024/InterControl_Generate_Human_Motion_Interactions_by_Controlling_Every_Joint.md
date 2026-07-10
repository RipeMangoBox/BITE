---
title: InterControl Generate Human Motion Interactions by Controlling Every Joint
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/InterControl_Zero_shot_Human_Interaction_Generation_by_Controlling_Every_Joint.pdf
aliases:
- IGHMIBCEJ
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将交互定义为关节对的空间接触/分离距离约束，并通过Motion ControlNet和逆运动学（IK）引导在扩散采样过程中精确满足这些约束。
primary_logic: 将多人交互抽象为每一时刻关节对之间的空间关系（距离、朝向），从而将零样本交互生成转化为单人物运动扩散模型的空间控制问题，无需任何多人训练数据。
claims:
- InterControl能够仅使用单人物数据生成多人交互，且用户偏好显著优于PriorMDM（81.2% vs 18.8%）。
- 在全部关节空间控制精度上，InterControl显著优于所有基线模型，根关节轨迹误差0.0132，位置误差0.0004。
- Motion ControlNet与IK引导缺一不可：移除ControlNet导致FID从0.178升至0.965，移除IK引导导致轨迹误差从0.040升至0.857。
- HumanML3D 上 FID（越低越好） = 0.159（Root控制）
---

# InterControl Generate Human Motion Interactions by Controlling Every Joint

> [!tip] 核心洞察
> 将多人交互抽象为每一时刻关节对之间的空间关系（距离、朝向），从而将零样本交互生成转化为单人物运动扩散模型的空间控制问题，无需任何多人训练数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterControl：通过控制每个关节实现零样本人类交互生成 |
| 英文题名 | InterControl Generate Human Motion Interactions by Controlling Every Joint |
| 会议/期刊 | NEURIPS 2024 |
| Links | [Code](https://github.com/zhenzhiwang/intercontrol) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | InterControl |
| Dataset | HumanML3D, Zero-shot Interaction, User Study |

> [!tip] 效果简介
> - HumanML3D 上，FID（越低越好） 0.159（Root控制） vs 0.544（MDM，无控制） (-0.385)；Traj. err. @50cm（越低越好） 0.0132（Root控制） vs 0.0387（OmniControl） (-0.0255)。
> - Zero-shot Interaction 上，Avg. err. (m)（越低越好） 0.0084 vs 0.6723（PriorMDM） (-0.6639)。
> - User Study 上，用户偏好率 81.2% vs 18.8%（PriorMDM） (+62.4%)。

## 概述

**InterControl** 提出了一种零样本人类交互生成框架，其核心目标是解决现有单人物运动扩散模型无法在全局空间中精确控制任意关节位置，因而无法生成需要空间接触或距离约束的多人交互这一瓶颈。传统方法（如 **PriorMDM**，Shafir et al., ICCV 2023）依赖多人运动交互数据集进行训练，生成人数受限于训练数据中的角色数量，且通过 inpainting 方式无法实现关节级别的精确全局定位。

InterControl 的核心洞察在于：将多人交互抽象为每一时刻关节对之间的空间关系（接触、分离距离），从而将零样本交互生成转化为单人物运动扩散模型的空间控制问题。这一转化使得模型**无需任何多人训练数据**，仅在单人物数据集（HumanML3D、KIT-ML）上训练即可泛化至任意人数。

方法层面，InterControl 构建了一个统一的控制框架，包含两个关键模块：**Motion ControlNet** 和**逆运动学（IK）引导**。Motion ControlNet 作为预训练 MDM（Tevet et al., ECCV 2023）的可训练副本，通过零初始化线性层注入全局空间控制信号，确保生成运动的逼真性；IK 引导则在每个去噪步利用 L-BFGS 优化后验均值，最小化关节到目标位置的距离，实现精确的空间对齐。此外，借助 GPT-4 将自然语言交互描述自动转换为关节接触对计划，实现了文本驱动的自动化交互生成。

实验结果表明，InterControl 在空间控制精度上显著优于所有基线模型：根关节轨迹误差仅 0.0132，位置误差 0.0004。在零样本交互场景下，平均空间误差为 0.0084 m，相较 PriorMDM 的 0.6723 m 降低了近两个数量级。用户研究中，InterControl 以 81.2% 的偏好率大幅领先 PriorMDM 的 18.8%。消融实验进一步揭示 Motion ControlNet 与 IK 引导的互补关系：移除 ControlNet 导致运动质量（FID）从 0.178 急剧劣化至 0.965；移除 IK 引导则使轨迹误差从 0.040 飙升至 0.857，二者缺一不可。

**局限与开放问题**：生成交互的质量高度依赖 LLM 规划器产生的接触计划的合理性；方法主要建立在空间关系上，难以处理需要时序协调或复杂物理交互（如抛接物体）的任务。如何在不依赖多人训练数据的前提下提升交互的物理合理性和时序协调性，以及将 IK 引导扩展至更复杂的物理约束，仍是后续研究的关键方向。

## 背景与动机

### 问题背景：从单人运动到多人交互的鸿沟

文本驱动的三维人体运动生成在近年来取得了显著进展，以 **MDM**（Tevet et al., ECCV 2023）为代表的运动扩散模型已在 **HumanML3D** 和 **KIT-ML** 等数据集上展现出高质量的生成能力。然而，这些模型面临一个根本性瓶颈：它们仅在单人运动数据上训练，无法在全局空间中精确控制任意关节位置，因而难以生成需要空间接触或距离约束的多人交互。

具体而言，多人交互——如拥抱、握手、打斗——的核心特征在于两个或多个人物之间关节对的空间关系：某些关节需要精确接触（如握手时的手腕），某些关节需要保持特定距离（如跳舞时的相对站位），某些关节需要避免碰撞（如打斗时的躯干）。现有方法无法在生成过程中显式建模和满足这些空间约束。

### 现有方法的缺口

当前试图解决运动空间控制的方法存在三方面不足：

**第一，空间控制能力受限。** **PriorMDM**（Shafir et al., ICCV 2023）基于 MDM 的 inpainting 机制，将控制信号作为已知区域进行条件生成，但该方法无法在全局空间中精确控制关节位置，控制精度严重不足。**GMD**（Karunratanakul et al., ICCV 2023）通过解耦根轨迹与位姿生成，仅能控制根关节（骨盆）的全局轨迹，对其他关节（如手腕、脚踝）的位置无能为力。同期工作 **OmniControl**（Xie et al., ECCV 2024）虽结合了 ControlNet 与 classifier-guidance，但仅处理单人物场景，且优化效率较低。

**第二，训练数据依赖严重。** 现有方法若需生成多人交互，通常依赖多人运动交互数据集（如 InterHuman），且生成人数受训练数据中人物数量的限制，无法泛化到任意人数。这导致数据采集成本高昂，且难以覆盖长尾交互类型。

**第三，交互定义缺乏自动化。** 传统方法依赖手工编写控制信号或预定义模板来指定交互方式，缺乏从自然语言描述到精确空间约束的自动化转换机制，限制了文本驱动交互生成的实用性和可扩展性。

### 核心洞察与动机

InterControl 的核心洞察在于：**多人交互可以被抽象为每一时刻关节对之间的空间关系（距离、朝向），从而将零样本交互生成转化为单人物运动扩散模型的空间控制问题。** 这意味着，只要能够精确控制每个关节在全局空间中的位置，就无需任何多人训练数据即可生成多人交互——只需为每个人物分别生成运动，并通过关节对约束确保他们之间的空间关系符合交互语义。

基于这一洞察，InterControl 提出了一个统一框架，包含两个互补的空间控制模块：**Motion ControlNet** 负责生成符合空间约束的逼真运动，**逆运动学（IK）引导** 负责在每个去噪步精确对齐关节位置。同时，利用大语言模型（GPT-4）将自然语言交互描述自动转换为关节接触对计划，实现完全文本驱动的零样本多人交互生成。

## 核心创新

InterControl 的核心创新在于将**多人交互生成**重新定义为**单人物运动扩散模型的空间控制问题**，从而在无需任何多人训练数据的条件下实现零样本交互生成。其关键突破体现在三个相互耦合的机制层面。

### 1. 交互定义的抽象：从多人运动到关节对空间约束

传统多人运动生成方法（如 **PriorMDM**，Shafir et al., ICCV 2023）依赖多人运动数据集训练，生成人数受训练数据限制，且难以泛化到任意人数。InterControl 的核心洞察在于：**多人交互的本质可被抽象为每一时刻关节对之间的空间关系**——接触、分离或特定距离。基于此，交互生成被转化为：给定每个人物的文本提示 $p$ 和空间控制信号 $c$（即关节对的接触/分离计划），分别生成各人物的单人物运动，并在生成过程中强制满足关节对的空间约束。

这一抽象使得模型仅需在单人物数据集（HumanML3D、KIT-ML）上训练，即可零样本支持任意人数的交互生成。交互计划则由 GPT-4 从自然语言描述自动解析为关节接触对，实现了文本驱动的交互生成。

### 2. 全局空间精确控制：Motion ControlNet + IK 引导

现有单人物控制方法存在根本性局限：**GMD**（Karunratanakul et al., ICCV 2023）仅解耦根轨迹与位姿生成，无法控制非根关节；**PriorMDM** 通过 inpainting 实现控制，但无法在全局空间精确定位关节；同期工作 **OmniControl**（Xie et al., ECCV 2024）虽结合了 ControlNet 与 classifier-guidance，但仅处理单人物且优化效率较低。

InterControl 提出了**双模块协同的空间控制架构**：

- **Motion ControlNet**：作为预训练 MDM（Tevet et al., ECCV 2023）的可训练副本，接收全局空间条件输入，通过零初始化线性层将控制信号注入每层 Transformer 编码器。其关键作用是**将 IK 引导优化后的后验均值拉回真实运动分布**，确保运动质量。
- **IK 引导**：在每个去噪步，利用 L-BFGS 优化器最小化后验均值 $\mu_t$ 与目标位置的距离损失：
  $$L(\mu_t, c) = \frac{\sum_n \sum_j m_{nj} \cdot l_{nj}}{\sum_n \sum_j m_{nj}}$$
  其中 $m_{nj}$ 为二值掩码，指示第 $n$ 帧第 $j$ 个关节是否需要控制。这一机制实现了**任意关节在全局空间中的精确到点定位**。

两者形成互补：Motion ControlNet 保障运动逼真度，IK 引导保障空间精度。消融实验（Table 3）给出了决定性证据——移除 ControlNet 导致 FID 从 0.178 急剧劣化至 0.965；移除 IK 引导则使轨迹误差从 0.040 飙升至 0.857。

### 3. 后验均值优化 vs. 预测 $x_0$ 优化

InterControl 在**后验均值 $\mu_t$ 上执行 IK 引导**，而非在预测的干净运动 $x_0$ 上优化。这一设计选择具有深层合理性：后验均值 $\mu_t$ 是 $x_{t-1}$ 的直接估计，在其上优化能更稳定地影响采样轨迹。实验表明（Table 3），在 $x_0$ 上执行 IK 引导虽可加快训练，但 FID 略有上升（0.195 vs 0.178）。此外，L-BFGS 二阶优化相比一阶梯度的 classifier-guidance 所需迭代更少，推理更快（80.1s vs 120s，Table 4）。

### 创新总结

| 创新维度 | 基线做法 | InterControl 做法 |
|---------|---------|------------------|
| 训练数据 | 需要多人交互数据集，人数固定 | 仅用单人物数据，零样本支持任意人数 |
| 空间控制 | Inpainting 或仅根轨迹解耦，无法精确控制所有关节 | Motion ControlNet + IK 引导，任意关节全局精确定位 |
| 交互定义 | 手工控制信号或预定义模板 | GPT-4 自动解析自然语言为关节接触对计划 |
| 优化目标 | 在 $x_0$ 或通过一阶梯度引导 | 在后验均值 $\mu_t$ 上用 L-BFGS 二阶优化 |

**注意**：LLM 规划器生成的接触计划质量直接影响交互合理性，不合理的计划可能导致交互失败，这一依赖关系需要在实际应用中加以验证。

## 整体框架

InterControl 将零样本多人交互生成重新定义为**单人物运动扩散模型的空间控制问题**。其核心洞察在于：多人交互的本质可抽象为每一时刻关节对之间的空间关系（接触距离、分离距离、相对朝向），因此无需任何多人训练数据，仅需在预训练的单人物模型上施加精确的全局空间控制即可生成任意人数的交互。

### 整体 Pipeline

整个框架由四个核心模块串联构成，其输入输出流如下：

1. **LLM 规划器（GPT-4）**：接收自然语言交互描述（如“两人拥抱”），将其解析为两个输出——每个人物的独立文本提示 $p^a, p^b$，以及关节接触对计划（joint contact plan）$c$。该计划定义了哪些关节对在哪些时刻需要满足何种空间约束（接触或分离距离）。此步骤将高层语义交互自动转化为可执行的空间控制信号（Section 3.5; Appendix A.3）。

2. **MDM Backbone（冻结）**：预训练的单人物文本条件运动扩散模型，基于 **MDM**（Tevet et al., ECCV 2023）。该模型接收文本提示 $p$ 和噪声运动序列 $x_t$，预测干净运动 $x_0$ 并估计后验均值 $\mu_\theta(x_t, t, p)$。在整个 InterControl 训练和推理过程中，MDM 参数保持冻结，作为运动先验的锚点（Section 3.2）。

3. **Motion ControlNet（可训练）**：MDM 的可训练副本，通过零初始化线性层与冻结的 MDM 各 Transformer 编码器层连接。它接收全局空间控制信号 $c$（即目标关节在全局坐标系中的三维位置），生成符合空间约束的逼真运动。ControlNet 的作用是**维持生成运动在训练分布内**，防止后续 IK 引导将运动推向分布外（Section 3.3; Figure 5）。

4. **逆运动学（IK）引导模块**：在每个去噪步，对 ControlNet 输出的后验均值 $\mu_t$ 执行 L-BFGS 优化，最小化关节当前位置与目标位置之间的加权距离损失：
   $$L(\mu_t, c) = \frac{\sum_n \sum_j m_{nj} \cdot l_{nj}}{\sum_n \sum_j m_{nj}}$$
   其中 $m_{nj}$ 为二值掩码，标记第 $n$ 帧第 $j$ 个关节是否需要控制。此模块确保关节位置**精确对齐**到目标空间坐标，是实现高精度控制的关键（Section 3.4; Equation 2）。

### 推理时的数据流

对于多人交互生成，上述流程以**并行方式**运行：每个人物拥有独立的 MDM Backbone 和 Motion ControlNet 副本，共享同一个 IK 引导损失函数 $L_{multi}(\mu_t^a, \mu_t^b)$，该损失同时考虑所有参与人物的关节约束。LLM 规划器为每个人物生成独立的文本提示和共享的接触计划，确保交互双方的动作在语义和空间上协调一致。

### 关键设计决策

- **训练仅需单人物数据**：Motion ControlNet 和 IK 引导模块均在 HumanML3D 和 KIT-ML 等单人物运动数据集上训练，无需任何多人交互数据。这使 InterControl 天然支持零样本泛化到任意人数（Section 3.1）。
- **ControlNet 与 IK 引导互补**：消融实验表明两者缺一不可——移除 ControlNet 导致 FID 从 0.178 急剧劣化至 0.965（运动质量崩塌）；移除 IK 引导则导致轨迹误差从 0.040 飙升至 0.857（无法满足空间约束）（Table 3）。
- **L-BFGS 优于一阶梯度优化**：相比 classifier-guidance 式的一阶梯度下降，L-BFGS 以更少迭代达到相近或更优性能，推理时间更短（80.1s vs 120s）（Table 3 Row 6; Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/002_Figure_2.jpg]]
*Figure 2: Overview. Our model could precisely control human joints in the global space via the Motion ControlNet and IK guidance module. By leveraging LLM to adapt interaction descriptions to joint contact pairs, it could generate multi-person interactions via a single-person motion generation model in a zero-shot manner*

## 核心模块与公式推导

InterControl 的核心架构由两个协同工作的空间控制模块构成：**Motion ControlNet** 与**逆运动学（IK）引导**。前者负责在全局空间中生成逼真且符合空间约束的运动，后者则通过优化后验均值实现关节位置的精确对齐。两者缺一不可，共同将零样本多人交互生成转化为单人物运动扩散模型的空间控制问题。

### 预训练基础：MDM 运动扩散模型

InterControl 构建在预训练的 **MDM**（Tevet et al., ECCV 2023）之上，该模型是一个基于 Transformer 的文本条件运动扩散模型。在去噪过程中，模型根据当前带噪运动 $x_t$、时间步 $t$ 和文本提示 $p$ 预测干净运动 $x_0$，进而估计后验均值 $\mu_{\theta}$：

$$
\mu_{\theta}(x_t, t, p) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t} x_0(x_t, t, p; \theta) + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t} x_t
$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数，$\beta_t = 1 - \alpha_t$ 为单步噪声方差。该后验均值是后续 DDIM 采样和 IK 引导优化的基础。在 InterControl 框架中，MDM 的参数被完全冻结，仅作为运动先验提供分布约束。

### Motion ControlNet：全局空间条件注入

Motion ControlNet 是 MDM 的一个可训练副本，其核心设计借鉴了 ControlNet（Zhang et al., ICCV 2023）的架构思想。具体而言：

- **结构连接**：ControlNet 的每个 Transformer 编码器层通过一个**零初始化线性层**连接到对应的 MDM 编码器层。零初始化确保训练初期 ControlNet 的输出为零，避免破坏预训练模型的运动分布。
- **条件输入**：ControlNet 接收全局空间控制信号 $c$（包括目标关节的全局坐标、控制掩码等），将其编码后注入到去噪过程中，引导生成的运动在全局空间中满足空间约束。
- **训练策略**：在训练阶段，ControlNet 需要适应被 IK 引导更新后的后验均值，从而学习将运动保持在训练数据分布内。这一设计使得 ControlNet 能够生成逼真运动，而 IK 引导则负责精确的空间对齐。

### IK 引导：精确关节定位

Motion ControlNet 提供了粗粒度的空间控制，但无法保证关节精确到达目标位置。为此，InterControl 在每个去噪步骤中对后验均值 $\mu_t$ 执行基于优化的 IK 引导。

**损失函数定义**：对于给定的空间控制信号 $c$，IK 引导的总损失为所有关节与帧的加权距离损失：

$$
L(\mu_t, c) = \frac{\sum_n \sum_j m_{nj} \cdot l_{nj}}{\sum_n \sum_j m_{nj}}
$$

其中 $n$ 遍历所有帧，$j$ 遍历所有关节，$m_{nj} \in \{0, 1\}$ 为二元掩码（指示该关节在该帧是否需要被控制），$l_{nj}$ 为关节 $j$ 在帧 $n$ 的预测位置与目标位置之间的距离（通常为 L2 距离）。

**优化过程**：在每个去噪步，使用 **L-BFGS** 优化器对后验均值 $\mu_t$ 进行 $k$ 次迭代优化，最小化 $L(\mu_t, c)$，使关节位置逐步逼近目标。优化后的后验均值用于 DDIM 采样得到 $x_{t-1}$。消融实验表明，L-BFGS 相比一阶梯度优化（classifier-guidance）需要更少的迭代次数即可达到相近性能，推理时间更短（80.1s vs 120s，Table 4）。

**多人交互扩展**：对于双人交互场景，单人的 IK 损失 $L_{single}(\mu_t, c)$ 被扩展为多人损失 $L_{multi}(\mu_t^a, \mu_t^b)$，同时优化两个角色的后验均值，使双方的受控关节满足接触或分离的空间关系。

### 模块协同与消融验证

消融实验（Table 3）揭示了两个模块的互补关系：

- **移除 ControlNet**（仅保留 IK 引导）：空间误差虽低，但运动质量急剧恶化，FID 从 0.178 升至 0.965，说明 IK 引导单独优化会破坏运动分布。
- **移除 IK 引导**（仅保留 ControlNet）：FID 为 0.287，运动质量尚可，但轨迹误差从 0.040 飙升至 0.857，无法精确满足控制条件。

这一结果表明：**Motion ControlNet 负责维护运动分布，IK 引导负责精确空间对齐**，两者协同才能同时实现高逼真度和高控制精度。

### LLM 规划器：自动化控制信号生成

为支持文本驱动的交互生成，InterControl 引入 **GPT-4** 作为规划器，将自然语言交互描述自动转换为每人的文本提示及关节接触对计划（contact plan）。该计划定义了每一时刻哪些关节对需要接触或保持特定距离，作为 IK 引导的空间控制信号 $c$。这一设计使得用户无需手工指定复杂的控制信号，实现了从文本到多人交互的端到端生成。

### 补充图表

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/009_Figure_5.jpg]]
*Figure 5: Architecture of Motion ControlNet*

## 实验与分析

### 核心实验设计

InterControl 的实验围绕两个核心维度展开：**单人物全局空间控制精度**与**零样本多人交互生成质量**。所有实验均基于 HumanML3D 和 KIT-ML 两个单人物运动数据集进行训练与评估，未使用任何多人交互数据。评估指标涵盖生成质量（FID、R-Precision、Diversity、Foot Skating）与空间控制精度（Trajectory Error、Location Error、Average Error）。基线方法包括 **MDM**（Tevet et al., ECCV 2023）、**PriorMDM**（Shafir et al., ICCV 2023）、**GMD**（Karunratanakul et al., ICCV 2023）和 **OmniControl**（Xie et al., ECCV 2024）。

### 单人物空间控制精度（Table 1）

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/003_Table_1.jpg]]
*Table 1: Spatial control results on HumanML3D [14]. → means closer to real data is better. Random One/Two/Three reports the average performance over 1/2/3 randomly selected joints in evaluation. † means our evaluation on their model*

Table 1 展示了在 HumanML3D 数据集上对各关节进行全局空间控制的结果。InterControl 在根关节控制任务上取得 **FID 0.159**，显著优于 OmniControl（0.310）和 GMD（0.276），且与无控制的 MDM（0.544）相比下降 0.385。在空间精度方面，InterControl 的根关节轨迹误差仅 **0.0132**，位置误差 **0.0004**，均大幅领先所有基线。

当控制关节数增加至全部 22 个关节时，InterControl 仍能将平均误差维持在 0.0061，而 OmniControl 为 0.0240，MDM 为 0.0245。这验证了 Motion ControlNet 与 IK 引导的协同机制：ControlNet 确保生成运动保持在真实分布内，IK 引导通过 L-BFGS 优化后验均值实现精确的全局位置对齐。值得注意的是，InterControl 在实现高精度控制的同时，R-Precision 和 Diversity 指标与无控制模型相当，说明空间约束并未损害运动的文本一致性与多样性。

### 零样本交互生成评估（Table 2）

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/004_Table_2.jpg]]
*Table 2: Evaluation on (left) spatial errors and (right) user preference in interactions*

Table 2 左半部分报告了交互场景下的空间误差。InterControl 的平均误差仅 **0.0084m**，而 PriorMDM 高达 0.6723m，OmniControl 为 0.6466m。这一巨大差距源于两类方法在控制机制上的根本差异：PriorMDM 和 OmniControl 依赖 inpainting 或 classifier-guidance 在局部关节点进行引导，无法在全局坐标系下精确满足多人间的接触/分离距离约束；InterControl 则通过将交互抽象为关节对之间的空间关系，在去噪过程中同时对多个人的后验均值进行 IK 优化，从而实现了亚厘米级的空间对齐。

Table 2 右半部分的用户研究进一步验证了生成质量。在 32 名参与者对 20 组交互的盲评中，InterControl 以 **81.2%** 的偏好率显著优于 PriorMDM 的 18.8%。用户被要求从运动真实性和交互合理性两个维度进行判断，结果表明即使在零样本设定下，InterControl 生成的握手、拥抱、格斗等交互在视觉上更具说服力。

### 消融实验：ControlNet 与 IK 引导的互补性（Table 3）

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on the HumanML3D [14] dataset*

Table 3 的消融实验揭示了两个核心模块的不可替代性：

- **移除 Motion ControlNet（仅保留 IK 引导）**：空间误差保持较低水平（Traj. err. 0.0421），但 **FID 从 0.178 急剧恶化至 0.965**。这说明 IK 引导虽然能精确移动关节，但缺乏 ControlNet 对运动分布的约束，导致生成的运动出现严重失真（如关节扭曲、姿态异常）。
- **移除 IK 引导（仅保留 Motion ControlNet）**：FID 为 0.287，仍可接受，但 **Traj. err. 从 0.040 飙升至 0.857**。这表明 ControlNet 单独无法严格满足精确的空间控制条件，仅能产生大致符合方向的运动趋势。

进一步的分析还表明，在后验均值 $\\mu_t$ 上执行 IK 引导优于在预测的干净运动 $x_0$ 上执行（FID 0.178 vs 0.195），这是因为 $\\mu_t$ 融合了当前噪声步与预测信号，提供了更稳定的优化目标。在优化器选择上，L-BFGS 相比一阶梯度优化（classifier-guidance 风格）需要更少的迭代次数即可收敛，推理时间从 120s 降至 **80.1s**（Table 4）。

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/008_Table_4.jpg]]
*Table 4: Inference time analysis on a NVIDIA A100 GPU*

### 文本到运动基准测试（Table 5）

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/010_Table_5.jpg]]
*Table 5: Text-to-motion evaluation on the (left) HumanML3D [14] and (right) KIT-ML [47] datasets. The right arrow → means closer to real data is better. Methods in the upper part are unable to perform spatial control. † means our implementation*

Table 5 展示了在 HumanML3D 和 KIT-ML 标准文本到运动基准上的结果。添加空间控制能力后，InterControl 的 FID（0.178）、R-Precision（0.608）和 Diversity（9.02）与原始 MDM（0.544 / 0.611 / 9.56）相比，生成质量并未因控制模块的引入而退化。这归功于 ControlNet 的零初始化连接策略，在训练初期不干扰预训练 MDM 的行为，逐步学习将空间条件融入生成过程。

### 失败模式与局限性

实验和定性分析揭示了以下主要失败模式：

1. **LLM 规划器依赖性**：交互质量高度依赖 GPT-4 生成的接触计划。当 LLM 产生不合理的关节配对（如将握手定义为头部接触）时，IK 引导仍会忠实执行，导致生成荒诞的交互。目前系统缺乏对接触计划合理性的验证机制。

2. **时序协调不足**：方法仅约束每一时刻的空间关系，无法建模交互的时序动态（如一人先伸手、另一人后握手的因果顺序）。这在需要精确时序配合的交互（如舞蹈、传球）中表现尤为明显。

3. **物理伪影残留**：尽管 Foot Skating 比率在控制后未显著上升，但生成的交互运动仍存在穿透、悬空等物理不合理现象。这是因为 IK 引导仅优化关节位置，不包含碰撞检测或物理约束。

4. **计算开销**：每个去噪步需运行 L-BFGS 优化（默认 5 次迭代），在 A100 GPU 上单次推理约需 80 秒，限制了实时应用场景。

### 开放问题

- 能否引入闭环物理仿真验证，在生成过程中实时检测并修正穿透与滑动？
- 接触计划能否通过可学习的规划器替代 LLM，实现端到端的交互意图到空间约束的映射？
- IK 引导的损失函数能否扩展至包含速度、加速度等动力学约束，以提升交互的物理合理性？

### 补充图表

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/005_Figure_3.jpg]]
*Figure 3: Comparison with PriorMDM [51] in user-study of zero-shot human interaction generation*

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results of zero-shot human interaction generation*

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/001_Figure_1.jpg]]
*Figure 1: InterControl is able to generate interactions of a group of people given joint-joint contact or separation pairs as spatial condition, and it is only trained on single-person data. Our generated interactions are realistic and similar to real interactions in internet images in (a) daily life and (b) fighting. (c) shows our generated group motions (red dots) could serve as reference motions for physics animation*

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/011_Table_6.jpg]]
*Table 6: Spatial control results on the HumanML3D [14] dataset. Ours (all) means the model is trained on one randomly selected joint among all joints in each iteration*

![[assets/figures/papers/paper_list_l1793_InterControl_Generate_Human_Motion_Interactions_by_Controlling_Every_Joi/figures/012_Figure_6.jpg]]
*Figure 6: Example of the questionnaire of user-study*

## 方法谱系与知识库定位

### 1. 方法在谱系中的位置

InterControl 处于**可控人体运动生成**与**零样本多人交互生成**的交叉点。其核心思路是将多人交互问题降解为单人物运动扩散模型的空间控制问题，从而绕过对多人运动数据集的依赖。这一思路在现有方法谱系中具有明确的定位：

- **上游基础**：InterControl 直接建立在单人物文本条件运动扩散模型 **MDM**（Tevet et al., ECCV 2023）之上。MDM 提供了基于 Transformer 的扩散去噪骨架，但本身不具备任何空间控制能力——它只能根据文本提示生成运动，无法指定关节在全局空间中的位置。InterControl 将 MDM 的参数完全冻结，仅通过外部模块注入空间控制信号，从而保留了 MDM 原有的文本到运动生成质量。

- **与 inpainting 类方法的区别**：**PriorMDM**（Shafir et al., ICCV 2023）同样基于 MDM，通过 inpainting 方式在已知部分关节轨迹的条件下补全其余运动。然而，inpainting 机制本质上是在运动特征空间中进行条件生成，缺乏对全局空间坐标的精确约束能力。实验证据表明，PriorMDM 在交互场景中的平均空间误差高达 0.6723 m，而 InterControl 仅为 0.0084 m（Table 2 左），差距达两个数量级。这一差异的根本原因在于：inpainting 只能“建议”关节趋向目标位置，而无法“强制”关节精确到达。

- **与根轨迹解耦方法的区别**：**GMD**（Karunratanakul et al., ICCV 2023）将运动生成解耦为根轨迹预测和局部姿态生成两个阶段，能够控制根关节的全局轨迹，但无法控制其他关节。InterControl 通过 Motion ControlNet 和 IK 引导的组合，实现了对任意关节的精确全局定位，包括根关节（Traj. err. 0.0132 vs GMD 的 0.0233，Table 1）和所有关节的平均控制（Avg. err. 0.0001 vs GMD 的 0.0045，Table 1）。

- **与同期 ControlNet 类方法的区别**：**OmniControl**（Xie et al., ECCV 2024）是同期工作，同样采用了 ControlNet 与 classifier-guidance 结合的策略进行单人物运动控制。两者的关键差异在于优化机制：OmniControl 使用一阶梯度优化（classifier-guidance），而 InterControl 使用二阶 L-BFGS 优化后验均值。这一选择带来了两个优势：（1）L-BFGS 收敛更快，推理时间更短（80.1s vs 120s，Table 4）；（2）在后验均值上优化而非在预测的 $x_0$ 上优化，使 Motion ControlNet 在训练阶段就能适应 IK 引导产生的分布偏移，从而保持生成运动的逼真度（FID 0.178 vs 在 $x_0$ 上优化的 0.195，Table 3 Row 2 vs Row 5）。

### 2. 核心因果机制

InterControl 的性能优势来源于两个互补模块的协同作用，消融实验（Table 3）提供了明确的因果证据：

**Motion ControlNet 的作用**：ControlNet 负责将全局空间条件编码并注入扩散去噪过程，确保生成的运动在满足空间约束的同时保持运动分布的真实性。移除 ControlNet 后，仅靠 IK 引导虽然仍能维持低空间误差（Traj. err. 0.0167），但运动质量急剧恶化——FID 从 0.178 飙升至 0.965（Table 3 Row 1 vs Row 2）。这说明 IK 引导单独使用时，虽然能“强行”将关节拉到目标位置，但会破坏运动的时间连贯性和物理合理性；ControlNet 的作用是在训练阶段学习如何生成自然运动的同时满足空间条件，从而“吸收”IK 引导可能引入的分布外扰动。

**IK 引导的作用**：IK 引导负责在每个去噪步对后验均值进行精确优化，最小化关节到目标位置的距离。移除 IK 引导后，仅靠 Motion ControlNet 得到 FID 0.287（仍可接受），但空间误差大幅上升——Traj. err. 从 0.040 升至 0.857（Table 3 Row 3 vs Row 2）。这说明 ControlNet 单独使用时只能“大致”满足空间条件，无法实现精确的关节定位。两者的关系可以概括为：ControlNet 保证“运动看起来真实”，IK 引导保证“关节确实到位”。

**优化目标的选取**：在后验均值 $\mu_t$ 上执行 IK 引导（而非在预测的干净运动 $x_0$ 上）是另一个关键设计。在 $x_0$ 上优化虽然可以加快训练（因为 ControlNet 不需要适应 IK 引导的扰动），但 FID 略有上升（0.195 vs 0.178，Table 3 Row 5 vs Row 2），因为推理时 ControlNet 从未见过 IK 引导修改后的分布。

### 3. 适用边界与局限

InterControl 的能力边界由其核心设计决定：**交互被定义为关节对之间的空间关系（距离、朝向）**。这一抽象既赋予了方法零样本泛化能力，也划定了其适用范围。

**适用的交互类型**：
- 基于空间接触的交互：握手、拥抱、击掌、格斗中的拳击/踢击等。这些交互的核心特征是特定关节对需要在某些时刻满足接触或近距离约束，与 InterControl 的空间控制机制天然契合。
- 基于空间分离的交互：保持距离、跟随、对峙等。这些交互可以通过设置关节对的最小距离约束来实现。
- 任意人数的群体交互：由于每个人物的运动独立生成，仅通过关节对约束耦合，因此可以零样本扩展到训练数据中未出现的任意人数。

**不适用的交互类型**：
- 需要时序精确协调的交互：如双人舞蹈中的同步动作、接力赛中的交接棒时机。InterControl 的约束是逐帧独立的空间约束，缺乏对时序模式的显式建模。
- 涉及物体传递或复杂物理的交互：如抛接球、抬重物。这些交互涉及力的传递、质量分布等物理约束，无法仅通过关节距离约束来刻画。IK 引导要求损失函数可微，对复杂的物理约束可能无法直接处理。
- 长序列交互中的接触一致性：LLM 规划的接触计划在较长序列中可能出现不一致（如手已经松开但后续帧仍要求接触），目前缺乏闭环反馈机制来检测和修正这类问题。

**其他已知局限**：
- 生成运动仍存在脚滑动等伪影，这是单人物运动扩散模型的固有缺陷，在交互场景中可能被放大。
- 交互质量高度依赖 LLM 规划器产生的接触计划质量；不合理的计划（如要求两个相距很远的人突然接触）会导致生成失败或运动不自然。
- 推理时需在每个去噪步运行 L-BFGS 优化，虽然比一阶优化快，但在 A100 GPU 上仍需约 80 秒（Table 4），难以满足实时应用需求。
- 方法未在真实的多人运动数据集（如 InterHuman）上直接评估交互真实性，所有交互评估均基于空间误差和用户偏好，缺乏与真实多人运动数据的分布对比。

### 4. 开放问题

1. **物理合理性提升**：如何在不依赖多人训练数据的前提下，提升交互的物理合理性（如接触力、动量守恒）和时序协调性？一个可能的方向是将 InterControl 与物理模拟器耦合，利用 IK 引导产生的运动作为参考轨迹，由模拟器进行物理修正。

2. **约束类型的扩展**：除了距离与朝向，还有哪些可微的空间关系可以作为交互定义？例如，关节之间的相对速度、加速度约束，或基于物理的接触力约束，能否纳入 IK 引导框架以覆盖更广泛的交互类型？

3. **LLM 规划的闭环反馈**：LLM 规划的接触计划在更长的交互序列中能否保持一致性？是否需要一个闭环反馈机制，在生成过程中检测接触计划的合理性并动态调整？

4. **与多人数据集的协同**：虽然 InterControl 的核心优势是零样本能力，但在有少量多人数据可用时，能否通过微调或条件注入进一步提升交互的真实性？这涉及零样本能力与监督学习的权衡。

5. **推理效率优化**：L-BFGS 优化是推理时间的主要瓶颈。是否可以通过学习一个“空间条件预测器”来直接预测满足空间约束的后验均值，从而避免迭代优化？或者通过蒸馏将 IK 引导的知识迁移到 ControlNet 中，实现单步生成？

## 原文 PDF

![[paperPDFs/NEURIPS_2024/InterControl_Zero_shot_Human_Interaction_Generation_by_Controlling_Every_Joint.pdf]]
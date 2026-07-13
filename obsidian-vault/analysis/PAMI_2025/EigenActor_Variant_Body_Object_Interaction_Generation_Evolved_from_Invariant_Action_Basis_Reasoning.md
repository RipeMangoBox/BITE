---
title: EigenActor Variant Body Object Interaction Generation Evolved from Invariant Action Basis Reasoning
type: paper
paper_level: A
venue: PAMI
year: 2025
pdf_ref: paperPDFs/PAMI_2025/EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invariant_Action_Basis_Reasoning.pdf
project_link: null
code_link: null
aliases:
- EVBOIGEFIABR
tags:
- PAMI_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将文本到HOI分解为两阶段：先推断物体无关的动作特异性规范身体动作，然后基于该动作基元丰富物体特异性交互风格，从而显式建模共享动作先验和物体风格先验。
primary_logic: 同一交互意图（如“举起椅子”与“举起杯子”）的HOI样本封装了相似的动作特异性身体运动模式，但展现不同的物体特异性交互风格；因此先学习动作模式基元，再演化交互风格，可有效提升生成质量。
claims:
- EigenActor在三个大规模数据集上显著优于所有SOTA方法，在语义一致性和交互真实性上提升明显。
- 解耦的动作特异性运动先验有效提升文本-HOI语义一致性，消融实验中推断动作基元可接近真实基元性能。
- 物体接触部分推断和手-物交互优化模块显著提高交互真实感与物理合理性。
- EigenActor在小样本训练下仍保持显著优势，如仅用10%样本时FID相对基线HIMO-Gen降低50%。
---

# EigenActor Variant Body Object Interaction Generation Evolved from Invariant Action Basis Reasoning

> [!tip] 核心洞察
> 同一交互意图（如“举起椅子”与“举起杯子”）的HOI样本封装了相似的动作特异性身体运动模式，但展现不同的物体特异性交互风格；因此先学习动作模式基元，再演化交互风格，可有效提升生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | EigenActor: 基于不变动作基演化的变体人体-物体交互生成 |
| 英文题名 | EigenActor Variant Body Object Interaction Generation Evolved from Invariant Action Basis Reasoning |
| 会议/期刊 | PAMI 2025 |
| Links |  |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | EigenActor |
| Dataset | HIMO, FullBodyManipulation, GRAB |

> [!tip] 效果简介
> - HIMO 上，R-Precision (Top-3) ↑ 0.6805 ± .0021；FID ↓ 1.1043 ± .0357；Contact Precision (C_prec) ↑ 0.85 ± .0021。
> - FullBodyManipulation 上，R-Precision (Top-3) ↑ 0.73；FID ↓ 0.62；MM-Dist ↓ 3.75。
> - GRAB 上，R-Precision (Top-3) ↑ 0.66。

## 概要

### 问题瓶颈

文本到三维人体-物体交互（Text-to-HOI）生成面临一个根本性瓶颈：现有方法通常部署从文本到物体特异性三维身体运动的**直接映射**，这一单阶段策略遭遇巨大的跨模态差距，且忽略了关键的结构性先验——相同交互意图（如“举起椅子”与“举起杯子”）的HOI样本封装了高度相似的**动作特异性身体运动模式**，仅在与不同物体交互时展现出不同的**物体特异性交互风格**。直接映射范式迫使模型同时学习语义理解、动作模式生成和交互风格建模，导致语义一致性与交互真实性均受制约。

### 核心方法定位

**EigenActor** 提出了一种解耦的文本到HOI生成范式，将身体运动推理分解为两个序贯阶段：

1. **动作特异性运动推断**：首先从文本指令推断**物体无关的规范身体动作序列**——即该交互意图下共享的动作基元。
2. **物体特异性交互演化**：基于该动作基元，融合由文本和物体形状条件生成的**交互风格残差**，形成与特定物体自然交互的完整身体姿势。

这一分解策略显式建模了共享动作先验和物体风格先验，使模型得以分别专注于语义理解和交互真实性。EigenActor由两个核心模块构成：**BodyNet** 负责上述两阶段身体姿势生成；**ObjectNet** 则通过接触部分推断、物体运动扩散和手-物交互优化三个组件，规划物体的6-DoF运动序列并提升物理交互真实感。

### 方法谱系与知识库定位

EigenActor定位于文本条件的三维HOI生成领域，与以下代表性工作形成差异化对比：

- **直接映射方法**：如 **HIMO-Gen**（Lv et al., ECCV 2024）、**CHOIS**（Li et al., ECCV 2024）等采用单阶段文本到HOI生成策略，缺乏对动作模式与交互风格的显式解耦。
- **接触引导方法**：如 **CG-HOI**（Diller and Dai, CVPR 2024）、**F-HOI**（Yang et al., ECCV 2024）利用接触信息引导生成，但未将动作先验作为独立推理目标。
- **扩散运动模型**：如 **MDM**（Tevet et al., ICLR 2022）、**MLD**（Chen et al., CVPR 2023）、**MotionGPT**（Jiang et al., NeurIPS 2023）专注于人体运动生成，未系统建模物体交互。
- **物理信息方法**：如 **InterDiff**（Xu et al., ICCV 2023）引入物理约束，但未采用动作-风格分解策略。

EigenActor的核心区分在于：通过**动作基元先验**的显式建模，将文本到HOI的映射从“端到端黑箱”转变为“先推理意图动作模式、再演化交互风格”的可控过程，在方法谱系中开辟了基于不变动作基推理的变体交互生成路径。

### 主要发现

EigenActor在三个大规模数据集（HIMO、FullBodyManipulation、GRAB）上显著优于所有对比方法，关键证据如下：

- **语义一致性**：HIMO数据集上R-Precision (Top-3) 达0.6805，FID降至1.1043；FullBodyManipulation上FID仅0.62，MM-Dist低至3.75。
- **交互真实性**：HIMO上接触精度（C_prec）达0.85，接触百分比（C_%）达0.67，验证了手-物交互的物理合理性。
- **解耦有效性**：消融实验表明，推断的动作特异性运动基元可接近真实基元性能（R-Prec 0.66 vs 0.69），且显著优于无动作基元的直接生成（R-Prec 0.63）。
- **小样本鲁棒性**：仅用10%训练样本时，EigenActor的FID相对基线HIMO-Gen降低约50%，展现出对数据规模的强鲁棒性。
- **用户偏好**：用户研究中EigenActor相对各基线的偏好率显著占优。

这些结果一致表明，将文本到HOI分解为动作基元推断与交互风格演化两个阶段，是提升生成质量的有效因果调控路径。



文本驱动的人体-物体交互（Text-to-HOI）生成旨在根据自然语言指令合成与指定物体进行物理交互的3D全身人体运动序列。该任务在具身智能、虚拟现实和机器人学习等领域具有重要应用价值，但其核心挑战在于跨越文本语义与3D物理交互之间的巨大模态鸿沟。

现有方法普遍采用单阶段直接映射策略，即从文本条件直接回归或生成物体特异性的3D身体运动。这类方法面临两个根本性瓶颈：其一，文本到高维运动空间的直接映射缺乏中间语义锚点，导致生成的交互动作与文本指令的语义一致性难以保证；其二，单阶段范式将动作模式与交互风格混为一谈，忽略了同一交互意图下不同物体实例之间共享的身体运动规律，从而限制了模型的泛化能力和交互真实感。

EigenActor 的核心洞察在于：具有相同交互意图的HOI样本——例如“举起椅子”与“举起杯子”——封装了高度相似的动作特异性身体运动模式（如弯腰、伸手、上举），但在与具体物体接触时展现出不同的物体特异性交互风格（如手部姿态、接触位置和力度分布）。这一观察暗示，将文本到HOI的推理过程分解为“先学习动作模式基元，再演化交互风格”的两阶段策略，有望从根本上缓解上述瓶颈。

基于此动机，EigenActor 提出了一种新颖的两阶段推理框架：首先从文本指令推断物体无关的动作特异性规范身体运动，将其作为共享的动作先验基元；然后基于该动作基元，结合文本语义与物体几何信息，丰富物体特异性的交互风格残差，从而生成既符合语义意图又具备物理真实感的完整HOI序列。这种分解策略显式建模了动作先验与物体风格先验，使模型能够在小样本场景下保持鲁棒性，并在语义一致性与交互真实性两个关键维度上取得显著提升。



## 核心方法与创新机理

EigenActor 的核心创新在于将文本到人体-物体交互（Text-to-HOI）的生成任务从传统的单阶段直接映射，重构为**两阶段解耦推理范式**。这一范式基于一个关键洞察：同一交互意图（如“举起椅子”与“举起杯子”）下的 HOI 样本，封装了相似的动作特异性身体运动模式，但展现出不同的物体特异性交互风格。因此，先学习共享的动作模式基元，再基于该基元演化出物体特异性的交互风格，可从机理上缩小文本与 3D 运动之间的跨模态鸿沟。

具体而言，EigenActor 改变了以下核心策略槽位（changed slot）：

- **身体运动推理策略**：从“单阶段直接映射文本到物体特异性 3D 身体动作”转变为“**两阶段分解推理**”——先推断物体无关的动作特异性规范运动（Action-specific Canonical Motion），再基于该动作基元融合物体特异性交互风格（Object-specific Interaction Style）。这一转变显式地建模了共享动作先验与物体风格先验，使得生成的 HOI 既能保持语义一致性，又能展现与目标物体自然交互的物理真实感。

在架构层面，该策略由两大核心模块承载：

1. **BodyNet**：负责从文本和物体条件生成 3D 全身姿态序列。其内部采用**动作特异性运动扩散**（Action-specific Motion Diffusion）从文本条件生成物体无关的规范身体动作序列，再通过**物体特异性交互扩散**（Object-specific Interaction Diffusion）从文本与物体形状条件生成交互风格残差，将两者相加得到最终身体姿势（见公式 `b_n' = \widetilde{b}_n' + \widehat{b}_n'`）。

2. **ObjectNet**：负责规划物体的 6-DOF 运动序列。其创新在于引入了**接触部分推断**（Contact Part Inference）模块，基于文本与物体几何预测手可接触的物体部件，为后续运动规划提供条件；并通过**手-物交互优化**（Interaction Optimization）施加时序一致性约束与接触帧零距离约束，显著提升手-物交互的物理真实感。

相较于现有方法（如 **HIMO-Gen** (Lv et al., ECCV 2024)、**CHOIS** (Li et al., ECCV 2024)、**InterDiff** (Xu et al., ICCV 2023) 等）的直接映射策略，EigenActor 的解耦设计在语义一致性和交互真实性上均取得了显著提升。消融实验证实，推断的动作基元可接近真实基元的性能，而接触部分推断与交互优化模块对交互质量有决定性贡献。



EigenActor 将文本到人体-物体交互（text-to-HOI）生成建模为一个扩散驱动的条件生成框架，其核心创新在于将身体运动推理分解为两个序贯阶段：**动作特异性运动推断**与**物体特异性交互推断**。该分解的动机源于一个关键观察：具有相同交互意图的 HOI 样本（如“举起椅子”与“举起杯子”）封装了相似的动作特异性身体运动模式，但展现不同的物体特异性交互风格。因此，先学习共享的动作基元，再基于物体条件演化交互风格，可有效缓解直接映射带来的跨模态差距与语义一致性瓶颈。

整体架构由两大核心模块构成：**BodyNet** 负责生成与文本语义对齐且与物体自然交互的全身姿态序列；**ObjectNet** 负责规划物体的 6-DoF 运动轨迹，并优化手-物接触的物理真实性。给定文本指令 $\pmb{t}$ 与物体几何 $\pmb{g}$，EigenActor 输出 $N$ 帧的身体姿态序列与物体运动序列：

$$\{ \pmb{b}_{1:N}, \dot{\pmb{o}}_{1:N} \} = \mathcal{F}(\pmb{g}, \pmb{t})$$

### BodyNet：解耦的身体姿态推理

BodyNet 采用两阶段扩散策略（Fig. 3）。第一阶段，**动作特异性运动扩散**从文本条件 $\pmb{t}$ 生成物体无关的规范身体动作序列 $\widetilde{\pmb{b}}_{1:N}$，学习共享的动作先验 $p(\widetilde{\pmb{b}} \mid \pmb{t})$。第二阶段，**物体特异性交互扩散**以文本 $\pmb{t}$ 和物体几何 $\pmb{g}$ 为联合条件，生成交互风格残差 $\widehat{\pmb{b}}_{1:N}$，学习 $p(\widehat{\pmb{b}} \mid \pmb{t}, \pmb{g})$。最终身体姿态由两者相加得到：

$$\pmb{b}_n' = \widetilde{\pmb{b}}_n' + \widehat{\pmb{b}}_n', \quad n \in \{1, \dots, N\}$$

其中交互风格残差在训练阶段定义为任意身体姿态序列与其类别内动作特异性规范姿态序列之差：$\widehat{\pmb{b}}_n = \pmb{b}_n - \widetilde{\pmb{b}}_n$。两个扩散过程均采用 Transformer 去噪器，分别以文本特征 $\pmb{f}_t$ 和文本-物体联合特征 $[\pmb{f}_t; \pmb{f}_o]$ 为条件。

### ObjectNet：物体运动规划与交互优化

ObjectNet 以 BodyNet 推断的身体姿态 $\pmb{b}'_{1:N}$、文本特征 $\pmb{f}_t$ 和物体特征 $\pmb{f}_o$ 为条件，规划 $N$ 帧物体 6-DoF 运动序列，包含三个子模块（Fig. 4）：

1. **接触部分推断**：基于文本与物体几何，预测手可接触的物体部件，生成接触置信度特征 $\pmb{f}_c$，为后续运动规划提供 affordance 引导。
2. **物体运动扩散**：以身体特征 $\pmb{f}_b$ 和接触特征 $\pmb{f}_c$ 为条件，通过扩散模型生成物体运动序列，其反向去噪步为：

$$\pmb{o}^{k-1} = \frac{1}{\sqrt{\gamma_k}} \pmb{o}^k - \sqrt{\frac{1}{\gamma_k} - 1} \, \epsilon_\gamma(\pmb{o}^k, k, \pmb{f}_b, \pmb{f}_c)$$

3. **手-物交互优化**：施加时序一致性约束与接触帧零距离约束，提升手-物交互的物理真实感。手-物距离通过高斯归一化转化为接触置信度：$\overline{d}_{n,j,p} = e^{-\frac{1}{2} \frac{d_{n,j,p}^2}{\sigma^2}}$。

### 输入输出流总结

| 阶段 | 模块 | 输入 | 输出 | 条件 |
|------|------|------|------|------|
| 身体推理 | 动作特异性运动扩散 | 随机噪声 | $\widetilde{\pmb{b}}_{1:N}$ | $\pmb{t}$ |
| 身体推理 | 物体特异性交互扩散 | 随机噪声 | $\widehat{\pmb{b}}_{1:N}$ | $\pmb{t}, \pmb{g}$ |
| 身体推理 | 姿态组合 | $\widetilde{\pmb{b}}_{1:N}, \widehat{\pmb{b}}_{1:N}$ | $\pmb{b}'_{1:N}$ | — |
| 物体推理 | 接触部分推断 | $\pmb{t}, \pmb{g}$ | $\pmb{f}_c$ | — |
| 物体推理 | 物体运动扩散 | 随机噪声 | $\dot{\pmb{o}}_{1:N}$ | $\pmb{b}'_{1:N}, \pmb{f}_c, \pmb{t}, \pmb{g}$ |
| 物体推理 | 交互优化 | $\pmb{b}'_{1:N}, \dot{\pmb{o}}_{1:N}$ | 精化后的 $\pmb{b}'_{1:N}, \dot{\pmb{o}}_{1:N}$ | 时序一致性、接触约束 |

该分解式框架的关键优势在于：动作特异性运动先验使模型在小样本场景下仍能保持语义一致性（仅用 10% 训练数据时 FID 相对基线 HIMO-Gen 降低约 50%），而物体特异性交互扩散与接触部分推断共同保障了交互的真实性与物理合理性。



EigenActor 将文本到人体-物体交互（Text-to-HOI）生成任务分解为两个核心模块：**BodyNet**（身体姿态推理）和 **ObjectNet**（物体运动规划），二者以级联方式协同工作。

### BodyNet：两阶段身体姿态推理

BodyNet 的核心创新在于将身体姿态推理显式分解为两个顺序阶段，分别建模**动作特异性运动先验**和**物体特异性交互先验**。

**第一阶段：动作特异性运动扩散（Action-specific Motion Diffusion）**

该阶段从文本条件 $\pmb{t}$ 出发，生成物体无关的规范身体动作序列 $\widetilde{\pmb{b}}_{1:N}$。其前向加噪过程定义为：

$$q\left(\widetilde{\pmb{b}}^k \ | \ \widetilde{\pmb{b}}^{k-1}\right) = \mathcal{N}\left(\sqrt{\alpha_k}\widetilde{\pmb{b}}^{k-1}, \left(1 - \alpha_k\right) I\right)$$

其中 $\alpha_k$ 为第 $k$ 步的噪声调度参数。训练目标为最小化去噪网络 $\epsilon_{\alpha}$ 的预测误差：

$$\mathcal{L}_{\widetilde{b}} = \mathbb{E}_{\epsilon, k} \left[ \left\| \epsilon - \epsilon_{\alpha} \left( \widetilde{b}^k, k, \pmb{f}_t \right) \right\|_2^2 \right]$$

$\pmb{f}_t$ 为文本特征编码，$\epsilon$ 为标准高斯噪声。该模块学习后验分布 $p(\widetilde{\boldsymbol{b}} | t)$，捕捉同类交互意图下共享的身体运动模式。

**第二阶段：物体特异性交互扩散（Object-specific Interaction Diffusion）**

该阶段以文本和物体几何形状为联合条件，生成交互风格残差 $\widehat{\pmb{b}}_{1:N}$。交互风格的形式化定义为每帧实际身体姿势与动作特异性规范姿势之差：

$$\widehat{\pmb{b}}_n = {\pmb{b}}_n - \widetilde{\pmb{b}}_n, \quad n \in \{1, \dots, N\}$$

去噪网络 $\epsilon_{\beta}$ 以文本特征 $\pmb{f}_t$ 和物体几何特征 $\pmb{f}_o$ 为条件，反向去噪步为：

$$\widehat{\pmb{b}}^{k-1} = \frac{1}{\sqrt{\beta_k}} \widehat{\pmb{b}}^k - \sqrt{\frac{1}{\beta_k} - 1} \epsilon_{\beta} ( \widehat{\pmb{b}}^k, k, \pmb{f}_t, \pmb{f}_o )$$

该模块学习后验分布 $p(\widehat{\boldsymbol{b}} | t, \boldsymbol{g})$，建模不同物体形状下交互风格的演化。

最终身体姿势由两阶段输出相加得到：

$$\pmb{b}_n' = \widetilde{\pmb{b}}_n' + \widehat{\pmb{b}}_n', \quad n \in \{1, \dots, N\}$$

### ObjectNet：接触感知的物体运动规划

ObjectNet 以 BodyNet 推断的身体姿势 $\pmb{b}'_{1:N}$、文本特征 $\pmb{f}_t$ 和物体特征 $\pmb{f}_o$ 为条件，规划 $N$ 帧物体 6-DOF 运动序列，包含三个子模块。

**接触部分推断（Contact Part Inference）**

该模块基于文本语义与物体几何，预测手可接触的物体部件。首先计算手关节 $j$ 到物体顶点 $p$ 的 L2 距离 $d_{n,j,p}$，经高斯归一化得到接触置信度：

$$\overline{d}_{n,j,p} = e^{-\frac{1}{2} \frac{d_{n,j,p}^2}{\sigma^2}}$$

接触部件预测器以二元交叉熵损失训练：

$$\mathcal{L}_c = -\sum_{p=1}^{P} \left[ \pmb{c}_p \ln \pmb{c}_p' + (1 - \pmb{c}_p) \ln(1 - \pmb{c}_p') \right]$$

其中 $\pmb{c}_p$ 为真实接触标签，$\pmb{c}_p'$ 为预测值。推断的接触部件特征 $\pmb{f}_c$ 为后续物体运动规划提供关键条件。

**物体运动扩散（Object Motion Diffusion）**

该模块以身体姿势特征 $\pmb{f}_b$ 和接触部件特征 $\pmb{f}_c$ 为条件，通过扩散模型生成物体运动序列。反向去噪步定义为：

$$\pmb{o}^{k-1} = \frac{1}{\sqrt{\gamma_k}} \pmb{o}^k - \sqrt{\frac{1}{\gamma_k} - 1} \epsilon_\gamma(\pmb{o}^k, k, \pmb{f}_b, \pmb{f}_c)$$

$\gamma_k$ 为物体运动扩散的噪声调度参数。

**手-物交互优化（Interaction Optimization）**

该模块施加两类约束以提升交互物理真实感：（1）**时序一致性约束**，确保相邻帧间物体运动平滑；（2）**接触帧零距离约束**，强制在接触时刻手与物体表面距离趋近于零。消融实验表明（Tab. 6），同时施加两类约束可获得最优性能。

### 关键设计要点

- **解耦先验的因果机制**：动作特异性运动扩散建模“做什么”的共享模式，物体特异性交互扩散建模“与什么交互”的风格差异，二者相加实现语义一致性与交互真实性的统一。
- **接触部件推断的桥梁作用**：预测的可接触部件将文本语义转化为物体几何上的空间约束，为物体运动扩散和交互优化提供关键条件信号。
- **模块化级联架构**：BodyNet 与 ObjectNet 的顺序依赖使得各阶段可独立训练与评估，消融实验中推断动作基元可接近真实基元性能（Tab. 3: Setup III R-Prec 0.66 vs Setup II 0.69），验证了分解策略的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/003_Figure_3.jpg]]
*Figure 3: BodyNet Module Overview. BodyNet factorizes the body pose reasoning task of text-to-HOI into two stages: synthesize action-specific canonical motion first and then enrich it with inferred object-specific interaction styles. With a denoising-based diffusion strategy, action-specific motion diffusion learns the conditional distribution from text-based intended semantics to its intra-class canonical 3D body motions. Object-specific interaction diffusion learns the conditional distribution from text-object joint conditions to body interaction styles*

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/004_Figure_4.jpg]]
*Figure 4: ObjectNet Module Overview. ObjectNet contains three components: contact part inference, object motion diffusion, and hand-object interaction optimization. Contact part inference analyzes object-specific hand-contactable parts for the following object-hand interaction planning. Object motion diffusion infers 3D object movements from inferred body poses and contact parts. Interaction optimization integrates inferred 3D body-object co-movements and improves the realism of the manipulation between them*



## 实验与关键发现

### 主实验结果

EigenActor在三个大规模基准数据集上进行了系统评估，涵盖HIMO、FullBodyManipulation和GRAB。所有实验均采用20次重复评估并报告95%置信区间，基线方法均使用官方开源代码和推荐超参数进行训练，确保比较公平性。

**HIMO数据集**（Table 1）：EigenActor在所有核心指标上均取得最优性能。语义一致性方面，R-Precision (Top-3) 达到0.6805，显著超越直接文本-HOI映射基线**HIMO-Gen**（Lv et al., ECCV 2024）。运动质量方面，FID降至1.1043，表明生成动作分布与真实分布高度吻合。交互真实感方面，接触精度（C_prec）达0.85，接触百分比（C_%）达0.67，验证了接触部分推断与交互优化模块的有效性。

**FullBodyManipulation与GRAB数据集**（Table 2）：EigenActor展现出良好的跨数据集泛化能力。在FullBodyManipulation上，R-Precision (Top-3) 为0.73，FID为0.62，MM-Dist为3.75，全面超越**CHOIS**（Li et al., ECCV 2024）、**InterDiff**（Xu et al., ICCV 2023）等基线。在GRAB数据集上，R-Precision (Top-3) 达0.66，进一步证明方法在不同交互类型和物体类别上的鲁棒性。

### 消融实验

消融实验系统验证了EigenActor各核心组件的贡献，所有消融均在HIMO数据集上进行。

**动作特异性运动基元**（Table 3）：实验设置三种策略对比——Setup I为无动作基元的直接生成，Setup II使用真实动作基元（上界），Setup III使用模型推断的动作基元。Setup III的R-Precision (Top-3) 达0.66，接近Setup II的0.69，显著优于Setup I的0.63。这证明解耦的动作特异性运动先验是提升语义一致性的关键瓶颈因素，且推断基元已能接近真实基元性能。

**物体特异性交互扩散的条件输入**（Table 4）：联合使用文本与物体几何作为条件输入时，R-Precision (Top-3) 为0.66；仅使用文本条件时降至0.58（降低约13%），仅使用物体条件时降至0.61（降低约8%）。这表明文本语义和物体几何对交互风格推断具有互补作用，二者缺一不可。

**接触部分推断**（Table 5）：引入推断的物体接触部件条件后，R-Precision (Top-3) 达0.66，显著优于无接触条件的0.57，且接近使用真实接触部件的0.71。该模块有效缩小了从物体几何到可接触区域的语义鸿沟，为后续物体运动规划提供了关键先验。

**手-物交互优化**（Table 6）：同时施加时序一致性约束与接触帧零距离约束时，R-Precision (Top-3) 为0.66，单独施加任一约束均比无约束基线有大幅提升。两种约束形成互补——时序一致性确保运动平滑性，接触帧零距离约束强制手部与物体在关键帧产生真实接触。

**超参数分析**（Table 7）：在8层Transformer和1000步去噪配置下，模型实现性能与推理效率的最佳平衡（R-Precision 0.66，FID 0.89，推理时间228ms）。增加层数或去噪步数带来的性能增益边际递减，但推理开销线性增长。

### 小样本学习能力

EigenActor在小样本场景下展现出显著优势（Fig. 6）。仅使用10%训练样本时，EigenActor的FID相对基线**HIMO-Gen**降低约50%，且性能下降曲线明显更为平缓。这归因于分解策略将学习问题解耦为两个子任务：动作模式基元的学习受益于同类交互意图的样本共享，降低了对样本量的依赖；物体特异性交互风格的学习则可利用预训练的动作基元作为强先验。

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/009_Figure_6.jpg]]
*Figure 6: Text-to-HOI synthesis performances with fewer training samples on HIMO*

### 定性分析与可视化

**生成多样性**（Fig. 8）：在相同文本和物体条件下，EigenActor可生成多种合理的交互样本，展现丰富的运动模式变化。

**动作特异性运动可视化**（Fig. 9）：模型推断的规范动作序列与真实规范动作高度一致，验证了动作基元学习的有效性。

**物体特异性交互可视化**（Fig. 10）：同一文本指令配对不同物体时，生成的交互风格呈现合理差异（如“举起”动作在椅子与杯子上展现不同的手臂姿态和手部构型），证明物体特异性交互扩散成功捕获了物体形状对交互风格的调制作用。

**接触推断与交互优化可视化**（Fig. 11-13）：接触部分推断模块能准确定位物体的可接触区域（如杯柄、椅背），交互优化模块显著改善手-物接触的物理真实感，消除穿透和悬空现象。

### 局限性与失败模式

尽管EigenActor取得了显著进展，仍存在以下局限：

1. **运动轨迹可控性不足**：当前方法仅从文本指令推断HOI，无法精确控制物体运动轨迹。语言描述的固有模糊性使得“将杯子向左移动”等空间指令难以被精确执行。
2. **物理约束缺失**：未考虑物体与地面的碰撞约束，可能产生漂浮或不自然的物体运动，在需要支撑面接触的场景（如“将椅子放在地上”）中尤为明显。
3. **零样本泛化未验证**：生成结果对文本输入的多样性仍依赖训练数据分布，未见在零样本物体类别上的评估，泛化边界尚不明确。

### 用户研究

用户研究（Fig. 7）表明，EigenActor在语义一致性和交互真实感两个维度上均获得显著高于各基线的偏好率，进一步验证了客观指标所反映的性能优势具有人类感知层面的有效性。

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/008_Figure_7.jpg]]
*Figure 7: User Study. Each bar indicates the preference rate of our proposed EigenActor model over other text-to-HOI synthesis methods*

### 补充图表

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/005_Table_1.jpg]]

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/010_Figure_8.jpg]]
*Figure 8: Generation Diversity Visualization. We visualize diverse HOI examples synthesized from the same given text-object condition contexts*

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/011_Table_3.jpg]]

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/012_Figure_9.jpg]]
*Figure 9: Decoupled Action-specific Motion Visualization. We visualize the synthesized and real action-specific motions of three different action categories*

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/017_Table_4.jpg]]

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/014_Table_5.jpg]]

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/013_Figure_10.jpg]]
*Figure 10: We choose two text instruction conditions and pair each of them with two different object shape conditions. Then, we respectively visualize four HOI samples synthesized from these four different textobject conditions*

![[assets/figures/papers/paper_list_l1800_EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invar/figures/020_Table_6.jpg]]



## 定位与知识库关联

### 任务定位与核心瓶颈

EigenActor 面向**文本驱动的全身人体-物体交互（Text-to-HOI）生成**任务：给定文本指令与物体三维几何，合成N帧全身人体姿态序列与物体6-DOF运动序列。该任务处于文本到运动生成、人体-物体交互理解与三维场景合成的交叉地带。

现有方法的核心瓶颈在于**单阶段直接映射**策略：从文本条件直接回归物体特异性的三维身体运动。这种端到端范式面临两个根本性困难：其一，文本语义空间与高维连续运动空间之间存在巨大的跨模态差距，导致语义一致性难以保证；其二，直接映射忽略了同一交互意图下动作模式的共享性——例如“举起椅子”与“举起杯子”封装了相似的全身发力模式，但因物体几何不同而呈现差异化的手部接触与姿态调整。现有方法将这两个因素混为一谈，迫使模型同时学习动作语义与交互细节，造成语义对齐与交互真实性的双重瓶颈。

### 核心思想：从“直接映射”到“先验分解”

EigenActor 的核心洞察是：**同一交互意图的HOI样本共享相似的动作特异性身体运动模式，但展现不同的物体特异性交互风格**。基于此，该方法将文本到HOI的推理分解为两个序贯阶段：

1. **动作特异性运动推理**：从文本条件推断物体无关的规范身体动作序列，捕捉交互意图的本质运动模式。
2. **物体特异性交互推理**：基于该动作基元，融合物体形状条件，演化出与特定物体自然交互的身体姿态。

这一分解策略的因果杠杆在于：先学习共享的动作先验，再学习物体风格先验，使模型能够分别专注于语义理解和交互细节，从而有效缩小跨模态差距并提升生成质量。

### 与现有方法的谱系关系

#### 文本到人体运动生成（Text-to-Motion）

EigenActor 在运动生成层面继承了扩散模型在人体运动合成中的成功经验。**MDM**（Tevet et al., ICLR 2022）首次将扩散模型应用于人体运动生成，**MLD**（Chen et al., CVPR 2023）进一步引入潜空间扩散以提升效率，**MotionGPT**（Jiang et al., NeurIPS 2023）探索了语言-运动统一建模。然而，这些方法仅处理独立的人体运动，不涉及物体交互。EigenActor 将扩散生成框架拓展至HOI领域，但其核心贡献不在于扩散架构本身，而在于**分解式先验建模**策略。

#### 文本到人体-物体交互生成（Text-to-HOI）

这是 EigenActor 的直接竞争领域。**HIMO-Gen**（Lv et al., ECCV 2024）作为HIMO数据集的基线方法，采用单阶段直接映射策略，是典型的端到端范式代表。**CHOIS**（Li et al., ECCV 2024）关注可控交互合成，**InterDiff**（Xu et al., ICCV 2023）引入物理信息扩散，**CG-HOI**（Diller and Dai, CVPR 2024）利用接触引导生成，**F-HOI**（Yang et al., ECCV 2024）强调细粒度语义对齐。这些方法均在单阶段框架内进行改进，通过更强的条件机制或物理约束提升生成质量，但未触及动作模式与交互风格的解耦问题。EigenActor 的分解策略与上述方法**正交互补**——理论上，其动作基元推理机制可作为插件融入其他HOI生成框架。

**Text2HOI**（Cha et al., CVPR 2024）专注于手-物交互生成，与EigenActor的全身交互定位有所重叠但在范围上更窄。

#### 接触推理与交互优化

在物体运动规划方面，EigenActor 引入了**接触部分推断**与**手-物交互优化**两个模块。接触部分推断基于文本与物体几何预测手可接触的物体部件，这一思想与 affordance 推理（如CG-HOI中的接触引导）有渊源，但EigenActor将其作为显式条件注入物体运动扩散过程。交互优化模块施加时序一致性约束与接触帧零距离约束，与物理仿真优化（如InterDiff中的物理信息损失）共享提升交互真实感的目标，但EigenActor采用后处理优化而非端到端物理仿真，在计算效率与物理精度之间做出权衡。

### 方法适用边界

**适用场景：**
- 文本描述具有明确交互意图的全身HOI生成（如“举起箱子”、“推动椅子”）。
- 已知物体三维几何的交互合成。
- 需要高语义一致性和交互真实感的生成任务。
- 小样本训练场景（仅需10%训练数据即可保持显著优势）。

**不适用或需谨慎使用的场景：**
- **精确物体轨迹控制**：当前方法仅从文本推断HOI，语言描述的模糊性使其无法精确控制物体运动轨迹。若应用需要厘米级的物体位姿规划，需额外引入轨迹约束。
- **物理碰撞约束**：未考虑物体与地面的碰撞，可能产生漂浮或不自然的物体运动。在需要严格物理仿真的场景中，需结合物理引擎后处理。
- **零样本物体泛化**：未见在训练集物体类别之外的零样本评估，对全新物体几何的泛化能力尚不明确。
- **多物体/多人交互**：当前框架针对单人物体交互设计，拓展至多物体协同操作或多人协作场景需要非平凡的架构调整。

### 局限与开放问题

**已确认的局限：**
1. **物体轨迹可控性不足**：文本指令难以精确描述空间轨迹，生成结果在物体运动路径上存在不确定性。
2. **物理约束缺失**：未建模物体-地面碰撞，可能产生物理上不可行的物体姿态。
3. **数据分布依赖**：生成多样性受限于训练数据分布，对罕见交互意图或极端物体几何的覆盖可能不足。

**值得探索的开放问题：**
1. **物理先验融合**：如何将物体位置先验（如支撑面约束）和物理碰撞约束引入扩散生成过程，在不牺牲生成多样性的前提下提升运动轨迹的可控性与真实性？
2. **端到端联合训练**：当前两阶段推理在训练上是解耦的。能否在保持分解先验优势的同时实现端到端联合优化，进一步提升动作基元与交互风格的一致性？
3. **多智能体拓展**：分解式先验策略能否自然泛化至多物体、多人交互场景？动作基元是否可以在多智能体间共享或组合？
4. **更丰富的几何表示**：当前使用点云或体素等显式几何特征。更丰富的物体表示（如隐式神经场、图神经网络编码的部件结构）是否能进一步提升交互风格的多样性和语义对齐精度？
5. **零样本泛化**：如何使模型在面对训练中未见过的物体类别时，仍能推断合理的动作基元并演化出可信的交互风格？这可能需要将物体几何理解与动作知识进行更彻底的解耦。



## 原文 PDF

![[paperPDFs/PAMI_2025/EigenActor_Variant_Body_Object_Interaction_Generation_Evolved_from_Invariant_Action_Basis_Reasoning.pdf]]

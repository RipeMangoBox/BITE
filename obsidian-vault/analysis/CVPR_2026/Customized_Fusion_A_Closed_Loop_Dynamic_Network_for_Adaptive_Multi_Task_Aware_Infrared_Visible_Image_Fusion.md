---
title: "Customized Fusion: A Closed-Loop Dynamic Network for Adaptive Multi-Task-Aware Infrared-Visible Image Fusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Customized_Fusion_A_Closed_Loop_Dynamic_Network_for_Adaptive_Multi_Task_Aware_Infrared_Visible_Image_Fusion.pdf
project_link: null
code_link: "https://github.com/YR0211/CLDyN"
aliases:
- CCLDN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 闭环优化机制中的语义传输链，通过需求驱动的语义补偿（RSC）模块，利用下游任务反馈的特征动态调整融合网络，结合奖励-惩罚策略精准适配多任务语义需求。
primary_logic: 将视觉引导融合网络（VFN）与可训练的需求驱动语义补偿（RSC）模块分离，通过冻结VFN并仅训练轻量RSC模块，使融合网络在不重新训练的情况下，依据下游任务语义反馈动态生成任务定制化融合结果。
claims:
- 在M3FD、FMB和VT5000数据集上，CLDyN在大多数融合质量指标（如Q_AB/F、Q_CB）上取得最佳，验证了视觉保真度优越。
- 在多任务性能对比中，CLDyN以仅0.46M可训练参数和174.06G FLOPs达到与重训练和联合训练方法相当甚至更优的结果，尤其在SOD任务上mFβ最高（0.8129）。
- 消融实验证实BVB和A2SI模块对多任务适应至关重要：移除BVB导致性能全面下降，固定A2SI架构引起对单一任务的偏向。
- 奖励-惩罚策略的超参数δ=5时，模型在所有下游任务上取得稳定最优性能，表明闭环优化的有效性。
---

# Customized Fusion: A Closed-Loop Dynamic Network for Adaptive Multi-Task-Aware Infrared-Visible Image Fusion

> [!tip] 核心洞察
> 将视觉引导融合网络（VFN）与可训练的需求驱动语义补偿（RSC）模块分离，通过冻结VFN并仅训练轻量RSC模块，使融合网络在不重新训练的情况下，依据下游任务语义反馈动态生成任务定制化融合结果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 定制化融合：面向自适应多任务感知的红外-可见光图像融合的闭环动态网络 |
| 英文题名 | Customized Fusion: A Closed-Loop Dynamic Network for Adaptive Multi-Task-Aware Infrared-Visible Image Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08924) · [Code](https://github.com/YR0211/CLDyN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CLDyN (Closed-Loop Dynamic Network) |
| Dataset | M3FD, FMB, M3FD, FMB, VT5000 |

> [!tip] 效果简介
> - M3FD 上，Q_AB/F ↑ 0.6900 vs 0.6601 (SMiF) (+0.0299)。
> - FMB 上，MI ↑ 2.6219 vs 2.4035 (TIMF) (+0.2184)。
> - M3FD, FMB, VT5000 (aggregated) 上，Params (M) 0.46 vs ≥46.52 (joint training methods) (参数减少>100倍)。

## 概要

现有的红外-可见光图像融合方法在面向下游任务时面临一个核心瓶颈：**当面对未经训练的下游任务网络（DTN）时，融合性能显著下降，难以同时自适应多个异构任务**。损失驱动或联合训练范式通常需要针对每个任务重新训练融合网络或DTN，缺乏对任务特定语义需求的精确、动态响应能力，导致多任务泛化受限。

针对这一问题，本文提出 **CLDyN（Closed-Loop Dynamic Network，闭环动态网络）**，其核心洞察是将视觉引导融合网络（VFN）与可训练的需求驱动语义补偿（RSC）模块解耦：**冻结预训练的VFN，仅训练轻量RSC模块**，通过闭环优化机制中的语义传输链，使融合网络在不重新训练的情况下，依据下游任务反馈的语义特征动态生成任务定制化融合结果。

**方法定位**：CLDyN属于任务感知融合方法，但区别于损失驱动（如TDAL）、语义引导（如SMiF）和联合训练（如MRFS、SAGE）等范式，它引入**闭环语义传输链 + 奖励-惩罚策略**，将多任务适应转化为一个轻量模块的单次训练问题。核心模块包括：
- **VFN**：冻结的基线融合网络，提取多模态特征并重建初始融合图像。
- **RSC模块**：包含基向量库（BVB）和架构自适应语义注入（A2SI）块，接收下游任务语义特征，对VFN中间特征进行任务特定补偿。
- **奖励-惩罚策略**：基于语义补偿前后任务性能的变化，动态优化RSC模块，结合CAGrad缓解多任务梯度冲突。

**主要结果**：在M3FD、FMB和VT5000三个数据集上，CLDyN在融合质量指标（如Q_AB/F达到0.6900，MI达到2.6219）和多任务性能上均取得领先。相比重训练和联合训练方法，CLDyN仅需**0.46M可训练参数**和**174.06G FLOPs**，参数减少超过100倍，同时在显著性目标检测（SOD）任务上取得最高mFβ（0.8129）。消融实验证实BVB和A2SI模块对多任务适应至关重要，奖励-惩罚系数δ=5时综合性能最优。



### 红外-可见光图像融合的任务驱动需求

红外与可见光图像融合旨在将热辐射信息与可见光纹理细节结合，生成兼具目标显著性和场景保真度的融合图像。随着自动驾驶、视频监控和无人机侦察等应用的发展，融合结果不再仅服务于人类视觉感知，而是越来越多地作为目标检测、语义分割、显著性检测等下游任务的输入。这一转变催生了一个核心需求：融合网络不仅需要保持高视觉质量，还必须为多个下游任务提供“任务定制化”的语义支持。

### 现有方法的三重困境

当前面向下游任务的红外-可见光融合方法可归为三类，但各自存在结构性缺陷：

**损失驱动型方法**（如 **TDAL**）通过在融合网络训练时引入任务相关损失函数来隐式引导融合方向。这类方法的瓶颈在于：损失函数仅提供弱监督信号，无法精确响应不同任务对特征语义的差异化需求；当面对未经训练的新任务时，融合结果的任务适配性急剧下降。

**语义注入型方法**（如 **SMiF**、**SAGE**）将分割或检测网络提取的语义特征通过拼接或注意力机制注入融合网络。然而，这些方法的语义注入路径是单向且静态的——下游任务的语义反馈无法反向优化融合过程，导致注入的语义与融合网络内部特征表示之间存在“语义错配”。

**联合训练型方法**（如 **MRFS**）将融合网络与下游任务网络端到端联合优化。这虽然能提升特定任务组合的性能，但代价极高：每新增一个下游任务或更换任务网络架构，都需要重新训练整个融合网络，参数量和计算开销随任务数量线性增长（可训练参数通常超过46M）。

上述方法的共同本质缺陷在于：**缺乏从下游任务到融合网络的显式闭环反馈机制**，无法根据任务的实际语义需求动态调整融合策略，导致多任务泛化能力受限。

### 本文动机：从开环注入到闭环定制

本文的核心洞察是：融合网络应当被视为一个“视觉基础模型”，其多模态特征提取能力是通用的；而任务特定的语义适配应当由一个轻量、可训练的外部模块完成，并通过下游任务的性能反馈进行闭环优化。

基于这一洞察，本文提出 **CLDyN（Closed-Loop Dynamic Network）**，其设计动机体现在三个层面：

1. **闭环语义传输链**：建立从下游任务网络到融合网络的显式反馈路径，使任务语义特征能够指导融合过程，同时任务性能变化反过来优化语义补偿策略。
2. **冻结融合网络、仅训练轻量补偿模块**：将视觉引导融合网络（VFN）冻结，仅训练需求驱动的语义补偿（RSC）模块，在保持融合质量的同时将可训练参数压缩至0.46M，实现对多任务的低成本适应。
3. **动态架构定制**：通过基向量库（BVB）和架构自适应语义注入（A2SI）模块，根据任务语义动态生成多感受野卷积核，使同一融合网络能为不同任务产生定制化的特征表示。

这一设计范式从根源上区别于现有方法的“一图多用”或“重训适配”策略，为多任务感知的图像融合提供了新的闭环动态框架。



## 核心方法与创新机理

CLDyN 的核心创新在于构建了一条**闭环语义传输链**，将下游任务的语义需求显式反馈至融合网络，从而在不重新训练视觉引导融合网络（VFN）的前提下，动态生成面向多任务的定制化融合结果。这一设计从根本上改变了现有任务感知融合方法的范式：传统方法（如损失驱动的 **TDAL** 或联合训练的 **MRFS**）需要针对每个下游任务重新训练整个融合网络或下游任务网络（DTN），导致多任务泛化成本极高；而 CLDyN 仅需训练一个轻量的需求驱动语义补偿（RSC）模块，即可同时适配目标检测、语义分割与显著性检测等多个固定任务集。

### 从单向开环到闭环反馈

现有任务感知融合方法通常采用“融合→任务”的单向开环范式（Figure 1a）：融合网络生成结果后，下游任务网络被动消费，缺乏从任务需求到融合过程的反馈通道。当面对未经训练的 DTN 时，这些方法的性能显著下降，暴露出对任务特定语义需求精确响应能力的缺失。CLDyN 通过闭环优化机制（Figure 1b）将这一范式逆转为“任务需求→融合补偿→任务验证”的闭环：下游任务网络提取的语义特征 $F_d^n$ 沿语义传输链回传至 RSC 模块，驱动对 VFN 中间特征的定制化补偿；补偿后的融合结果再次经过任务网络评估，形成奖励-惩罚信号以优化 RSC。

### 三个关键 changed slots

与现有基线相比，CLDyN 在以下三个维度上实现了结构性创新：

**1. 任务适配机制：从重训练到一次训练、多任务复用**

基线方法（如 **SAGE** 的语义注入、**IDF-TDDT** 的指令微调）要么需要为每个任务重新训练融合网络，要么依赖联合训练导致参数膨胀。CLDyN 将 VFN 冻结后，仅训练 RSC 模块（0.46M 参数，174.06G FLOPs），即可使同一融合网络动态适配多个下游任务。这一机制的核心在于奖励-惩罚策略：若语义补偿后任务性能提升，则给予奖励（$\ell_r^n$）；若补偿后性能反而不如初始融合结果，则施加惩罚（$\ell_p^n$），迫使 RSC 学习真正有益于任务的语义注入方式。

**2. 语义注入方式：从静态拼接/注意力到动态架构选择**

传统语义注入方式（如直接拼接、通道注意力加权或特征共享）采用固定的特征融合策略，难以适应不同任务对感受野和语义粒度的差异化需求。CLDyN 的 **A2SI 块** 通过卷积配置选择矩阵 $S$ 动态决定每个分支的卷积核尺寸与膨胀率组合，实现多感受野自适应语义提取。同时，**BVB（基向量库）** 将任务语义投影到一组可学习的基向量上，生成任务特定的卷积核参数 $W_m^{k,d}$，使同一模块能够为不同任务实例化不同的卷积行为。

**3. 多任务优化策略：从简单加权到性能反馈驱动的奖励-惩罚**

多任务学习中常见的简单损失加权容易导致任务间梯度冲突，且无法反映语义补偿的实际效果。CLDyN 的闭环优化目标 $\ell_{cl}^n = \ell_r^n + \delta \ell_p^n$ 直接以补偿前后的任务性能变化作为优化信号，而非预设的损失权重。结合 **CAGrad** 缓解多任务梯度冲突，超参数 $\delta=5$ 时模型在所有下游任务上取得稳定最优，证实了该策略对任务平衡的有效调控。



**CLDyN** 采用两阶段闭环范式，将视觉引导融合网络（VFN）与需求驱动的语义补偿（RSC）模块解耦，形成一条从下游任务语义反馈到融合特征调整的**语义传输链**（Figure 2）。其核心设计在于：VFN 仅需训练一次并保持冻结，而轻量级的 RSC 模块通过接收下游任务网络（DTN）的语义特征，对 VFN 中间层多模态特征进行任务特定的动态补偿，从而在无需重新训练融合网络的前提下，为多个下游任务生成定制化融合结果。

### 两阶段工作流

**第一阶段：VFN 预训练。** VFN 以红外图像 $I_{ir}$ 和可见光图像 $I_{vi}$ 为输入，经特征提取与重建输出初始融合图像 $I_f$ 及多层中间特征 $\{F_{ir/vi}^l\}_{l=1}^{L-1}$。训练仅依赖融合损失 $\ell_f$，该损失在像素和梯度两个层面约束融合图像与源图像最大值的 L1 一致性（Eq 1）。VFN 训练完成后冻结全部参数 $\theta_{\Phi}^*$，作为后续闭环优化的固定骨架。

**第二阶段：闭环优化。** 冻结的 VFN 生成初始融合结果后，DTN 对该结果进行任务预测并提取高层语义特征 $F_d^n$。RSC 模块以 $F_d^n$ 为条件，对 VFN 各层多模态特征 $\{F_{ir/vi}^l\}_{l=1}^{L-1}$ 执行语义补偿，生成任务调整后的特征 $\{F_{irs/vis}^{l,n}\}_{l=1}^{L-1}$，进而重建任务定制化的融合图像 $I_{fs}^n$。**奖励-惩罚策略**（Reward-Penalty Strategy）根据补偿前后 DTN 性能的变化计算闭环优化目标 $\ell_{cl}^n$（Eq 7），驱动 RSC 模块学习如何精准适配各任务语义需求。多任务梯度冲突通过 **CAGrad** 算法缓解。

### 核心模块关系

| 模块 | 角色 | 可训练性 |
|------|------|----------|
| **VFN**（Vision-guided Fusion Network） | 提取多模态特征并重建初始融合图像 | 冻结 |
| **RSC**（Requirement-driven Semantic Compensation） | 接收 DTN 语义反馈，对 VFN 中间特征进行任务特定补偿 | 可训练（仅 0.46M 参数） |
| **DTNs**（Downstream Task Networks） | 提供任务预测与语义特征反馈（YOLOv5s、SegFormer、CTDNet-18） | 冻结 |
| **奖励-惩罚策略** | 基于补偿前后性能变化计算优化信号 | 策略层，无参数 |

RSC 模块内部由两个关键组件构成：
- **BVB（Basis Vector Bank）**：生成任务特定的动态卷积核基向量，为后续多分支语义提取提供参数化基础。
- **A2SI（Architecture-Adaptive Semantic Injection）**：利用 BVB 输出的基向量预测多分支卷积配置（Eq 8-11），在多个感受野上并行提取任务语义信息，最终通过残差注入方式将聚合后的任务特定特征叠加回原始多模态特征（Eq 12），实现架构自适应的语义注入。

### 输入输出流

1. 红外 $I_{ir}$ 与可见光 $I_{vi}$ 输入冻结的 VFN → 初始融合图像 $I_f$ + 中间特征 $\{F_{ir/vi}^l\}$
2. $I_f$ 送入各 DTN → 任务预测 $\hat{y}_f^n$ + 语义特征 $F_d^n$
3. $F_d^n$ 与 $\{F_{ir/vi}^l\}$ 输入 RSC → 任务定制化特征 $\{F_{irs/vis}^{l,n}\}$ → 定制化融合图像 $I_{fs}^n$ → 任务预测 $\hat{y}_{fs}^n$
4. 比较 $\hat{y}_f^n$ 与 $\hat{y}_{fs}^n$ 的性能变化 → 计算奖励 $\ell_r^n$ 与惩罚 $\ell_p^n$（Eq 6）→ 闭环优化 RSC

该框架的关键优势在于：VFN 作为通用融合骨架保持稳定，所有任务适应性学习被压缩至轻量 RSC 模块中，使得整个系统在面对未经训练的 DTN 时仍能通过语义传输链动态调整，无需重新训练融合网络。

### 补充图表

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the adaptive multi-task-aware infrared-visible image fusion network. The network forms a semantic transmission chain, where semantic features from multiple downstream tasks guide the RSC module to perform task-specific compensation for the VFN. The reward-penalty strategy optimizes the compensation process by evaluating task performance before and after semantic compensation*



### 两阶段训练框架

CLDyN 的整体训练分为两个阶段。第一阶段训练一个**视觉引导融合网络**（Vision-guided Fusion Network, VFN），用于从红外与可见光图像中提取多模态特征并重建初始融合图像 $\boldsymbol{I}_f$。第二阶段冻结 VFN 的所有参数，引入**闭环优化机制**，通过一个轻量的**需求驱动语义补偿模块**（Requirement-driven Semantic Compensation, RSC）接收下游任务的语义反馈，对 VFN 的中间特征进行任务定制化补偿。

这一分离设计的核心洞察在于：融合网络本身保持通用视觉保真度，而任务适配能力完全由可训练的 RSC 模块承担，从而避免了为每个下游任务重新训练整个融合网络的巨大开销。

### 视觉引导融合网络与融合损失

VFN 以红外图像 $\boldsymbol{I}_{ir}$ 和可见光图像 $\boldsymbol{I}_{vi}$ 为输入，输出初始融合图像 $\boldsymbol{I}_f$ 及多尺度中间特征 $\{\mathbf{F}_{ir/vi}^l\}_{l=1}^{L-1}$。其训练目标为融合损失 $\ell_f$：

$$
\ell _ { f } = \| \boldsymbol { I } _ { f } - \operatorname* { m a x } ( \boldsymbol { I } _ { i r } , \boldsymbol { I } _ { v i } ) \| _ { 1 } + \lambda \| \nabla \boldsymbol { I } _ { f } - \operatorname* { m a x } ( \nabla \boldsymbol { I } _ { i r } , \nabla \boldsymbol { I } _ { v i } ) \| _ { 1 }
$$

该损失在像素层面和梯度层面同时约束融合图像与源图像最大值的 L1 一致性，$\lambda$ 平衡两项的权重。VFN 训练完成后参数 $\theta_{\Phi}^*$ 被完全冻结。

### 闭环优化机制与奖励-惩罚策略

闭环优化的核心是一条**语义传输链**：下游任务网络（DTN）对初始融合图像 $\boldsymbol{I}_f$ 进行预测，提取任务语义特征 $\mathbf{F}_d^n$（第 $n$ 个任务），RSC 模块据此对 VFN 中间特征进行补偿，生成任务定制化特征 $\{\mathbf{F}_{irs/vis}^{l,n}\}$，进而重建补偿后的融合图像 $\boldsymbol{I}_{fs}^n$。DTN 再次对 $\boldsymbol{I}_{fs}^n$ 进行预测，通过比较补偿前后的任务性能变化来优化 RSC。

具体而言，奖励损失 $\ell_r^n$ 和惩罚损失 $\ell_p^n$ 定义为：

$$
\begin{array}{ r l } & {\ell _ { r } ^ { n } = c ^ { n } ( \hat { \pmb { y } } _ { f s } ^ { n } , \pmb { y } _ { G T } ^ { n } ) , } \\ & {\ell _ { p } ^ { n } = \operatorname* { m a x } \big ( 0 , c ^ { n } ( \hat { \pmb { y } } _ { f s } ^ { n } , \pmb { y } _ { G T } ^ { n } ) - c ^ { n } ( \hat { \pmb { y } } _ { f } ^ { n } , \pmb { y } _ { G T } ^ { n } ) \big ) } \end{array}
$$

其中 $c^n(\cdot, \cdot)$ 为第 $n$ 个任务的评价指标（如检测的 mAP、分割的 mIoU），$\hat{\pmb{y}}_f^n$ 和 $\hat{\pmb{y}}_{fs}^n$ 分别为补偿前后 DTN 的预测结果。奖励损失直接取补偿后的任务误差，惩罚损失仅在补偿后性能**差于**补偿前时激活，取性能退化的幅度。

第 $n$ 个任务的闭环优化目标为：

$$
\ell _ { c l } ^ { n } = \ell _ { r } ^ { n } + \delta \ell _ { p } ^ { n }
$$

其中 $\delta$ 为惩罚系数，控制对性能退化的惩罚强度。消融实验证实 $\delta=5$ 时模型在所有下游任务上取得稳定最优性能（Table 9）。多任务优化时，采用 **CAGrad** 缓解各任务梯度间的冲突。

### 需求驱动语义补偿模块

RSC 模块由**基向量库**（Basis Vector Bank, BVB）和**架构自适应语义注入块**（Architecture-Adaptive Semantic Injection, A2SI）两部分组成，其语义补偿过程可形式化为：

$$
\{ \mathbf { } F _ { i r s / v i s } ^ { l , n } \} _ { l = 1 } ^ { L - 1 } = \operatorname { R S C } ( \{ \mathbf { } F _ { i r / v i } ^ { l } \} _ { l = 1 } ^ { L - 1 } , \mathbf { } F _ { d } ^ { n } ; \theta _ { \Psi } )
$$

#### 基向量库

BVB 存储一组可学习的基向量，用于根据任务语义生成任务特定的动态卷积核。每个基向量对应一种卷积配置（如不同膨胀率、不同核尺寸），使 A2SI 能够灵活组合多种感受野来提取任务语义。

#### 架构自适应语义注入块

A2SI 块是 RSC 的核心计算单元（结构见 Figure 3）。对于第 $l$ 层的多模态特征 $\mathbf{F}_{ir/vi}^l$ 和任务语义 $\mathbf{F}_d^n$，首先通过投影层对齐特征空间，然后计算**卷积配置选择矩阵** $S$：

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the A2SI block. The A2SI block comprises six projection layers*

$$
S = \mathrm { S o f t m a x } \big ( p \times \mathrm { R e s h } ( P r o j _ { 3 } ( [ P r o j _ { 1 } ( F _ { i r / v i } ^ { l } ) , P r o j _ { 2 } ( F _ { d } ^ { n } ) ] ) ) \big )
$$

该矩阵为 $M$ 个分支产生 4 种卷积配置的选择概率，实现**动态架构选择**——不同任务、不同层可自适应地激活不同的卷积配置组合。

每个分支 $m$ 根据其选择的卷积配置预测卷积核 $\mathcal{W}_m^{k,d}$，并行提取任务特定语义信息。所有分支的输出经平均池化后注入原始特征，得到任务定制化特征：

$$
{ { \mathcal { F } } _ { i r s / v i s } ^ { l , n } } = { { \mathcal { F } } _ { i r / v i } ^ { l } } + \frac { 1 } { M } \sum _ { m = 1 } ^ { M } ( { W _ { m } ^ { k , d } } * { { \mathcal { F } } _ { i r / v i } ^ { l } } )
$$

消融实验（Table 7, Figure 11）证实：移除 BVB 导致所有下游任务性能全面下降；将 A2SI 分支结构固定（取消自适应调整）则使模型偏向目标检测任务，多任务适应性显著恶化。这验证了动态架构选择与基向量生成机制对多任务泛化的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative and quantitative comparison between precompensation and post-compensation results*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/016_Figure_9.jpg]]
*Figure 9: Network architecture of VFN. The VFN (a) consists of a Feature Extraction Blocks (FEB) (b) and a Fusion Feature Reconstruction Block (FRB) (c)*



## 实验与关键发现

### 融合质量评估

为验证CLDyN在图像融合层面的视觉保真度，论文在M3FD、FMB和VT5000三个数据集上与多种现有方法进行了定量对比，结果汇总于Table 1。CLDyN在绝大多数融合质量指标上取得最优或次优成绩：在M3FD上，Q_AB/F达到0.6900（对比SMiF的0.6601）；在FMB上，MI达到2.6219（对比TIMF的2.4035）；在VT5000上，Q_CV达到0.7883。这些结果表明，闭环语义补偿机制在提升下游任务性能的同时，并未损害融合图像的视觉质量，反而通过任务语义的反馈增强了关键信息的保留。

### 多任务适应性与效率对比

论文的核心实验围绕“多任务适应效率”展开，将CLDyN与两类主流范式进行对比：任务网络重训练方法和联合训练方法。

**与重训练方法的对比（Table 2）**：重训练方法先使用通用融合结果训练下游任务网络（DTN），再对每个任务单独重新训练DTN。CLDyN以仅0.46M可训练参数和174.06G FLOPs，在目标检测（mAP50→95=0.6304）、语义分割（mIoU=60.34）、显著性检测（mFβ=0.8129）和边缘检测（Em=0.9087）四个任务上全面达到最优或次优。相比之下，重训练方法需要为每个任务分别训练完整的DTN，参数规模通常在46M以上，且多任务间无法共享融合优化信号。

**与联合训练方法的对比（Table 3）**：联合训练方法（如MRFS、SAGE）在训练过程中同时优化融合网络和DTN，虽然多任务性能较强，但可训练参数量巨大（SAGE需46.52M，MRFS需60.84M），且一旦DTN配置变化就需要重新训练整个流水线。CLDyN通过冻结VFN、仅训练轻量RSC模块，以约1/100的参数量达到与联合训练方法相当甚至更优的多任务性能，尤其在SOD任务上mFβ最高（0.8129 vs SAGE的0.8093）。

**与IDF-TDDT的对比（Figure 6）**：IDF-TDDT是一种任务指令微调的多任务适应方法。CLDyN在融合质量和多任务性能上均表现更优，验证了闭环语义传输链相比简单指令微调在多任务语义精确响应上的优势。

### 消融实验

**BVB与A2SI的必要性（Table 7, Figure 11）**：移除BVB后，模型在所有下游任务上性能全面下降，融合结果的纹理细节和热辐射信息保留变差，证明基向量库生成的任务特定卷积核对语义补偿至关重要。固定A2SI分支结构（取消自适应架构选择）导致模型偏向目标检测任务，在其他任务上的适应性显著下降，说明动态架构选择是多任务平衡的关键机制。

**语义补偿前后对比（Figure 7）**：论文对比了语义补偿前后的融合结果与任务性能。补偿后的融合图像在目标区域（如行人、车辆）的对比度和边缘清晰度显著增强，检测置信度和分割精度均有提升，直观验证了RSC模块的任务定制化效果。

**超参数δ分析（Table 9）**：奖励-惩罚系数δ控制惩罚项对闭环优化的影响强度。实验表明δ=5时模型在所有下游任务上取得稳定最优性能；δ过小（δ=1）时惩罚信号不足，任务适应能力减弱；δ过大（δ=10）时惩罚项主导优化，导致任务间性能失衡。这证实了奖励-惩罚策略的有效性及其对超参数的合理敏感性。

**其他消融（Table 8, Table 10, Table 11）**：论文还对补偿层数L、分支数M和特征维度e2进行了系统分析，验证了所选配置（L=3, M=4, e2=64）在性能与开销间的良好平衡。

### 跨检测器泛化

为验证RSC模块对不同DTN架构的泛化能力，论文在YOLOv5s和YOLOv11上进行了跨检测器实验（Table 4, Table 6）。CLDyN在两种检测器上均取得最优结果，且性能差距微小（YOLOv5 mAP50→95=0.6304，YOLOv11 mAP50→95=0.6321），表明RSC模块学习到的语义补偿策略对不同检测架构具有鲁棒的迁移能力。

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/013_Table_4.jpg]]
*Table 4: Quantitative results of cross-detector generalization*

### 失败模式与局限性

论文在Table 13中分析了CLDyN在复杂场景下的性能表现。在正常光照条件下，CLDyN的检测和分割性能稳定领先；但在模拟的暴雨、低光照和强噪声等恶劣环境下，性能下降幅度较明显。这表明当前方法假设输入图像来自正常天气条件，对极端环境的鲁棒性有限。此外，论文未考虑传感器老化导致的复合退化（噪声、坏点、伪影），这在实际部署中可能成为瓶颈。未来工作需拓展至开放世界复杂环境下的鲁棒多任务适应。

### 补充图表

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison between the proposed method and existing state-of-the-art approaches. The best and second-best performances for each metric are highlighted with Red and Blue backgrounds, respectively*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of the proposed method with the “task network retraining” methods. The number of parameters and the computational cost of the trainable parts are reported in the table. The best and second-best performances for each metric are highlighted with Red and Blue backgrounds*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison of the proposed method with the “joint training” methods. The number of parameters and the computational cost of the trainable parts are reported in the table. The best and second-best performances for each metric are highlighted with Red and Blue backgrounds, respectively*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/015_Table_7.jpg]]
*Table 7: Quantitative comparison between the full model and its ablated variants across multiple downstream tasks. The best performance for each metric is marked with a Red background*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/021_Table_9.jpg]]
*Table 9: Quantitative analysis of the hyperparameter δ across multiple downstream tasks. The hyperparameter settings of our proposed method are highlighted in bold, while the best performance for each metric is marked with a Red background*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative (a) and quantitative (b) comparison between the proposed method and IDF-TDDT*

![[assets/figures/papers/paper_list_l2116_https_arxiv_org_abs_2604_08924/figures/019_Figure_11.jpg]]
*Figure 11: Qualitative comparison between the full model and the ablation models (Model IV and Model V)*



## 定位与知识库关联

### 1. 任务感知融合方法的演进脉络

红外-可见光图像融合与下游任务的协同优化经历了从“分离处理”到“任务感知融合”的范式迁移。传统融合方法（如 **CoCo** ）仅关注视觉保真度，将融合与任务完全解耦，导致融合结果对后续检测、分割等任务并非最优。为弥补这一鸿沟，研究者提出了三类任务感知融合策略：

**损失驱动型任务感知**：以 **TDAL** 为代表，通过在融合损失中引入任务相关项（如检测损失、分割损失）间接引导融合网络关注任务语义。这类方法虽然提升了下游性能，但损失函数的线性组合难以精确控制语义注入的方向和强度，导致多任务平衡困难。

**语义引导型任务感知**：**SMiF** 和 **SAGE** 等方法将任务网络提取的语义特征直接注入融合网络（如通过拼接、注意力加权或SAM引导的特征调制）。这类方法实现了更直接的语义交互，但语义注入方式固定，无法根据任务需求动态调整网络架构，导致对不同任务的适应性存在偏置。

**联合训练型多任务融合**：**MRFS** 和 **IDF-TDDT** 等方法将融合网络与下游任务网络联合训练，通过特征共享或任务指令微调实现多任务适应。然而，这类方法需要针对每个任务组合重新训练整个融合网络，参数量和计算开销巨大（可训练参数通常超过46.52M），且当面对未经训练的DTN时性能显著下降。

### 2. CLDyN的方法学突破与定位

CLDyN的核心创新在于**将融合网络与任务适应机制解耦**，构建了一个“一次训练、多任务动态适配”的闭环框架。其方法学定位可从三个维度理解：

**解耦式闭环优化**：与联合训练方法（MRFS、IDF-TDDT）不同，CLDyN将视觉引导融合网络（VFN）冻结为不可训练的基线，仅通过轻量级的需求驱动语义补偿（RSC）模块（0.46M参数）接收下游任务反馈。这一设计使得融合网络无需针对不同任务重新训练，仅需训练一次RSC即可适应固定的多任务集合，参数开销降低超过100倍（Table 2 & Table 3）。

**动态架构自适应**：与固定语义注入方式（SMiF、SAGE）不同，CLDyN的A2SI块通过基向量库（BVB）生成任务特定的动态卷积核，实现多感受野的自适应语义提取。BVB存储了一组可学习的卷积基向量，与任务语义特征交互后预测M个分支的卷积配置（核大小k∈{1,3,5,7}、膨胀率d∈{1,3,5}），使网络架构随任务需求动态调整（Figure 3, Eq (8)-(12)）。消融实验证实，固定A2SI分支结构会导致模型偏向目标检测任务，多任务适应性显著下降（Table 7, Figure 11）。

**奖励-惩罚多任务平衡**：CLDyN的闭环优化目标$\ell_{cl}^n = \ell_r^n + \delta \ell_p^n$（Eq (7)）通过比较语义补偿前后的任务性能变化，对性能提升给予奖励、对性能下降施加惩罚（Eq (6)），并结合CAGrad缓解多任务梯度冲突。超参数δ=5时模型在所有下游任务上取得稳定最优（Table 9），验证了该策略的有效性。

### 3. 适用边界与局限

CLDyN的适用性受以下条件约束：

**环境鲁棒性有限**：方法假设输入红外与可见光图像在正常天气条件下获取。在暴雨、低光照、强噪声等恶劣环境下，VFN提取的多模态特征可能退化，RSC模块的语义补偿能力随之受限（Table 13）。该问题需手动验证——原文仅报告了曝光衰减场景的性能下降，未系统评估极端天气的鲁棒性。

**传感器退化未建模**：当前框架未考虑传感器老化引起的复合退化（噪声、坏点、伪影），这在实际部署中可能导致融合质量与任务性能的同步衰退。

**任务集合固定**：CLDyN的RSC模块针对预定义的固定任务集（目标检测、语义分割、显著性检测）训练，不支持运行时动态添加新的下游任务。若需扩展至新任务，需重新训练RSC模块。

### 4. 开放问题与未来方向

基于上述局限，CLDyN框架面临以下开放问题：

1. **极端环境鲁棒性**：如何在暴雨、低光照、强噪声等恶劣天气下保持多任务适应的鲁棒性？可能的路径包括在VFN训练阶段引入数据增强或设计环境感知的特征补偿机制。

2. **复合退化处理**：如何处理传感器老化引起的复合退化（噪声、坏点、伪影）？这可能需要将退化建模融入闭环优化框架，或设计退化自适应的RSC模块。

3. **计算效率与任务扩展性**：能否进一步减少RSC模块的计算开销（当前174.06G FLOPs），或使框架支持任意新增的下游任务而无需重新训练？后者可能涉及元学习或任务编码器的引入，使RSC能够泛化至未见任务。

4. **任务冲突的理论分析**：CAGrad虽然缓解了梯度冲突，但多任务语义需求的内在冲突（如检测关注边缘、分割关注区域一致性）是否可通过更优的语义注入策略从根本上调和，仍需进一步研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Customized_Fusion_A_Closed_Loop_Dynamic_Network_for_Adaptive_Multi_Task_Aware_Infrared_Visible_Image_Fusion.pdf]]

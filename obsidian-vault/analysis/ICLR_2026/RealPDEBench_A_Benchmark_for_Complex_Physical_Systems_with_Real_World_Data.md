---
title: "RealPDEBench: A Benchmark for Complex Physical Systems with Real-World Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RealPDEBench_A_Benchmark_for_Complex_Physical_Systems_with_Real_World_Data.pdf
project_link: https://realpdebench.github.io/
code_link: null
openreview_forum_id: y3oHMcoItR
aliases:
- RB
- RealPDEBench
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "构建配对的真实物理实验数据与数值模拟数据，定义三种训练范式（仅真实训练、仅模拟训练、模拟预训练后真实微调）并设计面向数据和物理的九项评估指标，系统性地量化模拟与真实之间的差距，并检验利用模拟数据提升真实预测的可行性。"
primary_logic: "直接在模拟数据上训练的模型难以泛化到真实数据，而通过模拟数据预训练再结合少量真实数据微调，不仅能大幅提升预测精度和加快收敛速度，而且能有效利用模拟数据中丰富的动态信息，为弥合sim-to-real鸿沟提供了可靠路径。"
claims:
- "模拟训练与真实训练之间存在显著性能差距，真实训练在Rel L2上的提升幅度达9.39%-78.91%。"
- "真实微调（模拟预训练+真实数据）在不同数据集和基线模型上均优于仅使用相同量真实数据从头训练。"
- "真实微调的更新比率（Update Ratio）普遍小于1，表明预训练能显著加快收敛，减少达到同等性能所需的迭代次数。"
- "在Cylinder数据集上，大规模预训练模型DPOT-L-FT在真实微调后取得最低RMSE 0.0394和Rel L2 0.0733。"
---

# RealPDEBench: A Benchmark for Complex Physical Systems with Real-World Data

> [!tip] 核心洞察
> 直接在模拟数据上训练的模型难以泛化到真实数据，而通过模拟数据预训练再结合少量真实数据微调，不仅能大幅提升预测精度和加快收敛速度，而且能有效利用模拟数据中丰富的动态信息，为弥合sim-to-real鸿沟提供了可靠路径。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RealPDEBench：基于真实数据的复杂物理系统基准 |
| 英文题名 | RealPDEBench: A Benchmark for Complex Physical Systems with Real-World Data |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=y3oHMcoItR) · [Project](https://realpdebench.github.io/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | RealPDEBench Benchmark |
| Dataset | Cylinder, Controlled Cylinder, Combustion, Cylinder (autoregressive) |

> [!tip] 效果简介
> - Cylinder 上，Update Ratio (simulated pretraining + finetuning vs. real-world training from scratch) 为 0.3636 (U-Net, Real-world Finetuning)，对比 1.0 (Real-world Training from scratch)，变化 -63.64%。
> - Controlled Cylinder 上，Relative L2 Error (Real-world Finetuning best vs. Simulated Training best) 为 0.0223 (U-Net, Real FT)，对比 0.1849 (CNO, Sim Training)，变化 -87.9%。
> - Combustion 上，Validation RMSE convergence (Real FT vs. Real Training) 为 Much faster decrease and better final RMSE (Figure 3b)，对比 Slower convergence and higher best RMSE from Real Training，变化 Qualitative, Figure 3b。

## 概要

科学机器学习在物理系统建模中面临一个根本性瓶颈：真实实验数据采集昂贵且稀缺，大量模型仅依赖数值模拟数据进行训练和验证，无法可靠评估其在真实物理场景中的表现。这一模拟-真实（sim-to-real）鸿沟严重制约了从仿真迁移到实际应用的关键研究。**RealPDEBench** 正是针对这一瓶颈构建的基准数据集与评测框架。

该基准的核心设计思路是：针对同一物理系统，同时采集真实实验测量数据与对应的数值模拟数据，形成配对数据集。在此基础上，定义了三种训练范式——**仅真实训练、仅模拟训练、模拟预训练后真实微调**——并设计了涵盖数据精度与物理一致性的九项评估指标，系统性地量化模拟与真实之间的差距，并检验利用模拟数据提升真实预测的可行性。

RealPDEBench 的核心洞察是：直接在模拟数据上训练的模型难以泛化到真实数据（真实训练在 Rel L2 上的提升幅度可达 9.39%–78.91%），但通过模拟数据预训练再结合少量真实数据微调，不仅能大幅提升预测精度、加快收敛速度，而且能有效利用模拟数据中丰富的动态信息。这一发现为弥合 sim-to-real 鸿沟提供了可靠路径。

在实验设计上，RealPDEBench 覆盖了流体动力学和燃烧领域的五个场景，提供超过 700 条轨迹（每条超过 2000 帧），并评估了十种代表性基线模型——从传统降阶模型 **DMD**（Kutz et al., 2016）到 CNN 架构 **U-Net**、神经算子方法 **FNO**（Li et al., 2021）、**DeepONet**（Lu et al., 2021）、**CNO**（Raonic et al., 2023），以及大规模预训练 PDE 基础模型 **DPOT**（Hao et al., 2024）等。主要实验结果表明：在 Cylinder 数据集上，大规模预训练模型 DPOT-L-FT 经真实微调后取得最低 RMSE 0.0394 和 Rel L2 0.0733；在 Controlled Cylinder 上，真实微调的最佳 Rel L2（0.0223）相比模拟训练最佳结果（0.1849）降低了 87.9%；真实微调的更新比率（Update Ratio）普遍小于 1，表明预训练能显著加快收敛。

当前基准的局限在于范围仍集中于流体与燃烧系统，尚未覆盖电磁学、结构力学等其他物理领域，也未针对燃烧系统引入专门的物理导向指标，且缺乏对强分布外工况的系统探索。这些方向为后续扩展留下了明确空间。



科学机器学习（SciML）在偏微分方程求解、物理场预测等任务中取得了显著进展，但其核心瓶颈正从模型设计转向数据层面：**真实物理实验数据极度稀缺且采集成本高昂**。当前绝大多数SciML模型——包括各类神经算子、Transformer架构乃至大规模预训练基础模型——均在纯模拟数据上训练和验证，缺乏对真实物理场景的可靠评估。这导致一个关键问题悬而未决：在模拟数据上表现优异的模型，部署到真实世界时是否依然有效？

模拟数据与真实数据之间存在本质性鸿沟。真实实验数据包含测量噪声、边界条件不确定性、多物理场耦合效应以及传感器模态限制等复杂因素，而数值模拟即使采用高精度CFD方法，也难以完全复现这些真实世界的“脏”特征。图1直观展示了五个场景下真实数据与模拟数据的差异——模态不同、噪声分布不同、数值误差模式不同。这些差异使得**sim-to-real迁移**成为SciML走向实际应用的核心挑战，但长期以来缺乏系统性的基准来量化这一差距。

现有基准工作存在明显缺口：它们要么仅提供模拟数据，要么仅提供真实数据，缺乏**配对**的模拟-真实数据来支撑对比分析。同时，评估指标多局限于逐点误差（如RMSE、相对L2），忽略了物理一致性——例如周期性特征的频率保真度、湍流动能误差、长期自回归预测的时均速度剖面偏差等。这些问题使得学界难以回答一个根本性问题：**利用大量廉价模拟数据能否有效提升真实场景下的预测能力？如果能，最佳迁移策略是什么？**

RealPDEBench正是为填补这一空白而构建。它系统性地采集了五个场景（Cylinder、Controlled Cylinder、FSI、Foil、Combustion）下超过700条轨迹、每条超2000帧的配对真实-模拟数据，覆盖流体动力学和燃烧两大领域。在此基础上，该基准定义了三种训练范式——仅真实训练、仅模拟训练、模拟预训练后真实微调——并设计了九项评估指标，从数据精度和物理一致性两个维度全面量化模型表现，为sim-to-real迁移研究提供了首个标准化测试平台。



## 核心方法与创新机理

RealPDEBench的核心创新不在于提出新的模型架构或训练算法，而在于**构建了首个基于真实物理实验数据的系统化评估基准**，并以此重新定义了科学机器学习模型的能力检验方式。

### 创新一：以真实数据为锚点的评估范式

当前科学机器学习领域面临一个根本性瓶颈：**真实物理数据稀少且采集成本高昂**，绝大多数模型仅在数值模拟数据上进行训练和验证，无法可靠评估其在真实物理场景中的表现。RealPDEBench直接回应了这一挑战——它采集了超过700条真实物理实验轨迹（每条超过2000帧），覆盖五种不同工况场景，并配以对应的数值模拟数据，使模型在真实数据上的泛化能力成为可量化、可比较的指标。

这一设计使得基准能够揭示一个此前被忽视的关键事实：**直接在模拟数据上训练的模型，在真实测试集上的相对L2误差比真实数据训练高出9.39%至78.91%**（Table 1，Section 4.2）。这一差距在不同模型和数据集上普遍存在，构成了“模拟-真实鸿沟”（sim-to-real gap）的定量证据。

### 创新二：三种训练范式的对比框架

RealPDEBench定义了三种训练设置（Section 3.1）：
- **真实训练**：直接在少量真实数据上训练
- **模拟训练**：在大量模拟数据上训练
- **模拟预训练 + 真实微调**：先在大规模模拟数据上预训练，再用少量真实数据微调

这并非简单的实验设计变体，而是**直接检验一个核心假设：模拟数据中的物理知识能否迁移到真实场景**。实验结果表明，模拟预训练加真实微调的策略在所有数据集和基线模型上均优于仅使用等量真实数据从头训练（Table 1），且更新比率（Update Ratio）普遍低于1，意味着预训练显著加速了收敛（Section 4.3）。这一发现为弥合sim-to-real鸿沟提供了可靠路径。

### 创新三：面向物理一致性的多维度评估

现有基准多局限于数据驱动的误差指标（如RMSE、MAE），而RealPDEBench引入了**物理导向的评估指标**，包括频率误差（FE）、动能误差（KE）和平均速度剖面误差（MVPE），从周期性、能量守恒和长期统计特性三个维度检验预测的物理合理性（Section 3.3.2）。

以频率误差为例，Figure 3a显示模拟训练的模型在频率域表现出远高于真实训练的误差，说明仅靠数据层面的拟合无法保证物理一致性。Figure 4进一步揭示了RMSE与频率误差之间的权衡关系——某些模型在RMSE上表现优异，却在频率域出现较大偏差，这种“数据-物理”的张力在传统基准中完全不可见。

### 创新四：面向真实数据特性的训练策略适配

RealPDEBench并非仅仅“收集数据然后跑模型”。针对真实数据与模拟数据之间的模态差异（如PIV测量仅获取二维速度场，而CFD可提供三维全场信息），基准设计了两种适配策略（Section 4.1-4.2）：
- **噪声注入**：向模拟数据添加噪声以逼近真实数据的分布特性
- **模态掩码**：随机遮蔽模拟数据中真实世界不可测的物理量，迫使模型学习利用可用的动态信息

这些策略并非独立的模型创新，而是**基准本身对sim-to-real迁移问题的系统性回应**，为后续研究提供了明确的改进方向。

### 与现有工作的本质差异

现有PDE基准（如PDEBench、PDEArena）的评估完全建立在数值模拟数据之上，其“性能”仅反映模型对数值求解器的逼近能力。RealPDEBench将评估锚点从模拟转移到真实物理世界，揭示出**模型在模拟数据上的优越表现并不能保证其在真实场景中的有效性**——这一发现对科学ML领域的方法论具有根本性的警示意义。



RealPDEBench 的核心 pipeline 由五个功能模块串联而成，形成从数据获取到模型评估的完整闭环。

**数据采集与生成**是 pipeline 的起点。真实数据通过粒子图像测速（PIV）技术在水洞中采集流体系统速度场，燃烧系统则采用化学发光（CL）成像获取火焰强度分布（Section 3.2, Figure 2）。对应的模拟数据则采用计算流体动力学（CFD）方法生成：二维流体系统使用基于有限体积法（FVM）和浸入边界法（IBM）的 Lilypad 求解器，三维流体系统使用 Waterlily 求解器在 GPU 上运行；燃烧数据集则通过三维隐式非定常大涡模拟（LES）结合涡耗散概念（EDC）模型生成（Section 3.2, Appendix B.2）。这一配对数据生成策略是后续 sim-to-real 分析的基础。

**任务定义模块**将预测问题统一形式化为从初始状态和物理参数到未来系统演化的映射 $\dot{F} : \mathcal{A} \times \dot{\Gamma} \to \mathcal{U}$，并在此基础上定义三种训练范式（Section 3.1）：
- **真实训练**：直接在少量真实样本上训练；
- **模拟训练**：在全部模拟样本上训练，并辅以噪声添加和模态掩码策略以逼近真实数据分布；
- **模拟预训练 + 真实微调**：先在模拟数据上预训练，再在真实数据上微调。

所有范式的评估均在真实世界数据上进行，确保评估的一致性和实际相关性。

**评估指标体系**包含九项指标，分为数据导向和物理导向两类（Section 3.3）。数据导向指标包括 RMSE、MAE、相对 $L_2$ 误差（Rel $L_2$）、决定系数 $R^2$ 和更新比率（Update Ratio）；物理导向指标包括频率误差（FE）、湍流动能误差（KE）、平均速度剖面误差（MVPE）和频段分解的 fRMSE。这些指标从点对点精度、频域特性、能量守恒和长期统计行为等多个维度刻画模型在真实场景中的表现。

**基线评估模块**覆盖十种代表性方法，横跨传统降阶模型（**DMD**, Kutz et al., 2016）、CNN 架构（**U-Net**, Ronneberger et al., 2015）、神经算子（**CNO**, Raonic et al., 2023; **DeepONet**, Lu et al., 2021; **FNO**, Li et al., 2021; **WDNO**, Hu et al., 2025; **MWT**, Gupta et al., 2021）、Transformer 架构（**GK-Transformer**; **Transolver**, Wu et al., 2024a）以及大规模预训练 PDE 基础模型（**DPOT** 小模型 30M 和大模型 509M, Hao et al., 2024）。所有基线在三种训练范式下统一评测，超参数针对各数据集单独调优（Section 3.4）。

pipeline 的输入输出流清晰：输入为初始物理场快照和工况参数，输出为未来时刻的物理场预测。评估时，所有模型在相同的参数级划分的真实验证集和测试集上进行，保证了实验协议的公平性。



RealPDEBench 本身是一个基准框架，而非提出新模型的方法论文，其核心模块由**数据生成管线**、**任务范式定义**和**评估指标体系**三部分构成。

### 数据生成管线

基准构建了配对的真实实验数据与数值模拟数据，覆盖流体力学与燃烧两类物理系统：

- **真实数据采集**：流体系统采用粒子图像测速（PIV）技术，在水循环水洞中测量速度场；燃烧系统通过旋流燃烧器实验台获取化学发光（CL）成像数据（见 Figure 2）。
- **模拟数据生成**：流体系统的模拟数据使用计算流体力学（CFD）方法生成，2D 场景采用 **Lilypad** 求解器，3D 场景采用 **Waterlily** 求解器，均基于有限体积法（FVM）与浸没边界法（IBM）在 GPU 上运行。燃烧数据集则采用三维隐式非定常大涡模拟（LES），以涡耗散概念（EDC）模型处理湍流-化学相互作用。

### 任务范式定义

基准定义了三种训练-评估范式（Section 3.1），所有评估均在真实数据上进行：

1. **真实训练（Real-world Training）**：直接在 $n$ 个真实样本上训练模型。
2. **模拟训练（Simulated Training）**：在所有 $N$ 个模拟样本上训练模型，并采用**噪声添加**和**模态随机掩码**两种策略以缩小模拟-真实分布差异。
3. **模拟预训练 + 真实微调（Simulated Pretraining + Real-world Finetuning）**：先在全部模拟数据上预训练，再在少量真实数据上微调。

预测任务的形式为学习从初始状态和参数到未来演化的映射：

$${ \dot { F } } : { \mathcal { A } } \times { \dot { \Gamma } } \to { \mathcal { U } }$$

其中 $\mathcal{A}$ 为初始离散化状态空间，$\Gamma$ 为参数空间，$\mathcal{U}$ 为目标演化空间。

### 评估指标体系

基准设计了九项评估指标，分为面向数据和面向物理两类（Section 3.3）。

#### 面向数据的指标

- **决定系数 $R^2$**，衡量预测解释的方差比例：

$$R^{2} = 1 - \frac{\sum_{k}(y_{k} - \hat{y}_{k})^{2}}{\sum_{k}(y_{k} - \bar{y})^{2}}$$

- **更新比率（Update Ratio）**：真实微调达到仅用真实数据从头训练最优性能所需迭代次数与从头训练总迭代次数的比值。该指标量化预训练带来的收敛加速效应。

#### 面向物理的指标

- **频率误差（FE）**：对时域信号空间求和后做一维 FFT，计算预测与真值频谱之间的平均绝对误差，评估模型捕捉周期特性的能力：

$$\mathrm{FE} = \frac{1}{KT} \sum_{k,t} \left| \mathcal{F}\left(\sum_{i} \mathbf{y}_{k}(t, x_{i})\right) - \mathcal{F}\left(\sum_{i} \hat{\mathbf{y}}_{k}(t, x_{i})\right) \right|$$

- **动能误差（KE）**：速度脉动动能的绝对误差，其中脉动速度定义为瞬时速度与时均速度之差：

$$\mathrm{KE} = |e - \hat{e}|, \quad e = \frac{\overline{(\mathbf{u}')^{2}} + \overline{(\mathbf{v}')^{2}}}{2}, \quad \overline{(\mathbf{u}')^{2}} = \frac{1}{T} \sum_{t} (\mathbf{u}(t) - \bar{\mathbf{u}})^{2}$$

- **时均速度剖面误差（MVPE）**：在探针位置处计算时均速度场的绝对差异，用于评估长期自回归预测的累积误差：

$$\mathrm{MVPE} = \frac{1}{K N_{\mathrm{probe}}} \sum_{k,j} \left| \bar{u}(x_{\mathrm{probe},k,j}, y_{\mathrm{probe},k,j}) - \bar{\hat{u}}(x_{\mathrm{probe},k,j}, y_{\mathrm{probe},k,j}) \right|$$

### 基线模型谱系

基准覆盖了十种代表性模型，从传统降阶方法到大规模预训练基础模型：

- **DMD**（Kutz et al., 2016）：基于 SVD 的线性降阶模型，其低维演化矩阵为 $\tilde{\mathbf{A}} = \mathbf{U}^{T} \mathbf{X}_{2} \mathbf{V} \pmb{\Sigma}^{-1}$，未来状态通过模态叠加预测 $\mathbf{x}(t) = \sum_{i} b_{i} \psi_{i} \exp(\bar{\lambda}_{i} \cdot t)$。
- **U-Net**（Ronneberger et al., 2015）、**CNO**（Raonic et al., 2023）：基于 CNN 的时空模型与卷积神经算子。
- **DeepONet**（Lu et al., 2021）、**FNO**（Li et al., 2021）、**WDNO**（Hu et al., 2025）、**MWT**（Gupta et al., 2021）：算子学习类方法。
- **GK-Transformer**（Cao, 2021）、**Transolver**（Wu et al., 2024a）：Transformer 类 PDE 求解器。
- **DPOT**（Hao et al., 2024）：自回归去噪算子 Transformer，提供小规模（30M）和大规模（509M）两种预训练版本，作为 PDE 基础模型参与基准测试。



## 实验与关键发现

### 核心发现：模拟到真实的鸿沟

RealPDEBench的核心实验揭示了一个关键结论：**直接在模拟数据上训练的模型难以泛化到真实数据，两者之间存在显著的性能鸿沟。** 表1给出了系统性的量化证据：在所有数据集和基线模型上，仅使用真实数据训练（Real-world Training）相比仅使用模拟数据训练（Simulated Training），在相对L2误差（Rel L2）上的提升幅度达9.39%至78.91%。这一差距在频率域更为突出——图3a显示，模拟训练模型在Controlled Cylinder数据集上的频率误差（FE）远高于真实训练模型，表明模拟数据无法捕捉真实物理系统中的周期性和频谱特性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/004_Figure_3.jpg]]
*Figure 3: (a) Frequency errors of baselines (statistics of 10 values) on real-world vs. simulated data from Controlled Cylinder. (b) Validation RMSE curves of real-world finetuning on Combustion, with crosses marking the best RMSE of real-world training. The x-axis shows the percentage of update iterations. (c) RMSE under 1, 2, 3, 5, and 10 rounds of autoregressive evaluation on Cylinder*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/003_Table_1.jpg]]
*Table 1: Results of RMSE, Rel L _ { 2 } , fRMSE, and Update Ratio. Different datasets have different colors. Because DMD lacks the training process, we place its inference results in the last column and leave the rest blank. The smaller the error result, the darker the color. The bolded is the best*

造成这一鸿沟的根源在于模拟与真实数据之间的系统性差异：真实数据包含测量噪声、实验边界条件的不确定性以及传感器模态限制，而模拟数据尽管物理上更完整，却缺乏这些真实世界的“瑕疵”。为缓解这一问题，论文提出向模拟数据添加噪声以近似真实数据分布，该策略有效提升了模拟训练模型在真实测试集上的泛化能力（Section 4.2）。此外，针对真实数据中某些模态不可测的问题（如燃烧系统中的三维组分场），采用随机掩码（mask-training）策略处理模拟数据中的不可测模态，利用额外的动态信息进一步提升了模型性能（Section 4.2, Appendix D.1）。

### 真实微调：弥合鸿沟的关键路径

论文最关键的发现是**模拟预训练加真实微调（Real-world Finetuning）范式的有效性。** 表1的Update Ratio列提供了强有力的收敛效率证据：在Cylinder数据集上，U-Net的真实微调更新比率仅为0.3636，意味着相比从头训练，仅需约36%的迭代次数即可达到同等性能。这一加速效应在Combustion数据集上同样得到验证——图3b显示，真实微调的验证RMSE下降速度远快于仅使用真实数据从头训练，且最终RMSE更低。

更重要的是，真实微调不仅在效率上占优，在精度上也显著超越等量真实数据从头训练。表1中，真实微调模型在各数据集上普遍取得最优结果。在Cylinder数据集上，大规模预训练模型DPOT-L-FT在真实微调后取得最低RMSE 0.0394和Rel L2 0.0733（Table 1, Table 5）。在Controlled Cylinder数据集上，U-Net的真实微调版本将Rel L2降至0.0223，相比模拟训练最佳结果（CNO, 0.1849）降低了87.9%。这些结果表明，模拟数据中蕴含的丰富动态信息可以通过预训练有效迁移，而少量真实数据足以完成领域适配。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/011_Table_5.jpg]]
*Table 5: 1, 2, and 3 rounds of autoregressive evaluation under RMSE, relative L _ { 2 } error, and fRMSE. The bolded values are the best*

### 自回归评估与长期稳定性

为检验模型的长期预测能力，论文设计了多轮自回归评估（1、2、3、5、10轮）。图3c展示了Cylinder数据集上RMSE随自回归轮数增加的变化趋势：所有模型的误差均随轮数增加而累积，但真实微调模型表现出更优的稳定性。表8和表9的对比进一步揭示了模拟与真实之间的深层差异：模拟数据全轨迹的MVPE为0.08718，而真实微调模型在仅200步预测下的MVPE可达0.01250至0.10668，这意味着经过微调的模型在长期预测中甚至可以超越模拟数据本身的物理保真度。

图5a展示了10轮自回归评估后各模型的MVPE分布，图5b则可视化了U-Net预测的时均速度剖面与真实值的对比。这些结果共同表明，真实微调不仅能提升单步预测精度，更能有效抑制误差的时序累积，为物理系统的长期演化预测提供了可靠路径。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/006_Figure_5.jpg]]
*Figure 5: (a) MVPEs of real-world finetuning under 10-round autoregressive evaluation on Cylinder. (b) MVP of U-Net’s 10-round autoregressive prediction on Cylinder*

### 频率域与物理导向指标分析

论文引入了频率误差（FE）、湍动能误差（KE）和平均速度剖面误差（MVPE）等物理导向指标，以超越传统的逐点误差度量。图4展示了RMSE与频率误差之间的权衡关系：部分模型在降低RMSE的同时牺牲了频率保真度，而真实微调模型通常在两个维度上均表现更优。图6进一步将频率误差分解为低、中、高频分量，揭示了不同模型在不同频段的差异化表现——这对于评估模型捕捉湍流多尺度结构的能力至关重要。

在Combustion数据集上，由于模拟与真实数据之间存在模态不匹配（模拟数据包含三维组分场，而真实测量仅为二维化学发光图像），直接进行模拟预训练难以奏效。论文采用训练好的替代模型（U-Net）桥接模拟模态与真实模态，使真实微调成为可能（Section D.2）。这一策略的成功表明，在面临严重模态差异时，中间表示学习是连接模拟与真实的关键技术。

### 基线模型对比与适用性分析

在十个基线模型中，不同架构展现出明显的场景特异性。传统降阶模型DMD无需训练，但在复杂流动中精度有限。CNN架构的U-Net在Controlled Cylinder和FSI等具有强空间局部结构的数据集上表现突出，取得最优Rel L2（0.0223和0.0733）。基于算子学习的CNO、FNO和DeepONet在模拟训练中具有一定优势，但迁移到真实数据时性能下降明显。Transformer架构的Transolver和GK-Transformer在Foil等几何复杂场景中表现更好。预训练基础模型DPOT（包括30M的小型版本和509M的大型版本）在真实微调后展现出最强的综合性能，尤其在Cylinder和Foil数据集上取得最优结果。

### 局限性与开放问题

尽管RealPDEBench在揭示sim-to-real鸿沟方面取得了系统性进展，但仍存在若干局限。首先，基准目前局限于流体动力学和燃烧领域，未覆盖电磁学、结构力学等其他重要物理系统。其次，燃烧数据集尚未引入专门的物理导向指标，对反应流动力学（如火焰面曲率、释热率分布）的评估仍不充分。此外，基准尚未系统性地探索强分布外参数区域，限制了泛化能力的测评。真实数据中的噪声模式和测量误差如何更有效地在模拟数据中建模，以提升sim-to-real迁移的鲁棒性，仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/002_Figure_2.jpg]]
*Figure 2: Photos of real-world data collection. (a) Water tunnel after laser irradiation. (b) Particle imaging photos taken by the camera. (c) Motion control equipment. (d) Swirl combustor equipment*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/016_Figure_9.jpg]]
*Figure 9: Schematic illustration of the Circulating Water Tunnel platform and the PIV measurement system installation. (a) A schematic of the water tunnel. (b) Experiment equipment*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/021_Figure.jpg]]
*Figure: (a) (b)*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/008_Table_2.jpg]]
*Table 2: Results of other metrics. The bolded values are the best*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/009_Table_3.jpg]]
*Table 3: 2 rounds of autoregressive evaluation. The bolded values are the best*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/010_Table_4.jpg]]
*Table 4: 3 rounds of autoregressive evaluation. The bolded values are the best*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/014_Table_6.jpg]]
*Table 6: Low, mid, high frequency error. The bolded values are the best*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_y3oHMcoItR/figures/015_Table_7.jpg]]
*Table 7: Overview of datasets. $\mathtt { n \_ t r a j }$ is the number of trajectories. n frame is the number of frames*



## 定位与知识库关联

### 1. 基准定位与核心贡献

RealPDEBench 并非提出一种新的学习算法，而是构建了一个系统性评估科学机器学习模型在真实物理数据上表现能力的基准平台。其核心贡献在于首次大规模地收集了配对的真实物理实验数据与数值模拟数据，并定义了三种训练范式（仅真实训练、仅模拟训练、模拟预训练后真实微调）以及九项评估指标，从而量化模拟与真实之间的鸿沟，并检验利用模拟数据提升真实预测的可行性。

该基准的定位填补了当前科学机器学习领域的一个关键空白：现有模型大多仅在模拟数据上训练和验证，缺乏对真实场景泛化能力的可靠评估。RealPDEBench 通过提供超过 700 条轨迹（每条超过 2000 帧）的真实-模拟配对数据，为 sim-to-real 迁移研究提供了标准化测试平台。

### 2. 基线模型谱系

RealPDEBench 覆盖了十种代表性基线模型，跨越传统降阶模型、卷积架构、算子学习、Transformer 架构到大规模预训练基础模型，形成了从经典到前沿的完整谱系：

**传统降阶模型：**
- **DMD**（Kutz et al., 2016）：基于 SVD 的线性演化算子，通过模态叠加预测未来状态。作为无需训练的传统方法，其推理结果作为基准参考线。

**卷积架构：**
- **U-Net**（Ronneberger et al., 2015）：经典的 CNN 编解码器结构，在时空预测任务中表现稳健。
- **CNO**（Raonic et al., 2023）：卷积神经算子，通过卷积架构实现函数空间映射。

**算子学习：**
- **DeepONet**（Lu et al., 2021）：深度算子网络，通过分支网络和主干网络解耦输入函数和查询点。
- **FNO**（Li et al., 2021）：傅里叶神经算子，在频域进行全局卷积，对周期性系统建模能力强。
- **MWT**（Gupta et al., 2021）：多分辨率小波变换算子，利用小波基捕获多尺度特征。
- **WDNO**（Hu et al., 2025）：小波扩散神经算子，结合扩散模型与算子学习。

**Transformer 架构：**
- **GK-Transformer**（Cao, 2021）：Galerkin Transformer 与 FNO 回归头结合，通过注意力机制建模 PDE 动态。
- **Transolver**（Wu et al., 2024a）：基于 Transformer 的 PDE 求解器，面向复杂几何和物理系统。

**大规模预训练模型：**
- **DPOT**（Hao et al., 2024）：自回归去噪算子 Transformer，提供小规模（30M）和大规模（509M）两个版本，作为预训练 PDE 基础模型的代表。

### 3. 方法适用边界

RealPDEBench 的实验设计揭示了各方法的适用边界：

**模拟训练的真实泛化瓶颈：** 直接在模拟数据上训练的模型难以泛化到真实数据，相对 L2 误差差距达 9.39%–78.91%（Table 1）。即使采用噪声添加和模态掩码策略来缩小分布差距，模拟训练在频率误差（Frequency Error）上仍显著劣于真实训练（Figure 3a），表明模拟数据难以完全复现真实物理系统的频谱特性。

**真实微调的优势边界：** 模拟预训练结合少量真实数据微调，在所有数据集和基线模型上均优于仅使用相同量真实数据从头训练。这一优势在 Cylinder 数据集上尤为显著——大规模预训练模型 DPOT-L-FT 在真实微调后取得最低 RMSE 0.0394 和 Rel L2 0.0733（Table 1, Table 5）。

**收敛加速效应：** 真实微调的更新比率（Update Ratio）普遍小于 1（Table 1），表明预训练能显著减少达到同等性能所需的迭代次数。例如，U-Net 在 Cylinder 上的更新比率仅为 0.3636，意味着微调只需从头训练 36.36% 的迭代即可达到相同精度。

**燃烧系统的特殊性：** 对于 Combustion 数据集，由于模拟模态（如温度、化学组分浓度）与真实模态（光强图像）之间存在本质差异，直接进行模拟预训练难以奏效。需要使用训练好的替代模型（如 U-Net）来桥接模拟模态和真实模态，这是该方法在燃烧领域应用的必要前提。

**自回归长期预测：** 在 Cylinder 数据集上进行 10 轮自回归评估时，真实微调模型的 MVPE 范围为 0.01250–0.10668，低于模拟数据全轨迹的 MVPE 0.08718（Table 8, Table 9），表明微调策略能有效抑制误差累积。

### 4. 局限与开放问题

**领域覆盖范围有限：** 当前基准局限于流体动力学（圆柱绕流、受控圆柱、流固耦合、翼型）和燃烧领域，未覆盖电磁学、结构力学、空气动力学等其他重要物理系统。这限制了基准在更广泛科学计算场景中的代表性。

**燃烧物理指标缺失：** 尽管设计了 FE、KE、MVPE 等物理导向指标，但尚未针对燃烧系统引入专门的物理一致性评估（如反应速率、火焰结构等），对燃烧动力学的物理精度评估仍不够充分。

**分布外泛化未探索：** 基准目前没有系统性地探索强分布外参数区域（如雷诺数、攻角等工况参数的大幅外推），限制了模型泛化能力的全面测评。

**开放问题：**
1. 如何为燃烧等多物理场耦合系统设计更有针对性的物理一致性指标？
2. 在强分布外工况下，模拟预训练与真实微调的迁移能力如何？需要新的任务设计和数据集扩展。
3. 基准是否应包含更多动态任务（如逆问题、参数估计）从而全面评估科学机器学习模型的真实世界适应能力？
4. 真实数据中的噪声模式和测量误差如何更有效地在模拟数据中建模，以提升 sim-to-real 迁移的鲁棒性？



## 原文 PDF

![[paperPDFs/ICLR_2026/RealPDEBench_A_Benchmark_for_Complex_Physical_Systems_with_Real_World_Data.pdf]]

---
title: "Progressive Guessing to Fixed Point: Rethinking Human Motion Prediction with Deep Equilibrium Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Progressive_Guessing_to_Fixed_Point_Rethinking_Human_Motion_Prediction_with_Deep_Equilibrium_Models.pdf
project_link: null
code_link: null
aliases:
- PGFPRHMPDEM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将多阶段细化过程重铸为共享参数的不动点求解，同时注入等变/不变观察条件，实现无限深度细化并适配流式运动。
primary_logic: 渐进式猜测本质上是一个有限步迭代过程；通过深度均衡模型（DEQ）将其转化为不动点问题，可以等价地执行无限次细化，且天然与流式运动数据的特点契合：可将前一轮的不动点作为当前轮的热启动，大幅减少冗余计算。
claims:
- MotionDEQ在Human3.6M上以不到300K参数在400ms处达到55.3mm预测误差，取得最优性能。
- MotionDEQ的训练内存消耗比对应的多阶段模型少2倍以上。
- Warm initial guess通过重用上一轮预测的不动点，显著加速求解器收敛。
- 稀疏不动点监督避免了手工设计中间目标，稳定训练并提升精度。
---

# Progressive Guessing to Fixed Point: Rethinking Human Motion Prediction with Deep Equilibrium Models

> [!tip] 核心洞察
> 渐进式猜测本质上是一个有限步迭代过程；通过深度均衡模型（DEQ）将其转化为不动点问题，可以等价地执行无限次细化，且天然与流式运动数据的特点契合：可将前一轮的不动点作为当前轮的热启动，大幅减少冗余计算。

| 字段 | 内容 |
|------|------|
| 中文题名 | 渐进式猜测到不动点：深度均衡人体运动预测的重新思考 |
| 英文题名 | Progressive Guessing to Fixed Point: Rethinking Human Motion Prediction with Deep Equilibrium Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wei_Progressive_Guessing_to_Fixed_Point_Rethinking_Human_Motion_Prediction_with_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionDEQ |
| Dataset | Human3.6M, CMU-MoCap, 3DPW |

> [!tip] 效果简介
> - Human3.6M 上，MPJPE (mm) 38.8 (walking@400ms) vs 40.9 (EqMotion) (-2.1)；MPJPE (mm) 32.2 (walking@320ms) vs 33.5 (EqMotion) (-1.3)；MPJPE (mm) 17.3 (walking@160ms) vs 17.8 (EqMotion) (-0.5)。
> - CMU-MoCap 上，MPJPE (mm) Outperforms all baselines (exact values in Table 2) vs EqMotion, PGBIG, etc. (uniform improvement)。
> - 3DPW 上，MPJPE (mm) improved by 4.6% @200ms, 3.3% @400ms over best baseline vs best baseline (probably EqMotion) (4.6% / 3.3% improvement)。

## 概要

人体运动预测旨在从观察到的历史姿态序列推断未来运动轨迹。近年来，多阶段渐进式猜测范式（如 **PGBIG** (Ma et al., CVPR 2022)、**EqMotion** (Xu et al., CVPR 2023)）取得了显著进展，但其核心瓶颈在于：各细化阶段参数独立、缺乏明确的停止准则，且路径依赖导致参数冗余和计算开销随深度线性增长。

本文提出 **MotionDEQ**，将渐进式猜测重新思考为深度均衡模型（Deep Equilibrium Model, DEQ）下的不动点学习问题。核心洞察是：多阶段细化本质上是一个有限步迭代过程；通过引入共享参数的不动点求解器，可以等价地执行无限次细化，且天然适配流式运动数据——可将前一轮的不动点作为当前轮的热启动，大幅减少冗余计算。

具体而言，MotionDEQ 将 EqMotion 的多阶段变换重铸为共享参数的单层隐式函数，其不动点 $\mathbf{z}^* = f_{\boldsymbol{\theta}}(\mathbf{z}^*, \mathbf{x})$ 对应无限次细化后的平衡态。训练采用稀疏不动点监督，直接在最终不动点和若干中间状态上与原始真值对齐，避免了手工设计中间目标。在流式场景中，模型复用上一轮预测的不动点作为热启动初始猜测，并通过等变校正适配器利用新观测进行轻量校正。

在 Human3.6M 数据集上，MotionDEQ 以不到 300K 参数在 400ms 处达到 55.3mm 预测误差，取得最优性能；训练内存消耗比对应的多阶段模型减少 2 倍以上。在 CMU-MoCap 和 3DPW 数据集上同样一致优于现有基线，验证了 DEQ 范式在人体运动预测中的有效性与效率优势。



### 问题背景

人体运动预测（Human Motion Prediction）旨在根据观测到的历史运动序列 $\mathbf{X}_{1:T_p}$，预测未来 $T_f$ 帧的三维人体姿态。这一任务在自动驾驶、人机交互和运动分析等领域具有重要应用价值。其核心挑战在于：人体运动天然具有**等变性（equivariance）**——当输入运动发生旋转或平移时，预测输出应相应变换；同时，运动模式又蕴含**不变性（invariance）**——关节间的协同关系在坐标系变换下保持稳定。如何在保持等变性的同时，充分挖掘不变模式以提升长时预测精度，是该领域的核心难题。

### 现有方法缺口：多阶段渐进式猜测的困境

近年来，多阶段渐进式猜测（multi-stage progressive guessing）范式在人体运动预测中取得了显著进展。以 **PGBIG**（Ma et al., CVPR 2022）和 **EqMotion**（Xu et al., CVPR 2023）为代表的方法，将预测过程分解为多个细化阶段，每个阶段在上一步预测基础上逐步逼近真值。这一策略虽然有效，但存在三个根本性缺陷：

1. **参数冗余**：各细化阶段 $\ell$ 拥有独立的参数集 $\mathcal{F}_{\mathrm{EGFL}}^{(\ell)}$ 和 $\mathcal{F}_{\mathrm{IPFL}}^{(\ell)}$，参数量随阶段数 $L$ 线性增长，导致模型臃肿且泛化能力受限。

2. **深度固定且无停止准则**：阶段数 $L$ 是人工设定的经验值，缺乏理论依据；各阶段之间没有明确的收敛判断机制，无法根据输入难度自适应调整计算量。

3. **路径依赖与存储开销**：逐阶段的前向传播使得中间状态必须全部保留，训练内存与推理时延均随 $L$ 线性增长。

这些缺陷的根源在于：多阶段范式将渐进式猜测视为一个**有限步的显式堆叠过程**，而非一个**可收敛的迭代求解问题**。

### 核心洞察：从有限步迭代到不动点求解

本文的核心洞察是：渐进式猜测本质上是一个有限步迭代过程，其极限状态对应于一个不动点方程的解。具体而言，若将各阶段共享的变换记为 $f_{\boldsymbol{\theta}}$，则无限次细化后的输出 $\mathbf{z}^*$ 满足：

$$\mathbf{z}^* = f_{\boldsymbol{\theta}}(\mathbf{z}^*, \mathbf{x})$$

其中 $\mathbf{x}$ 为观测条件。这意味着，**多阶段细化可以被重铸为一个深度均衡模型（Deep Equilibrium Model, DEQ），通过不动点求解等价地执行无限次细化**，从而从根本上消除阶段数 $L$ 的人为设定，并将参数复杂度从 $O(L)$ 降至 $O(1)$。

### 流式运动的天然适配

人体运动预测在实时应用中常以流式（streaming）方式运行：每接收一帧新观测，就更新未来预测。传统多阶段模型在流式场景下需从头计算，计算冗余严重。而 DEQ 范式与流式运动数据的特点天然契合：**上一轮预测的不动点 $\mathbf{z}^*_{r}$ 可作为当前轮的热启动初始猜测（warm initial guess）**，大幅加速求解器收敛，减少冗余计算。

### 本文动机与贡献

基于上述洞察，本文提出 **MotionDEQ**，将人体运动预测重新思考为一个不动点学习问题。MotionDEQ 的核心设计原则包括：

- **共享参数的无限制细化**：所有迭代共享同一组参数 $\boldsymbol{\theta}$，通过不动点求解器（如 Anderson mixing）实现由残差收敛（$\epsilon = 10^{-3}$）界定的自适应深度。
- **等变/不变观察条件注入**：在每次迭代中，通过等变注入层 $\mathcal{F}_{\mathrm{EGI}}$ 和不变注入层 $\mathcal{F}_{\mathrm{IPI}}$ 将观测特征融入当前猜测，确保等变性和不变性的同时保留。
- **稀疏不动点监督**：直接在最终不动点与稀疏采样的中间状态上与原始真值对齐，避免手工设计平滑目标或密集阶段监督。
- **流式适配**：通过热启动初始猜测和轻量等变校正适配器 $\mathcal{F}_{\mathrm{ECA}}$，使模型无缝适配流式运动数据。



## 核心方法与创新机理

### 问题瓶颈：多阶段渐进式猜测的“深度陷阱”

人体运动预测中的渐进式猜测范式（以 **PGBIG** (Ma et al., CVPR 2022) 和 **EqMotion** (Xu et al., CVPR 2023) 为代表）将预测过程分解为多个细化阶段，每个阶段通过独立的几何特征层 ${\mathcal{F}}_{\mathrm{EGFL}}^{(\ell)}$ 和模式特征层 ${\mathcal{F}}_{\mathrm{IPFL}}^{(\ell)}$ 逐步修正初始猜测。这一范式存在三个结构性缺陷：

1. **参数冗余**：各阶段参数独立，参数量随阶段数 $L$ 线性增长，但各阶段执行本质上相似的“猜测-修正”操作，未实现知识复用。
2. **无停止准则**：阶段数 $L$ 由经验固定，缺乏收敛判定机制——浅层可能细化不足，深层则浪费计算。
3. **路径依赖**：中间状态 ${\mathbf{z}}^{(\ell)}$ 必须手工设计平滑真值作为监督目标（PGBIG 的做法），否则训练不稳定；但手工设计的目标本身引入偏差。

这些缺陷使得模型在参数效率、训练稳定性和计算开销之间陷入 trade-off。

### 核心洞察：从有限步迭代到不动点求解

MotionDEQ 的核心洞察在于：**渐进式猜测本质上是有限步的迭代细化过程，可以等价地重铸为深度均衡模型（DEQ）中的不动点问题**。具体而言，将多阶段变换 ${\mathbf{z}}^{(\ell+1)} = f_{\theta_\ell}({\mathbf{z}}^{(\ell)}, {\mathbf{x}})$ 替换为共享参数的单一变换 $f_\theta$ 的无限次自映射：

$${\mathbf{z}}^* = f_{\boldsymbol{\theta}}({\mathbf{z}}^*, {\mathbf{x}})$$

其中 ${\mathbf{z}}^*$ 是不动点，${\mathbf{x}}$ 为观察条件。这一重铸带来三个根本性改变：

- **无限深度等价**：不动点 ${\mathbf{z}}^*$ 等价于经过无限次细化后的状态，突破了固定阶段数 $L$ 的限制。
- **$O(1)$ 参数与训练内存**：所有迭代共享同一组参数 $\theta$；训练时通过隐函数定理（IFT）计算梯度，仅依赖平衡态 ${\mathbf{z}}^*$，无需存储中间激活，训练内存比多阶段模型减少 2 倍以上。
- **自然收敛判定**：前向求解采用黑箱不动点求解器（如 Anderson mixing），以残差 $\varepsilon = 10^{-3}$ 作为停止准则，自适应决定迭代次数。

### 关键创新点（Changed Slots）

下表对比 MotionDEQ 与基线方法在四个关键维度的设计差异：

| 设计维度 | 基线方法（EqMotion/PGBIG） | MotionDEQ |
|---------|--------------------------|-----------|
| **参数共享** | 各阶段独立参数 ${\mathcal{F}}_{\mathrm{EGFL}}^{(\ell)}$、${\mathcal{F}}_{\mathrm{IPFL}}^{(\ell)}$ | 所有迭代共享同一组参数 $\theta$ |
| **细化深度** | 固定经验阶段数 $L$，无停止准则 | 无限深度，由残差收敛（$\varepsilon = 10^{-3}$）界定停止 |
| **初始猜测与观察注入** | 直接使用观察运动作为初始特征，无显式注入 | 最后一帧重复 ${\mathbf{X}}_{rep}$ 作为初始猜测；观察条件通过等变注入层 ${\mathcal{F}}_{\mathrm{EGI}}$ 和不变注入层 ${\mathcal{F}}_{\mathrm{IPI}}$ 引入每次迭代 |
| **监督目标** | 手工递归平滑的真值作为各阶段中间监督（PGBIG） | 稀疏不动点校正损失：直接在最终不动点和若干中间状态上与原始真值对齐 |

### 创新 1：等变/不变观察注入

MotionDEQ 并非简单地将 DEQ 应用于运动预测，而是针对运动数据的几何特性设计了注入机制。观察到的运动序列被分解为等变几何特征 ${\mathbf{X}}_G$ 和不变模式特征 ${\mathbf{X}}_H$，在每次 DEQ 迭代中通过 ${\mathcal{F}}_{\mathrm{EGI}}$ 和 ${\mathcal{F}}_{\mathrm{IPI}}$ 注入当前猜测：

$${\mathbf{P}} = {\mathcal{F}}_{\mathrm{EGI}}({\mathbf{G}}^{(\ell)}, {\mathbf{X}}_G), \quad {\mathbf{Q}} = {\mathcal{F}}_{\mathrm{IPI}}({\mathbf{H}}^{(\ell)}, {\mathbf{X}}_H)$$

$${\mathbf{G}}^{(\ell+1)} = {\mathcal{F}}_{\mathrm{EGFL}}({\mathbf{P}}, {\mathbf{Q}}, {\mathbf{X}}_C), \quad {\mathbf{H}}^{(\ell+1)} = {\mathcal{F}}_{\mathrm{IPFL}}({\mathbf{P}}, {\mathbf{Q}})$$

消融实验（Table 5）表明，${\mathcal{F}}_{\mathrm{EGI}}$ 和 ${\mathcal{F}}_{\mathrm{IPI}}$ 各自贡献约 6mm 的平均 MPJPE 增益，二者结合效果最佳；若移除观察注入直接使用标准 DEQ 形式（Eq. (2)），平均 MPJPE 从 32.1 骤升至 71.4，验证了注入机制的关键性。

### 创新 2：稀疏不动点监督

传统多阶段方法需要为每个中间阶段设计平滑真值作为监督目标，这一手工设计不仅引入偏差，还可能导致训练不稳定（Table 4 中平滑 GT 方案出现 NaN）。MotionDEQ 采用稀疏不动点校正损失：

$${\mathcal{L}}_{total} = \| {\mathcal{F}}_{\mathrm{EOL}}({\mathbf{z}}^*) - {\mathbf{Y}} \|_2^2 + \gamma \| {\mathcal{F}}_{\mathrm{EOL}}({\mathbf{z}}^{(\ell)}) - {\mathbf{Y}} \|_2^2$$

其中 $\gamma = 0.8$，仅在最终不动点和稀疏采样的中间状态上与原始真值对齐，避免了手工目标设计。Table 4 显示，该方案在 100/200/400ms 分别达到 13.98/30.63/61.38 的 MPJPE，显著优于平滑 GT 和密集监督方案。

### 创新 3：流式运动的热启动适配

人体运动具有天然的流式特性——连续帧之间高度相关。MotionDEQ 利用这一特性，将上一预测轮次的不动点 ${\mathbf{z}}_r^*$ 作为当前轮次的初始猜测（warm initial guess），显著加速求解器收敛（Figure 6a）。此外，设计等变校正适配器 ${\mathcal{F}}_{\mathrm{ECA}}$，利用上一轮预测偏差 ${\widehat{\mathbf{Y}}}_r - {\mathbf{X}}_{r+1}$ 对几何特征进行轻量校正：

$${\mathbf{H}}' = {\mathcal{F}}_{\mathrm{DL}}({\widehat{\mathbf{Y}}}_r - {\mathbf{X}}_{r+1}), \quad {\mathbf{H}} = {\mathbf{H}}_{r+1}^* + \mathsf{MLP}({\mathbf{H}}')$$

$${\mathbf{G}}' = {\mathcal{F}}_{\mathrm{EGNN}}({\mathbf{G}}_{r+1}^*, {\mathbf{H}}), \quad {\widehat{\mathbf{Y}}}_{r+1} = {\mathcal{F}}_{\mathrm{EOL}}({\mathbf{G}}')$$

这一适配器保持等变性，且在流式场景下可有效利用新到达的真值信息进行在线校正（Figure 7）。

### 创新 4：截断 Neumann 梯度

训练时，DEQ 通过隐函数定理计算梯度，需近似逆雅可比矩阵 $({\mathbf{I}} - \partial f / \partial {\mathbf{z}}^*)^{-1}$。MotionDEQ 采用 2 步截断 Neumann 级数近似：

$$\frac{\partial {\mathcal{L}}_{\mathrm{MSE}}}{\partial \boldsymbol{\theta}} \approx \frac{\partial {\mathcal{L}}_{\mathrm{MSE}}}{\partial {\mathbf{z}}^*} \left( {\mathbf{I}} + \frac{\partial f({\mathbf{z}}^*, {\mathbf{x}} | \boldsymbol{\theta})}{\partial {\mathbf{z}}^*} \right) \frac{\partial f({\mathbf{z}}^*, {\mathbf{x}} | \boldsymbol{\theta})}{\partial \boldsymbol{\theta}}$$

Figure 8(b) 显示，截断梯度显著优于不精确的 JFB（Jacobian-Free Backpropagation）梯度，在保持 $O(1)$ 训练内存的同时提升了预测精度。

### 局限与待验证问题

- **热启动的连续性假设**：warm initial guess 依赖连续运动帧的高度时间一致性，当运动发生剧烈突变时，复用旧不动点可能引入偏差。该问题在无真值校准的离线场景尤为突出，需进一步设计自适应热启动机制。
- **推理迭代开销**：尽管训练内存恒定，推理时需 10-30 次迭代求解，在极端低延迟场景下仍有一定开销。固定点求解的收敛速度缺乏理论保证，能否通过模型设计（如单调算子）进一步减少迭代次数是开放问题。
- **架构泛化性**：当前仅基于 EqMotion 骨干架构验证，向其他等变预测器或 Transformer/扩散模型等架构的迁移效果尚未实验。



MotionDEQ 将人体运动预测重新表述为一个**共享参数的深度均衡（DEQ）不动点求解过程**，其整体 pipeline 由五个核心模块串联构成，数据流从历史观测序列出发，经特征初始化、交互图推断、初始猜测分解、DEQ 迭代细化，最终由等变输出层生成未来姿态序列。

### 从多阶段细化到不动点求解

传统渐进式猜测范式（如 **PGBIG** (Ma et al., CVPR 2022) 和 **EqMotion** (Xu et al., CVPR 2023)）将预测过程分解为 L 个独立参数化的细化阶段，每阶段执行：

- 等变几何特征更新：$\mathbf{X}_G^{(\ell+1)} = \mathcal{F}_{\text{EGFL}}^{(\ell)}(\mathbf{X}_G^{(\ell)}, \mathbf{X}_H^{(\ell)}, \mathbf{X}_C)$
- 不变模式特征更新：$\mathbf{X}_H^{(\ell+1)} = \mathcal{F}_{\text{IPFL}}^{(\ell)}(\mathbf{X}_H^{(\ell)}, \mathbf{X}_G^{(\ell)})$

这种设计的核心瓶颈在于：**各阶段参数 $\mathcal{F}_{\text{EGFL}}^{(\ell)}$ 和 $\mathcal{F}_{\text{IPFL}}^{(\ell)}$ 相互独立，缺乏明确的停止准则，且计算和存储开销随深度线性增长**。

MotionDEQ 的关键洞察是：若将上述两步变换的**参数跨阶段共享**（所有 ℓ 使用同一组 θ），并允许无限次迭代直至收敛，则多阶段细化等价于求解不动点方程：

$$(\mathbf{G}^*, \mathbf{H}^*) = \mathbf{z}^* = f(\mathbf{z}^*, \mathbf{x} \mid \theta)$$

其中 $\mathbf{x}$ 为从历史观测中提取的条件特征（包括几何特征 $\mathbf{X}_G$、模式特征 $\mathbf{X}_H$ 和交互图 $\mathbf{X}_C$），$\mathbf{z}^*$ 为平衡态下的几何与模式特征。前向求解通过黑箱不动点求解器（如 Anderson mixing）将残差 $\|f(\mathbf{z}, \mathbf{x} \mid \theta) - \mathbf{z}\|$ 降至阈值 $\varepsilon = 10^{-3}$ 以下，**在概念上等价于无限次细化**。

### Pipeline 模块与数据流

MotionDEQ 的整体架构如 Figure 2 所示，包含以下五个核心模块：

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionDEQ. Given a past motion sequence, the model constructs the observed condition through feature initialization and invariant reasoning modules, while generating the initial guess*

1. **特征初始化模块 $\mathcal{F}_{\text{IL}}$**：从历史观测序列 $\mathbf{X}_{1:T_p}$ 中提取初始等变几何特征 $\mathbf{X}_G^{(0)}$ 和不变模式特征 $\mathbf{X}_H^{(0)}$，作为后续推理的条件基础。

2. **不变推理模块 $\mathcal{F}_{\text{IRM}}$**：基于初始几何和模式特征推断关节交互图 $\mathbf{X}_C = \mathcal{F}_{\text{IRM}}(\mathbf{X}_G^{(0)}, \mathbf{X}_H^{(0)})$，编码关节间的空间依赖关系。

3. **分解层 $\mathcal{F}_{\text{DL}}$**：将最后一帧的重复 $\mathbf{X}_{rep} = \{\mathbf{X}_{T_p}, \ldots, \mathbf{X}_{T_p}\}$ 分解为初始猜测的等变几何特征 $\mathbf{G}^{(0)}$ 和全零初始化的不变模式特征 $\mathbf{H}^{(0)}$：
   $$\mathcal{F}_{\text{DL}}(\mathbf{X}_{rep}): \mathbf{G}^{(0)} = \{\mathbf{X}_{T_p}, \ldots, \mathbf{X}_{T_p}\}, \quad \mathbf{H}^{(0)} = \mathbf{0}$$

4. **DEQ 层（共享参数的 $\mathcal{F}_{\text{EGFL}}$ 与 $\mathcal{F}_{\text{IPFL}}$，配合等变注入 $\mathcal{F}_{\text{EGI}}$ 与不变注入 $\mathcal{F}_{\text{IPI}}$）**：这是框架的核心。每步迭代中，当前猜测 $(\mathbf{G}^{(\ell)}, \mathbf{H}^{(\ell)})$ 与观测条件 $(\mathbf{X}_G, \mathbf{X}_H)$ 通过注入层混合，再经共享参数的变换更新至下一状态：
   $$\mathbf{P} = \mathcal{F}_{\text{EGI}}(\mathbf{G}^{(\ell)}, \mathbf{X}_G), \quad \mathbf{Q} = \mathcal{F}_{\text{IPI}}(\mathbf{H}^{(\ell)}, \mathbf{X}_H)$$
   $$\mathbf{G}^{(\ell+1)} = \mathcal{F}_{\text{EGFL}}(\mathbf{P}, \mathbf{Q}, \mathbf{X}_C), \quad \mathbf{H}^{(\ell+1)} = \mathcal{F}_{\text{IPFL}}(\mathbf{P}, \mathbf{Q})$$
   迭代持续至收敛到不动点 $\mathbf{z}^* = (\mathbf{G}^*, \mathbf{H}^*)$。消融实验表明，$\mathcal{F}_{\text{EGI}}$ 和 $\mathcal{F}_{\text{IPI}}$ 各自贡献约 6mm 的平均 MPJPE 增益，二者结合效果最佳（Table 5）。

5. **等变输出层 $\mathcal{F}_{\text{EOL}}$**：将平衡态几何特征 $\mathbf{G}^*$ 解码为最终预测的未来姿态序列 $\hat{\mathbf{Y}} = \mathcal{F}_{\text{EOL}}(\mathbf{G}^*)$，保证整个网络的等变性。

### 流式预测适配

在流式运动预测场景中，MotionDEQ 天然适配两个关键机制（Figure 3）：

- **热启动初始猜测**：将上一预测轮次获得的不动点 $\mathbf{z}^*$ 作为当前轮的初始猜测 $\mathbf{z}^{(0)}$，利用连续运动帧的时间一致性显著加速求解器收敛。
- **等变校正适配器 $\mathcal{F}_{\text{ECA}}$**：利用上一轮预测 $\hat{\mathbf{Y}}_r$ 与当前观测 $\mathbf{X}_{r+1}$ 的偏差，通过轻量级 MLP 和等变图网络对几何特征进行校正，进一步提升流式场景下的预测精度。

需要注意的是，$\mathcal{F}_{\text{ECA}}$ 依赖上一预测轮次的真值进行校准，在无法获取实时真值的离线推理中不可用；热启动机制在运动发生剧烈突变时也可能引入偏差。



### 3.1 从渐进式猜测到不动点求解

多阶段渐进式猜测范式（如 **PGBIG** (Ma et al., CVPR 2022)、**EqMotion** (Xu et al., CVPR 2023)）的核心瓶颈在于：各细化阶段参数独立、无明确停止准则、计算与存储开销随深度线性增长。MotionDEQ 将这一过程重铸为共享参数的不动点求解，实现概念上等价于无限次细化。

给定过去观测序列 $\mathbf{X}_{1:T_p} = \{ \mathbf{X}_1, \mathbf{X}_2, \cdots, \mathbf{X}_{T_p} \}$，目标是预测未来 $T_f$ 帧 $\hat{\mathbf{Y}}_{T_p+1:T_p+T_f}$。EqMotion 的原始流程可概括为：

- **Step (1a)**: 特征初始化 $\mathcal{F}_{\mathrm{IL}}$ 从观测中提取初始几何特征 $\mathbf{X}_G^{(0)}$ 和模式特征 $\mathbf{X}_H^{(0)}$。
- **Step (1b)**: 不变推理模块 $\mathcal{F}_{\mathrm{IRM}}$ 推断关节交互图 $\mathbf{X}_C$。
- **Step (1c)-(1d)**: 等变几何特征层 $\mathcal{F}_{\mathrm{EGFL}}^{(\ell)}$ 和不变模式特征层 $\mathcal{F}_{\mathrm{IPFL}}^{(\ell)}$ 进行 $L$ 阶段细化，各阶段参数独立。
- **Step (1e)**: 等变输出层 $\mathcal{F}_{\mathrm{EOL}}$ 将最终几何特征映射为预测运动。

MotionDEQ 的核心改造在于将 Step (1c)-(1d) 转化为**共享参数 $\theta$ 的无限迭代方案**，形成深度均衡过程：

$$( \mathbf{z}^{(0)}, \mathbf{x} | \theta ) \to \cdots \to ( \mathbf{z}^{(\ell)}, \mathbf{x} | \theta ) \to \cdots \to ( \mathbf{z}^*, \mathbf{x} | \theta )$$

其中 $\mathbf{z}^*$ 为不动点，满足：

$$\mathbf{z}^* = f(\mathbf{z}^*, \mathbf{x} | \theta)$$

观察条件 $\mathbf{x}$ 在每次迭代中注入，初始猜测 $\mathbf{z}^{(0)}$ 由最后一帧重复构造。

### 3.2 初始猜测与观察注入

传统多阶段方法直接使用观测运动作为初始特征，MotionDEQ 则显式分离初始猜测与观察条件：

**分解层 $\mathcal{F}_{\mathrm{DL}}$** 将最后一帧重复 $\mathbf{X}_{rep}$ 分解为等变几何特征和不变模式特征：

$$\mathcal{F}_{\mathrm{DL}}(\mathbf{X}_{rep}): \mathbf{G}^{(0)}=\{\mathbf{X}_{T_p},...,\mathbf{X}_{T_p}\}, \quad \mathbf{H}^{(0)}=\mathbf{0}$$

**等变几何注入层 $\mathcal{F}_{\mathrm{EGI}}$** 和**不变模式注入层 $\mathcal{F}_{\mathrm{IPI}}$** 在每次 DEQ 迭代中将观测条件与当前猜测混合：

$$\mathbf{P} = \mathcal{F}_{\mathrm{EGI}}(\mathbf{G}^{(\ell)}, \mathbf{X}_G), \quad \mathbf{Q} = \mathcal{F}_{\mathrm{IPI}}(\mathbf{H}^{(\ell)}, \mathbf{X}_H)$$

$$\mathbf{G}^{(\ell+1)} = \mathcal{F}_{\mathrm{EGFL}}(\mathbf{P}, \mathbf{Q}, \mathbf{X}_C), \quad \mathbf{H}^{(\ell+1)} = \mathcal{F}_{\mathrm{IPFL}}(\mathbf{P}, \mathbf{Q})$$

消融实验（Table 5）表明，$\mathcal{F}_{\mathrm{EGI}}$ 和 $\mathcal{F}_{\mathrm{IPI}}$ 各自贡献约 6mm 的平均 MPJPE 增益，二者结合效果最佳。

### 3.3 不动点求解与训练

前向传播中，不动点通过黑盒求解器（如 Anderson mixing）求解根查找问题：

$$g(\mathbf{z}, \mathbf{x} | \theta) = f(\mathbf{z}, \mathbf{x} | \theta) - \mathbf{z} = 0$$

收敛判据为残差阈值 $\varepsilon = 10^{-3}$，实际迭代次数通常为 10-30 步。

**训练目标**在不动点约束下最小化解码输出与真值的 MSE：

$$\hat{\boldsymbol{\theta}} = \arg \min_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{MSE}}( \mathcal{F}_{\mathrm{EOL}}(\mathbf{z}^*), \mathbf{Y}) \quad \mathrm{s.t.} \quad \mathbf{z}^* = f(\mathbf{z}^*, \mathbf{x} | \boldsymbol{\theta})$$

**隐式梯度**通过隐函数定理计算，仅依赖平衡态 $\mathbf{z}^*$，实现 $O(1)$ 训练内存：

$$\frac{\partial \mathcal{L}_{\mathrm{MSE}}}{\partial \boldsymbol{\theta}} = \frac{\partial \mathcal{L}_{\mathrm{MSE}}}{\partial \mathbf{z}^*} \left( \mathbf{I} - \frac{\partial f(\mathbf{z}^*, \mathbf{x} | \boldsymbol{\theta})}{\partial \mathbf{z}^*} \right)^{-1} \frac{\partial f(\mathbf{z}^*, \mathbf{x} | \boldsymbol{\theta})}{\partial \boldsymbol{\theta}}$$

实际采用 **2 步截断 Neumann 级数**近似逆雅可比矩阵，平衡效率与精度：

$$\frac{\partial \mathcal{L}_{\mathrm{MSE}}}{\partial \boldsymbol{\theta}} \approx \frac{\partial \mathcal{L}_{\mathrm{MSE}}}{\partial \mathbf{z}^*} \left( \mathbf{I} + \frac{\partial f(\mathbf{z}^*, \mathbf{x} | \boldsymbol{\theta})}{\partial \mathbf{z}^*} \right) \frac{\partial f(\mathbf{z}^*, \mathbf{x} | \boldsymbol{\theta})}{\partial \boldsymbol{\theta}}$$

消融实验（Figure 8b）证实截断梯度显著优于不精确的 JFB 梯度。

### 3.4 稀疏不动点监督

传统多阶段方法（如 PGBIG）需要手工递归平滑真值作为各阶段中间监督。MotionDEQ 采用**稀疏不动点校正损失**，直接在最终不动点和若干采样中间状态上与原始真值对齐：

$$\mathcal{L}_{total} = \| \mathcal{F}_{\mathrm{EOL}}(\mathbf{z}^*) - \mathbf{Y} \|_2^2 + \gamma \| \mathcal{F}_{\mathrm{EOL}}(\mathbf{z}^{(\ell)}) - \mathbf{Y} \|_2^2$$

其中 $\gamma = 0.8$。消融实验（Table 4）表明，稀疏监督（Num. 1）在 100/200/400ms 分别达到 13.98/30.63/61.38mm，而平滑 GT 监督导致训练不稳定（NaN），验证了该设计避免了手工中间目标的需求。

### 3.5 流式适配

流式运动预测中，MotionDEQ 将前一轮的不动点作为当前轮的热启动初始猜测，大幅减少求解器迭代次数。此外，**等变校正适配器 $\mathcal{F}_{\mathrm{ECA}}$** 利用上一轮预测偏差进行轻量校正：

$$\mathbf{H}' = \mathcal{F}_{\mathrm{DL}}(\widehat{\mathbf{Y}}_r - \mathbf{X}_{r+1}), \quad \mathbf{H} = \mathbf{H}_{r+1}^* + \mathsf{MLP}(\mathbf{H}'), \quad \mathbf{G}' = \mathcal{F}_{\mathrm{EGNN}}(\mathbf{G}_{r+1}^*, \mathbf{H}), \quad \widehat{\mathbf{Y}}_{r+1} = \mathcal{F}_{\mathrm{EOL}}(\mathbf{G}')$$

该适配器保持等变性，但需要上一预测轮次的真值，在离线推理中不可用。

### 补充图表

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/003_Figure_3.jpg]]
*Figure 3: Our DEQ model adaption to streaming human motion*



## 实验与关键发现

### 短期预测主结果

MotionDEQ 在三个标准人体运动预测基准上与多个代表性基线进行了对比，包括 **Res-sup.**（Martinez et al., CVPR 2017）、**LTD**（Mao et al., ICCV 2019）、**MSR-GCN**（Dang et al., ICCV 2021）、**PGBIG**（Ma et al., CVPR 2022）、**EqMotion**（Xu et al., CVPR 2023）、**SiMLPe**（Guo et al., WACV 2023）、**ALIEN**（Wei et al., CVPR 2025）和 **LuKAN**（Hasan et al., BMVC 2025）。所有对比均在关闭流式信息（即不使用等变校正适配器）的标准设置下进行，确保公平性。

**Human3.6M 数据集。** 在 Table 1 的短期预测结果中，MotionDEQ 在 walking 动作的四个预测时间步上均取得最优或次优性能：80ms 处 MPJPE 为 8.8mm，160ms 处为 17.3mm，320ms 处为 32.2mm，400ms 处为 38.8mm。与最强基线 EqMotion 相比，400ms 处误差降低 2.1mm（38.8 vs 40.9），320ms 处降低 1.3mm（32.2 vs 33.5）。从 80–400ms 的平均 MPJPE 来看，MotionDEQ 达到 32.1mm，优于 EqMotion 的约 32.4mm。值得注意的是，这一性能仅使用了不到 300K 参数（298K），而 SiMLPe 虽以 140K 参数达到 57.3mm，但精度明显落后；EqMotion 参数量更大但精度反而不及。Figure 4 的精度-参数量散点图直观展示了 MotionDEQ 在 trade-off 上的优势：以极轻量的参数预算实现了最优预测精度。

**CMU-MoCap 和 3DPW 数据集。** Table 2 的结果表明，MotionDEQ 在 CMU-MoCap 上全面超越所有基线。在更具挑战性的 3DPW 数据集上，MotionDEQ 在 200ms 处相较最佳基线提升 4.6%，在 400ms 处提升 3.3%，验证了该方法在野外场景下的鲁棒性。

### 消融实验

**监督策略。** Table 4 对比了三种监督方式：（1）稀疏不动点校正损失（本文方法）；（2）平滑真值作为中间目标；（3）密集阶段监督。稀疏监督在 100/200/400ms 分别达到 13.98/30.63/61.38mm 的 MPJPE，而平滑真值方案导致训练不稳定（NaN），密集监督则因手工设计的中间目标偏离真实运动分布而精度下降。这证明直接对齐不动点与原始真值既简化了训练流程，又避免了中间目标的分布偏移问题。

**网络组件。** Table 5 的组件消融揭示了各模块的独立贡献。完整的 MotionDEQ 平均 MPJPE 为 32.1mm。移除等变几何注入 F_EGI 后，误差急剧上升至 38.1mm（+6.0mm）；移除不变模式注入 F_IPI 后，误差升至 35.3mm（+3.2mm）。若进一步退化为基础 DEQ 公式（仅 Eq.(2)，无观察条件注入），误差飙升至 71.4mm，充分说明观察条件的等变/不变注入是模型有效性的关键。

**前向迭代与后向梯度。** Figure 8(a) 显示，随着前向迭代次数增加，预测误差单调下降，约 10 次迭代后性能趋于饱和。Figure 8(b) 对比了截断 Neumann 梯度（2-step）与不精确 JFB 梯度：截断梯度在所有时间步上均显著优于 JFB，验证了通过 Neumann 级数近似逆雅可比矩阵在精度-效率权衡上的优越性。Figure 6(a) 进一步表明，良好的不动点收敛（低残差）与更高的预测精度正相关。

**RNN 变体对比。** Table 3 在 3DPW 数据集上，以相同参数预算对比了 RNN 堆叠版本与 DEQ 版本。DEQ 的无限深度特性带来了持续的精度增益，验证了“深度即精度”的核心假设在运动预测任务中成立。

### 流式预测分析

Figure 7 展示了等变校正适配器 F_ECA 在流式场景下的影响。在 80ms 和 400ms 两个时间步上，F_ECA 对各类动作均带来一致的误差降低，尤其在长时预测（400ms）上增益更为显著。适配器的核心机制在于利用上一轮预测与当前观测的偏差，通过等变校正网络调整几何特征，从而有效抑制误差累积。

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/012_Figure_7.jpg]]
*Figure 7: Influence of*

### 定性结果

Figure 5 以 walkingtogether 动作为例展示了预测姿势的可视化对比。MotionDEQ 的预测轨迹（蓝色）与真值（绿色虚线）高度吻合，尤其在肢体末端关节的细粒度运动上明显优于基线方法，验证了无限次细化对运动细节的捕捉能力。

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/006_Figure_5.jpg]]
*Figure 5: Visualization comparison results on an example of action walkingtogether, where green dotted line represents ground truth*

### 局限与待验证问题

尽管 MotionDEQ 在标准基准上表现优异，仍存在以下边界条件需注意：

- **热启动的连续性假设。** 流式预测中复用上一轮不动点作为热启动依赖于运动帧间的高度时间一致性。当运动发生剧烈突变时，旧的不动点可能引入偏差，导致收敛速度下降甚至精度损失。这一场景下的鲁棒性尚未充分验证。
- **等变校正适配器的真值依赖。** F_ECA 需要上一预测轮次的真值进行偏差计算，在离线推理或无法获取实时真值的场景中不可用。如何设计无真值校准的自适应热启动机制是一个开放问题。
- **推理延迟。** 虽然训练内存恒定（O(1)），但推理时不动点求解器通常需要 10–30 次迭代，在极端低延迟场景下仍存在开销。能否通过单调算子设计等理论工具进一步减少迭代次数，目前缺乏理论保证。
- **架构泛化性。** 当前 MotionDEQ 仅基于 EqMotion 骨干验证，向其他等变预测器（如 Transformer、扩散模型）的迁移效果尚未实验。

### 补充图表

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/004_Table_1.jpg]]
*Table 1: Short-term prediction results on Human3.6M. ‘†’ denotes the average results over 5 runs from our reimplementation using released code due to its high sensitivity to network initialization. The best and second-best results are marked in bold and underline, respectively*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/005_Table_2.jpg]]
*Table 2: Results of average prediction errors on CMU-MoCap and 3DPW datasets*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/008_Figure_4.jpg]]
*Figure 4: Comparison of accuracy and parameter on Human3.6M*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/009_Figure_6.jpg]]
*Figure 6: Results of convergence, memory and inference time*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/011_Table_5.jpg]]
*Table 5: Ablation study on network designs on Human3.6M*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/010_Table_4.jpg]]
*Table 4: Ablations on smooth and dense supervision. ‘Num.’ is the number of correction losses, ‘NaN’ means training instability*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/013_Figure_8.jpg]]
*Figure 8: Ablations on forward iterations and backward gradients*

![[assets/figures/papers/paper_list_l1077_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Progressive_Guessi/figures/007_Table_3.jpg]]
*Table 3: Comparison result of RNN-variants on 3DPW dataset*



## 定位与知识库关联

### 1. 渐进式猜测范式的谱系定位

MotionDEQ 直接承袭并重构了**渐进式猜测（Progressive Guessing）**这一人体运动预测子领域的方法论。该范式的核心思想是将未来运动的预测分解为多阶段逐步细化：先产生一个粗糙的初始猜测，再通过堆叠的细化模块逐阶段逼近真值。代表性工作包括 **PGBIG**（Ma et al., CVPR 2022）和 **EqMotion**（Xu et al., CVPR 2023）。

MotionDEQ 与这些前驱工作的关系并非简单的性能超越，而是一次**范式层面的重新思考**：

- **PGBIG** 首次提出“猜测-细化”框架，但各阶段参数独立，需要手工设计递归平滑的真值作为中间监督目标，且阶段数 $L$ 为固定经验值，缺乏明确的停止准则。
- **EqMotion** 将等变/不变约束引入渐进式猜测，在几何一致性和交互建模上取得突破，但仍沿用了多阶段独立参数的架构，参数冗余和计算开销随深度线性增长。
- **MotionDEQ** 将上述多阶段过程重铸为**共享参数的不动点求解问题**：所有迭代共享同一组参数 $\theta$，通过求解 $g(\mathbf{z}, \mathbf{x} | \theta) = f(\mathbf{z}, \mathbf{x} | \theta) - \mathbf{z} = 0$ 实现概念上无限次的细化，停止准则由残差收敛（$\varepsilon = 10^{-3}$）自然界定。这一转变的因果机制在于：渐进式猜测本质上是一个有限步迭代过程，而深度均衡模型（DEQ）将其转化为不动点问题后，可以等价地执行无限次细化，且天然与流式运动数据的特点契合。

### 2. 与主流基线的对比定位

在更广泛的人体运动预测方法谱系中，MotionDEQ 的定位可通过以下基线的对比来理解：

| 基线方法 | 核心思路 | MotionDEQ 与之的差异 |
|----------|----------|----------------------|
| **Res-sup.** (Martinez et al., CVPR 2017) | 残差连接 + 直接回归 | 无渐进细化机制，长时预测误差累积显著 |
| **LTD** (Mao et al., ICCV 2019) | 时间离散余弦变换编码 | 频域建模，缺少几何等变约束 |
| **MSR-GCN** (Dang et al., ICCV 2021) | 多尺度图卷积 | 图结构建模但无等变/不变分解 |
| **SiMLPe** (Guo et al., WACV 2023) | 极简多层感知机 | 参数极少（~140K），但精度受限 |
| **ALIEN** (Wei et al., CVPR 2025) | 等变交互建模 | 同期工作，未采用 DEQ 无限深度范式 |
| **LuKAN** (Hasan et al., BMVC 2025) | Kolmogorov-Arnold 网络 | 函数逼近路径不同，未涉足不动点求解 |

从精度-参数量 trade-off 来看（Figure 4），MotionDEQ 以约 298K 参数在 Human3.6M 上达到 55.3mm（@400ms）的平均 MPJPE，在参数效率上显著优于 SiMLPe（140K 参数 / 57.3mm）和 EqMotion（更大参数量 / 56.8mm），形成了新的 Pareto 前沿。

### 3. 核心设计决策的消融证据与因果解释

MotionDEQ 的性能优势源于四个关键设计决策，每个决策均有消融实验支撑：

**（1）稀疏不动点监督替代平滑真值监督。** PGBIG 需要手工设计递归平滑的真值作为各阶段中间目标，这不仅引入了人工先验偏差，还可能导致训练不稳定。MotionDEQ 采用稀疏不动点校正损失 $\mathcal{L}_{total} = \|\mathcal{F}_{\mathrm{EOL}}(\mathbf{z}^*) - \mathbf{Y}\|_2^2 + \gamma \|\mathcal{F}_{\mathrm{EOL}}(\mathbf{z}^{(\ell)}) - \mathbf{Y}\|_2^2$（$\gamma = 0.8$），直接在最终不动点和稀疏采样的中间状态上与原始真值对齐。消融实验（Table 4）表明：平滑真值策略导致训练不稳定（NaN），而稀疏监督（Num. 1）在 100/200/400ms 分别达到 13.98/30.63/61.38mm 的最优精度。

**（2）等变/不变观察条件注入。** MotionDEQ 将观察到的运动特征作为外部条件，通过等变几何注入 $\mathcal{F}_{\mathrm{EGI}}$ 和不变模式注入 $\mathcal{F}_{\mathrm{IPI}}$ 融入每次 DEQ 迭代。消融实验（Table 5）显示：移除 $\mathcal{F}_{\mathrm{EGI}}$ 导致平均 MPJPE 从 32.1mm 升至 38.1mm（+6.0mm），移除 $\mathcal{F}_{\mathrm{IPI}}$ 升至 35.3mm（+3.2mm），而使用无注入的原始 DEQ 公式（Eq. 2）则升至 71.4mm。这揭示了观察条件的持续注入是不动点收敛到正确解的必要条件。

**（3）截断 Neumann 梯度替代 JFB 不精确梯度。** 隐式微分中逆雅可比矩阵的计算是 DEQ 训练的核心挑战。MotionDEQ 采用 2 步 Neumann 级数近似 $\frac{\partial \mathcal{L}}{\partial \boldsymbol{\theta}} \approx \frac{\partial \mathcal{L}}{\partial \mathbf{z}^*} (\mathbf{I} + \frac{\partial f}{\partial \mathbf{z}^*}) \frac{\partial f}{\partial \boldsymbol{\theta}}$，相比 JFB（Jacobian-Free Backpropagation）不精确梯度显著提升了预测精度（Figure 8b）。这一选择的因果机制在于：JFB 的一阶近似在不动点附近引入了不可忽略的梯度偏差，而 2 步截断在精度与计算开销之间取得了平衡。

**（4）流式热启动与等变校正适配器。** 流式运动预测场景下，MotionDEQ 将上一预测轮次的不动点作为当前轮次的热启动初始猜测，显著加速求解器收敛（Figure 6a）。此外，等变校正适配器 $\mathcal{F}_{\mathrm{ECA}}$ 利用上一轮预测偏差进行轻量校正（Eq. 12），在不同动作类型上的增益在 80ms 和 400ms 均有体现（Figure 7）。该设计的局限在于：$\mathcal{F}_{\mathrm{ECA}}$ 需要上一预测轮次的真值，在无法获取实时真值的离线推理中不可用。

### 4. 适用边界与局限

MotionDEQ 的适用边界受以下因素制约：

- **骨干架构依赖。** 当前实现仅基于 EqMotion 的等变/不变分解骨干验证，向其他等变预测器（如基于 Transformer 或扩散模型的架构）的迁移泛化性尚未实验。DEQ 范式的优势是否能跨架构保持，仍是一个开放问题。
- **推理延迟。** 尽管训练内存为 $O(1)$（相比多阶段模型的 2× 以上节省），推理时需要迭代求解器执行 10–30 次前向迭代（Figure 6a），在极端低延迟场景下仍有一定开销。10 次迭代后性能趋于饱和，但收敛速度的理论保证尚未建立。
- **运动连续性假设。** 热启动初始猜测依赖于连续运动帧的高度时间一致性。当运动发生剧烈突变（如突然转向、跌倒）时，复用旧的不动点可能引入偏差，导致收敛到次优解或需要更多迭代步数。
- **离线场景的适配器失效。** 等变校正适配器 $\mathcal{F}_{\mathrm{ECA}}$ 需要获取上一轮预测的真值进行偏差计算，在纯离线推理中不可用。如何设计无真值校准的自适应热启动机制，是流式部署中的关键开放问题。

### 5. 开放问题与后续方向

基于上述分析，以下开放问题值得后续工作关注：

1. **跨架构泛化性。** DEQ 范式能否与 Transformer、扩散模型等先进运动预测架构结合并保持优势？不动点求解的隐式无限深度特性是否与自注意力机制的全局感受野产生协同或冲突？
2. **收敛速度的理论与工程优化。** 固定点求解的收敛速度是否存在理论保证？能否通过模型设计（如单调算子约束、Lipschitz 正则化）进一步减少所需迭代次数，逼近实时推理需求？
3. **鲁棒热启动策略。** 在运动突变或无真值校准的离线场景，如何设计自适应的初始猜测机制？例如，基于运动模式切换检测动态选择冷启动或热启动策略。
4. **多人交互与异构传感器场景。** 在多人交互运动或惯性传感器等异构数据源的流式预测中，该框架的等变/不变分解是否仍然适用？交互图的不动点求解是否会引入额外的收敛挑战？



## 原文 PDF

![[paperPDFs/CVPR_2026/Progressive_Guessing_to_Fixed_Point_Rethinking_Human_Motion_Prediction_with_Deep_Equilibrium_Models.pdf]]

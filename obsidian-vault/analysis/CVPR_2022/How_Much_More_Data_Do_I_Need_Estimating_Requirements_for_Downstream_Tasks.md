---
title: "How Much More Data Do I Need? Estimating Requirements for Downstream Tasks"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/How_Much_More_Data_Do_I_Need_Estimating_Requirements_for_Downstream_Tasks.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/estimatingrequirements/
aliases:
- DREFCFMRC
- HMMDDINERDT
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过引入修正因子 τ 提高目标值、允许多轮（T=5）迭代收集，并综合多种回归函数（乐观/悲观）构建区间，可将数据收集量控制在最小需求的 1-2 倍以内。"
primary_logic: "经典的 Power Law 等函数能较好外推性能曲线，但直接求解目标性能对应的数据量对拟合误差极度敏感。改用乐观回归函数（如 Power Law、Logarithmic）配合校正因子 τ 并在多轮收集框架下迭代修正，可以在大多数任务上以不超过最小需求 2 倍的数据量稳定达到目标。"
claims:
- "在 ImageNet 上，四条外推曲线均达到 1-6% 的精度误差，但估计所需数据量却偏离 12 万到 31 万张图像。"
- "Arctan 函数在 ImageNet 上取得最低 RMSE（3.19），但用于估计数据需求会导致首轮即收集约 450 万张图像，远超实际需要的 90 万张。"
- "结合校正因子 τ 并在 T=5 轮收集下，Power Law、Logarithmic 和 Algebraic Root 函数在多个数据集上将收集数据量与最小需求之比控制在 1.03 至 2.5 之间。"
- "仅使用一轮收集时，综合所有回归函数的最大/最小估计能够频繁地上下界真实数据需求；图像分类任务中上界成功率超过 80%。"
---

# How Much More Data Do I Need? Estimating Requirements for Downstream Tasks

> [!tip] 核心洞察
> 经典的 Power Law 等函数能较好外推性能曲线，但直接求解目标性能对应的数据量对拟合误差极度敏感。改用乐观回归函数（如 Power Law、Logarithmic）配合校正因子 τ 并在多轮收集框架下迭代修正，可以在大多数任务上以不超过最小需求 2 倍的数据量稳定达到目标。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 下游任务数据需求估计：还需多少数据？ |
| 英文题名 | How Much More Data Do I Need? Estimating Requirements for Downstream Tasks |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2207.01725) · [Project](https://nv-tlabs.github.io/estimatingrequirements/) · [Project](https://research.nvidia.com/labs/toronto-ai/estimatingrequirements/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Data Requirement Estimation Framework with Correction Factor and Multi‑round Collection |
| Dataset | CIFAR10, CIFAR100, ImageNet, VOC, nuScenes (3D det / BEV seg), BDD100K, Image classification (CIFAR10/100, ImageNet) |

> [!tip] 效果简介
> - CIFAR10, CIFAR100, ImageNet, VOC, nuScenes (3D det / BEV seg), BDD100K 上，collected / minimum required data ratio (n₀+ n̂) / (n₀+ n*) 为 with τ, T=5, Power Law/Logarithmic/Algebraic Root achieve ratios between 1 and...，对比 single‑round Power Law without τ yields ratios < 1 (under‑estimates)，变化 eliminates under‑estimation; target met with at most ~2× minimum data on diverse vision tasks。
> - Image classification (CIFAR10/100, ImageNet) 上，frequency of bounding true data requirement 为 using all regression functions (max/min estimates) bounds true n* in over 80% o...，对比 single regression function does not consistently bound the requirement，变化 provides reliable interval estimate when only one round is available。

## 概要

下游任务的数据需求估计面临一个根本性瓶颈：**即使回归函数能够以较低误差外推模型性能曲线，直接求解目标性能对应的数据量仍会对拟合误差极度敏感**，导致所需数据量被严重高估或低估。在 ImageNet 上，四条外推曲线的精度误差仅为 1–6%，但估计的数据需求却偏离真实需求 12 万至 31 万张图像（Figure 1）。

本文的核心洞察在于：将“性能外推”与“数据需求求解”解耦，通过引入**校正因子 τ** 提高目标值、允许多轮（T=5）迭代收集，并综合多种回归函数（乐观/悲观）构建估计区间，可以在大多数任务上将实际收集数据量控制在最小需求的 1–2 倍以内。

方法层面，本文提出了一个**带校正因子的多轮数据需求估计框架**，相较于传统的单轮幂律外推方法，做出了三项关键改进：

1. **回归函数扩展**：在幂律函数之外引入 Arctan、Logarithmic 和 Algebraic Root 三种凹单调递增函数，利用不同函数的乐观/悲观倾向构建上下界估计。
2. **多轮迭代收集**：将单次估计改为最多 T=5 轮的迭代过程，每轮重新拟合回归模型并修正数据需求估计。
3. **目标校正**：在估计所需数据量时，将目标性能从 V* 提升至 V* + τ，以克服回归误差导致的系统性低估。

实验覆盖图像分类（CIFAR10/100、ImageNet）、2D/3D 目标检测（VOC、nuScenes）和语义分割（BDD100K、nuScenes BEV）等多种视觉任务。主要结果表明：结合校正因子 τ 并在 T=5 轮收集下，Power Law、Logarithmic 和 Algebraic Root 函数在多数数据集上将收集数据量与最小需求之比控制在 1.03 至 2.5 之间（Figure 4, Table 4），有效消除了单轮幂律外推的严重低估问题。当仅允许单轮收集时，综合所有回归函数的最大/最小估计能够在图像分类任务中以超过 80% 的频率上下界真实数据需求（Figure 5）。

该方法仍存在若干限制：假设模型和数据采样策略在收集过程中保持不变；校正因子 τ 需在留出任务上调参；以及对于不满足凹单调特性的任务（如个别类别 AP 波动），回归函数的适用性有待进一步验证。



### 问题定义：下游任务的数据需求估计

在构建机器学习系统时，一个反复出现的实际问题是：**为达到目标性能，还需要收集多少数据？** 给定一个初始数据集 $\mathcal{D}_0$（大小为 $n_0$）、一个模型 $f$ 和一个目标得分 $V^*$，数据收集问题的目标是确定最小的额外数据量 $\hat{n}$，使得在最多 $T$ 轮迭代收集中，模型在扩充数据集上的得分达到或超过 $V^*$。

这一问题的核心挑战在于：**模型性能随数据量变化的曲线 $v(n)$ 在收集开始前是未知的**。因此，必须从有限的初始数据出发，通过外推来估计数据需求。

### 现有方法的根本瓶颈：外推精度 ≠ 需求估计精度

现有的神经缩放律（neural scaling laws）研究表明，模型性能与数据集大小之间通常遵循幂律关系 $V \propto \theta_1 n^{\theta_2}$。基于这一观察，自然的方法是：用初始数据拟合一条性能曲线，然后求解目标性能对应的数据量。

然而，本文揭示了一个关键发现：**即使外推曲线在精度预测上误差很小，在数据需求估计上也可能产生巨大偏差**。如 Figure 1 所示，在 ImageNet 上，四条回归函数从 50% 数据外推时，精度误差仅为 1–6%，但估计所需数据量却偏离真实需求 12 万到 31 万张图像。更极端的是，Arctan 函数在 ImageNet 上取得了最低的 RMSE（3.19，Table 3），但用于估计数据需求时，首轮就会要求收集约 450 万张图像，远超实际需要的 90 万张。

这一现象的根本原因在于：**性能曲线在目标值附近趋于平缓时，微小的外推误差会被放大为巨大的数据量估计误差**。换言之，一个在 RMSE 意义上“最优”的回归函数，在数据需求估计这一下游任务上可能表现最差。

### 现有方法的两个关键缺口

1. **单轮估计的不可靠性**：传统的幂律外推方法通常采用单轮估计（single-shot estimation），即一次性估计所需数据量并全部收集。但如 Figure 3 所示，在 T=1 时，Power Law 函数在多个数据集上频繁低估数据需求（ratio < 1），导致无法达到目标性能。单轮估计缺乏迭代修正的机会，对初始拟合误差极为敏感。

2. **单一回归函数的局限性**：仅依赖幂律函数无法刻画不同任务上性能曲线的多样性。某些任务（如 VOC、BDD100K）的性能曲线可能不完全满足 concave 和单调递增的假设，单一函数的外推方向（乐观或悲观）也难以预判。Figure 5 表明，仅使用单一回归函数无法一致地上下界真实数据需求。

### 本文动机与核心思路

基于上述分析，本文的核心动机是：**构建一个能够可靠、高效地估计数据需求的框架，使得实际收集的数据量尽可能接近最小需求量**。

核心思路包含三个关键设计：

- **多函数集成**：引入四类 concave 单调递增回归函数（Power Law、Arctan、Logarithmic、Algebraic Root，Table 1），利用不同函数的外推特性（乐观/悲观）构建估计区间，而非依赖单一函数。

- **多轮迭代收集**：将数据收集过程组织为最多 $T=5$ 轮的迭代循环（Figure 2），每轮重新拟合回归函数并修正估计，逐步逼近真实需求。

- **校正因子 $\tau$**：在估计数据需求时，将目标性能提高一个偏置项 $\tau$（即求解 $\hat{v}(n_0 + \hat{n}; \boldsymbol{\theta}^*) \ge V^* + \tau$），以克服回归误差导致的系统性低估。$\tau$ 可在一个保留任务（如 CIFAR10）上调参确定。



## 核心方法与创新机理

### 从“拟合优度”到“需求稳健性”的视角转换

传统数据需求估计方法（如单轮 Power Law 外推）的核心逻辑是：用初始数据拟合一条性能曲线 $\hat{v}(n)$，然后直接求解 $\hat{v}(n_0 + \hat{n}) \ge V^*$ 得到所需数据量。这一范式隐含假设“外推误差小则估计准确”，但本文揭示了一个关键悖论：**即使回归函数的外推 RMSE 低至 1–6%，对数据需求的估计仍可能偏离 12 万至 31 万张图像**（Figure 1, ImageNet 案例）。根本原因在于，求解逆函数 $n = \hat{v}^{-1}(V^*)$ 对拟合参数的微小扰动极度敏感——当性能曲线在目标附近趋于平缓时，微小的预测偏差会被急剧放大。

这一洞察构成了方法创新的出发点：**将优化目标从“拟合性能曲线”转向“稳健地满足目标性能”**。本文的核心贡献在于三个相互耦合的 changed slots，共同构建了一个多轮迭代、带有校正机制和区间估计的数据需求估计框架。

### Changed Slot 1：从单一幂律到多函数回归族

**Baseline**：仅使用 Power Law 函数 $\hat{v}(n;\theta_1,\theta_2,\theta_3) = \theta_1 n^{\theta_2} + \theta_3$ 进行外推。

**Proposed**：引入四个凹单调递增回归函数——Power Law、Arctan、Logarithmic 和 Algebraic Root（Table 1），利用它们在渐近行为上的差异构建“乐观–悲观”谱系：

- **Logarithmic**（无上界，增长渐缓）：通常给出乐观估计（低估数据需求）
- **Power Law**（无上界，幂次增长）：居中
- **Algebraic Root**（有界，趋于饱和）：偏悲观
- **Arctan**（有界，快速饱和）：最悲观（高估数据需求）

这一设计的深层逻辑并非追求更低的 RMSE——事实上 Arctan 在 ImageNet 上取得了最低 RMSE（3.19，Table 3），但若直接用于估计数据需求，首轮就会要求收集约 450 万张图像，远超实际所需的 90 万张。多函数族的真正价值在于：**不同函数的估计偏差方向不同，联合使用可以形成对真实需求的上下界**。实验表明，即使仅用单轮收集（T=1），取所有函数估计的最大/最小值也能在图像分类任务上以超过 80% 的频率成功界定真实需求 $n^*$（Figure 5）。

### Changed Slot 2：从单次估计到多轮迭代收集

**Baseline**：一次性估计并收集全部所需数据（single shot）。

**Proposed**：将数据收集过程组织为最多 T=5 轮的迭代循环（Algorithm 1, Figure 2），每轮包含四个步骤：

1. **回归数据集构建**：从已有数据中生成 $r \le 10$ 个线性增长的嵌套子集，计算性能分数形成回归集合 $\mathcal{R}$
2. **回归模型拟合**：用加权最小二乘法拟合选定的回归函数
3. **数据需求估计**：求解满足 $\hat{v}(n_0 + \hat{n}; \boldsymbol{\theta}^*) \ge V^* + \tau$ 的最小 $\hat{n}$
4. **数据收集与评估**：采样 $\hat{n}$ 个新数据点，训练模型，评估性能，更新回归集合

多轮迭代的关键机制在于**逐步修正外推偏差**：首轮基于少量数据的外推可能严重偏离，但随着每轮收集新数据并重新拟合，回归函数逐渐逼近真实性能曲线，后续轮次的估计精度持续提升。Figure 3 的系统性模拟显示，T=1 时各函数在多个数据集上频繁出现 ratio < 1（低估导致无法达标）或 ratio ≫ 2（严重高估），而 T=5 时乐观函数（Power Law、Logarithmic、Algebraic Root）可将 ratio 控制在 1–2 之间。

### Changed Slot 3：校正因子 τ——从“恰好达标”到“留有余量”

**Baseline**：无校正机制，直接以目标性能 $V^*$ 为约束求解数据量。

**Proposed**：在估计约束中引入校正因子 $\tau$，将目标提升为 $V^* + \tau$（Section 5.1）。

这一设计的动机直接源于 Figure 3 的发现：乐观回归函数（如 Power Law、Logarithmic）在 T=5 时虽能将 ratio 压至接近 1，但频繁出现 ratio < 1 的低估情况——即实际收集的数据量不足以达到目标性能。$\tau$ 的作用是**强制回归函数在估计时“瞄准更高”，从而补偿拟合误差导致的系统性低估**。

$\tau$ 的调参在一个保留任务（CIFAR10）上完成，然后直接迁移到其他数据集。Figure 4 和 Table 4 的结果表明，结合 $\tau$ 后，Power Law、Logarithmic 和 Algebraic Root 在 T=5 时可将收集数据量与最小需求的比值控制在 1.03 至 2.5 之间，彻底消除了低估问题，且高估幅度可控。

### 创新耦合与系统效应

三个 changed slots 并非独立运作，而是形成协同增效：

- **多函数族**提供了“乐观–悲观”的估计谱系，使得单轮场景下即可构建需求区间（Figure 5），也为多轮迭代提供了不同风险偏好的估计器选择
- **多轮迭代**通过反复修正降低了对外推精度的依赖，使得即使使用较简单的回归函数也能逐步收敛
- **校正因子 τ** 弥补了乐观函数在多轮迭代中仍存在的系统性低估倾向，确保“达标”优先于“精准”

这一组合策略在六个不同规模和模态的数据集（CIFAR10/100、ImageNet、VOC、nuScenes 3D 检测/BEV 分割、BDD100K）上均表现出鲁棒性，覆盖了图像分类、2D 检测、3D 检测和语义分割等任务。值得注意的是，在 nuScenes 的类别级 AP 实验中（Figure 8），即使使用从 CIFAR10 迁移的 τ，多数类别的 ratio 仍能控制在 1–3 之间，验证了校正因子的跨任务泛化潜力。

### 方法局限

需注意以下边界条件（详见论文 Limitations）：

1. 假设模型架构 $f$ 和数据采样策略 $p(z)$ 在整个收集过程中保持不变，未考虑模型更新或超参数调整的影响
2. 回归函数的凹单调假设在 VOC、BDD100K 等任务上不完全成立（Figure 3 中 Arctan 和 Algebraic Root 的 ratio 曲线出现异常波动）
3. 校正因子 $\tau$ 需在保留任务上调参，当目标任务特性与调参任务差异较大时可能不够鲁棒
4. 模拟中以 ground truth $v(n)$ 代替实际重新训练，可能低估了重复训练引入的方差



本文提出的数据需求估计框架围绕一个核心迭代循环构建：**用有限初始数据拟合性能外推函数 → 估计达到目标性能所需数据量 → 按估计量收集新数据 → 重新拟合并修正估计**，在最多 T 轮内逐步逼近真实的数据需求。图 Figure 2 展示了这一循环的宏观流程。

### 问题形式化

给定一个初始已标注数据集 $\mathcal{D}_0$（大小为 $n_0$）、一个固定的模型训练与评估 pipeline $f$，以及一个目标性能值 $V^*$，数据收集问题的目标是：在最多 $T$ 轮内，确定最小的额外数据量 $\hat{n}$，使得在 $\mathcal{D}_0 \cup \hat{\mathcal{D}}$ 上训练的模型性能 $V_f(\mathcal{D}_0 \cup \hat{\mathcal{D}}) \ge V^*$。每一轮中，算法根据已有数据估计所需的 $\hat{n}$，按此数量采样新数据，重新训练并评估模型，将新的 $(n, V_f)$ 点加入回归数据集，供下一轮修正使用。

### Pipeline 核心模块

框架由四个顺序模块构成，对应 Algorithm 1 的主循环：

1. **回归数据集构建（Regression dataset creation）**  
   从当前已收集数据中，按线性增长方式采样 $r$ 个嵌套子集（$r \le 10$ 以保证低成本），在每个子集上训练模型并计算性能分数，形成回归数据集 $\mathcal{R} = \{(n_i, V_f(\mathcal{S}_i))\}$。子集大小按 $|\mathcal{S}_i| = |\mathcal{D}_0| (i+1)/r$ 增长（见 Section 4.1）。

2. **回归模型拟合（Regression model fitting）**  
   在 $\mathcal{R}$ 上，通过加权最小二乘法拟合四个预设的凹单调递增回归函数之一：Power Law、Arctan、Logarithmic 或 Algebraic Root（函数形式见 Table 1）。这些函数均具有三个可学习参数 $\pmb{\theta} = \{\theta_1, \theta_2, \theta_3\}$，且被设计为满足模型性能随数据量增长的 concave 和 monotonically increasing 特性（见 Section 3.2）。

3. **数据需求估计（Data requirement estimation）**  
   利用拟合好的回归函数 $\hat{v}(n; \pmb{\theta}^*)$，求解满足校正后目标约束的最小 $\hat{n}$：
   $$\hat{v}(n_0 + \hat{n}; \pmb{\theta}^*) \ge V^* + \tau$$
   其中 $\tau$ 为校正因子，用于对抗回归误差导致的低估（见 Section 5.1）。若无校正（$\tau=0$），直接求解 $V^*$ 对应的数据量对拟合误差极度敏感，常导致严重低估或高估。

4. **数据收集与评估（Data collection and evaluation）**  
   采样 $\hat{n}$ 个新数据点加入 $\hat{\mathcal{D}}$，在 $\mathcal{D}_0 \cup \hat{\mathcal{D}}$ 上重新训练模型 $f$，评估性能分数 $V_f$，并将新的 $(n_0 + \hat{n}, V_f)$ 点加入回归数据集 $\mathcal{R}$，进入下一轮迭代。

### 输入输出流

- **输入**：初始数据集 $\mathcal{D}_0$（大小 $n_0$），目标性能 $V^*$，最大轮数 $T$，校正因子 $\tau$，回归函数选择，子集数 $r$。
- **输出**：最终收集的数据总量 $n_0 + \hat{n}$，以及对应的模型性能 $V_f$。
- **中间状态**：每轮更新回归数据集 $\mathcal{R}$、回归参数 $\pmb{\theta}^*$、估计需求量 $\hat{n}$。

### 关键设计选择

- **多函数策略**：单一回归函数（如 Power Law）在性能外推上 RMSE 较低，但用于数据需求估计时方向性偏差显著。框架引入四类函数（乐观的 Power Law、Logarithmic 与悲观的 Arctan、Algebraic Root），既可单独使用，也可组合构建需求区间（见 Figure 5）。
- **多轮迭代（$T=5$）**：单轮估计（$T=1$）无法可靠满足目标——乐观函数导致低估（比率 $<1$），悲观函数导致严重高估（如 Arctan 在 ImageNet 上首轮即估计需 450 万张图像，而实际仅需 90 万张）。多轮迭代通过逐步修正回归曲线，将收集数据量与最小需求的比率控制在 1–2 倍以内（见 Figure 3、Figure 4）。
- **校正因子 $\tau$**：通过在目标 $V^*$ 上增加一个正的偏移量 $\tau$，抑制乐观回归函数的低估倾向。$\tau$ 需在保留任务（如 CIFAR10）上调参确定，再迁移至目标任务。



### 问题形式化：数据收集问题

给定初始已标注数据集 $\mathcal{D}_0$（规模 $n_0$）、一个固定的模型 $f$、一个固定的数据采样策略 $p(z)$，以及一个目标性能 $V^*$，目标是在最多 $T$ 轮迭代内，确定需要额外收集的最小数据量 $\hat{n}$，使得模型在扩充后的数据集 $\mathcal{D}_0 \cup \hat{\mathcal{D}}$ 上的得分 $V_f(\mathcal{D}_0 \cup \hat{\mathcal{D}}) \geq V^*$。

每轮迭代包含四个步骤（见 Algorithm 1 及 Figure 2）：
1. **回归数据集构建**：从 $\mathcal{D}_0$ 中采样 $r$ 个大小线性增长的嵌套子集 $S_0 \subset S_1 \subset \dots \subset S_{r-1}$，其中 $|S_i| = |\mathcal{D}_0| (i+1)/r$（通常 $r \leq 10$ 以控制计算开销）。在每个子集上训练模型并评估得分，形成回归数据集 $\mathcal{R} = \{(|S_i|, V_f(S_i))\}_{i=0}^{r-1}$。
2. **回归模型拟合**：使用加权最小二乘法，将选定的回归函数 $\hat{v}(n; \pmb{\theta})$ 拟合到 $\mathcal{R}$ 上，得到参数估计 $\pmb{\theta}^*$。
3. **数据需求估计**：求解满足 $\hat{v}(n_0 + \hat{n}; \pmb{\theta}^*) \geq V^* + \tau$ 的最小 $\hat{n}$，其中 $\tau$ 为校正因子（详见 Section 5.1）。
4. **数据收集与评估**：按策略 $p(z)$ 采样 $\hat{n}$ 个新样本，扩充数据集，重新训练模型并评估真实得分，将新数据点加入 $\mathcal{R}$ 后进入下一轮。

### 回归函数族

基于模型得分随数据量呈凹单调递增的经验观察，论文考察了四种参数化回归函数，所有函数共享可学习参数集 $\pmb{\theta} := \{\theta_1, \theta_2, \theta_3\}$（Table 1）：

**幂律函数（Power Law）**：
$$\hat{v}(n;\theta_1,\theta_2,\theta_3) = \theta_1 n^{\theta_2} + \theta_3$$
这是神经缩放律中最经典的形式，无上界，通常给出乐观估计（倾向于低估数据需求）。

**反正切函数（Arctan）**：
$$\hat{v}(n;\theta_1,\theta_2,\theta_3) = \frac{200}{\pi} \arctan\left(\theta_1 \frac{\pi}{2} n + \theta_2\right) + \theta_3$$
有界、单调递增，趋于有限值，通常给出悲观估计（倾向于高估数据需求）。在 ImageNet 上取得最低外推 RMSE（3.19，Table 3），但用于数据需求估计时会导致首轮即收集约 450 万张图像，远超实际所需的 90 万张。

**对数函数（Logarithmic）**：
$$\hat{v}(n;\theta_1,\theta_2,\theta_3) = \theta_1 \log(n + \theta_2) + \theta_3$$
无上界但增长速度渐缓，通常为乐观估计。

**代数根函数（Algebraic Root）**：
$$\hat{v}(n;\theta_1,\theta_2,\theta_3) = \frac{\theta_1 n}{(1 + |\theta_1 n|^{\theta_2})^{1/\theta_2}} + \theta_3$$
有界，增长速度介于幂律与反正切之间，性质居中。

### 校正因子 $\tau$ 机制

直接求解 $\hat{v}(n_0 + \hat{n}; \pmb{\theta}^*) \geq V^*$ 对拟合误差极度敏感——即使外推 RMSE 仅 1-6%，估计的数据需求量也可能偏离 12 万到 31 万张图像（Figure 1）。为此，论文引入校正因子 $\tau$，将约束修改为：
$$\hat{v}(n_0 + \hat{n}; \pmb{\theta}^*) \geq V^* + \tau$$
$\tau$ 的作用是提高目标值，迫使乐观回归函数（如 Power Law、Logarithmic）给出更保守的估计，从而避免因低估导致无法达到目标性能。$\tau$ 的值在一个保留任务（CIFAR10）上调参确定，随后迁移至其他任务。

### 多轮迭代与区间估计

在 $T=5$ 轮收集框架下，每轮重新拟合回归函数并更新 $\hat{n}$，逐步修正估计偏差。综合多个回归函数（乐观与悲观）的估计值，可以构建数据需求的上下界区间。当仅允许单轮收集（$T=1$）时，取所有回归函数估计值的最大值和最小值，能在图像分类任务上以超过 80% 的频率上下界真实数据需求 $n^*$（Figure 5）。

### 核心评估指标

数据收集效率的核心指标为实际收集数据量与最小需求量的比值：
$$\frac{n_0 + \hat{n}}{n_0 + n^*}$$
其中 $n^*$ 是满足真实得分曲线 $v(n_0 + n^*) = V^*$ 的最小数据量。比值 $<1$ 表示低估（未达目标），$>1$ 表示高估（收集了多余数据）。理想情况下比值应接近 1 且不小于 1。



## 实验与关键发现

### 1. 实验设置与评估协议

本文在 **Table 2** 所列的六个视觉基准上评估数据需求估计框架：图像分类（CIFAR10、CIFAR100、ImageNet）、2D 检测（VOC）、3D 检测与 BEV 分割（nuScenes）以及语义分割（BDD100K）。所有实验模拟数据收集流程：从完整训练集中随机采样初始子集 $\mathcal{D}_0$（默认 $n_0 = 10\%$，VOC 为 $20\%$），然后按 **Algorithm 1** 迭代估计所需额外数据量 $\hat{n}$、采样、评估并更新回归集，最多进行 $T$ 轮。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/004_Table_2.jpg]]
*Table 2: Data sets, tasks, and score functions considered*

为解耦采样随机性，模拟中不实际重新训练模型，而是通过预计算的 **ground truth 性能曲线** $v(n)$ 查询对应数据量下的模型得分（Section 4.2）。核心评估指标为**数据收集比** $(n_0 + \hat{n}) / (n_0 + n^*)$，其中 $n^*$ 是使 $v(n_0 + n^*) = V^*$ 的最小数据量。比值 $< 1$ 表示低估需求（未达标），$> 1$ 表示高估（过度收集），理想值为 $1$。

回归阶段使用加权最小二乘法拟合四种凹单调递增函数（**Table 1**）：Power Law、Arctan、Logarithmic 和 Algebraic Root。回归集 $\mathcal{R}$ 由 $r \le 10$ 个线性增长的嵌套子集构成（Section 4.1），以保持低成本。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/003_Table_1.jpg]]
*Table 1: Four concave monotonic increasing regression functions explored in this paper. The set of learnable parameters is $\pmb { \theta }$ : = $\{ \theta _ { 1 } , \theta _ { 2 } , \theta _ { 3 } \}$

---

### 2. 核心发现：外推精度 ≠ 数据需求估计可靠性

**Table 3** 报告了各回归函数在不同数据比例下的外推 RMSE。一个关键的反直觉发现是：**最低的 RMSE 并不转化为最可靠的数据需求估计**。在 ImageNet 上，Arctan 函数以 $3.19 \pm 2.1$ 的 RMSE 取得最佳拟合（$n_0 = 10\%$），但如 **Figure 3** 所示，使用 Arctan 进行单轮估计会导致首轮即收集约 450 万张图像——远超实际所需的约 90 万张（$n^*$ 对应 67% 验证精度）。

这一悖论的根源在于 **Figure 1** 揭示的敏感性问题：四条外推曲线在 50% 数据量（60 万张）上拟合时，精度误差仅 1-6%，但估计所需数据量却偏离 12 万到 31 万张。这说明即使外推曲线整体贴近 ground truth，在目标阈值 $V^*$ 附近的微小偏差也会被反函数求解放大为巨大的数据量误估。


---

### 3. 多轮收集与校正因子的效果

**Figure 3** 展示了 $T = 1, 3, 5$ 轮收集下各回归函数的数据收集比。单轮（$T=1$）时，Power Law 和 Logarithmic 作为乐观估计函数频繁低估需求（比值 $< 1$），而 Arctan 严重高估。随着轮数增加至 $T=5$，乐观函数通过迭代修正逐步逼近真实需求，但仍有部分目标值下出现低估。

为解决乐观函数的低估问题，引入**校正因子 $\tau$**（Section 5.1），将估计约束从 $\hat{v}(n_0 + \hat{n}) \ge V^*$ 修正为 $\hat{v}(n_0 + \hat{n}) \ge V^* + \tau$。**Figure 4** 显示，在 CIFAR10 上调参得到的 $\tau$ 配合 $T=5$ 轮收集，使 Power Law、Logarithmic 和 Algebraic Root 在 CIFAR10、CIFAR100 和 ImageNet 上的数据收集比控制在 $1.03$ 至 $2.5$ 之间，**Table 4** 进一步确认这一结果在多数数据集上成立。这意味着框架能以不超过最小需求约 2 倍的数据量稳定达标，消除了单轮 Power Law 的严重低估风险。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/009_Figure_4.jpg]]
*Figure 4: For T = 5 , , the ratio of the amount of data collected versus the minimum data needed to meet different target V ^ { * } when using regression functions with correction factors fitted using CIFAR10*

---

### 4. 多函数联合估计的边界能力

当仅允许单轮收集（$T=1$）时，**Figure 5** 探索了利用四种回归函数的估计差异构建区间的策略。在图像分类任务上，取所有函数的最大估计值作为上界、最小估计值作为下界，**超过 80% 的实例中该区间成功包含真实需求 $n^*$**。这一发现为资源极度受限（无法多轮迭代）的场景提供了实用的替代方案：通过综合乐观函数（Power Law、Logarithmic）和悲观函数（Arctan）的估计，可以获得对真实数据需求的有效边界。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/010_Figure_5.jpg]]
*Figure 5: (Top row) For T = 1 and varying $n _ { 0 }$ . , the frequency of instances where the largest and smallest nˆ estimated by the different functions upper and lower bound the true $n ^ { * }$ . (Bottom row) The largest and smallest ratios ( $n _ { 0 } + \hat { n }$ ) / ( $n _ { 0 } + n ^ { * }$ ) estimated by the different functions. The dashed black line corresponds to ratio 1*

---

### 5. 消融研究

#### 5.1 回归函数在不同架构上的表现

**Figure 7** 与 **Table 6** 考察了 CIFAR100 上不同 backbone（ResNet18/50/101、WideResNet）的影响。Arctan 在所有架构上一致地取得最低 RMSE，但始终是最悲观的估计器，导致显著高估数据需求。Power Law 和 Logarithmic 在不同架构间表现相对稳定，Algebraic Root 居中。这表明回归函数的相对悲观/乐观特性对架构选择具有鲁棒性。

#### 5.2 主动学习策略下的泛化

**Figure 9** 在 CIFAR100 上测试了三种主动学习策略（k-Centers、Least Confidence、Max Entropy）配合 $n_0 = 20\%$、$T=5$ 的设置。所有四种回归函数的数据收集比均落在 $0.8$ 至 $1.1$ 之间，表明框架在非随机采样下仍能有效工作。Arctan 保持最悲观估计，但多轮迭代有效抑制了过度收集。

#### 5.3 类别级指标的挑战

**Figure 8** 将框架应用于 nuScenes 的类别级 AP 估计（使用 CIFAR10 调参的 $\tau$，$T=5$）。Power Law、Logarithmic 和 Algebraic Root 对大多数类别实现了 $1$ 到 $3$ 的数据收集比，但 **bicycle** 和 **construction vehicle** 等罕见类别仍具挑战性——其性能曲线可能不满足凹单调假设，导致拟合偏差和估计不稳定。

---

### 6. 失败模式与边界条件

1. **凹单调假设的违背**：VOC 和 BDD100K 上的部分回归曲线（**Figure 6**）显示性能增长并非严格凹形，导致 Algebraic Root 和 Arctan 的拟合偏差增大。这是方法的一个结构性局限——当基础任务的学习曲线形态偏离假设族时，估计质量会退化。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/012_Figure_6.jpg]]
*Figure 6: Regression plots showing mean±standard deviation of multiple runs extrapolating performance in each task when trained on small subsets of the data. The solid blue line in each plot represents the ground truth performance*

2. **校正因子的迁移敏感性**：$\tau$ 在 CIFAR10 上调参后直接应用于 nuScenes 等异构任务（分类 → 检测/分割），虽然多数类别有效，但缺乏任务自适应的 $\tau$ 选择机制（见 **Open Questions**）。

3. **Ground truth 模拟的局限性**：实验中使用预计算的 $v(n)$ 替代实际重训练，虽然消除了训练方差，但可能低估了真实场景中重复训练引入的额外不确定性。

4. **Arctan 的 RMSE-需求悖论**：如 **Table 3** 与 **Figure 3/7** 反复验证，Arctan 在拟合精度上常优于 Power Law，但其有界饱和特性导致在目标值接近渐近线时估计的数据量呈指数级膨胀。**在选择回归函数时，预测不确定性在目标阈值附近的局部行为比全局 RMSE 更关键**。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/006_Table_3.jpg]]
*Table 3: tions achieve a ratio approximately equal to 1. Although Table 3 showed that Arctan achieved the lowest RMSE (3.19) of all functions in regression, using it to estimate data requirements would lead to an unnecessarily expensive data collection procedure. This reveals that simply analyzing regression error is insufficient when determining good data collection policies, necessitating our simulation approach*

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/007_Figure_3.jpg]]
*Figure 3: The ratio of the amount of data collected versus the minimum data needed (y-axis) for different target $V ^ { * }$ \ ( $\mathrm { x - a x i s }$ ) in simulations initializing with $n _ { 0 }$ = 1 0 \% of the data set ( $n _ { 0 }$ = 2 0 \% for VOC). For each data set, we show simulations for T = 1 , 3 , 5 maximum rounds. The dashed black line corresponds to collecting the least amount of data needed to reach $V ^ { * }$*

---

### 7. 关键图表索引

- **Table 1**：四种回归函数族及其可学习参数 $\pmb{\theta} = \{\theta_1, \theta_2, \theta_3\}$。
- **Table 2**：数据集、任务类型与评分函数汇总。
- **Table 3**：各回归函数在不同 $n_0$ 比例下的外推 RMSE（均值±标准差）。
- **Figure 1**：ImageNet 上从 10% 和 50% 数据外推的对比——外推精度与数据需求估计误差的分离。
- **Figure 3**：$T=1,3,5$ 轮下各回归函数的数据收集比随 $V^*$ 变化曲线。
- **Figure 4**：引入校正因子 $\tau$ 后（$T=5$）的数据收集比。
- **Figure 5**：单轮设置下多函数联合估计对真实需求的边界能力。
- **Figure 7**：不同 backbone 架构下的数据需求比（CIFAR100）。
- **Figure 8**：nuScenes 类别级 AP 的回归曲线与数据需求比。
- **Figure 9**：主动学习策略下的回归曲线与数据需求比（CIFAR100）。

![[assets/figures/papers/paper_list_l49_https_arxiv_org_abs_2207_01725/figures/016_Figure_9.jpg]]
*Figure 9: Experiments evaluating three different active learning strategies on CIFAR100 with n0 = 20% of the data set and T = 5 rounds. (Left) regression plots showing mean±standard deviation extrapolating performance. (Right) The ratio of data collected versus the minimum data needed (y-axis) for different target V ^ { * } (x-axis) in simulations*







## 定位与知识库关联

### 1. 与基线方法的本质区别

本工作提出的**带校正因子的多轮数据需求估计框架**，与标准单轮幂律外推方法存在三个根本性差异：

**回归函数族扩展**：基线方法仅依赖单一幂律函数（Power Law）进行性能外推，而本框架同时引入 Arctan、Logarithmic、Algebraic Root 共四类凹单调递增回归函数。其中 Power Law 和 Logarithmic 为无界函数（乐观估计），Arctan 和 Algebraic Root 为有界函数（悲观估计），四者联合可构建需求区间。

**收集轮次从单轮到多轮迭代**：基线方法在初始数据上一次性估计所需数据量并全量收集，本框架采用最多 T=5 轮迭代——每轮重新拟合回归函数、修正估计、增量收集，显著降低单次外推误差的累积影响。

**目标值校正机制**：基线方法直接求解 $\hat{v}(n_0 + \hat{n}; \pmb{\theta}^*) \ge V^*$ 的最小 $\hat{n}$，对拟合误差极度敏感。本框架引入校正因子 $\tau$，将约束改为 $\hat{v}(n_0 + \hat{n}; \pmb{\theta}^*) \ge V^* + \tau$，通过提高目标值对冲乐观估计导致的低估风险。$\tau$ 在留出任务（CIFAR10）上调参确定。

### 2. 适用边界

**有效场景**：
- 模型性能随数据量呈凹单调递增趋势的任务，如图像分类（CIFAR10/100、ImageNet）、2D 检测（VOC）、3D 检测（nuScenes）、BEV 分割（nuScenes）、语义分割（BDD100K）。
- 随机采样策略下的数据收集。
- 模型架构和训练超参数在整个收集过程中保持固定。

**弱效或失效场景**：
- 性能曲线不满足凹性或单调性的任务（如 nuScenes 中个别类别 AP 随数据量增加出现波动）。
- 模型架构或训练配置在收集过程中发生变更（如从 ResNet 切换到更强 backbone）。
- 校正因子 $\tau$ 从 CIFAR10 调参获得，当目标任务特性与 CIFAR10 差异过大时可能不够鲁棒。

### 3. 局限与开放问题

**已明确的局限**：
1. 假设模型 $f$ 和数据采样策略 $p(z)$ 在整个收集过程中不变，未考虑模型更新或超参数调整的影响。
2. 回归函数的凹单调假设在 VOC、BDD100K 等任务上不完全成立，可能导致拟合偏差。
3. 实验模拟中以 ground truth $v(n)$ 代替实际重新训练，可能忽略了重复训练引入的额外方差。
4. 仅针对随机采样评估；在主动学习场景中虽趋势一致，但未针对 budget 分配进行深入优化。

**待解决的开放问题**：
1. 能否在不依赖留出调参任务（如 CIFAR10）的情况下，自动为每个数据集选择最优回归函数和 $\tau$？
2. 校正因子 $\tau$ 对不同任务类型（检测 vs. 分割）的泛化能力如何？是否存在统一的 $\tau$ 设置或自适应调整策略？
3. 当数据采集过程中模型更新时，数据需求估计应如何动态调整？
4. 如何利用类别级或样本级指标优化每轮采样策略 $p(z)$，以在更少数据量下满足全局目标？
5. 对于不满足凹单调特性的任务，是否有更灵活的回归模型（如非参数方法）能够可靠拟合性能曲线？



## 原文 PDF

![[paperPDFs/CVPR_2022/How_Much_More_Data_Do_I_Need_Estimating_Requirements_for_Downstream_Tasks.pdf]]

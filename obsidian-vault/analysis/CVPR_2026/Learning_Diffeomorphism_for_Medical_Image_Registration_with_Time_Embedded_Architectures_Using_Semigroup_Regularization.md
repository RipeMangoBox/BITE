---
title: Learning Diffeomorphism for Medical Image Registration with Time-Embedded Architectures Using Semigroup Regularization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Diffeomorphism_for_Medical_Image_Registration_with_Time_Embedded_Architectures_Using_Semigroup_Regularization.pdf
project_link: null
code_link: null
aliases:
- SSDIR
- LDMIRTEAUSR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 半群正则化强度 λ：λ=10⁵ 时强制严格微分同胚流，λ=10⁴ 或更小时允许非微分同胚形变。
primary_logic: 仅用部分半群约束（L_sg）即足以迫使网络学习一个常微分方程（ODE）的流；该 ODE 流内生地保证可逆性、循环一致性和拓扑保留，无需显式积分或任何辅助正则项。
claims:
- SGDIR 仅使用单个半群正则化并移除缩放-平方与所有辅助正则项，仍达到近完美的微分同胚。
- 部分半群约束在数学上足以保证网络学习的是一个 ODE 流。
- λ=10⁵ 的 SGDIR DiT 在 OASIS 和 AbdomenCTCT 上实现 0.0% 负雅可比体素，并在 Dice/HD95 上超越现有微分同胚方法。
- OASIS (atlas-based) 上 Dice↑ = 86.53 ± 0.82 (SGDIR DiT λ=10⁵)
---

# Learning Diffeomorphism for Medical Image Registration with Time-Embedded Architectures Using Semigroup Regularization

> [!tip] 核心洞察
> 仅用部分半群约束（L_sg）即足以迫使网络学习一个常微分方程（ODE）的流；该 ODE 流内生地保证可逆性、循环一致性和拓扑保留，无需显式积分或任何辅助正则项。

| 字段 | 内容 |
|------|------|
| 中文题名 | 使用半群正则化的时间嵌入架构学习医学图像配准的微分同胚 |
| 英文题名 | Learning Diffeomorphism for Medical Image Registration with Time-Embedded Architectures Using Semigroup Regularization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Matinkia_Learning_Diffeomorphism_for_Medical_Image_Registration_with_Time-Embedded_Architectures_Using_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SGDIR (Semigroup Diffeomorphic Image Registration) |
| Dataset | OASIS, AbdomenCTCT, LungCT |

> [!tip] 效果简介
> - OASIS (atlas-based) 上，Dice↑ 86.53 ± 0.82 (SGDIR DiT λ=10⁵) vs 84.63 ± 1.12 (TransMorph-diff) (+1.90)；|J|<0%↓ 0.0 ± 0.0 (SGDIR DiT λ=10⁵) vs 0.0022 ± 0.0019 (GradICON) (−0.0022 pp)。
> - AbdomenCTCT 上，Dice↑ ~81.4 (SGDIR DiT λ=10⁴, from Table 3) vs ~76.5 (best competitor, see Table 3) (+~4.9 pp)；|J|<0%↓ 0.0 ± 0.0 (SGDIR UNet λ=10⁵) vs 0.043 ± 0.015 (TransMorph-diff, from Table 3) (−0.043 pp)。
> - LungCT (TRE) 上，TRE↓ 2.23 ± 0.14 (SGDIR UNet λ=10⁴) vs 2.50 ± 0.18 (best competing deformable, from Table 4) (−0.27 mm)。

## 概述

医学图像配准的核心挑战在于，如何在保证变形场拓扑结构的前提下，实现高精度的解剖对齐。现有基于学习的微分同胚方法普遍依赖**缩放-平方（scaling-and-squaring）积分方案**与多种**辅助正则项**（如雅可比行列式惩罚、平滑约束、逆一致性损失）来维持拓扑保持性。这些显式约束与离散积分近似不仅增加了训练复杂度，还限制了模型的泛化能力和推理效率。

本文提出 **SGDIR（Semigroup Diffeomorphic Image Registration）**，一种连续时间配准框架。其核心洞见在于：**仅需施加一个部分半群约束（partial semigroup constraint），即可在数学上迫使网络学习一个常微分方程（ODE）的流**，从而内生地保证变形的可逆性、循环一致性以及拓扑保持——完全无需显式积分方案或任何辅助正则项。这一发现将微分同胚配准从“积分+多重约束”的范式简化为“单一半群正则化”的范式。

**方法定位**：SGDIR 采用时间嵌入骨干网络（Temporal UNet 或 Diffusion Transformer），直接参数化连续时间变形场 $\phi_t(x;\theta) = x + t\mathbf{F}(x, t; I_f, I_m, \theta)$，可在任意时刻 $t \in [-1, 1]$ 瞬时查询变形。训练时通过均匀采样时间 $t$ 和图像对，联合优化连续时间相似性损失 $\mathcal{L}_{\mathrm{sim}}^t$ 与半群正则化 $\mathcal{L}_{\mathrm{sg}}^t$。正则化强度 $\lambda$ 作为核心控制旋钮：$\lambda=10^5$ 时强制严格的微分同胚流，$\lambda$ 降低时则允许非微分同胚的灵活形变。

**主要结果**：在 8 个涵盖 2D/3D、MR/CT 的公开医学影像基准上，SGDIR 取得了显著提升：
- **OASIS 脑图谱配准**：SGDIR DiT（$\lambda=10^5$）达到 Dice 86.53%，负雅可比体素比例 $|J|<0$ 为 **0.0%**，在拓扑保持性上超越所有现有微分同胚方法。
- **AbdomenCTCT 腹部配准**：SGDIR 在 Dice 上领先最佳竞争方法约 4.9 个百分点，$\lambda=10^5$ 时 $|J|<0$ 同样为 0.0%。
- **计算效率**：SGDIR DiT 推理速度约 0.22s，接近非微分同胚方法 HViT（0.51s）的一半，内存占用也显著低于基于积分的微分同胚方法。

这些结果表明，通过时间一致性的内在约束替代显式拓扑正则化，SGDIR 在精度、拓扑保证和计算效率三个维度上同时实现了突破。

## 背景与动机

医学图像配准的核心任务是为图像对建立空间对应关系，其输出通常是一个变形场 $\phi$。在临床应用中，变形场不仅需要高精度的解剖对齐，还必须满足**拓扑保持**——即形变应当是平滑、可逆且无折叠的。数学上，这类理想形变由**微分同胚**（diffeomorphism）来刻画：一个光滑、可逆且逆映射同样光滑的映射。违反拓扑保持会导致网格折叠（表现为雅可比行列式 $|J| < 0$），这在手术导航、脑图谱映射等场景中是不可接受的。

### 现有微分同胚方法的瓶颈

当前主流的学习型微分同胚配准方法，如 **TransMorph-diff**（Chen et al., MedIA 2022）、**GradICON**（Tian et al., CVPR 2023）和 **CycleMorph**（Kim et al., MedIA 2021），几乎都依赖以下两个核心机制的组合：

1. **缩放-平方积分方案（Scaling-and-Squaring）**：通过离散化常微分方程（ODE）$\frac{d\phi_t}{dt} = \mathbf{v}(\phi_t)$，将预测的速度场 $\mathbf{v}$ 经 $N$ 步递推合成最终变形场 $\phi_1$。具体地，先以小步长近似 $\phi_{1/2^N}(x) = x + \frac{\mathbf{v}(x)}{2^N}$，再通过 $\phi_{1/2^{N-1}} = \phi_{1/2^N} \circ \phi_{1/2^N}$ 递推至 $\phi_1$。这一显式积分过程不仅引入离散化误差，还显著增加了计算开销。

2. **多种辅助正则项**：为保障拓扑结构不被破坏，现有方法通常叠加雅可比行列式惩罚、平滑约束（如弯曲能量）、逆一致性损失等多项正则项。这些约束各自针对拓扑保持的某个侧面，但彼此之间缺乏统一的理论框架，导致超参数调优复杂，且不同正则项之间可能相互冲突，限制了训练效率和泛化能力。

此外，现有方法几乎都**仅预测 $t=1$ 时刻的最终变形场**，无法直接查询中间时刻的连续形变路径。这在需要时间序列形变分析的应用中构成明显短板。

### 核心动机：从显式约束到内生结构

上述瓶颈的根源在于：现有方法将微分同胚视为一种需要**外部施加**的约束集合，而非网络结构的**内生属性**。本文的核心洞察是：若能让网络直接学习一个 ODE 流，则可逆性、循环一致性和拓扑保持将自然成立，无需任何显式积分或辅助正则项。

ODE 流由半群性质（semigroup property）完全刻画：
$$\phi_0 = \mathrm{Id}, \qquad \phi_t \circ \phi_s = \phi_{t+s}, \quad \forall t,s$$

这一性质同时蕴含了逆一致性 $\phi_t^{-1} = \phi_{-t}$ 和循环一致性。然而，直接在整个时间域上强制完整的半群约束在计算上不可行。本文的关键问题是：**能否仅施加一个更弱的“部分半群约束”，就足以保证网络学习到 ODE 流？**

### 本文动机与目标

受上述问题驱动，本文提出 **SGDIR（Semigroup Diffeomorphic Image Registration）**，旨在实现以下目标：

- **消除显式积分方案**：通过时间嵌入架构直接输出任意 $t \in [-1,1]$ 时刻的连续变形场，无需缩放-平方递推。
- **仅用单一正则项保证微分同胚**：用部分半群正则化 $\mathcal{L}_{\mathrm{sg}}$ 替代所有辅助约束，并数学证明该弱条件足以诱导 ODE 流。
- **统一微分同胚与非微分同胚配准**：通过单一超参数 $\lambda$ 控制正则化强度，$\lambda=10^5$ 时强制严格微分同胚流，$\lambda=10^4$ 或更小时允许非微分同胚形变，从而在同一框架下兼顾拓扑保持与形变灵活性。

## 核心创新

### 问题瓶颈：显式积分与多重正则项的代价

现有学习型微分同胚配准方法（如 **TransMorph-diff** (Chen et al., MedIA 2022)、**GradICON** (Tian et al., CVPR 2023)、**CycleMorph** (Kim et al., MedIA 2021)）普遍依赖两条技术路径来保证拓扑保持：一是通过缩放-平方（scaling-and-squaring）积分方案从速度场重建变形场，二是引入多种辅助正则项——包括雅可比行列式惩罚、平滑约束、逆一致性损失等。这些显式约束与离散积分步骤带来了三重代价：（1）训练效率受限于积分迭代次数；（2）正则项之间的权重调谐复杂，泛化性受限；（3）推理时仍需执行完整积分链，增加了计算开销。本质上，现有方法将微分同胚视为需要外部强制的外生属性，而非网络结构内生的数学性质。

### 核心洞察：部分半群约束足以诱导 ODE 流

SGDIR 的核心洞察在于一个数学命题：**仅对变形场施加部分半群约束，即足以迫使网络学习一个常微分方程（ODE）的流**。具体而言，若变形族 $\phi_t$ 满足以下条件：

$$\phi_{2t-1} = \phi_t \circ \phi_{t-1}, \quad \phi_{2t-1} = \phi_{t-1} \circ \phi_t$$

则该变形族必然是指数映射（单参数微分同胚），即存在一个平稳速度场 $\mathbf{v}$ 使得 $\frac{d\phi_t}{dt} = \mathbf{v}(\phi_t)$。这一 ODE 流内生地保证了三项关键性质：**可逆性**（$\phi_t^{-1} = \phi_{-t}$）、**循环一致性**（$\phi_t \circ \phi_s = \phi_{t+s}$）以及**拓扑保持**（雅可比行列式恒正）。与现有方法将微分同胚视为需要外部强加的目标不同，SGDIR 通过半群正则化将微分同胚转化为网络学习的自然涌现属性。

### Changed Slots：三个维度的关键创新

**Slot 1：正则化策略——从“多重约束”到“单一半群正则”**

现有方法的正则化策略是“缩放-平方积分 + 多种正则项”的组合方案。以 GradICON 为例，其损失函数包含逆一致性损失和雅可比惩罚；TransMorph-diff 则依赖缩放-平方积分与平滑正则项。SGDIR 彻底移除了缩放-平方积分和所有辅助正则项，仅保留单个部分半群正则项 $\mathcal{L}_{\mathrm{sg}}^t$：

$$\mathcal{L}_{\mathrm{sg}}^t = \|\phi_{2t-1} - \phi_t \circ \phi_{t-1}\|_2 + \|\phi_{2t-1} - \phi_{t-1} \circ \phi_t\|_2$$

该正则项强制变形场在特定时间对之间满足半群关系，其数学强度由单一超参数 $\lambda$ 控制：$\lambda = 10^5$ 时强制严格微分同胚流，$\lambda = 10^4$ 或更小时允许非微分同胚形变以适应大变形场景。这一设计将正则化策略从“多目标加权平衡”简化为“单参数连续调节”，显著降低了调参复杂度。

**Slot 2：时间建模——从“离散重建”到“连续时间嵌入”**

现有方法通常仅预测 $t=1$ 时刻的变形场，或通过缩放-平方从速度场离散重建中间时刻的变形。SGDIR 引入时间嵌入架构，将时间 $t$ 作为条件输入直接注入骨干网络（Temporal UNet 或 Diffusion Transformer），使得变形场参数化为：

$$\phi_t(x; \theta) = x + t \,\mathbf{F}(x, t; I_f, I_m, \theta)$$

其中 $\mathbf{F}$ 是时间嵌入网络输出的速度场。这一参数化使得变形场在连续时间轴 $t \in [-1, 1]$ 上任意时刻可查询，无需迭代采样。正向变形（$t=1$）和逆向变形（$t=-1$）由同一网络统一建模，从根本上保证了双向配准的一致性。

**Slot 3：变形参数化——从“位移叠加”到“时间缩放速度场”**

传统变形参数化 $\phi(x) = x + u(x)$ 将变形视为固定位移场的叠加，缺乏对变形路径的显式建模。SGDIR 的变形参数化通过时间因子 $t$ 缩放速度场 $\mathbf{F}$，使得变形幅度与时间线性相关。这一设计的深层含义在于：当半群约束满足时，$\mathbf{F}$ 恰好逼近平稳 ODE 的速度场 $\mathbf{v}$，变形路径成为该速度场下的积分曲线。因此，SGDIR 的变形参数化不仅是一种计算上的便利，更是半群正则化得以生效的架构前提。

### 创新验证：消融实验的关键证据

半群正则化的核心作用在消融实验中得到直接验证：当 $\lambda$ 从 $10^5$ 降至 $0$ 时，OASIS 数据集上的负雅可比体素比例从 0.0% 单调上升至 1.3%，同时 Dice 从 85.90 降至 79.80（Table 6）。这证明半群正则化是拓扑保持的唯一控制因素，而非其他隐式正则效应的副产品。此外，连续时间采样训练优于离散时间采样（Figure 8），验证了时间嵌入架构与半群约束的协同效应——连续时间采样使网络在更多时间点上接受半群约束，从而更充分地学习 ODE 流结构。

值得注意的是，$\lambda = 10^5$ 的 SGDIR 在整个时间轴上保持 $|J|<0\% = 0\%$，而 $\lambda = 10^4$ 的版本仅在 $t \to 1$ 时出现少量折叠（Figure 7），表明半群正则化强度与拓扑保持程度之间存在精确的单调关系，这为实际部署中的参数选择提供了清晰的指导原则。

## 整体框架

SGDIR 的整体设计围绕一个核心思想展开：**仅用一个部分半群约束，无需显式积分方案或任何辅助正则项，即可迫使网络学习一个常微分方程（ODE）的流**，从而内生地保证变形的可逆性、循环一致性与拓扑保持。整个框架由三个关键模块构成，分别对应架构设计、训练流程与推理流程（Figure 2）。

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/002_Figure_2.jpg]]
*Figure 2: Architectures of SGDIR (left), Training scheme (middle) and inference scheme (right) of SGDIR. DiT blocks are implemented according to [37]. More details on the architecture can be found in the supplementary materials (Sec. 9)*

### 时间嵌入变形参数化

SGDIR 的目标是学习一个时间连续的变形场 $\phi_t: \Omega \to \mathbb{R}^3$，其中 $t \in [-1, 1]$，$\phi_0(x) = x$。变形场的参数化形式为：

$$\phi_t(x; \theta) = \phi(x, t; \theta) = x + t \mathbf{F}(x, t; I_f, I_m, \theta)$$

其中 $\mathbf{F}$ 是一个以时间为条件的时间嵌入网络，接收固定图像 $I_f$、移动图像 $I_m$ 和时间 $t$ 作为输入，输出速度场。这一参数化使得变形场在任意时刻 $t$ 都可即时查询，无需迭代采样或缩放-平方递推。

### 时间嵌入骨干网络

SGDIR 采用两种时间嵌入骨干架构（Figure 2 左）：
- **Temporal UNet**：在标准 UNet 的基础上引入时间条件编码，使特征提取过程感知时间变量。
- **Diffusion Transformer (DiT)**：基于 DiT 块构建，以时间嵌入为条件，提供更强的全局建模能力。

两种骨干网络均以图像对和时间 $t$ 为输入，输出速度场 $\mathbf{F}$，进而通过上述参数化生成对应时刻的变形场。

### 训练流程

训练流程（Figure 2 中）包含两个并行的损失函数：

1. **连续时间相似度损失** $\mathcal{L}_{\mathrm{sim}}^t$：强制正向与逆向变形在任意时刻 $t \in [0, 1]$ 对齐：
   $$\mathcal{L}_{\mathrm{sim}}^t = -\mathrm{NCC}(\phi_{t-1}[I_f], \phi_t[I_m])$$
   该损失使网络同时学习正向（$I_m \to I_f$）和逆向（$I_f \to I_m$）配准，实现双向配准能力。

2. **部分半群正则化** $\mathcal{L}_{\mathrm{sg}}^t$：仅对特定时间对施加半群约束：
   $$\mathcal{L}_{\mathrm{sg}}^t = \|\phi_{2t-1} - \phi_t \circ \phi_{t-1}\|_2 + \|\phi_{2t-1} - \phi_{t-1} \circ \phi_t\|_2$$
   该约束是 SGDIR 的核心创新——它仅要求变形场在 $t-1 \to t \to 2t-1$ 的路径上满足合成一致性，但理论证明（Theorem 1）这一较弱条件足以保证网络学到的变形场是一个 ODE 的流，从而内生地保证可逆性（$\phi_t^{-1} = \phi_{-t}$）和拓扑保持。

总训练目标通过均匀采样图像对和时间 $t$ 来优化：
$$\mathcal{L} = \mathbb{E}_{(I_f, I_m) \sim \mathcal{D}, t \sim \mathrm{Uni}(0,1)} \left[ \mathcal{L}_{\mathrm{sim}}^t + \lambda \mathcal{L}_{\mathrm{sg}}^t \right]$$

其中 $\lambda$ 是半群正则化强度，是控制框架行为的关键旋钮：$\lambda = 10^5$ 时强制严格的微分同胚流（|J|<0 为 0.0%），$\lambda = 10^4$ 或更小时允许非微分同胚的灵活形变。

### 推理流程

推理流程（Figure 2 右）极为简洁：给定训练好的时间嵌入网络，在目标时刻 $t$（通常为 $t=1$）直接前向传播一次，即可获得变形场 $\phi_1$，无需缩放-平方积分或任何迭代过程。这种单步推理的设计使得 SGDIR DiT 的推理时间仅约 0.22 秒，接近 HViT (0.51s) 的一半，内存占用也显著低于依赖多重积分的微分同胚方法（Table 7）。

### 与现有方法的根本差异

传统微分同胚配准方法依赖两条路径保证拓扑保持：**缩放-平方积分方案**（Eq. 2–3）将速度场逐步合成为最终变形，以及**多种辅助正则项**（雅可比惩罚、平滑约束、逆一致性损失等）。SGDIR 通过部分半群正则化将这两条路径一并消除——网络在训练中被迫满足流的合成一致性，从而在推理时天然输出满足 ODE 性质的变形场，无需任何显式积分或辅助约束。这是 SGDIR 在方法学上最根本的差异点。

## 核心模块与公式推导

### 问题形式化：连续时间变形场

SGDIR 寻求一个时间连续的变形场 $\phi_t: \Omega \rightarrow \mathbb{R}^3$，其中 $t \in [-1, 1]$ 且 $\phi_0(x) = x$，使得 $\phi_t$ 将移动图像 $I_m$ 向固定图像 $I_f$ 传输（正向），同时 $\phi_{-t}$ 实现逆过程。核心假设是 $\phi_t$ 为一个自主常微分方程（ODE）的流：

$$\frac{d\phi_t}{dt} = \mathbf{v}(\phi_t), \quad \phi_0(x) = x$$

其中 $\mathbf{v}$ 是未知的平稳速度场。该 ODE 流内生地满足**半群性质**：

$$\phi_0 = \mathrm{Id}, \qquad \phi_t \circ \phi_s = \phi_{t+s}, \quad \forall t, s$$

由半群性质可直接推导出**逆一致性恒等式** $\phi_t^{-1} = \phi_{-t}$，意味着逆变形无需额外计算或损失项即可自然获得。

### 核心模块一：时间嵌入变形参数化

传统方法仅预测 $t=1$ 时刻的位移场或通过缩放-平方从速度场重建离散时间变形。SGDIR 采用**时间嵌入网络**直接输出任意时刻的连续变形场：

$$\phi_t(x; \theta) = \phi(x, t; \theta) = x + t \mathbf{F}(x, t; I_f, I_m, \theta)$$

其中 $\mathbf{F}$ 是一个以时间 $t$ 为条件的神经网络（Temporal UNet 或 Diffusion Transformer），接受固定图像 $I_f$ 和移动图像 $I_m$ 作为输入，输出速度场。该参数化使得变形场在 $t \in [-1, 1]$ 的任意时刻可即时查询，无需迭代采样。

**时间嵌入骨干网络**（见 Figure 2）的核心设计是将时间 $t$ 作为条件注入特征提取过程。具体实现中，DiT 模块遵循 Peebles & Xie (2023) 的扩散 Transformer 设计，通过自适应层归一化将时间编码融入注意力计算。

### 核心模块二：连续时间相似性损失

为充分利用连续时间参数化的优势，SGDIR 在任意时刻 $t \in [0, 1]$ 强制正向与逆向变形对齐：

$$\mathcal{L}_{\mathrm{sim}}^t = -\mathrm{NCC}(\phi_{t-1}[I_f], \phi_t[I_m]), \quad \forall t \in [0, 1]$$

该损失使 $\phi_{t-1}$ 将固定图像向中间态变形，同时 $\phi_t$ 将移动图像向同一中间态变形，两者通过归一化互相关（NCC）比较。这一设计实现了**双向配准**，无需额外的逆一致性损失项。

### 核心模块三：部分半群正则化（关键创新）

SGDIR 的核心理论贡献是以**部分半群约束**替代传统方法中的缩放-平方积分与多种辅助正则项（雅可比惩罚、平滑约束、逆一致性损失等）。该约束仅施加于特定时间对：

$$\mathcal{L}_{\mathrm{sg}}^t = \|\phi_{2t-1} - \phi_t \circ \phi_{t-1}\|_2 + \|\phi_{2t-1} - \phi_{t-1} \circ \phi_t\|_2$$

该损失强制 $\phi_{2t-1} = \phi_t \circ \phi_{t-1}$ 和 $\phi_{2t-1} = \phi_{t-1} \circ \phi_t$，即变形满足指数映射条件（单参数微分同胚）。**定理 1** 证明：仅该弱条件即足以保证网络学习的是一个 ODE 流，从而内生地保证可逆性、循环一致性和拓扑保留。

**因果旋钮**：正则化强度 $\lambda$ 直接控制微分同胚的严格程度。$\lambda = 10^5$ 时强制严格微分同胚流，$\lambda = 10^4$ 或更小时允许非微分同胚形变。

### 联合训练目标

总损失通过对图像对和时间 $t$ 的均匀采样来优化：

$$\mathcal{L} = \mathbb{E}_{(I_f, I_m) \sim \mathcal{D}, t \sim \mathrm{Uni}(0, 1)} \left[\mathcal{L}_{\mathrm{sim}}^t + \lambda \mathcal{L}_{\mathrm{sg}}^t\right]$$

### 与传统方法的本质差异

| 设计维度 | 传统微分同胚方法 | SGDIR |
|---------|----------------|-------|
| 时间建模 | 仅预测 $t=1$ 变形场，或通过缩放-平方离散重建 | 时间嵌入网络直接输出任意 $t$ 的连续变形场 |
| 正则化策略 | 缩放-平方积分 + 雅可比惩罚 + 平滑约束 + 逆一致性损失 | 仅单个部分半群正则项 $\mathcal{L}_{\mathrm{sg}}^t$ |
| 可逆性保证 | 依赖显式积分方案和多种辅助约束 | 由半群约束诱导的 ODE 流内生保证 |
| 训练效率 | 需迭代积分步骤，计算开销大 | 单次前向传播，推理速度约 0.22s |

**证据强度说明**：定理 1 的数学证明在论文第 4 节给出，声称部分半群条件足以保证 ODE 流的学习；消融实验（Table 6）证实 $\lambda$ 从 $10^5$ 降至 0 时，$\vert J \vert < 0\%$ 从 0\% 逐渐上升至 1.3\%，Dice 从 85.90 降至 79.80，直接验证了半群正则化对拓扑保持的因果控制作用。

## 实验与分析

### 5.1 实验设置与基线方法

SGDIR 在 8 个涵盖 2D/3D、MR/CT 的公开数据集上评估，包括 OASIS（脑 MR 图谱配准与个体间配准）、IXI、Mindboggle101、LPBA40、CANDI（多站点脑 MR）、AbdomenCTCT（腹部 CT）、LungCT（肺部 CT）和 ACDC（心脏 MR）。评估指标涵盖分割重叠率（Dice）、Hausdorff 距离（HD95）、平均对称表面距离（ASSD）、结构相似性（SSIM）、目标配准误差（TRE）以及拓扑违反率（雅可比行列式负值体素百分比 |J|<0%）。

基线方法分为两类：微分同胚方法与可变形（非微分同胚）方法。微分同胚基线包括 **CycleMorph**（Kim et al., MedIA 2021，显式循环一致性约束）、**GradICON**（Tian et al., CVPR 2023，近似逆一致性）、**TransMorph-diff**（Chen et al., MedIA 2022，Transformer 骨干 + 缩放-平方积分）、**R2Net**（Joshi and Hong, MedIA 2023，Lipschitz 残差网络）和 **NODEO**（Wu et al., CVPR 2022，基于神经 ODE 的优化方法）。可变形基线包括 **TransMorph**、**TransMatch**（Jian et al., IEEE TMI 2023）、**HViT**（Ghahremani et al., CVPR 2024）、**CorrMLP**（Meng et al., CVPR 2024）和 **SACB-Net**（Cheng et al., CVPR 2025）。所有方法在相同数据集划分下严格比较，未发现不公正比较迹象。

SGDIR 评估四个变体：两个微分同胚模型（λ = 10⁵）使用时间嵌入 UNet 和 Diffusion Transformer（DiT）骨干，两个可变形对应模型（λ = 10⁴）使用相同架构（图 Figure 2）。

### 5.2 主要定量结果

**脑 MR 配准（OASIS 与多站点数据集）。** 在 OASIS 图谱配准任务上（表 Table 1），SGDIR DiT（λ = 10⁵）达到 Dice 86.53 ± 0.82，超越最佳微分同胚基线 TransMorph-diff 的 84.63 ± 1.12（+1.90 个百分点），同时实现 0.0% 的 |J|<0%（即完美拓扑保持），而 GradICON 的 |J|<0% 为 0.0022 ± 0.0019。在个体间配准任务上，SGDIR UNet（λ = 10⁴）达到 HD95 1.63 ± 0.33，为所有方法中最优。当放松半群约束至 λ = 10⁴ 时，SGDIR DiT 在 OASIS 上 Dice 进一步提升至 88.09 ± 0.91，HD95 降至 1.73 ± 0.41。

跨多个脑 MR 数据集（表 Table 2），SGDIR DiT（λ = 10⁵）在 IXI 上取得 Dice 80.18 ± 1.09，在 Mindboggle101 上取得 71.58 ± 1.12，均为参与比较方法中的最佳。在 IXI 和 LPBA40 上，SGDIR DiT（λ = 10⁵）保持 |J|<0% = 0.0 ± 0.0，证明完美的微分同胚性质。当 λ = 10⁴ 时，SGDIR DiT 在 OASIS 上 Dice 达到 83.88 ± 1.77（表 Table 2 上下文），在 ACDC 上达到 85.51 ± 0.96（表 Table 5）。

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/006_Table_2.jpg]]
*Table 2: Quantitative registration results across MRI brain datasets. For clarity, only Dice and topology violation rates*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/011_Table_5.jpg]]
*Table 5: Quantitative registration results on the ACDC dataset. The best result is shown in bold and the best competitor is presented in blue*

**腹部 CT 配准（AbdomenCTCT）。** 在 AbdomenCTCT 数据集上（表 Table 3），SGDIR DiT（λ = 10⁴）的 Dice 约 81.4，超越最佳竞争方法的约 76.5（+~4.9 个百分点）。SGDIR UNet（λ = 10⁵）实现 |J|<0% = 0.0 ± 0.0，而 TransMorph-diff 的 |J|<0% 为 0.043 ± 0.015。SGDIR UNet（λ = 10⁴）达到 HD95 9.19 ± 0.78，为所有方法中最优。可视化对比（图 Figure 4）显示 SGDIR 产生最平滑的形变网格，同时保持高 Dice 精度。

**肺部 CT 配准（LungCT）。** 在 LungCT 数据集上（表 Table 4），SGDIR UNet（λ = 10⁴）达到 TRE 2.23 ± 0.14 mm，优于最佳竞争可变形方法的 2.50 ± 0.18 mm（−0.27 mm）。

**心脏 MR 配准（ACDC）。** 在 ACDC 数据集上（表 Table 5），SGDIR DiT（λ = 10⁴）达到 Dice 85.51 ± 0.96，为所有方法中最高。分割掩膜叠加可视化（图 Figure 5）进一步验证了配准精度。

**综合性能概览。** 图 Figure 1 总结了 SGDIR 在微分同胚与非微分同胚设定下的表现：在微分同胚设定（λ = 10⁵）下，SGDIR 与顶级可变形模型性能相当；在非微分同胚设定（λ = 10⁴）下，SGDIR 超越所有基线方法。

### 5.3 消融实验

**半群正则化强度 λ 的影响。** 表 Table 6 展示了 λ 从 10⁵ 逐步降至 0 时在 OASIS 上的效果：|J|<0% 从 0.0% 单调上升至 1.3%，Dice 从 85.90 降至 79.80。这直接证明半群正则化是控制拓扑保持的核心因果旋钮——λ = 10⁵ 强制严格微分同胚流，而 λ = 10⁴ 或更小时允许非微分同胚形变以换取更高的配准精度。

**时间轴上的拓扑保持。** 图 Figure 7 显示 λ = 10⁵ 的 SGDIR 在整个时间轴 t ∈ [0, 1] 上保持 |J|<0% = 0%，而 λ = 10⁴ 的版本仅在 t → 1 时出现少量折叠。这验证了部分半群约束（L_sg）足以在整个连续时间流上诱导 ODE 流并保证可逆性。

**连续时间采样 vs 离散时间采样。** 图 Figure 8 表明，在 DiT 模型上（λ = 10⁵），使用连续时间采样训练优于离散时间采样，获得更高的 Dice 和更低的 |J|<0%。这支持了 SGDIR 时间嵌入架构的设计选择——从均匀分布 Uni(0, 1) 中采样 t 能够更好地利用连续时间流的表达能力。

**计算效率。** 表 Table 7 显示 SGDIR DiT 的推理速度约 0.22 秒，接近 HViT（0.51 秒）的一半，内存占用也为同级别的一半左右。SGDIR 消除了缩放-平方的迭代积分步骤，因此推理速度显著优于依赖积分的微分同胚方法（如 TransMorph-diff 需要 N 步递推合成）。

### 5.4 核心发现与失败模式

**核心发现。** SGDIR 仅使用单个部分半群正则项 L_sg（Eq. (10)），完全移除缩放-平方积分与所有辅助正则项（雅可比惩罚、平滑约束、逆一致性损失），仍达到近完美的微分同胚（|J|<0% = 0.0%）。定理 1 证明该部分半群约束足以保证网络学习的是一个 ODE 流，从而内生地保证可逆性、循环一致性和拓扑保留。λ 作为唯一的正则化强度参数，直接控制微分同胚流与可变形灵活性之间的权衡。

**失败模式与局限。** 部分半群约束仅在一个连续区间内施加，虽然在标准基准上理论保证成立，但在极端大变形情况下未进行专项验证。当前评估限于公开的标准医学影像配准基准，未在高度异质性或罕见病理数据上验证泛化性。λ 的调节目前为手动预设——不同数据集可能需要不同的最优 λ（如 OASIS 上 λ = 10⁴ 的 Dice 最高，而 AbdomenCTCT 上 λ = 10⁵ 的拓扑保持最严格），缺乏自适应的 λ 学习策略。当 λ = 0（完全移除半群约束）时，Dice 降至 79.80，|J|<0% 升至 1.3%，表明网络本身不具备内在的拓扑保持倾向，完全依赖半群正则化来诱导 ODE 流。

### 5.5 待验证问题

以下结论需要读者根据原文手动核实：AbdomenCTCT 上 SGDIR DiT（λ = 10⁴）的精确 Dice 值（分析中估计约 81.4）需对照表 Table 3 确认；部分基线方法（如 NODEO、PULPo）的完整指标需查阅补充材料。

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/008_Table_3.jpg]]
*Table 3: Quantitative registration results on the AbdomenCTCT dataset. The best result is shown in bold and the best competing method is presented in blue*

### 补充图表

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/005_Table_1.jpg]]
*Table 1: Quantitative registration results on the OASIS dataset in atlas-based and inter-subject settings. The best result is shown in bold and the best competitor is presented in blue*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/009_Table_4.jpg]]
*Table 4: Quantitative registration results on the LungCT dataset.The best result is shown in bold and the best competing result is presented in blue*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/015_Table_7.jpg]]
*Table 7: Computational analysis of SGDIR reveals the highest inference speed and lowest memory usage compared to top performing deformable and integration-based diffeomorphic methods*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/013_Figure_7.jpg]]
*Figure 7: The Dice score (top) and topology preservation of forward deformation (bottom) of SGDIR variants throughout time*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/014_Figure_8.jpg]]
*Figure 8: The effect of training with discrete vs. continuous (cont) time sampling on the inference for SGDIR DiT*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/004_Figure_4.jpg]]
*Figure 4: Visual comparison of SGDIR performance on the AbdomenCTCT dataset with top diffeomorphic and non-diffeomorphic methods. The -diff suffix denotes the SGDIR trained with*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/007_Figure_5.jpg]]
*Figure 5: Visual comparisons of SGDIR performance on the ACDC dataset with overlaid segmentation masks*

![[assets/figures/papers/paper_list_l2126_https_openaccess_thecvf_com_content_CVPR2026_html_Matinkia_Learning_Diff/figures/001_Figure_1.jpg]]
*Figure 1: A performance summary of SGDIR in diffeomorphic and non-diffeomorphic settings comparing with best performing (non)diffeomorphic methods in the experiments. SGDIR shows on-par performance with top deformable models in diffeomorphic setting and outperforms them in non-diffeomorphic setting*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果调控

现有学习型微分同胚配准方法面临一个根本性瓶颈：**依赖缩放-平方积分方案与多种辅助正则项（雅可比惩罚、平滑约束、逆一致性损失）来保证拓扑保留**。这些显式约束与离散积分步骤不仅增加了训练复杂度，还限制了泛化能力与推理效率。代表性方法包括：

- **TransMorph-diff** (Chen et al., MedIA 2022)：基于 Transformer 骨干网络，通过缩放-平方从速度场重建变形场，需配合显式正则项。
- **GradICON** (Tian et al., CVPR 2023)：通过近似逆一致性损失约束变形可逆性，但仍需雅可比惩罚等辅助项。
- **CycleMorph** (Kim et al., MedIA 2021)：显式施加循环一致性损失来保证可逆性。
- **R2Net** (Joshi and Hong, MedIA 2023)：利用 Lipschitz 残差网络约束变形平滑性。
- **NODEO** (Wu et al., CVPR 2022)：基于神经常微分方程的优化型方法，需通过积分求解变形路径。

**SGDIR 的核心因果调控变量是半群正则化强度 λ**。该参数直接控制变形场的拓扑保持程度：当 λ = 10⁵ 时，模型强制学习严格的微分同胚流；当 λ = 10⁴ 或更小时，约束放宽，允许非微分同胚的灵活形变。这一单一参数取代了传统方法中多个正则项的组合调控。

### 2. 方法谱系中的关键变化槽位

SGDIR 相对于现有基线方法在三个关键槽位上实现了根本性改变：

**槽位 1：正则化策略**
- 基线：缩放-平方积分 + 多种正则项（雅可比惩罚、平滑约束、逆一致性损失等）
- SGDIR：仅使用单个部分半群正则项 $\mathcal{L}_{sg}$，强制流的一致性
- 理论支撑：定理证明部分半群约束 $\phi_{2t-1} = \phi_t \circ \phi_{t-1}$ 和 $\phi_{2t-1} = \phi_{t-1} \circ \phi_t$ 足以保证网络学习到一个 ODE 的流，从而内生地保证可逆性、循环一致性和拓扑保留

**槽位 2：时间建模**
- 基线：仅预测 t=1 的最终变形场，或通过缩放-平方从速度场重建离散时间变形
- SGDIR：时间嵌入架构直接输出 t ∈ [−1,1] 的连续变形场，任意时刻可即时查询，无需迭代采样
- 参数化形式：$\phi_t(x;\theta) = x + t \mathbf{F}(x, t; I_f, I_m, \theta)$

**槽位 3：变形参数化**
- 基线：$\phi(x) = x + u(x)$ 或基于速度场 $\mathbf{v}$ 的积分路径
- SGDIR：通过时间嵌入网络 $\mathbf{F}$ 直接建模连续时间变形，消除了显式积分步骤

### 3. 适用边界

SGDIR 的适用边界由其设计假设和实验覆盖范围共同定义：

**已验证的适用范围：**
- **模态**：2D/3D 脑 MRI（OASIS、IXI、Mindboggle101、LPBA40、CANDI）、腹部 CT（AbdomenCTCT）、心脏 MRI（ACDC）、肺部 CT（LungCT）
- **任务类型**：图谱配准、个体间配准
- **骨干架构**：时间嵌入 UNet 和 Diffusion Transformer (DiT)
- **λ 配置**：λ = 10⁵（严格微分同胚）和 λ = 10⁴（灵活形变）两种模式均经过验证

**已知局限：**
- 部分半群约束仅在一个连续区间内施加，虽然在理论上证明足以诱导 ODE 流，但在极端大变形情况下的鲁棒性未进行专项验证
- 当前评估限于公开的标准医学影像配准基准，未在高度异质性或罕见病理数据上验证泛化性
- λ 的调节目前为手动预设，不同数据集可能需要不同的最优 λ，缺乏自适应的 λ 学习策略

### 4. 与现有方法的实证关系

SGDIR 在微分同胚设定下（λ = 10⁵）与现有微分同胚方法的对比：
- 在 OASIS 图谱配准上，SGDIR DiT 达到 Dice 86.53 ± 0.82，超越 **TransMorph-diff** (84.63 ± 1.12) 约 1.90 个百分点
- 拓扑违反率 |J|<0% 达到 0.0 ± 0.0，优于 **GradICON** (0.0022 ± 0.0019) 和所有其他微分同胚方法
- 在 AbdomenCTCT 上，SGDIR UNet (λ = 10⁵) 同样实现 0.0% 负雅可比体素，而 **TransMorph-diff** 为 0.043 ± 0.015

当半群约束放宽时（λ = 10⁴），SGDIR 的灵活变体进一步超越所有基线方法，包括非微分同胚方法如 **HViT** (Ghahremani et al., CVPR 2024)、**CorrMLP** (Meng et al., CVPR 2024)、**SACB-Net** (Cheng et al., CVPR 2025) 和 **TransMatch** (Jian et al., IEEE TMI 2023)。这表明半群正则化框架在微分同胚保证与配准精度之间实现了可控的权衡。

### 5. 开放问题

1. **非自主 ODE 扩展**：当前框架基于自主 ODE（平稳速度场）假设，能否将半群框架扩展到非自主 ODE（时变速度场），以进一步提高对大变形和非平稳运动的建模能力？

2. **跨模态泛化**：在更多模态（如超声、病理图像、术中影像）上，单一的半群约束是否依然能够独立保证拓扑保持？这些模态中图像质量、对比度和噪声特性差异显著，可能对半群约束的有效性提出挑战。

3. **自适应 λ 调度**：如何设计自适应的 λ 调度机制，在训练过程中动态平衡相似度与拓扑保持？当前手动调参的方式限制了方法的易用性，自适应策略可能进一步提升不同数据集上的性能鲁棒性。

4. **理论边界的实证验证**：部分半群约束仅在连续区间内施加，其在大变形极限下的理论保证是否在极端临床场景中仍能成立，需要进一步的实证验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Diffeomorphism_for_Medical_Image_Registration_with_Time_Embedded_Architectures_Using_Semigroup_Regularization.pdf]]

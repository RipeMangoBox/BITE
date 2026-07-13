---
title: "Interact2Ar: Full-Body Human-Human Interaction Generation via Autoregressive Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregressive_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- Interact2Ar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入自回归扩散管道和混合记忆机制，使模型能逐步生成子运动并利用历史上下文，从而增强交互的连贯性和实时适应能力。
primary_logic: 通过专有分支（身体、手部、轨迹）并行生成全身运动，并结合自回归生成与混合记忆，大幅提升交互质量和自适应能力。
claims:
- 在Inter-X数据集上，Interact2Ar的FID从0.671降至0.277，R-Precision Top 3从0.722提升至0.773，显著超越InterMask等SOTA方法。
- 新设计的评估器对运动退化（如噪声、轨迹交换）更敏感，验证了评估的可靠性。
- 35名参与者评定的用户研究中，Interact2Ar在文本对齐和手部运动真实性上显著优于InterMask和InterGen。
- 混合记忆消融实验表明，相比常规记忆，混合记忆能用更少的内存帧实现更优的生成质量，并促进长序列交互。
---

# Interact2Ar: Full-Body Human-Human Interaction Generation via Autoregressive Diffusion Models

> [!tip] 核心洞察
> 通过专有分支（身体、手部、轨迹）并行生成全身运动，并结合自回归生成与混合记忆，大幅提升交互质量和自适应能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | Interact2Ar：基于自回归扩散模型的全身人体交互生成 |
| 英文题名 | Interact2Ar: Full-Body Human-Human Interaction Generation via Autoregressive Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.19692) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Interact2Ar |
| Dataset | Inter-X |

> [!tip] 效果简介
> - Inter-X (Full Evaluator) 上，FID↓ 0.277 vs 0.671 (InterMask) (-0.394)；R-Precision Top 3↑ 0.773 vs 0.722 (InterMask) (+0.051)。
> - Inter-X (Body Evaluator) 上，FID↓ 0.352 vs 5.728 (InterMask) (-5.376)。

## 概要

**核心问题**：现有文本驱动的双人交互运动生成方法存在两个关键瓶颈。其一，多数方法仅关注身体运动而忽略手部细节，导致生成的交互缺乏精细的手部接触与协调；其二，主流方法采用一次性生成完整序列的范式，难以捕捉人类交互中固有的动态适应性与反应性——真实交互是一个逐步发生、彼此响应的时间过程。

**核心思路**：Interact2Ar 首次将自回归扩散模型引入全身人体交互生成，通过三项关键设计打破上述瓶颈。第一，引入**多头去噪器**，在共享编码器之上使用三个专用分支并行生成身体姿态、全局轨迹和手部运动，使模型能够以差异化精度处理不同粒度的运动成分。第二，采用**自回归生成范式**，将完整交互分解为连续的子运动片段逐步生成，每步预测均以已生成的历史为条件，从而模拟交互的时序因果性。第三，设计**混合记忆机制**，同时保留短时高帧率记忆（保证相邻片段平滑过渡）和长时降采样记忆（以极小的内存代价覆盖更长时间跨度），克服了常规记忆在长序列生成中信息衰减或内存膨胀的两难困境。

**方法定位**：Interact2Ar 属于自回归扩散生成范式，其去噪器采用协作式并行 Transformer 架构，通过交叉注意力在交互者之间传递空间关系信息。与 InterMask（残差 VQ-VAE + 掩码 Transformer）和 InterGen（单次扩散生成）等代表性方法相比，Interact2Ar 在生成范式和记忆管理上均有本质差异。

**主要结果**：在 Inter-X 数据集上，Interact2Ar 的 FID 从 InterMask 的 0.671 降至 0.277，R-Precision Top 3 从 0.722 提升至 0.773，取得显著领先。35 人参与的用户研究进一步证实，该方法在文本对齐度和手部运动真实感上均显著优于现有方法。消融实验表明，混合记忆在仅使用约 24 帧内存的条件下即可超越常规记忆的生成质量，验证了其效率与有效性。

### 人体交互生成的核心挑战

生成逼真的人与人交互动作是计算机视觉与图形学中的核心难题，其关键瓶颈在于：人类交互具有高度的**动态适应性**与**反应性**——交互双方的每一帧动作都依赖于对方的历史行为与即时反馈。现有方法普遍采用一次性生成完整序列的范式，忽略了这种逐步适应的过程，导致生成结果缺乏连贯性与真实感。

更关键的缺口在于**手部运动的缺失**。尽管手部动作（如握手、击掌、推搡）是人与人交互中信息密度最高的部位，但现有主流方法（如 **InterGen**、**InterMask**）通常仅关注身体关节，将手部视为姿态表示的附属品，导致生成的手部动作僵硬、脱离交互语境，严重损害了整体交互质量。

### 现有方法的局限

当前人体交互生成方法存在三个结构性缺陷：

1. **一次性生成范式**：模型在单次前向传播中生成整个序列，无法利用已生成帧的反馈来调整后续动作。这违背了真实交互中"感知-反应"的闭环特性，使得模型难以处理长序列中的动作漂移与语义偏离。

2. **缺乏有效的记忆机制**：即便引入有限的历史帧作为条件，现有方法也仅使用简单的短时窗口。这种设计导致模型在生成长交互序列时"遗忘"早期上下文，容易出现动作重复或语义断裂。

3. **手部运动被系统性忽略**：由于手部关节数量多、自由度大、标注成本高，现有数据集和方法往往对手部运动建模不足。这使得生成的交互在视觉上缺乏细节，无法支撑需要精细手部接触的交互类型。

### Interact2Ar 的核心动机

针对上述瓶颈，Interact2Ar 提出三个核心设计原则：

- **自回归扩散管道**：将完整交互分解为子运动序列，逐步生成每一段子运动，并利用已生成的历史作为条件。这使得模型能够根据过去的行为动态调整未来动作，模拟交互的适应性与反应性。

- **混合记忆机制**：同时维护短时高帧率记忆（保留细节过渡）和长时降采样记忆（覆盖更长时间范围），以有限的存储开销平衡局部连贯性与全局语义一致性。

- **多头去噪器架构**：通过专用分支并行生成身体姿态、全局轨迹和手部运动，确保每个部位都能获得针对性的建模，尤其是手部运动的精细生成。

## 核心方法与创新机理

Interact2Ar 的核心创新围绕一个因果链条展开：**现有交互生成方法忽略手部运动，且一次性生成完整序列，难以捕捉人类交互的动态适应性与反应性**。为解决这一问题，模型引入了三个相互协同的关键机制。

### 1. 多头去噪器：身体-手部-轨迹的并行生成

传统方法（如 InterGen）通常使用单一共享去噪头处理所有关节，导致模型难以同时兼顾身体姿态、手部精细动作和全局轨迹的不同特性。Interact2Ar 提出**多头去噪器**（Multi-Head Denoiser），在共享编码器提取联合特征后，分设三个专用预测头：

- **Body Pose Head**：预测身体关节姿态
- **Hand Pose Head**：预测手部关节姿态
- **Trajectory Head**：预测全局根轨迹

三个分支并行生成，各自专注于不同粒度的运动表征，使模型首次能够生成包含精细手部动作的全身交互运动（Figure 2A）。这一设计直接回应了“现有方法忽略手部运动”的核心瓶颈。

### 2. 自回归扩散范式：从一次性生成到逐步适应

基线方法（InterMask、InterGen 等）一次性生成完整运动序列，缺乏对交互过程中动态反馈的建模能力。Interact2Ar 将全长交互 $x$ 分解为 $K$ 个不重叠的子运动：

$$x = \bigcup_{k=0}^{K-1} x_{kn:(k+1)n}$$

模型以自回归方式逐步生成：每步调用去噪器预测下一段子运动，并将已生成帧保留为历史上下文。这一范式转变使模型具备了**时序组合、扰动适应和多人序列交互**等自适应能力（Figure 6），从根本上改变了交互生成的动态特性。

### 3. 混合记忆机制：短时细节与长时上下文的统一

自回归生成的核心挑战在于如何有效利用历史信息。常规记忆仅保留最近若干帧，要么细节丰富但时间跨度短，要么覆盖长时但信息稀疏。Interact2Ar 提出**混合记忆**（Mixed Memory），同时维护两种记忆：

- **短时记忆** $\mathcal{M}_k^s = x_{kn-m_s:kn}^0$：保留最近 $m_s$ 帧的完整帧率信息，确保子运动间的无缝过渡
- **长时记忆** $\mathcal{M}_k^l = \{ x_{kn-m_l+i\delta}^0 \mid i=0,1,\ldots,\lfloor m_l/\delta \rfloor \}$：以步长 $\delta$ 从过去 $m_l$ 帧中降采样，覆盖更长时间范围，避免长序列中的动作重复

两者拼接为完整记忆 $\mathcal{M}_k = \{ \mathcal{M}_k^l, \mathcal{M}_k^s \}$，供去噪器条件生成：

$$\hat{x}_{kn:(k+1)n}^0 = G(x_{kn:(k+1)n}^t, \mathcal{M}_k, c, t)$$

消融实验（Table 3）证实，混合记忆配置（$m_s=15, m_l=45, \delta=5$）仅使用 24 帧即实现 FID 0.277，优于常规记忆（$m_s=15, m_l=15$）的 FID 0.283，同时内存开销降低至 1/3（Figure 3）。

### 4. 协作去噪器：交互者间的信息流动

除上述三个主创新外，模型还采用**协作去噪器**（Cooperative Denoisers）：两个交互者各有一条共享权重的并行 Transformer 流，通过交叉注意力交换人际空间信息（Figure 2B）。这一设计确保了双人运动的空间协调性，是生成高质量交互的基础架构支撑。

### 创新点之间的因果耦合

三个核心创新并非孤立存在：**多头去噪器**提供了生成全身运动（含手部）的能力基础；**自回归范式**赋予模型逐步生成与动态适应的可能性；**混合记忆**则解决了自回归生成中历史上下文的质量与效率矛盾。三者协同作用，使 Interact2Ar 在 Inter-X 数据集上将 FID 从 InterMask 的 0.671 大幅降至 0.277，R-Precision Top 3 从 0.722 提升至 0.773（Table 2），并在用户研究中显著优于基线方法（Figure 4）。

Interact2Ar 的整体框架围绕三个核心设计展开：**多头去噪器**、**协作去噪机制**与**自回归生成范式**，共同构成一个从文本条件到全身交互运动生成的端到端管道。

### 输入与运动表示

模型以文本描述 $c$ 为条件，生成双人全身交互运动 $x$。交互运动完全基于 SMPL-X 参数表示，每个个体的运动 $^i x$ 由根平移、根旋转（6D 表示）、身体关节姿态和手部关节姿态组成。损失函数在多个表示层级上施加监督，总训练损失为：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{repr}} \mathcal{L}_{\mathrm{repr}}(x, \hat{x}) + \lambda_{\mathrm{orient}} \mathcal{L}_{\mathrm{orient}}(r, \hat{r}) + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}}(p, \hat{p}) + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}}(v, \hat{v}) + \lambda_{\mathrm{foot}} \mathcal{L}_{\mathrm{foot}}(f, \hat{f}) + \lambda_{\mathrm{dist}} \mathcal{L}_{\mathrm{dist}}(d, \hat{d})$$

该损失加权组合了表示损失、根方向损失、关节位置损失、速度损失、足部接触损失和成对距离损失，确保模型在运动学、物理接触和空间关系等多个维度上得到约束。

### 多头去噪器架构

去噪器采用“共享编码器 + 专用预测头”的设计（Figure 2A）。噪声运动和文本条件首先经编码器嵌入到统一的潜在空间，随后分流至三个并行的专用头部分支：

- **身体姿态头**：预测身体关节姿态；
- **轨迹头**：预测全局根轨迹；
- **手部姿态头**：预测手部关节姿态。

这种分支设计使模型能够对不同粒度的运动组件进行专业化建模，尤其解决了现有方法普遍忽略手部运动的问题。

### 协作去噪机制

为有效捕捉双人交互中的信息流动，模型采用**协作去噪器**（Figure 2B）：两个共享权重的并行 Transformer 流分别生成两个交互者，并通过交叉注意力层交换人际信息。具体实现中，运动编码器及身体、手部姿态头均使用 8 个 Transformer 块（8 注意力头，潜在维度 512，前馈维度 1024），轨迹头使用 4 个块以降低计算开销。

### 自回归生成与混合记忆

区别于一次性生成完整序列的范式，Interact2Ar 将全长交互 $x$ 分解为 $K$ 个长度为 $n$ 的不重叠子运动：

$$x = \bigcup_{k=0}^{K-1} x_{kn:(k+1)n}$$

生成过程自回归进行：每一步去噪器 $G$ 根据当前噪声子运动、历史记忆 $\mathcal{M}_k$、文本条件 $c$ 和扩散步 $t$ 预测干净子运动：

$$\hat{x}_{kn:(k+1)n}^0 = G(x_{kn:(k+1)n}^t, \mathcal{M}_k, c, t)$$

记忆机制采用**混合记忆**策略（Figure 3），由两部分拼接而成：

$$\mathcal{M}_k = \{ \mathcal{M}_k^l, \mathcal{M}_k^s \}$$

- **短时记忆** $\mathcal{M}_k^s = x_{kn-m_s:kn}^0$：保留最近 $m_s$ 个生成帧的全帧率细节，确保子运动间的无缝过渡；
- **长时记忆** $\mathcal{M}_k^l = \{ x_{kn-m_l+i\delta}^0 \mid i=0,1,\ldots,\lfloor m_l/\delta \rfloor \}$：以步长 $\delta$ 从过去 $m_l$ 帧中降采样，覆盖更长时间范围，防止长序列中的动作重复。

该设计以更少的内存帧数（仅 24 帧即可达到最优 FID）实现了优于常规记忆的生成质量，内存开销降低约 3 倍。扩散步数方面，完整模型使用 1000 步配合 DDIM-50 采样，而自回归版本仅需 10 步即可达到最佳经验效果。

### 管道模块总览

| 模块 | 功能 |
|---|---|
| Condition Encoder | 将噪声运动和文本条件嵌入潜在空间 |
| Cooperative Denoiser | 共享权重并行 Transformer 流，交叉注意力交换人际信息 |
| Body Pose Head | 从潜在表示预测身体关节姿态 |
| Trajectory Head | 预测全局根轨迹 |
| Hand Pose Head | 预测手部关节姿态 |
| Mixed Memory Buffer | 存储短时全帧率记忆和长时降采样记忆 |
| Autoregressive Generation Loop | 迭代生成子运动，每次调用去噪器并更新混合记忆 |

Interact2Ar 的生成管道由三个核心模块构成：**多头去噪器**（Multi-Head Denoiser）、**协作去噪器**（Cooperative Denoisers）与**自回归生成循环**（Autoregressive Generation Loop），辅以**混合记忆缓冲**（Mixed Memory Buffer）实现长序列上下文管理。

### 3.1 交互表示与训练损失

模型完全依赖 SMPL-X 参数表示双人交互。一个二元交互 $x$ 由两个个体的姿态组成：

$$x := \{ {}^a x, {}^b x \}$$

每个个体的运动 $^i x$ 表示为 $(r, \varphi, \theta_{\mathrm{body}}, \theta_{\mathrm{hands}})$，即根平移、根旋转、身体关节和手部关节的 6D 旋转表示。文本条件 $c$ 通过 CLIP 编码器嵌入。

训练去噪器 $G$ 时，总损失函数为多分量加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{repr}} \mathcal{L}_{\mathrm{repr}}(x, \hat{x}) + \lambda_{\mathrm{orient}} \mathcal{L}_{\mathrm{orient}}(r, \hat{r}) + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}}(p, \hat{p}) + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}}(v, \hat{v}) + \lambda_{\mathrm{foot}} \mathcal{L}_{\mathrm{foot}}(f, \hat{f}) + \lambda_{\mathrm{dist}} \mathcal{L}_{\mathrm{dist}}(d, \hat{d})$$

其中各分量含义如下：

| 损失项 | 变量含义 | 作用 |
|--------|----------|------|
| $\mathcal{L}_{\mathrm{repr}}$ | 6D 旋转表示的重建损失 | 约束身体与手部关节的旋转空间 |
| $\mathcal{L}_{\mathrm{orient}}$ | 根方向 $r$ 的 L2 损失 | 稳定全局朝向 |
| $\mathcal{L}_{\mathrm{pos}}$ | 全局关节位置 $p$ 的 L2 损失 | 见公式 (10) |
| $\mathcal{L}_{\mathrm{vel}}$ | 关节速度 $v$ 的 L2 损失 | 抑制抖动，提升平滑性 |
| $\mathcal{L}_{\mathrm{foot}}$ | 足部接触损失 | 见公式 (12) |
| $\mathcal{L}_{\mathrm{dist}}$ | 成对关节距离图损失 | 见公式 (13) |

**关节位置损失**（公式 10）对两个交互者的全局关节位置分别计算 L2 损失：

$$\mathcal{L}_{\mathrm{pos}}(p, \hat{p}) = ||p_a - \hat{p}_a||_2^2 + ||p_b - \hat{p}_b||_2^2$$

**足部接触损失**（公式 12）通过足部接触指标 $f_i$ 惩罚足部速度，减少滑步和悬浮：

$$\mathcal{L}_{\mathrm{foot}}(f, \hat{f}) = \sum_{i\in\{\mathrm{feet}\}} ||v_i \odot f_i||_2^2 + ||\hat{v}_i \odot \hat{f}_i||_2^2$$

**成对关节距离图损失**（公式 13）捕捉两个交互者间的空间关系，对距离图进行掩码 L2 损失：

$$\mathcal{L}_{\mathrm{dist}}(d, \hat{d}) = ||(D(p_a, p_b) - D(\hat{p}_a, \hat{p}_b)) \odot M||_2^2$$

其中 $D(\cdot, \cdot)$ 计算两个交互者关节间的成对距离矩阵，$M$ 为掩码。

### 3.2 多头去噪器与协作去噪器

**多头去噪器**（Figure 2A）采用共享编码器 + 专用预测头的架构设计。编码器将噪声运动 $x^t$ 和文本条件 $c$ 映射到统一潜在空间，随后分三路并行输出：

- **Body Pose Head**：预测身体关节姿态（含 22 个身体关节的 6D 旋转）
- **Trajectory Head**：预测全局根轨迹（根平移与根旋转）
- **Hand Pose Head**：预测手部关节姿态（双手共 30 个关节的 6D 旋转）

这种分支设计的核心优势在于：身体、轨迹和手部运动具有不同的动力学特性，专用头可针对各自子空间独立优化，避免单一共享头导致的表示容量瓶颈。

**协作去噪器**（Figure 2B）由两个共享权重的并行 Transformer 流组成，分别处理交互者 $a$ 和 $b$ 的运动。两者通过交叉注意力（cross-attention）交换人际信息，使每个个体的生成过程能感知对方的状态。这种设计确保了交互的协调性——例如，当一人伸出手时，另一人能生成相应的回应姿态。

### 3.3 自回归生成与混合记忆

传统扩散模型一次性生成完整序列，难以捕捉交互的动态适应性。Interact2Ar 将全长交互 $x$（$N$ 帧）分解为 $K$ 个不重叠的子运动，每段长度为 $n$：

$$x = \bigcup_{k=0}^{K-1} x_{kn:(k+1)n}$$

自回归生成循环依次预测每一段子运动，核心机制如下：

**短时记忆** $\mathcal{M}_k^s$ 保留最近生成的 $m_s$ 个干净帧，提供高帧率细节信息：

$$\mathcal{M}_k^s = x_{kn-m_s:kn}^0$$

**长时记忆** $\mathcal{M}_k^l$ 以步长 $\delta$ 从过去 $m_l$ 帧中降采样，覆盖更长时间范围：

$$\mathcal{M}_k^l = \{ x_{kn-m_l+i\delta}^0 \mid i=0,1,\ldots,\lfloor m_l/\delta \rfloor \}$$

**混合记忆**将两者拼接：

$$\mathcal{M}_k = \{ \mathcal{M}_k^l, \mathcal{M}_k^s \}$$

最终，去噪器 $G$ 根据噪声子运动、混合记忆、文本条件 $c$ 和扩散步 $t$ 预测干净子运动：

$$\hat{x}_{kn:(k+1)n}^0 = G(x_{kn:(k+1)n}^t, \mathcal{M}_k, c, t)$$

混合记忆的设计解决了常规记忆的两难困境：短窗口丢失长程上下文（导致动作重复），长窗口全帧率则内存开销过大。通过降采样长时记忆，模型以更少的内存帧（如 $m_s=15, m_l=45, \delta=5$ 时实际仅用 24 帧）实现了优于常规记忆（$m_s=15, m_l=15$ 共 30 帧）的生成质量（FID 0.277 vs 0.283），内存效率提升约 3 倍（Figure 3, Table 3）。

![[assets/figures/papers/paper_list_l1675_Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregress/figures/003_Figure_3.jpg]]
*Figure 3: Mixed Memory enables access to both detailed shortterm information, facilitating seamless transitions, along with long-term context, avoiding action repetition in long interactions. Our proposed Mixed Memory overcomes the limitations of regular context memory, providing up to a ×3 reduction in memory size*

## 实验与关键发现

### 评估器鲁棒性验证

交互运动生成领域长期受限于评估器对运动退化的不敏感性，导致指标无法可靠反映生成质量。Interact2Ar 重新训练了评估器，仅使用全局关节位置以消除旋转表示偏差，并在三种典型退化场景下验证其鲁棒性：对全身运动施加噪声、仅对轨迹施加噪声、交换双人轨迹。如表1所示，旧评估器在轨迹交换后 FID 仍低至 0.122、R-Precision 仍达 0.737，几乎无法区分退化运动与真实运动；而新评估器在相同条件下 FID 飙升至 62.05、R-Precision 骤降至 0.249，对运动质量退化表现出显著更高的敏感性。这为后续定量评估的可靠性奠定了基础。

### 主实验结果

在 Inter-X 数据集上，Interact2Ar 在所有标准指标上均显著超越现有方法。使用新训练的 Full Evaluator 评估时，Interact2Ar 的 FID 从 InterMask 的 0.671 降至 **0.277**（降幅 58.7%），R-Precision Top 3 从 0.722 提升至 **0.773**。在仅评估身体的 Body Evaluator 下，FID 从 5.728 降至 **0.352**，降幅超过一个数量级。即使去掉自回归生成模块的 Interact2Ar* 版本，FID 也达到 0.305，已优于 InterMask。所有评估重复 20 次并报告 95% 置信区间，确保统计可靠性。

在 InterHuman 数据集上的跨库评估进一步验证了泛化能力：Interact2Ar 的 R-Precision Top 1 达到 0.453，优于 InterMask 和 InterGen。

### 用户研究

35 名参与者对 10 个交互视频进行排名评估，覆盖文本对齐度和手部运动真实感两个维度。结果表明 Interact2Ar 在两个维度上均显著优于 InterMask 和 InterGen，且接近真实运动（Ground Truth）的质量水平。这直接验证了多头去噪器中专用手部分支的设计有效性。

### 混合记忆消融

混合记忆是自回归生成的核心组件。消融实验统一设置短时窗口 $m_s = 15$、降采样步长 $\delta = 5$，对比不同长时窗口 $m_l$ 配置下的生成质量。结果显示，混合记忆配置 $(m_s=15, m_l=45, \delta=5)$ 使用仅 24 个记忆帧即达到 FID **0.277**，优于常规记忆 $(m_s=15, m_l=15)$ 的 FID 0.283，同时内存开销减少约 3 倍。当 $m_l$ 过小（如 15）时，模型缺乏足够的长时上下文，导致动作重复；当 $m_l$ 过大（如 60）时，降采样后的稀疏帧无法提供有效的短时过渡信息，质量反而下降。

### 文本编码器与附加指标

文本编码器的选择对生成质量影响微小：CLIP 与 Qwen3-VL-Embedding-2B 在原始 Inter-X 指标上表现接近。这一现象归因于当前数据集的文本描述多样性有限，高级编码器的语义理解优势未能充分发挥。在接触频率、FID_CD、穿透体积、足部物理接触等附加二体交互指标上，Interact2Ar 均达到最优，进一步证实了成对距离损失和足部接触损失的有效性。

### 自适应能力验证

自回归扩散与混合记忆的组合赋予了模型三项关键自适应能力：（1）**时序运动组合**——可拼接不同文本描述的子运动生成连贯长序列；（2）**位移适应**——当交互者位置被外力扰动后，模型能自动调整后续运动以恢复合理空间关系；（3）**序贯多人交互**——可逐步引入新交互者，生成多人场景。这些能力是传统一次性生成范式无法实现的。

### 失败模式与局限

尽管整体质量大幅提升，所有方法（包括 Interact2Ar）仍存在脚部滑动问题，足部接触损失未能完全消除悬浮和滑步现象，可能需要后处理或物理约束增强。自回归推理的误差累积是另一潜在风险：早期子运动的微小偏差可能随生成步数放大。此外，模型仅使用中性体型归一化，无法生成不同体型的个体交互，且手部接触的精确物理建模（如接触压力分布）尚未解决。

![[assets/figures/papers/paper_list_l1675_Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregress/figures/007_Table_2.jpg]]
*Table 2: Comparison of our model (Interact2Ar) to the state of the art in human-human interaction motion generation on the Inter-X dataset. *Interact2Ar model is the version without autoregressive generation. All evaluations have been executed 20 times to elude the randomness of the generation. ± indicates the 95% confidence interval. We highlight the best and the second best results*

![[assets/figures/papers/paper_list_l1675_Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregress/figures/004_Table_1.jpg]]
*Table 1: Evaluator robustness comparison. Our evaluator demonstrates superior sensitivity to motion quality degradations compared to the previous one. Tested degradations: noise on full representation, noise on trajectory only, and trajectory swapping*

![[assets/figures/papers/paper_list_l1675_Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregress/figures/012_Table.jpg]]
*Table: B. Ablation study on memory configurations for Interact2Ar across different evaluation settings. ms and ml represent the context window used for each memory. ml = − indicates models not using Mixed Memory. For models using Mixed Memory, δ = 5. The total number of frames used in the full memory is $\mathcal { M } = m _ { s } + m _ { l } / \delta$*

![[assets/figures/papers/paper_list_l1675_Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregress/figures/014_Figure.jpg]]
*Figure: B. Close-up visualizations. Zoomed-in views of hands during challenging interactions involving body and hand contacts*

![[assets/figures/papers/paper_list_l1675_Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregress/figures/011_Table.jpg]]
*Table: A. Comparison of our model (Interact2Ar) to the state of the art in human-human interaction motion generation on the Inter-X dataset. *Interact2Ar model is the version without autoregressive generation. All evaluations have been executed 20 times to elude the randomness of the generation. ± indicates the 95% confidence interval. We highlight the best and the second best results*

## 定位与知识库关联

### 与基线工作的关系

Interact2Ar 的提出直接回应了现有双人交互生成方法的两个核心瓶颈：**忽略手部运动**和**一次性生成完整序列导致缺乏动态适应性**。在方法谱系中，其与以下基线形成明确对比：

- **InterGen**（基于扩散模型的双人交互生成）：InterGen 使用单一共享去噪头处理所有关节，且一次性生成完整运动序列。Interact2Ar 在此基础上引入多头去噪器（身体、手部、轨迹三个专用分支）和自回归生成范式，从根本上改变了信息流的组织方式。这一改动使得模型能够为不同身体部位学习专门的生成策略，尤其显著提升了手部运动质量——用户研究中 35 名参与者对 Interact2Ar 的手部真实感评分显著高于 InterGen（Figure 4, Sec. 4.1）。

- **InterMask**（基于残差 VQ-VAE 的掩码 Transformer 交互生成方法）：InterMask 在 Inter-X 数据集上曾是 SOTA，但其 FID 为 0.671。Interact2Ar 将 FID 降至 0.277，降幅达 0.394（Table 2）。这一提升的关键在于自回归生成配合混合记忆机制，使得模型能够利用历史上下文信息逐步生成子运动，而非一次性预测整个序列。值得注意的是，即使是不带自回归生成的 Interact2Ar* 版本，在 Body Evaluator 上的 FID 也达到 0.352，远优于 InterMask 的 5.728（Table 2），说明多头去噪器架构本身就带来了显著增益。

- **T2M**（文本到单人运动的扩散生成方法）：T2M 作为单人运动生成的经典方法，为扩散模型在运动生成领域的应用奠定了基础。Interact2Ar 将其扩散框架扩展到双人交互场景，并通过协作去噪器中的交叉注意力机制实现交互者之间的信息交换，这是 T2M 框架中不存在的关键扩展。

### 适用边界

Interact2Ar 的设计假设和实验设置划定了其适用边界：

1. **数据表示依赖**：模型完全依赖 SMPL-X 参数表示交互，使用 6D 旋转表示。这意味着模型无法处理原始视频或点云数据，需要预先将运动数据转换为 SMPL-X 参数。该表示的优势在于统一的身体-手部参数化，但代价是失去了对服装、头发等外观信息的建模能力。

2. **体型归一化限制**：模型仅使用中性体型进行训练，无法生成不同体型的个体交互。这是论文明确指出的局限性之一，意味着当前模型无法处理“一个高个子推一个矮个子”这类需要体型差异的场景。

3. **双人交互假设**：核心架构设计围绕双人交互展开，协作去噪器包含两个并行的 Transformer 流。虽然论文展示了顺序多人交互的扩展能力（Figure 6），但这是通过自回归方式串联双人交互实现的，而非原生支持多人同时交互。

4. **文本条件质量**：消融实验表明，使用 CLIP 或 Qwen3-VL-Embedding-2B 作为文本编码器对生成质量影响微小（Table C），说明当前数据集（Inter-X）的文本多样性有限，模型尚未充分受益于更强的文本理解能力。在文本描述更丰富或更复杂的场景下，性能增益可能受限。

### 局限与开放问题

论文明确指出的局限性和引申的开放问题包括：

**已知局限**：
- **脚部滑动**：所有方法（包括 Interact2Ar）仍存在脚部滑动问题，可能需要后处理或额外数据来解决。这是运动生成领域的共性问题，Interact2Ar 的足部接触损失（Eq. 12）虽然有所缓解，但未能根除。
- **体型单一**：仅使用中性体型归一化，无法生成不同体型的个体交互。
- **误差累积**：自回归推理可能引入误差累积，长序列生成时早期子运动的误差会传播到后续生成步骤。
- **文本多样性受限**：当前数据集的文本描述多样性有限，限制了高级文本编码器的增益效果。

**开放问题**：
- **多体型建模**：如何在不牺牲效率的前提下模拟不同体型的交互？这可能需要引入体型条件编码或从多样化体型数据中学习。
- **手部接触物理约束**：如何精确建模手部接触和物理约束（如接触压力、抓握力）？当前方法主要依赖运动学损失，缺乏对接触动力学的显式建模。
- **脚部滑动的根本解决**：除了后处理，是否可以通过改进损失函数、引入物理模拟或增加足部接触数据来从根本上减轻脚部滑动？
- **多人场景扩展性**：自回归扩散在更复杂的多人场景（三人及以上同时交互）中的扩展性和计算成本如何？协作去噪器架构可能需要从双流扩展到多流，计算复杂度将呈超线性增长。
- **评估器泛化性**：论文设计了更敏感的运动评估器（Table 1），但该评估器本身也是基于特定数据训练的。如何构建跨数据集、跨交互类型的通用评估器仍是一个开放挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/Interact2Ar_Full_Body_Human_Human_Interaction_Generation_via_Autoregressive_Diffusion_Models.pdf]]

---
title: "MoSa: Motion Generation with Scalable Autoregressive Modeling"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/MoSa_Motion_Generation_with_Scalable_Autoregressive_Modeling.pdf
project_link: "https://mosa-web.github.io/MoSa-web"
code_link: null
aliases:
- MoSa
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 多尺度令牌保留策略（MTPS）及基于此的可扩展自回归（SAR）建模
primary_logic: 通过在残差量化过程中保留粗到细的多尺度令牌集，并利用单个可扩展自回归transformer联合建模所有尺度，MoSa实现了跨层一致的粗到细生成，大幅减少推理步骤（10步），同时提升生成质量和速度。
claims:
- MoSa在Motion-X数据集上FID达到0.061，显著优于MoMask的0.20，且推理时间降低27%。
- 消融实验表明移除卷积-注意力混合模块后，HumanML3D生成FID从0.085升至0.150，重建FID从0.030升至0.055，证实CAQ-VAE的必要性。
- 随着推理步数从1到10，FID从23.92逐步降至0.085，验证了粗到细生成的有效性。
- HumanML3D 上 FID↓ = 0.085
---

# MoSa: Motion Generation with Scalable Autoregressive Modeling

> [!tip] 核心洞察
> 通过在残差量化过程中保留粗到细的多尺度令牌集，并利用单个可扩展自回归transformer联合建模所有尺度，MoSa实现了跨层一致的粗到细生成，大幅减少推理步骤（10步），同时提升生成质量和速度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoSa：可扩展自回归运动生成 |
| 英文题名 | MoSa: Motion Generation with Scalable Autoregressive Modeling |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2511.01200) · [Project](https://mosa-web.github.io/MoSa-web) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoSa |
| Dataset | HumanML3D, Motion-X |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.085 vs 0.20 (MoMask, reimpl. 0.172) (↓ 0.115)；R Precision Top-1↑ 0.530 vs 0.523 (MoMask) (↑ 0.007)；MultiModal Dist↓ 2.836 vs 3.016 (MoMask) (↓ 0.18)。
> - Motion-X 上，FID↓ 0.061 vs 0.20 (MoMask) (↓ 0.139)；R Precision Top-1↑ 0.448 vs 0.437 (MoMask) (↑ 0.011)；MultiModal Dist↓ 2.982 vs 3.180 (MoMask) (↓ 0.198)。

## 概述

文本驱动的人体运动生成旨在从自然语言描述合成逼真的3D动作序列。当前领先范式采用矢量量化-生成式Transformer（VQ-GT）框架：先通过VQ-VAE将连续运动压缩为离散令牌序列，再用生成式Transformer建模令牌分布。然而，以**MoMask**（Guo et al., CVPR 2024）为代表的层次化残差VQ方法存在根本性瓶颈——它独立生成各残差量化层的令牌，导致跨层信息不对齐，限制了运动生成的一致性与全局建模能力。

MoSa针对这一问题提出两个核心创新。**多尺度令牌保留策略（MTPS）**在残差量化过程中，通过对每层量化前的下采样与量化后的上采样，保留粗到细的多尺度令牌集；**可扩展自回归（SAR）建模**则用单个Transformer以尺度为步长联合预测所有尺度的令牌，每步并行生成该尺度的全部令牌。这一设计将推理步数从序列长度级（如49步）压缩至量化层数级（10步），同时实现了跨层一致的粗到细生成。

实验表明，MoSa在HumanML3D和Motion-X两个主流基准上均取得最优性能。在Motion-X上，FID达到0.061，显著优于MoMask的0.20；推理时间降低约27%。消融实验验证了卷积-注意力混合VQ-VAE（CAQ-VAE）、ℓ₂归一化、尺度感知RoPE等设计选择的必要性。此外，MoSa通过MASK_edit令牌机制支持运动修复、扩展等编辑任务，无需额外微调。

## 背景与动机

### 文本驱动人体运动生成

文本驱动的人体运动生成旨在根据自然语言描述合成逼真、语义一致的三维人体动作序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛应用。近年来，该领域的主流范式逐渐收敛于**矢量量化–生成式Transformer（VQ-GT）**框架：首先使用VQ-VAE将连续运动序列压缩为离散令牌（tokens），再通过自回归或掩码Transformer在令牌空间中进行生成。这一范式在**T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., CVPR 2024）等工作中取得了显著进展，在HumanML3D和Motion-X等基准上实现了领先的生成质量。

### 现有VQ-GT范式的瓶颈：跨层信息不对齐

尽管VQ-GT框架在运动生成中表现突出，但其核心设计存在一个被忽视的结构性缺陷。以当前最优方法**MoMask**为例，其生成过程分为两个阶段：首先由基础Transformer生成第一层残差量化的令牌序列，再由残差Transformer独立生成后续各层的残差令牌。这种**分层独立生成**的策略导致了一个关键问题——**跨层信息不对齐**（cross-layer misalignment）：不同量化层之间的令牌缺乏联合建模，粗尺度的结构信息无法有效指导细尺度的细节生成，限制了运动的一致性和全局建模能力。

更根本地，这一瓶颈源于传统残差VQ-VAE在量化过程中**仅保留最终单一尺度的令牌表示**。在逐层残差量化时，每一层都将特征压缩到相同的固定长度（通常为运动序列长度T），丢弃了中间尺度的粗粒度结构信息。这使得后续的生成式Transformer只能基于同一分辨率的令牌进行建模，无法利用“从粗到细”的多尺度先验。

### MoSa的动机与核心思路

针对上述问题，MoSa提出了一套系统性的解决方案，其核心洞察是：**在残差量化过程中显式保留粗到细的多尺度令牌集，并利用单个可扩展自回归Transformer对其进行联合建模**。具体而言：

1. **多尺度令牌保留策略（MTPS）**：在残差量化的每一层，通过下采样–量化–上采样的操作，保留从粗粒度（如3个令牌）到细粒度（如49个令牌）的多尺度离散表示，形成层次化的令牌集合。
2. **可扩展自回归（SAR）建模**：将经典的自回归生成范式从“逐令牌预测”扩展为“逐尺度预测”——以尺度为步长，每步并行预测该尺度内的所有令牌，且粗尺度令牌作为细尺度预测的条件。

这一设计从根本上解决了跨层不对齐问题：所有尺度在同一个Transformer中被联合建模，粗尺度为细尺度提供结构约束，细尺度在粗尺度基础上补充细节。同时，推理步数从传统方法的序列长度T步（如49步）大幅缩减至量化层数Q步（如10步），在提升生成质量的同时实现了约27%的推理加速。

### 与现有方法的对比定位

现有文本驱动运动生成方法可大致分为三类：基于VAE的方法（如**TEMOS**, Petrovich et al., ECCV 2022）、基于扩散模型的方法（如**MotionDiffuse**, Zhang et al., arXiv 2022; **MLD**, Chen et al., CVPR 2023）以及基于VQ-GT的方法（如**T2M-GPT**; **MoMask**）。MoSa属于VQ-GT范式的改进工作，但与MoMask的“双Transformer分层独立生成”不同，MoSa通过MTPS和SAR实现了**单Transformer跨尺度联合生成**，在方法谱系上填补了“多尺度一致建模”的空白。

## 核心创新

MoSa 的核心创新在于突破了传统 VQ-GT 范式（以 **MoMask** (Guo et al., CVPR 2024) 为代表）中独立生成各层残差令牌所导致的跨层信息不对齐瓶颈。其关键因果机制是**多尺度令牌保留策略（MTPS）**与基于此构建的**可扩展自回归（SAR）建模**，二者协同实现了跨层一致的粗到细生成。

### 从独立层生成到跨层对齐的范式转变

传统方法（如 MoMask）在残差量化后，对基础层和残差层分别使用两个独立的 masked transformer 进行生成。这种设计使得各层令牌之间缺乏显式的信息交互与约束，导致生成的各层表示在语义上无法对齐，损害了运动的一致性和全局建模能力。

MoSa 通过以下两个紧密耦合的 changed slots 从根本上改变了这一范式：

1. **令牌保留策略**：从“同一尺度的残差令牌序列”转变为“多尺度令牌集”——即保留 $Q$ 个尺度、长度从 $s_1$ 到 $s_Q$ 递增的令牌集合 $X = \{ x^{(1)}, \ldots, x^{(Q)} \}$（Eq. 7），形成粗到细的层次化表示。

2. **生成式 Transformer**：从“两个独立的 masked transformer”转变为“单个可扩展自回归 transformer（SAR）”。SAR 以尺度为单位进行自回归建模（Eq. 9），每步并行预测该尺度的所有令牌，而非逐时间步生成。这使推理步骤从序列长度 $T$（如 49 步）骤降至量化层数 $Q = 10$ 步。

$$p(x^{(1)}, \ldots, x^{(Q)} | c) = \prod_{q=1}^Q p(x^{(q)} | x^{(1)}, \ldots, x^{(q-1)}, c)$$

### 关键设计决策与消融证据

**MTPS 的尺度调度**：预定义的尺度序列 $S = (s_1, s_2, \ldots, s_Q)$ 是粗到细生成的核心控制变量。消融实验表明，尺度过小（$Q=6$）或过大（$Q=15$）均损害生成质量，$Q=10$ 在所有指标上取得最佳平衡（Fig. 4）。当前调度器为固定递增序列，未探索动态或学习得到的调度策略，这是一个明确的局限性。

**尺度感知位置编码**：为适应多尺度令牌序列中位置语义的变化，MoSa 提出了尺度感知 RoPE，将位置归一化至当前尺度。消融实验（TABLE III）证实其在所有指标上优于标准 RoPE、Sinusoidal 和可学习位置编码。这一设计是 SAR 有效建模跨尺度依赖的关键支撑。

**推理效率与质量的协同提升**：得益于 SAR 的并行预测特性，MoSa 在 HumanML3D 上的平均推理时间降至 0.045 秒，相比 MoMask 的 0.062 秒降低约 27%。同时，FID 从 0.20 显著改善至 0.085（TABLE I），验证了粗到细生成在质量与速度上的双重优势。Fig. 8 进一步展示了从推理步 1 到步 10，FID 从 23.92 逐步降至 0.085 的渐进改善过程，直观呈现了粗到细特性的有效性。

### 需要手动验证的潜在局限

MTPS 的尺度调度器 $S$ 是预定义的固定序列，论文未探索其根据运动类型或文本语义自适应调整的可能性。此外，虽然推理步数大幅减少，但每步需并行预测多个令牌，对内存和计算的要求在极大规模序列上可能仍构成挑战。运动编辑任务目前仅提供了定性示例（Fig. 7），缺乏定量指标，其鲁棒性和泛化性有待进一步考察。

## 整体框架

MoSa 的整体 pipeline 由两个核心阶段构成：**CAQ‑VAE（卷积‑注意力混合矢量量化变分自编码器）** 和 **可扩展自回归 Transformer（Scalable Autoregressive Transformer，SAR）**。前者将运动序列压缩为多尺度离散令牌集，后者以尺度为步长自回归地预测该令牌集，实现从粗到细的生成。整个框架的关键创新在于：在残差矢量量化（RQ‑VAE）中嵌入 **多尺度令牌保留策略（Multi‑scale Token Preservation Strategy，MTPS）**，使量化过程不再仅保留单一精细尺度的令牌，而是显式维护一个从粗到细的多尺度令牌集合 $X$（见 Fig. 2）。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/002_Figure_2.jpg]]
*Figure 2: Our MoSa framework overview. (a) Multi-scale Token Preservation Strategy (MTPS) integrated into a hierarchical RQ-VAE. MTPS employs interpolation (Downsampling/Upsampling operation) at each hierarchical quantization to effectively retain coarse-to-fine multi-scale token set X. The scales follow a predefined scheduler*

### 1. CAQ‑VAE 编码与多尺度量化

运动序列 $m$ 首先经过 CAQ‑VAE 的编码器 $\mathcal{E}$，得到连续潜在表示 $z$。随后进入 $Q=10$ 层的层次化残差量化过程。与传统 RQ‑VAE 在每层直接对原始尺度的残差进行量化不同，MoSa 在每层量化前执行 **下采样** 操作 $\downarrow(\cdot, s_q)$，将残差 $z^{(q)}$ 压缩至目标尺度 $s_q$（$s_1 < s_2 < \dots < s_Q = T$），再通过量化器 $\operatorname{Quant}^{(q)}$ 映射到对应码本中的离散令牌 $x^{(q)}$。量化后的令牌经反量化 $\operatorname{Dequant}^{(q)}$ 和 **上采样** $\uparrow(\cdot)$ 恢复至精细尺度，用于计算残差并传递至下一层。这一“下采样→量化→上采样”的循环（Eq. 8）使得每层输出一个尺度为 $s_q$ 的令牌序列，最终形成多尺度令牌集：

$$X = \{ \underbrace{(x_1^1, \ldots, x_{s_1}^1)}_{x^{(1)}}, \ldots, \underbrace{(x_1^Q, \ldots, x_{s_Q}^Q)}_{x^{(Q)}} \}$$

CAQ‑VAE 的解码器则从该多尺度令牌集重建运动 $\hat{m}$。训练时使用包含 $Q$ 层约束的残差 VQ‑VAE 复合损失（Eq. 6），其中 $\ell_2$ 归一化将码本查找的距离度量转换为余弦相似度，显著提升码本利用率（消融实验中移除 $\ell_2$ 归一化后码本利用率从 99.5% 降至 88.9%）。

### 2. 可扩展自回归建模（SAR）

传统的自回归 Transformer 按时间步逐令牌预测（Eq. 4），而 MoSa 的 SAR 以 **尺度为单位** 进行自回归建模。给定文本条件 $c$ 和历史尺度令牌 $x^{(1)}, \dots, x^{(q-1)}$，SAR 并行预测下一尺度的全部 $s_q$ 个令牌：

$$p(x^{(1)}, \ldots, x^{(Q)} \mid c) = \prod_{q=1}^{Q} p(x^{(q)} \mid x^{(1)}, \ldots, x^{(q-1)}, c)$$

在训练时，尺度感知的注意力掩码确保 $x^{(q)}$ 只能关注 $x^{(\le q)}$。由于不同尺度的令牌序列长度不同，在输入 Transformer 前，前一尺度的令牌 $x^{(q-1)}$ 会经过“上采样→下采样”操作以匹配当前尺度的序列长度（见 Fig. 2(b)）。推理时，SAR 仅需 $Q=10$ 步即可完成从粗尺度（如 $s_1=3$）到细尺度（$s_Q=49$）的生成，相比逐时间步预测的范式大幅减少了推理步数。

### 3. 模块关系与数据流

整体数据流可概括为：

1. **CAQ‑VAE 编码器** → 连续潜在表示 $z$
2. **MTPS + 层次化残差量化器** → 多尺度离散令牌集 $X$
3. **CAQ‑VAE 解码器** → 重建运动 $\hat{m}$（训练阶段）
4. **SAR Transformer** → 以文本条件 $c$ 为引导，自回归预测 $X$（生成阶段）
5. （可选）**运动编辑模块** → 通过 `MASK_edit` 令牌实现修复、扩展等任务，无需微调

CAQ‑VAE 与 SAR 的解耦设计使得运动表示学习与生成建模可以独立优化：前者通过混合卷积‑注意力架构（GroupNorm + SiLU + 自注意力）和非共享、逐层增大的码本提升重建质量与表示能力；后者借助尺度感知 RoPE 和交叉注意力文本融合，在仅 10 步推理内实现跨层一致的粗到细生成。

## 核心模块与公式推导

MoSa 的核心架构由三个关键模块构成：**多尺度令牌保留策略（MTPS）**、**可扩展自回归（SAR）建模**和**卷积-注意力混合 VQ-VAE（CAQ-VAE）**。这三个模块协同工作，解决了传统 VQ-GT 范式中跨层信息不对齐的根本瓶颈。

### 多尺度令牌保留策略（MTPS）

传统残差量化（RQ-VAE）在每一层独立进行量化，只保留当前尺度的令牌。MTPS 的核心创新在于：在每层残差量化**之前**对潜在向量进行下采样，量化**之后**再上采样恢复尺寸，从而显式保留粗到细的多尺度令牌集。

具体而言，对于第 $q$ 层的残差 $z^{(q)}$，MTPS 的操作定义为：

$$x^{(q)} = \operatorname{Quant}^{(q)}(\downarrow(z^{(q)}, s_q)), \quad \hat{z}^{(q)} = \uparrow(\operatorname{Dequant}^{(q)}(Z^{(q)}, x^{(q)}))$$

其中 $\downarrow(\cdot, s_q)$ 将潜在向量从精细尺度 $s_Q = T$ 下采样至目标尺度 $s_q$，$\uparrow(\cdot)$ 将量化后的表示上采样回原始尺寸以计算下一层残差。经过 $Q$ 层处理后，MTPS 保留的多尺度令牌集为：

$$X = \{ \underbrace{(x_1^1, \ldots, x_{s_1}^1)}_{x^{(1)}}, \ldots, \underbrace{(x_1^Q, \ldots, x_{s_Q}^Q)}_{x^{(Q)}} \}$$

其中 $s_1 < s_2 < \cdots < s_Q = T$，构成粗到细的层次结构。这一策略使得不同粒度的运动信息被显式编码为离散令牌，为后续的跨层联合建模提供了基础。

### 可扩展自回归（SAR）建模

传统自回归模型按时间步逐令牌分解序列概率：

$$p(x_1, \ldots, x_T \mid c) = \prod_{t=1}^T p(x_t \mid x_{<t}, c)$$

SAR 将这一范式扩展为**以尺度为步长**的分解。给定 MTPS 产生的多尺度令牌集，SAR 的联合概率定义为：

$$p(x^{(1)}, \ldots, x^{(Q)} \mid c) = \prod_{q=1}^Q p(x^{(q)} \mid x^{(1)}, \ldots, x^{(q-1)}, c)$$

每个推理步 $q$ 并行预测尺度 $s_q$ 内的所有令牌，总计仅需 $Q = 10$ 步（对比传统方法的 $T = 49$ 步）。训练时采用尺度感知的注意力掩码，确保 $x^{(q)}$ 只能关注 $x^{(\leq q)}$。此外，由于相邻尺度的令牌数量不同，前一层令牌 $x^{(q-1)}$ 需经过下采样-上采样操作以匹配当前尺度的维度后再输入 Transformer。

### 卷积-注意力混合 VQ-VAE（CAQ-VAE）

CAQ-VAE 对标准 VQ-VAE 架构进行了三项关键改进：

1. **残差块升级**：将标准残差块中的 ReLU 替换为 SiLU 激活函数，并使用 GroupNorm 替代 BatchNorm，提升训练稳定性。
2. **自注意力注入**：在卷积层之后引入自注意力层，捕获运动序列的全局时序依赖。
3. **量化特征归一化**：在码本量化时应用 $\ell_2$ 归一化，将欧氏距离转化为余弦相似度，显著提升码本利用率（从 88.9% 提升至 99.5%）。

VQ-VAE 的训练损失为：

$$\mathcal{L}_{\mathrm{vq}} = \| m - \hat{m} \|_1 + \| \operatorname{sg}[z] - \hat{z} \|_2 + \beta \| z - \operatorname{sg}[\hat{z}] \|_2$$

扩展到 $Q$ 层残差量化后，完整的 RVQ 训练目标为：

$$\mathcal{L}_{\mathrm{rvq}} = \| m - \hat{m} \|_1 + \sum_{q=1}^Q \left( \| \operatorname{sg}[z^{(q)}] - \hat{z}^{(q)} \|_2 + \beta \| z^{(q)} - \operatorname{sg}[\hat{z}^{(q)}] \|_2 \right)$$

消融实验证实了 CAQ-VAE 各组件的必要性：移除卷积-注意力混合模块后，HumanML3D 上的生成 FID 从 0.085 恶化至 0.150，重建 FID 从 0.030 升至 0.055；移除 $\ell_2$ 归一化后，生成 FID 升至 0.124。

### 辅助设计

- **非共享码本与线性增长**：CAQ-VAE 采用非共享码本以增强各层的表示能力，码本大小随层数线性增长，降低深层预测难度。
- **尺度感知 RoPE**：SAR Transformer 使用尺度感知的位置编码，将位置索引归一化至当前尺度 $s_q$，使模型感知不同尺度下的相对位置关系。消融实验表明，该策略在所有指标上优于标准 RoPE、Sinusoidal 和可学习位置编码。
- **运动编辑机制**：通过引入 `MASK_edit` 令牌，MoSa 无需微调即可支持运动修复、前后缀填充等编辑任务。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/003_Figure_3.jpg]]
*Figure 3: Previous VQ-VAE compared to our CAQ-VAE. Our CAQ-VAE uses residual blocks with GroupNorm and SiLU, along with a self-attention layer to capture global dependencies*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/007_Figure_6.jpg]]
*Figure 6: Visualization of the coarse-to-fine generation process. Starting at a coarse scale (3 tokens, Step 1) and progressively refined to a fine scale (49 tokens, Step 10). The final representation is achieved through dequantization and upsampling from the multi-scale token set and incremental accumulation into the VQ model for reconstruction*

## 实验与分析

### 主结果：文本到运动生成

MoSa在HumanML3D和Motion-X两个主流基准上均取得最优定量结果，并在推理效率上显著优于先前方法。TABLE I汇总了与代表性基线的全面对比。

在HumanML3D上，MoSa的FID降至**0.085**，相较MoMask的0.20（复现值0.172）大幅降低；R Precision Top-1达到**0.530**，MultiModal Dist降至**2.836**。在更大规模、更具挑战性的Motion-X数据集上，MoSa同样表现突出：FID达到**0.061**（MoMask为0.20），R Precision Top-1为**0.448**，MultiModal Dist为**2.982**。这些指标在95%置信区间内均显著优于包括**T2M-GPT**（Zhang et al., CVPR 2023）、**MLD**（Chen et al., CVPR 2023）、**MotionDiffuse**（Zhang et al., arXiv 2022）在内的扩散和自回归基线。

值得注意的是，推理效率的提升是MoSa的核心优势之一。由于SAR建模将推理步数从序列长度T（如49步）压缩为量化层数Q=10步，MoSa的平均推理时间降至**0.045秒**，相比MoMask的0.062秒**降低约27%**。这一加速直接源于方法设计：每步并行预测一个尺度的所有令牌，而非逐令牌串行生成。

为消除实现差异对公平比较的影响，作者对MoMask进行了复现，并将复现结果（TABLE I中标记为“†”）与论文报告值（灰色标注）一并呈现。相关差异已在GitHub issue #27中详细讨论。评估协议（数据集划分、评测代码）与MoMask等先前工作保持一致。

### 消融实验

#### CAQ-VAE架构消融

TABLE II系统验证了CAQ-VAE各设计组件的贡献。最关键的发现是**卷积-注意力混合模块**的必要性：移除该模块后，HumanML3D上的生成FID从0.085急剧恶化至**0.150**，重建FID也从0.030升至**0.055**。这表明标准残差块（ReLU激活）难以捕获运动序列中的全局依赖关系，而CAQ-VAE中引入的GroupNorm、SiLU激活和自注意力层对于学习高质量潜在表示至关重要。

**ℓ₂归一化**的消融同样揭示了其重要性。移除量化过程中的ℓ₂归一化后，生成FID升至**0.124**，更关键的是码本利用率从**99.5%骤降至88.9%**。ℓ₂归一化将欧氏距离转化为余弦相似度度量，有效防止了码本坍塌（codebook collapse），使码本向量得到更充分的利用。这一发现与VQ-VAE领域关于码本利用率的已知结论一致，但在运动生成的残差量化场景中得到了新的验证。

非共享码本与线性增长的码本大小设计进一步增强了表示容量。相比共享码本方案，这种分层差异化设计使各量化层能够专注于不同粒度的运动特征。

#### 多尺度令牌集大小Q的影响

Fig. 4展示了令牌集大小Q（即量化层数，也等于推理步数）对HumanML3D各指标的系统性影响。实验采用MoSa-mini配置，同时评估重建任务（VQ模型）和生成任务（Transformer）的性能。

结果表明，Q=6时尺度过于粗糙，无法充分保留运动细节；Q=15时虽然重建质量略有提升，但生成任务的FID和R Precision均出现退化，说明过多的尺度层级增加了Transformer的建模难度。**Q=10在所有指标上取得最佳平衡**，验证了默认配置的合理性。这一实验同时确认了推理步数从1到10时性能逐步提升的趋势（见Fig. 8），为粗到细生成策略提供了直接证据。

#### 位置编码与文本融合策略

TABLE III对比了不同位置编码和文本融合方法的影响。**尺度感知RoPE**在所有指标上一致优于标准RoPE、正弦位置编码和可学习位置编码。其核心机制是将位置索引按尺度进行归一化，使不同尺度的令牌在位置编码空间中保持一致的相对关系，这对于跨尺度的自回归预测尤为关键。

在文本融合方面，**交叉注意力**在FID、R Precision和MultiModal Dist上均优于前置法（prefix）和AdaIN。这一结果符合直觉：交叉注意力允许模型在每一层动态地关注文本条件的不同部分，而前置法和AdaIN仅在输入端或特征统计层面融合条件信息，表达能力受限。

### 粗到细生成特性的验证

Fig. 8展示了从推理步1到步10的逐步累积性能曲线。FID从初始的**23.92**（仅使用最粗尺度令牌重建）逐步降至最终的**0.085**，R Precision和MultiModal Dist也呈现单调改善趋势。这一曲线直观地证明了MoSa的粗到细生成特性：早期步提供运动的全局结构和粗粒度语义，后续步逐步补充细节，最终收敛到高质量运动。这种渐进式生成不仅提高了效率，还赋予了过程可解释性——Fig. 6的可视化进一步展示了从3个令牌到49个令牌的逐步细化过程。

### 失败模式与局限性

尽管MoSa在整体指标上表现优异，分析其边界情况有助于理解方法的适用范围：

1. **粗到细调度器的固定性**：当前调度器S（如3,6,10,...,49）是预定义的固定递增序列，无法根据运动类型或文本语义自适应调整。对于某些需要早期精细控制的运动类别，固定的粗阶段可能丢失关键细节，导致后续步骤难以弥补。

2. **并行预测的内存开销**：虽然推理步数降至10步，但每步需并行预测s_q个令牌（精细层可达49个），对GPU内存和计算的需求在极大规模部署时仍可能成为瓶颈，尤其是在生成长序列运动时。

3. **运动编辑缺乏定量评估**：运动编辑功能（Fig. 7）仅通过定性示例展示，缺乏标准化的定量指标和系统性鲁棒性测试。MASK_edit令牌在不同编辑子任务（修复、外推、自由补全）上的泛化性能有待进一步验证。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of the motion editing. Motion Editing encompasses a variety of sub-tasks, including motion inpainting, outpainting, prefix filling, suffix filling, and free-form motion completion. The input motion clips are highlighted in pink, and the generated motions are depicted in red. More results on motion editing are available on our project page*

4. **代码开源状态**：论文仅提供了项目页面和GitHub issue讨论，完整训练和推理代码尚未正式发布，部分实现细节（如CFG衰减策略的具体公式）需要从论文描述中推断。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/004_Table.jpg]]
*Table: I: Quantitative evaluation on the HumanML3D and Motion-X test set. ± indicates a 95% confidence interval. Blue and Red indicate the best and the second best result. ‘†’ denotes our reimplementation. The results of MoMask are slightly inconsistent with those reported in the paper (shown in gray). The relevant issue has been discussed in https://github.com/EricGuo5513/momask-codes/issues/27 as well as in *

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/008_Table.jpg]]
*Table: II: Ablation of our CAQ-VAE model and comparison of previous work on the HumanML3D and Motion-X datasets. The ablation study evaluates the effectiveness of the strategies proposed in IV-C. ‘†’ denotes our reimplementation, which are slightly inconsistent with the paper-reported results (shown in gray). The relevant issue has been discussed in https://github.com/EricGuo5513/momask-codes/issues/27*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/009_Table.jpg]]
*Table: III: We evaluate the impact of text fusion methods and position encoding (PE) strategies, including RoPE and our proposed Scale-wise RoPE. The result was evaluated using the HumanML3D test set*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/011_Figure_8.jpg]]
*Figure 8: Step-wise cumulative performance on HumanML3D. From inference steps 1 to 10, the metrics show a progressive improvement, indicating MoSa’s coarse-to-fine characteristics*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_01200/figures/005_Figure.jpg]]
*Figure: (b) MM-Dist↓ (a) FID↓*

## 方法谱系与知识库定位

### 在文本驱动运动生成谱系中的位置

MoSa 属于**基于矢量量化的离散令牌自回归生成**路线。该路线的前置范式中，**T2M-GPT**（Zhang et al., CVPR 2023）率先将 VQ-VAE 与自回归 transformer 结合，将连续运动映射为离散令牌后逐帧预测；**MoMask**（Guo et al., CVPR 2024）进一步引入层级残差量化和双 transformer 的 masked modeling，成为该路线在 MoSa 之前的最强基线。

与之平行的另一主流路线是**扩散模型**，包括 **MotionDiffuse**（Zhang et al., arXiv 2022）和 **MLD**（Chen et al., CVPR 2023）等，通过在连续潜在空间或原始运动空间进行去噪生成。此外，**TEMOS**（Petrovich et al., ECCV 2022）采用 VAE 框架，**MotionCLIP**（Tevet et al., ECCV 2022）引入 CLIP 跨模态对齐。MoSa 在 HumanML3D 和 Motion-X 上的 FID 分别达到 0.085 和 0.061，显著优于上述所有对比方法，确立了离散令牌自回归路线在生成质量上的新基准。

### 对瓶颈的突破机制

传统 VQ-GT 范式的核心瓶颈在于：残差量化的各层令牌在生成阶段被独立建模（如 MoMask 的双 transformer），导致跨层信息不对齐，损害运动的一致性和全局建模能力。MoSa 通过两个相互耦合的设计打破这一瓶颈：

1. **多尺度令牌保留策略（MTPS）**：在残差量化的每一层，先对潜在特征下采样至目标尺度 $s_q$，量化后再上采样恢复，从而保留从粗到细的 $Q$ 个尺度的离散令牌集 $X = \{x^{(1)}, \dots, x^{(Q)}\}$，尺度从 $s_1$ 递增至 $s_Q = T$（完整帧数）。这使得不同粒度的运动结构得以显式保留。

2. **可扩展自回归（SAR）建模**：将经典的自回归分解 $p(x_1, \dots, x_T|c) = \prod_{t=1}^T p(x_t | x_{<t}, c)$ 改造为以尺度为步长的分解 $p(x^{(1)}, \dots, x^{(Q)}|c) = \prod_{q=1}^Q p(x^{(q)} | x^{(1)}, \dots, x^{(q-1)}, c)$。单个 SAR transformer 联合建模所有尺度，每一步并行预测该尺度的全部 $s_q$ 个令牌，推理步数从序列长度 $T$（如 49 步）压缩至 $Q=10$ 步。

这一设计使生成过程天然具备**粗到细**的渐进特性：Fig. 8 的逐步累积实验表明，随着推理步数从 1 增加到 10，FID 从 23.92 单调降至 0.085，验证了跨层一致粗到细建模的有效性。

### 关键组件消融证据

- **CAQ-VAE 的卷积-注意力混合结构**：移除该模块后，HumanML3D 生成 FID 从 0.085 恶化至 0.150，重建 FID 从 0.030 升至 0.055（TABLE II），证实自注意力层对全局依赖建模的必要性。
- **$\ell_2$ 归一化**：移除后生成 FID 升至 0.124，码本利用率从 99.5% 降至 88.9%（TABLE II），表明余弦相似度量对码本学习至关重要。
- **尺度感知 RoPE**：在所有指标上优于标准 RoPE、Sinusoidal 和可学习位置编码（TABLE III），说明跨尺度的位置表征需要尺度归一化。
- **交叉注意力文本融合**：优于前置法（prefix）和 AdaIN（TABLE III），为多尺度令牌的条件注入提供了更有效的通道。
- **尺度数 $Q$ 的选择**：$Q=6$ 或 $Q=15$ 均损害生成质量，$Q=10$ 在所有指标上取得最佳平衡（Fig. 4）。

### 适用边界与局限

1. **调度器依赖预定义**：粗到细的尺度序列 $S = (s_1, s_2, \dots, s_Q)$ 是固定递增的（如 3, 6, 10, ...），未探索动态或学习得到的调度策略。不同运动类型（如精细手部动作 vs. 全身位移）可能受益于自适应的尺度分配。

2. **并行预测的内存-计算权衡**：虽然推理步数降至 10 步，但每步需并行预测 $s_q$ 个令牌，在极大规模（如超长序列或更大码本）下可能面临内存瓶颈。论文未提供不同序列长度下的显存占用分析。

3. **运动编辑缺乏定量评估**：MASK_edit 令牌机制在 inpainting、outpainting 等子任务上仅展示了定性示例（Fig. 7），缺少如编辑一致性、时序平滑性等定量指标，其鲁棒性和泛化性需要进一步验证。

4. **跨模态泛化未验证**：CAQ-VAE 的卷积-注意力混合结构和 MTPS 策略在图像、音频等其他矢量量化生成任务中的有效性尚未探索。

### 开放问题

- 多尺度令牌集的大小 $Q$ 和调度器 $S$ 能否根据文本语义或运动类型自适应调整，以在保持质量的同时进一步压缩推理成本？
- SAR 建模框架能否推广到超长运动序列（如数万帧）或其他时序数据模态（如视频、语音）的生成？
- 运动编辑中 MASK_edit 令牌的尺度一致性和编辑边界保持是否存在理论保证，是否有更优的编辑控制策略（如基于扩散的编辑）？
- 论文仅提供了项目页面和代码链接，完整训练与推理代码的开源状态尚不明确，社区复现和后续改进存在不确定性。

## 原文 PDF

![[paperPDFs/arxiv_2025/MoSa_Motion_Generation_with_Scalable_Autoregressive_Modeling.pdf]]
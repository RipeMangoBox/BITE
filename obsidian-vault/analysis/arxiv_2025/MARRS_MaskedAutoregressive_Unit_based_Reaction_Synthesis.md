---
title: "MARRS: Masked Autoregressive Unit-based Reaction Synthesis"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis.pdf
project_link: null
code_link: null
aliases:
- MARRS
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过采用无VQ的连续表征、将全身运动分解为身体和手部单元并独立编码、引入掩蔽自回归与扩散损失进行条件生成、以及启用自适应单元调制实现单元间的双向协调，从根本上解决了上述瓶颈。
primary_logic: 将全身运动分解为身体和手部单元，利用连续VAE独立编码，采用掩蔽自回归扩散框架，通过动作条件融合和自适应单元调制有效协调单元间信息，从而生成高质量、协调一致的人体反应运动。
claims:
- 在NTU120-AS在线无约束设置下，MARRS在训练条件FID（0.36）和测试条件FID（9.31）上大幅领先现有最优方法ReGenNet。
- 定量比较显示VQ-VAE和UD-VQ-VAE的重建与生成性能不佳，验证了连续VAE的必要性。
- 行动条件融合(ACF)在训练和测试条件下几乎所有指标均优于串联融合和协作Transformer。
- 双向自适应单元调制(AUM)在所有训练条件指标和测试条件FID/Acc上达到最佳。
---

# MARRS: Masked Autoregressive Unit-based Reaction Synthesis

> [!tip] 核心洞察
> 将全身运动分解为身体和手部单元，利用连续VAE独立编码，采用掩蔽自回归扩散框架，通过动作条件融合和自适应单元调制有效协调单元间信息，从而生成高质量、协调一致的人体反应运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | MARRS：基于掩蔽自回归单元的反应合成 |
| 英文题名 | MARRS: Masked Autoregressive Unit-based Reaction Synthesis |
| 会议/期刊 | arXiv 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MARRS |
| Dataset | NTU120-AS, Chi3D-AS |

> [!tip] 效果简介
> - NTU120-AS (online, unconstrained) 上，FID (train-conditioned) ↓ 0.36±0.02 vs 0.90±0.01 (ReGenNet) (↓0.54)；FID (test-conditioned) ↓ 9.31±0.36 vs 11.00±0.74 (ReGenNet) (↓1.69)；Accuracy (train-conditioned) ↑ 1.000±0.0000 vs 1.000±0.0000 (ReGenNet) (持平)。
> - NTU120-AS (offline) 上，FID ↓ 5.93±0.18 vs 6.19±0.33 (ReGenNet) (↓0.26)。
> - Chi3D-AS (online, unconstrained, train-cond) 上，FID ↓ 0.21±0.01 vs 0.28±0.01 (ReGenNet) (↓0.07)。

## 概要

人体动作-反应合成旨在根据一个人的动作（演员）生成另一个人的自然反应（反应者），在虚拟人交互、机器人协作等领域具有重要价值。然而，现有方法面临两个核心瓶颈：**其一**，基于向量量化（VQ）的方法存在量化信息丢失和码本利用率低的问题，限制了运动表征的精细度；**其二**，现有方法缺乏对身体和手部单元的相互感知，难以生成协调一致、细节丰富的全身反应运动。

针对上述问题，本文提出 **MARRS**（Masked Autoregressive Unit-based Reaction Synthesis），一个基于掩蔽自回归单元的反应合成框架。其核心思路是：**将全身运动分解为身体和手部两个独立单元**，采用无VQ的连续变分自编码器（UD-VAE）分别编码，从根本上避免量化信息损失；在此基础上，通过**掩蔽自回归扩散**范式进行条件生成，并引入**动作条件融合**（ACF）和**自适应单元调制**（AUM）实现演员-反应者之间以及身体-手部之间的双向信息协调。

在 NTU120-AS 在线无约束设置下，MARRS 在训练条件 FID（0.36）和测试条件 FID（9.31）上均显著领先现有最优方法 **ReGenNet**（Xu et al., CVPR 2024），同时在 Chi3D-AS 数据集上也取得了一致的性能优势。消融实验验证了连续 VAE 相较于 VQ-VAE 的必要性、身体-手部单元划分的合理性，以及 ACF 与双向 AUM 模块的关键作用。用户研究进一步表明，约 76% 的参与者认为 MARRS 生成的动作更自然，约 79% 认为物理真实感更强。

从方法谱系看，MARRS 融合了掩蔽自回归建模与扩散模型的优势，属于两阶段生成范式：第一阶段通过 UD-VAE 学习紧凑的连续运动表征，第二阶段在隐空间中以扩散损失驱动掩蔽 token 的自回归预测。相较于纯 VQ-VAE 方法（如 **MMM**）和纯扩散方法（如 **MDM**），MARRS 在生成质量与推理效率之间取得了更好的平衡。

人体运动生成是计算机视觉与图形学中的核心问题，其目标是根据给定的条件信号合成自然、协调的人体动作序列。其中，**人体反应合成**（Human Reaction Synthesis）聚焦于“动作-反应”交互场景：给定一个主动行为者（actor）的运动序列，系统需要生成一个被动反应者（reactor）的相应运动。这一任务在虚拟人交互、人机协作、AR/VR等领域具有重要应用价值，但其挑战性在于反应运动必须同时满足时间上的因果一致性、空间上的物理合理性，以及身体各部位之间的精细协调。

现有方法在解决这一问题时主要沿两条技术路线展开。一类方法基于**向量量化变分自编码器**（VQ-VAE），如 **MMM**（Pinyoanuntapong et al., 2024），通过将连续运动映射到离散码本进行掩蔽建模。另一类方法采用**扩散模型**直接生成运动序列，如 **MDM**（Tevet et al., 2022）和 **ReGenNet**（Xu et al., CVPR 2024），后者是当前人体动作-反应合成领域的最优方法。然而，这两类方法各自面临根本性的瓶颈。

**核心瓶颈**体现在两个层面。其一，基于VQ的方法存在**量化信息丢失**和**码本利用率低**的固有问题——将高维连续运动强制映射到有限离散码本的过程不可避免地损失运动细节，且码本中大量条目在训练中未被充分利用，导致重建与生成质量受限。定量证据表明，VQ-VAE及UD-VQ-VAE的重建与生成性能均不理想（Table 5）。其二，现有方法普遍将全身运动作为一个整体处理，**缺乏对身体和手部单元的相互感知**。手部运动（尤其是手指级精细动作）与身体运动在幅度、频率和语义上存在显著差异，统一建模难以同时捕捉两者的特性，导致生成的交互运动缺乏协调性，手部姿态和全局位移的精度不足。

上述瓶颈共同导致了现有方法在反应合成中的性能上限：**ReGenNet** 在 NTU120-AS 在线无约束设置下的测试条件 FID 为 11.00，距离真实运动分布仍有明显差距；手部运动的平均姿态误差（APE）和平均速度误差（AVE）也表明精细部位生成质量有待提升（Table 6）。

针对这些问题，**MARRS** 的动机在于从三个根本层面进行突破：（1）**抛弃离散量化**，采用连续VAE表征以避免信息损失；（2）**将全身运动分解为身体和手部两个独立单元**，分别编码以保留各自运动特性；（3）**引入掩蔽自回归与扩散损失的组合框架**，在条件生成过程中实现单元间的双向协调。这一设计思路的核心洞察是：通过“分而治之”的单元划分策略降低建模难度，再通过专门设计的融合与调制机制重建单元间的交互一致性，从而在保持生成多样性的同时大幅提升运动质量与协调性。

## 核心方法与创新机理

MARRS针对现有基于向量量化（VQ）的方法存在量化信息丢失和码本利用率低的问题，以及运动生成中身体与手部单元缺乏相互感知的瓶颈，提出了一套从表征、分解到交互的全链路创新方案。其核心创新可归纳为以下五个关键维度的“changed slots”：

### 1. 连续VAE替代向量量化（quantization_strategy）
现有方法普遍采用VQ-VAE将连续运动映射为离散码本索引，但量化过程不可避免地引入信息损失，且码本利用率低下。MARRS提出**UD-VAE（Unit-distinguished Motion VAE）**，完全摒弃量化操作，采用连续VAE对身体和手部单元分别编码为连续隐变量。消融实验（Table 5）直接验证了这一决策的正确性：VQ-VAE和UD-VQ-VAE的重建与生成FID均显著劣于连续VAE方案，而直接用L2损失替代扩散损失更导致测试条件FID从9.31急剧恶化至15.95，表明连续表征与扩散损失的组合是性能提升的基石。

### 2. 身体-手部单元分解（unit_division）
不同于以往将全身作为单一整体或按上下半身/六单元划分的策略，MARRS将全身运动分解为**身体（body）**和**手部（hands）**两个独立单元。Table 2的消融表明，这一划分方式在测试条件FID上达到最优（9.31），显著优于无划分（10.12）、上下半身划分（9.59）和六单元划分（9.86）。其因果机制在于：身体和手部在反应生成中具有不同的运动特性和时间尺度，独立编码使模型能够分别捕获各自的精细模式，同时通过后续的单元调制实现双向协调。

### 3. 动作条件融合（actor_reactor_fusion）
反应者如何有效获取演员的运动信息是反应生成的核心挑战。MARRS提出**动作条件融合（ACF）**模块：首先对演员token进行自注意力精炼（Eq. 3），对掩蔽后的反应者token同样进行自注意力处理（Eq. 4），随后通过交叉注意力将演员信息融入反应者token（Eq. 5）。Table 3的消融显示，ACF在训练和测试条件下几乎所有指标均优于ReGenNet的串联融合（Concatenate Fuse）和InterGen的协作Transformer（Cooperative Transformer），证明了交叉注意力融合机制在信息传递效率上的优势。

### 4. 自适应单元调制（unit_interaction）
身体与手部单元之间的信息交互是生成协调一致反应的关键。MARRS设计了**自适应单元调制（AUM）**，通过双向的scale和shift操作实现单元间的相互调制：身体信息通过线性层生成缩放和偏移参数，对手部嵌入进行调制（Eq. 6-7），反之亦然（Eq. 8-9）。Table 4的消融表明，双向AUM在所有训练条件指标和测试条件FID/Acc上均达到最佳，显著优于无通信、ParCo的协调层以及单向传递方案，验证了双向自适应调制在协调身体与手部运动中的核心作用。

### 5. 掩蔽自回归扩散生成范式（generation_paradigm + loss_function）
MARRS采用**掩蔽自回归（Masked Autoregressive）**与**扩散损失**相结合的两阶段生成范式：在第一阶段，UD-VAE将运动编码为连续token；在第二阶段，以自回归方式逐步生成反应token，每一步通过紧凑的MLP去噪器（仅3层MLP）进行扩散去噪。扩散损失（Eq. 11）同时作用于身体和手部token，替代了传统的L2重建损失。这一设计使得MARRS兼具自回归模型的高效推理（MARRS-Tiny推理仅需0.039s，快于ReGenNet的0.058s）和扩散模型的高质量生成能力，从根本上突破了VQ-VAE方法的性能上限。

MARRS 采用两阶段训练范式，将人体反应运动生成分解为**单元区分运动表征学习**与**掩蔽反应生成**两个核心阶段，其整体框架如图2所示。

**第一阶段：单元区分运动VAE（UD-VAE）**

该阶段的核心任务是将全身运动压缩为紧凑的连续隐变量表征，同时避免传统向量量化（VQ）带来的信息丢失问题。具体而言，MARRS 将全身运动显式拆分为**身体（body）**和**手部（hands）**两个独立单元，并为每个单元分别训练一个变分自编码器（VAE）。身体单元和手部单元的编码器各自将对应部分的运动序列 $x_k^{1:N}$（动作）与 $y_k^{1:N}$（反应）映射为连续的隐变量令牌，解码器则负责从隐变量重建原始运动。该阶段的优化目标为 SmoothL1 重建损失：

$$\mathcal{L}_{VAE}^{k} = \mathrm{SmoothL1}(\hat{x}_{k}^{1:N}, x_{k}^{1:N}) + \mathrm{SmoothL1}(\hat{y}_{k}^{1:N}, y_{k}^{1:N})$$

其中 $k \in \{b, h\}$ 分别代表身体和手部单元。UD-VAE 的连续表征设计是方法的关键前提——消融实验（Table 5）证实，基于VQ-VAE或UD-VQ-VAE的变体在重建与生成FID上均显著劣于连续VAE方案，验证了去除量化操作的必要性。

**第二阶段：掩蔽反应生成模型**

在获得单元隐变量后，第二阶段以演员（actor）的运动令牌为条件，通过掩蔽自回归扩散框架生成反应者（reactor）的运动令牌。该阶段包含三个核心模块的串行协作：

1. **动作条件融合（ACF）**：首先对演员的身体令牌进行自注意力精炼 $Y_{b}^{\prime} = \mathrm{Attn}(Y_{b}, Y_{b}, Y_{b})$，同时对随机掩蔽后的反应者令牌进行自注意力编码 $\hat{X}_{b}^{\prime} = \mathrm{Attn}(\hat{X}_{b}, \hat{X}_{b}, \hat{X}_{b})$。随后通过交叉注意力将演员信息融入反应者表征：$\hat{X}_{b}^{fusion} = \mathrm{Attn}(\hat{X}_{b}^{\prime}, Y_{b}^{\prime}, Y_{b}^{\prime})$。手部单元采用相同的对称操作。ACF 的随机掩蔽策略使模型在训练中学会从部分可见令牌预测完整反应，从而在推理时支持自回归生成。

2. **自适应单元调制（AUM）**：为协调身体与手部单元的生成，AUM 实现双向信息传递。身体融合令牌 $\hat{X}_{b}^{fusion}$ 通过线性层预测缩放与偏移参数，对手部令牌进行特征调制：$scale_{b}, shift_{b} = \mathrm{Linear}(\hat{X}_{b}^{fusion})$，$\hat{X}_{h}^{final} = scale_{b} \cdot \mathrm{LN}(\hat{X}_{h}^{fusion}) + shift_{b}$。对称地，手部信息也以相同机制反哺身体令牌。消融实验（Table 4）表明，双向AUM在所有训练条件指标及测试条件FID/准确率上均优于无通信、协调层及单向传递方案。

3. **紧凑扩散去噪**：经ACF与AUM处理后的令牌作为条件 $z_b, z_h$，输入到仅由3层MLP构成的紧凑扩散模型中进行去噪。训练时对令牌施加噪声 $x_b^t = \sqrt{\bar{\alpha}_t}\bar{x}_b + \sqrt{1-\bar{\alpha}_t}\epsilon_1$，扩散损失为身体和手部两个分支的噪声预测均方误差之和：

$$\mathcal{L}(\boldsymbol{x} \mid \boldsymbol{z}) = \mathbb{E}_{\boldsymbol{\varepsilon}_1, t}\left[||\boldsymbol{\epsilon}_1 - \boldsymbol{\epsilon}_{\theta_1}(\boldsymbol{x}_b^t \mid t, \boldsymbol{z}_b)||^2\right] + \mathbb{E}_{\boldsymbol{\varepsilon}_2, t}\left[||\boldsymbol{\epsilon}_2 - \boldsymbol{\epsilon}_{\theta_2}(\boldsymbol{x}_h^t \mid t, \boldsymbol{z}_h)||^2\right]$$

**推理流程**

推理时，MARRS 以自回归方式逐令牌生成反应序列：每个位置的身体和手部令牌通过迭代去噪步骤 $x_{n}^{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_{n}^{t} - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta}(x_{n}^{t} | t, z_{n}) \right) + \sigma_t \epsilon$ 从纯噪声逐步还原，最终由UD-VAE解码器将令牌序列转换回人体运动。得益于紧凑的MLP去噪器设计，MARRS-Tiny的推理速度（0.039s）显著快于ReGenNet（0.058s），而模型规模扩展（Tiny→Base）可进一步将测试条件FID从10.55降至9.31（Table 9）。

**输入输出规范**

- **输入**：演员的全身运动序列（SMPL-X参数表示），按身体和手部单元拆分后分别编码为隐变量令牌。
- **输出**：反应者的全身运动序列，由UD-VAE解码器从生成的身体和手部令牌重建。
- **条件信号**：演员令牌通过ACF的交叉注意力机制注入反应生成过程，AUM则在单元间建立双向协调通道。

MARRS 的核心架构由两大阶段构成：第一阶段为**单元区分运动变分自编码器（UD‑VAE）**，负责将全身运动压缩为连续隐变量；第二阶段为**掩蔽反应生成模型**，通过动作条件融合（ACF）、自适应单元调制（AUM）以及紧凑扩散去噪头，在隐空间中自回归地生成反应运动。

### 单元区分运动变分自编码器（UD‑VAE）

传统基于向量量化（VQ‑VAE）的方法存在量化信息丢失与码本利用率低的固有问题（Table 5 证实 VQ‑VAE 及 UD‑VQ‑VAE 的重建与生成性能均不理想）。MARRS 摒弃量化操作，转而采用连续 VAE，并将全身运动显式分解为**身体单元**和**手部单元**，分别由独立的 VAE 进行编码与解码（Figure 2‑a）。

对于第 $k$ 个单元（$k \in \{\text{body}, \text{hands}\}$），UD‑VAE 的优化目标为 Smooth L1 重建损失：

$$
\mathcal{L}_{VAE}^{k} = \mathrm{SmoothL1}(\hat{x}_{k}^{1:N}, x_{k}^{1:N}) + \mathrm{SmoothL1}(\hat{y}_{k}^{1:N}, y_{k}^{1:N}) \tag{1}
$$

其中 $x_{k}^{1:N}$ 与 $y_{k}^{1:N}$ 分别为该单元的动作与反应运动序列真值，$\hat{x}_{k}^{1:N}$ 与 $\hat{y}_{k}^{1:N}$ 为对应的 VAE 重建结果，$N$ 为序列长度。该损失同时约束动作与反应的重建，确保隐空间对两类运动均具有高保真表达能力。消融实验（Table 2）进一步表明，将全身划分为身体与手部两个单元（Body & Hands）在测试条件 FID 上达到最优（9.31），显著优于无划分、上下半身划分以及 6 单元划分策略。

### 掩蔽反应生成模型

第二阶段的核心任务是在给定演员运动隐变量 $\boldsymbol{z}$ 的条件下，自回归地生成反应者运动令牌序列。该模型由三个关键模块串联而成：动作条件融合（ACF）、自适应单元调制（AUM）以及扩散去噪头。

#### 动作条件融合（ACF）

ACF 通过交叉注意力机制将演员运动信息注入掩蔽后的反应者令牌。首先定义缩放点积注意力：

$$
\mathrm{Attn}(\mathrm{Q}, \mathrm{K}, \mathrm{V}) = \mathrm{softmax}\left(\frac{(\mathrm{QW}^{\mathrm{Q}}) \cdot (\mathrm{KW}^{\mathrm{K}})^{T}}{\sqrt{C}}\right) \cdot (\mathrm{VW}^{\mathrm{V}}) \tag{2}
$$

其中 $\mathrm{W}^{\mathrm{Q}}, \mathrm{W}^{\mathrm{K}}, \mathrm{W}^{\mathrm{V}}$ 为可训练权重矩阵，$C$ 为通道维度。以身体单元为例，ACF 的执行流程如下：

1. **演员自注意力精炼**：对演员身体令牌 $Y_b$ 进行自注意力，提取紧凑的演员表征：
   $$Y_{b}^{\prime} = \mathrm{Attn}(Y_{b}, Y_{b}, Y_{b}) \tag{3}$$

2. **反应者自注意力**：对随机掩蔽后的反应者身体令牌 $\hat{X}_{b}$ 进行自注意力：
   $$\hat{X}_{b}^{\prime} = \mathrm{Attn}(\hat{X}_{b}, \hat{X}_{b}, \hat{X}_{b}) \tag{4}$$

3. **交叉注意力融合**：以反应者令牌为查询、演员精炼表征为键和值，实现信息注入：
   $$\hat{X}_{b}^{fusion} = \mathrm{Attn}(\hat{X}_{b}^{\prime}, Y_{b}^{\prime}, Y_{b}^{\prime}) \tag{5}$$

手部单元采用完全对称的操作。Table 3 的消融实验表明，ACF 在训练与测试条件下的几乎所有指标上均优于 ReGenNet 的 Concatenate Fuse 和 InterGen 的 Cooperative Transformer，验证了交叉注意力融合机制的有效性。

#### 自适应单元调制（AUM）

身体与手部运动在物理上高度耦合，但 UD‑VAE 将其独立编码，因此需要在生成阶段重建单元间的协调关系。AUM 通过双向的缩放-偏移（scale‑shift）调制实现这一目标：

**身体→手部调制**：利用融合后的身体令牌 $\hat{X}_{b}^{fusion}$ 生成调制参数，作用于手部令牌：
$$scale_{b}, shift_{b} = \mathrm{Linear}(\hat{X}_{b}^{fusion}) \tag{6}$$
$$\hat{X}_{h}^{final} = scale_{b} \cdot \mathrm{LN}(\hat{X}_{h}^{fusion}) + shift_{b} \tag{7}$$

**手部→身体调制**：对称地，利用手部令牌调制身体令牌：
$$scale_{h}, shift_{h} = \mathrm{Linear}(\hat{X}_{h}^{fusion}) \tag{8}$$
$$\hat{X}_{b}^{final} = scale_{h} \cdot \mathrm{LN}(\hat{X}_{b}^{fusion}) + shift_{h} \tag{9}$$

其中 $\mathrm{LN}$ 为层归一化。Table 4 的消融实验证实，双向 AUM 在所有训练条件指标及测试条件 FID、Acc 上均优于无通信、ParCo 的协调层以及单向信息传递，是协调身体与手部运动的关键设计。

#### 扩散去噪损失

MARRS 不直接回归令牌值，而是采用掩蔽自回归扩散范式：对目标令牌施加前向噪声过程后，由紧凑 MLP 去噪头预测所加噪声。前向过程定义为：

$$x_b^t = \sqrt{\bar{\alpha}_t} \, \bar{x}_b + \sqrt{1-\bar{\alpha}_t} \, \epsilon_1, \quad x_h^t = \sqrt{\bar{\alpha}_t} \, x_h + \sqrt{1-\bar{\alpha}_t} \, \epsilon_2 \tag{10}$$

其中 $\bar{\alpha}_t$ 为噪声调度参数，$\epsilon_1, \epsilon_2 \sim \mathcal{N}(0, I)$。训练损失为两个单元的去噪均方误差之和：

$$
\mathcal{L}(\boldsymbol{x} \mid \boldsymbol{z}) = \mathbb{E}_{\boldsymbol{\varepsilon}_1, t}\left[||\boldsymbol{\epsilon}_1 - \boldsymbol{\epsilon}_{\theta_1}(\boldsymbol{x}_b^t \mid t, \boldsymbol{z}_b)||^2\right] + \mathbb{E}_{\boldsymbol{\varepsilon}_2, t}\left[||\boldsymbol{\epsilon}_2 - \boldsymbol{\epsilon}_{\theta_2}(\boldsymbol{x}_h^t \mid t, \boldsymbol{z}_h)||^2\right] \tag{11}
$$

其中 $\boldsymbol{\epsilon}_{\theta_1}$ 和 $\boldsymbol{\epsilon}_{\theta_2}$ 分别为身体和手部单元的紧凑 MLP 去噪网络（仅 3 层），以时间步 $t$ 和条件令牌 $\boldsymbol{z}_b, \boldsymbol{z}_h$ 为输入。Table 5 的消融实验表明，使用扩散损失替代直接 L2 回归损失至关重要：L2 损失导致测试条件 FID 从 9.31 急剧恶化至 15.95。

### 推理过程

推理时，MARRS 以自回归方式逐令牌生成反应序列。对于每个待生成的令牌 $x_n$，从纯噪声出发，通过条件去噪步迭代去噪：

$$x_{n}^{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_{n}^{t} - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_{\theta}(x_{n}^{t} \mid t, z_{n}) \right) + \sigma_t \epsilon \tag{12}$$

去噪完成后，令牌经 UD‑VAE 解码器还原为运动序列。由于去噪头仅由 3 层 MLP 构成，MARRS 在保持高质量生成的同时实现了快速推理（MARRS‑Tiny 推理耗时 0.039s，快于 ReGenNet 的 0.058s，Table 9）。

## 实验与关键发现

### 主实验结果

MARRS 在两个主流人体动作-反应合成基准上进行了全面评估，均采用在线无约束（online, unconstrained）设定，与现有最优方法 **ReGenNet**（Xu et al., CVPR 2024）进行对比。

**NTU120-AS 数据集**：如 Table 1 所示，MARRS 在训练条件（train-conditioned）下取得了 FID 0.36±0.02，较 ReGenNet 的 0.90±0.01 大幅降低 0.54；在更具挑战性的测试条件（test-conditioned）下，FID 达到 9.31±0.36，较 ReGenNet 的 11.00±0.74 降低 1.69。训练条件下的动作识别准确率（Acc）两者均达到 1.000，多样性（Div）与多模态（MultiMod）指标亦保持竞争力。

**Chi3D-AS 数据集**：如 Table 8 所示，MARRS 在训练条件 FID 上取得 0.21±0.01（ReGenNet 为 0.28±0.01），测试条件 FID 为 18.94±2.21（ReGenNet 为 21.24±3.42），进一步验证了方法的跨数据集泛化能力。

**离线设置**：在 NTU120-AS 离线（offline）设定下（Table 7），MARRS 的 FID 为 5.93±0.18，略优于 ReGenNet 的 6.19±0.33，表明方法在不同交互模式下均具有鲁棒性。

**手部与全局位移精度**：Table 6 展示了手部姿态及全局位移的定量对比，MARRS 在 MPJPE 等指标上优于 ReGenNet，证实了身体-手部分解策略对精细运动建模的有效性。

### 消融实验

所有消融实验均在 NTU120-AS 在线无约束设定下进行。

**单元划分策略（Table 2）**：将全身划分为身体和手部两个单元（Body & Hands）在测试条件 FID（9.31）上最优。相比之下，无划分（whole-body）策略、上半身/下半身划分（Upper & Lower，源自 SCA, Ghosh et al. 2021）以及 6 单元划分（6-Unit Division，源自 ParCo, Zou et al. 2024）均在测试条件 FID 上表现更差，验证了“身体+双手”分解对反应生成的关键作用。

**动作条件融合模块 ACF（Table 3）**：所提出的 ACF 在训练和测试条件下几乎所有指标均优于两种基线融合策略——ReGenNet 的串联融合（Concatenate Fuse）和 InterGen（Liang et al. 2024）的协作 Transformer（Cooperative Transformer）。这表明通过交叉注意力将演员运动信息选择性注入掩蔽的反应者 token，比直接拼接或对称 Transformer 交互更有效。

**自适应单元调制 AUM（Table 4）**：双向 AUM 在所有训练条件指标及测试条件 FID、Acc 上达到最佳。消融对比包括：无单元通信（w.o. Unit Communication）、ParCo（Zou et al. 2024）的协调层（Coordination Layer），以及单向信息传递（Hands → Body / Body → Hands）。结果表明，身体与手部之间的双向自适应调制是生成协调一致反应运动的核心机制。

**生成框架对比（Table 5）**：
- **连续 VAE vs. 向量量化**：基于 VQ-VAE（MMM, Pinyoanuntapong et al. 2024）和 UD-VQ-VAE 的重建与生成 FID 均显著劣于连续 UD-VAE，验证了避免量化信息丢失的必要性。
- **扩散损失 vs. L2 损失**：将扩散损失替换为直接 L2 损失后，测试条件 FID 从 9.31 急剧恶化至 15.95，证明扩散损失对高质量生成不可或缺。
- **与其他生成范式对比**：基于 VAE 的 ACTOR（Petrovich, Black, and Varol 2021）和自回归扩散方法 AMDM（Shi et al. 2024）在 FID 上均不及 MARRS。

**模型规模缩放（Table 9）**：增大模型尺寸可稳步提升 FID（MARRS-Tiny 10.55 → MARRS-Base 9.31），且 MARRS-Tiny 的推理速度（0.039s）快于 ReGenNet（0.058s），表明方法在效率与性能之间取得了良好平衡。

### 定性分析与用户研究

**定性对比**：Figure 3 和 Figure 5 展示了 MARRS 与 ReGenNet 的生成序列对比。MARRS 生成的反应动作与演员动作在时序和空间上更为一致，尤其在涉及手部交互的场景中优势明显。

**用户研究（Figure 6）**：在自然度（Naturalness）、流畅度（Smoothness）和物理真实感（Physical realism）三项主观指标上，约 76% 的参与者认为 MARRS 动作更自然，约 74% 认为更流畅，约 79% 认为物理真实感更强。

### 失败模式与局限性

尽管 MARRS 在定量和定性评估中均表现优异，论文明确指出以下局限性：
- **脚部滑动**：生成的运动会存在轻微的脚部滑动伪影，这一问题尚未得到充分探索和解决。
- **细粒度接触精度**：受限于数据集标注精度，某些精细运动（如手指接触）的生成不够精准。
- **数据集规模**：目前仅在 NTU120-AS 和 Chi3D-AS 上验证，缺乏更大规模、高质量的人类反应数据集以进一步测试泛化性。

### 重要图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | MARRS 在 NTU120-AS 在线无约束设定下全面超越 ReGenNet，训练/测试 FID 分别降低 0.54/1.69 |
| Table 2 | “身体+双手”单元划分在测试条件 FID 上最优 |
| Table 3 | ACF 融合策略优于串联融合和协作 Transformer |
| Table 4 | 双向 AUM 是单元间协调的关键，优于无通信和单向传递 |
| Table 5 | 连续 VAE + 扩散损失是性能基石；VQ-VAE 和 L2 损失均导致显著性能下降 |
| Table 9 | 模型可扩展且推理高效，MARRS-Tiny 速度已快于 ReGenNet |
| Figure 6 | 用户研究显示 MARRS 在自然度、流畅度、物理真实感上均获多数偏好 |

![[assets/figures/papers/paper_list_l1692_MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis/figures/003_Table_1.jpg]]
*Table 1: Comparison to state-of-the-arts on the online, unconstrained setting for human action-reaction synthesis on NTU120- AS (Xu et al. 2024). ± indicates 95% confidence interval, → means that closer to Real is better. Bold indicates best result and underline indicates second best*

![[assets/figures/papers/paper_list_l1692_MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis/figures/004_Table_2.jpg]]
*Table 2: Ablation studies on the Unit Division*

![[assets/figures/papers/paper_list_l1692_MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis/figures/006_Table_3.jpg]]
*Table 3: Ablation studies on Action-Conditioned Fusion (ACF). “Concatenate Fuse” is a method proposed by ReGenNet (Xu et al. 2024) for a reactor to get information from an actor. “Cooperative Transformer” is a transformer structure designed by InterGen (Liang et al. 2024). Our approach achieves SoTA on almost all metrics*

![[assets/figures/papers/paper_list_l1692_MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis/figures/007_Table_4.jpg]]
*Table 4: Ablation studies on Adaptive Unit Modulation (AUM). “w.o. Unit Communication” indicates that the body and hands branches do not interact with each other. “Coordination Layer” is a method proposed by ParCo (Zou et al. 2024) for transferring information between different units. “Hands → Body” and “Body → Hands” represent a unidirectional transfer of information between units. Our approach achieves SoTA on almost all metrics*

![[assets/figures/papers/paper_list_l1692_MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis/figures/008_Table_5.jpg]]
*Table 5: Ablation studies on different framework. “VQ-VAE” is based on MMM (Pinyoanuntapong et al. 2024)*

![[assets/figures/papers/paper_list_l1692_MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis/figures/014_Table_9.jpg]]
*Table 9: Model scaling results and comparison of computational complexity. Our proposed MARRS can converge faster in the training process than ReGenNet (Xu et al. 2024) and enlarging the model size can enhance the overall generation performance*

## 定位与知识库关联

### 1. 方法谱系：从 VQ-VAE 到掩蔽自回归扩散

MARRS 的核心贡献在于对现有动作-反应生成范式进行了系统性重构，其方法谱系可沿着三个关键维度展开：

**生成范式演进：VQ-VAE → 扩散 → 掩蔽自回归扩散。** 早期人体运动生成广泛采用基于向量量化（VQ-VAE）的框架，如 **MMM**（Pinyoanuntapong et al., 2024），通过离散码本将运动序列压缩为离散 token 后以自回归方式生成。然而，定量消融（Table 5）表明，VQ-VAE 在重建和生成 FID 上表现不佳，其变体 UD-VQ-VAE（将单元划分引入 VQ 框架）同样未能解决量化信息丢失和码本利用率低的固有问题。纯扩散方法如 **MDM**（Tevet et al., 2022）虽在文本到动作生成中取得突破，但直接应用于反应合成时面临条件建模效率不足的问题。**AMDM**（Shi et al., 2024）尝试将自回归与扩散结合，但其生成质量仍受限于框架设计。MARRS 的创新在于将掩蔽自回归（Masked Autoregressive）与紧凑扩散损失深度融合：第一阶段用连续 VAE（UD-VAE）将运动编码为连续隐变量，避免量化瓶颈；第二阶段以随机掩蔽的自回归方式生成 token，并用仅含 3 层 MLP 的紧凑扩散模型（Diffusion MLP）进行去噪，在保持推理速度（MARRS-Tiny 仅需 0.039s，快于 ReGenNet 的 0.058s，Table 9）的同时大幅提升生成质量。

**条件融合机制：简单拼接 → 交叉注意力融合。** 在如何将演员（actor）运动信息传递给反应者（reactor）这一关键问题上，现有方法主要采用两种策略：**ReGenNet**（Xu et al., CVPR 2024）提出的 Concatenate Fuse 将演员与反应者特征直接拼接后送入 Transformer；**InterGen**（Liang et al., 2024）设计的 Cooperative Transformer 通过协作注意力实现多人运动生成。Table 3 的消融实验显示，MARRS 提出的 Action-Conditioned Fusion（ACF）在训练和测试条件下几乎所有指标均优于上述两种方案。ACF 的核心机制是：先对演员 token 进行自注意力精炼（Eq. 3），再对随机掩蔽后的反应者 token 进行自注意力（Eq. 4），最后通过交叉注意力将精炼后的演员信息融入反应者 token（Eq. 5）。这种“先精炼后融合”的设计使得反应者能更精准地捕捉演员动作中的关键语义信息。

**单元间协调：无通信 → 双向自适应调制。** 将全身运动分解为多个独立单元后，如何协调各单元间的信息交互是决定生成质量的关键。**ParCo**（Zou et al., 2024）提出了 Coordination Layer 用于不同单元间的信息传递，但其设计为单向或简单的特征混合。Table 4 的消融实验表明，MARRS 提出的 Adaptive Unit Modulation（AUM）在所有训练条件指标和测试条件 FID/Acc 上均达到最优。AUM 采用双向调制机制：身体单元的融合特征通过线性层生成 scale 和 shift 参数，对手部单元进行自适应调制（Eq. 6-7）；同时手部单元也对称地调制身体单元（Eq. 8-9）。这种双向、自适应的信息交互使得身体和手部能够相互感知对方状态，从而生成协调一致的全身体动作。

### 2. 知识库定位：填补量化-连续鸿沟与单元感知空白

MARRS 在知识体系中的核心定位是**弥合了 VQ 离散表征与扩散连续生成之间的范式鸿沟**，同时**首次在反应生成中引入了单元间的相互感知机制**。

**与 VAE 基线的对比。** **cVAE**（Kingma & Welling, 2013）和 **ACTOR**（Petrovich, Black, and Varol, 2021）作为 VAE 类方法的代表，在动作条件运动生成中展现了潜力，但其生成多样性（Div）和物理真实感受限于 VAE 的先验假设。Table 5 显示，ACTOR 的生成 FID 显著劣于 MARRS。

**与扩散基线的对比。** **AGRoL**（Du et al., 2023）和 **MDM-GRU**（Tevet et al., 2022 的 GRU 变体）作为扩散方法的代表，在运动生成质量上较 VAE 有提升，但未针对反应生成的单元分解和条件融合进行专门设计。MARRS 通过 UD-VAE 的单元独立编码和 ACF/AUM 的条件协调机制，在 FID 指标上实现了对 ReGenNet（当前 SOTA）的大幅超越：训练条件 FID 从 0.90 降至 0.36（↓0.54），测试条件 FID 从 11.00 降至 9.31（↓1.69），如 Table 1 所示。

**跨数据集泛化能力。** MARRS 在 NTU120-AS 离线设置（Table 7，FID 5.93 vs ReGenNet 6.19）和 Chi3D-AS 在线无约束设置（Table 8，测试条件 FID 18.94 vs ReGenNet 21.24）上均保持领先，验证了方法的跨数据集鲁棒性。

### 3. 适用边界与局限

**数据依赖与泛化边界。** 当前验证仅覆盖 NTU120-AS 和 Chi3D-AS 两个数据集，受限于高质量人体反应数据的稀缺性，方法在更复杂交互场景（如多人、密集接触）下的表现尚未验证。此外，数据集精细标注精度的不足导致某些细粒度运动（如手指接触）的生成不够精准。

**物理真实感缺陷。** 生成的运动会存在轻微的脚部滑动（foot sliding）问题，这是当前运动生成领域的共性挑战，MARRS 尚未对此进行专门建模或后处理优化。

**计算-质量权衡。** 虽然 MARRS-Tiny 在推理速度上优于 ReGenNet，但增大模型尺寸（Table 9，Tiny → Base）虽能稳步提升 FID（10.55 → 9.31），也会增加计算开销，需要在部署时根据场景需求进行权衡。

### 4. 开放问题与未来方向

1. **多主体扩展。** 当前框架设计针对双人交互（actor-reactor），如何将掩蔽自回归扩散框架扩展至三个及以上交互主体的多人场景，需要重新设计条件融合和单元协调机制。

2. **物理约束集成。** 消除脚部滑动等物理伪影可能需要引入显式的物理约束（如接触力、地面反作用力）或后处理优化模块，而非仅依赖数据驱动的生成。

3. **更大规模预训练。** 在更大规模、更高质量的人体交互数据集上，MARRS 的连续 VAE + 掩蔽自回归扩散范式能否进一步提升精细度与泛化性，是一个值得探索的方向。

4. **跨任务迁移。** 该框架的核心组件（单元分解、掩蔽自回归、紧凑扩散）是否可迁移至其他条件驱动的运动生成任务，如语音或音乐引导的手势合成，目前仍是开放问题。

## 原文 PDF

![[paperPDFs/arxiv_2025/MARRS_MaskedAutoregressive_Unit_based_Reaction_Synthesis.pdf]]

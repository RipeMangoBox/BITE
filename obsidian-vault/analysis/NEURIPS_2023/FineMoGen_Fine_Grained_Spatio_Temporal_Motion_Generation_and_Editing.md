---
title: "FineMoGen: Fine-Grained Spatio-Temporal Motion Generation and Editing"
type: paper
paper_level: A
venue: NEURIPS
year: 2023
pdf_ref: paperPDFs/NEURIPS_2023/FineMoGen_Fine_Grained_Spatio_Temporal_Motion_Generation_and_Editing.pdf
aliases:
- FineMoGen
tags:
- NEURIPS_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 时空混合注意力（SAMI）机制：通过显式建模空间独立性和时间独立性，并引入稀疏激活的混合专家（MoE），使模型能够分别处理不同身体部位和时间段的细粒度约束。
primary_logic: 将注意力机制中的全局模板沿空间（身体部位）和时间（运动阶段）解耦，能够显式组合细粒度条件，从而实现可控且自然的运动生成。
claims:
- FineMoGen在BABEL和HuMMan-MoGen上的时序组合准确率显著超过现有方法，零样本下BABEL RPrecision达到0.51。
- 消融实验表明，同时引入时序独立性和MoE的完整FineMoGen在HuMMan-MoGen上的RPrecision（0.41）远高于基线（0.24）。
- 在空间组合任务中，FineMoGen的RPrecision（0.51）和FID（1.09）均显著优于基线（RPrecision 0.43, FID 2.87）。
- HuMMan-MoGen (Spatial Composition) 上 RPrecision↑ = 0.51
---

# FineMoGen: Fine-Grained Spatio-Temporal Motion Generation and Editing

> [!tip] 核心洞察
> 将注意力机制中的全局模板沿空间（身体部位）和时间（运动阶段）解耦，能够显式组合细粒度条件，从而实现可控且自然的运动生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | FineMoGen：细粒度时空运动生成与编辑 |
| 英文题名 | FineMoGen: Fine-Grained Spatio-Temporal Motion Generation and Editing |
| 会议/期刊 | NEURIPS 2023 |
| Links | [paper](https://arxiv.org/abs/2312.15004) · [Project](https://mingyuan-zhang.github.io/projects/FineMoGen.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FineMoGen |
| Dataset | HuMMan-MoGen, HumanML3D, BABEL |

> [!tip] 效果简介
> - HuMMan-MoGen (Spatial Composition) 上，RPrecision↑ 0.51 vs 0.43 (Baseline w/o SAMI) (+0.08)；FID↓ 1.09 vs 2.87 (Baseline) (-1.78)。
> - HuMMan-MoGen (Temporal Composition) 上，RPrecision↑ 0.41 vs 0.24 (Baseline w/o SAMI) (+0.17)。
> - HumanML3D 上，FID↓ 0.151 vs 0.544 (MDM) (-0.393)。

## 概述

### 问题瓶颈

文本驱动的运动生成旨在根据自然语言描述合成人体运动序列。现有方法（如 **MDM** (Tevet et al., ICLR 2023)、**MotionDiffuse** (Zhang et al., arXiv 2022)、**T2M-GPT** (Zhang et al., CVPR 2023)）在全局描述下已取得显著进展，但其核心瓶颈在于：**难以根据细粒度描述合成具有时空一致性的复杂运动序列**。具体而言，这些方法缺乏对空间维度（不同身体部位的独立动作与协作关系）和时间维度（多阶段语义的时序组合与过渡）的精细控制能力，导致生成的运动在局部细节上模糊不清或时序逻辑混乱。

### 核心方法

FineMoGen 是一种基于扩散模型的运动生成框架，其核心创新在于提出了**时空混合注意力机制（Spatio-Temporal Mixture Attention, SAMI）**。SAMI 的关键洞察是：将传统注意力机制中的全局模板沿空间（身体部位）和时间（运动阶段）两个维度解耦，使模型能够显式组合细粒度条件。

SAMI 包含三个关键组件：
- **空间独立性建模**：通过可学习参数对不同身体部位的特征进行加权融合，实现部位间协作关系的精细控制。
- **时间独立性建模**：将时间变化信号建模为时间差的线性函数，并通过高斯核归一化计算各时间段信号的相对重要性，从而捕捉运动阶段的时序依赖。
- **稀疏激活混合专家（MoE）**：引入 top-k 稀疏门控的专家网络，自适应提取细粒度特征，进一步提升模型对复杂条件的表达能力。

此外，FineMoGen 通过集成大型语言模型（ChatGPT-4）实现了**零样本交互式运动编辑**：用户以自然语言发出修改指令，LLM 自动调整细粒度描述矩阵，再由生成网络合成编辑后的运动序列。

### 主要结果

在通用运动生成基准 HumanML3D 上，FineMoGen 的 FID 达到 **0.151**，显著优于 MDM 的 0.544（降幅 72%）。在细粒度时空组合任务上，FineMoGen 展现了决定性的优势：

- **时序组合**（HuMMan-MoGen 零样本）：RPrecision 达到 **0.41**，较基线（无 SAMI）的 0.24 提升 **+0.17**。
- **空间组合**（HuMMan-MoGen 零样本）：RPrecision 达到 **0.51**，FID 降至 **1.09**，而基线分别为 0.43 和 2.87。
- **跨数据集泛化**（BABEL 零样本时序组合）：RPrecision 达到 **0.51**，超过 TEACH (Athanasiou et al., 3DV 2022) 等专用方法。

消融实验证实，SAMI 的空间独立性和时间独立性模块对性能提升均有显著贡献，而 MoE 的移除会导致性能一致下降，验证了稀疏专家激活在细粒度特征提取中的关键作用。

### 方法定位

FineMoGen 属于**扩散模型驱动的文本-运动生成**方法，其架构沿用了 MotionDiffuse 和 ReMoDiffuse 的 Transformer + 扩散范式，但在注意力机制层面进行了根本性重构。与 ReMoDiffuse 采用的混合高效注意力（MEA）相比，SAMI 将全局模板计算从单一的全局聚合解耦为空间与时间两个独立维度的建模，并引入 MoE 增强特征提取的适应性。该方法在方法谱系中填补了**细粒度时空可控运动生成**的空白，是首个同时支持零样本与全监督场景下细粒度生成与编辑的框架。

## 背景与动机

### 问题背景：文本驱动运动生成的粒度瓶颈

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维运动序列，在游戏、影视、虚拟人等领域具有广泛应用。近年来，扩散模型和自回归方法的引入显著提升了该任务的生成质量，代表性工作包括**MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse**（Zhang et al., arXiv 2022）、**T2M-GPT**（Zhang et al., CVPR 2023）以及基于检索增强的**ReMoDiffuse**（Zhang et al., arXiv 2023）等。然而，这些方法存在一个共同的根本性局限：它们仅能接受粗粒度的全局文本描述（如“一个人向前走并挥手”），无法根据细粒度描述合成具有时空一致性的复杂运动序列。

### 核心瓶颈：缺乏时空精细控制

现有方法的本质瓶颈在于缺乏对**空间**和**时间**两个维度的精细控制能力：

- **空间维度**：真实人体运动涉及多个身体部位的协同配合（如头部、脊柱、四肢等），而现有方法将运动视为整体表征，无法显式建模不同身体部位之间的独立性与协作关系。当文本描述要求“左手举起的同时右手保持下垂”这类空间组合条件时，模型难以准确区分和合成各部位的差异化动作。

- **时间维度**：复杂运动通常由多个时序阶段组成（如“先蹲下，再跳起，最后落地”），现有方法缺乏对语义时序一致性的显式建模，难以保证生成序列在不同时间段的动作与描述中的阶段划分保持一致。

### 现有方法的缺口

在时序动作组合方面，**TEACH**（Athanasiou et al., 3DV 2022）等方法尝试通过时序标注数据训练模型，但其泛化能力受限于监督数据的规模。在空间组合方面，此前尚无方法系统性地探索细粒度身体部位级别的条件生成。更关键的是，现有方法普遍缺乏内建的运动编辑能力，用户无法对生成结果进行交互式修改。

### 本文动机

针对上述缺口，FineMoGen提出以下核心动机：

1. **构建细粒度生成框架**：首次实现能够同时接受空间（身体部位级别）和时间（运动阶段级别）细粒度描述的运动生成与编辑框架，适用于零样本和全监督两种场景。

2. **解耦注意力机制**：深入分析运动扩散模型中的注意力技术，提出将全局模板沿空间（身体部位）和时间（运动阶段）两个维度解耦的方法，使模型能够显式组合细粒度条件，从而实现可控且自然的运动生成。

3. **引入混合专家机制**：通过在注意力模块中引入稀疏激活的混合专家（MoE），自适应地提取不同身体部位和时间段的细粒度特征，进一步提升模型对复杂条件组合的处理能力。

4. **实现交互式编辑**：借助大型语言模型（LLM）修改细粒度描述，实现零样本的交互式运动编辑，使用户能够通过自然语言指令对生成序列进行迭代修改。

## 核心创新

FineMoGen的核心创新在于针对现有文本驱动运动生成方法在细粒度时空控制上的根本性缺陷，提出了一套以**时空混合注意力（Spatio-Temporal Mixture Attention, SAMI）** 为核心的解决方案。其关键突破并非简单地增加模型容量，而是对注意力机制中的全局模板构建过程进行了**因果解耦**，从而首次实现了对空间（身体部位协作）和时间（语义时序一致性）的精细化、可组合控制。

### 瓶颈突破：从全局模糊到时空解耦

现有方法（如**MDM** (Tevet et al., ICLR 2023)、**MotionDiffuse** (Zhang et al., arXiv 2022)）在将文本条件注入运动生成时，其注意力机制生成的全局模板难以区分不同身体部位在不同时间阶段的独立约束，导致细粒度描述（如“先抬起左臂，然后放下右腿”）与生成的运动序列在时空一致性上存在显著鸿沟。FineMoGen的因果杠杆在于识别出**全局模板的混合性是导致控制失效的根源**，进而将其沿空间和时间两个维度进行显式解耦。

### 核心机制：时空混合注意力（SAMI）

SAMI模块是FineMoGen架构的“因果旋钮”，它通过三个相互协同的子机制，将细粒度条件转化为可控的运动生成：

1.  **空间独立性建模**：FineMoGen将原始运动表征手动划分为7个身体部位组（头、脊柱、左臂、右臂、左腿、右腿、尾骨），并对每个部位进行独立投影。空间特征的精炼通过一个可学习的权重矩阵 $\omega_{i,j}$ 实现，允许不同身体部位之间进行特征融合，其公式为：
    $$ \mathbf{Y}_{k,i}^S = \sum_{j=1}^{N_S} \mathbf{B}_{k,j} \cdot \omega_{i,j} $$
    该机制使得模型能够根据文本描述，显式地组合不同身体部位的动作，例如“左臂画圈”的同时“右腿保持静止”。

2.  **时间独立性建模**：为了捕捉运动在时间维度上的动态变化，SAMI引入了一组时间变化信号 $\mathbf{G}_{i,j}'(x)$ 和相对重要性权重 $\mathbf{G}_{i,j}^*(x_k)$。时间变化信号是时间差 $(x - \mathbf{G}_{i,j}^t)$ 的线性函数，而相对重要性则由以时间锚点 $\mathbf{G}_{i,j}^t$ 为中心的高斯核归一化计算得出：
    $$ \mathbf{G}_{i,j}^*(x_k) = \frac{e^{-(x_k - \mathbf{G}_{i,j}^t)^2 / \sigma^2}}{\sum_{l \in [1, N_g]} e^{-(x_k - \mathbf{G}_{i,l}^t)^2 / \sigma^2}} $$
    最终的时间精炼特征 $\mathbf{Y}_{k,i}^T$ 通过加权求和近似得到，这使得模型能够理解并生成如“先走两步，然后跳起来”这类具有时序依赖的复杂动作序列。

3.  **稀疏激活的混合专家（MoE）**：为了从解耦的时空特征中自适应地提取最关键的信息，SAMI在特征投影层引入了MoE机制。其核心公式为：
    $$ f_{\mathrm{MoE}}(x) = \sum_{i=1}^{N_e} \mathrm{TOP}_k(\mathrm{Softmax}(W_1 x)) \cdot W_2 \phi(W_3 x) $$
    该机制通过Top-k稀疏门控，仅激活少数最相关的专家网络，从而避免了不同细粒度特征之间的干扰，提升了特征提取的效率和纯度。

### 应用创新：零样本交互式运动编辑

与所有基线方法相比，FineMoGen的另一个关键“changed slot”是内建了**零样本运动编辑能力**。该方法无需任何编辑任务的训练数据，而是通过将大型语言模型（LLM，如ChatGPT-4）作为交互界面。用户使用自然语言发出编辑指令，LLM负责理解意图并直接修改原始的细粒度时空描述矩阵，随后FineMoGen根据修改后的描述重新生成运动序列。这一创新将复杂的运动编辑问题转化为一个语义描述修改问题，实现了完全开放词汇、交互式的运动编辑。

### 创新点总结

FineMoGen的创新之处不在于发明了全新的生成范式，而在于**对扩散模型中注意力机制的根本性重构**。它将一个全局混合的注意力模板，解耦为空间独立、时间独立且由MoE驱动的精细化组件，从而将细粒度文本描述与运动生成之间的映射关系从“黑箱关联”转变为“显式组合”。这一设计使得模型在零样本设定下，于时序和空间组合任务上的准确率远超所有基线方法，证明了其核心创新的有效性。

## 整体框架

FineMoGen 的整体 pipeline 围绕“细粒度时空描述 → 运动生成 → 交互式编辑”三条主线构建，如 **Figure 2** 所示。系统由六个核心模块串联而成，形成端到端的可控运动合成与编辑闭环。

### 输入：细粒度时空描述矩阵

与传统方法仅接受单一全局文本不同，FineMoGen 的输入是一个结构化的**描述矩阵** $\mathrm{Text}_{i,j}$，其中 $i \in [1, N_T]$ 对应时间阶段（motion stages），$j \in [1, N_S]$ 对应身体部位。该矩阵显式编码了“何时、哪个身体部位、做什么动作”的细粒度约束，是后续空间独立性和时间独立性建模的信息源头。

### 文本编码器：从描述矩阵到文本特征

细粒度描述矩阵首先经过一个**冻结的 CLIP 模型**（ViT-B/32）提取通用语义特征，随后通过**两层可训练的 Transformer 层**进行任务适配，得到精炼的文本特征矩阵。这一设计在保留 CLIP 强大泛化能力的同时，赋予模型对运动生成任务的领域适应性。

### 运动编码器：结构化运动表征

原始运动序列被输入一个**4 层 Transformer 运动编码器**，输出维度为 $7 \times 64$ 的特征张量——7 个身体部位（头、脊柱、左臂、右臂、左腿、右腿、轨迹），每部位 64 维。这种显式的身体部位分组为后续 SAMI 模块中的空间独立性建模提供了结构基础。

### SAMI 模块：时空混合注意力核心

SAMI（Spatio-Temporal Mixture Attention）是整个框架的**核心创新模块**，嵌入于 Motion Transformer 的每一层中。它从两个维度解耦全局注意力模板的生成：

1. **空间独立性建模**：允许不同身体部位之间通过可学习权重 $\omega_{i,j}$ 进行加权信息融合，而非简单拼接后全局注意力，从而显式组合各部位的细粒度条件。
2. **时间独立性建模**：通过生成 $N_g$ 个时间变化信号（time-varied signals），并以高斯核归一化计算各时刻的相对重要性，实现时序语义的精确对齐。
3. **稀疏激活混合专家（MoE）**：在空间和时间两条路径中均引入 MoE 层，使用 Top-k 稀疏门控自适应激活专家网络，以提取更具判别力的细粒度特征。

SAMI 的最终输出 $\mathbf{Y}_{k,i}$ 由空间细化特征 $\mathbf{Y}_{k,i}^S$ 与时间细化特征 $\mathbf{Y}_{k,i}^T$ 求和得到，实现了时空约束的联合建模。

### 扩散过程：生成与去噪

FineMoGen 基于扩散模型框架进行运动生成：

- **前向扩散**：1000 步马尔可夫链，逐步向原始运动序列 $\mathbf{x}_0$ 注入高斯噪声，$\beta_t$ 从 $0.0001$ 线性增长至 $0.02$。
- **逆向去噪**：推理时采用 50 步去噪过程，训练目标为最小化预测初始序列与真实值之间的均方误差（MSE）。训练中随机 mask 10% 的文本条件以增强鲁棒性。

### LLM 编辑器：零样本交互式编辑

FineMoGen 通过集成 **ChatGPT-4** 实现了零样本运动编辑能力。用户以自然语言提出编辑指令（如“让左臂举得更高一些”），LLM 负责修改对应的细粒度描述矩阵，修改后的描述直接送入生成网络产生新的运动序列。这一设计将运动编辑问题转化为文本描述修改问题，无需额外训练编辑模型。

### 数据流总结

整个 pipeline 的数据流可概括为：**细粒度描述矩阵 → CLIP + 可训练 Transformer → 文本特征矩阵 → SAMI 增强的 Motion Transformer（同时接受噪声运动序列输入）→ 去噪后运动序列**。编辑分支则为：**用户自然语言指令 → LLM 修改描述矩阵 → 重新生成**。

## 核心模块与公式推导

FineMoGen 的核心架构建立在扩散模型之上，其生成网络由多个结构相同的 **Motion Transformer** 块堆叠而成。每个块的核心是本文提出的 **时空混合注意力（Spatio-Temporal Mixture Attention, SAMI）** 模块，辅以前馈网络（FFN）。SAMI 的设计目标是从全局注意力模板的构建方式入手，显式解耦空间与时间维度的细粒度约束。

### 全局模板的构建与查询

传统混合高效注意力（Mixed Efficient Attention, MEA）首先通过线性投影和 Softmax 聚合构建全局模板 $\mathbf{G}$，再通过查询 $\mathbf{Q}$ 从中提取细化特征。其核心计算如下：

$$\mathbf{V} = [W_m^V \mathbf{X_m}; W_t^V \mathbf{X_t}], \quad \mathbf{K} = [W_m^K \mathbf{X_m}; W_t^K \mathbf{X_t}], \quad \mathbf{G} = \operatorname{Softmax}(\mathbf{K}) \mathbf{V}$$

$$\mathbf{Q} = W_m^Q \mathbf{X_m}, \quad \mathbf{Y} = \operatorname{Softmax}(\mathbf{Q}) \mathbf{G}$$

其中 $\mathbf{X_m}$ 为运动特征，$\mathbf{X_t}$ 为文本特征，$W$ 为可学习的投影矩阵。该过程将运动与文本特征融合为统一的全局模板 $\mathbf{G}$，再从中查询出细化后的运动特征 $\mathbf{Y}$。然而，这种全局混合的方式忽略了身体部位之间的空间独立性和运动阶段之间的时间独立性，难以精确响应细粒度的时空描述。

### 时间独立性建模

为解决上述问题，SAMI 将全局模板的构建过程沿时间维度解耦。对于第 $k$ 个时间步，其时间细化特征 $\mathbf{Y}_{k,i}^T$ 可近似为：

$$\mathbf{Y}_{k,i}^T \approx \mu_i(x_k) = \sum_{j=1}^{N_g} \mathbf{G}_{i,j}'(x_k) \cdot \mathbf{G}_{i,j}^*(x_k)$$

该公式的核心思想是：每个全局模板条目 $\mathbf{G}_{i,j}$ 不再是一个静态值，而是被建模为一个随时间变化的时间变化信号（time-varied signal）$\mathbf{G}_{i,j}'(x)$ 与一个描述其相对重要性的权重 $\mathbf{G}_{i,j}^*(x_k)$ 的加权组合。具体而言：

- **时间变化信号** $\mathbf{G}_{i,j}'(x)$ 定义为时间差的线性函数：
  $$\mathbf{G}_{i,j}'(x) = \mathbf{G}_{i,j}^s + \mathbf{G}_{i,j}^v \cdot (x - \mathbf{G}_{i,j}^t)$$
  其中 $\mathbf{G}_{i,j}^s$ 为静态基值，$\mathbf{G}_{i,j}^v$ 为变化率，$\mathbf{G}_{i,j}^t$ 为时间锚点。该设计使得模板在不同时间步可以产生不同的激活模式。

- **相对重要性** $\mathbf{G}_{i,j}^*(x_k)$ 通过高斯核归一化计算，衡量当前时间步 $x_k$ 与时间锚点 $\mathbf{G}_{i,j}^t$ 的距离：
  $$\mathbf{G}_{i,j}^*(x_k) = \frac{e^{-(x_k - \mathbf{G}_{i,j}^t)^2 / \sigma^2}}{\sum_{l \in [1, N_g]} e^{-(x_k - \mathbf{G}_{i,l}^t)^2 / \sigma^2}}$$

通过这种时间解耦，模型能够根据当前时间步动态调整各模板条目的贡献，从而实现对不同运动阶段细粒度时序条件的精确响应。

### 空间独立性建模

在空间维度上，FineMoGen 将原始运动表示手动划分为 $N_S = 7$ 个身体部位组（头部、脊柱、左臂、右臂、左腿、右腿、轨迹），并对每个部位独立进行特征投影。空间细化特征 $\mathbf{Y}_{k,i}^S$ 通过所有身体部位特征的加权融合得到：

$$\mathbf{Y}_{k,i}^S = \sum_{j=1}^{N_S} \mathbf{B}_{k,j} \cdot \omega_{i,j}$$

其中 $\mathbf{B}_{k,j}$ 为第 $j$ 个身体部位经 MoE 投影后的增强特征，$\omega_{i,j}$ 为可学习的融合权重，控制部位 $j$ 对部位 $i$ 的影响程度。该设计显式建模了身体部位之间的协作关系，使模型能够根据细粒度描述独立控制不同部位的运动。

### 稀疏激活混合专家（MoE）

为进一步增强模型对细粒度特征的提取能力，SAMI 在多个关键位置引入了稀疏激活的混合专家层。其标准形式为：

$$f_{\mathrm{MoE}}(x) = \sum_{i=1}^{N_e} \mathrm{TOP}_k(\mathrm{Softmax}(W_1 x)) \cdot W_2 \phi(W_3 x)$$

其中 $N_e$ 为专家总数，$\mathrm{TOP}_k$ 为稀疏门控操作（仅保留 top-$k$ 个最高权重的专家），$\phi$ 为激活函数。通过稀疏激活，不同输入可以路由到不同的专家子网络，从而自适应地提取多样化的细粒度特征。消融实验表明，移除 MoE 会导致性能一致下降，验证了稀疏专家激活对细粒度特征提取的关键作用。

### 扩散过程与训练目标

FineMoGen 采用标准的扩散模型框架。前向过程为 $T=1000$ 步的马尔可夫链，逐步向原始运动序列 $\mathbf{x}_0$ 注入高斯噪声：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$

其中 $\beta_t$ 从 $0.0001$ 线性增加到 $0.02$。利用 Ho 等人的简化技巧，任意时间步的加噪样本可直接采样：

$$\mathbf{x}_t := \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$$

其中 $\bar{\alpha}_t = \prod_{s=1}^t (1 - \beta_s)$，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$。逆向过程为 50 步去噪，训练目标是最小化预测初始序列与真实值之间的均方误差。训练时以 10% 的概率随机掩码文本条件，以增强模型的零样本泛化能力。

### 补充图表

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/001_Figure_1.jpg]]
*Figure 1: FineMoGen is a motion diffusion model that can accept fine-grained spatio-temporal descriptions. The synthesized motion sequences are natural and consistent with the given conditions. With the assistance of Large Language Model (LLM), users can interactively edit the generated sequence*

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/002_Figure_2.jpg]]
*Figure 2: An overview of FineMoGen. As for the motion generation task, the fine-grained descriptions are first processed by a text encoder. A text feature matrix can be acquired, and then sent to a diffusion model-based motion generative network to generate corresponding motion sequence. For the editing purpose, LLM is used to interact with users and modify the fine-grained description accordingly*

## 实验与分析

### 主流基准上的通用运动生成性能

FineMoGen首先在通用文本到运动生成基准上进行评估，以验证其基础生成能力。在HumanML3D测试集上（Table 1），FineMoGen取得了极具竞争力的结果：RPrecision Top-1达到0.504，FID降至0.151，MMDist为2.998。与基线方法相比，FineMoGen的FID显著低于**MDM**（Tevet et al., ICLR 2023）的0.544和**MotionDiffuse**（Zhang et al., arXiv 2022）的0.630，表明其生成运动的整体质量与真实分布更为接近。在KIT-ML测试集上（Table 2），FineMoGen同样展现出稳定的性能优势，验证了该方法在不同数据规模下的泛化能力。

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on the HumanML3D test set. $\mathbf { \ddot { \rho } } \mathbf { \hat { \rho } } \mathbf { \Phi } ^ { * } ( \mathbf { \vec { \rho } } \mathbf { \Phi } \mathbf { \vec { \rho } } \mathbf { \Phi } ^ { * }$ ) indicates that the values are better if the metric is larger (smaller). We run all the evaluations 20 times and report the average metric and 95% confidence interval is. The best result are in bold and the second best result are underlined

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on the KIT-ML test set*

值得注意的是，在HumanML3D上，基于检索增强的**ReMoDiffuse**（Zhang et al., arXiv 2023）在部分指标上略优于FineMoGen（RPrecision Top-1 0.510 vs 0.504，FID 0.103 vs 0.151）。这一差距源于ReMoDiffuse显式利用外部检索库进行混合去噪，而FineMoGen的核心设计目标是细粒度时空组合生成，并非在通用基准上追求绝对领先。FineMoGen在保持高度竞争力的同时，额外提供了现有方法不具备的细粒度控制能力。

### 时序组合生成：零样本与全监督评估

时序组合生成要求模型根据分阶段的文本描述合成具有语义时序一致性的运动序列，这是现有方法的显著短板。在BABEL测试集上的零样本评估中（Table 3），FineMoGen取得了0.51的RPrecision，显著超过专门针对时序组合设计的**TEACH**（Athanasiou et al., 3DV 2022）的约0.45（原文图表估算）。在HuMMan-MoGen测试集上，FineMoGen的RPrecision达到0.41，远超未使用SAMI的基线（0.24），提升幅度达70.8%。

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/007_Table_3.jpg]]
*Table 3: Quantitative results of temporal composition on the BABEL test set and HuMMan-MoGen test set*

这一性能优势的核心机制在于SAM中的时间独立性建模：通过生成$N_g$个时间变化信号，并对每个时间锚点计算相对重要性权重（见公式3），模型能够显式地捕捉不同运动阶段之间的语义转换，而非依赖隐式的序列建模。稀疏激活的混合专家（MoE）进一步增强了模型对不同时序模式的自适应提取能力。

### 空间组合生成：身体部位协同控制

空间组合任务要求模型根据对不同身体部位（头部、脊柱、左臂、右臂、左腿、右腿、轨迹）的独立描述生成协调一致的整体运动。在HuMMan-MoGen上的零样本评估中（Table 5），FineMoGen取得了0.51的RPrecision和1.09的FID，相比未使用SAMI的基线（RPrecision 0.43，FID 2.87）有显著提升。

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/010_Table_5.jpg]]
*Table 5: Ablation study on HuMMan-MoGen test set. All methods use zero-shot setting, it means that they are not trained on the spatial composition data. Here we report the average score from individual ones of seven different body parts*

空间独立性建模是这一任务的主要贡献来源：通过将运动表示显式划分为7个身体部位组，并引入可学习的部位间融合权重$\omega_{i,j}$（公式5），模型能够在保持各部位独立语义的同时实现协调的全身运动合成。仅引入空间独立性模块即可将RPrecision从0.43提升至0.49。

### 消融实验：SAMI各组件的贡献

Table 4和Table 5系统性地揭示了SAMI各组件在时序和空间组合任务中的作用机制。

**时序组合消融**（Table 4）表明，单独引入时间独立性可将RPrecision从基线的0.24提升至0.37，但单独引入MoE仅带来有限增益（0.29）。当两者结合时，FineMoGen达到0.41，表明时间独立性提供了时序建模的结构化先验，而MoE通过稀疏专家激活增强了模型对不同时序模式的判别能力，两者形成互补。

**空间组合消融**（Table 5）揭示了一个关键的交互效应：直接加入时间独立性模块会降低空间组合性能（RPrecision从0.43降至0.41），这是因为时间建模引入的全局信息混合干扰了空间独立性的细粒度约束。然而，当配合MoE后，FineMoGen达到最优的0.51，说明MoE的稀疏激活机制能够有效解耦时空特征，避免模态间的负面干扰。

移除MoE在所有配置下均导致性能下降，验证了稀疏专家激活在提取细粒度特征中的关键作用。

### 运动编辑能力评估

FineMoGen通过LLM辅助实现了零样本交互式运动编辑。用户以自然语言提出修改需求（如“让左臂摆动幅度更大”），ChatGPT-4将指令转换为对细粒度描述矩阵的修改，修改后的描述直接输入冻结的生成模型产生编辑后的运动。这一设计的核心优势在于：编辑操作发生在文本空间而非运动空间，避免了运动插值或重定向带来的伪影和不自然性。

然而，该编辑机制存在已知局限：LLM可能无法准确理解用户的隐含意图，导致修改后的描述偏离预期。论文明确指出需要指令微调或强化学习来提升LLM编辑器的可控性和鲁棒性。此外，编辑质量的上限受限于底层生成模型的能力和细粒度描述空间的表达能力。

### 失败模式与局限分析

1. **身体部位覆盖不完整**：FineMoGen仅生成骨骼运动数据，不包含手部动作和面部表情。对于需要精细手部交互（如抓取、手势）或面部表情的运动场景，生成的逼真度受到根本性限制，需额外集成专用模型。

2. **领域泛化不足**：训练和评估主要基于HuMMan-MoGen数据集，该数据集以健身动作为主。模型在更广泛的运动类别（如舞蹈、武术、日常交互）上的泛化能力尚未验证，生成的多样性可能受限于训练分布。

3. **LLM编辑的鲁棒性**：零样本编辑依赖预训练LLM的指令遵循能力，在处理模糊或复杂编辑需求时可能出现语义偏移。该组件的系统性评估和优化仍是开放问题。

4. **评估指标局限**：现有指标（FID、RPrecision、Diversity、MultiModality）主要衡量全局分布匹配和检索一致性，无法充分反映局部时空一致性和细粒度语义对齐质量。细粒度生成质量的评估缺乏统一标准。

### 关键实验结论

- **SAMI是细粒度生成的核心使能技术**：通过空间独立性和时间独立性的显式解耦建模，配合稀疏激活MoE的自适应特征提取，FineMoGen首次实现了对时空细粒度约束的有效组合。
- **时空解耦的必要性**：消融实验揭示空间和时间建模存在潜在的相互干扰，MoE的稀疏激活是缓解这一冲突、实现协同增益的关键机制。
- **零样本组合泛化**：FineMoGen在未见过组合标注的情况下，显著超越专门设计的基线方法，验证了SAMI结构先验的泛化能力。
- **LLM+扩散模型的编辑范式**：通过在文本空间进行编辑操作，避免了运动空间编辑的常见伪影，为交互式运动生成提供了新的技术路径，但LLM编辑器的鲁棒性仍需改进。

### 补充图表

![[assets/figures/papers/motion_editing_inpainting_20260603_finemogen/figures/008_Table_4.jpg]]
*Table 4: Ablation study on HuMMan-MoGen test set. All methods use zero-shot setting, it means that they are not trained on the temporal composition data*

## 方法谱系与知识库定位

FineMoGen处于文本驱动人体运动生成（Text-to-Motion）的扩散模型范式之中，其核心创新在于将细粒度时空条件显式注入生成过程。本节从基线关系、适用边界、局限性与开放问题四个维度进行定位。

### 与基线工作的关系

FineMoGen继承并改造了基于扩散的运动生成框架。其直接对比的基线包括：

- **MotionDiffuse**（Zhang et al., arXiv 2022）：早期文本驱动运动扩散模型，使用混合高效注意力（MEA）进行全局特征聚合，但缺乏对细粒度时空条件的显式建模。
- **MDM**（Tevet et al., ICLR 2023）：基于扩散的运动生成方法，在HumanML3D上FID为0.544，作为通用运动生成基线。
- **ReMoDiffuse**（Zhang et al., arXiv 2023）：引入检索增强机制的运动扩散模型，在HumanML3D上FID达到0.103，RPrecision Top1为0.510，是当时性能最强的基线之一。FineMoGen在HumanML3D上的FID（0.151）虽略逊于ReMoDiffuse，但其核心优势不在通用生成质量，而在细粒度组合能力。
- **T2M-GPT**（Zhang et al., CVPR 2023）：自回归运动生成方法，将运动生成转化为序列预测任务。
- **TEACH**（Athanasiou et al., 3DV 2022）：时序动作组合基线，在BABEL零样本时序组合任务中RPrecision约为0.45。

FineMoGen的方法论改造集中在注意力机制层面：将ReMoDiffuse等基线中使用的混合高效注意力（MEA）替换为时空混合注意力（SAMI）。这一替换并非简单的模块更迭，而是将全局注意力模板沿空间维度（7个身体部位）和时间维度（运动阶段）进行解耦，并引入稀疏激活的混合专家（MoE）层以自适应提取细粒度特征。消融实验（Table 4, Table 5）验证了这一改造的有效性：在HuMMan-MoGen时序组合任务中，完整FineMoGen的RPrecision（0.41）相比不含SAMI的基线（0.24）提升0.17；在空间组合任务中，RPrecision从0.43提升至0.51，FID从2.87降至1.09。

### 适用边界

FineMoGen的适用场景具有明确的边界条件：

1. **输入格式依赖**：模型接受细粒度描述矩阵$\text{Text}_{i,j}$，其中$i$对应$N_T$个时序阶段，$j$对应$N_S=7$个身体部位（头、脊柱、左臂、右臂、左腿、右腿、轨迹）。这一结构化输入格式是其核心能力的来源，但也意味着模型无法直接处理自由形式的自然语言描述。

2. **运动类别受限**：训练和评估所依赖的HuMMan-MoGen数据集主要包含健身动作，生成的多样性受限于此场景。该方法在更广泛的运动类别（如舞蹈、武术、日常交互动作）上的泛化能力尚未验证。

3. **表示粒度固定**：模型输出的骨骼运动数据不包含手部动作和面部表情，生成逼真视频需要额外集成其他技术。

4. **编辑能力依赖LLM**：零样本运动编辑通过ChatGPT-4修改细粒度描述实现，其可控性受限于LLM对用户意图的理解能力。指令微调或强化学习可能是提升编辑鲁棒性的方向，但当前尚未实施。

### 局限性与开放问题

**已知局限性**：

- 空间依赖模块在时序组合任务中的作用尚不明确。消融实验显示，在时序组合任务中仅使用空间独立性模块（不含时间独立性）时RPrecision为0.32，而完整模型为0.41，但空间模块的必要性缺乏独立验证。
- 细粒度生成质量的评估缺乏统一标准。现有指标（RPrecision、FID、MMDist、Diversity、MultiModality）主要衡量全局分布匹配和文本-运动对齐，无法充分反映局部时空一致性和动作自然度。
- 存在被滥用于制作虚假视频的潜在风险，尽管数据集本身来自健身动作。

**开放问题**：

1. **LLM编辑组件的鲁棒性评估**：当前编辑流程依赖预训练LLM的零样本能力，用户意图对齐的准确率和失败模式缺乏系统性量化分析。
2. **跨域泛化**：FineMoGen在HuMMan-MoGen上的细粒度组合能力是否能迁移到更复杂的运动类别（如双人交互、竞技体育）仍待探索。
3. **评估体系完善**：细粒度运动生成需要新的评估指标，能够分别衡量空间一致性（各身体部位协作的自然度）和时间一致性（动作阶段过渡的流畅性），而非仅依赖全局统计指标。
4. **手部与面部扩展**：将手部动作和面部表情纳入细粒度生成框架，是实现完整虚拟人运动合成的必要步骤，但会显著增加表示维度和标注成本。

## 原文 PDF

![[paperPDFs/NEURIPS_2023/FineMoGen_Fine_Grained_Spatio_Temporal_Motion_Generation_and_Editing.pdf]]
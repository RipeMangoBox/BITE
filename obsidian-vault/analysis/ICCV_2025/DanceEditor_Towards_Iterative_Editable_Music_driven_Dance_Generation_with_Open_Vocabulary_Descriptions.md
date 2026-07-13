---
title: "DanceEditor: Towards Iterative Editable Music-driven Dance Generation with Open-Vocabulary Descriptions"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/DanceEditor_Towards_Iterative_Editable_Music_driven_Dance_Generation_with_Open_Vocabulary_Descriptions.pdf
project_link: https://lzvsdy.github.io/DanceEditor/
code_link: null
aliases:
- DanceEditor
tags:
- ICCV_2025
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "CEM模块中基于时间相关性矩阵的自适应舞蹈融合权重σ，该权重动态调节初始舞蹈预测和当前编辑运动特征的融合比例。"
primary_logic: "通过预测-编辑范式将音乐条件生成与文本条件编辑解耦，并利用CEM捕获文本与舞蹈动作的时间相关性，从而在迭代编辑中同时保持音乐节奏同步和编辑语义对齐。"
claims:
- "CEM消融实验表明，相比不带CEM的编辑分支，它在所有指标上带来显著提升。"
- "完整的DanceEditor（含CEM）相比无编辑分支或无CEM版本，在FID、BAS、Diversity和MEAS上均取得最佳。"
- "预测-编辑范式支持多轮编辑，随着迭代次数增加，多样性上升而FID仅轻微下降，表明范式能有效保持质量。"
- "在DanceRemix和POPDG数据集上，DanceEditor在所有指标（FID、BAS、Diversity、PFC）上均超越现有最佳方法。"
---

# DanceEditor: Towards Iterative Editable Music-driven Dance Generation with Open-Vocabulary Descriptions

> [!tip] 核心洞察
> 通过预测-编辑范式将音乐条件生成与文本条件编辑解耦，并利用CEM捕获文本与舞蹈动作的时间相关性，从而在迭代编辑中同时保持音乐节奏同步和编辑语义对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DanceEditor：面向开放词汇描述的迭代可编辑音乐驱动舞蹈生成 |
| 英文题名 | DanceEditor: Towards Iterative Editable Music-driven Dance Generation with Open-Vocabulary Descriptions |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2508.17342) · [Project](https://lzvsdy.github.io/DanceEditor/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | DanceEditor |
| Dataset | DanceRemix, POPDG |

> [!tip] 效果简介
> - DanceRemix 上，FID 为 2.83，对比 3.57 (previous best)，变化 -20.7%。
> - POPDG 上，FID 为 2.87，对比 best in Table 2，变化 outperforms。

## 概要

**DanceEditor** 是一个面向音乐驱动舞蹈生成的大规模可编辑框架，核心目标是解决现有方法在保持音乐节奏同步的前提下，难以实现细粒度、多轮迭代文本编辑的瓶颈。该工作的根本驱动力在于：缺乏支持迭代编辑与多模态条件对齐的大规模舞蹈数据集，以及传统单次生成范式无法在音乐条件与文本编辑条件之间取得有效平衡。

为此，DanceEditor 提出了一种**预测-编辑范式**（prediction-then-editing paradigm），将音乐条件生成与文本条件编辑解耦为两个阶段。在初始预测阶段，一个基于扩散Transformer的生成分支根据音乐信号合成高保真舞蹈运动；在迭代编辑阶段，编辑分支通过**跨模态编辑模块**（Cross-modality Editing Module, CEM）自适应地融合初始舞蹈预测与当前编辑运动特征，从而在注入文本编辑语义的同时保持音乐节奏对齐。CEM 的核心机制是通过计算文本与舞蹈动作之间的时间相关性矩阵，动态生成融合权重 $\sigma$，以此调节初始预测与编辑特征的比例。

在数据集层面，该工作构建了**DanceRemix**——据论文声称是首个支持迭代可编辑舞蹈生成的大规模数据集（Table 1），每个音乐片段至少包含两组可迭代编辑序列对及对应编辑提示。

实验结果表明，DanceEditor 在 DanceRemix 和 POPDG 两个数据集上，于 FID、BAS、Diversity 和 PFC 等指标上均超越了现有最佳方法（Table 2）。消融实验证实，CEM 模块对保持音乐-语义对齐至关重要：移除 CEM 后 FID 从 2.85 显著上升至 3.68（Table 4）。此外，随着编辑迭代次数增加，多样性持续上升而 FID 仅轻微下降，验证了预测-编辑范式在质量与多样性之间的有效平衡（Table 3）。用户研究进一步表明，该方法在自然度、平滑度、运动-编辑文本对齐和变换一致性上均优于对比方法（Figure 5）。

当前方法的主要局限在于仅支持身体动作的生成与编辑，尚未覆盖面部表情和手势等细节，这也构成了未来向更具表现力的全身舞蹈生成扩展的开放问题。



音乐驱动的舞蹈生成旨在根据输入的音乐信号自动合成逼真且富有表现力的舞蹈动作序列，这一任务在数字人、虚拟现实和内容创作等领域具有广泛的应用前景。近年来，扩散模型在运动生成领域取得了显著进展，催生了一系列高质量的音乐条件舞蹈生成方法，如 **EDGE**（Tseng et al., CVPR 2023）、**TM2D**（Gong et al., ICCV 2023）、**Lodge**（Li et al., CVPR 2024）和 **POPDG**（Luo et al., CVPR 2024）。然而，这些方法普遍遵循“单次生成”范式——给定音乐，一次性输出完整的舞蹈序列，缺乏对生成结果进行精细控制和迭代修改的能力。

从实际创作需求来看，编舞过程天然是一个迭代优化的过程：编舞者需要根据音乐节奏不断调整动作幅度、变换舞姿风格、修正局部姿态。现有方法的根本瓶颈在于，**缺乏支持迭代编辑和多模态条件对齐的大规模舞蹈数据集**，以及**难以在保持音乐节奏同步的同时实现细粒度的文本描述编辑**。具体而言，要实现可编辑的舞蹈生成，需要同时满足三个条件：(1) 音乐与舞蹈的节拍对齐；(2) 文本编辑指令与动作修改的语义对齐；(3) 多轮编辑过程中的质量保持。现有方法在这三个维度上均存在明显不足。

为突破上述瓶颈，DanceEditor 提出了一个核心洞察：**通过“预测-编辑”范式将音乐条件生成与文本条件编辑解耦**，并利用跨模态编辑模块（CEM）捕获文本与舞蹈动作的时间相关性，从而在迭代编辑中同时保持音乐节奏同步和编辑语义对齐。这一设计使得框架既能继承现有音乐条件扩散模型的生成能力，又能灵活注入开放词汇的文本编辑信号，实现真正的多轮可编辑舞蹈生成。



## 核心方法与创新机理

DanceEditor 的核心创新在于将音乐驱动的舞蹈生成任务从“单次生成”重构为**预测‑编辑范式（Prediction‑then‑Editing Paradigm）**，并为此设计了**跨模态编辑模块（Cross‑modality Editing Module, CEM）**，从而在保持音乐节奏同步的前提下，首次支持基于开放词汇文本描述的多轮迭代编辑。

### 1. 预测‑编辑范式：解耦音乐条件与文本条件

现有方法（如 **EDGE**（Tseng et al., CVPR 2023）、**TM2D**（Gong et al., ICCV 2023）、**Lodge**（Li et al., CVPR 2024）、**POPDG**（Luo et al., CVPR 2024））通常将音乐到舞蹈的生成建模为单次条件映射，无法灵活响应文本编辑指令。DanceEditor 将任务拆分为两个阶段：

- **初始预测阶段**：一个基于 Diffusion Transformer 的生成分支（Generating Branch）仅以音乐信号为条件，合成高保真的初始舞蹈运动序列。
- **迭代编辑阶段**：编辑分支（Editing Branch）接收初始舞蹈预测、音乐信号和文本编辑描述，产出编辑后的舞蹈序列。该阶段可多轮执行，每一轮以上一轮的输出作为新的“初始预测”。

这一范式将音乐条件生成与文本条件编辑解耦，使得编辑过程不再需要重新建模音乐‑舞蹈的整体映射，而是专注于局部运动调整，从而在迭代编辑中保持音乐节奏的全局一致性。消融实验（Table 3）证实：随着编辑迭代次数从初始预测增加到第 3 轮，多样性从 3.12 升至 3.35，而 FID 仅轻微上升，表明范式能有效平衡生成质量与编辑多样性。

### 2. 跨模态编辑模块（CEM）：自适应融合音乐‑文本‑运动特征

编辑分支的核心是 CEM，它解决了文本编辑信号与音乐节奏信号在时间维度上容易冲突的关键问题。CEM 的因果调控机制如下：

1. **时间相关性矩阵**：分别计算当前迭代运动特征与文本嵌入之间的时间相关性矩阵 $M^{edit}$，以及初始舞蹈预测与文本嵌入之间的时间相关性矩阵 $M^{init}$。这两个矩阵捕获了文本描述对舞蹈序列各时间步的影响程度。
2. **自适应融合权重**：对 $M^{edit}$ 和 $M^{init}$ 执行自适应最大池化后通过 Softmax，得到标量融合权重 $\sigma$：
   $$(\sigma, 1 - \sigma) = \mathrm{Softmax}(\mathrm{AdPool}(M^{edit}), \mathrm{AdPool}(M^{init}))$$
   $\sigma$ 动态调节初始舞蹈特征与当前编辑运动特征的融合比例——当文本编辑对当前运动的某个时间步影响较弱时，模型会自动更多地保留初始预测中的音乐节奏信息。
3. **融合嵌入注入**：利用 $\sigma$ 对初始运动特征 $f^{init}$ 和当前迭代运动特征 $f^{\hat{x}_t}$ 进行加权求和，得到融合运动嵌入 $f^{fusion}$，再通过自适应实例归一化（AdaIN）层注入编辑分支，增强当前迭代运动特征：
   $$f^{fusion} = \sigma \cdot f^{init} + (1 - \sigma) \cdot f^{\hat{x}_t}$$
   $$f_h^{\prime \hat{x}_t} = \mathrm{AdaIN}(f^{\hat{x}_t}, f^{fusion})$$

CEM 的消融实验（Table 4）提供了决定性证据：完整 DanceEditor（含 CEM）的 FID 为 2.85，移除 CEM 后 FID 升至 3.68，性能大幅下降；相比完全无编辑分支的版本（FID=3.95），CEM 带来的提升更为显著。这表明 CEM 是维持音乐‑语义对齐的关键瓶颈模块。

### 3. 其他 changed slots

除上述核心范式与模块外，DanceEditor 还在以下方面区别于 baseline：

- **条件输入**：从“仅音乐”扩展为“音乐 + 文本编辑描述 + 初始舞蹈预测”，使编辑指令可直接作为条件信号参与生成。
- **运动表示**：采用 24‑joint SMPL 格式，每个关节使用 6D 旋转表示，附加 3 维根位置和 4 维脚接触标签，相比通用旋转/位置表示更有利于物理合理性。
- **训练损失**：在标准扩散损失 $\mathcal{L}_{simple}$ 基础上，引入速度损失 $\mathcal{L}_{vel}$ 和脚接触损失 $\mathcal{L}_{foot}$，总损失为 $\mathcal{L}_{total} = \lambda_{simple}\mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$，以约束运动的时序平滑性和足部接触的真实性。

### 4. 创新点的支撑证据强度

- **预测‑编辑范式的有效性**：Table 3 的多轮编辑实验直接证明了迭代编辑的可行性，证据置信度 0.95。
- **CEM 的关键作用**：Table 4 的消融实验显示 CEM 在所有指标上带来显著提升，证据置信度 0.95。
- **整体性能优势**：Table 2 表明 DanceEditor 在 DanceRemix 和 POPDG 两个数据集上的 FID、BAS、Diversity、PFC 均超越现有最佳方法，证据置信度 0.95。
- **用户研究佐证**：Figure 5 的用户研究表明 DanceEditor 在自然度、平滑度、运动‑编辑文本对齐和变换一致性上均优于对比方法，证据置信度 0.95。

### 5. 局限与待验证方向

当前创新集中于身体动作的生成与编辑，尚未涉及面部表情和手势。如何将 CEM 的跨模态时间对齐机制扩展到这些细粒度运动维度，是未来工作的开放问题。



![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2508_17342/figures/008_Figure_4.jpg]]
*Figure 4: Given the same music segments, the results generated by our DanceEditor framework and other SOTA comparison methods. Figure 5. User study with dance naturalness, motion smoothness, Motion-Editing Text Alignment, and motion transformation coherency on our dataset*

DanceEditor 遵循**预测-编辑范式（Prediction-then-Editing Paradigm）**，将音乐驱动的舞蹈生成与文本驱动的舞蹈编辑解耦为两个阶段，从而在迭代编辑中同时保持音乐节奏同步和编辑语义对齐。

### 两阶段流水线

**第一阶段：初始预测（Initial Prediction）**
- 输入：对齐的音乐信号 $c_m$。
- 模块：基于 **Diffusion Transformer** 的生成分支（Generating Branch）。
- 输出：与音乐节奏同步的高保真初始舞蹈运动序列。
- 训练目标：采用简单扩散损失 $\mathcal{L}_{simple}$、速度损失 $\mathcal{L}_{vel}$ 和脚接触损失 $\mathcal{L}_{foot}$ 的加权组合：
  $$\mathcal{L}_{total} = \lambda_{simple} \mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$$
  其中 $\lambda_{simple}=10.0$，扩散过程使用余弦噪声调度，共 1,000 个时间步。

**第二阶段：迭代编辑（Iterative Editing）**
- 输入：初始舞蹈预测、音乐信号、开放词汇的文本编辑描述。
- 模块：编辑分支（Editing Branch），其核心为**跨模态编辑模块（Cross-modality Editing Module, CEM）**。
- 输出：编辑后的舞蹈序列，可多轮迭代。
- 关键机制：CEM 通过计算文本与舞蹈动作的时间相关性矩阵，动态生成自适应融合权重 $\sigma$，将初始预测的运动特征与当前编辑的运动特征进行加权融合，再通过自适应实例归一化层（AdaIN）注入编辑分支，从而在引入编辑语义的同时保留音乐节奏信息。

### 运动表示

采用 24 关节 SMPL 格式表示身体结构，每个关节以 6D 旋转表示，附加 3 维根位置和 4 维脚接触标签，为舞蹈运动提供紧凑且物理合理的参数化。

### 核心因果机制

CEM 中的自适应融合权重 $\sigma$ 是整个框架的关键控制变量。其计算流程为：对编辑运动与文本的时间相关性矩阵 $M^{edit}$ 和初始运动与文本的时间相关性矩阵 $M^{init}$ 分别进行自适应最大池化后做 Softmax，得到融合权重：
$$(\sigma, 1-\sigma) = \text{Softmax}(\text{AdPool}(M^{edit}), \text{AdPool}(M^{init}))$$
随后对初始运动特征 $f^{init}$ 和当前迭代运动特征 $f^{\hat{x}_t}$ 进行加权融合：
$$f^{fusion} = \sigma \cdot f^{init} + (1-\sigma) \cdot f^{\hat{x}_t}$$
最终通过 AdaIN 将融合嵌入作为条件增强当前运动特征：
$$f_h^{\prime\hat{x}_t} = \text{AdaIN}(f^{\hat{x}_t}, f^{fusion})$$

这一设计使得编辑过程能够自适应地决定在多大程度上保留初始预测的音乐节奏结构、在多大程度上响应文本编辑指令，从而在迭代编辑中实现质量与多样性的平衡。消融实验证实，移除 CEM 会导致 FID 从 2.85 显著退化至 3.68（Table 4），验证了该模块对维持音乐-语义对齐的关键作用。



### 预测-编辑范式

DanceEditor 的核心架构遵循“先预测、后编辑”的两阶段范式，将音乐条件生成与文本条件编辑解耦。初始预测阶段由一个基于扩散 Transformer 的生成分支构成，该分支接收音乐信号 $c_m$ 作为条件输入，直接合成高保真的初始舞蹈运动序列。随后，编辑分支接收初始舞蹈预测、音乐信号以及文本编辑描述，通过跨模态编辑模块对运动进行迭代精修。这种解耦设计使得模型能够在多轮编辑中分别保持音乐节奏同步和编辑语义对齐。

### 跨模态编辑模块

跨模态编辑模块（Cross-modality Editing Module, CEM）是 DanceEditor 实现迭代可编辑舞蹈生成的关键组件，其核心机制是通过时间相关性矩阵捕获文本描述与舞蹈动作之间的时序依赖关系，并据此动态调节初始舞蹈预测与当前编辑运动特征的融合比例。

CEM 首先计算两组时间相关性矩阵：编辑运动嵌入与文本嵌入之间的相关性矩阵 $M^{edit} \in \mathbb{R}^{N \times N}$，以及初始运动嵌入与文本嵌入之间的相关性矩阵 $M^{init} \in \mathbb{R}^{N \times N}$。随后，通过对这两个矩阵执行自适应最大池化（Adaptive Max Pooling）并经由 Softmax 归一化，得到舞蹈融合权重：

$$(\sigma, 1 - \sigma) = \mathrm{Softmax}(\mathrm{AdPool}(M^{edit}), \mathrm{AdPool}(M^{init}))$$

其中 $\sigma$ 是自适应融合权重，决定了初始舞蹈特征在当前编辑中的保留程度。利用该权重，CEM 对初始运动特征 $f^{init}$ 和当前迭代运动特征 $f^{\hat{x}_t}$ 进行加权融合，得到融合运动嵌入：

$$f^{fusion} = \sigma \cdot f^{init} + (1 - \sigma) \cdot f^{\hat{x}_t}$$

最后，通过自适应实例归一化（Adaptive Instance Normalization, AdaIN）层，将融合嵌入作为条件注入编辑分支，增强当前迭代运动特征：

$$f_h^{\prime \hat{x}_t} = \mathrm{AdaIN}(f^{\hat{x}_t}, f^{fusion})$$

这一机制使得 CEM 能够在每次编辑迭代中自适应地平衡“保留音乐节奏信息”与“响应文本编辑指令”两个目标。当编辑文本与初始舞蹈的时间相关性较强时，$\sigma$ 趋近于 1，模型倾向于保留初始预测；反之，当编辑文本要求显著改变动作时，$\sigma$ 趋近于 0，模型倾向于采用当前编辑特征。消融实验（Table 4）证实，移除 CEM 会导致 FID 从 2.85 退化至 3.68，验证了该模块对保持音乐-语义对齐的关键作用。

### 训练目标

生成分支的训练采用扩散模型的简单去噪损失：

$$\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{x}, t, c_m, \epsilon \sim \mathcal{N}(0,1)} \left[ \left\| \mathbf{x} - \mathcal{D}_c(\mathbf{x}^t, t, c_m) \right\|_2^2 \right]$$

其中 $\mathbf{x}$ 为真实舞蹈运动，$\mathbf{x}^t$ 为加噪后的运动，$c_m$ 为音乐条件，$\mathcal{D}_c$ 为去噪网络。为提升运动质量，总体训练目标进一步引入速度损失 $\mathcal{L}_{vel}$ 和脚接触损失 $\mathcal{L}_{foot}$：

$$\mathcal{L}_{total} = \lambda_{simple} \mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$$

其中 $\lambda_{simple}$ 经验性地设为 10.0。速度损失约束相邻帧之间的运动连续性，脚接触损失则确保足部与地面的接触符合物理合理性。扩散过程采用余弦噪声调度，总时间步数为 1,000。运动表示采用 24 关节 SMPL 格式，每个关节以 6D 旋转表示，附加 3 维根位置和 4 维脚接触标签。

### 关键公式汇总

| 公式名称 | 核心变量含义 |
|---------|-------------|
| 简单扩散损失 $\mathcal{L}_{simple}$ | $\mathbf{x}$：真实运动；$\mathbf{x}^t$：加噪运动；$c_m$：音乐条件 |
| 总体训练损失 $\mathcal{L}_{total}$ | $\lambda_{simple}=10.0$：简单损失权重 |
| 舞蹈融合权重 $\sigma$ | $M^{edit}, M^{init}$：编辑/初始运动与文本的时间相关性矩阵 |
| 融合运动嵌入 $f^{fusion}$ | $f^{init}$：初始运动特征；$f^{\hat{x}_t}$：当前迭代运动特征 |
| AdaIN 增强嵌入 $f_h^{\prime \hat{x}_t}$ | 以融合嵌入为条件，增强当前迭代运动特征 |



## 实验与关键发现

### 核心瓶颈与评估逻辑

该工作的核心实验验证围绕一个根本瓶颈展开：**如何在保持音乐节奏同步的前提下，实现对舞蹈序列的细粒度文本编辑**。传统方法（如EDGE、TM2D）将音乐到舞蹈视为单次生成任务，缺乏对编辑语义的显式建模，导致编辑后的舞蹈容易丢失音乐对齐性或产生不自然的运动过渡。DanceEditor通过“预测-编辑”范式将这两个目标解耦，并将评估聚焦于生成质量（FID）、音乐-运动对齐（BAS）、运动多样性（Diversity）以及编辑文本对齐（PFC/MEAS）四个维度。

关键因果调节变量是**CEM模块中的自适应融合权重 $\sigma$**（公式3-4），它基于文本-运动时间相关性矩阵动态调节初始预测与当前编辑特征的比例。当 $\sigma$ 偏大时，编辑结果保留更多初始舞蹈结构但编辑响应减弱；当 $\sigma$ 偏小时，编辑效果增强但可能破坏音乐节奏一致性。消融实验（Table 4）直接验证了这一机制：移除CEM后，FID从2.85恶化至3.68，证明该自适应融合是平衡质量与编辑性的关键。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2508_17342/figures/007_Table_4.jpg]]
*Table 4: Ablation on Cross-modaliy Editing Module. ↑ denotes the higher the better, and ↓ indicates the lower the better*

### 主实验结果

**DanceRemix数据集**（Table 2）：DanceEditor在所有指标上均超越现有最佳方法。具体而言，FID达到2.83，相比次优方法（3.57）提升20.7%；BAS达到0.2560，表明音乐-运动对齐性最优；Diversity为3.35，PFC为0.0797，均优于EDGE（Tseng et al., CVPR 2023）、TM2D（Gong et al., ICCV 2023）、Lodge（Li et al., CVPR 2024）和POPDG（Luo et al., CVPR 2024）等基线。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2508_17342/figures/005_Table_2.jpg]]
*Table 2: Comparison of our DanceEditor framework and the state-of-the-art methods on our DanceRemix dataset and POPDG dataset. ↑ denotes the higher the better, and ↓ indicates the lower the better*

**POPDG数据集**（Table 2）：跨数据集泛化能力得到验证，FID达到2.87，同样超越所有对比方法。需要注意的是，该数据集并非为迭代编辑设计，但DanceEditor仍展现出优越的生成质量，说明预测-编辑范式本身具有较强的泛化性。

**定性对比**（Figure 4）：在相同音乐片段下，DanceEditor生成的舞蹈关键帧在动作自然度和编辑文本一致性上明显优于对比方法。用户研究（Figure 5）进一步量化了主观感受：在自然度、平滑度、运动-编辑文本对齐和变换一致性四个维度上，DanceEditor均获得最高评分，其中平滑度优势尤为突出——这归因于CEM模块通过时间相关性矩阵显式建模了编辑动作与原始动作的时序依赖。

### 消融实验

**预测-编辑范式消融**（Table 3）：该实验验证了多轮迭代编辑的可行性。从初始预测（Initial）到第3轮迭代编辑（Iteration #3），多样性从3.12单调上升至3.35，表明每轮编辑都引入了新的运动变化；同时FID仅从2.83小幅上升至2.95，BAS从0.2560轻微降至0.2532，证明范式能有效保持生成质量和音乐对齐性。这一趋势的关键在于CEM模块在每轮编辑中重新计算时间相关性矩阵，自适应调整融合权重，防止误差累积。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2508_17342/figures/006_Table_3.jpg]]
*Table 3: Ablation on Prediction-then-Editing Paradigm. ↑ denotes the higher the better, and ↓ indicates the lower the better*

**CEM模块消融**（Table 4）：这是验证核心机制的最直接证据。完整DanceEditor（含CEM）的FID为2.85，BAS为0.2551，Diversity为3.35，MEAS为0.0813。移除编辑分支（w/o Editing Branch）后，模型退化为标准音乐条件生成，FID恶化至3.95，BAS降至0.2507。保留编辑分支但移除CEM（w/o CEM）时，FID为3.68，BAS为0.2523，Diversity降至3.27。这组对比揭示了因果链条：编辑分支提供了文本条件注入的通道，但缺少CEM的时间相关性建模会导致音乐节奏与编辑语义的冲突，进而损害生成质量。CEM通过计算 $M^{edit}$ 和 $M^{init}$ 两个时间相关性矩阵（公式3），显式捕获了“哪些时间步需要编辑”与“哪些时间步需要保持原样”的决策边界。

### 失败模式与局限性

尽管实验结果表明DanceEditor在整体指标上表现优异，但Table 4中编辑分支的FID（2.85）仍略高于初始预测的FID（2.83），作者将此归因于开放词汇文本描述引入的采样噪声。这意味着当编辑描述与原始舞蹈的语义差距过大时，CEM的自适应融合可能无法完美平衡保真度与编辑强度，导致轻微的生成质量下降。

此外，该方法目前仅支持身体动作的生成与编辑，**尚未包含面部表情和手势**。在需要高表现力的舞蹈场景（如情感表达、叙事性编舞）中，这一限制可能导致生成结果的表现力不足。作者将此列为未来的开放问题。

### 实验设置公平性说明

所有对比方法均在相同的DanceRemix数据集上训练和评估，使用统一的音乐特征提取器（Jukebox）和SMPL 24-joint运动表示格式。评估指标FID、BAS、Diversity和PFC遵循先前工作的标准设定，确保了比较的公平性。训练超参数方面，简单扩散损失权重 $\lambda_{simple}=10.0$，扩散步数1000步，采用余弦噪声调度。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2508_17342/figures/003_Table_1.jpg]]
*Table 1: To the best of our knowledge, our DanceRemix is the first large-scale dataset that enables iterative editable dance generation. Given each music segment, our dataset contains at least two different iterable editing sequence pairs (i.e., × 2) with corresponding editing prompts*



## 定位与知识库关联

### 1. 与已有方法的谱系关系

DanceEditor 处于**音乐驱动舞蹈生成**与**多模态条件运动编辑**的交叉地带。其核心贡献在于将这两个此前相对独立的任务统一到一个“预测-编辑”范式中，从而支持开放词汇描述的迭代编辑。

**相对于音乐条件舞蹈生成方法：** 传统方法如 **EDGE** (Tseng et al., CVPR 2023) 和 **Lodge** (Li et al., CVPR 2024) 聚焦于单次音乐到舞蹈的映射，缺乏对生成结果的细粒度文本控制能力。DanceEditor 的生成分支继承了这类扩散模型的音乐条件机制，但通过引入编辑分支，将任务范式从“一次生成”扩展为“生成后多轮编辑”。

**相对于多模态舞蹈生成方法：** **TM2D** (Gong et al., ICCV 2023) 和 **POPDG** (Luo et al., CVPR 2024) 探索了音乐与文本的联合条件输入。然而，这些方法通常将文本作为全局风格或类别标签，不支持对特定身体部位或动作片段的精细编辑指令。DanceEditor 的关键区分在于 CEM 模块中的**时间相关性矩阵**——它显式建模文本描述与舞蹈序列在时间维度上的对应关系，使得“抬手”“加快节奏”等编辑指令能够精准定位到特定帧，而非全局施加影响。这是 DanceEditor 相对于 TM2D 和 POPDG 在方法层面的核心差异。

**运动表示与训练目标的继承与改进：** DanceEditor 采用 24-joint SMPL 格式与 6D 旋转表示，这与主流方法保持一致。训练损失在标准扩散损失 $\mathcal{L}_{simple}$ 的基础上增加了速度损失 $\mathcal{L}_{vel}$ 和脚接触损失 $\mathcal{L}_{foot}$，总损失为 $\mathcal{L}_{total} = \lambda_{simple}\mathcal{L}_{simple} + \mathcal{L}_{vel} + \mathcal{L}_{foot}$，其中 $\lambda_{simple}=10.0$。这一设计旨在提升生成运动的物理合理性，是对 EDGE 等基线损失函数的针对性增强。

### 2. 适用边界与前提条件

DanceEditor 的有效性依赖于以下关键前提：

- **数据基础：** 方法需要大规模、包含多轮编辑序列对的数据集。论文为此构建了 DanceRemix 数据集，通过运动检索、节拍对齐、Gemini 动作描述生成和 ChatGPT 编辑指令生成等自动化流程完成。若缺乏此类配对数据，编辑分支的训练将无法进行。
- **音乐特征提取：** 所有对比实验和模型训练均使用 Jukebox 作为音乐特征提取器，SMPL 作为人体表示格式。更换音乐编码器或骨架格式可能导致性能下降，需重新验证。
- **编辑粒度：** 当前编辑能力限于身体动作层面，不支持面部表情和手势的编辑。论文明确指出这一局限，并列为未来工作方向。

### 3. 局限性与失败模式分析

**已知局限：**
- **编辑范围受限：** 目前仅支持身体动作的生成与编辑，未包含面部表情和手势等细节。这意味着在生成更具表现力的舞蹈表演时，DanceEditor 无法处理表情与手势层面的语义描述。
- **开放词汇带来的质量波动：** 消融实验（Table 4）显示，引入开放词汇文本描述后，编辑分支的 FID 相比初始预测略有上升（从 2.85 升至编辑后的对应值），表明开放词汇的多样性和不确定性可能对生成质量产生轻微负面影响。

**潜在失败模式（基于方法设计的推断）：**
- **时间相关性矩阵的失效场景：** CEM 通过计算文本与运动特征的时间相关性矩阵 $M^{edit}$ 和 $M^{init}$ 来确定融合权重 $\sigma$。当编辑指令涉及跨帧的全局风格变化（如“让整个舞蹈更优雅”），而非特定时间点的局部动作修改时，时间相关性矩阵可能无法有效捕捉这种全局语义，导致编辑效果不显著。这一推断需要手动验证。
- **多轮编辑的累积误差：** 虽然 Table 3 显示随迭代次数增加，多样性从 3.12 升至 3.35，FID 仅轻微上升，但未报告极端迭代次数（如 10 轮以上）下的质量退化情况。扩散模型的迭代去噪与编辑分支的重复调用可能引入累积误差，在长序列编辑中导致运动失真。

### 4. 开放问题与后续方向

论文明确提出的开放问题包括：
- 如何将编辑能力扩展到面部表情与手势，以生成更具表现力且与音乐一致的真实舞蹈表演？

基于方法设计的延伸问题（非论文直接提出）：
- **跨音乐风格的泛化：** DanceRemix 数据集的音乐分布是否覆盖足够多样的音乐风格？模型在训练分布外的音乐风格（如古典乐、电子乐）上的编辑能力需要进一步验证。
- **实时编辑的可行性：** 当前框架采用扩散模型，推理需要多步去噪。是否可以通过蒸馏或一致性模型等技术实现低延迟的实时交互编辑，是走向实际应用的关键问题。
- **多模态条件的冲突消解：** 当音乐节拍与文本编辑指令存在冲突时（如音乐加速但文本要求“缓慢移动”），CEM 的融合权重 $\sigma$ 如何平衡这种冲突？论文未讨论此类边缘情况下的行为机制。



## 原文 PDF

![[paperPDFs/ICCV_2025/DanceEditor_Towards_Iterative_Editable_Music_driven_Dance_Generation_with_Open_Vocabulary_Descriptions.pdf]]

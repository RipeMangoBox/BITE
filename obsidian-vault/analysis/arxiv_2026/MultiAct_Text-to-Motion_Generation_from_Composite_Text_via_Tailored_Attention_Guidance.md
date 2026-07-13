---
title: "MultiAct: Text-to-Motion Generation from Composite Text via Tailored Attention Guidance"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/MultiAct:_Text-to-Motion_Generation_from_Composite_Text_via_Tailored_Attention_Guidance.pdf"
project_link: "https://natsala13.github.io/multiact.github.io"
code_link: null
aliases:
- MultiAct
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 交叉注意力对各文本标记的关注不均匀，特别是对次要动作要素的注意力过低。通过选择性放大这些未被充分表示的标记（underrepresented tokens）的交叉注意力得分，可以恢复缺失的动作语义。
primary_logic: 在预训练的扩散模型上，无需重新训练，通过对特定标记、特定Transformer层和特定扩散步骤进行定制化的注意力增强（梯度优化），可以显著改善复合提示的语义覆盖。由于最佳参数依赖于具体提示，引入轻量级决策方案ParamGate（基于最近邻、阈值分类和LLM测试时缩放）来自动预测最优强化参数，使得该方法能够泛化到未见提示。
claims:
- 基线模型MDM*在复合提示上经常遗漏关键动作成分，如图1所示的失败案例。
- MultiAct在Table 1的所有指标上均优于现有基线（MDM*、MoMask、STMC和适应的Attend-and-Excite），并在用户研究中获得显著偏好。
- 消融实验表明，固定参数组合导致较差的文本对齐（Dual MM Dist 105.97），而ParamGate逐步引入层、步骤和标记的定制选择后，对齐持续改善，其中测试时缩放取得最佳效果（Dual MM Dist 85.16）。
- HumanML3D "while" 子集 上 R Precision Top1 = 0.19 (MultiAct)
---

# MultiAct: Text-to-Motion Generation from Composite Text via Tailored Attention Guidance

> [!tip] 核心洞察
> 在预训练的扩散模型上，无需重新训练，通过对特定标记、特定Transformer层和特定扩散步骤进行定制化的注意力增强（梯度优化），可以显著改善复合提示的语义覆盖。由于最佳参数依赖于具体提示，引入轻量级决策方案ParamGate（基于最近邻、阈值分类和LLM测试时缩放）来自动预测最优强化参数，使得该方法能够泛化到未见提示。

| 字段 | 内容 |
|------|------|
| 中文题名 | MultiAct：通过定制化注意力引导的复合文本到运动生成 |
| 英文题名 | MultiAct: Text-to-Motion Generation from Composite Text via Tailored Attention Guidance |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.30925) · [Project](https://natsala13.github.io/multiact.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MultiAct |
| Dataset | HumanML3D "while" 子集, 作者构建的复合提示集（140 prompts） |

> [!tip] 效果简介
> - HumanML3D "while" 子集 上，R Precision Top1 0.19 (MultiAct) vs 0.14 (MDM*) (+0.05)。
> - 作者构建的复合提示集（140 prompts） 上，Dual MM Dist 85.16（测试时缩放） / 96.07（Action-detail） vs 各基线方法（见Table 1） (显著更低（更低偏差表示更好对齐）)。
> - 用户研究（质量/文本对齐/综合偏好） 上，Overall Preference 83.30% 投票率（测试时缩放） vs 与各基线成对比较，多数优于50% (大幅领先)。

## 概要

### 问题背景

文本到运动生成（text-to-motion generation）旨在根据自然语言描述合成人体运动序列。现有扩散模型在处理包含**单个动作**的提示时表现良好，但面对**同时包含多个动作的复合提示**（如“一边向前跳跃一边举起双臂”）时，普遍出现**语义消失（vanishing semantics）** 问题：交叉注意力机制倾向于过度集中在主导动词上，压制了方向、方式、肢体等次要动作成分，导致生成的运动遗漏了提示中的关键语义。

### 核心方法

MultiAct 提出了一种**免训练、推理时介入**的框架来解决上述瓶颈。其核心思路是：在预训练的扩散骨干上，通过对**特定文本标记、特定Transformer层和特定扩散步骤**进行定制化的交叉注意力增强，恢复被压制动作成分的表达。具体而言，MultiAct 通过梯度优化放大“未被充分表示标记”（underrepresented tokens）的注意力得分，使这些语义成分重新影响运动生成过程。

由于最优的增强参数（选择哪个标记、哪一层、哪个扩散步段）高度依赖于具体提示，MultiAct 进一步引入了轻量级决策方案 **ParamGate**，基于最近邻、阈值分类和LLM测试时缩放三种策略，自动为新提示预测最优参数组合，无需穷举搜索。

### 方法定位

MultiAct 在方法谱系中处于**推理时引导（inference-time guidance）** 与**参数定制化**的交叉点。与以下代表性工作形成对比：

- **MDM** (Tevet et al., ICLR 2023)：扩散骨干，不专门处理同时动作，是MultiAct的基底模型。
- **MoMask** (Guo et al., CVPR 2024)：基于VQ-VAE的离散方法，同样未针对复合动作设计。
- **STMC** (Petrovich et al., CVPRW 2024)：支持多轨道时间线控制，可处理同时动作，但需要额外的时间线标注。
- **Attend-and-Excite** (Chefer et al., NeurIPS 2023)：图像域的注意力编辑方法，本文将其适配到运动域作为基线，但其固定参数策略在复合运动提示上效果有限。

MultiAct 的独特优势在于：**无需重新训练或修改骨干架构**，通过轻量级参数预测实现提示定制化的注意力引导，在保持运动质量的同时显著提升复合语义的覆盖度。

### 主要结果

在作者构建的140个复合提示集上，MultiAct 在所有评估指标上均优于上述基线方法：
- **双模态距离（Dual MM Dist）**：测试时缩放变体取得 85.16，显著低于各基线，表明更好的文本-运动对齐。
- **用户研究**：综合偏好投票率达 83.30%，大幅领先对比方法。
- **消融实验**：固定参数组合导致对齐较差（Dual MM Dist 105.97），而 ParamGate 逐步引入层、步骤和标记的定制选择后，对齐持续改善，验证了参数定制化的必要性。

> **注意**：评估所用的复合提示集为作者自行构造，格式限定为“\<prefix\> while \<suffix\>”，其分布可能与真实使用场景存在偏差；双模态距离指标的有效性仅通过人工设计的辅助任务验证，尚缺乏大规模标准测试。

### 任务场景：复合文本到运动生成

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列。近年来，基于扩散模型的方法在单动作生成上取得了显著进展，但当文本提示包含**同时发生的多个动作**（composite prompts）时，现有方法暴露出一个关键瓶颈：**语义消失（vanishing semantics）**。

具体而言，当提示形如“<prefix> while <suffix>”（例如“向前跳跃的同时举起手臂”），扩散模型的交叉注意力（cross-attention）机制倾向于过度集中在主导动词上，而压制了其他动作成分——如方向、方式、附属动作等。这导致生成的运动未能实现提示中的所有语义，例如只跳不举手，或只移动方向错误。Figure 1 中，蓝色标注的骨干模型生成结果清晰地展示了这一失败模式：在“向前跳跃时举起手臂”和“向后移动时运球”两个复合提示上，关键动作成分（举手、运球）完全缺失。

### 现有方法的缺口

当前文本到运动生成的主流方法可分为两类：

- **通用生成模型**：如 **MDM**（Tevet et al., ICLR 2023）及其改进版 MDM*、**MoMask**（Guo et al., CVPR 2024）等，在标准单动作提示上表现优异，但并未专门设计处理同时动作的机制。当面对复合提示时，它们缺乏对多语义成分的显式建模能力。

- **多动作控制方法**：如 **STMC**（Petrovich et al., CVPRW 2024）通过多轨道时间线支持同时动作生成，但其控制方式依赖结构化输入，与自由文本描述的灵活性存在差距。

此外，将图像域中已有的注意力编辑方法直接迁移到运动域也面临挑战。例如，**Attend-and-Excite**（Chefer et al., NeurIPS 2023）在图像生成中通过增强被忽略对象的注意力来恢复缺失语义，但直接应用于运动生成时，其固定策略无法适应不同提示对参数（增强哪些标记、在哪些层、在哪些扩散步骤）的差异化需求，效果有限（见 Table 1 中 adapted Attend-and-Excite 的表现）。

### 核心动机：无需重训练的推理时干预

上述缺口指向一个明确的研究动机：**能否在不重新训练或修改预训练运动生成模型的前提下，通过推理时的轻量级干预，恢复复合提示中被压制的语义？**

这一思路的优势在于：
1. **即插即用**：无需访问训练数据或修改模型架构，可直接应用于现有的扩散骨干。
2. **经济高效**：避免了针对复合提示重新训练模型的高昂成本。
3. **可泛化性**：若干预策略能够根据提示自适应调整，则可处理未见过的复合动作组合。

MultiAct 正是在这一动机下提出的：它通过**定制化注意力引导（tailored attention guidance）**，在推理过程中选择性地放大未被充分表示的标记（underrepresented tokens）的交叉注意力得分，从而恢复缺失的动作语义。同时，为了消除人工调参的负担并实现跨提示泛化，MultiAct 引入轻量级参数决策方案 **ParamGate**，自动预测每个提示对应的最优增强参数。

## 核心方法与创新机理

MultiAct 的核心创新并非提出新的生成架构，而是在**预训练的文本到运动扩散模型上，通过推理阶段的定制化注意力引导，解决复合提示中的语义消失问题**。其关键洞察在于：现有扩散模型（如 **MDM**，Tevet et al., ICLR 2023）在生成同时包含多个动作的复合提示时，交叉注意力会过度集中在主导动词上，导致次要动作成分（如方向、方式、风格）在生成的运动中丢失（见图1蓝色案例）。MultiAct 通过选择性放大这些未被充分表示标记的交叉注意力得分，恢复了缺失的语义，且**无需重新训练或修改骨干架构**。

这一创新具体体现在以下三个核心 changed slots 上：

### 1. 交叉注意力的定制化引导优化

基线方法使用标准的交叉注意力，不施加任何外部调制。MultiAct 则引入了一个**注意力对齐损失** $\mathcal{L}_{atn}$，针对选定的未被充分表示标记 $m$，在所有 $N$ 帧上最大化其注意力得分：

$$\mathcal{L}_{atn} = \frac{1}{N} \sum_{i=1}^{N} (1 - A_{i,m})^2$$

然后通过梯度下降直接更新扩散过程中的运动潜在张量 $X$：

$$X' = X - \eta \nabla_X \mathcal{L}_{atn}$$

这一过程仅在选定的扩散步骤和 Transformer 层上执行，通过反向传播调整潜在表示，从而强化目标标记对生成运动的影响（见图4右侧）。与图像域中类似的 **Attend-and-Excite**（Chefer et al., NeurIPS 2023）不同，MultiAct 的优化参数（标记、层、步骤）是针对每个提示**定制化选择**的，而非使用固定策略。

### 2. 提示定制化的参数选择（ParamGate）

注意力引导的效果高度依赖于所选的优化参数——即增强哪个标记 $m$、在哪个 Transformer 层 $\ell$、以及从哪个扩散步骤 $\hat{t}$ 开始。固定参数组合会导致严重的文本对齐失败（消融实验中 Dual MM Dist 高达 105.97）。MultiAct 的核心机制创新在于 **ParamGate**，一个轻量级的决策方案，能够根据输入提示自动预测最优参数组合，而无需穷举搜索。

ParamGate 将参数预测分解为三个子问题，分别采用非深度学习的方法解决：
- **标记选择**：采用 LLM 测试时缩放（test-time scaling），让大语言模型从提示中识别出最可能被忽略的动作细节标记。
- **层选择**：基于 CLS token 嵌入的 L2 距离，使用最近邻方法从提示集中匹配最相似的提示，沿用其最优层参数。
- **步骤选择**：根据骨干模型在无引导下的偏差误差，通过预计算阈值进行分段分类，确定需要优化的扩散步骤范围。

这一设计使得 MultiAct 能够**泛化到未见过的提示**，而无需为每个新提示重新进行昂贵的参数搜索。

### 3. 优化的时机控制

基线扩散模型的整个去噪过程不可干预。MultiAct 发现，注意力优化仅在**扩散的早期步骤**（如 50 步中的第 46-48 步）有效。在过晚的步骤进行干预会破坏已形成的运动结构，而过早干预则效果不显著。这一发现通过消融实验得到验证：将优化步骤从全范围缩小到 $\mathcal{T} = [48, 47, 46]$ 后，文本对齐指标持续改善。同时，候选层也被限定在 8 层 Transformer 中的第 3 至 5 层，因为偏差空间可视化（图6）显示，这些层对应的参数组合在双模态距离上最接近原点，即对齐效果最佳。

综上，MultiAct 的创新本质是**将复合文本到运动生成的失败归因于交叉注意力分布不均，并通过提示定制化的、时机精准的注意力调制来修复这一问题**，从而在不改变骨干模型的前提下，显著提升了复合动作的语义覆盖和生成质量。

MultiAct 的整体流程围绕一个核心原则构建：**在预训练扩散模型的推理阶段，通过定制化的交叉注意力引导，恢复复合文本提示中被压制的动作语义**。整个框架无需对骨干模型进行重新训练或架构修改，仅通过干预推理过程实现语义覆盖的改善。

### 流程总览

给定一个复合文本提示（例如“<prefix> while <suffix>”结构），MultiAct 的处理流程分为两个阶段（Fig. 2）：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2605_30925/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline. Given a text prompt, MultiAct selects prompt-specific parameters (Sec. 4), applies tailored guided generation (Sec. 3.2), and outputs the resulting motion*

1. **参数选择阶段（ParamGate）**：根据输入提示，自动预测最优的注意力引导参数组合 $\theta = \{m, \ell, \hat{t}\}$，分别对应需要增强的标记、执行增强的 Transformer 层、以及应用增强的扩散步骤范围。
2. **定制化引导生成阶段**：在扩散去噪过程中，于选定的步骤 $\hat{t}$ 内，对选定层 $\ell$ 的交叉注意力施加梯度优化，放大目标标记 $m$ 的注意力得分，从而驱动生成的运动同时体现提示中的所有动作成分。

Fig. 4 以可视化方式展示了这一流程：左侧为集成了定制化优化的扩散推理管线，右侧为定制化优化的内部机制——通过注意力对齐损失 $\mathcal{L}_{atn}$ 反向传播更新运动潜在张量 $X$。

### 模块关系与数据流

MultiAct 的四个核心模块按如下方式协作：

**文本编码** → **ParamGate 决策** → **扩散骨干 + 交叉注意力引导优化** → **运动输出**

具体而言：
- **文本编码模块**使用 BERT 将提示编码为嵌入序列 $E$，作为后续交叉注意力的 Key 和 Value 来源。
- **ParamGate 决策方案**接收提示后，通过三个轻量级子模块分别预测 $\ell$（最近邻）、$\hat{t}$（阈值分类）和 $m$（LLM 测试时缩放），输出定制化的参数组合。
- **扩散骨干（MDM\*）**基于 DDPM 的 Transformer-decoder，逐步去噪生成运动。在推理过程中，**交叉注意力引导优化模块**被嵌入到选定的扩散步骤中：计算注意力对齐损失 $\mathcal{L}_{atn} = \frac{1}{N} \sum_{i=1}^{N} (1 - A_{i,m})^2$，并通过梯度下降 $X' = X - \eta \nabla_X \mathcal{L}_{atn}$ 更新潜在张量，以增强目标标记在所有帧上的注意力。

### 关键设计决策

- **干预时机**：优化仅应用于扩散早期步骤（如步骤 46-48，共 50 步），避免在后期破坏已形成的运动结构。这一设计源于消融实验的验证——过早或过晚干预均会导致对齐质量下降。
- **层选择性**：候选层被限定为第 3 至 5 层（共 8 层），这是通过对偏差空间的聚类分析得出的结论（Fig. 6 展示了层间的视觉分离）。
- **无训练特性**：整个过程不修改骨干模型的权重，仅通过推理时的梯度更新来调整运动潜在表示，保持了方法的即插即用特性。

> **注意**：ParamGate 的具体决策机制（最近邻、阈值分类、LLM 测试时缩放）将在后续章节详细展开，此处仅说明其在整体流程中的位置与功能。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2605_30925/figures/001_Figure_1.jpg]]
*Figure 1: MultiAct synthesizes motion from composite textual descriptions by selectively modulating cross-attention to amplify weakly represented elements in the prompt. Blue: Backbone text-to-motion synthesis fails to generate key action components, such as raising the arms while hopping forward (left) and dribbling a ball while moving backward (right). Brown: Our framework successfully generates all action primitives specified in the prompt. Color saturation indicates time progression; higher saturation indicates later times*

### 问题形式化与交叉注意力机制

MultiAct 构建在预训练的文本到运动扩散模型之上，其核心操作对象是 Transformer 解码器中每一层的交叉注意力（cross-attention）矩阵。给定扩散步骤 $t$ 和 Transformer 层 $\ell$，运动潜在表示 $X_{t,\ell} \in \mathbb{R}^{N \times d}$（$N$ 为运动帧数）与文本嵌入 $E \in \mathbb{R}^{M \times d}$（$M$ 为标记数）之间的交叉注意力得分定义为：

$$A = \mathrm{Softmax}\left(\frac{Q K^T}{\sqrt{d}}\right), \quad Q = X_{t,\ell} W_Q^T, \quad K = E W_K^T$$

其中 $A \in \mathbb{R}^{N \times M}$，$A_{i,m}$ 表示第 $m$ 个文本标记对第 $i$ 帧运动的影响强度。这一注意力矩阵是 MultiAct 进行语义干预的直接抓手。

### 语义消失的诊断与注意力对齐损失

复合提示（如 “walking forward while raising arms”）在标准扩散生成中会出现**语义消失**（vanishing semantics）：交叉注意力过度集中在主导动词（如 “walking”）上，而次要动作成分（如 “raising arms”）对应的标记获得极低的注意力得分，导致生成的运动缺失这些语义。MultiAct 将这类标记定义为**未被充分表示的标记**（underrepresented token），并设计了一个注意力对齐损失来主动放大其影响力：

$$\mathcal{L}_{atn} = \frac{1}{N} \sum_{i=1}^{N} (1 - A_{i,m})^2$$

该损失函数的目标是迫使目标标记 $m$ 在所有 $N$ 帧上的注意力得分 $A_{i,m}$ 趋近于 1，从而将其语义“注入”到整个运动序列中。

### 潜在张量的梯度优化

MultiAct 不修改模型权重，而是通过梯度下降直接调整扩散过程中的运动潜在表示 $X$。在第 $t$ 步去噪时，对选定的层 $\ell$ 和标记 $m$ 执行以下更新：

$$X' = X - \eta \nabla_X \mathcal{L}_{atn}$$

其中 $\eta$ 为优化步长（实验中设为 0.02），每次去噪步骤内重复优化 $r = 18$ 次。这一过程仅在扩散的早期步骤（$\hat{t}$ 范围）执行——实验表明在总共 50 步的扩散中，仅在第 46 至 48 步施加注意力引导即可有效恢复缺失语义，同时避免破坏已形成的运动结构。图 4 完整展示了这一“定制化注意力引导生成”流程。

### 参数空间与 ParamGate 决策方案

上述优化涉及三个关键参数的组合 $\theta = (m, \ell, \hat{t})$：增强哪个标记、在哪个 Transformer 层操作、在哪些扩散步骤执行。原始的穷举参数空间为：

$$\Theta_{\mathrm{pre}} = \{ m, \ell, \hat{t} \mid m \in [0 \ldots M-1], \ell \in [0 \ldots L-1], \hat{t} \in [T-1 \ldots 0] \}$$

该空间随标记数、层数和扩散步数呈组合爆炸。MultiAct 通过两个阶段将其压缩为可用的窄参数集 $\Theta$：首先通过聚类剪枝（基于偏差空间的可视化分离，见图 6）将候选层限定为第 3 至 5 层（共 8 层），候选扩散步骤限定为 $\mathcal{T} = [48, 47, 46]$，候选标记限定为动作细节类标记；随后通过 **ParamGate** 决策方案为每个新提示自动预测最优参数组合。

ParamGate 的预测逻辑由三个轻量级非深度学习方法组成：

- **层预测**（最近邻）：对提示集 $\mathcal{Y}$ 中的每个提示计算其 CLS 标记嵌入，通过 L2 距离找到最相似提示 $y_{nn}$，直接沿用其最优层参数 $\ell = \bar{\ell}(y_{nn})$。
- **扩散步骤预测**（阈值分类）：根据骨干模型在未见提示上的偏差误差 $err(y_{new})$，通过预计算阈值 $\kappa_0, \kappa_1, \ldots$ 将误差映射到离散的步骤范围 $\hat{t}$。
- **标记预测**（LLM 测试时缩放）：利用大语言模型从提示中识别动作细节标记，作为 $m$ 的候选。

最优参数的形式化定义为在数据集 $\mathcal{D}$ 上使偏差误差最小的组合：

$$\bar{\theta}(y) = \underset{\theta \in \Theta}{\arg\min} \, err(y, \theta)$$

### 偏差度量与数据集构建

ParamGate 的预测能力依赖于一个预先构建的数据集 $\mathcal{D} = \{ \boldsymbol{y}, \boldsymbol{\Theta}, \boldsymbol{\mathcal{I}}, \boldsymbol{\mathcal{E}} \}$，其中包含约 140 个复合提示、每个提示在所有 $\Theta$ 参数组合下生成的约 4000 个运动实例，以及对应的双模态偏差误差（dual multi-modal distance）。该偏差度量通过计算生成运动与提示前缀/后缀的 CLIP 嵌入距离来量化文本-运动对齐程度，其可信度通过人工设计的几何启发式验证（图 5）得到确认——低偏差对应正确的后缀动作生成，且未出现假阳性或假阴性。

### 骨干扩散模型的损失函数

MultiAct 所依赖的扩散骨干（MDM*）基于 DDPM 框架，其前向过程为：

$$q(x_t | x_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}, (1 - \alpha_t) I)$$

训练时使用简化的均方误差损失直接预测原始运动 $x_0$：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{t \sim [1, T]} \| x_0 - p_\theta(x_t, t) \|_2^2$$

MultiAct 在此预训练骨干之上进行推理时干预，不涉及对该损失的任何修改或微调。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2605_30925/figures/003_Figure_3.jpg]]
*Figure 3: Attention visualization. The colored heatmaps illustrate attention scores for the words “forward” (yellow) and “arms” (green). Our backbone assigns low attention to arm-related tokens, resulting in motions in which the arms are not raised. In contrast, our method assigns high attention scores to both tokens, producing a synchronized motion that faithfully reflects the prompt*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2605_30925/figures/004_Figure_4.jpg]]
*Figure 4: Attention guided generation. This figure visualizes Algs 1 and 2. Left: Diffusion inference pipeline (Appendix A.2) with tailored optimization integrated. Tailored optimization modifies the data tensors*

## 实验与关键发现

### 评估设置与数据集

为系统衡量MultiAct在复合提示上的表现，作者构造了一个包含 **140 个复合文本提示** 的评估集，提示格式统一为“\<prefix\> while \<suffix\>”，涵盖行走、奔跑、跳跃等基础动作及其方向、风格、肢体细节的组合。评估指标包括：

- **双模态距离（Dual MM Dist）**：基于骨干模型MDM*的特征空间，分别计算生成运动与prefix和suffix文本嵌入的匹配偏差，再取均方根。该指标的有效性通过人工设计的几何启发式规则（如手臂抬举高度）进行了视觉验证（Fig. 5），未发现假阳性或假阴性，表明其能可靠反映文本-运动对齐程度。
- **R Precision Top1**：在HumanML3D的“while”子集上，衡量生成运动与正确文本的匹配精度。
- **用户研究**：在质量、文本对齐和综合偏好三个维度上进行成对比较投票。

### 与基线方法的定量比较

**Table 1** 汇总了MultiAct与各基线在复合提示集上的全面对比。MultiAct在所有类别上均一致优于现有方法：

- 与骨干 **MDM***（Tevet et al., ICLR 2023）相比，MultiAct在Dual MM Dist上显著降低，表明复合语义的对齐程度大幅提升。
- 与专门支持同时动作生成的 **STMC**（Petrovich et al., CVPRW 2024）相比，MultiAct在用户研究的综合偏好中获得 **83.30%** 的投票率（测试时缩放版本），远高于50%的随机水平。
- 将图像域注意力编辑方法 **Attend-and-Excite**（Chefer et al., NeurIPS 2023）适配到运动域后，其表现仍不及MultiAct，说明单纯迁移图像域的注意力增强策略无法充分解决运动生成中的语义消失问题。
- 基于VQ-VAE的离散方法 **MoMask**（Guo et al., CVPR 2024）同样未针对同时动作进行设计，在复合提示上表现较弱。

**Table 2** 展示了HumanML3D“while”子集上的R Precision Top1结果：MultiAct达到 **0.19**，显著优于骨干MDM*的 **0.14**（+0.05）。需注意该子集并非为同时动作评估专门设计，因此提升幅度可能被低估。

### 消融实验：定制化参数选择的关键作用

**Table 3** 的消融实验揭示了ParamGate各组件对文本对齐的贡献，核心结论是：**固定参数组合效果最差，逐步引入提示定制化选择持续改善对齐**。

- **固定参数集**：使用在参数空间Θ中表现最佳的单一组合，Dual MM Dist高达 **105.97**，文本对齐严重不足。
- **引入层选择（最近邻）**：通过CLS token嵌入距离匹配最相似提示的Transformer层参数，对齐显著改善。
- **引入步骤选择（阈值分类）**：根据骨干模型的偏差误差预计算阈值，确定优化步数范围（46-48步），进一步降低偏差。
- **引入标记选择（测试时缩放）**：利用LLM对提示进行语义分解，自动识别需要增强的动作细节标记，取得最低的 **Dual MM Dist 85.16**，验证了测试时缩放策略的有效性。

消融实验还验证了层选择的重要性：候选层限定为第3-5层（共8层），这一设计源于偏差空间的可视化分析（Fig. 6），其中靠近原点（低偏差）的参数组合主要集中在这些层。

### 定性分析与失败模式

**Fig. 7** 的定性对比显示，MultiAct在保持高运动质量的同时，能忠实反映提示中的所有动作成分。相比之下，基线方法要么仅关注主导动词（如只生成“向前走”而忽略“举手”），要么出现脚部穿透地面或运动伪影。

**Fig. 8** 展示了运动风格化能力：当提示同时包含多个动作和风格描述（如“drunkenly walk forward while raising arms”），现有方法无法同时满足动作和风格要求，而MultiAct成功生成了具有醉酒特征的不平衡步态和手臂抬举的复合运动。

**Fig. 9** 验证了运动多样性：同一提示多次采样可生成多种合理的运动变体，且均满足复合语义约束。

### 推理开销与局限性

MultiAct的推理时间约为骨干模型的 **6倍**，其中注意力优化循环贡献约2倍，测试时缩放（LLM调用）额外贡献约3倍。这在实时应用中可能构成瓶颈，需要在部署时权衡。

评估所用的复合提示集由作者自行构造，格式限定为“while”结构，可能无法完全覆盖真实场景中更灵活的复合语义表达。双模态距离指标依赖于特定骨干的特征空间，更换骨干需重建约4000次生成的数据集，迁移成本较高。此外，交叉注意力引导每次仅强化单一标记，对于三个以上动作同时发生的极端复杂语义，其有效性尚未充分验证，需人工确认。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2605_30925/figures/010_Table_1.jpg]]
*Table 1: Comparison with baselines. MultiAct consistently outperforms the baselines across all categories on composite prompts. STMC, designed to accommodate co-occurring actions, ranks second in the user study. User study results reported here reflect Fig. 10, where our score is the average over comparisons with all baselines. Bold and underline denote best and second best, respectively. (· )∗ indicates the method was adapted to align with our task*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2605_30925/figures/014_Table_3.jpg]]
*Table 3: Ablation. Using a fixed parameter set yields poor results, while progressively introducing prompt-tailored selection of layers, steps, and tokens improves alignment, with test-time scaling performing best*

## 定位与知识库关联

### 工作定位与核心差异

MultiAct 面向**复合文本到运动生成**（compositional text-to-motion），解决现有扩散模型在同时包含多个动作的提示下出现的**语义消失**问题——交叉注意力过度集中在主导动词上，压制方向、方式等次要动作成分。与重新训练或修改模型架构的路线不同，MultiAct 是一种**无配对、仅推理时**的框架，直接在预训练运动生成器上运行。

在方法谱系中，MultiAct 与以下工作形成对比：

- **MDM**（Tevet et al., ICLR 2023）：基于 Transformer-decoder 的扩散运动生成骨干，使用标准交叉注意力，无额外调制机制。MultiAct 以其为骨干（记为 MDM*），在其上叠加注意力引导优化。
- **MoMask**（Guo et al., CVPR 2024）：基于 VQ-VAE 的离散运动生成方法，不专门处理同时动作。MultiAct 在复合提示上对其取得一致的定量优势（Table 1）。
- **STMC**（Petrovich et al., CVPRW 2024）：通过多轨道时间线控制支持同时动作生成，在用户研究中排名第二，但 MultiAct 在所有指标上均优于它（Table 1）。
- **Attend-and-Excite**（Chefer et al., NeurIPS 2023）：图像域的注意力编辑方法。MultiAct 将其适配到运动域作为基线，但固定参数策略在运动生成中效果有限，验证了提示定制化参数选择的必要性。

### 方法适用边界

**适用场景**：
- 复合文本提示，特别是“\<prefix\> while \<suffix\>”结构的双动作描述（如“向前跳跃 while 举起手臂”）。
- 运动风格化与同时动作的结合（Fig. 8 展示醉酒风格下的复合动作）。
- 需要保持运动多样性的场景——同一提示多次采样可生成多样且语义一致的运动（Fig. 9）。

**不适用或需谨慎的场景**：
- **三个以上动作同时发生**：交叉注意力引导每次仅强化一个标记，在极复杂语义下可能力不从心。作者声称单标记强化已足够，但缺乏系统性验证。
- **非“while”结构的灵活句式**：评估提示集限定为“while”格式，对更自由的复合描述（如“边跑边跳边挥手”）的泛化性未经充分测试。
- **实时或低延迟应用**：整体推理开销约为骨干的 6 倍（测试时缩放额外增加约 3 倍），在移动端或交互场景中可能构成瓶颈。
- **更换骨干模型**：偏差度量（dual multi-modal distance）的构建依赖特定骨干，更换骨干需重建约 4000 次生成的数据集，迁移成本高。

### 局限与开放问题

**已识别的局限**：
1. **提示集依赖**：ParamGate 的训练依赖约 140 个提示构成的提示集 $\mathcal{Y}$，其覆盖范围受限于构造标准，可能无法泛化到所有复合动作组合。
2. **计算开销**：LLM 测试时缩放引入显著推理成本，整体约 6 倍于骨干推理时间。
3. **度量可迁移性**：偏差指标仅在人工设计的辅助任务上验证（Fig. 5），缺乏大规模标准测试，且更换骨干需要重建数据集。
4. **评估覆盖度**：评估所用的提示集和人工评价可能不足以全面衡量所有类型复合动作的生成质量。

**开放问题**：
- 能否将注意力强化策略扩展到**多个语义元素的同时交互**，而非仅强化单一标记？
- 偏差度量在**更多样化的文本格式**下是否依然有效？若否，如何设计更通用的文本-运动对齐指标？
- 该方法是否可迁移到**其他条件生成任务**（如文本到视频、音乐生成）？
- 能否将 ParamGate 的决策逻辑**内化到可学习的模块**中，完全消除推理时的参数搜索，从而降低计算开销？

## 原文 PDF

![[paperPDFs/arxiv_2026/MultiAct:_Text-to-Motion_Generation_from_Composite_Text_via_Tailored_Attention_Guidance.pdf]]

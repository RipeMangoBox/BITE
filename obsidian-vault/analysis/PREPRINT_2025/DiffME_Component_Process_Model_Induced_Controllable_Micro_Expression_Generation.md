---
title: DiffME Component Process Model Induced Controllable Micro Expression Generation
type: paper
paper_level: A
venue: PREPRINT
year: 2025
pdf_ref: paperPDFs/PREPRINT_2025/DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Generation.pdf
project_link: null
code_link: null
aliases:
- DCPMICMEG
tags:
- PREPRINT_2025
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入组件过程模型（CPM）引导的AU共激活与抑制模式（CARM模块），结合自监督变形强度边界估计（ADDE模块），并通过概率强度感知扩散（PITD）中的分类器自由引导（CFG）作为强度滑块，实现情感一致、解剖协调的可控微表情生成。
primary_logic: 将心理学CPM结构先验嵌入扩散生成框架，通过解耦身份与AU运动的交叉注意力及身份拷贝网络（ID-Net）强身份约束，使得网络在保持个体身份的同时，能够精确调控AU强度和双侧对称性，生成情感真实、解剖合理的微表情。
claims:
- DiffME integrates AU representation disentanglement and CPM-informed structural priors, enabling intensity-aware AU control and structured affective modeling.
- The CPM-Guided AU Relational Module (CARM) models the co-activation and inhibition patterns among AUs.
- The AU-Decomposed Deformation Estimator (ADDE) leverages self-supervised training to disentangle AU-specific motion representations and estimate their intensity bounds.
- Leave-One-Dataset-Out (LODO) protocol across six spontaneous ME datasets (CASME... 上 AU prediction UF1/ACC = 与真实顶点帧性能接近（具体数值参见 Table 1）
---

# DiffME Component Process Model Induced Controllable Micro Expression Generation

> [!tip] 核心洞察
> 将心理学CPM结构先验嵌入扩散生成框架，通过解耦身份与AU运动的交叉注意力及身份拷贝网络（ID-Net）强身份约束，使得网络在保持个体身份的同时，能够精确调控AU强度和双侧对称性，生成情感真实、解剖合理的微表情。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffME：基于组件过程模型的可控微表情生成 |
| 英文题名 | DiffME Component Process Model Induced Controllable Micro Expression Generation |
| 会议/期刊 | PREPRINT 2025 |
| Links |  |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiffME |
| Dataset | Leave-One-Dataset-Out (LODO) protocol across six spontaneous ME datasets (CASME, CASME II, SAMM, MMEW, 4DME, CASME3) |

> [!tip] 效果简介
> - Leave-One-Dataset-Out (LODO) protocol across six spontaneous ME datasets (CASME... 上，AU prediction UF1/ACC 与真实顶点帧性能接近（具体数值参见 Table 1） vs 真实顶点帧（Ground-Truth Apex） (性能无明显退化)。

## 概要

微表情（Micro-Expressions, MEs）作为自发情感泄露的关键窗口，在安防、心理与临床等领域具有重要价值。然而，微表情数据的稀缺性与标注难度长期制约着相关研究。现有生成方法——无论是基于运动迁移的策略（如 Fan et al. 2021），还是基于 GAN 的条件生成（如 **FAMGAN**, Xu et al., ACM MM 2021；**ULME-GAN**, Zhou et al., Applied Intelligence 2024）——均存在根本性缺陷：它们或受限于固定的 AU 组合而缺乏控制灵活性，或仅支持粗糙的二值 AU 标签而无法调节强度，且普遍缺乏心理学驱动的情感结构建模，导致生成结果在解剖合理性与情感连贯性上表现不足。此外，该领域长期依赖主观人工编码进行评估，可复现性与公平性难以保证。

针对上述瓶颈，本文提出 **DiffME**——一个由组件过程模型（Component Process Model, CPM）引导的可控微表情扩散生成框架。其核心洞察在于：将心理学的 CPM 结构先验嵌入扩散生成过程，通过解耦身份与 AU 运动表征、引入强身份约束，使网络在保持个体身份的同时，能够像“滑块”一样精确调控 AU 强度与双侧对称性。DiffME 的关键创新包括：（1）**AU 分解形变估计器（ADDE）**，通过自监督学习分离各 AU 的运动表征并估计其生理强度上限；（2）**CPM 引导的 AU 关系模块（CARM）**，利用经验 AU 相关图与图卷积网络建模 AU 间的共激活与抑制模式；（3）**概率强度感知扩散（PITD）**，结合解耦交叉注意力与身份拷贝网络（ID-Net），在分类器自由引导（CFG）机制下实现强度可控生成。

在涵盖六个自发微表情数据集（CASME, CASME II, SAMM, MMEW, 4DME, CASME3）的留一数据集交叉验证协议下，DiffME 生成的顶点帧在 AU 预测指标（UF1/ACC）上接近真实顶点帧性能，且在不同 CFG 强度尺度下表现稳定。消融实验证实，ADDE 与 CARM 构成级联依赖关系，任一模块缺失均导致模型退化为基础潜在扩散模型，输出质量显著恶化。DiffME 还引入基于视觉语言模型（VLM）与深度学习模型（DLM）的标准化评估方案，以替代传统人工编码，增强评估的客观性与可复现性。

微表情（Micro-Expressions, MEs）是一种短暂、微弱且往往非自主的面部运动，通常持续仅 1/25 至 1/3 秒。作为情感计算和心理学研究中的关键线索，微表情在测谎、临床诊断和人机交互等场景中具有重要价值。然而，微表情数据的采集与标注极为困难——其低强度、短时程和稀疏发生特性使得大规模、高质量标注数据集的构建成本高昂，这严重制约了数据驱动的微表情分析与识别研究。

### 现有方法的缺口

为缓解数据稀缺问题，研究者尝试通过生成式模型合成微表情样本。当前主流方案可归为两类（参见 Figure 1 与 Figure 2）：

**基于运动迁移的方法**（如 Fan et al. 2021）从驱动视频中提取运动模式并将其迁移至目标人脸。这类方法受限于观测到的动态模式，只能复现固定的 AU 组合，缺乏对生成过程的灵活控制，难以产生超出驱动视频范围的新表情。

**基于 GAN 的 AU 条件生成方法**，如 **FAMGAN**（Xu et al., ACM MM 2021）和 **ULME-GAN**（Zhou et al., Applied Intelligence 2024），将动作单元（Action Unit, AU）标签作为条件输入。然而，这些方法存在两个根本性缺陷：
1. **控制粒度粗糙**：仅使用二值 AU 标签或固定 AU 组合，无法对 AU 的连续强度进行精细调控，更无法区分面部双侧（左侧/右侧）的独立控制；
2. **缺乏情感结构建模**：未显式建模 AU 之间的共激活与抑制关系，导致生成的微表情在解剖学和情感层面缺乏连贯性——例如，可能出现“嘴角上扬但眼轮匝肌未激活”这种在真实情感表达中不合理的组合。

此外，现有方法的评估几乎完全依赖人工编码（FACS 专家逐帧标注），这种评估方式主观性强、可复现性差，且难以规模化，使得不同方法之间的公平比较成为难题。

### 本文动机

上述缺口的本质在于：**现有微表情生成方法缺乏心理学驱动的结构化情感建模，无法实现 AU 强度和对称性的精细控制，且评估依赖主观人工编码，缺乏可复现性和公平比较。**

为突破这一瓶颈，本文提出 DiffME，其核心动机体现在三个层面：

1. **引入心理学结构先验**：将组件过程模型（Component Process Model, CPM）嵌入生成框架。CPM 是情感科学中广泛认可的理论框架，它定义了不同情感状态下面部动作的协调模式。DiffME 通过 CPM-Guided AU Relational Module（CARM）将这些结构先验编码为 AU 间的共激活与抑制关系，使生成的表情在情感上真实、在解剖上合理。

2. **实现精细可控生成**：将生成任务形式化为从起始帧（onset frame）和 21 维连续 AU 强度向量预测顶点帧（apex frame），该向量涵盖 12 个 AU 及其面部侧化信息，支持对强度和双侧对称性的独立调节。配合自监督的 AU-Decomposed Deformation Estimator（ADDE）估计各 AU 的生理强度上限，以及概率强度感知扩散（PITD）中的分类器自由引导（CFG）作为“强度滑块”，DiffME 实现了前所未有的控制粒度。

3. **建立标准化评估方案**：引入基于视觉语言模型（VLM）和深度学习模型（DLM）的自动评估协议，替代传统人工编码，增强评估的客观性、可复现性和可扩展性，为微表情生成方法的公平比较奠定基础。

## 核心方法与创新机理

DiffME 的核心创新在于将心理学的**组件过程模型（Component Process Model, CPM）**结构先验嵌入扩散生成框架，实现了对微表情（Micro-Expression, ME）的**精细粒度、情感一致且解剖协调的可控生成**。相较于现有方法，DiffME 在以下四个关键维度上实现了根本性突破：

### 1. 从二值标签到连续强度向量的 AU 控制方式

现有方法（如 **FAMGAN**，Xu et al., ACM MM 2021；**ULME-GAN**，Zhou et al., Applied Intelligence 2024）通常依赖二值 AU 标签或固定 AU 组合进行条件生成，缺乏对表情强度的精细调控能力。DiffME 将生成任务形式化为从起始帧（onset frame）和**21 维连续 AU 强度向量** $\mathbf{I}_{con} \in \mathbb{R}^{21}$ 预测顶点帧（apex frame），该向量涵盖 12 个 AU 及其面部侧化（facial laterality）信息，首次支持对 AU 强度和双侧对称性的独立精细控制。

### 2. 从无结构建模到 CPM 引导的 AU 关系建模

现有方法缺乏对 AU 之间共激活与抑制关系的显式建模，导致生成的表情可能在解剖学上不协调或情感上不连贯。DiffME 引入 **CPM 引导的 AU 关系模块（CARM）**，通过对可观测 ME 进行经验统计分析获得 AU 间的相关参数，并构建图卷积网络（GCN）对 21 个 AU 节点的共激活与抑制模式进行建模。GCN 的更新规则为：

$$\mathbf{h}_i^{(c+1)} = \mathrm{ReLU}\left( \sum_{j=1}^{21} \hat{A}_{ij} \cdot \mathbf{h}_j^{(c)} \cdot w_j \right)$$

其中 $\hat{A}_{ij}$ 为标准化的邻接矩阵，$w_j$ 为经验 AU 相关权重。这一设计使得生成的表情不仅在局部 AU 层面可控，在全局层面也符合情感表达的生理协调性。

### 3. 从无约束生成到自监督强度边界约束

现有方法未对 AU 运动强度设置上限，可能生成超出人类生理极限的夸张表情。DiffME 通过 **AU 分解形变估计器（ADDE）** 在自监督训练中从可观测样本分布估计每个 AU 的最大强度边界 $\mathbf{I}_{max} \in \mathbb{R}^{21}$，为生成过程提供生理约束。ADDE 利用起始-顶点帧对估计形变场，通过关键点区域的局部雅可比矩阵的 Frobenius 范数估计 AU 强度：

$$s_l = \frac{ \| \mathbf{J}_l \|_F }{ \| \mathbf{J}_l^{\max} \|_F }$$

这一机制确保生成的微表情运动幅度不会超出训练数据中观察到的生理极限。

### 4. 从特征拼接干扰到解耦身份保持机制

现有方法通常直接拼接身份特征与表情特征，容易导致特征干扰和身份信息丢失。DiffME 提出**身份-ME 解耦交叉注意力机制**，将身份嵌入 $f_{id}$ 和 ME 特征 $f_{ME}$ 通过独立投影计算交叉注意力，并以加权方式融合输出：

$$f_{\mathrm{ID-ME}} = \mathrm{Att}(Q, K_{\mathrm{id}}, V_{\mathrm{id}}) + \beta \cdot \mathrm{Att}(Q, K_{\mathrm{ME}}, V_{\mathrm{ME}})$$

同时引入 **ID-Net 身份拷贝网络**——一个完全克隆主 UNet 架构但仅在身份嵌入上条件化的并行分支，为生成过程提供逐层的身份一致性空间先验。这种双分支设计在保证表情可控性的同时，显著增强了身份保持能力。

### 创新点协同机制

上述四个创新点并非孤立存在，而是形成了一条完整的因果链路：ADDE 为 CARM 提供 AU 特定的形变表示和强度边界；CARM 基于 CPM 结构先验对 AU 关系进行建模，输出协调后的 AU 表示；这些表示作为条件输入**概率强度感知过渡扩散（PITD）**框架，通过解耦交叉注意力和 ID-Net 实现身份保持的可控生成；在推理阶段，通过分类器自由引导（CFG）的外推机制 $\tilde{\varepsilon}_\theta = \varepsilon_\theta + \lambda_{\mathrm{ME}} (\varepsilon_{\mathrm{ME}} - \varepsilon_\theta)$ 实现强度滑块式的精细调控。消融实验表明，移除 ADDE 或 CARM 中任一模块均会导致模型退化为基础潜在扩散模型，输出质量明显恶化，验证了这一协同设计的必要性。

DiffME 将微表情生成形式化为一个条件图像合成任务：给定起始帧 $F_{\text{onset}}$ 和一个细粒度的 AU 强度控制向量 $\mathbf{I}_{\text{con}} \in \mathbb{R}^{21}$，预测对应的顶点帧 $\hat{F}_{\text{apex}}$。其中 $\mathbf{I}_{\text{con}}$ 涵盖 12 个按面部侧化解耦的 AU，支持对强度和双侧对称性的精细调控。整个框架由三个核心模块串联构成，形成“自监督运动解耦—结构先验建模—强度感知扩散生成”的级联管线。

**AU-Decomposed Deformation Estimator (ADDE)** 作为管线前端，以起始-顶点帧对为输入，通过自监督运动编码器估计形变场 $\mathcal{T}_{F_{\text{onset}}F_{\text{apex}}}$。它将 AU 相关的关键点区域转化为高斯热力图，进而提取每个 AU 特定的局部雅可比矩阵，并通过 Frobenius 范数估计各 AU 的强度上限 $\mathbf{I}_{\max} \in \mathbb{R}^{21}$。这一强度边界从可观测样本分布中习得，为后续生成提供生理上限约束，防止生成的运动超越解剖学合理范围（图 3）。

**CPM-Guided AU Relational Module (CARM)** 接收 ADDE 输出的 21 个 AU 特定雅可比矩阵，利用图卷积网络对 AU 间的共激活与抑制关系进行建模。该模块以组件过程模型为理论指导，基于对可观测微表情的经验统计分析构建 AU 相关图——节点为 21 个 AU，边权重为 Pearson 相关系数（仅保留绝对值大于 0.1 的边，图 4 右）。GCN 的更新规则为：

$$\mathbf{h}_i^{(c+1)} = \mathrm{ReLU}\left( \sum_{j=1}^{21} \hat{A}_{ij} \cdot \mathbf{h}_j^{(c)} \cdot w_j \right)$$

其中 $\hat{A}$ 为标准化邻接矩阵，$w_j$ 为经验 AU 相关权重。CARM 输出的结构化 AU 表示作为条件注入下游扩散生成过程，确保生成的表情在情感维度上具有内在连贯性。

**Probabilistic Intensity-aware Transition Diffusion (PITD)** 是整个框架的生成核心（图 4 左）。它以起始帧的潜在编码和 CARM 导出的 AU 表示作为条件，在潜在空间中执行扩散去噪过程。为同时保证身份保持和表情可控性，PITD 引入两个关键设计：

1. **Identity-ME Decoupled Cross-Attention**：将身份嵌入 $f_{\text{id}}$ 和微表情特征 $f_{\text{ME}}$ 通过独立投影计算交叉注意力，最终输出为两者的加权和：
   $$f_{\text{ID-ME}} = \mathrm{Att}(Q, K_{\text{id}}, V_{\text{id}}) + \beta \cdot \mathrm{Att}(Q, K_{\text{ME}}, V_{\text{ME}})$$
   其中 $\beta = 0.8$。这种解耦设计避免了直接拼接带来的特征干扰和纠缠。

2. **ID-Net**：一个与主 UNet 架构完全相同的并行分支，但其交叉注意力层仅以身份嵌入 $f_{\text{id}}$ 为条件。ID-Net 提供逐层的身份一致空间先验，作为强身份正则器，确保主 UNet 在渲染目标微表情时不偏离个体身份。

在推理阶段，PITD 采用分类器自由引导实现强度控制：
$$\tilde{\varepsilon}_\theta(x_t, t, f_{\text{id}}, f_{\text{ME}}) = \varepsilon_\theta + \lambda_{\text{ME}} (\varepsilon_{\text{ME}} - \varepsilon_\theta)$$
其中 $\lambda_{\text{ME}}$ 作为强度滑块，通过外推调节生成表情的强度。较小的 $\lambda_{\text{ME}}$ 产生更接近起始帧的中性表情，较大的值则增强 AU 激活程度，但过大的值可能引入视觉伪影。

**输入输出流总结**：起始帧经预训练面部编码器提取身份嵌入 $f_{\text{id}}$；同时 ADDE 从训练数据中自监督估计各 AU 的强度上限 $\mathbf{I}_{\max}$；用户指定的目标强度向量 $\mathbf{I}_{\text{con}}$ 与 $\mathbf{I}_{\max}$ 共同约束 CARM，产出结构化 AU 条件表示 $f_{\text{ME}}$；$f_{\text{id}}$ 和 $f_{\text{ME}}$ 通过解耦交叉注意力注入 PITD 的主 UNet，ID-Net 并行提供身份先验，最终在潜在空间中解码生成顶点帧。三个模块形成紧耦合依赖：移除 ADDE 将使 CARM 无法工作，移除 CARM 则破坏 PITD 的强度估计，导致模型退化为基础潜在扩散模型，输出质量显著恶化。

![[assets/figures/papers/paper_list_l1651_DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Gen/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our Probabilistic Intensity-aware Transition Diffusion (PITD) pipeline. Left: Given onset image and target AU intensities, we extract identity embedding from a pretrained face encoder, and derive structured symmetry-aware AU representations via CARM. These two streams are fused through decoupled cross-attention to condition the primary UNet. A parallel UNet, ID-Net, is conditioned solely on the identity embedding to impose a strong identity constraint, ensuring identity preservation while the main UNet renders the desired ME. Right: Empirical AU correlation graph that informs the structural prior of CARM. For clarity, only edges with absolute correlation above 0.1 are displayed*

![[assets/figures/papers/paper_list_l1651_DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Gen/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of previous methods and our method. Top: Transfer-based methods restrict synthesis to fixed AU combinations. GAN-based methods fail to control intensities, causing affective incoherence. Bottom: Our method estimates intensity bounds in self-supervised manner and then models AU patterns guided by CPM to ensure affective and anatomical coherence*

DiffME 围绕三个核心模块构建：**AU‑Decomposed Deformation Estimator (ADDE)** 负责自监督运动解耦与强度边界估计；**CPM‑Guided AU Relational Module (CARM)** 将组件过程模型的结构先验注入 AU 关系建模；**Probabilistic Intensity‑aware Transition Diffusion (PITD)** 则通过解耦交叉注意力与身份拷贝网络实现可控生成。三个模块形成因果链条——ADDE 为 CARM 提供 AU 特定的雅可比表示与强度上界，CARM 输出结构化的 AU 条件信号，PITD 在此条件下完成从起始帧到顶点帧的扩散生成。

### ADDE：自监督变形估计与强度边界

ADDE 的核心目标是从可观测的起始‑顶点帧对中，自监督地估计每个 AU 的运动强度上界。给定起始帧 $F_{\mathrm{onset}}$ 和顶点帧 $F_{\mathrm{apex}}$，首先通过运动编码器估计二者之间的稠密变形场 $\mathcal{T}_{F_{\mathrm{onset}} F_{\mathrm{apex}}}$。为将全局变形场分解为 AU 特定的局部运动，ADDE 在 MediaPipe 提取的面部关键点 $p_k$ 处对变形进行一阶泰勒近似：

$$T_{F R}(p) \approx \mathcal{T}_{F R}(p_k) + \mathcal{T}_{p_k} \cdot (p - p_k)$$

其中 $\mathcal{T}_{p_k}$ 为关键点 $p_k$ 处的局部雅可比矩阵，刻画了该点邻域的旋转、缩放与剪切形变。为聚焦于 AU 相关区域，每个关键点被扩展为高斯热力图 $\mathcal{H}_{p_l}$，并与雅可比场逐元素相乘，得到 AU 特定的局部雅可比 $\mathbf{J}_l$。该雅可比的 Frobenius 范数自然反映了 AU 区域的形变强度：

$$\|\mathbf{J}_l\|_F = \sqrt{\sum_{m=1}^{2}\sum_{n=1}^{2} J_{l,mn}^2}$$

ADDE 在自监督训练过程中，从所有观测样本中统计每个 AU 的最大 Frobenius 范数 $\|\mathbf{J}_l^{\max}\|_F$，由此定义归一化 AU 强度与强度上界向量 $\mathbf{I}_{\max} \in \mathbb{R}^{21}$：

$$s_l = \frac{\|\mathbf{J}_l\|_F}{\|\mathbf{J}_l^{\max}\|_F}$$

该上界作为后续 PITD 中生成强度的生理约束，确保合成表情不超出训练分布中观测到的最大运动幅度。

### CARM：CPM 引导的 AU 关系图卷积

CARM 将组件过程模型（CPM）的情感结构先验转化为可学习的图约束。模块首先在可观测微表情数据上进行经验统计分析，获得 12 个基础 AU 之间的 Pearson 相关系数，并以此构建 AU 相关图（仅保留绝对相关系数大于 0.1 的边）。为处理面部侧化，12 个 AU 被扩展为 21 个节点（区分左右侧），邻接矩阵 $\hat{A}$ 经对称归一化后输入图卷积网络。第 $c$ 层的节点特征更新规则为：

$$\mathbf{h}_i^{(c+1)} = \mathrm{ReLU}\left(\sum_{j=1}^{21} \hat{A}_{ij} \cdot \mathbf{h}_j^{(c)} \cdot w_j\right)$$

其中 $w_j$ 为对应 AU 的经验相关权重，$\mathbf{h}_j^{(c)}$ 来自 ADDE 提取的 AU 特定雅可比表示。GCN 的输出是经过关系协调的 AU 特征，这些特征作为条件信号注入 PITD 的扩散 UNet，引导生成过程遵循解剖学上合理的共激活与抑制模式。

### PITD：解耦交叉注意力与身份保持

PITD 在潜在扩散框架中实现强度可控的顶点帧生成。其关键设计在于将身份嵌入 $f_{\mathrm{id}}$ 与微表情特征 $f_{\mathrm{ME}}$ 通过独立的投影矩阵映射为键值对，分别计算交叉注意力后加权融合：

$$f_{\mathrm{ID-ME}} = \mathrm{Att}(Q, K_{\mathrm{id}}, V_{\mathrm{id}}) + \beta \cdot \mathrm{Att}(Q, K_{\mathrm{ME}}, V_{\mathrm{ME}})$$

其中 $\beta=0.8$ 控制 ME 特征的贡献强度。这种解耦设计避免了朴素拼接带来的特征干扰。为进一步强化身份约束，PITD 引入 **ID‑Net**——一个完整克隆主 UNet 结构的并行分支，其交叉注意力层仅以 $f_{\mathrm{id}}$ 为条件，逐层提供身份一致的空间先验。主 UNet 在 ID‑Net 先验的引导下渲染目标微表情，从而在保持个体身份的同时实现精细的 AU 强度控制。

在推理阶段，PITD 采用分类器自由引导（CFG）实现强度滑块功能：

$$\tilde{\varepsilon}_\theta(x_t, t, f_{\mathrm{id}}, f_{\mathrm{ME}}) = \varepsilon_\theta + \lambda_{\mathrm{ME}} (\varepsilon_{\mathrm{ME}} - \varepsilon_\theta)$$

其中 $\varepsilon_\theta$ 为联合条件预测噪声，$\varepsilon_{\mathrm{ME}}$ 为仅以 ME 特征为条件的预测噪声。通过调节 $\lambda_{\mathrm{ME}}$，用户可在不改变 AU 组合的前提下连续控制生成表情的强度——较小的 $\lambda_{\mathrm{ME}}$ 趋向于保留起始帧的中性状态，较大的值则增强表情幅度。但需注意，过大的 $\lambda_{\mathrm{ME}}$ 会引入视觉伪影，这是 CFG 外推固有的局限性。

![[assets/figures/papers/paper_list_l1651_DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Gen/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the AU-Decomposed Deformation Estimator (ADDE). Given an onset–apex frame pair, ADDE employs a self-supervised motion encoder to estimate deformation fields*

![[assets/figures/papers/paper_list_l1651_DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Gen/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of ADDE in self-supervised image reconstruction. (a) Onset frame with AU annotations indicating micro-expression dynamics to appear in the upcoming (b) apex frame. (c) Reconstructed result of the apex frame. (d) Gaussian heatmap computed based on landmarks*

## 实验与关键发现

### 评估协议与基准设定

为了克服传统人工编码评估的主观性和不可复现性，DiffME 引入了基于视觉语言模型（VLM）和深度学习模型（DLM）的标准化评估方案。定量评估采用 **Leave-One-Dataset-Out (LODO)** 协议：在六个自发性微表情数据集（CASME、CASME II、SAMM、MMEW、4DME、CASME3）上，每次以其中一个数据集作为测试集，其余五个作为训练集，训练 AU 预测评估器。评估器在真实样本上训练后，对 DiffME 生成样本进行 AU 预测，以 **UF1** 和 **ACC** 作为核心指标。

### 主实验结果

Table 1 展示了 LODO 协议下不同评估器的定量对比。核心发现是：**DiffME 生成样本的 AU 预测性能与真实顶点帧（Ground-Truth Apex）紧密对齐，无明显退化**。具体而言，在不同 CFG 尺度（λ_ME）控制下，生成样本的 UF1/ACC 指标均能接近甚至匹配真实样本水平，验证了生成微表情在解剖学和情感维度上的保真度。

![[assets/figures/papers/paper_list_l1651_DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Gen/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of different evaluators under LODO protocol. For each column, the specified dataset is used for testing, and the remaining five for training. We report results on the original Ground Truth (GT) Apex frames and on frames generated by our method with varying micro-expression (ME) intensity, controlled by the CFG scale*

这一结果表明，DiffME 的 CPM 引导 AU 关系建模（CARM）与自监督强度边界估计（ADDE）协同工作，使得生成的运动模式在 AU 共激活与抑制关系上符合真实微表情的统计分布。

### 消融实验

消融实验揭示了各模块间的强耦合依赖关系：

- **移除 ADDE**：CARM 模块失去强度上界约束输入，无法正常工作。模型退化为基础潜在扩散模型（Latent Diffusion Model），输出质量明显恶化。
- **移除 CARM**：PITD 的强度估计失去 AU 关系结构先验，生成的表情缺乏情感连贯性和解剖协调性，同样导致输出退化。

这两种情况下，模型均无法维持可控微表情生成能力，证实了 ADDE → CARM → PITD 的级联依赖是方法有效性的结构性基础。

### 强度控制与失败模式

DiffME 通过分类器自由引导（CFG）实现强度滑块控制。Figure 6 展示了不同 λ_ME 尺度（0.5, 2.5, 4.5, 6.5）下的生成可视化：随着 λ_ME 增大，微表情强度逐步增强，验证了 PITD 框架对 AU 强度的连续可控性。

![[assets/figures/papers/paper_list_l1651_DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Gen/figures/007_Figure_6.jpg]]
*Figure 6: Visualization of DiffME-generated MEs under varying classifier-free guidance scales. From left to right: (a) input onset, (b) ground-truth apex, and (c)-(f) generated apex with*

然而，实验也揭示了明确的失败模式：**过大的 CFG 尺度（λ_ME）会产生视觉伪影**。这是由于 CFG 外推机制在过度放大条件信号时，可能破坏扩散过程的采样稳定性，引入不符合真实面部解剖的运动扭曲。

### 身份保持与生成质量

Figure 5 展示了 ADDE 的自监督重建能力：从起始帧（a）到真实顶点帧（b）的运动场估计能够高保真地重建顶点帧（c），高斯热力图（d）验证了 AU 相关关键点区域的形变聚焦。这为后续的强度边界估计提供了可靠的几何基础。

在身份保持方面，ID-Net 分支与 Identity-ME Decoupled Cross-Attention 的协同设计，使得生成的面部在呈现目标微表情的同时，保持与起始帧的身份一致性。消融表明，若将身份嵌入与 ME 特征简单拼接，会导致特征干扰和身份漂移。

### 局限性

尽管 DiffME 在可控微表情生成上取得了显著进展，仍存在以下限制：
- 将起始帧作为潜在空间条件输入，可能引入轻微的空间细节退化。
- 当前依赖手工选取的 MediaPipe 关键点和经验性 AU 相关图，限制了在更不受约束场景下的可扩展性。
- 过大的 CFG 尺度会产生视觉伪影，需要在强度控制与生成质量之间进行权衡。

## 定位与知识库关联

### 1. 与现有方法的对比与继承

DiffME 的核心贡献在于将心理学组件过程模型（CPM）的结构先验嵌入扩散生成框架，从而解决了现有微表情生成方法中两个关键瓶颈：**缺乏情感结构建模**和**无法实现精细强度控制**。从方法谱系上看，DiffME 与以下三类工作形成明确对比：

- **基于 GAN 的 AU 条件生成**：早期工作如 **FAMGAN**（Xu et al., ACM MM 2021）和 **ULME-GAN**（Zhou et al., Applied Intelligence 2024）采用 GAN 框架，以二值 AU 标签或固定 AU 组合作为条件生成微表情。这类方法的根本缺陷在于：AU 控制粗糙（仅有“激活/未激活”两种状态），且未显式建模 AU 间的共激活与抑制关系，导致生成结果缺乏情感连贯性。DiffME 将控制信号升级为 21 维连续强度向量（涵盖 12 个 AU 及其面部侧化），并通过 CARM 模块引入经验 AU 相关图引导的 GCN，从根本上改变了 AU 关系的建模方式。

- **基于运动迁移的方法**（如 Fan et al. 2021）：这类方法从驱动视频中提取运动模式并迁移到目标人脸，但其合成受限于观测到的 AU 组合，无法灵活控制单个 AU 的强度或对称性。DiffME 通过 ADDE 模块的自监督形变估计，将运动解耦为 AU 特定的变形表示，从而实现了独立于驱动视频的可控生成。

- **扩散模型在面部生成中的应用**：DiffME 继承了潜在扩散模型（Latent Diffusion Model）的架构范式，但其关键创新在于将身份与微表情特征通过解耦交叉注意力（Identity-ME Decoupled Cross-Attention）独立注入 UNet，并引入 ID-Net 身份拷贝网络提供逐层空间先验。这一设计直接回应了朴素拼接导致特征干扰的问题，其灵感可追溯至主题驱动生成中的解耦策略（如 Ye et al. 2023）。

### 2. 适用边界与能力范围

DiffME 的设计使其在以下条件下表现最优：

- **输入条件**：需要一张起始帧（onset frame）和一个 21 维 AU 强度向量。起始帧作为身份和初始状态的锚点，AU 向量提供精细的强度控制信号（包括双侧对称性）。
- **生成目标**：输出为对应的顶点帧（apex frame），即微表情强度达到峰值的单帧图像。
- **身份保持**：通过 ID-Net 的强约束，DiffME 在生成过程中能够较好地保持个体身份特征，避免因表情变化导致的面部形变溢出。
- **强度控制机制**：通过概率强度感知扩散（PITD）中的分类器自由引导（CFG），用户可通过调节 λ_ME 参数在推理阶段实现连续的强度滑块控制。

**当前适用边界**：
- DiffME 目前仅生成微表情的顶点帧，而非完整的动态序列。
- ADDE 模块依赖手工选取的 MediaPipe 面部关键点，CARM 模块依赖从可观测数据中统计得出的经验 AU 相关图。这意味着模型对关键点检测精度和统计先验的覆盖范围有较强依赖，在遮挡、大姿态等不受约束场景下的泛化能力受限。
- 起始帧被作为潜在空间中的条件输入，可能引入轻微的空间细节退化。

### 3. 局限性与已知失效模式

根据论文中的消融实验和定性分析，DiffME 存在以下已知局限：

- **模块依赖性**：ADDE 和 CARM 之间存在强耦合——移除 ADDE 会导致 CARM 无法获取 AU 特定的变形表示，移除 CARM 则会破坏 PITD 的强度估计。在两种情况下，模型均退化为基础潜在扩散模型，输出质量明显恶化。这表明系统的性能增益高度依赖各模块的协同工作，而非单一模块的贡献。
- **CFG 尺度的敏感性**：过大的 λ_ME 值会产生视觉伪影。这意味着强度控制存在一个有效区间，超出该区间后生成质量会下降。
- **手工先验的可扩展性瓶颈**：当前方法依赖 MediaPipe 关键点和经验性 AU 相关图，这些手工设计的先验限制了模型在更广泛面部形态和更不受约束场景下的可扩展性。

### 4. 开放问题与未来方向

DiffME 为微表情生成领域开辟了若干值得探索的方向：

- **数据驱动的结构先验学习**：当前 CARM 的经验 AU 相关图来自对可观测微表情的统计分析。一个自然的演进方向是：如何在数据驱动的方式下学习 AU 间的结构关系，而非依赖手工统计的先验？这可能涉及图结构学习或注意力机制的引入。
- **从单帧到序列的扩展**：DiffME 目前仅生成顶点帧。如何将其扩展至野外环境下的连续微表情序列生成，是实现动态微表情合成的重要一步。这需要解决帧间时间一致性和强度渐变控制的问题。
- **评估方案的标准化与推广**：DiffME 引入的基于视觉语言模型（VLM）和深度学习模型（DLM）的标准化评估方案，为替代传统人工编码评估提供了可复现的路径。这一评估范式的进一步完善和社区共识的建立，将是推动微表情生成领域公平比较的关键。

### 5. 知识库定位

DiffME 处于**可控面部生成**与**情感计算**的交叉点，其知识贡献可定位于：

- **面部动作单元生成**：首次将 CPM 心理学框架的结构先验嵌入扩散模型，实现了 AU 强度的精细控制和双侧对称性建模。
- **身份保持的可控生成**：通过解耦交叉注意力和 ID-Net 的设计，为需要在强身份约束下进行局部属性编辑的任务提供了可参考的架构方案。
- **自监督运动解耦**：ADDE 的自监督形变估计和强度边界推导，为无需显式运动标注的面部运动建模提供了新思路。

*注：由于分析中未提供论文的具体发表年份和会议信息，上述定位中的时间线比较需手动核实。*

## 原文 PDF

![[paperPDFs/PREPRINT_2025/DiffME_Component_Process_Model_Induced_Controllable_Micro_Expression_Generation.pdf]]

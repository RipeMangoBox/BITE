---
title: TriDi Trilateral Diffusion of 3D Humans Objects and Interactions
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions.pdf
project_link: null
code_link: null
aliases:
- TTD3HOI
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: TriDi
primary_logic: TriDi
claims:
- TriDi
---

# TriDi Trilateral Diffusion of 3D Humans Objects and Interactions

> [!tip] 核心洞察
> TriDi

| 字段 | 内容 |
|------|------|
| 中文题名 | TriDi Trilateral Diffusion of 3D Humans Objects and Interactions |
| 英文题名 | TriDi Trilateral Diffusion of 3D Humans Objects and Interactions |
| 会议/期刊 | ICCV 2025 |
| Links |  [paper](https://arxiv.org/abs/2412.06334)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method |  |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

**问题背景** 三维人体-物体交互（HOI）建模是计算机视觉与图形学中的核心挑战，涉及人体姿态、物体位姿以及两者之间交互关系的联合推理。现有方法大多采用单向生成范式，即给定部分条件生成另一部分，无法同时捕捉人体（H）、物体（O）与交互（I）三者的联合分布，导致生成结果在物理一致性和多样性方面存在局限。

**核心方法** TriDi 提出了一种统一的三维人体-物体交互建模框架，通过**三边扩散模型（Trilateral Diffusion）**首次实现对 H、O、I 联合分布的直接建模。该方法基于 UniDiffuser 范式构建，采用 Transformer 架构在统一的 token 空间中执行三向注意力机制，使得模型能够在七种不同条件组合模式下进行生成（如从物体推断人体与交互、从交互推断人体与物体等）。交互模态 I 通过融合接触图与文本描述在共享潜空间中表示，兼具几何精度与语义可控性。

**主要结果** 在 GRAB 与 BEHAVE 两个标准基准上，TriDi 在分布覆盖率和几何一致性方面均显著超越单向专用基线。以 BEHAVE 数据集上的 COV（覆盖率）指标为例，TriDi 达到 **47.81%**，较基线方法 GNet 的 40.71% 提升 **+7.10** 个百分点（Table 1）。定性结果表明，TriDi 生成的交互样本在避免穿透、保持接触合理性以及语义对齐方面均优于现有方法。

**方法定位** TriDi 属于**三维生成式 HOI 建模**这一新兴方向，区别于传统的回归式或检索式方法。其核心创新在于将扩散模型从单变量或双变量生成拓展至三变量联合分布学习，为下游应用（如场景填充、交互重建、文本驱动的交互编辑）提供了统一的概率框架。



三维人体-物体交互（Human-Object Interaction, HOI）建模是计算机视觉与图形学的核心挑战，其目标在于理解并生成人与物体在三维空间中的联合行为。该问题涉及三个相互耦合的模态：**人体 H**（包含姿态、体型与全局位姿）、**物体 O**（全局 6-DoF 位姿）以及**交互 I**（接触模式与语义描述）。现有方法通常沿两个方向展开：一类方法以人体为中心，在给定物体条件下预测人体姿态；另一类则以物体为中心，根据人体动作推断物体位姿。然而，这些方法普遍存在一个根本性局限——它们仅建模单向或双向的条件分布（如 $p(\mathcal{H}|\mathcal{O})$ 或 $p(\mathcal{O}|\mathcal{H})$），而非三者之间的联合分布 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$。

这一设计选择导致了若干关键缺口。首先，单向模型无法自然地处理多模态条件下的推理任务，例如同时给定部分人体信息和交互语义来恢复完整场景。其次，由于缺乏对交互模态的显式建模，现有方法难以保证生成结果在物理接触和语义层面的一致性。再者，确定性回归框架无法捕捉 HOI 数据中固有的多模态不确定性——同一物体条件下可能存在多种合理的人体姿态，反之亦然。

扩散模型在图像与运动生成领域的成功为上述问题提供了新的解决思路。扩散模型通过逐步去噪过程学习复杂数据分布，天然具备表达多模态不确定性的能力。然而，将扩散模型应用于三维 HOI 生成面临两个核心挑战：其一，如何构建一个统一的架构来同时处理人体、物体和交互三种异构模态的联合分布；其二，如何设计有效的交互表示，使其既能编码细粒度的接触几何信息，又能融合高层语义控制。

本文提出的 **TriDi**（Trilateral Diffusion）正是针对上述缺口而设计。TriDi 的核心动机在于：通过三边扩散框架直接建模 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$ 的联合分布，使模型能够在任意条件组合下进行推理与生成。同时，TriDi 将接触图与文本描述映射到共享的潜在空间作为交互表示，继承了接触几何的精确性与自然语言的灵活性。这一设计使得 TriDi 成为首个能够在全部七种条件模式下运行（即 $p(\mathcal{H},\mathcal{I}|\mathcal{O})$、$p(\mathcal{O},\mathcal{I}|\mathcal{H})$、$p(\mathcal{H},\mathcal{O}|\mathcal{I})$ 及其边际分布）的统一 HOI 生成模型，显著突破了现有单向专用模型的适用范围。



## 核心方法与创新机理

TriDi 的核心创新在于将人-物交互（HOI）建模从传统的单向条件生成提升为**三边联合扩散（Trilateral Diffusion）**，直接建模人（H）、物（O）与交互（I）三者的联合分布 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$。这一设计使得模型天然具备双向/多向条件推理能力，可在七种不同模式下运行（见 Fig. 1），而现有基线方法通常仅针对单一条件方向进行专门化设计。

在技术实现上，TriDi 基于 UniDiffuser 范式构建三路扩散过程，通过 **token-wise attention** 机制在 Transformer 架构内统一处理三类模态的 token 化表示。与单向基线相比，关键的 **changed slot** 在于扩散目标从单一变量扩展为三个变量的同步去噪，训练时对 $\mathcal{H}$、$\mathcal{O}$、$\mathcal{I}$ 分别采样独立的时间步 $t^{\mathcal{H}}, t^{\mathcal{O}}, t^{\mathcal{I}}$，并在统一的损失框架下联合优化。

另一重要创新在于**交互模态的表示设计**：TriDi 将接触图（contact map）与文本描述映射到共享的联合潜空间 $\mathbf{z}_{\mathcal{T}}$，从而同时继承了几何精确性和语义可控性的优势。这一 Contact-Text 联合编码（Fig. 3）使得交互信息既能从数据中自动提取接触约束，又能通过自然语言提供用户控制，为生成过程引入了此前方法不具备的细粒度交互推理能力。

在采样阶段，TriDi 引入**重建引导（reconstruction guidance）**机制，在每一步去噪时对生成的 $\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}$ 施加基于物理约束的梯度修正，进一步提升了生成结果中人与物的几何一致性。

综合来看，TriDi 通过将生成建模从“单向条件”升级为“三边联合”、将交互表示从单一模态扩展为 Contact-Text 融合、以及引入重建引导，构成了其在 BEHAVE 基准上 COV 指标提升 +7.10（47.81 vs. GNet 40.71）的核心技术动因。



TriDi 构建了一个**三边扩散（Trilateral Diffusion）**框架，统一建模人体（Human H）、物体（Object O）与交互（Interaction I）的联合分布 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$。其核心架构是一个基于 Transformer 的扩散模型，对三个模态的 token 化表征进行联合去噪，通过 token-wise attention 实现三向信息流动。

### 输入输出流

框架接收三类输入，其中仅物体表征 $\mathcal{C}_\mathcal{O}$ 为必选项，其余视运行模式灵活配置：

- **人体 H**：分解为 SMPL+H 姿态参数 $\theta_\mathcal{H}$、体型参数 $\beta_\mathcal{H}$ 和 6-DoF 全局位姿 $\mathbf{g}_\mathcal{H}$。
- **物体 O**：由规范几何特征与类别 one-hot 编码构成条件表征 $\mathcal{C}_\mathcal{O} = (f_\mathcal{O}, y_\mathcal{O})$，扩散对象为 6-DoF 全局位姿 $\mathbf{g}_\mathcal{O}$。
- **交互 I**：通过一个共享的紧凑隐码 $\mathbf{z}_\mathcal{T}$ 表示，该隐码由接触图（contact map）与 CLIP 文本嵌入联合映射得到（见图 3），继承了两者的互补优势。

### 扩散流程

TriDi 的扩散过程遵循 DDPM 范式。前向过程对 $\mathcal{H}$、$\mathcal{O}$、$\mathcal{I}$ 三个模态独立施加噪声：

$$q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\mathbf{z}_t; \sqrt{1 - \beta_t} \mathbf{z}_{t-1}, \beta_t \mathbf{I})$$

训练时，模型从数据分布 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$ 采样原始样本，对各模态独立采样时间步 $t^\mathcal{H}, t^\mathcal{O}, t^\mathcal{I} \sim \mathcal{U}(0, T)$，经前向扩散加噪后，由去噪网络 $\psi$ 预测原始样本 $\mathbf{z}_0$，最小化重建损失。

### 重建引导

在推理的每一步去噪中，TriDi 引入**重建引导（Reconstruction Guidance）**来增强生成质量。具体而言，对当前估计的 $(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}})$ 计算接触图一致性损失 $\mathcal{F}$（通过阈值化人-物距离得到二值接触图），并以引导尺度 $\lambda$ 沿梯度方向更新：

$$(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}) := (\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}) - \lambda \nabla_{\mathcal{H}^t, \mathcal{O}^t, \mathcal{I}^t} \mathcal{F}(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}})$$

这一机制使生成结果在物理合理性（如减少穿透）上得到显著改善。

### 模块关系总结

整体 pipeline 可归纳为三个关键模块的串联：**多模态表征编码**（将人体参数、物体位姿、交互接触-文本映射为统一 token 空间）→ **三边联合扩散 Transformer**（对三个模态执行独立时间步加噪与联合去噪）→ **重建引导优化**（利用接触图约束细化去噪输出）。该设计使 TriDi 成为唯一能覆盖全部七种运行模式（含无条件生成、单条件、双条件及联合生成）的统一框架。

### 补充图表

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/002_Figure_2.jpg]]
*Figure 2: TriDi Overview. TriDi is a Trilateral Diffusion for Human H (pose*



### 三变量联合分布建模

TriDi 的核心目标是建模人（Human）$\mathcal{H}$、物体（Object）$\mathcal{O}$ 和交互（Interaction）$\mathcal{I}$ 的三变量联合分布 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$。模型基于 UniDiffuser 范式，通过 token-wise 注意力机制实现三向扩散（Trilateral Diffusion），在统一的 Transformer 架构中对三个模态的 token 化表示进行联合去噪。

### 模态表示

**人体表示** $\mathcal{H}$ 被分解为三个组成部分：
$$
\mathcal{H} = (\theta_{\mathcal{H}}, \beta_{\mathcal{H}}, \mathbf{g}_{\mathcal{H}})
$$
其中 $\theta_{\mathcal{H}}$ 为 SMPL+H 姿态参数，$\beta_{\mathcal{H}}$ 为体型参数，$\mathbf{g}_{\mathcal{H}}$ 为 6-DoF 全局位姿。

**物体表示** 分为规范几何特征与类别编码 $\mathcal{C}_{\mathcal{O}} = (f_{\mathcal{O}}, y_{\mathcal{O}})$ 以及可扩散的 6-DoF 全局位姿 $\mathcal{O} = (\mathbf{g}_{\mathcal{O}})$。$\mathcal{C}_{\mathcal{O}}$ 是 TriDi 唯一必需的 conditioning 输入，其余输入根据操作模式可选。

**交互表示** $\mathcal{I}$ 通过 Contact-Text 联合潜在空间编码为紧凑的潜在码 $\mathcal{T} = (\mathbf{z}_{\mathcal{T}})$。该编码器（Figure 3）将接触图 $E_{\phi_{\mathcal{I}}}$ 与 CLIP 文本嵌入 $E_{T_{\mathcal{I}}}$ 映射到共享潜在空间，使模型同时继承几何接触约束与语义控制能力。

### 三向扩散过程

TriDi 对 $\mathcal{H}$、$\mathcal{O}$、$\mathcal{I}$ 分别施加独立的前向扩散过程。单步前向加噪遵循标准 DDPM 形式：
$$
q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\mathbf{z}_t; \sqrt{1 - \beta_t} \mathbf{z}_{t-1}, \beta_t \mathbf{I})
$$

训练目标为 $\mathbf{x}_0$-prediction 形式的去噪损失，对三个模态同时优化：
$$
\min_{\psi} \mathbb{E}_p \mathbb{E}_t \mathbb{E}_q \left[ \mathcal{D}_{\psi}(\mathbf{z}_t; c, t) - \mathbf{z}_0 \right]
$$

其中期望定义为：
$$
\mathbb{E}_p \equiv \mathbb{E}_{(\mathcal{H}^0,\mathcal{O}^0,\mathcal{Z}^0) \sim p(\mathcal{H},\mathcal{O},\mathcal{T})}, \quad \mathbb{E}_t \equiv \mathbb{E}_{(t^{\mathcal{H}},t^{\mathcal{O}},t^{\mathcal{T}}) \sim \mathcal{U}(0,T)^3}
$$

即从数据分布采样三元组，并为每个模态独立采样扩散时间步。

### 重建引导（Reconstruction Guidance）

在推理阶段，TriDi 在每个去噪步施加重建引导，以增强生成结果与 conditioning 的一致性。更新规则为：
$$
(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}) := (\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}) - \lambda \nabla_{\mathcal{H}^t, \mathcal{O}^t, \mathcal{I}^t} \mathcal{F}(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}})
$$
其中 $\lambda$ 为引导尺度，$\mathcal{F}$ 为基于去噪预测 $\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}$ 计算的重建损失函数。接触图通过计算人-物距离并阈值化获得，作为 $\mathcal{F}$ 中交互一致性约束的基础。

### 关键设计要点

- **唯一必需 conditioning**：仅 $\mathcal{C}_{\mathcal{O}}$ 为必选输入，其余模态可根据七种操作模式灵活设置为条件或生成目标。
- **共享潜在空间**：交互模态的 Contact-Text 联合编码使模型同时具备几何精度与语义可控性。
- **独立时间步采样**：三个模态各自采样扩散时间步，增强联合分布建模的灵活性。

### 补充图表

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of Contact-Text Interactions model. We train a mapping from the contact map*



## 实验与关键发现

### 生成分布质量

TriDi 在 BEHAVE 和 GRAB 两个数据集上评估了生成样本的分布覆盖能力，主要指标为覆盖率（COV）。**Table 1** 报告了核心结果：在 BEHAVE 数据集上，TriDi 在 H, I|O 模式下的 COV 达到 **47.81%**，相比最强基线 GNet 的 40.71% 提升了 **+7.10 个百分点**；在 O, I|H 模式下 COV 为 51.71%，同样显著优于所有单向专用基线。GRAB 数据集上，TriDi 在 H, I|O 和 O, I|H 模式下分别达到 42.87% 和 48.84% 的 COV，最高提升幅度达 47%。

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/005_Table_1.jpg]]
*Table 1: Quality of Generated Distribution. TriDi is the only one operating in all the modalities and shows better capability in covering data distribution, improving up to 47%*

TriDi 是唯一能够覆盖全部 7 种操作模态的方法，而基线方法（如 GNet、I-MultiNet 等）仅支持部分条件生成模式。这种全模态能力源于三向扩散对 Human、Object、Interaction 联合分布的直接建模，而非多个单向模型的拼接。

### 几何一致性

**Table 2** 从人体与物体的几何一致性角度评估生成质量。TriDi 在人体预测和物体预测两方面均展现出高水平的空间一致性。接触预测结果表明，网络已学会基于交互模态进行推理——接触图准确率同时报告了所有接触点和手部接触点的指标，验证了交互表征在引导生成中的实际作用。

### 消融实验

**Table S6** 和 **Table S7** 系统消融了三个关键设计选择对生成分布质量和几何一致性的影响：

1. **数据增强**：移除增强后，分布覆盖率和几何一致性均出现明显下降，表明增强策略对模型泛化至多样化的 HOI 场景至关重要。
2. **交互扩散（I diffusion）**：将交互模态从扩散过程中剥离会显著损害生成质量，验证了三向联合建模的必要性——交互不仅是条件信号，更是需要被扩散建模的核心变量。
3. **重建引导（reconstruction guidance）**：去除引导后，生成样本的几何一致性恶化，说明引导机制在约束生成结果符合物理合理性方面发挥了关键作用。

### 多样性与多模态性

**Table S4** 评估了所有采样模式下生成分布的多样性和多模态性。TriDi 生成分布的方差与真实数据（GT）的方差相当，表明生成的样本具有非平凡性（non-trivial），即模型没有退化为仅输出单一或高度相似的样本。同时，高接触准确率进一步说明多样性并未以牺牲物理合理性为代价。

### 交互条件生成

**Table S5** 专门评估了 H, O|I 模式（从交互生成人体和物体）。TriDi 在从接触图和文本查询两种交互条件采样时均优于 s-TriDi-HO。值得注意的是，文本条件比接触图提供更弱的约束，因此生成的分布多样性略有降低，但整体质量仍然保持在较高水平。

### 穿透分析

**Table S8** 进行了穿透（penetration）分析，量化了生成结果中人体与物体之间的相互穿透程度。TriDi 在该指标上表现优异，进一步佐证了重建引导和三向联合建模对维持物理一致性的贡献。

### 用户研究

**Table S2** 汇总了用户研究结果。人类评估者在多个维度上对 TriDi 的生成结果进行了偏好判断，为定量指标的提升提供了主观验证支撑。

### 失败模式与局限性

尽管 TriDi 在覆盖率和一致性指标上全面领先，但仍存在以下局限：

- **精细手部细节**：生成的 SMPL+H 手部姿态在细节上可能不够精确。论文提出了可选的后处理优化步骤（见 **Figure S6**），通过优化过程改善手部细节，但这并非模型内生的解决方案。
- **文本条件相对弱约束**：如 Table S5 所示，当仅依赖文本作为交互条件时，生成多样性虽高但精度略低于接触图条件，表明文本到接触的隐式映射仍有改进空间。
- **跨数据集泛化**：论文在 InterCap 和 OMOMO 数据集上展示了示例（Figure S7、S8），但未提供系统的跨数据集定量评估，泛化能力需进一步验证。

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/017_Table_S.5.jpg]]
*Table S.5: Quality of Generated Distribution for H, O|I. TriDi outperforms s-TriDi-HO in both sampling from contact maps and text queries. Text provides weaker conditioning than contact maps, thus the resulting distribution exhibits slightly less diversity*

### 与 COINS 的比较

**Table S3** 将 TriDi 与 COINS 进行了对比。TriDi 在生成质量上表现更优，具体指标差距需查阅原表确认。这一比较表明三向扩散框架相对于基于拼接的多模型方案具有结构性优势。

### 补充图表

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/006_Table_2.jpg]]
*Table 2: Geometrical Consistency of Generation. TriDi shows a high level of consistency both for human and object predictions. Our contact prediction indicates the networks have also learned to reason based on the interaction modality. For contacts, we show both the accuracy of contacts inferred from H and O meshes, as well as diffused contacts I (when available)*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/008_Figure_6.jpg]]
*Figure 6: Scene populating. Using 3D scans from HPS [27], we validate the practicality of TriDi for scene population in various conditioning cases. On the left, we demonstrate conditional synthesis of human-object interactions. On the right, TriDi is used for the joint generation of humans and objects*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/009_Figure_7.jpg]]
*Figure 7: Interaction reconstruction. DECO [78] annotates human H and contact I for the RGB image, while our TriDi recovers the object O, showing generalization on unseen data distributions*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/020_Table_S.6.jpg]]
*Table S.6: Ablation - Quality of Generated Distribution. Impact of augmentation, I diffusion, and guidance*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/021_Table_S.7.jpg]]
*Table S.7: Ablation - Geometrical Consistency of Generation. Impact of augmentation, I diffusion, and guidance*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/016_Table_S.4.jpg]]
*Table S.4: Evaluation of diversity and multi-modality for all sampling modes. The variance of the distribution generated by TriDi is on par with the variance of the GT data, which means that the generated samples are non-trivial. At the same time high contact accuracy (96.3 on average) and contact presence (98.4 on average) hint that generated interactions are plausible*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/022_Table_S.8.jpg]]
*Table S.8: Penetration analysis*

![[assets/figures/papers/paper_list_l1778_TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions/figures/004_Figure_4.jpg]]
*Figure 4: Comparison with baselines. In the two left-most columns, we show three samples for p(H, I|O) and p(O, I|H) from BEHAVE and GRAB test sets. TriDi’s generations are better aligned with the condition, causing less interpenetration (e.g., for basketball), respecting fine-grained details (e.g., for smaller objects), and demonstrating more diversity for limbs not restricted by contacts (e.g., for yoga ball). On the right, TriDi is the only model that can sample from p(H, O, I)*



## 定位与知识库关联

### 1. 方法谱系

TriDi 的核心技术路径建立在 **UniDiffuser** 范式之上，将其从双变量联合分布扩展为三变量联合分布建模。具体而言，TriDi 通过 token-wise attention 机制实现人体（H）、物体（O）与交互（I）的三向扩散，建模联合分布 $p(\mathcal{H}, \mathcal{O}, \mathcal{I})$。这一设计使其成为目前唯一能够覆盖全部七种操作模式（即任意条件组合下的生成与重建）的 HOI 生成模型。

在交互表征层面，TriDi 融合了两条技术路线：**接触图（contact maps）** 与 **文本描述**。论文指出，现有方法或依赖接触图提供细粒度空间约束，或利用文本提供语义灵活性，而 TriDi 将二者映射至共享的联合潜空间 $\mathbf{z}_{\mathcal{T}}$，同时继承了两者的优势。该交互编码器的架构包含接触图编码器 $E_{\phi_{\mathcal{I}}}$ 与 CLIP 文本嵌入 $E_{T_{\mathcal{I}}}$，通过联合训练实现跨模态对齐。

从生成范式角度看，TriDi 属于 **基于 Transformer 的扩散模型**，其前向扩散过程遵循标准 DDPM 公式：

$$q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\mathbf{z}_t; \sqrt{1 - \beta_t} \mathbf{z}_{t-1}, \beta_t \mathbf{I})$$

训练目标为预测原始样本 $\mathbf{z}_0$。在推理阶段，TriDi 引入 **重建引导（reconstruction guidance）** 机制，在每一步去噪时施加约束：

$$(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}) := (\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}}) - \lambda \nabla_{\mathcal{H}^t, \mathcal{O}^t, \mathcal{I}^t} \mathcal{F}(\hat{\mathcal{H}}, \hat{\mathcal{O}}, \hat{\mathcal{I}})$$

其中 $\lambda$ 为引导尺度，$\mathcal{F}$ 为重建损失函数。这一机制确保了生成结果与给定条件的一致性。

### 2. 与基线方法的关系

论文在 BEHAVE 和 GRAB 两个数据集上进行了定量对比。根据 Table 1 的数据，TriDi 在分布覆盖度指标 COV（%）上显著超越单向专用基线：

- **BEHAVE 数据集**：TriDi 在 H,I|O 模式下 COV 达到 47.81%，较 **GNet** 的 40.71% 提升 7.10 个百分点；在 O,I|H 模式下达到 51.71%。
- **GRAB 数据集**：TriDi 在 H,I|O 模式下 COV 为 42.87%，在 O,I|H 模式下为 48.84%。

论文明确指出，TriDi 是唯一能够在所有模态组合下运行的模型，而基线方法通常仅针对单一条件方向（如给定物体生成人体）进行优化。定性结果（Figure 4）进一步显示，TriDi 的生成样本在条件对齐度上优于基线，表现为更少的穿透伪影（如篮球场景）和更自然的交互姿态。

需要注意的是，论文未提供基线方法 GNet 的具体作者、会议和年份信息，该方法的详细技术背景需手动核实。

### 3. 适用边界与局限

TriDi 的适用边界由其设计选择决定：

- **物体表征依赖**：TriDi 的唯一必需条件为物体表征 $C_{\mathcal{O}} = (f_{\mathcal{O}}, y_{\mathcal{O}})$，即物体规范几何特征与类别标签。这意味着模型无法在完全无物体信息的场景下运行。
- **交互编码的信息瓶颈**：交互模态通过接触图与文本的联合潜空间编码 $\mathcal{T} = (\mathbf{z}_{\mathcal{T}})$ 表示。尽管该设计实现了多模态融合，但压缩后的潜码可能丢失细粒度的接触语义，这在复杂交互场景下可能成为性能瓶颈。
- **数据集覆盖范围**：模型在 BEHAVE 和 GRAB 数据集上验证，这些数据集主要覆盖人与小型物体的交互。对于大规模场景或动态多物体交互，泛化能力尚待验证。

论文在开放问题层面提出了以下值得关注的方向：

- **场景级扩展**：Figure 6 展示了 TriDi 在 3D 场景扫描（HPS）中进行场景填充的初步验证，但该应用仍处于概念验证阶段，尚未进行系统性的定量评估。
- **分布外泛化**：Figure 7 展示了 TriDi 结合 DECO 进行交互重建的能力，表明模型在未见数据分布上具有一定泛化性，但该结论缺乏定量消融支持，需进一步验证。

### 4. 开放问题

基于当前证据，以下问题尚未得到充分解答：

1. **三向扩散的耦合机制**：论文未深入分析 H、O、I 三个扩散流之间的注意力交互模式，以及不同时间步调度策略对生成质量的影响。这一设计空间值得进一步探索。
2. **重建引导的敏感性**：引导尺度 $\lambda$ 的选取策略及其对生成多样性与一致性权衡的影响，在论文中未进行系统消融。
3. **与大规模预训练模型的关系**：TriDi 使用了 CLIP 文本嵌入，但未探讨与其他视觉-语言模型（如更强大的 VLM）结合的可能性，也未分析文本条件在零样本交互生成中的上限。
4. **计算效率**：三向扩散相较于单向或双向扩散的计算开销增加幅度，以及在实际部署中的可行性，论文未提供相关分析。

**证据强度说明**：上述方法定位与关系分析主要基于论文自身陈述（confidence 0.85–0.98）。基线方法 GNet 的技术细节及外部对比的公平性需结合原始文献手动核实。



## 原文 PDF

![[paperPDFs/ICCV_2025/TriDi_Trilateral_Diffusion_of_3D_Humans_Objects_and_Interactions.pdf]]

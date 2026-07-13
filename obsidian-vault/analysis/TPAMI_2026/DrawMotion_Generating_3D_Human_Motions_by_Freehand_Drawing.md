---
title: "DrawMotion: Generating 3D Human Motions by Freehand Drawing"
type: paper
paper_level: A
venue: TPAMI
year: 2026
pdf_ref: paperPDFs/TPAMI_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.pdf
project_link: null
code_link: "https://github.com/InvertedForest/DrawMotion"
aliases:
- DrawMotion
tags:
- TPAMI_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入自由手绘轨迹与火柴人作为额外控制条件，提供空间与肢体姿态的直接约束。
primary_logic: 多条件融合模块（MCM）的中间特征形成连续稠密分布，使得无需重新训练即可通过梯度引导实现严格的轨迹约束。
claims:
- DrawMotion 比纯文本方法减少用户操作时间约 46.7%。
- MCM 中间特征分布连续且稠密，而 ReMoDiffuse 特征分布离散不规则。
- "DrawMotion 在 StiSim（火柴人相似度）上显著超越 StickMotion（HumanML3D: 59.26% vs 41.50%），表明精细手绘控制有效。"
- HumanML3D test set 上 StiSim↑ = 59.26%
---

# DrawMotion: Generating 3D Human Motions by Freehand Drawing

> [!tip] 核心洞察
> 多条件融合模块（MCM）的中间特征形成连续稠密分布，使得无需重新训练即可通过梯度引导实现严格的轨迹约束。

| 字段      | 内容                                                                                                                                            |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | DrawMotion：通过徒手绘草图生成三维人体动作                                                                                                                    |
| 英文题名    | DrawMotion: Generating 3D Human Motions by Freehand Drawing                                                                                   |
| 会议/期刊 | TPAMI 2026 |
| Links | [paper](https://arxiv.org/abs/2605.20955) · [Code](https://github.com/InvertedForest/DrawMotion) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method  | DrawMotion                                                                                                                                    |
| Dataset | HumanML3D test set, KIT-ML test set, User Study                                                                                               |

> [!tip] 效果简介
> - HumanML3D test set 上，StiSim↑ 59.26% vs StickMotion 41.50% (+17.76%)。
> - KIT-ML test set 上，StiSim↑ 52.17% vs StickMotion 42.60% (+9.57%)。
> - User Study 上，Total Time (s)↓ 34.3 vs text-to-motion only (approx. 64.4) (-46.7%)。

## 概要

文本驱动的三维人体动作生成面临一个结构性瓶颈：自然语言难以精确传达动作的空间轨迹、肢体姿态与节奏细节，导致生成结果与用户意图之间存在不可忽视的偏差。DrawMotion 针对这一瓶颈，引入**自由手绘轨迹与火柴人草图**作为额外的空间控制条件，使用户能够以直观的视觉语言直接约束动作的路径与关键姿态。

该方法的核心洞察在于：多条件融合模块（MCM）的中间特征形成了一个**连续且稠密的分布空间**，这为训练无关的梯度引导提供了可能——无需重新训练模型，即可通过中间特征引导（IFG）使生成的动作严格对齐用户提供的轨迹。实验证据表明，MCM 的特征分布在 PCA 投影下呈现连续稠密形态，而 ReMoDiffuse 的特征分布则离散不规则（Figure 5），这一结构特性是 IFG 得以生效的因果基础。

在 HumanML3D 和 KIT-ML 两个基准数据集上，DrawMotion 在火柴人相似度（StiSim）指标上显著超越仅支持固定三姿态火柴人的 StickMotion（Wang et al., CVPR 2025），分别达到 59.26% vs 41.50% 和 52.17% vs 42.60%，验证了精细手绘控制的有效性。用户研究进一步表明，手绘方式相比纯文本描述可减少约 46.7% 的操作时间（34.3s vs 约 64.4s），显著提升了人机交互效率。

在方法谱系上，DrawMotion 位于文本条件扩散模型（如 MDM、MotionDiffuse）的延伸线上，但通过引入多模态空间条件与训练无关引导机制，开辟了从“语义生成”到“精确控制”的新路径。其 MCM 设计（区分 Draw Decoder 与 Text Decoder，分别采用点积注意力和高效注意力）和条件混合策略，为多条件融合提供了可复用的架构范式。



三维人体动作生成是计算机视觉与图形学中的核心问题，其目标是根据用户给定的控制信号合成自然、多样的人体运动序列。近年来，基于扩散模型（diffusion models）的文本驱动动作生成方法取得了显著进展，代表性工作包括 **MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）以及引入检索增强的 **ReMoDiffuse**。然而，这些方法均以纯文本作为唯一的控制条件，面临一个根本性瓶颈：**文本描述难以精确传达动作的空间轨迹与肢体姿态**。

具体而言，语言在表达连续的空间路径（如“走一个 S 形曲线并在此处举起左手”）时存在天然的模糊性。用户往往需要反复修改文本提示词来逼近预期效果，这一过程耗时且不可控。论文通过用户实验证实，纯文本方案的平均操作时间约为 64.4 秒，而引入手绘控制后降至 34.3 秒，**时间节省约 46.7%**（Table XII）。这一定量证据直接揭示了文本单一模态在空间控制精度上的结构性缺陷。

针对上述缺口，**StickMotion**（Wang et al., CVPR 2025）率先尝试引入火柴人（stickman）作为额外条件，但仅支持在三个固定位置放置姿态，且不包含轨迹信息，控制粒度仍然粗糙。DrawMotion 的动机正是突破这一局限：**引入自由手绘轨迹与任意位置火柴人作为互补控制条件**，在保留文本全局语义的同时，提供空间路径与局部肢体姿态的直接约束。

这一动机背后的核心洞察在于：多条件融合模块（MCM）的中间特征形成了连续且稠密的分布空间（Figure 5 的 PCA 投影显示，ReMoDiffuse 特征分布离散不规则，而 MCM 特征分布连续稠密）。这种连续分布为**训练无关的梯度引导**（Intermediate Feature Guidance, IFG）提供了数学基础——模型无需重新训练即可在推理时通过梯度更新严格对齐用户提供的轨迹约束，同时保持生成质量。这一机制将“控制精度”与“生成保真度”两个通常互斥的目标统一在同一框架下。



## 核心方法与创新机理

DrawMotion 的核心创新在于将**自由手绘草图**（轨迹 + 火柴人）作为显式控制条件引入扩散运动生成框架，突破了纯文本描述在空间轨迹与肢体姿态表达上的根本局限。这一设计衍生出三个相互耦合的关键机制，构成了方法的核心 changed slots。

### 1. 控制条件类型的根本性扩展

纯文本方法（如 **MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022））仅依赖语言描述控制生成，难以精确传达动作的空间路径与特定时刻的肢体姿态。DrawMotion 将控制条件扩展为 **文本 + 手绘轨迹 + 火柴人** 的三元组：2D 轨迹提供全局运动路径的空间约束，火柴人则以直观的线条图指定关键帧的肢体姿态。用户可以在轨迹的任意位置放置多个火柴人，实现对动作细节的精细控制。这一条件扩展直接解决了文本到动作生成中“用户意图与生成结果偏差”的核心瓶颈。

### 2. 多条件融合机制：从掩码自注意力到 MCM

传统的多条件融合通常采用基于掩码的自注意力机制。DrawMotion 设计了 **多条件模块（Multi-Condition Module, MCM）**，其关键改进体现在两个层面：

- **模态特化的条件解码器**：MCM 内部区分 **Draw Decoder** 和 **Text Decoder**。Draw Decoder 采用标准点积注意力，建模局部姿态与轨迹的帧间关系；Text Decoder 采用高效注意力，计算复杂度与序列长度线性相关，用于捕获全局语义。消融实验表明，这一“eff/dot”组合（文本用高效注意力，画图用点积注意力）在 KIT-ML 上取得了最佳 FID 0.135。

- **条件融合 + 潜在编码器结构**：MCM 通过 Condition Fusion 模块将手绘与文本条件注入运动特征的潜在空间，配合 Latent Encoder 进行特征变换。消融实验证实，这一结构显著优于传统掩码机制。

### 3. 训练无关的中间特征引导（IFG）

MCM 带来的一个深层性质是：其**中间特征形成了连续且稠密的分布**，而 ReMoDiffuse 等模型的特征分布则呈现离散、不规则的簇状结构（见 Fig. 5 的 PCA 可视化）。基于这一发现，DrawMotion 提出了 **训练无关的中间特征引导（Intermediate Feature Guidance, IFG）**——在推理阶段，通过梯度更新直接优化 MCM 中间层特征，使生成动作的轨迹与用户输入对齐，同时利用马氏距离（Mahalanobis Distance）裁剪异常更新以维持生成质量。IFG 无需额外训练，使得模型在部署后仍能灵活适配新的轨迹约束。

这三个创新点形成了一条清晰的因果链：**扩展控制条件**提供了空间约束的表达能力，**MCM 的模态特化融合**保障了异质条件的有效整合，**IFG** 则利用 MCM 连续特征空间的优良性质，以零训练成本实现了严格的轨迹对齐。



DrawMotion 的整体推理流程如 Figure 1 所示，其核心由三个关键模块串联构成：**条件编码**、**多条件融合（MCM）** 与**扩散去噪**。用户输入包含三类模态——一段自然语言描述、一条徒手绘制的 2D 轨迹，以及沿轨迹任意位置放置的若干火柴人姿态。这些异构输入分别经过冻结的 CLIP ViT‑B/32 文本编码器、轨迹编码器（六层 Conv1d）和预训练并冻结的火柴人编码器，被映射为统一的嵌入表示。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/001_Figure_1.jpg]]
*Figure 1: Pipeline of DrawMotion inference. In addition to the trainingbased guidance, a training-free guidance updates the intermediate feature of the model within the MD boundary to ensure that the generations meet the conditions while maintaining its fidelity*

编码后的条件进入多条件融合模块（Multi‑Condition Module, MCM）。MCM 内部采用**条件融合（Condition Fusion）** 机制，将手绘条件与文本条件注入运动特征的隐空间；同时，MCM 沿批次维度将数据划分为四段，分别对应四种条件组合——(text, draw)、(text, ∅)、(∅, draw)、(∅, ∅)——以确保模型在训练中学习到不同条件组合下的噪声预测能力。MCM 中的条件解码器针对不同模态进行了专门化设计：**Draw Decoder** 采用标准点积注意力，用于捕捉局部姿态与轨迹的帧间关系；**Text Decoder** 则采用高效注意力，以线性复杂度建模全局语义。

在扩散过程一侧，DrawMotion 采用 DDIM 作为反向去噪框架。前向过程逐步向原始动作序列添加高斯噪声，模型学习在给定文本与手绘条件下预测所添加的噪声。训练时，统一的监督目标由三部分损失组成：

$$\mathcal{L}_{\mathrm{final}} = \mathcal{L}_{\mathrm{motion}} + \mathcal{L}_{\mathrm{traj}} + \mathcal{L}_{\mathrm{stick}}$$

其中 $\mathcal{L}_{\mathrm{traj}}$ 强制生成动作的全局轨迹与真实轨迹对齐，$\mathcal{L}_{\mathrm{stick}}$ 约束火柴人姿态的还原精度。

推理阶段，除了训练中习得的条件引导外，还引入了一项**无需训练的中间特征引导（Intermediate Feature Guidance, IFG）**。IFG 直接在 MCM 的中间特征空间上执行梯度更新，利用该空间连续且稠密的分布特性（见 Figure 4–6 的 PCA 可视化），在不重新训练的前提下将生成动作的轨迹与用户手绘轨迹精确对齐，同时通过马氏距离（Mahalanobis Distance）裁剪异常更新以保持生成质量。

整体输入‑输出流可概括为：**手绘轨迹 + 火柴人 + 文本 → 编码器 → MCM 条件融合 → 扩散去噪 → 3D 人体动作序列**。Figure 3 完整展示了这一框架，其中左侧为扩散过程的前向与反向流程，右侧为包含四个输入编码器和多层 MCM 的网络结构。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/003_Figure_3.jpg]]
*Figure 3: The DrawMotion framework consists of the diffusion process (left) and the network structure (right). 1) The diffusion process includes a forward and a reverse process. In the forward process, original motions are augmented with Gaussian noise and fed into DrawMotion, which learns to predict the added noise based on textual descriptions and hand-drawn sketches. In the reverse process, user-provided textual descriptions and hand-drawn sketches are input into DrawMotion, enabling the gradual generation of motion sequences using the predicted noise. 2) In the DrawMotion architecture, both the stickman encoder and the text encoder are frozen, while the remaining modules are trainable. Encoded in...*



### 问题建模与扩散框架

DrawMotion 的核心任务是在手绘轨迹 $T$、火柴人姿态序列 $S$ 和文本描述 $T_{\text{text}}$ 的条件下生成符合意图的三维人体动作序列。动作序列表示为 $x \in \mathbb{R}^{L \times D}$，其中 $L$ 为帧数，$D$ 为每帧的关节表示维度。

模型采用 DDIM 作为反向去噪过程。前向扩散过程定义为：

$$q(\mathbf{x}_{1:T} | \mathbf{x}_0) = \prod_{t=1}^{T} q(\mathbf{x}_t | \mathbf{x}_{t-1}), \quad q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{\alpha_t} \mathbf{x}_{t-1}, (1 - \alpha_t) \mathbf{I})$$

训练时，模型学习预测添加的噪声 $\epsilon_t$，损失函数为：

$$\mathbb{E}_{\epsilon_t, t, x_0} \Big[ \big\lVert \epsilon_t - \epsilon_{\theta}(\mathbf{x}_t, t, L, C(\mathrm{draw}), C(\mathrm{text})) \big\rVert^2 \Big]$$

其中 $C(\mathrm{draw})$ 和 $C(\mathrm{text})$ 分别为手绘条件与文本条件的编码表示。

---

### 条件编码器

DrawMotion 包含三个核心条件编码器，将异构输入映射到统一嵌入空间：

- **Stickman Encoder**：将用户手绘的火柴人编码为嵌入向量。该编码器经过预训练并冻结，显著提升了模型性能。预训练采用自编码器结构，包含一个火柴人编码器和一个姿态解码器，解码器预测 $N$ 个候选三维姿态，损失函数为：

$$\ell_n = 0.1 \times \| \mathrm{limb\_offset}^{gt} - \mathrm{limb\_offset}^{pred} \|_2^2$$

$$\ell^{\mathrm{final}} = 10 \times \ell_k + \sum_{n=1}^{N} \ell_n, \quad \text{where } k = \arg\min \ell_n$$

候选损失的设计动机在于：当两个肢体在二维投影中靠近时，火柴人无法可靠区分左右肢体，通过预测多个候选姿态可缓解这一歧义。

- **Text Encoder**：采用 CLIP ViT-B/32 将文本描述编码为嵌入向量，提供全局语义约束。

- **Trajectory Encoder**：由六层 Conv1d 与激活函数组成，将二维轨迹编码为逐帧嵌入，提供空间位置约束。

---

### Multi-Condition Module (MCM)

MCM 是 DrawMotion 的核心融合模块，替代了传统基于掩码的自注意力机制。每个 MCM 内部包含一个 Condition Fusion 模块，将手绘条件和文本条件融入动作特征的潜在空间。

在训练时，MCM 沿批次维度将数据划分为四个分段 $(B_1, B_2, B_3, B_4)$，分别对应四种条件组合：(text, draw)、(text, $\emptyset$)、($\emptyset$, draw)、($\emptyset$, $\emptyset$)。这一设计使模型能够学习在不同条件缺失情况下的生成能力。

**条件解码器结构**是 MCM 的关键设计。针对不同模态的特性，采用两种不同的注意力机制：

- **Draw Decoder（点积注意力）**：用于处理局部姿态和轨迹信息，建模帧间关系：

$$e^{kv} = \mathrm{concat}((e^{m} \oplus e^{j}), e^{s}), \quad Q = FCN_1(e^{m}), \quad K, V = FCN_{2,3}(e^{kv})$$

$$D(Q, K, V) = \mathrm{softmax}(QK)V$$

- **Text Decoder（高效注意力）**：用于处理全局语义信息，计算复杂度与序列长度线性相关：

$$Q = \mathrm{softmax}(FCN_4(e^{m})), \quad K, V = FCN_{5,6}(\mathrm{concat}(e^{m}, e^{t}))$$

$$D(Q, K, V) = Q \cdot (\mathrm{softmax}(K^{\intercal})V)$$

消融实验（Table VII）表明，文本解码器采用高效注意力、画图解码器采用点积注意力（eff/dot 配置）在 KIT-ML 上获得最佳 FID 0.135。

---

### 条件混合策略

推理阶段，模型通过加权混合不同条件组合的预测噪声来控制生成过程：

$$\hat{\epsilon}_{\theta} = w_1 \cdot \epsilon_{\theta}(\text{text, draw}) + w_2 \cdot \epsilon_{\theta}(\mathcal{D}, \text{draw}) + w_3 \cdot \epsilon_{\theta}(\text{text}, \mathcal{D}) + w_4 \cdot \epsilon_{\theta}(\mathcal{D}, \mathcal{D})$$

其中 $\mathcal{D}$ 表示丢弃对应条件，权重满足 $w_1 + w_2 + w_3 + w_4 = 1$。消融实验（Table IX）表明，设置 $p(\hat{w}=w) = 50\%$ 并偏向手绘条件可获得最佳 FID 0.124。

---

### 统一监督损失

训练时采用三项损失联合监督：

$$\mathcal{L}_{\mathrm{final}} = \mathcal{L}_{\mathrm{motion}} + \mathcal{L}_{\mathrm{traj}} + \mathcal{L}_{\mathrm{stick}}$$

其中轨迹损失强制生成动作与真值之间的全局轨迹对齐：

$$\mathcal{L}_{\mathrm{traj}} = \big\| \mathrm{Traj}(\hat{x}(\mathrm{draw}, *)) - \mathrm{Traj}(x) \big\|_2^2$$

---

### Intermediate Feature Guidance (IFG)

IFG 是训练无关的轨迹对齐引导机制，其设计依赖于一个关键发现：MCM 的中间特征形成连续且稠密的分布（Figure 5 的 PCA 可视化证实了这一点，而 ReMoDiffuse 的特征分布则呈离散不规则状态）。这一连续空间使得梯度引导成为可能。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/006_Figure_5.jpg]]
*Figure 5: 2D PCA projection onto the first two principal components of ReMoDiffuse and DrawMotion. Sample size = 80,000 and diffusion step = 299*

IFG 在推理时对选定的 MCM 层中间特征进行 SGD 更新，以最小化生成轨迹与用户提供轨迹之间的差异。为防止过度更新导致生成质量下降，IFG 引入 **Mahalanobis 距离裁剪**：

$$M(F) = \sqrt{(F - \mu)^T \Sigma^{-1} (F - \mu)}$$

其中 $\mu$ 和 $\Sigma$ 为中间特征的多元分布参数。当更新后的特征偏离分布超过阈值 $\epsilon_{\text{MD}}$ 时，将其裁剪回边界内，从而在满足轨迹约束的同时保持生成动作的逼真度。Table II 给出了 IFG 的超参数分析，包括 SGD 迭代次数、学习率、选用的 MCM 层以及 MD 阈值等。

---

### 关键设计动机

MCM 中间特征的连续稠密分布是 IFG 得以工作的**因果机制**。Figure 4 的概念图对比了三种特征分布：(a) 普通模型形成离散簇，(b) MCM 形成相对连续的空间，(c) VAE 强制全潜在空间覆盖。Table I 的扰动实验进一步验证了这一特性：在不同扰动因子 $\lambda$ 下，DrawMotion 的 FID 保持稳定，表明中间特征空间具有良好的连续性和鲁棒性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/004_Figure_4.jpg]]
*Figure 4: Conceptual illustration of intermediate feature distributions. The dashed lines correspond to level sets of the probability density function. (a) Ordinary models yield discrete clusters, (b) MCM forms a relatively continuous space, and (c) VAE enforces full latent coverage. This schematic is supported by Table I*



## 实验与关键发现

### 核心实验设置

DrawMotion 在两个主流人体动作生成基准上评估：HumanML3D 测试集和 KIT-ML 测试集。所有实验均在 A800 GPU 上运行，推理批大小设为 16 以保证公平比较。评估指标包括标准的文本-动作匹配指标（FID、R-Precision、Diversity、Multimodality），以及针对手绘控制专门引入的两个指标：

- **StiSim（火柴人相似度）**：衡量生成动作中关键帧姿态与用户提供的火柴人之间的匹配程度。
- **Traj.Err（轨迹误差）**：衡量生成动作的全局运动轨迹与用户手绘轨迹之间的偏差。

### 主要结果

**火柴人控制精度显著领先。** 在 HumanML3D 测试集上，DrawMotion 的 StiSim 达到 59.26%，远超 StickMotion（Wang et al., CVPR 2025）的 41.50%，提升 +17.76 个百分点（Table III）。在 KIT-ML 测试集上，DrawMotion 的 StiSim 为 52.17%，同样显著优于 StickMotion 的 42.60%（+9.57 个百分点，Table IV）。这一差距表明，允许用户在轨迹上任意位置放置多个火柴人（而非仅固定 3 个姿态）对精细控制至关重要。

**文本-动作生成质量具有竞争力。** 在 FID、R-Precision 等传统指标上，DrawMotion 与 state-of-the-art 文本驱动方法（如 MDM、MotionDiffuse、ReMoDiffuse）保持可比水平，证明引入手绘条件并未损害基础生成质量。

**用户效率大幅提升。** 用户研究表明，DrawMotion 的手绘方式相比纯文本描述减少约 46.7% 的操作时间（Table XII：总时间从约 64.4 秒降至 34.3 秒）。用户无需反复修改冗长的文本描述来微调空间细节，而是直接通过轨迹和火柴人传达意图。

### 训练无关引导（IFG）的有效性

Intermediate Feature Guidance（IFG）是 DrawMotion 无需重新训练即可实现严格轨迹对齐的关键机制。其核心前提是：MCM 的中间特征空间形成连续稠密分布，使得梯度引导可行且稳定。

**特征分布验证。** Figure 5 的 2D PCA 投影对比显示，ReMoDiffuse 的特征呈极度离散、不规则的簇状分布，而 DrawMotion 的 MCM 中间特征呈现连续且稠密的分布。Figure 6 进一步表明，同时使用文本和手绘条件时，特征分布最为连续，为 IFG 提供了良好的优化空间。

**扰动实验。** Table I 显示，在特征空间上施加不同程度的扰动（λ 因子），MCM 结构下的 FID 退化远小于传统模型，证明连续分布对扰动的容忍度更高，IFG 可以在不严重损害生成质量的前提下进行梯度更新。

**超参数分析。** Table II 在 KIT-ML 上系统分析了 IFG 的关键超参数：
- 重复迭代次数（repeat）：适度增加可改善轨迹对齐，但过多会引入时间开销（Table XI 给出了不同 repeat 下的时间消耗）。
- 学习率（lr）和马氏距离阈值（ϵMD）：用于裁剪异常更新，防止生成偏离真实分布。

### 消融实验

**条件解码器结构。** Table VII 显示，在文本解码器中使用高效注意力（eff）、在手绘解码器中使用点积注意力（dot）的 eff/dot 组合，在 KIT-ML 上获得最佳 FID 0.135。这表明全局语义理解适合线性复杂度的高效注意力，而局部姿态和轨迹的帧间关系建模需要标准点积注意力的细粒度交互。

**MCM 结构。** Table VIII 验证了条件融合（Condition Fusion）和潜在编码器（Latent Encoder）两个组件的必要性。同时使用两者时 FID 最优；去掉条件融合（回退到传统掩码机制）或去掉潜在编码器（使用简单线性层）均导致性能下降。

**条件混合策略。** Table IX 探索了推理阶段不同条件组合的噪声预测加权混合。设置 $p(\hat{w}=w)=50\%$ 并偏向手绘条件（即增大 draw 相关项的权重）时获得最佳 FID 0.124，说明适度强调手绘控制有助于生成更符合用户意图的动作。

**火柴人数量。** Table X 显示，使用 7 个火柴人时 FID 达到最优，继续增加数量带来的提升微乎其微。这为实际应用提供了效率参考——用户无需绘制过多火柴人即可获得良好控制效果。

### 失败模式与局限

1. **文本-轨迹冲突。** 当用户提供的文本描述与手绘轨迹存在语义冲突时（例如文本要求“向前走”但轨迹画成圆形），IFG 可能需要大量重复迭代才能缓解矛盾。最终损失值仍需用户自行解读，并手动调整混合权重等超参数来权衡文本与手绘的影响力。

2. **火柴人左右歧义。** 火柴人编码器在自遮挡或极端视角下仍存在左右肢体混淆的问题。候选损失（candidate loss）机制通过预测多个候选姿态来缓解此问题，但无法完全消除歧义。这一局限需要手动验证，文中未给出在极端视角下的定量鲁棒性分析。

3. **IFG 的时间开销。** 虽然 IFG 无需训练，但其迭代更新增加了推理时间。Table XI 给出了不同 repeat 次数下的时间消耗，用户需在轨迹对齐精度和推理速度之间权衡。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/009_Table.jpg]]
*Table: III: Comparison on the HumanML3D test set. We mark the best result as red and the second best one as blue . Arrows indicate the desired direction of metrics: ↓ (lower is better), ↑ (higher is better), and → (closer to real data is better). TABLE IV: Comparison on the KIT-ML test set*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/011_Table.jpg]]
*Table: VII: Analysis on the Structure of Condition Decoders on the KIT-ML dataset. R-prec (top3) denotes R-precision (top3). Text/Draw denotes the Text/Draw Decoder. And dot/eff denotes the dot-product/efficient attention structure respectively. The row with a gray background is our best practice. TABLE IX: Ablation study on the condition mixture for the inference / reverse process on KIT-ML dataset. The row with a gray background is our best practice. TABLE X: Ablation study of the stickman number on KIT dataset. IFG was not applied to save time*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/012_Table.jpg]]
*Table: VIII: Analysis on the Structure of MCM on the KIT-ML dataset. Rows without in the column “Condition Fusion” mean use of the traditional mask mechanism. Rows without $\surd$ in the column ”Latent Encoder” mean a simple linear layer is used. The row with a gray background is our best practice*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/007_Table.jpg]]
*Table: I: Comparison of FID under different perturbation factors λ. Lower is better*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/008_Table.jpg]]
*Table: II: Hyperparameter analysis of Intermediate Feature Guidance (IFG) on KIT-ML dataset. Here, repeat denotes the number of SGD iterations, lr is the learning rate of this update, $N _ { t h }$ layer specifies the selected MCM layer for guidance, ϵMD is the Mahalanobis distance threshold used for clipping abnormal updates, and λ is the clip scale*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/015_Table.jpg]]
*Table: XII: Comparison between stickman & text-to-motion and text-to-motion task. “TA” and “TB” represent the time cost for overall and detailed descriptions, respectively, while “TD” denotes the time required for hand-drawing. “TI” represents the inference time of the utilized model. For Handmade animation, the trajectory is fixed and no textual input is required. all experiments are conducted on an A800 GPU with a batch size of 1*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/013_Figure_7.jpg]]
*Figure 7: Visualization of DrawMotion (see the animation on GitHub)*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_20955/figures/005_Figure_6.jpg]]
*Figure 6: 2D PCA projection onto the first two principal components of different condition settings in DrawMotion. Sample size = 20,000 and diffusion step = 299*



## 定位与知识库关联

### 1. 问题定位：从文本到多模态控制的范式迁移

传统文本驱动动作生成（text-to-motion）的核心瓶颈在于：自然语言难以精确传达动作的空间轨迹与肢体姿态细节，导致生成结果与用户意图之间存在显著偏差。DrawMotion 的回应是将控制条件从单一文本扩展为“文本 + 手绘轨迹 + 火柴人”的多模态组合，从而在空间约束和姿态约束两个维度上提供直接的用户控制。

这一思路的直接前驱是 **StickMotion**（Wang et al., CVPR 2025），后者首次引入火柴人作为额外条件，但仅在动作序列中固定放置 3 个姿态，且不包含轨迹信息。DrawMotion 在此基础上做出两项关键推进：（1）允许用户在任意轨迹位置上放置任意数量的火柴人姿态；（2）引入显式的 2D 轨迹条件，使空间路径成为可控变量。

### 2. 与扩散动作生成基线的结构关系

DrawMotion 的扩散骨架建立在 **MDM**（Tevet et al., arXiv 2022）和 **MotionDiffuse**（Zhang et al., arXiv 2022）等文本驱动扩散模型的基础之上，但在条件融合机制上做出了根本性改变。

| 方法 | 条件类型 | 融合机制 | 轨迹对齐 |
|------|---------|---------|---------|
| MDM | 仅文本 | 基于掩码的自注意力 | 无 |
| MotionDiffuse | 仅文本 | 交叉注意力 | 无 |
| StickMotion | 文本 + 固定火柴人 | 掩码机制 | 无 |
| **DrawMotion** | 文本 + 轨迹 + 任意火柴人 | 多条件模块（MCM） | 训练无关中间特征引导（IFG） |

关键差异在于：基线方法普遍采用掩码或交叉注意力进行条件注入，而 DrawMotion 设计了 **Multi-Condition Module（MCM）**，其核心创新是区分了 Draw Decoder（标准点积注意力，用于局部姿态和轨迹的帧间建模）和 Text Decoder（高效注意力，计算复杂度与序列长度线性相关，用于全局语义融合）。消融实验（Table VII）证实，这种“文本用高效注意力、画图用点积注意力”（eff/dot）的配置在 KIT-ML 上获得最佳 FID 0.135。

### 3. 核心洞察：连续特征空间与训练无关引导

DrawMotion 最具理论价值的设计在于 **Intermediate Feature Guidance（IFG）** 的可行性基础。分析揭示（Figure 4, Figure 5）：MCM 的中间特征在 PCA 投影下呈现连续且稠密的分布，而 **ReMoDiffuse** 的特征分布则呈现离散且不规则的聚类。这一性质使得 IFG 可以在不重新训练的情况下，通过对中间特征进行梯度更新来实现严格的轨迹约束——本质上是在一个连续流形上进行梯度引导，而非在离散簇之间跳跃。

IFG 的具体实现涉及马氏距离裁剪（Mahalanobis Distance clipping），公式为 $M(F) = \sqrt{(F - \mu)^T \Sigma^{-1} (F - \mu)}$，用于将更新限制在特征分布的合理边界内，以维持生成质量。Table I 展示了不同扰动因子 λ 下的 FID 变化，Table II 则给出了 IFG 的超参数分析（重复迭代次数、学习率、MCM 层选择、MD 阈值等）。

### 4. 适用边界与局限

**适用场景**：DrawMotion 在需要精细空间控制的任务中具有明显优势。用户研究表明，手绘方式相比纯文本方法减少约 46.7% 的操作时间（Table XII）。在 StiSim（火柴人相似度）指标上，DrawMotion 在 HumanML3D 上达到 59.26%，显著超越 StickMotion 的 41.50%（Table III）；在 KIT-ML 上同样保持领先（52.17% vs 42.60%，Table IV）。

**已知局限**：
- **文本-轨迹冲突**：当用户提供的文本语义与轨迹存在严重冲突时，IFG 可能需要大量重复迭代才能缓解，且最终损失仍需用户解读并手动调整超参数。这是一个尚未被系统解决的开放问题。
- **火柴人编码器的歧义性**：在自遮挡或极端视角下，火柴人编码器对左右肢体的混淆仍然存在。目前尚不清楚是否需要额外的数据增强或结构改进来提升鲁棒性。

### 5. 知识库定位

DrawMotion 处于 **可控动作生成** 与 **训练无关引导** 的交叉点。其方法贡献可归纳为三个层面：

1. **条件扩展**：将手绘轨迹与火柴人引入扩散动作生成，形成文本-空间-姿态的三元控制范式。
2. **融合架构**：MCM 中的模态特定解码器设计（eff/dot 注意力分工）和条件混合策略（设置 $p(\hat{w}=w)=50\%$ 并偏向手绘条件可获得最佳 FID 0.124，Table IX）为多模态条件融合提供了可复用的模板。
3. **引导机制**：IFG 证明了在连续中间特征空间中进行训练无关引导的可行性，这一思路可能推广到其他需要精确约束的生成任务中。

**需要手动验证的点**：ReMoDiffuse 的具体引用信息（作者/会议/年份）在当前分析中缺失，建议查阅原始论文补充完整引用。



## 原文 PDF

![[paperPDFs/TPAMI_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.pdf]]

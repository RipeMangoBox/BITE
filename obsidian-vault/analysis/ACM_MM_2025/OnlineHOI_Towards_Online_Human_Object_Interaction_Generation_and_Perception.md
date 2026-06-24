---
title: "OnlineHOI: Towards Online Human-Object Interaction Generation and Perception"
type: paper
paper_level: A
venue: ACM MM
year: 2025
pdf_ref: paperPDFs/ACM_MM_2025/OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Perception.pdf
aliases:
- OOGGOPP
- OnlineHOI
tags:
- ACM_MM_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 以Mamba的单向状态空间扫描替代Transformer的自注意力机制，并引入短时/长时记忆增强模块，使模型在在线设置下高效利用历史序列。
primary_logic: Mamba的连续扫描和增量状态更新天然适合在线数据流，而记忆模块通过滑动窗口和相似性合并保留关键历史上下文，弥补了Mamba在长期检索与索引上的不足，从而大幅提升在线HOI性能。
claims:
- Transformer在在线设置下性能大幅下降，而Mamba在此场景下优势显著。
- OnlineHOI-G在Core4D S1上相较MDM和OMOMO显著降低FID并提升RA与用户偏好。
- OnlineHOI-P在HOI4D动作分割上准确率超越PointNet++和P4Transformer。
- M_E记忆模块（融合短时和长时记忆）在所有记忆变体和融合策略中取得最佳FID。
---

# OnlineHOI: Towards Online Human-Object Interaction Generation and Perception

> [!tip] 核心洞察
> Mamba的连续扫描和增量状态更新天然适合在线数据流，而记忆模块通过滑动窗口和相似性合并保留关键历史上下文，弥补了Mamba在长期检索与索引上的不足，从而大幅提升在线HOI性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | OnlineHOI：面向在线人物体交互生成与感知 |
| 英文题名 | OnlineHOI: Towards Online Human-Object Interaction Generation and Perception |
| 会议/期刊 | ACM MM 2025 |
| Links |  [paper](https://doi.org/10.1145/3746027.3754848)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OnlineHOI (OnlineHOI-G for generation, OnlineHOI-P for perception) |
| Dataset | Core4D S1, Core4D S2, Core4D User Study |

> [!tip] 效果简介
> - Core4D S1 (seen objects) 上，FID↓ 2.61 (Ours / M_E) vs 3.08 (Add Fusion) (-0.47)。
> - Core4D S2 (unseen objects) 上，FID↓ 2.54 (Ours / M_E) vs 3.26 (Add Fusion) (-0.72)。
> - Core4D User Study 上，Preference % 63.54 vs MDM / OMOMO (lower, exact not extracted) (majority preference)。

## 概述

人物体交互（Human-Object Interaction, HOI）的感知与生成在具身智能、人机协作等场景中具有重要价值。现有方法大多基于离线范式，即假设模型可以访问完整的时间序列，这在真实流式应用中难以成立。当模型仅能依赖历史与当前帧信息进行在线预测时，基于Transformer自注意力的主流方案性能严重退化，构成了本工作的核心瓶颈。

针对上述问题，本文提出 **OnlineHOI**（OnlineHOI-G 用于生成，OnlineHOI-P 用于感知），将在线HOI任务显式建模为流式序列学习问题。方法的核心洞察在于：**Mamba** 状态空间模型的单向扫描与增量状态更新机制天然适配在线数据流，避免了Transformer在因果掩码下对历史信息的重复计算与注意力退化；同时，引入**短时/长时记忆增强模块**（M_S 与 M_L 融合为 M_E），通过滑动窗口缓存与相似性合并策略保留关键历史上下文，弥补了纯Mamba在长期检索与索引上的不足。

实验表明，OnlineHOI-G 在 Core4D 数据集上相较 **MDM**（Tevet et al., arXiv 2022）和 **OMOMO**（Li et al., TOG 2023）显著降低了 FID，并在用户偏好测试中获得多数优势；OnlineHOI-P 在 HOI4D 动作分割任务上准确率超越 **PointNet++**（Qi et al., NeurIPS 2017）和 **P4Transformer**（Fan et al., CVPR 2021）。消融研究确认了 Mamba 在在线设置下对 Transformer 的显著优势，以及 M_E 记忆模块在所有记忆变体和融合策略中的最优性能。

**方法定位**：OnlineHOI 属于在线序列建模方法，以 Mamba 为时序骨干，辅以记忆增强机制，面向点云与运动数据的流式HOI感知与生成。其技术路线与离线扩散模型（MDM、OMOMO）及离线点云Transformer（P4Transformer）形成对比，在在线约束下实现了性能突破。

## 背景与动机

人物体交互（Human-Object Interaction, HOI）的感知与生成是理解人类行为并构建交互式智能系统的核心任务。现有工作在该领域已取得显著进展，但无论是基于Transformer的扩散生成方法（如 **MDM**，Tevet et al., arXiv 2022；**OMOMO**，Li et al., TOG 2023），还是点云动作分割方法（如 **PointNet++**，Qi et al., NeurIPS 2017；**P4Transformer**，Fan et al., CVPR 2021），均建立在**离线范式**之上——即模型在推理时可以访问完整的时间序列，利用全局上下文进行预测。

然而，在诸多实际应用场景（如实时人机协作、流式视频理解、在线动作预测）中，系统只能依据**当前帧及历史信息**进行即时决策，无法窥见未来数据。这一“在线”设定与离线范式之间存在根本性差异（见Figure 2），直接将离线模型迁移至在线场景往往导致性能严重退化。分析表明，Transformer的自注意力机制在因果掩码约束下，其长程依赖建模能力显著削弱，成为制约在线HOI性能的关键瓶颈。

针对上述缺口，本文提出 **OnlineHOI** 框架，旨在系统性地解决在线人物体交互的感知与生成问题。核心动机在于：需要一种天然适配流式数据处理的架构，能够在仅依赖历史信息的条件下高效提取时序特征，并有效保留关键历史上下文以弥补单向建模的信息损失。

## 核心创新

OnlineHOI 的核心创新在于将人物体交互（HOI）的生成与感知任务从离线范式迁移至在线流式场景，并通过**Mamba 单向状态空间模型**与**多尺度记忆增强模块**的协同设计，解决了现有 Transformer 方法在仅依赖历史与当前信息时性能严重退化的问题。

### 创新点一：以 Mamba 替代 Transformer 作为在线时序骨干

现有 HOI 方法（如 **MDM**（Tevet et al., arXiv 2022）和 **P4Transformer**（Fan et al., CVPR 2021））普遍采用 Transformer 的自注意力机制进行时序建模。在离线设置下，自注意力可并行处理完整序列；但在在线设置中，模型只能访问过去帧，需引入因果掩码，导致感受野受限且计算效率下降。OnlineHOI 的关键洞察在于：Mamba 的选择性状态空间模型天然适配在线数据流——其隐藏状态沿时间步增量更新，无需重新计算历史步骤，且单向扫描机制与在线推理的信息流向完全一致。

具体而言，Mamba 的状态更新公式为：

$$h_{t+1} = \overline{\mathbf{A}} h_t + \overline{\mathbf{B}} \mathbf{x}_t, \quad y_t = \mathbf{C} h_t$$

该递推结构使模型在每一时刻仅需当前输入 $\mathbf{x}_t$ 和上一时刻隐藏状态 $h_t$ 即可计算输出，避免了 Transformer 对完整历史序列的重复编码。消融实验（Table 4）直接验证了这一优势：Transformer 从离线切换到在线设置时性能大幅下降，而 Mamba 在在线场景下显著优于 Transformer，证明了状态空间模型对在线 HOI 建模的架构优越性。

### 创新点二：短时/长时记忆增强模块弥补 Mamba 的长期检索缺陷

尽管 Mamba 擅长增量状态更新，其固定维度的隐藏状态在压缩长序列信息时存在瓶颈，尤其难以精确检索距离较远的关键交互帧。为此，OnlineHOI 在 Mamba 编码器与解码器之间引入了记忆增强模块，由两部分构成：

- **短时记忆（M_S）**：采用 FIFO 滑动窗口机制，直接保留最近 $S$ 帧的编码特征，确保模型对近期交互细节的精确访问。
- **长时记忆（M_L）**：基于帧间相似性进行合并存储（Algorithm 1），将历史序列中语义相近的帧聚合为代表性特征，以有限容量保留长程关键上下文。

最终通过所设计的融合策略将 M_S 与 M_L 结合为 **M_E 记忆**，传递给解码器。Table 7 的消融表明：M_E 在 Core4D S1 和 S2 上的 FID 分别降至 2.61 和 2.54，优于单独使用 M_S 或 M_L，也优于简单的 Add 和 Max 融合方式。这证实了短时精确记忆与长时压缩记忆的互补性——前者保证局部时序精度，后者提供全局语义锚点，共同弥补了纯 Mamba 模型在长期索引与检索上的不足。

### 创新点三：面向在线 HOI 的双任务统一架构

OnlineHOI 并非单一任务模型，而是统一覆盖生成（OnlineHOI-G）与感知（OnlineHOI-P）的在线 HOI 框架。两者共享 Mamba + 记忆增强的核心设计，但在输入端和条件机制上各有适配：

- **OnlineHOI-G** 在 Mamba 编码器后引入自注意力条件化模块，将 actor 运动与物体几何信息融入隐藏状态，再通过扩散解码器生成反应者运动序列。
- **OnlineHOI-P** 采用 4D 卷积骨干（UNet 结构，四层 4D 卷积与反卷积）提取点云时空特征，随后由 Mamba 沿时间步进行前向扫描增强逐点特征，最终输出动作分割 logits。

这一双任务统一设计使得 Mamba 的在线序列建模能力与记忆增强策略在生成质量和感知精度两个维度上均得到验证：OnlineHOI-G 在 Core4D 上相较 MDM 和 OMOMO 显著降低 FID 并获得 63.54% 的用户偏好投票（Table 1）；OnlineHOI-P 在 HOI4D 动作分割上准确率超越 PointNet++ 和 P4Transformer（Table 2）。

### 与 baseline 的 changed slots 总结

| 变更维度 | Baseline 方案 | OnlineHOI 方案 | 证据锚点 |
|---------|-------------|---------------|---------|
| 时序骨干 | Transformer（自注意力 + 因果掩码） | Mamba（选择性 SSM + 单向扫描） | Section 3.3, Table 4 |
| 记忆机制 | 无显式记忆 | M_S（短时 FIFO）+ M_L（长时相似性合并）= M_E | Section 3.4, Table 7 |
| 扩散条件化 | Transformer-only 条件化 | Mamba 编码后接自注意力条件化模块 | Section 3.3.1 |
| 感知时序层 | P4Transformer（点云 Transformer） | 4D 卷积骨干 + Mamba 前向扫描 | Section 3.3.2, Table 2 |

> **需注意**：记忆模块的容量参数（$S$ 和 $L$ 帧数）及合并策略依赖手动设定，论文未探索自适应调整机制，这是当前方法的一个显式局限。

## 整体框架

OnlineHOI 的整体架构围绕 **在线流式数据流** 设计，核心由两个关键模块构成：**Mamba 块** 与 **记忆增强块**（Memory Augment Block），如图 Figure 3 所示。其设计目标是在仅能访问历史与当前帧信息的在线约束下，高效提取时序特征并完成生成或感知任务。

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/003_Figure_3.jpg]]
*Figure 3: Method overview. The figure illustrates the architecture of the proposed OnlineHOI. OnlineHOI consists of the Mamba block and the Memory Augment block. The Mamba Encoder and Decoder both have an unidirectional spatial Mamba block which possesses forward scans within SSM layers respectively. The Memory Augment Model is placed between the Encoder and Decoder to enhance the key knowledge from the Encoding state and then pass it forward to the Decoder*

### 数据流与模块关系

在线设置下，模型在每个时间步接收当前帧输入，并结合历史信息进行预测。数据流经以下核心模块：

1.  **Mamba 编码器（Mamba Encoder）**：接收输入序列，利用单向空间扫描的 Mamba 块提取时序特征，生成编码隐藏状态。其结构化状态空间演化（Equation 1）支持隐藏状态的增量更新，无需重新计算历史步骤，天然适配在线场景。
2.  **记忆增强模型（Memory Augment Model）**：位于编码器与解码器之间，负责存储和检索关键历史特征，以增强当前预测。该模块由短时记忆 **M_S**（滑动窗口 FIFO）和长时记忆 **M_L**（基于相似性合并的帧缓存，见 Algorithm 1）组成，最终融合为组合记忆 **M_E**，传递给解码器。
3.  **Mamba 解码器（Mamba Decoder）**：从增强后的隐藏状态解码输出，在生成任务中输出反应者运动序列，在感知任务中输出动作 logits。
4.  **条件融合模块（仅生成任务）**：在 Mamba 编码器之后，通过自注意力块将条件信息（主动者运动、物体几何）与编码隐藏状态融合，再送入记忆增强模块。

### 生成与感知分支

OnlineHOI 包含两个具体实例：

-   **OnlineHOI-G（生成）**：基于扩散模型框架，以 Mamba 编码器-解码器替代 Transformer U-Net 的骨干网络，在去噪过程中逐步生成反应者运动。条件信号通过自注意力块注入。
-   **OnlineHOI-P（感知）**：针对点云序列的动作分割任务，首先使用四层 4D 卷积与反卷积的类 UNet 骨干提取时空点云特征，随后由 Mamba 块沿时间步进行前向扫描，增强逐点特征表示，最后输出逐帧动作预测。

### 关键设计逻辑

-   **Mamba 替代 Transformer**：Transformer 的自注意力机制在在线设置下需使用因果掩码，性能大幅下降（见 Table 4）。Mamba 的单向扫描与增量状态更新机制在在线场景下具有天然优势。
-   **记忆增强的必要性**：纯 Mamba 在长期检索与索引方面存在不足。记忆模块通过滑动窗口保留近期细节（M_S）和相似性合并保留关键历史帧（M_L），弥补了这一缺陷，显著提升在线性能（见 Table 5、Table 6）。融合短时与长时记忆的 M_E 策略在所有记忆变体中取得最佳效果（见 Table 7）。

### 补充图表

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of the Offline and Online settings. (a) The whole timeline is known. (b) The network can only make predictions based on the current frame and previous information*

## 核心模块与公式推导

OnlineHOI 的核心架构由两个关键模块构成：**Mamba 主干网络** 与**记忆增强模块**（Memory Augment Model），二者协同实现在线流式场景下的高效时序建模。

### Mamba 主干网络

Mamba 作为一种选择性状态空间模型，其核心优势在于单向扫描机制与增量式状态更新。给定输入序列 $\mathbf{x}_t$，Mamba 的隐藏状态演化与输出计算遵循：

$$h_{t+1} = \overline{\mathbf{A}} h_t + \overline{\mathbf{B}} \mathbf{x}_t, \quad y_t = \mathbf{C} h_t$$

其中 $h_t$ 为时刻 $t$ 的隐藏状态，$\overline{\mathbf{A}}$、$\overline{\mathbf{B}}$、$\mathbf{C}$ 为离散化后的状态空间参数。这一递推结构使得 Mamba 在在线推理时无需重新计算所有历史步骤，仅需维护并更新当前隐藏状态即可，天然适配仅依赖历史与当前信息的在线约束。

为提升训练效率，Mamba 将上述递推过程等价转化为全局卷积形式：

$$\overline{\mathbf{K}} = (\mathbf{C} \overline{\mathbf{B}}, \mathbf{C} \overline{\mathbf{A} \mathbf{B}}, \ldots, \mathbf{C} \overline{\mathbf{A}}^{\mathbf{M}-1} \overline{\mathbf{B}}), \quad y = x * \overline{\mathbf{K}}$$

其中 $\overline{\mathbf{K}}$ 为长度为 $\mathbf{M}$ 的全局卷积核，$*$ 表示卷积操作。该等价变换使得训练阶段可利用并行卷积加速，而推理阶段仍可回归增量式状态更新。

在 OnlineHOI 框架中，Mamba Encoder 与 Mamba Decoder 均采用单向空间 Mamba 块，沿时间维度执行前向扫描（见 Figure 3）。对于生成任务（OnlineHOI-G），在 Mamba Encoder 之后引入一个自注意力条件化模块，将条件信息（actor 运动、物体几何）与编码后的隐藏状态进行融合，再送入扩散模型的去噪过程。扩散前向加噪过程定义为：

$$q(x_t | x_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}, (1 - \alpha_t) I)$$

其中 $\alpha_t$ 为噪声调度参数，控制逐步向数据注入高斯噪声的过程。

对于感知任务（OnlineHOI-P），首先通过 4D 卷积骨架提取点云序列的时空特征。该骨架采用类 UNet 结构，编码器与解码器各包含四层 4D 卷积与反卷积操作。4D 卷积在点云序列上的时空聚合操作定义为：

$$\mathbf{f}_t^{\prime (x,y,z)} = \sum_{\delta_t = -r_t}^{r_t} \sum_{\|(\delta_x, \delta_y, \delta_z)\| \leq r_s} \cdots$$

其中 $r_t$ 和 $r_s$ 分别为时间维度和空间维度的卷积半径，通过在时空邻域内进行求和与最大池化来聚合局部时空信息。随后，Mamba 块沿时间步对 4D 骨架提取的逐点特征进行前向扫描增强，最终输出动作分割的类别 logits。

### 记忆增强模块

记忆增强模块位于 Mamba Encoder 与 Decoder 之间，旨在弥补 Mamba 在长期检索与索引方面的不足。该模块由两部分组成：

- **短时记忆 $\mathbf{M}_S$**：采用 FIFO 滑动窗口机制，保留最近 $S$ 帧的编码特征，为当前帧提供紧邻时序上下文。
- **长时记忆 $\mathbf{M}_L$**：通过相似性合并策略存储关键历史帧特征。具体而言，当新帧到来时，计算其与已存储帧的特征相似度；若与某已存帧高度相似则合并更新，否则作为新关键帧加入记忆库（见 Algorithm 1）。该机制以有限的存储容量保留长程交互中的关键状态。

最终的增强记忆 $\mathbf{M}_E$ 将短时与长时记忆进行融合，传递给 Decoder 以增强当前预测。消融实验表明，$\mathbf{M}_E$ 融合策略在所有记忆变体中取得最佳 FID（Table 7），验证了多尺度历史信息对在线 HOI 性能的关键作用。

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/012_Table_7.jpg]]
*Table 7: Results on*

### 补充图表

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/009_Table_4.jpg]]
*Table 4: Online and offline results on Transformer and Mamba based Model*

## 实验与分析

### 在线生成主结果

OnlineHOI-G 在 Core4D 与 OAKINK2 两个基准上均取得最优生成质量，验证了 Mamba 架构与记忆增强模块在在线流式条件下的有效性。

在 Core4D S1（见过物体）上，OnlineHOI-G 的 FID 降至 **2.61**，显著优于基于 Transformer 的扩散基线 MDM（Tevet et al., arXiv 2022）与两阶段条件扩散方法 OMOMO（Li et al., TOG 2023）；在 S2（未见物体）上 FID 进一步降至 **2.54**，表明模型对物体几何变化的泛化能力较强（Table 1）。用户偏好研究显示，OnlineHOI-G 生成的反应者运动在 **63.54%** 的对比中获得偏好投票，超过 MDM 与 OMOMO 之和，说明在线范式下生成质量的主观可接受性明显更高。

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/004_Table_1.jpg]]
*Table 1: Results on Generation evaluated on CORE4D dataset. S1 and S2 denote seen and unseen objects, respectively. All models are trained and evaluated on the CORE4D dataset under identical settings, conditioned on both actor motion and object geometry. The reported metric evaluates the quality of generated reactor motion, which is the primary objective of these models*

在 OAKINK2 数据集上，OnlineHOI-G 的 FID 达到 **0.35**，同样优于 MDM 与 OMOMO（Table 3）。定性对比（Figure 4 与 Figure 5）揭示了 Transformer 基线在在线设置下的典型失败模式：MDM 与 OMOMO 生成的反应者运动常出现与物体接触失败、手部穿透或运动不自然等问题，而 OnlineHOI-G 能生成更合理的接触姿态与连贯轨迹。这一差异可归因于 Mamba 的单向状态扫描天然适配在线数据流，而记忆模块保留的历史关键帧弥补了长程依赖的退化。

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/007_Table_3.jpg]]
*Table 3: Results on Generation evaluated on OAKINK2 dataset. We do the official train, validation and test split for these three models. The condition is uniformly consists of the actor’s motion and two objects geometry. We evaluate the reactor’s generation errors*

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparisons on OAKINK2 dataset. The yellow hand represents the reactor, which is generated by MDM, OMOMO, and OnlineHOI-G. In Case 1, the reactor generated by MDM and OMOMO can not make contact with the object, while the reactor generated by OnlineHOI-G maintains a relatively tight grip. In Case 2, MDM and OMOMO cause some object penetration, with OMOMO being more pronounced in this regard, whereas OnlineHOI-G does not exhibit this issue. In Case 3, both MDM and OMOMO fail to hold the pen properly, while OnlineHOI-G successfully handles this task*

### 在线感知主结果

OnlineHOI-P 在 HOI4D 动作分割任务上以 **71.2%** 的准确率超越单帧基线 PointNet++（Qi et al., NeurIPS 2017）与时序 Transformer 方法 P4Transformer（Fan et al., CVPR 2021）（Table 2）。值得注意的是，P4Transformer 虽然引入了 4D 卷积与 Transformer 时序建模，但在在线因果掩码约束下性能退化明显；OnlineHOI-P 以相同的 4D 卷积骨干结合 Mamba 解码器，在仅依赖历史信息的条件下实现了更优的时序特征提取，证明 Mamba 的增量状态更新比自注意力机制更适合在线感知。

### 架构消融：Transformer vs. Mamba

Table 4 的在线/离线对比实验是本文最具因果诊断性的消融之一。基于 Transformer 的 U-Net 在从离线切换到在线设置时性能大幅下降，而基于 Mamba 的模型在同一转换下性能损失显著更小，且在在线设置下的绝对性能远超 Transformer。这一结果直接支持了核心因果主张：**Transformer 的自注意力机制在仅允许历史信息的在线因果掩码下严重受限，而 Mamba 的单向扫描与增量状态更新天然适配在线数据流**。该消融在相同数据集、相同条件输入与相同超参数下完成，结论可信度较高。

### 记忆模块消融

记忆模块的消融实验从三个维度验证了其有效性：

1. **有无记忆对比**（Table 5 & Table 6）：在生成与感知任务上，引入记忆模块均带来一致的性能提升，表明 Mamba 的隐状态虽能携带历史信息，但显式的多尺度记忆对关键帧的检索与重放仍有不可替代的作用。

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/010_Table_5.jpg]]
*Table 5: Results on w/ and w/o Memory on generation*

![[assets/figures/papers/paper_list_l1665_OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Percept/figures/011_Table_6.jpg]]
*Table 6: Results on w/ and w/o Memory on perception*

2. **记忆类型消融**（Table 7）：短时记忆 M_S（FIFO 滑动窗口）与长时记忆 M_L（基于相似性合并的历史帧）各自独立使用时均能改善 FID，但融合两者的 M_E 记忆在 Core4D S1 与 S2 上分别取得 **2.61** 与 **2.54** 的最优 FID，优于单独使用任一种记忆。这验证了短时细节保留与长时语义压缩的互补性。

3. **融合策略消融**（Table 7）：M_E 所采用的融合策略优于简单的 Add Fusion 与 Max Fusion。Add Fusion 在 S1 上的 FID 为 3.08，Max Fusion 表现更差，表明简单聚合无法有效整合两种记忆源的信息；M_E 通过门控或注意力机制（具体实现需参考原文 Algorithm 1 与 Section 3.4）实现了更优的信息筛选与组合。

### 失败模式与局限性

尽管 OnlineHOI 在三个基准上表现优异，仍存在以下已知局限：

- **记忆容量依赖手工设定**：短时记忆的窗口长度 S 与长时记忆的合并帧数 L 均为固定超参，对不同交互节奏（如快速抓取 vs. 缓慢操作）的适应性可能不足。自适应调整记忆容量的机制是值得探索的方向。
- **数据集覆盖有限**：验证仅在 Core4D、OAKINK2 与 HOI4D 上进行，这些数据集均为受控实验室采集的点云与运动捕捉数据，在真实场景的噪声、遮挡与多模态输入（如 RGB 视频）下的表现尚待验证。
- **多人多物扩展性未验证**：当前实验场景以单人或双人交互为主，Mamba 的单向扫描在更复杂的多人协作场景中是否仍能保持优势，以及记忆模块的容量需求如何随交互复杂度增长，均为开放问题。

### 关键图表结论汇总

- **Table 1**：OnlineHOI-G 在 Core4D 生成任务上全面超越 MDM 与 OMOMO，用户偏好超过半数。
- **Table 2**：OnlineHOI-P 在 HOI4D 动作分割上准确率超越 PointNet++ 与 P4Transformer。
- **Table 4**：Transformer 在线性能崩溃，Mamba 在线优势显著——这是方法有效性的核心证据。
- **Table 7**：M_E 记忆融合在所有记忆变体与融合策略中取得最优 FID，验证了短时/长时记忆互补设计的必要性。

## 方法谱系与知识库定位

### 离线范式向在线流式的迁移瓶颈

现有HOI生成与感知方法几乎全部构建于离线范式之上：模型可访问完整时间轴，依赖双向自注意力机制捕获全局时序依赖。**MDM**（Tevet et al., arXiv 2022）和**OMOMO**（Li et al., TOG 2023）在生成任务中采用基于Transformer的扩散架构，在离线设定下表现优异；**P4Transformer**（Fan et al., CVPR 2021）则通过4D卷积与Transformer的结合实现点云序列的动作分割。然而，一旦将这些模型迁移至仅允许历史与当前信息输入的在线流式场景，其性能便出现严重退化——Table 4的消融实验清晰揭示了这一断层：Transformer backbone从离线切换到在线时，各项指标下降幅度远大于Mamba backbone。

OnlineHOI的出发点正是这一未被充分正视的范式差距。论文将问题锚定在“在线HOI”这一具体设定下，而非简单追求离线指标的边际提升，这构成了其与前述baseline工作的根本分野。

### Mamba作为在线骨干的因果机制

方法的核心替换发生在时序建模骨干：以**Mamba**的选择性状态空间模型（selective state-space model）取代Transformer的自注意力机制。Mamba的单向扫描特性天然匹配在线数据流的因果约束——其隐藏状态沿时间步增量更新，无需为每个新帧重新计算整个历史序列：

$$h_{t+1} = \overline{\mathbf{A}} h_t + \overline{\mathbf{B}} \mathbf{x}_t, \quad y_t = \mathbf{C} h_t$$

这一递推结构使得Mamba在在线设定下的计算效率与建模能力均优于需要因果掩码的Transformer。Table 4的对比为这一论断提供了决定性证据：Mamba-based模型在在线场景下的FID显著低于Transformer-based模型，且离线到在线的性能降幅更小。

但Mamba并非无代价的替代方案。状态空间模型的连续扫描特性虽利于增量更新，却缺乏Transformer自注意力机制那种对远距离帧的直接索引能力——当历史序列中存在关键交互事件需要被精确检索时，Mamba的隐状态可能已将其“遗忘”或稀释。这正是记忆增强模块介入的因果节点。

### 记忆增强模块的补偿机制

记忆增强模型位于Mamba Encoder与Decoder之间，由短时记忆（$\mathbf{M}_S$）和长时记忆（$\mathbf{M}_L$）两部分融合为$\mathbf{M}_E$。$\mathbf{M}_S$采用FIFO滑动窗口机制，保留最近若干帧的编码特征，提供对近期上下文的精确访问；$\mathbf{M}_L$则通过相似性合并策略（Algorithm 1）将相邻的相似帧聚合存储，在有限容量内保留更长时间跨度的关键历史信息。

Table 7的消融实验系统验证了这一设计的有效性：$\mathbf{M}_E$（融合短时与长时记忆）在Core4D S1和S2上均取得最佳FID（分别为2.61和2.54），优于单独使用$\mathbf{M}_S$或$\mathbf{M}_L$，也优于简单的Add或Max融合策略。这一结果揭示了在线HOI中历史信息管理的双重需求——既需要精确的近期帧检索，也需要对长程关键事件的粗粒度保留。

### 适用边界与局限

OnlineHOI的验证集中在三个数据集：Core4D（生成）、OAKINK2（生成）和HOI4D（感知），覆盖了多人-物交互生成、手-物交互生成和动作分割三类任务。然而，论文明确指出的局限值得重视：

1. **记忆容量的手工设定**：短时记忆的窗口长度和长时记忆的合并阈值依赖经验选择，缺乏对交互节奏的自适应调整机制。在交互速度剧烈变化的场景中，固定参数可能导致关键帧的丢失或冗余信息的堆积。

2. **模态覆盖范围**：当前方法主要处理点云和运动数据，未涉及RGB视频等多模态输入。在实际在线交互系统中，视觉外观信息往往承载着关键的语义线索，这一缺失限制了方法的直接部署能力。

3. **场景复杂度**：验证场景以双人或手-物交互为主，向更复杂的多人多物协作场景推广时，记忆模块的容量管理和Mamba的隐状态容量可能成为新的瓶颈。

### 开放问题

基于上述局限，以下问题值得后续工作关注：

- **自适应记忆管理**：能否根据交互的瞬时变化速率动态调整$\mathbf{M}_S$的窗口长度和$\mathbf{M}_L$的合并阈值？这可能需要引入额外的元学习或门控机制。

- **长序列扩展性**：当序列长度远超当前验证范围时，Mamba的隐状态是否会出现信息饱和？记忆增强策略能否与更强大的状态空间模型（如Mamba-2）结合以提升长程建模能力？

- **跨任务泛化**：记忆增强的Mamba架构是否适用于其他在线序列建模任务（如自动驾驶中的轨迹预测、机器人实时操作规划）？其相对于在线Transformer的优势是否具有任务无关的普适性？

- **多模态融合**：将RGB视觉特征纳入现有框架时，记忆模块的存储与检索策略需要如何调整？视觉特征的冗余度与运动特征不同，可能需要差异化的合并策略。

## 原文 PDF

![[paperPDFs/ACM_MM_2025/OnlineHOI_Towards_Online_Human_Object_Interaction_Generation_and_Perception.pdf]]

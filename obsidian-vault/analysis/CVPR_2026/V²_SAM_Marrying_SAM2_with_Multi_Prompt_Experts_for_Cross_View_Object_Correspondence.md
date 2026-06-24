---
title: "V²-SAM: Marrying SAM2 with Multi-Prompt Experts for Cross-View Object Correspondence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/V_SAM_Marrying_SAM2_with_Multi_Prompt_Experts_for_Cross_View_Object_Correspondence.pdf
aliases:
- VS
- VSMSMPECVOC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入跨视角几何对应(V²-Anchor)和外观对齐(V²-Visual)的双分支提示，以及多专家训练和自适应循环一致性选择(PCCS)，有效融合互补信息。
primary_logic: 空间提示回答“在哪里”，视觉提示回答“长什么样”，两者互补；多专家集成与循环一致性选择可以自适应地利用两者优势，大幅提升复杂跨视角场景中的分割鲁棒性。
claims:
- V²-Anchor是跨视角定位的关键，移除后导致总IoU从40.1骤降至1.5。
- V²-Visual提供关键外观信息，移除后总IoU从41.4降至3.0。
- 多专家结合PCCS在Ego-Exo4D上显著超越所有基线，总IoU达48.0，较最佳基线O-MaMa(43.4)提升4.6点。
- 稀疏锚点数量对性能影响大，单点最佳（38.7 IoU），点越多性能越差。
---

# V²-SAM: Marrying SAM2 with Multi-Prompt Experts for Cross-View Object Correspondence

> [!tip] 核心洞察
> 空间提示回答“在哪里”，视觉提示回答“长什么样”，两者互补；多专家集成与循环一致性选择可以自适应地利用两者优势，大幅提升复杂跨视角场景中的分割鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | V²-SAM：将SAM2与多提示专家结合用于跨视角物体对应 |
| 英文题名 | V²-SAM: Marrying SAM2 with Multi-Prompt Experts for Cross-View Object Correspondence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20886) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | V²-SAM |
| Dataset | Ego-Exo4D, Ego-Exo4D (v2 test) - Ego2Exo方向, DAVIS-2017 Val, HANDAL-X |

> [!tip] 效果简介
> - Ego-Exo4D (v2 test) 上，Total-IoU 48.0 vs 43.4 (O-MaMa) (+4.6)。
> - Ego-Exo4D (v2 test) - Ego2Exo方向 上，IoU 46.3 vs 42.6 (O-MaMa) (+3.7)。
> - DAVIS-2017 Val (20帧间隔) 上，J&F_m 78.8 vs 70.2 (PCC) (+8.6)。

## 概述

跨视角物体对应（cross-view object correspondence）要求在视角、光照、遮挡和物体姿态剧烈变化的两幅图像之间，对同一物体实例进行精确分割。现有的基础分割模型（如 SAM、SAM2）虽然具备强大的单帧提示式分割能力，但它们的提示机制高度依赖单视角空间坐标或视觉参考，无法直接应对跨视角场景下目标位置和外观的双重漂移。这一瓶颈使得基于单视角空间提示的分割模型在跨视角条件下几乎完全失效。

V²-SAM 的核心洞察在于：**空间提示回答“在哪里”，视觉提示回答“长什么样”，两者在跨视角条件下天然互补**。基于这一认知，V²-SAM 在 SAM2 的框架之上引入了双分支跨视角提示生成机制——**V²-Anchor** 利用 DINOv3 的几何感知特征建立跨视角密集对应，生成坐标提示；**V²-Visual** 通过视觉提示匹配器（VPMatcher）从特征和结构两个层面进行跨视角外观对齐，生成视觉提示。两个提示分别送入独立的分割专家解码器（Anchor Expert、Visual Expert），并由第三个融合专家（Fusion Expert）联合处理，最终通过**事后循环一致性选择器（PCCS）**自适应地选择最可靠的预测结果。

这一设计在多个基准上取得了显著效果。在 Ego-Exo4D 对应 v2 测试集上，V²-SAM 以 **48.0 Total-IoU** 达到新 SOTA，较此前最佳方法 O-MaMa（43.4）提升 **+4.6 点**；在 DAVIS-2017 视频对象对应任务上，以 **78.8 J&F_m** 超越 PCC（70.2）达 **+8.6 点**；在零样本跨视角分割场景 HANDAL-X 上，IoU 达到 **77.2**，较 ObjectRelator（42.8）提升 **+34.4 点**。消融实验进一步证实了双提示的因果作用：移除 V²-Anchor 后 Anchor Expert 的 Total-IoU 从 40.1 骤降至 1.5，移除 V²-Visual 后 Visual Expert 的 Total-IoU 从 41.4 降至 3.0，表明两类提示各自承担着不可替代的定位和外观匹配功能。

在方法谱系上，V²-SAM 位于**基于提示的跨视角分割**与**多专家集成**的交汇点。它继承了 SAM2 的编码器-解码器架构，但通过几何对应和外观对齐两条互补路径重构了提示生成方式，区别于仅使用视觉参考提示的 Ref-SAM* 等扩展方法。与依赖候选匹配的 O-MaMa 和端到端方法 ObjectRelator 相比，V²-SAM 的多专家框架与 PCCS 选择器提供了更强的场景自适应能力，尤其在几何线索丰富或外观匹配困难的场景中展现出互补优势。

## 背景与动机

### 跨视角物体对应的核心挑战

跨视角物体对应（Cross-View Object Correspondence）要求在不同视角拍摄的图像之间建立同一物体的像素级对应关系。这一任务在增强现实、机器人操作和视频理解等应用中至关重要，但面临根本性困难：**同一物体在不同视角下的空间位置和外观表现会发生剧烈变化**，导致基于单视角空间提示的分割模型无法直接迁移。例如，在Ego-Exo4D数据集中，第一人称视角与第三人称视角之间的物体对应需要处理显著的视角变换、遮挡和尺度差异。

### SAM系列模型的局限

Segment Anything Model（SAM）及其视频扩展SAM2在图像和视频分割领域展现出强大的提示驱动分割能力。然而，现有SAM变体在跨视角场景中存在明显不足：

- **SAM**仅支持单一视图内的坐标点、框或掩码提示，缺乏跨视图的对应推理机制。
- **SAM2**引入了记忆机制用于视频时序传播，但其提示方式仍局限于单帧空间坐标，无法直接建立跨视角的语义对应。
- **Ref-SAM**等基于视觉参考提示的扩展尝试通过外观特征匹配进行跨帧分割，但仅依赖外观信息，在视角变化剧烈时容易失效。

如Figure 1所示，V²-SAM的提出正是为了弥补这一能力缺口——同时支持**坐标点提示**和**视觉参考提示**，以适应跨视角分割场景的多样化需求。

### 现有方法的瓶颈

当前跨视角物体对应方法可大致分为两类，各自存在关键瓶颈：

1. **基于候选匹配的方法**（如**O-MaMa**）：先在目标图像中生成大量候选区域，再通过匹配筛选。这类方法依赖预定义的候选生成策略，在复杂场景中召回率受限，且计算开销大。

2. **端到端分割方法**（如**ObjectRelator**、**XSegTx**）：直接学习跨视角映射，但在大规模视角变化下泛化能力不足，尤其在零样本场景中性能急剧下降。

**根本瓶颈**在于：现有方法未能有效融合“物体在哪里”的空间定位信息和“物体长什么样”的外观语义信息。单一信息源在跨视角条件下都容易失效——空间对应在无纹理区域或重复结构中不可靠，外观对应在光照变化或视角旋转时退化。

### 本文动机与核心思路

本文的核心洞察是：**空间提示回答“在哪里”，视觉提示回答“长什么样”，两者天然互补**。基于这一洞察，V²-SAM提出了双分支提示生成机制：

- **V²-Anchor**：通过DINOv3特征的几何对应恢复SAM2的空间定位能力，生成坐标提示。
- **V²-Visual**：通过视觉提示匹配器（VPMatcher）实现跨视角外观对齐，生成视觉提示。

进一步的，通过**多专家训练框架**和**自适应循环一致性选择器（PCCS）**，V²-SAM能够根据不同场景特性自适应地选择或融合两种提示的优势，从而在复杂跨视角场景中大幅提升分割鲁棒性。实验表明，这一设计在Ego-Exo4D上总IoU达48.0，较最佳基线O-MaMa（43.4）提升4.6个点，验证了双提示互补策略的有效性。

## 核心创新

V²-SAM 的核心创新在于**显式解耦并融合跨视角空间提示与外观提示**，通过多专家框架与自适应选择器，解决了 SAM2 在跨视角场景中因目标位置和外观剧烈变化而无法直接迁移的根本瓶颈。

### 1. 双分支互补提示生成

传统方法（如 Ref-SAM*）仅依赖视觉参考提示进行分割，在跨视角几何偏移较大时极易失效。V²-SAM 引入了两条互补的提示生成路径：

- **V²-Anchor（几何锚点提示）**：回答“目标在哪里”。利用 DINOv3 的几何感知特征空间建立跨视角密集对应，通过分层采样筛选可靠匹配点，将其转换为坐标提示。该分支无需训练，直接为 SAM2 解码器提供空间定位信号。
- **V²-Visual（视觉提示）**：回答“目标长什么样”。通过可训练的 Visual Prompt Matcher（VPMatcher）从特征映射和结构映射两个维度对齐跨视角目标表征，生成外观引导的提示嵌入。

这一设计的关键洞察在于：**空间提示与外观提示互补**——当几何对应可靠时，锚点提示提供精确定位；当外观特征显著时，视觉提示弥补几何失效。消融实验提供了强证据支持：移除 V²-Anchor 后，Anchor Expert 的 Total-IoU 从 40.1 骤降至 1.5；移除 V²-Visual 后，Visual Expert 的 Total-IoU 从 41.4 降至 3.0（Table 4）。这表明两种提示各自承载了不可替代的互补信息。

### 2. 多专家解码器架构

与单解码器接收单一种类提示的基线方案不同，V²-SAM 并行部署三个专家解码器：

- **Anchor Expert**：仅接收坐标提示，训练无关，依赖 V²-Anchor 的几何对应质量。
- **Visual Expert**：仅接收视觉提示，由 VPMatcher 生成。
- **Fusion Expert**：同时接收两种提示，显式融合空间与外观信号。

这种多专家设计使得系统能够**在不同场景下自适应地利用最合适的提示源**，而非强制单一策略。Figure 4 的场景级分析显示，不同专家在不同场景下的 IoU 分布差异显著，证明了多专家架构的必要性。

### 3. 后验循环一致性选择器（PCCS）

多专家输出需要有效的选择机制。PCCS 的核心思想是**点级循环一致性检验**：将每个专家预测的目标掩码通过 V²-Anchor 反向投影回查询视图，计算投影点与原始查询掩码的重合度，选择一致性最高的专家输出作为最终结果。公式为：

$$P_k^{t2q} = \mathrm{V}^2\mathrm{Anchor}(I_t, I_q; \hat{M}_{t_k})$$

相较于基于掩码的 Cycle-Mask 方案，Cycle-Points 选择器更轻量且精度相近或更优——在两专家（Anchor+Visual）设置下，Exo→Ego 方向的 IoU 提升 1.4 点，同时延迟降低 110 ms（Table 10）。PCCS 的关键价值在于**无需额外训练即可自适应地利用多专家互补性**，将 Anchor Expert 的几何鲁棒性与 Visual Expert 的外观敏感性动态结合。

### 4. 与基线的关键差异总结

| 设计维度 | 基线方案 | V²-SAM 创新 |
|---------|---------|------------|
| 提示生成 | 仅视觉参考提示（如 Ref-SAM*） | 几何锚点 + 视觉提示双分支 |
| 解码器配置 | 单解码器单提示 | 三专家并行（Anchor/Visual/Fusion） |
| 后处理选择 | 无或简单规则 | PCCS 基于循环一致性自适应选择 |

这些创新在 Ego-Exo4D 上带来了显著增益：V²-SAM Multi-Experts 的 Total-IoU 达 48.0，较最佳基线 O-MaMa（43.4）提升 4.6 点（Table 1）；在零样本跨数据集迁移 HANDAL-X 上，IoU 较 ObjectRelator 提升 34.4 点（77.2 vs 42.8，Table 3），验证了设计的泛化能力。

## 整体框架

V²-SAM 以 SAM2 为基础骨架，保留其 Encoder φ(·)、Prompt Encoder 和 Mask Decoder，但丢弃了与帧间记忆相关的模块，使框架聚焦于帧级跨视角对应（Section 3.1）。给定一对查询-目标图像 $(I_q, I_t)$ 以及查询视图中的物体掩码 $M_q$，系统并行生成两类跨视角提示，分别送入对应的掩码解码器，最终由一个后处理选择器输出最优预测掩码。

**输入与输出流** 如图 2 所示，整个 pipeline 包含两条互补的提示生成路径：

1. **几何锚点分支（V²-Anchor）**：利用 DINOv3 的几何感知特征空间，在查询图像与目标图像之间建立密集对应关系，经分层采样过滤后生成稀疏坐标提示 $P_{\text{anchor}}^{q2t}$。该分支回答“目标在哪里”的问题。
2. **外观提示分支（V²-Visual）**：通过掩码池化提取查询和目标物体的区域级特征，送入视觉提示匹配器（VPMatcher）进行跨视角外观对齐，生成视觉提示 $P_{\text{visual}}^{q2t}$。该分支回答“目标长什么样”的问题。

**多专家解码与选择** 两类提示分别驱动三个并行的掩码解码专家：
- **Anchor Expert**：仅接收坐标提示，属于训练无关的专家；
- **Visual Expert**：仅接收视觉提示；
- **Fusion Expert**：同时融合两种提示。

三个专家各自产生候选目标掩码 $\hat{M}_{t_k}$。随后，**后处理循环一致性选择器（PCCS）** 利用 V²-Anchor 将每个候选掩码反向投影回查询视图，通过点级循环一致性度量自适应地选择最可靠的预测作为最终输出（Section 3.5）。

**核心设计动机** 跨视角场景中，目标位置和外观均发生剧烈变化，单一模态提示难以应对所有情况。V²-SAM 通过几何与外观双分支的互补设计，结合多专家集成与自适应选择机制，实现了跨视角分割的鲁棒性提升。消融实验证实了这一设计的因果有效性：移除 V²-Anchor 后 Anchor Expert 的 Total-IoU 从 40.1 骤降至 1.5；移除 V²-Visual 后 Visual Expert 的 Total-IoU 从 41.4 降至 3.0（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/002_Figure_2.jpg]]
*Figure 2: Overview of V2-SAM. Given a query–target image pair*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of SAM variants in segmentation capability. Our proposed V²-SAM supports coordinate-point and visualreference prompts for cross-view segmentation*

## 核心模块与公式推导

V²-SAM 的核心在于将跨视角对应问题分解为“在哪里”和“长什么样”两个互补子问题，并设计对应的提示生成模块与多专家分割框架。以下按模块拆解其关键公式与机制。

### 跨视角锚点提示生成器（V²-Anchor）

该模块的目标是在目标视图 $I_t$ 中定位与查询对象几何对应的坐标点。其核心思路是利用 DINOv3 特征提供的空间感知能力，建立跨视角的密集对应。

**密集对应热力图**。给定查询图像 $I_q$ 和目标图像 $I_t$，首先通过冻结的 DINOv3 编码器 $\varphi(\cdot)$ 提取 patch 级特征，然后计算两者之间的余弦相似度热力图：

$$
\mathbf{H}_{ij} = \frac{\varphi(I_q)_i^\top \varphi(I_t)_j}{\lVert \varphi(I_q)_i \rVert_2 \lVert \varphi(I_t)_j \rVert_2}
\tag{1}
$$

其中 $\mathbf{H}_{ij}$ 表示查询图像第 $i$ 个 patch 与目标图像第 $j$ 个 patch 的特征相似度。通过查询对象掩码 $M_q$ 筛选前景区域后，在热力图上提取高置信度的对应点集合 $\mathcal{P}_t$。

**分层采样过滤**。为避免对应点过于集中导致退化，对候选点集施加最小距离约束进行分层采样：

$$
\mathcal{P'}_t = \{ p_i \mid \| p_i - p_j \|_2 > \tau, \forall j < i \}
\tag{2}
$$

该约束确保保留的点之间保持至少 $\tau$ 的距离，从而获得空间分布更均匀的稀疏锚点集。消融实验表明，稀疏锚点数量对性能影响显著：单点表现最佳（Ego2Exo IoU 达 38.7），点数增多反而导致性能下降（Table 9），说明精确的稀疏几何对应比冗余的密集点更有效。

最后，通过确定性几何投影 $\Pi(\cdot)$ 将筛选后的对应点线性映射到 SAM2 的规范坐标空间，形成坐标提示 $P_{anchor}^{q2t}$。

### 跨视角视觉提示生成器（V²-Visual）

V²-Visual 从外观角度回答“目标长什么样”，其核心组件是视觉提示匹配器（VPMatcher），包含特征映射和结构映射两个分支。

**区域特征提取**。利用 SAM2 编码器 $\phi(\cdot)$ 提取图像特征后，通过掩码池化获得查询对象和目标对象的区域级表征：

$$
\mathbf{v}_q = \mathrm{MaskP}(\phi(I_q), M_q), \quad \mathbf{v}_t = \mathrm{MaskP}(\phi(I_t), M_t)
\tag{3}
$$

**结构映射分支的调制机制**。VPMatcher 的结构映射分支基于轻量 CNN 掩码编解码器，通过以下调制公式将查询对象的掩码先验与语义条件融合：

$$
\tilde{\mathbf{m}} = \mathbf{m}_{\mathrm{prior}} \odot (1 + \tanh(\gamma)) + \beta + F_{\mathrm{mask}}(M_q)
\tag{4}
$$

其中 $\mathbf{m}_{\mathrm{prior}}$ 为初始掩码先验，$\gamma$ 和 $\beta$ 来自提示嵌入的语义调制参数，$F_{\mathrm{mask}}(M_q)$ 提供查询掩码的结构信息。调制后的特征经解码器逐步上采样，生成跨视角预测掩码 $\hat{M}_c$。

**视觉提示构造**。将预测的目标区域特征 $\hat{\mathbf{v}}_c$ 与查询特征 $\mathbf{v}_q$ 拼接后经 MLP 投影，形成视觉提示 $P_{visual}^{q2t}$，用于驱动后续的视觉专家解码器。

### 训练损失函数

V²-Visual 的训练采用多目标联合损失，同时约束特征空间、结构空间和掩码空间：

$$
\mathcal{L} = \lambda_1 \mathcal{L}_v(\hat{\mathbf{v}}_c, \mathbf{v}_t) + \lambda_2 \mathcal{L}_s(\hat{M}_c, M_t) + \lambda_3 \mathcal{L}_m(\hat{M}_t, M_t)
\tag{5}
$$

**跨视角对比损失** $\mathcal{L}_v$：强制预测区域特征 $\mathbf{v}_c$ 与真实目标特征 $\mathbf{v}_t$ 在嵌入空间中靠近，同时推开同批次其他样本的特征：

$$
\mathcal{L}_v = -\frac{1}{N} \sum_{i=1}^N \left[ \log \frac{\exp(\sin(\mathbf{v}_c, \mathbf{v}_t)/\tau)}{\sum_{k=1}^N \exp(\sin(\mathbf{v}_c, \mathbf{v}_t^k)/\tau)} + \log \frac{\exp(\sin(\mathbf{v}_t, \mathbf{v}_c)/\tau)}{\sum_{k=1}^N \exp(\sin(\mathbf{v}_t, \mathbf{v}_t^k)/\tau)} \right]
\tag{6}
$$

**掩码预测损失** $\mathcal{L}_m$：组合像素级交叉熵和区域级 Dice 损失，确保分割掩码的精确性：

$$
\mathcal{L}_m = \mathcal{L}_{CE}(\hat{M}, M) + \mathcal{L}_{Dice}(\hat{M}, M)
\tag{7}
$$

$\mathcal{L}_s$ 则对 VPMatcher 结构映射分支施加约束，消融实验证实语义映射与空间映射子模块及对应损失均有正向贡献，组合使用效果最佳（Table 11）。

### 后验循环一致性选择器（PCCS）

PCCS 是多专家框架的关键后处理模块，其核心思想是：一个好的跨视角分割结果应当满足循环一致性——将目标视图的预测掩码反向投影回查询视图，应能恢复原始查询掩码。

对于第 $k$ 个专家产生的目标掩码 $\hat{M}_{t_k}$，PCCS 利用 V²-Anchor 进行反向几何投影：

$$
P_k^{t2q} = \mathrm{V}^2\mathrm{Anchor}(I_t, I_q; \hat{M}_{t_k})
\tag{8}
$$

通过计算反向投影点与原始查询掩码的重合度，PCCS 自适应地选择循环一致性最高的专家输出作为最终结果。消融实验表明，基于点的 Cycle-Points 选择器相比基于掩码的 Cycle-Mask 方案更轻量且精度相近或更优：在两专家（Anchor+Visual）配置下，Exo→Ego 方向 IoU 提升 1.4 点，延迟降低 110 ms（Table 10）。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/003_Figure_3.jpg]]
*Figure 3: The structure of Visual Prompt Matcher. The Structural Mapping Branch is built upon a lightweight CNN-based mask encoder and decoder. The Feature Mapping Branch leverages Transformer-based cross-attention layers, while the Res-MLP component serves as a residual multi-layer perceptron*

## 实验与分析

### 主实验结果

V²-SAM在三个跨视角/跨帧物体分割基准上均取得最优性能，验证了空间提示与视觉提示互补融合的有效性。

**Ego-Exo4D对应基准。** 如 Table 1 所示，V²-SAM（Multi-Experts配置）在Ego-Exo4D v2测试集上达到 **48.0 Total-IoU**，较此前最优方法O-MaMa（43.4）提升 **+4.6点**。在方向性子任务中，Ego→Exo方向IoU达46.3（O-MaMa为42.6，+3.7），Exo→Ego方向同样显著领先。这一结果直接验证了核心洞察：空间提示（V²-Anchor）回答“在哪里”，视觉提示（V²-Visual）回答“长什么样”，两者互补后大幅提升了跨视角场景下的分割鲁棒性。

**DAVIS-2017视频物体对应。** 在20帧间隔的DAVIS-2017验证集上（Table 2），V²-SAM取得 **78.8 J&F_m**，较先前最佳方法PCC（70.2）提升 **+8.6点**。这表明即使在同一视频域内，当时间间隔导致显著外观变化时，几何锚点与外观对齐的双分支策略依然有效。

**HANDAL-X零样本分割。** 在零样本设定下（Table 3），V²-SAM的IoU达 **77.2**，远超端到端方法ObjectRelator（42.8，+34.4）。这一跨数据集泛化能力源于V²-Anchor基于DINOv3的几何对应不依赖目标域训练，而V²-Visual的视觉提示匹配器通过特征映射与结构映射双分支设计，能有效弥合跨域外观差异。

### 消融实验与机制验证

消融实验系统性地揭示了各模块的贡献权重与失效边界。

**双提示的不可或缺性。** Table 4的单个专家消融是最具决定性的证据：Anchor Expert在移除V²-Anchor后，Total-IoU从40.1骤降至 **1.5**；Visual Expert在移除V²-Visual后，Total-IoU从41.4降至 **3.0**。这表明任一提示的缺失都会导致分割系统几乎完全失效——几何对应提供跨视角定位基础，外观对齐提供目标辨识信息，二者缺一不可。

**稀疏锚点数量的非单调效应。** Table 9揭示了V²-Anchor中稀疏锚点数量的反直觉规律：单点对应表现最佳（Ego→Exo IoU 38.7），随着点数增加至5、10、30，性能反而持续下降。这一现象的因果机制在于：DINOv3的密集特征匹配在物体区域内会产生多个候选对应点，但跨视角下物体内部几何形变导致多数点存在偏差；分层采样（Equation 2）筛选出的单一质心点反而能最大程度抑制异常值，过多锚点会引入噪声，干扰SAM2解码器的掩码预测。

**PCCS选择器的轻量优势。** Table 10对比了基于点的循环一致性选择器（Cycle-Points）与基于掩码的版本（Cycle-Mask）：在两专家组合（Anchor+Visual）下，Cycle-Points在Exo→Ego方向IoU提升 **1.4点**，同时延迟降低 **110 ms**。其核心机制在于：V²-Anchor本身已提供高质量的点级几何对应，PCCS通过反向投影（Equation 8）在点空间进行一致性验证，避免了掩码级投影引入的累计误差与计算开销。

**VPMatcher子模块的协同增益。** Table 11的模块消融表明，语义映射分支（L_v损失监督）与空间映射分支（L_s损失监督）各自提供正向贡献，二者组合使用时效果最优。这验证了VPMatcher设计中“特征映射回答语义匹配，结构映射回答空间对齐”的双重互补机制。

### 多专家组合分析

Table 5展示了不同专家解码器组合的性能。Anchor Expert单独使用时已具备基础跨视角定位能力，Visual Expert补充外观信息后性能提升，而Fusion Expert的加入进一步带来增益。PCCS选择器在三专家全组合下达到最优Total-IoU 48.0，表明自适应选择机制能够根据不同场景特性动态依赖最可靠的专家输出——在几何对应置信度高时倾向Anchor Expert，在外观歧义大时依赖Visual Expert的语义匹配能力。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/004_Table_1.jpg]]
*Table 1: Results on the Ego-Exo4D Correspondences v2 test split*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/005_Table_2.jpg]]
*Table 2: Comparison of video object correspondence on DAVIS-2017 Val with a temporal gap of 20 frames*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/006_Table_3.jpg]]
*Table 3: Comparison of zero-shot (ZSL) object segmentation on HANDAL-X*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/007_Table_4.jpg]]
*Table 4: Ablation on individual experts*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/008_Table_5.jpg]]
*Table 5: Results of different expert decoder combinations on v2 test split. A: Anchor Expert, B: Visual Expert, C: Fusion Expert*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/009_Figure_4.jpg]]
*Figure 4: Comparison of Anchor, Visual, and Fusion Experts across different scenes. Left: per-scene IoU radar plot for the three experts. Right: per-scene Win% bars showing PCCS selections*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/016_Table_9.jpg]]
*Table 9: Ablation of sparse anchor point count in the*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/018_Table_10.jpg]]
*Table 10: Ablation on the Post-hoc Cyclic Consistency Selector in Ego↔Exo correspondence. We compare Cycle-Points (Ours) with the mask-based Cycle-Mask (Prior) on two decoder combinations: A+B (Anchor+Visual) and A+B+C (Anchor+Visual+Fusion)*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2511_20886/figures/010_Figure_5.jpg]]
*Figure 5: Ego2Exo qualitative results. From left to right: query view, predictions from the Anchor Expert, Visual Expert, and Fusion Expert, followed by the final output selected by the PCCS*

## 方法谱系与知识库定位

### 跨视角分割的方法谱系

V²-SAM 处于**跨视角物体分割**与**基于提示的分割大模型**两条技术路线的交汇点。其核心贡献在于为 SAM2 这类“单视角提示专家”注入跨视角几何与外观对应能力，使其能够在视角剧烈变化下保持可靠的物体分割。

#### 与基于候选匹配的方法对比

**O-MaMa** 代表了跨视角物体对应的传统范式：先在目标视角生成大量候选掩码，再通过匹配策略选择最优对应。这一范式将“定位”与“分割”解耦，但候选质量高度依赖底层分割器的泛化能力。V²-SAM 则通过 V²-Anchor 直接将几何对应转化为坐标提示，跳过了候选枚举步骤。在 Ego-Exo4D v2 测试集上，V²-SAM 的 Total-IoU 达到 48.0，较 O-MaMa 的 43.4 提升 4.6 点（Table 1），验证了“端到端提示驱动”相比“候选匹配”范式的优势。

#### 与端到端跨视角分割方法对比

**ObjectRelator** 是端到端跨视角分割的代表性工作，直接学习从查询掩码到目标掩码的映射。然而，这类方法在零样本场景下泛化能力有限。在 HANDAL-X 零样本分割测试中，V²-SAM 取得 77.2 IoU，而 ObjectRelator 仅为 42.8（Table 3），差距达 34.4 点。这一巨大差异揭示了 V²-SAM 的关键设计优势：通过解耦几何定位（V²-Anchor）与外观对齐（V²-Visual），模型不再需要“记忆”特定场景的视角变换模式，而是依赖 DINOv3 的通用几何特征空间和跨视角外观映射来泛化。

#### 与基于视觉提示的 SAM 扩展对比

**Ref-SAM*** 代表了将 SAM 扩展至视觉参考提示的技术路线。其核心思路是将参考图像的区域特征编码为提示嵌入，引导 SAM 在新图像中分割相似物体。V²-SAM 的 Visual Expert 分支继承了这一范式，但引入了两个关键改进：（1）通过 VPMatcher 显式建模跨视角外观对齐，而非简单依赖特征相似度；（2）与 Anchor Expert 和 Fusion Expert 形成多专家集成。消融实验表明，单独使用 Visual Expert（无 V²-Visual）时 Total-IoU 仅为 3.0（Table 4），说明纯视觉提示在跨视角场景中极易失效——这正是 V²-SAM 引入几何锚点提示的动机。

#### 与官方共分割基线对比

**XSegTx** 是 Ego-Exo4D 基准的官方跨视角共分割方法。V²-SAM 在 Ego→Exo 和 Exo→Ego 两个方向上均显著超越该基线（Table 1），表明通用分割大模型结合任务特定提示生成，可以超越专门为共分割设计的传统方法。

#### 与零样本分割方法对比

**PSALM** 作为零样本分割方法，在 DAVIS-2017 视频物体对应任务上取得了一定效果。V²-SAM 在该基准上以 78.8 J&F_m 超越 PSALM 及其他方法（Table 2），证明了跨视角提示生成机制在时序对应场景中同样有效——因为视频帧间物体对应本质上是一种“弱跨视角”问题。

### 关键设计选择与知识贡献

V²-SAM 的核心知识贡献可归纳为三个层次：

**第一层：双提示互补机制。** 空间提示（V²-Anchor）回答“目标在哪里”，视觉提示（V²-Visual）回答“目标长什么样”。Table 4 的消融实验提供了决定性证据：移除 V²-Anchor 后 Anchor Expert 的 Total-IoU 从 40.1 骤降至 1.5；移除 V²-Visual 后 Visual Expert 的 Total-IoU 从 41.4 降至 3.0。这表明在跨视角场景中，单一提示类型极易完全失效，而双提示互补是鲁棒分割的必要条件。

**第二层：多专家解耦与集成。** V²-SAM 将三种提示配置（纯几何、纯外观、融合）分配给三个独立专家解码器，而非在单一解码器中混合。Figure 4 的雷达图揭示了这一设计的深层动机：不同场景对不同专家的偏好差异巨大——某些场景 Anchor Expert 占优，另一些场景 Visual Expert 更可靠。PCCS 通过点级循环一致性自适应选择最优专家，在 A+B 配置下 Exo→Ego IoU 较 Cycle-Mask 方案提升 1.4 点，同时延迟降低 110 ms（Table 10）。

**第三层：几何对应的稀疏化策略。** V²-Anchor 的稀疏锚点数量对性能有显著影响。Table 9 显示，单点对应表现最佳（Ego→Exo IoU 38.7），随着点数增加至 5、10、30，性能反而下降。这一反直觉现象揭示了跨视角几何对应的一个关键特性：在存在大量外点的情况下，保守地选择最可靠的单一对应点，比引入更多但不可靠的对应点更有效。分层采样策略（Equation 2）正是为此设计。

### 适用边界与局限

**适用场景：** V²-SAM 在以下条件下表现最优：（1）存在可检测的几何对应点（场景纹理足够丰富）；（2）物体外观在跨视角下保留一定可辨识特征；（3）目标物体在查询视图中已有精确掩码标注。Ego-Exo4D、DAVIS-2017 和 HANDAL-X 三个基准覆盖了第一人称跨视角、视频时序对应和零样本机器人场景，验证了方法的广泛适用性。

**已知局限：** 当前验证分析中未提取到明确的局限性声明。但基于方法设计可推断以下潜在边界：（1）V²-Anchor 依赖 DINOv3 的几何感知特征，在极端无纹理场景（如纯色墙壁上的物体）中几何对应可能失效；（2）PCCS 的选择质量依赖于至少一个专家能产生合理预测——若所有专家同时失效，选择器无法挽救；（3）多专家并行推理增加了计算开销，尽管 PCCS 的轻量设计缓解了这一问题。

### 开放问题

当前验证分析中未提取到明确的开放问题声明。基于方法设计可提出以下值得探索的方向：（1）能否将 PCCS 的“事后选择”升级为“在线门控”，使专家在推理过程中动态协作而非独立预测？（2）V²-Anchor 的稀疏锚点数量为何与性能呈负相关？是否存在自适应确定最优锚点数量的机制？（3）双提示互补机制能否推广至其他视觉基础模型的跨域适应任务？这些问题需要进一步实验验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/V_SAM_Marrying_SAM2_with_Multi_Prompt_Experts_for_Cross_View_Object_Correspondence.pdf]]

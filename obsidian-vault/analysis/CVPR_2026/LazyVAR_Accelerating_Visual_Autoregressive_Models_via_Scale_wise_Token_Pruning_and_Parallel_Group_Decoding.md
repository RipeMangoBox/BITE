---
title: "LazyVAR: Accelerating Visual Autoregressive Models via Scale-wise Token Pruning and Parallel Group Decoding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LazyVAR_Accelerating_Visual_Autoregressive_Models_via_Scale_wise_Token_Pruning_and_Parallel_Group_Decoding.pdf
project_link: null
code_link: null
aliases:
- LazyVAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用相邻尺度聚合潜特征之间的余弦相似性作为尺度级更新指标（Update Index），在大尺度上对更新微小的令牌进行剪枝，并基于高相似性将多个连续尺度编组实现并行解码，从而大幅减少活跃令牌数和串行步骤。
primary_logic: 相邻尺度聚合潜特征的相似性随尺度增大而逐渐升高，大尺度上约94%令牌的余弦相似度超过0.95，表明大部分令牌更新极小；该更新模式具有跨尺度一致性，与生成图像的高频细节密切相关，因此可作为可靠的剪枝准则，并支撑并行组解码的近似。
claims:
- 在 Infinity 和 HART 两个 VAR 模型上，大尺度余弦相似度分布右偏且峰值接近1，例如第11个尺度94%令牌相似度>0.95
- LazyVAR 在 Infinity 上实现 2.94× 加速，推理时间从 1.38s 降至 0.47s，GenEval Overall 从 0.685 微升至 0.686
- Update Index 与生成图像补丁的方差存在显著 Spearman 秩相关，表明模型优先更新高频细节令牌
- 相邻尺度的 Update Index 之间存在显著 Spearman 相关，验证了跨尺度更新模式的一致性
---

# LazyVAR: Accelerating Visual Autoregressive Models via Scale-wise Token Pruning and Parallel Group Decoding

> [!tip] 核心洞察
> 相邻尺度聚合潜特征的相似性随尺度增大而逐渐升高，大尺度上约94%令牌的余弦相似度超过0.95，表明大部分令牌更新极小；该更新模式具有跨尺度一致性，与生成图像的高频细节密切相关，因此可作为可靠的剪枝准则，并支撑并行组解码的近似。

| 字段 | 内容 |
|------|------|
| 中文题名 | LazyVAR：通过尺度级令牌剪枝和并行组解码加速视觉自回归模型 |
| 英文题名 | LazyVAR: Accelerating Visual Autoregressive Models via Scale-wise Token Pruning and Parallel Group Decoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Mao_LazyVAR_Accelerating_Visual_Autoregressive_Models_via_Scale-wise_Token_Pruning_and_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LazyVAR |
| Dataset | GenEval, MJHQ-30K, HPSv2.1 |

> [!tip] 效果简介
> - GenEval 上，推理时间↓ (1024×1024) Infinity+LazyVAR: 0.47 s vs Infinity: 1.38 s (-0.91 s (2.94×))；Overall↑ Infinity+LazyVAR: 0.686 vs Infinity: 0.685 (+0.001)；推理时间↓ (1024×1024) HART+LazyVAR: 0.48 s vs HART: 0.80 s (-0.32 s (1.67×))。
> - MJHQ-30K 上，FID↓ Infinity+LazyVAR: 9.83 vs Infinity: 9.80 (+0.03)。
> - HPSv2.1 上，Average Infinity+LazyVAR: 29.83 vs Infinity: 30.44 (-0.61)。

## 概述

视觉自回归（Visual Autoregressive, VAR）模型通过将图像生成分解为多尺度令牌图的逐尺度预测，在文本到图像生成任务中取得了显著进展。然而，其固有的计算瓶颈严重制约了高分辨率图像生成的推理效率：随着尺度增大，令牌数量呈平方级增长（$\mathcal{O}(n^2)$），注意力计算复杂度更达到 $\mathcal{O}(n^4)$；同时，尺度间的严格串行解码机制使得不同分辨率的生成步骤无法并行，导致总体推理延迟居高不下。

本文的核心发现是：在 VAR 模型的生成过程中，相邻尺度聚合潜特征之间的余弦相似度随尺度增大而逐渐升高——在 Infinity 和 HART 两个代表性模型上，第 11 个尺度约 94% 令牌的余弦相似度超过 0.95（Figure 2），表明大部分令牌在大尺度上的更新量极小。这一“尺度级更新惰性”现象具有跨尺度一致性，且与生成图像的高频细节区域显著相关（Figure 3b），为高效的令牌剪枝和并行解码提供了可靠的统计依据。

基于上述洞察，**LazyVAR** 提出了一种无训练、即插即用的 VAR 加速方法，其核心包含两个协同模块：
- **尺度级令牌剪枝（Update Index Guided Token Pruning, UIGTP）**：以相邻尺度聚合潜特征的余弦相似度作为“更新指标”（Update Index），在大尺度上仅保留更新显著的令牌参与后续计算，将其余令牌剪枝并置零残差，从而大幅削减活跃令牌数量。
- **并行组解码（Parallel Group Decoding, PGD）**：利用相邻尺度聚合特征的高度相似性，将多个连续尺度编为一组，统一以同一聚合特征插值作为近似输入，实现组内多尺度 Transformer 前向的并行计算，打破原有的串行依赖。

在方法谱系中，LazyVAR 区别于 FastVAR（Guo et al., arXiv 2025）等前期工作——后者基于频率域信息进行令牌选择，而 LazyVAR 直接从 VAR 模型内在的尺度间特征更新模式出发，以无监督的相似性度量驱动剪枝，展现出更强的质量保持能力。

实验结果表明，LazyVAR 在 Infinity（Han et al., arXiv 2024）和 HART（Tang et al., arXiv 2024）两个基线模型上均实现了显著的推理加速与质量保持：在 GenEval 基准上，Infinity+LazyVAR 的推理时间从 1.38 s 降至 0.47 s（2.94× 加速），GenEval Overall 从 0.685 微升至 0.686；HART+LazyVAR 的推理时间从 0.80 s 降至 0.48 s（1.67× 加速）。在 MJHQ-30K 上，FID 仅从 9.80 微增至 9.83，几乎无质量损失（Table 1）。消融实验进一步验证了 UIGTP 剪枝准则和 PGD 并行策略各自的有效性，其中 PGD 在剪枝基础上额外贡献约 1.45× 加速，且质量几乎无损失（Table 7）。

## 背景与动机

### 视觉自回归模型的计算瓶颈

视觉自回归（Visual Autoregressive, VAR）模型将传统自回归生成从“下一个令牌”转变为“下一个尺度”，通过多尺度令牌图逐级生成高分辨率图像。然而，这一范式面临两个根本性的计算挑战：

1. **令牌数量的平方级增长**：随着生成尺度 $k$ 的增大，令牌数量以 $\mathcal{O}(n^2)$ 的速度扩张，而自注意力机制的计算复杂度更是达到 $\mathcal{O}(n^4)$。在生成 1024×1024 分辨率图像时，大尺度上的活跃令牌数急剧膨胀，成为推理延迟的主要来源。

2. **尺度间严格串行解码**：VAR 模型的多尺度令牌图联合分布为 $p(\mathbf{r}_1, \mathbf{r}_2, \ldots, \mathbf{r}_K) = \prod_{k=1}^{K} p(\mathbf{r}_k \mid \mathbf{r}_1, \mathbf{r}_2, \ldots, \mathbf{r}_{k-1}, c)$（公式 1），要求每个尺度必须等待前序尺度完成后方可计算。这种串行依赖使得不同尺度间的推理无法并行，进一步加剧了高分辨率生成时的延迟问题。

以 **Infinity**（Han et al., arXiv 2024）为例，在 RTX 4090 GPU 上生成一张 1024×1024 图像需耗时 1.38 秒，其中大尺度阶段占据了绝大部分计算开销。

### 现有加速方法的局限

针对 VAR 模型的推理加速，前期工作 **FastVAR**（Guo et al., arXiv 2025）提出了基于频率的令牌剪枝方法。然而，该方法在设计上存在明显不足：其剪枝准则未能充分捕捉 VAR 模型内部多尺度特征更新的本质规律，导致剪枝后生成质量出现不可忽视的退化。消融实验表明，将 LazyVAR 的剪枝准则替换为 FastVAR 的 PTS 方法后，GenEval Overall 从 0.686 降至 0.665（Table 8），验证了更精确的剪枝准则设计的必要性。

### 核心洞察：大尺度特征更新的高度冗余性

LazyVAR 的核心动机源于对 VAR 模型内部特征更新模式的深入观察。定义第 $k$ 个尺度的**聚合潜特征**为前 $k$ 个尺度残差插值到最终分辨率的累计和：

$$\hat{f}_k = \hat{f}_{k-1} + \mathrm{Interpolate}\big(r_k, (h_K, w_K)\big)$$

通过分析相邻尺度聚合潜特征之间的余弦相似度，论文发现了三个关键规律（Figure 2, Figure 3）：

- **相似度随尺度增大而单调升高**：在 Infinity 和 HART 两个 VAR 模型上，相邻尺度聚合潜特征的余弦相似度分布随尺度索引增大而显著右偏，峰值趋近于 1。例如，在第 11 个尺度上，约 **94% 的令牌余弦相似度超过 0.95**（Figure 2），表明大尺度上绝大部分令牌的更新量极小。

- **更新模式与图像高频细节相关**：令牌级的更新指标（Update Index，定义为 $1 - \cos\langle\hat{f}_{k-1}, \hat{f}_k\rangle$）与最终生成图像对应补丁的像素方差之间存在显著的 Spearman 秩相关（Figure 3b）。这意味着模型在大尺度上优先更新高频细节区域，而平坦区域的令牌几乎不再变化。

- **跨尺度更新模式具有一致性**：相邻尺度的 Update Index 之间存在显著的 Spearman 相关（Figure 3c），表明令牌的更新行为在连续尺度间保持稳定，使得基于前一尺度的更新指标来预测当前尺度的令牌重要性成为可能。

### 本文动机

上述发现揭示了 VAR 模型大尺度推理中存在大量可被安全剪枝的冗余计算，且更新模式的可预测性为并行解码提供了近似依据。基于此，LazyVAR 提出了一种**无训练、即插即用**的加速方案：利用尺度级更新指标（Update Index）指导大尺度令牌剪枝，同时将更新微小的连续尺度编组实现并行解码，从而在几乎不损失生成质量的前提下大幅降低推理延迟。

## 核心创新

LazyVAR 的核心创新在于将 VAR 模型推理过程中**尺度间令牌更新的冗余性**转化为两个相互协同的加速机制：**基于更新指标的尺度级令牌剪枝（Update Index Guided Token Pruning, UIGTP）**与**并行组解码（Parallel Group Decoding, PGD）**。该方法无需任何额外训练或微调，以即插即用方式作用于现有 VAR 模型。

### 关键洞察：大尺度令牌更新的高度冗余

VAR 模型在生成高分辨率图像时，令牌数量随尺度增大呈平方级增长（$\mathcal{O}(n^2)$），注意力计算复杂度更达 $\mathcal{O}(n^4)$，且各尺度间严格串行解码，构成推理延迟的主要瓶颈。LazyVAR 的核心洞察在于：**相邻尺度的聚合潜特征（aggregated latent features）之间的余弦相似度随尺度增大而持续升高**。如 Figure 2 所示，在第 11 个尺度上，约 94% 令牌的余弦相似度超过 0.95，表明绝大多数令牌在后续尺度中更新极小。这一“懒惰更新”现象为大规模令牌剪枝提供了可靠的统计基础。

进一步分析（Figure 3b）揭示，该更新指标与最终生成图像中对应补丁的像素方差存在显著的 Spearman 秩相关，说明模型优先更新高频细节区域的令牌，而平坦区域令牌的更新幅度极低。同时，相邻尺度的更新指标之间也存在显著的跨尺度 Spearman 相关（Figure 3c），验证了更新模式的跨尺度一致性——这正是后续并行组解码近似假设的实证支撑。

### Changed Slot 1：令牌参与策略——从全量计算到更新驱动的选择性激活

| 维度 | 基线方法（Infinity / HART） | LazyVAR 方法 |
|------|---------------------------|-------------|
| 大尺度令牌策略 | 所有令牌均参与 Transformer 前向计算 | 基于前一尺度的 Update Index 排序，仅保留更新幅度最大的部分令牌，其余剪枝并将其残差置零 |
| 剪枝准则 | 无剪枝 | `Update.Index_k = 1 - cos⟨f̂_{k-1}, f̂_k⟩`，值越大表示更新越显著，优先保留 |
| 作用范围 | — | 仅作用于较大尺度（如 Infinity 的尺度 10-13），小尺度完整保留以维护语义与结构完整性 |

这一设计将令牌参与从“全量激活”转变为“按需激活”。具体而言，在第 $k$ 个尺度，基于前一尺度聚合特征 $\hat{f}_{k-1}$ 与当前尺度聚合特征 $\hat{f}_k$ 的余弦距离计算逐令牌的 Update Index，按值降序排列后仅保留前 $n_k$ 个令牌继续参与后续计算，其余令牌的残差直接被置零。这一策略直接将活跃令牌数削减 1-2 个数量级，大幅降低 Transformer 的计算开销。

### Changed Slot 2：解码并行性——从严格串行到近似驱动的并行组解码

| 维度 | 基线方法（Infinity / HART） | LazyVAR 方法 |
|------|---------------------------|-------------|
| 尺度间解码方式 | 各尺度严格串行，每个尺度必须等待前一个尺度完成 | 将 $p$ 个连续尺度编为一组，组内所有尺度共享同一聚合特征进行近似输入，实现 Transformer 前向的并行计算 |
| 近似假设 | — | 组内后续尺度的输入 $\tilde{r}_{k+m}$ 直接由 $\hat{f}_{k-1}$ 插值得到，而非等待前序尺度残差累积 |

并行组解码的核心在于利用前述“跨尺度更新模式一致性”的发现：既然相邻尺度的聚合特征高度相似，那么组内后续尺度的输入可以直接用组首前一尺度的聚合特征 $\hat{f}_{k-1}$ 插值近似，即 $\tilde{r}'_{k+m} = \mathrm{Interpolate}(\hat{f}_{k-1}, (h_{k+m}, w_{k+m}))$。这使得组内 $p$ 个尺度的 Transformer 前向计算可以并行执行，将串行步骤数从 $p$ 步压缩为 1 步。

### 两种机制的协同效应

UIGTP 与 PGD 并非独立运作，而是形成正向协同：UIGTP 削减了每个尺度内的活跃令牌数，降低了单步计算量；PGD 则削减了串行步骤数，释放了并行潜力。消融实验（Table 7）表明，在 Infinity 上，仅剪枝（w/o PGD）可实现约 2.03× 加速，加入并行组解码后进一步提升至 2.94×（额外约 1.45× 加速），且生成质量几乎无损失（GenEval Overall 从 0.685 微升至 0.686）。这一协同使得 Infinity-2B 模型在单块 RTX 4090 上生成 1024×1024 图像的推理时间从 1.38s 降至 0.47s。

### 与现有加速方法的本质区别

与同期工作 **FastVAR**（Guo et al., arXiv 2025）相比，LazyVAR 的剪枝准则具有根本性差异。FastVAR 采用基于频率的 PTS 准则进行令牌选择，而 LazyVAR 的 Update Index 直接从相邻聚合潜特征的余弦相似度导出。消融实验（Table 8）显示，将 LazyVAR 的剪枝准则替换为 PTS 后，GenEval Overall 从 0.686 降至 0.665，表明更新驱动的剪枝准则在保持生成质量方面具有显著优势。这一差异的根源在于：Update Index 直接度量了令牌在潜空间中的实际更新幅度，与生成质量的关系更为紧密；而频率准则仅间接反映令牌的重要性，可能错误地剪除对细节生成关键的低频但持续更新的令牌。

## 整体框架

LazyVAR 是一种无训练、即插即用的 VAR 模型加速方法，其整体流程如 **Figure 4** 所示。该方法的核心思想是：在保持小尺度完整不变以维护生成图像的语义与结构完整性的前提下，对大尺度进行选择性令牌剪枝和并行组解码，从而大幅减少活跃令牌数量和串行解码步骤。

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/005_Figure_4.jpg]]
*Figure 4: Overview of LazyVAR. The smaller scales are kept intact to preserve the semantic and structural integrity of the generated image. At larger scales, pruning is guided by the Update Index, and the pruned steps are grouped to enable parallel inference*

### 输入输出流

LazyVAR 直接作用于预训练 VAR 模型的多尺度生成过程，不改变模型权重，不引入额外训练。其输入为文本条件 $c$ 和已生成的前序尺度残差 $\{\mathbf{r}_1, \mathbf{r}_2, \ldots, \mathbf{r}_{k-1}\}$，输出为当前尺度及后续尺度的残差预测。整个流程可划分为三个阶段：

1. **小尺度完整解码（尺度 1 至 $i-1$）**：所有令牌均参与正向计算，严格遵循原始 VAR 的串行自回归范式，确保低频结构信息无损。
2. **大尺度剪枝与并行组解码（尺度 $i$ 至 $K$）**：依据尺度级更新指标（Update Index）对令牌进行选择性激活，剪枝掉更新微小的令牌；同时将 $p$ 个连续尺度编为一组，利用近似输入实现并行 Transformer 前向计算。
3. **残差累积与聚合特征更新**：每个尺度解码完成后，将残差插值至最终分辨率并累加至聚合潜特征 $\hat{f}_k$，供下一组尺度使用。

### 模块关系

LazyVAR 由两个紧密协作的核心模块构成：

**Update Index 计算模块**负责量化相邻尺度间每个令牌的更新幅度。具体而言，对于尺度 $k$，其聚合潜特征 $\hat{f}_k$ 定义为前 $k$ 个尺度残差插值至最终分辨率的累计和（公式 (2)）。尺度 $k$ 的 Update Index 定义为：

$$\mathrm{Update.Index}_k = 1 - \cos\langle \hat{f}_{k-1}, \hat{f}_k \rangle \in [0, 2]^{h_K \times w_K}$$

该指标值越大，表示对应令牌在相邻尺度间的更新越显著。这是整个方法的因果旋钮——它直接决定哪些令牌值得继续参与计算。

**尺度级令牌剪枝（UIGTP）与并行组解码（PGD）模块**基于 Update Index 执行加速策略。UIGTP 依据 Update Index 排序，仅保留更新幅度最大的 $n_k$ 个令牌继续参与正向计算，其余令牌被剪枝并将其残差置零（公式 (10)）。PGD 则利用相邻尺度聚合特征高度相似的观察，将同组内后续尺度的输入统一近似为：

$$\tilde{r}'_{k+m} = \mathrm{Interpolate}\bigl(\hat{f}_{k-1}, (h_{k+m}, w_{k+m})\bigr)$$

从而使得 $p$ 个连续尺度的 Transformer 前向计算可以并行执行（公式 (9)），打破原始 VAR 的串行依赖瓶颈。

### 关键设计决策

- **剪枝仅作用于大尺度**：实验表明，小尺度（如尺度 1-8）的聚合潜特征相似性较低，过早剪枝会破坏语义与结构完整性，因此 LazyVAR 仅在尺度 $i$ 及之后启动剪枝。
- **分组策略与剪枝比例协同**：以 Infinity 模型为例，默认将尺度 10-13 编为一组（$p=4$），各尺度令牌保留比例分别为 $[20\%, 10\%, 5\%, 1\%]$；HART 模型则将尺度 12-13 编为一组，保留比例 $[30\%, 20\%]$。这种协同设计在加速比与生成质量之间取得了最优平衡。
- **近似假设的合理性**：并行组解码的核心近似 $\tilde{r}_{k+m} \approx \tilde{r}'_{k+m}$ 依赖于相邻尺度聚合特征高度相似的观察——在大尺度上约 94% 令牌的余弦相似度超过 0.95（**Figure 2**），且 Update Index 的跨尺度 Spearman 相关显著（**Figure 3c**），为近似提供了实证支撑。

## 核心模块与公式推导

LazyVAR 由两个核心模块构成：**尺度级令牌剪枝（Update Index Guided Token Pruning, UIGTP）** 和 **并行组解码（Parallel Group Decoding, PGD）**。二者共同作用于 VAR 模型的大尺度推理阶段，通过减少活跃令牌数量和打破串行依赖实现加速。

### 聚合潜特征与更新指标

VAR 模型在尺度 $k$ 输出残差令牌图 $r_k \in \mathbb{R}^{h_k \times w_k \times C}$，将其插值到最终分辨率 $(h_K, w_K)$ 后逐尺度累加，得到第 $k$ 个尺度的聚合潜特征：

$$
\hat{f}_k = \hat{f}_{k-1} + \mathrm{Interpolate}\big(r_k, (h_K, w_K)\big) \tag{3}
$$

其中 $\hat{f}_0$ 初始化为零。该递归形式使得相邻尺度间的特征更新可直接量化。定义**尺度级更新指标（Update Index）** 为 $\hat{f}_{k-1}$ 与 $\hat{f}_k$ 的余弦距离：

$$
\mathrm{Update.Index}_k = 1 - \cos\langle \hat{f}_{k-1}, \hat{f}_k \rangle \in [0, 2]^{h_K \times w_K} \tag{4}
$$

该指标在空间维度上是逐令牌的：值越大，表示该令牌位置从尺度 $k-1$ 到 $k$ 的更新越显著。实证分析表明，在大尺度上约 94% 令牌的余弦相似度超过 0.95（Figure 2），且 Update Index 与生成图像补丁的像素方差存在显著 Spearman 秩相关（Figure 3b），说明模型在大尺度上优先更新高频细节令牌，而大部分令牌更新极小——这构成了剪枝的经验基础。

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/003_Figure_2.jpg]]
*Figure 2: Distribution of the cosine similarity between adjacent aggregated latent features across scales*

### 尺度级令牌剪枝（UIGTP）

在尺度 $k$ 的 Transformer 前向计算中，输入 $\tilde{r}_k$ 由上一尺度的聚合特征下采样得到：

$$
\tilde{r}_k = \mathrm{Interpolate}\big(\hat{f}_{k-1}, (h_k, w_k)\big) \tag{5}
$$

UIGTP 的核心操作是：利用尺度 $k-1$ 计算得到的 Update Index 对尺度 $k$ 的令牌进行选择性激活。具体地，将 Update Index 值排序后，仅保留前 $n_k$ 个更新最显著的令牌参与 Transformer 计算，其余令牌被剪枝，其对应残差置零。剪枝从预设的起始尺度 $i$ 开始，小尺度（如 1–8）保持完整以保护语义与结构完整性。

### 并行组解码（PGD）

自回归解码的本质瓶颈在于尺度 $k$ 的输入 $\tilde{r}_k$ 依赖于 $k-1$ 的输出。LazyVAR 的观察是：在大尺度上相邻聚合特征高度相似，因此同组内后续尺度的输入可直接用组首尺度 $k$ 的聚合特征 $\hat{f}_{k-1}$ 近似：

$$
\tilde{r}_{k+m} \approx \tilde{r}'_{k+m} = \mathrm{Interpolate}\big(\hat{f}_{k-1}, (h_{k+m}, w_{k+m})\big) \tag{6}
$$

基于此近似，将 $p$ 个连续尺度编为一组，组内所有尺度的输入均从同一 $\hat{f}_{k-1}$ 插值得到，从而消除尺度间的串行依赖，实现 Transformer 前向的并行计算：

$$
r_k, \ldots, r_{k+p} = \mathrm{Blocks}\big(\tilde{r}_1, \tilde{r}_2, \ldots, \tilde{r}'_k, \ldots, \tilde{r}'_{k+p}, c\big) \tag{9}
$$

并行解码后，各尺度输出残差按原始分辨率插值并累加，更新聚合特征供下一组使用。PGD 在 UIGTP 剪枝的基础上进一步压缩串行步骤数，消融实验表明其相比仅剪枝（w/o PGD）额外带来约 1.45× 加速，且生成质量几乎无损失（Table 7）。

### 默认配置

在 **Infinity**（Han et al., arXiv 2024）上，剪枝从尺度 10 开始，尺度 10–13 编为一组，令牌保留率分别为 [20%, 10%, 5%, 1%]；在 **HART**（Tang et al., arXiv 2024）上，尺度 12–13 编组，保留率为 [30%, 20%]。两种配置均为无训练、即插即用，无需修改模型权重。

## 实验与分析

### 主要结果：推理速度与生成质量的权衡

LazyVAR 在两类 VAR 文本到图像模型上均实现了显著的推理加速，同时生成质量几乎无损。在 GenEval 基准上，Infinity+LazyVAR 将 1024×1024 图像的推理时间从 1.38 s 降至 0.47 s，加速比达 2.94×；GenEval Overall 指标从 0.685 微升至 0.686（Table 1）。HART+LazyVAR 在同等分辨率下推理时间从 0.80 s 降至 0.48 s，加速 1.67×，Overall 指标仅下降 0.8%（Table 2）。所有测试均在单块 RTX 4090 GPU 上使用官方发布权重完成，方法无需任何额外训练或微调。

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/006_Table_1.jpg]]
*Table 1: Comparison of inference efficiency and generation quality on GenEval and MJHQ-30K benchmarks. All models were evaluated on a single RTX 4090 GPU. ↑ indicates higher is better, and ↓ indicates lower is better. †Models marked with a dagger can only generate images up to 512 × 512 resolution; all others support 1024 × 1024 resolution*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/007_Table_2.jpg]]
*Table 2: Comprehensive quantitative evaluation on the GenEval benchmark*

在 MJHQ-30K 基准上，Infinity+LazyVAR 的 FID 为 9.83，与原始 Infinity 的 9.80 几乎持平（Table 1），CLIP 得分亦保持稳定（Table 3）。HPSv2.1 人类偏好评估显示，Infinity+LazyVAR 的平均得分为 29.83，略低于原始模型的 30.44（Table 5），表明加速带来的质量损失在主观感知层面极为有限。

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparisons of FID and CLIP scores on several categories in the MJHQ-30K benchmark*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/011_Table_5.jpg]]
*Table 5: Comprehensive quantitative evaluation on HPSv2.1*

加速幅度的差异源于两个模型在大尺度上的相似性特性不同：Infinity 在大尺度上约 94% 令牌的余弦相似度超过 0.95（Figure 2），为激进剪枝提供了充分依据；HART 作为混合离散/连续模型，其聚合潜特征的相似性分布相对分散，因此仅对最后两个尺度进行剪枝和编组，加速比相应较低。

### 消融实验

**剪枝比例。** 默认 Infinity 配置对尺度 10–13 分别采用 [20%, 10%, 5%, 1%] 的令牌保留比例，实现 2.94× 加速，GenEval Overall 0.686、FID 9.83。过度剪枝（如 [30%, 30%] 均匀保留）导致速度提升有限且生成质量下降（Table 6）。剪枝可视化（Figure 6）进一步表明，LazyVAR 优先保留图像高频细节区域的令牌，验证了 Update Index 与像素方差之间的显著 Spearman 秩相关（Figure 3b）。

**并行组解码。** 在 Infinity 上，仅使用 UIGTP 剪枝而不启用 PGD 时，加速比约为 2.03×；叠加 PGD 将连续四个尺度编为一组并行解码后，额外获得约 1.45× 的加速，且 GenEval Overall 几乎无变化（Table 7）。这证实了并行组解码所依赖的近似输入假设在大尺度下是高度可靠的。

**剪枝准则。** 将 Update Index 替换为 FastVAR 所采用的 PTS 准则（基于频率的剪枝）后，Infinity+LazyVAR 的 GenEval Overall 从 0.686 降至 0.665（Table 8）。该结果表明，基于余弦相似度的尺度级更新指标比频率域准则更能捕捉 VAR 模型在大尺度上的令牌更新模式，跨尺度更新一致性（Figure 3c）是其有效性的关键支撑。

### 失败模式与局限性

LazyVAR 的加速效果高度依赖于 VAR 模型在大尺度上的内部相似特性。对于相似性不足或架构差异较大的 VAR 变体，默认剪枝比例和分组策略可能需要重新调整，激进剪枝可能导致不可忽视的重建误差。此外，小尺度（尺度 1–8）必须完整保留以维持语义与结构的完整性，因此加速主要来源于大尺度阶段，对小尺度主导的模型加速空间有限。并行组解码在相邻尺度聚合特征相似性偏低时，近似输入可能引入额外的重建误差，这一问题在 HART 上已有所体现——其加速比（1.67×）显著低于 Infinity（2.94×）。

### 补充图表

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative comparison among the original models and FastVAR baseline and our LazyVAR on 1024×1024 image generation*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/014_Table_6.jpg]]
*Table 6: Ablation on Pruning ratio. † indicates the default setting*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/012_Table_7.jpg]]
*Table 7: Ablation on grouping strategy.† means the default setting*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/015_Table_8.jpg]]
*Table 8: Ablation on Pruning criterion.† means the default setting*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/013_Figure_6.jpg]]
*Figure 6: Visualization of pruned tokens under different ratios*

![[assets/figures/papers/paper_list_l892_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_LazyVAR_Accelerati/figures/004_Figure_3.jpg]]
*Figure 3: Investigation of the cosine similarity of aggregated latent features between adjacent scales in two families of VAR-based textto-image models, Infinity [22] and HART [55]. The text prompts are randomly sampled from a publicly available Midjourney v6 prompt dataset, with a total of 10,000 samples. In subfigure (b), Ours employs the cosine similarity of adjacent aggregated latent features as the pruning criterion, whereas PTS follows the approach proposed in FastVAR [21]*

## 方法谱系与知识库定位

### 与基线方法的关系

LazyVAR 面向的是视觉自回归（Visual Autoregressive, VAR）范式的文本到图像生成模型，其直接加速对象是两个代表性的 VAR 基线：**Infinity**（Han et al., arXiv 2024）和 **HART**（Tang et al., arXiv 2024）。Infinity 采用纯 VAR 架构进行文本到图像生成，HART 则在此基础上融合了离散与连续表示的混合生成策略。两者均遵循 VAR 的核心机制——以“下一尺度”替代“下一令牌”作为自回归预测目标，在多尺度令牌图上逐尺度串行解码。

LazyVAR 与上述基线的关系是**即插即用的无训练加速方法**：它不修改模型权重，也不改变模型架构，而是在推理阶段介入令牌参与策略和解码调度。具体而言，基线模型在所有尺度上均令全部令牌参与正向计算，且尺度间严格串行；LazyVAR 则在大尺度上依据 Update Index 选择性激活令牌，并对连续尺度编组实现并行解码。

在剪枝策略的谱系中，最直接的相关工作是 **FastVAR**（Guo et al., arXiv 2025）。FastVAR 同样针对 VAR 模型的令牌剪枝，但其剪枝准则基于频率域分析（PTS），与 LazyVAR 基于相邻尺度聚合潜特征余弦相似度的 Update Index 准则形成对比。消融实验（Table 8）表明，将 LazyVAR 的剪枝准则替换为 PTS 后，Infinity 在 GenEval 上的 Overall 得分从 0.686 降至 0.665，验证了 Update Index 作为剪枝准则的优越性。

### 方法谱系定位

从加速策略的维度，LazyVAR 可定位于以下两条技术路线的交汇处：

1. **令牌剪枝（Token Pruning）**：在 VAR 的多尺度令牌图上，利用尺度级更新指标识别并剪除更新微小的令牌。与 FastVAR 的频域剪枝不同，LazyVAR 的剪枝准则直接源自模型内部表征的相似性统计——相邻尺度聚合潜特征的余弦相似度在大尺度上右偏且峰值接近 1（Figure 2），约 94% 令牌的相似度超过 0.95，这为剪枝提供了可靠的信号基础。

2. **并行解码（Parallel Decoding）**：利用相邻尺度聚合潜特征高度相似的特性，将原本串行的多个连续尺度编为一组，以近似输入进行并行 Transformer 前向计算。该方法与推测解码（speculative decoding）类方法有精神上的相似性——均以近似换取并行性——但 LazyVAR 的近似直接来源于 VAR 自身的尺度间特征冗余，无需额外的草稿模型。

### 适用边界与局限

LazyVAR 的加速效果和适用性受以下边界条件约束：

- **尺度依赖性**：方法仅对较大尺度（Infinity 的尺度 10–13，HART 的尺度 12–13）进行剪枝和并行组解码。小尺度（如尺度 1–8）必须完整保留，否则会破坏生成图像的语义与结构完整性。这意味着加速主要来源于高分辨率尺度阶段，模型的总尺度数越多、大尺度占比越高，加速潜力越大。

- **模型相似性假设**：并行组解码的核心假设是组内各尺度的输入可由同一聚合特征近似（公式 (6)）。当实际相邻尺度间的聚合潜特征相似性偏低时，该近似会引入额外的重建误差。实验证据（Figure 2–3）在 Infinity 和 HART 上验证了高相似性的普遍存在，但对于设计显著不同的 VAR 变体，该假设需重新检验。

- **剪枝比例敏感性**：消融实验（Table 6）显示，默认剪枝比 [20%, 10%, 5%, 1%] 实现了 2.94× 加速且质量几乎无损；过度剪枝（如 [30%, 30%]）导致速度提升有限且质量下降。这表明剪枝比例需针对具体模型调优，不存在通用的最优配置。

- **硬件与精度约束**：所有实验在单块 RTX 4090 GPU 上完成，使用官方发布的模型权重，未进行额外训练或微调。方法的实际加速比可能因硬件特性（如内存带宽、并行计算能力）而异。

### 开放问题

基于已验证的分析，以下问题尚待进一步探索：

1. **跨模型泛化性**：Update Index 的统计特性（高相似度、右偏分布、与高频细节的秩相关）是否在更多 VAR 变体或自回归视觉生成模型中普遍成立？当前证据仅覆盖 Infinity 和 HART 两个模型族。

2. **自适应剪枝与分组策略**：当前剪枝比例和分组策略为人工设定，是否存在依据 Update Index 分布自适应确定剪枝阈值和组大小的方法？这直接影响方法在未知模型上的部署成本。

3. **与训练阶段加速的协同**：LazyVAR 是无训练的推理时加速方法，若与训练阶段的令牌压缩或高效注意力机制结合，是否存在协同增益或冲突？该方向尚未被探索。

4. **理论误差界**：并行组解码以近似输入替代真实输入，其引入的误差在多大程度上受尺度间相似度约束？当前缺乏对近似误差与生成质量退化之间的理论分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/LazyVAR_Accelerating_Visual_Autoregressive_Models_via_Scale_wise_Token_Pruning_and_Parallel_Group_Decoding.pdf]]

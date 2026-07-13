---
title: Pluggable Pruning with Contiguous Layer Distillation for Diffusion Transformers
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Pluggable_Pruning_with_Contiguous_Layer_Distillation_for_Diffusion_Transformers.pdf
project_link: null
code_link: "https://github.com/OPPO-Mente-Lab/Qwen-Image-Pruning"
huggingface_link: "https://huggingface.co/lodestones/Chroma1-HD"
aliases:
- PPPCLD
- PPCLDDT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过线性探针建模层的可替代性，并结合中心核对齐 (CKA) 相似度的一阶差分趋势分析，自动识别具有深度连续性的冗余层区间。利用非顺序教师-学生蒸馏方案，在单一训练阶段完成深度与宽度剪枝，避免误差累积，实现按需激活层的可插拔推理。
primary_logic: MMDiT 中的层冗余呈深度方向的连续性，连续移除层带来的性能退化远小于非连续移除。线性探针可有效近似层的输入‑输出映射，其叠加满足线性，从而高效检测连续可替代层。非顺序蒸馏打破错误传播链，使各剪枝模块独立优化，并支持推理时动态调整剪枝率。
claims:
- 连续移除层的生成质量始终优于非连续移除 (Figure 2)。
- 线性探针经过最小二乘初始化与对齐损失训练，可准确逼近教师层功能 (Eq.1, Eq.2)。
- 非顺序蒸馏方案将学生层输入直接设为教师前一深度输出，阻断了误差传播 (Section 3.3)。
- PPCL 在 Qwen-Image 上将参数减半，关键目标指标退化低于 3% (Abstract)。
---

# Pluggable Pruning with Contiguous Layer Distillation for Diffusion Transformers

> [!tip] 核心洞察
> MMDiT 中的层冗余呈深度方向的连续性，连续移除层带来的性能退化远小于非连续移除。线性探针可有效近似层的输入‑输出映射，其叠加满足线性，从而高效检测连续可替代层。非顺序蒸馏打破错误传播链，使各剪枝模块独立优化，并支持推理时动态调整剪枝率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用连续层蒸馏的可插拔剪枝方法用于扩散Transformer |
| 英文题名 | Pluggable Pruning with Contiguous Layer Distillation for Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16156) · [Code](https://github.com/OPPO-Mente-Lab/Qwen-Image-Pruning) · [HuggingFace](https://huggingface.co/lodestones/Chroma1-HD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PPCL (Pluggable Pruning with Contiguous Layer Distillation) |
| Dataset | Qwen-Image, FLUX.1-dev |

> [!tip] 效果简介
> - Qwen-Image 上，参数缩减 10B (减少50%) vs 20B (-50%)；DPG↑ 86.7 (PPCL 10B Finetune) vs 88.9 (-2.2)。
> - FLUX.1-dev 上，DPG↑ 80.0 (PPCL 8B) vs 83.8 (-3.8)。
> - FLUX.1-dev (8B模型) 上，平均性能退化 R(%)↓ 4.03 vs 0 (基模型) (+4.03)。

## 概要

扩散Transformer (Diffusion Transformer, DiT) 已成为文生图领域的主流架构，但其数十亿参数量带来的高昂计算成本，严重制约了在资源受限场景下的部署。现有结构化剪枝方法面临三重困境：**缺乏对多模态 DiT (MMDiT) 的通用性**、**无法灵活配置可插拔的剪枝率**、以及**对深层模型中层间依赖关系的理解不足**，导致剪枝后生成质量显著退化。

本文提出 **PPCL (Pluggable Pruning with Contiguous Layer Distillation)**，一种面向扩散Transformer的可插拔剪枝框架。其核心发现是：**MMDiT 中的层冗余呈深度方向的连续性**——连续移除若干相邻层带来的性能退化远小于非连续移除 (Figure 2)。基于此洞察，PPCL 通过**线性探针建模层的可替代性**，结合**中心核对齐 (CKA) 相似度的一阶差分趋势分析**，自动识别具有深度连续性的冗余层区间；进而采用**非顺序教师-学生蒸馏方案**，在单一训练阶段内完成深度与宽度剪枝，避免传统顺序蒸馏中的误差累积，实现推理时按需激活层的可插拔推理。

在 Qwen-Image 和 FLUX.1-dev 上的实验表明，PPCL 可将模型参数量削减至原始的 30%–50%，推理速度提升 1.3–1.8 倍，GPU 显存占用降低超过 30%。其中，在 Qwen-Image 上实现 50% 参数缩减时，关键目标指标退化低于 3%。该方法已开源，代码及模型权重可在 GitHub 和 Hugging Face 获取。

扩散模型已成为视觉内容生成的核心技术。近年来，扩散Transformer（Diffusion Transformer, DiT）凭借其卓越的生成质量，逐步取代U-Net成为主流骨干架构，并被广泛应用于多模态生成任务（MMDiT）。然而，这类模型参数量通常高达数十亿级别——例如Qwen-Image拥有约20B参数，FLUX.1-dev约12B参数——导致极高的推理延迟与显存占用，严重制约了其在资源受限场景下的部署可行性。

**现有剪枝方法的缺口**。模型压缩领域已有大量工作聚焦于CNN和U-Net架构，但针对MMDiT的结构化剪枝仍处于早期阶段。当前方法面临三个关键瓶颈：

1. **通用性不足**。多数剪枝方案针对特定架构设计，难以无缝迁移至双流（文本流/图像流）交互的MMDiT结构。
2. **配置僵化**。剪枝后模型参数固定，缺乏“可插拔”（plug-and-play）的灵活配置能力，无法根据部署场景动态调整剪枝率。
3. **层间依赖建模薄弱**。深层DiT中层与层之间的冗余关系未被充分理解。如Figure 2所示，随机移除单层对生成质量影响甚微，表明存在显著的层冗余——但并非所有层可被等量齐观地移除。连续移除层的性能退化远小于非连续移除（Figure 2, Figure 4），说明冗余具有深度方向上的连续性特征，而现有方法未能有效捕捉这一规律。

**核心动机**。本文旨在回答一个根本问题：*能否在单一训练阶段内，自动识别连续冗余层区间，并完成深度与宽度两个维度的剪枝，同时保持推理时可动态调整剪枝率的灵活部署能力？* 这一目标要求同时解决冗余检测的自动化、蒸馏过程的误差隔离，以及剪枝后模型的可插拔推理三个相互耦合的技术挑战。

## 核心方法与创新机理

PPCL 的核心创新在于对多模态扩散 Transformer (MMDiT) 层冗余模式的重新审视，以及一套与之深度耦合的“检测‑蒸馏”协同剪枝框架。其关键创新点可归纳为三个相互关联的 changed slots。

### 1. 冗余区间检测：从孤立敏感度到连续可替代性建模

传统剪枝方法通常基于逐层敏感度分析或启发式阈值来移除“不重要”的层，忽略了 MMDiT 深层模型中广泛存在的**深度方向连续性冗余**。PPCL 的核心洞察是：连续移除层带来的性能退化远小于非连续移除（Figure 2），这意味着冗余不是孤立的，而是以“连续区间”的形式存在。

为自动识别此类区间，PPCL 引入了**线性探针 + CKA 一阶差分分析**的检测机制：
- **线性探针训练**：为教师模型的每个 MMDiT 块训练一个线性探针，以最小二乘闭式解初始化权重（Eq.1），并通过对齐损失（Eq.2）逼近该层的输入‑输出映射。线性探针的可叠加性使得后续的连续层替代模拟成为可能。
- **CKA 一阶差分趋势分析**：在模拟剪枝阶段，计算原始教师层与线性探针叠加替代模型输出之间的 CKA 相似度（Eq.3），并追踪其一阶差分 $\Delta(u,k)$（Eq.4）。当 $\Delta(u,k)$ 由持续下降转为上升时，标记冗余区间的终点 $v$（Eq.5）。这一机制将冗余检测从“该不该剪某一层”转化为“连续几层能否被一个紧凑替代体所覆盖”的可替代性判断。

该方法相对基线的本质变化在于：**检测对象从单层重要性转变为层间连续可替代性**，从而在机制层面保证了剪枝后的结构一致性。

### 2. 蒸馏机制：从顺序误差累积到非顺序误差隔离

现有知识蒸馏方法通常采用顺序方案——学生层依次接收前一学生层的输出作为输入，导致误差沿深度方向累积，深层学生被迫拟合已受干扰的中间表示。PPCL 提出了**非顺序层间蒸馏**：学生层直接接收教师模型前一深度的输出作为输入，而非依赖其他学生层的输出。

这一设计的关键因果效应是**打破错误传播链**：每个学生层独立优化，其输入始终来自未受剪枝干扰的教师表示。深度蒸馏损失（Eq.6）直接对齐学生输出与教师第 $v$ 层的 L2 归一化特征，强调方向一致性而非幅度匹配。这使得深度剪枝和宽度剪枝可以在单一训练阶段内交替进行，而不会因误差累积导致训练不稳定。

### 3. 宽度剪枝策略：从仅深度压缩到流级与 FFN 联合轻量化

在深度剪枝之外，PPCL 进一步挖掘了 MMDiT 内部的宽度冗余。CKA 热力图（Figure 5）揭示：文本流存在高度跨层相似性，而图像流呈平滑对角线衰减。基于此，PPCL 引入了**流级和 FFN 级的宽度剪枝**：
- **文本流替换**：对于冗余文本流层，保留 QKV 投影器，其余参数替换为两个轻量线性投影器 $l_p^z$ 和 $l_p^h$（Eq.8），输入来自前一层的中间表示和输出。
- **FFN 替换**：对图像流和文本流中的冗余 FFN 层，用线性投影器 $l_q^{img}$ 和 $l_q^{txt}$ 替代（Eq.9），输入为门控输出。

这种“保留注意力核心、替换线性映射”的策略，在压缩参数量的同时维持了跨模态交互的关键通路，相对无宽度剪枝或仅深度剪枝的基线实现了更极致的压缩效率。

### 创新协同与可插拔特性

上述三个 changed slots 并非孤立设计，而是形成了一条因果链路：**线性探针检测连续冗余区间 → 非顺序蒸馏在区间内独立优化 → 宽度剪枝进一步压缩区间内结构**。这一协同使得 PPCL 具备“可插拔”特性——推理时可根据资源约束动态调整激活的层数，无需重新训练。在 Qwen-Image 上，PPCL 将参数减半（20B → 10B），关键目标指标退化低于 3%；在 FLUX.1-dev 上，8B 变体的平均性能退化仅为 4.03%，显著优于同等压缩比下的对比方法（Table 1）。

PPCL 的整体流程由两个递进阶段构成：**深度剪枝 (Depth-wise Pruning)** 与**宽度剪枝 (Width-wise Pruning)**，二者在单一训练阶段内通过非顺序教师‑学生蒸馏方案有机衔接，最终输出一个可按需配置激活层数的可插拔压缩模型（Figure 3、Algorithm 1）。

![[assets/figures/papers/paper_list_l913_https_arxiv_org_abs_2511_16156/figures/003_Figure_3.jpg]]
*Figure 3: (a) Depth-wise pruning: Stage 1.1 performs linear probing training for each MMDiT block. Stage 1.2 simulates pruning training to assess the continuity between adjacent MMDiT blocks by tracking the first-order difference of CKA between each block outputs and its corresponding linear probe outputs. A decreasing first-order difference indicates a contiguous layer, while a sudden increase suggests a break. The length represents the value of the first-order difference. Stage 1.3 conducts feature distillation, with the inputs to the student model taken from the same contiguous layer unit. (b) Width-wise pruning: We prune both stream-level and FFN redundancy in MMDiT*

### 阶段一：深度剪枝

深度剪枝的目标是识别并压缩 MMDiT 中沿深度方向呈连续性的冗余层区间，其内部又细分为三个子步骤。

1. **线性探针训练 (Stage 1.1)**  
   为教师模型的每一个 MMDiT 块构建一个线性探针 $l_i$，通过最小化对齐损失 $\mathcal{L}_{fit}(i) = || l_i(T_{i-1}^D) + T_{i-1}^D - T_i(T_{i-1}^D) ||_2^2$ 来逼近该层的输入‑输出映射。探针权重 $W_i^*$ 首先由最小二乘闭式解初始化，再经梯度优化精调，使得探针能以极低的参数量复现教师层的功能。

2. **模拟剪枝与冗余区间检测 (Stage 1.2)**  
   利用训练好的线性探针构建替代模型，计算原始教师层 $u$ 与替代模型在第 $k$ 层输出之间的 CKA 相似度 $\text{cka}(u,k)$，并追踪其一阶差分 $\Delta(u,k) = -(\text{cka}(u,k) - \text{cka}(u,k-1))$。当 $\Delta(u,k)$ 由降转升时，即满足 $v = \min \{ k-1 \mid \Delta(u,k) > \Delta(u,k-1) \}$，标记出冗余连续层区间的终点 $v$，从而自动划定可安全移除的层范围 $[u, v]$。

3. **非顺序特征蒸馏 (Stage 1.3)**  
   对每个冗余区间 $[u,v]$，将学生层的输入直接设为教师模型第 $u-1$ 层的输出，而非学生自身前一层的输出，从而彻底阻断顺序蒸馏中固有的误差累积链。蒸馏损失 $\mathcal{L}_{depth}^{[u,v]} = \| \mathrm{Norm}(S_{init}^u(T_{u-1}^D)) - \mathrm{Norm}(T_v^D) \|_2^2$ 对师生输出做 L2 归一化后计算均方误差，强调方向对齐而非幅值匹配。

### 阶段二：宽度剪枝

在完成深度剪枝后，PPCL 进一步压缩 MMDiT 内部的流级与 FFN 级冗余。

- **文本流压缩**：对于第 $p$ 层，保留 QKV 投影器，将其余文本流参数替换为两个轻量线性投影器 $l_p^z$ 和 $l_p^h$，分别接收前一层文本流的中间表示 $z_r^{txt}$ 和输出 $h_r^{txt}$ 作为输入。
- **FFN 压缩**：对第 $q$ 层的图像流和文本流中的 FFN，用线性投影器 $l_q^{img}$、$l_q^{txt}$ 替换，输入为对应的门控输出 $g_q^{img}$、$g_q^{txt}$。

宽度剪枝同样通过线性对齐损失进行蒸馏，使被替换模块的输出逼近教师对应层的表示。

### 训练与推理特性

深度剪枝与宽度剪枝共享同一教师模型，在 6k 步深度蒸馏后接续 2k 步宽度蒸馏（8 张 H20 GPU，microbatch=2），最后辅以 1k 步全参数微调恢复性能。由于非顺序蒸馏使每个剪枝模块独立优化，推理时可根据资源约束灵活增减激活层数，无需重新训练，实现了真正的“可插拔”部署。

### 整体框架：两阶段剪枝流水线

PPCL 的整体框架由两个阶段构成：**深度剪枝**与**宽度剪枝**，二者在单一训练阶段内通过非顺序教师-学生蒸馏方案交替执行。整体流程如 Figure 3 和 Algorithm 1 所示。

**深度剪枝**包含三个子阶段：
1.  **Stage 1.1 线性探针训练**：为教师模型的每个 MMDiT 块训练一个线性探针，逼近该层的输入-输出映射。
2.  **Stage 1.2 模拟剪枝过程**：通过追踪 CKA 相似度的一阶差分，评估相邻 MMDiT 块输出的连续性，识别冗余的连续层区间。
3.  **Stage 1.3 特征蒸馏**：对每个冗余区间进行非顺序特征蒸馏，学生模型的输入直接取自同一连续层单元中教师的前一深度输出。

**宽度剪枝**在深度剪枝完成后进行，针对 MMDiT 中的流级冗余和 FFN 冗余进行压缩。

---

### 深度剪枝：冗余区间检测与蒸馏

#### 线性探针训练

为检测层间的可替代性，PPCL 为教师模型的每一层 $i$ 构建一个线性探针 $l_i$。探针采用最小二乘闭式解进行最优初始化，使其输出逼近教师层输出。

**线性探针最优初始化** (Eq.1)：
$$W_i^* = (T_i(T_{i-1}^D) - T_{i-1}^D)(T_{i-1}^D)^\top (T_{i-1}^D (T_{i-1}^D)^\top)^{-1}$$

其中 $T_{i-1}^D$ 为教师第 $i-1$ 层在数据集 $D$ 上的输出，$T_i(\cdot)$ 为教师第 $i$ 层的映射函数。该公式通过最小化重构误差给出探针权重 $W_i^*$ 的闭式解。

**线性探针对齐损失** (Eq.2)：
$$\mathcal{L}_{fit}(i) = || l_i(T_{i-1}^D) + T_{i-1}^D - T_i(T_{i-1}^D) ||_2^2$$

该损失函数在训练中最小化带残差结构的探针输出与教师层输出之间的 L2 距离，确保探针能准确逼近教师层的功能。

#### 冗余区间检测

训练完成后，PPCL 通过模拟剪枝来评估层间连续性。对于任意起始层 $u$ 和终止层 $k$，计算替代模型输出与原始教师层输出之间的 CKA 相似度：

**CKA 相似度** (Eq.3)：
$$cka(u,k) = CKA(T_u(T_{u-1}^X), T_{u:k}^{[u k]}(T_{u-1}^X))$$

其中 $T_{u:k}^{[u k]}$ 表示用线性探针替代层 $u$ 到 $k$ 后的替代模型。

**CKA 一阶差分** (Eq.4)：
$$\Delta(u,k) = -(cka(u,k) - cka(u,k-1))$$

$\Delta(u,k)$ 衡量 CKA 相似度沿层索引的变化率：差分持续下降表明当前层与前一层的表示高度连续，即存在冗余；差分由降转升则表明连续性中断。

**冗余区间终点** (Eq.5)：
$$v = \min \{ k-1 \in [u+2, M] \mid \Delta(u,k) > \Delta(u,k-1) \}$$

当 CKA 一阶差分首次由降转升时，标记冗余连续层区间的终点 $v$，从而自动确定一个完整的冗余区间 $[u, v]$。

#### 非顺序深度蒸馏

对每个检测到的冗余区间 $[u, v]$，PPCL 执行非顺序特征蒸馏。与传统顺序蒸馏不同，学生层直接接收教师前一深度（即区间起点前一层）的输出作为输入，从而阻断误差传播链。

**深度蒸馏损失** (Eq.6)：
$$\mathcal{L}_{depth}^{[u,v]} = \| \mathrm{Norm}(S_{init}^u(T_{u-1}^D)) - \mathrm{Norm}(T_v^D) \|_2^2$$

其中 $S_{init}^u$ 为区间 $[u, v]$ 的初始学生模型，$T_v^D$ 为教师第 $v$ 层的输出。$\mathrm{Norm}(\cdot)$ 表示沿特征维度的 L2 归一化，强调方向对齐而非幅度匹配，以缓解分布偏移。

所有 $n$ 个冗余区间的总深度蒸馏损失为：
$$\mathcal{L}_{depth} = \sum_{i=1}^{n} \mathcal{L}_{depth}^{[u_i, v_i]}$$

---

### 宽度剪枝：流级与 FFN 压缩

宽度剪枝针对 MMDiT 中两类冗余：文本流的流级冗余和前馈网络的 FFN 冗余。核心策略是用紧凑的线性投影器替换冗余组件。

**文本流线性投影** (Eq.8)：
$$z_p^{txt} = l_p^z(z_r^{txt}), \quad h_p^{txt} = l_p^h(h_r^{txt})$$

对于第 $p$ 层（$p \in R_{txt}$，即文本流冗余层集合），除 QKV 投影器外的所有文本流参数被两个轻量线性投影器 $l_p^z$ 和 $l_p^h$ 替换。输入 $z_r^{txt}$ 和 $h_r^{txt}$ 分别来自前一层文本流的中间表示和最终输出。

**FFN 线性投影** (Eq.9)：
$$h_q^{img} = l_q^{img}(g_q^{img}), \quad h_q^{txt} = l_q^{txt}(g_q^{txt})$$

对于第 $q$ 层（$q \in R_{ffn}$，即 FFN 冗余层集合），图像流和文本流中的 FFN 被线性投影器替换。输入 $g_q^{img}$ 和 $g_q^{txt}$ 分别为对应流中门控机制的输出。

宽度蒸馏损失与深度蒸馏类似，采用 L2 归一化后的均方误差对齐学生输出与教师对应层输出：
$$\mathcal{L}_{width}^{j} = \| \mathrm{Norm}(S_{width}^{j}(T_{j-1}^D)) - \mathrm{Norm}(T_j^D) \|_2^2$$

---

### 关键设计机理

**线性探针的可叠加性**是冗余区间检测的理论基础。由于线性映射的复合仍为线性，多个连续线性探针的叠加可以等价地表示为单个线性变换，这使得探针能够有效模拟连续层的联合映射，从而评估层间可替代性。

**非顺序蒸馏的误差隔离**是深度剪枝质量保障的核心。传统顺序蒸馏中，前一学生层的误差会传播至后续层，导致误差累积。PPCL 将学生层输入直接锚定在教师对应深度的输出上，使各剪枝模块独立优化，推理时可按需激活不同层数，实现真正的可插拔推理。

**CKA 一阶差分**作为冗余区间边界的检测器，其物理含义是：当相邻层表示高度相似时，CKA 值缓慢下降，差分为负且递减；当遇到功能突变层时，相似度骤降，差分由负转正，形成局部极小值点，即为区间终点。这一启发式方法在 Qwen-Image 和 FLUX.1-dev 上均表现出稳定的区间划分能力，但缺乏严格理论支撑，在不同架构上需验证其泛化性。

### 补充图表

![[assets/figures/papers/paper_list_l913_https_arxiv_org_abs_2511_16156/figures/004_Figure_4.jpg]]
*Figure 4: Subjective comparison of complex text rendering in Qwen-Image when randomly removing contiguous and non-contiguous blocks. Columns 1 and 3 show the results for contiguous layer removal, while columns 2 and 4 correspond to non-contiguous layer removal*

## 实验与关键发现

### 核心发现：连续层冗余是 DiT 剪枝的关键杠杆

PPCL 的设计根植于一项关键观察：在多模态扩散 Transformer (MMDiT) 中，层的冗余呈现出显著的**深度连续性**。Figure 2 在 LongText-Bench 上的对比实验清晰地揭示了这一点——连续移除层 (contiguous removal) 的生成质量始终优于非连续移除 (non-contiguous removal)，而单层移除 (individual layer removal) 的影响则最为微弱。这一现象表明，MMDiT 中存在天然的“冗余区间”，连续跳过这些区间对模型功能的扰动远小于在模型中随机“打孔”。Figure 5 进一步从表示层面印证了这一规律：文本流 (text stream) 的 CKA 热力图展现出极高的跨层相似性，说明相邻层的文本流功能高度重叠；图像流 (image stream) 则呈现平滑的对角衰减，表示其沿深度方向的特征演化更为渐进，冗余度相对较低。这两项观察共同构成了 PPCL 方法论的实证基石——剪枝不应是孤立的层删除，而应是对连续冗余区间的结构性压缩。

### 主实验结果：参数减半，性能退化可控

Table 1 汇总了 PPCL 在 FLUX.1-dev 和 Qwen-Image 两个主流 MMDiT 模型上与现有剪枝方法的全面对比。在 **Qwen-Image** 上，PPCL 将参数量从 20B 压缩至 10B（减少 50%），关键目标指标退化低于 3%（DPG 从 88.9 降至 86.7），同时实现 1.3–1.8× 的推理加速和超过 30% 的 GPU 显存节省。在 **FLUX.1-dev** 上，PPCL 剪枝至 8B 参数时，平均性能退化 R(%) 仅为 4.03%，在所有 8B 参数级别的压缩方法中表现最优。值得注意的是，PPCL 的 14B 变体在 Qwen-Image 上的平均退化仅为 0.42%（DPG 87.9），几乎与原始 20B 模型持平，说明该方法在温和压缩比下几乎可以无损保留生成能力。

![[assets/figures/papers/paper_list_l913_https_arxiv_org_abs_2511_16156/figures/006_Table_1.jpg]]
*Table 1: A comprehensive comparison in terms of performance and efficiency. P., M., L. and R. denote model parameter count (Billion), GPU memory usage, inference latency (milliseconds), and average performance drop, respectively*

与基线方法的对比凸显了 PPCL 的优势。在相同剪枝比例（FLUX.1 33%，Qwen-Image 30%）和相同训练条件下，**TinyFusion** 和 **HierarchicalPrune** 的剪枝后模型性能退化更为明显。Figure 6 的主观对比直观地展示了这一差距：PPCL 剪枝至 10B 的生成结果在色彩还原、细节纹理和面部特征合成上均优于 TinyFusion 和 HierarchicalPrune 的 14B 剪枝变体。对于已开源的压缩变体 **FLUX.1 Lite** 和 **Chroma1-HD**，PPCL 在可比参数量下同样展现出更低的性能退化。

![[assets/figures/papers/paper_list_l913_https_arxiv_org_abs_2511_16156/figures/007_Figure_6.jpg]]
*Figure 6: A subjective comparison result: The first row shows the teacher model. The second and third rows display the 14B pruned HierarchicalPrune and TinyFusion models, respectively. The last row illustrates the effect of our method pruned to 10B*

### 消融实验：线性探针、非顺序蒸馏与宽度剪枝的递进贡献

Table 2 通过逐步叠加各模块，量化了 PPCL 各组件的独立贡献。实验以原始 Qwen-Image (60 层，平均分 0.893) 为基线：

![[assets/figures/papers/paper_list_l913_https_arxiv_org_abs_2511_16156/figures/008_Table_2.jpg]]
*Table 2: Ablation studies of linear probing, depth-wise pruning and width-wise pruning. The Original denotes the original Qwen-Image (60 layers). Each subsequent row adds a specific component to the configuration of the preceding row. To compute the average, we scale the DPG scores by a factor of 0.01*

1. **线性探针 (LP) + 一阶差分检测**：相比简单的 CKA 阈值法和固定区间法，LP 结合一阶差分能更准确地识别冗余区间，为后续剪枝奠定基础。
2. **非顺序深度蒸馏 (DP)**：引入 DP 后，平均分从 0.761 跃升至 0.848，提升幅度达 8.7 个百分点。这一显著增益验证了非顺序蒸馏方案在阻断误差传播方面的关键作用——学生层直接接收教师前一深度输出，避免了顺序蒸馏中逐层累积的分布偏移。
3. **宽度剪枝 (WP)**：在深度剪枝的基础上，对文本流和 FFN 进行线性投影替换，平均分进一步提升至 0.870，与原始模型仅差 2.61%。这表明 MMDiT 中不仅存在深度冗余，文本流和 FFN 内部也存在可被轻量线性投影器有效替代的宽度冗余。

### 失败模式与局限性

尽管 PPCL 在整体指标上表现优异，但在特定场景下仍存在退化。Figure 13 展示的失败案例主要集中在两类场景：(1) **极长文本渲染**——当提示词包含超长字符串时，剪枝后模型的文本可读性和结构完整性下降；(2) **小尺寸文字生成**——在复杂低分辨率区域中，文字细节的清晰度和准确性不足。这些失败模式与剪枝导致的模型容量下降直接相关，说明文本渲染能力对参数量的敏感度高于整体图像质量。

![[assets/figures/papers/paper_list_l913_https_arxiv_org_abs_2511_16156/figures/024_Figure_13.jpg]]
*Figure 13: Some failure cases*

此外，论文明确指出两项技术局限：(1) 基于 CKA 一阶差分的冗余区间检测缺乏严格理论支撑，仅作为经验启发式方法，在不同架构和数据集上的稳定性有待验证；(2) 剪枝后应用 INT4 量化会导致显著的性能下降，因为剪枝缩小了参数分布范围，使得粗粒度量化难以捕捉精细的参数结构。这两点构成了 PPCL 在更极致压缩场景下的应用边界。

## 定位与知识库关联

### 剪枝方法谱系中的位置

PPCL 处于**结构化剪枝**与**知识蒸馏**的交叉地带，其设计直接回应了现有扩散 Transformer 压缩方法的三个核心缺口。

**与剪枝基线的对比。** 在 FLUX.1-dev 和 Qwen-Image 上，PPCL 与 **TinyFusion**、**HierarchicalPrune** 和 **Dense2MoE** 进行了系统比较。TinyFusion 和 HierarchicalPrune 代表传统的结构化剪枝范式——前者依赖敏感度分析或启发式阈值选择移除层，后者采用层级化剪枝策略；Dense2MoE 则将密集层替换为混合专家结构以实现稀疏化。这些方法的共同局限在于：它们缺乏对 MMDiT 双流架构中层间依赖关系的显式建模，且剪枝配置固定，无法在推理时动态调整。PPCL 的差异化优势体现在三个层面：

1. **冗余检测机制**：用线性探针训练 + CKA 一阶差分分析替代手工设计的层重要性度量，自动识别具有深度连续性的冗余区间。
2. **蒸馏范式**：用非顺序层间蒸馏替代顺序知识蒸馏，阻断了学生层之间的误差传播链。
3. **可插拔性**：剪枝后的模型支持推理时按需激活不同数量的层，这是前述基线均不具备的能力。

在公平性方面，所有对比方法在相同数据集、训练步数和硬件环境下复现，剪枝比例设置一致（FLUX.1 为 33%，Qwen-Image 为 30%）。对于已开源的压缩变体 **FLUX.1 Lite** 和 **Chroma1-HD**，直接引用官方结果；无官方模型的基线则按论文描述重新实现。实验表明，在 FLUX.1-dev 上剪枝至 8B 参数时，PPCL 的平均性能退化仅为 4.03%，显著低于同类方法。

**与压缩变体的关系。** FLUX.1 Lite 和 Chroma1-HD 是社区中对 FLUX.1 模型进行压缩的尝试，但它们并非通用剪枝框架——前者是特定模型的轻量化变体，后者的压缩策略和训练细节未完全公开。PPCL 的定位是**通用可插拔剪枝方案**，在 Qwen-Image 和 FLUX.1-dev 两个架构迥异的 MMDiT 模型上均验证了有效性，且提供完整的训练代码和检查点。

### 适用边界

PPCL 的设计基于以下关键假设，这些假设划定了其适用边界：

1. **MMDiT 架构前提**。冗余区间检测依赖双流（文本流 + 图像流）的 CKA 相似度分析。Figure 5 的热力图揭示了文本流高度冗余、图像流平滑衰减的规律——这一规律是线性探针 + 一阶差分方法有效性的经验基础。对于单流 DiT 或非 Transformer 的扩散骨干网络，该检测机制的有效性需要重新验证。

2. **连续冗余假设**。PPCL 的核心洞察——连续移除层的性能退化远小于非连续移除（Figure 2, Figure 4）——是在 Qwen-Image 和 FLUX.1 上观察到的经验规律。若目标模型的层间依赖呈非连续模式（例如某些层承担不可替代的特定功能），连续剪枝策略可能失效。

3. **蒸馏数据依赖**。非顺序蒸馏需要教师模型的前向传播作为监督信号，这意味着剪枝过程依赖完整的教师模型和训练数据集。在教师模型不可用或数据受限的场景下，PPCL 无法直接应用。

4. **压缩比上限**。论文验证了 30%–50% 的参数削减（Qwen-Image 从 20B 到 10B，FLUX.1 从 12B 到 8B）。在更极端的压缩比（如 80% 参数削减）下，非顺序蒸馏的误差隔离优势是否依然成立，目前缺乏实验证据。

### 局限与开放问题

**已识别的局限。**

- **冗余检测缺乏理论保证。** 基于 CKA 一阶差分的冗余区间检测仅作为经验启发式方法，其数学性质（如差分阈值的统计显著性、区间边界的置信度）未得到严格分析。在不同架构和数据集上，该方法的稳定性需要更多验证。
- **量化不兼容。** 剪枝后应用 INT4 量化会导致显著的性能下降。原因是剪枝缩小了参数分布范围，使得粗粒度的 16 级量化难以捕捉精细的参数结构。这一发现暗示剪枝与量化的联合优化需要专门设计，而非简单串行。
- **细粒度文本渲染退化。** 剪枝模型在渲染极长文本或小尺寸文字时，可读性和结构完整性下降（Figure 13）。复杂低分辨率区域中的文本细节生成仍然是薄弱环节，这可能与文本流剪枝策略有关——线性投影器虽然高效，但可能丢失了原始注意力机制中的细粒度跨模态对齐能力。

**开放问题。**

1. 能否为冗余区间的自动检测建立严格的理论基础？例如，将 CKA 一阶差分与信息瓶颈理论或神经切线核关联，使其对不同 DiT 架构的适用性具有可预测的边界。
2. 如何设计自适应的混合精度量化策略，在剪枝后恢复 INT4 量化的性能？这需要在剪枝阶段就考虑量化约束，而非事后补救。
3. 非顺序蒸馏方案在更极端的压缩比下是否依然保持误差隔离的优势？当学生层数大幅减少时，教师“前一深度输出”与学生当前层之间的语义鸿沟可能增大，需要新的对齐机制。
4. PPCL 的可插拔特性是否可以扩展到其他生成任务中的扩散 Transformer？视频生成和 3D 生成中的时序/空间维度可能引入新的冗余模式，连续层蒸馏的范式需要相应的适配。

需要注意的是，论文中提及的基线方法（TinyFusion、HierarchicalPrune、Dense2MoE）在提供的材料中未附带完整的作者/会议/年份元数据，建议读者在引用时手动核实原始文献的出版信息。

## 原文 PDF

![[paperPDFs/CVPR_2026/Pluggable_Pruning_with_Contiguous_Layer_Distillation_for_Diffusion_Transformers.pdf]]

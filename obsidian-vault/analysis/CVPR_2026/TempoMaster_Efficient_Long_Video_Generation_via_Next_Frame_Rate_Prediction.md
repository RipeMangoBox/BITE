---
title: "TempoMaster: Efficient Long Video Generation via Next-Frame-Rate Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TempoMaster_Efficient_Long_Video_Generation_via_Next_Frame_Rate_Prediction.pdf
project_link: "https://scottykma.github.io/tempomaster-gitpage/"
code_link: null
aliases:
- TempoMaster
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 解耦高层次时间语义（全局动态结构）与低层次视觉细节（局部运动与纹理），通过下一帧率预测范式，只在最低帧率上进行一次全局规划，后续阶段以已生成帧为锚点并行填充中间帧。
primary_logic: 视频中大量存在时间冗余，因此全局连贯的动态结构仅需稀疏的关键帧即可建立，剩余中间帧可在已知全局动态和上下文依赖的条件下高效推断。这一去耦同时实现了长程一致性与并行生成能力。
claims:
- TempoMaster通过在低帧率双向前向建立全局结构，再逐步提升帧率细化局部细节，以此整合双向建模的全局规划能力与自回归的递进生成优势。
- 并行推理通过多路树实现，同级节点间无因果依赖，可切分为多段并行生成，显著降低计算复杂度。
- 在长视频（500帧）和短视频（121帧）的Vbench评估中总得分均达到最高，证明了方法的有效性。
- Vbench (500 frames, 480p) 上 Total Score = 80.30
---

# TempoMaster: Efficient Long Video Generation via Next-Frame-Rate Prediction

> [!tip] 核心洞察
> 视频中大量存在时间冗余，因此全局连贯的动态结构仅需稀疏的关键帧即可建立，剩余中间帧可在已知全局动态和上下文依赖的条件下高效推断。这一去耦同时实现了长程一致性与并行生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | TempoMaster：基于下一帧率预测的高效长视频生成 |
| 英文题名 | TempoMaster: Efficient Long Video Generation via Next-Frame-Rate Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.12578) · [Project](https://scottykma.github.io/tempomaster-gitpage/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | TempoMaster |
| Dataset | Vbench, Human study |

> [!tip] 效果简介
> - Vbench (500 frames, 480p) 上，Total Score 80.30 vs 79.52 (FramePack, 13B) (+0.78)。
> - Vbench (121 frames, 480p) 上，Total Score 80.76 vs 80.55 (MMPL, 14B) (+0.21)。
> - Human study (500 frames, 480p) 上，Overall mean score (1-5) 3.69 vs 3.47 (SkyReels-V2) (+0.22)。

## 概要

长视频生成长期受困于一对根本矛盾：**长期时间一致性的维护**与**计算成本的可控性**。全序列双向注意力虽然能全局建模时空结构，但计算复杂度随帧数平方增长；自回归逐帧预测虽可控制单步开销，却因历史帧累积与误差传播导致外观漂移与运动不一致。TempoMaster 将这一困境的突破口定位于视频中普遍存在的**时间冗余**——全局连贯的动态结构仅需稀疏的关键帧即可建立，剩余中间帧可在已知全局动态和上下文依赖的条件下高效推断。

基于此洞察，TempoMaster 提出**下一帧率预测**（next-frame-rate prediction）范式：先在最低帧率上通过双向建模生成全局动态蓝图，随后以已生成帧为锚点，逐步提升帧率并行填充中间帧。这一范式将高层次时间语义（全局结构）与低层次视觉细节（局部运动与纹理）解耦，同时继承了双向建模的全局规划能力与自回归方法的递进生成优势，并在推理阶段通过**分层并行推理引擎**将整体计算复杂度从 $O(N^2)$ 降至 $O(N^2/4^K)$（$W \ge 2$ 时）。

在 Vbench 基准上，TempoMaster 在长视频（500 帧）和短视频（121 帧）的自动评估中均取得最高总分（80.30 与 80.76），分别超越 **FramePack**（Zhang and Agrawala, 2025）和 **MMPL**（Xiang et al., 2025）等同期先进模型。人类偏好研究进一步验证了其在语义对齐、审美质量与运动平滑度上的主观优势。

**方法谱系与知识库定位**：TempoMaster 属于视频扩散模型中的分层生成路线，其核心创新在于将帧率作为可控的时间抽象维度引入生成过程。与自回归长视频模型（如 **MAGI-1** / Teng et al., 2025；**SkyReels-V2** / Chen et al., 2025）不同，它不依赖逐帧历史条件；与全序列双向生成方法不同，它通过多帧率训练与分层并行推理实现了长序列的高效处理。其 Multi-Mask 条件注入机制以零参数方式统一处理文本、图像、多帧等异构条件，避免了适配器或上下文学习引入的额外开销。



### 长视频生成的核心瓶颈

长视频生成面临一对相互纠缠的根本性挑战：**长期时间一致性维护**与**计算成本的可控性**。这两个目标在现有范式下呈现尖锐的权衡关系。

**全序列双向建模**通过对完整视频序列施加双向注意力，能够在全局范围内建立连贯的语义结构和运动轨迹。然而，其计算复杂度随帧数 $N$ 呈 $O(N^2)$ 增长，内存需求同步膨胀，使得生成长达数百帧的视频在实践上不可行。

**自回归逐帧预测**将视频生成分解为条件下一帧预测的序列过程，在计算上更为可控。但这一范式存在两个深层缺陷：其一，历史帧的累积式条件依赖导致误差随生成步数逐步放大，引发外观漂移和运动不一致；其二，因果注意力结构使模型无法在生成早期帧时利用未来帧的全局信息，难以建立长程动态结构。

这种困境的本质在于：现有方法将高层次的全局语义规划与低层次的局部视觉细节耦合在同一个生成过程中，迫使模型在“全局一致性”与“计算可行性”之间做出妥协。

### 关键洞察：时间冗余的解耦机会

视频数据中存在大量时间冗余——相邻帧之间的视觉变化通常是平滑且可预测的。这一观察揭示了一个被现有方法忽视的机会：**全局连贯的动态结构仅需稀疏的关键帧即可建立**，而大量中间帧可以在已知全局动态和上下文依赖的条件下高效推断。

这意味着，长视频生成可以被重新组织为两个解耦的子任务：
1. **全局规划**：在极低帧率下建立整个视频的语义结构和运动蓝图；
2. **局部细化**：以全局蓝图为锚点，逐步填充中间帧以提升视觉细节和运动平滑度。

这一解耦策略同时回应了前述两个瓶颈：全局规划阶段因帧数极少而天然具有低计算复杂度；局部细化阶段则因已有全局锚点而无需处理长程依赖，且各片段间天然适合并行化。

### 现有方法的缺口

当前先进的长视频生成模型虽在各自范式内取得了显著进展，但均未从根本上实现上述解耦。**MAGI-1**（Teng et al., 2025, 24B）和**FramePack**（Zhang and Agrawala, 2025, 13B）延续自回归范式，受限于误差累积和因果结构；**SkyReels-V2**（Chen et al., 2025, 14B）和**MMPL**（Xiang et al., 2025, 14B）虽引入规划机制，但仍将规划与生成耦合在序列过程中，未能实现全局结构的独立建立与并行细化的分离。

### 本文动机

基于上述分析，本文提出 **TempoMaster**，核心动机在于：通过**下一帧率预测**（next-frame-rate prediction）范式，将长视频生成中高层次的全局动态结构与低层次的局部视觉细节彻底解耦。在最低帧率上以双向注意力一次性建立全局蓝图，随后以已生成帧为条件，逐级提升帧率并并行填充中间帧。这一设计在理论上同时继承了双向建模的全局规划能力与自回归方法的递进生成优势，同时通过层级并行化将计算复杂度从 $O(N^2)$ 降至 $O(N^2/4^K)$（$W \geq 2$ 时），为高效长视频生成提供了新的路径。



## 核心方法与创新机理

TempoMaster 的核心创新在于将长视频生成重新定义为**下一帧率预测**（next-frame-rate prediction）范式，通过解耦高层次时间语义与低层次视觉细节，从根本上突破了现有方法在长期一致性与计算效率之间的两难困境。

### 范式转换：从逐帧到逐帧率

传统自回归模型将视频似然分解为逐帧条件概率：

$$p(V) = \prod_{t=1}^{T} p(x_t | x_0, x_1, ..., x_{t-1})$$

这种顺序依赖导致历史帧累积误差，引发外观漂移和运动不一致。全序列双向生成虽能建立全局结构，但注意力计算复杂度随帧数平方增长，难以扩展至长视频。

TempoMaster 将似然重新公式化为帧率序列上的乘积：

$$p(V) = p(V^{K-1}) \prod_{i=0}^{K-2} p(V^i | V^{i+1}, V^{i+2}, ..., V^{K-2})$$

其核心直觉是：**视频中存在大量时间冗余，全局连贯的动态结构仅需稀疏的关键帧即可建立**。模型首先在最低帧率上通过双向注意力生成全局蓝图 $V^{K-1}$，随后以已生成帧为锚点，逐级预测更高帧率的中间帧序列。这一设计同时继承了双向建模的全局规划能力与自回归的递进生成优势（Figure 2）。

### 关键机制创新

**Multi-Mask 条件注入**取代了传统的适配器或上下文学习方法。任意数量的条件帧按时间位置零填充至目标视频长度，编码后的潜变量与噪声潜变量沿通道维拼接，并附加帧级掩码提供精确时间步信息。该方法无需引入额外参数，统一处理文本、图像、多帧等异构条件（Figure 4）。

**多帧率训练**通过调节旋转位置编码（RoPE）的时间索引间隔向模型注入帧率信息：

$$t_j = t_{\mathrm{start}} + j \cdot 2^i, \quad t_{\mathrm{start}} \sim \mathcal{U}[0, T_{max}]$$

训练时采用连续随机位置采样，增强时域外推能力。消融实验表明，随机化策略使 Vbench 总分从 80.00 提升至 80.19，且在各子指标上均稳定优于固定索引基线（Table 4）。

**分层并行推理**将生成过程组织为多路树结构。同级子节点间无因果依赖，可切分为多段并行生成，整体复杂度从 $O(N^2)$ 降至 $O(N^2/4^K)$（$W \geq 2$ 时）：

$$\frac{N^{2}}{4^{K}} \cdot \sum_{i=0}^{K-1} \left( \frac{4}{W^{2}} \right)^{i}$$

这一设计实现了指数级加速，同时保持生成质量对并行配置的鲁棒性（Table 3）。



TempoMaster 提出一种**下一帧率预测**（next‑frame‑rate prediction）范式，将长视频生成重新形式化为从粗粒度全局蓝图到细粒度局部细节的逐级细化过程。其整体 pipeline 由四个核心模块串联构成，形成“条件注入 → 多帧率扩散建模 → 时域位置编码 → 分层并行推理”的完整生成链路。

### 1. 范式转换：从逐帧自回归到逐帧率预测

传统自回归视频生成将视频似然分解为逐帧条件概率的乘积：

$$p(V) = \prod_{t=1}^{T} p(x_t | x_0, x_1, ..., x_{t-1})$$

这种方式面临历史帧累积导致的计算膨胀与误差传播问题。TempoMaster 将似然重新公式化为不同帧率序列的层次化条件概率：

$$p(V) = p(V^{K-1}) \prod_{i=0}^{K-2} p(V^i | V^{i+1}, V^{i+2}, ..., V^{K-2})$$

其中 $V^i$ 表示第 $i$ 级帧率的视频序列，$V^{K-1}$ 为最低帧率的全局蓝图。这一公式化将长程时间一致性的建立与局部运动细节的填充解耦——**全局动态结构仅在最低帧率上通过双向注意力一次性规划，后续阶段则以已生成帧为锚点并行推断中间帧**（Figure 2 直观对比了自回归、全序列双向建模与 TempoMaster 三种范式的差异）。

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/002_Figure_2.jpg]]
*Figure 2: Different video modeling paradigms. Autoregressive models generate frames sequentially under a causal structure. Bidirectional models generate the entire sequence at once by processing the full sequence directly. TempoMaster establishes the global structure via a low-frame-rate bidirectional pass, then progressively enhances local details via predicting the video at the next higher frame rate*

### 2. 条件注入：Multi‑Mask 机制

Multi‑Mask 是统一的跨模态条件注入模块。任意数量的条件帧（可来自文本、图像或多帧视频）按时间位置零填充至目标视频长度，经 VAE 编码为潜变量后，与噪声潜变量沿通道维拼接。同时，一个帧级二值掩码被附加到拼接张量上，为模型提供精确的时间步信息。该设计**无需额外适配器参数或上下文长度扩展**，即可灵活支持从单图到多帧、从连续片段到多镜头视频的多样化条件输入。

### 3. 多帧率扩散 Transformer（DiT）

生成主干为基于 Wan2.2 的 Mixture‑of‑Experts（MoE）扩散 Transformer。模型在固定上下文长度下，同时接受 6 fps、12 fps、24 fps 等多种帧率的视频进行去噪训练。两阶段训练策略确保模型先掌握单帧率下的条件生成能力，再学习跨帧率的下一帧率预测任务，统一使用流匹配损失：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, p_t(\mathbf{z}_0)} \left[ || \mathbf{v}_\theta(\mathbf{z}_t, t) - (\mathbf{z}_1 - \mathbf{z}_0) ||_2^2 \right]$$

### 4. 时域位置编码：帧率感知的 RoPE

帧率信息通过调节旋转位置嵌入（RoPE）的时间索引间隔注入模型。对于帧率 $V^i$ 的第 $j$ 帧，其时间位置索引定义为：

$$t_j = t_{\mathrm{start}} + j \cdot 2^i, \quad t_{\mathrm{start}} \sim \mathcal{U}[0, T_{max}]$$

间隔 $2^i$ 使得低帧率帧具有更大的时间跨度，高帧率帧则密集排布。训练时对 $t_{\mathrm{start}}$ 进行连续随机采样，增强了模型对未见时间位置的泛化能力（消融实验证实该策略使 Vbench 总分从 80.00 提升至 80.19）。

### 5. 分层并行推理引擎

推理过程被组织为一棵多路生成树（Figure 5）。从最低帧率的全局蓝图开始，每级节点将其父节点的帧序列切分为多个无因果依赖的片段，**同级子节点可完全并行生成**。这一设计将整体计算复杂度从传统全序列双向注意力的 $O(N^2)$ 降至：

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/005_Figure_5.jpg]]
*Figure 5: The inference process of TempoMaster. TempoMaster first generates videos with the lowest frame rate and the largest interval of temporal position indices. Within the same level, the generated frames can be partitioned into multiple segments to enable parallel generation, which proceeds hierarchically down to the leaf node level*

$$\frac{N^2}{4^K} \cdot \sum_{i=0}^{K-1} \left( \frac{4}{W^2} \right)^i$$

当并行度 $W \geq 2$ 时级数收敛，实现指数级加速。同时，该策略保留了每级内部的双向注意力，确保局部片段的生成质量不受并行切分的影响。

### 6. 端到端数据流

整体 pipeline 的数据流可概括为：**条件输入**（文本/图像/视频帧）→ Multi‑Mask 编码与噪声拼接 → 多帧率 DiT 在最低帧率上通过双向注意力生成全局蓝图 → 基于帧率感知 RoPE 逐级提升帧率，每级内并行生成中间帧 → 输出完整高帧率长视频。该流程在 500 帧 480p 的 Vbench 长视频基准上取得 80.30 总分，超越 **FramePack**（Zhang and Agrawala, 2025, 79.52）等同期方法，并在人类评估中以 3.69 的平均分优于 **SkyReels‑V2**（Chen et al., 2025, 3.47）。

### 补充图表

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/001_Figure_1.jpg]]
*Figure 1: TempoMaster first generates a video sequence at coarse and low frame rate to establish the global dynamics and semantic structure, and subsequently refines it by predicting frames at higher rates, thereby enhancing temporal smoothness and detail. This nextframe-rate prediction paradigm results in videos with improved motion quality and temporal consistency*



### 下一帧率预测范式

TempoMaster 将长视频生成重新公式化为**下一帧率预测**（next-frame-rate prediction），其核心思想是将视频的时间结构分解为不同帧率的层次化表示。设视频 $V$ 包含 $K$ 个帧率层级 $V^0, V^1, \dots, V^{K-1}$，其中 $V^{K-1}$ 为最低帧率（最粗糙的时间粒度），$V^0$ 为最高帧率（原始帧率）。传统自回归方法将视频似然分解为逐帧条件概率：

$$p(V) = \prod_{t=1}^{T} p(x_t | x_0, x_1, ..., x_{t-1})$$

TempoMaster 则摒弃了顺序历史条件依赖，转而将似然重新组织为帧率层级间的条件乘积：

$$p(V) = p(V^{K-1}) \prod_{i=0}^{K-2} p(V^i | V^{i+1}, V^{i+2}, ..., V^{K-2})$$

这一公式化的关键含义是：**先生成最低帧率的全局序列 $V^{K-1}$**，建立整个视频的粗粒度蓝图（全局动态结构与语义布局）；**随后以已生成的低帧率序列为条件，逐级预测更高帧率的中间帧**，逐步细化视觉细节与运动连续性。由于低帧率序列已捕获长程时间依赖，高帧率层级仅需在相邻关键帧之间进行局部推断，从而将长程一致性与局部细节解耦。

### Multi-Mask 条件注入模块

为统一处理文本、图像、多帧等异构条件输入，TempoMaster 设计了 **Multi-Mask 条件注入机制**。该模块的核心操作如下：

1. **零填充对齐**：将任意数量的条件帧保持其原始时间位置，其余位置以零填充，扩展至目标视频序列长度。
2. **潜变量拼接**：将填充后的条件序列编码为潜变量表示，与带噪声的视频潜变量沿**通道维度**拼接。
3. **帧级掩码**：附加一个帧级二值掩码，精确标记每个时间步是否为条件帧，为模型提供显式的时间位置信息。

该设计的优势在于：无需引入适配器（adapter）或增加上下文长度的上下文学习（in-context learning）等额外参数，即可灵活支持任意数量、任意时间位置的条件帧注入。训练时，Multi-Mask 机制进一步支持**多镜头视频训练**——通过随机丢弃选定镜头内的所有条件帧，迫使模型学习镜头间的自然过渡，增强长视频的镜头切换能力。

### 多帧率训练与时间位置编码

TempoMaster 在**固定上下文长度**的 Diffusion Transformer (DiT) 上进行多帧率联合训练。模型需要感知当前处理的帧率层级，这一信息通过**可调间隔的旋转位置嵌入（RoPE）**注入。

对于帧率层级 $V^i$ 中的第 $j$ 帧，其时间位置索引定义为：

$$t_j = t_{\mathrm{start}} + j \cdot 2^i, \quad t_{\mathrm{start}} \sim \mathcal{U}[0, T_{max}]$$

其中间隔 $2^i$ 随帧率层级变化：最低帧率 $V^{K-1}$ 的索引间隔最大（$2^{K-1}$），最高帧率 $V^0$ 的间隔为 $1$。训练时，起始位置 $t_{\mathrm{start}}$ 从连续均匀分布 $\mathcal{U}[0, T_{max}]$ 中随机采样，这一**连续随机位置编码增强**使模型在推理时能够泛化到训练中未见的时间位置，支持时域外推。

训练采用**两阶段范式**：
- **第一阶段**：在单一帧率上学习 Multi-Mask 条件注入，计算量为约 300 H100 GPU 天。
- **第二阶段**：在多帧率上学习下一帧率预测，计算量为约 1200 H100 GPU 天。

两阶段统一使用**流匹配损失**（Flow Matching Loss）：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, p_t(\mathbf{z}_0)} \left[ || \mathbf{v}_\theta(\mathbf{z}_t, t) - (\mathbf{z}_1 - \mathbf{z}_0) ||_2^2 \right]$$

该损失建模从干净潜变量 $\mathbf{z}_0$ 到高斯噪声 $\mathbf{z}_1$ 的直线路径，$\mathbf{v}_\theta$ 为模型预测的速度场。

### 分层并行推理引擎

推理阶段将生成过程组织为**多路生成树**，实现指数级加速。具体流程为：

1. **根节点生成**：以最低帧率 $V^{K-1}$ 生成全局蓝图序列，采用双向注意力，一次性建立长程动态结构。
2. **逐级细化**：将父节点序列按帧率翻倍分解为子节点，每个子节点负责填充父节点相邻帧之间的中间帧。
3. **级内并行**：同一层级的不同子节点之间**无因果依赖**，可将父节点帧序列切分为多段并行生成。

计算复杂度分析揭示了并行策略的加速效果。设视频总帧数为 $N$，帧率层级数为 $K$，每级并行段数为 $W$。仅考虑级间并行时，总计算复杂度为：

$$\sum_{i=0}^{K-1} W^{i} \cdot \left( \frac{N}{2^{K-i} \cdot W^{i}} \right)^{2} = \frac{N^{2}}{4^{K}} \cdot \sum_{i=0}^{K-1} \left( \frac{4}{W} \right)^{i}$$

当 $W \geq 4$ 时，级数和收敛为常数，整体复杂度降至 $O(N^2 / 4^K)$。进一步引入**级内并行**（将每段再切分为 $W$ 个子段并行生成）后，复杂度进一步降低为：

$$\frac{N^{2}}{4^{K}} \cdot \sum_{i=0}^{K-1} \left( \frac{4}{W^{2}} \right)^{i}$$

此时条件放松至 $W \geq 2$ 即可使级数收敛，实现更显著的加速。默认配置采用帧率列表 $f(6, 24)$ 与并行因子 $m(1, 4)$，在 Vbench 长视频评估中取得 80.30 总分，消融实验表明性能对并行配置鲁棒。

### 补充图表

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/003_Figure_3.jpg]]
*Figure 3: Multi-Frame-Rate Training. TempoMaster is trained on videos with varying frame rates, which are signaled to the model by scaling the interval of the temporal positional indices. As illustrated, training on a video at half the highest frame rate employs a positional index interval of 2*

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/004_Figure_4.jpg]]
*Figure 4: Multi-Mask Condition. Condition frames are zeropadded to the length of the full sequence; their latent representations and a frame-wise mask that provides precise timestep information are then concatenated with the noisy latents to guide generation*



## 实验与关键发现

### 主要量化结果

TempoMaster 在长视频与短视频两个基准上均取得最优总分。**Table 1** 展示了 Vbench 自动评估结果，所有视频统一为 480p 分辨率，长视频 500 帧、短视频 121 帧。

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/007_Table_1.jpg]]
*Table 1: Vbench evaluation results. We compare TempoMaster with state-of-the-art long video generation models of similar or larger size. Top: the evaluation results of long videos (500 frames). Bottom: the evaluation results of short videos (121 frames). Our method achieves the highest total score in both long and short video generation. Higher values are better for all dimensions*

在长视频（500 帧）设定下，TempoMaster 总得分 **80.30**，超越 13B 参数的 **FramePack**（Zhang and Agrawala, 2025）的 79.52，以及 24B 参数的 **MAGI-1**（Teng et al., 2025）等其他同类模型。在短视频（121 帧）设定下，TempoMaster 总得分 **80.76**，以微弱优势领先 14B 参数的 **MMPL**（Xiang et al., 2025）的 80.55。这一结果验证了下一帧率预测范式在长程一致性与局部细节质量上的双重优势：低帧率双向全局规划确保了语义结构的长期稳定，而逐级帧率提升则有效细化了运动平滑度和视觉细节。

值得注意的是，TempoMaster 在参数规模并不占优（与 13B~24B 的基线模型相比）的情况下取得了最优结果，表明其方法层面的效率优势而非单纯的规模扩展。

### 人类偏好研究

为进一步验证主观感知质量，论文进行了长视频（500 帧、480p）的人类偏好评估（**Table 2**），评分维度涵盖语义对齐、审美质量、运动平滑度和动态幅度，各维度 1-5 分，总分为平均。TempoMaster 获得 **3.69** 的总体平均分，超越 **SkyReels-V2**（Chen et al., 2025）的 3.47 及其他基线模型。其中 **LongCat**（LongCat Team, 2025）作为短视频生成模型仅用于审美质量和语义对齐的参照基准，其在运动平滑度上的劣势反映了短视频模型在长程时序一致性上的固有局限。

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/009_Table_2.jpg]]
*Table 2: Human study results on long videos. All videos are 500 frames in length and generated in 480p. Note that LongCat is a short-video generation model that can extend video clips with an overlap of only 13 frames. We employ it as a strong baseline for benchmarking aesthetic quality, semantic alignment, and motion quality. Each dimension is scored from 1 to 5 (with 1 representing the poorest quality and 5 the best), and the total score is computed as the average across all dimensions*

人类研究结果与自动评估趋势一致，表明 TempoMaster 在用户感知层面同样具备竞争优势，尤其在需要长期运动连贯性的场景下优势更为明显。

### 消融实验

#### 并行配置鲁棒性

**Table 3** 展示了不同并行配置下的 Vbench 得分与总计算量（PFLOPs）。默认配置 `f(6,24) m(1,4)` 在长视频取得 80.30 总分。实验表明，减少中间帧率阶段或降低并行段数对性能影响较小，但可显著降低计算开销。这一消融验证了分层并行推理策略的鲁棒性：同级节点间无因果依赖的特性使得并行切分不会破坏生成质量，同时实现指数级的计算复杂度降低（由 $O(N^2)$ 降至 $O(N^2/4^K)$，当 $W \geq 2$ 时）。

#### 随机时间位置索引

**Table 4** 对比了训练时采用固定时间位置索引与随机化索引的效果。随机化策略使 Vbench 总分从 **80.00** 提升至 **80.19**，且在各子指标上均稳定优于固定索引基线。这一提升源于随机起始点 $t_{\text{start}} \sim \mathcal{U}[0, T_{max}]$ 扩大了模型在推理时对时间位置的外推能力，使得模型在未见过的帧率组合下仍能保持稳定的生成质量。该消融直接验证了多帧率训练中连续位置编码设计的必要性。

### 定性分析

**Figure 6** 展示了 500 帧、480p 分辨率下的长视频生成实例，可见 TempoMaster 在保持全局语义结构一致性的同时，逐级细化了局部运动细节。**Figure 7** 进一步展示了超长视频压力测试：通过 5 秒重叠扩展方式，模型可生成超过 1500 帧的分钟级视频片段，证明下一帧率预测范式具备向超长时序扩展的潜力。

### 局限性讨论

论文未明确列出形式化的失败模式，但结合实验设置可推断以下潜在局限需要人工验证：

1. **首帧延迟（TTF）**：分层并行推理虽然降低了总计算量，但最低帧率的全局蓝图生成仍需完整序列的双向注意力，可能导致首次出帧延迟较高。不同并行配置下吞吐量与延迟的权衡关系尚缺乏详细报告。
2. **极端运动场景**：在快速运动或大幅度相机运动场景下，低帧率蓝图可能丢失关键动态信息，导致高帧率细化阶段出现运动模糊或伪影。
3. **超长视频泛化**：随机时间索引在 >1500 帧视频上的泛化效果尚未量化验证，多镜头视频的镜头间过渡质量也缺乏系统评估。

以上局限需结合具体应用场景进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/010_Table_3.jpg]]
*Table 3: Ablation on the parallel configs. Top: the evaluation results of long videos (500 frames). Bottom: the evaluation results of short videos (121 frames). We include total computational Flops for comparison. All videos maintain a resolution of 480p. Higher values are better for all dimensions*

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/011_Table_4.jpg]]
*Table 4: Ablation on randomized temporal position indices. We report Vbench metrics. All videos are 500 frames in length and maintain a resolution of 480p*

![[assets/figures/papers/paper_list_l939_https_arxiv_org_abs_2511_12578/figures/008_Figure_7.jpg]]
*Figure 7: Visualization of long-term generation stress test. Our method is capable of extending video clips with a window size comparable to autoregressive methods. Our method composes minute-long videos (exceeding 1500 frames) by extending 480 frames with 5-second overlaps*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

长视频生成面临两个相互纠缠的根本挑战：**长期时间一致性维护**与**计算成本高昂**。现有方法在这两个维度上存在不可兼得的困境：

- **全序列双向注意力模型**：虽然能直接建模全局依赖，但内存与计算量随帧数 $N$ 呈 $O(N^2)$ 增长，难以扩展到数百帧的长视频。
- **自回归逐帧预测模型**：通过因果结构将复杂度控制在可控范围，但历史帧的逐帧累积导致外观漂移和误差传播，运动连贯性随生成长度增加而显著退化。

这一矛盾构成了长视频生成领域的核心瓶颈：**如何在维持长期一致性的同时，避免计算成本的指数级膨胀？**

### 2. 方法谱系中的定位

TempoMaster 在现有长视频生成范式谱系中占据了一个独特位置——它既非纯双向，也非纯自回归，而是通过**下一帧率预测（Next-Frame-Rate Prediction）** 范式实现了两者的结构性融合。

| 范式 | 代表方法 | 核心机制 | 全局一致性 | 计算效率 |
|------|----------|----------|------------|----------|
| 全序列双向 | 早期扩散模型 | $O(N^2)$ 全局注意力 | 强 | 差（不可扩展） |
| 自回归逐帧 | **MAGI-1** (Teng et al., 2025, 24B)、**FramePack** (Zhang and Agrawala, 2025, 13B)、**SkyReels-V2** (Chen et al., 2025, 14B)、**MMPL** (Xiang et al., 2025, 14B) | 因果掩码逐帧预测 | 弱（漂移累积） | 较好 |
| 下一帧率预测 | **TempoMaster**（本文） | 低帧率双向全局规划 + 逐级并行细化 | 强（全局蓝图锚定） | 优（$O(N^2/4^K)$ 指数级加速） |

TempoMaster 的核心创新在于**解耦高层次时间语义（全局动态结构）与低层次视觉细节（局部运动与纹理）**。这一解耦基于一个关键洞察：视频中存在大量时间冗余，全局连贯的动态结构仅需稀疏的关键帧即可建立，剩余中间帧可在已知全局动态和上下文依赖的条件下高效推断。

具体而言，TempoMaster 将视频似然重新公式化为帧率序列的条件乘积：

$$p(V) = p(V^{K-1}) \prod_{i=0}^{K-2} p(V^i | V^{i+1}, V^{i+2}, ..., V^{K-2})$$

其中 $V^{K-1}$ 为最低帧率的全局蓝图，$V^i$ 为逐级提升帧率后的序列。这一公式化将自回归的“逐帧历史条件”替换为“逐级帧率条件”，从根本上切断了误差传播链。

### 3. 关键技术差异点

与上述基线方法相比，TempoMaster 在四个关键槽位上做出了实质性改变：

**（1）生成范式**：从自回归逐帧预测或全序列双向生成，转变为下一帧率预测。最低帧率阶段采用双向注意力建立全局结构，后续阶段以已生成帧为锚点并行填充中间帧。这同时继承了双向建模的全局规划能力与自回归的递进生成优势。

**（2）条件注入**：现有方法多采用适配器（adapter）或上下文学习（in-context learning），引入额外参数或增加上下文长度。TempoMaster 的 **Multi-Mask** 机制将任意数量条件帧按时间位置零填充至目标视频长度，编码后与噪声潜变量沿通道维拼接，并附加帧级掩码提供精确时间步信息，无需额外参数即可统一处理文本、图像、多帧等异构条件。

**（3）训练帧率**：不同于固定单帧率训练（如 24 fps），TempoMaster 采用多帧率训练（6, 12, 24 fps），通过 RoPE 的时间位置索引间隔 $2^i$ 注入帧率信息，并采用连续随机位置编码增大泛化性：

$$t_j = t_{\mathrm{start}} + j \cdot 2^i, \quad t_{\mathrm{start}} \sim \mathcal{U}[0, T_{max}]$$

**（4）推理策略**：从顺序片段生成或全序列一次性生成，转变为分层并行推理。生成过程组织为多路树，同级无因果依赖的子节点可并行生成，整体复杂度由 $O(N^2)$ 降至 $O(N^2/4^K)$（当并行段数 $W \geq 2$ 时）。

### 4. 适用边界与局限

**适用场景**：
- 长视频生成（500 帧以上），需要维持全局语义与运动连贯性
- 对计算效率有较高要求的部署场景，可通过调整并行配置灵活权衡质量与速度
- 多条件输入场景（文本、图像、多帧混合），Multi-Mask 提供统一注入接口

**已知局限**（论文未明确列出，需结合实验推断）：
- 并行策略的首帧延迟（Time-To-First-Frame, TTF）在不同配置下的具体表现未量化报告
- 随机时间索引在超长视频（>1500帧）或多镜头视频上的泛化效果未充分验证
- 在快速运动、大幅度相机运动等复杂场景下的运动连贯性保持情况缺乏专项评估

**开放问题**（需进一步研究）：
1. 不同并行配置（如 f(6,12,24) 配合 m(1,2,4) 等组合）在 Vbench 各子指标上的详细表现如何？
2. 并行策略在实际部署中的吞吐量与延迟权衡曲线如何？
3. 模型在更极端的运动场景（如体育赛事、第一人称快速移动）下的鲁棒性如何？

> **注意**：上述局限与开放问题部分基于对实验设计的逻辑推断，论文未提供明确的失败案例分析。建议在实际应用中针对具体场景进行补充验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/TempoMaster_Efficient_Long_Video_Generation_via_Next_Frame_Rate_Prediction.pdf]]

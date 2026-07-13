---
title: "Let Features Decide Their Own Solvers: Hybrid Feature Caching for Diffusion Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Let_Features_Decide_Their_Own_Solvers_Hybrid_Feature_Caching_for_Diffusion_Transformers.pdf
project_link: https://darrenzheng303.github.io/HyCa.github.io/
code_link: null
openreview_forum_id: URbsHlTK8c
aliases:
- LFDTOSHFCDT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将隐藏特征演化建模为混合ODE，通过动态聚类将维度分组，并为每个聚类分配最合适的数值求解器，实现维度感知的自适应缓存。"
primary_logic: "DiT的隐藏特征维度表现出异质ODE动态，但这些动态的聚类在提示、时序和分辨率上高度稳定，使得离线的“一次性选择”求解器成为可能，无需推理时额外开销。"
claims:
- "特征维度聚类在提示、时序和分辨率上高度稳定（ARI>0.8），验证了“一次性选择”求解器的可行性。"
- "HyCa在多种任务和模型（文本到图像、视频、编辑及蒸馏模型）上均实现近无损加速（如FLUX上5.55×加速，ImageReward仅降0.03%）。"
- "维度级缓存策略优于令牌级和统一缓存，混合求解器性能超越任何单一求解器。"
- "聚类和求解器分配对LoRA微调保持鲁棒，ARI仍高于0.8，无需重新聚类。"
---

# Let Features Decide Their Own Solvers: Hybrid Feature Caching for Diffusion Transformers

> [!tip] 核心洞察
> DiT的隐藏特征维度表现出异质ODE动态，但这些动态的聚类在提示、时序和分辨率上高度稳定，使得离线的“一次性选择”求解器成为可能，无需推理时额外开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 让特征决定自身求解器：面向扩散Transformer的混合特征缓存 |
| 英文题名 | Let Features Decide Their Own Solvers: Hybrid Feature Caching for Diffusion Transformers |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=URbsHlTK8c) · [Project](https://darrenzheng303.github.io/HyCa.github.io/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | HyCa |
| Dataset | FLUX.1-dev (DrawBench), Qwen-Image (DrawBench), HunyuanVideo (VBench), Qwen-Image-Edit (GEdit-Bench CN) |

> [!tip] 效果简介
> - FLUX.1-dev (DrawBench) 上，ImageReward ↑ 为 0.9895 (HyCa N=7)，对比 0.9898 (Original 50 steps)，变化 -0.03%。
> - Qwen-Image (DrawBench) 上，ImageReward ↑ 为 1.2363 (HyCa N=3)，对比 1.2547 (Original 50 steps)，变化 -1.465%。
> - HunyuanVideo (VBench) 上，VBench Score ↑ 为 80.25 (HyCa N=6)，对比 80.66 (Original 50 steps)，变化 -0.51%。

## 概要

扩散Transformer（DiT）在生成质量和多样性上持续突破，但其高昂的计算开销——源于每个去噪步骤都要执行完整的前向传播——严重制约了实际部署。特征缓存（feature caching）通过复用先前计算的隐藏表示来跳过冗余的Transformer块计算，已成为加速DiT的主流范式。然而，现有方法存在一个根本性的瓶颈：**它们对所有特征维度采用统一的缓存策略，忽视了不同维度间震荡与平滑等异质动态行为**，导致预测误差大、生成质量显著下降。

本文提出 **HyCa**（Hybrid Feature Caching），一个混合特征缓存框架。其核心洞察是：**DiT的隐藏特征维度表现出异质的ODE动态，但这些动态的聚类在提示、时序和分辨率上高度稳定**（ARI > 0.8，Figure 2），使得离线的“一次性选择”求解器成为可能，无需推理时额外开销。基于此，HyCa将隐藏特征演化建模为**混合ODE**，通过动态聚类将维度分组，并为每个聚类分配最合适的数值求解器，实现维度感知的自适应缓存。

在方法谱系中，HyCa相对于现有特征缓存工作做出了三个关键改变：首先，缓存粒度从令牌级（如 **ToCa**，Zou et al., 2024a；**DuCa**，Zou et al., 2024b）或统一维度级（如 **FORA**，Selvaraju et al., 2024；**TaylorSeer**，Liu et al., 2025a）转向**维度级动态聚类分组**；其次，求解器分配从单一求解器（如TaylorSeer的泰勒外推、FORA的跳步复制）转向**混合求解器池**（包含Runge–Kutta、Adams–Bashforth、Taylor、BDF、Adams–Moulton等），通过最小化每个聚类内所有维度的平均下一步预测误差来优化分配；第三，特征动态建模从单一ODE或启发式预测升级为**混合ODE体系**，捕捉异质动态。

实验覆盖文本到图像、视频生成、图像编辑及蒸馏模型等多种任务和架构。主要结果包括：在FLUX.1-dev上实现**5.55×加速**，ImageReward仅降0.03%（Table 2）；在HunyuanVideo上实现**5.56×加速**，VBench得分仅降0.51%（Table 3）；在Qwen-Image-Edit上实现**6.24×加速**，且整体得分反超原始模型0.41%（Table 4）。消融研究证实，维度级缓存策略显著优于令牌级和统一缓存，混合求解器性能超越任何单一求解器（Figure 7）。此外，聚类和求解器分配对LoRA微调保持鲁棒（ARI > 0.8），无需重新聚类。该方法仅需约1秒的离线预处理，无需额外训练，在近无损质量下实现了显著的推理加速。



扩散Transformer（DiT）已成为文生图、文生视频等生成任务的主流架构。然而，其推理过程需要数十步去噪，每一步都需完整执行深层Transformer块，计算开销极大。为缓解这一问题，**特征缓存**（Feature Caching）作为一种免训练的加速范式被广泛采纳：它利用去噪过程中隐藏特征的时序冗余，在部分步骤跳过Transformer计算，直接复用或预测缓存的特征。

现有特征缓存方法存在一个共同瓶颈：**对所有特征维度施加统一的缓存策略**。无论是基于令牌级选择的方法（如 **ToCa**，Zou et al., 2024a；**DuCa**，Zou et al., 2024b），还是统一复用全部维度的方案（如 **FORA**，Selvaraju et al., 2024；**TaylorSeer**，Liu et al., 2025a），都隐含假设所有特征维度的演化行为是同质的。然而，实证观察表明，DiT隐藏特征的不同维度呈现出显著异质的动态行为——部分维度轨迹剧烈震荡，另一些则平滑单调（Figure 2 a–b）。这种“一刀切”的缓存策略忽视了维度间的动态差异，导致预测误差累积，最终损害生成质量。

本文的核心动机源于一个关键发现：**尽管特征维度表现出异质的ODE动态，但这些维度的聚类分配在提示、时序和分辨率上高度稳定**（Figure 2 c–d，调整兰德指数ARI > 0.8）。这一稳定性意味着，可以在离线阶段通过“一次性”分析确定每个维度聚类的最优求解器，而在推理时无需额外开销即可实现维度感知的自适应缓存。

基于此，本文提出 **HyCa**（Hybrid Feature Caching），将隐藏特征演化建模为**混合ODE**，通过无监督聚类将维度分组，并为每个聚类从求解器池中自动分配最合适的数值求解器（如Runge–Kutta、Adams–Bashforth、Taylor等），从而实现维度级自适应缓存。该方法在多种DiT模型和任务上均实现了近无损的显著加速（如FLUX上5.55×，ImageReward仅降0.03%），验证了“让特征决定自身求解器”这一范式的有效性。



## 核心方法与创新机理

HyCa的核心创新在于将DiT的隐藏特征演化建模为**混合ODE（mixture of ODEs）**，并据此实现**维度级自适应求解器分配**。这一设计直接回应了现有特征缓存方法的根本瓶颈：对所有特征维度采用统一策略，忽视了不同维度间存在的异质动态行为（如震荡与平滑），导致预测误差大、生成质量下降。

### 关键改进点

**1. 缓存粒度：从令牌级到维度级**

现有方法普遍在令牌（token）级别决定缓存策略（如**ToCa**的令牌级选择，Zou et al., 2024a；**DuCa**的动态令牌更新，Zou et al., 2024b）或对所有维度采用统一策略（如**FORA**的隐藏表示复用，Selvaraju et al., 2024；**TaylorSeer**的多项式外推，Liu et al., 2025a）。HyCa首次将缓存粒度下沉到**特征维度（dimension）级别**，并通过无监督聚类将具有相似动态行为的维度分组。

这一选择的核心依据是维度级聚类的**高度稳定性**：实验表明，聚类分配在提示、时序和分辨率上均保持高度一致（ARI>0.8），而令牌级特征则缺乏这种不变性。这验证了“一次性选择”求解器的可行性——只需在单个提示的前几步进行一次探测，即可为所有后续推理确定最优求解器分配。

**2. 特征动态建模：从单一ODE到混合ODE**

基线方法通常将特征演化视为单一动态过程（如TaylorSeer的Taylor外推），或采用启发式预测（如FORA的跳步复制）。HyCa首次将隐藏特征演化形式化为**混合ODE**：

$$\frac{d}{d\tau}\mathcal{F}(x(\tau)) = g_{\boldsymbol{\theta}}(\mathcal{F}(x(\tau)), \tau)$$

并认识到不同维度遵循不同的局部动态——有些维度呈平滑近线性演化，适合显式方法；有些则表现出快速震荡，需要隐式方法处理。基于这一视角，特征缓存被自然地转化为数值ODE求解问题。

**3. 求解器策略：从单一求解器到混合求解器池**

这是HyCa最关键的机制创新。现有方法本质上使用单一求解器（如TaylorSeer的Taylor公式、FORA的零阶保持），而HyCa构建了一个包含显式和隐式方法的**求解器池** $S$：Runge–Kutta (RK)、Adams–Bashforth (AB)、Taylor Formula (TF)、Backward Differentiation Formula (BDF) 和 Adams–Moulton (AM)。每种求解器具有不同的稳定性和精度特性，适用于不同类型的局部动态。

求解器分配通过一个**一次性优化过程**完成：在探测阶段提取每个维度的动态描述符（Jerk ratio、curvature ratio等），经k-means聚类后，为每个聚类选择平均预测误差最小的求解器：

$$\operatorname*{min}_{\{s_c \in S\}_{c=1}^C} \sum_{c=1}^C \left[ \frac{1}{|c|} \sum_{d \in c} \left\| \hat{\mathcal{F}}_{t+1}^{(s_c, d)} - \mathcal{F}_{t+1}^{(d)} \right\|_2^2 \right]$$

消融实验（Figure 7 c-d）直接验证了这一设计的有效性：HyCa的混合求解器策略在预测误差和图像质量上均**超越任何单一求解器基线**（如纯RK、纯Taylor等），证明其收益来源于组合多样化求解器，而非依赖单一积分策略。

### 创新点的因果链路

这三个改进形成了一条清晰的因果链：**混合ODE建模**（识别异质动态）→ **维度级聚类**（利用聚类稳定性实现一次性分配）→ **混合求解器池**（为不同动态匹配最优求解器）。这一链路使得HyCa在多种模型（FLUX、Qwen-Image、HunyuanVideo）和任务（文本到图像、视频生成、图像编辑）上均实现近无损加速，甚至在蒸馏模型上**提升**生成质量（FLUX.1-schnell上ImageReward提升5.03%），这是单一求解器方法无法实现的。

值得注意的是，聚类和求解器分配对LoRA微调保持鲁棒（ARI>0.8），无需重新聚类即可直接复用，进一步降低了实际部署的门槛。



![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/003_Figure_3.jpg]]
*Figure 3: HyCa Framework. (a) Offline Preprocessing: feature dimensions are first analyzed and clustered with temporal indicators (e.g., differences, curvature). For each cluster, candidate solvers generate predicted features, then compared against real computed features; the solver with minimum error is then assigned to that cluster. (b) Inference: once assigned, each cluster consistently reuses its solver, enabling efficient prediction by skipping redundant computations while maintaining accuracy*

HyCa 的整体流程分为两个阶段：**离线预处理** 与 **推理时混合缓存**。其核心思路是将 DiT 中隐藏特征的演化建模为一个**混合常微分方程**，并通过维度级的动态聚类为每一组特征维度分配合适的数值求解器，从而在跳过冗余计算的同时保持预测精度。

### 离线预处理阶段

预处理阶段的目标是为目标模型建立一套“一次性”的维度-求解器映射表，仅需在单个提示词的前几个时间步上完成一次探测，耗时约 1 秒，无需任何训练。

1. **动态指标提取与聚类**：在探测过程中，对每个特征维度 $d$ 提取一个描述其时间动态的向量 $\phi_d$，包含 Jerk ratio、curvature ratio 等时序指标。随后，对全体维度施加 k-means 聚类，得到 $C$ 个聚类 $\{c(d)\}$，每个聚类内部的特征维度共享相似的 ODE 动态行为。

2. **求解器选择**：针对每个聚类 $c$，从预定义的求解器池 $S$ 中选出最优求解器 $s_c^*$。求解器池包含显式与隐式数值方法：Runge–Kutta (RK)、Adams–Bashforth (AB)、Taylor Formula (TF)、Backward Differentiation Formula (BDF) 和 Adams–Moulton (AM)。选择标准是最小化聚类内所有维度的平均下一步预测误差：
   $$\operatorname*{min}_{\{s_c \in S\}_{c=1}^C} \sum_{c=1}^C \left[ \frac{1}{|c|} \sum_{d \in c} \left\| \hat{\mathcal{F}}_{t+1}^{(s_c, d)} - \mathcal{F}_{t+1}^{(d)} \right\|_2^2 \right]$$

聚类分配在提示词、时间步和分辨率上表现出高度稳定性（ARI > 0.8），这意味着离线阶段选定的求解器映射可直接复用于任意推理场景，无需重新计算。

### 推理时混合缓存

推理阶段直接复用离线阶段建立的聚类-求解器映射，在跳跃步骤中执行维度感知的特征预测：

- 在需要跳过计算的步骤中，对每个聚类 $c$ 使用其预分配的求解器 $s_c^*$，基于先前缓存的残差特征 $\mathcal{F}_t, \mathcal{F}_{t-1}, \dots$ 预测当前步骤的残差 $\hat{\mathcal{F}}_{t+1}$，并将其注入 Transformer 块。
- 不同聚类采用不同的数值策略：平滑维度可能使用低阶外推，而震荡维度则使用隐式方法以保证稳定性。
- 前几步始终完整计算，因此早期步骤中可能存在的轻微聚类不稳定并不影响最终生成质量。

### 与基线方法的模块级差异

| 模块 | 基线做法 | HyCa 做法 |
|------|----------|-----------|
| 缓存粒度 | 令牌级（ToCa, DuCa）或维度统一（FORA, TaylorSeer） | 维度级，按动态聚类分组 |
| 特征演化建模 | 单一 ODE 或启发式预测 | 混合 ODE，捕获异质动态 |
| 求解器策略 | 单一求解器（如 TaylorSeer 的 Taylor 外推、FORA 的跳步复制） | 混合求解器池，每聚类自动择优 |

HyCa 的维度级缓存策略相较于令牌级方案具有更好的稳定性——特征空间的聚类结构在跨提示、分辨率和时间步的条件下几乎不变（Figure 6），而令牌级缓存在不同输入下的行为一致性则难以保障。同时，混合求解器策略使 HyCa 在预测误差和生成质量上均超越任何单一求解器基线（Figure 7 c-d），验证了“让特征决定自身求解器”这一核心洞察的有效性。



HyCa 将特征缓存重新建模为数值常微分方程（ODE）求解问题，其核心由三个模块串联构成：**动态分析与聚类**、**求解器选择**、**推理时混合缓存**。

### 3.1 特征演化的混合ODE建模

DiT 的隐藏特征演化可被描述为由网络诱导的连续时间 ODE：

$$
\frac{d}{d\tau}\mathcal{F}(x(\tau)) = g_{\boldsymbol{\theta}}\big(\mathcal{F}(x(\tau)), \tau\big)
$$

其中 $\mathcal{F}$ 为某 Transformer 层的隐藏特征，$\tau$ 为连续时间变量，$g_{\boldsymbol{\theta}}$ 为网络参数化的动力学函数。传统特征缓存直接复用上一步计算的特征值：

$$
\tilde{\mathcal{F}}_k = \mathcal{C}(\mathcal{F}_t, k) := \mathcal{F}_t, \quad \forall k \in (t, t+n-1]
$$

即在 $n$ 步跳跃窗口内，用 $t$ 时刻的特征 $\mathcal{F}_t$ 替代 $k$ 时刻的真实特征。这一“复制即用”策略等价于零阶保持器，对震荡维度引入显著误差。

HyCa 的核心洞察是：**不同特征维度呈现异质动态行为**——部分维度轨迹平滑，部分则剧烈震荡。因此，将特征演化建模为 **混合 ODE**，并为每个维度集群分配合适的数值求解器，是降低预测误差的关键。

### 3.2 求解器池

为适配从平滑近线性到快速变化的不同局部动态，HyCa 构建了一个包含显式和隐式方法的求解器池 $S$，涵盖五类数值格式：

- **Runge–Kutta (RK)**：基于多步缓存残差的显式预测，适合平滑轨迹的二阶外推。
- **Adams–Bashforth (AB)**：显式线性多步法，利用历史特征值的加权组合。
- **Taylor Formula (TF)**：基于泰勒展开的多阶导数外推，适合近线性维度。
- **Backward Differentiation Formula (BDF)**：隐式方法，对震荡或离散动态具有更好的稳定性。
- **Adams–Moulton (AM)**：隐式校正格式，与 AB 配合可进一步提升精度。

每个求解器以先前缓存特征为输入，输出下一时刻的预测值：

$$
\hat{\mathcal{F}}_{t+1} \approx \operatorname{Solver}(\mathcal{F}_t, \mathcal{F}_{t-1}, ...)
$$

以二阶 RK 预测器为例，仅需两个缓存残差即可完成外推：

$$
\widehat F_{t_{n+1}}^{(d)} = \frac{3}{2} F_{t_n}^{(d)} - \frac{1}{2} F_{t_{n-2}}^{(d)}
$$

### 3.3 动态聚类与一次性求解器分配

**动态分析与聚类**模块在离线预处理阶段运行：对单个提示的前几个去噪步骤，提取每个特征维度 $d$ 的动态描述向量 $\phi_d$（包含 Jerk ratio、curvature ratio 等时序指标），随后应用 k-means 聚类获得维度分区 $\{c(d)\}$。聚类结果在提示、时序和分辨率上高度稳定（ARI > 0.8，见 Figure 2），这为“一次性选择”求解器提供了可行性保障。

**求解器选择**模块对每个聚类 $c$，从求解器池 $S$ 中选择平均下一步预测误差最小的求解器 $s_c^*$：

$$
\operatorname*{min}_{\{s_c \in S\}_{c=1}^C} \sum_{c=1}^C \left[ \frac{1}{|c|} \sum_{d \in c} \left\| \hat{\mathcal{F}}_{t+1}^{(s_c, d)} - \mathcal{F}_{t+1}^{(d)} \right\|_2^2 \right]
$$

该优化仅需一次探测性前向传播即可完成，无需额外训练。

**推理时混合缓存**模块在跳跃步骤中，对每个聚类使用其预分配的求解器，基于缓存特征预测下一个残差，并注入 Transformer 块。前几步始终完整计算，因此早期聚类的不稳定性不影响最终生成质量（见 Figure 15 的消融验证）。



## 实验与关键发现

### 核心性能：近无损加速的跨任务验证

HyCa在文本到图像、视频生成、图像编辑及蒸馏模型四个场景上均实现了近无损的显著加速，核心证据如下：

- **Qwen-Image（文本到图像）**：在DrawBench的200个提示上，HyCa以N=3配置实现2.12×加速，ImageReward仅从1.2547降至1.2363（-1.465%），远优于同等加速比下的所有基线方法（Table 1）。当加速比提升至5.38×（N=8）时，ImageReward仍保持在1.0811，而TeaCache在相近加速比下已降至0.7936。
- **FLUX.1-dev**：HyCa在N=7配置下达到5.55×加速，ImageReward为0.9895，与原始50步模型的0.9898几乎持平（-0.03%），同时CLIP Score仅降0.28%（Table 2）。在N=4时甚至出现+2.865%的ImageReward正增益，表明混合求解器在适度缓存下可超越原始质量。
- **HunyuanVideo（文本到视频）**：在VBench的946个提示上，HyCa以N=6实现5.56×加速，VBench Score从80.66降至80.25（-0.51%），保持视频时序一致性（Table 3）。相比之下，TaylorSeer在相近加速下出现明显伪影和时序不一致（Figure 10）。
- **Qwen-Image-Edit（图像编辑）**：在GEdit-Bench上，HyCa以N=8实现6.24×加速，中文Overall Score从7.41提升至7.44（+0.41%），英文从7.36提升至7.38（+0.27%），证明缓存策略对编辑任务同样有效（Table 4）。
- **蒸馏模型**：在FLUX.1-schnell（4步蒸馏）上，HyCa以N=2进一步加速至2×，ImageReward从0.9133提升至0.9592（+5.03%），延迟从2.34s降至1.16s（Table 5）。这表明HyCa的隐式求解器（如BDF）能有效处理蒸馏模型的离散/振荡动态，而其他缓存方法在此场景下失效。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of text-to-image generation on Qwen-Image*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of text-to-image generation on FLUX.1-dev*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison of text-to-video generation on HunyuanVideo*

### 消融研究：维度级缓存与混合求解器的双重优势

**维度级缓存优于令牌级和统一策略。** Figure 7(a-b)显示，在FLUX和Qwen-Image上，HyCa的维度级分配在ImageReward和预测误差上均显著优于令牌级方法（ToCa, DuCa）和统一缓存方法（FORA, TaylorSeer）。这一优势源于特征维度的聚类在提示、时序和分辨率上的高度稳定性（ARI>0.8，Figure 6），而令牌级动态随内容剧烈变化，难以稳定预测。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/011_Figure_6.jpg]]
*Figure 6: Top row: Clustering results from FLUX; Bottom row: Clustering results from Hunyuan Video. The clustering assignments remain highly consistent across various prompts, resolutions and timesteps, suggesting stable and robust geometric structure in the feature space*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/012_Figure_7.jpg]]
*Figure 7: Overall and ablation results of HyCa. (a–b) HyCa consistently outperforms token-wise (ToCa, DuCa) and one-size-fits-all (FORA, Taylorseer) baselines on FLUX and Qwen-Image. (c–d) Ablation on FLUX shows HyCa surpasses all single-solver baselines in the solver pool, maintaining lower error and better quality. Confirming that HyCa benefits from combining diverse solvers rather than relying on a single integration strategy*

**混合求解器超越任何单一求解器。** Figure 7(c-d)的消融显示，在FLUX上HyCa的混合策略比求解器池中任一单一求解器（纯RK、纯AB、纯TF、纯BDF、纯AM）都获得更低的预测误差和更高的ImageReward。这验证了核心假设：不同特征维度确实表现出异质ODE动态，需要不同的数值方法才能准确预测——平滑维度适合低阶显式方法，振荡维度则需要隐式方法。

**聚类稳定性的边界条件。** 附录分析揭示了两个边界情况：
- **极端设置下聚类保持稳定**：在极端分辨率（如1024×1024与256×256对比）和无意义提示下，ARI仍超过0.8（Figure 14），说明聚类结构对输入扰动鲁棒。
- **早期步骤的轻微不稳定不影响生成**：去噪的最初2-3步聚类可能不一致，但Figure 15证明这不对最终图像质量产生影响，因为前几步总是完整计算，不涉及缓存预测。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/019_Figure_14.jpg]]
*Figure 14: (a–b) The left two figures show that clustering structures remain stable under extreme resolution settings. (c–d) The right two figures show that clustering is also consistent for nonsensical prompts and closely matches those from normal, well-formed prompts*

### LoRA鲁棒性：无需重新聚类的即插即用

HyCa的聚类分配对LoRA微调保持高度不变性。Figure 8和Figure 13显示，在FLUX.1-dev及其Art LoRA和Anime LoRA变体之间，聚类分配的ARI均值超过0.8。这意味着用户只需在原始模型上执行一次离线聚类（约1秒），即可直接将相同的求解器分配应用于任意LoRA变体，无需额外预处理。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/018_Figure_13.jpg]]
*Figure 13: ARI between clustering assignments from FLUX.1-dev and its LoRA variants. (a) ARI distributions across different prompts and timesteps for FLUX.1-dev show clustering consistency within the base model. (b) and (c) compare the original model’s clustering with that from Art LoRA and Anime LoRA, respectively. In both cases, the ARI values remain high (most above 0.8, marked by the red dashed line), confirming strong agreement between the LoRA and original clustering results. This further supports that solver assignments in HyCa can be reused across LoRA variants*

### 失败模式与局限

1. **早期步骤聚类不稳定（已缓解）**：如Figure 15所示，前3步的聚类可能不一致，但因这些步骤总是完整计算，实际生成质量不受影响。
2. **极端加速下的质量退化**：在FLUX.1-schnell上N=8时，ImageReward下降13.84%（Table 2），表明在已高度压缩的蒸馏模型上过度缓存仍会导致质量损失。
3. **求解器池的手工设计限制**：当前求解器池由经典数值方法构成，未利用数据驱动的学习型预测器，可能在特定动态模式下存在改进空间。
4. **架构泛化性待验证**：所有实验均在DiT架构（FLUX、Qwen-Image、HunyuanVideo）上进行，对U-Net等传统架构的适用性尚未探索。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/002_Figure_2.jpg]]
*Figure 2: Feature trajectory clusters and stability of assignments. (a–b) Cluster 1 shows oscillatory trajectories while Cluster 2 shows smooth ones. (c–d) ARI distributions on Hunyuan Video and Qwen-Image exceed 0.8 in most cases, confirming stable and consistent cluster assignments across prompts and timesteps. An ARI above 0.8 indicates strong agreement and high clustering reliability*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/016_Figure_11.jpg]]
*Figure 11: The first row shows, from left to right, ARI comparison plots of FLUX, Qwen-Image, and Hunyuan Video under different prompts and timesteps, with the last plot illustrating ARI comparisons of FLUX across different resolutions. It can be seen that ARI distributions exceed 0.8 in most cases, confirming stable and consistent cluster assignments across prompts, timesteps and resolutions. An ARI above 0.8 indicates strong agreement and high clustering reliability. The three plots in the second row depict the intra-cluster metric shifts between clusters formed by indicators from every two adjacent prompts of FLUX. The normalized value is obtained by dividing the inter-cluster shift of a given indi...*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/017_Figure_12.jpg]]
*Figure 12: Clustering consistency between original and LoRA-tuned models. Each subplot visualizes the clustering results under different prompts for FLUX.1-dev (top row), and its two LoRA variants, the Art LoRA (middle row) and Anime LoRA (bottom row). Despite fine-tuning, the cluster boundaries remain highly consistent across prompts and models, indicating that HyCa’s solver assignments remain stable and reusable even after LoRA adaptation*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_URbsHlTK8c/figures/020_Figure.jpg]]
*Figure: (a)*



## 定位与知识库关联

### 核心瓶颈与设计动机

现有扩散Transformer（DiT）的特征缓存方法存在一个被普遍忽视的结构性瓶颈：**对所有特征维度采用统一缓存策略**。无论是**FORA**（Selvaraju et al., 2024）的直接复用、**ToCa**（Zou et al., 2024a）的令牌级选择、**DuCa**（Zou et al., 2024b）的动态更新，还是**TaylorSeer**（Liu et al., 2025a）的多项式外推，均将隐藏特征视为同质整体，忽略了不同维度间存在**震荡型与平滑型**等异质动态行为。这种“一刀切”策略导致预测误差累积，在高加速比下生成质量急剧下降。

HyCa的突破性洞察在于：**DiT隐藏特征的演化可建模为混合ODE**，且这些动态的聚类结构在提示、时序和分辨率上高度稳定（ARI > 0.8，Figure 2(c-d)）。这一发现将特征缓存问题从“如何为所有维度找一个好策略”转化为“如何为每个维度聚类分配最合适的数值求解器”，从而在推理时零额外开销的前提下实现维度感知的自适应缓存。

### 方法谱系定位

HyCa在特征缓存方法谱系中占据**维度级混合求解器**的独特位置，可沿两个关键维度与现有工作区分：

**缓存粒度维度**：
- **统一缓存**：**FORA**（Selvaraju et al., 2024）、**TeaCache**（Liu et al., 2024）、**∆-DiT**（Chen et al., 2024c）对所有特征维度采用相同策略。
- **令牌级缓存**：**ToCa**（Zou et al., 2024a）、**DuCa**（Zou et al., 2024b）在令牌层面进行选择性缓存或更新。
- **维度级缓存（HyCa）**：以特征维度为最小缓存单元，通过聚类将维度分组后分别处理。

消融实验（Figure 7(a-b)）明确证实：维度级分配在ImageReward和预测误差上均显著优于令牌级和统一基线，验证了更细粒度缓存的价值。

**求解器策略维度**：
- **单一求解器**：**TaylorSeer**（Liu et al., 2025a）使用Taylor外推，**FORA**采用直接复用（等价于零阶保持），**FoCa**（Zheng et al., 2025）在频域操作但本质仍为单一策略。
- **混合求解器（HyCa）**：构建包含Runge–Kutta、Adams–Bashforth、Taylor、BDF、Adams–Moulton等显式和隐式方法的求解器池，为每个聚类自动选择最优求解器。

消融实验（Figure 7(c-d)）表明：混合求解器策略在预测误差和图像质量上均超越任何单一求解器（如纯RK、纯Taylor等），验证了组合多样化求解器的收益。

### 关键设计决策与因果机制

**1. 为什么是维度级而非令牌级？**

核心原因在于稳定性。令牌级动态受语义内容影响剧烈，跨提示变化大；而特征维度的动态模式在模型训练后即固化，形成稳定的几何结构。Figure 6的可视化显示：FLUX和HunyuanVideo的聚类分配在跨提示、分辨率和时间步下保持高度一致，暗示特征空间存在稳健的内在几何结构。这一稳定性使得**离线的“一次性选择”求解器**成为可能——仅需在单个提示的前几步进行一次探测，即可确定适用于所有后续推理的求解器分配。

**2. 混合ODE建模的因果链**

HyCa的因果链可概括为：
- **异质动态识别**：通过Jerk ratio、curvature ratio等时序指标提取每个维度的动态特征描述符 $\phi_d$。
- **稳定聚类**：k-means聚类将维度分组，聚类分配跨条件高度稳定（ARI > 0.8）。
- **求解器匹配**：对每个聚类，从求解器池中选择平均下一步预测误差最小的求解器（公式5）。
- **推理时零开销**：预分配的求解器在推理时直接复用，无需额外计算。

**3. 对蒸馏模型的特殊适配**

HyCa的求解器池包含BDF等隐式方法，适合处理蒸馏模型（如FLUX.1-schnell）中常见的离散或震荡动态。Table 5显示：HyCa在FLUX.1-schnell上不仅实现2×加速，还将ImageReward从0.9133提升至0.9592（+5.03%），表明混合求解器策略可**逆转蒸馏模型的质量损失**——这是单一求解器方法无法实现的。

### 适用边界与鲁棒性

**已验证的适用范围**：
- **架构**：DiT系列（FLUX、Qwen-Image、HunyuanVideo），覆盖文本到图像、文本到视频、图像编辑任务。
- **模型变体**：原始模型、蒸馏模型（FLUX.1-schnell）、LoRA微调模型。
- **加速比**：2×至6.24×，在多个模型上实现近无损加速。

**LoRA鲁棒性**：Figure 13的ARI量化分析显示，原始FLUX.1-dev与其Art LoRA和Anime LoRA变体之间的聚类分配ARI均值超过0.8，表明HyCa的聚类结果对LoRA微调几乎不变，无需重新聚类或求解器选择。这一特性极大降低了实际部署中的适配成本。

**极端条件鲁棒性**：Figure 14验证了在极端分辨率设置和无意义提示下，聚类结构仍保持稳定，ARI分布超过0.8。

### 局限性与已知失效模式

1. **离线预处理需求**：每个模型需进行一次离线聚类和求解器选择（约1秒），虽无需训练，但无法实现完全即插即用的零样本部署。

2. **早期步骤聚类不稳定**：Figure 15揭示，在最初2-3个去噪步骤中聚类结果可能不一致，但不影响生成质量——因为前几步总是完整计算，不涉及特征缓存。这一失效模式被系统设计自然规避。

3. **求解器池的手工设计**：当前求解器池限于经典数值方法，未引入数据驱动的学习型预测器，可能未充分利用特征动态的可预测性。

4. **架构限制**：所有验证均在DiT架构上完成，是否适用于U-Net或其他生成架构尚待研究。U-Net的跳跃连接结构可能引入不同的特征动态模式。

### 开放问题

- **跨范式扩展**：混合ODE视角是否能推广到自回归生成模型（如LLM的KV缓存）？自回归模型中的隐藏状态演化是否也呈现可聚类的异质动态？

- **学习型缓存策略**：能否通过元学习或强化学习自动发现更优的求解器，甚至学习全新的预测算子以替代手工设计的数值方法？

- **聚类指标的自适应选择**：当前使用的Jerk ratio等时序指标是否为最优？能否设计自适应机制根据模型特性自动选择或组合动态描述符？

- **大规模可扩展性**：在百亿参数级DiT上，聚类数量是否需要增加？求解器池是否需要扩展？离线探测的计算成本是否仍可忽略？

- **与模型压缩的协同**：HyCa与剪枝、量化等模型压缩技术的叠加效果如何？维度级缓存是否可与结构化稀疏性结合实现更高加速？



## 原文 PDF

![[paperPDFs/ICLR_2026/Let_Features_Decide_Their_Own_Solvers_Hybrid_Feature_Caching_for_Diffusion_Transformers.pdf]]

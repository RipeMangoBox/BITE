---
title: "Fast3Dcache: Training-free 3D Geometry Synthesis Acceleration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Fast3Dcache_Training_free_3D_Geometry_Synthesis_Acceleration.pdf
project_link: "https://fast3dcache-agi.github.io"
code_link: null
aliases:
- Fast3Dcache
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 体素占用稳定化的三阶段对数线性衰减模式可被建模以动态控制缓存预算，同时利用潜在特征的速度和加速度震荡来识别可安全复用的稳定令牌。
primary_logic: 去噪过程中体素变化呈现可预测的三阶段模式，其中第二阶段可通过对数线性函数近似；联合分析速度大小与加速度大小的变化能精确区分稳定区域与活跃区域，使得在不损害几何保真度的前提下大幅跳过冗余计算。
claims:
- Fast3Dcache 在 TRELLIS 上实现 27.12% 吞吐量提升和 54.83% FLOPs 降低，而 Chamfer Distance 仅增加 2.48%，F-Score 仅下降 1.95%
- PCSC 动态调度显著优于固定比例缓存，固定比例（25%/12.5%）会导致严重的几何退化
- SSC 联合速度和加速度比单独使用任一指标获得更好的几何保真度
- 与 TeaCache 结合可实现 3.41× 加速，并改善 CD 和 F-Score
---

# Fast3Dcache: Training-free 3D Geometry Synthesis Acceleration

> [!tip] 核心洞察
> 去噪过程中体素变化呈现可预测的三阶段模式，其中第二阶段可通过对数线性函数近似；联合分析速度大小与加速度大小的变化能精确区分稳定区域与活跃区域，使得在不损害几何保真度的前提下大幅跳过冗余计算。

| 字段 | 内容 |
|------|------|
| 中文题名 | Fast3Dcache：无训练的3D几何合成加速 |
| 英文题名 | Fast3Dcache: Training-free 3D Geometry Synthesis Acceleration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22533) · [Project](https://fast3dcache-agi.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Fast3Dcache |
| Dataset | TRELLIS, DSO |

> [!tip] 效果简介
> - TRELLIS (Toys4K) 上，Throughput (iters/s)↑ / FLOPs (T)↓ / CD↓ / F-Score↑ Fast3Dcache (τ=8): 0.6426 / 110.3 / 0.0703 / 53.7528 vs Vanilla TRELLIS: 0.5055 / 244.2 / 0.0686 / 54.8244 (Throughput +27.12%, FLOPs -54.83%, CD +2.48%, F-Score -1.95%)。
> - DSO (Toys4K) 上，Throughput (iters/s)↑ / FLOPs (T)↓ / CD↓ / F-Score↑ Fast3Dcache (τ=8): 0.4071 / 115.4 / 0.0704 / 53.5487 vs Vanilla DSO: 0.3496 / 244.2 / 0.0687 / 54.8350 (Throughput +16.45%, FLOPs -52.74%, CD +2.47%, F-Score -2.35%)。

## 概述

3D扩散模型在几何合成阶段存在大量计算冗余——去噪过程中相邻时间步的潜在特征和体素占用状态高度相似，但直接复用2D/视频缓存方法会破坏几何一致性，导致拓扑错误和结构伪影。**Fast3Dcache** 针对这一瓶颈提出了一种无训练的几何感知缓存框架，其核心洞察是：去噪过程中体素变化呈现可预测的三阶段模式，其中第二阶段可通过对数线性函数近似；同时，联合分析潜在特征的速度大小与加速度大小的变化能精确区分稳定区域与活跃区域，从而在不损害几何保真度的前提下大幅跳过冗余计算。

方法层面，Fast3Dcache 引入两个关键机制：**Predictive Caching Scheduler Constraint (PCSC)** 通过对数线性衰减模型动态预测每步可缓存的令牌数量，替代固定比例采样；**Spatiotemporal Stability Criterion (SSC)** 联合归一化后的速度和加速度评分，精准筛选可安全复用的稳定令牌。整个推理过程划分为三个阶段——初期全采样建立几何基础、中期动态缓存加速主体去噪、末期无CFG细化阶段采用激进缓存策略，并在阶段间设置周期性刷新以控制误差累积。

在 **TRELLIS** 框架上，Fast3Dcache 实现 **27.12%** 吞吐量提升和 **54.83%** FLOPs 降低，而 Chamfer Distance 仅增加 **2.48%**、F-Score 仅下降 **1.95%**；在 **DSO** 变体上同样取得 **16.45%** 加速和 **52.74%** FLOPs 降低。消融实验证实，PCSC 自适应调度显著优于固定比例缓存（后者导致严重的几何退化），SSC 联合速度和加速度比单独使用任一指标获得更好的几何保真度。此外，Fast3Dcache 与模态无关加速器 **TeaCache** 结合可实现 **3.41×** 加速，且几何质量优于单独使用 TeaCache，验证了方法的互补性。

## 背景与动机

### 3D生成扩散模型的计算瓶颈

基于扩散模型的3D内容生成近年来取得了显著进展，以 **TRELLIS** 为代表的框架通过稀疏结构潜在表示实现了高质量的几何合成。然而，这类方法在推理阶段面临严重的计算冗余问题：去噪过程通常需要数十步迭代，每步均需对完整的潜在特征网格执行Transformer自注意力计算，导致FLOPs开销巨大、生成吞吐量受限。

将2D或视频领域的缓存加速策略直接移植到3D几何合成中存在根本性障碍。以 **RAS**（模态感知的DiT缓存方法）为代表的现有方案，在3D场景下会导致显著的几何退化——实验表明，RAS在25%采样率下使F-Score下降26.53%（Table 1）。其根本原因在于：2D缓存方法依赖特征相似度或随机选择来判定令牌的可复用性，但3D几何合成中潜在特征网格的演化与最终几何结构的拓扑一致性紧密耦合，粗暴的令牌丢弃会破坏体素占用的空间连贯性，引入拓扑错误和表面伪影（Figure 4）。

### 体素稳定化的三阶段可预测模式

Fast3Dcache的核心发现是：3D扩散去噪过程中，体素占用的变化呈现高度可预测的三阶段模式（Figure 1a）。

- **Phase 1（不稳定形成期）**：去噪初期，几何轮廓从噪声中逐步涌现，体素占用状态剧烈翻转，动态体素数（相邻时间步状态变化的体素数量，定义为 $\Delta s_t = \sum_{i,j,k} \left( O_{t+1}(i,j,k) \oplus O_t(i,j,k) \right)$）维持在高位且波动剧烈。
- **Phase 2（稳定衰减期）**：几何主体结构确立后，动态体素数进入系统性衰减阶段。关键洞察在于，这一衰减在对数坐标系下可被线性函数可靠近似，即 $\log(\Delta \hat{s}) = \mu \cdot t + \lambda$，其中斜率 $\mu$ 刻画衰减速率。
- **Phase 3（CFG-Free精炼期）**：当分类器自由引导（CFG）关闭后，动态体素数出现急剧下降（Figure 7），几何结构进入微调收敛状态，计算冗余达到峰值。

这一三阶段模式构成了Fast3Dcache动态缓存调度策略的理论基础：Phase 2的可预测衰减使得缓存预算可以被主动建模和外推，而非依赖固定比例或启发式规则。

### 潜在特征的双重稳定性信号

除了体素层面的宏观稳定趋势，Fast3Dcache进一步揭示了潜在特征网格内部的微观稳定性信号。定义令牌 $i$ 在时间步 $t$ 的**瞬时缓存误差（ICE）**，即加速度大小：

$$\operatorname{ICE}_i(t) \triangleq A_i(t) = ||\nu_i(t) - \nu_i(t-1)||_2$$

其中 $\nu_i(t)$ 为令牌 $i$ 在时间步 $t$ 的速度向量。加速度大小衡量了潜在特征更新的瞬时不稳定程度——加速度越小，表明该令牌的特征演化越趋于平稳，越适合被缓存复用。同时，速度大小 $V_i(t)$ 本身也反映了令牌的活跃程度。

实验可视化和定量消融均证实（Figure 2, Table 4）：速度场和加速度场的时空演化同样遵循三阶段稳定模式，且**联合使用速度和加速度**（通过归一化加权评分 $C_i(t) = \omega \cdot \mathrm{norm}(A_i(t)) + (1 - \omega) \cdot \mathrm{norm}(V_i(t))$，最佳权重 $\omega=0.7$）比单独使用任一指标获得更优的几何保真度。这验证了双重信号在区分稳定令牌与活跃令牌方面的互补性。

### 方法缺口与本文动机

综上，现有3D生成加速面临的核心矛盾是：**如何在大幅削减计算量的同时，保持几何结构的一致性？** 固定比例缓存策略无法适应去噪过程中动态变化的冗余程度——固定25%采样率导致CD从0.0686恶化至0.0956（Table 3）；而基于特征相似度的2D缓存方法则忽视了3D几何的拓扑约束。

Fast3Dcache的动机正是弥合这一缺口：利用体素稳定化的可预测三阶段模式来**动态调度缓存预算**（PCSC），并利用潜在特征的速度-加速度双重信号来**精确筛选可安全复用的令牌**（SSC），从而在不损害几何保真度的前提下实现训练无关的推理加速。

## 核心创新

Fast3Dcache 的核心创新在于首次将**几何感知缓存**引入 3D 扩散模型推理加速，其关键洞察是：去噪过程中体素占用的稳定化趋势呈现可预测的**三阶段模式**，且潜在特征的速度与加速度震荡可作为识别可安全缓存令牌的可靠信号。基于此，方法通过两个紧密耦合的模块——**PCSC**（动态缓存预算调度）与 **SSC**（时空稳定性令牌选择）——实现了在不损害几何保真度的前提下大幅跳过冗余计算。

### 从固定采样到几何感知动态调度：PCSC

现有缓存加速方法（如 **RAS** 的固定比例采样）直接移植到 3D 几何合成时，会因忽略体素结构的演化规律而导致严重的拓扑错误与结构伪影。Fast3Dcache 的核心突破在于将缓存配额的控制权从“固定比例”转变为“几何状态驱动”。

具体而言，PCSC 基于一个关键的实证发现（Figure 1）：去噪过程中动态体素数 $\Delta s_t$ 在第二阶段呈现稳定的**对数线性衰减**。PCSC 在第一阶段结束时，于锚点步测量实际体素变化量，校准对数线性模型 $\log(\Delta \hat{s}) = \mu \cdot t + \lambda$ 的斜率 $\mu$ 与截距 $\lambda$，随后外推得到每个时间步的预期动态体素数 $\Delta \hat{s}_t$。最终，通过映射因子 $\gamma_{up}$ 将预测的体素变化量转换为潜在特征令牌空间中的活跃计算需求，从而动态确定可缓存令牌配额 $c_t = D^3 - \Delta \hat{s}_t / \gamma_{up}$。

这一“预测-约束”机制使得缓存预算能够自适应地跟随几何结构的收敛速度：在结构剧烈变化的早期，预算收紧以保证精度；在几何趋于稳定的后期，预算放宽以最大化加速。消融实验（Table 3）有力地验证了这一设计的必要性——固定 25% 采样比例导致 F-Score 从 54.09 骤降至 34.51，而 PCSC 在相同加速水平下将 F-Score 维持在 54.09，CD 仅 0.0697。

### 从特征相似度到时空稳定性：SSC

确定缓存配额后，第二个关键问题是**选择哪些令牌进行缓存**。2D/视频方法通常依赖特征相似度或随机选择，但这些准则在 3D 潜在网格中无法准确反映几何结构的稳定性。

Fast3Dcache 提出 SSC，其核心思想是：**令牌的稳定性应同时由其变化速度（一阶）和变化加速度（二阶）来刻画**。具体地，SSC 计算每个令牌的速度大小 $V_i(t)$ 与加速度大小 $A_i(t)$（即 ICE，定义为 $\operatorname{ICE}_i(t) = ||\nu_i(t) - \nu_i(t-1)||_2$），经归一化后加权融合为缓存能力评分：

$$C_i(t) = \omega \cdot \mathrm{norm}(A_i(t)) + (1 - \omega) \cdot \mathrm{norm}(V_i(t))$$

评分越低表示令牌越稳定，SSC 据此选择最低分的 $c_t$ 个令牌进行缓存，仅对剩余活跃令牌执行完整的 Transformer 自注意力计算。

Table 4 的消融实验揭示了联合使用速度与加速度的必要性：仅用速度（$\omega=0$）时 CD 为 0.0739，仅用加速度（$\omega=1$）时 CD 为 0.0708，而联合使用（$\omega=0.7$）将 CD 进一步降至 0.0697。这表明速度与加速度捕捉了稳定性的不同维度——速度反映当前变化幅度，加速度则预警即将发生的突变，二者的互补使得 SSC 能更精确地识别真正稳定的几何区域。

### 三阶段策略与误差累积控制

PCSC 与 SSC 被嵌入一个精心设计的**三阶段推理策略**（Figure 3）：

- **Phase 1（全采样阶段）**：在去噪初期进行完整推理以建立几何基础，并在锚点步校准 PCSC 参数。
- **Phase 2（动态缓存阶段）**：由 PCSC 提供动态预算，SSC 筛选稳定令牌，仅对活跃令牌计算。为控制误差累积，每隔 $\tau$ 步执行一次强制全采样刷新。
- **Phase 3（CFG-Free 细化阶段）**：CFG 关闭后几何进入高度稳定状态，采用激进的固定高比例缓存 $\xi$，并按照 $f_{corr}$ 周期执行全校正步以保持几何对齐。

这一分段策略的合理性源于 Figure 1a 揭示的体素动态规律：Phase 1 对应体素剧烈变化的轮廓形成期，Phase 2 对应可预测的对数线性衰减期，Phase 3 对应 CFG 关闭后的极低变化期。Table 10 表明，Phase 3 的全校正步机制至关重要——$f_{corr}=3$ 时 FLOPs 为 115.4 T 且 CD 保持 0.0697，而无校正版本会导致几何质量显著退化。

### 与现有加速范式的本质差异

Fast3Dcache 与现有缓存加速方法存在根本性的设计哲学差异：

| 维度 | 2D/视频缓存方法（RAS, TeaCache） | Fast3Dcache |
|------|------|------|
| 缓存依据 | 特征相似度或模态无关的时序冗余 | 体素占用的几何稳定化趋势 |
| 调度策略 | 固定比例或步长无关的规则 | 对数线性模型驱动的动态预测 |
| 稳定性准则 | 单尺度特征变化 | 速度与加速度的联合时空分析 |

这种差异的直接后果是：**RAS** 在 25% 采样率下导致 F-Score 暴跌 26.53%，而 Fast3Dcache 在更高加速比下仅损失 1.95%（Table 1）。更重要的是，Fast3Dcache 与模态无关加速器 **TeaCache** 的组合可实现 3.41× 加速，且 CD 与 F-Score 均优于单独使用 TeaCache（Table 2），证明了几何感知缓存与通用缓存之间的互补性。

## 整体框架

Fast3Dcache 是一个无训练的几何感知缓存框架，其核心设计动机源于对 3D 扩散模型几何合成阶段计算冗余的重新审视。直接移植 2D/视频缓存方法到 3D 会破坏几何一致性，导致拓扑错误和结构伪影；Fast3Dcache 转而利用去噪过程中体素占用的内在稳定化规律来实现安全加速。

### 三阶段加速策略

如 Figure 3 所示，Fast3Dcache 将推理过程划分为三个策略性阶段，每个阶段承担不同的缓存角色：

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the Fast3Dcache three-stage acceleration strategy. Phase 1 (Full Sampling): The process begins with full sampling to establish initial geometric stability. At the end of this phase, the PCSC is calibrated by measuring voxel change (??) at the anchor step. Phase 2 (Dynamic Caching): In the main phase, the SSC identifies stable tokens for caching based on the dynamic budget predicted by PCSC. Only unstable tokens are processed by the FT. Phase 3 (CFG-Free Refinement): The final stage employs an aggressive fixed-ratio schedule. A high and fixed ratio ?? is used to determine the proportion of tokens to cache, maximizing computational savings during these stable refinement steps*

**Phase 1 — 全采样阶段。** 在去噪初期，几何结构处于快速成型期，动态体素数波动剧烈（见 Figure 1a），此时任何缓存行为都可能引入不可逆的几何偏差。因此 Phase 1 执行完整推理，不做任何令牌复用。该阶段的另一关键任务是在锚点步（anchor step）测量体素变化量，为 PCSC 模块提供校准所需的斜率和初始值，从而建立后续阶段的动态缓存预算预测基线。

**Phase 2 — 动态缓存阶段。** 这是加速的核心区间。去噪进入第二阶段后，体素占用变化呈现可预测的对数线性衰减趋势（Figure 1a 红色虚线）。PCSC 利用这一规律，在每个时间步根据预测的体素稳定化程度动态输出可缓存令牌配额 $c_t$；SSC 则联合计算每个令牌的速度大小 $V_i(t)$ 与加速度大小 $A_i(t)$（即 ICE），通过归一化加权评分 $C_i(t) = \omega \cdot \mathrm{norm}(A_i(t)) + (1-\omega) \cdot \mathrm{norm}(V_i(t))$ 筛选出最稳定的 $c_t$ 个令牌进行缓存复用，仅对活跃令牌子集执行 Transformer 自注意力计算。为防止缓存误差累积导致几何漂移，Phase 2 每隔 $\tau$ 步强制执行一次全采样刷新。

**Phase 3 — CFG-Free 细化阶段。** 当 Classifier-Free Guidance 关闭后，生成过程进入高度稳定状态（Figure 1a 第三阶段），动态体素数降至极低水平。此时 Fast3Dcache 切换为激进的固定高比例缓存策略（比例 $\xi$），继续使用 SSC 选择稳定令牌，并按照 $f_{corr}$ 周期执行全校正步以保持几何对齐。这一阶段在几乎不损失质量的前提下最大化计算节省。

### 模块间的数据流与协作

三个核心模块的协作关系如下：

1. **PCSC（Predictive Caching Scheduler Constraint）** 作为调度层，在每个时间步输出全局缓存预算 $c_t$。它从 Phase 1 末尾的锚点步获取校准参数（斜率 $\mu$ 和初始值），通过公式 $\Delta \hat{s} = \sigma \cdot e^{\mu \cdot (t - \lceil T \cdot \rho_a \rceil)}$ 外推当前步的预期动态体素数，再经 $c_t = D^3 - \Delta \hat{s}_t / \gamma_{up}$ 映射为令牌空间的可缓存数量。PCSC 的输入仅依赖体素占用的宏观统计，不涉及潜在特征计算，因此调度开销可忽略。

2. **SSC（Spatiotemporal Stability Criterion）** 作为选择层，接收 PCSC 输出的配额 $c_t$，在潜在特征网格 $S_t$ 上逐令牌计算稳定性评分，选出评分最低（即最稳定）的 $c_t$ 个令牌进行缓存。SSC 同时利用速度大小（衡量令牌当前变化幅度）和加速度大小（衡量变化趋势的稳定性），弥补了单一指标的不足——消融实验表明，联合使用两者（$\omega=0.7$）比单独使用速度或加速度获得更好的几何保真度。

3. **Phase 管理逻辑** 控制三阶段切换与误差校正：Phase 1 到 Phase 2 的切换由预设的时间比例 $\rho_a$ 决定；Phase 2 内部的 $\tau$ 步刷新和 Phase 3 的 $f_{corr}$ 全校正共同构成误差累积控制机制。

### 与外部加速器的兼容性

Fast3Dcache 专注于几何感知的令牌级缓存，与模态无关的加速方法（如 TeaCache）作用于不同的冗余维度。实验表明，将两者结合可在 TRELLIS 上实现 **3.41× 加速**，且 Chamfer Distance 和 F-Score 均优于单独使用 TeaCache（Table 2），验证了框架的即插即用兼容性。

## 核心模块与公式推导

### 问题建模：3D几何合成中的冗余发现

Fast3Dcache 的核心洞察来自对TRELLIS框架中3D扩散去噪过程的实证分析。在几何合成阶段，模型通过迭代修正一个潜在特征网格 $S_t$ 来逐步生成稀疏体素结构。研究发现，这一过程存在两种互补的冗余形式：

1. **体素占用的三阶段稳定化模式**：相邻时间步之间发生状态翻转的体素数量——即动态体素数 $\Delta s_t$——呈现出可预测的衰减规律（Figure 1a）。
2. **潜在特征的时间稳定性差异**：不同空间位置的潜在特征更新速度存在显著异质性，部分令牌在去噪中后期已高度稳定，无需逐步重新计算。

这两类冗余共同构成了缓存加速的理论基础：如果能够预测何时、何地可以安全地复用历史计算结果，就能在不损害几何保真度的前提下大幅减少冗余计算。

### 关键观测量的形式化定义

**动态体素数（Dynamic Voxels）** 量化了相邻时间步之间几何结构的变化幅度：

$$\Delta s_t = \sum_{i,j,k} \left( O_{t+1}(i,j,k) \oplus O_t(i,j,k) \right) \tag{Eq. 1}$$

其中 $O_t(i,j,k) \in \{0,1\}$ 表示时间步 $t$ 时体素 $(i,j,k)$ 的占用状态，$\oplus$ 为异或运算。该指标直接反映了去噪过程中几何结构的收敛速度。

**瞬时缓存误差（Instantaneous Caching Error, ICE）** 衡量了令牌级潜在特征的更新剧烈程度，定义为加速度大小：

$$\operatorname{ICE}_i(t) \triangleq A_i(t) = ||\nu_i(t) - \nu_i(t-1)||_2 \tag{Eq. 2}$$

其中 $\nu_i(t)$ 为令牌 $i$ 在时间步 $t$ 的速度向量（即潜在特征的一阶差分）。$A_i(t)$ 越大，表示该令牌的特征变化越剧烈，缓存该令牌引入的近似误差也越大。类似地，速度大小 $V_i(t) = ||\nu_i(t)||_2$ 则反映了令牌当前更新的绝对强度。

### PCSC：预测性缓存调度约束

**设计动机**：Figure 1a 揭示了体素稳定化的三阶段模式——Phase 1 为剧烈波动的结构形成期，Phase 2 为对数线性衰减的稳定化期，Phase 3 为 CFG 关闭后的高度平稳期。Phase 2 中的衰减趋势可通过对数线性函数可靠近似：

$$\log(\Delta \hat{s}) = \mu \cdot t + \lambda \tag{Eq. 3}$$

**核心机制**：PCSC 在 Phase 1 结束时的锚点步 $t_a = \lceil T \cdot \rho_a \rceil$ 处校准模型参数，随后外推预测后续每个时间步的预期动态体素数：

$$\Delta \hat{s}_t = \sigma \cdot e^{\mu \cdot (t - t_a)} \tag{Eq. 4}$$

其中 $\sigma$ 为锚点步实测的动态体素数，$\mu$ 为衰减斜率（默认为 -0.07）。最后，将预测的动态体素数映射到潜在特征令牌空间，得到可缓存的令牌配额：

$$c_t = D^3 - \frac{\Delta \hat{s}_t}{\gamma_{up}} \tag{Eq. 5}$$

其中 $D^3$ 为潜在特征网格的总令牌数，$\gamma_{up}$ 为体素到令牌的缩放因子。该公式的核心逻辑是：预测的体素变化越小，可安全缓存的令牌越多，从而在几何稳定期自动提高缓存比例。

### SSC：时空稳定性准则

**设计动机**：即使确定了每步的缓存预算 $c_t$，仍需解决“缓存哪些令牌”的选择问题。Figure 2 显示，速度大小和加速度大小在空间上的分布随时间演化，且均呈现与体素稳定化一致的三阶段衰减模式。单独使用任一指标均不足以精确区分稳定与活跃令牌（Table 4 消融实验证实了这一点）。

**核心机制**：SSC 联合归一化后的加速度大小和速度大小，计算每个令牌的缓存能力评分：

$$C_i(t) = \omega \cdot \mathrm{norm}(A_i(t)) + (1 - \omega) \cdot \mathrm{norm}(V_i(t)) \tag{Eq. 6}$$

其中归一化函数将各指标映射到 $[0,1]$ 区间：

$$\mathrm{norm}(A_i(t)) = \frac{A_i(t) - \min_j A_j(t)}{\max_j A_j(t) - \min_j A_j(t)} \tag{Eq. 7}$$

$$\mathrm{norm}(V_i(t)) = \frac{V_i(t) - \min_j V_j(t)}{\max_j V_j(t) - \min_j V_j(t)}$$

$\omega = 0.7$ 为加权系数（Table 4 消融确定的最优值）。评分 $C_i(t)$ 越低，表示令牌越稳定，越适合被缓存。SSC 按评分升序排列所有令牌，选取前 $c_t$ 个作为缓存令牌，仅对剩余活跃令牌执行 Transformer 自注意力计算。

### 三阶段加速策略

Fast3Dcache 将推理过程划分为三个策略阶段（Figure 3）：

- **Phase 1（全采样阶段）**：前 $\rho_a$ 比例的时间步执行完整推理，建立初始几何基础；在锚点步校准 PCSC 的 $\sigma$ 和 $\mu$ 参数。
- **Phase 2（动态缓存阶段）**：PCSC 提供每步动态缓存预算，SSC 筛选稳定令牌；每隔 $\tau$ 步（默认 $\tau=8$）执行一次全采样刷新以消除误差累积。
- **Phase 3（CFG-Free 细化阶段）**：CFG 关闭后采用固定高比例缓存 $\xi$，继续使用 SSC 选择令牌，并按照 $f_{corr}$ 周期（默认 $f_{corr}=3$）进行全校正以保持几何对齐。

此外，为优化时间步分配，采用非均匀时间调度将更多步数集中在 CFG 激活的早期阶段：

$$t = \frac{\eta \cdot t_{\ell}}{1 + (\eta - 1) \cdot t_{\ell}} \tag{Eq. 8}$$

其中 $\eta=3$ 为偏移因子，$t_{\ell}$ 为均匀时间步。

### 补充图表

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/001_Figure_1.jpg]]
*Figure 1: Observed voxel stabilization trend and the PCSC motivation. (a) The Original curve plots the empirically observed number of dynamic voxels (log-scale) per inference step, revealing a distinct three-phase pattern. (b) The PCSC curve illustrates our approach, motivated by this observation. We identify that the decay in Phase 2 can be reliably approximated by a log-linear function (red dashed line). This predictability forms the foundation for our scheduler, which we calibrate at an anchor step to forecast the stabilization budget*

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of velocity field and acceleration field feature maps in*

## 实验与分析

### 主要结果：TRELLIS 与 DSO 框架上的加速与保真度权衡

Fast3Dcache 在 TRELLIS 和 DSO 两个 3D 生成框架上进行了系统评估。评估采用 Toys4K 数据集的 71 个物体、852 个有效图像提示，所有实验在单张 NVIDIA GeForce RTX 4090 GPU 上运行，默认启用 FlashAttention，生成的 mesh 归一化到单位立方体并使用 ICP 对齐 ground truth。

**Table 1** 展示了核心量化对比。在 TRELLIS 框架上，Fast3Dcache（τ=8）实现了 **0.6426 iters/s 的吞吐量**，较 Vanilla TRELLIS（0.5055 iters/s）提升 **27.12%**；FLOPs 从 244.2 T 降至 110.3 T，降低 **54.83%**。几何保真度方面，Chamfer Distance 仅从 0.0686 轻微上升至 0.0703（+2.48%），F-Score 从 54.8244 降至 53.7528（-1.95%）。在 DSO 框架上，Fast3Dcache（τ=8）实现吞吐量 +16.45%、FLOPs -52.74%，CD +2.47%、F-Score -2.35%。当 τ=5 时，TRELLIS 上的吞吐量进一步提升至 0.6344 iters/s（+25.50%），FLOPs 降至 121.3 T（-50.33%），CD 和 F-Score 仅轻微变化。

作为对比，直接将 2D 模态感知缓存方法 **RAS** 适配到 3D 场景会导致严重的几何退化。RAS 在 25% 采样比例下，F-Score 从 54.8244 骤降至 40.2769（-26.53%），CD 从 0.0686 恶化至 0.0956。这一对比揭示了 3D 几何合成中的缓存策略必须考虑空间结构一致性，简单的令牌丢弃或固定比例采样会破坏几何完整性。**Figure 4** 的可视化对比进一步印证了这一结论：RAS 生成的 mesh 出现明显的几何伪影和表面噪声，而 Fast3Dcache 保持了与原始 TRELLIS 相当的结构保真度。

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/008_Figure_4.jpg]]
*Figure 4: Visualization comparison of 3D geometry synthesis. The leftmost column presents the input image. Subsequent columns display 3D meshes generated by TRELLIS, RAS method (at varying sampling ratios). Observe that while RAS introduces noticeable geometric artifacts and surface noise, Fast3Dcache preserves structural fidelity comparable to the original TRELLIS framework, achieving acceleration without compromising quality*

### 与模态无关加速器的互补性

**Table 2** 展示了 Fast3Dcache 与模态无关加速器 **TeaCache** 的协同效果。将两者结合后，在 TRELLIS 上实现了 **3.41× 加速**，同时 CD 降至 0.0701、F-Score 达到 53.9420，两项几何指标均优于单独使用 TeaCache。这一结果表明，Fast3Dcache 的几何感知缓存与 TeaCache 的特征层缓存作用于不同冗余维度，可叠加产生更优的加速-质量 Pareto 前沿。

### 消融实验：PCSC 动态调度的有效性

**Table 3** 对 PCSC 模块进行了消融。固定比例采样策略（25%、12.5%）导致严重的几何退化：25% 固定比例下 CD 恶化至 0.0956、F-Score 降至 34.51；12.5% 固定比例下 CD 进一步恶化至 0.1115、F-Score 仅 21.79。相比之下，PCSC 自适应调度（最佳斜率 μ=-0.07）获得 CD 0.0697、F-Score 54.0900，与全采样基线（CD 0.0686、F-Score 54.8244）极为接近。

衰减斜率 μ 的敏感性分析表明，μ 的选择对几何质量有显著影响。μ=-0.07 为最优值，偏离该值会导致 CD 和 F-Score 的退化。这一发现验证了 PCSC 对数线性模型对体素稳定化趋势的准确建模能力——第二阶段动态体素数量的衰减可被可靠近似，从而为每步缓存预算提供精确预测。

### 消融实验：SSC 联合判据的必要性

**Table 4** 对 SSC 模块的评分机制进行了消融。单独使用速度大小（velocity only）时 CD 为 0.0739；单独使用加速度大小（acceleration only）时 CD 为 0.0708。联合使用两者（ω=0.7）获得最优 CD 0.0697 和 F-Score 54.0900。这一结果揭示了潜在特征网格中速度与加速度携带互补信息：速度反映当前变化幅度，加速度反映变化的不稳定程度，仅依赖单一指标无法全面区分稳定令牌与活跃令牌。

### Phase 3 校正策略与超参数分析

Phase 3（CFG-Free 细化阶段）采用固定高比例缓存以最大化计算节省，但需周期性全校正以控制误差累积。**Table 10** 显示，全校正步频率 f_corr=3 在 FLOPs 115.4 T 下保持 CD 0.0697、F-Score 54.0900，大幅优于无校正版本。固定缓存比例 ξ 的消融（**Table 9**）表明，过高的 ξ 会导致几何对齐丢失，需要在校正频率和缓存比例之间取得平衡。

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/017_Table_10.jpg]]
*Table 10: Ablation study of the hyperparameter*

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/016_Table_9.jpg]]
*Table 9: Ablation study of the hyperparameter ??. CD of*

刷新间隔 τ 的敏感性分析（**Table 11**）显示，τ 可有效权衡速度与质量：τ=5 时吞吐量进一步提升至 0.6344 iters/s，CD 和 F-Score 仅有轻微变化；增大 τ 会逐步增加几何退化风险，但整体退化幅度可控。

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/014_Table_11.jpg]]
*Table 11: Hyperparameter analysis of ?? (left) and ?? (right)*

### 数据驱动参数选择与跨数据集泛化

**Figure 5** 展示了 Toys4K 和 OmniObject3D 数据集上斜率 μ 的分布及对数衰减趋势。通过对 100 个采样实例进行 RANSAC 拟合获得中位 μ 值作为数据驱动参数。**Table 8** 的量化结果表明，数据驱动参数选择策略在两个数据集上均能保持与手动调参相当的几何保真度，验证了 PCSC 对数线性模型的跨数据集普适性。

**Table 6** 和 **Table 7** 分别展示了文本到 3D（TRELLIS-text-xlarge）和 OmniObject3D 数据集上的图像到 3D 生成结果，Fast3Dcache 在这些设置下同样保持了加速与保真度的良好权衡。

### 反直觉发现：更高计算量未必带来更好质量

**Figure 8** 揭示了一个反直觉现象：采样比例与几何质量并非单调正相关。采样比例为 0.3 时获得的 CD 低于 0.4 时的 CD，表明在扩散去噪的特定阶段，过多的计算介入反而可能引入扰动。这一发现为缓存策略的设计提供了深层启示——加速的目标不仅是“少算”，更是“在正确的时机算正确的东西”，PCSC 的动态调度正是基于这一洞察。

### 补充图表

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on TRELLIS [64] and DSO [20] frameworks. We benchmark Fast3Dcache against TRELLIS and existing modality-aware method (RAS [30]). Our method consistently outperforms the baseline, achieving higher throughput and lower FLOPs while preserving geometric fidelity (CD and F-Score) across various settings. (best and second-best)*

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/006_Table_2.jpg]]
*Table 2: Results of Fast3Dcache combined with a modalityagnostic SOTA method. Integrating our method with the modality-agnostic acceleration framework TeaCache yields further speedup while also improving reconstruction quality*

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/007_Table_3.jpg]]
*Table 3: Ablation study of the PCSC module. We evaluate the effectiveness of our adaptive scheduler compared to fixed-rate sampling methods. Additionally, we analyze the sensitivity of the decay slope ??, demonstrating that optimal slope calibration is essential for preserving generation quality*

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/009_Table_4.jpg]]
*Table 4: Ablation study of the SSC module. We evaluate the individual contributions of the velocity (????) and acceleration (????) components. The results demonstrate that relying on a single metric is insufficient, while the joint consideration of both fields yields better geometric fidelity*

![[assets/figures/papers/paper_list_l2486_https_arxiv_org_abs_2511_22533/figures/010_Table_6.jpg]]
*Table 6: Results of text-to-3D on TRELLIS-text-xlarge*

## 方法谱系与知识库定位

### 核心定位：3D扩散模型的几何感知缓存加速

Fast3Dcache 是一个**无训练（training-free）的几何感知缓存框架**，专为3D扩散模型的几何合成阶段设计。其核心定位区别于两类现有加速方法：

1. **模态无关的通用缓存方法**：如 **TeaCache**（Liu et al., 2024）、**PAB**（Zhao et al., 2024）等，它们通过特征相似度或注意力冗余来跳过Transformer层计算，但直接移植到3D生成会忽略几何结构特有的时空一致性约束，导致拓扑错误和表面伪影。

2. **2D/视频DiT的模态感知缓存方法**：如 **RAS**（Zhou et al., 2024），虽然考虑了模态特性，但其稳定性准则基于2D特征统计，无法感知3D体素网格中几何结构的演化规律。实验表明，RAS在25%采样率下导致F-Score下降26.53%（Table 1），而Fast3Dcache仅下降1.95%。

Fast3Dcache的关键突破在于**将几何合成的物理过程建模为可预测的体素稳定化趋势**，并据此设计了两级缓存控制机制：宏观层面的**PCSC**（Predictive Caching Scheduler Constraint）通过体素变化的对数线性衰减预测动态缓存预算；微观层面的**SSC**（Spatiotemporal Stability Criterion）利用潜在特征的速度和加速度震荡来识别可安全复用的稳定令牌。

### 方法谱系中的位置

#### 上游基础：TRELLIS框架的结构生成阶段

Fast3Dcache 直接作用于 **TRELLIS**（Xiang et al., 2024）及其物理引导变体 **DSO**（Liu et al., 2024）的稀疏结构生成阶段。该阶段通过迭代修正潜在特征网格 $S_t \in \mathbb{R}^{D \times D \times D \times C}$ 来合成3D几何，核心计算瓶颈在于Transformer自注意力层对全部 $D^3$ 个令牌的全量计算。Fast3Dcache 不修改模型架构或权重，仅改变每步参与计算的令牌子集，因此保持了与原始框架的完全兼容。

#### 并行/互补关系：与TeaCache的协同

Fast3Dcache 与模态无关加速器 **TeaCache** 存在明确的互补性：前者在**空间维度**上通过几何稳定性筛选令牌，后者在**层维度**上通过特征残差跳过Transformer块。实验证实，两者结合可实现 **3.41× 加速**（Table 2），且联合使用时的CD（0.0701）和F-Score（53.9420）均优于单独使用TeaCache，说明几何感知缓存与层间缓存存在正交的冗余空间。

#### 与采样调度器的关系

Fast3Dcache 采用了非均匀时间调度策略 $t = \frac{\eta \cdot t_{\ell}}{1 + (\eta - 1) \cdot t_{\ell}}$（Eq. 8），通过偏移因子 $\eta$ 将更多步数集中在CFG激活的早期阶段。这与 **DPM-Solver++**（Lu et al., 2022）等高级ODE求解器的思路不同——后者通过数值方法减少总步数，而Fast3Dcache在固定步数内减少单步计算量。理论上两者可叠加，但需要重新校准PCSC的衰减斜率 $\mu$。

### 适用边界与限制

#### 表示形式的约束

当前实现针对 **稀疏体素网格** 表示进行优化。PCSC的体素动态计数 $\Delta s_t = \sum_{i,j,k} (O_{t+1}(i,j,k) \oplus O_t(i,j,k))$ 和SSC的速度/加速度场计算都依赖于规则网格结构。将其直接应用于连续隐式表示（如SDF、NeRF）需要重新定义"几何变化"的度量方式，这是论文明确指出的开放问题。

#### 生成阶段的边界

加速仅覆盖 **几何合成阶段**（sparse structure generation），不涉及后续的纹理生成阶段（SLAT）。两阶段之间的联合加速——例如利用几何阶段的稳定性信息指导纹理阶段的缓存策略——是论文提及但未解决的研究方向。

#### 超参数的配置敏感性

默认超参数针对特定采样器配置标定：$\eta=3$，CFG区间 $t \in [0.5, 1]$。Figure 7的消融显示，当CFG全程激活（$t \in [0, 1]$）时，体素动态曲线中的"急剧下降"现象消失，这会影响Phase 3的划分边界和固定缓存比例 $\xi$ 的设置。使用定制调度器时需要重新进行数据驱动的参数选择（Figure 5展示了通过RANSAC在100个采样实例上估计中位数 $\mu$ 的流程）。

#### 硬件与评估的公平性说明

所有实验在单张NVIDIA GeForce RTX 4090 GPU上运行，默认启用FlashAttention。评估采用Toys4K数据集的71个物体、852个有效图像提示，生成的mesh均归一化到单位立方体并使用ICP对齐ground truth。这些条件确保了与TRELLIS基线对比的公平性，但也意味着性能提升数据在其他GPU或数据集上的可迁移性需要独立验证。

### 开放问题与后续方向

1. **跨表示泛化**：如何将几何感知缓存范型扩展到连续隐式表示（SDF、NeRF、3D Gaussian Splatting）？这需要设计表示无关的稳定性准则，而非依赖体素占用的离散变化。

2. **端到端联合加速**：能否在统一框架中同时处理几何和纹理约束？当前两阶段流水线中，纹理阶段（SLAT）的潜在特征演化是否呈现类似的稳定化模式，是值得探索的问题。

3. **参数自动化的鲁棒性**：Figure 5展示了数据驱动的 $\mu$ 选择方法，但Table 11显示 $\mu$ 在 -0.05 到 -0.09 区间内CD变化约0.002。如何在不牺牲鲁棒性的前提下完全消除手动调参，尤其是在跨数据集迁移时（Table 7显示OmniObject3D上的结果），仍需进一步研究。

4. **与高级采样器的协同**：PCSC的预测依赖于固定步数的体素衰减规律。若结合DPM-Solver++等自适应步长求解器，体素动态曲线的形状可能改变，需要重新验证对数线性近似的有效性。

5. **误差累积的理论分析**：Phase 2中每 $\tau$ 步强制全采样的刷新策略（$\tau=8$ 为默认值）是基于经验观察的工程方案。Table 11显示 $\tau=5$ 可进一步加速但CD轻微上升，缺乏对误差传播上界的理论刻画。

## 原文 PDF

![[paperPDFs/CVPR_2026/Fast3Dcache_Training_free_3D_Geometry_Synthesis_Acceleration.pdf]]
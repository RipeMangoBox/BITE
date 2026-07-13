---
title: "Locality-aware Parallel Decoding for Efficient Autoregressive Image Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Locality_aware_Parallel_Decoding_for_Efficient_Autoregressive_Image_Generation.pdf
project_link: null
code_link: https://github.com/mit-han-lab/lpd
openreview_forum_id: h06l9w1clt
aliases:
- LLAPD
- LAPDEAIG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "并行生成步数（每步预测的token组大小）与生成质量之间的权衡：减少步数可降低延迟，但组内token间的相互依赖会导致生成质量下降。"
primary_logic: "将上下文提供与token生成解耦，使用可学习位置查询token（position query tokens）指导目标位置的并行生成，并通过专用的注意力掩码保证并行token的相互可见性；同时利用图像生成中强烈的空间局部性，设计局部感知的生成顺序调度，在每一步优先选择靠近已生成token（最大化上下文支持）且远离同组其他token（最小化组内依赖）的位置，从而在将生成步数大幅减少（如256→20）的同时维持图像质量。"
claims:
- "提出的灵活并行自回归建模将生成步数从256减少到20（256×256分辨率），且FID仅2.10，与光栅顺序基线（FID 2.12, 256步）质量相当，但延迟降低约12.9倍。"
- "在512×512分辨率上，生成步数从1024减少到48，LPD-L达到与1024步光栅基线相同的FID 2.54，延迟从14.25s降至0.69s。"
- "局部感知生成顺序调度显著优于随机顺序和Halton顺序，在XL模型32步设置下，结合两个局部性原则的FID为1.92，而随机顺序为2.11。"
- "LLaMaGen模型中注意力权重随空间距离急剧下降，证明了图像生成中的强空间局部性，为局部感知调度提供了动机。"
---

# Locality-aware Parallel Decoding for Efficient Autoregressive Image Generation

> [!tip] 核心洞察
> 将上下文提供与token生成解耦，使用可学习位置查询token（position query tokens）指导目标位置的并行生成，并通过专用的注意力掩码保证并行token的相互可见性；同时利用图像生成中强烈的空间局部性，设计局部感知的生成顺序调度，在每一步优先选择靠近已生成token（最大化上下文支持）且远离同组其他token（最小化组内依赖）的位置，从而在将生成步数大幅减少（如256→20）的同时维持图像质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 局部感知并行解码的高效自回归图像生成 |
| 英文题名 | Locality-aware Parallel Decoding for Efficient Autoregressive Image Generation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=h06l9w1clt) · [GitHub](https://github.com/mit-han-lab/lpd) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | LPD (Locality-aware Parallel Decoding) |
| Dataset | ImageNet 256×256 class-conditional, ImageNet 512×512 class-conditional, GenEval 1024×1024 text-to-image |

> [!tip] 效果简介
> - ImageNet 256×256 class-conditional 上，FID↓ / IS↑ / #Steps / Latency(s)↓ / Throughput(img/s)↑ 为 LPD-XL: FID 2.10, IS 326.7, 20 steps, latency 0.41s, throughput 75.20，对比 Raster Counterpart-XL: FID 2.12, IS 307.4, 256 steps, latency 5.29s, throughput 12.31，变化 FID -0.02, steps 12.8× reduction, latency ~12.9× lower, throughput ~6.1× higher。
> - ImageNet 512×512 class-conditional 上，FID↓ / IS↑ / #Steps / Latency(s)↓ / Throughput(img/s)↑ 为 LPD-L: FID 2.54, IS 292.2, 48 steps, latency 0.69s, throughput 35.16，对比 Raster Counterpart-L: FID 2.54, IS 278.5, 1024 steps, latency 14.25s, throughput 3.79，变化 FID unchanged, steps 21.3× reduction, latency ~20.7× lower, throughput ~9.3× higher。
> - GenEval 1024×1024 text-to-image 上，Overall GenEval score / #Steps 为 LPD-XL: 0.62, 64 steps，对比 Raster Counterpart-XL: 0.60, 4096 steps，变化 Score +0.02, steps 64× reduction。

## 概要

传统自回归图像生成模型将图像序列化为token序列，按光栅顺序逐token预测，每次仅生成一个token。这种逐token生成模式形成**内存受限的工作负载**，导致生成步数多、延迟高，难以在保持高吞吐的同时实现低延迟。例如，在256×256分辨率下需256步，512×512分辨率下需1024步。

本文提出**LPD（Locality-aware Parallel Decoding）**，通过两个核心机制突破上述瓶颈：

1. **灵活并行自回归建模**：将上下文提供与token生成解耦，使用可学习的位置查询token（position query tokens）指导目标位置的并行生成，并通过专用注意力掩码保证并行token的相互可见性，实现任意顺序和任意并行度的解码。
2. **局部感知生成顺序调度**：利用图像生成中强烈的空间局部性（注意力权重随空间距离急剧下降），在每一步优先选择靠近已生成token（最大化上下文支持）且远离同组其他token（最小化组内依赖）的位置，从而在将生成步数大幅减少的同时维持图像质量。

**核心结论**：LPD在256×256分辨率上将生成步数从256降至20，FID仅2.10，与光栅顺序基线（FID 2.12，256步）质量相当，但延迟降低约12.9倍；在512×512分辨率上将生成步数从1024降至48，FID保持2.54不变，延迟从14.25s降至0.69s。在内存受限的小批次推理场景下，LPD实现比光栅顺序约12倍的更高吞吐。

**方法定位**：LPD属于并行化自回归生成方法，区别于固定区域并行的PAR、随机顺序+位置指令token的RandAR、编码器-解码器交叉注意力的ARPG等方案。其关键差异在于：通过解耦上下文与生成的角色，避免了RandAR中因果掩码将并行生成退化为批量逐token预测的问题，且仅缓存已生成token而不缓存指令token，节省了KV缓存内存。



自回归（Autoregressive, AR）模型在语言生成领域取得了巨大成功，其核心范式——将联合分布按序列分解为条件概率的乘积——也被自然地迁移到图像生成任务中。标准自回归图像生成将图像编码为离散token序列，并按照固定的光栅顺序（raster order）逐token预测：

$$p ( x _ { 1 } , x _ { 2 } , . . . , x _ { N } ; c ) = \prod _ { n = 1 } ^ { N } p ( x _ { n } | x _ { < n } ; c )$$

这种逐token的生成方式虽然建模精确，但带来了根本性的效率瓶颈：每次模型前向仅生成一个token，整个生成过程需要与图像分辨率平方成正比的步数（如256×256分辨率需256步，512×512需1024步）。在内存受限的推理场景下，这一瓶颈尤为突出——每一步的计算量不足以充分利用GPU的并行能力，导致生成延迟高、吞吐量低。

### 并行化解码的探索与困境

为突破逐token生成的效率限制，研究者尝试了多种并行化策略。这些方法的核心思想是将序列分组，以组为单位进行并行预测：

$$p ( x _ { 1 } , x _ { 2 } , \ldots , x _ { N } ; c ) = \prod _ { g = 1 } ^ { G } p ( X _ { g } \mid X _ { < g } ; c )$$

其中每组$X_g$包含多个token，组内token被联合预测，组间保持条件依赖。通过将$G$设置为远小于$N$的值，可大幅减少生成步数。

然而，现有并行化方法面临一个核心权衡：减少步数会加剧组内token间的相互依赖问题，导致生成质量下降。具体而言：

- **编码器-解码器方法**（如**ARPG**、**SAR**）：通过交叉注意力机制实现token间的独立生成，但查询token不贡献键值对，限制了上下文建模能力。
- **纯解码器方法**（如**RandAR**）：使用位置指令token引导生成，但因果注意力掩码将并行生成退化为批量化的逐token预测，且指令token需被缓存，使内存占用翻倍。

这些方法的共同缺陷在于，它们未能从根本上解耦“提供上下文”与“执行生成”这两个角色——在标准自回归中，每个token同时承担这两项职责，限制了架构的灵活性和并行效率。

### 空间局部性：被忽视的关键线索

本文通过分析**LlamaGen**模型的注意力图，揭示了一个关键现象：图像生成中存在强烈的空间局部性。定量分析显示，解码token的注意力高度集中于空间上邻近的token，且注意力权重随空间距离急剧衰减。这一发现为并行解码策略提供了重要启示：并非所有已生成token对当前预测同等重要，空间邻近的token提供了最主要的上下文支持。

### 本文动机与核心思路

基于上述观察，本文提出**LPD（Locality-aware Parallel Decoding）**，从两个层面解决并行解码的效率-质量权衡：

1. **灵活并行自回归建模**：将上下文提供与token生成解耦——已生成token仅提供上下文，而可学习的位置查询token（position query tokens）驱动目标位置的并行生成。专用注意力掩码保证并行token间的相互可见性，实现真正的联合预测。

2. **局部感知生成顺序调度**：利用空间局部性，在每一步优先选择靠近已生成token（最大化上下文支持）且远离同组其他token（最小化组内依赖）的位置。这一调度策略使模型在将生成步数从256大幅压缩至20（256×256）的同时，维持与光栅顺序基线相当的图像质量。



## 核心方法与创新机理

LPD 的核心创新在于对自回归图像生成的两个关键维度进行了根本性重构：**生成架构**和**生成顺序调度**。传统自回归模型（如 **LlamaGen**）采用固定光栅顺序逐 patch 预测，每个 token 同时承担"提供上下文"和"预测下一 token"双重角色，导致生成步数多、延迟高，且无法灵活并行。LPD 通过两个 changed slots 系统性地解决了这一瓶颈。

### 创新一：灵活并行自回归建模（架构解耦）

**基线做法**：标准 decoder-only 架构使用因果注意力掩码，每个 token 按光栅顺序依次生成，token 既是上下文载体又是预测目标。这种耦合限制了并行化程度和生成顺序的灵活性。

**LPD 做法**：将"上下文提供"与"token 生成"两个角色彻底解耦（Figure 3）。具体而言：
- **已生成的图像 token** 仅负责提供上下文信息，通过 KV 缓存持续更新。
- **可学习位置查询 token**（Position Query Tokens）驱动目标位置的并行生成：将目标位置的位置嵌入与共享可学习嵌入相加，形成引导特定位置生成的位置查询 token。

训练时采用专用注意力掩码（Figure 4），包含两种注意力模式：
- **Context Attention**：允许所有后续 token（包括位置查询 token）以因果方式关注已生成的图像 token，获取上下文支持。
- **Query Attention**：保证同一并行步内的位置查询 token 相互可见，实现联合预测；同时阻止后续 token 关注这些查询 token，避免信息泄露。

推理时，LPD 将已生成图像 token 的编码（更新 KV 缓存）与新 token 的解码融合为单次前向传播（Figure 5），避免步骤数加倍。与 **RandAR** 等 decoder-only 并行方法相比，LPD 的专用掩码确保了并行 token 间的相互可见性，而非退化为批处理的逐 token 预测；与 **ARPG** 等编码器-解码器方法相比，LPD 仅缓存生成的图像 token，避免了查询 token 带来的额外内存开销（Figure 6）。

### 创新二：局部感知生成顺序调度

**基线做法**：固定光栅顺序或纯随机顺序，未考虑图像生成中强烈的空间局部性，导致并行组内 token 间相互依赖强、上下文支持弱。

**LPD 做法**：基于对 **LlamaGen** 模型的注意力分析（Figure 7）——注意力权重随空间距离急剧下降，且此局部性在所有注意力头中一致存在——LPD 设计了局部感知的生成顺序调度算法（Algorithm 1），遵循两个原则：
1. **高邻近性**：优先选择靠近已生成 token 的位置，最大化上下文支持。
2. **低并发邻近性**：同一步内选中的 token 彼此远离，最小化组内相互依赖。

具体实现中，调度器通过邻近性排序、排斥阈值筛选和最远点采样，预计算每一步的生成位置。推理时直接使用预计算顺序，无额外延迟。该调度使得在生成步数从 256 大幅压缩至 20 时，同组 token 间的依赖最小化，上下文信息最大化，从而在极低步数下维持生成质量。

### 关键证据

- **架构有效性**：在 XL 模型上将步数从 256 降至 32 时，LPD 的 FID 几乎不变（~1.92），而 **ARPG** 和 **RandAR** 在相同步数下 FID 显著增加（Figure 9a），验证了灵活并行建模中相互可见性设计的必要性。
- **调度有效性**：在 32 步设置下，LPD 的局部感知调度（FID 1.92）显著优于随机顺序（FID 2.11）和 Halton 顺序（Figure 9b）。单独应用"高邻近性"原则将 FID 从 2.11 降至 2.00，单独应用"低并发邻近性"降至 2.06，两者结合降至 1.92（Figure 9c），证明两个原则具有互补增益。
- **系统级验证**：在 ImageNet 256×256 上，LPD-XL 以 20 步达到 FID 2.10，与 256 步光栅基线（FID 2.12）质量相当，但延迟降低约 12.9 倍（Table 1）。在 512×512 上，LPD-L 以 48 步达到与 1024 步光栅基线相同的 FID 2.54，延迟从 14.25s 降至 0.69s（Table 2）。

### 局限性提示

- 位置查询 token 引入额外计算开销：在计算受限的大批次推理场景下，加速比从内存受限场景的 ~12 倍下降至约 3 倍（Figure 14）。
- 生成顺序需根据分辨率和步数预先计算，无法在推理时根据内容动态调整。



LPD（Locality-aware Parallel Decoding）的整体框架围绕一个核心洞察展开：**将上下文提供与token生成解耦**，从而在保持自回归建模优势的同时实现高度并行解码。该框架由三个关键模块协同工作，形成一条从输入到输出的高效生成流水线。

### 输入与输出流

- **输入**：条件信息 $c$（如类别标签或文本描述）以及预定义的生成步数 $G$ 和每步并行生成的token数量。
- **输出**：完整的图像token序列 $x_1, x_2, \ldots, x_N$，通过分组并行自回归分解 $p(x_1, x_2, \ldots, x_N; c) = \prod_{g=1}^{G} p(X_g \mid X_{<g}; c)$ 逐步生成。

### 模块关系与流水线

整个生成过程由以下模块按序协作完成：

1. **局部感知顺序调度器（Locality-aware Order Scheduler）**
   - **角色**：在推理前预计算每一步要生成的token位置索引。
   - **机制**：基于两个局部性原则——**高邻近性**（靠近已生成token以获取强上下文支持）和**低并发邻近性**（同组token彼此远离以减少组内依赖）——通过邻近性排序、排斥阈值筛选和最远点采样（Algorithm 1）生成调度方案。
   - **特点**：完全离线预计算，推理时直接查表使用，不引入额外延迟。

2. **位置查询Token嵌入（Position Query Token Embedding）**
   - **角色**：将调度器指定的目标位置转化为可学习的查询向量，驱动并行生成。
   - **机制**：将目标位置的位置嵌入与共享的可学习嵌入相加，形成位置查询token。这些token不存储KV缓存，仅用于解码阶段指导对应位置的token预测。
   - **关键设计**：与标准自回归中每个token同时承担"上下文提供"和"下一token预测"双重角色不同，LPD将这两个角色分离——已生成的图像token负责提供上下文，位置查询token专门驱动目标位置的并行生成（Figure 3）。

3. **融合编码-解码注意力机制（Fused Encoding-Decoding Attention）**
   - **训练阶段**：采用专用的双模式注意力掩码（Figure 4）：
     - **Context Attention**：允许后续token以因果方式关注所有已生成的图像token，获取上下文信息。
     - **Query Attention**：保证同一并行步内的位置查询token相互可见，实现联合预测；同时阻止后续token关注这些查询token，避免信息泄露。
   - **推理阶段**：将已生成图像token的KV缓存更新（编码）与新token的解码融合为单个前向步骤（Figure 5），避免步骤数加倍。具体而言，每一步同时完成：将上一步生成的图像token编码入KV缓存，并利用位置查询token并行解码当前步的目标token。

### 核心工作流

1. 调度器预计算 $G$ 步的生成位置索引。
2. 初始步：以条件 $c$ 和起始token（如 [BOS]）为上下文，位置查询token嵌入模块生成第一批查询token，通过融合注意力机制并行预测第一组图像token $X_1$。
3. 后续步：将已生成的token序列 $X_{<g}$ 的KV缓存与新一批位置查询token一起送入融合注意力模块，并行预测 $X_g$。
4. 重复直至 $G$ 步完成，输出完整token序列并解码为图像。

### 与基线方法的架构差异

| 方法 | 上下文与生成关系 | 并行机制 | 缓存策略 |
|------|-----------------|---------|---------|
| 标准光栅自回归（Raster Counterpart） | 耦合：每个token同时提供上下文并预测下一token | 无并行，逐token预测 | 缓存所有已生成token |
| PAR / RandAR | 部分解耦：使用位置指令token | 固定区域并行或批量next-token预测 | 需缓存指令token，内存加倍 |
| ARPG | 编码器-解码器分离 | 查询token独立生成，无相互可见性 | 查询token不贡献KV |
| **LPD（本方法）** | **完全解耦**：图像token提供上下文，位置查询token驱动生成 | **灵活并行**：查询token相互可见，支持任意并行度 | **仅缓存生成token**，查询token不占用缓存 |

这一架构设计使得LPD在将生成步数从256压缩至20（256×256分辨率）时，仍能保持与光栅顺序基线相当的生成质量（FID 2.10 vs 2.12，Table 1），同时实现约12.9倍的延迟降低。



### 标准自回归与分组并行分解

传统自回归图像生成将图像token序列 $\{x_1, x_2, \ldots, x_N\}$ 的联合分布按光栅顺序分解为条件概率的乘积：

$$p(x_1, x_2, ..., x_N; c) = \prod_{n=1}^{N} p(x_n | x_{<n}; c) \tag{1}$$

其中 $c$ 为条件信息（如类别标签或文本），$x_{<n}$ 表示前 $n-1$ 个token。这一逐token预测范式导致生成步数等于token总数（如256×256分辨率需256步），形成严重的内存受限瓶颈。

LPD将序列划分为 $G$ 个组，每组内token被联合预测，组间保持条件依赖：

$$p(x_1, x_2, \ldots, x_N; c) = \prod_{g=1}^{G} p(X_g \mid X_{<g}; c) \tag{2}$$

其中 $X_g$ 为第 $g$ 步并行生成的一组token，$X_{<g}$ 为前 $g-1$ 步已生成的所有token。这一分解将生成步数从 $N$ 压缩至 $G$（如 $G=20$ 替代 $N=256$），但组内token间的相互依赖成为制约生成质量的核心因素。

### 位置查询Token与解耦架构

LPD的核心洞察是将“上下文提供”与“token生成”解耦：已生成的图像token仅负责提供上下文信息（通过KV缓存），而生成过程由可学习的位置查询token（Position Query Token）驱动。具体而言，对于第 $g$ 步要生成的每个目标位置，其位置嵌入与共享的可学习嵌入相加，形成位置查询token。该token通过注意力机制从已生成token中提取上下文，并直接预测对应位置的图像token。

训练时采用专用注意力掩码，包含两种注意力模式（Figure 4）：
- **Context Attention**：允许所有后续token（包括位置查询token）以因果方式关注已生成的图像token，提供上下文支持。
- **Query Attention**：保证同一并行步内的位置查询token相互可见，实现联合预测；同时阻止后续token关注这些查询token，防止信息泄露。

推理时，已生成图像token的KV缓存更新（编码）与新token的解码被融合为单个前向步骤（Figure 5），避免步数加倍。

### 空间局部性的量化

为量化图像生成中的空间局部性强度，引入每token注意力距离指标（Per-Token Attention, PTA）：

$$PTA_{s} = \frac{1}{N} \sum_{i=1}^{N} \frac{\sum_{j} \mathrm{Attention}(T_{i}, T_{j}) \cdot \mathbb{I}[d(T_{i}, T_{j}) = s]}{\sum_{j} \mathbb{I}[d(T_{i}, T_{j}) = s]} \tag{3}$$

其中 $T_i$、$T_j$ 为图像token，$d(T_i, T_j)$ 为它们在2D网格上的欧氏距离，$s$ 为目标距离。$PTA_s$ 衡量所有token对距离为 $s$ 的邻居的平均注意力权重。实验表明（Figure 7），PTA随距离急剧衰减，且这一局部性在所有注意力头中一致存在，为局部感知调度提供了经验基础。

### 局部感知生成顺序调度

调度算法（Algorithm 1）基于两个原则预计算每步的生成位置：
1. **高邻近性**：优先选择靠近已生成token的位置，以最大化上下文支持。
2. **低并发邻近性**：同组token彼此远离，以最小化组内依赖。

具体流程：对每个待选位置计算其到已选集合的逆欧氏距离作为邻近性度量；将满足邻近阈值 $\rho$ 且相互间距离超过排斥阈值 $\tau$ 的位置优先入队；当高邻近性池耗尽时，使用最远点采样填充剩余位置。调度结果在推理时直接查表使用，不引入额外延迟。



## 实验与关键发现

### 核心性能：步数压缩与质量保持

LPD在多个基准上实现了生成步数的数量级压缩，同时维持甚至略微提升生成质量，证明了灵活并行自回归建模与局部感知调度策略的有效性。

**ImageNet 256×256 类条件生成**（Table 1）：
- LPD-XL仅需**20步**即达到FID **2.10**、IS 326.7，而光栅顺序基线（Raster Counterpart-XL）需**256步**才达到FID 2.12、IS 307.4。步数压缩**12.8倍**，FID略优（-0.02），延迟从5.29s降至0.41s（约**12.9倍**加速），吞吐量从12.31 img/s提升至75.20 img/s（约**6.1倍**）。
- LPD-L在20步下FID为2.40，吞吐量达到139.11 img/s，展现了一致的小步数高质量特性。
- 与现有并行化自回归方法相比，LPD在FID-延迟权衡曲线上占据显著优势（Figure 1），延迟至少降低**3.4倍**。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/008_Table_1.jpg]]
*Table 1: System-level comparison on ImageNet 256×256 class-conditional generation. We evaluate the generation quality by metrics including Fréchet inception distance (FID), inception score (IS), precision and recall. #Steps is the number of model runs needed to generate an image. We measure latency with a batch size of 1 and throughput with a batch size of 64 on a single NVIDIA A100 GPU under BFloat16 precision, with classifier-free guidance (CFG) for both*

**ImageNet 512×512 类条件生成**（Table 2）：
- LPD-L以**48步**达到与1024步光栅基线完全相同的FID 2.54，步数压缩**21.3倍**，延迟从14.25s降至0.69s（约**20.7倍**加速），吞吐量从3.79 img/s提升至35.16 img/s（约**9.3倍**）。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/009_Table_2.jpg]]
*Table 2: System-level comparison on ImageNet 512×512 class-conditional generation. Metrics and evaluation setup are the same as in Table 1*

**GenEval 1024×1024 文本到图像生成**（Table 3）：
- LPD-XL仅需**64步**即达到Overall GenEval得分0.62，优于4096步光栅基线的0.60，步数压缩**64倍**，证明方法在大分辨率文本条件生成场景下同样有效。

### 消融实验：方法组件的独立贡献

所有消融实验均在ImageNet 256×256分辨率、XL模型尺寸下进行（Figure 9）。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/011_Figure_9.jpg]]
*Figure 9: Ablation Studies. All ablation experiments are conducted with XL size models on 256×256 resolution. (a) Effectiveness of flexible parallelized autoregressive modeling. (b) Effectiveness of locality-aware generation order schedule. (c) Effectiveness of the locality principles*

**灵活并行自回归建模的有效性**（Figure 9a）：
- 当生成步数从256降至32时，LPD的FID几乎不变（~1.92），而**ARPG**和**RandAR**在相同步数下FID显著增加。这验证了位置查询token与专用注意力掩码（Context Attention + Query Attention）设计在维持并行生成质量方面的关键作用——组内token的相互可见性保证了联合预测的一致性。

**局部感知生成顺序调度的有效性**（Figure 9b）：
- 在32步设置下，局部感知顺序的FID为**1.92**，显著优于随机顺序的**2.11**和Halton顺序。这证明基于空间局部性先验的调度策略能有效提升并行生成质量。

**两个局部性原则的独立贡献**（Figure 9c）：
- 随机顺序基线FID为2.11。
- 仅应用"高邻近性"原则（选择靠近已生成token的位置）：FID降至**2.00**。
- 仅应用"低并发邻近性"原则（使用最远点采样使同组token相互远离）：FID降至**2.06**。
- 结合两者：FID进一步降至**1.92**。

两个原则存在协同效应：高邻近性确保每步预测有充分的上下文支持，低并发邻近性减少组内token间的相互依赖冲突，二者互补地提升了并行生成质量。

### 敏感性分析：阈值参数的鲁棒性

对排斥阈值 $\tau$ 和邻近阈值 $\rho$ 的敏感性分析（Table 6）揭示了调度策略的稳健性：

- **排斥阈值 $\tau$**：无排斥（$\tau=0$）时FID为2.00；适当排斥（$\tau=2$）时FID最优为1.92；过大排斥（$\tau=4$）时FID回升至2.00。这表明适度的组内token分离至关重要，但过度排斥可能牺牲上下文质量。
- **邻近阈值 $\rho$**：在 $\rho=0$ 到 $\rho=1$ 范围内FID稳定在1.93~1.92，对参数不敏感；但 $\rho$ 过大时（$\rho=2$）FID恶化至2.04，说明过度放宽邻近约束会引入低质量上下文。

### 效率分析：内存受限场景的加速特性

在内存受限的小批次推理场景下（Figure 14），生成步数的减少几乎线性地转化为延迟降低。LPD在相同批次大小下实现比光栅顺序约**12倍**的更高吞吐量。即使在最大可行批次大小下（计算受限场景），LPD仍保持约**3倍**的吞吐量优势。额外的位置查询token引入了计算开销，这是大批次下加速比下降的主要原因。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/021_Figure_14.jpg]]
*Figure 14: Throughput vs. Batch Size on ImageNet 256×256 Class-Conditional Generation. For LPD, we use 20 generation steps. Raster refers to the traditional fixed-raster-order generation model. We progressively increase the batch size until the process runs out of memory. The throughput values on the y-axis are plotted on a logarithmic scale*

### 注意力局部性分析：调度策略的动机验证

对**LlamaGen**模型的注意力权重分析（Figure 7）为局部感知调度提供了实证基础：
- Per-Token Attention（PTA，Equation 3）随空间距离急剧下降，大部分注意力集中在局部邻域内（$s \leq 3$）。
- 该空间局部性在所有注意力头中一致观察到（Figure 7b），证明图像自回归生成中确实存在强烈的局部依赖模式，支持"靠近已生成token的位置获得更强上下文支持"这一核心假设。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/006_Figure_7.jpg]]
*Figure 7: Attention Analysis of LLAMAGEN. (a) Attention diminishes with distance (b) Spatial locality is consistently observed in all heads*

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of attention maps in the LLAMAGEN-1.4B model. There is strong spatial locality, as the attention of a decoding token is concentrated on nearby spatial tokens. LLAMAGEN encodes images into 24 × 24 tokens, where a token that is 24 positions earlier in the attention map corresponds to the token directly above it in the 2D grid*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/003_Figure_3.jpg]]
*Figure 3: Raster Order vs. Flexible Parallelized Autoregressive Modeling. (a) In raster order, each token simultaneously provides context and predicts the next token, restricting flexibility and efficiency. (b) Our approach decouples these roles: previously generated tokens supply context, while position query tokens drive parallel generation at arbitrary target positions. This separation enables both flexible order and efficient parallelization*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the training attention mask. Context Attention allows subsequent tokens to attend to the context tokens causally. Query Attention ensures mutual visibility among the position query tokens within the same step, and prevents any subsequent tokens from attending to the query tokens. For example, image token 4 can be attended to by all subsequent tokens, including image tokens and position query tokens, to provide context information. The two position query tokens P3 and P5 in the same generation step attend to the condition, to the image token 4, and to each other, while ignoring the earlier query P4*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/005_Figure_6.jpg]]
*Figure 6: Comparison with other methods. (a) Encoder–decoder approaches such as SAR and ARPG generate tokens independently, since query tokens contribute no key–value pairs. (b) Decoderonly methods like RANDAR rely on positional instruction tokens, but the causal mask reduces parallel generation to batched next-token prediction and forces instruction tokens to be cached, doubling memory. (c) In contrast, our method employs a specialized training mask that ensures mutual visibility among concurrently predicted tokens while caching only the generated tokens*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/016_Figure_10.jpg]]
*Figure 10: More visualization of attention maps in the LLAMAGEN-1.4B model*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/017_Figure_11.jpg]]
*Figure 11: More visualization of attention maps in the LLAMAGEN-1.4B model*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_h06l9w1clt/figures/019_Figure_13.jpg]]
*Figure 13: Generation Examples of Our Model. We show 1024×1024 text-to-image generation samples*



## 定位与知识库关联

### 1. 问题定位：自回归图像生成的并行化困境

传统自回归图像生成遵循光栅顺序的逐token预测范式，其核心瓶颈在于**内存受限的工作负载**：每次前向传播仅生成一个token，导致生成步数与图像分辨率呈线性增长（256×256需256步，512×512需1024步），延迟高企。这一瓶颈催生了多条并行化路线，LPD的工作正是在此脉络中展开。

### 2. 并行化自回归方法的谱系

LPD所处的并行化自回归图像生成领域，可大致分为以下几类方法：

**固定区域并行方法**：**PAR** 将图像划分为固定区域，每个区域内部并行预测。该方法受限于固定的分区策略，无法灵活调整并行度与生成顺序。

**随机顺序+位置指令方法**：**RandAR** 采用随机生成顺序，并通过位置指令token（positional instruction tokens）告知模型当前要预测的位置。然而，其因果注意力掩码将并行生成退化为批量式的next-token预测，且指令token需要被缓存，导致内存占用翻倍。

**编码器-解码器交叉注意力方法**：**ARPG** 和 **SAR** 使用编码器-解码器架构，查询token通过交叉注意力从编码器获取上下文，但查询token本身不贡献键值对，导致并行生成的token之间相互独立，缺乏联合建模能力。

**多尺度预测方法**：**VAR** 采用next-scale预测范式，从粗到细逐尺度生成，本质上是一种不同粒度的并行化策略，但其生成步数受尺度层级限制。

**非自回归方法**：**NAR** 一次性并行生成所有token，虽速度极快但质量通常显著低于自回归方法。

LPD的核心创新在于**将上下文提供与token生成解耦**，使用可学习位置查询token（position query tokens）驱动目标位置的并行生成，并通过专用的Context Attention和Query Attention掩码保证并行token的相互可见性。这使其区别于上述所有方法：既不像RandAR那样退化为批量next-token预测，也不像ARPG那样缺乏token间联合建模，同时保持了任意生成顺序和任意并行度的灵活性。

### 3. 空间局部性洞察的方法论贡献

LPD的另一个关键贡献在于**将图像生成中的空间局部性显式建模为生成顺序调度的指导原则**。通过对**LlamaGen**模型的注意力图分析（Figure 7），LPD定量验证了图像自回归生成中注意力权重随空间距离急剧衰减的现象——这并非LPD的原创发现，但LPD首次将其系统性地转化为生成顺序优化的两个可操作原则：

- **高邻近性原则**：优先选择靠近已生成token的位置，最大化上下文支持
- **低并发邻近性原则**：同组token彼此远离，最小化组内依赖

这一设计使得LPD在将生成步数从256大幅压缩至20时，仍能维持与光栅顺序基线相当的生成质量（FID 2.10 vs 2.12），而随机顺序和Halton顺序在相同步数下质量显著下降。该结果表明，**空间局部性感知的调度策略是并行自回归生成中维持质量的关键杠杆**，为后续工作提供了明确的优化方向。

### 4. 适用边界与局限

**计算受限场景下的加速衰减**：位置查询token的引入带来了额外的计算开销。在内存受限的小批次推理中，生成步数的减少几乎线性转化为延迟降低（约12倍加速）；但在计算受限的大批次推理中，加速比下降至约3倍。这意味着LPD的收益高度依赖于推理的批次规模——在单张图像生成的交互式场景中收益最大，在高吞吐离线批量生成中收益收窄。

**生成顺序的静态性**：当前方法需根据分辨率和步数预先计算生成顺序，无法在推理时根据图像内容动态调整。这限制了模型对不同局部区域复杂度差异的适应能力——某些区域可能需要更多上下文支持，而静态调度无法响应。

**评估范围的局限性**：实验主要集中在ImageNet类条件生成和内部文本-图像数据集，对更复杂的开放域场景（如复杂组合、多对象交互）和更大规模模型的泛化性尚未完全验证。此外，GenEval上的文本-图像生成评估仅覆盖1024×1024分辨率。

**视觉生成任务的单一性**：目前仅验证了图像生成任务，尚未扩展到视频生成（时间维度的局部性）、3D生成等其他视觉生成模态。时间维度的局部性是否可以采用类似的调度策略，仍是一个开放问题。

### 5. 开放问题

1. **多模态统一生成**：该灵活并行解码框架能否无缝扩展到同时输出文本和图像的多模态统一生成模型？文本序列的局部性与图像空间局部性存在本质差异，如何统一调度是一个挑战。

2. **自适应调度学习**：局部感知顺序调度中的邻近阈值ρ和排斥阈值τ是否可以学习，从而自适应不同数据集和分辨率？当前的手动设定（τ=2, ρ=1）在消融实验中表现稳定，但学习式调度可能带来进一步收益。

3. **KV缓存压缩的协同**：位置查询token带来的额外内存占用能否通过KV缓存压缩技术缓解？这直接影响LPD在大批次推理中的竞争力。

4. **极低步数下的质量保障**：当生成步数进一步压缩至8步甚至更少时，如何保证生成质量？当前20步（256×256）和48步（512×512）的设置已接近质量持平边界，更激进的压缩可能需要新的建模策略。

5. **视频生成中的时空局部性**：视频生成中时间维度的局部性（相邻帧的token高度相关）是否可以利用类似的调度策略？时空联合的局部性感知调度可能成为视频自回归生成加速的关键。



## 原文 PDF

![[paperPDFs/ICLR_2026/Locality_aware_Parallel_Decoding_for_Efficient_Autoregressive_Image_Generation.pdf]]

---
title: "InterMoE: Individual-Specific 3D Human Interaction Generation via Dynamic Temporal-Selective MoE"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic_Temporal_Selective_MoE.pdf
aliases:
- InterMoE
tags:
- AAAI_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 动态时间选择性混合专家（Dynamic Temporal‑Selective MoE）中的专家容量可学习性、批级路由和协同文本‑运动路由权重 α
primary_logic: 通过协同路由器融合高层文本语义与底层运动学特征，指导专家分配；再引入可学习偏置使每个专家自适应决定从批级时间池中选取多少及哪些关键帧，从而在保持个体身份的同时实现高语义保真度。
claims:
- InterMoE 在 InterHuman 和 InterX 分别降低 FID 9% 和 22%，取得最低 FID（4.677 和 0.297）和最佳 R‑Precision/MM‑Dist
- Synergistic Router 和 Dynamic Temporal Selection 各自对 FID 和 R‑Precision 有显著贡献（消融实验）
- 本文 MoE 范式优于 Token‑Choice 和 Expert‑Choice，FID 由 5.095/8.699 降至 4.677
- InterHuman 上 FID ↓ = 4.677
---

# InterMoE: Individual-Specific 3D Human Interaction Generation via Dynamic Temporal-Selective MoE

> [!tip] 核心洞察
> 通过协同路由器融合高层文本语义与底层运动学特征，指导专家分配；再引入可学习偏置使每个专家自适应决定从批级时间池中选取多少及哪些关键帧，从而在保持个体身份的同时实现高语义保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向个体特定的三维人机交互生成：基于动态时间选择性混合专家 |
| 英文题名 | InterMoE: Individual-Specific 3D Human Interaction Generation via Dynamic Temporal-Selective MoE |
| 会议/期刊 | AAAI 2026 |
| Links | [Code](https://github.com/Lighten001/InterMoE) · [paper](https://arxiv.org/abs/2511.13488) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InterMoE |
| Dataset | InterHuman, InterX |

> [!tip] 效果简介
> - InterHuman 上，FID ↓ 4.677 (‑9%（相对最佳对比方法）)；R‑Precision Top‑1 ↑ 0.512；MM‑Dist ↓ 3.762。
> - InterX 上，FID ↓ 0.297 (‑22%（相对最佳对比方法）)；R‑Precision Top‑1 ↑ 0.427；MM‑Dist ↓ 3.011。

## 概述

三维人机交互生成旨在根据文本描述合成双人交互运动序列，其核心挑战在于**同时保留个体独有特征与严格遵循文本语义**。现有方法或采用标准前馈网络，或引入固定的混合专家（MoE）路由（如 Token‑Choice 与 Expert‑Choice），但这些机制对时间维度的非均匀重要性缺乏感知，导致动作趋同、身份混淆和语义对齐不足。

**InterMoE** 针对上述瓶颈提出了 **动态时间选择性混合专家（Dynamic Temporal‑Selective MoE）** 范式。其核心洞察是：通过协同路由器融合高层文本语义与底层运动学特征来指导专家分配，并引入可学习偏置使每个专家自适应地从批级时间池中选取关键帧，从而在保持个体身份的同时实现高语义保真度。方法的关键调控变量包括专家容量可学习性、批级路由以及协同文本‑运动路由权重 α。

在 **InterHuman** 和 **InterX** 两个基准数据集上，InterMoE 分别将 FID 降低 9% 和 22%，取得了最低 FID（4.677 和 0.297）以及最优的 R‑Precision 与 MM‑Dist。消融实验证实，协同路由器、批级路由和动态时间选择各自对 FID 和 R‑Precision 有显著贡献；本文 MoE 范式在 FID 上明显优于 Token‑Choice（5.095）和 Expert‑Choice（8.699）。定性结果进一步显示，InterMoE 在击剑、拔河等复杂交互中有效缓解了身份混淆和关键动作缺失的问题。

**方法定位**：InterMoE 以 **InterGen**（Liang et al., CVPR 2024）的扩散框架为基础，将其标准 FFN 替换为动态时间选择性 MoE，同时引入因果‑骨骼 VAE 进行层次化运动编码。该方法在单人多动作生成任务（HumanML3D）上也展现出插拔式提升，验证了其模块的通用性。

**局限与展望**：当前框架未显式施加物理约束，偶尔产生穿透、抖动和脚部滑动等微小瑕疵；且仅处理人‑人交互，尚未扩展到人‑物、人‑动物等更广泛的交互类型。如何引入物理先验、适配更多样交互场景以及支撑长序列多智能体生成，是值得进一步探索的开放问题。

## 背景与动机

三维人机交互生成旨在根据文本描述合成双人或多人的三维动作序列，在虚拟现实、游戏角色动画、人机协作仿真等领域具有重要应用价值。该任务的核心难点在于同时满足两个高度耦合的需求：**语义保真度**（生成的动作必须严格遵循文本描述中的交互语义）与**个体特异性**（交互双方需保持各自独立的运动风格与身份特征，避免动作趋同或身份混淆）。

现有方法主要沿两条技术路径展开。一类以 **InterGen**（Liang et al., CVPR 2024）为代表，采用扩散模型框架，通过双人共享权重的去噪器与交叉注意力机制建模交互动态，但其前馈层使用标准 FFN，缺乏对时间维度非均匀重要性的感知能力。另一类方法如 **TIMotion**（Wang et al., 2025）和 **InterMask**（Javed, Li et al., 2025）分别从时序建模与空间‑时间 Transformer 自回归生成的角度推进，但同样未解决一个根本性问题：**交互动作序列中不同时间帧对语义表达和个体特征承载的重要性存在显著差异，而传统架构对此缺乏显式建模**。

混合专家（Mixture of Experts, MoE）机制为上述问题提供了潜在的解决方向。然而，传统的 Token‑Choice MoE（Fei et al., 2024）让每个 token 选择固定数量的专家，Expert‑Choice MoE（Sun et al., 2024a）则让每个专家选择固定数量的最显著 token——二者均采用**固定容量分配**策略，无法感知不同时间帧在语义和运动学层面的差异化需求。如 Figure 1 所示，Token‑Choice 在“伸手”等关键动作上生成不准确，Expert‑Choice 则整体运动学质量较低。这些缺陷的根源在于：**现有 MoE 路由机制缺乏对高层文本语义与底层运动学特征的协同利用，且专家容量分配不具备时间选择性**。

综上，本工作的核心动机可归纳为三个层面：
1. **时间选择性缺失**：交互动作的关键语义往往集中在少数时间帧（如接触瞬间、方向转折点），现有方法对全序列均匀处理，导致关键帧信息被稀释；
2. **语义‑运动协同不足**：文本路由与运动路由各自独立时，难以在“做什么”（语义）与“怎么做”（运动学）之间建立精确对应；
3. **个体身份混淆**：双人交互中，若无针对性的时间特征分配机制，双方动作容易相互污染，丧失个体特异性。

针对上述缺口，本文提出 **InterMoE**，核心思路是通过**动态时间选择性混合专家**机制，使每个专家能够自适应地从批级时间池中选择关键帧进行处理，同时引入协同路由器融合文本语义与运动学特征来指导分配决策，从而在保持个体身份的同时实现高语义保真度的交互生成。

## 核心创新

InterMoE 的核心创新在于用**动态时间选择性混合专家（Dynamic Temporal‑Selective MoE）**替代传统 Transformer 块中的标准前馈网络（FFN），以解决三维人机交互生成中个体身份混淆与文本语义对齐不足的双重瓶颈。该模块由两个关键子机制构成：**协同路由器（Synergistic Router）**与**动态时间选择（Dynamic Temporal Selection）**，二者共同实现“文本‑运动协同路由 + 可学习容量 + 批级关键帧自适应分配”的独特范式。

### 1. 协同路由器：融合高层语义与底层运动学

传统 MoE 路由通常仅基于 token 的表征（如 Token‑Choice）或全局负载均衡（如 Expert‑Choice），缺乏对文本语义的显式利用。InterMoE 引入并行的**运动路由器**和**文本路由器**，分别从运动特征和文本条件计算路由 logits：

- 运动路由 logits：$\mathbf{R}_{e,s,i}^{\mathrm{motion}} = \mathbf{Router}_{e}^{\mathrm{motion}}(m_{s,i}^{\mathrm{flat}})$，基于个体运动特征 $m_{s,i}^{\mathrm{flat}}$ 计算第 $e$ 个专家的路由信号（Eq. 1）。
- 文本路由 logits：$\mathbf{R}_{e}^{\mathrm{text}} = \mathbf{Router}_{e}^{\mathrm{text}}(c_t)$，基于文本条件 $c_t$ 计算专家路由信号（Eq. 2）。
- 融合路由：$\mathbf{R}_{e,s,i}^{\mathrm{comb}} = \alpha \mathbf{R}_{e,s,i}^{\mathrm{motion}} + (1 - \alpha) \mathbf{R}_{e}^{\mathrm{text}}$，其中 $\alpha=0.5$（Eq. 3）。

这一设计的因果作用在于：运动路由器捕捉个体独特的运动学特征以保持身份，文本路由器注入高层语义约束以保证动作与描述的对应关系。消融实验（Table 2）证实，移除并行路由器（仅保留单一路由器）会导致 R‑Precision 和 FID 均显著下降，表明两种信息的协同是语义保真度和个体特征保留的关键。

### 2. 动态时间选择：可学习容量与批级关键帧分配

现有 MoE 范式（Token‑Choice 和 Expert‑Choice）对时间维度的非均匀重要性缺乏感知——交互动作的关键帧往往集中在少数时间步，而均匀分配专家容量会导致关键帧处理不足或资源浪费。InterMoE 的**动态时间选择**通过以下机制解决该问题：

- **批级路由池**：路由器在批次内所有时间帧组成的全局特征池上操作，而非局限在单个样本内。这使专家能够跨样本学习哪些时间步对特定动作语义具有普遍重要性。消融实验（Table 2）显示，禁用批级路由回退到实例级路由后，FID 显著恶化。
- **可学习专家偏置 $b_e$**：每个专家 $e$ 维护一个可学习偏置，与融合路由 logits 相加后经 sigmoid 得到激活掩码 $\mathbf{M}_{e,s} = \sigma(\mathbf{R}_{e,s}^{\mathrm{comb}} + b_e)$。偏置的更新规则为 $b_e \gets b_e - \sigma \Delta b_e$，其中 $\Delta b_e = \mathrm{sign}(K_e^{\mathrm{select}} - K_e^{\mathrm{exp}})$（Eqs. 7‑9）。该规则使专家在训练中自适应调整其处理的 token 数量，逐步收敛到期望容量 $C^{\mathrm{exp}}$。
- **软门控与硬掩码结合**：最终门控权重 $\mathbf{G}_{e,s}$ 在 $\mathbf{M}_{e,s} > 0$ 时取 softmax 归一化的路由权重 $\mathbf{A}_{e,s}$，否则置零（Eqs. 4‑6）。MoE 输出为所有专家输出的加权和：$m_s^{\mathrm{out}} = \sum_{e=1}^N \mathbf{G}_{e,s} E(m_s)$（Eq. 10）。

这一机制的核心洞察在于：通过可学习偏置使每个专家**自行决定从批级时间池中选取多少及哪些关键帧**，而非被动接受固定容量的分配。消融实验（Table 2）表明，用固定 top‑K 替代动态选择或移除时间选择（均匀分配）均导致 FID 大幅上升。此外，Table 3 的 MoE 类型消融显示，本文范式（FID 4.677）显著优于 Token‑Choice（FID 5.095）和 Expert‑Choice（FID 8.699），验证了动态时间选择性在交互生成中的根本优势。

### 3. 与 baseline 的 changed slots 对比

InterMoE 相对于强基线 **InterGen**（Liang et al., CVPR 2024）的核心改动集中在去噪网络的**前馈层/路由机制**：

| 改动槽位 | InterGen / 常规 MoE | InterMoE |
|----------|---------------------|----------|
| 路由机制 | 标准 FFN 或固定容量的 Token‑Choice / Expert‑Choice MoE | Dynamic Temporal‑Selective MoE（协同语义‑运动路由器 + 可学习专家容量 + 批级动态时间选择） |
| 路由范围 | 实例级（仅基于单个样本） | 批级（批次内所有时间帧组成全局特征池） |
| 专家容量 | 固定 Top‑K（每个专家选择固定个数的 token） | 可学习偏置 $b_e$ 动态确定每个专家处理的 token 数量（训练驱动收敛到期望容量 $C^{\mathrm{exp}}$） |

这些改动直接针对现有方法的根本瓶颈：标准 FFN 无法为不同语义和时间位置分配差异化处理能力，而固定容量的 MoE 对时间维度的非均匀重要性缺乏感知。InterMoE 通过协同路由和动态选择，在保持个体身份的同时实现了高语义保真度——这一因果链条在 InterHuman（FID 降低 9%）和 InterX（FID 降低 22%）两个基准上得到了充分验证。

### 4. 局限与待验证方向

当前设计未显式施加物理约束，偶尔产生穿透、抖动和脚部滑动等微小瑕疵。如何引入物理先验（如碰撞检测、接触力学）以进一步减少伪影，是值得探索的方向。此外，动态时间选择 MoE 在多智能体（>2 人）交互中的扩展性和效率仍需验证。

## 整体框架

InterMoE 的整体生成流程遵循“编码—扩散去噪—解码”的范式，并在去噪阶段引入动态时间选择性混合专家（Dynamic Temporal‑Selective MoE）以同时保留个体身份特征与文本语义保真度。整个框架由三个核心模块串联构成：

1. **Causal‑Skeletal VAE**：对双人各自的三维骨骼运动进行层次化压缩编码与重建解码。
2. **Cooperative MoE Denoiser**：两个权重共享的扩散去噪网络，在隐空间中交互式地去除噪声，内部集成自注意力、交叉注意力与 MoE 块。
3. **Dynamic Temporal‑Selective MoE**：嵌入每个 Transformer 块的 MoE 层，由 Synergistic Router 和 Dynamic Temporal Selection 两部分组成，负责在批级时间池上动态分配专家。

### 输入输出流

给定一段文本描述 $c_t$ 和两个体运动序列 $\mathbf{m}_1, \mathbf{m}_2 \in \mathbb{R}^{T \times J \times d}$（$T$ 为帧数，$J$ 为关节数，$d$ 为特征维度），Causal‑Skeletal VAE 先将每人的运动压缩为紧凑的隐变量 $\mathbf{z}_1, \mathbf{z}_2$，然后通过扩散过程逐步加噪。去噪阶段，两个权重共享的 Cooperative MoE Denoiser 分别接收 $\mathbf{z}_1$ 和 $\mathbf{z}_2$，在每一层 Transformer 块中依次执行：

- **自注意力**：建模个体内部时序依赖。
- **交叉注意力**：融合伙伴的运动特征，实现交互信息交换。
- **MoE 块**：将展平后的运动特征 $\mathbf{m}_s^{\mathrm{flat}} \in \mathbb{R}^{1 \times D}$（$s$ 为样本索引）送入 Dynamic Temporal‑Selective MoE，由 Synergistic Router 计算路由 logits，再由 Dynamic Temporal Selection 决定各专家处理哪些时间帧，最后加权求和得到输出。

去噪完成后，VAE 解码器将隐变量恢复为原始运动序列，完成生成。

### 关键模块关系

整个框架的设计瓶颈集中在 MoE 块的路由与选择机制上。标准前馈网络或固定容量的 Token‑Choice / Expert‑Choice MoE 对时间维度的非均匀重要性缺乏感知，导致动作趋同和身份混淆。InterMoE 的解决思路是：

- **Synergistic Router** 在批级范围内（而非单样本内部）融合高层文本语义与底层运动学特征，生成协同路由信号 $\mathbf{R}_{e,s,i}^{\mathrm{comb}} = \alpha \mathbf{R}_{e,s,i}^{\mathrm{motion}} + (1 - \alpha) \mathbf{R}_{e}^{\mathrm{text}}$（$\alpha = 0.5$），使路由决策既感知“做什么动作”也感知“谁在做”。
- **Dynamic Temporal Selection** 引入可学习偏置 $b_e$，使每个专家自适应地从批级时间池中选取关键帧，而非固定 Top‑K 分配。偏置通过训练动态更新 $b_e \gets b_e - \sigma \Delta b_e$，其中 $\Delta b_e = \mathrm{sign}(K_e^{\mathrm{select}} - K_e^{\mathrm{exp}})$，使实际选择的 token 数量 $K_e^{\mathrm{select}}$ 逐步逼近期望容量 $K_e^{\mathrm{exp}}$。这一机制使专家能够专注于对语义和身份区分最关键的时序片段，从而在保持个体特征的同时实现高语义保真度。

图 2 完整展示了上述模块的连接关系：Causal‑Skeletal VAE（图 2a）提供压缩表示，两个权重共享的 Cooperative MoE Denoiser（图 2b）交互去噪，而 Synergistic Router 与 Dynamic Temporal‑Selective Expert（图 2c）则嵌入每个 Transformer 块的 MoE 层中，构成框架的核心创新点。

### 补充图表

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of the InterMoE. (a) Causal-Skeletal VAE to encode/decode individual motions; (b) Two Cooperative MoE Denoisers to interactively perform denoising; (c) Our proposed Synergistic Router and Dynamic Temporal-Selective Expert mechanism. The router guides multiple experts to select and process critical temporal features of the motion sequence dynamically*

## 核心模块与公式推导

### 3.1 因果骨骼 VAE（Causal‑Skeletal VAE）

交互生成的第一步是将高维骨骼运动压缩为紧凑的潜在表示。InterMoE 采用**因果骨骼 VAE**对单人运动进行层次化编码（Figure 2a）。对于个体 $i$ 的三维运动序列 $\mathbf{m}_i \in \mathbb{R}^{T \times J \times d}$（$T$ 帧，$J$ 个关节，$d$ 维特征），编码过程分两步：

1. **骨骼图卷积**：首先在每一帧内对骨骼图执行图卷积，捕捉关节间的空间依赖关系。
2. **因果卷积**：随后沿时间维度施加因果卷积（Figure 6），建模帧间时序动态，同时严格保持因果性——即当前帧的表示仅依赖于过去帧，防止未来信息泄漏。最后通过池化操作获得紧凑的潜在编码。

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/012_Figure_6.jpg]]
*Figure 6: Illustration of the causal convolution*

解码器采用对称的上池化操作，逐步恢复原始运动分辨率。VAE 的训练目标为：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_m + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{kl}} \mathcal{L}_{\mathrm{kl}} \tag{11}$$

其中 $\mathcal{L}_m$ 为运动特征的 L1 重建损失，$\mathcal{L}_{\mathrm{pos}}$ 和 $\mathcal{L}_{\mathrm{vel}}$ 分别为关节位置和速度的 L1 重建项，$\mathcal{L}_{\mathrm{kl}}$ 为 KL 散度正则项，$\lambda_{\mathrm{pos}}$、$\lambda_{\mathrm{vel}}$、$\lambda_{\mathrm{kl}}$ 为对应权重。

### 3.2 协作 MoE 去噪器（Cooperative MoE Denoiser）

扩散模型的去噪网络由**两个权重共享的协作去噪器**组成，分别处理交互双方的运动（Figure 2b）。每个去噪器由多个 Transformer 块堆叠而成，每块包含三个核心组件：

- **自注意力层**：建模个体内部的时序依赖。
- **交叉注意力层**：融合伙伴的运动特征，实现交互信息交换。
- **MoE 块**：替代标准 FFN，是本文的核心创新。

输入去噪器的运动特征首先被展平为 $\mathbf{m}_i \in \mathbb{R}^{T \times D_m}$，其中 $D_m = J \times d$。

### 3.3 动态时间选择性 MoE（Dynamic Temporal‑Selective MoE）

MoE 块由**协同路由器（Synergistic Router）**和**动态时间选择（Dynamic Temporal Selection）**两部分构成，是 InterMoE 的核心机制（Figure 2c）。

#### 3.3.1 协同路由器

路由器在**批级时间池**上操作：将批次内所有样本的所有时间帧拼接为全局特征池，使专家能从跨样本、跨时间的视角进行选择。路由器包含两个并行分支：

- **运动路由器**：以个体运动特征 $m_{s,i}^{\mathrm{flat}}$ 为输入，计算第 $e$ 个专家的路由 logits：

$$\mathbf{R}_{e,s,i}^{\mathrm{motion}} = \mathbf{Router}_{e}^{\mathrm{motion}}(m_{s,i}^{\mathrm{flat}}) \tag{1}$$

- **文本路由器**：以文本条件 $c_t$ 为输入，计算专家路由 logits：

$$\mathbf{R}_{e}^{\mathrm{text}} = \mathbf{Router}_{e}^{\mathrm{text}}(c_t) \tag{2}$$

两路 logits 通过加权融合得到最终路由分数：

$$\mathbf{R}_{e,s,i}^{\mathrm{comb}} = \alpha \mathbf{R}_{e,s,i}^{\mathrm{motion}} + (1 - \alpha) \mathbf{R}_{e}^{\mathrm{text}} \tag{3}$$

其中 $\alpha = 0.5$，平衡高层语义引导与底层运动学特征。

#### 3.3.2 动态时间选择

传统 MoE 中每个专家处理的 token 数量是固定的（如 Top‑K），但交互序列中不同时间帧对语义表达的重要性差异显著。InterMoE 引入**可学习专家偏置** $b_e$，使每个专家自适应地决定从批级时间池中选取多少及哪些关键帧。

具体地，对每个专家 $e$ 和序列 $s$：

- 计算激活掩码：$\mathbf{M}_{e,s} = \mathrm{sigmoid}(\mathbf{R}_{e,s}^{\mathrm{comb}}) + b_e$
- 计算注意力权重：$\mathbf{A}_{e,s} = \mathrm{softmax}(\mathbf{R}_{e,s}^{\mathrm{comb}})$
- 动态门控为：

$$\mathbf{G}_{e,s} = \begin{cases} \mathbf{A}_{e,s}, & \mathbf{M}_{e,s} > 0, \\ 0, & \mathrm{otherwise}. \end{cases} \tag{4-6}$$

训练过程中，每个专家 $e$ 实际选择的 token 数量 $K_e^{\mathrm{select}}$ 与期望数量 $K_e^{\mathrm{exp}} = \frac{C^{\mathrm{exp}} \times \mathrm{SequenceLength}}{\mathrm{ExpertNumber}}$ 比较，偏置按以下规则更新：

$$\Delta b_e = \mathrm{sign}(K_e^{\mathrm{select}} - K_e^{\mathrm{exp}}) \tag{7-8}$$

$$b_e \gets b_e - \sigma \Delta b_e \tag{9}$$

其中 $\sigma$ 为更新步长。该机制使专家容量在训练中动态收敛至期望值 $C^{\mathrm{exp}}$，无需手工设定固定 Top‑K。

最终，MoE 块的输出为所有专家输出的加权和：

$$m_s^{\mathrm{out}} = \sum_{e=1}^N \mathbf{G}_{e,s} \, E(m_s), \quad m_s \in \mathbb{R}^{1 \times D}, \; s \in \{1, \ldots, S\} \tag{10}$$

其中 $N$ 为专家总数，$E(\cdot)$ 为第 $e$ 个专家网络的前向计算，$S$ 为批级时间池中的序列总数。

### 3.4 关键设计决策的因果机制

上述模块设计直指核心瓶颈：**标准 FFN 或固定路由 MoE 无法感知时间维度的非均匀重要性**，导致动作趋同和身份混淆。协同路由器通过融合文本语义与运动学特征，为专家分配提供了双视角引导；可学习偏置 $b_e$ 使专家容量从“固定分配”变为“数据驱动自适应”，批级路由则扩大了专家的选择视野，使其能从全局时间池中筛选对语义保真和个体特征最关键的帧。消融实验（Table 2）证实：移除任一路由器、禁用批级路由、或用固定 Top‑K 替代动态选择，均导致 FID 和 R‑Precision 显著恶化。

### 补充图表

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/001_Figure_1.jpg]]
*Figure 1: Compared with conventional MoE mechanisms, Token-Choice inaccurately generates the “extends” action, and Expert-Choice has low overall kinematic quality. Our framework leverages the Synergistic Router and Dynamic Temporal Selection mechanism to generate 3D human interactions that exhibit both high semantic fidelity and robust preservation of individual-specific characteristics*

## 实验与分析

### 主实验结果

InterMoE 在 InterHuman 和 InterX 两个双人交互数据集上进行了全面评估，与 **InterGen**（Liang et al., CVPR 2024）、**TIMotion**（Wang et al., 2025）、**InterMask**（Javed, Li et al., 2025）等方法对比。所有方法使用相同的训练/测试划分和评估协议（20 次评估，95% 置信区间）。

**Table 1** 给出了定量结果。在 InterHuman 上，InterMoE 取得最低 FID（4.677），相对最佳对比方法降低约 9%；同时获得最佳 R-Precision Top-1（0.512）和最佳 MM-Dist（3.762）。在 InterX 上，FID 降至 0.297，相对最佳对比方法降低约 22%，R-Precision Top-1 达到 0.427，MM-Dist 为 3.011。这两个数据集上的 FID 优势表明，动态时间选择性 MoE 有效提升了生成动作的整体真实感。

值得注意的是，InterMoE 的 MultiModality 得分略低于部分方法，但其 R-Precision 和 FID 优势明显。这反映了一个设计权衡：模型优先保证文本对齐与真实感，而非追求同一文本描述下的动作多样性最大化。

**Figure 3** 的定性对比进一步印证了上述结论。在击剑、拔河、跆拳道等交互动作中，InterMoE 生成的运动轨迹（箭头标注）更贴合文本描述，关键动作（红圈标注）准确，而 TIMotion 和 InterMask 在部分场景中出现身份混淆（紫框标注）。这验证了协同路由器在保持个体特征方面的有效性。

### 消融实验

**Table 2** 展示了关键组件的消融结果，所有实验均在 InterHuman 测试集上进行。

**协同路由器的必要性。** 移除并行的运动路由器或文本路由器（仅保留单一路由器）后，R-Precision 和 FID 均显著下降。这表明高层文本语义与底层运动学特征的协同融合是保证语义保真度的关键——单独依赖任一信息源都会导致路由决策偏差。

**批级路由的贡献。** 禁用批级路由、回退到实例级路由时，FID 严重恶化。这说明在批次内所有时间帧组成的全局特征池上进行专家分配，能够学习到更丰富的生成分布，实例级路由则因信息受限而无法捕捉跨样本的时序模式。

**动态时间选择的决定性作用。** 用固定 top-K 替代动态选择机制，或完全移除时间选择（均匀分配专家），均导致 FID 大幅上升。这验证了核心洞察：时间维度的非均匀重要性要求专家能够自适应地决定从批级时间池中选取哪些关键帧，而非被动接受固定分配。

**Table 3** 比较了不同 MoE 范式。Token-Choice MoE（TC, Fei et al., 2024）和 Expert-Choice MoE（EC, Sun et al., 2024a）的 FID 分别为 5.095 和 8.699，而 InterMoE 的 Dynamic Temporal-Selective MoE 将 FID 降至 4.677。EC 表现最差，因为其强制每个专家选择固定数量的最显著 token，忽略了时间维度的重要性差异；TC 虽允许 token 选择专家，但缺乏对时序动态的感知。**Figure 5** 的定性对比显示，在“递纸”等场景中，TC 生成的动作轨迹偏离文本描述，EC 的运动学质量整体较低，而 InterMoE 在语义保真度和运动轨迹上均表现最佳。

**Table 4** 和 **Table 5** 分别消融了专家数量和期望容量。8 个专家时 FID 最优（4.677），16 个专家时略有退化（4.970），说明过多专家可能导致过拟合或路由分散。期望容量 $C^{\mathrm{exp}}=1$ 时 FID 最优（4.677），增大或减小均导致指标变差——容量过小限制了专家表达能力，容量过大则稀释了动态选择的专注性。

### 泛化性与用户研究

**Table 6** 展示了在 HumanML3D 单人动作生成数据集上的泛化实验。将 InterMoE 的核心模块（协同路由器和动态时间选择）插入其他基线模型后，FID 和 R-Precision 均有提升，验证了该 MoE 范式不限于双人交互场景，具备插拔式通用性。

**Table 7** 的用户研究从三个维度评估：个体特征保持、语义保真度和整体质量。InterMoE 在所有维度上均获得最高评分，与定量指标一致。

### 失败模式与局限

尽管整体表现优异，InterMoE 仍存在以下已知局限：

1. **物理伪影。** 由于未显式施加物理约束（如碰撞检测、接触力学），生成动作偶尔出现穿透、抖动和脚部滑动等微小瑕疵。这在高接触性交互（如摔跤、拥抱）中更为明显。
2. **交互类型受限。** 当前框架仅处理人-人交互，尚未扩展到人-物、人-动物等更广泛的交互类型。
3. **长序列与多智能体扩展性。** 在长序列生成和多智能体（>2 人）场景下的效率和扩展性有待探索，专家分配可能面临组合爆炸问题。

这些局限指向了未来的改进方向：引入物理先验以减少伪影，设计层级时间抽象或记忆机制以支撑长期交互推理，以及探索多智能体场景下的高效专家分配策略。

### 补充图表

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative comparisons among the different MoE types. Arrowed lines mark the trajectories of motion*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons with TIMotion (2025) and InterMask (2025). Arrowed lines mark the trajectories of motion, Red circles indicate key actions that align with the text, and Purple boxes highlight the identity confusion error*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation results on the test sets of InterHuman and Inter-X datasets. ↑ and ↓ denote that higher and lower values are better, respectively, while → denotes that the values closer to the real motion are better. We run the evaluations 20 times. ± indicates a 95% confidence interval*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/005_Table_2.jpg]]
*Table 2: Ablation study results on the InterHuman test set to verify key components of our InterMoE*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/006_Table_3.jpg]]
*Table 3: Ablation results of the MoE type*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/008_Table_4.jpg]]
*Table 4: Ablation results of the expert number*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/007_Table_5.jpg]]
*Table 5: Ablation results of the expectation of the number of experts allocated per feature Cexp*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/009_Table_6.jpg]]
*Table 6: Quantitative results on the HumanML3D test set, demonstrate the generalization of our InterMoE framework*

![[assets/figures/papers/paper_list_l1664_InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic/figures/013_Table_7.jpg]]
*Table 7: User study results*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

InterMoE 的核心贡献在于将混合专家（MoE）机制引入三维人-人交互生成，并通过动态时间选择性路由解决个体身份保持与文本语义对齐之间的冲突。其方法定位可以从以下几条谱系来理解：

**（1）交互生成基线。** 本文直接对标的是基于扩散的双人交互生成框架 **InterGen**（Liang et al., CVPR 2024）。InterGen 采用双人共享权重的去噪器与交叉注意力机制来建模交互，但其前馈层使用标准 FFN，缺乏对时间维度非均匀重要性的感知能力。InterMoE 在保持 InterGen 的共享权重去噪器架构的基础上，将 FFN 替换为 Dynamic Temporal-Selective MoE，从而在几乎不增加推理开销的前提下显著提升生成质量。此外，**TIMotion**（Wang et al., 2025）和 **InterMask**（Javed, Li et al., 2025）作为近期最强对比方法，分别在时序动态建模和空间-时间 Transformer 自回归生成上有所建树，但在个体身份保持和语义保真度上仍存在可观察的退化——Figure 3 中的定性对比明确展示了 TIMotion 和 InterMask 在击剑、拔河等动作中出现的身份混淆和关键动作缺失。

**（2）MoE 路由范式。** 在 MoE 路由机制层面，本文系统对比了两种主流范式：**Token-Choice MoE**（Fei et al., 2024），即每个 token 选择固定数量的专家；以及 **Expert-Choice MoE**（Sun et al., 2024a），即每个专家选择固定数量的最显著 token。两者的共同缺陷在于路由容量固定，无法感知时间维度上关键帧与非关键帧的差异。Table 3 的消融实验给出了有力证据：Token-Choice 的 FID 为 5.095，Expert-Choice 则高达 8.699，而 InterMoE 的 Dynamic Temporal-Selective MoE 将 FID 降至 4.677。Figure 1 进一步从定性角度揭示了 Expert-Choice 整体运动学质量低下、Token-Choice 在“伸手”等语义关键动作上生成不准确的问题。

**（3）文本-运动对齐方法。** 在文本条件驱动的运动生成领域，现有工作通常仅依赖文本语义进行条件注入。InterMoE 提出的 Synergistic Router 通过并行计算运动路由 logits（Eq. 1）和文本路由 logits（Eq. 2），并以可学习权重 $\alpha=0.5$ 进行加权融合（Eq. 3），实现了高层语义与底层运动学特征的协同指导。Table 2 的消融实验表明，移除并行运动/文本路由器会导致 R-Precision 和 FID 同时显著下降，验证了双源路由融合的必要性。

### 2. 适用边界与局限

尽管 InterMoE 在 InterHuman 和 InterX 两个基准上取得了最优 FID（分别为 4.677 和 0.297，相对最佳对比方法分别降低 9% 和 22%），其适用边界和局限同样值得关注：

**（1）物理合理性不足。** 本文方法未显式施加物理约束（如碰撞检测、接触力学），导致生成结果中偶尔出现穿透、抖动和脚部滑动等微小瑕疵。这是当前数据驱动生成方法的共性瓶颈——扩散模型优化的分布匹配目标并不天然保证物理可行性。

**（2）交互类型受限。** 当前框架仅处理人-人交互，尚未扩展到人-物交互、人-动物交互等更广泛的交互类型。Causal-Skeletal VAE 的骨骼图卷积和因果卷积设计虽然对双人骨骼结构具有通用性，但跨实体的交互建模可能需要重新设计交叉注意力或路由机制。

**（3）长序列与多智能体扩展性。** 在长序列生成场景下，批级动态时间选择的计算复杂度随序列长度线性增长；在多智能体（三人及以上）交互中，如何高效分配专家并保持各自身份特征，避免组合爆炸，仍是开放问题。Table 4 显示专家数从 8 增至 16 时 FID 从 4.677 退化至 4.970，暗示当前路由策略在专家数量扩展上存在边际效益递减。

**（4）多样性与保真度的权衡。** Table 1 中 InterMoE 的 MultiModality 得分略低于部分对比方法，但其 R-Precision 和 FID 优势明显。这表明本文方法在设计上优先保证了文本对齐与真实感，可能在一定程度上牺牲了同一文本条件下的动作多样性。这并非严格缺陷，而是设计决策的体现。

### 3. 开放问题与后续方向

基于上述局限，以下方向值得后续工作探索：

- **物理先验的引入。** 如何在扩散生成过程中嵌入碰撞检测、接触力学或物理模拟器反馈，以进一步减少穿透和滑步伪影，是提升交互生成物理可信度的关键路径。
- **跨实体交互泛化。** 将 Dynamic Temporal-Selective MoE 适配到人-物交互、人-动物交互等场景，需要重新考虑路由器的输入特征设计和批级时间池的构建方式。
- **层级时间抽象。** 针对超长时序生成，引入层级时间抽象或记忆机制（如 temporal pyramid、recurrent memory bank）可能有助于支撑稳定的长期交互推理，同时缓解批级路由的计算压力。
- **多智能体路由扩展。** 在三人及以上交互中，专家分配策略可能需要从当前的批级平面路由升级为图结构路由或层级路由，以在保持个体身份的同时控制计算复杂度。
- **通用性验证。** Table 6 中 HumanML3D 单人数据集上的泛化实验已初步验证了 InterMoE 模块的插拔式提升能力，但更多基线（如 MDM、MLD 等）和更多数据集上的系统性验证将有助于确立该方法的通用性边界。

## 原文 PDF

![[paperPDFs/AAAI_2026/InterMoE_Individual_Specific_3D_Human_Interaction_Generation_via_Dynamic_Temporal_Selective_MoE.pdf]]
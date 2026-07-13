---
title: "TransPhase: Deep Compositional Phase Diffusion for Long Motion Sequence Generation"
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation.pdf
project_link: null
code_link: https://github.com/asdryau/TransPhase
aliases:
- CPDT
- TransPhase
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过 ACT-PAE 将运动编码到统一的相位潜空间，SPDM 引入语义条件去噪，同时 TPDM 双向引入相邻片段的相位动态调节，在扩散过程中逐步对齐过渡区域的相位参数。
primary_logic: 在可变长运动编码的周期性相位潜空间内进行双条件（语义+相邻相位）并行扩散，可同步实现语义对齐和相位平滑过渡，且框架可线性扩展至任意数量的运动片段。
claims:
- 在组合运动对生成任务中，TransPhase 在整体运动真实感（Overall FID）和文本对齐（Overall MMD）上均优于所有基线。
- 在长时运动生成（3164个文本，168分钟）中，TransPhase 在整体 FID（0.847）和 MMD（4.849）上取得最优。
- 在无条件运动内插（UMIB）中，TransPhase 在所有过渡长度下的 L2-Vel 和 NPSS 等过渡真实感指标上均大幅领先基线。
- 在条件运动内插（CMIB）中，TransPhase 在 60 帧和 120 帧过渡长度下取得最佳运动真实感（Smt.FID）和文本对齐（MMD）。
---

# TransPhase: Deep Compositional Phase Diffusion for Long Motion Sequence Generation

> [!tip] 核心洞察
> 在可变长运动编码的周期性相位潜空间内进行双条件（语义+相邻相位）并行扩散，可同步实现语义对齐和相位平滑过渡，且框架可线性扩展至任意数量的运动片段。

| 字段 | 内容 |
|------|------|
| 中文题名 | TransPhase：面向长运动序列生成的深度组合相位扩散 |
| 英文题名 | TransPhase: Deep Compositional Phase Diffusion for Long Motion Sequence Generation |
| 会议/期刊 | NEURIPS 2025 |
| Links | [Code](https://github.com/asdryau/TransPhase) · [paper](https://arxiv.org/abs/2510.14427) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Compositional Phase Diffusion (TransPhase) |
| Dataset | Compositional Motion Pair Generation, Long-term Motion Generation, Unconditional Motion Inbetweening (UMIB) 60/120/180 frames, Conditional Motion Inbetweening (CMIB) 60/120 frames |

> [!tip] 效果简介
> - Compositional Motion Pair Generation (BABEL-TEACH) 上，Overall FID 0.782 vs best baseline: MDM-30 1.146; TEACH 1.041; PCMDM 0.837; priorMDM 0.839 (优于所有基线)。
> - Compositional Motion Pair Generation 上，Overall MMD 4.711 vs best baseline: MDM-30 4.923; TEACH 4.821; PCMDM 5.423; priorMDM 5.025 (优于所有基线)。
> - Long-term Motion Generation (3164 texts, 168 min) 上，Overall FID 0.847 vs best baseline: TEACH 1.780; PCMDM 0.876; priorMDM 1.536 (优于所有基线)。

## 概要

### 问题背景

现有运动生成模型在组合多个语义片段时，通常直接在原始运动空间中进行过渡建模，例如通过线性混合相邻帧（**MDM-30**, Tevet et al., 2023; **MLD-30**, Chen et al., CVPR 2023）或自回归生成过渡片段（**TEACH**, Shi et al., 2023）。这些方法忽略了运动内在相位的动态连续性，导致过渡区域频繁出现脚滑动、突然转向等突兀伪影，严重影响长序列运动的真实感。

### 核心方法

**TransPhase** 提出了一种深度组合相位扩散框架，将运动生成从原始空间迁移到统一的**相位潜空间**中。其核心设计包含三个关键模块：

- **ACT-PAE（动作中心周期性自编码器）**：将任意长度的运动片段编码为一组相位参数 $(\mathbf{F}, \mathbf{A}, \mathbf{B}, \mathbf{S})$，并通过正弦信号 $\mathbf{Q} = \mathbf{A} \sin(\mathbf{F} \cdot (T - \mathbf{S})) + \mathbf{B}$ 参数化，捕捉运动的内在周期性动态。
- **SPDM（语义相位扩散模块）**：利用 CLIP 文本嵌入作为条件，对当前运动片段的相位潜变量进行语义去噪，确保生成动作与文本描述对齐。
- **TPDM（过渡相位扩散模块）**：双向引入相邻片段的纯净相位潜变量，在扩散过程中逐步对齐过渡区域的相位参数，实现相邻动作间的平滑动态过渡。

在去噪过程中，通过相位混合方程 $\mathbf{P}_{.}^{0} = r \frac{\mathbf{P}_{.f}^{0} + \mathbf{P}_{.b}^{0}}{2} + (1 - r) \mathbf{P}_{.c}^{0}$ 动态融合语义预测与过渡预测，其中混合权重 $r = (k/K)^3$ 随去噪步长自适应变化。该框架可线性扩展至任意数量的运动片段，支持组合生成、运动内插和长时生成三种应用模式（图1）。

### 主要结果

在 **BABEL-TEACH** 数据集上的系统实验表明：

- **组合运动对生成**（Table 1）：TransPhase 在整体运动真实感（Overall FID: **0.782**）和文本对齐（Overall MMD: **4.711**）上均优于所有基线方法（次优：PCMDM FID 0.837, priorMDM FID 0.839）。
- **长时运动生成**（Table 2）：在包含 3164 个文本指令、总长 168 分钟的序列上，TransPhase 取得最优 Overall FID（**0.847**）和 MMD（**4.849**），显著优于 TEACH（FID 1.780）和 priorMDM（FID 1.536）。
- **无条件运动内插**（Table 3）：在 60/120/180 帧过渡长度下，L2-Vel 等过渡真实感指标均大幅领先基线。
- **条件运动内插**（Table 4）：在 60 帧和 120 帧过渡长度下取得最佳运动真实感（Smt.FID: **0.389** / **0.679**）和文本对齐。

### 方法定位

TransPhase 首次将周期性相位表征与扩散模型结合，在统一的相位潜空间内实现语义条件与相邻动态条件的并行去噪，解决了现有方法在原始运动空间中过渡建模的根本性缺陷。该方法属于**潜空间组合扩散**范式，与 **PCMDM**（Liu et al., 2024）的并行组合思路和 **priorMDM**（Zhang et al., 2024）的过渡生成策略形成对比，但通过相位空间建模实现了更优的过渡平滑性和语义一致性。

### 局限与展望

当前框架依赖两片段对的训练监督，对三个以上连续语义片段的组合或非相邻片段间的相位传播尚未充分验证。相位混合权重 $r$ 由启发式三次曲线定义，缺乏数据驱动的自适应机制。此外，模型在更大规模运动数据集（如 AMASS）上的泛化能力仍需检验。未来工作可探索基于分数或势能的扩散变体、可学习的相位混合参数，以及与物理约束（如 PhysDiff）的结合。



### 问题背景

生成符合文本描述的长时人体运动序列在动画制作、虚拟现实和具身智能等领域具有重要应用价值。随着扩散模型在运动生成领域取得显著进展，研究者逐渐从生成单一短动作转向合成由多个语义片段组合而成的长运动。然而，现有方法在组合多个语义片段时，普遍面临一个核心瓶颈：**过渡区域产生突兀伪影**，例如脚滑动（foot skating）、突然转向或不自然的姿态突变。

### 现有方法缺口

当前主流运动生成方法在组合多片段运动时，主要在**原始运动空间**（raw motion space）中建模过渡，具体表现为以下几类策略：

- **线性混合策略**：如 **MDM-30**（Tevet et al., 2023）和 **MLD-30**（Chen et al., CVPR 2023）在相邻片段的 30 帧重叠区域进行线性插值，该方法简单但无法建模复杂的过渡动态。
- **自回归生成策略**：如 **TEACH**（Shi et al., 2023）自回归地生成相邻片段及其过渡，再通过 SLERP 进行平滑，但误差会沿序列累积。
- **并行生成策略**：如 **PCMDM**（Liu et al., 2024）和 **priorMDM**（Zhang et al., 2024）尝试并行生成多个片段，但 priorMDM 在原始空间中独立生成语义片段后再生成过渡片段并插值，仍难以保证过渡的物理合理性。

这些方法的共同缺陷在于：**忽略了运动内在相位的动态连续性**。人体运动天然具有周期性特征（如行走的频率、摆臂的幅值），这些相位参数在动作切换时应当是平滑演化的。直接在原始关节旋转或位置空间中建模过渡，无法显式地对齐和传播这种相位动态，导致过渡区域的运动失真。

### 本文动机

针对上述问题，TransPhase 提出一个核心思路：**将运动从原始空间映射到统一的相位潜空间，在该空间内并行地进行语义条件扩散和相位动态对齐**。具体而言：

1. **相位潜空间编码**：利用 Action-Centric Periodic Autoencoder（ACT-PAE）将可变长运动片段编码为一组相位参数（频率 $F$、幅值 $A$、偏移 $B$、相移 $S$），并通过正弦参数化 $\mathbf{Q} = \mathbf{A} \sin(\mathbf{F} \cdot (T - \mathbf{S})) + \mathbf{B}$ 捕捉运动的内在周期性动态。
2. **双条件并行扩散**：在相位潜空间内，语义相位扩散模块（SPDM）负责文本语义对齐，过渡相位扩散模块（TPDM）双向引入相邻片段的纯净相位潜变量作为条件，在扩散去噪过程中逐步对齐过渡区域的相位参数。
3. **可扩展框架**：通过相位混合机制动态融合语义预测与过渡预测，使框架可线性扩展至任意数量的运动片段，同时适用于组合生成、运动内插和长时生成三种任务。

这一设计的关键洞察在于：**在周期性相位潜空间内进行双条件并行扩散，可以同步实现语义对齐和相位平滑过渡**，从根本上解决原始空间中过渡建模的局限性。



## 核心方法与创新机理

### 1. 瓶颈洞察：从原始空间组合到相位动态断裂

现有运动生成模型在处理多语义片段组合时，普遍直接在**原始运动空间**（raw motion space）进行拼接或过渡生成。代表性基线如 **MDM-30**（Tevet et al., 2023）和 **MLD-30**（Chen et al., CVPR 2023）采用线性混合 30 帧重叠区域的策略；**TEACH**（Shi et al., 2023）以自回归方式学习相邻片段过渡后接 SLERP 平滑；**priorMDM**（Zhang et al., 2024）先独立生成语义片段，再在原始空间生成过渡片段并插值。这些方法的共同缺陷在于忽略了运动内在的**相位动态连续性**，导致过渡区域频繁出现脚滑动（foot skating）、突然转向（sudden turn）等突兀伪影——这一瓶颈在 Figure 5 的定性对比中尤为明显，priorMDM 在坐下动作中出现不自然的突然旋转，TEACH 的行走动作则伴随脚部滑动。

### 2. 因果调控变量：统一相位潜空间与双条件并行扩散

TransPhase 的核心创新在于将调控变量从原始运动空间转移到**周期性相位潜空间**，并引入**双条件并行扩散机制**，具体体现为三个 changed slots：

| 方法槽位 | 基线取值 | TransPhase 取值 | 证据锚点 |
|---------|---------|----------------|---------|
| **运动表征空间** | 原始运动空间（raw motion） | ACT-PAE 编码的统一相位潜空间（phase latent，参数 $\mathbf{F},\mathbf{A},\mathbf{B},\mathbf{S}$） | Sec 3.1.1 |
| **过渡建模** | 原始空间线性混合或自回归生成过渡片段 | TPDM 双向相位动态调节，在扩散过程中迭代对齐相邻片段的相位参数 | Sec 3.2.1, 3.2.3 |
| **条件融合机制** | 仅使用文本语义条件 | 语义条件（SPDM）+ 相邻相位动态条件（TPDM），通过去噪步长相关的动态权重 $r$ 混合 | Sec 3.2.1, Eq. 2 |

### 3. 核心机制：ACT-PAE 与相位参数化解耦

**ACT-PAE**（Action-Centric Periodic Autoencoder）构建于 DeepPhase 之上，将可变长运动片段 $\mathbf{X} \in \mathbb{R}^{N \times E}$ 编码为四组相位参数——频率 $\mathbf{F}$、幅值 $\mathbf{A}$、偏移 $\mathbf{B}$ 和相移 $\mathbf{S}$，并通过正弦参数化将其转化为周期性信号：

$$\mathbf{Q} = \mathbf{A} \sin(\mathbf{F} \cdot (T - \mathbf{S})) + \mathbf{B}$$

这一表征的关键优势在于：**(1)** 将运动语义与过渡动态统一压缩到低维相位流形中，使扩散过程无需直接处理高维关节轨迹；**(2)** 周期性结构天然捕捉运动的节律特征，为相邻片段的相位对齐提供几何基础。

### 4. 双条件扩散：语义对齐与相位平滑的并行协同

框架通过两类扩散模块实现并行去噪：

- **SPDM**（Semantic Phase Diffusion Module）：以 CLIP 文本嵌入为条件，对当前运动片段的相位潜变量 $\mathbf{P}^k$ 进行语义去噪，确保生成动作与文本描述对齐。
- **TPDM**（Transitional Phase Diffusion Module）：以前向/后向两个实例分别接收相邻片段的**纯净相位潜变量** $\mathbf{P}^0$ 作为条件，对当前片段的相位潜变量进行过渡感知去噪，使当前去噪动作与相邻片段的运动动态保持一致。

两者的预测通过**相位混合方程**在每一步去噪中融合：

$$\mathbf{P}_{.}^{0} = r \frac{\mathbf{P}_{.f}^{0} + \mathbf{P}_{.b}^{0}}{2} + (1 - r) \mathbf{P}_{.c}^{0}$$

其中混合比 $r = (k/K)^3$（语义片段）或 $r = 1$（过渡片段），$k$ 为当前去噪步数，$K$ 为总步数。这一设计使去噪早期阶段更依赖语义引导以确定动作类型，后期逐渐增强相位动态约束以平滑过渡——消融实验（Sec 4.4）证实该三次曲线策略是最优配置。

### 5. 框架可扩展性：线性堆叠至任意片段数

TransPhase 的模块化设计使其可**线性扩展**：每增加一个运动片段，仅需添加对应的 SPDM 和一对 TPDM 模块，所有片段可并行去噪。在长时运动生成任务中（3164 个文本指令，168 分钟），框架通过堆叠模块实现了对超长序列的端到端生成，无需自回归累积误差。Table 2 显示该方法在 Overall FID（0.847）和 Overall MMD（4.849）上均优于 TEACH（1.780/4.984）、PCMDM（0.876/5.156）等基线，验证了扩展后的稳定性。

### 6. 创新边界与待验证假设

当前框架的创新存在以下边界条件，需在解读时保持审慎：

- **训练监督依赖**：模型在两片段对的监督下训练，对三个以上连续语义片段的组合或非相邻片段间的相位传播尚未充分验证。
- **混合权重的启发式设计**：$r = (k/K)^3$ 虽经消融验证有效，但缺乏数据驱动或任务感知的自适应机制，可能非全局最优。
- **数据集泛化性**：所有实验基于 BABEL-TEACH 数据集，在 AMASS 等更大规模运动数据集上的表现需进一步检验。



TransPhase 框架的核心设计动机源于一个关键瓶颈：现有运动生成模型在组合多个语义片段时，直接在原始运动空间建模，忽略了运动内在相位的动态连续性，导致过渡区域频繁出现脚滑动、突然转向等突兀伪影。为解决这一问题，框架将可变长运动片段统一编码到**周期性相位潜空间**中，并通过双条件并行扩散机制，在去噪过程中同步实现语义对齐与相位平滑过渡。

### 整体流水线

框架的输入为一系列可变长的运动片段 $\mathbf{X} \in \mathbb{R}^{N \times E}$（$N$ 为帧数，$E=269$ 为含 6D 旋转根轨迹的表示维度），以及对应的文本语义条件。流水线由三个核心模块构成：

1. **ACT-PAE（Action-Centric Periodic Autoencoder）**：作为运动表征的编解码枢纽。其编码器将每个运动片段映射为一组统一的相位潜变量 $\mathbf{P} = [\mathbf{F}, \mathbf{A}, \mathbf{B}, \mathbf{S}]$（频率、幅值、偏移、相移），并通过正弦参数化方程 $\mathbf{Q} = \mathbf{A} \sin(\mathbf{F} \cdot (T - \mathbf{S})) + \mathbf{B}$ 生成周期性信号 $\mathbf{Q}$，捕捉运动的内在相位动态。解码器则从 $\mathbf{Q}$ 重建原始运动序列。

2. **SPDM（Semantic Phase Diffusion Module，语义相位扩散模块）**：基于 CLIP-ViT-B/32 文本嵌入，对当前运动片段的相位潜变量执行语义条件去噪，确保生成的运动与文本描述对齐。

3. **TPDM（Transitional Phase Diffusion Module，过渡相位扩散模块）**：分为前向和反向两个子模块。前向 TPDM 利用前一片段的纯净相位潜变量 $\mathbf{P}_\mathbf{p}^0$ 对当前过渡片段的噪声潜变量 $\mathbf{P}_\mathbf{t}^k$ 进行去噪；反向 TPDM 则利用后一片段的纯净相位潜变量 $\mathbf{P}_\mathbf{s}^0$ 进行对称操作。这种双向相位动态调节机制使当前片段的去噪过程始终与相邻片段的运动动态保持一致。

### 模块协同与相位混合

在扩散去噪的每一步 $k$ 中，SPDM 和前后向 TPDM 分别输出各自的干净相位预测。这些预测通过**相位混合方程**进行融合：

$$\mathbf{P}_{.}^{0} = r \frac{\mathbf{P}_{.f}^{0} + \mathbf{P}_{.b}^{0}}{2} + (1 - r) \mathbf{P}_{.c}^{0}$$

其中 $\mathbf{P}_{.c}^{0}$ 为 SPDM 的语义预测，$\mathbf{P}_{.f}^{0}$ 和 $\mathbf{P}_{.b}^{0}$ 分别为前向和反向 TPDM 的过渡预测。混合权重 $r$ 采用与去噪步长相关的动态策略：对语义条件片段使用三次曲线 $r = (k/K)^3$，使早期去噪阶段以语义引导为主，后期逐步增强过渡一致性约束；对过渡片段则固定 $r=1$，完全依赖相邻片段的相位动态进行调节。

混合后的干净相位潜变量经 DDIM 调度器估计下一步潜变量，或经 ACT-PAE 解码器重建运动片段。最终，各运动片段通过线性混合拼接为完整的长序列输出。

### 应用模式的可扩展性

TransPhase 的模块化设计支持线性扩展至多种任务场景（如图 Figure 1 所示）：
- **组合运动生成**：同时合成多个语义片段，SPDM 和 TPDM 并行处理每个片段，确保语义准确与过渡平滑（对应 Figure 3 流水线）。
- **运动内插**：在给定的前后段之间生成过渡运动，TPDM 双向引入相邻片段的相位动态，可选 SPDM 实现条件内插（对应 Figure 4 流水线）。
- **长时运动生成**：通过堆叠更多的 SPDM/TPDM 模块，框架可直接扩展至任意数量的运动片段，实现超长序列（如 168 分钟）的并行生成。

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/001_Figure_1.jpg]]
*Figure 1: Our Compositional Phase Diffusion framework produces high-quality composite motion sequences with smooth transitions and semantic alignment. (a) Compositional generation involves synthesizing multiple motion segments of varying lengths simultaneously, ensuring smooth transitions between segments. (b) Motion inbetweening allows users to select segments (in blue and yellow) and create conditional or unconditional bridging motions. (c) Long-term motion generation is achieved by scaling the framework with additional modules, enabling the parallel denoising of a larger number of motion segments. The rainbow color indicates time progression*

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the phase diffusion pipeline for the compositional motion generation task. SPDMs and TPDMs guide the denoising of motion segments through semantic information and the phase dynamics information from adjacent motions, respectively. The denoised results are combined via phase mixing and either diffused back to step*

所有 SPDM 和 TPDM 均以 $\epsilon$-模型实现，训练过程遵循标准扩散框架的 L1 损失。这种统一的相位潜空间表征与双条件扩散机制的协同，构成了 TransPhase 在组合运动生成、运动内插和长时生成三大任务上取得一致优越性能的架构基础。



TransPhase 框架由三个核心模块构成：**动作中心周期性自编码器（ACT-PAE）**、**语义相位扩散模块（SPDM）** 和 **过渡相位扩散模块（TPDM）**。三者协同工作，在统一的相位潜空间内完成语义对齐与过渡平滑的双重目标。

### ACT-PAE：周期性相位编码与解码

ACT-PAE 是整个框架的基石，其核心作用是将可变长的原始运动片段映射到一个统一的相位潜空间。给定一段包含 $N$ 帧的运动 $\mathbf{X} \in \mathbb{R}^{N \times E}$（其中 $E=269$，包含关节位置、速度、旋转及根关节的 6D 旋转表示），编码器将其压缩为一组相位参数 $\mathbf{P} = [\mathbf{F}, \mathbf{A}, \mathbf{B}, \mathbf{S}]$，分别代表频率（Frequency）、幅值（Amplitude）、偏移（Offset）和相移（Phase Shift）。

这组参数随后被参数化为一个周期性正弦信号 $\mathbf{Q}$，以显式捕捉运动的内在相位动态：

$$
\mathbf{Q} = \mathbf{A} \sin(\mathbf{F} \cdot (T - \mathbf{S})) + \mathbf{B}
$$

其中 $T$ 为时间索引。解码器则从该周期性信号 $\mathbf{Q}$ 重建出原始运动 $\mathbf{X}$。这一设计的核心洞察在于：运动的过渡不自然（如脚滑动、突然转向）本质上是相位参数在边界处的不连续所致，而在相位潜空间中进行操作，为后续的平滑过渡建模提供了天然的数学接口。

### SPDM：语义条件相位去噪

SPDM 负责将文本语义条件注入去噪过程，确保生成的运动与用户指定的动作描述对齐。该模块采用预训练的 CLIP-ViT-B/32 模型将输入文本编码为嵌入向量 $\mathbf{C}$，并以此作为条件引导当前运动片段相位潜变量 $\mathbf{P}^k$ 的去噪过程。SPDM 实现为标准的 $\epsilon$-预测扩散模型，其训练损失为 L1 范数：

$$
\mathcal{L}_{\mathrm{S}} = \| \mathcal{F}_{\mathrm{S}}(k, \mathbf{C}_{\mathbf{p}}, \mathbf{P}_{\mathbf{p}}^k) - \epsilon_{\mathbf{p}} \|_1 + \| \mathcal{F}_{\mathrm{S}}(k, \mathbf{C}_{\mathbf{s}}, \mathbf{P}_{\mathbf{s}}^k) - \epsilon_{\mathbf{s}} \|_1
$$

其中 $\mathcal{F}_{\mathrm{S}}$ 为语义去噪函数，下标 $\mathbf{p}$ 和 $\mathbf{s}$ 分别表示前一片段和后一片段的对应量。该损失同时优化对前后两个相邻片段的去噪能力，使语义条件能够覆盖整个运动序列。

### TPDM：过渡感知相位动态调节

TPDM 是解决过渡区域运动伪影的关键模块。其核心思想是利用相邻片段的纯净相位潜变量（即无噪声的 $\mathbf{P}^0$）作为条件，在去噪过程中逐步将当前片段的相位参数向相邻片段的动态模式对齐。TPDM 分为前向和反向两个子模块：

- **前向 TPDM**：以 $\mathbf{P}_{\mathbf{p}}^0$ 为条件，对 $\mathbf{P}_{\mathbf{t}}^k$ 去噪，使过渡片段的动态向前一片段靠拢。
- **反向 TPDM**：以 $\mathbf{P}_{\mathbf{s}}^0$ 为条件，对 $\mathbf{P}_{\mathbf{t}}^k$ 去噪，使过渡片段的动态向后一片段靠拢。

前向 TPDM 的训练损失为：

$$
\mathcal{L}_{\mathrm{T}_f} = \| \mathcal{F}_{\mathrm{T}_f}(k, \mathbf{P}_{\mathbf{t}}^k, \mathbf{P}_{\mathbf{p}}^0) - \epsilon_{\mathbf{t}} \|_1 + \| \mathcal{F}_{\mathrm{T}_f}(k, \mathbf{P}_{\mathbf{s}}^k, \mathbf{P}_{\mathbf{t}}^0) - \epsilon_{\mathbf{s}} \|_1
$$

该损失同时训练模型对过渡片段和语义片段的去噪能力，确保相位动态信息的双向传播。

### 相位混合：双条件融合机制

在每个去噪步 $k$，SPDM 和两个 TPDM 分别产生各自的干净相位预测：$\mathbf{P}_{.c}^0$（语义预测）、$\mathbf{P}_{.f}^0$（前向过渡预测）和 $\mathbf{P}_{.b}^0$（反向过渡预测）。这三者通过相位混合方程融合为最终的干净相位潜变量：

$$
\mathbf{P}_{.}^{0} = r \frac{\mathbf{P}_{.f}^{0} + \mathbf{P}_{.b}^{0}}{2} + (1 - r) \mathbf{P}_{.c}^{0}
$$

混合权重 $r$ 的设计遵循以下原则：
- 对于语义条件片段，$r = (k/K)^3$，其中 $K$ 为总去噪步数。该三次曲线使得去噪早期（$k$ 较大时）过渡预测占主导，优先保证相位连续性；去噪后期（$k$ 较小时）语义预测权重增大，精细对齐文本条件。
- 对于过渡片段本身，$r = 1$，即完全依赖相邻片段的相位动态引导，不引入语义条件干扰。

融合后的 $\mathbf{P}_{.}^{0}$ 经 DDIM 调度器估计下一步的噪声潜变量 $\mathbf{P}_{.}^{k-1}$，或于最终步送入 ACT-PAE 解码器生成运动片段，再通过线性混合拼接为完整的长序列。

> **注意**：消融实验（Sec 4.4）验证了上述 $r = (k/K)^3$ 策略为最优配置，且 SPDM 与 TPDM 中引入帧级 token 能显著提升对参数级 token 的去噪性能。复合位置编码（Comp-PE）与混合时间窗（mixT）对可变长度运动编码至关重要，详见附录 A.2。

### 补充图表

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/002_Figure_2.jpg]]
*Figure 2: Module detail of TPDM and SPDM. (a) The TPDM uses the clean phase latents from the adjacent segment*

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/004_Figure_4.jpg]]
*Figure 4: The phase diffusion pipeline for the motion inbetweening tasks. The inbetweening motion*



## 实验与关键发现

### 核心实验设计

TransPhase 的实验体系围绕三个递进任务展开：**组合运动对生成**（验证双条件扩散的基本能力）、**长时运动生成**（验证框架的线性扩展性）和**运动内插**（验证相位过渡建模的泛化性）。所有实验均在 BABEL-TEACH 数据集上进行，统一采用 HumanML3D 格式（含 6D 旋转表示，特征维度 E=269），评估指标为标准 FID 与 MMD，并按语义段、过渡段和整体分别报告，规避评估偏差。

### 组合运动对生成：双条件扩散的基准验证

该任务要求同时生成两个语义不同的运动片段并平滑过渡。Table 1 的量化结果显示，TransPhase 在**整体运动真实感**（Overall FID=0.782）和**文本对齐**（Overall MMD=4.711）上均优于所有基线方法。具体而言：

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/006_Table_1.jpg]]
*Table 1: Quantitative results for Compositional Motion Pair Generation on the BABEL-TEACH test set. Bold and underline indicates the best and the second-best result*

- 相比直接在原始运动空间进行线性混合的扩散模型 **MDM-30**（Tevet et al., 2023）和 **MLD-30**（Chen et al., CVPR 2023），TransPhase 的整体 FID 分别降低了 0.364 和 0.319，过渡段 FID 的改善尤为显著（1.807 vs. 2.982/3.056），直接验证了**在相位潜空间建模过渡优于原始空间线性混合**的核心主张。
- 与自回归长运动生成方法 **TEACH**（Shi et al., 2023）相比，TransPhase 的整体 FID 降低 0.259，过渡段 FID 降低 0.432。TEACH 依赖 SLERP 进行后处理平滑，而 TransPhase 通过 TPDM 在扩散过程中双向对齐相位参数，从根本上消除了脚滑动等伪影（Figure 5 定性对比直观展示了这一差异：TEACH 的行走动作存在脚滑动，priorMDM 的坐下动作出现突然转向）。
- 与并行组合扩散方法 **PCMDM**（Liu et al., 2024）和两阶段方法 **priorMDM**（Zhang et al., 2024）相比，TransPhase 的整体 FID 分别降低 0.055 和 0.057。虽然差距缩小，但 TransPhase 在文本对齐（MMD=4.711 vs. 5.423/5.025）上优势明显，表明**相位潜空间的语义条件去噪比原始空间的条件建模更精确**。

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/005_Figure_5.jpg]]
*Figure 5: Compositional motion pair result visualization for [walk(2.4s), sit down(3.6s)]. The motion frames are colored from red to purple in a rainbow gradient to represent the progression of time. Note that priorMDM exhibits an unrealistic, sudden turn during the sit-down action, which is reflected in its low FID score. TEACH’s result includes footing skating in the walk motion. In contrast, our framework generates a fluid walking motion that transitions smoothly into a sit-down action*

**Figure 5** 的定性对比进一步揭示了失败模式：priorMDM 在坐下动作中产生不自然的突然转向，TEACH 的行走动作存在脚滑动，而 TransPhase 生成了流畅的行走并平滑过渡到坐下。这些伪影的消除直接归因于 TPDM 的双向相位动态调节机制——相邻片段的纯净相位潜变量在去噪过程中持续约束当前片段的动态连续性。

### 长时运动生成：框架的线性扩展能力

该任务将组合生成扩展至 3164 个文本指令、302298 帧（约 168 分钟）的超长序列。Table 2 的结果表明，TransPhase 在整体 FID（0.847）和整体 MMD（4.849）上均取得最优，且**性能不随序列长度增加而退化**：

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/007_Table_2.jpg]]
*Table 2: Quantitative results for Long-term Motion Generation on the BABEL-TEACH test set with a single extended text sequence of 3,164 texts (302,298 frames, 168 minutes). Bold and underline indicates the best and the second-best result*

- 相比 TEACH（自回归生成，误差逐段累积），TransPhase 的整体 FID 降低 0.933，MMD 降低 0.135。这验证了并行扩散框架在长序列上的稳定性——每个片段的去噪独立进行，仅通过相邻相位条件耦合，避免了自回归的误差传播。
- 相比 PCMDM（整体 FID=0.876），TransPhase 的优势虽小但一致（ΔFID=0.029），且文本对齐更优（MMD=4.849 vs. 5.156）。这表明在超长序列中，相位潜空间的语义压缩能力（ACT-PAE 将可变长运动编码为固定维度相位参数）比原始空间的潜在扩散更有效。

值得注意的是，TransPhase 在语义段 FID（0.773）和过渡段 FID（0.909）上均保持领先，证明**SPDM 的语义对齐和 TPDM 的相位平滑在长序列中协同工作，未出现性能折损**。

### 运动内插：相位过渡建模的泛化验证

运动内插任务分为无条件（UMIB）和条件（CMIB）两种设置，分别验证 TPDM 的过渡生成能力和 SPDM+TPDM 的联合能力。

#### 无条件运动内插（UMIB）

Table 3 报告了 60、120、180 帧三种过渡长度下的结果。TransPhase 在所有过渡长度下的 **L2-Vel**（运动速度连贯性）和 **NPSS**（过渡自然度）上均大幅领先基线：

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/009_Table_3.jpg]]
*Table 3: Quantitative results for Unconditional Motion Inbetweening (UMIB) on BABEL-TEACH [12] test set. We report the performance under settings of transition lengths at 60, 120, and 180 frames. Bold and underline indicates the best and the second-best result*

- 在 60 帧过渡中，L2-Vel=0.0101，相比 MDM 的 0.0251 降低 59.8%；在 120 帧过渡中，L2-Vel=0.0278，相比 priorMDM 的 0.0382 降低 27.2%。L2-Vel 直接衡量相邻帧的速度差异，该指标的显著改善证明**TPDM 的双向相位条件有效消除了过渡区域的突然加速/减速**。
- 在 180 帧过渡中，TransPhase 的 L2-Vel=0.0288 仍保持最低，而其他方法（如 MDM 和 priorMDM）的性能随过渡长度增加而恶化。这表明**TPDM 的相位动态调节对长过渡的鲁棒性优于原始空间的生成或插值方法**。

**Figure 6** 的定性可视化（蓝色为前段，绿色为过渡，黄色为后段）显示，TransPhase 的过渡动作在运动学上自然连贯，未出现基线方法中常见的僵硬衔接或突然转向。

#### 条件运动内插（CMIB）

Table 4 的结果表明，在引入文本条件（如“bend arms up”）后，TransPhase 在 60 帧和 120 帧过渡长度下取得最佳**运动真实感**（Smt.FID）和**文本对齐**（MMD）：

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/011_Table_4.jpg]]
*Table 4: Quantitative results for Conditional Motion Inbetweening (CMIB) on the BABEL-TEACH [12] test set. We report the performance of various methods under the settings of transition lengths at 60, 120, and 180 frames. Bold and underline indicates the best and the second-best result*

- 在 60 帧过渡中，Smt.FID=0.389，相比 CMB（Kim et al., 2022）的 0.693 降低 43.9%，相比 MDM 的 0.694 降低 43.9%。这表明**在相位潜空间中进行语义条件去噪比在原始空间生成过渡片段更精确**。
- 在 120 帧过渡中，TransPhase 的 Smt.FID=0.679 仍保持领先，但优势缩小。这可能是因为更长的过渡需要更强的语义约束，而 SPDM 的 CLIP 文本嵌入在长时序上的条件强度有限。

**Figure 7** 的定性可视化（条件为“bend arms up”）显示，TransPhase 生成的过渡动作在满足语义要求的同时保持了运动连贯性，而基线方法往往在语义对齐和运动平滑之间顾此失彼。

### 消融实验：关键设计的因果验证

消融实验（Sec 4.4 及 Appendix A.2）验证了三个关键设计的必要性：

1. **帧级 token 的引入**：在 SPDM 和 TPDM 中加入帧级 token（与参数级 token 互补）能显著提升去噪性能。移除帧级 token 后，过渡段的 FID 和 MMD 均出现明显恶化，证明**细粒度的时序信息对相位参数的去噪至关重要**。

2. **相位混合策略**：对语义条件片段使用 $r = (k/K)^3$（三次曲线），对过渡片段使用 $r=1$ 的配置是最优的。该策略的直觉是：在去噪早期（$k$ 大），过渡信息权重高以快速建立动态连贯性；在去噪后期（$k$ 小），语义信息权重高以精细对齐文本条件。实验表明，使用线性 $r$ 或恒定 $r$ 都会导致过渡平滑度或语义对齐度的下降。

3. **复合位置编码（Comp-PE）与混合时间窗（mixT）**：这两个设计对 ACT-PAE 编码可变长度运动至关重要。移除其中任一组件都会导致编码器无法有效捕捉不同长度片段的相位动态，进而影响下游扩散模块的性能。具体而言，Comp-PE 通过组合绝对和相对位置编码使模型感知帧在片段内的位置，mixT 通过多尺度时间窗捕捉不同频率的周期性模式。

### 失败模式与局限性分析

尽管 TransPhase 在所有任务上均取得最优，但以下局限性值得关注：

1. **多片段组合的未验证性**：当前框架依赖两片段对的训练监督（SPDM 处理前后片段，TPDM 处理相邻片段对），对三个以上连续语义片段的组合或非相邻片段之间的相位传播尚未充分验证。在长时生成任务（Table 2）中，虽然序列包含 3164 个片段，但每个片段仅与直接相邻片段通过 TPDM 耦合，远距离的相位一致性缺乏显式建模。

2. **数据集泛化性**：所有实验基于 BABEL-TEACH 数据集，该数据集的运动类型和过渡模式可能具有特定偏差。模型在更大规模的运动数据集（如 AMASS）上的泛化能力仍需检验，尤其是在包含更多样化运动风格和非周期性动作的场景下。

3. **启发式混合权重的次优性**：相位混合权重 $r = (k/K)^3$ 由启发式三次曲线定义，缺乏数据驱动或任务感知的自适应机制。在条件运动内插的 120 帧过渡中（Table 4），TransPhase 的优势缩小，可能部分归因于固定混合策略无法根据过渡长度和语义复杂度动态调整语义与过渡信息的权衡。

4. **物理约束的缺失**：虽然 TPDM 通过相位对齐减少了脚滑动等伪影，但 TransPhase 未显式引入物理约束（如接触力、地面穿透惩罚）。在极端过渡场景（如从跑步到突然停止）中，生成的过渡可能仍存在微小的物理不合理性。与 PhysDiff 等物理约束扩散模型的结合是潜在的改进方向。

### 补充图表

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of the UMIB with 120 transition frames: preceding motion in blue, transitioning motion in green, and succeeding motion in yellow*

![[assets/figures/papers/paper_list_l1920_TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_G/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of the CMIB with 120 transition boundary frames conditioned with bend arms up: preceding motion in blue, transitioning motion in green, and succeeding motion in yellow*



## 定位与知识库关联

### 1. 任务定位与基线谱系

TransPhase 瞄准人类运动生成中一个被多数方法忽略的瓶颈：**组合多个语义片段时，过渡区域的动态连续性与自然感**。现有方法可大致归为三类基线谱系，它们均在原始运动空间（raw motion space）内完成片段组合或过渡，从而暴露了相位动态失配的根本缺陷。

**单文本条件扩散 + 线性混合**：以 **MDM**（Tevet et al., 2023）和 **MLD**（Chen et al., CVPR 2023）为代表。这类方法独立生成各语义片段，然后在原始运动空间中对 30 帧重叠区域进行线性混合。其根本问题在于，线性混合仅对关节位置做数值插值，完全忽略运动内在的周期性相位动态（频率、幅值、相移），导致过渡段出现脚滑动、突然转向等突兀伪影。

**自回归长运动生成 + 后处理平滑**：**TEACH**（Shi et al., 2023）学习相邻片段间的过渡生成，随后采用 SLERP 进行后处理平滑。虽然自回归机制引入了对相邻片段的显式建模，但过渡生成与平滑仍然在原始运动空间内完成，未能触及运动的相位本质。

**并行组合扩散**：**PCMDM**（Liu et al., 2024）和 **priorMDM**（Zhang et al., 2024）代表了更近期的并行生成思路。PCMDM 在原始空间内并行生成多个语义片段，priorMDM 则先独立生成语义片段，再在原始空间生成过渡片段并插值。尽管并行机制提升了效率，但它们依然在原始运动空间内建模过渡，无法实现相位层面的动态对齐。

在运动内插（motion inbetweening）子任务中，**CMB**（Kim et al., 2022）作为条件运动内插基线，同样在原始空间内操作，缺乏对相位连续性的显式约束。

### 2. 核心范式转换：从原始空间到相位潜空间

TransPhase 的方法论创新在于完成了一次**表征空间的范式转换**——将组合运动生成从原始运动空间迁移到统一的相位潜空间（phase latent manifold）。这一转换通过三个关键槽位（slot）的替换实现：

| 方法槽位 | 基线做法 | TransPhase 做法 | 证据锚点 |
|---------|---------|----------------|---------|
| **运动表征空间** | 原始运动空间（raw motion） | ACT-PAE 编码的统一相位潜空间（参数 F, A, B, S） | Sec 3.1.1 |
| **过渡建模** | 原始空间线性混合或自回归生成过渡片段 | TPDM 双向相位动态调节，在扩散过程中迭代对齐相邻片段的相位参数 | Sec 3.2.1, 3.2.3 |
| **条件融合机制** | 仅使用文本语义条件 | 语义条件（SPDM）+ 相邻相位动态条件（TPDM），通过去噪步长相关的动态权重 r 混合 | Sec 3.2.1, Eq. 2 |

这一范式转换的因果机制可概括为：ACT-PAE 将可变长运动片段编码为频率 F、幅值 A、偏移 B 和相移 S 四组相位参数，并通过正弦信号 $\mathbf{Q} = \mathbf{A} \sin(\mathbf{F} \cdot (T - \mathbf{S})) + \mathbf{B}$ 参数化为周期性表征（Eq. 1）。在此相位潜空间内，SPDM 引入 CLIP 文本嵌入进行语义条件去噪，TPDM 则双向引入相邻片段的纯净相位潜变量作为动态条件——前向 TPDM 利用前一相邻片段的相位动态调节当前片段，后向 TPDM 利用后一相邻片段的相位动态进行对称约束。两者预测通过相位混合方程 $\mathbf{P}_{.}^{0} = r \frac{\mathbf{P}_{.f}^{0} + \mathbf{P}_{.b}^{0}}{2} + (1 - r) \mathbf{P}_{.c}^{0}$（Eq. 2）动态融合，其中混合比 $r = (k/K)^3$ 随去噪步长 k 递减，使早期去噪侧重语义对齐、后期去噪侧重相位平滑过渡。

### 3. 知识库定位与框架适用边界

**与 DeepPhase 的继承关系**：ACT-PAE 构建于 **DeepPhase**（Starke et al., 2022）之上，继承了周期性相位编码的核心思想。但 TransPhase 的关键推进在于：DeepPhase 仅用于运动分解与周期性分析，而 TransPhase 将相位潜空间作为扩散模型的生成空间，并引入双条件（语义 + 过渡）去噪机制，使相位表征从分析工具升格为生成控制的核心载体。

**与扩散模型谱系的关系**：SPDM 和 TPDM 均实现为 $\epsilon$-模型（$\epsilon$-model），遵循 DDIM（Song et al., 2021）的去噪调度框架。TransPhase 的贡献不在于扩散算法本身的创新，而在于**将扩散过程适配到相位潜空间的独特几何结构**，并通过相位混合机制实现语义条件与过渡条件的协同。

**框架的线性扩展性**：TransPhase 的一个显著优势是其模块化设计天然支持线性扩展。对于 N 个语义片段的组合生成，只需部署 N 个 SPDM 和 2(N-1) 个 TPDM 进行并行去噪，无需重新训练或架构修改。这一特性在长时运动生成任务（Table 2，3164 个文本指令，168 分钟运动）中得到验证。

**适用边界与局限**：

1. **片段数量上限未充分验证**：当前框架依赖两片段对的训练监督（paired segment training），对三个以上连续语义片段的组合或非相邻片段间的相位传播，尚未经过充分实验验证。尽管框架理论上可线性扩展，但误差累积效应在极长序列中的影响仍属未知。

2. **数据集泛化能力待检验**：所有实验基于 BABEL-TEACH 数据集，模型的泛化能力在其他大规模运动数据集（如 AMASS）上仍需验证。不同数据集的运动风格分布、动作类型覆盖度可能影响相位潜空间的表征质量。

3. **相位混合权重的启发式设计**：混合比 r 由三次曲线 $r = (k/K)^3$ 定义，缺乏数据驱动或任务感知的自适应机制。消融实验（Sec 4.4）表明该配置在语义片段上最优，但过渡片段采用 r=1 的固定策略可能不是全局最优解。

4. **物理约束的缺失**：尽管 TransPhase 在过渡真实感指标上大幅领先基线（Table 3, L2-Vel），但框架本身不包含显式的物理约束（如足部接触、关节限位）。与 **PhysDiff**（Yuan et al., 2023）等物理感知扩散模型的结合，可能进一步消除残留的脚滑动等伪影。

### 4. 开放问题

1. **扩散范式升级**：当前框架采用 DDIM 调度，能否迁移至基于分数（score-based）或势能（potential-based）的扩散框架以进一步提升生成质量？相位潜空间的周期性结构可能为设计特殊的前向过程提供新的自由度。

2. **自适应相位混合**：是否可以设计可学习的相位混合参数或注意力机制，在去噪过程中根据当前片段的语义特征和相邻片段的相位差异，自适应地权衡语义信息与过渡信息？这有望替代当前启发式的三次曲线策略。

3. **非周期性动作的扩展**：ACT-PAE 的正弦参数化天然适用于周期性或准周期性动作（如行走、跑步），但对于非周期性动作（如跳跃、投掷）的相位表征质量如何？是否需要在相位潜空间中引入非周期性的补充编码通道？

4. **物理约束集成**：在保留相位平滑优势的前提下，如何将物理约束（如 PhysDiff 的物理引导机制）嵌入相位扩散过程？物理约束可能在相位潜空间中有其对应的表达形式，而非仅在解码后的原始运动空间施加。



## 原文 PDF

![[paperPDFs/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation.pdf]]

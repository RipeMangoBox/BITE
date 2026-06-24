---
title: Multi-level Causal LLM-based Text-to-Motion Generation with Human Alignment
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multi_level_Causal_LLM_based_Text_to_Motion_Generation_with_Human_Alignment.pdf
aliases:
- MLCLBTMGHA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入Causal RVQ-VAE实现多级因果运动量化，采用时间滞后因果预测在并行解码中维持严格因果依赖，并通过MHPO动态加权层级语义相似度进行人类偏好对齐。
primary_logic: 多级残差因果量化与时间滞后预测策略弥合了因果LLM与运动模态之间的因果表示鸿沟；结合多级混合加权偏好优化，将细粒度人类偏好信号有效注入训练，显著提升运动生成的真实性与语义对齐度。
claims:
- MoTiGA在HumanML3D上将FID从0.232降至0.041，相对其他LLM方法提升82.3%。
- MoTiGA在KIT-ML上将FID从0.510降至0.180，相对其他LLM方法提升64.7%。
- 将标准VQ-VAE替换为Causal RVQ-VAE，生成FID从0.213提升至0.186。
- 时间滞后因果预测在FID(0.041)和R-Precision(52.3)上均优于时间同步并行(0.064, 51.0)与逐步解码。
---

# Multi-level Causal LLM-based Text-to-Motion Generation with Human Alignment

> [!tip] 核心洞察
> 多级残差因果量化与时间滞后预测策略弥合了因果LLM与运动模态之间的因果表示鸿沟；结合多级混合加权偏好优化，将细粒度人类偏好信号有效注入训练，显著提升运动生成的真实性与语义对齐度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于多级因果LLM的文本到动作生成与人类对齐 |
| 英文题名 | Multi-level Causal LLM-based Text-to-Motion Generation with Human Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Multi-level_Causal_LLM-based_Text-to-Motion_Generation_with_Human_Alignment_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | MoTiGA |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.041 vs 0.232 (MotionGPT, LLM-based) (-0.191 (82.3%↓))。
> - KIT-ML 上，FID 0.180 vs 0.510 (MotionGPT, LLM-based) (-0.330 (64.7%↓))。
> - HumanML3D (with initial pose) 上，FID 0.040 vs 0.493 (MotionGPT) (-0.453)。

## 概述

文本驱动的三维人体动作生成旨在从自然语言描述中合成逼真、语义一致的运动序列。近年来，基于大型语言模型（LLM）的方法因其强大的序列建模能力而备受关注，但现有方案普遍面临一个核心瓶颈：**运动量化器与因果语言模型之间存在因果性失配**。具体而言，主流的非因果VQ-VAE在运动离散化过程中引入细粒度量化误差，且其编码方式未能保持严格的时间因果依赖，导致LLM在生成运动令牌时缺乏可靠的因果先验。此外，现有方法普遍缺少显式的人类偏好对齐机制，使得生成动作在语义一致性与细节真实度上难以满足人类预期。

针对上述问题，本文提出 **MoTiGA**（Multi-level Causal LLM-based Text-to-Motion Generation with Human Alignment），以**多级因果运动量化**和**人类偏好对齐**两条主线重构LLM-based动作生成范式。其核心思路是：通过Causal RVQ-VAE建立多级残差因果运动表示，弥合因果LLM与运动模态之间的表示鸿沟；同时引入时间滞后因果预测策略，在并行解码中维持严格的层级因果依赖；在此基础上，以多级混合加权偏好优化（MHPO）将细粒度人类偏好信号注入训练，实现生成动作与人类预期的有效对齐。

实验结果表明，MoTiGA在HumanML3D数据集上将FID从LLM-based方法的最佳结果0.232降至**0.041**，相对提升82.3%；在KIT-ML上将FID从0.510降至**0.180**，相对提升64.7%，显著超越了包括MotionGPT、MotionLLM在内的现有LLM-based方法以及T2M-GPT、MoMask等专用方法。消融实验进一步验证了Causal RVQ-VAE、时间滞后因果预测和MHPO各组件的独立贡献。

## 背景与动机

### 文本驱动人体动作生成的任务定义

文本驱动的人体动作生成（Text-to-Motion Generation）旨在根据自然语言描述 $X = (x_1, x_2, ..., x_N)$ 合成逼真且语义一致的 3D 人体动作序列 $\mathcal{M}' = (m'_1, m'_2, ..., m'_{T'})$。该任务在游戏动画、虚拟人交互、影视预演等领域具有广泛的应用前景，其核心挑战在于跨模态语义对齐与动作细节的真实性。

### LLM-based 方法的兴起与瓶颈

近年来，大规模语言模型（LLM）的推理能力被引入动作生成领域，形成了以 **MotionGPT**（Zhang et al., AAAI 2024）、**MotionLLM** 等为代表的 LLM-based 方法。这些方法通常将动作量化为离散 token，再利用预训练语言模型进行序列建模。然而，现有 LLM-based 方法存在三个关键瓶颈：

**瓶颈一：非因果 VQ-VAE 的细粒度量化误差。** 现有方法普遍采用标准 VQ-VAE 或简单残差 VQ（RVQ）进行动作量化，这些量化器缺乏因果约束，无法在量化过程中保持动作帧之间的时序依赖关系，导致细粒度动作细节（如手指运动、脚步节奏）在量化-重建过程中严重丢失。

**瓶颈二：因果语言模型与运动表示之间的因果性不匹配。** LLM 本质上是因果模型，其自回归生成依赖于严格的时序因果链。然而，标准 RVQ 的多级 token 之间不存在因果依赖关系，当 LLM 以并行方式预测多级 token 时，会破坏运动模态固有的层级时序结构，造成“因果表示鸿沟”（causal representation gap）。

**瓶颈三：缺乏显式的人类偏好对齐机制。** 现有 LLM-based 方法仅依赖指令微调（instruction tuning），缺少对人类偏好的显式建模。这导致生成的动作虽然在统计指标上可能合理，但常出现语义错位（如“向右走”生成“向左走”）、动作幅度失当、节奏不自然等违背人类直觉的错误，如图 Figure 2(b) 所示。

### 本文动机

针对上述三个瓶颈，本文提出 **MoTiGA**（Multi-level Causal LLM-based Text-to-Motion Generation with Human Alignment），核心动机包括：

1. **弥合因果表示鸿沟**：设计 Causal RVQ-VAE，通过因果卷积在多级残差量化中建立严格的时序因果依赖，使动作 token 序列与 LLM 的因果推理范式内在一致。
2. **实现高效因果并行解码**：提出时间滞后因果预测策略，在保持因果约束的前提下允许跨层级并行预测，兼顾生成质量与推理效率。
3. **注入细粒度人类偏好信号**：构建 HumanML3D-R 偏好数据集，提出多级混合加权偏好优化（MHPO），利用层级自适应语义奖励将人类偏好信号有效注入 LLM 训练，提升动作的真实性与语义对齐度。

实验表明，MoTiGA 在 HumanML3D 上将 FID 从 0.232 降至 0.041（相对其他 LLM 方法提升 82.3%），在 KIT-ML 上从 0.510 降至 0.180（提升 64.7%），显著缩小了 LLM-based 方法与专用方法之间的性能差距。

## 核心创新

MoTiGA 的核心创新可归纳为三个相互耦合的“改动槽”（changed slots），它们共同解决了现有 LLM-based 文本到动作生成方法中**因果表示鸿沟**与**人类偏好对齐缺失**两大瓶颈。

### 1. 从非因果 VQ-VAE 到 Causal RVQ-VAE：多级因果运动量化

现有 LLM-based 方法（如 **MotionGPT** (Zhang et al., AAAI 2024)、**MotionLLM**）普遍采用标准 VQ-VAE 或简单残差 VQ（RVQ）进行运动量化，这类量化器在编码时缺乏严格的因果约束，导致细粒度量化误差累积，且与因果语言模型的推理范式存在根本性不匹配。

MoTiGA 提出 **Causal RVQ-VAE**，其核心改动在于：

- **多级残差量化（V=4）**：采用 V 个共享码本进行迭代残差量化，基础级（v=1）捕捉运动的全局粗粒度结构，后续残差级（v=2,3,4）逐步编码细粒度细节。消融实验表明，V=4 时达到最佳生成 FID 0.055 和重建 FID 0.031（Table 5）。
- **因果卷积编码**：在编码器中引入因果卷积，确保每一帧的量化仅依赖过去帧信息，从而建立严格的时间因果依赖。这一设计使得运动令牌序列天然适配因果语言模型的逐令牌生成范式。

**证据强度**：将标准 VQ-VAE 替换为 Causal RVQ-VAE 后，生成 FID 从 0.213 提升至 0.186（Table 4），验证了因果量化对生成质量的直接增益。需注意，Causal RVQ-VAE 的重建 FID 略高于标准 RVQ-VAE，表明因果约束在纯重建场景下可能引入轻微细节损失。

### 2. 从逐步自回归到时间滞后因果并行预测

传统 LLM-based 方法采用逐步自回归解码，每次仅预测单个令牌，推理效率低下。若直接改为多级令牌并行预测（时间同步并行），则会破坏 Causal RVQ-VAE 建立的因果依赖——当前时刻的细层级令牌需要依赖同一时刻的粗层级令牌，但并行预测时该依赖信息尚未生成，如公式所示：

$$P ( b _ { t + 1 } ^ { v + 1 } \mid b _ { 1 : t } ^ { 1 : v + 1 } , X , \Gamma ) \neq P ( b _ { t + 1 } ^ { v + 1 } \mid b _ { t + 1 } ^ { 1 : v } , b _ { 1 : t } ^ { 1 : v + 1 } , X , \Gamma )$$

MoTiGA 的 **时间滞后因果预测** 策略通过引入层级间的时间偏移来解决这一矛盾：粗层级令牌（如 b¹）预测未来时间步（如 t₄），细层级令牌（如 b⁴）预测较早时间步（如 t₁），使得每个令牌在生成时其因果依赖的令牌均已就绪，从而在保持严格因果性的前提下实现多级并行解码（Figure 4）。

**证据强度**：时间滞后因果预测在 FID（0.041）和 R-Precision Top-1（52.3）上均优于时间同步并行（0.064, 51.0）和逐步解码（Table 4），证实了因果性维护对生成质量和语义对齐的关键作用。

### 3. 从无偏好对齐到多级混合加权偏好优化（MHPO）

现有方法仅依赖指令微调，缺乏显式的人类偏好信号注入，导致生成动作常出现语义错位（如“向右移动”生成为“向左移动”，Figure 2b）。

MoTiGA 的 **MHPO** 在 GRPO（Group Relative Policy Optimization）框架基础上引入两个关键创新：

- **层级自适应奖励塑造**：利用预训练 TMR 模型计算文本 X 与解码自前 v 级令牌的运动 Mᵛ 之间的语义相似度 δᵛ，作为令牌级自适应奖励增量。对于人类偏好样本，基础级令牌获得奖励 $(1-\alpha) r_i + \alpha \delta^1$，残差级令牌获得增量奖励 $(1-\alpha) r_i + \alpha (\delta^v - \delta^{v-1})$，从而激励各级令牌逐步提升语义一致性。对于非偏好样本，施加惩罚性奖励 $(1-\alpha) r_j + \alpha (1-\delta^V)(-1)$。
- **正负优势分离标准化**：对正负样本的动态奖励分别进行零填充标准化，得到正向优势估计 $\hat{A}^+$ 和负向优势估计 $\hat{A}^-$，再组合为 PPO-style 最终优化目标。

**证据强度**：添加 MHPO 后取得最优整体结果（FID 0.041），且优于无对齐基线及标准 GRPO（Table 4）。权重因子 α=0.6 时效果最佳（Table 6），表明层级语义增量与全局二值奖励的混合加权对对齐效果有显著影响。

### 创新点耦合关系

三个改动槽并非孤立改进，而是形成因果链条：**Causal RVQ-VAE** 提供因果运动表示基础 → **时间滞后因果预测** 在保持该因果性的前提下实现高效并行解码 → **MHPO** 利用多级令牌的层级语义信息进行细粒度人类偏好对齐。这种协同设计使得 MoTiGA 在 HumanML3D 上将 FID 从 0.232 降至 0.041（相对 LLM-based 方法提升 82.3%），在 KIT-ML 上从 0.510 降至 0.180（提升 64.7%），同时 R-Precision Top-1 分别达到 52.3 和 44.3（Table 1）。

## 整体框架

MoTiGA 的整体设计围绕一个核心矛盾展开：**因果语言模型（LLM）与运动模态之间的因果表示鸿沟**。现有 LLM‑based 方法直接套用非因果 VQ‑VAE 量化运动序列，再交由因果 LLM 进行自回归生成，这一做法在量化阶段引入了细粒度误差，在生成阶段又破坏了运动本身的因果结构，最终导致语义漂移和细节失真。MoTiGA 的应对策略是将“因果性”与“人类偏好对齐”同时注入运动表示、生成策略和优化目标三个层面，形成一条端到端的因果对齐流水线。

图 3 给出了 MoTiGA 的完整框架，其信息流可概括为以下三个阶段：

1. **Causal RVQ‑VAE Tokenizer（多级因果运动量化）**  
   输入为原始 3D 运动序列，输出为多级因果运动令牌。与标准 RVQ‑VAE 不同，该模块在残差量化的每一级都引入因果卷积，确保当前时刻的细粒度令牌仅依赖过去时刻的粗粒度令牌，从而在离散化阶段就建立起严格的层级因果依赖。

2. **Time‑lagged Causal Prediction（时间滞后因果并行预测）**  
   量化后的多级令牌序列被送入 Llama 7B 因果语言模型。由于标准的时间同步并行预测会破坏 Causal RVQ‑VAE 建立的因果结构（见式 (1)），MoTiGA 采用时间滞后策略：粗层级令牌预测未来时间步，细层级令牌预测较早时间步，多个并行 Neck 网络分别负责不同层级的预测头。这一设计在保持因果性的前提下实现了多级令牌的并行解码，兼顾了生成效率与因果一致性。

3. **Multi‑level Hybrid‑weighted Preference Optimization（MHPO 人类偏好对齐）**  
   在指令微调阶段之后，MoTiGA 引入 MHPO 进行偏好对齐。该模块以 GRPO（式 (2)）为基础框架，但将标准二值奖励扩展为令牌级动态奖励：对于人类偏好样本，奖励由全局二值奖励与层级自适应语义增量加权构成（式 (3)）；对于非偏好样本，则施加由全层级语义相似度决定的惩罚项（式 (5)）。语义增量通过预训练的 TMR 模型计算文本与逐级解码运动之间的相似度得到（式 (4)），从而将细粒度的人类偏好信号有效注入 LLM 的生成过程。

三个模块之间形成强因果耦合：Causal RVQ‑VAE 定义了多级因果令牌空间，时间滞后预测严格遵循这一空间的因果约束进行解码，而 MHPO 则利用同一多级令牌结构对不同层级的生成质量进行差异化奖励，最终使 MoTiGA 在 HumanML3D 上将 FID 从 0.232 降至 0.041，相对其他 LLM‑based 方法提升 82.3%。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/003_Figure_3.jpg]]
*Figure 3: The framework of MoTiGA: (1) Time-lagged Causal Prediction, maintaining strict causality and hierarchical temporal dependencies across different levels; (2) Causal RVQ-VAE Tokenizer, discretizing 3D motion sequences into multi-level motion tokens; and (3) Human Alignment using Multi-level Hybrid-weighted Preference Optimization (MHPO)*

## 核心模块与公式推导

MoTiGA 的核心架构由三个紧密耦合的模块构成：**Causal RVQ-VAE Tokenizer**（多级因果运动量化）、**Time-lagged Causal Prediction**（时间滞后因果预测）与 **MHPO**（多级混合加权偏好优化）。这三个模块分别解决了现有 LLM-based 方法在运动表示、解码策略与人类偏好对齐三个层面的根本性缺陷。

### 3.1 Causal RVQ-VAE Tokenizer

现有 LLM-based 方法普遍采用标准 VQ-VAE 或简单 RVQ 进行运动量化，其量化过程不具有因果约束，导致细粒度运动细节在量化时产生不可忽略的误差。MoTiGA 提出 Causal RVQ-VAE，在残差量化的每一级引入因果卷积，确保当前时刻的量化仅依赖于过去时刻的信息，从而建立严格的时间因果依赖关系。

具体而言，Causal RVQ-VAE 使用 $V=4$ 个共享码本进行多级残差量化：基础级（$v=1$）捕捉运动的全局粗粒度结构，后续残差级（$v=2,3,4$）逐级补充细粒度细节。这种多级因果量化机制使得运动令牌序列天然具备层级化因果结构——粗粒度令牌 $b^1_t$ 在时间上先于同帧的细粒度令牌 $b^4_t$ 被确定，为后续的因果解码策略提供了表示基础。

### 3.2 Time-lagged Causal Prediction

标准的多级并行预测策略在同一时间步同时预测所有层级的运动令牌，这会破坏 Causal RVQ-VAE 建立的因果依赖关系。MoTiGA 通过公式严格刻画了这一因果违背问题：

$$P ( b _ { t + 1 } ^ { v + 1 } \mid b _ { 1 : t } ^ { 1 : v + 1 } , X , \Gamma ) \neq P ( b _ { t + 1 } ^ { v + 1 } \mid b _ { t + 1 } ^ { 1 : v } , b _ { 1 : t } ^ { 1 : v + 1 } , X , \Gamma )$$

该公式表明，时间同步并行预测因缺失当前时刻 $t+1$ 的粗层令牌 $b_{t+1}^{1:v}$ 而无法正确建模条件概率，违背了 Causal RVQ-VAE 中粗层级令牌在因果上先于细层级令牌的依赖关系。

为解决这一问题，MoTiGA 提出**时间滞后因果预测策略**：在并行预测多级令牌时，为不同层级引入时间偏移——粗粒度令牌（如 $b^1$）预测未来时间步（如 $t_4$），而细粒度令牌（如 $b^4$）预测较早时间步（如 $t_1$）。这种策略在保持多级并行解码效率的同时，严格维护了 Causal RVQ-VAE 的因果结构。消融实验证实，时间滞后因果策略在 FID（0.041）和 R-Precision Top-1（52.3）上均显著优于时间同步并行策略（0.064, 51.0）和逐步自回归解码。

### 3.3 Multi-level Hybrid-weighted Preference Optimization (MHPO)

现有 LLM-based 方法仅通过指令微调进行训练，缺乏显式的人类偏好信号。MoTiGA 在 GRPO（Group Relative Policy Optimization）框架基础上引入多级混合加权偏好优化。

GRPO 的基础目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o|} \sum_{t=1}^{|o|} \min\left( w_{i,t}(\theta) \hat{A}_{i,t}, \operatorname{clip}_{1-\epsilon}^{1+\epsilon}(w_{i,t}(\theta)) \hat{A}_{i,t} \right) \right]$$

其中 $G$ 为群组大小，$w_{i,t}(\theta)$ 为重要性采样权重，$\hat{A}_{i,t}$ 为优势估计，$\epsilon$ 控制裁剪范围。

MHPO 的核心创新在于为每个令牌设计**层级感知的动态奖励**。对于人类偏好样本，令牌级正向奖励定义为：

$$\hat{r}_{i,t}^{+} = \begin{cases} (1-\alpha) r_i + \alpha \delta^v, & o_{i,t} \in b^v, v=1, \\ (1-\alpha) r_i + \alpha (\delta^v - \delta^{v-1}), & o_{i,t} \in b^v, v \in [2,V]. \end{cases}$$

其中 $r_i$ 为全局二值奖励（偏好样本为 1），$\alpha$ 为混合权重因子，$\delta^v$ 为层级自适应奖励增量。对于基础级令牌（$v=1$），奖励直接加入 $\delta^1$；对于残差级令牌（$v \geq 2$），奖励加入该层级相对于上一级的**语义增量** $\delta^v - \delta^{v-1}$。这种设计使得不同层级的令牌根据其对语义的边际贡献获得差异化的奖励信号。

层级自适应奖励增量 $\delta^v$ 通过预训练的 TMR 运动检索模型计算文本与解码运动之间的语义相似度：

$$\delta^v = S_{[0,1]}(X, M^v) = S_{[0,1]}(X, \mathcal{D}(\sum_{k=1}^{v} b^k))$$

其中 $X$ 为输入文本，$M^v$ 为由前 $v$ 级令牌解码得到的运动，$\mathcal{D}$ 为 Causal RVQ-VAE 的解码器，$S_{[0,1]}$ 为归一化到 $[0,1]$ 区间的语义相似度函数。

对于非偏好样本，令牌级负向奖励定义为：

$$\hat{r}_{j,t}^{-} = (1-\alpha) r_j + \alpha (1-\delta^{V})(-1)$$

其中 $r_j$ 为基础负奖励，$(1-\delta^V)$ 为全层级语义相似度决定的惩罚强度——语义偏离越大，惩罚越重。

获得正负样本的动态奖励后，MHPO 分别对其进行零填充和标准化以得到优势估计：

$$\hat{A}^{+} = \mathcal{N}(\{\hat{r}_{i=1}^{+}, \dots, \hat{r}_{i=n}^{+}, 0_{i=n+1}, \dots, 0_{G}\})$$

$$\hat{A}^{-} = \mathcal{N}(\{\hat{r}_{j=1}^{-}, \dots, \hat{r}_{j=G-n}^{-}, 0_{j=G-n+1}, \dots, 0_{G}\})$$

最终，MHPO 将正负优势项组合为 PPO 风格的优化目标：

$$\mathcal{T}_{\mathrm{MHPO}}(\theta) = \mathbb{E}\bigg[\frac{1}{G}\bigg(\sum_{i=1}^{n}\frac{1}{|o|}\sum_{t=1}^{|o|}\min_{1-\epsilon}(\mathrm{clip}(w_{i,t}(\theta))\hat{A}_{i,t}^{+}, w_{i,t}(\theta)\hat{A}_{i,t}^{+}) + \sum_{j=1}^{G-n}\frac{1}{|o|}\sum_{t=1}^{|o|}\min(\mathrm{clip}(w_{j,t}(\theta))\hat{A}_{j,t}^{-}, w_{j,t}(\theta)\hat{A}_{j,t}^{-})\bigg)\bigg]$$

消融实验表明，混合权重因子 $\alpha=0.6$ 时 MHPO 达到最优效果（FID 0.041），且多级奖励塑造策略显著优于标准 GRPO，验证了层级感知的偏好信号对运动生成质量的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of different prediction strategies. Different colored tokens represent motion tokens at different hierarchical levels quantized by the Causal RVQ-VAE*

## 实验与分析

### 核心瓶颈与评估逻辑

MoTiGA 的实验设计围绕三个递进问题展开：(1) 因果运动量化与时间滞后预测能否弥合因果 LLM 与运动模态之间的表示鸿沟？(2) 多级混合加权偏好优化（MHPO）能否将细粒度人类偏好信号有效注入训练？(3) 各模块的贡献如何，是否存在边际收益递减或隐性代价？

评估采用 HumanML3D 和 KIT-ML 两个标准基准，所有实验重复 20 次并报告 95% 置信区间。指标覆盖生成质量（FID）、语义对齐（R-Precision Top-1/2/3）、运动多样性（Diversity）和条件一致性（MM-Dist）。特别注意：FID 越低越好，R-Precision 和 Diversity 越高越好，但 Diversity 需与真实数据分布（Real）接近而非无上限提升。

### 主实验结果

**Table 1** 展示了文本驱动运动生成的核心对比。在 HumanML3D 上，MoTiGA 以 **FID 0.041** 取得最优，相比 LLM-based 方法中表现最好的 MotionGPT（Llama, 0.232）提升 **82.3%**，相比任务专用方法中表现最好的 MoMask（0.045）亦有微弱优势。R-Precision Top-1 达到 **52.3**，仅次于 MoMask（52.9），但显著优于其他 LLM-based 方法（MotionGPT Llama 为 49.2）。在 KIT-ML 上，MoTiGA 的 FID 为 **0.180**，相比 MotionGPT（Llama, 0.510）提升 **64.7%**，R-Precision Top-1 为 **44.3**，仅次于 MotionLLM（45.1）和 MoMask（44.7）。

关键洞察：MoTiGA 是首个在 FID 上大幅超越任务专用方法的 LLM-based 方案。此前 LLM-based 方法（MotionGPT、MotionLLM）在 FID 上始终落后于 T2M-GPT 和 MoMask 等专用架构，其瓶颈正是非因果 VQ-VAE 的量化误差与因果不匹配。MoTiGA 通过 Causal RVQ-VAE + 时间滞后预测的组合，将 LLM-based 方法的 FID 从 0.2+ 压缩至 0.041，证明因果表示对齐是释放 LLM 运动生成潜力的关键杠杆。

**Table 2** 和 **Table 3** 分别验证了运动描述（motion captioning）和带初始姿态条件的生成任务。在描述任务上，MoTiGA 的 R-Precision Top-1 达到 55.9，BLEU@4 为 14.7，与 MotionGPT（Llama）持平或略优。在初始姿态条件生成上，MoTiGA 以 FID 0.040 显著优于 MotionGPT 的 0.493，说明因果量化表示同样有利于条件控制任务。

### 消融实验：因果链条的逐环验证

**Table 4** 是理解 MoTiGA 工作机制的核心证据，按因果逻辑链组织：

**第一环：Causal RVQ-VAE vs 标准 VQ-VAE。** 将标准 VQ-VAE 替换为 Causal RVQ-VAE，生成 FID 从 0.213 降至 0.186（↓12.7%），R-Precision Top-1 从 49.9 升至 51.3。这验证了多级因果量化对细粒度运动表示的增益——因果卷积在编码器中建立的时间依赖使得量化令牌序列更忠实地保留了运动动态，而非简单地将相邻帧独立量化。

**第二环：时间滞后因果预测 vs 时间同步并行 vs 逐步解码。** 这是论文最具原创性的消融对比。时间同步并行预测（即所有层级令牌在同一时间步并行生成）的 FID 为 0.064，R-Precision 为 51.0；时间滞后因果预测将 FID 进一步压缩至 **0.041**，R-Precision 升至 **52.3**。逐步解码（逐 token 自回归）的 FID 为 0.055，R-Precision 为 51.8。时间滞后策略的优势源于它严格维护了 Causal RVQ-VAE 建立的因果依赖——粗层级令牌（b¹）为未来时间步生成，细层级令牌（b⁴）为较早时间步生成，确保每个令牌预测时其因果父节点已就绪。时间同步并行因缺失当前时刻粗层令牌而破坏这一依赖，如 Eq. (1) 所揭示，导致条件概率分布偏离真实分布。

**第三环：MHPO 偏好对齐。** 在时间滞后预测基础上添加 MHPO，FID 从 0.041 进一步优化至 0.041（持平但方差更小），R-Precision 从 52.3 升至 52.3（持平），但 Diversity 从 9.418 调整至 9.503，更接近真实分布的 9.503。与标准 GRPO 的对比更具说服力：GRPO 仅使用全局二值奖励，而 MHPO 引入层级自适应语义奖励后，在 R-Precision 和 Diversity 上均优于 GRPO。这表明多级奖励塑造确实将更细粒度的人类偏好信号注入了训练，而非仅在全局层面做粗糙的二分类对齐。

**Table 5** 进一步消融量化层级数 V。V=4 时生成 FID 达到最优 0.055（注意此表可能使用不同配置，与 Table 4 的 0.041 存在差异，需手动核实实验设置），重建 FID 为 0.031。V=2 时生成 FID 为 0.078，V=8 时为 0.062。层级过少（V=2）导致量化粒度不足，层级过多（V=8）引入冗余并增加优化难度。值得注意的是，Causal RVQ-VAE 的重建 FID（0.031）略高于标准 RVQ-VAE（0.029），这是因果约束的代价——因果卷积限制了编码器对全局上下文的访问，在纯重建任务上存在轻微细节损失，但换来了生成任务上的显著增益。

**Table 6** 消融 MHPO 权重因子 α（文中记为 ω）。α=0.6 时 FID 达到最优 0.041，R-Precision 为 52.3。α=0（仅全局奖励）时 FID 为 0.045，α=1.0（仅层级奖励）时 FID 为 0.049。这表明全局二值奖励与层级语义奖励之间存在互补关系：全局奖励提供粗粒度的偏好方向，层级奖励提供令牌级的细粒度信号，两者以 0.6:0.4 的比例混合效果最佳。

### 失败模式与定性分析

**Figure 5** 提供了消融实验的定性可视化。未使用 Causal RVQ-VAE 的生成结果出现明显的语义错位（如“跳跃”动作被生成为“行走”），未使用 MHPO 的结果存在肢体穿透和节奏不自然等问题。这些失败模式与 **Figure 2(b)** 中展示的 HumanML3D-R 偏好数据集的典型错误类型一致：肢体穿透、语义缺失、节奏异常、物理不合理。

**Figure 2(a)** 的散点图直观展示了 MoTiGA 在 FID-R-Precision 权衡中的优势——它位于左下角（低 FID、高 R-Precision）的最优区域，而其他 LLM-based 方法集中在高 FID 区域。

### 局限性与开放问题

Causal RVQ-VAE 的重建 FID 略高于标准 RVQ-VAE，在纯重建场景下可能不是最优选择。HumanML3D-R 偏好数据集依赖人工标注且仅覆盖 HumanML3D 的动作分布，其主观偏差和领域局限性可能影响 MHPO 在更广泛场景下的泛化能力。MHPO 的语义相似度奖励依赖预训练 TMR 模型，若 TMR 存在领域偏差，将通过奖励信号传导至策略优化。目前仅在 HumanML3D 和 KIT-ML 上验证，在更大规模、更多样化的真实运动数据上的表现仍需进一步检验。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/005_Table_1.jpg]]
*Table 1: Text-driven motion generation results on HumanML3D [13] and KIT-ML [33]. The evaluation is repeated 20 times, and the mean is reported, along with a 95% confidence interval. ±0.000 means the variance is not measured. The best and second-best results are indicated in bold and underlined, respectively*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/008_Table_4.jpg]]
*Table 4: Ablation studies of MoTiGA on HumanML3D [13]*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/002_Figure_2.jpg]]
*Figure 2: Left: (a) Quantitative comparison with results of SoTA LLM-based methods [19, 45, 51], using FID → and R-Precision Top-1 ↑ metrics; Right: (b) Common data pairs of misaligned and non-preferred human motion generation*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/010_Figure_5.jpg]]
*Figure 5: Visualisation examples for ablation studies and qualitative comparison using retargeted characters [2]*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/007_Table_3.jpg]]
*Table 3: Experiments of text-driven motion generation with given initial pose on HumanML3D [13]*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/006_Table_2.jpg]]
*Table 2: Experiments of motion captioning task on the HumanML3D [13] benchmark*

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Multi_level_Causa/figures/009_Figure.jpg]]
*Figure: Ablation studies of human alignment, the text is “a person moves to his right then back”*

## 方法谱系与知识库定位

### 与现有LLM-based运动生成方法的对比与突破

当前基于大语言模型的文本到运动生成方法（如 **MotionGPT**、**MotionLLM**）普遍采用“VQ-VAE量化+LLM自回归解码”的范式，但这一技术路线存在两个根本性瓶颈。其一，标准VQ-VAE或简单残差VQ-VAE在运动量化时未考虑时序因果性，导致细粒度运动细节的量化误差在解码阶段被逐级放大。其二，因果语言模型（如Llama）天然依赖严格的时间因果假设，而运动令牌的并行预测策略往往违反这一假设，造成因果表示鸿沟（causal representation gap）。此外，现有方法普遍缺乏显式的人类偏好对齐机制，生成的运动在语义一致性和自然度上难以满足人类期望。

MoTiGA（CVPR 2026）针对上述瓶颈提出了三个核心改进槽位：

1. **运动量化器升级：从非因果VQ-VAE到Causal RVQ-VAE。** 标准VQ-VAE（单级或残差）在量化时未区分时序前后关系，而Causal RVQ-VAE通过因果卷积和迭代残差量化，将运动序列编码为V=4级因果令牌，其中基础级（$b^1$）捕捉全局运动模式，残差级（$b^2$至$b^4$）逐级补充细粒度细节，且各级令牌间维持严格的因果依赖。消融实验证实，仅将标准VQ-VAE替换为Causal RVQ-VAE，生成FID即从0.213提升至0.186（Table 4）。

2. **运动令牌预测策略升级：从逐步自回归解码到时间滞后因果并行预测。** 传统方法采用逐令牌串行解码，效率低下；而时间同步并行预测（time-synchronized parallel prediction）虽然加速了推理，却因缺失当前时刻粗层令牌而破坏了Causal RVQ-VAE建立的因果依赖（见Eq. (1)）。MoTiGA提出的时间滞后因果预测策略（Figure 4(c)）通过引入时序偏移——粗层令牌预测未来时刻、细层令牌预测当前或较早时刻——在维持严格因果性的同时实现了多级令牌的并行预测，最终在FID（0.041）和R-Precision Top-1（52.3）上均显著优于时间同步并行策略（0.064, 51.0）和逐步解码策略（Table 4）。

3. **偏好优化机制引入：从仅指令微调到多级混合加权偏好优化（MHPO）。** 现有LLM-based方法仅依赖标准指令微调，缺乏对人类偏好的显式建模。MoTiGA构建了HumanML3D-R偏好数据集，并设计了MHPO框架：在GRPO（Group Relative Policy Optimization）基础上，引入层级自适应语义相似度奖励（$\delta^v$），通过TMR模型计算文本与解码自前v级令牌的运动之间的语义相似度，为人类偏好样本的令牌级奖励注入层级增量（Eq. (3)），同时为非偏好样本施加由全层级语义相似度决定的惩罚项（Eq. (5)）。消融表明，添加MHPO后取得最优FID 0.041，且优于标准GRPO（Table 4），权重因子$\alpha=0.6$时效果最佳（Table 6）。

### 与任务特定方法的对比

除LLM-based方法外，MoTiGA还与任务特定方法进行了全面对比，包括 **T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., CVPR 2024）和 **Motion Diffuse**（Zhang et al., TPAMI 2024）。在HumanML3D和KIT-ML两个标准基准上，MoTiGA以FID 0.041（HumanML3D）和0.180（KIT-ML）超越了上述所有任务特定方法（Table 1），同时在R-Precision Top-1上达到52.3（HumanML3D）和44.3（KIT-ML），验证了LLM-based框架在引入因果表示与人类对齐后的竞争力。

在给定初始姿态的文本驱动生成任务中，MoTiGA将FID从MotionGPT的0.493降至0.040（Table 3），进一步证明了因果运动令牌表示在条件生成场景下的优势。

### 适用边界与局限

尽管MoTiGA在生成质量上取得了显著突破，其方法设计仍存在以下适用边界：

1. **重建-生成权衡。** Causal RVQ-VAE虽然在生成任务上表现更优，但重建FID略高于标准RVQ-VAE（Table 5），表明因果约束在纯重建场景下可能引入轻微的细节损失。当应用场景对重建精度要求高于生成多样性时，需谨慎选择量化器类型。

2. **偏好数据依赖。** HumanML3D-R偏好数据集依赖人工标注，可能存在主观偏差，且目前仅覆盖HumanML3D的动作分布。在迁移到其他运动风格或领域（如舞蹈、体育动作）时，偏好模型的对齐效果可能下降。

3. **语义相似度奖励的领域偏差。** MHPO中的自适应奖励增量依赖于预训练TMR模型。若TMR模型本身在特定运动类型或文本描述上存在领域偏差，可能将错误信号注入偏好优化过程，影响对齐效果。

4. **验证范围有限。** 目前仅在HumanML3D和KIT-ML两个标准数据集上验证，尚未在更多样化、更大规模或更复杂的真实场景（如多人交互、长时间序列）中测试，方法的泛化性有待进一步验证。

### 开放问题与后续方向

1. **时间滞后机制的泛化性。** 时间滞后因果预测的具体时序偏移如何确定？不同层级之间的最优时间滞后期数和冗余是否适应所有运动类型（如快速运动与慢速运动），仍需系统研究。

2. **偏好数据集的质量与覆盖。** HumanML3D-R数据集中偏好对的具体错误类别分布如何？不同错误类型（如语义偏离、物理不自然、节奏错误）对模型对齐效果的敏感度有何差异？构建更细粒度的偏好标注体系可能进一步提升对齐精度。

3. **跨模态推广。** 多级混合加权偏好优化是否可推广到其他序列生成任务（如语音合成、视频生成）？层级语义增量在其他模态中的定义方式需要如何调整，是一个值得探索的方向。

4. **模型规模扩展。** Causal RVQ-VAE是否可以在更大基础模型（如LLaMA-13B/30B）上获得进一步增益？计算效率与生成质量之间的平衡点在哪里，需要实验验证。

5. **人类对齐的评估体系。** 除FID和R-Precision外，是否有更适合评估人类对齐程度的自动化指标或用户研究方案？现有指标主要衡量分布匹配和检索精度，无法直接反映人类对运动自然度、语义准确性的主观判断，构建更全面的对齐评估基准是推动该方向发展的关键。

## 原文 PDF

![[paperPDFs/CVPR_2026/Multi_level_Causal_LLM_based_Text_to_Motion_Generation_with_Human_Alignment.pdf]]
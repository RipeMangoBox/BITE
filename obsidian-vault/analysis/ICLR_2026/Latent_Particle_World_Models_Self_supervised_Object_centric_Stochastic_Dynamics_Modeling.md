---
title: "Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Latent_Particle_World_Models_Self_supervised_Object_centric_Stochastic_Dynamics_Modeling.pdf
project_link: https://taldatech.github.io/lpwm-web
code_link: null
openreview_forum_id: lTaPtGiUUc
aliases:
- LPWML
- LPWMSSOCSDM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "CONTEXT模块引入的每粒子连续潜在动作，通过逆动力学与潜在策略的双头设计，实现了粒子级的随机动力学建模与多模态条件控制。"
primary_logic: "将视频分解为具有显式空间属性的潜在粒子集合，并为每个粒子分配独立的潜在动作，可以在无需跟踪的条件下学习对象间交互，从而在复杂真实场景中实现高效且可解释的随机世界模型。"
claims:
- "LPWM在多个随机动态数据集的FVD和LPIPS上超越所有对象中心基线（如PlaySlot）和patch基线（DVAE）。"
- "在BAIR-64视频预测上，紧凑的LPWM（89.4 FVD）与大型视频模型（如VideoGPT 103.3, FitVid 93.6）性能相当，体现了对象中心归纳偏置的优势。"
- "LPWM在OGBench-Scene的task1上达到100%成功率，在task3上89%，显著优于所有基线（如HIQL 80%, 61%）。"
- "消融实验证明每粒子潜在动作（vs全局）是关键设计选择，全局动作池化会严重降低重建质量。"
---

# Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling

> [!tip] 核心洞察
> 将视频分解为具有显式空间属性的潜在粒子集合，并为每个粒子分配独立的潜在动作，可以在无需跟踪的条件下学习对象间交互，从而在复杂真实场景中实现高效且可解释的随机世界模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 潜在粒子世界模型：自监督对象中心随机动力学建模 |
| 英文题名 | Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=lTaPtGiUUc) · [Project](https://taldatech.github.io/lpwm-web) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Latent Particle World Models (LPWM) |
| Dataset | Sketchy-U, LanguageTable-A, Bridge-L, PandaPush 1-Cube |

> [!tip] 效果简介
> - Sketchy-U 上，FVD↓ 为 163.91，对比 192.63 (DVAE)，变化 -28.72。
> - LanguageTable-A 上，FVD↓ 为 15.96，对比 26.78 (DVAE)，变化 -10.82。
> - Bridge-L 上，FVD↓ 为 47.78，对比 146.85 (DVAE)，变化 -99.07。

## 概要

当前视频世界模型普遍采用固定网格的Patch表示来编码视觉场景，缺乏对象中心的结构化分解能力。这种表示方式与文本领域以语义单元（词、子词）进行建模的范式形成鲜明对比——图像被机械地切分为均匀网格，难以高效捕捉多对象场景中的局部动态与随机交互，且计算开销随分辨率急剧增长。

**潜在粒子世界模型（Latent Particle World Models, LPWM）** 提出了一种自监督的对象中心随机动力学建模框架，核心思路是将视频分解为一组具有显式空间属性的潜在粒子集合，并为每个粒子分配独立的连续潜在动作。LPWM无需显式跟踪即可学习对象间交互，在保持紧凑表示的同时实现了高效且可解释的随机世界建模。

方法层面，LPWM建立在深度潜在粒子（DLP）表示与DDLP框架之上，引入四项关键改进：将表示模态从固定网格Patch转向解耦的潜在粒子属性（关键点、尺度、深度、透明度、特征）；将潜在动作从全局向量细化为每粒子连续潜在动作，并通过逆动力学与潜在策略双头设计实现随机控制；以隐式的粒子-网格机制替代显式跟踪；统一支持动作、语言、图像目标及多视角等多模态条件。

实验层面，LPWM在多个随机动态数据集上取得最优性能：在Sketchy-U上FVD达到163.91（DVAE为192.63），LanguageTable-A上FVD为15.96（DVAE为26.78），Bridge-L上FVD为47.78（DVAE为146.85）。在BAIR-64视频预测任务中，紧凑的LPWM（FVD 89.4）与大型视频模型VideoGPT（103.3）、FitVid（93.6）性能相当，验证了对象中心归纳偏置的样本效率优势。在决策任务上，LPWM在OGBench-Scene的task1达到100%成功率，task3达到89%，显著超越所有基线方法。

消融实验进一步确认：每粒子潜在动作是重建质量的关键（PSNR 28.55 vs 全局池化27.24）；AdaLN位置嵌入优于标准可加性嵌入；潜在动作维度在3到10之间性能稳定。当前局限在于粒子移动范围受限、确定性场景下提升有限，以及潜在策略的泛化能力有待改进。

### 视频世界模型的表示瓶颈

视频世界模型的核心目标是学习环境的紧凑动力学，从而支持未来帧预测与决策规划。当前主流方法大多将视频帧分割为固定网格的patch嵌入（patchify），再交由Transformer或扩散模型处理。这种表示方式在文本领域有自然对应——文本天然被分词为语义单元（词或子词），但图像patch并不显式编码语义内容（Figure 2）。由此带来的瓶颈是双重的：

1. **结构缺失**：固定网格表示缺乏对象中心的结构化分解，无法显式建模多对象场景中的实体边界、遮挡关系和局部交互。
2. **计算低效**：patch序列长度随分辨率平方增长，在长时程随机动态建模中计算开销巨大，且注意力机制难以聚焦于真正交互的实体。

### 对象中心方法的进展与局限

为缓解上述问题，对象中心表示应运而生。现有方法可大致分为三类（Table 1/Table 4）：

- **Slot-based方法**（如**PlaySlot**, Villar-Corrales & Behnke, 2025；**SlotFormer**, Wu et al., 2022b）：将场景分解为一组潜在槽位，每个槽位绑定一个对象，但槽位通常缺乏显式空间属性。
- **Patch-based对象中心方法**（如**G-SWM**, Lin et al., 2020a）：在patch表示上施加对象中心归纳偏置，但表示本身仍非显式对象化。
- **Particle-based方法**（如**DDLP**, Daniel & Tamar, 2024）：将对象建模为具有显式空间属性（位置、尺度、深度、透明度）的潜在粒子，具备更强的可解释性。

然而，现有对象中心方法存在三个关键缺口：

1. **跟踪依赖**：DDLP等粒子方法依赖显式的时序跟踪与滤波来维持粒子身份，限制了并行编码能力。
2. **随机性建模不足**：多数方法将动力学建模为确定性映射，无法捕捉真实场景中的多模态随机交互。
3. **条件灵活性有限**：现有方法通常仅支持单一条件信号（如动作或语言），缺乏统一的多模态条件框架。

### 本文动机

本文的核心洞察是：**将视频分解为具有显式空间属性的潜在粒子集合，并为每个粒子分配独立的潜在动作，可以在无需显式跟踪的条件下学习对象间交互，从而在复杂真实场景中实现高效且可解释的随机世界模型。**

基于此，LPWM在DDLP的深度潜在粒子（DLP）表示基础上，引入两个关键创新：
- **CONTEXT模块**：通过逆动力学与潜在策略的双头设计，为每个粒子推断连续的潜在动作，实现粒子级随机动力学建模。
- **隐式粒子-网格机制**：利用AdaLN位置嵌入替代显式跟踪，使粒子在局部区域内自由移动并通过特征转移机制保持身份连续性。

这种设计使LPWM能够同时支持动作、语言、图像目标及多视图等多种条件信号，并在随机动态场景中显著超越现有对象中心基线和patch基线。

## 核心方法与创新机理

LPWM的核心创新在于将**对象中心的潜在粒子表示**与**每粒子连续潜在动作**相结合，构建了一个无需显式跟踪的随机动力学世界模型。相比现有方法，LPWM在以下四个关键维度上实现了突破。

### 1. 从固定网格Patch到解耦潜在粒子

现有视频世界模型（如DVAE、G-SWM）普遍采用固定网格的patch嵌入，缺乏对象中心的结构化分解，难以高效建模多对象场景下的局部动态与交互。LPWM继承并扩展了DLP框架，将每帧图像编码为M个前景粒子与一个背景粒子，每个前景粒子由显式的空间属性向量定义：

$$z_{\mathrm{fg}} = [z_p, z_s, z_d, z_t, z_f] \in \mathbb{R}^{6 + d_{\mathrm{obj}}}$$

其中$z_p$为关键点位置、$z_s$为尺度、$z_d$为深度、$z_t$为透明度、$z_f$为视觉特征。这种解耦设计使模型能够自主发现关键点、边界框和对象掩码，无需任何监督信号。

### 2. 每粒子连续潜在动作：随机控制的因果旋钮

LPWM的CONTEXT模块是核心因果调控机制。与PlaySlot等使用全局离散潜在动作的方法不同，LPWM为**每个粒子**建模独立的连续潜在动作$z_c^{m,t}$，直接控制从$z^{m,t}$到$z^{m,t+1}$的状态转移。CONTEXT模块实现为因果时空Transformer，包含双头设计：

- **潜在逆动力学头**：基于当前与下一帧粒子状态推断潜在动作
- **潜在策略头**：仅基于历史粒子状态预测潜在动作，作为逆动力学的先验正则化

训练时通过KL散度将两者对齐，推理时可从潜在策略采样以实现随机生成。消融实验（Table 11）证实，每粒子潜在动作是决定性的设计选择：将潜在动作替换为全局均值池化会导致PSNR从28.55降至27.24。

### 3. 隐式粒子-网格机制：无需显式跟踪

DDLP等前代粒子模型依赖显式的时序跟踪与滤波来维持粒子身份一致性。LPWM通过**隐式粒子-网格机制**彻底消除了这一需求：每个粒子被约束在其初始patch中心周围的局部区域内移动，当粒子到达区域边界时，其特征通过AdaLN位置嵌入隐式传递给邻近粒子。这种设计使所有帧可并行编码，同时保持粒子身份在时间维度上的连续性。消融实验表明，AdaLN位置嵌入显著优于标准可加性嵌入（PSNR 28.55 vs 21.54）。

### 4. 统一多模态条件接口

LPWM的CONTEXT模块天然支持多种条件信号的统一注入，包括动作、语言（通过T5-large编码）、图像目标和多视图输入。这使得同一预训练模型可灵活适配视频预测、语言条件生成、目标条件模仿学习等多种下游任务，无需架构修改。

LPWM 将视频建模为一个端到端的时序变分自编码器，其核心架构由四个协同模块构成：**ENCODER**、**DECODER**、**CONTEXT** 和 **DYNAMICS**。整体流程遵循“编码—上下文推理—动力学预测—解码”的闭环。

给定过去 $T$ 帧观测 $I_{0:T-1}$ 和可选条件信号 $c$（如动作、语言或图像目标），LPWM 的目标是预测未来 $\tau$ 帧 $\hat{I}_{T:T+\tau-1}$。这一过程在潜在空间中进行，而非直接操作像素。

**编码阶段**：ENCODER $\mathcal{E}_{\phi}$ 将每一帧独立映射为一组解耦的潜在粒子集合。对于第 $t$ 帧，输出包含 $M$ 个前景粒子 $\{z_{\mathrm{fg}}^{m,t}\}_{m=0}^{M-1}$ 和一个背景粒子 $z_{\mathrm{bg}}^{t}$。每个前景粒子是一个具有显式空间属性的随机向量，包含关键点位置、尺度、深度、透明度和外观特征。背景粒子则从前景区域被遮蔽后的图像中编码得到，确保前景与背景的解耦。由于编码过程逐帧并行执行，LPWM 无需显式的粒子跟踪机制，这是相对于 DDLP 等前驱方法的关键简化。

**上下文推理阶段**：CONTEXT $\mathcal{K}_{\psi}$ 接收全部 $T+1$ 帧的粒子集合及条件信号，通过因果时空 Transformer 为每个粒子推断其独立的连续潜在动作 $z_{c}^{m,t}$。该模块采用双头设计：**逆动力学头**从相邻帧的粒子状态差异中提取潜在动作，而**潜在策略头**则仅基于历史信息预测潜在动作分布，二者通过 KL 散度相互正则化。这一设计使得 LPWM 能够建模粒子级的随机动力学，同时支持在推理时从潜在策略采样以实现多模态未来生成。

**动力学预测阶段**：DYNAMICS $\mathcal{F}_{\xi}$ 以当前时刻的粒子状态和 CONTEXT 输出的潜在动作为输入，通过另一个因果时空 Transformer 预测下一时刻的粒子分布参数。该模块采用 AdaLN 方式嵌入位置信息，而非标准可加性位置编码，消融实验表明这一选择对重建质量至关重要。

**解码阶段**：DECODER $\mathcal{D}_{\theta}$ 从预测的粒子集合中重建图像。它通过 RGBA 合成将前景粒子的 alpha 掩码与背景粒子融合，生成最终的像素级预测 $\hat{I}_t$。

**训练目标**：LPWM 通过最大化时序 ELBO 进行端到端训练，总损失分解为第一帧的静态 ELBO 和后续帧的动态 ELBO：

$$\mathcal{L}_{\mathrm{LPWM}} = -\sum_{t=0}^{T-1} ELBO(x_t = I_t) = \mathcal{L}_{\mathrm{static}} + \mathcal{L}_{\mathrm{dynamic}}$$

动态 ELBO 包含三项：重建损失、粒子动力学的 KL 散度（后验分布与动力学先验之间），以及上下文模块的 KL 散度（逆动力学与潜在策略之间）。KL 贡献通过粒子透明度属性进行掩码，仅可见粒子参与损失计算。

这一框架的关键瓶颈突破在于：通过将视频分解为具有显式空间属性的潜在粒子集合，并为每个粒子分配独立的潜在动作，LPWM 在无需跟踪的条件下实现了高效的对象中心随机动力学建模，且计算开销远低于基于固定网格 patch 的方法。

LPWM 由四个端到端联合训练的组件构成：编码器（ENCODER）、解码器（DECODER）、上下文模块（CONTEXT）和动力学模块（DYNAMICS）。整体训练目标为最大化时序证据下界（ELBO），损失函数分解为静态项与动态项：

$$
\mathcal{L}_{\mathrm{LPWM}} = -\sum_{t=0}^{T-1} ELBO(x_t = I_t) = \mathcal{L}_{\mathrm{static}} + \mathcal{L}_{\mathrm{dynamic}}
$$

其中 $\mathcal{L}_{\mathrm{static}}$ 仅作用于首帧的静态 VAE 重建，$\mathcal{L}_{\mathrm{dynamic}}$ 则覆盖后续帧的时序预测。动态 ELBO 的完整形式为：

$$
\mathcal{L}_{\mathrm{dynamic}} = \sum_{t=1}^{T-1} \Big[ \mathcal{L}_{\mathrm{rec}}(x_t, \hat{x}_t) + \beta_{\mathrm{dyn}} KL(q_{\phi}(z^t | x_t) \| p_{\xi}(z^t | z^{<t}, z_c^{<t})) + \beta_{\mathrm{ctx}} KL(p_{\psi}^{\mathrm{inv}}(z_c^t | z^{\le t+1}) \| p_{\psi}^{\mathrm{policy}}(z_c^t | z^{\le t})) \Big]
$$

该损失包含三项核心机制：重建损失约束解码图像与真实帧的一致；动力学 KL 散度迫使预测的粒子先验分布逼近后验分布；上下文 KL 散度则让潜在策略（仅依赖历史信息）正则化逆动力学（可窥见未来一帧），从而在随机生成时提供合理的先验。KL 贡献通过粒子透明度属性进行掩码，仅可见粒子参与计算。

**ENCODER $\mathcal{E}_{\phi}$** 将每帧图像映射为一组潜在粒子：

$$
\mathcal{E}_{\phi}(x = I_t) = [\{z_{\mathrm{fg}}^{m,t}\}_{m=0}^{M-1}, z_{\mathrm{bg}}^{t}]
$$

每个前景粒子 $z_{\mathrm{fg}} = [z_p, z_s, z_d, z_t, z_f] \in \mathbb{R}^{6 + d_{\mathrm{obj}}}$ 是解耦的随机属性向量，分别编码关键点位置、尺度、深度、透明度和视觉特征。背景粒子则从被前景掩码遮挡后的图像中编码得到。

**DECODER $\mathcal{D}_{\theta}$** 通过 RGBA 合成将选定的前景粒子与背景粒子重建为图像：

$$
\mathcal{D}_{\theta}([\{z_{\mathrm{fg}}^{l,t}\}_{l=0}^{L-1}, z_{\mathrm{bg}}^{t}]) = \hat{I}_t
$$

每个粒子被解码为局部外观块，由其空间属性定位与缩放，透明度和深度属性处理可见性与遮挡关系。

**CONTEXT $\mathcal{K}_{\psi}$** 是 LPWM 的核心创新——一个因果时空 Transformer，为每个粒子推断连续的潜在动作：

$$
\mathcal{K}_{\psi}( \{ [ \{ z_{\mathrm{fg}}^{m, t} \}_{m=0}^{M-1}, z_{\mathrm{bg}}^{t}, c_t ] \}_{t=0}^{T} ) = \{ [ \{ z_{c, \mathrm{fg}}^{m, t} \}_{m=0}^{M-1}, z_{c, \mathrm{bg}}^{t} ] \}_{t=0}^{T-1}
$$

该模块包含双头设计：(1) 潜在逆动力学头，以当前和未来粒子状态为条件推断潜在动作；(2) 潜在策略头，仅以历史粒子状态为条件生成潜在动作先验。两者通过 KL 散度耦合，使模型在开环生成时能采样合理的潜在动作。潜在动作维度设为 $d_{\mathrm{ctx}} = 7$，消融实验表明该值在 3 到 10 之间性能稳定，过小（1）或过大（14）会导致 FVD 显著恶化。

**DYNAMICS $\mathcal{F}_{\xi}$** 同样采用因果时空 Transformer，以当前粒子和潜在动作为输入，通过 AdaLN 注入位置嵌入，预测下一时刻的粒子分布参数：

$$
\mathcal{F}_{\xi}( \{ [ \{ z_{\mathrm{fg}}^{m, t} \}_{m=0}^{M-1}, z_{\mathrm{bg}}^{t}, z_c^{t} ] \}_{t=0}^{T-1} ) = \{ [ \{ \hat{z}_{\mathrm{fg}}^{m, t} \}_{m=0}^{M-1}, \hat{z}_{\mathrm{bg}}^{t} ] \}_{t=1}^{T}
$$

动力学模块采用粒子-网格机制（particle-grid regime）：每个粒子仅在其初始块中心周围的局部区域内移动，当到达区域边界时，其特征被转移至邻近粒子，从而在无需显式跟踪的条件下隐式维护粒子身份。消融实验证实，AdaLN 位置嵌入显著优于标准可加性嵌入（PSNR 28.55 vs 21.54），是模型性能的关键设计选择。

## 实验与关键发现

### 核心性能：随机动态视频预测

LPWM在多个随机动态数据集上一致超越对象中心和patch基线。Table 2汇总了无监督潜在动作条件（U）、真实动作条件（A）和语言条件（L）下的定量结果。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lTaPtGiUUc/figures/005_Table_2.jpg]]
*Table 2: scale alone achieves. Extended results are in Appendix A.10 and videos are available: https: //taldatech.github.io/lpwm-web. Table 2: Quantitative results on latent-action-conditioned (U), action-conditioned (A), and languageconditioned (L) video prediction. FVD is reported for stochastic generation by sampling from the latent policy. t is the training horizon, c is the conditional frames at inference, and p is the predicted frames at inference*

在无监督潜在动作条件下，LPWM在Sketchy-U上取得FVD 163.91，相比DVAE（192.63）降低28.72，同时PSNR达28.41、LPIPS仅0.062。在BAIR-U上，LPWM的FVD为163.91，PSNR 25.66，SSIM 0.89。在Mario-U上，FVD 195.95，PSNR 27.50。这些结果验证了对象中心粒子表示在建模多对象随机交互时的效率优势——LPWM无需显式跟踪即可隐式学习对象间动态。

在动作条件场景下，LPWM在LanguageTable-A上取得FVD 15.96，远超DVAE的26.78（降低10.82）。语言条件生成任务中，LPWM在Bridge-L上FVD仅47.78，而DVAE高达146.85（降低99.07），表明CONTEXT模块的语言条件融合机制有效利用了T5-large编码的语义信息。

### 与大规模视频模型的对比

在BAIR-64视频预测基准上，紧凑的LPWM模型（FVD 89.4）与参数规模更大的通用视频模型性能相当：VideoGPT为103.3，FitVid为93.6。这一结果直接证明了对象中心归纳偏置的价值——通过将场景分解为少量结构化粒子，LPWM以更低的计算开销实现了与密集patch表示模型可比的预测质量。粒子表示的低维度特性使得动力学建模更加高效。

### 决策任务迁移

LPWM作为世界模型在机器人操作任务中展现出强迁移能力。在PandaPush 1-Cube任务上，LPWM达到92.7%成功率，与EC Diffuser（94.8%）接近。值得注意的是，基线方法为每个任务单独训练策略，而LPWM使用单一模型跨任务训练，这一设置对基线更有利，因此LPWM的实际泛化能力可能被低估。

在OGBench-Scene基准上，LPWM的优势更加显著：task1成功率达100±0%，显著超越GCIVL（84±4%）和HIQL（80±6%）；task3达89±9%，超越HIQL（61±11%）。Table 13的完整结果显示，LPWM在所有OGBench任务上均优于或持平最强基线。Figure 4的可视化进一步表明，LPWM生成的想象轨迹与实际环境执行高度一致，验证了潜在粒子世界模型在目标条件模仿学习中的实用性。

### 消融分析

**每粒子潜在动作 vs 全局动作**：Table 11的消融显示，每粒子潜在动作对重建质量至关重要（PSNR 28.55 vs 全局均值池化27.24），但生成多样性有所损失（FVD 120.32 vs 100.75）。这一trade-off表明：局部潜在动作提供了更精确的粒子级控制，有利于重建保真度；而全局信息聚合有助于捕获场景级随机性，提升生成多样性。该结果确认了每粒子设计是LPWM的核心因果旋钮。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lTaPtGiUUc/figures/024_Table_11.jpg]]
*Table 11: robustness to latent action dimension as long as it approximates the effective particle dimension ( < 6 + $d _ { \mathrm { o b j } }$ , i.e., 10 for Sketchy), balancing compression and information retention; our choice of $d _ { \mathrm { c t x } }$ = 7 reflects this trade-off5. Finally, adaptive layer normalization (AdaLN) for embedding timestep and particle identity outperforms standard additive positional embeddings, as previously observed (Zhu et al., 2024), albeit with an increased parameter count. Table 11: Ablation results: impact of latent action dimensions and type, and positional embeddings on LPWM performance. Results are reported on the Sketchy dataset after 10 epochs of training. R...

**潜在动作维度**：维度 $d_{\text{ctx}}$ 在3到10范围内性能稳定，过小（$d_{\text{ctx}}=1$，FVD 177.64）或过大（$d_{\text{ctx}}=14$，FVD 121.02）均导致性能下降。论文选择 $d_{\text{ctx}}=7$，接近有效粒子维度 $6+d_{\text{obj}}$（Sketchy上约为10），在压缩与信息保留间取得平衡。

**位置嵌入方式**：AdaLN位置嵌入显著优于标准可加性嵌入（PSNR 28.55 vs 21.54）。AdaLN通过条件归一化将位置信息注入Transformer层，而非简单加到token上，使得模型能更有效地利用粒子空间位置进行动力学预测。

### 局限性

尽管LPWM在随机动态场景中表现优异，在确定性动力学数据集上相对基线的提升有限——此时随机建模能力未被充分利用。此外，粒子仅在初始Patch周围局部移动，当物体需要大范围位移时，特征转移机制可能引入累积误差。潜在策略采样生成的多样性在映射到实际执行动作时出现性能下降，映射网络更偏好逆动力学输出而非策略采样，表明潜在策略的泛化能力尚需改进。LPWM仍需手动指定每帧粒子数量 $M$ 和训练超参数，对动态变化场景的适应性有待验证。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lTaPtGiUUc/figures/003_Table_1.jpg]]
*Table 1: summarizes key differences between self-supervised object-centric video prediction and world modeling methods. Table 1: Comparison of object-centric video prediction and world modeling methods across key dimensions and representation types. Please refer to Table 4 for an extended comparison*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lTaPtGiUUc/figures/016_Table_4.jpg]]
*Table 4: Comparison of video prediction and world modeling approaches across key dimensions. Models are grouped by representation category: holistic, Table 4: patch/object-centric, slot/object-centric, and particle/object-centric. AR: autoregressive; GNN: graph neural network. “Image-Goal Cond.” is e-goal conditioning sup*


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lTaPtGiUUc/figures/019_Table_7.jpg]]
*Table 7: DLPv3, DLPv2, and DLP image reconstruction performance comparison in the singleimage setting, evaluated on the test set*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lTaPtGiUUc/figures/020_Table_8.jpg]]
*Table 8: Quantitative results on video prediction for datasets with deterministic dynamics. t is the training horizon, c is the conditional frames at inference and p is the predicted frames at inference*

## 定位与知识库关联

### 1. 核心瓶颈与设计动机

现有视频世界模型普遍采用固定网格的patch表示（如ViT风格的patchify），这种表示缺乏对象中心的结构化分解，导致三个关键瓶颈：**（1）** 难以高效建模多对象场景下的随机交互与局部动态，因为patch网格无法显式区分不同对象的运动模式；**（2）** 计算开销巨大，patch序列的全注意力机制随帧数和分辨率平方增长；**（3）** 与自然语言tokenization存在“表示鸿沟”——文本被分解为语义有意义的词或子词，而图像却被机械地切割为无语义内容的固定网格（见Figure 2）。

LPWM的核心洞察在于：将视频分解为具有显式空间属性的潜在粒子集合，并为每个粒子分配独立的潜在动作，可以在无需显式跟踪的条件下学习对象间交互，从而在复杂真实场景中实现高效且可解释的随机世界模型。这一设计直接回应了上述瓶颈——粒子表示天然提供对象中心的结构化分解，而每粒子潜在动作则实现了粒子级的随机动力学建模与多模态条件控制。

### 2. 方法谱系与关键差异

LPWM建立在**DLP**（Daniel & Tamar, 2024）的对象中心潜在表示框架之上，但对其动力学建模部分进行了根本性重构。DLP将每帧图像编码为M个前景潜在粒子与一个背景粒子，每个前景粒子由解耦的随机属性向量定义：位置 $z_p$、尺度 $z_s$、深度 $z_d$、透明度 $z_t$ 和视觉特征 $z_f$，并通过alpha通道实现像素级前后景分解。然而，DLP依赖显式的时序跟踪与滤波来维持粒子身份，这限制了其扩展到复杂场景的能力。

LPWM与主要对象中心基线方法的关键差异体现在以下维度（完整对比见Table 1和Table 4）：

**（1）表示模态**：与基于slot的**PlaySlot**（Villar-Corrales & Behnke, 2025）和基于patch的**G-SWM**（Lin et al., 2020a）不同，LPWM采用解耦的潜在粒子属性（关键点、尺度、深度、透明度、特征），每个属性具有明确的物理语义，可直接解码为边界框和对象掩码。

**（2）潜在动作粒度**：**PlaySlot**和**CADDY**使用全局潜在动作向量，而LPWM引入连续每粒子潜在动作，通过逆动力学（inverse dynamics）与潜在策略（latent policy）双头设计实现粒子级随机动力学建模。消融实验表明，每粒子潜在动作对重建PSNR至关重要（28.55 vs 全局均值池化27.24），尽管生成多样性（FVD）受益于全局信息（120.32 vs 100.75），这揭示了重建精度与生成多样性之间的权衡。

**（3）粒子跟踪机制**：**DDLP**（Daniel & Tamar, 2024）依赖显式时序跟踪与滤波，而LPWM采用隐式粒子网格机制（particle-grid regime）——每个粒子仅在初始patch周围的局部区域内移动，当到达区域边界时通过特征转移机制将信息传递给邻近粒子，结合AdaLN位置嵌入，完全消除了显式跟踪的需求。消融实验证实AdaLN位置嵌入显著优于标准可加性嵌入（PSNR 28.55 vs 21.54）。

**（4）条件灵活性**：**DDLP**不提供条件接口，**PlaySlot**仅支持潜在动作条件，而LPWM通过CONTEXT模块实现统一条件框架，支持动作、语言（T5-large）、图像目标和多视角输入。这一设计使LPWM能够无缝适配视频预测、语言条件生成和目标条件模仿学习等多种下游任务。

### 3. 与大型视频生成模型的关系

LPWM的定位并非取代大型视频生成模型，而是提供一种**对象中心归纳偏置**的替代路径。在BAIR-64视频预测基准上，紧凑的LPWM（89.4 FVD）与**VideoGPT**（103.3 FVD）和**FitVid**（93.6 FVD）等大型模型性能相当（Table 9），但LPWM的参数规模和计算开销远小于后者。这表明对象中心的粒子表示能够以更紧凑的模型容量捕获多对象场景的结构化动态，其效率优势在需要长期rollout或实时推理的场景中尤为突出。

### 4. 适用边界与局限

**（1）大范围移动场景**：粒子网格机制将每个粒子约束在初始patch周围的局部区域内。当物体需要大范围连续移动时，特征转移机制可能引入误差，导致长期预测质量下降。这一局限在需要跨区域跟踪的长时间序列中尤为明显。

**（2）确定性场景收益有限**：LPWM的核心优势在于随机动力学建模。在确定性动力学数据集上，LPWM相对基线的提升有限，因为此时潜在策略的随机采样能力未被充分利用，逆动力学输出的确定性映射已足够。

**（3）潜在策略的泛化瓶颈**：在实际执行动作映射时，策略映射网络更偏好逆动力学输出而非潜在策略采样，表明潜在策略的生成多样性与真实数据分布之间存在不匹配。这限制了LPWM在需要多样化行为生成的开放环境中的应用。

**（4）手动超参数依赖**：LPWM仍需手动指定每帧的粒子数量M和训练超参数（如潜在动作维度 $d_{ctx}=7$），对动态变化场景（如物体数量变化）的适应性有待验证。消融实验表明 $d_{ctx}$ 在3到10之间性能稳定，但过小（1）或过大（14）导致FVD显著变差（177.64和121.02 vs 120.32）。

### 5. 开放问题

**（1）大规模扩展的稳定性**：如何将LPWM扩展到通用大规模视频数据，并保持对象中心表示的稳定性？当前实验集中在特定领域数据集（机器人操作、游戏场景），粒子分解在开放域视频上的鲁棒性尚未验证。

**（2）统一多模态条件**：当前LPWM支持单一条件类型（动作、语言或图像目标），能否实现同时使用动作、语言和图像目标的统一多模态条件？这需要CONTEXT模块处理异构条件信号的融合。

**（3）与强化学习的集成**：LPWM作为世界模型，天然适合与显式奖励建模结合用于基于模型的强化学习。如何在潜在粒子空间中定义奖励函数，以及如何利用粒子分解实现更高效的探索，是重要的研究方向。

**（4）策略映射的分布匹配**：为什么策略映射网络在逆动力学输出上性能更好？是否由于潜在策略与真实数据分布不匹配？这可能需要改进潜在策略的训练目标，例如引入对抗训练或分布匹配正则化。

**（5）动态粒子数量**：当前LPWM固定每帧粒子数量M，对于物体进出场景的动态变化缺乏适应性。如何实现自适应粒子分配，使模型能够根据场景复杂度动态调整表示容量，是一个具有挑战性的开放问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Latent_Particle_World_Models_Self_supervised_Object_centric_Stochastic_Dynamics_Modeling.pdf]]

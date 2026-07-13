---
title: Exploring Motion-Language Alignment for Text-driven Motion Generation
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Exploring_Motion-Language_Alignment_for_Text-driven_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- MG
- EMLATDMG
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入可学习的记忆槽位（Memory Slots）提供全局运动先验，同时通过局部交叉注意力建立运动帧与文本token的细粒度对齐；进一步通过SinkRatio量化注意力集中程度，并据此设计sink-mask（抑制起始token）和sink-ctrl（自适应调节分类器自由引导强度）来缓解注意力沉没，从而系统性地提升运动-语言对齐与生成质量。
primary_logic: 在文本驱动动作生成的跨模态注意力中，注意力权重会不成比例地集中在起始token（注意力沉没），限制了模型对语义token的利用。通过定义SinkRatio量化该集中程度，并利用sink-mask和sink-ctrl动态调节注意力分布与引导信号，可以促使模型关注更广泛的语义token，显著改善运动细节与文本语义的对齐。
claims:
- 消融实验表明，记忆槽位和局部对齐模块的组合使FID从0.120（无两者）降至0.076（完整），R-Precision进一步提升，验证了两者的协同作用。
- sink-mask机制使SinkRatio从0.9-1.0降至0.6-0.4，表明注意力分布明显更均衡；同时强掩码阈值(t_thresh=0.2)将FID从0.099降至0.056。
- 在HumanML3D数据集上，MLA-Gen-B的FID达到0.040，远超ACMDM-B的0.083，且R-Precision、CLIP-score等指标均为最优。
- 可视化显示，未掩码模型的注意力几乎全集中在<start token>，而掩码模型保留了<re>、<arranging>等有语义token的较高注意力。
---

# Exploring Motion-Language Alignment for Text-driven Motion Generation

> [!tip] 核心洞察
> 在文本驱动动作生成的跨模态注意力中，注意力权重会不成比例地集中在起始token（注意力沉没），限制了模型对语义token的利用。通过定义SinkRatio量化该集中程度，并利用sink-mask和sink-ctrl动态调节注意力分布与引导信号，可以促使模型关注更广泛的语义token，显著改善运动细节与文本语义的对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向文本驱动动作生成的运动-语言对齐探索 |
| 英文题名 | Exploring Motion-Language Alignment for Text-driven Motion Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.02973) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | MLA-Gen |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.040 (MLA-Gen-B) vs 0.083 (ACMDM-B) (-0.043)；R-Precision Top-1↑ 0.527 (MLA-Gen-B) vs 0.522 (ACMDM-B) (+0.005)；Matching Score↓ 3.108 (MLA-Gen-B) vs 3.178 (ACMDM-B) (-0.070)。

## 概要

文本驱动动作生成任务的目标是根据自然语言描述生成与之语义一致的人体动作序列。现有方法（如基于CLIP特征的扩散或流模型）普遍依赖全局文本表示进行条件控制，能够捕捉整体运动模式，但存在一个关键瓶颈：**缺乏帧级运动与文本token之间的细粒度时序对齐**，导致生成的动作虽然整体语义正确，却频繁遗漏关键细节（如图1所示，人物“整理”物品时手部动作模糊或缺失）。更隐蔽的问题是，在跨模态注意力计算中，注意力权重不成比例地集中在无信息量的起始token上——这一现象被本文定义为**注意力沉没（Attention Sink）**，进一步加剧了语义利用不充分的问题。

针对上述瓶颈，本文提出 **MLA-Gen**（Motion-Language Alignment Generation）框架，核心思路是通过三个互补机制系统性地提升运动-语言对齐质量：

1. **可学习记忆槽位（Memory Slots）**：引入一组共享的运动原型向量，通过交叉注意力向隐藏特征注入全局运动先验，弥补纯文本条件的不足。
2. **局部运动-语言对齐（Motion-Language Alignment）**：在帧级运动特征与文本token之间建立细粒度交叉注意力，生成局部语义条件并与全局条件融合，使每个运动帧能够直接关注相关词汇。
3. **SinkRatio驱动的注意力沉没缓解**：定义SinkRatio指标量化注意力在起始token上的集中程度，并据此设计 **sink-mask**（在特定时间步后屏蔽起始token的注意力）和 **sink-ctrl**（基于SinkRatio自适应调节分类器自由引导强度），促使模型关注更广泛的语义token。

在HumanML3D基准上的实验表明，MLA-Gen-B的FID达到 **0.040**，显著优于基线ACMDM-B的0.083，同时在R-Precision、Matching Score和CLIP-score等指标上均取得最优或次优结果。消融实验进一步验证：记忆槽位与局部对齐模块的组合使FID从0.120降至0.076；sink-mask机制将SinkRatio从0.9-1.0降至0.4-0.6，强掩码配置（$t_{\text{thresh}}=0.2$）将FID从0.099降至0.056，证实了注意力分布均衡化对生成质量的关键作用。



文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型和流匹配等生成范式在该任务上取得了显著进展，代表性工作包括 **MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2024）、**ReMoDiffuse**（Zhang et al., 2023）以及 **MLD++** 等。这些方法通常将文本条件以全局特征的形式注入生成过程，能够捕捉动作的整体语义，生成与描述大致相符的运动序列。

然而，现有方法存在一个关键瓶颈：**缺乏帧级运动与文本token之间的细粒度时序对齐**。全局文本表示（如CLIP特征）虽然能提供高层语义引导，但无法精确指定“何时发生何种动作”，导致生成的动作虽然整体语义正确，却频繁遗漏关键细节——例如“先迈左脚再转身”中的时序顺序或“缓慢抬手”中的速度修饰。如图1所示，先前框架在捕捉全局运动模式的同时，往往忽略了细粒度的运动细节，这正是本文致力于解决的核心问题。

进一步分析发现，在运动-语言跨模态注意力中存在一个被忽视的现象——**注意力沉没（Attention Sink）**：注意力权重不成比例地集中在无信息量的起始token（如`<start>`）上，严重限制了模型对语义token的有效利用。这一现象使得即使引入了细粒度对齐机制，其实际效果也会大打折扣，因为模型并未真正“关注”到有意义的文本内容。

针对上述问题，本文提出 **MLA-Gen**，一个系统性地探索运动-语言对齐的文本驱动动作生成框架。MLA-Gen的核心动机是：**通过引入全局运动先验与局部细粒度条件，并显式建模和缓解注意力沉没问题，从根本上提升运动生成中文本语义的利用效率与对齐精度**。具体而言，MLA-Gen通过可学习的记忆槽位（Memory Slots）提供全局运动原型，利用局部交叉注意力建立帧级运动与文本token的对齐，并基于提出的SinkRatio指标设计sink-mask和sink-ctrl机制来抑制注意力沉没，从而在多个层面协同提升生成质量。



## 核心方法与创新机理

MLA-Gen 的核心创新在于系统性地解决了文本驱动动作生成中“粗粒度语义利用”与“跨模态注意力失效”两个相互耦合的问题。与仅依赖全局文本特征（如CLIP特征）的基线方法（如 **ACMDM** (Meng et al., 2025)、**MDM** (Tevet et al., 2022)）不同，MLA-Gen 引入了三个紧密协作的机制，构成了从全局先验注入、局部细粒度对齐到注意力动态调控的完整创新链路。

### 1. 全局运动先验：可学习记忆槽位

现有方法缺乏对跨序列共享运动模式的显式建模。MLA-Gen 引入一组可学习的记忆槽位模块 $M \in \mathbb{R}^{S \times D_{flow}}$，通过交叉注意力 $\hat{h} = h + \mathrm{Attn}(Q=h, K=M, V=M)$ 向每层 Transformer 的隐藏特征注入全局运动原型。这些槽位在训练中自动学习到具有语义结构的运动模式——如 Figure 3 的热力图所示，不同运动帧与不同记忆槽位之间形成了差异化的高激活模式，表明槽位捕获了可解释的运动先验。消融实验证实，仅添加记忆槽位即可将 FID 从 0.120 降至 0.110（Table 3），验证了全局先验对生成质量的独立贡献。

### 2. 细粒度对齐：局部运动-语言交叉注意力

全局条件 $C_g$ 无法提供帧级的语义约束，导致生成动作遗漏细节（如手指动作、局部节奏变化）。MLA-Gen 构建了帧级运动特征 $z$ 与文本 token $T$ 之间的局部交叉注意力：

$$C_l = \mathrm{Attn}(Q=z, K=W_{\mathrm{up}} T, V=W_{\mathrm{up}} T)$$

并通过加权融合 $C = C_g + \lambda \cdot W_{\mathrm{down}} C_l$ 将局部条件注入主干网络。Figure 4 的热力图展示了运动帧与文本 token（如“re”“arranging”）之间的细粒度对应关系。单独添加该模块使 FID 从 0.120 降至 0.101，而记忆槽位与局部对齐的组合进一步将 FID 推至 0.076（Table 3），证明全局先验与细粒度对齐具有显著的互补增益。

### 3. 注意力沉没缓解：SinkRatio 度量与双重干预

这是 MLA-Gen 最具洞察力的创新。作者发现跨模态注意力中存在严重的“注意力沉没”（Attention Sink）现象——注意力权重不成比例地集中在无信息的 `<start token>` 上，导致语义 token 几乎无法被利用。为量化这一现象，MLA-Gen 定义了 SinkRatio 度量：

$$\mathrm{SinkRatio} = \frac{1}{L} \sum_{i=1}^{L} s_i, \quad s_i = \sum_{k \in \mathrm{Top}-K(A_i)} A_{i,k}$$

该度量统计了 top-K 注意力权重的集中程度。基于此，MLA-Gen 设计了双重干预机制：

- **sink-mask**：在采样时间步 $t > t_{\mathrm{thresh}}$ 时，强制将 `<start token>` 的注意力置零：
  
  $$\hat{A}_{i,j_0} = \begin{cases} 0, & \text{if } t > t_{\mathrm{thresh}} \\ A_{i,j_0}, & \text{otherwise} \end{cases}$$

- **sink-ctrl**：基于 SinkRatio 自适应调节分类器自由引导（CFG）的强度，通过 $k_{\mathrm{eff}} = k_{\mathrm{base}} (1 + \alpha \cdot \mathrm{SinkRatio})$ 动态修正引导信号。

Figure 5 的可视化提供了直接证据：未掩码模型的注意力几乎全部集中在 `<start token>`，而掩码模型保留了 `<re>`、`<arranging>` 等语义 token 的较高注意力。Figure 6 的 SinkRatio 曲线进一步量化了这一变化——未掩码模型的 SinkRatio 维持在 0.9-1.0，而掩码模型降至 0.6-0.4。消融实验中，强掩码（$t_{\mathrm{thresh}}=0.2$）将 FID 从 0.099 降至 0.056，sink-ctrl 进一步将 FID 从 0.117（固定策略）降至 0.044（Table 3），验证了动态调控的有效性。

### 创新点之间的协同关系

三个创新点形成了因果闭环：记忆槽位提供全局运动骨架，局部对齐注入帧级语义细节，而 SinkRatio 机制确保这些语义信息在注意力计算中被有效利用而非被沉没效应淹没。这种“注入-对齐-保障”的三层架构使得 MLA-Gen 在 HumanML3D 数据集上实现了 FID 0.040（MLA-Gen-B），远超 ACMDM-B 的 0.083（Table 1），同时 R-Precision、CLIP-score 等语义指标也达到最优。



MLA-Gen 的整体 pipeline 围绕一个核心矛盾展开：现有文本驱动动作生成方法依赖全局文本表示（如 CLIP 特征），虽能捕获整体语义，却因缺乏帧级运动与文本 token 之间的细粒度时序对齐而遗漏关键细节。更隐蔽的问题是，跨模态注意力中出现的“注意力沉没”（Attention Sink）现象使注意力过度集中在无信息的起始 token 上，进一步加剧了语义利用不充分。

针对这一瓶颈，MLA-Gen 在条件流匹配（Conditional Flow Matching）框架之上，引入了三个互补模块，形成“全局先验注入 → 局部细粒度对齐 → 注意力沉没缓解”的级联式 pipeline。

### 输入与潜在空间编码

pipeline 的输入端为文本描述 $y$ 和从高斯噪声采样的初始潜在状态 $X_0 \sim p_0$。运动自编码器（固定权重）预先将原始运动序列压缩到低维潜在空间，生成过程在该空间内进行，生成完成后再由解码器复原为运动序列。这一设计使主干网络只需建模潜在空间的条件分布 $p(X|y)$，降低了计算开销。

### 主干生成模型：条件流匹配速度网络

主干模型 $v_\theta$ 是一个 Transformer 架构的速度预测网络，接受三个输入：当前时间步 $t$、噪声状态 $X_t$ 以及文本条件。训练遵循 Rectified Flow 范式，采用线性插值路径：

$$X_t = (1-t) X_0 + t X_1, \quad t \in [0,1]$$

模型通过最小化预测速度与目标恒定速度 $(X_1 - X_0)$ 的 L2 距离来学习条件流映射：

$$\mathcal{L}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(0,1), X_0 \sim p_0, X_1 \sim q} \left[ \| v_\theta(X_t, t, y) - (X_1 - X_0) \|_2^2 \right]$$

推理时，从 $X_0$ 出发，通过 ODE 求解器沿学习到的速度场积分即可生成运动样本。

### 三模块级联架构

在主干网络的每层 Transformer 中，MLA-Gen 依次插入以下三个模块：

**记忆槽位注意力模块** 向隐藏特征注入全局运动先验。一组可学习的记忆槽位 $M \in \mathbb{R}^{S \times D_\text{flow}}$ 作为共享运动原型，通过交叉注意力与隐藏特征交互：

$$\hat{h} = h + \mathrm{Attn}(Q=h, K=M, V=M)$$

该模块使模型在生成早期就能从槽位中检索全局运动模式，为后续细粒度对齐提供结构骨架。Figure 3 的热力图显示，不同帧会激活不同的记忆槽位，验证了槽位确实编码了多样化的运动原型。

**局部运动-语言对齐模块** 建立帧级运动特征与文本 token 的细粒度对应。具体而言，以运动帧特征 $z$ 为 Query，文本 token 经上投影 $W_\text{up} T$ 后作为 Key 和 Value，计算交叉注意力：

$$C_l = \mathrm{Attn}(Q=z, K=W_{\text{up}} T, V=W_{\text{up}} T)$$

得到的局部条件 $C_l$ 与全局文本条件 $C_g$ 通过加权融合注入主干：

$$C = C_g + \lambda \cdot W_{\text{down}} C_l$$

Figure 4 的对齐热力图直观展示了运动帧与语义 token（如动作动词、物体名词）之间的帧级对应关系。

**SinkRatio 机制与注意力沉没缓解** 是 MLA-Gen 的关键创新。研究发现，标准交叉注意力中，注意力权重会不成比例地集中在起始 token（如 `<start>`）上，形成“注意力沉没”，严重限制了模型对语义 token 的利用。为量化这一现象，定义 SinkRatio 为所有帧的 top-K 注意力权重和的均值：

$$\mathrm{SinkRatio} = \frac{1}{L} \sum_{i=1}^{L} s_i, \quad s_i = \sum_{k \in \mathrm{Top}-K(A_i)} A_{i,k}$$

基于 SinkRatio，MLA-Gen 在两条路径上同时干预：
- **sink-mask**：在注意力计算阶段，当时序 $t > t_\text{thresh}$ 时，将起始 token $j_0$ 的注意力权重强制置零，迫使模型关注更广泛的语义 token。Figure 5 的可视化对比清晰展示了掩码前后注意力分布的变化——未掩码模型的注意力几乎全集中在 `<start token>`，而掩码模型保留了 `<re>`、`<arranging>` 等语义 token 的较高注意力。
- **sink-ctrl**：在采样阶段，根据 SinkRatio 自适应调节分类器自由引导（CFG）的强度，通过 $k_\text{eff} = k_\text{base} (1 + \alpha \cdot \mathrm{SinkRatio})$ 动态修正引导信号，避免注意力沉没导致的引导偏差。

### 推理流程

完整推理过程为：从噪声 $X_0$ 出发，ODE 求解器在每一步调用 $v_\theta$ 预测速度场。$v_\theta$ 内部，隐藏特征依次经过记忆槽位注意力（注入全局先验）、局部交叉注意力（融合细粒度文本条件），并在注意力计算中应用 sink-mask（抑制起始 token）。采样过程中，sink-ctrl 根据实时 SinkRatio 动态调节 CFG 引导信号，最终在潜在空间中生成运动编码，经解码器恢复为运动序列。

这一 pipeline 的核心设计逻辑在于：记忆槽位提供“骨架”，局部对齐填充“血肉”，而 SinkRatio 机制确保语义信号不被注意力沉没所淹没——三者协同，系统性地提升了运动-语言对齐与生成质量。

### 补充图表

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our MLA-Gen framework. It comprises three complementary components: Memory Slots for capturing global motion priors, Motion-Language Alignment for providing fine-grained textual semantics, and a SinkRatio-based mechanism that models and mitigates the attention sink phenomenon during both attention computation (sink-mask) and sampling (sink-ctrl)*



MLA-Gen 以条件流匹配（Conditional Flow Matching）为生成骨干，在潜在运动空间中建模条件分布 $p(X|y)$。其核心设计围绕三个递进式模块展开：全局运动先验注入、局部运动-语言对齐，以及注意力沉没（Attention Sink）度量与缓解。

### 3.1 条件流匹配骨干

运动自编码器先将原始运动序列压缩至潜在空间。生成过程由速度网络 $v_\theta$ 驱动，遵循流ODE：

$$\frac{d\psi_t(X_0)}{dt} = v_\theta(\psi_t(X_0), t, y), \quad \psi_0(X_0) = X_0 \tag{1}$$

其中 $y$ 为文本条件，$\psi_t$ 为从初始噪声 $X_0$ 到数据分布 $X_1$ 的流映射。采用 Rectified Flow 的线性插值路径：

$$X_t = (1-t) X_0 + t X_1, \quad t \in [0,1] \tag{2}$$

训练目标为最小化预测速度与恒定目标速度的 $L_2$ 距离：

$$\mathcal{L}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(0,1), X_0 \sim p_0, X_1 \sim q} \left[ \| v_\theta(X_t, t, y) - (X_1 - X_0) \|_2^2 \right] \tag{3}$$

### 3.2 全局先验与局部对齐

**记忆槽位模块（Memory Slots）** 引入一组可学习记忆槽位 $M \in \mathbb{R}^{S \times D_{flow}}$，作为共享运动原型。在每层 Transformer 中，通过交叉注意力向隐藏特征 $h$ 注入全局运动先验：

$$\hat{h} = h + \mathrm{Attn}(Q=h, K=M, V=M) \tag{4}$$

该机制使模型在生成早期即可从槽位中检索典型运动模式，提供结构化的全局约束。

**局部运动-语言对齐模块** 在帧级建立运动特征与文本 token 的细粒度对应。以运动帧特征 $z$ 为 Query，文本 token 经上投影 $W_{up}T$ 作为 Key 和 Value，计算局部条件：

$$C_l = \mathrm{Attn}(Q=z, K=W_{up}T, V=W_{up}T) \tag{5}$$

随后与全局条件 $C_g$ 加权融合，形成最终条件：

$$C = C_g + \lambda \cdot W_{down} C_l \tag{6}$$

其中 $\lambda$ 为融合系数，$W_{down}$ 将局部条件投影回与全局条件一致的维度。这一设计弥补了仅依赖全局 CLIP 文本特征时对细粒度语义（如“arranging”、“reaching”等动作细节）的遗漏。

### 3.3 注意力沉没的量化

在跨模态注意力中，论文发现注意力权重不成比例地集中在 `<start token>` 等无信息 token 上，称为“注意力沉没”现象。为量化该效应，定义 SinkRatio：

$$\mathrm{SinkRatio} = \frac{1}{L} \sum_{i=1}^{L} s_i, \quad s_i = \sum_{k \in \mathrm{Top}-K(A_i)} A_{i,k} \tag{7}$$

其中 $A_i$ 为第 $i$ 帧对所有文本 token 的注意力分布，$s_i$ 为 top-K 注意力权重之和。SinkRatio 越高，表明注意力越集中于少数 token，语义利用越不充分。

### 3.4 沉没缓解：sink-mask 与 sink-ctrl

**sink-mask** 在采样后期直接抑制对起始 token 的注意力。当时间步 $t$ 超过阈值 $t_{thresh}$ 时，将 `<start token>` 位置 $j_0$ 的注意力置零：

$$\hat{A}_{i,j_0} = \begin{cases} 0, & \text{if } t > t_{thresh} \\ A_{i,j_0}, & \text{otherwise} \end{cases} \tag{8}$$

该机制迫使模型在生成细节阶段重新分配注意力到有语义的 token 上。

**sink-ctrl** 在分类器自由引导（CFG）层面自适应调节。标准 CFG 形式为：

$$X = X_{uncond} + w (X_{cond} - X_{uncond}) \tag{10}$$

sink-ctrl 将引导系数 $k_{base}$ 按 SinkRatio 动态放大：

$$k_{eff} = k_{base} (1 + \alpha \cdot \mathrm{SinkRatio}) \tag{9}$$

进而用有效系数修正引导信号 $\hat{E} = E - k_{eff} \cdot \mathrm{sign}(E)$。当注意力沉没严重（SinkRatio 高）时，$k_{eff}$ 增大，强化条件引导的校正力度；当注意力分布较均衡时，引导强度自动回落，避免过度修正。

### 补充图表

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/003_Figure_3.jpg]]
*Figure 3: Heatmap of the memory slots activation. Regions rendered in brighter yellow indicate higher attention weights between the corresponding motion frames and memory slots*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/004_Figure_4.jpg]]
*Figure 4: Heatmap of motion-language alignment. Regions rendered in brighter yellow indicate higher attention weights between the corresponding motion frames and text tokens*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/005_Figure_5.jpg]]
*Figure 5: Heatmaps comparison of alignment on the masked model (left) and the unmasked model (right). The textual descriptions and timesteps are kept consistent*



## 实验与关键发现

### 主实验结果

我们在HumanML3D数据集上对MLA-Gen进行了全面的定量评估，并与当前主流方法进行了对比。表1展示了各方法的FID、R-Precision、Matching Score和CLIP-score四项核心指标的结果。所有评估均重复20次并报告95%置信区间，确保统计可靠性。

**MLA-Gen在两个模型规模上均显著优于直接对比基线ACMDM。** 在大模型配置下，MLA-Gen-B的FID达到**0.040**，相比ACMDM-B的0.083降低了51.8%；在小模型配置下，MLA-Gen-S的FID为**0.056**，相比ACMDM-S的0.107降低了47.7%。这一跨规模的性能提升表明，记忆槽位和运动-语言对齐模块的设计并非仅适用于特定模型容量，而是具有较好的泛化性。

在语义对齐指标上，MLA-Gen同样保持领先：MLA-Gen-B的R-Precision Top-1达到**0.527**（ACMDM-B为0.522），Matching Score降至**3.108**（ACMDM-B为3.178），CLIP-score提升至**0.656**（ACMDM-B为0.652）。值得注意的是，尽管FID提升幅度显著（相对降幅约50%），语义对齐指标的绝对提升相对温和（约1-2%），这暗示FID的改善可能主要来源于运动质量和多样性的提升，而非单纯的文本条件匹配度增强。

与其他方法相比，MLA-Gen-B的FID（0.040）在所有对比方法中处于最优水平，超越了扩散模型基线MDM（Tevet et al., 2022）、MotionDiffuse（Zhang et al., 2024）、检索增强的ReMoDiffuse（Zhang et al., 2023）、潜在扩散模型MLD++、潜在一致性模型MotionLCM V2（Dai et al., 2024）以及掩码自回归扩散模型MARDM-e/MARDM-v（Meng et al., 2025）。

### 消融研究

为验证MLA-Gen各组件的独立贡献，我们进行了系统的消融实验，结果汇总于表3。

**记忆槽位与局部对齐的协同效应。** 在移除所有增强模块的基线配置（仅保留全局条件C_g）下，FID为0.120。单独引入记忆槽位（Memory）将FID降至0.110，单独引入局部运动-语言对齐模块（Align）将FID降至0.101。当两者同时启用时，FID进一步降至**0.076**，验证了全局运动先验与细粒度语义对齐之间的互补关系——记忆槽位提供跨序列共享的运动原型，而局部对齐补充帧级的文本语义细节，两者协同作用才能最大化生成质量。

**注意力沉没缓解的有效性。** sink-mask机制对生成质量的影响显著且与掩码强度正相关。在未使用sink-mask的配置下，FID为0.099；使用弱掩码（t_thresh=0.6）将FID降至0.069；使用强掩码（t_thresh=0.2）将FID进一步降至**0.056**。这一结果表明，更早地在采样过程中抑制对起始token的注意力集中，能够更有效地释放模型对语义token的利用能力。图6的SinkRatio曲线提供了机制层面的解释：未掩码模型的SinkRatio维持在0.9-1.0的高位，表明注意力几乎完全集中在起始token上；而掩码模型的SinkRatio降至0.6-0.4区间，注意力分布明显更加均衡。

**CFG中局部条件的适度引入。** 在CFG的无条件分支中引入50%的局部条件C_l，使FID从0.101降至0.070。这表明适度的局部语义信息能够稳定无条件生成过程，避免无条件分支因缺乏文本引导而产生低质量样本，从而提升CFG的整体效果。

**sink-ctrl自适应引导策略。** 基于SinkRatio的自适应CFG策略（sink-ctrl）将FID从固定策略的0.117大幅降至0.044，尽管R-Precision Top-1从0.510略降至0.501。这一权衡值得关注：sink-ctrl通过动态调节引导强度（k_eff = k_base (1 + α · SinkRatio)）显著提升了运动的整体质量和多样性，但略微牺牲了文本匹配精度。这暗示注意力沉没的缓解在改善运动自然度的同时，可能需要更精细的引导信号设计来维持语义保真度。

### 可视化分析

图5的注意力热力图对比直观展示了sink-mask的作用机制。在未掩码模型中，几乎全部注意力权重集中在<start token>上，语义token（如<re>、<arranging>）几乎未被利用；而掩码模型在相同文本描述和时间步下，注意力分布明显向有意义的语义token扩散，保留了<re>、<arranging>等词的高注意力区域。这验证了SinkRatio量化指标与注意力分布均衡性之间的一致性。

图7的运动生成可视化对比进一步印证了定量结果。ACMDM-S生成的动作为“一个人向前走然后蹲下”，虽然整体语义正确，但蹲下动作的幅度和时序细节不足；MLA-Gen-S生成的相同动作在蹲下阶段的姿态变化更加自然、细节更加丰富。这与MLA-Gen通过局部运动-语言对齐捕捉细粒度语义的设计目标一致。

### 失败模式与局限性

尽管MLA-Gen在多数场景下表现优异，但仍存在明确的失败模式。图8展示了一个典型失败案例：当输入文本描述极长且包含多个连续动作时，模型无法准确捕获所有细节，部分动作片段出现语义遗漏或时序错位。这一局限性在分析中被明确归因于当前全局-局部对齐机制在处理高度复杂语义时的容量不足。

此外，SinkRatio作为诊断指标仅度量注意力在top-K token上的集中程度，无法捕获token间的高阶语义依赖关系（如动词-宾语结构、时序因果关系等）。这意味着即使SinkRatio显示注意力分布均衡，模型仍可能在语义组合层面存在偏差，但现有指标无法检测此类问题。

当前设计完全基于流匹配框架，尽管论文指出该方法可迁移至自回归模型，但尚未进行实际验证。注意力沉没问题在不同生成范式（如自回归、扩散）下的表现特性可能不同，sink-mask和sink-ctrl的超参数（如t_thresh、α）可能需要针对不同框架重新调优。

> **注意：** 以上失败模式和局限性分析均来自论文自身的报告。关于极长文本场景下的具体性能退化程度、SinkRatio在高阶语义偏差检测中的定量不足程度，建议结合实际应用场景进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/007_Table_1.jpg]]
*Table 1: Quantitative text-to-motion evaluation in HumanML3D [15] dataset. We repeat the evaluation 20 times and report the average with 95% confidence interval. We use bold face / underline to indicate the best/2nd results, and gray shade to indicate the better results between our method and ACMDM [39]*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/010_Table_3.jpg]]
*Table 3: Ablation study of components in MLA-Gen. We use gray shade and bold face to denote the original configurations. Unless otherwise specified, all ablated variants share the same settings as the original model, except for the component under investigation. In Memory&Align, ?? and ?? denote memory slots and the motion-language alignment module. In sink-mask, strong and weak masks correspond to*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/008_Figure_7.jpg]]
*Figure 7: Visualization comparison between ACMDM-S [39] and our MLA-Gen-S*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/009_Table_2.jpg]]
*Table 2: Hyperparameter settings. Hyperparameters listed above the dividing line are those required for training, while those below correspond specifically to the MLA-Gen model*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/001_Figure_1.jpg]]
*Figure 1: Failure cases from previous text-to-motion generation framework [39], which captures global motion patterns but often overlooks fine-grained motion details. In these figures, the color gradient from dark to light represents the temporal progression of motion from earlier to later stages*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/006_Figure_6.jpg]]
*Figure 6: SinkRatio curves for masked and unmasked models. Each curve depicts the mean SinkRatio across all batch samples over timesteps, with the shaded region indicating the standard deviation*

![[assets/figures/papers/paper_list_l3311_https_arxiv_org_abs_2604_02973/figures/011_Figure_8.jpg]]
*Figure 8: A failure case of MLA-Gen with a very long textual description*



## 定位与知识库关联

### 基线关系与差异化定位

MLA-Gen 建立在条件流匹配（Conditional Flow Matching）框架之上，其直接对比骨干为 **ACMDM**（Meng et al., 2025），两者共享相同的流匹配生成范式与运动自编码器架构。然而，ACMDM 仅依赖全局 CLIP 文本特征作为条件信号，缺乏帧级运动与文本 token 之间的细粒度交互机制。MLA-Gen 的核心差异化在于三个递进式设计：

1. **记忆槽位（Memory Slots）**：引入可学习参数 $M \in \mathbb{R}^{S \times D_{\text{flow}}}$，通过交叉注意力 $\text{Attn}(Q=h, K=M, V=M)$ 向每层 Transformer 注入共享的全局运动原型。这一机制弥补了 ACMDM 仅使用单一全局文本向量导致运动先验不足的缺陷。

2. **局部运动-语言对齐（Motion-Language Alignment）**：基于帧级运动特征 $z$ 与文本 token $T$ 的交叉注意力 $C_l = \text{Attn}(Q=z, K=W_{\text{up}}T, V=W_{\text{up}}T)$，生成细粒度局部条件，并与全局条件融合为 $C = C_g + \lambda \cdot W_{\text{down}}C_l$。这直接回应了现有方法（如 Figure 1 所示）虽能捕获全局运动模式却遗漏关键细节的瓶颈。

3. **注意力沉没缓解（Sink-aware Mechanism）**：首次在运动生成领域识别并量化了跨模态注意力中的“注意力沉没”现象——注意力权重不成比例地集中在无信息的起始 token 上。通过定义 SinkRatio 度量注意力集中度，并设计 sink-mask（时序依赖的起始 token 掩码）和 sink-ctrl（基于 SinkRatio 的自适应分类器自由引导）两个互补策略，系统性地改善了语义利用效率。

在更广泛的基线谱系中，MLA-Gen 与以下方法形成对比：

- **扩散模型基线**：**MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2024）采用扩散生成范式，但同样缺乏显式的运动-语言细粒度对齐设计。**ReMoDiffuse**（Zhang et al., 2023）引入检索增强机制，其外部知识利用思路与 MLA-Gen 的记忆槽位形成互补但不同的技术路径。

- **潜在空间方法**：**MLD++** 和 **MotionLCM V2**（Dai et al., 2024）分别在潜在扩散和潜在一致性模型框架下工作，与 MLA-Gen 的流匹配范式不同，但共享在压缩潜在空间进行生成的思路。

- **自回归方法**：**MARDM-e/MARDM-v**（Meng et al., 2025）采用掩码自回归扩散模型，代表了另一类生成范式。MLA-Gen 的记忆槽位和对齐模块理论上可迁移至自回归框架，但论文未进行实际验证，这构成一个开放问题。

### 适用边界与局限

**适用场景**：MLA-Gen 在 HumanML3D 数据集的标准文本-动作生成任务上表现优异，尤其在中短文本描述和常规运动类别下，能有效改善全局语义与局部细节的对齐。消融实验（Table 3）表明，记忆槽位和局部对齐模块的组合使 FID 从 0.120（无两者）降至 0.076（完整），验证了两者的协同作用。

**已知局限**：

1. **极长文本与复杂语义**：Figure 8 展示了一个失败案例，MLA-Gen 在极长文本描述下可能无法准确捕获所有细节。这表明当前的对齐机制在面对长距离语义依赖时仍存在容量瓶颈。

2. **诊断能力有限**：SinkRatio 仅度量注意力集中程度，未直接捕获 token 间的高阶语义依赖关系。这意味着该指标可作为注意力分布的“健康检查”，但无法诊断更复杂的对齐失败模式（如语义错配、时序错位）。

3. **框架依赖性**：当前设计深度耦合于流匹配生成框架。虽然作者声称可迁移至自回归模型，但缺乏实验验证，迁移的可行性与性能保持尚不明确。

### 开放问题

1. **跨模态泛化**：运动-语言对齐的思想能否扩展到视频生成、具身智能体控制等其他多模态合成任务？记忆槽位作为一种通用的全局先验注入机制，在不同模态间的迁移性值得探索。

2. **更富表达力的对齐诊断**：能否设计超越 SinkRatio 的指标（如考虑高阶语义依赖、时序因果性）来更精细地诊断和指导运动-语言对齐？这可能需要引入对比学习或因果推断的方法。

3. **长文本鲁棒性**：在极长文本和复杂语义下，如何构建更健壮的全局-局部对齐机制？可能的路径包括层次化文本编码、分段对齐策略，或引入外部知识增强。

4. **注意力沉没的尺度特性**：注意力沉没问题在更大规模模型或自回归框架中是否表现出不同特性？sink-mask 的阈值 $t_{\text{thresh}}$ 和 sink-ctrl 的自适应系数 $\alpha$ 是否需要随模型规模动态调节？这些问题的回答将决定该机制的通用性。

5. **与检索增强方法的融合**：ReMoDiffuse 的检索增强思路与 MLA-Gen 的记忆槽位在功能上互补——前者提供实例级参考，后者提供类别级原型。两者的融合可能进一步提升生成多样性（Diversity）与语义对齐的协同优化。



## 原文 PDF

![[paperPDFs/arxiv_2026/Exploring_Motion-Language_Alignment_for_Text-driven_Motion_Generation.pdf]]

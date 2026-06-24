---
title: "DynFusion: Rethinking Condition Fusion for Adaptive Multi-Conditional Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DynFusion_Rethinking_Condition_Fusion_for_Adaptive_Multi_Conditional_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- DynFusion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 条件适配模块（CAM）与解耦多模态注意力（DMMA）结合，动态地根据扩散时间步和网络层自适应选择、融合条件，消除冗余和冲突。
primary_logic: 不同条件在扩散过程的不同阶段具有不同的重要性；通过数据驱动学习这种阶段依赖性，可以在不增加计算开销的前提下实现多条件的协同增强，而非简单堆叠。
claims:
- DynFusion 在四个多条件任务（Multi-Spatial、Subject-Insertion、Subject-Depth、Subject-Canny）上全面超越现有方法，且计算成本更低。
- 深度和边缘激活模式与生成阶段高度对齐：深度在早期主导，边缘在后期激增，主题和背景在中段活跃，验证了自适应门控的有效性。
- 消融实验证明 CAM、DMMA、Fusion-LoRA 以及适当的稀疏度均对性能有显著贡献，移除任一模快均导致 FID 升高。
- Multi-Spatial Generation 上 FID↓ = 6.52
---

# DynFusion: Rethinking Condition Fusion for Adaptive Multi-Conditional Text-to-Image Generation

> [!tip] 核心洞察
> 不同条件在扩散过程的不同阶段具有不同的重要性；通过数据驱动学习这种阶段依赖性，可以在不增加计算开销的前提下实现多条件的协同增强，而非简单堆叠。

| 字段 | 内容 |
|------|------|
| 中文题名 | DynFusion：面向自适应多条件文本到图像生成的条件融合再思考 |
| 英文题名 | DynFusion: Rethinking Condition Fusion for Adaptive Multi-Conditional Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Fang_DynFusion_Rethinking_Condition_Fusion_for_Adaptive_Multi-Conditional_Text-to-Image_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DynFusion |
| Dataset | Multi-Spatial Generation, Subject-Insertion Generation, Subject-Depth Generation, Subject-Canny Generation |

> [!tip] 效果简介
> - Multi-Spatial Generation 上，FID↓ 6.52 vs — (最优)；SSIM↑ 0.66 vs — (最优)；Speed↑ (it/s) 2.02 vs — (最优)。
> - Subject-Insertion Generation 上，FID↓ 4.53 vs — (最优)；CLIP-I↑ 97.21 vs — (最优)；Speed↑ (it/s) 2.09 vs — (最优)。
> - Subject-Depth Generation 上，FID↓ 6.21 vs — (最优)。

## 概述

### 问题背景与核心瓶颈

文本到图像生成模型在多条件可控生成场景下面临一个关键瓶颈：**异构条件（几何结构、语义内容、外观风格）被静态统一注入扩散过程，导致条件间相互干扰和控制不一致**。现有方案通常将所有条件通过求和、拼接或多模态注意力等机制不加区分地激活，忽略了不同条件在扩散去噪的不同阶段具有截然不同的重要性。这种“一刀切”的策略在需要同时保持主体身份、空间布局和纹理细节的设计场景下，严重限制了生成保真度与可控性。

### 核心方法

DynFusion 提出了一种**数据驱动的自适应条件融合范式**，核心思想是让模型自主学会“在什么时间、在网络的哪一层、激活哪些条件”。方法包含三个关键设计：

- **条件适配模块（CAM）**：以噪声嵌入为输入，通过解耦聚合与门控网络动态预测条件选择掩码，实现按需激活。
- **解耦多模态注意力（DMMA）**：隔离条件分支与去噪分支，噪声令牌作为查询同时关注文本和所有视觉条件，但条件令牌之间不进行信息交互，从而保持条件信号的纯度。
- **Fusion-LoRA**：低秩适配模块，修正多条件动态激活带来的噪声潜变量分布偏移，提升集成稳定性。

与静态统一激活的基线方案相比，DynFusion 在不增加额外计算开销的前提下，实现了多条件的**协同增强而非简单堆叠**。

### 方法谱系与知识库定位

DynFusion 处于**多条件可控图像生成**这一研究方向，其方法定位可从以下维度理解：

- **相对于单条件可控生成**：ControlNet（Zhang et al., ICCV 2023）和 IP-Adapter（Ye et al., 2023）分别从结构控制和外观注入角度实现了高质量的单条件生成，但缺乏对多条件协同的原生支持。DynFusion 在此基础上引入动态门控，将单条件能力扩展至多条件场景。
- **相对于多条件统一控制**：UniControlNet（Zhao et al., NeurIPS 2023）和 Cocktail（Hu et al., NeurIPS 2023）尝试统一处理多种条件模态，但仍采用静态融合策略。DynFusion 的关键突破在于将“何时使用何种条件”的决策从人工设计转变为数据驱动的自适应学习。
- **相对于 DiT 架构下的高效控制**：OminiControl（Tan et al., 2024）和 EasyControl（Zhang et al., ICCV 2025）在 DiT 骨干上实现了轻量级条件注入，但同样未解决多条件下的条件干扰问题。DynFusion 的解耦注意力设计直接针对这一缺陷，在保持高效推理的同时提升了多条件一致性。

### 主要结果概要

DynFusion 在四个多条件任务上进行了全面验证：

| 任务 | 关键指标 | DynFusion 表现 |
|------|---------|---------------|
| Multi-Spatial | FID↓ / SSIM↑ | 6.52 / 0.66（最优） |
| Subject-Insertion | FID↓ / CLIP-I↑ | 4.53 / 97.21（最优） |
| Subject-Depth | FID↓ / SSIM↑ | 6.21 / 0.56（最优） |
| Subject-Canny | FID↓ / SSIM↑ | 5.72 / 0.64（最优） |

在所有任务上，DynFusion 均以更低的参数量和 FLOPs 取得了最优的 FID 和保真度指标，同时推理速度达到 2.02–2.09 it/s，实现了**生成质量与计算效率的双重提升**（Table 1）。

消融实验进一步验证了各组件的必要性：移除 CAM 的自适应门控（退化为均匀激活）导致 FID 升高；替换 DMMA 为标准多模态注意力不仅增加计算量，还降低了生成质量；移除 Fusion-LoRA 使 FID 从 4.53 升至 5.93。条件激活动态可视化（Figure 4）直观展示了深度条件在去噪早期主导、边缘条件在后期激增、主题和背景在中段活跃的阶段依赖模式，为自适应门控的有效性提供了机理解释。

## 背景与动机

### 问题背景

文本到图像生成模型在近两年取得了显著进展，从早期的单文本提示生成逐步演化为支持多种视觉条件（如空间布局、深度图、边缘图、主体图像）的可控生成。这一趋势的核心驱动力在于：真实世界的创作需求往往需要同时满足几何结构、语义内容和外观风格等多维约束，单一条件已难以胜任复杂的设计场景。然而，当多个异构条件——例如一张主体参考图、一张深度图、一张 Canny 边缘图——同时注入扩散模型时，**条件干扰**与**控制不一致**成为制约生成质量的关键瓶颈。

### 现有方法的缺口

当前主流的多条件可控生成方案可归纳为两类范式，但均存在结构性缺陷：

**第一类：条件信号聚合。** 典型方法如 **UniControlNet**（Zhao et al., NeurIPS 2023）和 **UniCombine**（Wang et al., 2025）试图在时间域上将多种视觉条件聚合成一个高度一致的控制信号，再注入去噪过程。这种“先统一、再注入”的策略隐含假设所有条件对生成过程的贡献是静态且均等的，忽略了不同条件在扩散去噪的不同阶段具有截然不同的重要性。

**第二类：多模态注意力融合。** 以 **Cocktail**（Hu et al., NeurIPS 2023）和 **EasyControl**（Zhang et al., ICCV 2025）为代表的方法，通过多模态注意力（MMA）让噪声表征在潜空间中同时关注文本和所有视觉条件。然而，标准 MMA 允许条件令牌之间进行信息交互，导致异构条件在注意力计算中相互“污染”——例如，主体外观令牌可能被深度几何令牌错误地重新加权，从而削弱各自的控制纯度。

这两种范式的共同症结在于：**条件注入策略是静态的、统一的**。无论扩散过程处于早期布局阶段还是后期纹理细化阶段，所有条件都被无差别地激活，既引入了冗余计算，又引发了条件间的冲突与干扰。Figure 2 直观对比了这三种方案：聚合方案（a）丢失了条件的时序差异性，MMA 方案（b）存在条件间的信息泄漏，而本文提出的动态融合方案（c）则根据当前去噪需求自适应地选择条件。

### 核心动机

本文观察到，扩散模型的去噪过程具有天然的**阶段依赖性**：早期步骤主要确定全局布局和几何结构，中期步骤建立语义对应和主体身份，后期步骤则聚焦于纹理细节和边缘锐化。在这一洞察下，不同视觉条件理应在不同时间步和不同网络层被差异化地激活。例如，深度图在去噪早期对布局约束至关重要，而 Canny 边缘图在后期对细节保真度更为关键。

基于此，本文提出 **DynFusion**，核心动机是：**以数据驱动的方式学习“何时、何处、激活何种条件”的自适应门控策略**，替代现有的静态条件堆叠范式。具体而言，DynFusion 通过条件适配模块（CAM）根据噪声嵌入动态预测条件选择掩码，实现按需激活；通过解耦多模态注意力（DMMA）隔离条件分支与去噪分支，杜绝条件间的信息污染；并通过 Fusion-LoRA 修正因条件动态激活带来的噪声潜变量分布偏移。这一设计在消除条件冗余与冲突的同时，不增加推理计算开销，甚至在稀疏激活下实现了效率提升（见 Table 1 速度指标）。

### 待验证的开放问题

尽管本文在四个多条件任务上取得了全面的定量与定性优势，以下问题仍需进一步探索：条件激活模式在不同骨干架构（如 SD3 vs. FLUX）上的可迁移性；当条件数量扩展至四个以上时，动态门控是否会遭遇组合爆炸或稀疏度不稳定；以及在小规模数据集上习得的门控策略对未见过的新模态条件的泛化能力。这些问题将直接影响该范式向更广泛的多模态生成任务的推广。

## 核心创新

DynFusion 的核心创新在于将多条件可控生成从“静态堆叠”范式转向“数据驱动的动态融合”范式。其关键改造体现在三个相互协同的 **changed slots** 上，共同解决了异构条件间的干扰与控制不一致问题。

### 1. 条件注入策略：从静态统一激活到动态门控选择

现有方法（如 **ControlNet** (Zhang et al., ICCV 2023)、**UniControlNet** (Zhao et al., NeurIPS 2023)、**Cocktail** (Hu et al., NeurIPS 2023)）通常采用静态统一策略——所有条件被同时激活，通过求和、拼接或多模态注意力统一注入去噪网络。这种“全开”模式忽略了不同条件在扩散过程各阶段重要性的差异，导致条件冗余甚至冲突。

DynFusion 引入 **条件适配模块（Condition Adaptation Module, CAM）**，以噪声嵌入为输入，动态预测每个 MMDiT 块的条件选择掩码 $\hat{\mathbf{M}} \in \{0, 1\}^n$。CAM 采用解耦聚合设计：沿序列维和嵌入维分别进行平均池化以提取全局与局部特征，再通过 MLP 融合后经 Gumbel Softmax 输出可微的离散掩码。这使得模型能够根据扩散时间步和网络层深度，自适应地决定“激活哪些条件”，而非无条件地激活全部。

Figure 4 直观展示了这一机制的效果：深度条件在去噪早期（步 0–10）高频激活，负责布局与结构确立；Canny 边缘条件在后期（步 15–25）激增，负责细节锐化；主题与背景条件在中段（步 10–20）达到峰值。这种阶段依赖性与生成过程的直觉高度一致，验证了动态门控的有效性。

### 2. 多模态注意力机制：从全交互到解耦隔离

标准多模态注意力（MMA）允许条件令牌之间进行信息交互，这在多条件场景下会导致条件信号相互“污染”——例如，深度条件可能被主题外观条件干扰，削弱结构控制力。

DynFusion 提出 **解耦多模态注意力（Decoupled Multi-Modal Attention, DMMA）**，其核心设计原则是：噪声令牌作为查询（Query），同时关注文本和所有视觉条件，但条件令牌之间**不计算注意力**。数学上，DMMA 将键（Key）和值（Value）拼接为 $[C_T^{k/v}, X^{k/v}, C_{V_{1:n}}^{k/v}]$，仅以噪声令牌 $X^q$ 为查询进行单次注意力计算。这一隔离策略从源头切断了条件间的信息流动，保证了每个控制信号的“纯度”。

Table 3 的消融实验表明，DMMA 相比 MMA 和 CMMA 不仅生成指标更优，且注意力操作次数从理论统一值 2.66T 降至实际 1.77T，实现了质量与效率的双赢。

### 3. 噪声特征适应：Fusion-LoRA 修正分布偏移

当 CAM 动态切换条件组合时，注入去噪分支的条件信号在数量、类型和强度上不断变化，导致噪声潜变量分布产生偏移。传统方法缺乏对此偏移的补偿机制，使得多条件集成效果不稳定。

DynFusion 在去噪分支中引入 **Fusion-LoRA**——一个低秩适配模块，专门用于修正因条件动态激活带来的噪声嵌入分布变化。Table 4 的消融实验显示，移除 Fusion-LoRA 后 Subject-Insertion 任务的 FID 从 4.53 升至 5.93，降幅显著，验证了该模块对多条件动态集成的关键支撑作用。

### 创新协同机制

上述三个 changed slots 并非孤立运作，而是形成闭环协同：CAM 决定“何时用哪些条件”，DMMA 保证“用到的条件互不干扰”，Fusion-LoRA 修正“动态切换带来的分布偏移”。这一协同使得 DynFusion 在不增加计算开销的前提下（Table 1 显示其参数量、FLOPs 和推理速度均优于现有方法），在四个多条件任务上全面超越基线——例如 Subject-Insertion 的 FID 达 4.53，Subject-Depth 的 SSIM 达 0.56，均为最优。

## 整体框架

DynFusion 的核心设计动机源于一个关键观察：在多条件可控扩散生成中，异构条件（如几何深度图、语义边缘图、外观参考图）在去噪过程的不同阶段具有显著不同的重要性，但现有方法普遍采用静态统一注入策略，导致条件间相互干扰、控制不一致，严重限制设计场景下的保真度与可控性。

为此，DynFusion 提出了一套**数据驱动的自适应条件融合框架**，其核心流水线由三个协同模块构成，围绕“何时激活哪些条件”这一核心问题展开：

1.  **条件适配模块（Condition Adaptation Module, CAM）**：接收当前去噪步的噪声嵌入，通过解耦聚合与 MLP 预测一个二值条件选择掩码，动态决定每个 MMDiT 块中哪些条件被激活。该模块使模型能够根据扩散时间步和网络层自适应地选择最优条件组合，而非静态激活所有条件。
2.  **解耦多模态注意力（Decoupled Multi-Modal Attention, DMMA）**：在条件注入阶段，将噪声令牌作为查询（Query），同时关注文本令牌和所有视觉条件令牌，但条件令牌之间**不计算注意力交互**。这一设计隔离了条件分支与去噪分支，防止条件令牌间的信息交叉污染，保证条件信号的纯度。
3.  **Fusion-LoRA**：位于去噪分支的低秩适配模块，用于修正因多条件动态激活带来的噪声潜变量分布偏移，提升多条件集成的稳定性与生成质量。

在训练阶段，CAM 通过引入 **Gumbel Softmax** 使离散掩码可微，并将条件选择掩码转换为**注意力掩码**，在 Softmax 计算中剔除未被选中条件令牌的影响，同时保持矩阵形状不变以支持批量并行训练。推理时，未被选中的条件分支直接被跳过，从而在提升生成质量的同时降低计算开销。整体优化目标为流匹配损失与稀疏度损失的加权组合：

$$\mathcal{L}_{\theta} = \mathcal{L}_{\mathrm{diff}} + \alpha \cdot \mathcal{L}_{\mathrm{sps}}$$

其中稀疏度损失 $\mathcal{L}_{\mathrm{sps}}$ 鼓励模型以较少的条件激活实现高质量生成，在生成效果与计算效率之间取得平衡。

图 3 展示了 DynFusion 的整体框架：前向过程中，CAM 基于噪声嵌入生成条件激活指令；训练过程中，注意力掩码与 Gumbel 噪声被整合到多模态注意力的 Softmax 计算中，实现端到端训练。

### 补充图表

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our proposed DynFusion framework. (a) During forward process, the CAM generates instructions based on the noise embeddings to activate the optimal condition combination. (b) During training, we incorporate the attention mask with gumbel noise into the softmax calculation of multi-modal attention to filter out the invalid conditions, thus enabling end-to-end training*

## 核心模块与公式推导

DynFusion 的核心由三个模块构成：条件适配模块（CAM）、解耦多模态注意力（DMMA）和 Fusion-LoRA。三者协同实现“在什么时间步、在网络的哪一层、激活哪些条件”的动态决策。

### 条件适配模块（CAM）

CAM 的输入是当前扩散时间步的噪声令牌 $\mathbf{X} \in \mathbb{R}^{* \times d}$，输出是一个二值掩码 $\hat{\mathbf{M}} \in \{0, 1\}^n$，指示 $n$ 个视觉条件中哪些被激活。其内部采用解耦聚合策略，分别沿序列维和嵌入维进行平均池化，以捕获全局依赖和局部表征：

$$
\mathbf{Z}_{\mathrm{global}} = \mathrm{MLP}_{\mathrm{glb}}\big(\mathrm{Agg}_{\mathrm{seq}}(\mathbf{X}); \boldsymbol{\Theta}_{\mathrm{glb}}\big)
$$

$$
\mathbf{Z}_{\mathrm{local}} = \mathrm{MLP}_{\mathrm{loc}}\big(\mathrm{Agg}_{\mathrm{emb}}(\mathbf{X}); \boldsymbol{\Theta}_{\mathrm{loc}}\big)
$$

其中 $\mathrm{Agg}_{\mathrm{seq}}$ 对所有 token 求均值（得到 $d$ 维全局特征），$\mathrm{Agg}_{\mathrm{emb}}$ 对每个 token 的嵌入维度求均值（得到序列长度的局部特征）。融合后的特征 $\mathbf{Z}_{\mathrm{glb-loc}}$ 经 MLP 与激活函数 $\mathrm{Act}(\cdot)$ 预测掩码：

$$
\mathbf{M} = \mathrm{Act}\big(\mathrm{MLP}_{\mathrm{mask}}(\mathbf{Z}_{\mathrm{glb-loc}}; \Theta_{\mathrm{glb-loc}})\big)
$$

为使离散掩码可微，训练时在 $\mathrm{Act}(\cdot)$ 中注入 Gumbel 噪声，使 $\hat{\mathbf{M}}$ 近似为可微版本。同时，将二值掩码转换为注意力掩码，以在 Softmax 中屏蔽被丢弃的条件 token，同时保持 token 数量固定以支持批量并行训练：

$$
\hat{\mathbf{M}}_{\mathrm{attn}}^{(i,j)} = \begin{cases} 0, & \text{if } \hat{\mathbf{M}}_{\mathcal{C}(i)} \wedge \hat{\mathbf{M}}_{\mathcal{C}(j)} = 0; \\ 1, & \text{otherwise}. \end{cases}
$$

掩码化注意力分数为：

$$
\tilde{\mathbf{A}}^{(i,j)} = \frac{\exp(\mathbf{P}^{(i,j)}) \, \hat{\mathbf{M}}_{\mathrm{attn}}^{(i,j)}}{\sum_{k=1}^{N} \exp(\mathbf{P}^{(i,j)}) \, \hat{\mathbf{M}}_{\mathrm{attn}}^{(i,j)} + \varepsilon}
$$

其中 $\mathbf{P} = Q K^{\top} / \sqrt{d}$ 为缩放点积注意力得分。

### 解耦多模态注意力（DMMA）

标准多模态注意力（MMA）允许条件 token 之间进行信息交互，容易引入条件间干扰。DMMA 将条件分支与去噪分支隔离：噪声 token $X^q$ 作为查询，同时关注文本 token $C_T$ 和所有视觉条件 token $C_{V_{1:n}}$，但条件 token 之间不计算注意力，从而保证条件信号的纯度：

$$
\mathrm{DMMA}(Q=X^q, K/V=[C_T^{k/v}, X^{k/v}, C_{V_{1:n}}^{k/v}]) = \mathrm{Softmax}\left(\frac{1}{\sqrt{d}} X^q [C_T^k, X^k, C_{V_{1:n}}^k]^{\top}\right) [C_T^v, X^k, C_{V_{1:n}}^v]
$$

这一设计在减少注意力操作次数的同时，防止了异构条件间的冗余交互。

### Fusion-LoRA

多条件动态激活会改变噪声潜变量的分布，Fusion-LoRA 是一个低秩适配模块，位于去噪分支中，用于修正这种分布偏移。它以极小的参数量调制不同数量和组合的条件信号，提升多条件集成的稳定性。消融实验证实，移除 Fusion-LoRA 会导致 FID 从 4.53 升至 5.93（Table 4）。

### 联合优化目标

训练损失由流匹配损失 $\mathcal{L}_{\mathrm{diff}}$ 和稀疏度损失 $\mathcal{L}_{\mathrm{sps}}$ 加权组合，使模型在高生成质量与低计算开销之间取得平衡：

$$
\mathcal{L}_{\theta} = \mathcal{L}_{\mathrm{diff}} + \alpha \cdot \mathcal{L}_{\mathrm{sps}}
$$

稀疏度损失鼓励 CAM 输出稀疏的条件激活模式，实验表明 50% 稀疏度取得最佳 FID（4.77），过度稀疏或全激活均导致性能下降（Table 5）。

### 补充图表

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of different schemes dealing with multiple conditions. (a) Aggregating various visual conditions into a highly consistent control signal in the temporal domain. (b) Noise representation acquires spatial modal knowledge in the latent space through multi-modal attention. (c) We employ dynamic condition fusion to precisely match the current demands*

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of denoising step at steps 5, 10, 15, 20 and 25, where each pair includes the generated result and condition activation distribution. Subject, background, depth, canny are used to guide image generation*

## 实验与分析

### 主要定量结果

DynFusion 在四个多条件可控生成任务上进行了系统评估，包括 Multi‑Spatial、Subject‑Insertion、Subject‑Depth 和 Subject‑Canny，所有对比方法均基于 **FLUX** 骨干网络，在相同硬件环境下测量参数量、FLOPs 与推理速度，确保对比公平性。

Table 1 汇总了 DynFusion 与 **ControlNet** (Zhang et al., ICCV 2023)、**IP‑Adapter** (Ye et al., 2023)、**OminiControl** (Tan et al., 2024)、**UniControlNet** (Zhao et al., NeurIPS 2023)、**Cocktail** (Hu et al., NeurIPS 2023)、**EasyControl** (Zhang et al., ICCV 2025) 以及 **UniCombine** (Wang et al., 2025) 等方法的全面对比。在 Multi‑Spatial 任务上，DynFusion 取得 FID 6.52、SSIM 0.66、推理速度 2.02 it/s，三项指标均为最优。在 Subject‑Insertion 任务上，FID 达到 4.53，CLIP‑I 达到 97.21，速度 2.09 it/s，同样全面领先。在 Subject‑Depth 和 Subject‑Canny 任务上，FID 分别为 6.21 和 5.72，SSIM 分别为 0.56 和 0.64，速度均保持在 2.02–2.04 it/s。值得注意的是，DynFusion 在取得最优生成质量的同时，引入的额外参数量和 FLOPs 均低于多数对比方法，验证了自适应条件融合在效率与效果上的双重优势。

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of our method with existing approaches on Multi-Spatial, Subject-Insertion, Subject-Depth, and Subject-Canny conditional generative tasks. The bold and underlined figures represent the optimal and sub-optimal results, respectively. In the last column, “Params↓” and “FLOPs↓” are additional introduced parameters and floating-point operations for processing visual conditions on FLUX, and “Speed↑” denotes diffusion iterations per second, which is the average on test set*

Figure 7 和 Figure 8 分别展示了 Subject‑Depth 与 Subject‑Canny 任务的定性对比。DynFusion 生成的图像在主体一致性、深度结构对齐和边缘细节保持方面均明显优于基线方法，且未出现条件冲突导致的伪影或主体丢失。

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparison on Subject-Depth generation*

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative comparison on Subject-Canny generation*

### 条件激活动态分析

Figure 4 可视化了去噪过程中不同时间步下的条件激活动态，揭示了条件重要性的阶段依赖性。深度条件（绿色虚线）在去噪早期（步 0–10）主导激活，负责建立全局空间结构；主体条件（蓝色线）和背景条件（黄色线）在中期（步 10–20）达到峰值，参与语义布局和外观细化；边缘条件（红色线）在后期（步 15–25）急剧上升，用于精修局部细节。这一模式直观解释了为何静态统一激活会导致条件冗余和干扰——不同条件在扩散过程的不同阶段具有截然不同的控制需求，DynFusion 的 CAM 模块正是通过学习这种阶段依赖性来实现自适应门控。

### 消融实验

**自适应条件融合策略** (Table 2)：在 Subject‑Insertion 任务上，对比了 Uniform（统一激活所有条件）、Sole（Softmax 选择）和 Free（Sigmoid 自由选择）三种策略。Free 策略取得 FID 4.53，显著优于 Uniform 和 Sole，证明数据驱动的自适应门控比固定或概率性选择更能消除条件冗余。

**解耦多模态注意力 DMMA** (Table 3)：相比标准多模态注意力 MMA 和级联多模态注意力 CMMA，DMMA 将实际注意力操作次数从理论统一的 2.66T 降至 1.77T，同时生成指标更优。这验证了隔离条件分支、防止条件 token 间信息交互对保持条件信号纯度的重要性。

**Fusion‑LoRA 模块** (Table 4)：移除 Fusion‑LoRA 后 FID 从 4.53 升至 5.93，降幅显著。该模块通过低秩适配修正多条件动态激活带来的噪声嵌入分布偏移，是多条件协同集成的关键保障。

**条件稀疏度** (Table 5)：当条件稀疏度设为 50% 时取得最佳 FID 4.77；过度稀疏（30%）导致信息缺失，完全密集（100%）则引入冗余干扰，均使性能下降。这直接证明了动态稀疏化在平衡信息完整性与计算效率方面的必要性。

### 失败模式与局限性

论文未显式报告失败案例或局限性分析。从条件激活动态 (Figure 4) 可推断，当条件类型组合发生显著变化（例如引入全新模态）时，CAM 学得的阶段依赖性可能失效，需要重新训练或微调。此外，稀疏度消融 (Table 5) 表明门控策略对稀疏度超参数敏感，实际部署时需针对任务进行调优。以上推断需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/011_Table_2.jpg]]
*Table 2: Quantitative ablation of adaptive condition fusion strategy on Subject-Insertion task. “Uniform” means activating all conditions uniformly. “Sole” and “Free” indicate selecting the conditions with softmax and sigmoid function, respectively*

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/010_Table_4.jpg]]
*Table 4: Quantitative ablation of Fusion-LoRA component on Subject-Insertion task. Fusion-LoRA is capable of modulating different quantities and combinations of conditional signals, thereby providing better assistance in generating*

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison on Subject-Insertion generation*

![[assets/figures/papers/paper_list_l2308_https_openaccess_thecvf_com_content_CVPR2026_html_Fang_DynFusion_Rethink/figures/001_Figure_1.jpg]]
*Figure 1: Demonstrations of DynFusion’s versatile capabilities. (a) Controllable image generation under a single visual condition (e.g., subject-driven generation and spatially-aligned tasks). (b) Multi-conditional controllable generation. Compared with single-conditional generation, it improves the image quality, controllability and flexibility. Meanwhile, proposed dynamic condition fusion performs better than uniform strategy by eliminating condition redundancies. (c) Visualization results under more conditions. (d) Quantitative results of our DynFusion. We simultaneously improved both the generation effect and efficiency*

## 方法谱系与知识库定位

### 1. 从单条件可控到多条件融合的演进

DynFusion 处于扩散模型可控生成从“单条件注入”向“多条件协同”演进的关键节点。早期工作如 **ControlNet** (Zhang et al., ICCV 2023) 和 **IP-Adapter** (Ye et al., 2023) 分别解决了结构控制与外观/风格注入问题，但每条路径独立运作，无法处理多条件共存场景。**UniControlNet** (Zhao et al., NeurIPS 2023) 试图统一多条件控制，但其本质仍是将异构条件编码为统一表示后静态注入，未能解决条件间的冗余与冲突。

在 DiT 范式下，**OminiControl** (Tan et al., 2024) 和 **EasyControl** (Zhang et al., ICCV 2025) 通过多任务训练实现了更高效的条件注入，但仍采用“全激活、统一融合”策略。**Cocktail** (Hu et al., NeurIPS 2023) 和 **UniCombine** (Wang et al., 2025) 探索了多模态条件混合，但其融合机制是静态的——所有条件在去噪全过程被同等对待，忽略了不同条件在扩散不同阶段的差异化重要性。

DynFusion 的核心突破在于将条件融合从“静态统一”转变为“数据驱动的动态选择”。这一转变的因果机制是：**不同条件在扩散过程的不同阶段具有不同的重要性**——深度等几何线索在早期布局阶段主导，边缘等细节线索在后期精修阶段激增，而主题和背景语义在中段活跃（Figure 4 的可视化直接验证了这一阶段依赖性）。通过 CAM 模块学习这种阶段依赖性，DynFusion 在无需人工设计规则的前提下实现了自适应条件选择。

### 2. 关键技术差异与因果机制

与现有方法的三个核心差异槽位：

| 设计维度 | 现有方法 | DynFusion | 因果机制 |
|---------|---------|-----------|---------|
| 条件注入策略 | 静态统一激活，求和/拼接/注意力统一注入 | CAM 根据扩散时间步和网络层动态门控 | 消除条件冗余与冲突，按需激活，降低计算开销 |
| 多模态注意力 | 标准 MMA，条件令牌间允许信息交互 | DMMA，噪声令牌作为查询，条件令牌间无信息交换 | 隔离条件分支与去噪分支，保证条件信号纯度 |
| 噪声特征适应 | 无特殊适应模块 | Fusion-LoRA 修正多条件动态激活后的噪声分布 | 缓解动态门控带来的分布偏移，提升集成稳定性 |

这三个模块形成因果闭环：CAM 决定“何时用哪些条件”，DMMA 保证“用的时候不互相干扰”，Fusion-LoRA 则修正“动态选择带来的副作用”。消融实验（Table 2–5）提供了强证据：移除任一模块均导致 FID 显著升高（如移除 Fusion-LoRA 使 FID 从 4.53 升至 5.93），验证了每个模块的独立贡献。

### 3. 适用边界与局限

**适用场景**：
- 多条件可控生成任务，包括多空间对齐（Multi-Spatial）、主体插入（Subject-Insertion）、主体-深度联合（Subject-Depth）、主体-边缘联合（Subject-Canny）
- 基于 FLUX 骨干的 DiT 架构，方法通过 LoRA/适配器方式实现，冻结原有权重，参数量可控

**已知局限**（论文未明确列出，需手动验证）：
- 当前验证集中在 2–4 个条件组合，当条件数量进一步增加（例如 >4）时，动态门控是否会遭遇组合爆炸或稀疏度不稳定，论文未提供实验证据
- CAM 的决策过程是隐式学习的，缺乏显式可解释性约束——门控掩码的语义含义需要事后分析（如 Figure 4 的激活模式可视化），而非在训练中被显式引导
- 论文未讨论在小规模数据集上学习的门控策略对域外条件（未见过的新模态）的泛化能力

### 4. 开放问题与未来方向

1. **跨骨干泛化性**：条件激活模式是否在不同骨干（如 SD3、FLUX.1）以及不同条件类型组合上保持一致？当前结论仅基于 FLUX 骨干验证。

2. **可扩展性边界**：当条件数量从 4 扩展到 10+ 时，CAM 的门控搜索空间呈指数增长，当前基于 Gumbel Softmax 的离散掩码训练策略是否仍然稳定？是否需要引入层次化门控或条件分组机制？

3. **可解释性增强**：能否将 CAM 的决策过程与条件重要性显式关联，例如通过引入条件级别的归因损失或对比学习约束，使门控掩码具有更清晰的语义含义？

4. **跨模态与跨任务迁移**：多条件自适应融合范式能否直接扩展到视频生成（时间维度的条件动态变化）、3D 生成（多视角条件一致性）或图像编辑（局部条件与全局条件的协调）？这需要重新审视 DMMA 中“条件令牌间无信息交换”的设计是否仍然适用。

5. **稀疏度与质量的帕累托前沿**：Table 5 显示 50% 稀疏度取得最佳 FID，但这是否是任务无关的最优值？能否设计自适应稀疏度调度器，根据任务复杂度和条件冲突程度动态调整稀疏度目标？

## 原文 PDF

![[paperPDFs/CVPR_2026/DynFusion_Rethinking_Condition_Fusion_for_Adaptive_Multi_Conditional_Text_to_Image_Generation.pdf]]

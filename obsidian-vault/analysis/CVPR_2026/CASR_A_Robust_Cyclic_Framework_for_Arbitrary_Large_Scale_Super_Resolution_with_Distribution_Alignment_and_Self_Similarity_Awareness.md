---
title: "CASR: A Robust Cyclic Framework for Arbitrary Large-Scale Super-Resolution with Distribution Alignment and Self-Similarity Awareness"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CASR_A_Robust_Cyclic_Framework_for_Arbitrary_Large_Scale_Super_Resolution_with_Distribution_Alignment_and_Self_Similarity_Awareness.pdf
project_link: null
code_link: null
aliases:
- CASR
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 将超大尺度超分重新定义为一系列分布内尺度转换的循环过程，通过超像素结构对齐（SSAM）抑制分布漂移，并借助自相似性感知精炼（SARM）恢复跨patch的纹理一致性。
primary_logic: 实现极端超分的关键不在于模型或数据规模，而在于理解并调节表征在尺度间的演化；将输入解耦为超像素低通表示与深度结构约束可有效过滤级联噪声，同时用特征空间自相似性矩阵约束可保持全局纹理一致性。
claims:
- CASR在循环过程中保持更低的分布偏移（SIFID指标），稳定于训练分布附近。
- 在DIV8K合成数据集×30时，CASR的LPIPS比第二名LIIF+Diff低16.9%，并在MUSIQ、NIQE、PI上分别相对IDM提升75.2%、降低12.3%和15.8%。
- 在RealSR真实数据集×30时，CASR的MUSIQ、NIQE、PI分别超越IDM 34.1%、6.5%和9.5%。
- 消融实验证明，超像素对齐、深度约束和自相似性精炼各自显著提升感知质量，完整模型取得最佳性能。
---

# CASR: A Robust Cyclic Framework for Arbitrary Large-Scale Super-Resolution with Distribution Alignment and Self-Similarity Awareness

> [!tip] 核心洞察
> 实现极端超分的关键不在于模型或数据规模，而在于理解并调节表征在尺度间的演化；将输入解耦为超像素低通表示与深度结构约束可有效过滤级联噪声，同时用特征空间自相似性矩阵约束可保持全局纹理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CASR：一种基于分布对齐与自相似性感知的任意大尺度超分辨率鲁棒循环框架 |
| 英文题名 | CASR: A Robust Cyclic Framework for Arbitrary Large-Scale Super-Resolution with Distribution Alignment and Self-Similarity Awareness |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22159) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | CASR |
| Dataset | DIV8K synthetic, RealSR, CelebA-HQ |

> [!tip] 效果简介
> - DIV8K synthetic (×30) 上，LPIPS 0.501 vs LIIF+Diff (约0.603) (相对降低16.9%)；MUSIQ 41.76 vs IDM (相对提升75.2%)；NIQE 6.98 vs IDM (相对降低12.3%)。
> - RealSR (×30) 上，MUSIQ 37.84 vs IDM (相对提升34.1%)；NIQE 7.81 vs IDM (相对降低6.5%)；PI 6.73 vs IDM (相对降低9.5%)。
> - CelebA-HQ (×12) 上，MUSIQ 71.71 vs IDM / Kim (明显更优)。

## 概要

### 问题背景与瓶颈

任意尺度超分辨率（Arbitrary-Scale Image Super-Resolution, ASISR）旨在从低分辨率输入重建任意放大倍数的高质量图像。现有方法——包括基于隐式神经表示的方法（如**LIIF** Chen et al., CVPR 2021；**CiaoSR** Cao et al., CVPR 2023）、基于归一化流的方法（如**LINF** Yao et al., CVPR 2023；**BFSR** Tsao et al., CVPR 2024）以及基于扩散模型的方法（如**IDM** Gao et al., CVPR 2023；**Kim** Kim and Kim, CVPR 2024）——在训练尺度范围内表现良好，但在超大尺度（如×30）下普遍面临严重的**跨尺度分布偏移**问题。当放大倍数远超训练分布时，模型输出逐渐偏离训练数据的分布，导致模糊加剧、细节丢失和伪影累积。此外，超大尺度超分通常需要分块处理，各图像块独立重建仅依赖重叠区域拼接，造成**跨patch纹理不一致**——同一语义对象在不同patch中被赋予不同的纹理模式（见图2）。这两个问题共同构成了超大尺度超分的核心瓶颈：**循环放大过程中的分布漂移与自相似性丧失**。

### 核心思路与方法定位

CASR提出了一种根本性的视角转换：**实现极端超分的关键不在于模型或数据规模，而在于理解并调控表征在尺度间的演化**。该方法将超大尺度超分重新定义为一系列**分布内尺度转换的循环过程**，通过两个核心模块解决上述双重瓶颈：

- **超像素结构对齐模块（SSAM）**：将输入图像解耦为超像素低通表示与深度结构约束，有效过滤循环过程中累积的级联噪声与伪影，将每一步的输入稳定在训练分布附近（见图4）。这一设计使循环放大过程中的分布偏移显著低于其他方法（见图1）。
- **自相似性感知精炼模块（SARM）**：利用缓存特征的全局自注意力、LR全局语义交叉注意力以及相关引导损失，在特征空间中约束重建图像与真值图像的自相似性矩阵一致，从而恢复跨patch的纹理一致性（见图5）。

CASR以SD-Turbo单步扩散模型为骨干网络，通过LoRA微调实现高效重建，并采用ControlNet分支注入结构控制信号。与现有方法将ASISR视为单步直接映射或独立级联不同，CASR将放大策略从“单步跨越分布外尺度”转变为“单模型循环逐步放大”（总尺度分解为子尺度乘积，每步≤s_max），确保每步推理均落在训练分布内。

### 主要结果概要

在DIV8K合成数据集×30尺度下，CASR的LPIPS比第二名**LIIF+Diff**相对降低16.9%，在MUSIQ、NIQE、PI上分别相对**IDM**提升75.2%、降低12.3%和15.8%。在RealSR真实数据集×30尺度下，CASR的MUSIQ、NIQE、PI分别超越**IDM** 34.1%、6.5%和9.5%，展现出对真实世界图像的强泛化能力。在CelebA-HQ人脸数据集×12尺度下，CASR准确重建眉目等细粒度特征，而**IDM**和**Kim**在此尺度下无法恢复面部细节。消融实验系统验证了超像素对齐、深度约束和自相似性精炼各自对感知质量的显著贡献，完整模型在所有指标上取得最佳性能。

### 方法谱系与知识库定位

CASR处于**ASISR与扩散模型超分**的交叉地带，其知识贡献可定位如下：

- **相对隐式神经表示方法**（LIIF, CiaoSR）：CASR摒弃了坐标到RGB的连续函数映射范式，转而采用循环扩散框架，通过分布对齐机制解决了隐式方法在训练尺度外的性能退化问题。
- **相对基于流的方法**（LINF, BFSR）：CASR不依赖归一化流的可逆变换，而是通过超像素分解实现更直接、更稳定的分布控制。
- **相对扩散ASISR方法**（IDM, Kim）：CASR引入了循环放大策略和自相似性感知精炼，弥补了现有扩散方法在跨patch一致性和级联稳定性方面的不足。
- **相对通用扩散后处理增强**（LIIF+Diff, CiaoSR+Diff）：CASR将扩散模型作为核心重建引擎而非后处理模块，实现了更紧致的端到端优化。

CASR的核心创新在于**将分布感知与自相似性约束系统性地嵌入循环放大框架**，为超大尺度超分辨率提供了一种鲁棒且可泛化的解决范式。



### 任意尺度超分辨率的现实需求与核心挑战

超分辨率（Super-Resolution, SR）旨在从低分辨率（LR）输入重建高分辨率（HR）图像，是计算机视觉中的经典逆问题。近年来，任意尺度超分辨率（Arbitrary-Scale Image Super-Resolution, ASISR）因其在单一模型中支持连续放大倍数的灵活性而受到广泛关注，代表性工作包括基于隐式神经表示的 **LIIF**（Chen et al., CVPR 2021）、基于归一化流的 **LINF**（Yao et al., CVPR 2023）和 **BFSR**（Tsao et al., CVPR 2024），以及基于扩散模型的 **IDM**（Gao et al., CVPR 2023）和 **Kim**（Kim and Kim, CVPR 2024）等。

然而，现有ASISR方法面临一个根本性瓶颈：**当推理尺度超出训练分布时，模型性能急剧退化**。具体表现为模糊、细节丢失和伪影累积，且这一问题在超大尺度（如×30）下尤为严重。其本质原因在于，ASISR模型在训练阶段通常仅接触有限尺度范围（如×1至×4），当推理时被要求执行远超训练范围的放大时，输入特征分布发生显著偏移，模型无法可靠地外推。

### 循环放大中的分布漂移与自相似性丧失

为应对超大尺度超分，一种直观策略是将总放大倍数分解为多个子尺度的级联或循环放大。然而，这种级联方式引入了两个相互交织的问题：

**跨尺度分布偏移（Cross-Scale Distribution Shift）。** 在循环过程中，每一步的输出都会累积噪声和伪影，导致后续步骤的输入分布逐渐偏离训练分布。Figure 1 通过SIFID指标量化了不同ASISR方法在循环级联过程中的分布稳定性：CASR的方法显著优于其他对比方法，能够在多次迭代后仍将重建图像保持在训练分布附近，而其他方法的分布偏移随迭代次数持续扩大。

**分块处理导致的自相似性丧失。** 受显存限制，超大尺度超分通常需要将图像切分为多个patch独立处理，再通过重叠区域拼接。如 Figure 2 所示，这种逐patch独立重建的方式破坏了图像内部的结构一致性——同一图像中本应具有相似纹理的重复区域（如对称的建筑立面、重复的图案）被重建为不同的纹理模式，产生视觉上的不协调。

### 现有方法的局限与研究动机

现有ASISR方法在设计上未充分解决上述两个问题。隐式神经表示方法（LIIF、CiaoSR）通过连续坐标映射实现任意尺度，但缺乏对循环过程中分布稳定的显式控制；流基方法（LINF、BFSR）虽然建模了尺度间的可逆映射，但在极端尺度下仍面临外推困难；扩散模型方法（IDM、Kim）借助生成先验提升了感知质量，但循环累积的伪影和跨patch不一致性依然存在。

上述分析揭示了实现极端超分的关键洞察：**核心瓶颈不在于模型容量或数据规模，而在于理解并调节表征在尺度间的演化**。具体而言，需要一种机制将输入解耦为稳定的低通表示与结构约束，以过滤级联噪声；同时，需要一种跨patch的一致性约束来保持全局纹理的协调性。这构成了CASR框架的核心设计动机：通过超像素结构对齐抑制分布漂移，并借助特征空间的自相似性矩阵约束恢复纹理一致性。



## 核心方法与创新机理

CASR的核心创新在于将任意大尺度超分辨率（ASISR）从“单步预测”或“多模型级联”范式，重新定义为**单模型循环逐步放大**的分布内尺度转换过程，并通过两个关键模块——**超像素结构对齐（SSAM）**和**自相似性感知精炼（SARM）**——分别解决循环过程中的分布漂移与跨patch纹理不一致问题。

### 1. 循环分布内放大策略：从单步外推到逐步演化

现有ASISR方法（如**LINF**（Yao et al., CVPR 2023）、**BFSR**（Tsao et al., CVPR 2024）、**IDM**（Gao et al., CVPR 2023）等）通常试图在单步内直接预测任意目标尺度，或级联多个专用网络。这种策略的根本缺陷在于：当目标尺度超出训练分布范围时，模型面临严重的跨尺度分布偏移，导致模糊、细节丢失和伪影累积，且循环过程中噪声会逐级放大。

CASR的解决思路是将总放大尺度 $s$ 分解为若干子尺度的乘积：

$$s = s^1 \times s^2 \times \cdots \times s^k \times \cdots \times s^K, \quad s^k \leq s_{\max}$$

框架执行 $K$ 次迭代上采样，每次仅放大一个分布内子尺度（不超过训练最大尺度 $s_{\max}$），使每步输入始终保持在模型熟悉的分布范围内。**同一模型**在循环中被重复调用，无需训练多个专用网络。这一策略的因果机制在于：**将“外推到未知分布”转化为“在已知分布内逐步演化”**，从根源上抑制了分布漂移的累积效应。Figure 1的SIFID分布稳定性对比直接验证了这一点——CASR在循环过程中保持显著更低的分布偏移，稳定于训练分布附近。

### 2. 超像素结构对齐（SSAM）：分布锚定与噪声过滤

仅靠循环分解仍不足以完全稳定分布——每次上采样引入的微小误差会在迭代中累积，形成级联噪声。SSAM模块的核心作用是在每次迭代前对输入进行**分布锚定**：将图像分解为超像素低通表示与深度结构图两个互补分量（Figure 4）。

具体而言，超像素分割网络（SSN）预测像素到超像素的软分配概率，对每个超像素区域 $r$ 计算归一化颜色表示：

$$C_r^{k-1} = \frac{1}{|r|} \sum_{i \in r} I_i^{k-1}$$

这一操作将视觉相似像素聚合为同质区域，有效滤除随机噪声和累积伪影，同时保留低频语义内容。深度图作为辅助结构约束，保持几何边界的一致性。**双分量解耦的关键洞察在于**：超像素图像提供了稳定、去噪的低通表示，使后续SR骨干网络始终接收“干净”的分布内输入；深度图则确保结构信息在去噪过程中不被破坏。消融实验证实，仅添加超像素对齐即可使LPIPS从0.585降至0.471，MUSIQ从31.73升至42.23（Table 4），验证了分布锚定对感知质量的决定性影响。

### 3. 自相似性感知精炼（SARM）：跨patch纹理一致性约束

大尺度超分通常需要分块处理，各patch独立重建仅依赖重叠区域拼接，导致相同语义区域（如重复纹理）被重建为不同模式（Figure 2）。SARM模块通过**特征空间自相似性约束**解决这一跨patch一致性问题。

SARM利用预训练SAM编码器提取深度特征 $e$，构造自相似性矩阵以编码图像内部纹理相关性：

$$R^k = e^k (e^k)^{\top}, \quad R^{\mathrm{gt}} = e^{\mathrm{gt}} (e^{\mathrm{gt}})^{\top}$$

通过相关引导损失约束重建图像与真值的自相似性结构一致：

$$L_{\mathrm{corr}} = \| R^k - R^{\mathrm{gt}} \|_2$$

模块内部采用缓存特征的全局自注意力实现跨patch信息融合，并通过LR全局语义交叉注意力注入低分辨率图像的全局上下文。消融实验表明，完整的SARM使LPIPS进一步降至0.450，MUSIQ升至51.44（Table 4 Full Model）；单独加入LR全局语义交叉注意力即可带来MUSIQ +2.34、NIQE -0.29的提升（Table 5）。这证明**自相似性感知不是简单的局部纹理匹配，而是需要全局语义引导的跨patch结构一致性建模**。

### 创新总结

CASR的三个changed slots构成了一条完整的因果链：**循环分布内放大**设定总体策略框架，**SSAM**在每次迭代入口处过滤级联噪声并锚定分布，**SARM**在每次迭代出口处恢复跨patch纹理一致性。三者的协同使得极大规模超分（×30甚至更高）在感知质量上显著超越现有方法——在DIV8K ×30上LPIPS相对第二名LIIF+Diff降低16.9%，MUSIQ相对IDM提升75.2%（Section 4.4.1）；在真实场景RealSR ×30上MUSIQ相对IDM提升34.1%（Section 4.4.2）。



CASR 将超大尺度超分辨率重新定义为一个**循环逐步放大**的过程，其核心设计原则是：将任意目标放大倍数 $s$ 分解为一系列子尺度的乘积 $s = s^1 \times s^2 \times \cdots \times s^K$，其中每一步的子尺度 $s^k \leq s_{\max}$ 始终落在模型的训练分布范围内。框架执行 $K$ 次迭代上采样，每一次迭代的中间结果作为下一次迭代的输入，从而将“跨尺度分布偏移”这一根本瓶颈转化为可控的分布内逐步演化问题。

整个 pipeline 由三个关键模块串联构成（Figure 3 示意）：

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the proposed CASR. The purple module denotes the SSAM, the green block corresponds to the SARM, and the gray U-Net represents the SR backbone*

1. **超像素结构对齐模块（SSAM）**：位于每次循环迭代的输入端，负责将当前图像分解为超像素低通表示与深度结构图两种互补表征。超像素表示通过对视觉相似像素的软分组与区域归一化 $C_{r}^{k-1} = \frac{1}{|r|} \sum_{i \in r} I_{i}^{k-1}$ 滤除级联过程中累积的噪声与伪影，深度图则保留高频几何边界，共同为后续 SR 骨干网络提供分布稳定的输入。

2. **自相似性感知精炼模块（SARM）**：作用于 SR 骨干网络的输出端，解决分块处理导致的跨 patch 纹理不一致问题。SARM 利用缓存特征的全局自注意力、LR 全局语义交叉注意力，以及基于预训练 SAM 编码器特征的自相似性矩阵约束 $L_{\mathrm{corr}} = \| R^{k} - R^{\mathrm{gt}} \|_2$，强制重建图像内部纹理相关性结构与真值保持一致。

3. **SR 骨干网络**：采用 SD-Turbo 单步扩散模型，经 LoRA 微调后执行分布内超分辨率重建，并通过 ControlNet 分支注入结构控制信号引导解码器细节生成。

信息流路径为：**输入图像 → SSAM（分布对齐与去噪）→ SR 骨干（上采样重建）→ SARM（跨 patch 纹理一致性精炼）→ 下一循环迭代**。该循环结构确保每一步都在训练分布附近运作，从根本上抑制了级联放大中的质量退化。



CASR 的核心架构由三个紧密协作的模块构成：**超像素结构对齐模块（SSAM）**、**自相似性感知精炼模块（SARM）**，以及基于 **SD-Turbo 扩散骨干网络** 的超分重建模块。它们共同支撑起“将总尺度 $s$ 分解为 $K$ 步子尺度 $s^k \leq s_{\max}$ 的循环逐步放大”这一核心策略。

### 3.1 超像素结构对齐模块（SSAM）

循环放大过程中，每一轮的输出会作为下一轮的输入，导致级联噪声与伪影在尺度间累积，使输入分布逐渐偏离训练分布。SSAM 的设计目标是在每一步放大前，将输入图像解耦为两个互补且分布稳定的表示：**超像素图像**（捕获低频内容）和**结构图像（深度图）**（保留高频几何边界）。

具体而言，轻量的**超像素分割网络（SSN）**首先预测像素到超像素区域的软分配概率，将视觉相似的像素分组为同质区域。对每个区域 $r$，其归一化颜色表示为：

$$C_{r}^{k-1} = \frac{1}{|r|} \sum_{i \in r} I_{i}^{k-1}$$

该公式通过对分割掩码 $P^{k-1}$ 中区域 $r$ 内的所有像素取均值，获得该区域的代表性颜色，从而构建超像素图像。这一低通滤波操作本质上移除了累积的高频伪影与随机噪声，同时保留了语义内容与边界一致性。深度图则通过预训练的深度估计模型（DepthAnything）提取，作为辅助几何约束，在后续扩散过程中引导边缘锐度与结构保真度。

### 3.2 自相似性感知精炼模块（SARM）

大尺度超分辨率通常需要将图像分块处理，各块独立重建后拼接。这导致跨 patch 的纹理一致性丧失——同一物体在相邻块中可能被重建为截然不同的纹理模式（如 Figure 2 所示）。SARM 通过显式建模并约束图像内部的**自相似性结构**来解决这一问题。

核心思想是：图像的自相似性可以通过深度特征空间中的相关性来表达。设 $e^{k}$ 为预训练 SAM 编码器从重建图像中提取的特征图，$e^{\mathrm{gt}}$ 为真值图像的特征图，则自相似性矩阵定义为：

$$R^{k} = e^{k} (e^{k})^{\top}, \quad R^{\mathrm{gt}} = e^{\mathrm{gt}} (e^{\mathrm{gt}})^{\top}$$

其中 $R^{k}$ 和 $R^{\mathrm{gt}}$ 分别编码了重建图像与真值图像内部各空间位置之间的成对语义相似性。为强制重建图像保持与真值一致的纹理相关性结构，引入**相关引导损失**：

$$L_{\mathrm{corr}} = \| R^{k} - R^{\mathrm{gt}} \|_2$$

该损失直接约束两个自相似性矩阵在 L2 范数下的一致性。在实现层面，SARM 在扩散 U-Net 的解码器端引入缓存特征的全局自注意力机制，以及 LR 全局语义特征的交叉注意力，使每个 patch 的重建过程能够感知全局上下文，从而恢复跨 patch 的纹理一致性。

### 3.3 扩散骨干网络与训练目标

CASR 采用 **SD-Turbo** 作为单步扩散骨干网络，经 LoRA 微调以执行超分辨率重建。**ControlNet 分支**接收 SSAM 输出的超像素图像与深度图作为结构控制信号，注入解码器以引导细节生成。

训练分为两阶段。第一阶段冻结 SSAM，仅训练 SR 骨干网络，优化目标为组合感知重建损失与深度一致性损失：

$$L_{\mathrm{rec}} = \lambda_1 L_2 + \lambda_2 L_{\mathrm{LPIPS}} + \lambda_3 L_{\mathrm{GAN}}$$

$$L_{\mathrm{depth}} = \| \mathrm{Norm}(d^{k}) - \mathrm{Norm}(d^{\mathrm{gt}}) \|_2$$

$$L_{\mathrm{total}_1} = L_{\mathrm{rec}} + \lambda_4 L_{\mathrm{depth}}$$

其中 $L_{\mathrm{depth}}$ 约束重建图像与真值图像的归一化深度图一致，保持几何结构。第二阶段引入 SARM，在原有损失基础上加入相关引导损失：

$$L_{\mathrm{total}_2} = L_{\mathrm{rec}} + \lambda_4 L_{\mathrm{depth}} + \lambda_5 L_{\mathrm{corr}}$$

这一渐进式训练策略确保模型先学会稳定的分布内重建，再学习跨 patch 的纹理一致性约束。

### 补充图表

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the distribution alignment process, where the input image is decomposed into a superpixel representation and a depth map. This decomposition effectively removes artifacts and noise, enabling robust SR*

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/005_Figure_5.jpg]]
*Figure 5: Illustration of the local self-similarity computation, where structurally similar regions are assigned higher correlation*



## 实验与关键发现

### 实验设置

CASR采用两阶段训练策略。第一阶段冻结结构对齐模块（SSAM），训练超分骨干网络10K次迭代，批次大小为32，学习率为$2 \times 10^{-5}$；第二阶段引入自相似性精炼模块（SARM）进行联合微调。微调阶段，VAE编码器的LoRA秩设为16，扩散U-Net的LoRA秩设为32。训练数据统一使用DF2K数据集，低分辨率图像由双三次下采样生成。测试阶段，所有对比方法均采用相同的512×512分块处理，块间重叠64像素进行拼接。评估指标涵盖参考指标LPIPS与无参考感知指标MUSIQ、NIQE、PI。

### 合成数据集上的主结果

在DIV8K合成数据集上，CASR在极大规模超分辨率（×30）下展现出显著的感知质量优势。如Table 1所示，CASR的LPIPS达到0.501，相比第二名方法**LIIF+Diff**（LIIF集成扩散后处理的增强变体）相对降低16.9%。与隐式扩散模型**IDM**（Gao et al., CVPR 2023）相比，CASR在MUSIQ上取得41.76，相对提升75.2%；NIQE降至6.98，相对降低12.3%；PI相对降低15.8%。在渐进式上采样设置（×4 × 3 × 1.5）下，CASR同样保持最优性能，验证了循环框架在分布内逐步放大的有效性。

Figure 6的视觉对比进一步印证了定量结果：在大尺度超分场景下，CASR能够重建出更逼真的雕像纹理和猫耳处的精细毛发细节，而其他方法则出现明显的模糊和伪影累积。

### 真实世界数据集上的泛化性能

在RealSR真实数据集×30尺度下，CASR展现出强大的泛化能力（Table 2）。MUSIQ达到37.84，超越IDM 34.1%；NIQE为7.81，降低6.5%；PI为6.73，降低9.5%。在×8尺度下，CASR同样取得MUSIQ 53.50、NIQE 6.81、PI 5.71的优异表现。Figure 7的视觉效果显示，CASR生成的图像更清晰、更自然，有效抑制了真实场景下的伪影累积。

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/008_Table_2.jpg]]
*Table 2: Comparison with ASISR methods on real-world datasets, with the best results in bold. Our approach archives consistently superior performance over others, showcasing strong generalization in real-world image*

### 人脸数据集上的细粒度重建

在CelebA-HQ人脸数据集×12超分任务中（Table 3），CASR的MUSIQ达到71.71，NIQE为4.77，PI为4.04，大幅领先于扩散基方法**IDM**和**Kim**（Kim and Kim, CVPR 2024）。Figure 8显示，IDM和Kim无法恢复眉毛、眼睛等细粒度面部特征，而CASR能够生成更清晰、更锐利的人脸细节，验证了自相似性精炼模块对纹理一致性的关键作用。

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/011_Table_3.jpg]]
*Table 3: Comparison with diffusion-based ASISR methods on the CelebA-HQ dataset. Our method achieves superior performance at large upsampling scales*

### 消融实验

#### 核心组件消融

Table 4系统验证了各模块的贡献。基础模型（仅含重建损失）的LPIPS为0.585，MUSIQ仅31.73。加入超像素对齐（+SuperPixel）后，LPIPS显著降至0.471，MUSIQ提升至42.23，证明SSAM有效抑制了循环过程中的累积模糊和伪影。进一步引入深度约束（+Depth）使MUSIQ提升至45.18，NIQE降至6.15，边缘清晰度明显增强（Figure 9）。完整模型（Full Model）加入SARM后，LPIPS进一步降至0.450，MUSIQ跃升至51.44，NIQE降至6.01，验证了自相似性感知精炼对跨patch纹理一致性的决定性作用。

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/013_Figure_9.jpg]]
*Figure 9: Impact of different components. Incorporating the superpixel module (Model1) effectively suppresses accumulated blur and artifacts during cascading, while depth conditioning (Model2) further enhances edge sharpness. The full model produces natural results with consistent textures across patches*

#### SARM内部机制消融

Table 5分析了SARM中全局语义上下文的作用。加入低分辨率全局语义交叉注意力后，MUSIQ额外提升2.34，NIQE降低0.29，表明全局上下文信息能够有效补充局部patch间融合，实现更连贯的重建。

#### 损失函数消融

Table 6验证了各损失项的独立贡献。相关引导损失$L_{\mathrm{corr}}$单独添加即可带来MUSIQ +0.90、NIQE -0.47的增益；同时加入深度一致性损失$L_{\mathrm{depth}}$取得最佳综合性能，证实了结构约束与纹理约束的互补性。

#### 超像素尺寸消融

Table 7和Figure 10揭示了超像素尺寸的关键权衡。4×4尺寸取得最优性能平衡；当尺寸增大至8×8时，LPIPS回升至0.516，细节被过度抹除甚至改变图像内容，说明过大的超像素会牺牲纹理保真度。

### 失败模式与局限性

尽管CASR在极大规模超分上取得突破性进展，仍存在以下局限：（1）超像素尺寸固定为4×4，缺乏内容自适应能力，过大尺寸会抹除细节（Figure 10）；（2）方法依赖预训练的深度估计模型（DepthAnything）和分割模型（SAM、SuperPixel-FCN），其性能波动可能影响最终效果；（3）两阶段训练流程增加了实施复杂度，单步扩散采样可能限制生成纹理的多样性；（4）在极端尺度（>×30）下仍存在一定的质量退化，分布漂移未被完全消除。

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/016_Figure_10.jpg]]
*Figure 10: While superpixels effectively suppress degradation artifacts, excessively large superpixel sizes remove fine details and may even alter image content*

### 补充图表

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of cyclic cascade stability across different ASISR. The SIFID measures distribution shifts between reconstructed images and the training data during cascading. Our method achieves notably higher distribution stability than others*

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/002_Figure_2.jpg]]
*Figure 2: This illustrates the texture inconsistency between patches caused by patch-based super-resolution, where identical repeated objects are reconstructed with different texture patterns*

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/006_Table_1.jpg]]
*Table 1: Comparison with ASISR methods on the DIV8K synthetic dataset, with the best results in bold. The ×4 × 3 × 1.5 column evaluates all methods under progressive upsampling*

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/012_Table_4.jpg]]
*Table 4: Ablation study of major components in CASR. Each module contributes to the overall performance improvement*

![[assets/figures/papers/paper_list_l845_https_arxiv_org_abs_2602_22159/figures/017_Table_5.jpg]]
*Table 5: Ablation on global semantic context within SARM*



## 定位与知识库关联

### 任意尺度超分辨率的方法学演进

CASR所处的任意尺度超分辨率（Arbitrary-Scale Image Super-Resolution, ASISR）领域，核心挑战在于使单一模型能够处理训练时未见过的连续放大尺度。早期方法以隐式神经表示（Implicit Neural Representation, INR）为范式，**LIIF**（Chen et al., CVPR 2021）通过局部隐函数将图像坐标映射为RGB值，实现了连续尺度的查询能力。在此基础上，**CiaoSR**（Cao et al., CVPR 2023）引入连续隐式注意力机制，进一步提升了高频细节的重建质量。

然而，INR类方法在训练尺度外存在严重的性能退化。为缓解这一问题，基于归一化流的方法被引入ASISR。**LINF**（Yao et al., CVPR 2023）利用归一化流的可逆变换建模LR到HR的条件分布；**BFSR**（Tsao et al., CVPR 2024）则通过流程增强策略改进了流基方法的稳定性。与此同时，扩散模型凭借其强大的生成先验成为另一条技术路线。**IDM**（Gao et al., CVPR 2023）将隐式扩散模型应用于ASISR，**Kim**（Kim and Kim, CVPR 2024）则进一步结合扩散模型与隐式神经解码器。此外，部分工作尝试将扩散后处理模块集成到INR方法中，形成**LIIF+Diff**和**CiaoSR+Diff**等增强变体。

上述方法虽然在不同维度上推进了ASISR的性能边界，但共享一个根本性局限：它们均采用单步直接预测的策略，将任意尺度的超分辨率视为一次性的映射问题。这种范式在训练尺度附近表现尚可，但当目标尺度远超训练分布时，输入特征与模型参数之间产生严重的分布偏移（distribution shift），导致模糊、细节丢失和伪影累积。

### CASR的范式突破：循环分布感知

CASR的核心范式创新在于将超大尺度超分重新定义为**一系列分布内尺度转换的循环过程**。具体而言，CASR将总放大倍数 $s$ 分解为子尺度乘积 $s = s^1 \times s^2 \times \cdots \times s^K$，每步缩放因子 $s^k \leq s_{\max}$，确保每一步的输入-输出映射都落在训练分布范围内。这种“单模型循环逐步放大”策略，从根本上规避了跨尺度分布偏移问题，与所有基线方法的单步预测范式形成鲜明对比。

为支撑这一循环框架，CASR引入了两个关键机制：

**超像素结构对齐模块（SSAM）** 负责在每一步循环迭代前稳定输入分布。它将当前中间结果分解为超像素图像（低通表示）和深度图（结构约束），通过超像素区域归一化 $C_{r}^{k-1} = \frac{1}{|r|} \sum_{i \in r} I_{i}^{k-1}$ 滤除累积的级联噪声，同时保留几何结构完整性。这一设计使得后续SR骨干网络始终接收分布稳定的输入，有效抑制了循环过程中的误差传播。

**自相似性感知精炼模块（SARM）** 解决了分块超分辨率导致的跨patch纹理不一致问题。现有方法通常对各图像块独立处理，仅依赖重叠区域进行简单拼接，导致相同纹理在不同patch中被重建为不同模式。SARM通过缓存特征的全局自注意力、LR全局语义交叉注意力，以及相关引导损失 $L_{\mathrm{corr}} = \| R^{k} - R^{\mathrm{gt}} \|_2$（其中 $R^{k} = e^{k} (e^{k})^{\top}$ 为重建图像的自相似性矩阵），在特征空间层面约束跨patch的纹理一致性。

### 知识库定位与适用边界

从方法论谱系来看，CASR位于**循环分布感知ASISR**这一新兴节点。它首次将分布稳定性作为超大尺度超分的核心设计目标，通过超像素分解与自相似性约束两个互补机制，在循环框架内实现了分布内推理。与依赖单一强大生成先验的扩散方法（IDM, Kim）不同，CASR的优势在于**理解并调节表征在尺度间的演化**，而非单纯依赖模型或数据规模的提升。

**适用场景**方面，CASR在以下条件下表现突出：
- 超大放大倍数（×12至×30），远超常规ASISR方法的有效范围；
- 真实世界低质量输入，需要抑制累积伪影的场景；
- 包含重复纹理结构的图像（如建筑、织物），受益于自相似性约束。

**适用边界与局限**：
1. **超像素尺寸固定**：当前超像素尺寸固定为4×4，无法根据图像内容自适应调整。消融实验表明，过大的尺寸（如8×8）会抹除细节，导致LPIPS从0.450回升至0.516。这一固有限制意味着在纹理复杂度差异较大的图像上，CASR存在一定的性能折衷。
2. **外部模型依赖**：方法依赖预训练的深度估计（DepthAnything）和分割模型（SAM, SuperPixel-FCN），其性能和泛化能力直接影响SSAM的分解质量。在分布外场景（如特殊成像模态）下，这些预训练组件的退化可能传导至最终重建结果。
3. **训练复杂度**：两阶段训练流程增加了实施复杂度，且仅使用单步扩散采样可能限制生成纹理的多样性。
4. **极端尺度退化**：在×30以上的极端尺度下，分布漂移未被完全消除，仍存在一定的质量退化。

### 开放问题

1. **内容感知的自适应超像素**：如何实现超像素尺寸的动态调整，使其能够根据局部纹理复杂度进行内容感知的结构对齐？这需要设计可微分的超像素粒度选择机制，或引入多尺度超像素融合策略。
2. **跨任务推广**：循环分布感知框架的核心思想——将大跨度映射分解为分布内步骤——是否可推广到视频超分（时序分布偏移）、三维内容重建（体素尺度偏移）及跨模态生成（模态分布偏移）等任务？这需要重新定义相应模态下的“分布内”约束和结构对齐机制。
3. **与强生成先验的深度融合**：当前CASR使用SD-Turbo作为骨干网络，但分布对齐模块与扩散过程的交互仍较为浅层。如何设计端到端的联合优化策略，使分布约束直接参与扩散去噪过程的引导，可能进一步提升极端尺度下的生成质量。



## 原文 PDF

![[paperPDFs/CVPR_2026/CASR_A_Robust_Cyclic_Framework_for_Arbitrary_Large_Scale_Super_Resolution_with_Distribution_Alignment_and_Self_Similarity_Awareness.pdf]]

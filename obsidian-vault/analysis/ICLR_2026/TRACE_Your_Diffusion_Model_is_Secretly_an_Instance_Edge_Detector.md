---
title: "TRACE: Your Diffusion Model is Secretly an Instance Edge Detector"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TRACE_Your_Diffusion_Model_is_Secretly_an_Instance_Edge_Detector.pdf
project_link: https://shjo-april.github.io/TRACE/
code_link: null
openreview_forum_id: BjElYlJKMj
aliases:
- TRACE
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "扩散模型自注意力在去噪早期隐式编码实例边界，通过时序KL散度峰值精确定位实例涌现点（IEP），并利用注意力边界散度（ABDiv）将像素间自注意力差异直接转化为实例边缘；再通过单步自蒸馏与背景引导传播（BGP）将边缘无缝融入分割，实现无标注的实例级分离。"
primary_logic: "文本到图像扩散模型的自注意力图在去噪过程中会短暂地从语义结构过渡到实例结构，该过渡点可由连续自注意力图间的KL散度峰值标记（IEP）；在该点，像素的跨邻域自注意力分布差异在真实实例边界处达到最大，从而构成无需任何标注的高质量实例边缘信号。"
claims:
- "IEP通过最大化连续自注意力图间的KL散度定位实例结构最清晰的去噪步，该峰值在不同扩散模型中分布一致。"
- "ABDiv利用4邻域像素的自注意力KL散度生成边界图，无需聚类或标注即可获得高精度伪边缘。"
- "单步自蒸馏将逐图IEP+ABDiv替换为一次前向，推理速度提升81倍（从3682ms降至45ms），同时边缘连通性更强。"
- "TRACE在COCO上提升无监督实例分割AP达+5.1点，仅依赖图像级标签即可超越点监督全景分割基线。"
---

# TRACE: Your Diffusion Model is Secretly an Instance Edge Detector

> [!tip] 核心洞察
> 文本到图像扩散模型的自注意力图在去噪过程中会短暂地从语义结构过渡到实例结构，该过渡点可由连续自注意力图间的KL散度峰值标记（IEP）；在该点，像素的跨邻域自注意力分布差异在真实实例边界处达到最大，从而构成无需任何标注的高质量实例边缘信号。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TRACE：扩散模型秘密地是一个实例边缘检测器 |
| 英文题名 | TRACE: Your Diffusion Model is Secretly an Instance Edge Detector |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=BjElYlJKMj) · [Project](https://shjo-april.github.io/TRACE/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | TRACE |
| Dataset | COCO 2014 val (UIS), VOC 2012 val (WPS), COCO 2014 val (Edge Quality), COCO 2014 (Inference Speed) |

> [!tip] 效果简介
> - COCO 2014 val (UIS) 上，AP^mk 为 8.2 (ProMerge + TRACE)，对比 3.1 (ProMerge)，变化 +5.1。
> - VOC 2012 val (WPS) 上，PQ 为 56.9 (DHR + TRACE, ResNet-50)，对比 45.0 (DHR, tag-only, ResNet-50)，变化 +11.9。
> - COCO 2014 val (Edge Quality) 上，ODS 为 0.889 (TRACE)，对比 0.428 (DiffusionEdge)，变化 +0.461。

## 概要

密集实例分割的标注成本极高，而现有的无监督与弱监督方法依赖语义聚类或深度先验，难以可靠分离同类相邻实例，常导致合并或碎片化。TRACE 的核心发现是：**文本到图像扩散模型的自注意力图在去噪早期会短暂地从语义结构过渡到实例结构**，该过渡点可由连续自注意力图间的 KL 散度峰值精确定位，称为实例涌现点（Instance Emergence Point, IEP）。在 IEP 时刻，像素的跨邻域自注意力分布差异在真实实例边界处达到最大，构成无需任何标注的高质量实例边缘信号。

基于此洞察，TRACE 提出了一套完整的无标注实例边缘提取与利用流水线：首先通过 IEP 定位最优去噪步，再利用注意力边界散度（Attention Boundary Divergence, ABDiv）将像素间自注意力差异直接转化为伪边缘图；随后通过单步自蒸馏训练轻量边缘解码器，将逐图搜索替换为一次前向；最后以背景引导传播（Background-Guided Propagation, BGP）将边缘作为边界势垒融入现有分割流程，实现相邻实例分离与碎片修复。

**核心结果**：TRACE 在 COCO 无监督实例分割上将 AP 提升 +5.1 点；仅依赖图像级标签即可超越点监督全景分割基线（VOC PQ +11.9）；边缘质量大幅领先传统检测器（ODS 0.889 vs. 0.428）；推理速度提升 81 倍（从 3682ms 降至 45ms）。

**方法定位**：TRACE 属于扩散模型内部表征挖掘范式，与基于 DINO 特征的聚类方法（如 **MaskCut**, Wang et al., 2023a）和深度先验方法正交，可作为即插即用的边缘先验模块与现有无监督/弱监督分割流程协同工作。

实例分割是计算机视觉的核心任务，要求模型同时定位、分类并逐像素分离图像中的每个对象。主流的全监督方法依赖密集的像素级掩码标注，但此类标注成本极高——以COCO数据集为例，单张图像平均包含7.7个实例，标注员需精确勾勒每个对象的轮廓，耗时远超边界框标注。这一瓶颈严重制约了实例分割模型向长尾类别、新领域和高分辨率场景的扩展。

为降低标注依赖，研究者先后探索了无监督实例分割（UIS）和弱监督全景分割（WPS）两条路径。UIS方法试图在无任何人工标注的条件下发现并分离实例，其代表性工作包括基于DINO自监督特征的谱聚类方法**MaskCut**（Wang et al., 2023a）及其后处理增强版本**ProMerge**（Li & Shin, 2024）。WPS方法则利用图像级标签（如类别标签）训练分割模型，代表方法包括**DHR**（Jo et al., 2024a）等。然而，这两类方法面临一个共同的深层瓶颈：

**语义聚类与深度先验难以可靠分离同类相邻实例。**

现有UIS方法的核心机制是语义特征聚类——它们假设同一实例的像素在特征空间中彼此靠近，不同实例则彼此远离。但这一假设在同类相邻对象（如并排停放的汽车、重叠的行人）面前系统性失效：语义特征在这些区域高度相似，聚类算法无法区分实例边界，导致相邻实例被错误合并为单一掩码，或同一实例被过度分割为多个碎片。深度先验（如单目深度估计）虽能提供一定的几何分离线索，但其精度受限于深度估计模型本身的质量，且对扁平场景和远距离目标几乎无效。实验表明，当前最优UIS方法ProMerge在COCO上的AP^mk仅为3.1，远未达到实用水平。

WPS方法同样受困于此。点监督全景分割方法**Point2Mask**（Li et al., 2023b）和**EPLD**（Li et al., 2024）虽能利用少量点击标注，但点击本身即引入了人工成本，且无法覆盖所有实例边界。DHR等仅用图像级标签的方法在生成伪掩码时，同样因缺乏边界先验而产生合并或碎片化问题。

**本文的核心洞察是：扩散模型的自注意力图在去噪过程中会短暂地从语义结构过渡到实例结构，这一过渡点可由连续自注意力图间的KL散度峰值精确标记；在该点，像素的跨邻域自注意力分布差异在真实实例边界处达到最大，从而构成无需任何标注的高质量实例边缘信号。**

这一洞察源于对文本到图像扩散模型内部表示的深入观察。如图1所示，扩散模型在去噪早期，其交叉注意力层保持语义级别的响应（如“狗”的区域整体激活），但自注意力层在特定去噪步会突然呈现出锐利的实例级结构——同一对象的像素彼此高度关注，而不同对象的像素间注意力显著减弱。这种从“语义团块”到“实例结构”的涌现过程是扩散模型独有的特性：非扩散模型（如DINO、CLIP）的自注意力仅形成语义团块，无法揭示实例边界（见图8、表5）。

基于此，TRACE方法无需任何实例级标注，直接从预训练扩散模型的自注意力图中提取实例边缘，并将其作为边界先验注入现有的UIS和WPS流程，从而从根本上解决相邻同类实例的分离难题。

## 核心方法与创新机理

TRACE 的核心创新在于将文本到图像扩散模型的自注意力图重新定位为一种**零标注的实例边缘信号源**，从而绕开了现有无监督与弱监督实例分割方法对语义聚类或深度先验的根本依赖。这一范式转换由三个紧密耦合的 changed slots 构成，分别覆盖信号来源、推理效率与边缘-分割集成方式。

### 创新一：从扩散自注意力中直接提取实例边缘（信号来源的范式转换）

现有无监督实例分割方法——如基于 DINO 特征的 **MaskCut**（Wang et al., 2023a）及其后处理增强 **ProMerge**（Li & Shin, 2024）——依赖语义聚类将像素分组为实例，但这类方法在同类相邻对象上极易发生合并或碎片化，因为语义特征缺乏实例级的区分度。深度先验虽能提供几何线索，却受限于单目深度估计的精度瓶颈。TRACE 彻底改变了这一格局：它发现扩散模型在去噪早期会短暂地从语义结构过渡到实例结构，并设计了两项机制将这一瞬态信号转化为高质量边缘。

- **Instance Emergence Point（IEP）**：通过最大化连续自注意力图间的 KL 散度 $t^{\star} = \operatorname*{argmax}_{t} D_{\mathrm{KL}}(SA(X_{t_{\mathrm{prev}}}) \parallel SA(X_t))$，精确定位实例结构最清晰的去噪步。消融实验证实，若跳过 IEP 直接在固定语义步应用 ABDiv，APmk 仅从 3.1 提升至 3.2，几乎无增益；而 IEP 定位后 ABDiv 将 APmk 推至 4.8（Table 3），证明时序定位是不可或缺的因果杠杆。

- **Attention Boundary Divergence（ABDiv）**：在 IEP 时刻的自注意力图上，计算 4 邻域像素间自注意力分布的 KL 散度 $\mathrm{ABDiv}(SA)_{i,j} := D_{\mathrm{KL}}(SA_{i+1,j} \parallel SA_{i-1,j}) + D_{\mathrm{KL}}(SA_{i,j+1} \parallel SA_{i,j-1})$。其物理直觉清晰：边界两侧像素关注不同实例区域，自注意力分布差异大；实例内部像素关注相似区域，差异小（Figure 5）。这一非参数操作无需任何聚类或标注，直接生成伪边缘图。

- **扩散先验的独特性**：对比实验表明，非扩散骨干（如 DINOv2、Qwen2.5-VL）的自注意力仅形成语义团块，无法揭示实例边界；而扩散骨干（SD2.1、FLUX.1）在 IEP 时刻呈现锐利的实例边界（Figure 8, Table 5），证明这一能力是扩散生成过程的内在属性，而非通用注意力机制所共有。

### 创新二：单步自蒸馏实现 81 倍推理加速（推理流程的架构重构）

IEP+ABDiv 的原始流程需对每张图像执行扩散前向以搜索 IEP 并计算 ABDiv，推理延迟高达 3682 ms/图，无法实用。TRACE 通过**单步自蒸馏**将这一昂贵流程压缩为一次前向：

- 以 IEP+ABDiv 生成的伪边缘作为教师监督信号，联合微调扩散骨干（LoRA）与轻量边缘解码器 $G_\phi$，训练目标为 $\mathcal{L}(\theta, \phi) = \|I - \hat{I}\|^2 + \operatorname{DiceLoss}(E, \hat{E})$。其中重建损失锚定全局结构，Dice 损失驱动边缘预测。
- 蒸馏后推理仅需 45 ms/图（81 倍加速，Table 3），且边缘连通性反而增强——自蒸馏闭合了伪边缘中的断裂（Figure 4 绿圈标注），APmk 从 4.8 进一步提升至 8.2。

这一 changed slot 的关键在于：TRACE 将扩散模型的瞬态实例知识永久固化为可单步调用的边缘解码器，使扩散先验从“推理时在线提取”变为“训练时一次性蒸馏”，彻底解耦了边缘生成与扩散采样过程。

### 创新三：背景引导传播（BGP）将边缘无缝融入分割（边缘-分割集成方式）

现有方法不提供显式实例边界先验，语义亲和力传播难以可靠分离相邻实例。TRACE 设计了**背景引导传播（BGP）**（Figure 6），将 TRACE 边缘作为不可逾越的边界势垒：

- 以原始掩码为种子，在 TRACE 边缘约束下通过随机游走传播 $\operatorname{vec}(M_c^*) = T^t \cdot \operatorname{vec}(M_c \odot (1 - \hat{E}))$，修复碎片化区域。
- 迭代合并重叠掩码（IoU > 0.5），利用边缘信息精确裁决合并决策，避免相邻实例错误融合。

这一集成方式使 TRACE 可作为即插即用的边界增强模块，叠加于现有 UIS 基线（ProMerge + TRACE 在 COCO 上 APmk 达 8.2，较 ProMerge 的 3.1 提升 +5.1）或弱监督分割流程（DHR + TRACE 在 VOC 2012 上 PQ 达 56.9，仅用图像级标签即超越点监督基线 **Point2Mask** 和 **EPLD**，Table 2）。

### 创新间的因果链条

三个 changed slots 形成递进依赖：IEP 定位实例涌现时刻 → ABDiv 在该时刻提取边界 → 自蒸馏将边界提取能力压缩为单步推理 → BGP 将边界作为约束传播掩码。消融实验严格验证了这一链条：单独 ABDiv 无效（APmk 3.2），IEP+ABDiv 有效（APmk 4.8），蒸馏后最优（APmk 8.2），且轻量 CNN 解码器（0.1MB）与重型 Mask2Former 解码器（258MB）性能几乎相同（APmk 8.2 vs 8.4，Table 9），证明核心增益来自扩散边缘信号本身而非解码器容量。

TRACE 的整体流水线由四个核心模块串联构成：**实例涌现点定位（IEP）** → **注意力边界散度（ABDiv）** → **单步自蒸馏边缘解码器** → **背景引导传播（BGP）**。其设计哲学是将扩散模型去噪过程中短暂出现的实例结构信号，转化为可单步推理的高质量实例边缘，并以此作为边界约束融入现有分割流程。

### 流水线总览

**阶段一：扩散前向与伪边缘生成（图4a）**

给定输入图像 $X_0$，TRACE 首先通过预训练文本到图像扩散模型执行部分去噪前向。在选定的离散去噪步 $\{\tau_1, \dots, \tau_N\}$ 上提取所有自注意力块的自注意力图，经上采样至最大空间分辨率后取均值，得到聚合自注意力图 $SA(X_t)$。

IEP 模块通过最大化连续步间自注意力图的 KL 散度，定位实例结构最清晰的去噪步 $t^\star$：

$$t^{\star} = \operatorname*{argmax}_{t \in \{\tau_1, \dots, \tau_N\}} D_{\mathrm{KL}}(SA(X_{t_{\mathrm{prev}}}) \parallel SA(X_t))$$

在 $t^\star$ 时刻的自注意力图 $SA(X_{t^\star})$ 上，ABDiv 模块计算 4 邻域像素间自注意力分布的 KL 散度之和，生成非参数伪边缘图 $E$：

$$\mathrm{ABDiv}(SA)_{i,j} := D_{\mathrm{KL}}\big(SA_{i+1,j} \parallel SA_{i-1,j}\big) + D_{\mathrm{KL}}\big(SA_{i,j+1} \parallel SA_{i,j-1}\big)$$

这一阶段完全无需任何标注，仅依赖扩散模型内部的自注意力信号。

**阶段二：单步自蒸馏（图4b）**

阶段一虽能生成高质量伪边缘，但每张图需执行完整扩散前向并逐步提取自注意力，推理延迟高达 3682 ms/图。TRACE 通过单步自蒸馏将这一过程压缩为一次前向：以 $t=0$ 时刻的噪声图像作为输入，使用 LoRA 微调扩散骨干，并联合训练一个轻量边缘解码器 $G_\phi$。监督信号来自阶段一生成的伪边缘图 $E$，同时引入重建损失以稳定训练并提升边缘连通性。为抑制伪标签噪声，采用基于均值 $\mu$ 和标准差 $\sigma$ 的可靠性阈值策略，将 ABDiv 分数高于 $\mu+\sigma$ 的像素标记为边缘（1），低于 $\mu-\sigma$ 的标记为内部（0），中间区间标记为不确定（-1），在损失计算中排除。

蒸馏完成后，推理时边缘解码器直接从单步前向输出预测边缘 $\hat{E}$，延迟降至 45 ms/图（约 81 倍加速），且蒸馏后的边缘连通性优于原始 ABDiv 伪边缘（图4 绿色圆圈所示）。

**阶段三：背景引导传播（BGP，图6）**

将 TRACE 预测的边缘 $\hat{E}$ 作为不可逾越的边界势垒，BGP 以随机游走方式传播现有分割方法产生的碎片化掩码。传播在实例边界内部进行，闭合断裂区域；随后对重叠掩码以 IoU 阈值 $\tau_{\mathrm{BGP}} = 0.5$ 迭代合并直至收敛，最终输出完整的实例掩码。

### 模块间关系

IEP 为 ABDiv 提供时间定位——若在固定语义步（无 IEP）直接应用 ABDiv，AP$^\text{mk}$ 几乎无提升（3.2 vs 基线 3.1）；IEP 定位后 ABDiv 将 AP$^\text{mk}$ 提升至 4.8。单步自蒸馏将 IEP+ABDiv 的昂贵计算压缩为轻量推理，同时通过端到端训练闭合伪边缘的断裂，使 AP$^\text{mk}$ 进一步提升至 8.2。BGP 作为边缘与分割的桥接模块，将 TRACE 边缘无缝融入现有无监督或弱监督分割流程，无需修改上游方法本身。

TRACE 的核心方法由四个模块级联构成：**实例涌现点定位（IEP）**、**注意力边界散度（ABDiv）**、**单步自蒸馏边缘解码器**以及**背景引导传播（BGP）**。前两个模块从扩散模型的自注意力图中提取无参数的伪边缘，第三个模块将这一昂贵过程压缩为单次前向，第四个模块则将边缘约束融入分割掩码的修复与分离。

### 3.1 实例涌现点定位（IEP）

扩散模型在去噪过程中，自注意力图会经历从语义结构到实例结构的转变。IEP 的目标是精确找到实例边界最清晰的那个去噪步 $t^\star$。

给定一系列候选去噪步 $\{\tau_1, \dots, \tau_N\}$，IEP 选择使连续自注意力图间 KL 散度最大的步：

$$t^{\star} = \operatorname*{argmax}_{t \in \{\tau_1, \dots, \tau_N\}} D_{\mathrm{KL}}(SA(X_{t_{\mathrm{prev}}}) \parallel SA(X_t))$$

其中 $SA(X_t)$ 表示在去噪步 $t$ 处聚合后的自注意力图，$t_{\mathrm{prev}}$ 为上一个被采样的步。该公式的直觉是：当自注意力结构发生剧烈重组——即从语义团块转向实例边界——时，相邻步之间的分布差异达到峰值。实验表明，该峰值在不同扩散模型中分布一致（Fig. 7），且 KL 散度在精度与效率之间取得最优平衡（Tab. 4）。

### 3.2 注意力边界散度（ABDiv）

在 IEP 定位的 $t^\star$ 时刻，自注意力图 $SA(X_{t^\star})$ 呈现出清晰的实例边界特征：边界像素的注意力分布与其邻域像素显著不同，而实例内部像素的分布则保持稳定。ABDiv 利用这一性质，通过计算 4 邻域像素间自注意力分布的 KL 散度来生成边界分数：

$$\mathrm{ABDiv}(SA)_{i,j} := D_{\mathrm{KL}}\big(SA_{i+1,j} \parallel SA_{i-1,j}\big) + D_{\mathrm{KL}}\big(SA_{i,j+1} \parallel SA_{i,j-1}\big)$$

该公式对像素 $(i,j)$ 的上下邻域和左右邻域分别计算 KL 散度并求和。在真实实例边界处，对侧邻域的自注意力分布差异大，ABDiv 值高；在实例内部，分布趋于一致，ABDiv 值低（Fig. 5）。ABDiv 完全无参数、无需聚类或标注，直接输出像素级边界分数图。

### 3.3 单步自蒸馏边缘解码器

IEP+ABDiv 需对每张图像进行完整扩散前向并提取自注意力，推理延迟高达 3682 ms/图。单步自蒸馏将此过程压缩为一次前向：以 IEP+ABDiv 生成的伪边缘 $E$ 为监督信号，联合微调扩散骨干（通过 LoRA）并训练一个轻量边缘解码器 $G_\phi$。

训练损失由两部分组成：

$$\mathcal{L}(\theta, \phi) = \|I - \hat{I}\|^2 + \operatorname{DiceLoss}(E, \hat{E})$$

其中 $\|I - \hat{I}\|^2$ 为图像重建损失，$\hat{I}$ 为解码器重建的图像，用于稳定训练并保持全局结构；$\operatorname{DiceLoss}(E, \hat{E})$ 为边缘损失，采用不确定性掩码——将 ABDiv 分数在均值 $\pm$ 标准差之间的像素标记为不确定（$-1$），排除在损失计算之外，以抑制伪标签噪声。推理时仅需 $t=0$ 时刻的单次前向，延迟降至 45 ms，提速 81 倍（Tab. 3），且蒸馏后的边缘连通性更强。

### 3.4 背景引导传播（BGP）

现有无监督实例分割方法生成的掩码常存在碎片化和相邻实例合并问题。BGP 以 TRACE 预测的边缘 $\hat{E}$ 为边界势垒，通过随机游走将原始掩码在实例边界内传播：

$$\operatorname{vec}(M_c^*) = T^t \cdot \operatorname{vec}(M_c \odot (1 - \hat{E}))$$

其中 $M_c$ 为原始碎片掩码，$T$ 为在边缘约束下的转移矩阵，传播 $t$ 步后得到修复的掩码 $M_c^*$。传播完成后，对重叠区域按 IoU 阈值 $\tau_{\mathrm{BGP}} = 0.5$ 进行迭代合并，直至收敛。BGP 同时解决了碎片重连与相邻实例分离两个问题（Fig. 6）。

## 实验与关键发现

### 核心瓶颈的验证

TRACE 的设计围绕一个核心瓶颈展开：现有无监督与弱监督方法难以可靠分离同类相邻实例，而密集标注成本极高。实验从三个层面验证了这一瓶颈的突破：实例边缘质量、无监督实例分割增益、以及弱监督全景分割的跨范式提升。

**实例边缘质量。** 在 COCO 2014 验证集上，TRACE 生成的实例边缘在 ODS（最优数据集尺度 F-measure）上达到 0.889，超过最强传统边缘检测基线 DiffusionEdge（0.428）两倍以上（Table 6）。同时，衡量拓扑连通性的 clDice 达到 0.826，表明 TRACE 边缘在闭合轮廓方面具有显著优势。这一结果直接支持了核心洞察：扩散自注意力在 IEP 时刻编码的实例边界信号，远优于传统边缘检测器所能提取的结构。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_BjElYlJKMj/figures/027_Table_6.jpg]]
*Table 6: Instance Edge Quality. Evaluation on COCO 2014 validation set against ground-truth instance boundaries*

**无监督实例分割。** 在 COCO 2014 上，将 TRACE 附加到 ProMerge（Li & Shin, 2024）基线后，AP^mk 从 3.1 提升至 8.2，增益 +5.1 点（Table 1）。这一增益在不同 UIS 基线上一致复现：附加到 MaskCut（Wang et al., 2023a）时 AP^mk 提升 +5.3 点。更重要的是，TRACE 的边缘增强使标签监督方法 DHR（Jo et al., 2024a）仅凭图像级标签即达到 56.9 PQ，超越了点监督方法 Point2Mask（Li et al., 2023b）和 EPLD（Li et al., 2024）在 VOC 2012 上的表现（Table 2）。这验证了因果操纵变量：扩散自注意力提供的实例边缘信号，可以替代人工标注的边界先验。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_BjElYlJKMj/figures/013_Table_1.jpg]]
*Table 1: Performance of unsupervised instance segmentation*

### 关键组件消融

Table 3 的逐组件消融揭示了各模块的独立贡献与交互机制：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_BjElYlJKMj/figures/016_Table_3.jpg]]
*Table 3: Effect of key components on COCO 2014 with the UIS baseline (Li & Shin, 2024)*

- **仅用 ABDiv 而无 IEP（固定语义步）：** AP^mk 仅从 3.1 提升至 3.2，几乎无增益。这证明扩散自注意力中的实例结构并非始终存在，而是仅在特定去噪步涌现——IEP 的定位作用是必要条件。
- **IEP + ABDiv（无蒸馏）：** AP^mk 跃升至 4.8，但推理延迟高达 3682 ms/图，因为每张图需完整扩散前向并逐步计算自注意力。
- **IEP + ABDiv + 单步自蒸馏：** AP^mk 进一步提升至 8.2，同时推理延迟降至 45 ms/图（81 倍加速）。蒸馏不仅消除了推理时的 IEP/ABDiv 计算，还通过端到端训练闭合了伪边缘中的断裂（Figure 4 绿色圆圈所示），使边缘连通性更强。

**相似性度量的选择。** Table 4 对比了 IEP 和 ABDiv 中使用的分布差异度量。KL 散度在 AP^mk 与延迟之间取得最优平衡（AP^mk 9.4，延迟 3082 ms）。JSD 精度相同但延迟高出 60% 以上；MSE 和 MAE 则导致 AP^mk 大幅下降。这一结果与公式设计一致：KL 散度对分布尾部差异敏感，适合捕捉边界处自注意力分布的突变。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_BjElYlJKMj/figures/020_Table_4.jpg]]
*Table 4: Similarity metrics for IEP and ABDiv*

**不确定性掩码的作用。** Table 10 显示，使用均值 ± 标准差作为阈值将 ABDiv 分数三值化（边缘/内部/不确定），将边缘 ODS-Precision 从 0.572 提升至 0.852。排除不确定像素的训练策略有效抑制了伪标签噪声，使蒸馏后的边缘解码器学到了更干净的边界表示。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_BjElYlJKMj/figures/033_Table_10.jpg]]
*Table 10: Ablation on pseudo-labeling schemes for ABDiv (Sec. 3.3). ODS-Precision and ODS-Recall denote the precision and recall at the optimal dataset scale (ODS) for instance edges, from which the ODS (F-measure) is computed*

**边缘解码器容量。** Table 9 表明，轻量 CNN 边缘解码器（0.1 MB）与重型 Mask2Former 解码器（258 MB）在 AP^mk 上几乎持平（8.2 vs 8.4）。这说明 TRACE 的边缘信号本身质量足够高，不需要复杂解码器架构来弥补信号缺陷。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_BjElYlJKMj/figures/032_Table_9.jpg]]
*Table 9: Effect of edge decoder capacity. We replace our lightweight CNN edge decoder in TRACE with heavier alternatives and evaluate performance of unsupervised instance segmentation on COCO 2014*

**重建损失的辅助作用。** 在自蒸馏中联合优化图像重建损失，使 AP^mk 从 8.9 升至 9.4，SSIM 从 0.71 升至 0.83。重建损失为解码器提供了全局结构锚点，稳定了训练过程并防止边缘预测退化。

### 扩散先验的独特性验证

Table 5 对比了扩散与非扩散骨干的 TRACE 微调结果。扩散骨干（如 FLUX.1、SD3.5）在 COCO 2014 上 AP^mk 达到 8.3，而非扩散骨干（如 Qwen2.5-VL）仅 4.1。Figure 8 进一步可视化了两类模型的自注意力图：扩散模型在 IEP 时刻呈现锐利的实例边界，而非扩散模型的自注意力仅形成语义团块，无法区分相邻同类实例。这强有力地证明了扩散生成先验的独特性——去噪过程中的时序自注意力轨迹是实例边界信号的根本来源。

### 失败模式与局限性

TRACE 在两个场景下表现出系统性退化：

- **微小目标密集场景（卫星图像）：** 在 HRSID 和 iSAID 数据集上，TRACE 附加到 UIS 基线后 AP 分别下降 5.1 和 5.4 点（Table 14）。根因在于 VAE 的 16 倍空间下采样导致潜在空间丢失精细结构，使紧邻小目标的边界无法可靠分离。
- **分布外领域（医学影像）：** 在 MoNuSeg 细胞核分割上，TRACE 预测的边缘不完整且错误定位细胞边界，PQ 下降 0.097。文本到图像的扩散先验在医学影像领域失效，因为自然图像与医学图像的分布差异巨大。

这些失败模式指向两个开放问题：如何突破 VAE 潜在空间分辨率限制以处理微小目标，以及如何将扩散先验迁移至专业领域。

### 计算开销

Table 7 显示，TRACE 引入的额外计算开销极小：在 ProMerge 基线的基础上，延迟仅增加约 2%。这是因为推理时仅需一次前向通过轻量边缘解码器，无需扩散迭代或自注意力提取。

## 定位与知识库关联

### 无监督实例分割中的边界先验演进

TRACE 在无监督实例分割（UIS）领域的核心贡献在于**首次将扩散模型自注意力显式转化为实例边缘先验**，从而绕过了现有方法对语义聚类或深度先验的依赖。此前的 UIS 方法大致可分为两类：

- **基于语义特征聚类的方法**，如 **MaskCut**（Wang et al., 2023a），利用 DINO 自监督特征进行归一化切割，但难以可靠分离同类相邻实例，易产生合并或碎片化。
- **基于后处理优化的方法**，如 **ProMerge**（Li & Shin, 2024），通过特征合并策略改进初始掩码，但本质上仍受限于底层语义表征的实例区分能力。

TRACE 的方法论突破在于**改变了实例边缘信息的来源**：不再从语义特征空间中间接推断，而是直接从扩散模型去噪过程中的自注意力图提取。这一转变的因果机制是：扩散模型在去噪早期存在一个短暂的“语义→实例”结构过渡窗口，该窗口可通过连续自注意力图间的 KL 散度峰值精确定位（IEP）。在此窗口内，像素的跨邻域自注意力分布差异在真实实例边界处达到最大，构成高质量的非参数边缘信号（ABDiv）。消融实验（Table 3）证实，仅用 ABDiv 在固定语义步（无 IEP）几乎无提升（AP^mk 3.2），IEP 定位后 ABDiv 将 AP^mk 提升至 4.8，蒸馏进一步达到 8.2，验证了 IEP 定位的关键性。

### 弱监督全景分割中的边界增强

在弱监督全景分割（WPS）领域，TRACE 展示了**边界先验对伪掩码质量的提升可超越监督信号级别的差异**。与点监督方法 **Point2Mask**（Li et al., 2023b）和 **EPLD**（Li et al., 2024）相比，TRACE 仅依赖图像级标签（通过 **DHR**（Jo et al., 2024a）生成语义伪掩码），却在 VOC 2012 上达到 56.9 PQ，超越点监督基线（Table 2）。这表明精确的实例边界先验可以部分弥补监督信号的稀疏性，因为边界信息直接解决了相邻实例分离这一核心难点。

### 扩散先验的独特性与适用边界

TRACE 的有效性**严格依赖于扩散模型特有的时序自注意力轨迹**。Table 5 的对比实验揭示了这一边界条件：扩散骨干（如 FLUX.1, AP^mk 8.3）显著优于非扩散骨干（如 Qwen2.5-VL, AP^mk 4.1），因为后者缺乏去噪过程中的语义→实例结构过渡，其自注意力仅形成语义团块而无法揭示实例边界（Fig. 8）。这一发现将 TRACE 的知识贡献定位于**扩散生成先验的实例感知特性**，而非通用的注意力边界提取方法。

### 已知局限与失效模式

TRACE 在两个关键场景中存在系统性失效：

1. **微小目标密集场景**：卫星图像（HRSID -5.1 AP, iSAID -5.4 AP）中，VAE 的 16 倍空间下采样导致潜在空间丢失精细结构，TRACE 边缘无法可靠分离紧邻小目标。这是扩散模型架构层面的固有限制。

2. **分布外专业领域**：医学影像（如 MoNuSeg PQ -0.097）中，文本到图像扩散模型的自然图像先验失效，TRACE 预测的边缘不完整且错误定位细胞边界。这表明当前方法无法直接迁移至与预训练分布差异巨大的领域。

此外，训练阶段仍需完整扩散前向以提取 IEP+ABDiv 伪标签，虽然蒸馏后推理极快（45ms），但训练成本仍较高。

### 开放问题与未来方向

TRACE 打开了若干值得探索的方向：

- **分辨率限制突破**：如何绕过 VAE 潜在空间的下采样瓶颈，使扩散模型在微小目标场景下仍能提供清晰实例边界？可能的路径包括级联高分辨率特征或定制轻量扩散骨干。
- **领域迁移机制**：如何将扩散先验适配至医学等专业领域？直接微调扩散模型或引入领域特定的特征提取器是否可行？
- **自适应涌现点选择**：IEP 目前使用固定步长和全局峰值，能否实现图像自适应的涌现点定位，以应对不同内容和复杂度的场景？
- **端到端实例分割**：TRACE 实例边缘质量极高（ODS 0.889, Table 6），但当前仍需依赖 UIS 或 WSS 分割流程。如何直接从边缘生成像素级实例掩码，构建完整的无监督实例分割模型，是值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/TRACE_Your_Diffusion_Model_is_Secretly_an_Instance_Edge_Detector.pdf]]

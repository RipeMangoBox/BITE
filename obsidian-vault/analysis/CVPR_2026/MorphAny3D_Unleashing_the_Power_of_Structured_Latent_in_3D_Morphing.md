---
title: "MorphAny3D: Unleashing the Power of Structured Latent in 3D Morphing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MorphAny3D_Unleashing_the_Power_of_Structured_Latent_in_3D_Morphing.pdf
project_link: "https://xiaokunsun.github.io/MorphAny3D.github.io/"
code_link: null
aliases:
- MorphAny3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在注意力层中智能融合源与目标的SLAT特征（而非在噪声或条件层面插值），通过分离式交叉注意力与时间融合自注意力实现结构连贯与时间平滑。
primary_logic: 直接聚合SLAT特征于注意力机制内，相较于在噪声或条件层面插值，能产生更合理且视觉平滑的三维变形。
claims:
- MorphAny3D在50对跨类别源-目标上取得最优FID(111.95)、PDV(0.0006)、AS(81%)和用户偏好(86.73%)，PPL(2.47)与最优接近。
- 消融实验确认MCA使得FID从125.47降至112.18，加入TFSA后PPL降至2.87，加入方向校正后PPL进一步降至2.47，各项指标逐步提升。
- MCA通过独立计算源与目标注意力输出，避免了KV融合带来的语义歧义（图5），且其在t-SNE轨迹上更加平滑（图6）。
- 方向校正策略有效减少中间变形阶段的方向跳变（图7），使PPL与PDV进一步下降。
---

# MorphAny3D: Unleashing the Power of Structured Latent in 3D Morphing

> [!tip] 核心洞察
> 直接聚合SLAT特征于注意力机制内，相较于在噪声或条件层面插值，能产生更合理且视觉平滑的三维变形。

| 字段 | 内容 |
|------|------|
| 中文题名 | MorphAny3D：释放三维变形中结构化隐变量的力量 |
| 英文题名 | MorphAny3D: Unleashing the Power of Structured Latent in 3D Morphing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.00204) · [Project](https://xiaokunsun.github.io/MorphAny3D.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MorphAny3D |
| Dataset | 50对多样的跨类别三维物体（真实数据集与Trellis生成）, 50对多样的跨类别三维物体 |

> [!tip] 效果简介
> - 50对多样的跨类别三维物体（真实数据集与Trellis生成） 上，FID 111.95 vs 164.68 (FreeMorph) (-52.73)。
> - 50对多样的跨类别三维物体 上，PPL 2.47 vs 2.41 (MorphFlow) (+0.06)；PDV 0.0006 vs 0.0006 (3DInterp) (0)；AS 81.00% vs 11.00% (FreeMorph) (+70.00%)。

## 概要

三维变形（3D Morphing）旨在生成从源物体到目标物体的平滑、语义连贯的过渡序列。然而，跨类别变形面临一项核心瓶颈：**语义一致性与时间平滑性难以兼顾**。传统基于匹配的方法依赖显式对应关系，忽略纹理演进且泛化能力差；基于二维图像变形再升维的方法无法保证时序连续与结构合理性；直接插值噪声或条件特征的方法则产生语义模糊与视觉伪影。这些缺陷使得现有方案难以在任意三维物体之间生成真实且美观的变形。

针对上述瓶颈，MorphAny3D 提出了一种**无需训练的三维变形框架**，其核心思路是：在注意力层中智能融合源与目标的**结构化隐变量（Structured Latent, SLAT）**特征，而非在噪声或条件层面进行插值。具体而言，框架引入两个关键模块——**Morphing Cross-Attention（MCA）**和**Temporal-Fused Self-Attention（TFSA）**——分别解决结构连贯性与时间平滑性问题，并辅以方向校正策略抑制变形过程中的方向跳变。

在50对跨类别源-目标物体上的实验表明，MorphAny3D 在多项指标上取得最优或接近最优结果：FID 达 111.95（较最优基线 FreeMorph 降低 52.73），感知路径长度（PPL）为 2.47（与最优的 MorphFlow 仅差 0.06），路径方向方差（PDV）为 0.0006，美学评分（AS）达 81%，用户偏好（UP）达 86.73%。消融实验进一步验证了各模块的贡献：MCA 使 FID 从 125.47 降至 112.18，TFSA 使 PPL 从 3.66 降至 2.87，方向校正则进一步将 PPL 降至 2.47。该方法无需任何训练或超参数调节，可直接嵌入现有三维生成管线，为跨类别三维变形提供了一种高效且通用的解决方案。

### 问题背景：三维变形的核心瓶颈

三维变形（3D Morphing）旨在生成从源物体到目标物体的平滑、语义连贯的过渡序列。这一任务在视觉特效、数字内容创作和虚拟现实等领域具有广泛应用。然而，实现高质量的三维变形面临一个根本性瓶颈：**跨类别语义一致性与时间平滑性难以兼顾**。

具体而言，变形过程需要同时满足两个关键要求：一是中间帧必须在结构上合理、视觉上逼真，不能出现断裂或伪影；二是整个序列必须在时间维度上平滑演进，避免突兀的跳变。当源与目标属于不同语义类别（如“蜜蜂”变形为“双翼飞机”）时，二者之间缺乏直接的几何或纹理对应关系，这一矛盾尤为突出。

### 现有方法及其局限

当前的三维变形策略可归纳为三条技术路线，但均存在结构性缺陷：

**基于匹配的方法**（如 **3DInterp**、**SLATInterp**; Zhu et al., ICLR 2025）依赖显式的几何对应关系进行插值。这类方法需要源与目标之间共享拓扑结构或语义部件，泛化能力弱，且完全忽略了纹理的演进过程，导致变形结果在视觉上缺乏真实感（Figure 2a）。

**二维变形升维方法**（如 **DiffMorpher**; Zhang et al., CVPR 2024; **FreeMorph**; Cao et al., ICCV 2025）先在二维图像域完成变形，再借助 Image-to-3D 模型（如 Trellis）将中间帧提升至三维。这一间接路线割裂了二维变形与三维生成之间的关联，无法保证时序连续性与三维结构的合理性，常出现帧间跳变或几何崩塌（Figure 2b）。

**直接插值方法**（如 **DirectInterp**）在噪声或条件特征层面进行线性混合。然而，源与目标的特征空间往往存在语义歧义，简单插值会导致中间帧产生不合理的混合结构，视觉质量低下（Figure 2c）。

### 核心洞察：在注意力机制中融合结构化隐变量

上述方法的共同缺陷在于，它们未能在变形过程中有效利用三维生成模型内部的**结构化隐变量（Structured Latent, SLAT）**表征。SLAT 是 Trellis 等现代三维生成模型在去噪过程中产生的中间特征，编码了物体的稀疏结构（Sparse Structure, SS）与局部几何细节。

本文的核心洞察是：**直接在注意力层中智能融合源与目标的 SLAT 特征，而非在噪声或条件层面进行插值，能够产生更合理且视觉平滑的三维变形**。注意力机制天然具备跨模态信息聚合的能力——通过分别计算源与目标对当前帧的注意力输出，并按变形进度进行融合，可以避免特征层面的语义混淆；同时，引入前一帧的自注意力信息，能够自然地将时序平滑性内嵌于生成过程之中。

### 本文动机与目标

基于上述洞察，本文提出 **MorphAny3D**，一个无需任何训练的、基于 SLAT 的三维变形框架。其设计目标为：

1. **结构连贯性**：通过分离式交叉注意力（Morphing Cross-Attention, MCA）独立聚合源与目标信息，消除 KV 融合带来的语义歧义；
2. **时间平滑性**：通过时序融合自注意力（Temporal-Fused Self-Attention, TFSA）引入帧间约束，确保变形序列的连续演进；
3. **方向稳定性**：通过方向校正策略缓解中间阶段的方向跳变问题；
4. **零训练部署**：在现有 Trellis 模型基础上仅替换注意力模块，无需额外训练或超参数调节。

## 核心方法与创新机理

MorphAny3D的核心创新在于**将变形控制从条件/噪声空间迁移至注意力机制内部**，通过三个紧密协同的“changed slots”解决跨类别三维变形中语义一致性与时间平滑性难以兼顾的瓶颈。

### 瓶颈与因果杠杆

现有三维变形方法面临根本性困境：基于匹配的方法（如**3DInterp**、**SLATInterp**，Zhu et al., ICLR 2025）依赖DenseMatcher建立对应关系，但忽略了纹理演进且跨类别泛化能力差；2D变形后升维的方法（如**DiffMorpher**，Zhang et al., CVPR 2024；**FreeMorph**，Cao et al., ICCV 2025）通过Trellis将二维变形结果转为三维，却无法保证时序连续与结构合理；直接插值法（**DirectInterp**）则在噪声或条件层面进行线性混合，导致变形不真实或出现跳跃伪影。

MorphAny3D识别出真正的因果杠杆在于：**在注意力层中智能融合源与目标的SLAT特征，而非在噪声或条件层面插值**。这一洞察源于对SLAT融合模式的系统分析（Figure 4）：在交叉注意力中融合KV（键值）能提升合理性（FID最优），在自注意力中融合KV则有利于平滑性（PPL最优）。基于此，MorphAny3D设计了三个相互增强的模块，形成完整的变形控制链路。

### 关键Changed Slots

**1. 初始特征生成：从线性插值到球面插值**

传统直接插值法对噪声和条件特征采用线性混合，忽略了高维特征空间的几何结构。MorphAny3D改用基于变形权重α的球面插值（Slerp），利用源和目标SLAT特征之间的夹角θ进行插值：

$$f_{\mathrm{init.ss}}^{n} = \frac{\sin((1-\alpha^{n})\theta)}{\sin(\theta)} f_{\mathrm{init.ss}}^{\mathrm{src}} + \frac{\sin(\alpha^{n}\theta)}{\sin(\theta)} f_{\mathrm{init.ss}}^{\mathrm{tgt}}$$

这一改变使得初始特征在球面流形上平滑过渡，为后续注意力融合提供了更合理的起点（Sec. 3.2, Eq. 5）。

**2. 交叉注意力机制：从KV融合到MCA分离式融合**

这是最核心的changed slot。直接KV融合（KV-Fused Attention）在注意力计算前对源和目标的键值进行线性插值：

$$\mathrm{KV\text{-}Fused\text{-}Attn}(Q^n,K^{\mathrm{src/tgt}},V^{\mathrm{src/tgt}}) = \mathrm{Attn}\big(Q^n,(1-\alpha^n)K^{\mathrm{src}}+\alpha^n K^{\mathrm{tgt}},(1-\alpha^n)V^{\mathrm{src}}+\alpha^n V^{\mathrm{tgt}}\big)$$

然而，这种融合方式会导致严重的语义歧义——注意力图显示KV-Fused CA错误地关注了无关区域（Figure 5，橙色框标注），t-SNE可视化进一步揭示其特征轨迹呈现不稳定和中断（Figure 6）。

MorphAny3D提出的**Morphing Cross-Attention（MCA）**彻底改变了融合范式：**分别计算源和目标的注意力输出，然后用α线性融合结果**：

$$\mathrm{MCA}(Q^n,K^{\mathrm{src/tgt}},V^{\mathrm{src/tgt}}) = (1-\alpha^n)\mathrm{Attn}(Q^n,K^{\mathrm{src}},V^{\mathrm{src}}) + \alpha^n\mathrm{Attn}(Q^n,K^{\mathrm{tgt}},V^{\mathrm{tgt}})$$

这种“先注意后融合”的策略使得每个查询token能够独立地从源和目标中提取语义正确的信息，避免了KV融合带来的特征纠缠。消融实验证实，仅将标准交叉注意力替换为MCA，FID即从125.47降至112.18（Table 2），局部伪影被有效抑制（Figure 9-(a)）。

**3. 自注意力机制：从单帧到TFSA时间融合**

标准自注意力仅使用当前帧的SLAT特征，忽略了变形序列的时间连续性。MorphAny3D引入**Temporal-Fused Self-Attention（TFSA）**，融合前一帧的注意力输出：

$$\mathrm{TFSA}(Q^n,K^n,V^n,K^{n-1},V^{n-1}) = (1-\beta)\mathrm{Attn}(Q^n,K^n,V^n) + \beta\mathrm{Attn}(Q^n,K^{n-1},V^{n-1})$$

其中β=0.2控制前一帧的影响权重。TFSA的核心优势在于：它融合的是已经生成合理的前一帧特征，而非噪声或中间状态，因此在增强时间连贯性的同时不会引入伪影。消融实验显示，在MCA基础上加入TFSA后，PPL从3.66降至2.87，PDV从0.0010降至0.0007（Table 2），时间一致性显著增强（Figure 9-(b)）。

**4. 方向稳定性：从无约束到方向校正策略**

MorphAny3D还引入了一个辅助性的changed slot——方向校正策略。研究发现变形过程中存在突发的方向跳变（相邻帧角度差超过45°），且这些跳变集中在变形中间阶段（Figure 7）。为此，在稀疏结构生成阶段，对每个方向跳变帧生成四个偏航旋转候选，选择与前帧Chamfer距离最小者作为校正结构（Sec. 3.6）。加入方向校正后，PPL进一步降至2.47，PDV降至0.0006（Table 2），方向跳变得以有效缓解（Figure 9-(c)）。

### 创新协同效应

四个changed slots形成了从特征初始化、跨对象信息融合、时间一致性到方向稳定性的完整创新链路。MCA解决了“变形什么”（结构合理性），TFSA解决了“如何过渡”（时间平滑性），方向校正解决了“朝向哪里”（方向稳定性），而球面插值则为整个链路提供了几何上合理的起点。这种协同使得MorphAny3D在无需任何训练或超参数调节的前提下，在50对跨类别源-目标上取得了最优的FID（111.95）、PDV（0.0006）、AS（81%）和用户偏好（86.73%），PPL（2.47）也与最优方法接近（Table 1）。

MorphAny3D 的整体流程围绕 **结构化隐变量（Structured Latent, SLAT）** 这一核心表示展开，无需任何训练或微调，即可在任意三维物体之间生成平滑、语义连贯的变形序列。给定一个源物体 $x^{\mathrm{src}}$ 和一个目标物体 $x^{\mathrm{tgt}}$，目标是生成一段从源逐渐过渡到目标的 $N$ 帧变形序列 $\{x^n\}_{n=0}^{N}$，其中 $x^0 = x^{\mathrm{src}}$，$x^N = x^{\mathrm{tgt}}$，变形进度由权重 $\alpha^n \in [0,1]$ 控制。

### 管线模块与数据流

框架建立在 **Trellis** 的 SLAT 表示之上，包含五个关键模块，形成从三维反演到最终解码的完整闭环：

1. **三维反演（3D Inversion）**  
   从源和目标的三维资产（真实扫描或生成结果）中提取各自的初始噪声 SLAT 特征 $f_{\mathrm{init}}^{\mathrm{src}}$、$f_{\mathrm{init}}^{\mathrm{tgt}}$ 以及对应的图像条件。这一步将三维物体映射到 Trellis 的隐空间，为后续变形提供统一的表示基础。

2. **球面插值初始化**  
   利用源和目标初始特征之间的夹角 $\theta$，通过球面插值（SLERP）计算每一帧 $n$ 的初始稀疏结构（Sparse Structure, SS）特征：
   $$f_{\mathrm{init.ss}}^{n} = \frac{\sin((1-\alpha^{n})\theta)}{\sin(\theta)} f_{\mathrm{init.ss}}^{\mathrm{src}} + \frac{\sin(\alpha^{n}\theta)}{\sin(\theta)} f_{\mathrm{init.ss}}^{\mathrm{tgt}}$$
   同样的球面插值也应用于 SLAT 特征的初始化。这种初始化方式保证了变形路径在隐空间中沿最短弧线行进，为后续的平滑过渡奠定基础。

3. **稀疏结构（SS）生成**  
   将初始化后的 SS 特征送入 **SS Flow Transformer**。在此阶段，交叉注意力层被替换为 **Morphing Cross-Attention（MCA）**，分别计算源和目标的注意力输出，再以 $\alpha^n$ 线性融合；同时引入 **方向校正策略**，在检测到相邻帧偏航角差异超过 $45^\circ$ 时，生成四个偏航旋转候选，选择与前一帧 Chamfer 距离最小者作为校正后的稀疏结构。该模块输出每一帧的稀疏体素结构。

4. **结构化隐变量（SLAT）生成**  
   将初始化后的 SLAT 特征送入 **SLAT Flow Transformer**。此阶段同样采用 MCA 处理跨物体的信息融合，并在自注意力层中引入 **Temporal-Fused Self-Attention（TFSA）**，以权重 $\beta=0.2$ 融合前一帧的自注意力输出，增强帧间的时间一致性。该模块输出每一帧的局部隐向量，构成完整的 SLAT 表示。

5. **三维解码**  
   将生成的 SLAT 解码为标准的显式三维表示——论文默认使用 Trellis 的解码器，可输出 Mesh、NeRF 或 3D Gaussian Splatting（3DGS）等形式，供下游应用直接使用。

### 核心设计决策

整个框架的关键设计在于 **将源与目标的 SLAT 特征融合操作下沉到注意力层内部**，而非在噪声或条件特征层面进行插值。这一决策由 Figure 4 中的融合模式分析驱动：实验表明，在交叉注意力中融合 KV（键值）有利于提升合理性（FID 更低），而在自注意力中融合 KV 有利于提升平滑性（PPL 更低）。MorphAny3D 据此分别设计了 MCA（交叉注意力中的输出级融合）和 TFSA（自注意力中的时序融合），在合理性与平滑性之间取得了最优平衡。Figure 3 清晰展示了 MCA、TFSA 和方向校正模块在 Trellis 原有流程中的插入位置，体现了“即插即用”的模块化设计理念。

![[assets/figures/papers/paper_list_l2548_https_arxiv_org_abs_2601_00204/figures/003_Figure_3.jpg]]
*Figure 3: (a) Overview of our method. MorphAny3D generates a smooth and high-quality morphing sequence between diverse object categories by leveraging the SLAT representation without any training. (b) Morphing Cross-Attention (MCA) fuses information from the ????� ????source and target objects in the cross-attention layers to ensure the structural coherence and aesthetics of the deformation. (c) Temporal-Fused Self-Attention (TFSA) enhances temporal smoothness by incorporating SLAT features from the previous morphing frame into the Previous Frame’s self-attention mechanism, enabling smooth transitions over time. (d) An orientation correction strategy inspired by statistical orientation Structure ????...*

![[assets/figures/papers/paper_list_l2548_https_arxiv_org_abs_2601_00204/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of different 3D morphing strategies. (a) Matching-Based 3D Morphing; (b) 2D Morphing + 3D Generation; (c) Direct Interpolation; (d) MorphAny3D. Our method leverages the powerful SLAT to achieve semantically plausible and temporally smooth 3D morphing without any training. α ∈ [0, 1] is the deformation weight controlling the morphing progress*

MorphAny3D 在预训练的 Trellis 三维生成框架上，仅替换注意力层而无需任何训练，实现了跨类别三维变形。其核心由四个关键模块构成：球面插值初始化、Morphing Cross-Attention（MCA）、Temporal-Fused Self-Attention（TFSA）和方向校正策略。

### 标准注意力机制

MorphAny3D 的所有注意力模块均基于标准缩放点积注意力构建：

$$
\mathrm{Attn}(Q,K,V) = \mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

其中 $Q$ 为查询向量，$K$ 和 $V$ 分别为键和值特征，$d_k$ 为键向量的维度，用于缩放防止梯度消失。

### 球面插值初始化

给定源物体 $x^{\mathrm{src}}$ 和目标物体 $x^{\mathrm{tgt}}$，首先通过三维反演提取各自的初始噪声特征。对于变形序列的第 $n$ 帧，其初始稀疏结构（SS）特征 $f_{\mathrm{init.ss}}^{n}$ 通过球面插值计算：

$$
f_{\mathrm{init.ss}}^{n} = \frac{\sin((1-\alpha^{n})\theta)}{\sin(\theta)} f_{\mathrm{init.ss}}^{\mathrm{src}} + \frac{\sin(\alpha^{n}\theta)}{\sin(\theta)} f_{\mathrm{init.ss}}^{\mathrm{tgt}}
$$

其中 $\alpha^{n} \in [0,1]$ 为变形权重，控制变形进程；$\theta$ 为源和目标初始特征向量之间的夹角。球面插值相较于直接线性插值，能更好地保持特征在高维空间中的范数一致性，为后续注意力融合提供更稳定的初始化。

### Morphing Cross-Attention（MCA）

在交叉注意力层中，传统做法是将源和目标的键值直接进行线性插值融合（KV-Fused Attention）：

$$
\mathrm{KV\text{-}Fused\text{-}Attn}(Q^n,K^{\mathrm{src/tgt}},V^{\mathrm{src/tgt}}) = \mathrm{Attn}\big(Q^n,(1-\alpha^n)K^{\mathrm{src}}+\alpha^n K^{\mathrm{tgt}},(1-\alpha^n)V^{\mathrm{src}}+\alpha^n V^{\mathrm{tgt}}\big)
$$

然而，这种在注意力计算前对键值进行融合的方式会导致语义歧义——源和目标的键向量在语义空间中可能指向不同区域，直接混合使得注意力图无法准确聚焦于各自对应的结构（见图5），从而产生局部伪影。

MCA 将融合操作推迟到注意力计算之后，分别计算源和目标的独立注意力输出，再用变形权重 $\alpha^n$ 进行线性融合：

$$
\mathrm{MCA}(Q^n,K^{\mathrm{src/tgt}},V^{\mathrm{src/tgt}}) = (1-\alpha^n)\mathrm{Attn}(Q^n,K^{\mathrm{src}},V^{\mathrm{src}}) + \alpha^n\mathrm{Attn}(Q^n,K^{\mathrm{tgt}},V^{\mathrm{tgt}})
$$

这一设计的核心洞察在于：**在注意力输出层面聚合，而非在噪声或条件层面插值**，能保留各自的语义完整性。t-SNE 可视化（图6）证实，MCA 的特征轨迹相比 KV-Fused Attention 更加平滑稳定，避免了中间帧的语义跳变。消融实验（Table 2）表明，将标准交叉注意力替换为 MCA 后，FID 从 125.47 降至 112.18，局部伪影被有效抑制。

### Temporal-Fused Self-Attention（TFSA）

自注意力层仅使用当前帧的 SLAT 特征时，相邻帧之间缺乏显式的时序约束，容易导致变形序列出现抖动。TFSA 通过融合前一帧的注意力输出来增强时间连贯性：

$$
\mathrm{TFSA}(Q^n,K^n,V^n,K^{n-1},V^{n-1}) = (1-\beta)\mathrm{Attn}(Q^n,K^n,V^n) + \beta\mathrm{Attn}(Q^n,K^{n-1},V^{n-1})
$$

其中 $\beta=0.2$ 控制前一帧的影响权重。TFSA 并非简单地对帧特征进行平滑，而是在注意力层面引入时序信息——当前帧的查询 $Q^n$ 同时与当前帧和前一帧的键值计算注意力，使得生成的特征既保留当前变形阶段的语义忠实度，又继承前一帧已形成的合理结构。消融实验（Table 2）显示，加入 TFSA 后 PPL 从 3.66 降至 2.87，PDV 从 0.0010 降至 0.0007，时间一致性显著提升。

### 方向校正策略

在变形过程中，稀疏结构生成阶段可能出现偏航方向的突然跳变，尤其在中间帧（$\alpha$ 接近 0.5）时最为频繁（图7）。方向校正策略的机制是：当检测到相邻帧的偏航角变化 $\Delta E$ 超过 $45^\circ$ 时，在稀疏结构阶段生成四个偏航旋转候选（$0^\circ$、$90^\circ$、$180^\circ$、$270^\circ$），选择与前一帧 Chamfer 距离最小的候选作为校正后的结构。该策略使 PPL 进一步降至 2.47，PDV 降至 0.0006（Table 2）。

### 模块协同

上述模块在 Trellis 的两阶段生成流程中分工协作：SS Flow Transformer 使用 MCA 交叉注意力和方向校正生成帧的稀疏体素结构；SLAT Flow Transformer 使用 MCA 交叉注意力和 TFSA 自注意力生成局部隐向量；最终由三维解码器将结构化隐变量解码为 Mesh、NeRF 或 3DGS 等标准表示。整个框架无需任何训练或超参数调节，仅替换注意力模块即实现了跨类别三维变形的结构连贯性与时间平滑性。

![[assets/figures/papers/paper_list_l2548_https_arxiv_org_abs_2601_00204/figures/006_Figure_5.jpg]]
*Figure 5: Attention maps visualization for different attention etmechanisms. Red stars denote head SLAT features; pink stars Tamark their corresponding input regions. Orange boxes highlight KV-Fused CA’s incorrect attention focus. MCA preserves correct, 3D Resultssemantically consistent attention and avoids KV-Fused CA’s artifacts shown in Fig. 4-(b)*

## 实验与关键发现

### 评估设置与基线

为系统验证 MorphAny3D 的变形质量，作者构建了包含 50 对跨类别源-目标物体的测试集，涵盖真实扫描资产与 Trellis 生成资产。评估维度覆盖五个方面：**FID**（变形合理性）、**PPL**（路径平滑度）、**PDV**（路径方向方差）、**AS**（美学评分，由 Gemini-2.5 与 ChatGPT-5 双模型评判，见 Figure 13）以及 **UP**（用户偏好投票）。

基线方法分为三类：（1）**匹配法**——3DInterp 与 SLATInterp（Zhu et al., ICLR 2025），基于 DenseMatcher 进行三维几何或 SLAT 特征插值；（2）**2D 升维法**——DiffMorpher（Zhang et al., CVPR 2024）与 FreeMorph（Cao et al., ICCV 2025），先在二维图像空间变形，再通过 Trellis 升维至三维；（3）**直接插值法**——DirectInterp，在噪声与条件特征层面直接线性插值。所有 2D 方法统一使用 Trellis 作为 Image-to-3D 后端，确保比较公平。MorphAny3D 无需任何训练或超参数调节，仅在 Trellis 框架内替换注意力模块。

### 主结果分析

Table 1 汇总了各方法的定量对比。MorphAny3D 在五项指标中取得四项最优：

![[assets/figures/papers/paper_list_l2548_https_arxiv_org_abs_2601_00204/figures/010_Table_1.jpg]]
*Table 1: Quantitative comparison. Best and second-best in bold and underlined*

| 指标 | MorphAny3D | 最优基线 | 提升幅度 |
|------|-----------|---------|---------|
| FID↓ | **111.95** | 164.68 (FreeMorph) | -52.73 |
| PPL↓ | 2.47 | 2.41 (MorphFlow) | +0.06（次优） |
| PDV↓ | **0.0006** | 0.0006 (3DInterp) | 持平最优 |
| AS↑ | **81.00%** | 11.00% (FreeMorph) | +70.00% |
| UP↑ | **86.73%** | 5.51% (DirectInterp) | +81.22% |

FID 的显著优势（111.95 vs. 164.68）表明 MCA 驱动的变形在视觉合理性上远超所有基线。PPL 略逊于 MorphFlow（2.47 vs. 2.41），但 MorphFlow 依赖多视图再生，泛化性受限；MorphAny3D 在保持接近平滑度的同时，获得了压倒性的美学与用户偏好优势。AS 与 UP 的大幅领先（+70% 和 +81%）直接验证了核心洞察：**在注意力层内智能融合 SLAT 特征，比在噪声或条件层面插值产生更符合人类审美的变形结果**。

DirectInterp 的 UP 仅 5.51%，说明直接插值噪声会导致严重伪影与语义断裂；2D 升维法（DiffMorpher、FreeMorph）受限于二维变形与三维重建之间的域间隙，FID 均超过 160。匹配法（3DInterp、SLATInterp）虽在平滑度上表现尚可，但忽略了纹理演进，导致美学评分不足 10%。

### 消融实验

Table 2 与 Figure 9 系统拆解了三大模块的贡献。消融基线为 KV-Fused CA + 标准自注意力（无方向校正）：

![[assets/figures/papers/paper_list_l2548_https_arxiv_org_abs_2601_00204/figures/011_Table_2.jpg]]
*Table 2: Ablation study on key components of MorphAny3D*

![[assets/figures/papers/paper_list_l2548_https_arxiv_org_abs_2601_00204/figures/012_Figure_9.jpg]]
*Figure 9: Ablation study on (a) MCA, (b) TFSA, and (c) OC*

| 配置 | FID↓ | PPL↓ | PDV↓ |
|------|------|------|------|
| KV-Fused CA + Standard SA | 125.47 | 3.66 | 0.0010 |
| + MCA（替换 KV-Fused CA） | **112.18** | 3.66 | 0.0010 |
| + MCA + TFSA | 112.18 | **2.87** | **0.0007** |
| + MCA + TFSA + OC（完整版） | **111.95** | **2.47** | **0.0006** |

**MCA 的独立贡献**：将 KV-Fused CA 替换为 MCA 后，FID 从 125.47 骤降至 112.18（降幅 10.6%）。Figure 9-(a) 定性显示，MCA 消除了 KV 融合带来的局部伪影（如蓝色框区域）。机制层面，Figure 5 揭示 KV-Fused CA 在注意力图中出现语义错配（橙色框），而 MCA 通过独立计算源与目标的注意力输出保持了正确的语义对应；Figure 6 的 t-SNE 轨迹进一步证实 MCA 的特征演进更加稳定平滑，而 KV-Fused CA 轨迹呈现断续跳跃。

**TFSA 的独立贡献**：在 MCA 基础上加入 TFSA，PPL 从 3.66 降至 2.87（降幅 21.6%），PDV 从 0.0010 降至 0.0007（降幅 30%）。Figure 9-(b) 显示 TFSA 增强了时间一致性——螃蟹钳子和眼睛等精细结构在帧间保持稳定（绿色/红色框）。这一改进源于 TFSA 以 β=0.2 融合前一帧的自注意力输出，使当前帧的 SLAT 特征受已生成合理帧的约束。

**方向校正的独立贡献**：加入方向校正（OC）后，PPL 进一步降至 2.47，PDV 降至 0.0006。Figure 9-(c) 展示 OC 有效抑制了中间帧的方向跳变，使变形序列的物体朝向保持连贯。该策略在稀疏结构生成阶段，当相邻帧偏航角差超过 45° 时触发校正——生成四个偏航候选，选择与前一帧 Chamfer 距离最小者作为校正结构。

### 失败模式与局限性

Figure 12 展示了两个典型失败案例。案例一涉及极精细几何结构（如复杂机械部件），变形过程中出现局部伪影与细节丢失——这继承自 Trellis 对细粒度结构建模的固有限制。案例二涉及偏航对称物体（如对称花瓶），方向校正策略无法有效处理对称轴上的旋转歧义，导致变形序列中出现不自然的旋转。

此外，每帧生成耗时约 30 秒（A6000 GPU），难以满足实时交互需求。在基于文本条件（而非图像条件）的 SLAT 模型中，变形质量与时间连贯性均有下降，表明当前框架对条件模态存在一定敏感性。这些局限性指向了未来改进方向：增强方向校正以处理对称物体、通过 KV 缓存等加速推理、以及探索文本条件下的鲁棒变形策略。

## 定位与知识库关联

### 三维变形方法谱系

MorphAny3D 处于三维变形方法谱系中的“结构化隐变量驱动”分支，其核心定位是**免训练、跨类别、时序平滑的三维变形框架**。与现有方法相比，其关键差异在于变形发生的表征层面与融合机制。

**基于匹配的三维变形方法**通过在源与目标之间建立显式对应关系实现变形。**3DInterp**（Zhu et al., ICLR 2025）利用 DenseMatcher 建立几何对应后进行插值，在 PDV 指标上达到 0.0006 的路径平滑度，但该方法完全忽略纹理信息的演进，且匹配质量高度依赖类别相似性，跨类别泛化能力有限。**SLATInterp**（同上）将匹配机制迁移至 SLAT 特征空间，但仍受限于对应关系质量。**MorphFlow**（Tsai et al., ECCV 2022）通过多视图再生变形实现时序平滑，取得了最优 PPL（2.41），但其依赖多视图输入，部署复杂度较高。

**二维变形升维方法**将三维变形问题转化为二维图像变形后通过重建模型升维。**DiffMorpher**（Zhang et al., CVPR 2024）与 **FreeMorph**（Cao et al., ICCV 2025）均采用此范式，使用 Trellis 作为统一的 Image-to-3D 后端。这类方法的根本瓶颈在于：二维变形无法保证三维结构在时间维度上的连续性与合理性，导致 FID 高达 164.68（FreeMorph），对齐得分（AS）仅 11.00%，表明生成结果与源/目标的结构一致性严重不足。

**直接插值方法**（DirectInterp）在噪声或条件特征层面进行线性插值，是最朴素的免训练基线。该方法完全缺乏对语义结构的感知，用户偏好（UP）仅 5.51%，且常产生不合理的中间形态。

MorphAny3D 的方法论突破在于**将变形操作从表征插值层面提升至注意力融合层面**。通过 Morphing Cross-Attention（MCA）分别计算源与目标的注意力输出后线性融合，避免了 KV 融合带来的语义歧义（Figure 5）；通过 Temporal-Fused Self-Attention（TFSA）引入前帧自注意力输出，实现了帧间平滑过渡。这一设计使得 MorphAny3D 在 FID（111.95）上大幅领先所有基线，同时保持与最优方法接近的时序平滑度（PPL 2.47 vs. MorphFlow 2.41）。

### 知识库定位与理论基础

MorphAny3D 建立在两个关键知识基础之上：

1. **结构化隐变量（SLAT）表征**：继承自 Trellis 框架的三维生成先验。SLAT 将三维物体编码为稀疏结构（SS）与局部隐向量（SLAT）的双层表征，为变形提供了语义上有意义的操作空间。MorphAny3D 不修改 Trellis 的预训练权重，仅在注意力层替换融合策略，体现了“表征复用”的设计哲学。

2. **扩散模型反演与引导**：通过三维反演（3D Inversion）从真实资产或生成结果中提取源与目标的初始噪声特征和图像条件，利用球面插值（Eq. 5）初始化各帧特征，再通过 SS Flow Transformer 与 SLAT Flow Transformer 逐步去噪生成中间帧。这一流程本质上是一种免训练的扩散引导策略。

### 适用边界与局限

**适用场景**：
- 跨类别三维物体之间的平滑变形（如蜜蜂到双翼飞机，Figure 1）
- 解耦变形、双目标变形、三维风格迁移等扩展应用（Figure 10）
- 基于图像条件或文本条件的 SLAT 模型均可适用

**明确局限**：
1. **精细结构伪影**：继承 Trellis 的固有限制，对极精细的几何结构（如细长触角、复杂机械部件）可能产生伪影（Figure 12 案例 1）。
2. **方向校正盲区**：方向校正策略基于偏航旋转候选的 Chamfer 距离选择，无法处理偏航对称物体（如对称花瓶）的旋转跳变（Figure 12 案例 2）。
3. **推理效率**：每帧生成耗时约 30 秒（A6000 GPU），难以满足实时交互需求。
4. **文本条件退化**：在基于文本条件的 SLAT 模型中，变形质量和时间连贯性较图像条件模型有所下降。

### 开放问题

1. **方向校正增强**：如何扩展方向校正策略以处理偏航对称物体的旋转？可能需要引入语义感知的朝向判别机制。
2. **推理加速**：能否通过 KV 缓存、帧间特征复用或蒸馏等方法将推理时间降低至实时交互水平（<1 秒/帧）？
3. **形状-纹理解耦**：当前方法对形状与纹理进行联合变形，如何实现更精细的解耦控制以支持局部编辑？
4. **表征泛化**：本框架能否推广至动态场景变形或其他三维表征（如 3D Gaussian Splatting）？这需要重新审视 SLAT 表征的适用范围。

## 原文 PDF

![[paperPDFs/CVPR_2026/MorphAny3D_Unleashing_the_Power_of_Structured_Latent_in_3D_Morphing.pdf]]

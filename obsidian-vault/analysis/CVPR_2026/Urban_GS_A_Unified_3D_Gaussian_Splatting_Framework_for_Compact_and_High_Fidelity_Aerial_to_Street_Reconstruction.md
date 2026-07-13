---
title: "Urban-GS: A Unified 3D Gaussian Splatting Framework for Compact and High-Fidelity Aerial-to-Street Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Urban_GS_A_Unified_3D_Gaussian_Splatting_Framework_for_Compact_and_High_Fidelity_Aerial_to_Street_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- UG
- Urban-GS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将梯度按投影面积（即像素覆盖数）加权以平衡不同尺度下的贡献，从而准确触发致密化。
primary_logic: 通过投影面积加权梯度实现跨尺度自适应的致密化；通过贡献感知的掩码正则化实现保留稀疏但局部重要的锚点，同时有效剪枝冗余结构；并采用全局到局部的分阶段优化策略，重点细化视图不稳定的欠优化区域。
claims:
- 同时使用空地视角进行梯度累积的致密化性能劣于单独使用一种视角，表明存在梯度冲突。
- 投影面积加权致密化（AJAD）可大幅提升渲染质量，PSNR从25.20提升至25.66。
- 贡献感知锚点剪枝（CAP）在几乎无损画质下将锚点数从9713k降至2785k，减少约71%。
- 全局到局部优化（GLO）进一步将PSNR提升至26.05，且锚点数降至2682k。
---

# Urban-GS: A Unified 3D Gaussian Splatting Framework for Compact and High-Fidelity Aerial-to-Street Reconstruction

> [!tip] 核心洞察
> 通过投影面积加权梯度实现跨尺度自适应的致密化；通过贡献感知的掩码正则化实现保留稀疏但局部重要的锚点，同时有效剪枝冗余结构；并采用全局到局部的分阶段优化策略，重点细化视图不稳定的欠优化区域。

| 字段 | 内容 |
|------|------|
| 中文题名 | Urban-GS：面向紧凑高保真空地联合重建的统一三维高斯泼溅框架 |
| 英文题名 | Urban-GS: A Unified 3D Gaussian Splatting Framework for Compact and High-Fidelity Aerial-to-Street Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Urban-GS_A_Unified_3D_Gaussian_Splatting_Framework_for_Compact_and_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Urban-GS |
| Dataset | Horizon-GS 数据集, UC-GS 数据集 |

> [!tip] 效果简介
> - Horizon-GS 数据集 (Colosseum 场景) 上，PSNR 26.88 vs 26.16 (Horizon-GS) (+0.72)；SSIM 0.890 vs 0.879 (Horizon-GS) (+0.011)；LPIPS 0.095 vs 0.108 (Horizon-GS) (-0.013)。
> - Horizon-GS 数据集 (平均) 上，锚点数 (存储效率) ~1801k (41% reduction) vs ~3050k (Horizon-GS 平均) (-1249k (-41%))。
> - UC-GS 数据集 (View+1m 场景) 上，PSNR 26.58 vs 25.48 (Horizon-GS) (+1.10)。

## 概要

空地联合三维重建的核心瓶颈在于，航拍与街景视角之间存在巨大的覆盖范围与尺度差异。当直接沿用标准高斯泼溅方法中基于均匀梯度累积的致密化策略时，两类视角的梯度信号会相互冲突，导致模型无法有效识别那些在不同尺度下均具有重要贡献的高斯原语，从而严重限制了细节重建质量。同时，为捕捉多尺度细节而引入的大量锚点造成了显著的存储开销，而不平衡的视角分布又使得部分区域长期处于欠优化状态。

针对上述问题，**Urban-GS** 提出了一套统一的三维高斯泼溅框架，通过三个关键设计实现紧凑且高保真的空地联合重建：

1.  **空地联合自适应致密化 (AJAD)**：将致密化触发条件中的梯度按各视图的投影面积（即像素覆盖数）进行加权，以平衡不同尺度下的梯度贡献，从而准确触发锚点生长，解决梯度冲突。
2.  **贡献感知锚点剪枝 (CAP)**：引入可学习的掩码机制，并设计贡献加权的掩码正则化损失，在保留稀疏但对渲染贡献大的局部重要锚点的同时，有效剪除冗余结构，大幅降低存储开销。
3.  **全局到局部优化 (GLO)**：采用两阶段训练策略，在全局训练后识别出视图不稳定的欠优化区域，对其进行分组局部细化，在不增加额外锚点的前提下显著提升重建质量。

实验表明，在 Horizon-GS 数据集上，Urban-GS 相较于当前最优方法 **Horizon-GS** (Jiang et al., CVPR 2025)，在 Colosseum 场景上实现了 **+0.72 dB PSNR** 的提升，同时平均锚点数量减少 **41%**，渲染帧率亦显著提高。在 UC-GS 数据集上，Urban-GS 同样取得了 **+1.10 dB PSNR** 的增益。消融实验进一步验证了各模块的有效性：AJAD 使 PSNR 从 25.20 提升至 25.66；CAP 在几乎无损画质下将锚点数从 9713k 降至 2785k（减少约 71%）；GLO 则将 PSNR 进一步提升至 26.05，且锚点数降至 2682k。

### 任务场景：空地联合城市场景重建

大尺度城市场景的数字化建模是自动驾驶、城市规划、虚拟现实等应用的基础技术。近年来，基于**3D Gaussian Splatting (3DGS)**（Kerbl et al., ACM TOG 2023）的显式辐射场表示方法凭借其高质量实时渲染能力受到广泛关注。然而，城市场景的重建面临一个独特挑战：数据采集通常包含**航拍视角**（俯瞰、全局覆盖）和**街道视角**（地面、局部细节）两类来源，两者在空间分辨率、覆盖范围和外观上存在巨大差异。如何在一个统一框架中同时利用这两种互补视角，实现高保真且存储高效的重建，是当前亟待解决的问题。

### 现有方法的局限

目前最直接的基线方法**Horizon-GS**（Jiang et al., CVPR 2025）率先尝试了空地联合的3DGS重建，但其仍存在三个核心瓶颈：

1. **致密化梯度冲突**：标准3DGS的致密化策略基于所有训练视图上未加权的平均视空间位置梯度（Eq. 3）来触发新高斯原语的生成。在空地联合场景中，航拍视图下单个高斯覆盖的像素数远多于街道视图，导致两类视图的梯度量级严重失衡。梯度累积时，来自某一类视图的有效致密化信号会被另一类视图的梯度“淹没”，使得需要细化的区域无法被正确识别。实验证据（Table 1）表明，同时使用空地视角进行梯度累积的致密化性能**劣于**单独使用一种视角，直接验证了梯度冲突的存在。

2. **锚点数量膨胀**：为捕捉从航拍到街道的多尺度细节，模型倾向于生成大量高斯原语，导致存储开销急剧增加。例如，基线模型在Colosseum场景上的锚点数可达9713k，严重制约了实际部署效率。

3. **欠优化区域**：空地视角分布极不均衡——航拍视图覆盖全局但稀疏，街道视图局部密集但存在大量遮挡和视角受限区域。均匀采样训练策略无法对视图不稳定的欠优化区域进行针对性细化，导致部分区域的重建质量瓶颈。

### 本文动机与核心思路

针对上述问题，本文提出**Urban-GS**，一个统一的3D高斯泼溅框架，旨在实现紧凑且高保真的空地联合重建。核心洞察在于：**通过投影面积加权梯度实现跨尺度自适应的致密化**，消除梯度冲突；**通过贡献感知的掩码正则化**，在保留稀疏但局部重要锚点的同时有效剪枝冗余结构；**通过全局到局部的分阶段优化策略**，重点细化视图不稳定的欠优化区域。三者协同，在显著提升渲染质量的同时将锚点数量平均压缩41%。

## 核心方法与创新机理

Urban-GS 的核心创新在于系统性地解决了空地联合三维重建中由极端尺度差异引发的三个连锁瓶颈：**致密化冲突**、**存储冗余**和**视图不平衡优化**。与直接基线 **Horizon-GS**（Jiang et al., CVPR 2025）相比，Urban-GS 在致密化触发条件、锚点剪枝正则化和优化策略三个关键槽位上进行了根本性改造，形成了“自适应致密化—贡献感知剪枝—全局到局部优化”的闭环。

### 创新一：空地联合自适应致密化（AJAD）—— 解决梯度冲突

空地视角间巨大的覆盖范围差异导致标准致密化策略失效。标准 3DGS 的致密化条件是对所有训练视图的视空间位置梯度取未加权平均（Eq. 3），这在空地场景中会引发严重的梯度冲突：航拍视图覆盖像素多但梯度幅值小，街拍视图覆盖像素少但梯度幅值大，二者直接平均导致大量本应致密化的高斯原语被抑制。Table 1 的消融实验直接验证了这一现象——同时使用空地视角进行梯度累积的致密化性能（PSNR 25.35/25.32）劣于单独使用航拍视角（PSNR 25.64/25.21），证实了梯度冲突的存在。

Urban-GS 提出的 AJAD 策略将致密化条件改为**按各视图贡献像素数（投影面积）加权的平均梯度**（Eq. 6）。其因果机制在于：投影面积直接反映了高斯原语在不同视图下的可见尺度，以像素数为权重可以自然平衡航拍大尺度低梯度与街拍小尺度高梯度之间的贡献差异，使致密化决策真正反映原语在多尺度下的重建需求。Table 5 的模块消融表明，仅添加 AJAD 即可将 PSNR 从 25.20 提升至 25.66，验证了加权机制对梯度冲突的有效化解。

### 创新二：贡献感知锚点剪枝（CAP）—— 实现高效压缩

多尺度细节捕捉导致锚点数量膨胀，标准全局掩码稀疏损失 $L_{mask} = (\frac{1}{N} \sum M_i)^2$（Eq. 8）对所有锚点施加均匀的稀疏压力，无法区分局部重要但全局稀疏的锚点与真正冗余的锚点，容易误删对特定视角至关重要的结构。

Urban-GS 的 CAP 策略引入**贡献加权的掩码正则化** $L_m = \frac{1}{kN} \sum (1-w_i) m_i$（Eq. 11）。其核心机制是：首先计算每个神经高斯在各视图下的归一化贡献 $w_i^v$（Eq. 9），然后跨视图聚合得到聚合贡献权重 $w_i$（Eq. 10），最后用 $(1-w_i)$ 作为掩码 $m_i$ 的惩罚系数——贡献越高的锚点惩罚越小，从而在稀疏化过程中被保护。Table 5 显示，添加 CAP 后锚点数从 9713k 骤降至 2785k（减少约 71%），而 PSNR 仅从 25.66 微降至 25.50，实现了近乎无损的高效压缩。Table 7 的对比消融进一步证明，在相同 PSNR 水平下，贡献感知剪枝比全局掩码正则化使用更少的锚点，有效保护了局部重要结构。

### 创新三：全局到局部优化（GLO）—— 针对性细化欠优化区域

空地数据的不平衡视角分布导致部分区域在全局训练中欠优化。Urban-GS 提出两阶段 GLO 策略：全局训练完成后，识别 PSNR 波动较大的不稳定视图，将与其锚点重叠率超过阈值 $\tau_{group}$ 的候选视图组成局部优化组（Eq. 12），冻结无关参数后进行针对性细化。Table 5 显示，添加 GLO 后 PSNR 进一步提升至 26.05，同时锚点数进一步降至 2682k，表明局部细化可在不增加额外锚点的情况下显著提升质量。Table 8 的对比消融显示，GLO 带来的 PSNR 增益（+0.55）远高于额外 20k 迭代统一采样的增益（+0.09），证明了针对性局部优化的有效性远超简单的增加训练量。

Urban-GS 提出了一套面向空地联合城市场景重建的统一三维高斯泼溅框架，其核心目标是同时解决**空地视角间巨大的尺度差异导致的梯度冲突**以及**多尺度细节捕捉带来的锚点数量膨胀与存储开销**问题。框架采用两阶段流水线设计，整体结构如 **Figure 2** 所示。

![[assets/figures/papers/paper_list_l2622_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Urban_GS_A_Unifie/figures/002_Figure_2.jpg]]
*Figure 2: The overview pipeline of Urban-GS. Top (Gloabal Training): We start by initializing LOD-structured anchors from SfMderived points of the aerial-to-street urban scene, followed by adaptive densification control using Aerial-Street Joint Adaptive Densification (Sec. 4.1) and Contribution-based Anchor Pruning (Sec. 4.2) for high-quality and memory-efficient global modeling. Bottom (Local Refinement): Based on PSNR fluctuations collected during global training, we perform local refinement (Sec. 4.3) on regions observed by unstable views to further enhance reconstruction quality, after global training finished*

### 全局训练阶段

第一阶段为**全局训练**，从运动恢复结构（SfM）导出的稀疏点云出发，初始化具有层级细节（LOD）结构的锚点。在此之上，框架引入两个关键模块交替驱动场景表示的生长与压缩：

- **空地联合自适应致密化（Aerial-Street Joint Adaptive Densification, AJAD）**：针对标准 3DGS 中基于所有视图未加权平均位置梯度（Eq. 3）触发致密化的策略在空地场景下失效的问题，AJAD 将致密化条件修改为按各视图的**投影面积（即贡献像素数 $|\mathcal{P}_i^v|$）加权**的平均梯度（Eq. 6）。这一设计使得在不同尺度视图下均有重要贡献的高斯原语能被准确识别并触发锚点生长，从而解决了因航空与街景视图覆盖像素数悬殊而导致的梯度积累冲突。
- **贡献感知锚点剪枝（Contribution-based Anchor Pruning, CAP）**：为抑制多尺度细节导致的锚点数量膨胀，CAP 为每个锚点引入可学习的二值掩码 $m_i$（通过 Gumbel-Softmax 采样），并设计**贡献加权的掩码正则化损失** $L_m$（Eq. 11）。与全局均匀稀疏化损失（Eq. 8）不同，$L_m$ 根据各高斯原语在渲染过程中的实际贡献权重 $w_i$（Eq. 9-10）进行差异化惩罚：低贡献高斯被鼓励将其掩码值减小至零以实现剪枝，而稀疏但局部贡献大的锚点则被保留。这在不牺牲渲染质量的前提下大幅压缩了模型规模。

全局训练阶段还联合优化了包含 L1、SSIM、体积正则、深度监督、透明度掩码及掩码正则化在内的多损失函数（Eq. 14），为后续局部细化提供高质量的全局基模型。

### 局部细化阶段

第二阶段为**局部细化**。全局训练完成后，框架通过监测各训练视图在训练过程中的 PSNR 波动（最后三次记录值的最大差异超过 1.0 的视图被标记为不稳定），识别出视图不稳定的欠优化区域。随后，根据候选视图与目标不稳定视图的锚点重叠率（Eq. 12）将相关视图组成视图组，针对性地进行局部细化训练。在此过程中，与当前组无关的锚点参数被冻结，仅更新组内可见锚点，从而在不引入额外锚点的情况下显著提升欠优化区域的渲染质量。

### 输入输出流

整体管线以空地联合采集的多视角图像及对应的 SfM 点云为输入，经过全局训练与局部细化两阶段处理后，输出一个紧凑的、支持跨尺度高保真新视角合成的 3D 高斯场表示。该表示可在街景与航拍视角下均提供优于基线方法的渲染质量，同时实现平均约 41% 的存储开销降低（**Table 3**）。

Urban‑GS 围绕三个核心机制重构了空地联合重建的致密化、剪枝与优化流程：**空地联合自适应致密化 (AJAD)**、**贡献感知锚点剪枝 (CAP)** 与 **全局到局部优化 (GLO)**。它们共同解决空地视角间巨大的尺度差异所引发的梯度冲突、锚点膨胀与欠优化区域问题。

### 4.1 空地联合自适应致密化 (AJAD)

空地视角的投影面积相差悬殊——航拍视图下单个高斯可能覆盖数百像素，街头视图下仅覆盖数个像素。若按标准 3DGS 的做法对所有视图的视空间位置梯度取未加权平均作为致密化判据：

$$
\frac { 1 } { | \mathcal { V } | } \sum _ { v \in \mathcal { V } } \sqrt { \left( \sum _ { p \in \mathcal { P } _ { i } ^ { v } } \frac { \partial L _ { p } ^ { v } } { \partial \mu _ { i , x } ^ { v } } \right) ^ { 2 } + \left( \sum _ { p \in \mathcal { P } _ { i } ^ { v } } \frac { \partial L _ { p } ^ { v } } { \partial \mu _ { i , y } ^ { v } } \right) ^ { 2 } } > \tau _ { \mathrm { p o s } }
$$

则航拍视图的梯度幅值将主导平均结果，使街景视图下关键细节的高斯原语难以触发致密化，反之亦然。实验直接证实了这一冲突：同时使用空地视图进行梯度累积的致密化，其渲染 PSNR 劣于仅使用单一视角类型（Table 1）。

AJAD 的因果调节变量是将梯度按各视图的**投影面积**（即贡献像素数 $|\mathcal{P}_i^v|$）加权，从而平衡不同尺度下的梯度贡献：

$$
\frac { \displaystyle \sum _ { v \in \mathcal { V } } | \mathcal { P } _ { i } ^ { v } | \cdot \sqrt { \left( \sum _ { p \in \mathcal { P } _ { i } ^ { v } } \frac { \partial L _ { p } ^ { v } } { \partial \mu _ { i , x } ^ { v } } \right) ^ { 2 } + \left( \sum _ { p \in \mathcal { P } _ { i } ^ { v } } \frac { \partial L _ { p } ^ { v } } { \partial \mu _ { i , y } ^ { v } } \right) ^ { 2 } } } { \displaystyle \sum _ { v \in \mathcal { V } } | \mathcal { P } _ { i } ^ { v } | } > \tau _ { p o s }
$$

当该加权梯度超过阈值 $\tau_{pos}$ 时，对应锚点生长出新的神经高斯。消融实验中，加入 AJAD 后 PSNR 从 25.20 提升至 25.66（Table 5），验证了投影面积加权对梯度冲突的有效缓解。

### 4.2 贡献感知锚点剪枝 (CAP)

多尺度细节捕捉导致锚点数量急剧膨胀，存储开销巨大。CAP 的目标是**保留稀疏但局部贡献大的锚点，同时剪除冗余结构**。为此，每个锚点被赋予可学习的二值掩码 $m_i \in \{0,1\}$（通过 Gumbel‑Softmax 采样），渲染方程修改为：

$$
C ( p ) = \sum _ { i = 1 } ^ { N _ { n g } } c _ { i } \cdot m _ { i } \cdot \sigma _ { i } \cdot T _ { i } , \quad T _ { i } = \prod _ { j = 1 } ^ { i - 1 } ( 1 - m _ { j } \cdot \sigma _ { j } )
$$

掩码的正则化是 CAP 的关键。与全局掩码稀疏损失 $L_{mask} = (\frac{1}{N}\sum M_i)^2$ 不同，CAP 引入**贡献加权**：首先计算每个神经高斯在单视图下的归一化贡献 $w_i^v$，再跨视图聚合为 $w_i$，最后构造正则项：

$$
L _ { m } = \frac { 1 } { k N } \sum _ { i = 1 } ^ { k N } ( 1 - w _ { i } ) m _ { i }
$$

该损失鼓励低贡献高斯将其掩码 $m_i$ 推向 0，而高贡献锚点的掩码得以保留。消融显示，CAP 在几乎无损画质下将锚点数从 9713k 降至 2785k，减少约 71%（Table 5）。与全局掩码正则化相比，CAP 在相同 PSNR 下使用更少锚点，有效保护了局部重要结构（Table 7）。

### 4.3 全局到局部优化 (GLO)

全局训练后，部分视图的 PSNR 仍存在大幅波动（最后三次记录的最大差值超过 1.0），这些视图被标记为不稳定视图。GLO 将不稳定视图作为目标视图，并寻找与其锚点重叠率超过阈值 $\tau_{group}$ 的候选视图组成局部优化组：

$$
\frac{|\mathcal{A}_{target} \cap \mathcal{A}_{candidate}|}{\min(|\mathcal{A}_{target}|, |\mathcal{A}_{candidate}|)} > \tau_{group}
$$

在局部细化阶段，冻结组外参数，仅对组内视图进行针对性训练。消融表明，GLO 将 PSNR 进一步提升至 26.05，且锚点数降至 2682k（Table 5）。与额外 20k 迭代的均匀采样训练相比，GLO 的 PSNR 增益（+0.55）远高于前者的 +0.09（Table 8），证明针对性局部优化的有效性远优于盲目延长全局训练。

### 4.4 多损失联合训练

最终训练目标整合了重建、体积正则、深度、透明度掩码与掩码正则化项：

$$
L = L_1 + \lambda_{ssim} L_{ssim} + \lambda_{vol} L_{vol} + \lambda_d L_d + \lambda_o L_o + \lambda_m L_m
$$

其中透明度掩码损失 $L_o$ 利用 2D 掩码抑制天空、车辆等动态对象区域的错误高斯，$L_m$ 即 CAP 的贡献加权掩码正则化。

## 实验与关键发现

### 核心瓶颈验证：空地视角梯度冲突

空地联合重建的核心挑战并非单纯的数据量不足，而是航拍与街拍视图间巨大的尺度差异导致的**梯度积累冲突**。标准3D高斯泼溅（3DGS）的致密化策略对所有训练视图的视空间位置梯度取未加权平均（Eq. 3），这在单尺度场景下有效，但在空地联合场景中，航拍视图下高斯原语的投影面积远小于街拍视图，导致两类视图对同一高斯的梯度贡献严重失衡，使致密化信号被主导视图“淹没”。

为验证这一假设，作者在Colosseum场景上进行了梯度来源消融实验（Table 1）：分别仅使用航拍视图梯度、仅使用街拍视图梯度和合并两类视图梯度来触发致密化。结果表明，合并梯度（Merge）的渲染质量（航拍PSNR 25.35 / 街拍PSNR 25.32）显著低于仅使用航拍梯度（航拍PSNR 25.64）或仅使用街拍梯度（街拍PSNR 25.52）的对应最优指标，直接证实了**跨尺度梯度冲突的存在**——两类视图的梯度信号在简单累加后相互抵消，导致致密化策略无法有效识别在各自尺度下具有重要贡献的高斯原语。

![[assets/figures/papers/paper_list_l2622_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Urban_GS_A_Unifie/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison across accumulating gradients for densification from aerial views only, street views only and merged views on Colosseum scene [10]. All methods are trained with 60k iterations*

进一步分析（Figure 3）揭示了冲突的机制：那些仅满足航拍致密化条件但在合并视图下被抑制的高斯，其平均投影半径较小（即主要在航拍尺度上可见），而仅满足街拍条件但被抑制的高斯则具有较大的投影半径。这表明标准致密化策略对投影面积大的视图（街拍）赋予了过高的隐式权重，系统性地压制了航拍尺度细节的生长机会。

### 关键模块消融：从冲突解决到压缩与细化

Table 5 系统展示了Urban-GS各核心模块的累积贡献。基线模型（Base）采用标准致密化策略，PSNR为25.20，但锚点数高达9713k，存在严重的冗余生长。

![[assets/figures/papers/paper_list_l2622_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Urban_GS_A_Unifie/figures/011_Table_5.jpg]]
*Table 5: Ablation on main model components. “+” means adding components in addition to all components in the above rows. “AJAD”, “CAP”, and*

**空地联合自适应致密化（AJAD）** 通过将梯度按各视图的贡献像素数 $|\mathcal{P}_i^v|$ 加权（Eq. 6），以投影面积平衡不同尺度下的梯度贡献，从根本上解决了上述冲突。添加AJAD后，PSNR从25.20跃升至**25.66**（+0.46），验证了自适应致密化对多尺度细节捕捉能力的显著提升。

**贡献感知锚点剪枝（CAP）** 在AJAD基础上引入可学习掩码和贡献加权正则化 $L_m$（Eq. 11），将锚点数从9713k**压缩至2785k**（减少约71%），而PSNR仅从25.66略降至25.50（-0.16），实现了几乎无损的高效压缩。与全局掩码正则化（MaskGaussian的 $L_{mask}$，Eq. 8）的对比（Table 7）进一步表明，CAP在相同PSNR水平下使用更少的锚点，有效保护了局部贡献大但全局稀疏的重要结构，避免了全局正则化“一刀切”剪枝对细节的破坏。

**全局到局部优化（GLO）** 在全局训练完成后，识别PSNR波动大于1.0的不稳定视图，将其分组进行局部细化（冻结无关参数）。添加GLO后，PSNR进一步提升至**26.05**（+0.39），同时锚点数进一步降至2682k。Table 8的对比消融表明，GLO带来的PSNR增益（+0.55）远超同等额外迭代次数下统一采样训练的增益（+0.09），证明**针对性局部优化**而非简单增加训练量，是提升欠优化区域质量的关键。

### 主结果：渲染质量与存储效率的双重优势

在Horizon-GS数据集上（Table 2），Urban-GS在所有场景下均取得了最优或次优的渲染质量。以Colosseum场景为例，PSNR达到**26.88**，较最强基线Horizon-GS（26.16）提升+0.72；SSIM从0.879提升至**0.890**；LPIPS从0.108降至**0.095**。在UC-GS数据集上（Table 4），Urban-GS同样表现稳健，在View+1m场景下PSNR达到**26.58**，较Horizon-GS（25.48）提升+1.10。

![[assets/figures/papers/paper_list_l2622_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Urban_GS_A_Unifie/figures/005_Table_2.jpg]]
*Table 2: Quantitative novel view rendering results comparison on Horizon-GS [10] dataset. The best performance of each part is in bold, while the scecond-best results are underlined*

在存储效率方面（Table 3），Urban-GS的锚点数较Horizon-GS**平均减少41%**（约1801k vs. 3050k），同时渲染帧率更高（Colosseum场景83.3 FPS vs. 64.7 FPS），实现了**质量-存储-速度**的协同优化。定性对比（Figure 4, 5）显示，Urban-GS在航拍视角的屋顶结构、街拍视角的立面细节等跨尺度区域均表现出更清晰的几何保真度和纹理还原。

![[assets/figures/papers/paper_list_l2622_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Urban_GS_A_Unifie/figures/006_Table_3.jpg]]
*Table 3: Efficiency comparison between our method and Horizon-GS [10] on the Horizon-GS dataset*

![[assets/figures/papers/paper_list_l2622_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Urban_GS_A_Unifie/figures/007_Figure_4.jpg]]
*Figure 4: Qualitive comparisons of Urban-GS against baselines [10, 12, 13] across scenes of Horizon-GS dataset [10]. Patches that highlight the visual differences are emphasized with red and yellow insets for clearer visibility*

### 方法谱系与知识库定位

Urban-GS继承并改进了结构化高斯表示的范式。其锚点生长机制源于**Scaffold-GS**（Lu et al., CVPR 2024）的层级锚点结构，但将致密化触发条件从均匀梯度改为投影面积加权梯度，以适配空地多尺度场景。掩码剪枝策略借鉴了**MaskGaussian**的全局稀疏正则化思想，但引入贡献感知权重，使剪枝从“全局均匀稀疏”转向“保留局部重要结构”。全局到局部优化策略与**UC-GS**（Zhang et al., arXiv 2024）的跨视角不确定性处理思路形成互补——后者通过不确定性建模指导优化，而Urban-GS通过PSNR波动直接识别欠优化视图进行分组细化。相较于**Horizon-GS**（Jiang et al., CVPR 2025）这一最直接的基线，Urban-GS在保持空地联合建模能力的同时，通过系统性的致密化-剪枝-优化协同设计，显著提升了渲染质量与存储效率。

## 定位与知识库关联

### 与基线方法的关系

Urban-GS 处于“空地联合城市场景重建”这一新兴任务线上，其最直接的基线是 **Horizon-GS**（Jiang et al., CVPR 2025），后者首次将空地多视图纳入统一的 3D Gaussian Splatting 框架。Urban-GS 在继承这一联合重建范式的同时，识别并解决了 Horizon-GS 未触及的核心瓶颈：空地视角间巨大的尺度差异导致梯度积累冲突，使得标准均匀梯度的致密化策略无法有效识别跨尺度重要的高斯原语。

在技术路线上，Urban-GS 与以下工作构成递进或对比关系：

- **3DGS**（Kerbl et al., ACM TOG 2023）：作为基础高斯泼溅方法，其致密化策略采用所有视图上未加权平均的视空间位置梯度（Eq. 3）作为触发条件。Urban-GS 的实验表明，当直接将此策略应用于空地联合训练时，混合视角下的渲染质量反而劣于仅使用单一视角类型（Table 1），这直接验证了“梯度冲突”的存在，并构成了 AJAD 模块的动机来源。

- **Scaffold-GS**（Lu et al., CVPR 2024）：作为结构化高斯表示的基线，Urban-GS 沿用了其“锚点-神经高斯”的层级表示框架，但在此基础上引入了贡献感知的掩码剪枝（CAP）和投影面积加权致密化（AJAD），以应对空地场景特有的多尺度冗余问题。

- **UC-GS**（Zhang et al., arXiv 2024）：该方法从交叉视角不确定性的角度处理空地重建，Urban-GS 在 UC-GS 数据集上与其进行了定量对比（Table 4），在 View+1m 场景下 PSNR 达到 26.58，较 Horizon-GS 的 25.48 提升 +1.10，验证了 Urban-GS 在不同数据集上的泛化能力。

- **Hier-3DGS**（Kerbl et al., ACM TOG 2024）与 **CityGaussian**（Liu et al., ECCV 2024）：前者提出层级 LOD 表示，后者面向大规模城市场景重建。Urban-GS 在致密化策略的扩展消融中与 Hier-GS、Abs-GS 进行了对比（Table 6），证明 AJAD 的投影面积加权方案优于这些替代策略。

### 关键改进槽位与因果机制

Urban-GS 相对于基线方法的核心改进可归纳为四个“因果旋钮”：

1. **致密化触发条件**：从“所有视图未加权平均梯度”改为“按各视图贡献像素数加权的平均梯度”（Eq. 3 → Eq. 6）。其因果逻辑在于：航拍视图下高斯原语的投影面积远小于街拍视图，若不加权，街拍视图的大梯度将主导致密化决策，压制航拍视角所需的细节生长。投影面积加权使不同尺度下的梯度贡献趋于平衡，从而准确触发跨尺度致密化。

2. **锚点剪枝正则化**：从“全局掩码稀疏损失”（Eq. 8, MaskGaussian 策略）改为“贡献加权的掩码正则化”（Eq. 11）。全局稀疏损失对所有锚点一视同仁，容易误删在局部视图中有重要贡献但全局出现频率低的锚点。CAP 通过计算每个神经高斯在各视图下的归一化贡献（Eq. 9-10），使低贡献高斯被鼓励剪枝，而稀疏但局部重要的锚点得以保留。

3. **优化策略**：从“单阶段全局训练”改为“全局到局部两阶段优化”（GLO）。全局训练后，通过监测 PSNR 波动识别不稳定视图（波动 >1.0），并将与这些视图共享足够锚点的候选视图组成局部优化组（Eq. 12），冻结无关参数后进行针对性细化。消融实验（Table 8）表明，GLO 带来的 PSNR 增益（+0.55）远高于同等迭代次数的额外均匀训练（+0.09），证明针对性局部优化的有效性远优于简单增加训练量。

4. **损失函数**：在标准 L1+SSIM 基础上引入体积回归、深度、透明度掩码和掩码正则化项（Eq. 14），其中透明度掩码损失（Eq. 13）专门用于抑制天空、车辆等动态对象区域的错误高斯。

### 适用边界与局限

Urban-GS 的设计假设和适用边界可从以下几个方面理解：

- **场景假设**：方法针对“空地联合城市场景”，要求输入同时包含航拍和街拍视图，且场景以静态建筑结构为主体。对于纯航拍或纯街拍场景，AJAD 的跨尺度加权优势将不再显著——Table 1 显示，仅使用单一视角类型时，航拍专用和街拍专用的致密化策略已能取得较好效果。

- **存储-质量权衡**：CAP 模块在几乎无损画质下将锚点数从 9713k 降至 2785k（约 71% 压缩），但 Table 5 显示 PSNR 从 25.66 微降至 25.50。这表明贡献感知剪枝存在轻微的质量代价，在极端存储受限的场景下需要手动调整 λ_m 超参数以平衡压缩率与渲染质量。

- **局部优化的触发条件**：GLO 依赖 PSNR 波动阈值（>1.0）来识别不稳定视图。该阈值的敏感性可能因场景而异——过于宽松会导致局部优化组过大、计算开销增加；过于严格则可能遗漏欠优化区域。论文未提供该阈值的敏感性分析，此点需要在实际部署中手动验证。

- **动态对象处理**：透明度掩码损失 L_o 依赖 2D 像素掩码来抑制动态对象区域的高斯，但论文未详细说明掩码的获取方式（如是否依赖语义分割模型）。若掩码质量不佳，可能影响对车辆、行人等动态元素的处理效果。

### 开放问题

1. **跨场景泛化的阈值敏感性**：AJAD 的致密化阈值 τ_pos 和 GLO 的不稳定视图判定阈值 τ_group 在不同城市场景（如高密度摩天大楼 vs. 低密度郊区）下的最优取值是否稳定，论文未进行跨场景的敏感性分析。

2. **贡献权重的尺度超参数**：聚合贡献权重 w_i 中引入了尺度超参数 γ_scale（Eq. 10），其物理含义和调参策略未在现有材料中充分展开，可能影响 CAP 在不同分辨率输入下的剪枝行为。

3. **与 NeRF-based 方法的对比缺失**：现有实验仅与 3DGS 系列方法对比，未纳入空地联合重建的 NeRF-based 方法（如 Urban-NeRF 系列），无法判断 Urban-GS 在渲染质量上的绝对上限。

4. **实时渲染的端侧部署**：虽然 Table 3 显示 Urban-GS 的 FPS 优于 Horizon-GS（83.3 vs. 64.7），但论文未讨论在移动端或 Web 端的部署可行性与内存占用细节，这对于“紧凑重建”这一宣称的实际落地至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/Urban_GS_A_Unified_3D_Gaussian_Splatting_Framework_for_Compact_and_High_Fidelity_Aerial_to_Street_Reconstruction.pdf]]

---
title: "WildRayZer: Self-supervised Large View Synthesis in Dynamic Environments"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WildRayZer_Self_supervised_Large_View_Synthesis_in_Dynamic_Environments.pdf
project_link: "https://wild-rayzer.cs.virginia.edu/"
code_link: null
aliases:
- WildRayZer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过分析-合成策略：利用预训练的静态渲染器RayZer预测刚性场景的外观，并利用预测残差（结合DINOv3特征和SSIM）构建伪运动掩码，进而蒸馏运动估计器并掩蔽动态令牌，使监督集中于背景补全。
primary_logic: 将静态渲染器预测与观测图像之间的残差作为运动证据，通过自监督伪掩码训练，可实现无需任何3D或动态掩码监督的前馈式动态场景新视角合成，分离静态背景与动态物体。
claims:
- 在D-RE10K和D-RE10K-iPhone上，WildRayZer一致地优于优化和基于前馈的基线方法，单次前馈即可实现更优的瞬态区域移除和全帧NVS质量。
- 在D-RE10K（4视图）上，WildRayZer取得22.38 PSNR，明显优于次优方法RayZer + SAV（20.73 PSNR），提升1.65 dB。
- 引入DINOv3特征极大加速了运动掩码的涌现并提升质量：达到mIoU=30需约20k步而不使用DINOv3，但使用DINOv3仅需1.5k步。
- D-RE10K (Views=4) 上 PSNR = 22.38
---

# WildRayZer: Self-supervised Large View Synthesis in Dynamic Environments

> [!tip] 核心洞察
> 将静态渲染器预测与观测图像之间的残差作为运动证据，通过自监督伪掩码训练，可实现无需任何3D或动态掩码监督的前馈式动态场景新视角合成，分离静态背景与动态物体。

| 字段 | 内容 |
|------|------|
| 中文题名 | WildRayZer：动态环境下的自监督大视角合成 |
| 英文题名 | WildRayZer: Self-supervised Large View Synthesis in Dynamic Environments |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10716) · [Project](https://wild-rayzer.cs.virginia.edu/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | WildRayZer |
| Dataset | D-RE10K, D-RE10K-iPhone |

> [!tip] 效果简介
> - D-RE10K (Views=4) 上，PSNR 22.38 vs 20.73 (RayZer + SAV) (+1.65)；SSIM 0.773 vs 0.711 (RayZer + SAV) (+0.062)。
> - D-RE10K-iPhone (Views=4) 上，PSNR 20.98 vs 18.86 (Spotless-Splats) (+2.12)；LPIPS 0.298 vs 0.382 (Spotless-Splats) (-0.084)。

## 概述

**核心问题**：现有的大视角新视角合成（NVS）方法，无论是基于优化的NeRF/3DGS管线还是前馈式Transformer架构，均假设场景是静态的。在真实世界的动态环境中，移动的行人、宠物、临时杂物等瞬态物体严重破坏多视图一致性，导致渲染结果出现鬼影、幻觉几何以及相机姿态估计的不稳定。关键瓶颈在于：**如何在没有任何真实动态掩码监督的条件下，可靠地定位并剔除动态区域**，从而仅从刚性背景中学习场景表示。

**核心方法**：WildRayZer提出了一种**分析-合成（analysis-by-synthesis）的自监督策略**。其核心洞察是：一个预训练的静态渲染器（RayZer）能够预测刚性场景应有的外观，而预测图像与观测图像之间的残差，恰好构成了动态物体的“运动证据”。方法流程如下：

1. 利用RayZer渲染无动态物体的背景预测，计算其与真实图像的**SSIM外观差异**和**DINOv3语义特征差异**，二者融合后经聚类与GrabCut精修，生成像素级的**伪运动掩码**。
2. 用这些伪掩码作为监督信号，训练一个**运动估计器**（Motion Estimator），使其能够在推理时直接从前馈输入中预测动态区域。
3. 在场景编码阶段，将预测为动态的图像令牌**直接置零**，使场景编码器仅从静态令牌中构建3D表示，渲染解码器据此合成无瞬态物体的新视角图像。
4. 训练采用**交替优化调度**：先冻结渲染器训练运动掩码，再冻结运动头训练遮蔽渲染器，最后联合微调；同时引入COCO对象的**复制-粘贴增强**以提升运动估计器的跨域泛化能力。

整个过程无需任何3D监督或真实动态掩码，仅依赖稀疏的无姿态多视图输入，实现单次前馈即可完成动态场景的静态新视角合成。

**方法定位**：WildRayZer属于**前馈式、无3D显式表示的自监督大视角合成方法**，直接继承自RayZer（An et al., CVPR 2024），并在此基础上新增了运动估计与动态令牌掩蔽两条关键支路。与基于优化的动态NeRF方法（如**NeRF On-the-go**, Ren et al., CVPR 2022）和动态3DGS方法（如**Spotless-Splats**、**WildGaussians**）不同，WildRayZer无需逐场景优化，单次前馈即可完成推理；与RayZer + 外部运动分割器（如**SAV**, Liang et al., CVPR 2024）的组合方案相比，WildRayZer的运动掩码与渲染器联合训练，能够更好地处理跨视图补全和全局几何保持。

**主要结果**：
- 在D-RE10K（4视图）上，WildRayZer取得**22.38 PSNR**，比次优方法RayZer + SAV（20.73 PSNR）提升**1.65 dB**；SSIM达到0.773，LPIPS降至0.290。
- 在D-RE10K-iPhone（4视图）上，PSNR达到**20.98**，比Spotless-Splats（18.86）提升**2.12 dB**；LPIPS降至0.298。
- 消融实验表明，DINOv3特征的引入将运动掩码涌现速度提升约**13倍**（从约20k步降至1.5k步达到mIoU=30）；复制-粘贴增强结合伪掩码训练，将DAVIS跨数据集泛化的mIoU从3.4提升至**31.0**。
- 定性结果显示，WildRayZer能更干净地移除瞬态物体，更好地完成跨视图背景补全，并更准确地保持全局场景几何与细粒度纹理。

**局限与开放问题**：伪运动掩码不强制实例级分割，可能仅高亮运动部位而遗漏静止部分；当运动物体占据画面过大比例时，掩码质量和背景补全能力下降。该方法对极端大遮挡、非刚性运动、户外光照变化的鲁棒性，以及能否摆脱对预训练RayZer的依赖实现端到端训练，仍是待探索的开放问题。

## 背景与动机

新视角合成（Novel View Synthesis, NVS）旨在从稀疏的多视角观测中重建三维场景，并在任意目标视角下生成逼真的图像。近年来，基于前馈的大视角合成方法（如 **RayZer**）在静态场景上取得了显著进展：它们通过大规模Transformer架构，以自监督方式从无姿态、无标定的稀疏图像中直接预测相机参数和场景表示，无需显式的NeRF或3DGS等三维表示即可实现高质量的跨视角生成。然而，这些方法的成功高度依赖于一个隐含假设——**场景是静态的**。

真实世界中的视觉数据远非静态。室内场景中走动的人、宠物，室外场景中移动的车辆，都构成了**瞬态物体**（transient objects）。当这些动态元素出现在训练视图中时，它们会从两个层面破坏现有多视图系统的核心假设：

**瓶颈一：多视图一致性被破坏。** 静态渲染器试图用单一刚体场景解释所有观测，但动态物体在不同视图间的位置变化使得这种解释在物理上不可能。强制拟合的结果是产生**鬼影**（ghosting）、**幻觉几何**（hallucinated geometry），以及背景区域的模糊或扭曲。

**瓶颈二：姿态估计不稳定。** 前馈方法通常依赖图像令牌之间的对应关系来隐式推断相机位姿。动态物体在不同视图中占据不同的图像位置，引入了错误的对应信号，导致相机估计器产生偏差甚至崩溃。

**瓶颈三：缺乏可扩展的动态场景训练数据。** 如Table 1所示，现有静态NVS数据集（如RealEstate10K）可达数万序列，而动态场景数据集通常仅有数十个序列，且依赖昂贵的优化管线逐场景处理。这种数据规模的鸿沟使得直接训练动态感知的前馈模型变得极为困难。

**瓶颈四：动态掩码监督的缺失。** 定位动态物体的最直接方式是训练一个运动分割器，但这需要像素级的真实动态掩码。在无约束的真实场景中，获取此类标注的成本极高，且难以覆盖多样化的物体类别和运动模式。

面对上述挑战，一个核心问题浮现：**能否在没有任何三维监督或动态掩码监督的情况下，从动态多视图图像中学习到静态场景的新视角合成？** WildRayZer的动机正是填补这一空白——设计一个自监督框架，使其能够自动发现并抑制动态物体，将监督信号集中于背景补全，从而在单次前馈推理中生成无瞬态物体的清晰新视角。

## 核心创新

WildRayZer 的核心创新在于**将动态场景新视角合成重构为“分析-合成”的自监督学习问题**，在不引入任何 3D 监督或真实动态掩码的条件下，实现了对动态物体的定位与去除。其区别于现有方法的关键设计体现在以下几个 changed slots 上。

### 从渲染残差中自监督发现运动

现有前馈式静态渲染器（如 RayZer）在遇到动态场景时，会因多视图一致性被破坏而产生鬼影和几何幻觉，但模型本身缺乏识别动态区域的机制。WildRayZer 的突破在于**将静态渲染器的预测误差转化为运动证据**：利用预训练 RayZer 预测刚性场景应有的外观 $\hat{I}$，然后计算 $\hat{I}$ 与观测图像 $I$ 之间的残差，这些残差天然地高亮动态区域。

具体而言，伪运动掩码构建器融合了两类互补的差异信号：
- **语义差异**：基于 DINOv3 归一化特征向量的余弦距离 $D_{\mathrm{DINO}}(p) = 1 - \langle \Phi_p(I), \Phi_p(\hat{I}) \rangle$，捕获语义层面的不一致；
- **外观差异**：基于像素级 SSIM 的结构差异 $D_{\mathrm{SSIM}}(x) = 1 - \mathrm{SSIM}(I,\hat{I})(x)$，捕获纹理和结构层面的不一致。

两者通过自适应加权融合为显著性图，再经 DINO 块特征聚类投票、形态学平滑、小分量去除和 GrabCut 细化，最终生成像素级二值运动掩码（见 Figure 3）。这一流水线**完全自监督**，无需任何人工标注的运动分割真值。

### 可学习的运动估计器与令牌门控

RayZer 的原始架构中，所有图像令牌无差别地送入场景编码器，动态区域会污染 3D 场景表示。WildRayZer 在相机估计器旁**新增一个运动估计器 $E_{\mathrm{mot}}$**，其结构与相机估计器对称：将图像令牌与 Plücker 射线令牌拼接后，通过 4 层 Transformer 进行跨视图推理，再由 DPT 风格解码器上采样输出每像素运动 logits $S(I)$。

训练时，运动估计器以伪掩码为监督目标进行蒸馏。推理时，预测的运动概率经阈值化生成二值掩码，**动态令牌在进入场景编码器前被直接置零**，使编码器仅聚合静态区域的信息。这一“预测-门控”机制将运动分离从隐式的误差容忍提升为显式的架构组件。

### 复制-粘贴增强与交替训练调度

为弥补伪掩码在训练初期的噪声，WildRayZer 引入两项训练策略创新：
- **复制-粘贴增强**：将 COCO 对象（带真实掩码）粘贴到训练视图的随机位置，合成额外的动态样例及其精确掩码，扩充伪掩码监督的信号多样性。消融实验表明，单独使用该增强无法迁移到真实视频（DAVIS mIoU 仅 3.4），但与伪掩码结合后 mIoU 跃升至 31.0（Table 5），证明两者协同作用对跨域泛化至关重要。
- **交替优化调度**：先冻结渲染器堆栈训练运动掩码，再冻结运动头训练遮蔽渲染器，最后联合微调所有组件。这一渐进策略被论文明确指出“对稳定性和可靠收敛至关重要”（confidence 0.9）。

### 与基线方法的关键差异

| 变更槽位 | RayZer（基线） | WildRayZer（本文） |
|---------|---------------|-------------------|
| 运动估计模块 | 无，仅依赖隐式误差处理 | 基于 DINOv3 和交叉注意力的 Transformer 运动估计器，以伪标签和复制-粘贴增强训练 |
| 输入令牌掩蔽 | 所有图像令牌均用于场景编码 | 根据预测运动概率阈值化后，将动态令牌置零 |
| 训练数据 | 静态 RealEstate10K | 动态 D-RE10K + COCO 复制-粘贴增强 |
| 训练调度 | 端到端训练 | 交替优化：掩码学习 → 遮蔽渲染 → 联合微调 |
| 伪掩码构建 | 无运动掩码概念 | 融合 SSIM 和 DINOv3 差异度，经聚类和 GrabCut 生成像素级二值掩码 |

这些创新使 WildRayZer 在 D-RE10K（4 视图）上取得 22.38 PSNR，较次优方法 RayZer + SAV（20.73 PSNR）提升 1.65 dB；在 D-RE10K-iPhone 上达到 20.98 PSNR，较 Spotless-Splats（18.86 PSNR）提升 2.12 dB。更重要的是，所有改进均在一次前馈推理中完成，无需对每个场景进行优化。

## 整体框架

WildRayZer 在 RayZer 静态渲染器之上引入运动感知能力，构建了一个完全自监督的动态场景新视角合成流水线。其核心设计遵循分析-合成策略：先用一个冻结的静态渲染器解释刚性背景，再将预测残差作为运动证据，驱动运动估计与掩蔽重建的联合学习。

### 输入与输出

模型接收一组无姿态、无标定的稀疏多视图动态图像 $\mathbf{I} = \{I_1, \dots, I_N\}$（通常 $N \in \{2,3,4\}$），在单次前馈中同时预测：
- 每视图的相对相机位姿 $P_i \in SE(3)$ 与共享内参 $K$；
- 每像素的运动概率图（二值化后得到动态掩码）；
- 去除瞬态物体后的静态新视角图像。

### 五大核心模块

流水线由五个功能模块串联构成，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/003_Figure_2.jpg]]
*Figure 2: WildRayZer self-supervised learning framework. (a) Training. WildRayZer takes unposed, uncalibrated multi-view dynamic images I and predicts per-view camera parameters (intrinsics and relative poses), which are converted into pixel-aligned Plucker ray maps ¨ R. A camera-only static renderer explains the rigid background; residuals between renderings*

1. **相机估计器 (Camera Estimator, $E_\text{cam}$)**：从输入图像预测每视图的刚体位姿和共享内参，并将其转换为像素对齐的 Plücker 射线图 $\ddot{R}$，为后续几何推理提供空间线索。

2. **运动估计器 (Motion Estimator, $E_\text{mot}$)**：接收图像标记、射线标记和 DINOv3 特征，通过 4 层 Transformer 进行跨视图推理，经 DPT 风格解码器上采样后输出每像素运动 logits $S(I)$。预测结果经阈值化得到二值动态掩码 $M_\text{pred}$。

3. **场景编码器 (Scene Encoder, $E_\text{scene}$)**：将输入视图的图像标记与射线标记融合后，根据运动掩码将动态区域对应的标记置零（token gating），仅保留静态标记送入 8 层 Transformer 聚合为隐式场景表示 $z$。

4. **渲染解码器 (Rendering Decoder, $D_\text{render}$)**：以场景表示 $z$ 和目标相机射线为条件，通过 8 层 Transformer 解码器合成去瞬态的新视角图像。

5. **伪掩码构造器 (Pseudo-mask Constructor)**：在训练阶段，利用冻结的静态渲染器预测 $\hat{I}$，计算其与真实图像 $I$ 之间的 SSIM 差异和 DINOv3 语义差异，经自适应加权融合、聚类投票和 GrabCut 精修，生成像素级伪运动掩码 $\tilde{M}(I)$ 作为运动估计器的监督信号。

### 训练调度

训练采用交替优化策略，分三个阶段渐进执行：
1. **掩码学习阶段**：冻结渲染器堆栈（相机估计器、场景编码器、渲染解码器），仅训练运动估计器，使其拟合伪掩码构造器产生的伪标签。
2. **掩蔽渲染阶段**：冻结运动估计器，训练场景编码器和渲染解码器，使渲染损失仅作用于静态区域（通过掩蔽 MSE 实现）。
3. **联合微调阶段**：解冻所有组件进行端到端微调，损失函数结合掩蔽重建损失与运动掩码的二值交叉熵。

这种分级训练策略对稳定性和收敛至关重要——直接端到端训练会导致运动掩码和渲染质量同时崩溃。

### 数据流与增强

训练数据为 D-RE10K 的 15K 动态室内序列。为提升运动估计器的泛化能力，引入复制-粘贴增强：将 COCO 对象按真实掩码粘贴到训练视图中，其掩码直接作为额外的伪运动标签 $\tilde{M}(I)$。这一简单策略使模型在跨数据集（如 DAVIS）上的运动掩码 mIoU 从 3.4 跃升至 31.0。

输入视图的所有标记沿序列维度拼接，使运动估计器能够利用多视图一致性区分相机运动与物体运动——这是单视图方法无法实现的关键能力。

### 补充图表

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/001_Figure_1.jpg]]
*Figure 1: Our self-supervised WildRayZer learns to render static novel views from dynamic images without any 3D or GT mask supervision. It extends the state-of-the-art self-supervised large view synthesis model RayZer to dynamic environments by adding a learned motion mask estimator and a masked 3D scene encoder*

## 核心模块与公式推导

### 1. 伪运动掩码构建器（Pseudo‑Motion Mask Constructor）

这是 WildRayZer 实现“分析‑合成”自监督的核心模块，其目标是从静态渲染器 RayZer 的预测残差中，无监督地提取动态物体的像素级二值掩码，为后续的运动估计器提供监督信号。

**输入**：原始多视图动态图像 $I$ 与 RayZer 静态渲染器输出的预测图像 $\hat{I}$。

**构建流程**（对应 Figure 3）：

1. **语义差异图**：利用预训练的 DINOv3 对 $I$ 和 $\hat{I}$ 分别提取逐块（patch）的 L2‑归一化特征向量 $\Phi_p(I)$ 与 $\Phi_p(\hat{I})$，计算余弦距离得到语义差异图：

   $$D_{\mathrm{DINO}}(p) = 1 - \langle \Phi_p(I), \Phi_p(\hat{I}) \rangle$$

   该图对纹理平坦但语义不一致的动态区域（如移动的人体）高度敏感。

2. **外观差异图**：计算像素级结构相似性差异：

   $$D_{\mathrm{SSIM}}(x) = 1 - \mathrm{SSIM}(I, \hat{I})(x)$$

   该图对纹理变化敏感，但对语义变化不敏感。

3. **自适应融合显著性图**：将两种差异图分别进行 Z‑score 标准化后加权融合：

   $$D_{\mathrm{bin}}(p) = w_{\mathrm{DINO}} \mathcal{Z}(D_{\mathrm{DINO}}(p)) + w_{\mathrm{SSIM}} \mathcal{Z}(D_{\mathrm{SSIM}}(p))$$

   权重 $w_{\mathrm{DINO}}$ 和 $w_{\mathrm{SSIM}}$ 根据各差异图的动态范围自适应调整，以避免某一模态主导。

4. **块级掩码投票**：对 DINO patch 特征进行聚类，以聚类中心投票方式生成粗粒度的块级动态掩码。

5. **像素级精细化**：通过形态学平滑、小连通域去除和 GrabCut 将粗掩码精化为像素级二值伪掩码 $\tilde{M}(I)$。

**关键机制**：该模块不依赖任何真实动态掩码监督，完全利用静态渲染器的“预测‑观测”残差作为运动证据。其瓶颈在于：当动态物体占据过大画面比例或纹理极弱时，伪掩码质量会显著下降。

---

### 2. 运动估计器（Motion Estimator $E_{\text{mot}}$）

运动估计器是一个基于 Transformer 的前馈模块，其目标是从输入图像直接预测逐像素的运动概率，从而在推理时无需再运行昂贵的伪掩码构建流程。

**架构**：与 RayZer 的相机估计器并列放置，由 4 层 Transformer 组成。输入为图像 tokens 和 Plücker 射线 tokens 的拼接序列，通过跨视图注意力实现多视图信息交互。输出经 DPT 风格解码器上采样至 $H \times W$，得到每像素的 logits $S(I)$。

**训练监督**：使用伪掩码构建器生成的 $\tilde{M}(I)$ 作为目标，以二值交叉熵损失进行蒸馏。同时引入 COCO 对象的复制‑粘贴增强：将带真实掩码的 COCO 物体粘贴到训练视图上，其掩码直接作为额外的伪标签 $\tilde{M}(I)$，显著提升了跨数据集的泛化能力（DAVIS 上 mIoU 从 3.4 提升至 31.0，见 Table 5）。

**推理时的作用**：将 $S(I)$ 阈值化为二值掩码，用于门控输入 tokens——动态 tokens 在进入场景编码器前被置零，从而将监督信号集中于静态背景补全。

---

### 3. 掩蔽场景编码器与渲染器

**输入门控**：经运动估计器预测的二值掩码标记为动态的图像块，其融合 tokens 在馈入场景编码器 $E_{\text{scene}}$ 前被直接置零。这迫使编码器仅从静态 tokens 中构建 3D 场景隐式表示 $z$。

**掩蔽渲染损失**：在计算渲染损失时，同样使用伪掩码 $\tilde{M}(I)$ 对动态像素进行门控，仅计算静态区域的 MSE：

$$\mathrm{MSE}_M = \frac{\sum_{i,j} (I_{ij} - \hat{I}_{ij})^2 M_{ij}}{\sum_{i,j} M_{ij}}$$

其中 $M_{ij}$ 为二值掩码在像素 $(i,j)$ 处的值。该设计避免了动态像素对光度损失的污染。

**渲染解码器** $D_{\text{render}}$ 保持与 RayZer 相同的 Transformer 解码器结构（8 层），根据场景表示 $z$ 和目标相机射线合成新视角图像。

---

### 4. 训练调度与联合损失

WildRayZer 采用交替优化策略以保证训练的稳定性和收敛：

1. **阶段一**：冻结渲染器堆栈（$E_{\text{cam}}$, $E_{\text{scene}}$, $D_{\text{render}}$），仅训练运动估计器 $E_{\text{mot}}$，使其学习伪掩码。
2. **阶段二**：冻结运动估计器，训练掩蔽场景编码器和渲染器，使其学会从静态 tokens 中重建背景。
3. **阶段三**：联合微调所有组件。

联合训练的总损失为：

$$\mathcal{L} = \mathcal{L}_{\text{masked}} + \lambda_{\text{mask}} \cdot \mathrm{BCE}(M_{\text{pred}}, M_{\text{target}})$$

其中 $\mathcal{L}_{\text{masked}}$ 为掩蔽重建损失（结合 MSE 和感知损失），第二项为运动掩码的二值交叉熵损失。

---

### 5. 关键公式速查

| 公式 | 含义 | 所在章节 |
|------|------|----------|
| $\mathcal{L} = \frac{1}{|\mathcal{T}_{\mathcal{B}}|} \sum_{\hat{I}} \big( \mathrm{MSE}(I,\hat{I}) + \lambda \mathrm{Percep}(I,\hat{I}) \big)$ | RayZer 静态渲染自监督损失 | Sec 4.1 |
| $D_{\mathrm{DINO}}(p) = 1 - \langle \Phi_p(I), \Phi_p(\hat{I}) \rangle$ | DINOv3 语义差异图 | Sec 4.2 |
| $D_{\mathrm{SSIM}}(x) = 1 - \mathrm{SSIM}(I, \hat{I})(x)$ | SSIM 外观差异图 | Sec 4.2 |
| $D_{\mathrm{bin}}(p) = w_{\mathrm{DINO}} \mathcal{Z}(D_{\mathrm{DINO}}(p)) + w_{\mathrm{SSIM}} \mathcal{Z}(D_{\mathrm{SSIM}}(p))$ | 自适应融合显著性 | Sec 4.2 |
| $\mathrm{MSE}_M = \frac{\sum_{i,j} (I_{ij} - \hat{I}_{ij})^2 M_{ij}}{\sum_{i,j} M_{ij}}$ | 掩蔽 MSE 损失 | Supp B.2 |
| $\mathcal{L} = \mathcal{L}_{\text{masked}} + \lambda_{\text{mask}} \cdot \mathrm{BCE}(M_{\text{pred}}, M_{\text{target}})$ | 联合训练总损失 | Supp Eq.2 |

### 补充图表

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/004_Figure_3.jpg]]
*Figure 3: Pseudo Motion Mask Pipeline. We fuse SSIM- and DINO-based dissimilarity into a saliency map, cluster DINO patch features to vote for dynamic patches, then refine the coarse patch mask to pixel resolution via morphological smoothing, smallcomponent removal, and GrabCut [65]*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/011_Figure_6.jpg]]
*Figure 6: Examples of Copy–paste mask augmentation. We inject synthetic transient objects (e.g., animals, household items, vehicles) into static RE10K scenes to simulate dynamic elements in otherwise static environments*

## 实验与分析

### 核心实验设置

WildRayZer 的训练与评估在两个互补的数据集上进行：**D-RE10K** 和 **D-RE10K-iPhone**。D-RE10K 包含约 15K 个真实室内动态序列，涵盖人物、宠物、杂物等多样化瞬态物体，填补了动态场景大规模训练数据的空白（见表 1）。D-RE10K-iPhone 则提供手持拍摄的真实世界动态场景，用于验证方法的实际部署能力。

模型采用 28 层 Transformer 架构：运动估计器 4 层，相机估计器、场景编码器和渲染解码器各 8 层。训练使用 768 个场景令牌，学习率 $4 \times 10^{-4}$，余弦调度，共 100k 次迭代，批大小为 64。所有基线方法均在相同的 2–4 视图稀疏输入协议下重新评估，确保公平对比。对于 D-RE10K，主要图像质量指标仅计算在静态区域上，以排除动态物体的不公平影响；D-RE10K-iPhone 则报告全图保真度。

### 主要结果

表 2 汇总了在 2、3、4 个输入视图下的平均性能。WildRayZer 在 D-RE10K 和 D-RE10K-iPhone 上一致优于所有优化型和前馈型基线方法。

**D-RE10K（4 视图，仅静态区域）：**
- WildRayZer 取得 **22.38 PSNR**，显著优于次优方法 RayZer + SAV（20.73 PSNR），提升 **+1.65 dB**。
- SSIM 达到 **0.773**，相比 RayZer + SAV（0.711）提升 +0.062。
- LPIPS 降至 **0.290**，表明感知质量亦有明显改善。

**D-RE10K-iPhone（4 视图，全图保真度）：**
- WildRayZer 取得 **20.98 PSNR**，大幅领先 Spotless-Splats（18.86 PSNR），提升 **+2.12 dB**。
- LPIPS 为 **0.298**，相比 Spotless-Splats（0.382）降低 0.084。

定性结果（图 4）进一步验证了这些数值优势：WildRayZer 更干净地移除瞬态物体，更好地处理跨视图补全（对比 RayZer + SAV 基线），并更忠实地保留全局场景几何（如厨房结构）和细粒度细节（如植物叶片）。在 DAVIS 数据集上的泛化测试（图 5）表明，即使面对未见过的户外场景，WildRayZer 仍能有效掩蔽瞬态物体。

### 运动掩码质量分析

运动掩码的质量直接决定了背景补全的上限。表 4 对比了监督式和自监督式运动分割方法在稀疏视图设置下的表现。WildRayZer 的自监督运动估计器在不同输入视图数量下均取得更高的 **mIoU** 和 **Recall**，证明了伪掩码蒸馏策略的有效性。

图 7 的可视化对比进一步揭示了关键差异：基于联合分割（Co-segmentation）、MegaSAM、Segment Any Video（SAV）和 VideoCutler 等现成方法在稀疏多视图条件下往往产生碎片化或不完整的运动掩码，而 WildRayZer 的预测掩码更连贯、更完整。这归因于其运动估计器通过多视图令牌的交叉注意力机制隐式地利用了多视图一致性。

### 消融实验

**DINOv3 特征的关键作用。** 引入 DINOv3 特征极大加速了运动掩码的涌现并提升其质量。实验表明，不使用 DINOv3 时，达到 mIoU=30 需要约 20k 训练步；而使用 DINOv3 仅需 **1.5k 步**，加速超过 13 倍。DINOv3 提供的语义级差异图有效补充了 SSIM 的外观级差异，使伪掩码构造器能更可靠地定位动态区域。

**复制-粘贴增强的泛化贡献。** 表 5 的消融实验显示：单独的 COCO 对象复制-粘贴增强在真实视频上的迁移效果有限（DAVIS mIoU 仅 3.4）。然而，当与伪掩码结合使用时，跨数据集泛化能力显著提升，DAVIS 上的 mIoU 从 3.4 跃升至 **31.0**。这表明复制-粘贴增强为运动估计器提供了多样化的合成动态样例，而伪掩码则提供了真实场景的自监督信号，二者协同作用。

**分级训练策略。** 交替优化调度对训练的稳定性和收敛至关重要：先冻结渲染器堆栈学习运动掩码，再冻结运动头学习掩蔽渲染器，最后联合微调所有组件。直接端到端训练会导致运动掩码和渲染质量的双重退化。

### 失败模式与局限性

尽管 WildRayZer 展现出强大的动态场景处理能力，但分析揭示了几类典型失败案例（图 8）：

1. **部分运动掩码：** 伪运动掩码不强制实例级分割，可能仅高亮运动部分而遗漏静止部分。例如，当人物主体运动时，掩码可能只覆盖躯干而遗漏脚部等较小区域。
2. **大物体遮挡：** 当瞬态物体占据图像过大比例时，掩码质量下降，且背景补全可能不完整——预测掩码往往小于实际物体区域。
3. **户外泛化有限：** 虽然在 DAVIS 上展示了初步泛化能力，但模型在户外复杂光照和大幅外观变化下的鲁棒性仍需进一步验证。
4. **对预训练 RayZer 的依赖：** 当前方法需要预训练的 RayZer 作为初始化，增加了训练流程的复杂性，且静态渲染器的质量上限约束了动态处理的潜力。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| 表 2 | WildRayZer 在 D-RE10K（+1.65 dB PSNR）和 D-RE10K-iPhone（+2.12 dB PSNR）上均显著超越最强基线 |
| 图 4 | 定性上更干净地移除瞬态物体，跨视图补全和几何保留更优 |
| 表 4 | 自监督运动掩码在稀疏视图下的 mIoU 和 Recall 超越现成监督/自监督分割方法 |
| 表 5 | 复制-粘贴增强 + 伪掩码联合使用使 DAVIS mIoU 从 3.4 提升至 31.0 |
| 图 8 | 失败模式：部分掩码、大物体遮挡、背景补全不完整 |

### 补充图表

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/005_Table_2.jpg]]
*Table 2: Main Results on Novel View Synthesis. We report mean performance for 2, 3, 4 input views on D-RE10K (left, static regions only) and D-RE10K-iPhone (right, full-image fidelity). Metrics are PSNR ↑, SSIM ↑, and LPIPS ↓. Cells highlighted in red, orange, and yellow denote the best, second, and third results respectively. SAV denotes Segment Any Motion in Videos [21]*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons. Qualitative results on DRE10K-Mask (top two rows) and DRE10K-iPhone (bottom row). Compared to baselines, our method (1) more cleanly removes transient objects, (2) better handles cross-view completion (compare with RayZer + SAV baseline), and (3) better preserves global scene geometry (e.g., kitchens) and fine details (e.g., plants). SLS denotes Splotless-Splats [67]*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/008_Table_4.jpg]]
*Table 4: Motion-mask quality. Comparison of supervised and self-supervised motion segmentation methods under sparse-view settings. WildRayZer achieves higher mIoU and recall across different numbers of input views*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/010_Table_5.jpg]]
*Table 5: Copy–Paste Ablation. Copy–paste alone does not transfer to real videos but improves out-of-domain generalization when combined with pseudo-masks*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative Results. (1) First row: D-RE10K (no ground-truth novel views). (2) Second row: D-RE10K-iPhone. (3) Third and fourth rows: additional NVS results on DAVIS [54], where ground truth is also unavailable, demonstrating that WildRayZer generalizes to outdoor scenes and can mask unseen transient objects*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/002_Table_1.jpg]]
*Table 1: Common datasets for novel view synthesis. “Large?” marks datasets with ≥10K sequences. Static NVS datasets are large, but dynamic ones are typically tiny. D-RE10K closes this gap with 15K real, in-the-wild and dynamic indoor sequences featuring diverse transient objects (people, pets, clutter), enabling training for transient-aware NVS at scale*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/014_Figure_9.jpg]]
*Figure 9: Additional qualitative results. We show 12 extra examples to illustrate WildRayZer’s behavior across datasets. The first three rows are from D-RE10K, the next two rows demonstrate generalization to the unseen DAVIS dataset [55], and the last row shows additional real-world results on D-RE10K-iPhone*

![[assets/figures/papers/paper_list_l2630_https_arxiv_org_abs_2601_10716/figures/013_Figure.jpg]]
*Figure: Predicted Motion Mask*

## 方法谱系与知识库定位

### 1. 方法谱系：从静态渲染到动态解耦

WildRayZer 的核心技术路径建立在**前馈式静态大视角合成**的基础上，通过引入自监督运动解耦机制，将适用边界从纯静态场景拓展至动态环境。其谱系可沿两条轴线梳理：

**轴线一：静态大视角合成基座。**
WildRayZer 直接以 **RayZer** (An et al., CVPR 2024) 为预训练初始化。RayZer 是一个基于 Transformer 的自监督大视角合成模型，能够从无姿态的稀疏多视图输入中预测相机参数并合成新视角。其核心损失为渲染图像与真值之间的 MSE 和感知损失：

$$\mathcal{L} = \frac{1}{|\mathcal{T}_{\mathcal{B}}|} \sum_{\hat{I} \in \hat{\mathcal{T}}_{\mathcal{B}}} \big( \mathrm{MSE}(I,\hat{I}) + \lambda \mathrm{Percep}(I,\hat{I}) \big)$$

RayZer 的设计前提是多视图一致性，即所有输入视图共享同一刚性场景。这一前提在动态场景中被破坏，导致鬼影、幻觉几何和姿态估计不稳定——这正是 WildRayZer 所要解决的核心瓶颈。

**轴线二：动态场景新视角合成方法。**
在动态 NVS 领域，主流方法可分为两类：基于优化的方法和基于前馈的方法。

基于优化的方法以 **NeRF On-the-go** (Weining Ren et al., CVPR 2022)、**3DGS** (Kerbl et al., ACM Trans. Graph., 2023) 及其动态扩展（T-3DGS、Spotless-Splats、WildGaussians）为代表。这些方法通常需要为每个场景单独优化，依赖多视图一致性假设或手工设计的正则项来分离动态与静态成分。在稀疏视图（2-4 视图）设置下，优化型方法面临严重的欠约束问题，性能受限。

基于前馈的方法试图通过端到端学习直接预测新视角，但现有工作大多假设静态场景。WildRayZer 是少数将前馈式渲染与动态解耦结合的工作，其关键创新在于**无需任何 3D 监督或真实动态掩码**即可实现动态区域的识别与抑制。

### 2. 知识库定位：核心创新与增量贡献

WildRayZer 的知识贡献可分解为以下四个增量槽位：

| 槽位 | 基线值（RayZer） | 提出值（WildRayZer） | 证据强度 |
|------|------------------|---------------------|---------|
| 运动估计模块 | 无（仅依赖隐式误差处理） | 基于 DINOv3、图像标记和射线标记的 Transformer 运动估计器，用伪标签和复制-粘贴增强训练 | 强（Table 4 消融验证） |
| 输入令牌掩蔽策略 | 所有图像令牌均用于场景编码 | 根据预测的运动概率二值掩码，将动态令牌置零 | 强（Table 2 主结果支持） |
| 伪掩码构建 | 无 | 融合 SSIM 和 DINOv3 差异度，通过聚类和 GrabCut 生成像素级运动掩码 | 强（Figure 3 流程 + 消融） |
| 训练调度 | 端到端训练 | 交替优化：冻结渲染器训练掩码 → 冻结掩码训练渲染器 → 联合微调 | 中（论文声称对稳定性关键） |

**伪掩码构建**是 WildRayZer 最具原创性的知识贡献。其核心洞察在于：预训练静态渲染器的预测残差本身就是运动证据。具体而言，对于输入图像 $I$ 和静态渲染器的预测 $\hat{I}$，构建两种差异图：

$$D_{\mathrm{DINO}}(p) = 1 - \langle \Phi_p(I), \Phi_p(\hat{I}) \rangle$$

$$D_{\mathrm{SSIM}}(x) = 1 - \mathrm{SSIM}(I,\hat{I})(x)$$

两者通过自适应加权融合为显著性图 $D_{\mathrm{bin}}(p)$，再经 DINO patch 特征聚类投票和 GrabCut 精修，生成像素级二值运动掩码。这一分析-合成策略使得运动定位完全自监督，无需任何人工标注。

**DINOv3 特征的引入**被证明是伪掩码质量的关键杠杆：消融实验显示，不使用 DINOv3 时需要约 20k 训练步才能达到 mIoU=30，而使用 DINOv3 仅需 1.5k 步——加速超过 13 倍。

### 3. 与竞争方法的边界对比

在实验对比中，WildRayZer 与以下方法构成了直接竞争关系：

- **RayZer + SAV** (Liang et al., CVPR 2024)：将 Segment Any Motion in Videos 作为外部运动分割模块接入 RayZer。在 D-RE10K（4 视图）上取得 20.73 PSNR，WildRayZer 以 22.38 PSNR 领先 1.65 dB。这一对比直接验证了端到端学习运动掩码优于外部冻结分割器的策略。

- **RayZer + Co-Seg** (An et al., CVPR 2024)：基于冻结特征联合分割的方法，性能低于 WildRayZer，说明联合优化的运动估计器比冻结特征聚类更有效。

- **RayZer + MegaSAM**：基于 Segment Anything 的运动分割，在稀疏视图下泛化能力受限。

- **Spotless-Splats**：基于优化的 3DGS 方法，在 D-RE10K-iPhone（4 视图）上取得 18.86 PSNR，WildRayZer 以 20.98 PSNR 领先 2.12 dB。这表明即使在真实手机拍摄数据上，前馈式方法也能超越逐场景优化的 3DGS 变体。

值得注意的是，**D-RE10K 上的图像质量指标仅在静态区域计算**，以排除动态物体对评估的不公平影响。这一评估协议确保了对比的公正性。

### 4. 适用边界与局限

WildRayZer 的适用边界受以下因素制约：

**（1）运动掩码的粒度限制。** 伪运动掩码不强制实例级分割，可能仅突出物体的运动部分而遗漏静止部分（如站立人物的脚部）。Figure 8 的失败案例显示，当运动物体占据图像过大比例时，掩码质量下降且背景补全不完整。

**（2）对预训练 RayZer 的依赖。** WildRayZer 需要预训练的静态 RayZer 作为初始化，增加了训练流程的复杂性。这限制了该方法在全新领域（如户外大规模场景）的直接迁移。

**（3）户外场景泛化。** 尽管在 DAVIS 数据集上展示了初步泛化能力，但模型主要在室内 D-RE10K 上训练，对户外光照变化、复杂动态模式的鲁棒性仍需进一步验证。

**（4）复制-粘贴增强的局限性。** Table 5 的消融显示，单独的复制-粘贴增强（Copy-Paste Only）在 DAVIS 上的 mIoU 仅 3.4，必须结合伪掩码才能提升至 31.0。这表明合成增强无法独立替代真实动态场景的学习信号。

### 5. 开放问题

基于当前工作的局限，以下问题值得后续研究关注：

- **极端遮挡场景**：当瞬态物体占据大部分视场时，静态渲染器的预测残差可能无法提供足够的背景信息用于补全。能否引入生成式先验来处理此类情况？

- **非刚性运动与可变形物体**：当前方法假设动态区域可通过刚性场景的残差来识别，对于可变形物体（如飘扬的衣物、流动的水面），这一假设可能失效。如何扩展至非刚性运动建模？

- **去预训练化**：能否消除对预训练 RayZer 的依赖，实现从零开始的端到端训练？这将显著降低方法的使用门槛。

- **光照变化鲁棒性**：在户外场景中，光照变化可能导致静态渲染器产生系统性残差，被误判为运动。如何解耦光照变化与物体运动？

- **时序一致性**：当前方法逐帧独立处理，未利用时序信息。引入时序约束可能进一步提升运动掩码的稳定性和背景补全的质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/WildRayZer_Self_supervised_Large_View_Synthesis_in_Dynamic_Environments.pdf]]
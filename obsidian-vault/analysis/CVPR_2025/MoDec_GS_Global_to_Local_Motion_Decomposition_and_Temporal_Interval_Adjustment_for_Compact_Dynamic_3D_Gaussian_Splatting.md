---
title: "MoDec-GS: Global-to-Local Motion Decomposition and Temporal Interval Adjustment for Compact Dynamic 3D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adjustment_for_Compact_Dynamic_3D_Gaussian_Splatting.pdf
project_link: https://kaist-viclab.github.io/MoDecGS-site/
code_link: null
aliases:
- MG
- MoDec-GS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将运动分解为全局和局部两级，分别利用全局锚点变形（GAD）捕捉大尺度刚性运动，利用局部高斯变形（LGD）细化细节运动，并引入时间间隔自适应调整（TIA）动态分配每个局部规范空间（Local CS）的时间覆盖范围，使得在紧凑的模型容量下能够精确表达复杂运动，从而大幅降低存储需求并保持或提升渲染质量。"
primary_logic: "全局运动主要由物体的整体刚性位移构成，因而变形稀疏的锚点即可高效表示；局部运动则体现为每个高斯的小幅变化，在全局变形之后已经简化，可通过显式变形重建的高斯来捕获。将运动分解后，每个Local CS仅需处理简化后的局部运动，同时TIA根据训练中位置梯度自动收缩运动复杂的时间段，保证每个局部模型的表达能力得到最有效利用，避免了因配给不当导致的容量浪费或模糊。"
claims:
- "在iPhone数据集上，MoDec-GS相比质量第二好的SC-GS，PSNR提升0.7 dB，同时存储减少94%。"
- "在HyperNeRF数据集上，MoDec-GS取得最高PSNR (27.78 dB) 和 SSIM (0.827)，存储仅为SC-GS的18%。"
- "消融实验表明，GAD可将存储减少52%且基本不影响质量；添加LGD和TIA后模型达到最优性能（PSNR 14.60，存储18.37 MB）。"
- "TIA可视化显示，时间区间从均匀分布变为非均匀，与归一化光流运动幅度一致，证明了自适应调整的有效性。"
---

# MoDec-GS: Global-to-Local Motion Decomposition and Temporal Interval Adjustment for Compact Dynamic 3D Gaussian Splatting

> [!tip] 核心洞察
> 全局运动主要由物体的整体刚性位移构成，因而变形稀疏的锚点即可高效表示；局部运动则体现为每个高斯的小幅变化，在全局变形之后已经简化，可通过显式变形重建的高斯来捕获。将运动分解后，每个Local CS仅需处理简化后的局部运动，同时TIA根据训练中位置梯度自动收缩运动复杂的时间段，保证每个局部模型的表达能力得到最有效利用，避免了因配给不当导致的容量浪费或模糊。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MoDec-GS：面向紧凑动态3D高斯泼溅的全局-局部分解运动与时间间隔调整 |
| 英文题名 | MoDec-GS: Global-to-Local Motion Decomposition and Temporal Interval Adjustment for Compact Dynamic 3D Gaussian Splatting |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.03714) · [Project](https://kaist-viclab.github.io/MoDecGS-site/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoDec-GS |
| Dataset | Dycheck-iPhone [16], HyperNeRF interp - Cut-lemon [49], HyperNeRF Average (interp) [49] |

> [!tip] 效果简介
> - Dycheck-iPhone [16] 上，Average mPSNR↑ 为 14.60，对比 13.90 (SC-GS)，变化 +0.70。
> - Dycheck-iPhone [16] 上，Average Storage (MB)↓ 为 18.37，对比 232.4 (SC-GS)，变化 -214.03 (约-92%)。
> - HyperNeRF interp - Cut-lemon [49] 上，PSNR↑ 为 31.08，对比 30.17 (4DGS)，变化 +0.91。

## 概要

真实世界视频中的动态场景同时包含**全局刚性运动**与**局部非刚性变形**，现有动态3D Gaussian Splatting（3DGS）方法——如**4DGS**、**Deformable 3DGS**、**SC-GS**——难以在模型存储开销与渲染质量之间取得平衡：单一变形场或固定时间分段策略无法有效同时捕捉两类运动，导致大运动或长序列中出现模糊，而增大模型则带来难以承受的存储代价。

针对这一瓶颈，本文提出 **MoDec-GS**，核心思路是**全局-局部分解运动（Global-to-Local Motion Decomposition, GLMD）**：将复杂运动拆解为两级——先通过**全局锚点变形（Global Anchor Deformation, GAD）** 捕捉大尺度刚性运动，再通过**局部高斯变形（Local Gaussian Deformation, LGD）** 细化细节运动。同时引入**时间间隔自适应调整（Temporal Interval Adjustment, TIA）**，在训练中根据位置梯度动态分配每个局部规范空间的时间覆盖范围，使有限模型容量得到最有效利用。

主要实验结果：
- 在 **Dycheck-iPhone** 数据集上，MoDec-GS 相较质量第二的 SC-GS，PSNR 提升 **0.7 dB**，同时存储减少 **94%**（18.37 MB vs 232.4 MB）。
- 在 **HyperNeRF** 数据集上取得最高 PSNR（**27.78 dB**）和 SSIM（**0.827**），存储仅为 SC-GS 的 18%。
- 在 **Nvidia monocular** 数据集上，PSNR 达到 **26.65 dB**，比 4DGS 高出 **1.19 dB**。
- 消融实验证实：GAD 可将存储减少约 52% 且基本不影响质量；加入 LGD 和 TIA 后模型达到最优性能；两阶段变形仅带来约 0.9 FPS 的微小渲染速度下降，保持了实时渲染能力。

MoDec-GS 在**方法谱系**上继承并改进了锚点式 3DGS 表示（Scaffold-GS），将静态锚点扩展为动态规范骨架，并通过两级 hexplane 变形场与可学习锚点动态参数，实现了紧凑且表达力强的动态场景建模。其局限性在于，对单目视频中薄且高细节纹理的物体（如 HyperNeRF 的 broom 场景）表示能力仍有限，这是当前基于 3DGS 方法的共有挑战。



### 动态场景重建的存储与质量困境

三维高斯泼溅（3D Gaussian Splatting, 3DGS）在静态场景的新视角合成中取得了显著成功，但其向动态场景的扩展面临根本性挑战。现有动态3DGS方法——如**4DGS**、**Deformable 3DGS**和**SC-GS**——在真实世界视频中遭遇一个核心瓶颈：**全局刚性运动与局部非刚性变形往往同时存在且相互叠加**，而单一变形场或固定的时间分段策略难以同时高效捕捉这两种性质迥异的运动模式。

具体而言，这一瓶颈表现为三个相互制约的矛盾：

1. **容量与质量的失衡**：较大的模型（如使用密集高斯变形或复杂时变表示）虽能部分缓解模糊问题，却带来巨大的存储开销。例如SC-GS在iPhone数据集上的模型存储高达232.4 MB，严重限制了实际部署。

2. **全局与局部的耦合**：全局运动（如相机平移、物体整体位移）涉及大尺度刚性变换，局部运动（如表情变化、细微形变）则体现为每个高斯原语的小幅非刚性调整。单一变形场被迫同时建模这两种运动，导致在大运动场景中出现渲染模糊，而在细节区域又缺乏足够的表达精度。

3. **固定分段的低效**：现有方法或采用等长时间分段，或依赖外部运动幅度进行固定划分，无法根据场景的真实运动复杂度自适应分配模型容量。运动剧烈的短时段与运动平缓的长时段被分配相同的表示资源，造成容量浪费或表达能力不足。

### 核心动机：分解与自适应

MoDec-GS的出发点在于一个关键洞察：**全局运动主要由物体的整体刚性位移构成，变形稀疏的锚点即可高效表示；局部运动则体现为每个高斯的小幅变化，在全局变形已被剥离之后，这些残余运动已被显著简化。** 这意味着，若能将运动分解为全局和局部两级，分别用不同粒度的表示来处理，就有可能在紧凑的模型容量下实现精确的复杂运动建模。

基于这一思想，MoDec-GS提出两个核心机制：

- **全局-局部分解运动（GLMD）**：通过Global Anchor Deformation（GAD）捕捉大尺度刚性运动，通过Local Gaussian Deformation（LGD）细化残余的局部运动，形成从粗到精的两阶段变形管线。

- **时间间隔自适应调整（TIA）**：在训练过程中根据位置梯度动态收缩运动复杂的时间段，使每个Local Canonical Scaffold的时间覆盖范围与场景的运动复杂度相匹配，避免均匀分段造成的容量浪费。

### 预期目标

通过上述设计，MoDec-GS旨在实现一个三赢目标：**在显著降低模型存储的同时保持或提升渲染质量，并维持实时渲染能力**。初步实验表明，在iPhone数据集上MoDec-GS相比质量第二好的SC-GS，PSNR提升0.7 dB，同时存储减少94%（从232.4 MB降至18.37 MB），验证了这一技术路线的可行性。



## 核心方法与创新机理

MoDec-GS 的核心创新围绕一个关键瓶颈展开：现有动态 3DGS 方法在处理真实世界视频中全局刚性运动与局部非刚性变形的组合时，难以在模型存储容量与渲染质量之间取得平衡。单一变形场或固定分段策略无法有效同时捕捉两种尺度的动态，导致在大运动或长序列中出现模糊，而增大模型则带来难以承受的存储开销。MoDec-GS 通过三个相互协同的“changed slots”系统性地解决了这一问题。

### 1. 两阶段全局-局部分解运动（GLMD）

与 4DGS、Deformable 3DGS、SC-GS 等主流方法采用的单一显式高斯变形策略不同，MoDec-GS 提出 **Global-to-Local Motion Decomposition (GLMD)**，将运动分解为两级处理（Fig. 2, Sec. 4.1）：

- **Global Anchor Deformation (GAD)**：利用一个小型全局 hexplane $H_G$ 直接变形稀疏锚点的位置和属性，将 Global Canonical Scaffold（Global CS）变换到对应时间段的 Local CS，高效捕捉大尺度刚性运动。其核心洞察在于：全局运动主要由物体的整体刚性位移构成，变形稀疏的锚点即可高效表示，无需对每个高斯逐一变形。消融实验表明，将基线方法从直接高斯变形切换为锚点变形（GAD），存储减少约 52%，而 PSNR 仅轻微下降（14.29 → 14.12），验证了锚点变形对全局运动的高效性（Tab. 3）。

- **Local Gaussian Deformation (LGD)**：在全局变形已经简化运动之后，使用共享的局部 hexplane $H_L$ 显式变形 Local CS 重建出的神经高斯至目标时间戳，捕捉剩余的局部细微运动。添加 LGD 后，PSNR 从 14.12 提升至 14.48，SSIM 从 0.460 提升至 0.478，表明分解后的局部运动被有效捕捉（Tab. 3）。

完整的 GLMD（GAD + LGD）相比仅使用单一阶段的变形均获得更好的 PSNR（14.48），说明全局-局部分解是必要的。运动分解的可视化（Fig. 9）进一步证实：GAD 阶段变形主要集中在具有主导运动的物体附近（如柠檬和刀），整体光流方向趋于一致；而 LGD 阶段运动遍布整个场景，方向更为多样。

### 2. 训练内自适应时间间隔调整（TIA）

现有方法采用固定等长时间段或依赖外部运动幅度进行分段，缺乏对场景运动复杂度的自适应能力。MoDec-GS 提出 **Temporal Interval Adjustment (TIA)**，将时间分段直接集成到训练过程中（Sec. 4.4, Algo. 1）：

- 在每个时间区间 $c$ 内累积位置梯度的 Frobenius 范数 $g_c^{\text{acc}}$，以此评估该区间的运动复杂度。
- 当某个区间的累积梯度超过阈值（$\mu + \tau_{\text{TIA}} \cdot \sigma$），自动收缩该区间的时间跨度，将释放的时间容量分配给相邻区间。

TIA 的效果是决定性的：添加 TIA 后，最终模型 PSNR 从 14.48 提升至 14.60，SSIM 达 0.480，LPIPS 为 0.443，且未增加存储（Tab. 3）。TIA 的可视化（Fig. 5）显示，时间区间从均匀分布变为非均匀分布，与归一化光流运动幅度高度一致，证明了自适应调整的有效性。

### 3. 基于锚点的规范空间表示与可学习动态

MoDec-GS 采用 Scaffold-GS 的锚点表示替代典型 3DGS 的逐高斯属性存储（Sec. 3.2, Sec. 4.2）：稀疏锚点存储隐含特征，通过 MLP 生成多个神经高斯的属性。在此基础上，引入可学习的 **Anchor Dynamics**：

- **全局动态参数 $d_G$**：通过 sigmoid 阈值二值化产生软掩码 $M(d_G)$，决定是否对锚点应用全局变形，实现运动区域的自适应选择（Eq. 6）。
- **局部动态参数 $d_L$**：通过 sigmoid 缩放控制局部变形量，实现局部运动的可控融合（Eq. 7）。

这种设计使得模型能够自动学习哪些锚点参与全局运动、哪些需要进一步的局部细化，避免了手工设定运动区域的局限性。

### 创新协同效应

三个创新点形成因果闭环：GLMD 将复杂运动分解为全局和局部两级，降低了每级的建模难度；锚点表示与可学习动态使全局变形高效且自适应；TIA 则根据实际运动复杂度动态优化每个 Local CS 的时间覆盖范围，确保模型容量被最有效利用。三者共同实现了在紧凑模型下精确表达复杂运动的目标——在 iPhone 数据集上，MoDec-GS 相比质量第二的 SC-GS，PSNR 提升 0.7 dB，同时存储减少 94%；在 HyperNeRF 数据集上取得最高 PSNR（27.78 dB）和 SSIM（0.827），存储仅为 SC-GS 的 18%（Tab. 1, Tab. 2）。

值得注意的是，两阶段变形仅带来微小的推理速度下降（约 0.9 FPS，从 24.7 降至 23.8），保持了实时渲染能力（Tab. 7），验证了该设计方案在实际部署中的可行性。



![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results comparison on three datasets [16, 49, 64]. The yellow boxes highlight areas where the proposed method achieves notable visual quality improvements, and the storage for the corresponding sequence is displayed below each rendered patch*

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/001_Figure_1.jpg]]
*Figure 1: Novel view synthesis results on [49]. We introduce MoDec-GS, a novel framework for learning compact dynamic 3D Gaussians from real-world videos with complex motion. While existing SOTA methods [21, 60, 63] have difficulty modeling such complex combination of global and local motions, our approach effectively handles them thanks to GLMD (Sec. 4.1), and outperforms the prior methods in rendering quality even with a compact model size. The metrics under each framework are, PSNR (dB)↑ / LPIPS [65] ↓ / Storage (MB)↓*

MoDec-GS 的整体 pipeline 围绕“全局-局部分解运动”（Global-to-Local Motion Decomposition, GLMD）展开，将动态场景的复杂运动建模拆分为两个串行阶段，并辅以训练期间的自适应时间间隔调整（Temporal Interval Adjustment, TIA），从而在紧凑的模型容量下实现高质量渲染。其核心流程如图 2 所示，包含以下关键模块与数据流：

1. **全局规范 Scaffold（Global CS）**  
   首先在所有训练帧上训练一个静态的锚点规范表示（基于 Scaffold-GS）。该 Global CS 存储稀疏锚点及其隐含特征，作为后续全局运动变形的起点。

2. **全局锚点变形（Global Anchor Deformation, GAD）**  
   利用一个小型全局 hexplane $H_G$，将 Global CS 中每个锚点的位置和属性变形到对应时间段的局部规范空间（Local CS）。此阶段主要捕捉场景中的大尺度刚性运动（如物体的整体位移）。变形过程受可学习的“锚点动态”参数 $d_G$ 控制：通过阈值二值掩码 $M(d_G)$ 决定是否对特定锚点施加全局变形，从而实现选择性运动建模。

3. **局部规范 Scaffold（Local CS）**  
   GAD 输出的变形后锚点构成 Local CS，每个 Local CS 负责一个特定时间段的表示。Local CS 通过神经高斯派生（neural Gaussian derivation）从锚点特征重建出 3D 高斯原语。

4. **局部高斯变形（Local Gaussian Deformation, LGD）**  
   使用一个共享的局部 hexplane $H_L$ 和 MLP 解码器，对 Local CS 重建出的每个神经高斯进行显式变形，将其映射到目标时间戳 $t_L$。由于全局运动已被 GAD 剥离，此阶段仅需处理简化后的局部细微运动（如非刚性变形），变形量由可学习的局部动态参数 $d_L$ 经 sigmoid 缩放后融合。

5. **时间间隔调整（TIA）**  
   在训练过程中，TIA 动态管理各 Local CS 的时间覆盖范围。初始时段时间区间均匀分配；随着训练进行，TIA 累积每个区间内位置梯度的 Frobenius 范数 $g_c^{\mathrm{acc}}$，并据此评估运动复杂度。对于梯度积累高于阈值（$\mu + \tau_{\mathrm{TIA}} \cdot \sigma$）的区间，TIA 通过调整规范时间列表 $T_c$ 收缩其时间跨度，使运动复杂的片段获得更细粒度的局部模型表达，而运动简单的片段则分配更宽的时间区间，从而最大化模型容量的利用效率。

**输入输出流总结**：输入为单目视频的时间戳和相机参数；Global CS 提供静态锚点表示，经 GAD 变形为 Local CS，再经 LGD 变形为目标时刻的 3D 高斯；最终通过可微光栅化渲染出对应视角的图像。TIA 在训练期间持续优化各 Local CS 的时间边界，无需外部运动数据。



MoDec-GS 的核心设计思想是将复杂动态场景的运动分解为全局与局部两个层级，并通过自适应的时间分段策略实现紧凑建模。其系统架构包含以下关键模块。

### 全局锚点变形（GAD）

全局运动主要表现为物体的整体刚性位移，因此直接在稀疏锚点层面进行变形比逐高斯变形更高效。GAD 模块使用一个小型全局六平面（global hexplane）$H_G$ 对 Global CS 中每个锚点 $v$ 的位置与属性进行变形：

$$
\Delta f_v = \varphi_f [ F_G ( H_G ( x_v, y_v, z_v, t_c ) ) ]
$$

其中 $H_G$ 以锚点位置 $(x_v, y_v, z_v)$ 和规范时间 $t_c$ 为输入，输出局部上下文特征；$F_G$ 为轻量 MLP，$\varphi_f$ 为特征头。变形后的锚点位置由可学习的锚点动态参数 $d_G$ 控制是否应用变形：

$$
M(d_G) = \mathrm{sg}( \mathscr{T} [ \sigma(d_G) > \epsilon ] - \sigma(d_G) ) + \sigma(d_G)
$$

$$
x_{v'}, y_{v'}, z_{v'} = (x_v, y_v, z_v) + M(d_G) \cdot (\Delta x, \Delta y, \Delta z)
$$

$M(d_G)$ 通过 sigmoid 阈值二值化产生软掩码，$\mathrm{sg}$ 为停止梯度算子，$\epsilon$ 为阈值。锚点特征更新由局部动态参数 $d_L$ 缩放变形量：

$$
f_{v'} = f_v + \Delta f \cdot \sigma(d_L)
$$

### 局部高斯变形（LGD）

经 GAD 变形后，Local CS 重建出的神经高斯仅需处理简化后的局部运动。LGD 使用共享的局部六平面 $H_L$ 对每个神经高斯进行显式变形，以位置变形为例：

$$
\Delta x_k, \Delta y_k, \Delta z_k = \varphi_p [ F_L ( H_L ( x_k, y_k, z_k, t_L ) ) ]
$$

其中 $(x_k, y_k, z_k)$ 为第 $k$ 个神经高斯的位置，$t_L$ 为目标时间戳，$F_L$ 为 MLP 解码器，$\varphi_p$ 为位置头。其他属性（旋转、缩放等）的变形采用相同机制。

### 时间间隔自适应调整（TIA）

TIA 在训练过程中动态优化每个 Local CS 的时间覆盖范围，使运动复杂的区间获得更短的时间段以集中表达能力。具体地，在每个时间区间 $c$ 内累积位置梯度的 Frobenius 范数：

$$
g_c^{\mathrm{acc}} = g_c^{\mathrm{acc}} + g_t^{pos}
$$

同时记录累积次数 $\nu_c^{\mathrm{acc}} = \nu_c^{\mathrm{acc}} + 1$。当达到预设迭代后，根据统计量 $\mu$ 和 $\sigma$ 判断是否收缩区间：若某区间的归一化梯度超过阈值 $\mu + \tau_{TIA} \cdot \sigma$，则将其边界向内收缩步长 $s_{TIA}$，相邻区间相应扩展（详见 Algorithm 1）。

### 渲染基础

神经高斯的属性通过锚点特征和视角相关位移预测：

$$
\{ \mathrm{attr}_{v,0}, \ldots, \mathrm{attr}_{v,k-1} \} = F_{\mathrm{att}}( \hat{f}_v, \delta_{v,\mathrm{cam}}, \overrightarrow{\mathbf{d}}_{v,\mathrm{cam}} )
$$

神经高斯中心由锚点位置加可学习偏移得到：$\mathbf{m}_i = \mathbf{x}_v + \mathbf{o}_i$。投影到屏幕空间的协方差矩阵为 $\Sigma' = J^T W^T \Sigma W J$，像素颜色由 alpha 混合计算：

$$
C = \sum_{i=1}^{n} c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)
$$

### 模块间的因果机制

GAD 与 LGD 的分工具有明确的因果逻辑：全局刚性运动在锚点层面被高效吸收后，残存的局部运动幅度小且方向分散，恰好适合逐高斯的显式变形。消融实验证实了这一设计的有效性——单独使用 GAD 可将存储减少约 52% 而质量仅轻微下降；加入 LGD 后 PSNR 从 14.12 提升至 14.48；再叠加 TIA 后达到最终 14.60 PSNR，且未增加存储（Table 3）。两阶段变形仅带来约 0.9 FPS 的微小推理开销（Table 7）。



## 实验与关键发现

### 核心结果：质量与存储的双重突破

MoDec-GS 在三个主流动态场景基准上均取得了渲染质量与模型紧凑性的显著提升，验证了全局-局部分解运动（GLMD）与时间间隔自适应调整（TIA）的有效性。

在 **Dycheck-iPhone 数据集**上，MoDec-GS 以仅 **18.37 MB** 的平均存储取得了 **14.60 dB** 的 mPSNR，相比此前质量最优的 SC-GS（13.90 dB, 232.4 MB），PSNR 提升 0.7 dB，存储减少约 92%（Table 1）。这一结果直接回应了论文的核心瓶颈——在真实手机视频的复杂运动（全局晃动+局部变形）下，以往方法要么牺牲质量换取紧凑模型，要么以巨大存储为代价维持渲染精度，而 MoDec-GS 首次同时实现了最优质量和最小模型。

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/004_Table_1.jpg]]
*Table 1: Quantitative results comparison on the iPhone datasets [16]. Red and blue denote the best and the second best performances, respectively. Each block element of 4-performance denotes (mPSNR(dB)↑ / mSSIM↑ / mLPIPS↓ Storage(MB)↓)*

在 **HyperNeRF 数据集**上，MoDec-GS 取得 27.78 dB PSNR 和 0.827 SSIM，均优于 SC-GS（26.95 dB, 0.806）和 4DGS（26.86 dB, 0.803），存储仅 40.82 MB，约为 SC-GS 的 18%（Table 2-a）。在 **Nvidia 单目数据集**上，MoDec-GS 以 26.65 dB PSNR 超越 4DGS（25.46 dB）达 1.19 dB，存储 39.64 MB（Table 2-b）。值得注意的是，HyperNeRF 的 cut-lemon 场景中 PSNR 达到 31.08 dB，比 4DGS 高出 0.91 dB，该场景包含刀具与柠檬的大幅相对运动，恰好体现了 GLMD 对全局刚性与局部非刚性混合运动的处理优势。

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/006_Table_2.jpg]]
*Table 2: Quantitative results comparison on (a) HyperNeRF [49] and (b) Nvidia monocular [64] dataset. Table 3. Ablation studies on MoDec-GS components. Each row evaluates the impact of a specific design choice. Yellow-green cells highlight configurations with substantial storage reduction*

**渲染速度**方面，两阶段变形仅带来微小的 FPS 下降（HyperNeRF vrig 数据集上从 24.7 降至 23.8 FPS，Table 7），保持了实时渲染能力。综合来看，MoDec-GS 在 PSNR-FPS-存储的三维权衡中占据帕累托前沿（Figure 7 气泡图）：位于高 PSNR、高 FPS、小气泡（低存储）区域。

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/011_Table_7.jpg]]
*Table 7: Rendering speed comparison between 1-stage and 2- stage deformation of our method*

### 消融实验：各组件的因果贡献

Table 3 的系统消融揭示了 GLMD 各阶段与 TIA 的独立作用链条：

**从直接高斯变形到锚点变形（GAD）**：将基线方法（直接变形每个高斯）改为基于 Scaffold-GS 的锚点变形后，存储从 38.07 MB 骤降至 18.29 MB（减少约 52%），而 mPSNR 仅从 14.29 微降至 14.12（Table 3-a vs 3-b）。这证实了核心洞察：全局运动主要由物体整体刚性位移构成，变形稀疏锚点即可高效表示，无需逐高斯变形。

**引入局部高斯变形（LGD）**：在 GAD 基础上添加 LGD 后，mPSNR 从 14.12 回升至 14.48，mSSIM 从 0.460 提升至 0.478（Table 3-c）。这表明全局变形后的残差局部运动虽然幅度小，但通过显式变形重建的高斯仍能被有效捕捉。仅使用 LGD 而无 GAD 的配置（Table 3-d）性能明显更差，证明两级分解的必要性：先全局后局部的顺序不可颠倒。

**TIA 的自适应增益**：在完整 GLMD 基础上加入 TIA，最终模型 mPSNR 从 14.48 进一步提升至 14.60，mSSIM 达 0.480，且存储不变（Table 3-g vs 3-f）。Figure 5 的可视化提供了机制解释：TIA 将初始均匀的时间区间（黑色虚线）重新分配为非均匀区间（蓝色实线），收缩方向与归一化光流运动幅度一致——运动复杂的时段获得更窄的时间窗口，使得每个 Local CS 仅需处理简化后的运动，避免了容量浪费或欠拟合。

**超参数敏感性**：Table 8 显示，默认的 hexplane 大小、voxel 大小和 Noffset 设置在质量与存储间取得了最佳平衡，方法对超参数选择具有一定鲁棒性。

### 运动分解的可视化验证

Figure 9 对 cut-lemon 场景的光流可视化直接揭示了 GLMD 的工作机制。在 GAD 阶段，变形主要集中在具有主导运动的物体附近（柠檬和刀具），整体光流颜色趋势相似，表明捕捉到的是方向一致的全局刚性运动。而在 LGD 阶段，运动遍布整个场景，方向更加多样，对应局部细节的微调。这种清晰的运动分工是 MoDec-GS 以紧凑模型实现高精度渲染的结构性原因。

### 失败模式与局限

尽管 MoDec-GS 在多数场景中表现优异，但在 HyperNeRF 的 broom 场景中出现明显模糊（Figure 10）。该场景包含薄而高细节纹理的扫帚，模型无法充分表示其精细几何与纹理。这是当前基于 3DGS 方法的共有局限——高斯原语对细薄结构的表达能力不足。论文计划未来通过整合纹理/alpha 映射或层次金字塔特征来增强表示能力。

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/018_Figure_10.jpg]]
*Figure 10: Failure case: HyperNeRF-broom. In the face of challenges in reconstructing dynamic scenes from monocular video, there are limitations in adequately representing thin and highly intricate textured objects*

### 公平性说明

训练与渲染速度比较中，MoDec-GS 使用 RTX A6000 GPU，而对比方法（如 4DGS）使用 RTX 3090，两者内存带宽存在差异（Table 4 caption 已声明）。虽不影响质量与存储的核心结论，但速度对比的精确量化需在相同硬件上进一步验证。

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/009_Table_4.jpg]]
*Table 4: Performance comparison with a NeRF-extension framework, including training and rendering speed. Averaged over 536×960 HyperNeRF’s vrig datasets [49]. The performance numbers of [11, 19, 26, 48, 49] are sourced from [60]. The training times and run times reported in [60] were measured on an NVIDIA RTX 3090 GPU, while our framework was tested on an RTX A6000 GPU. Please note that the A6000 GPU has approximately 20 % lower memory bandwidth compared to that of the RTX 3090*

### 补充图表

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/003_Figure.jpg]]
*Figure: canonical time ???? Anchor at Global CS Anchor deformation to Local CS for modeling global motion Gaussian deformation for modeling local motion \label {eq:dynamics masking} x_{v'},y_{v'},z_{v'} = (x_v, y_v, z_v)& + M(d_G)\cdot (\Delta x,\Delta y,\Delta z) \\ f_{v'} f_v &+ \Delta f \cdot \sigma (d_L), o_{v'} o_v o s_{v'} s_v s (d_L). resenting a complex motion of 3D Gaussians,a global movement over time intervals can be more effciently handled through deformation of anchor itself.In contrast,subtle motions of individual 3D Gaussians within a time interval can be effectively addressed by explicit deformation of each Gaussian*

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/012_Table_5.jpg]]
*Table 5: Performance comparison on D-NeRF dataset. The results were averaged over all sequences in the dataset, and the values for the comparison method were taken from [25]*

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/013_Table_6.jpg]]
*Table 6: Performance comparison on PanopticSports dataset. Results for the comparison method were sourced from [22]*

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/014_Table.jpg]]

![[assets/figures/papers/paper_list_l10_MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adju/figures/016_Table_9.jpg]]
*Table 9: Quantitative results comparison on (a) iPhone [16], (b) HyperNeRF [49], (c) Nvidia [64] datasets. Red and blue denote the best and second best performances, respectively. Each block element of 5-performance denotes (PSNR(dB)↑ / SSIM↑ [59] / LPIPS↓ [65] / tOF↓ [7] Storage(MB)↓). For iPhone dataset, the masked metrics are used. For Nvidia monocular dataset, tOF values are not computed since the test views are sparsely distributed along the temporal axis*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

MoDec-GS 切入的是动态3D高斯泼溅（Dynamic 3DGS）在真实世界单目视频重建中的核心矛盾：**模型存储容量与渲染质量之间的失衡**。现有主流方法在处理包含全局刚性运动与局部非刚性变形组合的复杂运动时，面临两类典型困境：

- **单一变形场方法**（如 **Deformable 3DGS** [63]、**4DGS** [60]）使用一个全局变形场同时捕捉所有尺度的运动，导致在大幅度运动或长序列中出现模糊，难以同时兼顾全局位移与局部细节。
- **固定分段策略方法**（如 **SC-GS** [21]）虽然将时间轴划分为多个局部模型，但采用均匀分段或外部运动先验，无法根据场景的实际运动复杂度自适应分配模型容量，造成简单时段浪费容量、复杂时段容量不足。

MoDec-GS 的因果调节旋钮在于：**将运动分解为全局和局部两级，并让时间分段在训练中自适应调整**。这一设计使得每个局部规范空间（Local CS）仅需处理经全局变形简化后的残余局部运动，同时 TIA 机制自动将模型容量集中于运动复杂的时段，从而在紧凑的模型尺寸下实现高精度渲染。

### 2. 方法谱系中的位置

MoDec-GS 在动态场景表示的方法谱系中处于以下交叉位置：

**（1）相对于显式变形方法的改进**

以 4DGS 为代表的显式变形方法，直接用 hexplane 对每个高斯原语进行位移预测。MoDec-GS 继承了 hexplane 作为时空编码器的设计，但将其拆分为两级：一个轻量全局 hexplane 用于锚点级变形，一个共享局部 hexplane 用于高斯级变形。这种分解使得全局 hexplane 仅需捕捉稀疏锚点的大尺度运动，参数规模大幅缩减——消融实验表明，仅将显式高斯变形替换为锚点变形（GAD），存储即减少约 52%，而 PSNR 仅从 14.29 降至 14.12（Tab. 3）。

**（2）相对于基于锚点表示方法的拓展**

MoDec-GS 基于 **Scaffold-GS** [40] 的锚点-神经高斯架构，但将其从静态场景拓展到动态视频重建。关键创新在于为锚点引入了**可学习的锚点动态参数**（Anchor Dynamics）：全局动态参数 $d_G$ 通过阈值二值掩码决定锚点是否参与全局运动，局部动态参数 $d_L$ 通过 sigmoid 缩放控制局部变形的幅度。这使得原本仅编码静态几何的锚点特征获得了运动感知能力。

**（3）相对于时间分段方法的创新**

此前的时间分段方法（如 Shaw et al.）依赖外部光流估计来预先确定分段边界。MoDec-GS 的 TIA 机制首次将时间分段**嵌入训练过程**：通过累积各时段内位置梯度的 Frobenius 范数来评估运动复杂度，并在训练中动态收缩高梯度区间的长度。Fig. 5 的可视化证实，调整后的非均匀时间区间与归一化光流运动幅度高度吻合，验证了 TIA 无需外部运动数据即可自适应定位运动复杂时段的能力。

### 3. 适用边界与局限

**已验证的有效场景：**

- 包含显著全局刚性运动与局部细节变形的真实世界单目视频（iPhone 数据集、HyperNeRF 数据集、Nvidia 单目数据集）
- 需要紧凑模型存储的应用场景：在 iPhone 数据集上，MoDec-GS 相比质量第二的 SC-GS 存储减少 94%，同时 PSNR 提升 0.7 dB（Tab. 1）；在 HyperNeRF 数据集上，存储仅为 SC-GS 的 18%（Tab. 2-(a)）

**已知局限：**

1. **薄结构和高细节纹理的表示能力不足**：在 HyperNeRF 的 broom 场景中，模型对薄且纹理复杂的物体（如扫帚刷毛）渲染结果模糊（Fig. 10）。这是当前基于 3DGS 方法的共有局限，源于高斯原语对细长几何结构的表达能力有限。

2. **训练时间较长**：两阶段变形和 TIA 的自适应调整增加了训练开销。虽然推理阶段仅带来约 0.9 FPS 的微小下降（Tab. 7），训练效率仍有优化空间。

3. **GPU 公平比较待完善**：当前 MoDec-GS 使用 RTX A6000 GPU，而对比方法（如 4DGS）使用 RTX 3090，两者内存带宽存在差异，作者声明未来将进行相同硬件的公平比较（Tab. 4 caption）。

### 4. 开放问题

1. **高斯原语的表达能力增强**：如何在保证实时渲染的前提下，通过整合纹理/alpha 映射、广义指数函数或层次金字塔特征来增强对精细纹理和复杂几何细节的表示能力，是 MoDec-GS 未来改进的明确方向。

2. **多视角与长序列扩展**：当前方法针对单目视频设计，能否扩展到多视角同步输入或更长的视频序列，同时保持模型的紧凑性，是一个有待验证的问题。

3. **TIA 超参数的自适应**：TIA 训练中使用的阈值 $\tau_{TIA}$ 和步长 $s_{TIA}$ 是否对数据敏感，能否实现完全自适应的调整，尚需进一步研究。

4. **训练效率优化**：是否可以通过分阶段优化（如先冻结全局变形后精调局部变形）来压缩训练时间，是一个具有工程价值的开放方向。



## 原文 PDF

![[paperPDFs/CVPR_2025/MoDec_GS_Global_to_Local_Motion_Decomposition_and_Temporal_Interval_Adjustment_for_Compact_Dynamic_3D_Gaussian_Splatting.pdf]]

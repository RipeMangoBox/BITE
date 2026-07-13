---
title: "OMG-Avatar: One-shot Multi-LOD Gaussian Head Avatar"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OMG_Avatar_One_shot_Multi_LOD_Gaussian_Head_Avatar.pdf
project_link: null
code_link: null
aliases:
- OA
- OMG-Avatar
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将全局-局部特征提取与网格细分过程解耦：在低分辨率网格（5023顶点）上仅执行一次交叉注意力，随后通过逐步细分和投影采样获取局部特征，并利用深度缓冲筛选可见顶点以实现遮挡感知融合；同时独立建模头部与肩部区域，最终由神经优化器增强细节。
primary_logic: 提出统一的多细节层次（LOD）单样本高斯头像框架。核心在于只在初始低分辨率网格上进行昂贵的注意力操作，并通过粗到细的细分高效扩展特征空间，结合深度缓冲引导的局部特征遮罩融合全局语义与局部细节，同时通过多区域分解提高头像完整性。
claims:
- OMG-Avatar在VFHQ数据集上的自重建PSNR达22.72，SSIM 0.831，LPIPS 0.091，均优于所有基线方法。
- "低分辨率LOD（Sub#1，约29K高斯点）性能已超过LAM（80K点）和GAGAvatar（180K点）。"
- 去除局部特征导致身份一致性CSIM从0.869骤降至0.429。
- 去除神经优化器使PSNR从22.72下降至21.42，并丢失牙齿等动态细节。
---

# OMG-Avatar: One-shot Multi-LOD Gaussian Head Avatar

> [!tip] 核心洞察
> 提出统一的多细节层次（LOD）单样本高斯头像框架。核心在于只在初始低分辨率网格上进行昂贵的注意力操作，并通过粗到细的细分高效扩展特征空间，结合深度缓冲引导的局部特征遮罩融合全局语义与局部细节，同时通过多区域分解提高头像完整性。

| 字段 | 内容 |
|------|------|
| 中文题名 | OMG-Avatar：单图多细节层次高斯头部头像 |
| 英文题名 | OMG-Avatar: One-shot Multi-LOD Gaussian Head Avatar |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01506) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | OMG-Avatar |
| Dataset | VFHQ, HDTF |

> [!tip] 效果简介
> - VFHQ 上，PSNR（自重建） 22.72（Ours Sub#2） vs 22.65（LAM） (+0.07)；LPIPS（自重建） 0.091（Ours Sub#2） vs 0.109（LAM） (-0.018)。
> - HDTF 上，PSNR（自重建） 24.14（Ours Sub#2） vs 23.43（LAM） (+0.71)；CSIM（跨重建） 0.886（Ours Sub#2） vs 0.849（LAM） (+0.037)。
> - 推理效率 上，FPS（A100，基于神经渲染的方法） 85.94（Ours Sub#2） vs 22.70（GPAvatar） (+约63（约3.8×）)。

## 概要

**核心问题**：现有单图3D头像重建方法在计算效率与细节层次可控性上存在显著瓶颈。以GAGAvatar、LAM为代表的方案在高分辨率网格上执行交叉注意力，其计算成本随细分级别指数增长；同时，这些方法普遍缺乏对肩部等非头部区域的有效建模，导致高斯点冗余、推理速度慢且头像不完整。

**方法定位**：OMG-Avatar提出统一的多细节层次（Multi-LOD）单样本高斯头部头像框架。其核心策略是将昂贵的全局注意力操作与网格细分过程解耦——仅在初始低分辨率网格（约5K顶点）上执行一次交叉注意力，随后通过粗到细的逐步细分和投影采样高效获取局部特征，并利用深度缓冲引导的遮挡感知融合机制（OAFF）整合全局语义与局部细节。此外，通过多区域分解独立建模头部与肩部，提升头像完整性。

**关键结论**：
- 在VFHQ数据集上，OMG-Avatar自重建PSNR达22.72，LPIPS为0.091，均优于所有基线方法（表1）。
- 最低细节层次（Sub#1，仅约29K高斯点）性能已超越LAM（80K点）和GAGAvatar（180K点），验证了粗到细策略的高效性。
- 推理效率达85.94 FPS（A100），较GPAvatar提升约3.8倍；训练成本仅约200 GPU小时，较LAM降低90%以上（表6）。
- 消融实验证实：去除局部特征导致身份一致性CSIM从0.869骤降至0.429；去除神经优化器使PSNR下降至21.42并丢失动态细节（表4，图4）。

**局限与展望**：模型依赖FLAME先验和精确3DMM跟踪，大角度旋转（>±60°）下出现明显伪影；性能在2级细分后趋于饱和，受限于DINOv2特征图分辨率。未来可探索更高分辨率特征提取器及多视角数据融合以突破当前瓶颈。

### 单图3D头像重建的效率困境

从单张肖像图像重建可驱动的3D头像，是数字人、虚拟现实和远程通信等应用的核心技术。近年来，基于3D高斯泼溅（3DGS）的单图前馈方法（如GAGAvatar、LAM）显著提升了重建速度与渲染质量，但其在计算效率与细节层次可控性上仍存在明显瓶颈。

**核心瓶颈在于高分辨率网格上的交叉注意力计算**。现有方法通常在高分辨率网格（例如LAM在约80K顶点上）直接执行交叉注意力，以获取全局语义特征。然而，该操作的计算复杂度随细分级别指数增长（见Eq. (13)），导致训练与推理成本急剧上升——LAM的训练成本高达约2600 GPU小时。同时，固定分辨率的特征提取策略使得模型无法在推理时动态调整细节层次（LOD），迫使所有应用场景承担相同的计算开销，即便在低算力设备或实时场景下也缺乏灵活性。

### 局部细节与全局语义的融合难题

单图头像重建的另一关键挑战在于，如何从二维图像中同时捕获驱动所需的全局身份语义和渲染所需的局部纹理细节。现有方法通常将二者混为一体处理，缺乏对遮挡区域的显式建模：当面部顶点因姿态变化被自遮挡时，从图像平面采样的局部特征可能引入错误的外观信息，导致跨身份重演时出现身份漂移或纹理伪影。此外，多数方法未对非头部区域（如肩部）进行独立建模，导致生成的头像在颈部以下区域不完整或与头部割裂。

### 本文动机与核心思路

针对上述问题，OMG-Avatar提出了**统一的多细节层次（LOD）单样本高斯头像框架**，其核心设计原则是“将昂贵的全局注意力与廉价的局部采样解耦，并通过粗到细的细分策略实现效率与质量的平衡”。

具体而言，该方法仅在初始低分辨率网格（约5K顶点）上执行一次交叉注意力，随后通过逐步Loop细分将顶点数扩展至29K（Sub#1）或约80K（Sub#2），并利用投影采样从DINOv2特征图中高效获取局部细节。这种“粗到细”策略使得低分辨率LOD（Sub#1，仅29K高斯点）的性能已超越LAM（80K点）和GAGAvatar（180K点），同时将训练成本降低90%以上（约200 GPU小时）。在此基础上，深度缓冲引导的遮挡感知特征融合模块（OAFF）仅融合可见顶点的局部特征，有效抑制了自遮挡区域的错误信息；独立的多区域建模则通过分割掩码预测肩部高斯参数，提升了头像的完整性。最终，UNet风格的神经优化器对粗渲染结果进行细节增强，使模型在VFHQ数据集上达到22.72 PSNR和0.091 LPIPS，均优于所有基线方法。

这一设计使得OMG-Avatar在单张A100 GPU上实现85.94 FPS的实时重演，同时支持推理时动态选择LOD级别，为不同算力场景提供了灵活的效率-质量权衡。

## 核心方法与创新机理

OMG-Avatar 的核心创新在于将**全局-局部特征提取与网格细分过程彻底解耦**，从而以极低的计算开销实现多细节层次（multi-LOD）的可控高斯头部头像重建。与现有单图方法（如 GAGAvatar、LAM）在高分辨率网格上直接执行昂贵的交叉注意力不同，OMG-Avatar 仅在初始低分辨率网格（5023 顶点）上计算一次交叉注意力，随后通过**粗到细的逐步细分**和**投影采样**高效扩展特征空间，配合**深度缓冲引导的遮挡感知融合**，在显著降低计算复杂度的同时，实现了对非头部区域（肩部）的完整建模。

### 1. 特征提取与网格细分解耦

现有方法（如 LAM）在约 80K 顶点的高分辨率网格上直接计算交叉注意力，计算复杂度随细分级别 $k$ 呈指数增长：

$$O ( l \cdot h \cdot 4^{k} \cdot V_{0} \cdot N_{\mathrm{DINO}} \cdot d_{\mathrm{head}} )$$

OMG-Avatar 将这一昂贵的注意力操作限定在 $k=0$ 级（细分前），仅处理 5023 个顶点。全局特征 $F_{global}^{GS_0}$ 在此阶段一次性提取，随后通过 MLP 和 Loop 细分逐步细化：

$$F_{global}^{GS_{k+1}}, V_{k+1} = \Delta(\Phi_k(F_{global}^{GS_k}), V_k), \quad 0 \le k \le K$$

局部特征则通过**层次化投影采样（HPFS）**独立获取：将各细分层级的顶点投影到图像平面，在 DINOv2 特征图上进行双线性采样：

$$F_{local}^{GS_k} = \mathrm{Sampling}(\mathrm{P}(V_k), F_{local}), \quad 0 \leq k \leq K$$

这种解耦设计使得 OMG-Avatar 的训练成本仅约 **200 GPU 小时**，相比 LAM 的约 2600 GPU 小时**降低 90% 以上**（表 6）。

### 2. 遮挡感知特征融合（OAFF）

简单融合全局与局部特征会引入被遮挡顶点的噪声。OMG-Avatar 提出**深度缓冲引导的遮挡感知特征融合**，通过比较顶点深度 $z_i$ 与渲染深度缓冲 $\hat{z}_i$ 生成二元可见性掩码：

$$M_i^{GS_k} = \begin{cases} 1, & \mathrm{if } z_i = \hat{z}_i \\ 0, & \mathrm{if } z_i > \hat{z}_i \end{cases}$$

仅可见顶点的局部特征被保留，与全局特征相加得到融合表示：

$$F_h^{GS_k} = F_{global}^{GS_k} + F_{local}^{GS_k} \odot M^{GS_k}$$

消融实验表明，去除局部特征导致身份一致性 CSIM 从 0.869 **骤降至 0.429**（表 4），证实了遮挡感知局部特征对身份保持的关键作用。

### 3. 多区域分解建模

现有方法通常忽略肩部区域或依赖完整前向模型，导致头像不完整。OMG-Avatar 通过图像分割掩码 $M_s$ 和特征平面独立预测肩部高斯参数：

$$c_s, o_s, s_s, r_s, O_s = \mathrm{Flatten}(\mathrm{Conv}(F_{local}^{GS}) \odot M_s)$$

头部与肩部高斯点拼接后进行统一渲染，在几乎不增加推理开销的前提下显著提升了头像完整性。

### 4. 多细节层次动态推理

OMG-Avatar 支持推理时动态选择细分级别（Sub#0 至 Sub#2），实现计算量与重建质量的灵活权衡。低分辨率 LOD（Sub#1，仅约 29K 高斯点）的性能已**超越 LAM（80K 点）和 GAGAvatar（180K 点）**（表 1、表 2），充分验证了粗到细策略的有效性。最高细分级别（Sub#2）在 VFHQ 上达到 PSNR 22.72、LPIPS 0.091，均优于所有基线方法。

OMG‑Avatar 的整体流水线围绕 **单张图像 → 可驱动多细节层次高斯头像** 这一目标设计，核心思路是将昂贵的全局注意力计算与网格细分过程解耦，并通过遮挡感知融合和多区域建模提升头像的完整性与细节可控性。图 1 给出了框架的全貌，主要包含以下阶段：

1. **身份与局部特征提取**  
   给定源图像，首先利用冻结的 **DINOv2** 骨干网络一次性提取局部特征图 $F_{\mathrm{local}}$ 和身份特征 $F_{\mathrm{id}}$。身份特征随后通过多个交叉注意力块与初始低分辨率头部网格（FLAME 模型，约 5023 个顶点）交互，产生全局特征 $F_{\mathrm{global}}^{GS_0}$，并同时预测顶点偏移量以增强 FLAME 的几何表达能力（Eq. 1）。**这一交叉注意力仅在最低分辨率网格上执行一次**，从根本上避免了后续细分级别上计算量指数级膨胀的问题（Eq. 13）。

2. **粗到细的层次化特征采样与融合（HPFS + OAFF）**  
   在训练过程中，网格 $V_k$ 及其全局特征 $F_{\mathrm{global}}^{GS_k}$ 通过 MLP 和 Loop 细分逐步细化至最多 2 级（$K=2$，最终约 79,936 个顶点）。每一级细分后，**层次化投影特征采样模块（HPFS）** 将顶点投影到图像平面，从 $F_{\mathrm{local}}$ 中双线性采样局部特征 $F_{\mathrm{local}}^{GS_k}$（Eq. 4）。  
   为避免被遮挡顶点引入噪声，**遮挡感知特征融合模块（OAFF）** 利用深度缓冲生成二元可见性掩码 $M^{GS_k}$（Eq. 5），仅将可见顶点的局部特征与全局特征相加，得到融合后的头部表示 $F_h^{GS_k}$（Eq. 6）。这一设计使得低分辨率层次（Sub #1，约 29K 高斯点）的性能即可超越 LAM（80K 点）和 GAGAvatar（180K 点）。

3. **多区域建模与高斯属性回归**  
   针对 FLAME 模型缺乏肩部区域的问题，框架通过图像分割掩码和共享特征平面独立预测肩部高斯参数（颜色、不透明度、尺度、旋转及位置偏移），并与头部高斯拼接，形成完整的上半身头像（Eq. 9–10）。头部高斯的位置直接取自最终细分网格 $V_K$，其余属性由 MLP 从 $F_h^{GS_K}$ 回归得到（Eq. 7–8）。

4. **神经优化器与可驱动重演**  
   粗渲染结果 $I_c$ 经过一个基于 UNet 的 **神经优化器** 细化，生成最终高质量图像 $I_r$。训练损失在粗渲染和精炼图像上联合计算 L2、SSIM 和感知损失，并对顶点偏移施加 L2 正则化（Eq. 12）。  
   在重演阶段，仅需根据驱动图像的 FLAME 参数更新头部高斯的位置分量（图 1 红色虚线路径），其余属性保持不变，从而实现 **单图 0.2 秒重建、85 FPS 实时驱动** 的高效推理。

**输入与输出**  
- **输入**：单张 RGB 源图像（可含肩部），驱动图像序列（仅用于提取姿态/表情参数）。  
- **输出**：可在任意 FLAME 参数驱动下实时渲染的多细节层次高斯头像，支持 0–2 级细分动态切换，高斯点数从约 29K 到约 89K 可调。

> 注：上述流水线描述综合了图 1 的框架示意、第 3.1–3.4 节的方法细节以及消融实验中关于模块必要性的证据。各模块的定量贡献（如去除局部特征导致 CSIM 从 0.869 降至 0.429，去除神经优化器使 PSNR 下降 1.3 dB）在后续消融分析章节中有详细讨论。

![[assets/figures/papers/paper_list_l1031_https_arxiv_org_abs_2603_01506/figures/001_Figure_1.jpg]]
*Figure 1: The overall pipeline of OMG-Avatar framework. Our method extracts global features via cross-attention and local details via projection-based sampling, which are fused under the guidance of depth buffers. A coarse-to-fine strategy is proposed to facilitate hierarchical detail perception. The head and shoulder are predicted separately using shared features and then combined for rendering*

OMG-Avatar 的核心设计围绕一个关键洞察展开：**将昂贵的交叉注意力操作限制在初始低分辨率网格上，随后通过粗到细的网格细分与投影采样高效扩展特征空间**。这一策略从根本上解决了现有方法（如 LAM 在高分辨率网格上直接计算注意力）面临的计算复杂度随细分级别指数增长的问题。

### 1. 3DMM 增强网格与全局特征提取

方法首先利用 FLAME 模型构建增强的头部网格。给定身份参数 $\vec{\beta}$、姿态参数 $\vec{\theta}$ 和表情参数 $\vec{\psi}$，基础网格由 blendshape 线性组合得到，并叠加一个由全局特征预测的顶点偏移量 $\Phi_{\mathrm{offset}}(F_{global}^{GS_0})$：

$$
T_p(\vec{\beta}, \vec{\theta}, \vec{\psi}) = \overline{T} + B_S(\vec{\beta}; S) + B_P(\vec{\theta}; P) + B_E(\vec{\psi}; E) + \Phi_{\mathrm{offset}}(F_{global}^{GS_0})
$$

其中 $\overline{T}$ 为平均模板，$B_S$、$B_P$、$B_E$ 分别为身份、姿态、表情的 blendshape 基。经蒙皮函数 $\mathrm{W}$ 处理后得到初始头部顶点 $V_0$（约 5023 个顶点）。

**全局特征 $F_{global}^{GS_0}$ 的提取是计算效率的核心瓶颈**。OMG-Avatar 使用 DINOv2 提取图像特征后，仅在初始低分辨率网格 $V_0$ 上执行一次交叉注意力，获得初始全局特征。这避免了后续细分级别上的重复注意力计算。

### 2. 粗到细网格细分与特征细化

为实现多细节层次（LOD），方法引入粗到细的细分策略。在第 $k$ 级，通过 MLP $\Phi_k$ 细化全局特征，并利用 Loop 细分算法 $\Delta$ 对网格进行上采样：

$$
F_{global}^{GS_{k+1}}, V_{k+1} = \Delta(\Phi_k(F_{global}^{GS_k}), V_k), \quad 0 \le k \le K
$$

最大细分级别 $K=2$，最终顶点数约 79,936。**注意：交叉注意力仅在 $k=0$ 级执行**，后续级别仅通过 MLP 和细分传播特征，计算复杂度 $O(l \cdot h \cdot 4^{k} \cdot V_0 \cdot N_{\mathrm{DINO}} \cdot d_{\mathrm{head}})$ 随 $k$ 指数增长——这恰好解释了为何将注意力限制在 $k=0$ 级能带来显著的效率优势。

### 3. 层次化投影特征采样（HPFS）

局部细节通过 HPFS 模块获取。将细分后的顶点 $V_k$ 投影到图像平面 $\mathrm{P}(V_k)$，在 DINOv2 局部特征图 $F_{local}$ 上进行双线性采样：

$$
F_{local}^{GS_k} = \mathrm{Sampling}(\mathrm{P}(V_k), F_{local}), \quad 0 \leq k \leq K
$$

这一投影采样机制使得局部特征能够随网格细分逐步精细化，而无需额外的注意力计算。

### 4. 遮挡感知特征融合（OAFF）

直接融合所有顶点的局部特征会引入被遮挡区域的噪声。OAFF 模块利用深度缓冲区生成可见性掩码：对每个顶点，比较其投影深度 $z_i$ 与深度缓冲值 $\hat{z}_i$：

$$
M_i^{GS_k} = \begin{cases} 1, & \text{if } z_i = \hat{z}_i \\ 0, & \text{if } z_i > \hat{z}_i \end{cases}
$$

仅保留可见顶点的局部特征，并与全局特征相加得到融合表示：

$$
F_h^{GS_k} = F_{global}^{GS_k} + F_{local}^{GS_k} \odot M^{GS_k}
$$

消融实验证实了这一设计的决定性作用：**去除局部特征后，身份一致性 CSIM 从 0.869 骤降至 0.429**（表 4），说明 OAFF 是维持身份保真度的关键机制。

### 5. 多区域建模与神经优化器

为弥补 FLAME 模型缺乏肩部区域的不足，方法通过图像分割掩码 $M_s$ 和特征平面独立预测肩部高斯参数（颜色 $c_s$、不透明度 $o_s$、缩放 $s_s$、旋转 $r_s$）及位置偏移 $O_s$：

$$
c_s, o_s, s_s, r_s, O_s = \mathrm{Flatten}(\mathrm{Conv}(F_{local}^{GS}) \odot M_s)
$$

头部与肩部高斯点拼接后进行粗渲染，再由基于 UNet 的神经优化器对粗渲染特征图进行细化，生成最终高质量图像。消融显示，**去除神经优化器使 PSNR 从 22.72 降至 21.42，并丢失牙齿等动态细节**（表 4，图 4）。

### 6. 训练损失

总损失在驱动图像 $I_d$、粗渲染 $I_c$ 和精炼图像 $I_r$ 上联合计算：

$$
\mathscr{L} = \lambda_1 \mathscr{L}_2(I_d, I_c \& I_r) + \lambda_2 \mathscr{L}_{\mathrm{SSIM}}(I_d, I_c \& I_r) + \lambda_3 \mathscr{L}_{\mathrm{percep}}(I_d, I_c \& I_r) + \lambda_4 \mathscr{L}_{\mathrm{reg}}
$$

其中 $\mathscr{L}_{\mathrm{reg}} = \| \mathbf{offset} \|_2$ 对顶点偏移施加 L2 正则化，防止几何过度变形。

## 实验与关键发现

### 主实验结果

OMG-Avatar 在 VFHQ 和 HDTF 两个数据集上进行了自重建与跨身份重演评估，并与 12 个基线方法进行了全面对比。

**VFHQ 数据集**（表 1）：在最高细分级别 Sub#2 下，OMG-Avatar 的自重建 PSNR 达到 22.72，SSIM 0.831，LPIPS 0.091，在所有指标上均优于包括 LAM（PSNR 22.65）和 GAGAvatar（PSNR 22.20）在内的全部基线。跨身份重演场景下，身份一致性 CSIM 达到 0.869，同样领先。值得注意的是，即使在最低细分级别 Sub#1（仅约 29K 高斯点），其性能已超越 LAM（80K 高斯点）和 GAGAvatar（180K 高斯点），验证了分层特征提取与融合策略在参数效率上的显著优势。

**HDTF 数据集**（表 2）：Sub#2 的自重建 PSNR 为 24.14，跨重建 CSIM 达 0.886，分别比 LAM 高出 0.71 和 0.037，进一步确认了方法的泛化能力。

**推理效率**（表 3）：在 A100 GPU 上，OMG-Avatar Sub#2 以 85.94 FPS 的速度运行，约为 GPAvatar（22.70 FPS）的 3.8 倍，且高斯点数更少（表 5）。即使在 RTX 4090 上，Sub#2 仍可达到 58.82 FPS，满足实时重演需求。所有推理速度测量均排除了驱动参数估计时间，因为该部分可预计算。

### 消融实验

消融实验（表 4，图 4）系统验证了各核心模块的贡献：

- **去除局部特征**（w/o Local Feature）：身份一致性 CSIM 从 0.869 骤降至 0.429，PSNR 降至 21.21，表明投影采样的局部细节对保持身份至关重要。
- **去除神经优化器**（w/o Refiner）：PSNR 从 22.72 下降至 21.42，且牙齿、皱纹等动态细节明显丢失（图 4），证明 UNet 精炼器对视觉保真度的关键作用。
- **去除全局特征**（w/o Global Feature）：在眼睛、嘴巴等动态区域引入与源图像不一致的伪影（图 4），说明全局语义对表情一致性的必要性。
- **细分级别影响**（图 5）：性能在 2 级细分后趋于饱和。分析认为瓶颈在于 DINOv2 特征图的分辨率（约 88K），超过 80K 顶点后的投影采样无法获取更多独立局部信息，限制了进一步细分的收益。

### 失败模式与局限性

1. **大角度视角退化**（图 6）：由于仅在单目访谈视频上训练，模型对头部旋转超出 ±60° 的视角泛化能力有限，会出现明显伪影。这是训练数据分布限制的直接后果。
2. **3DMM 依赖**：模型依赖 FLAME 先验和精确的 3DMM 跟踪参数。当驱动图像的 3DMM 估计不准确时，可能导致几何失真和身份漂移，但这一点的定量评估需要手动验证。
3. **特征分辨率瓶颈**：如图 5 所示，进一步增加细分级别无法提升性能，受限于 DINOv2 特征图的分辨率上限，这构成了当前框架的固有天花板。

### 训练成本分析

表 6 对比了 OMG-Avatar 与 LAM 的训练配置。OMG-Avatar 总训练时间约 200 GPU 小时（A100），而 LAM 需要约 2600 GPU 小时，成本降低超过 90%。这一效率提升源于仅在初始低分辨率网格（5K 顶点）上执行交叉注意力，避免了随细分级别指数增长的注意力计算成本（见 Eq. 13 的复杂度分析）。

![[assets/figures/papers/paper_list_l1031_https_arxiv_org_abs_2603_01506/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the VFHQ dataset. The first , second , and third best-performing methods are highlighted. The Sub # indicates the subdivision level for inference*

![[assets/figures/papers/paper_list_l1031_https_arxiv_org_abs_2603_01506/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on the HDTF dataset*

![[assets/figures/papers/paper_list_l1031_https_arxiv_org_abs_2603_01506/figures/010_Table_4.jpg]]
*Table 4: Ablation results on the VFHQ dataset*

![[assets/figures/papers/paper_list_l1031_https_arxiv_org_abs_2603_01506/figures/013_Table_6.jpg]]
*Table 6: Comparison of training configurations for LAM and ours*

![[assets/figures/papers/paper_list_l1031_https_arxiv_org_abs_2603_01506/figures/014_Figure_8.jpg]]
*Figure 8: Comparision with state-of-the-art methods that support one-shot, feed-forward 3D avatar reconstruction with real-time facial reenactment*

## 定位与知识库关联

**核心瓶颈与因果机制**

现有单图3D头像重建方法在计算效率与细节层次可控性上存在明显瓶颈。以 **GAGAvatar** 和 **LAM** 为代表的基于交叉注意力的方法，其注意力计算复杂度随网格顶点数呈指数增长——$O(l \cdot h \cdot 4^k \cdot V_0 \cdot N_{\text{DINO}} \cdot d_{\text{head}})$，其中 $k$ 为细分级别（Eq.13）。这导致高分辨率网格上的交叉注意力成本极高：LAM 在约80K顶点上直接计算注意力，训练成本高达约2600 GPU小时（A100），而 **OMG-Avatar** 仅需约200 GPU小时，降低90%以上（表6）。此外，这些方法普遍缺乏对非头部区域（如肩部）的有效建模，导致头像不完整。

OMG-Avatar 的核心因果杠杆在于**将全局-局部特征提取与网格细分过程解耦**：仅在初始低分辨率网格（5023顶点）上执行一次交叉注意力，随后通过逐步细分和投影采样获取局部特征，并利用深度缓冲筛选可见顶点以实现遮挡感知融合。这一设计从根本上切断了注意力复杂度与细分级别之间的指数依赖关系，使得推理时可在0.2秒内完成单图重建，并在A100上实现85.94 FPS的实时重演（表3）。

**与基线方法的关键差异**

| 方法维度 | 基线方法（LAM/GAGAvatar） | OMG-Avatar | 证据锚点 |
|---------|------------------------|------------|---------|
| 特征提取策略 | 在高分辨率网格上直接执行交叉注意力 | 仅在初始低分辨率网格（5K顶点）执行交叉注意力，逐步细分后投影采样局部特征 | 第3.1节，Eq.(3) |
| 特征融合方法 | 简单融合或无遮挡处理 | 深度缓冲引导的遮挡感知特征融合（OAFF），仅融合可见顶点的局部特征 | 第3.2节，Eq.(5)(6) |
| 多区域建模 | 未显式建模肩部 | 通过分割掩码和特征平面独立预测肩部高斯参数 | 第3.3节，Eq.(9)(10) |
| 细节层次控制 | 固定分辨率 | 支持0-2级细分，推理时动态选择LOD | 第1节，4.5节 |
| 训练成本 | LAM约2600 GPU小时 | 约200 GPU小时 | 表6 |

**知识库定位与适用边界**

OMG-Avatar 属于**单样本前馈高斯头部头像重建**方法，与以下方法构成直接比较关系：

- **GAGAvatar**：基于3D高斯泼溅的单图头像重建，使用约180K高斯点，推理速度较慢（表3中未直接列出FPS，但OMG-Avatar Sub#1仅用29K点即超越其性能）。
- **LAM**：基于交叉注意力的高分辨率网格方法，使用约80K高斯点，训练成本极高（~2600 GPU小时），OMG-Avatar以更低的高斯点数（29K-80K）和训练成本实现更优性能。
- **GPAvatar**：基于神经渲染的方法，在A100上FPS为22.70，OMG-Avatar Sub#2达到85.94 FPS，约3.8倍加速（表3）。
- **ROME、StyleHeat、OTAvatar、HideNeRF、GOHA、CVTHead、Real3DPortrait、Portrait4D、Portrait4D-v2**：这些方法在VFHQ和HDTF数据集上与OMG-Avatar进行了定量比较（表1、表2），OMG-Avatar在PSNR、SSIM、LPIPS、CSIM等指标上均取得最优或次优结果。

**方法局限与失效模式**

1. **3DMM先验依赖**：模型依赖FLAME先验和精确的3DMM跟踪，当3DMM估计不准确时可能导致几何失真。这是该类方法的共性局限，需要手动验证具体失效案例。

2. **大角度视角泛化有限**：由于仅在单目访谈视频上训练，对头部旋转超出±60°的视角会出现明显伪影（图6）。这一局限源于训练数据分布，而非方法设计缺陷。

3. **特征分辨率瓶颈**：在2级细分后性能趋于饱和（图5），主要受限于DINOv2特征图的分辨率（约88K有效采样点），无法通过进一步增加顶点恢复更多细节。这提示当前框架的性能上限由特征提取器的空间分辨率决定。

**开放问题**

1. 是否可以引入更高分辨率的图像特征（如ViT-H/14）来突破当前细分级别的性能瓶颈？这将直接提升特征采样密度，但可能带来额外的计算开销。

2. 如何高效地结合多视角或3D扫描数据，提升在大角度旋转下的鲁棒性？当前方法在±60°外的伪影问题需要额外的几何先验来解决。

3. 该方法能否直接扩展到全身或多人物头像的生成，且保持实时性？多区域建模策略（第3.3节）为扩展提供了技术基础，但全身建模涉及更复杂的几何约束和更大的特征空间。

## 原文 PDF

![[paperPDFs/CVPR_2026/OMG_Avatar_One_shot_Multi_LOD_Gaussian_Head_Avatar.pdf]]

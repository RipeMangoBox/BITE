---
title: "BiMotion: B-spline Motion for Text-guided Dynamic 3D Character Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BiMotion_B_spline_Motion_for_Text_guided_Dynamic_3D_Character_Generation.pdf
aliases:
- BiMotion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用连续可微的B样条曲线表示运动，将任意长度的运动序列压缩为固定数量的控制点，从而在无需修改生成模型能力的前提下，实现完整运动语义的保留。
primary_logic: 运动本质是连续的，帧数仅为采样细节。利用B样条曲线的局部控制性和可重参数化特性，可将任意长度序列编码为紧凑的控制点集，使固定尺寸模型能够生成语义完整的运动。
claims:
- BiMotion在Vbench所有5个定量指标上均超越现有最优方法（GVFDiffusion、AnimateAnyMesh、V2M4），同时生成速度更快、GPU内存占用更低。
- B样条插值从预测控制点重建的轨迹在整段序列上的L1误差显著低于线性插值。
- Laplacian正则化在短序列（T<k）情况下产生比Ridge回归更自然的运动插值。
- 多层级控制点嵌入（Control-PE）相比传统频率位置编码，能更准确地恢复精细运动（如狮子尾巴的摆动）。
---

# BiMotion: B-spline Motion for Text-guided Dynamic 3D Character Generation

> [!tip] 核心洞察
> 运动本质是连续的，帧数仅为采样细节。利用B样条曲线的局部控制性和可重参数化特性，可将任意长度序列编码为紧凑的控制点集，使固定尺寸模型能够生成语义完整的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | BiMotion：基于B样条运动的文本引导动态3D角色生成 |
| 英文题名 | BiMotion: B-spline Motion for Text-guided Dynamic 3D Character Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_BiMotion_B-spline_Motion_for_Text-guided_Dynamic_3D_Character_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | BiMotion |
| Dataset | Vbench |

> [!tip] 效果简介
> - Vbench 上，OC↑ 0.187 vs 0.175 (V2M4) (+0.012)；SC↑ 0.948 vs 0.951 (AnimateAnyMesh) (-0.003)；TF↑ 0.995 vs 0.993 (AnimateAnyMesh) (+0.002)。

## 概述

文本驱动的动态3D角色生成面临一个根本性瓶颈：运动序列天然具有可变长度，而主流生成模型依赖固定容量的离散帧表示。现有方法或裁剪序列至固定长度导致运动语义不完整，或均匀下采样造成轨迹抖动与子动作碎片化——其本质矛盾在于**可变长度运动序列与固定容量生成模型之间的不兼容**。

BiMotion 的核心洞察是：**运动本质上是连续的，帧数仅为采样细节**。通过引入连续可微的B样条曲线表示运动，BiMotion 将任意长度的顶点位移序列压缩为固定数量的控制点，从而在不修改生成模型容量的前提下保留完整运动语义。具体而言，一个闭式的 Laplacian 正则化最小二乘求解器将变长序列高效拟合到紧凑的控制点集；随后，专门设计的 B样条 VAE 通过多层级控制点嵌入、法向融合以及对应/刚性损失，将控制点与初始形状编码为紧凑潜变量；最后，流匹配生成器根据文本提示生成运动潜变量，经解码与 B样条重投影重建任意长度的网格序列。

在 Vbench 基准上，BiMotion 在全部五项指标上超越现有最优方法——包括 **AnimateAnyMesh**（Wu et al., ICCV 2025）、**GVFDiffusion**（Zhang et al., ICCV 2025）和 V2M4——同时生成速度更快、GPU 内存占用更低（Table 1）。消融实验证实，B样条插值的重建误差显著低于线性插值（L1误差从 3.237 降至 1.078），Laplacian 正则化在短序列上产生更自然的运动插值，法向融合有效消除空间邻近部件的伪影，多层级控制点嵌入则比传统位置编码更准确地恢复精细运动细节。

方法的主要局限在于：控制点数量固定，可能不足以表达极高频的复杂运动；假设网格拓扑不变，不支持撕裂或破碎等拓扑变化；B样条的光滑性约束偶尔会导致语义一致性指标（SC）略低于离散方法。这些局限也指明了未来的开放方向：自适应控制点数量选择、向非网格表示（如点云、NeRF）的扩展，以及结合物理约束或骨架先验以进一步提升运动合理性。

## 背景与动机

### 问题背景：文本驱动的动态3D角色生成

文本驱动的动态3D角色生成旨在根据自然语言描述，为给定的静态3D角色网格赋予符合语义的连续运动。该任务在游戏制作、影视特效、虚拟人等应用中具有重要价值。形式上，给定一个初始网格 $M_0$ 和文本提示 $y$，目标是学习条件后验分布 $p_{\theta}(M_{1:T} \mid M_0, y)$，以生成长度为 $T$ 的动态网格序列。

### 现有方法的根本瓶颈

当前主流方法普遍采用**离散帧表示**来处理运动序列。以 **AnimateAnyMesh**（Wu et al., ICCV 2025）为代表的前馈式方法，将运动表示为逐帧的顶点位移差，并通过VAE潜空间扩散进行生成；而 **GVFDiffusion**（Zhang et al., ICCV 2025）、**V2M4** 等视频到4D的方法则从视频帧中重建动态网格。这些方法面临一个根本性矛盾：**可变长度的运动序列与固定容量生成模型之间的冲突**。

具体而言，现有方法通过裁剪至固定长度或均匀下采样来统一序列长度。这导致两个严重后果：
- **运动语义碎片化**：长序列被截断后，完整的运动语义（如“从蹲下到起跳再落地”）被割裂为不连贯的子动作片段。
- **时序抖动**：均匀下采样丢失了关键帧之间的过渡信息，导致重建的运动轨迹出现高频抖动。

### 核心洞察与动机

BiMotion的核心洞察在于：**运动本质上是连续的，帧数仅仅是采样细节**。一条完整的运动轨迹（如角色手臂的挥动）可以用一条光滑的空间曲线来描述，而离散帧只是该曲线上的一系列采样点。因此，如果能够找到一种连续表示来刻画运动曲线，就可以将任意长度的序列压缩为固定数量的参数，从根本上消除序列长度对生成模型的限制。

这一洞察引导出一个关键的因果调节变量：**运动表示的选择**。BiMotion选择**B样条曲线**作为运动表示，原因在于其具备两个关键特性：
- **局部控制性**：修改单个控制点仅影响曲线的局部区域，使得模型可以精确控制运动的各个阶段。
- **可重参数化**：任意长度的采样序列可以通过闭式最小二乘拟合，压缩为固定数量的控制点，而无需改变生成模型的结构。

基于此，BiMotion将运动生成问题重新定义为：**给定初始网格和文本提示，直接生成B样条控制点，再通过B样条插值重建任意长度的连续运动轨迹**。这一范式转换使得固定尺寸的生成模型能够完整保留运动语义，同时保持生成轨迹的光滑性和物理合理性。

## 核心创新

BiMotion 的核心创新在于用**连续 B 样条曲线替代离散帧表示**，从根本上解决了可变长度运动序列与固定容量生成模型之间的矛盾。传统方法（如 **AnimateAnyMesh**，Wu et al., ICCV 2025）依赖逐帧的顶点位移差，必须将序列裁剪或下采样至固定长度，导致运动语义碎片化或时序抖动。BiMotion 通过以下四个关键槽位（changed slots）的重新设计，实现了完整运动语义的保留与高效生成。

### 1. 运动表示：从离散帧差到连续 B 样条曲线

**基线做法**：AnimateAnyMesh 等方法将运动表示为离散帧间的顶点位移差 $\mathcal{V}_T$，序列长度 $T$ 可变，但生成模型要求固定维度输入，因此必须强制裁剪或均匀下采样。

**BiMotion 方案**：将每条顶点运动轨迹独立建模为 $d$ 阶 B 样条曲线：
$$\mathcal{C}(t) = \sum_{i=0}^{k-1} \mathcal{N}_{i,d}(t) \mathbf{p}_i, \quad t \in [u_d, u_{m-1-d}]$$
其中 $k$ 为控制点数量，$\mathbf{p}_i$ 为控制点坐标，$\mathcal{N}_{i,d}$ 为 B 样条基函数。在 $T$ 个时间点采样可写成矩阵形式 $\mathcal{C}_T = B_{T,k} \mathcal{P}_k$。

**关键机制**：B 样条曲线的局部控制性意味着每个控制点仅影响有限时间区间内的曲线形状，而曲线整体仍保持 $C^{d-1}$ 阶连续可微。这使得任意长度的运动序列可被压缩为固定数量 $k$ 的控制点集 $\mathcal{P}_k$，无需修改生成模型的结构或容量。运动本质是连续的，帧数仅是采样细节——这一洞察是 BiMotion 的理论根基。

### 2. 序列长度处理：从强制裁剪到闭式正则化拟合

**基线做法**：固定长度裁剪或均匀下采样，前者丢失运动完整性，后者引入时序抖动。

**BiMotion 方案**：通过带 Laplacian 正则化的最小二乘拟合，将任意长度序列压缩到固定控制点集。当 $k \leq T$ 时，最小二乘解唯一；当 $k > T$（短序列场景）时，系统欠定，引入 Laplacian 正则化项：
$$\min_{\mathcal{P}_k} \| \boldsymbol{B}_{T,k} \mathcal{P}_k - \mathcal{V}_T \|_F^2 + \mu \| \mathbf{L} \mathcal{P}_k \|_F^2$$
其闭式解为：
$$\mathcal{P}_k = \left( \boldsymbol{B}_{T,k}^{\top} \boldsymbol{B}_{T,k} + \mu \mathbf{L}^{\top} \mathbf{L} \right)^{-1} \boldsymbol{B}_{T,k}^{\top} \mathcal{V}_T$$

**证据强度**：消融实验（Figure 6）证实，在 $T=10$ 的短序列上进行 2 倍 B 样条插值时，Laplacian 正则化相比 Ridge 回归产生更自然的运动过渡，避免了因过拟合导致的非物理形变。这是 BiMotion 处理短序列能力的核心保障。

### 3. 运动几何嵌入：从频率位置编码到多层级控制点嵌入

**基线做法**：标准频率位置编码（如 NeRF 式位置编码）将控制点坐标映射到高频空间，但未利用 B 样条的多尺度结构。

**BiMotion 方案**：设计多层级控制点嵌入（Control-PE），通过预计算的小波包分解基 $\mathcal{W}_k$ 将控制点 $\mathcal{P}_{n,k_s}$ 分解为粗细尺度残差与最粗系数：
$$\mathcal{E}_{k} = [\mathcal{R}_{s}, ..., \mathcal{R}_{1}, \mathcal{P}_{n,k_{0}}] = \mathcal{W}_{k} \mathcal{P}_{n,k_{s}}$$
其中 $\mathcal{R}_i$ 为第 $i$ 级残差，$\mathcal{P}_{n,k_0}$ 为最粗尺度系数。这种分层表示使 VAE 编码器能同时捕获运动的全局趋势与局部细节。

**证据强度**：消融实验（Figure 8）表明，Control-PE 相比传统位置编码能更准确地恢复精细运动（如狮子尾巴的摆动），并减少高频伪影。定量消融（Table 2）进一步支持了该模块对重建精度的贡献。

### 4. 几何感知：从纯顶点特征到法向融合

**基线做法**：仅使用顶点位置或网格连接信息（如 AnimateAnyMesh 的采样方法）进行特征编码，难以区分空间邻近但运动模式不同的部件。

**BiMotion 方案**：提出法向融合策略（Normal Fusion），利用点特征与法向特征之间的余弦相似度作为自适应权重，融合两者：
$$\mathbf{F}_{0} = \mathbf{F}_{\mathcal{P}_{0}} + \left( w(\mathbf{F}_{\mathcal{P}_{0}}, \mathbf{F}_{\mathcal{N}_{0}}) \odot \mathbf{1}_{c} \right) \odot \mathbf{F}_{\mathcal{N}_{0}}$$
其中 $w(\cdot,\cdot)$ 为余弦相似度权重。该机制使模型能感知局部表面朝向，从而分离空间上邻近但运动独立的部件（如角色的手臂与躯干）。

**证据强度**：消融实验（Figure 7）直接展示了去除法向融合后，空间邻近部件之间出现明显伪影。该模块以轻量方式增强了 VAE 编码器的几何感知能力，无需额外标注或骨架先验。

### 创新总结

BiMotion 的四项槽位创新构成了一个闭环系统：B 样条表示将变长运动压缩为固定控制点集，Laplacian 正则化拟合保证短序列下的自然插值，多层级嵌入保留多尺度运动细节，法向融合增强几何感知。这些设计共同实现了在固定模型容量下生成语义完整、时序连贯的动态 3D 角色运动，且推理速度与 GPU 内存占用均优于现有方法（Table 1）。

## 整体框架

BiMotion 提出了一种基于 B 样条（B-spline）的运动表示与生成框架，核心思路是将变长顶点位移序列压缩为固定数量的控制点，从而在保持完整运动语义的前提下，使固定容量的生成模型能够处理任意长度的动态网格序列。

### 框架总览

整个 pipeline 由五个关键模块串联构成，如 Figure 2 所示，分为训练（红色箭头）和推断（黑色箭头）两条路径：

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/002_Figure_2.jpg]]
*Figure 2: Overview. BiMotion uses a B-spline representation for motion generation. During training (red arrow), vertex differences are converted into control points and encoded into motion latents. During inference (black arrow), the initial mesh and the text prompt generate motion latents that are decoded into control points and converted into the generated mesh sequence via B-spline reprojection*

1. **B 样条运动表示（B-spline Motion Representation）**：将输入的变长顶点位移序列 $\\mathcal{V}_T$ 通过闭式 Laplacian 正则化最小二乘拟合，压缩为固定数量 $k$ 的控制点集 $\\mathcal{P}_k$。
2. **B 样条 VAE 编码器（B-spline VAE Encoder）**：以控制点 $\\mathcal{P}_{n,k}$ 和初始形状 $(P_{n,0}, N_0)$ 为输入，通过多层级控制点嵌入（Control-PE）和法向融合（Normal Fusion）提取几何感知特征，经交叉注意力压缩为紧凑的运动潜变量 $z_k$ 和初始形状潜变量 $z_0$。
3. **流匹配生成器（Flow-Matching Generator）**：以文本提示 $y$ 和初始形状潜变量 $z_0$ 为条件，通过基于 DiT 的速度场网络从噪声中生成运动潜变量 $\\hat{z}_k$。
4. **B 样条 VAE 解码器（B-spline VAE Decoder）**：将运动潜变量 $\\hat{z}_k$ 通过交叉注意力与初始形状特征融合，解码为预测的控制点 $\\hat{\\mathcal{P}}_{n,k}$。
5. **B 样条重投影（B-spline Reprojection）**：利用 B 样条基函数矩阵 $B_{T,k}$，将预测控制点与初始网格顶点 $\\mathbf{V}_0$ 结合，重建任意长度的顶点序列 $\\hat{\\mathbf{V}}_{1:T} = \\mathbf{V}_0 + B_{T,k} \\hat{\\mathcal{P}}_k$。

### 模块关系与数据流

训练阶段，原始动态网格序列 $M_{0:T}$ 首先被转换为顶点位移 $\\mathcal{V}_T$，再经 B 样条拟合得到控制点 $\\mathcal{P}_k$。控制点与初始形状一同送入 VAE 编码器，产生潜变量 $z_0$ 和 $z_k$。VAE 解码器从潜变量重建控制点，并通过 B 样条重投影恢复顶点序列，训练信号来自控制点拟合损失、轨迹一致性损失和局部刚性损失的联合约束。

推断阶段，仅需初始网格 $M_0$ 和文本提示 $y$。初始形状经 VAE 编码器得到 $z_0$，流匹配生成器以 $z_0$ 和 $y$ 为条件采样运动潜变量 $\\hat{z}_k$，随后由 VAE 解码器解码为控制点，最终通过 B 样条重投影生成完整的动态网格序列。

### 核心设计决策

框架的关键设计在于用 **B 样条曲线的连续表示** 替代传统的离散帧间位移。这一选择带来了三个因果性优势：

- **长度无关性**：任意长度 $T$ 的序列均被压缩为固定数量 $k$ 的控制点，生成模型无需感知序列长度。
- **局部控制性**：B 样条基函数的局部支撑特性使每个控制点仅影响有限时间窗口，便于模型学习局部运动模式。
- **可微重参数化**：从控制点到顶点序列的映射是线性且可微的，允许端到端训练时梯度通过 B 样条基矩阵 $B_{T,k}$ 回传至控制点。

当序列较短（$T < k$）时，最小二乘系统欠定，框架引入 **Laplacian 正则化项** $\\mu \\| \\mathbf{L} \\mathcal{P}_k \\|_F^2$ 强制相邻控制点之间的平滑过渡，产生自然的运动插值（见 Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/001_Figure_1.jpg]]
*Figure 1: We propose BiMotion, a fast, feed-forward B-spline–based method for dynamic 3D character generation. It produces continuous, high-quality expressive motion trajectories aligned with rich textual prompts, outperforming discrete temporal sampling-based methods such as AnimateAnyMesh [96] under the same fixed-input constraint. See our project page for full motion dynamics*

## 核心模块与公式推导

### 3.1 运动生成的问题形式化

给定一个包含可变长度动态网格序列与文本提示的数据集 $\mathcal{D} = \{ ( M_{0:T}^{(i)}, y^{(i)} ) \}_{i=1}^{N}$，其中 $T$ 可变，目标是学习条件后验分布 $p_{\theta}(M_{1:T} \mid M_0, y) \approx p_{\mathcal{D}}(M_{1:T} \mid M_0, y)$。核心瓶颈在于：生成模型通常要求固定容量输入，而运动序列长度可变，直接裁剪或均匀下采样会破坏运动语义完整性。BiMotion 的关键思路是将运动从“帧序列”空间映射到“连续曲线控制点”空间，从而在固定维度下保留完整运动信息。

### 3.2 B样条运动表示

BiMotion 将每个顶点的位移轨迹独立建模为一条3维B样条曲线。一条由 $k$ 个控制点 $\mathbf{p}_i \in \mathbb{R}^3$ 定义的 $d$ 阶B样条曲线为：

$$\mathcal{C}(t) = \sum_{i=0}^{k-1} \mathcal{N}_{i,d}(t) \mathbf{p}_i, \quad t \in [u_d, u_{m-1-d}]$$

其中 $\mathcal{N}_{i,d}(t)$ 为B样条基函数，由节点向量 $[u_0, u_1, \dots, u_{m-1}]$ 决定。在 $T$ 个时间点采样该曲线，可写为矩阵形式：

$$\mathcal{C}_T = B_{T,k} \mathcal{P}_k$$

其中 $B_{T,k} \in \mathbb{R}^{T \times k}$ 是基函数在采样时间点上的取值矩阵，$\mathcal{P}_k \in \mathbb{R}^{k \times 3}$ 是堆叠的控制点矩阵。论文采用均匀三次B样条（$d=3$）。

### 3.3 闭式控制点拟合

给定一段长度为 $T$ 的顶点位移序列 $\mathcal{V}_T \in \mathbb{R}^{T \times 3}$，控制点通过最小二乘拟合求得。当 $k \leq T$ 时，系统是超定或恰定的，有唯一解。当序列较短（$k > T$）时，系统欠定，论文引入Laplacian正则化项以强制相邻控制点之间自然过渡：

$$\min_{\mathcal{P}_k} \| \boldsymbol{B}_{T,k} \mathcal{P}_k - \mathcal{V}_T \|_F^2 + \mu \| \mathbf{L} \mathcal{P}_k \|_F^2$$

其中 $\mathbf{L}$ 是Laplacian矩阵，$\mu$ 控制正则化强度。该凸优化问题存在闭式解：

$$\mathcal{P}_k = \left( \boldsymbol{B}_{T,k}^{\top} \boldsymbol{B}_{T,k} + \mu \mathbf{L}^{\top} \mathbf{L} \right)^{-1} \boldsymbol{B}_{T,k}^{\top} \mathcal{V}_T$$

**因果机制**：该闭式求解器是BiMotion的核心“压缩”模块——无论输入序列长度 $T$ 如何变化，输出始终是固定数量 $k$ 的控制点，从而消除了可变长度输入与固定容量生成模型之间的矛盾。Laplacian正则化在短序列场景下（Figure 6）产生比Ridge回归更自然的插值结果，因为它显式惩罚相邻控制点间的突变。

### 3.4 B样条VAE编码器设计

B样条VAE将控制点 $\mathcal{P}_{n,k}$ 和初始形状（点位置 $\mathcal{P}_{n,0}$ 和法向 $\mathcal{N}_0$）压缩为紧凑潜变量。编码器包含三个关键设计：

**法向融合（Normal Fusion）**：对于空间上邻近但运动模式不同的部件（如手臂与躯干），仅靠位置特征难以区分。法向融合通过余弦相似度权重将点特征 $\mathbf{F}_{\mathcal{P}_0}$ 与法向特征 $\mathbf{F}_{\mathcal{N}_0}$ 加权融合：

$$\mathbf{F}_{0} = \mathbf{F}_{\mathcal{P}_{0}} + \left( w(\mathbf{F}_{\mathcal{P}_{0}}, \mathbf{F}_{\mathcal{N}_{0}}) \odot \mathbf{1}_{c} \right) \odot \mathbf{F}_{\mathcal{N}_{0}}$$

其中 $w(\cdot,\cdot)$ 为逐点余弦相似度权重。消融实验（Figure 7）表明，无法向融合时空间邻近部件产生明显伪影。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/010_Figure_7.jpg]]
*Figure 7: Normal Fusion (NF) Ablation. NF effectively separates nearby distinct parts. Without it, artifacts appear (see red)*

**多层级控制点嵌入（Control-PE）**：不同于标准频率位置编码，Control-PE将控制点进行多层级小波包分解，输出粗尺度系数与各层残差的堆叠：

$$\mathcal{E}_{k} = [\mathcal{R}_{s}, ..., \mathcal{R}_{1}, \mathcal{P}_{n,k_{0}}] = \mathcal{W}_{k} \mathcal{P}_{n,k_{s}}$$

其中 $\mathcal{W}_k$ 是预计算的多层级分解基。该嵌入能更准确地恢复精细运动（如Figure 8中狮子尾巴的摆动），而传统位置编码会丢失此类细节。

### 3.5 VAE训练损失

VAE通过交叉注意力从压缩潜变量重建控制点特征：$\hat{\mathbf{F}}_k = \operatorname{CrossAttn}(\mathbf{F}_0, \hat{\mathbf{F}}_0', \hat{\mathbf{F}}_k')$。训练使用三个损失函数：

**Charbonnier拟合损失**：约束预测控制点 $\hat{\mathcal{P}}_{n,k}$ 与真实控制点 $\mathcal{P}_{n,k}$ 一致：

$$\mathcal{L}_{\mathrm{Fit}} = \mathbb{E}\left[\sqrt{\|\hat{\mathcal{P}}_{n,k} - \mathcal{P}_{n,k}\|_F^2 + \delta^2}\right]$$

**对应损失**：约束B样条重投影后的顶点轨迹与真实位移一致：

$$\mathcal{L}_{\mathrm{Corr}} = \mathbb{E}\left[\sqrt{\|\hat{\mathcal{V}}_{n,T'} - \mathcal{V}_{n,T'}\|_F^2 + \delta^2}\right]$$

**局部刚性损失**：强制KNN点对距离在时间上保持稳定，减少肢体拉伸或收缩伪影（Figure 9）：

$$\mathcal{L}_{\mathrm{Rigid}} = \mathbb{E}\left[\sqrt{(r_t(i,j) - r_{t-1}(i,j))^2 + \delta^2}\right]$$

其中 $r_t(i,j)$ 为点 $i$ 与 $j$ 在时刻 $t$ 的欧氏距离。消融实验（Table 2）表明，去除局部刚性损失后重建L1误差显著上升。

### 3.6 流匹配运动生成器

生成器基于DiT架构（12个DiT块），使用流匹配在潜空间生成运动。初始形状潜变量 $\tilde{\mathbf{z}}_0$ 与加噪运动潜变量 $\tilde{\mathbf{z}}_k^{(\tau)}$ 拼接作为输入，CLIP文本嵌入通过解耦交叉注意力作为条件。速度场 $v_{\theta_{\mathrm{vel}}}$ 的损失函数为：

$$\mathcal{L}_{\mathrm{FM}}(\theta_{\mathrm{vel}}) = \mathbb{E}\left[\|v_{\theta_{\mathrm{vel}}}(\tilde{\mathbf{z}}_k^\tau|\tau,\tilde{\mathbf{z}}_0,y) - \mathbf{u}\|_F^2\right]$$

其中目标速度 $\mathbf{u} = \mathbf{z}_k - \epsilon$，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$。

### 3.7 B样条重投影

推断时，生成的控制点 $\hat{\mathcal{P}}_k$ 通过B样条基函数重投影为任意长度的顶点序列：

$$\hat{\mathbf{V}}_{1:T} = \mathbf{V}_0 + B_{T,k} \hat{\mathcal{P}}_k$$

该步骤将固定维度的控制点表示恢复为可变长度的网格动画，且理论上可生成任意帧数的运动序列，不受训练时帧数限制。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/003_Figure_3.jpg]]
*Figure 3: B-spline VAE Pipeline. Given the initial shape*

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/009_Figure_6.jpg]]
*Figure 6: Laplacian Regularizer L. B-spline ×2 interpolation comparison from a T = 10 mesh sequence comparing Ridge [35] and our Laplacian regularizer L. L produces more natural results*

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/012_Figure_8.jpg]]
*Figure 8: Control-PE Ablation. Our control-PE (Bottom) captures fine motion (e.g., the lion’s tail) and reduces artifacts (red circles) compared to conventional position encoding (Middle)*

## 实验与分析

### 核心性能突破：Vbench 定量评估

BiMotion 在 Vbench 基准上的五项指标中四项取得最优，同时推理速度与显存占用显著优于现有方法。Table 1 汇总了与 **AnimateAnyMesh**（Wu et al., ICCV 2025）、**GVFDiffusion**（Zhang et al., ICCV 2025）和 **V2M4** 的全面对比：

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparisons. Our approach not only surpasses existing methods across multiple metrics (Sec. 4.3), but also requires less time and peak GPU memory (PG) on an A100 GPU*

- **动态程度（DD↑）**：BiMotion 达到 0.800，较次优方法 V2M4（0.750）提升 **+0.050**，表明 B 样条连续表示能生成更丰富的运动轨迹。
- **外观质量（AQ↑）**：0.529，优于 AnimateAnyMesh 的 0.514（**+0.015**），法向融合和局部刚性损失有效抑制了网格伪影。
- **时序连贯性（TF↑）**：0.995，略高于 AnimateAnyMesh（0.993，**+0.002**），连续 B 样条插值天然保证帧间平滑过渡。
- **对象一致性（OC↑）**：0.187，高于 V2M4（0.175，**+0.012**），说明生成的运动未破坏初始形状的几何结构。
- **语义一致性（SC↑）**：0.948，略低于 AnimateAnyMesh（0.951，**−0.003**）。这一微小差距可能与 B 样条的光滑性约束限制了部分高频语义表达有关，属于方法的内在权衡。

在效率维度，BiMotion 生成单个动态角色仅需约 3 秒，峰值 GPU 内存（A100）远低于依赖视频生成的 GVFDiffusion 和 V2M4，体现了前馈 B 样条框架在部署上的优势。

> 公平性说明：视频生成基线（GVFDiffusion、V2M4）均使用相同的高质量视频生成器 Kling 作为输入源，以消除视频预处理阶段的伪影干扰。BiMotion 与 AnimateAnyMesh 均在 16 帧固定输入约束下比较，排除了帧数差异的影响。

### 消融实验：组件贡献的因果链

#### 1. B 样条表示 vs. 线性插值（Table 2, Figure 5）

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/006_Table_2.jpg]]
*Table 2: VAE Quantitative Ablations. “Rec Error” indicates the mean L1 error (×10−2) averaged per trajectory and per instance*

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/007_Figure_5.jpg]]
*Figure 5: B-spline Ablation. B-spline interpolation from predicted control points achieves lower L1 error over the entire sequence than linear interpolation on sampled raw differences*

VAE 消融的定量结果（Table 2）揭示了表示选择的根本影响：将线性插值替换为 B 样条插值后，逐轨迹平均 L1 重建误差从基线 3.237 × 10⁻² 降至 1.078 × 10⁻²，误差缩减约 **67%**。Figure 5 进一步表明，B 样条从预测控制点重建的轨迹在整段序列上的 L1 误差均显著低于线性插值方案，验证了连续可微表示对运动语义的保真能力。

#### 2. Laplacian 正则化：短序列的插值质量（Figure 6）

当序列长度 T 小于控制点数量 k 时，最小二乘系统欠定。Figure 6 对比了 Ridge 回归与 Laplacian 正则化的 B 样条 ×2 插值效果：Laplacian 正则化通过约束相邻控制点的平滑性，产生更自然的过渡运动，避免了 Ridge 方案中出现的僵硬或非物理形变。这一设计直接解决了可变长度序列压缩到固定控制点集时的欠定问题。

#### 3. 法向融合（NF）：空间邻近部件的分离（Figure 7）

Figure 7 展示了无法向融合时的典型失效模式：空间上邻近但运动模式不同的部件（如角色的手臂与躯干）会产生纠缠伪影。法向融合利用余弦相似度加权融合点特征与法向特征，有效分离了这些部件，消除了红色标注区域中的伪影。这一组件对 B 样条 VAE 的几何感知能力至关重要。

#### 4. 多层级控制点嵌入（Control-PE）：精细运动恢复（Figure 8）

Figure 8 以狮子尾巴摆动为例，对比了传统频率位置编码与多层级控制点嵌入的细节恢复能力。标准位置编码（中行）在尾部区域出现明显伪影（红色圆圈），而 Control-PE（下行）准确捕捉了尾巴的连续摆动轨迹。该嵌入通过类似小波包分解的方式，将控制点表示为粗细尺度残差的堆叠，使 VAE 能同时关注运动的全局趋势与局部细节。

#### 5. 局部刚性损失（LRigid）：抑制拉伸伪影（Figure 9）

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/008_Figure_9.jpg]]
*Figure 9: LRigid Ablation. Our local rigid loss reduces the redcircled artifacts during motion generation. Prompt: “The pistol tilts up to an angled pose, then returns to forward-facing.”*

Figure 9 展示了枪械倾斜-复位场景下局部刚性损失的消融效果。未施加该损失时，枪管区域出现明显的拉伸/收缩伪影（红色圆圈）；引入后，运动保持了几何一致性。该损失通过强制 KNN 点对距离在时间上恒定，有效约束了非刚性形变。

#### 6. 网格重划分鲁棒性（Figure 10）

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/011_Figure_10.jpg]]
*Figure 10: Robustness to Meshing. Ours produces consistent motion under mesh changes (Top to Bottom), whereas AnimateAnyMesh exhibits unstable motion and artifacts (red circles)*

Figure 10 对比了 BiMotion 与 AnimateAnyMesh 在不同网格拓扑下的运动稳定性。BiMotion 生成的轨迹在网格变化后保持一致，而 AnimateAnyMesh 出现不稳定运动和明显伪影（红色圆圈）。这一鲁棒性源于 B 样条表示将运动编码为与网格采样无关的连续控制点，而非依赖特定顶点索引的离散位移。

### 失败模式与局限性

1. **高频运动细节丢失**：当控制点数量不足以覆盖复杂运动的高频分量时，B 样条的光滑性会导致细节平滑化。这在语义一致性（SC）指标上体现为略低于 AnimateAnyMesh，提示控制点数量的自适应选择是一个开放问题。
2. **拓扑变化不支持**：框架假设网格拓扑固定，因此无法处理涉及破碎、撕裂或拓扑变化的动态场景。
3. **光滑性-语义权衡**：B 样条的光滑性约束在保证时序连贯性的同时，可能过滤掉某些语义相关的高频运动模式（如快速抖动、突然转向），需要在实际应用中根据场景调整控制点密度或正则化强度。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_BiMotion_B_spline/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons. Our method (BiMotion) results in superior motion quality and is more aligned with the user-provided text prompts. Artifacts for the baseline methods are highlighted in red. Please see the supplementary material for additional results*

## 方法谱系与知识库定位

BiMotion 的核心贡献在于将**可变长度运动序列的生成问题**转化为**固定容量模型可处理的连续表示学习问题**。这一设计使其在文本驱动的动态3D角色生成领域占据了一个独特的方法论位置：它既不同于依赖离散帧采样的前馈方法，也不同于需要视频中间表示的两阶段方案。

### 与基线方法的关系

**AnimateAnyMesh**（Wu et al., ICCV 2025）是BiMotion最直接的对比对象。两者共享“给定初始网格与文本提示，直接生成动态网格序列”的任务设定，且均在16帧固定输入约束下进行比较。然而，AnimateAnyMesh采用离散帧间顶点位移作为运动表示，通过VAE潜空间扩散生成运动。这种逐帧独立的表示方式使其难以捕获跨帧的运动连贯性——当运动序列长度变化时，需要裁剪或均匀下采样，导致子动作碎片化或抖动。BiMotion通过B样条曲线将任意长度序列压缩为固定数量的控制点，从根本上规避了这一瓶颈。定量结果（Table 1）显示，BiMotion在Vbench的5项指标中有4项超越AnimateAnyMesh，其中动态程度（DD）提升显著（+0.050），仅在语义一致性（SC）上略低0.003——这可能源于B样条的光滑性约束对某些高频语义表达的限制。

**GVFDiffusion**（Zhang et al., ICCV 2025）和**V2M4**代表另一类方法：从单目视频重建或生成动态3D内容。这类方法依赖视频作为中间表示，其运动质量受限于视频生成模型的能力与视频到3D重建的精度。BiMotion直接生成3D运动，避免了视频域的退化与重建误差。在效率上，BiMotion的生成时间与GPU峰值内存均显著低于这两种方法（Table 1），体现了前馈B样条框架的计算优势。

### 适用边界与局限

BiMotion的设计建立在三个核心假设之上，这些假设也划定了其适用边界：

1. **运动连续性假设**：B样条表示天然适合平滑、连续的运动轨迹。对于包含突变、碰撞或高频振动的运动，固定数量的控制点可能不足以表达细节——这是B样条表示能力与计算开销之间的固有权衡。

2. **固定拓扑假设**：方法将网格顶点视为独立轨迹进行建模，依赖初始网格的顶点对应关系。这意味着BiMotion不支持拓扑变化的运动（如物体破碎、撕裂或部件分离），限制了其在破坏性场景或形态变化场景中的应用。

3. **控制点数量固定假设**：控制点数量k是预定义超参数，对所有运动序列统一适用。对于简单的周期性运动，k可能冗余；对于复杂的多阶段运动，k可能不足。如何自适应地选择k以平衡表达能力与计算开销，仍是一个开放问题。

### 开放问题与未来方向

从知识库定位的角度，BiMotion开辟了“连续表示驱动3D运动生成”的研究方向，但以下问题值得后续工作关注：

- **表示扩展**：B样条框架能否推广到非网格表示（如点云、3D高斯泼溅、NeRF）？这需要解决点对应关系的建立问题，以及连续表示在不同几何表示间的迁移问题。

- **拓扑变化支持**：引入动态图结构或部件级运动表示，可能使框架支持部件分离或形态变化的运动，扩展其在更广泛动态场景中的适用性。

- **物理与结构先验**：当前方法仅依赖数据驱动学习运动模式。结合骨架先验、物理约束（如刚体运动约束）可能改善运动的物理合理性，尤其是在训练数据稀疏的运动类型上。

- **真实世界泛化**：BiMotion在BIMO合成数据集上训练与评估，其在真实世界扫描数据或交互式应用中的泛化性能尚待验证。域适应或弱监督微调策略可能成为关键。

- **控制粒度与语义对齐**：SC指标的轻微下降提示B样条光滑性可能与某些文本语义的精确表达存在冲突。探索自适应光滑性控制或混合表示（如B样条与稀疏关键帧结合）可能进一步提升语义对齐质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/BiMotion_B_spline_Motion_for_Text_guided_Dynamic_3D_Character_Generation.pdf]]
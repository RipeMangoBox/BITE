---
title: "Secondary Motion-Aware 3D Clothed Gaussian Avatars from Monocular Videos"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Secondary_Motion_Aware_3D_Clothed_Gaussian_Avatars_from_Monocular_Videos.pdf
project_link: null
code_link: null
openreview_forum_id: 2A3Q2EtGTF
aliases:
- SMADS
- SMA3CGAFMV
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入速度编码的自回归图神经网络（GNN）变形器，在构造的高斯节点图上模拟二阶质量-弹簧-阻尼器动力学，取代基于模板的变形，并通过记忆缓冲和自适应边权重捕捉时序依赖。"
primary_logic: "将3D高斯点构建为图结构，利用GNN自回归地预测节点速度和加速度，而无需预定义骨骼蒙皮，使得衣物的动态形变能够自然产生，并通过等距和阻尼正则化保持局部结构稳定。"
claims:
- "在4D-Dress数据集上新姿态合成任务中，我们的方法在所有子集上（00148/00170/00185/00187/00190）的PSNR、SSIM、LPIPS全面超越GART、GaussianAvatar、3DGS-Avatar、ExAvatar等基线方法。"
- "速度编码（VE）显著减少运动误差尖峰35.5%，并提升长序列动态和重复姿态下的渲染质量（w/ VE PSNR 25.65/26.84 vs w/o VE 24.47/24.69）。"
- "消融实验表明，添加物理启发的正则化和自适应弹簧系数带来+0.84 PSNR提升；速度编码窗口τ_v=11时PSNR提升+5.83，LPIPS下降40.3%；SMAD容量M=40k达到最佳性能。"
- "我们的方法在训练、测试和OOD运动序列间未表现出显著差异（p>0.05），表明良好的泛化能力；而基线方法在低运动相似度下感知质量显著下降。"
---

# Secondary Motion-Aware 3D Clothed Gaussian Avatars from Monocular Videos

> [!tip] 核心洞察
> 将3D高斯点构建为图结构，利用GNN自回归地预测节点速度和加速度，而无需预定义骨骼蒙皮，使得衣物的动态形变能够自然产生，并通过等距和阻尼正则化保持局部结构稳定。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于单目视频的次级运动感知3D着装高斯头像 |
| 英文题名 | Secondary Motion-Aware 3D Clothed Gaussian Avatars from Monocular Videos |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2A3Q2EtGTF) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Secondary Motion-Aware Deformation (SMAD) |
| Dataset | 4D-Dress (Subject 00148), ZJU-MoCap (Subject 394), LoCo-Human (Subject S01) |

> [!tip] 效果简介
> - 4D-Dress (Subject 00148) 上，PSNR / SSIM / LPIPS 为 24.74 / 0.9601 / 0.0397，对比 ExAvatar: 21.93 / 0.9536 / 0.0628，变化 +2.81 / +0.0065 / -0.0231。
> - ZJU-MoCap (Subject 394) 上，PSNR / SSIM / LPIPS 为 30.89 / 0.9677 / 0.0311，对比 HumanNeRF: 30.31 / 0.9642 / 0.0328，变化 +0.58 / +0.0035 / -0.0017。
> - LoCo-Human (Subject S01) 上，PSNR / SSIM / LPIPS 为 25.07 / 0.9483 / 0.0468，对比 ExAvatar: 23.46 / 0.9431 / 0.0515，变化 +1.61 / +0.0052 / -0.0047。

## 概要

### 问题瓶颈

现有的基于3D高斯泼溅（3DGS）的人体化身方法将衣物变形建模为当前身体姿态的函数，依赖参数化身体模板（如SMPL）和线性混合蒙皮，存在两个根本缺陷：

1. **缺乏时间连续性**：逐帧独立的变形机制无法捕获惯性驱动的次级运动（如裙摆抖动、宽松衣物的摆动），导致动态场景下出现时间不一致的渲染伪影。
2. **模板-几何不匹配**：在裸体SMPL模板表面初始化高斯点，与穿着宽松衣物的真实几何形状存在系统性偏差，造成高斯点分布误差和渲染质量下降。

### 核心方法

本文提出**次级运动感知变形**（Secondary Motion-Aware Deformation, SMAD），通过三个关键设计解决上述瓶颈：

- **个性化高斯初始化（PGI）**：利用可变形NeRF从单目视频中提取穿着衣物的规范密度场，直接生成与衣物形状对齐的高斯点云，消除对裸体模板的依赖。
- **速度编码高斯图**：将3D高斯点构建为图结构，通过速度缓冲记忆和SMPL姿态先验编码时序上下文，为自回归变形提供历史状态信息。
- **GNN自回归变形器**：在图节点上模拟二阶质量-弹簧-阻尼器动力学，通过消息传递图神经网络预测节点加速度和位置更新，使衣物动态形变自然产生，无需预定义骨骼蒙皮。

### 核心结论

1. **次级运动建模能力显著提升**：在4D-Dress数据集的宽松衣物受试者上，PSNR较最优基线ExAvatar提升最高达+2.81 dB，LPIPS降低0.0231（Table 1a）。
2. **速度编码是关键驱动因素**：速度编码窗口τ_v=11时PSNR提升+5.83，LPIPS降低40.3%，并使运动误差尖峰减少35.5%（Table 2, Figure 6）。
3. **物理启发正则化有效**：等距损失和阻尼损失联合自适应弹簧系数带来+0.84 PSNR提升，保证变形过程中的局部结构稳定（Table 2）。
4. **良好的分布外泛化**：在训练、测试和分布外运动序列间未表现出显著差异（p>0.05），而基线方法在低运动相似度下感知质量显著下降（Table 3, Figure J）。

### 方法谱系与知识库定位

本工作处于**3DGS化身**与**物理启发动态建模**的交叉点。与现有基于模板的方法形成对比：

| 方法 | 变形机制 | 模板依赖 | 时序建模 |
|------|---------|---------|---------|
| **GART** (Lei et al., 2024) | 预定义姿态变形 | 是 | 无 |
| **GaussianAvatar** (Hu et al., 2024a) | 骨架驱动变形 | 是 | 无 |
| **3DGS-Avatar** (Qian et al., 2024b) | 单目视频重建 | 是 | 无 |
| **ExAvatar** (Moon et al., 2024) | 显式动态外观 | 是 | 无 |
| **SMAD（本文）** | 自回归GNN图变形 | 否 | 速度编码+记忆缓冲 |

相较于神经隐式化身（如**NeuralBody**、**HumanNeRF**、**MonoHuman**），SMAD在保持3DGS实时渲染优势的同时，首次将图神经网络和二阶动力学引入化身变形，实现了对次级运动的物理一致性建模。

### 3D高斯化身建模的现状与瓶颈

近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的数字化身方法在渲染质量和速度上取得了显著进展，但现有方法在建模人体动态外观时存在一个根本性瓶颈：**变形被建模为当前身体姿态的瞬时函数**。具体而言，主流方法（如**GART** (Lei et al., 2024)、**GaussianAvatar** (Hu et al., 2024a)、**3DGS-Avatar** (Qian et al., 2024b)、**ExAvatar** (Moon et al., 2024)）依赖参数化身体模板（如SMPL）和线性混合蒙皮（LBS）来驱动高斯点的变形，这种设计存在两方面的结构性缺陷。

**第一，缺乏时间连续性，无法捕获次级运动。** 由于变形是逐帧独立计算的，系统对前一时刻的运动状态毫无记忆。当人体穿着宽松衣物（如裙子、外套）并进行动态运动时，衣物因惯性产生的摆动、抖动等次级运动（secondary motion）无法被建模。这些运动本质上是由历史速度和质量分布决定的二阶动力学现象，而基于静态姿态映射的变形机制天然无法捕捉这种时序因果链。

**第二，裸体模板初始化导致几何失配。** 现有方法通常在裸体SMPL模板表面采样点作为高斯的初始位置。当目标人物穿着宽松衣物时，衣物的实际几何形状与裸体模板之间存在显著偏差，导致高斯点的初始分布与真实表面不匹配。这不仅增加了后续优化的难度，还容易在渲染中产生伪影和几何失真。

### 核心动机与解决思路

针对上述瓶颈，本文的核心动机是：**将3D高斯点的变形建模为一个具有记忆能力的二阶动态系统，而非当前姿态的静态函数**。这一思路的因果杠杆在于引入速度和加速度作为显式状态变量，使系统能够模拟惯性驱动的运动。

具体而言，本文提出两大创新：

- **模板无关的个性化高斯初始化**：通过可变形NeRF从单目视频中直接估计穿着衣物的规范密度场，提取与真实衣物几何对齐的高斯点云，从根本上消除裸体模板带来的初始化偏差。
- **次级运动感知变形（SMAD）**：将高斯点构建为图结构，通过自回归图神经网络（GNN）预测节点的速度和加速度，模拟质量-弹簧-阻尼器动力学，使衣物动态形变能够自然产生，而无需预定义骨骼蒙皮。

这一设计使得系统在宽松衣物和动态运动场景下能够产生时序一致的、物理上合理的次级运动，填补了现有3DGS化身方法的关键能力缺口。

## 核心方法与创新机理

本文的核心创新在于用**速度编码的自回归图神经网络（GNN）变形器**取代了传统3DGS化身中依赖参数化身体模板的变形范式。这一转变解决了两个互为因果的瓶颈：（1）现有方法将变形建模为当前身体姿态的函数，缺乏时间连续性，无法捕获惯性驱动的次级运动（如裙摆抖动）；（2）在裸体SMPL模板表面初始化高斯点，与宽松衣物的几何形状不匹配，导致高斯分布误差和渲染伪影。

### 变形机制的范式转换：从模板驱动到图网络自回归预测

传统方法（如GaussianAvatar、ExAvatar、3DGS-Avatar）的核心变形逻辑是：给定当前帧的SMPL姿态参数，通过线性混合蒙皮（LBS）将规范空间的高斯点逐帧独立地变形到观测空间。这种“姿态→变形”的单步映射缺乏对历史运动状态的记忆，无法产生惯性效应——例如，当人物突然停止时，衣摆应继续向前摆动，而非瞬间静止。

SMAD模块的变形机制发生了根本性变化（**changed slot: 变形机制**）。它将3D高斯点构建为图结构，每个节点被视为一个具有质量 $g_i$ 的质点，其运动遵循二阶质量-弹簧-阻尼器动力学：

$$\mathbf{F}_i^{\mathrm{ext}}(t) = g_i \ddot{\mathbf{x}}_i(t) + \gamma_i \dot{\mathbf{x}}_i(t) + \sum_j k_{ij} \big( \mathbf{x}_i(t) - \mathbf{x}_j(t) - \mathbf{L}_{ij}^{\mathrm{rest}} \big)$$

关键设计在于：**不显式计算外力**，而是让消息传递GNN自回归地预测节点加速度 $\mathbf{a}_i(t)$，作为神经代理替代力计算。GNN的节点特征 $\mathbf{h}_i$ 由位置、缓冲速度记忆向量和SMPL姿态先验拼接而成，通过消息传递聚合邻域信息后输出加速度更新。随后通过显式欧拉积分更新速度和位置：

$$\mathbf{v}_i(t+\Delta t) = \mathbf{v}_i(t) + \Delta t \cdot \mathbf{a}_i(t), \quad \mathbf{x}_i(t+\Delta t) = \mathbf{x}_i(t) + \Delta t \cdot \mathbf{v}_i(t+\Delta t)$$

这一自回归机制使得衣物的动态形变能够自然产生，无需预定义骨骼蒙皮。消融实验证实，SMAD节点容量 $M=40k$ 相较于无SMAD基线带来 **+3.60 PSNR，SSIM +0.017，LPIPS减少32.2%**（Table 2 右侧块）。物理启发的等距正则化（保持局部表面面积）和阻尼正则化（抑制高频振动）进一步贡献 **+0.84 PSNR，LPIPS降低10.3%**（Table 2 A1）。自适应弹簧系数 $k_{ij}$ 在无监督条件下自动区分刚性与非刚性部位，带来额外增益（Table 2 A2）。

### 模板无关的高斯初始化

传统方法在裸体SMPL模板表面采样点作为高斯初始位置（**changed slot: 高斯初始化**）。当目标人物穿着宽松外套或长裙时，衣物表面与裸体模板之间存在显著几何偏差，导致高斯点分布在错误的位置，渲染时产生模糊和伪影。

本文提出个性化高斯初始化（PGI），利用可变形NeRF从单目视频中估计穿着衣物的规范密度场，通过时间平均密度 $\bar{\boldsymbol{\sigma}}(\mathbf{x}) = \frac{1}{T} \sum_t \boldsymbol{\sigma}(\mathbf{x}, t)$ 提取与衣物轮廓对齐的高斯点云。这一设计消除了对裸体模板的依赖，使高斯原语直接贴合衣物的真实几何形状。视觉消融（Figure 6 右）显示，PGI对捕获衣物细节纹理（如褶皱、图案）至关重要。

### 时序上下文的系统编码

传统方法仅以当前姿态为条件，缺乏历史状态信息（**changed slot: 运动上下文编码**）。SMAD引入速度编码（VE）机制：计算节点瞬时速度 $\mathbf{v}_i(t) = \frac{\mathbf{x}_i(t) - \mathbf{x}_i(t-\Delta t)}{\Delta t}$，并缓存过去 $\tau_v$ 个速度向量作为记忆缓冲，与SMPL姿态先验序列拼接输入GNN。

VE的效果在消融实验中极为显著：窗口 $\tau_v=11$ 相较于无VE基线（$\tau_v=1$）**PSNR提升+5.83，LPIPS降低40.3%**（Table 2 中间块）。在长序列测试中，VE使运动误差尖峰减少35.5%（Figure 6 左），并在动态序列（PSNR 25.65 vs 24.47）和重复姿态序列（PSNR 26.84 vs 24.69）上均显著优于无VE版本（Table 5）。这验证了多帧历史状态对缓解自回归误差累积和捕捉长程时序依赖的关键作用。

### 创新点的协同效应

三个changed slot并非孤立改进，而是形成因果闭环：PGI提供与衣物几何匹配的初始高斯分布，使图结构的节点位置具有物理意义；速度编码为GNN提供时序上下文，使其能够推理惯性效应；GNN自回归变形器则利用这些信息模拟二阶动力学，产生自然的次级运动。消融实验的全量配置（A3）相较于基线（A0）实现 **+2.68 PSNR和31.0% LPIPS降低**（Table 2），证实了各组件的协同增益。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2A3Q2EtGTF/figures/006_Figure_2.jpg]]
*Figure 2: To model secondary motions in 3DGS-based avatars, we introduce a two-stage framework: (1) Personalized Gaussian Initialization using a deformable NeRF to estimate canonical Gaussians $\mathcal G ^ { \mathrm { c } }$ , and (2) Secondary Motion-Aware Deformation. $\breve { \mathscr { G } ^ { \mathrm { c } } }$ are structured as a Gaussian graph Γ, processed by a GNN-based autoregressive deformer, and decoded via $U _ { \psi }$ into deformed Gaussians $\bar { \boldsymbol { \mathcal { G } } } ^ { \mathrm { d } }$ . Motion descriptors derived from SMPL poses Θ guide temporally coherent deformation. Then GS Renderer then synthesizes the final images

本文提出一个两阶段框架，核心目标是解决现有3DGS化身方法在宽松衣物和次级运动建模上的根本瓶颈：现有方法将变形建模为当前身体姿态的函数，依赖参数化身体模板（SMPL）和线性混合蒙皮，缺乏时间连续性，无法捕获惯性驱动的次级运动（如裙摆抖动），且裸体模板初始化与宽松衣物的几何形状不匹配，导致高斯点分布误差和渲染伪影。

框架的因果机制在于：通过**速度编码的自回归图神经网络（GNN）变形器**，在构造的高斯节点图上模拟二阶质量-弹簧-阻尼器动力学，取代基于模板的逐帧独立变形，并通过记忆缓冲和自适应边权重捕捉时序依赖。整体流程如图2所示，分为两个阶段：

**阶段一：个性化高斯初始化（Personalized Gaussian Initialization, PGI）**

该阶段解决了裸体模板与穿着衣物几何不匹配的根本问题。现有方法在SMPL裸体模板表面采样高斯点作为初始位置，当受试者穿着宽松衣物时，高斯点分布远离真实表面，导致后续变形和渲染产生伪影。本文通过可变形NeRF（deformable NeRF）从单目视频中估计穿着衣物的规范密度场，提取时间平均密度 $\bar{\boldsymbol{\sigma}}(\mathbf{x}) = \frac{1}{T} \sum_t \boldsymbol{\sigma}(\mathbf{x}, t)$，从中采样生成与衣物轮廓对齐的个性化高斯点云 $\mathcal{G}^c$，无需裸体模板。这一设计使得高斯原语在初始化阶段即忠实于受试者的穿着几何形态，为后续变形提供了正确的空间起点。

**阶段二：次级运动感知变形（Secondary Motion-Aware Deformation, SMAD）**

该阶段是框架的核心创新，包含三个紧密耦合的子模块：

1. **高斯图构建**：对阶段一提取的规范高斯点进行体素下采样，通过k-NN构建图结构，节点为高斯点，边权重由距离高斯核定义。这一图结构降低了计算复杂度，同时保留了局部几何邻接关系，为GNN消息传递提供拓扑基础。

2. **速度编码（Velocity Encoding, VE）**：计算每个节点速度 $\mathbf{v}_i(t) = \frac{\mathbf{x}_i(t) - \mathbf{x}_i(t-\Delta t)}{\Delta t}$，缓存历史速度记忆向量（窗口大小 $\tau_v$），与SMPL姿态先验拼接作为节点输入特征。速度编码引入了时间连续性，使模型能够感知运动趋势而非仅依赖当前姿态，这是捕获惯性驱动次级运动的关键。

3. **GNN自回归变形器**：将每个高斯节点建模为遵循二阶质量-弹簧-阻尼器动力学的质点：
   $$\mathbf{F}_i^{\mathrm{ext}}(t) = g_i \ddot{\mathbf{x}}_i(t) + \gamma_i \dot{\mathbf{x}}_i(t) + \sum_j k_{ij} \big( \mathbf{x}_i(t) - \mathbf{x}_j(t) - \mathbf{L}_{ij}^{\mathrm{rest}} \big)$$
   实际实现中，GNN通过学习更新函数 $\mathbf{a}_i(t) = G_{\theta}\big(\mathbf{h}_i^{\ell}(t), \mathbf{m}_i^{\mathrm{agg}}(t)\big)$ 隐式替代显式力计算，自回归地预测节点加速度、速度和位置更新，并解码颜色、不透明度、协方差等渲染属性。自适应弹簧系数 $k_{ij}$ 在无监督条件下区分刚性与非刚性部件，使衣物的动态形变能够自然产生。

**正则化约束**：为保证变形稳定性，引入等距损失 $\mathcal{L}_{\mathrm{iso}}$（保持局部表面面积）和阻尼损失 $\mathcal{L}_{\mathrm{damp}}$（抑制高频振动），总损失为：
$$\mathcal{L}_{\mathrm{SMAD}} = \mathcal{L}_{\mathrm{RGB}} + \lambda_{\mathrm{iso}} \mathcal{L}_{\mathrm{iso}} + \lambda_{\mathrm{damp}} \mathcal{L}_{\mathrm{damp}}$$

**输入输出流**：输入为单目视频帧序列 $\{I_1, ..., I_T\}$ 及对应的SMPL姿态参数 $\Theta$。阶段一输出规范高斯点云 $\mathcal{G}^c$；阶段二以 $\mathcal{G}^c$ 和姿态序列为输入，经过速度编码高斯图和GNN自回归变形器，输出逐帧变形后的高斯集合 $\mathcal{G}_t^{\mathrm{d}} = \{ (\mu_{t,i}, \Sigma_{t,i}, c_{t,i}, \alpha_{t,i}) \}_{i=1}^{N}$，最终通过3DGS渲染器合成图像。

消融实验验证了各模块的因果贡献：速度编码窗口 $\tau_v=11$ 时PSNR提升+5.83，LPIPS降低40.3%，运动误差尖峰减少35.5%（Figure 6, Table 2）；物理启发正则化和自适应弹簧系数带来+0.84 PSNR提升；SMAD节点数 $M=40k$ 达到最佳性能。这些证据表明，框架通过图结构动力学建模和时序编码，有效突破了现有方法在次级运动建模上的瓶颈。

本文提出的两阶段框架（Figure 2）围绕一个核心洞察展开：将3D高斯点构建为图结构，利用GNN自回归地预测节点速度和加速度，从而绕开对预定义骨骼蒙皮的依赖，使衣物的动态形变能够自然产生。以下聚焦于次级运动感知变形（SMAD）模块的关键设计与公式。

### 速度编码高斯图构建

传统方法将变形建模为当前身体姿态的函数，逐帧独立预测，缺乏时间连续性。SMAD通过速度编码（Velocity Encoding, VE）引入时序上下文：对每个高斯节点 $i$，计算其瞬时速度

$$\mathbf{v}_i(t) = \frac{\mathbf{x}_i(t) - \mathbf{x}_i(t-\Delta t)}{\Delta t}$$

并缓存过去 $\tau_v$ 个速度记忆向量，与SMPL姿态先验拼接作为节点输入特征。这一设计使变形器能够捕捉惯性驱动的次级运动（如裙摆抖动），而非仅响应瞬时姿态。消融实验表明，$\tau_v=11$ 时PSNR相较无VE基线（$\tau_v=1$）提升 **+5.83**，LPIPS降低 **40.3%**（Table 2），且运动误差尖峰减少 **35.5%**（Figure 6）。

### 图神经网络自回归变形器

SMAD将下采样后的高斯节点通过k-NN构建图结构，边权重由距离高斯核定义。每个节点 $i$ 被建模为点质量 $g_i$，其运动遵循二阶质量-弹簧-阻尼器动力学：

$$\mathbf{F}_i^{\mathrm{ext}}(t) = g_i \ddot{\mathbf{x}}_i(t) + \gamma_i \dot{\mathbf{x}}_i(t) + \sum_j k_{ij} \big( \mathbf{x}_i(t) - \mathbf{x}_j(t) - \mathbf{L}_{ij}^{\mathrm{rest}} \big)$$

其中 $\gamma_i$ 为阻尼系数，$k_{ij}$ 为自适应弹簧刚度（无监督地区分刚性与非刚性区域），$\mathbf{L}_{ij}^{\mathrm{rest}}$ 为规范空间中的静止边长度。与传统显式力计算不同，SMAD使用消息传递GNN学习更新函数，直接预测节点加速度：

$$\mathbf{a}_i(t) = G_{\theta}\big(\mathbf{h}_i^{\ell}(t), \mathbf{m}_i^{\mathrm{agg}}(t)\big)$$

其中 $\mathbf{h}_i^{\ell}$ 为节点特征（包含位置、速度记忆、姿态先验），$\mathbf{m}_i^{\mathrm{agg}}$ 为聚合的邻域消息。随后通过显式欧拉积分更新速度和位置：

$$\mathbf{v}_i(t+\Delta t) = \mathbf{v}_i(t) + \Delta t \,\mathbf{a}_i(t)$$

$$\mathbf{x}_i(t+\Delta t) = \mathbf{x}_i(t) + \Delta t \,\mathbf{v}_i(t+\Delta t)$$

GNN同时解码颜色、不透明度、协方差等渲染属性。

### 物理启发的正则化

为保证变形稳定性与局部结构保真，引入两项正则化损失。总损失函数为：

$$\mathcal{L}_{\mathrm{SMAD}} = \mathcal{L}_{\mathrm{RGB}} + \lambda_{\mathrm{iso}} \mathcal{L}_{\mathrm{iso}} + \lambda_{\mathrm{damp}} \mathcal{L}_{\mathrm{damp}}$$

- **等距损失 $\mathcal{L}_{\mathrm{iso}}$**：惩罚相邻节点间测地距离的偏差，保持局部表面面积不变，防止衣物过度拉伸或塌缩。
- **阻尼损失 $\mathcal{L}_{\mathrm{damp}}$**：正则化速度幅值 $\sum_t \|\mathbf{v}_i(t)\|_2^2$，抑制高频振动和动态不稳定。

消融实验证实，添加上述物理启发正则化与自适应弹簧系数带来 **+0.84 PSNR** 提升（Table 2, A1），而SMAD节点数 $M=40\mathrm{k}$ 时相较无SMAD基线PSNR提升 **+3.60**，SSIM **+0.017**，LPIPS降低 **32.2%**（Table 2右侧块）。

### 个性化高斯初始化

作为SMAD的前置阶段，该方法通过可变形NeRF估计穿着衣物的规范密度场 $\bar{\boldsymbol{\sigma}}(\mathbf{x}) = \frac{1}{T}\sum_t \boldsymbol{\sigma}(\mathbf{x}, t)$，从中提取个性化高斯点，避免裸体SMPL模板与宽松衣物几何不匹配导致的高斯分布误差。此初始化与SMAD协同，使变形器在无骨骼蒙皮先验的条件下自然产生次级运动。

## 实验与关键发现

### 主要结果

我们在三个数据集上进行了系统评估：4D-Dress（宽松衣物、新姿态合成）、ZJU-MoCap（紧身衣物、新视角合成）和LoCo-Human（宽松衣物、真实场景）。表1汇总了定量对比结果。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2A3Q2EtGTF/figures/030_Table_1.jpg]]
*Table 1: Quantitative comparisons across (a) novel pose synthesis on 4D-Dress, (b) novel view synthesis on ZJU-MoCap, and (c) LoCo-Human in-the-wild. We highlight the best (bold) and second-best (underline) performance in each case*

**4D-Dress新姿态合成**。如表1(a)所示，我们的方法在所有五个受试者上全面超越GART、GaussianAvatar、3DGS-Avatar和ExAvatar等基于3DGS的化身方法。以受试者00148为例，PSNR达到24.74，相较第二名ExAvatar（21.93）提升+2.81 dB，LPIPS从0.0628降至0.0397（降低37%）。该数据集的宽松裙摆和外套产生显著次级运动，基于骨架蒙皮的基线方法无法捕获这些动态细节，导致衣物区域出现严重模糊和几何失真（图3）。

**ZJU-MoCap新视角合成**。在紧身衣物场景下（表1(b)），我们的方法同样取得最优或次优性能。受试者394上PSNR达30.89，略优于HumanNeRF（30.31）。需要指出，ZJU-MoCap的衣物形变幅度有限，次级运动不显著，因此各方法间差距较小，但我们的方法在重复运动序列中仍展现出更好的视角一致性（图5）。

**LoCo-Human真实场景**。该数据集专门构建以包含宽松衣物和动态运动，弥补现有基准缺乏次级运动评估的不足。如表1(c)所示，在受试者S01上PSNR达25.07，相较ExAvatar（23.46）提升+1.61 dB。图4的定性对比显示，基线方法在裙摆和宽松外套区域出现明显的几何塌陷和纹理模糊，而我们的方法保持了衣物的自然垂坠和抖动。

### 消融实验

表2从三个维度系统消融各组件的贡献。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2A3Q2EtGTF/figures/031_Table_2.jpg]]
*Table 2: Ablation study on the effectiveness of our mainly proposed components. Three column blocks report (Left) loss/arch. design, (Middle) velocity encoding, and (Right) SMAD capacity M*

**损失函数与架构设计**。以无物理正则化、无自适应弹簧系数的朴素GNN为基线（A0，PSNR 25.21），逐步添加物理启发的有限差分正则化（A1，等距损失+阻尼损失）带来+0.84 PSNR提升和10.3% LPIPS下降。引入自适应弹簧刚度系数$k_{ij}$（A2）使模型在无监督条件下自动区分刚性与非刚性区域，进一步提升动态场景渲染质量。采用带边特征嵌入的高级消息传递策略（A3）再贡献+0.68 PSNR和10.2% LPIPS下降。完整配置（A3）相较基线累计提升+2.68 PSNR，LPIPS降低31.0%。

**速度编码窗口**。速度编码（VE）是捕获时序依赖的核心机制。当速度记忆窗口$\tau_v=1$（即仅使用当前帧差分作为速度估计，等价于无VE基线）时，PSNR仅为22.06。随着$\tau_v$增大，性能持续提升，在$\tau_v=11$时达到峰值（PSNR 27.89，LPIPS 0.040），相较无VE基线PSNR提升+5.83，LPIPS降低40.3%。这验证了多帧历史状态对建模惯性驱动次级运动的必要性。

**SMAD容量**。SMAD节点数$M$控制高斯图的稀疏程度。$M=0$（无SMAD，即纯基于模板的变形）时PSNR为24.29。$M=40k$达到最佳性能（PSNR 27.89，SSIM 0.963，LPIPS 0.040），相较无SMAD基线PSNR提升+3.60，SSIM提升+0.017，LPIPS降低32.2%。过小的$M$导致图结构过于稀疏，无法充分建模局部形变；过大的$M$则引入冗余计算且性能饱和。

**视觉消融**。图6展示了各模块的定性效果。左栏表明VE显著减少运动误差尖峰（定量上尖峰减少35.5%），使变形在时序上更加连贯。右栏显示个性化高斯初始化（PGI）能够捕获衣物细节纹理（如褶皱和缝线），而裸体模板初始化则丢失这些信息。SMAD模块保证了衣物动态的鲁棒性，避免基线方法中常见的裙摆穿透和异常拉伸。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2A3Q2EtGTF/figures/032_Figure_6.jpg]]
*Figure 6: Ablation study on the visual effectiveness of (left) VE, (right) PGI, and SMAD. VE significantly reduces the motion error by encouraging temporal consistent deformation. PGI contributes to capturing finedetailed clothing patterns, and SMAD sufficiently guarantees the robustness of clothing dynamics*

### 泛化性分析

为评估模型在分布外（OOD）运动上的泛化能力，我们在训练集、测试集和OOD运动序列上分别评估。表3显示，训练集PSNR为28.64，测试集为27.89，OOD序列为26.51。三者间无显著差异（$p>0.05$），表明模型性能不受运动分布偏移的显著影响。图J(b)进一步揭示，基线方法的LPIPS随运动相似度（NCC）降低而急剧恶化（低相似度时LPIPS约85），而我们的方法在整个相似度范围内保持稳定且较低的LPIPS（约40-50）。这表明自回归GNN变形器学到的是通用的物理动态规律，而非对训练姿态的过拟合。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2A3Q2EtGTF/figures/033_Table_3.jpg]]
*Table 3: Quantitative results on train/test, and out-of-distribution (OOD) motion sequences to evaluate generalization capability of our method (blue: p-val p > 0 . 0 5 )*

表4对比了SMAD的不同架构选择：MLP、vanilla GNN和我们的完整GNN设计。完整GNN在测试集上PSNR达27.89，优于vanilla GNN（27.12）和MLP（26.45），验证了图结构消息传递对建模高斯点间交互的必要性。

### 误差累积分析

自回归模型面临误差随序列长度累积的风险。表5在长动态序列和重复运动序列上消融速度编码。引入VE后，动态序列PSNR从24.47提升至25.65，重复序列从24.69提升至26.84。VE通过缓存多帧历史状态，使模型在长序列中保持变形一致性，缓解了单步误差的逐帧放大。图6（左）进一步证实VE使运动误差尖峰减少35.5%。

### 失败模式与局限性

尽管整体性能优异，我们的方法在以下场景仍存在不足：

1. **突变大幅度运动**：当驱动姿态发生突然且剧烈的变化时（如快速转身或跳跃），自回归预测可能超出训练分布，导致节点加速度估计失准，表现为衣物局部撕裂或异常振荡。这是自回归模型的固有局限。

2. **多件衣物交互**：当前高斯图为单层结构，将所有衣物视为一个整体变形体。当受试者穿着多层衣物（如外套+内搭+裙摆）时，模型无法独立预测各层的相对运动，导致层间穿透或运动不一致。

3. **单视角语义分割**：构建分层图结构以建模多件衣物交互的前提是精确的衣物语义分割，但单视角视频中实现这一目标仍具挑战性，限制了该方向的进一步发展。

4. **训练效率**：图J(a)的t-SNE可视化显示OOD姿态与训练姿态在隐空间中存在一定距离。虽然统计检验未检测到显著差异，但极端OOD场景下的性能下降趋势仍然存在，引入双向时间上下文或生成式流匹配可能是潜在的改进方向。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_2A3Q2EtGTF/figures/044_Figure_37.jpg]]
*Figure 37: (b) Figure J: (a) Visual check of in-distribution (blue) and out-of-distribution (orange) driving poses with t-sne plot. (b) Average perceptual metric (LPIPS; lower is better) with standard error plot of 4D-Dress over motion similarity between train and test set. Our method (red) maintains consistent rendering performance even for test motions with low similarity to the training motion—showing relatively less performance degradation compared to high-similarity cases—whereas a baseline (blue) exhibits a significant drop in perceptual quality when handling test motions with low motion similarity*

## 定位与知识库关联

### 1. 与现有3DGS化身的核心差异

当前3DGS化身方法的主流范式可概括为“参数化模板 + 逐帧姿态驱动变形”。具体而言，**GART** (Lei et al., 2024)、**Gaussian Avatar** (Hu et al., 2024a)、**3DGS-Avatar** (Qian et al., 2024b) 和 **ExAvatar** (Moon et al., 2024) 等工作均以SMPL裸体模板为规范空间，通过线性混合蒙皮（LBS）将当前帧的姿态参数映射为高斯的位移。这一范式存在两个结构性瓶颈：

**瓶颈一：变形缺乏时间连续性。** 上述方法将每帧变形建模为当前身体姿态的确定性函数，帧与帧之间独立计算，无法捕获惯性驱动的次级运动（如裙摆抖动、宽松衣物的滞后摆动）。当驱动姿态与训练分布偏离时，这种“无记忆”变形机制会累积误差，导致渲染伪影。

**瓶颈二：裸体模板与衣物几何不匹配。** 在SMPL模板表面采样高斯初始位置，隐含假设衣物紧贴身体表面。对于宽松衣物（如裙子、外套），这种初始化将高斯点强制约束在与实际几何不符的位置，后续变形网络需要额外“纠正”这一系统性偏差，增加了优化难度。

本文提出的**次级运动感知变形（SMAD）**从两个维度突破了上述范式：第一，引入速度编码的自回归图神经网络（GNN）变形器，在构造的高斯节点图上模拟二阶质量-弹簧-阻尼器动力学，取代基于模板的变形，使衣物动态形变能够自然产生；第二，通过可变形NeRF估计穿着衣物的规范密度场，提取个性化高斯点，无需裸体模板初始化。

### 2. 与神经隐式化身的关系

在3DGS化身兴起之前，神经隐式化身（NeRF-based）是该领域的主导方法。**NeuralBody** (Peng et al., 2021a) 将隐式表示锚定在SMPL顶点上，通过稀疏卷积扩散潜在编码；**HumanNeRF** (Weng et al., 2022) 和 **MonoHuman** (Yu et al., 2023) 进一步探索了单目视频下的动态人体重建；**ARAH** (Wang et al., 2022) 则关注姿态驱动的体渲染。这些方法的共同局限在于：隐式表示在渲染时需要密集采样和体渲染，计算开销大，且同样依赖SMPL模板作为几何先验，难以处理宽松衣物。

SMAD继承了神经隐式方法中“从数据学习变形场”的思想，但将其迁移到显式高斯表示上，并通过图结构建模节点间交互，实现了更高效的渲染和更灵活的变形建模。

### 3. 关键设计选择与消融证据

SMAD的核心设计选择均经过消融验证：

- **物理启发的正则化与自适应弹簧系数**：在基础配置上添加等距损失、阻尼损失和自适应弹簧刚度$k_{ij}$，带来**+0.84 PSNR**和**-10.3% LPIPS**的提升（Table 2, A1→A2），表明物理约束对保持局部结构稳定至关重要。
- **速度编码窗口**：将速度历史窗口从$\tau_v=1$（无记忆）扩展至$\tau_v=11$时，PSNR提升**+5.83**，LPIPS降低**40.3%**（Table 2, Middle block），且运动误差尖峰减少**35.5%**（Figure 6），证实了时序上下文对抑制误差累积的关键作用。
- **SMAD节点容量**：将图节点数提升至$M=40k$时，相较于无SMAD基线，PSNR提升**+3.60**，SSIM提升**+0.017**，LPIPS降低**32.2%**（Table 2, Right block），表明足够的图容量对建模复杂衣物动态是必要的。

### 4. 适用边界与局限性

**适用场景**：SMAD在包含宽松衣物和动态运动的数据集上表现突出。在4D-Dress数据集的新姿态合成任务中，所有五个受试者的PSNR、SSIM、LPIPS全面超越ExAvatar等基线（Table 1a）；在专门构建的LoCo-Human数据集上同样保持显著优势（Table 1c）。泛化性分析表明，SMAD在训练、测试和分布外运动序列间的性能差异不显著（$p>0.05$，Table 3），而基线方法在低运动相似度下感知质量显著下降。

**局限一：突然且大幅度运动变化的处理困难。** 由于SMAD采用自回归预测，当驱动姿态超出训练分布时，节点加速度的估计精度下降。这是自回归模型的固有局限，可能通过双向时间上下文或生成式流匹配技术缓解。

**局限二：单层高斯图无法建模多件衣物交互。** 当前图结构将所有高斯节点视为单一系统，无法独立预测不同服装部件（如外套与内搭）的运动。这限制了在多层衣物场景下的精细控制。

**局限三：单视角衣物分割的挑战。** 实现分层图结构的前提是从单视角视频中精确分割多件衣物，这仍是一个开放问题。

### 5. 开放问题

1. **分布外加速度预测**：如何预测超出训练分布的复杂加速度分布？双向时间上下文编码或生成式流匹配技术可能提供解决方案。
2. **多件衣物分层建模**：如何从单视角视频中实现高精度的多件衣物语义分割，以支持分层高斯图建模多件衣物的独立运动与交互？
3. **物理模拟约束的引入**：是否可以通过引入显式物理模拟约束（如布料本构模型）来进一步提升分布外运动的泛化能力？

## 原文 PDF

![[paperPDFs/ICLR_2026/Secondary_Motion_Aware_3D_Clothed_Gaussian_Avatars_from_Monocular_Videos.pdf]]

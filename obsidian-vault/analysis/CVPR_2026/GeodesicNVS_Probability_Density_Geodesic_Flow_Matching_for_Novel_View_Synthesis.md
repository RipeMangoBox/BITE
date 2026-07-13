---
title: "GeodesicNVS: Probability Density Geodesic Flow Matching for Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeodesicNVS_Probability_Density_Geodesic_Flow_Matching_for_Novel_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- PF
- GeodesicNVS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将数据映射为确定性流，并沿数据流形测地线约束插值路径，使变换保持视图一致性。
primary_logic: 通过概率密度测地线流匹配，使插值轨迹对齐数据流形的高密度区域；利用教师-学生蒸馏框架将测地线优化到环境空间，实现高效且几何一致的视图合成。
claims:
- Linear-D2D-FM 在 Objaverse 上 FID 5.4324，优于 Free3D 的 5.5434（-0.111），表明确定性数据对偶流匹配可提升一致性。
- PDG-FM 在缩减训练设置下 FID 10.4010，相比 Linear-D2D-FM 的 11.8124 降低 1.4114，SSIM 从 0.8736 提升至 0.8768，验证测地线插值有效性。
- 测地线插值平均光流幅度（AOFM）13.6968，显著高于线性插值 11.9875，表明路径更符合相机旋转，而非静态混合。
- 优化后的测地线路径在训练集上具有更低的欧拉-拉格朗日残差，满足测地线方程条件，与感知和几何一致性提升一致。
---

# GeodesicNVS: Probability Density Geodesic Flow Matching for Novel View Synthesis

> [!tip] 核心洞察
> 通过概率密度测地线流匹配，使插值轨迹对齐数据流形的高密度区域；利用教师-学生蒸馏框架将测地线优化到环境空间，实现高效且几何一致的视图合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeodesicNVS：基于概率密度测地线流匹配的新视角合成方法 |
| 英文题名 | GeodesicNVS: Probability Density Geodesic Flow Matching for Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01010) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | PDG-FM |
| Dataset | Objaverse test, Objaverse |

> [!tip] 效果简介
> - Objaverse test 上，FID ↓ 5.4324 (Linear-D2D-FM) vs 5.5434 (Free3D) (-0.1110)；PSNR ↑ 20.8447 (Linear-D2D-FM) vs 20.8246 (Naive FM) (+0.0201)。
> - Objaverse (reduced setup) 上，FID ↓ 10.4010 (PDG-FM) vs 11.8124 (Linear-D2D-FM) (-1.4114)；SSIM ↑ 0.8768 (PDG-FM) vs 0.8736 (Linear-D2D-FM) (+0.0032)。

## 概要

新视角合成（Novel View Synthesis, NVS）的目标是从稀疏输入视图生成任意相机姿态下的场景图像。当前主流方法依赖条件扩散模型，通过随机噪声到数据的去噪过程学习视图变换。然而，扩散模型的**随机性破坏了视图间的确定性几何结构**，导致生成结果在空间一致性上出现偏差——同一场景的不同视角可能产生纹理漂移或几何错位。

本文的核心洞察是：**将新视角合成重新定义为数据到数据的确定性流匹配问题，并使插值轨迹沿数据流形的概率密度测地线行进**。具体而言，作者提出 **Probability Density Geodesic Flow Matching (PDG-FM)** 框架，包含两个关键设计：

1. **Data-to-Data Flow Matching (D2D-FM)**：摒弃噪声到数据的随机扩散，直接学习成对视图之间的确定性速度场，从结构上保证映射的可逆性与一致性。
2. **概率密度测地线插值**：在线性插值基础上引入环境空间校正网络，使插值路径沿数据流形的高密度区域弯曲，从而生成几何上更忠实的中间视图。测地线优化通过教师-学生蒸馏框架实现——教师在 DDIM 前向潜空间中以密度分数为引导优化测地线，学生将优化结果蒸馏回环境空间。

**主要结果**：
- Linear-D2D-FM（线性插值基线）在 Objaverse 测试集上取得 FID 5.4324，优于扩散模型 Free3D 的 5.5434（−0.111），且仅需 10 次函数评估（NFE）即可保持性能优势。
- PDG-FM 在缩减训练设置下相比 Linear-D2D-FM 将 FID 从 11.8124 降至 10.4010（−1.4114），SSIM 从 0.8736 提升至 0.8768，验证了测地线插值的有效性。
- 测地线路径的平均光流幅度（AOFM）为 13.6968，显著高于线性插值的 11.9875，表明路径更贴合相机旋转而非静态混合，且优化后的测地线在训练集上具有更低的欧拉-拉格朗日残差，满足测地线方程条件。

**方法定位**：PDG-FM 属于确定性流匹配范式，区别于 Zero-1-to-3（扩散模型）、EscherNet（多视图扩散）、Free3D（无 3D 表示的扩散模型）以及 Metric FM（学习黎曼度量的流匹配）。其核心贡献在于将几何一致性显式编码为插值路径的密度测地线约束，而非依赖扩散模型的隐式正则。



### 新视角合成中的确定性困境

新视角合成（Novel View Synthesis, NVS）要求从单一或少量源视图生成任意相机姿态下的目标视图，其核心挑战在于保持跨视图的几何一致性与语义保真度。近年来，以扩散模型为代表的条件生成方法在该领域取得了显著进展，代表性工作包括 **Zero-1-to-3**（Liu et al., 2023）、**EscherNet**（Xin et al., 2024）和 **Free3D**（Zheng & Vedaldi, CVPR 2024）等。然而，这类方法存在一个根本性的瓶颈：**扩散模型的随机性破坏了视图间的确定性映射关系，导致生成结果在结构上缺乏一致性**。

具体而言，传统条件扩散模型学习的是从噪声到数据的随机转换过程。即使给定相同的源视图和相机变换条件，每次采样都可能产生不同的目标视图，这使得模型难以捕捉新视角合成中固有的确定性几何变换——相机旋转本质上是一个确定性的单射映射，而非一对多的随机过程。这一矛盾构成了当前扩散式 NVS 方法在视图一致性上的理论上限。

### 流匹配的机遇与线性路径的局限

流匹配（Flow Matching, FM）提供了一条突破上述瓶颈的路径。与扩散模型不同，流匹配学习的是从源分布到目标分布的确定性速度场，理论上能够建立一对一的映射关系。然而，现有流匹配方法（如 Naive FM）通常采用**噪声到数据**的建模范式，其插值路径为简单的线性轨迹：

$$x_t = (1-t)x_0 + t x_1$$

这种线性插值虽然计算高效，但忽视了数据流形的几何结构。对于新视角合成任务而言，线性路径在两个视图之间直接混合像素，而非遵循相机旋转所对应的自然变换轨迹，导致中间状态偏离数据流形的高密度区域，产生语义不连贯的过渡结果。

### 密度测地线的几何直觉

在黎曼几何框架下，数据流形上两点之间的最优路径不应是环境空间中的直线，而应是**测地线**——即流形上局部最短的曲线。当度量张量 $G(x) = p(x)^{-2} I$ 被定义为与数据概率密度成反比时，测地线自然倾向于穿越高密度区域，从而保证路径上的每一点都具有高似然性。这一性质恰好契合新视角合成的需求：相机旋转对应的视图变换序列应当始终保持在自然图像的流形上，而非退化为不真实的混合图像。

满足上述密度测地线的路径由欧拉-拉格朗日方程刻画：

$$\ddot{\gamma} + \|\dot{\gamma}\|^2 \left( I - \hat{\dot{\gamma}}\hat{\dot{\gamma}}^{\mathsf{T}} \right) \nabla \log p(\gamma) = 0$$

该方程表明，测地线的曲率由密度分数的梯度驱动，迫使路径向高概率区域弯曲。然而，直接在高维潜空间中求解此方程面临两大挑战：其一，数据密度的精确估计本身是一个困难问题；其二，测地线优化需要在每次训练中迭代求解，计算开销巨大。

### 本文动机

基于上述分析，本文的核心动机可概括为三个层次：

1. **范式转换**：将新视角合成从噪声到数据的随机生成范式，转变为数据到数据的确定性流匹配范式，从根本上消除扩散模型的随机性对视图一致性的损害。

2. **几何约束**：在确定性流匹配的基础上，引入概率密度测地线约束，使插值路径对齐数据流形的高密度区域，确保中间状态在语义和几何上保持合理。

3. **高效实现**：通过教师-学生蒸馏框架，将测地线优化从昂贵的迭代求解解耦为一次性前向预测，使密度测地线流匹配在计算上可行，同时保留其几何优势。



## 核心方法与创新机理

GeodesicNVS 的核心创新在于将新视角合成从“噪声→数据”的随机扩散范式重构为“数据→数据”的确定性流匹配范式，并通过概率密度测地线约束插值路径的几何一致性。这一转变通过三个关键的技术槽位体现：

### 1. 框架类型：从噪声到数据的扩散/流匹配 → 数据到数据的确定性流匹配

传统条件扩散模型（如 **Zero-1-to-3** (Liu et al., 2023)、**Free3D** (Zheng & Vedaldi, CVPR 2024)）学习从高斯噪声到目标视图的随机映射，其随机性导致视图间结构不一致，确定性映射被破坏。GeodesicNVS 提出 **Data-to-Data Flow Matching（D2D-FM）** 框架，直接在配对视图 $(x_0, x_1)$ 之间学习确定性变换，将条件流匹配的速度场目标从去噪方向改为数据对偶方向：

$$u_t(x_t | x_0, x_1) = x_1 - x_0$$

训练速度网络 $v_\theta$ 逼近该真实速度场，损失函数为：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{x_0, x_1, t} \left[\| v_{\theta}(x_t, t, q, c) - (x_1 - x_0) \|^2\right]$$

这一改变的直接证据来自 **Table 1**：Linear-D2D-FM 在 Objaverse 上 FID 达到 5.4324，优于扩散基线 Free3D 的 5.5434（−0.111），同时 PSNR 从 Naive FM 的 20.8246 提升至 20.8447，验证了确定性数据对偶流匹配相比噪声到数据范式的结构保持优势。

### 2. 插值路径：线性插值 → 概率密度测地线插值

线性插值 $x_t = (1-t)x_0 + t x_1$ 仅对端点进行凸组合，在数据流形上可能穿越低密度区域，产生语义不一致的中间视图。GeodesicNVS 引入概率密度测地线插值，通过环境空间校正网络 $\phi_\eta$ 对线性路径进行非线性修正：

$$x_t = (1-t)x_0 + t x_1 + \phi_{\eta}(x_0, x_1, t)$$

其理论基础是概率密度测地线方程——路径长度在黎曼度量 $G(x) = p(x)^{-2} I$ 下最小化，使得插值轨迹沿数据流形的高密度区域行进，而非简单的像素混合。

**Table 3** 提供了关键验证：在缩减训练设置下，PDG-FM 相比 Linear-D2D-FM 将 FID 从 11.8124 降至 10.4010（−1.4114），SSIM 从 0.8736 提升至 0.8768。**Table 4** 进一步表明，测地线插值的平均光流幅度（AOFM）为 13.6968，显著高于线性插值的 11.9875，说明其路径更符合相机旋转的真实几何变换，而非静态混合。

### 3. 几何约束优化：无几何约束 → 教师-学生蒸馏优化密度测地线

直接在高维环境空间优化测地线方程面临密度估计困难。GeodesicNVS 设计了教师-学生蒸馏框架来解决这一问题：

- **教师网络** $\phi_\xi$ 在 DDIM-F 潜空间中进行测地线优化，利用预训练扩散模型提供的密度分数代理 $\nabla \log p(z_t | c_t, \tau)$，通过缩放泛函导数更新路径：

$$g_t = \left( I - \hat{\dot{\gamma}}_t \hat{\dot{\gamma}}_t^{\mathsf{T}} \right) \nabla \log p(z_t | c_t, \tau) + \frac{\ddot{\gamma}_t}{\|\dot{\gamma}_t\|^2}$$

- **学生网络** $\phi_\eta$ 通过蒸馏损失将潜空间测地线映射回环境空间：

$$\ell^{0}(\eta) = \mathbb{E}_t \left[\| x_t - \mathrm{DDIM\text{-}B}(z_t, c_t, \tau) \|^2\right]$$

**Figure 7** 显示，优化后的测地线路径在训练集上具有更低的欧拉-拉格朗日残差，表明其更好地满足测地线方程条件，与感知和几何一致性提升一致。

这三个槽位的协同作用形成了完整的创新链条：确定性流匹配消除随机性破坏，测地线插值保证路径几何一致性，教师-学生蒸馏使密度测地线优化在计算上可行。



GeodesicNVS 提出 **概率密度测地线流匹配（Probability Density Geodesic Flow Matching, PDG-FM）** 框架，将新视角合成重新建模为从源视图到目标视图的确定性连续变换。整个框架由两个核心阶段级联而成：**数据到数据流匹配（Data-to-Data Flow Matching）** 和 **测地线插值蒸馏（Variational Distillation of Geodesics）**，最终统一为端到端的测地线流匹配流程（Figure 2）。

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Probability Density Geodesic Flow Matching (PDG-FM) framework. (a) Data-to-Data Flow Matching framework learns deterministic mappings between paired samples*

### 数据到数据流匹配阶段

该阶段摒弃了传统扩散模型从噪声到数据的随机映射，转而学习成对视图之间的确定性速度场。给定同一场景在两个相机姿态下的潜空间表示 $x_0$（源视图）和 $x_1$（目标视图），框架定义线性插值路径 $x_t = (1-t)x_0 + t x_1$，并通过条件流匹配损失训练速度网络 $v_\theta$ 逼近真实速度场 $u_t(x_t|x_0,x_1) = x_1 - x_0$：

$$
\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{x_0, x_1, t} [\| v_{\theta}(x_t, t, q, c) - (x_1 - x_0) \|^2] \tag{Eq 8}
$$

速度网络 $v_\theta$ 采用与 Zero-1-to-3 类似的 U-Net 骨干，输入包括当前插值状态 $x_t$、时间步 $t$、目标相机射线嵌入（Plücker 坐标）$q$ 以及源视图语义条件 $c$。其中语义条件由 CLIP 编码器 $\varepsilon_{\text{clip}}$ 提取源视图特征，并与 VAE 编码器 $\varepsilon_{\text{img}}$ 编码的源视图潜变量拼接后注入网络。这一基线配置被称为 **Linear-D2D-FM**，其确定性映射特性使视图间结构一致性显著优于扩散基线（Table 1：FID 5.4324 vs Free3D 5.5434）。

### 测地线插值蒸馏阶段

线性插值路径在数据流形上仅做端点混合，未利用数据分布几何结构。PDG-FM 引入 **概率密度测地线** 替代线性插值，使变换路径沿数据流形的高密度区域行进。测地线插值参数化为带环境空间校正网络的形式：

$$
x_t = (1-t)x_0 + t x_1 + \phi_{\eta}(x_0, x_1, t) \tag{Eq 9}
$$

为高效获取密度测地线，框架采用 **教师-学生蒸馏** 策略（Algorithm 1, Figure 2b）：
- **教师网络** $\phi_\xi$ 在扩散模型的 DDIM-F 潜空间中进行测地线优化。DDIM-F 算子通过前向 ODE 将环境空间点映射为平滑潜变量 $z_t$，并利用无分类器引导近似密度分数的梯度 $\nabla \log p(z_t|c_t,\tau)$。教师通过最小化欧拉-拉格朗日残差（Eq 4）来更新测地线路径，使其满足测地线方程。
- **学生网络** $\phi_\eta$ 在环境空间中直接预测测地线校正量，通过最小化其输出与教师潜变量经 DDIM-B 反向重建之间的 MSE 进行蒸馏（Eq 17），从而将测地线优化过程蒸馏到环境空间，避免推理时依赖扩散模型。

### 统一流程

在推理阶段，PDG-FM 将蒸馏后的 GeodesicNet $\phi_\eta$ 与 VelocityNet $v_\theta$ 统一：给定源视图 $x_0$ 和目标相机姿态，GeodesicNet 预测密度感知的测地线插值路径 $x_t$，VelocityNet 沿该路径积分生成目标视图。这一确定性流匹配框架在缩减训练设置下，PDG-FM 相比 Linear-D2D-FM 将 FID 从 11.8124 降至 10.4010（-1.4114），SSIM 从 0.8736 提升至 0.8768（Table 3），验证了测地线插值对几何一致性的增益。

> **注意**：当前分析基于项目博客提供的技术细节，部分实现细节（如教师网络的具体优化步数、蒸馏损失权重）需待正式论文发布后验证。



### 数据到数据流匹配框架

GeodesicNVS 的核心创新在于将新视角合成从传统的“噪声到数据”扩散范式转变为“数据到数据”的确定性流匹配框架。传统扩散模型学习的是随机噪声到目标视图的随机映射，这种随机性破坏了视图间的确定性几何结构。而数据到数据流匹配直接学习源视图到目标视图的连续确定性变换，从根本上保证了映射的一致性。

该框架由两个关键模块构成：

**VelocityNet（速度场预测器 $v_\theta$）**：采用与 Zero-1-to-3 类似的 U-Net 骨干网络，接收当前插值状态 $x_t$、时间步 $t$、目标相机射线（通过 PlückerRayEmbedder 编码为 Plücker 坐标 $q$）以及源视图语义条件 $c$（由 CLIP Encoder $\varepsilon_{\text{clip}}$ 提取）。源视图通过 VAE Encoder $\varepsilon_{\text{img}}$ 编码到潜空间并拼接输入，为网络提供像素级几何先验。

**线性插值基线（Linear-D2D-FM）**：在基础版本中，条件路径定义为带微小噪声平滑的线性插值：
$$x_t = (1-t)x_0 + t x_1 + \sigma_{\min}\varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I)$$
对应的真实速度场为端点差：
$$u_t(x_t | x_0, x_1) = x_1 - x_0$$

训练目标为条件流匹配损失（Conditional Flow Matching Loss）：
$$\mathcal{L}_{\text{CFM}}(\theta) = \mathbb{E}_{x_0, x_1, t} \left[\| v_{\theta}(x_t, t, q, c) - (x_1 - x_0) \|^2\right]$$

该损失直接监督速度网络逼近线性插值的常速度场，无需像扩散模型那样估计噪声或分数函数。

### 概率密度测地线流匹配

线性插值在数据流形上并非最短路径，可能导致中间状态偏离高密度区域，产生语义不一致的视图。GeodesicNVS 引入概率密度测地线来约束插值路径，使其沿数据流形的高密度区域行进。

**密度测地线的变分原理**：在数据流形上定义黎曼度量张量 $G(x) = p(x)^{-2}I$，其中 $p(x)$ 为数据密度。路径长度由 Lagrangian 给出：
$$S[\gamma] = \int_0^1 L(t, \gamma(t), \dot{\gamma}(t)) \mathrm{d}t, \quad L(t, \gamma, \dot{\gamma}) = \|\dot{\gamma}\|_{G(\gamma)}$$
极小化该泛函的路径满足 Euler-Lagrange 测地线方程：
$$\ddot{\gamma} + \|\dot{\gamma}\|^2 \left( I - \hat{\dot{\gamma}}\hat{\dot{\gamma}}^{\mathsf{T}} \right) \nabla \log p(\gamma) = 0$$

该方程揭示：测地线路径的加速度由密度分数的切空间投影驱动，使路径向高密度区域弯曲。

**环境空间测地线参数化**：为避免直接在潜空间求解测地线方程的高昂代价，GeodesicNVS 将测地线插值参数化为带校正网络的线性基：
$$x_t = (1-t)x_0 + t x_1 + \phi_{\eta}(x_0, x_1, t)$$
其中 $\phi_{\eta}$ 为 GeodesicNet（学生网络），在环境空间直接预测对线性路径的密度感知偏移。

### 教师-学生蒸馏框架

密度分数 $\nabla \log p(x)$ 的精确估计是测地线优化的瓶颈。GeodesicNVS 利用预训练扩散模型作为密度分数的代理，并设计教师-学生蒸馏框架将测地线优化与推理解耦。

**教师网络（DDIM-F 空间测地线优化）**：教师网络 $\phi_{\xi}$ 在扩散模型的确定性潜空间（DDIM-F 空间）中工作。DDIM 前向 ODE 定义为：
$$\frac{\mathrm{d}}{\mathrm{d}t} \left( \frac{x_t}{\sqrt{\bar{\alpha}_t}} \right) = \frac{\mathrm{d}}{\mathrm{d}t} \left( \sqrt{\frac{1-\bar{\alpha}_t}{\bar{\alpha}_t}} \right) \zeta(x_t, c, t)$$
该 ODE 将数据点映射为平滑的潜变量，同时提供密度分数估计。通过无分类器引导近似 Stein 分数：
$$\nabla \log p(x_\tau | c, \tau) \approx \beta \omega(\tau) (\zeta(x_\tau, c, \tau) - \zeta(x_\tau, c_{\text{neg}}, \tau))$$

教师网络的更新方向由缩放泛函导数给出：
$$g_t = \left( I - \hat{\dot{\gamma}}_t \hat{\dot{\gamma}}_t^{\mathsf{T}} \right) \nabla \log p(z_t | c_t, \tau) + \frac{\ddot{\gamma}_t}{\|\dot{\gamma}_t\|^2}$$

**学生蒸馏**：学生网络 $\phi_{\eta}$ 通过最小化与教师潜变量的 DDIM-B 重建之间的 MSE 来学习：
$$\ell^{0}(\eta) = \mathbb{E}_t \left[\| x_t - \text{DDIM-B}(z_t, c_t, \tau) \|^2\right]$$

这一蒸馏设计将计算密集的测地线优化限制在训练阶段，推理时仅需学生网络的前向传播，实现了高效且几何一致的新视角合成。

### 补充图表

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/001_Figure_1.jpg]]
*Figure 1: From Conditional Diffusion Model to Probability Density Geodesic Flow Matching. Conventional diffusion models learn stochastic noise-to-data transitions, often losing deterministic structure. We instead train a Data-to-Data Flow Matching network to learn continuous deterministic transformations between paired data samples*

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/009_Figure_6.jpg]]
*Figure 6: Geodesic Interpolants vs Linear Interpolants. Geodesic interpolants traverse semantically meaningful regions of the data manifold, producing perceptually consistent interpolants. In contrast, linear interpolants merely blend the two endpoints, resulting in limited structural continuity and unrealistic transitions*

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/010_Figure_7.jpg]]
*Figure 7: Comparison of Geodesic Gradient Norm across Time for geodesic interpolants, their pre-optimization counterparts, and linear interpolants on training dataset. The optimized geodesic paths have lower residuals thus indicating better satisfaction of the Euler-Lagrange condition, aligning with improved perceptual and geometric consistency*



## 实验与关键发现

### 核心定量结果

Linear-D2D-FM 作为数据到数据流匹配的线性插值基线，在 Objaverse 测试集上取得了 **FID 5.4324**，优于扩散模型基线 Free3D 的 5.5434（-0.111），同时 PSNR 达到 20.8447，略高于 Naive FM 的 20.8246（Table 1，100 NFE）。在 GSO30 数据集上，Linear-D2D-FM 同样展现出竞争力，FID 为 15.0543，验证了确定性流匹配框架在跨数据集泛化上的有效性。

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/003_Table_1.jpg]]
*Table 1: Novel view synthesis performance on Objaverse and GSO datasets. Comparison of Linear-D2D-FM against diffusion and flow baselines on Objaverse and GSO30*

加速推断场景下（10 NFE），Linear-D2D-FM 保持性能优势：FID 5.8223、CLIP-S 88.9749、SSIM 0.8688、LPIPS 0.0782，显著优于 Free3D（FID 8.9367、CLIP-S 84.4197、SSIM 0.7894、LPIPS 0.1493），且与 Naive FM 相当或略优（Table 2）。这表明数据到数据流匹配在低步数推断时仍能维持确定性映射的结构保真度，而扩散模型的随机性在步数受限时导致更严重的退化。

### 测地线对齐效果

在缩减训练设置下，PDG-FM（概率密度测地线流匹配）相比 Linear-D2D-FM 实现了一致性提升：**FID 从 11.8124 降至 10.4010（-1.4114）**，SSIM 从 0.8736 提升至 0.8768（Table 3）。同时，PDG-FM 的 CLIP 相似度达到 92.3368，LPIPS 为 0.0804，均优于 Metric FM（Kapusniak et al., 2024）的 11.9609 / 92.0370 / 0.0900，证明密度感知测地线插值比学习黎曼度量的方法更有效地捕捉了数据流形的几何结构。

定性对比（Figure 5）进一步印证：PDG-FM 生成的视图在几何保真度上优于 Linear-D2D-FM，测地线路径使插值轨迹穿越数据流形的高密度语义区域，而非简单的端点混合。

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparisons between PDG-FM (geodesic) and Linear-D2D-FM (linear) on Objaverse. Visual results showing that PDG-FM generates more geometrically faithful novel views. The improvement reflects the effect of energy-guided optimization along data-dependent geodesics*

### 测地线路径研究

Table 4 的路径研究表明，测地线插值的**平均光流幅度（AOFM）为 13.6968**，显著高于线性插值的 11.9875，且更接近真实相机轨迹的参考值。这表明测地线路径更好地遵循了相机旋转引起的像素运动，而非产生静态混合。同时，测地线插值的路径感知长度（PPL）也优于 DDIM 初始化的变体。

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/011_Table_4.jpg]]
*Table 4: Geodesic Path Study Results. We report PPL and AOFM for linear, DDIM-initialized, and geodesic interpolants, with ground-truth camera trajectories as the reference*

Figure 7 从优化角度提供了机制性证据：优化后的测地线路径在训练集上具有更低的欧拉-拉格朗日残差，满足密度测地线方程 $$\ddot{\gamma} + \|\dot{\gamma}\|^2 (I - \hat{\dot{\gamma}}\hat{\dot{\gamma}}^{\mathsf{T}}) \nabla \log p(\gamma) = 0$$ 的条件，与感知和几何一致性提升的观察一致。

### 消融研究

Table 5 揭示了两个关键设计选择：

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/013_Table_5.jpg]]
*Table 5: Ablation study of noise augmentation (top) and timestep sampling (bottom) in Linear-D2D-FM*

- **噪声增强**：中等噪声水平（eps=400）在所有指标上优于低噪声变体（eps=50），FID 5.4324 vs 5.8050。过低噪声导致过拟合，适度噪声增强有助于保留语义一致性。
- **时间步采样**：离散时间步采样 $U_{10}$ 在 10 NFE 评估下实现最佳平衡（FID 5.5146），优于连续均匀采样。这表明在有限推断步数下，精心选择的时间离散化对性能有显著影响。

### 失败模式与局限

当前方法存在三个主要局限，需在解读结果时注意：

1. **密度估计依赖**：测地线优化依赖预训练扩散模型作为密度分数的代理，其估计质量直接影响测地线路径的准确性。在数据分布与预训练模型训练域偏离较大时，密度分数可能不可靠。
2. **计算开销**：测地线蒸馏和文本反演增加了训练计算成本，Table 3 的缩减训练设置即反映了完整训练的高昂代价。
3. **场景泛化**：当前实验使用对象类别的简单提示（如“an object of category”），对复杂场景的泛化能力尚未在现有结果中得到验证，需谨慎外推。

### 补充图表

![[assets/figures/papers/paper_list_l2505_https_arxiv_org_abs_2603_01010/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparisons on Objaverse. Comparison of Linear-D2D-FM, the Noise-to-Data FM (Naive FM) baseline and the diffusion-based Free3D model*



## 定位与知识库关联

### 核心基线与差异化定位

**扩散模型基线**。新视角合成（NVS）领域的主流范式是条件扩散模型：**Zero-1-to-3**（Liu et al., 2023）及其扩展版本 **Zero-1-to-3-XL** 通过文本到图像的零样本迁移实现视角变换；**EscherNet**（Xin et al., 2024）引入多视图一致性约束；**Free3D**（Zheng & Vedaldi, CVPR 2024）则在不依赖显式 3D 表示的前提下追求一致性生成。这些方法的共同瓶颈在于：扩散过程的随机性破坏了视图间的确定性结构映射，导致几何不一致（verified_analysis 中 bottleneck 确认）。

**流匹配基线**。本文的直接对比对象包括 **Naive FM**——采用相同 U-Net 架构但执行噪声到数据的条件流匹配，以及 **Metric FM**（Kapusniak et al., 2024）——学习黎曼度量的流匹配方法。Linear-D2D-FM 在 Objaverse 上 FID 达到 5.4324，优于 Free3D 的 5.5434（−0.111），同时 PSNR 20.8447 超过 Naive FM 的 20.8246（Table 1），证明数据到数据的确定性映射在视图一致性上具有结构性优势。

### 方法谱系中的位置

PDG-FM 的方法论贡献体现在三个递进的“改变槽位”（changed_slots）：

1. **框架类型**：从噪声到数据的随机映射转向数据到数据的确定性流匹配。这一转变消除了扩散模型中的随机噪声注入，使速度场 $v_\theta$ 直接学习配对视图间的连续变换，保留了几何结构的确定性。

2. **插值路径**：从线性插值 $x_t = (1-t)x_0 + t x_1$ 升级为概率密度测地线插值 $x_t = (1-t)x_0 + t x_1 + \phi_\eta(x_0, x_1, t)$。这一改变的核心洞察在于：数据流形上的最短路径应沿高密度区域行进，而非在环境空间中进行简单的线性混合。Table 3 显示，在缩减训练设置下，PDG-FM 的 FID 从 Linear-D2D-FM 的 11.8124 降至 10.4010（−1.4114），SSIM 从 0.8736 提升至 0.8768，验证了测地线插值的有效性。

3. **几何约束优化**：引入教师-学生蒸馏框架。教师在 DDIM-F 空间中通过最小化欧拉-拉格朗日残差（Eq. 4）优化测地线路径，学生网络 $\phi_\eta$ 通过蒸馏损失 $\ell^0(\eta) = \mathbb{E}_t [\| x_t - \text{DDIM-B}(z_t, c_t, \tau) \|^2]$ 将测地线映射回环境空间。Figure 7 的梯度范数分析证实，优化后的测地线路径具有更低的欧拉-拉格朗日残差，满足测地线方程条件。

### 适用边界与局限

**依赖预训练扩散模型**。密度分数的估计依赖于预训练的 DDIM 模型，通过无分类器引导近似 Stein 分数 $\nabla \log p(x_\tau | c, \tau) \approx \beta \omega(\tau) (\zeta(x_\tau, c, \tau) - \zeta(x_\tau, c_{\text{neg}}, \tau))$（Eq. 12）。这一代理估计的质量直接影响测地线优化的精度，在低密度区域可能产生不可靠的梯度方向。

**计算开销**。测地线蒸馏过程需要联合训练教师网络 $\phi_\xi$ 和学生网络 $\phi_\eta$，并通过文本反演获取条件嵌入，增加了训练阶段的算力需求。Table 3 的实验在缩减训练设置下进行，暗示全量训练的计算成本可能更高。

**场景泛化**。当前实验采用对象类别的简单提示（如“an object of category”），对复杂多物体场景或真实世界环境的新视角合成能力尚未验证。Table 4 中测地线插值的平均光流幅度（AOFM）为 13.6968，高于线性插值的 11.9875，表明路径更符合相机旋转，但这一优势是否在复杂场景中保持需要进一步检验。

### 开放问题

1. **大规模扩展**：密度测地线估计依赖 DDIM 空间中的迭代优化，如何将其高效扩展到更大规模数据集（如完整 Objaverse 或真实场景数据）是一个工程与算法挑战。

2. **极低推理步数**：Table 2 显示 Linear-D2D-FM 在 10 NFE 下保持 FID 5.8223 的竞争力，但 PDG-FM 的测地线路径是否能在极低步数下保持几何优势尚未验证。测地线插值本身需要更精细的路径采样，可能在少步推断中丧失优势。

3. **去扩散依赖**：能否设计不依赖预训练扩散模型的密度估计方法？例如直接学习数据流形的密度函数或采用能量基模型，以降低对外部模型的依赖并提升可扩展性。

4. **多视图与 3D 重建**：当前方法聚焦于两视图间的变换，如何将测地线一致性扩展到多视图一致生成和显式 3D 重建（如 NeRF 或 3D Gaussian Splatting 的初始化）是一个自然延伸方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/GeodesicNVS_Probability_Density_Geodesic_Flow_Matching_for_Novel_View_Synthesis.pdf]]

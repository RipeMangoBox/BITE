---
title: "ChordEdit: One-Step Low-Energy Transport for Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ChordEdit_One_Step_Low_Energy_Transport_for_Image_Editing.pdf
project_link: "https://chordedit.github.io"
code_link: null
aliases:
- ChordEdit
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间平滑窗口δ（通过动态最优输运推导出的低能量和弦控制场的时间平均宽度）
primary_logic: 将一步图像编辑视为源与目标分布间的动态最优输运问题，并通过因果核平滑（时间加权平均）从可观测的模型输出中构造低能量、稳定的控制场，使得单步大步长积分可实现高保真编辑。
claims:
- 朴素编辑场具有高能量且不稳定，导致单步编辑失败
- 和弦控制场是L²收缩算子，抑制能量尖峰
- 和弦控制场在PIE-bench上实现背景一致性和语义对齐的显著提升
- 用户研究确认ChordEdit在语义对齐和背景保真度上均显著优于对比方法
---

# ChordEdit: One-Step Low-Energy Transport for Image Editing

> [!tip] 核心洞察
> 将一步图像编辑视为源与目标分布间的动态最优输运问题，并通过因果核平滑（时间加权平均）从可观测的模型输出中构造低能量、稳定的控制场，使得单步大步长积分可实现高保真编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | ChordEdit：面向图像编辑的一步低能传输 |
| 英文题名 | ChordEdit: One-Step Low-Energy Transport for Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19083) · [Project](https://chordedit.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ChordEdit |
| Dataset | PIE-bench |

> [!tip] 效果简介
> - PIE-bench 上，PSNR↑ 22.20 (ChordEdit SD-Turbo, with prox) vs 21.38 (Naive δ=0 SD-Turbo, with prox) (+0.82)；CLIP-Edited↑ 22.96 (ChordEdit SD-Turbo, with prox) vs 21.96 (Naive δ=0 SD-Turbo, with prox) (+1.00)；Runtime (s)↓ 0.38 (ChordEdit SD-Turbo) vs 7.22 (FlowEdit, 33 steps) (19x faster)。

## 概述

**问题瓶颈**：在一步文本到图像（T2I）模型中进行文本引导编辑时，朴素的漂移差值（drift difference）所诱导的高能量、非平滑矢量场会导致严重的物体扭曲和背景崩坏，使得训练无关、逆无关的单步编辑不可行。

**核心洞察**：ChordEdit 将一步图像编辑重新定义为源分布与目标分布之间的动态最优输运问题，并通过因果核平滑（时间加权平均）从可观测的模型输出中构造低能量、稳定的“和弦控制场”（Chord Control Field），使得单步大步长积分即可实现高保真编辑。

**方法定位**：ChordEdit 是一种**模型无关、训练无关、逆无关**的单步编辑方法，直接作用于快速生成模型（如 SD-Turbo、SwiftBrush-v2），无需额外训练专用网络或执行反演步骤。与需要 33 步推理的 **FlowEdit**、需要训练专用网络的 **SwiftEdit**、需要 4 步推理的 **InfEdit** 以及需要反演的多步方法形成鲜明对比。

**主要结果**：
- **效率**：ChordEdit 在 PIE-bench 上仅需 0.38 秒完成编辑，比 FlowEdit（7.22 秒，33 步）快约 19 倍，比 Direct Inversion（79.10 秒）快超过 208 倍。
- **背景保真度**：在不使用近端细化的情况下，ChordEdit 在 NFE=1 时达到 PSNR 23.89，显著优于朴素基线（PSNR 21.89，+2.00）。
- **语义对齐**：使用近端细化后，CLIP-Edited 达到 22.96，较朴素基线提升 1.00。
- **用户偏好**：在四选一盲评用户研究中，ChordEdit 在语义对齐（42.5%）和背景保存（48.3%）上均显著领先于对比方法。

**关键机制**：和弦控制场通过时间平滑窗口 δ 对可观测代理场进行加权平均（公式 $ \hat{u}_t(x_{\tau}) = \frac{t \mathbf{R}(x_{\tau}, t-\delta) + \delta \mathbf{R}(x_{\tau}, t)}{t+\delta} $），构成 $L^2$ 收缩算子，有效抑制能量尖峰，使单步传输稳定可靠。

## 背景与动机

### 一步生成模型的编辑困境

文本引导的图像编辑（text-guided image editing）旨在根据目标文本提示修改输入图像的语义，同时保持非编辑区域的视觉一致性。近年来，蒸馏式一步文本到图像（T2I）生成模型（如 SD-Turbo、SwiftBrush-v2）将推理成本压缩至单次前向传递，使实时图像生成成为可能。然而，在这些一步模型上实现高质量编辑面临根本性挑战：**朴素的漂移差值（drift difference）所诱导的编辑矢量场具有高能量和非平滑特性，导致单步大步长积分时出现严重的物体扭曲和背景崩坏**（Figure 3）。

具体而言，在多步扩散模型中，编辑通常通过迭代应用源-目标漂移差 $\Delta v(x_t, t) = v(x_t, t, c_{\text{tar}}) - v(x_t, t, c_{\text{src}})$ 来实现，小步长积分保证了轨迹的稳定性（Figure 4a）。但当这一策略直接迁移到一步模型时，该朴素的编辑场变得高能且易变，单次大步长积分会累积显著误差，产生两类不可接受的失败模式：（i）编辑物体严重扭曲；（ii）背景崩解并出现伪结构（Figure 4b）。

### 现有方法的缺口

当前编辑方法在效率与质量之间存在显著张力：

- **多步方法**（如 **FlowEdit**，33步；**Direct Inversion + PnP**，50步）虽然编辑质量较高，但依赖反演或多步推理，运行时长达数秒至数十秒，无法满足实时编辑需求。
- **少步方法**（如 **InfEdit**，4步）部分缓解了效率问题，但仍需多次函数评估，且通常需要反演步骤。
- **一步方法**（如 **SwiftEdit**）虽实现了单步推理，但需要训练专用编辑网络，丧失了训练无关（training-free）的灵活性，且与特定模型绑定。

核心瓶颈在于：**在一步 T2I 模型中进行训练无关、逆无关（inversion-free）的单步编辑时，如何构造一个低能量、稳定的控制场，使得单次大步长传输即可实现高保真编辑？** 现有方法要么牺牲效率换取稳定性（多步），要么牺牲通用性换取速度（训练专用），缺乏一种既无需训练/反演、又能以单步推理实现高质量编辑的统一方案。

### 本文动机：从最优输运视角重构编辑

ChordEdit 将图像编辑重新定义为**源分布与目标分布之间的动态最优输运问题**。给定源提示 $c_{\text{src}}$ 和目标提示 $c_{\text{tar}}$，编辑的目标是将图像从条件分布 $p(x \mid c_{\text{src}})$ 传输到 $p(x \mid c_{\text{tar}})$。根据 Benamou–Brenier 动态最优输运理论，最优传输路径应最小化动能泛函：

$$\min_{\rho,u} \int_0^1 \int \frac{1}{2} \|u_t(x)\|^2 \rho_t(x) dx dt \quad \mathrm{s.t.} \quad \partial_t \rho_t(x) + \nabla_x \cdot (\rho_t(x) u_t(x)) = 0$$

这一视角揭示了朴素漂移差方法的本质缺陷：其高能量场违背了最优输运的最小动能原则，导致传输路径偏离最优轨迹，在粗离散化（单步）下表现灾难性（Figure 5 的 2D 玩具示例直观展示了这一现象）。

ChordEdit 的核心动机在于：**通过因果核平滑（时间加权平均）从可观测的模型输出中构造低能量、稳定的和弦控制场（Chord Control Field），使得单步大步长积分可实现高保真编辑，同时保持训练无关和逆无关的灵活性**。这一设计使得 ChordEdit 在 PIE-bench 上以 0.38 秒的单步推理实现了与多步方法竞争甚至更优的背景一致性（PSNR）和语义对齐（CLIP-Edited），速度比 FlowEdit 快 19 倍，比 Direct Inversion 快 208 倍（Table 1）。

## 核心创新

ChordEdit 的核心创新在于**将一步图像编辑重新定义为源分布与目标分布之间的动态最优输运问题**，并由此推导出**低能量和弦控制场（Chord Control Field）**，从根本上解决了朴素漂移差值在单步大步长积分下因高能量、非平滑矢量场导致的物体扭曲与背景崩坏问题。

### 瓶颈发现：朴素编辑场的高能失稳

在一步 T2I 模型中进行文本引导编辑时，最直接的做法是计算朴素漂移差值（Simple Drift Difference）：

$$ \Delta v(x_t, t) = v(x_t, t, c_{\mathrm{tar}}) - v(x_t, t, c_{\mathrm{src}}) $$

然而，该场具有高能量且不稳定的特性（Figure 3）。在多步扩散模型中，迭代应用该漂移可确保稳定轨迹；但在蒸馏得到的一步模型中，单次大步长积分会累积显著误差，导致两类致命失败：（i）严重的物体扭曲；（ii）背景崩坏与伪影生成（Figure 4）。这一瓶颈使得训练无关、逆无关的单步编辑长期不可行。

### 核心机制：基于动态最优输运的和弦控制场

ChordEdit 的核心洞察是：编辑过程可被建模为 Benamou–Brenier 动态最优输运问题，其目标是最小化传输过程中的动能：

$$ \min_{\rho,u} \int_0^1 \int \frac{1}{2} \|u_t(x)\|^2 \rho_t(x) dx dt \quad \mathrm{s.t.} \quad \partial_t \rho_t(x) + \nabla_x \cdot (\rho_t(x) u_t(x)) = 0 $$

基于此理论框架，ChordEdit 从可观测代理场 $\mathbf{R}(x_{\tau}, t)$ 出发，通过因果核平滑（时间加权平均）构造出低能量、稳定的控制场：

$$ \hat{u}_t(x_{\tau}) = \frac{t \mathbf{R}(x_{\tau}, t-\delta) + \delta \mathbf{R}(x_{\tau}, t)}{t+\delta} $$

其中 $\delta$ 为时间平滑窗口。该公式等价于对朴素场做因果单边核平滑 $\hat{u} = K_{\delta} * \mathbf{R}$。由 Jensen 不等式可证，该和弦场是 $L^2$ 收缩算子，满足 $\int \|\hat{u}\|^2 \leq \int \|\mathbf{R}\|^2$，有效抑制了能量尖峰（Section 4.2）。

### 关键 changed slots 与创新对比

| 创新维度 | 基线方法 | ChordEdit 方案 | 创新性质 |
|----------|----------|----------------|----------|
| **编辑场构造** | 朴素漂移差值 $\Delta v$（高能、非平滑） | 和弦控制场 $\hat{u}_t$（时间平滑、$L^2$ 收缩） | 理论驱动的方法创新 |
| **推理步数** | 多步推理（FlowEdit 33步、Direct Inversion 50步） | 单步传输（NFE=1） | 效率的阶跃提升 |
| **近端细化** | 无 | 可选的单步前向传递 $\mathrm{prox}(x^{\mathrm{pred}}, t_c, c_{\mathrm{tar}})$ | 解耦一致性与语义的模块化设计 |

### 解耦设计：一致性与语义的模块化分工

ChordEdit 的另一个关键创新在于**将背景一致性与语义对齐解耦为两个独立模块**。和弦控制场优先保证背景一致性——在 PIE-bench 上，仅使用和弦场（w/o prox）即可将 PSNR 从朴素基线的 21.89 提升至 23.89（Table 2）。而可选的近端细化步骤 $\mathrm{prox}(x^{\mathrm{pred}}, t_c, c_{\mathrm{tar}})$ 通过目标提示的单步前向传递增强目标语义，将 CLIP-Edited 从 21.87 提升至 22.96。这种模块化设计使用户可根据需求灵活选择是否启用细化，且两个模块的贡献互不干扰（Table 2 消融实验）。

### 理论保证与实证验证

和弦控制场的稳定性在 2D 玩具实验中得到直观验证：朴素残差场在粗离散化下高能且不稳定，而 ChordEdit 的低能量场驱动粒子以最小偏差直达目标分布（Figure 5）。在真实图像编辑中，能量可视化（Figure 8）和稳定性分析（Figure 9）均证实：随着积分步数 $S \to 1$，朴素场的能量急剧飙升，导致 PSNR 崩溃；而和弦场能量保持低位，PSNR 维持高水平。用户研究进一步确认，ChordEdit 在语义对齐（42.5% 偏好）和背景保真度（48.3% 偏好）上均显著优于对比方法（Figure 21）。

## 整体框架

ChordEdit 将文本引导的图像编辑重新定义为源提示分布与目标提示分布之间的动态最优输运问题，并以此为基础构建了一个训练无关、反演无关的单步编辑流水线。其核心设计理念是：通过因果核平滑从可观测的模型输出中构造低能量、稳定的控制场，使得单次大步长积分即可实现高保真编辑，从而避免朴素漂移差值场的高能量尖峰所导致的物体扭曲与背景崩坏。

### 流水线模块与数据流

ChordEdit 的完整流水线由四个串行且解耦的模块组成，数据流从输入图像和提示对出发，依次经过可观测残差计算、和弦控制场估计、单步传输和可选的近端细化，最终输出编辑后的图像。

**模块一：可观测残差计算**

给定输入图像 $x_{\text{in}}$、源提示 $c_{\text{src}}$ 和目标提示 $c_{\text{tar}}$，首先将图像编码至 VAE 潜空间得到 $z_0$。随后，利用预训练的一步文生图模型（如 SD-Turbo、SwiftBrush-v2）计算在锚点 $x_\tau$ 处的可观测代理编辑场 $\mathbf{R}(x_{\tau}, t)$。该场通过蒙特卡洛采样从条件概率流 ODE 的漂移差值中估计期望得到：

$$\mathbf{R}(x_{\tau}, t) = \mathbb{E}_{z \sim K_t(\cdot | x_{\tau})} [B_t \Delta Q(z, t)]$$

其中 $\Delta Q(z, t)$ 表示目标提示与源提示在潜变量 $z$ 处的模型输出差异，$B_t$ 为将潜空间差异映射回图像空间的变换矩阵，$K_t$ 为从锚点 $x_\tau$ 出发的前向扩散核。这一模块的输出是一组在不同时间点 $t$ 上的代理场快照，为后续的时间平滑提供原始测量信号。

**模块二：和弦控制场估计**

这是 ChordEdit 的核心创新模块。直接从代理场 $\mathbf{R}$ 构造的朴素漂移差值场具有高能量和非平滑特性，在单步大步长积分下会累积显著误差。ChordEdit 通过动态最优输运理论推导出一个因果核平滑策略，将代理场在时间窗口 $\delta$ 内进行加权平均，得到低能量的和弦控制场 $\hat{u}_t$：

$$\hat{u}_t(x_{\tau}) = \frac{t \mathbf{R}(x_{\tau}, t-\delta) + \delta \mathbf{R}(x_{\tau}, t)}{t+\delta}$$

该公式在数学上对应一个严格凸二次代理目标 $\Phi_t(u; x_\tau)$ 的唯一极小解，平衡了递归能量先验与当前测量信号的一致性。由 Jensen 不等式可证，和弦控制场是 $L^2$ 收缩算子（$\int \|\hat{u}\|^2 \leq \int \|\mathbf{R}\|^2$），有效抑制了高能量尖峰。当 $\delta=0$ 时，和弦场退化为朴素场；当 $\delta>0$ 时，时间平滑窗口将高能波动“熨平”，使场在粗离散化下仍保持稳定。所有中间变量可在一个批次内并行计算，因此该模块的额外计算开销极小。

**模块三：单步传输**

获得和弦控制场后，ChordEdit 采用显式欧拉积分一步更新图像：

$$x_{\text{pred}} = x_{\text{in}} + \lambda \cdot \hat{u}$$

其中 $\lambda$ 为传输步长。这是整个流水线中唯一的图像更新步骤，对应 NFE（函数评估次数）仅为 1。与需要 33 步的 FlowEdit 或需要反演的多步方法相比，ChordEdit 在推理效率上实现了数量级提升（约 19 倍于 FlowEdit，208 倍于 Direct Inversion + PnP）。

**模块四：近端细化（可选）**

单步传输优先保证背景一致性（高 PSNR），但语义对齐（CLIP-Edited）可能尚有提升空间。为此，ChordEdit 引入一个可选的近端细化步骤，通过目标提示的单步前向传递增强目标语义：

$$\text{prox}(x^{\text{pred}}, t_c, c_{\text{tar}}) = \mathcal{B}_{t_c} Q(x^{\text{pred}}, t_c, c_{\text{tar}})$$

该步骤在潜空间中对预测图像施加一次模型前向传递，利用目标提示的条件信息微调编辑区域的语义表达，同时保持背景结构不变。消融实验表明，和弦场与近端细化在功能上解耦：前者驱动背景一致性（PSNR 从 21.89 提升至 23.89），后者提升语义对齐（CLIP-Edited 从 21.87 提升至 22.96），两者叠加可实现 Pareto 最优的感知-语义权衡。

### 关键超参数与数据流总结

ChordEdit 的完整数据流可概括为：输入图像 $x_{\text{in}}$ → VAE 编码 → 潜空间锚点 $x_\tau$ → 多时间点代理场 $\mathbf{R}$ 计算 → 和弦控制场 $\hat{u}$ 估计（$\delta$ 控制平滑窗口） → 单步传输（$\lambda$ 控制步长） → 可选近端细化（$t_c$ 控制细化强度） → VAE 解码 → 输出图像。整个流水线在单噪声样本（$n=1$）设置下即可实现稳定编辑，对随机种子表现出极低的敏感性（CLIP 变异系数 0.20%，PSNR 变异系数 0.07%）。

### 补充图表

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of editing field stability. (a) Multi-step Simple Drift: In conventional multi-step diffusion, the iterative application of the simple drift*

## 核心模块与公式推导

### 3.1 问题形式化：条件概率流与编辑残差

ChordEdit 将文本引导的图像编辑建模为**源分布与目标分布之间的动态传输问题**。预训练的文本到图像（T2I）模型隐式地诱导了一个条件概率流常微分方程（ODE）：

$$\frac{dx_t}{dt} = v(x_t, t, c) \tag{3.1}$$

其中 $v$ 是条件速度场，$c$ 为文本条件（源提示 $c_{\text{src}}$ 或目标提示 $c_{\text{tar}}$）。在理想情况下，编辑可通过施加一个连续的**瞬时残差场**来实现，该残差场对齐两个条件动力学：

$$\Delta v(x_t, t) = v(x_t, t, c_{\text{tar}}) - v(x_t, t, c_{\text{src}}) \tag{3.1 后续}$$

然而，在蒸馏得到的一步模型中，直接使用该朴素漂移差值（$\delta = 0$）会导致**高能量、非平滑的矢量场**，进而在单步大步长积分时产生严重的物体扭曲和背景崩坏（Figure 3）。

### 3.2 可观测代理场：从隐变量到像素空间的映射

由于真实残差场 $\Delta v$ 在一步模型中不可直接获取，ChordEdit 转而构造一个**可观测的代理编辑场**。给定锚点 $x_\tau$，利用扩散模型的前向加噪核 $K_t(\cdot | x_\tau)$ 将图像映射到隐变量空间，计算模型输出残差 $\Delta Q(z, t)$ 并通过映射 $B_t$ 投影回像素空间，取期望：

$$\mathbf{R}(x_{\tau}, t) = \mathbb{E}_{z \sim K_t(\cdot | x_{\tau})} [B_t \Delta Q(z, t)] \tag{3.3}$$

该代理场 $\mathbf{R}$ 是 ChordEdit 后续构建低能量控制场的**唯一可观测信号源**。

### 4.1 动态最优输运视角

ChordEdit 的核心洞察来自 **Benamou–Brenier 动态最优输运理论**。将编辑视为在时间 $[0,1]$ 内将源分布传输到目标分布，最优传输方案应最小化总动能：

$$\min_{\rho,u} \int_0^1 \int \frac{1}{2} \|u_t(x)\|^2 \rho_t(x) dx dt \quad \mathrm{s.t.} \quad \partial_t \rho_t(x) + \nabla_x \cdot (\rho_t(x) u_t(x)) = 0 \tag{4.1}$$

其中 $\rho_t$ 是概率密度，$u_t$ 是速度场。该公式直接揭示了**低能量场是实现稳定传输的关键**——能量越低，离散化误差越小，单步大步长积分越可靠。

### 4.2 和弦控制场：因果核平滑与能量收缩

基于上述理论，ChordEdit 通过最小化一个严格凸的二次代理目标来估计局部常值控制场 $u$：

$$\Phi_t(u; x_{\tau}) = t \|u - \hat{u}_{t-\delta}(x_{\tau})\|^2 + \int_{t-\delta}^{t} \|u - \mathbf{R}(x_{\tau}, \xi)\|^2 d\xi \tag{4.2 目标函数}$$

该目标函数包含两项：第一项是**递归能量先验**，惩罚当前估计与上一步和弦场的偏离；第二项是**数据保真项**，要求估计与时间窗口 $[t-\delta, t]$ 内的代理场测量一致。其唯一闭式解为：

$$u_t^{\star}(x_{\tau}) = \frac{t}{t+\delta} \hat{u}_{t-\delta}(x_{\tau}) + \frac{1}{t+\delta} \int_{t-\delta}^{t} \mathbf{R}(x_{\tau}, \xi) d\xi \tag{4.2 闭式解}$$

在实际实现中，该递归结构等价于一个**因果单边核平滑**，最终简化为简洁的**和弦控制场**公式：

$$\hat{u}_t(x_{\tau}) = \frac{t \mathbf{R}(x_{\tau}, t-\delta) + \delta \mathbf{R}(x_{\tau}, t)}{t+\delta} \tag{4.5}$$

其中 $\delta$ 是**时间平滑窗口**，为 ChordEdit 的核心因果旋钮。该公式具有两个关键性质：

- **低能量性**：由 Jensen 不等式，和弦场是 $L^2$ 收缩算子，$\int \|\hat{u}\|^2 \leq \int \|\mathbf{R}\|^2$，有效抑制了朴素场中的能量尖峰。
- **稳定性**：平滑窗口 $\delta > 0$ 使得控制场在时间上连续变化，避免了 $\delta = 0$ 时场的高波动性（Figure 4c, Figure 5）。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/005_Figure_5.jpg]]
*Figure 5: 2D Toy Example of Distribution transport. Naive residual fields are high-energy and unstable under coarse discretization. ChordEdit computes a low-energy field (Eq. (4.5)) that drives particles straight to the target with minimal deviation, facilitating reliable one-step transport*

### 4.3 近端细化：语义增强的可选步骤

和弦控制场优先保证背景一致性（高 PSNR），但可能对目标语义的驱动力不足。为此 ChordEdit 引入一个可选的**近端细化步骤**，通过目标提示的单步前向传递增强编辑语义：

$$\mathrm{prox}(x^{\mathrm{pred}}, t_c, c_{\mathrm{tar}}) = \mathcal{B}_{t_c} Q(x^{\mathrm{pred}}, t_c, c_{\mathrm{tar}}) \tag{4.7}$$

该步骤在传输完成后执行，仅需 1 次额外的函数评估（NFE），将 CLIP-Edited 分数从 21.87 提升至 22.96（Table 2），而几乎不影响背景一致性。

### 4.4 单步传输算法

完整算法（Algorithm 1）在 VAE 潜空间中执行，仅需 **1 NFE** 完成传输（加 1 NFE 可选细化）：

1. **可观测残差计算**：在锚点 $x_{\text{in}}$ 处，对时间 $t$ 和 $t-\delta$ 分别采样噪声 $z$，计算代理场 $\mathbf{R}(x_{\text{in}}, t)$ 和 $\mathbf{R}(x_{\text{in}}, t-\delta)$。
2. **和弦控制场估计**：通过公式 (4.5) 计算低能量场 $\hat{u}_t$。
3. **单步传输**：利用显式欧拉积分一步更新图像 $x_{\text{pred}} = x_{\text{in}} + \lambda \cdot \hat{u}_t$。
4. **近端细化（可选）**：通过公式 (4.7) 增强目标语义。

所有中间变量可在一个批次内并行计算，使得传输步骤严格保持 1-NFE。

## 实验与分析

### 核心性能对比

ChordEdit 在一步推理（NFE=1）的条件下，在 PIE-bench 上实现了与多步方法相当甚至更优的背景一致性和语义对齐，同时将推理速度提升了一个数量级以上。Table 1 汇总了 ChordEdit 与多步、少步及一步方法的定量对比。以 SD-Turbo 为骨干模型，ChordEdit 的单步传输仅需 **0.38 秒**，比 FlowEdit（33 步，7.22 秒）快 **19 倍**，比 Direct Inversion + PnP（79.10 秒）快 **208 倍**。在不使用近端细化（w/o prox）的纯单步设定下，ChordEdit 的 PSNR 达到 **23.89**，显著高于朴素基线（δ=0）的 21.89（+2.00），CLIP-Edited 得分也从 20.83 提升至 21.87（+1.04）。加入可选的近端细化后，PSNR 为 22.20，CLIP-Edited 进一步提升至 22.96，在语义对齐维度上超越了所有对比的训练无关/逆无关方法。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison on PIE-bench [11]. T-free: Training-free. I-free: Inversion-free. The best/second/third results in each numeric column are highlighted with yellow / orange / blue backgrounds, respectively. A comprehensive table with extended metrics (e.g., SSIM, Structure Distance) is available in Appendix*

Figure 2 以散点图形式展示了 ChordEdit 在 PSNR、CLIP-Edited 和 Runtime 三个维度上的综合优势：ChordEdit 位于 Pareto 前沿的左上角区域，表明其在保持高背景一致性的同时实现了最快的推理速度。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/002_Figure_2.jpg]]
*Figure 2: Comparing ChordEdit (SD-Turbo) against one-step, few-step, and multi-step editing methods on PIE-bench [11], evaluating performance on background consistency (PSNR), semantic alignment (CLIP, referring to CLIP-Edited) [27], and Runtime. Our method facilitates real-time text-guided editing while yielding highly competitive results*

### 消融研究：和弦控制场与近端细化的解耦贡献

Table 2 的系统消融揭示了框架中两个核心组件的功能分工：

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/012_Table_2.jpg]]
*Table 2: Ablation of Chord transport field and refinement. Our Chord field drives consistency (PSNR), while the prox step boosts semantics (CLIP-Edited). Full metrics are in the Appendix*

- **和弦控制场（Chord Control Field）** 是背景一致性的主要驱动力。仅使用和弦场（w/o prox）时，PSNR 达到 23.89，相比朴素基线（δ=0, w/o prox）的 21.89 提升 2.00。这表明时间平滑窗口 δ 所构造的低能量矢量场有效抑制了背景崩坏和伪影。
- **近端细化（Proximal Refinement）** 专门增强目标语义。在和弦场基础上加入近端步骤后，CLIP-Edited 从 21.87 跃升至 22.96（+1.09），而 PSNR 仅从 23.89 小幅下降至 22.20，验证了两者的解耦关系——和弦场保守地保护非编辑区域，近端步骤激进地注入目标语义。

### 时间平滑窗口 δ 的关键作用

Figure 9（上）展示了编辑场的能量和 PSNR 随积分步数 S 的变化曲线。朴素场（δ=0）的能量在 S→1 时急剧飙升，导致 PSNR 崩溃；而 ChordEdit（δ=0.15）的能量始终保持在低水平，PSNR 在大步长下依然稳定。Figure 8 的可视化对比进一步印证了这一结论：朴素方法的高能量场导致物体扭曲和背景破裂，而 ChordEdit 的低能量场产出了结构完整、背景保真的编辑结果。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative Comparison and Energy Visualization. We compare ChordEdit (Ours) against the naive baseline (δ = 0, Naive). The naive method’s high-energy field leads to artifacts and background corruption. Our ChordEdit derives a stable, low-energy field, resulting in high-fidelity edits that preserve object identity and non-edited regions. Results shown used SwiftBrush-v2 (first column) and SD-Turbo (second and third columns). Energy plots are computed as*

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/010_Figure_9.jpg]]
*Figure 9: (top) ChordEdit Stability as a function of Integration Steps. We compare ChordEdit*

Figure 9（下）的感知-语义 Pareto 前沿分析表明，ChordEdit（δ≠0，红色曲线）在所有感知失真水平上严格 Pareto 支配朴素基线（δ=0，蓝色曲线），即在相同的 LPIPS 失真下始终获得更高的 CLIP-Edited 语义对齐分数。

### 噪声样本数与种子鲁棒性

Figure 11 显示，增加蒙特卡洛噪声样本数 n 对 ChordEdit 的边际收益几乎为零。n=1 到 n=4 的 LPIPS-CLIP Pareto 前沿几乎完全重叠，且均显著优于朴素基线。在 20 个随机种子上的单噪声（n=1）分布直方图表明，CLIP-Edited 的变异系数仅为 0.20%，PSNR 的变异系数仅为 0.07%，证实 ChordEdit 对随机种子几乎不敏感。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/015_Figure_11.jpg]]
*Figure 11: Pareto dominance and Seed robustness. Left: LPIPS–CLIP Pareto fronts [37] comparing ChordEdit (solid) to the naive baseline (dashed). Shaded regions denote the envelope across seeds. Fronts for ChordEdit with n = 1 . . . 4 are nearly overlapping and dominate the naive counterparts, indicating negligible marginal returns from multi-noise. Right: histograms of CLIP-Edited and PSNR across 20 seeds for singlenoise (n=1). Both distributions are tight (CLIP CoV 0.20%, PSNR CoV 0.07%), confirming that ChordEdit one noise is effectively insensitive to the random seed*

### 跨模型泛化验证

Table 3 验证了 ChordEdit 的模型无关性。在 SD-Turbo、SwiftBrush-v2 和 LCM 等多个一步 T2I 模型上，ChordEdit 一致地超越了朴素基线。例如在 SwiftBrush-v2 上，PSNR 从基线的 21.38 提升至 22.20，CLIP-Edited 从 21.96 提升至 22.96，证明了和弦控制场策略不依赖于特定模型架构。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/013_Table_3.jpg]]
*Table 3: Quantitative comparison on different T2I models. Our method (Ours) consistently outperforms the naive baseline across all tested models. Full details are provided in the Appendix*

### 编辑强度可控性

Figure 20 展示了步长尺度 λ 的定性分析。λ 作为直观的“编辑强度”控制器：较小的 λ（如 0.8）产生微妙的欠编辑效果，随着 λ 增大，编辑强度逐步增强，而背景结构始终保持稳定。这一特性使得用户可以根据需求灵活调节编辑力度。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/026_Figure_20.jpg]]
*Figure 20: Qualitative analysis of the step scale λ. We vary λ while keeping other parameters fixed. λ functions as an intuitive ’edit strength’ controller. Small values (e.g., λ = 0.8) result in subtle, under-edited images (’mountain’). As λ increases, the intensity of the target semantic (’volcano’) becomes progressively stronger. This provides a simple and predictable knob for users to modulate the edit’s impact*

### 用户研究

Figure 21 汇总了四选一盲评的用户偏好率。ChordEdit 在语义对齐上获得 **42.5%** 的偏好率，在背景保存质量上获得 **48.3%** 的偏好率，在两个维度上均显著领先于对比方法，与定量指标的趋势高度一致。

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/028_Figure_21.jpg]]
*Figure 21: User Study Results. Aggregated human preference rates from a four-way blind comparison, matching the data cited in the main paper. ChordEdit was the clear winner in both Semantic Alignment (42.5%) and Preservation Quality (48.3%), demonstrating its superior overall performance*

### 失败模式与边界分析

尽管 ChordEdit 在绝大多数场景下表现鲁棒，但分析揭示了以下边界条件：
- 当语义变化幅度极大（如将“猫”编辑为“摩天大楼”）时，单步传输的容量受限，编辑可能不彻底。此时需适当增大 λ 或启用近端细化来补偿。
- 超参数 δ、t、λ 和 t_c 目前依赖经验调优，尚未实现自适应调整。在极端编辑需求下，不当的参数组合可能导致语义不足或背景漂移。

### 补充图表

![[assets/figures/papers/paper_list_l2026_https_arxiv_org_abs_2602_19083/figures/003_Figure_3.jpg]]
*Figure 3: One-Step Simple drift editing fails. ChordEdit preserves structure. Simple drifts, a direct drift-difference from a one-step model, induce a high-energy, non-smooth vector field, yielding two disqualifying failures: (i) severe object distortion and (ii) background breakup and spurious structures. Zoomed crops (bottom) highlight the distortions in Simple drifts versus the faithful, photorealistic result of ChordEdit*

## 方法谱系与知识库定位

### 一步编辑的困境与朴素漂移的失败

在文本引导图像编辑领域，多步扩散模型长期依赖**训练无关/逆无关**的范式，通过迭代应用朴素漂移差值（simple drift difference）实现稳定的编辑轨迹。该差值的定义为：

$$\Delta v(x_t, t) = v(x_t, t, c_{\mathrm{tar}}) - v(x_t, t, c_{\mathrm{src}})$$

其中 $v$ 为预训练 T2I 模型诱导的条件概率流 ODE 的漂移项。在多步推理中，每一步仅施加微小的漂移修正，累积误差可控；然而，当将该朴素差值直接作用于**一步蒸馏模型**（如 SD-Turbo、SwiftBrush-v2）时，所诱导的矢量场呈现高能量、非平滑的特性（见 Figure 3），导致单步大步长积分时出现严重的物体扭曲和背景崩坏。这一瓶颈使得训练无关、逆无关的单步编辑在此前不可行。

### 方法谱系：ChordEdit 的定位

ChordEdit 在以下维度上重新定义了编辑方法的效率-保真度边界：

| 维度 | 多步方法（FlowEdit 等） | 少步方法（InfEdit） | 训练依赖一步方法（SwiftEdit） | **ChordEdit（本文）** |
|------|------------------------|---------------------|-------------------------------|----------------------|
| 训练需求 | 训练无关 | 训练无关 | 需要训练专用网络 | **训练无关** |
| 反演需求 | 需反演（Direct Inversion）或不需（FlowEdit） | 不需 | 不需 | **不需** |
| NFE | 33–50+ | 4 | 1 | **1（+可选1 NFE近端细化）** |
| 编辑场构造 | 朴素漂移差值（多步迭代稳定） | 朴素漂移差值 | 学习到的编辑网络 | **和弦控制场（时间平滑低能量场）** |
| 运行时（PIE-bench） | 7.22 s（FlowEdit, 33步） | — | — | **0.38 s（19×加速）** |

**FlowEdit** 代表了训练无关/逆无关的多步编辑路线，通过 33 步迭代漂移实现稳定编辑，但其推理开销较高。**SwiftEdit** 则走向另一端——通过训练专用网络实现一步编辑，牺牲了训练无关的灵活性。**InfEdit** 以 4 步推理在效率与保真度间寻求折中。**Direct Inversion + PnP** 则依赖反演过程，引入了额外的计算负担和反演误差。

ChordEdit 的核心创新在于从**动态最优输运**（Benamou–Brenier 公式）的视角重新审视编辑问题，将源提示分布到目标提示分布的传输视为最小化动能的最优控制问题：

$$\min_{\rho,u} \int_0^1 \int \frac{1}{2} \|u_t(x)\|^2 \rho_t(x) dx dt \quad \mathrm{s.t.} \quad \partial_t \rho_t(x) + \nabla_x \cdot (\rho_t(x) u_t(x)) = 0$$

基于此理论框架，ChordEdit 通过**因果核平滑**（时间加权平均）从可观测的模型输出中构造低能量和弦控制场：

$$\hat{u}_t(x_{\tau}) = \frac{t \mathbf{R}(x_{\tau}, t-\delta) + \delta \mathbf{R}(x_{\tau}, t)}{t+\delta}$$

其中 $\mathbf{R}(x_{\tau}, t)$ 为可观测代理编辑场，$\delta$ 为时间平滑窗口。由 Jensen 不等式可证，该和弦场是 $L^2$ 收缩算子（$\int \|\hat{u}\|^2 \leq \int \|\mathbf{R}\|^2$），有效抑制了朴素场中的能量尖峰，使单步大步长积分成为可能。

### 消融揭示的因果机制

消融实验（Table 2）清晰地解耦了 ChordEdit 两个组件的功能分工：

- **和弦传输场（$\delta > 0$，无近端细化）**：优先保证背景一致性，在 SD-Turbo 上实现 PSNR 23.89（相较朴素 $\delta=0$ 的 21.89 提升 +2.00），但语义对齐相对保守（CLIP-Edited 21.87）。
- **近端细化（可选单步前向传递）**：通过目标提示的单步前向传递增强目标语义，将 CLIP-Edited 提升至 22.96（+1.09），同时 PSNR 仍保持在 22.20。

这一解耦设计使得 ChordEdit 在感知质量-语义对齐的 Pareto 前沿上严格支配朴素基线（Figure 9 bottom）。

### 关键超参数与鲁棒性

时间平滑窗口 $\delta$ 是 ChordEdit 稳定性的核心调节旋钮。$\delta=0$ 退化为朴素高能量场，随着积分步数 $S \to 1$，能量急剧上升，PSNR 崩溃；而 $\delta=0.15$ 时能量保持低位，PSNR 稳定（Figure 9 top）。此外，蒙特卡洛噪声样本数 $n$ 对性能的边际收益可忽略——$n=1$ 已实现最佳性能，且跨 20 个随机种子的 CLIP-Edited 变异系数仅 0.20%、PSNR 变异系数仅 0.07%（Figure 11），表明方法对随机种子高度鲁棒。

### 适用边界与局限

**当前已验证的适用边界：**
- 一步蒸馏 T2I 模型（SD-Turbo、SwiftBrush-v2）上的文本引导图像编辑
- 基于 PIE-bench 的编辑任务（物体替换、属性编辑、风格迁移等）
- 训练无关、逆无关、单步推理场景

**需要手动验证的潜在局限：** 论文未明确报告失败案例或局限性章节，以下边界需在实际部署中验证：
- 超参数 $\delta$、$t$、$\lambda$ 和 $t_c$ 目前依赖经验调优，在分布外图像或极端编辑指令下的泛化性未经验证
- 和弦控制场的理论风险界 $O(\delta)$ 在更大语义变化（如大幅度形变、视角变换）下是否保持尚不明确

### 开放问题

1. **自适应超参数调优**：当前 $\delta$ 等超参数依赖人工设定，能否根据输入图像内容和编辑指令的语义距离自适应调整？
2. **跨模态扩展**：该方法在视频编辑（时序一致性）或 3D 编辑（多视角一致性）任务上的扩展性如何？和弦控制场的因果平滑机制是否可直接迁移至时空域？
3. **非扩散模型适用性**：ChordEdit 的控制策略基于条件概率流 ODE 的漂移场，能否扩展到非扩散类生成模型（如 GAN 或自回归模型）的编辑场景？
4. **理论紧致性**：和弦控制场的 $O(\delta)$ 风险界在更一般的分布传输问题中是否紧致？是否存在更优的平滑核设计？

## 原文 PDF

![[paperPDFs/CVPR_2026/ChordEdit_One_Step_Low_Energy_Transport_for_Image_Editing.pdf]]

---
title: Enhancing 3D Human Motion Prediction with Gaze informed Affordance in 3D Scenes
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D_Scenes.pdf
project_link: null
code_link: null
aliases:
- SGP
- E3HMPGIA3S
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 前向模型超参数（尤其是 SLM 像素分辨率）以及前向传播模型类型（自由空间传播 vs 傅里叶全息）是控制 GS-PINN 性能的核心杠杆。
primary_logic: 通过 Saltelli 扩展的 Sobol 全局敏感性分析，揭示了 SLM 像素分辨率是影响 GS-PINN 神经网络性能的首要因素，自由空间传播模型整体优于傅里叶全息；在此基础上提出的复合评估指标整合了性能一致性、泛化能力和超参数扰动鲁棒性，为不同 CGH 配置下的统一基准建立了标准。
claims:
- SLM 像素分辨率是影响神经网络灵敏度的主要因素。
- 自由空间传播前向模型相比傅里叶全息能显著提升 GS-PINN 的神经网络性能。
- 引入了一个结合性能一致性、泛化能力和超参数扰动鲁棒性的复合评估指标，为跨配置的统一基准建立了标准。
- h_mid 超参数配置 (1024 个 FMH 组合, 自由空间 vs 傅里叶) 上 PSNR (GS-PINN) = 自由空间传播 (base_free 或 base_fourier_free)
---

# Enhancing 3D Human Motion Prediction with Gaze informed Affordance in 3D Scenes

> [!tip] 核心洞察
> 通过 Saltelli 扩展的 Sobol 全局敏感性分析，揭示了 SLM 像素分辨率是影响 GS-PINN 神经网络性能的首要因素，自由空间传播模型整体优于傅里叶全息；在此基础上提出的复合评估指标整合了性能一致性、泛化能力和超参数扰动鲁棒性，为不同 CGH 配置下的统一基准建立了标准。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向计算机生成全息图的基于 Gerchberg-Saxton 的物理启发神经网络的鲁棒性与泛化：一种敏感性分析框架 |
| 英文题名 | Enhancing 3D Human Motion Prediction with Gaze informed Affordance in 3D Scenes |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 基于 Sobol 敏感性分析的 GS-PINN 全局敏感性评估框架 |
| Dataset | h_mid 超参数配置, Sobol 全局敏感性分析 |

> [!tip] 效果简介
> - h_mid 超参数配置 (1024 个 FMH 组合, 自由空间 vs 傅里叶) 上，PSNR (GS-PINN) 自由空间传播 (base_free 或 base_fourier_free) vs 傅里叶全息 (base_fourier_fourier) (显著优于 (p=2.03e-169, Wilcoxon signed-rank test))；SSIM (GS-PINN) 自由空间传播 vs 傅里叶全息 (显著优于 (p=2.03e-169, 基于基模型 base_fourier))；PSNR (GS 算法) 傅里叶全息 vs 自由空间传播 (傅里叶显著优于自由空间 (p<2.36e-168, iteration 1))。
> - Sobol 全局敏感性分析 (h_mid) 上，总效应敏感指数 ST SLM 像素分辨率 (M) ST=0.82 (PSNR), ST=0.96 (SSIM) vs 传播距离 (d) ST=0.19 (PSNR) (SLM 像素分辨率支配方差)。

## 概要

计算机生成全息图（CGH）的相位恢复质量高度依赖于前向传播模型及其超参数（Forward Model Hyperparameters, FMH）的选择。GS-PINN 等物理启发神经网络虽然在相位恢复任务中展现出优势，但其性能在不同硬件配置下难以泛化——同一网络在不同 SLM 像素分辨率、像素间距、波长或传播距离下可能表现迥异，而现有研究缺乏对这些超参数影响的系统量化与公平基准。

本文的核心洞察是：**通过 Saltelli 扩展的 Sobol 全局敏感性分析，揭示 SLM 像素分辨率是支配 GS-PINN 神经网络性能的首要因素**（PSNR 总效应指数 ST = 0.82，SSIM 的 ST = 0.96），其影响力远超传播距离、像素间距和波长等参数；同时，**自由空间传播前向模型（ASM）相比傅里叶全息能显著提升 GS-PINN 的性能**（Wilcoxon 符号秩检验 p = 2.03e-169），为模型参数化和泛化提供了更优的基础。

在此基础上，本文提出了一个**复合评估指标**，将性能一致性、泛化能力与超参数扰动鲁棒性加权整合，为不同 CGH 配置下的统一基准建立了标准，从而缓解了因 FMH 配置差异导致的模型间不可比问题。

在方法谱系上，本工作定位于物理启发神经网络（PINN）与全局敏感性分析的交叉地带。与直接改进相位恢复算法精度的工作不同，本文聚焦于**评估框架本身**——不提出新的网络架构或损失函数，而是建立一套可复用的敏感性量化工具链。基线方法包括经典 Gerchberg-Saxton（GS）迭代算法，以及分别使用傅里叶全息和自由空间传播前向模型的 GS-PINN 变体。通过准蒙特卡洛采样（Saltelli 扩展的 Sobol 序列）在 h_inner、h_mid、h_outer 三个超参数区域进行全范围分析，本文揭示了超参数影响随区域变化的规律，并发现一阶和二阶 Sobol 指数在有限实验数量下不稳定，最终以总效应指数 ST 作为主要分析依据。

主要实证发现可概括为三点：
1. **SLM 像素分辨率是核心控制杠杆**，在 h_mid 区域的 Sobol 分析中其总效应指数远超其他参数。
2. **前向模型选择产生方向性差异**：自由空间传播在 GS-PINN 上显著优于傅里叶全息，但这一趋势在经典 GS 算法上恰好相反，暗示神经网络与迭代算法对前向模型的敏感模式存在本质区别。
3. **复合指标框架**为解决 FMH 引发的参数复杂度问题提供了结构化方案，但其权重系数（α, β, γ）需根据具体应用场景手动设定，通用性仍有待验证。



### 计算机生成全息图与相位恢复

计算机生成全息图（Computer-Generated Holography, CGH）通过计算光的衍射传播，在目标平面上重建期望的光场分布，其核心挑战在于**相位恢复**——即从已知的目标振幅反推出空间光调制器（SLM）上所需的相位分布。经典方法中，Gerchberg-Saxton（GS）算法通过在前向传播与反向传播之间交替施加振幅约束，以迭代方式逼近可行解。然而，GS 算法的收敛速度与最终精度高度依赖于初始相位选择，且其迭代过程缺乏对物理先验的显式利用。

### GS-PINN 的兴起与隐藏瓶颈

为克服上述局限，研究者将 GS 算法展开为物理启发神经网络（Physics-Inspired Neural Networks, PINN），通过可学习的相位初始化网络替代随机初始相位，从而在无监督框架下实现端到端的相位恢复训练。这类 GS-PINN 方法的核心在于**前向模型**的选择——它定义了光从 SLM 平面到全息平面之间的传播物理过程。两种主流前向模型分别为：

- **傅里叶全息**：利用透镜的傅里叶变换性质，将 SLM 平面的波场映射到后焦面，其唯一的前向模型超参数是 SLM 像素分辨率。
- **自由空间传播（角谱法，ASM）**：通过带宽限制的角谱方法模拟光场传播，其超参数包括波长、传播距离、SLM 像素分辨率和像素间距。

**真实瓶颈在于**：GS-PINN 的相位恢复性能高度依赖于前向模型及其超参数（Forward Model Hyperparameters, FMH）的选择。不同的 FMH 配置会导致同一模型在相同任务上表现出显著差异的性能，这使得模型在不同硬件配置下难以泛化，且各方法之间缺乏公平的基准比较标准。如图 2 所示，傅里叶全息与自由空间传播两种前向模型引入了不同维度的超参数空间，而这些超参数对网络性能的影响程度和影响机制在此前从未被系统量化。

### 现有方法的缺口

在本文之前，CGH 领域的模型评估存在以下关键缺口：

1. **缺乏全局敏感性分析**：现有工作通常采用固定的 FMH 组合进行训练与评估，未揭示各超参数对网络性能的独立贡献及交互效应。这导致研究者无法判断性能波动究竟源于模型架构改进，还是仅由超参数配置差异引起。
2. **基准比较不公平**：由于不同前向模型引入的参数复杂度不同（图 5 顶部面板所示），直接比较 PSNR 或 SSIM 等单一指标无法反映模型在超参数扰动下的鲁棒性，也难以衡量其泛化能力。
3. **前向模型选择缺乏指导**：自由空间传播与傅里叶全息在 GS-PINN 和传统 GS 算法上的相对优势未被系统比较，导致模型设计时缺乏选择前向模型的依据。

### 本文动机与核心思路

针对上述缺口，本文提出了一套**基于 Sobol 全局敏感性分析的 GS-PINN 评估框架**，其核心动机在于：

- **量化 FMH 影响**：采用 Saltelli 扩展的 Sobol 序列准随机采样方法，在归一化超参数空间的内层（h_inner）、中层（h_mid）和外层（h_outer）三个区域进行全范围采样（图 3），通过计算总效应敏感指数（ST）揭示各超参数对网络性能方差的贡献。
- **建立统一基准**：引入**复合评估指标** Υ = α Υ_GSW + β Υ_GM + γ Υ_R，将 GS-加权性能一致性、泛化能力和超参数扰动鲁棒性整合为单一度量，从而消除因 FMH 配置差异导致的模型性能不可比问题（图 5 底部面板示意）。
- **指导前向模型选择**：通过大规模蒙特卡洛比较，系统评估自由空间传播与傅里叶全息在 GS-PINN 和 GS 算法上的性能差异，为不同应用场景下的前向模型选择提供实证依据。

通过这一框架，本文旨在为 CGH 领域的物理启发神经网络研究提供**可复现的敏感性分析工具**和**公平的基准测试标准**，从而推动鲁棒且可泛化的相位恢复方法发展。



## 核心方法与创新机理

本工作的核心创新并非提出一种全新的相位恢复网络架构，而是**为 GS‑PINN 类方法建立了一套系统性的全局敏感性评估框架**，解决了该类方法在跨硬件配置下性能不可比、泛化能力不明的根本瓶颈。其关键创新体现在两个紧密耦合的 **changed slots** 上。

### 从前向模型超参数“黑箱”到全局敏感性量化

在 GS‑PINN 的现有范式中，前向模型超参数（Forward Model Hyperparameters, FMH）——如 SLM 像素分辨率、像素间距、传播距离和波长——通常被视为固定配置，其对神经网络性能的影响缺乏系统理解。这导致两个直接后果：① 不同文献中的模型性能无法公平比较，因为性能差异可能源于 FMH 选择而非算法本身；② 模型在未见过的硬件配置上泛化能力不可知。

本工作将 FMH 选择从固定的“环境变量”转变为一个可系统研究的 **控制杠杆**。具体而言，采用 **Saltelli 扩展的 Sobol 序列准随机采样**，在归一化超参数空间的三个代表性区域——h_inner、h_mid、h_outer——分别生成大量 FMH 配置（h_mid 区域 $N=1024$ 产生 10240 组配置，h_outer 和 h_inner 各 $N=256$ 产生 2560 组实验，见 Figure 3 及 TABLE I）。在此基础上，通过方差分解计算每个超参数的一阶敏感指数 $S_i$、二阶交互指数 $S_{ij}$ 和总效应指数 $S_{T_i}$：

$$S_{T_i} = \frac{\mathbb{E}_{{\mathbf{X}}_{\sim i}}\left(\mathbb{V}_{X_i}[Y \mid {\mathbf{X}}_{\sim i}]\right)}{V(Y)} = 1 - \frac{\mathbb{V}_{{\mathbf{X}}_{\sim i}}\left(\mathbb{E}_{X_i}[Y \mid {\mathbf{X}}_{\sim i}]\right)}{V(Y)}$$

这一量化框架直接揭示了 **SLM 像素分辨率是支配 GS‑PINN 性能的首要因素**（PSNR 的 $S_T=0.82$，SSIM 的 $S_T=0.96$，见 TABLE II），其影响远超传播距离（$S_T=0.19$）等其他超参数。该发现为 GS‑PINN 的硬件适配和模型设计提供了明确的优先级指引。

> **证据强度**：需注意由于实验数量有限，一阶（$S_1$）和二阶（$S_2$）指数表现不稳定，当前结论主要依赖总效应指数 $S_T$。这意味着参数间的精细交互效应尚未被充分揭示，该点需在解读时审慎对待。

### 从单指标评估到复合基准的统一框架

传统 CGH 方法通常仅以 PSNR 或 SSIM 等单一指标评估性能，无法反映模型在不同 FMH 配置下的一致性和鲁棒性。本工作提出的 **复合评估指标** $\Upsilon$ 将评估维度扩展至三个层面：

$$\Upsilon = \alpha (\Upsilon_{\mathrm{gsw}}) + \beta (\Upsilon_{\mathrm{gm}}) + \gamma (\Upsilon_{\mathrm{r}})$$

其中，$\Upsilon_{\mathrm{gsw}}$ 为 GS‑加权指标（衡量模型相对于 GS 算法基线的性能提升），$\Upsilon_{\mathrm{gm}}$ 为泛化指标（衡量模型在未见过 FMH 配置上的表现），$\Upsilon_{\mathrm{r}}$ 为鲁棒性指标（衡量模型对超参数微扰的敏感程度）。三者通过权重 $\alpha, \beta, \gamma$ 灵活组合，为不同 CGH 应用场景提供了统一的基准测试标准（见 Figure 5）。

这一复合指标的核心价值在于：它直接回应了“同一模型在不同前向模型配置下性能不一致”这一参数复杂性问题。例如，Figure 10 的小提琴图显示，自由空间传播前向模型在 GS‑PINN 上的 PSNR 显著优于傅里叶全息（Wilcoxon signed‑rank test，$p=2.03\times10^{-169}$），而 GS 算法本身却呈现完全相反的趋势——傅里叶全息显著优于自由空间传播（$p<2.36\times10^{-168}$）。若仅用单一 PSNR 指标评估，这些因前向模型选择而产生的性能反转将被掩盖，而复合指标通过整合多维度信息，使跨配置的公平比较成为可能。

> **公平性说明**：复合指标的权重 $(\alpha, \beta, \gamma)$ 需根据具体实验需求手动设定，论文未提供通用的自动确定方法，这可能在实际应用中引入一定的主观性。此外，GS‑加权指标的有效性依赖于 GS 算法本身作为基线的普适性——当 GS 算法在某些配置下表现不佳时，该维度的参考价值可能受限。



本工作构建了一套面向 GS-PINN 前向模型超参数（FMH）的全局敏感性评估框架，其核心目标并非提出新的相位恢复网络，而是为不同硬件配置下的 CGH 方法建立一个可比较、可复现的基准测试体系。整体 pipeline 由五个功能模块串联而成，形成“初始化—传播—迭代优化—敏感性量化—复合评估”的闭环。

### 模块一：相位初始化神经网络

框架沿用 GS-PINN 中仅保留全息平面的相位检索网络（Phase Retrieval Neural Network），以目标图像为输入，通过复数卷积神经网络预测一个初始相位估计，替代传统 GS 算法中的随机初始相位。这一设计在保证计算效率的同时，为后续的迭代展开提供了更优的起点。网络结构如图 1 所示，包含相位初始化、波前调整和相位调整三个子网络，但本框架仅使用相位初始化部分以加速实验。

### 模块二：前向传播模型

相位初始化后，光场需通过前向模型（Forward Model, FM）从 SLM 平面传播至全息平面。框架支持两类前向模型：

- **傅里叶全息**：假设 SLM 与全息平面之间存在一个透镜，前后焦面的波场由傅里叶变换关联，其唯一超参数为 SLM 像素分辨率 $M$。
  
  $$ \Psi_{\mathrm{Fourier}}(\Gamma(\mathbf{x},\mathbf{y})) = \gamma \mathcal{F}(\Gamma(\mathbf{x},\mathbf{y})) = \Gamma(\mathbf{u},\mathbf{v}) $$

- **自由空间传播（ASM）**：采用带宽限制的角谱方法模拟光场在自由空间中的衍射传播，超参数包括波长 $\lambda$、传播距离 $d$、SLM 像素分辨率 $M$ 和像素间距 $\Delta x$。

  $$ \Psi_{\mathrm{ASM}}(\Gamma(\mathbf{x},\mathbf{y})) = \widetilde{\mathcal{F}}[\Gamma(\mathbf{u},\mathbf{y}) \, \mathrm{H}(\lambda, \Delta x, M, d)] $$

两类模型及其超参数的对应关系由图 2 给出。前向模型的选择及其超参数组合构成了本框架分析的核心对象——FMH 配置空间。

### 模块三：GS 迭代展开与无监督训练

将经典 Gerchberg-Saxton 算法展开为可微分的迭代过程，在目标平面与全息平面之间交替施加振幅约束。损失函数直接作用于目标平面的重建强度与目标图像之间：

$$ \text{Loss}\Big( \left| \mathrm{E}_{\mathrm{TP}}(\mathbf{x}, \mathbf{y}) \right|^{2}, \mathcal{T}_{\mathrm{TP}}(\mathbf{x}, \mathbf{y}) \Big) $$

训练过程为无监督方式，仅需目标图像即可优化相位初始化网络的参数。这一模块的输出是给定 FMH 配置下的训练后网络性能（以 PSNR、SSIM 等精度函数度量）。

### 模块四：Sobol 全局敏感性分析

这是框架的方法论核心。采用 Saltelli 扩展的 Sobol 序列进行准蒙特卡洛采样，在归一化超参数空间的三个区域——h_inner、h_mid、h_outer（图 3，具体取值见 Table I）——分别生成 FMH 配置样本。对于 h_mid 区域，$N=1024$ 个基样本经 Saltelli 采样矩阵扩展为 10240 个 FMH 配置；对于 h_inner 和 h_outer，$N=256$ 各产生 2560 个实验配置。

基于方差分解的 Sobol 指数用于量化每个超参数对网络性能方差的贡献：

- **一阶指数** $S_i$：参数 $X_i$ 单独的主效应贡献。
- **总效应指数** $S_{T_i}$：参数 $X_i$ 的主效应及其与所有其他参数的交互效应之和。

$$ S_{T_i} = \frac{\mathbb{E}_{\mathbf{X}_{\sim i}}\left(\mathbb{V}_{X_i}[Y \mid \mathbf{X}_{\sim i}]\right)}{V(Y)} = 1 - \frac{\mathbb{V}_{\mathbf{X}_{\sim i}}\left(\mathbb{E}_{X_i}[Y \mid \mathbf{X}_{\sim i}]\right)}{V(Y)} $$

由于有限实验数量下一阶和二阶指数不稳定，框架最终以总效应指数 $S_{T_i}$ 作为主要分析依据。

### 模块五：复合评估指标

为克服单一指标（如 PSNR）在不同 FMH 配置下无法公平比较模型性能的瓶颈，框架引入复合评估指标 $\Upsilon$，加权整合三个维度：

$$ \Upsilon = \alpha (\Upsilon_{\mathrm{gsw}}) + \beta (\Upsilon_{\mathrm{gm}}) + \gamma (\Upsilon_{\mathrm{r}}) $$

- **$\Upsilon_{\mathrm{gsw}}$（GS-加权指标）**：以 GS 算法在相同 FMH 下的性能为参照，衡量 GS-PINN 的相对提升。
- **$\Upsilon_{\mathrm{gm}}$（泛化指标）**：评估模型在未见过 FMH 配置上的性能保持能力。
- **$\Upsilon_{\mathrm{r}}$（鲁棒性指标）**：量化模型对超参数扰动的容忍度。

该复合指标的设计逻辑由图 5 阐释：上半部分展示了不同算法在相似 FMH 配置下的性能不一致性如何使基准测试复杂化；下半部分则说明复合指标如何通过整合多维性能信息，建立跨 CGH 配置的统一基准标准。权重 $\alpha, \beta, \gamma$ 需根据具体应用场景手动设定，这是框架的一个实用灵活性来源，同时也引入了主观性因素。

### 数据流总结

输入目标图像 → 相位初始化网络预测初始相位 → 前向模型（傅里叶或 ASM）传播至全息平面 → GS 迭代展开进行无监督优化 → 输出重建全息图及精度指标 → Sobol 敏感性分析量化各超参数贡献 → 复合指标综合评定模型性能。整个 pipeline 在 h_inner、h_mid、h_outer 三个超参数区域分别执行，以揭示超参数影响在不同参数尺度下的变化规律。

### 补充图表

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/001_Figure_1.jpg]]
*Figure 1: GS-Physics Inspired Neural Network (GS-PINN) with Phase Initialization, Wavefront and Phase Adjustment Neural networks (Algorithm 2). The laser constraints consist of a linearly polarized beam with uniform amplitude, and the ’star’ symbol represents the formation of a complex wavefront*



### 前向模型与超参数空间

GS-PINN 的相位恢复性能高度依赖于前向模型及其超参数（FMH）的选择，这是本研究的核心瓶颈。框架中涉及两种前向传播模型：

**傅里叶全息（Fourier Holography）** 假设 SLM 平面和全息平面之间放置一个透镜，两平面上的波场通过傅里叶变换关联：

$$\Psi_{\mathrm{Fourier}}(\Gamma(\mathbf{x},\mathbf{y})) = \gamma \mathcal{F}(\Gamma(\mathbf{x},\mathbf{y})) = \Gamma(\mathbf{u},\mathbf{v})$$

其中 $\gamma = \exp(2 \mathrm{i} k f) / \mathrm{i} \lambda f$ 为相位因子，$k$ 为波数，$\lambda$ 为波长，$f$ 为焦距。该模型仅有一个超参数：SLM 像素分辨率 $M$。

**自由空间传播（Free Space Propagation）** 采用带宽限制的角谱方法（ASM）模拟光场传播：

$$\Psi_{\mathrm{ASM}}(\Gamma(\mathbf{x},\mathbf{y})) = \widetilde{\mathcal{F}}[\Gamma(\mathbf{u},\mathbf{y}) \mathrm{H}(\lambda, \Delta x, M, d)]$$

该模型包含四个超参数：波长 $\lambda$、传播距离 $d$、SLM 像素间距 $\Delta x$ 和像素分辨率 $M$。这些 FMH 构成了敏感性分析的输入空间（Fig. 2）。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/002_Figure_2.jpg]]
*Figure 2: Forward Models (FM) and Forward Model Hyperparameters (FMH). For Fourier holography SLM pixel-resolution is the FMH (Eq. 1). For free space propagation wavelength of light, propagation distance, SLM pixel-resolution and pixel-pitch are the FMH (Eq. 2)*

### GS-PINN 训练框架

GS-PINN 将经典 Gerchberg-Saxton 迭代算法展开为可训练的神经网络（Algorithm 2）。其核心模块为**相位初始化神经网络**（NN_TP^θ），该网络在目标平面预测初始相位，替代传统 GS 算法中的随机初始相位。为加速计算，框架仅在全息平面使用复数卷积神经网络进行相位检索。

训练采用无监督方式，损失函数衡量重建全息图与目标图像之间的相关性：

$$A = \frac{\sum \widetilde{I}(x,y,z) I(x,y,z)}{\sqrt{\sum I(x,y,z)^2 \sum \widetilde{I}(x,y,z)^2}}$$

### Sobol 全局敏感性分析

为量化各 FMH 对神经网络性能的影响，框架引入基于 Saltelli 扩展的 Sobol 方差分解方法。模型输出 $Y$ 的 ANOVA 分解形式为：

$$Y = f _ { 0 } + \sum _ { i } f _ { i } ( X _ { i } ) + \sum _ { i < j } f _ { i , j } ( X _ { i } , X _ { j } ) + \cdots + f _ { 1 , 2 , \ldots , k }$$

满足零积分条件：

$$\int _ { 0 } ^ { 1 } f _ { i _ { 1 } , i _ { 2 } , \ldots , i _ { s } } ( X _ { i _ { 1 } } , X _ { i _ { 2 } } , \ldots , X _ { i _ { s } } ) d X _ { i _ { w } } = 0$$

基于此分解，定义一阶 Sobol 指数衡量参数 $X_i$ 的独立方差贡献：

$$S_{i} = \frac{\mathbb{V}_{X_{i}}\left(\mathbb{E}_{\mathbf{X}_{\sim i}}[Y \mid \mathbf{X}_{i}]\right)}{V(Y)}$$

总效应指数衡量参数 $X_i$ 的总贡献（包含自身及所有高阶交互效应）：

$$S_{T_{i}} = \frac{\mathbb{E}_{{\mathbf{X}}_{\sim i}}\left(\mathbb{V}_{X_{i}}[Y \mid {\mathbf{X}}_{\sim i}]\right)}{V(Y)} = 1 - \frac{\mathbb{V}_{{\mathbf{X}}_{\sim i}}\left(\mathbb{E}_{X_{i}}[Y \mid {\mathbf{X}}_{\sim i}]\right)}{V(Y)}$$

实验发现一阶（S1）和二阶（S2）指数在有限实验数量下不稳定，因此最终分析主要依赖总效应指数 ST。

### 复合评估指标

为解决不同 FMH 配置下模型性能不可比的问题，框架提出复合评估指标：

$$\Upsilon = \alpha ( \Upsilon _ { \mathrm { g s w } } ) + \beta ( \Upsilon _ { \mathrm { g m } } ) + \gamma ( \Upsilon _ { \mathrm { r } } )$$

其中 $\Upsilon_{\mathrm{gsw}}$ 为 GS-加权性能指标（衡量相对于 GS 算法的性能提升），$\Upsilon_{\mathrm{gm}}$ 为泛化能力指标（衡量跨 FMH 配置的性能一致性），$\Upsilon_{\mathrm{r}}$ 为鲁棒性指标（衡量对超参数扰动的稳定性）。权重 $\alpha$、$\beta$、$\gamma$ 需根据具体 CGH 实验需求设定，论文未给出通用确定方法，这构成一个开放问题。

### 采样策略

敏感性分析在归一化超参数空间的三个区域进行：h_inner、h_mid 和 h_outer（Fig. 3）。采样采用 Saltelli 扩展的 Sobol 序列准随机采样方法。对于 h_mid 区域，$N=1024$ 生成 10240 个 FMH 配置（$k=4$ 参数）；对于 h_outer 和 h_inner，$N=256$ 各产生 2560 个实验配置。三个参考点的具体超参数取值见 TABLE I。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/003_Figure_3.jpg]]
*Figure 3: Normalized hyperparameter space with Inner, Mid and Outer points. Sampling for SA was performed using Saltelli’s extension of Sobol’s sequence [59]–[61]. For hmid*

### 补充图表

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/005_Figure_5.jpg]]
*Figure 5: FMH-induced parameter complexity and the composite metric. Top panel represents the inconsistency in performance of different algorithms for similar set of FMH configurations, complicating benchmarking. In the bottom panel, the composite metric addresses variability in model performance across similar FMH configurations, enabling more reliable benchmarking*



## 实验与关键发现

### 实验设置与前向模型超参数空间

本研究围绕 GS-PINN 的相位恢复性能对前向模型超参数（Forward Model Hyperparameters, FMH）的敏感性展开系统评估。实验涉及两类前向传播模型：**傅里叶全息**（Fourier Holography）和**自由空间传播**（Free Space Propagation, Angular Spectrum Method, ASM）。傅里叶全息的唯一超参数为 SLM 像素分辨率 $M$；自由空间传播的超参数则包括波长 $\lambda$、传播距离 $d$、SLM 像素间距 $\Delta x$ 和像素分辨率 $M$，共四个维度。

为覆盖不同超参数区间，实验在归一化 FMH 空间中定义了三个参考点：**h_inner**（内点）、**h_mid**（中点）和 **h_outer**（外点），具体取值见 **TABLE I**。基于 Saltelli 对 Sobol 序列的扩展方法进行准随机采样：对于 h_mid，$N = 1024$，生成 $10240$ 个 FMH 配置（$k=4$ 参数）；对于 h_outer 和 h_inner，$N = 256$，各生成 $2560$ 个实验配置（Fig. 3）。

### 主结果一：SLM 像素分辨率是主导因素

Sobol 全局敏感性分析的核心发现是：**SLM 像素分辨率 $M$ 是影响 GS-PINN 神经网络性能的首要因素**。在 h_mid 区域的 $10240$ 个 FMH 配置上，以 PSNR 为精度函数的 GS-PINN 总效应敏感指数 $S_T$ 中，SLM 像素分辨率的 $S_T = 0.82$，远超传播距离（$S_T = 0.19$）、像素间距（$S_T = 0.13$）和波长（$S_T = 0.05$）（**TABLE II**）。以 SSIM 为精度函数时，SLM 像素分辨率的支配性更加显著，$S_T$ 高达 $0.96$（**TABLE III**）。

Fig. 12 进一步揭示了 SLM 像素分辨率与 GS-PINN 性能之间的具体关系：随着 SLM 像素分辨率增大，GS-PINN 的 PSNR 呈现先下降后趋于平稳的趋势。这一趋势在基模型分别基于傅里叶全息（base_fourier）和自由空间传播（base_free）训练时均保持一致。相比之下，GS 算法本身对 SLM 像素分辨率的响应模式则有所不同（Fig. 13），表明神经网络在前向模型超参数变化下的行为与经典迭代算法存在结构性差异。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/012_Figure_12.jpg]]
*Figure 12: Relationship between SLM pixel-resolution and GS-PINN performance, measured in terms of PSNR accuracy function Eq. 5a. Base models were trained on Fourier holography (base fourier) Eq. 1 and free space propagation (base free) Eq. 2. The dotted lines in the left panel indicate the SLM parameters and corresponding PSNR scores for the base models. Finetuned models are labeled as base X Y, where X denotes the base model and Y specifies the forward model (FM) used for finetuning (1024 FMH configurations Fig. 4). The right panel presents Pearson and Spearman correlation coefficients, with statistically significant correlations*

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/013_Figure_13.jpg]]
*Figure 13: Relationship between SLM pixel-resolution and GS algorithm performance, measured in terms of PSNR accuracy function*

在 h_inner 和 h_outer 区域，SLM 像素分辨率的 $S_T$ 绝对值有所下降，但相对排序保持不变，传播距离、像素间距和波长的敏感性进一步降低（Fig. 7），说明超参数敏感性的空间分布是非均匀的，但 SLM 像素分辨率的主导地位具有跨区域的稳健性。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/007_Figure_7.jpg]]
*Figure 7: Sensitivity analysis (SA) for GS-PINN at*

### 主结果二：自由空间传播显著优于傅里叶全息

前向模型类型的对比实验给出了一个关键结论：**自由空间传播前向模型在 GS-PINN 上的神经网络性能显著优于傅里叶全息**。在 h_mid 区域的 $1024$ 个 FMH 配置上，以 PSNR 为指标，自由空间传播（base_free 或 base_fourier_free）的 GS-PINN 性能显著高于傅里叶全息（base_fourier_fourier），Wilcoxon 符号秩检验 $p = 2.03 \times 10^{-169}$（Fig. 10）。以 SSIM 为指标时，结论一致（Fig. 16）。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/010_Figure_10.jpg]]
*Figure 10: GS-PINN: Forward model comparison with respect to PSNR accuracy. Base models were trained on Fourier holography (base fourier) Eq. 1 or free-space propagation (base free) Eq. 2. Finetuned models (1024 FMH configurations Fig. 4) are labeled as base X Y, where X indicates the base model and Y the forward model (FM) used for finetuning. Violin plots (medians in dotted black lines, with extremes and mean values) show that free-space propagation consistently outperforms Fourier holography (first two plots), and base models perform better when finetuned with the same FM (last two plots). Wilcoxon signed-rank test (one-sided, alternative: “less”) confirmed significant differences*

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/017_Figure_16.jpg]]
*Figure 16: GS-PINN: Forward model comparison with respect to SSIM accuracy. Base models were trained on Fourier holography (base fourier) Eq. 1 or free space propagation (base free) Eq. 2. Finetuned models are labeled as base X Y, where X indicates the base model and Y the forward model (FM) (1024 FMH configurations Fig. 4) used for finetuning. Violin plots (medians in dotted black lines, with extremes and mean values) show that free space propagation consistently outperforms Fourier holography (first two plots), and base models perform better when finetuned with the same FM (last two plots). Wilcoxon signed-rank test (one-sided, alternative: “less”) confirmed significant differences*

值得注意的是，这一趋势在 GS 算法上完全相反：**傅里叶全息在 GS 迭代算法上的性能显著优于自由空间传播**（Fig. 11, $p < 2.36 \times 10^{-168}$）。这种前向模型在神经网络与经典算法上的“性能反转”现象，构成了本研究揭示的一个关键洞察——前向模型的选择对物理启发神经网络的影响机制与对传统迭代算法的影响机制截然不同，简单的“算法迁移”假设并不成立。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/011_Figure_11.jpg]]
*Figure 11: GS algorithm: Forward model comparison (1024 FMH configurations Fig. 4) with respect to PSNR accuracy. Violin plots (medians in dotted black lines, with extremes and mean values) show that Fourier holography Eq. 1 consistently outperforms free space propagation Eq. 2 for all iterations. Wilcoxon signed-rank test (one-sided, alternative: “greater”) confirmed significant differences (p < 0.025, marked *) include: (i) iteration 1 : W =523961, p=2.36e−168, n=1024, (ii) iteration 5 : W =524385*

### 主结果三：复合评估指标与参数复杂度

FMH 配置的多样性导致不同算法在同一组超参数配置下的性能排序出现不一致，使得跨配置的公平基准比较变得困难（Fig. 5 上层面板）。为此，论文引入了一个复合评估指标：

$$\Upsilon = \alpha \Upsilon_{\mathrm{gsw}} + \beta \Upsilon_{\mathrm{gm}} + \gamma \Upsilon_{\mathrm{r}}$$

其中 $\Upsilon_{\mathrm{gsw}}$ 为 GS-加权指标（衡量相对于 GS 算法基线的性能提升），$\Upsilon_{\mathrm{gm}}$ 为泛化指标（衡量跨 FMH 配置的性能一致性），$\Upsilon_{\mathrm{r}}$ 为鲁棒性指标（衡量对超参数扰动的恢复能力）。该复合指标通过加权汇总三个维度的性能得分，解决了因 FMH 配置不同而导致的模型性能不可比问题，为不同 CGH 配置下的统一基准建立了标准。

Fig. 14 的参数复杂度分析显示，GS-PINN 与 GS 算法在 PSNR 上存在相关性，但这种相关性受到 FMH 配置的显著调制，进一步验证了引入复合指标的必要性。

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/014_Figure_14.jpg]]
*Figure 14: Parameter complexity analysis for GS-PINN and the GS algorithm, evaluated using the PSNR accuracy function Eq. 5a. Models are labeled as*

### 消融与稳定性分析

**Sobol 指数的稳定性**：在有限实验数量下，一阶（$S_1$）和二阶（$S_2$）Sobol 指数表现不稳定，因此最终分析主要依赖总效应指数 $S_T$。这一消融发现限制了交互效应的深入解读，但 $S_T$ 本身已足以揭示主导超参数。

**超参数区域的效应变化**：在 h_inner 和 h_outer 区域分别训练并分析后，发现传播距离、像素间距和波长的 $S_T$ 绝对值均有所下降，表明超参数影响随区域变化而变化。这提示敏感性分析的结果对采样空间的选择具有一定依赖性，在将结论推广到极端超参数配置时需谨慎。

**损失函数的影响**：Fig. 20 展示了使用 MSE 损失函数时不同前向模型的重建可视化结果。与 PSNR 和 SSIM 精度函数下的结论一致，自由空间传播在视觉质量上也优于傅里叶全息，且缩放前后的对比揭示了重建全息图在动态范围上的差异。

### 失败模式与局限性

1. **训练不足**：所有实验仅使用 5 个 epoch 训练初始化网络，可能不足以充分优化网络参数，影响敏感性分析的精确定量结论。
2. **Sobol 低阶指数不稳定**：$S_1$ 和 $S_2$ 指数在有限实验数量下的不稳定性，限制了对超参数间交互效应的精细建模，当前分析仅能可靠地报告总效应。
3. **网络结构简化**：仅对包含一个初始化神经网络（NN_TP$^\theta$）的简化版 GS-PINN 进行了分析，未包含波前调整和相位调整网络的完整架构，其他变体的行为可能不同。
4. **复合指标权重的主观性**：$\alpha$、$\beta$、$\gamma$ 的设定缺乏通用确定方法，需要根据具体 CGH 应用场景手动调整，可能引入评估偏差。
5. **GS 基线依赖**：GS-加权指标 $\Upsilon_{\mathrm{gsw}}$ 依赖于 GS 算法本身在前向模型上的性能表现，当 GS 算法作为基线不普适时，复合指标的公平性可能受影响。

### 补充图表

![[assets/figures/papers/paper_list_l23_Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D/figures/027_Figure_20.jpg]]
*Figure 20: Visualization of network performance using the mean squared error (MSE) loss function for hmid FMH across different forward models. The first two columns (black-bordered) correspond to free space propagation, while the last two columns (bluebordered) represent Fourier holography. The upper triangular region in each panel shows the original image, while the lower triangular region displays the GS-PINN output. To ensure comparability, the outputs in the second and fourth columns are scaled to match the mean intensity of the corresponding original images. Performance metrics-including PSNR, SSIM, and accuracy*



## 定位与知识库关联

### 经典基线：Gerchberg-Saxton 算法

Gerchberg-Saxton (GS) 算法是计算机生成全息图（CGH）领域最经典的迭代相位恢复方法。它通过在 SLM 平面与目标平面之间交替施加振幅约束，逐步逼近满足双平面振幅分布要求的相位解。本文将其作为核心基线，并在算法层面将其展开（unrolling）为物理启发神经网络（GS-PINN），从而将传统迭代过程转化为可端到端训练的神经网络架构。

GS 算法的关键局限在于其对前向模型超参数（FMH）的敏感性：在自由空间传播模型下，GS 算法的 PSNR 性能显著低于傅里叶全息模型（p < 2.36e-168），这一趋势与 GS-PINN 恰好相反——后者在自由空间传播下表现更优。这种“模型-算法”交互效应的反转，构成了本文敏感性分析框架的核心动机之一。

### 物理启发神经网络谱系

本文的 GS-PINN 属于模型驱动深度学习（model-driven deep learning）或物理启发神经网络（Physics-Inspired Neural Networks）的方法谱系。其核心设计思路是将物理前向模型（傅里叶全息或自由空间传播的角谱法 ASM）嵌入神经网络的推理流程中，通过展开 GS 迭代并引入可训练的相位初始化网络（$NN_{TP}^\theta$），实现无监督的相位恢复训练。

**与前序工作的关系**：
- 本文仅使用 GS-PINN 的简化版本——只保留目标平面的相位初始化网络，省略了波前调整网络和相位调整网络，以降低计算开销并聚焦于前向模型超参数的敏感性分析。
- 相较于已有的 GS-PINN 变体（如包含完整三网络的版本），本文的简化设计牺牲了部分建模能力，但换取了在大规模超参数扫描（10240 个 FMH 配置）下的计算可行性。

**与并行/后续工作的潜在关系**：
- 本文提出的全局敏感性分析框架可推广至其他物理启发神经网络（如基于物理信息神经网络 PINN 的波前工程方法），但目前尚未有直接将 Sobol 方差分解用于 CGH 超参数分析的先例。
- 复合评估指标 $\Upsilon = \alpha \Upsilon_{gsw} + \beta \Upsilon_{gm} + \gamma \Upsilon_r$ 的引入，为不同 CGH 配置下的统一基准建立了标准，但其权重设定目前依赖人工经验，尚未与自动化超参数优化（如贝叶斯优化）方法进行系统对比。

### 前向模型选择：傅里叶全息 vs 自由空间传播

本文系统比较了两类前向模型：

| 前向模型 | 超参数 | 核心公式 | GS-PINN 性能 | GS 算法性能 |
|---------|--------|---------|-------------|------------|
| 傅里叶全息 | SLM 像素分辨率 $M$ | $\Psi_{\mathrm{Fourier}}(\Gamma(\mathbf{x},\mathbf{y})) = \gamma \mathcal{F}(\Gamma(\mathbf{x},\mathbf{y}))$ | 较差 | **较优** |
| 自由空间传播 (ASM) | 波长 $\lambda$、距离 $d$、像素分辨率 $M$、像素间距 $\Delta x$ | $\Psi_{\mathrm{ASM}}(\Gamma(\mathbf{x},\mathbf{y})) = \widetilde{\mathcal{F}}[\Gamma(\mathbf{u},\mathbf{y}) \mathrm{H}(\lambda, \Delta x, M, d)]$ | **较优** | 较差 |

**关键发现**：自由空间传播模型为 GS-PINN 提供了更丰富的参数化和更强的泛化能力（PSNR 显著优于傅里叶全息，Wilcoxon signed-rank test p = 2.03e-169），而 GS 算法在傅里叶全息下表现更优。这种“前向模型-算法”的交互效应表明，前向模型的选择不能脱离具体的相位恢复算法进行孤立评估——这正是本文复合评估指标试图解决的问题。

### 敏感性分析方法的知识库定位

本文采用的 **Saltelli 扩展的 Sobol 全局敏感性分析** 属于基于方差的准蒙特卡洛方法。在 CGH 领域，此前尚未有工作将 Sobol 指数系统应用于前向模型超参数的敏感性量化。

**方法适用边界**：
1. **Sobol 指数稳定性**：由于实验数量有限（$h_{mid}$ 区域 $N = 1024$，$h_{inner/outer}$ 区域 $N = 256$），一阶指数 $S_1$ 和二阶指数 $S_2$ 表现不稳定，当前分析主要依赖总效应指数 $S_T$。这意味着参数间的交互效应（如像素分辨率与波长的耦合）尚未得到充分解析。
2. **训练充分性**：GS-PINN 仅训练 5 个 epoch，可能不足以让初始化网络充分收敛，这会影响敏感性分析的精度。在更充分的训练条件下，超参数的相对重要性排序是否保持稳定，仍需验证。
3. **超参数空间范围**：分析覆盖了 $h_{inner}$、$h_{mid}$ 和 $h_{outer}$ 三个区域，但超参数范围的设定（如 $M \in [128, 2048]$）直接影响敏感性指数的绝对值。扩展超参数范围可能导致不同的主导因素排序。

### 局限与开放问题

**已识别的局限**：
- 仅分析了简化版 GS-PINN（仅含相位初始化网络），完整三网络架构下的超参数敏感性可能不同。
- 复合指标权重 $(\alpha, \beta, \gamma)$ 缺乏通用确定方法，需根据具体 CGH 应用场景手动调整。
- 论文标题与内容存在不一致（原始载荷标题为 3D 人体运动预测，实际内容为 CGH 敏感性分析），可能源于数据预处理错误，需人工核实。

**开放问题**：
1. 如何为不同 CGH 应用（如 AR 显示、光遗传学刺激）自动设定复合指标的最佳权重？
2. 自由空间传播与傅里叶全息在 GS-PINN 与 GS 算法上表现出的相反趋势，是否存在统一的物理解释（例如与模型容量和信息瓶颈相关）？
3. 当使用更多采样点或更大超参数范围时，$S_1$ 和 $S_2$ 指数能否变得稳定，从而揭示更精细的参数交互效应（如像素分辨率与波长的耦合对重建质量的非线性影响）？
4. 该敏感性分析框架能否直接推广到其他类型的物理启发神经网络（如基于衍射神经网络的波前整形），或需要针对不同物理前向模型进行适配？



## 原文 PDF

![[paperPDFs/CVPR_2025/Enhancing_3D_Human_Motion_Prediction_with_Gaze_informed_Affordance_in_3D_Scenes.pdf]]

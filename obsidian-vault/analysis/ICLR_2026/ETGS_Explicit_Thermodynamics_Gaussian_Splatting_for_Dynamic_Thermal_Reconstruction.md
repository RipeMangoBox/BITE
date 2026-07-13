---
title: "ETGS: Explicit Thermodynamics Gaussian Splatting for Dynamic Thermal Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ETGS_Explicit_Thermodynamics_Gaussian_Splatting_for_Dynamic_Thermal_Reconstructi_6090bdf94c7b.pdf
project_link: null
code_link: "https://github.com/jankin-wang/ETGS"
aliases:
- EETGS
- ETGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将具有闭式解析解的一阶热传导常微分方程直接嵌入显式高斯表示，使每个高斯基元都具备可学习的等效热容、换热系数和热源激发参数，并能在任意时刻高效计算温度。
primary_logic: 采用牛顿冷却定律与谐波热源激发组合构成一阶线性ODE，通过积分因子法与谐波展开推导出闭式温度演化公式，完全避免了数值积分，从而在保持静态3DGS相近训练与渲染效率的同时实现物理一致的动态热场景重建。
claims:
- ETGS在所有场景下的平均PSNR达到40.68 dB，显著优于NTR-Gaussian的34.96 dB，提升约5.7 dB。
- ETGS训练仅需197秒，而NTR-Gaussian需要1469秒；渲染速度458 FPS远超NTR-Gaussian的68 FPS。
- 移除热源激发项Q后PSNR从44.73降至43.70，移除正则项后降至42.58，验证了两者的必要性。
- 闭式解在附录A中完整推导，确保物理一致性与可微性，无需数值积分。
---

# ETGS: Explicit Thermodynamics Gaussian Splatting for Dynamic Thermal Reconstruction

> [!tip] 核心洞察
> 采用牛顿冷却定律与谐波热源激发组合构成一阶线性ODE，通过积分因子法与谐波展开推导出闭式温度演化公式，完全避免了数值积分，从而在保持静态3DGS相近训练与渲染效率的同时实现物理一致的动态热场景重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | ETGS：面向动态热重建的显式热力学高斯散射 |
| 英文题名 | ETGS: Explicit Thermodynamics Gaussian Splatting for Dynamic Thermal Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=P2Nw2LMkjH) · [Code](https://github.com/jankin-wang/ETGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ETGS (Explicit Thermodynamics Gaussian Splatting) |
| Dataset | RHD |

> [!tip] 效果简介
> - RHD (10个场景平均) 上，PSNR (dB) 40.68 vs 34.96 (NTR-Gaussian) (+5.72)；SSIM 0.989 vs 0.983 (Thermal3D-GS) (+0.006)；LPIPS 0.050 vs 0.072 (Thermal3D-GS) (-0.022)。

## 概要

动态热场景的三维重建与渲染是工业检测、热管理等领域的关键技术，但现有方法面临根本性困境：静态重建方法（如3DGS、Thermal3D-GS）无法捕捉温度随时间的变化；动态方法（如NTR-Gaussian）虽引入热力学建模，却依赖隐式神经表示与数值积分来融入物理方程，导致训练耗时近1500秒、渲染仅68 FPS，且误差累积严重。**ETGS**（Explicit Thermodynamics Gaussian Splatting）提出了一条截然不同的路径——将具有闭式解析解的一阶热传导常微分方程直接嵌入显式高斯表示，使每个高斯基元都具备可学习的等效热容、换热系数和谐波热源激发参数，从而在任意时刻高效计算温度，完全避免了数值积分的计算开销与误差累积。

核心结论是：ETGS在RHD数据集的10个场景上平均PSNR达到40.68 dB，相较NTR-Gaussian的34.96 dB提升约5.7 dB；训练仅需197秒（NTR-Gaussian需1469秒），渲染速度达458 FPS（NTR-Gaussian为68 FPS），效率接近静态3DGS。消融实验进一步验证，移除热源激发项后PSNR下降约1 dB，移除谐波系数正则项后下降约2.15 dB，证实了双组件温度模型（牛顿冷却指数项+谐波热源激发项）与正则化策略的必要性。

在方法谱系上，ETGS属于**物理驱动显式神经渲染**的范式：它继承3DGS的显式点基元与快速光栅化管线，但将高斯属性集从光学颜色（球谐系数）替换为热力学参数（$C_i, h_i, Q_i(t), T_i(t)$），并通过积分因子法与谐波展开推导出一阶线性ODE的闭式温度解，实现了物理一致性与计算效率的统一。与NTR-Gaussian（隐式热力学+数值积分）、4DGS（数据驱动变形场）等动态基线相比，ETGS在精度-效率帕累托前沿上占据显著优势。



### 热场景重建的现实需求与挑战

动态热场景的三维重建在工业检测、建筑热诊断、夜视增强等领域具有重要应用价值。与常规RGB图像不同，热红外图像记录的是场景的温度辐射信息，其像素强度直接反映物体的表面温度。因此，热场景重建的核心目标不仅是恢复三维几何结构，更要准确捕捉场景中随时间演化的温度场分布。

这一任务面临双重挑战。首先，热红外图像通常缺乏纹理细节，基于特征匹配的传统三维重建方法难以获得可靠的几何先验。其次，热过程本质上是动态的——物体在加热或冷却过程中温度持续变化，而现有方法要么将每个时间步作为独立静态场景处理，要么采用纯数据驱动的时间建模策略，未能有效利用热力学物理规律。

### 现有方法的两类缺口

**静态方法的根本局限。** 以**3DGS**（Kerbl et al., SIGGRAPH 2023）为代表的高斯散射方法在RGB新视角合成上取得了显著成功，并已被扩展至热成像领域（如**Thermal3D-GS**）。然而，这些静态方法假设场景属性不随时间变化，只能重建某一时刻的温度快照，无法描述加热、冷却等动态热过程。当场景温度随时间快速变化时，静态方法在不同时间步之间缺乏任何物理约束，导致重建结果在时间维度上不一致。

**动态方法的效率与精度困境。** 现有动态场景重建方法主要沿两条技术路线发展。一类以**4DGS**为代表，通过引入时间维度的变形场或外观嵌入来建模场景变化，但这类纯数据驱动方法缺乏对热力学过程的显式建模，难以准确捕捉温度演化的物理规律。另一类以**NTR-Gaussian**为代表，尝试将热传导方程融入神经表示，但依赖于隐式神经场和数值积分来求解物理方程。这种隐式-数值方案带来了三个突出问题：

1. **计算开销巨大**：每次前向传播需要执行数值积分，导致训练时间长达1469秒（约24.5分钟），渲染速度仅68 FPS，难以满足实时应用需求。
2. **误差累积**：数值积分的离散化误差在长序列中逐步累积，影响重建精度。
3. **时序灵活性差**：隐式时间编码通常假设均匀采样，难以处理非均匀或乱序的时间戳。

### 本文的核心动机

上述分析揭示了一个关键瓶颈：**现有动态重建方法要么完全忽略热力学过程，要么以高昂的计算代价和精度损失为代价来融入物理约束**。这引出了一个自然的问题：能否将热力学方程以显式、解析的方式直接嵌入高斯表示，从而在保持静态方法效率的同时实现物理一致的动态温度场重建？

本文的动机正是基于这一洞察。我们注意到，在合理的简化假设下（一阶热交换、谐波热源激发），热传导过程可以用一阶线性常微分方程描述，且该方程存在闭式解析解。这意味着，如果我们将热力学参数作为高斯基元的显式属性，并利用解析解直接计算任意时刻的温度，就可以完全绕过数值积分，实现物理驱动的高效动态重建。这一思路将热力学从“需要求解的约束”转变为“可直接计算的属性”，从根本上消除了隐式-数值方案的计算瓶颈。



## 核心方法与创新机理

ETGS 的核心创新在于**将热力学过程显式、可微地嵌入 3D 高斯散射表示**，使每个高斯基元不仅携带几何与外观属性，还具备物理可解释的热学参数和闭式温度演化能力。这一设计从根本上改变了动态热场景重建的范式，与现有方法的关键差异体现在以下三个 changed slots 上。

### 1. 从光学高斯到热高斯：属性空间的根本重构

标准 3DGS 的高斯基元定义为：

$$G_i = \{ \mu_i, \Sigma_i, R_i, \alpha_i, f_i \}$$

其中 $f_i$ 为球谐系数，用于编码视角相关的 RGB 颜色。ETGS 完全移除了光学颜色属性，代之以一组热力学参数：

$$\widetilde{G}_i = \{ \mu_i, \Sigma_i, R_i, \alpha_i, C_i, h_i, Q_i(t), T_i(t) \}$$

新增的四个属性分别对应**等效热容 $C_i$**、**换热系数 $h_i$**、**热源激发 $Q_i(t)$** 和**温度状态 $T_i(t)$**。这一属性重构使得每个高斯从“静态颜色载体”转变为“动态热源体”，为后续物理驱动的温度演化提供了参数基础。

### 2. 从隐式/数值驱动到显式闭式热力学演化

现有动态热重建方法（如 **NTR-Gaussian**）要么采用纯数据驱动的时间嵌入或变形场来模拟温度变化，要么依赖隐式神经表示辅以数值积分来融入物理方程，这带来了高昂的计算开销和误差累积风险。ETGS 直接基于能量守恒建立一阶线性常微分方程：

$$C_i \frac{d T_i(t)}{dt} = -h_i (T_i(t) - T_{env}) + Q_i(t)$$

该方程包含两个物理组件：**牛顿冷却项**描述高斯向环境温度 $T_{env}$ 的指数趋近，**热源激发项** $Q_i(t)$ 捕捉周期性或复杂的外部能量输入。$Q_i(t)$ 进一步展开为对数均匀频率网格上的傅里叶基：

$$Q_i(t) = \sum_{k=1}^{K} A_{i,k} \sin(\omega_k t) + B_{i,k} \cos(\omega_k t)$$

通过积分因子法与谐波展开，ETGS 推导出任意时刻 $t$ 的**闭式解析解**（完整推导见 Appendix A）：

$$T_i(t) = T_{env} + (T_{i,0} - T_{env}) e^{-t/\tau_i} + \sum_{k=1}^{K} \frac{\tau_i}{C_i (1+(\omega_k \tau_i)^2)} \{ A_{i,k}[\sin(\omega_k t) - \omega_k \tau_i \cos(\omega_k t) + \omega_k \tau_i e^{-t/\tau_i}] + B_{i,k}[\cos(\omega_k t) + \omega_k \tau_i \sin(\omega_k t) - e^{-t/\tau_i}] \}$$

其中 $\tau_i = C_i / h_i$ 为热时间常数。这一闭式解的关键优势在于：**完全避免了数值积分**，支持非均匀与乱序时间戳的直接计算，且整个表达式对 $C_i$、$h_i$、$A_{i,k}$、$B_{i,k}$ 完全可微，可以无缝嵌入反向传播训练流程。

### 3. 从纯图像损失到物理正则化约束

ETGS 在训练损失中引入了对谐波系数的正则化项：

$$\mathcal{L}_{total} = (1-\lambda) \mathcal{L}_1 + \lambda \mathcal{L}_{D-SSIM} + \lambda_{reg} \sum_{i,k} (A_{i,k}^2 + B_{i,k}^2)$$

这一设计针对热源激发项 $Q_i(t)$ 的过参数化风险：傅里叶基展开虽能灵活表示复杂激励，但缺乏约束时容易在长时间序列中产生非物理振荡。消融实验（Table 3）证实，移除正则项后 PSNR 从 44.73 dB 降至 42.58 dB，降幅约 2.15 dB，且视觉上出现明显的虚假温度波动（Figure 6 左）。正则项通过压制高频系数的幅度，在表达力与物理合理性之间取得平衡。

### 创新带来的因果效应

上述三个 changed slots 形成了从“表示—演化—约束”的完整因果链：热高斯属性为物理建模提供参数载体，闭式 ODE 解实现高效可微的温度演化，正则化损失确保优化过程的物理一致性。这一设计使得 ETGS 在 RHD 数据集 10 个场景上的平均 PSNR 达到 40.68 dB，较隐式热力学方法 NTR-Gaussian 的 34.96 dB 提升约 5.7 dB（Table 1），同时训练时间从 1469 秒缩减至 197 秒，渲染速度从 68 FPS 跃升至 458 FPS（Table 2）——在精度和效率两个维度均实现了数量级式的突破。

**需要人工验证的点**：论文未明确说明 $T_{env}$ 是全局共享超参数还是可学习变量，这一细节影响模型的物理自由度，建议核对原文 Section 3.2 的具体实现。



ETGS 的整体框架由四个顺序耦合的模块构成：**热高斯场构建** → **热力学演化模块** → **动态热渲染器** → **训练与优化**。其核心设计思想是将一阶热传导物理方程直接嵌入显式高斯表示，使每个高斯基元携带可学习的热力学参数，并通过闭式解析解在任意时刻高效计算温度，从而将动态热重建问题转化为一个端到端可微的优化过程。

### 模块关系与数据流

**1. 热高斯场构建。** 从多视角 RGB 图像出发，利用结构从运动（SfM）获取初始稀疏点云与相机位姿。每个点被扩展为一个热高斯 $\widetilde{G}_i$，其属性集为：

$$\widetilde{G}_i = \{ \mu_i, \Sigma_i, R_i, \alpha_i, C_i, h_i, Q_i(t), T_i(t) \}$$

相较于标准 3DGS 的高斯表示 $G_i = \{ \mu_i, \Sigma_i, R_i, \alpha_i, f_i \}$（包含球谐颜色 $f_i$），ETGS 移除了光学颜色属性，转而引入四个热力学参数：等效热容 $C_i$、换热系数 $h_i$、热源激发 $Q_i(t)$ 和温度状态 $T_i(t)$。$Q_i(t)$ 采用对数均匀频率网格上的傅里叶基展开，以捕捉周期性或复杂的外部能量输入。

**2. 热力学演化模块。** 每个热高斯的温度演化由基于能量守恒的一阶线性常微分方程描述：

$$C_i \frac{d T_i(t)}{dt} = -h_i (T_i(t) - T_{\text{env}}) + Q_i(t)$$

该方程由两项物理机制驱动：牛顿冷却项 $-h_i(T_i - T_{\text{env}})$ 描述高斯向环境温度 $T_{\text{env}}$ 的指数趋近过程；热源激发项 $Q_i(t)$ 建模外部能量的注入。利用积分因子法与谐波展开，该 ODE 可推导出任意时刻 $t$ 的闭式解析解（详见附录 A），完全避免了数值积分带来的计算开销与误差累积，同时支持非均匀和乱序时间戳的查询。

**3. 动态热渲染器。** 在给定时刻 $t$，将每个高斯的温度 $T_i(t)$ 线性映射为灰度强度 $I_i(t)$，再通过标准 $\alpha$ 合成沿视线累加：

$$C = \sum_{i=1}^{N} \text{Tr}_i \, \alpha_i \, I_i(t)$$

其中 $\text{Tr}_i$ 为累积透射率。生成的灰度热图像可进一步通过伪彩色映射进行可视化。由于渲染过程仅涉及前向代数运算，该模块在训练和推理阶段均保持与静态 3DGS 相近的效率。

**4. 训练与优化。** 总损失函数在标准 3DGS 损失基础上增加对谐波系数的正则项：

$$\mathcal{L}_{\text{total}} = (1-\lambda) \mathcal{L}_1 + \lambda \mathcal{L}_{\text{D-SSIM}} + \lambda_{\text{reg}} \sum_{i,k} (A_{i,k}^2 + B_{i,k}^2)$$

其中 $A_{i,k}$、$B_{i,k}$ 为热源激发 $Q_i(t)$ 的傅里叶系数。正则项抑制长时间序列中的非物理振荡，防止过拟合。优化过程采用与 3DGS 相同的高斯裁剪、致密化等策略，所有几何参数与热力学参数通过反向传播联合更新。

### 关键设计选择

整个框架的瓶颈突破点在于**闭式解析解替代数值积分**。现有动态热重建方法（如 NTR-Gaussian）依赖隐式神经表示与数值积分来融入物理方程，导致训练耗时（1469 秒）和渲染缓慢（68 FPS）。ETGS 通过选择一阶线性 ODE 这一可解析求解的物理模型，将温度计算退化为代数求值，使得训练时间降至 197 秒、渲染速度提升至 458 FPS，同时 PSNR 从 34.96 dB 提升至 40.68 dB。

值得注意的是，各高斯的温度演化在物理方程层面是独立建模的，但渲染后的热场通过高斯重叠与密集监督实现隐式耦合。这一设计牺牲了高斯间显式热传导的物理完备性，换取了极高的计算效率——这是当前框架的一个核心权衡。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. ETGS directly incorporates thermal physics modeling into the explicit Gaussian scene representation. The temperature of each Gaussian consists of two components: an exponential term*



### 3.1 热高斯场构建

ETGS 将 3DGS 的标准高斯表示从纯光学域扩展至热物理域。原始 3DGS 高斯定义为：

$$G_i = \{ \mu_i, \Sigma_i, R_i, \alpha_i, f_i \}$$

其中 $\mu_i$ 为中心位置，$\Sigma_i$ 为协方差矩阵，$R_i$ 为旋转，$\alpha_i$ 为不透明度，$f_i$ 为球谐颜色函数。ETGS 移除光学颜色属性，代之以四个热力学参数，构成**热高斯**（Thermal Gaussian）：

$$\widetilde{G}_i = \{ \mu_i, \Sigma_i, R_i, \alpha_i, C_i, h_i, Q_i(t), T_i(t) \}$$

新增属性的物理含义：
- **$C_i$**：等效热容（equivalent heat capacity），表征高斯元对热量的存储能力。
- **$h_i$**：换热系数（heat transfer coefficient），控制与环境的热交换速率。
- **$Q_i(t)$**：热源激发项（heat source excitation），描述外部能量输入的时间函数。
- **$T_i(t)$**：温度状态（temperature state），高斯元在时刻 $t$ 的当前温度。

这一扩展使每个高斯元从单纯的几何-外观基元转变为携带独立热力学演化能力的物理实体。

### 3.2 温度演化ODE与闭式解

温度演化由基于能量守恒的一阶线性常微分方程描述：

$$C_i \frac{d T_i(t)}{dt} = -h_i (T_i(t) - T_{env}) + Q_i(t)$$

该方程包含两个物理过程：右端第一项为牛顿冷却项，驱动温度向环境温度 $T_{env}$ 指数衰减；第二项为热源激发项，引入外部能量输入。定义时间常数 $\tau_i = C_i / h_i$，利用积分因子法可得解析解：

$$T_i(t) = T_{env} + (T_{i,0} - T_{env}) e^{-t/\tau_i} + \frac{1}{C_i} \int_0^t e^{-(t-s)/\tau_i} Q_i(s) ds$$

为使该解在任意时刻 $t$ 可高效计算且完全可微，ETGS 将 $Q_i(t)$ 展开为傅里叶基：

$$Q_i(t) = \sum_{k=1}^{K} A_{i,k} \sin(\omega_k t) + B_{i,k} \cos(\omega_k t)$$

其中 $\omega_k$ 为全局对数均匀频率网格，$A_{i,k}$、$B_{i,k}$ 为可学习的谐波系数。将此展开代入卷积积分并解析求解，得到最终的**闭式温度表达式**：

$$T_i(t) = T_{env} + (T_{i,0} - T_{env}) e^{-t/\tau_i} + \sum_{k=1}^{K} \frac{\tau_i}{C_i (1+(\omega_k \tau_i)^2)} \{ A_{i,k}[\sin(\omega_k t) - \omega_k \tau_i \cos(\omega_k t) + \omega_k \tau_i e^{-t/\tau_i}] + B_{i,k}[\cos(\omega_k t) + \omega_k \tau_i \sin(\omega_k t) - e^{-t/\tau_i}] \}$$

该闭式解是 ETGS 的核心技术瓶颈突破点：
- **完全可微**：所有运算（指数、三角函数、代数组合）均可解析求导，支持端到端反向传播。
- **无需数值积分**：避免了 NTR-Gaussian 等隐式方法中 ODE 求解器的计算开销与误差累积。
- **任意时刻查询**：支持非均匀、乱序时间戳的直接温度计算，无需时间步进。

### 3.3 动态热渲染器

获得各高斯元在时刻 $t$ 的温度 $T_i(t)$ 后，通过线性映射转换为灰度强度 $I_i(t)$，再沿视线进行 $\alpha$ 合成：

$$C = \sum_{i=1}^{N} Tr_i \alpha_i I_i(t)$$

其中 $Tr_i$ 为累积透射率。最终输出可保留为灰度热图像，或通过伪彩色映射实现可视化。

### 3.4 训练损失函数

ETGS 在标准 3DGS 损失基础上引入谐波系数正则项，总损失为：

$$\mathcal{L}_{total} = (1-\lambda) \mathcal{L}_1 + \lambda \mathcal{L}_{D-SSIM} + \lambda_{reg} \sum_{i,k} (A_{i,k}^2 + B_{i,k}^2)$$

正则项 $\sum_{i,k} (A_{i,k}^2 + B_{i,k}^2)$ 抑制谐波系数的过度增长，防止长时间序列中出现非物理振荡。消融实验证实：移除该正则项后 PSNR 从 44.73 dB 降至 42.58 dB（Table 3），验证了其必要性。

### 3.5 关键设计选择

- **一阶线性模型的选择**：ETGS 有意采用一阶线性热传导模型，因为该形式存在闭式解，可在保持物理一致性的同时实现高效训练与渲染。对于非线性或高阶热力学现象，当前框架无法直接描述，这构成其核心局限。
- **频率数 $K$ 的平衡**：消融实验表明，$K$ 从 8 增至 64 时性能改善迅速饱和，$K=24$ 在精度与计算开销间取得良好平衡，超过 32 后 PSNR 改善小于 0.2 dB（Table 4）。
- **高斯间耦合机制**：各高斯元的温度演化被独立建模，但渲染出的热场通过高斯重叠和密集监督隐式耦合，无需显式建模高斯间热传导即可捕捉场景级热分布。



## 实验与关键发现

### 核心定量结果与效率优势

ETGS 在自建的 Rapid Heat Dynamics (RHD) 数据集上进行了系统评估，与静态基线（3DGS、Mip-Splatting、Thermal3D-GS）和动态基线（4DGS、NTR-Gaussian）进行了全面对比。Table 1 汇总了 10 个场景的平均重建质量，ETGS 在所有指标上均取得最优结果：平均 PSNR 达到 **40.68 dB**，相比最强的动态对比方法 NTR-Gaussian（34.96 dB）提升约 **5.72 dB**；SSIM 达到 **0.989**，LPIPS 降至 **0.050**，均显著优于所有基线。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation of our method compared to previous work*

效率方面的优势更为突出。如 Table 2 所示，ETGS 的训练仅需 **197 秒**，而 NTR-Gaussian 需要 1469 秒，训练时间缩短约 7.5 倍；渲染速度达到 **458 FPS**，远超 NTR-Gaussian 的 68 FPS。这一效率优势的根源在于 ETGS 的闭式温度解完全避免了数值积分开销，使得训练与渲染效率接近静态 3DGS 水平，同时实现了物理一致的动态热场景重建。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/007_Table_2.jpg]]
*Table 2: Comparisons of training and rendering efficiency of our method with previous methods*

### 消融实验：热源激发项与正则化的关键作用

为验证各组件贡献，Table 3 报告了在典型场景上的消融结果。完整模型的 PSNR 为 44.73 dB。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/008_Table_3.jpg]]
*Table 3: Ablation Study. We remove the heat source excitation Q and the regularization term separately to evaluate their impact*

- **移除热源激发项 Q**（w/o Q）：PSNR 降至 43.70 dB，下降约 1.03 dB。如 Figure 6（右）所示，缺少热源激发项后模型无法充分捕捉外部能量输入驱动的温度变化，导致细节丢失和欠拟合，验证了谐波展开对复杂热源建模的必要性。
- **移除正则项**（w/o Regular）：PSNR 降至 42.58 dB，下降约 2.15 dB。Figure 6（左）显示，缺乏对谐波系数的约束会导致长时间序列中出现非物理的温度振荡，表明正则项在抑制过拟合和维持物理合理性方面不可或缺。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of the ablation study. Left: Ablation of the regularization term. Right: Ablation of the heat source excitation Q*

### 频率数 K 的敏感性分析

热源谐波展开的频率数 K 是控制模型表达能力与计算开销的关键超参数。Table 4 的消融显示，当 K 从 8 增加到 64 时，性能改善迅速饱和：K=24 在精度与计算开销之间取得良好平衡，超过 32 后 PSNR 改善小于 0.2 dB。这一结果表明，对数均匀频率网格能够以较少的基函数有效覆盖热场景的频域特征，过高的 K 值带来的边际收益有限。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/010_Table_4.jpg]]
*Table 4: Ablation Study. Effect of the number of frequencies K on reconstruction quality*

### 失败模式与局限性

尽管 ETGS 在 RHD 数据集上表现优异，分析揭示了若干结构性局限：

1. **高斯间热传导缺失**：各高斯的温度演化被独立建模，仅通过高斯重叠和密集监督隐式耦合，未显式建模高斯间的热传导过程。在存在强空间温度梯度的场景中，这一简化可能限制重建精度。
2. **几何固定假设**：当前方法假设场景几何固定，不能同时处理几何形变与温度变化，无法应对物体在加热/冷却过程中发生形变的场景。
3. **一阶线性 ODE 的表达力边界**：闭式解基于牛顿冷却定律与谐波热源的一阶线性组合，无法描述非线性或高阶热力学现象（如辐射主导传热、相变过程等）。
4. **数据覆盖有限**：RHD 数据集涵盖的场景和热过程仍有限，缺乏移动热源、更强环境扰动等更复杂情况，模型的泛化边界尚待进一步验证。

以上局限性的验证置信度中等（基于方法设计分析，非直接实验验证），建议在实际部署前针对目标场景进行专项评估。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/001_Figure_1.jpg]]
*Figure 1: Our method achieves high-quality rendering of dynamic thermal scenes with efficiency comparable to static methods (Kerbl et al. (2023); Yu et al. (2024)). The key to this performance is the novel explicit modeling of dynamic thermal Gaussians based on thermodynamics, which significantly speeds up scene optimization and synthesis of new views, while achieving state-of-the-art quality*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/003_Figure_3.jpg]]
*Figure 3: Pixel-aligned RGB-IR acquisition platform. (a) All devices are mounted on a rigid frame to ensure stability. (b) Response bands of the RGB and IR cameras: The RGB camera uses the IMX585 chip (response band 300-800nm), and the IR camera uses an uncooled vanadium oxide (VOx) microbolometer sensor (response band 8-14µm). (c) Optical principle of pixel-level alignment: A piece of coated glass (coating materials: zinc sulfide, silver) is mounted within the black frame. Visible light passes through the glass and enters the front RGB CMOS, while infrared light is reflected by the glass and reaches the side IR CMOS. The two imaging paths share the same incident light beam, which is split into diffe...*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/004_Figure_4.jpg]]
*Figure 4: Alignment Error Verification. (a) Average alignment error for each of the 20 RGB-IR image pairs. The overall average error is 0.4869 pixels, reaching sub-pixel accuracy. (b) Comparison of checkboard corner detection results. The RGB camera corners (blue circles) and the IR camera corners (red crosses) almost coincide*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/011_Table_5.jpg]]
*Table 5: Each scene of the Rapid Heat Dynamics Dataset*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_P2Nw2LMkjH/figures/013_Table_7.jpg]]
*Table 7: Complete calculation cost*



## 定位与知识库关联

### 1. 方法定位与谱系关系

ETGS 处于**动态场景重建**与**物理驱动神经渲染**的交汇点，其核心贡献在于将热力学过程的闭式解析解直接嵌入显式高斯表示，从而在保持静态 3DGS 效率的同时实现物理一致的动态热场景重建。理解其定位需要沿着两条谱系展开：高斯散射的演化路径，以及热重建的方法演进。

**高斯散射谱系**。3DGS（Kerbl et al., SIGGRAPH 2023）以显式高斯基元替代隐式神经表示，实现了实时辐射场渲染。后续工作沿两个方向拓展：**Mip-Splatting**（Yu et al., 2024）改进多尺度渲染质量，**4DGS** 引入变形场处理动态场景——但这些方法均面向光学外观，缺乏对物理过程的显式建模。ETGS 直接改造了高斯属性集：移除球谐颜色 $f_i$，引入等效热容 $C_i$、换热系数 $h_i$、热源激发 $Q_i(t)$ 和温度状态 $T_i(t)$，将高斯从“光学基元”转化为“热学基元”。这一属性槽位替换是方法的核心分叉点。

**热重建谱系**。**Thermal3D-GS** 将 3DGS 直接应用于静态热图像，仅将灰度强度替代 RGB 颜色，不涉及任何时间维度或物理约束。**NTR-Gaussian** 是动态热重建的直接基线：它采用隐式神经表示对温度场建模，并通过数值积分融入热传导方程。ETGS 相对于 NTR-Gaussian 的关键差异在于**物理融入方式**——后者依赖数值求解器，每次前向传播需执行离散时间步积分，导致训练耗时达 1469 秒、渲染仅 68 FPS；而 ETGS 利用一阶线性 ODE 的闭式解（Eq. 8），将温度计算退化为解析表达式求值，训练仅需 197 秒、渲染达 458 FPS。

### 2. 核心机制与因果瓶颈

ETGS 解决的真实瓶颈是：**现有动态热重建方法要么忽略物理过程（纯数据驱动），要么以隐式表示搭配数值积分融入物理方程，导致计算开销大、误差累积，且难以处理非均匀时序采样**。

因果旋钮在于**闭式可微温度演化**。具体而言，ETGS 将每个高斯的温度演化建模为一阶线性 ODE（牛顿冷却定律 + 谐波热源激发）：

$$C_i \frac{d T_i(t)}{dt} = -h_i (T_i(t) - T_{env}) + Q_i(t)$$

热源 $Q_i(t)$ 以傅里叶基展开：

$$Q_i(t) = \sum_{k=1}^{K} A_{i,k} \sin(\omega_k t) + B_{i,k} \cos(\omega_k t)$$

通过积分因子法与谐波展开，推导出任意时刻 $t$ 的闭式温度解（Eq. 8），完全避免数值积分。这一设计的深层洞察在于：**一阶线性 ODE 是少数具有闭式解的动力学系统，而牛顿冷却与谐波激励的组合恰好覆盖了热场景中最常见的指数衰减与周期性激励模式**。附录 A 给出了完整推导，确保物理一致性与可微性。

消融实验验证了这一设计选择的因果效力。移除热源激发项 $Q$ 后，PSNR 从 44.73 降至 43.70（Table 3），视觉上表现为细节丢失和欠拟合（Figure 6 右）；移除谐波系数正则项后，PSNR 进一步降至 42.58，长时间序列中出现非物理振荡（Figure 6 左）。频率数 $K$ 的消融（Table 4）表明，$K=24$ 在精度与计算开销间取得良好平衡——超过 32 后 PSNR 改善小于 0.2 dB，性能迅速饱和。

### 3. 适用边界与局限

ETGS 的设计假设划定了明确的适用边界：

- **独立热力学假设**。各高斯的温度演化被独立建模，仅通过高斯重叠和密集监督隐式耦合，未显式建模高斯间热传导。论文在 Discussion 中承认这一局限，指出渲染热场通过重叠高斯实现隐式耦合，但对于需要显式热流建模的场景可能不足。
- **固定几何假设**。当前方法假设场景几何固定，不能同时处理几何形变与温度变化。这意味着 ETGS 适用于刚体热场景（如工件加热、液体冷却），但无法处理伴随形变的热过程（如材料热膨胀变形）。
- **一阶线性限制**。闭式解基于一阶线性 ODE，无法准确描述非线性或高阶热力学现象（如辐射传热的四次方律、相变潜热）。论文明确指出，这一阶模型是“有意选择”的，因为其闭式解特性是效率的关键——对于需要更高阶物理的场景，需要权衡效率与精度。
- **数据集覆盖有限**。RHD 数据集覆盖的场景和热过程仍有限，缺乏移动热源、更强环境扰动、多材质复杂交互等更复杂情况。这限制了方法在极端场景下的泛化性验证。

### 4. 开放问题与未来方向

基于上述局限，论文和验证分析中浮现出以下开放问题：

1. **显式高斯间热传导**。如何在维持高效训练与渲染的前提下，引入高斯间热传导的显式建模？可能的路径包括基于空间邻近性的热流图网络，或通过渲染方程隐式耦合的增强方案。

2. **联合几何-热学重建**。如何将 ETGS 的闭式热力学框架与 4DGS 等动态几何建模方法结合，实现真正的动态几何+热学协同重建？这需要解决几何变形与温度演化之间的双向耦合问题。

3. **非线性热力学扩展**。能否将闭式框架推广至非线性或高阶传热方程？例如，对辐射项采用线性化近似，或引入分段线性化策略处理相变等强非线性过程。

4. **多模态协同重建**。当前 ETGS 仅输出热图像。能否将物理驱动的 RGB 渲染器与温度建模耦合，利用 RGB 信息辅助几何重建，同时用热信息约束材质参数，实现多模态协同？

5. **数据集增强**。构建包含移动热源、多材质复杂交互、强环境扰动等场景的 RHD 增强版本，以系统评估物理驱动方法的泛化边界。

### 5. 知识库定位总结

ETGS 在知识库中的定位可概括为：**将物理 ODE 的闭式解嵌入显式基元表示的开创性尝试**。它证明了在特定条件下（一阶线性动力学 + 谐波激励），物理一致性可以与静态方法的效率兼容。这一范式——将可解析求解的物理方程直接“烘焙”进场景表示——可能启发其他物理驱动重建任务（如流体可视化、声学场重建），前提是找到对应的闭式动力学模型。对于需要超越一阶线性的复杂场景，ETGS 提供了效率上界参考，但需要新的数值或近似方案来突破其适用边界。



## 原文 PDF

![[paperPDFs/ICLR_2026/ETGS_Explicit_Thermodynamics_Gaussian_Splatting_for_Dynamic_Thermal_Reconstructi_6090bdf94c7b.pdf]]

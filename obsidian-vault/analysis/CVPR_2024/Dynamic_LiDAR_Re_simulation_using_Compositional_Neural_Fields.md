---
title: "Dynamic LiDAR Re-simulation using Compositional Neural Fields"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Dynamic_LiDAR_Re_simulation_using_Compositional_Neural_Fields.pdf
project_link: https://shengyuh.github.io/dynfl/
aliases:
- DLRSUCNF
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "基于SDF的静态-动态分解神经场组合渲染与射线丢弃测试，通过在规范空间重建动态物体并独立渲染后融合，同时保持物理精确度。"
primary_logic: "将动态场景分解为静态背景和多个刚体动态物体，为每个物体构建独立神经场并利用二阶段组合渲染（相交检测、独立渲染、最近距离选择、射线丢弃融合），可以同时实现精确几何重建、动态场景重仿真及丰富的场景编辑操作。"
claims:
- "DyNFL在动态场景Waymo Dynamic上的MAE（30.8 cm）远优于LiDARsim（170.1 cm）和UniSim（35.6 cm），尤其动态车辆MedAE从14.3（UniSim）降至8.5 cm。"
- "组合神经场和射线丢弃测试使得动态车辆的ECDF曲线显著优于UniSim和LiDARsim。"
- "SDF-based表面重建在静态场景平面区域（如地面）表现出比NFL更清晰的几何，受益于SDF正则化。"
- "Waymo Dynamic 上 MAE (cm) = 30.8"
---

# Dynamic LiDAR Re-simulation using Compositional Neural Fields

> [!tip] 核心洞察
> 将动态场景分解为静态背景和多个刚体动态物体，为每个物体构建独立神经场并利用二阶段组合渲染（相交检测、独立渲染、最近距离选择、射线丢弃融合），可以同时实现精确几何重建、动态场景重仿真及丰富的场景编辑操作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于组合神经场的动态LiDAR重仿真 |
| 英文题名 | Dynamic LiDAR Re-simulation using Compositional Neural Fields |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.05247); [Project](https://shengyuh.github.io/dynfl); [Project](https://shengyuh.github.io/dynfl/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DyNFL |
| Dataset | Waymo Dynamic, TownClean (static), Waymo Dynamic NVS |

> [!tip] 效果简介
> - Waymo Dynamic 上，MAE (cm) 为 30.8，对比 35.6 (UniSim)，变化 -4.8。
> - TownClean (static) 上，MAE (cm) 为 26.7，对比 32.0 (NFL)，变化 -5.3。
> - Waymo Dynamic NVS 上，MAE (cm) 为 72.9，对比 115.1 (UniSim)，变化 -42.2。

## 概述

自动驾驶系统的安全验证依赖大规模、高保真的传感器仿真。LiDAR作为核心感知传感器，其重仿真（re-simulation）需同时满足两个要求：**物理精确性**——准确复现主动传感器的双向透射率、射线丢弃等物理特性；**场景编辑灵活性**——支持物体移除、插入与轨迹操控，以构建丰富的corner case。

现有方法在这两个目标之间存在根本性张力。静态神经场方法（如 **NFL**）虽能精确建模LiDAR物理，但局限于静态场景；动态方法（如 **UniSim**）通过联合采样渲染实现动态场景重建，却忽略了主动传感器的物理特性，导致保真度显著下降。这一瓶颈的核心在于：**缺乏一种既能保持逐物体几何精度、又能正确融合多物体渲染结果的组合机制**。

**DyNFL** 的核心洞察是：将动态驾驶场景显式分解为静态背景与多个刚体动态物体，为每个组件构建独立的、基于SDF的神经场，并通过二阶段组合渲染（射线相交检测→各场独立渲染→基于最近距离选择与射线丢弃测试的融合）来合成最终LiDAR扫描。这一设计同时解锁了三个能力：

- **物理精确的动态重仿真**：继承NFL的双向透射率与射线丢弃建模，并在多场融合中通过射线丢弃测试正确处理透明表面与遮挡。
- **高保真几何重建**：SDF驱动的体积渲染在平面区域（如地面）提供比密度场更强的表面正则化。
- **丰富的场景编辑**：物体的独立神经场使其可被移除、插入或改变轨迹，无需重新训练。

实验验证了上述设计的有效性。在Waymo Dynamic数据集上，DyNFL的MAE为30.8 cm，相比UniSim（35.6 cm）降低13.6%，动态车辆的MedAE从14.3 cm降至8.5 cm（降幅40.6%）。在静态场景TownClean上，DyNFL（26.7 cm）也优于物理精确的NFL（32.0 cm），证明SDF表示本身带来了精度增益。消融实验进一步确认：主动传感器渲染公式、表面SDF正则化、以及二阶段组合与射线丢弃模块各自贡献了显著的性能提升。

**方法定位**：DyNFL属于基于神经场的LiDAR重仿真方法，在技术谱系上位于静态物理精确方法（NFL）与动态神经仿真方法（UniSim）的交汇点——它保留了前者的物理精确性，同时获得了后者的动态编辑能力。其静态-动态分解与组合渲染策略为后续工作（如4D神经场、端到端分解）提供了可扩展的框架。

**局限与展望**：DyNFL依赖预先追踪的边界框，对框精度敏感；合成未见视角的移动车辆仍需学习先验来补全缺失信息；训练（7–16小时）与推理（每帧2–7秒）速度尚无法满足在线闭环仿真需求。这些方向——摆脱边界框依赖、扩展到4D表示、提升推理效率——构成了未来工作的关键挑战。

## 背景与动机

### 动态LiDAR重仿真的核心瓶颈

自动驾驶系统的安全验证高度依赖大规模、高保真的传感器仿真。LiDAR作为核心感知传感器，其物理精确的重仿真面临一个根本性矛盾：**现有神经场方法无法同时实现动态场景的高保真重建与灵活编辑**。

具体而言，两类主流方法各自存在结构性缺陷：

- **静态神经场方法**（如 **NFL**）通过建模双向透射率等物理传感器特性，实现了高保真的静态场景LiDAR重仿真，但其本质上是场景整体的单一表示，无法处理移动物体，更不具备场景编辑能力。
- **动态神经场方法**（如 **UniSim**）虽然支持动态场景，但在渲染过程中忽略了LiDAR的物理传感器特性——包括双向透射率（two-way transmittance）和射线丢弃（ray drop）机制，导致重建保真度显著下降，尤其在动态物体区域误差集中。

这种“物理精确”与“动态灵活”的互斥，构成了动态LiDAR重仿真的核心瓶颈。

### 现有方法的因果机制与失效模式

从因果角度看，上述瓶颈源于**场景表示粒度**与**传感器物理建模**之间的结构性冲突：

1. **单一场表示的限制**：静态方法将所有场景元素（地面、建筑、车辆）编码进同一个全局神经场，无法区分静态背景与动态前景，因而无法独立操控动态物体。
2. **物理建模的缺失**：动态方法为追求多物体渲染的便利，采用联合采样或混合渲染策略，但舍弃了LiDAR的主动传感器特性。具体表现为：
   - 忽略双向透射率，导致射线在穿过半透明或复杂几何时积累误差；
   - 缺少射线丢弃测试，使得被遮挡或超出有效测量范围的射线无法被正确过滤，在物体边界处产生伪影。

这些失效模式在动态车辆等移动前景上尤为突出——UniSim在Waymo Dynamic数据集上动态车辆的MedAE高达14.3 cm，而静态场景的误差相对可控。

### 本文动机与核心思路

本文的出发点是：**能否通过场景的静态-动态分解，结合物理精确的独立场渲染与组合策略，同时获得高保真度和编辑灵活性？**

核心洞察在于：将驾驶场景分解为一个静态背景场和多个刚体动态物体场，每个物体在规范空间中独立重建，然后通过一种考虑射线丢弃的二阶段组合渲染（相交检测 → 独立渲染 → 最近距离选择 → 射线丢弃融合），可以在保留双向透射率等物理建模的前提下，实现动态场景的重仿真和丰富的编辑操作（物体移除、插入、轨迹操控、新视角合成）。

这一思路的关键在于**解耦**——将“物理精确渲染”交给各个独立神经场，将“动态组合”交给后处理阶段的射线级融合策略，从而绕过了单一场表示的内在矛盾。

## 核心创新

DyNFL 的核心创新在于通过**组合神经场（Compositional Neural Fields）** 与**射线丢弃测试（Ray Drop Test）** ，首次在动态场景 LiDAR 重仿真中同时实现了高保真度与灵活的场景编辑能力。其关键突破可归纳为三个相互耦合的“changed slots”：

### 1. 静态-动态解耦的场景表示

现有神经场方法要么局限于静态场景（如 **NFL**），要么采用单一全局场表示动态场景（如 **UniSim**），难以兼顾重建精度与编辑灵活性。DyNFL 利用驾驶场景的刚体运动先验，将场景显式分解为**一个静态背景场**和**N 个动态物体场**（Section 3.1）。每个动态车辆通过边界框跟踪信息变换到各自的规范空间（canonical space）中独立重建，这使得 DyNFL 天然支持物体移除、插入和轨迹编辑等操作，而无需重新训练整个场景。

### 2. SDF 驱动的主动传感器体积渲染

传统 LiDAR 神经渲染方法（如 NFL）采用密度 $\sigma$ 驱动的体积渲染，而 DyNFL 转向**符号距离函数（SDF）驱动的体积渲染**，通过 Sigmoid 函数从 SDF 推导不透明度：

$$\tilde{\sigma}_{\zeta_i} = \max\left(\frac{-\frac{d\Phi_s}{d\zeta_i}(f(\zeta_i))}{\Phi_s(f(\zeta_i))}, 0\right)$$

$$\tilde{\alpha}_{\zeta_j} = \max\left(\frac{\Phi_s(f(\zeta_j))^2 - \Phi_s(f(\zeta_{j+1}))^2}{2\Phi_s(f(\zeta_j))^2}, 0\right)$$

这一改变带来了双重收益：SDF 的正则化特性使得平面区域（如地面）的几何重建更加清晰（Figure 4），同时保留了 NFL 对 LiDAR 物理特性的精确建模——包括**双向透射率**（two-way transmittance）和**射线丢弃概率**（ray drop probability），这是 UniSim 等动态方法所忽略的关键物理约束。

### 3. 二阶段多场组合渲染与射线丢弃融合

这是 DyNFL 最关键的机制创新。与 UniSim 将多个场的采样点混合后联合渲染不同，DyNFL 采用**二阶段组合策略**（Section 4.4）：

1. **相交检测**：对每条射线，先识别可能与哪些动态物体的边界框相交；
2. **独立渲染 + 最近距离选择**：在每个相交的场中独立进行体积渲染，然后按估计距离排序，选择最近的有效测量作为最终输出；
3. **射线丢弃融合**：当所有场的射线丢弃概率 $p_d > 0.5$ 时，判定该射线被丢弃，从而正确处理透明表面和遮挡关系。

这一设计使得动态车辆的几何重建质量显著提升——在 Waymo Dynamic 数据集上，动态车辆的中位绝对误差（MedAE）从 UniSim 的 14.3 cm 降至 **8.5 cm**（Table 1），ECDF 曲线也显示出对 LiDARsim 和 UniSim 的明显优势（Figure 3）。消融实验进一步证实，射线丢弃模块是动态车辆误差减半的关键因素（Section 6.3, Figure 5）。

### 创新总结

上述三个 changed slots 形成了完整的因果链：**场景分解**提供了编辑灵活性的基础，**SDF 渲染**保证了静态几何的物理精确度，而**二阶段组合渲染**则解决了多场融合时的遮挡与保真度难题。这一组合使得 DyNFL 在动态场景重仿真中首次同时超越了静态物理仿真方法（NFL）和动态神经仿真方法（UniSim），并解锁了物体级场景编辑能力。

## 整体框架

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/001_Figure_1.jpg]]
*Figure 1: Overview of DyNFL. Our method takes LiDAR scans and tracked bounding boxes of dynamic vehicles as input. DyNFL first decomposes the scene into a static background and N dynamic vehicles, each modelled using a dedicated neural field. These neural fields are then composed to re-simulate LiDAR scans in dynamic scenes. Our composition technique supports various scene edits, including altering object trajectories, removing and adding reconstructed neural assets between scenes*

DyNFL 的核心思想是将动态驾驶场景分解为一个静态背景和 N 个刚性运动的动态物体，并为每一部分构建独立的神经场，最后通过组合渲染实现高保真 LiDAR 重仿真。图 1 展示了这一整体流程。

**输入与场景分解。** 方法以 T 帧自车运动补偿后的 LiDAR 扫描 $\mathcal{X} = \{ \mathbf{X}_t \}_{t=1}^T$ 和 N 个动态车辆的追踪边界框 $\boldsymbol{B} = \{ \mathbf{B}_t^v \}_{v=1}^N$ 作为输入。每条 LiDAR 射线被表示为五元组 $(\mathbf{o}, \mathbf{d}, \zeta, e, p_d)$，分别对应射线原点、方向、距离、强度和射线丢弃指示。利用驾驶场景可分解为静态背景与刚性运动组件的归纳偏置，系统建立 N+1 个神经场：一个静态背景场 $F_{\text{static}}$ 和 N 个动态物体场 $F^v$。动态车辆通过边界框间的相对变换对齐到规范坐标系，使得同一物体在不同帧的观测可在统一空间中累积重建。

**神经场编码与预测。** 每个神经场均采用多分辨率哈希编码（MHE）与多层感知机（MLP）的组合架构。位置编码后的特征经几何 MLP $f_s$ 预测符号距离 $s$ 和几何特征 $f_{\text{geo}}$，射线方向特征经强度 MLP $f_e$ 预测强度 $e$，经射线丢弃 MLP $f_{\text{drop}}$ 预测射线丢弃概率 $p_d \in [0,1]$。这一设计可形式化为：
$$(s, f_{\text{geo}}) = f_s(f_{\text{pos}}), \quad e = f_e(f_{\text{ray}}), \quad p_d = f_{\text{drop}}(f_{\text{ray}})$$

**SDF 驱动的主动传感器体积渲染。** 与传统密度驱动的体积渲染不同，DyNFL 从符号距离函数导出不透明度。连续不透明度 $\tilde{\sigma}_{\zeta_i}$ 由 SDF 的 Sigmoid 函数 $\Phi_s$ 推导：
$$\tilde{\sigma}_{\zeta_i} = \max\left(\frac{-\frac{d\Phi_s}{d\zeta_i}(f(\zeta_i))}{\Phi_s(f(\zeta_i))}, 0\right)$$
进而得到离散不透明度 $\tilde{\alpha}_{\zeta_j}$，并以此计算主动传感器的辐射功率 $P$ 和深度渲染权重 $\tilde{w}_j$：
$$P = \sum_{j=1}^{N} \mathcal{T}_{\zeta_j}^2 \tilde{\alpha}_{\zeta_j} \rho_{\zeta_j}', \quad \tilde{w}_j = 2\tilde{\alpha}_{\zeta_j} \cdot \prod_{i=1}^{j-1} (1 - 2\tilde{\alpha}_{\zeta_i})$$
其中 $\mathcal{T}_{\zeta_j}^2$ 为双向透射率，继承了 NFL 的物理精确建模。

**二阶段多场组合渲染。** 这是 DyNFL 区别于 UniSim 等联合采样方法的关键模块。第一阶段进行射线相交测试，识别与当前射线可能相交的 k 个动态场；第二阶段对各场独立执行体积渲染，得到 k+1 组 LiDAR 测量结果，然后按估计距离升序排列，选择最近距离作为最终预测。同时，射线丢弃测试判定：若所有神经场均指示丢弃概率 $p_d > 0.5$，则该射线被标记为丢弃。这一策略有效处理了多场间的遮挡与透明表面问题，是动态车辆 MedAE 减半的核心原因。

**损失优化。** 训练采用加权多任务损失：
$$\mathcal{L} = w_{\zeta} \mathcal{L}_{\zeta} + w_{s} \mathcal{L}_{s} + w_{\mathrm{eik}} \mathcal{L}_{\mathrm{eik}} + w_{e} \mathcal{L}_{e} + w_{\mathrm{drop}} \mathcal{L}_{\mathrm{drop}}$$
其中 $\mathcal{L}_{\zeta}$ 为距离 L1 损失，$\mathcal{L}_{s}$ 强制表面点 SDF 值趋近于零以改善平面区域几何，$\mathcal{L}_{\mathrm{eik}}$ 为 Eikonal 正则项，$\mathcal{L}_{e}$ 为强度 L2 损失，$\mathcal{L}_{\mathrm{drop}}$ 结合二元交叉熵与 Lovász 损失监督射线丢弃。这一组合损失同时约束了几何精度、物理一致性和感知质量。

## 核心模块与公式推导

### 场景分解与规范空间对齐

DyNFL 的核心前提是将动态驾驶场景分解为一个静态背景场与 N 个刚体动态物体场。给定 T 帧自运动补偿后的 LiDAR 扫描 $\mathcal{X} = \{ \mathbf{X}_t \}_{t=1}^T$ 及对应的 N 个车辆追踪边界框 $\boldsymbol{B} = \{ \mathbf{B}_t^v \}_{v=1}^N$，系统为静态背景建立神经场 $F_{static}$，为每个动态车辆建立独立的 $F^v$。

动态物体的规范空间对齐通过边界框间的相对刚体变换 $\{T_t \in SE(3)\}_{t=2}^T$ 实现：所有时刻的测量被变换并累积到该物体的规范坐标系中，使得单个物体在不同帧的观测可以被同一神经场统一学习。这一分解策略直接决定了后续组合渲染的可行性与编辑灵活性。

### 神经场编码与预测

每个神经场采用多分辨率哈希编码（MHE）对输入坐标进行编码，随后通过三个 MLP 分支分别预测：

$$(s, f_{geo}) = f_s(f_{pos}), \quad e = f_e(f_{ray}), \quad p_d = f_{drop}(f_{ray})$$

其中 $s$ 为符号距离函数（SDF）值，$e$ 为强度，$p_d \in [0,1]$ 为射线丢弃概率。$f_{pos}$ 和 $f_{ray}$ 分别为位置编码和方向编码特征。SDF 的引入替代了传统密度场 $\sigma$，为后续物理精确的体积渲染提供了更规整的表面表示。

### SDF 驱动的 LiDAR 体积渲染

与被动传感器（如相机）不同，LiDAR 的主动传感特性要求建模双向透射率。DyNFL 继承 NFL 的物理模型，将 LiDAR 辐射功率 $P$ 表示为脉冲功率 $P_e(t)$ 与脉冲响应 $H$ 的卷积：

$$P(\zeta) = \int_0^{2\zeta/c} P_e(t) H(\zeta - \frac{ct}{2}) dt$$

其中脉冲响应由目标分量 $H_T$ 和传感器分量 $H_s$ 组成：

$$H_T(\zeta) = \frac{\rho}{\pi} \cos(\theta) \delta(\zeta - \bar{\zeta}), \quad H_s(\zeta) = T^2(\zeta) \frac{A_e}{\zeta^2}$$

为将 SDF 表示与体积渲染结合，DyNFL 从 SDF 值 $f(\zeta)$ 推导连续不透明度 $\tilde{\sigma}$：

$$\tilde{\sigma}_{\zeta_i} = \max\left(\frac{-\frac{d\Phi_s}{d\zeta_i}(f(\zeta_i))}{\Phi_s(f(\zeta_i))}, 0\right)$$

其中 $\Phi_s$ 为 Sigmoid 函数。基于此，离散不透明度 $\tilde{\alpha}$ 定义为：

$$\tilde{\alpha}_{\zeta_j} = \max\left(\frac{\Phi_s(f(\zeta_j))^2 - \Phi_s(f(\zeta_{j+1}))^2}{2\Phi_s(f(\zeta_j))^2}, 0\right)$$

最终的辐射功率离散体积渲染公式为：

$$P = \sum_{j=1}^{N} \mathcal{T}_{\zeta_j}^2 \tilde{\alpha}_{\zeta_j} \rho_{\zeta_j}', \quad \tilde{w}_j = 2\tilde{\alpha}_{\zeta_j} \cdot \prod_{i=1}^{j-1} (1 - 2\tilde{\alpha}_{\zeta_i})$$

深度估计通过加权求和得到：

$$\zeta = \sum_{n=1}^{N} 2 \cdot \mathcal{T}_{\zeta_n}^2 \cdot \tilde{\alpha}_{\zeta_n} \cdot \zeta_n = \sum_{n=1}^{N} w_n \cdot \zeta_n$$

### 二阶段多场组合渲染

这是 DyNFL 区别于 UniSim 等混合采样方法的核心创新。组合渲染分为两个阶段：

**第一阶段：射线相交测试。** 对每条射线 $\mathbf{r} = (\mathbf{o}, \mathbf{d}, \zeta, e, p_d)$，检测其与 N 个动态物体边界框的相交情况，筛选出 $k \geq 0$ 个可能相交的动态场。

**第二阶段：独立渲染与融合。** 对 $k+1$ 个场（静态场 + k 个动态场）分别执行完整的 SDF 驱动体积渲染，得到各自的距离估计。随后按距离升序排列，选择最近的距离作为最终预测。射线丢弃判定采用投票机制：当所有场的 $p_d > 0.5$ 时，该射线被标记为丢弃。这一策略有效处理了透明表面和遮挡关系，避免了 UniSim 联合采样导致的几何模糊。

### 损失函数

总损失为五项加权组合：

$$\mathcal{L} = w_{\zeta} \mathcal{L}_{\zeta} + w_{s} \mathcal{L}_{s} + w_{\mathrm{eik}} \mathcal{L}_{\mathrm{eik}} + w_{e} \mathcal{L}_{e} + w_{\mathrm{drop}} \mathcal{L}_{\mathrm{drop}}$$

各分量含义如下：
- **范围损失** $\mathcal{L}_{\zeta} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r} \in \mathcal{R}} |\zeta_{est} - \zeta_{gt}|$：L1 距离监督。
- **表面 SDF 正则** $\mathcal{L}_{s} = \frac{1}{|\mathcal{P}|} \sum_{\mathbf{p} \in \mathcal{P}} |s(\mathbf{p})|$：强制表面点 SDF 值趋近于零，改善平面区域重建。
- **Eikonal 损失** $\mathcal{L}_{\mathrm{eik}}$：标准 SDF 梯度约束。
- **强度损失** $\mathcal{L}_{e}$：L2 强度监督。
- **射线丢弃损失** $\mathcal{L}_{\mathrm{drop}} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r} \in \mathcal{R}} \left( \mathcal{L}_{bce}(p_{d,est}, p_{d,gt}) + \mathcal{L}_{ls}(p_{d,est}, p_{d,gt}) \right)$：结合二元交叉熵与 Lovasz 损失，处理类别不平衡。

## 实验与分析

### 核心定量结果

DyNFL 在动态与静态场景的 LiDAR 新视角合成（NVS）任务上均取得了显著优于现有方法的性能。在 Waymo Dynamic 数据集上，DyNFL 的 MAE 达到 **30.8 cm**，相比 LiDARsim（170.1 cm）和 UniSim（35.6 cm）分别降低了 139.3 cm 和 4.8 cm（Table 1）。针对动态车辆的误差尤为突出：MedAE 从 UniSim 的 14.3 cm 降至 **8.5 cm**，降幅超过 40%。ECDF 曲线（Figure 3）进一步验证了这一优势——DyNFL 在所有点云和动态车辆点云上的误差分布均显著优于 LiDARsim 和 UniSim，表明组合神经场与射线丢弃测试对动态物体重建的关键作用。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/003_Table_1.jpg]]
*Table 1: Evaluation of LiDAR NVS on Waymo Dynamic dataset*

在静态场景上，DyNFL 同样展现出竞争力。TownClean 数据集上 MAE 为 **26.7 cm**，优于物理精确的 NFL（32.0 cm）达 5.3 cm（Table 2）。这一提升归因于 SDF-based 表面建模带来的增强正则化效果，尤其在平面区域（如地面）重建更为清晰（Figure 4）。Waymo Dynamic NVS 任务上，DyNFL 的 MAE 为 **72.9 cm**，相比 UniSim（115.1 cm）降低 42.2 cm（Table 7），证明其在视角大幅变化时的鲁棒性。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/004_Table_2.jpg]]
*Table 2: Evaluation of LiDAR NVS on static scenes*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/019_Table_7.jpg]]
*Table 7: Evaluation of LiDAR NVS on Waymo Dynamic NVS*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results of range estimation. Regions with gross errors (-100 100 cm) are highlighted*

### 下游任务验证

为评估重仿真点云的实际可用性，论文在 Waymo Dynamic 数据集上进行了目标检测和语义分割实验。目标检测结果（Table 5）显示，DyNFL 生成的点云在与真实扫描的检测一致性上优于 UniSim 和 LiDARsim，动态车辆检测的 Agg. Dyn. 指标提升明显。语义分割实验（Table 6）中，DyNFL 在静态类别 IoU 达到 81.1，动态类别 IoU 高达 97.3，表明重仿真的点云不仅几何准确，语义信息也高度保真。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/007_Table_5.jpg]]
*Table 5: Object detection results on Waymo Dyanmic datasets*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/008_Table_6.jpg]]
*Table 6: Semantic segmentation results on Waymo NVS dataset*

### 消融研究

消融实验揭示了 DyNFL 三个核心设计的作用：

1. **主动传感器体积渲染**（Table 3）：将 SDF-based 体积渲染从被动传感器模式切换为主动传感器模式（即建模双向透射率 $\mathcal{T}^2$），在 TownClean 上 MAE 降低 **1.5 cm**，验证了物理精确的 LiDAR 测量模型对性能的贡献。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/009_Table_3.jpg]]
*Table 3: Ablation study of volume rendering for active sensing*

2. **表面点 SDF 正则化**（Table 4）：在 TownReal 数据集上，显式约束 LiDAR 表面点处 SDF 值趋近于零，使 MAE 降低 **3.3 cm**，改善了平面区域的几何重建质量。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/010_Table_4.jpg]]
*Table 4: Ablation study of the surface points’ SDF regularisation*

3. **二阶段组合渲染与射线丢弃模块**（Section 6.3, Figure 5）：与 UniSim 的联合采样混合渲染相比，DyNFL 的独立渲染后按最近距离选择并融合射线丢弃测试的策略，使动态车辆的 MedAE **减半**。Figure 5 定性展示了射线丢弃模块有效处理了多场间的遮挡与透明表面问题。

### 场景编辑与新视角合成

DyNFL 的组合神经场表示支持丰富的场景编辑操作。Figure 8 展示了物体移除与插入效果——DyNFL 将重建的神经资产（卡车）无缝插入新场景，而 UniSim 则出现明显的几何建模失败。Figure 9 验证了轨迹操控的逼真度：操控后的卡车可被检测器成功识别。Figure 7 展示了传感器参数变化（仰角、位置、线束数）下的新视角合成，点云强度分布合理，证明了方法的泛化能力。

### 失败模式与局限性

DyNFL 在合成未见视角的移动车辆时存在困难，需要学习先验来补全缺失的强度与射线丢弃模式信息。方法依赖预先追踪的边界框和轨迹，当边界框不精确时性能会下降。训练时间约 7–16 小时，推理每帧约 2–7 秒，无法满足实时应用需求。场景编辑能力仅限于刚体运动假设，无法处理非刚性变形。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/022_Figure_13.jpg]]
*Figure 13: Visualization of scene editing capabilities. We showcase 3 kinds of scene editing capabilities including vehicle removal(left), trajectory manipulation(middle) and vehicle insertion(right). The first row represents the original scenes, the second row demonstrates the scenes after editing. All points are color-coded by the intensity values(0 0.25)*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/018_Table.jpg]]

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2312_05247/figures/020_Table_8.jpg]]
*Table 8: Results of future frame simulation*

## 方法谱系与知识库定位

### 1. 核心定位：动态场景的物理精确 LiDAR 神经重仿真

DyNFL 处于**神经场景表示**、**LiDAR 仿真**与**动态场景建模**三者的交汇点。其核心贡献在于首次将物理精确的主动传感器体积渲染（继承自 NFL）与组合式神经场架构相结合，解决了现有方法在“高保真度”与“灵活编辑”之间无法兼得的瓶颈。

具体而言，此前的神经 LiDAR 仿真方法分为两个阵营：
- **静态物理精确方法**：以 **NFL** 为代表，通过建模双向透射率（two-way transmittance）和射线丢弃（ray drop）实现了物理上正确的 LiDAR 渲染，但场景表示局限于静态，无法处理运动物体。
- **动态方法**：以 **UniSim** 为代表，支持动态场景和场景编辑，但其渲染管线忽略了主动传感器的物理特性（如双向透射率），导致几何精度下降。

DyNFL 通过**静态-动态分解的组合神经场**（一个静态背景场 + N 个规范空间中的动态物体场）填补了这一空白。其关键创新在于**二阶段组合渲染策略**：首先进行射线与各物体包围盒的相交测试，然后在各场中独立执行完整的物理精确体积渲染，最后通过射线丢弃测试和最近距离选择进行融合。这使得 DyNFL 在保持 NFL 级别物理精确度的同时，获得了 UniSim 级别的场景编辑灵活性。

### 2. 与基线方法的关系

| 方法 | 与 DyNFL 的关系 | 关键差异 |
|------|----------------|---------|
| **NFL** | 物理渲染基础的直接继承者 | DyNFL 将 NFL 的静态 SDF 体积渲染扩展到多场组合，并引入 SDF 正则化改善平面区域重建 |
| **UniSim** | 动态场景建模的对比基线 | UniSim 采用联合采样混合渲染，忽略双向透射率；DyNFL 采用独立渲染后融合，保留物理精确度 |
| **LiDARsim** | 传统动态 LiDAR 仿真基线 | 基于显式几何重建，非神经场方法，动态车辆重建质量显著劣于 DyNFL（MAE 170.1 cm vs 30.8 cm） |
| **i-NGP / DS-NeRF / URF** | 静态场景神经渲染基线 | 均为被动传感器渲染方法，未建模主动 LiDAR 的物理特性 |

**决定性证据**：在 Waymo Dynamic 数据集上，DyNFL 的 MAE（30.8 cm）显著优于 LiDARsim（170.1 cm）和 UniSim（35.6 cm），尤其在动态车辆上的 MedAE 从 UniSim 的 14.3 cm 降至 8.5 cm（Table 1）。ECDF 曲线（Figure 3）进一步证实组合渲染在动态车辆点上的分布优势。

### 3. 适用边界

**强适用场景**：
- 以刚体运动为主的自动驾驶动态场景（车辆、骑行者等）
- 需要物理精确传感器建模的下游任务（如目标检测、语义分割的闭环评估）
- 需要场景编辑能力的仿真应用（物体移除、插入、轨迹操控）

**弱适用场景**：
- 非刚体变形物体（行人姿态变化、植被摆动等）
- 实时或在线仿真（训练 7~16 小时，推理每帧 2~7 秒）
- 完全无监督的前背景分割（依赖预先追踪的边界框）

### 4. 局限与开放问题

**已确认局限**：
1. **未见视角合成困难**：DyNFL 在合成移动车辆的未见视角时存在困难，需要学习先验来补全缺失的强度、射线丢弃模式等信息。
2. **边界框依赖**：方法依赖预先追踪的边界框和轨迹作为输入，当边界框不精确时性能会下降。这是组合式方法的固有假设——场景分解的质量直接影响渲染精度。
3. **计算开销**：训练时间约 7~16 小时，推理每帧约 2~7 秒，无法满足实时应用需求。
4. **刚体运动假设**：场景编辑能力仅限于刚体运动，无法处理非刚性变形。

**开放问题**：
1. **端到端分解**：能否摆脱对边界框和轨迹的依赖，实现端到端的前背景分割与动态物体重仿真？这将显著降低数据标注成本。
2. **4D 时空表示**：如何将表示扩展到 4D 空间-时间神经场，同时保留场景编辑的灵活性？这是平衡“重建精度”与“编辑自由度”的核心挑战。
3. **跨实例泛化**：如何在不重新训练的情况下，泛化到未见过的物体形状和类别？当前各动态物体需要独立训练。
4. **在线闭环仿真**：能否通过模型压缩或高效推理方案，将 DyNFL 应用于在线闭环仿真？这需要将推理速度提升数个数量级。

## 原文 PDF

![[paperPDFs/CVPR_2024/Dynamic_LiDAR_Re_simulation_using_Compositional_Neural_Fields.pdf]]

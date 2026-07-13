---
title: "RF4D:Neural Radar Fields for Novel View Synthesis in Outdoor Dynamic Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RF4D_Neural_Radar_Fields_for_Novel_View_Synthesis_in_Outdoor_Dynamic_Scenes.pdf
project_link: "https://zhan0618.github.io/RF4D"
code_link: null
aliases:
- RF4D
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过引入时间维度（时空神经场）和场景流模块对动态物体运动进行建模，同时设计物理一致的雷达功率渲染公式（占位乘以RCS对数）来消除矛盾。
primary_logic: 将动态场景表示为位置与时间的连续函数，通过预测运动偏移量实现时间一致性，并利用雷达物理的先验知识设计功率渲染过程，使占位与反射率正相关，从而无需外部占位监督。
claims:
- RF4D通过场景流模块预测运动偏移量，实现相邻帧占用一致性，成功渲染了动态车辆，而Radar Fields无法恢复。
- RF4D的雷达特定功率渲染公式将占用作为一个软门控，确保高占用对应强RCS，解决了Radar Fields中的占用-反射矛盾。
- 在RobotCar数据集的多个场景中，RF4D在SSIM、CD等指标上显著优于现有方法，例如Scene 1 SSIM从0.3372提升至0.6103，Scene 3 CD从9.5357降至3.2896。
- Oxford RobotCar (Scene 1) 上 SSIM ↑ = 0.6103
---

# RF4D:Neural Radar Fields for Novel View Synthesis in Outdoor Dynamic Scenes

> [!tip] 核心洞察
> 将动态场景表示为位置与时间的连续函数，通过预测运动偏移量实现时间一致性，并利用雷达物理的先验知识设计功率渲染过程，使占位与反射率正相关，从而无需外部占位监督。

| 字段 | 内容 |
|------|------|
| 中文题名 | RF4D：面向室外动态场景新视角合成的神经雷达场 |
| 英文题名 | RF4D:Neural Radar Fields for Novel View Synthesis in Outdoor Dynamic Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_RF4DNeural_Radar_Fields_for_Novel_View_Synthesis_in_Outdoor_Dynamic_CVPR_2026_paper.html) · [Project](https://zhan0618.github.io/RF4D) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | RF4D |
| Dataset | Oxford RobotCar, Boreas |

> [!tip] 效果简介
> - Oxford RobotCar (Scene 1) 上，SSIM ↑ 0.6103 vs 0.3372 (RadarFields) (+0.2731)。
> - Oxford RobotCar (Scene 3) 上，CD ↓ 3.2896 vs 9.5357 (RadarFields) (-6.2461)。
> - Boreas (Sun) 上，SSIM ↑ 0.7001 vs 0.3641 (RadarFields) (+0.3360)。

## 概要

**RF4D** 是首个利用神经场从雷达测量中建模室外动态场景的方法，发表于 CVPR 2026。其核心动机源于现有雷达神经场方法（如 **Radar Fields**）的两大瓶颈：其一，仅能处理静态场景，无法恢复动态物体（如行驶车辆）；其二，预测的占位（occupancy）与反射率之间存在物理矛盾——高占位区域对应低反射率，导致动态目标消失或重建质量退化。

RF4D 的关键洞察是将动态场景表示为位置与时间的连续函数，并引入雷达物理先验来消除上述矛盾。具体而言，方法在三个维度上实现了突破：

1. **时空神经场与场景流建模**：通过显式输入时间戳 $t$ 学习时空神经场，并引入场景流模块预测运动偏移量，使相邻帧的占位预测保持时间一致性，从而成功渲染动态物体。
2. **物理一致的功率渲染**：设计雷达特定的功率渲染公式 $\hat{P}_{r} = \alpha \cdot \log_{10}(\sigma / \delta^{2})$，将占位 $\alpha$ 作为软门控与雷达截面积（RCS）$\sigma$ 耦合，确保高占位必然对应强 RCS，从根本上解决了占位-反射矛盾。
3. **无需外部占位监督**：仅通过雷达功率重建损失和内部正则化即可学习占位，摆脱了对 LiDAR 等外部占位估计器的依赖。

实验表明，RF4D 在 Oxford RobotCar 和 Boreas 两个数据集上均显著优于现有方法。在动态场景中，RF4D 成功渲染了 Radar Fields 无法恢复的移动车辆；定量指标上，Scene 1 的 SSIM 从 0.3372 提升至 0.6103，Scene 3 的 Chamfer Distance 从 9.5357 降至 3.2896。消融实验进一步验证了时间一致性正则化和运动偏移正则化对稳定训练和动态场景合成至关重要。



### 雷达感知的核心优势与挑战

在自动驾驶和移动机器人领域，鲁棒的环境感知是实现安全导航的基础。当前主流感知方案高度依赖相机与激光雷达（LiDAR），然而这些光学传感器在恶劣天气（如雨、雪、雾）和低光照条件下性能严重退化。毫米波雷达因其长波长特性，能够穿透雨雪尘埃，且不受环境光照影响，成为全天候感知的关键补充模态。Figure 5 直观展示了这一优势：在暴雪场景中，LiDAR 点云严重退化，而雷达测量保持稳定。

然而，雷达数据本身存在固有限制：其空间分辨率远低于相机和 LiDAR，且测量值（接收功率）与场景物理属性之间的映射关系复杂。如何从稀疏、低分辨率的雷达测量中恢复出稠密的场景几何与外观信息，是雷达感知领域的核心难题。

### 现有方法的两大瓶颈

**瓶颈一：局限于静态场景。** 以 **Radar Fields** 为代表的神经雷达场方法，首次将神经辐射场（NeRF）的隐式场景表示引入雷达领域，实现了从 2D 雷达扫描到 3D 场景的几何重建与新视角合成。然而，Radar Fields 将场景建模为纯静态的三维函数，完全忽略了时间维度。在包含移动车辆、行人等动态目标的真实室外场景中，该方法无法对运动物体进行建模，导致动态目标在渲染结果中消失或产生严重伪影（Figure 1）。

**瓶颈二：占用-反射率物理不一致。** Radar Fields 采用与 NeRF 类似的解耦策略，分别预测占用（occupancy）和反射率（reflectance），并将两者相乘作为渲染权重。这一设计在雷达物理上存在矛盾：雷达接收功率与目标的雷达截面积（RCS）直接相关，而 RCS 本身隐含了“目标存在”的前提——高占用区域理应具有强 RCS，低占用区域则应具有弱 RCS。Radar Fields 的解耦预测却可能产生高占用低反射率的非物理组合，导致重建质量下降（Figure 2）。

此外，Radar Fields 依赖外部占用估计器（如 LiDAR 点云或 CFAR 检测器）提供占用监督，这不仅引入了额外的传感器依赖，也限制了方法的通用性。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **RF4D**，旨在实现室外动态场景的雷达新视角合成与占用估计。核心动机可归纳为两点：

1. **引入时间维度，建模动态场景。** 将场景表示为位置与时间的连续函数（时空神经场），并通过场景流模块预测运动偏移量，实现相邻帧间的占用一致性，从而有效渲染动态目标。
2. **设计物理一致的雷达功率渲染。** 基于雷达方程推导出占用与 RCS 的乘积形式渲染公式 $\hat{P}_{r} = \alpha \cdot \log_{10}(\sigma / \delta^{2})$，使占用作为软门控，确保高占用与强 RCS 正相关，消除占用-反射率矛盾，同时摆脱对外部占用监督的依赖。

RF4D 是首个利用神经场从雷达测量中建模动态场景的工作，其核心洞察在于：将雷达物理先验嵌入神经渲染管线，能够在无需额外传感器的情况下，同时实现高质量的雷达测量合成与几何占用估计。



## 核心方法与创新机理

RF4D 的核心创新在于通过**时空神经场**与**雷达物理先验**的深度融合，首次将神经雷达场从静态场景拓展至户外动态场景。其关键突破可归纳为三个相互耦合的“changed slots”。

### 1. 时间维度的显式引入与场景流建模

现有方法（如 **Radar Fields**）仅建模静态场景，无法处理移动物体。RF4D 将场景表示为位置 $\mathbf{x}$ 与时间 $t$ 的连续函数，通过时空编码器 $f_{\chi}(\mathcal{H}(\mathbf{x}), T(t))$ 将多分辨率哈希网格编码的位置与可学习时间嵌入融合为潜在特征 $\chi$，使网络能够感知场景的时间演化。

在此基础上，RF4D 引入**场景流模块** $f_{\Delta x}(\chi)$，预测每个空间点相对于相邻帧的运动偏移量 $\Delta x$。该偏移量将当前点变形到相邻帧，并通过共享的占用预测头计算变形后的占用值 $\alpha^{t-\Delta t}$ 和 $\alpha^{t+\Delta t}$，进而构建时间一致性损失 $\mathcal{L}_{\mathrm{oc}}$ 约束相邻帧占用一致。这一机制使 RF4D 能够稳定渲染动态车辆，而 Radar Fields 则完全无法恢复移动目标（见 Figure 1）。

### 2. 物理一致的雷达功率渲染公式

Radar Fields 存在一个根本性矛盾：其解耦预测的占用与反射率之间缺乏物理关联，常出现**高占用但低反射**的不一致现象，导致动态物体在渲染中“消失”。

RF4D 从雷达物理方程出发，将接收功率建模为：

$$\hat{P}_{r} = \alpha \cdot \log_{10}\left(\frac{\sigma}{\delta^{2}}\right)$$

其中 $\alpha$ 为占用（Gumbel-Sigmoid 激活），$\sigma$ 为雷达截面积（RCS），$\delta$ 为目标距离。该公式将占用作为**软门控**：当 $\alpha \to 0$ 时，无论 RCS 如何，合成功率趋近于零；当 $\alpha \to 1$ 时，功率由 RCS 对数与距离共同决定。这一设计确保了**高占用必然对应强 RCS**，从根本上消除了占位-反射矛盾（见 Figure 2），同时使网络无需外部占用监督即可从雷达功率重建损失中自主学习占用。

### 3. 内在占用学习与外部监督的解耦

Radar Fields 依赖外部占用估计器（如 LiDAR 或 CFAR）提供监督信号。RF4D 通过上述功率渲染公式，将占用学习完全内化于雷达功率重建损失 $\mathcal{L}_{\mathrm{rt}}$ 中。配合占用稀疏性正则化 $\mathcal{L}_{\mathrm{p}}$ 惩罚平均占用值以避免平凡解，以及 Gumbel-Sigmoid 激活驱动近二值化输出，RF4D 实现了从纯雷达测量中端到端学习占用，摆脱了对 LiDAR 等外部传感器的依赖。这一设计在 Boreas 雪景中尤为关键——此时 LiDAR 地面真值因暴雪不可靠，但 RF4D 仍能保持稳定的雷达测量重建（见 Figure 5）。

### 创新点间的协同效应

上述三个 changed slots 并非孤立运作：时间维度使场景流模块得以建模运动，运动偏移正则化 $\mathcal{L}_{\mathrm{m}}$ 约束变形幅度防止过度扭曲，时间一致性损失 $\mathcal{L}_{\mathrm{oc}}$ 则确保运动物体的占用在时序上平滑传递。三者与物理功率渲染公式共同构成完整的训练目标 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rt}} + \lambda_{\mathrm{oc}}\mathcal{L}_{\mathrm{oc}} + \lambda_{\mathrm{p}}\mathcal{L}_{\mathrm{p}} + \lambda_{\mathrm{m}}\mathcal{L}_{\mathrm{m}}$，消融实验证实移除任一组分均会导致性能显著退化（Table 3, Table 4）。



RF4D 将动态场景建模为一个时空神经场，其核心流水线由五个紧密耦合的模块构成，以雷达距离-方位图作为输入，输出新视角的合成雷达功率图与三维占位估计。整体架构如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed RF4D framework. Given a 3D query point x at time t and view direction d, RF4D first predicts two radar-specific physical quantities: occupancy α and radar cross-section (RCS) σ, using neural radar fields. The occupancy α indicates whether the point is physically occupied, and the RCS σ represents its reflectivity. These quantities are combined through the radarspecific power rendering to estimate the received radar power. During training, the rendered power is supervised by ground-truth radar measurements, and the scene flow module enforces temporal consistency by predicting motion offsets and warping points to adjacent frames to regularize occupancy over time*

**输入与投影。** 给定一帧雷达扫描，首先通过**雷达-世界投影**将每个距离-方位单元 $(\\delta, \\theta)$ 转换为世界坐标系下的三维查询点 $\\mathbf{x}$。具体而言，先将极坐标映射为雷达局部笛卡尔坐标 $\\mathbf{x}_{\\mathrm{radar}} = [\\delta \\cos(\\theta), \\delta \\sin(\\theta), 0]^T$，再利用雷达位姿 $H_i$ 变换到全局世界坐标 $\\mathbf{x}_{\\mathrm{world}} = H_i \\cdot \\mathbf{x}_{\\mathrm{radar}}$。

**时空编码。** 每个三维点 $\\mathbf{x}$ 与当前时间戳 $t$ 被送入**时空神经编码器**，通过多分辨率哈希网格 $\\mathcal{H}(\\mathbf{x})$ 与可学习时间嵌入 $T(t)$ 联合编码为潜在特征 $\\chi = f_{\\chi}(\\mathcal{H}(\\mathbf{x}), T(t))$。此设计使网络能够同时捕获空间几何与时间动态。

**物理量预测。** 潜在特征 $\\chi$ 被输入两个并行的预测头：**占位预测头** $f_{\\alpha}$ 输出占位值 $\\alpha$（经 Gumbel-Sigmoid 激活，趋向近二值化），**雷达截面积预测头** $f_{\\sigma}$ 结合方向编码 $S(\\mathbf{d})$ 输出方向相关的 RCS 值 $\\sigma$。这两个物理量是后续渲染与正则化的核心。

**时间一致性约束。** 为处理动态物体，**场景流模块** $f_{\\Delta x}$ 从 $\\chi$ 预测当前点相对于前一帧与后一帧的运动偏移量 $\\Delta x^-$ 和 $\\Delta x^+$。通过将点变形到相邻帧并重新编码、预测占位，得到 $\\alpha^{t-\\Delta t}$ 与 $\\alpha^{t+\\Delta t}$，进而施加时间一致性损失 $\\mathcal{L}_{\\mathrm{oc}}$，鼓励相邻帧占位预测一致。

**雷达特定功率渲染。** 最终，**雷达特定功率渲染器**将占位与 RCS 按物理公式合成为接收功率：

$$\hat{P}_{r} = \\alpha \\cdot \\log_{10}\\left(\\frac{\\sigma}{\\delta^{2}}\\right)$$

这里占位 $\\alpha$ 充当软门控——仅当点被判定为占位时，其 RCS 才对功率有显著贡献。这一设计从根本上消除了 Radar Fields 中存在的占位-反射不一致矛盾（高占位低反射），使占位与物理反射率保持正相关（见 Figure 2）。

**训练目标。** 整个框架端到端训练，总损失由四部分加权组成：

$$\mathcal{L}_{\\mathrm{total}} = \\mathcal{L}_{\\mathrm{rt}} + \\lambda_{\\mathrm{oc}} \\mathcal{L}_{\\mathrm{oc}} + \\lambda_{\\mathrm{p}} \\mathcal{L}_{\\mathrm{p}} + \\lambda_{\\mathrm{m}} \\mathcal{L}_{\\mathrm{m}}$$

其中 $\\mathcal{L}_{\\mathrm{rt}}$ 为合成功率与真实雷达功率的均方误差，$\\mathcal{L}_{\\mathrm{p}}$ 为占位稀疏性正则化（防止平凡全占位解），$\\mathcal{L}_{\\mathrm{m}}$ 为运动偏移量的 L2 正则化（防止过度变形）。值得注意的是，RF4D 完全摆脱了对外部占位监督（如 LiDAR 点云）的依赖，仅通过雷达功率重建损失与内部正则化即可学习有意义的占位场。

**输出。** 推理时，对于任意目标视角的雷达扫描，RF4D 可同时输出合成距离-方位功率图与三维占位体素网格（Figure 6），实现动态场景的新视角合成与三维几何重建。



### 3.1 雷达物理先验：接收功率方程

RF4D 的渲染设计根植于雷达物理。对于距离雷达 $\delta$ 处的单个目标，其接收功率由雷达方程给出：

$$P_{r} = \frac{P_{t} \cdot G^{2} \cdot \sigma}{(4\pi)^{3} \delta^{2}}$$

其中 $P_t$ 为发射功率，$G$ 为天线增益，$\sigma$ 为目标的雷达截面积（RCS）。该方程揭示了核心物理关系：接收功率与 RCS 成正比，与距离的四次方成反比。这一先验是后续功率渲染公式设计的物理基础。

### 3.2 时空神经编码器

为建模动态场景，RF4D 将场景表示为位置与时间的连续函数。对于给定 3D 查询点 $\mathbf{x}$ 和时间戳 $t$，时空潜在特征通过以下方式编码：

$$\chi = f_{\chi}(\mathcal{H}(\mathbf{x}), T(t))$$

- $\mathcal{H}(\mathbf{x})$：对 3D 位置的多分辨率哈希网格编码，捕获高频空间细节。
- $T(t)$：对时间戳的可学习嵌入，将时间信息注入潜在空间。
- $f_{\chi}$：融合网络，将空间与时间编码合并为统一潜在特征 $\chi$。

### 3.3 占用与 RCS 预测头

从潜在特征 $\chi$ 出发，两个并行预测头分别输出雷达特异性的物理量：

$$\begin{array}{r} \text{Occupancy } \alpha = f_{\alpha}(\chi) \\ \text{RCS } \sigma = f_{\sigma}(\chi, S(\mathbf{d})) \end{array}$$

- **占用 $\alpha$**：通过 Gumbel-Sigmoid 激活，输出近二值的软占用概率，表示该点是否被物理占据。
- **RCS $\sigma$**：预测方向相关的雷达截面积。其中 $S(\mathbf{d})$ 为视角方向 $\mathbf{d}$ 的编码（球谐函数），使反射率随观测角度变化，符合雷达物理特性。

### 3.4 雷达特定功率渲染器

RF4D 的核心创新在于将占用与 RCS 通过物理一致的方式耦合为合成接收功率。渲染公式为：

$$\hat{P}_{r} = \alpha \cdot \log_{10}\left(\frac{\sigma}{\delta^{2}}\right)$$

- **占用 $\alpha$ 作为软门控**：当 $\alpha \to 0$（自由空间），渲染功率被抑制；当 $\alpha \to 1$（被占据），功率由 RCS 和距离决定。这天然保证了“高占用对应强反射”的物理一致性，消除了 Radar Fields 中占用-反射解耦导致的矛盾。
- **对数变换**：对 $\sigma / \delta^{2}$ 取对数，将雷达方程中的乘性关系转化为加性关系，稳定训练梯度，同时匹配雷达功率通常以 dB 尺度表示的实际。
- **免外部占用监督**：该公式使占用可直接通过雷达功率重建损失学习，无需依赖 LiDAR 等外部占用估计器。

### 3.5 场景流模块与时间一致性

动态场景中，物体运动会导致相邻帧的占用预测不一致。RF4D 引入场景流模块，从潜在特征预测运动偏移量：

$$\Delta x = f_{\Delta x}(\chi)$$

其中 $\Delta x^{-}$ 和 $\Delta x^{+}$ 分别表示当前点相对于前一帧和后一帧的运动偏移。利用这些偏移，将点变形到相邻帧并预测占用：

$$\begin{array}{l} \alpha^{t-\Delta t} = f_{\alpha}(f_{\chi}(\mathcal{H}(x+\Delta x^{-}), \mathcal{T}(t-\Delta t))) \\ \alpha^{t+\Delta t} = f_{\alpha}(f_{\chi}(\mathcal{H}(x+\Delta x^{+}), \mathcal{T}(t+\Delta t))) \end{array}$$

这一机制不依赖外部光流或跟踪器，完全以自监督方式学习运动场，是 RF4D 能够渲染动态车辆而 Radar Fields 失败的关键（见图 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/002_Figure_2.jpg]]
*Figure 2: Predicted occupancy and reflectance from Radar Fields [4] versus occupancy and radar cross-section (RCS) from RF4D. Our predictions follow radar physics, where high occupancy corresponds to strong RCS, while Radar Fields lacks such consistency*



## 实验与关键发现

RF4D 在 Oxford RobotCar 和 Boreas 两个公开雷达数据集上进行了全面评估，覆盖多种天气条件和动态场景。实验从雷达测量合成质量与占位估计精度两个维度验证了方法的有效性。

### 主实验结果

在 RobotCar 数据集的四个驾驶场景中，RF4D 在所有指标上均显著优于现有方法 **Radar Fields**。以 Scene 1 为例，SSIM 从 0.3372 提升至 0.6103，提升幅度达 81%；Scene 3 的 CD（Chamfer Distance）从 9.5357 降至 3.2896，降幅达 65%（Table 1）。这表明 RF4D 在雷达功率图重建和 3D 几何恢复方面均取得了实质性进步。

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison across four different driving scenarios from the RobotCar dataset [2]. The best result and the runner-up are highlighted in bold and underline, respectively*

在 Boreas 数据集上，RF4D 同样展现出跨天气的鲁棒性。晴天场景（Sun）下 SSIM 达到 0.7001，较 Radar Fields 的 0.3641 提升 92%；雨天（Rain）和静态场景（Static）中各项指标也保持领先（Table 2）。值得注意的是，雪景的 CD 和 RCD 指标未报告，原因是暴雪条件下 LiDAR 地面真值不可靠，但 RF4D 的雷达功率合成质量（SSIM 0.7946）仍大幅领先。

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison across four driving scenarios from the Boreas dataset [6]. The best result and the runner-up are highlighted in bold and underline, respectively. CD and RCD are not reported for the snow scene due to unreliable ground-truth LiDAR geometry under heavy snowfall*

在占位估计任务上，RF4D 与基于 CFAR 的传统方法、贝叶斯滤波方法以及 Radar Fields 进行了对比（Table 5）。RF4D 在 RobotCar 四个场景和 Boreas 三个场景的 CD/RCD 指标上均取得最优或次优结果，例如 Scene 3 的 CD 仅为 3.2896，RCD 为 0.0097，验证了无需外部占位监督即可学习高质量 3D 占位的能力。

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/009_Table_5.jpg]]
*Table 5: Comparison of occupancy estimation results across different driving scenarios on the Oxford Radar RobotCar [2] and Boreas [6] datasets. The best and second-best results are highlighted in bold and underline, respectively*

定性结果（Figure 4）显示，RF4D 重建的雷达测量图结构清晰，动态目标（如移动车辆）得以完整保留，而 Radar Fields 的结果噪声更大且模糊。Figure 5 进一步展示了雷达在雪天条件下相对于 LiDAR 的鲁棒性——LiDAR 点云严重退化时，雷达测量保持稳定，RF4D 能够准确重建雷达测量，跨天气性能一致。

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison of novel-view radar measurement synthesis and occupancy estimation on the Oxford Radar RobotCar dataset [2]. Ground-truth occupancy is derived from LiDAR point clouds. RF4D reconstructs radar measurements with clear structures and preserved dynamic targets (red boxes), while Radar Fields produces noisier and blurrier results*

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/010_Figure_5.jpg]]
*Figure 5: Radar robustness and generalization across weather conditions. While LiDAR point clouds degrade severely in snow, radar measurements remain stable. RF4D accurately reconstructs radar measurements, maintaining consistent performance across different weather conditions*

### 消融实验

为验证各设计组件的贡献，论文在 RobotCar（Table 3）和 Boreas（Table 4）上进行了消融实验。

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/006_Table_3.jpg]]
*Table 3: Ablation study for the RobotCar dataset [2]. The best result and the runner-up are highlighted in bold and underline, respectively*

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/007_Table_4.jpg]]
*Table 4: Ablation study for the Boreas dataset [6]. The best result and the runner-up are highlighted in bold and underline, respectively. CD and RCD are not reported for the snow scene due to unreliable ground-truth LiDAR geometry under heavy snowfall*

**雷达功率重建损失（L_rt）的核心作用**：仅使用 L_rt 训练时，SSIM 和占位估计指标（CD、RCD）显著恶化，说明物理一致的功率渲染公式是模型有效性的基础。移除该损失意味着失去对占位和 RCS 的直接监督信号。

**时间一致性正则化（L_oc）与运动偏移正则化（L_m）**：引入 L_oc 可稳定训练过程，改善动态场景的视角合成质量；L_m 限制运动偏移量大小，防止过度变形。完整损失函数（L_total = L_rt + λ_oc·L_oc + λ_p·L_p + λ_m·L_m）在 RobotCar Scene 3 上取得 PSNR 23.76，Boreas Rain 场景取得 PSNR 27.98，均为各场景最优。

**Gumbel–Sigmoid 与稀疏性正则化（L_p）**：RF4D 采用 Gumbel–Sigmoid 激活函数配合占位门控机制，驱动神经场输出接近二值的占位值，有效抑制背景噪声。结合全局占位稀疏性正则化 L_p，避免了平凡解（全占位），生成更干净的渲染雷达测量和更可靠的占位图。

### 关键图表结论

- **Table 1 & Table 2**：RF4D 在 RobotCar 和 Boreas 数据集上全面超越 Radar Fields，尤其在动态场景和恶劣天气下优势显著。
- **Table 5**：占位估计精度优于传统 CFAR 方法和贝叶斯滤波，证明从雷达测量中端到端学习 3D 占位的可行性。
- **Figure 4**：定性展示 RF4D 的雷达测量合成质量——结构清晰、动态目标完整，而 Radar Fields 结果模糊且噪声大。
- **Figure 5**：雷达在雪天条件下保持稳定，RF4D 跨天气泛化能力强，弥补了 LiDAR 在恶劣天气下的退化问题。
- **Table 3 & Table 4**：消融实验证实物理一致功率渲染、时间一致性正则化和运动偏移正则化三者缺一不可，共同支撑 RF4D 的性能优势。

### 补充图表

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of radar view synthesis for a dynamic scene with a moving vehicle (orange box). RF4D successfully renders the moving object, whereas Radar Fields [4] fails to recover it*

![[assets/figures/papers/paper_list_l2584_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RF4DNeural_Radar/figures/011_Figure_6.jpg]]
*Figure 6: 3D voxel grid reconstruction from radar measurements. Our method reconstructs full 3D occupancy geometry from sparse and low-resolution radar data, capturing both moving vehicles and static objects present in the scene*



## 定位与知识库关联

### 1. 与基线方法的关系

RF4D 的核心定位是**首个将神经场用于雷达动态场景建模的工作**，其在方法谱系上同时承接了静态雷达神经渲染与动态视觉神经渲染两条技术路线。

**与 Radar Fields 的关系**：Radar Fields 是 RF4D 最直接的对比基线，也是雷达神经场领域的开创性工作。Radar Fields 仅处理静态场景，其渲染公式将占用与反射率解耦预测，导致“高占用-低反射”的物理矛盾——即模型可能在空间某处预测高占用概率，却赋予极低的反射率，使得动态物体在渲染中消失。RF4D 的核心改进在于两点：一是引入时间维度与场景流模块，使模型能建模动态物体的运动；二是设计了物理一致的雷达功率渲染公式 $\hat{P}_{r} = \alpha \cdot \log_{10}(\sigma / \delta^{2})$，将占用 $\alpha$ 作为软门控，确保高占用必然对应强雷达截面积（RCS）贡献，从根本上消除了占用-反射矛盾。这一改进同时移除了 Radar Fields 对外部占用监督（如 LiDAR）的依赖。

**与 D-NeRF 的关系**：**D-NeRF**（Pumarola et al., CVPR 2021）是基于 RGB 的动态场景神经渲染方法，通过变形场将观测帧映射到规范帧来实现时间一致性。RF4D 在跨域对比中将其作为基线，但两者在输入模态和物理建模上存在本质差异：D-NeRF 依赖 RGB 相机的稠密光度信号，而 RF4D 处理的是稀疏、低分辨率的雷达功率测量。RF4D 的场景流模块在思路上与变形场类似，均通过预测运动偏移量实现相邻帧一致性，但其偏移量直接作用于世界坐标系的 3D 点，并受 L2 正则化约束以防止过度变形。

**与 HexPlane 的关系**：**HexPlane**（Fridovich-Keil et al., CVPR 2023）采用显式时空分解进行动态场景重建，在 RGB 领域取得了高效的重建效果。RF4D 将其作为雷达域的动态基线进行对比，实验结果表明，基于显式分解的方法在雷达稀疏测量下的泛化能力有限，而 RF4D 的隐式时空神经场表示更适合雷达数据的特性。

**与传统雷达占用估计方法的关系**：RF4D 在占用估计任务上与 **CFAR-based method** 和 **Bayesian filter ** 等传统方法进行了对比（Table 5）。传统方法依赖手工设计的信号检测阈值或时序滤波，在复杂动态场景下鲁棒性不足。RF4D 通过端到端学习，仅从雷达功率重建损失中隐式习得占用，无需任何占用真值监督，在 CD 和 RCD 指标上显著优于传统方法。

### 2. 适用边界

RF4D 的设计假设和使用边界可从以下几个维度界定：

- **传感器模态**：专为 FMCW 雷达设计，利用距离-方位角极坐标表示的雷达功率图作为输入。核心物理建模依赖雷达方程 $P_{r} = \frac{P_{t} \cdot G^{2} \cdot \sigma}{(4\pi)^{3} \delta^{2}}$，因此方法对雷达的系统参数（发射功率 $P_t$、天线增益 $G$）具有依赖性。论文未验证该方法在 4D 成像雷达或其他雷达配置下的迁移能力。
- **场景类型**：面向室外自动驾驶场景，在 Oxford RobotCar 和 Boreas 两个数据集的多种天气条件（晴天、雨天、雪天、夜间）下进行了验证。动态物体主要为行驶中的车辆，论文未涉及行人、骑行者等非刚体或小尺度动态目标。
- **运动复杂度**：场景流模块预测的运动偏移量受 L2 正则化约束，倾向于平滑运动场。对于高速运动、急转弯或运动突变场景，该正则化可能过度平滑运动场，导致动态物体重建精度下降。这是一个需要人工验证的潜在局限点。
- **占用估计**：Gumbel-Sigmoid 激活配合全局稀疏性正则化推动占用值趋于二值化，适合刚体占用的建模，但对半透明或模糊边界（如植被、围栏）的占用估计可能存在偏差。

### 3. 局限与开放问题

论文未明确列出局限性章节，但从方法设计和实验设置中可推断以下局限，并结合雷达神经场领域的发展趋势提出开放问题：

- **跨传感器泛化**：RF4D 的物理渲染公式基于标准雷达方程，该方法能否推广到其他类型的雷达（如 4D 成像雷达、不同配置的 FMCW 雷达或合成孔径雷达）尚待验证。不同雷达的功率响应特性差异可能要求重新设计渲染公式。
- **大规模动态场景的鲁棒性**：场景流模块通过预测逐点运动偏移并变形到相邻帧来保持时间一致性，其计算开销与采样点数成正比。在高速运动或多动态对象场景下，运动偏移的预测精度和训练稳定性需要进一步评估。
- **多模态融合潜力**：RF4D 展示了仅从雷达测量中恢复 3D 占用的能力，但雷达的固有稀疏性和低分辨率限制了重建精度。如何将 RF4D 的框架与相机或 LiDAR 等多模态传感器融合，以提升重建质量和占用估计精度，是一个自然的扩展方向。
- **运动正则化的精细设计**：当前的运动偏移 L2 正则化对所有点施加均匀约束，可能过度平滑局部复杂运动。设计运动场自适应的正则化策略（如基于运动梯度或不确定性的加权约束）可能改善对非均匀运动的建模能力。
- **实时性约束**：论文未报告推理速度或计算开销。对于自动驾驶等实时应用场景，时空神经场的推理效率是一个关键考量，需要后续工作验证其是否满足部署要求。



## 原文 PDF

![[paperPDFs/CVPR_2026/RF4D_Neural_Radar_Fields_for_Novel_View_Synthesis_in_Outdoor_Dynamic_Scenes.pdf]]

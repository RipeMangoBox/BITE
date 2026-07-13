---
title: "The Spacetime of Diffusion Models: An Information Geometry Perspective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Spacetime_of_Diffusion_Models_An_Information_Geometry_Perspective.pdf
project_link: null
code_link: https://github.com/Aalto-QuML/spacetime-geometry
openreview_forum_id: qCsbYJZRA5
aliases:
- SFRGDM
- SDMIGP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入潜在时空变量 z=(x_t, t) 并应用 Fisher-Rao 信息度量，利用去噪分布构成的指数族结构，实现仿真自由的曲线能量估计，从而定义非平凡的几何结构，使测地线能够编码噪声与去噪的编辑序列。"
primary_logic: "扩散模型中的去噪分布 p(x_0|x_t) 可表示为指数族，其 Fisher-Rao 度量可以通过自然参数 η 和期望参数 μ 的雅可比计算，无需运行反向 SDE；由此得到的时空测地线对应于最小编辑序列，其长度即为扩散编辑距离（DiffED），并可高效生成分子过渡路径。"
claims:
- "标准回拉方法迫使测地线解码为数据空间的直线段，忽略曲率。"
- "去噪分布构成指数族，允许简化 Fisher-Rao 能量计算公式。"
- "曲线长度可在不运行反向 SDE 的情况下估计，显著降低计算成本。"
- "时空测地线可解释为最小化编辑序列：添加恰好足够的噪声以遗忘特定信息，再引入新的信息。"
---

# The Spacetime of Diffusion Models: An Information Geometry Perspective

> [!tip] 核心洞察
> 扩散模型中的去噪分布 p(x_0|x_t) 可表示为指数族，其 Fisher-Rao 度量可以通过自然参数 η 和期望参数 μ 的雅可比计算，无需运行反向 SDE；由此得到的时空测地线对应于最小编辑序列，其长度即为扩散编辑距离（DiffED），并可高效生成分子过渡路径。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散模型的时空：信息几何视角 |
| 英文题名 | The Spacetime of Diffusion Models: An Information Geometry Perspective |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=qCsbYJZRA5) · [GitHub](https://github.com/Aalto-QuML/spacetime-geometry) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Spacetime Fisher-Rao Geometry in Diffusion Models |
| Dataset | Alanine Dipeptide (MaxEnergy ↓), Alanine Dipeptide (#Evaluations ↓ for 1000 paths) |

> [!tip] 效果简介
> - Alanine Dipeptide (MaxEnergy ↓) 上，MaxEnergy (kcal/mol) 为 37.36 ± 0.60，对比 MCMC-fixed-length: 42.54 ± 7.42，变化 -5.18。
> - Alanine Dipeptide (#Evaluations ↓ for 1000 paths) 上，Number of energy evaluations 为 16M (+16M one-time training)，对比 MCMC-fixed-length: 1.29B，变化 reduction by ~1.27B。

## 概要

扩散模型在生成建模中取得了显著成功，但其潜在空间的几何结构尚未被充分理解。现有工作多采用基于确定性概率流 ODE（PF-ODE）解码器的回拉几何（pullback geometry），然而该方法存在根本性缺陷：**它迫使潜在空间中的测地线在数据空间解码为直线段，完全忽略数据流形的曲率结构**。另一方面，若仅以最终噪声 $\mathbf{x}_T$ 作为潜在变量并应用 Fisher-Rao 信息度量，由于去噪分布 $p(\mathbf{x}_0|\mathbf{x}_T)$ 在 $T$ 足够大时近似独立于 $\mathbf{x}_T$，度量将坍塌为零，无法区分不同点。

本文的核心洞见是：**扩散模型中的去噪分布 $p(\mathbf{x}_0|\mathbf{x}_t)$ 构成指数族**，其 Fisher-Rao 度量可通过自然参数 $\eta$ 与期望参数 $\mu$ 的雅可比高效计算，无需运行反向 SDE。基于此，作者提出**潜在时空变量 $\mathbf{z} = (\mathbf{x}_t, t)$**，将所有噪声水平统一建模，从而恢复非平凡的几何结构。在此框架下，时空测地线对应于两点之间的最小编辑序列——先添加恰好足够的噪声以遗忘源点特有信息，再通过去噪引入目标点信息；其长度定义为**扩散编辑距离（DiffED）**。

方法定位上，本文属于扩散模型与信息几何的交叉研究，区别于基于 PF-ODE 的回拉几何（测地线解码为直线）和 MCMC 过渡路径采样方法（如 **Brotzakis & Bolhuis, 2016** 的 two-way shooting）。在丙氨酸二肽（Alanine Dipeptide）过渡路径采样任务上，该方法以 **37.36 ± 0.60 kcal/mol** 的最大能量显著优于 MCMC 基线（42.54 ± 7.42），且能量评估次数从 12.9 亿次降至 1600 万次（外加一次性训练成本）。在图像域，DiffED 与 SSIM 相关性达 53%，与 LPIPS 相关性仅 -7%，表明其捕捉结构相似性而非感知相似性。



### 扩散模型的几何化趋势

扩散模型通过前向过程将数据逐步转化为噪声，再通过逆向过程从噪声中重建数据，其核心由前向过程

$$p(\pmb{x}_t|\pmb{x}_0) = \mathcal{N}(\pmb{x}_t|\alpha_t\pmb{x}_0, \sigma_t^2\pmb{I})$$

和逆向随机微分方程

$$d\pmb{x} = \big( f_t\pmb{x} - g_t^2 \nabla \log p_t(\pmb{x}) \big) dt + g_t d\overline{\mathbf{W}}_t$$

及其确定性对应——概率流 ODE

$$d\pmb{x} = \Big( f_t\pmb{x} - \frac{1}{2} g_t^2 \nabla \log p_t(\pmb{x}) \Big) dt$$

共同定义。近年来，研究者开始从几何角度审视扩散模型，试图为潜在空间赋予黎曼度量，从而利用测地线刻画数据点之间的“最短路径”。这一思路在分子过渡路径采样、图像编辑距离等任务中具有天然的应用潜力。

### 现有方法的两个关键缺口

然而，现有的几何化尝试存在两个根本性缺陷，构成了本文的核心动机。

**缺口一：回拉几何迫使测地线解码为直线。** 最直接的做法是将扩散模型的确定性 PF-ODE 解码器视为从噪声空间到数据空间的映射，并将数据空间的欧氏度量回拉到噪声空间，构造所谓的回拉度量：

$$\mathbf{G}_{\mathrm{PB}}(\mathbf{x}_T) = \left( \frac{\partial \mathbf{x}_0}{\partial \mathbf{x}_T} \right)^\top \left( \frac{\partial \mathbf{x}_0}{\partial \mathbf{x}_T} \right).$$

该度量的测地线在噪声空间中可能呈现弯曲，但一经解码器映射回数据空间，便被**证明性地强制为直线段**（Figure 2），完全忽略了数据流形的曲率结构。换言之，回拉几何无法捕捉数据分布的内在几何特征。

**缺口二：基于 $x_T$ 的 Fisher-Rao 度量发生坍塌。** 若放弃回拉思路，直接以最终噪声 $x_T$ 为潜在变量，并采用 Fisher-Rao 信息度量：

$$\mathbf{G}_{\mathrm{IG}}(\pmb{x}_T) = \mathbb{E}_{\pmb{x}_0 \sim p(\pmb{x}_0|\pmb{x}_T)} \big[ \nabla_{\pmb{x}_T} \log p(\pmb{x}_0|\pmb{x}_T) \nabla_{\pmb{x}_T} \log p(\pmb{x}_0|\pmb{x}_T)^\top \big],$$

则面临另一个问题：当 $T$ 足够大时，$x_T$ 几乎为纯噪声，去噪分布 $p(x_0|x_T)$ 对 $x_T$ 的依赖极弱，导致 Fisher-Rao 度量近似为零，无法有效区分不同点。这一“度量坍塌”现象使得基于 $x_T$ 的几何结构失去实用价值。

### 本文动机：从空间到时空

上述两个缺口的共同根源在于**仅将扩散模型的某一时刻（$t=0$ 或 $t=T$）作为几何载体**。本文的核心洞察是：扩散模型的去噪过程本身蕴含丰富的几何信息——不同噪声水平下的去噪分布 $p(x_0|x_t)$ 构成了一个指数族，其 Fisher-Rao 度量可以通过自然参数 $\eta$ 和期望参数 $\mu$ 的雅可比高效计算，**无需运行逆向 SDE**。具体而言，

$$\eta(\pmb{x}_t,t) = \big( \frac{\alpha_t}{\sigma_t^2}\pmb{x}_t, -\frac{\alpha_t^2}{2\sigma_t^2} \big), \quad \mu(\pmb{x}_t,t) = \big( \mathbb{E}[\pmb{x}_0|\pmb{x}_t], \mathbb{E}[\|\pmb{x}_0\|^2|\pmb{x}_t] \big),$$

其中 $\mu$ 可通过 Tweedie 公式和 Hutchinson 迹估计器实现仿真自由的计算：

$$\mathbb{E}[\|\pmb{x}_0\|^2|\pmb{x}_t] \approx \|\hat{\pmb{x}}_0(\pmb{x}_t)\|^2 + \frac{\sigma_t^2}{\alpha_t} \mathrm{div}_{\pmb{x}_t} \hat{\pmb{x}}_0(\pmb{x}_t).$$

基于此，本文提出将潜在变量从单一时刻扩展为**时空点 $\boldsymbol{z} = (\boldsymbol{x}_t, t) \in \mathbb{R}^D \times (0, T]$**，并赋予其基于指数族结构的 Fisher-Rao 度量。由此得到的时空测地线具有明确的语义解释：它是两数据点之间的**最小编辑序列**——先添加恰好足够的噪声以遗忘源点的特定信息，再通过去噪引入目标点的特定信息。其长度即为**扩散编辑距离（DiffED）**：

$$\mathrm{DiffED}(\pmb{x}^a, \pmb{x}^b) = \ell(\gamma).$$

Figure 1 给出了这一概念的可视化：时空测地线是连接两个去噪分布的最短路径，其贯穿不同噪声水平的过程天然编码了“遗忘-重建”的编辑语义。



## 核心方法与创新机理

本文的核心创新在于**将扩散模型的潜在空间重新构建为“时空”流形**，并赋予其信息几何度量，从而克服了现有几何方法的两大根本性缺陷。

### 从回拉几何到信息几何的范式转换

此前基于扩散模型潜在空间的几何研究主要采用**回拉度量**（Pullback Metric），即通过确定性概率流 ODE 解码器将数据空间的黎曼度量拉回到噪声空间。然而，本文揭示了该方法的致命缺陷：由于扩散模型的潜在空间与数据空间维度相同，解码器直接在环境空间中操作，导致**所有回拉测地线在数据空间解码后必然退化为直线段**（Figure 2），完全无法捕捉数据流形的曲率结构。

另一方面，若将潜在变量直接设为最终噪声 $x_T$ 并采用 Fisher-Rao 度量，则会遭遇**度量坍塌**问题：当 $t \to T$ 时，去噪分布 $p(x_0|x_T)$ 近似与 $x_T$ 无关，导致 Fisher-Rao 度量趋近于零，无法区分不同噪声点。

### 核心机制：时空 Fisher-Rao 几何

本文的关键突破在于**将潜在变量从单一的 $x_T$ 扩展为时空点 $z = (x_t, t)$**，统一建模所有噪声水平下的去噪分布。这一设计恢复了非平凡的几何结构，使测地线能够编码从噪声到去噪的完整编辑序列。

在此基础上，作者证明**去噪分布 $p(x_0|x_t)$ 构成指数族**，其 Fisher-Rao 度量可通过自然参数 $\eta$ 与期望参数 $\mu$ 的雅可比简洁计算：

$$\mathcal{E}(\gamma) \approx \frac{N-1}{2} \sum_{n=0}^{N-2} \big( \pmb{\eta}(z_{n+1}) - \pmb{\eta}(z_n) \big)^\top \big( \pmb{\mu}(z_{n+1}) - \pmb{\mu}(z_n) \big)$$

这一公式的关键优势在于**仿真自由**（simulation-free）：曲线能量估计仅需计算去噪器的雅可比向量积（通过 Tweedie 公式与 Hutchinson 技巧），无需运行反向 SDE，大幅降低了计算成本。

### 从几何到应用：扩散编辑距离与过渡路径采样

时空测地线具有优雅的物理解释：**两点之间的测地线对应于最小编辑序列**——先添加恰好足够的噪声以遗忘源点的特定信息，再通过去噪引入目标点的信息。测地线长度即为**扩散编辑距离**（DiffED）：

$$\mathrm{DiffED}(\pmb{x}^a, \pmb{x}^b) = \ell(\gamma)$$

在分子动力学领域，这一几何结构自然延伸为**过渡路径采样**：通过在测地线上执行退火朗之万动力学，可高效生成低能态之间的过渡路径，且能通过约束优化实现低方差或区域避免（Figure 7）。

### 方法谱系与知识库定位

| 维度 | 回拉几何基线 | 本文方法 |
|------|-------------|---------|
| 潜在表示 | 最终噪声 $x_T$ | 时空点 $z = (x_t, t)$ |
| 黎曼度量 | 回拉度量（解码为直线段） | 指数族 Fisher-Rao 度量 |
| 能量估计 | 需运行反向 SDE 或不可处理 | 仿真自由（仅需去噪器雅可比） |
| 几何意义 | 忽略数据流形曲率 | 编码噪声-去噪编辑序列 |

在过渡路径采样任务上，本文方法在丙氨酸二肽基准上取得 MaxEnergy = 37.36 ± 0.60 kcal/mol，显著优于 MCMC 基线（42.54 ± 7.42），且能量评估次数从 1.29B 降至 16M（不含一次性训练成本，Table 1）。与 **Doob's Lagrangian**（Du et al., 2024）等先进方法的对比显示，本文路径能更好地避开高能区域且不塌缩为单一路径（Figure 6）。

### 局限与待验证边界

- **数值稳定性**：测地线端点需锚定在 $t_{\min} > 0$ 以避免 $t \approx 0$ 时去噪分布趋近狄拉克 $\delta$ 函数导致的能量爆炸。
- **计算效率**：DiffED 计算约需 6 分钟/对（A100），远慢于 LPIPS/SSIM 等感知指标，不适合实时应用。
- **感知相关性**：DiffED 与 LPIPS 相关性仅约 -7%，与 SSIM 相关性约 53%，表明其捕捉结构相似性而非像素级感知相似性。
- **应用范围**：过渡路径采样目前仅适用于具有已知能量函数的分子系统；部分基线方法（Holdijk et al., 2023; Raja et al., 2025）因可重现性问题未纳入对比，需手动验证。



![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_qCsbYJZRA5/figures/009_Figure_6.jpg]]
*Figure 6: Transition paths generated with a spacetime geodesic avoid high-energy regions without collapsing to a single path. Compared with MCMC baselines, the spacetime-geodesic method yields transition paths that better avoid high-energy areas, whereas Doob’s Lagrangian collapses to generating nearly identical trajectories. Ten sample paths are shown for each method*

本文提出的时空 Fisher-Rao 几何框架围绕一个核心洞察展开：扩散模型中的去噪分布 $p(\pmb{x}_0|\pmb{x}_t)$ 构成指数族，使得 Fisher-Rao 度量可以通过自然参数 $\eta$ 与期望参数 $\mu$ 的雅可比计算，无需运行反向 SDE。由此得到的时空测地线对应于最小编辑序列，其长度即为扩散编辑距离（DiffED），并可高效生成分子过渡路径。

### 核心瓶颈与因果调控

**瓶颈**：标准回拉几何（基于确定性 PF-ODE 解码器）迫使潜在空间测地线在数据空间解码为直线段，完全忽略数据的流形结构（Figure 2）；另一方面，若仅以最终噪声 $\pmb{x}_T$ 为潜在变量，Fisher-Rao 度量因模型的无记忆性而近似为零，导致度量坍塌，无法区分不同点。

**因果调控**：引入潜在时空变量 $\pmb{z} = (\pmb{x}_t, t) \in \mathbb{R}^D \times (0, T]$，统一所有噪声水平，并应用基于去噪分布指数族结构的 Fisher-Rao 度量，实现仿真自由的曲线能量估计，从而定义非平凡的几何结构。

### 方法谱系与知识库定位

本框架在三个关键维度上区别于现有方法：

| 维度 | 基线方法 | 本文方法 |
|------|----------|----------|
| 潜在表示 | 最终时刻的噪声 $\pmb{x}_T$ | 时空点 $\pmb{z} = (\pmb{x}_t, t)$ |
| 黎曼度量 | 回拉度量（或基于 $\pmb{x}_T$ 的坍塌 Fisher-Rao） | 基于去噪分布指数族结构的 Fisher-Rao 度量 |
| 能量估计 | 不可处理或需运行反向 SDE | 使用自然/期望参数的仿真自由估计（Tweedie 公式 + Hutchinson 技巧） |

在过渡路径采样任务上，基线方法包括 **MCMC two-way shooting**（Brotzakis & Bolhuis, 2016）和 **Doob's Lagrangian**（Du et al., 2024）。本文方法在丙氨酸二肽上取得了更低的 MaxEnergy（37.36 vs. 42.54 kcal/mol），且能量评估次数从 1.29B 降至 16M（+16M 一次性训练成本），独立于生成的路径数量。

### 整体 Pipeline

框架由七个核心模块串联构成，形成从扩散过程定义到最终应用的完整闭环：

**1. 前向过程定义**：定义扩散过程，将数据逐步转化为噪声：
$$p(\pmb{x}_t|\pmb{x}_0) = \mathcal{N}(\pmb{x}_t|\alpha_t\pmb{x}_0, \sigma_t^2\pmb{I})$$

**2. 去噪器建模（分数估计）**：近似去噪期望 $\mathbb{E}[\pmb{x}_0|\pmb{x}_t]$ 或分数函数，本文使用 EDM2 模型。

**3. 期望参数计算**：利用 Tweedie 公式和 Hutchinson 技巧计算期望参数 $\mu$ 和自然参数 $\eta$：
$$\eta(\pmb{x}_t,t) = \big( \frac{\alpha_t}{\sigma_t^2}\pmb{x}_t, -\frac{\alpha_t^2}{2\sigma_t^2} \big), \quad \mu(\pmb{x}_t,t) = \big( \mathbb{E}[\pmb{x}_0|\pmb{x}_t], \mathbb{E}[\|\pmb{x}_0\|^2|\pmb{x}_t] \big)$$
其中 $\mathbb{E}[\|\pmb{x}_0\|^2|\pmb{x}_t] \approx \|\hat{\pmb{x}}_0(\pmb{x}_t)\|^2 + \frac{\sigma_t^2}{\alpha_t} \mathrm{div}_{\pmb{x}_t} \hat{\pmb{x}}_0(\pmb{x}_t)$，散度项通过 Hutchinson 随机迹估计器计算，仅需去噪器的雅可比向量积。

**4. 曲线能量/长度估计**：基于指数族结构，离散曲线的信息几何能量可近似为：
$$\mathcal{E}(\gamma) \approx \frac{N-1}{2} \sum_{n=0}^{N-2} \big( \pmb{\eta}(z_{n+1}) - \pmb{\eta}(z_n) \big)^\top \big( \pmb{\mu}(z_{n+1}) - \pmb{\mu}(z_n) \big)$$
该估计是仿真自由的，无需运行反向 SDE，显著降低计算成本。

**5. 测地线优化**：通过梯度下降优化三次样条曲线以最小化能量，端点锚定在 $t_{\min} > 0$ 以保证数值稳定性。

**6. 扩散编辑距离计算**：最终测地线长度即为两数据点间的 DiffED：
$$\mathrm{DiffED}(\pmb{x}^a, \pmb{x}^b) = \ell(\gamma)$$
该距离度量捕捉结构相似性（与 SSIM 相关性 53%），而非感知相似性（与 LPIPS 相关性 -7%）。

**7. 过渡路径采样**：沿测地线利用退火朗之万动力学采样过渡路径：
$$d\pmb{x} = -\nabla_{\pmb{x}} U(\pmb{x}|\gamma_s) dt + \sqrt{2} d\mathbf{W}_t$$
当数据分布为玻尔兹曼分布时，条件能量函数为 $U(\pmb{x}_0|\pmb{x}_t) = U(\pmb{x}_0) + \frac{1}{2} \mathrm{SNR}(t) \|\pmb{x}_0 - \pmb{x}_t/\alpha_t\|^2$。交替执行朗之万步骤与测地线点更新，逐步从 $s=0$ 退火至 $s=1$。

### 输入输出流

- **输入**：两个数据点 $\pmb{x}^a, \pmb{x}^b$（图像或分子构象），预训练扩散模型
- **中间表示**：时空曲线 $\gamma: [0,1] \to \mathbb{R}^D \times (0, T]$，离散化为 $N$ 个点
- **核心计算**：通过 $\eta$ 和 $\mu$ 的差分估计 Fisher-Rao 能量，梯度下降优化曲线
- **输出**：
  - 扩散编辑距离 DiffED（标量，衡量编辑代价）
  - 时空测地线（可视化编辑序列，Figure 4）
  - 过渡路径样本（用于分子动力学，Figure 5）

### 约束扩展

框架支持通过惩罚项实现约束路径采样：
$$\min_{\gamma} \left\{ \mathcal{E}(\gamma) + \lambda \int_{0}^{1} h(\gamma_s) ds \right\}$$
例如，通过惩罚低 SNR 实现低方差过渡路径，或通过 KL 散度惩罚 $\mathrm{KL}[p(\cdot|z^*) \| p(\cdot|\gamma_s)]$ 实现区域避免，而不会塌缩为单一路径（Figure 7）。

### 已知局限

- **数值稳定性**：端点需锚定在 $t_{\min} > 0$，避免 $t \approx 0$ 时去噪分布趋近于狄拉克 $\delta$ 函数导致的能量爆炸
- **计算速度**：DiffED 约 6 分钟/对（A100），远慢于 LPIPS（毫秒级），不适合实时应用
- **应用范围**：过渡路径采样目前仅适用于具有已知能量函数的分子系统
- **基线对比**：因可重现性问题，未与 Holdijk et al. (2023) 和 Raja et al. (2025) 的原方法比较



### 潜在时空表示

本方法的核心创新在于将扩散模型的潜在空间从单一的最终噪声状态 $x_T$ 扩展为 **$(D+1)$ 维的潜在时空点**：

$$z = (x_t, t) \in \mathbb{R}^D \times (0, T]$$

这一设计直接解决了两个根本性问题：① 标准回拉度量迫使测地线在数据空间解码为直线段，完全忽略数据流形的曲率；② 若仅以 $x_T$ 为潜在变量，Fisher-Rao 度量因去噪分布 $p(x_0|x_T)$ 近似独立于 $x_T$ 而坍塌为零，无法区分不同点。通过同时建模所有噪声水平，时空表示恢复了非平凡的几何结构。

### 指数族结构与 Fisher-Rao 度量

本方法的关键洞察是：**去噪分布构成指数族**。对于标准高斯前向过程：

$$p(x_t|x_0) = \mathcal{N}(x_t|\alpha_t x_0, \sigma_t^2 I)$$

其对应的去噪分布 $p(x_0|x_t)$ 可表示为指数族，其**自然参数** $\eta$ 与**期望参数** $\mu$ 分别为：

$$\eta(x_t, t) = \left( \frac{\alpha_t}{\sigma_t^2} x_t, -\frac{\alpha_t^2}{2\sigma_t^2} \right), \quad \mu(x_t, t) = \left( \mathbb{E}[x_0|x_t], \mathbb{E}[\|x_0\|^2|x_t] \right)$$

这一指数族结构使得 Fisher-Rao 度量的计算得到极大简化。对于时空曲线 $\gamma$，其信息几何能量可近似为：

$$\mathcal{E}(\gamma) \approx \frac{N-1}{2} \sum_{n=0}^{N-2} \big( \eta(z_{n+1}) - \eta(z_n) \big)^\top \big( \mu(z_{n+1}) - \mu(z_n) \big)$$

该公式仅需计算自然参数与期望参数的差分内积，**无需运行反向 SDE**，显著降低了计算成本。

### 仿真自由的能量估计

期望参数 $\mu$ 中的第二项 $\mathbb{E}[\|x_0\|^2|x_t]$ 需要特殊处理。利用 **Tweedie 公式**和 Hutchinson 技巧：

$$\mathbb{E}[\|x_0\|^2|x_t] \approx \|\hat{x}_0(x_t)\|^2 + \frac{\sigma_t^2}{\alpha_t} \text{div}_{x_t} \hat{x}_0(x_t)$$

其中 $\hat{x}_0(x_t)$ 是预训练去噪器对 $\mathbb{E}[x_0|x_t]$ 的估计，散度项通过 Hutchinson 随机迹估计器（仅需计算去噪器的雅可比向量积）高效求解。整个能量估计过程是**仿真自由的**（simulation-free），无需运行扩散采样的前向或反向过程。

### 测地线优化与扩散编辑距离

测地线通过梯度下降优化三次样条曲线以最小化能量 $\mathcal{E}(\gamma)$ 得到。两数据点 $x^a$ 与 $x^b$ 之间的**扩散编辑距离**（Diffusion Edit Distance, DiffED）定义为该时空测地线的长度：

$$\text{DiffED}(x^a, x^b) = \ell(\gamma)$$

该距离的物理含义是：测地线在时空中的路径对应于**最小编辑序列**——先添加恰好足够的噪声以遗忘 $x^a$ 特有的信息，再通过去噪引入 $x^b$ 特有的信息。

### 过渡路径采样

对于具有已知能量函数 $U(x)$ 的分子系统（数据分布为玻尔兹曼分布 $q(x) \propto \exp(-U(x))$），去噪分布具有可处理的形式：

$$p(x_0|x_t) \propto \exp\left(-U(x_0) - \frac{1}{2}\text{SNR}(t)\|x_0 - x_t/\alpha_t\|^2\right)$$

过渡路径采样采用**退火朗之万动力学**沿测地线进行：

$$dx = -\nabla_x U(x|\gamma_s) dt + \sqrt{2} d\mathbf{W}_t$$

通过交替执行朗之万步骤与沿测地线推进锚点 $\gamma_n \mapsto \gamma_{n+1}$，该方法生成的过渡路径能有效避开高能区域，且不会塌缩为单一路径。



## 实验与关键发现

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_qCsbYJZRA5/figures/010_Table_1.jpg]]
*Table 1: Spacetime geodesics outperform methods tailored to transition path sampling. Parentheses denote extra energy evaluations used to generate training data for the base diffusion model, which do not scale with the number of generated paths. Baseline details in Appendix H*

### 过渡路径采样：丙氨酸二肽上的定量评估

在分子动力学标准基准丙氨酸二肽（Alanine Dipeptide）上，时空测地线方法在过渡路径采样的两项关键指标上均显著优于现有基线。表 1 汇总了核心定量结果。

**最大能量（MaxEnergy ↓）**：时空测地线方法达到 **37.36 ± 0.60 kcal/mol**，相比 MCMC-fixed-length 基线的 42.54 ± 7.42 kcal/mol 降低了约 5.18 kcal/mol，且方差大幅缩小（0.60 vs. 7.42），表明路径质量更稳定。Doob’s Lagrangian（Du et al., 2024）的已发布实现结果显著差于原论文报告，作者推测可能源于数值不稳定性，因此未直接纳入对比。

**能量评估次数（#Evaluations ↓）**：生成 1000 条过渡路径时，时空测地线方法仅需 **1600 万次**能量评估（另加 1600 万次用于扩散模型的一次性预训练），而 MCMC-fixed-length 基线需要 **12.9 亿次**，减少约 1.27 亿次评估。这一数量级差异的关键在于：测地线优化本身是仿真自由的（simulation-free）——曲线能量可直接通过指数族结构估计，无需运行反向 SDE 或反复查询能量函数；预训练的 1600 万次成本独立于生成路径数量，路径越多，摊销优势越显著。

**公平性说明**：部分基线（Holdijk et al., 2023; Raja et al., 2025）因可重现性问题被排除。Doob’s Lagrangian 的对比受其实现数值不稳定影响。本方法的一次性预训练成本在评估时未计入，但独立于路径数量。

### 定性分析：高能区域规避与路径多样性

图 5 展示了丙氨酸二肽能量景观上的完整工作流：左图为 ϕ/ψ 二面角空间中的能量分布，中图为连接两个低能态的时空测地线 γ，右图为沿测地线通过退火朗之万动力学采样的过渡路径。图 6 的定性对比进一步揭示：时空测地线方法生成的过渡路径能更好地规避高能区域，同时不会坍缩为单一路径；相比之下，MCMC 基线（Brotzakis & Bolhuis, 2016）的路径在能量景观中穿越更多高能区。

### 约束过渡路径：低方差与区域规避

测地线优化框架天然支持通过惩罚项施加路径约束。图 7 展示了两种约束模式的定性结果：

- **低方差过渡路径**：通过惩罚低 SNR 区域（即惩罚过度加噪），迫使路径保持在较低噪声水平，从而减小样本方差。
- **区域规避**：通过引入 KL 散度惩罚项，使路径的中间去噪分布远离指定的受限区域 $p(\cdot|z^*)$，成功避开禁止区域而不影响路径多样性。

这些约束均通过在原能量函数 $\mathcal{E}(\gamma)$ 上添加惩罚项实现，优化过程与无约束版本一致，无需修改底层几何结构。

### 消融实验：PF-ODE 轨迹与测地线的对比

图 3 提供了关键消融证据，比较了 PF-ODE 采样轨迹与能量最小化测地线在两种场景下的行为差异：

- **1D 玩具密度（左）**：在高噪声水平（早期采样阶段），时空测地线比 PF-ODE 轨迹更“直”——即测地线以更短的路径穿越噪声-时间空间。随着噪声水平降低，两者逐渐趋近，在低噪声区域几乎无法区分。这验证了理论分析：标准回拉几何迫使测地线解码为数据空间直线段，而时空 Fisher-Rao 度量在噪声空间中编码了更丰富的几何结构。
- **ImageNet-512 EDM2 模型（右）**：在真实图像生成模型中，测地线与 PF-ODE 采样轨迹的感知差异极小，但测地线倾向于更早引入信息（即更早开始去噪）。这表明在高维数据中，PF-ODE 路径本身已接近能量最小化路径，但时空几何提供了更原则性的编辑距离定义。

### DiffED 与感知度量的相关性分析

扩散编辑距离（DiffED）作为两数据点之间时空测地线的长度，定义了一种新的相似性度量。图 8 在 20 对随机图像上定性比较了 DiffED、LPIPS、SSIM 和欧氏距离的排序结果：

- **与 SSIM 的相关性为 53%**：DiffED 与结构相似性指数存在中等正相关，表明它捕捉的是图像间的结构编辑代价，而非像素级差异。
- **与 LPIPS 的相关性约为 -7%**：几乎为零的负相关说明 DiffED 与感知相似性度量本质不同——它衡量的是“需要多少编辑操作才能将一幅图变为另一幅”，而非人类感知的距离。

这一发现揭示了 DiffED 的适用边界：它适合评估编辑结构相似性，但不适合替代感知质量指标。

### 失败模式与局限性

1. **数值稳定性**：测地线端点需锚定在 $t_{\min} > 0$，而非 $t=0$。原因在于 $t \to 0$ 时去噪分布趋近于狄拉克 δ 函数，导致 Fisher-Rao 度量奇异、能量估计爆炸。这限制了方法在近乎干净样本间的直接应用。
2. **计算速度**：DiffED 计算约需 6 分钟/对（A100 GPU），远慢于 LPIPS/SSIM 的毫秒级推理，不适用于实时或大规模检索场景。
3. **与感知质量脱节**：DiffED 与 LPIPS 的相关性极低（-7%），确认其不适合作为感知相似性的替代度量。
4. **应用领域限制**：过渡路径采样目前仅适用于具有已知能量函数的分子系统（如玻尔兹曼分布），且需额外的退火朗之万步骤。对于图像等无明确能量函数的领域，过渡路径的定义尚不明确。
5. **基线对比不完整**：因可重现性问题，未与 Holdijk et al. (2023) 和 Raja et al. (2025) 的原方法直接比较，相关结论的普适性需进一步验证。



## 定位与知识库关联

### 核心瓶颈：从回拉几何到信息几何的范式转换

扩散模型的潜在空间几何研究存在两条主要路线：**确定性回拉几何**与**随机信息几何**。本文揭示了这两条路线在扩散模型语境下的根本性缺陷，并提出了统一的时空 Fisher-Rao 框架。

**回拉几何的失效。** 标准方法将 PF-ODE 解码器 $x_0(x_T)$ 视为从噪声到数据的确定性映射，并定义回拉度量 $\mathbf{G}_{\mathrm{PB}}(\mathbf{x}_T) = (\partial \mathbf{x}_0 / \partial \mathbf{x}_T)^\top (\partial \mathbf{x}_0 / \partial \mathbf{x}_T)$。该度量的测地线衡量噪声变化对解码样本的影响，但存在致命缺陷：由于扩散模型中潜在空间与数据空间维度相同，解码器直接在环境空间中操作，**所有回拉测地线在数据空间解码为直线段**，完全忽略数据流形的曲率结构。这一结论可被严格证明，使得回拉几何在扩散模型中“实际上毫无用处”。

**Fisher-Rao 度量的坍塌。** 若改用随机解码器，将潜在变量视为 $x_T$，并定义 Fisher-Rao 度量 $\mathbf{G}_{\mathrm{IG}}(\mathbf{x}_T) = \mathbb{E}_{p(x_0|x_T)}[\nabla_{x_T} \log p(x_0|x_T) \nabla_{x_T} \log p(x_0|x_T)^\top]$，则面临另一种坍塌：当 $t=T$ 时，$p(x_0|x_T)$ 近似独立于 $x_T$，导致 Fisher-Rao 度量趋近于零，无法区分不同点，几何结构完全退化。

**时空变量的因果杠杆。** 本文的关键操作是引入 $(D+1)$ 维潜在时空变量 $\boldsymbol{z} = (\boldsymbol{x}_t, t) \in \mathbb{R}^D \times (0, T]$，同时对所有噪声水平建模。这一操作恢复了非平凡的几何结构：去噪分布 $p(x_0|x_t)$ 构成指数族，其 Fisher-Rao 度量可通过自然参数 $\eta$ 和期望参数 $\mu$ 的雅可比计算，**无需运行反向 SDE**，实现了仿真自由的曲线能量估计。由此得到的时空测地线对应于最小编辑序列：先添加恰好足够的噪声以遗忘源数据特定信息，再通过去噪引入目标数据信息。

### 与现有方法的谱系关系

**过渡路径采样基线。** 在分子动力学领域，过渡路径采样是经典难题。本文与以下方法构成直接对比：

- **MCMC two-way shooting**（Brotzakis & Bolhuis, 2016）：通过 MCMC 采样生成固定长度的过渡路径，但需要大量能量评估（Table 1 中约 1.29B 次），且路径倾向于穿越高能区域。
- **Doob's Lagrangian**（Du et al., 2024）：利用 Doob 变换构造条件扩散过程，理论上是先进方法，但已发布实现的结果显著差于原论文报告，可能因数值不稳定。在本文实验中，Doob's Lagrangian 产生的路径与无条件采样高度相似，未能有效避开高能区。

**图像相似度度量。** DiffED 与现有感知度量的定位关系明确：
- 与 **LPIPS**（Zhang et al., 2018）相关性仅约 -7%，表明 DiffED 不捕捉像素级感知相似性。
- 与 **SSIM** 相关性约 53%，说明 DiffED 更关注结构相似性，这与“编辑结构”的几何解释一致。
- 计算速度远慢于 LPIPS/SSIM（约 6 分钟/对 vs. 毫秒级，A100），不适合实时应用。

**未直接对比的方法。** 因可重现性问题，本文未与 **Holdijk et al.**（2023）和 **Raja et al.**（2025）的过渡路径采样方法进行定量比较。这一缺失需要在未来工作中补全。

### 适用边界与局限

1. **数值稳定性约束。** 测地线端点必须锚定在 $t_{\min} > 0$，因为 $t \approx 0$ 时去噪分布趋近于狄拉克 δ 函数，导致 Fisher-Rao 能量爆炸。这限制了在完全干净数据点之间直接计算测地线的能力。

2. **应用领域限制。** 过渡路径采样目前仅适用于具有已知能量函数 $U(x)$ 的分子系统（如丙氨酸二肽），此时去噪分布可写为 $p(x_0|x_t) \propto \exp(-U(x_0) - \frac{1}{2}\mathrm{SNR}(t)\|x_0 - x_t/\alpha_t\|^2)$。对于图像等没有明确能量函数的领域，过渡路径的定义和采样方法尚不明确。

3. **计算开销。** 尽管 Fisher-Rao 能量估计是仿真自由的（仅需计算去噪器的雅可比向量积，通过 Tweedie 公式和 Hutchinson 技巧实现），但测地线优化本身需要梯度下降迭代，且 DiffED 计算速度远慢于轻量级感知指标。蒸馏为快速预测网络是一个可能的加速方向。

4. **基线对比的完整性。** 部分先进基线因可重现性问题被排除，且预训练扩散模型的一次性训练成本（16M 能量评估）在评估时未计入，虽然该成本独立于生成的路径数量。

### 开放问题

- **DiffED 的蒸馏与加速：** 能否训练一个独立模型直接预测 DiffED，使其适用于实时或大规模应用？
- **采样策略改进：** 时空几何结构能否用于优化扩散模型的采样轨迹，例如设计更高效的噪声调度器？
- **跨领域过渡路径：** 对于图像、音频等无显式能量函数的领域，如何定义“过渡路径”任务？是否需要学习隐式能量函数或利用分类器引导？
- **度量学习的扩展：** Fisher-Rao 度量在度量学习、生成模型评估或模型压缩中是否有进一步应用？
- **与其他生成模型的兼容性：** 时空几何框架是否可扩展到基于流的模型或其他生成范式？指数族结构在这些模型中是否存在对应物？



## 原文 PDF

![[paperPDFs/ICLR_2026/The_Spacetime_of_Diffusion_Models_An_Information_Geometry_Perspective.pdf]]

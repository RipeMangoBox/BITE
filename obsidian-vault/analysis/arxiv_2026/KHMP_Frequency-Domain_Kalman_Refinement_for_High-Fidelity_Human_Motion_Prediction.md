---
title: "KHMP: Frequency-Domain Kalman Refinement for High-Fidelity Human Motion Prediction"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/KHMP_Frequency-Domain_Kalman_Refinement_for_High-Fidelity_Human_Motion_Prediction.pdf
project_link: https://github.com/wenhanwu95/KHMP-Project-Page.git
code_link: null
aliases:
- KHMP
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在 DCT 频域对高频系数序列应用递归卡尔曼滤波，并通过估计的 SNR 动态调节滤波噪声参数。
primary_logic: 将高频 DCT 系数建模为频率索引的一阶高斯-马尔可夫过程，利用 SNR 驱动的自适应卡尔曼滤波选择性地抑制抖动同时保留运动细节。
claims:
- 在 HumanEva-I 数据集上，KHMP 取得了 ADE 0.188、FDE 0.204、MMADE 0.301 的领先结果，同时保持 APD 7.481 的高多样性。
- 自适应卡尔曼滤波器相较固定参数滤波器能够更显著地降低误差指标。
- 通过引入物理约束和卡尔曼修正，基线 ADE 从 0.196 降至 0.188，且抖动平均降低 28.0%。
- HumanEva-I 上 ADE = 0.188
---

# KHMP: Frequency-Domain Kalman Refinement for High-Fidelity Human Motion Prediction

> [!tip] 核心洞察
> 将高频 DCT 系数建模为频率索引的一阶高斯-马尔可夫过程，利用 SNR 驱动的自适应卡尔曼滤波选择性地抑制抖动同时保留运动细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | KHMP：面向高保真人体运动预测的频域卡尔曼修正 |
| 英文题名 | KHMP: Frequency-Domain Kalman Refinement for High-Fidelity Human Motion Prediction |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21327) · [Project](https://github.com/wenhanwu95/KHMP-Project-Page.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | KHMP |
| Dataset | HumanEva-I, Human3.6M |

> [!tip] 效果简介
> - HumanEva-I 上，ADE 0.188 vs 0.196 (-0.008)；FDE 0.204 vs 0.211 (-0.007)；APD 7.481 vs 6.516 (+0.965)。
> - Human3.6M 上，ADE 0.349 vs 0.357 (-0.008)；FDE 0.441 vs 0.445 (-0.004)；APD 9.235 vs 8.217 (+1.018)。

## 概要

现有随机人体运动预测方法普遍缺乏频率感知的自适应抑制机制，导致生成的运动序列常伴有高频抖动与时间不连续性。针对这一瓶颈，KHMP 提出在离散余弦变换（DCT）频域对预测序列的高频系数施加递归卡尔曼滤波，并通过估计的信噪比（SNR）动态调节滤波噪声参数，从而在抑制抖动的同时保留运动细节。

核心思路是将高频 DCT 系数建模为沿频率索引的一阶高斯-马尔可夫过程，利用 SNR 驱动的自适应卡尔曼滤波实现选择性平滑。方法上，KHMP 以 VAE 生成网络为骨干，在训练阶段引入时序平滑损失与关节角度约束损失以注入生物力学先验，在推理阶段则通过自适应频域卡尔曼修正模块对原始预测进行精修。

在 HumanEva-I 和 Human3.6M 两个基准数据集上，KHMP 取得了领先的准确率（HumanEva-I 上 ADE 0.188、FDE 0.204），同时保持了较高的运动多样性（APD 7.481）。消融实验表明，物理约束训练与自适应卡尔曼修正互补，二者组合使基线 ADE 从 0.196 降至 0.188，且关节抖动平均降低 28.0%。



### 问题背景

人体运动预测旨在基于观测到的历史姿态序列，生成未来一段时间的合理运动轨迹。该任务在自动驾驶、人机交互、机器人导航和计算机动画等领域具有广泛应用。随着深度学习的发展，基于生成模型的方法已成为主流范式，其中变分自编码器（VAE）、生成对抗网络（GAN）和扩散模型等随机生成框架能够产生多样化的未来运动候选，避免了确定性方法固有的均值回归问题。

### 现有方法的瓶颈

尽管随机生成模型在运动多样性上取得了显著进展，但现有方法普遍存在一个关键缺陷：**缺乏频率感知的自适应抑制机制**。具体表现为：

1. **高频抖动**：生成的运动序列常伴随关节轨迹上的高频噪声，导致视觉上的不自然抖动。如 Fig. 1 所示，先前框架在 jogging 动作的预测中出现了明显的物理不合理性（红色圆圈标注区域）和时序不连续性（突变姿态过渡）。

2. **时序不连续性**：逐帧预测之间缺乏平滑约束，相邻帧之间可能出现不符合生物力学规律的姿态跳变。

3. **物理不合理性**：预测的关节角度可能超出人体正常的活动范围，产生解剖学上不可行的姿态。

这些问题的根源在于，现有生成模型在训练和推理阶段均未显式建模运动信号的频域特性，无法区分需要保留的运动细节与应当抑制的高频噪声。

### 本文动机

针对上述瓶颈，KHMP 提出了一种双阶段解决方案：

- **训练阶段**：在 VAE 主干网络的损失函数中注入结构化物理约束——时序平滑损失 $\mathcal{L}_{\mathrm{temporal}}$ 和关节角度约束损失 $\mathcal{L}_{\mathrm{angle}}$，从源头减少生成结果中的抖动和物理不合理性。

- **推理阶段**：引入**自适应频域卡尔曼修正模块**，将预测序列通过离散余弦变换（DCT）映射到频域，对高频系数序列应用递归卡尔曼滤波。核心创新在于：将高频 DCT 系数建模为沿频率索引的一阶高斯-马尔可夫过程，并通过估计的信噪比（SNR）动态调节滤波器的过程噪声 $Q$ 和观测噪声 $R$，实现对抖动信号的选择性抑制——对低 SNR 的含噪序列施加强平滑，对高 SNR 的干净序列保守保留细节。

这种“物理先验训练 + 频域自适应修正”的组合策略，使 KHMP 能够在保持高运动多样性的同时，显著提升预测的时序平滑性和物理合理性。



## 核心方法与创新机理

KHMP 的核心创新在于将**频域自适应卡尔曼滤波**引入随机人体运动预测管线，形成“生成—精修”两阶段框架。其关键洞察是：现有随机生成方法（如 VAE）虽能产生多样化预测，但缺乏频率感知的抑制机制，导致高频抖动和时序不连续性。KHMP 通过三个紧密耦合的 changed slots 系统性解决了这一问题。

### 1. 训练时物理约束注入

在 VAE 主干（**SLD-HMP** 重实现）的训练阶段，KHMP 额外引入两项结构化物理损失，从源头上抑制不合理的运动模式：

- **时序平滑损失** $\mathcal{L}_{\mathrm{temporal}}$：惩罚相邻帧之间的位移方差，促进预测序列的时序连续性（Eq. 10）。
- **关节角度约束损失** $\mathcal{L}_{\mathrm{angle}}$：通过余弦值的软惩罚确保关节角度落在生物力学合理范围内，仅在超出预设阈值时激活（Eq. 11, Eq. 55）。

训练总目标为三项损失的加权组合（Eq. 12），权重配置详见 Table 3。消融实验（Table 2b）证实，$\mathcal{L}_{\mathrm{temporal}}$ 和 $\mathcal{L}_{\mathrm{angle}}$ 各自独立提升预测质量，二者联合效果最优。

### 2. 推理时频域卡尔曼修正

推理阶段的核心贡献是一个与生成模型解耦的**自适应频域卡尔曼修正模块**（Sec. 4.3, Algorithm 1）。其工作原理如下：

1. **DCT 变换**：将 VAE 主干生成的预测序列变换到频域，得到 DCT 系数序列。
2. **频域状态空间建模**：将高频 DCT 系数沿频率索引 $k$ 建模为一阶高斯-马尔可夫过程（$A=1, H=1$），其中状态转移方程 $x_k = x_{k-1} + w_k$ 和观测方程 $z_k = x_k + v_k$ 分别刻画了相邻频率分量间的平滑演化和含噪观测关系（Eq. 13–14）。
3. **递归卡尔曼滤波**：对每个频率索引 $k$ 执行预测-更新循环，利用卡尔曼增益 $K_k = \frac{P_{k|k-1}}{P_{k|k-1} + R}$ 递归地抑制高频噪声（Eq. 8–9）。
4. **IDCT 重建**：将精修后的频域系数通过逆离散余弦变换映射回时域，得到最终平滑的运动序列。

### 3. SNR 驱动的自适应滤波策略

区别于固定参数的卡尔曼滤波器，KHMP 的关键创新在于**基于估计信噪比动态调节过程噪声 $Q$ 和观测噪声 $R$**：

- **高频能量比** $\rho^{(j,d)}$ 用于估计每个关节-维度通道的噪声水平（Eq. 20）。
- **估计信噪比** $\mathrm{SNR}_{\mathrm{est}} = \frac{1 - \rho}{\rho + \epsilon}$ 由高频能量比导出（Eq. 21）。
- 过程噪声随 $\mathrm{SNR}_{\mathrm{est}}$ 降低而增大（$Q = Q_0(1 + \lambda_Q / \mathrm{SNR}_{\mathrm{est}})$，Eq. 22），观测噪声则随 $\mathrm{SNR}_{\mathrm{est}}$ 升高而降低（$R = R_0 / (1 + \lambda_R \cdot \mathrm{SNR}_{\mathrm{est}})$，Eq. 23）。

这一自适应设计的因果机制如 Fig. 6 所示：低 SNR 时滤波器行为偏向强平滑以抑制抖动，高 SNR 时则趋于细节保留。消融实验（Table 2c）直接验证了自适应策略相较固定卡尔曼滤波在所有误差指标上的显著优势。

### 4. 创新协同效应

物理约束训练与频域卡尔曼修正形成互补：前者在训练阶段注入生物力学先验，从分布层面减少不合理生成；后者在推理阶段作为后处理模块，针对性地抑制残余高频抖动。完整框架（Full KHMP）在 HumanEva-I 上取得 ADE 0.188，相较基线（ADE 0.196）降低 4.1%，同时平均抖动降低 28.0%（Table 2a, 2e）。值得注意的是，KHMP 在提升准确度的同时保持了高多样性（APD 7.481 vs 基线 6.516），表明自适应滤波并未过度平滑运动细节。



KHMP 的整体设计遵循“训练时注入物理先验、推理时频域自适应精修”的双阶段范式，其 pipeline 如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed KHMP framework. During training (left), a VAE backbone model learns with standard losses augmented by structured Physical Constraints (Sec. 4.2) for enhanced realism. During inference (right), raw predictions are processed by the Adaptive Frequency-Kalman Refinement module (Sec. 4.3). This module uses SNR-based parameter adjustments and recursive Kalman filtering to adaptively smooth high-frequency noise, yielding refined predictions*

**训练阶段**以基于 VAE 的随机人体运动预测主干网络（即 **SLD-HMP** 的重实现版本）为核心生成引擎。该主干从历史观测序列中学习运动分布，并产生初始的多样化未来运动预测。在此基础上，KHMP 在训练目标中额外引入两类结构化物理约束损失：时序平滑损失 $\mathcal{L}_{\mathrm{temporal}}$ 和关节角度约束损失 $\mathcal{L}_{\mathrm{angle}}$。前者通过惩罚相邻帧之间的位移方差来抑制时序不连续性，后者则利用余弦值的软惩罚将关节角度限制在生物力学合理范围内。最终训练目标为三者加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{base}} + \lambda_{\mathrm{temporal}} \mathcal{L}_{\mathrm{temporal}} + \lambda_{\mathrm{angle}} \mathcal{L}_{\mathrm{angle}}$$

**推理阶段**的核心创新在于自适应频域卡尔曼修正模块。该模块位于 VAE 主干之后，作为即插即用的后处理单元，其工作流程如下：

1. **DCT 变换**：将 VAE 主干生成的原始预测序列沿时间维度进行离散余弦变换（DCT），得到各关节通道 $(j, d)$ 的频域系数序列。
2. **自适应卡尔曼滤波**：对高频 DCT 系数（频率索引 $k \ge k_0$）应用递归卡尔曼滤波。该滤波器将相邻频率分量建模为一阶高斯-马尔可夫过程（$A=1, H=1$），其核心在于过程噪声协方差 $Q$ 和观测噪声协方差 $R$ 并非固定值，而是根据每个通道的估计信噪比 $\mathrm{SNR}_{\mathrm{est}}$ 动态调节——$\mathrm{SNR}_{\mathrm{est}}$ 由高频能量比 $\rho^{(j,d)}$ 导出。自适应策略使滤波器在低信噪比时施加更强平滑以抑制抖动，在高信噪比时趋于保守以保留运动细节。
3. **IDCT 反变换**：将精修后的频域系数通过逆离散余弦变换（IDCT）映射回时域，得到最终的平滑运动序列。

这一设计将生成多样性（由 VAE 主干保证）与时序保真度（由频域卡尔曼修正保证）解耦，使得两个阶段可以独立优化。消融实验证实，物理约束训练与频域卡尔曼修正互补——完整框架（Full KHMP）在 HumanEva-I 上取得最优 ADE 0.188，相较仅使用 VAE 主干的基线（ADE 0.196）有显著提升（Table 2a）。



KHMP 框架由三个核心模块构成：VAE 主干生成网络、训练时物理约束模块，以及推理时自适应频域卡尔曼修正模块。

### VAE 主干生成网络

KHMP 以 **SLD-HMP** 的 VAE 架构作为生成主干，负责从观测历史序列中学习运动分布并产生初始的多样化未来运动预测。该主干并非本文原创，KHMP 的核心贡献在于其下游的精修机制。

### 训练时物理约束模块

为从源头抑制生成结果的物理不合理性，KHMP 在训练阶段引入两类结构化物理先验损失，与基础 VAE 损失联合优化。

**时序平滑损失** $\mathcal{L}_{\mathrm{temporal}}$ 惩罚相邻帧之间的位移方差，强制预测序列的时序连续性：

$$\mathcal{L}_{\mathrm{temporal}} = \frac{1}{T' - 1} \sum_{t=2}^{T'} \| \widehat{\mathbf{Y}}_t - \widehat{\mathbf{Y}}_{t-1} \|_2^2$$

其中 $\widehat{\mathbf{Y}}_t$ 为第 $t$ 帧的预测姿态，$T'$ 为预测序列长度。

**关节角度约束损失** $\mathcal{L}_{\mathrm{angle}}$ 通过对关节角度余弦值施加软边界惩罚，确保预测姿态落在生物力学合理范围内：

$$\mathcal{L}_{\mathrm{angle}} = \frac{1}{T' \cdot N_{\mathrm{angles}}} \sum_{t=1}^{T'} \sum_{j=1}^{N_{\mathrm{angles}}} \Big[ ( \cos(\theta_{t,j}) - \cos_j^{\mathrm{max}} )^2 \cdot \mathbb{I}( \cos(\theta_{t,j}) > \cos_j^{\mathrm{max}} ) + ( \cos_j^{\mathrm{min}} - \cos(\theta_{t,j}) )^2 \cdot \mathbb{I}( \cos(\theta_{t,j}) < \cos_j^{\mathrm{min}} ) \Big]$$

其中 $\cos(\theta_{t,j})$ 通过归一化点积 $\frac{\mathbf{v}_1 \cdot \mathbf{v}_2}{\|\mathbf{v}_1\| \|\mathbf{v}_2\| + \epsilon}$ 稳定计算，$\mathbb{I}(\cdot)$ 为指示函数——仅在角度超出预设上下界时才施加二次惩罚。

**统一训练目标**为基础 VAE 损失与上述物理损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{base}} + \lambda_{\mathrm{temporal}} \mathcal{L}_{\mathrm{temporal}} + \lambda_{\mathrm{angle}} \mathcal{L}_{\mathrm{angle}}$$

### 自适应频域卡尔曼修正模块

这是 KHMP 的核心创新。推理时，VAE 生成的初始预测序列仍可能残留高频抖动。该模块将预测序列按每个关节-维度通道 $(j, d)$ 通过 DCT 变换到频域，对高频 DCT 系数序列应用递归卡尔曼滤波，再经 IDCT 还原为精修后的时域运动序列。

**频域状态空间建模**。将高频 DCT 系数沿频率索引 $k$ 建模为一阶高斯-马尔可夫过程：

$$x_k = x_{k-1} + w_k, \quad w_k \sim \mathcal{N}(0, Q)$$
$$z_k = x_k + v_k, \quad v_k \sim \mathcal{N}(0, R)$$

其中 $x_k$ 为干净的频域隐状态，$z_k$ 为 VAE 生成的含噪 DCT 系数（观测值），$Q$ 和 $R$ 分别为过程噪声和观测噪声协方差。此处状态转移矩阵 $A=1$，观测矩阵 $H=1$，对应相邻频率分量高度相关的先验假设。

**递归滤波**。卡尔曼预测步为：

$$\hat{x}_{k|k-1} = \hat{x}_{k-1|k-1}$$
$$P_{k|k-1} = P_{k-1|k-1} + Q$$

给定观测 $z_k$，更新步为：

$$K_k = \frac{P_{k|k-1}}{P_{k|k-1} + R}$$
$$\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (z_k - \hat{x}_{k|k-1})$$

其中 $K_k$ 为卡尔曼增益，决定了滤波结果在预测值与观测值之间的权衡权重。

**自适应噪声参数调节**。固定 $Q$ 和 $R$ 无法区分剧烈抖动与精细运动。KHMP 通过估计信噪比动态调节这两个参数。首先计算高频能量比：

$$\rho^{(j,d)} = \frac{\sum_{k \geq k_0} |c_k^{(j,d)}|^2}{\sum_{k=0}^{K-1} |c_k^{(j,d)}|^2 + \epsilon}$$

其中 $k_0$ 为高频起始频率索引。由此导出估计信噪比：

$$\mathrm{SNR}_{\mathrm{est}} = \frac{1 - \rho^{(j,d)}}{\rho^{(j,d)} + \epsilon}$$

然后根据 $\mathrm{SNR}_{\mathrm{est}}$ 自适应调整噪声参数：

$$Q = Q_0 \left(1 + \frac{\lambda_Q}{\mathrm{SNR}_{\mathrm{est}} + \epsilon}\right)$$
$$R = \frac{R_0}{1 + \lambda_R \cdot \mathrm{SNR}_{\mathrm{est}}}$$

其行为逻辑为：当 $\mathrm{SNR}_{\mathrm{est}}$ 较低（信号含噪严重）时，$Q$ 增大、$R$ 减小，卡尔曼增益 $K_k$ 降低，滤波器倾向强平滑；反之，当信噪比较高时，$R$ 急剧下降而 $Q$ 温和下降，增益增大，滤波器倾向保留细节。这一自适应设计使得模块能对抖动严重的预测施加更强抑制，而对已平滑的运动保守处理。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/008_Figure_6.jpg]]
*Figure 6: Behavior of adaptive Kalman filter parameters versus estimated SNR*



## 实验与关键发现

### 主实验结果

KHMP 在 HumanEva-I 和 Human3.6M 两个标准基准上均取得了领先的预测精度。Table 1 汇总了与现有方法的定量对比。在 HumanEva-I 上，KHMP 的 ADE 达到 0.188，FDE 为 0.204，MMADE 为 0.301，均优于此前最优方法；同时 APD 保持在 7.481 的高多样性水平。在 Human3.6M 上，KHMP 同样取得 ADE 0.349、FDE 0.441 的领先结果，APD 为 9.235。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison between KHMP and published state-of-the-art methods. The bold and underlined values represent the best and second-best results, respectively. * indicates our re-implementation of the baseline [30], trained with KHMP’s hyperparameters but without physical constraints (Sec. 4.2) and Frequency-Kalman refinement (Sec. 4.3)*

值得注意的是，基线模型 SLD-HMP（Baseline*）为作者在 KHMP 超参数配置下的重实现版本，ADE 为 0.196。KHMP 完整框架相较该公平基线在 ADE 上降低了 0.008，FDE 降低了 0.007，且 APD 从 6.516 提升至 7.481，表明方法在提升精度的同时并未牺牲多样性，反而有所增益。

Table 4 进一步给出了与 MotionWavelet 的专项对比。在两个数据集上，KHMP 在所有误差指标上均优于 MotionWavelet，验证了自适应频域卡尔曼修正相比小波域处理策略的优越性。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/010_Table_4.jpg]]
*Table 4: Quantitative comparison between KHMP and MotionWavelet on HumanEva-I and Human3.6M datasets. Best results are highlighted in bold*

### 消融实验

Table 2 系统拆解了 KHMP 各组件的贡献，形成一条清晰的因果链。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/004_Table_2.jpg]]
*Table 2: Comprehensive ablation studies and quantitative analysis of the KHMP framework. (a) Analysis of the full framework components. (b) Ablation on structured physical losses. (c) Comparison of Frequency-Kalman refinement strategies. (d) Fixed Frequency Suppression [29] vs. our Adaptive Frequency-Kalman Refinement on HumanEva-I. (e) Quantitative evaluation of jitter reduction*

**框架组件消融（Table 2a）**：在基线模型上逐步叠加物理约束训练和频域卡尔曼修正。仅添加物理约束（+Physical Constraints）使 ADE 从 0.196 降至 0.192；仅添加卡尔曼修正（+Kalman Refinement）使 ADE 降至 0.191。两者组合的完整框架（Full KHMP）取得最优 ADE 0.188，证明训练时物理先验与推理时频域精修的互补性。

**物理损失消融（Table 2b）**：分别考察时序平滑损失 $\mathcal{L}_{\mathrm{temporal}}$ 和关节角度约束损失 $\mathcal{L}_{\mathrm{angle}}$ 的独立贡献。单独引入任一损失均可降低 ADE 和 FDE，二者联合使用效果最佳。$\mathcal{L}_{\mathrm{temporal}}$ 主要抑制帧间抖动，$\mathcal{L}_{\mathrm{angle}}$ 则提升关节角度的解剖合理性，两者作用于不同维度的物理合理性。

**卡尔曼策略消融（Table 2c）**：对比固定参数卡尔曼滤波（Fixed Kalman）与自适应卡尔曼滤波（Adaptive Kalman）。固定卡尔曼已能带来一定改善，但自适应策略通过估计 SNR 动态调节过程噪声 $Q$ 和观测噪声 $R$，在所有误差指标上取得了更显著的降低。这验证了 SNR 驱动的自适应机制是频域修正模块的核心效能来源。

**与固定频率压制对比（Table 2d）**：将 KHMP 的自适应频域卡尔曼修正与固定频率压制策略（Fixed Frequency Suppression）进行对比，前者显著更优。固定压制无法区分信号与噪声成分，容易误伤有效运动细节；自适应滤波则根据估计 SNR 选择性抑制高频抖动，保留真实运动信息。

**抖动定量分析（Table 2e）**：KHMP 平均降低 28.0% 的关节抖动，从数值上印证了 Fig. 4 中关节轨迹的可视化效果——基线预测（红色曲线）存在明显高频抖动，而 KHMP（蓝色曲线）显著平滑且紧密贴合真值（绿色虚线）。

### 超参数敏感度

Fig. 3 展示了五个关键超参数的敏感度分析：高频阈值 $k_0$、自适应过程噪声系数 $\lambda_Q$、自适应观测噪声系数 $\lambda_R$、角度损失权重 $\lambda_{\mathrm{angle}}$ 和时序损失权重 $\lambda_{\mathrm{temporal}}$。各参数在合理区间内均表现出稳健的性能，最优值附近波动不会导致性能剧烈退化。具体权重配置见 Table 3。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/005_Figure_3.jpg]]
*Figure 3: Sensitivity analysis of hyperparameters: k0, λQ, λR*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/009_Table_3.jpg]]
*Table 3: Loss weights configuration*

### 自适应机制的行为验证

Fig. 6 揭示了自适应卡尔曼滤波参数随估计 SNR 的动态行为：当 SNR 升高（信号质量好），观测噪声 $R$ 急剧下降，过程噪声 $Q$ 温和下降，卡尔曼增益 $K_k$ 随之增大，滤波器从强平滑模式（低 SNR，噪声主导）切换至细节保持模式（高 SNR，信号主导）。这一行为曲线从机制层面解释了自适应滤波为何能选择性抑制抖动而不过度平滑。

### 失败模式与局限性

尽管 KHMP 在精度和物理合理性上取得了显著提升，仍存在以下局限：

1. **推理开销**：频域卡尔曼修正模块引入额外计算，HumanEva-I 上推理时间约为基线的 1.2 倍，Human3.6M 上约为 1.6 倍。该开销源于逐关节、逐维度的 DCT/IDCT 变换与递归滤波，尚未针对实时部署优化。
2. **多样性提升温和**：APD 的提升幅度（HumanEva-I 上 +0.965，Human3.6M 上 +1.018）相对准确度改善较为有限，精度-多样性前沿仍有优化空间。
3. **骨干网络通用性未验证**：当前仅在 VAE 主干（SLD-HMP）上验证了方法的有效性，其在扩散模型等其他生成式骨干上的迁移效果尚不明确。
4. **长期预测未探索**：实验设置聚焦于标准短期预测（400ms），该方法能否扩展到 >1000ms 的长期预测场景需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/006_Figure.jpg]]
*Figure: (a) Gesturing - Ankle: Ours vs Baseline (b) Gesturing - Upper Arm: Ours vs Baseline (c) Gesturing - Wrist: Ours vs Baseline (d) Gesturing - Shin: Ours vs Baseline (e) Walking - Ankle: Ours vs Baseline (g) Walking - Thigh: Ours vs Baseline (f) Walking - Shin: Ours vs Baseline (h) Walking - Wrist: Ours vs Baseline*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/007_Figure_5.jpg]]
*Figure 5: Visual comparison highlighting KHMP’s enhanced prediction quality over the baseline across various actions (Boxing, Jogging, Walking, and Gesturing). The figure showcases KHMP’s ability to correct physical implausibility often present in raw generative model outputs. In the examples shown, red arrows indicate issues in baseline predictions, while blue boxes highlight the corresponding smoother and more coherent KHMP results. Best viewed by zooming in. We also provide video demos in the SupMat*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2603_21327/figures/011_Figure_7.jpg]]
*Figure 7: Additional qualitative comparison between Baseline and KHMP predictions for selected frames from Jogging and Gesturing actions. Red arrows highlight implausible poses in the baseline, while blue boxes show the refined and more realistic results from KHMP*



## 定位与知识库关联

### 基线关系与继承

KHMP 直接构建在 **SLD-HMP** (论文引用编号 ) 的 VAE 主干之上。论文将 SLD-HMP 作为 Baseline* 进行了公平重实现——使用 KHMP 的超参数配置但剥离物理约束损失和频域卡尔曼修正模块，确保对照实验的可比性。从方法继承角度看，KHMP 保留了 SLD-HMP 的完整生成管线：历史运动序列编码为潜变量，再解码为多样化的未来预测。KHMP 的创新并非替换这一生成范式，而是在两个关键环节注入新机制：训练阶段引入结构化物理先验，推理阶段附加频域自适应后处理。

与同期频域修正方法 **MotionWavelet** 的对比（Table 4）表明，KHMP 在 HumanEva-I 和 Human3.6M 两个基准上均取得更优结果，验证了卡尔曼滤波框架相比小波域处理在此任务上的优势。此外，消融实验中与 **Fixed Frequency Suppression**（引用编号 ）的对比（Table 2d）进一步说明，简单的固定频率压制策略远不及 SNR 驱动的自适应卡尔曼滤波有效。

### 方法适用边界

KHMP 的设计建立在一组明确的前提假设之上，这些假设同时界定了其适用范围：

1. **生成主干依赖性**：频域卡尔曼修正模块以 VAE 生成的初始预测为前提。当前仅在 SLD-HMP 这一种 VAE 骨架上验证，尚未在扩散模型、GAN 或自回归 Transformer 等其它生成范式上测试通用性。若更换主干，修正模块的有效性需重新评估。

2. **DCT 频域假设**：自适应滤波的核心操作在 DCT 域完成，依赖“高频系数对应时序抖动”这一频谱特性。对于本身频谱特征不同的运动类型（如极高频率的震颤动作或极低频率的缓慢漂移），高频能量比 $\rho^{(j,d)}$ 作为 SNR 估计代理的有效性可能下降。

3. **短时预测场景**：当前实验聚焦于标准的人体运动预测基准（HumanEva-I 和 Human3.6M），预测时长通常在 400-1000ms 范围内。论文明确将“扩展到长期预测（>1000ms）”列为开放问题，暗示现有框架在更长时域上可能出现误差累积或平滑过度。

4. **单模态运动数据**：方法在 3D 人体骨架序列上验证，关节角度约束损失 $\mathcal{L}_{\mathrm{angle}}$ 依赖预定义的解剖学角度范围。扩展到非人体运动（如动物、机械臂）或包含交互物体的场景时，物理约束需要重新设计。

### 已知局限

论文在实验分析中明确指出了三个层面的局限：

**计算开销**：推理时的频域卡尔曼修正引入可测量的延迟。在 HumanEva-I 上约为 1.2 倍推理时间，在 Human3.6M 上约为 1.6 倍。这一开销源于对每个关节-维度通道 $(j,d)$ 独立执行 DCT、递归滤波和 IDCT 操作。对于需要实时部署的应用场景（如在线人机交互），当前未经优化的实现可能构成瓶颈。

**多样性-准确性权衡**：虽然 KHMP 在准确性指标（ADE、FDE、MMADE）上持续优于基线，但多样性指标 APD 的提升相对温和（HumanEva-I 上从 6.516 升至 7.481，Human3.6M 上从 8.217 升至 9.235）。这表明自适应卡尔曼滤波在抑制高频抖动的同时，可能也轻微削弱了生成样本的模态多样性。如何在平滑与多样性之间取得更优平衡，仍是待解问题。

**架构通用性未验证**：如适用边界中所述，修正模块仅在 VAE 骨架上验证。扩散模型等新型生成骨干近年来在运动生成领域展现出强大能力，KHMP 的频域卡尔曼修正是否能无缝迁移到这些框架中，目前缺乏实验证据。

### 开放问题

论文在讨论部分明确提出了四个开放方向：

1. **联合优化预测质量与多样性**：当前框架将准确性提升（通过物理约束和卡尔曼修正）与多样性保持（通过 VAE 随机采样）作为两个相对独立的机制。是否存在端到端的联合优化策略，使两者同时获益而非相互制约？

2. **降低计算开销以实现实时部署**：推理延迟主要来自逐通道的频域变换和递归滤波。通过选择性修正（仅对抖动显著的通道应用卡尔曼滤波）或并行化频域操作，有望将开销压缩到可接受范围。论文将此列为明确的工程优化方向。

3. **推广至扩散模型等其它生成骨干**：扩散模型的去噪过程本身具有频域特性。将自适应频域卡尔曼修正的思想嵌入扩散模型的去噪步骤中，可能带来更紧密的集成而非当前的后处理范式。这一方向需要重新设计状态转移模型和 SNR 估计策略。

4. **扩展至长期预测场景**：当预测时长超过 1000ms 时，误差累积效应加剧，卡尔曼滤波的递归结构可能放大而非抑制漂移。长期预测可能需要引入额外的全局一致性约束或分层频域处理策略。

### 知识库定位

在人体运动预测的方法谱系中，KHMP 占据了一个独特的位置：它不属于端到端生成模型的创新（如新的网络架构或训练范式），也不属于纯后处理平滑方法（如高斯滤波或样条插值），而是在**生成模型与信号处理之间建立了自适应接口**。其核心贡献——将 DCT 高频系数建模为频率索引的一阶高斯-马尔可夫过程，并用估计 SNR 驱动卡尔曼滤波参数——在现有文献中未见先例。

从更广的视角看，KHMP 代表了一类“生成-精修”混合范式：生成模型负责多样性和全局结构，信号处理方法负责局部时序一致性。这一范式与扩散模型中的“去噪-引导”策略有概念上的亲缘性，但 KHMP 在频域操作的递归滤波机制提供了不同的精度-效率权衡点。



## 原文 PDF

![[paperPDFs/arxiv_2026/KHMP_Frequency-Domain_Kalman_Refinement_for_High-Fidelity_Human_Motion_Prediction.pdf]]

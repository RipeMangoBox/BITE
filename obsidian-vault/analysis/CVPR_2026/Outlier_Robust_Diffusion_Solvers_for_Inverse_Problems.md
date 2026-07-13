---
title: Outlier-Robust Diffusion Solvers for Inverse Problems
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Outlier_Robust_Diffusion_Solvers_for_Inverse_Problems.pdf
project_link: null
code_link: null
aliases:
- RGRC
- ORDSIP
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 测量中的离群污染（arbitrary corruption model）与加性高斯噪声的耦合，以及保真项形式
primary_logic: 将平方ℓ2保真项替换为元素级Huber损失，并显式估计加性噪声以修正测量，从而构建对离群点鲁棒的优化目标；进一步用共轭梯度法替代梯度下降，避免学习率调参。
claims:
- Huber损失替代ℓ2保真项使Robust-GD/Robust-CG在离群污染下大幅优于所有基线
- 显式噪声估计与Huber损失结合在两个基线（DPS、DiffPIR）上均提升性能，证明组件有效性
- CelebA 256×256 Gaussian deblurring, σ=0.05, ρ=0.02 上 PSNR↑ = 29.38±1.78 (Robust-CG), 29.27±1.68 (Robust-GD)
- CelebA 256×256 Inpainting (random 70%), σ=0.05, ρ=0.10 上 PSNR↑ = 31.20 (Robust-CG)
---

# Outlier-Robust Diffusion Solvers for Inverse Problems

> [!tip] 核心洞察
> 将平方ℓ2保真项替换为元素级Huber损失，并显式估计加性噪声以修正测量，从而构建对离群点鲁棒的优化目标；进一步用共轭梯度法替代梯度下降，避免学习率调参。

| 字段 | 内容 |
|------|------|
| 中文题名 | 对离群值鲁棒的扩散模型逆问题求解器 |
| 英文题名 | Outlier-Robust Diffusion Solvers for Inverse Problems |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.09477) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Robust-GD / Robust-CG |
| Dataset | CelebA 256×256 Gaussian deblurring, σ=0.05, ρ=0.02, CelebA 256×256 Inpainting (random 70%), σ=0.05, ρ=0.10 |

> [!tip] 效果简介
> - CelebA 256×256 Gaussian deblurring, σ=0.05, ρ=0.02 上，PSNR↑ 29.38±1.78 (Robust-CG), 29.27±1.68 (Robust-GD) vs 22.06 (DPS) (+7.32 (Robust-CG vs DPS))。
> - CelebA 256×256 Inpainting (random 70%), σ=0.05, ρ=0.10 上，PSNR↑ 31.20 (Robust-CG) vs 15.60±1.94 (DAPS) (+15.60)。

## 概要

基于扩散模型的逆问题求解器在图像修复、超分辨率等任务中取得了显著进展，但现有方法普遍依赖平方ℓ₂保真项（即 $\|\mathbf{y} - \mathcal{A}(\bar{\mathbf{x}}_0)\|_2^2$），对测量中的离群值（outliers）高度敏感。当观测数据以概率 $\rho$ 被任意值替换时，平方损失会因少数大幅偏离的残差而严重扭曲优化方向，导致重建质量急剧退化。这一瓶颈在真实场景中尤为突出——传感器故障、传输错误或对抗干扰都可能引入此类离群污染。

本文的核心洞察是：将平方ℓ₂保真项替换为**元素级Huber损失**，并**显式估计加性噪声以修正测量**，可以构建对离群值鲁棒的优化目标。Huber损失在残差较小时表现为二次函数，在大幅偏离时退化为线性，从而自动抑制离群点的影响；而噪声估计则进一步将测量中的高斯噪声与离群污染解耦，为后续保真项提供更干净的修正测量 $\bar{\mathbf{y}}$。

基于这一框架，作者提出了两种求解器：**Robust-GD** 采用梯度下降近似求解鲁棒优化问题；**Robust-CG** 则引入共轭梯度法，利用 Fletcher-Reeves 公式计算搜索方向，并通过闭式步长（线性算子）或有限差分近似（非线性算子）避免学习率调参。

实验覆盖线性逆问题（超分辨率、随机修复、高斯/运动去模糊）和非线性去模糊，在 CelebA、FFHQ、ImageNet 三个数据集上验证。在典型设置下（高斯噪声 $\sigma=0.05$，污染率 $\rho=0.02$），Robust-CG 在 CelebA 高斯去模糊任务上达到 **29.38 dB PSNR**，比 DPS 的 22.06 dB 高出 **7.32 dB**；在随机修复任务（$\rho=0.10$）上达到 **31.20 dB**，比 DAPS 的 15.60 dB 高出 **15.60 dB**。消融实验进一步证实：将显式噪声估计与 Huber 损失嵌入 DPS 和 DiffPIR 后，Robust-DPS 与 Robust-DiffPIR 均显著优于原始基线，验证了核心组件的独立有效性。



### 扩散模型求解逆问题的基本范式

逆问题旨在从含噪观测 $\pmb{y}$ 中恢复未知信号 $\pmb{x}_0^*$，其标准观测模型为：

$$\pmb{y} = \mathcal{A}(\pmb{x}_0^*) + \pmb{\nu}$$

其中 $\mathcal{A}$ 为前向测量算子（可为线性或非线性），$\pmb{\nu}$ 为加性高斯噪声。近年来，基于扩散模型的逆问题求解器（如 **DPS**、**DiffPIR**、**DCPS**、**RED-diff**、**DAPS** 等）在该领域取得了显著进展，其核心思路是利用预训练扩散模型中的先验知识，在采样过程中通过数据保真项将测量信息注入去噪过程，从而引导生成与观测一致的重建结果。

### 离群污染的挑战

然而，现有方法普遍隐含假设测量噪声服从独立同分布的高斯分布，并采用平方 $\ell_2$ 保真项 $\|\pmb{y} - \mathcal{A}(\bar{\pmb{x}}_0)\|_2^2$ 来度量数据一致性。这一设计在实际场景中存在严重脆弱性：当测量中包含离群值（outliers）时，平方 $\ell_2$ 损失对大幅偏离的异常点极为敏感，导致梯度被少数污染元素主导，重建质量急剧退化。

本文考虑的离群污染模型为任意元素污染模型（arbitrary corruption model）：

$$y_i = \begin{cases} \xi_i, & \text{if } i \in \mathcal{C} \\ (\mathcal{A}(\mathbf{x}_0^*))_i + \nu_i, & \text{if } i \notin \mathcal{C} \end{cases}$$

即每个测量元素以概率 $\rho$ 被替换为任意值 $\xi_i$，其余元素仍服从标准加性高斯噪声。这种污染模式广泛存在于传感器故障、传输错误或对抗攻击等实际场景中，但现有扩散模型逆方法均未专门处理此类离群污染。

### 现有方法的根本缺陷

从因果机制分析，现有方法的退化源于两个耦合因素：

1. **保真项形式不当**：平方 $\ell_2$ 损失对残差施加二次惩罚，离群点产生的巨大残差会不成比例地放大梯度贡献，使优化方向偏离真实解；
2. **噪声与离群未解耦**：现有方法未显式区分加性高斯噪声与离群污染，导致测量中的离群值被误作为高噪声处理，进一步加剧了重建偏差。

因此，核心瓶颈在于：如何在扩散采样框架下构建对离群点鲁棒的优化目标，同时保持对高斯噪声的有效抑制。



## 核心方法与创新机理

### 瓶颈分析：ℓ₂ 保真项在离群污染下的脆弱性

现有基于扩散模型的逆问题求解器（如 **DPS**、**DiffPIR**、**DCPS**、**RED-diff**、**DAPS** 等）在标准加性高斯噪声设定下表现优异，但其核心数据保真项普遍采用平方 ℓ₂ 范数形式：

$$ \min_{\bar{\boldsymbol{x}}_0} \frac{1}{2 r_t^2} \|\bar{\boldsymbol{x}}_0 - \hat{\boldsymbol{x}}_0(\tilde{\boldsymbol{x}}_t, t)\|_2^2 + \frac{1}{2\gamma_t^2} \|\boldsymbol{y} - \mathcal{A}(\bar{\boldsymbol{x}}_0)\|_2^2 $$

当测量 $\boldsymbol{y}$ 中混入离群值（arbitrary corruption）时，平方 ℓ₂ 损失对大幅偏离的残差项施加二次惩罚，导致梯度被少数污染元素主导，信号估计严重退化。实验证据表明，在 CelebA 256×256 高斯去模糊任务中（σ=0.05，污染率 ρ=0.02），**DPS** 的 PSNR 仅为 22.06 dB，而本文方法可达 29.27–29.38 dB（表 2 / 表 13），差距超过 7 dB——这直接印证了 ℓ₂ 保真项是该场景下的核心脆弱点。

### Changed Slot 1：从平方 ℓ₂ 到 Huber 损失的保真项重构

本文的关键创新在于将数据保真项从平方 ℓ₂ 损失替换为**元素级 Huber 损失**，并辅以**显式噪声估计**来修正测量。观测模型为：

$$ \boldsymbol{y} = \mathcal{A}(\boldsymbol{x}_0^*) + \boldsymbol{\nu} $$

其中离群污染模型为：以概率 ρ 将第 i 个测量元素 $y_i$ 替换为任意值 $\xi_i$，否则为正常含噪测量。Huber 损失定义为：

$$ \mathcal{H}_{\delta}(r) = \begin{cases} r^2, & \text{if } |r| \le \delta, \\\\ 2\delta|r| - \delta^2, & \text{if } |r| > \delta. \end{cases} $$

其核心机制在于：当残差 $|r| \le \delta$ 时保持二次增长（对正常噪声敏感），当 $|r| > \delta$ 时切换为线性增长（对离群值不敏感），从而在优化过程中自动抑制离群元素的梯度贡献。通过将 Huber 损失表达为迭代重加权最小二乘（IRLS）形式：

$$ \min_{\bar{\boldsymbol{x}}_0} \frac{1}{2} \left( \frac{1}{r_t^2} \|\bar{\boldsymbol{x}}_0 - \hat{\boldsymbol{x}}_0(\tilde{\boldsymbol{x}}_t, t)\|_2^2 + \frac{1}{\gamma_t^2} \|\boldsymbol{W}_{\delta}(\bar{\boldsymbol{y}} - \boldsymbol{A}(\bar{\boldsymbol{x}}_0))\|_2^2 \right) $$

其中权重矩阵 $\boldsymbol{W}_{\delta}$ 根据当前残差动态调整，大残差元素获得小权重。这一设计使得优化目标在每次迭代中保持二次形式，便于高效求解。

**显式噪声估计**作为配套组件，通过引入噪声变量 $\bar{\boldsymbol{\nu}}$ 并求解联合优化问题：

$$ \min_{\bar{\boldsymbol{x}}_0, \bar{\boldsymbol{\nu}}} \frac{1}{2 r_t^2} \|\bar{\boldsymbol{x}}_0 - \hat{\boldsymbol{x}}_0(\bar{\boldsymbol{x}}_t, t)\|_2^2 + \frac{1}{2\sigma^2} \|\bar{\boldsymbol{\nu}}\|_2^2 + \frac{1}{2\gamma_t^2} \|\boldsymbol{y} - \mathcal{A}(\bar{\boldsymbol{x}}_0) - \bar{\boldsymbol{\nu}}\|_2^2 $$

得到噪声的闭式估计：

$$ \tilde{\boldsymbol{\nu}} = \frac{\sigma^2}{\gamma_t^2 + \sigma^2} \left( \boldsymbol{y} - \mathcal{A}(\hat{\boldsymbol{x}}_0(\tilde{\boldsymbol{x}}_t, t)) \right) $$

进而将测量修正为 $\bar{\boldsymbol{y}} = \frac{1}{\gamma_t^2 + \sigma^2} (\gamma_t^2 \boldsymbol{y} + \sigma^2 \mathcal{A}(\hat{\boldsymbol{x}}_0(\tilde{\boldsymbol{x}}_t, t)))$，有效剥离了加性噪声对保真项计算的干扰。消融实验（表 13）证实，将显式噪声估计与 Huber 损失嵌入 **DPS** 和 **DiffPIR** 后，**Robust-DPS** 与 **Robust-DiffPIR** 均显著优于原始基线，验证了两个组件的独立贡献。

### Changed Slot 2：从梯度下降到共轭梯度法的优化器升级

**Robust-GD** 直接对式 (17) 执行梯度下降，但实验表明其性能对学习率 $\eta_x$ 高度敏感——同一任务下 PSNR 可从 16.20 dB 波动至 28.29 dB（表 11），需要精细调参。

**Robust-CG** 将优化器替换为共轭梯度法，从根本上规避了学习率调参问题。对于线性前向算子 $\mathcal{A}(\boldsymbol{x}) = \boldsymbol{A}\boldsymbol{x}$，目标函数为二次型，CG 方法可通过线搜索获得闭式最优步长：

$$ \alpha_j = \frac{\boldsymbol{g}_j^{\mathrm{T}} \boldsymbol{g}_j}{\frac{1}{r_t^2} \boldsymbol{d}_j^{\mathrm{T}} \boldsymbol{d}_j + \frac{1}{\gamma_t^2} (\boldsymbol{W}_{\delta}^{(j)} \boldsymbol{A} \boldsymbol{d}_j)^{\mathrm{T}} (\boldsymbol{W}_{\delta}^{(j)} \boldsymbol{A} \boldsymbol{d}_j)} $$

其中 $\boldsymbol{g}_j$ 为当前梯度，$\boldsymbol{d}_j$ 为共轭方向，Fletcher-Reeves 公式用于方向更新。对于非线性前向算子，则通过有限差分近似 Jacobian 向量积来计算步长。这一设计使 Robust-CG 在保持鲁棒性的同时免除了学习率的手动调节，且 PSNR-计算成本权衡（图 6）显示其在效率上具备竞争力。

### 创新总结

两项 changed slot 形成因果闭环：**Huber 损失 + 显式噪声估计**解决了“保真项对离群值敏感”的瓶颈，**共轭梯度法**解决了“梯度下降对学习率敏感”的工程瓶颈。两者的结合使得方法在离群污染场景下（ρ=0.02–0.10）相比现有 DM 逆问题求解器获得 5–15 dB 的 PSNR 增益，且 Huber 阈值 δ 在 $\{0.005, 0.01, 0.02, 0.04\}$ 范围内性能波动小于 0.5 dB（表 10），表现出良好的参数鲁棒性。



本文提出的 Robust-GD 与 Robust-CG 方法在扩散模型逆问题求解的通用流程中插入了两个关键模块：**显式噪声估计**与**鲁棒目标函数构建**，从而在测量包含离群污染时保持重建质量。整体 pipeline 如图 1 所示，每个时间步 $t_i$ 的处理流程如下：

1. **信号估计**：利用预训练扩散模型的数据预测网络 $x_\theta$，从当前带噪潜变量 $\tilde{\mathbf{x}}_t$ 估计干净信号 $\hat{\mathbf{x}}_0(\tilde{\mathbf{x}}_t, t)$。
2. **显式噪声估计与测量修正**：将加性噪声 $\nu$ 作为显式优化变量，与信号联合估计，得到噪声的闭式解 $\tilde{\nu}$，进而将原始测量 $\mathbf{y}$ 修正为 $\bar{\mathbf{y}}$。
3. **鲁棒目标函数构建**：将标准平方 $\ell_2$ 保真项替换为元素级 Huber 损失，并表达为迭代重加权最小二乘形式，形成对离群点不敏感的目标函数。
4. **迭代求解**：对鲁棒目标函数执行梯度下降（Robust‑GD）或共轭梯度法（Robust‑CG），更新信号估计 $\bar{\mathbf{x}}_0$。在每步迭代中，权重矩阵 $\mathbf{W}_\delta$ 根据当前残差动态更新。
5. **采样推进**：利用更新后的 $\bar{\mathbf{x}}_0$ 计算下一个时间步的潜变量 $\tilde{\mathbf{x}}_{t_{i-1}}$，重复上述过程直至完成采样。

**模块间关系**：显式噪声估计模块为后续鲁棒目标函数提供了更干净的测量 $\bar{\mathbf{y}}$，降低了噪声与离群值的耦合干扰；Huber 损失模块通过自适应权重矩阵 $\mathbf{W}_\delta$ 抑制大幅偏离的残差元素，使得梯度更新不被离群点主导。两个模块可独立嵌入现有扩散逆问题求解器（如 DPS、DiffPIR），形成 Robust‑DPS 与 Robust‑DiffPIR，消融实验（表 13）证实了各组件对性能提升的独立贡献。

**Robust‑GD 与 Robust‑CG 的差异**：两者共享相同的鲁棒目标函数，区别在于求解器。Robust‑GD 使用梯度下降，需手动调节学习率 $\eta_x$，对学习率高度敏感（表 11 显示同一任务 PSNR 可从 16.20 变化至 28.29）。Robust‑CG 采用共轭梯度法，通过线搜索自动确定步长——线性前向算子下具有闭式解，非线性场景则通过有限差分近似 Jacobian‑向量积，完全避免了学习率调参问题。

### 补充图表

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our proposed Robust-GD and Robust-CG methods. At each timestep*



### 3.1 观测模型与离群污染建模

本文考虑的逆问题观测模型为加性高斯噪声形式：

$$
\pmb{y} = \pmb{\mathcal{A}}(\pmb{x}_0^*) + \pmb{\nu}
$$

其中 $\pmb{x}_0^*$ 为真实信号，$\pmb{\mathcal{A}}$ 为前向算子（可为线性或非线性），$\pmb{\nu} \sim \mathcal{N}(0, \sigma^2 \mathbf{I})$ 为加性高斯噪声。在此基础上引入**任意离群污染模型**（arbitrary corruption model）：

$$
y_i = \begin{cases}
\xi_i, & \text{if } i \in \mathcal{C} \\[4pt]
(\mathcal{A}(\mathbf{x}_0^*))_i + \nu_i, & \text{if } i \notin \mathcal{C}
\end{cases}
$$

其中 $\mathcal{C}$ 为随机选取的污染索引集，污染比例 $\rho = |\mathcal{C}|/m$，$\xi_i$ 为任意离群值。该模型刻画了测量中部分元素被完全替换为异常值的场景，是现有扩散模型逆问题方法（依赖平方 $\ell_2$ 保真项）严重退化的根本原因。

### 3.2 显式噪声估计与测量修正

标准扩散模型求解器在每步去噪时优化如下目标（以 $\hat{\pmb{x}}_0(\tilde{\pmb{x}}_t, t)$ 表示从带噪潜变量 $\tilde{\pmb{x}}_t$ 估计的干净信号）：

$$
\min_{\bar{\pmb{x}}_0} \frac{1}{2 r_t^2} \|\bar{\pmb{x}}_0 - \hat{\pmb{x}}_0(\tilde{\pmb{x}}_t, t)\|_2^2 + \frac{1}{2 \gamma_t^2} \|\pmb{y} - \mathcal{A}(\bar{\pmb{x}}_0)\|_2^2
$$

其中 $r_t$、$\gamma_t$ 为与扩散调度相关的系数。为缓解加性噪声与离群值的耦合影响，本文引入显式噪声变量 $\bar{\pmb{\nu}}$，构建**联合信号与噪声估计**问题：

$$
\min_{\bar{\pmb{x}}_0, \bar{\pmb{\nu}}} \frac{1}{2 r_t^2} \|\bar{\pmb{x}}_0 - \hat{\pmb{x}}_0(\tilde{\pmb{x}}_t, t)\|_2^2 + \frac{1}{2\sigma^2} \|\bar{\pmb{\nu}}\|_2^2 + \frac{1}{2\gamma_t^2} \|\pmb{y} - \mathcal{A}(\bar{\pmb{x}}_0) - \bar{\pmb{\nu}}\|_2^2
$$

对 $\bar{\pmb{\nu}}$ 求闭式解可得噪声估计：

$$
\tilde{\pmb{\nu}} = \frac{\sigma^2}{\gamma_t^2 + \sigma^2} \left( \pmb{y} - \mathcal{A}(\hat{\pmb{x}}_0(\tilde{\pmb{x}}_t, t)) \right)
$$

将 $\tilde{\pmb{\nu}}$ 代回原问题，得到**修正测量** $\bar{\pmb{y}}$：

$$
\bar{\pmb{y}} = \frac{1}{\gamma_t^2 + \sigma^2} \left( \gamma_t^2 \pmb{y} + \sigma^2 \mathcal{A}(\hat{\pmb{x}}_0(\tilde{\pmb{x}}_t, t)) \right)
$$

修正后的测量 $\bar{\pmb{y}}$ 是原始测量 $\pmb{y}$ 与当前信号估计经前向算子投影的加权平均，权重由噪声方差 $\sigma^2$ 和调度参数 $\gamma_t^2$ 决定——当 $\sigma^2$ 较大时更信赖模型预测。

### 3.3 基于 Huber 损失的鲁棒目标函数

平方 $\ell_2$ 保真项对大幅偏离的离群点高度敏感。本文将其替换为**元素级 Huber 损失**：

$$
\mathcal{H}_\delta(r) = \begin{cases}
r^2, & \text{if } |r| \le \delta, \\[4pt]
2\delta |r| - \delta^2, & \text{if } |r| > \delta.
\end{cases}
$$

对残差向量 $\bar{\pmb{y}} - \mathcal{A}(\bar{\pmb{x}}_0)$ 逐元素施加 Huber 损失：

$$
\mathcal{H}_\delta(\bar{\pmb{y}} - \mathcal{A}(\bar{\pmb{x}}_0)) = \sum_{i=1}^{m} \mathcal{H}_\delta((\bar{\pmb{y}} - \mathcal{A}(\bar{\pmb{x}}_0))_i)
$$

为便于优化，将 Huber 损失改写为**迭代重加权最小二乘**（IRLS）二次形式。引入对角权重矩阵 $\mathbf{W}_\delta$，其对角元为：

$$
(\mathbf{W}_\delta)_{ii} = \begin{cases}
1, & |r_i| \le \delta \\[4pt]
\sqrt{2\delta / |r_i|}, & |r_i| > \delta
\end{cases}
$$

使得 $\|\mathbf{W}_\delta(\bar{\pmb{y}} - \mathcal{A}(\bar{\pmb{x}}_0))\|_2^2$ 与原始 Huber 损失共享相同梯度。最终**鲁棒目标函数**为：

$$
\min_{\bar{\pmb{x}}_0} \frac{1}{2} \left( \frac{1}{r_t^2} \|\bar{\pmb{x}}_0 - \hat{\pmb{x}}_0(\tilde{\pmb{x}}_t, t)\|_2^2 + \frac{1}{\gamma_t^2} \| \mathbf{W}_\delta (\bar{\pmb{y}} - \mathcal{A}(\bar{\pmb{x}}_0)) \|_2^2 \right)
$$

该目标中，$\mathbf{W}_\delta$ 对残差大的元素自动降权，抑制离群值对梯度方向的扭曲。

### 3.4 梯度下降与共轭梯度求解

**Robust-GD** 直接对上述目标执行梯度下降，每步更新权重矩阵 $\mathbf{W}_\delta$（见算法 1）。然而，梯度下降对学习率 $\eta_x$ 高度敏感——消融实验（表 11）表明同一任务 PSNR 可从 16.20 变化至 28.29。

**Robust-CG** 改用共轭梯度法避免学习率调参。当 $\mathcal{A}$ 为线性算子时，目标函数是 $\bar{\pmb{x}}_0$ 的二次型，可求得闭式最优步长：

$$
\alpha_j = \frac{g_j^{\mathrm{T}} g_j}{\frac{1}{r_t^2} d_j^{\mathrm{T}} d_j + \frac{1}{\gamma_t^2} (\mathbf{W}_\delta^{(j)} \mathbf{A} d_j)^{\mathrm{T}} (\mathbf{W}_\delta^{(j)} \mathbf{A} d_j)}
$$

其中 $g_j$ 为当前梯度，$d_j$ 为共轭方向（由 Fletcher-Reeves 公式更新），$\mathbf{W}_\delta^{(j)}$ 为第 $j$ 次 CG 迭代的权重矩阵。对于非线性前向算子，通过有限差分近似 Jacobian-向量积 $\mathbf{W}_\delta \mathbf{A} d_j$，以微小精度代价换取无需学习率调参的便利（见算法 2）。

### 3.5 模块化嵌入验证

为验证各组件可独立迁移，本文将显式噪声估计与 Huber 损失嵌入到两个代表性基线中，得到 **Robust-DPS** 和 **Robust-DiffPIR**。消融结果（表 13）表明，在 CelebA Gaussian deblurring（$\rho=0.10$）任务上，Robust-DPS 达到 27.70 PSNR 而原始 DPS 仅 22.06，证明两个核心模块均对性能提升有独立贡献。



## 实验与关键发现

### 主要结果：离群污染下的鲁棒重建

实验在三个预训练扩散模型（CelebA 256×256、FFHQ 256×256、ImageNet 256×256）上评估，覆盖线性逆问题（4×超分辨率、随机70%掩码修复、高斯去模糊、运动去模糊）和非线性去模糊。所有方法使用统一采样步数（100步DDIM）和NFE预算，离群值按式(2)的arbitrary corruption model注入，污染率ρ∈{0.02, 0.10, 0.30}，加性高斯噪声σ=0.05或0.5。

**线性去模糊**是离群敏感度最高的任务。在CelebA高斯去模糊（σ=0.05, ρ=0.02）上，Robust-CG达到29.38±1.78 PSNR，Robust-GD达到29.27±1.68，而DPS仅22.06，提升超过7 dB（表2）。当污染率升至ρ=0.10时，DPS降至19.36，Robust-CG仍保持27.79，差距扩大至8.43 dB。运动去模糊趋势一致：ρ=0.10时Robust-CG为26.40，DPS为21.22。

**图像修复**任务中离群污染的破坏力更强。CelebA随机70%修复（σ=0.05, ρ=0.10）下，Robust-CG取得31.20 PSNR，而DAPS仅15.60±1.94，差距达15.60 dB（表1）。DiffPIR和DCPS等基线在此设置下同样崩溃，PSNR均低于17。这是因为修复任务中测量维度高（70%像素被掩码），离群值直接污染大量观测，平方ℓ₂保真项将大幅残差反向传播至重建，导致严重伪影。

**超分辨率**任务下离群影响相对温和。CelebA 4×超分（σ=0.05, ρ=0.10）中Robust-CG为29.23，DPS为25.58，差距约3.65 dB（表1）。这是因为超分的降采样算子本身具有平滑效应，离群值经双三次下采样后能量分散，单个离群像素的破坏力被稀释。

**非线性去模糊**场景（表3）验证了方法的泛化能力。Robust-CG在非线性高斯去模糊（σ=0.05, ρ=0.10）上取得27.61 PSNR，而DPS仅20.53。由于非线性前向算子需通过有限差分近似Jacobian，Robust-CG的闭式步长公式不再严格成立，但共轭梯度框架仍能通过线搜索找到合适步长，避免了Robust-GD对学习率的手动调参。

**高噪声场景**（σ=0.5, 表4）进一步验证鲁棒性。当噪声水平提升10倍，Robust-CG在CelebA修复（ρ=0.10）上保持27.38 PSNR，DPS降至18.51。显式噪声估计模块在此场景下作用关键：式(10)-(11)的闭式解将噪声方差σ²显式纳入测量修正，使得高噪声下的修正测量ȳ更接近真实信号。

### 消融实验：组件贡献与超参数敏感性

**显式噪声估计与Huber损失的独立贡献**（表13）。将两个核心组件分别嵌入DPS和DiffPIR基线：Robust-DPS（仅加入显式噪声估计和Huber损失）在CelebA高斯去模糊（ρ=0.10）上达到27.70，相比DPS的22.06提升5.64 dB；Robust-DiffPIR达到28.13，相比DiffPIR的21.68提升6.45 dB。这表明组件具有可迁移性，并非仅在与Robust-GD/CG耦合时才有效。

**Huber损失阈值δ的鲁棒性**（表10）。Robust-CG在δ∈{0.005, 0.01, 0.02, 0.04}范围内，CelebA高斯去模糊PSNR波动小于0.5 dB，运动去模糊波动小于0.3 dB。这是因为Huber损失在|r|≤δ时退化为ℓ₂损失（保留对正常残差的效率），在|r|>δ时退化为ℓ₁损失（抑制离群梯度），阈值仅决定切换点，不改变渐近行为。

**Robust-GD对学习率的敏感性**（表11）。同一CelebA高斯去模糊任务下，学习率η_x从0.0005变化至0.005时，PSNR从16.20剧烈波动至28.29，跨度超过12 dB。这直接驱动了Robust-CG的设计动机：共轭梯度法通过式(21)的闭式步长（线性算子）或线搜索（非线性算子）消除了学习率调参需求。

**计算成本与性能权衡**（图6）。Robust-CG在CelebA高斯去模糊上以约1.5×的额外NFE代价（相比DPS）换取了7+ dB的PSNR提升。计算开销主要来自每步的共轭梯度内迭代（通常3-5次CG迭代）和权重矩阵Wδ的更新。

### 失败模式与局限

**极端污染率**（ρ≥0.30）下所有方法性能均下降，但Robust-CG/CG的退化速度远慢于基线。当ρ=0.30时，Robust-CG在CelebA高斯去模糊上仍保持约25 PSNR，而DPS已降至约17。Huber损失的ℓ₁分支对离群梯度有界（最大梯度为2δ），但离群比例超过50%时，正常观测成为少数，权重矩阵Wδ的估计可能偏向离群分布，需手动验证。

**非线性前向算子的Jacobian近似误差**。有限差分近似引入的误差在高曲率区域可能放大，表现为非线性去模糊任务中Robust-CG相对Robust-GD的优势缩小（表3中二者差距约0.5-1 dB，而线性任务中差距约0.1 dB）。

**噪声方差已知假设**。显式噪声估计依赖σ²的准确值。若实际噪声方差偏离预设值，修正测量ȳ的权重γ_t²/(γ_t²+σ²)将失配。实验未覆盖噪声方差误设场景，该点需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/008_Table_2.jpg]]
*Table 2: (Linear IPs) Gaussian deblurring and motion deblurring with additive Gaussian noise*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/004_Table_1.jpg]]
*Table 1: (Linear IPs) Super-resolution (4×), inpainting (random 70%) with additive Gaussian noise (σ = 0.05) and contamination fraction ρ = 0.02 or 0.10. Measurement Reference DPS DiffPIR*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/018_Table_13.jpg]]
*Table 13: (Linear IPs) Gaussian deblurring and motion deblurring with additive Gaussian noise*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/015_Table_10.jpg]]
*Table 10: Performance of Robust-CG with different value of the Huber loss threshold δ on Gaussian deblurring and motion deblurring with additive Gaussian noise*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/016_Table_11.jpg]]
*Table 11: Performance of Robust-GD with different value of learning rate*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/019_Figure_6.jpg]]
*Figure 6: Visualization of the relationship between the distortion metric PSNR and computational cost for the CelebA Gaussian deblurring task. The computational cost is measured in terms of (left) average inference time over 100 images, (middle) number of function evaluations, and (right) number of forward operator evaluations*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/007_Table_3.jpg]]
*Table 3: Nonlinear deblurring with additive Gaussian noise*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/010_Table_4.jpg]]
*Table 4: Super-resolution (4×) and inpainting (random 70%) with additive Gaussian noise (σ = 0.5) and contamination fraction*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/006_Figure_4.jpg]]
*Figure 4: Visualization results of our methods and other DM-based approaches for the Gaussian deblurring task, with Gaussian noise*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/002_Figure_2.jpg]]
*Figure 2: Visualization results of our methods and other DMbased approaches for the inpainting task, with Gaussian noise*

![[assets/figures/papers/paper_list_l908_https_arxiv_org_abs_2605_09477/figures/003_Figure_3.jpg]]
*Figure 3: Visualization results of our methods and other DMbased approaches for the super-resolution task, with Gaussian noise (σ = 0.05) and a contamination fraction of*



## 定位与知识库关联

### 1. 与现有扩散模型逆问题求解器的关系

本工作直接回应了当前扩散模型逆问题方法在**测量包含离群值（outliers）**场景下的系统性脆弱性。现有主流方法——包括 **DPS**、**DiffPIR**、**DCPS**、**RED-diff**、**DAPS**——在标准加性高斯噪声假设下表现良好，但其数据保真项普遍采用平方 ℓ₂ 范数 ‖y − A(x̄₀)‖₂²。该形式对大幅偏离的离群点高度敏感：单个被污染元素的残差平方即可主导整个保真项的梯度方向，导致信号估计严重偏离真实值。这一瓶颈在本文的离群污染模型（式(2)）下被系统暴露：当任意元素以概率 ρ 被替换为任意值 ξᵢ 时，上述基线的 PSNR 出现灾难性下降（如 Gaussian deblurring CelebA ρ=0.02 下 DPS 仅 22.06 dB，而本文方法达 29.27–29.38 dB）。

本文的核心贡献并非提出全新的扩散采样范式，而是**在现有 DDIM/DDPM 采样框架内替换保真项和优化器两个关键模块**，属于“模块级改进”型工作。具体而言：

- **保真项层面**：将平方 ℓ₂ 损失替换为元素级 Huber 损失 H_δ(r)（式(13)），并引入显式噪声估计 ν̃（式(10)–(11)）以修正测量 y 为 ȳ。Huber 损失在残差 |r| ≤ δ 时保持二次增长，在 |r| > δ 时退化为线性增长，从而对离群点赋予有限权重。这一思路在经典鲁棒统计中已有根基，但本文将其与扩散先验的时序耦合（r_t、γ_t 随扩散时间步变化）以及噪声估计的闭式解结合，形成了完整的鲁棒逆问题求解目标（式(17)）。

- **优化器层面**：Robust-GD 直接对式(17)执行梯度下降，但作者发现其性能对学习率 η_x 高度敏感（同一任务 PSNR 可从 16.20 变化至 28.29，见表11）。Robust-CG 引入共轭梯度法替代梯度下降，利用 Fletcher-Reeves 公式生成共轭方向，并通过线搜索获得闭式步长（线性前向算子，式(21)）或有限差分近似步长（非线性前向算子）。这一设计消除了学习率调参需求，同时保持了迭代效率。

**组件可迁移性**：消融实验（表13）表明，将显式噪声估计与 Huber 损失嵌入 DPS 和 DiffPIR 后，**Robust-DPS** 和 **Robust-DiffPIR** 在离群污染下均显著优于原始基线（如 Robust-DPS 27.70 dB vs DPS 22.06 dB）。这证明本文的两个核心组件具有跨方法泛化能力，不依赖于特定的采样策略。

### 2. 适用边界

**有效场景**：
- 线性逆问题（超分辨率、随机掩码修复、高斯/运动去模糊）在加性高斯噪声 σ = 0.05 且离群污染率 ρ ∈ {0.02, 0.10} 下，Robust-CG 和 Robust-GD 均大幅领先所有基线。
- 非线性去模糊（表3）同样有效，但需通过有限差分近似 Jacobian-向量积，性能增益依然显著。
- 更高噪声水平（σ = 0.5，表4）下仍保持优势，但绝对 PSNR 随噪声增大而下降。

**退化或受限场景**：
- **非线性前向算子**需借助有限差分近似共轭梯度步长，可能引入额外近似误差和计算开销。作者未提供该近似误差的理论界。
- **加性噪声假设**：显式噪声估计依赖于 ν ~ N(0, σ²I) 且方差 σ² 已知。实际场景中 σ² 可能需要估计，且泊松噪声、混合噪声等复杂噪声模型未被覆盖。
- **权重矩阵 W_δ 的迭代依赖**：W_δ 在每次 CG 迭代中基于当前估计更新（算法2），但该迭代重加权最小二乘（IRLS）过程未保证收敛到全局最优解。作者未讨论收敛性分析。
- **极端污染率**：实验仅覆盖 ρ ≤ 0.10，对于 ρ > 0.5 的高污染场景，Huber 损失的鲁棒性边界尚未被探索（作者在开放问题中提及）。

### 3. 局限与开放问题

**已识别的局限**：
1. **Huber 阈值 δ 的设定**：虽然消融实验（表10）表明 Robust-CG 在 δ ∈ {0.005, 0.01, 0.02, 0.04} 范围内 PSNR 波动 < 0.5 dB，但 δ 的最优值仍与任务和数据分布相关。作者未提出自适应阈值机制。
2. **计算开销**：Robust-CG 每步需执行线搜索（线性场景为闭式解，非线性场景需多次有限差分评估），计算成本高于简单梯度步。图6展示了 PSNR 与计算成本的权衡，但未给出与基线在等计算量下的公平对比。
3. **理论分析缺失**：未提供 Huber 损失下优化问题的收敛性保证、离群污染下信号恢复的理论误差界，以及共轭梯度方向在非二次目标下的收敛性质。

**开放问题**：
- 是否可以将显式噪声估计框架扩展到**非高斯噪声模型**（如泊松噪声、脉冲噪声、混合噪声）？这需要重新推导 ν 的闭式估计或引入变分推断。
- 在**极端高污染率（ρ > 0.5）**下，Huber 损失的鲁棒性是否仍然成立？可能需要更激进的损失函数（如 Tukey’s biweight）或结合离群检测的预处理步骤。
- 能否通过**自适应阈值 δ**（如基于残差中位数绝对偏差 MAD 的迭代更新）进一步提升鲁棒性，同时减少人工调参？
- 权重矩阵 W_δ 的更新策略是否可改进？当前设计在每次 CG 迭代中固定 W_δ，但理论上应在 IRLS 框架下交替更新 W_δ 和 x̄₀ 直至收敛。当前截断策略对最终解质量的影响尚不明确。

### 4. 知识库定位

本工作在扩散模型逆问题领域填补了**离群鲁棒性**这一空白。在本文之前，该领域的主流关注点集中在采样效率、非线性逆问题的近似精度、以及不同先验强度下的保真-先验平衡，而**测量污染模型下的鲁棒性**几乎未被系统研究。本文通过引入经典鲁棒统计工具（Huber 损失、IRLS）与扩散先验的时序结构相结合，开辟了一个新的子方向。

从技术谱系看，本文处于以下三条线的交汇处：
- **扩散模型逆问题求解器**（DPS、DiffPIR、DCPS 等）：继承其 DDIM/DDPM 采样框架和基于优化的逆问题求解范式。
- **鲁棒统计**：继承 Huber 损失和迭代重加权最小二乘的经典思想。
- **共轭梯度优化**：将 CG 方法引入扩散逆问题，替代手工调参的梯度下降，提供了更稳定的优化路径。

后续工作可沿两个方向延伸：（1）**更复杂的污染模型**（结构化离群、对抗性污染）与更强的鲁棒损失函数；（2）**理论层面**的鲁棒恢复保证，将压缩感知中的鲁棒恢复理论扩展到扩散先验约束下的逆问题。



## 原文 PDF

![[paperPDFs/CVPR_2026/Outlier_Robust_Diffusion_Solvers_for_Inverse_Problems.pdf]]

---
title: A Statistical Approach to Monte Carlo Denoising
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/A_Statistical_Approach_to_Monte_Carlo_Denoising.pdf
project_link: "https://www.cg.tuwien.ac.at/StatMC"
code_link: "https://benedikt-bitterli.me/resources/"
aliases:
- SDMS
- SAMCD
tags:
- SIGGRAPH_ASIA_2024
- topic/other_unclear
core_operator: 通过为每个像素维护在线统计量（均值、方差、偏度等），构建成对统计检验（Welch t‑检验的变体）作为“成员函数”，仅当两个像素的分布足够相似时才允许降噪滤波将它们组合，从而在方差降低与偏差引入之间取得主动控制。
primary_logic: 将像素视为随机变量，利用在线估计的样本分布统计量进行快速假设检验，以理论最优的方式最小化均方误差；该方法不依赖任何预训练，仅通过统计推断即可达到与神经网络降噪器相当的图像质量，并能自然推广到俄罗斯轮盘赌和多重要度采样等其他蒙特卡洛估计量。
claims:
- 对于对称像素权重且样本服从正态分布的情形，经典的Welch t‑检验在均方误差意义上是最优的。
- 所提统计降噪方法在图像质量上与现有最优神经网络方法相当，且无需任何计算密集的预训练。
- 成员函数在方差趋于零时自动排除具有不同估值的像素，从而保证降噪结果的一致性（无偏收敛）。
- 方法在多个场景上以约28 ms的时间完成1280×720图像的降噪，速度显著优于ProDen和OptiX，与最快的OIDN（~20 ms）接近。
---

# A Statistical Approach to Monte Carlo Denoising

> [!tip] 核心洞察
> 将像素视为随机变量，利用在线估计的样本分布统计量进行快速假设检验，以理论最优的方式最小化均方误差；该方法不依赖任何预训练，仅通过统计推断即可达到与神经网络降噪器相当的图像质量，并能自然推广到俄罗斯轮盘赌和多重要度采样等其他蒙特卡洛估计量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 蒙特卡洛降噪的统计方法 |
| 英文题名 | A Statistical Approach to Monte Carlo Denoising |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [paper](https://users.cg.tuwien.ac.at/~hiroyuki/StatMC/) · [Project](https://www.cg.tuwien.ac.at/StatMC) · [arXiv](https://arxiv.org/abs/1510.04923) · [Code](https://benedikt-bitterli.me/resources/) |
| Topic | #topic/other_unclear |
| Method | Statistical Denoising Method (StatMC) |
| Dataset | Wooden Staircase, Bathroom, Salle de Bain, Classroom |

> [!tip] 效果简介
> - Wooden Staircase (Fig. 1, 256 SPP) 上，denoising time (ms) 28.0 vs 19.5 (OIDN) (+8.5 ms (slower than OIDN, but competitive with other methods))。
> - Bathroom (Fig. 2, 8192 SPP) 上，denoising time (ms) 29.3 vs 20.2 (OIDN) (+9.1 ms)。
> - Salle de Bain (Fig. 3, 32 SPP) 上，denoising time (ms) 28.5 vs 22.1 (OIDN) (+6.4 ms)。

## 概要

蒙特卡洛渲染图像因样本不足而充满噪声，现有神经网络降噪器虽能有效去噪，却依赖大规模预训练，且容易在阴影、焦散等细微光照特征上引入偏差，缺乏收敛性保证。本文提出一种统计降噪方法 **StatMC**，将每个像素视为随机变量，利用在线估计的样本均值、方差及偏度等矩统计量，构建成对 Welch t‑检验作为二元“成员函数”，仅当两个像素的分布足够相似时才允许降噪滤波器将其组合，从而在降低方差与控制偏差之间取得主动平衡。方法完全无需预训练，仅依赖渲染过程中实时收集的统计量，在多个场景上以约 28 ms（1280×720 分辨率）的耗时达到与 **OIDN**、**OptiX** 等神经网络方法相当的图像质量，且随样本数增加自然收敛。此外，该统计框架可推广至俄罗斯轮盘赌与多重要度采样等其他蒙特卡洛估计量。

## 核心方法与创新机理

### 问题瓶颈与统计视角

蒙特卡洛路径追踪生成的图像中，每个像素 $i$ 的真实值 $I_i$ 由渲染方程定义：

$$I_i = \int_{\Omega_i} W_i(\omega) L'(\mathbf{x}, \omega) \, d\omega$$

实际渲染以有限样本 $n_i$ 的蒙特卡洛估计量 $\hat{\theta}_i$ 近似：

$$\hat{\theta}_i = \frac{1}{n_i} \sum_{k=1}^{n_i} \frac{f_k}{p_k}$$

噪声的本质在于：每个像素的估计量 $\hat{\theta}_i$ 是来自其自身样本分布的随机变量，有限样本下方差显著。现有降噪方法——尤其是神经网络方法——在抑制方差时，缺乏对像素间分布差异的显式建模，容易将来自不同分布（即对应不同真实值 $\theta_i$）的像素混合，引入不可控的偏差，表现为边缘模糊、阴影和焦散等光照细节丢失。同时，神经网络方法依赖大规模预训练，泛化能力受限于训练数据分布。

本文的核心洞察是：**将每个像素视为随机变量，利用渲染过程中实时收集的样本分布统计量，通过成对统计检验显式控制哪些像素可以组合**，从而在方差降低与偏差引入之间取得理论上有依据的平衡。

### 核心机制：统计成员函数

降噪估计量 $\tilde{\theta}_j$ 定义为输入噪声估计量的凸组合：

$$\tilde{\theta}_j = \sum_i w_{ij} \hat{\theta}_i$$

其均方误差可分解为方差与偏差平方之和：

$$\mathrm{MSE}(\tilde{\theta}_j, \theta_j) = \mathrm{Var}(\tilde{\theta}_j) + \mathrm{Bias}(\tilde{\theta}_j, \theta_j)^2$$

关键创新在于将滤波权重 $w_{ij}$ 分解为两部分：

$$w_{ij} = \frac{\rho_{ij} m_{ij}}{\sum_i \rho_{ij} m_{ij}}$$

其中 $\rho_{ij}$ 是先验权重（如基于空间距离和 G‑buffer 相似度的联合双边滤波器），$m_{ij} \in \{0, 1\}$ 是**二元统计成员函数**。$m_{ij}$ 的核心作用是：仅当两个像素的样本分布“足够相似”时才允许组合（$m_{ij}=1$），否则禁止（$m_{ij}=0$），从而主动阻断偏差引入。

成员函数的设计源自一个理论最优推导。考虑两个估计量 $\hat{\theta}_i$ 和 $\hat{\theta}_j$ 的成对组合，在对称权重约束下，最小化两者总 MSE 的最优权重为：

$$w^* = \frac{2(\theta_i - \theta_j)^2 + \mathrm{Var}(\hat{\theta}_i) + \mathrm{Var}(\hat{\theta}_j)}{2((\theta_i - \theta_j)^2 + \mathrm{Var}(\hat{\theta}_i) + \mathrm{Var}(\hat{\theta}_j))}$$

当两个像素的真实值相同（$\theta_i = \theta_j$）时，$w^* = 0.5$，即均匀平均最优；当真实值差异远大于方差时，$w^* \to 1$，意味着不应混合。据此定义二元成员函数：

$$m_{ij} = 1 \quad \text{if} \quad (1 - w^*) > \gamma, \quad 0 \quad \text{otherwise}$$

其中 $\gamma$ 是阈值参数（默认 $\gamma = 0.001$）。该设计保证了关键性质：**当方差趋于零时，任何真实值不同的像素对将被自动排除**（$(1-w^*) \to 0$），从而确保降噪结果的一致性（无偏收敛）。这等价于用 Welch t‑检验的双侧检验来判定两个分布是否显著不同：当样本服从正态分布时，该检验在 MSE 意义上是最优的。

### Changed Slots：与现有方法的关键差异

**Slot 1：像素组合准则（从连续权重到统计检验门控）**

基线方法（如联合双边滤波器、Moon CI）仅基于空间距离、颜色或 G‑buffer 相似度赋予连续权重，或使用简单的置信区间排除像素。本文在此基础上引入二元统计成员函数 $m_{ij}$，将组合决策转化为假设检验问题：只有通过 Welch t‑检验（或 Curto 校正）的像素对才被允许组合。这一改变使得降噪过程具备了**分布感知能力**——滤波核的形状不再仅由启发式权重决定，而是由样本统计量自适应地确定边界。

**Slot 2：样本分布处理（从正态假设到偏度校正）**

现有基于置信区间的方法（如 Moon et al.）假设样本服从正态分布，但渲染的辐亮度样本通常严重右偏。本文先对样本应用 Box‑Cox 变换以接近正态：

$$x_k'(\lambda) = \begin{cases} \log(x_k), & \lambda = 0 \\ (x_k^\lambda - 1)/\lambda, & \text{otherwise} \end{cases}$$

取 $\lambda = 1/2$（即平方根变换），然后使用 Curto (2023) 的偏度校正均值置信区间方法进行检验。这一改变显著提升了统计检验在非正态分布下的准确性。

**Slot 3：在线统计量维护（从无状态到增量矩估计）**

不同于仅存储累计均值或方差的方法，本文采用 Welford/Meng 在线算法，在渲染过程中同步更新每个像素的均值、二阶中心矩和三阶中心矩：

$$M_l = \frac{1}{n_i} \sum_k (X_k - \bar{X})^l$$

这使得统计检验所需的所有信息（均值、方差、偏度）均可增量维护，无需存储历史样本，内存开销极小。

**Slot 4：训练依赖（从预训练到零训练）**

神经网络方法（OptiX、OIDN、ProDen）需要大规模预训练数据，而本文方法完全基于渲染过程中实时收集的统计量，无需任何预训练。这从根本上消除了训练数据分布对泛化能力的限制。

### 流水线模块与因果关系

整个降噪流水线由五个模块串联构成，模块间存在明确的因果依赖：

1.  **在线统计追踪器 (Online Statistics Tracker)**：在路径追踪的样本累积阶段，逐像素增量更新均值、二阶和三阶中心矩。这是所有后续统计推断的数据基础——没有准确的矩估计，后续检验将失效。

2.  **Box‑Cox 变换**：在进入统计检验前，对严重右偏的辐亮度样本应用 $\lambda=1/2$ 的 Box‑Cox 变换，使其接近正态分布。该模块直接服务于成员函数的有效性：Welch t‑检验在正态假设下才是最优的，变换降低了因分布偏斜导致的检验失效风险。

3.  **基滤波器 (Joint Bilateral Filter)**：提供基于空间距离和 G‑buffer 特征（法线、深度等）的先验高斯权重：

    $$\rho_{ij} = \exp\left(-\frac{1}{2} (\mathbf{p}_j - \mathbf{p}_i)^T \Sigma^{-1} (\mathbf{p}_j - \mathbf{p}_i)\right)$$

    该模块的作用是双重的：一方面确保基本的空间平滑效果，另一方面限制滤波核的有效半径（默认 20 像素），避免统计检验在全图范围内搜索相似像素带来的计算开销。

4.  **成员函数 (Membership Function)**：对滤波核内的每对像素 $(i, j)$，利用在线统计量计算成对最优权重 $w^*$，并通过阈值 $\gamma$ 生成二元决策 $m_{ij}$。这是整个方法的核心因果节点——$m_{ij}$ 直接决定了哪些像素可以混合，从而控制偏差的引入量。

5.  **滤波权重计算与归一化**：将 $\rho_{ij}$ 与 $m_{ij}$ 相乘并归一化，得到最终滤波权重 $w_{ij}$，对输入估计量加权求和输出降噪结果。

模块间的因果关系链为：**在线统计量 → (Box‑Cox 变换 →) 成员函数决策 → 滤波权重 → 降噪输出**，基滤波器则提供空间局部性约束。消融实验验证了这一链条中每个环节的必要性：移除成员函数（$m_{ij} \equiv 1$）导致阴影和焦散等边缘被过度模糊；禁用 Box‑Cox 变换使右偏分布下的 RMSE/MAE 升高；缩小基滤波器半径可提速但残留更多噪声。

### 训练与推理路径

本方法**无训练阶段**。所有参数（$\alpha=0.005$、滤波半径 20 像素、$\lambda=1/2$）均为固定值，未针对场景或样本数进行调优。

推理路径在 GPU 上以单次遍历完成：渲染器在累积样本的同时更新在线统计量，达到目标样本数后，统计量直接传入降噪核，执行上述流水线，输出降噪图像。对于 $1280 \times 720$ 分辨率，完整降噪时间约 28 ms（含 GPU 上传/下载），与最快的神经网络方法 OIDN（约 20 ms）接近，显著快于 OptiX（约 85–142 ms）和 ProDen（约 1800–2000 ms）。

![[assets/figures/papers/paper_list_l41_https_users_cg_tuwien_ac_at_hiroyuki_StatMC/figures/002_Figure_3.jpg]]
*Figure 3: Salle de Bain scene rendered with 32 SPP. Denoising time for Moon CI: 36.4 ms, OptiX: 141.6 ms, OIDN: 22.1 ms, ProDen: 1979.9 ms, ours: 28.5 ms. In the supplementary document, we provide results for this scene at a higher sample count of 512 SPP*

![[assets/figures/papers/paper_list_l41_https_users_cg_tuwien_ac_at_hiroyuki_StatMC/figures/003_Figure_2.jpg]]
*Figure 2: Bathroom scene rendered with 8192 SPP. Denoising time for Moon CI: 39.7 ms, OptiX: 91.2 ms, OIDN: 20.2 ms, ProDen: 2027.5 ms, ours: 29.3 ms*

## 实验与关键发现

**实验设置与公平性说明。** 所有方法在同一消费级GPU上运行，降噪时间包含完整的GPU数据上传与下载。本文方法在所有样本数下均使用固定滤波参数（显著性水平 $\alpha = 0.005$，滤波半径20像素），未按场景或样本数进行调优，以展示其自然的收敛行为。对比的神经网络方法（OptiX、OIDN）需要离线预训练，而本文方法仅依赖渲染过程中在线收集的统计量，无预训练成本。

**主结果：图像质量与速度对比。** 在四个测试场景上，StatMC以约28 ms的降噪时间（1280×720分辨率）取得了与当前最优方法相当的视觉质量。表1汇总了各场景下的降噪耗时对比。

| 场景（SPP） | Moon CI | OptiX | OIDN | ProDen | StatMC（本文） |
|---|---|---|---|---|---|
| Wooden Staircase（256 SPP） | 35.3 ms | 85.5 ms | 19.5 ms | 1834.9 ms | **28.0 ms** |
| Bathroom（8192 SPP） | 39.7 ms | 91.2 ms | 20.2 ms | 2027.5 ms | **29.3 ms** |
| Salle de Bain（32 SPP） | 36.4 ms | 141.6 ms | 22.1 ms | 1979.9 ms | **28.5 ms** |
| Classroom（256 SPP） | 35.6 ms | 89.5 ms | 20.8 ms | 1840.5 ms | **28.3 ms** |

关键发现：StatMC的速度显著优于OptiX（约3倍）和ProDen（约65倍），与最快的OIDN（~20 ms）差距在10 ms以内，但OIDN需要大量预训练数据和计算，而StatMC完全零预训练。在极低样本数下（Salle de Bain, 32 SPP），OIDN的优势缩小至约6 ms，表明统计方法在稀疏样本场景下的竞争力更强。

**定量收敛性分析。** Fig. 5展示了四个场景在RMSE、MAE和DSSIM（经色调映射至LDR后计算）三项指标上随样本数增加的收敛曲线。核心结论：

- **与Moon CI对比**：StatMC在所有样本数下均显著优于Moon CI的单侧置信区间方法，验证了双侧Welch t‑检验在MSE意义上的理论优势。
- **与神经网络方法对比**：在中等至高样本数（≥256 SPP）下，StatMC的RMSE/MAE与OIDN和OptiX几乎重合或略优；在极低样本数（32 SPP）下，OIDN的RMSE略低，但StatMC的MAE和DSSIM与之接近，表明统计方法在保持结构相似性方面不逊色。
- **收敛一致性**：随着样本数增加，StatMC的误差持续下降，未出现神经网络方法中可能存在的偏差平台效应，验证了成员函数在方差趋于零时自动排除不同分布像素的一致性保证。

**消融实验：各模块的因果贡献。** Fig. 6系统消融了StatMC的关键设计选择（默认配置为中心图）：

1. **移除统计成员函数（$m_{ij} \equiv 1$，仅双边滤波）**：阴影边缘和焦散等未在G‑buffer中出现的特征被严重模糊，偏差显著增加。这直接证明了统计检验是抑制偏差的核心机制，双边滤波器的先验权重单独使用时无法区分像素分布差异。

2. **禁用Box‑Cox变换**：在渲染图像典型的右偏辐亮度分布下，RMSE和MAE均升高，验证了正态性假设对t‑检验有效性的重要性，以及Box‑Cox变换（$\lambda = 1/2$）在缓解偏度影响中的关键作用。

3. **缩小滤波半径（20→6像素）**：运行时间降至约11 ms，但部分区域噪声残留更多，表明当前20像素半径是在速度与降噪质量间的经验平衡，实际部署中可根据性能需求调整。

4. **允许非对称权重**：生成视觉上更吸引人的结果，但可能导致整体亮度和能量损失，定量误差略增。这揭示了对称性约束在保持无偏性方面的保守但安全的作用。

5. **采用Moon CI的单侧检验**：性能弱于本文的双侧Welch t‑检验，验证了理论推导中双侧检验在MSE最优性上的优势。

6. **G‑buffer的作用**：将基滤波器从联合双边替换为纯高斯滤波（无G‑buffer引导），降噪质量下降，但统计成员函数仍能保留主要边缘，说明统计检验本身已提供了一定的结构感知能力。

**扩展应用验证。** 本文还将统计框架推广到其他蒙特卡洛估计量：

- **近似贡献俄罗斯轮盘赌（ACRR）**：在等时预算下（~417 s），ACRR以987 SPP取得了与经典吞吐量轮盘赌（RR‑1, 2048 SPP）相当的rMSE，节省了约50%的样本数（Fig. 7），证明了统计推断在自适应终止路径追踪中的有效性。
- **选择式多重要度采样（SMIS）**：在等时条件下（~733 s），SMIS以1063 SPP的rMSE优于参考MIS（1024 SPP），且降噪后的BSDF/直接光照采样胜率可视化显示了统计检验在识别采样策略优势中的能力（Fig. 8）。

![[assets/figures/papers/paper_list_l41_https_users_cg_tuwien_ac_at_hiroyuki_StatMC/figures/006_Figure_7.jpg]]
*Figure 7: Comparison between our approximate-contribution Russian roulette (ACRR) and classic throughput-based RR starting at the first bounce (RR-1) and at the fifth bounce (RR-5). Images show RR-1 at 2048 SPP (417.53 s), RR-5 at 1451 SPP (418.05 s) and ACRR at 987 SPP (417.00 s). Timings include GPU upload, denoising, and download. Here, we also show relative mean squared error (rMSE) [Rousselle et al. 2011], as it allows to gauge the sampling performance for individual pixels, regardless of their absolute value*

![[assets/figures/papers/paper_list_l41_https_users_cg_tuwien_ac_at_hiroyuki_StatMC/figures/008_Figure_8.jpg]]
*Figure 8: Comparison of our selective multiple importance sampling (SMIS) to standard multiple importance sampling [Veach 1997] (“Ref. MIS”) and visualization of first-bounce SMIS win rates for BSDF sampling (??BSDF) and direct-light sampling (??DL) before and after denoising. We use rMSE [Rousselle et al. 2011] to better assess the sampling performance for individual pixels. Images show Ref. MIS at 1024 SPP (734.80 s) and our SMIS at 1063 SPP (732.89 s)*

**失败模式与适用边界。** 当前方法存在以下已知限制：

- **二元成员函数的局限**：$m_{ij}$ 仅取0/1值，丢弃了最优权重 $w^*$ 中的连续信息，可能在边缘过渡区域引入轻微的块状伪影。连续成员函数的设计是未来改进方向。
- **固定参数策略**：所有实验使用固定的 $\alpha = 0.005$ 和20像素半径，在极端样本数或特殊场景下可能不是最优。实际应用中可能需要手动调优，或设计自适应参数策略。
- **时间域未扩展**：方法仅处理单帧图像，未利用动画序列中的时间样本统计量，对于动态场景的时间一致性未做处理。
- **速度差距**：约28 ms的延迟对于实时应用（如游戏引擎的~16 ms预算）仍有差距，尽管已显著快于OptiX和ProDen。

**证据强度评估。** 主结果和消融实验的证据置信度高（0.9–0.95），均来自论文明确标注的图表和数据。扩展应用（ACRR、SMIS）的定量对比基于等时预算的rMSE，验证了统计框架的泛化能力。失败模式中连续成员函数的潜力尚待实验验证，需手动确认。

![[assets/figures/papers/paper_list_l41_https_users_cg_tuwien_ac_at_hiroyuki_StatMC/figures/001_Figure_1.jpg]]
*Figure 1: Our statistical denoising method, using online estimates of sample statistics, achieves image quality comparable to current state-of-the-art methods, without any computation-heavy prior training. We compare our denoiser to the approach by Moon et al. [2013] (“Moon CI”), NVIDIA OptiX AI-Accelerated Denoiser (“OptiX”), Intel Open Image Denoise (OIDN), and progressive denoising [Firmino et al. 2022] (“ProDen”). These results have been generated using 256 samples per pixel (SPP) with the following denoising times; Moon CI: 35.3 ms, OptiX: 85.5 ms, OIDN: 19.5 ms, ProDen: 1834.9 ms, ours: 28.0 ms*

![[assets/figures/papers/paper_list_l41_https_users_cg_tuwien_ac_at_hiroyuki_StatMC/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study: we compare our default settings (center) to (a) the noisy input, (b) the joint bilateral base filter only*

## 定位与知识库关联

本文提出的 **StatMC** 在蒙特卡洛降噪知识谱系中的核心定位是：**将像素组合准则从“启发式相似度权重”替换为“基于在线统计推断的二元成员函数”**，从而在零预训练条件下实现与神经网络降噪器相当的图像质量，并天然具备收敛性保证。

### 改变的 Slot：像素组合准则

传统降噪方法（无论是经典的双边滤波器还是现代神经网络降噪器）在决定“哪些像素可以参与滤波”时，依赖以下两类机制之一：

- **空间/颜色/G‑buffer 相似度权重**：如 **Joint Bilateral Filter**（Eisemann and Durand, 2004; Petschnigg et al., 2004）仅根据空间距离和辅助特征（法线、深度等）的相似性赋予连续权重，完全不考虑像素估计量本身的统计分布差异。这导致在阴影边界、焦散边缘等 G‑buffer 无法体现的特征处，偏差被系统性引入。
- **神经网络学习的隐式映射**：如 **OptiX**（Chaitanya et al., 2017）和 **OIDN**（Áfra, 2024）通过大量预训练数据学习从噪声图像到干净图像的映射，其像素组合逻辑隐含在网络参数中，既不透明也无法提供收敛性保证。**ProDen**（Firmino et al., 2022）虽引入了渐进式收敛控制，但本质上仍依赖预训练网络。

StatMC 将这一 slot 替换为：**在基滤波器权重 $\rho_{ij}$ 之上，叠加一个二元统计成员函数 $m_{ij} \in \{0,1\}$**，该函数通过成对 Welch t‑检验（经 Box‑Cox 变换和 Curto 偏度校正）决定两个像素的样本分布是否“足够相似”。仅当检验不拒绝同分布假设时，才允许像素组合。这直接回应了 MSE 分解中的偏差项——成员函数在方差趋于零时自动排除具有不同估值的像素，从而保证降噪结果的无偏收敛（property (d), §4.1）。

### 与最邻近基线 Moon CI 的本质差异

**Moon CI**（Moon et al., 2013）是唯一同样使用统计检验的基线，但其方法存在两个根本性局限：

1. **单侧置信区间 vs 双侧假设检验**：Moon CI 使用单侧置信区间排除像素，本质上只控制了“错误包含”的风险，未考虑“错误排除”的代价。StatMC 从最小化成对 MSE 出发，推导出双侧 Welch t‑检验作为理论最优的成员函数（在对称权重和正态假设下，§4.2）。消融实验（Fig. 6(h)）证实，Moon CI 的单侧检验在 RMSE/MAE 上均弱于 StatMC 的双侧检验。
2. **正态假设的严格性**：Moon CI 直接假设样本服从正态分布，未处理渲染中常见的右偏分布。StatMC 引入 Box‑Cox 变换（$\lambda=1/2$）和基于三阶矩的 Curto 校正，显著提升了非正态分布下的检验效力（Fig. 6(f) 消融证实禁用 Box‑Cox 会导致误差升高）。

### 知识库挂载点

StatMC 可挂载到渲染知识库的以下节点：

- **蒙特卡洛估计理论**：将像素视为随机变量、在线维护 Welford/Meng 高阶矩（Alg. 1）的做法，将降噪问题重新形式化为统计推断问题。这为后续研究打开了将其他统计工具（如贝叶斯检验、序贯检验）引入渲染的通道。
- **自适应采样与路径引导**：StatMC 的在线统计量天然适用于指导样本分配——高方差或分布复杂的像素可被识别并分配更多样本。文中已展示其在俄罗斯轮盘赌（ACRR, Fig. 7）和多重要度采样（SMIS, Fig. 8）中的应用，证明该框架可推广至其他蒙特卡洛估计量。
- **零样本降噪方法族**：与需要预训练的神经网络方法形成互补。StatMC 的“即插即用”特性使其特别适用于预训练数据不可得或场景分布与训练集差异大的情形。

### 适用边界

- **时间域未覆盖**：当前方法仅处理单帧图像，未利用动画序列中的时间统计量，因此不适用于需要时间一致性的动画降噪任务。
- **参数固定**：所有实验使用固定显著性水平 $\alpha=0.005$ 和滤波半径 20 px，未根据样本数或场景特征自动调整。在实际部署中，可能需要手动调参以平衡偏差与方差。
- **速度略逊于最快方法**：约 28 ms 的降噪时间（1280×720）比 OIDN（~20 ms）慢约 40%，对于严格实时应用（如 60 fps 游戏）仍有差距。
- **二元成员函数的局限性**：当前 $m_{ij} \in \{0,1\}$ 丢弃了最优权重 $w^*$ 中的连续信息，可能损失部分降噪潜力。连续成员函数的设计是明确的后续方向。

### 后续启发

1. **连续成员函数**：将 $m_{ij}$ 设计为 $w^*$ 的连续函数（而非阈值化），有望进一步降低总体 MSE。
2. **时空统计降噪**：将在线统计量扩展到时域，利用帧间样本的分布相似性进行时空联合滤波，可同时提升降噪质量和时间一致性。
3. **自适应参数调整**：根据像素的样本数和方差水平自动调整 $\alpha$ 和滤波半径，实现更精细的偏差-方差权衡。
4. **与其他渲染组件的深度集成**：StatMC 的统计框架可作为“通用方差降低层”集成到路径引导、自适应采样、光子映射等渲染流程中，替代现有启发式规则。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/A_Statistical_Approach_to_Monte_Carlo_Denoising.pdf]]
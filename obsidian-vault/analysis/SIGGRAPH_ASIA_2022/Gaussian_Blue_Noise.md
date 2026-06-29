---
title: Gaussian Blue Noise
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Gaussian_Blue_Noise.pdf
project_link: null
code_link: null
aliases:
- GBNG
- GBN
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 三个关键设计选择共同决定了性能：1) 使用完整（未截断）高斯核并基于梯度下降直接优化全点对能量；2) 选取合适的核带宽σ（如2D中σ=1）；3) 执行足够的迭代次数以充分降低低频噪声。此外，环面边界条件和可分离性使高维扩展成为可能。
primary_logic: "推导出理想高斯核蓝噪声的功率谱上界为指数形式（P(ω) ≤ ε e^{σ²‖ω‖²}），理论上面临的噪声基底优于细胞方法的多项式谱；通过消除核截断带来的频率失真、采纳环面边界实现平衡以及利用梯度下降持续优化，首次使核方法在噪声基底上超越BNOT达两个数量级，并且算法自然扩展至高维空间。"
claims:
- GBN 在 2D 中的低频噪声基底比 BNOT 低两个数量级，比已有核方法低十个数量级。
- 理论推导得到高斯核蓝噪声的理想功率谱呈指数增长，先天优于细胞方法的多项式谱。
- 使用完整的核支持（所有点对）而非局部邻域，是收敛到高质量频谱的关键。
- 选取σ=1 可在 2D 获得最优蓝噪声频谱，且算法在高维可自然地获得更低噪声基底。
---

# Gaussian Blue Noise

> [!tip] 核心洞察
> 推导出理想高斯核蓝噪声的功率谱上界为指数形式（P(ω) ≤ ε e^{σ²‖ω‖²}），理论上面临的噪声基底优于细胞方法的多项式谱；通过消除核截断带来的频率失真、采纳环面边界实现平衡以及利用梯度下降持续优化，首次使核方法在噪声基底上超越BNOT达两个数量级，并且算法自然扩展至高维空间。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高斯蓝噪声 |
| 英文题名 | Gaussian Blue Noise |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2206.07798) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Gaussian Blue Noise (GBN) |
| Dataset | 2D 蓝噪声质量评估（径向功率谱）, 蒙特卡洛积分（高斯和函数，2D/3D/8D）, 自适应采样与重建（512×768 图像） |

> [!tip] 效果简介
> - 2D 蓝噪声质量评估（径向功率谱） 上，噪声基底（低频功率） GBN（低于 BNOT 约 2 个数量级） vs BNOT (低频能量显著更低，峰值更小)。
> - 蒙特卡洛积分（高斯和函数，2D/3D/8D） 上，积分方差 GBN（方差最低） vs BNOT、分层采样、Halton 等 (方差比对比分布低数个数量级)。
> - 自适应采样与重建（512×768 图像） 上，视觉噪声 / 细节保真度 GBN（噪声明显更低，细节更锐利） vs BNOT, KDM (噪声显著减少，尤其在 100k 迭代后效果优异)。

## 概要

现有蓝噪声优化面临一个核心瓶颈：核方法（如 KDM、VnC、BlueNets）因采用截断核、局部邻域和不充分的优化迭代，始终未能达到充分低的噪声基底，远未发挥理论上指数级功率谱的潜力；而基于最优传输的细胞方法 BNOT 虽长期被视为质量标杆，但其功率谱本质上受限于多项式形式，且难以向高维扩展。

本文提出 **Gaussian Blue Noise (GBN)**，通过三个关键设计选择从根本上突破上述限制：（1）使用完整（未截断）高斯核，在全点对支持下基于梯度下降直接优化能量函数；（2）选取合适的核带宽（2D 中 σ=1）；（3）执行充分的迭代（推荐 10K 轮）以持续压低低频噪声。理论推导表明，理想高斯核蓝噪声的功率谱上界为指数形式 $P(\pmb{\omega}) \leq \epsilon e^{\sigma^{2}\|\pmb{\omega}\|^{2}}$，先天优于细胞方法的多项式谱。

实验表明，GBN 在 2D 中的低频噪声基底比 BNOT 低约两个数量级，比已有核方法低十个数量级；在 2D/3D/8D 蒙特卡洛积分任务中，方差显著低于分层采样、BNOT 等分布；自适应采样与重建中噪声更低、细节更锐利。方法自然扩展至高维空间，且高维中收敛更快、噪声基底更低。

## 核心方法与创新机理

### 瓶颈分析：核方法蓝噪声为何长期落后于细胞方法

蓝噪声优化的核心目标是在保持均匀空间分布的同时，将噪声能量推向高频区域，使低频噪声尽可能低。长期以来，基于最优传输的细胞方法 **BNOT**（de Goes et al., 2012）被视为蓝噪声质量的标杆，其功率谱在低频段呈现多项式衰减。相比之下，基于核的方法（如 KDM、VnC、BlueNets）虽然理论上具备产生指数级功率谱的潜力，却始终未能达到充分低的噪声基底——实际频谱与 BNOT 相比并无优势。

本文揭示了核方法表现不佳的三个根本原因，它们共同构成了制约性能的瓶颈：

1. **核截断与局部邻域**：现有核方法普遍截断高斯核的支持范围，仅考虑局部邻域内的点对相互作用。这种截断等价于在频域中将核频谱与 sinc 函数卷积，导致频率结构严重畸变，破坏了指数谱的潜在优势。
2. **不合适的核带宽**：多数方法未对高斯核的带宽 σ 进行精细调节，或选取过小的 σ 值（如 σ < 1），虽然能快速产生视觉均匀的分布，但频谱收敛浅、噪声基底高。
3. **不充分的优化迭代**：受限于计算效率和启发式策略，核方法的优化迭代次数往往不足，未能充分压低低频能量。

### 核心洞察：指数谱的理论优势与实现路径

本文的核心理论贡献在于推导出理想高斯核蓝噪声的功率谱上界为指数形式：

$$P(\pmb{\omega}) \leq \epsilon e^{\sigma^{2}\|\pmb{\omega}\|^{2}}$$

该上界表明，基于高斯核的蓝噪声在理论上先天优于细胞方法的多项式谱——在低频区域，指数函数值远小于多项式，意味着可达的噪声基底更低。这一理论优势的兑现依赖于三个关键设计选择：**完整核支持**（消除频率畸变）、**合适的核带宽**（平衡收敛速度与频谱深度）、**充分的梯度下降优化**（持续压低低频能量）。

### 方法框架：从能量函数到梯度下降

GBN 的核心思想源于核方法的基本框架：在样本点 $\mathbf{X} = \{\mathbf{x}_k\}_{k=1}^N$ 上放置一组相同的高斯核，通过优化点位置来最小化核密度之和的方差。该方差定义为：

$$\mathrm{Var}\big(A(\mathbf{X})\big) = \frac{\pi\sigma^{2}}{N}\sum_{k=1}^{N}\sum_{l=1}^{N}\exp\left(-\frac{\|\mathbf{x}_{k}-\mathbf{x}_{l}\|^{2}}{4\sigma^{2}}\right) - \left(2\pi\sigma^{2}\right)^{2}$$

最小化该方差等价于衰减除直流分量外的整个功率谱，从而驱动点集形成蓝噪声特性。基于此，定义每点的损失函数：

$$\mathcal{E}(\mathbf{x}_{k}) = \frac{\pi\sigma^{2}}{N} \sum_{l\neq k} \exp\left(-\frac{\|\mathbf{x}_{k} - \mathbf{x}_{l}\|^{2}}{2\sigma^{2}}\right)$$

并推导其解析梯度用于迭代更新：

$$\nabla\mathcal{E}(\mathbf{x}_{k}) = -\frac{\pi}{N}\sum_{l\neq k}\exp\left(-\frac{\|\mathbf{x}_{k} - \mathbf{x}_{l}\|^{2}}{2\sigma^{2}}\right)\frac{\mathbf{x}_{k} - \mathbf{x}_{l}}{\sigma^{2}}$$

### 关键设计槽位与因果机制

**槽位一：核支持范围——从局部截断到全支持**

这是 GBN 实现突破的最关键设计选择。现有核方法为降低计算复杂度，通常将高斯核截断到有限邻域（如仅考虑 Voronoi 第一环邻居）。然而，截断操作在频域中引入 sinc 函数的卷积效应，扩展了能量核的频率支持，导致频谱结构发生不可逆的畸变。实验表明（Fig. 4, 5），1σ 截断使结果退化为类似 Centroidal Voronoi Tessellation (CVT) 的分布，频谱质量大幅下降。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_abs_2206_07798/figures/004_Figure_4.jpg]]
*Figure 4: The Fourier transform (shown in (b,c)) of the three (truncated) Gaussians (shown in (a)) including: the standard Gaussian (colored blue), a truncated Gaussian in the range of [−1, 1] (colored red) and in the range of [−2, 2] (colored yellow)*

GBN 采用全支持策略，考虑所有点对之间的相互作用。在环面（周期性）边界条件下，通过高斯核的可分离性，将多维能量计算分解为一维无限求和的乘积，利用 theta 函数高效评估精确能量。这种设计消除了频率畸变的根源，使指数谱的理论优势得以兑现。

**槽位二：边界条件——从有界域到环面域**

有界域中边缘点受力不平衡，会破坏蓝噪声的均匀性。GBN 采用环面（toroidal）域，通过周期性边界使每个点获得平衡的邻域力场。环面能量的计算利用高斯核的可分离性：

$$\mathcal{E}_{ij} = \sum_{k=-\infty}^{\infty} \exp\left(-\frac{(x_i - x_j - k)^2}{2\sigma^2}\right) \sum_{l=-\infty}^{\infty} \exp\left(-\frac{(y_i - y_j - l)^2}{2\sigma^2}\right)$$

对于有界域应用，GBN 采用连续域模型进行适配。环面设计不仅保证了边界质量，还使高维扩展成为可能——可分离性意味着 d 维优化的计算复杂度为 O(dN²)，而非指数增长。

**槽位三：核带宽 σ 的选择——2D 最优值 σ=1**

σ 控制着高斯核的宽度，直接影响优化行为与频谱形状。较小的 σ（如 0.5）使点间排斥力集中在极近邻域，虽然少量迭代即可产生视觉均匀的分布，但频谱收敛浅、噪声基底高。较大的 σ 使排斥力范围扩大，有利于压低低频能量，但收敛速度减慢。

系统实验（Fig. 3a）表明，σ=1 在 2D 中提供了收敛速度与频谱深度之间的最优平衡。这一选择并非经验性的——它与单位面积内点密度的自然尺度相匹配，使每个点的有效邻域恰好覆盖其统计意义上的相互作用范围。

**槽位四：优化策略——长期梯度下降**

GBN 采用基于完整能量函数的梯度下降优化，推荐执行 10K 轮迭代。收敛行为（Fig. 7）显示：前约 500 次迭代内呈线性收敛，频谱快速成形；随后收敛减速，但持续迭代仍能稳定压低噪声基底。这种长期优化是达到极低噪声基底的必要条件——GBN 在低频区域的噪声基底比 BNOT 低约两个数量级，比现有核方法低十个数量级。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_abs_2206_07798/figures/007_Figure_7.jpg]]
*Figure 7: Evolution of the radial power curve of our algorithm at different iterations counts, showing the power spectrum of (a) the discrete points and (b) the Gaussian-filtered set*

值得注意的是，梯度下降的 Hessian 矩阵固有奇异，导致优化无法完全停止，后期收敛呈线性且缓慢。这是方法的固有特性，而非缺陷。

**槽位五：自适应采样扩展**

对于非均匀密度采样，GBN 引入密度相关的核成形机制。每个点 $\mathbf{x}_i$ 关联一个权重 $a_i$，扩展方差公式为：

$$\mathrm{Var}\left(A(\mathbf{x})\right) = \frac{1}{N}\sum_{i=1}^{N}\sum_{j=1}^{N}\frac{2\pi a_{i}a_{j}\sigma^{2}}{a_{i}+a_{j}}\exp\left(-\frac{a_{i}a_{j}\left\|\mathbf{x}_{i}-\mathbf{x}_{j}\right\|^{2}}{2\sigma^{2}\left(a_{i}+a_{j}\right)}\right) - \left(2\pi\sigma^{2}\right)^{2}$$

优化过程交替进行：在固定权重下优化点位置（梯度下降），在固定点位置下优化权重（使混合核密度逼近目标密度图）。这种交替优化策略使 GBN 在自适应采样任务中同样展现出优于 BNOT 的噪声特性。

### 高维扩展的自然优势

高斯核的可分离性使 GBN 天然适用于高维空间。实验发现（Fig. 3b），在更高维度（如 8D）中，GBN 不仅收敛更快，还能达到更低的噪声基底。作者初步猜测这与自由度增加有关，但确切机制仍需进一步研究。这一特性使 GBN 在高维蒙特卡洛积分等应用中具有显著优势。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_abs_2206_07798/figures/010_Figure_10.jpg]]
*Figure 10: Adaptive sampling a density map, comparing (b) BNOT [de Goes et al. 2012], (c) KDM [Fattal 2011], and (d) our algorithm. The input image is shown in (a), along with a blurred version below. The reconstructed images using Algorithm 2 are shown in the bottom row*

## 实验与关键发现

### 2D 蓝噪声质量：噪声基底与频谱对比

GBN 在 2D 均匀蓝噪声质量上的核心优势体现在低频噪声基底的显著降低。图 1(g) 的径向功率谱（1000 个实例、每实例 4000 点）揭示了两类频谱形态：BNOT 与分层采样呈现多项式谱（在双对数坐标中为直线），而 GBN、VnC、KDM 和 FPO 呈现指数谱。GBN 的低频功率比现有最优核方法低约十个数量级，甚至比长期被视为质量标杆的 BNOT（de Goes et al., 2012）低约两个数量级。图 1(f) 的点分布图中，GBN 的中心区域呈现近乎纯黑的低频能量，视觉噪声明显低于其他方法。这一结果验证了理论推导的核心预测：理想高斯核蓝噪声的功率谱上界为指数形式 $P(\pmb{\omega}) \leq \epsilon e^{\sigma^{2}\|\pmb{\omega}\|^{2}}$，先天优于细胞方法的多项式上界。

图 8 进一步使用经典蓝噪声测量指标进行系统对比。在有效奈奎斯特率 $\nu_{\mathrm{eff}}$、振荡 $\Omega$ 和键取向序等指标上，GBN 与 BNOT、FPO、KDM 等 SOTA 方法相当或更优。值得注意的边界条件是：这些指标主要衡量中高频特性，而 GBN 的差异化优势集中在极低频区域，因此传统指标对 GBN 的优越性反映有限。

### 蒙特卡洛积分：跨维度方差降低

图 9 展示了 GBN 在蒙特卡洛积分任务中的实际效用。实验使用两类被积函数——高斯和函数与半空间函数，分别在 2D、3D 和 8D 下比较 GBN 与 BNOT、分层采样、Halton 序列等常见分布的积分方差。在 2D 情形下，平均 100 个被积函数实例、1000 个点集；3D 和 8D 下各 100 个点集。结果显示 GBN 的方差比对比分布低数个数量级，且这一优势随维度升高而保持甚至扩大。这与图 3(b) 的发现一致：高维下 GBN 收敛更快、能达到更低的噪声基底（初步猜测源于自由度增加，但作者指出有待进一步研究）。

### 自适应采样与图像重建

在非均匀密度采样任务中，GBN 扩展了自适应核成形机制（Algorithm 2），通过优化每个点的核权重 $a_i$ 使混合核密度逼近输入图像。图 10 使用 512×768 密度图比较了 BNOT、KDM 和 GBN 的重构质量：GBN 的重建图像噪声明显更低、细节更锐利。图 17 提供了更细致的收敛对比：在约 300 次迭代（与 BNOT 单次优化耗时相当）时，GBN 已取得可比或更优质量；延长至 100k 次迭代后，重构质量进一步提升，噪声几乎完全消除。公平性方面，所有方法均使用相同的加权随机初始化（de Goes et al., 2012），重构均通过提出的核成形算法进行，确保比较基准一致。

### 关键消融实验

**核带宽 σ 的选择。** 图 2 揭示了 σ 对频谱质量的决定性影响：σ=0.5 仅需 30 次迭代即可产生视觉均匀的分布，但其频谱收敛极浅、噪声基底高；σ=1.1 需 1M 次迭代才能获得类似视觉质量，但频谱收敛更深。图 3(a) 系统扫描了不同 σ 值在 2D 下的实际频谱（1000 点集、10k 迭代），确认 σ=1 为 2D 最优平衡点——在视觉质量与频谱深度之间取得最佳折衷。

**核截断的损害。** 图 4 从频域角度解释了核截断的破坏机制：截断等价于在空域乘以矩形窗，频域则卷积 sinc 函数，扩展了核的频率支撑并引入畸变。图 5 展示了实际优化结果：1σ 截断仅覆盖第一圈 Voronoi 邻居，结果趋近于 Centroidal Voronoi Tessellation（CVT）；2σ 和 3σ 截断产生不同类型的失真。只有使用完整核支持（所有点对）才能收敛到高质量频谱。这一发现解释了以往核方法性能受限的关键瓶颈。

**收敛行为。** 图 7 展示了梯度下降过程中径向功率谱的演化：约 500 次迭代内呈线性收敛，随后减速；持续迭代（推荐 10k 轮）持续降低噪声基底。作者指出 Hessian 矩阵固有奇异，导致优化无法完全停止，后期收敛缓慢但稳定。

### 效率与适用边界

在 Titan GPU 上，4000 点、10k 次迭代的单次优化约需 5 秒，与 BNOT 的完整优化耗时相当。对于极大量点集（如数十万点），全核评估的 $O(N^2)$ 复杂度成为瓶颈，可通过 9σ 局部邻域近似缓解，但需权衡频谱质量损失。1D 蓝噪声的实现受限：点数对邻域的限制导致自然趋向规则网格，仅能通过窄带频谱截断获得。自适应采样需交替进行点优化和核成形，增加了迭代复杂度。算法在极高维下的实际效用和稀疏区域表现尚未深入探讨。

![[assets/figures/papers/paper_list_l54_https_arxiv_org_abs_2206_07798/figures/016_Figure_16.jpg]]
*Figure 16: Stippling comparison of the zebra test image [de Goes et al. 2012]*

![[assets/figures/papers/paper_list_l54_https_arxiv_org_abs_2206_07798/figures/001_Figure_1.jpg]]
*Figure 1: Point distributions (1k sets) and power spectra (1k realizations) of different blue-noise optimization techniques including: (a) BNOT [de Goes et al. 2012], (b) KDM [Fattal 2011], (c) VnC [Ulichney 1993], (d) FPO [Schlömer et al. 2011], (e) BlueNets [Ahmed and Wonka 2021], and (f ) GBN (Ours). While the frequency power spectral plots may look similar, a closeup view reveals that the low-frequency energy in the middle is perfectly black in GBN, indicating very low low-frequency noise. (g) A log-log plot of the radial power spectra, using 1000 realizations of 4k point sets. Stratified sets are also included for comparison. We may distinguish two families of spectral profiles: polynomial (BNOT...*

![[assets/figures/papers/paper_list_l54_https_arxiv_org_abs_2206_07798/figures/003_Figure_3.jpg]]
*Figure 3: Actual frequency spectra we obtained for (a) various values of ?? in 2D, using 1k point sets and 10k iterations, and (b) different dimensions, with*

## 定位与知识库关联

GBN 的核心定位是**核方法蓝噪声优化的理论纠偏与工程补全**——它不是发明了新的蓝噪声范式，而是通过消除既往核方法中三个系统性设计缺陷，首次使核方法在噪声基底上超越长期被视为标杆的细胞方法 **BNOT**（de Goes et al., 2012）。理解这一突破需要明确 GBN 相对于两类基线改变了什么 slot，以及它在知识库中的挂载点。

### 相对已有方法的本质差异

**相对于核方法基线（KDM、VnC、BlueNets 等）**，GBN 改变的关键 slot 是**核支持范围**：从截断/局部邻域改为全支持（所有点对参与能量评估）。这一改变并非简单的计算量取舍，而是有深刻的频域因果——截断等价于在空间域乘矩形窗，在频域则卷积 sinc 函数，导致能量核的频率支撑展宽并引入旁瓣畸变（见图 4）。当这种畸变核被用作优化目标时，梯度下降实际上在最小化一个失真的频谱代理，因此永远无法收敛到理想的指数型蓝噪声谱。GBN 通过环面域的无限镜像求和（利用高斯核的可分离性高效计算），在物理上实现了全核支持，消除了这一根本性失真源。

**相对于 BNOT（细胞方法标杆）**，GBN 改变的是**频谱形状的理论上界**。BNOT 基于最优传输构造容量约束的幂图（power diagram），其功率谱在低频区以多项式形式增长（在 log-log 图上呈直线）；而 GBN 从理论上推导出高斯核蓝噪声的功率谱上界为 $P(\pmb{\omega}) \leq \epsilon e^{\sigma^{2}\|\pmb{\omega}\|^{2}}$，即**指数增长**，在低频区天然低于 BNOT 的多项式谱。这一理论优势在实验中兑现为约两个数量级的噪声基底降低（Fig. 1(e)）。

**相对于 BlueNets**（Ahmed and Wonka, 2021）——GBN 最直接的核方法前驱——GBN 继承其损失函数形式但改变了三个 slot：（1）将二进网（dyadic net）上的优化改为连续域梯度下降；（2）引入环面边界条件替代有界域；（3）通过 σ=1 的带宽选择和 10K 级别的迭代次数，将 BlueNets 未充分挖掘的潜力彻底释放。BlueNets 的低频噪声基底比 GBN 高约十个数量级，这一差距主要源于迭代不充分和核截断。

### 知识库挂载点

GBN 挂载在蓝噪声采样知识库的两个交叉节点上：

**节点一：核方法蓝噪声的频谱分析框架**。KDM（Fattal, 2011）首次建立核能量与功率谱的关联，但未给出闭合形式的频谱上界。GBN 通过推导 $P(\pmb{\omega}) \leq \epsilon |\hat{g}|^{-2}(\pmb{\omega})$ 并代入高斯核的频域表达式 $\hat{g}(\pmb{\omega}) = \exp(-\frac{\sigma^{2}}{2}\|\pmb{\omega}\|^{2})$，得到了显式的指数型上界。这一理论贡献将核方法蓝噪声从启发式工程提升为有理论保证的优化框架，后续工作可直接引用该上界作为质量基准。

**节点二：蓝噪声质量的理论极限与维度扩展**。BNOT 受限于最优传输的细胞结构，其多项式谱是高维扩展的内在瓶颈。GBN 利用高斯核的维度可分离性，将优化自然扩展至任意维度，且实验表明高维中收敛更快、噪声基底更低（Fig. 3(b)）。这为蒙特卡洛积分、高维采样等应用提供了 BNOT 无法覆盖的能力边界。

### 适用边界与后续启发

GBN 的适用边界由三个约束定义：（1）**时间复杂度为 $O(N^2)$**，尽管可通过 9σ 邻域截断缓解，但全核评估在十万级以上点集时仍面临计算压力；（2）**梯度下降的 Hessian 矩阵固有奇异**，导致后期收敛呈线性且无法完全停止，需要人工设定迭代预算；（3）**1D 蓝噪声的实现受限**，因一维邻域约束使点集自然趋向规则网格，仅能通过窄带频谱截断获得。

后续研究可从以下方向展开：将 GBN 的指数型频谱上界推广至其他核函数族，探索是否存在更优的核形状；利用高维加速收敛的特性，将蓝噪声样本作为高维空间中的“像素等价单元”用于数据表示和压缩；在自适应采样中结合更高效的密度估计算法，减少交替优化的迭代开销。论文本身提出的开放问题——高维加速收敛的深层原因——也指向了优化景观与自由度关系的理论空白。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Gaussian_Blue_Noise.pdf]]
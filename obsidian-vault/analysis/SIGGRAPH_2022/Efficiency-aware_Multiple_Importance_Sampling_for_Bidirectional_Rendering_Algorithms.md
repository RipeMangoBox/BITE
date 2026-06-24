---
title: Efficiency-aware Multiple Importance Sampling for Bidirectional Rendering Algorithms
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Efficiency_aware_Multiple_Importance_Sampling_for_Bidirectional_Rendering_Algorithms.pdf
project_link: "https://graphics.cg.uni-saarland.de/publications/grittmann-sig2022.html"
code_link: "https://doi.org/10.5281/zenodo.6514204"
aliases:
- EAMISEAM
- EAMISBRA
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 样本分配策略（即每种技术的采样数量及每像素的合并决策）直接决定渲染效率。通过自动为每个像素和全局选择最优的样本计数组合，可以在不牺牲鲁棒性的前提下大幅提升效率，并避免用户调参。
primary_logic: "利用一次廉价的导频渲染（如路径追踪）即可同时估计多种候选样本分配策略的效率（工作归一化二阶矩）。核心在于数值稳健的校正因子δ_{n,m}，它基于代理策略将导频样本的贡献映射到候选策略的矩估计，无需重新采样。从而可以极低开销穷举搜索最优策略，并自然地处理像素级和图像级的联合优化。"
claims:
- 在目标实践等简单场景中，未优化的 VCM 渲染速度仅为前向路径追踪的一半，而本文方法自动禁用低效技术，实现高效渲染。
- 在25个测试场景上，自动优化的 VCM 相对于路径追踪最多加速600倍，最差情况仅慢2%。
- 优化的 VCM 相对于未调优的 vanilla VCM 最高加速5.32倍，最差也提高12%。
- 优化的 BDPT 在22个场景中平均比未调优的 BDPT 快18%。
---

# Efficiency-aware Multiple Importance Sampling for Bidirectional Rendering Algorithms

> [!tip] 核心洞察
> 利用一次廉价的导频渲染（如路径追踪）即可同时估计多种候选样本分配策略的效率（工作归一化二阶矩）。核心在于数值稳健的校正因子δ_{n,m}，它基于代理策略将导频样本的贡献映射到候选策略的矩估计，无需重新采样。从而可以极低开销穷举搜索最优策略，并自然地处理像素级和图像级的联合优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向双向渲染算法的效率感知多重重要性采样 |
| 英文题名 | Efficiency-aware Multiple Importance Sampling for Bidirectional Rendering Algorithms |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://graphics.cg.uni-saarland.de/publications/grittmann-sig2022.html) · [Code](https://doi.org/10.5281/zenodo.6514204) · [Project](https://prime-itn.eu) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Efficiency-aware Multiple Importance Sampling (Efficiency-aware MIS) |
| Dataset | 25 test scenes, 22 test scenes |

> [!tip] 效果简介
> - 25 test scenes (VCM application) 上，relMSE speed-up vs. unidirectional PT Optimized VCM vs Unidirectional PT (Up to 600.77× (best), 0.98× (worst))；relMSE speed-up vs. vanilla VCM Optimized VCM vs Vanilla VCM (Up to 5.32× (best), 1.12× (worst))；relMSE after 60s, comparison across methods Ours (VCM) vs PT, vanilla VCM, Guided PT (Consistently outperforms PT and vanilla VCM; competitive with or better than Gu...)。
> - 22 test scenes (BDPT application) 上，relMSE speed-up vs. vanilla BDPT Optimized BDPT vs Vanilla BDPT (Average 1.18×)。

## 概要

复杂多重重要性采样（MIS）组合（尤其是顶点连接与合并 VCM）虽具鲁棒性，但在许多常见场景中效率远低于简单的前向路径追踪，且需用户手动调节参数，否则性能可能显著恶化。本文提出一种**效率感知的 MIS 优化方法**：利用一次廉价的导频渲染（通常为路径追踪），通过数值稳健的校正因子 $\delta_{\mathbf{n},\mathbf{m}}$ 将导频样本的贡献映射到候选策略的二阶矩估计，从而以极低开销穷举搜索最优的样本分配策略（包括每像素合并决策、光路数与连接数等全局参数），自动为每个像素和图像级选择使工作归一化相对二阶矩最小的配置。

在25个测试场景上，优化后的 VCM 相对于路径追踪**最多加速600倍**，最差情况仅慢2%；相对于未调优的 vanilla VCM 最高加速5.32倍，最差也提高12%。优化后的 BDPT 在22个场景中平均比未调优版本快18%。方法无需用户介入，自动在简单场景中禁用低效技术、在复杂光传输区域精准启用合并，实现了鲁棒性与效率的统一。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

双向渲染算法（如 VCM、BDPT）虽然理论上能处理复杂光传输，但在实践中存在一个被长期忽视的效率瓶颈：**复杂的多重重要性采样（MIS）组合在许多常见场景中效率远低于简单的前向路径追踪**。例如，在 Target Practice 这类简单场景中，未优化的 VCM 渲染速度仅为前向路径追踪的一半（Fig. 1）。这种效率损失源于手工固定的样本分配策略——用户需要手动调节光路数、连接数、是否启用光子映射等参数，否则大量计算资源会被浪费在低效技术上。这一瓶颈严重限制了双向算法的实用性。

![[assets/figures/papers/paper_list_l34_https_graphics_cg_uni_saarland_de_publications_grittmann_sig2022_html/figures/001_Figure_1.jpg]]
*Figure 1: Two scenes that are challenging to render efficiently without user guidance: The caustics and strong indirect illumination in the Fish scene (left) resolve much faster with a bidirectional method such as VCM. But the simpler Target Practice scene (right) renders 2 × slower with VCM than with forward path tracing. Our method renders both scenes efficiently by automatically setting the number of light subpaths to trace, the number of bidirectional connections to make, and in which pixels to perform photon density estimation (the ‘merge mask’ specifies a probability for performing a photon lookup in a pixel)*

本文的核心洞察在于：**样本分配策略（即每种技术的采样数量及每像素的合并决策）直接决定渲染效率**。通过自动为每个像素和全局选择最优的样本计数组合，可以在不牺牲鲁棒性的前提下大幅提升效率，并彻底消除用户调参需求。实现这一目标的关键技术挑战是：如何以极低开销估计多种候选策略的效率，从而在庞大搜索空间中快速定位最优解。

### 框架总览：效率感知的样本分配优化

本文提出**效率感知多重重要性采样（Efficiency-aware MIS）**，其核心流程分为三个阶段：

1. **导频渲染（Pilot rendering）**：使用指定的导频策略（通常为单向路径追踪）以 1 spp 渲染图像，收集样本轨迹用于后续矩估计。
2. **候选策略效率估计（Candidate moment estimation）**：利用导频样本和数值稳健的校正因子，为所有候选策略估计每个像素的二阶矩，开销极低。
3. **分层优化（Hierarchical optimization）**：先对每个像素选择最优的像素级样本计数（如合并决策），再固定像素级决策后选择最优的图像级样本计数（如光路数、连接数）。

这一框架的独特之处在于：**只需一次廉价的导频渲染，即可穷举搜索所有候选策略的效率**，无需为每个候选策略重新采样。其理论基础和实现细节如下。

### 问题形式化：工作归一化相对二阶矩最小化

考虑一个包含 $T$ 种采样技术的 MIS 估计器。设策略 $\mathbf{n} = (n_1, \ldots, n_T)$ 表示每种技术的样本数量，则多样本 MIS 估计器为：

$$\langle I \rangle _ { \mathbf { n } } = \sum _ { t = 1 } ^ { T } \sum _ { i = 1 } ^ { n _ { t } } w _ { \mathbf { n } , t } ( x _ { t , i } ) \frac { f ( x _ { t , i } ) } { n _ { t } \, p _ { t } ( x _ { t , i } ) } \tag{1}$$

其中 $w_{\mathbf{n}, t}(x)$ 为扩展平衡启发式权重：

$$w _ { \mathbf { n } , t } ( x ) = \frac { c _ { t } ( x ) \, n _ { t } \, p _ { t } ( x ) } { \sum _ { t ^ { \prime } } c _ { t ^ { \prime } } ( x ) \, n _ { t ^ { \prime } } \, p _ { t ^ { \prime } } ( x ) } \tag{2}$$

$c_t(x)$ 为校正因子，用于调整有效概率密度（如处理合并样本间的相关性）。

渲染效率通常定义为**工作归一化方差的倒数**，即单位计算成本所能达到的精度。由于方差估计昂贵，本文采用**二阶矩 $M[\langle I \rangle_{\mathbf{n}}]$** 作为方差的近似（因为 $\mathrm{Var} = M - I^2$，而 $I^2$ 在优化中为常数）。为平衡不同亮度区域的误差感知，进一步采用**相对二阶矩**（除以像素亮度平方 $I_j^2$），避免优化器过拟合高亮区域。

最终优化目标为最小化所有像素的工作归一化相对二阶矩之和：

$$\mathbf { n } = \arg \operatorname* { m i n } _ { { \bf n } } \; C ( { \bf n } ) \sum _ { j = 1 } ^ { P } \frac { M [ \langle I _ { j } \rangle _ { \bf n } ] } { I _ { j } ^ { 2 } } \tag{7}$$

其中 $C(\mathbf{n})$ 为策略 $\mathbf{n}$ 的计算成本启发式。

### 关键机制一：基于校正因子的跨策略矩估计

如何从导频策略 $\mathbf{m}$ 的样本估计候选策略 $\mathbf{n}$ 的二阶矩，是本文最核心的技术创新。直接计算需要重新采样，开销巨大。本文推导出一个巧妙的**校正因子**，将导频样本的贡献映射到候选策略的矩估计。

候选策略 $\mathbf{n}$ 的二阶矩可表达为导频策略 $\mathbf{m}$ 的积分形式：

$$M [ \langle I \rangle _ { \bf n } ] = \int _ { \cal X } \frac { f ^ { 2 } ( x ) \sum _ { t } c _ { t } ( x ) w _ { \bf m , \it t } } { \sum _ { t } c _ { t } ( x ) m _ { t } \rho _ { t } ( x ) } \, \delta _ { \bf n , \bf m } ( x ) \, \mathrm { d } x \tag{10}$$

其中 $\delta_{\mathbf{n}, \mathbf{m}}(x)$ 为校正因子。为获得数值稳健的估计，引入**代理策略 $\mathbf{a}$**，将校正因子重构为：

$$\delta _ { \mathbf { n } , \mathbf { m } } ( x ) = \frac { \left( \sum _ { t } \frac { m _ { t } } { a _ { t } } w _ { \mathbf { a } , t } ( x ) \right) ^ { 2 } \sum _ { t } c _ { t } ( x ) \frac { n _ { t } } { a _ { t } } w _ { \mathbf { a } , t } ( x ) } { \left( \sum _ { t } \frac { n _ { t } } { a _ { t } } w _ { \mathbf { a } , t } ( x ) \right) ^ { 2 } \sum _ { t } c _ { t } ( x ) \frac { m _ { t } } { a _ { t } } w _ { \mathbf { a } , t } ( x ) } \tag{11}$$

这一形式的关键优势在于：
- **数值稳健性**：避免直接处理数值悬殊的概率密度求和，代理策略分离出与候选策略无关的预计算项。
- **计算高效性**：与候选策略 $\mathbf{n}$ 相关的项仅涉及 $n_t$ 的简单代数运算，可极快评估大量候选策略。

最终，候选策略 $\mathbf{n}$ 的二阶矩估计仅需将导频策略的每个样本的平方贡献乘以校正因子：

$$\langle M [ \langle I \rangle _ { \mathbf { n } } ] \rangle _ { \mathbf { m } } = \sum _ { t } \sum _ { i = 1 } ^ { m _ { t } } \left( \frac { w _ { \mathbf { m } , t } ( x _ { t , i } ) f ( x _ { t , i } ) } { m _ { t } p _ { t } ( x _ { t , i } ) } \right) ^ { 2 } \delta _ { \mathbf { n } , \mathbf { m } } ( x _ { t , i } ) \tag{13}$$

这一机制实现了**一次采样，多次评估**：导频渲染的开销仅约 2%，却能同时估计数十种候选策略的效率。

### 关键机制二：分层优化与合并掩码滤波

优化过程采用**先像素级、后图像级**的分层策略（Algorithm 1）：

1. **像素级优化**：对每个像素 $j$，从候选策略集合 $\{\mathbf{n}^1, \ldots, \mathbf{n}^N\}$ 中选择使工作归一化矩最小的策略，确定每像素的样本计数 $\mathbf{p}_j$（如是否启用合并）。
2. **图像级优化**：固定所有像素的 $\mathbf{p}_j$ 后，累加所有像素的相对矩和成本，通过线性搜索选择最优的全局样本计数 $\mathbf{i}$（如光路数 $n$、连接数 $c$）。

对于 VCM 应用，像素级优化产生一个**合并掩码（merge mask）**，指示每个像素是否启用光子密度估计。由于掩码基于单次迭代的噪声矩估计，直接使用会产生伪影。本文设计了一个**滤波流水线**（Fig. 2）：
- 高斯模糊：平滑噪声
- 降采样：减少计算量
- 决策：基于阈值二值化
- 扩张：填充孔洞
- 高斯模糊：软化边界

![[assets/figures/papers/paper_list_l34_https_graphics_cg_uni_saarland_de_publications_grittmann_sig2022_html/figures/002_Figure_2.jpg]]
*Figure 2: When optimizing the pixel-level merging decisions ???? , we apply a simple filtering scheme to increase robustness. The top row shows the effect of the different operations on the merge mask and the equal-time error. The bottom row shows an overlay of the mask over the reference image, without filtering and after applying our filtering*

这一流水线使单次迭代的二阶矩估计接近通过 4096 次迭代获得的真实二阶矩掩码（Fig. 9），显著提高了鲁棒性。

### 关键机制三：相关感知权重与相对矩优化

两个关键设计确保了优化的可靠性：

**相关感知 MIS 权重**：在 VCM 中，顶点合并样本间存在相关性，经典平衡启发式会导致性能恶化。本文采用 Grittmann et al. (2021) 的相关感知权重，通过校正因子 $c_t(x)$ 降低相关样本的 MIS 权重。在灯罩场景中（Fig. 3），经典权重导致合并不当启用，而相关感知权重阻止了合并，保持了加速效果。

**相对矩优化**：使用绝对矩会导致优化器过拟合高亮区域（如天花板光带），只保留能渲染亮区域的技术而禁用其余（Fig. 4）。相对矩（除以 $I_j^2$）平衡了所有亮度区域的误差，在所有像素上取得更均衡的加速。

### VCM 应用的具体实现

对于 VCM，策略空间包含三个维度：
- 光源路径数 $n$
- 双向连接数 $c$
- 每像素合并决策 $\chi_j$（二元）

成本启发式基于实现拟合：

$$C ( n , c , \chi ) = C _ { \mathrm { l i g h t } } \tilde { n } _ { 1 } n + P \tilde { n } _ { \mathrm { c } } \bigl ( C _ { \mathrm { c a m } } + C _ { \mathrm { c o n } } c + C _ { \mathrm { m } } \tilde { n } _ { 1 } n \tilde { n } _ { \mathrm { m } } \sum _ { j } \chi _ { j } \bigr ) \tag{15}$$

参数通过 25 个测试场景拟合得到：$C_{\mathrm{cam}} = C_{\mathrm{light}} = 1$，$C_{\mathrm{con}} = 0.4$，$C_{\mathrm{m}} = 0.5$。

当导频渲染（PT）决定启用双向采样时，可采用**两阶段优化**：先用优化后的 VCM 导频再估计一次矩以细化合并掩码，并丢弃 PT 导频的结果。这适用于长渲染任务，因为 VCM 导频能生成更准确的合并掩码，但会引入约 3.3 倍单次迭代的额外开销。

### 方法边界与局限

本方法的优化粒度限于像素级二元合并决策和少数全局参数，无法针对每个路径长度或场景表面点进行更精细的分配。候选策略集合需要手动指定，若最优分配不在集合内则无法达到理论最佳性能。优化基于二阶矩近似方差，在某一技术的方差极低或样本严重相关时近似可能失效。成本模型依赖特定实现的启发式参数，需要在不同渲染器中重新拟合。

![[assets/figures/papers/paper_list_l34_https_graphics_cg_uni_saarland_de_publications_grittmann_sig2022_html/figures/004_Figure_3.jpg]]
*Figure 3: A scene rendered with and without a lamp shade. We show the merge masks and the rendering speed-up due to our optimization when using the classical balance heuristic and Grittmann et al.’s [2021] correlation-aware weights. The lamp shade causes severe covariance in the merging techniques, and our optimization can further worsen the already poor performance of the classical balance heuristic. Using the correlation-aware weights avoids this problem by assigning low MIS weights to the problematic samples. Hence our optimization does not enable merges because they would not contribute to the combined estimate*

![[assets/figures/papers/paper_list_l34_https_graphics_cg_uni_saarland_de_publications_grittmann_sig2022_html/figures/003_Figure_4.jpg]]
*Figure 4: In this scene, light tracing is the sole technique that can render the bright strip around the ceiling (top row, reduced exposure). Optimizing for absolute moments overfits on this bright region and disables all other techniques for the entire image. Using relative moments resolves the problem. Note that “Ours rel.” yields lower relMSE but higher MSE than vanilla VCM*

## 实验与关键发现

### 主结果：VCM 应用的效率加速

论文在 25 个测试场景上评估了优化后的 VCM（顶点连接与合并）渲染器，所有比较均在等时间（60 秒渲染，640×480 分辨率）下进行，使用 relMSE（相对均方误差）作为误差指标，并移除每张图中 0.01% 最高误差像素以抑制异常值影响。每个结果为 5 次运行的平均值。

**Table 1** 汇总了核心加速统计数据。相对于单向路径追踪（PT），优化后的 VCM 在最佳场景上实现了 **600.77×** 的加速，而在最差场景上也仅慢 **0.98×**（即几乎无性能损失）。这意味着本文方法自动识别出哪些场景适合双向方法、哪些场景只需前向路径追踪，从而在保持鲁棒性的同时大幅提升效率。相比之下，未经优化的 vanilla VCM 虽然在某些场景上优于 PT，但在简单场景（如 Target Practice）中渲染速度仅为 PT 的一半——这正是本文要解决的核心瓶颈。

相对于 vanilla VCM，优化后的 VCM 最高加速 **5.32×**，最差情况下也提高了 **1.12×**（即 12% 的性能提升）。这表明即使场景已经受益于双向方法，自动调整样本分配策略仍能带来显著增益。Fig. 6 的跨场景加速比条形图进一步显示，优化后的 VCM 在所有场景上一致地优于 PT 和 vanilla VCM，且与引导式路径追踪（Guided PT, Ruppert et al. 2020）相比也具备竞争力或更优。

![[assets/figures/papers/paper_list_l34_https_graphics_cg_uni_saarland_de_publications_grittmann_sig2022_html/figures/007_Figure_6.jpg]]
*Figure 6: Speed-up in terms of relMSE of different methods over unidirectional path tracing. ‘Guided PT’ is the path guiding method of Ruppert et al. [2020]. Our method consistently outperforms unidirectional PT and vanilla VCM*

### 主结果：BDPT 应用

在 22 个测试场景的 BDPT（双向路径追踪）应用中，优化后的 BDPT 相对于 vanilla BDPT 平均加速 **1.18×**。虽然加速幅度不如 VCM 应用显著（因为 BDPT 的样本分配自由度较小，仅涉及光路数和连接数的调整），但这一结果验证了效率感知 MIS 框架的通用性——它不依赖于特定的渲染算法，只要存在可调整的样本分配参数即可应用。

### 关键消融实验

**相对矩 vs. 绝对矩（Fig. 4）。** 优化目标的选择对结果有决定性影响。若使用绝对二阶矩（即直接最小化 MSE 的期望），优化器会过拟合图像中的高亮区域。在 Fig. 4 的场景中，天花板周围的亮带只能由光追踪（light tracing）技术渲染；绝对矩优化器因此在整个图像范围内禁用所有其他技术，只为亮带区域保留光追踪。这导致虽然绝对 MSE 降低，但 relMSE 恶化。使用相对矩（即除以像素亮度的平方）则避免了这一问题，在所有像素上取得更均衡的加速。这一设计选择是方法实用性的关键保障。

**相关感知 MIS 权重（Fig. 3）。** 顶点合并技术引入的样本间相关性会破坏经典平衡启发式的无偏性假设。在灯罩场景中，使用经典平衡启发式时，合并样本的协方差导致估计质量下降；本文优化器在经典权重下甚至会不当启用合并，进一步恶化性能。采用 Grittmann et al. (2021) 的相关感知权重后，优化器正确地为有问题的合并样本分配低 MIS 权重，从而阻止了合并不当启用，保持了加速效果。这一消融表明，效率感知 MIS 框架需要与能够处理样本相关性的权重函数配合，才能在实际场景中可靠工作。

**导频策略选择（Fig. 5）。** 导频渲染的策略选择直接影响优化开销和决策质量。使用 PT 作为导频时，优化器开销仅约 2%（主要是矩估计和搜索的计算成本），且 PT 导频提供的样本信息足以判断是否切换到双向方法。在 Modern Living Room 场景（不适合双向方法）中，PT 导频避免了浪费的双向样本；在 Sponge 场景（主要由焦散照明，PT 难以渲染）中，PT 导频仍能提供足够信息来更新采样策略，并实现比 vanilla VCM 更快的渲染。若直接使用 VCM 作为导频，虽然能生成更准确的合并掩码，但会引入约 3.3 倍单次迭代的额外开销（来自浪费的双向样本），不利于短渲染任务。论文采用两阶段策略：先用 PT 导频决策是否启用双向方法，若启用则再用优化后的 VCM 导频细化合并掩码。

**二阶矩近似的有效性（Fig. 7）。** 本文优化基于二阶矩（second moment）而非完整的方差估计，因为方差估计需要成对样本的协方差计算，开销远高于二阶矩。Fig. 7 的验证实验表明，基于二阶矩选择的样本数量（红色虚线标记）与使用昂贵完整方差计算得到的最优选择高度一致，且等时间比较中优化后的 BDPT 一致优于两种基线。这验证了二阶矩作为效率近似指标的充分性。

**合并掩码滤波流水线（Fig. 2, Fig. 9）。** 合并掩码基于单次迭代的噪声矩估计，直接使用会产生伪影和不稳定决策。论文设计的滤波流水线（高斯模糊 → 降采样 → 决策 → 扩张 → 高斯模糊）显著提高了鲁棒性。Fig. 9 的验证表明，经滤波的单次迭代掩码与通过 4096 次迭代收敛得到的真实掩码高度接近，证实了滤波流水线的有效性。

### 失败模式与适用边界

1. **近似失效风险。** 当某一技术的方差极低或样本间存在严重相关性时，二阶矩近似可能偏离真实方差，导致优化器做出次优决策。虽然相关感知权重缓解了部分问题，但极端情况下近似误差仍可能影响结果。

2. **合并掩码的噪声敏感性。** 在极低采样预算下（如 1 spp 导频），单次迭代的矩估计噪声较大，滤波流水线虽能改善但无法完全消除不准确的掩码决策。这在需要极短渲染时间的场景中可能成为瓶颈。

3. **优化粒度限制。** 当前方法仅在像素级别做二元合并决策，并在图像级别调整少数全局参数（光路数、连接数）。它无法针对同一像素内的不同路径长度或不同表面点进行差异化分配，因此当最优策略需要更细粒度的控制时，方法无法达到理论上界。

4. **成本模型的可移植性。** VCM 的成本启发式参数（$C_{\text{cam}}=C_{\text{light}}=1$, $C_{\text{con}}=0.4$, $C_m=0.5$）是通过在 25 个测试场景上拟合得到的，依赖于具体渲染器的实现细节。在不同渲染器或硬件平台上应用时，需要重新拟合这些参数。

5. **候选策略集合的完备性。** 优化器通过穷举搜索候选策略集合来选择最优分配。若真实最优分配不在预设的候选集合内，方法只能返回次优解。论文通过精心设计候选集合（覆盖从纯 PT 到全功能 VCM 的多种组合）来缓解此问题，但无法保证全局最优。

6. **静态场景假设。** 当前方法针对静态场景的单帧优化设计，未考虑动画或交互式渲染中的时间一致性需求。在连续帧间，逐帧独立优化可能导致合并掩码闪烁或样本分配策略的剧烈切换。

### 公平性保障

所有实验均采用等时间比较（60 秒或 10 秒渲染预算），使用 relMSE 作为统一的误差指标，并在 5 次独立运行上取平均。测试场景覆盖了从简单直接照明到复杂焦散和间接照明的广泛光照条件，确保了结论的普适性。

![[assets/figures/papers/paper_list_l34_https_graphics_cg_uni_saarland_de_publications_grittmann_sig2022_html/figures/006_Table_1.jpg]]
*Table 1: Statistics of the speed-up (higher is better) of our method across the 25 test scenes of the VCM application and the 22 scenes of the BDPT application. Computed after 60s rendering, averaged across 5 runs, using the relMSE error metric with outlier removal*

## 定位与知识库关联

### 与基线方法的本质差异

本文的核心贡献在于将双向渲染算法中**样本分配策略**这一长期由人工经验主导的“控制槽”替换为自动化的效率感知优化器。具体而言，本文改变了以下关键 slot：

**样本分配策略槽**：传统 VCM（Georgiev et al., 2012; Hachisuka et al., 2012）和 BDPT（Veach & Guibas, 1995）采用固定或启发式的手工设置——用户需预先指定光路数、连接数，并全局决定是否启用光子合并。本文将其替换为基于导频渲染的自动化搜索：通过一次廉价渲染（通常为单向路径追踪 PT）收集样本，利用数值稳健的校正因子 $\delta_{\mathbf{n},\mathbf{m}}$ 将导频样本的贡献映射到多个候选策略的二阶矩估计，从而以极低开销穷举搜索最优的每像素和图像级样本计数组合。这一替换使得系统能够根据场景特征自动决定是否启用双向技术、在哪些像素启用合并、以及分配多少光路和连接样本，无需用户干预。

**每像素合并决策槽**：传统 VCM 的合并是一个全局二元开关——要么所有像素都执行光子密度估计，要么全部禁用。本文将其替换为逐像素的合并掩码，通过从噪声二阶矩估计中提取、经高斯模糊-降采样-扩张-高斯模糊流水线滤波后，得到每像素的合并概率。这使得合并仅在焦散等需要效果的局部区域启用，避免了在无收益像素上的冗余计算。

**MIS 权重函数槽**：经典平衡启发式（$c_t(x)=1$）在合并样本存在相关性时会导致方差估计严重低估，进而误导优化器。本文采用 Grittmann et al.（2021）的相关感知权重作为校正因子 $c_t(x)$，使得优化器能正确识别合并样本的真实贡献，避免在相关性强的区域（如灯罩遮挡）错误启用合并。

**优化目标度量槽**：从无自动优化（固定分配）替换为最小化工作归一化相对二阶矩之和 $\sum_j M[\langle I_j\rangle_\mathbf{n}] / I_j^2 \times C(\mathbf{n})$。采用相对矩（除以像素亮度平方）而非绝对矩，是避免优化器过拟合亮区域的关键设计——绝对矩会导致优化器仅为亮区域保留技术而禁用其余，相对矩则实现了全图均衡加速。

### 知识库挂载点

本文可挂载至渲染领域知识库的以下节点：

1. **多重重要性采样（MIS）理论**：作为 Veach & Guibas（1995）平衡启发式的效率扩展，本文在 MIS 框架中引入了样本分配的自动优化维度，将 MIS 从“给定分配下的权重优化”推进到“自动选择最优分配”。校正因子 $\delta_{\mathbf{n},\mathbf{m}}$ 的推导为 MIS 的二阶矩分析提供了新的理论工具。

2. **双向渲染算法（VCM/BDPT）**：作为 VCM 和 BDPT 的实用化增强层，本文解决了这类算法长期存在的“场景依赖性强、需专家调参”的痛点。优化后的 VCM 在 25 个测试场景上相对路径追踪最多加速 600 倍，最差仅慢 2%，证明了自动化分配可大幅扩展双向方法的适用范围。

3. **路径引导方法**：与 Ruppert et al.（2020）的 Guided PT 形成互补——前者通过学习空间-方向采样分布加速 PT，本文通过自动选择技术组合和样本分配加速双向方法。两者可在不同维度上组合。

4. **渲染优化与自动调参**：本文提供了一种通用的“导频-估计-搜索”范式，可推广至其他 MIS 应用（如直接照明的光源选择、路径引导中的建议分布混合），其数值稳健的矩估计方案为后续自动化渲染研究提供了可复用的技术组件。

### 适用边界与局限

**适用边界**：
- 适用于静态场景的单帧渲染优化，特别是光照复杂且难以预判最佳技术组合的场景。
- 优化效果依赖于候选策略集合的覆盖度——若最优分配不在预设候选集中，方法无法达到理论最佳。
- 成本模型 $C(\mathbf{n})$ 依赖特定实现的启发式参数（如 $C_{\text{con}}=0.4$, $C_m=0.5$），需在不同渲染器中重新拟合，限制了即插即用的可移植性。

**已知失效模式**：
- 当某技术的方差极低或样本严重相关时，基于二阶矩的方差近似可能失效，导致次优决策。
- 合并掩码依赖单次迭代的噪声矩估计，尽管采用了滤波流水线，在极低采样下仍可能产生不准确掩码。
- 选择 VCM 作为导频时，优化过程引入约 3.3 倍单次迭代开销，不利于极短渲染任务（<10s）。
- 优化粒度限于像素级二元合并决策和少数全局参数，无法针对每个路径长度或场景表面点进行更精细分配。

### 后续研究启发

本文打开的关键后续方向包括：

1. **更细粒度的分配优化**：将优化拓展到路径空间而非屏幕空间，实现同一像素内不同路径长度的差异化样本分配，或基于材质/光路特征设计启发式预先排除不必要的合并区域。

2. **低开销的矩估计改进**：使用轻量级神经网络去噪器替代当前线性滤波，从单样本矩估计中重建更精确的逐像素合并决策；或将图像处理操作移至 GPU 以大幅降低优化阶段的时间成本。

3. **偏差感知的优化目标**：将顶点合并引入的偏差纳入效率目标，避免在偏差显著区域过度使用合并。

4. **时域扩展**：将优化信息在连续帧间复用或平滑过渡，以支持动画和交互式渲染场景。

5. **更通用的范式推广**：将“导频-估计-搜索”范式应用于其他 MIS 应用（如光源选择、建议分布混合），验证其数值稳健性和加速效果。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Efficiency_aware_Multiple_Importance_Sampling_for_Bidirectional_Rendering_Algorithms.pdf]]
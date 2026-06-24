---
title: Efficient Estimation of Boundary Integrals for Path-space Differentiable Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Efficient_Estimation_of_Boundary_Integrals_for_Path_space_Differentiable_Rendering.pdf
project_link: "https://shuangz.com/projects/psdr-aq-sg22/"
code_link: null
aliases:
- EEBIPSDR
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在主样本空间构建自适应KD树，以分段线性方式逼近目标函数，并利用多重重要性采样（MIS）融合光照采样和方向采样，从而显著降低边界积分估计的方差；可选的边缘排序进一步改善了主样本空间映射的连续性。
primary_logic: 将边界积分重新参数化为主样本空间上的积分，并使用KD树自适应分区，根据局部拟合误差动态细分区域，在目标函数变化剧烈的区域分配更多样本，同时利用MIS结合互补的边界方向采样策略，避免单一采样方式在复杂光照下的失败。
claims:
- "在等时条件下，本方法生成的边界分量梯度图像比Zhang et al. [2020]的方法噪声更低、更清晰。"
- 与warped-area sampling (WAS)相比，本方法在等样本数下产生更干净的梯度结果且速度显著更快；在等时条件下优势更大。
- 消融实验证明，边缘排序和MIS均可独立降低方差，而本方法结合两者可进一步获得更优的梯度估计，并在逆渲染中实现更快收敛和更高重建精度。
- "在多个逆渲染任务中（如环境光照下的几何恢复），采用本方法估计的梯度使优化收敛速度远超Zhang et al. [2020]的PSDR，且最终重建的Chamfer距离更小。"
---

# Efficient Estimation of Boundary Integrals for Path-space Differentiable Rendering

> [!tip] 核心洞察
> 将边界积分重新参数化为主样本空间上的积分，并使用KD树自适应分区，根据局部拟合误差动态细分区域，在目标函数变化剧烈的区域分配更多样本，同时利用MIS结合互补的边界方向采样策略，避免单一采样方式在复杂光照下的失败。

| 字段 | 内容 |
|------|------|
| 中文题名 | 路径空间可微渲染的边界积分高效估计 |
| 英文题名 | Efficient Estimation of Boundary Integrals for Path-space Differentiable Rendering |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://shuangz.com/projects/psdr-aq-sg22/) · [Project](https://shuangz.com/projects/psdr-aq-sg22/") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 我们的方法（基于主样本空间KD树引导的边界路径积分高效估计） |
| Dataset | 多个测试场景（包括Bunny、Dragon等）上的边界梯度图像比较, 逆渲染优化（多个合成场景，如Jumpy Dumpty、Klee、Bunny in glass等） |

> [!tip] 效果简介
> - 多个测试场景（包括Bunny、Dragon等）上的边界梯度图像比较 上，视觉质量/方差 本方法生成梯度图像噪声极低，边缘清晰。 vs PSDR [Zhang et al. 2020] / WAS [Bangaru et al. 2020] (等时条件下噪声显著降低，等样本下速度更快且质量更高。)。
> - 逆渲染优化（多个合成场景，如Jumpy Dumpty、Klee、Bunny in glass等） 上，Chamfer距离 / 最终重建精度 采用本方法估计的梯度，优化收敛更快且最终重建几何误差更小。 vs PSDR [Zhang et al. 2020] (显著更低的梯度噪声带来更快的收敛和更精确的重建。)。

## 概要

在物理可微渲染中，处理几何参数（如网格顶点位置）的梯度时，边界路径积分至关重要，但其蒙特卡洛估计极具挑战：被积函数高度复杂、不连续且呈现锐利峰值，直接均匀采样或固定网格近似均导致极高方差。本文提出一种基于主样本空间引导的高效边界积分估计方法。核心思路是将边界积分重参数化到三维主样本空间，利用自适应KD树以分段线性方式逼近目标函数，在变化剧烈区域动态分配更多样本；同时引入多重重要性采样融合光照采样与方向采样两种互补策略，避免单一采样在遮挡等复杂情况下的失效；并辅以可选的边缘排序预处理，改善主样本空间映射的连续性。实验表明，在等时条件下，本方法生成的边界梯度图像比Zhang et al. (2020)的PSDR和Bangaru et al. (2020)的Warped-Area Sampling噪声显著更低、边缘更清晰。消融实验证实，边缘排序和MIS各自独立降低方差，组合使用效果最优。在多个逆渲染任务中，采用本方法估计的梯度使优化收敛速度远超PSDR，最终重建几何的Chamfer距离更小。该方法定位为对PSDR边界积分估计模块的改进，将固定网格分段常数近似替换为自适应KD树引导的采样，并增加了MIS组合与边缘排序两个新组件。

## 核心方法与创新机理

### 一、问题瓶颈与核心思路

在基于物理的可微渲染中，对场景几何参数（如网格顶点位置）求导会产生路径空间边界上的积分项。根据 Zhang et al. (2020) 的微分路径积分公式，像素强度对场景参数 $\theta$ 的梯度可分解为内部项和边界项：

$$\frac{\mathrm{d}I}{\mathrm{d}\theta} = \left( \int_{\hat{\Omega}} \frac{\partial \hat{f}}{\partial \theta} \mathrm{d}\mu(\bar{p}) \right) + \int_{\partial\hat{\Omega}} \hat{f}^{\mathrm{B}} \hat{f}^{\mathrm{S}} \hat{f}^{\mathrm{D}} \mathrm{d}\dot{\mu}$$

其中边界项的被积函数 $\Gamma(u_1, u_2) = \hat{f}^{\mathrm{B}} J^{\mathrm{B}} \, h^{\mathrm{S}} h^{\mathrm{D}}$ 高度复杂、不连续且具有锐利峰值，直接均匀采样或使用固定网格近似（如 Zhang et al. 的规则 3D 网格分段常数近似）均会产生极高方差。

本文的核心洞察是：将边界积分重新参数化到三维主样本空间 $[0,1)^3$ 上，并利用自适应 KD 树以分段线性方式逼近目标函数，从而在函数变化剧烈的区域自动分配更多样本；同时引入多重重要性采样（MIS）融合互补的边界方向采样策略，避免单一采样方式在复杂光照下的系统性失败。

### 二、主样本空间重参数化

边界路径由边界段 $x^{\mathrm{B}}$ 和边界方向 $\omega^{\mathrm{B}}$ 唯一定义。$x^{\mathrm{B}}$ 必须位于某多边形面的边上（1D 流形），$\omega^{\mathrm{B}}$ 取自 2D 流形，因此边界积分天然可映射到三维主样本空间：

$$\int_{[0,1)^3} F(u_1, u_2) \mathrm{d}u_2 \mathrm{d}u_1$$

其中 $u_1 \in [0,1)$ 参数化所有多边形边的集合，$u_2 \in [0,1)^2$ 参数化边界方向。这一重参数化将复杂的边界采样问题转化为在单位立方体上构造重要性分布的问题。

### 三、自适应 KD 树引导采样（Changed Slot 1）

**基线方法（Zhang et al. 2020）** 在规则 3D 网格上对目标函数进行分段常数近似，网格分辨率固定，无法适应被积函数的局部变化。

**本方法** 递归构建 KD 树，以分段线性（三线性）方式自适应逼近目标函数。由于真实被积函数 $\Gamma$ 在采样前未知，方法使用光子映射得到的近似函数 $\tilde{F}$ 作为引导目标：

$$\tilde{F}(u_1, u_2) = |\hat{f}^{\mathrm{B}}| J^{\mathrm{B}} \tilde{h}^{\mathrm{S}} \tilde{h}^{\mathrm{D}}$$

其中 $\tilde{h}^{\mathrm{S}}$ 和 $\tilde{h}^{\mathrm{D}}$ 分别通过光子图和进口子图（importon map）预计算得到，用于近似源子路径和探测器子路径的贡献。

KD 树构建过程（Algorithm 1）的核心逻辑是：对每个节点，计算当前区域内 $\tilde{F}$ 的三线性拟合，并评估拟合误差；若误差超过阈值，沿误差最大的轴将区域一分为二，递归构建子树。这一过程确保计算资源自动集中于 $\tilde{F}$ 变化剧烈的区域——通常是边界贡献 $|\hat{f}^{\mathrm{B}}| J^{\mathrm{B}}$ 出现锐利峰值的位置。采样时，先按叶节点存储的积分估计值比例选择叶节点，再通过反演方法从该叶节点的三线性拟合中抽取 $(u_1, u_2)$ 样本，最后映射回边界段。

### 四、多重重要性采样融合（Changed Slot 2）

边界方向 $\omega^{\mathrm{B}}$ 的采样存在两种互补策略：

- **光照采样**：先在光源上采样点 $x_0^{\mathrm{S}}$，再设 $\omega^{\mathrm{B}} = \text{normalized}(x_0^{\mathrm{S}} - x^{\mathrm{B}})$。该方法在光源可见时有效，但当采样方向导致边界段穿透物体时会产生无效样本（Fig. 3）。
- **方向采样**：直接在半球上采样 $\omega^{\mathrm{B}}$。该方法始终有效，但在光源较小或遮挡严重时效率低下。

![[assets/figures/papers/paper_list_l35_https_shuangz_com_projects_psdr_aq_sg22/figures/004_Figure_3.jpg]]
*Figure 3: When sampling the direction*

**基线方法（Zhang et al. 2020）** 仅采用光照采样，在复杂遮挡场景中产生大量无效样本。

**本方法** 利用 MIS 框架融合两种策略：分别为光照采样和方向采样构建独立的目标函数 $\tilde{F}_{\mathrm{light}}$ 和 $\tilde{F}_{\mathrm{dir}}$，各自使用独立的 KD 树进行引导采样，最终通过平衡启发式权重合并两个估计器。两个目标函数的区别仅在于雅可比项 $J^{\mathrm{B}}$ 的计算方式不同——光照采样使用从边界点到光源点的映射雅可比 $J_{\mathrm{light}}^{\mathrm{B}}$，方向采样使用直接方向采样的雅可比 $J_{\mathrm{dir}}^{\mathrm{B}}$。MIS 权重自动在两种策略间分配样本：当某一策略在当前区域失效时，另一策略自然获得更高权重。

### 五、边缘排序预处理（Changed Slot 3）

主样本空间中 $u_1$ 到多边形边的映射连续性直接影响 $\tilde{F}$ 的光滑程度。若相邻 $u_1$ 值对应空间上相距甚远的边，则 $\tilde{F}$ 会引入额外的不连续性，降低 KD 树拟合效率。

**基线方法** 未对边进行排序，映射连续性差。

**本方法** 在预处理阶段对网格的所有边进行排序以形成连续链（Fig. 4）：从一个未访问的边出发，贪心地选择共享顶点的相邻边，直至无法继续，然后开始新链。所有链首尾相连后，$u_1$ 沿链线性推进，相邻 $u_1$ 值对应空间上邻近的边，显著改善 $\tilde{F}$ 的连续性。这一步骤要求网格为场对齐（field-aligned），对于非结构化输入可能需要预重网格化。

### 六、完整推理路径

单次梯度估计的完整流程为：

1. **预计算阶段**：生成光子图和进口子图（$\tilde{h}^{\mathrm{S}}$、$\tilde{h}^{\mathrm{D}}$）；对网格边执行排序形成链；分别为 $\tilde{F}_{\mathrm{light}}$ 和 $\tilde{F}_{\mathrm{dir}}$ 构建 KD 树。
2. **边界段采样**：分别从两个 KD 树中采样叶节点，反演三线性拟合得到 $(u_1, u_2)$，映射为边界段 $(x^{\mathrm{B}}, \omega^{\mathrm{B}})$。
3. **子路径构建**：给定边界段后，使用标准单向或双向路径追踪构建源子路径和探测器子路径。
4. **MIS 组合**：分别计算两个策略的估计器值，通过平衡启发式权重合并，得到无偏的边界积分估计。
5. **梯度合成**：将边界项估计与内部项估计相加，得到完整梯度。

各模块间的因果关系清晰：边缘排序改善 $\tilde{F}$ 的光滑性 → KD 树能以更少的分区达到同等拟合精度 → 采样分布更贴近真实被积函数 → 估计方差降低；MIS 融合互补策略 → 避免单一策略在特定光照条件下的系统性失败 → 估计鲁棒性提升。两者协同作用：边缘排序使两个目标函数都更易拟合，MIS 则确保在两种策略的优势区域分别获得高质量样本。

![[assets/figures/papers/paper_list_l35_https_shuangz_com_projects_psdr_aq_sg22/figures/006_Figure_4.jpg]]
*Figure 4: Edge sorting: (a) Sorting the edges of a mesh allows us to create long “chains” (marked in red), improving the continuity of*

## 实验与关键发现

### 核心对比：梯度图像质量

本方法最直接的性能体现在边界分量梯度图像的估计质量上。在等时条件下，与 **PSDR**（Zhang et al., SIGGRAPH 2020）的固定网格近似相比，本方法生成的梯度图像噪声显著更低、边缘更清晰（Fig. 6）。PSDR在3D规则网格上对目标函数做分段常数近似，当目标函数在局部剧烈变化时，固定分辨率无法有效捕捉峰值，导致高方差；而本方法通过自适应KD树以分段线性方式逼近目标函数，在高误差区域自动细分，将样本集中于贡献大的区域。

![[assets/figures/papers/paper_list_l35_https_shuangz_com_projects_psdr_aq_sg22/figures/007_Figure_6.jpg]]
*Figure 6: Differentiable-rendering comparisons: We compare boundary-component-only gradient images generated with our technique (c) with Zhang et al.’s method [2020] indicated as “PSDR” (b1, b2). At equal-time, our technique produces significantly cleaner gradient estimates (b2, c)*

与 **Warped-Area Sampling (WAS)**（Bangaru et al., 2020）的对比进一步验证了效率优势（Fig. 7）：在等样本数条件下，本方法产生更干净的梯度结果且速度显著更快；在等时条件下，质量差距进一步拉大。WAS基于重参数化处理可微渲染，但其采样策略未针对边界积分的特殊结构（被积函数高度不连续且存在锐利峰值）做专门优化，而本方法的主样本空间引导直接针对该瓶颈设计。

![[assets/figures/papers/paper_list_l35_https_shuangz_com_projects_psdr_aq_sg22/figures/008_Figure_7.jpg]]
*Figure 7: Differentiable-rendering comparisons: We compare gradient images generated with our technique and the warped-area sampling (WAS) method [Bangaru et al. 2020]. With equal sample counts, our technique produces cleaner results while being significantly faster. At equal-time, the quality differences become even greater*

### 消融实验：边缘排序与MIS的独立贡献

消融实验系统评估了两个关键模块的独立与联合效应（Fig. 8, Fig. 9）。

![[assets/figures/papers/paper_list_l35_https_shuangz_com_projects_psdr_aq_sg22/figures/009_Figure_8.jpg]]
*Figure 8: Ablation study (differentiable rendering): We evaluate the effectiveness of our edge-sorting (§4.3) and multiple-importance-sampling (§4.2) steps. All results in columns (b–d) are generated in equal time*

**边缘排序**（§4.3）通过预处理将网格边缘组织为连续链，改善了从主样本空间到边界点的映射连续性。Fig. 5以光滑材质蛋形场景展示了排序前后的映射差异：未排序时，相邻主样本可能映射到空间距离很远的边界点，导致目标函数出现大量人为不连续性；排序后映射更连续，目标函数更平滑，KD树的拟合更有效。值得注意的是，边缘排序对PSDR的固定网格方法几乎没有提升（Fig. 8顶行 vs 底行），说明其收益依赖于自适应分区的引导框架，而非通用改进。

**多重重要性采样（MIS）**（§4.2）结合了光照采样和方向采样两种互补策略。单独的光照采样在存在遮挡时会产生大量无效样本（Fig. 3），而单独的方向采样在复杂间接光照下效率低下。MIS通过平衡启发式权重融合两个估计器，使两者在各自有利的区域主导采样。Fig. 8-d显示，MIS配置的梯度图像噪声明显低于任一单一采样策略。

**联合效应**：边缘排序和MIS结合使用可获得最优梯度估计（Fig. 8最右列）。这一趋势在逆渲染消融中得到进一步验证（Fig. 9）：使用MIS和边缘排序的配置均能提供更准确的形状重建（以Chamfer距离衡量），两者组合的最终重建精度最高。

### 逆渲染收敛速度与重建精度

在多个逆渲染任务中，采用本方法估计的梯度使优化收敛速度远超PSDR（Fig. 10, Fig. 11）。以Chamfer距离作为评估指标（仅用于评估，不参与优化），本方法在所有测试场景（Jumpy Dumpty、Klee、Bunny in glass等）中均实现了更快的误差下降和更低的最终重建误差。Table 2提供了详细的优化配置与性能统计：引导时间（每迭代KD树构建）和渲染时间分开统计，所有实验在配备AMD Ryzen Threadripper Pro 3975WX CPU（32核）和Nvidia RTX Titan GPU的工作站上进行。

![[assets/figures/papers/paper_list_l35_https_shuangz_com_projects_psdr_aq_sg22/figures/013_Figure_10.jpg]]
*Figure 10: Inverse-rendering comparison: We solve inverse-rendering problems using gradients estimated using our technique and PSDR [Zhang et al. 2020]. For each example, we use identical target images (with one shown), losses, and optimization settings (e.g., initial states, optimizers, and learning rates). At equal-time, our technique has allowed significantly faster convergence for all examples. The plotted mesh error captures the Chamfer distance [Barrow et al. 1977] between the reconstructed and groundtruth geometries (normalized so that the GT has a unit bounding box). We use this information only for evaluation, and not for optimization*

公平性保障：所有对比实验均在等时条件下进行；逆渲染优化使用相同的初始网格、优化器（Nicolet et al., 2021的方法）、学习率和迭代次数；内部项估计统一采用Zhang et al. 2020的方法，仅改变边界积分估计部分。

### 适用边界与失效模式

**表面光传输限制**：本方法仅针对表面光传输设计。对于包含参与介质的场景，主样本空间维数从3升至5，引导难度显著增大，现有KD树构建和采样策略无法直接扩展。这是方法的核心适用范围边界。

**子路径采样未优化**：本方法仅改进了边界段的采样分布，源子路径和探测器子路径的采样仍使用标准方式。在源/探测器子路径贡献占主导的场景中，边界段采样的改进对整体梯度估计的收益可能有限。

**网格结构要求**：边缘排序要求网格为场对齐（field-aligned），对于非结构化的输入网格可能需要预重网格化处理。每迭代几何变化时，排序需要重新计算，其开销在动态几何场景中可能成为负担。

**引导构建开销**：KD树构建需要预计算光子图和进口子图来近似源/探测器贡献（Eq. 11），这一预处理步骤引入了额外的时间开销（Table 2中的“guiding time”）。在迭代次数较少或场景简单的应用中，引导构建的开销可能抵消采样效率提升带来的收益。

## 定位与知识库关联

本文的核心贡献在于，为路径空间可微渲染中的**边界路径积分**提供了一种高效、低方差的蒙特卡洛估计方法。其相对于已有工作的本质差异，集中体现在**边界段采样分布近似**这一关键slot上，并在**边界方向采样策略**和**主样本空间映射连续性**两个辅助slot上引入了互补性改进。

### 相对于已有方法的本质差异

在路径空间可微渲染的框架下，Zhang et al.（SIGGRAPH 2020）提出的**PSDR**方法将梯度分解为内部项和边界项。对于边界项，PSDR采用在**规则3D网格**上对目标函数进行**分段常数近似**的策略来引导采样。这种固定分辨率的均匀分区方式，无法适应目标函数在场景几何边缘、高光区域等处出现的锐利峰值和剧烈变化，导致在这些关键区域欠采样，而在平滑区域过采样，最终产生高方差的梯度估计。

本文方法将这一slot替换为基于**自适应KD树**的**分段线性（三线性）近似**。KD树根据局部拟合误差动态决定细分——在目标函数变化剧烈的区域自动加深细分，在平坦区域保持粗粒度——从而将计算资源集中在对梯度估计方差贡献最大的区域。这一改变是方差降低的核心驱动力。

在**边界方向采样策略**这一slot上，PSDR仅采用**光照采样**（即先采样光源点，再确定边界方向），这在遮挡复杂或光源分布极不均匀的场景中会产生大量无效样本（边界段穿透物体）。Bangaru et al.（ACM Trans. Graph. 2020）的**Warped-Area Sampling（WAS）**方法则基于重参数化，但未专门针对边界路径的采样策略进行优化。本文引入**多重重要性采样（MIS）**，同时构建针对光照采样和方向采样的两个独立目标函数 $\tilde{F}_{\mathrm{light}}$ 和 $\tilde{F}_{\mathrm{dir}}$，并通过平衡启发式权重融合两个估计器。这使方法能在不同光照和几何配置下自动选择更有效的采样策略，避免单一策略的灾难性失效。

在**主样本空间映射连续性**这一slot上，已有方法均未对多边形边的排序进行处理。本文引入可选的**边缘排序**预处理步骤，将网格边组织成连续链，改善了从主样本 $u_1$ 到边界点 $x^B$ 的映射连续性，减少了目标函数的人为不连续性，从而进一步提升了KD树近似的精度和采样效率。

### 知识库挂载点

本方法在知识库中的核心挂载点可定位为：**可微渲染 → 物理基可微渲染 → 路径空间方法 → 边界积分估计**。

具体而言：
- **上游依赖**：方法直接建立在Zhang et al.（2020）的微分路径积分理论框架之上，继承了其材料形式重参数化、内部项/边界项分解，以及基于光子映射的源/探测器子路径近似 $\tilde{h}^{\mathrm{S}}$ 和 $\tilde{h}^{\mathrm{D}}$。
- **采样技术谱系**：KD树引导采样属于**自适应重要性采样**家族，与Müller et al.（SIGGRAPH 2017）在路径引导中使用的SD-tree等方法共享“根据被积函数局部变化自适应分配样本”的核心思想，但本文将其应用到了边界路径积分这一此前未被充分探索的特定子问题上。
- **MIS融合**：将MIS与引导采样结合，属于**组合采样策略**的技术路线，与Veach & Guibas（SIGGRAPH 1995）的经典MIS框架以及后续在渲染中的多种应用一脉相承。

### 适用边界

本方法的设计和验证存在明确的适用范围限制：
- **仅适用于表面光传输**。对于包含参与介质（体积散射）的场景，主样本空间维数从3升至5，目标函数的复杂度急剧增加，KD树构建和引导采样的难度显著增大，当前方法无法直接扩展。
- **边缘排序要求场对齐网格**。对于非结构化的输入网格，可能需要预重网格化才能有效应用边缘排序带来的连续性改善。
- **仅改进了边界段采样**。源子路径和探测器子路径的采样仍使用标准方式，这两部分在特定场景（如复杂间接光照）中可能成为新的方差瓶颈。

### 后续研究启发

本工作为可微渲染的采样效率提升开辟了若干后续方向：
1. **向体积光传输的扩展**：如何将自适应主样本空间引导推广到5维采样空间，处理参与介质场景下的边界积分估计，是一个直接但极具挑战的开放问题。
2. **与MCMC方法的结合**：当前方法基于独立采样，若能将其引导分布作为MCMC采样的提议分布，有望在极低样本预算下进一步降低方差。
3. **端到端的全路径引导**：将KD树引导的思想扩展到源/探测器子路径的采样中，实现边界段和子路径的联合重要性采样，可能在更广泛的逆渲染问题中实现端到端的方差缩减。
4. **动态几何场景**：边缘排序在每迭代几何更新的逆渲染优化中的计算开销和适用性，值得进一步探索和优化。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Efficient_Estimation_of_Boundary_Integrals_for_Path_space_Differentiable_Rendering.pdf]]
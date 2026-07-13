---
title: Capturing and Animation of Body and Clothing from Monocular Video
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Capturing_and_Animation_of_Body_and_Clothing_from_Monocular_Video.pdf
project_link: null
code_link: "https://github.com/YadiraF/SCARF"
aliases:
- SSCARF
- CABCFMV
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用显式网格身体 + 隐式NeRF服装的混合表示，配合针对性的分离损失和网格集成体积渲染。
primary_logic: 人体身体形状规律，适合统计网格模型（如SMPL‑X）；服装拓扑多变、材质复杂，更适合神经辐射场（NeRF）；将两者结合可以兼顾可驱动性与外观保真度。
claims:
- 混合表示在面部、手部和服装几何上显著优于纯NeRF或纯网格表示。
- 在People‑Snapshot数据集的新视图合成任务上，SCARF在PSNR/SSIM/LPIPS上优于主流方法。
- 服装重建质量明显高于SMPLicit和BCNet，可处理裙装等复杂拓扑。
- People‑Snapshot (novel view synthesis) 上 PSNR / SSIM / LPIPS (male‑3‑casual, male‑4‑casual, female‑3... = 30.59/0.977/0.024; 28.99/0.970/0.025; 30.14/0.977/0.028; 29...
---

# Capturing and Animation of Body and Clothing from Monocular Video

> [!tip] 核心洞察
> 人体身体形状规律，适合统计网格模型（如SMPL‑X）；服装拓扑多变、材质复杂，更适合神经辐射场（NeRF）；将两者结合可以兼顾可驱动性与外观保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 单目视频中身体与服装的捕捉与动画化 |
| 英文题名 | Capturing and Animation of Body and Clothing from Monocular Video |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2210.01868) · [Code](https://github.com/YadiraF/SCARF) · [paper](https://arxiv.org/abs/2210.01868") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SCARF (Segmented Clothed Avatar Radiance Field) |
| Dataset | People‑Snapshot |

> [!tip] 效果简介
> - People‑Snapshot (novel view synthesis) 上，PSNR / SSIM / LPIPS (male‑3‑casual, male‑4‑casual, female‑3‑casual, female‑4‑ca... 30.59/0.977/0.024; 28.99/0.970/0.025; 30.14/0.977/0.028; 29.96/0.972/0.026 vs Anim‑NeRF, Neural Body, HumanNeRF (具体数值见表1) (定性/定量上均达到最优或领先)。

## 概要

**问题**：从单目视频同时恢复可自由驱动的人体模型与可独立迁移的服装外观，是数字人建模的核心难题。现有方法要么采用整体隐式表示（如NeRF），无法分离身体与服装；要么依赖3D扫描训练的显式分层模型，泛化能力弱且缺乏外观信息。

**方法**：本文提出**SCARF**（Segmented Clothed Avatar Radiance Field），一种**显式网格身体 + 隐式NeRF服装**的混合表示。身体部分使用带可学习顶点偏移的SMPL-X参数化网格，保证面部、手部的精细驱动能力；服装部分则由标准空间中的NeRF建模，配合非刚体变形场处理宽松衣物的残余形变。通过**网格集成体积渲染**将两者融合——光线碰到身体网格时提前终止并用网格颜色替代NeRF颜色——并结合服装分割掩码损失、可见身体损失等分离约束，迫使NeRF仅学习服装区域。整个过程仅需单目RGB视频与服装分割掩码，无需任何3D监督。

**结果**：在People-Snapshot数据集的新视图合成任务上，SCARF在PSNR/SSIM/LPIPS指标上全面优于Anim-NeRF、Neural Body、HumanNeRF等主流方法。服装重建质量显著超过SMPLicit和BCNet，可处理裙装等复杂拓扑。消融实验证实，混合表示相比纯NeRF或纯网格表示，在面部、手部与服装几何上均有明显提升。

**定位**：SCARF在“身体-服装分离表示”这一关键设计槽位上做出改进——将传统的整体NeRF或纯网格方案替换为网格+NeRF的混合架构，并配套设计了针对性的分离损失与渲染策略。该方法属于单目视频驱动的可动画化虚拟人重建方向，后续可向多材质建模、实时推理等方向延伸。

## 核心方法与创新机理

### 瓶颈与核心思路

从单目视频重建可驱动的全身虚拟化身面临一个根本性矛盾：**人体身体形状规律性强**，适合用统计网格模型（如SMPL‑X）表达，而**服装拓扑多变、材质复杂**，难以用固定拓扑的网格准确建模。现有方法要么采用整体神经辐射场（NeRF）隐式表示全身，无法分离身体与服装，导致面部和手部细节模糊（如Anim‑NeRF）；要么基于大规模3D扫描数据训练分层网格模型（如SMPLicit、BCNet），泛化性差且缺乏外观重建能力。SCARF的核心洞察是：**将显式网格身体与隐式NeRF服装结合**，利用前者保证身体的可驱动性和面部/手部精度，利用后者灵活捕捉服装的任意拓扑和复杂外观。

### 混合表示架构

SCARF的表示由三个互补层次构成：

**第一层：SMPL‑X参数化身体网格。** 身体采用SMPL‑X模型表达，包含形状参数$\beta$、姿态参数$\theta$、表情参数$\psi$以及可学习的顶点偏移$\mathrm{O}$。带偏移的模板顶点通过线性混合蒙皮（LBS）变换到观测空间：

$$M(\beta,\theta,\psi,\mathrm{O}) = \mathrm{LBS}(T_P(\beta,\theta,\psi,\mathrm{O}), \mathbf{J}(\beta), \theta, \mathcal{W})$$

其中模板顶点$T_P$由基础模板$\mathrm{T}$、顶点偏移$\mathrm{O}$和混合变形$B(\beta,\theta,\psi)$组成：

$$T_P(\beta,\theta,\psi,\mathrm{O}) = \mathrm{T} + \mathrm{O} + B(\beta,\theta,\psi)$$

SCARF使用上采样版本的SMPL‑X（$n_v=38,703$个顶点，$n_t=77,336$个面），为每个被优化对象学习独立的顶点偏移$\mathrm{O}$以捕捉局部几何细节。同时，一个顶点颜色模型$F_t: t \to c$为每个顶点预测RGB颜色，用于后续的网格表面渲染。

**第二层：NeRF服装模型。** 服装部分由一个神经辐射场$F_c$在规范空间（canonical space）中建模，输入为规范空间坐标$\mathbf{x}^c$，输出颜色$\mathbf{c}$和体密度$\sigma$：

$$F_c: \mathbf{x}^c \to (\mathbf{c}, \sigma)$$

规范空间采用“星型”姿态$\theta^c$（四肢伸展的姿态，便于建模服装的完整几何），所有观测空间的点通过加权逆SMPL‑X变换映射到此空间。对于观测空间中的任意点$\mathbf{x}$，其规范对应点$\mathbf{x}^c$通过其$N(\mathbf{x})$个最近邻顶点的加权逆变换计算：

$$\sum_{\mathbf{v}_i \in N(\mathbf{x})} \frac{\omega_i(\mathbf{x})}{\omega(\mathbf{x})} \mathrm{M}_i(0,\pmb{\theta}^c,0,0) (\mathrm{M}_i(\pmb{\beta},\pmb{\theta},\psi,0))^{-1} \mathbf{x} \to \mathbf{x}^c$$

其中权重$\omega_i(\mathbf{x})$综合考虑了点$\mathbf{x}$到顶点$\mathbf{v}_i$的空间距离和蒙皮权重的差异：

$$\omega_i(\mathbf{x}) = \exp\left(-\frac{\|\mathbf{x} - \mathbf{v}_i\|_2 \|\mathbf{w}_{\mathrm{nn}(x)} - \mathbf{w}_i\|_2}{2\sigma^2}\right)$$

**第三层：非刚体变形场。** 为补偿SMPL‑X蒙皮无法解释的服装形变（如宽松衣物、裙摆飘动），SCARF在规范空间中学习一个残差非刚体变形函数$F_m$，对规范空间坐标进行微调，使NeRF能够建模蒙皮之外的服装动态。

### 关键创新之一：网格集成体积渲染

这是SCARF实现身体与服装无缝融合的核心技术。传统NeRF沿射线进行全路径体积积分，而SCARF的渲染过程如下：

1. 沿每条射线$\mathrm{R}$在观测空间中采样$n_s$个点，通过可微光栅化器$\mathrm{R}_m$判断射线是否与身体网格$M$相交。
2. 若射线在点$\mathrm{R}(t_{n_s})$处与网格相交，则将远裁剪面$t_f$设置为该交点，使NeRF仅渲染网格前方的区域（即服装层）。
3. 沿射线累积NeRF的颜色和密度，得到聚合颜色：

$$\mathcal{C}(\mathrm{R}) = \sum_{i=1}^{n_s-1} \alpha_i \mathbf{c}_i + \tau \mathbf{c}$$

其中，当射线击中网格时，最终颜色$\mathbf{c}$使用网格交点处的顶点颜色$F_t(\mathrm{r}_{n_s}^c)$，而非NeRF在无穷远处的颜色。这确保了身体表面被网格的精确颜色覆盖，而服装部分由NeRF贡献，实现了**身体和服装在渲染层面的精确分离**。

### 关键创新之二：多层次的分离损失

SCARF通过一组精心设计的损失函数强制NeRF仅建模服装区域，身体部分完全由网格负责。总损失函数为：

$$L = L_{\mathrm{recon}} + L_{\mathrm{clothing}} + L_{\mathrm{body}}$$

**重建损失**$L_{\mathrm{recon}}$结合了Huber损失和ID‑MRF损失（基于图像块的感知损失），用于约束渲染图像$\mathcal{R}_v$与输入图像$I$的一致性：

$$L_{\mathrm{recon}} = \lambda_{\mathrm{vol}} L_{\delta}(\mathcal{R}_v - I) + \lambda_{\mathrm{mrf}} L_{\mathrm{mrf}}(\mathcal{R}_v - I)$$

**服装分割损失**$L_{\mathrm{clothing}}$利用预训练的服装分割网络（U²‑Net）提供的掩码$S_c$，约束NeRF的聚合密度仅在服装区域非零：

$$L_{\mathrm{clothing}} = \lambda_{\mathrm{clothing}} \|S_v - S_c\|_{1,1}$$

其中$S_v$为渲染的聚合密度图。该损失确保NeRF不会在服装掩码之外产生密度。

**身体损失**$L_{\mathrm{body}}$包含多个子项：
- $L_{\mathrm{silhouette}}$：约束渲染轮廓与输入轮廓一致。
- $L_{\mathrm{bodymask}}$和$L_{\mathrm{skin}}$：约束可见身体部分的颜色由网格顶点颜色模型预测，而非NeRF。
- $L_{\mathrm{inside}}$和$L_{\mathrm{skininside}}$：约束身体网格内部的NeRF密度为零，防止NeRF在身体内部产生伪影。
- $L_{\mathrm{reg}}$：正则化项，约束顶点偏移和变形场的平滑性。

### 关键创新之三：联合优化姿态

与多数方法固定初始姿态估计不同，SCARF在优化过程中联合优化SMPL‑X的姿态参数$\theta_f$。初始姿态由PIXIE提供，随后与网络参数一同优化。这一设计使得姿态估计能够根据渲染损失进行微调，改善了重建的纹理细节（如Fig. 8所示，移除姿态优化会导致重建模糊）。

### 训练流程

SCARF的训练分为两个阶段：

**第一阶段**：仅优化NeRF服装模型$F_c$和顶点颜色模型$F_t$，同时微调姿态参数$\theta$和形状参数$\beta$。此阶段**不优化非刚体变形场$F_m$**，并关闭ID‑MRF损失（$\lambda_{\mathrm{mrf}}=0$）。这一策略对稳定训练至关重要——先用刚性蒙皮建立身体与服装的粗略对应，再引入非刚体变形处理复杂服装动态。

**第二阶段**：引入非刚体变形场$F_m$和ID‑MRF损失，联合优化所有模块。输入为单目RGB视频帧和对应的服装分割掩码，使用缩放正交相机模型$p=[s,\mathbf{t}^T]^T$（各向同性缩放$s$和平移$\mathbf{t}$），无需任何3D监督信号。

### Changed Slots总结

| 设计维度 | 基线方法 | SCARF方案 |
|---------|---------|----------|
| 身体/服装表示 | 整体NeRF或纯网格+顶点偏移 | SMPL‑X网格（身体）+ NeRF（服装） |
| 渲染策略 | 标准NeRF全射线积分 | 网格集成体积渲染（射线在网格表面截断） |
| 分离机制 | 无显式分离损失 | 服装掩码损失+身体可见区域损失+内部约束 |
| 姿态处理 | 固定初始姿态 | 联合优化姿态参数$\theta_f$ |

### 推理与应用路径

训练完成后，SCARF支持三种应用模式：
1. **身体驱动**：修改SMPL‑X的姿态$\theta$和表情$\psi$参数，NeRF服装通过规范空间映射自动适应新姿态。
2. **体型适配**：修改形状参数$\beta$，NeRF服装通过变形场适应新体型（如Fig. 9所示）。
3. **服装迁移**：将一个对象的NeRF服装模型迁移到另一个对象的身体网格上，实现跨对象服装迁移（如Fig. 1(d)所示）。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2210_01868/figures/005_Figure_3.jpg]]
*Figure 3: Graphic illustration for mesh integrated volume rendering in Sec. 3.3*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2210_01868/figures/010_Figure_7.jpg]]
*Figure 7: Rendered images and extracted meshes from different components of SCARF. Our hybrid representation gives better estimated face, hand, and clothing geometry than vanilla NeRF or a mesh-based representation*

## 实验与关键发现

### 新视图合成主结果

SCARF在People‑Snapshot数据集上与Anim‑NeRF、Neural Body、HumanNeRF等主流方法进行了新视图合成对比。定量结果（Table 1）显示，SCARF在四个测试序列上均取得最优或领先指标：male‑3‑casual达到PSNR 30.59 / SSIM 0.977 / LPIPS 0.024，male‑4‑casual为28.99 / 0.970 / 0.025，female‑3‑casual为30.14 / 0.977 / 0.028，female‑4‑casual为29.96 / 0.972 / 0.026。这些数值反映了混合表示在重建精度和感知质量上的综合优势。

需要指出的是，定量表中基线方法的具体数值因篇幅限制未在正文中完整列出，仅说明了相对提升。此外，对比方法SMPLicit和BCNet的训练/测试设置与SCARF不完全相同——前者依赖大规模3D扫描数据进行预训练且处理单张图像，而SCARF直接从视频序列优化，无需任何3D监督。这一差异意味着定量对比的公平性存在一定边界，但SCARF在零3D监督条件下的表现仍然具有说服力。

### 服装重建质量对比

定性对比（Fig. 4, Fig. 13）表明，SCARF在服装几何重建上显著优于SMPLicit（Corona et al., ECCV 2021）和BCNet（Jiang et al., ECCV 2020）。SMPLicit使用深度无符号距离函数建模服装，BCNet从单张图像预测分层形状，两者均难以处理裙装等复杂拓扑结构。SCARF的NeRF服装模型能够捕捉裙摆的褶皱和飘逸形态，而基线方法往往产生过度平滑或拓扑错误的几何。这一差异的核心原因在于NeRF的连续体积表示天然适合建模任意拓扑，而基于网格或隐式曲面先验的方法受限于预定义的拓扑假设。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2210_01868/figures/007_Figure_4.jpg]]
*Figure 4: Garment reconstruction comparison. SCARF reconstructs different clothing types more faithfully than SMPLicit [Corona et al. 2021] and BCNet [Jiang et al. 2020]*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2210_01868/figures/017_Figure_13.jpg]]
*Figure 13: Additional examples for qualitative comparison of garment reconstruction. SCARF reconstructs different clothing types more faithfully than SMPLicit [Corona et al. 2021] and BCNet [Jiang et al. 2020]*

与SelfRecon（Jiang et al., CVPR 2022）和Anim‑NeRF（Chen et al., ICCV 2021）的对比（Fig. 5）进一步揭示了混合表示的关键优势：虽然所有方法在服装区域的渲染质量相当，但SCARF在面部和手部细节上明显更优。这是因为纯NeRF方法（如Anim‑NeRF）将身体和服装统一建模，身体部分的几何精度受限于NeRF的分辨率和采样密度；而SCARF将身体交给SMPL‑X网格显式建模，NeRF仅负责服装，从而在身体区域获得网格级别的几何精度。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2210_01868/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison with SelfRecon [Jiang et al. 2022] and Anim-NeRF [Chen et al. 2021b] for reconstruction. While all methods capture the clothing with comparable quality, our approach has much more detailed face and hands due to the disentangled representation of clothing and body*

### 关键消融实验

**混合表示 vs. 纯表示**（Fig. 7）：分别提取纯NeRF表示、纯网格表示和SCARF混合表示的渲染图像与几何网格进行对比。纯NeRF在面部和手部产生模糊几何，纯网格表示无法捕捉服装的复杂褶皱，而SCARF的混合表示在三个区域均取得最佳几何质量。这一消融直接验证了核心设计动机——身体适合网格建模，服装适合NeRF建模，两者结合才能兼顾精度与灵活性。

**姿态优化的作用**（Fig. 8）：移除姿态优化（即固定由PIXIE提供的初始姿态）会导致纹理细节丢失，重建结果整体变模糊。姿态优化使SMPL‑X参数θ_f在训练过程中联合调整，能够更好地对齐输入视频中的身体姿态，从而为NeRF提供更准确的标准化变换，间接提升服装外观的重建精度。

**训练稳定性设计**：第一阶段NeRF训练时不优化非刚体变形模型F_m，并将ID‑MRF损失的权重λ_mrf设为0。这一策略对稳定训练至关重要——过早引入变形场优化会导致标准空间与观测空间的映射不收敛，而ID‑MRF损失在训练初期会引入高频噪声梯度。第二阶段再逐步开启这些组件，使模型能够从粗到细地学习。

### 失败模式与适用边界

**服装分割依赖性**（Fig. 11）：SCARF依赖外部服装分割掩码（基于U2NET的cloth‑segmentation）来驱动身体‑服装分离损失。当分割结果错误时——例如遗漏腰带等配饰——会导致对应区域的NeRF密度被错误抑制，在重建服装上形成可见缺口。这一失败模式揭示了方法的脆弱环节：分离机制完全依赖分割质量，而分割模型本身在复杂服装边界和细分配饰上存在固有误差。

**服装几何噪声**（Fig. 10）：尽管渲染外观良好，从NeRF提取的服装底层几何有时呈现噪声表面。这是因为体积密度场在服装边界区域的过渡不够锐利，且缺乏显式的表面正则化。这一限制不影响视图合成质量，但会降低几何提取的可用性，对需要精确服装网格的下游应用（如物理仿真）构成障碍。

**重驱动伪影**（Fig. 12）：对训练视频中未见过的姿态进行重驱动时，可能出现视觉伪影。原因在于非刚体变形场F_m是从有限姿态的视频中学习的，对分布外姿态的泛化能力有限。宽松衣物在极端姿态下的形变模式难以从少量观测中充分学习。

**建模范围限制**：当前方法无法处理长发、鞋子和复杂配饰。这些元素要么缺乏对应的参数化模型（如头发），要么与身体的附着关系复杂（如鞋子随脚部运动但具有独立形变），超出了现有身体‑服装二分框架的表达能力。

**计算开销**：在NVIDIA V100上训练约需40小时，主要瓶颈在于每步需要同时执行NeRF体积渲染和网格光栅化，以及多损失项的梯度回传。这限制了方法的实时应用场景和快速迭代能力。

### 适用边界总结

SCARF适用于以下条件：输入为单目RGB视频，人物穿着可被现有分割模型有效分离的服装（不含长发和复杂配饰），训练姿态覆盖了目标驱动姿态范围。方法在无需3D监督的前提下，能够生成可独立动画的身体和可迁移的服装外观，在面部/手部细节和服装拓扑灵活性上优于纯NeRF或纯网格方法。但在分割质量差、极端未见姿态、或需要精确服装几何的场景下，性能会显著下降。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2210_01868/figures/016_Figure_11.jpg]]
*Figure 11: The wrong clothing segmentation results in a visible gap within the reconstructed clothing*

## 定位与知识库关联

SCARF 的核心定位是 **单目视频驱动的可分离身体‑服装化身重建**，其相对于已有方法改变的关键 slot 在于 **身体与服装的表示方式**：将现有方法中“整体 NeRF 统一表示全身”（如 Anim‑NeRF）或“纯网格+顶点偏移”的策略，替换为 **SMPL‑X 显式网格建模身体 + NeRF 仅建模服装** 的混合表示，并配套引入网格集成体积渲染与多层次的分离损失。

### 1. 与基线方法的本质差异

**相对于 Anim‑NeRF**（Chen et al., ICCV 2021）：Anim‑NeRF 使用单个 NeRF 建模整个人体外观，身体与服装在隐式空间中耦合，导致无法独立驱动身体或迁移服装。SCARF 通过显式分离表示，将身体交给可驱动的 SMPL‑X 网格，仅用 NeRF 捕获服装区域，从根本上解耦了两者。这一改变使得 SCARF 可以独立改变身体姿态（包括面部表情和手部动作）而不影响服装外观，反之亦可实现服装在不同主体间的迁移——这是 Anim‑NeRF 等整体 NeRF 方法无法做到的。

**相对于 SMPLicit**（Corona et al., ECCV 2021）和 **BCNet**（Jiang et al., ECCV 2020）：这两类方法虽然也显式分离身体与服装，但依赖大规模 3D 扫描数据进行预训练，且服装建模采用深度无符号距离函数（SMPLicit）或分层网格预测（BCNet），在处理裙装等复杂拓扑时表现有限（见 Fig. 4, Fig. 13）。SCARF 直接从单目视频优化，无需 3D 监督，且 NeRF 的隐式表示天然适合捕获任意拓扑和复杂材质的外观细节。在服装重建质量上，SCARF 对不同服装类型（包括裙装）的还原度明显更高。

**相对于 SelfRecon**（Jiang et al., CVPR 2022）：SelfRecon 从多视图或单目视频重建可驱动的隐式身体表面，但面部和手部细节受限于隐式表示的几何精度。SCARF 将身体交给 SMPL‑X 网格，利用其参数化先验和顶点偏移模型 $F_d$ 捕获局部几何细节，在面部和手部区域的重建质量显著优于纯隐式方法（Fig. 5, Fig. 7）。

### 2. 知识库挂载点

SCARF 在知识库中的挂载点可归纳为以下三个维度：

**（1）混合显式‑隐式人体表示**：SCARF 属于将统计人体模型（SMPL 族）与神经辐射场结合的路线。该路线在知识库中可挂载到 **Neural Body**（Peng et al., ECCV 2020）和 **HumanNeRF**（Weng et al., CVPR 2022）等工作的延伸分支，但 SCARF 的关键区别在于：它不是用 SMPL 仅为 NeRF 提供变形场或姿态条件，而是将网格本身作为独立的可渲染层，通过网格集成体积渲染实现两层表示的深度融合。

**（2）可分离分层人体建模**：在分层人体建模的知识谱系中，SCARF 可挂载到 **SMPLicit** 和 **BCNet** 之后，作为“从单目视频学习分层表示”的新节点。与前者依赖 3D 扫描预训练不同，SCARF 证明了仅从 2D 视频信号（RGB + 服装分割掩码）配合精心设计的分离损失，即可实现有效的身体‑服装解耦。

**（3）NeRF 的网格增强渲染**：SCARF 提出的网格集成体积渲染（Eq. 7）可挂载到 NeRF 渲染技术的扩展分支。其核心思想是：光线在抵达身体网格表面时提前截断，用网格颜色替换 NeRF 颜色。这一策略既保证了身体表面的清晰几何边界，又避免了 NeRF 在身体区域产生噪声密度——这是纯 NeRF 方法在人体重建中常见的失败模式。

### 3. 适用边界与限制

SCARF 的适用边界明确受以下因素约束：

- **输入依赖服装分割掩码**：分离损失 $L_{\text{clothing}}$ 和 $L_{\text{body}}$ 均依赖服装分割结果。当分割错误（如遗漏腰带等配饰）时，会导致身体与服装的错误分离，形成可见缺口（Fig. 11）。这意味着 SCARF 对分割质量敏感，在复杂服装或遮挡场景下可能退化。
- **服装几何噪声**：尽管 NeRF 渲染的服装外观良好，但底层密度场提取的几何往往噪声较大（Fig. 10），不适合直接用于物理仿真或碰撞检测等需要精确几何的下游任务。
- **未覆盖的类别**：当前方法无法处理长发、鞋子和复杂配饰——这些元素既不属于 SMPL‑X 网格的建模范围，也不在服装分割掩码的覆盖区域。
- **重驱动伪影**：对未见过的姿态进行重驱动时可能出现视觉伪影（Fig. 12），这源于 NeRF 在标准空间中的非刚体变形场 $F_m$ 对极端姿态的泛化能力有限。
- **计算开销**：训练时间约 40 小时（NVIDIA V100），限制了快速迭代和实时应用的可能性。

### 4. 后续研究启发

SCARF 的开放问题为后续工作指明了方向：

- **分割鲁棒性**：利用光流时间一致性改进服装分割质量，或设计不依赖显式分割掩码的分离机制，是提升方法鲁棒性的关键。
- **覆盖范围扩展**：将头发、鞋子和配饰纳入 NeRF 建模，需要解决这些元素与身体/服装的遮挡关系和独立可驱动性问题。
- **几何质量改进**：采用 SDF 类隐式表示替代密度场，有望改善服装几何重建质量，使其适用于物理仿真等下游任务。
- **重驱动泛化**：处理极端姿态并减少重驱动伪影，可能需要更强的非刚体变形先验或数据增强策略。
- **材质与光照分解**：从形状中分解光照和材质属性，将使服装迁移更加真实，支持不同光照条件下的重照明。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Capturing_and_Animation_of_Body_and_Clothing_from_Monocular_Video.pdf]]
---
title: Differentiable Adaptive 4D Structured Illumination for Joint Capture of Shape and Reflectance
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Differentiable_Adaptive_4D_Structured_Illumination_for_Joint_Capture_of_Shape_and_Reflectance.pdf
project_link: "https://www.einscan.com/handheld-3dscanner/2x-plus/"
code_link: null
aliases:
- DA4SI
- DA4SIJCSR
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过在每次采集步骤中微分化地优化下一批照明图案（light pattern和mask pattern），以最小化深度不确定性（交叉熵损失），实现对任意物体的自适应高效扫描。
primary_logic: 利用基于直方图的像素级概率模型对深度和反射率进行建模，将下一照明条件与降低深度不确定性的损失可微连接，从而指导自适应照明优化；同时采用多LED复用大幅减少曝光时间。
claims:
- 提出首个学习型4D空间-角度域多重复用方案，同时高效采集形状和反射率。
- 提出可微分框架，在采集过程中在线优化复杂的照明条件，以适应目标物体。
- 相比每次仅点亮一个LED的先前工作，曝光时间减少高达100倍，总采集时间减少2倍。
- 深度结果显著优于现有技术，反射率结果在照片验证下具有可比性。
---

# Differentiable Adaptive 4D Structured Illumination for Joint Capture of Shape and Reflectance

> [!tip] 核心洞察
> 利用基于直方图的像素级概率模型对深度和反射率进行建模，将下一照明条件与降低深度不确定性的损失可微连接，从而指导自适应照明优化；同时采用多LED复用大幅减少曝光时间。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可微分自适应四维结构光联合采集形状与反射率 |
| 英文题名 | Differentiable Adaptive 4D Structured Illumination for Joint Capture of Shape and Reflectance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.06214) · [Project](https://www.einscan.com/handheld-3dscanner/2x-plus/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Differentiable Adaptive 4D Structured Illumination |
| Dataset | 物理物体（10个，最大尺寸9-15cm） |

> [!tip] 效果简介
> - 物理物体（10个，最大尺寸9-15cm） 上，深度 RMSE (mm) / 内点百分比 1.79 / 98.7% (72个自适应图案，图8) vs 33.72 / 41% (单LED，图6) (-31.93 mm / +57.7%)。
> - 物理物体 上，单视角采集时间 约10分钟（总曝光时间15秒） vs 24分钟 (减少2倍)。
> - 反射率质量 上，与新视角照片的视觉对比 可比 vs (无量化指标)。

## 概述

三维物体的数字化采集——同时获取其精确几何形状与空间变化反射率——是计算机图形学与视觉领域的长期挑战。现有基于4D空间-角度域结构光的方法（如**Unified spatial-angular structured light**，Xu et al., CVPR 2023）虽能联合采集形状与反射率，但依赖离线预优化的固定照明图案，且每次仅点亮单个LED，导致单视角采集耗时长达24分钟，无法根据物体特性自适应调整，采集效率与精度均受制约。

本文提出**可微分自适应四维结构光（Differentiable Adaptive 4D Structured Illumination）**，核心思想是将照明图案的优化过程与采集目标可微连接：通过为每个像素建立基于直方图的深度与反射率概率模型，以最小化深度不确定性（交叉熵损失）为目标，在线自适应地生成下一批照明图案（light pattern与mask pattern），同时采用多LED复用策略大幅缩短曝光时间。该方法首次实现了学习型的4D空间-角度域多重复用方案，在统一框架下高效联合采集形状与反射率。

实验表明，在相同硬件原型上，本方法使用72个自适应图案即可将深度RMSE从33.72 mm降至1.79 mm，内点比例从41%提升至98.7%；总曝光时间减少高达100倍，单视角采集时间由24分钟压缩至约10分钟。反射率结果在新视角照片验证下与现有技术可比。该方法为面向任意物体的高效高精度数字化采集提供了可微分的自适应范式。

## 背景与动机

### 问题背景：联合采集形状与反射率的挑战

在计算机视觉与图形学中，同时获取物体的三维形状和表面反射率是实现照片级真实感重光照、数字孪生和文化遗产数字化的核心技术需求。传统方法通常将几何采集与外观采集分离：先通过结构光或立体视觉获取深度，再在受控光照下拍摄多角度图像以拟合反射模型。这种分步策略不仅耗时，而且两阶段之间的误差累积会损害最终结果的一致性。

近年来，**统一空间-角度结构光**（unified spatial-angular structured light）被提出用于同时采集形状和反射率。其核心思想是：利用LED阵列提供角度域变化的光照，配合LCD掩模引入空间域调制，形成四维（4D）结构光照明，从而在单次采集过程中编码几何与外观信息。**Unified spatial-angular structured light**（Xu et al., CVPR 2023）是这一方向的代表性工作，它通过离线预优化设计照明图案，在统一框架下实现了形状与反射率的联合重建。

### 现有方法的关键瓶颈

尽管统一结构光方法取得了进展，但其在实际应用中面临两个根本性瓶颈：

**1. 采集效率极低。** 现有方法[43]每次仅点亮一个LED，导致单视角采集需要经历大量曝光。具体而言，完成一次完整的形状与反射率采集需要约**24分钟**。这一时间成本使得该方法无法应用于对时间敏感的场景，也难以推广到多视角扫描。

**2. 照明图案无法自适应物体特性。** 现有方法的照明图案是离线预优化的——即在扫描开始前就固定了所有光照条件，不随被扫描物体的几何形状、材质特性而发生任何调整。这意味着照明策略对“简单物体”和“复杂物体”一视同仁，导致：
- 对简单区域过度采样，浪费采集时间；
- 对复杂区域（如高光、凹陷、纹理稀疏处）采样不足，导致深度估计不确定性高。

本质上，这是一个**信息获取效率**问题：固定的照明方案无法将有限的采集预算集中到最需要降低不确定性的区域。

### 本文动机：可微分自适应四维结构光

针对上述瓶颈，本文提出一个核心问题：**能否让照明图案在采集过程中根据物体的实际响应动态调整，从而用更少的曝光获得更高质量的联合重建？**

这一思路的可行性建立在以下观察之上：如果能够对每个像素的深度和反射率建立概率模型，那么就可以量化“当前对某个深度值的确定程度”，进而通过优化下一批照明图案来最大化地降低这种不确定性。关键在于，这个过程必须是**可微的**——即照明图案的优化能够通过梯度反向传播与不确定性降低的目标直接关联。

基于此，本文提出**可微分自适应四维结构光**（Differentiable Adaptive 4D Structured Illumination），其核心设计原则包括：

- **在线自适应优化**：在每次采集步骤中，根据当前的概率模型动态生成下一批照明图案（light pattern和mask pattern），而非使用预优化的固定序列。
- **多LED复用**：同时点亮多个LED以大幅减少曝光次数，突破“每次一个LED”的限制。
- **不确定性驱动**：通过最小化深度估计的交叉熵损失来指导照明优化，使采集资源集中在信息最匮乏的区域。
- **几何与反射率联合自适应**：形状和反射率的采集不再分步进行，而是在统一的自适应框架下协同优化。

通过这一方法，本文旨在证明：**智能地选择“看什么”和“怎么看”，比简单地“看得更多”更为高效。**

## 核心创新

### 瓶颈与因果杠杆

现有4D结构光联合采集形状与反射率的关键瓶颈在于**照明效率与适应性**。先前工作（Xu et al., CVPR 2023）采用预优化的固定照明图案，且每次仅点亮单个LED，导致单视角采集耗时高达24分钟，无法根据物体表面反射特性进行动态调整，深度误差达33.72 mm，内点比例仅41%。这一瓶颈的根源是照明条件与场景内容之间缺乏反馈闭环：照明图案在采集前确定，无法感知当前已获得的信息量，也无法针对性地降低剩余不确定性。

本工作的**因果杠杆**是在每次采集步骤中，将下一批照明图案的优化与当前深度/反射率概率模型可微连接，通过最小化深度交叉熵损失，使系统能够“感知”哪些区域的深度仍不可靠，并生成专门针对这些区域的照明图案。这一杠杆同时解决了效率和精度两个维度的问题。

### 核心洞察

方法的底层洞察可概括为三点：

1. **像素级概率建模替代全局确定性估计**：为每个有效像素建立深度和各BRDF参数的直方图概率分布，将采集过程转化为逐步降低分布熵的信息增益过程。这一设计使得系统能够量化“哪里还不确定”，而非仅输出一个点估计。

2. **可微不确定性驱动照明优化**：通过基于ZNCC的软最大似然将候选分类问题与交叉熵损失连接，使得照明图案（light pattern和mask pattern）的优化可以通过梯度下降进行。损失函数直接编码了“降低深度不确定性”的目标，从而实现了从物体特性到照明条件的端到端自适应。

3. **多LED复用打破时间瓶颈**：同时点亮多个LED（多路复用）替代逐个LED点亮的方式，将曝光时间降低高达100倍，总采集时间减少2倍。这一设计在保持信息获取量的同时大幅压缩了物理采集时间。

### 与基线方法的Changed Slots

| 改进维度 | 基线方法 (, Xu et al., CVPR 2023) | 本方法 | 证据强度 |
|---------|--------------------------------------|--------|---------|
| 照明复用方式 | 每次仅一个LED点亮 | 同时点亮多个LED（多路复用），曝光时间减少100× | 高（量化结果支撑） |
| 照明图案设计 | 离线预优化，固定图案 | 在线可微分自适应优化，根据物体特性动态生成 | 高（消融实验验证） |
| 不确定性建模 | 无显式不确定性指导 | 基于直方图的深度/反射率概率模型，交叉熵损失驱动优化 | 高（公式与流程图完整） |
| 反射率采集集成度 | 分步采集（先几何后外观） | 几何与反射率同时联合自适应采集 | 高（框架设计明确） |

**照明复用方式**的改变直接带来了采集时间的数量级缩减。**照明图案设计**从静态转向自适应是精度提升的核心驱动：消融实验（Figure 8）显示，自适应图案数量从36增至72时，RMSE从4.78 mm降至1.79 mm，内点比例从94%提升至98.7%。**不确定性建模**的引入使得自适应成为可能——它提供了优化目标（交叉熵）与照明参数之间的可微桥梁。**反射率采集集成度**的提升则使系统输出从单一深度图扩展为完整的GGX BRDF参数图（法线、粗糙度等），实现了形状与外观的联合获取。

### 方法谱系与知识库定位

本工作在4D结构光领域首次提出了**学习型空间-角度域多重复用方案**，将自适应照明优化的思想从传统空间域结构光拓展到空间-角度联合域。与经典的空间结构光方法**MPS**（Gupta and Nayar, CVPR 2012）仅采集几何相比，本方法同时输出反射率参数；与统一空间-角度结构光[43]（Xu et al., CVPR 2023）相比，本方法将照明设计从离线预优化升级为在线自适应优化，并引入多LED复用机制。从知识库定位看，本方法处于**计算成像×可微优化×结构光**的交叉点，其“概率建模+可微损失驱动采集策略”的范式可迁移至其他主动视觉任务。

## 整体框架

本文提出一种**两阶段流水线**，以可微分方式自适应计算4D空间‑角度域照明条件，实现对任意物理物体形状与反射率的高效联合采集。整体流程如图2所示。

**第一阶段：自适应采集**

该阶段在采集过程中在线优化照明图案，核心是一个“感知‑决策‑更新”的闭环：

1. **概率建模**：为每个有效像素建立基于直方图的深度与BRDF参数概率分布。深度概率模型将相机射线与有效体积的交集划分为 $n_{\text{bin}}$ 个区间（实验中 $n_{\text{bin}}=100$），每个区间存储对应深度候选者模拟测量与物理测量之间的最高ZNCC分数（图3）。反射率参数同样以直方图形式建模，通过L1距离更新分布。

2. **自适应图案优化**：基于当前概率分布随机采样候选者（实验中 $n_{\text{sample}}=600$），将每个候选者视为一个类别，通过最小化**交叉熵损失**来可微地优化下一批照明/掩模图案（light pattern 与 mask pattern）。损失函数定义为所有有效像素深度不确定度之和，将下一照明条件与降低深度不确定性的目标可微连接。

3. **测量更新**：使用优化后的图案拍摄照片，根据新测量值（ZNCC用于深度，L1距离用于反射率）更新概率分布。

4. **迭代循环**：重复上述步骤直至终止条件满足。实验中采用 $3 \times 24 = 72$ 个自适应图案，总曝光时间约15秒，单视角采集时间约10分钟，相比先前每次仅点亮一个LED的方法（**Unified spatial-angular structured light**，Xu et al., CVPR 2023）将曝光时间减少高达100倍、总采集时间减少2倍。

**第二阶段：微调**

从概率模型获取深度与反射率的初始估计后，通过最小化物理测量与模拟图像之间的差异进行联合微调。反射率采用GGX BRDF模型参数化，并以16D神经隐向量配合5个MLP重新参数化。最终输出为深度图与存储GGX参数（法向、粗糙度等）的纹理图（图5），微调过程约需2小时。

**关键设计决策**

- **多LED复用**：同时点亮多个LED，替代先前工作中每次仅点亮单个LED的方式，大幅压缩曝光时间。
- **可微分自适应优化**：将照明图案设计从离线预优化转变为在线动态生成，使系统能根据物体特性自适应调整。
- **不确定性驱动的损失**：以深度交叉熵作为优化目标，显式地将信息增益最大化原则嵌入采集过程。

**输入输出**

- **输入**：物理物体，通过由相机、LED阵列与LCD掩模组成的采集装置（图1）获取图像测量。
- **输出**：高精度深度图（RMSE 1.79 mm，内点比例98.7%）与参数化反射率图（GGX BRDF参数），可用于新视角重光照渲染。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/002_Figure_2.jpg]]
*Figure 2: Our pipeline consists of two stages. First, for a physical object, we compute the next light/mask pattern(s) by minimizing the cross entropy among possible candidates sampled from histogram-based probability models. We then take photograph(s) with these patterns, and update probability distributions based on new measurements. This process is repeated until a termination condition is met. Next, we use the depth/reflectance estimate from previous stage as initial values, and fine-tune the results by minimizing the differences between physical measurements and corresponding simulated ones. The final output is a depth map and several texture maps that store parameters of the GGX BRDF model. Par...*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/001_Figure_1.jpg]]
*Figure 1: Our acquisition setup. It consists of a camera, an LED array and an LCD mask (a). The setup is working with optimized light/mask pattern (b). A side view is illustrated in (c)*

## 核心模块与公式推导

### 整体流水线

本方法包含两个阶段（图2）。第一阶段为**自适应采集**：对物理物体迭代优化下一批光照/掩模图案，拍摄照片后更新概率模型，直至满足终止条件。第二阶段为**微调**：以第一阶段输出的深度与反射率估计为初值，通过最小化物理测量与模拟图像之间的差异进行联合优化，最终输出深度图与GGX BRDF参数纹理图。

流水线的核心可微分模块包括三个部分：概率模型构建、自适应图案优化器、以及测量更新。

### 模块一：概率模型构建

对每个有效像素，建立基于直方图的深度与BRDF参数概率分布。

**深度概率模型**（图3）：首先通过将有效体积与相机射线求交确定深度范围 $z_{\min}$ / $z_{\max}$，将该范围划分为 $n_{\text{bin}}$ 个区间（实验中 $n_{\text{bin}} = 100$）。每个区间存储该深度候选下物理测量与模拟测量之间的最高ZNCC分数。

**反射率概率模型**：对每个BRDF参数独立构建类似的直方图分布，以L1距离作为匹配分数。

### 模块二：自适应图案优化器

在每次采集步骤中，基于当前概率模型可微分地优化下一批光照/掩模图案，以最小化深度不确定性。

**候选采样**：根据当前概率分布随机采样 $n_{\text{sample}}$ 个候选者（实验中 $n_{\text{sample}} = 600$），每个候选者被视为一个独立的类别。

**损失函数**：深度不确定性定义为每个有效像素的交叉熵损失之和。对于单个像素：

$$-\sum_{a,b} y_{a,b} \log(\hat{y}_{a,b})$$

其中 $\hat{y}_{a,b}$ 为候选 $a$ 被分类为候选 $b$ 的软最大似然，基于模拟测量与物理测量之间的ZNCC分数计算：

$$\hat{y}_{a,b} = \frac{e^{\mathrm{ZNCC}(\{I_{j,a}\}_j, \{I_{j,b}\}_j)}}{\sum_b e^{\mathrm{ZNCC}(\{I_{j,a}\}_j, \{I_{j,b}\}_j)}}$$

该损失将下一光照条件与降低深度不确定性可微地连接，使优化器能够自动搜索最能区分不同深度候选的光照/掩模图案。

### 模块三：测量更新

使用优化后的图案拍摄照片后，根据新测量更新概率分布：对深度模型，以ZNCC分数更新各区间；对反射率模型，以L1距离更新。更新后的分布将在下一轮迭代中指导新的图案优化。该循环重复进行，直至采集足够信息（实验中采用 $3 \times 24 = 72$ 个自适应图案）。

### 图像测量模型

上述模块均依赖于一个统一的图像测量模型。对于第 $j$ 个光照/掩模图案下的像素 $k$，其测量值近似为：

$$I_{j,k} \approx \sum_l f_{k,l} F L_j(l) \Psi(-\omega_k^i) \int_A L(\mathbf{x}_l) M_j(\mathbf{x}_l, \mathbf{x}_k) dA$$

其中 $f_{k,l}$ 为BRDF项，$F$ 为相机响应因子，$L_j(l)$ 为第 $j$ 个图案下LED $l$ 的相对强度，$\Psi(-\omega_k^i)$ 为LED的角度分布函数，$L(\mathbf{x}_l)$ 为空间核，$M_j$ 为LCD掩模调制。LED辐射的分解形式为：

$$L_j(\mathbf{x}_l, -\omega_k^i) \approx L_j(l) \Psi(-\omega_k^i) L(\mathbf{x}_l)$$

该模型将光源的空间-角度分布与掩模调制统一纳入可微框架，使得图案优化器能够同时搜索光照图案与掩模图案的最优组合。

### 微调阶段

自适应采集结束后，从概率模型中提取深度与反射率初值，将BRDF模型重参数化为16维神经隐向量与5个MLP，通过最小化物理测量与模拟图像之间的差异进行联合微调，进一步提升重建精度。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/003_Figure_3.jpg]]
*Figure 3: Graphical illustration of our probability model for depth. To build this model, we first determine its range*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of various parts in adaptive acquisition. From the left column to right, after the initialization, after pattern#3, #12 and #30 is projected. From the top row to bottom, light pattern, mask pattern, corresponding photograph, depth uncertainty visualization (yellow = uncertain, blue = certain), and the visualization of the probability model at a single pixel*

## 实验与分析

### 主结果：与现有技术的定量与定性比较

实验在10个物理物体上进行，最大尺寸为9–15 cm，使用与**统一空间-角度结构光方法**（Xu et al., CVPR 2023）完全相同的硬件原型（相机、LED阵列、LCD掩模），确保对比公平。本文方法采用3×24=72个自适应光/掩模图案，单视角总采集时间约**10分钟**（总曝光时间仅15秒），而[43]使用预优化固定图案且每次仅点亮一个LED，单视角采集耗时**24分钟**，本文实现了采集时间减少约2倍、曝光时间减少高达100倍的效率提升。

深度重建质量方面，如图6所示，本文自适应方法在72个图案下达到**RMSE 1.79 mm**、内点百分比**98.7%**（内点RMSE 0.27 mm），而[43]的RMSE为**33.72 mm**、内点百分比仅**41%**（内点RMSE 1.07 mm），深度误差降低约31.93 mm，内点比例提升57.7个百分点。作为几何基准的**微相移方法**（MPS, Gupta and Nayar, CVPR 2012）同样被本文方法显著超越。图7进一步展示了本文多LED复用方案相较于[43]中单LED（中心/左侧/右侧角落）的定性优势——单光源结构光在非均匀照明区域产生大量缺失深度值，而本文方法通过多角度复用照明实现了完整且精确的重建。

反射率结果通过GGX BRDF参数图（法线、粗糙度等，见图5）表示，在新视角照片下进行视觉验证。本文反射率渲染结果与照片具有可比性，与[43]的反射率质量相当。需要指出，反射率比较目前仅依赖定性视觉评估，缺乏数值指标，该结论的强度需结合具体应用场景判断。

### 消融实验

本文通过系统消融实验验证了自适应采集框架中各关键超参数的影响，所有消融均以深度RMSE为核心指标。

**自适应图案总数（图8）**：将自适应光/掩模图案从36增至54再增至72，深度RMSE从4.78 mm降至1.87 mm再降至1.79 mm，内点RMSE从0.42 mm（94%内点）降至0.28 mm（98.6%）再降至0.27 mm（98.7%）。结果表明，增加自适应图案数量持续提升深度精度，但边际收益递减——从54到72图案的改进幅度明显小于从36到54。

**Monte Carlo采样数 n_sample（图9）**：增加候选采样数量可提高重建质量，这与直觉一致：更多采样意味着更精确的概率分布估计，从而指导更有效的图案优化。

**同时优化的下一批图案数 n_batch（图10）**：在总采集时间相同的前提下，不同的批优化数量影响深度质量。这一消融揭示了在线优化的“前瞻性”与单步优化质量之间的权衡——过大的批次可能因优化难度增加而降低单批图案的信息增益。

**交叉熵计算中的峰值候选数 n_peak（图11）**：该参数控制用于计算交叉熵损失的候选类别数量，对深度质量有显著影响，表明选择合适的类别粒度对不确定性建模至关重要。

**直方图分箱数 n_bin（图12）**：更细的分箱以更多计算为代价提升质量。本文实验中采用n_bin=100，在精度与计算开销之间取得平衡。

**计算自适应图案的图像分辨率（图13）**：使用低分辨率图像计算自适应图案在同等重建分辨率下仍可接受，验证了该策略在降低计算开销方面的有效性。这一发现对实际部署具有重要意义——可在不显著牺牲最终重建质量的前提下加速在线优化过程。

### 失败模式与局限性

**间接光照未建模**：深度不确定度计算在自适应图案优化时未考虑间接光照（interreflection），这可能导致在凹面区域或高反照率物体上不确定性估计失准，进而影响图案优化的最优性。该问题在复杂几何场景中尤为突出。

**输出表示的表达能力受限**：最终输出为深度图与参数化GGX BRDF纹理，难以重建细粒度几何细节（如微观凹凸）和复杂空间变化外观（如各向异性反射）。精细几何与外观的丢失限制了重光照的真实感。

**硬件小型化尚未完成**：当前方法基于实验室原型装置，尚未应用于手持设备实现自由视角扫描。从固定视角到手持自由扫描的迁移需要进一步解决配准、实时优化等问题。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/005_Figure_5.jpg]]
*Figure 5: Reflectance results represented as GGX BRDF parameters map. Tangent maps are not shown here due to limited space*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/006_Figure_6.jpg]]
*Figure 6: Comparisons with state-of-the-art techniques on shape and reflectance capture. From the left column to right: depth reconstruction with our approach (adaptive/non-adaptive patterns), [43] and MPS [16]; photograph under a lighting condition not used in optimization, rendering with the reflectance results of our approach and [43]. Quantitative errors are listed below each related image*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/010_Figure_7.jpg]]
*Figure 7: Comparison with a single-source structured light [43]. From the left to right: our result, the result of [43] when the LED at the center, left, or right corner of the LED array is on*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/011_Figure_8.jpg]]
*Figure 8: Impact of the total number of adaptive light/mask patterns over the depth quality*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/014_Figure_9.jpg]]
*Figure 9: Impact of*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/013_Figure_10.jpg]]
*Figure 10: Impact of the number of simultaneously optimized next patterns (nbatch) over the depth quality, with the same total acquisition time*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/009_Figure_11.jpg]]
*Figure 11: Impact of*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2605_06214/figures/012_Figure_12.jpg]]
*Figure 12: Impact of*

## 方法谱系与知识库定位

### 1. 在4D结构光采集谱系中的位置

本文工作在**空间-角度域4D结构光**这一细分方向上，直接继承并改进了**统一空间-角度结构光方法**（Xu et al., CVPR 2023）的核心框架。两者共享同一硬件原型（相机、LED阵列、LCD掩模），但在照明策略上形成根本性分叉：

- **（Xu et al., CVPR 2023）**：采用**离线预优化**的照明图案，每次仅点亮**单个LED**，单视角采集耗时约24分钟。该方法将空间结构光（掩模调制）与角度结构光（LED方向性）统一建模，但照明设计对物体特性无感知，导致采集效率低下。
- **本文方法**：提出**在线可微分自适应优化**框架，每次同时点亮**多个LED**（多路复用），并动态生成下一批照明图案以最小化深度不确定性。总采集时间压缩至约10分钟，曝光时间减少高达100倍。

这一改进的核心机制在于：将照明优化与**基于直方图的像素级概率模型**可微连接。通过为每个有效像素建立深度和各BRDF参数的直方图分布，并以**交叉熵损失**量化深度不确定性，本文首次实现了“采集-建模-优化”闭环的自适应4D结构光。

### 2. 与经典结构光方法的关系

在几何采集层面，本文还与经典**空间结构光**方法形成对比基线：

- **Micro Phase Shifting (MPS)**（Gupta and Nayar, CVPR 2012）：仅用于几何采集的经典方法，通过微相位偏移实现高精度深度重建。本文在实验中将MPS作为几何基准之一（Figure 6），但MPS不涉及反射率采集，且照明图案为固定设计，不具备自适应性。

本文在反射率采集上的集成度显著超越上述两类方法：**几何与反射率同时联合自适应采集**，而非分步执行（先几何后外观），这在4D结构光领域属于首次。

### 3. 方法适用边界与局限

尽管本文在效率和精度上取得显著提升，但方法存在明确的适用边界：

1. **间接光照建模缺失**：深度不确定度计算在自适应图案优化时未考虑间接光照（如互反射、次表面散射），这可能导致复杂几何或高反照率场景下的不确定度估计偏差，进而影响照明优化的最优性。

2. **输出表示的表达能力瓶颈**：最终输出为**深度图**和**参数化GGX BRDF纹理图**（法线、粗糙度等），这种显式2D表示难以重建细粒度的几何细节（如毛发、薄结构）和复杂外观（如空间变化的各向异性反射）。

3. **硬件与扫描模式的限制**：当前实现基于固定台式装置（相机-LED阵列-LCD掩模），尚未应用于手持设备自由扫描。硬件小型化和自由视角扫描是工程化落地的关键挑战。

4. **反射率验证的量化不足**：反射率结果仅通过新视角照片进行**定性视觉对比**，缺乏数值指标（如BRDF拟合的RMSE或重光照误差），其精度声明的可复现性有待加强。

### 4. 开放问题与后续工作方向

基于上述局限，本文明确或隐含地指向以下开放问题：

- **如何将间接光照融入自适应图案优化？** 这需要在深度不确定度建模中引入全局光照的可微近似，可能涉及路径追踪的简化变体或神经渲染的在线集成。
- **如何结合更先进的表示实现高质量重光照？** 文中提及**高斯泼溅（Gaussian Splatting）**作为潜在方向，将几何与外观表示为可微的3D基元，可能突破当前深度图+BRDF纹理图的表达能力瓶颈。
- **能否将方法迁移至手持设备？** 这需要解决实时概率模型更新、低延迟图案优化以及小型化硬件（如微型LED阵列与可编程掩模的集成）等工程问题。
- **反射率采集的量化评估体系构建**：未来工作需要建立标准化的反射率基准和数值指标，以客观衡量联合采集方法在外观重建上的真实能力。

### 5. 在知识库中的定位总结

本文在计算成像与结构光领域占据**“自适应4D结构光联合采集”**这一新兴节点：它上承统一空间-角度结构光[43]的硬件与建模框架，下启可微分照明优化与概率引导采集的新范式。其方法论贡献——将采集过程本身视为可微优化问题——与更广泛的“学习型传感”趋势（如自适应主动视觉、神经采集）形成共振，但当前仍受限于显式表示和忽略间接光照的理论简化。

## 原文 PDF

![[paperPDFs/CVPR_2026/Differentiable_Adaptive_4D_Structured_Illumination_for_Joint_Capture_of_Shape_and_Reflectance.pdf]]

---
title: Active Exploration for Neural Global Illumination of Variable Scenes
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Active_Exploration_for_Neural_Global_Illumination_of_Variable_Scenes.pdf
project_link: "http://fungraph.inria.fr"
code_link: null
aliases:
- AENGIVS
tags:
- SIGGRAPH_2022
- topic/generative_models_diffusion
core_operator: 主动探索（Active Exploration）策略：利用基于MCMC的随机游走，在训练过程中根据损失与梯度乘积定义的目标函数，引导采样至“困难”区域，从而有效生成对训练最有价值的数据。
primary_logic: 将训练与数据生成交织，并用MCMC在训练数据空间中主动搜索高误差区域，能够以远少于均匀采样的训练预算学会复杂、局部化的光照现象，使神经网络能够保留锐利细节并再现困难光路。
claims:
- 与均匀采样相比，主动探索在相同训练时间内能够产生更清晰的阴影、反射和焦散，定性及定量指标（DSSIM、MAPE等）均显著更优。
- MCMC采样分布随训练逐渐逼近目标函数（损失×梯度）的分布，证实主动探索可以有效聚焦于重要的训练区域。
- 随着可变参数维度增加，主动探索相较于均匀采样的优势变得更加明显。
- 与Granskog et al. (2020)的编码器-解码器方案相比，在相同18小时训练+渲染的总时间下，本文方法可渲染出接近参考的全局光照；而前者几乎完全失败（MAPE 0.082 vs 0.823），即使将前者训练时间延长至4天，其质量仍不及本文方法（MAPE 0.655 vs 0.082）。
---

# Active Exploration for Neural Global Illumination of Variable Scenes

> [!tip] 核心洞察
> 将训练与数据生成交织，并用MCMC在训练数据空间中主动搜索高误差区域，能够以远少于均匀采样的训练预算学会复杂、局部化的光照现象，使神经网络能够保留锐利细节并再现困难光路。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向可变场景的神经全局光照主动探索 |
| 英文题名 | Active Exploration for Neural Global Illumination of Variable Scenes |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://repo-sam.inria.fr/fungraph/active-exploration/) · [Project](http://fungraph.inria.fr) |
| Topic | #topic/generative_models_diffusion |
| Method | Active Exploration (MCMC-guided on-the-fly data generation with self-tuning sample reuse and adaptive resolution) |
| Dataset | Living Room, Spaceship, ArchViz |

> [!tip] 效果简介
> - Living Room (Fig. 11) 上，DSSIM 0.0141 vs 0.0241 (Uniform) (↓ 41.5% (0.0100))；MAPE 0.079 vs 0.162 (Uniform) (↓ 51.2% (0.083))。
> - Spaceship (Fig. 15) 上，DSSIM 0.0155 vs 0.0461 (Işık et al. ANF) (↓ 66.4% (0.0306))。
> - Living Room (same training time, Fig. 12 bottom) 上，MAPE 0.082 (18h total) vs 0.823 (Granskog et al., 18h training) (↓ 90.0% (0.741))。

## 概要

可变场景（视角、材质、物体位置、光源等动态改变）的神经全局光照面临一个根本瓶颈：高维场景配置空间极为庞大，而重要的光照效果（如焦散、锐利反射、间接光）高度局部化且稀疏，均匀采样几乎无法捕获，导致神经网络无法学到完整的全局光照。

本文提出**主动探索（Active Exploration）**策略，将训练与数据生成交织进行：利用基于MCMC的随机游走，以损失与梯度乘积为目标函数，引导采样器主动搜索训练误差最大的“困难”区域，从而以远低于均匀采样的训练预算学会复杂、局部化的光照现象。配套机制包括自调节样本重用（动态平衡渲染成本与过拟合）和自适应递增分辨率训练（从128×128逐步升至600×600，聚焦高频细节）。

实验表明，在相同训练时间下，主动探索在Living Room场景上的DSSIM较均匀采样降低41.5%，MAPE降低51.2%；与Granskog et al. (2020)的编码器-解码器方案相比，在18小时总时间下MAPE从0.823降至0.082，等质量时训练加速约7.3倍；与实时去噪方法Işık et al. (2021)相比，焦散等困难光路得以清晰重现。方法定位于可变场景神经渲染的数据生成策略改进，以显式场景参数向量替代隐式编码，在5–18小时训练后可实现4–6 fps的交互式全局光照渲染。

## 核心方法与创新机理

### 问题瓶颈与核心思路

可变场景的神经全局光照面临一个根本性效率瓶颈：场景的可变参数构成一个高维配置空间 **D**，对该空间进行均匀采样以生成训练数据，效率极低且成本高昂。关键的全局光照效果——焦散、锐利反射、间接光——在参数空间中高度局部化且稀疏，均匀采样几乎不可能捕获这些“困难”光路，导致神经网络无法学习完整的全局光照函数。

本文的核心洞察在于：**将训练与数据生成交织进行，并利用MCMC在训练数据空间中主动搜索高误差区域**。具体而言，方法维护一个以网络当前损失与梯度乘积为目标函数的马尔可夫链，在训练过程中持续引导采样器向网络难以重建的场景配置移动。这些“困难”样本被即时渲染为地面真值并注入训练，从而以远少于均匀采样的渲染预算，学会复杂、局部化的光照现象。

### 方法框架与模块因果链

整体框架由六个核心模块串联构成，形成“探索-渲染-重用-训练-增强”的闭环：

1. **场景定义与显式参数化** → 2. **主动探索MCMC采样器** → 3. **即时路径追踪渲染** → 4. **自调节样本重用** → 5. **PixelGenerator网络训练** → 6. **自适应分辨率增强**

**模块1** 从XML场景描述中提取所有可变参数（物体位置、材质属性、光源强度、相机视角等），归一化后组成显式场景表示向量 **u**。这一设计（changed slot 1）替代了先前方法（如Granskog et al., 2020）通过编码器从渲染图像中提取隐式潜变量的方案，使得场景编辑具有可解释性和精确可控性。

**模块2** 是核心创新。它维护16条平行马尔可夫链，每条对应一个训练patch。提议分布采用混合策略：以概率 $p_{\mathrm{LS}} = 0.3$ 执行大步长（从整个参数空间 **Ψ** 均匀采样），否则执行小步长（对当前状态施加正态扰动）。大步长保证全局探索，防止陷入局部区域；小步长则精细调节光源位置、材质参数等，在局部高误差区域密集采样。

接受策略采用激进的确定性规则（changed slot 2）：

$$\alpha(\mathbf{u}_i \to \mathbf{v}) = \begin{cases} 1 & \text{if } p(\mathbf{v}) > p(\mathbf{u}_i) \\ 0 & \text{else} \end{cases}$$

其中目标函数 $p(\cdot)$ 定义为当前patch上损失值与ADAM优化步长范数的乘积。仅当候选配置的目标函数值**严格大于**当前状态时才接受移动。这一设计与标准Metropolis-Hastings接受概率的本质区别在于：它不给予低概率区域任何保留机会，迫使链快速向高重要性区域聚集，同时允许网络通过充分学习逐渐降低该区域的目标函数值，自然地使链继续前进。

**模块3** 根据采样器输出的场景配置，使用Mitsuba 2 GPU路径追踪器渲染32×32的patch作为地面真值。**模块4** 引入自调节样本重用机制（changed slot 3），通过比较新渲染样本与已存储样本的损失值（指数移动平均），动态决定训练时使用旧样本还是请求新渲染：

$$p_s = \sigma(\mathrm{Loss}_{\mathrm{exist}} - \mathrm{Loss}_{\mathrm{new}} + \beta)$$

其中 $\beta = 4.6$，使得当新旧样本损失相等时重用概率高达0.99。这一机制在渲染成本与过拟合风险之间取得平衡：当新样本不再提供显著更高的训练价值时，系统倾向于重用已有数据，大幅减少昂贵的路径追踪调用。

**模块5** 采用修改版PixelGenerator架构（8层MLP，512维隐藏单元，带跳跃连接）。关键设计在于位置预调节：网络前几层仅输入世界坐标位置，使其先形成对场景几何的全局理解，随后再拼接法线、材质、出射方向等G‑buffer信息以及复制后的场景表示向量 **u**。这一设计使网络在形成阴影和焦散时能够忽略木材纹理等高频表面细节，显著加速收敛。

训练损失函数为L1损失与结构相异度损失的组合。

**模块6** 在训练过程中逐步提升渲染分辨率：从128×128开始，每2000次迭代增加4个像素，直至600×600。递增分辨率与主动探索形成正向反馈：低分辨率阶段网络快速学习全局光照的大尺度结构，高分辨率阶段主动探索自然聚焦于锐利阴影边界、镜面高光等细节区域。

### 训练与推理路径

训练时，16条马尔可夫链并行运行，每条链独立提议候选场景配置，经激进接受策略筛选后，由路径追踪器渲染对应patch。自调节样本重用模块决定是否将新渲染数据加入训练集。PixelGenerator以当前训练集为输入进行优化，其损失与梯度乘积实时反馈给MCMC采样器，更新目标函数景观，引导下一轮采样。这一“探索-渲染-训练”循环持续5-18小时（取决于场景复杂度和期望质量）。

推理时，给定任意场景配置向量 **u** 和对应G‑buffer，PixelGenerator可逐像素预测完整的全局光照图像，支持动态修改视角、材质、光源等。原型实现达到4-6 fps（Python实现，包含Mitsuba G‑buffer生成开销）。

![[assets/figures/papers/paper_list_l46_https_repo_sam_inria_fr_fungraph_active_exploration/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach. Left: During training we define a scene and the set of variable parameters via an xml file resulting in a explicit scene representation vector ??. Using Active Exploration we guide the configurations of the variable scene towards more difficult instances that are important for the PixelGenerator network. Right: After 5-18 hours of training – depending on the complexity of the variable parameters and quality required – we can interactively request any variation of the scene with visual dynamic changes in illumination, move objects, the viewpoint and modify materials*

![[assets/figures/papers/paper_list_l46_https_repo_sam_inria_fr_fungraph_active_exploration/figures/016_Figure_12.jpg]]
*Figure 12: Same quality (top) and same time (bottom) comparison with Granskog et al. [2020]. We show result of ArchViz for same quality as ours using the pretrained network provided by the authors in their rendering framework. We also show Living Room for same time as ours by training their method on our variable scene in our rendering framework. The 3 path traced observations required by Granskog et al. [2020] are shown on the right in both cases*

## 实验与关键发现

### 主结果：主动探索 vs. 均匀采样

在 Living Room 场景（Fig. 11, Table 3）上，主动探索 MCMC 与均匀采样在相同训练时间下的对比揭示了核心瓶颈的突破程度。均匀采样无法捕获焦散、锐利阴影和反射等高度局部化的光照现象，而主动探索将这些细节清晰重现。定量上，主动探索的 DSSIM 为 **0.0141**，均匀采样为 0.0241，降幅达 **41.5%**；MAPE 从 0.162 降至 **0.079**，降幅 **51.2%**。这一差距的因果根源在于：均匀采样在高维参数空间中几乎不可能命中那些对网络训练至关重要的“困难”光路配置，而主动探索通过 MCMC 随机游走将采样密度主动导向高损失×梯度区域，使网络得以在有限训练预算内学会这些稀疏但决定视觉质量的光照效果。

![[assets/figures/papers/paper_list_l46_https_repo_sam_inria_fr_fungraph_active_exploration/figures/013_Table_3.jpg]]
*Table 3: Quantitative results using 4 metrics for the configuration shown in Figure 11*

![[assets/figures/papers/paper_list_l46_https_repo_sam_inria_fr_fungraph_active_exploration/figures/012_Figure_11.jpg]]
*Figure 11: We compare our active exploration MCMC method vs. Uniform sampling of the space D trained for the same time. We see that Uniform search running for the same time cannot produce sharp shadows, reflections and caustics*

### 与先前方法的对比

**与 Granskog et al. (2020) 的编码器-解码器方案对比**（Fig. 12）构成了最具说服力的证据。在“等时间”设置下（Living Room，各18小时训练+渲染总时间），本文方法 MAPE 为 **0.082**，而 Granskog et al. 方法高达 **0.823**——后者几乎完全无法重建全局光照。即使将后者的训练时间延长至4天，其 MAPE（0.655）仍远不及本文18小时的结果。在“等质量”设置下（ArchViz），本文方法需约 **36小时**达到目标质量，而 Granskog et al. 使用预训练网络需约 **11天**，加速约 **7.3倍**。这一悬殊差距的机制在于：编码器-解码器方案试图从渲染图像中隐式编码场景配置，但其潜在空间无法准确捕捉可变参数对光照的精细影响；相反，本文的显式场景表示向量直接将归一化参数传递给 PixelGenerator，消除了编码器带来的信息瓶颈。

**与 Işık et al. (2021) 的 ANF 实时去噪方法对比**（Fig. 15, Table 4）则验证了本文方法对“硬光路”的独特优势。在 Spaceship 场景上，本文 DSSIM 为 **0.0155**，ANF 为 0.0461，降幅 **66.4%**。关键定性差异在于：路径追踪+去噪方案中，焦散和焦散阴影几乎完全消失，而本文的神经渲染器能够清晰重现这些困难光路。这是因为去噪器本质上是后处理滤波器，无法恢复在低采样率路径追踪中根本未被采到的光路；而本文方法通过主动探索在训练阶段就迫使网络学习这些光路的完整全局光照函数。

### 关键消融实验

**MCMC 目标函数的选择**（Table 7, Fig. 17）：使用损失×梯度乘积作为目标函数，显著优于仅使用损失。仅使用损失时，网络容易陷入局部极小值——MCMC 会反复采样某个高损失区域，但该区域的损失因网络容量限制无法进一步降低，导致采样浪费且结果更模糊。损失×梯度乘积则同时考虑“当前误差大”和“网络在此处有学习潜力”两个维度，引导采样至既有改进空间又能有效推动训练的区域。

**位置预调节**（Table 5, Fig. 16）：将世界坐标仅输入网络第一层（而非与其他 G‑buffer 拼接后输入所有层），使网络在形成阴影和焦散时能够忽略木材纹理等高频表面细节，从而更快收敛。定量上，该设计在所有指标上均有显著提升，其因果机制在于：预调节让网络早期层专注于建立全局光照的宏观结构，后续层再融合材质细节，避免了高频纹理对光照学习的干扰。

**自适应分辨率增强**（Table 6, Fig. 7）：训练期间从 128×128 逐步增至 600×600（每2000次迭代增加4像素），使主动探索能够更有效地解析高频信息。固定分辨率训练在定量和定性上均不及自适应方案，因为后者允许网络先学习光照的粗粒度结构，再逐步聚焦于锐利反射和阴影边缘等细节——这与主动探索聚焦“困难区域”的策略形成协同效应。

**可变维度的影响**（Fig. 14）：当场景可变参数从5维增至10维时，主动探索相对于均匀采样的损失差急剧扩大。这证实了方法的核心优势：高维空间中“困难”配置更加稀疏，均匀采样命中概率指数级下降，而 MCMC 引导的主动探索能够维持对重要区域的聚焦能力。

### 失败模式与适用边界

尽管主动探索在多个场景上展现了显著优势，其适用边界同样明确。首先，**场景表示向量的维度限制**：显式参数化要求向量维度与 G‑buffer 尺寸对齐，当变量个数过多（如数千个）时会导致内存爆炸，此时需要编码器等压缩方案，但这会牺牲显式参数化带来的编辑精度。其次，**训练时间仍然较长**（5–18小时），取决于变量复杂度和期望质量，无法满足极快速的内容更新需求。第三，**当前原型推理仅达 4–6 fps**（Python 实现，包含 Mitsuba G‑buffer 生成开销），尚未针对实时应用进行极端优化。第四，**变量重要性未差异化利用**：所有变量被归一化到同一范围，但控制高频阴影的旋转变量比颜色变量更难学习，网络的容量分配可能未达最优——MCMC 的扰动尺度也未根据每种变量的实际影响进行自适应调整。

### 公平性说明

所有对比实验均遵循严格的公平性原则：均匀采样基线同样使用了本文的样本重用策略（但不包含分辨率适应，因后者会使均匀采样表现更差）；与 Granskog et al. 的比较在“等质量”和“等时间”两种设置下分别进行，使用相同的场景和渲染器；与 Işık et al. 的比较中，将其去噪网络在本文场景数据上进行了微调并控制相同训练时长；所有方法均使用相同的 G‑buffer 输入和相同的路径追踪器生成训练数据。

![[assets/figures/papers/paper_list_l46_https_repo_sam_inria_fr_fungraph_active_exploration/figures/007_Figure_7.jpg]]
*Figure 7: Ablation study for adaptive resolution MCMC vs Uniform training. First row: the resolution is always 128x128. Second row: we progressively focus resolution, improving quality*

![[assets/figures/papers/paper_list_l46_https_repo_sam_inria_fr_fungraph_active_exploration/figures/019_Table_4.jpg]]
*Table 4: Quantitative results using 4 metrics for the configuration shown in Figure 15*

## 定位与知识库关联

### 相对已有方法的本质差异：改变的是“训练数据生成策略”这一 slot

本文在神经渲染管线中改变的核心 slot 是**训练数据生成策略**：从传统的“均匀随机采样可变场景参数空间”切换为“主动探索（Active Exploration）”，即利用 MCMC 随机游走，在训练过程中根据损失与梯度乘积定义的目标函数，将采样引导至高误差区域，从而以更少的渲染预算学会复杂、局部化的全局光照现象。这一 slot 的改变是方法有效性的根本原因，其他模块（自适应分辨率、自调节样本重用、显式场景参数化）均围绕该 slot 提供配合与加速。

与以下基线工作的本质差异如下：

- **Uniform Sampling（朴素基线）**：在高维可变场景空间中均匀采样，无法有效捕获稀疏且局部化的焦散、锐利反射和间接光，导致网络训练效率极低。本文的主动探索将采样分布动态对准“网络当前最难以学习”的区域，在相同训练时间内 DSSIM 降低 41.5%、MAPE 降低 51.2%（Table 3, Fig. 11），且随着可变维度增加优势急剧扩大（Fig. 14）。
- **Compositional Neural Scene Representations（CNSR）**（Granskog et al., ACM Trans. Graph. 2020）：CNSR 采用编码器-解码器架构，从渲染图像中提取隐式场景表示向量，训练数据同样来自均匀采样。其隐式编码缺乏可编辑性，且无法主动聚焦困难光路。本文改用**显式场景表示向量**（由所有可变参数归一化后直接组成），跳过编码器，使场景编辑可控且可解释；同时以 MCMC 主动探索替代均匀采样。在等时间对比（18 小时训练+渲染）下，CNSR 的 MAPE 为 0.823，本文方法仅 0.082；即使将 CNSR 训练时间延长至 4 天，其 MAPE 仍为 0.655，远不及本文方法（Fig. 12, Sec. 7.2.2）。在等质量对比中，本文方法仅需 36 小时，而 CNSR 需约 11 天，加速约 7.3 倍。
- **Affinity of Neural Features（ANF）denoising**（Işık et al., ACM Trans. Graph. 2021）：ANF 属于实时去噪路线，对路径追踪的少量采样结果进行神经去噪，擅长处理 diffuse 和低频光照，但难以保留焦散、焦散阴影等硬光路。本文方法在相同训练时间内能够清晰重现这些困难光路，在 Spaceship 场景上 DSSIM 降低 66.4%（Table 4, Fig. 15），体现了神经渲染器直接预测完整全局光照相对于“路径追踪+去噪”在硬光路保真度上的结构性优势。

### 知识库挂载点

本文在以下知识库节点上提供了明确的增量贡献：

1. **神经渲染中的训练数据生成策略**：将“主动学习/重要性采样”思想引入可变场景神经全局光照训练，提出了基于 MCMC 的 on-the-fly 数据生成框架。该框架以损失与 ADAM 步长范数的乘积作为目标函数（消融实验证实该乘积显著优于仅用损失，Table 7, Fig. 17），并通过激进接受策略（仅当候选状态目标函数值更大时才接受，Eq. 4）加速向高重要性区域移动。这为“训练即探索”范式在渲染领域的应用提供了可复用的模板。

2. **显式场景参数化与可编辑神经渲染**：通过将场景可变参数直接编码为显式向量并复制后馈入 PixelGenerator，实现了对视角、材质、几何位置、光源等属性的可解释、可控制调节。相比于 CNSR 的隐式编码路线，本文证明了显式参数化在编辑性和训练效率上的优势，为后续可编辑神经渲染工作提供了架构选择依据。

3. **自适应分辨率与样本重用**：自适应递增分辨率（从 128×128 逐步升至 600×600）配合主动探索，使网络能逐步聚焦高频细节（Table 6, Fig. 7）；自调节样本重用通过比较新旧样本损失的指数移动平均，动态平衡渲染成本与过拟合风险（Sec. 6.1）。这两项技术可独立迁移至其他需要昂贵训练数据生成的神经渲染任务。

### 适用边界与条件

- **变量维度上限**：当可变参数数量达到数千个时，显式场景表示向量会因需要与 G‑buffer 尺寸对齐而导致内存爆炸，此时需借助编码器等其他压缩方案。本文方法目前适用于数十到数百个变量的场景。
- **训练时间下限**：训练仍需 5–18 小时（取决于变量复杂度和期望质量），无法满足极快速的内容更新需求。
- **推理速度**：原型实现仅 4–6 fps（Python 实现，含 Mitsuba G‑buffer 生成开销），尚未针对实时应用进行极端优化。
- **变量重要性未显式建模**：当前所有变量被归一化到同一范围，不同变量对光照影响的差异（如控制高频阴影的旋转变量远比颜色变量更难学习）未被主动探索过程显式利用，网络容量分配可能未达最优。
- **网络架构固定**：采用 8 层 512 维 MLP 加跳跃连接，更大或不同的架构可能进一步提升质量或缩短训练时间。

### 后续工作启发

本文的开放问题直接指向若干可扩展方向：

- **变量重要性感知的主动探索**：将不同场景变量对光照学习难度的差异显式注入 MCMC 的目标函数或提议分布中，例如对控制高频阴影的旋转变量赋予更大的突变尺度或更高的采样权重，以进一步提升采样效率。
- **自适应变量范围归一化**：当前所有变量被归一化到 [0,1]，但 360° 旋转与 15° 旋转产生截然不同的频率变化。如何根据每种变量的实际影响动态调整 MCMC 的突变尺度，是一个值得探索的方向。
- **高维变量扩展**：如何高效处理数千甚至更多变量（如可变纹理）而不导致内存爆炸，同时仍保留显式参数化带来的编辑性和控制精度，可能需要结合编码器压缩与显式参数的混合表示方案。
- **在线主动探索**：当前方法属于预计算模式（训练完成后推理），主动探索和自调节样本重用是否可以应用于需要在线实时路径追踪的混合方案，使得训练与渲染在运行时交替进行，是一个有潜力的未来方向。
- **非浮点变量的参数化**：能否将显式场景参数化方法扩展到难以用少量浮点数表示的变量（如参数化变形），例如使用关键帧作为参数，值得进一步研究。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Active_Exploration_for_Neural_Global_Illumination_of_Variable_Scenes.pdf]]
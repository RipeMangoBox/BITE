---
title: "Underground Plant Exploration: Non-Destructive 3D Root Assessment with GPR Based on Point Graph Neural Network"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Underground_Plant_Exploration_Non_Destructive_3D_Root_Assessment_with_GPR_Based_on_Point_Graph_Neural_Network.pdf
project_link: null
code_link: null
aliases:
- OGBRD3RF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 专门针对根系双曲线特征设计的检测网络（含MobileNetV2骨干和曲线拟合模块）与基于点图神经网络的3D重建模块（残差图卷积、双池化注意力、上采样）的组合，直接提升了对微小目标的检测精度和从稀疏点云恢复几何细节的能力。
primary_logic: 利用GPR信号的双曲线形状先验进行目标检测与参数回归，并在3D阶段通过图网络在非规则点上传播和强化几何特征，从而在保留根系分支结构的前提下实现稀疏到稠密的重建。
claims:
- 在仿真GPR图像上，所提检测网络的AP达到0.857，AP-75达到0.870，均显著优于SE-SSD（AP 0.736）、Feng等人（AP 0.719）和DiffusionDet（AP 0.731）。
- 在3D点云重建任务中，所提方法的平均CD为2.03，EMD为5.03，远低于最佳对比方法PointLLM-V2的CD 6.69和EMD 14.99。
- 消融实验证实，移除点图网络或上采样模块会导致CD和EMD大幅上升，证明这两个模块对保持点云结构完整性的关键作用。
- Simulated 2D GPR Images (200 3D root models, 18,000 B-scans) 上 AP / AP-50 / AP-75 = 0.857 / 0.902 / 0.870
---

# Underground Plant Exploration: Non-Destructive 3D Root Assessment with GPR Based on Point Graph Neural Network

> [!tip] 核心洞察
> 利用GPR信号的双曲线形状先验进行目标检测与参数回归，并在3D阶段通过图网络在非规则点上传播和强化几何特征，从而在保留根系分支结构的前提下实现稀疏到稠密的重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 地下植物探测：基于探地雷达与点图神经网络的非破坏式三维根系评估 |
| 英文题名 | Underground Plant Exploration: Non-Destructive 3D Root Assessment with GPR Based on Point Graph Neural Network |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhou_Underground_Plant_Exploration_Non-Destructive_3D_Root_Assessment_with_GPR_Based_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Ours (GPR-based Root Detection and 3D Reconstruction Framework) |
| Dataset | Simulated 2D GPR Images, Synthetic 3D root point cloud dataset |

> [!tip] 效果简介
> - Simulated 2D GPR Images (200 3D root models, 18,000 B-scans) 上，AP / AP-50 / AP-75 0.857 / 0.902 / 0.870 vs 0.736 / 0.850 / 0.768 (SE-SSD, best baseline) (+0.121 / +0.052 / +0.102)。
> - Synthetic 3D root point cloud dataset (5 test roots, 8192 points each) 上，CD (×100) / EMD (×100) mean 2.03 / 5.03 vs 6.69 / 14.99 (PointLLM-V2, best baseline) (-4.66 / -9.96)。

## 概要

探地雷达（GPR）作为一种非破坏式探测技术，能够通过发射电磁脉冲并接收地下目标的反射回波来揭示土壤中的隐蔽结构。然而，将其应用于植物根系评估时面临一个根本性瓶颈：根系产生的反射信号极其微弱且稀疏，传统方法难以在强噪声背景下可靠地检测出细小的双曲线特征，更难以将检测到的稀疏二维切片点云转化为保留分支拓扑的致密三维根系模型。

针对这一难题，本文提出了一套完整的GPR根系三维重建框架，其核心洞察在于**将GPR信号的双曲线形状先验显式融入目标检测与参数回归**，并在三维阶段通过**图神经网络在非规则点上传播和强化几何特征**，从而实现从稀疏到稠密的高保真重建。该方法由两大关键模块串联构成：根系双曲线检测网络与基于点图神经网络的三维重建模块。检测网络以MobileNetV2为骨干，通过多任务头同步预测边界框、分类置信度及双曲线几何参数（顶点、曲率、弧长）；三维重建模块则通过残差图卷积、双池化注意力机制和专用上采样模块，在保持根系分支结构的前提下恢复稠密点云的几何细节。

实验结果表明，在仿真GPR图像上，所提检测网络的AP达到0.857，AP-75达到0.870，显著优于SE-SSD（AP 0.736）、Feng等人（AP 0.719）和DiffusionDet（AP 0.731）；在三维点云重建任务中，本方法的平均Chamfer Distance为2.03，Earth Mover's Distance为5.03，远低于最佳对比方法PointLLM-V2的6.69和14.99（Table 1、Table 2）。消融实验进一步证实，移除点图网络或上采样模块会导致重建质量大幅下降，表明图结构学习和上采样对保持点云结构完整性具有关键作用（Figure 11）。同时，本方法模型参数量仅20.98M，在对比方法中最小，兼顾了轻量与性能（Table 3）。

### 方法谱系与知识库定位

本工作在二维检测和三维重建两个维度上均与现有方法存在明确的继承与改进关系。

在二维检测侧，本方法以**SE-SSD**（Zheng et al., CVPR 2021）框架为基础，但进行了两项关键改造：将原有骨干网络替换为MobileNetV2（仅使用前6个逆残差模块及5个额外卷积层），以适配GPR图像中根系目标的尺度特征；在标准定位损失和分类置信度损失之外，新增曲线拟合损失 $L_{\mathrm{curve}}$，显式监督双曲线的弧长、顶点坐标和曲率参数，使检测头从单纯的“目标定位”升级为“几何参数回归”。对比基线还包括**Feng等人**（ICRA 2020）的GPR地下目标检测方法以及基于扩散模型的**DiffusionDet**（Chen et al., ICCV 2023），本方法在所有AP指标上均取得显著提升。

在三维重建侧，本方法区别于传统的直接插值或基于折叠解码器的方案（如**Polis等人**的迭代TIN生成方法，CVPR 1992），引入了点图神经网络进行结构感知的特征传播。与**VAPCNet**（Fu et al., ICCV 2023）的视角感知补全策略和**PointLLM-V2**（Xu et al., ECCV 2024）的LLM驱动点云理解路径不同，本方法通过KNN构建局部图、残差图卷积聚合邻域信息、双池化注意力（最大池化与平均池化元素乘积）突出根系关键结构，并辅以基于最远点采样的上采样模块，在保持分支拓扑的前提下实现稀疏到稠密的几何恢复。这一设计在CD和EMD指标上均大幅领先对比方法，验证了图结构先验对根系这类细长分支目标的独特适配性。

值得注意的是，本方法的GPR预处理流程也进行了精细化设计，包含时零校正、去直流、水平噪声去除、均值道背景去除、针对根系直径调谐的带通FIR滤波、SEC增益、土壤介电常数校正以及基尔霍夫/f-k偏移共八个步骤，为下游检测网络提供了更高质量的信号输入。



植物根系是陆地生态系统中最不易观测的器官，其三维构型直接决定水分与养分吸收效率，对作物育种、碳汇估算和生态建模均具有核心价值。然而，现有的根系表型测量手段长期陷入两难：**破坏性挖掘**（如根钻法、剖面法）可获得局部几何信息，却切断根系原生拓扑，无法追踪时变发育；**非破坏性成像**（如X射线CT、MRI）虽能保留三维结构，却受限于扫描体积小、成本高、难以在田间原位部署。探地雷达（Ground Penetrating Radar, GPR）提供了折中可能——通过向土壤发射高频电磁脉冲并接收来自介电常数差异界面的反射回波，可在不扰动土壤的前提下对地下根系进行大面积扫描。当GPR天线经过线状根系时，由于天线-根系垂直距离在正上方达到极小，反射波的走时曲线自然形成**双曲线形态**（Figure 2），这成为从B-scan图像中识别根系信号的关键物理先验。

然而，从GPR数据到可用的三维根系模型之间，存在一条尚未被有效跨越的鸿沟。**瓶颈集中在两个串联环节**：

1. **2D信号检测困难**。植物根系的直径通常为毫米至厘米级，其反射信号在GPR B-scan中极为微弱，且与土壤非均匀散射、天线耦合噪声和地下其他目标（石块、管道）的反射混杂。传统方法依赖人工勾画双曲线或基于阈值分割，在处理低信噪比和密集目标时漏检率高、虚警严重。深度学习方法（如SE-SSD、DiffusionDet）虽在通用目标检测上表现优异，但缺乏对根系双曲线几何形状的结构化建模，难以从稀疏噪声中稳定检测出微小且形态特定的信号。

2. **稀疏到稠密的三维重建断层**。即便成功检测到各B-scan切片中的双曲线顶点，将其沿扫描轨迹堆叠所得的初始点云仍是**极度稀疏且不规则的**——相邻切片间缺乏显式对应关系，根系分支的拓扑连续性在点云中表现为断裂的散点。现有三维点云重建方法（如Polis等人的迭代TIN生成、VAPCNet的视角感知补全、PointLLM-V2的大模型理解）或依赖密集输入，或面向通用物体补全，未针对根系这种细长分支结构的几何特性设计，导致重建结果丢失分支拓扑、表面细节模糊。

**本文的核心动机**正是打通这两个瓶颈：利用GPR信号的双曲线形状先验，在2D检测端引入专门的曲线拟合监督，使网络不仅定位目标，还回归双曲线的顶点、曲率和弧长参数；在3D重建端，通过点图神经网络在非规则稀疏点上传播和强化局部几何特征，配合上采样模块恢复分支拓扑和表面细节，最终形成一套从GPR B-scan到稠密三维根系模型的完整非破坏式评估框架。



## 核心方法与创新机理

本文的核心创新在于针对GPR根系探测中“信号微弱、特征稀疏、拓扑断裂”这一真实瓶颈，设计了一条从精细信号预处理到稀疏点云稠密重建的完整管线，并在两个关键阶段引入了结构化的方法改进。

### 创新一：双曲线形状先验驱动的检测网络

传统GPR目标检测方法（如**SE-SSD** (Zheng et al., CVPR 2021)、**DiffusionDet** (Chen et al., ICCV 2023)）将地下目标视为通用边界框，忽略了根系反射特有的双曲线几何形态。本文的核心洞察在于：**双曲线的顶点、曲率和弧长本身就是强先验**，直接回归这些参数可以显著提升对微弱信号的检测鲁棒性。

具体而言，检测网络在三个关键槽位上进行了改造：

1.  **骨干网络替换**：将SE-SSD原有的PointNet++骨干替换为**MobileNetV2的前六个逆残差模块**，并额外追加五个卷积层（Figure 4）。轻量化的设计在保持多尺度特征提取能力的同时，适配了GPR B-scan中目标尺度极小（通常仅占几十个像素）的特点。

2.  **多任务检测头扩展**：在标准定位头和分类头之外，新增**曲线拟合头**，为每个正样本锚框直接预测双曲线的弧长 `len`、顶点坐标 `vert` 和曲率 `K`。这使得网络不仅学习“目标在哪里”，还学习“目标的双曲线形态是什么”。

3.  **曲线拟合损失函数**：引入平滑L1形式的曲线损失 `L_curve`，与定位损失 `L_local` 和置信度损失 `L_conf` 加权组合：

    $$L_{\mathrm{det}} = L_{\mathrm{local}} + w_{1} L_{\mathrm{conf}} + w_{2} L_{\mathrm{curve}}$$

    其中 $w_{1}=1.0, w_{2}=0.5$。`L_curve` 定义为：

    $$L_{\mathrm{curve}} = \frac{1}{N} \sum_{q=1}^{N} \sum_{n \in \{len, vert, K\}} SL1(F_n^q - G_n^q)$$

    该损失直接监督双曲线几何参数回归，迫使网络关注反射信号的形状一致性，而非仅依赖纹理特征。消融实验表明，移除曲线拟合头会导致检测AP显著下降。

### 创新二：面向稀疏根系点云的结构感知重建网络

从多张2D B-scan检测结果拼接而成的初始3D点云极度稀疏（通常仅数百个点），且点之间缺乏显式拓扑连接。传统点云补全方法（如**Polis et al.** (CVPR 1992)的迭代TIN生成、**VAPCNet** (Fu et al., ICCV 2023)）难以从这种无序稀疏点集中恢复出根系特有的细长分支结构。本文的重建网络通过三个模块化创新解决了这一问题：

1.  **残差图卷积网络**：基于KNN在稀疏点云上构建动态图，通过带残差连接和层归一化的图卷积传播结构信息：

    $$\mathbf{h}_i^{(l+1)} = \sigma\left( \mathrm{LN}\left( \sum_{j \in \mathcal{N}(i)} \frac{1}{Z_{ij}} \mathbf{W}^{(l)} \mathbf{h}_j^{(l)} \right) + \mathbf{h}_i^{(l)} \right)$$

    残差连接与层归一化有效缓解了深层图卷积的过平滑问题，使得网络在聚合邻域信息的同时保留节点自身的几何特征。这是保持根系分支独立性的关键机制。

2.  **双池化注意力机制**：对每个节点的邻域特征分别进行最大池化和平均池化，将两者**元素相乘**得到注意力权重：

    $$\mathbf{F}_{\mathrm{att}} = \mathbf{F}_{\mathrm{max}} \odot \mathbf{F}_{\mathrm{avg}}$$

    随后通过残差连接增强原始特征：$\mathbf{F}_{\mathrm{enh}} = \mathbf{F}_{\mathrm{att}} + \mathcal{G}_{1}(\mathbf{h}_i)$。最大池化捕获邻域中的显著结构信号（如分支点），平均池化提供上下文平滑，两者乘积实现了对根系关键结构的选择性突出。

3.  **仿射归一化上采样模块**：采用最远点采样选取种子点，聚合其K近邻特征后，通过仿射归一化（减均值除标准差）稳定特征分布，再经MLP扩展点数。这一设计确保上采样生成的新点沿根系分支方向分布，而非在空间中均匀填充。

重建总损失由粗粒度Chamfer Distance、细粒度Earth Mover's Distance和K-NN隔离损失加权组成：

$$L_{\mathrm{recon}} = L_{\mathrm{coarse}} + w_{3} L_{\mathrm{fine}} + w_{4} L_{\mathrm{iso}}$$

其中 $w_{3}=0.3, w_{4}=0.1$，隔离损失通过惩罚生成点与K近邻的平均距离，显式约束点云沿分支方向的紧凑性。

### 创新三：面向根系信号的八步精细预处理

预处理管线本身虽非算法创新，但其**针对根系弱信号的系统性调谐**构成了方法有效性的重要支撑。八步流程包括：时零校正→去直流→水平噪声去除→均值道背景去除→带通FIR滤波（针对根系直径调谐截止频率）→SEC增益→土壤介电常数校正→基尔霍夫/f-k偏移。其中，**均值道背景去除**被论文明确指认为最具影响力的单步操作，因其能有效压制背景杂波，使微弱的根系双曲线信号得以凸显（Figure 3）。

### 消融实验的关键证据

消融实验（Figure 11）揭示了各模块的因果贡献层级：**移除点图网络或上采样模块**造成的CD和EMD上升幅度，远大于移除注意力机制。这表明，对于稀疏根系点云重建任务而言，**图结构传播和上采样策略是保持点云正确性与根系完整性的首要因素**，注意力机制则起到精细化增强的辅助作用。同时，完整方法以仅20.98M的参数量（Table 3）在对比方法中实现了最小模型规模，验证了设计的轻量性。



本文提出一种基于探地雷达（GPR）的植物根系非破坏式三维评估框架，以**两阶段级联管线**为核心：首先从GPR B-scan中检测根系产生的微弱双曲线反射信号并生成稀疏三维点云，随后通过点图神经网络从该稀疏点云中重建保留分支拓扑的稠密根系结构。

### 管线总览

整个系统（图1）的数据流如下：

1. **GPR信号采集**：天线沿地表扫描，发射电磁脉冲并接收来自地下根系的反射回波。当天线位于根系正上方时，电磁波传播路径最短，在B-scan中形成特征性的双曲线图案（图2）。
2. **预处理**：对原始B-scan执行八步精细预处理——时零校正、去直流（dewow）、水平噪声去除、均值道背景去除、针对根系直径调谐的带通FIR滤波、SEC增益、土壤介电常数校正以及基尔霍夫/f-k偏移。其中均值道背景去除对增强微弱根系双曲线信号最为关键。
3. **双曲线检测**：预处理后的B-scan送入以MobileNetV2为骨干的检测网络，多任务头同时预测边界框、类别置信度以及双曲线的几何参数（顶点坐标、曲率、弧长），经NMS后处理得到各切片的检测结果。
4. **稀疏点云构建**：沿扫描轨迹将所有2D检测结果聚合，形成初始的稀疏3D根系点云。
5. **3D重建**：在稀疏点云上构建KNN图，通过带残差连接与层归一化的图卷积传播几何特征，并引入双池化注意力机制（最大池化与平均池化元素乘积）突出根系关键结构，最后经最远点采样与仿射归一化的上采样模块将点云稠密化，生成保留分支拓扑的最终根系模型（图5）。

### 两阶段级联的设计逻辑

该框架的核心设计逻辑在于**利用GPR信号的双曲线形状先验进行目标检测与参数回归**，并在3D阶段通过**图网络在非规则点上传播和强化几何特征**，从而在保留根系分支结构的前提下实现稀疏到稠密的重建。

- **检测阶段的关键设计**：不同于通用目标检测，根系双曲线信号微弱且稀疏，因此检测网络不仅预测边界框，还额外引入曲线拟合损失 $L_{\text{curve}}$ 来监督双曲线的几何参数回归。完整的检测目标函数为：

  $$L_{\mathrm{det}} = L_{\mathrm{local}} + w_{1} L_{\mathrm{conf}} + w_{2} L_{\mathrm{curve}}$$

  其中 $w_1=1.0$，$w_2=0.5$。定位损失 $L_{\mathrm{local}}$ 对匹配的正样本锚框进行平滑L1回归，分类置信度损失 $L_{\mathrm{conf}}$ 区分前景与背景，而 $L_{\mathrm{curve}}$ 对每个正样本的弧长、顶点坐标和曲率参数施加平滑L1约束。

- **重建阶段的关键设计**：稀疏点云缺乏足够的几何信息来直接表征根系分支结构。点图神经网络通过图卷积在节点间传播特征，其更新规则为：

  $$\mathbf{h}_i^{(l+1)} = \sigma\left( \mathrm{LN}\left( \sum_{j \in \mathcal{N}(i)} \frac{1}{Z_{ij}} \mathbf{W}^{(l)} \mathbf{h}_j^{(l)} \right) + \mathbf{h}_i^{(l)} \right)$$

  残差连接与层归一化有效缓解了深层图卷积的过平滑问题。注意力增强特征 $\mathbf{F}_{\mathrm{enh}} = \mathbf{F}_{\mathrm{att}} + \mathcal{G}_{1}(\mathbf{h}_i)$ 通过 $\mathbf{F}_{\mathrm{att}} = \mathbf{F}_{\mathrm{max}} \odot \mathbf{F}_{\mathrm{avg}}$ 突出局部关键结构。重建总损失由粗粒度Chamfer Distance、细粒度Earth Mover's Distance和K-NN隔离损失加权组成：

  $$L_{\mathrm{recon}} = L_{\mathrm{coarse}} + w_{3} L_{\mathrm{fine}} + w_{4} L_{\mathrm{iso}}$$

  其中 $w_3=0.3$，$w_4=0.1$，联合优化点云的全局分布与局部几何一致性。

### 模块间的依赖关系

检测模块的输出质量直接影响重建模块的输入条件。为公平评估重建性能，所有对比实验统一使用所提检测网络生成的稀疏点云作为输入，避免了检测质量差异对下游重建对比的干扰。消融实验进一步揭示，点图网络和上采样模块对保持点云结构完整性具有决定性作用——移除其中任一组件均会导致CD和EMD大幅上升，其影响程度超过移除注意力机制。

### 补充图表

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed 3D root reconstruction pipeline utilizing GPR data. The system first detects hyperbolic root signals from GPR B-scans to generate a sparse 3D root point cloud (left), followed by interpolation techniques to reconstruct a dense and detailed root structure (right)*

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of GPR signal acquisition for subsurface root detection. The system emits short electromagnetic pulses into the soil, capturing reflected echoes from buried targets. When the antenna is positioned directly over a root, the travel time and vertical distance to the target are minimized, generating a characteristic hyperbolic pattern in GPR B-scans*



### 2D根系双曲线检测模块

检测模块的核心任务是从GPR B-scan中同时定位根系双曲线并回归其几何参数。该模块以**SE-SSD**（Zheng et al., CVPR 2021）框架为基础，进行了两项关键改造。

**骨干网络替换**：将原有基于PointNet++的骨干替换为**MobileNetV2**，提取前6个逆残差模块（至conv_6）的特征图作为多尺度特征金字塔。这一设计利用了MobileNetV2的轻量特性，同时5个额外卷积层进一步扩展感受野，以捕获不同尺度根系双曲线的上下文信息（Figure 4）。

**多任务检测头**：检测头同时输出三组预测——边界框定位、分类置信度，以及双曲线几何参数（顶点坐标vert、曲率K、弧长len）。完整检测目标函数为三部分损失的加权和：

$$L_{\mathrm{det}} = L_{\mathrm{local}} + w_{1} L_{\mathrm{conf}} + w_{2} L_{\mathrm{curve}}$$

其中 $w_{1}=1.0$，$w_{2}=0.5$。定位损失 $L_{\mathrm{local}}$ 对匹配的正样本锚框进行边界框回归监督，采用平滑L1损失（$SL1$）对宽高取对数后计算偏差，对中心坐标取归一化偏差：

$$L_{\mathrm{local}} = \sum_{i \in \mathcal{P}} \sum_{k \in \{w, h\}} SL1(\log \frac{P_k^i}{D_k^{j(i)}}) + \sum_{i \in \mathcal{P}} \sum_{k \in \{x, y\}} SL1(\frac{P_k^i - D_k^{j(i)}}{D_k^{j(i)}})$$

$$SL1(x) = \begin{cases} \frac{1}{2}x^2, & \text{if } |x| < 1 \\ |x| - 0.5, & \text{otherwise} \end{cases}$$

**曲线拟合损失** $L_{\mathrm{curve}}$ 是本文检测模块区别于通用检测器的关键创新，它对每个正样本预测的双曲线弧长len、顶点vert和曲率K施加平滑L1约束：

$$L_{\mathrm{curve}} = \frac{1}{N} \sum_{q=1}^{N} \sum_{n \in \{len, vert, K\}} SL1(F_n^q - G_n^q)$$

该损失显式编码了GPR信号的双曲线形状先验，使网络不仅“找到目标”，还能“理解目标的几何形态”，为后续3D重建提供更丰富的几何线索。

---

### 点图神经网络重建模块

从检测到的2D切片沿扫描轨迹构建初始稀疏3D点云后，核心挑战在于从非规则分布的稀疏点中恢复保持分支拓扑的密集根系结构。本文提出**点图神经网络**（Point Graph Neural Network），通过图结构传播和注意力机制增强局部几何特征（Figure 6）。

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/007_Figure_6.jpg]]
*Figure 6: Architecture of the proposed point graph neural network. This framework enhances feature representation by propagating spatial and structural information across sparse root point clouds while incorporating attention mechanisms for improved detail preservation*

**图构建与残差图卷积**：基于KNN在点云上构建局部图 $\mathcal{G}=(\mathcal{V}, \mathcal{E})$。节点 $i$ 在第 $l$ 层的特征更新规则为：

$$\mathbf{h}_i^{(l+1)} = \sigma\left( \mathrm{LN}\left( \sum_{j \in \mathcal{N}(i)} \frac{1}{Z_{ij}} \mathbf{W}^{(l)} \mathbf{h}_j^{(l)} \right) + \mathbf{h}_i^{(l)} \right)$$

其中 $\mathcal{N}(i)$ 为节点 $i$ 的邻居集合，$Z_{ij}$ 为归一化因子，$\mathbf{W}^{(l)}$ 为可学习权重矩阵，$\mathrm{LN}$ 为层归一化，$\sigma$ 为非线性激活函数。**残差连接** $\mathbf{h}_i^{(l)}$ 的引入是防止深层图卷积过平滑的关键设计，确保节点在聚合邻域信息时不丢失自身独有的结构特征。

节点聚合特征由相对边缘特征、绝对点上下文和位置编码拼接后经函数 $\mathcal{G}$ 映射得到：

$$\mathbf{h}_i = \mathcal{G}\big( \big[ \mathbf{h}_{ij} - \mathbf{h}_i, \mathbf{h}_i, \mathbf{f}_{\mathrm{pos}} \big] \big)$$

**双池化注意力机制**：为进一步突出根系关键结构（如分支点、细根末端），对节点邻域特征分别进行最大池化和平均池化，然后元素相乘生成注意力权重：

$$\mathbf{F}_{\mathrm{att}} = \mathbf{F}_{\mathrm{max}} \odot \mathbf{F}_{\mathrm{avg}}$$

$$\mathbf{F}_{\mathrm{enh}} = \mathbf{F}_{\mathrm{att}} + \mathcal{G}_{1}(\mathbf{h}_i)$$

最大池化捕获邻域中最显著的结构信号（如分支拐点），平均池化保留整体上下文，二者逐元素乘积形成自适应的结构感知注意力，有效抑制噪声点干扰。消融实验（Figure 11）表明，移除点图网络或上采样模块造成的性能下降比移除注意力机制更严重，证明图结构学习是保持点云正确性与根系完整性的瓶颈环节。

---

### 点云上采样模块

为从稀疏点云恢复稠密根系几何，上采样模块采用“采样-聚合-扩展”策略（Figure 7）。首先通过**最远点采样（FPS）** 选取种子点，确保覆盖点云全局分布；对每个种子点 $p_i$，聚合其K近邻特征 $F_{\mathrm{agg},i}$，并通过仿射归一化稳定特征分布：

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/006_Figure_7.jpg]]
*Figure 7: Architecture of the proposed point cloud upsampling module. This network refines and densifies sparse root point clouds while maintaining structural consistency*

$$F_{m} = \frac{F_{\mathrm{agg},i} - \mu(F_{\mathrm{agg},i})}{\sigma(F_{\mathrm{agg},i})}$$

归一化后的特征经MLP扩展为 $r$ 倍点数（$r$ 为上采样率），生成稠密且保留分支拓扑的点云。该模块与图神经网络形成级联——图网络负责传播和强化结构特征，上采样模块负责在特征空间中进行几何扩展，二者协同实现稀疏到稠密的高保真重建。

---

### 多阶段重建损失函数

重建总损失由粗粒度、细粒度和正则化三项加权组成：

$$L_{\mathrm{recon}} = L_{\mathrm{coarse}} + w_{3} L_{\mathrm{fine}} + w_{4} L_{\mathrm{iso}}$$

其中 $w_{3}=0.3$，$w_{4}=0.1$。

- **$L_{\mathrm{coarse}}$（Chamfer Distance）**：度量粗重建点云与真值之间的平均最近点距离，约束全局形状对齐。
- **$L_{\mathrm{fine}}$（Earth Mover's Distance）**：度量两个点集分布之间的最小传输代价，对局部几何差异更敏感，引导细粒度结构恢复。
- **$L_{\mathrm{iso}}$（K-NN隔离损失）**：计算每个点与其K近邻的平均距离，作为正则项防止生成点过度聚集或产生离群噪声。

三项损失的联合优化使重建结果在全局形态、局部细节和点分布均匀性三个层面同时逼近真实根系结构。

### 补充图表

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/005_Figure_4.jpg]]
*Figure 4: Architecture of the hyperbola detection framework. The model utilizes a MobileNetV2-based backbone for multi-scale feature extraction, followed by a multi-task detection head that simultaneously predicts bounding boxes, classification confidence, and specific hyperbola geometry parameters*

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/004_Figure_5.jpg]]
*Figure 5: Pipeline for the 3D root reconstruction process. The graph will be built among the 3D points through a graph neural network and the branches will be connected and interprelated*

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of GPR B-scans before and after preprocessing. Left: Raw GPR scan with substantial noise and signal distortion. Right: Enhanced scan after applying pre-processing techniques, improving root structure visibility and reducing environmental interference*



## 实验与关键发现

### 实验设置

**数据集构建**：实验基于两类数据。仿真数据集包含200个三维根系模型，通过gprMax正演模拟生成18 000张2D GPR B-scan图像，用于检测网络的训练与测试。三维点云重建实验从测试集中随机选取5个独立根系，每个标准化为8 192点。真实数据由SIR-4000主机搭配800D天线实地采集，用于定性验证。

**对比基线**：2D检测任务对比**SE-SSD**（Zheng et al., CVPR 2021）、**Feng et al.**（ICRA 2020）以及**DiffusionDet**（Chen et al., ICCV 2023）。3D重建任务对比传统三角网插值方法**Polis et al.**（CVPR 1992）、视角感知补全网络**VAPCNet**（Fu et al., ICCV 2023）和基于大语言模型的**PointLLM-V2**（Xu et al., ECCV 2024）。所有对比方法均采用其论文推荐的最佳配置，在相同数据集上训练与评估。重建实验统一使用所提检测网络生成的稀疏点云作为输入，避免检测质量差异对下游对比的干扰。

**评价指标**：检测任务采用AP、AP-50、AP-75。重建任务采用Chamfer Distance（CD，×100）和Earth Mover's Distance（EMD，×100），数值越低表示重建精度越高。

---

### 2D根系双曲线检测结果

Table 1给出了仿真GPR图像上的定量对比。所提方法在全部指标上取得最优：AP达到**0.857**，AP-50为**0.902**，AP-75为**0.870**。相比最强基线SE-SSD（AP 0.736，AP-75 0.768），AP提升0.121，AP-75提升0.102。这一差距在高IoU阈值下更为突出，表明MobileNetV2骨干与曲线拟合损失联合优化有效提升了对微小双曲线目标的定位精度。Feng et al.的传统方法（AP 0.719）和DiffusionDet（AP 0.731）均显著落后，说明通用检测器难以处理GPR中低信噪比的双曲线特征。

Figure 8的可视化对比进一步印证：所提方法检测框贴合双曲线边界，漏检和虚警明显少于对比方法。真实GPR B-scan上的定性结果（Figure 9）同样显示，本文方法在非理想条件下仍能稳定捕获根系双曲线，而对比方法在信号微弱处频繁漏检。

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/009_Figure_9.jpg]]
*Figure 9: Comparison of root target detection results in real-world GPR B-scans. From left to right: Input real-world GPR; Detection by our root hyperbola detection network; Detection from SE-SSD [51]; Detection from [14]; Detection from DiffusionNet [6]*

---

### 3D根系点云重建结果

Table 2汇报了重建量化结果。所提完整管线取得平均CD **2.03**、EMD **5.03**，远优于最佳对比方法PointLLM-V2（CD 6.69，EMD 14.99）。VAPCNet和Polis et al.的误差更大（CD分别约9.28和11.45），表明传统插值与通用点云补全方法无法从稀疏切片点云中恢复根系的分支拓扑和几何细节。

Figure 10的视觉对比揭示了性能差异的结构性原因：Polis et al.生成的根系断裂、分支缺失严重；VAPCNet虽能补全大体形状，但细支扭曲或消失；PointLLM-V2的点云分布松散，缺少明确的枝干结构。相比之下，本文方法重建的根系在分支连续性、粗细过渡和空间走向上与真实点云高度一致。

---

### 消融实验

Figure 11展示了针对3D重建模块的消融结果。移除点图网络（Ours w/o point graph network）后，CD和EMD分别显著上升，点云结构出现断裂和分支丢失，证明图卷积在非规则点上传播结构信息对保持根系拓扑至关重要。移除上采样模块（Ours w/o upsampling network）同样导致指标恶化，点云密度不足、枝干不完整。移除注意力机制（Ours w/o attention）的影响相对较小，但仍造成可观测的性能下降。消融实验证实，图结构学习和上采样对点云正确性与根系完整性的贡献大于注意力机制，三者协同作用方能实现稀疏到稠密的高质量重建。

---

### 模型复杂度分析

Table 3对比了各方法的参数量与推理速度。所提方法参数量仅**20.98M**，在对比方法中最小，兼顾了轻量与性能。这一优势得益于MobileNetV2骨干的高效设计和点图网络的紧凑结构。需注意，论文未完整报告推理速度数据，该结论需结合实际部署环境进一步验证。

---

### 局限性讨论

论文未报告失败案例的详细分析，但结合开放问题和实验设计可识别以下潜在失效模式：

1. **检测-重建级联误差传播**：前级检测的漏检或误检会直接传递至重建阶段，导致3D根系缺失或伪影，论文未量化该误差链的影响程度。
2. **预处理依赖现场测量**：八步预处理中的土壤介电常数校正依赖现场标定，在全自动部署场景下可能引入额外误差，不同土壤类型下的参数适应性未经验证。
3. **数据集规模有限**：重建实验仅在5个测试根上进行，统计显著性不足；真实数据仅用于定性展示，缺少大规模野外验证。
4. **细长结构断裂风险**：当根系分支极细或间距过近时，图网络的KNN构图可能跨分支连接，上采样可能产生虚假粘连，该边界条件未讨论。

### 补充图表

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/010_Table_1.jpg]]
*Table 1: Quantitative Comparisons of Root Target Detection Performance with [51], [14] and [6] on Simulated 2D GPR Images*

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/012_Table_2.jpg]]
*Table 2: Quantitative point cloud reconstruction results. CD and EMD of different methods are reported. CD and EMD are both scaled by 100. The comparison is conducted and reported on five independent roots randomly selected from the test set. Lower values indicate better performance for both EMD and CD metrics*

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/014_Figure_11.jpg]]
*Figure 11: Ablation analysis results comparing point cloud reconstruction between our method and various ablated settings. CD and EMD are reported and multiplied by 100. Lower values indicate better performance for both metrics*

![[assets/figures/papers/paper_list_l2650_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Underground_Plant/figures/013_Table_3.jpg]]
*Table 3: Comparisons of different methods in terms of the number of model parameters and inference speed (in seconds per sample)*



## 定位与知识库关联

### 任务定位与核心瓶颈

本文针对**地下植物根系的三维非破坏性评估**这一交叉任务，其输入为探地雷达（GPR）沿测线采集的B-scan序列，输出为保留分支拓扑的稠密3D根系点云。该任务的本质瓶颈在于：GPR信号中根系产生的反射能量微弱且稀疏，传统方法难以从强噪声背景中可靠检测细小的双曲线特征，并进一步将稀疏的2D切片点云转换为保持拓扑连续性的密集3D结构。本文的核心洞察在于**利用GPR双曲线的几何先验进行目标检测与参数回归，并在3D阶段通过图神经网络在非规则点上传播和强化结构特征**，从而在保留根系分支结构的前提下实现从稀疏到稠密的重建。

### 方法谱系与知识继承

#### 2D检测阶段：从通用目标检测到双曲线感知检测

本文的根系双曲线检测网络以**SE-SSD**（Zheng et al., CVPR 2021）为基础框架进行改造。SE-SSD原为点云3D检测器，其骨干基于PointNet++提取点特征。本文将其迁移至2D GPR图像域后，做出了两项关键改造：

1. **骨干网络替换**：将SE-SSD原有的PointNet++骨干替换为**MobileNetV2**（前6个逆残差模块 + 5个额外卷积层），以适应2D图像的轻量多尺度特征提取需求。这一选择兼顾了推理效率与特征表达能力，最终模型参数量仅20.98M，在对比方法中最小。

2. **多任务检测头扩展**：在标准定位损失和分类置信度损失之外，新增**曲线拟合损失** $L_{\mathrm{curve}}$，对每个正样本预测其双曲线的弧长、顶点坐标和曲率参数，采用平滑L1损失监督。检测总损失为：
   $$L_{\mathrm{det}} = L_{\mathrm{local}} + w_{1} L_{\mathrm{conf}} + w_{2} L_{\mathrm{curve}}$$
   其中 $w_{1}=1.0$，$w_{2}=0.5$。这一设计显式编码了GPR双曲线的几何先验，使检测头不仅输出边界框，还回归双曲线形状参数，为后续3D重建提供更丰富的几何线索。

在对比基线方面，本文与三类代表性方法进行了比较：**Feng et al.**（ICRA 2020）是专门针对GPR地下目标检测的传统方法；**DiffusionDet**（Chen et al., ICCV 2023）代表基于扩散模型的检测新范式。实验表明，在仿真GPR图像上本文方法的AP达到0.857，显著优于SE-SSD（0.736）、Feng et al.（0.719）和DiffusionDet（0.731），验证了双曲线几何先验编码的有效性。

#### GPR预处理：领域知识的系统化工程化

本文的GPR信号预处理流程体现了对领域知识的深度整合。八步精细预处理管线包括：时零校正、去直流、水平噪声去除、均值道背景去除、带通FIR滤波（针对根系直径调谐）、SEC增益、土壤介电常数校正、基尔霍夫/f-k偏移。其中，**均值道背景去除**被论文明确指出为“对增强根系双曲线特征影响最大的步骤之一”。这一系统化的预处理工程为后续检测网络提供了高质量的输入，但其介电常数校正依赖现场测量，可能限制全自动部署。

#### 3D重建阶段：从传统插值到图神经网络

在3D点云重建方面，本文的方法谱系跨越了从传统几何方法到现代深度学习方法的演进路径：

- **传统基线**：**Polis et al.**（CVPR 1992）代表基于迭代TIN生成的经典方法，依赖显式的几何假设，难以处理稀疏和噪声数据。
- **深度学习点云补全**：**VAPCNet**（Fu et al., ICCV 2023）引入视角感知机制进行点云补全，但缺乏对根系分支拓扑的显式建模。
- **大语言模型驱动的点云理解**：**PointLLM-V2**（Xu et al., ECCV 2024）将大语言模型引入点云任务，在本文实验中是表现最佳的对比方法，但其CD（6.69）和EMD（14.99）仍远高于本文方法（2.03 / 5.03）。

本文提出的重建管线由三个核心模块构成：

1. **点图神经网络**：基于KNN构建点云图，通过带残差连接与层归一化的图卷积传播特征：
   $$\mathbf{h}_i^{(l+1)} = \sigma\left( \mathrm{LN}\left( \sum_{j \in \mathcal{N}(i)} \frac{1}{Z_{ij}} \mathbf{W}^{(l)} \mathbf{h}_j^{(l)} \right) + \mathbf{h}_i^{(l)} \right)$$
   残差连接缓解了深层图卷积的过平滑问题，保留根系分支的拓扑结构。

2. **双池化注意力机制**：对节点邻域特征分别进行最大池化和平均池化，元素相乘得到注意力权重，再与原始变换特征相加：
   $$\mathbf{F}_{\mathrm{enh}} = \mathbf{F}_{\mathrm{att}} + \mathcal{G}_{1}(\mathbf{h}_i) \quad \text{with} \quad \mathbf{F}_{\mathrm{att}} = \mathbf{F}_{\mathrm{max}} \odot \mathbf{F}_{\mathrm{avg}}$$
   该设计突出根系关键结构点，增强对细小分支的感知能力。

3. **上采样模块**：采用最远点采样选取种子点，聚合其K近邻特征后经仿射归一化与MLP扩展点数，生成稠密且保留分支拓扑的根系点云。

重建总损失由粗粒度Chamfer Distance、细粒度Earth Mover's Distance和K-NN隔离损失加权组成：
$$L_{\mathrm{recon}} = L_{\mathrm{coarse}} + w_{3} L_{\mathrm{fine}} + w_{4} L_{\mathrm{iso}}$$
其中 $w_{3}=0.3$，$w_{4}=0.1$，联合优化点云的全局分布与局部几何。

### 适用边界与局限

1. **土壤与频率鲁棒性未验证**：本文仅在单一模拟数据集和有限真实采集上评估，未测试不同土壤类型（黏土、砂土等）、含水量及GPR中心频率下的性能。预处理中的介电常数校正依赖现场测量，全自动部署受限。

2. **数据集规模与泛化能力存疑**：合成数据集包含200个3D根系模型和18,000张B-scan，测试集仅5个根系。缺乏大规模野外根系系统的验证，向真实复杂根系（如须根系、缠绕根系）的迁移能力不明。

3. **级联误差传播未分析**：检测和重建为级联系统，前级检测的遗漏或误检对最终3D结构的影响程度未做定量分析。消融实验虽证明了各模块的重要性，但未解耦检测误差对重建的干扰。

4. **实时性约束**：点图网络与上采样模块的计算开销在移动平台或手持式GPR上的可行性未讨论，推理速度表部分数据缺失。

5. **任务迁移潜力待验证**：该方法是否可迁移至其他细长目标的检测与重建（如地下管道裂缝、昆虫巢穴），尚需扩展研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Underground_Plant_Exploration_Non_Destructive_3D_Root_Assessment_with_GPR_Based_on_Point_Graph_Neural_Network.pdf]]

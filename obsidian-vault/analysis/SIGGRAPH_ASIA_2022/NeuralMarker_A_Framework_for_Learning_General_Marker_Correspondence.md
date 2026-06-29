---
title: "NeuralMarker: A Framework for Learning General Marker Correspondence"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/NeuralMarker_A_Framework_for_Learning_General_Marker_Correspondence.pdf
project_link: null
code_link: "https://github.com/drinkingcoder/NeuralMarker"
aliases:
- NeuralMarker
tags:
- SIGGRAPH_ASIA_2022
- topic/other_unclear
core_operator: 通过合成包含各种几何变形的FlyMarkers数据集训练运动回归器，使网络学会处理复杂变形；并通过SED损失利用SfM提供的光照变化图像进行弱监督训练，促使图像特征编码器对光照变化不变，从而在无需密集对应标注的情况下实现鲁棒的密集标记对应。
primary_logic: 将标记对应学习分解为几何变化和外观变化两个独立挑战：使用合成数据应对几何变形，使用基于SfM的SED弱监督应对光照变化，两者结合使网络同时具备对变形和光照的鲁棒性，极大提升泛化性能。
claims:
- 在DVL-Markers变形/视角/光照三个子集上，NeuralMarker的SSIM和PSNR均大幅超越所有对比方法，且失败率为0%。
- 在FlyingMarkers测试集上，NeuralMarker的PCK-5达到99%，表明运动回归器几乎能捕获所有标记变换与变形。
- 消融实验证明，加入SED损失在合成数据上仅轻微降低PCK-1，但将DVL-Markers变形子集的SSIM中位数从0.52大幅提升至0.69，并使得模型能够推广至真实场景。
- DVL-Markers (Deformation) 上 SSIM (median) = 0.69
---

# NeuralMarker: A Framework for Learning General Marker Correspondence

> [!tip] 核心洞察
> 将标记对应学习分解为几何变化和外观变化两个独立挑战：使用合成数据应对几何变形，使用基于SfM的SED弱监督应对光照变化，两者结合使网络同时具备对变形和光照的鲁棒性，极大提升泛化性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | NeuralMarker：通用标记对应关系学习框架 |
| 英文题名 | NeuralMarker: A Framework for Learning General Marker Correspondence |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://drinkingcoder.github.io/publication/neuralmarker/) · [Code](https://github.com/drinkingcoder/NeuralMarker) |
| Topic | #topic/other_unclear |
| Method | NeuralMarker |
| Dataset | DVL-Markers, FlyingMarkers test set |

> [!tip] 效果简介
> - DVL-Markers (Deformation) 上，SSIM (median) 0.69 vs 0.30 (R-Flow) (+0.39)。
> - DVL-Markers (Viewpoint) 上，SSIM (median) 0.77 vs 0.57 (SIFT+H) (+0.20)。
> - DVL-Markers (Lighting) 上，SSIM (median) 0.82 vs 0.63 (SP+SG+H) (+0.19)。

## 概要

传统标记对应估计依赖稀疏特征匹配与单应性模型，仅适用于平面场景，无法处理非平面变形和显著光照变化；同时真实场景下像素级密集对应标注难以获取，使数据驱动方法缺乏训练数据。NeuralMarker 将这一挑战分解为几何变化与外观变化两个独立问题：通过合成包含随机仿射、单应与薄板样条变形的 FlyMarkers 数据集训练运动回归器，使网络学会处理复杂几何变形；同时提出对称极线距离（SED）损失，利用 SfM 从不同光照条件下的图像中获取相机位姿进行弱监督，促使图像特征编码器对光照变化保持不变性，从而在无需密集对应标注的情况下实现鲁棒的密集标记对应。

在 DVL-Markers 基准上，NeuralMarker 在变形、视角和光照三个子集上的 SSIM 中位数分别达到 0.69、0.77 和 0.82，远超 SIFT+H、SP+SG+H、R-Flow 和 PDC-Net 等对比方法，且失败率为 0%。在 FlyingMarkers 合成测试集上 PCK-5 达 99%。消融实验表明，预训练 Twins-SVT Transformer 编码器与 SED 弱监督损失是泛化性能的关键：加入 SED 损失后，变形子集 SSIM 中位数从 0.52 提升至 0.69，而合成数据上的 PCK-1 仅从 0.95 降至 0.89，证明该方法在保持合成数据精度的同时大幅增强了真实场景鲁棒性。

方法定位于标记对应学习框架，以 RAFT 式迭代对应回归为基础，通过合成数据监督与 SfM 弱监督的组合训练策略，填补了通用标记对应学习中几何鲁棒性与光照鲁棒性同时解决的空白。

## 核心方法与创新机理

### 问题瓶颈与解耦策略

传统标记对应估计面临两个相互纠缠的核心瓶颈：**几何变化**与**外观变化**。基于SIFT特征匹配加单应性估计的方法（如SIFT+H）仅适用于平面场景，无法处理非平面变形；基于光流或语义对应的深度方法（如R-Flow、PDC-Net）虽能建模密集对应，但依赖真实场景的像素级密集对应标注，而此类标注在实际中几乎无法获取。这导致数据驱动的深度学习方法在真实场景下泛化能力严重不足。

NeuralMarker的核心洞察是将这一复杂问题**解耦为两个独立子问题**：几何变形挑战通过合成数据应对，外观变化挑战通过弱监督应对。两者分别针对网络的不同能力维度，最终联合训练使模型同时具备对变形和光照的鲁棒性。

### 整体框架与模块顺序

NeuralMarker的神经网络架构遵循RAFT的光流估计范式，由两个核心阶段构成：**Siamese图像特征编码**与**迭代运动回归**。训练时额外引入两个数据/损失模块：合成数据生成模块（FlyingMarkers）和弱监督模块（SED损失）。

**推理路径**：给定标记图像 $I_M$ 和参考图像 $I_R$，首先通过共享权重的Siamese特征编码器分别提取两者的特征图，计算4D相关体积以衡量所有像素对之间的外观相似度；随后迭代运动回归器从相关体积和上下文特征中逐步回归像素级对应残差，最终输出从标记到参考图像的密集对应场 $f_{RM}$。

**训练路径**：每次迭代输入一个三元组 $(I_M, I_{R1}, I_{R2})$，其中 $(I_M, I_{R1})$ 来自FlyingMarkers合成数据集，提供密集对应真值用于监督损失 $L_{Syn}$；$(I_M, I_{R2})$ 来自SfM采集的真实光照变化图像对，利用相机位姿计算SED弱监督损失 $L_{SED}$。总损失为两者之和：

$$L_{all}(I_M, I_{R1}, I_{R2}) = L_{Syn}(I_M, I_{R1}) + L_{SED}(I_M, I_{R2})$$

### Changed Slot 1：图像特征编码器——从CNN到Twins-SVT Transformer

传统光流网络（如RAFT）使用CNN提取局部特征，但CNN的有限感受野使其难以捕捉标记与参考图像之间的全局外观对应，尤其在视角变化剧烈或非平面变形时，局部纹理可能产生歧义匹配。

NeuralMarker将特征编码器替换为**预训练的Twins-SVT Transformer**。Twins-SVT是一种融合局部窗口注意力和全局子采样注意力的混合架构，能够在保持计算效率的同时编码全局上下文特征。这一替换的因果机制在于：标记对应本质上需要判断“标记上的某个角点对应参考图像中的哪个位置”，而全局特征使网络能够利用整个图像的结构信息进行匹配，而非仅依赖局部邻域的纹理相似度。

消融实验（Table 4）证实了该替换的决定性作用：使用CNN编码器时，模型在DVL-Markers上几乎完全失效（SSIM中位数接近0），而仅将编码器换为Twins-SVT后，变形子集SSIM中位数跃升至0.52，视角子集达0.39，光照子集达0.46。这表明**全局特征编码是实现跨域泛化的必要条件**，CNN的局部特征在合成数据上虽可收敛，但无法推广到真实场景的复杂变形和视角变化。

![[assets/figures/papers/paper_list_l74_https_drinkingcoder_github_io_publication_neuralmarker/figures/008_Table_4.jpg]]
*Table 4: Ablation study. ‘Twins +*

### Changed Slot 2：合成数据生成模块——FlyingMarkers

受FlyingChairs和FlyingThings等光流合成数据集的启发，NeuralMarker构建了**FlyingMarkers合成数据集**，通过程序化生成包含密集对应真值的标记-参考图像对，专门应对几何变化挑战。

数据生成流程如下：从自然图像中随机裁剪矩形区域作为“标记”，对该标记施加一系列几何变换生成参考图像，包括随机仿射变换、随机单应变换和薄板样条（TPS）变形。TPS变形能够模拟非刚性表面（如弯曲的纸张、飘动的旗帜）产生的复杂变形，这是传统单应性模型完全无法处理的场景。最终数据集包含176,167个训练样本，每个样本提供像素级密集对应真值 $\mathbf{T}(\mathbf{x}_i)$。

合成数据上的监督损失定义为预测对应与真值之间的L1距离：

$$L_{Syn}(I_M, I_R) = \sum_{\mathbf{x}_i \in S} || f_{RM}(\mathbf{x}_i) - \mathbf{T}(\mathbf{x}_i) ||_1$$

该损失直接监督运动回归器学习从外观特征到几何对应的映射，使网络能够捕获几乎任意形式的2D变形。Table 2显示，在FlyingMarkers测试集上NeuralMarker的PCK-5达到0.99，表明运动回归器几乎完美拟合了合成数据的变形分布。

### Changed Slot 3：弱监督模块——SED损失

合成数据虽然覆盖了丰富的几何变形，但无法模拟真实场景中的光照变化、曝光差异、阴影和高光等外观变化。若仅使用 $L_{Syn}$ 训练，模型对光照变化极为敏感，在DVL-Markers光照子集上表现不佳。

为解决这一瓶颈，NeuralMarker提出**对称极线距离（SED）损失**，利用SfM（Structure from Motion）采集的真实场景图像进行弱监督训练。具体而言，对同一平面场景在不同光照条件下拍摄多张图像，通过SfM恢复相机内参和相对位姿，得到基础矩阵 $\mathbf{F}$。对于图像对 $(I_A, I_B)$ 中的任一像素 $\mathbf{x}$，其预测对应点 $f_{BA}(\mathbf{x})$ 应位于 $\mathbf{x}$ 在 $I_B$ 中的极线 $l'$ 上。SED定义为预测点对到彼此极线的距离之和：

$$SED(\mathbf{x}, \mathbf{x}', \mathbf{F}) = ED(\mathbf{x}, \mathbf{x}', \mathbf{F}) + ED(\mathbf{x}', \mathbf{x}, \mathbf{F}^T)$$

其中 $ED(\mathbf{x}, \mathbf{x}', \mathbf{F})$ 为点 $\mathbf{x}'$ 到极线 $\mathbf{F}\mathbf{x}$ 的距离。对称设计确保约束的双向一致性。整张图像的SED损失为所有像素的SED之和：

$$L_{SED}(I_A, I_B) = \sum_{\mathbf{x}_i \in S} SED(\mathbf{x}_i, f_{BA}(\mathbf{x}_i), \mathbf{F})$$

SED损失的核心机制在于：它**不要求像素级对应真值**，仅利用相机位姿提供的极线几何约束，迫使网络学习对光照变化不变的特征表示。由于极线约束是几何必然性（同一3D点在两视图中的投影必位于对应极线上），该损失在数学上是严格的弱监督信号。训练时，SfM图像对与合成数据以混合批次形式输入，$L_{SED}$ 与 $L_{Syn}$ 联合优化，使特征编码器同时学习几何变形不变性和光照不变性。

消融实验（Table 4）揭示了SED损失的因果效应：在Twins-SVT + $L_{Syn}$ 基础上加入 $L_{SED}$ 后，DVL-Markers变形子集SSIM中位数从0.52提升至0.69（+0.17），视角子集从0.39提升至0.67（+0.28），光照子集从0.46提升至0.82（+0.36）。值得注意的是，FlyingMarkers测试集上的PCK-1仅从0.95微降至0.89，表明SED损失在几乎不损害合成数据拟合能力的前提下，大幅增强了真实场景的泛化性能。

### 模块间因果关系总结

三个Changed Slot之间存在清晰的因果依赖链：**Twins-SVT编码器提供全局特征表示能力**，这是后续所有模块发挥作用的基础（CNN编码器下即使加入SED损失也无法挽救性能）；**FlyingMarkers合成数据训练运动回归器处理几何变形**，使网络具备密集对应估计的基本能力；**SED弱监督损失迫使特征编码器对光照变化不变**，在保持几何估计精度的同时消除外观变化的干扰。三者缺一不可，共同构成了从合成域到真实域的泛化桥梁。

![[assets/figures/papers/paper_list_l74_https_drinkingcoder_github_io_publication_neuralmarker/figures/012_Figure_9.jpg]]
*Figure 9: Limitations. Row 1: NeuralMarker still fails when the motion blur is so severe. Row 2: Without occlusion mask prediction, the marker directly warped by predicted correspondences will cover the occluder*

## 实验与关键发现

NeuralMarker 在合成基准和真实场景基准上均展现出对标记对应估计的压倒性优势，其核心性能来源于两个独立组件的协同作用：合成数据驱动的运动回归器赋予网络处理任意几何变形的能力，而 SED 弱监督损失则使特征编码器对光照变化获得强鲁棒性。

### DVL-Markers 真实场景基准：全面超越现有方法

DVL-Markers 基准包含变形（Deformation）、视角（Viewpoint）和光照（Lighting）三个子集，共 300 张测试图像，通过将标记按预测对应关系变形后与参考图像计算 SSIM 和 PSNR 来评估对应精度。Table 1 的结果表明，NeuralMarker 在所有三个子集上均以显著优势超越所有对比方法，且失败率为 0%。

在最具挑战性的变形子集上，NeuralMarker 的 SSIM 中位数达到 **0.69**，而最强基线 R-Flow 仅为 0.30，提升幅度高达 **+0.39**。传统稀疏特征加单应性方法（SIFT+H、SP+SG+H）在此场景下几乎完全失效（SSIM 中位数分别为 0.05 和 0.02），因为单应性模型无法表达非平面变形。值得注意的是，即便是同为深度学习密集对应方法的 PDC-Net，其 SSIM 中位数也仅为 0.22，说明通用光流或几何对应网络未经针对性设计时，难以泛化到标记对应这一特定任务。

在视角子集上，NeuralMarker 的 SSIM 中位数达到 **0.77**，相较 SIFT+H（0.57）提升 **+0.20**，相较 SP+SG+H（0.55）提升 **+0.22**。在光照子集上，SSIM 中位数达到 **0.82**，相较 SP+SG+H（0.63）提升 **+0.19**。这两个子集的结果共同验证了 SED 弱监督训练的有效性：通过利用 SfM 采集的不同光照条件下的图像对，网络学会了提取对光照变化不变的外观特征，从而在真实光照剧烈变化的场景中仍能建立准确的像素级对应。

Figure 6 的定性可视化进一步佐证了定量结果：在极端变形、大视角变化和恶劣光照条件下，NeuralMarker 估计的对应关系能够将标记精确对齐到参考图像，而其他方法则出现明显的错位、扭曲或完全失效。

![[assets/figures/papers/paper_list_l74_https_drinkingcoder_github_io_publication_neuralmarker/figures/006_Figure_6.jpg]]
*Figure 6: Marker Correspondence Visualization on the DVL-Markers Benchmark. We show an extreme reference image of the same marker for each condition and visualize the estimated marker correspondences*

### FlyingMarkers 合成基准：运动回归器几乎捕获所有变形

FlyingMarkers 测试集提供了像素级密集对应的真值标注，可直接用 PCK 指标评估对应精度。Table 2 显示，NeuralMarker 的 PCK-5 达到 **0.99**，PCK-3 为 **0.97**，PCK-1 为 **0.89**，全面超越所有对比方法。相比之下，PDC-Net 的 PCK-5 仅为 0.82，PCK-1 仅为 0.42；R-Flow 的 PCK-5 为 0.80，PCK-1 为 0.28。这一结果证明，在经过 FlyMarkers 合成数据的充分训练后，运动回归器几乎能够捕获所有标记经历的仿射、单应和薄板样条变形。PCK-1 的 0.89 表明，即使在最严格的 1 像素误差阈值下，绝大多数像素的对应估计仍然精确。

![[assets/figures/papers/paper_list_l74_https_drinkingcoder_github_io_publication_neuralmarker/figures/007_Table_2.jpg]]
*Table 2: Evaluation on the test set of FlyingMarkers with PCK-1, PCK-3, and PCK-5*

### 消融实验：编码器选择与 SED 损失的决定性作用

Table 4 的消融实验揭示了两个关键设计选择的因果效应。

**特征编码器从 CNN 到 Twins-SVT 的转变是泛化能力的基石。** 当使用 CNN（遵循 RAFT 设计）作为特征编码器且仅用合成数据训练时（CNN + L_Syn），模型在 DVL-Markers 三个子集上几乎完全不可用，SSIM 中位数接近 0。这表明 CNN 提取的局部特征无法泛化到真实场景中未见过的标记和光照条件。替换为预训练的 Twins-SVT Transformer 后（Twins + L_Syn），变形子集 SSIM 中位数跃升至 0.52，视角子集升至 0.39，光照子集升至 0.46。Transformer 的全局感受野使其能够编码更具判别力和不变性的外观特征，这是泛化的前提条件。

**SED 弱监督损失在保持合成性能的同时大幅提升真实场景鲁棒性。** 在 Twins + L_Syn 基础上加入 SED 损失（Twins + L_Syn + L_SED，即最终模型），DVL-Markers 变形子集 SSIM 中位数从 0.52 进一步提升至 **0.69**（+0.17），视角子集从 0.39 升至 0.77（+0.38），光照子集从 0.46 升至 0.82（+0.36）。光照子集高达 0.36 的提升幅度直接印证了 SED 损失的设计初衷——通过 SfM 数据中的光照变化图像对施加极线约束，强制特征编码器学习光照不变表示。同时，FlyingMarkers 上的 PCK-1 仅从 0.95 轻微下降至 0.89，说明 SED 损失并未损害网络处理几何变形的能力，两者形成了良好的互补。

### 数据规模效应

Table 3 展示了训练数据场景数量对性能的影响。当仅使用 1 个场景的数据训练时，FlyingMarkers 上的 PCK-1 仅为 0.042，模型几乎无法学习到有意义的对应关系。随着场景数量从 1 逐步增加到 176，PCK-1 单调提升至 0.887，且未出现饱和迹象。这表明标记对应学习受益于数据多样性，更大的数据规模有望带来进一步的性能增益。

![[assets/figures/papers/paper_list_l74_https_drinkingcoder_github_io_publication_neuralmarker/figures/009_Table_3.jpg]]
*Table 3: PCK with different scales of training data. The models are evaluated on the test set of FlyingMarkers*

### 难度梯度分析

Figure 7 展示了不同方法在 DVL-Markers 变形子集各难度等级上的性能曲线。NeuralMarker 在所有难度等级上均保持领先，且性能随难度增加而下降的幅度明显小于其他方法。在最高难度等级（level 5）上，其他方法的 SSIM 中位数普遍降至 0.2 以下，而 NeuralMarker 仍维持在较高水平，证明其对极端变形具有独特的鲁棒性。

![[assets/figures/papers/paper_list_l74_https_drinkingcoder_github_io_publication_neuralmarker/figures/010_Figure_7.jpg]]
*Figure 7: Performance in increasing difficulty levels on DVL-Markers*

### 失败模式与适用边界

尽管 NeuralMarker 在绝大多数场景下表现优异，论文明确指出了其局限性。**严重运动模糊**是主要失败模式之一（Figure 9 Row 1）：当标记图像出现严重运动模糊时，特征编码器无法提取有效的外观特征，导致对应估计失败。当前 DVL-Markers 基准未包含运动模糊场景的定量评估，这一边界条件的量化尚待补充。

**无遮挡推理能力**是另一关键局限（Figure 9 Row 2）：NeuralMarker 估计的密集对应无法区分遮挡区域，直接将标记按对应关系变形到目标图像上会覆盖前景遮挡物。这在视频编辑和 AR 应用中会引入明显的伪影，需要额外的遮挡掩膜预测模块来解决。

此外，当前框架每次只能处理单个标记，无法在单次前向传递中同时估计多个标记的对应关系。对于包含多个标记的场景，需要多次独立运行，计算效率受限。

## 定位与知识库关联

NeuralMarker 的核心定位是**首个面向通用标记对应（marker correspondence）的深度学习框架**，其根本贡献在于将标记对应问题分解为几何变化和外观变化两个独立轴，并通过合成数据与弱监督的协同训练实现跨轴泛化。相对于已有工作，NeuralMarker 改变了三个关键 slot：

### 1. 相对于传统稀疏对应方法（SIFT+H、SP+SG+H）

传统方法（**SIFT** Lowe, 2004；**SuperPoint+SuperGlue** Sarlin et al., 2020）依赖稀疏特征点匹配后估计单应性矩阵，其核心假设是场景为平面或近似平面。这一假设在非平面变形（如弯曲、褶皱的标记表面）下必然失效，且稀疏匹配对光照剧烈变化的鲁棒性有限。NeuralMarker 将**对应估计的几何模型从单应性（全局参数化变换）替换为密集像素级运动回归器（非参数化流场）**，使模型能处理任意非刚体变形。这一改变的本质是放弃了“平面假设”这一知识库中的经典约束，转而让网络从数据中学习变形的分布。

### 2. 相对于光流与语义对应方法（R-Flow、PDC-Net）

**R-Flow**（Shen et al., 2020）和 **PDC-Net**（Truong et al., 2021）等基于光流或学习几何对应的方法虽然能输出密集对应，但它们是为通用图像对设计的，未针对标记对应场景进行专门优化。NeuralMarker 的关键差异在于**训练数据的构造策略**：通过 FlyMarkers 合成数据集，系统性地覆盖仿射、单应、薄板样条等多种几何变形分布，使运动回归器在训练阶段即见过远超真实场景中可能出现的变形模式。这一策略借鉴了光流领域 **FlyingChairs/FlyingThings**（Dosovitskiy et al., 2015; Mayer et al., 2016）的合成数据驱动范式，但将其适配到标记对应这一特定任务上。知识库挂载点在于：**合成数据预训练 + 真实数据微调**的范式在光流估计中已被验证有效，NeuralMarker 证明了该范式同样适用于标记对应，前提是合成数据的变形分布足够丰富。

### 3. 核心创新：SED 弱监督损失对光照泛化的作用

这是 NeuralMarker 相对所有 baseline 最本质的差异 slot。传统方法（包括基于深度学习的 R-Flow、PDC-Net）在训练时仅依赖像素级监督或自监督信号，难以获取覆盖真实光照变化的密集对应标注。NeuralMarker 引入**对称极线距离（SED）损失**，利用 SfM 从多光照图像集合中恢复的相机位姿作为弱监督信号，约束预测对应点在极线上的位置，从而**在不需密集标注的情况下使图像特征编码器学会对光照变化不变**。

这一设计的深层洞察在于：几何对应学习（由 $L_{Syn}$ 驱动）和外观不变性学习（由 $L_{SED}$ 驱动）可以解耦训练。$L_{Syn}$ 负责教会网络“标记可以怎么变形”，$L_{SED}$ 负责教会网络“光照变化时标记长什么样”。两者通过共享的图像特征编码器（Twins-SVT）和运动回归器（ConvGRU）协同作用，使最终模型同时具备对变形和光照的鲁棒性。消融实验（Table 4）提供了决定性证据：仅用 $L_{Syn}$ 训练时，DVL-Markers 变形子集的 SSIM 中位数仅为 0.52；加入 $L_{SED}$ 后提升至 0.69，同时 FlyingMarkers 上的 PCK-1 仅从 0.95 降至 0.89，证明 SED 损失在几乎不损害合成数据性能的前提下大幅增强了真实场景泛化能力。

### 适用边界与局限性

NeuralMarker 的适用边界由以下因素界定：

1. **单标记假设**：当前框架一次仅处理一个标记，无法在单次前向传递中检测并对应多个标记。这与实际 AR 或视频编辑场景中可能同时出现多个标记的需求存在差距。
2. **无遮挡推理**：估计的密集对应不区分遮挡区域，直接将标记变形到目标图像上会覆盖前景遮挡物。这限制了其在复杂场景下的编辑应用。
3. **运动模糊敏感**：定性结果（Fig. 9）显示，在严重运动模糊下 NeuralMarker 仍会失败。这源于训练数据（FlyMarkers 和 SfM 图像）未系统性覆盖运动模糊分布。
4. **基准覆盖缺口**：DVL-Markers 基准未包含运动模糊场景的定量评估，因此模型在该条件下的性能缺乏系统证据。

### 知识库挂载点与后续启发

NeuralMarker 在知识库中的挂载点可归纳为：

- **RAFT 架构的领域适配**：将 RAFT（Teed and Deng, 2020）的光流估计架构迁移到标记对应任务，核心改动是将 CNN 特征编码器替换为预训练 Transformer（Twins-SVT），以获取全局感受野对光照变化的鲁棒性。
- **合成数据驱动的变形学习**：继承 FlyingChairs/FlyingThings 的合成数据范式，通过随机变形场生成覆盖广泛几何变化的训练样本。
- **极线约束作为弱监督信号**：将多视图几何中的极线约束转化为可微损失函数，实现无需密集标注的外观不变性学习。这一思路可推广到其他需要跨光照泛化的密集对应任务。

后续研究可沿以下方向展开：
- **多标记联合检测与对应**：将标记检测（如角点检测或语义分割）与对应估计集成到端到端框架中。
- **遮挡感知对应**：扩展框架以同时预测遮挡掩膜，使变形后的标记能正确融入场景。
- **时序一致性**：利用视频帧间的时序信息提升对应的平滑性和准确性，尤其在运动模糊和遮挡场景下。
- **轻量化部署**：探索知识蒸馏或高效架构设计，使 NeuralMarker 能在移动端实现实时推理。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/NeuralMarker_A_Framework_for_Learning_General_Marker_Correspondence.pdf]]
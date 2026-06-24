---
title: "DEF: Deep Estimation of Sharp Geometric Features in 3D Shapes"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/DEF_Deep_Estimation_of_Sharp_Geometric_Features_in_3D_Shapes.pdf
project_link: "https://www.opencascade.com/"
code_link: "https://github.com/artonson/def"
aliases:
- DDEF
- DEF
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 将尖锐特征检测从逐点二分类转换为回归截断距离场，并采用基于局部补丁的CNN预测与多视图融合策略，从而实现对任意规模点云的高效处理。
primary_logic: 通过回归到最近特征线的截断距离场，可以自然地处理未精确落在特征上的点样本，并且局部图像补丁上的CNN能够学习丰富的几何上下文，再通过视图合成融合多个补丁的预测以重建完整的距离场，从而显著提升了在噪声和不同采样密度下的鲁棒性。
claims:
- "Histogram loss 在验证集上相对于L2损失将RMSE从101.3×10^{-3}降低到61.5×10^{-3}，Recall从24.2%提升到57.4% (Table 1)。"
- "DEF网络在合成补丁上的RMSE达到11.1×10^{-3}，Recall 80.02%，FPR 0.02%，全面优于VCM、EC-Net等方法 (Table 2)。"
- 在完整3D形状上，DEF实现了Recall 79.0%且FPR仅为0.5%，与VCM的Recall相似但FPR低近10倍 (Table 3)。
- 在真实扫描数据上，DEF的Recall达到91.7%（2 mm阈值），而VCM只能达到其约1/3 (Table 4)。
---

# DEF: Deep Estimation of Sharp Geometric Features in 3D Shapes

> [!tip] 核心洞察
> 通过回归到最近特征线的截断距离场，可以自然地处理未精确落在特征上的点样本，并且局部图像补丁上的CNN能够学习丰富的几何上下文，再通过视图合成融合多个补丁的预测以重建完整的距离场，从而显著提升了在噪声和不同采样密度下的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | DEF：三维形状中尖锐几何特征的深度估计 |
| 英文题名 | DEF: Deep Estimation of Sharp Geometric Features in 3D Shapes |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2011.15081) · [Code](https://github.com/artonson/def) · [arXiv](https://arxiv.org/abs/2103.02766) · [Project](https://www.opencascade.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | DEF (Deep Estimators of Features) |
| Dataset | DEF-Sim local patches, Parametric curve extraction on ABC shapes |

> [!tip] 效果简介
> - DEF-Sim local patches (r_high=0.02, w/bg) 上，RMSE ×10^{-3} 9.7 (CNN DEF) vs 11.3 (DGCNN) (-1.6)。
> - Parametric curve extraction on ABC shapes 上，Chamfer Distance 0.04 (DEF) vs 0.97 (PIE-NET) (-0.93)。

## 概要

从三维扫描数据中精确检测尖锐几何特征（如棱线、折痕）是几何处理的基础难题。现有方法大多将特征检测建模为逐点二分类任务，对点采样不对齐和噪声高度敏感，且受限于固定大小的全局输入，难以扩展到包含数百万点的大规模点云。

本文提出 **DEF（Deep Estimators of Features）**，将特征检测从分类问题转化为**回归截断距离场**的问题——即预测每个点到最近特征曲线的截断距离。核心思路是：首先将三维形状分解为大量局部深度图像补丁，利用 **CNN（U-Net/ResNet-152）** 在规则网格上高效回归距离场；然后通过**基于扭曲的多视图合成**将局部预测融合为完整三维模型上的一致距离场估计。训练中采用**直方图损失**替代传统 MSE，显著提升了回归精度和召回率。

在合成数据和真实扫描数据上的实验表明，DEF 在完整三维形状上实现了 **79.0% 的召回率**，且误报率（FPR）仅为 0.5%，比最优竞争方法 VCM 低近一个数量级；在噪声和缺失的真实扫描数据上，召回率达到 **91.7%**，约为 VCM 的三倍。该方法首次实现了对任意规模点云的尖锐特征距离场估计，并支持下游参数化特征曲线提取。

## 核心方法与创新机理

### 问题定义与瓶颈分析

三维形状中尖锐几何特征的可靠检测是逆向工程、CAD重建和机器人感知中的基础性问题。传统方法将特征检测建模为**逐点二分类任务**——给定一个点，判断其是否位于尖锐特征上。这一范式存在两个根本性瓶颈：其一，对点样本与真实特征线之间的微小不对齐极度敏感，采样点几乎不可能精确落在特征线上，导致分类器在特征附近区域产生大量假阳性；其二，现有方法（如EC-Net、PIE-NET）要求将整个形状下采样为固定大小的全局点集，无法扩展到包含数百万点的大规模点云。这两个瓶颈的根源在于**离散分类表示无法编码空间距离信息**，使得模型在特征线邻域内缺乏平滑的置信度衰减机制。

### 核心洞察：从分类到截断距离场回归

DEF的核心创新在于**将尖锐特征检测从逐点二分类转换为回归截断距离场（truncated distance-to-feature field）**。对于三维空间中的任意点 $p$，定义其到最近特征曲线的欧氏距离：

$$\| q(p) - p \| = \min_{\gamma_k \in \Gamma} \inf_{q \in \gamma_k} \| q - p \|$$

其中 $\Gamma$ 为所有尖锐特征曲线段的集合。为避免远距离值主导训练，引入截断操作：

$$d^{\varepsilon}(p) = \min(\| q(p) - p \|, \varepsilon)$$

这一表示转换带来了三个关键优势：（1）**自然的空间容错性**：即使采样点未精确落在特征线上，距离值仍能提供连续的接近度信息，从根本上解决了点样本不对齐问题；（2）**丰富的上下文信息**：距离场在特征线两侧形成平滑的梯度场，CNN可以从局部图像补丁中学习到特征线的几何走向和邻域结构；（3）**下游任务兼容性**：距离场可直接通过阈值化提取特征点集，或作为后续参数化曲线拟合的输入。

### 方法框架：四大模块的因果链条

DEF的完整流水线由四个顺序耦合的模块构成，形成从数据生成到特征提取的闭环：

**模块1：训练数据构建（Training Data Construction）**
从ABC数据集的CAD模型中提取局部三角化补丁，通过虚拟相机（Fibonacci球面采样，$n_v$ 个视点）进行光线投射生成深度图像。对每个补丁，仅使用穿过补丁内部的尖锐特征曲线段计算截断距离场标注 $d^{\varepsilon}(p)$，特征曲线由相邻面法向夹角超过阈值 $\alpha_{\text{norm}} = 18^\circ$ 的网格边定义。这一局部标注策略（仅包含内部特征线，排除外部特征线）是后续单视图预测一致性的关键预处理步骤——它迫使网络学习补丁内的局部几何上下文，而非依赖全局特征拓扑。

**模块2：基于补丁的深度估计器（Patch-Based Deep Estimators）**
将每个局部补丁渲染为 $64 \times 64$ 像素的深度图像 $P_i$，输入CNN回归器 $f(\cdot; \theta)$，输出为同尺寸的距离场预测。训练目标为最小化预测与真值之间的损失：

$$\min_{\theta} \frac{1}{N} \sum_{i=1}^{N} L(d_i, f(P_i; \theta))$$

网络架构采用U-Net或ResNet-152骨干网络。这一模块的核心因果机制在于：**CNN在规则网格上的卷积操作天然适合捕捉深度图像中的局部几何模式**（如折痕、角点、曲面弯曲），而基于点云的MLP/图网络（如DGCNN）缺乏这种空间归纳偏置，需要从无序点集中隐式学习几何结构，效率显著更低。

**模块3：完整3D模型上的全局融合（Estimation on Complete 3D Models）**
单视图预测仅覆盖局部区域且存在视点依赖的不一致性。DEF采用基于扭曲视图合成的多视图融合策略：对每个源视图的预测距离场，通过相机投影关系将其重投影到目标视图的图像平面：

$$\widehat{\boldsymbol{p}} = \boldsymbol{K} \boldsymbol{T}_s^{-1} \boldsymbol{T}_t ( \boldsymbol{I}_t(\boldsymbol{p}) \cdot \boldsymbol{K}^{-1} \boldsymbol{p} )$$

其中 $\boldsymbol{K}$ 为相机内参矩阵，$\boldsymbol{T}_s, \boldsymbol{T}_t$ 分别为源视图和目标视图的外参矩阵，$\boldsymbol{I}_t(\boldsymbol{p})$ 为目标视图在像素 $\boldsymbol{p}$ 处的深度值。重投影后进行线性插值，最终对每个点的多视图预测取**最小值**作为融合后的距离估计。最小值融合的因果逻辑在于：距离场在真实特征线处应趋近于零，任何单视图的高估（假阳性）都会被其他视图的低值覆盖，从而系统性地抑制FPR。

**模块4：特征拟合（Feature Fitting，可选）**
从融合后的距离场中，通过阈值化提取候选特征点集，再使用参数化曲线拟合算法（基于B样条或直线段）重建显式的特征曲线表示。这一模块将稠密的距离场转换为轻量级的CAD兼容表示，直接服务于逆向工程下游应用。

### 关键创新槽位：五个维度的系统性变更

相较于现有方法，DEF在五个关键设计槽位上进行了根本性替换：

**槽位1：任务表示（分类→回归）**
基线方法（VCM、EC-Net、PIE-NET）均输出离散的特征/非特征标签，DEF输出连续的截断距离值。这一变更使得模型能够表达“距离特征线有多近”的细粒度信息，是后续所有性能提升的根源。

**槽位2：输入形式（全局点云→局部深度图像补丁）**
传统方法将整个形状下采样为固定点数（如2048点）的全局点集，DEF将形状分解为可变数量的 $64 \times 64$ 局部深度图像补丁。这一变更解决了可扩展性问题——补丁数量随形状复杂度线性增长，而非受限于固定输入维度。

**槽位3：模型架构（点云网络→CNN）**
基线方法使用DGCNN、PointNet++等点云专用架构，DEF采用U-Net/ResNet-152等成熟CNN架构。CNN在规则网格上的卷积归纳偏置使其能够高效学习深度图像中的局部几何模式，而点云网络需要从无序点集中隐式重建空间结构。

**槽位4：损失函数（MSE/MAE→直方图损失）**
传统回归任务使用L2或L1损失，DEF采用直方图损失（Histogram loss）：将距离值离散化为244个bin，网络预测每个bin的置信度，最终输出为置信度加权和。直方图损失对距离分布的多模态性和离群值更鲁棒，在验证集上将RMSE从 $101.3 \times 10^{-3}$ 降低至 $61.5 \times 10^{-3}$，Recall从24.2%提升至57.4%（Table 1）。

**槽位5：全局融合（无→多视图最小值融合）**
现有方法要么单次推断整个形状，要么简单聚合局部预测，DEF通过基于相机几何的扭曲视图合成和最小值池化实现全局一致的距离场重建。这一融合策略是连接局部补丁预测与完整3D形状估计的关键桥梁。

### 训练与推理路径

**训练阶段**：从ABC数据集中采样CAD模型，提取局部补丁并生成深度图像-距离场训练对。网络在合成数据上训练，使用直方图损失和Adam优化器。关键训练策略包括：（1）在训练集中包含带有深度不连续性和背景的补丁，以改善边界附近预测的稳定性（Figure 19）；（2）数据集大小达到64K补丁时性能趋于饱和（Table 10）；（3）使用更大的ResNet-152骨干网显著提升回归质量（Table 11）。

**推理阶段**：对输入点云（来自深度扫描或采样），首先从多个视点渲染深度图像补丁，每个补丁独立通过CNN预测距离场，然后通过多视图扭曲合成和最小值融合重建完整距离场，最后可选地通过阈值化和曲线拟合提取参数化特征线。整个流程对点云规模具有线性可扩展性——计算成本与补丁数量成正比，而非与总点数成正比。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2011_15081/figures/023_Figure_18.jpg]]
*Figure 18: Our current pipeline improves corner detection (row 1) and is able to resolve complex curves (row 2), whereas Wireframes outputs imprecise curve graphs that lead to outlier curves with extreme variation*

## 实验与关键发现

DEF的实验评估围绕四个层次展开：补丁级距离场回归精度、完整3D形状上的距离场重建质量、真实扫描数据的泛化能力，以及下游参数曲线提取的端到端性能。核心对比基线包括基于Voronoi协方差矩阵的**VCM**（Mérigot et al., 2010）、基于学习的**EC-Net**（Yu et al., 2018）、**PIE-NET**（Wang et al., 2020）和**PC2WF**（Liu et al., 2021）等。

### 损失函数消融：直方图损失的决定性作用

在补丁级验证集上，损失函数的选择对回归质量产生根本性影响（Table 1）。将MSE损失替换为直方图损失（Histogram loss, Imani & White 2018）后，RMSE从$101.3 \times 10^{-3}$骤降至$61.5 \times 10^{-3}$，Recall（1r阈值）从24.2%跃升至57.4%。直方图损失的核心机制在于：它通过预测244个距离bin的置信度分布并计算加权和作为最终输出，有效缓解了距离场中尖锐峰值的回归困难——MSE倾向于将尖锐特征平滑化，而直方图损失允许网络以概率分布的形式表达对距离值的不确定性。这一消融直接确立了直方图损失作为DEF训练的标准配置。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2011_15081/figures/011_Table_1.jpg]]
*Table 1: In our experiments, directly optimizing Histogram loss [Imani and White 2018] significantly improves performance across different quality measures. We present results computed using the validation set of depth images (with background), with sampling distance*

### 补丁级主实验：全面超越现有方法

在合成深度图像补丁上（Table 2），DEF的CNN回归器（基于U-Net/ResNet-152）达到RMSE $11.1 \times 10^{-3}$、Recall 80.02%、FPR仅0.02%。与基于点云的方法相比，基于DGCNN的回归器RMSE为$11.3 \times 10^{-3}$（Table 6），DEF略优但差距不大；然而在分割指标上，CNN方法显著优于所有基线。**VCM**作为传统几何方法，Recall仅约40%且FPR高达约5%；**EC-Net**和**PIE-NET**等基于分类的方法在补丁级也未能达到DEF的召回率-误报率平衡。这一优势源于CNN在规则网格上能够有效利用空间上下文——深度图像中特征线表现为深度不连续或曲率突变，卷积核天然适合捕捉这类局部模式。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2011_15081/figures/016_Table_2.jpg]]
*Table 2: Our local patch-based networks for distance-to-feature estimation and feature line segmentation are more effective compared to competitor methods across a variety of segmentation and regression quality measures (evaluated on synthetic image patches, ?? = 50, ?? = 0.02)*

### 完整3D形状重建：低误报率的突破

将补丁级预测通过多视图融合重建完整距离场后（Table 3），DEF在ABC数据集上实现Recall 79.0%、FPR仅0.5%。与最强几何基线VCM相比，DEF的Recall与之相当，但FPR降低了近10倍（VCM的FPR约5%）。这一差异的因果链在于：VCM基于局部协方差分析，对平坦区域中的噪声和采样不均匀敏感，容易将平滑曲面误判为特征；而DEF通过回归截断距离场$d^\varepsilon(p)$，在远离特征线的区域天然输出接近$\varepsilon$的常数值，经阈值截断后不会产生虚假特征响应。最小值融合策略进一步抑制了单视图预测中的不一致误检。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2011_15081/figures/017_Table_3.jpg]]
*Table 3: Our method is able to reconstruct a robust estimate of a distanceto-feature field defined for a complete 3D shape. While DEF achieves similar Recall to VCM, it does so by truncating an accurate distance field and demonstrates nearly 10× lower FPR*

### 真实扫描数据的泛化能力

在RangeVision Spectrum扫描仪采集的84个3D打印模型数据集上（Table 4），DEF展现出显著的sim-to-real泛化优势。以2 mm阈值计，DEF的Recall达到91.7%，而VCM仅约其1/3；同时DEF保持适中的FPR。定量上，DEF重建的完整距离场RMSE为1.5 mm，95分位数RMSE为2.9 mm。这一结果验证了合成数据训练的策略有效性：训练时注入的噪声模型（高斯噪声$\sigma^2$从0到$0.005$）和深度不连续性补丁（Figure 19消融）使网络学会区分真实特征与扫描伪影。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2011_15081/figures/018_Table_4.jpg]]
*Table 4: Compared to the closest state-of-the-art competitor approach, VCM, our method achieves 3× higher Recall (4?? ) on noisy and incomplete scanned data, while maintaining a moderate FPR (4?? ). Quantitatively, our method reconstructs the full distance-to-feature field with*

### 鲁棒性分析：噪声与采样密度的双重优势

Figure 13系统分析了各方法对噪声和采样密度的敏感性。在噪声维度上，随着噪声方差从0增加到$0.005$，VCM和EC-Net的Recall急剧下降（VCM从约40%降至约15%），而DEF的Recall仅从约80%降至约70%。在采样密度维度上，当采样距离从$0.01$增大到$0.04$时，DEF保持Recall约75%，而VCM降至约25%。这种鲁棒性来源于两个设计选择：（1）回归距离场而非硬分类，使得网络在远离特征线的区域输出平滑的常数值，对局部扰动不敏感；（2）多视图融合中取最小值操作天然容忍个别视图的漏检。

### 关键消融实验

**训练数据规模**（Table 10）：训练补丁数量从1K增加到64K时，RMSE持续下降；超过64K后性能趋于稳定，表明64K补丁已覆盖足够的几何多样性。

**骨干网络容量**（Table 11）：从ResNet-18到ResNet-152，RMSE逐步改善，验证了更大容量模型对距离场精细结构的建模能力。

**背景与深度不连续性**（Figure 19）：在训练集中包含带有深度不连续性和背景区域的补丁，显著改善了边界附近像素的预测稳定性。这是因为真实扫描中物体边缘天然存在深度跳变，网络需要学习区分“特征线导致的深度不连续”与“物体边界导致的深度不连续”。

**融合视图数量**（Figure 21, Figure 22）：将融合视图数$n_v$从4增加到16，Recall从约70%提升至约90%；继续增加到32时收益递减。这表明16个均匀分布的视图已能提供足够的覆盖冗余。

**VCM先验无效**（Table 6, Table 14）：在CNN输入中添加VCM尖锐度作为额外通道并未提升性能，甚至略有下降。这与点基方法（DGCNN）形成对比——后者受益于VCM先验。原因在于CNN从深度图像中已能直接学习到足够的几何线索，额外的先验反而引入噪声。

### 下游应用：参数曲线提取

在ABC形状的参数曲线提取任务上（Table 5），DEF的Chamfer Distance仅为0.04，而PIE-NET达到0.97，精度提升一个数量级。这得益于DEF距离场的连续性和准确性：从距离场中提取特征线只需寻找局部最小值，比从稀疏分类点中拟合曲线更为可靠。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2011_15081/figures/021_Table_5.jpg]]
*Table 5: Compared to PIE-NET parametric feature curve extraction stage, DEF achieves an order of magnitude more accurate reconstruction*

### 失败模式与适用边界

1. **极尖锐特征不敏感**：特征定义依赖$18^\circ$法向角阈值，对于法向内积约等于0.95的极尖锐边缘（对应角度约$18^\circ$附近），标注可能不稳定。这限制了方法在机械零件中极细微倒角特征上的召回。

2. **平坦区域虚假信号**：基于欧氏距离的距离场标注在平坦区域可能产生微弱但非零的距离值，训练时已排除此类补丁，但可能限制了方法在无明显特征线的平滑曲面上的适用性。

3. **视图间不一致**：单视图预测在不同视角下可能存在不一致（例如某视图中特征线可见但在另一视图中被遮挡），当前最小值融合可缓解但无法完全消除，在复杂自遮挡形状上可能导致特征线断裂。

4. **参数提取的阈值敏感性**：曲线提取阶段对距离场截断阈值敏感，在特征交汇处（如三条特征线汇聚的顶点）可能产生不完整的曲线段。

5. **真实数据标注偏差**：真实扫描数据的真值依赖半自动配准（手工对齐+ICP细化），其精度受限于人工操作和配准算法，可能低估DEF在真实场景中的实际性能。

总体而言，DEF在合成和真实数据上均展现出对噪声和采样变化的显著鲁棒性，其核心优势在于将尖锐特征检测从脆弱的逐点分类转化为鲁棒的距离场回归，并通过多视图融合实现了对大规模点云的可扩展处理。

## 定位与知识库关联

DEF 的核心贡献在于将尖锐特征检测的**任务表示**从逐点二分类彻底转换为回归截断距离场 $d^\varepsilon(p)$，这是相对已有基线改变的关键 slot。现有方法（VCM, Mérigot et al., 2010；Sharpness Fields, Raina et al., 2019；EC-Net, Yu et al., 2018；PIE-NET, Wang et al., 2020）均以“点是否落在特征上”作为监督信号，导致对点样本不对齐和噪声高度敏感——点云采样稍有偏移，分类边界即失效。DEF 将问题重塑为“每个点到最近特征曲线的截断距离”，使得即使采样点未精确落在特征线上，仍能通过距离场梯度隐式定位特征位置，从根本上解耦了采样密度与检测精度的强绑定。

第二个关键 slot 变更是**输入形式**：从固定大小的全形状点云（如 DGCNN 所需的固定点数）变为局部深度图像补丁（64×64 像素）。这一变更直接解决了“无法扩展到数百万点的大规模点云”的瓶颈——基于补丁的 CNN 处理与形状整体复杂度无关，仅取决于补丁数量和分辨率。同时，将不规则点云映射到规则深度图像网格上，使得成熟的 CNN 架构（U-Net、ResNet-152）可以直接复用，无需设计复杂的点云卷积算子。

在**知识库挂载点**上，DEF 可定位于 3D 深度学习的两个交叉领域：一是**基于局部补丁的几何学习**（与 PointNet 系列的全形状处理范式形成对比），二是**隐式场回归用于几何特征检测**（与 Occupancy Networks、DeepSDF 等隐式表示方法共享“场回归”思想，但目标不同——DEF 回归的是距离特征线的场，而非表面距离场）。从方法论角度，DEF 的视图合成融合策略（warping-based view synthesis + min aggregation）借鉴了多视图立体视觉的投影几何机制，但将其用于距离场而非深度值的融合，这是一个从 MVS 到几何特征场的新颖迁移。

**适用边界**方面，DEF 存在几个明确限制：(1) 特征定义依赖 $18^\circ$ 法向角阈值，对法向内积超过 0.95 的极尖锐边缘可能不敏感，这限制了其在工业级高精度 CAD 重建中的应用；(2) 距离场标注在平坦区域可能产生虚假信号，训练时已排除此类数据，意味着该方法在缺乏尖锐特征的平滑曲面上可能退化；(3) 单视图预测在不同视角间可能存在不一致，当前通过最小值融合缓解但无法完全消除，在特征交汇复杂区域（如多棱交汇点）可能出现距离场不连续；(4) 真实扫描数据的半自动配准标注流程（手工对齐 + ICP 细化）可能引入系统性偏差，影响 sim-to-real 泛化评估的可靠性。

**后续启发**可以从以下几个方向展开：(1) 自适应法向阈值设计，使方法能处理从平滑过渡到尖锐的连续特征谱系，而非依赖固定阈值；(2) 将特征类型从内部曲线扩展到边界曲线和角点，构建统一的多类型特征场；(3) 在距离场重建中引入几何先验（非负性、分段线性、有界性）作为正则化约束，可望进一步提升精度和一致性；(4) 域自适应学习（合成→真实）可缩小 sim-to-real 差距，减少对真实标注数据的依赖；(5) 减少对融合视图数量和采样密度的依赖，使方法在低密度扫描（如手持设备）下仍保持竞争力。与 **PIE-NET**（Wang et al., 2020）的直接对比显示，DEF 的参数曲线提取阶段在 Chamfer Distance 上达到 0.04，而 PIE-NET 为 0.97，一个数量级的提升表明距离场回归范式在特征曲线矢量化下游任务中具有显著优势。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/DEF_Deep_Estimation_of_Sharp_Geometric_Features_in_3D_Shapes.pdf]]
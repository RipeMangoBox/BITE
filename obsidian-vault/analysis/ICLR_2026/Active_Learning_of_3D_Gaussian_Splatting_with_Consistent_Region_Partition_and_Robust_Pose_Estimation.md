---
title: "Active Learning of 3D Gaussian Splatting with Consistent Region Partition and Robust Pose Estimation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Active_Learning_of_3D_Gaussian_Splatting_with_Consistent_Region_Partition_and_Robust_Pose_Estimation.pdf
project_link: null
code_link: https://github.com/csrqli/al-3dgs
aliases:
- OA3RRPSV
- AL3GSCRPRPE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过分析3DGS高斯点的几何、纹理与可见性特征，将模型划分为一致性区域，并利用自监督语义特征的方差评估区域重建噪声，从而直接生成最具信息量的拍摄位姿；同时，通过相对位姿优化消除实际采集位姿偏差的影响。"
primary_logic: "利用高斯属性与可见性矩阵划分模型的一致性区域，结合自监督Point-MAE提取的语义特征方差评估区域重建质量，实现自底向上、分而治之的主动采集；该策略可直接生成下一最佳位姿，无需候选采样，且对位姿噪声具有鲁棒性。"
claims:
- "在Blender数据集10视角完美位姿设定下，本方法PSNR达25.542 dB，比FisherRF高1.9 dB"
- "移除可见性特征Γ、距离项或Point-MAE均导致PSNR/SSIM/LPIPS恶化，全模型取得最优"
- "在真实场景手持设备采集下，位姿优化将平均PSNR从21.961大幅提升至26.241"
- "在Objaverse数据集上，本方法平均PSNR比FisherRF高5.7 dB，验证了泛化性"
---

# Active Learning of 3D Gaussian Splatting with Consistent Region Partition and Robust Pose Estimation

> [!tip] 核心洞察
> 利用高斯属性与可见性矩阵划分模型的一致性区域，结合自监督Point-MAE提取的语义特征方差评估区域重建质量，实现自底向上、分而治之的主动采集；该策略可直接生成下一最佳位姿，无需候选采样，且对位姿噪声具有鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于一致性区域划分与鲁棒位姿估计的三维高斯泼溅主动学习 |
| 英文题名 | Active Learning of 3D Gaussian Splatting with Consistent Region Partition and Robust Pose Estimation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=yye5kN9jH7) · [GitHub](https://github.com/csrqli/al-3dgs) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Our Active 3DGS Reconstruction with Region Partition and Semantic Variance |
| Dataset | Blender (NeRF-Synthetic), Objaverse |

> [!tip] 效果简介
> - Blender (NeRF-Synthetic) 上，PSNR 为 25.542，对比 23.642，变化 +1.9 dB。
> - Blender (NeRF-Synthetic) 上，PSNR 为 30.186，对比 29.586，变化 +0.6 dB。
> - Objaverse 上，PSNR 为 38.321，对比 32.654，变化 +5.7 dB。

## 概要

现有辐射场主动重建方法通常需要在候选视图上评估渲染质量，这种自上而下的策略难以感知遮挡区域和语义可识别性，且普遍假设采集位姿准确，忽略真实场景中不可避免的位姿噪声，导致采集效率与重建质量受限。本文针对三维高斯泼溅（3DGS）提出一种自底向上的主动重建框架，核心思路是：分析高斯点的几何、纹理与可见性特征，将模型划分为一致性区域；再利用自监督点云编码器（Point‑MAE）通过随机Dropout生成逐点语义特征方差，以此量化区域重建噪声；最终直接从噪声区域生成下一最佳拍摄位姿，无需在候选空间采样。同时，通过相对位姿优化校正实际采集中的位姿偏差，使方法在手持有设备等真实采集条件下仍然鲁棒。实验表明，在完美位姿设定下，该方法在Blender合成数据集上10视角PSNR达25.542 dB，比当前最好的主动选择基线FisherRF提高1.9 dB；消融实验验证了可见性特征、距离项和语义方差模块的贡献；在真实手持采集场景中，位姿优化将平均PSNR从21.961 dB大幅提升至26.241 dB；在更大规模的Objaverse数据集上，方法相对FisherRF的PSNR优势扩大至5.7 dB，展现出良好泛化能力。整体而言，该方法通过"分而治之"的区域分析与语义不确定性驱动，实现了更高效的主动视图生成，并对位姿噪声具有较强的鲁棒性。



神经辐射场(NeRF)与三维高斯泼溅(3D Gaussian Splatting, 3DGS)的出现，使得从稀疏图像集合中重建高质量三维场景成为可能。然而，这些方法对输入视图的质量与覆盖范围高度敏感：若采集视角不足或关键区域遗漏，重建模型会产生显著的几何缺失与纹理退化。主动重建旨在通过迭代选择最具信息量的拍摄视角，以最小采集成本获取最优重建质量。

现有辐射场主动重建方法（如FisherRF、ActiveNeRF）普遍依赖**在候选图像上逐像素评估渲染不确定性**，通过Fisher信息或射线熵等信息增益指标指导视图选择。这类策略存在三个结构性的效率瓶颈：其一，必须从大量预定义候选图像中采样评估，计算开销随候选规模线性增长；其二，评估对象是二维渲染像素的质量，无法直接感知三维空间中遮挡区域的欠重建状态；其三，不确定性度量缺乏语义层面的可识别性，难以区分"纹理复杂需精细采样"与"语义模糊需补全重建"这两种本质上不同的信息需求。

更关键的是，现有主动重建流程**假设所采集图像的相机位姿完美精确**。在实际应用中，即使借助AR设备预览期望位姿，用户拍摄时仍不可避免地引入视角偏差与姿态噪声。这一事实层面的误差若不被显式建模与矫正，将直接注入高斯优化过程，导致重建质量的系统性塌缩——这一"从期望位姿到实际位姿"的鸿沟，是主动重建从仿真走向部署的核心障碍。

本文针对上述缺口提出了一种**"自底向上、分而治之"的主动三维高斯泼溅重建框架**。其核心思想是：不评估候选图像，而是直接对当前3DGS模型内部的高斯点进行质量分析，自底向上地生成下一最优拍摄位姿。具体而言，通过联合分析高斯点的几何位置、颜色、旋转四元数以及跨多采样相机的可见性矩阵，将模型点云划分为可视一致性区域；进而利用预训练Point-MAE编码器在蒙特卡洛Dropout下的逐点语义特征方差，评估每个区域的重建噪声水平，选定最需补全的"噪声区域"作为目标；最后，通过von Mises-Fisher分布在该区域附近直接采样生成下一组相机位姿，无需任何候选视图池。同时，框架引入相对位姿优化模块，在冻结高斯属性的前提下，仅优化新采集图像的相对位姿，使实际图像与期望视角对齐，消除采集噪声对重建的污染。

这一策略的因果有效性由多维度实验支持：在Blender数据集10视角完美位姿设定下，方法达到25.542 dB PSNR，超出FisherRF基线1.9 dB(Table 1)；当移除去可见性特征、历史距离惩罚项或Point-MAE语义方差时，所有指标均发生明显恶化，验证了每个组件的独有贡献(Table 2)；在真实手持设备采集的AR场景中，位姿优化将平均PSNR从21.961 dB大幅提升至26.241 dB(Tables 8, 9)，解耦了"位姿噪声"这一部署瓶颈的影响；在Objaverse跨物体数据集上，方法平均PSNR达38.321 dB，比FisherRF高5.7 dB(Table 10)，验证了其泛化性。需要指出的是，方法当前继承3DGS对透明/反射表面的固有弱点，且Partition与语义方差计算步各需约4秒，在交互速率上仍有优化空间。



## 核心方法与创新机理

现有辐射场主动重建方法普遍依赖在候选图像上评估渲染质量来决定拍摄视角，这一范式存在两个深层瓶颈：**①** 仅考虑可见表面的渲染不确定性，忽略被遮挡区域的潜在信息缺失；**②** 无法处理实际采集中的位姿噪声，导致真实环境下的重建质量急剧下降。本文的核心创新在于抛弃"候选评估"范式，提出一种**自底向上的主动拍摄策略**，直接从当前3DGS模型中解析出最具信息量的拍摄区域与相机位姿，并辅以鲁棒的位姿优化，在三个关键维度上实现了突破。

### 1. 从"评估候选视图"到"直接生成最佳位姿"的范式转变

以往方法（如FisherRF）需要预先采样大量候选相机位姿，再逐一评估每个位姿的信息增益（例如Fisher信息矩阵的迹或行列式），然后选择增益最大的若干位姿。这种策略不仅计算开销大，且难以保证候选集覆盖真正的信息盲区。**本文方法则通过分析高斯点的属性与可见性直接生成拍摄位姿**，无需任何候选采样（Figure 2）。具体而言：

- **一致性区域划分**：利用每个高斯点的归一化位置、颜色、旋转四元数以及从俯拍球面采样100个相机位姿得到的可见性矩阵$\Gamma$，构造特征向量$\gamma = [\mathbf{x}/r, \mathbf{c}/\sqrt{3}, R, \Gamma_m/\sqrt{N}]$（Equation 3），通过K‑Means聚类将模型划分为在几何、纹理与可见性上一致的区域。这种可见性驱动的分区首次显式发现了遮挡面（Figure 3），使采集策略能主动瞄准需要更多观测的欠重建区域。
- **噪声区域确定**：对每个区域，从当前高斯模型重建表面点云，利用预训练的Point‑MAE编码器做$T=10$次随机Dropout前传，计算每点的语义特征方差$S_{\text{sem}}$（Equation 4），其范数量化了该点的重建噪声水平。区域的综合得分$S_{\text{total}}^j$还结合了与历史采集位姿的距离（Equation 5），从而实现"下一最佳视图"的区域选择：优先覆盖语义方差高且从未被观测到的区域。
- **视图采样**：对于选中的高噪声区域，以区域中心为起点，沿法线方向与包围球相交确定相机位置，并从von Mises‑Fisher分布采样朝向，直接生成此次采集的$l$个相机位姿（Algorithm 1）。这一过程完全由模型自身驱动，避免了任何候选图像渲染。

### 2. 基于点云语义方差的不确定性度量

传统主动NeRF/3DGS方法的不确定性估计基于渲染图像的逐像素量（如Fisher信息、射线熵或颜色方差），这些度量仅反映已观测像素的可信度，无法评估不可见区域的缺失信息。本文提出**一种基于点云语义特征方差的不确定性度量**：将当前高斯模型的表面抽取为点云，通过Point‑MAE预训练模型提取逐点的深层语义特征，并利用Monte Carlo Dropout在前向传播中引入随机性，计算多次推理的方差。该方差与区域重建质量高度相关——方差大的点通常位于几何细节未充分恢复、纹理复杂或被遮挡的区域。相比渲染层面的不确定性，语义层面的方差具有更强的跨视角一致性和对不可见区域的辨别力。消融实验表明，移除语义方差度量后，PSNR、SSIM和LPIPS全面恶化（Table 2）。

### 3. 鲁棒位姿优化：消除实际采集的位姿噪声

多数主动重建工作假设采集位姿是完美的，但这在手持设备或AR应用场景中不成立。本文引入**相对位姿优化模块**（Section 3.3）：在获取新图像后，冻结所有3DGS属性（高斯均值、协方差、颜色、不透明度），仅优化该图像的相对位姿$\mathbf{T}$，最小化基于梯度重投影损失$\mathcal{L}_{\text{pose}}$（Equation 6）。由于3DGS模型本身在此步骤不更新，优化只纠正采集位姿的微小漂移，不会破坏已学到的几何结构。实验表明，在真实场景的手持设备采集下，开启位姿优化后平均PSNR从21.961 dB大幅提升至26.241 dB（Tables 8–9），定性结果也显示出对细微结构的明显恢复（Figure 5）。

### 创新有效性验证

上述三个核心创新点的组合在多个基准上形成了显著增益：
- **Blender数据集10视图完美位姿**：PSNR达25.542 dB，比竞争对手FisherRF高出1.9 dB（Table 1）。
- **Objaverse数据集20视图**：平均PSNR 38.321 dB，领先FisherRF 5.7 dB，表明方法对不同形状物体的泛化性（Table 10）。
- **组件消融**：移除可见性特征$\Gamma$、历史距离项或语义方差计算，均导致各项指标一致下降，全模型达到最优（Table 2）。
- **超参数稳定性**：聚类数5、语义特征采样数10等默认配置在效率与性能间取得最佳平衡（Tables 3–5）。

综上，本文的核心创新在于构建了一套从"模型分区感知"到"不确定性量化"再到"位姿生成与优化"的完整闭环，使3DGS的主动重建首次具备了面向真实采集的实用性和高效性。



![[assets/figures/papers/iclr26_0006_yye5kN9jH7_Active_Learning_of_3D_Gaussian_Splatting_with_Co/figures/002_Figure_2.jpg]]
*Figure 2: The above figure shows the pipeline of our active reconstruction algorithm. The next best pose estimation contains consistent region partitioning, noisy region determination and view sampling stages. The 3DGS model training, next pose estimation and guided image acquisition are performed iteratively*

本文提出的主动三维高斯泼溅（3DGS）重建系统遵循一个**迭代式自底向上的采集与优化闭环**。其核心目标是从当前不完整的3DGS模型中直接推断出最具信息量的拍摄位姿，而非依赖候选图像的渲染质量评估。整个框架由两个相互交织的回路构成：（1）**下一最佳位姿估计**流水线，根据模型现状生成信息采集建议；（2）**3DGS训练与位姿优化**回路，利用新采图像更新模型并校正真实采集中的位姿误差。图2以框图形式概括了这一流程。

**输入输出流与闭环迭代**。每一轮迭代的输入是当前已训练的3DGS模型 $\mathcal{G}^k$（由一组高斯点及其属性组成），输出则是一组下一最佳相机位姿 $\{\mathbf{P}_k^1,\dots,\mathbf{P}_k^l\}$（公式2）。系统初始化时用均匀采样的3张图像训练初始模型；随后在每一轮中，首先通过位姿估计流水线生成推荐的拍摄方向，在合成数据中直接渲染对应视图，或在真实设备上引导用户采集实际图像；当应用于手持设备等含噪声的采集环境时，增加一个**鲁棒位姿优化**步骤——冻结高斯属性，通过最小化重投影损失将期望位姿校正到真实位姿（公式6）。新采图像加入训练集后，继续训练3DGS模型，形成"模型评估→位姿推荐→采集校正→模型更新"的闭环，直至达到预设视点数或重建质量收敛。

**下一最佳位姿估计流水线**由三个核心模块串联而成，所有操作均建立在当前3DGS模型之上，无需任何候选图像池：

1. **一致性区域划分**。为每个高斯点构造特征向量 $\gamma$，融合归一化位置、颜色、旋转四元数以及关键性的**可见性矩阵行**（公式3）。可见性矩阵通过大量包围球采样相机并记录各高斯点的可见性获得，从而将遮挡关系显式编码为高维特征。对特征进行K‑Means聚类，将3DGS模型拆分为若干**可视一致性区域**，每个区域对应一个位置连续、颜色相近且对一定视角区间共同可见的局部表面（§3.2.1）。这一步将"分而治之"的策略形式化，后续可以独立评估不同表面区域的重建质量。

2. **噪声区域确定**。对聚类后的每个区域，使用预训练的Point‑MAE编码器提取其底层点云的自监督语义特征，并通过MC Dropout（多次随机丢弃）计算逐点特征的方差，得到**语义方差得分** $S_{\mathrm{sem}}$（公式4）。方差越大的点，其语义特征越不稳定，可视为重建噪声较大的区域。将区域内点的语义方差平均值与区域到历史拍摄位姿的距离加权组合，得到每个区域的**总体噪声得分** $S_{\mathrm{total}}^j$（公式5），选择得分最高的区域作为当前最需探索的"欠重建区"（§3.2.2）。这种不确定性度量不再依赖于新视角的渲染图像，而是直接定位模型内部的高熵表面。

3. **视图采样**。在选定的噪声区域中心，沿表面法线向外延伸并与包围球相交，以此交点为中心，从von Mises‑Fisher分布采样一系列相机方向，生成一组信息采集位姿（§3.2.3）。采样数量由区域的空间范围以及当前采集阶段自适应确定，确保每次采集既能有效覆盖欠重建区，又避免冗余视图。该过程完全从模型内部几何与语义噪声出发，第一次在主动3DGS重建中实现了**无需候选采样**的直接位姿生成。

流水线的整体设计将"一致性分区—语义噪声评估—自适应点位生成"嵌入到主动重建的迭代循环中。其因果机制可以概括为：通过可见性与几何‑纹理特征解耦出相互独立的表面块，再利用自监督深度特征的随机扰动量化每块的重建不确定性，最终驱动相机直接瞄准模型最需要补充信息的区域。该流水线同时具备对真实采集**位姿噪声的鲁棒性**，因为位姿优化回路能够在固定模型的情况下单独修正采集视点的外参，从而将下游任务的误差隔离在采集端。



该方法围绕"自底向上、分而治之"的主动采集策略，通过四个关键模块将当前 3DGS 模型转化为一组最能提升重建质量的相机位姿，并在实际采集时利用位姿优化抵抗噪声。整体采集函数定义为

$$\{\mathbf{P}_k^1, \mathbf{P}_k^2, \ldots, \mathbf{P}_k^l\} = A(\mathcal{G}^k),$$

其中 $\mathcal{G}^k$ 是第 $k$ 步的 3DGS 模型，输出为下一组最佳相机位姿（公式 (2)）。以下逐一展开四个核心模块及其中嵌入的关键公式。

### 1. 一致性区域划分（Consistent Region Partitioning）

该模块将高斯点划分为可视一致性区域，使得同一区域内的点具有相似的几何、纹理和可见性特性，为后续局部覆盖提供基础。

**高斯特征向量构建。** 对每个高斯点，构造特征向量 $\gamma_i$（公式 (3)）：

$$\gamma_i = \left[ \frac{\mathbf{x}_i}{r}, \frac{\mathbf{c}_i}{\sqrt{3}}, \mathbf{R}_i, \frac{\mathbf{\Gamma}_i}{\sqrt{N}} \right].$$

其中：
- $\mathbf{x}_i/r$：经场景包围球半径 $r$ 归一化的空间位置。
- $\mathbf{c}_i/\sqrt{3}$：归一化颜色，分母使得各分量方差量级相近。
- $\mathbf{R}_i$：高斯旋转四元数，携带局部朝向信息。
- $\mathbf{\Gamma}_i/\sqrt{N}$：高斯的可见性行向量（维度 $N$），归因于相机采样数 $N$。该向量通过采样 $M$ 个高斯点、利用 Alpha Shape 重建表面并进行遮挡检测得到，捕捉了点在预定义相机集合下的可见模式，使聚类能区分不可见面（例如被遮挡区域）（Algorithm 1，行 18）。

**聚类。** 使用 K‑Means 对所有高斯的 $\gamma$ 进行聚类，得到 $K$ 个一致性区域（默认 $K=5$，该值在消融实验中取得最优 PSNR/SSIM/LPIPS，Table 3）。聚类过程不依赖渲染图像，因此天然避免了对候选视角的枚举。

### 2. 噪声区域确定（Noisy Region Determination）

为从分割出的区域中选择重建最不充分的一个，定义基于自监督语义特征方差的噪声度量。

**逐点语义方差。** 首先对当前 3DGS 模型进行 Alpha Shape 表面重建，提取顶点作为点云。使用预训练的 Point‑MAE 编码器（12 层 Transformer，输出 512 维特征）对点云进行 $T$ 次随机 Dropout 前向传播（默认 $T=10$，每次随机采样 $90\%$ 的点作为输入，模型参数 Dropout 率 $0.8$）。记第 $t$ 次前向得到的逐点特征为 $f_t(\mathbf{x}_j)$，则高斯点 $\mathbf{x}_j$ 的语义方差评分定义为

$$S_{\mathrm{sem}}(\mathbf{x}_j) = \big\| \mathrm{var}_t\, f_t(\mathbf{x}_j) \big\| \quad \text{(公式 (4)，对应 Algorithm 1 行 26)}，$$

即 $T$ 次特征向量在各维度上取方差后再计算其范数。方差越大表明模型对该点的语义表达越不稳定，即重建噪声越大。

**区域综合评分。** 对每个一致性区域 $R_j$，计算其平均语义方差，并综合历史采集距离以避免重复拍摄：

$$S_{\mathrm{total}}^j = \lambda_1 \cdot \frac{1}{|R_j|} \sum_{\mathbf{x} \in R_j} S_{\mathrm{sem}}(\mathbf{x}) + \lambda_2 \cdot \mathrm{dist}(R_j, \text{history}) \quad \text{(公式 (5)，Algorithm 1 行 28)}.$$

其中 $\lambda_1$、$\lambda_2$ 为平衡系数，$\mathrm{dist}(R_j, \text{history})$ 衡量区域中心与已拍摄相机位姿的距离。得分最高的区域被选为当前步骤的噪声区域进行覆盖。

### 3. 视图采样（View Pose Sampling）

针对选定的噪声区域，算法沿该区域中心的表面法线方向向外发射射线，与包围球相交得到参考点，并在以该点为中心的 von Mises‑Fisher 分布上采样相机位姿。采样方向集中在朝向该区域，且每次采集的视图数量根据区域大小自适应确定（Section 3.2.3，Algorithm 1）。这一设计直接从模型内部生成最具信息量的位姿，无需对候选图像进行费时的渲染增益评估，是其区别于 FisherRF 等基线方法的关键机制。

### 4. 鲁棒位姿优化（Robust Pose Optimization）

实际采集（如手持设备拍摄）中获得的图像通常带有位姿偏差。为消除这一偏差，该模块固定已优化好的高斯属性，仅对新采集图像的相对位姿进行微调，目标是最小化重投影损失：

$$\mathbf{T}^* = \arg\min_{\mathbf{T}} \mathcal{L}_{\mathrm{pose}}(\mathbf{T}\mathbf{P}, \mathbf{P}) \quad \text{(公式 (6))。}$$

这里 $\mathbf{T}$ 为需要优化的相对位姿变换，$\mathbf{P}$ 为根据期望位姿生成的渲染结果，$\mathcal{L}_{\mathrm{pose}}$ 为基于重投影误差的损失。通过冻结高斯参数，位姿优化只对齐图像与当前重建，有效避免位姿噪声传导至模型参数，使重建在真实环境中仍能保持高质量。

以上模块共同实现了从 3DGS 模型直接生成下一最佳位姿的主动重建流程。消融实验表明，移除可见性特征 $\mathbf{\Gamma}$、距离项或 Point‑MAE 语义方差均会导致 PSNR/SSIM/LPIPS 明显下降（Table 2），验证了各组件的重要性。



## 实验与关键发现

### 主结果
在合成场景（Blender/NeRF‑Synthetic）和真实手持采集两种设定下，我们系统比较了所提方法与 FisherRF、随机采样 (Random)、最远距离采样 (Furthest) 以及基于 NeRF 的主动重建方法（NeurAR、ActiveNeRF）。所有主动策略均从 3 张初始图像出发，训练步数与超参数保持一致（fairness notes）。

**完美位姿下的渲染质量。** 在 10 视角设定下，本方法取得 25.542 dB 的 PSNR，比 FisherRF 高出 1.9 dB，LPIPS 降至 0.063（Table 1）。增加至 20 视角后，PSNR 提升至 30.186 dB，仍领先 FisherRF 0.6 dB，SSIM 达 0.943（Table 1 & Table 7）。逐场景分析（Table 6 & Table 7）表明，优势在遮挡较多、几何细节丰富的场景（如 drums、lego）中更为显著，原因是本文的区域划分能准确隔离不可见面并定向采集。

![[assets/figures/papers/iclr26_0006_yye5kN9jH7_Active_Learning_of_3D_Gaussian_Splatting_with_Co/figures/005_Table_1.jpg]]
*Table 1: The quality of rendered images using active reconstruction under perfect pose*

**真实手持采集中的鲁棒性。** 实际部署中直接将期望位姿用于采集会导致显著退化：ARP（无位姿优化）的平均 PSNR 跌至 21.961 dB，SSIM 仅 0.831（Table 9）。引入相对位姿优化后，平均值大幅回升至 26.241 dB PSNR、0.909 SSIM（Table 8）。定性对比（Figure 5）显示，位姿优化成功恢复了 phoenix 翅膀等原本完全丢失的细节，表明本方法对消费级传感器位姿噪声具有强鲁棒性。

![[assets/figures/papers/iclr26_0006_yye5kN9jH7_Active_Learning_of_3D_Gaussian_Splatting_with_Co/figures/013_Table_8.jpg]]
*Table 8: The per-scene quantitative results of AR-based active reconstruction with pose optimization*

![[assets/figures/papers/iclr26_0006_yye5kN9jH7_Active_Learning_of_3D_Gaussian_Splatting_with_Co/figures/014_Table_9.jpg]]
*Table 9: The per-scene quantitative results of AR-based active reconstruction without pose optimization*

**跨数据集泛化。** 在更大规模的 Objaverse 数据集上，本方法在 20 视角下取得 38.321 dB PSNR，较 FisherRF 提升超过 5.7 dB（Table 10），验证了"分而治之"的区域驱动策略在不同物体类别上均可提供稳定增益。

![[assets/figures/papers/iclr26_0006_yye5kN9jH7_Active_Learning_of_3D_Gaussian_Splatting_with_Co/figures/015_Table_10.jpg]]
*Table 10: The per-scene quantitative results on the Objaverse dataset*

### 消融实验
核心组件消融（Table 2）说明，移除可见性特征 Γ、距离权重或 Point‑MAE 语义方差，均会导致 PSNR/SSIM 下降及 LPIPS 恶化，证实三者协同作用支撑了高效的下一最佳位姿估计。仅使用几何距离或单维不确定性的消融变体性能明显弱于全模型，表明可见性约束（Γ）与自监督语义评判缺一不可。

![[assets/figures/papers/iclr26_0006_yye5kN9jH7_Active_Learning_of_3D_Gaussian_Splatting_with_Co/figures/007_Table_2.jpg]]
*Table 2: Ablation study results of our method*

超参数敏感性分析（Table 3–5）给出以下结论：
- 聚类数设为 5 时最佳（PSNR 25.542），过少（3）无法区分遮挡区域，过多（7）则引入冗余划分；
- 语义特征方差采样数 T=10 在效率与性能间取得平衡，T=15 仅有微弱提升（PSNR +0.43 dB，Table 4）；
- 可见性矩阵采样相机数 N=100 已足够稳定，N 增至 200 仅微幅优化 LPIPS（Table 5）。

### 失败模式与局限性
本方法继承 3DGS 的固有问题，对透明、强反射表面重建质量不稳定，且要求采集图像清晰、实际位姿需位于估计位姿的邻域，否则位姿优化可能失效。当前设计聚焦单物体场景，固定使用的 Point‑MAE 编码器可能限制在杂乱场景或开放环境中的适应性。每步运行时消耗（区域划分约 4.13 s，语义方差计算约 3.7 s）在实时交互场景下仍需压缩，但考虑到主动重建是离线‑在线迭代过程，当前成本可接受。



## 定位与知识库关联

本工作在主动三维重建领域明确了一条与以往基于渲染图像质量评估完全不同的路径。现有辐射场主动重建方法（如 FisherRF[1] 和 ActiveNeRF/NeurAR[2]）通过在一组候选视图上计算渲染不确定性（逐像素 Fisher 信息、射线熵等）来选择下一最佳视角，但这一范式忽视了两个关键因素：**遮挡区域的可见性差异**和**几何-语义层面的可重建性**，且默认采集位姿完全准确，难以直接迁移到真实手持拍摄场景。本文提出的方法从 3D 高斯泼溅（3DGS）的内部表征出发，**将模型划分为可视一致性区域**，并用自监督语义特征的方差**直接量化区域重建噪声**，由此生成下一组相机位姿而无需候选采样，从根本上改变了"评估‑选择"的流水线。这一差异体现在 Table 1 和 Table 10 中：在 Blender 合成数据集 10 视角设定下，本方法 PSNR 达 25.542 dB，比 FisherRF 高出 1.9 dB；在更具多样性的 Objaverse 数据集上优势进一步拉大至 5.7 dB（平均 PSNR）。消融实验（Table 2）进一步证实，移除可见性特征 Γ、历史距离项或 Point‑MAE 均导致所有指标恶化，说明"分而治之"的区域划分与语义方差度量共同构成了性能提升的核心。

与以 NeRF 为骨架的主动方法（ActiveNeRF/NeurAR）的根本区别在于：本方法直接利用 3DGS 高斯点的几何、纹理和可见性属性进行**自底向上的区域划分**，而无需依赖视点采样后逐像素评估，因此能够更高效地发现被遮挡或尚未充分重建的区域（见图 4）。另一方面，针对真实采集不可避免的位姿偏差，本文引入**相对位姿优化**（冻结 3DGS 属性，仅用重投影损失优化新图像的相对位姿），将实际 AR 采集的平均 PSNR 从 21.961 dB 提升至 26.241 dB（Tables 8 & 9），这是现有主动重建基线完全未覆盖的环节。

**适用边界**方面，本方法继承 3DGS 对透明/强反射表面建模能力较弱的特点，因此在含有大量镜面或半透明物体的场景中表现可能受限。另要求所采集图像具有足够清晰度，实际相机位姿不能与期望位姿偏差过大（大尺度初始漂移时位姿优化可能失效），且当前设计针对**单物体场景**，未显式融入场景级语义分割或多物体推理。

**局限**明确落在以下几点：(a) 区域划分和语义方差计算开销较大（分别约 4.13 s 和 3.7 s），难以实时运行；(b) 语义编码器固定为 Point‑MAE，面对开放世界的多类别物体时泛化性可能不足；(c) 未处理运动模糊等问题。

**开放问题**包括：(1) 扩展到场景级重建，需结合语义分割与多物体一致性推理；(2) 用基于学习的位姿估计器（如 DUSt3R）替代当前的相对位姿优化，以应对更大范围的初始位姿漂移；(3) 引入类别感知或任务感知的视图选择策略，利用其他点云理解网络提升下游适应性和重建语义质量。这些方向将推动主动 3DGS 重建从单物体演示走向可部署的真实世界应用。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Active_Learning_of_3D_Gaussian_Splatting_with_Consistent_Region_Partition_and_Robust_Pose_Estimation.pdf

![[paperPDFs/ICLR_2026/Active_Learning_of_3D_Gaussian_Splatting_with_Consistent_Region_Partition_and_Robust_Pose_Estimation.pdf]]

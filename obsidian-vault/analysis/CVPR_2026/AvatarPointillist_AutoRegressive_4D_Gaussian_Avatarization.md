---
title: "AvatarPointillist: AutoRegressive 4D Gaussian Avatarization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AvatarPointillist_AutoRegressive_4D_Gaussian_Avatarization.pdf
project_link: "https://kumapowerliu.github.io/AvatarPointillist"
code_link: null
aliases:
- AvatarPointillist
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将点云生成建模为自回归序列任务，直接学习生成高斯点的分布，从而摆脱固定模板的约束，实现对高斯点空间分布和总数的自适应调整。
primary_logic: 把4D高斯化身的一次性生成转化为自回归点云序列建模，使模型能像高斯溅射本身那样灵活地决定点的位置和数量——在几何复杂的区域增加点密度，在平滑区域减少点数，从根源上发挥3DGS的表示能力。
claims:
- 固定模板点云造成细节丢失：LAM基于FLAME模板的方法无法重建马尾辫等精细结构，而自回归生成能够自适应地放置点。
- 自回归逐点生成范式使模型动态调整高斯分布：根据主体复杂度自适应控制点数与空间分布。
- 将AR隐状态特征与位置编码共同输入高斯解码器，显著提升渲染质量，是性能的关键设计。
- NeRSemble (self-reenactment) 上 LPIPS↓ = 0.15
---

# AvatarPointillist: AutoRegressive 4D Gaussian Avatarization

> [!tip] 核心洞察
> 把4D高斯化身的一次性生成转化为自回归点云序列建模，使模型能像高斯溅射本身那样灵活地决定点的位置和数量——在几何复杂的区域增加点密度，在平滑区域减少点数，从根源上发挥3DGS的表示能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | AvatarPointillist：自回归4D高斯化身生成 |
| 英文题名 | AvatarPointillist: AutoRegressive 4D Gaussian Avatarization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04787) · [Project](https://kumapowerliu.github.io/AvatarPointillist) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AvatarPointillist |
| Dataset | NeRSemble |

> [!tip] 效果简介
> - NeRSemble (self-reenactment) 上，LPIPS↓ 0.15 vs N/A (N/A)；FID↓ 95.18 vs N/A (N/A)；AKD↓ 2.38 vs N/A (N/A)。
> - NeRSemble (cross-reenactment) 上，FID↓ 160.74 vs N/A (N/A)；CLIP↑ 0.75 vs N/A (N/A)；AKD↓ 5.93 vs N/A (N/A)。

## 概要

从单张肖像图像重建可驱动的4D数字化身是计算机视觉中的一项核心挑战。现有方法多依赖固定的点云模板（如FLAME顶点）来初始化3D高斯溅射（3DGS）的几何结构，这从根本上限制了模型对个体几何复杂性的适应能力——精细细节（如胡须、发型、马尾辫）往往因模板约束而丢失。

**AvatarPointillist** 提出了一种全新的范式：将4D高斯化身的生成建模为**自回归点云序列任务**。其核心思路是，让一个仅解码器的Transformer像生成语言记号那样逐点生成高斯点云——每个点由量化后的空间坐标与绑定索引构成。这一“逐点生成”的策略使模型能够像高斯溅射本身那样灵活地决定点的位置和数量：在几何复杂的区域自适应地增加点密度，在平滑区域减少点数，从根本上释放3DGS的表示能力。

在方法谱系中，AvatarPointillist位于单图3DGS化身生成的前沿，直接对比的基线包括基于固定FLAME模板的**LAM**（Zheng et al.）和采用三平面表示的**GAGAvatar**（Chu et al.）。与LAM的“模板+偏移”策略不同，AvatarPointillist从零学习点云分布；与GAGAvatar的隐式几何不同，AvatarPointillist通过自回归显式生成点云几何，再经由一个Transformer高斯解码器预测完整的外观属性（颜色、不透明度、缩放、旋转等），最后利用预测的绑定信息通过线性混合蒙皮（LBS）和矫正混合形状驱动动画。

实验表明，该方法在NeRSemble数据集的自驱动与交叉驱动任务上取得了领先的定量结果，并在表情一致性、姿态一致性和身份保留方面展现出显著的定性优势。消融实验进一步证实，将自回归隐状态特征与点位置编码共同输入高斯解码器是性能的关键设计，而仅使用FLAME模板位置则会导致严重质量退化，印证了固定模板的局限性。



### 单图化身生成的需求与挑战

从单张肖像图像重建可驱动的动态3D头像，在虚拟现实、远程呈现和数字人应用中具有广泛前景。该任务的核心要求是：在仅给定一张输入图像的前提下，生成一个身份一致、几何精确且可实时驱动表情与姿态的化身。近年来，3D高斯溅射（3D Gaussian Splatting, 3DGS）凭借其显式点云表示和高效可微渲染能力，成为该方向的主流技术路线。

然而，现有基于3DGS的单图化身方法在几何建模灵活性上存在一个根本性瓶颈：它们普遍依赖固定的点云模板来定义高斯的初始位置。

### 固定模板范式的局限性

以 **LAM** 为代表的现有方法，将高斯点云构建于FLAME参数化头部模型的顶点之上。这意味着所有化身——无论其输入图像中的主体具有怎样的几何特征——都使用相同数量和空间分布的高斯点。模型仅能学习预测每个顶点上的微小偏移量，而无法从根本上改变点的分布格局。

这种“模板+偏移”的策略带来了两个直接后果：

1. **细节丢失**：对于几何结构超出模板表达能力的区域，模型无能为力。如 Figure 2 所示，LAM无法重建马尾辫等精细结构——因为FLAME模板中根本没有对应这些细节的顶点。
2. **资源错配**：所有主体使用相同数量的高斯点，无法根据实际几何复杂度进行自适应分配。在平滑区域浪费计算资源，在复杂区域又缺乏足够的表示能力。

更本质地说，3DGS的核心优势恰恰在于其点云表示的灵活性——可以在几何复杂区域放置更多点，在平坦区域使用更少的点。固定模板范式恰恰扼杀了这一优势，使得3DGS的表示能力无法得到充分发挥。

### 自回归生成范式的动机

本文提出的 **AvatarPointillist** 旨在从根本上解决上述问题。其核心洞察是：将4D高斯化身的点云生成建模为自回归序列任务，使模型能够像高斯溅射本身那样灵活地决定点的位置和数量。

具体而言，AvatarPointillist 用一个解码器仅结构的Transformer直接自回归生成完整的高斯点云序列（包含坐标和绑定信息），完全摆脱了固定模板的约束。这一“逐点生成”范式带来了三个关键突破：

- **自适应点密度**：模型根据输入图像中主体的几何复杂度，自主决定在何处放置多少高斯点——在胡须、发型等精细区域自动增加点密度，在平滑区域减少点数。
- **端到端学习**：不再需要手工设计的模板初始化和偏移预测流程，模型从数据中直接学习点云分布。
- **身份感知生成**：自回归过程通过交叉注意力机制注入DINOv2提取的图像特征，使生成的点云能够忠实反映输入主体的身份特征。

如 Figure 1 所示，AvatarPointillist 的自回归模型能够模拟高斯溅射的自适应点调整能力，生成精确的几何结构（如头发和浓密胡须），这是固定模板方法无法实现的。



## 核心方法与创新机理

AvatarPointillist 的核心创新在于从根本上改变了 3DGS 化身的点云生成范式：将原本**依赖固定模板的回归问题重新建模为自回归序列生成任务**。这一范式转换带来了三个层面的关键突破。

### 从模板约束到自适应点云生成

现有单图 3DGS 化身方法（如 **LAM** ）普遍依赖 FLAME 顶点作为固定的点云模板，再通过预测偏移量来变形模板。这种设计的根本局限在于：所有对象——无论几何复杂度如何——都被强制使用相同数量的高斯点，导致精细结构（如马尾辫、胡须）无法被充分表示。Figure 2 的对比直观地展示了这一瓶颈：LAM 无法重建马尾辫等细节，而 AvatarPointillist 的自回归生成能够自适应地在几何复杂区域放置更多点、在平滑区域减少点数。

AvatarPointillist 通过将点云序列化为离散记号序列：

$$P = ( x_1, y_1, z_1, b_1, \ldots, x_N, y_N, z_N, b_N )$$

并利用自回归分解：

$$p(T) = \prod_{n=1}^{4N} p(T_n \mid T_{<n})$$

使模型能够逐点决定高斯的位置和绑定信息。这一设计让模型真正“像高斯溅射本身那样”灵活地调整点的空间分布和总数，从根源上释放了 3DGS 的表示能力。

### 隐状态特征与位置编码的协同解码

将点云生成建模为自回归任务后，一个关键设计是将 AR Transformer 的隐状态特征 $F_n^p$ 与去量化后的位置编码 $P_n$ 拼接，共同输入高斯解码器。消融实验（Table 2）表明，仅使用 $P_n$（类似 LAM 的模板思路）或仅使用 $F_n^p$ 都会造成渲染质量显著下降；二者协同使用才能获得最佳 LPIPS 和 FID。Figure 5 的可视化进一步证实：$F_n^p$ 提供深层语义线索，$P_n$ 提供显式空间引导，二者的互补是解码器性能的关键。

### 端到端的自回归 4D 化身生成

整个框架将 4D 化身的一次性生成分解为两个阶段：AR Transformer 负责几何生成（坐标与绑定信息），高斯解码器负责外观属性预测。绑定信息通过重心坐标插值从 FLAME 顶点继承蒙皮权重和混合形状：

$$\hat{\mathbf{w}}_i = b_0 \mathbf{W}_0 + b_1 \mathbf{W}_1 + b_2 \mathbf{W}_2$$

$$\hat{\mathbf{S}}_i = b_0 \mathbf{S}_0 + b_1 \mathbf{S}_1 + b_2 \mathbf{S}_2$$

这使得生成的高斯点云可以直接通过 LBS 和 corrective blendshapes 驱动，无需额外的动画适配网络。与 **GAGAvatar** 等依赖辅助网络细化的三平面方法相比，AvatarPointillist 的显式点云生成在视角一致性和身份保留上具有天然优势（Figure 4）。



AvatarPointillist 提出了一种从单张肖像图像直接生成可驱动 4D 高斯化身的全新范式。其核心思想是将高斯点云的生成建模为自回归序列任务，从而摆脱传统方法对固定点云模板的依赖，使模型能够根据输入主体的几何复杂度自适应地调整高斯点的空间分布与总数。

### 两阶段流水线

整个框架由两个核心模块构成，形成“几何生成—属性预测”的两阶段流水线，如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2442_https_arxiv_org_abs_2604_04787/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our framework. It consists of two modules: an autoregressive (AR) model for Gaussian geometry generation and a Gaussian Decoder for predicting rendering attributes. The AR model takes image features from DINOv2 [50] and point cloud features as input. The point cloud feature extract via Pixel3DMM [15] and a point cloud encoder [85]. The AR model is trained to generate a Gaussian point cloud via next-token prediction, where each point is represented by four quantized tokens*

**第一阶段：自回归几何生成。** 给定单张输入图像，系统首先通过 **DINOv2** 特征提取器获取 2D 视觉特征，同时利用外部的 3D 人脸重建模型（Pixel3DMM）估计 FLAME 参数，再通过点云编码器提取 FLAME 顶点的结构特征作为 3D 先验。这两类特征通过交叉注意力机制注入一个解码器仅结构的 Transformer。该 Transformer 以自回归方式逐记号地生成量化后的点云序列，每个高斯点由四个离散记号表示：三个空间坐标 $(x, y, z)$ 和一个绑定索引 $b$，后者将生成的点关联到 FLAME 拓扑的特定三角面片，为后续动画驱动提供结构锚定。

**第二阶段：高斯属性解码。** 自回归生成的记号经反量化恢复为连续坐标后，系统为每个点构造两类互补特征：基于坐标的位置编码 $P_n$ 和 AR Transformer 最终层的隐状态特征 $F_n^p$。二者拼接后送入一个基于 Transformer 的高斯解码器，预测完整的渲染属性——包括颜色、不透明度、缩放、旋转和相对于 FLAME 模板的偏移量。关键设计在于，$F_n^p$ 携带了自回归生成过程中积累的深层语义线索，而 $P_n$ 提供显式的空间引导，二者的协同作用被消融实验证实为渲染质量的决定性因素。

### 动画驱动

生成的规范空间高斯点云通过线性混合蒙皮和矫正混合形变实现表情与姿态驱动。AR 模型预测的绑定索引 $b$ 通过重心坐标插值，将 FLAME 顶点的蒙皮权重和混合形变参数迁移到每个生成的高斯点上，使得化身能够直接响应 FLAME 的表情与姿态参数，完成从静态点云到动态 4D 化身的转换。

### 训练策略

训练分为两个解耦阶段：首先以标准交叉熵损失训练 AR Transformer，使其学会准确预测量化点云序列的下一个记号；随后冻结 AR 模型，以 $L_1$、SSIM、LPIPS 和正则化项的加权组合优化高斯解码器，权重经验设定为 $1$、$0.5$、$0.1$、$0.1$。这种分阶段训练策略避免了端到端优化的不稳定性，同时确保几何生成和外观建模各自收敛到较优解。

### 与基线方法的根本差异

Figure 2 直观展示了本文方法与基于固定模板的方法（如 **LAM**）的本质区别。LAM 以 FLAME 顶点作为高斯点云的初始化模板，仅通过预测偏移来变形模板——这导致其无法在模板覆盖不到的区域（如马尾辫、浓密胡须）生成足够的高斯点，造成精细几何结构的丢失。AvatarPointillist 则通过自回归生成从零开始构建点云，模型自主决定在几何复杂区域增加点密度、在平滑区域减少点数，从根本上释放了 3DGS 的表示潜力。



### 3DGS 预备知识：局部到全局的变换

在介绍核心模块之前，有必要建立 3D 高斯溅射（3DGS）在化身动画中的基本变换关系。为将规范空间的高斯属性驱动至目标表情/姿态，系统需要将局部定义的旋转 $r$、位置 $\mu$ 和缩放 $s$ 根据所属 FLAME 面片的变换矩阵转换到全局空间。该变换形式为：

$$r' = R r, \quad \mu' = k R \mu + T, \quad s' = k s$$

其中 $R$ 为面片的旋转矩阵，$T$ 为平移向量，$k$ 为缩放因子。这一变换构成了后续动画驱动模块的数学基础，确保了规范空间生成的几何能够随面部参数灵活变形。

### 点云序列化与量化：将几何转化为离散记号

AvatarPointillist 的核心创新在于将 4D 高斯化身的生成问题转化为自回归序列建模问题。首先，规范空间中的高斯点云被组织为一个有序序列：

$$P = ( x_1, y_1, z_1, b_1, \ldots, x_N, y_N, z_N, b_N )$$

其中 $(x_n, y_n, z_n)$ 为第 $n$ 个高斯点在规范空间的全局坐标，$b_n$ 为其绑定的 FLAME 面片索引。这一序列化操作将无序点云转化为具有明确生成顺序的一维结构。

为使自回归 Transformer 能够处理连续坐标，系统对每个坐标分量进行均匀量化，并附加绑定索引，形成离散记号序列：

$$T = ( T_1^x, T_1^y, T_1^z, T_1^b, \ldots, T_N^x, T_N^y, T_N^z, T_N^b )$$

每个高斯点对应四个离散记号，序列总长度为 $4N$。自回归模型将整个点云序列的联合概率分解为条件概率的乘积：

$$p(T) = \prod_{n=1}^{4N} p(T_n \mid T_{<n})$$

模型通过最大化该似然进行训练，逐步预测下一个记号，从而在推理时逐点生成完整的高斯点云。

### 自回归 Transformer：几何生成的核心引擎

自回归模型的主体为仅解码器（decoder-only）结构的 Transformer（见 Figure 3 框架总览）。其每一层包含交叉注意力层、自注意力层和前馈网络。模型接收两类条件输入以实现身份感知的几何生成：

- **2D 视觉特征**：使用 DINOv2 直接从输入肖像图像提取特征，通过交叉注意力注入 Transformer 各层，提供外观与身份信息。
- **3D 结构先验**：通过 Pixel3DMM 估计 FLAME 参数，再利用点云编码器提取 FLAME 顶点的几何特征，为生成过程提供粗糙的三维结构引导。

Transformer 逐记号生成序列 $T$ 后，经过去量化恢复实际的连续坐标值。同时，模型最终层的隐藏状态被保留为每个点对应的隐状态序列：

$$F = ( F_1^x, F_1^y, F_1^z, F_1^b, \ldots, F_N^x, F_N^y, F_N^z, F_N^b )$$

其中每个点对应四个记号向量，这些向量编码了丰富的语义与几何上下文信息，是后续高斯解码器的关键输入。

### 高斯解码器：从几何到完整外观属性

仅有点云坐标不足以进行高质量渲染，还需预测每个高斯的颜色、不透明度、缩放、旋转和偏移等属性。高斯解码器采用 Transformer 结构，其输入为每个点的两类特征拼接：去量化后的位置编码 $P_n$ 和 AR Transformer 的隐状态特征 $F_n^p$。消融实验（Table 2, Figure 5）证实，仅使用位置编码或仅使用 AR 特征均会导致渲染质量显著下降，二者的协同作用——空间引导与深层语义线索的互补——是解码器性能的关键。

解码器的训练目标为渲染图像与真值之间的复合损失函数：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{L1} \mathcal{L}_{L1} + \lambda_{SSIM} \mathcal{L}_{SSIM} + \lambda_{LPIPS} \mathcal{L}_{LPIPS} + \lambda_{Reg} \mathcal{L}_{Reg}$$

其中各项权重经验设定为 $\lambda_{L1}=1$、$\lambda_{SSIM}=0.5$、$\lambda_{LPIPS}=0.1$、$\lambda_{Reg}=0.1$。该损失组合同时约束像素级精度、结构相似性和感知质量，正则化项则用于稳定训练。

### 动画模块：绑定信息驱动的面部驱动

为使规范空间生成的化身能够做出表情与姿态变化，AR 模型在生成坐标的同时预测每个高斯点的绑定信息 $b_n$。动画模块利用该绑定索引，通过重心坐标插值从对应 FLAME 面片的三个顶点获取蒙皮权重和混合形状参数：

$$\begin{array}{rl} \hat{\mathbf{w}}_i &= b_0 \mathbf{W}_0 + b_1 \mathbf{W}_1 + b_2 \mathbf{W}_2 \\ \hat{\mathbf{S}}_i &= b_0 \mathbf{S}_0 + b_1 \mathbf{S}_1 + b_2 \mathbf{S}_2 \end{array}$$

随后，系统通过顶点级线性混合蒙皮（LBS）和矫正混合形状（corrective blendshapes）驱动规范点云变形至目标姿态。这一设计使得自回归生成的点云天然具备可驱动性，无需额外的绑定后处理步骤。

### 关键设计决策的证据链

上述模块设计中，有两个决策具有决定性证据支持。其一，**自回归逐点生成范式**使模型能够根据主体几何复杂度自适应调整高斯点的密度与总数——在胡须、发丝等精细区域自动放置更多点，在平滑区域减少点数（Figure 2 对比 LAM 的固定模板方法，后者无法重建马尾辫等细节结构）。其二，**AR 隐状态与位置编码的拼接输入**是高斯解码器性能的关键：论文明确指出，将解码器条件化于 AR 生成器的隐状态特征上，能够显著提升最终渲染质量（Sec. 4.2），消融实验量化结果（Table 2）进一步验证了该设计的必要性。

![[assets/figures/papers/paper_list_l2442_https_arxiv_org_abs_2604_04787/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of different Gaussian point cloud modeling approaches. LAM [22] constructs Gaussian point clouds based on a point cloud template, which fails to reconstruct fine details from the image, such as ponytails. In contrast, our method utilizes an AR model to directly model the Gaussian point cloud. It effectively learns the capability to adaptively adjust point density and count, enabling precise modeling. Moreover, we also include final rendering results for comparison. LAM produces distorted geometry and shows noticeable artifacts*



## 实验与关键发现

### 主实验结果

AvatarPointillist在NeRSemble数据集上进行了自驱动（self-reenactment）和交叉驱动（cross-reenactment）两种设定下的评估。Table 1汇总了与现有方法的定量比较结果。

在自驱动设定下，方法在图像重建质量上取得LPIPS 0.15、FID 95.18，在动画精度上取得AKD 2.38、APD 22.86。在更具挑战性的交叉驱动设定下，方法取得FID 160.74、CLIP 0.75、AKD 5.93、APD 153.13。论文声称方法在所有指标上显著优于所有基线方法，但Table 1中未提供各基线方法的具体数值（仅标注了最佳/次佳结果的颜色标识），因此完整的定量对比需查阅原表确认。

Figure 4展示了定性比较结果。在自驱动任务中，方法生成的化身在表情和姿态上与目标图像高度一致；在交叉驱动任务中，方法在身份保留方面表现出明显优势，而基线方法容易出现身份漂移或纹理模糊。这归因于自回归点云生成能够为每个主体自适应地分配高斯点密度，使几何复杂区域（如胡须、发型）获得更精细的表征。

### 消融实验

消融实验聚焦于高斯解码器的输入配置，在NeRSemble数据集上进行定量评估（Table 2），并通过Figure 5展示可视化结果。

**FLAME位置基线**：仅使用规范FLAME网格顶点作为模板，通过解码器预测偏移来变形点云（类似LAM的方法）。该配置导致渲染质量严重下降——Figure 5显示其无法重建马尾辫等精细结构，产生明显的几何畸变和伪影。这直接验证了固定模板点云是现有方法的瓶颈：模板的顶点密度与分布无法适配不同主体的几何复杂性。

**仅使用AR特征**（$F_n^p$）：移除位置编码$P_n$，仅将AR Transformer的隐状态特征输入高斯解码器。此时解码器缺乏显式的空间坐标引导，渲染结果出现细节模糊和结构偏差。

**仅使用位置编码**（$P_n$）：移除AR隐状态特征，仅使用去量化后的坐标信息。该配置虽保留了空间精度，但丢失了AR模型在生成过程中积累的深层语义线索，导致纹理一致性和身份特征保持能力下降。

**完整方法**（$F_n^p + P_n$）：同时使用位置编码和AR隐状态特征，在LPIPS和FID上均取得最优结果。Figure 5显示完整方法能够同时保持精确的几何结构和高保真的纹理细节。这一结果揭示了二者协同作用的机制：位置编码提供显式的空间锚点，确保几何准确性；AR特征携带自回归生成过程中逐步积累的全局上下文信息，补充语义层面的身份线索。论文明确指出，将AR隐状态特征注入解码器是显著提升渲染质量的关键设计。

### 失败模式与局限性

论文未在实验部分系统展示失败案例，但根据方法设计可识别以下潜在失败模式：

1. **高密度点云的效率瓶颈**：AR序列长度随点数线性增长。当生成点数增加时，自回归解码的延迟和显存消耗会显著上升。论文未讨论点数上限的处理策略，也未测试在需要极高密度点云的极端情况下的性能退化程度。

2. **外部模块的误差传播**：方法依赖Pixel3DMM估计FLAME参数，再用点云编码器提取3D结构先验。这些外部模块的估计误差（如极端姿态下的参数失准）会通过交叉注意力机制传播到AR Transformer，进而影响点云生成质量和动画精度。论文未测试方法对这些误差的鲁棒性。

3. **全身扩展的未验证性**：当前方法专注于头部化身，对于全身或更大范围场景的扩展面临角色绑定复杂度和序列长度管理的双重挑战。论文将此列为开放问题，未提供初步实验结果。

### 公平性讨论

论文未明确说明所有方法是否使用完全相同的训练数据划分与超参数搜索空间。基线方法（如LAM、GAGAvatar）的完整复现细节与官方实现对比未被提供，因此定量比较的可复现性需要进一步验证。建议读者在实际对比时关注训练数据、数据增强策略和超参数选择的一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2442_https_arxiv_org_abs_2604_04787/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with state-of-the-art methods. The leftmost column shows the input images, with the target image displayed in the bottom-right corner. The first row presents self-reenactment results, while the remaining three rows show cross-reenactment results. Our method demonstrates superior performance in expression and pose consistency, as well as better identity preservation compared to other approaches*

![[assets/figures/papers/paper_list_l2442_https_arxiv_org_abs_2604_04787/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of ablation study on input setting of Gaussian decoder. The leftmost column shows the input. The FLAME Positions baseline, similar to the LAM method, uses the canonical FLAME mesh vertices as a template and only applies decoder-predicted offsets to deform this template into a final Gaussian point cloud. Pointwise AR Feature refers to using only the AR features (F pn ) without positional information, while Positional Encoding uses only the point embeddings*



## 定位与知识库关联

### 与基线方法的关系

AvatarPointillist 的核心贡献在于将 4D 高斯化身的生成问题重新定义为**自回归点云序列建模**，从而从根本上区别于现有的两类主流方法。

**1. 相对于基于固定模板的 3DGS 化身方法**

以 **LAM** 为代表的现有方法，其高斯点云构建严重依赖固定的 FLAME 顶点模板：模型仅预测顶点偏移量，而高斯点的总数和初始空间分布完全由模板决定。这种设计导致了两方面瓶颈：其一，对于模板无法覆盖的精细几何结构（如马尾辫、浓密胡须），模型缺乏在对应区域增加高斯点的自由度，造成细节丢失或几何畸变；其二，对于几何复杂度较低的平滑区域，固定点数又造成计算资源的浪费。AvatarPointillist 通过自回归 Transformer 直接生成完整的高斯点云坐标序列，使模型能够**根据输入图像中主体的几何复杂度自适应地调整点的密度和总数**——在复杂区域放置更多点，在平滑区域减少点数。这种“像高斯溅射本身那样灵活”的点分布能力，是固定模板范式无法实现的质变。

**2. 相对于隐式几何表示方法**

**GAGAvatar** 采用基于三平面（tri-plane）的 2D-to-3D 提升方案，通过辅助网络细化生成隐式几何表示。该类方法虽然避免了显式模板的约束，但隐式表示在视角一致性和几何精度方面存在固有局限，且仍需额外的解码步骤才能获得可用于动画驱动的显式几何。AvatarPointillist 直接生成显式的 3DGS 点云，不仅几何可解释性更强，而且天然支持基于 LBS 和 blendshapes 的动画驱动，无需额外的几何提取或拟合步骤。

**3. 方法谱系中的独特定位**

从技术路线看，AvatarPointillist 处于三条研究脉络的交汇点：

- **3DGS 化身生成**：继承了 3D Gaussian Splatting 的显式表示和高效渲染优势，但突破了固定模板对点云自由度的限制。
- **自回归生成建模**：借鉴语言模型中成熟的 next-token prediction 范式，将连续几何生成转化为离散序列建模问题，通过交叉注意力机制注入 2D 图像特征和 3D 结构先验。
- **点云深度学习**：利用 Pixel3DMM 估计 FLAME 参数并通过点云编码器 提取顶点特征，作为自回归模型的结构先验，而非直接将其顶点作为生成模板。

### 适用边界

**适用场景**：
- 单张肖像图像到可驱动 4D 高斯化身的端到端生成；
- 需要自适应几何细节建模的人头/面部化身任务，尤其是包含复杂发型、胡须等精细结构的主体；
- 自驱动（self-reenactment）和交叉驱动（cross-reenactment）两种动画设定。

**技术前提与依赖**：
- 依赖外部的 FLAME 参数估计模块（Pixel3DMM）和点云编码器，这些模块的估计误差会沿管线传播，且论文未测试方法对估计误差的鲁棒性；
- 依赖 DINOv2 作为 2D 图像特征提取器，其预训练分布与目标数据的匹配程度会影响生成质量；
- 当前方法专注于头部化身，对于全身或更大范围场景的扩展需要重新设计数据构造、序列长度管理和动画绑定策略。

**不适用或需谨慎的场景**：
- 极高密度点云需求下，AR 序列长度随点数线性增长，推理效率会显著下降；
- 缺乏 FLAME 模板先验的非常规几何体（如非人角色、夸张卡通造型），当前绑定机制可能失效；
- 对实时交互延迟有严格要求的应用，自回归解码的串行特性构成瓶颈。

### 局限与开放问题

**已识别的局限**：

1. **序列长度与效率的矛盾**：AR 模型的序列长度为 $4N$（每个点对应 4 个量化记号），当生成极高密度点云时推理延迟显著增加。论文未讨论点数上限的处理策略或截断机制。

2. **外部模块的误差传播**：FLAME 参数估计（Pixel3DMM）和点云编码器作为前置模块，其误差会直接影响 AR 模型的输入质量和最终生成效果。论文未进行对这些模块估计误差的鲁棒性分析。

3. **训练数据依赖性**：方法在 NeRSemble 多视角数据集上训练，该数据集包含大量受控环境下的多视角人脸数据。在少样本、野外图像或无模板先验条件下的泛化能力有待验证。

4. **范围受限**：当前仅验证了头部化身的生成，未涉及全身化身或更大范围场景。

**开放问题**：

1. **层级化生成策略**：能否通过粗到细（coarse-to-fine）的层级化 AR 策略减少单层序列长度，从而在保持几何精度的同时提升推理效率并支持更稠密的点云？

2. **全身化身扩展**：将同一自回归点云生成范式扩展到全身化身面临多重挑战——全身几何的复杂度更高、角色绑定需要处理更复杂的蒙皮权重分布、大幅面自回归生成的序列长度管理更加困难。这些问题的解决路径尚不明确。

3. **推理加速**：在实时交互应用中，AR 解码的延迟如何进一步压缩？能否引入投机解码（speculative decoding）、非自回归解码或并行化策略来加速推理？

4. **少样本泛化**：当训练数据规模有限或目标主体与训练分布差异较大时，AR 模型的点云生成质量是否会显著退化？能否通过更强的先验注入或元学习策略提升泛化能力？

5. **与扩散模型的对比**：近期扩散模型在 3D 生成领域展现出强大的能力，自回归序列建模与扩散去噪范式在点云生成任务上的优劣对比尚未被系统研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/AvatarPointillist_AutoRegressive_4D_Gaussian_Avatarization.pdf]]

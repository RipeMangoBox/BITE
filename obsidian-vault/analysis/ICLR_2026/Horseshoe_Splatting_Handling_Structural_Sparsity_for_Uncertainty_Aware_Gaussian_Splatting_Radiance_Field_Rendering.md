---
title: "Horseshoe Splatting: Handling Structural Sparsity for Uncertainty-Aware Gaussian-Splatting Radiance Field Rendering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Horseshoe_Splatting_Handling_Structural_Sparsity_for_Uncertainty_Aware_Gaussian_e32e9c64d698.pdf
project_link: null
code_link: "https://github.com/HKU-MedAI/Horseshoe-Splatting"
aliases:
- HS
- HSHSSUAGSRFR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 在3DGS每个高斯核的对角尺度参数上施加全局-局部Horseshoe先验，利用其在零点的尖峰和重尾自适应地收缩不相关方向，同时保留数据支持的显著各向异性结构，从而诱导结构化稀疏性并校准不确定性。
primary_logic: 将Horseshoe先验的贝叶斯收缩机制引入3DGS的协方差建模，通过结构化稀疏性同时实现高质量渲染与像素级后验不确定性，且额外计算开销极小。
claims:
- Horseshoe先验使得尺度后验呈现明显的零处尖峰和重尾分布，成功诱导结构化稀疏性，而高斯和拉普拉斯先验做不到。
- 在LF数据集上，我们的方法在深度不确定性估计（AUSE）上达到0.18，优于所有基线，其中basket场景比次优方法改善23%。
- 在大规模数据集Tanks & Temples上，我们的方法将NLL从2.46（Variational 3DGS）大幅降低至0.58，同时保持领先的PSNR。
- LF dataset (平均) 上 AUSE（深度不确定性） = 0.18
---

# Horseshoe Splatting: Handling Structural Sparsity for Uncertainty-Aware Gaussian-Splatting Radiance Field Rendering

> [!tip] 核心洞察
> 将Horseshoe先验的贝叶斯收缩机制引入3DGS的协方差建模，通过结构化稀疏性同时实现高质量渲染与像素级后验不确定性，且额外计算开销极小。

| 字段 | 内容 |
|------|------|
| 中文题名 | Horseshoe Splatting: 面向不确定性感知的高斯泼溅辐射场渲染的结构化稀疏性处理 |
| 英文题名 | Horseshoe Splatting: Handling Structural Sparsity for Uncertainty-Aware Gaussian-Splatting Radiance Field Rendering |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NHuyk9KsG6) · [Code](https://github.com/HKU-MedAI/Horseshoe-Splatting) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Horseshoe Splatting |
| Dataset | LF dataset, Tanks & Temples, Mip-NeRF360 |

> [!tip] 效果简介
> - LF dataset (平均) 上，AUSE（深度不确定性） 0.18 vs 0.19 (Variational 3DGS) (-0.01)。
> - Tanks & Temples 上，NLL（RGB不确定性） 0.58 vs 2.46 (Variational 3DGS) (-1.88)；PSNR 23.67 vs 23.45 (Variational 3DGS) (+0.22)。
> - Mip-NeRF360 上，NLL 0.72 vs 2.88 (Variational 3DGS) (-2.16)。

## 概要

**背景与瓶颈**：3D高斯泼溅（3DGS）已成为实时新视角合成的事实标准，但其本质上是确定性框架——每个高斯核的协方差矩阵在优化中缺乏显式的结构化稀疏性编码。这导致两个关键缺陷：(1) 噪声主导的方向未被充分正则化，渲染质量受限于协方差的冗余自由度；(2) 无法为视图合成提供像素级的不确定性估计，限制了模型在下游任务（如主动学习、分布外检测）中的适用性。

**核心思路**：本文提出 **Horseshoe Splatting**，将贝叶斯统计中经典的全局-局部 Horseshoe 先验引入3DGS的协方差建模。具体而言，在每个高斯核的对角尺度参数 $s_{ij}$ 上施加层次化先验 $s_{ij} \mid \lambda_{ij}, \theta_j \sim \mathcal{N}(\beta_{ij}, \sigma_{ij}^2 \theta_j^2 \lambda_{ij}^2)$，其中全局收缩参数 $\theta_j$ 和局部收缩参数 $\lambda_{ij}$ 由半柯西先验驱动。Horseshoe 先验在零点具有尖锐的尖峰和厚尾特性，能够自适应地将不相关方向的尺度收缩至零，同时保留数据支持的各向异性结构，从而**诱导结构化稀疏性**并**校准不确定性**。

**方法定位**：Horseshoe Splatting 属于贝叶斯3DGS的变分推断分支，与 **Variational 3DGS**（均值场变分框架）和 **FisherRF**（Fisher信息不确定性）构成直接对比。其独特之处在于先验设计——Horseshoe 先验的逆Gamma增广（IG-IG）结构使得变分后验可在匹配的因子化族中高效推断，仅需在标准3DGS训练目标上附加KL正则项 $\mathcal{L}_{\text{KL}}$，额外计算开销极小。

**主要结果**：
- **深度不确定性**：在LF数据集上，Horseshoe Splatting 的平均AUSE达到 **0.18**，优于所有基线方法；其中 *basket* 场景的AUSE为0.10，比次优方法改善 **23%**（Table 1）。
- **RGB不确定性**：在大规模数据集 Tanks & Temples 上，NLL从 Variational 3DGS 的2.46大幅降至 **0.58**；在 Mip-NeRF360 上从2.88降至 **0.72**，同时保持领先的PSNR（Table 8）。
- **结构化稀疏性**：在 $\varepsilon=5$ 的阈值下，Horseshoe 先验诱导了 **64.62%** 的尺度稀疏性，远超 Laplace 和 Gaussian 先验（Table 7），验证了其收缩机制的独特优势。
- **计算效率**：训练时间87.33秒，渲染速度33 FPS，峰值显存1.43GB，模型大小59MB（Table 9），与确定性3DGS处于同一量级。

**方法谱系与知识库定位**：Horseshoe Splatting 将高维回归中的全局-局部收缩先验（Horseshoe, Carvalho et al., 2009）首次迁移至3D辐射场的协方差建模。相较于 NeRF 系列的不确定性方法——如 **CF-NeRF**（基于归一化流）、**S-NeRF**（贝叶斯权重推断）和 **Bayes' Ray**（拉普拉斯近似）——本方法直接作用于3DGS的高斯核参数空间，避免了额外的网络模块。在3DGS分支内，本方法区别于 **FisherRF**（基于Fisher信息的后验近似）和 **Ensemble GS**（10模型集成）的昂贵计算，通过单次变分训练即可获得校准良好的像素级不确定性。



### 3D高斯泼溅的确定性本质与不确定性盲区

3D高斯泼溅（3D Gaussian Splatting, 3DGS）以其实时渲染能力和优异的视觉质量，迅速成为新视角合成领域的主流方法。然而，3DGS本质上是一个确定性框架：每个高斯核的协方差矩阵（通过缩放矩阵和旋转矩阵参数化）在优化过程中被直接学习，没有任何概率先验或后验推断机制。这意味着模型无法量化其对每个像素预测的置信度——当场景包含遮挡边界、高光反射或训练视角稀疏的区域时，渲染结果可能高度不可靠，但3DGS对此完全“沉默”。

这种确定性建模带来了两个紧密关联的问题。第一，**缺乏像素级不确定性**使得下游应用（如机器人导航、主动感知、医学图像重建）无法区分可信与不可信的渲染区域，限制了3DGS在安全关键场景中的部署。第二，**协方差结构缺乏正则化**：在没有先验引导的情况下，3DGS的高斯核可能在噪声主导的方向上保留非零尺度，导致场景表示中存在冗余的自由度，既降低了表示效率，也使得渲染在不同视角间产生不必要的波动。

### 现有不确定性方法的局限

为弥补3DGS的不确定性盲区，研究者已尝试将贝叶斯推断引入3DGS框架。**FisherRF** 通过Fisher信息矩阵估计参数不确定性，但仅提供权重的后验近似，无法直接建模协方差的结构化稀疏性。**Variational 3DGS** 采用变分推断框架对3DGS进行贝叶斯建模，但其先验选择（如高斯先验或拉普拉斯先验）缺乏对协方差尺度结构化稀疏性的显式诱导能力。**Ensemble GS** 通过训练10个独立的3DGS模型来估计不确定性，计算和存储开销巨大，且本质上是一种频率学派的自助法近似，缺乏统一的概率建模。

在NeRF侧，**CF-NeRF** 通过归一化流对辐射场进行不确定性建模，**S-NeRF** 和 **Bayes' Ray** 分别采用变分推断和拉普拉斯近似。然而，这些方法受限于NeRF的隐式表示特性，无法直接迁移到3DGS的显式高斯核表示中。

### 核心瓶颈：结构化稀疏性的缺失

问题的关键在于，上述方法均未对3DGS的**协方差尺度参数**施加能够诱导**结构化稀疏性**的先验。在3DGS中，每个高斯核的对角尺度参数 $s_{ij}$（$i$ 为高斯核索引，$j$ 为空间维度）控制着该核沿各主轴方向的延展程度。理想情况下，噪声主导的、对场景几何贡献微弱的方向应当被收缩至接近零，而承载显著结构信息的方向则应当被保留——这正是结构化稀疏性的核心诉求。

然而，常用的高斯先验或拉普拉斯先验无法实现这一目标：高斯先验的轻尾特性导致其对大尺度参数的惩罚过强（偏差大），而拉普拉斯先验在零点附近的收缩力度不足（稀疏性弱）。如图4所示（后验密度对比），只有Horseshoe先验能够产生**零点处的尖锐尖峰**（强力收缩噪声方向）和**重尾分布**（保留显著的几何结构），而高斯和拉普拉斯先验均无法同时满足这两个条件。

### 本文动机与核心思路

本文的核心洞察在于：**将Horseshoe先验的贝叶斯收缩机制引入3DGS的协方差建模，可以同时实现高质量渲染与像素级后验不确定性，且额外计算开销极小**。Horseshoe先验是一种经典的全局-局部收缩先验，其半柯西分布的尖峰-重尾特性使其在稀疏信号恢复中具有接近极小极大的理论性质。本文将其应用于3DGS的每个高斯核对角尺度参数上，构建了一个全局-局部层次贝叶斯模型：

$$s_{ij} \mid \lambda_{ij}, \theta_j \sim \mathcal{N}(\beta_{ij}, \sigma_{ij}^2 \theta_j^2 \lambda_{ij}^2)$$

其中 $\theta_j$ 为全局收缩参数（控制整个维度的稀疏程度），$\lambda_{ij}$ 为局部收缩参数（允许单个高斯核的尺度偏离全局趋势）。通过半柯西先验的逆Gamma混合表示，该层次模型在变分推断框架下获得了闭合形式的KL散度，使得训练仅需在标准3DGS损失上增加一个KL正则化项，计算开销极小（见表9，推理时间仅0.03秒）。

这一设计使得模型在训练过程中**自适应地**识别并收缩不相关的尺度方向，同时保留数据支持的显著各向异性结构。最终，通过从变分后验中蒙特卡洛采样尺度参数并渲染，模型能够输出像素级的预测均值和方差，为每个像素提供校准良好的不确定性估计。



## 核心方法与创新机理

**Horseshoe Splatting** 的核心创新在于将贝叶斯结构化稀疏性先验引入 3D 高斯泼溅（3DGS）的协方差建模，从根本上改变了尺度参数的优化行为。与确定性 3DGS（Kerbl et al., 2023）将每个高斯核的对角尺度参数 $s_{ij}$ 作为自由优化变量不同，Horseshoe Splatting 在 $s_{ij}$ 上施加全局-局部 **Horseshoe 先验**：

$$s_{ij} \mid \lambda_{ij}, \theta_j \sim \mathcal{N}(\beta_{ij}, \sigma_{ij}^2 \theta_j^2 \lambda_{ij}^2)$$

其中 $\theta_j$ 为轴 $j$ 上的全局收缩参数，$\lambda_{ij}$ 为每个高斯核的局部收缩参数，二者均服从半柯西先验并通过逆 Gamma（IG-IG）增广表示。这一层次先验在零点具有**尖峰（spike-at-zero）**，在尾部保持**重尾（heavy-tails）**，自适应地将不相关方向上的尺度收缩至近零，同时保留数据支持的显著各向异性结构。

### 关键 changed slots 分析

**1. 协方差尺度先验（从无先验到 Horseshoe 层次先验）**

确定性 3DGS 对尺度参数无显式正则化，仅通过重建损失间接约束，导致噪声主导的方向缺乏收缩机制。Horseshoe 先验的引入带来了两个关键能力：

- **结构化稀疏性诱导**：在 LF torch 场景中，以 $\varepsilon=5$ 为阈值，Horseshoe 先验诱导了 **64.62%** 的尺度稀疏性，远超 Laplace 和 Gaussian 先验（Table 7）。尺度后验呈现明显的“零处尖峰 + 重尾”分布（Figure 4），验证了先验的自适应收缩机制。
- **后验收缩速率保证**：理论分析（Theorem 1）表明，尺度参数的后验收缩速率 $\varepsilon_{N,P}^2 = C \frac{\sigma^2}{P} \frac{k \log(e 3N/k)}{\kappa_{\min}^2}$ 趋近极小极大速率，重尾性质确保大尺度坐标的偏差可忽略——显著几何结构被保留，噪声被收缩。

**2. 推断方法（从确定性优化到变分贝叶斯推断）**

为匹配 Horseshoe 先验的 IG-IG 增广结构，论文设计了**均值场变分推断**框架，将变分分布 $q$ 因子化为 Gaussian 和逆 Gamma 族的乘积。这一设计使得：

- 训练目标从纯重建损失变为 **ELBO**：$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{KL}}$，其中 $\mathcal{L}_{\mathrm{rec}}$ 为期望负对数似然，$\mathcal{L}_{\mathrm{KL}}$ 为变分后验与先验的 KL 散度，通过重参数化技巧进行随机梯度优化。
- 相比 Variational 3DGS 的通用变分框架，Horseshoe 特定的变分族利用了先验的共轭结构，使得 KL 项具有解析形式，优化更稳定。

**3. 不确定性量化（从无到像素级后验不确定性）**

确定性 3DGS 仅输出渲染颜色，无法提供不确定性估计。Horseshoe Splatting 通过**后验预测采样**实现像素级不确定性：

$$p(\tilde{I}_u \mid D) \approx \frac{1}{M} \sum_{m=1}^{M} p(\tilde{I}_u \mid \{\Sigma_i^{(m)}, R_i, c_i, \alpha_i\})$$

从变分后验中采样尺度参数构建协方差矩阵，经可微光栅化渲染后计算逐像素均值和方差。这一过程额外计算开销极小（Table 9，单张 RTX 3090 上推理时间仅小幅增加），却带来了显著的不确定性校准提升：

- **深度不确定性**：LF 数据集上 AUSE 达 **0.18**，优于所有基线，其中 basket 场景比次优方法改善 **23%**（Table 1）。
- **RGB 不确定性**：Tanks & Temples 上 NLL 从 Variational 3DGS 的 2.46 降至 **0.58**（Table 8），Mip-NeRF360 上从 2.88 降至 **0.72**，同时保持领先的 PSNR。

### 创新本质总结

Horseshoe Splatting 的创新不在于引入新的渲染管线或网络架构，而在于**将贝叶斯收缩理论中的 Horseshoe 先验与 3DGS 的协方差参数化进行精确对接**。这一对接使得原本确定性的尺度优化转变为自适应收缩的贝叶斯推断，同时实现了三个目标：(1) 结构化稀疏性——噪声方向被自动收缩；(2) 高质量渲染——显著结构被重尾保护而得以保留；(3) 校准良好的不确定性——后验预测分布自然输出像素级方差。三者并非独立设计，而是 Horseshoe 先验“尖峰-重尾”性质的统一产物，这是该方法区别于其他不确定性感知 3DGS 方法（如 FisherRF 的 Fisher 信息、Ensemble GS 的模型集成、Variational 3DGS 的通用变分推断）的根本所在。



Horseshoe Splatting 以标准 3DGS 管线为基础，在其协方差建模环节插入贝叶斯层次先验与变分推断，形成**先验定义 → 变分后验近似 → 联合 ELBO 优化 → 后验预测采样**四阶段流水线，整体框架如图 2 所示。

### 输入与初始化

管线接收一组多视图 RGB 图像及其通过运动恢复结构（SfM）获得的稀疏点云与相机位姿。与原始 3DGS 一致，每个点被初始化为一个 3D 高斯核，包含位置均值 $\mu_i$、不透明度 $\alpha_i$、球谐颜色系数 $c_i$、旋转四元数 $R_i$ 以及对角尺度矩阵 $S_i = \operatorname{diag}(s_{i1}, s_{i2}, s_{i3})$。**关键修改在于尺度参数 $s_{ij}$ 不再作为确定性变量直接优化，而是被赋予全局-局部 Horseshoe 先验**，成为贝叶斯推断的潜变量。

### 模块一：Horseshoe 先验定义

对每个高斯核 $i$ 的每个轴 $j \in \{1,2,3\}$，对角尺度 $s_{ij}$ 服从如下层次先验：

$$s_{ij} \mid \lambda_{ij}, \theta_j \sim \mathcal{N}(\beta_{ij}, \sigma_{ij}^2 \theta_j^2 \lambda_{ij}^2)$$

其中 $\theta_j$ 为全局收缩参数（所有高斯核共享），$\lambda_{ij}$ 为局部收缩参数（每核每轴独立）。二者均通过半柯西分布表示，并利用逆 Gamma（IG）增广转化为共轭形式：

$$\lambda_{ij}^2 \mid \nu_{ij} \sim \mathrm{IG}(1/2, 1/\nu_{ij}), \quad \nu_{ij} \sim \mathrm{IG}(1/2, 1)$$
$$\theta_j^2 \mid \xi_j \sim \mathrm{IG}(1/2, 1/\xi_j), \quad \xi_j \sim \mathrm{IG}(1/2, 1/b^2)$$

这一层次结构是框架的核心机制：**Horseshoe 先验在零点处的尖峰将噪声主导方向的尺度强收缩至近零，而重尾特性保护数据支持的显著各向异性结构不被过度收缩**，从而在协方差层面诱导结构化稀疏性。

### 模块二：变分后验近似

由于 Horseshoe 层次下的精确贝叶斯推断不可解，采用均值场变分族 $q(\mathbf{s}, \boldsymbol{\lambda}^2, \boldsymbol{\nu}, \boldsymbol{\theta}^2, \boldsymbol{\xi})$ 进行近似。变分分布被因子化为与 IG-IG 增广结构匹配的形式：每个 $s_{ij}$ 的后验为高斯分布，$\lambda_{ij}^2$、$\nu_{ij}$、$\theta_j^2$、$\xi_j$ 的后验均为逆 Gamma 分布。这种设计使得 KL 散度项存在闭式解，保证了优化的可扩展性。

### 模块三：联合 ELBO 与损失函数

训练目标为最小化负证据下界（ELBO），等价于联合损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{KL}} = -\mathbb{E}_q[\ln p(D \mid \{S_i\})] + \mathrm{KL}[q(\mathbf{s}, \boldsymbol{\lambda}^2, \boldsymbol{\theta}^2) \| p(\mathbf{s}, \boldsymbol{\lambda}^2, \boldsymbol{\theta}^2)]$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为期望负对数似然，通过重参数化技巧从变分后验中采样尺度参数并执行可微光栅化渲染来计算；$\mathcal{L}_{\mathrm{KL}}$ 为正则化项，约束后验不偏离先验过远。优化使用随机梯度下降，与原始 3DGS 的训练计划兼容，额外计算开销极小（见表 9，单张 RTX 3090 GPU 上仅增加约 5% 的训练时间）。

### 模块四：后验预测与不确定性输出

训练完成后，从变分后验 $q$ 中蒙特卡洛采样 $M$ 组尺度参数 $\{S_i^{(m)}\}_{m=1}^M$，构建对应的协方差矩阵 $\Sigma_i^{(m)} = R_i S_i^{(m)} S_i^{(m)T} R_i^T$，并通过标准 3DGS 光栅化渲染得到 $M$ 个颜色样本。对每个像素 $u$，其后验预测分布近似为：

$$p(\tilde{I}_u \mid D) \approx \frac{1}{M} \sum_{m=1}^{M} p(\tilde{I}_u \mid \{\Sigma_i^{(m)}, R_i, c_i, \alpha_i\}_{i=1}^N)$$

由此可计算逐像素的预测均值与方差，方差即作为**像素级不确定性图**输出，同时支持任意置信区间的构建。

### 模块间的因果链路

Horseshoe 先验（模块一）通过其尖峰-重尾特性决定收缩行为 → 变分后验（模块二）在数据驱动下自适应地学习哪些轴被收缩、哪些被保留 → ELBO 优化（模块三）平衡数据拟合与稀疏正则化 → 后验采样（模块四）将协方差的不确定性传播至像素空间，产出校准的不确定性估计。**这一链路的核心因果机制在于：结构化稀疏性并非通过硬阈值剪枝实现，而是由 Horseshoe 先验的贝叶斯收缩自动诱导，收缩强度由数据自适应决定**，从而在保持渲染质量的同时获得良好校准的不确定性。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/002_Figure_2.jpg]]
*Figure 2: The framework of our proposed Horseshoe Splatting*



### 3DGS 渲染基础

Horseshoe Splatting 建立在标准 3DGS 的可微渲染管线之上。对于像素 $u$，其渲染颜色 $\hat{I}(u)$ 通过前向合成方式计算：

$$\hat{I}(u) = \sum_{i=1}^{N} T_i \left(1 - \exp(-\alpha_i)\right) c_i, \quad T_i = \exp\Bigl(-\sum_{j<i} \alpha_j\Bigr)$$

其中 $N$ 为与像素 $u$ 重叠的高斯核数量，$c_i$ 为第 $i$ 个高斯核的颜色，$\alpha_i$ 由其不透明度和投影协方差决定，$T_i$ 为累积透射率。每个高斯核的协方差矩阵 $\Sigma_i = R_i S_i S_i^T R_i^T$ 由旋转矩阵 $R_i$ 和对角尺度矩阵 $S_i = \operatorname{diag}(s_{i1}, s_{i2}, s_{i3})$ 参数化。**核心问题在于**：标准 3DGS 对尺度参数 $s_{ij}$ 采用确定性优化，缺乏对噪声方向的正则化机制，也无法输出不确定性。

### 核心模块一：Horseshoe 先验定义

对每个高斯核 $i$ 的每个轴 $j \in \{1, 2, 3\}$，在对角尺度 $s_{ij}$ 上施加全局-局部 Horseshoe 先验：

$$s_{ij} \mid \lambda_{ij}, \theta_j \sim \mathcal{N}(\beta_{ij}, \sigma_{ij}^2 \theta_j^2 \lambda_{ij}^2)$$

- **$\theta_j$**：全局收缩参数，控制第 $j$ 轴的整体收缩强度，由半柯西先验表示
- **$\lambda_{ij}$**：局部收缩参数，允许每个高斯核的每个轴独立偏离全局收缩，同样由半柯西先验表示
- **$\beta_{ij}, \sigma_{ij}^2$**：均值和基础方差，来自 3DGS 的初始化

该先验的关键特性是**零点的尖峰（spike-at-zero）和重尾（heavy tails）**：尖峰使得噪声主导的尺度被强收缩至零附近，而重尾确保数据支持的显著各向异性结构得以保留。

为便于变分推断，利用半柯西分布的逆 Gamma（IG）混合表示将先验增广为：

$$\lambda_{ij}^2 \mid \nu_{ij} \sim \mathrm{IG}(1/2, 1/\nu_{ij}), \quad \nu_{ij} \sim \mathrm{IG}(1/2, 1)$$

$$\theta_j^2 \mid \xi_j \sim \mathrm{IG}(1/2, 1/\xi_j), \quad \xi_j \sim \mathrm{IG}(1/2, 1/b^2)$$

其中 $b$ 为全局收缩超参数，控制整体稀疏程度。

### 核心模块二：变分后验近似

由于 Horseshoe 层次模型下的精确贝叶斯推断不可解，采用**均值场变分推断**。变分分布 $q$ 因子化为与 IG-IG 增广结构匹配的形式：

$$q(\mathbf{s}, \boldsymbol{\lambda}^2, \boldsymbol{\nu}, \boldsymbol{\theta}^2, \boldsymbol{\xi}) = \prod_{i,j} q(s_{ij}) \cdot q(\lambda_{ij}^2) q(\nu_{ij}) \cdot \prod_j q(\theta_j^2) q(\xi_j)$$

其中 $q(s_{ij})$ 为高斯分布，$q(\lambda_{ij}^2)$ 和 $q(\theta_j^2)$ 为逆 Gamma 分布，与先验的共轭结构一致，使得 KL 散度具有闭式解。

### 核心模块三：联合 ELBO 与损失函数

训练目标为最小化负证据下界（ELBO），由重建损失和 KL 正则化项组成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{KL}} = -\mathbb{E}_q[\ln p(D \mid \{S_i\})] + \mathrm{KL}[q(\mathbf{s}, \boldsymbol{\lambda}^2, \boldsymbol{\theta}^2) \| p(\mathbf{s}, \boldsymbol{\lambda}^2, \boldsymbol{\theta}^2)]$$

- **$\mathcal{L}_{\mathrm{rec}}$**：期望负对数似然，通过从 $q$ 中采样尺度参数并渲染来蒙特卡洛近似
- **$\mathcal{L}_{\mathrm{KL}}$**：变分后验与 Horseshoe 先验之间的 KL 散度，起到收缩正则化作用，驱动不相关方向的尺度趋零

采用重参数化技巧进行随机梯度下降优化，使整个框架端到端可训练。

### 核心模块四：后验预测采样与不确定性量化

训练完成后，从变分后验中采样 $M$ 组尺度参数 $\{S_i^{(m)}\}_{m=1}^M$，构建协方差矩阵并通过可微光栅化渲染，得到像素级预测分布：

$$p(\tilde{I}_u \mid D) \approx \frac{1}{M} \sum_{m=1}^{M} p(\tilde{I}_u \mid \{\Sigma_i^{(m)}, R_i, c_i, \alpha_i\})$$

由此计算每个像素的预测均值和方差，生成不确定性图。该过程仅需少量蒙特卡洛采样（如 $M=10$），额外计算开销极小。

### 理论保证

**Theorem 1** 给出了 Horseshoe 先验下尺度参数的后验收缩速率：

$$\varepsilon_{N,P}^2 = C \frac{\sigma^2}{P} \frac{k \log(e\,3N/k)}{\kappa_{\min}^2}$$

其中 $P$ 为观测像素数，$k$ 为非零尺度的数量，$\kappa_{\min}$ 为最小非零奇异值。该速率表明：Horseshoe 收缩以趋近极小极大的速率自动将接近零的尺度驱至零，而重尾特性确保对大尺度坐标的偏差可忽略——即**噪声被收缩，显著几何结构被保留**。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/011_Figure_4.jpg]]
*Figure 4: Posterior density of covariance scale*



## 实验与关键发现

### 主要定量结果

**深度不确定性估计（LF数据集）。** 在LF数据集的8个场景上，Horseshoe Splatting在深度不确定性指标AUSE上达到平均0.18，优于所有基线方法（Table 1）。其中在*basket*场景上AUSE为0.10，相比次优方法Variational 3DGS（0.13）改善约23%。这一提升源于Horseshoe先验的“零处尖峰”特性：噪声主导的方向被自适应收缩至近零，而数据支持的显著结构得以保留，使得深度渲染的不确定性仅在真正的几何边缘处升高，而非遍布整个场景。

**新视角合成质量与不确定性联合评估（LF与LLFF数据集）。** Table 2汇总了LF和LLFF数据集上的PSNR、SSIM、LPIPS以及不确定性指标AUSE和NLL。Horseshoe Splatting在保持与确定性3DGS相当或更优的合成质量的同时，提供了校准良好的像素级不确定性。值得注意的是，在LLFF数据集上，该方法在NLL指标上显著优于Variational 3DGS等贝叶斯基线，验证了Horseshoe先验对RGB不确定性的校准能力。

**大规模场景验证（Tanks & Temples与Mip-NeRF360）。** 在大规模数据集上，Horseshoe Splatting展现出更强的优势（Table 8）。在Tanks & Temples上，该方法将NLL从Variational 3DGS的2.46大幅降至0.58，降幅达76%，同时PSNR达到23.67 dB，略高于Variational 3DGS的23.45 dB。在Mip-NeRF360上，NLL从2.88降至0.72，降幅达75%。这表明Horseshoe先验的结构化稀疏性机制在大规模、复杂几何的场景中尤为有效——全局收缩参数$\theta_j$在轴级别自动识别并抑制噪声方向，而重尾特性确保显著的各向异性结构不被过度收缩。

### 消融研究

**先验分布对比。** Table 3对比了Horseshoe先验与Laplace先验、Gaussian先验在LF数据集上的表现。Horseshoe先验在NLL上达到-0.74，而Laplace和Gaussian先验的NLL明显更高，验证了Horseshoe的“尖峰-重尾”结构对不确定性校准的关键作用。Figure 4进一步从后验密度层面揭示了原因：Horseshoe先验下的尺度后验呈现明显的零处尖峰和重尾分布，成功诱导结构化稀疏性；而Laplace和Gaussian先验无法同时实现有效的噪声收缩和信号保留。

**超参数敏感性。** Table 6展示了全局收缩超参数$\rho$和KL正则化权重$\lambda_{KL}$的影响。在$\rho=-5$和$\lambda_{KL}=0.001$时达到最佳平衡点，此时PSNR=25.86，AUSE=0.31，NLL=0.14。过大的$\lambda_{KL}$会导致先验过度主导，损害合成质量；过小的$\lambda_{KL}$则使先验收缩不足，不确定性校准退化。

**结构化稀疏性量化。** Table 7以阈值$\varepsilon=5$量化了不同先验诱导的尺度稀疏性。Horseshoe先验诱导了64.62%的尺度稀疏性，远高于Laplace先验和Gaussian先验。这一结果直接验证了核心机制：Horseshoe的全局-局部收缩层次结构能够自动识别并抑制协方差中噪声主导的方向，从而实现结构化的、而非无差别的稀疏性。

### 定性分析

**不确定性图可视化。** Figure 3展示了新视角渲染的预测不确定性图。Horseshoe Splatting生成的不确定性在物体边界、高光区域和纹理缺失处升高，而在平坦、纹理丰富的区域保持低位——这与人类对“模型应该在哪里不确定”的直觉一致。Figure 5和Figure 6分别展示了LF和LLFF数据集上的深度渲染与RGB渲染的不确定性定性结果，进一步验证了不确定性估计的空间合理性。

**后验收缩行为。** Theorem 1给出了尺度参数的后验收缩速率$\varepsilon_{N,P}^2 = C \frac{\sigma^2}{P} \frac{k \log(e 3N/k)}{\kappa_{\min}^2}$，表明估计误差随数据量以近极小极大速率减小。Remark 2.1和2.2进一步阐释：Horseshoe收缩自动将接近零的尺度驱动至零，而重尾特性对大坐标引入的偏差可忽略，从而在收缩噪声的同时保留显著几何结构。

### 计算开销

Table 9报告了在LF *torch*场景上的计算开销。所有实验均在单张NVIDIA RTX 3090 GPU上运行。Horseshoe Splatting引入的额外开销极小：变分推断仅增加了对尺度参数的采样和KL散度计算，而可微光栅化管线保持不变。与Ensemble GS（需维护10个独立模型）相比，Horseshoe Splatting以单模型实现了更优的不确定性估计，且计算和存储开销显著更低。

### 下游任务验证

**主动学习。** Table 4和Table 10分别展示了在LF数据集和Tanks & Temples上的主动视图选择结果。以预测方差作为采集函数，Horseshoe Splatting在有限训练视图预算下始终优于随机选择和基于其他不确定性度量的策略，验证了其不确定性估计在下游决策中的实用价值。

**分布外视图检测。** Table 11报告了LLFF数据集上的OOD视图检测结果。Horseshoe Splatting的预测不确定性能够有效区分训练视角分布内的视图与偏离较大的视图，进一步验证了不确定性估计的校准质量。

### 局限性与失败模式

尽管Horseshoe Splatting在不确定性估计和合成质量上表现优异，仍存在以下局限：（1）当前框架仅适用于静态场景，未扩展到动态场景或需要时间建模的任务；（2）协方差建模局限于对角形式，未包含轴间相关性——虽然框架理论上可扩展至低秩修正，但尚未实现；（3）变分推断采用均值场近似，可能低估后验方差，在极端分布外场景下不确定性校准可能偏乐观。这些局限在高度非朗伯表面和剧烈视角变化的场景中可能表现为不确定性图过于平滑或对某些边缘区域的置信度过高，需人工验证具体场景下的表现。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/003_Table_1.jpg]]
*Table 1: Depth uncertainty estimation (AUSE-MAE) performance on the LF dataset. The best result is in boldface, and the second-best is underlined*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/004_Table_2.jpg]]
*Table 2: NVS and uncertainty estimation results on the LF and LLFF datasets. The best result is in boldface, and the second-best is underlined*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/005_Table_3.jpg]]
*Table 3: Horseshoe Prior compared with Laplace Prior and Gaussian Prior*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/006_Figure_3.jpg]]
*Figure 3: Visualization of predicted uncertainty maps of novel view renderings*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/010_Table_7.jpg]]
*Table 7: Comparison of Structural Sparsity Induction on LF torch*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/014_Table_8.jpg]]
*Table 8: Novel View Synthesis (NVS) and Uncertainty Estimation on large-scale datasets (Tanks & Temples and Mip-NeRF360). Our method achieves significantly better uncertainty metrics (AUSE, NLL) while maintaining superior visual quality. Best results are in boldface*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/015_Table_9.jpg]]
*Table 9: Computational Cost on the LF torch scene. All experiments were conducted on a single NVIDIA RTX 3090 GPU*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/007_Table_4.jpg]]
*Table 4: The experiment on active learning*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/016_Table_10.jpg]]
*Table 10: Active Learning on Tanks & Temples*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_NHuyk9KsG6/figures/017_Table_11.jpg]]
*Table 11: OOD View Detection on LLFF*



## 定位与知识库关联

### 与现有基线的关系

Horseshoe Splatting 在 3DGS 不确定性估计这一新兴子领域中，从贝叶斯收缩先验的角度切入，与现有方法形成了清晰的差异化定位。

**相对于 NeRF 系不确定性方法**：早期 NeRF 的不确定性建模主要依赖集成策略或变分推断。**CF-NeRF** 通过归一化流对辐射场进行概率建模，**S-NeRF** 在 MLP 权重上施加变分贝叶斯推断，**Bayes' Ray** 则利用拉普拉斯近似构建空间不确定性场。这些方法受限于 NeRF 的体积渲染管线，推理速度慢且难以实现实时交互。Horseshoe Splatting 继承了 3DGS 的高效光栅化渲染，在保持实时性能的同时引入贝叶斯不确定性，从根本上绕开了 NeRF 的计算瓶颈。

**相对于 3DGS 系不确定性方法**：当前 3DGS 的不确定性估计主要有三条技术路线。**FisherRF** 利用 Fisher 信息矩阵度量参数不确定性，但仅提供后验方差的一阶近似，缺乏完整的概率建模。**Variational 3DGS** 在 3DGS 上引入均值场变分推断，是最直接的贝叶斯扩展，但其先验选择缺乏对协方差结构的针对性设计。**Ensemble GS** 通过集成 10 个独立训练的 3DGS 模型来估计不确定性，计算和存储开销随集成规模线性增长。Horseshoe Splatting 的核心差异在于：它不单纯追求“贝叶斯化”，而是通过 Horseshoe 先验的尖峰-重尾特性，主动诱导协方差尺度的结构化稀疏性。这一设计使得不确定性估计不仅来自后验采样，更源于对噪声方向的显式收缩——在 Variational 3DGS 报告 NLL 为 2.46 的 Tanks & Temples 数据集上，Horseshoe Splatting 将 NLL 大幅降至 0.58（Table 8），同时 PSNR 从 23.45 提升至 23.67，证明结构化稀疏性在不确定性校准上的增益远超单纯的变分框架。

**相对于确定性 3DGS**：原始 **3DGS**（Kerbl et al., 2023）本质上是确定性优化，每个高斯核的尺度参数仅由重建损失驱动，缺乏对噪声方向的显式建模。Horseshoe Splatting 在其基础上仅修改了尺度参数的先验和推断方式，保留了 3DGS 的全部渲染管线，因此额外计算开销极小（Table 9 显示在单张 RTX 3090 上仅增加约 5% 的训练时间）。

### 适用边界

Horseshoe Splatting 的设计假设和实验验证界定了其当前的适用范围：

1. **场景类型**：方法在 LF 数据集（密集 360° 视图）、LLFF 数据集（前向-facing 视图）、Tanks & Temples 和 Mip-NeRF360（大规模场景）上均进行了验证，覆盖了从实验室环境到真实大规模场景的多种设定。结构化稀疏性的理论保证（Theorem 1 中的后验收缩速率）不依赖于特定场景几何，因此方法对一般静态场景具有较好的泛化性。

2. **不确定性类型**：当前框架输出的是逐像素的认知不确定性（epistemic uncertainty），来源于模型参数的后验分布。对于数据本身的偶然不确定性（aleatoric uncertainty），方法通过渲染方程中的噪声项间接建模，但未做显式分解。

3. **计算资源**：所有实验在单张 NVIDIA RTX 3090 GPU 上完成，训练时间与原始 3DGS 可比（Table 9），推理时需进行 M 次蒙特卡洛采样（默认 M=10），可在实时或近实时条件下运行。

### 局限与开放问题

**已识别的局限**：

1. **静态场景限制**：当前方法仅适用于静态场景，未扩展到动态场景或需要时间建模的任务。3DGS 本身已有多项动态扩展工作，将 Horseshoe 先验引入动态高斯核的时序演化是一个自然的延伸方向。

2. **对角协方差假设**：协方差建模局限于对角形式 $\Sigma_i = R_i S_i S_i^T R_i^T$，其中 $S_i = \text{diag}(s_{i1}, s_{i2}, s_{i3})$。这忽略了轴间相关性，可能限制了对复杂各向异性结构的表达能力。论文指出框架理论上可扩展至低秩修正，但尚未实现。

3. **均值场近似的偏差**：变分推断采用均值场近似，因子化假设可能低估后验方差，影响不确定性的精确校准。在强相关的参数空间中，均值场近似的偏差尤为明显。

4. **先验超参数的手动选择**：全局收缩参数 $b$ 和 KL 正则化权重 $\lambda_{KL}$ 需要手动调节（Table 6 显示 $\rho=-5$ 和 $\lambda_{KL}=0.001$ 为最佳设置），缺乏自动适应不同场景稀疏程度的机制。

**开放问题**：

1. **自适应全局收缩**：如何自动选择全局收缩参数 $b$ 的最佳值以适应不同场景的稀疏程度？一个可能的方向是将 $b$ 也纳入层次先验，通过经验贝叶斯或全贝叶斯推断自动学习。

2. **稀疏性驱动的剪枝**：Horseshoe 先验在 $\epsilon=5$ 阈值下诱导了 64.62% 的尺度稀疏性（Table 7），这些被收缩至近零的尺度对应的高斯核对渲染贡献极小。能否将结构稀疏性信息集成到 3DGS 的剪枝与密度控制中，实现更高效的场景表示？这需要解决稀疏性阈值与渲染质量的联合优化问题。

3. **协方差结构扩展**：如何将框架扩展到更完整的协方差结构（如低秩修正 $\Sigma_i = R_i S_i S_i^T R_i^T + L_i L_i^T$），以捕获轴间相关性？这需要在 Horseshoe 先验的收缩机制与低秩因子的建模之间建立一致的贝叶斯框架。

4. **不确定性驱动的主动视图选择**：Table 4 和 Table 10 已初步验证了不确定性在主动学习中的有效性。能否进一步利用结构稀疏性信息——即哪些区域的高斯核尺度被强烈收缩——来指导更高效的视图选择策略？



## 原文 PDF

![[paperPDFs/ICLR_2026/Horseshoe_Splatting_Handling_Structural_Sparsity_for_Uncertainty_Aware_Gaussian_e32e9c64d698.pdf]]

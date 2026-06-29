---
title: "ViP-NeRF: Visibility Prior for Sparse Input Neural Radiance Fields"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/ViP_NeRF_Visibility_Prior_for_Sparse_Input_Neural_Radiance_Fields.pdf
project_link: null
code_link: "https://github.com/NagabhushanSN95/ViP-NeRF"
aliases:
- VN
- ViP-NeRF
tags:
- SIGGRAPH_2023
- topic/graphics_rendering_materials
core_operator: 引入基于平面扫描体积（PSV）计算的密集可见性先验，并设计可见性正则化损失 L_vip 和可见性一致性损失 L_v，在训练过程中约束 NeRF 的可见性预测，从而改善场景几何和渲染质量。
primary_logic: 在多视图设置中，相对深度和可见性比绝对深度更容易可靠估计；利用多视图间的可见性一致性作为密集监督，可以更好地约束稀疏输入 NeRF，显著减少过拟合和渲染伪影。
claims:
- 在 RealEstate-10K 数据集上使用 2 个输入视图时，ViP-NeRF 在 LPIPS（0.1704）、SSIM（0.8087）和 PSNR（24.48）上均显著优于所有基线方法，包括使用预训练密集深度先验的 DDP-NeRF（LPIPS 0.2527）。
- 可见性先验的可靠性显著优于 DDP-NeRF 的密集深度先验：在 RealEstate-10K 上，可见性先验的 F1 分数为 0.89，而深度先验仅为 0.33。
- 消融实验表明，移除密集可见性先验（仅使用稀疏深度先验）会导致 RealEstate-10K 上 LPIPS 从 0.1704 大幅升高到 0.4273，证实了可见性先验的核心作用。
- RealEstate-10K (2 views) 上 LPIPS = 0.1704
---

# ViP-NeRF: Visibility Prior for Sparse Input Neural Radiance Fields

> [!tip] 核心洞察
> 在多视图设置中，相对深度和可见性比绝对深度更容易可靠估计；利用多视图间的可见性一致性作为密集监督，可以更好地约束稀疏输入 NeRF，显著减少过拟合和渲染伪影。

| 字段 | 内容 |
|------|------|
| 中文题名 | ViP-NeRF：面向稀疏输入神经辐射场的可见性先验 |
| 英文题名 | ViP-NeRF: Visibility Prior for Sparse Input Neural Radiance Fields |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://arxiv.org/abs/2305.00041) · [Code](https://github.com/NagabhushanSN95/ViP-NeRF) |
| Topic | #topic/graphics_rendering_materials |
| Method | ViP-NeRF |
| Dataset | RealEstate-10K, NeRF-LLFF |

> [!tip] 效果简介
> - RealEstate-10K (2 views) 上，LPIPS 0.1704 vs 0.2527 (DDP-NeRF) (-0.0823)。
> - NeRF-LLFF (2 views) 上，LPIPS 0.4017 vs 0.4223 (DDP-NeRF) (-0.0206)。
> - RealEstate-10K (4 views) 上，PSNR 28.13 vs 24.17 (DDP-NeRF) (+3.96)。

## 概要

在仅有稀疏输入视图的条件下训练神经辐射场（NeRF）极易过拟合，导致深度估计不准、渲染结果出现模糊与漂浮物等伪影。ViP-NeRF 的核心思路是：利用多视图间相对容易可靠估计的**密集可见性先验**替代传统深度先验来正则化 NeRF。具体而言，该方法通过平面扫描体积（PSV）从输入视图对中计算二元可见性先验图，同时改造 NeRF 使其直接输出 3D 点的可见性，并以可见性先验损失和可见性一致性损失进行约束，从而在无需任何预训练网络的前提下显著改善场景几何与渲染质量。

在 RealEstate-10K 数据集上使用仅 2 个输入视图时，ViP-NeRF 的 LPIPS 达到 0.1704，大幅优于依赖预训练密集深度先验的 DDP-NeRF（0.2527）；消融实验证实，移除密集可见性先验会使 LPIPS 骤升至 0.4273，验证了可见性先验的核心作用。该方法属于**基于多视图几何先验的稀疏输入 NeRF 正则化**路线，其关键定位是将正则化信号从深度先验切换为更可靠、无需学习的可见性先验，为稀疏视图神经渲染提供了新的约束范式。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

在稀疏输入视图（如仅2-4张图像）条件下训练神经辐射场（NeRF）时，模型极易过拟合到有限观测上，导致深度估计严重失准，渲染结果出现模糊、鬼影和漂浮物等伪影。现有方法主要依赖深度先验进行正则化：DS-NeRF使用稀疏SfM深度监督，DDP-NeRF通过预训练CNN补全密集深度先验，RegNeRF则施加深度平滑约束。然而，这些深度先验存在根本性局限——在稀疏输入条件下，绝对深度的可靠估计极为困难，预训练网络也面临跨场景泛化偏差。

ViP-NeRF的核心洞察在于：**在多视图设置中，可见性（即某视图中像素在另一视图中是否可见）比绝对深度更容易进行密集可靠估计**。这一洞察基于一个关键观察——平面扫描体积（Plane Sweep Volume, PSV）中的最小颜色匹配误差与可见性高度相关，而无需精确知道场景深度。因此，可见性可以作为更鲁棒的密集正则化信号，约束NeRF学习正确的场景几何。

### 方法框架与模块链

ViP-NeRF的整体架构围绕三个核心创新展开：**密集可见性先验计算、NeRF输出的可见性扩展、以及双重可见性正则化损失**。其训练流程包含四个顺序耦合的模块：

#### 模块一：可见性先验计算模块（PSV）

该模块对每对输入训练视图（主视图与副视图）离线计算密集的二进制可见性先验图 $\tau'(\mathbf{q})$。具体流程为：

1. **平面扫描体积构建**：在场景深度范围内采样 $K$ 个深度平面，将副视图图像 $I^{(2)}$ 通过单应性变换扭曲到主视图的每个深度平面上，得到 $K$ 张扭曲图像 $I_k^{(2)}$。
2. **误差图计算**：对每个深度平面 $k$，计算扭曲图像与主视图图像 $I^{(1)}$ 的逐像素L1误差，形成误差图 $E_k$：
   $$E_k = \| I^{(1)} - I_k^{(2)} \|_1$$
3. **最小误差提取**：对每个像素 $\mathbf{q}$，取所有深度平面中的最小误差 $e(\mathbf{q}) = \min_k E_k(\mathbf{q})$。若某像素在主视图中可见于副视图，则存在某一深度平面使得颜色一致，最小误差应较小；若被遮挡，则所有深度平面的匹配误差均较大。
4. **二值化**：将最小误差通过指数变换后与阈值0.5比较，得到可见性先验：
   $$\tau'(\mathbf{q}) = \mathbb{1}_{\{ \exp(-e(\mathbf{q}) / \gamma) > 0.5 \}}$$
   其中 $\gamma$ 为温度参数，控制二值化的敏感度。

该模块的关键优势在于**无需任何预训练网络**，仅利用输入视图间的几何一致性即可生成密集先验。实验表明（Table 3），在RealEstate-10K数据集上，该可见性先验的F1分数达到0.89，而DDP-NeRF使用的密集深度先验F1仅为0.33，证实了可见性先验的显著可靠性优势。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2305_00041/figures/008_Table_3.jpg]]
*Table 3: Comparison of reliability of priors used in different models. The reference visibility is obtained using NeRF trained with dense input views*

#### 模块二：NeRF MLP模块（$\mathcal{F}_1$ + $\mathcal{F}_2$）

ViP-NeRF对标准NeRF的MLP架构进行了关键扩展，使其直接输出可见性以加速训练。标准NeRF中，MLP $\mathcal{F}_1$ 从3D点 $\mathbf{p}_i$ 预测体密度 $\sigma_i$ 和潜向量 $\mathbf{h}_i$，MLP $\mathcal{F}_2$ 从潜向量和视角方向 $\mathbf{v}$ 预测颜色 $\mathbf{c}_i$。ViP-NeRF的改动在于：

- **$\mathcal{F}_1$** 保持不变，输出 $\sigma_i$ 和 $\mathbf{h}_i$。
- **$\mathcal{F}_2$** 的输入扩展为潜向量 $\mathbf{h}_i$、主视方向 $\mathbf{v}$ 和**副视方向 $\mathbf{v}'$**，输出扩展为颜色 $\mathbf{c}_i$ 以及**主视方向可见性 $\hat{T}_i$ 和副视方向可见性 $\hat{T}_i'$**：
  $$\mathbf{c}_i, \hat{T}_i, \hat{T}_i' = \mathcal{F}_2(\mathbf{h}_i, \mathbf{v}, \mathbf{v}')$$

这一设计的核心动机是**计算效率**：若直接使用体积渲染累积的透射率 $T_i$ 作为可见性监督目标，则每次计算副视图像素可见性 $t'(\mathbf{q})$ 时需要沿射线采样点并查询 $\mathcal{F}_1$ 获取 $\sigma_i$ 以计算 $T_i'$，计算开销随采样点数线性增长。通过让 $\mathcal{F}_2$ 直接输出 $\hat{T}_i'$，可在单次前向传播中同时获取颜色和可见性，大幅降低训练时间。

#### 模块三：体积渲染模块

体积渲染沿两条路径进行：

1. **颜色渲染**：标准NeRF流程，沿射线积分预测像素颜色 $\hat{\mathbf{c}}$：
   $$\hat{\mathbf{c}} = \sum_{i=1}^N w_i \mathbf{c}_i, \quad w_i = T_i (1 - \exp(-\delta_i \sigma_i))$$
   其中 $T_i = \exp(-\sum_{j=1}^{i-1} \delta_j \sigma_j)$ 为累积透射率。

2. **副视图可见性渲染**：对主视图像素 $\mathbf{q}$ 对应的射线，其3D采样点 $\mathbf{p}_i$ 在副视图方向 $\mathbf{v}'$ 上的可见性 $\hat{T}_i'$（由 $\mathcal{F}_2$ 直接输出）进行加权求和，得到像素级可见性：
   $$t'(\mathbf{q}) = \sum_{i=1}^N w_i \hat{T}_i' \in [0, 1]$$
   权重 $w_i$ 与颜色渲染共享，确保可见性估计与场景几何一致。

#### 模块四：损失计算与反向传播模块

ViP-NeRF的总损失由三部分组成，形成互补的正则化体系：

1. **颜色重建损失 $\mathcal{L}_{mse}$**：标准MSE损失，约束渲染颜色与真实像素颜色一致。

2. **可见性先验损失 $\mathcal{L}_{vip}$**：将PSV计算的可见性先验 $\tau'(\mathbf{q})$ 作为监督信号，约束NeRF预测的像素可见性 $t'(\mathbf{q})$：
   $$\mathcal{L}_{vip}(\mathbf{q}) = \max(\tau'(\mathbf{q}) - t'(\mathbf{q}), 0)$$
   该损失采用**单侧惩罚**设计：仅当先验认为可见（$\tau'=1$）而预测可见性不足时施加惩罚。当先验认为不可见（$\tau'=0$）时，无论预测值如何均不惩罚。这一设计基于关键观察：PSV先验在判断"不可见"时可能不可靠（如镜面反射区域颜色一致性假设不成立），因此避免在不可靠的不可见区域施加错误监督。

3. **可见性一致性损失 $\mathcal{L}_v$**：确保 $\mathcal{F}_2$ 直接输出的可见性 $\hat{T}_i$ 与体积渲染累积的透射率 $T_i$ 相互一致，防止网络学习到自相矛盾的几何表示：
   $$\mathcal{L}_v = \sum_{i=1}^N \left( (\text{SG}(T_i) - \hat{T}_i)^2 + (T_i - \text{SG}(\hat{T}_i))^2 \right)$$
   其中 $\text{SG}(\cdot)$ 表示停止梯度操作，即交替固定一方优化另一方，避免训练震荡。该损失使网络直接输出的可见性与隐式几何保持自洽，同时通过停止梯度稳定训练。

总损失为：
$$\mathcal{L} = \mathcal{L}_{mse} + \lambda_{vip} \mathcal{L}_{vip} + \lambda_v \mathcal{L}_v$$
其中 $\lambda_{vip}$ 和 $\lambda_v$ 为权重超参数。

### 三个关键Changed Slots

相对于基线方法，ViP-NeRF在以下三个核心维度实现了创新：

1. **正则化信号/先验**：从深度先验（稀疏或密集）转变为密集可见性先验。深度先验需要精确的绝对距离估计，在稀疏输入下可靠性低（DDP-NeRF深度先验F1仅0.33）；可见性先验仅需判断遮挡关系，通过PSV即可可靠计算（F1达0.89），且无需预训练。

2. **NeRF MLP输出**：从仅预测颜色和体密度扩展为额外直接输出主视和副视方向的可见性 $\hat{T}_i$ 和 $\hat{T}_i'$。这一改动将可见性计算从昂贵的体积渲染累积中解耦，使训练效率显著提升。

3. **监督损失函数**：从仅使用颜色MSE损失扩展为添加 $\mathcal{L}_{vip}$ 和 $\mathcal{L}_v$ 双重可见性正则化。$\mathcal{L}_{vip}$ 提供跨视图的密集几何监督，$\mathcal{L}_v$ 保证网络预测的内部一致性，两者协同作用实现鲁棒的几何学习。

### 模块间因果关系

四个模块形成紧密的因果链：

- **PSV模块**提供可靠的外部几何监督信号（$\tau'$），其可靠性（F1=0.89）是整个方法有效性的前提。
- **MLP模块**的可见性输出扩展使后续的可见性监督能以计算高效的方式施加，避免了对每条射线重复体积渲染的开销。
- **体积渲染模块**将MLP的点级可见性聚合为像素级可见性 $t'(\mathbf{q})$，使其与PSV先验的像素级粒度对齐。
- **损失模块**中，$\mathcal{L}_{vip}$ 将PSV先验与渲染可见性连接，$\mathcal{L}_v$ 将MLP直接输出与隐式几何连接，形成闭环约束。消融实验（Table 5）证实：移除 $\mathcal{L}_{vip}$（即仅使用稀疏深度先验）导致LPIPS从0.1704急剧恶化至0.4273，验证了可见性先验的核心因果作用；仅使用可见性先验（无稀疏深度）仍能取得LPIPS 0.2754，显著优于DDP-NeRF的0.2527，进一步证实可见性正则化的独立有效性。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2305_00041/figures/001_Figure_1.jpg]]
*Figure 1: Overview of ViP-NeRF architecture. Given the images from primary and secondary views, we estimate a visibility prior map in the primary view and use it to supervise the visibility of pixels as predicted by the NeRF. Specifically, we cast a ray through a randomly selected pixel in the primary view and sample 3D points along the*

## 实验与关键发现

### 主实验结果

ViP-NeRF 在三个标准稀疏视图基准上进行了系统评估，与 InfoNeRF、DietNeRF、RegNeRF、DS-NeRF 和 DDP-NeRF 等方法对比。

**RealEstate-10K 数据集（室内外场景视频）** 上，仅使用 2 个输入视图时，ViP-NeRF 在所有指标上均达到最优。如 Table 1 所示，LPIPS 为 **0.1704**，相比最强基线 DDP-NeRF 的 0.2527 降低了 0.0823（相对提升约 32.6%）；PSNR 为 **24.48** dB，SSIM 为 **0.8087**。当输入视图增加到 4 个时，ViP-NeRF 的 PSNR 达到 **28.13** dB，明显优于 DDP-NeRF 的 24.17 dB（提升 3.96 dB），且 LPIPS 进一步降至 0.0966。这表明可见性先验在极稀疏输入下尤为有效，且随视图增加持续受益。

**NeRF-LLFF 数据集（前向拍摄的真实场景）** 上，2 视图设置下 ViP-NeRF 的 LPIPS 为 **0.4017**，优于 DDP-NeRF 的 0.4223；PSNR 为 **19.86** dB，SSIM 为 **0.6266**。该数据集场景更复杂、视点变化更大，所有方法性能均有所下降，但 ViP-NeRF 仍保持领先。

**DTU 数据集（物体级扫描）** 上的对比需注意公平性问题：RegNeRF+ 在训练时使用了测试相机姿态，而 ViP-NeRF 仅使用训练视图姿态。在相同设置下，ViP-NeRF 优于未使用测试姿态的 RegNeRF 及 DS-NeRF（Table 7）。

### 先验可靠性分析

ViP-NeRF 的核心优势源于可见性先验比深度先验更可靠。Table 3 以密集视图训练的 NeRF 的可见性为参考，评估了不同先验的质量：在 RealEstate-10K 上，ViP-NeRF 的可见性先验 F1 分数为 **0.89**，而 DDP-NeRF 使用的密集深度先验 F1 仅为 **0.33**。深度先验需要从稀疏 SfM 点通过预训练 CNN 补全为密集深度图，这一过程在稀疏输入下极易产生错误估计；而可见性先验通过平面扫描体积直接计算，无需预训练，仅依赖于输入视图间的颜色一致性，因此估计更准确。

深度估计的定量评估（Table 4）进一步佐证了这一结论：以密集 NeRF 的深度为参考，ViP-NeRF 在 RealEstate-10K 上的深度 RMSE 为 **1.6411**，SROCC 为 **0.3896**，均优于所有基线方法。Figure 5 的定性对比显示，DDP-NeRF 的深度图过于平滑，丢失了物体边界和细节，而 ViP-NeRF 能更好地保持场景几何结构。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2305_00041/figures/007_Figure_5.jpg]]
*Figure 5: Estimated depth map on RealEstate-10K dataset with two input views. We find that ViP-NeRF is better in both frame synthesis and depth estimation compared to the competing models. For example, in the first row, the depth estimated by DDP-NeRF is smooth which may be leading to a loss of sharpness in synthesizing the shrubs. In contrast, ViP-NeRF predictions are sharper. For better visualization, we show inverse depth and normalize it to set the maximum value to unity*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2305_00041/figures/009_Table_4.jpg]]
*Table 4: Evaluation of depth estimated by different models with two input views. The reference depth is obtained using NeRF trained with dense input views. The depth RMSE on the two datasets are of different orders on account of different depth ranges*

### 消融实验

Table 5 的消融实验揭示了各组件的作用机制：

**移除密集可见性先验（仅保留稀疏深度先验）** 导致性能急剧下降：RealEstate-10K 上 LPIPS 从 0.1704 升至 **0.4273**，NeRF-LLFF 上从 0.4017 升至 **0.4548**。这证实了密集可见性监督是性能提升的主要驱动力，而非稀疏深度先验。

**仅使用密集可见性先验（无稀疏深度）** 仍能取得较好性能：RealEstate-10K 上 LPIPS 为 **0.2754**，显著优于 DS-NeRF（依赖稀疏深度）和 DDP-NeRF（依赖密集深度先验）。这进一步验证了可见性先验本身的有效性，也说明其可以作为独立的强正则化信号，无需深度监督。

**移除可见性一致性损失 L_v** 同样导致性能下降，表明直接输出的可见性 $\hat{T}_i$ 与体积渲染累积的透射率 $T_i$ 之间的自洽性约束对稳定训练有贡献。

### 失败模式与适用边界

尽管 ViP-NeRF 在多数场景下表现优异，但存在以下局限：

1. **去遮挡区域合成质量下降**：可见性先验仅约束至少两个输入视图中可见的区域。对于在所有输入视图中均被遮挡的区域（如物体背面的空洞），无法提供监督，导致这些区域的渲染出现模糊或伪影。这是多视图可见性约束的固有边界。

2. **镜面反射表面**：可见性先验的计算依赖于颜色一致性假设——同一 3D 点在两个视图中的颜色应相似。当场景包含高度镜面反射表面（如玻璃、金属）时，该假设不成立，平面扫描体积的误差估计不准确，导致先验不可靠。Figure 4 的定性结果表明，随输入视图增加，ViP-NeRF 对镜面区域的建模有所改善，但 2 视图下仍存在挑战。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2305_00041/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative examples on RealEstate-10K and NeRF-LLFF dataset with two, three, and four input views. We observe that ViP-NeRF models specular regions better as the number of input views increases. For example, in the first row, the reflection of the chair is better reconstructed as the number of views increases*

3. **大基线视图间距**：当输入视图极少（如仅 2 张）且视点间距较大时，平面扫描体积的匹配误差增大，可见性先验的可靠性可能减弱。NeRF-LLFF 数据集上整体性能低于 RealEstate-10K，部分原因即在于视点变化更大。

4. **计算开销**：可见性先验计算需要对每对训练视图执行平面扫描体积构建，视图数增加时计算量线性增长。不过，通过让 NeRF 直接输出可见性 $\hat{T}_i$ 避免了在训练期间重复计算体积渲染的透射率，有效降低了正则化损失的计算成本。

### 实验公平性说明

ViP-NeRF 不使用任何预训练网络或外部数据学习先验，而 DDP-NeRF 依赖在大量场景上预训练的 CNN 进行密集深度补全。这种差异意味着 DDP-NeRF 的性能可能受预训练数据分布的影响，在分布外场景中泛化能力存疑。ViP-NeRF 的可见性先验完全从输入视图本身计算，具有更好的场景自适应性和泛化性。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2305_00041/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on RealEstate-10K dataset*

## 定位与知识库关联

ViP-NeRF 在稀疏输入 NeRF 的正则化设计空间中，将核心正则化信号从**深度先验**替换为**密集可见性先验**，这是其相对于所有基线方法的根本性 slot 变更。理解这一变更的关键在于：稀疏视图下，绝对深度的可靠估计极为困难，而相对深度关系与可见性（即某视图中像素在另一视图中是否可见）是一个更容易被可靠推断的几何量。ViP-NeRF 正是抓住了这一因果瓶颈，将正则化的锚点从“场景的绝对深度是多少”转移到“两个视图间哪些区域是共见的”。

### 相对已有方法的本质差异

**正则化信号 slot 的根本替换。** 现有稀疏输入 NeRF 方法普遍依赖深度作为几何正则化信号：**DS-NeRF**（Deng et al., 2022）使用 COLMAP 的稀疏 SfM 深度点作为监督；**DDP-NeRF**（Roessle et al., 2022）进一步引入预训练 CNN 将稀疏深度补全为密集深度先验；**RegNeRF**（Niemeyer et al., 2022）通过深度平滑正则化和幻觉视图来约束几何。这些方法的共同假设是：如果能获得可靠的深度监督，NeRF 的几何学习就能被有效约束。然而，深度先验的可靠性在稀疏输入下存在系统性缺陷——DDP-NeRF 的密集深度先验在 RealEstate-10K 上的 F1 分数仅为 0.33（Table 3），说明预训练深度补全网络在稀疏视图场景中泛化能力有限。

ViP-NeRF 的替换逻辑是：放弃直接监督绝对深度，转而监督一个更容易可靠估计的量——可见性。其可见性先验通过平面扫描体积（PSV）从给定的稀疏视图中直接计算，无需任何预训练网络，在 RealEstate-10K 上达到 F1 分数 0.89（Table 3）。这一高可靠性源于可见性估计依赖的是多视图颜色一致性（相对比较），而非绝对深度的回归——前者在几何上是一个更良态的问题。

**输出 slot 的协同扩展。** 为高效实施可见性正则化，ViP-NeRF 对标准 NeRF 的输出 slot 进行了扩展：MLP 不仅预测颜色 $c_i$ 和体密度 $\sigma_i$，还直接输出 3D 点在主视和副视方向的可见性 $\hat{T}_i$ 和 $\hat{T}_i'$。这与标准 NeRF 中仅通过体积渲染间接获得透射率 $T_i$ 的做法形成对比。直接输出可见性的设计使得可见性一致性损失 $\mathcal{L}_v$ 能够以计算高效的方式施加，避免了每次训练迭代都需要对副视方向进行完整的体积渲染。

**损失函数 slot 的对应调整。** ViP-NeRF 在标准颜色 MSE 损失 $\mathcal{L}_{mse}$ 之上，增加了两个新损失项：可见性先验损失 $\mathcal{L}_{vip}$ 和可见性一致性损失 $\mathcal{L}_v$。$\mathcal{L}_{vip}$ 的设计具有不对称性——仅当先验认为某像素可见（$\tau'=1$）而网络预测的可见性 $t'$ 不足时才施加惩罚，对先验认为不可见的区域不施加损失。这种设计直接回应了可见性先验的核心不对称特性：可见性先验在“可见”区域具有高置信度（颜色匹配提供了强证据），而在“不可见”区域置信度较低（颜色不匹配可能源于遮挡，也可能源于镜面反射或视图依赖效应）。这一不对称损失设计是 ViP-NeRF 方法逻辑自洽的关键环节。

### 知识库挂载点

ViP-NeRF 在知识图谱中的定位可以从三个维度理解：

**挂载点一：稀疏输入 NeRF 正则化方法谱系。** ViP-NeRF 属于利用多视图几何约束进行正则化的方法分支，与基于语义一致性（**DietNeRF**, Jain et al., 2021）、基于信息论（**InfoNeRF**, Kim et al., 2022）和基于深度先验（DS-NeRF, DDP-NeRF, RegNeRF）的方法形成互补而非替代关系。其可见性先验可以与其他正则化策略组合使用——消融实验显示，在密集可见性先验基础上加入稀疏深度监督可进一步提升性能（RealEstate-10K LPIPS 从 0.2754 降至 0.1704，Table 5），说明可见性正则化与深度正则化存在协同效应。

**挂载点二：平面扫描体积方法在神经渲染中的应用。** PSV 是经典的多视图立体匹配工具，ViP-NeRF 将其从深度估计的前端模块重新定位为训练过程中的正则化信号生成器。这一用法与基于 cost volume 的 NeRF 变体（如 MVSNeRF）有本质区别：后者将 PSV 特征直接馈入网络作为输入编码，而 ViP-NeRF 仅用 PSV 生成一个二值可见性掩码作为监督信号，保持了 NeRF 架构的简洁性和通用性。

**挂载点三：NeRF 的几何正则化与过拟合抑制。** 稀疏输入 NeRF 过拟合的本质原因是颜色渲染损失对几何的约束不足——网络可以通过学习“漂浮”的半透明云团来解释训练视图的颜色，导致新视图渲染出现伪影。ViP-NeRF 的可见性正则化通过跨视图的几何一致性约束，切断了这种“作弊”路径：如果网络在错误深度位置积累了体密度，其预测的跨视图可见性将与 PSV 先验产生冲突，从而被损失函数惩罚。这一机制与 RegNeRF 的深度平滑约束在目标上相似（都旨在消除漂浮物），但作用路径不同——可见性约束是跨视图的、二值的、基于颜色一致性的，而深度平滑约束是单视图的、连续的、基于局部先验的。

### 适用边界与限制

ViP-NeRF 的可见性先验机制存在几个明确的适用边界：

1. **视图数量下限。** 可见性先验的计算至少需要两个训练视图，且当输入视图极少（如仅 2 张）且视图间距较大时，PSV 的匹配误差增大，先验可靠性可能减弱。这是基于图像匹配的方法的固有局限。

2. **去遮挡区域盲区。** 可见性先验仅能约束至少两个输入视图中可见的区域。对于在所有训练视图中均被遮挡的区域，ViP-NeRF 无法提供任何正则化信号，这些区域的渲染质量依赖于 NeRF 的插值泛化能力。这一限制在场景遮挡严重时尤为突出。

3. **镜面反射表面的退化。** PSV 可见性估计基于朗伯颜色一致性假设。当场景包含高度镜面反射表面时，不同视图间的颜色不再一致，可见性先验可能出现系统性错误。论文在 Figure 4 的定性结果中观察到，随着输入视图数量增加，镜面反射区域的建模有所改善，但两视图设置下这仍是一个薄弱环节。

4. **与预训练先验方法的公平比较。** DDP-NeRF 依赖在大量场景上预训练的深度补全 CNN，而 ViP-NeRF 的可见性先验完全从给定稀疏视图中在线计算。这一差异使得两者在跨域泛化场景下的性能对比需要谨慎解读——DDP-NeRF 的性能可能受限于预训练数据与测试场景的域差异。

### 后续研究启发

ViP-NeRF 提出的可见性先验范式为稀疏输入神经渲染打开了几个有价值的研究方向：

1. **学习型可见性先验。** 论文在开放问题中明确提出了使用预训练网络估计可见性的可能性。与深度补全网络相比，可见性估计是一个二分类问题，可能具有更好的跨域泛化能力。这一方向可能产生类似 DDP-NeRF 之于 DS-NeRF 的改进路径——用学习型密集可见性先验替代手工 PSV 可见性先验，特别是在镜面反射区域。

2. **遮挡区域的幻觉监督。** 对于在所有训练视图中均被遮挡的区域，可见性先验天然无法提供约束。一个自然的扩展是通过生成模型幻觉新视图，为这些区域提供额外的可见性监督，类似于 RegNeRF 的幻觉视图策略但作用于可见性域。

3. **可见性先验与深度先验的深度融合。** 消融实验已表明可见性先验与稀疏深度监督存在协同效应。探索两者在训练过程中的动态加权或级联使用策略，可能进一步提升鲁棒性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/ViP_NeRF_Visibility_Prior_for_Sparse_Input_Neural_Radiance_Fields.pdf]]
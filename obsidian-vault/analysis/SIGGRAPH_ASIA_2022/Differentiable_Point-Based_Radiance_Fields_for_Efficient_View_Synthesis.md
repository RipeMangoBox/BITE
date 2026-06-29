---
title: Differentiable Point-Based Radiance Fields for Efficient View Synthesis
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Differentiable_Point_Based_Radiance_Fields_for_Efficient_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- DPBRF
- DPBRFEVS
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
core_operator: 将场景表示从隐式坐标网络（MLP）改为显式点云，并将渲染方式从体积射线步进（后向映射）改为可微点基splatting（前向映射），从而大量减少计算冗余，实现数量级加速。
primary_logic: 尽管NeRF的MLP紧凑且单次评估相对高效，但图像合成的本质是‘后向映射’操作，需多次评估。若采用支持‘前向映射’的表示（即单次前向pass即可生成图像），可在存储上获得适度增益，更重要的是在训练和渲染时间上获得数量级的效率提升。
claims:
- 训练和推理速度均比NeRF快300倍，静态场景内存占用低于10 MB。
- 在Blender合成数据集上，PSNR达30.3 dB，SSIM 0.945，LPIPS 0.078，训练仅需3分钟，推理32 fps，模型大小9 MB，相较于Plenoxels取得更优的效率-质量平衡。
- 消融实验表明，去除球谐函数建模、混合coarse-to-fine策略或训练过滤函数，均导致PSNR大幅下降（27.1 dB, 26.6 dB, 29.1 dB），验证了各组件的有效性。
- "Synthetic Blender Dataset (static) [Mildenhall et al. 2020] 上 PSNR (dB) / SSIM / LPIPS / Training / Inference / Model Size = 30.3 / 0.945 / 0.078 / ~3 min / 32 fps / 9 MB"
---

# Differentiable Point-Based Radiance Fields for Efficient View Synthesis

> [!tip] 核心洞察
> 尽管NeRF的MLP紧凑且单次评估相对高效，但图像合成的本质是‘后向映射’操作，需多次评估。若采用支持‘前向映射’的表示（即单次前向pass即可生成图像），可在存储上获得适度增益，更重要的是在训练和渲染时间上获得数量级的效率提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于可微点辐射场的高效视图合成 |
| 英文题名 | Differentiable Point-Based Radiance Fields for Efficient View Synthesis |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2205.14330) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation |
| Method | Differentiable Point-Based Radiance Fields |
| Dataset | Synthetic Blender Dataset (static) [Mildenhall et al. 2020], STNeRF Dataset (multi-view video) [Zhang et al. 2021], DSC Dataset (dynamic scenes) [Vlasic et al. 2009] |

> [!tip] 效果简介
> - Synthetic Blender Dataset (static) [Mildenhall et al. 2020] 上，PSNR (dB) / SSIM / LPIPS / Training / Inference / Model Size 30.3 / 0.945 / 0.078 / ~3 min / 32 fps / 9 MB vs NeRF: 31.01 / -- / -- / ~20 h / ~0.02 fps / 5 MB; Plenoxels: 31.71 / -- / -- /... (PSNR略低于NeRF和Plenoxels（约0.7-1.4 dB），但训练速度提升约200倍（vs NeRF）和3倍（vs Plenoxels），推理速度提...)。
> - STNeRF Dataset (multi-view video) [Zhang et al. 2021] 上，PSNR (dB) / SSIM / LPIPS / Training / Inference / Model Size 34.6 / 0.927 / 0.207 / 30 min / 25 fps / 110 MB vs STNeRF: 32.1 / -- / -- / 50 h / 1/30 fps / 12 MB; NeRF-t: 28.9 / -- / -- / 100... (PSNR高出2.5-5.7 dB，训练速度快100-200倍，推理速度快约750倍，且模型大小仍保持较低)。
> - DSC Dataset (dynamic scenes) [Vlasic et al. 2009] 上，Training / Inference / Model Size (total for all frames) 1 h / 28 fps / 240 MB vs STNeRF: 86 h / 1/18 fps / 12 MB; NeRF: 75 h / 1/15 fps / 16 MB; NeRF-t: 50 h /... (训练速度快50-86倍，推理速度快400-500倍，总模型大小稍大但因每帧独立点云)。

## 概要

神经辐射场（NeRF）依赖沿每条光线采样数百点并反复查询坐标网络，导致训练与推理极慢，难以用于实时场景。本文提出**可微点基辐射场**，将场景表示从隐式 MLP 替换为显式 3D 点云，每点存储可学习的 RGB 球谐系数以建模视角相关辐射度；渲染方式从体积射线步进改为可微点基 splatting 前向映射，单次前向 pass 即可合成图像。训练采用混合 coarse-to-fine 策略，联合优化点位置与外观参数并周期性进行几何细化。

在 Blender 合成数据集上，该方法 PSNR 达 30.3 dB，训练仅需约 3 分钟、推理 32 fps、模型大小 9 MB，训练和推理速度均比 NeRF 快约 300 倍；在多视图视频数据集上，PSNR 较 STNeRF 和 NeRF-t 高出 2.5–5.7 dB，训练速度快 100–200 倍。方法定位于显式点基表示与可微前向渲染的交叉点，相比隐式体积方法以适度质量代价换取数量级的效率提升。

## 核心方法与创新机理

### 问题瓶颈与因果转向

神经辐射场（NeRF）的核心计算瓶颈在于其**隐式坐标网络+体积射线步进**的渲染范式。具体而言，NeRF 将场景编码为一个5D MLP（位置+视角方向），渲染每帧图像时需沿每条光线采样数百个点，并对每个采样点执行一次完整的网络前向传播。这种“后向映射”（backward mapping）策略——即从像素反向追踪场景属性——导致单帧渲染需数十秒，训练需数十小时，且内存消耗随采样密度线性增长。

本方法的核心洞察在于：**若将场景表示从隐式MLP切换为显式点云，并将渲染方式从体积射线步进改为可微点基splatting（前向映射），则可在单次前向pass中完成整帧合成，从而消除沿光线重复评估的冗余计算。** 这一因果转向直接带来了训练和推理速度的数量级提升——论文宣称比NeRF快300倍——同时将静态场景模型大小压缩至10 MB以下。

### 核心表示与渲染管线

方法由五个顺序模块构成，形成从初始化到最终渲染的完整可微管线：

**1. 视觉壳点云初始化**

利用多视图前景掩码，在由所有视图定义的视觉壳（visual hull）内进行拒绝采样：随机生成候选3D点，仅保留投影到所有视图均落在前景掩码内的点。这一过程无需COLMAP等外部几何估计，仅依赖掩码提供的粗糙空间先验，为后续优化提供初始几何猜测。初始点云密度通过采样数量控制，论文中静态场景典型使用约15k点。

**2. 球谐辐射度模型**

每个3D点 $P_i$ 存储一组可学习的球谐系数：
$$H_i = \{ h_{i,lm} \mid 0 \leq l \leq l_{\text{max}}, -l \leq m \leq l \}$$

给定相机 $j$ 的视点方向 $v_i^j = \frac{ R_j P_i + t_j }{ \| R_j P_i + t_j \| }$，该点的RGB颜色通过球谐基函数加权求和得到：
$$c_i^j = \sum_{l=0}^{l_{\text{max}}} \sum_{m=-l}^{l} h_{i,lm} Y_l^m( v_i^j )$$

这一设计使每个点具备视角相关的辐射特性（如高光、反射），同时保持紧凑的参数化——仅需 $(l_{\text{max}}+1)^2 \times 3$ 个系数。论文中 $l_{\text{max}}$ 通常取2或3，在表达能力与存储效率间取得平衡。消融实验（Table 3）表明，移除球谐函数（即使用与视角无关的颜色）导致PSNR从30.3 dB骤降至27.1 dB，验证了视角相关建模对高光区域重建的关键作用。

**3. 可微点splatting渲染器**

渲染过程完全摒弃光线步进，采用前向splatting策略：

- **点投影**：将3D点通过相机外参 $(R_j, t_j)$ 和内参 $M_j$ 投影至图像平面，经透视除法得到2D坐标：
  $$\boldsymbol{p}_i^j = \left( M_j ( R_j \boldsymbol{P}_i + t_j ) \right)^{\downarrow}$$

- **高斯不透明度核**：以投影位置 $\boldsymbol{p}_i^j$ 为中心，半径为 $r$ 的高斯RBF定义点对像素 $u$ 的不透明度贡献：
  $$\alpha_i^j(u) = \frac{1}{\sqrt{2\pi r^2}} e^{ -\frac{ \| \boldsymbol{p}_i^j - \boldsymbol{u} \|^2 }{ 2r^2 } }$$
  半径 $r$ 控制splat的扩散范围，直接影响渲染的锐度与抗锯齿特性。

- **前端到后端alpha混合**：按深度排序所有点后，逐点累加颜色贡献：
  $$\hat{I}_j(u) = \sum_{i=1}^{n} A_i^j(u) c_i^j$$
  其中净贡献权重 $A_i^j(u) = \alpha_i^j(u) \prod_{k=1}^{i-1} (1 - \alpha_k^j(u))$ 建模了前方点对后方点的遮挡衰减。

整个渲染过程完全可微，梯度可通过alpha混合链反向传播至点位置、球谐系数和高斯半径，无需离散采样或近似梯度估计。

**4. 混合coarse-to-fine优化策略**

这是方法区别于简单梯度下降的关键创新。训练并非仅优化点参数，而是交替执行**梯度更新**与**几何细化操作**（Algorithm 1）：

- **梯度更新阶段**：使用Adam优化器同时更新所有点的位置和球谐系数，损失函数为MSE重建损失与各向异性总变差（TV）正则项的组合：
  $$\mathcal{L} = \sum_{j=1}^{N} \| I_j - \hat{I}_j \|_2^2 + \lambda \text{TV}( \hat{I}_j )$$
  TV正则强制渲染图像的光滑性，抑制点云噪声。

- **几何细化阶段**（周期性触发）：
  - **体素缩减（voxel reduction）**：将空间划分为体素网格，每个体素内仅保留一个代表性点，消除冗余。
  - **异常值剔除（outlier removal）**：移除投影一致性差的点（即并非在所有视图中都落在前景区域），抑制漂浮噪声。
  - **点生成（point generation）**：对现有点进行上采样，新点的位置和参数取最近邻的平均值，逐步增加点云密度以捕获更精细的几何细节。

这一混合策略的因果链条为：**梯度更新提供光度一致性信号→体素缩减和异常值剔除净化几何→点生成提升空间分辨率→新一轮梯度更新在更优几何上优化外观**。消融实验（Table 3）表明，移除该混合策略使PSNR从30.3 dB暴跌至26.6 dB，并产生大量离群点（Figure 8），证明逐步几何细化对稳定收敛不可或缺。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2205_14330/figures/011_Figure_8.jpg]]
*Figure 8: Analysis of Coarse-to-Fine Optimization. We analyze rendering quality with and without the hybrid coarseto-fine training strategy. We observe noticeable outlier points if we train the model without the coarse-to-fine training strategy, validating the proposed approach*

**5. 训练过滤函数**

在训练过程中持续应用一致性检查函数：
$$CC(\boldsymbol{p}^j) = \mathbb{I}( \sum_{i=1}^{N} \mathbb{I}( M_i( \boldsymbol{p}_i^j ) > 0 ) = N )$$
即仅保留在所有 $N$ 个训练视图中均投影到前景掩码内的点。这一简单机制有效抑制了背景区域的虚假几何。消融实验显示关闭过滤使PSNR降至29.1 dB。

### Changed Slots：相对于NeRF的三项根本性替换

| 设计维度 | NeRF基线 | 本方法 | 因果效应 |
|---------|---------|--------|---------|
| **场景表示** | 隐式MLP编码5D辐射场 | 显式3D点云，每点存储球谐系数 | 消除网络前向传播冗余，支持前向映射 |
| **渲染方式** | 体积射线步进（后向映射），每光线数百次MLP评估 | 可微点splatting（前向映射），单次pass合成全图 | 推理速度提升约600倍，训练速度提升约200倍 |
| **训练策略** | 端到端MLP参数优化，无几何更新 | 混合coarse-to-fine：梯度更新+周期性几何细化 | 在无预计算几何的条件下逐步逼近精确表面 |

前两个替换构成了**“表示-渲染”联合转向**：显式点云使前向映射成为可能，而splatting渲染器将前向映射实现为可微计算图。第三个替换解决了点云优化中的几何漂移问题，使方法无需依赖COLMAP等离线几何先验（区别于Pulsar、PBNR等基线）。

### 视频扩展机制

对于多视图视频，方法对每一帧独立训练一个点云模型，但利用帧间连续性进行初始化：计算上一帧模型的多个候选点云（通过随机扰动生成）与当前帧初始点云的Chamfer距离，选择距离最小的候选作为当前帧的初始点云：
$$\mathcal{CD}(S_1, S_2) = \frac{1}{|S_1|} \sum_{x \in S_1} \min_{y \in S_2} \|x-y\|_2^2 + \frac{1}{|S_2|} \sum_{y \in S_2} \min_{x \in S_1} \|x-y\|_2^2$$

这一设计使逐帧训练仅需约30分钟（STNeRF数据集），而STNeRF需50小时，且无需任何显式时序正则化。

### 效率优势的根源

方法的速度优势并非来自单一技巧，而是**表示、渲染、优化三层面的协同压缩**：
- **表示层面**：点云稀疏地分布在物体表面附近，避免了体积表示在空白区域的浪费（Plenoxels虽为显式体积，仍需存储完整稀疏网格，模型达778 MB，而本方法仅9 MB）；
- **渲染层面**：splatting仅计算投影点附近的像素贡献，计算量与点数和图像分辨率线性相关，而非光线密度；
- **优化层面**：混合策略在训练中动态调整点云密度，使计算资源集中于几何复杂区域。

这种协同效应解释了为何方法在PSNR略低于NeRF（30.3 vs 31.01 dB）和Plenoxels（30.3 vs 31.71 dB）的情况下，仍被视为突破性工作——它重新定义了效率-质量的帕累托前沿。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2205_14330/figures/012_Figure_7.jpg]]
*Figure 7: View Ablations. We evaluate the quality of the proposed point-based method and the volumetric NeRF [2020] on the ’Ficus’ scene [2020] with a gradually reduced number of training views. The proposed sparse representation allows for reconstructions with reasonable quality even with as few as 20 views, where NeRF drops by more than 10 dB in PSNR*

## 实验与关键发现

### 核心性能基准

**静态场景新视图合成（Synthetic Blender Dataset）**。在Mildenhall et al. (2020)的合成数据集上，所提方法以3分钟训练、32 fps推理和9 MB模型体积，取得PSNR 30.3 dB、SSIM 0.945、LPIPS 0.078（Table 1）。与NeRF相比，训练速度提升约200倍（~20 h → ~3 min），推理速度提升约600倍（~0.02 fps → 32 fps），而PSNR仅下降约0.7 dB。与当时最快的显式体积方法Plenoxels相比，训练速度快3倍（~10 min → ~3 min），推理速度快2倍（~15 fps → 32 fps），模型体积仅为后者的1/86（778 MB → 9 MB），PSNR差距约1.4 dB（31.71 dB vs 30.3 dB）。这表明点基表示在效率-质量权衡上取得了更优的帕累托前沿：以可接受的质量损失换取数量级的计算和存储增益。

**多视图视频新视图合成（STNeRF Dataset）**。在Zhang et al. (2021)的视频数据集上，所提方法取得PSNR 34.6 dB、SSIM 0.927、LPIPS 0.207，训练仅需30分钟，推理达25 fps，模型大小110 MB（Table 2）。相比之下，STNeRF的PSNR为32.1 dB，训练需50小时，推理仅1/30 fps；NeRF-t的PSNR仅28.9 dB，训练需100小时，推理1/26 fps。所提方法在PSNR上分别高出2.5 dB和5.7 dB，训练速度快100-200倍，推理速度快约750倍。这一优势源于点基渲染的单次前向pass特性，无需为每帧执行昂贵的体积射线步进。

**动态场景（DSC Dataset）**。在Vlasic et al. (2009)的动态场景数据集上，所提方法采用逐帧独立点云训练策略，总训练时间1小时，推理28 fps，总模型体积240 MB（Table 5）。相比STNeRF（86 h训练，1/18 fps推理）、NeRF（75 h，1/15 fps）和NeRF-t（50 h，1/15 fps），训练速度快50-86倍，推理速度快400-500倍。模型体积虽大于基于MLP的方法（因每帧独立存储点云），但仍在可接受范围内。

### 关键消融实验

Table 3系统验证了三个核心组件的贡献（均在Blender数据集上评估）：

1. **球谐函数视角相关建模**：移除球谐系数（即每个点仅存储与视角无关的RGB值）导致PSNR从30.3 dB骤降至27.1 dB，SSIM和LPIPS同步恶化。Figure 5显示，高光区域（如金属材质、镜面反射）出现明显的颜色失真和模糊，验证了视角相关辐射度建模对复杂材质重建的必要性。

2. **混合coarse-to-fine更新策略**：关闭点云几何的逐步细化（包括体素缩减、异常点剔除和点生成）使PSNR降至26.6 dB，降幅达3.7 dB。Figure 8表明，无此策略时点云中出现大量离群点，渲染结果伴随显著噪声和伪影。这说明单纯依赖梯度更新无法有效优化点云几何分布，混合策略通过周期性几何操作维持了点云的结构一致性。

3. **训练过滤函数**：移除一致性检查过滤使PSNR降至29.1 dB（下降1.2 dB），表明在训练过程中持续剔除不一致点有助于抑制噪声积累，保持渲染质量。

### 点云密度与效率权衡

Table 6展示了点云数量对性能的影响。在STNeRF数据集上，点云从15k增至45k时PSNR从32.2 dB提升至34.6 dB（+2.4 dB），但继续增至100k时PSNR反而降至34.2 dB，同时训练时间和模型体积显著增加。这表明45k点为效率-质量最优平衡点：过少的点无法充分表达场景细节，过多的点则引入冗余并可能导致过拟合或优化困难，收益递减。

### 稀疏视角鲁棒性

Figure 7显示，当训练视图数从100降至20时，所提方法的PSNR下降幅度远小于NeRF（NeRF下降超过10 dB）。这一优势源于点基表示的显式几何先验：视觉壳初始化和点云结构本身提供了有效的归纳偏置，在少视图条件下起到正则化作用，而纯隐式MLP表示在数据匮乏时更容易产生严重伪影。

### 效率-质量权衡总结

综合所有实验，所提方法的核心竞争力不在于绝对质量超越所有基线，而在于以可接受的质量代价换取数量级的效率提升。在静态场景上，PSNR虽低于NeRF和Plenoxels约0.7-1.4 dB，但训练和推理速度分别提升200倍和600倍；在视频场景上，PSNR反而超越专用视频方法2.5-5.7 dB，同时保持100倍以上的训练加速。这种效率优势的根本原因在于渲染范式的转变：从“每条光线数百次网络评估”的体积射线步进，变为“单次前向pass完成整幅图像合成”的点基splatting。

### 方法适用边界

需注意以下几点限制：
- 所有实验均在已知相机参数的前提下进行，未涉及相机位姿联合优化。
- 对于动态场景，采用逐帧独立训练策略，未利用帧间时序信息，模型体积随帧数线性增长。
- 点基渲染的质量依赖于点云密度和分布，对极度稀疏或高度遮挡区域的重建能力有限。
- 与基于MLP的方法相比，在极端视角相关效果（如复杂折射）的表达能力可能受限，因为球谐函数的阶数有限。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2205_14330/figures/004_Table_1.jpg]]
*Table 1: Static Novel View Synthesis Evaluation on the Synthetic Blender Dataset. We evaluate the proposed method and comparable baseline approaches for novel view synthesis on the static Blender scenes from [Mildenhall et al. 2020]. The proposed model does not require an extra dataset for pretraining and improves on existing methods in training, inference speed and model size, at cost of only a small reduction in quality. Specifically, although the concurrent Plenoxels [2021a] achieves better quality, our model is two magnitudes smaller than theirs. We also compare here to the Plenoxels_s model from [Yu et al. 2021a] (Plenoxels with smaller volume resolution), which achieves worse rendering quality...*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2205_14330/figures/006_Table_2.jpg]]
*Table 2: Quantitative Evaluation on the STNeRF Dataset. Compared to STNeRF and the NeRF variants suggested in [Zhang et al. 2021], the training speed and inference speed of the proposed method is two orders of magnitude higher*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2205_14330/figures/007_Table_3.jpg]]
*Table 3: Model Ablation Experiments. We evaluate the rendering quality of our method on the Blender dataset [2020] when gradually removing components from the rendering pipeline. Specifically, we ablate the spherical harmonics model per point, the coarse-to-fine strategy, and the filtering function for the training. The experimental results validate that all components contribute to the rendering quality*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2205_14330/figures/013_Table_5.jpg]]
*Table 5: Quantitative Evaluation on the DSC Dataset. We report the training time, rendering speed and the model size required to represent scenes from the DSC[Vlasic et al. 2009] dataset with the proposed method. Note that we train a radiance point cloud for each frame here and we report the total memory consumption*

## 定位与知识库关联

本文的核心贡献在于同时改变了视图合成中的两个关键槽位：**场景表示**从隐式坐标MLP替换为显式可学习点云，**渲染方式**从体积射线步进（后向映射）替换为可微点基splatting（前向映射）。这一双重替换使得训练和推理效率获得数量级提升，同时保持了可比的渲染质量。

### 相对基线方法的本质差异

**相对NeRF（Mildenhall et al., ECCV 2020）**：NeRF将场景编码为MLP权重，渲染时需沿每条光线采样数百点并反复查询网络，这是其速度瓶颈的根源。本文用显式点云存储辐射度（球谐系数），将渲染变为单次前向splatting pass，无需光线步进。这一改变使训练从约20小时降至约3分钟（约400倍），推理从约0.02 fps提升至32 fps（约1600倍）。质量上PSNR略低约0.7 dB（30.3 vs 31.01），但效率优势使其在实时应用中更具实用价值。

**相对Plenoxels（Yu et al., 2022）**：Plenoxels同样采用显式表示（稀疏体素网格+球谐系数），但渲染仍基于体积射线步进。本文的关键差异在于用splatting替代了ray marching，这一前向映射策略使推理速度提升约2倍（32 fps vs 15 fps），模型大小缩减约86倍（9 MB vs 778 MB）。Plenoxels的体素网格需存储大量空区域，而点云表示天然稀疏，仅在表面附近分配容量。

**相对Pulsar（Lassner & Zollhöfer, 2021）和PBNR（Kopanas et al., 2021）**：这两者同样使用点基表示，但存在根本性差异。Pulsar需要COLMAP预计算几何作为输入，且训练耗时数小时；PBNR依赖SfM先验和图像翻译网络，训练也需数小时。本文从视觉壳随机初始化开始，端到端联合优化点位置和外观，无需任何几何先验，训练仅需数分钟。这一差异源于本文的可微splatting渲染器允许梯度直接流向点位置，而Pulsar和PBNR的渲染管线或依赖预计算几何，或梯度路径不完整。

**相对STNeRF和NeRF-t（Zhang et al., 2021）**：在视频新视图合成任务上，本文方法训练快100-200倍（30分钟 vs 50-100小时），推理快约750倍（25 fps vs 1/30 fps），PSNR高出2.5-5.7 dB。关键差异在于本文的帧间初始化策略：使用Chamfer距离选择上一帧最优点云作为下一帧初始，使优化快速收敛，而NeRF变体需从零训练每帧的MLP。

### 知识库挂载点

本文在知识库中的定位是**显式神经渲染**与**可微点基渲染**的交叉节点。它连接了以下知识脉络：

1. **显式神经表示**：与Plenoxels、TensoRF等共享“用显式结构替代MLP”的思路，但本文选择了点云这一更稀疏、更灵活的结构。这为后续3D Gaussian Splatting（Kerbl et al., 2023）将点扩展为3D高斯椭球体提供了直接的方法论基础——3D Gaussian Splatting本质上是本文点基辐射场的“各向异性高斯+更精细优化策略”升级版。

2. **可微点渲染**：本文的可微splatting渲染器（高斯RBF核+前端到后端alpha混合）是可微点渲染在视图合成中的早期成功应用。它证明了前向映射在效率上的根本优势，为后续工作打开了“用可微光栅化替代体积渲染”的技术路线。

3. **球谐视角相关建模**：与Plenoxels共享球谐系数表示视角相关辐射度的做法，本文将其从体素网格迁移到点云上，验证了该表示在不同显式结构上的通用性。

### 适用边界

- **优势场景**：多视图输入充足（如100张训练图像）、场景表面可被点云充分覆盖的静态或逐帧动态场景。在稀疏视角（20视图）下，本文方法PSNR下降幅度远小于NeRF（Figure 7），表现出更强的正则化特性。
- **局限性**：点云表示难以建模体积效应（如烟雾、半透明物体），因为这些场景缺乏明确的表面；点云数量需手动设定，且存在效率-质量权衡（45k点为最优平衡点，继续增加收益递减）；点云初始化依赖前景掩码，对无掩码场景需额外处理。
- **质量边界**：在Blender合成数据集上PSNR约30.3 dB，低于NeRF（31.01 dB）和Plenoxels（31.71 dB），表明纯点基表示在精细几何和视角相关效果的重建精度上仍有提升空间——这一边界后来被3D Gaussian Splatting突破。

### 后续启发

本文的核心启发在于证明了**前向映射渲染对实时视图合成的根本性重要性**。它直接启发了3D Gaussian Splatting，后者将点扩展为3D高斯椭球体，使用各向异性协方差矩阵建模点的空间范围，配合更精细的自适应密度控制策略，在保持实时渲染的同时将PSNR提升至超越NeRF的水平。此外，本文的“逐帧独立点云+Chamfer距离初始化”策略为动态场景的轻量级建模提供了范式，后续工作可在此基础上引入时序一致性约束或可变形点云以进一步提升时间连贯性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Differentiable_Point_Based_Radiance_Fields_for_Efficient_View_Synthesis.pdf]]
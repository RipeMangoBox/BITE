---
title: "ADOP: Approximate Differentiable One-pixel Point Rendering"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/ADOP_Approximate_Differentiable_One_pixel_Point_Rendering.pdf
project_link: null
code_link: "https://github.com/darglein/ADOP"
aliases:
- ADOP
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 可微的单像素点光栅化，通过近似每个像素点的空间梯度，使得原本不可微的离散投影操作变得可微，从而允许优化器调节所有结构及光度输入参数。
primary_logic: 将单像素点渲染的离散化转化为可微的近似操作，使得逆渲染框架能够同时优化点云位置、相机内外参、环境光照及色调映射参数，提高输入一致性，并允许使用更轻量的神经网络实现实时高保真渲染。
claims:
- 结构优化 (SO) 在所有场景中均能降低 VGG 重建损失（Train 降 28%, Playground 降 15%, M60 降 14%, Lighthouse 降 31%）。
- 即使从随机扰动位姿初始化，SO 也能恢复出优于 COLMAP 初始的位姿和渲染质量。
- ADOP 在 RTX 3080 上达到 27 ms 推理时间，比 NeRF++ 快约 6700 倍，比 NPBG 快近 2 倍。
- 加入可微色调映射后，ADOP 能处理曝光差异达 426 倍的不一致输入，消除色斑伪影。
---

# ADOP: Approximate Differentiable One-pixel Point Rendering

> [!tip] 核心洞察
> 将单像素点渲染的离散化转化为可微的近似操作，使得逆渲染框架能够同时优化点云位置、相机内外参、环境光照及色调映射参数，提高输入一致性，并允许使用更轻量的神经网络实现实时高保真渲染。

| 字段 | 内容 |
|------|------|
| 中文题名 | ADOP：近似可微单像素点渲染 |
| 英文题名 | ADOP: Approximate Differentiable One-pixel Point Rendering |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://github.com/darglein/ADOP) · [arXiv](http://arxiv.org/abs/1412.6980) · [Code](https://github.com/darglein/ADOP") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ADOP |
| Dataset | Tanks and Temples, 1920×1080 点云 |

> [!tip] 效果简介
> - Tanks and Temples (平均) 上，推理时间 (ms) 27 vs NeRF++: ~183000; SVS: ~2400; NPBG: 50 (约 6700 倍快于 NeRF++)。
> - 1920×1080 点云 (10.3M 点) 上，前向渲染时间 (ms) 3.65 (4 层) / 3.08 (含随机丢弃) vs Pulsar: 209; Synsin: 7342 (快约两个数量级)。

## 概要

多视角三维重建与神经渲染中，初始点云、相机位姿及光度参数的不一致性导致合成视图出现模糊、重影和亮度偏差。ADOP 提出一种近似可微单像素点渲染框架，通过离散投影的空间梯度近似使整个逆渲染管线可微，从而联合优化点位置、相机内外参、镜头畸变、环境光照及曝光白平衡等参数。渲染管线由可微光栅化器、轻量 4 层 U‑Net 神经渲染器与可微物理相机色调映射器构成。在 Tanks and Temples 等场景上，ADOP 以 27 ms 推理时间达到实时性能，比 NeRF++ 快约 6700 倍，比 NPBG 快近 2 倍；结构优化使 VGG 重建损失降低 14–31%，并能从随机扰动位姿恢复优于 COLMAP 初始的渲染质量。该方法属于点基逆渲染路线，关键差异在于单像素可微光栅化与全参数联合优化，为高保真实时视图合成提供了高效替代方案。

## 核心方法与创新机理

### 一、问题瓶颈与设计动机

基于代理几何的神经渲染（如点云或网格）在视图合成中面临一个根本性瓶颈：初始三维重建（点云位置、相机位姿、镜头畸变）与光度参数（曝光时间、白平衡、渐晕）之间的不一致性。这种不一致导致渲染图像出现模糊、重影和亮度跳变，限制了高保真视图合成的上限。传统方法将点云和相机参数视为固定输入，仅优化神经网络的权重，无法从根本上消除这些结构误差。

ADOP 的核心洞察在于：将单像素点渲染的离散化操作转化为可微的近似操作，使得原本不可微的投影-光栅化管线能够反向传播梯度，从而允许优化器同时调节所有结构和光度参数。这一设计使得逆渲染框架能够将不一致的初始重建“拉”向一致，同时允许使用更轻量的神经网络实现实时高保真渲染。

### 二、流水线整体架构

ADOP 的流水线由三个级联的可微模块组成（图2），形成从三维场景表示到最终 LDR 图像的完整可微前向通路：

1. **可微光栅化器**：将具有学习特征的点云和神经环境图渲染为多分辨率稀疏神经图像。
2. **神经渲染器（U-Net）**：填充空洞、合成 HDR 输出图像。
3. **可微色调映射器**：利用学习到的光度参数将 HDR 图像转换为 LDR，实现曝光、白平衡等物理调节。

三个模块之间的因果关系清晰：光栅化器输出的稀疏图像质量直接决定 U-Net 的填充难度和最终细节保真度；U-Net 的 HDR 输出为色调映射器提供线性辐照度，使色调映射器能够应用物理相机模型；色调映射器的梯度则反向传播至 U-Net 和光栅化器，驱动结构和光度参数的联合优化。

### 三、核心创新：可微单像素点光栅化

#### 3.1 基本渲染函数

光栅化器在不同分辨率层 $l$ 上输出神经图像 $\mathrm{I}_{l}$：

$$\mathrm{I}_{l} = \Phi_{l}( C, R, t, x, n, E, \tau )$$

其中 $C$ 为相机内参模型，$(R, t)$ 为相机位姿，$x$ 为点云位置，$n$ 为法线，$E$ 为环境图，$\tau$ 为神经纹理。投影变换将世界点映射至图像空间：

$$P_{l}(C, R, t, x) = \frac{1}{2^{l}} C( R x + t )$$

离散像素坐标通过舍入操作获得：

$$p_{i} = \big\lfloor P_{l}(C, R, t, x_{i}) \big\rceil$$

这一舍入操作是光栅化不可微的根源。

#### 3.2 空间梯度近似：从离散到可微的关键转换

ADOP 的核心创新在于不修改前向渲染（仍保持单像素点的高效性），而是在反向传播时近似空间梯度。对于图像坐标 $(u,v)$ 处的偏导数，采用相邻像素强度变化的均值进行近似：

$$\left.\frac{\partial I}{\partial u}\right|_{p=(u,v)} \approx \frac{1}{2}\left( \left.\frac{\Delta I}{\Delta u}\right|_{p=(u-1,v)} + \left.\frac{\Delta I}{\Delta u}\right|_{p=(u+1,v)} \right)$$

其中 $\frac{\Delta I}{\Delta u}$ 表示将投影点平移一个像素后引起的强度变化。根据目标像素的深度和背景情况，该变化分为四种情形：

$$\frac{\Delta I}{\Delta u}\bigg|_{p=(i,j)} = \begin{cases} \tau(u,v) - I_{l}(i,j), & \Lambda_{l,u,v} = \emptyset \\ 0, & z > (1+\alpha)\mathrm{min}_{z}(u,v) \\ \tau(u,v) - I_{l}(i,j), & z(1+\alpha) < \mathrm{min}_{z}(u,v) \\ \frac{|\Lambda_{i,j}| I_{l}(i,j) + \tau(u,v)}{1+|\Lambda_{i,j}|} - I_{l}(i,j), & \text{else} \end{cases}$$

四种情形的物理含义分别为：(1) 目标像素为空，直接使用点颜色填充；(2) 新点深度远大于已有最小深度（被遮挡），不产生变化；(3) 新点深度远小于已有最小深度（遮挡已有内容），替换颜色；(4) 深度接近，与新点混合。模糊深度测试的阈值 $\alpha$ 控制混合边界（图3，$\alpha=0.01$ 时产生平滑过渡）。

这一梯度近似方案的关键优势在于：它完全保留了前向渲染的单像素高效性（无需渲染多像素斑点），同时在反向传播中提供了对点位置、相机参数的平滑梯度信号，使得结构优化成为可能。

#### 3.3 随机点丢弃：效率与质量的权衡

在低分辨率层，大量点可能通过模糊深度测试，导致过绘制和计算浪费。ADOP 引入随机点丢弃机制，根据点的屏幕空间半径 $r_{screen}$ 和均匀随机数 $\beta$ 决定是否丢弃：

$$\frac{r_{screen}}{\sqrt{1-\beta}} > \frac{1}{\gamma}$$

参数 $\gamma$ 控制丢弃强度（所有数据集设为 1.5）。该机制大约将混合点数减半，光栅化时间降低 15-25%，且无感知质量损失（图9）。

### 四、Changed Slot 1：输入优化替代固定参数

传统点基神经渲染（如 NPBG）将点云位置、相机位姿和畸变系数视为固定输入，仅优化神经纹理和网络权重。ADOP 的关键改变在于将所有结构参数设为可优化变量：

- **点云位置**：通过空间梯度反向传播直接优化三维坐标。
- **相机位姿**：在 SE(3) 李代数切空间中进行更新：

$$(R', t') = \exp(x) \cdot (R, t)$$

其中 $\exp$ 为指数映射，$x$ 为六维增量参数。

- **镜头畸变**：作为相机内参模型的一部分参与优化。

这一改变的根本意义在于：即使初始重建存在显著误差（如 COLMAP 位姿不精确、LiDAR-相机外参未对齐），结构优化（Structure Optimization, SO）也能在训练过程中自动修正这些误差（图7）。实验表明，即使从随机扰动位姿初始化，SO 也能恢复出优于 COLMAP 初始的渲染质量。

### 五、Changed Slot 2：可微物理相机模型替代固定色调映射

传统神经渲染通常假设输入图像具有一致的曝光和白平衡，或仅做简单的逐图像归一化。ADOP 引入完整的可微物理相机模型，包含四个子组件：

**曝光校正**：根据估计的曝光值 $\mathrm{EV}_i$ 调整 HDR 图像亮度：

$$I_{e} = \frac{I_{HDR}}{2^{\mathrm{EV}_{i}}}$$

曝光值从图像元数据初始化：

$$\mathrm{EV}_{i} = \log_{2}\left(\frac{f_{i}^{2}}{t_{i}}\right) + \log_{2}\left(\frac{S_{i}}{100}\right) - \overline{\mathrm{EV}}$$

其中 $f_i$ 为光圈值，$t_i$ 为曝光时间，$S_i$ 为 ISO。

**渐晕校正**：用像素到渐晕中心的径向距离 $r$ 的多项式模拟强度衰减：

$$I_{v} = I_{w} \cdot \left(1 + a_{2} r^{2} + a_{4} r^{4} + a_{6} r^{6}\right)$$

**相机响应函数（CRF）**：通过一维纹理查找表将线性 HDR 值转换为非线性 LDR：

$$I_{ldr} = R(I_{v})$$

训练时使用泄露响应函数避免过曝/欠曝区域的梯度消失：

$$R_{t}(x) = \begin{cases} \alpha x, & x < 0 \\ R(x), & 0 \leq x \leq 1 \\ \frac{-\alpha}{\sqrt{x}} + \alpha + 1, & 1 < x \end{cases}$$

这一设计的实际价值在于：ADOP 能处理曝光差异达 426 倍的不一致输入，消除因曝光变化导致的色斑伪影（图14）。在推理时，学习到的色调映射器可替换为电影色调映射，获得更自然的视觉效果（图15）。

### 六、Changed Slot 3：简化的神经渲染网络

相比 NPBG 使用的 5 层 U-Net，ADOP 采用 4 层 U-Net。这一简化的依据在于：当结构优化和光度校准提供了更一致的光栅化输入后，深度网络的需求降低。实验表明，5 层网络在部分场景出现过拟合（训练损失低而测试损失高），4 层网络在保持良好填充能力的同时提高了效率（图8）。

为支持 HDR 渲染，网络移除了批归一化层（避免丢失传感器辐照度的绝对尺度），并在场景辐照度范围较大（>1:400）时对神经点描述符使用对数缩放，避免优化器收敛问题。

### 七、训练与推理路径

**训练路径**：给定一组 RGB 图像和初始三维重建（点云、相机位姿、稀疏模型），前向传播依次通过可微光栅化器、U-Net 和色调映射器生成 LDR 图像。损失函数使用 VGG 感知损失（相比 L1 或 MSE 显著提高清晰度和细节，图5）。梯度反向传播通过色调映射器、U-Net 和空间梯度近似，同时更新神经纹理、网络权重、点云位置、相机参数和光度参数。

**推理路径**：对新视角，仅执行前向传播。可选的测试细化（Test Refinement, TR）步骤可进一步优化该特定视角的渲染质量。在 RTX 3080 上，推理时间仅 27 ms（1920×1080 分辨率），比 NeRF++ 快约 6700 倍，比 NPBG 快近 2 倍（表2）。

![[assets/figures/papers/paper_list_l40_https_github_com_darglein_ADOP/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our point-based HDR neural rendering pipeline. The scene, consisting of a textured point cloud and an environment map, is rasterized into a set of sparse neural images in multiple resolutions. A deep neural network reconstructs an HDR image, which is then converted to LDR by a differentiable physically-based tonemapper. All parameters in the rectangular boxes, as well as the neural network can be optimized simultaneously during training*

![[assets/figures/papers/paper_list_l40_https_github_com_darglein_ADOP/figures/021_Figure_16.jpg]]
*Figure 16: The initial camera pose estimates of the SLAM-System are slightly misaligned w.r.t. the LiDAR point cloud. Reprojecting the pixel color of several source views into a target view produces ghosting artifacts (center row). Our system is able to optimize the camera poses resulting in almost pixel perfect reprojections (bottom row)*

## 实验与关键发现

ADOP 的实验评估围绕三个核心维度展开：视图合成质量与速度的权衡、各组件贡献的消融验证，以及方法在极端条件下的鲁棒性边界。评估场景来自 Tanks and Temples 数据集（M60、Train、Playground、Lighthouse）及作者自采数据（Kemenate、Boat、Office），涵盖固定曝光与大幅变化曝光（Boat 场景曝光差异达 426 倍）两类条件，点云规模从 9.7M 到 34.1M 点不等（Table 1）。

![[assets/figures/papers/paper_list_l40_https_github_com_darglein_ADOP/figures/005_Table_1.jpg]]
*Table 1: Overview of our evaluation scenes. M60, Train, Playground, and Lighthouse are from the Tanks and Temples dataset. Kemenate and Boat were captured by the authors, Office was provided by (anonymous)*

### 推理效率：实时性能的突破

ADOP 在推理速度上展现出数量级优势。在 Tanks and Temples 四个场景上取平均，ADOP 在 RTX 3080 上的单帧推理时间仅为 **27 ms**，对比方法中：**NPBG**（Aliev et al., 2020）为 50 ms，**SVS**（Riegler and Koltun, 2021）在半分辨率下约 2400 ms，**NeRF++**（Zhang et al., 2020）约 183000 ms（~3 分钟/帧）。ADOP 比 NeRF++ 快约 **6700 倍**，比 NPBG 快近 2 倍（Table 2）。这一差距根源于“单像素点渲染”的设计选择——每个点仅占据一个像素，避免了基于多像素斑点的可微渲染（如 Pulsar 的 209 ms、Synsin 的 7342 ms）中随分辨率增长的过绘制开销。在 1920×1080 分辨率、10.3M 点的前向渲染专项测试中，ADOP 的 4 层 U-Net 配置仅需 **3.65 ms**，启用随机点丢弃后进一步降至 **3.08 ms**（Table 5），比 Pulsar 快约两个数量级。

![[assets/figures/papers/paper_list_l40_https_github_com_darglein_ADOP/figures/006_Table_2.jpg]]
*Table 2: Timings for novel view synthesis averaged over the four tanks and temples scenes, and approximate training times. For SVS and Nerf++ we used the provided standard parameters for training*

### 消融实验：三个关键组件的因果贡献

Table 3 的定量消融揭示了环境图（Env）、可微色调映射（TM）和结构优化（SO）三个组件的场景依赖性贡献。以 VGG 感知损失为统一度量：

![[assets/figures/papers/paper_list_l40_https_github_com_darglein_ADOP/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative ablation study of the results presented in Table 3*

- **Train 场景**：完整 ADOP（含 Env + TM + SO）的 VGG 损失相比基线降低 **28%**。
- **Playground 场景**：降低 **15%**。
- **M60 场景**：降低 **14%**——该场景以固定曝光拍摄，因此色调映射的贡献天然较小，但结构优化仍带来显著收益。
- **Lighthouse 场景**：降低 **31%**，受益最为显著。

Fig. 6 提供了 Train 场景的定性对比：无环境图时背景区域出现明显伪影，无色调映射时亮度不一致导致色斑，无结构优化时几何错位引发重影。三个组件叠加后，合成图像与真值的高度一致性验证了各模块的因果必要性。

结构优化的鲁棒性在 Fig. 7 中得到进一步压力测试：将 COLMAP 初始位姿施加随机扰动后，无 SO 的模型产生严重重影和模糊；启用 SO 后，模型在 400 个训练 epoch 内恢复出**优于 COLMAP 初始**的渲染质量。这表明可微光栅化提供的梯度信号能够有效校正初始重建中的位姿误差，而非仅仅依赖初始化的质量。

### 网络深度与过拟合边界

U-Net 层数的消融（Fig. 8）揭示了神经渲染器容量与泛化的权衡。5 层 U-Net 虽然增强了空洞填充能力，但在部分场景上出现训练损失低而测试损失高的过拟合现象；4 层 U-Net 在保持足够填充质量的同时，提升了推理效率并降低了过拟合风险。这一发现支持了 ADOP 的轻量网络设计选择：当输入参数本身可优化时，网络无需承担全部重建负担，较浅的网络反而泛化更好。

### 损失函数选择：感知质量 vs. 像素指标

Fig. 5 对比了 L1、MSE 和 VGG 感知损失对训练结果的影响。尽管 L1 损失在某些像素级指标上占优，VGG 损失训练的模型在图像清晰度和细节保真度上显著优于前者。这一现象与逆渲染任务的特性一致：当优化目标同时涉及几何、光度参数和网络权重时，感知损失提供的特征空间梯度有助于避免像素空间中的局部极小，产生更锐利的合成结果。

### 随机点丢弃的效率增益

随机点丢弃机制（Eq. (12)，参数 $\gamma=1.5$）大约将参与混合的点数减半，光栅化效率提升 15-25%，且无感知质量损失（Fig. 9）。这一机制利用世界空间半径和均匀随机数 $\beta$ 控制过绘制，在小分辨率层尤为有效——该层通常有数百个点通过模糊深度测试，丢弃机制在不牺牲覆盖的前提下减少了冗余计算。

### HDR 色调映射：消除曝光不一致伪影

Boat 数据集以自动曝光拍摄，曝光值（EV）变化剧烈（Fig. 13）。无色调映射和曝光校正时，合成视图出现大面积色斑伪影；启用可微色调映射后，模型能估计每张训练图像的曝光值 $EV_i$（Eq. (14)-(15)），将 HDR 重建结果校正至统一曝光，消除伪影（Fig. 14）。在推理阶段，学习到的色调映射可替换为电影级色调映射，产生更自然的视觉效果（Fig. 15），展示了物理相机模型与神经网络解耦的灵活性。

### 与主流方法的定性比较

Fig. 10 展示了 Train、Playground、M60 三个场景上 ADOP 与 NPBG、SVS、NeRF++ 的视觉对比。ADOP 在细节保留和几何一致性上均表现优异，尤其在 Playground 的复杂几何结构和 Train 的细长杆件区域，ADOP 避免了 NPBG 的模糊和 SVS（半分辨率）的锯齿。需注意 SVS 因内存限制仅在半分辨率下评估，这一公平性说明在 Table 2 中亦有标注。

### 失败模式与适用边界

尽管 ADOP 在多数场景表现强劲，其方法设计隐含若干边界条件：

1. **静态场景假设**：当前系统无法处理动态对象，所有优化参数（点位置、位姿、光度参数）均假设场景在拍摄期间保持不变。
2. **点云密度依赖**：放大视点时，若原始点云密度不足，神经渲染可能产生模糊（Fig. 12 展示了视点外推的极限情况）。作者将此列为开放问题，提出未来可通过动态生成新点并插值神经描述符来改善。
3. **初始重建完整性**：大面积缺失区域（如 COLMAP 未能重建的弱纹理表面）仍难以逼真填补，神经渲染器的空洞填充能力受限于训练数据的覆盖范围。
4. **时序一致性缺失**：系统未引入时域组件，在视频序列中可能出现闪烁，这是实时神经渲染走向视频应用需解决的关键问题。

综上，ADOP 的实验证据链完整支撑了其核心主张：通过可微单像素点光栅化实现的结构与光度联合优化，在保持实时推理的前提下，显著提升了基于代理的神经渲染质量，并在曝光不一致、位姿不精确等实际退化条件下展现出强鲁棒性。

![[assets/figures/papers/paper_list_l40_https_github_com_darglein_ADOP/figures/003_Figure_3.jpg]]
*Figure 3: One-pixel point rendering with fuzzy depth testing and threshold*

## 定位与知识库关联

ADOP 的核心定位是**将点基神经渲染从“固定输入的前馈合成”升级为“可微逆渲染框架”**，其改变的关键槽位（changed slot）并非渲染网络的容量或架构，而是**光栅化阶段的可微性**与**光度模型的物理化**。相对于现有基线，这一改变体现在三个层面。

### 1. 相对基线的本质差异

**相对于 NPBG**（Aliev et al., 2020）：NPBG 使用 OpenGL 点渲染，其投影与遮挡判定不可微，因此点云位置、相机位姿、曝光参数在训练期间完全固定。ADOP 将这一不可微光栅化替换为**可微单像素点光栅化**（通过空间梯度近似实现反向传播），使得优化器可以调节所有结构参数（点位置、相机内外参、镜头畸变）和光度参数（曝光、白平衡、渐晕、相机响应函数）。这一改变直接解决了 NPBG 中“初始重建不一致导致渲染模糊/重影”的瓶颈。同时，ADOP 将 NPBG 的 5 层 U-Net 简化为 4 层，在提高效率的同时减少过拟合（Fig. 8 显示 5 层网络在部分场景测试损失反而升高）。

**相对于 NeRF++**（Zhang et al., 2020）：NeRF++ 属于体素神经辐射场方法，其渲染需要对每条射线进行密集采样和网络查询，推理速度极慢。ADOP 采用点基表示，单像素光栅化只需一次投影与混合，在 RTX 3080 上推理时间仅 27 ms，比 NeRF++ 快约 6700 倍（Table 2）。二者改变的槽位本质不同：NeRF++ 以网络容量换取视图质量，ADOP 以显式几何与可微光栅化换取实时性。

**相对于 SVS**（Riegler and Koltun, 2021）：SVS 使用网格/点混合表示进行视图合成，但其光栅化基于多像素斑点，且不支持输入参数优化。ADOP 的单像素光栅化在 1920×1080 分辨率下前向渲染仅需 3.65 ms，比 Pulsar（209 ms）和 Synsin（7342 ms）快约两个数量级（Table 5）。关键差异在于 ADOP 通过随机点丢弃（Eq. 12, γ=1.5）控制过绘制，将混合点数减半而不损失感知质量（Fig. 9）。

### 2. 知识库挂载点

ADOP 在知识库中的挂载点可定位为 **“可微点渲染”与“神经逆渲染”的交汇节点**。

- **上游依赖**：ADOP 的可微光栅化梯度近似（Eq. 10-11）与已有的可微点溅射技术（如 Kopanas et al., 2021; Yifan et al., 2019）共享核心思想——通过扰动投影位置计算空间梯度。但 ADOP 将这一思想从“多像素斑点”压缩到“单像素点”，并通过模糊深度测试（α=0.01, Fig. 3）处理遮挡边界，形成了独特的效率-可微性平衡点。

- **下游延伸**：ADOP 的可微色调映射器（Sec 3.3）将物理相机模型（曝光值 EV_i 从 EXIF 元数据初始化，Eq. 15；渐晕多项式模型，Eq. 16；相机响应函数查找表，Eq. 17）集成到训练循环中，使得框架能处理曝光差异达 426 倍的不一致输入（Fig. 14）。这一设计为后续的“非受控捕获条件下的神经渲染”提供了可复用的光度模块。

- **训练范式**：ADOP 使用 VGG 感知损失训练，相比 L1 或 MSE 显著提高图像清晰度（Fig. 5），这一选择与 NPBG 等工作的实践一致，但 ADOP 证明了在可微光栅化框架下感知损失同样有效。

### 3. 适用边界

ADOP 的适用边界由以下条件界定：

- **场景静止假设**：当前系统无法处理动态对象，所有结构优化（点位置、位姿）依赖于多视图静态一致性。
- **初始点云完整性依赖**：结构优化（SO）可以从随机扰动位姿恢复（Fig. 7），但大面积缺失区域仍难以逼真填补，神经渲染的填充能力受限于 U-Net 的感受野和训练数据覆盖。
- **放大视点的模糊**：当视点放大导致原始点云密度不足时，单像素光栅化会产生稀疏图像，神经渲染可能产生模糊（论文明确列为限制）。
- **时域一致性缺失**：未引入时域组件，视频序列中可能出现闪烁。

### 4. 后续启发

ADOP 为知识库提供了两个明确的延伸方向：

1. **动态点生成与描述符插值**：论文提出的开放问题——在放大视图中动态生成新点并赋以插值后的神经描述符——指向“可微点云上采样”与“神经纹理超分辨率”的结合，这需要将光栅化器的梯度进一步传播到点生成模块。

2. **时域神经点渲染**：加入时域组件以减轻闪烁并支持动态场景，这需要将 ADOP 的单帧逆渲染框架扩展为时域一致的优化问题，可能涉及光流或变形场的可微建模。

3. **更轻量的实时部署**：ADOP 已在 RTX 3080 上达到 27 ms 推理（含测试细化 TR），随机丢弃进一步降低光栅化时间约 20%（Fig. 9），这为移动端或 AR/VR 设备的实时高保真视图合成提供了工程基线。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/ADOP_Approximate_Differentiable_One_pixel_Point_Rendering.pdf]]
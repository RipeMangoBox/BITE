---
title: Efficient Neural Radiance Fields for Interactive Free-viewpoint Video
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Efficient_Neural_Radiance_Fields_for_Interactive_Free_viewpoint_Video.pdf
project_link: null
code_link: null
aliases:
- ENRFIFVV
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于级联成本体积的深度引导采样策略，通过预测粗略场景几何，仅在表面附近采样少量点，从而大幅减少渲染所需的采样数量。
primary_logic: 将多视图立体的显式几何估计整合到可泛化神经辐射场中，利用深度概率分布指导采样，在保持渲染质量的同时，将采样点数从数百降至个位数，实现60倍以上的渲染加速。
claims:
- 在DTU数据集上，深度引导采样在仅使用2个采样点时PSNR达27.45，而无深度引导时PSNR骤降至17.75，证明表面邻近采样在极低采样数下仍能保持渲染质量。
- 级联成本体积设计将渲染帧率从9.749 FPS提升至20.31 FPS，在不损失质量的情况下加速了深度推理。
- 所提方法在多个基准数据集上的渲染速度比先前可泛化方法至少快60倍（例如静态场景中达到25.29 FPS，动态场景中达到40.21 FPS）。
- 在无深度监督的条件下，仅通过RGB损失即可端到端学习出合理的深度预测，并在动态场景上实现实时渲染（40.21 FPS）与高质量重建（ZJU-MoCap PSNR 31.21）。
---

# Efficient Neural Radiance Fields for Interactive Free-viewpoint Video

> [!tip] 核心洞察
> 将多视图立体的显式几何估计整合到可泛化神经辐射场中，利用深度概率分布指导采样，在保持渲染质量的同时，将采样点数从数百降至个位数，实现60倍以上的渲染加速。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高效神经辐射场实现交互式自由视点视频 |
| 英文题名 | Efficient Neural Radiance Fields for Interactive Free-viewpoint Video |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://zju3dv.github.io/enerf/) |
| Topic | #topic/graphics_rendering_materials #topic/graphics_animation_interaction #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ENeRF |
| Dataset | NeRF Synthetic, DTU, ZJU-MoCap, Real Forward-facing |

> [!tip] 效果简介
> - NeRF Synthetic (Hotdog) 上，PSNR↑ 34.64 vs 27.70 (IBRNet) (+6.94)。
> - DTU (scan #1) 上，PSNR↑ 28.85 vs 28.40 (MVSNeRF) (+0.45)。
> - ZJU-MoCap (dynamic) 上，PSNR↑ / FPS 31.21 / 40.21 vs ~28.5 (IBRNet_gen) / <1 (>2.7 / >39)。

## 概要

现有的可泛化神经辐射场方法在渲染时需在每条射线上密集采样大量3D点，导致渲染速度极慢，无法支持交互式自由视点视频应用。本文提出 **ENeRF**，核心思路是将多视图立体的显式几何估计引入可泛化辐射场：通过构建**级联成本体积**预测粗糙场景深度，再利用深度概率分布**在表面附近进行引导采样**，将每射线采样点数从数百降至个位数。该方法在保持渲染质量的同时，渲染速度比先前可泛化方法**至少快60倍**——静态场景达25.29 FPS，动态场景达40.21 FPS；在DTU、NeRF Synthetic及ZJU-MoCap等基准上取得有竞争力的PSNR/SSIM指标。整个系统仅需RGB监督即可端到端训练，无需深度真值。

## 核心方法与创新机理

### 问题的唯一瓶颈

现有的可泛化神经辐射场方法（如IBRNet、MVSNeRF、PixelNeRF）面临一个根本性的渲染效率瓶颈：它们在每条射线上需要在近远平面之间均匀采样大量3D点（通常128个），包括大量位于空白区域的无效采样。这些无效采样不仅浪费计算资源，还严重拖慢渲染速度，使得此类方法无法支持交互式自由视点视频应用。ENeRF的核心洞察在于：如果能够预先获得场景的粗略几何信息，就可以将采样限制在物体表面附近，从而将采样点数从数百降至个位数，实现数量级的渲染加速。

### 核心创新机制：深度引导采样

ENeRF的创新本质是将多视图立体（MVS）的显式几何估计整合到可泛化神经辐射场框架中。具体而言，系统通过构建级联成本体积来预测目标视点的深度概率分布，并利用该分布指导体积渲染的采样过程。这一设计形成了一个因果链路：

**级联成本体积 → 深度概率分布 → 表面区间估计 → 稀疏采样 → 高效渲染**

该链路的关键在于：深度预测不仅提供了“在哪儿采样”的几何先验，还通过深度标准差量化了预测的不确定性，从而自适应地调整采样区间的宽度。这使ENeRF在仅使用2～8个采样点时仍能保持渲染质量，而传统均匀采样策略在如此低的采样数下会完全失效。

### 三个关键Changed Slots

**Changed Slot 1：采样策略（从均匀密集采样到深度引导稀疏采样）**

基线方法在每条射线的近远平面之间均匀采样128个点，其中大部分位于空白区域。ENeRF利用预测的表面深度区间 $\hat{\mathrm{U}}(u,v)$ 进行采样，该区间由深度均值 $\hat{\mathrm{L}}(u,v)$ 和标准差 $\hat{\mathrm{S}}(u,v)$ 确定：

$$\hat{\mathrm{U}}(u,v) = [ \hat{\mathrm{L}}(u,v) - \lambda \hat{\mathrm{S}}(u,v), \hat{\mathrm{L}}(u,v) + \lambda \hat{\mathrm{S}}(u,v) ]$$

其中 $\lambda$ 为超参数（文中设为1）。深度均值由深度概率分布加权求得：

$$\hat{\mathrm{L}}(u,v) = \sum_{i=1}^D \mathrm{P}_i(u,v) \mathrm{L}_i(u,v)$$

深度标准差则量化了预测的不确定性：

$$\hat{\mathrm{S}}(u,v) = \sqrt{ \sum_{i=1}^D \mathrm{P}_i(u,v) ( \mathrm{L}_i(u,v) - \hat{\mathrm{L}}(u,v) )^2 }$$

这一设计使得采样点集中在表面附近的高密度区域，从根本上消除了空白区域的无效计算。实验证据（Table 4）表明：在仅使用2个采样点时，深度引导采样的PSNR达27.45，而无深度引导时骤降至17.75，证明表面邻近采样在极低采样数下仍能保持渲染质量。

![[assets/figures/papers/paper_list_l50_https_zju3dv_github_io_enerf/figures/009_Table_4.jpg]]
*Table 4: Quantitative ablation of the design choices on the DTU dataset. “Depth-gui.” and “Depth-sup.” are “Depthguided” and “Depth-supervision”, respectively. The rendering resolution here is set to 512 × 640*

**Changed Slot 2：深度预测模块（从无显式几何到级联成本体积）**

基线可泛化方法（如PixelNeRF）直接从图像特征推断辐射场，缺乏显式的场景几何推理。ENeRF引入了由粗到精的级联成本体积构建流程，作为深度预测和3D特征提取的核心模块。

该模块的工作流程如下：

1. **多尺度图像特征提取**：使用2D UNet从输入视图提取多尺度特征图 $F_{i,1}$，为后续成本体积构建提供特征基础。

2. **级联成本体积构建**：在目标视点的视锥体内，由粗到精地构建成本体积。对于每个深度假设平面 $z$，通过单应变换将输入视图的特征图扭曲到目标视图：

$$\mathrm{H}_i(z) = \mathrm{K}_i \mathrm{R}_i \Big( \mathrm{I} + \frac{ ( \mathrm{R}_i^{-1} \mathrm{t}_i - \mathrm{R}_t^{-1} \mathrm{t}_t ) \mathrm{a}^T \mathrm{R}_t }{ z } \Big) \mathrm{R}_t^{-1} \mathrm{K}_t^{-1}$$

$$F_i^w(u,v,z) = F_{i,1}( \mathrm{H}_i(z) [u,v,1]^T )$$

其中 $\mathrm{K}_i, \mathrm{R}_i, \mathrm{t}_i$ 为输入视图的相机内参、旋转和平移，$\mathrm{a}^T$ 为目标视点的主轴方向。

3. **3D CNNs处理**：将扭曲后的多视图特征通过3D卷积网络处理，输出深度概率分布 $P$ 和3D特征体积。级联设计使得粗级别的深度预测可以缩小精细级别的深度搜索范围，从而在保持精度的同时提高效率。

级联设计的因果效应在Table 4中得到验证：级联成本体积将渲染帧率从非级联的9.749 FPS提升至20.31 FPS，在不损失质量的情况下加速了深度推理。

**Changed Slot 3：辐射场特征输入（从单一图像特征到图像+体素双特征）**

基线方法（如PixelNeRF）仅使用像素对齐的图像特征来推断辐射场，缺乏对3D空间结构的显式建模。ENeRF同时使用两种互补特征：

- **图像对齐特征 $f_{\mathrm{img}}$**：通过IBRNet的加权池化算子 $\psi$ 聚合多视图投影得到的像素特征，提供视角相关的表观信息。
- **体素对齐特征 $f_{\mathrm{voxel}}$**：从3D特征体积中通过三线性插值提取，提供视角无关的几何结构信息。

这两种特征被送入MLP $\phi$ 以联合推断密度和点特征：

$$f_p, \sigma = \phi( f_{\mathrm{img}}, f_{\mathrm{voxel}} )$$

双特征设计的因果逻辑在于：$f_{\mathrm{voxel}}$ 编码了场景的3D几何结构（由级联成本体积提取），为密度预测提供强几何先验；$f_{\mathrm{img}}$ 则保留了视角相关的纹理细节，为颜色预测提供表观信息。两者的互补性使得ENeRF即使在稀疏采样下也能准确推断场景的几何和表观。

### 完整的渲染管线

ENeRF的推理管线由以下模块按顺序构成，模块间存在明确的因果依赖关系：

**模块1：多尺度图像特征提取**
- 输入：多视图RGB图像
- 输出：多尺度特征图
- 因果作用：为级联成本体积提供特征基础，为辐射场解码提供像素对齐特征

**模块2：级联成本体积构建与处理**
- 输入：多尺度特征图、相机参数、深度范围（由SfM提供）
- 处理：由粗到精构建成本体积 → 3D CNNs → 深度概率分布 + 3D特征体积
- 输出：深度均值 $\hat{\mathrm{L}}$、深度标准差 $\hat{\mathrm{S}}$、3D特征体积
- 因果作用：深度分布指导后续采样，3D特征体积提供体素对齐特征

**模块3：深度引导采样区间确定**
- 输入：深度均值 $\hat{\mathrm{L}}$、深度标准差 $\hat{\mathrm{S}}$
- 计算：$\hat{\mathrm{U}} = [\hat{\mathrm{L}} - \lambda \hat{\mathrm{S}}, \hat{\mathrm{L}} + \lambda \hat{\mathrm{S}}]$
- 输出：每条射线的表面搜索区间
- 因果作用：将采样点从128个降至2～8个，实现60倍以上加速

**模块4：图像特征聚合**
- 输入：多视图图像特征、采样点3D坐标
- 处理：将采样点投影到各输入视图 → 提取像素特征 → 加权池化 $\psi$
- 输出：图像对齐特征 $f_{\mathrm{img}}$
- 因果作用：提供视角相关的表观信息

**模块5：体素特征查询**
- 输入：采样点3D坐标、3D特征体积
- 处理：坐标变换 → 三线性插值
- 输出：体素对齐特征 $f_{\mathrm{voxel}}$
- 因果作用：提供视角无关的几何结构信息

**模块6：密度与点特征预测**
- 输入：$f_{\mathrm{img}}$、$f_{\mathrm{voxel}}$
- MLP $\phi$：$f_p, \sigma = \phi( f_{\mathrm{img}}, f_{\mathrm{voxel}} )$
- 输出：体积密度 $\sigma$、点特征 $f_p$
- 因果作用：$\sigma$ 用于体积渲染的透明度累积，$f_p$ 用于颜色预测

**模块7：颜色混合权重预测**
- 输入：点特征 $f_p$、源视图特征 $f_i$、方向差 $\Delta \mathrm{d}_i$
- MLP $\varphi$：$w_i = \varphi( f_p, f_i, \Delta \mathrm{d}_i )$
- 输出：各源视图的混合权重 $w_i$
- 因果作用：通过softmax加权平均得到采样点颜色

$$\hat{\mathbf{c}}_p = \sum_{i=1}^N \frac{ \exp(w_i) \mathbf{c}_i }{ \sum_{j=1}^N \exp(w_j) }$$

**模块8：体积渲染**
- 输入：各采样点的密度 $\sigma$ 和颜色 $\hat{\mathbf{c}}_p$
- 处理：沿射线累积透射率加权的颜色
- 输出：像素颜色 $\hat{\mathbf{C}}$
- 因果作用：生成最终渲染图像

### 训练策略与损失函数

ENeRF的所有模块均端到端训练，仅使用RGB图像监督，无需深度真值。训练损失由两部分组成：

**均方误差损失**（主损失）：
$$\mathcal{L}_{mse} = \frac{1}{N_r} \sum_{i=1}^{N_r} \lVert \hat{\mathbf{C}}_i - \mathbf{C}_i \rVert_2^2$$

**感知损失**（辅助损失，提升细节质量）：
$$\mathcal{L}_{perc} = \frac{1}{N_i} \sum_{i=1}^{N_i} \Vert \Phi(\hat{\mathbf{I}}_i) - \Phi(\mathbf{I}_i) \Vert$$

其中 $\Phi$ 为预训练网络的感知特征提取器。消融实验（Supplementary）表明，感知损失将DTU上的LPIPS从0.106降至0.091，验证了其对细节质量的提升作用。

值得注意的是，Table 4的消融实验显示：额外添加深度监督并没有提升渲染质量（PSNR 27.11 vs 27.45），说明端到端的RGB监督已足以驱动级联成本体积学习出合理的深度预测。这一发现简化了训练流程，避免了深度真值的依赖。

### 动态场景的实时渲染适配

对于动态场景，ENeRF将每一帧视为独立的静态场景，直接应用泛化模型而不利用时序信息。这种设计保证了与可泛化基线的公平对比，同时实现了实时渲染（40.21 FPS）。Supplementary中进一步引入了bound_mask技术，通过限制有效渲染区域将动态场景的帧率从30.57 FPS提升至40.21 FPS，在不损失质量的前提下进一步加速。

### 方法边界条件

ENeRF的深度引导采样依赖于级联成本体积能够预测出合理的深度分布。当场景包含大量透明物体、镜面反射或细薄结构时，成本体积的匹配质量可能下降，导致深度预测不准确，进而影响采样区间的有效性。此外，深度范围需要由SfM算法提供，在稀疏视角或纹理缺失场景中，SfM的深度范围估计可能不可靠，影响成本体积的构建质量。这些边界条件需要在应用时根据具体场景进行验证。

![[assets/figures/papers/paper_list_l50_https_zju3dv_github_io_enerf/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the proposed approach. Given multi-view images of a static scene or a dynamic scene at one frame, we first construct the cascade cost volume, which is processed to output the 3D feature volume and the coarse scene geometry (represented by depth and confidence maps). The estimated geometry guides us to sample around the surface, which significantly accelerates the volume rendering process. Also, the 3D feature volume provides rich geometry-aware information for generalizable radiance fields construction. All network components are trained end-to-end using only RGB images*

![[assets/figures/papers/paper_list_l50_https_zju3dv_github_io_enerf/figures/013_Figure_6.jpg]]
*Figure 6: Illustration of compositional ENeRF. (a) To implement compositional ENeRF, we estimate 3D bounding boxes of foreground and background entities, and use ENeRF to separately predict their radiance fields, which are then composited to the full scene’s radiance field. (b) MVS-based depth estimator tends to give smooth predictions that are inaccurate on the edge between the foreground and background. (c) By separately predicting the depth of foreground and background entities, we can sample points around accurate surfaces, thereby enabling NeRF to represent the sharp depth discontinuities*

## 实验与关键发现

ENeRF 的核心实验设计围绕一个关键命题展开：**深度引导采样能否在极低采样数下保持渲染质量，同时将可泛化神经辐射场的渲染速度提升至交互帧率？** 实验覆盖静态场景泛化、逐场景优化、动态场景实时渲染三个维度，并辅以充分的消融分析来拆解各模块的因果贡献。

### 动态场景：实时渲染与质量的双重突破

动态场景是 ENeRF 最核心的应用场景。在 ZJU-MoCap 数据集上，ENeRF 在**不进行任何逐场景微调**（训练时间为 0）的情况下，取得了 **PSNR 31.21 / SSIM 0.970 / LPIPS 0.041** 的表现，同时渲染速度达到 **40.21 FPS**（Table 1）。这一速度相比 IBRNet 泛化版本（IBRNet_gen）的不足 1 FPS 提升了超过 40 倍，且质量也显著领先（IBRNet_gen 的 PSNR 约 28.5）。值得注意的是，ENeRF 在 DynamicCap 数据集上同样实现了 40.21 FPS 的实时渲染与 PSNR 26.29 的合成质量，验证了该方法在不同动态场景下的鲁棒性。

![[assets/figures/papers/paper_list_l50_https_zju3dv_github_io_enerf/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on dynamic scenes. The time within parentheses represents the training time of the model on the scene. "0" means that we directly apply the model to the scene without additional fine-tuning. All methods are evaluated on the same machine to report the speed of rendering a 512 × 512 image. NB denotes NeuralBody*

与需要逐场景训练的 NeuralBody（NB）相比，ENeRF 在 ZJU-MoCap 上的 PSNR 略低（31.21 vs NB 的 31.42），但 NB 需要约 14 小时的训练时间，而 ENeRF 无需任何微调即可直接泛化。这一对比揭示了 ENeRF 在**效率与质量权衡**上的优势：以微小的质量代价换取免训练部署和实时渲染能力。

### 静态场景泛化：60 倍加速的实证

在静态场景的泛化设置下（Table 2），ENeRF 在 NeRF Synthetic、DTU 和 Real Forward-facing 三个基准上均展现出与逐场景优化方法可比的质量，同时渲染速度达到 **25.29 FPS**。相比之下，IBRNet 和 MVSNeRF 等先前可泛化方法的渲染速度仅约 0.4 FPS，ENeRF 实现了 **至少 60 倍的加速**（Abstract, Table 2）。

![[assets/figures/papers/paper_list_l50_https_zju3dv_github_io_enerf/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of static scenes. “Generalization” means that the model is not additionally fine-tuned. “Per-scene optimization” means that the model is trained or fine-tuned on the target scene. All methods are evaluated on an RTX 3090 GPU to report the speed of rendering a 512 × 512 image. The results of baselines are borrowed from MVSNeRF*

具体而言，在 NeRF Synthetic 的 Hotdog 场景上，ENeRF 取得了 PSNR 34.64，相比 IBRNet 的 27.70 提升了 **+6.94 dB**（Table 8）。在 DTU 数据集上，ENeRF 的 PSNR 为 27.61，与 MVSNeRF 的 28.40 相比仅低 0.79 dB，但渲染速度提升了两个数量级。在 Real Forward-facing 的 Fortress 场景中，ENeRF 的 PSNR 为 29.58，略低于经 1 小时微调的 IBRNet_ft-1h（30.34），但 SSIM 略高（0.940 vs 0.937），且无需任何微调（Table 9）。

### 深度预测质量：隐式几何学习的有效性

尽管 ENeRF 从未接收深度监督，仅通过 RGB 损失端到端训练，其在 DTU 数据集上的深度预测质量却显著优于有深度监督的 MVSNet（Table 3）。ENeRF 的参考视图绝对误差仅为 **3.80 mm**，而 MVSNet 为 4.24 mm。这一反直觉的结果表明，**级联成本体积在辐射场训练的梯度驱动下，能够自发地学习出高质量的深度估计**，无需额外的深度真值信号。这也为深度引导采样的可靠性提供了基础保障。

![[assets/figures/papers/paper_list_l50_https_zju3dv_github_io_enerf/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison of depth results on the DTU dataset. We follow the experimental setting of MVS-NeRF and borrow the baseline results from it. MVSNet is trained with depth supervision while other methods are trained with RGB supervision. Abs err means the absolute error. Acc(X) metric is the percentage of pixels whose error is less than X mm*

### 消融实验：因果链路的逐一验证

消融实验（Table 4）是理解 ENeRF 各模块因果贡献的关键证据链。

**深度引导采样是核心性能瓶颈。** 当采样点数降至 2 时，有深度引导的 ENeRF 仍能维持 PSNR 27.45，而去除深度引导后 PSNR 骤降至 **17.75**（降幅近 10 dB）。这直接证明了表面邻近采样策略在极低采样数下的决定性作用——传统的均匀采样在 2 个采样点下几乎无法捕获任何有效表面信息，而深度引导使得每个采样点都落在高概率表面区间内。

**级联成本体积提升了推理效率。** 将级联设计替换为非级联版本后，渲染帧率从 20.31 FPS 降至 9.749 FPS（Table 4），说明由粗到精的成本体积构建在保证深度精度的同时，显著降低了计算开销。这一设计是 ENeRF 实现实时渲染的关键工程支撑。

**深度监督是冗余的。** 额外引入深度监督后，PSNR 为 27.11，反而不及无深度监督的 27.45（Table 4）。这表明 RGB 损失已能为深度预测提供足够的梯度信号，显式深度监督可能引入与渲染目标不一致的偏差。

**动态场景的 bound_mask 加速。** 在动态场景中，应用 bound_mask 将渲染帧率从 30.57 FPS 提升至 40.21 FPS（Supplementary, Sec. 1.2）。该技术利用人体包围盒裁剪空白区域的采样，进一步压缩了无效计算。

**渲染头设计选择。** 采用混合权重预测颜色的渲染头（blending weights）相比直接预测 RGB 的渲染头，PSNR 从 26.77 提升至 27.88，SSIM 从 0.95 提升至 0.96（Supplementary）。这说明利用多视图颜色混合而非直接回归，能更好地保持视图一致性。

**感知损失的辅助作用。** 在 MSE 损失基础上加入感知损失，将 DTU 上的 LPIPS 从 0.106 降至 0.091（Supplementary），改善了合成图像的感知质量，但对 PSNR 的影响有限。

### 适用边界与潜在局限

尽管 ENeRF 在速度和泛化能力上取得了显著突破，其设计仍存在若干边界条件。首先，深度引导采样的有效性依赖于级联成本体积能够预测出合理的深度分布——在纹理稀疏或重复纹理区域，深度预测的不确定性增大，可能导致采样区间偏离真实表面。其次，ENeRF 的动态场景实验基于 ZJU-MoCap 和 DynamicCap 等受控的人体运动数据，对于更复杂的非刚性形变（如衣物飘动、流体）或剧烈拓扑变化场景，深度预测的稳定性需要进一步验证。此外，ENeRF 的泛化能力依赖于训练时覆盖的多场景多样性，对于与训练分布差异过大的场景类型，渲染质量可能出现退化。

**公平性说明：** 所有速度对比均在同一台 RTX 3090 GPU 上以 512×512 分辨率进行；泛化设置下模型未在目标场景做任何微调；动态场景中直接逐帧应用泛化模型，不利用时序信息，保证了与可泛化基线的公平对比。

## 定位与知识库关联

ENeRF 的核心定位是在**可泛化神经辐射场**（Generalizable NeRF）框架中引入**显式的、端到端学习的场景几何估计**，以此作为辐射场采样的引导信号。与现有可泛化方法相比，它改变的关键 slot 并非辐射场解码器本身，而是**采样策略**——从“全深度范围均匀密集采样”转变为“基于预测表面区间的稀疏深度引导采样”。这一改变使得每条射线的采样点数从上百个降至 2～8 个，从而在保持渲染质量的同时实现了 60 倍以上的渲染加速。

### 相对于 Baseline 的本质差异

**IBRNet**（Wang et al., 2021b）和 **PixelNeRF**（Yu et al., 2021b）代表了可泛化神经渲染的一条主流路线：它们从输入视图中提取像素对齐的图像特征，然后在目标射线上密集采样 3D 点，通过 MLP 推断颜色和密度。这类方法缺乏对场景几何的显式建模，导致大量采样点落在空白区域，计算资源被严重浪费。ENeRF 在这一流程中**插入了一个级联成本体积模块**，该模块由多视图特征通过单应变换构建而成，经 3D CNN 处理后同时输出：(1) 深度概率分布，用于定位表面位置；(2) 3D 特征体积，为辐射场提供体素对齐的几何感知特征。这一插入点正是知识库中“多视图立体几何估计”与“神经辐射场渲染”两个技术簇的交汇处。

**MVSNeRF**（Chen et al., 2021）同样构建了成本体积，但其设计目标是将成本体积特征直接用于辐射场的条件输入，并未利用深度估计来指导采样——它仍然沿袭了密集采样的范式。ENeRF 的关键突破在于将深度概率分布**转化为采样区间的约束**：通过期望深度 $\hat{\mathrm{L}}(u,v)$ 和标准差 $\hat{\mathrm{S}}(u,v)$ 定义表面搜索区间 $\hat{\mathrm{U}}(u,v) = [\hat{\mathrm{L}} - \lambda \hat{\mathrm{S}}, \hat{\mathrm{L}} + \lambda \hat{\mathrm{S}}]$（Eq. 5），使采样点集中在表面附近。这一设计使得深度估计不再仅仅是辅助特征，而是**直接决定了渲染效率的上限**。

与逐场景优化的 **NeRF**（Mildenhall et al., 2020）相比，ENeRF 保持了可泛化方法的优势——无需对每个新场景进行长时间训练即可生成新视角，同时将渲染速度从 NeRF 的秒级提升到交互式帧率（静态场景 25.29 FPS，动态场景 40.21 FPS）。

### 知识库挂载点

ENeRF 在知识库中的主要挂载点包括：

1. **多视图立体匹配（MVS）与神经渲染的融合**：继承自 MVSNeRF 的成本体积构建范式，但将 MVS 的几何估计能力从“辅助特征”升级为“采样引导器”。这一定位使得 ENeRF 可以受益于 MVS 领域的后续进展（如更高效的成本体积构建、更精确的深度估计网络），同时保持与神经渲染框架的兼容性。

2. **可泛化辐射场的效率优化**：在 IBRNet 的聚合框架（加权池化算子 $\psi$）基础上，ENeRF 证明了通过几何引导可以大幅减少采样点数量而不损失质量。这为后续工作提供了一个明确的方向：**几何先验是加速可泛化 NeRF 的关键杠杆**。

3. **无深度监督的几何学习**：消融实验（Table 4）表明，额外的深度监督并未提升渲染质量（PSNR 27.11 vs 27.45），说明仅靠 RGB 损失即可端到端学习出对渲染有用的深度估计。这一发现将 ENeRF 与需要深度真值训练的 MVS 方法（如 MVSNet）区分开来，降低了数据获取门槛。

### 适用边界与条件

ENeRF 的深度引导采样策略依赖于**成本体积能够预测出合理的深度分布**。当输入视图数量不足、基线过窄或场景纹理缺失时，深度估计的不确定性增大（$\hat{\mathrm{S}}$ 变大），采样区间会相应扩大，加速效果会打折扣。在动态场景中，ENeRF 对每帧独立处理，不利用时序信息，这意味着它无法从运动线索中获益，但也因此避免了时序建模的计算开销。

在 Real Forward-facing 场景（Table 9, Fortress）中，ENeRF 的 PSNR 略低于经过 1 小时微调的 IBRNet（29.58 vs 30.34），表明在视角变化受限的前向场景中，深度引导的优势被部分削弱——因为均匀采样在窄深度范围内固有的低效性不那么突出。

### 后续启发与延伸方向

ENeRF 揭示了一条清晰的技术路径：**用轻量级几何估计换取渲染效率的指数级提升**。这一范式对后续工作的启发包括：

- **更高效的几何估计模块**：级联成本体积虽然比非级联版本更快（20.31 FPS vs 9.749 FPS），但仍是整个流程的计算瓶颈。用更轻量的深度预测网络（如单目深度估计）替代成本体积，可能进一步降低推理成本，但需要权衡多视图几何的一致性。

- **时序扩展**：当前 ENeRF 独立处理动态场景的每一帧，未利用帧间连续性。将深度引导采样与时序融合（如光流引导的采样区间传播）结合，有望在动态场景中进一步减少采样点或提升深度估计的稳定性。

- **混合采样策略**：对于深度不确定性高的区域（如镜面反射、透明物体），可以回退到均匀采样或增加采样点密度。ENeRF 的标准差 $\hat{\mathrm{S}}$ 天然提供了这种不确定性度量，为自适应采样提供了接口。

- **与 3D 重建的结合**：ENeRF 预测的深度图在 DTU 数据集上表现出竞争力（Table 3, Abs err 3.80），暗示其几何估计能力可以服务于渲染之外的下游任务，如快速 3D 重建或深度补全。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Efficient_Neural_Radiance_Fields_for_Interactive_Free_viewpoint_Video.pdf]]
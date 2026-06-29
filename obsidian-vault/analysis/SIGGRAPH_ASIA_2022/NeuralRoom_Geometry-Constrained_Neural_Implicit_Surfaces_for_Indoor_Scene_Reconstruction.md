---
title: "NeuralRoom: Geometry-Constrained Neural Implicit Surfaces for Indoor Scene Reconstruction"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/NeuralRoom_Geometry_Constrained_Neural_Implicit_Surfaces_for_Indoor_Scene_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- NeuralRoom
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入可靠的几何先验（MVS距离先验与不确定度过滤的法向先验）以及扰动-残差约束，限制隐式表面的空间变化范围，从而缓解形状-辐射歧义。
primary_logic: 深度估计与法向估计具有互补性：MVS在纹理丰富区域精度高，而法向估计网络在纹理缺乏区域表现好；将两者结合为几何先验引导神经渲染，可以有效克服室内重建中的歧义。
claims:
- 在消融研究中，完整方法（Full）取得了最低的Overall误差0.024，相比仅使用颜色损失的Base（0.106）大幅降低。
- 在ScanNet数据集上，NeuralRoom的F-score（66.756）和Overall（0.055）均显著优于同期最佳基线Atlas（F-score 61.871, Overall 0.070）。
- 法向先验是最关键的损失项，单独添加即能将Overall误差从0.106降至0.054，显著改善完整性和精度。
- 距离先验提供了精确的三维点，单独使用时将Overall误差从0.106降至0.072，提升了重建细节的精度。
---

# NeuralRoom: Geometry-Constrained Neural Implicit Surfaces for Indoor Scene Reconstruction

> [!tip] 核心洞察
> 深度估计与法向估计具有互补性：MVS在纹理丰富区域精度高，而法向估计网络在纹理缺乏区域表现好；将两者结合为几何先验引导神经渲染，可以有效克服室内重建中的歧义。

| 字段 | 内容 |
|------|------|
| 中文题名 | NeuralRoom：面向室内场景重建的几何约束神经隐式表面 |
| 英文题名 | NeuralRoom: Geometry-Constrained Neural Implicit Surfaces for Indoor Scene Reconstruction |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2210.06853) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NeuralRoom |
| Dataset | ScanNet |

> [!tip] 效果简介
> - ScanNet (8个测试场景) 上，F-score↑ 66.756 vs 61.871 (Atlas) (+4.885)；Overall↓ 0.055 vs 0.070 (Atlas) (-0.015)；Precision↑ 68.347 vs 67.957 (Atlas) (+0.390)。

## 概要

**问题**：室内场景重建面临形状-辐射歧义（shape-radiance ambiguity）——神经隐式表面在弱纹理区域即使渲染图像与输入一致，仍会收敛到错误的几何形状，导致传统多视图立体和现有神经渲染方法在室内场景中失效。

**方法**：NeuralRoom 通过引入互补的几何先验来约束隐式表面的空间变化范围，从而缓解歧义。具体而言，利用 COLMAP MVS 在纹理丰富区域提供精确的距离先验，利用法向估计网络在弱纹理区域提供可靠的法向先验（以不确定度过滤），并将两者结合为损失函数引导体渲染训练；同时提出扰动-残差约束（平滑深度项与法向一致性项）来强制局部表面连续。

**主要结果**：在 ScanNet 数据集上，NeuralRoom 的 F-score 达到 66.756，Overall 误差 0.055，显著优于同期最佳基线 Atlas（F-score 61.871，Overall 0.070）。消融实验表明，法向先验是最关键的损失项（单独将 Overall 从 0.106 降至 0.054），距离先验提供精确三维点（降至 0.072），两者互补并结合残差约束后完整方法达到 Overall 0.024。

**方法定位**：NeuralRoom 在神经隐式表面重建管线中，将原本仅依赖光度一致性的训练范式，替换为“MVS 距离先验 + 不确定度过滤法向先验 + 扰动-残差局部平滑”的几何约束框架，属于将经典多视图几何先验融入可微渲染的混合重建方法。

## 核心方法与创新机理

### 1. 问题本质：室内场景重建中的形状-辐射歧义

室内场景重建的核心瓶颈在于**形状-辐射歧义**（shape-radiance ambiguity）。神经隐式表面方法（如 NeuS、Unisurf、VolSDF）通过体渲染优化符号距离函数（SDF）和辐射场，在单物体重建上表现优异，但在室内场景中却常常收敛到错误表面：渲染图像可以与输入一致，但重建几何却完全错误。其根本原因在于，室内场景存在大量弱纹理区域（白墙、天花板、地板），这些区域的光度一致性信号极弱，导致优化过程缺乏足够的几何约束，SDF 的零等值面可以在保持渲染颜色不变的情况下发生大幅偏移。

### 2. 核心洞察：深度先验与法向先验的互补性

NeuralRoom 的核心洞察在于利用**深度估计与法向估计的互补特性**来约束隐式表面。具体而言：
- **MVS 深度估计**（COLMAP）在纹理丰富区域和边缘处精度高，但在弱纹理区域会失效或产生空洞；
- **法向估计网络**（UncertSurfaceNormal）在平坦弱纹理区域能够给出准确的法向，但在纹理丰富区域精度有限。

将两者结合为几何先验，可以覆盖室内场景的不同区域（Figure 3 清晰展示了这种分工：距离先验约束纹理丰富区域和边缘，法向先验约束平坦弱纹理区域），从而有效限制隐式表面的空间变化范围，缓解形状-辐射歧义。

### 3. 方法框架与模块顺序

NeuralRoom 系统由两大部分构成（Figure 4）：**几何先验获取** 和 **NeuralRoom 渲染器**。完整流程如下：

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2210_06853/figures/004_Figure_4.jpg]]
*Figure 4: Method overview. The goal of our system is to reconstruct indoor scenes directly from RGB images with known camera parameters. The system consists of two parts. First, we use the multiview stereo method [Schonberger and Frahm 2016] and the normal estimate network [Bae et al. 2021] to acquire the geometry prior. The distance prior acquired from MVS ensures the accuracy of texture-rich and edge areas, while the normal prior ensures the completeness of the texture-less region. Then, we use these geometry prior and RGB images to guide the optimization of the NeuralRoom module, which is a volume rendering-based neural surface reconstruction method. In addition, in the NeuralRoom module, we propo...*

#### 3.1 图像预处理

输入 RGB 图像序列及已知相机参数后，首先使用 **Laplacian 滤波器进行模糊检测**，筛选出清晰帧用于后续处理，避免运动模糊对重建质量的影响。

#### 3.2 距离先验获取

运行 **COLMAP MVS** 获取每视图的稀疏深度图，经过几何一致性过滤和 3 像素腐蚀后，将其转换为归一化的距离先验。对于像素 $\mathbf{p}$，其对应的 3D 世界坐标通过重投影获得：

$$X_i(\mathbf{p}) = T_i^{-1} K_i^{-1} D_i^{MVS}(\mathbf{p}) \tilde{\mathbf{p}}$$

距离先验定义为相机中心到 3D 点的归一化距离：

$$D_i(\mathbf{p}) = \| K_i^{-1} D_i^{MVS}(\mathbf{p}) \tilde{\mathbf{p}} \| / s$$

其中 $s$ 为归一化因子。这一先验提供了精确的 3D 点位置约束，确保纹理丰富区域的重建精度。

#### 3.3 法向先验获取

使用 **UncertSurfaceNormal**（Bae et al., 2021）估计每像素的法向及不确定度。利用不确定度均值进行过滤，仅保留高置信度的法向估计。这一过滤机制至关重要：法向估计网络在弱纹理区域的不确定度低（估计可靠），而在纹理边缘处不确定度高（估计不可靠），因此过滤后的法向先验恰好作用于 MVS 失效的平坦区域，形成互补。

#### 3.4 NeuralRoom 渲染器

渲染器包含两个 MLP：
- **几何 MLP** $f(x)$：将 3D 点映射为 SDF 值，表面由零等值面定义：

$$S = \{ x \in \mathbb{R}^3 \mid f(x) = 0 \}$$

- **颜色 MLP** $c(x, v)$：将 3D 点 $x$ 和视线方向 $v$ 映射为颜色。

沿光线的体渲染过程如下：在每条光线上采样 $n$ 个点，对于第 $i$ 个采样点 $x_i$，其不透明度 $\alpha_i$ 由 SDF 值通过可学习的 sigmoid 函数 $\Phi_s$ 导出：

$$\alpha_i = \max\left(\frac{\Phi_s(f(x_i)) - \Phi_s(f(x_{i+1}))}{\Phi_s(f(x_i))}, 0\right)$$

累积透射率 $M_i = \prod_{j=1}^{i-1} (1 - \alpha_j)$，渲染颜色和深度分别为：

$$\hat{C}(\mathbf{r}) = \sum_{i=1}^{n} M_i \alpha_i c(x_i, v)$$

$$\hat{D}(\mathbf{r}) = \sum_{i=1}^{n} M_i \alpha_i t_i$$

其中 $t_i$ 为采样点沿光线的深度值。

#### 3.5 训练损失函数

总损失函数由四项组成：

$$\mathcal{L} = \mathcal{L}_{\text{color}} + \mathcal{L}_{\text{prior}} + \mathcal{L}_{\text{res}} + \mathcal{L}_{\text{Eikonal}}$$

- **颜色损失** $\mathcal{L}_{\text{color}}$：渲染颜色与输入图像之间的 L1 损失，提供基础的光度一致性约束。
- **先验损失** $\mathcal{L}_{\text{prior}}$：包含距离先验损失和法向先验损失，将渲染深度/法向约束到几何先验附近。
- **残差损失** $\mathcal{L}_{\text{res}}$：本文提出的扰动-残差约束，包含两项：
  - **平滑深度损失** $\mathcal{L}_{\text{smooth}_D}$：对光线上的采样点施加微小扰动后重新渲染深度，约束扰动前后的深度一致性：

  $$\mathcal{L}_{\text{smooth}_D} = \frac{1}{k}\sum_{k} \text{SmoothL1}(\hat{D}_k, \hat{D}_k^{\text{pert}})$$

  - **法向一致性损失** $\mathcal{L}_{\text{consist}_N}$：约束扰动前后的渲染法向一致。
- **Eikonal 损失** $\mathcal{L}_{\text{Eikonal}}$：标准 SDF 正则项，约束梯度范数接近 1。

#### 3.6 网格提取与后处理

训练完成后，使用 Marching Cubes 从 SDF 中提取粗糙网格。随后通过光线追踪获得各视角的深度图，利用 **TSDF 融合** 生成最终的 3D 网格模型。这一后处理步骤进一步提升了重建的完整性和表面质量。

### 4. 关键创新槽位与因果机制

相较于仅依赖颜色损失的基线方法，NeuralRoom 在两个关键槽位上进行了创新：

#### 槽位一：几何约束方式

**基线**：仅依赖光度一致性（渲染损失），在弱纹理区域缺乏有效约束。

**NeuralRoom**：添加 MVS 距离先验损失和不确定度过滤的法向先验损失。因果机制如下：
- 距离先验为纹理丰富区域提供精确的 3D 锚点，限制 SDF 零等值面在这些区域的空间偏移范围；
- 法向先验为弱纹理区域提供表面朝向约束，防止 SDF 在这些区域产生错误的凹凸或空洞；
- 两者互补覆盖室内场景的不同特征区域，共同将隐式表面的优化空间从“任意可能表面”压缩到“与几何先验一致的表面”。

#### 槽位二：局部平滑约束

**基线**：无显式局部几何正则，仅靠 MLP 的隐式平滑先验。

**NeuralRoom**：引入扰动-残差约束。因果机制如下：
- 当 SDF 零等值面存在不连续或断裂时（Figure 6 所示两种情况），对采样点施加微小扰动会导致渲染深度发生剧烈跳变；
- 平滑深度损失惩罚这种跳变，迫使表面在局部保持连续；
- 法向一致性损失进一步约束扰动前后的法向一致，防止表面出现尖锐的虚假褶皱。

### 5. 训练与推理路径

**训练路径**：
1. 预处理选定清晰帧；
2. 离线计算距离先验（COLMAP MVS）和法向先验（UncertSurfaceNormal）；
3. 在选定的场景边界框内采样光线，每条光线采样 64 个粗采样点 + 64 个细采样点；
4. 前向传播几何 MLP（8 层）和颜色 MLP（4 层），通过体渲染获得颜色、深度和法向；
5. 计算四项损失并反向传播，联合优化两个 MLP 的参数。

**推理路径**：
1. 在训练收敛的 SDF 场上运行 Marching Cubes 提取粗糙网格；
2. 对各视角进行光线追踪获得深度图；
3. TSDF 融合生成最终网格。

训练配置：单张 RTX 2080Ti，约 9.6 GB 显存，训练时间约 16 小时。

### 6. 关键公式变量含义总结

| 符号 | 含义 |
|------|------|
| $f(x)$ | 几何 MLP 输出的 SDF 值 |
| $c(x, v)$ | 颜色 MLP 输出的辐射值 |
| $\Phi_s$ | 可学习的 sigmoid 函数，将 SDF 映射为密度 |
| $\alpha_i$ | 第 $i$ 个采样点的离散不透明度 |
| $M_i$ | 累积透射率 |
| $\hat{C}(\mathbf{r})$ | 沿光线 $\mathbf{r}$ 的渲染颜色 |
| $\hat{D}(\mathbf{r})$ | 沿光线 $\mathbf{r}$ 的渲染深度 |
| $D_i^{MVS}(\mathbf{p})$ | COLMAP 估计的像素 $\mathbf{p}$ 的深度值 |
| $D_i(\mathbf{p})$ | 归一化距离先验 |
| $\mathcal{L}_{\text{smooth}_D}$ | 平滑深度损失，约束扰动前后的深度一致性 |

### 7. 方法边界条件

- **相机位姿依赖**：方法假设相机位姿已知且准确，实际使用 COLMAP 提供的位姿。当位姿误差较大时，几何先验与渲染器之间的配准会出现偏差，导致重建质量显著下降。
- **先验质量依赖**：距离先验和法向先验的质量直接影响最终结果。COLMAP 在极端弱纹理或重复纹理场景下可能产生错误深度，法向估计网络在光照复杂区域可能失效。
- **场景规模限制**：MLP 的容量和计算开销限制了场景规模，目前适用于房间级场景，扩展到更大场景需要更高效的表示方法。
- **表面分离困难**：当两个法向相同且接近的表面缺乏正确的距离先验时（Figure 11 右），扰动-残差约束可能过度平滑，错误地合并两个表面。

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2210_06853/figures/001_Figure_1.jpg]]
*Figure 1: We present a system called NeuralRoom for reconstructing a room-sized indoor scene from 2D images. There are many texture-less regions in indoor scenes, making conventional multiview stereo methods fail in reconstruction. The implicit neural representation method has recently become a promising reconstruction method due to its simplicity and high reconstruction quality. However, shape-radiance ambiguity makes it unable to reconstruct indoor scenes well. NeuralRoom effectively integrates normal and depth information to overcome ambiguity, which guarantees reconstruction details and completeness*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2210_06853/figures/017_Figure_12.jpg]]
*Figure 12: The improvement of reconstruction quality of different reconstruction algorithms by our proposed NeuralRoom system*

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2210_06853/figures/002_Figure_2.jpg]]
*Figure 2: Inherent shape-radiance ambiguity. For each set of results, the first row shows the reconstruction results. The second row shows rendering results from the implicit neural representation. State-of-the-art methods [Oechsle et al. 2021; Wang et al. 2021b; Yariv et al. 2021] can yield impressive high-quality reconstruction of a single object, while they often yield unsatisfactory reconstruction and rendering results for indoor scenes. Optimization of implicit neural representations easily falls into a local optimum, which will result in an incorrect reconstruction or even fail in reconstruction*

## 实验与关键发现

### 核心定量结果

NeuralRoom 在 ScanNet 数据集的 8 个测试场景上进行了系统评估，与多类基线方法进行了比较，包括传统 MVS 方法（COLMAP、ACMP）、学习型深度估计方法（ESTDepth、3DVNet）以及端到端体素重建方法（Atlas、NeuralRecon）。所有方法均使用相同的相机位姿和图像输入，评价指标为标准 3D 重建指标（Precision/Recall/F-score 和 Accuracy/Completion/Overall），由官方工具计算。

**Table 3** 展示了主要定量对比结果。NeuralRoom 在所有指标上均优于同期最佳基线 Atlas：

- **F-score**: NeuralRoom 达到 **66.756**，相比 Atlas 的 61.871 提升 **+4.885**，表明重建结果在精度和完整性之间取得了更好的平衡。
- **Overall 误差**: NeuralRoom 为 **0.055**，相比 Atlas 的 0.070 降低 **-0.015**（降幅约 21%），说明整体重建误差显著减小。
- **Precision**: NeuralRoom 达到 **68.347**，略高于 Atlas 的 67.957（+0.390），保持了较高的细节精度。
- **Recall**: NeuralRoom 为 **65.237**，明显优于 Atlas 的 56.741（+8.496），表明在纹理缺失区域的完整性有大幅提升。

与 COLMAP（F-score 56.399, Overall 0.097）等传统方法相比，NeuralRoom 的优势更为显著，Overall 误差降低了约 43%。学习型方法 ESTDepth 和 3DVNet 的 F-score 分别为 42.317 和 50.111，远低于 NeuralRoom，反映出仅依赖单目或多视图深度估计难以处理室内场景的弱纹理区域。NeuralRecon 的 F-score 为 52.762，虽然具备实时增量重建能力，但完整性不足。

**Figure 7** 的定性对比进一步印证了定量结果：NeuralRoom 在视觉感知上展现出与 Atlas 相似的场景完整性，同时在细节保留上优于其他算法，尤其在墙壁、地板等大面积弱纹理区域能够恢复出连续平滑的表面。

### 先验质量验证

几何先验的质量直接决定了 NeuralRoom 的重建上限。**Table 1** 和 **Table 2** 分别评估了 COLMAP 深度图和法向估计的精度。

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2210_06853/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of the acquired normal map. The filtered normal maps are with a _50 extension*

- **深度先验（Table 1）**: COLMAP 在纹理丰富区域能够提供准确的深度估计，但在弱纹理区域存在缺失和噪声。通过几何一致性过滤和 3 像素腐蚀后，深度图保留了高置信度的稀疏点，为 NeuralRoom 提供了可靠的 3D 锚点。
- **法向先验（Table 2）**: UncertSurfaceNormal 估计的法向图在平坦区域精度较高，通过不确定度均值过滤（标记为 `_50` 扩展）后，法向的平均角度误差显著降低，确保只有高置信度的法向参与训练。**Figure 5** 可视化了过滤前后的差异：不确定度图中高亮区域（不可靠法向）被剔除，保留的法向与真值高度一致。

### 消融实验：各损失项的因果贡献

**Table 4** 和 **Figure 9** 在一个无边界框的简单场景（Scene0801_00）上进行了系统的消融实验，逐项验证各损失函数的作用。该消融是支撑论文核心主张的决定性证据。

| 配置 | Overall ↓ | Accuracy ↓ | Completion ↓ | Precision ↑ | Recall ↑ | F-score ↑ |
|------|-----------|------------|--------------|-------------|----------|-----------|
| Base（仅颜色损失） | 0.106 | 0.087 | 0.124 | 63.264 | 55.467 | 59.109 |
| Base + Distance prior | 0.072 | 0.059 | 0.085 | 66.952 | 59.271 | 62.878 |
| Base + Normal prior | **0.054** | 0.046 | 0.062 | 68.896 | 62.818 | 65.717 |
| Base + Prior（两者） | 0.041 | 0.035 | 0.047 | 70.912 | 64.801 | 67.719 |
| Full（+扰动-残差） | **0.024** | 0.020 | 0.028 | 73.018 | 68.983 | 70.943 |

**关键发现**：

1. **法向先验是最关键的损失项**：单独添加法向先验将 Overall 从 0.106 降至 0.054（降幅 49%），远优于单独添加距离先验（降至 0.072）。这证实了在室内弱纹理区域，法向约束对缓解形状-辐射歧义至关重要。论文明确指出“normal prior is the most important term”。

2. **距离先验提供精确 3D 点**：单独添加距离先验将 Overall 降至 0.072，主要提升了 Precision（从 63.264 到 66.952），说明 MVS 点云有效改善了纹理丰富区域的细节精度。

3. **两种先验互补**：同时使用两种先验（Base+Prior）将 Overall 进一步降至 0.041，F-score 提升至 67.719，表明深度和法向信息在空间上互补——深度先验约束纹理丰富区域和边缘，法向先验约束平坦弱纹理区域（如 **Figure 3** 所示）。

4. **扰动-残差约束消除局部断裂**：完整方法（Full）加入平滑距离项 $L_{smooth\_D}$ 和法向一致性项 $L_{consist\_N}$ 后，Overall 降至 0.024，Completion 从 0.047 降至 0.028，Recall 从 64.801 升至 68.983。**Figure 9(g) vs (d)** 的视觉对比显示，扰动-残差约束显著改善了表面连续性和完整性，消除了仅使用先验时仍存在的局部孔洞和断裂。

![[assets/figures/papers/paper_list_l75_https_arxiv_org_abs_2210_06853/figures/012_Figure_9.jpg]]
*Figure 9: Visualization results of the ablation study of a simple scene without a boundingbox. The analysis is presented in Section 5.4. The quantitative comparisons are shown in Table 4*

### 失败模式与适用边界

论文通过 **Figure 11** 和文字分析明确了 NeuralRoom 的局限性：

1. **对位姿和先验误差敏感**：方法严重依赖准确的相机位姿。当位姿或先验存在较大误差时，重建质量会显著下降（“pose and priors errors have a strong adverse impact”）。这意味着在实际应用中，需要高质量的 SfM 或 SLAM 前端提供可靠的位姿估计。

2. **近距离相似表面过度平滑**：当两个法向相同且距离接近的表面缺乏正确的距离先验时，模型可能过度平滑并错误地合并它们（Figure 11 右）。这是几何先验稀疏性带来的固有局限——在深度先验缺失的区域，法向约束可能将两个平行表面拉向同一平面。

3. **计算开销大**：默认配置（8 层几何 MLP，4 层颜色 MLP，64+64 采样光线）需约 9.6GB 显存，单张 RTX 2080Ti 训练需 16 小时。这限制了方法的实时应用和大规模部署。

4. **场景规模受限**：目前仅适用于房间规模场景，扩展到更大或更复杂的场景受限于 MLP 的表示容量和计算量。这是神经隐式表示的共性问题。

### 扩展应用：NeuralRoom-Advanced

**Table 5** 和 **Figure 12** 展示了 NeuralRoom 作为后处理模块提升现有重建算法的能力（NeuralRoom-Advanced）。实验表明，将 COLMAP、ACMP、ESTDepth 等方法的初始重建结果输入 NeuralRoom 进行优化后，各方法的 F-score 均有显著提升，验证了几何约束神经隐式表面作为通用优化框架的潜力。

## 定位与知识库关联

NeuralRoom 的核心贡献在于**改变了神经隐式表面重建中“几何约束方式”这一关键 slot**。传统神经隐式表面方法（如 NeuS、VolSDF、Unisurf）仅依赖光度一致性（渲染颜色损失）来优化 SDF，这在单物体重建中效果显著，但面对室内场景的大量弱纹理区域时，会陷入形状-辐射歧义（shape-radiance ambiguity）——网络可以生成完全错误的几何表面，却仍能渲染出与输入一致的图像（参见 Figure 2）。NeuralRoom 的突破在于**将可靠的显式几何先验（MVS 距离先验 + 不确定度过滤的法向先验）注入隐式优化过程**，从而大幅收窄隐式表面的可能空间变化范围，使优化能够逃离局部最优。

具体而言，相对于基线方法，NeuralRoom 改变了两个关键 slot：

1. **几何约束方式**：从“仅依赖渲染损失”变为“渲染损失 + 距离先验损失 + 法向先验损失 + 扰动-残差约束”。其中，距离先验来自 COLMAP MVS（**Schonberger and Frahm, 2016**），法向先验来自 UncertSurfaceNormal 网络（**Bae et al., 2021**），两者互补——MVS 在纹理丰富区域精度高，法向估计网络在纹理缺失区域表现好（Figure 3）。这种互补性使得几何先验能够覆盖室内场景的不同区域类型。

2. **局部平滑约束**：引入扰动-残差约束（perturbation-residual restrictions），这是本文独有的设计。通过对采样点施加微小扰动，约束渲染深度和法向在局部邻域内保持一致（平滑距离项 $\mathcal{L}_{\text{smooth}_D}$ 和法向一致性项 $\mathcal{L}_{\text{consist}_N}$），从而抑制隐式表面在缺乏先验的区域出现断裂或过度波动（Figure 6）。

### 与已有方法的关系与差异

- **相对于传统 MVS 方法**（COLMAP, **Schonberger and Frahm, 2016**；ACMP, **Xu and Tao, 2019**）：传统 MVS 在弱纹理区域直接失效，无法生成完整网格。NeuralRoom 将 MVS 的稀疏深度转为距离先验，仅作为优化引导而非最终结果，利用神经渲染的连续性填补缺失区域。

- **相对于学习型深度估计方法**（ESTDepth, **Long et al., 2021b**；3DVNet, **Rich et al., 2021**）：这些方法预测稠密深度图后进行融合，但深度预测在弱纹理区域同样不可靠。NeuralRoom 不直接使用深度图进行融合，而是将其作为先验损失项嵌入体渲染优化中，使网络有能力“修正”先验中的错误。

- **相对于端到端体素重建方法**（Atlas, **Murez et al., 2020**；NeuralRecon, **Sun et al., 2021a**）：Atlas 和 NeuralRecon 直接回归 TSDF 体素，受限于体素分辨率和感受野。NeuralRoom 采用基于 MLP 的连续隐式表示，理论上可表示任意分辨率的几何，且通过几何先验缓解了隐式方法在室内场景中的歧义问题。实验表明，NeuralRoom 的 F-score（66.756）和 Overall（0.055）均显著优于 Atlas（61.871, 0.070）（Table 3）。

- **相对于 NeuS/VolSDF/Unisurf**（**Wang et al., 2021b**；**Yariv et al., 2021**；**Oechsle et al., 2021**）：这些方法奠定了 SDF-based 体渲染的理论基础（将 SDF 转换为密度用于体渲染），但未引入任何显式几何先验。NeuralRoom 继承了其渲染框架，但在损失函数层面增加了几何先验损失和扰动-残差约束，是对该框架在室内场景适用性上的关键扩展。

### 知识库挂载点

NeuralRoom 可挂载到知识库的以下位置：

- **神经隐式表面重建**：作为“几何先验引导的神经隐式表面重建”子类，与 NeuS、VolSDF 并列，区别在于引入了外部几何先验和局部平滑约束。
- **多视图室内重建**：作为“神经渲染 + MVS 先验”的混合方法，介于传统 MVS 和纯学习型方法之间。
- **形状-辐射歧义缓解**：作为该问题的解决方案之一，通过收窄隐式表面的空间变化范围来缓解歧义，与 MonoSDF（**Yu et al., 2022**）等使用单目先验的方法形成对比——NeuralRoom 使用的是多视图 MVS 先验，理论上在纹理丰富区域更精确。

### 适用边界与局限性

1. **相机位姿依赖**：方法严重依赖准确的相机位姿（通常由 COLMAP 提供）。当位姿误差较大时，几何先验的投影关系被破坏，重建质量会显著下降。这是实际部署中的主要瓶颈。

2. **先验质量敏感**：距离先验和法向先验的质量直接影响最终结果。在极端弱纹理或重复纹理场景中，COLMAP 的深度估计可能完全失效，法向估计的不确定度过高会导致有效先验稀疏，此时方法退化为普通神经隐式重建。

3. **计算开销大**：单场景训练需约 16 小时（RTX 2080Ti），显存占用约 9.6GB，限制了其实时或大规模应用。

4. **场景规模受限**：目前仅适用于房间规模场景。MLP 的容量有限，扩展到更大场景需要分块策略或更高效的表示（如 Instant-NGP、TensoRF）。

5. **表面合并问题**：当两个法向相同且距离接近的表面缺乏正确的距离先验时，扰动-残差约束可能过度平滑并错误地合并它们（Figure 11 右）。

### 后续工作启发

- **高效表示替换**：将 MLP 替换为 Instant-NGP 或 TensoRF 等加速表示，有望将训练时间从小时级降至分钟级，同时提升可处理的场景规模。
- **自适应先验权重**：根据先验质量（如法向不确定度、MVS 置信度）自适应调整损失权重，可提升在不同场景下的鲁棒性。
- **先验质量提升**：使用更先进的 MVS 方法（如基于学习的深度估计）和法向估计网络，可直接提升重建质量的上限。
- **与语义先验结合**：引入语义分割或平面检测等高层先验，可进一步约束室内场景中的平面区域（墙面、地面、天花板），改善几何完整性。
- **位姿联合优化**：将相机位姿作为可优化变量纳入训练过程，可降低对离线 SfM 精度的依赖，提升方法在真实场景中的实用性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/NeuralRoom_Geometry_Constrained_Neural_Implicit_Surfaces_for_Indoor_Scene_Reconstruction.pdf]]
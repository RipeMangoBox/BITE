---
title: "4D-Rotor Gaussian Splatting: Towards Efficient Novel View Synthesis for Dynamic Scenes"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/4D_Rotor_Gaussian_Splatting_Towards_Efficient_Novel_View_Synthesis_for_Dynamic_Scenes.pdf
project_link: null
code_link: "https://github.com/weify627/4D-Rotor-Gaussians"
aliases:
- 4RGS4
- 4RGSTENVSDS
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入 4D 高斯表示与 rotor 旋转，通过时序切片将 4D 高斯投影为 3D 高斯，利用时间衰减项自然建模物体的出现与消失，并结合基于光栅化的高效渲染实现实时性能。
primary_logic: 将 3D 高斯拓展到 4D 空间，动态场景可视为 4D 高斯在不同时间切面上的投影，这种显式时空表示天然适合捕捉复杂运动并保持实时性。
claims:
- 在 Plenoptic Video Dataset 上，PSNR 达到 31.62，超过此前最优方法 (MixVoxels 30.85) 0.77 dB，渲染速度 277 FPS 是 RealTime4DGS (72.8 FPS) 的 3.8 倍。
- 在 D-NeRF 数据集上，PSNR 34.26（黑背景）超越同类 4D 高斯方法 RealTime4DGS 1.55 dB，渲染速度达 1258 FPS（约为其 4.3 倍）。
- 消融实验表明，移除熵损失 (L_entropy) 使 PSNR 从 33.06 降至 32.64（白色背景），移除 4D 一致性损失 (KNN) 使 PSNR 降至 31.91。
- 4D 一致性损失有效提升光流场的平滑性与准确性 (Figure 6)，熵损失显著减少稀疏视角下的漂浮物 (Figure 8)。
---

# 4D-Rotor Gaussian Splatting: Towards Efficient Novel View Synthesis for Dynamic Scenes

> [!tip] 核心洞察
> 将 3D 高斯拓展到 4D 空间，动态场景可视为 4D 高斯在不同时间切面上的投影，这种显式时空表示天然适合捕捉复杂运动并保持实时性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4D-Rotor 高斯泼溅：面向动态场景的高效新视角合成 |
| 英文题名 | 4D-Rotor Gaussian Splatting: Towards Efficient Novel View Synthesis for Dynamic Scenes |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://weify627.github.io/4drotorgs/) · [Code](https://github.com/weify627/4D-Rotor-Gaussians) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | 4D-Rotor Gaussian Splatting (4DRotorGS) |
| Dataset | Plenoptic Video Dataset, D-NeRF Dataset |

> [!tip] 效果简介
> - Plenoptic Video Dataset 上，PSNR 31.62 vs 30.85 (MixVoxels) (+0.77)；FPS 277.47 vs 72.80 (RealTime4DGS) (+204.67)。
> - D-NeRF Dataset 上，PSNR (black bg) 34.26 vs 32.71 (RealTime4DGS) (+1.55)；FPS 1257.63 vs 289.07 (RealTime4DGS) (+968.56)。

## 概要

**问题**：现有动态新视角合成方法依赖基于变形场或体渲染的框架，难以高效处理物体突然出现/消失等复杂动态，且推理速度远达不到实时要求。

**方法**：本文提出 **4D-Rotor Gaussian Splatting (4DRotorGS)**，将场景显式建模为各向异性 4D 高斯，并用 4D rotor 表示时空旋转。动态场景被视作 4D 高斯在不同时刻的时序切片——每个时刻从 4D 高斯中切出对应的 3D 高斯，并自然携带时间衰减项以建模物体的出现与消失。渲染直接沿用 3D 高斯的光栅化管线，保持高效。

**结果**：在 Plenoptic Video Dataset 上，PSNR 达 31.62 dB，超越此前最优方法 MixVoxels 0.77 dB，渲染速度 277 FPS（RTX 3090），是 RealTime4DGS 的 3.8 倍。在 D-NeRF 数据集上，PSNR 34.26 dB（黑背景），超越 RealTime4DGS 1.55 dB，渲染速度 1258 FPS，约为其 4.3 倍。

**定位**：该方法以 3D Gaussian Splatting (Kerbl et al., SIGGRAPH 2023) 为基础，将表示空间从 3D 扩展到 4D，并引入 rotor 旋转与时空一致性正则化，属于显式 4D 高斯动态表示路线，与基于变形场的方法和双四元数 4D 高斯方法形成对比。

## 核心方法与创新机理

### 问题瓶颈与核心思路

动态场景新视角合成面临两个核心瓶颈：其一，基于变形场的方法（如 D-NeRF、Deformable3DGS）将每一帧映射到规范空间，难以处理物体突然出现/消失等非连续动态；其二，主流 NeRF 方法依赖体渲染，推理速度远不能满足实时需求。4DRotorGS 的关键洞察在于：**将动态场景视为 4D 时空高斯在不同时间切面上的投影**，从而用显式时空表示统一处理复杂运动与实时渲染。

具体而言，方法将 3D 高斯拓展到 4D 空间，每个 4D 高斯携带空间均值 $\pmb{\mu}_{3D}$、时间均值 $\mu_t$、4D 协方差矩阵 $\Sigma_{4D}$、不透明度 $\alpha$ 和球谐系数。给定时间查询 $t$，通过**时序切片**（temporal slicing）从 4D 高斯推导出对应的 3D 高斯，该 3D 高斯天然包含时间衰减项和运动偏移，可直接送入 3DGS 的可微光栅化管线。这种设计使物体的出现与消失由时间衰减项 $e^{-\frac{1}{2}\lambda(t-\mu_t)^2}$ 自然建模，无需额外机制。

### 核心模块与因果关系

方法由四个关键模块串联，形成端到端的训练与推理管线：

**模块 1：4D 高斯初始化。** 在 4D 包围盒内均匀采样点，初始化 4D 均值、尺度、rotor 旋转参数和不透明度。与 3DGS 的 SfM 点云初始化不同，动态场景缺乏可靠的 4D 先验，因此采用均匀采样策略。

**模块 2：Rotor 旋转表示与归一化。** 这是方法的核心 changed slot。4D 旋转的表示直接影响优化稳定性和渲染质量。方法采用几何代数中的 4D rotor，其 8 分量表示为：
$$\mathbf{r} = s + b_{01}\mathbf{e}_{01} + b_{02}\mathbf{e}_{02} + b_{03}\mathbf{e}_{03} + b_{12}\mathbf{e}_{12} + b_{13}\mathbf{e}_{13} + b_{23}\mathbf{e}_{23} + p\mathbf{e}_{0123}$$
其中前四个分量（$s, b_{01}, b_{02}, b_{03}$）编码空间旋转，后四个分量（$b_{12}, b_{13}, b_{23}, p$）编码时空耦合旋转（即空间平移）。关键性质：当后四个分量置零时，rotor 退化为四元数，可表示纯 3D 空间旋转——这使 4DRotorGS 在静态场景上天然兼容 3DGS（Figure 4 验证了静态场景下 PSNR 27.07 vs 3DGS 27.01）。相较于 RealTime4DGS 使用的双四元数，rotor 的梯度传播更稳定，训练损失曲线更低（Figure 11）。

![[assets/figures/papers/paper_list_l8_https_weify627_github_io_4drotorgs/figures/004_Figure_4.jpg]]
*Figure 4: Modeling 3D Static Scenes. Our rotor-based representation enables both 3D static and 4D dynamic scene modeling, matching the results of 3DGS on 3D scenes*

Rotor 通过梯度更新后需重归一化以保证有效性，4D 旋转矩阵由 rotor 的指数映射导出，进而构建 4D 协方差矩阵：
$$\Sigma_{4D} = \mathbf{R}_{4D} \mathbf{S}_{4D} \mathbf{S}_{4D}^T \mathbf{R}_{4D}^T$$

**模块 3：时序切片。** 给定时间 $t$，将 4D 协方差矩阵分块：
$$\Sigma_{4D} = \begin{pmatrix} \mathbf{U} & \mathbf{V} \\ \mathbf{V}^T & \mathbf{W} \end{pmatrix}, \quad \Sigma_{4D}^{-1} = \begin{pmatrix} \mathbf{A} & \mathbf{M} \\ \mathbf{M}^T & \mathbf{Z} \end{pmatrix}$$
通过舒尔补推导，切片的 3D 高斯为：
$$G_{3D}(\mathbf{x}, t) = e^{-\frac{1}{2}\lambda (t - \mu_t)^2} e^{-\frac{1}{2} [\mathbf{x} - \mu(t)]^T \Sigma_{3D}^{-1} [\mathbf{x} - \mu(t)]}$$
其中 $\lambda = \mathbf{W}^{-1}$ 为时间衰减因子，$\mu(t) = \pmb{\mu}_{3D} + \mathbf{V}\mathbf{W}^{-1}(t - \mu_t)$ 为时间驱动的空间均值偏移，$\Sigma_{3D} = \mathbf{U} - \mathbf{V}\mathbf{V}^T/\mathbf{W}$ 为切片协方差（避免直接对 $\mathbf{A}$ 求逆）。

**因果链路**：rotor 旋转决定了 4D 协方差的结构，进而通过切片公式同时影响 3D 高斯的位置偏移 $\mu(t)$、形状 $\Sigma_{3D}$ 和可见性权重 $e^{-\frac{1}{2}\lambda(t-\mu_t)^2}$。这种联合建模使 4D 高斯能表达旋转、平移、缩放和出现/消失等复杂动态。

**模块 4：损失函数与优化。** 总损失为：
$$L = (1 - \lambda_1) L_1 + \lambda_1 L_{ssim} + \lambda_2 L_{entropy} + \lambda_3 L_{consistent4D}$$

新增的两个正则化项是关键的 changed slots：

- **熵损失** $L_{entropy} = \frac{1}{N}\sum_{i=1}^{N} -o_i \log(o_i)$：促使 4D 高斯的不透明度趋向 0 或 1，减少半透明漂浮物。消融实验表明，移除该项使 D-NeRF 白色背景 PSNR 从 33.06 降至 32.64（Table 6），在稀疏视角下效果尤为显著（Figure 8）。

- **4D 一致性损失** $L_{consistent4D} = \frac{1}{N}\sum_{i=1}^{N} \|\mathbf{s}_i - \frac{1}{K}\sum_{j\in\Omega_i}\mathbf{s}_j\|_1$：对每个 4D 高斯的时空均值 $\mathbf{s}_i = (\pmb{\mu}_{3D}, \mu_t)$，约束其与 K 近邻高斯保持一致。这使运动场更平滑，光流可视化显示噪声显著减少（Figure 6）。消融实验表明，移除该项使 PSNR 从 33.06 降至 31.91（Table 6），降幅达 1.15 dB，是影响最大的单一组件。

### 训练与推理路径

**训练路径**：4D 高斯初始化 → 给定时间 $t$，rotor 构建 $\Sigma_{4D}$ → 时序切片得到 $G_{3D}(\mathbf{x}, t)$ → 可微光栅化渲染 → 计算 $L$ → 梯度回传更新所有 4D 高斯参数（均值、rotor、尺度、不透明度、球谐系数）→ 自适应密度控制（基于视图空间梯度克隆/分裂高斯，裁剪近透明高斯）→ 迭代优化。

**推理路径**：给定新视角和时间 $t$，执行时序切片 → 光栅化渲染，无需梯度计算。得益于光栅化的高效性，在 RTX 3090 上渲染 1352×1014 视频达 277 FPS，RTX 4090 上达 583 FPS。

**CUDA 加速实现**：方法提供 PyTorch 原型和 C++/CUDA 高性能版本。CUDA 版本将 4D rotor 到旋转矩阵的转换、4D 高斯切片、密度控制等操作全部定制实现，训练加速 16.6 倍，GPU 显存占用低。这是实现实时渲染的关键工程支撑。

### 与基线的核心差异

相较于 3DGS（仅静态 3D 高斯），4DRotorGS 将表示空间从 $\mathbb{R}^3$ 拓展到 $\mathbb{R}^4$，通过时序切片自然引入时间维度。相较于 RealTime4DGS（双四元数 4D 旋转），rotor 表示提供了更稳定的梯度传播和更低的训练损失（Figure 11），且 rotor 到四元数的退化性质使静态场景建模无需特殊处理。相较于变形场方法（Deformable3DGS、D-NeRF），4DRotorGS 无需学习 MLP 映射，所有动态信息编码在 4D 高斯的显式参数中，避免了变形场对非连续动态的建模困难。

![[assets/figures/papers/paper_list_l8_https_weify627_github_io_4drotorgs/figures/002_Figure_2.jpg]]
*Figure 2: A Simplified 2D Illustration of the Proposed Temporal Slicing. (a) We model 2D dynamics with 3D ?????? ellipsoids and slice them with different time queries. (b) The sliced 3D ellipsoids form 2D dynamic ellipses at each timestamp*

![[assets/figures/papers/paper_list_l8_https_weify627_github_io_4drotorgs/figures/003_Figure_3.jpg]]
*Figure 3: Framework Overview. After initialization, we first temporally slice the 4D Gaussians whose spatio-temporal movements are modeled with rotors. The dynamics such as the flickering flames naturally evolve through time, even within a short period of 0.27 second. The sliced 3D Gaussians are then projected onto 2D using differentiable rasterization. The gradients from image loss are back-propagated and guide the adaptive density control of 4D Gaussians*

## 实验与关键发现

### 主要定量结果

**Plenoptic Video Dataset 上的性能。** 在 Plenoptic Video Dataset 上，4DRotorGS 在渲染质量与推理速度上均显著超越此前最优方法。PSNR 达到 **31.62**，较此前最优的 MixVoxels（30.85）提升 **0.77 dB**；SSIM 为 0.94，LPIPS 降至 0.14（Table 1）。渲染速度方面，4DRotorGS 在 RTX 3090 上达到 **277.47 FPS**，是 RealTime4DGS（72.80 FPS）的 **3.8 倍**，训练时间仅需约 60 分钟。这一速度优势源于基于光栅化的渲染管线，避免了体渲染的密集采样。

**D-NeRF 数据集上的性能。** 在单目视频动态 NVS 基准 D-NeRF 上，4DRotorGS 同样取得最优。黑色背景下 PSNR 达到 **34.26**，超过同属 4D 高斯范式的 RealTime4DGS（32.71）**1.55 dB**，渲染速度达 **1257.63 FPS**，约为 RealTime4DGS（289.07 FPS）的 **4.3 倍**（Table 2）。值得注意的是，背景颜色对 PSNR 有显著影响：多数场景在黑色背景下 PSNR 更高，但部分方法（如 Deformable4DGS）在白色背景下更优。文中在 Table 7 中分别报告了两种背景的结果，以与各基线原始设置对齐。

**HyperNeRF 与 Total-Recon 数据集。** 在 HyperNeRF 数据集上，4DRotorGS 在多数场景和平均 PSNR 上超越此前最优方法 Deformable4DGS（Table 4）。在极稀疏视角的 Total-Recon 数据集上，仅用 RGB 监督时 4DRotorGS 仍取得最高 PSNR（Table 5），但渲染质量整体较低，容易出现漂浮物（Figure 10），表明稀疏视角下 4D 高斯的约束仍不充分。

### 关键消融实验

Table 6 报告了在 D-NeRF 数据集上的组件消融（白色背景，完整模型 PSNR 33.06）：

- **移除熵损失（$L_{\text{entropy}}$）**：PSNR 从 33.06 降至 **32.64**（-0.42 dB）。熵损失通过惩罚中间透明度值，促使高斯趋向完全透明或不透明，从而有效减少稀疏视角下的漂浮物（Figure 8 定性验证）。
- **移除 4D 一致性损失（KNN）**：PSNR 从 33.06 降至 **31.91**（-1.15 dB），降幅最大。该损失约束邻近高斯的运动一致性，缺失时运动估计出现明显噪声，光流场的平滑性和准确性显著下降（Figure 6 定性验证）。
- **移除批量训练（Batch Training）**：PSNR 降至 32.57（-0.49 dB），同时高斯点数从 0.65M 增至 0.78M，表明批量训练有助于控制高斯数量并提升质量。

此外，Figure 11 比较了 rotor 旋转与双四元数旋转的训练损失曲线，rotor 表示收敛更快且最终损失更低，验证了 4D rotor 在表示时空旋转上的优势。

### 定性分析与可视化

**动态细节恢复。** Figure 5 展示了在 Plenoptic Video Dataset 上的定性对比：4DRotorGS 在动态区域（如人体局部放大）恢复出更精细的细节，静态区域（如钩子）也呈现更锐利的边缘。Figure 7 在 D-NeRF 数据集上进一步验证，相较于 TiNeuVox（NeRF 基线）、Deformable4DGS 和 RealTime4DGS（高斯基线），4DRotorGS 在运动边界和纹理细节上均表现更优。

**光流场的自然导出。** 4DRotorGS 可从 4D 高斯直接推导出速度场，渲染为 2D 光流。Figure 6 显示，加入 4D 一致性损失后，光流噪声显著减少，运动估计更加平滑准确，表明该损失不仅提升渲染质量，还增强了场景运动建模的物理合理性。

**静态场景兼容性。** Figure 4 验证了 rotor 表示对静态 3D 场景的兼容性：将时间维度置零后，rotor 退化为四元数，4DRotorGS 在静态场景上达到与 3DGS 相当的 PSNR（27.07 vs. 27.01），证明方法未因引入时间维度而损害空间建模能力。

### 失败模式与适用边界

1. **稀疏视角下的漂浮物**：在 Total-Recon 等极稀疏视角数据集上，仅用 RGB 监督时 4D 高斯难以充分约束，容易产生漂浮物和不一致运动（Figure 10）。熵损失和 4D 一致性损失虽能缓解，但无法完全消除。
2. **快速相机运动与大幅动态**：文中指出方法对快速相机运动和大幅运动场景仍存在挑战，可能产生模糊或几何错误，具体定量证据有待进一步验证。
3. **时间尺度初始化敏感性**：方法对时间尺度的初始化较为敏感，需根据数据集调整，这增加了跨场景迁移的调参负担。
4. **背景颜色依赖性**：Table 7 揭示不同方法对背景颜色偏好不同，4DRotorGS 在黑色背景下表现更优，白色背景下优势缩小，需在实际应用中注意对齐评估设置。

![[assets/figures/papers/paper_list_l8_https_weify627_github_io_4drotorgs/figures/014_Figure_10.jpg]]
*Figure 10: Qualitative Results on Total-Recon Dataset. We show the qualitative results of our method on the challenging Total-Recon dataset [Park et al. 2021b]. In this scene, the dog runs or walks freely in a spacious room. Due to the very sparse training views, our NVS results become much worse than those on other datasets. For scene regions that have been captured by multiple frames (e.g., left example), the synthesized novel views are relatively clear. When the dog runs and the camera follows with rapidly changing camera poses, the rendering quality becomes severely affected. For example, the right example shows the renderings are very bad due to floaters caused by too sparse training views*

### 效率分析

4DRotorGS 的高效率来自两个层面：算法层面，基于光栅化的渲染避免了体渲染的密集采样；工程层面，C++/CUDA 高性能实现将 4D rotor 到旋转矩阵的转换、4D 高斯切片、复制与剪枝等操作均在 GPU 上完成，训练加速达 **16.6 倍**，在 RTX 4090 上渲染速度可达 **583 FPS**（1352×1014 分辨率），满足实时应用需求。

![[assets/figures/papers/paper_list_l8_https_weify627_github_io_4drotorgs/figures/007_Table_1.jpg]]
*Table 1: Evaluation on Plenoptic Video Dataset. We compare our method with both NeRF-based and Gaussian-based approaches. Our method significantly outperforms baselines on PSNR and inference speed. *: Only tested on the scene Flame Salmon. **: Trained on 8 GPUs. †: Results from paper*

![[assets/figures/papers/paper_list_l8_https_weify627_github_io_4drotorgs/figures/008_Table_2.jpg]]
*Table 2: Evaluation on D-NeRF Dataset. Our method outperforms NeRF-based and Gaussian-based baselines on both PSNR and rendering speed by a large margin*

## 定位与知识库关联

**方法定位与核心改变**

4DRotorGS 的根本贡献在于将动态场景的表示从“3D 高斯 + 变形场”范式迁移到“原生 4D 高斯 + 时序切片”范式。具体而言，它改变了动态 NVS 方法中的**场景表示**与**动态建模方式**两个关键 slot：

- **场景表示 slot**：从 3D 高斯（仅空间维度）升级为含时间维度的 4D 高斯，并用 8 分量 4D rotor 替代四元数/双四元数来参数化 4D 旋转。这一改变使得场景本身就是一个完整的时空实体，而非在规范空间与观测帧之间建立映射关系。
- **动态建模方式 slot**：从基于变形场（如 D-NeRF (Pumarola et al., CVPR 2021)、Deformable3DGS (Yang et al., 2023)）或双四元数旋转（RealTime4DGS (Yang et al., 2024)）的间接动态描述，转变为对 4D 高斯在给定时刻 t 进行直接时序切片。切片操作天然产生两个效应：时间衰减项 $\lambda(t-\mu_t)^2$ 控制高斯在时间维度上的可见性，使物体的出现与消失无需额外建模；运动项 $\mu(t)$ 由切片协方差矩阵的块结构自动推导，无需独立的位移预测网络。

这一范式转换的因果链路是：4D rotor 提供时空可分离的旋转表示 → 4D 协方差矩阵可按空间/时间块分块求逆 → 给定 t 时可解析地推导出 3D 协方差 $\Sigma_{3D} = \mathbf{U} - \mathbf{V}\mathbf{V}^T/\mathbf{W}$ 和时间衰减因子 $\lambda = \mathbf{W}^{-1}$ → 切片后的 3D 高斯直接送入 3DGS 的可微光栅化管线，保持了实时渲染能力。

**与现有方法的关键差异**

| 维度 | 变形场范式 (Deformable3DGS, RealTime4DGS) | 4D 高斯切片范式 (4DRotorGS) |
|------|------|------|
| 动态来源 | 规范空间 + 变形映射 | 4D 高斯的时空协方差结构 |
| 出现/消失 | 需额外建模（如透明度变化） | 时间衰减项自然处理 |
| 旋转表示 | 四元数 (3D) 或双四元数 (4D) | 8 分量 rotor，时空可分离 |
| 运动场获取 | 隐式或额外预测 | 从切片协方差解析推导 |
| 渲染管线 | 需先变形再光栅化 | 切片后直接光栅化 |

相较于 RealTime4DGS 的双四元数旋转，4D rotor 的关键优势在于其时空可分离性：当 rotor 的后四个分量（时空旋转分量）设为零时，rotor 退化为标准四元数，可直接建模 3D 静态场景（Figure 4 验证了此等价性）。此外，Figure 11 的训练损失曲线显示，rotor 表示比双四元数收敛更快、损失更低，这归因于 rotor 在几何代数框架下对 4D 旋转的紧致、无冗余参数化。

**知识库挂载点**

本方法在知识库中可挂载于以下节点：

1. **动态场景表示**：作为“显式时空表示”分支的代表方法，与基于 NeRF 的隐式表示（K-Planes (Fridovich-Keil et al., CVPR 2023)、MixVoxels (Wang et al., 2023)）和基于 3D 高斯变形的方法（Deformable4DGS (Wu et al., 2023)、RealTime4DGS (Yang et al., 2024)）形成对比。其核心洞察是：动态场景可视为 4D 高斯在不同时间切面上的投影，这种显式表示天然适合捕捉复杂运动并保持实时性。

2. **几何代数在视觉中的应用**：4D rotor 源自几何代数框架（Bosch 2020），本工作将其引入动态 NVS 领域，展示了 Clifford 代数在时空旋转建模中的实用性。rotor 的 8 分量结构（$s + b_{01}\mathbf{e}_{01} + ... + p\mathbf{e}_{0123}$）为后续工作提供了可扩展的参数化模板。

3. **高效动态渲染**：继承 3DGS (Kerbl et al., SIGGRAPH 2023) 的光栅化渲染管线，通过 C++/CUDA 加速实现训练加速 16.6 倍，渲染速度达 277 FPS (RTX 3090) 至 583 FPS (RTX 4090)，将动态 NVS 推入实时域。

**适用边界与局限性**

- **稀疏视角场景**：在 Total-Recon 数据集（极稀疏视角）上，仅用 RGB 监督时渲染质量较低，容易出现漂浮物（Figure 10）。这是 4D 高斯表示自由度较高、约束不足的直接后果。
- **快速/大幅运动**：对快速相机运动和大幅物体运动仍然存在挑战，可能产生模糊或几何错误。这源于 4D 高斯在时间维度上的平滑性假设与剧烈运动之间的冲突。
- **时间尺度敏感性**：4D 高斯的初始化依赖时间尺度参数，需根据数据集手动调整，缺乏自适应性。
- **长序列扩展**：当前框架针对固定时长的视频片段设计，向更长序列的扩展需要解决内存线性增长和 4D 高斯密度控制策略的适配问题。

**后续启发与开放方向**

1. **下游任务复用**：4D 高斯表示天然提供场景的时空连续描述，可直接导出 3D 运动场（Figure 6 的光流可视化即为直接应用），有望用于目标跟踪、动态场景分割、动作识别等任务。
2. **多模态监督融合**：引入深度、光流等显式监督信号有望缓解稀疏视角下的漂浮物问题，增强 4D 高斯的几何约束。
3. **表示能力扩展**：rotor 框架可进一步扩展至更高维度的旋转表示，为更复杂的时空变换（如非刚性变形）提供参数化基础。
4. **内存与计算优化**：4D 高斯的密度控制策略目前直接继承 3DGS，针对 4D 特性的自适应剪枝和压缩策略值得探索，以支持更长序列和更大场景。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/4D_Rotor_Gaussian_Splatting_Towards_Efficient_Novel_View_Synthesis_for_Dynamic_Scenes.pdf]]
---
title: "GM-R^2: Generative Matching Learning for Unsupervised Geometric Representation and Registration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GM_R_2_Generative_Matching_Learning_for_Unsupervised_Geometric_Representation_and_Registration.pdf
project_link: null
code_link: null
aliases:
- GR2
- GR2GMLUGRR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 以几何条件驱动的跨视角图像生成一致性作为隐式监督信号，替代显式位姿标签，迫使几何特征提取器学习对应对齐的表示。
primary_logic: 只有对应关系一致的几何条件才能驱动生成器产生跨视角一致的图像，因此通过优化跨视角生成一致性可以间接强制编码器学习对应一致的点云几何描述符。
claims:
- 在3DMatch和ScanNet基准上实现无监督SOTA，旋转/平移/倒角距离精度全面超越全监督方法，如旋转平均误差降低2.5°（vs PARE-Net），平移误差降低8.6cm。
- 消融实验验证AFoV-ERP相对于标准ERP一致提升精度，更高分辨率范围图带来倒角精度增益。
- 3DMatch 上 Mean Rotation Error (deg) = 2.0
- 3DMatch 上 Mean Translation Error (cm) = 6.4
---

# GM-R^2: Generative Matching Learning for Unsupervised Geometric Representation and Registration

> [!tip] 核心洞察
> 只有对应关系一致的几何条件才能驱动生成器产生跨视角一致的图像，因此通过优化跨视角生成一致性可以间接强制编码器学习对应一致的点云几何描述符。

| 字段 | 内容 |
|------|------|
| 中文题名 | GM-R^2: 面向无监督几何表示与配准的生成式匹配学习 |
| 英文题名 | GM-R^2: Generative Matching Learning for Unsupervised Geometric Representation and Registration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_GM-R2_Generative_Matching_Learning_for_Unsupervised_Geometric_Representation_and_Registration_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | GM-R^2 |
| Dataset | 3DMatch, ScanNet |

> [!tip] 效果简介
> - 3DMatch 上，Mean Rotation Error (deg) 2.0 vs PARE-Net: 4.5 (estimated from delta 2.5↓) (−2.5)；Mean Translation Error (cm) 6.4 vs PARE-Net: 15.0 (estimated from delta 8.6↓) (−8.6)；Rotation Accuracy @5° (%) 96.2 vs Best supervised (see Table 1) (N/A)。
> - ScanNet 上，Mean Rotation Error (deg) 7.3 vs SOTA supervised (comparable) (comparable)；Mean Translation Error (cm) 18.5 vs SOTA supervised (comparable) (comparable)；Chamfer Accuracy @10mm (%) 83.5 vs SOTA supervised (comparable) (comparable)。

## 概要

全监督几何描述符学习方法在3D点云配准任务中取得了显著进展，但其性能高度依赖昂贵的真实位姿标注。这种依赖严重制约了模型向大规模、多样化真实场景的泛化能力。与此同时，现有的无监督方法在低重叠区域、重复几何结构以及复杂真实环境下，往往因缺乏可靠的监督信号而陷入局部最优，导致匹配精度不足。

针对这一瓶颈，**GM-R^2** 提出了一种全新的**生成式匹配学习范式**：将几何描述符学习重新定义为以几何条件驱动的跨视角图像生成问题。其核心洞见在于——只有当几何编码器提取的特征具备对应一致性时，生成器才能合成跨视角一致的图像；因此，通过优化跨视角生成一致性，可以间接强制编码器学习对应对齐的点云表示，从而完全摆脱对显式位姿监督的依赖。

为实现这一范式，GM-R^2 设计了两个关键机制。**Auto-FoV Equirectangular Projection (AFoV-ERP)** 自适应地将点云投影到有效视场范围内的高分辨率、无内参范围图，最大化像素利用率与几何保真度。**Denoising-Agnostic Coupled ControlNet** 将传统单视图 ControlNet 扩展为双向跨视图生成器，仅以耦合范围图为条件，移除对噪声潜在变量的依赖，从而构建起从几何条件到跨视图图像生成的直接映射通道。

在实验验证层面，GM-R^2 在 **3DMatch** 和 **ScanNet** 两大基准上实现了无监督方法的 SOTA 性能，且关键指标全面超越全监督方法：在 3DMatch 上，旋转平均误差降至 **2.0°**（较全监督 SOTA **PARE-Net** 降低约 2.5°），平移平均误差降至 **6.4 cm**（降低约 8.6 cm），旋转精度 @5° 达到 **96.2%**。在 ScanNet 上，旋转误差 **7.3°**、平移误差 **18.5 cm**、倒角精度 @10mm **83.5%**，均达到与全监督 SOTA 可比甚至更优的水平。消融实验进一步证实，AFoV-ERP 相对于标准 ERP 在所有阈值上持续提升精度，且提高范围图分辨率可稳定改善倒角距离指标。

GM-R^2 的贡献在于首次证明了**生成一致性可以作为无监督几何描述符学习的有效代理监督信号**，为摆脱昂贵位姿标注的大规模3D表示学习开辟了新路径。

三维点云配准是计算机视觉与机器人领域的核心任务，其目标是在部分重叠的源点云与目标点云之间估计最优刚体变换。该任务的关键瓶颈在于建立可靠的点级对应关系，而对应关系的质量高度依赖于几何描述符的判别力与一致性。全监督深度几何描述符学习范式——以 **FCGF**（Choy et al., ICCV 2019）、**Predator**（Huang et al., CVPR 2021）和 **PARE-Net**（Yao et al., ECCV 2024）为代表——通过大规模标注的位姿真值驱动对比学习或对应关系预测，已在多个基准上取得显著进展。然而，这一范式的根本缺陷在于**对昂贵位姿标注的刚性依赖**：真实场景中获取亚厘米级精度的六自由度变换标注需要高精度传感器或人工标定，成本随场景规模急剧攀升，严重制约了深度描述符向大规模、多场景部署的扩展。

无监督方法试图摆脱位姿标注的束缚。现有路线主要包括：基于手工特征的传统方法（如FPFH），其判别力有限；基于自监督信号重构的 **PPF-FoldNet**（Deng et al., ECCV 2018），仅学习局部几何编码而缺乏跨视图一致性约束；以及基于半监督匹配或强化学习的 **FMR**（Huang et al., CVPR 2020）和 **CEMNet**（Jiang et al., ICCV 2021），它们虽减少了对标注的依赖，但在低重叠、重复纹理结构和复杂真实场景下仍容易陷入局部最优，匹配精度与全监督方法之间存在显著差距。

上述困境引出一个核心问题：**能否找到一种替代显式位姿标签的隐式监督信号，迫使几何特征提取器学习对应一致的表示？** GM-R^2 的动机正是源于一个关键洞察：在几何条件驱动的跨视角图像生成中，只有当源点云与目标点云的几何编码真正“对齐”时，生成器才能产生跨视角一致的图像。换言之，**跨视角生成一致性天然蕴含了对应关系一致性的信息**，可以作为几何描述符学习的高质量代理监督。这一思路将描述符学习从“匹配-标注”范式重新表述为“几何条件驱动的跨视图图像生成”问题，从而在无需任何位姿真值的前提下，间接强制编码器学习对应一致的点云几何描述符。

## 核心方法与创新机理

GM-R^2 的核心创新在于将几何描述符学习从“显式位姿监督”范式彻底转向“生成一致性隐式监督”范式，通过三个紧密耦合的 changed slots 实现这一转变。

### 1. 监督信号的根本性转变：从位姿标签到生成一致性

传统全监督方法（如 **FCGF** (Choy et al., ICCV 2019)、**Predator** (Huang et al., CVPR 2021)、**PARE-Net** (Yao et al., ECCV 2024)）依赖昂贵的真实位姿标注来驱动几何一致性学习，这严重限制了大规模扩展能力。GM-R^2 的核心洞察在于：**只有对应关系一致的几何条件才能驱动生成器产生跨视角一致的图像**。基于此因果机制，方法将训练目标重新定义为最大化给定几何特征时跨视角图像的条件对数似然：

$$
\operatorname* { m a x } _ { \theta } \mathbb { E } _ { ( \mathbf { I } ^ { P } , \mathbf { I } ^ { Q } , \mathbf { P } , \mathbf { Q } ) \sim \mathcal { D } } \left[ \log p ( \mathbf { I } ^ { P } , \mathbf { I } ^ { Q } \mid g _ { \theta } ( \mathbf { P } ) , g _ { \theta } ( \mathbf { Q } ) \right]
$$

通过优化跨视角生成一致性，间接强制编码器 $g_\theta$ 学习对应一致的点云几何描述符，从而完全摆脱对位姿标注的依赖。这一转变是方法有效性的根本原因。

### 2. 生成器架构的关键改造：去噪无关耦合 ControlNet

为实例化上述生成式匹配学习范式，GM-R^2 对标准 ControlNet 进行了两项关键改造：

- **从单视图到跨视图的耦合设计**：将源点云和目标点云的范围图在垂直方向拼接为统一条件图 $\tilde{\mathbf{d}}^{PQ}$，使 ControlNet 编码器能够同时感知两个视角的几何结构，从而生成跨视角一致的图像对。这与仅支持单视图生成的 Vanilla ControlNet 形成本质区别。

- **移除潜在变量依赖（Denoising-Agnostic）**：传统 ControlNet 在训练时需注入噪声潜在变量 $\mathbf{x}_t$，但推理时仅依赖几何条件，导致训练-推理不一致。GM-R^2 的耦合 ControlNet 完全移除潜在变量注入，使编码器在训练和推理阶段遵循完全相同的路径，确保训练目标与几何推理任务严格对齐。

### 3. 几何条件质量的提升：自适应视场等距投影（AFoV-ERP）

标准 ERP 将全 360°×180° 视场均匀离散化，导致大量像素浪费在无点云区域，几何保真度低。AFoV-ERP 通过自适应缩放至有效视场区域，将点云投影重新归一化到完整分辨率栅格：

$$
\tilde { u } _ { i } = \Big \lfloor \frac { \theta _ { i } - \theta _ { \mathrm { m i n } } } { \Delta _ { \theta } } W \Big \rfloor , \quad \tilde { v } _ { i } = \Big \lfloor \frac { \phi _ { i } - \phi _ { \mathrm { m i n } } } { \Delta _ { \phi } } H \Big \rfloor
$$

这一设计的直接效果是最大化像素利用率，生成高分辨率、高保真度的范围图，为后续 ControlNet 提供更优质的几何条件。消融实验证实，AFoV-ERP 相比 Vanilla ERP 在所有评估阈值上持续提升配准精度（Table 3）。

### 创新点之间的关系

三个 changed slots 形成因果链条：AFoV-ERP 提供高质量几何条件 → 耦合 ControlNet 实现跨视图生成 → 生成一致性损失替代位姿监督。这一链条的核心逻辑是：**生成质量的上限决定了隐式监督信号的有效性**，因此几何条件的保真度和生成器架构的跨视图能力共同构成了方法性能的瓶颈与调节旋钮。

GM-R^2 将几何描述符学习重新定义为**几何条件驱动的跨视图图像生成**问题，其核心逻辑链条为：只有对应关系一致的几何条件才能驱动生成器产生跨视图一致的图像，因此通过优化跨视图生成一致性，可以间接强制编码器学习对应一致的点云几何描述符。整个框架由三个关键模块串联构成：**AFoV-ERP 投影**、**去噪无关耦合 ControlNet** 和**生成一致性监督**，形成从 3D 点云到 2D 描述符再到配准估计的端到端无监督管线。

### 输入输出流

- **输入**：一对有重叠区域的源点云 $\mathbf{P}$ 和目标点云 $\mathbf{Q}$，以及对应的 RGB 图像 $\mathbf{I}^P$、$\mathbf{I}^Q$。
- **中间表示**：通过 AFoV-ERP 将 $\mathbf{P}$ 和 $\mathbf{Q}$ 分别投影为无内参的高分辨率范围图 $\tilde{\mathbf{D}}^P$ 和 $\tilde{\mathbf{D}}^Q$，二者沿垂直方向拼接为耦合范围图 $\tilde{\mathbf{d}}^{PQ}$，作为 ControlNet 编码器的几何条件输入。
- **训练信号**：耦合 ControlNet 以 $\tilde{\mathbf{d}}^{PQ}$ 为唯一条件，驱动 Stable Diffusion U-Net（冻结）执行跨视图图像去噪生成；**去噪损失**（生成一致性损失）作为隐式监督信号，仅反向传播至 ControlNet 编码器参数 $\theta$，迫使其提取对应一致的几何特征。
- **输出**：训练完成后，ControlNet 编码器提取的多尺度几何特征与 FPFH 手工特征融合，经 PCA 降维得到紧凑的 3D 描述符；在推理阶段，通过最近邻匹配建立点对应，再以 RANSAC 估计刚体变换 $(\mathbf{R}, \mathbf{t})$。

### 模块关系与数据流

Figure 2 给出了 GM-R^2 的完整管线。训练与推理共享同一特征提取通路，差异仅在于训练时额外引入去噪生成分支以提供监督信号。

![[assets/figures/papers/paper_list_l2512_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_GM_R2_Generative/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of ControlNet-driven Generative Matching Learning*

1. **AFoV-ERP 投影**（Section 3.2.2, Figure 3）：将点云从相机坐标系转换为球坐标 $(\theta_i, \phi_i)$，自适应计算有效 FoV 边界 $[\theta_{\min}, \theta_{\max}]$ 和 $[\phi_{\min}, \phi_{\max}]$，在该区间内重新离散化到 $H \times W$ 栅格，得到高像素利用率、无内参依赖的范围图。相比标准 ERP 在全 $360^\circ \times 180^\circ$ 范围内均匀离散化，AFoV-ERP 通过“缩放”到有效区域，显著提升了几何保真度和后续特征分辨率。

2. **去噪无关耦合 ControlNet**（Section 3.2.3）：将源/目标范围图垂直拼接为耦合几何条件 $\tilde{\mathbf{d}}^{PQ}$，输入 ControlNet 编码器 $\mathrm{CN}_{\mathrm{enc}}$。编码器提取多尺度特征，通过零卷积注入到冻结的 Stable Diffusion U-Net 解码器。关键设计在于**移除潜在变量依赖**——生成过程仅以几何条件为输入，不依赖噪声潜在变量，使得训练与推理阶段 ControlNet 编码器遵循完全相同的通路，保证了表示学习的一致性。

3. **生成一致性监督**（Section 3.2.4）：将真值透视图像通过球面映射重投影到球面坐标，与 AFoV-ERP 生成的球面图像对齐。耦合 ControlNet 以 $\tilde{\mathbf{d}}^{PQ}$ 为条件预测去噪输出，去噪损失 $\mathcal{L} = \mathbb{E}\left[ \left\| \epsilon_{\omega}\left( \tilde{\mathbf{x}}_t^{PQ}, t, \mathrm{CN}_{\mathrm{enc}}(\tilde{\mathbf{d}}^{PQ}; \theta) \right) - \epsilon_t \right\|_2^2 \right]$ 仅优化 $\theta$（冻结 $\omega$），将跨视图图像生成一致性转化为对几何特征提取器的隐式匹配监督。

4. **描述符生成与配准**（Section 3.2.5）：推理时，ControlNet 编码器从耦合范围图中提取多尺度几何特征，与 FPFH 手工特征融合后经 PCA 降维，再通过 2D→3D 反投影得到每个点的紧凑描述符。基于描述符的最近邻搜索建立对应关系 $\mathcal{C}^*$，最后用 RANSAC 求解最优刚体变换 $\operatorname*{min}_{\mathbf{R}, \mathbf{t}} \sum_{(\mathbf{p}, \mathbf{q}) \in \mathcal{C}^*} \left\| \mathbf{R} \mathbf{p} + \mathbf{t} - \mathbf{q} \right\|_2^2$。

### 与全监督范式的对比

Figure 1 对比了全监督匹配学习与 GM-R^2 的无监督生成式匹配范式。全监督方法依赖昂贵的真值刚体变换标注来驱动几何一致性学习（如 FCGF、Predator、PARE-Net 等），而 GM-R^2 以几何条件驱动的跨视图生成一致性作为代理监督信号，完全摆脱了对位姿标签的依赖。这一范式转换的核心洞见在于：**只有对应关系正确的几何条件才能让生成器合成出跨视图一致的图像**，因此优化生成质量等价于隐式优化几何描述符的对应质量。

![[assets/figures/papers/paper_list_l2512_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_GM_R2_Generative/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between fully-supervised matching learning and our unsupervised generative matching paradigm. Supervised methods rely on costly ground-truth transformations to guide geometric consistency learning. By contrast, our framework employs generative consistency supervision, where a geometry-conditioned cross-view generator supplies indirect supervisory signals to enforce correspondence-consistent geometric feature learning*

### 问题形式化：点云配准的优化目标

给定源点云 $\mathbf{P} = \{\mathbf{p}_i\}_{i=1}^N$ 和目标点云 $\mathbf{Q} = \{\mathbf{q}_j\}_{j=1}^M$，点云配准的目标是在已知真值对应集合 $\mathcal{C}^*$ 下，估计最优刚体变换 $[\mathbf{R}, \mathbf{t}]$，使得配准残差的 $L_2$ 范数最小化：

$$\operatorname*{min}_{\mathbf{R},\mathbf{t}} \sum_{(\mathbf{p},\mathbf{q}) \in \mathcal{C}^*} \left\| \mathbf{R}\mathbf{p} + \mathbf{t} - \mathbf{q} \right\|_2^2$$

该公式揭示了全监督范式的核心瓶颈：$\mathcal{C}^*$ 的获取依赖昂贵的位姿标注，限制了方法在大规模场景下的扩展性。

### 生成式匹配学习目标

GM-R^2 将几何描述符学习重新形式化为几何条件驱动的跨视角图像生成问题。其核心优化目标为最大化给定几何特征时跨视角图像的条件对数似然：

$$\operatorname*{max}_{\theta} \mathbb{E}_{(\mathbf{I}^P, \mathbf{I}^Q, \mathbf{P}, \mathbf{Q}) \sim \mathcal{D}} \left[ \log p(\mathbf{I}^P, \mathbf{I}^Q \mid g_\theta(\mathbf{P}), g_\theta(\mathbf{Q})) \right]$$

其中 $g_\theta(\cdot)$ 为待学习的几何特征提取器，$\mathbf{I}^P$ 和 $\mathbf{I}^Q$ 分别为源视角和目标视角的 RGB 图像。该目标的因果逻辑在于：只有对应关系一致的几何条件才能驱动生成器产生跨视角一致的图像，因此优化生成一致性可以间接强制编码器学习对应一致的点云几何描述符。

### 核心模块一：Auto-FoV Equirectangular Projection (AFoV-ERP)

标准 ERP 将点云球坐标 $[\theta_i, \phi_i]$ 线性映射到全 $360^\circ \times 180^\circ$ 的 $H \times W$ 栅格：

$$u_i = \Big\lfloor \frac{\theta_i - (-\pi)}{2\pi} W \Big\rfloor, \quad v_i = \Big\lfloor \frac{\phi_i - (-\pi/2)}{\pi} H \Big\rfloor$$

这导致大量像素被浪费在点云未覆盖的 FoV 区域。AFoV-ERP 通过自适应缩放有效 FoV 边界 $[\theta_{\min}, \theta_{\max}]$ 和 $[\phi_{\min}, \phi_{\max}]$，将球坐标重新归一化到全分辨率栅格：

$$\tilde{u}_i = \Big\lfloor \frac{\theta_i - \theta_{\min}}{\Delta_\theta} W \Big\rfloor, \quad \tilde{v}_i = \Big\lfloor \frac{\phi_i - \phi_{\min}}{\Delta_\phi} H \Big\rfloor$$

其中 $\Delta_\theta = \theta_{\max} - \theta_{\min}$，$\Delta_\phi = \phi_{\max} - \phi_{\min}$。该投影机制无需相机内参，最大化像素利用率，同时保持角度连续性和几何结构保真度。

### 核心模块二：Denoising-Agnostic Coupled ControlNet

标准 ControlNet 通过零卷积 $\mathcal{Z}(\cdot)$ 将条件特征注入 Stable Diffusion U-Net 解码器：

$$\mathbf{y}_t = \mathrm{SD}_{\mathrm{enc}}(\mathbf{x}_t) + \mathcal{Z}\big(\mathrm{CN}_{\mathrm{enc}}(\mathbf{x}_t + \mathcal{Z}(\mathbf{c}))\big)$$

GM-R^2 将其扩展为耦合跨视图生成器：将源/目标 AFoV-ERP 范围图垂直拼接为统一条件 $\tilde{\mathbf{d}}^{PQ}$，并移除潜在变量注入，使 ControlNet 编码器在训练和推理阶段遵循完全相同的通路。前向过程为：

$$\tilde{\mathbf{y}}_t = \mathrm{SD}_{\mathrm{enc}}(\tilde{\mathbf{x}}_t^{PQ}) + \mathcal{Z}\big(\mathrm{CN}_{\mathrm{enc}}(\tilde{\mathbf{x}}_t^{PQ} + \mathcal{Z}(\tilde{\mathbf{d}}^{PQ}); \theta)\big)$$

### 核心模块三：生成一致性监督与去噪损失

训练时，通过球面映射将透视真值图像重投影到球面坐标，与生成的球面图像对齐。仅优化 ControlNet 编码器参数 $\theta$，冻结 Stable Diffusion 去噪器 $\epsilon_\omega$，损失函数为标准去噪损失：

$$\mathcal{L} = \mathbb{E}\left[ \left\| \epsilon_\omega\left( \tilde{\mathbf{x}}_t^{PQ}, t, \mathrm{CN}_{\mathrm{enc}}(\tilde{\mathbf{d}}^{PQ}; \theta) \right) - \epsilon_t \right\|_2^2 \right]$$

该损失将生成从像素级目标转化为几何感知的监督机制：去噪误差的梯度通过冻结的 U-Net 反向传播至 ControlNet 编码器，强制其学习对应一致的几何表示。

### 描述符提取与配准推理

推理时，从 ControlNet 编码器提取多尺度几何特征，与 FPFH 手工特征融合后经 PCA 降维得到紧凑的 3D 描述符。通过描述符最近邻搜索建立对应，最终使用 RANSAC 估计刚体变换。评估指标为旋转误差 $\mathrm{RE}$ 和平移误差 $\mathrm{TE}$：

$$\mathrm{RE} = \arccos \frac{\mathrm{Tr}(\hat{\mathbf{R}}^\top \mathbf{R}) - 1}{2}, \quad \mathrm{TE} = \|\hat{\mathbf{t}} - \mathbf{t}\|_2$$

其中 $\hat{\mathbf{R}}, \hat{\mathbf{t}}$ 为预测值，$\mathbf{R}, \mathbf{t}$ 为真值。

## 实验与关键发现

### 主实验结果

GM-R^2 在 3DMatch 和 ScanNet 两个主流基准上均取得了无监督配准的最优性能，并在多项指标上超越全监督方法。

**3DMatch 基准**（Table 1）：GM-R^2 在旋转精度上表现突出，旋转准确率 @5° 达到 96.2%，@10° 达到 98.6%，@45° 达到 99.7%。平均旋转误差为 2.0°，中位数旋转误差为 1.2°。与全监督旋转等变描述符 **PARE-Net**（Yao et al., ECCV 2024）相比，平均旋转误差降低约 2.5°。平移方面，平均平移误差为 6.4 cm，中位数为 4.0 cm，较 PARE-Net 降低约 8.6 cm。平移准确率 @5cm 为 61.4%，@10cm 为 87.8%，@25cm 为 97.1%。在倒角距离指标上同样达到可比甚至更优的水平。值得注意的是，GM-R^2 作为无监督方法，在旋转和倒角距离精度上全面超越了表中所有全监督深度描述符（如 **FCGF**（Choy et al., ICCV 2019）、**Predator**（Huang et al., CVPR 2021））。

**ScanNet 基准**（Table 2）：在更具挑战性的 ScanNet 室内场景上，GM-R^2 保持与全监督 SOTA 可比拟的性能。平均旋转误差为 7.3°，平均平移误差为 18.5 cm，倒角准确率 @10mm 达到 83.5%。考虑到 GM-R^2 完全不使用位姿真值标注，这一结果验证了生成式匹配学习范式在复杂真实场景下的鲁棒性。

**低重叠场景定性分析**（Figure 5）：在与全监督 SOTA 描述符 PARE-Net 的低重叠 ScanNet 场景定性对比中，GM-R^2 持续展现出更高的对齐精度，表明生成一致性监督能够有效应对低重叠和重复结构等困难情况。Figure 4 的 t-SNE 可视化进一步显示，GM-R^2 学习到的几何描述符在特征空间中形成了清晰对应聚类，即使在挑战性低重叠场景下，内点对应（绿色连线）仍占主导。

### 消融实验

Table 3 在 3DMatch 数据集上验证了 AFoV-ERP 投影策略和范围图分辨率的影响。

![[assets/figures/papers/paper_list_l2512_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_GM_R2_Generative/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on 3DMatch [50] dataset. (∗) denotes the default configuration*

**AFoV-ERP vs. 标准 ERP**：将 AFoV-ERP 替换为标准 ERP 后，平均旋转误差从 2.0° 退化至 3.4°，旋转准确率 @5° 从 96.2% 降至 90.1%，平移和倒角距离指标也全面下降。这验证了自适应有效 FoV 缩放对像素利用率和几何保真度的关键作用——标准 ERP 在全 360°×180° 范围内均匀离散化，大量像素浪费在空区域，导致有效分辨率不足。

**范围图分辨率敏感性**：将范围图分辨率从默认的 256 提升至 512 时，倒角距离精度有轻微改善（Chamfer@1: 84.3→86.2），但旋转和平移指标波动较小，表明 AFoV-ERP 在较低分辨率下已能提供足够丰富的几何条件。这一现象说明生成一致性监督对分辨率的敏感度低于传统监督方法，可能得益于扩散模型的多尺度去噪先验的鲁棒性。

### 失败模式与局限性

尽管 GM-R^2 取得了优异的实验结果，分析中揭示了以下局限：

1. **大模型依赖**：方法依赖预训练 Stable Diffusion 和 ControlNet 权重，计算和存储开销显著高于轻量级全监督描述符（如 FCGF），可能限制实时部署场景（如嵌入式 SLAM 系统）的适用性。

2. **投影退化风险**：AFoV-ERP 假设点云已转换到相机坐标系且能可靠计算有效 FoV 边界。在传感器运动剧烈或遮挡严重导致点云极度稀疏、FoV 边界估计不准确的极端情况下，投影质量可能退化，进而影响生成一致性监督的有效性。

3. **多传感器数据依赖**：训练和推理仍需成对点云及对应 RGB 图像，未完全摆脱对多传感器数据的依赖。纯几何驱动的无监督生成式匹配（不依赖 RGB）仍是一个开放问题。

4. **动态场景泛化性未知**：当前实验集中在静态室内场景（3DMatch、ScanNet），方法在动态场景和 LiDAR SLAM 在线更新场景下的表现尚未验证。

> **注意**：上述失败模式部分基于方法设计的内在假设推演，具体退化程度的量化实验（如极低重叠率下的精度衰减曲线）在现有分析材料中未提供，建议查阅原文补充验证。

![[assets/figures/papers/paper_list_l2512_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_GM_R2_Generative/figures/004_Table_1.jpg]]
*Table 1: Comparison of the methods on rotation, translation, and Chamfer distance on 3DMatch [50] benchmark dataset. (∗), (△) and (♢) denote the traditional, unsupervised, and fully-supervised deep geometric descriptors, respectively*

![[assets/figures/papers/paper_list_l2512_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_GM_R2_Generative/figures/005_Figure_4.jpg]]
*Figure 4: The t-SNE visualization of the*

![[assets/figures/papers/paper_list_l2512_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_GM_R2_Generative/figures/006_Table_2.jpg]]
*Table 2: Comparison of the methods on rotation, translation, and Chamfer distance on ScanNet [5] benchmark dataset. (∗), (△) and (♢) denote the traditional, unsupervised, and fully-supervised deep geometric descriptors, respectively*

## 定位与知识库关联

### 1. 与全监督几何描述符的关系

GM-R^2 直接对标的核心基线是当前全监督几何描述符的 SOTA 水平。这些方法依赖昂贵的真值位姿标注来驱动对比学习或度量学习，构成 GM-R^2 试图打破的“标注瓶颈”。

- **FCGF**（Choy et al., ICCV 2019）：全监督深度几何描述符的里程碑工作，使用稀疏全卷积网络在点云体素表示上学习逐点特征，通过对比损失利用真值对应关系。GM-R^2 在 3DMatch 上以无监督方式全面超越其配准精度（Table 1），证明生成一致性监督可以替代显式对应标注。
- **Predator**（Huang et al., CVPR 2021）：面向低重叠场景的全监督配准方法，通过重叠注意力机制增强描述符对重叠区域的敏感度。GM-R^2 在低重叠 ScanNet 场景中无需任何位姿标注即可达到与之可比甚至更优的对齐精度（Figure 5, Table 2），表明跨视图生成一致性隐式编码了重叠结构信息。
- **PARE-Net**（Yao et al., ECCV 2024）：全监督旋转等变描述符的最新代表，通过 SO(3) 等变网络设计提升旋转鲁棒性。GM-R^2 在 3DMatch 上将平均旋转误差降低约 2.5°、平均平移误差降低约 8.6 cm（Table 1），且定性可视化显示在低重叠场景中配准精度更高（Figure 5），验证了无监督生成式范式对全监督等变设计的竞争力。

这些对比表明，GM-R^2 并非在现有全监督框架内做增量改进，而是通过引入生成一致性这一新的监督信号源，从根本上绕开了位姿标注的依赖。

### 2. 与无监督配准/描述符方法的关系

在无监督赛道，GM-R^2 相对于已有方法的核心差异在于监督信号的来源和形式。

- **PPF-FoldNet**（Deng et al., ECCV 2018）：基于点对特征（PPF）的自编码器重建来学习无监督局部描述符，但缺乏跨帧一致性约束，难以处理大视角变化。GM-R^2 通过跨视图图像生成将帧间结构一致性引入训练，在 3DMatch 上精度显著领先（Table 1）。
- **FMR**（Huang et al., CVPR 2020）：半监督特征匹配方法，利用少量标注和大量无标注数据。GM-R^2 完全不需要位姿标注，且精度更高，验证了生成一致性信号比半监督特征传播更有效。
- **CEMNet**（Jiang et al., ICCV 2021）：基于强化学习的无监督配准方法，通过试错搜索变换空间。GM-R^2 通过生成式目标直接学习对应一致表示，避免了 RL 训练的不稳定性和高方差问题。

GM-R^2 在无监督方法中的独特定位在于：它不依赖点云自身的重建或自监督变换预测，而是将 2D 图像生成作为隐式几何监督的桥梁，利用预训练扩散模型的强大先验来约束 3D 特征学习。

### 3. 技术组件的知识溯源

GM-R^2 的三个核心组件各自有明确的技术渊源，但组合方式构成了其独特性。

- **AFoV-ERP 投影**：源于标准等距矩形投影（ERP），但解决了其“全 FoV 均匀离散化导致有效区域像素利用率低”的固有问题。AFoV-ERP 通过自适应缩放有效 FoV 到全分辨率网格，实现了无内参的高分辨率范围图生成。这一设计使得投影不再依赖传感器标定参数，增强了跨传感器泛化能力。
- **去噪无关耦合 ControlNet**：继承自 ControlNet（Zhang et al., ICCV 2023）的条件生成架构，但做了两项关键修改：(1) 将单视图条件扩展为源-目标耦合范围图，实现跨视图生成；(2) 移除潜在变量注入，使训练和推理阶段编码器路径完全一致。这种“去噪无关”设计确保了训练时优化的几何特征与推理时提取的特征来自同一分布，消除了训练-推理不一致性。
- **生成一致性损失**：形式上采用标准扩散去噪损失，但其监督意义被重新定义——去噪目标 $\epsilon_t$ 不再服务于图像生成质量，而是作为几何特征提取器的隐式监督信号。只有对应关系一致的点云才能驱动生成器产生跨视图一致的图像，因此最小化去噪误差等价于强制编码器学习对应一致的描述符。

### 4. 适用边界与局限性

尽管 GM-R^2 在无监督设定下展现了强大的配准能力，但其适用边界受限于以下因素：

1. **多模态数据依赖**：训练和推理均需要成对点云及对应的 RGB 图像。在缺乏视觉传感器的纯 LiDAR 场景中，该方法无法直接应用。是否可能仅利用点云几何（如反射率或纯几何渲染）实现类似的生成式监督，仍是一个开放问题。

2. **AFoV-ERP 的退化风险**：AFoV-ERP 假设点云已转换到相机坐标系且能可靠计算有效 FoV 边界。在传感器剧烈运动、严重遮挡或非结构化环境中，有效 FoV 估计可能不准确，导致投影质量下降。该方法能否处理极端 FoV 或非完整球面投影的更一般传感器，有待验证。

3. **计算与存储开销**：方法依赖预训练 Stable Diffusion 大模型作为生成器骨干。虽然训练时仅优化 ControlNet 编码器，但推理时仍需完整的 U-Net 前向传播来提取多尺度特征，这可能影响实时部署和资源受限场景的适用性。

4. **小规模数据的泛化能力**：去噪无关的 ControlNet 编码器在训练中利用了预训练扩散模型的强先验，但在目标域数据量极小的情况下，其泛化能力是否会退化，尚未得到充分验证。

### 5. 开放问题

GM-R^2 的范式创新引出了若干值得后续探索的方向：

- **纯几何生成式匹配**：能否仅利用点云几何信息（不依赖 RGB 图像）实现无监督生成式匹配？例如，通过可微渲染或神经辐射场生成跨视角几何视图作为监督信号。
- **动态场景与在线 SLAM**：当前方法面向静态场景的离线配准。能否扩展到动态场景，或集成到 LiDAR SLAM 系统中实现在线更新，是一个有实际价值的问题。
- **更一般的传感器模型**：AFoV-ERP 目前假设球面投影模型。对于非标准传感器（如固态激光雷达的非均匀扫描模式），如何设计相应的自适应投影机制？
- **生成一致性信号的理论分析**：当前工作从经验上验证了生成一致性监督的有效性，但缺乏对“何种程度的跨视图生成质量足以保证对应一致性”的理论刻画，这可能是未来研究的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/GM_R_2_Generative_Matching_Learning_for_Unsupervised_Geometric_Representation_and_Registration.pdf]]

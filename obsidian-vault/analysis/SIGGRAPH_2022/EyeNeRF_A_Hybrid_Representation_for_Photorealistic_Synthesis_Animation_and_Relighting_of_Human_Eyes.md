---
title: "EyeNeRF: A Hybrid Representation for Photorealistic Synthesis, Animation, and Relighting of Human Eyes"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/EyeNeRF_A_Hybrid_Representation_for_Photorealistic_Synthesis_Animation_and_Relighting_of_Human_Eyes.pdf
project_link: "https://trimsh.org/"
code_link: null
aliases:
- EyeNeRF
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/representation_self_supervised_transfer
core_operator: 采用混合表示：显式参数化眼球网格进行光线追踪以精确计算反射和折射，同时用隐式神经体积建模眼周区域；并引入NeRF-SHL网络预测球谐系数以高效近似光照传输，实现视角/注视/光照的分离控制。
primary_logic: 人眼区域的异质性需要差异化的几何与外观表示：角膜的镜面反射与折射最适合用显式表面模型和光线追踪处理，而散射性的巩膜、毛发和变形皮肤更适合用隐式体积表示，并通过球谐函数将光照与环境解耦，从而实现可控的注视动画和重光照。
claims:
- 混合表示结合了显式眼球网格和隐式体积，能够建模反射、折射和毛发结构。
- 显式眼球表面允许通过光线追踪建模高频角膜镜面反射和折射。
- 移除显式眼球模型导致在新视角/新光照下出现严重伪影。
- NeRF-SHL预测漫反射和镜面反射球谐系数，与环境光球谐积分相乘实现重光照。
---

# EyeNeRF: A Hybrid Representation for Photorealistic Synthesis, Animation, and Relighting of Human Eyes

> [!tip] 核心洞察
> 人眼区域的异质性需要差异化的几何与外观表示：角膜的镜面反射与折射最适合用显式表面模型和光线追踪处理，而散射性的巩膜、毛发和变形皮肤更适合用隐式体积表示，并通过球谐函数将光照与环境解耦，从而实现可控的注视动画和重光照。

| 字段 | 内容 |
|------|------|
| 中文题名 | EyeNeRF：一种用于人眼真实感合成、动画与重光照的混合表示 |
| 英文题名 | EyeNeRF: A Hybrid Representation for Photorealistic Synthesis, Animation, and Relighting of Human Eyes |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2206.08428) · [Project](https://trimsh.org/) · [paper](https://arxiv.org/abs/2206.08428") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/representation_self_supervised_transfer |
| Method | EyeNeRF |
| Dataset |  |

> [!tip] 效果简介
> - 新视角合成 上，MSE ↓ / SSIM ↑ 7.67e-4 / 0.863 vs 消融条件（简化架构/无眼球模型等，见Table 1） (优于或相当所有消融)。
> - 重注视（新注视方向） 上，MSE ↓ / SSIM ↑ 7.23e-4 / 0.857 vs 消融条件（同上） (优于或相当所有消融)。
> - 重光照（新环境光） 上，MSE ↓ / SSIM ↑ 7.23e-4 / 0.829 vs 消融条件（同上） (优于或相当所有消融)。

## 概要

人眼区域的真实感建模面临根本性异构挑战：角膜表现为刚体旋转与高频镜面反射/折射，而眼周皮肤、睫毛等则为非刚性变形与散射介质，现有方法无法统一处理这两类迥异的几何与外观特性。**EyeNeRF** 提出一种混合表示——用显式参数化眼球网格进行光线追踪以精确计算反射和折射，同时用隐式神经体积建模眼周区域，并通过 **NeRF-SHL** 网络预测球谐系数实现与环境光照的解耦，从而支持视角、注视方向与光照条件的分离控制。实验表明，该方法在新视角合成、重注视与重光照三项任务上均达到或优于消融基线（MSE 约 $7\times10^{-4}$，SSIM 约 0.83–0.86），消融实验证实移除显式眼球模型会导致反射/折射严重伪影。该工作属于神经渲染与图形学几何表示的交叉，核心贡献在于根据人眼区域的物理异质性选择差异化表示，并将球谐预积分引入 NeRF 框架以实现高效重光照。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

人眼区域的真实感建模面临一个根本性的异构难题：眼球本身是刚性的旋转体，其角膜表面产生高频镜面反射和折射；而眼周区域（皮肤、眼睑、睫毛）则是非刚性变形、散射主导的软组织（图2）。现有方法要么仅处理眼球的反射/折射（如传统光线追踪），要么仅建模眼周的非刚性变形（如NeRF体积表示），缺乏一个统一框架能够同时处理这两种截然不同的物理特性，并实现视角、注视方向和光照的分离控制。

EyeNeRF的核心洞察在于：**不同的物理过程需要差异化的几何与外观表示**。角膜的镜面反射和折射最适合用显式表面模型配合光线追踪精确计算，而散射性的巩膜、毛发和变形皮肤更适合用隐式体积表示。通过将光照传输函数展开为球谐系数并预计算环境光积分，可以实现高效的重光照。

### 混合表示架构

EyeNeRF采用一种**显式-隐式混合表示**，将人眼区域分解为两个互补的子系统：

**1. 显式眼球表面模型（Explicit Eyeball Model）**

眼球表面采用基于LeGrand眼模型的参数化网格表示，由两个重叠球体构成（分别对应角膜和巩膜）。该显式网格具有以下关键属性：
- 每个顶点允许独立的位移向量，在训练过程中优化以捕捉个体眼球的精确形状
- 支持高效的光线-表面求交计算，用于生成反射射线和折射射线
- 眼球运动建模为每帧的6自由度刚体变换（旋转+平移），实现注视方向的精确控制

**2. 隐式神经体积表示（Implicit Volumetric Representation）**

眼周区域和眼球内部采用可变形的隐式体积表示，其核心是一个称为**NeRF-SHL**的神经网络（图4）。该网络在规范空间（canonical NeRF space）中为每个3D点预测：
- 不透明度 $\sigma$（通过ReLU激活保证正值）
- 反照率 $\mathbf{a}$（通过Sigmoid约束到[0,1]）
- 漫反射球谐系数 $\mathbf{c}^{\text{diff}}$
- 镜面反射球谐系数 $\mathbf{c}^{\text{spec}}$

网络架构分为三个分支（图4）：
- **第一分支**：仅输入规范空间点的位置编码，预测不透明度和反照率
- **第二分支**：额外输入世界空间点的位置编码，预测漫反射球谐系数，以更好地建模阴影效应
- **第三分支**：加入视线方向，预测视角依赖的镜面反射球谐系数

### 变形处理机制

为处理眼周区域的非刚性变形，EyeNeRF学习了一个**变形场MLP**（warp field），将世界空间的采样点映射到规范NeRF空间。具体而言：
- 对于**反射射线和角膜前射线**上的采样点，应用学习的变形场进行非刚性扭曲
- 对于**折射射线**（进入眼球内部）上的采样点，应用眼球刚体变换的逆变换，将其转换到眼球的规范空间

这种设计使得眼球内部的巩膜、虹膜等结构在眼球旋转时保持刚性，而眼周皮肤和毛发则允许平滑的非刚性变形。

### 光照模型与重光照机制

EyeNeRF的关键创新在于将**球谐光照传输**与神经体积表示相结合，实现高效的视角无关重光照。

**理论基础**：标准光传输方程（无发射项）为：
$$L_o(\mathbf{x}, \omega_o) = \int_\Omega f(\mathbf{x}, \omega_o, \omega_i) L_i(\mathbf{x}, \omega_i) d\omega_i$$

在环境光照假设下，入射光替换为环境图 $E(\omega_i)$：
$$L_o(\mathbf{x}, \omega_o) = \int_\Omega f_{\text{tot}}(\mathbf{x}, \omega_o, \omega_i) E(\omega_i) d\omega_i$$

**球谐近似**：将总光传输函数 $f_{\text{tot}}$ 用球谐基函数展开：
$$f_{\text{tot}}(\mathbf{x}, \omega_o, \omega_i) \approx \sum_{l=0}^{\text{order}} \sum_{m=-l}^{l} c_{lm}(\mathbf{x}, \omega_o) Y_{lm}(\omega_i)$$

其中 $c_{lm}$ 是NeRF-SHL网络预测的球谐系数。重排积分顺序后得到：
$$L_o(\mathbf{x}, \omega_o) \approx \sum_{l=0}^{\text{order}} \sum_{m=-l}^{l} c_{lm}(x, \omega_o) \left( \int_\Omega Y_{lm}(\omega_i) E(\omega_i) d\omega_i \right)$$

**关键分离**：括号内的环境图球谐积分项与网络预测的系数解耦，可以**预计算**。在渲染时，只需将预计算的环境球谐系数与网络输出的传输系数相乘即可，避免了每个采样点重新积分的巨大开销。

### 光线追踪与体积渲染管线

EyeNeRF的渲染流程（图5）结合了传统光线追踪与神经体积渲染：

1. **光线求交**：从相机发射射线，与显式眼球网格求交，计算反射射线 $\mathbf{r}_r$ 和折射射线 $\mathbf{r}_e$
2. **分层采样**：在反射射线、折射射线和角膜前射线上分别采样3D点
3. **空间变换**：
   - 反射射线和角膜前射线的采样点通过变形场映射到规范空间
   - 折射射线的采样点通过眼球刚体变换的逆变换映射到规范空间
4. **网络查询**：对每个规范空间点查询NeRF-SHL，获得不透明度、反照率和球谐系数
5. **光照积分**：将球谐系数与预计算的环境光球谐系数相乘，并与反照率合成得到RGB颜色
6. **体积渲染**：沿每条射线累积颜色和不透明度：
   $$\alpha_i = e^{-\sigma_i \delta_i}, \quad T_t = \prod_{i=0}^{t-1} \alpha_i, \quad C(\mathbf{r}) = \sum_{t=0}^{N_S} T_t (1-\alpha_t) \mathbf{c}_t$$
7. **菲涅尔合成**：使用菲涅尔因子 $f$ 合并反射与折射射线的贡献：
   $$\alpha_{\text{comb}} = \alpha_k (1-f), \quad c_{\text{comb}} = \frac{ (1-\alpha_k) c_k + f \alpha_k \mathcal{C}(\mathbf{r}^{\prime}) }{ \alpha_{\text{comb}} }$$

### 三阶段训练策略

EyeNeRF采用分阶段训练以稳定优化过程：

**第一阶段**：使用简化架构（图7）训练，此时漫反射球谐系数仅依赖规范空间点（不输入世界空间点），加速初始收敛。此阶段主要优化眼球姿态、形状和粗略的外观表示。

**第二阶段**：切换到完整架构（图4），引入世界空间点输入以建模阴影，并加入镜面反射分支。此阶段精细优化眼周区域的外观质量。

**第三阶段**：联合优化所有参数，包括眼球网格顶点位移、变形场MLP和NeRF-SHL网络权重。

训练损失函数包括：
- **图像重建损失**：在sRGB空间计算粗糙网络和精细网络输出与真实图像的L2距离
- **非负球谐损失**：惩罚负的球谐响应值，避免出现无光照的"死区"：
  $$l_{\text{nonneg}} = \mathbb{E}_{\omega_i \sim \Omega} \left[ -\min(0, \sum_{l=0}^{\text{order}} \sum_{m=-l}^{l} c_{lm}(\mathbf{x}, \omega_o) Y_{lm}(\omega_i)) \right]$$

### Changed Slots 总结

相对于现有方法，EyeNeRF在四个关键设计槽位上进行了根本性改变：

| 设计槽位 | 基线方案 | EyeNeRF方案 | 因果作用 |
|---------|---------|------------|---------|
| 眼球表面表示 | 隐式体积（NeRF）或无模型 | 显式参数化网格+光线追踪 | 精确计算反射/折射，避免体积表示的模糊伪影 |
| 外观模型 | 视角依赖的辐射场 | NeRF-SHL预测球谐系数 | 将光照与环境解耦，实现重光照 |
| 变形处理 | 仅刚体变换 | 变形场MLP+眼球刚体变换 | 同时处理非刚性皮肤变形和刚性眼球旋转 |
| 光照集成 | 隐式包含在辐射中 | 环境图球谐预计算+系数乘法 | 高效重光照，避免每点重新积分 |

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2206_08428/figures/005_Figure_4.jpg]]
*Figure 4: The architecture for NeRF-SHL can be divided intro three branches. The first branch predicts opacity and albedo from the 3D point in canonical NeRF space. For the second branch, we additionally feed the 3D world-space point as input to better model shadowing. Lastly, we add the view direction input for the branch that predicts specular SH coefficients*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2206_08428/figures/008_Figure_7.jpg]]
*Figure 7: To improve initial network convergence, we start training with the simplified architecture shown above, and later on continue to train the full architecture as depicted in Fig. 4. The main difference is that here the diffuse SH coefficients only depend on the the 3D NeRF-Space points, where in the full model they also depend on the 3D World-Space points, in order to better model shadowing*

## 实验与关键发现

EyeNeRF 的实验验证围绕三个核心任务展开：新视角合成、重注视（novel gaze）和重光照（novel illumination）。所有定量评估均在 300×300 的眼部裁剪区域上进行，排除了背景等不相关区域的干扰。完整方法在三个任务的 MSE 和 SSIM 指标上均优于或相当所有消融设置（Table 1），但实验设置与各基线方法存在重要差异，需审慎解读对比结论。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2206_08428/figures/012_Table_1.jpg]]
*Table 1: Results from our quantitative ablation study. Our full method outperforms or achieves comparable performance with the ablation settings on most metrics for all 3 tasks*

### 主结果与指标对比

在定量消融研究中，完整 EyeNeRF 在新视角合成任务上达到 MSE = 7.67×10⁻⁴、SSIM = 0.863；在重注视任务上达到 MSE = 7.23×10⁻⁴、SSIM = 0.857；在重光照任务上达到 MSE = 7.23×10⁻⁴、SSIM = 0.829。这些数值均优于或持平于各消融变体（Table 1）。

与外部基线的定性比较揭示了方法的相对优势，但对比条件并不完全公平：
- 与 **He et al. 2019** 在注视重定向上的对比（Fig. 10）显示，EyeNeRF 的注视控制更精确且身份保持更好。但需注意，He et al. 仅需单张输入图像，而 EyeNeRF 依赖多视角和手持灯光采集，设置复杂度显著更高。
- 与 **Schwartz et al. 2020**（TOG）的对比（Fig. 11）表明，EyeNeRF 能捕捉高频皮肤/眼球反射并合成睫毛、眉毛等薄结构，而 Schwartz 等人的方法不支持重光照和高频反射捕捉。这一优势直接源于显式眼球网格与光线追踪的设计。
- 与 **Pandey et al. 2021**（SIGGRAPH）的重光照对比（Fig. 12）显示，EyeNeRF 在眼睛区域的环境反射质量更高，验证了 NeRF-SHL 球谐光照解耦的有效性。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2206_08428/figures/010_Figure_10.jpg]]
*Figure 10: We compare with [He et al. 2019] for regazing. EyeNeRF controls the gaze more accurately and preserves the identity better. Please note that [He et al. 2019] operates on a single input image only, where ours is a much more involved setting*

### 关键消融实验

消融实验（Fig. 8, Table 1）系统验证了各设计选择的因果贡献：

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2206_08428/figures/009_Figure_8.jpg]]
*Figure 8: Ablation Study. We evaluate different design choices for EyeNeRF. Without the explicit eyeball model, the volumetric model fails to represent reflection and refraction, leading to strong artifacts. Without the first training stage, the eyeball pose and shape is inaccurate (see novel side view) hence many specular effects on the eyeball are not reproduced. Without the second training stage, the quality of the periocular region is reduced, yielding significant blur in the images. Results from the simplified architecture or without disconnect look similar to EyeNeRF in the training view. However, they exhibit artifacts on the iris and sclera for novel views or novel illumination conditions*

**移除显式眼球模型**是最具决定性的消融。当仅使用隐式体积表示时，模型无法表示角膜的反射和折射，在新视角和新光照下出现严重伪影。这直接证实了核心假设：角膜的高频镜面反射和折射必须通过显式表面模型和光线追踪来处理，纯体积表示无法胜任。

**跳过第一阶段训练**（仅训练完整架构）导致眼球姿态和形状估计不准确。在侧面新视角下，许多镜面效果无法复现，因为眼球几何未充分收敛。Fig. 13 可视化了训练过程中眼球姿态和形状的优化过程：初始估计（蓝色）经过训练后被显著细化（橙色），巩膜表面变得凹凸有致而角膜保持光滑，合成的高光从初始偏移逐步与真实高光重合。

**跳过第二阶段训练**（仅使用简化架构，Fig. 7）则主要损害眼周区域的质量，图像出现显著模糊。这是因为简化架构中漫反射球谐系数仅依赖规范空间点，无法充分建模世界空间中的阴影效应。

**使用简化架构或不断开虚线连接**（Fig. 4 中世界空间点到漫反射分支的输入）时，在训练视角下结果与完整 EyeNeRF 相似，但在新视角或新光照条件下，虹膜和巩膜区域出现伪影。这表明世界空间条件输入对于泛化到未见光照和视角至关重要。

### 失败模式与适用边界

EyeNeRF 存在若干明确记录的局限性：

**巩膜高光外观不真实**（Fig. 9）：虽然优化后巩膜上高光的整体位置正确，但其外观在视觉上偏离真实。根本原因是显式眼球参数模型的空间分辨率不足以表示泪液和结膜引起的高频表面变化。这是混合表示的固有瓶颈——显式网格的表示能力受限于其顶点密度。

**不支持面部表情**：当前方法无法建模闭眼、眯眼、微笑等表情变化，也无法分离注视与表情。这限制了其在完整面部动画管线中的应用。

**未建模动态细节**：结膜与巩膜的相对滑动、瞳孔扩张等解剖学动态过程未被纳入参数化模型。

**光传输的边界**：方法无法处理超越角膜反射的高频光传输效应，如睫毛遮挡和皮肤上的镜面反射。这些效应在 NeRF-SHL 的球谐近似框架下难以捕捉。

**计算开销极高**：训练需约 4 天（8 块 NVIDIA V100 GPU），渲染一帧 800×800 图像约需 30 秒，远未达到实时应用要求。这是混合光线追踪与体积渲染架构的固有代价。

### 证据强度总结

支撑核心主张的证据链较为完整：显式眼球模型的必要性由 Fig. 8 的消融直接证实；NeRF-SHL 的光照解耦能力由重光照任务的定量结果和 Fig. 12 的定性对比支持；两阶段训练策略的必要性由对应消融的模糊和伪影结果验证。但需注意，与外部基线的对比缺乏统一的定量基准，且采集设置差异较大，这些对比更适合理解为能力展示而非严格性能排序。巩膜高光真实性问题（Fig. 9）和计算开销是方法当前最明确的两个实用边界。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2206_08428/figures/007_Figure_6.jpg]]
*Figure 6: left: Our static setup consists of 4 high-quality cameras (red) arranged in a diamond-shape and surrounded by 8 illuminators (yellow). right: A set of AR markers is attached to the forehead of the subject to track head movement as well as relative camera motion*

## 定位与知识库关联

EyeNeRF 的核心定位在于**改变了“眼部区域几何与外观的统一表示”这一关键 slot**。在它之前，眼区建模工作要么聚焦于眼球的镜面反射与折射（以显式表面模型为主），要么处理眼周皮肤的非刚性变形与毛发结构（以隐式体积或图像变换为主），但从未有一个框架能同时高质量地完成这两件事。EyeNeRF 用一个**混合表示**填补了这一空白：眼球表面采用显式参数化网格进行光线追踪，精确计算角膜反射与折射；眼周区域及眼球内部则使用隐式变形神经体积建模，并通过 NeRF-SHL 网络预测球谐系数来实现与环境光照的解耦。这一 slot 的变更直接解锁了三项下游能力——新视角合成、注视重定向和重光照——且这三者可以在同一模型中任意组合。

### 相对已有方法的本质差异

- **相对 He et al. 2019（注视重定向）**：该方法仅需单张输入图像，通过图像域操作实现注视重定向，不建模三维几何与光照。EyeNeRF 则建立在多视角、多光照的采集设置之上，显式建模了眼球的三维表面与眼周体积，因此注视控制更精确、身份保持更好（见 Fig. 10）。差异的本质在于：前者在图像空间操作，后者在三维表示空间操作。

- **相对 Schwartz et al. (TOG 2020)**：该方法支持视角合成与注视控制，但采用纯隐式体积表示，无法捕捉高频角膜反射与折射，也不能合成睫毛、眉毛等薄结构，且不支持重光照（见 Fig. 11）。EyeNeRF 通过引入显式眼球表面和光线追踪，直接改变了“几何表示”这一 slot，从而获得高频镜面效果和薄结构建模能力；同时通过 NeRF-SHL 将光照从辐射场中显式解耦，实现了 Schwartz et al. 所不具备的重光照功能。

- **相对 Pandey et al. (SIGGRAPH 2021)**：该方法支持重光照，但眼睛区域的环境反射质量有限（见 Fig. 12）。EyeNeRF 的改进在于将球谐光照积分与显式眼球光线追踪结合：角膜反射/折射由物理光线追踪处理，漫反射和镜面反射则通过 NeRF-SHL 预测的球谐系数与环境图预计算球谐积分相乘得到。这种“物理光线追踪 + 球谐近似”的混合光照方案，比 Pandey et al. 的纯球谐近似更准确地捕捉了眼睛特有的高频环境反射。

### 知识库挂载点

EyeNeRF 在知识图谱中的挂载点可以从以下维度定位：

1. **神经渲染与神经辐射场（NeRF）谱系**：EyeNeRF 继承并扩展了 NeRF 的体积渲染管线（Eq. 6），同时引入了变形场（warp field）将世界空间点映射到规范空间，这与 Nerfies (Park et al., ICCV 2021) 等动态 NeRF 工作共享技术基因。其关键扩展在于：用显式网格替代了眼球区域的隐式表面，形成了“混合 NeRF”这一新子类。

2. **可重光照神经表示**：NeRF-SHL 网络输出球谐系数，通过预计算环境图球谐积分实现高效重光照（Eq. 5），这与 NeRV (Srinivasan et al., CVPR 2021) 等可重光照 NeRF 工作一脉相承。EyeNeRF 的独特性在于：将球谐近似仅应用于漫反射和镜面反射分量，而将角膜的高频反射/折射留给显式光线追踪处理，避免了纯球谐近似对高频光传输的欠拟合。

3. **眼部建模与注视重定向**：在计算机图形学中，眼部建模长期依赖参数化眼球模型（如 LeGrand 眼模型）。EyeNeRF 将这一传统与神经表示结合，通过学习得到的每顶点位移来优化眼球形状（Fig. 13），并将眼球 6-DoF 刚体变换与眼周变形场统一在同一个可微渲染框架中。这为后续的高保真数字人眼部建模提供了“显式眼球 + 隐式眼周”的范式参考。

4. **基于物理的可微渲染**：EyeNeRF 在眼球表面执行光线追踪以计算反射和折射射线，并用菲涅尔方程合并反射与折射贡献（Sec. 4.2.4），这使其与可微路径追踪（如 Mitsuba 生态）产生关联。但其创新在于：仅在需要高频物理精度的区域（角膜）使用光线追踪，其余区域使用高效的体积渲染，实现了精度与效率的折中。

### 适用边界

EyeNeRF 的适用边界由以下因素界定：

- **采集要求高**：需要 4 台高质量相机和 8 个可控光源的多视角、多光照数据（Fig. 6），以及 AR 标记进行头部跟踪。这限制了其在消费级场景的直接应用。
- **不支持表情**：当前模型仅建模注视变化，无法处理眨眼、眯眼、微笑等面部表情，因此不能用于完整的数字人面部动画。
- **计算开销大**：训练需约 4 天（8 块 V100 GPU），渲染一帧 800×800 图像约需 30 秒，远未达到实时。
- **高频细节不足**：显式眼球模型的空间分辨率不足以表示泪液和结膜引起的高频表面变化，导致巩膜反射外观不真实（Fig. 9）；睫毛遮挡和皮肤高频镜面反射等更复杂的光传输效应也未建模。

### 后续启发与开放方向

EyeNeRF 为后续研究指明了几个高价值方向：

- **混合表示的泛化**：将“显式表面 + 隐式体积”的混合范式推广到其他人脸区域（如嘴唇、牙齿）或其他具有异质几何/外观特性的对象。
- **高效化**：利用 Instant NGP (Müller et al., SIGGRAPH 2022) 等高效神经表示加速训练和渲染，推动实时应用。
- **表情扩展**：将面部表情参数（如 blendshape 系数）纳入变形场，实现注视与表情的解耦控制。
- **更精细的眼球模型**：提高眼球网格分辨率，或引入微几何表示（如法线贴图、位移贴图），以捕捉泪液膜和结膜的高频细节。
- **简化采集**：探索从更稀疏的输入（如单目视频、环境光照）中重建眼部混合表示的方法，降低使用门槛。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/EyeNeRF_A_Hybrid_Representation_for_Photorealistic_Synthesis_Animation_and_Relighting_of_Human_Eyes.pdf]]
---
title: Authentic Volumetric Avatars From a Phone Scan
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Authentic_Volumetric_Avatars_From_a_Phone_Scan.pdf
project_link: "https://www.cs.rochester.edu/u/lchen63"
code_link: null
aliases:
- DLAD
- AVAFPS
tags:
- SIGGRAPH_2022
- topic/benchmarks_datasets_evaluation
core_operator: 在实验室光场数据上预训练的、可适配的深度光照模型（增益/偏置映射生成网络），结合在目标场景少量关键帧上的领域自适应微调，使模型能够准确建模并补偿复杂光照差异。
primary_logic: 通过将光照的变化表示为依赖于姿态、视角和表情的增益与偏置映射，并利用基于物理的光场数据学习这种映射的生成网络，再通过小样本自适应将其迁移到自然场景，从而在保持高保真面部追踪的同时鲁棒地解耦光照。
claims:
- 所提方法在L2、SSIM、PSNR和CSIM四个指标上均取得最优，显著优于I2ZNet及其他对比方法
- 消融实验表明，预训练光照模型和光照自适应两个组件对跟踪精度有显著贡献，去掉预训练后L2从11.35升至14.88，去掉自适应后升至18.03
- 仅需48帧关键帧即可达到与全部帧接近的自适应效果，验证了小样本自适应的有效性
- In-the-wild test set (10 subjects, various illuminations) 上 L2 (↓) = 12.59
---

# Authentic Volumetric Avatars From a Phone Scan

> [!tip] 核心洞察
> 通过将光照的变化表示为依赖于姿态、视角和表情的增益与偏置映射，并利用基于物理的光场数据学习这种映射的生成网络，再通过小样本自适应将其迁移到自然场景，从而在保持高保真面部追踪的同时鲁棒地解耦光照。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向 AR/VR 的高保真面部追踪：基于深度光照自适应 |
| 英文题名 | Authentic Volumetric Avatars From a Phone Scan |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://sites.google.com/site/zjucaochen/home) · [Project](https://www.cs.rochester.edu/u/lchen63) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Deep Lighting Adaptation for DAM |
| Dataset | In-the-wild test set |

> [!tip] 效果简介
> - In-the-wild test set (10 subjects, various illuminations) 上，L2 (↓) 12.59 vs I2ZNet (best prior method) (best among all compared)。
> - In-the-wild test set 上，SSIM (↑) 0.93 vs I2ZNet (best)；PSNR (↑) 37.93 vs I2ZNet (best)；CSIM (↑) 0.871 vs I2ZNet (best)。

## 概要

本文针对现有 3D 照片级人脸模型（如 **DAM**，Lombardi et al., TOG 2018）在 in-the-wild 视频中因复杂光照导致表情追踪失真的瓶颈，提出 **基于深度光照自适应的 DAM 扩展方法**。核心思路是：在实验室光场数据上预训练一个物理驱动的增益/偏置映射生成网络，将光照表示为依赖姿态、视角和表情的逐像素增益图 $\mathbf{g}^v$ 与偏置图 $\mathbf{b}^v$；然后在目标视频的少量关键帧上对光照编码 $\mathbf{l}$ 和网络权重 $\phi$ 进行领域自适应微调，使模型准确补偿场景光照差异。in-the-wild 注册采用三步流程——2D 关键点初始化、光照模型自适应、结合稠密光流约束的逐帧跟踪——最终在保持高保真面部细节的同时鲁棒解耦光照与表情。在包含 10 名受试者、多种光照条件的测试集上，本方法在 L2、SSIM、PSNR 和 CSIM 四项指标上均优于 **I2ZNet**（Yoon et al., CVPR 2019）等现有方法；消融实验证实，去除光场预训练或光照自适应均会导致跟踪精度大幅下降，仅 48 帧关键帧即可接近全帧自适应效果。方法定位于将可控光场先验与 in-the-wild 小样本自适应相结合，为 AR/VR 高保真虚拟化身驱动提供了新的光照鲁棒方案。

## 核心方法与创新机理

### 问题背景与核心瓶颈

基于深度外观模型（**DAM**，Lombardi et al., TOG 2018）的3D照片级人脸重建方法，虽然在实验室受控光照下能够生成高保真虚拟化身，但在自然场景（in-the-wild）视频中面临根本性挑战：**复杂光照（方向、颜色、软硬阴影、高光等）与面部刚性/非刚性运动在像素空间中高度耦合**。DAM的原始框架将光照视为均匀或仅用低阶球谐函数近似，无法建模真实世界中高频、视角依赖的光照模式，导致跟踪时表情细节丢失、纹理重建出现严重伪影。现有单目表演捕捉方法（如I2ZNet）虽尝试通过颜色校正缓解此问题，但缺乏对光照物理过程的显式建模，在极端光照下仍会失败。

### 核心洞察与创新机制

本文的核心创新在于提出了一种**可适配的深度光照模型**，其关键洞察是：**光照变化可以被表示为依赖于姿态、视角和表情的增益与偏置映射（gain/bias maps），而这些映射的生成规律可以通过在物理光场数据上预训练的神经网络来捕获，再通过目标场景的少量关键帧进行领域自适应微调，从而将实验室学到的光照先验迁移到自然场景中**。

这一设计实现了两个关键解耦：
1. **光照与运动的解耦**：光照模型G显式地将光照编码、头部姿态和全亮纹理映射为增益/偏置图，使跟踪优化可以专注于表情和姿态参数，而不被光照变化干扰。
2. **实验室先验与自然场景的桥接**：通过在光场数据上预训练获得强大的光照生成先验，再通过小样本自适应（仅需48帧）将其适配到目标场景，避免了在自然场景中从头学习光照的困难。

### 方法框架与模块顺序

整个方法建立在DAM的解码器基础之上，形成了**预训练光照模型 + 三步注册流水线**的完整框架：

#### 1. DAM基础表示（Eq. 1）

预训练的面部解码器D将表情编码 $`\mathbf{z}`$ 和视角方向 $`\mathbf{v}^v`$ 映射为3D网格 $`\hat{\mathbf{M}}`$ 和视角相关的全亮纹理 $`\hat{\mathbf{T}}^v`$：
$$ \hat{\mathbf{M}}, \hat{\mathbf{T}}^v = D(\mathbf{z}, \mathbf{v}^v) $$
该解码器在实验室光场数据上预训练，参数在后续流程中保持固定。

#### 2. 深度光照模型G（核心changed slot，Eq. 2-5）

光照模型G是一个卷积神经网络（详细结构见Figure 10），输入包括：
- 光照编码 $`\mathbf{l}`$：150维二值向量（50个光照组 × 3个颜色通道），表示场景光照配置
- 头部姿态 $`\mathbf{h}^v`$：编码头部刚体旋转与平移
- 全亮纹理 $`\hat{\mathbf{T}}^v`$：DAM解码器输出的无光照纹理

G输出与输入纹理同分辨率的增益图 $`\mathbf{g}^v`$ 和偏置图 $`\mathbf{b}^v`$：
$$ \mathbf{g}^v, \mathbf{b}^v = G(\mathbf{l}, \mathbf{h}^v, \hat{\mathbf{T}}^v; \phi) $$
重光照纹理通过逐元素运算获得：
$$ \mathbf{T}^v = \hat{\mathbf{T}}^v \odot \mathbf{g}^v + \mathbf{b}^v $$

**光场数据预训练**（Figure 2）：在包含460个可控光源和171个相机的光场系统上，采集同一受试者在不同光照配置和表情下的多视角数据。训练时，固定DAM解码器参数，联合优化光照模型权重 $`\phi`$ 和每帧表情编码 $`\mathbf{Z}`$，损失函数为：
$$ \mathcal{L}_{\mathrm{render}}(\phi, \mathbf{Z}) = \sum_{t,v} \left\| \left( I_t^v - \mathcal{R}(\mathbf{T}_t^v, \hat{\mathbf{M}}_t) \right) \odot m^v \right\|_1 $$
$$ \mathcal{L} = \mathcal{L}_{\mathrm{render}} + \lambda_{\mathrm{geo}} \sum_t \| \mathbf{M}_t - \hat{\mathbf{M}}_t \|^2 + \lambda_{\mathrm{reg}} \| \mathbf{Z} \|^2 $$
其中 $`\lambda_{\mathrm{geo}}=1.0`$ 约束网格几何一致性，$`\lambda_{\mathrm{reg}}=0.1`$ 防止表情编码过拟合。预训练耗时约36小时（NVIDIA DGX），但这是一次性开销。

#### 3. 三步in-the-wild注册流水线（Figure 3）

![[assets/figures/papers/paper_list_l10_https_sites_google_com_site_zjucaochen_home_repair/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of in-the-wild registration. We estimate the initial tracking parameters in step 1, adapt the lighting model and tracking parameters l, φ*

**Step 1：基于2D关键点的初始化**（Eq. 6）
使用现成的2D人脸关键点检测器，通过最小化模型3D关键点在图像平面上的投影与检测到的2D关键点之间的距离，初始化头部姿态和表情参数 $`\tilde{\mathbf{p}}`$：
$$ \mathcal{L}_{\mathrm{land}}(\tilde{\mathbf{p}}) = \sum_{v,i} \left\| \Pi_v \left( \tilde{\mathbf{r}} \tilde{\mathbf{M}}^{(\ell_i)} + \tilde{\mathbf{t}} \right) - L_i^v \right\|^2 $$
此步骤提供粗略的姿态和表情估计，为后续优化提供起点。

**Step 2：光照模型自适应**（核心changed slot，Algorithm 1）
在K个参考帧（关键帧）上，联合微调光照编码 $`\mathbf{l}`$、网络权重 $`\phi`$ 和跟踪参数 $`\{\mathbf{p}_k\}`$。损失函数结合像素级残差和拉普拉斯残差：
$$ \mathcal{L}_{\mathrm{pix}}(\mathbf{l}, \phi, \{\mathbf{p}_k\}) = \sum_k \left\| r_k \odot w_k \right\|_1 + \lambda_{\triangle} \left\| \triangle r_k \odot w_k \right\|_1 $$
其中 $`r_k`$ 为渲染图像与真实图像的残差，$`w_k`$ 为可见性掩码，拉普拉斯残差项增强高频细节的匹配。此步骤是**领域自适应的关键**：通过微调预训练光照模型的部分权重，使其从实验室光照分布迁移到目标场景的特定光照分布。自适应仅需约4分钟。

**Step 3：逐帧面部追踪**（Eq. 8）
对于视频的每一帧，固定光照模型G（使用Step 2微调后的参数），仅优化姿态和表情参数 $`\mathbf{p}`$。损失函数在像素损失基础上，引入**稠密光流一致性约束**：
$$ \mathcal{L}_{\mathrm{flow}}(\mathbf{p}) = \sum_{v,i} \left\| \left( \mathbf{r} \mathbf{M}^{(i)} + \mathbf{t} \right) - \Pi_v \left( \tilde{\mathbf{r}} \tilde{\mathbf{M}}^{(i)} + \tilde{\mathbf{t}} \right) - \mathbf{d}_i^v \right\|^2 $$
$$ \mathcal{L} = \mathcal{L}_{\mathrm{pix}} + \lambda_{\mathrm{flow}} \mathcal{L}_{\mathrm{flow}}, \quad \lambda_{\mathrm{flow}}=3.0 $$
光流约束的核心作用在于：通过强制当前参数生成的网格顶点与初始参数生成的网格顶点之间的运动与稠密光流 $`\mathbf{d}_i^v`$ 一致，有效约束了跟踪的时序稳定性，防止在纹理较弱区域（如脸颊）出现漂移。

### 模块间的因果链路

整个框架的因果链路清晰且层次化：

1. **DAM解码器 → 光照模型G**：解码器提供全亮纹理作为G的输入条件，G在此基础上叠加光照效应。这种设计使光照建模与几何/纹理生成解耦，G可以专注于学习光照的物理规律。

2. **光场预训练 → 自然场景自适应**：预训练阶段在已知光照配置的监督下学习 $`\mathbf{l} \rightarrow (\mathbf{g}^v, \mathbf{b}^v)`$ 的映射规律，获得强大的光照先验；自适应阶段通过微调 $`\phi`$ 和 $`\mathbf{l}`$，将先验适配到未知的自然光照。消融实验（Table 2）证明，去掉预训练后L2误差从11.35升至14.88，去掉自适应后更升至18.03，验证了两个环节的因果必要性。

3. **光照自适应 → 面部追踪**：Step 2获得的光照模型在Step 3中被固定，使得逐帧追踪的优化目标（Eq. 8）仅涉及姿态和表情参数，避免了光照与运动的耦合优化问题。Figure 4直观展示了这一递进关系：Step 1输出粗糙的化身，Step 2校正光照后纹理显著改善，Step 3进一步恢复精细的表情和视线方向。

4. **光流约束 → 时序稳定性**：光流损失将帧间运动显式编码为优化约束，使追踪结果在时序上平滑一致，尤其对快速运动和局部遮挡具有鲁棒性。

### 关键设计选择与边界条件

- **增益/偏置图 vs. 球谐光照**：Figure 7的对比表明，球谐光照无法处理复杂光照（如单侧强光、彩色光照），产生严重伪影；而增益/偏置图作为逐像素的变换，可以建模高频阴影、镜面高光等复杂光照效应。
- **视角条件化**：G以视角 $`\mathbf{v}^v`$ 为输入，使增益图能随视角变化而调整（Figure 8），正确再现镜面高光的视角依赖性。
- **小样本自适应**：Table 2显示仅需48帧关键帧即可接近全帧自适应效果（L2: 11.35 vs. 11.21），验证了方法的实用价值——用户仅需录制短暂视频即可完成个性化光照适配。
- **计算开销**：预训练36小时、自适应4分钟的开销较高，且需要为每个用户单独采集光场数据，限制了规模化应用。此外，方法假设测试视频中光照恒定，无法处理光照动态变化的场景。

![[assets/figures/papers/paper_list_l10_https_sites_google_com_site_zjucaochen_home_repair/figures/002_Figure_2.jpg]]
*Figure 2: Training the lighting model on the light-stage data. We update the lighting model G and per-frame expression code z while fixing the other parameters*

## 实验与关键发现

### 主实验结果：在自然场景测试集上全面领先

论文构建了一个包含10名受试者、覆盖多种光照条件的in-the-wild测试集，将所提方法与包括I2ZNet、MoFA、RingNet、MGCNet在内的多个state-of-the-art方法进行定量比较（Table 1）。评估采用四个互补指标：像素级L2误差（↓）、结构相似性SSIM（↑）、峰值信噪比PSNR（↑）和身份保持能力CSIM（↑）。

![[assets/figures/papers/paper_list_l10_https_sites_google_com_site_zjucaochen_home_repair/figures/011_Table_1.jpg]]
*Table 1: The quantitative evaluation on the test set. ↓/↑ denote the lower/higher, the better. The top-1 scores are highlighted*

所提方法在全部四个指标上均取得最优。以当前最佳方法**I2ZNet**（Yoon et al., CVPR 2019）为参照，本方法在L2上达到12.59，SSIM达到0.93，PSNR达到37.93，CSIM达到0.871。CSIM指标的优势表明，该方法不仅在像素级重建质量上领先，在保持人物身份特征方面同样具有显著优势——这对于AR/VR虚拟化身应用至关重要。

定性比较（Figure 5, Figure 6）进一步验证了上述结论。在侧光、顶光、混合色温等复杂光照条件下，对比方法普遍出现纹理模糊、表情丢失或身份特征扭曲的问题，而本方法能够稳定恢复嘴唇形状、注视方向等精细表情细节，且重光照虚拟化身与输入图像的光照一致性明显更优。

![[assets/figures/papers/paper_list_l10_https_sites_google_com_site_zjucaochen_home_repair/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison. We suggest to view it using a monitor for better visual quality. We selected 8 subjects from the test set with different lighting conditions, facial expression, and head motion. From left to right: (a) Captured image, (b) Abrevaya et al. [1], (c) 3DDFAv2 [15], (d) PRNet [11], (e) RingNet [37], (f) FaceScape [53], (g) Deng et al. [10], (h) MGCNet [40], and (i) our method*

![[assets/figures/papers/paper_list_l10_https_sites_google_com_site_zjucaochen_home_repair/figures/006_Figure_6.jpg]]
*Figure 6: Visual comparison between our method and I2ZNet [54] on testing video frames. From top to bottom: captured image, I2ZNet [54], and our method*

### 消融实验：预训练光照先验与领域自适应缺一不可

消融实验（Table 2, Figure 9）系统拆解了三个核心组件的贡献：

![[assets/figures/papers/paper_list_l10_https_sites_google_com_site_zjucaochen_home_repair/figures/008_Table_2.jpg]]
*Table 2: Quantitative results of the ablation study*

| 配置 | L2 (↓) | SSIM (↑) |
|------|--------|----------|
| 完整方法（48帧自适应） | 11.35 | 0.950 |
| 完整方法（全部帧自适应） | 11.21 | 0.954 |
| 去掉光场预训练 | 14.88 | — |
| 去掉光照自适应（仅用预训练模型） | 18.03 | — |

**因果链路分析**：

1. **去掉光照自适应**（即直接使用光场预训练的光照模型G处理in-the-wild视频，不做任何微调）导致误差最大，L2飙升至18.03。这揭示了核心瓶颈：实验室光场数据与自然场景之间存在显著的光照分布偏移（光源数量、环境光、色温等），预训练模型无法零样本泛化。

2. **去掉光场预训练**（即随机初始化光照模型G并在目标视频上从头训练）使L2升至14.88。这表明基于物理的光场数据所提供的强先验——包括多光源组合下的增益/偏置映射模式——对于引导模型收敛到合理的光照解空间至关重要。缺乏这一先验，仅凭少量in-the-wild帧难以学到有效的光照表示。

3. **小样本自适应效率**：仅使用48帧关键帧进行光照自适应，即可达到与使用全部帧几乎相同的效果（L2 11.35 vs. 11.21，SSIM 0.950 vs. 0.954）。这验证了领域自适应的样本效率，也说明光照模型G学到的先验结构使得微调只需少量目标域样本即可完成分布对齐。

### 光照模型表达能力的边界验证

将所提的增益/偏置图光照模型替换为传统的**球谐光照（Spherical Harmonics, SH）**模型时（Figure 7），在复杂光照条件下出现严重伪影。球谐模型只能表达低频光照变化，无法捕捉镜面高光、局部阴影等高频光照效应，而本方法的增益/偏置图可以逐像素地建模依赖于姿态和视角的复杂光照模式（Figure 8展示了不同视角下增益图的显著变化）。这一对比直接验证了选择增益/偏置图表征而非简化光照模型的必要性。

### 失败模式与适用边界

论文明确指出了方法的若干限制，这些边界条件对于理解方法的实际适用范围至关重要：

1. **受试者特异性依赖**：整个流程建立在为单个受试者采集的多视角光场数据之上，需要搭建包含460个可控光源的采集系统并训练个人化DAM模型。这导致方法难以规模化部署，每位新用户都需要重复昂贵的采集和训练流程。

2. **光照恒定假设**：测试视频假设光源在拍摄过程中保持固定。当场景光照发生动态变化时（如移动光源、室外云层变化），预训练光照模型和自适应阶段学到的固定光照编码l将不再有效。这是一个根本性的方法假设，而非工程优化问题。

3. **计算开销**：光场数据上的光照模型预训练需要36小时，in-the-wild光照自适应需要约4分钟（NVIDIA DGX）。虽然跟踪阶段可以实时运行，但前置准备的计算成本限制了交互式应用场景。

4. **单受试者验证**：所有实验仅在单个受试者的DAM模型上进行，未验证光照模型在多身份间的泛化能力。光照模式是否具有跨身份的可迁移性，以及能否训练通用光照模型，仍是开放问题。

5. **极端姿态与遮挡**：论文未系统评估大角度侧脸、严重遮挡等情况下的跟踪鲁棒性。光流约束依赖于可见网格顶点的对应关系，在遮挡区域可能引入错误约束。

## 定位与知识库关联

本文的核心贡献在于为 **DAM (Deep Appearance Models)** (Lombardi et al., TOG 2018) 这一高保真3D面部模型引入了一个可适配的深度光照模块，从而将其从受控光场环境拓展到in-the-wild单目视频的高精度追踪。相对于现有工作的本质差异可以概括为**一个关键slot的改变**：

**改变的核心slot：光照建模与补偿机制。** 基础DAM假设均匀光照或使用简单的球谐函数/颜色校正矩阵来处理光照差异，这在复杂自然光照下会导致纹理重建伪影和表情细节丢失。本文将该slot替换为一个在物理光场数据上预训练的增益/偏置图生成网络 $G$，该网络以光照编码 $\mathbf{l}$、头部姿态 $\mathbf{h}^v$、视角 $\mathbf{v}^v$ 和全亮纹理 $\hat{\mathbf{T}}^v$ 为输入，输出逐像素的增益图 $\mathbf{g}^v$ 和偏置图 $\mathbf{b}^v$，通过 $\mathbf{T}^v = \hat{\mathbf{T}}^v \odot \mathbf{g}^v + \mathbf{b}^v$ 实现重光照。这一设计的因果机制在于：增益/偏置图能够表达依赖于姿态和视角的高频光照模式（如镜面高光、阴影），而不仅仅是低频环境光，从而在解耦光照与面部几何/表情时具备更强的表达能力。

**知识库挂载点：基于物理先验的领域自适应。** 该方法在知识库中的定位是“物理数据驱动的光照先验 + 小样本领域自适应”这一技术路线的典型实例。其光照模型 $G$ 在460个可控光源的光场数据上预训练，学习的是从光照编码到增益/偏置图的通用映射能力——这是一个强物理先验。在in-the-wild部署时，仅需在目标场景的少量关键帧（如48帧）上对光照编码 $\mathbf{l}$ 和网络权重 $\phi$ 进行微调，即可将该先验迁移到自然光照环境。这种“预训练通用光照模型 + 目标域微调”的范式，与知识库中其他domain adaptation方法（如fine-tuning预训练特征提取器）在结构上相似，但独特之处在于其预训练数据来自物理光场而非自然图像，且适应的对象是光照的物理参数化表示而非语义特征。

**相对于已有方法的本质差异：**

- **vs. DAM** (Lombardi et al., TOG 2018)：DAM是本文的基础模型，提供了解码器 $D(\mathbf{z}, \mathbf{v}^v)$ 和全亮纹理生成能力，但缺乏对复杂光照的建模。本文在其上增加了光照模型 $G$ 和相应的自适应流程，将DAM从“光照受限的高保真模型”升级为“光照鲁棒的高保真模型”。改变的是光照处理slot，保留了DAM的表情编码和视角依赖纹理生成能力。

- **vs. I2ZNet** (Yoon et al., CVPR 2019)：I2ZNet是当时最先进的单目表演捕捉方法，使用MOTC颜色校正来处理光照。本文方法在L2、SSIM、PSNR和CSIM四个指标上均超越I2ZNet（Table 1），定性结果（Figure 6）也显示本文能更好地保留唇形、注视方向等细节表情。本质差异在于I2ZNet的颜色校正是一种全局/局部线性变换，无法建模与姿态和视角相关的高频光照变化；而本文的增益/偏置图是空间变化的且显式依赖于头部姿态和视角。

- **vs. 球谐光照模型**：消融实验（Figure 7）直接将本文的光照模型替换为球谐光照（SH），结果显示SH无法处理复杂光照，产生严重伪影。这验证了增益/偏置图表征相较于SH在表达能力上的优势——SH适合低频环境光，而增益/偏置图可以捕捉镜面高光、自阴影等高频现象。

- **vs. MoFA, RingNet, MGCNet等基于模型或自监督方法**：这些方法（Tewari et al., ICCVW 2017; Sanyal et al., CVPR 2019; Shang et al., arXiv 2020）通常使用低维参数化模型（如3DMM）或直接从图像回归形状，缺乏对特定人物的高保真纹理建模能力。本文的DAM基础提供了照片级真实的纹理和几何，而光照自适应进一步保证了在自然光照下该高保真模型的追踪精度。

**适用边界与局限：**

1. **人物特异性限制**：该方法需要为每个用户搭建多视角光场采集系统并训练个人化DAM模型，成本高且难以规模化。这是其与通用3DMM方法相比的根本性局限，限制了其在消费级AR/VR中的直接部署。

2. **光照恒定假设**：测试视频中假设光源固定，光照模型自适应后不再更新。对于光照动态变化的场景（如移动光源、室外时变光照），该方法无法处理。这是一个明确的适用边界。

3. **计算开销**：光照模型预训练需36小时，自适应需4分钟（NVIDIA DGX），对于实时应用场景需要进一步优化。

4. **单身份验证**：目前仅在单个受试者的DAM模型上进行训练和评估，未验证多身份泛化能力。光照模型是否可以在不同人物间共享或迁移，仍是开放问题。

**后续启发与知识库价值：**

本文为知识库提供了以下可延续的研究方向：

- **光照模型的通用化**：能否训练一个跨身份共享的光照模型，减少或消除对个人化光场采集的依赖？这需要探索光照与面部几何/纹理的解耦程度。

- **在线光照自适应**：当前的自适应是离线的（4分钟处理K个关键帧），能否实现无需离线阶段的在线光照适应方法，以应对光照动态变化的视频？

- **物理先验与数据驱动的结合**：本文展示了物理光场数据作为预训练先验的有效性，这一思路可以推广到其他需要物理合理性的视觉任务（如材质估计、重光照）。

- **光照模型的结构化改进**：增益/偏置图虽然表达能力强，但参数量大。能否设计更结构化的光照表示（如结合物理光照模型与学习残差），在保持表达能力的同时提高效率？

总之，本文在知识库中的定位是“高保真面部追踪中光照鲁棒性”问题的基准解决方案，其核心贡献——基于物理光场预训练的深度光照自适应——为后续研究提供了明确的技术路线和改进方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Authentic_Volumetric_Avatars_From_a_Phone_Scan.pdf]]
---
title: Pupil-aware Holography
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Pupil_aware_Holography.pdf
project_link: null
code_link: null
aliases:
- PAH
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 空间光调制器（SLM）上的相位图是可控因果变量。通过在优化过程中引入可微的瞳孔采样前向模型，并对多样的瞳孔状态进行随机采样，可以联合优化图像质量和视场能量分布，从而使重建质量对瞳孔状态鲁棒。
primary_logic: 通过内容驱动的瞳孔感知相位优化，可以在视场中心获得类似均匀目标相位的高能量、无散斑重建，同时在视场边缘获得类似随机相位的均匀能量分布，从而在不同瞳孔采样情况下均保持可辨识的图像，无需眼动追踪。
claims:
- 瞳孔感知全息显著消除严重伪影，显著优于现有方法。
- 在瞳孔移动到非瞳孔感知全息图像完全消失的偏心位置时，瞳孔感知全息仍能保持图像质量。
- 瞳孔感知全息可扩展到未来大 étendue 显示器（模拟验证）。
- 模拟与硬件原型显示 上 不同瞳孔状态下的视觉图像质量（定性） = 在 eyebox 偏心位置仍保持可识别图像，无明显散斑或裁切
---

# Pupil-aware Holography

> [!tip] 核心洞察
> 通过内容驱动的瞳孔感知相位优化，可以在视场中心获得类似均匀目标相位的高能量、无散斑重建，同时在视场边缘获得类似随机相位的均匀能量分布，从而在不同瞳孔采样情况下均保持可辨识的图像，无需眼动追踪。

| 字段 | 内容 |
|------|------|
| 中文题名 | 瞳孔感知全息显示 |
| 英文题名 | Pupil-aware Holography |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2203.14939) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Pupil-aware Holography (瞳孔感知全息相位恢复) |
| Dataset | 大 étendue 显示器模拟（16×, 64×）, 3D 多平面显示实验 |

> [!tip] 效果简介
> - 模拟与硬件原型显示 上，不同瞳孔状态下的视觉图像质量（定性） 在 eyebox 偏心位置仍保持可识别图像，无明显散斑或裁切 vs 非瞳孔感知方法在偏心位置图像完全丢失 (显著提升)。
> - 大 étendue 显示器模拟（16×, 64×） 上，视觉重建质量 高保真重建，方法可扩展 vs 未明确给出对比 (有效扩展)。
> - 3D 多平面显示实验 上，聚焦切换时近/远物体清晰度 仅改变相机对焦即可区分远近物体，瞳孔感知优化可行 vs 无对比 (首次扩展到 3D)。

## 概要

近眼全息显示器面临一个根本性挑战：人眼瞳孔仅能对空间光调制器（SLM）发出的波前进行部分采样，且瞳孔大小、位置和方向动态变化，导致现有全息方法在 eyebox 边缘出现图像完全丢失、严重散斑或裁切等灾难性伪影。本文提出**瞳孔感知全息（Pupil-aware Holography）**，首次将瞳孔采样行为显式纳入全息图优化框架。核心思路是：构建可微的瞳孔采样前向传播模型，在迭代优化中随机采样多样瞳孔状态，联合优化完整波前与瞳孔采样下的重建损失，从而在 eyebox 全域同时实现高保真图像质量和均匀能量分布。该方法无需眼动追踪，不依赖新硬件。在原型系统上的实验表明，瞳孔感知全息在整个 eyebox 范围内保持可辨识的高质量重建，即使在非瞳孔感知方法图像完全消失的偏心位置仍能维持图像；同时，方法可扩展至大 étendue 显示器（模拟验证）和 3D 多平面全息显示。

## 核心方法与创新机理

### 问题瓶颈：瞳孔部分采样导致的图像崩溃

全息近眼显示器面临一个独特而根本的问题：人眼瞳孔仅能对空间光调制器（SLM）发出的波前进行**部分采样**，且瞳孔的大小、位置和方向在观察过程中动态变化。现有全息相位恢复方法假设整个波前被完整采集，因此当瞳孔偏离中心或缩小时，重建图像会出现三类灾难性退化：

1. **散斑噪声**：远场配置下，小瞳孔截断了 SLM 波前的空间频率分量，导致严重的散斑伪影（Figure 3, Figure 8 第二行）。
2. **图像裁切**：近场配置下，瞳孔的有限孔径直接裁切目标图像区域，造成部分图像丢失（Figure 8 第三行）。
3. **亮度消失**：传统方法将光能集中在瞳孔平面极小区域（Maxwellian 型显示），一旦瞳孔偏离该区域，图像完全消失（Figure 4）。

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2203_14939/figures/003_Figure_3.jpg]]
*Figure 3: (a) Compound DSLR lenses with large aperture ?? are capable of capturing the entire light bundle with diameter ?? emitted from a holographic display, as opposed to a human eye. (c) This results in high-fidelity holographic reconstructions on the imaging sensor. However, human eyes have limited- and variable-size pupils that only partially sample the incoming wavefront to the eyes. (b) & (d) As a result of the partial wavefront sampling due to an unknown pupil state, the projected image quality degrades, as a conventional computer-generated holography assumes that all of the wavefront is properly captured. Note that the low-contrast region of the cat’s reflection on the floor is close to bei...*

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2203_14939/figures/004_Figure_4.jpg]]
*Figure 4: Conventional holographic displays [Kim et al. 2022; Maimone et al. 2017] focus the SLM modulated light down to a point on the pupil plane, resulting in a very tiny eyebox (middle). This approach severely restricts the “valid” region where the eyes can see the holographic image, thereby resulting in no viewable imagery outside of the small eyebox region (top and bottom) that is mandated by the limited étendue of today’s holographic systems*

这一问题的本质在于：**étendue 有限的 SLM 无法同时满足大视场（eyebox）与高图像质量**，而瞳孔采样的不确定性使这一矛盾在近眼显示中尤为突出。

### 核心洞察：内容驱动的瞳孔感知相位优化

本文的核心创新在于识别并操控了一个关键的因果变量——**目标图像平面的物体相位（object phase）**。传统非瞳孔感知方法对该相位的处理存在两种极端：

- **随机目标相位**：在 eyebox 内产生均匀的能量分布，但重建图像被极端散斑噪声破坏（Figure 9 第一行）。
- **均匀零相位**：能量集中在 eyebox 中心，中心区域无噪声重建，但瞳孔一旦偏离中心即丢失图像，有效 eyebox 极小（Figure 9 第二行）。

瞳孔感知优化的核心洞察是：**通过可微的瞳孔采样前向模型，在优化过程中对多样化的瞳孔状态进行随机采样，联合优化图像质量和 eyebox 能量分布，从而在中心获得类均匀相位的高质量重建，在边缘获得类随机相位的均匀能量分布，实现不同瞳孔状态下的鲁棒重建**（Figure 9 第三行）。频谱分析（Figure 10）证实，优化得到的物体相位同时包含低频成分（类似均匀相位）和高频成分（类似随机相位），其空间结构叠加了目标图像的轮廓信息。

### 方法框架与模块链

瞳孔感知全息相位恢复包含六个核心模块，形成端到端的可微优化管线（Figure 6）：

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2203_14939/figures/006_Figure_6.jpg]]
*Figure 6: Pupil-aware Holography. We optimize for phase-only holograms to produce high-fidelity reconstructions and energy distribution across the eyebox. To this end, we rely on a differentiable image formation model that explicitly considers the eye pupil sampling of the eyebox, allowing us to backpropagate an intensity reconstruction loss to the SLM phase pattern for each step of our iterative optimization. By a stochastically sampled pupil-aware optimization, the proposed method is able to achieve both image quality and energy distribution over the entire eyebox*

#### 模块一：目标图像到物体相位的初始化

目标图像被赋予振幅 $A_{\text{ref}}$，物体相位 $\phi_0$ 作为可优化变量。初始相位可随机初始化或设为零，优化过程中通过梯度下降迭代更新。这一变量是连接图像内容与 eyebox 能量分布的关键因果节点。

#### 模块二：复全息场形成（卷积模型）

系统采用与 SLM 共面的凸透镜，通过算法引入共轭凹透镜相位函数，在 SLM 平面生成虚拟图像（Figure 5）。SLM 上的复全息场 $U_{\text{SLM}}$ 由目标图像场 $U_{\text{target}}$ 与传播核 $G$ 的卷积得到：

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2203_14939/figures/005_Figure_5.jpg]]
*Figure 5: To evaluate the proposed pupil-aware holographic phase retrieval, we use a ray-biasing convex lens coplanar with the SLM, achieving a large eyebox. A conjugate lens phase function is applied on the SLM (top) which results in plane waves leaving the SLM-lens system (bottom), thereby creating a virtual image at optical infinity*

$$U_{\text{SLM}} = U_{\text{target}} * G$$

其中传播核定义为：

$$G = e^{-j \frac{k}{2f} (x^2 + y^2)}$$

$f$ 为透镜焦距，$k$ 为波数。该卷积模型等价于目标像素加权的凹透镜相位函数的连续叠加：

$$H(\bar{x}) = \int_{\bar{t} \in L} A(\bar{x}) e^{j \phi_0(\bar{x})} e^{-\frac{jk}{2f}(\bar{x} - \bar{t})} d\bar{t}$$

这一设计使 SLM 出射光形成平面波，虚拟图像位于光学无穷远，从而实现大 eyebox。

#### 模块三：双相位振幅编码

复全息场 $A e^{j\phi}$ 需编码为纯相位全息图以适配 SLM。采用双相位振幅编码方法，将复振幅分解为两个纯相位项：

$$A e^{j\phi} = 0.5 e^{j(\phi - \cos^{-1}A)} + 0.5 e^{j(\phi + \cos^{-1}A)}$$

两项通过棋盘格交错排列在 SLM 像素上，利用 SLM 的低通滤波特性滤除高频噪声，实现高保真的复振幅调制。

#### 模块四：瞳孔感知可微前向传播（核心创新模块）

这是方法的核心 changed slot。传统前向模型仅计算完整波前采样下的目标面重建，而本文推导了**可微的瞳孔采样变体**：

- **完整采样传播**（所有 SLM 像素可见）：

$$U_{\text{target;full}} = \mathcal{F}^{-1}\left(\mathcal{F}(U_{\text{SLM}}) \odot M_{\text{iris}}\right) * G^{\dagger}$$

- **瞳孔采样传播**（随机瞳孔掩码 $M$ 作用于傅里叶面）：

$$U_{\text{target;pupil}} = \mathcal{F}^{-1}\left(M \odot \mathcal{F}(U_{\text{SLM}}) \odot M_{\text{iris}}\right) * G^{\dagger}$$

瞳孔掩码 $M$ 在每次迭代中随机采样不同的位置、大小和方向，模拟人眼瞳孔在 eyebox 内的多样化状态。$M_{\text{iris}}$ 为固定光阑掩码，$G^{\dagger}$ 为逆传播核。这一双路径前向模型使梯度能够同时反向传播到完整采样和瞳孔采样的重建损失，驱动 SLM 相位向瞳孔鲁棒的方向优化。

#### 模块五：多损失联合计算

优化目标同时最小化完整采样和瞳孔采样下的重建损失：

$$A_{\text{SLM}}, \Phi_{\text{SLM}} = \underset{\{A_{\text{SLM}}', \Phi_{\text{SLM}}'\}}{\arg\min} \mathcal{L}(|U_{\text{target;full}}|, A_{\text{ref}}) + \mathcal{L}(|U_{\text{target;pupil}}|, A_{\text{ref}})$$

损失函数 $\mathcal{L}$ 由四项加权组合构成：

$$\mathcal{L} = \lambda_{\ell_2} \mathcal{L}_{\ell_2} + \lambda_{\text{SSIM}} \mathcal{L}_{\text{SSIM}} + \lambda_{\text{pERC}} \mathcal{L}_{\text{pERC}} + \lambda_{\text{wFFT}} \mathcal{L}_{\text{wFFT}}$$

其中感知损失 $\mathcal{L}_{\text{PERC}}$ 基于 VGG-19 各层特征图的 L1 距离：

$$\mathcal{L}_{\text{PERC}} = \sum_{l} v_{l} ||\phi_{l}(x) - \phi_{l}(y)||_{1}$$

L2 损失保证像素级保真度，SSIM 损失保持结构相似性，VGG-19 感知损失提升视觉质量，Watson FFT 损失在频域约束重建精度。瞳孔采样和完整采样的损失通过加权求和联合优化，实现图像质量与 eyebox 鲁棒性的平衡。

#### 模块六：随机梯度下降优化（Wirtinger 梯度）

整个管线完全可微，通过 Wirtinger 梯度进行复数域的随机梯度下降，迭代更新 SLM 的振幅 $A_{\text{SLM}}$ 和相位 $\Phi_{\text{SLM}}$。每次迭代随机采样一个新的瞳孔状态，使优化过程遍历 eyebox 内的多样化采样条件。

### 训练与推理路径

**训练（优化）阶段**：对每帧目标图像，执行约 500–1000 次迭代的随机梯度下降。每次迭代中，随机采样瞳孔掩码 $M$ 的位置、大小和方向，计算完整采样和瞳孔采样的联合损失，反向传播梯度更新 SLM 相位。优化完成后输出纯相位全息图。当前 GPU 实现每帧约需 2 秒，尚不能实时运行。

**推理（显示）阶段**：将优化得到的相位全息图加载到 SLM，通过硬件光路投影。由于全息图已内化了对多种瞳孔状态的鲁棒性，显示时无需眼动追踪，瞳孔在 eyebox 内任意移动均可保持可辨识的重建图像。

### 关键因果链路总结

1. **物体相位 $\phi_0$** → 控制目标面的能量分布和图像结构 → 通过卷积模型影响 SLM 复全息场 $U_{\text{SLM}}$。
2. **瞳孔掩码 $M$** → 随机截断 SLM 波前的空间频率分量 → 在瞳孔采样传播路径中产生部分采样效应。
3. **双路径损失联合优化** → 完整采样路径保证图像保真度，瞳孔采样路径强制能量在 eyebox 内均匀分布 → 梯度反向传播驱动 $\phi_0$ 收敛到兼具低频和高频成分的瞳孔感知最优解。
4. **双相位编码** → 将复振幅转换为纯相位全息图 → 通过 SLM 的物理低通滤波抑制编码噪声。

这一方法链的核心 changed slot 在于：**将传统的不考虑瞳孔采样的前向模型替换为可微的瞳孔采样双路径模型，并在损失函数中引入瞳孔采样重建项**。这使得优化过程能够主动感知瞳孔状态的变化，在图像质量和 eyebox 鲁棒性之间找到内容自适应的最优折中，而无需依赖眼动追踪硬件。

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2203_14939/figures/007_Figure_7.jpg]]
*Figure 7: Prototype Holographic Display. We built an experimental display to validate pupil-aware holographic phase retrieval. To mimic the pupil sampling of a human eye, we use an aperture on the eyebox plane, as can be seen in front of the camera, as a virtual pupil. The proposed pupil-aware holography method enables accurate holographic image reconstructions across the eyebox for diverse pupil states*

## 实验与关键发现

### 核心实验框架

本研究在自建硬件原型上验证瞳孔感知全息方法，原型在空间光调制器（SLM）前共面放置凸透镜以扩展 eyebox，并在 eyebox 平面放置可调光圈模拟人眼瞳孔采样（Fig. 7）。优化在 GPU 上执行，每帧约需 2 秒。实验以非瞳孔感知的随机梯度下降优化（分别采用随机目标相位和均匀零相位）作为主要对比基线，同时纳入 **CITL 全息相位恢复**（Peng et al., 2020）作为非瞳孔感知的附加参照。

### 主实验结果

**1. 瞳孔状态鲁棒性（硬件原型）**

实验在宽 eyebox 显示配置下，以不同位置和尺寸的瞳孔光圈采样重建图像。非瞳孔感知方法在瞳孔偏离 eyebox 中心时出现灾难性退化：采用均匀目标相位的方法在偏心位置图像完全丢失（Fig. 13 中行，Fig. 14 中行）；采用随机目标相位的方法虽能维持能量分布，但图像被严重散斑噪声破坏。瞳孔感知全息在整个 eyebox 范围内保持可识别的高保真重建，即使在密集采样偏心位置（Fig. 14 底行）仍能维持图像质量，而非瞳孔感知方法在中等偏心处即完全丢图。这一结果直接支撑了核心主张：**瞳孔感知优化可在无需眼动追踪的条件下，使重建质量对瞳孔状态鲁棒**。

**2. 大 étendue 显示器可扩展性（模拟）**

在模拟环境中将显示 étendue 放大 16× 和 64× 进行测试，瞳孔感知方法仍能产生高保真重建（Fig. 11），表明该方法可扩展到未来大 étendue 显示器。需注意，该结论完全基于模拟，实际大 étendue 硬件的物理验证尚未进行。

**3. 3D 多平面显示扩展（硬件原型）**

将瞳孔感知优化扩展到 3D 全息，在单一 SLM 图案上同时编码近距和远距图像。仅通过改变相机对焦即可区分近远物体，对应焦平面清晰、离焦平面模糊（Fig. 15），验证了瞳孔感知优化在多平面投影中的可行性。该实验为定性展示，未与 3D 全息基线进行定量比较。

### 关键消融与分析

**1. 目标相位选择对 eyebox 能量分布的决定性作用（Fig. 9）**

这是全文最关键的消融实验，揭示了瞳孔感知优化的内在机理：
- **随机目标相位**：在 eyebox 内产生均匀能量分布，但重建图像被极端散斑噪声破坏，无法辨识内容。
- **均匀零相位**：能量高度集中在 eyebox 中心，中心区域重建无噪声，但瞳孔一旦偏离中心即完全丢失图像，有效 eyebox 极小。
- **瞳孔感知优化**：在 eyebox 中心获得类似均匀相位的低噪声重建，在边缘获得类似随机相位的均匀能量分布，实现中心高保真与边缘可辨识的折中。

**2. 优化所得物体相位的频谱特性（Fig. 10）**

瞳孔感知优化得到的物体相位包含目标图像结构叠加高频分量。对数频谱显示其同时具备低频成分（类似均匀相位）和高频成分（类似随机相位），频谱的圆形截断来源于 4F 系统的傅里叶滤波，其尺寸与 eyebox 一致。该频谱特性直接解释了为何瞳孔感知方法能在中心和边缘分别呈现类均匀和类随机相位的行为。

**3. 显示配置对瞳孔采样伪影类型的影响（Fig. 8, Fig. 12）**

通过模拟和硬件实验对比三种显示配置在不同瞳孔状态下的重建：
- **远场中继配置**：小瞳孔导致空间频率截断，产生严重散斑噪声；瞳孔直径是影响散斑程度的主要因素，位置影响相对较小。
- **近场中继配置**：瞳孔采样导致图像裁切和衍射伪影，瞳孔位置变化直接改变可见图像区域。
- **宽 eyebox 配置（本文采用）**：结合瞳孔感知优化后，可在多样瞳孔状态下保持重建质量。

该消融明确了不同显示架构下瞳孔采样问题的表现差异，并验证了宽 eyebox 配置作为方法验证平台的合理性。

### 失败模式与适用边界

**1. 极端偏心处的质量退化**

尽管瞳孔感知优化在整个 eyebox 内维持可辨识图像，但在极端偏心位置，重建质量仍下降至接近随机目标相位的水平。这是因为边缘瞳孔采样到的 SLM 像素数急剧减少，物理上限制了可恢复的信息量。该方法不保证 eyebox 内均匀的高保真重建，而是保证不出现完全丢图或不可辨识的灾难性退化。

**2. 低对比度区域的脆弱性**

如 Fig. 3(d) 所示，在较小瞳孔直径下，图像中低对比度区域（如猫在地板上的倒影）接近不可见。瞳孔感知优化虽能改善整体能量分布，但无法完全补偿由瞳孔缩小导致的光通量减少对低对比度细节的影响。

**3. 优化速度限制**

每帧优化约需 2 秒（GPU），远未达到实时应用需求。该限制源于随机梯度下降的迭代性质和每步需计算多个瞳孔采样的前向传播。

**4. 未考虑人眼视觉特性**

当前损失函数（L2、SSIM、VGG-19 感知损失、Watson FFT）仅关注显示端图像保真度，未融入人眼透镜像差、瞳孔形状畸变、视觉掩蔽效应等实际感知因素。在实际人眼观察中，主观体验可能与相机捕获结果存在差异。

**5. 缺乏定量指标**

所有实验结果均以定性视觉比较呈现，未报告 PSNR、SSIM 等客观数值指标，无法进行严格的统计显著性判断。与基线的比较主要针对自身方法的非瞳孔感知版本，未与其他主流全息方法进行系统的定量对比。

### 证据强度总结

| 主张 | 证据类型 | 强度 |
|------|---------|------|
| 瞳孔感知优化消除严重瞳孔依赖伪影 | 硬件原型定性对比（Fig. 13, 14） | 高（置信度 0.95） |
| 偏心位置仍保持图像质量 | 密集瞳孔采样硬件实验（Fig. 14） | 高（置信度 0.95） |
| 方法可扩展到大 étendue 显示器 | 仅模拟验证（Fig. 11） | 中（置信度 0.9，需硬件验证） |
| 3D 多平面扩展可行 | 硬件原型定性展示（Fig. 15） | 中（置信度 0.9，缺乏定量对比） |
| 瞳孔感知优化的频谱机理 | 频谱分析（Fig. 10） | 高（置信度 0.9） |

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2203_14939/figures/008_Figure_8.jpg]]
*Figure 8: Evaluating Display Configurations (Simulation). We study commonly used near- and far-field display configurations and the proposed wide eyebox variant for evaluating our pupil-aware holography method. See Fig. 2 for SLM relayed and non-relayed setup schematics, and Fig. 4 for a small pupil forming Maxwellian-style display. We test the configurations for five pupil masks with different sizes and locations shown on top, where the white mask represent the eye pupil. All existing methods, with varying pupil states, produce either speckle while truncating the spatial frequencies that are admitted into the pupil in the far-field configuration (second row), or truncate the image itself as shown in...*

## 定位与知识库关联

### 问题定位：瞳孔采样——被忽视的因果瓶颈

现有全息近眼显示方法的核心假设是“人眼瞳孔完整采样 SLM 出射的整个波前”。这一假设在相机全孔径接收下成立，但在真实人眼观看时完全失效：瞳孔仅能部分采样波前，且其位置、大小和方向动态变化。由此产生的因果链是：**瞳孔状态变化 → 波前部分采样 → 空间频率截断/图像裁切 → 严重散斑或图像完全丢失**。

传统全息相位恢复方法（如 **CITL holographic phase retrieval**, Peng et al., 2020）聚焦于通过相机反馈迭代优化 SLM 相位以提升完整波前下的重建质量，但从未将瞳孔采样作为优化变量。这导致它们在实际人眼观看时表现剧烈退化：当瞳孔偏离 eyebox 中心时，图像可能完全消失（Fig. 13, Fig. 14 中间行）。该问题的根源在于 **étendue 受限**——现有 SLM 的 étendue 远不足以支撑大 eyebox，而 étendue 扩展硬件（如衍射掩模，Buckley et al. 2006; Kuo et al. 2020; Park and Askari 2019）虽能增大 eyebox，却未解决瞳孔部分采样导致的图像退化。

### 改变的 Slot：从“忽略瞳孔”到“瞳孔感知优化”

本文在以下关键 slot 上做出了改变，从而将瞳孔采样从“不可控的退化因素”转化为“可优化的约束条件”：

**Slot 1：前向模型中的瞳孔采样（从隐式假设到显式可微建模）**
- **Baseline 值**：前向传播模型假设全部波前被完整采样（$I = |\mathcal{P}(H)|^2$），瞳孔掩码不存在。
- **本文值**：在前向模型中显式引入可微的瞳孔掩码 $M$，使得重建图像为 $I = |\mathcal{P}(H \odot M)|^2$ 或 $U_{\mathrm{target;pupil}} = \mathcal{F}^{-1}(M \odot \mathcal{F}(U_{\mathrm{SLM}}) \odot M_{\mathrm{iris}}) * G^{\dagger}$。优化过程中随机采样不同的瞳孔状态（位置、大小、方向），使梯度反向传播时同时考虑完整采样和部分采样两种情形。

**Slot 2：优化目标（从单一完整波前损失到联合瞳孔感知损失）**
- **Baseline 值**：仅最小化完整波前重建与参考图像之间的损失 $\mathcal{L}(|U_{\mathrm{target;full}}|, A_{\mathrm{ref}})$。
- **本文值**：联合优化完整采样和瞳孔采样重建的加权组合损失：
  $$A_{\mathrm{SLM}}, \Phi_{\mathrm{SLM}} = \arg\min \mathcal{L}(|U_{\mathrm{target;full}}|, A_{\mathrm{ref}}) + \mathcal{L}(|U_{\mathrm{target;pupil}}|, A_{\mathrm{ref}})$$
  损失函数由 L2、SSIM、VGG-19 感知损失和 Watson FFT 损失加权组成。

这两个 slot 的协同改变产生了一个关键的因果机制：优化过程被迫在“中心高质量重建”（类均匀目标相位）和“边缘均匀能量分布”（类随机目标相位）之间找到内容驱动的折中。具体而言，优化得到的物体相位在频谱上呈现出中心低频率（类似均匀相位，保证中心无散斑重建）、边缘高频率（类似随机相位，保证边缘能量均匀）的混合结构（Fig. 10）。

### 知识库挂载点

本文可挂载到以下知识节点：

1. **计算全息相位恢复（Computer-generated Holography, CGH）**：本文继承并扩展了基于随机梯度下降（SGD）的迭代相位优化框架（Wirtinger 梯度），但首次将瞳孔采样作为可微前向模型的一部分。与 **CITL**（Peng et al., 2020）相比，本文不需要相机反馈闭环，而是通过随机采样模拟瞳孔状态变化。

2. **Étendue 扩展与 eyebox 设计**：本文与 étendue 扩展硬件方法（衍射掩模，Buckley et al. 2006; Kuo et al. 2020; Park and Askari 2019）正交。后者通过硬件增加 étendue，本文通过算法使有限 étendue 下的重建对瞳孔采样鲁棒。两者可互补：在更大 étendue 硬件上部署瞳孔感知优化可能实现完全的瞳孔不变性（Fig. 11 模拟验证了可扩展性，但实际大 étendue 硬件验证待完成）。

3. **近眼显示中的视觉感知**：本文未融入人类视觉系统模型（如掩蔽效应、视觉敏感度分布），仅关注显示端图像保真度。这为后续工作留下了明确的改进空间：将瞳孔感知优化与注视点渲染、眼动追踪或视觉感知模型结合。

### 适用边界与局限

1. **硬件依赖**：本文未提出新硬件，仅在有限 étendue 原型上通过凸透镜扩展 eyebox 以模拟大 eyebox 场景。实际大 étendue 显示器（如小像素间距 SLM）上的完全验证尚待完成。
2. **人眼模型简化**：未考虑人眼透镜像差、瞳孔形状畸变等个体差异，实际感知质量可能受这些因素影响。
3. **实时性缺失**：每帧优化耗时约 2 秒（GPU），无法满足实时应用需求。
4. **定量评估不足**：仅通过定性视觉比较验证，缺乏 PSNR/SSIM 等客观数值指标的定量报告。
5. **极端场景退化**：对于极暗或低对比度图像区域，瞳孔感知优化仍可能受限于光能分布，极端偏心处重建质量可能下降至随机相位水平。

### 后续启发

本文开辟了“瞳孔感知计算全息”这一新方向，后续工作可从以下路径展开：
- **硬件-算法联合设计**：将瞳孔感知优化与定制 étendue 扩展元件联合设计，实现完全的瞳孔不变性。
- **实时化**：探索轻量化优化策略或神经网络推理，在保持瞳孔感知特性的前提下实现实时相位生成。
- **视觉感知集成**：引入人眼视觉模型（深度感知、颜色感知、视觉敏感度），进一步提升主观体验。
- **动态场景扩展**：将方法扩展到视频全息和动态场景，与注视点渲染结合，优化计算资源分配。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Pupil_aware_Holography.pdf]]
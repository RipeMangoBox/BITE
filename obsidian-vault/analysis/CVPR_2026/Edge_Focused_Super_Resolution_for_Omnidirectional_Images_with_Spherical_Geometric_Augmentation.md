---
title: Edge-Focused Super-Resolution for Omnidirectional Images with Spherical Geometric Augmentation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Edge_Focused_Super_Resolution_for_Omnidirectional_Images_with_Spherical_Geometric_Augmentation.pdf
project_link: null
code_link: null
aliases:
- EAMSENSGA
- EFSROISGA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于球面坐标变换的数据增强（保持场景连续性）和边缘聚焦的多尺度注意力网络（EFB中的EEB/ERB与GIB），使得网络能够更准确地恢复边缘和全局结构。
primary_logic: 通过球面几何一致的数据增强模拟视角变化并维持全景图的环形拓扑，同时显式建模多尺度边缘注意力和全局特征集成，可显著提升高倍率全向图像超分辨率的重建质量与边缘连续性。
claims:
- 在ODI-SR数据集上，EAM在×8和×16任务中分别取得25.69 dB和23.86 dB的WS-PSNR，相比当时最优方法FATO提升1.15 dB和1.13 dB。
- 球面坐标变换数据增强将×8任务的WS-PSNR从约24.95 dB提升至25.69 dB，WS-SSIM从0.6529提升至0.6839，证实其在保持场景连续性和改善边缘恢复方面的有效性。
- 消融研究显示，去除EEB、ERB或GIB任一模块均导致WS-PSNR和WS-SSIM下降，验证了边缘聚焦设计和全局集成模块的必要性。
- ODI-SR 上 WS-PSNR (×8) = 25.69
---

# Edge-Focused Super-Resolution for Omnidirectional Images with Spherical Geometric Augmentation

> [!tip] 核心洞察
> 通过球面几何一致的数据增强模拟视角变化并维持全景图的环形拓扑，同时显式建模多尺度边缘注意力和全局特征集成，可显著提升高倍率全向图像超分辨率的重建质量与边缘连续性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于球形几何增强的边缘聚焦全向图像超分辨率 |
| 英文题名 | Edge-Focused Super-Resolution for Omnidirectional Images with Spherical Geometric Augmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Edge-Focused_Super-Resolution_for_Omnidirectional_Images_with_Spherical_Geometric_Augmentation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Edge-Aware Multi-Scale (EAM) network with Spherical Geometric Augmentation |
| Dataset | ODI-SR |

> [!tip] 效果简介
> - ODI-SR 上，WS-PSNR (×8) 25.69 vs 24.54 (FATO) (+1.15 dB)；WS-PSNR (×16) 23.86 vs 22.73 (FATO) (+1.13 dB)。

## 概要

全向图像（Omnidirectional Images, ODIs）以等距柱状投影（Equirectangular Projection, ERP）记录360°全景场景，广泛应用于虚拟现实、自动驾驶等领域。然而，在极大放大倍数（×8、×16）的超分辨率任务中，现有方法面临两个核心瓶颈：其一，公开数据集样本极为稀缺（仅约1200张），传统二维平移/旋转增强会破坏球面投影的环形拓扑连续性；其二，通用超分辨率网络缺乏显式的边缘建模机制，导致重建图像边缘模糊、细节丢失。

针对上述问题，本文提出**基于球形几何增强的边缘感知多尺度超分辨率网络（Edge-Aware Multi-Scale, EAM）**。该方法的核心思路是：在数据层面，通过球面坐标变换实现三维旋转与平移增强，保持场景的几何连续性与环形结构完整性；在网络层面，设计**边缘聚焦模块（Edge Focused Block, EFB）**——由边缘增强模块（EEB）与边缘细化模块（ERB）级联构成，结合多尺度扩张卷积与空间/通道注意力机制，显式捕获并优化边缘特征；同时引入**全局整合模块（Global Integration Block, GIB）**，利用大核深度可分离卷积扩展感受野，融合多尺度全局上下文信息。

实验表明，在ODI-SR数据集上，EAM在×8和×16任务中分别取得**25.69 dB**和**23.86 dB**的WS-PSNR，相较此前最优方法FATO（An et al., MM Asia 2024）分别提升**1.15 dB**和**1.13 dB**。消融研究证实，球面坐标增强、EFB各子模块及多目标联合损失（L1 + 感知损失 + SSIM损失）均对性能有显著贡献。

全向图像（Omnidirectional Image, ODI）因其360°沉浸式视觉体验，在虚拟现实、自动驾驶和机器人导航等领域应用日益广泛。然而，受限于采集设备分辨率和传输带宽，全向图像常需进行高倍率超分辨率重建。现有方法在该任务上面临两大核心瓶颈：**数据稀缺**与**边缘退化**。

在数据层面，主流的ODI-SR数据集仅包含约1200张训练图像，远少于普通图像超分辨率任务的数据规模。更关键的是，传统二维数据增强（如平移、旋转）直接作用于等距柱状投影（Equirectangular Projection, ERP）图像，会破坏球面场景的环形拓扑连续性，导致投影失真加剧，反而损害重建质量。

在方法层面，现有全向图像超分辨率方法——包括基于纬度自适应的**LAU-Net**（Deng et al., CVPR 2021）、基于连续球面表示的**SphereSR**（Yoon et al., CVPR 2022）、失真感知Transformer **OSRT**（Yu et al., CVPR 2023）以及频率注意力Transformer **FATO**（An et al., MM Asia 2024）——普遍缺乏显式的边缘建模机制。在8×和16×等极大放大倍数下，边缘细节的恢复尤为困难，重建图像常出现模糊和伪影。

针对上述缺口，本文的动机在于：**通过球面几何一致的数据增强模拟真实视角变化，同时构建边缘感知的多尺度注意力网络，从根本上提升高倍率全向图像超分辨率的边缘恢复质量和结构保真度。** 具体而言，本文提出基于球面坐标变换的数据增强策略，将二维旋转/平移转化为三维球面旋转，从而保持场景的几何完整性；同时设计边缘聚焦模块（EFB）和全局整合模块（GIB），分别负责多尺度边缘特征的增强与细化，以及长程上下文依赖的捕获。这一“数据-模型”协同设计的思路，构成了本文方法的核心出发点。

## 核心方法与创新机理

本文的核心创新围绕全向图像（ODI）超分辨率的两大瓶颈展开：**高倍率下边缘保持能力差**与**传统数据增强破坏球面几何连续性**。对应地，方法在数据增强策略、边缘特征建模、多尺度特征整合和损失函数四个维度上提出了针对性改进。

### 数据增强策略：从平面变换到球面坐标变换

传统超分辨率方法采用二维图像的平移与旋转进行数据增强，但等距柱状投影（ERP）的全向图像并非欧氏平面——其左右边界在球面上是连续的，顶部与底部极点则存在严重畸变。直接应用二维仿射变换会导致**边缘截断、填充伪影和环形结构断裂**（见 Figure 3 对比），使网络学习到错误的几何先验。

本工作将数据增强提升到**球面坐标空间**。具体流程为：将 ERP 图像的像素坐标 $(u,v)$ 映射为球面方位角与极角：

$$\varphi_i = 2\pi \frac{u}{W}, \quad \theta_i = \pi \frac{v}{H}$$

进而转换为单位球上的三维笛卡尔坐标 $(x_p, y_p, z_p)$。在三维空间中对场景点施加绕 $X$、$Y$、$Z$ 轴的旋转（分别对应俯仰、翻滚、偏航），再反投影回 ERP 图像坐标。这一过程等价于**改变虚拟相机的观察视角**，而非对投影图像进行几何扭曲。其关键优势在于：平移操作（绕 $Z$ 轴旋转）天然保持 360° 环形拓扑的连续性，左右边界无缝衔接；旋转操作（绕 $X$ 或 $Y$ 轴）则模拟真实视角变化，不引入非物理的边缘填充。

消融实验（Table 3）证实，在 $\times8$ 任务上，球面坐标增强将 WS-PSNR 从无增强的约 24.95 dB 提升至 25.69 dB，WS-SSIM 从 0.6529 提升至 0.6839，增益显著。

### 边缘特征建模：Edge Focused Block (EFB)

现有全向图像超分辨率方法（如 LAU-Net、SphereSR、OSRT、FATO）缺乏显式的边缘注意力机制，在高倍率下难以保持细粒度边缘。本工作设计了**边缘聚焦模块（EFB）**，由边缘增强模块（EEB）和边缘细化模块（ERB）级联构成，形成“增强-细化”的两阶段边缘处理管线。

**EEB** 的核心是**多尺度扩张卷积与双路注意力融合**。输入特征 $X$ 经多个不同扩张率的 $3\times3$ 卷积提取多尺度上下文，随后并行计算：

- **边缘感知通道注意力** $A_c$：通过自适应最大池化与两个 $1\times1$ 卷积生成通道权重，强化对边缘敏感的通道响应；
- **边缘感知空间注意力** $A_s$：通过 $3\times3$ 卷积后接 $7\times7$ 大核卷积建模边缘的空间连续性，生成空间权重图。

多尺度特征与 $A_c$、$A_s$ 逐元素相乘后，经批归一化并通过残差连接与原始输入相加，得到增强特征 $X_1$。这一设计使网络能够**自适应地放大边缘区域的响应，同时抑制平坦区域的噪声**。

**ERB** 在此基础上进一步细化边缘质量。它通过可学习权重 $\alpha$ 动态平衡原始特征 $X_1$ 与由边缘可靠性图 $M_e$ 调制的细化特征：

$$X_2 = (1 - \alpha) \cdot X_1 + \alpha \cdot (X_r \otimes M_e)$$

其中 $M_e$ 由深度可分离卷积和 Sigmoid 生成，用于评估每个空间位置边缘恢复的置信度。$\alpha$ 作为可训练参数，使网络在训练过程中自动学习原始信息与细化信息的最佳混合比例。

消融实验（Table 4）表明，移除 EEB 或 ERB 均导致 WS-PSNR 和 WS-SSIM 下降，验证了“增强-细化”两级设计的必要性。

### 多尺度特征整合：Global Integration Block (GIB)

EFB 聚焦于局部边缘的增强与细化，但全向图像的重建还需要**全局上下文信息**来保持大尺度结构的连贯性。本工作引入**全局整合模块（GIB）**，弥补了多数全向图像超分辨率方法缺少长程依赖建模的不足。

GIB 的设计遵循“多尺度上下文提取 + 注意力融合”范式。输入特征分别经过两个分支：一支使用大核深度可分离卷积捕获全局感受野，另一支使用标准卷积保留局部细节。两支特征拼接后经 $1\times1$ 卷积和 Sigmoid 生成通道注意力权重 $A$，对融合特征进行加权。最终输出经 $1\times1$ 卷积压缩通道，得到全局整合后的特征表示。

Table 4 的消融结果显示，去除 GIB 后性能下降，证明全局上下文对高倍率全向图像超分辨率的贡献不可忽视。

### 损失函数：多目标联合优化

传统超分辨率方法通常采用单一的 $L_1$ 损失或感知损失。本工作将 $L_1$ 损失、感知损失和 SSIM 损失组合为多目标联合损失：

$$L_{\mathrm{Total}} = L_{\mathrm{L1}} + 0.01 \times L_{\mathrm{Perceptual}} + 0.1 \times (1 - L_{\mathrm{SSIM}})$$

其中 $L_1$ 保证像素级重建精度，感知损失（基于预训练 VGG 特征）提升纹理真实感，SSIM 损失约束结构相似性。Table 5 的消融实验显示，三者联合使用取得最高 WS-PSNR（25.69 dB），单独使用 $L_1$+感知损失或 $L_1$+SSIM 损失性能均次之，表明三者在优化目标上具有互补性——$L_1$ 提供逐像素保真度，SSIM 损失强化边缘结构一致性，感知损失改善视觉质量。

### 创新点总结

综上，本工作的核心创新可归纳为四个 **changed slots**：**(1)** 将数据增强从二维平面变换升级为球面坐标变换，保持场景几何连续性；**(2)** 设计 EFB（EEB+ERB）实现显式的多尺度边缘注意力建模；**(3)** 引入 GIB 捕获全局长程依赖；**(4)** 采用 $L_1$+感知+SSIM 的多目标联合损失。这些创新相互协同——球面增强提供几何一致的训练数据，EFB 强化局部边缘，GIB 补充全局上下文，联合损失从多个维度约束重建质量——共同驱动了在 $\times8$ 和 $\times16$ 任务上相比当时最优方法 FATO 分别提升 1.15 dB 和 1.13 dB WS-PSNR 的显著增益。

EAM（Edge-Aware Multi-Scale）超分辨率网络的设计核心围绕“边界保持与精细化”展开。整体流程为：低分辨率全向图像（$I_{\mathrm{LR}}$）首先经过MeanShift去除亮度偏差，再由一个$3\times3$卷积提取浅层特征 $F_{\mathrm{p}}$（Eq. 7）。这些特征随后进入级联的**边缘聚焦模块（EFB, Edge Focused Block）**，该模块由**边缘增强模块（EEB, Edge Enhanced Block）**和**边缘细化模块（ERB, Edge Refined Block）**组成，负责多尺度边缘特征的增强与优化，输出 $F_{r}$（Eq. 8）。之后，特征通过**全局整合模块（GIB, Global Integration Block）**，利用大核深度可分离卷积和注意力融合捕获长程依赖，扩展感受野。最终，网络采用渐进式上采样重建策略：将目标放大倍数分解为多个$2\times$步骤，每一步使用PixelShuffle提高分辨率并结合$3\times3$卷积恢复高频细节，生成高分辨率输出。

整个pipeline的因果逻辑是：**球面几何增强保证训练数据的场景连续性与环形拓扑一致性**（Section 3.1），为网络提供几何合理的监督信号；**EFB（EEB+ERB）显式建模多尺度边缘注意力**，通过通道注意力 $A_c$（Eq. 10）和空间注意力 $A_s$（Eq. 11）强化边缘相关特征，再经自适应加权融合（Eq. 13）细化边缘；**GIB整合全局上下文**，弥补局部模块感受野不足的问题。三者的协同使得EAM在高倍率（$\times8$、$\times16$）全向图像超分辨率任务中显著提升了边缘连续性和重建质量。

**证据强度**：消融实验（Tab. 4）表明，移除EEB、ERB或GIB任一模块均导致WS-PSNR和WS-SSIM下降，验证了各模块的必要性（置信度0.95）。完整EAM在ODI-SR数据集$\times8$任务上取得25.69 dB WS-PSNR，相比当时最优方法FATO提升1.15 dB（Tab. 1，置信度0.98）。

![[assets/figures/papers/paper_list_l2251_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Edge_Focused_Supe/figures/004_Figure_4.jpg]]
*Figure 4: (a) The network architecture of the proposed EAM; (b) Illustration of the proposed Edge Enhanced Block(EEB); (c) Illustration of the proposed Edge Refined Block(ERB); (d) Illustration of the proposed Global Integration Block(GIB)*

### 球面几何增强的数学基础

传统二维图像平移与旋转操作会破坏全向图像（ODI）的360°环形拓扑结构，导致边缘截断和填充伪影。本文提出基于球面坐标变换的数据增强，其核心是将等距柱状投影（ERP）的2D像素映射至单位球面，在三维空间执行旋转后重新投影回2D图像平面，从而保持场景的几何连续性与环形完整性（Fig. 3）。

![[assets/figures/papers/paper_list_l2251_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Edge_Focused_Supe/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of omnidirectional image translation and rotation operations*

**2D到球面坐标映射**：给定ERP图像尺寸 $W \times H$，像素坐标 $(u, v)$ 首先映射为方位角 $\varphi_i$ 与极角 $\theta_i$：

$$\varphi_i = 2\pi \frac{u}{W}, \quad \theta_i = \pi \frac{v}{H} \tag{Eq.1}$$

**球面到三维笛卡尔坐标**：将球面角转换为单位球上的3D坐标：

$$x_p = \cos \varphi_i \sin \theta_i, ~ y_p = \sin \varphi_i \sin \theta_i, ~ z_p = \cos \theta_i \tag{Eq.2}$$

**三维旋转操作**：绕X、Y、Z轴分别旋转 $\alpha, \beta, \gamma$ 角度，对应旋转矩阵 $R_x(\alpha), R_y(\beta), R_z(\gamma)$（Eq.3），合成旋转 $R$ 作用于3D坐标：

$$\begin{bmatrix} x_p' \\ y_p' \\ z_p' \end{bmatrix} = R \begin{bmatrix} x_p \\ y_p \\ z_p \end{bmatrix} \tag{Eq.4}$$

其中水平平移等效为绕Z轴旋转 $\gamma \in [0, 2\pi]$，垂直旋转通过绕X/Y轴旋转实现视角变化。

**球面角更新与重投影**：从旋转后的笛卡尔坐标反算球面角：

$$\varphi_i' = \arctan2(y_p', x_p'), \quad \theta_i' = \operatorname{arccos}(z_p') \tag{Eq.5}$$

最终映射回2D图像空间：

$$u_p' = \frac{W}{2\pi} \varphi_i', \quad v_p' = \frac{H}{\pi} \theta_i' \tag{Eq.6}$$

该变换链保证增强后的图像保持全向场景的连续性与合理性，为后续边缘聚焦网络提供几何一致的训练样本。

---

### 边缘聚焦模块（EFB）：EEB与ERB

EAM网络的核心设计围绕“边界保持与细化”展开，其边缘聚焦模块（Edge Focused Block, EFB）由边缘增强模块（Edge Enhanced Block, EEB）和边缘细化模块（Edge Refined Block, ERB）级联构成。

#### 边缘增强模块（EEB）

EEB旨在通过多尺度特征提取与边缘感知注意力机制实现定向边缘增强（Fig. 4(b)）。其关键计算流程如下：

**边缘感知通道注意力**：对输入特征 $X$ 先经 $3\times3$ 卷积，再通过自适应最大池化与两个 $1\times1$ 卷积生成通道注意力权重 $A_c$：

$$A_c = \sigma(\operatorname{Conv}_{1\times1}(\operatorname{Conv}_{1\times1}(\operatorname{Pool}(\operatorname{Conv}_{3\times3}(X))))) \tag{Eq.10}$$

其中 $\sigma$ 为Sigmoid激活，该分支强化对边缘判别具有高响应的特征通道。

**边缘感知空间注意力**：通过 $3\times3$ 卷积后接 $7\times7$ 大核卷积提取空间注意力权重 $A_s$，建模边缘的连续性与空间分布：

$$A_s = \sigma(\mathrm{Conv}_{7\times7}(\mathrm{Conv}_{3\times3}(X))) \tag{Eq.11}$$

**多尺度特征融合**：多尺度特征 $X_{\mathrm{multi}}$ 经 $3\times3$ 卷积后与通道注意力 $A_c$、空间注意力 $A_s$ 逐元素相乘，通过批归一化（BN）稳定训练，并以残差连接与原始输入 $X$ 融合：

$$X_1 = X + \mathrm{BN}(\mathrm{Conv}_{3\times3}(X_{\mathrm{multi}}) \otimes A_c \otimes A_s) \tag{Eq.12}$$

该门控残差设计使EEB能够选择性增强边缘区域特征，同时抑制非边缘噪声。

#### 边缘细化模块（ERB）

ERB在EEB输出的基础上进一步细化边缘质量（Fig. 4(c)）。其核心机制是学习一个边缘可靠性图 $M_e$，对细化特征 $X_r$ 进行调制，并通过可学习权重 $\alpha$ 自适应平衡原始特征与细化特征：

$$X_2 = (1 - \alpha) \cdot X_1 + \alpha \cdot (X_r \otimes M_e) \tag{Eq.13}$$

$\alpha$ 为可学习参数，使网络在训练过程中自动调节对边缘细化分支的依赖程度，避免过度锐化或边缘伪影。

---

### 全局整合模块（GIB）

为捕获全向图像的大范围空间依赖，GIB通过多尺度上下文提取与注意力融合扩展感受野（Fig. 4(d)）。两支并行的深度可分离卷积分支分别提取不同尺度的全局特征 $X_{\mathrm{scale1}}$ 与 $X_{\mathrm{scale2}}$，拼接后经 $1\times1$ 卷积与Sigmoid生成通道注意力权重 $A$：

$$A = \sigma(\mathrm{Conv}_{1\times1}(\mathrm{Concat}(X_{\mathrm{scale1}}, X_{\mathrm{scale2}}))) \tag{Eq.14}$$

最终将融合特征 $Y$ 用注意力 $A$ 加权后经 $1\times1$ 卷积输出：

$$X_{\mathrm{out}} = \operatorname{Conv}_{1\times1}\left( Y \otimes A \right) \tag{Eq.15}$$

GIB与EFB形成互补：EFB聚焦局部边缘细节，GIB提供全局结构约束，共同提升高倍率超分辨率下的重建质量。

---

### 多目标联合损失函数

为同时优化像素精度、结构相似性与感知质量，EAM采用三项损失的加权组合：

$$L_{\mathrm{Total}} = L_{\mathrm{L1}} + 0.01 \times L_{\mathrm{Perceptual}} + 0.1 \times (1 - L_{\mathrm{SSIM}}) \tag{Eq.16}$$

其中 $L_{\mathrm{L1}}$ 保证像素级重建精度，$L_{\mathrm{Perceptual}}$ 基于预训练VGG特征提升感知质量，$(1 - L_{\mathrm{SSIM}})$ 作为结构损失引导边缘与纹理的结构一致性。消融实验（Tab. 5）证实三者互补：单独使用 $L_1$+感知损失或 $L_1$+SSIM损失均无法达到三者联合的25.69 dB WS-PSNR最优性能。

## 实验与关键发现

### 主实验结果

EAM在ODI-SR数据集上进行了×8和×16超分辨率任务的定量评估，采用WS-PSNR和WS-SSIM作为球面感知评价指标。如**Table 1**所示，在×8任务中，EAM取得了**25.69 dB**的WS-PSNR，相比当时最优方法FATO（An et al., MM Asia 2024）的24.54 dB提升了**1.15 dB**；在×16任务中，EAM取得**23.86 dB**，较FATO的22.73 dB提升了**1.13 dB**。这一显著提升验证了边缘聚焦设计与球面几何增强在极大放大倍数下的有效性。

![[assets/figures/papers/paper_list_l2251_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Edge_Focused_Supe/figures/005_Table_1.jpg]]
*Table 1: Quantitative results (WS-PSNR/WS-SSIM) on ODI-SR and SUN360 datasets*

与通用SISR方法相比，EDSR（Lim et al., CVPRW 2017）、RCAN（Zhang et al., ECCV 2018）和SwinIR（Liang et al., ICCV 2021）在全向图像上表现明显不足，因为它们未考虑球面投影的几何特性。在全向SR专用方法中，LAU-Net（Deng et al., CVPR 2021）通过纬度自适应策略改善边缘区域重建，SphereSR（Yoon et al., CVPR 2022）采用连续球面表示，OSRT（Yu et al., CVPR 2023）引入畸变感知Transformer，但这些方法在×8和×16的高倍率下仍存在边缘模糊和结构失真问题。EAM通过显式的边缘注意力建模和全局特征集成，在定量指标上全面超越这些基线。

在计算效率方面，**Table 2**展示了×16任务中各方法的参数量、FLOPs和推理时间对比。EAM在保持竞争性计算开销的同时实现了最优重建质量，体现了边缘聚焦模块设计的效率优势。

![[assets/figures/papers/paper_list_l2251_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Edge_Focused_Supe/figures/007_Table_2.jpg]]
*Table 2: Computational efficiency comparison across methods for ×16 super-resolution on the ODI-SR dataset*

### 消融实验分析

#### 数据增强的有效性

**Table 3**展示了球面坐标数据增强的消融结果。在×8任务中，采用球面增强后WS-PSNR从无增强的约24.95 dB提升至**25.69 dB**，WS-SSIM从0.6529提升至**0.6839**；在×16任务中同样观察到一致的性能增益。这一结果证实了球面几何一致的增强策略能有效保持场景连续性，为网络提供更合理的训练样本，从而改善边缘恢复质量。

#### 网络组件的必要性

**Table 4**对EAM的核心组件进行了消融分析。完整EAM（包含EEB、ERB和GIB）在×8任务上取得25.69 dB / 0.6839的最优结果。移除GIB后性能下降，验证了全局整合模块在捕获长程依赖和扩展感受野方面的作用。进一步移除ERB或EEB均导致WS-PSNR和WS-SSIM的持续下降，证明了边缘增强与边缘细化两个子模块的互补性——EEB负责多尺度边缘特征的初步增强，ERB通过自适应加权机制进一步细化边缘可靠性。

#### 损失函数的互补效应

**Table 5**比较了不同损失函数组合的影响。联合使用L1损失、SSIM损失和感知损失（权重分别为1、0.1和0.01）取得了最高WS-PSNR（25.69 dB）。单独使用L1+感知损失或L1+SSIM损失时性能次之，表明三者之间存在互补关系：L1损失保证像素级重建精度，SSIM损失约束结构相似性，感知损失提升视觉质量。权重设置（感知损失仅0.01）说明在该任务中像素保真度和结构一致性比高层语义感知更为关键。

### 可视化分析

**Figure 5**展示了×8超分辨率任务的可视化对比结果。EAM在边缘区域（如建筑轮廓、文字边缘）的重建清晰度明显优于其他方法，边缘连续且无明显伪影。相比之下，FATO和OSRT在强边缘处仍存在模糊或锯齿现象，SwinIR则容易产生结构扭曲。这直观验证了边缘聚焦模块（EEB和ERB）在保持边缘完整性和连续性方面的设计优势。

**Figure 6**对比了数据增强前后的重建效果。采用球面增强后，全景图的环形结构保持完整，边缘过渡自然；未增强时在图像边界处出现明显的纹理断裂和伪影。这一视觉差异与**Table 3**的定量结果一致，进一步证实了球面坐标变换增强对于维持全向图像拓扑连续性的关键作用。

### 失败模式与局限性

尽管EAM在定量和定性评估中均表现优异，但论文未明确讨论具体的失败案例。根据方法设计推断，潜在的局限性包括：球面增强依赖于准确的等距柱状投影假设，当输入图像存在严重投影畸变或非标准投影时，增强效果可能受限；边缘聚焦模块依赖于显式的边缘注意力建模，在纹理极度复杂或边缘方向高度各向异性的区域，多尺度扩张卷积的固定感受野可能不足以捕获所有边缘模式。此外，该方法仅在ODI-SR和SUN360数据集上验证，其在不同下采样退化（如模糊核退化）或真实场景全向图像上的泛化能力尚待进一步检验。

![[assets/figures/papers/paper_list_l2251_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Edge_Focused_Supe/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparisons of ×8 SR results of different methods on ODI-SR dataset*

![[assets/figures/papers/paper_list_l2251_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Edge_Focused_Supe/figures/008_Table_4.jpg]]
*Table 4: Ablation study on EAM components.All models are trained on ×8 SR task on ODI-SR dataset*

## 定位与知识库关联

### 任务定位与基线关系

本文聚焦于**全向图像超分辨率（ODISR）** 这一细分任务，其核心挑战在于等距柱状投影（ERP）引入的几何失真与高倍率下（×8、×16）边缘细节的严重丢失。与通用单图像超分辨率（SISR）方法不同，ODISR 必须处理球面投影的非均匀采样特性。

**基线方法谱系**可划分为两条主线：

1. **通用 SISR 方法**：包括 **EDSR**（Lim et al., CVPRW 2017）的深度残差架构、**RCAN**（Zhang et al., ECCV 2018）的通道注意力机制，以及 **SwinIR**（Liang et al., ICCV 2021）的 Transformer 架构。这些方法在常规图像上表现优异，但缺乏对球面投影失真的建模，直接应用于 ODISR 时边缘恢复能力显著不足。

2. **专用 ODISR 方法**：**LAU-Net**（Deng et al., CVPR 2021）引入纬度自适应上采样以应对 ERP 的拉伸效应；**SphereSR**（Yoon et al., CVPR 2022）将球面图像表示为连续球面信号进行超分；**OSRT**（Yu et al., CVPR 2023）设计了失真感知的 Transformer；**FATO**（An et al., MM Asia 2024）则采用频率注意力 Transformer。FATO 是本文实验时公开的最优方法（×8 任务 24.54 dB WS-PSNR），但该类方法均未显式建模边缘注意力机制。

### 本文方法的知识贡献

本文提出的 **Edge-Aware Multi-Scale (EAM) 网络 + 球面几何增强**框架，在两个维度上区别于现有工作：

**维度一：球面几何一致的数据增强。** 传统二维平移/旋转在 ERP 投影下会产生不可逆的几何扭曲（如环形结构断裂）。本文通过球面坐标变换（Eq.1–Eq.6）将增强操作定义在单位球上的三维旋转，保持了场景的拓扑连续性和几何完整性。这一设计不是简单的数据扩充技巧，而是对 ODISR 任务中“视角一致性”这一先验的显式编码。

**维度二：边缘聚焦的多尺度注意力架构。** EAM 的核心创新在于三个模块的协同设计：
- **边缘增强模块（EEB）**：通过多尺度扩张卷积与边缘感知的通道/空间注意力（Eq.10–Eq.12），在特征提取阶段即强化边缘响应；
- **边缘细化模块（ERB）**：利用可学习权重 α 自适应融合原始特征与边缘可靠性图调制的细化特征（Eq.13），实现边缘信息的精炼；
- **全局整合模块（GIB）**：通过大核深度可分离卷积和注意力融合（Eq.14–Eq.15），扩展感受野以捕获长程依赖，弥补局部边缘模块在全局结构感知上的不足。

这三个模块形成“增强—细化—整合”的级联流水线，与现有 ODISR 方法中普遍采用的单一注意力或 Transformer 架构形成互补而非替代关系。

### 适用边界与局限

基于文中提供的证据（Tab.1, Tab.3, Tab.4），EAM 的适用边界可归纳如下：

1. **数据集规模约束**：ODI-SR 数据集仅含 1200 张图像（1024×2048 分辨率），球面几何增强通过模拟视角变化有效缓解了数据稀缺问题。但在更大规模、更多样化的真实场景下，该方法的泛化能力尚待验证——文中未提供跨数据集或跨退化类型的实验。

2. **投影类型限制**：方法设计紧密耦合于等距柱状投影（ERP）的球面坐标映射。对于其他全向投影类型（如鱼眼、立方体贴图），球面坐标变换的适用性需要重新验证，文中未涉及此类讨论。

3. **计算效率权衡**：Table 2 提供了 ×16 任务下的 FLOPs、参数量和推理时间对比，但分析未给出具体数值。需要手动核实 EAM 相对于 FATO 等轻量方法的效率差异——若 GIB 的大核卷积带来显著开销，则在实时应用场景中可能受限。

4. **损失函数组合的通用性**：联合损失 $L_{\mathrm{Total}} = L_{\mathrm{L1}} + 0.01 \times L_{\mathrm{Perceptual}} + 0.1 \times (1 - L_{\mathrm{SSIM}})$ 的权重（0.01 和 0.1）是在 ODI-SR 上调优的结果（Tab.5），迁移到其他数据集时可能需要重新校准。

### 开放问题

1. **跨投影泛化**：球面坐标增强框架能否适配鱼眼、立方体贴图等非 ERP 投影？若推广，坐标映射公式（Eq.1–Eq.6）需如何调整？

2. **增强策略的边界**：文中旋转角度 γ ∈ [0, 2π] 已覆盖完整水平旋转，但俯仰方向的增强范围未明确。更大的视角变化范围或引入更多样的球面几何变换（如球面缩放）能否进一步提升性能？

3. **边缘注意力机制的效率优化**：EEB 中的多尺度扩张卷积和双注意力计算是否可通过神经架构搜索（NAS）或轻量化设计（如深度可分离卷积替换）进一步压缩？这对于将方法部署到移动端或实时系统至关重要。

4. **真实退化场景的鲁棒性**：当前实验采用理想的下采样退化（直接 resize），而真实全向图像可能面临运动模糊、压缩伪影、传感器噪声等复合退化。EAM 在盲超分辨率设定下的表现需要进一步研究。

5. **与最新 ODISR 方法的对比时效性**：文中对比的最优方法 FATO 发表于 MM Asia 2024，若后续有更强基线（如基于扩散模型或更先进 Transformer 的方法）出现，EAM 的性能优势需要重新评估。此点需手动确认论文投稿时间线与同期工作的关系。

## 原文 PDF

![[paperPDFs/CVPR_2026/Edge_Focused_Super_Resolution_for_Omnidirectional_Images_with_Spherical_Geometric_Augmentation.pdf]]

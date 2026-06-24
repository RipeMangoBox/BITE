---
title: "RAP: 3D Rasterization Augmented End-to-End Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RAP_3D_Rasterization_Augmented_End_to_End_Planning.pdf
openreview_forum_id: a9bOgeqbdB
aliases:
- RRAP
- RAP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用轻量级3D光栅化（保留几何、语义和动态信息，忽略纹理/光照）生成可扩展的合成视图，并结合特征空间对齐（R2R模块）弥合sim-to-real差距，从而实现大规模的反事实恢复性扰动和跨代理视角增强。"
primary_logic: "端到端驾驶规划训练不需要照片级真实感；语义准确性与可扩展性远比像素级逼真更重要。光栅化标注基元能保留规划必需的几何与动态线索，而特征空间对齐比像素级对齐更有效、更稳定地迁移语义知识。"
claims:
- "RAP-DINO在NAVSIM v1上以93.8 PDMS取得最高分，超越此前所有相机方法"
- "RAP-DINO在NAVSIM v2上取得36.93两阶段EPDMS，远高于LTF的23.12"
- "恢复性扰动将NAVSIM v2两阶段EPDMS从32.5提升至36.9，验证了反事实增强对闭环鲁棒性的关键作用"
- "R2R特征对齐消融显示，空间+全局对齐在所有真实数据比例下均显著优于无对齐"
---

# RAP: 3D Rasterization Augmented End-to-End Planning

> [!tip] 核心洞察
> 端到端驾驶规划训练不需要照片级真实感；语义准确性与可扩展性远比像素级逼真更重要。光栅化标注基元能保留规划必需的几何与动态线索，而特征空间对齐比像素级对齐更有效、更稳定地迁移语义知识。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RAP：3D光栅化增强的端到端规划 |
| 英文题名 | RAP: 3D Rasterization Augmented End-to-End Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=a9bOgeqbdB); [Project](https://alan-lanfeng.github.io/RAP/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | RAP (Rasterization Augmented Planning) |
| Dataset | NAVSIM v1 (navtest), NAVSIM v2 (navhard), WOD Vision-based E2E Driving |

> [!tip] 效果简介
> - NAVSIM v1 (navtest) 上，PDMS↑ 为 93.8，对比 92.1 (Centaur)，变化 +1.7。
> - NAVSIM v2 (navhard) 上，two-stage EPDMS↑ 为 36.93，对比 23.12 (LTF)，变化 +13.81。
> - WOD Vision-based E2E Driving 上，ADE@5s↓ 为 2.65，对比 2.74 (Poutine)，变化 -0.09。

## 概述

端到端自动驾驶系统长期受困于一个根本矛盾：模仿学习训练的规划器缺乏对分布外状态的恢复能力，在闭环测试中因协变量漂移导致误差快速累积；而现有基于神经渲染或物理引擎的真实感数据增强方案速度慢、成本高，难以大规模生成反事实训练数据。RAP（Rasterization Augmented Planning）针对这一瓶颈提出了一条差异化路径——**端到端驾驶规划训练不需要照片级真实感，语义准确性与可扩展性远比像素级逼真更重要**。

方法的核心机制是双重的。其一，采用**轻量级3D光栅化管线**，将标注基元（车道线折线、有向立方体）投影为可控的透视视图，保留场景几何与动态信息的同时舍弃纹理和光照细节，从而以极低成本生成大规模合成样本。在此基础上，通过恢复性轨迹扰动和跨代理视角合成，系统性地注入反事实场景与交互多样性。其二，引入**Raster-to-Real（R2R）特征空间对齐模块**，以空间级MSE损失和全局域对抗对齐弥合合成视图与真实图像的分布差距，使语义知识从光栅化域向真实域稳定迁移。

实验证据支撑了这一设计的有效性。RAP-DINO在NAVSIM v1上以93.8 PDMS取得最高分（Table 1），在NAVSIM v2更具挑战性的两阶段评估中以36.93 EPDMS大幅领先（Table 2），在WOD端到端驾驶挑战赛和Bench2Drive闭环基准上也均位列第一（Table 3、Table 4）。消融实验进一步揭示了因果机制：恢复性扰动对NAVSIM v2两阶段EPDMS的提升达4.4分（32.5→36.9），而对v1无影响，表明该增强专为闭环鲁棒性设计（Table 6）；R2R对齐在所有真实数据比例下均显著优于无对齐，且50%合成数据时性能已超越100%真实数据训练（Figure 5）；跨代理视角合成呈现高度对数缩放规律（$R^2=0.9942$），表明该方法具备可预测且持续的规模收益（Figure 6）。

在方法谱系中，RAP区别于**Centaur**（Sima et al., arXiv 2025）的测试时训练范式、**DiffusionDrive**（Liao et al., CVPR 2025）的截断扩散策略以及**UniAD**（Hu et al., CVPR 2023）的规划导向架构，其独特贡献在于将数据增强从像素空间迁移至特征空间，并以光栅化基元替代昂贵的渲染引擎。该方法依赖高质量的场景标注（车道线、3D目标框），在标注稀疏或噪声场景中有效性可能下降，但定性分析表明模型仍能从真实图像中学习未标注的视觉线索（Figure 7）。当前验证限于仿真与日志基准，实际路测尚未开展。

## 背景与动机

端到端自动驾驶旨在直接从传感器输入映射到驾驶动作或轨迹，省去传统模块化流水线中的中间表示。近年来，模仿学习（imitation learning）驱动的端到端规划器在开环评测中取得了显著进展，但在闭环测试中仍面临一个根本性瓶颈：**协变量漂移（covariate shift）**。由于训练数据仅包含专家演示，模型从未见过偏离专家轨迹后的状态，一旦测试中出现微小误差，便会迅速累积并导致灾难性失败。本质上，模仿学习训练的端到端策略缺乏恢复数据——它不知道如何从不安全状态回到安全状态。

解决这一问题的自然思路是通过数据增强来暴露模型于更多样化的场景，尤其是反事实的恢复性操作。然而，现有的数据增强手段面临两难困境：

- **基于神经渲染或物理引擎的真实感增强**（如NeRF、3DGS、游戏引擎）虽然能够生成逼真的合成视图，但计算成本极高、速度慢，难以大规模生成训练数据。这些方法试图在像素空间弥合sim-to-real差距，却付出了难以承受的算力代价。
- **传统的图像空间增强**（如裁剪、色彩抖动）则缺乏对驾驶场景几何和动态信息的控制，无法生成语义上有意义的反事实场景（例如“如果车辆偏移了车道中心，应该如何恢复”）。

这一困境揭示了一个更深层的认知盲区：**端到端驾驶规划训练是否真的需要照片级真实感？** 驾驶规划的核心信息——车道线几何、交通参与者的三维位姿与运动、可通行区域边界——本质上都是结构化的几何与语义线索，而非纹理细节或光照效果。如果能以极低成本保留这些关键信息，同时大规模生成可控的合成视图，就有望打破现有数据增强的瓶颈。

正是基于这一洞察，本文提出了 **RAP（Rasterization Augmented Planning）** 框架。其核心思想是：**语义准确性与可扩展性远比像素级逼真更重要**。具体而言，RAP采用轻量级3D光栅化（3D Rasterization）将标注基元（车道线折线、有向立方体）投影为可控的透视视图，在保留几何、语义和动态信息的同时舍弃纹理与光照细节。这种极简的合成方式使得大规模反事实数据增强成为可能：通过自车轨迹的恢复性扰动（recovery-oriented perturbation）和跨代理视角合成（cross-agent view synthesis），RAP能够以极低成本生成超过50万训练样本。

此外，为了弥合光栅化视图与真实图像之间的域差距，RAP引入了 **Raster-to-Real（R2R）特征空间对齐模块**，通过空间级蒸馏损失和全局域对抗对齐，使模型在特征层面将合成视图与真实图像统一，而非在像素层面追求逼真度。实验表明，特征空间对齐比像素级对齐更有效且更稳定地迁移语义知识。

综上所述，RAP的动机可归纳为三个递进的判断：
1. 闭环鲁棒性的关键在于暴露于反事实恢复场景，而这需要大规模、可控的数据增强；
2. 现有真实感渲染方法速度慢、成本高，无法满足大规模增强的需求；
3. 驾驶规划不需要照片级真实感——保留几何与动态信息的光栅化基元已足够，配合特征空间对齐即可实现有效的sim-to-real迁移。

## 核心创新

RAP框架针对模仿学习在端到端驾驶中的核心瓶颈——**协变量漂移导致闭环误差累积**与**现有数据增强方法速度慢、成本高**——提出了三个关键创新，构成一条完整的“合成-对齐-增强”技术链路。

### 创新一：轻量级3D光栅化替代昂贵渲染

传统的数据增强依赖神经渲染或物理引擎生成真实感视图，计算开销巨大，难以大规模扩展。RAP的核心洞察在于：**端到端规划训练不需要照片级真实感，语义准确性与可扩展性远比像素级逼真更重要**。

基于此，RAP设计了一个轻量级3D光栅化管线：将标注基元——车道线多段线（polylines）和有向立方体（oriented cuboids）——通过针孔相机模型投影到透视视图：

$$u_{uv} = \pi(p_w) = K T_{w c} \tilde{p}_w$$

立方体的八个角点由尺寸和SE(3)位姿计算：

$$C_i = T_i \left[ \pm l_i/2 \quad \pm w_i/2 \quad 0, h_i \right]^\top$$

为处理遮挡，光栅化采用深度感知合成，通过淡出权重 $\alpha = \max(0, 1 - d / d_{\max})$ 实现平滑的前后层叠。该管线**保留场景几何、语义和动态信息，丢弃纹理/光照细节**（见图3），使得单场景生成成本从秒级降至毫秒级，支撑大规模数据生产。

消融实验（Table 5）验证了设计选择的有效性：固体颜色面片+深度衰减+黑色背景的组合取得最优MinADE（0.91），移除任一组份均导致性能下降。

### 创新二：Raster-to-Real特征空间对齐

光栅化视图与真实图像之间存在天然的域间隙。RAP**放弃像素级对齐，转向特征空间对齐**，提出R2R（Raster-to-Real）模块，包含两个互补层次：

- **空间级对齐**：将真实特征图 $F^r$ 向冻结的光栅特征图 $F^s$ 对齐，使用MSE损失 $\mathcal{L}_{\mathrm{spatial}} = \frac{1}{N} \sum_{j=1}^{N} \| F_{j}^{r} - F_{j}^{s} \|_{2}^{2}$，保持空间结构一致性。
- **全局对齐**：通过梯度反转层（GRL）与域分类器 $D$ 实现对抗域适应，损失为 $\mathcal{L}_{\mathrm{global}} = - \mathbb{E}_{(g, y)} [ y \log D(g) + (1 - y) \log (1 - D(g)) ]$，使编码器提取域不变特征。

总训练目标为 $\mathcal{L} = \mathcal{L}_{\mathrm{task}} + \lambda_{s} \mathcal{L}_{\mathrm{spatial}} + \lambda_{g} \mathcal{L}_{\mathrm{global}}$。

消融结果（Figure 5）表明：空间+全局对齐在所有真实数据比例下均显著优于无对齐基线，且**仅用50%合成数据配合对齐，性能即可超越100%真实数据训练**。对齐方向消融（Table 7）进一步揭示Real-to-Raster方向最优（MinADE 1.02），优于Raster-to-Real（1.12）和对称对齐（1.14）。

### 创新三：反事实数据增强策略

基于光栅化的可控性，RAP引入两类传统方法难以实现的大规模增强：

1. **恢复性扰动**：对自车轨迹施加横向偏移、纵向偏移和高斯噪声 $\tilde{\tau}(t) = \tau^*(t) + \delta_{\mathrm{lat}}(t) + \delta_{\mathrm{long}}(t) + \epsilon_t$，生成从偏离分布状态恢复的反事实场景，直接针对协变量漂移问题。消融（Table 6）显示该增强对NAVSIM v1无影响（92.5→92.5），但使v2两阶段EPDMS从32.5提升至36.9（+4.4），验证了其专为闭环鲁棒性设计的有效性。

2. **跨代理视角合成**：利用其他交通参与者的视角生成多样化交互样本。缩放实验（Figure 6）发现合成样本数与MinADE呈高度对数相关（$y = -0.021 \ln(x) + 1.2173$，$R^2 = 0.9942$），表明该方法具备可预测且持续的缩放收益。

### 方法谱系与知识库定位

RAP属于**数据驱动端到端规划**范式，与以下工作形成对比：

| 维度 | 现有方法 | RAP |
|------|---------|-----|
| 数据增强 | 无（**UniAD** Hu et al., CVPR 2023; **VAD** Jiang et al., ICCV 2023）或依赖昂贵渲染 | 轻量3D光栅化，毫秒级生成 |
| 域适应 | 像素级（神经渲染方法）或无显式对齐 | 特征空间R2R对齐（空间+全局） |
| 反事实训练 | 无（标准模仿学习） | 恢复性扰动+跨代理视角合成 |
| 规划器架构 | 各方法独立设计（**DiffusionDrive** Liao et al., CVPR 2025; **iPad** Guo et al., arXiv 2025; **LTF** Chitta et al., 2023） | 兼容多种规划器（DINO/ResNet骨干） |

RAP的核心贡献不在于规划器架构创新，而在于**提出了一种可扩展、与规划器解耦的数据增强与域适应框架**，通过“语义精确的合成+特征空间对齐”解决了端到端驾驶中长期存在的数据稀缺与闭环鲁棒性瓶颈。

## 整体框架

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_a9bOgeqbdB/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed RAP. (a) Data Augmentations via 3D Rasterization: annotated driving logs are converted into large-scale synthetic samples through cross-agent view synthesis and recovery-oriented perturbation. (b) Raster-to-Real Alignment: paired real and rasterized inputs are processed by a frozen image encoder and a learnable feature projector. Spatial-level alignment uses MSE loss against detached raster features, while global-level alignment employs a gradient reversal layer and domain classifier to enforce domain confusion*

RAP 框架围绕一个核心洞察构建：端到端驾驶规划训练不需要照片级真实感，语义准确性与可扩展性远比像素级逼真更重要。基于此，RAP 用轻量级3D光栅化替代昂贵的神经渲染或引擎渲染，在保留几何、语义和动态信息的前提下生成大规模可控合成视图，再通过特征空间对齐弥合合成到真实的域间隙，最终增强模仿学习策略的闭环鲁棒性。

框架由三大模块串联而成，如图2所示：

**1. 3D光栅化管线（数据生成引擎）**
将标注基元（车道多段线、智能体有向立方体）通过针孔相机模型投影到透视视图，经深度感知合成生成光栅化图像。该管线丢弃纹理和光照细节，仅保留规划必需的几何结构与动态线索，具备高可扩展性和完全可控性。

**2. 数据增强模块（训练样本扩展）**
在光栅化视图基础上施加两类增强：
- **恢复性扰动**：对自车轨迹施加横向/纵向偏移和高斯噪声，生成反事实恢复场景，使策略学会从分布外状态回归。
- **跨代理视角合成**：从其他智能体的视角渲染场景，扩展交互多样性。

最终构建的数据集包含85k真实-光栅配对样本、272k自车光栅样本、200k其他车辆光栅样本及8.5k扰动样本，总计超500k训练样本。

**3. Raster-to-Real（R2R）特征对齐模块**
这是弥合sim-to-real差距的关键。模块包含两个层次：
- **空间级对齐**：以均方误差损失将真实图像的特征图向冻结的光栅特征图对齐。
- **全局级对齐**：通过梯度反转层与域分类器实现无监督域适应，迫使编码器提取域不变全局特征。

最终训练目标为规划任务损失与两级对齐损失的加权和：
$$\mathcal{L} = \mathcal{L}_{\mathrm{task}} + \lambda_{s} \mathcal{L}_{\mathrm{spatial}} + \lambda_{g} \mathcal{L}_{\mathrm{global}}$$

**输入输出流**：训练时，配对的真实图像与光栅化视图分别经冻结的DINOv3-H骨干网络提取特征，再由可学习的MLP投影器处理后送入迭代可变形注意力解码器，输出多模态轨迹及其评分。推理时仅需真实图像输入，无需光栅化管线。

该框架的核心设计选择——在特征空间而非像素空间对齐——源于一个关键观察：冻结DINOv3提取的光栅化与真实图像特征具有相似的PCA结构（图4），说明光栅化基元作为感知替代是有效的。特征空间对齐比像素级对齐更稳定、更高效地迁移语义知识，使得RAP能够以极低的计算成本实现大规模反事实数据增强。

## 核心模块与公式推导

RAP框架的核心由三个模块构成：3D光栅化管线、数据增强策略、以及Raster-to-Real（R2R）特征对齐模块。以下逐一阐述其关键设计与数学表达。

### 3D光栅化管线

该管线将标注基元投影为可控的透视视图，替代昂贵的神经渲染或引擎渲染。场景表示分为两类：

- **静态地图元素**（车道线、人行横道等）以多段线（polylines）表示；
- **交通参与者**（车辆、行人等）以有向立方体（oriented cuboids）近似。

投影过程基于针孔相机模型。给定世界坐标系下的3D点 $p_w$，其齐次坐标 $\tilde{p}_w$ 经世界到相机的外参 $T_{wc}$ 和内参矩阵 $K$ 投影至图像平面：

$$u_{uv} = \pi(p_w) = K T_{wc} \tilde{p}_w$$

随后通过透视除法获得像素坐标：

$$(u, v) = \left( \frac{u_x}{u_z}, \frac{u_y}{u_z} \right)$$

对于每个交通参与者，根据其尺寸 $(l_i, w_i, h_i)$ 和 $\text{SE}(3)$ 位姿 $T_i$ 计算有向立方体的八个角点：

$$C_i = T_i \left[ \pm l_i/2 \quad \pm w_i/2 \quad 0, h_i \right]^\top$$

所有基元被光栅化到RGB画布中，采用深度感知合成（depth-aware compositing）。每个片段存储深度 $d$，并通过淡出权重实现遮挡处理：

$$\alpha = \max(0, 1 - d / d_{\max})$$

跨越近裁剪面的基元使用Sutherland–Hodgman裁剪处理。消融实验（Table 5）表明，**固体颜色面片 + 深度衰减 + 黑色背景**的配置取得最低MinADE（0.91），移除任一组分均导致性能下降。

### 数据增强策略

基于3D光栅化的可控性，RAP设计了两种数据增强：

**恢复性扰动**：通过对真实自车轨迹施加横向偏移 $\delta_{\text{lat}}(t)$、纵向偏移 $\delta_{\text{long}}(t)$ 和高斯噪声 $\epsilon_t$，生成反事实恢复场景：

$$\tilde{\tau}(t) = \tau^*(t) + \delta_{\text{lat}}(t) + \delta_{\text{long}}(t) + \epsilon_t$$

这迫使规划器学习从分布外状态恢复的能力。消融实验（Table 6）显示，扰动对NAVSIM v1无影响（PDMS均为92.5），但将NAVSIM v2的两阶段EPDMS从32.5显著提升至36.9，表明该增强专为闭环鲁棒性设计。

**跨代理视角合成**：利用日志中其他智能体的轨迹生成其视角下的光栅化视图，扩展交互多样性。实验（Figure 6）揭示合成样本数 $x$ 与MinADE $y$ 之间呈高度对数相关：

$$y = -0.021 \ln(x) + 1.2173, \quad R^2 = 0.9942$$

这表明该方法具备可预测且持续的缩放收益。

### Raster-to-Real（R2R）特征对齐

R2R模块在特征空间弥合合成视图与真实图像之间的域间隙，包含两个层次：

**空间级对齐**：冻结光栅特征图 $F^s$，通过均方误差损失将真实特征图 $F^r$ 向其靠拢：

$$\mathcal{L}_{\text{spatial}} = \frac{1}{N} \sum_{j=1}^{N} \| F_{j}^{r} - F_{j}^{s} \|_{2}^{2}$$

**全局级对齐**：在编码器后插入梯度反转层（GRL），配合域分类器 $D$ 实现对抗域适应。分类器以域标签 $y$ 监督，而编码器通过GRL被优化为最大化域混淆：

$$\mathcal{L}_{\text{global}} = - \mathbb{E}_{(g, y)} \bigl[ y \log D(g) + (1 - y) \log (1 - D(g)) \bigr]$$

GRL的缩放因子 $\lambda(p)$ 随训练进度 $p$ 平滑退火：

$$\lambda(p) = 0.1 \cdot \left( \frac{2}{1 + \exp(-\gamma p)} - 1 \right)$$

**总体训练目标**由规划任务损失与两级对齐损失加权组成：

$$\mathcal{L} = \mathcal{L}_{\text{task}} + \lambda_{s} \mathcal{L}_{\text{spatial}} + \lambda_{g} \mathcal{L}_{\text{global}}$$

消融实验（Figure 5）表明，空间+全局对齐在所有真实数据比例下均显著优于无对齐，且在50%合成数据时性能已超过100%真实数据训练。对齐方向消融（Table 7）进一步显示，**Real-to-Raster**对齐（将真实特征向冻结的光栅特征对齐）优于Raster-to-Real和对称对齐，在50%真实数据下MinADE降至1.02。

## 实验与分析

### 核心实验设置

RAP 在三个互补基准上评估：NAVSIM v1（开环，navtest）、NAVSIM v2（两阶段反事实评估，navhard）、Waymo Open Dataset 视觉端到端驾驶挑战赛（WOD-E2E），以及 Bench2Drive（闭环仿真）。规划器采用两种配置：**RAP-DINO** 以冻结 DINOv3-H 为骨干配合可学习 MLP 投影器和迭代可变形注意力解码器，用于开环评估；**RAP-ResNet** 以 ResNet34 为骨干，用于闭环实时推理。训练数据包含 85k 真实-光栅配对样本、272k 自车光栅样本、200k 其他车辆光栅样本和 8.5k 扰动样本，总规模超过 500k。

### 主要结果

**NAVSIM v1（开环）**：如 Table 1 所示，RAP-DINO 以 **93.8 PDMS** 取得最高分，超越此前所有相机方法，包括 Centaur（92.1）、iPad（91.8）和 DiffusionDrive（91.3）。在子指标上，RAP-DINO 在无碰撞（NC 99.1）、可驾驶区域合规（DAC 98.9）和碰撞时间（TTC 96.7）上均为第二。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_a9bOgeqbdB/figures/006_Table_1.jpg]]
*Table 1: NAVSIM v1 benchmark (navtest). Bold/underlined indicates the best/second-best*

**NAVSIM v2（两阶段反事实）**：如 Table 2 所示，RAP-DINO 以 **36.93 EPDMS** 大幅领先 LTF 的 23.12（+13.81），在 Stage 1 和更具挑战性的 Stage 2 反事实评估中均保持强势。这一结果直接验证了恢复性扰动增强对闭环鲁棒性的关键作用——Table 6 消融显示，扰动对 v1 无影响（均为 92.5），但将 v2 两阶段 EPDMS 从 32.5 提升至 36.9。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_a9bOgeqbdB/figures/007_Table_2.jpg]]
*Table 2: Public leaderboard for the NAVSIM v2 benchmark (navhard). Bold indicates the best result*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_a9bOgeqbdB/figures/011_Table_6.jpg]]

**WOD-E2E 驾驶挑战赛**：如 Table 3 所示，RAP-DINO 在公开排行榜上取得 **ADE@5s 2.65**（此前最佳 Poutine 为 2.74）和 **RFS (Overall) 8.04**（此前最佳 ViT-Adapter-GRU / Poutine 为 7.99），在轨迹精度和综合评分上均实现 SOTA。

**Bench2Drive（闭环）**：如 Table 4 所示，RAP-ResNet 取得最高驾驶分数 **66.42**（此前最佳 iPad 为 65.02）和最高成功率 **37.27%**（iPad 35.91%），同时在效率和舒适度指标上也领先，验证了方法在真实闭环条件下的泛化能力。

### 消融分析

#### 3D 光栅化设计选择

Table 5 消融了三个关键设计因素：面片渲染类型（纯色 vs 半透明）、深度衰减（有/无）和背景（黑色 vs 自然图像）。实验表明，**纯色面片 + 深度衰减 + 黑色背景**的组合取得最低 MinADE（0.91）。移除深度衰减导致性能下降最显著，因为深度感知合成是实现正确遮挡处理的核心机制。Figure 9 提供了各配置的定性可视化，最右侧的完整配置提供了信息量最丰富且最稳定的场景表示。

#### 恢复性扰动

Table 6 揭示了扰动增强与评估范式之间的深刻关联：在 NAVSIM v1 的标准开环评估下，扰动无效果（PDMS 均为 92.5）；但在 NAVSIM v2 的两阶段反事实评估中，扰动将 EPDMS 从 32.5 提升至 36.9（+4.4）。这证实了**协变量漂移是模仿学习端到端规划的核心瓶颈**：标准开环指标无法暴露模型在分布外状态下的脆弱性，而恢复性扰动通过显式生成反事实恢复场景，使模型学会从偏离状态中安全回归。

#### R2R 特征对齐

Figure 5 展示了三个对齐策略在不同真实数据比例下的 MinADE 曲线：无对齐、空间对齐、空间+全局对齐。两个关键发现：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_a9bOgeqbdB/figures/012_Figure_5.jpg]]
*Figure 5: Ablation on R2R alignment (Section 4.2), showing that both spatial and global alignment improve performance*

1. **两种对齐策略在所有真实数据比例下均优于无对齐**，且空间+全局对齐组合始终最优。
2. **使用 50% 合成数据 + R2R 对齐的性能已超过 100% 真实数据训练**，证明特征空间对齐能有效弥合 sim-to-real 差距，使合成数据成为真实数据的有效替代而非补充。

Table 7 进一步比较了对齐方向：**Real-to-Raster 对齐**（将真实特征向冻结的光栅特征对齐）在 50% 真实数据下取得 MinADE 1.02，优于 Raster-to-Real（1.12）和对称对齐（1.14）。这一方向选择的关键在于：冻结的光栅特征作为稳定锚点，避免了合成特征被真实图像中的噪声或纹理干扰。

#### 跨代理视角合成的缩放特性

Figure 6 揭示了跨代理视角合成样本数与 MinADE 之间高度吻合的**对数缩放规律**：$y = -0.021 \ln(x) + 1.2173$，$R^2 = 0.9942$。这表明该方法具备可预测且持续的缩放收益——每增加一个数量级的合成样本，MinADE 稳定下降约 0.021。这一发现具有重要的实践意义：用户可以根据目标性能需求，精确估算所需的合成数据规模。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_a9bOgeqbdB/figures/013_Figure_6.jpg]]
*Figure 6: Scaling curve for cross-agent view synthesis (Section 4.2), showing consistent gains as more synthetic samples are added*

### 定性分析

Figure 7 展示了 RAP-DINO 对未标注真实世界线索的感知能力。在左侧场景中，模型从真实图像正确识别了未标注的 "Keep Left" 标志（光栅化视图中不存在），输出正确轨迹；而仅依赖光栅化输入的模型失败。右侧场景展示了模型从真实图像识别出光栅化数据中不存在的动态 LED 箭头，安全完成变道。这表明 **R2R 对齐成功保留了模型从真实图像中学习未标注视觉线索的能力**，避免了纯合成训练可能带来的语义盲区。

Figure 8 展示了 WOD-E2E 数据集上的定性规划结果，RAP-DINO 成功识别停止标志、锥桶和夜间来车，输出准确且安全的轨迹规划。

### 局限与失败模式

1. **标注依赖性**：3D 光栅化依赖高质量的场景标注（车道线、3D 目标框），在标注稀疏或噪声显著的场景中，光栅化视图可能丢失关键信息。虽然定性实验表明模型能从真实图像补偿部分缺失线索，但在完全无真实图像的纯合成训练下效果未知。
2. **纹理/光照信息丢失**：光栅化舍弃了纹理和光照细节，可能无法编码某些对驾驶至关重要的视觉线索（如路面湿滑状态、临时施工标志的颜色语义）。当前方法依赖真实图像分支弥补这一缺陷，但增加了训练数据需求。
3. **闭环验证范围有限**：闭环测试仅在 Bench2Drive 仿真环境中完成，尚未在实际路测中验证。NAVSIM v2 的两阶段评估虽能更好地反映闭环性能，但仍是对真实闭环的近似。
4. **对抗训练不稳定性**：全局对齐依赖梯度反转层的对抗训练，可能引入训练不稳定。论文使用平滑退火策略 $\lambda(p) = 0.1 * \left( \frac{2}{1 + \exp(-\gamma p)} - 1 \right)$ 缓解此问题，但在更大规模训练中仍需关注。
5. **视角选择策略未优化**：跨代理视角合成目前采用随机采样，尚未探索基于交互密度或不确定性的智能选择策略，可能未充分利用日志数据的潜力。

## 方法谱系与知识库定位

### 核心洞察与瓶颈突破

RAP的核心洞察在于一个反直觉的判断：**端到端驾驶规划训练不需要照片级真实感**。语义准确性与可扩展性远比像素级逼真更重要。这一判断直接回应了当前模仿学习范式下的真实瓶颈——端到端驾驶策略因缺乏恢复数据，在闭环测试中因协变量漂移导致误差快速累积；而现有基于神经渲染或物理引擎的真实感数据增强方法速度慢、成本高，无法大规模生成训练数据。

RAP的因果调节旋钮由三个组件构成：**轻量级3D光栅化**（保留几何、语义和动态信息，丢弃纹理/光照）生成可扩展的合成视图；**特征空间R2R对齐**弥合sim-to-real差距；以及基于光栅化的大规模**反事实数据增强**（恢复性扰动+跨代理视角合成）。三者协同使模型在闭环鲁棒性上获得显著增益。

### 与基线工作的关系

RAP并非重新发明端到端规划架构，而是在现有规划器之上叠加数据增强与特征对齐能力。论文中RAP-DINO基于冻结的DINOv3-H骨干+MLP投影+迭代可变形注意力解码器（借鉴自**iPad** (Guo et al., arXiv 2025)的架构），RAP-ResNet则使用轻量ResNet34骨干。这意味着RAP的方法贡献集中在**训练范式与数据策略**层面，而非模型架构创新。

在NAVSIM v1上，RAP-DINO以93.8 PDMS超越此前最佳的**Centaur** (Sima et al., arXiv 2025)的92.1，领先+1.7。在更考验闭环鲁棒性的NAVSIM v2上，RAP-DINO取得36.93两阶段EPDMS，远超**LTF** (Chitta et al., 2023)的23.12，领先+13.81——这一巨大差距直接验证了恢复性扰动对闭环泛化的关键作用。在WOD-E2E挑战赛上，RAP-DINO以ADE@5s 2.65和RFS (Overall) 8.04略优于**Poutine** (Rowe et al., arXiv 2025)和**ViT-Adapter-GRU**。在Bench2Drive闭环测试中，RAP-ResNet以66.42 Driving Score和37.27% Success Rate超越**iPad** (Guo et al., arXiv 2025)的65.02和35.91%。

值得注意的对比是：**Centaur**采用测试时训练策略提升鲁棒性，**iPad**通过迭代建议中心化改进轨迹质量，**DiffusionDrive** (Liao et al., CVPR 2025)使用截断扩散模型生成多模态轨迹，**Hydra-MDP** (Li et al., 2024)探索多模态端到端规划，**UniAD** (Hu et al., CVPR 2023)和**VAD** (Jiang et al., ICCV 2023)分别以规划导向和向量化场景表示构建端到端系统。这些方法均依赖真实图像训练，RAP则开辟了“合成增强+特征对齐”的互补路径——该方法路径与上述工作并非替代关系，理论上可叠加于任何端到端规划架构之上。

### 适用边界与局限

**标注依赖性**。3D光栅化需要高质量的场景标注基元（车道线多段线、3D目标检测框），在标注稀疏或存在噪声的实际场景中，光栅化视图的质量将直接受损。论文附录通过定性分析（Figure 7）说明模型仍能从真实图像学习未标注的视觉线索（如“Keep Left”标志、LED动态箭头），但这依赖于真实-光栅配对训练——在完全无真实图像的纯合成训练下，这些未标注线索将彻底丢失，效果未知。

**视觉线索的舍弃**。3D光栅化主动丢弃纹理和光照信息，虽然实验证明这对规划任务影响有限，但在某些需要细粒度视觉理解的场景（如识别临时交通标志、施工人员手势、路面异常）中可能构成瓶颈。当前验证局限于nuPlan、WOD和Bench2Drive三个仿真/日志基准，尚未在实际路测中验证。

**训练复杂度**。R2R对齐模块需要配对的真实-光栅数据，全局对齐依赖对抗训练（梯度反转层），可能引入训练不稳定性。论文使用平滑退火策略（$\lambda(p) = 0.1 * ( \frac{2}{1 + \exp(-\gamma p)} - 1 )$）缓解此问题，但并未完全消除对抗训练的固有脆弱性。

**跨代理视角采样的效率**。当前跨代理视角合成使用随机采样策略，尚未探索基于难度或信息量的智能视角选择。虽然实验显示合成样本数与MinADE呈高度对数相关（$y = -0.021 \ln(x) + 1.2173$，$R^2 = 0.9942$），表明持续增益可期，但更高效的采样策略可能进一步提升数据利用效率。

### 开放问题

1. **从数据增强到闭环模拟器**。当前3D光栅化用于生成静态场景的合成视图，能否将其扩展为完整的闭环模拟器，支持强化学习微调或在线策略训练？这需要解决光栅化场景中的动态交互建模问题。

2. **减少对配对数据的依赖**。R2R对齐需要真实-光栅配对样本，能否利用自监督或半监督学习进一步增强对齐，降低对配对数据的依赖？例如，利用时间一致性或跨视角一致性作为弱监督信号。

3. **智能视角选择**。如何设计更高效的跨代理视角选择策略？基于交互密度、不确定性采样或难度估计的智能采样可能比随机采样更高效地利用日志数据。

4. **复杂场景的表示充分性**。在更复杂的动态场景（如行人密集区、非常规道路、恶劣天气）中，简化的几何基元（多段线+有向立方体）是否仍能提供足够丰富的表示？可能需要引入额外的语义基元（如行人姿态骨架、临时障碍物轮廓）来扩展表示能力。

5. **因果混淆的缓解**。RAP仍基于模仿学习范式，继承其因果混淆问题（如对自车历史轨迹的过度依赖）。恢复性扰动在一定程度上缓解了协变量漂移，但并未从根本上解决模仿学习中的分布外泛化问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/RAP_3D_Rasterization_Augmented_End_to_End_Planning.pdf]]

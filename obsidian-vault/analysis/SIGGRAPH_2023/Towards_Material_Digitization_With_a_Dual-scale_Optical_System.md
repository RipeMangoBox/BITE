---
title: Towards Material Digitization With a Dual-scale Optical System
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Towards_Material_Digitization_With_a_Dual_scale_Optical_System.pdf
project_link: null
code_link: null
aliases:
- DSOAPDSENMP
- TMDDSOS
tags:
- SIGGRAPH_2023
- topic/graphics_rendering_materials
core_operator: 构建双尺度光学采集系统（微观＋介观），结合偏振定向光源与可微渲染优化SVBSDF参数（各向异性、透射率），并通过神经网络将微观参数传播至介观尺度。
primary_logic: 在高分辨率微观尺度上借助偏振与可微渲染精确估计SVBSDF参数，再通过图像到图像的网络传播将精细属性映射到大尺寸介观样本，从而在保持微观精度的前提下实现实用的大面积材料数字化。
claims:
- 微观相机达到14020 PPI的光学分辨率，可分辨纤维级别的细节。
- 利用偏振分离漫反射与镜面反射，显著改善SVBSDF估计。
- 三步可微优化（逐步引入specular、diffuse、法线与切线）比单次优化明显降低伪影，提高SSIM。
- 完整的SVBSDF模型（含各向异性、specular tint、可变IOR）在验证视图的SSIM对比中始终误差最小。
---

# Towards Material Digitization With a Dual-scale Optical System

> [!tip] 核心洞察
> 在高分辨率微观尺度上借助偏振与可微渲染精确估计SVBSDF参数，再通过图像到图像的网络传播将精细属性映射到大尺寸介观样本，从而在保持微观精度的前提下实现实用的大面积材料数字化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向材料数字化的双尺度光学系统 |
| 英文题名 | Towards Material Digitization With a Dual-scale Optical System |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://www.elenagarces.es/projects/SEDDIDome/web/index.html) |
| Topic | #topic/graphics_rendering_materials |
| Method | Dual-scale Optical Acquisition with Polarized Differentiable SVBSDF Estimation and Neural Mesoscale Propagation |
| Dataset | 验证视图集（定向光、Stretch、Bias、Specular/Sheen场景）, 介观地图对比（由Rodriguez-Pardo and Garces [2021]提出） |

> [!tip] 效果简介
> - 验证视图集（定向光、Stretch、Bias、Specular/Sheen场景） 上，SSIM 完整模型（含各向异性、Specular Tint、可变IOR） vs 消融变体（去除各向异性、去除Specular Tint、限制IOR） (完整模型在多种材质上取得最小SSIM误差（定性及定量报告）)。
> - 介观地图对比（由Rodriguez-Pardo and Garces [2021]提出） 上，视觉质量（法线、切线图） 本文提出的带独立解码器与残差连接的传播网络 vs Rodriguez-Pardo and Garces 2021 方法 (本文方法产生更清晰、结构化更好的法线和切线图)。
> - 微观光学分辨能力 上，PPI / 像素尺寸 14020 PPI（微观相机） vs 现有便携系统一般在数百PPI (可分辨纤维级别细节（3–20 µm）)。

## 概要

现有材料数字化设备普遍受限于单一成像尺度，难以同时捕捉微观结构细节与宏观外观属性，且缺乏对透射、各向异性等关键SVBSDF参数的有效估计。本文提出一种双尺度光学采集系统，同步获取微观（14020 PPI）与介观（490–1036 PPI）图像，并利用偏振定向光源分离漫反射与镜面反射分量。在微观尺度，通过三步可微渲染优化（依次拟合镜面反射、漫反射颜色、法线与切线）精确估计包含各向异性、镜面色调与可变折射率的空间变化SVBSDF参数；随后，以独立解码器神经网络将微观参数传播至大尺寸介观样本。实验表明，完整SVBSDF模型在多种复杂材质上取得最小SSIM误差，偏振分离与多步优化显著减少伪影，神经网络传播优于直接插值方法。该系统为面向真实材质数字化的大面积、高精度外观重建提供了实用方案。

## 核心方法与创新机理

### 问题瓶颈与系统设计逻辑

现有材料外观数字化设备普遍受限于**单一空间尺度**——要么在微观分辨率下捕获精细结构但视野极小，要么在介观尺度下覆盖大面积样本却丢失纤维级细节。更关键的是，复杂材质（如织物、天鹅绒、缎面）的外观由各向异性反射、透射、表面法线/切线方向等多维属性共同决定，而现有系统缺乏对这些属性的**联合估计能力**。本文识别出的核心瓶颈在于：如何在保持微观测量精度的前提下，将空间变化双向散射表面反射分布函数（SVBSDF）参数有效传播到大尺寸样本，同时利用偏振信息解耦漫反射与镜面反射分量。

针对这一瓶颈，作者构建了一套**双尺度光学采集系统**，其设计逻辑遵循“微观精确估计→神经网络空间传播→介观完整材质模型”的因果链条。系统的物理基础是一个内径约40cm的半球形光穹（Light Dome），内部集成127个准直偏振定向LED光源、一台高分辨率微观相机（14020 PPI，视场8.9×6.7mm）和两台介观相机（分别达到490 PPI和1036 PPI）。微观相机通过电控液体透镜实现无机械移动部件的自动对焦，最小工作距离的缩短使得系统整体尺寸可控。

### 核心创新机制：偏振辅助的SVBSDF解耦与三步可微优化

本文的核心创新机理体现在**微观尺度的SVBSDF参数估计策略**上，该策略通过三个关键changed slots实现了对基线方法的突破：

**Changed Slot 1：照明与采集的偏振控制。** 基线方法使用非偏振或简单定向光，难以分离漫反射与镜面反射分量。本文在微观相机端配备动态调谐偏振滤光片，通过旋转偏振角度获取P0（平行偏振）和P90（交叉偏振）图像对。核心操作是将P90与P0图像相减，得到主要直接反射分量（predominantly direct reflection），从而为后续各向异性镜面反射拟合提供干净的输入信号。Figure 5的实验证据表明，偏振分离能显著区分不同材质的反射行为——例如绿色缎面在交叉偏振下镜面高光被有效抑制，而亚麻材质的漫反射主导特性在不同偏振态下变化较小。

**Changed Slot 2：SVBSDF模型的完整参数化。** 本文采用的各向异性反射模型包含16个空间变化参数：基色/漫反射反照率 $\mathbf{b} \in \mathbb{R}^3$、粗糙度 $roughness \in \mathbb{R}$、折射率 $ior \in \mathbb{R}$、各向异性度 $\alpha \in \mathbb{R}$、镜面色调 $\rho_s \in \mathbb{R}$、法线 $\mathbf{n} \in \mathbb{R}^3$ 和切线 $\mathbf{t}_q \in \mathbb{R}^3$。相比Disney 2015 BRDF模型（Burley, 2015），本文增加了显式的各向异性切线场和镜面色调参数，使模型能够表达缎面等材质的定向拉丝高光和色彩偏移效应。透射部分采用单一漫透射瓣 $\mathbf{t} \in \mathbb{R}^3$，受底层几何角度调制。

**Changed Slot 3：三步逐次可微优化策略。** 这是本文最关键的方法创新。基线方法（单次可微渲染直接拟合所有参数）容易陷入局部极小值，产生暗/亮伪影和错误的基色估计。本文提出将优化过程分解为三个因果关联的步骤：

- **Step 1（镜面反射估计）**：仅优化镜面反射相关参数（粗糙度、IOR、各向异性度、镜面色调），使用偏振分离后的直接反射分量作为目标。此时漫反射瓣固定为初始值，避免漫反射分量“吸收”镜面反射的误差。

- **Step 2（漫反射颜色引入）**：在镜面反射参数收敛后，将漫反射基色 $\mathbf{b}$ 加入优化变量。此时镜面反射已基本正确，漫反射可以专注于解释剩余的能量分布。

- **Step 3（法线与切线精化）**：利用前两步得到的稳定反射参数，进一步优化法线 $\mathbf{n}$ 和切线 $\mathbf{t}_q$。此时梯度信号更加清晰，能产生结构化的切线场。

三步优化共享统一的损失函数，由三个加权项组成：

$$\mathcal{L} = k_1 \mathcal{L}_{\mathrm{rec}} + k_2 \mathcal{L}_{\mathrm{ortho}} + k_3 \mathcal{L}_{\mathrm{ior}}$$

其中重建损失 $\mathcal{L}_{\mathrm{rec}}$ 在拟合光集合 $Q_F$ 上计算捕获图像 $i_k$ 与渲染图像 $r_k$ 之间的平滑L1损失：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{|Q_F|} \sum_{k \in Q_F} \hat{\ell}_1(i_k, r_k)$$

正交惩罚损失 $\mathcal{L}_{\mathrm{ortho}}$ 针对虚拟正交视图 $Q_M$（半球顶部未放置LED的方向），防止渲染器在无观测区域产生过亮伪影：

$$\mathcal{L}_{\mathrm{ortho}} = \frac{1}{|Q_M|} \sum_{k \in Q_M} \max(0, r_k - \bar{i}), \quad \bar{i} = \max_{1 \leqslant k \leqslant |Q_F|} i_k$$

IOR损失 $\mathcal{L}_{\mathrm{ior}}$ 为折射率设置柔性上界 $\mathrm{I\bar{0}R}$，鼓励物理合理值：

$$\mathcal{L}_{\mathrm{ior}} = \left( \frac{\max(0, \mathrm{IOR} - \mathrm{I\bar{0}R})}{4 - \mathrm{I\bar{0}R}} \right)$$

权重设置为 $k_1=35.0$、$k_2=1.0$、$k_3=0.01$。Figure 8的消融实验证实，三步优化相比单次优化在验证视图上显著降低了SSIM误差，并消除了基色图中的暗斑和亮斑伪影。

### 透射与不透明度估计

对于半透明材质，本文利用光穹底部的背光LED阵列和偏振控制来计算两个关键参数图。不透明度图 $\tau$ 由三个二值掩膜的交集构建：$\tau = B_b \cap B_{\mathrm{IOR}} \cap B_n$，分别对应基色、折射率和法线的有效区域。透射图 $\mathbf{t}$ 通过取四个透射图像（使用漫反射偏振模式P0）的最小值获得：$\mathbf{t} = \min(\{i_k^{P0}\}_{k \in Q_T})$。Figure 9展示了基色、不透明度和透射图的可视化结果，其中透射图能清晰表现织物经纬线交叉处的光线穿透差异。

### 神经网络介观传播

微观估计得到的SVBSDF参数仅覆盖约9×7mm的区域，需要传播到11×11cm的介观尺度。本文采用**每材质单独训练**的图像到图像翻译网络，这是另一个关键的changed slot：基线方法（Rodriguez-Pardo and Garces, 2021）使用直接插值或通用网络，难以恢复精细的法线和切线结构。

网络架构包含独立解码器、残差连接和Group Normalization，输入为介观相机捕获的多光照图像，输出为对应的SVBSDF参数图。训练目标以微观估计结果作为ground truth，并添加多通道感知损失以保持纹理结构。Figure 10的对比表明，本文方法产生的法线图和切线图具有更清晰的纤维走向和更少的模糊伪影，而Rodriguez-Pardo and Garces方法在复杂编织结构上会出现方向混乱。

### 模块间因果关系总结

整个pipeline的因果链条为：**偏振图像采集→漫反射/镜面反射分离→三步可微反射拟合→透射图计算→神经网络空间传播**。微观模块的输出（精确的SVBSDF参数）直接作为介观传播网络的监督信号，而偏振分离的质量决定了后续优化的收敛稳定性。三步优化中，Step 1的镜面反射估计为Step 2的漫反射颜色引入提供了无偏的镜面分量，Step 3的法线/切线精化又依赖于前两步的稳定反射参数。这种层级依赖关系是本文方法优于单次优化的根本原因。

![[assets/figures/papers/paper_list_l7_https_www_elenagarces_es_projects_SEDDIDome_web_index_html/figures/006_Figure_6.jpg]]
*Figure 6: Left, 2D projections of the directional lights and cameras of the dome. Right, an overview of the parameter estimation pipeline. Our method estimates the SVBSDF at two scales. At the microscale, we fit the parameters of the anisotropic reflectance lobe using directional lighting. The transmittance and opacity maps are computed next using backlighting and some reflectance maps. Once the micro SVBSDF is estimated, we propagate these values to the mesoscale using a neural network trained with data captured with the optical device*

## 实验与关键发现

### 主实验结果

**微观光学分辨率验证**：微观相机在 8.9 × 6.7 mm 视场内达到 14020 PPI 的光学分辨率，可分辨 3–20 µm 的纤维级别细节。作为参照，介观极向相机和中距离相机分别达到 490 PPI 和 1036 PPI，现有便携式材料采集系统通常仅数百 PPI。这一分辨能力是后续SVBSDF参数精确估计的硬件基础。

**偏振分离对反射估计的贡献**：实验表明，通过旋转微观相机端的偏振滤光片，可在特定角度（P90与P0）有效分离直接镜面反射与漫反射分量。Figure 5 展示了偏振角扫描下的平均强度曲线，以及缎面和亚麻在两种偏振模式下的捕获差异——这一分离为后续三步优化提供了更干净的镜面反射初始化。

**三步优化 vs. 单次优化**：Figure 8 报告了验证视图上的SSIM误差对比。三步逐次优化（先specular、再diffuse、最后法线/切线）相比单次直接拟合，显著减少了暗/亮伪影，提升了Albedo图质量。在三种材质上的可视化对比中，三步优化产出的基础色图更均匀、无异常暗斑。

**完整SVBSDF模型的消融对比**：Figure 11 展示了SVBSDF各组件对再现真实样本的贡献。完整模型（含各向异性、Specular Tint、可变IOR）在多种材质（缎面、天鹅绒、提花织物等）的验证视图上取得最小SSIM误差。定性比较中，完整模型的渲染结果与实拍照片在定向光、Stretch、Bias、Specular/Sheen四种验证场景下最为接近。

**介观传播网络对比**：Figure 10 将本文提出的传播网络与 Rodriguez-Pardo and Garces (2021) 的方法进行对比。本文网络采用独立解码器、残差连接与Group Normalization，并加入多通道感知损失，产出的法线图和切线图结构更清晰，能更好地保留微观尺度估计的精细方向信息。

### 关键消融发现

| 消融项 | 影响 | 典型失效材质 |
|--------|------|-------------|
| 去除各向异性 | SSIM误差显著增加 | 缎面等编织类材料 |
| 去除Specular Tint | 带彩镜面反射精度下降 | 缎面、天鹅绒 |
| 限制IOR ≤ 1.78 | 高镜面反射材质表达能力削弱 | 高光泽织物 |
| 单次优化替代三步 | 暗/亮伪影增多，Albedo质量下降 | 多种材质 |

各向异性项对编织类材料尤为关键：缎面的镜面反射方向性极强，去除各向异性后渲染结果失去方向性高光特征。Specular Tint则对带色彩偏移的镜面反射材质（如染色缎面、深色天鹅绒）不可缺失。IOR上界限制削弱了高镜面反射材质的物理准确性。

### 物理验证场景

Figure 12 展示了四种验证场景设计：
- **定向光场景**：评估镜面反射和各向异性的准确性
- **Stretch场景**：测试法线图在变形下的表现
- **Bias场景**：验证切线方向对反射的影响
- **Specular/Sheen场景**：检验掠射角下的外观再现

![[assets/figures/papers/paper_list_l7_https_www_elenagarces_es_projects_SEDDIDome_web_index_html/figures/012_Figure_12.jpg]]
*Figure 12: Setups used for qualitative testing. Each scene showcases a different appearance property*

Figure 13 进一步验证了位移贴图和透射渲染的效果：带位移的漫反射织物渲染比无位移版本更接近实拍；使用完整透射模型（而非简单alpha近似）的织物渲染也更准确地再现了背光透过效果。

### 失败模式与适用边界

1. **金属与定向镜面透射不支持**：当前SVBSDF模型不包含金属材质和定向镜面透射项，无法处理金属光泽织物或高透明材料的镜面透射效果。

2. **掠射角效应缺失**：可微渲染优化仅使用正交视点，未考虑掠射角的视线依赖效应（如Sheen、纱线间互遮挡），在极端掠射光照下的渲染可能与实拍存在偏差。

3. **微观3D形貌未重建**：系统未重建微观表面几何，无法生成掠射光照射下纱线突起产生的投射阴影，位移贴图仅作为近似补偿。

4. **色彩偏差**：相机传感器光谱灵敏度差异导致渲染与实拍之间存在轻微色彩偏差，尤其在饱和色材质上更为明显。

5. **介观传播的泛化限制**：传播网络需为每种材质单独训练，泛化到全新材质需重新采集微观数据并训练，无法零样本迁移。

6. **介观颜色地图的覆盖不足**：某些复杂材质的微观捕获区域可能未覆盖所有颜色变异，导致介观颜色地图在部分区域欠完整。

### 微观结构信息的附加验证

Figure 14 展示了基于图像的飞丝检测和纤维捻度估计结果。这些微观结构信息可进一步应用于设计特定织物着色模型（如Figure 15所示），将捻度作为控制镜面反射瓣粗糙度和方向的实时着色器参数，验证了微观尺度信息向实际渲染管线传递的可行性。

Figure 16 展示了多种材质在实拍与渲染下的对比画廊，覆盖了从漫反射织物到高光泽缎面的广泛材质类型，为系统的整体数字化质量提供了定性证据。

### 实验证据强度评估

需注意，主实验结果以定性比较为主，缺乏与最先进单尺度方法的定量数值对比（如PSNR、LPIPS等指标的系统报告）。介观传播网络的对比也仅限于视觉质量判断，未提供像素级误差度量。消融实验虽系统覆盖了SVBSDF各组件，但仅在Figure 11中以定性方式呈现，定量SSIM差异的具体数值未明确列出。此外，所有验证均在自建设备采集的数据上进行，外部泛化性未经独立验证。

![[assets/figures/papers/paper_list_l7_https_www_elenagarces_es_projects_SEDDIDome_web_index_html/figures/010_Figure_10.jpg]]
*Figure 10: Comparison with the method of Rodriguez-Pardo and Garces [2021] for mesoscale maps propagation. The first row (a) showcases an example where multiple captures at the microscale were needed to cover the spatiallyvarying albedo of the material. (b) and (c) required a single capture, we show the result of normals and tangents maps compared with previous work*

![[assets/figures/papers/paper_list_l7_https_www_elenagarces_es_projects_SEDDIDome_web_index_html/figures/005_Figure_5.jpg]]
*Figure 5: (a) Influence of polarization in reflectance: Average intensity of the captured image (y-axis) varying the angle of polarization of the micro camera (x-axis). The insets are captured images at those peak angles. (b) A green satin (top) and a linen (bottom) captured with different polarization modes*

![[assets/figures/papers/paper_list_l7_https_www_elenagarces_es_projects_SEDDIDome_web_index_html/figures/008_Figure_8.jpg]]
*Figure 8: On the left, we show SSIM errors on the validation views comparing direct (single-pass) and three-step (multi-pass) optimization approaches. Right: optimized base color (albedo) for three materials. Top Row: The multipass fit reduces dark and bright artifacts at the extreme of horizontal yarns. Middle row: The velvet albedo in a single pass accumulates a specular component, lowering the SSIM in multiple views. Bottom row: Leather does not have high transmissive-reflectance effects, and thus the ior treatment is not as relevant. However, the normals are better estimated, reducing artifacts in albedo*

![[assets/figures/papers/paper_list_l7_https_www_elenagarces_es_projects_SEDDIDome_web_index_html/figures/011_Figure_11.jpg]]
*Figure 11: Ablation study of the different components of the SVBSDF and its contribution to reproducing the real sample. On the left, we show SSIM errors on the validation views comparing several variations of our full model. These variations include removing anisotropy and specular tint, and clamping the IOR to the most commonly used range for dielectric textiles, that is 1.78. On the right, we showcase some examples. Fabrics (a) and (d) have colored specular; hence, they benefit from the specular tint term. Fabric (b) is highly anisotropic, so removing that piece introduces a penalty in error. Fabrics like (c) and the leather (f ) can be reproduced with a simple isotropic model with an IOR within th...*

## 定位与知识库关联

本文在材料数字化这一方向上，相对已有工作做出的核心改变可以归纳为 **“采集尺度”与“参数传播方式”两个关键 slot 的替换**。已有材料外观捕获系统——无论是以 **Disney 2015 BRDF模型**（Burley, 2015）为代表的宏观手持扫描方案，还是基于显微成像的微观材料分析设备——均受限于单一空间尺度：要么在厘米级视场下获得宏观 BRDF，但丢失纤维级微观结构导致的各向异性与透射细节；要么在微米级分辨率下精确刻画局部反射，却无法将参数扩展到实用的大面积材质。本文通过构建一套**双尺度同步光学系统**，将微观（FOV 8.9 × 6.7 mm, 14020 PPI）与介观（最大 11 × 11 cm, 490–1036 PPI）两个尺度的采集整合在同一半球光穹中，从而填补了“微观精度”与“介观覆盖”之间的鸿沟。

在 **SVBSDF 参数传播**这一 slot 上，本文明确对比了 **Rodriguez-Pardo and Garces (2021)** 的方法。该方法同样尝试将微观尺度估计的材质参数传播到大面积介观样本，但其核心机制依赖直接插值或较浅的网络结构，容易在法线、切线等高频结构地图上产生模糊和伪影。本文的替换方案是：为每种材质单独训练一个**带独立解码器、残差连接与 Group Normalization 的传播网络**，并引入多通道感知损失。这一设计使得网络能够从介观 RGB 图像中更准确地恢复微观 SVBSDF 参数的空间分布，尤其在编织纹理的方向性结构（切线场）和表面起伏（法线图）上，产生了比 Rodriguez-Pardo and Garces (2021) 更清晰、结构化更好的结果（Figure 10）。这一改进的本质是：将传播问题从“图像到参数的回归”重新定义为“结构保持的特征迁移”，其中独立解码器为每个参数图提供专门的解码路径，残差连接则保留了微观尺度与介观尺度之间的高频对应关系。

从**知识库挂载点**来看，本文的工作可以定位在以下几条技术脉络的交汇处：

1. **偏振辅助材质采集**：利用偏振分离漫反射与镜面反射在计算机图形学中已有较长历史，但本文将其与可微渲染优化深度耦合——相机端动态调谐偏振滤光片，在 P90 与 P0 两个正交偏振态下采集，从而为后续 SVBSDF 拟合提供干净的镜面反射先验。这一设计将偏振从“后处理分离工具”提升为“采集-优化联合系统中的前端物理约束”。

2. **可微渲染驱动的 SVBRDF/SVBSDF 估计**：近年来基于可微渲染的材质估计方法多采用单次优化直接拟合所有参数。本文的**三步逐次优化策略**（先 specular，再 diffuse，最后法线/切线）表明，将强非线性优化分解为物理意义明确的子问题，配合 $\mathcal{L}_{\text{rec}}$、$\mathcal{L}_{\text{ortho}}$、$\mathcal{L}_{\text{ior}}$ 三项损失，能显著降低局部极小值导致的暗/亮伪影（Figure 8）。这为可微渲染优化在高度欠约束的 SVBSDF 估计场景中提供了一种有效的退火式策略。

3. **神经材质超分辨率与传播**：将微观材质参数“超分辨”到宏观尺度的工作近年来多采用基于学习的图像翻译框架。本文的贡献在于指出：对于各向异性材质，单一编码器-解码器结构不足以同时处理颜色、法线、切线、粗糙度等异质参数图；独立解码器与 Group Normalization 的组合能更好地保持各参数通道的统计特性。

**适用边界**需要明确。本文的 SVBSDF 模型**不支持金属材质和定向镜面透射**——这是一个重要的限制，意味着对于金属丝织物、带金属涂层的装饰材料、或高度透明的薄纱类材质，当前系统无法给出准确的数字化结果。此外，可微渲染优化仅使用正交视点，未考虑掠射角下的视线依赖效应（如 Sheen、纱线间互遮挡），因此在极端掠射光照条件下的渲染质量可能下降。介观传播网络需要为每种材质单独训练，泛化到全新材质类型需要重新采集微观数据并重新训练网络，这限制了系统的“即拍即用”能力。相机传感器光谱灵敏度差异导致的色彩偏差也需要通过额外的色彩校准步骤来缓解。

**后续研究启发**可从以下几个方向展开：

- **模型扩展**：将空间变化的金属度参数融入优化过程，同时保持鲁棒性，是向更通用材质模型迈进的关键一步。定向镜面透射的加入则需要额外的采集配置（如背光方向的可变性）和更复杂的透射模型。
- **视角依赖效应**：利用系统中已有的两台极向相机（Polar Camera），通过多视角立体或光度立体方法估计视线依赖的外观变化（如纱线间互遮挡），有望在保持单次采集效率的前提下提升掠射角渲染质量。
- **跨设备泛化**：当前介观传播网络与特定光学系统强绑定。探索领域自适应或无监督域迁移方法，使得在一个设备上训练的传播网络能迁移到其他消费级相机拍摄的介观图像上，将大幅提升该技术的实用范围。
- **微观几何重建**：当前方法仅估计法线图作为几何代理，未重建真实的微观 3D 形貌。若能结合结构光或光度立体技术恢复微面高度场，则可在渲染时产生投射阴影和互反射效果，进一步提升真实感。

总体而言，本文在“采集尺度”和“参数传播”两个 slot 上的替换，使得高精度材料数字化从实验室微观分析走向实用的大面积材质捕获成为可能。其在偏振-可微渲染-神经网络三者之间的系统级整合，为后续面向复杂外观（金属、透明、多层）的材料数字化系统提供了清晰的架构参考。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Towards_Material_Digitization_With_a_Dual_scale_Optical_System.pdf]]
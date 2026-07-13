---
title: "MetaSpectra+: A Compact Broadband Metasurface Camera for Snapshot Hyperspectral+ Imaging"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MetaSpectra_A_Compact_Broadband_Metasurface_Camera_for_Snapshot_Hyperspectral_Imaging.pdf
project_link: "https://meta-imaging.qiguo.org"
code_link: null
aliases:
- MCBMCSHI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过分离折射透镜（成像）与超构表面（分束与色散控制）的功能，并采用双层超构表面设计（第一层分束偏转，第二层补偿/控制各通道色散），实现对各通道色散的独立调控，从而在保持紧凑性的同时扩展操作带宽至250 nm。
primary_logic: 将折射光学与超构表面解耦，利用折射透镜实现低F数成像，利用双层超构表面独立编码各通道的色散、曝光与偏振，克服了单超构表面多功能成像的窄带瓶颈。
claims:
- 双层超构表面组装：第一层分束偏转，第二层部分或完全补偿偏转以引入可控色散或消除色散。
- 通过联合设计α_i和β_i，可精确调谐甚至消除点扩散函数的色散位移。
- MetaSpectra+原型实现了450–700 nm宽带操作，并在KAUST数据集上取得最高重建精度。
- 真实场景HDR+高光谱成像中，动态范围提升11 dB。
---

# MetaSpectra+: A Compact Broadband Metasurface Camera for Snapshot Hyperspectral+ Imaging

> [!tip] 核心洞察
> 将折射光学与超构表面解耦，利用折射透镜实现低F数成像，利用双层超构表面独立编码各通道的色散、曝光与偏振，克服了单超构表面多功能成像的窄带瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | MetaSpectra+：一种用于快照高光谱+成像的紧凑宽带超构表面相机 |
| 英文题名 | MetaSpectra+: A Compact Broadband Metasurface Camera for Snapshot Hyperspectral+ Imaging |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.09116) · [Project](https://meta-imaging.qiguo.org) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MetaSpectra+ |
| Dataset | KAUST dataset, Real-world HDR+Hyperspectral scenes |

> [!tip] 效果简介
> - KAUST dataset 上，PSNR (dB)↑ / SSIM↑ / SAM↓ MetaSpectra+ (DWDN) 32.92 / 0.94 / 0.17; MetaSpectra+ (DDPM) 33.31 / 0.92 / 0.23 vs 2-in-1 Cam 31.14 / 0.86 / 0.24; Array-HSI 27.44 / 0.89 / 0.20; others see Table... (Best PSNR improvement +2.17 dB over 2-in-1 Cam)。
> - Real-world HDR+Hyperspectral scenes 上，Dynamic range increase MetaSpectra+ HDR fusion achieves 11 dB increase over LDR vs Native CMOS low-dynamic range images (+11 dB)。

## 概要

**问题瓶颈**：现有多功能超构表面成像系统受限于强色散像差，只能在单波长或窄带（10–100 nm）工作，难以同时实现宽带高光谱成像与其他模态（如HDR、偏振）的获取。

**核心思路**：**MetaSpectra+** 将折射透镜（成像）与超构表面（分束与色散控制）功能解耦，采用双层超构表面设计——第一层分束偏转，第二层补偿/控制各通道色散。通过联合设计偏转参数 $\boldsymbol{\alpha}_i$ 与补偿参数 $\boldsymbol{\beta}_i$，可精确调谐甚至消除各通道点扩散函数的色散位移（当 $\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i = 0$ 时实现消色散），从而在保持紧凑性的同时将操作带宽扩展至 250 nm（450–700 nm），覆盖几乎整个可见光波段。

**方法定位**：MetaSpectra+ 属于快照式高光谱+成像系统，其光学前端由物镜、分束超构表面 $M_0$（随机交织多路偏转）、色散控制超构表面 $M_{1:4}$、目镜透镜及可选滤光片（ND/偏振）组成，在共享传感器上同时形成四路子图像；计算后端采用 DWDN 或 DDPM 网络从子图像重建高光谱数据立方体，并可融合多曝光通道实现 HDR 或计算偏振度。

**关键结果**：
- 在 KAUST 数据集上，MetaSpectra+ 取得最高重建精度（DWDN: PSNR 32.92 dB, SSIM 0.94; DDPM: PSNR 33.31 dB），较此前最优方法 **2-in-1 Cam**（SIGGRAPH 2024）提升 +2.17 dB。
- 真实场景 HDR+高光谱成像中，动态范围提升 11 dB。
- 系统总轨迹长度（TTL）为对比方法中最短，F 数低至 f/6~12，兼具紧凑性与高光通量。

**局限与待验证点**：随机交织抑制高阶衍射伪影的同时降低了衍射效率，当前原型帧率上限约 10 FPS，高速视频应用受限；更高折射率材料（如 GaN、TiO₂）的引入能否在成本可控的前提下解决光效问题，仍需进一步验证。

高光谱成像（Hyperspectral Imaging, HSI）旨在捕获场景在每个像素上的完整光谱响应，为材质识别、遥感、生物医学诊断等任务提供超越传统RGB图像的丰富信息。然而，传统高光谱成像系统通常依赖空间或光谱扫描机制，导致采集时间长、体积庞大，难以适应动态场景和便携式应用。近年来，快照式高光谱成像（Snapshot HSI）成为研究热点，其目标是在单次曝光中同时获取空间与光谱信息，从而消除时间扫描的瓶颈。

在这一方向上，超构表面（Metasurface）因其对光场的亚波长调控能力而备受关注。超构表面由亚波长尺度的纳米结构阵列构成，能够在极薄的光学元件上实现对相位、振幅、偏振和色散的灵活编码。已有工作尝试利用单一超构表面同时完成成像与分束功能，以实现紧凑的多功能成像系统。然而，这种“单超构表面多功能”范式面临一个根本性的瓶颈：**强色散像差**。由于成像与分束功能耦合在同一元件中，超构表面固有的波长依赖性导致不同光谱通道之间产生难以补偿的空间偏移和模糊，迫使系统只能在单波长或窄带（10–100 nm）条件下工作，无法同时实现宽带高光谱成像与其他模态（如高动态范围HDR、偏振）的获取。

这一窄带瓶颈的因果机制可归结为：单一超构表面必须同时承担“将入射光聚焦成像”和“将光束分束到不同通道”两个任务。前者要求对宽带光实现消色差聚焦，后者则要求对不同通道施加差异化的偏转角。当这两种需求叠加在同一相位轮廓上时，各通道的色散位移相互耦合且难以独立控制，导致宽带下图像质量急剧退化。因此，现有基于超构表面的多功能成像系统（如 **2-in-1 Cam** (SIGGRAPH 2024)、**Array-HSI** (SIGGRAPH Asia 2024)、**SCCD** (Optica 2021 / ICCV 2021) 等）虽然在紧凑性上具有优势，但其操作带宽和成像质量受到根本性制约。

MetaSpectra+ 的核心动机正是打破这一耦合。其关键洞察在于：**将折射光学与超构表面解耦**——让折射透镜负责低F数、高质量的成像，而让超构表面专注于分束与各通道色散的独立编码。通过引入双层超构表面设计（第一层分束偏转，第二层补偿/控制各通道色散），系统能够对各通道的色散位移进行精确调谐甚至完全消除，从而在保持紧凑形态的同时，将操作带宽扩展至250 nm（450–700 nm），几乎覆盖整个可见光波段。这一解耦策略不仅解决了宽带高光谱成像的瓶颈，还为实现HDR和偏振等多模态快照成像开辟了空间。

此外，该系统采用随机交织（Random Interleaving）策略构建分束超构表面，以抑制规则交织方案中因大偏转角引起的高阶衍射伪影，进一步保障了多通道子图像的质量。在重建端，MetaSpectra+ 结合深度展开网络（DWDN）和去噪扩散概率模型（DDPM）两种后处理架构，从捕获的子图像中恢复高光谱数据立方体，并可选的融合HDR或计算偏振信息。

综上所述，MetaSpectra+ 的提出旨在回答一个核心问题：**能否在保持紧凑性的前提下，实现宽带、多功能的快照高光谱成像？** 其通过光学功能解耦与双层超构表面协同设计，为这一问题提供了肯定的答案。

## 核心方法与创新机理

MetaSpectra+ 的核心创新在于通过**功能解耦**与**双层超构表面色散独立编码**，突破了现有多功能超构表面成像系统长期受困的窄带瓶颈。其关键创新可归纳为以下四个维度。

### 1. 成像与分束的功能解耦

现有超构表面成像系统（如 **2-in-1 Cam** (SIGGRAPH 2024)、**Array-HSI** (SIGGRAPH Asia 2024) 等）通常令单一超构表面同时承担成像与分束双重任务。这种功能耦合导致严重的色散像差，将操作带宽限制在 10–100 nm 的窄带范围内。MetaSpectra+ 的核心洞察是**将折射光学与超构表面解耦**：用折射透镜实现低 F 数（f/6~12）的成像功能，而超构表面仅负责分束与色散控制。这一解耦使系统在保持紧凑外形（总轨道长度 TTL 仅 17 mm）的同时，将操作带宽一举扩展至 **250 nm（450–700 nm）**，几乎覆盖整个可见光波段。

### 2. 双层超构表面实现各通道色散独立调控

这是系统最关键的机制创新。传统单超构表面架构无法对不同光学通道的色散进行独立控制，而 MetaSpectra+ 采用**双层超构表面组装**：

- **第一层 M₀（分束超构表面）**：将入射准直光束分为 V 个通道，并对每个通道施加不同的偏转角 $\boldsymbol{\alpha}_i$。
- **第二层 M₁:₄（色散控制超构表面）**：对每个通道施加额外的线性相位延迟 $\boldsymbol{\beta}_i$，用于补偿或控制该通道的色散位移。

通过联合设计 $\boldsymbol{\alpha}_i$ 与 $\boldsymbol{\beta}_i$，系统可以精确调谐甚至消除点扩散函数（PSF）的波长依赖空间位移。其核心控制方程（Eq. (13)）为：

$$\Delta\mathbf{x}_i(\lambda) = \frac{\lambda f}{\lambda_c}(\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i)$$

当 $\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i = 0$ 时，第 i 通道的色散被完全消除，产生消色差子图像；当保留非零和值时，则引入可控色散用于光谱编码。这一机制赋予了系统前所未有的灵活性：可以在同一快照中同时获取消色差 RGB 图像（用于结构引导）和色散编码的高光谱信息。

### 3. 随机交织分束策略

在多通道同时分束的实现上，MetaSpectra+ 采用**随机交织（random interleaving）**策略（Eq. (5)），而非传统的规则交织。规则交织在大偏转角下会产生严重的高阶衍射伪影，而随机交织通过破坏伪影的相干叠加条件，有效抑制了这些伪影。这一策略以一定程度的光效损失为代价，换取了更干净的成像质量（Figure 7 对比了两种策略的仿真波前振幅）。

### 4. 多功能成像的统一光学框架

MetaSpectra+ 将上述色散控制能力与**可选光学滤波**（ND 滤光片、偏振片）相结合，实现了在单一紧凑光学架构下的多功能成像。通过在四个通道中分别配置不同的 ND 滤光片（0.3 OD 和 0.9 OD）或正交偏振片，系统可在单次快照中同时获取：

- 高光谱数据立方体
- HDR 图像（通过 Debevec 和 Malik 方法融合多曝光子图像，动态范围提升 **11 dB**）
- 偏振信息（水平-垂直线偏振度 $\mathrm{DoLP}_{HV} = |I_3 - I_4| / |I_3 + I_4|$）

这种“高光谱+”的统一框架使 MetaSpectra+ 在功能维度上显著超越了仅聚焦于高光谱重建的基线系统。

### 创新总结

| 创新维度 | 基线方案 | MetaSpectra+ 方案 | 关键证据 |
|---------|---------|------------------|---------|
| 成像/分束耦合 | 单超构表面同时成像与分束 | 折射透镜成像 + 超构表面分束 | Introduction 解耦声明 |
| 操作带宽 | 10–100 nm | 250 nm (450–700 nm) | Abstract; Section 4.1 |
| 色散控制 | 无法独立控制各通道 | 双层超构表面，$\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i$ 联合设计 | Eq. (13) |
| F 数 | 较高 | f/6~12（低 F 数） | Introduction; Fig. 1b |
| 分束策略 | 规则交织 | 随机交织抑制高阶衍射伪影 | Section 4.1; Figure 7 |

这些创新共同构成了 MetaSpectra+ 在 KAUST 数据集上取得最高重建精度（DWDN: 32.92 dB PSNR, DDPM: 33.31 dB PSNR，超越 **2-in-1 Cam** 达 +2.17 dB）以及真实场景 HDR+ 高光谱成像中 11 dB 动态范围增益的底层技术支撑。

MetaSpectra+ 的核心设计思想是将**成像功能**与**分束/色散控制功能**解耦，从而突破传统多功能超构表面成像系统因强色散像差导致的窄带瓶颈（通常仅 10–100 nm）。系统采用“折射透镜 + 双层超构表面”的混合光学架构，在保持紧凑性的同时，将操作带宽扩展至 450–700 nm（250 nm），几乎覆盖整个可见光波段。

### Pipeline 总览

整个成像与重建流水线由**前端光学编码**和**后端计算解码**两大阶段构成，如 Figure 1 和 Figure 2 所示：

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/001_Figure_1.jpg]]
*Figure 1: Overview. (a) MetaSpectra+ employs a compact, hybrid optical assembly that integrates refractive lenses with metasurfaces (blue), forming multiple images in a single shot, each engineered with distinct dispersion, exposure, or polarization. The system reconstructs a hyperspectral datacube together with either an HDR image or two polarization channels from a snapshot capture. (b) Compared with previous multifunctional metasurface systems [7, 24, 27, 36, 43], the hybrid optical design of MetaSpectra+ supports a significantly broader operating bandwidth and a lower F-number, while being comparably compact*

1. **物镜准直**：入射光经物镜与视场光阑 $A(\mathbf{x})$ 准直为平面波前。
2. **分束超构表面 M₀**：将准直光束分为 $V$ 个（原型中 $V=4$）独立光学通道，并对每个通道施加不同的偏转角 $\boldsymbol{\alpha}_i$。M₀ 的相位轮廓通过**随机交织**（random interleaving）从 $V$ 个子轮廓中等概率采样构建，以抑制高阶衍射伪影。
3. **色散控制超构表面 M₁:₄**：每个通道对应一片独立的超构表面，施加额外的线性相位延迟 $\boldsymbol{\beta}_i$。通过联合设计 $\boldsymbol{\alpha}_i$ 与 $\boldsymbol{\beta}_i$，可精确调控各通道点扩散函数（PSF）的色散位移：
   $$
   \Delta\mathbf{x}_i(\lambda) = \frac{\lambda f}{\lambda_c}(\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i)
   $$
   当 $\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i = 0$ 时，该通道实现消色差成像；否则保留可控色散用于光谱编码。
4. **目镜聚焦**：各通道经独立目镜透镜（焦距 $f$）聚焦至共享传感器平面的不同区域，形成子图像 $I_{1:4}$。
5. **可选光学滤波**：在目镜前可插入中性密度（ND）滤光片或偏振片，调节各通道的曝光量或偏振敏感性，以支持 HDR 与偏振成像模态。
6. **传感器捕获**：共享的全局快门 RGB 或单色传感器同时记录四幅子图像，实现单次曝光快照采集。
7. **计算重建**：捕获的子图像送入图像复原网络（DWDN 或 DDPM）进行高光谱数据立方体重建；对于 HDR 模态，额外采用 Debevec & Malik 方法融合不同曝光子图像；对于偏振模态，由正交偏振通道计算线偏振度 $\mathrm{DoLP}_{HV} = |I_3 - I_4| / |I_3 + I_4|$。

### 模块关系与数据流

```
入射光 → [物镜+视场光阑] → 准直光束
       → [M₀ 分束超构表面] → V 路偏转光束 (α_i)
       → [M₁:₄ 色散控制超构表面] → 各通道色散调控 (β_i)
       → [可选滤波 F₁:₄] → 曝光/偏振调制
       → [目镜透镜组] → 聚焦至传感器
       → [传感器] → 单次捕获 4 幅子图像 I₁:₄
       → [计算重建网络] → 高光谱立方体 + (可选) HDR / 偏振图
```

该架构的关键优势在于：折射透镜承担低 F 数（f/6~12）成像任务，而双层超构表面仅负责分束与各通道独立的色散、曝光、偏振编码，二者各司其职，从而在 17 mm 总轨道长度（TTL）的紧凑空间内实现了宽带、多模态快照成像。

MetaSpectra+ 的光学系统由六个核心模块级联构成，其功能分工与物理建模如下。

### 光学管线模块

**1. 物镜与视场光阑**
入射光首先经物镜准直，并由视场光阑 $A(\mathbf{x})$ 限制视场，形成宽带准直平面波前：
$$U_0^-(\mathbf{x}, \lambda, \mathbf{n}) = \exp\left(j\frac{2\pi}{\lambda}\mathbf{n}_\perp \cdot \mathbf{x}\right)$$

**2. 分束超构表面 $M_0$**
$M_0$ 将准直光束分为 $V$ 个通道，并对每个通道施加不同的偏转角 $\boldsymbol{\alpha}_i$。其核心设计策略是**随机交织**：在中心波长 $\lambda_c$ 处，整体相位轮廓由各子通道的线性相位轮廓通过等概率多项式分布随机采样构成：
$$M_0(\mathbf{x}, \lambda_c) = M_{0,k}(\mathbf{x}, \lambda_c), \quad k \sim \text{Multinomial}(1/V)$$
其中第 $i$ 个子轮廓为 $M_{0,i}(\mathbf{x}, \lambda_c) = \exp\left(j\frac{2\pi}{\lambda_c}\boldsymbol{\alpha}_i \cdot \mathbf{x}\right)$。随机交织（而非规则交织）是抑制大偏转角下高阶衍射伪影的关键设计选择（消融实验证实，见 Figure 7）。

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/008_Figure_7.jpg]]
*Figure 7: Simulated wavefront amplitude incident on the dispersion-control metasurface when using (a,c) regular interleaving and*

**3. 色散控制超构表面 $M_{1:4}$**
第二层超构表面对每个通道施加额外的线性相位延迟 $\boldsymbol{\beta}_i$，其传递函数近似为：
$$M_i(\mathbf{x}, \lambda) \approx b_i(\lambda) \exp\left(j\frac{2\pi}{\lambda_c}\boldsymbol{\beta}_i \cdot \mathbf{x}\right)$$
其中 $b_i(\lambda)$ 为透射效率。通过联合设计 $\boldsymbol{\alpha}_i$ 与 $\boldsymbol{\beta}_i$，可精确调控各通道点扩散函数（PSF）的色散位移。

**4. 目镜透镜**
每个通道对应一个理想薄透镜，焦距为 $f$，其相位调制为：
$$L_i(\mathbf{x}) = (\|\mathbf{x} - \mathbf{x}_i\| < r_i) \exp\left(-\frac{j\pi\|\mathbf{x} - \mathbf{x}_i\|^2}{\lambda f}\right)$$

**5. 光学滤光片 $F_{1:4}$**
可选插入中性密度（ND）滤光片或偏振片，以调节各通道的曝光量或偏振敏感性。在 HDR 高光谱成像模式下，$I_{1:3}$ 通道使用 0.3 OD 的 ND 滤光片，$I_4$ 使用 0.9 OD ND 滤光片，实现多曝光捕获。

**6. 图像传感器**
传感器位于后焦面，同时捕获四个子图像 $I_{1:4}$。子图像形成模型包含高斯读出噪声和光子散粒噪声：
$$I_i(\mathbf{x};j) = \text{Gauss}(0,\sigma^2) + G \cdot \text{Poisson}\left(t \int \eta(\lambda;j) (H(\mathbf{x},\lambda) \odot h(\mathbf{x},\lambda)) d\lambda\right)$$

### 核心公式：色散位移控制

整个光学管线推导的核心结果是第 $i$ 通道 PSF 的波长依赖空间位移：
$$\Delta\mathbf{x}_i(\lambda) = \frac{\lambda f}{\lambda_c}(\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i)$$

**变量含义：**
- $\Delta\mathbf{x}_i(\lambda)$：波长 $\lambda$ 处 PSF 相对参考位置的横向位移
- $\lambda_c$：设计中心波长
- $f$：目镜焦距
- $\boldsymbol{\alpha}_i$：$M_0$ 施加的偏转角参数
- $\boldsymbol{\beta}_i$：$M_i$ 施加的补偿偏转角参数

**设计自由度：**
- 当 $\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i = 0$ 时，色散被完全消除，通道呈消色差行为（如原型中的 $I_3, I_4$ 通道）
- 当 $\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i \neq 0$ 时，保留可控色散用于光谱编码（如 $I_1, I_2$ 通道的相互正交色散）

这一公式揭示了 MetaSpectra+ 将折射成像与超构表面分束/色散控制解耦后的核心调控机制：通过双层超构表面的联合设计，首次在紧凑系统中实现了对各通道色散的独立、精确控制，从而将操作带宽扩展至 250 nm（450–700 nm）。

### 超构表面物理实现

超构表面采用 SiN 纳米柱阵列实现相位与色散控制。每个纳米单元的半径从预计算库中选取，以最佳匹配目标相位调制：
$$r_i(w\mathbf{k}) = \arg\min_{r_n} \left| M_i(w\mathbf{k}) - M(r_n; \lambda_{c,i}) \right|$$

### 通道光谱响应标定

每个通道的光谱效率通过测量有无光学组件时的单色能量比获得：
$$\alpha_i(\lambda) = \eta(\lambda) E_i(\lambda) / E(\lambda)$$
其中 $\eta(\lambda)$ 为传感器光谱响应，$E_i(\lambda)$ 和 $E(\lambda)$ 分别为有/无光学组件时测得的单色能量。原型中四个通道的设计波长分别为 $\lambda_{c,1:4} = \{450, 550, 600, 750\}$ nm（见 Figure 3d）。

### 计算重建

捕获的子图像通过标准图像复原网络进行高光谱重建。文中使用了两种后处理架构：DWDN 和 DDPM。DDPM 的重建过程中引入了偏置项 $b^{k,t}$ 并采用衰减学习率调度，消融实验表明这两项改进均提升了重建质量。对于 HDR 高光谱模式，采用 Debevec 和 Malik 经典方法对多曝光子图像进行融合；偏振模式则通过正交偏振通道计算线偏振度：
$$\text{DoLP}_{HV} = |I_3 - I_4| / |I_3 + I_4|$$

### 补充图表

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/002_Figure_2.jpg]]
*Figure 2: MetaSpectra+ optical design. The optical assembly simultaneously captures multiple sub-images*

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/009_Figure_6.jpg]]
*Figure 6: Schematics of the beamsplitting metasurface*

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/011_Figure_8.jpg]]
*Figure 8: CAD model of the assembly. Numbers correspond to the items in the list of parts in Tab. 3*

## 实验与关键发现

### 核心实验设置

MetaSpectra+ 原型在 450–700 nm（250 nm 带宽）下工作，采用四通道设计：设计波长 λ_{c,1:4} = {450, 550, 600, 750} nm，其中 I₁ 和 I₂ 通道保留可控色散用于光谱编码，I₃ 和 I₄ 通道通过 α_i + β_i = 0 实现消色差成像（见 Eq. (13) 和图 3c–e）。训练数据由 Harvard 和 ICVL 数据集合成，子图像通过 D-Flat 模拟器 基于光学设计渲染，并注入高斯读出噪声和光子散粒噪声（Eq. (14)）。两种重建架构——DWDN 和 DDPM——均在合成数据上训练，在 KAUST 数据集 上测试，该数据集未参与任何方法的训练。

### 主结果：KAUST 数据集重建精度

Table 1 给出了与近期快照高光谱成像系统的系统级对比。MetaSpectra+ 在 PSNR/SSIM/SAM 三项指标上均取得最优：DWDN 版本达到 32.92 dB / 0.94 / 0.17，DDPM 版本达到 33.31 dB / 0.92 / 0.23，较第二名 **2-in-1 Cam**（SIGGRAPH 2024）的 31.14 dB 提升 +2.17 dB。同时，MetaSpectra+ 以 17 mm 的总轨道长度（TTL）实现了最小的系统体积，并支持 4 路同时子图像捕获（Table 1）。Figure 4 的定性对比显示，MetaSpectra+ 在结构保真度和光谱精度上均优于所有对比方法，放大区域可见更清晰的纹理和更准确的光谱恢复。

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/004_Table_1.jpg]]
*Table 1: System-level comparison of recent hyperspectral imagers. These systems exhibit complementary strengths in F-number, field of view (FoV), and compactness (quantified by total track length, TTL). MetaSpectra+ achieves the smallest TTL, enabled by the use of metasurfaces in its hybrid design. It also delivers the highest reconstruction accuracy across all metrics on the KAUST dataset. * indicates systems can simultaneously capture an achromatic RGB image for structural guidance*

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/005_Figure_4.jpg]]
*Figure 4: Sample hyperspectral reconstruction results on the KAUST dataset. MetaSpectra+ produces the highest structural fidelity and spectral accuracy among all compared methods. See enlarged insets for details. The inset numbers are PSNR (dB) for hyperspectral reconstructions*

### 真实场景多功能成像

在真实场景测试中，系统展示了三种工作模式：

- **纯高光谱成像**（Figure 5a）：从单次曝光中重建 31 通道高光谱数据立方体。
- **HDR + 高光谱成像**（Figure 5b）：通过在 I₁:₃ 子图像上放置 0.3 OD 中性密度滤光片、在 I₄ 上放置 0.9 OD ND 滤光片实现曝光包围，采用 Debevec 和 Malik 方法融合 I₃ 和 I₄ 得到 HDR 估计，最终重建的动态范围相比原生 CMOS 低动态范围图像提升 **11 dB**。
- **偏振 + 高光谱成像**（Figure 5c）：I₃ 和 I₄ 分别配置正交偏振片，通过 DoLP_{HV} = |I₃ − I₄| / |I₃ + I₄| 计算水平-垂直线偏振度，同时保持高光谱重建能力。

### 消融研究

**DDPM 后处理改进。** 在 DDPM 的归一化步骤中引入偏置项 b^{k,t} 并采用衰减学习率调度，经验上提升了重建质量。Table 2 列出了 DDPM 的完整超参数配置，但论文未给出该消融的定量对比数据，需手动核实具体增益幅度。

**随机交织 vs. 规则交织。** 分束超构表面 M₀ 采用随机交织（Eq. (5)）而非规则交织，有效抑制了由大偏转角引起的高阶衍射伪影（Figure 7 对比仿真显示了波前振幅的改善），但代价是光效率降低，导致当前原型需要较长积分时间。

### 系统局限与失败模式

1. **帧率瓶颈。** 随机交织导致的衍射效率损失使原型帧率上限约 10 FPS，难以应用于高速视频场景。论文指出可通过降低束偏转角或采用高折射率材料（如 GaN, TiO₂）来改善光效和速度，但未给出实验验证。
2. **光效与带宽的权衡。** 宽带操作（250 nm）的代价是各通道光谱响应存在差异（Figure 3d），且整体光效率受限于超构表面的衍射效率，在低光照场景下信噪比可能不足。
3. **标定依赖性。** 通道光谱响应 α_i(λ) 需通过单色光测量逐波长标定（Eq. (16)），标定精度直接影响重建质量，但论文未讨论标定误差的传播影响。

### 图表要点总结

- **Table 1**：系统级对比核心表，MetaSpectra+ 在重建精度（PSNR 最高 33.31 dB）和紧凑性（TTL 17 mm）上均领先，同时是唯一支持 4 路同时子图像的系统。
- **Figure 4**：KAUST 数据集定性对比，MetaSpectra+ 在细节恢复和光谱准确性上明显优于 2-in-1 Cam、Array-HSI、SCCD 等基线。
- **Figure 5**：真实场景多功能验证，HDR 模式动态范围提升 11 dB，偏振模式成功分离正交偏振分量。
- **Figure 7**：随机交织消融仿真，直观展示其抑制高阶衍射伪影的效果。

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/006_Figure_5.jpg]]
*Figure 5: Sample real-world results of MetaSpectra+. (a) Hyperspectral imaging only. (b) HDR + hyperspectral imaging. Inset numbers represent the dynamic range (dB) of the picture. Compared to low-dynamic range (LDR) images recorded with CMOS cameras, the reconstructed HDR images from MetaSpectra+ demonstrate increases of 11 dB in dynamic range, and preserve both dark and bright scene details. Zoom in for finer structures. Inset numbers represent the dynamic range (dB) of the scene. (c) Polarization + hyperspectral imaging. The sample scene includes a*

### 公平性说明

所有对比方法的评估均在 KAUST 数据集上进行，该数据集未用于任何方法的训练。对于光谱覆盖或分辨率无法对齐至 450–700 nm 的方法，结果在其原始光谱网格上生成（Table 1 备注）。

### 补充图表

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/007_Table_2.jpg]]
*Table 2: Hyperparameters of DDPM*

![[assets/figures/papers/paper_list_l2086_https_arxiv_org_abs_2603_09116/figures/010_Table_3.jpg]]
*Table 3: List of parts*

## 定位与知识库关联

### 1. 问题定位：多功能超构表面成像的窄带瓶颈

现有多功能超构表面成像系统面临一个根本性矛盾：单一超构表面同时承担分束与成像功能时，强烈的色散像差将可操作带宽压缩至10–100 nm量级，只能在单波长或极窄带内工作。这直接限制了系统同时获取宽带高光谱数据与其他成像模态（如高动态范围、偏振）的能力。MetaSpectra+ 的核心诊断是：**成像与分束的耦合是窄带瓶颈的结构性根源**。

### 2. 因果杠杆：功能解耦与双层色散编码

MetaSpectra+ 的解决方案是将折射光学与超构表面解耦：

- **折射透镜**负责低F数（f/6~12）成像，释放超构表面的成像负担；
- **双层超构表面**仅负责分束与色散控制：第一层（M₀）将入射光束分为多个通道并施加偏转角 $\boldsymbol{\alpha}_i$，第二层（M₁:₄）对各通道施加额外偏转 $\boldsymbol{\beta}_i$，通过联合设计使点扩散函数的色散位移 $\Delta\mathbf{x}_i(\lambda) = \frac{\lambda f}{\lambda_c}(\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i)$ 可精确调谐甚至消除（当 $\boldsymbol{\alpha}_i + \boldsymbol{\beta}_i = 0$ 时）。

这一设计将操作带宽从窄带扩展至250 nm（450–700 nm），覆盖几乎整个可见光波段，同时保持紧凑形态（总轨道长度仅17 mm，为Table 1中所有系统最小）。

### 3. 与现有快照高光谱成像系统的关系

MetaSpectra+ 在系统级指标上与近期代表性工作形成互补而非替代关系（Table 1）：

| 系统 | 核心机制 | F数 | 视场 | TTL | 子图像数 | 宽带能力 |
|------|----------|-----|------|-----|----------|----------|
| **2-in-1 Cam** (SIGGRAPH 2024) | 衍射光学+RGB引导 | 较高 | 较大 | 较长 | 2 | 窄带 |
| **Array-HSI** (SIGGRAPH Asia 2024) | 微透镜阵列 | 中等 | 中等 | 中等 | 多 | 窄带 |
| **SCCD** (Optica 2021 / ICCV 2021) | 编码孔径+色散 | 较高 | 中等 | 较长 | 1 | 宽带 |
| **MetaSpectra+** | 折射+双层超构表面 | f/6~12 | 中等 | **17 mm（最小）** | **4（最多）** | **250 nm（最宽）** |

关键差异在于：MetaSpectra+ 是唯一同时实现最小TTL、最多同步子图像和宽带操作的方案。在KAUST数据集上，MetaSpectra+（DWDN）以32.92 dB PSNR超越2-in-1 Cam（31.14 dB）和Array-HSI（27.44 dB），MetaSpectra+（DDPM）进一步提升至33.31 dB——这是Table 1中所有系统的最高重建精度。

与RGB-to-spectrum方法（如 **MST++** 和 **HRNet**，CVPRW 2020）相比，MetaSpectra+ 不依赖RGB图像的先验光谱假设，而是从物理编码的子图像中直接重建，对场景光谱复杂度的鲁棒性更强。

### 4. 适用边界与局限

**适用场景**：MetaSpectra+ 适用于需要单次曝光同时获取宽带高光谱数据与HDR/偏振信息的静态或准静态场景，如材料检测、生物医学成像、遥感等。

**核心局限**：

1. **光效与帧率矛盾**：随机交织策略（式5）虽有效抑制高阶衍射伪影（Figure 7验证），但导致衍射效率下降，当前原型积分时间较长，帧率上限约10 FPS，难以直接应用于高速视频场景。这是“宽带能力”与“光通量”之间的根本权衡。

2. **材料限制**：当前采用SiN纳米柱阵列，其折射率限制了偏转角与衍射效率的联合优化空间。更高折射率材料（如GaN、TiO₂）可能改善光效，但需验证其宽带相位调控能力与制造成本。

3. **标定复杂度**：四个通道的光谱响应 $\alpha_i(\lambda)$ 需逐通道标定（式16），且各通道设计波长 $\lambda_{c,1:4} = \{450, 550, 600, 750\}$ nm 不同，标定流程对系统复现构成工程门槛。

### 5. 开放问题

1. **光效-带宽-紧凑性的三元优化**：能否在不牺牲250 nm带宽和17 mm TTL的前提下，通过超构表面拓扑优化或非周期性排布将衍射效率提升至实用视频帧率（>30 FPS）水平？

2. **材料替代的可行性与成本**：GaN或TiO₂超构表面能否在可见光波段实现与SiN相当的相位控制精度，且其制造工艺是否兼容大规模量产？

3. **计算重建的泛化性**：DWDN和DDPM均在Harvard和ICVL合成数据上训练，对KAUST真实数据的跨域泛化表现良好，但对更极端的光照条件（如极低照度、强眩光）和非常见光谱分布场景的鲁棒性尚未验证。

4. **多模态融合的理论上限**：MetaSpectra+ 同时获取高光谱、HDR和偏振信息，但三者共享有限的光子预算。是否存在一个信息论框架来定量分析光子在多模态间的分配效率与重建精度的理论边界？

5. **系统可复现性**：原型依赖定制3D打印件和商用光机组件组装（Table 3, Figure 8），其光学对准精度和长期稳定性对实际部署的影响需要更多量化评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/MetaSpectra_A_Compact_Broadband_Metasurface_Camera_for_Snapshot_Hyperspectral_Imaging.pdf]]

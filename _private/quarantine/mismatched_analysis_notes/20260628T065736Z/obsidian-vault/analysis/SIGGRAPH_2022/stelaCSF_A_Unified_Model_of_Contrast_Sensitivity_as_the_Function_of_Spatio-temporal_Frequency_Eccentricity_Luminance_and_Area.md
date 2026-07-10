---
title: stelaCSF — A Unified Model of Contrast Sensitivity as the Function of Spatio-temporal Frequency, Eccentricity Luminance, and Area
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/stelaCSF_A_Unified_Model_of_Contrast_Sensitivity_as_the_Function_of_Spatio_temporal_Frequency_Eccentricity_Luminance_and_Area.pdf
project_link: "https://kenchen10.github.io/projects/tmometric/index.html"
code_link: null
aliases:
- MASDPE
- SUMCSAFSTFEL
tags:
- SIGGRAPH_2022
- topic/benchmarks_datasets_evaluation
core_operator: 通过显示模型将显示编码内容转换为绝对光度值，再使用感知均匀传输函数（PU21）将两者映射到共同的显示编码空间，消除表示差异。
primary_logic: 无需设计新的专用色调映射质量度量；通过简单的输入适配策略（显示模型 + 感知编码），即可大幅提升现有通用 SDR 质量度量的预测性能，并持续优于专门设计的色调映射度量。
claims:
- 经过 DM + PU21 编码的通用度量（如 TOPIQ、DISTS）在所有五个数据集上的平均 Spearman 相关性显著高于专门色调映射度量（见图 8 排名）。
- 仅对 HDR 参考进行编码（如线性编码）时相关性显著低于同时编码参考与测试的 DM + PU21 策略（见图 8 中不同星形标记的比较）。
- Aggregate over 5 tone mapping datasets (LUNAM, Linköping, LIVE, What is HDR?, O... 上 Mean Spearman rank correlation = DM+PU21 adapted general-purpose metrics (e.g., TOPIQ, DISTS...
- Our Dataset (Illumination vs. Reflectance study) 上 Just-Objectionable-Difference (JOD) = Larger quality drop and steeper slope when reflectance cont...
---

# stelaCSF — A Unified Model of Contrast Sensitivity as the Function of Spatio-temporal Frequency, Eccentricity Luminance, and Area

> [!tip] 核心洞察
> 无需设计新的专用色调映射质量度量；通过简单的输入适配策略（显示模型 + 感知编码），即可大幅提升现有通用 SDR 质量度量的预测性能，并持续优于专门设计的色调映射度量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 适应色调映射的质量度量 |
| 英文题名 | stelaCSF — A Unified Model of Contrast Sensitivity as the Function of Spatio-temporal Frequency, Eccentricity Luminance, and Area |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.cl.cam.ac.uk/~rkm38/) · [Project](https://kenchen10.github.io/projects/tmometric/index.html) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Metric Adaptation Strategy with DM + PU21 Encoding |
| Dataset | Aggregate over 5 tone mapping datasets, Our Dataset |

> [!tip] 效果简介
> - Aggregate over 5 tone mapping datasets (LUNAM, Linköping, LIVE, What is HDR?, O... 上，Mean Spearman rank correlation DM+PU21 adapted general-purpose metrics (e.g., TOPIQ, DISTS) rank highest vs Specialized tone mapping metrics (e.g., FSITM, CIVDM) rank significantly lower (Clear and consistent improvement in correlation, with adapted metrics outperfor...)。
> - Our Dataset (Illumination vs. Reflectance study) 上，Just-Objectionable-Difference (JOD) Larger quality drop and steeper slope when reflectance contrast is reduced vs Milder quality drop when illumination contrast is reduced (Confirms the hypothesis that observers are more tolerant to illumination change...)。

## 概要

色调映射将高动态范围（HDR）内容转换为标准动态范围（SDR）显示，但 HDR 参考与 SDR 测试图像之间的光度表示差异，使现有通用质量度量无法直接比较两者的感知质量。本文提出一种**度量适配策略**：通过显示模型（GOG）将显示编码内容转换为绝对光度值，再利用感知均匀传输函数（PU21）将两者映射到共同的显示编码空间，使通用 SDR 质量度量无需修改即可用于色调映射质量评估。此外，针对 ColorVideoVDP 度量，提出分别对参考和测试图像采样对比度敏感度的改进（ColorVideoVDP-tm），增强其对绝对亮度差异的敏感性。

在五个色调映射数据集上的评估表明，经过 DM+PU21 编码适配的通用度量（如 TOPIQ、DISTS）在所有数据集上的平均 Spearman 相关性均显著优于专门设计的色调映射度量（如 FSITM、CIVDM）。该方法的核心洞察在于：无需设计新的专用度量，通过简单的输入表示适配即可大幅提升现有通用度量的预测性能。该方法属于**输入适配层**，位于显示编码与质量度量之间，可灵活接入各类通用度量。

## 核心方法与创新机理

### 问题瓶颈：光度表示差异导致的度量失效

色调映射质量评估的核心瓶颈在于：HDR 参考图像存储的是绝对光度值（cd/m²），而色调映射后的 SDR 测试图像存储的是显示编码值（如 0–255 的 gamma 编码像素值）。这两者处于完全不同的表示空间，现有通用质量度量无法直接比较。专用色调映射度量（如 FSITM、CIVDM）虽然接受混合输入——HDR 参考为光度值、SDR 测试为显示编码值——但它们的预测性能始终不理想。本文的核心洞察是：**无需设计新的专用度量，通过一个简单的输入适配策略，即可让现有通用 SDR 质量度量大幅超越专用度量**。

### 核心机制：显示模型 + 感知编码的双向统一

适配策略的关键操作是将参考和测试图像都映射到一个**共同的显示编码空间**。这需要两步变换，如图 1 所示：

**第一步：显示模型（Display Model）将显示编码值还原为绝对光度值。** 对于 SDR 内容，采用增益-偏移-伽马（GOG）模型：

$$\mathbf{I} = \mathcal{M}_{\mathrm{SDR}}(\mathbf{D}) = (L_{\mathrm{max}} - L_{\mathrm{min}}) \cdot \mathcal{P}^{-1}(\mathbf{D}) + L_{\mathrm{min}} + L_{\mathrm{refl}}$$

其中 $\mathbf{D}$ 是显示编码像素值，$\mathcal{P}^{-1}$ 是电光传输函数（EOTF），$L_{\mathrm{max}}$ 和 $L_{\mathrm{min}}$ 分别为显示器的峰值和黑位亮度，$L_{\mathrm{refl}}$ 为环境光反射分量。对于 HDR 内容（通常以 PQ 编码），直接应用 PQ 的逆变换即可：

$$\mathbf{I} = \mathcal{M}_{\mathrm{HDR}}(\mathbf{D}) = \mathcal{P}^{-1}(\mathbf{D})$$

**第二步：感知编码（Perceptual Encoding）将光度值映射到感知均匀的显示编码空间。** 本文采用 PU21 感知传输函数：

$$\mathcal{P}_{\star}(\mathbf{I}) = a\left(\log_{2}(\mathbf{I}) - \log_{2}(0.005)\right)^{2} + b\left(\log_{2}(\mathbf{I}) - \log_{2}(0.005)\right) + c$$

该函数将绝对光度值 $\mathbf{I}$ 映射到 0–1 范围，且该空间中的等量数值差对应等量的感知差异。经过这两步后，HDR 参考和 SDR 测试图像均处于同一显示编码空间，可直接输入任意通用质量度量。

### Changed Slot 1：从仅编码参考到双向编码

基线适配策略（Naïve adaptation）仅对 HDR 参考应用光电传输函数（OETF），而 SDR 测试保持原始显示编码：

$$q = Q\left(\mathcal{P}(\mathbf{I}_R), \mathbf{D}_T\right)$$

这一策略的根本缺陷在于：OETF 编码后的参考与显示编码的测试仍处于不同的表示空间，度量无法公平比较两者的感知差异。本文提出的策略同时对两者进行显示模型还原和感知编码：

$$q = Q\left(\mathcal{P}_{\star}(\mathcal{M}_{\mathrm{SDR}}(\mathbf{D}_R)), \mathcal{P}_{\star}(\mathcal{M}_{\mathrm{SDR}}(\mathbf{D}_T))\right)$$

这一改变确保了参考和测试在输入度量之前经历了完全相同的变换链。消融实验（Figure 8, Section 5.3）证实：DM+PU21 编码在所有五个数据集上的 Spearman 相关性一致高于线性编码、PQ 编码、μ-law 编码或仅使用 PU 编码的策略。

![[assets/figures/papers/paper_list_l16_https_www_cl_cam_ac_uk_rkm38/figures/013_Figure_8.jpg]]
*Figure 8: Metric evaluation. Image and video quality metrics are compared with respect to mean Spearman correlation coefficient across the five tone mapping quality assessment datasets. The metrics are sorted (bottom to top) based on correlation across all the display encodings tested, with top-performing encoding techniques connected with a solid line. Colored stars represent different display encoding techniques; white stars represent quality metrics that accept photometric inputs (i.e., do not require display encoding). Note that correlation scores can have a range between 0–1; we plot a constrained range here for better visualization. We also included the metric’s approach, with symbols represent...*

### Changed Slot 2：对比度敏感度的双向采样

视觉差异预测器（VDP）类度量（如 ColorVideoVDP）的失效原因更为精细。基础 ColorVideoVDP 在计算对比度敏感度时，仅针对参考图像采样：

$$\mathbf{C}_{R_{(x,y)}}^{\prime} = \mathbf{C}_{R_{(x,y)}} S(\mathbf{L}_{R_{(x,y)}})$$

其中 $S(\cdot)$ 是对比度敏感度函数，$\mathbf{L}_{R_{(x,y)}}$ 为参考图像的局部亮度。这导致度量对测试图像中因绝对亮度变化引起的感知差异不敏感——而色调映射恰恰会大幅改变绝对亮度。

本文提出的 ColorVideoVDP-tm 分别对参考和测试图像计算对比度敏感度：

$$\mathbf{C}_{R_{(x,y)}}^{\prime} = \mathbf{C}_{R_{(x,y)}} S(\mathbf{L}_{R_{(x,y)}}); \quad \mathbf{C}_{T_{(x,y)}}^{\prime} = \mathbf{C}_{T_{(x,y)}} S(\mathbf{L}_{T_{(x,y)}})$$

这一修改使度量能够捕捉绝对亮度差异带来的感知影响。如 Figure 2 所示，ColorVideoVDP-tm 生成的误差图能更好地反映绝对亮度失真，而基础 ColorVideoVDP 的误差图则遗漏了这些区域。

![[assets/figures/papers/paper_list_l16_https_www_cl_cam_ac_uk_rkm38/figures/006_Figure_2.jpg]]
*Figure 2: Error map visualization. Our ColorVideoVDP-tm can generate error maps that better account for distortions in absolute luminance compared to the base ColorVideoVDP metric. “Reference” and “Tone-mapped” images here were tone-mapped for presentation*

### 模块顺序与推理路径

完整的推理流水线由以下模块按顺序构成：

1. **Display Model (GOG)**：接收 SDR 显示编码内容 $\mathbf{D}$，根据显示器参数（$L_{\mathrm{max}}$、$L_{\mathrm{min}}$、$L_{\mathrm{refl}}$）将其转换为绝对光度值 $\mathbf{I}$。对于 HDR 内容，使用 PQ 逆变换。
2. **Perceptual Encoding (PU21)**：将光度值 $\mathbf{I}$ 映射到感知均匀的显示编码空间，输出归一化值 $\mathcal{P}_{\star}(\mathbf{I}) \in [0,1]$。
3. **Quality Metric**：在统一的显示编码空间中计算感知质量分数。可选度量包括 TOPIQ、DISTS、ColorVideoVDP 等通用度量，或经过对比度敏感度修改的 ColorVideoVDP-tm。
4. **Contrast Sensitivity Sampling（仅 ColorVideoVDP-tm）**：在第 3 步之前，分别为参考和测试图像计算对比度敏感度，使度量对绝对亮度变化敏感。

### 因果链路解析

**显示模型 → 感知编码 → 度量性能提升** 的因果链如下：显示模型消除了 SDR 显示编码的非线性（gamma 曲线），将内容还原到线性光度域；PU21 编码将线性光度值映射到感知均匀空间，使得等量数值差对应等量感知差异。这一变换链的核心作用是**消除 HDR 参考与 SDR 测试之间的表示差异**，使通用度量能够公平比较两者的感知质量。消融实验（Section 5.3）证实，单独使用显示模型或单独使用感知编码均无法达到组合的效果，说明两步变换之间存在协同效应——显示模型提供正确的物理亮度，感知编码提供正确的感知尺度。

**对比度敏感度双向采样 → ColorVideoVDP-tm 性能提升** 的因果链：色调映射会显著改变图像的绝对亮度分布。基础 ColorVideoVDP 仅使用参考图像的对比度敏感度来加权误差，隐含假设测试图像的局部亮度与参考相似。当这一假设被色调映射破坏时，度量的预测能力下降。双向采样使度量能够根据测试图像的实际亮度调整感知权重，从而更准确地预测主观质量。实验（Section 5.4, Figure 8）证实 ColorVideoVDP-tm 在色调映射质量预测上显著优于基础 ColorVideoVDP。

### 方法边界与未验证假设

本方法假设显示器的峰值亮度 $L_{\mathrm{max}}$、黑位亮度 $L_{\mathrm{min}}$ 和环境光反射 $L_{\mathrm{refl}}$ 已知。在实际部署中，这些参数可能需要针对具体显示设备进行校准。此外，PU21 传输函数的设计基于特定观看条件下的对比度敏感度数据，其在极端亮度范围或不同色域空间中的有效性需要进一步验证。

## 实验与关键发现

### 整体评估框架

为系统验证度量适配策略的有效性，作者在五个色调映射质量评估数据集上进行了大规模基准测试：LUNAM、Linköping、LIVE、What is HDR? 以及本文新构建的数据集。评估采用成对比较协议，以 Spearman 秩相关系数作为度量预测与主观评分一致性的核心指标。为跨数据集聚合相关性，使用 Fisher 变换归一化后计算平均 Spearman 相关系数：

$$\rho = F^{-1}\left(\frac{1}{N_{\mathcal{D}}}\sum_{d\in\mathcal{D}}F(\rho_{d})\right), \quad F(\rho) = \frac{1}{2}\ln\left(\frac{1+\rho}{1-\rho}\right)$$

这一设计避免了直接平均相关系数带来的统计偏差，使跨数据集比较更为稳健。

### 主要结果：适配通用度量全面超越专用色调映射度量

Figure 8 展示了所有度量在不同显示编码策略下的平均 Spearman 相关性排名，是本研究的核心证据。最关键的发现是：经过 **DM + PU21** 编码适配的通用图像/视频质量度量（如 TOPIQ、DISTS、ColorVideoVDP-tm）在所有五个数据集上的平均相关性**显著且一致地高于**专门为色调映射设计的度量（如 FSITM、CIVDM）。具体而言：

- **TOPIQ + DM + PU21** 在所有测试度量中排名最高，其相关性远超任何专用色调映射度量。
- **DISTS + DM + PU21** 紧随其后，同样大幅领先于专用度量。
- 专用度量如 **FSITM** 和 **CIVDM** 的相关性排名处于中下游，即使与其最佳编码策略组合，仍无法匹敌适配后的通用度量。

这一结果直接支撑了本文的核心主张：**无需设计新的专用色调映射质量度量**，通过对现有通用 SDR 度量施加恰当的输入适配，即可获得更优的色调映射质量预测性能。

### 编码策略消融：DM + PU21 的压倒性优势

Figure 8 中不同颜色星形标记的对比揭示了编码策略选择的决定性作用。消融对比覆盖了五种编码方案：

| 编码策略 | 核心机制 | 平均 Spearman 相关性表现 |
|---------|---------|----------------------|
| **DM + PU21** | 显示模型 + 感知均匀传输函数 | **最优**，所有数据集上一致最高 |
| PU-only | 仅 PU21 编码，无显示模型 | 显著低于 DM + PU21 |
| Linear | 线性重缩放至 [0,1] | 远低于 DM + PU21 |
| PQ | 感知量化编码 | 低于 DM + PU21 |
| μ-law | 对数压缩编码 | 低于 DM + PU21 |

**DM + PU21 相比其他编码策略的优势在所有数据集上保持一致**，不存在某个数据集上其他策略反超的情况。这一消融强有力地证明：显示模型（将显示编码内容转换为绝对光度值）与 PU21 感知传输函数（将光度值映射到感知均匀空间）**两者缺一不可**。仅使用 PU21 而跳过显示模型会导致性能显著下降，因为此时 HDR 参考与 SDR 测试图像的光度表示差异未被充分消除。

### 关键消融：参考与测试双端编码的必要性

Figure 8 中的白色星形标记代表接受光度输入（无需显示编码）的度量，其性能普遍低于经过 DM + PU21 编码的度量。更关键的是，仅对 HDR 参考进行编码的“朴素适配策略”（Naïve adaptation，式 13）在相关性上显著低于同时编码参考与测试的 DM + PU21 策略。这一对比揭示了核心因果机制：

- **仅编码参考**：$q = Q(\mathcal{P}(\mathbf{I}_R), \mathbf{D}_T)$ 仅消除了 HDR 参考的表示差异，但 SDR 测试图像仍保持原始显示编码，两者仍处于不同“语言”空间。
- **双端编码**：DM + PU21 将两者统一映射到共同的感知均匀显示编码空间，使度量能够公平比较。

这一消融直接验证了本文的瓶颈诊断：**HDR 参考与 SDR 测试之间的光度表示差异是常规度量失效的根本原因**，而双端编码是消除该差异的必要条件。

### ColorVideoVDP-tm：对比度敏感度独立采样的增益

ColorVideoVDP 基础版本在色调映射质量预测上表现不佳，因为其视觉差异预测器（VDP）仅针对参考图像计算对比度敏感度。本文提出的 **ColorVideoVDP-tm** 修改了这一机制，分别为测试和参考图像采样对比度敏感度：

$$\mathbf{C}_{R_{(x,y)}}^{\prime} = \mathbf{C}_{R_{(x,y)}} S(\mathbf{L}_{R_{(x,y)}}); \quad \mathbf{C}_{T_{(x,y)}}^{\prime} = \mathbf{C}_{T_{(x,y)}} S(\mathbf{L}_{T_{(x,y)}})$$

这一修改使度量对绝对亮度差异更为敏感。Figure 8 显示，ColorVideoVDP-tm 的相关性排名显著高于基础版本，且 Figure 2 的可视化对比表明，ColorVideoVDP-tm 生成的误差图能更好地捕捉绝对亮度失真区域。

### 主观实验：光照与反射率容忍度差异

本文构建的新数据集包含一项控制实验，系统操纵色调映射中的光照对比度（$\gamma_i$）和反射率对比度（$\gamma_r$），各采样五个水平（$\gamma_i = 0.6, 0.7, 0.8, 0.9, 1.0$；$\gamma_r = 0.6, 0.733, 0.867, 1.0, 1.133$）。15 名参与者（10 男 5 女，19-47 岁）通过 ASAP 主动采样成对比较协议进行评分，结果缩放为 Just-Objectionable-Difference（JOD）单位。

Figure 6 展示了核心发现：
- **反射率对比度降低**时，JOD 质量下降幅度更大、斜率更陡。
- **光照对比度降低**时，JOD 质量下降相对平缓。

![[assets/figures/papers/paper_list_l16_https_www_cl_cam_ac_uk_rkm38/figures/011_Figure_6.jpg]]
*Figure 6: Illumination vs. reflectance study data. The user study data scaled to JODs for the illumination vs. reflectance tone mapper is shown here, with either illumination (left, ???? ) or reflectance (right, ???? ) on the ?? -axis and JOD on the ??-axis. The 0 JOD condition was set to the*

这确认了假设：观察者对光照变化比反射率变化**更为宽容**。这一发现对色调映射算法的设计具有指导意义——在动态范围压缩过程中，应优先保留反射率对比度，而光照对比度的牺牲相对可接受。

### 度量优化实验：评估与优化的不一致性

在度量优化研究中（Section 4.3），作者以不同质量度量作为目标函数，通过最大化度量分数优化色调映射参数，然后将优化结果的主观评分与度量预测进行对比。Figure 7 显示了一个值得关注的失败模式：**ColorVideoVDP 在预测主观质量时表现尚可，但在作为优化目标时表现不佳**——其优化出的色调映射图像主观评分较低。这表明度量在“评估”和“优化”两种使用场景下的表现可能不一致，是实际应用中的重要边界条件。

![[assets/figures/papers/paper_list_l16_https_www_cl_cam_ac_uk_rkm38/figures/012_Figure_7.jpg]]
*Figure 7: Metric optimization study data. The ranking of different metrics in the metric optimization study is shown, where the ??-axis shows quality metrics used for optimization and the ??-axis are scaled study results (in JODs, averaged across scenes). We show the lowest and highest-quality tone-mapped images for the “Bloom” scene*

### 适用边界与局限性

1. **数据集覆盖范围**：评估限于五个色调映射数据集，虽然涵盖了多种场景和失真类型，但可能无法完全代表所有色调映射应用场景。某些数据集样本量较小可能引入统计偏差。

2. **显示模型假设**：DM + PU21 策略依赖特定的显示模型参数（峰值亮度 $L_{\mathrm{max}}$、黑位 $L_{\mathrm{min}}$、环境光反射 $L_{\mathrm{refl}}$）。在显示设置未知或与假设偏差较大的场景中，适配效果可能下降。作者未系统测试不同显示参数设置的鲁棒性。

3. **评估与优化的不一致性**：如 Figure 7 所示，某些度量（如 ColorVideoVDP）在预测主观评分和作为优化目标时的表现存在差异，提示度量在闭环优化任务中的可靠性需要独立验证。

4. **主观实验规模**：参与者仅 15 人，虽然采用高效的 ASAP 成对比较协议，但样本量限制可能影响主观数据在更广泛人群中的代表性。

5. **无参考场景缺失**：当前适配策略依赖 HDR 参考图像，无法直接应用于缺少参考的无参考质量评估场景。

## 定位与知识库关联

### 改变的核心 slot：从“域内直接比较”到“显示感知的感知均匀化”

现有色调映射质量评估方法可归为两类：**专用色调映射度量**（如 FSITM、CIVDM）和**通用 SDR 质量度量的 naïve 适配**。两者的共同瓶颈在于，它们都在“表示不匹配”的条件下操作——HDR 参考图像以绝对光度值（或 PQ 编码）存在，而色调映射后的 SDR 测试图像以显示编码（如 sRGB）存在。这种光度表示差异使得任何直接比较都无法可靠捕捉人眼感知的质量退化。

本文改变的 slot 是**输入表示的预处理策略**。具体而言：

- **Baseline slot 值**：专用度量直接接受混合域输入 $q = Q_{\mathrm{t}}(\mathbf{I}_R, \mathbf{D}_T)$（光度参考 + 显示编码测试）；naïve 适配仅对 HDR 参考施加 OETF 编码 $q = Q(\mathcal{P}(\mathbf{I}_R), \mathbf{D}_T)$，测试图像保持原始显示编码。
- **Proposed slot 值**：通过显示模型（GOG）将 SDR 显示编码内容转换为绝对光度值，再使用 PU21 感知传输函数将参考和测试两者同时映射到共同的感知均匀显示编码空间，形成 $q = Q(\mathcal{P}_{\star}(\mathcal{M}_{\mathrm{SDR}}(\mathbf{D}_T)), \mathcal{P}_{\star}(\mathcal{M}_{\mathrm{HDR}}(\mathbf{D}_R)))$。

这一改变的因果链条是：显示模型解决了“显示编码→光度”的逆映射问题，PU21 解决了“光度→感知均匀编码”的正向映射问题，两者联合消除了参考与测试之间的表示鸿沟，使得任何为 SDR 设计的通用质量度量都能直接应用于色调映射评估，而无需修改度量本身的核心算法。

### 相对于专用色调映射度量的本质差异

专用色调映射度量（如 **FSITM** 和 **CIVDM**）的设计思路是“为色调映射任务定制质量预测逻辑”，它们通常内嵌了对动态范围压缩、局部对比度保持等特定失真的手工特征提取。这类方法的根本局限在于：它们假设度量内部已经隐含了显示模型和感知编码，但实际上这些隐含假设往往过于简化或不准确。

本文的策略采取了相反的路径：“不修改度量，而是修正输入”。这类似于计算机视觉中的“域自适应”思想——不是为每个目标域重新训练模型，而是通过输入变换将目标域映射到源域。关键差异在于：

1. **通用性**：专用度量只能用于色调映射评估；适配后的通用度量（如 TOPIQ、DISTS）可同时用于 SDR 和色调映射场景。
2. **可升级性**：随着通用 SDR 度量（如基于深度学习的 TOPIQ）的持续进步，适配策略可“免费”获得性能提升，而专用度量需要重新设计。
3. **性能优势**：图 8 的跨数据集排名显示，经过 DM+PU21 编码的 TOPIQ、DISTS 等通用度量的平均 Spearman 相关性显著高于所有专用色调映射度量，说明“修正输入”的策略在预测准确性上同样优于“定制算法”。

### 知识库挂载点：显示建模与感知编码的标准化接口

本文在知识库中的核心挂载点是**视觉质量评估的输入标准化层**。具体可挂载到以下知识节点：

1. **显示建模（Display Modeling）**：GOG 模型（Berns 1996）作为 SDR 显示的特征化标准，PQ 编码（SMPTE ST 2084）作为 HDR 显示的特征化标准。本文的工作表明，在质量评估流水线中显式引入显示模型是消除域差异的关键步骤。这一发现可推广到任何涉及跨显示比较的场景（如增强现实中的虚实融合质量评估）。

2. **感知均匀编码（Perceptual Uniform Encoding）**：PU21 传输函数作为将光度值映射到感知均匀空间的标准化工具。与线性编码、μ-law、PQ 等替代方案相比，PU21 在色调映射质量预测任务中表现最优（图 8 消融实验），说明其感知均匀性假设在该场景下成立。

3. **视觉差异预测器（VDP）的对比度敏感度采样**：ColorVideoVDP-tm 的修改揭示了一个更底层的原则——当参考与测试的绝对亮度差异显著时，必须分别为两者计算对比度敏感度函数 $S(\mathbf{L})$，而非仅依赖参考图像的单一采样。这一修改可视为对 VDP 类方法的通用增强规则。

### 适用边界与限制条件

本文策略的适用边界由以下因素界定：

- **显示参数依赖性**：显示模型（GOG）需要已知目标显示器的峰值亮度 $L_{\mathrm{max}}$、黑电平 $L_{\mathrm{min}}$ 和环境光反射 $L_{\mathrm{refl}}$。当这些参数未知或与假设偏差较大时，适配效果可能下降。论文未系统测试显示参数失配的鲁棒性，这是一个需要手动验证的边界条件。
- **动态范围上限**：PU21 传输函数的设计基于特定动态范围假设。对于超出常规 HDR 范围（如直接观看高亮度光源）的场景，其感知均匀性可能不再成立。
- **色域假设**：当前策略主要处理亮度域的表示差异，对色域映射（如 HDR 的 BT.2020 到 SDR 的 BT.709）未做显式处理。在色域差异显著的场景中，可能需要额外的色域适配层。
- **评估与优化的不一致性**：论文的度量优化实验（图 7）显示，部分在预测上表现良好的度量（如 ColorVideoVDP）在作为优化目标时表现不佳。这说明适配策略提升了度量的“诊断能力”，但未必提升了其“指导优化”的能力，两者之间存在尚未解决的 gap。

### 后续研究启发

1. **跨应用泛化**：该适配策略的核心思想（显示模型 + 感知编码 = 统一表示空间）可推广到其他导致绝对亮度显著变化的应用，如显示调光（display dimming）以优化功耗、增强现实中的虚实亮度匹配、以及跨显示设备的图像/视频质量评估。

2. **无参考扩展**：当前策略需要 HDR 参考图像。结合无参考质量度量，可在仅有 SDR 测试图像的场景中实现色调映射质量评估——这需要无参考度量能够从单一 SDR 图像中推断出“色调映射质量”这一本质上需要参考的概念，是一个开放挑战。

3. **显示自适应度量**：将显示模型参数作为度量的可调节输入，而非固定假设，可使同一度量适应不同的观看环境（如室内/室外、不同峰值亮度的显示器）。这需要建立显示参数与感知质量之间的定量映射模型。

4. **优化导向的度量设计**：解决“预测好但优化差”的不一致性，可能需要设计专门面向优化的质量度量，或在优化过程中引入额外的约束（如避免产生视觉上不自然的中间状态）。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/stelaCSF_A_Unified_Model_of_Contrast_Sensitivity_as_the_Function_of_Spatio_temporal_Frequency_Eccentricity_Luminance_and_Area.pdf]]
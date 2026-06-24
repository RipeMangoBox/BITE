---
title: "Dark Stereo: Improving Depth Perception Under Low Luminance"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Dark_Stereo_Improving_Depth_Perception_Under_Low_Luminance.pdf
project_link: "https://dark-stereo.mpi-inf.mpg.de/"
code_link: null
aliases:
- DSSPCE
- DSIDPULL
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 通过根据立体恒常性模型增强图像局部对比度，补偿因亮度降低而下降的深度感知精确度。
primary_logic: 基于心理物理实验建立了一个立体恒常性模型（stereo constancy model），该模型量化了在不同亮度和对比度下双目深度线索的精确度；利用该模型可以导出维持同等深度感知精确度所需的对比度增强量，并据此设计了一种实时的多尺度对比度增强算法。
claims:
- 低亮度下心理测量曲线斜率变浅，表明深度判断精确度下降，但感知角度无系统性偏差（准确度不变）。
- 所提立体恒常模型（quadratic function）能很好地拟合实验数据，并揭示在低亮度下需要更强的对比度增强才能维持相同的立体任务精确度。
- 在VR主观实验中，8/9 的观察者认为经本方法处理的图像更具三维感，且同样比例观察者更偏好本方法处理的图像，显著优于标准渲染和Wanat et al.的方法。
- VR主观偏好实验 (Experiment 2) 上 观察者选择本方法更富三维感的比率 (vs 标准渲染) = 88.9% (8/9)
---

# Dark Stereo: Improving Depth Perception Under Low Luminance

> [!tip] 核心洞察
> 基于心理物理实验建立了一个立体恒常性模型（stereo constancy model），该模型量化了在不同亮度和对比度下双目深度线索的精确度；利用该模型可以导出维持同等深度感知精确度所需的对比度增强量，并据此设计了一种实时的多尺度对比度增强算法。

| 字段 | 内容 |
|------|------|
| 中文题名 | 暗光立体视觉：提升低亮度下的深度感知 |
| 英文题名 | Dark Stereo: Improving Depth Perception Under Low Luminance |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://dark-stereo.mpi-inf.mpg.de/) |
| Topic | #topic/other_unclear |
| Method | Dark Stereo (Stereo-preserving Contrast Enhancement) |
| Dataset | VR主观偏好实验 |

> [!tip] 效果简介
> - VR主观偏好实验 (Experiment 2) 上，观察者选择本方法更富三维感的比率 (vs 标准渲染) 88.9% (8/9) vs Standard rendering (+88.9%)；观察者选择本方法更富三维感的比率 (vs Wanat's method) 88.9% (8/9) vs Wanat et al.'s method (+88.9%)；总体偏好选择比率 (vs 标准渲染) 88.9% (8/9) vs Standard rendering (+88.9%)。

## 概要

在低显示亮度（如夜间模式、暗室观影）下，人眼对双目视差深度线索的感知精确度显著下降，导致三维场景的立体感减弱。针对这一问题，本文提出了一种**立体恒常性（stereo constancy）对比度增强方法**。首先，通过心理物理实验建立了立体恒常性模型——一个以亮度和对比度为输入的二次函数，用于量化双目深度线索的感知精确度。基于该模型，作者设计了一种实时的多尺度对比度增强算法：将图像分解为拉普拉斯金字塔，在各频带计算局部RMS对比度，然后依据立体恒常模型导出维持同等深度精确度所需的对比度增强因子，逐像素调整后重建图像。VR主观实验表明，在低亮度条件下，8/9的观察者认为经本方法处理的图像比标准渲染和Wanat等人的对比恒常方法更具三维感，且总体偏好同样为8/9。该方法定位为一种感知驱动的后处理增强，区别于传统基于对比检测阈值的增强思路，直接以恢复立体深度线索精确度为目标。

## 核心方法与创新机理

### 问题背景与唯一瓶颈

立体显示器在低亮度条件下（如移动VR、投影系统、暗室观影）面临一个根本性困境：显示亮度的降低会显著削弱双目视差深度线索的精确度，导致观察者对三维形状的判断变得模糊。现有低亮度图像增强方法（如Wanat et al. 2014年的对比恒常性方法）仅以维持主观感知对比度为目标，并未针对立体深度感知这一特定任务进行优化。本文识别的**唯一瓶颈**是：低显示亮度降低了双目视差深度线索的精确度，而现有对比度增强方法无法有效补偿这一损失。

### 核心机制：从立体恒常性模型到对比度重定向

本文的核心创新在于提出了一种**立体恒常性（stereo constancy）**框架，其运作逻辑分为两个紧密耦合的阶段：

**阶段一：心理物理建模——量化亮度与对比度对立体精度的联合影响。** 作者首先通过心理物理实验（Experiment 1）收集了人类观察者在不同亮度（0.1–1000 cd/m²）和对比度条件下判断立体铰链角度的数据。实验采用仅含视差线索的纹理刺激，排除了其他深度线索的干扰。关键发现是：心理测量函数（psychometric function）的斜率随亮度和对比度降低而变浅，表明深度判断的**精确度**下降，但函数的50%穿越点始终保持在约90°附近，说明深度感知的**准确度**未发生系统性偏差。

为量化这一规律，作者将观察者的判断行为建模为Weibull累积分布形式的心理测量函数：

$$p(\alpha, \beta) = 1 - \exp\Big(\log(0.5) 10^{\beta(\alpha - \alpha_{thr})}\Big)$$

其中 $\alpha$ 为铰链的实际角度，$\alpha_{thr}$ 为50%判断阈限（固定为90°），$\beta$ 为检测敏感度参数，直接反映立体任务的精确度——$\beta$ 越大，心理测量曲线越陡，判断越精确。

进一步，作者假设 $\beta$ 可由对数亮度 $L = \log_{10}(Y)$ 和对数对比度 $c = \log_{10}(C_W + 1)$ 的二次函数解释：

$$\beta(c, L; \mathbf{w}) = w_1 L + w_2 c + w_3 L^2 + w_4 c^2 + w_5$$

该模型通过最大后验估计（MAP）拟合实验数据，目标函数包含二项分布似然项和对二阶参数的正则化先验：

$$\underset{\mathbf{w}}{\arg\min} -\sum_s \sum_{\mathbf{d}} \log\Big(\binom{n_{s,\mathbf{d}}}{k_{s,\mathbf{d}}} \mathcal{P}_{\mathbf{d}}^{k_{s,\mathbf{d}}} (1-\mathcal{P}_{\mathbf{d}})^{(n_{s,\mathbf{d}}-k_{s,\mathbf{d}})}\Big) + \sum_{i=3,4} \frac{1}{2\sigma_i^2} (w_i - \mu_i)^2$$

拟合得到的模型参数见表1，心理测量曲线与实验数据的吻合度见图4（蓝色曲线）。该模型的核心价值在于：对于任意给定的源亮度 $Y_{in}$ 和目标亮度 $Y_{out}$，可以求解出维持相同立体敏感度 $\beta$ 所需的**等效对比度** $c_{eq}$：

$$c_{\mathrm{eq}}(c, Y_{\mathrm{in}}, Y_{\mathrm{out}}) = \frac{-w_2 + \sqrt{w_2^2 - 4 w_4 t}}{2 w_4}$$

其中 $t = w_1 (L_{out} - L_{in}) + w_3 (L_{out}^2 - L_{in}^2)$。

**阶段二：实时对比度增强算法——将立体恒常模型嵌入多尺度图像处理流水线。** 基于上述模型，作者设计了一个完整的实时对比度增强算法，其处理流程如图6所示，包含以下顺序模块：

1. **色彩空间线性化与亮度提取**：将gamma编码的RGB输入转换为线性色彩空间，按ITU-R BT.709基色计算相对亮度：
   $$y_{\mathrm{input}}(\mathbf{x}) = \sum_{k=1}^{3} v_k I_{\mathrm{input}}^{\prime \gamma}(\mathbf{x}, k)$$
   随后转换为对数亮度 $l = \log_{10}(y_{input})$，以便在感知均匀空间中进行对比度操作。

2. **多尺度拉普拉斯金字塔分解**：将对数亮度图像分解为3层拉普拉斯金字塔（2个带通层 + 1个低通层），每层系数为相邻高斯模糊层的差值：
   $$P_{i}(\mathbf{x}) = (g_{i} * l)(\mathbf{x}) - (g_{i+1} * l)(\mathbf{x})$$
   这一分解使得不同空间频率的局部对比度可以被独立操控。

3. **局部RMS对比度测量**：从高斯金字塔高效计算每个像素位置的局部均方根对比度：
   $$c_{i}(\mathbf{x}) = \sqrt{ H_{i}(\mathbf{x}) - G_{i}^{2}(\mathbf{x}) }$$
   其中 $G_i$ 为对数亮度的高斯金字塔，$H_i$ 为对数亮度平方的高斯金字塔。选用RMS对比度而非拉普拉斯系数绝对值的关键原因在于：后者在对比度边缘处存在零交叉，且会低估横跨多个频带的边缘对比度（见图7）。

4. **基于立体恒常模型的对比度重定向**：对于每个像素位置，根据其局部对比度 $c_i(\mathbf{x})$、源亮度 $Y_{in}(\mathbf{x})$ 和目标显示亮度 $Y_{out}(\mathbf{x})$，计算维持相同立体精度的等效对比度 $c_{eq}$，并生成逐像素增强因子：
   $$m_i(\mathbf{x}) = \frac{c_{\mathrm{eq}}\Big(c_i(\mathbf{x}), Y_{\mathrm{in}}(\mathbf{x}), Y_{\mathrm{out}}(\mathbf{x})\Big)}{c_i(\mathbf{x})}$$

5. **金字塔层缩放与重建**：将增强因子应用于各层拉普拉斯系数：
   $$\tilde{P}_i(\mathbf{x}) = P_i(\mathbf{x}) \cdot m_i(\mathbf{x})$$
   将所有增强后的层级求和，得到增强后的对数亮度，再转换回线性亮度空间。

6. **饱和度感知的颜色重建与gamma编码**：将增强后的亮度通道与原始图像的颜色信息结合。为避免对比度增强导致的颜色过饱和，采用饱和度感知的灰度-彩色转换策略（见图9对比），最后进行gamma编码输出。

### 与基线方法的关键差异（Changed Slots）

本文方法相对于Wanat et al. (2014) 的对比恒常性方法，存在三个核心改变槽位：

| 槽位 | 基线值（Wanat et al.） | 本文方法 |
|------|----------------------|---------|
| **核心增强模型** | Kulikowski有效对比恒常模型（基于对比度检测阈值和CSF） | 立体恒常模型（基于双目视差精度的二次函数 $\beta(c, L; \mathbf{w})$） |
| **增强量决定依据** | 维持感知对比度主观相等 | 维持双目深度线索的精确度相等（基于等$\beta$线） |
| **颜色重建策略** | 朴素全局缩放 | 饱和度感知的灰度-彩色转换 |

这些差异导致了一个关键结果：在0.1–10 cd/m²的低亮度区间，立体恒常性所需的对比度增强量**显著大于**对比恒常性所需的增强量（见图5中实线与虚线的对比）。这意味着仅维持主观对比度感知不足以补偿低亮度下的立体深度感知损失，必须针对立体任务进行更强的对比度增强。

### 推理路径与因果链条

整个方法的推理路径可概括为：**低亮度 → 立体敏感度 $\beta$ 下降 → 心理测量曲线变浅 → 深度判断精确度降低 → 通过立体恒常模型求解维持同等 $\beta$ 所需的等效对比度 → 计算逐像素增强因子 → 多尺度对比度增强 → 恢复立体深度感知精确度。**

模块间的因果关系紧密：拉普拉斯金字塔分解为局部对比度测量提供了多尺度表征；RMS对比度测量为立体恒常模型提供了可靠的输入特征；立体恒常模型输出的等效对比度直接驱动增强因子的计算；增强因子反作用于金字塔各层，实现了空间频率自适应的对比度重定向；饱和度感知的颜色重建则防止了增强过程中颜色畸变这一副作用。整个流水线无需训练，所有参数由心理物理实验预校准，支持实时处理。

![[assets/figures/papers/paper_list_l16_https_dark_stereo_mpi_inf_mpg_de/figures/006_Figure_5.jpg]]
*Figure 5: The solid lines, or equivalent-?? lines, connect the contrast values that result in the same precision of perceiving depth (the same*

![[assets/figures/papers/paper_list_l16_https_dark_stereo_mpi_inf_mpg_de/figures/009_Figure_8.jpg]]
*Figure 8: Method of finding equivalent contrast that preserves the precision of binocular disparity cues. Similar as in Figure 5, for a given input contrast and source luminance, our stereo constancy model gives the curves of equivalent contrast (constant*

## 实验与关键发现

### 心理物理实验：低亮度降低立体深度精度而非准确度

论文首先通过严格的立体形状感知实验（Experiment 1）揭示了核心瓶颈：低显示亮度并非使人"看错"深度，而是让人"看不清"深度。实验要求观察者判断仅由双目视差线索再现的铰链状凹面的角度（Figure 2），在四种亮度水平（0.1, 1, 10, 1000 cd/m²）和多种纹理对比度下收集判断数据。

![[assets/figures/papers/paper_list_l16_https_dark_stereo_mpi_inf_mpg_de/figures/002_Figure_2.jpg]]
*Figure 2: Top: The stimulus used in Experiment 1. The observer is presented with a hinge-like concave shape. The angle is changed by moving the hinge part towards or away from the observer (depicted by the arrows). Bottom: Procedural organic pattern on a uniform background. The superimposed grid depicts the three-dimensional shape of the stimuli. Note that the superimposed grid was only added to this figure to facilitate its 3D interpretation, while originally the hinge shape was reproduced only by the disparity cue*

关键发现来自心理测量函数的斜率变化（Figure 4）。在所有亮度和对比度条件下，心理测量曲线在约90°处穿过50%概率点，表明观察者的深度判断没有系统性偏差——**感知准确度（accuracy）未受影响**。然而，曲线的斜率随亮度和对比度降低而显著变浅：低亮度低对比度下曲线更平缓，意味着观察者更频繁地误判角度。这直接证明**低亮度降低了立体深度线索的精确度（precision）**，而非准确度。这一发现构成了整个方法的动机基础：需要补偿的是深度感知的精确度损失，而非校正某种偏差。

![[assets/figures/papers/paper_list_l16_https_dark_stereo_mpi_inf_mpg_de/figures/005_Figure_4.jpg]]
*Figure 4: The red stars are the original data points collected from the 3D shape perception experiment (Section 3). They represent the frequency at which the participants assessed the angle as obtuse under various luminance and contrast conditions. The error bars denote the 99% confidence intervals. The blue curves represent our fitted psychometric model (Section 4). The top-left plot has no data points as it was impossible to see the stimuli at this condition*

### 立体恒常模型：量化亮度-对比度-深度精度的关系

基于实验数据，作者拟合了一个将立体任务敏感度 $\beta$ 建模为对数亮度 $L$ 和对数对比度 $c$ 的二次函数：

$$\beta(c, L; \mathbf{w}) = w_1 L + w_2 c + w_3 L^2 + w_4 c^2 + w_5$$

模型参数通过最大后验估计（MAP）拟合，似然函数采用二项分布，并对二阶项参数施加高斯先验正则化（Table 1）。拟合结果（Figure 4蓝色曲线）与实验数据（红色星号）吻合良好。

![[assets/figures/papers/paper_list_l16_https_dark_stereo_mpi_inf_mpg_de/figures/004_Table_1.jpg]]
*Table 1: Estimated values of free parameters of (3) and the priors for the Maximum a Posteriori (MAP) estimation. Symbol "/" means that no prior was used*

该模型的核心价值在于可导出**等精度线**（equivalent-β lines, Figure 5实线）：在给定显示亮度下，维持相同深度感知精确度所需的对比度水平。与基于Kulikowski对比恒常模型的等感知对比度线（Figure 5虚线）相比，立体恒常模型在0.1–10 cd/m²低亮度区间要求**更强的对比度增强**。这从机制上解释了为何已有的对比度保持方法（如Wanat et al. 2014）不足以恢复低亮度下的立体深度感知——它们补偿的是对比度检测阈值，而非双目视差线索的可用性。

### VR主观验证：深度印象与偏好的双重优势

Experiment 2在VR头显中将所提方法、标准渲染（无增强）和Wanat et al.方法进行两两强制选择比较。9名不知情观察者（其中2名因立体视锐度测试不合格被排除）在暗室中以约5 cd/m²峰值亮度观看立体场景（Figure 10, 11），判断哪幅图像"更富三维感"以及"整体更偏好"。

结果（Figure 12）呈现高度一致性：

- **三维印象**：8/9（88.9%）的观察者认为本方法处理的图像比标准渲染更富三维感；同样8/9认为优于Wanat方法。
- **整体偏好**：同样88.9%的观察者整体更偏好本方法，无论对比对象是标准渲染还是Wanat方法。

95%置信区间远超50%随机猜测线，统计上具有显著性。值得注意的是，Wanat方法虽能增强局部对比度使图像更锐利（Figure 11特写），但其增强策略未针对立体深度线索优化，因而在三维印象上不及本方法。这直接验证了核心因果机制：**针对性补偿双目视差线索的精确度损失，比通用的对比度增强更有效地恢复低亮度下的深度感知**。

### 实验条件的公平性保障

两项实验均采取了严格的控制措施：实验顺序随机化；所有参与者通过立体视筛查，不适应者被排除；亮度切换时给予1分钟适应期；Experiment 2采用双选强制选择范式，参与者在不知实验目的的情况下完成判断（作者不参与Experiment 2）。这些措施排除了适应效应、实验者偏差和猜测策略对结论的干扰。

### 方法的适用边界与局限

论文明确指出了若干限制条件：

1. **亮度范围约束**：立体恒常模型仅在0.1–1000 cd/m²范围内校准，无法保证泛化至更低的暗视水平（scotopic levels）。当显示亮度低于0.1 cd/m²时，模型的预测能力未经实验验证。

2. **色调映射未纳入**：当前方法假设输入为线性亮度的渲染结果，未考虑色调映射（tone mapping）中对比度压缩对立体深度线索的二次影响。在HDR内容处理中，色调映射可能进一步降低可用视差信息，而本方法无法补偿这一损失。

3. **颜色外观未处理**：方法采用饱和度感知的颜色重建策略以避免过饱和，但未主动补偿极低亮度下可能出现的颜色畸变。实验参与者未报告颜色不适，但若需覆盖更宽亮度范围，可能需要结合颜色外观模型。

4. **峰值亮度依赖**：算法需要估计目标显示的峰值亮度作为输入参数，对不同显示设备的适应性需进一步标定。

5. **增强的副作用未知**：论文未系统评估对比度增强是否可能引入视觉不适或改变深度感知的绝对尺度。虽然主观偏好实验中未报告不适，但长期观看或极端参数下的影响有待研究。

### 未经验证的开放问题

分析显示以下关键问题缺乏实验证据支撑，需后续工作验证：

- 模型能否通过重新校准推广至暗视水平（<0.1 cd/m²）？
- 色调映射的对比度压缩如何定量影响立体深度感知，能否将其纳入统一的补偿框架？
- 方法在投影系统、移动VR等其他立体显示技术上的有效性如何？
- 增强后的对比度是否在长时间观看下引发视觉疲劳？

这些边界条件表明，Dark Stereo在当前形式下最适用于亮度可控的直视型立体显示器（如VR头显），且输入应为未经色调映射的线性渲染内容。

![[assets/figures/papers/paper_list_l16_https_dark_stereo_mpi_inf_mpg_de/figures/003_Figure_3.jpg]]
*Figure 3: Top: The photograph of a prototype stereo HDR display. Each observer sat at the display with their head stabilized by both the chin-rest and the head-rest. Note that the upper part of the display, intended for multi-focal-plane presentation, was not used in this project. Bottom: The schematic diagram of the display, showing the portion of the stereo display*

## 定位与知识库关联

### 问题域定位：低亮度下的双目深度线索退化

本文直面一个被长期忽视的感知瓶颈：显示亮度的下降会系统性地削弱双目视差深度线索的精确度，而非准确度。传统低亮度图像增强方法（如 Wanat and Mantiuk, ACM Trans. Graph. 2014）的优化目标始终锚定在**对比度检测阈值**上——即追求在不同亮度下维持主观感知对比度的恒定（Kulikowski 对比恒常模型）。本文的核心突破在于将优化目标从“看得见”迁移到“看得准”：**对比度增强的量不再由对比度匹配模型决定，而是由立体深度判断的精确度保持模型（stereo constancy model）决定**。这一目标函数的根本性转变，使得该方法在低亮度场景下对三维感知的恢复效果显著区别于所有基于对比度恒常性的增强方法。

### 改变的核心 Slot：从对比度恒常到立体恒常

相对已有工作的本质差异可精确定位为一个关键 slot 的替换：

| Slot | 基线方法（Wanat 等） | 本文方法 |
|------|---------------------|----------|
| **增强量的决定依据** | Kulikowski 对比度匹配模型：旨在使增强后的感知对比度与参考亮度下的感知对比度相等 | 自建的立体恒常模型：旨在使增强后的双目深度线索精确度（心理测量函数斜率 β）与参考亮度下相等 |

这一 slot 替换的因果链条清晰可追溯：心理物理实验（Experiment 1）首先建立了亮度 $L$ 和对比度 $c$ 到立体任务敏感度 $\beta$ 的映射关系 $\beta(c, L; \mathbf{w}) = w_1 L + w_2 c + w_3 L^2 + w_4 c^2 + w_5$；Figure 5 中的等 $\beta$ 线（实线）与 Kulikowski 模型的等感知对比度线（虚线）的对比直接揭示了关键差异——在 0.1–10 cd/m² 的亮度区间内，维持相同立体精确度所需的对比度增强远大于维持相同感知对比度所需的增强量。这意味着，**若仅追求对比度恒常，增强后的图像在低亮度下仍然会丢失大量的三维深度信息**。

### 知识库挂载点

本文可在以下知识库节点进行挂载：

1. **感知驱动的图像增强（Perception-based Image Enhancement）**：本文属于该领域的子类——基于心理物理模型的对比度增强。与现有工作（如 Wanat and Mantiuk 2014 基于 CSF 的增强、Mantiuk et al. 的显示自适应色调映射）共享“从人类视觉系统模型导出增强参数”的范式，但将感知建模的维度从对比度检测扩展到了双目深度感知。挂载时需注明：该方法的心理物理模型是**任务特异性的**（仅针对双目视差深度判断任务），并非通用视觉模型。

2. **立体视觉的感知模型（Perceptual Models of Stereopsis）**：本文建立了一个可计算的立体任务难度模型，量化了亮度和对比度对双目深度线索精确度的联合影响。该模型填补了现有立体视觉研究中“亮度-对比度-深度精度”三元关系缺乏量化描述的空白，可作为未来立体显示质量评估和渲染优化的基础模块。

3. **显示自适应渲染（Display-adaptive Rendering）**：该方法属于显示自适应后处理管线，输入为已渲染的立体图像对，输出为经对比度增强的适配低亮度显示的图像。与色调映射（tone mapping）形成互补——色调映射处理的是动态范围压缩问题，而本方法处理的是低亮度下的深度线索保持问题。论文明确指出，色调映射中的对比度压缩可能进一步削弱立体深度线索，但将二者的联合优化留作开放问题。

### 适用边界与限制

- **亮度校准范围**：立体恒常模型的参数仅在 0.1–1000 cd/m² 的亮度范围内通过心理物理实验校准（Table 1, MAP 估计）。低于 0.1 cd/m² 的暗视水平（scotopic vision）下，视锥细胞功能衰退、视杆细胞主导，模型无法保证泛化。论文将此列为明确的限制条件。
- **线索隔离假设**：实验刺激仅包含双目视差这一种深度线索（使用仅两阶灰度的程序化纹理消除纹理梯度等其他线索，Figure 2）。在真实场景中，多种深度线索共存且相互影响，模型的增强量是否在富线索场景下仍然最优，尚需验证。
- **颜色处理的简化**：颜色重建采用饱和度感知的灰度-彩色转换（Figure 9），避免增强引起颜色过饱和，但未建立完整的颜色外观模型。在极低亮度下可能出现的色度感知偏移（Purkinje shift）未被补偿。
- **显示技术依赖**：实验在高动态范围立体显示器上进行（Figure 3），算法依赖峰值亮度的准确估计。对投影系统、移动 VR 等其他立体显示技术的有效性需独立验证。

### 后续工作启发

论文留下的开放问题直接指向若干高价值研究方向：

1. **立体恒常模型的暗视扩展**：将心理物理实验扩展至 0.1 cd/m² 以下，建立覆盖暗视-明视全范围的统一模型，是理论上的自然延伸。

2. **色调映射与立体恒常的联合优化**：当前渲染管线中，色调映射通常先于本方法执行。色调映射中的局部对比度压缩可能不可逆地破坏双目深度线索，探索二者的联合优化框架（例如在色调映射阶段即考虑深度线索的保持）具有实际意义。

3. **多线索融合下的立体恒常**：在纹理、阴影、透视等额外深度线索存在的真实渲染场景中，立体恒常模型的增强量是否需要调整？是否存在线索间的补偿或掩蔽效应？这需要更接近真实应用的实验设计。

4. **颜色外观与立体感知的交互**：结合颜色外观模型（如 CIECAM02）同时补偿亮度下降引起的色度感知变化，可能进一步提升低亮度下的整体视觉体验质量。

5. **实时性能的进一步优化**：本方法基于 3 层拉普拉斯金字塔，已具备实时性，但在移动 VR 等算力受限平台上的部署可能需要更轻量的近似实现（如使用双边网格或引导滤波替代金字塔分解）。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Dark_Stereo_Improving_Depth_Perception_Under_Low_Luminance.pdf]]
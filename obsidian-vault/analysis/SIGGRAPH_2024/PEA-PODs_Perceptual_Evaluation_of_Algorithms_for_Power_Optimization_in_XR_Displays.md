---
title: "PEA-PODs: Perceptual Evaluation of Algorithms for Power Optimization in XR Displays"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/PEA_PODs_Perceptual_Evaluation_of_Algorithms_for_Power_Optimization_in_XR_Displays.pdf
project_link: null
code_link: "https://github.com/NYU-ICL/pea-pods"
aliases:
- PP
- PEA-PODs
tags:
- SIGGRAPH_2024
- topic/benchmarks_datasets_evaluation
core_operator: 显示映射方法的选择及其调制强度参数α（通过线性缩放、裁剪、滚降等操作调整像素值或色度），直接控制功耗节省幅度与感知失真程度。
primary_logic: 通过大规模主观实验将六种显示映射技术的感知失真统一量化为JOD分数，结合硬件实测功耗模型构建JOD-功耗转换函数，首次实现跨显示类型和眼动模态的定量质量-功耗折衷分析，直接指导XR功耗预算。
claims:
- 主观实验数据被缩放到统一的JOD感知单位，使不同方法的视觉质量可直接比较。
- 构建了JOD与功耗节省百分比的转移函数，并在验证实验中与用户偏好高度一致（Spearman r=0.943, p<.005 对于20%节能目标；r=0.999, p<<.001 对于40%节能目标）。
- 亮度滚降（Brightness Rolloff）在眼动追踪下提供最大的节能（OLED上达到38.5%@-1JOD），远超统一调光等其他方法。
- "OLED display with eye tracking (Bino+ET), target -1 JOD 上 Power saved (%) at -1 JOD perceptual quality loss = Brightness Rolloff: 38.5%"
---

# PEA-PODs: Perceptual Evaluation of Algorithms for Power Optimization in XR Displays

> [!tip] 核心洞察
> 通过大规模主观实验将六种显示映射技术的感知失真统一量化为JOD分数，结合硬件实测功耗模型构建JOD-功耗转换函数，首次实现跨显示类型和眼动模态的定量质量-功耗折衷分析，直接指导XR功耗预算。

| 字段 | 内容 |
|------|------|
| 中文题名 | PEA-PODs：面向XR显示器功耗优化算法的感知评估 |
| 英文题名 | PEA-PODs: Perceptual Evaluation of Algorithms for Power Optimization in XR Displays |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://kenchen10.github.io/projects/sig24/index.html) · [Code](https://github.com/NYU-ICL/pea-pods) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | PEA-PODs 统一感知评估框架 |
| Dataset | OLED display with eye tracking (Bino+ET), target -1 JOD, OLED display without eye tracking (Monocular), target -1 JOD, Local dimming LC display with eye tracking (Mono+ET), target -1 JOD |

> [!tip] 效果简介
> - OLED display with eye tracking (Bino+ET), target -1 JOD 上，Power saved (%) at -1 JOD perceptual quality loss Brightness Rolloff: 38.5% vs Uniform Dimming: 20.2% (+18.3 percentage points)。
> - OLED display without eye tracking (Monocular), target -1 JOD 上，Power saved (%) at -1 JOD Uniform Dimming: 20.2% vs Whitepoint Shift: 2.01% (+18.19 percentage points)。
> - Local dimming LC display with eye tracking (Mono+ET), target -1 JOD 上，Power saved (%) at -1 JOD Brightness Rolloff: 33.7% vs Uniform Dimming: 20.2% (+13.5 percentage points)。

## 概要

XR显示器功耗优化面临一个根本性困境：显示映射算法能节省功耗，但会引入视觉失真，而二者之间的定量折衷关系从未在统一感知尺度上被标准化——这使得不同显示架构（OLED、全局/局域调光LCD）和眼动追踪条件下的架构决策缺乏公平比较的依据。

本文提出**PEA-PODs**统一感知评估框架，核心思路是将六种显示功耗优化技术（均匀调光、亮度裁剪、亮度滚降、双眼交替调光、白点偏移、色觉中心凹映射）的感知失真，通过大规模主观实验缩放到统一的**JOD**（恰可察觉差异）尺度，再结合硬件实测功耗模型，构建出**JOD-功耗节省转移函数**，首次实现跨显示类型和眼动模态的定量质量-功耗折衷分析。

主要发现包括：(1) 在眼动追踪OLED上，亮度滚降在-1 JOD感知损失下可实现**38.5%**的功耗节省，远超均匀调光的20.2%；(2) 转移函数预测与独立验证实验的用户偏好高度一致（Spearman r=0.943, p<.005 @20%节能；r=0.999, p<<.001 @40%节能）；(3) 若计入眼动追踪仪自身功耗，非眼动追踪的均匀调光或双眼交替调光可能反超亮度滚降。

方法定位上，PEA-PODs并非提出新的显示映射算法，而是为现有技术建立了一个标准化的感知质量-功耗评估基准，可直接指导XR系统的功耗预算决策。

## 核心方法与创新机理

PEA-PODs 的核心贡献在于构建了一套**统一的感知评估框架**，首次将不同显示映射技术的视觉质量缩放到同一把“感知尺子”——JOD（Just-Objectionable-Difference，恰可察觉差异）上，并与硬件实测功耗模型耦合，形成跨显示架构、跨眼动模态的定量质量-功耗折衷分析工具。

### 问题的唯一瓶颈

XR 头显的续航焦虑本质上是显示功耗与视觉体验之间的折衷问题。然而，现有功耗优化技术（均匀调暗、亮度裁剪、边缘滚降、色适应白点偏移等）各自在完全不同的实验条件、度量标准和设备上被评估，导致架构师无法回答一个根本性问题：**在可接受的感知质量损失下，哪种技术省电最多？** 这个瓶颈源于三个层面的“不可通约性”：

1. **感知质量的度量不统一**：不同研究使用不同的主观评分量表、阈值检测任务或客观指标（PSNR、SSIM），彼此无法直接比较。
2. **功耗节省的计算基准不同**：有的以面板理论功耗计算，有的以整机电池寿命推算，缺乏统一的硬件功耗模型。
3. **观看条件不匹配**：眼动追踪的有无、单目/双目显示模式、显示面板技术（OLED vs. LC）均影响省电技术的实际效果，但缺乏系统性的交叉比较。

PEA-PODs 的因果调节旋钮是**显示映射方法的选择及其调制强度参数 α**——通过线性缩放、裁剪、滚降或色度偏移等操作调整像素值或白点，直接控制功耗节省幅度与感知失真程度。框架的核心洞察在于：将六种技术的感知失真统一量化为 JOD 分数，结合硬件实测功耗模型构建 JOD-功耗转换函数，使跨技术、跨显示类型的定量决策成为可能。

### 框架的模块化架构与因果关系链

PEA-PODs 的评估管线由五个顺序耦合的模块组成，每个模块的输出作为下一模块的输入，形成一条从物理测量到决策函数的完整因果链：

```
硬件功耗测量与建模 → 显示映射方法与α调制 → 大规模主观实验(2IFC+ASAP) → JOD感知质量缩放 → JOD-功耗转移函数
```

#### 模块一：硬件功耗测量与建模

该模块解决“功耗节省”的量化基准问题。研究者对两款商用 XR 头显——**OLED 面板的 HTC Vive Pro Eye** 和**局域调光 LC 面板的 Meta Quest Pro**——进行了实际功耗测量，通过在分流电阻上测量电压降获得精确的像素级功耗数据，并回归出解析功耗模型。

**OLED 功耗模型**（Equation 5）将总功耗表达为各像素色值的线性加权和：

$$\mathcal{P}(\mathcal{I}) = \sum_{\mathbf{c} \in \mathcal{I}} \mathbf{p}^{\intercal} \mathbf{c} + \delta$$

其中 $\mathbf{p}$ 是由 RGB 三原色发光效率决定的权重向量，$\delta$ 为静态偏置功耗。这一线性结构意味着 OLED 的功耗直接正比于像素亮度和颜色——蓝色子像素效率最低，功耗权重最高。

**LC 显示功耗模型**更为复杂，需要分别建模液晶面板（LC）和背光单元（BLU）：

- **BLU 功耗**（Equation 1）随相对亮度 $y$ 线性变化：$\mathcal{M}_{\mathcal{B}}(y) = \alpha y + \delta$，回归拟合的 $r^2$ 达到 0.99。
- **LC 面板功耗**（Equation 2）由 RGB 三通道的二次多项式之和建模：$M_{\mathrm{LC}}(\mathbf{c}) = \sum_{p=0}^{3} \alpha_{p} \mathbf{c}_{p}^{2} + \delta_{p}$，模型拟合 RMSE 为 0.31，MAPE 仅 0.92%。

**全局调光模式**下的总功耗（Equation 3）为 BLU 最大驱动所需功耗与所有像素 LC 功耗之和：

$$\mathcal{P}(\mathcal{I}) = \mathcal{M}_{\mathcal{B}}(\max\{\mathbf{c} : \mathbf{c} \in \mathcal{I}\}) + \sum_{\mathbf{c} \in \mathcal{I}} \mathcal{M}_{\mathrm{LC}}(\mathbf{c})$$

这一公式揭示了全局调光 LC 的关键特征：BLU 功耗由图像中最亮的像素决定，因此仅降低暗区像素无法减少背光功耗。**局域调光模式**则通过将背光分区独立控制，使 BLU 功耗变为各分区最大值之和，为亮度滚降等空间差异化技术提供了硬件基础。

该模块的因果作用：**将显示映射的输出（像素值）转化为可量化的功耗节省百分比**，是后续 JOD-功耗转移函数的物理基础。

#### 模块二：显示映射方法与调制因子 α

框架集成了六种显示功耗优化技术，每种技术通过统一的调制因子 $\alpha \in [0, 1]$ 控制强度——$\alpha = 0$ 表示无修改（参考图像），$\alpha$ 越大表示修改越强、省电越多但失真也越大。这一设计使不同技术可以在统一的“强度轴”上进行比较。

**1. 均匀调暗（Uniform Dimming）**
最基础的技术，对所有像素进行线性缩放（Equation 6）：
$$\mathbf{c}' = (1 - \alpha) \mathbf{c}$$
其因果机制是全局降低发光强度，功耗节省与 $\alpha$ 成正比，但感知失真表现为整体亮度下降和对比度压缩。

**2. 亮度裁剪（Luminance Clipping）**
仅裁剪亮度超过阈值 $(1-\alpha)$ 的像素（Equation 7）：
$$\mathbf{c}' = (1 - \alpha) \frac{\mathbf{c}}{\mathbf{y}(\mathbf{c})}, \text{ if } \mathbf{y}(\mathbf{c}) > (1 - \alpha)$$
该技术保持色调不变，但牺牲高光区域的细节和亮度。其因果逻辑在于：高亮像素功耗占比大，裁剪它们能以较小的图像面积换取较大的功耗节省，但代价是产生可见的高光剪切伪影。

**3. 亮度滚降（Brightness Rolloff）**
基于视网膜离心率 $\phi$ 的高斯型边缘调暗（Equation 8）：
$$\mathbf{c}' = \exp\left(\frac{4\ln(1-\alpha)}{(\mathrm{FOV} - \theta)^2} \phi^2\right) \mathbf{c}$$
其中 $\theta$ 定义了保持不变的中央窝区域大小。该技术要求眼动追踪以确定注视点，其因果优势在于：人眼对边缘视场的亮度/细节敏感度低，因此可在几乎不被察觉的情况下大幅降低边缘像素功耗。这是感知驱动的空间差异化节能。

**4. 双眼交替调暗（Dichoptic Dimming）**
仅调暗左眼显示的图像，利用双眼融合效应——大脑会将双眼图像融合，感知亮度约为两眼的平均值，但功耗仅降低了一只眼。这是双目视觉机制驱动的节能策略，不需要眼动追踪。

**5. 白点偏移（Whitepoint Shift）**
根据全图平均色 $\overline{\mathbf{c}}$ 计算功耗最优的白点（Equation 11）：
$$\mathbf{w}' = \mathbf{w} + \alpha \left( f(\overline{\mathbf{c}}, 0) - \overline{\mathbf{c}} \right)$$
然后通过 Bradford 色适应变换矩阵 $\mathbf{M}_{\mathrm{A}} = \mathbf{B}^{-1} \mathbf{diag}(\gamma' \oslash \gamma) \mathbf{B}$ 将整幅图像映射到新白点下。其因果机制利用了发光效率的波长依赖性——蓝色子像素效率低、功耗高，将白点向黄绿方向偏移可降低功耗，而人眼色适应机制可在一定程度上补偿颜色变化。

**6. 色觉中心凹映射（Color Foveation）**
在感知不可区分的颜色集合 $\mathcal{M}_{\Theta}(\mathbf{c}, \phi)$ 中寻找功耗最小的颜色（Equation 9）：
$$f : (\mathbf{c}, \phi) \mapsto \operatorname*{argmin}_{x \in \mathcal{M}_{\Theta}(\mathbf{c}, \phi)} \mathcal{P}(x)$$
该技术要求眼动追踪，利用边缘视场对色度差异不敏感的特性，在边缘区域用低功耗颜色替换高功耗颜色。

这六种技术的 **changed slot** 可归纳为三个维度：
- **空间均匀性**：均匀调暗和白点偏移是全局操作；亮度裁剪是半全局（仅影响高亮区）；亮度滚降和色觉中心凹映射是空间差异化操作，需要眼动追踪。
- **处理域**：亮度域（均匀调暗、亮度裁剪、亮度滚降、双眼交替调暗）vs. 色度域（白点偏移、色觉中心凹映射）。
- **双目策略**：单目一致（均匀调暗、亮度裁剪、白点偏移）vs. 双眼差异化（双眼交替调暗）vs. 眼动追踪驱动（亮度滚降、色觉中心凹映射）。

#### 模块三：大规模主观实验（2IFC + ASAP 主动采样）

实验采用**双间隔强制选择任务（2IFC）** 的成对比较范式：每次呈现一对图像（参考 vs. 处理后），参与者判断哪一幅更接近参考图像。这种设计比绝对评分更敏感，能检测到微小的感知差异。

关键创新在于使用了 **ASAP（Active Sampling via Attraction Probability）主动采样策略**：系统根据所有历史响应实时计算每对未测试比较的期望信息增益，优先选择最能降低模型不确定性的比较对。这使实验效率大幅提升——无需对所有可能的条件组合进行全因子测试，而是将采样集中在最有信息量的比较上。

实验在 **自然图像和自由观看条件**下进行，这区别于传统心理物理实验中使用人工刺激（如 Gabor 光栅、均匀色块）的做法。自由观看意味着参与者可以自由移动视线，这对于评估亮度滚降和色觉中心凹映射等眼动追踪技术的真实效果至关重要——如果强制注视，会低估这些技术在实际使用中的感知失真。

#### 模块四：JOD 感知质量缩放

成对比较数据通过 **Thurstone Case V 模型**的贝叶斯极大似然估计缩放到统一的 JOD 尺度。Thurstone 模型假设每个刺激的感知质量服从正态分布，成对比较的胜负概率由两分布均值之差决定。JOD 定义为恰好可察觉的感知差异单位——1 JOD 对应约 75% 的正确辨别率。

这一缩放步骤是框架的“统一度量衡”核心：它将不同技术、不同 $\alpha$ 强度下的原始比较数据映射到同一把感知尺子上，使“亮度滚降在 $\alpha=0.3$ 时的失真”与“白点偏移在 $\alpha=0.5$ 时的失真”可以直接比较。ANOVA 分析验证了实验设计的敏感性——显示映射技术类型（$F=23.49, p \ll .001$）和调制强度（$F=35.67, p \ll .001$）均对 JOD 分数有显著影响。

#### 模块五：JOD-功耗转移函数构建

这是框架的最终输出——将模块四的 JOD 分数与模块一的硬件功耗模型耦合，形成 **JOD vs. 功耗节省百分比**的转移函数。具体做法是：对每种技术在每个 $\alpha$ 值下，计算处理图像相对于原图的功耗节省百分比，然后与对应的 JOD 分数配对，拟合出平滑曲线。

转移函数的因果价值在于**实现跨技术、跨显示类型的定量决策**。例如，给定“可接受 -1 JOD 的感知质量损失”这一约束，可以直接从转移函数上读取每种技术在 OLED、全局调光 LC、局域调光 LC 以及不同眼动模态下的功耗节省百分比，形成类似 Table 1 的排名表。

### 验证实验的因果闭环

为验证转移函数的预测有效性，研究者进行了独立验证实验：设定 20% 和 40% 两个功耗节省目标，用转移函数反推各技术所需的调制强度，然后收集用户对这些处理图像的偏好评分。**Spearman 秩相关分析**显示转移函数预测的 JOD 分数与验证实验收集的 JOD 分数高度正相关（20% 节能目标：$r=0.943, p<.005$；40% 节能目标：$r=0.999, p \ll .001$），证实了 JOD-功耗转换函数的可靠性。

### 关键公式变量含义汇总

| 符号 | 含义 | 所属模型 |
|------|------|----------|
| $\alpha$ | 调制强度因子，$\in [0,1]$ | 所有显示映射 |
| $\mathbf{c}$ | 像素 RGB 三通道色值 | 功耗模型与映射 |
| $\mathbf{y}(\mathbf{c})$ | 像素亮度（luminance） | 亮度裁剪 |
| $\phi$ | 视网膜离心率（视角） | 亮度滚降 |
| $\theta$ | 中央窝保持不变的区域大小 | 亮度滚降 |
| $\mathbf{p}$ | OLED 原色功耗权重向量 | OLED 功耗模型 |
| $\mathbf{w}, \mathbf{w}'$ | 原始/偏移后白点色度坐标 | 白点偏移 |
| $\mathcal{M}_{\Theta}$ | 感知不可区分的颜色集合 | 色觉中心凹映射 |
| $\mathcal{K}(\lambda)$ | 发光效率代理函数，$\propto \eta(\lambda)V(\lambda)$ | 功耗最优颜色搜索 |

## 实验与关键发现

PEA-PODs 的核心实验设计遵循“测量-建模-感知-转换-验证”的链条。首先对两款商用XR头显（OLED: HTC Vive Pro Eye；局域调光LC: Meta Quest Pro）进行硬件功耗测量与回归建模，得到像素颜色到功耗（mW）的分析模型（Figure 3），然后对六种显示映射技术在三个调制强度水平下进行大规模主观实验，将成对比较数据缩放到统一的JOD感知尺度，最后将JOD分数与硬件功耗模型结合，构建JOD-功耗节省转移函数（Figure 7），并在独立验证实验中检验其预测有效性。

![[assets/figures/papers/paper_list_l29_https_kenchen10_github_io_projects_sig24_index_html/figures/009_Table_1.jpg]]
*Table 1: Power saving rankings at -1 JOD. The transfer functions in Figure 7 were evaluated for each method at -1 JOD for common XR display types, including non eye-tracked (ET) as well as eye-tracked monocular and binocular displays. Colors represent power saving rankings for a column, blacked out cells are techniques which do not apply to the specific display modality, and grey cells are methods which save near-zero power*

![[assets/figures/papers/paper_list_l29_https_kenchen10_github_io_projects_sig24_index_html/figures/004_Figure_3.jpg]]
*Figure 3: LC display power models. A visualization of the LC (left) and backlight unit (BLU, right) power models. Points show physical measurements, and dashed curves are regressed model fits*

![[assets/figures/papers/paper_list_l29_https_kenchen10_github_io_projects_sig24_index_html/figures/008_Figure_7.jpg]]
*Figure 7: Perceptual Impact (JODs) vs. Power Savings (%). Using the hardware-accurate power models described in Section 3 and the user study data, we fit transfer functions of JODs vs. % power savings for each display mapping for three different display types – OLED, global and local dimming LC. Shaded regions represent 95% confidence intervals of percentage power savings; horizontal and vertical error bars represent 95% confidence intervals of JOD scores and power savings, respectively. Note that methods like uniform and dichoptic dimming are content-independent and thus do not exhibit any vertical error bars*

### 主实验结果：-1 JOD下的功耗节省排名

Table 1 汇总了在-1 JOD（即可感知但轻微的质量损失）条件下各技术的功耗节省百分比，这是跨技术公平比较的核心基准。关键发现如下：

**眼动追踪条件下，亮度滚降（Brightness Rolloff）在所有显示类型上均提供最大节能。** 在OLED+双眼眼动追踪（Bino+ET）配置下，亮度滚降达到 **38.5%** 的功耗节省，而传统均匀调光（Uniform Dimming）仅为 **20.2%**，前者相对提升 **18.3个百分点**。在局域调光LC+单眼眼动追踪（Mono+ET）下，亮度滚降为 **33.7%**，同样远超均匀调光的20.2%（+13.5个百分点）。这一优势来源于亮度滚降的空间选择性——它仅在视网膜离心率增大时指数衰减亮度（公式8），而中心窝区域保持原样，因此感知失真极低，允许在相同JOD预算下施加更强的调制。

**非眼动追踪条件下，均匀调光是最优的通用选择。** 在OLED单眼（Monocular）配置下，均匀调光以 **20.2%** 的节能领先于其他非眼动追踪技术，白点偏移（Whitepoint Shift）仅达 **2.01%**，亮度裁剪（Luminance Clipping）为 **12.2%**。均匀调光的线性缩放（公式6）虽然简单，但在无空间选择性时，其失真均匀分布在整幅图像上，反而在给定JOD预算下比局部高光裁剪或全局色适应更可接受。

**双眼交替调光（Dichoptic Dimming）在非眼动追踪下表现意外强劲。** 该技术仅调暗左眼图像，在OLED单眼配置下达到 **19.7%** 的节能，接近均匀调光。其机理是利用双眼融合——大脑将左右眼亮度平均，感知亮度下降约一半，但功耗节省接近均匀调光水平。

### JOD-功耗转移函数的构建与验证

Figure 7 的核心贡献是将感知质量与功耗节省直接挂钩。对于每种显示映射技术，研究者在三个显示类型（OLED、全局调光LC、局域调光LC）和三种眼动模态（无眼动追踪、单眼+ET、双眼+ET）下拟合了JOD vs. 功耗节省百分比的转移函数。

转移函数的有效性通过独立验证实验得到确认。研究者设定20%和40%两个节能目标，利用转移函数预测各技术对应的JOD分数，再与验证实验中收集的用户偏好进行Spearman秩相关分析。结果显示：
- **20%节能目标**：预测JOD与实测用户偏好高度相关，**Spearman r = 0.943, p < .005**；
- **40%节能目标**：相关性近乎完美，**Spearman r = 0.999, p << .001**。

这一结果强有力地证明，转移函数能够准确预测不同节能幅度下的相对感知质量排序，为架构师提供了直接可用的决策工具——给定功耗预算，即可查询各技术的预期感知质量。

### 关键消融与敏感性分析

**ANOVA分析确认实验设计的敏感性。** 对主观评分数据的方差分析表明，显示映射技术类型（F=23.49, p<<.001）和调制强度（F=35.67, p<<.001）均对感知质量有极显著影响，无显著交互效应。这说明：① 实验能够可靠区分不同技术间的质量差异；② 调制强度的三个水平设置合理，覆盖了从接近阈值到明显可见失真的范围。

**Pilot实验验证了调制强度校准的有效性。** 预实验采用QUEST自适应阶梯法确定均匀调光的1 JND阈值（α=0.171, 75%检测率），随后Pilot实验通过线性拟合将各技术的调制强度校准到1、2、3 JOD目标水平（Figure 5）。这一校准过程确保了主实验中不同技术的刺激强度在感知上可比，避免了因强度设置不当导致的排名偏差。

### 失败模式与适用边界

**眼动追踪功耗可颠覆技术排名。** Figure 9 的分析表明，若将眼动追踪仪自身功耗（估算约100-190mW）计入总系统功耗，亮度滚降的优势可能被完全抵消。在计入眼动仪开销后，非眼动追踪的均匀调光或双眼交替调光在总功耗节省上反而可能优于亮度滚降。这一发现直接警告：**眼动追踪相关技术的节能优势高度依赖眼动仪本身的能效**，在低功耗眼动仪可用之前，不应盲目采用。

**亮度裁剪的高光细节丢失是主要感知代价。** 虽然亮度裁剪在-1 JOD下可节省12.2%（OLED单眼），但其失真机制是直接裁剪超过阈值的高光区域（公式7），导致高光细节完全丢失。这在自然图像中可能不可接受，尤其是当高光区域包含重要视觉信息时。转移函数仅量化了失真的“可感知幅度”，而未区分失真类型（亮度损失 vs. 细节丢失 vs. 色偏），这是框架的一个已知局限。

**白点偏移的节能潜力极低。** 在-1 JOD下，白点偏移在所有配置中仅节省2.01%-2.41%，远低于其他技术。其根本原因在于，色适应虽然允许白点在一定范围内偏移而不引起强烈不适，但显示器的原色效率差异有限，通过白点偏移可获得的功耗降低空间本身很小。该技术更适合作为辅助手段与其他技术组合使用，而非独立方案。

**设备依赖性与可迁移性未知。** 所有功耗模型和JOD-功耗转移函数均基于两款特定头显测量，结果对其他显示技术（如mini/micro-LED、LCOs）的可迁移性未经验证。例如，OLED的功耗模型为像素值的线性加权和（公式5），而LC模型包含BLU的全局调光非线性（公式3），不同显示技术的功耗特性差异巨大，转移函数的形式和排名可能完全不同。

**静态图像实验的生态效度限制。** 实验采用静态自然图像和2IFC主观评分任务，参与者在自由观看条件下判断哪幅图像更接近参考图。在动态视频、游戏渲染或任务型XR应用中，用户的注意力分配和失真敏感度可能显著不同，转移函数的预测准确性需要进一步验证。此外，显示映射算法产生的伪影（如亮度滚降的边缘渐暗、亮度裁剪的高光丢失）可能影响视觉舒适度和临场感，但本研究仅测量了可见失真的幅度，未评估这些高阶感知维度。

![[assets/figures/papers/paper_list_l29_https_kenchen10_github_io_projects_sig24_index_html/figures/006_Figure_5.jpg]]
*Figure 5: Pilot Study. We conducted a pre-pilot to set initial magnitude values for each display mapping. The left plot shows the stimuli magnitudes as scheduled by QUEST, and the right plot shows the psychometric fit to the user responses (P1). The dashed line represents 75% detection (1 JND)*

![[assets/figures/papers/paper_list_l29_https_kenchen10_github_io_projects_sig24_index_html/figures/010_Figure_8.jpg]]
*Figure 8: Display primary optimization. (Left) Display primaries which introduce non-zero power savings are plotted, with average color difference (CIEDE2000*

![[assets/figures/papers/paper_list_l29_https_kenchen10_github_io_projects_sig24_index_html/figures/011_Figure_9.jpg]]
*Figure 9: Eye tracker power consumption. We conduct an analysis of gaze-contingent power-saving techniques, while considering estimations of eye tracker power consumption. Solid lines represent power saved for three methods (brightness rolloff, uniform dimming, and dichoptic dimming), and the dotted line represents the difference in power saved between brightness rolloff and the next best method with the same perceptual impact*

## 定位与知识库关联

PEA-PODs 的核心定位是**为 XR 显示器功耗优化算法建立第一个跨显示架构、跨眼动模态的统一感知质量-功耗折衷标准**。此前领域的状态是：各类显示映射技术（均匀调光、亮度裁剪、边缘调暗等）各自在特定设备和受控条件下被提出，但彼此之间缺乏可比较的感知质量度量，导致架构师无法在 OLED、全局调光 LC、局域调光 LC 以及眼动追踪有无之间做出有依据的功耗预算决策。

### 相对于已有方法的本质差异：改变的是哪个 slot

已有方法（如 **Uniform Dimming** (Choi et al., 2002; Gatti et al., 2002)、**Luminance Clipping** (Kerofsky and Daly, 2006)、**Brightness Rolloff** (Kim and Lee, 2020)、**Color Foveation** (Duinkharjav et al., 2022b)、**Whitepoint Shift** (Dong and Zhong, 2011a; Luo et al., 2000)）各自定义了从输入图像到输出像素值的映射函数，并通常以峰值信噪比或自设的感知阈值来评估失真。这些工作改变的 slot 是**显示映射算子本身**——即给定目标功耗节省量，如何设计一个产生最小可见伪影的像素变换。

PEA-PODs 并不提出新的映射算子，而是改变了一个**更上层的 slot：评估与决策框架**。具体而言，它将问题从“设计更好的映射函数”转置为“给定一组候选映射函数，如何在统一的感知尺度上量化其质量-功耗折衷，从而支持跨技术和跨硬件的架构决策”。这个 slot 的输入是多种候选显示映射技术及其调制参数 α，输出是 JOD（just-objectionable-difference）感知质量分数与功耗节省百分比之间的转移函数。该 slot 在已有文献中几乎为空——此前不存在将主观感知评分缩放到统一 JOD 单位并与硬件实测功耗模型耦合的标准化流程。

### 知识库挂载点

PEA-PODs 可挂载到以下知识库节点：

1. **感知质量评估方法**：采用 Thurstone Case V 模型下的贝叶斯极大似然估计将成对比较数据缩放到 JOD 尺度，这与图像/视频质量评估领域的标准化实践（如 ITU-R BT.500 建议的主观实验方法）兼容。主动采样策略 ASAP (Mikhailiuk et al., 2021) 的引入使大规模成对比较实验在有限试验次数下仍能获得稳健的感知分数估计。

2. **显示功耗建模**：对 OLED 和 LC（全局/局域调光）两类主流 XR 显示架构建立了从像素颜色到功耗（mW）的分析模型。OLED 模型采用各原色通道的线性加权和（Equation 5），LC 模型则分离背光单元（BLU）的线性模型（Equation 1）和液晶面板的二次多项式模型（Equation 2）。这些模型可被后续研究直接复用或扩展至新型显示技术。

3. **XR 系统功耗优化**：该框架输出的 JOD-功耗转移函数可直接嵌入 XR 系统的功耗管理策略中——例如，给定目标功耗预算或目标感知质量上限，自动选择最优显示映射技术及其调制强度。这构成了显示子系统的功耗-质量 Pareto 前沿。

### 适用边界

PEA-PODs 的适用边界需严格注意以下几点：

- **硬件依赖性**：功耗模型基于 Meta Quest Pro（LC）和 HTC Vive Pro Eye（OLED）两款特定头显测量得到，对 mini/micro-LED、LCOs 等新兴显示技术的可迁移性未经验证。若需应用于其他设备，必须重新进行硬件功耗测量和模型回归。

- **静态图像假设**：感知实验使用自然图像和静态 VR 场景，结果不直接适用于动态视频或交互式渲染内容。动态场景中的时域掩蔽效应可能改变各技术的感知失真强度排序。

- **眼动追踪功耗未计入主分析**：主结果（Table 1, Figure 7）未包含眼动追踪仪自身的功耗（估算约 100–190 mW）。当计入该开销后，非眼动追踪的均匀调光或双眼交替调光（Dichoptic Dimming）可能比亮度滚降更优（Figure 9），这改变了技术排名。

- **算法变体空间未穷尽**：仅评估了六种固定版本的显示映射技术，未探索不同滚降剖面、多技术组合或端到端可微优化。不同参数化可能产生不同的 JOD-功耗曲线。

### 后续启发与可跟进方向

1. **新型显示技术的功耗-质量标定**：将 PEA-PODs 框架复制到 micro-LED、LCOs、全息显示等新兴架构上，建立对应的功耗模型和 JOD 转移函数，扩展知识库的硬件覆盖范围。

2. **动态内容的感知标定**：设计面向视频和交互式内容的感知实验，检验静态图像下获得的转移函数是否在时域场景中保持一致性，或是否需要内容自适应的 JOD 修正。

3. **眼动追踪联合优化**：鉴于眼动仪自身功耗可能抵消亮度滚降的优势，存在一个开放问题——能否联合优化亮度滚降剖面和眼动追踪采样策略，使系统总功耗（显示 + 眼动追踪）达到全局最优。

4. **多原色显示与颜色映射的联合设计**：Figure 8 展示了显示器原色优化可在低色差（ΔE*）下获得额外功耗节省。将原色选择与白点偏移、色觉中心凹映射等技术联合优化，有望同时提升色域、色准和能效。

5. **端到端可微功耗-质量模型**：当前框架依赖大规模主观实验来获得 JOD 分数。若能训练一个可微的感知质量预测器，并与功耗模型耦合，则可通过梯度优化直接求解给定功耗预算下的最优显示映射参数，大幅降低实验成本。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/PEA_PODs_Perceptual_Evaluation_of_Algorithms_for_Power_Optimization_in_XR_Displays.pdf]]
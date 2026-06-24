---
title: "Dual Band Thermal Videography: Separating Time-Varying Reflection and Emission Near Ambient Conditions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dual_Band_Thermal_Videography_Separating_Time_Varying_Reflection_and_Emission_Near_Ambient_Conditions.pdf
project_link: "https://dual-band-thermal.github.io"
code_link: null
aliases:
- DBTVD
- DBTVSTVRENAC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 双波段光谱比率（材料发射率比值固定）与时间动态差异（物体温度平滑变化、背景反射突变）的结合，为欠定系统提供额外约束。
primary_logic: 物体温度演化遵循热传导方程，呈平滑指数规律；背景反射与物体温度变化不相关。利用静态像素微分比（k1）与动态场景残差比（k2）可解耦双波段发射率，进而重构物体与背景温度。
claims:
- 双波段光谱比与时间平滑先验的结合可有效分离近环境场景的发射与反射。
- 本文方法在中等噪声水平的仿真中显著优于基线（BCP、双波长高温计、朴素最小二乘）。
- 真实视频实验表明，未标定方法的物体温度估计误差仅为1.72%~5.34%，远低于朴素最小二乘的31.68%~45.5%。
- 标定发射率与ECOSTRESS谱库及FLIR反射器方法一致，对低发射率材料精度更优。
---

# Dual Band Thermal Videography: Separating Time-Varying Reflection and Emission Near Ambient Conditions

> [!tip] 核心洞察
> 物体温度演化遵循热传导方程，呈平滑指数规律；背景反射与物体温度变化不相关。利用静态像素微分比（k1）与动态场景残差比（k2）可解耦双波段发射率，进而重构物体与背景温度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 双波段热成像视频分析：分离近环境条件下时变的反射与辐射 |
| 英文题名 | Dual Band Thermal Videography: Separating Time-Varying Reflection and Emission Near Ambient Conditions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.11334) · [Project](https://dual-band-thermal.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Dual Band Thermal Videography (DBVT) |
| Dataset | Simulated thermal videos, Real wineglass video, Real coffee pot video, Emissivity estimation |

> [!tip] 效果简介
> - Simulated thermal videos (ECOSTRESS spectral library materials) 上，RMSE of object temperature 显著低于所有基线 vs BCP, dual-wavelength, naive LS (中等噪声下大幅降低错误（log scale）)。
> - Real wineglass video 上，T_o估计误差百分比 (vs thermocouple) 1.72% vs naive LS: 31.68% (-29.96%)。
> - Real coffee pot video 上，T_o估计误差百分比 5.34% vs naive LS: 45.5% (-40.16%)。

## 概述

热像仪在近环境温度场景下面临一个根本性欠定问题：物体自身的热辐射与来自周围环境的背景反射在强度上相当，且两者均随时间变化。传统方法依赖灰体假设（发射率与波长无关）或背景静止假设，无法有效分离这两种信号。**DBVT**（Dual Band Thermal Videography）通过将双波段光谱比率与时间动态先验相结合，为这一欠定系统引入额外约束，实现了逐像素的发射-反射分离。

**核心瓶颈**：近环境温度下，物体发射与背景反射的时变信号相互耦合，单波段观测无法区分。传统双波长高温计（Tsai et al., Int. J. Thermophysics 1990）忽略背景辐射，**BCP**（Grimming et al., Optical Engineering 2023）依赖局部黑体假设，均未充分建模时变背景。

**因果调节变量**：双波段光谱比率（材料发射率比值 $k_1 = \epsilon_2 / \epsilon_1$ 固定）与时间动态差异（物体温度受热传导方程约束呈平滑指数变化，背景反射可突变且与物体温度不相关）的结合，为欠定系统提供了可解耦的自由度。

**核心洞察**：静态背景像素处的双波段时域导数比为定值 $k_1$，去除平滑发射主导信号后的残差比为定值 $k_2 = (1-\epsilon_2)/(1-\epsilon_1)$。由 $k_1$ 和 $k_2$ 可解析求解双波段发射率，进而重构物体与背景温度。

**主要结果**：
- 仿真实验中，DBVT 在中等噪声水平下显著优于 BCP、双波长高温计和朴素最小二乘法（Figure 2）。
- 真实视频实验中，未标定方法的物体温度估计误差仅为 1.72%（酒杯）和 5.34%（咖啡壶），远低于朴素最小二乘的 31.68% 和 45.5%（Figure 6）。
- 标定发射率与 ECOSTRESS 谱库及 FLIR 反射器法一致，对低发射率材料（如铬球，参考值 0.1）精度更优（Table 2）。

**方法定位**：DBVT 属于“非灰体双波段 + 时域平滑先验”的物理驱动优化方法，区别于纯数据驱动或单波段时域滤波方法。消融实验表明，重建损失是最关键项（移除后误差增加 90.1%），平滑项和 Huber 鲁棒损失分别贡献 56.7% 和 11.3% 的误差降低（Table 1）。

**局限性**：方法假设背景辐射变化与物体信号不相关，在全局均匀升温场景下可能失效；低成本微测辐射热计在窄带滤光下灵敏度不足，难以检测低发射率物体的微小温差。

## 背景与动机

### 热成像的物理歧义：发射与反射的纠缠

热像仪接收到的红外辐射并非单一来源。如Figure 1所示，每个像素的测量值由五个组分构成：物体自身辐射 $\Phi_s$、背景辐射经物体表面反射 $\Phi_b$、光学元件辐射 $\Phi_o$、传输路径辐射 $\Phi_t$，以及相机内部组件辐射 $\Phi_i$。在经过增益/偏置校正（Figure 7）消除光学与内部辐射后，单波段像素强度可简化为物体发射与背景反射的加权和：

$$I_m(t) = \epsilon_m U_m(T_o(t)) + (1-\epsilon_m) U_m(T_b(t))$$

其中 $\epsilon_m$ 为波段 $m$ 的发射率，$U_m(\cdot)$ 为温度-强度转换函数（在常见工作范围内近似线性），$T_o$ 与 $T_b$ 分别为物体温度与等效背景温度。

这一模型的根本困难在于：**每个像素的观测量（单波段强度）远少于未知量（发射率、物体温度、背景温度）**。在近环境温度条件下，$T_o$ 与 $T_b$ 相近，物体自身辐射与背景反射强度相当，两者均随时间变化，使得问题高度欠定。

### 现有方法的局限

传统热成像方法依赖多种简化假设来缓解上述欠定性，但这些假设在动态近环境场景中往往不成立：

**灰体假设与双波长高温计。** 传统双波长高温计（Tsai et al., International Journal of Thermophysics 1990）假设物体为灰体（$\epsilon_1 = \epsilon_2$），并忽略背景辐射项。当物体发射率随波长变化（非灰体）或背景反射不可忽略时，该方法产生显著偏差。

**多波长最小二乘法。** 朴素的多波段联合优化方法试图同时估计发射率与温度，但由于发射率矩阵 $\mathbf{E}$ 的秩仅为2（在双波段情形下），系统本质上仍欠定，需要良好的初始猜测，且对噪声敏感。

**黑体通道先验（BCP）。** Grimming等人（Optical Engineering 2023）提出的BCP方法假设图像局部最亮像素近似为黑体，以此抑制反射分量。然而该假设在非黑体材料占主导的场景中失效，且无法显式估计物体温度。

**FLIR反射器法。** FLIR Systems推荐的反射器法（2019）可用于标定发射率，但对低发射率材料精度不足（见Table 2：Chrome Ball参考值0.1，反射器法测得0.43），且无法处理时变背景。

### 核心瓶颈与本文动机

上述方法的共同缺陷在于：**未同时利用光谱维度的约束与时域动态的先验**。具体而言：

- **光谱维度**：不同材料在双波段下的发射率比值 $\epsilon_2/\epsilon_1$ 是固定但未知的常数，这一光谱比率提供了跨波段的约束，但单独使用不足以解耦发射与反射。
- **时域维度**：物体温度变化遵循热传导方程，呈平滑指数规律；而背景反射变化（如人员走动、设备启停）与物体温度演化不相关，常表现为突变。这一时域差异可提供额外的分离依据。

本文的核心动机在于：**将双波段光谱比率与时域平滑/突变差异相结合，为原本欠定的发射-反射分离问题引入充分约束，从而在无需已知发射率或背景静止假设的条件下，逐像素估计物体发射率、物体温度与背景温度。**

## 核心创新

本文提出的 **双波段热成像视频分析（Dual Band Thermal Videography, DBVT）** 框架，其核心创新在于突破了近环境温度下热成像反射-发射分离的欠定瓶颈。当物体温度接近环境温度时，自身热辐射与背景反射强度相当，且两者均随时间变化，传统方法依赖灰体假设或背景静止假设，无法有效解耦。DBVT通过以下三个关键机制协同工作，为欠定系统提供了充分约束。

### 1. 双波段非灰体发射率先验

传统双波长高温计（Tsai et al., International Journal of Thermophysics 1990）假设物体为灰体，即发射率与波长无关（$\epsilon_1 = \epsilon_2$），这在真实材料中几乎不成立。BCP方法（Grimming et al., Optical Engineering 2023）则通过局部最亮像素假设来抑制反射，回避了发射率建模。DBVT的核心洞察是：**材料在两个窄波段的发射率虽不相等，但其比值是固定的**。这一假设由静态背景像素的时域导数比 $k_1$ 和动态场景残差比 $k_2$ 两个常比率来表征：

$$k_1 = \frac{\epsilon_2}{\epsilon_1} = \frac{a_1}{a_2} \frac{\partial I_2/\partial t}{\partial I_1/\partial t}$$

$$k_2 = \frac{1-\epsilon_2}{1-\epsilon_1} = \frac{a_1}{a_2} \frac{I_2(t)-\tilde{I}_2(t)}{I_1(t)-\tilde{I}_1(t)}$$

由 $k_1$ 和 $k_2$ 可直接解析求解双波段发射率：

$$\epsilon_1 = \frac{k_2-1}{k_2-k_1}, \quad \epsilon_2 = k_1 \frac{k_2-1}{k_2-k_1}$$

这一设计将发射率从“完全未知”降维为“比值固定”，显著降低了问题的自由度。

### 2. 物体温度平滑动态先验

传统方法通常假设物体温度恒定或背景静止，无法处理时变场景。DBVT引入了一个物理驱动的先验：**物体温度变化遵循热传导常微分方程（ODE），呈平滑指数规律**，而背景反射变化与物体温度不相关。这一先验使得算法能够通过递归构造平滑的发射主导信号 $\tilde{I}_m(t)$，将时域信号分解为平滑的物体发射分量和突变的背景反射分量，从而为 $k_2$ 的估计提供干净的残差信号。

### 3. 联合优化框架替代解析解

尽管 $k_1$ 和 $k_2$ 提供了发射率的解析表达式，但解析解对噪声高度敏感。DBVT转而构建了一个**联合优化目标**，直接优化发射率而非依赖噪声敏感的中间比率：

$$\mathcal{L}_{\text{total}} = \gamma_1 \mathcal{L}_{\text{smooth}} + \gamma_2 \mathcal{L}_{\text{Huber}} + \gamma_3 \mathcal{L}_{\text{MSE}} + \gamma_4 \mathcal{L}_{\text{noise}}^{L2} + \gamma_5 \mathcal{L}_{\text{noise}}^{M}$$

其中，$\mathcal{L}_{\text{smooth}}$ 编码物体温度平滑先验，$\mathcal{L}_{\text{Huber}}$ 提供鲁棒数据保真，$\mathcal{L}_{\text{MSE}}$ 约束 $k_2$ 重建一致性，噪声正则化项在低信噪比下提供额外稳定性。消融实验（Table 1）表明，重建损失是最关键项（移除后误差增加90.1%），平滑项和Huber损失各自贡献显著（分别增加56.7%和11.3%），噪声正则化在低信噪比下尤为有益（增加11.6%）。

### 4. 硬件层面的双窄带滤光方案

与使用单个宽波段LWIR相机的传统方案不同，DBVT采用**双窄带滤光片**（8.5μm, 9.5μm, 10.6μm, 12.1μm）配合热像仪进行同步视频采集。波段选择经过发射率矩阵 $E$ 的条件数分析（Figure 9），确保数值稳定性。这一硬件设计使得光谱比率约束在物理上可测量，是算法创新的硬件基础。

## 整体框架

DBVT（Dual Band Thermal Videography）的整体流程围绕一个核心矛盾展开：在近环境温度下，物体自身热辐射与背景反射强度相当，且两者均随时间变化，传统方法依赖灰体假设或背景静止假设，无法有效解耦。DBVT通过**双波段光谱比率约束**与**时间动态差异先验**的组合，将这一高度欠定问题转化为可联合优化的系统。

### 输入与预处理

系统的原始输入为使用不同中心波长窄带滤光片（8.5μm、9.5μm、10.6μm、12.1μm）同步采集的双波段热视频序列。在进入核心算法之前，需完成两项预处理：

1. **增益/偏置校正**：消除光学元件和相机自身辐射（自恋效应，narcissus effect）对测量值的污染。与仅做偏置校正的现有方法不同，DBVT同时进行增益和偏置校正，以确保对入射辐射的准确恢复（Figure 7）。
2. **温度-强度线性标定**：通过黑体辐射源在不同温度下的测量，建立各波段的线性映射关系 $U_m(T) = a_m T + b_m$。实验表明，在热像仪噪声水平以下，Sakuma-Hattori指数拟合与线性拟合的差异不超过几个计数值（Figure 7），因此采用线性模型即可满足精度要求。

### 双波段图像形成模型

每个波段 $m$ 的像素强度由物体发射与背景反射的加权和构成：

$$I_m(t) = \epsilon_m U_m(T_o(t)) + (1-\epsilon_m) U_m(T_b(t))$$

其中 $\epsilon_m$ 为波段 $m$ 的材料发射率，$T_o(t)$ 和 $T_b(t)$ 分别为物体温度和背景等效温度。这一模型将每个像素的未知量压缩为四个标量：两个波段的发射率 $\epsilon_1, \epsilon_2$，以及时变的 $T_o(t)$ 和 $T_b(t)$。

### 核心约束与求解路径

DBVT的求解分为**标定**和**未标定**两条路径：

**标定路径**（已知物体与背景温度）：利用热电偶等接触式传感器获取 $T_o$ 和 $T_b$ 的真值，通过单波段图像直接求解发射率：

$$\epsilon_m = \frac{I_m - U_m(T_b)}{U_m(T_o) - U_m(T_b)}$$

当发射率已知时，则可通过闭合表达式从双波段图像中恢复 $T_o$ 和 $T_b$（Eq.14）。标定路径主要用于验证方法的物理正确性——实验表明，标定得到的发射率与ECOSTRESS光谱库及FLIR反射器法高度一致，且对低发射率材料精度更优（Table 2）。

**未标定路径**（核心贡献）：在无温度真值的通用场景下，系统面临 $M \times N$ 帧图像中每个像素四个未知量的欠定问题。DBVT引入两类互补约束：

1. **静态像素微分比 $k_1$**：在背景辐射不变（$\partial T_b/\partial t = 0$）的像素处，双波段时域导数的比值为常数，等于两波段发射率之比：

   $$k_1 = \frac{\epsilon_2}{\epsilon_1} = \frac{a_1}{a_2} \frac{\partial I_2/\partial t}{\partial I_1/\partial t}$$

2. **动态场景残差比 $k_2$**：物体温度变化服从热传导ODE，呈平滑指数规律。去除平滑的发射主导信号 $\tilde{I}_m(t)$ 后，残差的比值同样为常数，取决于 $(1-\epsilon_m)$：

   $$k_2 = \frac{1-\epsilon_2}{1-\epsilon_1} = \frac{a_1}{a_2} \frac{I_2(t)-\tilde{I}_2(t)}{I_1(t)-\tilde{I}_1(t)}$$

由 $k_1$ 和 $k_2$ 可解析求解双波段发射率（Eq.23），进而通过闭合式恢复温度。

### 优化框架与模块串联

实际应用中，直接使用解析解对噪声敏感。DBVT将上述约束嵌入全局优化框架（Algorithm 1），各模块串联如下：

| 模块 | 功能 | 关键机制 |
|------|------|----------|
| 平滑信号估计 | 利用 $k_1$ 比值递归构造发射主导信号 $\tilde{I}_m(t)$ | Eq.25 递推式 |
| 发射率优化 | 通过总损失函数直接优化 $\epsilon_1, \epsilon_2$ | 替代噪声敏感的解析解 |
| 温度恢复 | 利用优化后的发射率和双波段图像闭合求解 $T_o, T_b$ | Eq.14 闭合式 |

总损失函数联合五项约束（Eq.30）：

$$\mathcal{L}_{\text{total}} = \gamma_1 \mathcal{L}_{\text{smooth}} + \gamma_2 \mathcal{L}_{\text{Huber}} + \gamma_3 \mathcal{L}_{\text{MSE}} + \gamma_4 \mathcal{L}_{\text{noise}}^{L2} + \gamma_5 \mathcal{L}_{\text{noise}}^{M}$$

其中 $\mathcal{L}_{\text{smooth}}$ 编码物体温度平滑先验，$\mathcal{L}_{\text{Huber}}$ 提供鲁棒数据保真（归一化Huber损失），$\mathcal{L}_{\text{MSE}}$ 约束 $k_2$ 重建精度，噪声正则化项在低信噪比下提供额外稳定性。消融实验（Table 1, Figure 8）表明：重建损失是最关键项（移除后误差增加90.1%），平滑项和Huber损失各自贡献显著（分别增加56.7%和11.3%），噪声正则化在低SNR下收益明显（增加11.6%）。

### 输出

最终输出为每个像素的**时变物体温度** $T_o(t)$、**时变背景温度** $T_b(t)$，以及**双波段发射率** $\epsilon_1, \epsilon_2$。在真实视频实验中，未标定方法的物体温度估计误差仅为1.72%~5.34%，远低于朴素最小二乘的31.68%~45.5%（Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/001_Figure_1.jpg]]
*Figure 1: Image formation in a thermal camera comprises of radiation from the object*

## 核心模块与公式推导

### 热成像辐射传输建模

热像仪接收的辐射由五个组分构成：目标表面发射辐射 $\Phi_s$、背景反射辐射 $\Phi_b$、光学元件辐射 $\Phi_o$、传输路径辐射 $\Phi_t$ 以及相机内部组件辐射 $\Phi_i$（Figure 1）。经增益/偏置校正（Figure 7）消除光学元件与内部辐射后，目标表面出射的总辐射可表为发射与反射的加权和：

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/008_Figure_7.jpg]]
*Figure 7: Top: Shows the gain and offset correction images for the various spectral bands. Unlike [22] which only performs offset correction, we perform both gain and offset correction for accurate recovery of incoming radiation. Bottom: Shows blackbodies at different temperatures and their corresponding pixel values in blue, with the exponential Sakuma-Hattori fit [29] and linear fit for the pixel values is shown in dotted red and green respectively. As seen, both temperature to camera counts curve looks linear and the difference between the Sakuma-Hattori and linear curve is less than a couple of counts, which is much below the noise floor of the thermal camera*

$$\Phi_A(\lambda) = \epsilon_s(\lambda) \Phi_s(\lambda) + (1 - \epsilon_s(\lambda)) \Phi_b(\lambda)$$

其中 $\epsilon_s(\lambda)$ 为光谱发射率。在窄带假设下，第 $m$ 波段的像素强度线性化为：

$$I_m(t) = \epsilon_m U_m(T_o(t)) + (1 - \epsilon_m) U_m(T_b(t))$$

其中 $U_m(\cdot)$ 为温度-强度转换函数（实验表明在所用波段内线性近似误差远低于相机噪声底限，Figure 7）。该模型的核心瓶颈在于：近环境温度下物体自身辐射与背景反射强度相当，且两者均随时间变化，单波段观测高度欠定。

### 双波段标定框架

当物体温度 $T_o$ 与背景温度 $T_b$ 已知（如通过热电偶与黑体反射标定），各波段发射率可直接求解：

$$\epsilon_m = \frac{I_m - U_m(T_b)}{U_m(T_o) - U_m(T_b)}$$

反之，若双波段发射率已知，物体与背景温度可通过闭合式解析恢复：

$$T_o = \frac{a_1(I_2-b_2)(\epsilon_1-1) - a_2(I_1-b_1)(\epsilon_2-1)}{a_1 a_2 (\epsilon_1-\epsilon_2)}$$

其中 $a_m$、$b_m$ 为波段 $m$ 的线性转换系数。该闭合解是后续未标定场景温度重构的基础。

### 未标定场景的动态约束

在发射率未知的未标定场景，双波段观测矩阵 $\mathbf{E}$ 秩为 2，需引入额外先验方可求解。本文的核心洞察在于同时利用**光谱比率**与**时间动态差异**两个互补约束：

**静态像素微分比 $k_1$**：对于背景辐射不随时间变化的像素区域（如场景中的静止背景），双波段时域导数比值为定值，等于两波段发射率之比：

$$k_1 = \frac{\epsilon_2}{\epsilon_1} = \frac{a_1}{a_2} \frac{\partial I_2/\partial t}{\partial I_1/\partial t}$$

**动态场景残差比 $k_2$**：物体温度变化服从热传导方程，呈平滑指数形式。去除平滑的发射主导信号 $\tilde{I}_m(t)$ 后，残差主要由背景反射的突变引起，其比值同样为常数：

$$k_2 = \frac{1-\epsilon_2}{1-\epsilon_1} = \frac{a_1}{a_2} \frac{I_2(t)-\tilde{I}_2(t)}{I_1(t)-\tilde{I}_1(t)}$$

由 $k_1$ 与 $k_2$ 可解析求解双波段发射率：

$$\epsilon_1 = \frac{k_2-1}{k_2-k_1}, \quad \epsilon_2 = k_1 \frac{k_2-1}{k_2-k_1}$$

### 优化框架与损失函数

上述解析解对噪声敏感，实际采用全局优化框架联合估计发射率与平滑信号。平滑信号通过 $k_1$ 约束递归构造：

$$\tilde{I}_2(t) = \tilde{I}_2(t-1) + k_1 \frac{a_2}{a_1} (\tilde{I}_1(t) - \tilde{I}_1(t-1))$$

总损失函数整合四项约束：

$$\mathcal{L}_{\text{total}} = \gamma_1 \mathcal{L}_{\text{smooth}} + \gamma_2 \mathcal{L}_{\text{Huber}} + \gamma_3 \mathcal{L}_{\text{MSE}} + \gamma_4 \mathcal{L}_{\text{noise}}^{L2} + \gamma_5 \mathcal{L}_{\text{noise}}^{M}$$

各损失项的作用与消融验证（Table 1, Figure 8）：
- **$\mathcal{L}_{\text{smooth}}$**：物体温度平滑先验，移除后误差增加 56.7%；
- **$\mathcal{L}_{\text{Huber}}$**：归一化鲁棒数据保真项，移除后误差增加 11.3%；
- **$\mathcal{L}_{\text{MSE}}$**：$k_2$ 残差比约束的重建损失，是最关键项，移除后误差增加 90.1%；
- **$\mathcal{L}_{\text{noise}}$**：噪声正则化项，在低信噪比下显著有益，移除后误差增加 11.6%。

### 补充图表

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/010_Figure_9.jpg]]
*Figure 9: Condition numbers of emissivity matrix E in Eq. 15 for different spectral band pairs, averaged over materials in the spectral library [3, 21]*

## 实验与分析

### 仿真实验：多材料、多噪声水平下的方法对比

为系统评估DBVT框架的性能，作者基于ECOSTRESS光谱库中的多种材料生成仿真热视频，并在不同噪声水平下与三类基线方法进行比较：**BCP**（Grimming et al., Optical Engineering 2023）、传统**双波长高温计**（Tsai et al., Int. J. Thermophysics 1990）和**朴素多波长最小二乘**。仿真中物体温度服从热传导ODE的指数衰减规律，背景温度引入随机突变以模拟真实场景的动态反射。

**Figure 2（左）**展示了各方法的物体温度RMSE随噪声水平的变化。核心结论如下：

- **中等噪声下DBVT优势显著**：在log-scale误差坐标下，DBVT在中等信噪比区间的误差远低于所有基线。双波长高温计因忽略背景辐射且依赖灰体假设，误差始终较高；BCP虽能抑制反射，但在物体非黑体时引入系统偏差；朴素最小二乘对初始化高度敏感，即使选取五次初始化中的最优结果，仍因欠定问题而性能不佳。
- **高噪声下所有方法均退化**，但DBVT的退化曲线更平缓，表明其优化框架中的噪声正则化项（$\mathcal{L}_{\text{noise}}^{L2}$和$\mathcal{L}_{\text{noise}}^{M}$）在低信噪比下发挥了缓冲作用。
- **Figure 2（右）**进一步展示了DBVT在不同发射率真值和噪声水平下的发射率估计误差，结果表明对于中等发射率（0.3–0.7）的材料，估计精度最高；极低发射率（<0.1）时误差增大，这源于反射分量主导使信号分离难度上升。

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/002_Figure_2.jpg]]
*Figure 2: [Left] Comparison of our method with a recent BCP [9] technique, naive multi-wavelength, and dual-wavelength pyrometry [2, 39] on simulated thermal videos of different materials sourced from the spectral library [3, 21]. The naive least squares result uses the best of five initializations selected based on the one that achieved the least objective. All methods degrade at high noise; ours improves significantly at moderate noise (log scale). See our plot in the supplementary for per-material comparisons. [Right] Shows the error in estimated emissivities from our method for a range of emissivities under varying noise levels in simulation*

**Figure 3**给出了空间温度误差的逐像素可视化。在包含热传导仿真与移动玩具背景的合成视频中，DBVT的平均空间温度误差显著低于朴素最小二乘，尤其在物体边缘和背景突变区域，朴素LS出现大面积高误差，而DBVT保持了全局一致性。

### 损失项消融实验

为量化各损失项的贡献，作者在仿真环境中逐一移除损失项并测量温度估计误差的百分比变化（**Table 1**，**Figure 8**）：

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/009_Figure_8.jpg]]
*Figure 8: Ablating the loss terms in simulation: We individually disable each loss term from the full optimization pipeline. Note the log scale on the plots. Reconstruction loss is obviously the most important term followed by smoothing, huber and noise optimization. The noise term is useful at high noise levels*

| 移除项 | 误差增加比例 | 关键发现 |
|--------|-------------|---------|
| 重建损失 $\mathcal{L}_{\text{MSE}}$ | **+90.1%** | 最关键的项，缺失后框架失去数据保真能力 |
| 平滑先验 $\mathcal{L}_{\text{smooth}}$ | **+56.7%** | 物体温度平滑假设是分离发射与反射的核心约束 |
| Huber损失 $\mathcal{L}_{\text{Huber}}$ | **+11.3%** | 鲁棒损失对背景突变产生的离群值具有抑制作用 |
| 噪声正则化 $\mathcal{L}_{\text{noise}}$ | **+11.6%** | 在低信噪比下贡献尤为显著（Figure 8印证） |

消融结果表明，DBVT的性能并非由单一技巧驱动，而是光谱比率约束（k1/k2）、时域平滑先验与鲁棒优化的协同产物。重建损失提供基础驱动，平滑项赋予分离能力，Huber与噪声正则化则在边缘场景下保障稳定性。

### 真实场景实验：反射-发射分离

作者在多种加热方式（热液体、手部接触、热风）的真实物体上验证了DBVT的未标定分离能力。**Figure 6**展示了咖啡壶、酒杯等物体的分离结果，每行依次为估计的发射分量与均值去除后的反射分量。

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/007_Figure_6.jpg]]
*Figure 6: Reflection–emission separation results for objects heated using different methods (hot liquid, hand contact, and hot air). For each object, the first row shows the estimated emission, and the second row shows the mean-subtracted reflection. Input thermal frames from two spectral bands are shown on the left. Since per-pixel temperature ground truth is unobtainable, we record temperatures at sparse locations using a thermocouple. The wineglass and coffee pot reached peak temperatures of*

定量评估采用热电偶实测温度作为真值：

- **酒杯视频**：DBVT物体温度估计误差仅为**1.72%**，而朴素最小二乘误差高达**31.68%**，误差降低约30个百分点。
- **咖啡壶视频**：DBVT误差为**5.34%**，朴素LS误差为**45.5%**，误差降低约40个百分点。

值得注意的是，这些实验**未使用任何发射率标定**，完全依赖DBVT的盲分离能力。朴素LS在此场景下基本失效，原因是其将反射分量错误归因于物体温度变化，导致严重高估或低估。

**Figure 5**展示了两个精细分离案例：（上）玻璃板上热指纹（热传导产生的发射）与均匀背景反射的分离；（下）玻璃板反射的手指镜像（光传输）与恒温玻璃板自身发射的分离。这两个案例直观验证了DBVT对发射与反射物理来源的准确解耦——前者依赖温度变化驱动，后者依赖背景变化驱动。

### 发射率标定实验

在标定模式下，作者利用已知温度的黑体和热电偶，通过Eq.12计算各波段的发射率。**Figure 4**展示了不同光谱滤光片（8.5μm, 9.5μm, 10.6μm, 12.1μm）下的标定图像及所得发射率值。

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/006_Figure_4.jpg]]
*Figure 4: [Top] Images captured with different spectral filters used for calibration. The red bounding box highlights the reflected blackbody on the object. A thermocouple is placed next to this reflection to measure the object’s temperature. [Bottom] Calibrated emissivity values for various materials using our technique align the closely with reported values [1, 3] as shown in Tab. 2*

**Table 2**将DBVT标定结果与FLIR反射器法及参考值进行对比：

| 材料 | DBVT标定 | 反射器法 | 参考值 |
|------|---------|---------|--------|
| 铬球 (Chrome Ball) | **0.12** | 0.43 | 0.1 |
| 铝杯 (Al. Cup) | 0.21 | 0.25 | 0.15–0.2 |
| 高发射率材料 | 与反射器法一致 | — | 与ECOSTRESS谱库吻合 |

关键发现：对于**低发射率材料**（如铬球），DBVT标定结果（0.12）远优于反射器法（0.43），更接近参考值（0.1）。反射器法在低发射率时因多次反射假设不成立而高估发射率，DBVT通过直接测量已知温度下的辐射强度避开了这一缺陷。对于高发射率材料，两种方法结果一致，均与ECOSTRESS光谱库吻合。

### 方法局限与失效模式

尽管DBVT在多数场景下表现优异，论文明确指出了两类局限：

1. **背景-物体相关性假设**：DBVT的核心约束之一是背景辐射变化与物体温度变化不相关。当整个场景均匀升温（如房间整体加热）时，该假设失效，k2比率的恒定性被破坏，导致分离质量下降。作者指出这需要更复杂的时域模型来应对。

2. **硬件灵敏度瓶颈**：低成本微测辐射热计在窄带滤光下灵敏度不足。对于低发射率物体，反射分量主导图像强度，而物体自身发射的微小温差信号可能淹没在噪声中，使DBVT的优化框架难以收敛到正确解。Figure 8中噪声正则化在高噪声下的有限收益也间接反映了这一硬件约束。

### 光谱带选择分析

**Figure 9**给出了不同波段组合下发射率矩阵$\mathbf{E}$的条件数分析。条件数越低，双波段系统的数值稳定性越好。结果表明，8.5μm与12.1μm的组合在ECOSTRESS材料库上平均条件数最优，这与作者实验中选择的波段对一致。这一分析为未来多波段扩展提供了选带依据。

### 补充图表

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/004_Figure_3.jpg]]
*Figure 3: Spatial temperature errors*

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/005_Figure_5.jpg]]
*Figure 5: Finger print versus Finger reflection: [Top] Separating finger prints on a glass plate that emit light (heat transport) from the reflection of the uniform background (light transport). [Bottom] Separating the reflection of the fingers (light transport) by the glass plate at constant room temperature (heat transport)*

![[assets/figures/papers/paper_list_l2121_https_arxiv_org_abs_2509_11334/figures/011_Figure_10.jpg]]
*Figure 10: Comparison of our method with a recent BCP [9] technique to remove reflections, a naive multi-wavelength approach and a traditional dual-wavelength pyrometry technique [2, 39] using simulated thermal videos of different materials sourced from spectral library [3, 21]. For naive least squares, we run the optimization with five initializations and select one that achieved the least objective compared to ground truth (which we will not have access to at test time). At high noise levels, all methods have a large error as the problem is too under constrained. As noise decreases to more reasonable levels, our method performs significantly better. Note the log scale on the plots*

## 方法谱系与知识库定位

### 问题谱系：从灰体假设到非灰体时变分离

热成像中物体温度与发射率的耦合是长期存在的欠定问题。传统方法依赖两类简化假设来降低自由度：

**灰体假设路径**：双波长高温计（**Dual-wavelength pyrometry**, Tsai et al., Int. J. Thermophysics 1990）假设物体为灰体（发射率与波长无关），从而将未知数从 $M+2$（$M$ 个波段发射率 + 物体温度 + 背景温度）压缩至 $3$。但该假设在近环境温度下失效——多数材料的发射率随波长变化显著，且背景反射强度与物体自身辐射相当，忽略反射导致系统误差。

**背景静止假设路径**：**Blackbody Channel Prior (BCP)**（Grimming et al., Optical Engineering 2023）假设局部最亮像素为黑体，利用该先验抑制反射分量。此方法无需多波段硬件，但依赖“场景中存在黑体”的强假设，且无法处理时变背景辐射——当背景温度变化时，最亮像素不再对应黑体。

**朴素多波段最小二乘**：联合优化发射率与温度，但缺乏物理先验约束，在噪声下极易陷入局部最优。仿真中该方法使用五种初始化中目标函数最小者，仍远逊于本文方法（Figure 2）。

本文 **Dual Band Thermal Videography (DBVT)** 在谱系中占据独特位置：它同时放弃灰体假设和背景静止假设，转而利用**双波段光谱比率的时间不变性**与**物体温度演化的物理平滑先验**，将欠定系统转化为可解问题。

### 核心假设与适用边界

DBVT 的有效性建立在三个关键假设之上：

1. **发射率比值固定**：材料在双波段的发射率比值 $k_1 = \epsilon_2/\epsilon_1$ 为未知常数。这比灰体假设弱得多（灰体要求 $k_1=1$），允许材料为非灰体。ECOSTRESS 谱库验证表明，多数材料在窄波段内的发射率比值确实稳定（Figure 9 条件数分析）。

2. **物体温度平滑演化**：物体温度变化服从热传导 ODE，呈指数衰减/上升形式。此假设在短时间尺度（数秒至数分钟）内成立，Ramanagopal et al. 的工作为此提供了理论支撑。当物体受到突变热源（如瞬间接触高温物体）时，该假设可能局部失效。

3. **背景辐射与物体信号不相关**：背景反射的变化与物体温度变化统计独立。这是推导动态背景比率 $k_2$ 的前提。**当整个场景均匀升温（如房间空调启动）时，此假设可能失效**，此时背景与物体温度变化存在相关性，$k_2$ 的估计会引入偏差。

### 硬件谱系：从宽波段到双窄带

传统热成像使用单个宽波段 LWIR 相机（8–14 μm），光谱信息被积分丢失。DBVT 引入**双窄带滤光片**（8.5 μm, 9.5 μm, 10.6 μm, 12.1 μm）配合微测辐射热计相机，在硬件层面实现了光谱解耦。Figure 9 的条件数分析表明，波段选择直接影响发射率矩阵 $\mathbf{E}$ 的数值稳定性——波段间距过小导致条件数恶化，过大则信号强度不足。本文选择的波段对在 ECOSTRESS 材料库上平均条件数最优。

硬件限制同样明确：低成本微测辐射热计在窄带滤光下的灵敏度不足，难以检测低发射率物体（如 $\epsilon \approx 0.1$ 的抛光金属）的微小温差。这是方法向更低成本硬件扩展的主要障碍。

### 损失函数设计的消融证据

总损失函数（Eq. 30）包含五项：

$$\mathcal{L}_{\text{total}} = \gamma_1 \mathcal{L}_{\text{smooth}} + \gamma_2 \mathcal{L}_{\text{Huber}} + \gamma_3 \mathcal{L}_{\text{MSE}} + \gamma_4 \mathcal{L}_{\text{noise}}^{L2} + \gamma_5 \mathcal{L}_{\text{noise}}^{M}$$

Table 1 的消融实验揭示了各项的贡献层级：

| 移除项 | 误差增加 | 机制解释 |
|--------|----------|----------|
| MSE 重建损失 | **90.1%** | 数据保真项，约束 $k_2$ 重建一致性 |
| 平滑先验 | **56.7%** | 编码物体温度指数演化，抑制高频噪声 |
| Huber 鲁棒损失 | 11.3% | 对离群反射突变提供鲁棒性 |
| 噪声正则化 | 11.6% | 低 SNR 下显著有益（Figure 8 验证） |

MSE 重建损失和平滑先验是性能的“双支柱”，移除任一项导致误差翻倍以上。Huber 损失和噪声正则化提供精细增益，在高噪声场景下作用更为突出。

### 标定与无标定两条路径的知识定位

DBVT 提供两种工作模式：

- **标定模式**（Section 4.1）：利用已知温度的黑体和热电偶，通过 Eq. 12 直接计算各波段发射率。Table 2 显示，本文标定方法对低发射率材料（如 Chrome Ball，$\epsilon=0.12$）的精度优于 FLIR 推荐的反射器法（Reflector method, FLIR Systems Inc. 2019，测得 0.43），更接近参考值 0.1。

- **无标定模式**（Section 4.2）：完全从视频中盲估计发射率与温度。真实视频实验中，酒杯物体温度估计误差仅 **1.72%**（对比朴素最小二乘的 31.68%），咖啡壶误差 **5.34%**（对比 45.5%），证明无标定模式在实用场景中的有效性。

### 开放问题与未来方向

1. **相关背景场景的鲁棒性**：当背景辐射变化与物体信号相关时（如整个房间升温），$k_2$ 的推导前提被破坏。能否通过引入更复杂的时域模型（如背景温度的独立 ODE 建模）保持鲁棒性，是理论上的开放问题。

2. **低成本硬件扩展**：当前方法依赖微测辐射热计在窄带滤光下的灵敏度。向更低成本、更多波段（如四波段）的硬件扩展，并实现实时视频处理，是工程上的关键挑战。

3. **波段选择的自动化**：Figure 9 的条件数分析为波段选择提供了原则，但最优波段对依赖于材料类型。自适应波段选择策略（如根据场景初步估计后动态切换滤光片）可能进一步提升精度。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dual_Band_Thermal_Videography_Separating_Time_Varying_Reflection_and_Emission_Near_Ambient_Conditions.pdf]]

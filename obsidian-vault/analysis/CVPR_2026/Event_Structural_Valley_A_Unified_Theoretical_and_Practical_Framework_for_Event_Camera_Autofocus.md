---
title: "Event Structural Valley: A Unified Theoretical and Practical Framework for Event Camera Autofocus"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Event_Structural_Valley_A_Unified_Theoretical_and_Practical_Framework_for_Event_Camera_Autofocus.pdf
project_link: null
code_link: null
aliases:
- ESVBAE
- ESVUTPFECA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 事件率曲线随散焦变化呈现非单调的双峰谷结构，谷底对应真实焦点。通过定位两峰之间的最小值即可恢复准确焦点。
primary_logic: 在焦点扫掠过程中，事件率随散焦程度先升后降：精准对焦处事件率为局部最小值，轻微散焦时边缘扩展使事件率升高并形成双峰，进一步散焦则梯度减弱、事件率下降。真实焦点位于事件率曲线两个主导峰之间的谷底。
claims:
- 真实焦点对应事件率曲线中的局部最小值。
- 事件率曲线在一路焦点扫掠中呈现双峰谷结构。
- 理论模型证明激活区域在σ=0（精准对焦）时为严格局部最小值。
- ESVA通过结构正则化模块鲁棒恢复谷底，无需图像重建或监督。
---

# Event Structural Valley: A Unified Theoretical and Practical Framework for Event Camera Autofocus

> [!tip] 核心洞察
> 在焦点扫掠过程中，事件率随散焦程度先升后降：精准对焦处事件率为局部最小值，轻微散焦时边缘扩展使事件率升高并形成双峰，进一步散焦则梯度减弱、事件率下降。真实焦点位于事件率曲线两个主导峰之间的谷底。

| 字段 | 内容 |
|------|------|
| 中文题名 | 事件结构谷：一种统一的事件相机自动对焦理论与实用框架 |
| 英文题名 | Event Structural Valley: A Unified Theoretical and Practical Framework for Event Camera Autofocus |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xiang_Event_Structural_Valley_A_Unified_Theoretical_and_Practical_Framework_for_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Event Structural Valley-based Autofocus (ESVA) |
| Dataset | SYN, DAVIS, EVK4, EAD |

> [!tip] 效果简介
> - SYN (Static) 上，平均时间戳误差 (ms) 3.16 vs 8.25 (ELP) (-5.09)。
> - SYN (Small Shake) 上，平均时间戳误差 (ms) 5.46 vs 8.36 (ELP) (-2.90)。
> - SYN (Huge Shake) 上，平均时间戳误差 (ms) 11.25 vs 9.43 (ELP) (+1.82)。

## 概述

事件相机因其微秒级时间分辨率、高动态范围和低功耗特性，在高鲁棒性自动对焦任务中展现出独特潜力。然而，现有事件驱动自动对焦方法普遍依赖**最大事件率（Maximum Event Rate, MER）假设**，认为对焦最清晰时事件触发数量达到最大。本文揭示这一假设在物理上并不成立：精准对焦时边缘紧凑、像素级强度变化集中，反而触发更少的事件；轻微散焦时边缘扩展、激活区域扩大，事件率反而升高。这一现象导致基于MER的方法系统性地将焦点定位在真实焦点附近的散焦位置。

本文的核心发现是：在一次完整的焦点扫掠过程中，**事件率曲线呈现非单调的双峰谷结构**——两个主导峰分别对应前后散焦方向上的最大激活区域，而谷底恰好对应真实焦点。基于这一物理洞察，作者提出了**事件结构谷自动对焦框架（Event Structural Valley-based Autofocus, ESVA）**。ESVA将自动对焦问题形式化为事件率曲线在双峰约束区间内的谷底定位问题，无需任何图像重建或监督信号，完全在事件域内完成焦点估计。

为实现鲁棒的谷底恢复，ESVA设计了三个结构正则化模块：**高斯结构平滑**抑制高频噪声、**一致性滤波**消除瞬态运动伪影、**双峰约束**将搜索区间限定在物理有意义的范围内。最终，谷底位置通过区间内最小事件率定位，并辅以置信度分数评估对焦可靠性。

实验覆盖四个数据集（SYN、DAVIS、EVK4、EAD），涵盖静态、抖动、低光、运动模糊等多样化场景。在SYN数据集上，ESVA的平均时间戳误差为6.62 ms，显著优于现有最优方法ELP（Bao et al., CVPR 2025）的8.68 ms；在更具挑战性的EAD数据集上，ESVA实现了65.38 µm的平均距离误差。消融实验进一步验证了三个结构模块各自对鲁棒谷底定位的贡献。

本工作的主要贡献可归纳为：
- **理论层面**：首次从物理建模角度解释了事件率曲线的双峰谷结构，并严格证明了谷底对应真实焦点；
- **方法层面**：提出了完全在事件域内运行的结构化谷底定位框架，无需图像重建或监督；
- **实验层面**：在多个数据集和传感器平台上验证了方法的精度优势与泛化能力。

## 背景与动机

### 事件相机与自动对焦需求

事件相机是一类受生物启发的视觉传感器，其每个像素独立异步地响应场景的对数亮度变化。当像素位置 $(x,y)$ 的对数强度变化超过预设的对比度阈值 $C$ 时，即触发一个事件：

$$\Delta L ( x , y , t ) = L ( x , y , t ) - L ( x , y , t - \delta t ) \ge C$$

与传统的帧式相机不同，事件相机天然具备微秒级时间分辨率、高动态范围和低数据冗余，使其在高速对焦场景中具有显著的感知优势。在事件驱动的自动对焦任务中，相机在连续焦距扫掠过程中采集异步事件流，目标是从这些事件流中确定使场景边缘最为锐利的最优焦点位置（见 Figure 1）。

### 传统MER方法的瓶颈

现有事件相机自动对焦方法普遍基于**最大事件率（Maximum Event Rate, MER）假设**：认为当对焦最清晰时，场景边缘处亮度梯度最大，因而触发的事件数量最多。这一假设驱动了一系列方法的设计，包括基于黄金分割搜索的 **ER+EGS**（Lin et al., CVPR 2022）、基于事件极性平衡的显微对焦方法 **OLE'23**（Ge et al., Optics and Lasers in Engineering 2023）、基于事件极性对称的快速对焦 **PBF**（Bao et al., Optics Express 2023），以及单步事件驱动高速对焦 **ELP**（Bao et al., CVPR 2025）。

然而，MER假设存在根本性的物理缺陷。**精准对焦时，场景边缘最为紧凑，边缘像素数量最少，因此实际触发的事件数量反而较少**；而轻微散焦时，边缘因模糊而扩展，覆盖更多像素，导致事件率升高。这一现象使得基于最大事件率的方法系统性地将焦点定位在略微散焦的位置，而非真实的物理焦点。

### 事件率曲线的双峰谷结构

本文的核心发现是：在连续焦距扫掠过程中，事件率随散焦程度的变化并非单调，而是呈现**非单调的双峰谷结构**（见 Figure 2）。具体而言：

- 当镜头从远散焦位置向焦点移动时，模糊逐渐减小，边缘开始显现，事件率上升，形成**第一个主导峰** $P_1$；
- 继续逼近精准对焦位置时，边缘趋于紧凑，激活像素面积缩小，事件率下降，在最优焦点 $f^*$ 处达到**局部最小值**；
- 越过焦点后，散焦再次加剧，边缘重新扩展，事件率再次上升形成**第二个主导峰** $P_2$；
- 进一步散焦则梯度减弱，事件率整体下降。

因此，**真实焦点并非事件率曲线的全局最大值，而是位于两个主导峰之间的谷底**。这一结构特性构成了本文方法的核心理论依据。

### 研究动机与贡献

上述分析揭示了现有MER方法的根本性局限：由于错误地将焦点对准事件率最大位置，这些方法在原理上无法恢复准确的焦点。本文的动机在于：

1. **建立统一的理论模型**，从模糊依赖的激活区域出发，严格证明事件率曲线在精准对焦处（$\sigma=0$）为局部最小值，并系统刻画双峰谷结构的形成机制；
2. **设计无需图像重建的纯事件域方法**，通过结构正则化模块鲁棒地从含噪事件率曲线中恢复谷底位置，实现准确、稳定的自动对焦；
3. **在多种传感器和场景下验证方法的有效性与泛化能力**，突破现有方法对MER假设的依赖。

## 核心创新

ESVA 的核心创新在于**颠覆了事件相机自动对焦领域长期沿用的最大事件率（MER）假设**，并建立了一套完整的“结构谷”理论与实用框架。传统方法（如 **ER+EGS**（Lin et al., CVPR 2022）、**ELP**（Bao et al., CVPR 2025））隐含地认为，对焦最清晰时场景边缘变化最剧烈，因此触发的事件数量应达到峰值。ESVA 通过理论分析和实验观测揭示了这一假设的根本性缺陷：**真实焦点恰恰位于事件率曲线的局部最小值处**。

这一反直觉的发现源于对事件生成物理过程的深入建模。在焦点连续扫掠过程中，事件率随散焦程度并非单调变化，而是呈现一种**双峰谷结构（dual-peak–valley profile）**：精准对焦时，边缘最为紧凑，因散焦变化而激活的像素区域面积达到局部最小，事件率因此处于谷底；当轻微散焦时，边缘扩展导致激活区域扩大，事件率上升并形成两个主导峰；进一步散焦则梯度减弱，事件率再次下降。真实焦点 $f^*$ 正是两个主导峰 $P_1$ 与 $P_2$ 之间的谷底位置。

基于这一因果机制，ESVA 在三个关键维度上完成了相对于 baseline 的范式转换：

| 关键维度 | 传统方法（MER 范式） | ESVA（结构谷范式） |
|---------|---------------------|-------------------|
| **对焦判定准则** | 选择事件率全局最大位置 | 选择双峰之间的谷底位置（Eq. 8, Corollary 1） |
| **峰值检测与搜索区间** | 无显式峰值检测，依赖全局极值 | 检测两个主导峰，将搜索区间约束为 $[P_1, P_2]$（Eq. 12-13） |
| **曲线去噪与正则化** | 无或简单滤波 | 高斯结构平滑 + 一致性滤波（局部线性投影）（Eq. 9-11） |

ESVA 的另一个重要创新在于**完全在事件域内运行，无需任何图像重建或监督信号**。整个流程由三个结构正则化模块串联构成：结构平滑模块通过高斯核抑制高频噪声，保留曲线的全局双峰谷形态；一致性滤波模块利用局部线性投影移除瞬态噪声引入的虚假峰值，维持曲线的物理连续性；双峰约束模块在平滑后的曲线上检测主峰与次峰，将焦点搜索锁定在物理上有意义的区间内。最终，谷底定位模块在该区间内寻找最小事件率位置，并通过置信度评估模块（Eq. 15）输出对焦可靠性指标——谷底与双峰的平均高度差，差值越大表示焦点越稳健。

这一框架的线性复杂度 $O(N)$ 使其天然适合实时嵌入式部署，所有操作均为单遍前向过程，无需迭代优化。

## 整体框架

ESVA (Event Structural Valley-based Autofocus) 将事件相机自动对焦形式化为一个**结构谷定位问题**，其核心流程可概括为：从事件流中提取事件率曲线，通过结构正则化揭示双峰谷形态，最终在峰值约束区间内定位谷底作为最优焦点。

### 输入与输出

- **输入**：焦点扫掠过程中采集的异步事件流 $\{e_n = (x_n, y_n, t_n, p_n)\}$，以及对应的焦点位置序列 $\{f_i\}$。
- **输出**：最优焦点位置 $f^\star$ 及其置信度分数 $S$。

### Pipeline 模块

ESVA 由六个串行模块构成，所有操作均为单次遍历、无迭代优化，整体复杂度为 $O(N)$（$N$ 为焦点采样点数）。

| 模块 | 功能 | 关键公式 |
|------|------|----------|
| **事件率曲线计算** | 在每个焦点位置 $f_i$ 处以时间窗口 $\Delta t$ 累积事件数，得到原始事件率曲线 $R(f_i)$ | Eq. (2) |
| **结构平滑** | 使用高斯核对 $R(f)$ 进行平滑，抑制高频噪声同时保留全局双峰谷结构，得到 $\tilde{R}(f)$ | Eq. (9) |
| **一致性滤波** | 通过局部线性投影剔除与邻域不一致的采样点，消除瞬态运动噪声，得到正则化曲线 $\hat{R}(f)$ | Eq. (10)–(11) |
| **双峰约束** | 在 $\hat{R}(f)$ 上检测两个主导峰 $P_1$、$P_2$，将搜索区间限定为 $[P_1, P_2]$ | Eq. (12)–(13) |
| **谷底定位** | 在约束区间内寻找 $\hat{R}(f)$ 的全局最小值，作为最优焦点 $f^\star$ | Eq. (14) |
| **置信度评估** | 计算谷底与双峰的平均高度差 $S$，量化对焦可靠性 | Eq. (15) |

### 数据流

```
事件流 + 焦点序列
       │
       ▼
┌─────────────────┐
│ 事件率曲线计算   │  → R(f)   (原始事件率)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 结构平滑         │  → R̃(f)   (去高频噪声)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 一致性滤波       │  → R̂(f)   (消除瞬态噪声)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 双峰约束         │  → [P₁, P₂] (搜索区间)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 谷底定位         │  → f*      (最优焦点)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 置信度评估       │  → S       (可靠性指标)
└─────────────────┘
```

### 与基线方法的关键差异

传统事件自动对焦方法（如 **ER+EGS** (Lin et al., CVPR 2022)、**ELP** (Bao et al., CVPR 2025)）基于最大事件率（MER）假设，选择事件率曲线的全局最大值作为焦点。ESVA 的核心突破在于揭示了事件率曲线的**双峰谷结构**物理本质：精准对焦时边缘紧凑、激活区域最小，事件率处于局部谷底；轻微散焦时边缘扩展导致事件率升高并形成两个主导峰。因此，ESVA 将对焦准则从“选最大值”改为“选双峰之间的最小值”，从根本上解决了 MER 方法的系统偏差。

三个结构正则化模块的协同作用保证了这一策略的鲁棒性：结构平滑保留全局形态，一致性滤波消除瞬态噪声引入的虚假峰值，双峰约束防止算法在极端散焦处错误收敛。消融实验（Figure 7）验证了每个模块的独立贡献——缺少任一模块均会导致对焦误差显著增加。

### 补充图表

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/001_Figure_1.jpg]]
*Figure 1: Event-based Autofocus. The goal of event-based autofocus is to determine the optimal focus position from asynchronous event streams acquired at different focal depths. During a continuous focus sweep (top), the event camera generates ON/OFF events in response to brightness changes along scene edges. The middle rows show accumulated event maps and corresponding intensity images across focal settings. Bottom left: previous Maximum Event Rate (MER) methods [21, 22] select the focus with maximum event activity, often yielding approximate results at slightly defocused states; bottom right: our structural valley-based approach locates the inter-peak valley to achieve a more accurate focus estimate*

## 核心模块与公式推导

### 3.1 事件生成与事件率曲线

事件相机在每个像素独立检测对数强度变化。当累积变化量超过对比度阈值 $C$ 时，触发一个事件。形式化地，事件生成条件为：

$$\Delta L ( x , y , t ) = L ( x , y , t ) - L ( x , y , t - \delta t ) \ge C \quad \text{(Eq. 1)}$$

在一次连续的焦点扫掠过程中，相机在不同焦距位置 $f_i$ 处采集事件流。对每个焦点位置，在时间窗口 $\Delta t$ 内累积触发的事件总数，构成**事件率曲线** $R(f)$：

$$R_i = \sum_{n=1}^{M} \mathbf{1} \big( | t_n - t(f_i) | \leq \frac{\Delta t}{2} \big) \quad \text{(Eq. 2)}$$

其中 $t_n$ 为第 $n$ 个事件的时间戳，$t(f_i)$ 为焦点到达 $f_i$ 的时刻，$\mathbf{1}(\cdot)$ 为指示函数。

### 3.2 双峰谷结构的理论建模

事件率的物理根源在于散焦模糊变化导致的边缘像素激活。定义**模糊依赖激活区域** $\Omega(\sigma)$ 为：在散焦尺度 $\sigma$ 下，对数强度随 $\sigma$ 的变化率超过有效阈值 $\theta(C)$ 的像素集合：

$$\Omega ( \sigma ) := \Bigl\{ \mathbf{x} : \Bigl| \frac{\partial L_{\sigma}(\mathbf{x})}{\partial \sigma} \Bigr| \ge \theta(C) \Bigr\} \quad \text{(Eq. 5)}$$

核心关系在于：事件率正比于该激活区域的面积（像素数量）：

$$R(\sigma) \propto \mathrm{meas}(\Omega(\sigma)) \quad \text{(Eq. 6)}$$

当 $\sigma = 0$（精准对焦）时，边缘最紧凑，激活区域面积达到**严格局部最小值**（Proposition 1 与 Corollary 1）。轻微散焦时，边缘扩展导致激活区域扩大、事件率上升，形成两个主导峰 $P_1$ 和 $P_2$；进一步散焦则梯度减弱，事件率下降。因此，事件率曲线 $R(f)$ 呈现**双峰谷结构**（Figure 2），真实焦点 $f^*$ 位于两峰之间的谷底：

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/002_Figure_2.jpg]]
*Figure 2: Structural characterization of the event-rate curve. Top: spatiotemporal event stream. Middle: during a one-way focus sweep, the event rate*

$$f^{\star} = \arg \operatorname*{min}_{f \in [P_1, P_2]} R(f) \quad \text{(Eq. 8)}$$

这从根本上推翻了传统最大事件率（MER）方法的假设——后者选取事件率最大位置，恰对应轻微散焦状态，导致焦点偏离。

### 3.3 结构正则化框架

原始事件率曲线受传感器噪声和瞬态运动干扰，直接定位谷底不可靠。ESVA 通过三个模块对曲线进行正则化：

**结构平滑**：使用高斯核对原始曲线 $R(f)$ 进行平滑，抑制高频噪声同时保留全局双峰谷结构：

$$\tilde{R}(f_i) = \frac{\sum_{j} R(f_j) \exp[-(f_i - f_j)^2/(2\sigma_s^2)]}{\sum_{j} \exp[-(f_i - f_j)^2/(2\sigma_s^2)]} \quad \text{(Eq. 9)}$$

其中 $\sigma_s$ 为平滑尺度参数。

**一致性滤波**：通过局部线性投影移除物理上不一致的采样点，消除瞬态噪声引入的虚假波动：

$$\hat{R}(f_i) = (1-\eta) \tilde{R}(f_i) + \frac{\eta}{2}[\tilde{R}(f_{i-1}) + \tilde{R}(f_{i+1})] \quad \text{(Eq. 11)}$$

其中 $\eta \in [0,1]$ 控制投影强度。该操作强制曲线在局部保持近似线性，维持物理连续性。

**双峰约束**：在正则化后的曲线 $\hat{R}(f)$ 上检测两个主导峰 $P_1$ 和 $P_2$（Eq. 12-13），将焦点搜索区间严格约束为 $[P_1, P_2]$，避免算法在极端散焦区域错误收敛。

### 3.4 谷底定位与置信度评估

在双峰约束区间内，最优焦点为 $\hat{R}(f)$ 的全局最小值：

$$f^{\star} = \arg \operatorname*{min}_{f \in [P_1, P_2]} \hat{R}(f) \quad \text{(Eq. 14)}$$

为量化对焦结果的可靠性，定义**置信度分数** $S$ 为谷底与两侧峰的平均高度差：

$$S = \frac{1}{2}[\hat{R}(P_1) + \hat{R}(P_2)] - \hat{R}(f^{\star}) \quad \text{(Eq. 15)}$$

$S$ 越大，表明谷底越深、焦点定位越稳健。该分数可在实际部署中用于判断对焦是否成功。

### 3.5 计算复杂度

整个 ESVA 流水线——包括平滑、一致性滤波、双峰检测和谷底定位——均为**单遍前向操作**，无需迭代优化。计算复杂度与焦点采样点数 $N$ 呈线性关系，即 $O(N)$。这使得 ESVA 适合在嵌入式平台上实时运行（见 Table 5 运行时间对比）。

## 实验与分析

### 核心发现：事件率曲线的双峰谷结构

ESVA 的核心实验发现是：在一次焦点扫掠过程中，事件率曲线 $R(f)$ 并非传统方法所假设的单调单峰形态，而是呈现稳定的**双峰–谷底**结构。如 Figure 2 所示，两个主导峰 $P_1$ 和 $P_2$ 分别对应散焦模糊向两侧扩展时事件激活面积增大的阶段，而两峰之间的谷底恰好对应精准对焦位置 $f^*$。这一结构与理论分析一致——精准对焦时边缘激活区域最小，事件率处于局部最小值；轻微散焦时边缘扩展使激活面积增大，事件率上升形成双峰；进一步散焦则梯度减弱、事件率回落。

传统最大事件率（MER）方法选择事件率最高的位置作为焦点，但该位置通常落在某一峰的散焦区域，而非真实焦点。ESVA 通过定位双峰之间的谷底，从根本上纠正了这一系统性偏差。

### 合成数据集（SYN）定量结果

Table 1 报告了 SYN 数据集上各方法的平均时间戳误差。ESVA 在三种运动模式下均展现出显著优势：

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/004_Table_1.jpg]]
*Table 1: Results on the SYN dataset. Average focusing timestamp error (ms) under different motion patterns. Best result per row in bold*

- **静态场景**：ESVA 误差仅 3.16 ms，ELP 为 8.25 ms，**MPGD** 为 8.87 ms，ESVA 相对 ELP 降低 61.7%。
- **小幅抖动场景**：ESVA 误差 5.46 ms，ELP 为 8.36 ms，降低 34.7%。
- **大幅抖动场景**：ESVA 误差 11.25 ms，ELP 为 9.43 ms，ESVA 在此极端条件下略逊于 ELP（+1.82 ms）。这一退化归因于剧烈运动导致事件率曲线结构被噪声淹没，双峰谷底模式难以稳定识别。
- **综合平均**：ESVA 误差 6.62 ms，ELP 为 8.68 ms，整体提升 23.7%。

Figure 3 展示了 SYN 数据集 `cat4-static` 序列的度量曲线。可观察到 ESVA 的估计对焦时刻（红色虚线）与真值（黑色实线）高度吻合，而对比方法的估计点则明显偏离真实焦点。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/003_Figure_3.jpg]]
*Figure 3: SYN (cat4-static): metric curves and estimated focus timestamps. Red dashed: estimate; black solid: ground truth. Subplot titles report timestamp errors; side images visualize events within 1 ms around the estimate*

### 真实数据集（DAVIS）定量结果

Table 2 报告了 DAVIS 数据集的结果。ESVA 在不同光照（明亮/暗光）和运动（静态/运动）条件下均保持高精度，**平均时间戳误差仅 1.30 ms**。值得注意的是，DAVIS 相机的事件噪声水平高于合成数据，但 ESVA 的结构正则化模块有效抑制了噪声干扰，保持了谷底定位的稳定性。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/007_Table_2.jpg]]
*Table 2: Results on the DAVIS dataset. Average focusing timestamp error (ms) across different lighting and motion conditions. Best result per row in bold*

Figure 4 展示了 `box-bright-static` 序列的度量曲线，ESVA 的估计值与真值几乎重合，侧面事件分布图也显示估计时刻的事件边缘最为紧凑清晰。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/006_Figure_4.jpg]]
*Figure 4: DAVIS (box-bright-static): metric curves and estimated focus timestamps. Red dashed: estimate; black solid: ground truth. Side images show events within 1 ms around the estimate*

### 真实数据集（EVK4）定量结果

Table 3 报告了 EVK4 数据集的结果。ESVA 在所有光照和运动组合下均取得最优或次优结果，**平均时间戳误差为 4.22 ms**。EVK4 相机具有更高的分辨率和不同的事件噪声特性，ESVA 的跨传感器泛化能力在此得到验证。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/011_Table_3.jpg]]
*Table 3: Results on the EVK4 dataset. Average focusing timestamp error (ms) under various lighting and motion conditions. Best result per row in bold*

Figure 5 展示了 `focusboard-dark-motion` 这一挑战性序列的结果。在暗光且运动条件下，事件率曲线噪声显著增加，但 ESVA 仍能准确定位谷底，侧面事件分布图显示估计时刻的事件边缘最为锐利。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/008_Figure_5.jpg]]
*Figure 5: EVK4 (focusboard-dark-motion): metric curves and estimated focus timestamps. Red dashed: estimate; black solid: ground truth. Event distributions within 1 ms are visualized around each estimate*

### 挑战性数据集（EAD）定量结果

Table 4 报告了 EAD 数据集的平均距离误差（µm）。该数据集包含极低光照和复杂运动场景，传统基于帧的相机在此条件下已无法捕获清晰图像。ESVA 在所有条件下均取得最优结果，**平均距离误差为 65.38 µm**。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/010_Table_4.jpg]]
*Table 4: Results on the challenging EAD dataset. Average focusing distance error (µm) under different illumination and motion conditions. Best result per row in bold*

Figure 6 可视化了 EAD 数据集中多个挑战性场景的定性对比。在 `camel`、`cactus`、`construction` 等暗光静态场景以及 `bottle drone`、`focusboard` 等暗光运动场景中，ESVA 的对焦结果均最接近真值图像。相比之下，其他方法在低光条件下容易出现较大偏差。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of challenging scenarios from the EAD dataset. The top three rows correspond to dark static scenes (camel, cactus, construction), and the bottom two rows show more challenging dark motion scenes (bottle drone, focusboard). Each column represents a different autofocus method, with the last column showing the ground-truth image. In such low-light and dynamic conditions, conventional frame-based cameras fail to capture clear images, while event-based methods remain functional. Focus error (in µm) is annotated in each subfigure*

### 消融实验

Figure 7 通过三组消融实验验证了各结构模块的贡献：

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/012_Figure_7.jpg]]
*Figure 7: Ablation study of the proposed structural modules. (Top) Spatiotemporal smoothing evaluated on DAVIS dataset / focusboard-bright-motion (error in ms). (Middle) Consistency filtering evaluated on EAD / crossroad-dark-static (focus error in µm). (Bottom) Dual-peak constraint evaluated on DAVIS dataset / ghost-bright-motion (error in ms). In each case, the temporal curves compare the metric evolution with and without the corresponding component. The qualitative images show the frame at the estimated focus moment, overlaid with the event distribution (red: positive events; blue: negative events). A clearer frame and sharper event indicate a more accurate focus estimation*

- **去除结构平滑模块**（Figure 7 Top）：高频振荡破坏事件率曲线的谷底结构，导致对焦误差大幅增加。在 DAVIS `focusboard-bright-motion` 序列上，去除平滑后估计时刻的事件分布明显发散。
- **去除一致性滤波模块**（Figure 7 Middle）：瞬态运动噪声引入虚假峰值，导致谷底定位错误。在 EAD `crossroad-dark-static` 序列上，去除一致性滤波后对焦误差显著增大。
- **去除双峰约束模块**（Figure 7 Bottom）：算法可能在极端散焦位置错误对焦，降低可靠性。在 DAVIS `ghost-bright-motion` 序列上，去除双峰约束后估计焦点偏离真值。

三组消融一致表明：三个模块各自承担不可替代的角色——平滑保留全局结构、一致性滤波消除瞬态噪声、双峰约束限定有效搜索区间。

### 运行效率

Table 5 报告了各方法在不同数据集上的运行时间。ESVA 的所有操作（平滑、一致性滤波、双峰检测）均为单次遍历过程，无需迭代优化，整体复杂度为 $O(N)$（$N$ 为焦点采样点数）。在相同硬件条件下（Intel i9 CPU），ESVA 的运行时间与其他方法相当或更优，验证了其实用性。

![[assets/figures/papers/paper_list_l2478_https_openaccess_thecvf_com_content_CVPR2026_html_Xiang_Event_Structural/figures/013_Table_5.jpg]]
*Table 5: Runtime comparison (ms) on different event autofucus datasets*

### 失败模式与局限性

尽管 ESVA 在大多数场景下表现优异，实验也揭示了其局限性：

1. **剧烈运动退化**：在 SYN 数据集的大幅抖动条件下，ESVA 误差（11.25 ms）略高于 ELP（9.43 ms）。当运动幅度过大时，事件率曲线被噪声严重污染，双峰结构难以可靠检测，谷底定位精度下降。
2. **多深度层场景**：当前公式假设扫掠过程中场景由单一主导深度层控制对焦目标。在多深度层共存时，事件率曲线可能出现更复杂的多峰结构，此时仅依赖全局谷底可能无法正确选择对焦目标。该问题在 EAD 数据集的某些复杂场景中已有体现，需要进一步引入空间约束或任务特定先验来提升可靠性。

## 方法谱系与知识库定位

### 1. 核心瓶颈：最大事件率假设的根本性缺陷

事件相机自动对焦领域长期被一个直观但物理上错误的假设所主导：**对焦最清晰时，边缘处亮度变化最剧烈，因此触发的事件数量应达到最大**。基于该假设的方法将自动对焦建模为事件率曲线上的全局最大值搜索问题。

然而，本文从物理光学和事件生成机制出发，揭示了这一假设的致命缺陷。精准对焦（散焦尺度 $\sigma = 0$）时，边缘过渡最为紧凑，模糊激活区域 $\Omega(\sigma)$ 的面积实际上处于**局部最小值**；轻微散焦导致边缘扩展、激活区域增大，事件率随之上升并形成两个主导峰；进一步散焦则梯度减弱、激活区域萎缩。因此，事件率曲线 $R(f)$ 在焦点扫掠过程中呈现**非单调的双峰谷结构**，真实焦点位于两峰之间的谷底，而非峰值处。

这一发现从根本上改写了事件相机自动对焦的问题定义：从“寻找最大事件率”转变为“在双峰约束区间内定位事件率最小值”。

### 2. 方法谱系与关键差异

#### 2.1 最大事件率范式（MER）

- **ER+EGS**（Lin et al., CVPR 2022）：将事件率作为对焦度量，采用黄金分割搜索加速峰值定位。该方法继承了 MER 假设，在精准对焦时事件率下降的物理事实面前存在系统性偏差。
- **OLE'23**（Ge et al., Optics and Lasers in Engineering 2023）：利用事件极性平衡作为显微对焦判据，本质上仍依赖事件活动量的极值搜索。
- **PBF**（Bao et al., Optics Express 2023）：基于事件极性对称性实现快速对焦，同样未脱离事件活动量最大化框架。
- **ELP**（Bao et al., CVPR 2025）：单步事件驱动高速对焦，是当前 MER 范式中性能最强的代表，在 SYN 数据集上平均时间戳误差为 8.68 ms。

上述方法的共同瓶颈在于：**对焦判定准则**选择事件率最大位置，而非物理真实的谷底位置；**缺乏峰值检测与搜索区间约束**，使用全局最大值导致搜索范围不受限；**曲线去噪与正则化**仅依赖简单滤波或无显式处理。

#### 2.2 ESVA 的范式转换

ESVA 在三个关键维度上实现了对 MER 范式的系统性替代：

| 维度 | MER 范式 | ESVA 范式 |
|------|----------|-----------|
| 对焦判定准则 | 选择事件率最大位置 | 选择双峰之间谷底位置（Eq. 8, Corollary 1） |
| 峰值检测与搜索区间 | 全局最大值，无显式峰值检测 | 检测两个主导峰，约束搜索区间为 $[P_1, P_2]$（Eq. 12-13） |
| 曲线去噪与正则化 | 无或简单滤波 | 高斯结构平滑 + 一致性滤波（局部线性投影）（Eq. 9-11） |

ESVA 的流水线由六个模块构成：事件率曲线计算（Eq. 2）→ 结构平滑（Eq. 9）→ 一致性滤波（Eq. 10-11）→ 双峰约束（Eq. 12-13）→ 谷底定位（Eq. 14）→ 置信度评估（Eq. 15）。所有操作均为单次遍历、无迭代优化，整体复杂度为 $O(N)$，与焦点采样数线性相关。

### 3. 适用边界与局限

#### 3.1 已验证的适用场景

实验覆盖四个数据集、三种传感器（SYN 合成、DAVIS、EVK4、EAD 显微），涵盖静态、小抖动、大抖动、低光照、暗场景运动等多种条件。ESVA 在 SYN 平均误差 6.62 ms（较 ELP 提升 24%）、DAVIS 平均误差 1.30 ms、EVK4 平均误差 4.22 ms、EAD 平均距离误差 65.38 µm，展示了跨传感器、跨场景的泛化能力。

消融实验（Figure 7）分别验证了三个结构模块的必要性：去除时空平滑后高频振荡破坏谷底结构；去除一致性滤波后瞬态运动噪声引入虚假峰值；去除双峰约束后算法可能在极端散焦位置错误对焦。

#### 3.2 已知局限

论文明确指出的核心局限是：**当前理论模型假设扫掠过程中场景由单一主导深度层控制对焦目标**。当场景中存在多个竞争深度层时，事件率曲线可能呈现更复杂的多峰多谷结构，单纯依赖全局双峰约束可能失效。此时需要引入额外的空间约束或任务特定先验来区分不同深度层对应的谷底。

此外，在 SYN (Huge Shake) 条件下，ESVA 误差（11.25 ms）略高于 ELP（9.43 ms），提示在极端运动模糊下，事件率曲线结构可能被严重破坏，结构正则化的鲁棒性存在上限。

### 4. 开放问题

论文提出了两个值得进一步探索的方向：

1. **多模态融合**：如何融合事件极性模式、强度变化或空间先验信息，实现联合对焦估计以进一步提升精度和泛化能力？当前 ESVA 仅使用事件数量信息，丢弃了极性、空间分布等潜在有用信号。

2. **多深度层场景**：在多个竞争深度层共存时，事件率曲线的结构会发生怎样的变化？如何设计空间约束或任务特定约束以鲁棒地处理此类场景？这是从单深度层理论模型走向通用事件相机自动对焦系统的关键障碍。

### 5. 知识库定位

ESVA 在事件相机自动对焦领域完成了从“经验假设驱动”到“物理理论驱动”的范式转换。其核心贡献不仅是提出一种性能更优的算法，更在于建立了首个解释事件率双峰谷结构的理论模型（Proposition 1, Corollary 1），并基于该理论设计了结构正则化框架。该框架无需图像重建、无需监督信号，完全在事件域内运行，为后续研究提供了可解释、可扩展的理论基础。

## 原文 PDF

![[paperPDFs/CVPR_2026/Event_Structural_Valley_A_Unified_Theoretical_and_Practical_Framework_for_Event_Camera_Autofocus.pdf]]

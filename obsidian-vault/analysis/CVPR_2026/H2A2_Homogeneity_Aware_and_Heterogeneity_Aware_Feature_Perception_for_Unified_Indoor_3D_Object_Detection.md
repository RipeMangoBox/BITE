---
title: "H^2A^2: Homogeneity-Aware and Heterogeneity-Aware Feature Perception for Unified Indoor 3D Object Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/H_2A_2_Homogeneity_Aware_and_Heterogeneity_Aware_Feature_Perception_for_Unified_Indoor_3D_Object_Detection.pdf
project_link: null
code_link: null
aliases:
- H22
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 场景结构感知的卷积核权重选择（SF-KS）：通过学习偏移有效性先验和结构一致性后验，动态决定稀疏卷积核中各偏移的权重共享或专用，从而分离并增强同质特征，同时保留场景特异异质特征。
primary_logic: 室内场景中，基本几何结构（如线、面、角）在不同场景中激发相似的稀疏卷积核偏移模式，构成跨场景同质特征；而场景特有布局、尺度等因素产生异质响应。联合建模并自适应分离这两类特征，能显著提升统一室内3D目标检测的性能与泛化性。
claims:
- 图1展示不同物体和场景中相似结构引发的同质化卷积核偏移表示，说明跨场景几何同质性的存在。
- SF-KS通过任务感知线性调制、偏移有效性先验与结构一致性后验选择核权重，实现同质/异质特征分离。
- NGH算法通过归一化并动态重加权各任务梯度范数，缓解多源联合优化中的梯度冲突，稳定训练。
- Table 1显示H^2A^2在ScanNet v2、SUN RGB-D、S3DIS上均显著优于TR3D等基线，验证了方法的有效性。
---

# H^2A^2: Homogeneity-Aware and Heterogeneity-Aware Feature Perception for Unified Indoor 3D Object Detection

> [!tip] 核心洞察
> 室内场景中，基本几何结构（如线、面、角）在不同场景中激发相似的稀疏卷积核偏移模式，构成跨场景同质特征；而场景特有布局、尺度等因素产生异质响应。联合建模并自适应分离这两类特征，能显著提升统一室内3D目标检测的性能与泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | H^2A^2：面向统一室内3D目标检测的同质与异质特征感知 |
| 英文题名 | H^2A^2: Homogeneity-Aware and Heterogeneity-Aware Feature Perception for Unified Indoor 3D Object Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xie_H2A2_Homogeneity-Aware_and_Heterogeneity-Aware_Feature_Perception_for_Unified_Indoor_3D_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | H^2A^2 |
| Dataset | ScanNet v2, SUN RGB-D, S3DIS, 3RScan |

> [!tip] 效果简介
> - ScanNet v2 上，mAP@0.25 / mAP@0.5 77.5 / 63.8 vs 72.9 / 59.3 (+4.6 / +4.5)。
> - SUN RGB-D 上，mAP@0.25 / mAP@0.5 68.0 / 51.4 vs 67.1 / 50.4 (+0.9 / +1.0)。
> - S3DIS 上，mAP@0.25 / mAP@0.5 78.7 / 59.3 vs 74.5 / 51.7 (+4.2 / +7.6)。

## 概要

**核心问题：** 现有室内 3D 目标检测器在跨场景统一训练时，缺乏有效机制联合建模不同场景之间共享的同质几何特征与场景特有的异质特征。直接将骨干网络参数全场景共享，导致来自无关场景的异质信号相互干扰，限制了检测精度与泛化能力。

**核心洞察：** 室内场景中，基本几何结构（如线、面、角）在不同场景中会激发相似的稀疏卷积核偏移模式，构成跨场景**同质特征**；而场景特有的布局、尺度等因素则产生**异质响应**。自适应地分离并增强这两类特征，是提升统一室内 3D 检测性能的关键。

**方法定位：** 本文提出 **H^2A^2**（Homogeneity-Aware and Heterogeneity-Aware Feature Perception），包含两个核心组件：

- **结构特征感知核选择（SF-KS）**：嵌入稀疏卷积层，通过可学习的偏移有效性先验与结构一致性后验，动态决定卷积核中各偏移使用共享权重还是场景专用权重，从而在分离同质/异质特征的同时增强场景结构表示。
- **范数梯度均一化（NGH）**：在反向传播时监测各数据源梯度范数的不平衡程度，当冲突严重时触发梯度重缩放，使所有任务的梯度范数对齐后求平均，保留方向信息，防止大梯度任务支配优化。

**主要结果：** 在 ScanNet v2、SUN RGB-D、S3DIS 三个室内基准上，H^2A^2 以仅几何坐标输入，一致超越强基线 **TR3D**（Rukhovich et al., ICIP 2023）：ScanNet v2 mAP@0.25 由 72.9 提升至 77.5（+4.6），S3DIS mAP@0.5 由 51.7 提升至 59.3（+7.6）。在 3RScan 上的零样本泛化实验进一步验证了方法的迁移能力（mAP@0.25: 50.7 vs 47.6）。消融实验确认 SF-KS 与 NGH 各自贡献显著，且模块可迁移至 **FCAF3D**（Rukhovich et al., ECCV 2022）框架并带来一致提升。



### 室内3D目标检测的现状与瓶颈

室内3D目标检测旨在从点云输入中定位并识别物体，是场景理解、机器人导航等应用的基础任务。现有方法主要分为两类：基于霍夫投票的方法（如 **VoteNet**，Qi et al., ICCV 2019）、基于混合几何基元的方法（如 **H3DNet**，Zhang et al., ECCV 2020）、基于Transformer的方法（如 **GroupFree3D**，Liu et al., ICCV 2021），以及近年来表现出更强性能的anchor-free稀疏体素检测器（如 **FCAF3D**，Rukhovich et al., ECCV 2022；**TR3D**，Rukhovich et al., ICIP 2023）。

然而，这些方法在面向**统一室内检测**（即单一模型同时覆盖多个场景数据集）时，面临一个根本性瓶颈：**现有检测器缺乏联合建模跨场景同质几何特征与场景特异性异质特征的有效机制**。当骨干网络在所有场景间直接共享时，来自不同场景的异质信号会相互干扰，限制了检测精度与泛化性。

### 核心洞察：室内场景中的同质性与异质性

论文通过观察稀疏卷积核在不同场景中的偏移模式，揭示了一个关键现象：**室内场景中，基本的几何结构（如线、面、角）在不同场景中会激发相似的卷积核偏移表示**，构成跨场景的**同质特征**（homogeneous features）；而场景特有的布局、尺度等因素则产生**异质响应**（heterogeneous features）。Figure 1 直观展示了这一现象——边界结构、平面结构和线性结构在不同物体和场景中均能诱导出高度相似的核偏移模式。

这一洞察意味着：若能有效分离并增强同质特征，同时保留场景特异的异质特征，就可以在统一检测框架下同时提升精度与泛化性。然而，现有方法将卷积核权重在所有场景间无差别共享，既无法显式利用同质几何先验，也无法隔离异质信号的干扰。

### 多源联合训练的梯度冲突

统一检测的另一个实际挑战来自**多源数据联合训练中的梯度冲突**。当多个数据集（如ScanNet v2、SUN RGB-D、S3DIS）被分配到不同GPU秩（rank）并行训练时，各数据源的梯度范数可能存在严重不平衡。直接平均这些梯度会导致大梯度任务支配共享参数的更新方向，使小梯度任务的优化被边缘化。这一问题在多数据集联合训练中普遍存在，但缺乏轻量且有效的解决方案。

### 本文动机与贡献

针对上述瓶颈，H^2A^2 提出两个互补的核心机制：

1. **结构特征感知的卷积核选择（SF-KS）**：通过学习偏移有效性先验和结构一致性后验，动态决定稀疏卷积核中各偏移的权重是共享还是专用，从而在骨干网络中实现同质特征的分离与增强，同时保留场景特异异质特征。

2. **范数梯度均一化（NGH）**：通过归一化并动态重加权各任务梯度范数，缓解多源联合优化中的梯度冲突，使训练过程更加稳定高效。

这两个机制分别从**特征感知**和**优化策略**两个层面，系统性地解决了统一室内3D检测中的同质/异质特征建模与多源训练协同问题。



## 核心方法与创新机理

H^2A^2 的核心创新在于首次从**稀疏卷积核偏移的同质/异质响应**视角重新审视统一室内3D检测问题，并提出两个紧密协同的机制：面向特征感知的**结构特征感知核选择（SF-KS）**与面向优化稳定的**范数梯度均一化（NGH）**。

### 1. 问题洞察：稀疏卷积中的同质与异质信号冲突

现有统一室内3D检测器通常将所有场景的数据混合后直接送入共享骨干网络，忽略了跨场景特征的二重性（Figure 1）：

- **同质特征**：基本几何结构（如线、面、角）在不同场景中激发**相似的稀疏卷积核偏移模式**，构成可共享的通用表示。
- **异质特征**：场景特有的布局、尺度、物体分布等因素产生**场景特异性响应**，强行共享会引入相互干扰。

当骨干网络不加区分地共享所有卷积核权重时，异质信号之间的冲突会削弱同质特征的提取，限制检测精度与泛化性。H^2A^2 的核心洞察是：**自适应地分离同质与异质特征，而非简单共享或完全独立，是提升统一检测性能的关键**。

### 2. 结构特征感知核选择（SF-KS）

SF-KS 是嵌入稀疏卷积层的自适应核权重选择机制，由三个子组件串联构成，实现从“场景结构感知”到“核权重决策”的闭环：

**（1）任务感知线性调制（TLM）**  
在卷积操作之前，利用可学习的场景嵌入 $F_{scene} \in \mathbb{R}^{C_t}$ 通过轻量 MLP $\mathcal{F}$ 生成通道级仿射参数 $(\varphi, \theta)$，对输入特征 $F_{in}$ 进行逐通道调制：

$$(\varphi, \theta) = \mathcal{F}(F_{scene}), \quad \widehat{F}_{in} = F_{in} \odot \varphi + \theta$$

这一步骤增强了特征中的场景结构表示，为后续核选择提供更丰富的结构线索（Figure 3）。

**（2）核权重选择：偏移有效性先验与结构一致性后验**  
SF-KS 将每个稀疏卷积核偏移 $j$ 的权重决策建模为二值判别问题：

- **偏移有效性先验 $\alpha_j$**：一组可学习参数经 sigmoid 激活得到 $\alpha = \sigma(O) \in (0,1)^V$，表示各偏移在几何层面的可靠性分数。
- **结构一致性后验 $\beta_j$**：通过核原型向量与场景点云特征的余弦相似度度量，判断当前场景结构是否支持该偏移的共享（Figure 4）。

两者融合后经阈值 $\tau$ 二值化，得到判别分数 $\gamma_j$：

$$\gamma_j = \text{Binarization}(\alpha_j \beta_j; \tau)$$

最终卷积核权重由共享核 $W_j^{sh}$ 与专用核 $W_j^{ex}$ 插值得到：

$$W_j = \gamma_j W_j^{sh} + (1 - \gamma_j) W_j^{ex}$$

当 $\gamma_j=1$ 时使用共享权重（捕获同质特征），$\gamma_j=0$ 时使用专用权重（保留异质特征），实现**偏移级别的自适应分离**。

**（3）任务感知通道门控**  
卷积输出后，通过场景向量生成门控信号 $g = \sigma(\text{MLP}(F_{scene}))$，对输出特征进行通道级重校准 $F = F_{out} \odot (1+g)$，进一步强化场景适应性。

### 3. 范数梯度均一化（NGH）

多数据集联合训练时，不同数据源的梯度范数差异可能导致大梯度任务主导参数更新，造成优化不稳定。NGH 在反向传播阶段对共享参数的梯度进行秩间重缩放：

- **触发条件**：计算各秩梯度范数的两两相似度 $\Psi$，当 $\Psi < \gamma$ 时判定为严重冲突，触发均一化。
- **重缩放策略**：将各秩梯度范数对齐至目标范数 $M_t$，保留方向不变：

$$s_k = \frac{M_t}{n_k + \varepsilon}, \quad \tilde{g}_k^p = s_k g_k^p$$

缩放后的梯度再进行跨秩平均 $\bar{g}^p = \frac{1}{K} \sum_{k=1}^K \tilde{g}_k^p$，实现平衡的参数更新（Figure 5）。

### 4. 创新点总结

| 改进维度 | baseline（TR3D） | H^2A^2 创新 | 机制 |
|---------|-----------------|-------------|------|
| 特征调制 | 无 | 任务感知线性调制 | 场景嵌入生成通道仿射参数，增强结构表示 |
| 核权重策略 | 所有场景共享同一核 | 偏移级自适应选择 | 先验+后验二值判别，分离同质/异质特征 |
| 通道后处理 | 无 | 任务感知通道门控 | 场景向量门控输出通道重校准 |
| 梯度聚合 | 直接平均 | 范数梯度均一化 | 冲突检测+范数对齐+方向保留 |

SF-KS 与 NGH 形成**特征-优化协同**：SF-KS 在结构层面分离同质/异质信号，提升特征质量；NGH 在优化层面平衡多源梯度，保障训练稳定性。两者共同解决了统一室内3D检测中“共享什么、保留什么、如何稳定学习”的核心问题。



H^2A^2 的整体架构建立在一个稀疏3D CNN骨干网络之上，核心目标是**在统一的多场景联合训练框架中，自适应地分离并增强跨场景同质几何特征，同时保留场景特异性的异质特征**。整个pipeline由三个关键组件构成：MinkResNet骨干、结构特征感知核选择模块（SF-KS）和范数梯度均一化算法（NGH），如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/002_Figure_2.jpg]]
*Figure 2: Overview architecture of*

**输入与骨干网络**：系统接收仅包含几何坐标的点云输入，通过 **MinkResNet** 稀疏3D CNN骨干进行多层级特征提取（Section 3.1）。骨干网络中的稀疏卷积层是SF-KS模块的嵌入载体。

**SF-KS模块——特征感知的核心机制**：SF-KS嵌入在稀疏卷积层中，通过三个子组件实现同质/异质特征的自适应分离（Section 3.2）：
1. **任务感知线性调制（TLM）**：利用可学习场景嵌入 $F_{scene}$ 生成通道级仿射参数 $(\varphi, \theta)$，对输入特征进行逐通道调制 $\widehat{F}_{in} = F_{in} \odot \varphi + \theta$，增强场景结构表示（Figure 3）。
2. **核权重选择**：融合**偏移有效性先验** $\alpha = \sigma(O)$（可学习参数经sigmoid）和**结构一致性后验** $\beta$（原型向量与场景特征的余弦相似度，Figure 4），生成判别分数 $\gamma_j$，经二值化决定第 $j$ 个偏移使用共享核权重还是专用核权重：$W_j = \gamma_j W_j^{sh} + (1-\gamma_j) W_j^{ex}$。
3. **任务感知通道门控**：通过场景向量生成门控信号 $g = \sigma(MLP(F_{scene}))$，对输出特征进行通道级重校准 $F = F_{out} \odot (1+g)$。

**NGH算法——多源联合训练的稳定器**：在多数据集联合训练时，每个数据源绑定到不同GPU rank。NGH在反向传播阶段计算各秩梯度范数的两两相似度 $\Psi$，当 $\Psi < \gamma$（即梯度范数严重不平衡）时触发均一化：将所有秩的梯度范数对齐至目标范数 $s_k = M_t / (n_k + \varepsilon)$，保留梯度方向后进行跨秩平均 $\bar{g}^p = \frac{1}{K} \sum_{k=1}^K \tilde{g}_k^p$（Section 3.3，Figure 5）。这有效缓解了多源联合优化中的梯度冲突。

**检测头**：骨干网络输出的多层级特征送入**多级检测头**，基于深度对齐的点云管道回归有向3D边界框及类别（Section 3.1）。

整个pipeline的信息流可概括为：点云 → MinkResNet（含SF-KS增强的稀疏卷积层）→ 多级特征 → 检测头 → 3D边界框；同时，NGH在反向传播时介入共享参数的梯度更新，确保多场景联合训练的稳定性。

### 补充图表

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/001_Figure_1.jpg]]
*Figure 1: Explaining the homogenized spatial responses induced by similar structural patterns across different objects in varied scene. (a)(f) represent the convolution kernel offset representation induced by boundary structures; (b)(d)(e) represent the offset representation induced by planar structures; (c) represents the kernel offset representation induced by linear structures*



H^2A^2 的核心由两个模块构成：结构特征感知核选择（SF-KS）与范数梯度均一化（NGH）。SF-KS 嵌入稀疏卷积层，负责分离并增强同质/异质特征；NGH 作用于反向传播，缓解多数据源联合训练中的梯度冲突。

### 3.1 结构特征感知核选择（SF-KS）

SF-KS 包含三个子组件：任务感知线性调制（TLM）、混合稀疏卷积核权重选择、任务感知通道门控。

**任务感知线性调制（TLM）** 在卷积前对输入特征进行场景自适应增强。引入一组可学习的场景嵌入 $F_{scene} \in \mathbb{R}^{C_t}$，通过轻量调制函数 $\mathcal{F}$ 生成通道级仿射参数：

$$(\varphi, \theta) = \mathcal{F}(F_{scene}), \quad \varphi, \theta \in \mathbb{R}^{C_{in}}$$

随后对输入特征 $F_{in}$ 逐通道调制：

$$\widehat{F}_{in} = F_{in} \odot \varphi + \theta, \quad \widehat{F}_{in} \in \mathbb{R}^{N \times C_{in}}$$

**混合稀疏卷积核权重选择** 是 SF-KS 的核心机制。对于稀疏卷积中 $V$ 个偏移位置，每个位置 $j$ 维护一对权重：共享核 $W_j^{sh}$ 和专用核 $W_j^{ex}$。最终权重由判别分数 $\gamma_j$ 在二者间插值：

$$W_j = \gamma_j W_j^{sh} + (1 - \gamma_j) W_j^{ex}, \quad j = 1, \ldots, V$$

其中 $\gamma_j$ 由偏移有效性先验 $\alpha_j$ 与结构一致性后验 $\beta_j$ 融合后二值化得到：

$$\gamma_j = \text{Binarization}(\alpha_j \beta_j; \tau)$$

- **偏移有效性先验** $\alpha = \sigma(O) \in (0,1)^V$：可学习参数 $O$ 经 sigmoid 得到，反映各偏移位置对跨场景共享的固有可靠性。
- **结构一致性后验** $\beta_j$：通过核原型向量与场景点云特征计算余弦相似度得到，衡量当前场景结构与第 $j$ 个偏移模式的匹配程度。
- **二值化阈值** $\tau$：当 $\alpha_j \beta_j \ge \tau$ 时 $\gamma_j = 1$（使用共享核），否则 $\gamma_j = 0$（使用专用核）。

**任务感知通道门控** 在卷积输出后对通道进行软选择。利用场景向量生成门控信号：

$$g = \sigma(MLP(F_{scene})) \in (0,1)^C$$

输出特征重校准为：

$$F = F_{out} \odot (1 + g)$$

### 3.2 范数梯度均一化（NGH）

多数据源联合训练时，各数据秩（rank）上共享参数的梯度范数可能严重失衡，导致大梯度任务支配优化方向。NGH 通过监控秩间梯度范数相似性，在失衡严重时触发均一化。

设 $K$ 个数据秩上共享参数 $p$ 的局部梯度为 $\{g_k^p\}_{k=1}^K$，其范数为 $n_k = \|g_k^p\|_2$。秩间梯度范数相似性定义为：

$$\Psi = \frac{1}{K(K-1)} \sum_{i \neq j} \frac{2 n_i n_j}{n_i^2 + n_j^2 + \varepsilon}$$

$\Psi \in (0,1]$，值越小表示范数失衡越严重。当 $\Psi < \gamma$（预设阈值）时触发均一化：计算目标范数 $M_t$（通常取各秩范数的均值），为每个秩计算缩放因子：

$$s_k = \frac{M_t}{n_k + \varepsilon}$$

对局部梯度进行范数对齐，保留方向：

$$\tilde{g}_k^p = s_k \cdot g_k^p$$

最终全局梯度为缩放后梯度的跨秩平均：

$$\bar{g}^p = \frac{1}{K} \sum_{k=1}^K \tilde{g}_k^p$$

当 $\Psi \ge \gamma$ 时，梯度冲突轻微，直接对原始梯度取平均，不触发缩放。

### 3.3 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|----------|------|
| $(\varphi, \theta) = \mathcal{F}(F_{scene})$ | $F_{scene}$: 场景嵌入; $\varphi,\theta$: 通道仿射参数 | 生成场景自适应调制参数 |
| $\widehat{F}_{in} = F_{in} \odot \varphi + \theta$ | $\widehat{F}_{in}$: 调制后特征; $F_{in}$: 原始输入特征 | 增强场景结构表示 |
| $\alpha = \sigma(O)$ | $O$: 可学习参数; $\alpha$: 偏移有效性先验 | 学习各偏移的跨场景可靠性 |
| $\gamma_j = \text{Binarization}(\alpha_j \beta_j; \tau)$ | $\beta_j$: 结构一致性后验; $\tau$: 二值化阈值 | 决定偏移使用共享/专用核 |
| $W_j = \gamma_j W_j^{sh} + (1-\gamma_j) W_j^{ex}$ | $W_j^{sh}$: 共享核; $W_j^{ex}$: 专用核 | 混合卷积核权重 |
| $g = \sigma(MLP(F_{scene}))$ | $g$: 通道门控信号 | 生成输出通道选择权重 |
| $F = F_{out} \odot (1+g)$ | $F_{out}$: 卷积输出; $F$: 门控后特征 | 输出通道重校准 |
| $\Psi = \frac{1}{K(K-1)} \sum_{i \neq j} \frac{2 n_i n_j}{n_i^2 + n_j^2 + \varepsilon}$ | $n_i$: 第 $i$ 秩梯度范数; $\Psi$: 范数相似性 | 衡量秩间梯度失衡程度 |
| $\tilde{g}_k^p = s_k g_k^p, \ s_k = \frac{M_t}{n_k+\varepsilon}$ | $s_k$: 缩放因子; $M_t$: 目标范数 | 对齐梯度范数，保留方向 |

### 补充图表

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the task-aware linear modulation process, where a modulation function takes the scene embedding as input to generate modulation parameters*

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/004_Figure_4.jpg]]
*Figure 4: The kernel prototype vector queries the scene point cloud features to measure their similarity, thereby obtaining the structural consistency posterior*

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/005_Figure_5.jpg]]
*Figure 5: Two-case schematic for NGH. Black: original rank gradients; red: naive mean; blue: result after norm-based homogenization (directions preserved). NGH activates only when Ψ*



## 实验与关键发现

### 主实验结果

H^2A^2 在三个主流室内 3D 目标检测基准上均显著超越直接基线 **TR3D**（Rukhovich et al., ICIP 2023），验证了同质/异质特征感知机制的有效性。Table 1 汇总了基于纯几何输入的方法对比：

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/006_Table_1.jpg]]
*Table 1: Results of*

- **ScanNet v2**：H^2A^2 达到 mAP@0.25 77.5%（+4.6）和 mAP@0.5 63.8%（+4.5），在所有对比方法中排名第一。
- **SUN RGB-D**：mAP@0.25 68.0%（+0.9），mAP@0.5 51.4%（+1.0），提升幅度相对较小，可能与 SUN RGB-D 场景多样性更高、异质特征更分散有关。
- **S3DIS**：mAP@0.25 78.7%（+4.2），mAP@0.5 59.3%（+7.6），在 mAP@0.5 上的增益尤为突出，表明 H^2A^2 对高 IoU 阈值的定位精度有显著改善。

值得注意的是，H^2A^2 在 S3DIS 上的 mAP@0.5 提升（+7.6）远大于 mAP@0.25（+4.2），暗示 SF-KS 模块对边界框精度的优化效果在严格 IoU 条件下更为明显。这与其设计目标一致：通过分离同质几何特征，网络能更精确地回归物体边界。

### 消融实验

**模块逐步添加**（Table 2）。以 TR3D 为起点，逐步添加 SF-KS 和 NGH 模块，三个数据集上均呈现单调提升：

1. TR3D（baseline）：共享卷积核，直接平均梯度。
2. +SF-KS：引入场景感知核选择，ScanNet mAP@0.25 提升约 3 个点。
3. +NGH：在 SF-KS 基础上叠加梯度均一化，进一步带来约 1-2 个点的增益。
4. H^2A^2（完整版）：达到最优性能。

这表明 SF-KS 是性能提升的主要驱动因素，而 NGH 在多数据源联合训练时起到稳定优化、减少梯度冲突的辅助作用。

**任务感知线性调制（TLM）消融**（Table 4）。对比三种变体：
- w/o TLM：移除线性调制，直接使用原始特征。
- LA（线性注意力）：用线性注意力替代 TLM 进行场景特征增强。
- TLM（H^2A^2 采用）：可学习场景嵌入生成通道级仿射参数。

TLM 在所有数据集上均优于 w/o TLM 和 LA，验证了通道级仿射调制对增强场景结构表示的有效性。LA 变体表现介于两者之间，说明简单的注意力机制无法完全替代显式的场景调制。

**模块迁移性验证**（Table 3）。将 SF-KS 和 NGH 集成到另一 anchor-free 检测器 **FCAF3D**（Rukhovich et al., ECCV 2022）中，ScanNet mAP@0.25 从 70.3% 提升至 73.6%（+3.3），SUN RGB-D 提升 1.8 个点，证明所提模块不依赖于特定骨干网络，具有良好的通用性。

### 零样本泛化

在 3RScan 数据集上的零样本迁移实验（Table 5）中，H^2A^2 相比 TR3D 在 mAP@0.25 上提升 3.1 个点（50.7% vs. 47.6%），mAP@0.5 提升 1.5 个点（39.1% vs. 37.6%）。这表明通过分离同质几何特征，模型学习到了更泛化的场景结构表示，而非过拟合训练场景的特异模式。

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/011_Table_5.jpg]]
*Table 5: Zero-shot generalization comparison between*

### 定性分析

**检测结果可视化**（Figure 6）。与 TR3D 相比，H^2A^2 生成的 3D 边界框更紧凑，误检更少。在复杂室内场景中，TR3D 容易出现边界框偏移或重复检测，而 H^2A^2 能更准确地定位物体边界，验证了同质特征增强对几何定位精度的改善。

**特征空间可视化**（Figure 7）。t-SNE 降维显示，H^2A^2 学习到的同质特征（homogeneous features）在不同场景间呈现聚类趋势，而异质特征（heterogeneous features）则保持场景特异性分布。这直接验证了 SF-KS 模块确实实现了两类特征的有效分离。

### 失败模式与局限

尽管 H^2A^2 在室内基准上表现优异，但存在以下局限：

1. **场景范围受限**：当前仅在 ScanNet、S3DIS、SUN RGB-D 三个室内数据集上验证，未扩展到室外自动驾驶等场景。室外场景的几何结构差异更大，SF-KS 的核选择机制能否有效泛化仍需验证。

2. **超参数敏感性**：核选择中的二值化阈值 τ 和 NGH 中的激活阈值 γ 需要手动设定。论文未对这些阈值进行充分的敏感性分析，其选择对性能的影响程度不明确。

3. **仅支持几何输入**：当前方法仅使用点云坐标，未探索结合 RGB 颜色信息的情况。在多模态输入下，SF-KS 的特征分离机制是否仍然有效是开放问题。

4. **多场景扩展性未知**：当前联合训练仅涉及三个数据集（对应三个 GPU rank），当扩展到更多场景（>3）时，SF-KS 的核选择空间和 NGH 的梯度平衡策略的可扩展性尚未验证。

### 补充图表

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of 3D detection results. Compared with TR3D*

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/009_Table_3.jpg]]
*Table 3: Transferability of the proposed modules: ablation after integration into the FCAF3D baseline*

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/010_Table_4.jpg]]
*Table 4: Ablation study of Task-aware Linear Modulation (TLM) on ScanNet v2, SUN RGB-D and S3DIS datasets*

![[assets/figures/papers/paper_list_l2518_https_openaccess_thecvf_com_content_CVPR2026_html_Xie_H2A2_Homogeneity_A/figures/012_Figure_7.jpg]]
*Figure 7: Visualization of t-SNE from learned homogeneous and Heterogeneous features with our proposed*



## 定位与知识库关联

### 1. 基线关系与继承

H^2A^2 直接构建于 **TR3D**（Rukhovich et al., ICIP 2023）的 anchor-free 稀疏体素检测框架之上，继承其 MinkResNet 骨干与深度对齐的点云检测头。与 TR3D 在所有场景共享同一个稀疏卷积核权重不同，H^2A^2 在卷积层中嵌入结构特征感知核选择（SF-KS）模块，使网络能够感知场景结构并动态决定各卷积核偏移的权重共享或专用策略。这一改动保持了与 TR3D 完全相同的输入（仅几何坐标）和训练配置，确保了对比的公平性。

在更早的方法谱系中，**VoteNet**（Qi et al., ICCV 2019）开创了基于霍夫投票的室内 3D 检测范式，**H3DNet**（Zhang et al., ECCV 2020）通过混合几何基元增强几何推理，**GroupFree3D**（Liu et al., ICCV 2021）则引入 Transformer 消除手工分组。这些工作均聚焦于单数据集训练，未涉及跨场景的特征同质/异质建模。H^2A^2 的贡献不在于改变检测范式，而在于提出一种通用的稀疏卷积层增强机制，使得多数据集联合训练时能够自适应分离共享与专用特征。

模块迁移性实验（Table 3）进一步表明，SF-KS 和 NGH 可无缝集成至 **FCAF3D**（Rukhovich et al., ECCV 2022）框架，在 ScanNet v2、SUN RGB-D 和 S3DIS 上均带来显著提升，验证了该方法作为即插即用组件的通用性。

### 2. 适用边界与约束

**场景域限制**：当前验证全部集中在室内场景数据集（ScanNet v2、SUN RGB-D、S3DIS、3RScan），未涉及室外自动驾驶（如 KITTI、nuScenes）或工业场景。室外场景的几何结构模式（如大规模平面、稀疏物体分布）与室内存在本质差异，SF-KS 中的结构原型向量和偏移有效性先验能否直接迁移尚需验证。

**输入模态限制**：所有实验仅使用几何坐标（XYZ）作为输入，未探索 RGB 颜色信息。当引入多模态输入时，SF-KS 的特征调制和核选择机制需要扩展以处理异构特征通道间的交互，当前框架对此缺乏设计。

**超参数敏感性**：核选择中的二值化阈值 τ 和 NGH 中的激活阈值 γ 均需手动设定。论文未对这些阈值进行消融，其在不同数据集组合下的最优取值和鲁棒性未知。实际部署时可能需要针对具体数据分布进行调参。

**联合训练规模**：当前最多联合训练 3 个数据集（ScanNet v2 + SUN RGB-D + S3DIS），每个数据集绑定到独立 GPU rank。当扩展到更多数据集（如 >5）时，场景嵌入的区分能力、NGH 的梯度重缩放效率以及 GPU 资源分配策略均面临可扩展性挑战。

### 3. 局限性与已知问题

1. **结构原型向量的表达能力**：SF-KS 使用可学习的核原型向量与场景特征计算余弦相似度作为结构一致性后验。原型向量的维度和更新机制（随网络端到端训练）是否足以捕捉细粒度的几何差异（如不同风格的家具边界）缺乏深入分析。当训练数据包含更多样化的场景时，固定数量的原型向量可能成为瓶颈。

2. **偏移有效性先验的数据依赖性**：α 作为可学习参数经 sigmoid 得到，其学习过程依赖于训练数据的偏移分布。若训练集与测试集的稀疏卷积偏移模式差异较大（如点云密度变化导致的有效偏移位置漂移），该先验可能失效。论文未提供跨密度或跨传感器泛化的分析。

3. **NGH 的方向保留假设**：NGH 在触发均一化时仅缩放梯度范数而保留方向，这假设了不同任务的梯度方向本身是相容的。当任务间存在方向性冲突（即梯度指向相反的优化方向）时，单纯范数对齐无法解决冲突，甚至可能放大噪声方向的影响。论文未对方向冲突程度进行量化分析。

4. **零样本泛化的上限**：在 3RScan 上的零样本实验（Table 5）显示 H^2A^2 相较 TR3D 有提升，但绝对 mAP@0.25 仅为 50.7%，远低于在训练域上的表现。这表明 SF-KS 学到的同质特征虽有一定泛化性，但面对全新的场景布局和物体类别时，异质特征的缺失仍限制了性能上限。

### 4. 开放问题

- **多模态扩展**：能否将 H^2A^2 扩展到 RGB+深度输入，并保持对几何同质特征和纹理异质特征的分离建模能力？这需要在 SF-KS 中设计跨模态的结构一致性度量。

- **大规模联合训练**：当联合训练数据集数量增至 5 个以上时，场景嵌入的判别性是否足够？NGH 的秩间梯度相似性度量 Ψ 是否会因秩数增加而退化？可能需要引入层次化场景分组或自适应秩合并策略。

- **自动化阈值选择**：τ 和 γ 的自动化或自适应选择机制值得探索，例如基于梯度统计的在线阈值调整，以减少人工调参负担并提升跨数据集鲁棒性。

- **室外场景泛化**：室内场景中有效的“线-面-角”几何基元在室外是否仍然构成主要的同质特征？可能需要重新定义结构原型以适应更大尺度、更稀疏的室外几何模式。

- **与 Foundation Model 的融合**：近期 3D 视觉基础模型（如 PointLLM、Uni3D）展现出强大的场景理解能力，H^2A^2 的场景嵌入和结构原型能否与这些预训练表示结合，进一步提升跨场景泛化？



## 原文 PDF

![[paperPDFs/CVPR_2026/H_2A_2_Homogeneity_Aware_and_Heterogeneity_Aware_Feature_Perception_for_Unified_Indoor_3D_Object_Detection.pdf]]

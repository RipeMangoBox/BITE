---
title: Self-Consistency for LLM-Based Motion Trajectory Generation and Verification
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Self_Consistency_for_LLM_Based_Motion_Trajectory_Generation_and_Verification.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Ma_Self-Consistency_for_LLM-Based_Motion_Trajectory_Generation_and_Verification_CVPR_2026_paper.html
project_link: https://majiaju.io/trajectoryself-consistency
code_link: null
aliases:
- SCMTGVLGH
- SCLBMTGV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过定义基于李群（Lie group）的几何变换层次结构（如刚性、相似性、仿射等），并构建变换不变距离度量，从而对采样轨迹进行聚类并选择最自洽的簇。
primary_logic: 将视觉提示映射为一个原型轨迹与一个几何变换群的组合，即同一族内的轨迹可以通过指定群内的扭曲（warp）相互转换，因此可以通过计算变换群下的不变距离来衡量轨迹间的一致性。
claims:
- 我们的方法在生成任务上将GPT-4.1和GPT-5的准确率分别提高4-6个百分点。
- 在验证任务上，我们的自洽性方法比VLM基线提高了11%的精度和5.6%的F1分数。
- 在已知正确变换群（oracle）的情况下，生成准确率可进一步提升，验证F1达到85.6。
- 224-prompt motion trajectory benchmark (generation) 上 Accuracy = 68.0 (Majority-Consensus, GPT-4.1); 83.3 (Majority-Consensu...
---

# Self-Consistency for LLM-Based Motion Trajectory Generation and Verification

> [!tip] 核心洞察
> 将视觉提示映射为一个原型轨迹与一个几何变换群的组合，即同一族内的轨迹可以通过指定群内的扭曲（warp）相互转换，因此可以通过计算变换群下的不变距离来衡量轨迹间的一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于LLM的运动轨迹生成与验证的自洽性方法 |
| 英文题名 | Self-Consistency for LLM-Based Motion Trajectory Generation and Verification |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_Self-Consistency_for_LLM-Based_Motion_Trajectory_Generation_and_Verification_CVPR_2026_paper.html) · [Project](https://majiaju.io/trajectoryself-consistency) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Self-Consistent Motion Trajectory Generation/Verification via Lie Group Hierarchy |
| Dataset | 224-prompt motion trajectory benchmark, 2240-pair trajectory verification dataset |

> [!tip] 效果简介
> - 224-prompt motion trajectory benchmark (generation) 上，Accuracy 68.0 (Majority-Consensus, GPT-4.1); 83.3 (Majority-Consensus, GPT-5) vs 62.1 (LLM-Direct, GPT-4.1); 79.1 (LLM-Direct, GPT-5) (+5.9 (GPT-4.1); +4.2 (GPT-5))。
> - 224-prompt motion trajectory benchmark (generation, oracle W) 上，Accuracy 68.5 (GPT-4.1); 83.5 (GPT-5) vs 62.1 (GPT-4.1); 79.1 (GPT-5) (+6.4 (GPT-4.1); +4.4 (GPT-5))。
> - 2240-pair trajectory verification dataset 上，Precision / Recall / F1 85.8 / 66.1 / 74.7 (Majority-Consensus); F1=84.6 (Hierarchical-Consistency) vs 74.0 / 84.7 / 79.0 (VLM, GPT-5) (Precision +11.8; F1 +5.6 (Hierarchical-Consistency vs VLM GPT-5))。

## 概述

**问题瓶颈**：在运动图形轨迹生成任务中，LLM 常因自然语言提示的固有歧义而产生不符合预期的轨迹。核心困难在于，一个视觉提示对应的正确输出并非唯一，而是构成一个**形状族（shape family）**——族内轨迹可通过几何变换相互转换。因此，传统的“身份匹配”式一致性判断在此连续空间中失效。

**核心洞见**：本文提出将视觉提示映射为一个**原型轨迹**与一个**李群（Lie group）几何变换群**的组合。同一形状族内的轨迹，可通过群内指定的扭曲（warp）相互转换。基于此，可定义**变换不变距离度量**，在给定变换群下计算两条轨迹的最优对齐均方距离，从而衡量其是否属于同一族。

**方法定位**：该方法属于**无监督的自洽性（self-consistency）范式**在视觉领域的适应性扩展。与直接单次 LLM 采样（LLM-Direct）或使用 VLM 进行端到端验证的基线不同，本方法通过多样性采样、基于李群层次结构的聚类，以及自动变换群选择，构建了一个无需额外训练的生成与验证框架。

**主要结果**：
- **轨迹生成**：在 224 条提示的运动轨迹基准上，GPT-4.1 和 GPT-5 的准确率分别提升 4–6 个百分点（如 GPT-5 从 79.1% 提升至 83.3%）。
- **轨迹验证**：在 2240 对轨迹的验证数据集上，自洽性方法相比 VLM 基线（GPT-5）精度提升 11.8%，F1 分数提升 5.6%（达到 84.6）。
- **已知正确变换群（oracle）时**，验证 F1 可达 85.6，进一步验证了框架的上界性能。

## 背景与动机

### 问题背景：LLM 驱动的运动图形生成

运动图形动画广泛存在于信息可视化、用户界面和数字叙事中，其核心往往由描述物体运动路径的几何轨迹构成。近年来，大语言模型（LLM）展现出从自然语言提示直接生成运动图形代码的能力——用户只需描述期望的运动形状（如“画一个五角星”或“生成一个抛物线轨迹”），LLM 即可输出可执行的动画程序。这一范式大幅降低了运动图形创作的门槛。

然而，**自然语言提示存在固有的不确定性**：一个提示所对应的正确输出往往不是唯一的，而是构成一个“形状族”（shape family）。例如，“画一个圆”可以对应不同大小、位置、旋转角度的圆，甚至可以是经过仿射变换的椭圆——它们在不同程度上都“正确”地满足了提示。这种一对多的映射关系使得简单的身份匹配（判断两条轨迹是否完全相同）无法用于评估 LLM 输出的一致性。

### 现有方法缺口

当前 LLM 在运动轨迹生成任务上面临两个核心挑战：

1.  **生成不可靠**：LLM 单次采样（LLM-Direct）的生成结果经常偏离提示意图。如 Figure 1 所示，即使对于看似简单的几何形状，LLM 也可能输出形状扭曲、比例失调甚至完全错误的轨迹。在本文构建的 224 提示基准上，GPT-4.1 的单次生成准确率仅为 62.1%，GPT-5 为 79.1%（Table 1）。

2.  **验证困难**：判断一条给定轨迹是否匹配提示描述是一个具有挑战性的视觉验证任务。直接使用视觉语言模型（VLM）进行二分类判断存在严重的校准问题——VLM 倾向于过度判定为“匹配”，导致精确率偏低（GPT-5 VLM 验证精确率仅 74.0%，Table 2），而召回率虚高。

这两个问题的根源在于：**现有方法缺乏一个能够刻画“同一提示下多种正确输出之间等价关系”的形式化框架**。在没有监督信号的情况下，如何自动识别哪些 LLM 生成结果属于同一形状族、并从中选出最具自洽性的输出，是一个尚未被充分探索的问题。

### 本文动机与核心思路

本文的核心动机是将**自洽性（self-consistency）** 思想从离散推理领域推广到连续视觉生成领域。在语言任务中，自洽性通过多数投票从多个采样中选出最一致的答案；但在视觉轨迹生成中，由于输出是连续空间中的几何形状，无法直接套用“投票”机制。

本文的关键洞察是：**将视觉提示映射为一个原型轨迹与一个几何变换群（李群）的组合**。具体而言，定义一个形状族 $\mathcal{F}(o, W) = \{ w(o) \mid w \in W \}$，其中 $o$ 为原型轨迹，$W$ 为变换群（如刚性变换、相似变换、仿射变换等）。同一族内的轨迹可以通过群内的扭曲（warp）相互转换，因此可以通过计算变换群下的不变距离来衡量轨迹间的一致性：

$$d_W(t_1, t_2) = \min_{w \in W} \frac{1}{n} \sum_{i=1}^{n} \| w(t_{1,i}) - t_{2,i} \|^2$$

基于这一形式化，本文提出了一套完整的无监督流程：对 LLM 进行多样性采样生成多条轨迹，利用几何变换群层次结构对轨迹进行聚类，自动选择最合适的变换群，并从最大簇中选取原型作为自洽生成结果。该框架同时可自然地扩展为验证器——通过检查查询轨迹是否能加入最大簇来判断其有效性。

在生成任务上，该方法将 GPT-4.1 和 GPT-5 的准确率分别提升 4–6 个百分点；在验证任务上，相比 VLM 基线提高了 11% 的精确率和 5.6% 的 F1 分数。

## 核心创新

本工作将大语言模型的自洽性范式迁移至视觉生成领域，核心创新在于用**李群层次结构下的几何变换不变性**替代传统自洽性中的身份匹配，从而解决“正确输出不唯一”这一根本瓶颈。具体而言，创新体现在以下四个关键维度的改变：

### 1. 一致性定义的几何化：从身份匹配到变换群不变距离

传统自洽性方法（如文本生成中的多数投票）依赖输出之间的身份匹配，这在连续空间的视觉生成中失效——同一提示对应的正确轨迹可以具有不同的尺度、朝向或仿射变形。本工作提出**形状族**（shape family）概念，将提示对应的所有合法输出建模为一个原型轨迹 $o$ 与一个李变换群 $W$ 的组合：

$$\mathcal{F}(o, W) = \{ w(o) \mid w \in W \}$$

其核心洞察是：同一族内的轨迹可以通过群内的扭曲（warp）相互转换。基于此，定义**变换不变距离度量**：

$$d_W(t_1, t_2) = \min_{w \in W} \frac{1}{n} \sum_{i=1}^{n} \| w(t_{1,i}) - t_{2,i} \|^2$$

该度量在变换群 $W$ 下保持不变，通过广义 ICP 算法优化对齐后计算均方距离。两条轨迹若距离低于阈值 $\tau$，即判定为属于同一形状族。这一距离定义将“一致性”从离散的身份匹配升级为连续的几何等价关系，是方法有效性的理论根基。

### 2. 采样策略：从单次生成到多样性采样

基线方法 **LLM-Direct** 仅对 LLM 进行单次采样生成，无法利用输出分布的信息。本工作改为**多样性采样**，每次生成 $N=19$ 条轨迹，鼓励覆盖分布尾部。这一改变使得后续聚类能够捕获 LLM 输出分布中的多数模式，为自洽性选择提供统计基础。消融实验表明，当 $N$ 从 1 增加至 10 后，验证 F1 趋于稳定，10 个样本即可获得接近最优的性能。

### 3. 变换群选择：从无到自动层次决策

基线方法不存在变换群选择的概念。本工作构建了从刚性变换到仿射变换的**李群层次结构**（Figure 3），并提出两种自动选择准则：

- **多数共识**（Majority-Consensus）：选择使最大簇规模最大的变换群。
- **层次一致性**（Hierarchical-Consistency）：选择使最大簇保持完整的最严格变换群。

这两种准则利用层次结构中的包含关系，无需监督即可自动识别提示对应的最合适变换群。实验表明，在已知正确变换群（oracle）的情况下，生成准确率可进一步提升（GPT-4.1 从 +5.9 到 +6.4 个百分点），说明变换群选择的准确性仍有提升空间，但自动准则已能捕获大部分收益。

### 4. 验证方式：从 VLM 二分类到形状族成员检测

基线验证方法使用 VLM（如 GPT-4.1 / GPT-5）直接判断轨迹是否匹配提示，存在严重的校准问题——精确率仅 74.0%，召回率高达 84.7%，表现为过度宽松的倾向。本工作将验证重构为**形状族成员检测**：给定提示，先通过多样性采样和聚类找到最大簇及其原型轨迹，再检查查询轨迹与原型在选定变换群下的距离是否小于阈值 $\tau$。这一改变将验证从黑箱视觉推理转化为可解释的几何距离判断，使精确率提升 11.8 个百分点（85.8% vs 74.0%），F1 提升 5.6 个百分点（84.6 vs 79.0）。

### 创新总结

上述四个 changed slots 构成一条完整的因果链：**多样性采样**提供统计基础 → **变换不变距离**定义几何一致性 → **层次变换群选择**自动适配提示的几何约束 → **成员检测**实现可校准的验证。这一链条将 LLM 的自洽性从离散符号空间推广到连续几何空间，为视觉生成中的无监督质量提升提供了新的方法论框架。

## 整体框架

本工作提出了一套面向LLM运动轨迹生成与验证的无监督自洽性框架。其核心流程可概括为四个阶段：**多样性采样 → 变换不变聚类 → 变换群选择 → 原型选择与验证**。图1给出了该流程的全局概览。

**输入与输出。** 系统的输入为一条自然语言提示（如“绘制一个五角星形轨迹”），输出端则根据任务分为两种模式：（1）**生成模式**下，返回一条自洽性最高的运动轨迹作为最终生成结果；（2）**验证模式**下，接收一条查询轨迹，返回其是否属于提示所描述的形状族的二值判断。

**模块关系与数据流。** 各模块的串联关系如下：

1. **LLM轨迹采样器**（Section 4.1）接收提示，以多样性解码策略生成 N=19 条运动图形动画程序，执行后得到轨迹集合。采样设计鼓励覆盖分布尾部，以增加捕获正确形状族的概率。
2. **变换不变距离计算**（Section 3, Equation 2）为轨迹集合中每一对轨迹，在给定的几何变换群 W 下计算最小对齐均方距离 $d_W(t_1, t_2)$。该距离通过广义ICP算法实现，对群内扭曲保持不变。
3. **DBSCAN聚类**（Section 4.2）基于上述距离矩阵对轨迹进行聚类，识别出具有自洽性的轨迹簇。聚类阈值 τ 控制簇的紧致程度。
4. **变换群选择模块**（Section 4.3）利用变换群的层次结构（Figure 3），通过两种决策准则——多数共识（Majority-Consensus）或层次一致性（Hierarchical-Consistency）——自动选择最合适的变换群 W*。
5. **原型选择**（Section 4.2）在选定变换群下的最大簇中，选取中心样本作为该形状族的原型轨迹 o。
6. **验证器**（Section 4.4）通过检查查询轨迹 t 与原型 o 在选定变换群 W* 下的距离 $d_{W^*}(t, o)$ 是否小于阈值 τ，判断 t 是否为有效输出。

**关键设计决策。** 框架的核心洞察在于将视觉提示映射为一个原型轨迹与一个几何变换群（李群）的组合——即同一形状族内的轨迹可通过群内扭曲相互转换。这一形式化使得“一致性”不再依赖脆弱的身份匹配，而是通过变换不变距离来度量。变换群层次结构（刚性 → 相似性 → 仿射 → 投影）为系统提供了从严格到宽松的多粒度一致性判断能力，而自动群选择机制则使整个流程在无监督设定下保持端到端的可用性。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/001_Figure_1.jpg]]
*Figure 1: Complex motion graphics animations are often composed of trajectories in the form of geometric shapes (left). While LLMs can generate motion graphics animations from a prompt describing the shape of an object’s trajectory, the resulting animation does not always follow the prompt specification (right, motions move from blue to red). We present a self-consistency method that enables more accurate LLM-based trajectory generation without supervision and show that it can be used for trajectory verification. We ask the LLM to generate multiple trajectory samples, cluster the samples using a hierarchy of geometric transformation groups, and choose the largest cluster as the most self-consistent s...*

## 核心模块与公式推导

### 问题形式化：形状族与变换不变距离

本方法的核心建模是将视觉提示所对应的正确输出集合形式化为一个**形状族（Shape Family）**。给定一个原型轨迹 $o$ 和一个李群变换群 $W$，形状族定义为该原型在群内所有扭曲作用下的像的集合：

$${\mathcal{F}}(o, W) = \{ w(o) \mid w \in W \}$$

**公式含义**：若两条轨迹可通过群 $W$ 内的某个几何变换相互转换，则它们属于同一形状族，在语义上被视为“一致”。这一定义直接回应了核心瓶颈：自然语言提示的模糊性导致正确答案不唯一，无法通过身份匹配判断一致性。

基于此，方法定义了**变换不变距离度量** $d_W(t_1, t_2)$，用于衡量两条轨迹在群 $W$ 下的最小对齐均方距离：

$$d_W(t_1, t_2) = \min_{w \in W} \frac{1}{n} \sum_{i=1}^{n} \| w(t_{1,i}) - t_{2,i} \|^2$$

**公式含义**：通过优化求解群 $W$ 内的最优扭曲 $w$，将轨迹 $t_1$ 对齐到 $t_2$，计算逐点均方误差。若 $d_W(t_1, t_2) < \tau$（预设阈值），则判定两条轨迹在群 $W$ 下一致。该距离通过广义迭代最近点（ICP）算法实现，轨迹在 $400\text{px} \times 400\text{px}$ 的 SVG 画布上表示为 $n=100$ 个弧长重采样点，单对计算平均耗时 67 毫秒。

### 变换群层次结构

方法构建了一个李群变换层次结构，按约束强度从严格到宽松排列，每个节点对应一个变换群及其诱导的形状族。层次结构中的关键群包括：**刚性变换**（旋转+平移）、**相似变换**（刚性+均匀缩放）、**仿射变换**（线性变形+平移）等。约束越严格的群，对形状一致性的判定越保守；约束越宽松的群，越能容忍几何形变。

这一层次结构是方法的核心因果调节旋钮：不同提示对应的正确形状族可能处于层次结构的不同层级，方法通过自动选择最合适的变换群来匹配提示的几何语义。

### 核心流程模块

**模块1：LLM轨迹采样器**。给定自然语言提示，调用 LLM 生成 $N=19$ 个运动图形动画程序，执行后获得轨迹集合。采样采用多样性策略，鼓励覆盖分布尾部，以增加捕获正确形状族的概率。

**模块2：变换不变距离计算**。对轨迹集合中的每一对，在层次结构中各变换群下分别计算 $d_W$，生成距离矩阵。

**模块3：DBSCAN 聚类**。基于各变换群下的距离矩阵，对轨迹进行聚类。每个群 $W$ 下的聚类结果反映了在该几何约束下轨迹之间的一致性结构。

**模块4：变换群选择**。这是连接几何建模与决策的关键模块。方法提出两种自动选择准则：
- **Majority-Consensus**：选择使最大簇包含轨迹数最多的变换群，倾向于选择约束较宽松的群。
- **Hierarchical-Consistency**：从最严格的群开始沿层次结构向下搜索，选择最大簇保持完整的**最严格**变换群，倾向于选择约束较严格的群。

**模块5：原型选择**。在选定变换群的最大簇中，选取中心样本作为该形状族的原型轨迹。

**模块6：验证器**。给定查询轨迹 $t$，计算其与原型在选定变换群下的距离 $d_W$，若低于阈值 $\tau$ 则判定为有效输出，即 $t \in \mathcal{F}(o, W)$。这本质上是一个形状族成员检测器，将 VLM 直接二分类替换为基于几何一致性的判定，解决了 VLM 的校准问题。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/002_Figure_2.jpg]]
*Figure 2: We define a shape family*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/003_Figure_3.jpg]]
*Figure 3: Hierarchy of Lie transformation groups and shape families they induce. Each node represents a transformation group and depicts a prototype square-shaped trajectory o as well as other trajectories w(o) within the corresponding shape family*

## 实验与分析

### 轨迹生成实验

我们在包含 224 个提示的轨迹生成基准上评估方法。基线为 **LLM-Direct**，即对每个提示仅采样一次并直接输出生成轨迹。我们的方法对每个提示采样 N=19 条轨迹，通过聚类与群选择模块确定最自洽的簇，并从中选取原型作为最终输出。

**主要结果**（Table 1）：在 Majority-Consensus 决策准则下，GPT-4.1 的准确率从基线的 62.1% 提升至 68.0%（+5.9 个百分点），GPT-5 从 79.1% 提升至 83.3%（+4.2 个百分点）。Hierarchical-Consistency 准则在 GPT-4.1 上达到 68.0%，在 GPT-5 上达到 82.7%，均显著优于单次采样基线。

在 oracle 设定下（使用真实变换群 W 计算自洽性），GPT-4.1 的准确率进一步提升至 68.5%（+6.4 个百分点），GPT-5 提升至 83.5%（+4.4 个百分点）。这表明自动群选择模块仍有改进空间，但已逼近 oracle 上界。

### 轨迹验证实验

在 2240 对轨迹的验证数据集上，我们将自洽性方法作为验证器：对给定提示采样 N=19 条轨迹，构建形状族原型，然后检查查询轨迹与原型在选定变换群 W 下的距离是否小于阈值 τ。

**主要结果**（Table 2）：与 VLM 直接二分类基线相比，我们的方法在精确率上有显著提升。以 GPT-5 为骨干的 VLM 基线精确率为 74.0%，召回率为 84.7%，F1 为 79.0%。Majority-Consensus 准则下，精确率达到 85.8%（+11.8 个百分点），召回率为 66.1%，F1 为 74.7%。Hierarchical-Consistency 准则实现了更均衡的精确率（83.3%）和召回率（86.0%），F1 达到 84.6（+5.6 个百分点），优于 VLM 基线。在 oracle W 设定下，F1 达到 85.6（+6.6 个百分点）。

VLM 基线的高召回率、低精确率模式表明，VLM 倾向于将大量轨迹判定为匹配，存在校准偏差；而自洽性方法通过几何约束有效抑制了误判。

### 消融实验

**采样数量 N 的影响**（Figure 5）：当 N 从 1 增加到 30 时，验证 F1 在 N=10 后趋于稳定。10 个样本通常足以获得接近最优的性能，说明方法对采样数量的需求较为温和。

**聚类阈值 τ 的敏感性**：在 0.25 到 8.0 的 32 倍范围内变化 τ 时，F1 仅下降 7.2 个百分点。方法对 τ 不敏感，降低了调参负担。

**决策准则的错误模式分析**：Majority-Consensus 在选错 W 时有 95.6% 的概率选择了过于严格的群（即低估了形状族的容许变形范围），导致簇过于碎片化；而 Hierarchical-Consistency 有 80.6% 的概率选择了过于宽松的群（高估了容许变形），可能将不匹配的轨迹纳入簇中。两种准则的错误偏向互补，解释了 Hierarchical-Consistency 在验证任务上召回率更高的原因。

### 定性结果与失败模式

**聚类定性分析**（Figure 4）：在五边形提示下，失败样本（簇 2-4）在视觉上与正确轨迹明显不同；而在三角形提示下，部分失败样本仍保持三角形形态，仅在几何细节上有偏差。最右侧的抛物线案例中，一条倾斜抛物线在仿射变换群下会被归入最大簇，说明在过于宽松的变换群下，方法可能接纳语义上不匹配的轨迹。

**方法局限**：当 LLM 生成的轨迹分布不满足假设（例如无法形成多数簇）时，方法可能失效。此外，当前框架假设每个提示对应的形状族可由单个原型和单个几何变换群描述，不支持同时包含多个不相交形状族的提示（如七角星存在 {7/2} 和 {7/3} 两种无法相互变换的形态）。论文指出，这一问题可通过简单的多簇扩展缓解，但未在实验中验证。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/004_Figure_4.jpg]]
*Figure 4: We present clustering results on LLM-generated samples from three example prompts in our dataset. Each trajectory has a ground truth label on the upper right. Clusters colored green are the chosen largest clusters, and we note that their sizes vary, sometimes less than half of the total number of trajectories (middle). In the pentagon case, failed samples (Cluster 2–4) appear visually distinct from the true ones, while some of the failed deltoids (Cluster 4–8) look closer to the correct one with their triangular forms. The rightmost parabola is a skewed one that would have been grouped into the largest cluster under the affine warp*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/005_Table_2.jpg]]
*Table 2: Motion trajectory verification experiment (see Sec. 5.3). We compare our self-consistency-based approach for verifying whether a trajectory matches an input prompt against the alternative of using a VLM (GPT-4.1 or GPT-5)*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/006_Table_1.jpg]]
*Table 1: Motion trajectory generation experiment (see Sec. 5.2). We evaluate the accuracy of LLM-generated motion trajectories (GPT-4.1 and GPT-5) under different decoding strategies. Under different decision criteria for selecting a transformation group W , our self-consistency approach improves upon the baseline alternative of directly generating a single sample (LLM-Direct)*

![[assets/figures/papers/paper_list_l27_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Self_Consistency_fo/figures/007_Figure_5.jpg]]
*Figure 5: F1 scores across different numbers of sampled trajectories N . Decision criteria performances stabilize after N = 10*

## 方法谱系与知识库定位

### 1. 方法脉络与基线关系

本工作处于 **LLM 视觉生成可靠性** 与 **几何不变性无监督评估** 的交叉点。其直接对比的两类基线如下：

| 基线类型 | 代表方法 | 核心机制 | 根本局限 |
|----------|----------|----------|----------|
| 直接生成 | **LLM-Direct** | 单次采样，取 argmax 或单次随机解码 | 无法处理自然语言提示固有的欠定性与形状族歧义 |
| VLM 验证 | **VLM-based Verification** (GPT-4.1 / GPT-5) | 将轨迹渲染为图像，由 VLM 判断是否匹配提示 | 存在严重校准问题：高召回（84.7）但低精度（74.0），倾向过度接受 |

本方法的关键突破在于：**将“一致性”从身份匹配重新定义为几何变换群下的不变性**。这使方法能够无监督地识别同一形状族内的不同实现，从而绕过了 VLM 对视觉细节的校准困难。实验证据表明，在验证任务上，自洽性方法将精度从 74.0 提升至 85.8（+11.8 个百分点），F1 从 79.0 提升至 84.6（+5.6 个百分点）。

### 2. 与上游自洽性工作的继承与差异

本方法继承了 LLM 推理中 **Self-Consistency**（Wang et al., ICLR 2023）的核心思想——通过多次采样并选择最一致的答案来提高可靠性。但将其迁移到视觉连续空间时，面临根本性瓶颈：

- **文本域**：答案离散，一致性可通过精确字符串匹配或语义等价判断。
- **视觉轨迹域**：正确输出构成连续形状族，无法通过身份匹配判断一致性。

本工作的核心贡献在于解决了这一迁移瓶颈：通过引入李群层次结构与变换不变距离度量，为连续视觉输出定义了一种可计算的一致性概念。

### 3. 与几何对齐与聚类方法的关系

在实现层面，本方法的技术组件与以下领域存在连接：

- **广义 ICP（Iterative Closest Point）**：用于计算变换群下的最小对齐距离。论文报告每对轨迹的计算平均耗时 67 毫秒（标准桌面 CPU），表明该方法在实际应用中具有可接受的计算开销。
- **DBSCAN 聚类**：基于距离矩阵对轨迹进行聚类。论文未对聚类算法本身进行消融，其选择理由（对噪声鲁棒、无需预设簇数）与形状族问题的特性一致，但该点需要手动验证是否有更优替代方案。
- **李群层次结构**：从刚性变换（SE(2)）到相似变换（Sim(2)）再到仿射变换（Aff(2)），构成由严格到宽松的变换群谱系。这一设计使方法能够根据提示的几何约束强度自动选择合适的变换群。

### 4. 适用边界与失效模式

**方法假设**（来自论文明确陈述）：

1. **单原型-单变换群假设**：提示对应的形状族可由单个原型轨迹与单个几何变换群描述。
2. **多数簇假设**：LLM 生成的正确样本在采样分布中形成多数簇（或至少是可识别的大簇）。
3. **几何可变形性**：同一形状族内的轨迹可通过李群内的扭曲相互转换。

**已知失效模式**：

- **多不相交形状族提示**：如“七角星”存在 {7/2} 和 {7/3} 两种无法通过几何变换相互转换的形态。论文指出可通过简单的多簇扩展缓解，但未在实验中验证。
- **LLM 采样分布偏离假设**：当 LLM 生成的轨迹分布无法形成多数簇时（例如所有样本均错误且彼此不一致），方法将选择错误的簇作为输出。
- **复杂视觉语义缺失**：当前变换群仅覆盖几何形状，无法处理时序属性（如速度、加速度曲线）或精确数学曲线边界（如特定参数的贝塞尔曲线）。

**决策准则的偏差特性**（来自消融实验）：

- **Majority-Consensus**：选错变换群时，有 95.6% 概率选择过于严格的群（导致欠聚类，可能遗漏正确输出）。
- **Hierarchical-Consistency**：选错变换群时，有 80.6% 概率选择过于宽松的群（导致过聚类，可能引入错误输出）。

这一差异揭示了两类决策准则的内在权衡：Majority-Consensus 偏向精度，Hierarchical-Consistency 偏向召回。

### 5. 超参数鲁棒性边界

- **采样数 N**：F1 在 N=10 后趋于稳定，表明 10–19 个样本足以获得接近最优的性能。论文默认使用 N=19。
- **聚类阈值 τ**：在 0.25 到 8.0 的 32 倍范围内变化时，F1 仅下降 7.2 个百分点，表明方法对 τ 不敏感。这一鲁棒性源于变换不变距离度量的设计：正确匹配与错误匹配之间的距离差距足够大。

### 6. 开放问题与可扩展性

论文明确提出的开放方向：

1. **跨领域推广**：将该自洽性框架推广到其他空间与形状相关的视觉领域，如 3D 场景生成、通用视觉生成任务。核心挑战在于为不同领域定义合适的变换群层次结构。
2. **多原型自动发现**：为多原型、多变换群的复杂提示自动发现层次化形状族。当前方法需要人工设计变换群层次结构。
3. **视觉语义增强**：在自洽性流程中引入更丰富的视觉表示，以支持除了几何形状之外的运动属性（如速度、加速度、时序约束）。

此外，以下问题虽未被论文明确列出，但可从方法局限中自然推导：

- 能否将变换群从参数化李群扩展到更灵活的非参数变形模型（如薄板样条），以覆盖更广泛的形状族？
- 在 LLM 采样分布严重偏离时，能否引入主动采样策略（如基于当前聚类结果引导后续采样）来提高多数簇的形成概率？

## 原文 PDF

![[paperPDFs/CVPR_2026/Self_Consistency_for_LLM_Based_Motion_Trajectory_Generation_and_Verification.pdf]]

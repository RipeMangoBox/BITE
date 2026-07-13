---
title: "Articulation in Motion: Prior-free Part Mobility Analysis for Articulated Objects by Dynamic-Static Disentanglement"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated_Objects.pdf
project_link: https://haoai-1997.github.io/AiM/
code_link: https://github.com/zrporz/AutoSeg-SAM2
aliases:
- AMA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入连续运动视频替代静态两状态输入；设计双高斯表示（静态高斯集+可变形高斯集）实现动态-静态解耦，并通过静态运动检测（SDMD）处理新出现的静态区域；采用无先验的顺序RANSAC从运动轨迹聚类刚体部件并自动估计关节参数，从而摆脱了对部件数量和几何对应的依赖。
primary_logic: 通过捕捉铰接物体的连续运动视频，利用运动先验自动分离静态基座与动态部件，并基于多时间窗口的刚体轨迹一致性实现无需先验知识的部件分割与关节参数恢复。
claims:
- 在复杂多部件物体Storage(6 moving parts)上，AIM的动态部件平均3D IoU达到69.01%，远超最佳基线ArtGS（65.30%）和DTA（39.01%），显示出对未知部件数量的鲁棒性。
- 在Storage 47648（复杂物体）上，AIM将平均关节轴角度误差从ArtGS的10.18°大幅降低至0.08°，误差减少99%以上。
- 消融实验证实双高斯表示和SDMD模块的关键作用：移除双高斯后Storage 47648动态部分Chamfer距离从8.36增至17.43；移除SDMD后CD-m剧增至91.52。
- Oven (two-part object) 上 3D IoU Dynamic Part (%) = 89.61±1.50
---

# Articulation in Motion: Prior-free Part Mobility Analysis for Articulated Objects by Dynamic-Static Disentanglement

> [!tip] 核心洞察
> 通过捕捉铰接物体的连续运动视频，利用运动先验自动分离静态基座与动态部件，并基于多时间窗口的刚体轨迹一致性实现无需先验知识的部件分割与关节参数恢复。

| 字段 | 内容 |
|------|------|
| 中文题名 | 运动中的铰接：基于动态-静态解耦的无先验部件移动性分析 |
| 英文题名 | Articulation in Motion: Prior-free Part Mobility Analysis for Articulated Objects by Dynamic-Static Disentanglement |
| 会议/期刊 | ICLR 2026 |
| Links | [Project](https://haoai-1997.github.io/AiM/) · [paper](https://arxiv.org/abs/2308.13561) · [Code](https://github.com/zrporz/AutoSeg-SAM2) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Articulation in Motion (AIM) |
| Dataset | Oven, Storage 47648, Table 31249 |

> [!tip] 效果简介
> - Oven (two-part object) 上，3D IoU Dynamic Part (%) 89.61±1.50 vs ArtGS 65.68±24.50 (+23.93 pp)。
> - Storage 47648 (complex, 6 moving parts) 上，Average joint axis angular error (°) 0.08 vs ArtGS 10.18 (-10.10 °)。
> - Table 31249 (complex, multiple parts) 上，Average joint axis angular error (°) 1.19 vs ArtGS 33.19 (-32.00 °)。

## 概要

铰接物体的部件移动性分析是机器人操控、数字孪生和具身智能的关键基础能力。现有方法普遍依赖两个离散状态（如关闭与打开）的RGB-D图像，通过跨状态几何对应来分割部件并估计关节参数。然而，当最终状态暴露出初始状态不可见的区域时（如打开冰箱门后露出的内部空间），几何对应关系会失效，导致分割与关节估计严重退化。此外，这些方法通常需要预先指定部件数量，并对初始化和超参数敏感，难以推广到未知部件数量的真实场景。

针对上述瓶颈，本文提出**Articulation in Motion (AIM)**，一种无先验的铰接物体移动性分析框架。其核心洞察在于：通过捕捉铰接物体从关闭到打开的连续运动视频，利用运动先验自动分离静态基座与动态部件，并基于多时间窗口的刚体轨迹一致性实现无需预知部件数量的分割与关节参数恢复。

AIM包含三个递进阶段：首先利用3D高斯泼溅（3DGS）从多视图扫描重建初始状态几何与外观；其次引入**双高斯表示**——将场景显式解耦为静态高斯集与可变形高斯集，通过联合优化逐步将运动部件从静态集中剪枝，并借助**静态运动检测（SDMD）**模块将交互过程中新出现的静态区域归还给静态集，实现干净的动态-静态分离；最后，对运动高斯的时间轨迹应用**顺序RANSAC**，自动聚类刚体部件并直接解析关节参数（轴方向、位置、运动类型与角度），无需任何部件数量先验或优化迭代。

实验结果表明，AIM在复杂多部件物体上展现出显著优势：在Storage（6个运动部件）上，动态部件平均3D IoU达到69.01%，远超最佳基线ArtGS（65.30%）和DTA（39.01%）；在Storage 47648上，平均关节轴角度误差从ArtGS的10.18°大幅降至0.08°，误差减少99%以上。消融实验进一步验证了双高斯表示和SDMD模块的关键作用——移除双高斯后动态部件Chamfer距离从8.36增至17.43，禁用SDMD后更急剧恶化至91.52。

AIM的方法定位清晰：它首次将连续运动视频引入铰接物体分析，通过动态-静态解耦与无先验刚体聚类，从根本上绕开了两状态方法对部件数量假设和跨状态几何对应的依赖，为无先验部件移动性分析开辟了新路径。



铰接物体的感知与理解是具身智能和机器人交互的核心能力之一。要让机器人自主操作日常物体（如打开冰箱、拉出抽屉），系统必须能够从视觉输入中恢复物体的部件级几何结构、运动分割以及关节参数。这一任务面临双重挑战：既要精确重建物体在不同状态下的三维几何，又要从运动中推断各部件的刚体变换关系。

### 两状态范式的根本局限

近年来，基于神经辐射场（NeRF）和三维高斯泼溅（3DGS）的方法在该领域取得了显著进展。然而，现有方法几乎都遵循一个共同范式：**从两个离散状态（如关闭和打开）的RGB/RGB-D图像中推断铰接结构**。代表性工作包括 **PARIS**（Liu et al., CVPR 2023）、**DTA**（Weng et al., 2024）和 **ArtGS**（Liu et al., 2025）。

这一范式存在两个根本性瓶颈：

**第一，部件数量先验依赖。** 现有方法要求用户预先指定运动部件的数量，并基于此进行部件分割和关节参数优化。当部件数量估计错误时，分割结果会出现严重的过度分割或欠分割（Figure 2）。例如，DTA和ArtGS在给定错误部件数（4个）时，无法恢复正确的部件划分，导致分割结果与真实几何严重偏离。

**第二，跨状态几何对应的脆弱性。** 两状态方法隐式或显式地依赖关闭状态与打开状态之间的几何对应关系来推断运动。然而，当最终状态暴露出初始状态不可见的区域时——例如，打开冰箱门后露出的内部空间——这种对应关系会系统性失效。此时，分割与关节估计的性能急剧退化，因为模型无法为“新出现”的几何区域建立有意义的跨状态映射（Figure 1左）。

此外，基于优化的方法对初始化和超参数高度敏感，在未知部件数量的场景中难以稳定推广。

### 从“两状态快照”到“连续运动流”

本文的核心洞察在于：**铰接物体的运动过程本身蕴含了丰富的结构信息，而不仅仅是两个端点的状态差异。** 通过捕捉物体从关闭到打开的连续运动视频，我们可以利用运动先验自动分离静态基座与动态部件，并基于多时间窗口的刚体轨迹一致性实现无需先验知识的部件分割与关节参数恢复。

这一思路将问题的焦点从“跨状态几何匹配”转移到“动态-静态解耦与运动轨迹分析”，从而从根本上摆脱了对部件数量先验和几何对应的依赖。



## 核心方法与创新机理

AIM 的核心创新在于**将铰接物体分析从“两状态几何对应”范式转变为“连续运动解耦”范式**，从根本上绕开了现有方法对部件数量先验和跨状态几何对应的依赖。

### 1. 输入模态的根本性转变

现有方法（如 **PARIS** (Liu et al., CVPR 2023)、**DTA** (Weng et al., 2024)、**ArtGS** (Liu et al., 2025)）依赖两个离散状态（开始与结束）的 RGB/RGB-D 图像，通过跨状态几何对应来分割部件并估计关节参数。然而，当结束状态暴露出初始状态不可见区域时（如冰箱门打开后露出的内部隔层），对应关系会失败，导致分割严重退化（Figure 1, Figure 2）。

AIM 将输入替换为**初始状态的 3D 扫描 + 连续运动视频（单目 RGB）**。这一转变的深层逻辑是：连续运动提供了天然的“运动先验”——静态部件在视频中保持静止，而动态部件产生可追踪的轨迹。这使方法不再需要跨状态几何对应，也无需预知部件数量。

### 2. 双高斯表示与动态-静态解耦

这是 AIM 最核心的技术创新。现有基于 3DGS 的方法（如 ArtGS）在所有高斯上定义统一的变形场，无法显式分离静态基座与运动部件，导致静态区域被错误关联到运动高斯集，产生“静态泄漏”（Figure 4）。

AIM 设计了**双高斯表示**（Figure 3）：
- **静态高斯集** $\mathcal{G}^S$：从初始状态 3D 扫描重建，在联合优化过程中逐步剪枝——被识别为运动的高斯被移除，最终保留纯静态基座。
- **可变形高斯集** $\mathcal{G}^{M,t}$：通过变形网络预测每个高斯的位移与旋转偏移，跟踪运动部件的轨迹。

$$
(\delta \mu_j, \delta r_j) = \mathcal{F}_{\boldsymbol{\theta}}( \gamma( \mathrm{sg}(\mu_j) ), \gamma(t) )
$$

这一解耦机制的关键在于**静态运动检测模块（SDMD）**：当运动过程中暴露出新的静态区域（如抽屉内部的侧壁），SDMD 通过顺序 RANSAC 检测运动幅度低于阈值（旋转角 ≤ 0.1 rad，平移 ≤ 0.05 单位）的高斯组，将其从可变形集归还到静态集。消融实验证实，移除 SDMD 后动态部件 Chamfer 距离从 8.36 剧增至 91.52（Table 4）。

### 3. 无先验的顺序 RANSAC 部件分割与关节估计

现有方法需要已知部件数量，通过优化预测部件分割后估计关节参数，对初始化敏感且无法推广到未知部件数量的场景（Figure 2 展示了输入错误部件数量时的过度分割）。

AIM 的**顺序 RANSAC**（Figure 5）直接利用解耦后运动高斯的轨迹进行聚类：
1. 在多时间窗口上通过 Kabsch 算法求解最优刚体变换，计算逐高斯的对齐残差；
2. 迭代提取满足刚体一致性的最大内点集，自动确定部件数量；
3. 从每个部件的刚体变换矩阵中，通过 Rodrigues 公式直接解析关节轴方向、旋转角度、平移量和轴位置，无需优化。

在 Storage 47648（6 个运动部件）上，AIM 将平均关节轴角度误差从 ArtGS 的 10.18° 降至 **0.08°**，误差减少 99% 以上（Table 3(c)）。用 DB-SCAN 或 K-means 替换顺序 RANSAC 则无法产生有效分割（Section 4.3）。

### 创新总结

| 关键维度 | 现有方法 | AIM |
|---------|---------|-----|
| 输入 | 两状态 RGB/RGB-D 图像 | 初始 3D 扫描 + 连续运动视频 |
| 静态-动态分离 | 统一变形场，无显式分离 | 双高斯表示 + SDMD 模块 |
| 部件分割 | 需已知部件数量，优化驱动 | 顺序 RANSAC 自动聚类，无先验 |
| 关节估计 | 依赖分割结果，间接估计 | 从刚体变换直接解析 |

这三个 changed slots 形成了一条因果链：连续运动视频使动态-静态解耦成为可能，解耦后的纯净运动轨迹又使无先验的部件分割与关节估计变得可行。



AIM 的核心洞察在于：铰接物体的连续运动视频天然携带了动态部件与静态基座的分离线索。与依赖两离散状态（如闭合与打开）并需要跨状态几何对应的先前方法不同，AIM 通过捕捉从闭合到完全打开的完整交互过程，将部件分割与关节估计问题转化为对运动轨迹的刚体一致性分析。

该方法由三个紧密衔接的阶段构成，形成一条从几何重建到运动解耦再到关节解析的完整流水线：

**阶段 I：初始状态 3DGS 重建。** 在物体静止的闭合状态下，通过多视角 RGB 扫描（约 100 张图像）训练一个 3D Gaussian Splatting（3DGS）模型，获得静态高斯集 $\mathcal{G}^S$，为后续动态-静态分离提供精确的初始几何与外观参考。

**阶段 II：双高斯联合优化与动态-静态解耦。** 这是整个框架的核心。系统同时维护两个高斯集合：从阶段 I 继承的**静态高斯集** $\mathcal{G}^S$，以及一个**可变形高斯集** $\mathcal{G}^{M,t}$，后者通过变形网络 $\mathcal{F}_{\boldsymbol{\theta}}$ 预测每个高斯在时刻 $t$ 的位置偏移 $\delta\mu$ 和旋转偏移 $\delta r$，以跟踪运动部件。联合优化过程中，静态集中被识别为运动的高斯被逐步剪枝，从而实现动态与静态的初步分离。

为解决闭合状态被遮挡、运动过程中才暴露的静态区域（如冰箱内部），AIM 引入了**静态运动检测模块（SDMD）**。该模块在连续时间窗口内对可变形高斯集的运动轨迹执行顺序 RANSAC，利用 Kabsch 算法估计局部刚体变换；运动幅度低于预设阈值（旋转角 $\Theta \le 0.1$ 弧度，平移量 $\Phi \le 0.05$ 单位）的高斯组被判定为静态，并重新归入静态集 $\mathcal{G}_p^S$。这一机制有效防止了“静态泄漏”——即新出现的静态区域被错误关联到运动部件。

阶段 II 的输出是两个清晰分离的高斯集合：表示静态基座的 $\mathcal{G}_p^S$，以及携带完整运动轨迹的可变形高斯集 $\mathcal{G}^{M,t}$。

**阶段 III：基于运动的部件分割与关节分析。** 阶段 II 提供的干净运动轨迹 $\mathcal{G}^{M,t}$ 使得无需任何先验知识即可进行部件聚类与关节估计。系统采用**顺序 RANSAC**：在多个时间窗口内，对高斯轨迹反复执行 Kabsch 刚体对齐，将满足刚体一致性约束的高斯聚类为一个部件；已聚类的高斯被移除后，算法继续在剩余轨迹上迭代，自动发现下一个刚体部件，直至所有运动高斯被分配完毕——部件数量完全由数据驱动确定。

对每个聚类得到的部件，从其刚体变换矩阵中通过 Rodrigues 公式解析提取关节轴方向 $\mathbf{u}_k$、旋转角 $\Theta_k$ 和平移量 $\Phi_k$，并根据旋转角是否超过 $10^\circ$ 阈值自动分类为旋转关节或平移关节，无需任何优化步骤。

整个流水线的设计使得 AIM 从根本上摆脱了对部件数量预设和跨状态几何对应的依赖，从而在处理具有未知数量运动部件的复杂铰接物体时展现出显著优势。

### 补充图表

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the first two stages: I) 3DGS start-state*



AIM 的核心技术路线围绕三个关键模块展开：**双高斯动态-静态解耦表示**、**运动中静态检测（SDMD）** 以及**基于顺序RANSAC的无先验刚体分割与关节解析**。以下逐一阐述其机理与核心公式。

### 双高斯动态-静态解耦表示

传统基于两状态的方法对所有高斯/点统一建模变形，无法显式分离静态基座与运动部件，导致当最终状态暴露出初始状态不可见区域时，几何对应关系崩溃。AIM 引入双高斯集合联合优化，从根本上解决这一问题：

- **静态高斯集** $\mathcal{G}^S$：由初始状态多视图扫描重建的 3DGS 初始化，编码物体的静态基座。
- **可变形高斯集** $\mathcal{G}^M$：以 $\mathcal{G}^S$ 为初始化，通过变形网络 $\mathcal{F}_{\boldsymbol{\theta}}$ 预测每个高斯在时间 $t$ 的位置偏移 $\delta\mu_j$ 与旋转偏移 $\delta r_j$，从而跟踪运动部件。

变形网络的数学形式为：

$$(\delta\mu_j, \delta r_j) = \mathcal{F}_{\boldsymbol{\theta}}\big(\gamma(\text{sg}(\mu_j)), \gamma(t)\big) \quad \text{(Eq. 1)}$$

其中 $\mu_j$ 为高斯 $j$ 的初始位置（通过 stop-gradient $\text{sg}(\cdot)$ 阻断梯度回传至初始几何），$\gamma(\cdot)$ 为位置编码，$t$ 为归一化时间戳。该网络仅作用于 $\mathcal{G}^M$，而 $\mathcal{G}^S$ 保持固定。

联合优化过程中，$\mathcal{G}^S$ 中与运动部件对应的区域被逐步剪枝，形成剪枝后的静态集 $\mathcal{G}_p^S$。这一“从静态中剥离运动”的机制，使得动态-静态边界随视频帧的推进而自然浮现，无需人工指定部件数量。

### 运动中静态检测（SDMD）

当铰接物体从关闭状态运动至打开状态时，原本被遮挡的**静态内部区域**（如冰箱内壁、烤箱内腔）首次暴露。若不加处理，这些区域会被可变形高斯错误地关联为运动部件。SDMD 模块专门解决这一问题。

其核心思想是：对 $\mathcal{G}^M$ 中高斯的时间轨迹进行局部刚体一致性检测。具体而言，从 $\mathcal{G}^M$ 的轨迹序列中采样两个时间窗口，利用 **Kabsch 算法**求解最优刚体变换：

$$(\mathbf{R}_{ab}^*, \mathbf{t}_{ab}^*) = \arg\min_{\mathbf{R},\mathbf{t}} \sum_{i \in S_{\min}} \| \mu_{i,b}^M - (\mathbf{R} \mu_{i,a}^M + \mathbf{t}) \|^2 \quad \text{(Eq. 2)}$$

其中 $\mu_{i,a}^M$ 和 $\mu_{i,b}^M$ 分别为高斯 $i$ 在时间 $a$ 和 $b$ 的位置。随后计算每个高斯的对齐残差：

$$\mathrm{err}_i = \| \mu_{i,b}^M - (\mathbf{R}_{ab}^* \mu_{i,a}^M + \mathbf{t}_{ab}^*) \| \quad \text{(Eq. 3)}$$

为增强鲁棒性，AIM 结合两个时间窗口（$0 \to 0.5$ 和 $0 \to 1$）的平均残差进行内点判定：

$$\mathrm{err}_i = \frac{1}{2} \| \mu_{i,0.5}^M - (\mathbf{R}_{0\to0.5}^* \mu_{i,0}^M + \mathbf{t}_{0\to0.5}^*) \| + \frac{1}{2} \| \mu_{i,1}^M - (\mathbf{R}_{0\to1}^* \mu_{i,0}^M + \mathbf{t}_{0\to1}^*) \| \quad \text{(Eq. 4)}$$

通过顺序 RANSAC 提取局部刚体运动模式，将运动幅度低于预设阈值（旋转角 $\Theta \leq 0.1$ 弧度且平移量 $\Phi \leq 0.05$ 单位）的高斯组识别为静态，并将其从 $\mathcal{G}^M$ 归还至 $\mathcal{G}_p^S$。消融实验证实，移除 SDMD 后 Storage 47648 的动态部件 Chamfer 距离从 8.36 急剧增至 91.52，验证了该模块对处理新出现静态区域的关键作用。

### 顺序RANSAC与关节参数解析

在获得干净的动态高斯轨迹 $\mathcal{G}^M$ 后，AIM 采用**顺序 RANSAC** 实现无先验的刚体部件聚类与关节参数估计。与需要预知部件数量的优化方法（如 DTA、ArtGS）不同，顺序 RANSAC 自动确定部件数量：每次 RANSAC 迭代从剩余未分配高斯中提取最大的刚体一致集作为新部件，直至剩余高斯数量低于阈值。

对每个聚类后的部件 $k$，其刚体变换矩阵 $\mathbf{R}_k$ 通过 **Rodrigues 旋转公式**分解为关节轴方向 $\mathbf{u}_k$ 和旋转角 $\Theta_k$：

$$\mathbf{R}_k = \cos \Theta_k \mathbf{I} + \sin \Theta_k [\mathbf{u}_k]_\times + (1 - \cos \Theta_k)(\mathbf{u}_k \otimes \mathbf{u}_k) \quad \text{(Eq. 5)}$$

反向提取轴方向与角度：

$$\mathbf{u}_k = \frac{1}{2 \sin \Theta_k} \begin{pmatrix} \mathbf{R}_k[2,1] - \mathbf{R}_k[1,2] \\ \mathbf{R}_k[0,2] - \mathbf{R}_k[2,0] \\ \mathbf{R}_k[1,0] - \mathbf{R}_k[0,1] \end{pmatrix}, \quad \Theta_k = \operatorname{arccos}\left( \frac{\operatorname{tr}(\mathbf{R}_k) - 1}{2} \right) \quad \text{(Eq. 6)}$$

平移距离与关节轴位置由下式给出：

$$\Phi_k = \left| \frac{\mathbf{u}_k \cdot \mathbf{t}_k}{\|\mathbf{u}_k\|^2} \right|, \quad \mathbf{p}_k = (\mathbf{R}_k - \mathbf{I})^{-1} \cdot (\boldsymbol{\Phi}_k \cdot \mathbf{u}_k - \mathbf{t}_k) \quad \text{(Eq. 7)}$$

关节类型通过旋转角阈值判定：当 $\Theta_k > 10^\circ$（约 0.17 弧度）时归类为旋转关节（revolute），否则为平移关节（prismatic）。

消融实验表明，用 DB-SCAN 或 K-means 替换顺序 RANSAC 无法产生有效分割或导致性能显著下降，验证了基于刚体一致性采样的聚类策略对无先验设定的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/005_Figure_5.jpg]]
*Figure 5: Stage III: Motion-based part segmentation and articulation analysis. As the clean*



## 实验与关键发现

### 核心性能：部件分割

AIM 在两部件、三部件及复杂多部件物体上均取得了领先的部件分割精度，尤其在未知部件数量的复杂场景下优势显著。Table 1 汇总了定量对比结果：

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/006_Table_1.jpg]]
*Table 1: Part segmentation performance on articulated objects. (a) Two-part; (b) Three-part; (c) Complex objects. For two-part objects, 3D IoU(%) is reported as mean±std over 10 trials, while for three-part and complex objects, we report mean 3D IoU(%) over 10 trials*

- **两部件物体**：在 Oven 上，AIM 的动态部件 3D IoU 达到 **89.61%**，远超最佳基线 ArtGS 的 65.68%，提升 **+23.93 个百分点**。在 Fridge、Laptop 等其余物体上，AIM 同样保持最优或次优水平，且标准差显著低于依赖部件数量先验的对比方法，表明其分割稳定性更高。
- **复杂多部件物体**：在 Storage（6 个运动部件）上，AIM 的动态部件平均 3D IoU 达到 **69.01%**，比 ArtGS（65.30%）和 DTA（39.01%）分别高出 3.71 和 30.00 个百分点。DTA 和 ArtGS 因依赖预设部件数量，在复杂场景下常出现过度分割（Figure 2 左），而 AIM 无需此先验，直接从运动轨迹中自动恢复正确的部件划分。

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/002_Figure_2.jpg]]
*Figure 2: Left: DTA and ArtGS fail to recover from an incorrect input number of parts (4 here) and result in oversegmentations; Right: Visual results of DTA and ArtGS with closed-start and open-end states. The static part is gray and the moving part is green. In contrast, Ours requires no geometric priors and recovers accurate part-level segmentation from the continuous closed-start→open-end interaction process*

**Figure 6** 的定性结果进一步印证了这一结论：在 Storage-47648 上，AIM 为每个运动部件输出了清晰的语义分割掩码，且关节轴方向与部件颜色一一对应，与真值高度吻合。

### 核心性能：关节估计

Table 3 的关节参数估计结果表明，AIM 在复杂物体上的关节轴角度误差降低了 **一个数量级以上**：

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation of articulation estimation. (a) Two-part; (b) Three-part; (c) Complex objects. For complex objects, we report the average of all moving parts. Due to the different magnitudes of part motion for revolute and prismatic joints, we report both of them. F denotes failure. W T denotes that more than 6 out of 10 trials result in an incorrect joint-type prediction. − indicates prismatic joints w/o rotation axis*

- **Storage 47648**：平均关节轴角度误差从 ArtGS 的 10.18° 降至 **0.08°**，误差减少 **99% 以上**。
- **Table 31249**：角度误差从 ArtGS 的 33.19° 降至 **1.19°**，降幅达 **32.00°**。
- 在两部件物体上，AIM 的关节轴角度误差同样保持最低（如 Fridge 0.57° vs. ArtGS 0.65°），且轴位置误差和部件运动幅度误差均优于或持平于使用 RGB-D 输入的基线方法。

值得注意的是，AIM 仅使用 RGB 视频输入，而 PARIS、DTA、ArtGS 均依赖 RGB-D 深度信息，但 AIM 在关节估计精度上仍全面领先，这归因于其从连续运动轨迹中直接解析刚体变换的闭环解析策略，避免了优化过程中的局部极小和初始化敏感问题。

### 网格重建质量

Table 2 报告了网格重建的 Chamfer 距离（CD）。在 Storage 47648 上，AIM 的动态部件 CD 仅为 **8.36 mm**，而 ArtGS 为 17.43 mm，DTA 则高达 91.52 mm。静态部件重建方面，AIM 与使用 RGB-D 输入的 PARIS、ArtGS 保持可比水平，说明双高斯表示在解耦动态与静态的同时，未牺牲静态几何的保真度。

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/007_Table_2.jpg]]
*Table 2: Mesh reconstruction comparison. (a) Two-part objects; (b) Three-part objects; (c) Complex objects. For two-part objects, we report CD distance (mm) as mean±std across 10 trials. For three-part and complex objects, we only report the mean value, while we report average CD for movable parts. Lower (↓) is better*

### 消融实验

Table 4 的系统消融揭示了各模块的因果贡献：

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/011_Table_4.jpg]]
*Table 4: Ablation studies on complex objects. We report the average metrics of dynamic parts. And we calculate the mean across three trials*

1. **双高斯表示的核心作用**：将双高斯替换为单一 Deformable 3DGS（Ours-b）后，Storage 47648 的动态部件 CD 从 8.36 剧增至 **17.43**，同时动态部件平均 3D IoU 从 79.34% 降至 72.60%。**Figure A14** 的定性对比显示，Deformable 3DGS 的静态噪声严重污染了运动轨迹聚类，导致分割碎片化。
2. **初始状态扫描的必要性**：移除预重建的静态高斯集（随机初始化）后，动态部件平均 IoU 从 79.34% 骤降至 **37.60%**，表明精确的初始几何先验是后续动态-静态解耦的基础。
3. **SDMD 模块的关键性**：禁用 SDMD 后，Storage 47648 的动态部件 CD 飙升至 **91.52**，IoU 降至 53.83%。**Figure 4** 直观展示了无 SDMD 时的失败模式：新出现的静态内部区域被错误关联到运动高斯集，导致静态泄漏和运动轨迹污染。
4. **顺序 RANSAC 的不可替代性**：用 DB-SCAN 或 K-means 替换顺序 RANSAC 后，要么无法产生有效分割，要么性能显著下降。这是因为基于密度的聚类无法区分刚体运动模式的一致性，而顺序 RANSAC 通过 Kabsch 算法（Eq. 2）显式检验刚体变换假设，从机制上保证了聚类的物理合理性。

### 失败模式与局限性

尽管 AIM 在受控合成数据上表现优异，论文揭示了以下边界情形：

- **镜面反射物体**：烤箱玻璃门的强镜面反射导致 3DGS 重建出现伪影，进而影响动态-静态分离。**Figure A11** 的真实世界实验表明，SDMD 模块可部分缓解此问题，但重建质量仍是瓶颈。
- **完全展开部件的几何缺失**：抽屉、刀片等完全拉出后，内部几何在初始扫描中不可见，AIM 无法补全这些区域，需借助数据驱动生成模型。
- **相互依赖运动**：当前方法假定各部件独立运动，对于具有耦合自由度的铰接结构（如多连杆机构）尚未处理。
- **真实世界部署**：当前捕获流程依赖 AR 眼镜和手动交互，自动化程度有限；复杂物体需 500 帧运动视频，对采集效率提出要求。

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/026_Figure.jpg]]
*Figure: GT Figure A11: Qualitative results of our AIM on the real-world data of the oven. Left: Comparison between the ground-truth views and rendered views. Besides, we provide the rendered masks based on our dual-Gaussian representation (via directly changing the spherical harmonics of Gaussians). Due to the strong specular reflections on the oven’s glass door, the appearance of the moving part undergoes frequent and significant changes during interaction. Despite this challenge, our dual-Gaussian representation still achieves clean dynamic–static disentanglement by relying on stable motion cues. Moreover, the SDMD module reliably reassigns the newly revealed static interior regions back to the s...*

### 公平性说明

所有对比方法在相同数据集上评估，使用统一的 3D IoU、Chamfer 距离、关节轴角度/位置误差等指标。对于两状态基线（PARIS、DTA、ArtGS），作者使用其公开代码在相同数据上运行，并报告多次试验的均值与标准差。AIM 仅使用 RGB 输入，而部分基线使用 RGB-D，但 AIM 仍在多数指标上取得更优性能，排除了输入模态带来的不公平优势。

### 补充图表

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/001_Figure_1.jpg]]
*Figure 1: Left: Prior two-state methods often degrade on the sequences from closed-start to open-end. Right: Results of the proposed AIM, compared to ground truth (GT) geometry*

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative results of part segmentation and articulation estimation on two two-part objects (fridge, left; oven, middle) and a complex multi-part object (Storage-47648, right). For complex object, each predicted joint axis is visualised using the same colour as its corresponding part segmentation mask. Across the two-part objects, DTA and ArtGS often struggle with mis-segmentation and inaccurate joint-axis/type predictions. In contrast, our method produces clean part segmentation and consistent joint-axis estimation across all objects*

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/032_Figure.jpg]]
*Figure: A13: Qualitative comparisons for the ablation studies*

![[assets/figures/papers/paper_list_l1786_Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated/figures/019_Figure.jpg]]
*Figure: A6: Qualitative comparison between DTA, ArtGS and ours, w.r.t. GT*



## 定位与知识库关联

### 1. 与现有基线的结构性差异

AIM 与现有铰接物体分析方法的根本分歧在于**输入模态**与**先验依赖**两个维度。传统方法——包括 **PARIS** (Liu et al., CVPR 2023)、**DTA** (Weng et al., 2024) 和 **ArtGS** (Liu et al., 2025)——均采用“开始-结束”两个离散状态的 RGB/RGB-D 图像作为输入。这一设计隐含两个强假设：(a) 部件数量已知且作为先验输入；(b) 两个状态之间存在可靠的几何对应关系。当最终状态暴露出初始状态不可见的区域（如冰箱门打开后显露的内部搁架），跨状态对应关系即告失效，导致分割与关节估计严重退化（见 Figure 1 左侧，Figure 2 左侧）。AIM 将输入替换为**初始状态的多视图扫描 + 连续运动视频（单目 RGB）**，从根本上规避了跨状态对应问题：运动本身提供了天然的部件分离线索，无需几何对应。

在**动态-静态分离机制**上，PARIS 和 ArtGS 基于变形场或线性混合蒙皮在所有高斯/点上统一定义变形，缺乏显式的静态-动态解耦。AIM 引入**双高斯表示**：初始静态高斯集 `{G^S}` 通过联合优化逐步剪枝，可变形高斯集 `{G^M, t}` 专门跟踪运动部件。这一设计的关键创新在于**静态运动检测模块（SDMD）**：当运动过程中暴露出原本被遮挡的静态区域（如烤箱内壁），SDMD 通过顺序 RANSAC 检测近零运动轨迹，将这些高斯从可变形集归还至静态集，从而维持两个集合的纯净性。消融实验证实了这一设计的决定性作用：移除 SDMD 后，Storage 47648 的动态部件 Chamfer 距离从 8.36 急剧增至 91.52。

在**部件分割与关节估计**上，DTA 和 ArtGS 需要已知部件数量，通过优化预测部件分割后估计关节参数。AIM 的**顺序 RANSAC** 对运动高斯轨迹进行刚体聚类，自动确定部件数量，并直接从轨迹中解析关节参数（轴方向、旋转角、平移量、关节位置），无需任何优化步骤。这一“无先验”特性使得 AIM 在复杂多部件物体上展现出显著优势：Storage（6 个运动部件）上动态部件平均 3D IoU 达 69.01%，远超 ArtGS 的 65.30% 和 DTA 的 39.01%（Table 1(c)）。

### 2. 知识库定位与适用边界

AIM 在铰接物体分析领域填补了“**无先验部件数量、无需跨状态对应**”的方法空白。其核心贡献可定位于以下交叉点：

- **3D Gaussian Splatting 的动态扩展**：与 Deformable 3DGS 的单一场表示不同，AIM 提出了动静分离的双场架构，为动态场景的部件级建模提供了新范式。
- **基于运动的无监督分割**：顺序 RANSAC 利用多时间窗口的刚体轨迹一致性（结合 Kabsch 算法求解最优刚体变换，见 Eq. (2)-(4)），实现了无需语义先验的部件发现。
- **关节参数的直接解析**：通过 Rodrigues 旋转公式（Eq. (5)）从旋转矩阵恢复关节轴方向和角度（Eq. (6)），再计算平移距离与轴位置（Eq. (7)），避免了优化方法对初始化的敏感性。

**适用边界**方面，当前方法存在以下约束：

1. **镜面反射物体**：3DGS 重建对光照变化敏感，烤箱玻璃门等镜面表面可能导致动态-静态分离困难。真实世界数据上的定性结果（Figure A11）表明，运动线索在一定程度上可缓解此问题，但定量鲁棒性仍需验证。
2. **完全拉出部件的几何不完整**：抽屉、刀片等完全展开的部件内部几何无法从运动视频中恢复，需数据驱动方法补全。
3. **部件独立运动假设**：当前方法假定各部件运动相互独立，无法处理具有相互依赖自由度的铰接结构（如多连杆机构）。
4. **视频长度需求**：复杂多部件物体需要约 500 帧运动视频，对采集效率和存储提出要求。

### 3. 局限与开放问题

**已识别的局限**（来自论文分析与消融实验）：

- 消融实验表明，移除初始状态扫描（随机初始化静态高斯）导致 Storage 47648 动态部件平均 3D IoU 从 79.34% 降至 37.60%，说明 AIM 对初始几何重建质量有较强依赖。
- 用单一 Deformable 3DGS 替换双高斯表示后，Storage 47648 动态部件 Chamfer 距离升至 17.43，关节估计精度同步退化，证实动静分离架构的必要性。
- 用 DB-SCAN 或 K-means 替换顺序 RANSAC 无法产生有效分割或导致性能显著下降，表明轨迹聚类的算法选择对结果至关重要。

**开放问题**：

1. **多模态融合**：如何融合深度或多模态信息以减轻镜面反射和复杂光照对 3DGS 重建的影响？现有方法仅使用 RGB 输入，深度信息可能显著提升重建鲁棒性。
2. **大规模场景扩展**：如何将该方法扩展至包含大量部件或相互依赖运动的大规模真实场景，并保持计算效率？
3. **短序列与遮挡**：在运动视频较短或存在严重遮挡时，如何提升动态-静态解耦和轨迹推断的稳定性？当前方法依赖充分的运动观测。
4. **生成式几何补全**：能否利用数据驱动生成模型补充被遮挡或未观察到的内部部件几何，实现交互式数字副本的完整呈现？
5. **真实世界部署**：当前真实世界捕获依赖 AR 眼镜和手动交互，自动化程度及对日常设备的普适性仍有待提高。



## 原文 PDF

![[paperPDFs/ICLR_2026/Articulation_in_Motion_Prior_free_Part_Mobility_Analysis_for_Articulated_Objects.pdf]]

---
title: "IMU-HOI: A Symbiotic Framework for Coherent Human-Object Interaction and Motion Capture via Contact-Conscious Inertial Fusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IMU_HOI_A_Symbiotic_Framework_for_Coherent_Human_Object_Interaction_and_Motion_Capture_via_Contact_Conscious_Inertial_Fusion.pdf
project_link: null
code_link: null
aliases:
- IH
- IMU-HOI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于IMU流预测的概率性手-物接触信号（π_t），该信号作为门控变量，在运动学（FK）分支与惯性（IMU）分支之间进行贝叶斯式融合，从而在有接触时利用手部运动学锚定物体、无接触时依赖IMU积分。
primary_logic: 通过在人体和物体上同时佩戴稀疏IMU，并将手-物接触建模为可学习的概率先验，可以在不依赖视觉的条件下，端到端地联合恢复人体全身姿态与物体的6-DoF轨迹，实现漂移抑制和物理一致性。
claims:
- 在OMOMO数据集上，Obj Err 从GlobalPose*的39.34降至14.15（降幅64.0%），HOI Err 从39.56降至14.94（降幅62.2%）。
- 在IMHD²数据集上，Obj Err 从GlobalPose*的83.96降至43.97（降幅68.5%）；在BEHAVE上Obj Err 从25.81降至20.90（降幅30.6%）。
- 消融实验表明，接触门控融合（Fusion）在OMOMO上比仅IMU分支Obj Err降低0.21（1.8%），在IMHD²上比仅FK分支Obj Err降低17.61（28.6%）。
- OMOMO 上 Obj Err = 14.15
---

# IMU-HOI: A Symbiotic Framework for Coherent Human-Object Interaction and Motion Capture via Contact-Conscious Inertial Fusion

> [!tip] 核心洞察
> 通过在人体和物体上同时佩戴稀疏IMU，并将手-物接触建模为可学习的概率先验，可以在不依赖视觉的条件下，端到端地联合恢复人体全身姿态与物体的6-DoF轨迹，实现漂移抑制和物理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | IMU-HOI：一种基于接触感知惯性融合的协调人-物交互与运动捕捉共生框架 |
| 英文题名 | IMU-HOI: A Symbiotic Framework for Coherent Human-Object Interaction and Motion Capture via Contact-Conscious Inertial Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lin_IMU-HOI_A_Symbiotic_Framework_for_Coherent_Human-Object_Interaction_and_Motion_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | IMU-HOI |
| Dataset | OMOMO, IMHD², BEHAVE |

> [!tip] 效果简介
> - OMOMO 上，Obj Err 14.15 vs 39.34 (GlobalPose*) (-25.19 (64.0%))；HOI Err 14.94 vs 39.56 (GlobalPose*) (-24.62 (62.2%))。
> - IMHD² 上，Obj Err 43.97 vs 83.96 (GlobalPose*) (-39.99 (68.5%))。
> - BEHAVE 上，Obj Err 20.90 vs 25.81 (GlobalPose*) (-4.91 (30.6%))。

## 概述

**IMU-HOI**（CVPR 2026）面向一个此前被惯性运动捕捉社区忽视的关键瓶颈：现有基于IMU的人体姿态估计方法孤立地重建人体运动，完全抛弃了人与物体的交互状态与物体自身的运动轨迹；而基于视觉的人-物交互（HOI）捕捉方案又受限于遮挡和有限的采集空间，难以在自然环境中部署。该工作的核心洞察在于，当人体与物体同时佩戴稀疏IMU时，手-物接触本身可以作为一种可学习的概率先验，端到端地联合驱动人体全身姿态与物体6-DoF平移轨迹的恢复。

为实现这一目标，IMU-HOI设计了一个三阶段的接触感知惯性融合流水线（见Figure 2）。第一阶段从局部IMU窗口预测校准的手-物接触先验 $\pi_t$ 与短时物体速度；第二阶段采用分区式架构估计人体全身关节与根部平移；第三阶段则是该方法的核心贡献——接触门控的运动学-惯性融合：$\pi_t$ 作为门控变量，在左/右手运动学（FK）分支与物体IMU积分分支之间进行贝叶斯式融合，使得有接触时利用手部运动学锚定物体、无接触时依赖IMU积分，从而有效抑制漂移并保持物理一致性。

实验证据表明，IMU-HOI在多个数据集上取得了显著且一致的增益。在OMOMO数据集上，物体误差（Obj Err）从GlobalPose\*的39.34降至14.15（降幅64.0%），人-物交互误差（HOI Err）从39.56降至14.94（降幅62.2%）；在IMHD²数据集上，Obj Err从83.96降至43.97（降幅68.5%）；在BEHAVE上Obj Err从25.81降至20.90（降幅30.6%）（Table 1, Table 2）。消融实验进一步验证了接触门控融合的有效性：在OMOMO上比纯IMU分支Obj Err降低0.21（1.8%），在IMHD²上比纯FK分支Obj Err降低17.61（28.6%）（Table 3）。此外，该接触门控融合模块具有良好的即插即用特性，可直接部署到DynaIP、TransPose等现有IMU人体姿态估计器上，在IMHD²上为GlobalPose\*带来Obj Err降低54.57（53.9%）的增益（Table 4）。

在方法谱系中，IMU-HOI首次将稀疏IMU运动捕捉从纯人体域拓展至人-物交互域，填补了惯性HOI捕捉的空白。其接触门控融合机制提供了一种将物理接触信号显式注入学习的范式，区别于传统仅依赖足-地接触的全局平移估计方案。需要指出的是，当前模型基于准刚性、单接触假设，不显式处理滑动接触、多点同时接触或可变形物体的交互，这些构成了该方向后续研究的主要开放性挑战。

## 背景与动机

人体运动捕捉是计算机视觉与图形学领域的核心问题，其应用涵盖混合现实、具身智能与数字人动画。传统光学运动捕捉系统虽能提供高精度全身姿态与物体轨迹，却受限于受控采集体积、多相机标定成本和严重遮挡场景。基于单目或RGB-D的视觉方法近年来在姿态估计上取得显著进展，但在人-物交互场景中仍面临两大瓶颈：**遮挡**导致手-物接触区域不可见，以及**受限采集体积**使物体轨迹超出相机视野后无法追踪。

惯性测量单元（IMU）因其不受光照与遮挡影响、采集体积不受限的特性，成为视觉方法的重要补充。现有基于IMU的人体运动捕捉方法，如**TransPose**（Yi et al., ACM TOG 2021）、**TIP**（Jiang et al., SIGGRAPH Asia 2022）与**DynaIP**（Zhang et al., CVPR 2024），已能仅凭稀疏体表传感器恢复全身姿态与根部平移。然而，这些方法的根本局限在于：**它们将人体视为孤立系统，完全忽略人与物体的交互与物体自身状态**。当人体与物体发生物理接触时，物体的运动学信息本可为人体姿态提供强约束，反之亦然，但现有方法无法利用这一共生关系，导致物体6-DoF轨迹完全丢失。

这一缺口催生了本文的核心动机：**能否在人体与物体上同时佩戴稀疏IMU，通过显式建模手-物接触，在无视觉依赖的条件下端到端地联合恢复人体全身姿态与物体6-DoF轨迹？** 这一思路面临三个关键挑战：

1. **接触感知的惯性融合**：如何从稀疏IMU信号中可靠地推断手-物接触状态，并将其作为路由机制，协调人体运动学推理与物体惯性积分？
2. **漂移抑制**：纯惯性积分不可避免地产生累积漂移，如何在接触阶段利用人体运动学锚定物体位置，在非接触阶段依赖IMU积分，实现平滑过渡与漂移抑制？
3. **模块化与兼容性**：如何设计即插即用的融合模块，使其能够赋能现有IMU人体姿态估计器，以最小代价获得物体追踪能力？

本文提出的IMU-HOI框架正是针对上述挑战的系统性回应。其核心洞察在于：**将手-物接触建模为可学习的概率先验，并以此作为贝叶斯式门控变量，在运动学分支与惯性分支之间进行自适应融合**——有接触时，手部运动学分支锚定物体；无接触时，物体IMU分支提供互补运动信息。这一设计使得框架无需任何视觉输入，即可在三个基准数据集上实现物体平移误差的大幅降低（最高达68.5%），并展现出对现有IMU姿态估计器的强即插即用能力。

## 核心创新

IMU-HOI 的核心创新在于将**概率性手‑物接触信号**显式建模为可学习的先验，并以此作为门控变量，在运动学（FK）推理与惯性（IMU）积分之间进行**贝叶斯式融合**，从而在不依赖视觉的条件下，端到端地联合恢复人体全身姿态与物体的 6‑DoF 平移轨迹。

### 从孤立人体到人‑物共生：填补的三个关键空白

现有基于 IMU 的人体运动捕捉方法（如 **DynaIP** (Zhang et al., CVPR 2024)、**TransPose** (Yi et al., ACM TOG 2021)、**TIP** (Jiang et al., SIGGRAPH Asia 2022)）仅以人体姿态为目标，完全忽略物体状态。IMU‑HOI 在此基础上引入了三个根本性的 **changed slots**：

| 维度 | 基线方法 | IMU‑HOI 的改进 | 证据锚点 |
|---|---|---|---|
| **物体状态估计** | 无（仅人体姿态） | 联合输出人体全身姿态与物体 6‑DoF 平移轨迹 | Abstract; 1. Introduction |
| **接触建模与利用** | 仅足‑地接触（用于根部平移） | 概率性手‑物接触先验 $\pi_t$，显式路由运动学与惯性推理 | 3.2; 3.4 |
| **物体平移估计分支** | 无 | 接触门控的三分支融合（左手 FK + 右手 FK + 物体 IMU 积分） | 3.4 |

这三个改变共同构成了一条**接触‑感知的惯性融合流水线**：接触信号既不是硬二元判定，也不是后处理规则，而是作为贯穿 Stage I 到 Stage III 的连续概率先验，驱动物体平移的平滑路由。

### 接触门控融合：因果机制与公式表达

IMU‑HOI 的因果旋钮是瞬时手‑物接触状态 $\pi_t$，其参数化为三类分布：

$$\pi_t = \left[ p_L(t), p_R(t), 1 - \max(p_L(t), p_R(t)) \right] \in \Delta^2$$

该参数化避免了双接触场景下的概率重复计算，将接触建模为 {左手, 右手, 无接触} 的互斥分类（式(3)）。Stage I 的 LSTM 头从局部 IMU 窗口预测该先验，并同时输出短时物体速度作为辅助运动线索。

在 Stage III，物体全局平移由三个分支的加权融合给出：

$$\hat{\mathbf{p}}_O(t) = \sum_{k \in \{L, R, IMU\}} w_{t,k} \hat{\mathbf{p}}_O^{(k)}(t)$$

其中 FK 分支基于**准刚性接触假设**：一旦手 $s$ 与物体建立接触，物体坐标系下的偏移 ${}^{O}\mathbf{d}^{(s)}$ 在接触段内保持不变（式(4)）。由此，物体位置可通过手部运动学直接锚定：

$$\hat{\mathbf{p}}_O^{FK-s}(t) = \hat{\mathbf{p}}_H^{(s)}(t) + {}^{W}R_O(t) {}^{O}\hat{\mathbf{u}}_t^{(s)} \hat{\ell}_t^{(s)}$$

融合权重 $\mathbf{w}_t$ 由 LSTM 预测的 logits $\mathbf{z}_t$ 与接触先验 $\pi_t$ 经温度 $\tau$ 的 softmax 生成：

$$\mathbf{w}_t = \mathrm{softmax}\Big( \frac{1}{\tau} \big[ \mathbf{z}_t + \beta \log \pi_t \big] \Big)$$

这一设计的核心效果是：**当接触置信度高时，FK 分支将物体锚定在手部运动学上，抑制 IMU 漂移；当接触减弱或断开时，IMU 分支接管，提供独立的惯性运动估计**。门控权重在两者之间实现平滑过渡，避免了硬切换带来的轨迹跳变。

### 即插即用的模块化设计

接触门控融合模块被设计为与具体人体姿态估计器解耦的独立组件。实验表明，将其即插即用到 **GlobalPose\***、**DynaIP**、**TransPose** 等现有 IMU 人体姿态估计主干上，可在 IMHD² 数据集上为 GlobalPose\* 降低 Obj Err 54.57（53.9%）和 HOI Err 48.34（47.4%）（Table 4）。这意味着该创新不仅提升了 IMU‑HOI 自身的性能，还具备向已有方法迁移的通用价值。

### 创新边界与局限

当前接触模型基于**准刚性、单接触假设**，不显式处理以下场景：
- 滑动接触或动态变化的接触点；
- 双手同时接触同一物体时的多点约束；
- 与可变形物体（如布料、绳索）的交互。

这些限制意味着 IMU‑HOI 在抓握稳定、接触点固定的刚性物体交互场景中表现最佳，而在推、滑、抛接等动态接触模式下的泛化能力仍需进一步验证。

## 整体框架

IMU-HOI 提出了一种**三阶段、接触感知的惯性融合架构**，其核心目标是从稀疏分布在人体与物体表面的 IMU 信号中，联合恢复全身人体姿态与物体的 6-DoF 平移轨迹，全程不依赖任何视觉输入。图 2 给出了管线的整体概览。

### 问题形式化

给定一段长度为 $T$ 的序列，系统接收的输入包括：附着于人体各分区的 IMU 测量值（加速度与角速度）、物体上的 IMU 测量值，以及一个已知的初始状态 $S_0 = \{ \mathbf{pose}_0, \mathbf{p}_{\mathrm{root}}(0), {}^W R_O(0), \mathbf{p}_O(0) \}$。输出为每一时刻 $t$ 的人体姿态、根部平移，以及物体的 6-DoF 平移轨迹。整个问题被解耦为三个串行阶段，每个阶段聚焦于一个可管理的子任务。

### 三阶段管线

**Stage I：接触与速度估计。** 该阶段从局部 IMU 时间窗口中提取短时运动线索，输出两个关键信号：一是校准后的手-物接触先验 $\pi_t$，建模为左、右或无接触的三类分类分布；二是短时物体速度，为后续的物体 IMU 分支提供运动先验。接触先验是整个框架的**因果旋钮**——它作为门控变量，在后续的运动学（FK）分支与惯性（IMU）分支之间进行贝叶斯式路由。

**Stage II：人体姿态与根部平移估计。** 该阶段采用分区式架构（继承自 **DynaIP**，Zhang et al., CVPR 2024）估计全身关节姿态，并利用双分支平移头（继承自 **TransPose**，Yi et al., ACM TOG 2021）恢复根部平移。Stage II 的输出为后续物体平移估计提供了手部位置 $\hat{\mathbf{p}}_H^{(s)}(t)$，这是 FK 分支的关键输入。

**Stage III：接触门控的 FK–IMU 融合物体平移估计。** 该阶段是框架的核心创新。它维护三个并行的物体位置假设分支——左手 FK、右手 FK 和物体 IMU 积分——并通过接触门控权重进行融合：

$$\hat{\mathbf{p}}_O(t) = \sum_{k \in \{L, R, IMU\}} w_{t,k} \hat{\mathbf{p}}_O^{(k)}(t)$$

融合权重 $\mathbf{w}_t$ 由 LSTM 预测的 logits 与 Stage I 输出的接触先验 $\pi_t$ 通过带温度 $\tau$ 的 softmax 共同决定：

$$\mathbf{w}_t = \mathrm{softmax}\Big( \frac{1}{\tau} \big[ \mathbf{z}_t + \beta \log \pi_t \big] \Big)$$

这一设计的**核心洞见**在于：当检测到可靠的手-物接触时，FK 分支将物体锚定到手部位置，利用人体运动学抑制纯惯性积分带来的漂移；当接触减弱或中断时，IMU 分支提供独立的物体运动估计，而门控机制在两者之间实现平滑过渡。FK 分支基于**准刚性接触假设**：一旦手 $s$ 与物体建立接触，接触点在物体坐标系下的偏移量 ${}^{O}\mathbf{d}^{(s)}$ 在接触段内保持不变，从而可以从手部位置和物体姿态推导出物体平移。

### 训练策略

训练采用分阶段策略：首先单独训练 Stage I，损失函数 $\mathcal{L}^{(1)} = \mathcal{L}_{\mathrm{hands}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{cal}} \mathcal{L}_{\mathrm{cal}}$ 监督手部接触分类、物体速度回归和校准正则化；随后固定 Stage I 权重，联合训练 Stage II 和 Stage III 的其余部分。这种解耦训练保证了接触先验的质量，为下游融合提供可靠的门控信号。

### 模块关系总结

三个阶段的依赖关系是严格串行的：Stage I 的接触先验同时服务于 Stage II（足部接触用于根部平移估计）和 Stage III（手部接触用于物体平移融合）；Stage II 的手部位置输出是 Stage III 中 FK 分支的必要输入；Stage III 的融合模块将前两个阶段的输出与物体 IMU 信号整合，产生最终的物体平移估计。这种设计使得接触门控融合模块具有**即插即用**的特性——消融实验表明，它可以被集成到 **DynaIP**、**TransPose**、**TIP**（Jiang et al., SIGGRAPH Asia 2022）等现有 IMU 人体姿态估计器中，以极小的额外代价赋予其交互感知的物体动态跟踪能力（见 Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our three-stage HOI pipeline from sparse human–object IMUs: Stage I (mid-bottom) predicts hand/foot contacts and object velocity, Stage II (mid-top) estimates part-based human pose and root translation, and Stage III (mid-right) contact-gates FK and IMU branches to recover object translation*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/001_Figure_1.jpg]]
*Figure 1: IMU-HOI recovers full-body human motion and 6-DoF object trajectories from a sparse set of stick-on IMUs attached to both the body and the object, without using cameras*

## 核心模块与公式推导

IMU-HOI 的核心设计在于将手-物接触建模为可学习的概率先验，并以此作为门控变量，在运动学推理与惯性积分之间进行自适应路由。整个流水线按三阶段展开，其中接触估计模块与物体平移融合模块是区别于现有纯惯性人体姿态估计方法的关键增量。

### 接触状态的概率化建模

Stage I 从局部 IMU 窗口中预测校准的手-物接触先验。接触状态被显式参数化为一个三类分布：

$$\pi_t = \left[ p_L(t), p_R(t), 1 - \max(p_L(t), p_R(t)) \right] \in \Delta^2$$

其中 $p_L(t)$ 和 $p_R(t)$ 分别表示左手和右手与物体接触的概率。该参数化方式避免了双接触情形下的概率重复计算，将瞬时接触状态归约为{左手接触，右手接触，无接触}的互斥分类。一个紧凑的 LSTM 头以人体和物体 IMU 的短时窗口为输入，输出 $p_L(t)$ 和 $p_R(t)$ 的 logits。

### 准刚性接触假设与运动学分支

Stage III 的核心前提是**准刚性接触模型**：一旦手 $s \in \{L, R\}$ 与物体建立接触，假设接触点在物体坐标系下保持固定。该偏移量定义为：

$$^{O}\mathbf{d}^{(s)} = {}^{W}R_O(t)^{\top} \big( {}^{W}\mathbf{p}_O(t) - {}^{W}\mathbf{p}_H^{(s)}(t) \big)$$

其中 ${}^{W}\mathbf{p}_O$ 和 ${}^{W}\mathbf{p}_H^{(s)}$ 分别为世界坐标系下物体和手部的位置，${}^{W}R_O$ 为物体朝向。在接触段内，$^{O}\mathbf{d}^{(s)}$ 被视为常数，由此可从手部位置反向推导物体位置：

$$\hat{\mathbf{p}}_O^{FK-s}(t) = \hat{\mathbf{p}}_H^{(s)}(t) + {}^{W}R_O(t) {}^{O}\hat{\mathbf{u}}_t^{(s)} \hat{\ell}_t^{(s)}$$

该式将物体平移假设分解为手部位置加上物体帧方向与长度的乘积，从而实现“以手锚定物体”的运动学推理。

### 接触门控的三分支融合

物体全局平移由三个分支的加权融合给出：

$$\hat{\mathbf{p}}_O(t) = \sum_{k \in \{L, R, IMU\}} w_{t,k} \hat{\mathbf{p}}_O^{(k)}(t)$$

其中 $k$ 分别对应左手 FK 分支、右手 FK 分支和物体 IMU 积分分支。融合权重 $\mathbf{w}_t$ 由一个 LSTM 预测的 logits $\mathbf{z}_t$ 与接触先验 $\pi_t$ 通过温度 $\tau$ 进行贝叶斯式结合：

$$\mathbf{w}_t = \mathrm{softmax}\Big( \frac{1}{\tau} \big[ \mathbf{z}_t + \beta \log \pi_t \big] \Big)$$

这一设计的因果机制在于：当接触概率高时，FK 分支获得主导权重，物体被手部运动学锚定，抑制纯惯性积分的漂移；当接触减弱时，IMU 分支权重上升，提供独立的物体运动信息。接触先验 $\pi_t$ 作为门控变量，在两者之间实现平滑过渡，避免了硬切换带来的不连续性。

### 训练策略

Stage I 独立预训练，损失函数为：

$$\mathcal{L}^{(1)} = \mathcal{L}_{\mathrm{hands}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{cal}} \mathcal{L}_{\mathrm{cal}}$$

其中 $\mathcal{L}_{\mathrm{hands}}$ 为手部接触分类损失，$\mathcal{L}_{\mathrm{vel}}$ 为短时物体速度回归损失，$\mathcal{L}_{\mathrm{cal}}$ 为校准正则项，用于约束接触概率的置信度与真实接触频率一致。Stage II 和 Stage III 在 Stage I 收敛后联合微调。

### 模块的即插即用特性

接触门控融合模块的设计与人体姿态估计主干解耦。消融实验表明，将该模块即插即用到 **DynaIP**（Zhang et al., CVPR 2024）、**TransPose**（Yi et al., ACM TOG 2021）等现有 IMU 人体姿态估计器上，可在 IMHD² 数据集上为 GlobalPose* 降低 Obj Err 54.57（53.9%）和 HOI Err 48.34（47.4%），验证了其作为通用物体运动捕捉插件的有效性。

## 实验与分析

### 核心实验设置

IMU-HOI 在三个公开的人-物交互（HOI）数据集上进行评估：**OMOMO**（日常物体交互）、**IMHD²**（高动态双手交互）和 **BEHAVE**（自然场景交互）。所有对比方法均使用相同的稀疏 IMU 传感器配置（人体 6 个、物体 1 个），且**不依赖任何视觉信息**，保证与纯惯性方法的公平比较。基线方法包括扩展的纯惯性人体姿态估计器 **GlobalPose\***，以及 **DynaIP**（Zhang et al., CVPR 2024）、**TransPose**（Yi et al., ACM TOG 2021）和 **TIP**（Jiang et al., SIGGRAPH Asia 2022）等代表性稀疏 IMU 人体运动重建方法。

评价指标涵盖物体平移误差（Obj Err，cm）、人-物交互误差（HOI Err，cm）、角度误差（Ang Err，°）、位置误差（Pos Err，cm）和运动抖动（Jitter，m/s³），均为越低越好。

### 主要定量结果

**Table 1** 给出了不包含根部平移的对比结果。IMU-HOI 在所有三个数据集上均取得最优的 Obj Err 和 HOI Err：

- 在 **OMOMO** 上，Obj Err 从 GlobalPose\* 的 39.34 降至 **14.15**，降幅达 **64.0%**；HOI Err 从 39.56 降至 **14.94**，降幅达 **62.2%**。这一大幅提升表明，接触感知融合有效将物体轨迹锚定到人体运动上，克服了纯惯性积分的漂移问题。
- 在 **IMHD²** 上，Obj Err 从 GlobalPose\* 的 83.96 降至 **49.76**，降幅约 40.7%；HOI Err 从 84.62 降至 **51.09**，降幅约 39.6%。IMHD² 的高动态双手交互场景对纯惯性方法构成极大挑战，而 IMU-HOI 通过双 FK 分支与 IMU 分支的贝叶斯式融合，显著抑制了漂移。
- 在 **BEHAVE** 上，Obj Err 从 GlobalPose\* 的 25.81 降至 **22.26**，降幅约 13.8%；HOI Err 从 26.12 降至 **22.62**，降幅约 13.4%。BEHAVE 场景中交互动作相对简单，基线已有一定精度，但 IMU-HOI 仍保持一致的增益。

**Table 2** 进一步评估了包含根部平移和运动抖动的完整指标。IMU-HOI 在所有数据集上继续领先：

- 在 **OMOMO** 上，Obj Err 为 **11.31**，HOI Err 为 **17.44**，相比 GlobalPose\* 分别降低 28.03（71.3%）和 22.12（55.9%）。
- 在 **IMHD²** 上，Obj Err 从 83.96 降至 **43.97**，降幅达 **68.5%**，表明接触门控融合在高动态场景中的全局平移估计上优势更为突出。
- 在 **BEHAVE** 上，Obj Err 从 25.81 降至 **20.90**，降幅 **30.6%**。

**Figure 3** 展示了 OMOMO 和 BEHAVE 数据集上的累积根部平移误差随时间的变化曲线。IMU-HOI 的误差增长速率显著低于 GlobalPose\*，特别是在长序列中，接触门控机制有效抑制了漂移的累积。

### 消融实验

**Table 3** 对物体平移头的三种变体进行消融，揭示了接触门控融合的核心作用：

- **仅 IMU 分支**：纯惯性积分，无接触信息利用。
- **仅 FK 分支**：仅依赖手部运动学锚定，无 IMU 积分补偿。
- **Fusion（完整方法）**：接触门控融合左右手 FK 与 IMU 三分支。

在 **OMOMO** 上，Fusion 相比仅 IMU 分支 Obj Err 降低 0.21（1.8%），HOI Err 降低 0.63（3.5%）。由于 OMOMO 场景中接触频繁且稳定，FK 分支本身已能提供较好锚定，但 Fusion 仍通过 IMU 分支在弱接触时刻提供补充，带来小幅增益。

在 **IMHD²** 上，Fusion 相比仅 FK 分支 Obj Err 降低 **17.61（28.6%）**，HOI Err 降低 **14.25（24.7%）**。这一显著差距揭示了关键机制：**高动态交互中接触频繁断裂，纯 FK 分支在无接触时完全失效，而 Fusion 通过接触门控在 FK 与 IMU 分支间平滑过渡，利用 IMU 积分填补接触间隙，从而大幅抑制漂移。**

**Figure 5** 提供了三个平移头变体的误差-时间曲线与参考帧可视化，直观展示了 Fusion 在接触状态切换时刻（如抓取-释放过渡）的误差控制优势：仅 IMU 分支随时间漂移累积，仅 FK 分支在释放后误差骤增，而 Fusion 实现了两者的自适应切换。

### 即插即用泛化性

**Table 4** 展示了接触门控融合模块的即插即用能力。将该模块集成到 DynaIP、TransPose、TIP 等现成的 IMU 人体姿态估计器上，可在 **IMHD²** 上为 GlobalPose\* 降低 Obj Err **54.57（53.9%）**和 HOI Err **48.34（47.4%）**。这表明接触门控融合作为独立模块，能够以极小额外成本将任意稀疏 IMU 姿态估计器升级为交互感知的物体轨迹跟踪系统。

### 定性分析

**Figure 4** 展示了 BEHAVE 测试集上四个序列的运动估计可视化对比。IMU-HOI 恢复的物体轨迹与真值高度吻合，尤其在涉及抓取、搬运、放置的连续交互序列中，物体位置未出现纯惯性方法常见的漂移现象。在双手交替接触场景中，接触门控机制能够正确识别活跃手并切换 FK 锚定源，保持物体轨迹的连续性。

### 失败模式与局限性

尽管 IMU-HOI 在多数场景下表现优异，其核心假设——**准刚性、单接触模型**——构成了主要局限：

1. **滑动接触**：当手在物体表面滑动时，物体坐标系下的接触偏移量不再恒定（违反式(4)的准刚性假设），FK 分支的物体位置假设将产生系统性偏差。此时接触门控可能错误地信任 FK 分支，导致物体轨迹失真。
2. **多点同时接触**：双手同时稳定抓握物体时，当前参数化 $\pi_t = [p_L(t), p_R(t), 1 - \max(p_L(t), p_R(t))]$ 无法建模双接触状态，融合权重分配可能次优。
3. **可变形物体**：对于软体或形状变化的物体，物体坐标系下的固定偏移假设完全失效，FK 分支不可用。

这些场景下，融合权重应更多地偏向 IMU 分支，但当前接触预测器未针对滑动或双接触状态进行校准，可能导致门控决策错误。需要手动验证这些边界情况的性能。

### 开放问题

- 如何扩展接触模型以处理滑动接触或动态变化的接触点？
- 能否支持多物体或可变形物体的交互？
- 在缺乏接触标注数据的更广泛场景中，接触预测的泛化能力如何？

### 补充图表

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/003_Table_1.jpg]]
*Table 1: Comparison on three HOI datasets. Numbers are lower-is-better. Best in bold*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/004_Table_2.jpg]]
*Table 2: Main comparison with root-translation and jitter. Numbers are lower-is-better. Best in bold*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/006_Table_3.jpg]]
*Table 3: Ablation of our object-translation heads. Lower is better. Best in bold*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/009_Table_4.jpg]]
*Table 4: Fusion on off-the-shelf IMU HPE backbones. Lower is better. Best in bold*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/005_Figure_3.jpg]]
*Figure 3: Cumulative root-translation error vs. time for OMOMO (left) and BEHAVE (right)*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/008_Figure_5.jpg]]
*Figure 5: Visualization of error–time curves and reference frames (A–D) for the three object-translation heads*

![[assets/figures/papers/paper_list_l1065_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_IMU_HOI_A_Symbioti/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of motion estimation on four sequences from the BEHAVE test set*

## 方法谱系与知识库定位

### 1. 基线关系与演进定位

IMU‑HOI 处于 **稀疏惯性运动捕捉** 与 **人‑物交互 (HOI) 理解** 的交叉点。其直接对比的基线可分为两类：纯惯性人体姿态估计器和该工作的无物体感知扩展版本。

**纯惯性人体姿态估计基线**。论文选取了三个代表性方法作为人体姿态骨干的参照点：
- **DynaIP** (Zhang et al., CVPR 2024)：采用分区架构从稀疏 IMU 恢复人体姿态，IMU‑HOI 在 Stage II 继承了其分区设计思路。
- **TransPose** (Yi et al., ACM TOG 2021)：实时六 IMU 人体平移与姿态估计方法，IMU‑HOI 在 Stage II 的根部平移估计中采用了 TransPose 式的双分支平移头。
- **TIP** (Jiang et al., SIGGRAPH Asia 2022)：基于 Transformer 的稀疏 IMU 人体运动重建方法。

**GlobalPose\*** 是论文构造的 **扩展基线**：将纯惯性人体姿态估计器扩展为同时输出物体位姿，用于量化引入物体感知建模后的增益。在 OMOMO 数据集上，GlobalPose\* 的 Obj Err 为 39.34、HOI Err 为 39.56，而 IMU‑HOI 将这两项指标分别降至 14.15（降幅 64.0%）和 14.94（降幅 62.2%）（Table 1）。这一巨大差距揭示了 **核心瓶颈**：现有方法孤立地重建人体姿态，完全忽略了手‑物接触信号与物体运动学约束，因而无法恢复物体轨迹。

**演进逻辑**。IMU‑HOI 并非简单地将物体 IMU 作为额外输入，而是引入了一个 **可学习的概率性接触先验** 作为门控变量，在运动学 (FK) 分支与惯性 (IMU) 分支之间进行贝叶斯式路由。这一设计将“接触”从隐式特征提升为显式的因果调节旋钮：有接触时，手部运动学锚定物体；无接触时，物体 IMU 积分接管。这种 **接触感知的惯性融合** 是 IMU‑HOI 区别于所有纯惯性基线的方法论增量。

### 2. 模块化与即插即用能力

接触门控融合模块被设计为 **与骨干网络解耦** 的独立组件。Table 4 的即插即用实验表明，将该模块直接接入 DynaIP、TransPose 等现有 IMU 人体姿态估计器，可在 IMHD² 数据集上为 GlobalPose\* 带来 Obj Err 降低 54.57（降幅 53.9%）、HOI Err 降低 48.34（降幅 47.4%）。这验证了接触门控融合的 **架构无关性** 和 **最小侵入性**——无需修改骨干网络即可赋予其物体轨迹感知能力。

### 3. 适用边界与假设约束

IMU‑HOI 的有效性建立在以下假设之上，这些假设同时划定了其适用边界：

1. **准刚性接触假设**。方法假定手与物体一旦建立接触，接触点在物体坐标系下的位置在整个交互段内保持不变（式 4）。这意味着 **滑动接触、滚动接触或动态变化的接触点** 不在显式建模范围内。
2. **单接触主导假设**。接触状态被参数化为左、右或无接触的三类分布（式 3），通过 $\max(p_L, p_R)$ 避免双接触时的概率重复计算。这隐含假设每个时刻最多一只手与物体发生有效接触，**多点同时接触**（如双手同时抓握不同部位）的场景未被显式处理。
3. **刚性物体假设**。方法针对刚性物体的 6‑DoF 轨迹估计设计，**可变形物体** 或 **多物体交互** 场景超出当前框架的覆盖范围。

### 4. 局限性与开放问题

论文明确指出的局限性集中在交互模型的简化上：不显式处理滑动接触、多点同时接触或与可变形物体的交互。从方法论角度，以下开放问题值得关注：

- **接触预测的泛化能力**。接触先验 $\pi_t$ 由 Stage I 的 LSTM 头从局部 IMU 窗口预测，其训练依赖接触标注数据。在没有接触标注的更广泛场景（如野外日常活动）中，接触预测的准确性和校准性有待验证。
- **滑动与动态接触建模**。准刚性偏移 $^{O}\mathbf{d}^{(s)}$ 在接触段内被假设为常数，但实际交互中抓握点可能发生漂移。引入时变偏移或接触点不确定性建模可能是自然扩展方向。
- **多物体与可变形物体扩展**。当前框架以单一刚性物体为前提，扩展到多个物体需要解决物体间关联与遮挡推理；扩展到可变形物体则需要重新定义“接触”与“物体状态”的表征方式。

### 5. 知识库定位

在更广阔的 HOI 重建知识库中，IMU‑HOI 代表了一条 **纯惯性、无视觉** 的技术路径。与基于视觉的方法（受遮挡和受限采集体积影响）相比，IMU‑HOI 以牺牲物体朝向与形状细节为代价，换取了无拘束环境下的鲁棒性。其核心贡献——将手‑物接触建模为可学习概率先验并用于门控多分支融合——可被视为 **接触感知传感器融合** 的通用范式，对多模态 HOI 重建（如视觉‑惯性联合）具有潜在启发性。

## 原文 PDF

![[paperPDFs/CVPR_2026/IMU_HOI_A_Symbiotic_Framework_for_Coherent_Human_Object_Interaction_and_Motion_Capture_via_Contact_Conscious_Inertial_Fusion.pdf]]
---
title: Intuitive and Efficient Camera Control with the Toric Space
type: paper
paper_level: A
venue: TOG
year: 2015
pdf_ref: paperPDFs/TOG_2015/Intuitive_and_Efficient_Camera_Control_with_the_Toric_Space.pdf
aliases:
- TSCC
- IECCTS
tags:
- TOG_2015
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Toric空间将两目标问题参数化为角度三元组(α, θ, φ)，将搜索空间降至4自由度，并可将视觉属性表达为这些角度上的区间约束，进而支持确定性区间剪枝。
primary_logic: 通过在Toric空间中代数表达视觉属性的解集（角度区间或2D区域），可以直接修剪不可行区域，从而实现高效确定性相机求解，并能构建出直接在屏幕空间操纵这些属性的直观交互控件。
claims:
- Toric空间将两目标相机优化从7-DOF降至4-DOF。
- 视觉属性（构图、距离、大小、视角）可直接在Toric空间中表达为区间或二维子集，用于剪枝。
- 基于区间的确定性搜索在速度和满意度上均优于随机优化方法(Ranon & Urli)。
- 屏幕空间操作器使新手用户完成任务的速度显著快于传统MotionBuilder操作。
---

# Intuitive and Efficient Camera Control with the Toric Space

> [!tip] 核心洞察
> 通过在Toric空间中代数表达视觉属性的解集（角度区间或2D区域），可以直接修剪不可行区域，从而实现高效确定性相机求解，并能构建出直接在屏幕空间操纵这些属性的直观交互控件。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于Toric空间的直观高效虚拟相机控制 |
| 英文题名 | Intuitive and Efficient Camera Control with the Toric Space |
| 会议/期刊 | TOG 2015 |
| Links | [paper](https://doi.org/10.1145/2766965) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Toric Space Camera Control |
| Dataset | Five viewpoint composition problems from Ranon & Urli 2014, Precise framing problem, User study: reproduce a reference viewpoint, Interpolation cost: 7-key / 15-key viewpoint sequences |

> [!tip] 效果简介
> - Five viewpoint composition problems from Ranon & Urli 2014 上，Satisfaction mean (%) at ~5ms search time 89% vs 85% (Ranon & Urli) (+4% satisfaction, ~20-40% less computation time)。
> - Precise framing problem (two targets, tight on-screen regions) 上，Satisfaction mean (%) at 100ms / 200ms search budget 100% at both 100ms and 200ms vs Ranon & Urli cannot reach 100% (perfect satisfaction vs. suboptimal)。
> - User study: reproduce a reference viewpoint 上，Mean manipulation time (seconds) lower for novices (blue bars, Figure 9) vs MotionBuilder classical interaction (red bars) (significant time reduction for novices)。

## 概述

**问题瓶颈**：虚拟相机控制是三维交互中的基础任务，但传统方法面临两难困境——直接操纵相机自由度（如平移、旋转、变焦）虽然灵活，却要求用户将高层视觉意图（“让目标A在画面左侧，目标B在右侧，且保持特定视角”）手动翻译为低层变换序列；而自动视角计算方法通常在7自由度空间中进行随机优化（如**Ranon & Urli**，IEEE TVCG 2014），计算代价高且缺乏确定性保证。

**核心思路**：本文提出**Toric空间**（Toric Space）——一种将两目标相机控制问题从7自由度压缩至4自由度的紧凑表示。该空间将相机位置参数化为围绕两个目标的角度三元组 $(\alpha, \theta, \varphi)$，其中 $\alpha$ 控制相机到两目标的距离关系，$\theta$ 和 $\varphi$ 分别控制水平和垂直环绕角度。在此表示下，相机朝向可通过代数方式直接确定，无需额外优化（Section 3.1）。

**关键洞察**：Toric空间的核心优势在于，构图、距离、目标大小、视角等视觉属性均可被表达为该空间上的角度区间或二维解集。这使得相机求解从“在连续空间中随机搜索”转变为“在Toric空间中对各属性解集求交的确定性区间剪枝”——既保证了求解的完备性，又大幅提升了计算效率。

**方法定位**：本工作在方法谱系上处于**基于屏幕空间的相机操纵**与**自动视角计算**的交汇点。其前身是**Lino & Christie**（SCA 2012）提出的二维Toric流形，本文将其推广到三维空间，并在此基础上构建了完整的交互与控制流水线。

**主要结果**：
- **自动视角计算**：在Ranon & Urli（2014）的五个标准问题上，Toric方法在约5ms计算预算下达到89%的属性满意度，优于基线方法的85%，且计算时间减少20–40%（Table 1a）；在精确构图问题上达到100%满意度，而基线方法无法完全满足（Table 1b）。
- **用户交互**：基于Toric空间的屏幕空间操纵器（位置、大小、视角、Vertigo四种）使新手用户完成视角重建任务的平均时间显著低于Autodesk MotionBuilder的传统操纵方式（Figure 9）。
- **视角插值**：基于构图的代数插值方法可在91ms内生成45秒的7关键帧相机序列，计算成本约为每电影秒2ms（30fps下），满足实时性能需求。

**局限性**：当前方法原生仅支持两个目标，未处理遮挡可见性约束，且插值路径无法保持线性推轨运动。这些构成了后续研究的主要开放问题。

## 背景与动机

在三维虚拟环境（如电影预演、游戏关卡编辑、建筑漫游）中，相机控制是创作者与场景交互的核心环节。一个理想的相机系统需要同时满足两类需求：**自动视角计算**——根据给定的视觉属性约束（如目标在屏幕上的位置、大小、视角角度）求解最优相机位姿；以及**交互式操纵**——让用户能直观、实时地调整画面构图。然而，这两类任务在传统方法中长期面临一个共同的瓶颈：**搜索空间的高维度与视觉属性表达之间的断层**。

具体而言，一个虚拟相机的完整配置包含7个自由度（7-DOF）：三维位置、三维朝向（通常用欧拉角或四元数表示）以及视场角（field of view）。当用户或自动化算法需要满足“目标A位于画面左三分之一处，目标B占据画面约20%面积，且从侧面约45°观察”这类高层视觉约束时，7-DOF空间中的搜索本质上是一个代价高昂的逆向问题。现有方法主要沿两条路径应对这一挑战：

- **基于优化的方法**（如 **Ranon & Urli, IEEE TVCG 2014** 的粒子群优化框架）将视觉属性表达为目标函数，通过随机搜索在7-DOF空间中寻找最优解。这类方法虽然通用，但计算成本高，且无法保证找到满足所有约束的解——其随机本质决定了它可能陷入局部最优或遗漏可行区域。

- **直接操纵方法**（如 **Autodesk MotionBuilder** 等商业软件中的平移/旋转/缩放控件）让用户通过低层变换操作相机。这种方式虽然灵活，但要求用户将高层构图意图（“让这个角色变大一点，同时保持另一个角色在画面中的位置不变”）在脑内翻译为一系列相机变换序列，操作繁琐且容易破坏已建立的其他视觉属性。

这种“高层视觉意图”与“低层相机参数”之间的语义鸿沟，构成了虚拟相机控制领域的核心瓶颈。**Lino & Christie (SCA 2012)** 提出的Toric流形（Toric manifold）首次为这一问题提供了几何突破口：他们证明，在给定两个目标点的情况下，能够以特定方式将两个目标投影到屏幕指定位置的所有相机，其位置落在一个二维流形曲面上。这一发现将两目标构图问题从7-DOF降至2-DOF搜索。然而，该表示仅覆盖了相机位置，并未系统性地整合朝向、视场角以及其他视觉属性（如目标距离、屏幕大小、视角角度）的表达。

本文的核心动机正是基于这一缺口：**能否构建一个统一的表示空间，使得所有关键的视觉属性都能在其中被代数化地表达为区间约束，从而将相机控制问题转化为确定性的可行域剪枝与搜索？** 这一问题的肯定回答将带来三重收益：（1）自动视角计算可以从随机优化转变为高效、可预测的确定性求解；（2）交互式操纵可以从低层相机变换升级为直接在屏幕空间拖拽视觉属性的直观控件；（3）视角插值可以在保持构图约束的前提下进行代数化路径规划。

本文提出的**Toric空间（Toric Space）**正是对这一问题的系统回应。它将Lino & Christie的二维流形推广为一个三维搜索空间，用角度三元组 $(\alpha, \theta, \varphi)$ 参数化相机位置，并在此基础上代数推导出朝向的确定性计算方式。更重要的是，Toric空间使得**构图、距离、屏幕大小、视角角度**等视觉属性可以被表达为该空间中的角度区间或二维子集——这为后续的区间剪枝搜索和屏幕空间操纵器奠定了理论基础。

## 核心创新

### 瓶颈转移：从7-DOF优化到4-DOF确定性求解

传统虚拟相机控制面临的核心瓶颈在于：面向两目标（或更多目标）的视角计算问题通常需要在7自由度（相机位置3维、朝向3维、视场角1维）空间中进行搜索或优化，计算昂贵且缺乏直接操纵视觉属性的直观界面。Toric空间通过将相机位置编码为角度三元组 $(\alpha, \theta, \varphi)$，将搜索空间降至4自由度（三个Toric参数 + 视场角），实现了维度压缩的突破。

这一降维的关键在于Toric空间的定义方式：每个三元组 $(\alpha, \theta, \varphi)$ 唯一确定一个相机位置，且其朝向通过代数三步过程自动计算，确保两目标在屏幕上的指定构图（Section 3.1）。具体而言，朝向计算包括：(i) 基于相机到两目标的平均方向构建look-at四元数；(ii) 计算屏幕定位变换旋转以精确控制目标在屏幕上的投影位置；(iii) 施加横滚角约束。最终朝向由 $q = q_{\psi} \cdot q_{\mathrm{look}} \cdot (q_{\mathrm{trans}})^{-1}$ 组合确定。

### 核心机制：视觉属性的代数表达与区间剪枝

Toric空间的决定性创新在于：将经典视觉属性（构图、距离、大小、视角）直接表达为Toric角度上的区间约束或二维解集，从而将视角计算转化为确定性剪枝问题，而非随机优化。

- **构图约束**：将目标投影限制在屏幕凸区域内的需求，转化为 $\alpha$ 角度的区间 $[\alpha_{\min}, \alpha_{\max}]$，在 $(\theta, \alpha)$ 平面上形成水平条带（Figure 3）。
- **距离约束**：相机到目标的精确距离 $d_A$ 或 $d_B$ 可表达为 $\alpha$ 与 $\theta$ 之间的代数关系（Equation 2, 3），距离区间则对应 $(\theta, \alpha)$ 平面上的二维解集（Figure 4）。
- **大小约束**：通过将目标近似为包围球（半径 $r$），将屏幕投影面积 $s$ 转换为等效距离 $d = r \sqrt{\frac{\pi S_x S_y}{4s}}$，进而复用距离约束的表达（Section 3.3）。
- **视角约束**：视角角 $\beta$ 与Toric角度存在关系 $\theta = 2\beta = 2(\pi - \alpha - \beta')$，视角约束可在 $(\theta, \varphi)$ 平面上表达为二维解集（Figure 6）。

基于这些代数表达，论文提出**渐进式区间剪枝算法**：在 $\varphi$、$\theta$、$\alpha$ 维度上依次采样子集并求交集，采样密度分别为 $d_{\varphi} = 2\sqrt[3]{N/2}$、$d_{\theta} = 4\sqrt[3]{N/2}$、$d_{\alpha} = N$，以在Toric空间内获得均匀分布。该算法在相同计算时间预算下，相比基于粒子群优化的随机搜索方法（Ranon & Urli, IEEE TVCG 2014），满意度提升4个百分点（89% vs 85%），且计算速度提升20-40%（Table 1a）。在精确构图问题上，Toric方法在100ms和200ms搜索预算下均达到100%满意度，而随机方法无法达到（Table 1b）。

### 交互范式革新：屏幕空间视觉属性操纵

传统相机交互（如Autodesk MotionBuilder）依赖平移、旋转、推拉等低层3D变换操作，用户需间接映射操作到视觉结果。Toric空间使**直接操纵视觉属性**成为可能：四种屏幕空间拖拽工具（Figure 7）分别控制目标的屏幕位置、屏幕大小、视角角度和Vertigo效果（视场角变化），同时自动维持其他视觉属性的约束。

这一交互范式的关键在于Toric空间的双向映射能力：用户在屏幕空间的拖拽操作被实时转换为Toric参数更新，而其他约束通过Toric空间的代数结构自动保持。用户评估显示，新手使用Toric操作器完成视角重建任务的平均操作时间显著低于MotionBuilder传统控制（Figure 9），验证了直观性的提升。

### 方法谱系与知识库定位

Toric空间是**Lino & Christie**（SCA 2012）提出的二维Toric流形的三维推广。原Toric流形仅支持两目标的精确屏幕定位（2-DOF流形），Toric空间通过引入 $\varphi$ 角度参数扩展为3-DOF搜索空间，并系统性地将多种视觉属性表达为该空间上的约束，实现了从“精确定位”到“约束满足”的能力跃迁。

在自动视角计算领域，Toric方法相对于**Ranon & Urli**（IEEE TVCG 2014）的粒子群优化方法，核心改变在于：(i) 搜索维度从7-DOF降至4-DOF；(ii) 朝向计算从优化问题变为代数确定；(iii) 搜索算法从随机优化变为确定性区间剪枝。在交互领域，Toric操作器相对于传统3D变换操作，将交互原语从“相机运动”提升为“视觉属性操纵”，降低了认知负荷。

### 局限与待验证方向

Toric空间目前原生仅支持两个目标，多目标场景需通过目标切换或两两组合间接处理。可见性约束（遮挡）未被整合到区间剪枝框架中。用户评估仅与MotionBuilder比较，未与**Gleicher & Witkin**（1992）的Through-The-Lens等经典屏幕空间技术进行定量对比。这些方向仍需进一步验证。

## 整体框架

Toric空间相机控制系统围绕一个核心降维表示构建，将涉及两个目标的虚拟相机问题从传统的7自由度优化空间压缩至4自由度搜索空间。整个pipeline由五个功能模块串联而成，形成“参数化—约束表达—自动求解—交互操纵—轨迹插值”的完整闭环。

**Toric空间参数化**是整个框架的数学基础。给定场景中的两个目标A和B，相机位置被编码为三元组 `(α, θ, φ)`——α控制相机到两目标的夹角（生成相机可定位的流形面），θ定义绕目标的水平角，φ定义垂直角。通过四元数公式 `C = A + (q_φ · q_θ · AB) · sin(α + θ/2)` 可将Toric坐标直接转换为笛卡尔位置，而相机朝向则通过三步代数过程确定：先计算look-at方向四元数，再施加屏幕定位变换，最后叠加横滚角（公式1: `q = q_ψ · q_look · (q_trans)⁻¹`）。这一参数化将搜索维度从7-DOF（位置3+朝向3+视场角1）降至4-DOF（Toric参数3+视场角1）（Section 1）。

**视觉属性表达**模块将用户关心的构图、距离、目标大小、视角等高层需求，翻译为Toric空间中的角度区间或二维解集。例如，屏幕上的构图约束将α限制在 `[α_min, α_max]` 区间内，在 `(θ, α)` 平面上形成水平可解条带（Figure 3）；目标距离约束在 `(θ, α)` 平面上对应由距离边界方程（公式2、3）确定的曲线所围区域（Figure 4）；投影大小通过包围球近似转换为等效距离约束（公式5）；视角约束则在 `(θ, φ)` 平面上产生二维解集（Figure 5、6）。这些代数表达为后续的确定性剪枝提供了精确的可行域描述（Section 3.1–3.4）。

**基于区间的视角求解器**利用上述约束表达，执行确定性搜索而非随机优化。算法沿φ、θ、α维度逐步采样，采样密度递增（`d_φ = 2∛(N/2)`，`d_θ = 4∛(N/2)`，`d_α = N`），在每个维度上求取各属性解集的交集，并加入可见性检查。这种区间剪枝策略使求解器在相同计算时间预算下，比基于粒子群优化的随机方法（Ranon & Urli, IEEE TVCG 2014）获得更高的属性满足率（89% vs. 85%），且计算速度提升20–40%（Table 1, Section 4.1–4.2）。

**屏幕空间操纵器**将Toric空间的代数能力转化为直观的用户交互。系统提供四种拖拽工具：Position操纵器在屏幕上重定位一个目标的同时保持另一目标的屏幕位置；Size操纵器调整目标大小同时保持两者屏幕位置；Vantage操纵器改变围绕目标的视角角度；Vertigo操纵器改变视场角同时精确维持两目标的屏幕位置（Figure 7）。这些操纵器直接在屏幕空间响应拖拽操作，实时更新Toric参数以维持相关约束，使新手用户完成视角重建任务的速度显著快于MotionBuilder的传统平移/旋转/缩放控制（Figure 9, Section 5）。

**视角插值引擎**将上述能力扩展到动态场景。用户只需指定首尾两个关键视角及目标对 `(A,B)` 与 `(A',B')`，系统通过代数插值生成两条分别满足各自构图约束的相机路径，再利用用户控制的非线性时间曲线 `g_p(t)` 和 `g_f(t)` 混合位置与朝向，生成最终平滑轨迹（Figure 10、11）。插值过程完全代数化，计算开销极低——45秒序列仅需91ms，80秒序列需160ms，满足实时性能要求（Section 6）。

**输入输出流**：用户输入包括场景中的目标对、视觉属性约束区间（构图区域、距离范围、目标大小、视角方向与容差）以及可选的关键视角。系统输出为满足所有约束的相机配置（位置、朝向、视场角）或连续相机轨迹，可直接驱动渲染引擎。

**局限性说明**：当前框架原生仅支持最多两个目标，多目标场景需通过切换目标对或提取点对间接处理；未集成可见性约束（遮挡检查仅在求解器中部分实现，操纵与插值过程不检查视线阻挡）；插值方法适用于弧线绕拍等最小化画面变化的运动，无法保持线性推轨路径；目标大小计算依赖包围球近似，无法处理精确物体形状。这些限制在原文中已明确标注，后续研究可沿可见性集成、多目标扩展、直线路径支持等方向推进。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/012_Figure_11.jpg]]
*Figure 11: Overview of the interpolation pipeline, between two key viewpoints. (a)(b) The user drafts two viewpoints at times t0 and t1. (c) (S)he controls interpolation curves over the camera motion and re-framing along time; (s)he is required to handle few controllers, encompassing the duration of enforcement, as well as ease-in/easeout values controlling the speed of the camera. (d) For each key framing, we compute a camera path (τ and τ 0 respectively) that smoothly moves the camera between key positions while enforcing this framing. We finally interpolate both paths (in terms of the camera position and orientation) by relying on the interpolation curves*

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/006_Figure_5.jpg]]
*Figure 5: Computation of the vantage function in the space ( $\beta , \varphi$ ) in the case of an ellipse. The resolution is done through the intersection of the ellipse with a circle of radius r = $\tan ( \beta$ ) . This resolution is similar in case of a parabola or a hyperbola

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/011_Figure_10.jpg]]
*Figure 10: Composition-based interpolation of the camera position around a pair of targets ( A , B ) . For two key camera positions and a key framing to enforce on a pair of targets, we algebraically interpolate the camera position as a path which provides linear changes over their on-screen appearance. The path is defined through a function $F _ { ( A , B ) }$ ( x ) such that any intermediate position ( $\mathrm { i . e . }$ f o r \ x $\in$ ] 0 ; 1 [ ) is computed by relying on a linear interpolation of all visual properties of the pair of targets

## 核心模块与公式推导

### Toric空间参数化

Toric空间将围绕两个目标A、B的相机位置编码为欧拉角三元组 $(\alpha, \theta, \varphi)$（Figure 2）。其中，$\alpha$ 定义相机到两目标的夹角（生成一个可定位相机的流形面），$\theta$ 定义绕目标对的水平角，$\varphi$ 定义垂直角。这一表示将涉及至少两个目标的相机优化问题从7自由度（位置、朝向、视场角）降至4自由度（Toric三元组 + 视场角）。

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/003_Figure_2.jpg]]
*Figure 2: In the Toric space representation, a viewpoint is parametrized with a triplet of Euler angles ( $\alpha , \theta , \varphi$ ) defined around a pair of targets; α defines the angle between the camera and both targets –it generates a manifold surface on which to position the camera–, θ defines an horizontal angle around the targets and $\varphi$ defines a vertical angle around the targets

相机从Toric表示到笛卡尔坐标的转换通过四元数旋转实现：

$$C = A + ( q_{\varphi} \cdot q_{\theta} \cdot AB ) \sin ( \alpha + \theta / 2 )$$

其中 $q_{\varphi}$、$q_{\theta}$ 分别为绕垂直轴和水平轴旋转的四元数，$AB$ 为目标A到B的向量。

### 相机朝向的代数计算

给定Toric位置后，相机朝向通过三步代数过程确定（Section 3.1），无需优化：

**第一步：Look-at朝向。** 计算相机到两目标的平均方向向量 $l$，构建look-at四元数 $q_{\mathrm{look}}$：

$$l = \frac{1}{2} \left[ \frac{CA}{\|CA\|} + \frac{CB}{\|CB\|} \right]$$

**第二步：屏幕定位变换。** 计算变换旋转 $q_{\mathrm{trans}}$，使两目标投影到屏幕上的指定位置。该变换基于屏幕原点方向向量 $p_O^3(0,0,1)$ 与目标投影中点方向向量 $p_M^3(\frac{x_M}{S_x}, \frac{y_M}{S_y}, 1)$（均归一化）之间的旋转。

**第三步：横滚角施加。** 绕视线轴施加横滚角 $\psi$ 的旋转 $q_{\psi}$。

最终相机朝向为三者组合：

$$q = q_{\psi} \cdot q_{\mathrm{look}} \cdot (q_{\mathrm{trans}})^{-1}$$

### 视觉属性的代数表达

Toric空间的核心优势在于可将构图、距离、大小、视角等视觉属性直接表达为角度上的区间或二维子集，用于确定性剪枝。

**构图约束（Section 3.1）：** 将两目标约束在屏幕凸形区域 $s_A$、$s_B$ 内时，$\alpha$ 角被限制在区间 $[\alpha_{\min}, \alpha_{\max}]$ 内，在 $(\theta, \alpha)$ 平面上形成水平条带（Figure 3）。

**距离约束（Section 3.2）：** 约束相机到目标A的精确距离 $d_A$ 时，$\alpha$ 与 $\theta$ 满足：

$$\alpha = \operatorname{acos}\left( \frac{d_A - \|AB\| \cos(\theta/2)}{\sqrt{d_A^2 + \|AB\|^2 - 2 \|AB\| d_A \cos(\theta/2)}} \right)$$

当 $d_B \leq \|AB\|$ 时，相机到目标B的精确距离约束为：

$$\alpha = \frac{\pi}{2} \pm \operatorname{acos}\left[ \frac{\|AB\|}{d_B} \sin\left(\frac{\theta}{2}\right) \right]$$

距离区间约束在 $(\theta, \alpha)$ 平面上对应两条边界曲线之间的白色解集区域（Figure 4）。

**大小约束（Section 3.3）：** 将屏幕投影面积 $s$ 转换为距离约束，需将目标近似为半径 $r$ 的包围球：

$$d = r \sqrt{ \frac{ \pi S_x S_y }{ 4 s } }$$

其中 $S_x$、$S_y$ 为屏幕尺寸。

**视角约束（Section 3.4）：** 视角角 $\beta$ 与Toric角度的关系为 $\theta = 2\beta = 2(\pi - \alpha - \beta')$。通过将视角锥与Toric流形求交，视角约束可表达为 $(\theta, \varphi)$ 平面上的二维解集（Figure 5、Figure 6），其计算涉及椭圆与圆 $r = \tan(\beta)$ 的交点求解。

### 区间剪枝求解器

基于上述代数表达，确定性求解器逐步在 $\varphi$、$\theta$、$\alpha$ 维度上采样子集并求交集，生成满足所有属性的相机配置（Section 4.1）。采样密度按递增分配以保证Toric空间内的均匀分布：

$$d_{\varphi} = 2 \sqrt[3]{N/2}, \quad d_{\theta} = 4 \sqrt[3]{N/2}, \quad d_{\alpha} = N$$

该确定性搜索在相同计算预算下，满意度均值达89%，优于随机粒子群优化方法 **Ranon & Urli**（IEEE TVCG 2014）的85%，且计算时间减少20–40%（Table 1）。

### 屏幕空间操作器

四种屏幕空间拖拽工具直接操纵视觉属性，同时维持其他约束（Figure 7）：

- **Position操作器：** 拖动一个目标的屏幕位置，维持另一目标的屏幕位置。
- **Size操作器：** 缩放一个目标的屏幕大小，维持两目标的屏幕位置。
- **Vantage操作器：** 改变绕一个目标的视角角度，尽可能维持屏幕位置。
- **Vertigo操作器：** 改变视场角，精确维持两目标的屏幕位置。

### 视角插值引擎

插值流水线基于两对目标 $(A,B)$ 和 $(A',B')$ 的视觉属性线性插值生成相机轨迹（Section 6，Figure 10、Figure 11）。在插值比 $x$ 处，针对目标对 $(A,B)$ 的相机位置由平衡两目标插值视觉特征的公式给出：

$$F_{(A,B)}(x) = \frac{1}{2} \left[ A + B + \sum_{i \in \{A,B\}} v_i^x \cdot \frac{d_i^x + d_i^{\alpha,x} \lambda_i^x}{1 + \lambda_i^x} \right]$$

最终相机位置通过非线性时间函数 $g_p(t)$ 混合两条轨迹：

$$p(t) = F_{(A,B)}(g_p(t)) (1 - g_p(t)) + F_{(A',B')}(g_p(t)) g_p(t)$$

相机朝向通过类似混合得到：

$$q(t) = q_{(A,B)} (1 - g_f(t)) + q_{(A',B')} g_f(t)$$

该代数方法在45秒序列（7个关键视角）上总计算时间仅91ms，80秒序列（15个关键视角）上仅160ms，满足实时性能（约2ms/秒，30fps下）。

## 实验与分析

### 自动视角计算：与随机优化方法的定量对比

Toric空间的确定性区间剪枝算法在计算效率与属性满足度上均优于基于随机优化的基准方法。实验采用Ranon & Urli（IEEE TVCG 2014）定义的五个通用视角计算问题，在相同计算时间预算（约5ms）下进行评估。**Table 1(a)** 的结果显示，本方法在5ms搜索时间内达到89%的平均属性满足度，而Ranon & Urli的粒子群优化方法为85%，同时本方法的计算时间减少约20–40%。这一优势源于Toric空间将搜索维度从7-DOF降至4-DOF，并通过代数化的视觉属性区间表达直接剪枝不可行区域，避免了随机搜索的采样浪费。

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/007_Table_1.jpg]]
*Table 1: Comparison of our technique with Ranon and Urli in measuring time and satisfaction of visual properties: (a) average values for five viewpoint computation problems defined by Ranon and Urli (b) average values for a single viewpoint computation problem with a precise framing property (see Section 4.2)*

在精确构图问题的极端测试中，差距更为显著。**Table 1(b)** 展示了一个要求两个目标精确落在指定屏幕区域内的严格构图任务：本方法在100ms和200ms的搜索预算下均达到100%满足度，而Ranon & Urli的方法始终无法达到完全满足。这验证了区间剪枝的确定性优势——当解集非空时，算法能够精确捕获所有可行配置；随机搜索则可能在复杂约束下遗漏可行解。

需要指出，此对比基于统一的视觉属性定义和满意度评估指标（均来自Ranon & Urli 2014），且Toric方法使用代数计算朝向，而基准方法进行朝向优化。对比的公允性在于两者在相同计算时间预算下运行，Toric的确定性剪枝与基准的随机粒子群优化形成清晰对照。

### 屏幕空间操作器的用户评估

为评估Toric空间屏幕操作器的直观性和效率，研究开展了一项用户实验，要求参与者重现给定的参考视角。实验将四类Toric操作器（位置、大小、视角、Vertigo）与Autodesk MotionBuilder的传统平移/旋转/缩放控制进行对比，参与者分为新手和MotionBuilder专家两组。

**Figure 9** 的柱状图显示，新手用户使用Toric操作器完成视角重建任务的平均操作时间显著低于使用MotionBuilder传统控制。**Figure 8** 进一步展示了操作过程中用户视角与参考视角的距离演变曲线：使用传统控制时（红色曲线），用户视角在较长时间内保持较大偏差，而Toric操作器（蓝色曲线）能更快收敛至目标视角。这一差异的核心机制在于，Toric操作器直接在屏幕空间操纵视觉属性（如目标位置、大小、视角），用户无需在3D空间中反复调整相机位置和朝向；操作器内部通过Toric空间参数化实时更新相机配置，同时自动维持其他约束。

需要注意的是，该用户评估存在以下局限：专家参与者样本量较小，且仅与MotionBuilder的传统控制进行了对比，未与其他高级屏幕空间技术（如Gleicher & Witkin 1992的Through-The-Lens方法）进行定量比较。因此，Toric操作器相对于更先进交互技术的优势仍需进一步验证。

### 视角插值的实时性能

视角插值引擎的计算效率满足实时应用需求。实验测试了包含7个关键视角（生成45秒序列）和15个关键视角（生成80秒序列）的两条相机轨迹：总计算时间分别为91ms和160ms，相当于每帧（30fps）约2ms的计算开销。这一效率得益于插值方法的纯代数特性——相机位置和朝向通过解析公式直接计算，无需逐帧优化或搜索。插值过程通过非线性时间函数混合两条基于不同目标对的轨迹，在维持画面构图约束的同时生成平滑运动。

### 方法的失败模式与适用边界

尽管Toric空间在效率和直观性上展现出优势，实验和分析揭示了若干明确的失败模式：

1. **可见性缺失**：自动视角求解和插值过程中均未检查视线遮挡。当目标被场景几何体遮挡时，算法仍可能返回不可行的相机配置，需要用户手动调整或后续处理。

2. **多目标限制**：屏幕操作器和视角计算原生仅支持两个目标。虽然可通过切换目标对或提取点的方式间接处理更多目标，但缺乏原生的三目标及以上支持，这在需要同时关注多个角色的场景中构成瓶颈。

3. **路径类型约束**：插值方法适用于最小化画面布局变化的运动（如弧线绕拍、跟拍），但无法保持线性路径（如推轨镜头）。这是因为插值公式基于视觉属性的线性变化，而非相机在笛卡尔空间中的直线运动。

4. **目标几何近似**：距离和大小约束依赖将目标近似为包围球，忽略了实际物体形状。对于细长或复杂形状的目标，投影面积与距离的关系可能产生偏差。

5. **评估覆盖不足**：用户实验仅与MotionBuilder对比，未涉及更广泛的交互技术（如Through-The-Lens、3D widgets等），且专家样本量小，限制了结论的泛化性。

这些失败模式指向了Toric空间的适用边界：在需要精确可见性保证、线性相机路径、或同时处理三个以上目标的场景中，当前方法需要补充机制或与其它技术结合使用。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/004_Figure_4.jpg]]
*Figure 4: Solution sets (in white) corresponding to all camera positions within a range of distances to targets A and B. (a) Solution pairs ( $\alpha , \theta$ ) for a distance to A within [5, 10]; each red curve corresponds to a bounding value of the interval of distance. (b) Solution pairs (α, θ) for a distance to B within [4, 8]; each green curve corresponds to a bounding value of the interval of distance

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/005_Figure_6.jpg]]
*Figure 6: Solution range of a vantage angle, for a given view d i - rection (vantage vector) and an accepted angular deviation $\gamma$ . In these examples, the angle between the line (AB) and the vantage vector is ${ \frac { \pi } { 4 } }$ . . In each case, the white area represents the set of pairs ( $\theta , \varphi$ ) satisfying the vantage angle constraint

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/008_Figure.jpg]]
*Figure: (a) Position manipulator (b) Size manipulator (c) Vantage manipulator (d) Vertigo manipulator*

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/009_Figure_7.jpg]]
*Figure 7: Our screen-space manipulators. (a) the Position manipulator enables repositioning one target on the screen while the other target’s on-screen position is maintained; (b) the Size manipulator enables resizing one target while both targets’ on-screen positions are maintained; (c) the Vantage manipulator enables changing the view angle around one target, while targets’ on-screen positions are maintained as much as possible; (d) the Vertigo manipulator enables changing the camera’s field of view while both targets’ on-screen positions are exactly maintained. (a) Novice user of 3D modelers*

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/002_Figure_3.jpg]]
*Figure 3: Constraining the projection of targets A and B in onscreen convex shapes s A and sB reduces the domain of variable α in the Toric space. The set of cameras which satisfy the framing constraint (white area) is then given by a horizontal strip $\alpha \in [ \alpha _ { \operatorname* { m i n } } , \alpha _ { \operatorname* { m a x } }$ ] in the plane ( $\theta , \alpha$ )

![[assets/figures/papers/paper_list_l10_https_doi_org_10_1145_2766965/figures/010_Figure_8.jpg]]
*Figure 8: Evolution of the distance from the user’s manipulated viewpoint to a reference viewpoint, for a novice user and an expert user of MotionBuilder (both displayed in red). The distance obtained using our tool is displayed in blue. The manipulation time is in seconds. Figure 9: Mean manipulation time (in seconds) required by the participants to reproduce a viewpoint using our manipulators (blue) compared to using the classical interaction of MotionBuilder (red)*

## 方法谱系与知识库定位

### 1. 方法溯源与核心突破

Toric 空间相机控制方法直接继承自 **Lino & Christie**（SCA 2012）提出的 Toric 流形（Toric manifold）。该前身工作首次将两目标精确屏幕定位问题表达为一个二维流形上的搜索，但仅限于相机位置的两个自由度，无法同时处理距离、大小、视角等多重视觉属性约束。本工作将这一表示推广为三维搜索空间 $(\alpha, \theta, \varphi)$，并系统性地建立了一套视觉属性到 Toric 角度的代数映射机制，使搜索维度从传统的 7-DOF（位置 3 + 朝向 3 + 视场角 1）降至 4-DOF（Toric 三元组 + 视场角），这是该方法在计算效率上的根本性突破。

与自动视角计算领域的代表性基线 **Ranon & Urli**（IEEE TVCG 2014）相比，本方法在求解范式上实现了从随机搜索到确定性剪枝的转变。Ranon & Urli 采用粒子群优化在 7-DOF 空间中随机采样并评估满意度，其收敛速度和最优性受限于随机搜索的固有不确定性。Toric 方法则将视觉属性（构图、距离、大小、视角）直接表达为 Toric 角度上的区间约束或二维解集，通过逐步在 $\varphi$、$\theta$、$\alpha$ 维度上采样子集并求交集，实现确定性剪枝。在相同的五个基准问题上，Toric 方法在约 5ms 搜索时间预算下达到 89% 的平均满意度，优于 Ranon & Urli 的 85%，且计算时间减少约 20-40%（Table 1(a)）。在精确构图问题上，Toric 方法在 100ms 和 200ms 预算下均达到 100% 满意度，而 Ranon & Urli 无法达到该水平（Table 1(b)）。

在交互范式层面，本方法区别于 **Autodesk MotionBuilder** 等商业工具采用的传统直接相机变换（平移、旋转、缩放）。MotionBuilder 要求用户在三维空间中操作相机本身，而 Toric 屏幕空间操作器允许用户直接在屏幕空间拖拽目标的位置、大小、视角和视场角，系统在后台实时求解 Toric 参数以维持其他视觉属性的约束。用户研究表明，新手使用 Toric 操作器完成视角重建任务的平均操作时间显著低于使用 MotionBuilder 传统控制（Figure 9）。

### 2. 技术模块与关键公式

**Toric 空间参数化** 是整套方法的几何基础。相机位置 $C$ 通过 Toric 角度三元组 $(\alpha, \theta, \varphi)$ 和两目标 $A, B$ 表达为：
$$C = A + ( q_{\varphi} \cdot q_{\theta} \cdot AB ) \sin ( \alpha + \theta / 2 )$$
其中 $q_{\varphi}$ 和 $q_{\theta}$ 分别为绕 $AB$ 轴的垂直和水平旋转四元数，$\alpha$ 控制相机到两目标的夹角。

**相机朝向计算** 采用三步代数过程（Section 3.1）：
1. 计算 look-at 四元数 $q_{\text{look}}$，其视线方向为相机到两目标的平均方向：
   $$l = \frac{1}{2} \left[ \frac{CA}{\|CA\|} + \frac{CB}{\|CB\|} \right]$$
2. 计算变换旋转 $q_{\text{trans}}$，将屏幕原点与目标投影中点对齐到期望位置。
3. 组合横滚角 $q_{\psi}$ 得到最终朝向：
   $$q = q_{\psi} \cdot q_{\text{look}} \cdot (q_{\text{trans}})^{-1}$$

**视觉属性代数化** 是实现确定性剪枝的关键：
- **构图约束**：将目标投影限制在屏幕上的凸区域，将 $\alpha$ 的可行域缩减为区间 $[\alpha_{\min}, \alpha_{\max}]$，在 $(\theta, \alpha)$ 平面上形成水平条带（Figure 3）。
- **距离约束**：相机到目标 $A$ 的精确距离 $d_A$ 与 Toric 角度的关系为：
  $$\alpha = \operatorname{acos}\left( \frac{d_A - \|AB\| \cos(\theta/2)}{\sqrt{d_A^2 + \|AB\|^2 - 2 \|AB\| d_A \cos(\theta/2)}} \right)$$
  到目标 $B$ 的距离约束在 $d_B \leq \|AB\|$ 时有解析形式（Equation 3），这些方程在 $(\theta, \alpha)$ 平面上定义曲线边界（Figure 4）。
- **大小约束**：通过包围球近似将屏幕投影面积 $s$ 转换为距离 $d$：
  $$d = r \sqrt{ \frac{ \pi S_x S_y }{ 4 s } }$$
  其中 $r$ 为包围球半径，$S_x, S_y$ 为屏幕尺寸。
- **视角约束**：视角角 $\beta$ 与 Toric 角度的关系为 $\theta = 2\beta = 2(\pi - \alpha - \beta')$，其解集在 $(\theta, \varphi)$ 平面上形成二维区域（Figure 6），通过求交椭圆与圆来计算（Figure 5）。

**区间剪枝求解器** 采用渐进采样密度分配：
$$d_{\varphi} = 2 \sqrt[3]{N/2}, \quad d_{\theta} = 4 \sqrt[3]{N/2}, \quad d_{\alpha} = N$$
在 $\varphi$、$\theta$、$\alpha$ 维度上依次采样子集并求交集，最终生成满足所有属性的相机配置。

### 3. 适用边界与局限

**目标数量限制**：该方法原生仅支持最多两个目标。虽然可以通过切换目标对或提取目标上两点来处理更多目标，但缺乏原生的多目标（≥3）支持框架。这一限制源于 Toric 空间的几何定义依赖于两目标构成的基线 $AB$。

**可见性缺失**：整个方法体系未集成目标可见性约束（遮挡处理）。在自动视角计算、屏幕空间操作和插值过程中，均不检查视线是否被场景几何体阻挡。这是该方法在真实三维场景应用中的主要短板。

**目标形状近似**：大小和距离计算依赖将目标近似为包围球，无法处理精确的物体形状。这可能导致对非球形物体的屏幕投影面积估计不准确。

**运动路径类型受限**：插值方法适用于最小化画面布局变化的运动（如弧线绕拍、跟拍），但无法保持线性路径（如推轨镜头）。这是因为 Toric 空间本质上描述的是围绕目标对的球面运动。

**用户评估局限性**：用户研究仅与 MotionBuilder 比较操作效率，样本量较小（Figure 9），且未与其他高级屏幕空间技术（如 Gleicher & Witkin 1992 的 Through-The-Lens 技术）进行定量对比。专家用户样本尤其不足，限制了结论的普适性。

### 4. 开放问题

1. **可见性约束集成**：如何高效地在 Toric 空间中表达并整合可见性约束？可能的方向包括预计算可见性图或利用硬件遮挡查询进行实时检查，但如何将这些信息映射到 Toric 角度的区间表示上仍需探索。

2. **多目标扩展**：能否将 Toric 空间概念形式化地扩展至三个或更多目标，而不仅仅是通过两两组合的增量式处理？这可能需要定义更高维度的流形或采用层次化目标分组策略。

3. **线性路径保持**：能否在 Toric 空间中表达需要保持直线路径的相机运动（如 dolly 横移）？这可能需要放松 Toric 空间的某些几何约束，或引入混合表示。

4. **单目标形式化**：论文提到可通过选取目标上两点来处理单目标情况，但该方法的精度和适用条件尚未形式化评估。

5. **与其他屏幕空间技术的定量比较**：Toric 屏幕操作器与经典的 Through-The-Lens（Gleicher & Witkin 1992）等基于屏幕的相机控制技术在精度和易用性上的定量比较仍有待开展。

6. **动态场景扩展**：区间剪枝算法能否扩展到包含动态目标（移动角色）的场景，以实现实时相机规划？这需要处理目标运动导致的 Toric 空间约束动态变化问题。

## 原文 PDF

![[paperPDFs/TOG_2015/Intuitive_and_Efficient_Camera_Control_with_the_Toric_Space.pdf]]

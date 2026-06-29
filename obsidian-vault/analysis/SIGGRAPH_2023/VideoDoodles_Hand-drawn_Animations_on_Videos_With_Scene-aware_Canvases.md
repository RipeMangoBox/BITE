---
title: "VideoDoodles: Hand-drawn Animations on Videos With Scene-aware Canvases"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/VideoDoodles_Hand_drawn_Animations_on_Videos_With_Scene_aware_Canvases.pdf
project_link: null
code_link: null
aliases:
- VideoDoodles
tags:
- SIGGRAPH_2023
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 预先计算相机位姿、深度图和光流以重建3D场景，将涂鸦嵌入平面3D画布，并用关键帧引导的3D跟踪算法自动计算画布位置与朝向。
primary_logic: 将2D绘画与3D场景效果解耦：用户在正视画布上创作，系统利用3D信息自动处理透视和遮挡，并通过泊松积分稳定轨迹、优化朝向以跟随运动方向。
claims:
- 在TAP-Vid DAVIS基准上，单关键帧条件下我们的方法在Avg Jaccard (40.8% vs 37.2%) 和 <δ_avg^x (59.2% vs 52.7%) 上超越TAP-Net，增加第二个关键帧后进一步提升至45.5%和67.3%。
- 七名用户（含两名专家）完成任务1平均用时10分30秒，从零开始任务2平均14分钟，满意度评分4.7/5。
- 参与者约49%的时间用于绘画而非技术操作，显示自动化跟踪和3D渲染有效节省了机械操作时间。
- 消融实验表明泊松积分对跟踪精度至关重要：去除后Avg Jaccard从40.8%骤降至18.3%。
---

# VideoDoodles: Hand-drawn Animations on Videos With Scene-aware Canvases

> [!tip] 核心洞察
> 将2D绘画与3D场景效果解耦：用户在正视画布上创作，系统利用3D信息自动处理透视和遮挡，并通过泊松积分稳定轨迹、优化朝向以跟随运动方向。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoDoodles: 视频上的场景感知手绘动画 |
| 英文题名 | VideoDoodles: Hand-drawn Animations on Videos With Scene-aware Canvases |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://em-yu.github.io/research/videodoodles/) |
| Topic | #topic/graphics_animation_interaction #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VideoDoodles |
| Dataset | TAP-Vid DAVIS |

> [!tip] 效果简介
> - TAP-Vid DAVIS (24 videos subset) 上，Average Jaccard (AJ) 40.8% (Ours 1kf, strided) vs 37.2% (TAP-Net) (+3.6%)。
> - TAP-Vid DAVIS 上，<δ_avg^x 59.2% (Ours 1kf, strided) vs 52.7% (TAP-Net) (+6.5%)；Occlusion Accuracy (OA) 80.6% (Ours 1kf, strided) vs 81.2% (TAP-Net) (-0.6%)。

## 概要

**问题瓶颈：** 手动在视频上创作手绘动画（Video Doodles）需要逐帧绘制并人工处理透视变形、遮挡和运动同步，极为耗时且难以使涂鸦在三维场景中显得真实。

**核心方法：** 本文提出 VideoDoodles 交互系统，将二维涂鸦嵌入平面三维画布，锚定于三维场景点。系统预先计算相机位姿、深度图和光流以重建三维场景，用户仅需在少数关键帧中放置画布，系统即通过关键帧引导的三维跟踪算法（最短路径图搜索 + 泊松积分轨迹优化）自动计算画布的三维位置与朝向，并利用深度信息自动渲染透视和遮挡效果。用户在一个正视校正的二维绘画面板上创作，无需手动处理三维复杂性。

**主要结果：** 在 TAP-Vid DAVIS 基准上，单关键帧条件下 Average Jaccard 达 40.8%（超越 TAP-Net 的 37.2%），位置精度 <δ_avg^x 达 59.2%（vs. 52.7%）；增添第二个关键帧后进一步提升至 45.5% 和 67.3%。消融实验证实泊松积分对跟踪精度起决定性作用——去除后 AJ 骤降至 18.3%。用户研究（n=7）显示参与者平均 10 分 30 秒完成引导任务，约 49% 时间用于绘画而非技术操作，满意度评分 4.7/5。

**方法定位：** 本工作将二维视频涂鸦创作提升为三维场景感知的交互范式，其核心贡献在于将关键帧引导的三维点跟踪与画布朝向优化相结合，使非专业用户也能高效创作具有正确透视和遮挡效果的手绘动画。方法受限于平面画布假设，无法处理物体自转等复合运动，且依赖深度估计精度。

## 核心方法与创新机理

VideoDoodles 的核心问题是如何让用户在视频中手绘动画时，无需逐帧手动处理透视变形、遮挡关系和运动同步。系统通过将 2D 绘画操作与 3D 场景效果解耦来实现这一目标：用户在正视画布上创作，系统利用预计算的 3D 场景信息自动处理所有几何效果。其方法链由五个关键模块构成，形成从场景重建到最终渲染的完整管线。

### 3D 场景重建预处理

系统首先对输入视频进行密集的几何重建。采用 Schönberger 和 Frahm (2016) 的方法估计每帧相机位姿，使用 Teed 和 Deng (2020) 的 RAFT 模型计算稠密光流，并通过单目深度估计网络（如 MiDaS）获取每帧深度图。这些预处理步骤将 2D 视频转换为 RGBD 序列，为后续所有 3D 操作提供几何基础。具体而言，对于第 $t$ 帧中的像素 $p_i^t$，系统利用相机内参矩阵和深度图将其反投影到 3D 空间位置 $P_i^t$；同时将 2D 光流向量 $v_i^t$ 提升为 3D 场景流向量 $V_i^t$，表示该像素在 3D 空间中的帧间运动。这一预处理模块是整个方法的基础，其质量直接影响后续跟踪和遮挡处理的精度。

### 关键帧引导的 3D 轨迹跟踪

动态画布的核心挑战在于如何让画布跟随场景中的移动物体。VideoDoodles 引入了一种新颖的 3D 点跟踪算法，仅需用户在一个或多个关键帧中指定画布位置，即可自动推断完整的 3D 运动轨迹。该算法分两步执行：

**第一步：图构建与最短路径初始轨迹。** 系统构建一个有向图，其中节点为视频中经过外观筛选的像素。为降低计算复杂度，算法保留每帧中与关键帧在外观上最相似的 10% 像素（基于深层视觉特征相似度）。图的边连接连续帧间可能对应的像素，其权重定义为 3D 场景流预测位置与实际位置的差异：

$$w(p_i^t, p_j^{t+1}) = \left\| (P_j^{t+1} - P_i^t) - V_i^t \right\|^2$$

该权重衡量了“从 $P_i^t$ 出发，按照场景流 $V_i^t$ 移动后到达的位置”与候选像素 $P_j^{t+1}$ 之间的 3D 距离。通过在图中运行 Dijkstra 最短路径算法，系统获得连接所有关键帧的初始 3D 轨迹。然而，由于遮挡、纹理缺失以及低分辨率图结构的影响，这条初始轨迹通常存在明显的抖动和漂移（Fig. 4b, Fig. 5b 红线）。

**第二步：泊松积分轨迹优化。** 这是本方法的关键创新点。系统沿初始轨迹在原始分辨率上采样场景流向量，并将轨迹优化建模为一个带约束的最小二乘问题：

$$\min_{\mathbf{P}} \sum_t \left\| (P^{t+1} - P^t) - V^t \right\|^2 + \lambda_{\mathrm{depth}} \sum_k \left\| \tilde{P}^k - P^k \right\|^2 \quad \text{s.t.} \ \tilde{\mathbf{p}}^k = \Pi^k(P^k)$$

该目标函数包含两项：第一项最小化轨迹的帧间差分与场景流之间的偏差，即要求轨迹的运动与场景实际运动一致；第二项为深度约束项，要求优化后的轨迹点在重投影后与用户在关键帧中指定的像素位置 $\tilde{\mathbf{p}}^k$ 保持一致。$\lambda_{\mathrm{depth}}$ 平衡运动平滑性与关键帧约束的严格性。

这一优化的核心洞见在于：即使初始轨迹因遮挡而漂移到错误位置（如跟踪物体被前景遮挡时），只要被跟踪物体整体进行相同的平移运动，采样到的场景流向量仍然反映正确的运动方向。通过积分这些场景流向量，泊松优化能够消除遮挡引起的漂移，产生一条平滑且物理正确的 3D 轨迹（Fig. 4c, Fig. 5b 浅蓝线）。该模块的计算效率较高：对于 80 帧、1200×674 分辨率的视频，图构建和最短路径计算约需 3 秒（在 2.4GHz Intel i5 MacBook Pro 上）。

### 画布朝向优化

仅跟踪位置不足以使画布在 3D 场景中显得自然——画布的朝向必须与物体运动方向保持一致。VideoDoodles 将朝向跟踪建模为 SO(3) 上的优化问题。设 $R^t$ 为第 $t$ 帧画布的 3D 旋转矩阵，$\bar{V}^t$ 为轨迹的切线方向（运动方向），$R^\star$ 为用户指定的相对旋转矩阵（允许画布法线不与运动方向完全对齐）：

$$\min_{\{R^t, R^\star\}} \sum_t \| (R^t R^\star) |_X - \bar{V}^t \|^2 + \lambda_{\mathrm{smooth}} \sum_t \| R^{t+1} - R^t \|^2$$

其中 $(R^t R^\star) |_X$ 表示经相对旋转修正后的画布 X 轴方向。目标函数第一项要求画布的指定轴与轨迹切线方向对齐，第二项为时序平滑项，防止朝向突变。$R^\star$ 允许用户在一个关键帧中设定画布相对于运动方向的偏转角度，系统自动在所有帧中保持这一相对关系。Fig. 6 展示了这一优化的效果：当轨迹转弯时，固定朝向的画布会产生不自然的旋转（Fig. 6b），而优化后的朝向使画布始终与轨迹方向保持合理的关系（Fig. 6c）。该优化计算效率较高：80 帧的单段轨迹优化约需 1.5 秒。

### 2D 绘画面板与渲染

用户界面模块将 3D 跟踪的复杂性完全隐藏。用户在正视画布上进行 2D 绘画，系统将画布校正为正面平行视图（fronto-parallel），消除透视变形对绘画的干扰。画布上同时显示校正后的视频底图作为参考。用户可以在不同关键帧上绘制不同的内容，系统自动在关键帧之间进行插值，实现逐帧动画效果。

渲染模块利用预计算的相机位姿和深度图，将画布上的涂鸦内容投影回视频画面。通过深度测试，系统自动处理涂鸦与真实场景物体之间的遮挡关系：当画布上的某个像素在场景深度图对应位置的深度值大于画布深度时，该像素被遮挡。这一机制使得涂鸦能够自然地出现在场景物体后方（如 Fig. 2 中画布被身体和柱子遮挡）。

![[assets/figures/papers/paper_list_l11_https_em_yu_github_io_research_videodoodles/figures/002_Figure_2.jpg]]
*Figure 2: At the core of our interactive system is a novel tracking algorithm that deduces the 3D position and orientation of a planar canvas over an RGBD video given a few keyframes (green denotes a position keyframe, red denotes a position and orientation keyframe). Note how the canvas rotates to align with the direction of the trajectory and gets occluded by the body and the poles. Users create scene-aware doodles by drawing over the canvas in a simple 2D interface*

### 创新机理总结

VideoDoodles 相对于传统 2D 视频涂鸦方法的关键改变体现在三个维度：

1. **画布与场景交互**：从无透视/遮挡处理的 2D 叠加转变为锚定于 3D 场景点的平面画布，自动渲染透视和遮挡效果。这一改变使得涂鸦能够与 3D 场景产生真实的几何交互。

2. **运动跟踪**：从手动关键帧或易漂移的 2D 点跟踪转变为关键帧引导的 3D 轨迹优化。最短路径提供初始估计，泊松积分利用场景流消除遮挡漂移，两者协同实现了鲁棒的 3D 跟踪。

3. **画布朝向**：从固定朝向或手动调整转变为基于轨迹切线方向的自动优化，并支持用户通过相对旋转关键帧进行灵活控制。

这三个模块之间存在紧密的因果关系：3D 重建为跟踪提供场景流和深度信息；跟踪算法输出的 3D 轨迹为朝向优化提供运动方向和关键帧约束；朝向优化结果与轨迹共同定义画布在每帧的完整 3D 刚体变换；最终渲染模块利用这一变换和深度图实现透视投影和遮挡处理。整个管线将用户从繁琐的逐帧技术操作中解放出来，使其能够专注于绘画创作本身。

![[assets/figures/papers/paper_list_l11_https_em_yu_github_io_research_videodoodles/figures/004_Figure_4.jpg]]
*Figure 4: Schematic illustration of our tracking algorithm. We extract an initial trajectory as the least-cost path in the directed graph connecting each keyframed pixel to similar pixels in consecutive frames (a). This trajectory often jitters over the object to track due to occlusions, lack of visual features, and our use of a low-resolution graph (b). We recover a stable trajectory by integrating the scene flow sampled along the initial trajectory at full resolution (c, red arrows)*

![[assets/figures/papers/paper_list_l11_https_em_yu_github_io_research_videodoodles/figures/001_Figure_1.jpg]]
*Figure 1: Video doodles combine hand-drawn animations with video footage. Our interactive system eases the creation of this mixed media art by letting users place planar canvases in the scene which are then tracked in 3D. In this example, the inserted rainbow bridge exhibits correct perspective and occlusions, and the character’s face and arms follow the tram as it runs towards the camera*

![[assets/figures/papers/paper_list_l11_https_em_yu_github_io_research_videodoodles/figures/015_Figure_11.jpg]]
*Figure 11: Video doodles created with our system by participants of our user study. Participants created static doodles (text in P1 - hike, finishing line in P7 - motorbike race) as well as dynamic doodles (P3 - angel & devil child, P5 - squirrel friend). Several of these doodles get occluded by real objects (poles in P4 - car race, face on the tree in P5 - squirrel friend), and are synchronized with specific video events (yellow sparkles when P2’s dancer touches the ground, water splash when P6’s horse ends its jump*

## 实验与关键发现

VideoDoodles 的实验评估围绕三个层面展开：跟踪算法的定量基准测试、系统组件的消融验证，以及用户工作流的定性研究。由于该系统本质上是一个交互式创作工具而非全自动算法，评估策略兼顾了客观数值指标与主观用户体验，以此全面衡量方法在真实场景中的可用性。

### 跟踪精度：TAP-Vid DAVIS 基准对比

作者在 TAP-Vid DAVIS 基准的 24 个视频子集上对跟踪算法进行了定量评估，与同期工作 **TAP-Net**（Doersch et al., 2022）进行对比。需要指出的是，3D 重建仅在 DAVIS 的 30 个视频中的 24 个上成功完成，这一预处理瓶颈可能引入选择偏差，但论文未对此进行深入讨论。

Table 1 报告了单关键帧条件下的核心结果（`Ours (1kf, strided)` 行）。在平均 Jaccard（Average Jaccard, AJ）指标上，VideoDoodles 达到 40.8%，相较 TAP-Net 的 37.2% 提升 **+3.6 个百分点**；在 `<δ_avg^x` 指标（衡量位置精度）上达到 59.2%，相较 TAP-Net 的 52.7% 提升 **+6.5 个百分点**。这两个指标的提升表明，VideoDoodles 的 3D 轨迹在空间定位上更为精确。然而，在遮挡准确率（Occlusion Accuracy, OA）上，VideoDoodles 为 80.6%，略低于 TAP-Net 的 81.2%（差距 -0.6%），说明两者在遮挡判断能力上基本持平。

![[assets/figures/papers/paper_list_l11_https_em_yu_github_io_research_videodoodles/figures/011_Table_1.jpg]]
*Table 1: Evaluation of our tracking algorithm on 24 videos of the TAP-Vid DAVIS benchmark with a single keyframe (1kf ). Adding an extra keyframe (2kf ) yields a significant improvement in all metrics (higher is better). We report the results of TAP-Net [Doersch et al. 2022] computed on the 24- videos subset for which we obtained a successful 3D reconstruction*

当用户增加第二个关键帧后（`Ours (2kf)` 行），性能获得显著跃升：AJ 从 40.8% 提升至 45.5%，`<δ_avg^x` 从 59.2% 提升至 67.3%。这一结果直接验证了“关键帧引导”这一核心交互范式的有效性——用户仅需额外标注一帧，系统即可利用新增约束大幅改善轨迹质量。Fig. 7 提供了可视化对比：VideoDoodles 的轨迹在平滑性和精确性上均优于 TAP-Net，但在物体发生复杂自转运动时（如汽车轮毂旋转），两种方法都表现出明显的跟踪困难。

### 消融实验：泊松积分的决定性作用

消融实验揭示了泊松积分（Poisson integration）模块对系统性能的关键支撑。去除该模块后（Table 1 中 `w/o Poisson` 行），AJ 从 40.8% **骤降至 18.3%**，`<δ_avg^x` 从 59.2% 降至 31.6%，降幅分别达到 22.5 和 27.6 个百分点。这一断崖式下跌表明，单纯依赖最短路径图搜索得到的初始轨迹在遮挡区域极易漂移，而泊松积分通过在全分辨率下采样场景流并最小化轨迹导数与场景流的偏差，有效消除了遮挡引起的累积误差。

Fig. 5 以自行车被前景植物遮挡的案例直观展示了这一机制：最短路径轨迹（红色）在遮挡发生时漂移到植物上，而泊松积分后的轨迹（浅蓝色）则稳定地保持在自行车位置上，即使自行车完全被遮挡也能依据场景流推断出正确的运动路径。这一机制的核心在于利用了“遮挡物与被遮挡物经历不同运动”这一物理约束——植物静止而自行车平移，场景流在遮挡边界处提供了区分信号。

### 朝向优化的定性验证

画布朝向优化没有定量指标，但 Fig. 6 提供了关键的定性消融证据。当用户在单关键帧中将画布设置为垂直于运动方向后，若保持画布朝向在场景空间中固定不变（`constant orientation` 条件），当轨迹转弯时画布会与运动方向产生明显偏离，视觉效果不自然。而经过朝向优化后，画布自动旋转以保持与轨迹切线方向的对齐关系，使涂鸦始终“面朝”运动方向。这一效果对于火车转弯、车辆变道等场景尤为关键，直接决定了涂鸦在 3D 场景中的视觉可信度。

![[assets/figures/papers/paper_list_l11_https_em_yu_github_io_research_videodoodles/figures/007_Figure_6.jpg]]
*Figure 6: In this example, the user orients the canvas to be perpendicular to the motion trajectory in one keyframe (a). Keeping this orientation constant in scene space produces an implausible result as the trajectory turns to follow the tracks (b). Our optimization rotates the canvas to preserve its orientation relative to the trajectory (c)*

### 用户研究：效率与满意度

七名参与者（含两名专业艺术家）的用户研究提供了系统可用性的实证支撑。参与者完成两项任务：任务 1 为在预定义关键帧上创作涂鸦，平均用时 **10 分 30 秒**；任务 2 为从零开始完整创作，平均用时 **14 分钟**。满意度评分达到 **4.7/5**，表明系统在降低创作门槛方面取得了显著成效。

Fig. 8 的操作时间线可视化揭示了一个关键发现：参与者约 **49% 的时间用于实际绘画**，而非技术操作（如放置关键帧、调整画布）。这一比例在视频涂鸦创作中具有重要意义——在传统逐帧手绘流程中，机械操作（处理透视、遮挡、运动同步）会占据绝大部分时间。VideoDoodles 将技术负担压缩到约一半时间，使用户能将精力集中在创意表达上。时间线还显示，参与者经常在关键帧设置与绘画之间交替切换（如 P4），说明系统支持迭代式创作，而非强制要求先完成所有技术设置。

### 失败模式与适用边界

论文坦率地展示了系统的多个失败模式，这些限制定义了 VideoDoodles 的适用边界。

**物体自转跟踪失败**（Fig. 9）：跟踪算法假设被跟踪物体朝向其主导运动方向，当物体发生显著自转时（如舞者旋转跳跃），单关键帧条件下系统仅能跟踪身体的上移运动，无法捕捉旋转。用户需手动添加朝向关键帧来修正，这暴露了算法在旋转自由度上的根本局限——系统跟踪的是点的 3D 平移，而非物体的完整 6-DoF 姿态。

**严重透视收缩下的背景失真**（Fig. 10a）：绘画面板将画布校正为正视视角以方便绘画，但当画布在相机视角中严重透视收缩时，校正后的视频底图会出现强烈的拉伸失真，使绘画参考失去意义。这是平面画布表示的结构性限制，在极端视角下无法规避。

**深度估计错误导致的错误遮挡**（Fig. 10b）：系统依赖预计算的深度图来处理遮挡关系。当深度估计算法在遮挡物轮廓附近产生错误时（如舞者手臂周围的小区域），会导致涂鸦被错误地遮挡或穿透前景物体。这一问题在细薄结构（如手指、头发）附近尤为突出，因为深度估计算法在这些区域的不确定性最高。

**细薄物体跟踪丢失**（Fig. 7 底行）：当被跟踪物体过细或缺乏纹理特征时，即使增加关键帧，算法也可能完全丢失跟踪目标。Fig. 7 底部展示了汽车轮毂旋转的案例，VideoDoodles 和 TAP-Net 均无法可靠跟踪这种复合微运动。

这些失败模式共同划定了系统的有效工作域：VideoDoodles 最适合跟踪具有清晰平移运动、适中尺寸和丰富纹理的物体，在遮挡不严重、视角变化平缓的场景中表现最佳。对于自转主导的运动、极端透视视角和细薄结构，用户需要预期额外的手动干预或接受效果折损。

## 定位与知识库关联

VideoDoodles 解决的核心问题是 **2D 手绘动画与 3D 视频场景的感知一致性**。传统视频涂鸦工具将绘画视为 2D 图像平面上的叠加层，用户必须逐帧手动修正透视变形和遮挡关系，创作成本极高且效果依赖个人空间想象力。VideoDoodles 改变了这一范式：它将涂鸦嵌入到 **3D 场景中的平面画布** 上，利用预计算的相机位姿、深度图和光流自动处理透视渲染和遮挡，使用户可以在正视校正后的 2D 界面上绘画，而系统负责将绘画“投影”回 3D 场景。

### 相对于已有方法的本质差异：改变的三个关键 slot

与已有视频涂鸦和点跟踪方法相比，VideoDoodles 在三个核心 slot 上做出了实质性改变：

**Slot 1：画布与场景的交互方式——从 2D 叠加到 3D 锚定。**
传统方法将画布视为 2D 图像层，无透视和遮挡处理。VideoDoodles 将画布定义为锚定于 3D 场景点的平面 3D 对象，通过 3D 刚性变换放置，渲染时自动执行深度测试实现遮挡（Fig. 2）。这本质上将“绘画空间”从屏幕坐标提升到了场景坐标，使得绘画与场景的几何关系由系统自动维护，而非用户手动模拟。

**Slot 2：运动跟踪——从 2D 点跟踪到 3D 轨迹优化。**
现有 2D 点跟踪方法（如 TAP-Net，Doersch et al., 2022）在图像空间操作，缺乏深度信息，易漂移且无法处理遮挡。VideoDoodles 提出了一种 **关键帧引导的 3D 轨迹优化** 方法：首先在低分辨率图上通过最短路径获得初始 3D 轨迹，然后利用场景流进行 **泊松积分** 以消除遮挡引起的漂移（Fig. 5）。这一 slot 的改变使得跟踪从“逐帧匹配外观”转变为“在 3D 空间积分运动场”，在 TAP-Vid DAVIS 基准上，单关键帧条件下 Average Jaccard 达到 40.8%（TAP-Net 为 37.2%），去除泊松积分后骤降至 18.3%，证实了这一改变的决定性作用。

**Slot 3：画布朝向——从固定朝向到轨迹对齐的自动优化。**
已有方法通常保持画布朝向固定或由用户手动调整，当被跟踪物体转弯时会产生不自然的视觉效果（Fig. 6b）。VideoDoodles 引入基于轨迹切线方向的朝向优化，在 SO(3) 上最小化画布法线与运动方向的对齐误差，同时支持用户通过相对旋转关键帧控制画布与物体的相对朝向。这使得画布能“跟随”物体转向（Fig. 6c），显著提升了动态场景中的视觉合理性。

### 知识库挂载点

VideoDoodles 可挂载到以下知识库节点：

1. **视频编辑与增强 (video editing and augmentation)**：作为交互式视频增强工具，与 3D 感知的视频编辑方法（如基于 NeRF 的场景编辑）并列。VideoDoodles 的独特贡献在于将手绘动画与 3D 视频场景融合，而非修改场景本身的纹理或几何。

2. **3D 点跟踪 (3D point tracking)**：与 TAP-Net（Doersch et al., 2022）、PIPs（Harley et al., 2022）等 2D 跟踪方法形成对比，VideoDoodles 的 3D 跟踪算法利用深度和场景流实现了更高的精度和时序平滑性。其泊松积分框架将跟踪问题转化为带关键帧约束的轨迹优化，与基于物理的轨迹平滑方法有理论联系。

3. **交互式 3D 绘画 (interactive 3D painting)**：与在 3D 模型表面绘画的工具（如 Adobe Substance 3D Painter）不同，VideoDoodles 在动态视频场景中引入平面画布，用户绘画时无需理解 3D 几何，系统自动处理透视和遮挡。

4. **视频深度估计与场景流应用 (applications of video depth and scene flow)**：VideoDoodles 展示了如何将现有的视频深度估计（如 Schönberger and Frahm, 2016）和光流方法（如 RAFT, Teed and Deng, 2020）组合为下游交互应用的预处理管线，为类似系统提供了参考架构。

### 适用边界

- **平面画布限制**：系统仅支持平面画布，无法创建自由形态的 3D 笔触（如围绕物体的螺旋彩带）。这限制了涂鸦的表现力，使其更适合“贴纸”式动画而非全 3D 绘画。
- **跟踪假设**：朝向优化假设物体朝向其主导运动方向，当物体自转时（如旋转的舞者，Fig. 9）无法自动捕捉，需用户手动添加朝向关键帧。
- **遮挡依赖深度精度**：深度估计错误会导致错误的遮挡效果（Fig. 10b），尤其在遮挡物轮廓周围。
- **透视收缩失真**：当画布严重透视收缩时，正视校正后的绘画面板会显示强烈扭曲的背景（Fig. 10a），影响绘画体验。
- **3D 重建成功率**：在 TAP-Vid DAVIS 的 30 个视频中仅 24 个成功完成 3D 重建，表明预处理管线对视频质量有一定要求。

### 后续启发

1. **非平面画布扩展**：论文提出的开放问题——如何定义基于参数形状或高度场的非平面画布——指向了将 VideoDoodles 的框架从平面提升到曲面，可能借鉴 3D 建模中的变形表面表示。

2. **多点联合跟踪**：当前方法独立跟踪每个画布，扩展为多点同时跟踪可改善朝向估计，并支持更复杂的多物体交互场景。

3. **遮挡感知的图构建**：论文提出的“跳跃边”概念（跳过遮挡帧）值得进一步探索，如何在不过度增加图复杂度的情况下处理长时遮挡，是多目标跟踪中的通用问题。

4. **多尺度跟踪策略**：当前方法在细薄物体上容易丢失跟踪，多尺度图构建或特征金字塔可能提升鲁棒性。

5. **与 NeRF/3DGS 的融合**：随着神经渲染技术的发展，将 VideoDoodles 的画布嵌入到可微渲染管线中，可能实现更精确的遮挡和光照一致性。

总体而言，VideoDoodles 的核心贡献在于 **将 3D 几何推理引入交互式视频涂鸦**，通过改变画布锚定、运动跟踪和朝向优化三个 slot，显著降低了用户创作场景感知动画的门槛。其在 TAP-Vid 基准上的定量优势（+3.6% AJ，+6.5% <δ_avg^x）和用户研究中的效率提升（49% 时间用于绘画而非技术操作）验证了这一设计思路的有效性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/VideoDoodles_Hand_drawn_Animations_on_Videos_With_Scene_aware_Canvases.pdf]]
---
title: "Localizing, Structuring, and Rendering: Bridging 3D and 2D Vision-Language-Action Models for Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision_Language_Action_Models_for_Robotic_Manipulation.pdf
project_link: null
code_link: "https://github.com/zyl123456aB/DIFFVLA"
aliases:
- DV
- LSRB32VLAMRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 可微渲染作为视觉桥梁，将 3D 空间语义嵌入图像，使 2D VLA 的损失梯度能反向传播至 3D 表示（立方体定位、颜色光束、相机姿态），形成闭环梯度流，统一空间推理与视觉感知。
primary_logic: 通过（1）在世界坐标系中定位立方体标记操作臂末端目标；（2）对周围几何进行颜色编码，使空间方向与距离信息转化为视觉可区分的彩色光束；（3）端到端学习自适应相机视角以最大化空间信息可见性，最终生成同时携带语义与空间线索的可微图像，驱动 2D VLA 实现精确的 6-DoF 操作。
claims:
- DiffRender-VLA 在 RLBench 仿真基准上达到 80.5% 的平均成功率，比现有最先进方法整体提升 +12.1%。
- 在遮挡、杂乱、空间推理三种典型困难场景中，分别获得 11.2%、17.8%、13.4% 的性能增益。
- 消融实验证实可微光束与自适应视角是关键：移除可微性后成功率从 80.5% 骤降至 74.8%，且翻译和旋转误差明显增大。
- 在真实机器人 AgileX PIPER 上取得 78.3% 平均成功率，相较 DP3 高出 45.0%，证明框架的实用性。
---

# Localizing, Structuring, and Rendering: Bridging 3D and 2D Vision-Language-Action Models for Robotic Manipulation

> [!tip] 核心洞察
> 通过（1）在世界坐标系中定位立方体标记操作臂末端目标；（2）对周围几何进行颜色编码，使空间方向与距离信息转化为视觉可区分的彩色光束；（3）端到端学习自适应相机视角以最大化空间信息可见性，最终生成同时携带语义与空间线索的可微图像，驱动 2D VLA 实现精确的 6-DoF 操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | 定位、结构化与渲染：桥接3D与2D视觉语言动作模型用于机器人操作 |
| 英文题名 | Localizing, Structuring, and Rendering: Bridging 3D and 2D Vision-Language-Action Models for Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision-Language-Action_Models_CVPR_2026_paper.html) · [Code](https://github.com/zyl123456aB/DIFFVLA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DiffRender-VLA |
| Dataset | RLBench, Real-world AgileX PIPER |

> [!tip] 效果简介
> - RLBench (Simulation) 上，Average Success Rate (%) 80.5 vs GWM (79.6) (+0.9)。
> - Real-world AgileX PIPER 上，Average Success Rate (%) 78.3 vs DP3 (33.3) (+45.0)。

## 概要

**问题瓶颈**：当前机器人操作模型存在两条割裂的技术路线——2D VLA 模型（如 RT-2、OpenVLA）擅长从图像中提取语义感知，但缺乏显式 3D 空间推理能力；3D VLA 模型（如 GWM、DP3）通过点云/体素实现精确几何推理，却牺牲了视觉直观性。这一鸿沟导致两类模型均无法同时获得空间理解与视觉感知的优势。

**核心洞察**：本文提出以**可微渲染**作为视觉桥梁，将 3D 空间语义嵌入图像，使 2D VLA 的损失梯度能反向传播至 3D 表示（立方体定位、颜色光束、相机姿态），形成闭环梯度流，统一空间推理与视觉感知。具体通过三阶段管道实现：（1）在世界坐标系中定位立方体标记操作臂末端目标；（2）对周围几何进行颜色编码，使空间方向与距离信息转化为视觉可区分的彩色光束；（3）端到端学习自适应相机视角以最大化空间信息可见性。

**关键结论**：
- 在 RLBench 仿真基准上达到 **80.5%** 平均成功率，比现有最优方法整体提升 **+12.1%**；在遮挡、杂乱、空间推理三种典型困难场景中，分别获得 **11.2%**、**17.8%**、**13.4%** 的性能增益。
- 在真实机器人 AgileX PIPER 上取得 **78.3%** 平均成功率，相较 DP3 高出 **45.0%**，验证了框架的实用价值。
- 消融实验证实可微光束与自适应视角是关键设计：移除可微性后成功率从 80.5% 骤降至 74.8%，替换为固定视角后降至 77.2%。

**方法定位**：DiffRender-VLA 属于 **3D 感知驱动的 2D VLA 增强框架**，通过可微渲染将点云几何结构转化为携带空间线索的 2D 图像，使预训练 2D VLA 无需架构改动即可获得 6-DoF 空间推理能力。其知识增量在于首次建立了从 2D VLA 损失到 3D 表示的可微梯度路径，实现了空间理解与语义感知的端到端协同优化。代码已开源（[DIFFVLA](https://github.com/zyl123456aB/DIFFVLA)）。



机器人操作正从“在已知位置拾取已知物体”向“在复杂三维环境中根据语言指令完成灵巧操作”演进。这一趋势催生了视觉语言动作模型（Vision-Language-Action, VLA），它将视觉感知、语言理解和动作生成统一为端到端可学习的策略。然而，当前 VLA 研究存在一条深刻的方法论断层：**2D VLA 与 3D VLA 各自擅长一端，却无法兼得空间推理与视觉感知**。

2D VLA 模型（如 **RT-2** (Brohan et al., 2023)、**OpenVLA** (Kim et al., 2024)、**UniVLA** (Wang et al., 2025)）以多视角 RGB 图像为输入，借助大规模预训练的视觉语言模型获得强大的语义理解与视觉直观性。但它们缺乏显式的三维几何表征，难以进行精确的空间推理——例如判断物体间的相对方位、在遮挡场景中推断目标位置、或在杂乱环境中规划无碰撞的末端路径。

3D VLA 模型（如 **ManiGaussian** (Lu et al., 2024)、**GWM** (Lu et al., 2025)、**DP3** (Ze et al., 2024)）则从点云或体素中直接学习几何表征，天然擅长空间推理，能够精确建模物体形状与位姿。但代价是牺牲了视觉语义的丰富性：点云缺乏纹理、光照等 2D 视觉线索，难以继承大规模 2D 视觉语言预训练的知识红利。

**核心瓶颈**在于：2D VLA 的损失函数作用于图像空间的语义特征，而 3D VLA 的损失作用于点云或体素空间，两者之间不存在梯度通路。这意味着空间理解（3D 擅长）与视觉感知（2D 擅长）无法在训练中相互促进，形成信息孤岛。

本文的动机正是打破这一壁垒。核心洞察是：**可微渲染可以作为视觉桥梁**——将 3D 空间语义“绘制”到 2D 图像中，使 2D VLA 的损失梯度能够反向传播至 3D 表征参数，形成闭环梯度流。具体而言，通过三个关键步骤实现这一桥接：(1) 在世界坐标系中定位立方体标记操作臂末端目标；(2) 对周围几何进行颜色编码，使空间方向与距离信息转化为视觉可区分的彩色光束；(3) 端到端学习自适应相机视角，最大化空间信息的可见性。最终生成的图像同时携带语义与空间线索，驱动 2D VLA 实现精确的六自由度（6-DoF）操作。

该框架在 RLBench 仿真基准上取得 80.5% 的平均成功率，比现有最先进方法整体提升 +12.1%；在遮挡、杂乱、空间推理三种典型困难场景中，分别获得 11.2%、17.8%、13.4% 的性能增益。在真实机器人 AgileX PIPER 上取得 78.3% 平均成功率，相较 DP3 高出 45.0%，验证了从仿真到现实的迁移能力。



## 核心方法与创新机理

DiffRender-VLA 的核心创新在于构建了一条**闭环可微梯度路径**，将 3D 空间推理与 2D 视觉语言动作模型（VLA）统一在端到端学习框架中。其关键突破体现在以下三个维度的设计变更：

### 1. 观察表示：从原始图像到可微渲染的空间语义图像

现有 2D VLA（如 **RT-2** (Brohan et al., 2023)、**OpenVLA** (Kim et al., 2024)）直接依赖原始 RGB(-D) 图像，缺乏显式 3D 空间推理能力；而 3D VLA（如 **GWM** (Lu et al., 2025)）虽擅长几何推理，却牺牲了视觉直观性。DiffRender-VLA 通过**可微渲染**生成同时携带语义与空间线索的图像，具体包括：
- **世界对齐立方体标记**：在世界坐标系中定位操作臂末端目标区域，以立方体显式锚定空间目标；
- **颜色编码空间关系**：对周围点云进行可微颜色光束编码——色相表示世界轴对齐的空间方向（红/青、绿/品红、蓝/黄），强度编码相对距离，将抽象的空间方向与距离信息转化为视觉可区分的彩色特征。

这一设计使 2D VLA 的损失梯度能够经渲染图像反向传播至 3D 表示（立方体定位、光束编码），形成闭环梯度流，从根本上打通了空间推理与视觉感知之间的信息壁垒。

### 2. 视角选择：从固定视角到端到端可学习的自适应视角

传统方法采用固定或预定义的多视角渲染，无法根据任务需求动态调整观察角度。DiffRender-VLA 引入**自适应视角渲染**模块：通过解码器将可学习的视角参数映射为相机外参和视场角，以任务损失为驱动，端到端优化相机姿态，最大化目标-环境空间关系在 2D 投影中的可见性。消融实验证实，将自适应视角替换为固定视角后，成功率从 80.5% 降至 77.2%，验证了可学习视角对空间信息利用率的提升。

### 3. 梯度流与知识传递：从断裂到闭环的可微路径

在传统范式中，2D VLA 与 3D 表示之间不存在梯度传递，两者独立训练或仅通过特征拼接进行浅层融合。DiffRender-VLA 构建了完整的可微梯度路径：2D VLA 的任务损失 → 渲染图像 → 自适应视角参数 → 颜色光束编码 → 立方体定位 → 点云特征。这一闭环机制使得 3D 空间表示能够直接接收来自 2D 语义理解的监督信号，实现空间与语义的深层协同优化。消融实验表明，移除光束的可微性后，成功率从 80.5% 骤降至 74.8%，平移和旋转误差明显增大，强有力地证明了端到端梯度的必要性。



DiffRender-VLA 的核心设计理念是**以可微渲染为桥梁，将 3D 空间推理能力注入 2D VLA 的语义感知流程**。如图 2 所示，框架由五个紧密耦合的模块串联而成，形成一条从点云到 6-DoF 动作的端到端可微管道。

### 管道总览

**输入**：场景点云 $\mathbf{V}$ 与语言指令嵌入 $\mathbf{e}_{\mathrm{lang}}$。

**输出**：末端执行器的 6-DoF 动作——三维平移位置、离散欧拉角旋转、二值夹爪开合状态。

**模块级联关系**：

1. **Coarse Cube Prediction Network（粗立方体预测网络）**
   接收点云与语言嵌入，通过 Perceiver IO 编码器 $\Phi_{\mathrm{enc}}$ 一次性联合预测三个关键量：目标区域的粗定位体素概率 $\mathbf{Q}_{\mathrm{coarse}}$、空间上下文特征 $\mathbf{Z}_{\mathrm{coarse}}$、以及自适应相机视角参数 $\pmb{\theta}_{\mathrm{view}}$。这一步在世界坐标系中确定一个与轴对齐的立方体标记区域，为后续空间编码提供几何锚点。

2. **Structuring Module（结构化模块）**
   将粗立方体周围的几何关系转化为视觉可区分的彩色光束。对点云中每个点计算其到立方体六个面的符号距离，并用世界轴对齐的互补色对（红/青、绿/品红、蓝/黄）进行颜色混合，生成同时保留原始外观与空间方向/距离信息的可微点云。混合权重由 sigmoid 函数根据点到立方体中心的距离自适应调节。

3. **Adaptive Viewpoint Rendering（自适应视角渲染）**
   将可学习的视角参数 $\pmb{\theta}_{\mathrm{view}}$ 解码为相机外参和视场角，以可微方式渲染多个自适应视角的图像 $\mathbf{I}_i$。视角参数通过任务损失反向传播进行优化，使相机自动寻找最能揭示目标-环境空间关系的观察角度。

4. **VLA Backbone（VLA 骨干网络）**
   采用预训练的 2D VLA（如 OpenVLA）处理每个渲染视角的图像与语言指令，提取语义特征 $\mathbf{Z}_{\mathrm{VLA}}^{i} = \psi_{\mathrm{VLA}}(\mathbf{I}_i, \mathbf{e}_{\mathrm{lang}})$。骨干网络在训练中微调，以适应空间标记带来的新视觉模式。

5. **Bidirectional Cross-Attention Fusion & Action Prediction（双向交叉注意力融合与动作预测）**
   对粗空间特征 $\mathbf{Z}_{\mathrm{coarse}}$ 与多视角 VLA 语义特征 $\mathbf{Z}_{\mathrm{VLA}}$ 执行双向交叉注意力融合，得到联合表示 $\mathbf{Z}_{\mathrm{fused}}$。基于该融合特征，三个独立预测头分别输出：精炼的平移位置（通过立方体六个面的投影得分聚合取平均）、离散欧拉角旋转、以及夹爪二值状态。

### 关键梯度流

框架的独特之处在于形成了一条**闭环可微梯度路径**：2D VLA 的动作预测损失 $\mathcal{L}_{\mathrm{task}}$ 经渲染图像 $\mathbf{I}_i$ 反向传播至相机视角参数、光束颜色混合权重、乃至粗立方体定位。这意味着空间推理模块（定位、结构化、视角选择）能够直接从任务目标中学习，而非依赖独立的监督信号。消融实验表明，切断这条梯度路径（如将光束设为不可微）会导致成功率从 80.5% 骤降至 74.8%，充分验证了端到端梯度流的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DiffRender-VLA. The framework bridges spatial and 2D VLA paradigms through differentiable rendering: localiz-Cross Attention Action Predictioning anchors the next manipulation target, structuring encodes surrounding geometry as color-encoded differentiable features, and rendering optimizes viewpoints to project spatial semantics as interpretable, differentiable images*



DiffRender-VLA 的核心创新在于构建了一条**闭环可微梯度路径**：将 3D 空间语义嵌入可微渲染图像，使 2D VLA 的任务损失能够反向传播至 3D 表示（立方体定位、颜色光束、相机姿态），从而统一空间推理与视觉感知。该框架由五个关键模块串联而成。

### 粗定位编码器

框架首先通过 Perceiver IO 编码器联合处理体素化点云与语言指令嵌入，一次性输出三项关键信息：

$$( \mathbf{Q}_{\mathrm{coarse}}, \mathbf{Z}_{\mathrm{coarse}}, \pmb{\theta}_{\mathrm{view}} ) = \Phi_{\mathrm{enc}} ( \mathbf{V}, \mathbf{e}_{\mathrm{lang}} )$$

其中 $\mathbf{V}$ 为输入体素，$\mathbf{e}_{\mathrm{lang}}$ 为语言嵌入。$\mathbf{Q}_{\mathrm{coarse}}$ 是粗定位体素概率分布，$\mathbf{Z}_{\mathrm{coarse}}$ 是空间特征，$\pmb{\theta}_{\mathrm{view}}$ 是可学习的相机视角参数。最高置信度的粗位置 $\mathbf{p}_{\mathrm{coarse}} \in \mathbb{R}^{3}$ 通过对 $\mathbf{Q}_{\mathrm{coarse}}$ 的可微空间期望计算得到。该立方体与世界轴对齐（而非相机轴），以确保在 2D 投影中通过纯几何关系编码空间信息。

### 结构化光束编码

结构化模块将抽象的 3D 空间关系转化为视觉可感知的颜色特征。对于点云中的每个点 $\mathbf{x}$，计算其到立方体六个面的符号距离，并用世界轴对齐的颜色（红/青、绿/品红、蓝/黄）进行光束混合：

$$\mathbf { c } _ { \mathrm { b e a m } } ( \mathbf { x } ) = \left( 1 - \alpha ( \mathbf { x } ) \right) \mathbf { c } _ { \mathrm { o r i g } } ( \mathbf { x } ) + \alpha ( \mathbf { x } ) \sum _ { j = 1 } ^ { 6 } \mathbf { c } _ { j } \, \exp \bigl ( - k _ { \mathrm { b e a m } } w _ { j } ( d _ { j } ( \mathbf { x } ) ) \bigr )$$

其中 $\mathbf{c}_{\mathrm{orig}}(\mathbf{x})$ 为点的原始颜色，$\mathbf{c}_j$ 为六个面对应的方向性颜色，$d_j(\mathbf{x})$ 为点到面 $j$ 的符号距离，$w_j$ 为基于距离的权重函数，$k_{\mathrm{beam}}$ 控制光束衰减速率。混合权重 $\alpha(\mathbf{x})$ 通过 sigmoid 函数根据点到立方体中心的距离平滑控制：

$$\alpha ( \mathbf { x } ) = \sigma _ { \mathrm { s i g } } \bigg ( \frac { r _ { \mathrm { t a r g e t } } - \left\| \mathbf { x } - \mathbf { p } _ { c } \right\| } { \sigma _ { \mathrm { b l e n d } } } \bigg )$$

该设计的关键特性是：色相指示空间方向（与世界轴对齐），强度编码相对距离，且编码在多视角下保持一致。

### 自适应视角渲染

与固定或预定义视角不同，DiffRender-VLA 通过解码器将可学习的视角参数 $\pmb{\theta}_{\mathrm{view}}$ 映射为相机外参和视场角，以可微方式渲染多个自适应视角的图像。可微相机姿态使梯度能够从渲染图像回流至视角参数，即 $\frac{\partial \mathcal{L}_{\mathrm{task}}}{\partial \mathbf{I}_i} \rightarrow \frac{\partial \mathbf{I}_i}{\partial \pmb{\theta}_{\mathrm{view}}}$，从而端到端优化视角以最大化目标-环境空间关系的可见性。

### VLA 特征提取与双向交叉注意力融合

每个渲染视角的图像 $\mathbf{I}_i$ 经预训练的 2D VLA 骨干（如 OpenVLA）处理，提取语义特征：

$$\mathbf{Z}_{\mathrm{VLA}}^{i} = \psi_{\mathrm{VLA}} ( \mathbf{I}_{i}, \mathbf{e}_{\mathrm{lang}} )$$

随后，粗空间特征 $\mathbf{Z}_{\mathrm{coarse}}$ 与多视角 VLA 语义特征 $\mathbf{Z}_{\mathrm{VLA}}$ 通过双向交叉注意力进行融合：

$$\mathbf{Z}_{\mathrm{fused}} = \mathrm{CrossAttn}( \mathbf{Z}_{\mathrm{coarse}}, \mathbf{Z}_{\mathrm{VLA}} ) + \mathrm{CrossAttn}( \mathbf{Z}_{\mathrm{VLA}}, \mathbf{Z}_{\mathrm{coarse}} )$$

这一设计使空间结构引导语义聚焦，同时用语义理解精炼空间预测，形成双向信息流。

### 动作预测头

基于融合特征 $\mathbf{Z}_{\mathrm{fused}}$，三个独立预测头分别输出 6-DoF 末端执行器动作。平移头将融合特征解码为平移得分体素，并投影回空间坐标：

$$\mathbf{Q}_{\mathrm{trans}}^{i} = h_{\mathrm{trans}}( \mathbf{Z}_{\mathrm{fused}}^{i} ) \in \mathbb{R}^{D \times H \times W}, \quad \mathbf{p}^{(i)} = \mathrm{Proj.to.Spatial} \big( \operatorname*{argmax}_{x,y,z} \mathbf{Q}_{\mathrm{trans}}^{i} \big)$$

最终位置取立方体六个表面预测的平均：$\mathbf{p} = \frac{1}{6}\sum_{i=1}^{6} \mathbf{p}^{(i)}$。旋转头通过最大池化聚合多视角特征后预测离散欧拉角，夹爪头输出二值开合状态。

整个管道的梯度流闭环是方法的核心：2D VLA 的损失经渲染图像反向传播至光束编码参数、立方体定位和视角参数，使 3D 空间推理与 2D 视觉感知在统一优化目标下协同学习。消融实验证实，移除光束的可微性后成功率从 80.5% 降至 74.8%，验证了端到端梯度的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of differentiable point cloud rendered image. We use RLbench [19] and RH20T [10] dataset for display*

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/009_Figure_7.jpg]]
*Figure 7: Adaptive viewpoint analysis validates differentiable camera poses enable task-specific optimization*



## 实验与关键发现

### 核心瓶颈与因果机制

当前 2D VLA 模型（如 **RT-2** (Brohan et al., 2023)、**OpenVLA** (Kim et al., 2024)）依赖图像语义进行决策，缺乏显式 3D 空间推理能力；而 3D VLA 模型（如 **GWM** (Lu et al., 2025)、**ManiGaussian** (Lu et al., 2024)）虽擅长几何推理，却牺牲了视觉直观性。DiffRender-VLA 通过可微渲染建立视觉桥梁：将 3D 空间语义嵌入图像，使 2D VLA 的损失梯度能反向传播至立方体定位、颜色光束编码和相机姿态参数，形成闭环梯度流，统一空间推理与视觉感知。

### 仿真实验主结果：RLBench 基准

Table 1 展示了在 RLBench 仿真基准上的完整任务成功率。DiffRender-VLA 取得 **80.5%** 的平均成功率，相较于最强竞争对手 **GWM** (79.6%) 提升 +0.9 个百分点，整体比现有最先进方法提升 **+12.1%**。在遮挡、杂乱、空间推理三种典型困难场景中，分别获得 **11.2%**、**17.8%**、**13.4%** 的性能增益。这些结果验证了可微渲染桥接策略在复杂空间场景下的有效性。

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/005_Table_1.jpg]]
*Table 1: Simulation results on RLBench. Success rates (%) with standard deviation. Best results in bold, second best underlined.View*

### 真实世界实验：AgileX PIPER 平台

Table 2 报告了在真实机器人 AgileX PIPER 上的 6 项操作任务结果（每项任务 20 次试验）。DiffRender-VLA 取得 **78.3%** 的平均成功率，相较 **DP3** (Ze et al., 2024) 的 33.3% 高出 **+45.0%**，证明框架在真实环境中的实用性和鲁棒性。Figure 4 和 Figure 6 分别展示了真实世界任务执行步骤和部署场景。

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/008_Table_2.jpg]]
*Table 2: Real-world results on AgileX PIPER. Success rates (%) across 20 trials per task*

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of our real-world tasks. For each task, we show several steps to understand the task process*

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/007_Figure_6.jpg]]
*Figure 6: Real-World Deployment Situation*

### 组件消融：可微光束与自适应视角的决定性作用

Table 3 的消融实验揭示了各组件对性能的贡献：

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/010_Table_3.jpg]]
*Table 3: Component ablation. Trans./Rot. Error in cm/degrees*

- **完整可微框架**：成功率 80.5%，平移误差 1.7 cm，旋转误差 8.2°。
- **移除光束可微性**（Non-differentiable beams）：成功率骤降至 **74.8%**，平移和旋转误差明显增大，证实端到端梯度流的必要性。
- **固定视角**（Fixed views）：成功率降至 **77.2%**，表明可学习视角（Figure 7）通过最大化空间信息可见性，显著提升了空间信息利用率。
- **仅用 RGB 而不使用光束编码**（No beams）：成功率进一步降至 **70.1%**，证实空间颜色编码（色相表示方向、强度编码距离）是有效的视觉中介。

### 零样本泛化能力

Table 4 的零样本泛化实验评估了分布偏移下的性能衰减。DiffRender-VLA 在未见过的场景配置中保持了较高的成功率，衰减幅度显著低于对比方法，表明框架学习到的空间-语义联合表示具有较强的泛化性。

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/011_Table_4.jpg]]
*Table 4: Zero-shot generalization. Success (%) and degradation from in-domain*

### 光束参数敏感性

Figure 8 的热力图分析了光束厚度与透明度参数对小型物体操作的影响，揭示了最优参数区域。该分析为实际部署中的超参数调优提供了指导。

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/012_Figure_8.jpg]]
*Figure 8: Beam parameters improvement for small objects*

### 失败模式与局限

尽管整体性能优异，方法在极端动态环境（如高速移动物体）或完全未见过的物体类别上的泛化能力仍需进一步验证。此外，可微渲染的实时性在资源受限的嵌入式机器人平台上的表现尚未明确，这限制了其在低算力场景中的直接部署。

### 补充图表

![[assets/figures/papers/paper_list_l2181_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Localizing_Struct/figures/006_Figure_5.jpg]]
*Figure 5: Simulation Tasks for Occlusion and Clutter enviroments*



## 定位与知识库关联

### 范式定位：2D VLA 与 3D VLA 的桥接者

DiffRender-VLA 的核心定位在于填补 2D 视觉-语言-动作模型（VLA）与 3D VLA 之间的根本性鸿沟。现有 2D VLA 模型（如 **RT-2**（Brohan et al., 2023）、**OpenVLA**（Kim et al., 2024）、**UniVLA**（Wang et al., 2025））依赖多视角图像变换器提取直观语义，但在遮挡、杂乱和需要精细空间推理的任务中缺乏显式 3D 几何理解；而 3D VLA 模型（如 **GWM**（Lu et al., 2025）、**ManiGaussian**（Lu et al., 2024）、**DP3**（Ze et al., 2024））通过点云/体素实现精确空间感知，却牺牲了视觉可解释性。DiffRender-VLA 通过可微渲染将 3D 空间语义嵌入 2D 图像，使 2D VLA 的损失梯度能反向传播至 3D 表示（立方体定位、颜色光束、相机姿态），形成闭环梯度流，从而统一两类范式的优势。

### 技术谱系中的关键创新槽位

相较于现有方法，DiffRender-VLA 在三个关键设计槽位上进行了系统性的创新替换：

| 设计槽位 | 基线方案 | DiffRender-VLA 方案 |
|----------|----------|---------------------|
| **观察表示** | 原始 RGB(-D) 图像或体素/点云特征 | 可微渲染图像，嵌入世界对齐立方体及颜色编码的空间关系（方向、距离） |
| **视角选择** | 固定或预定义的多视角渲染 | 通过任务损失端到端可学习的自适应相机视角，最大化空间信息可见性 |
| **梯度流与知识传递** | 2D VLA 与 3D 表示之间无梯度传递 | 闭环可微梯度路径：2D VLA 损失经渲染图像反向传播至立方体定位、光束编码和视角参数 |

这些创新并非孤立存在，而是形成了一条完整的因果链：**粗定位**在世界坐标系中预测目标立方体区域 → **结构化编码**将周围几何转化为方向性彩色光束 → **自适应渲染**优化相机视角以最大化空间信息在 2D 投影中的可见性 → **可微梯度**使 2D VLA 的语义理解反向塑造 3D 空间表示。这一闭环设计是该方法区别于所有基线工作的本质特征。

### 适用边界与约束条件

基于论文提供的实验证据，DiffRender-VLA 的适用边界可归纳如下：

**已验证的有效场景：**
- 仿真环境（RLBench）中的 6-DoF 操作任务，包括遮挡、杂乱和空间推理三类困难场景
- 真实机器人平台（AgileX PIPER）上的 6 项操作任务，涵盖抓取、放置等典型操作

**已知约束：**
- 依赖点云输入，需要深度传感器或仿真器提供 3D 几何信息
- VLA 骨干基于预训练模型（OpenVLA）初始化，其性能受限于基座模型的能力边界
- 可微渲染引入额外计算开销，在资源受限的嵌入式平台上的实时性表现尚未明确

**待验证的泛化边界：**
- 极端动态环境（如高速移动物体）下的性能
- 完全未见过的物体类别上的零样本泛化能力（论文 Table 4 展示了分布偏移下的泛化结果，但未覆盖极端域外场景）
- 不同机器人本体和传感器配置下的迁移能力

### 局限与开放问题

论文未明确讨论以下局限，需读者自行评估：

1. **数据依赖与偏差**：论文未提及训练数据的分布偏差、伦理合规性或公平性问题。所有实验在标准基准和特定真实机器人上进行，未见对特定群体或场景的系统性偏见分析，但这一缺失本身值得关注。

2. **可微渲染的实时性**：虽然可微性是该方法的核心优势，但渲染管线的计算延迟在真实部署中的影响未被量化。对于需要高频闭环控制的操作任务，这一因素可能成为瓶颈。

3. **光束编码的普适性**：颜色编码依赖世界轴对齐的色相映射（红/青、绿/品红、蓝/黄），在物体自身颜色与光束颜色相近时，空间信息的可辨识性可能下降。论文 Figure 8 分析了光束参数对小型物体的影响，但未讨论颜色冲突场景。

4. **与更大规模基座模型的整合**：DiffRender-VLA 目前基于 OpenVLA 初始化，未来与更大规模 VLA 或视觉-语言模型的整合方式及性能增益尚未探索。

5. **多任务与持续学习**：论文聚焦单任务训练，未讨论多任务联合训练或持续学习场景下的表现，这限制了其在开放世界机器人应用中的直接适用性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision_Language_Action_Models_for_Robotic_Manipulation.pdf]]

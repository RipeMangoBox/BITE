---
title: "MoRig: Motion-Aware Rigging of Character Meshes from Point Clouds"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/MoRig_Motion_Aware_Rigging_of_Character_Meshes_from_Point_Clouds.pdf
project_link: null
code_link: "https://github.com/zhan-xu/MoRig"
aliases:
- MoRig
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
core_operator: 引入基于点云序列的Transformer运动编码器，提取运动感知的顶点特征，用于指导变形、关节定位和蒙皮权重的推断，从而将运动线索与目标网格绑定流程紧密结合。
primary_logic: 通过Transformer编码器聚合多帧顶点位移轨迹，可以生成与关节部位高度相关的运动感知特征；这些特征能有效区分不同运动区域，使关节提取更准确，蒙皮权重更一致，最终提升动画质量。
claims:
- 在ModelsResource测试集上，MoRig的关节Chamfer距离为3.5%，相比SkeRig降低53%（7.5%→3.5%），动画顶点距离误差为2.4%，相比RigNet降低22.5%（3.1%→2.4%）。
- 在真实点云序列测试中，MoRig的关节IoU达到65.7%，显著高于RigNet的46.7%。
- 消融实验表明，Transformer编码器优于平均/最大池化，且模型性能随输入帧数增加而提升。
- ModelsResource test split 上 Joint Chamfer distance = 3.5%
---

# MoRig: Motion-Aware Rigging of Character Meshes from Point Clouds

> [!tip] 核心洞察
> 通过Transformer编码器聚合多帧顶点位移轨迹，可以生成与关节部位高度相关的运动感知特征；这些特征能有效区分不同运动区域，使关节提取更准确，蒙皮权重更一致，最终提升动画质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoRig: 基于点云的运动感知角色网格绑定 |
| 英文题名 | MoRig: Motion-Aware Rigging of Character Meshes from Point Clouds |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://zhan-xu.github.io/motion-rig/) · [Code](https://github.com/zhan-xu/MoRig) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_animation_interaction #topic/vision_multimodal_applications |
| Method | MoRig |
| Dataset | ModelsResource test split, Real-world scans |

> [!tip] 效果简介
> - ModelsResource test split 上，Joint Chamfer distance 3.5% vs 7.5% (SkeRig) (-53% (相对减少))；Joint Chamfer distance 3.5% vs 3.9% (RigNet) (-10% (相对减少))；Skinning L1 error 0.32 vs 0.39 (RigNet) (-18% (相对减少))。
> - Real-world scans (DFaust / KillingFusion) 上，Joint IoU 65.7% vs 46.7% (RigNet) (+19.0% (绝对提升))；Joint Precision 70.0% vs 44.5% (RigNet) (+25.5% (绝对提升))；Joint Recall 62.2% vs 49.9% (RigNet) (+12.3% (绝对提升))。

## 概要

传统角色骨骼绑定方法依赖手工模板或仅利用静态几何信息，难以适应多样化结构，且忽略运动线索，导致绑定骨架与动画动作不符。MoRig 提出一种运动感知的自动绑定方法，输入目标网格与表演角色的单视角点云序列，通过 Transformer 运动编码器从多帧顶点位移轨迹中提取与关节部位相关的运动感知特征，指导变形对齐、关节定位和蒙皮权重推断，最终实现运动重定向。在合成测试集上，MoRig 的关节 Chamfer 距离为 3.5%，相比 SkeRig 相对降低 53%，相比 RigNet 降低 10%；动画顶点误差为 2.4%，相比 RigNet 降低 22.5%。在真实扫描数据上，关节 IoU 达 65.7%，显著优于 RigNet 的 46.7%。该方法将运动信息引入绑定流程，属于基于学习的骨骼绑定方法的延伸，其核心创新在于用 Transformer 聚合时序运动特征替代纯几何特征。

## 核心方法与创新机理

### 问题背景与核心瓶颈

传统的角色骨骼绑定方法面临两个根本性瓶颈。其一，基于手工模板的方法需要艺术家为每种角色结构设计专用模板，难以适应多样化的角色形态。其二，以 **RigNet**（Xu et al., SIGGRAPH 2020）为代表的基于学习的自动绑定方法，仅从单个静态网格的几何形状推断骨骼和蒙皮权重，完全忽略了角色的运动信息。这导致绑定的骨骼可能与用户期望的动画动作不匹配——例如，几何上相似但运动功能不同的部位（如装饰性突起与可活动的肢体）在静态几何中难以区分，从而限制了动画重定向的准确性和灵活性。

**MoRig** 的核心创新在于引入运动线索作为绑定的关键输入：给定一个目标网格和一段表演角色的单视角点云序列，方法自动为网格生成与点云运动相匹配的骨骼绑定和蒙皮权重，并将运动重定向到绑定后的网格上。

### 核心机制：运动感知特征的学习

MoRig 的核心机制是通过 **Transformer 运动编码器** 聚合多帧顶点位移轨迹，生成与关节部位高度相关的运动感知特征。其关键洞察在于：同一关节部位内的顶点在运动过程中表现出高度相似的位移模式，而不同部位之间的运动差异显著。通过 Transformer 的自注意力机制，模型能够自适应地聚合多帧位移信息，使运动感知特征能够有效区分不同运动区域。这些特征随后被注入到绑定模块中，指导关节提取和蒙皮权重预测，使关节定位更准确、蒙皮权重更一致。

### Changed Slots：相对于基线的关键差异

MoRig 相对于 **RigNet** 和 **SkeRig** 等基线方法，在以下三个关键维度上引入了根本性改变：

| 维度 | 基线方法 | MoRig 方案 |
|------|---------|-----------|
| **输入模态** | 仅单个静态网格 | 静态网格 + 表演角色的点云序列 |
| **运动编码器** | 无运动编码器，或使用平均/最大池化 | 带可学习 `[CLS]` token 的 Transformer 编码器 |
| **绑定输入特征** | 仅几何特征 | 几何特征 + 运动编码器生成的运动感知特征 |

其中，输入模态的改变是根本性的：点云序列提供了角色在运动中的时空信息，使模型能够“看到”哪些部位在运动、如何运动。运动编码器架构的选择则决定了能否有效提取这些信息——消融实验证实，Transformer 编码器显著优于简单的平均/最大池化聚合。绑定输入特征的扩展使骨骼推断和蒙皮预测同时受益于几何和运动双重线索。

### 方法框架与模块顺序

MoRig 的完整流水线由五个顺序模块组成，模块之间存在紧密的因果依赖关系：

1. **对应关系模块（Correspondence Module）**：为每帧预测网格顶点与点云点之间的软对应关系。
2. **变形模块（Deformation Module）**：利用对应关系将目标网格对齐到每个点云帧，处理遮挡。
3. **运动编码器（Motion Encoder）**：将逐顶点位移轨迹转换为运动感知特征。
4. **绑定模块（Rigging Module）**：利用运动感知特征预测骨骼关节和蒙皮权重。
5. **动画迁移（Animation Transfer）**：通过逆运动学回归关节角度，将运动重定向到绑定后的网格。

各模块的因果关系如下：对应关系模块的输出（匹配得分和对应掩膜）驱动变形模块；变形模块产生的逐帧顶点位移序列是运动编码器的输入；运动编码器生成的运动感知特征被馈入绑定模块，指导关节定位和蒙皮权重预测；最后，绑定结果与点云运动轨迹结合，通过 IK 重定向实现动画迁移。整个流水线是端到端可微的，允许梯度从绑定损失回传至对应关系模块。

### 关键模块详解

#### 对应关系模块

该模块为每帧 $t$ 预测两类输出：
- **匹配得分** $s_{p,v}^{(t)} = \mathbf{f}_p^{(t)} \cdot \mathbf{f}_v$：点云点特征 $\mathbf{f}_p^{(t)}$ 与网格顶点特征 $\mathbf{f}_v$ 的余弦相似度，用于衡量点与顶点的匹配程度。
- **对应掩膜概率** $q_v^{(t)}$：指示顶点 $v$ 在帧 $t$ 中是否有真实对应点的概率，用于处理遮挡。

训练时使用两个损失函数监督：
- **对应掩膜损失** $L_{\text{mask}} = \sum_{t,v} \text{BCE}(q_v^{(t)}, m_v^{(t)})$：二进制交叉熵损失，监督对应掩膜预测。
- **对应 InfoNCE 损失** $L_{\text{corr}} = -\sum_{t,v} \log \frac{\exp(\mathbf{f}_{\hat{\imath}(v)}^{(t)} \cdot \mathbf{f}_v / \tau)}{\sum_{p} \exp(\mathbf{f}_p^{(t)} \cdot \mathbf{f}_v / \tau)}$：对比损失，拉近真实匹配点-顶点特征对，推远非匹配特征对。

#### 变形模块

变形模块分两步将目标网格对齐到每个点云帧：

**第一步：初始变形估计。** 对每个顶点 $v$，计算加权位移向量：
$$\mathbf{d}_v^{(t)} = \frac{\sum_{p} \exp(s_{p,v}^{(t)}/\tau) (\mathbf{y}_p^{(t)} - \mathbf{y}_v)}{\sum_{p} \exp(s_{p,v}^{(t)}/\tau)}$$
即以匹配得分为权重的 softmax 加权平均位移。对于对应掩膜概率 $q_v^{(t)} < 50\%$ 的顶点（可能被遮挡），将其位移替换为最近可靠测地邻居的位移，实现变形传播。

**第二步：变形精炼。** 使用 GMEdgeNet 图神经网络对初始变形进行精炼。逐顶点输入特征为：
$$\mathbf{x}_v = [\mathbf{y}_v, \mathbf{d}_v^{(t)}, q_v^{(t)}]$$
即位置、初始位移和对应概率的拼接。网络输出精炼后的位移残差 $\mathbf{e}_v^{(t)}$，最终变形后的顶点位置为 $\mathbf{y}_v^{(1)} = \mathbf{y}_v + \mathbf{e}_v^{(1)}$。训练使用 L1 损失监督：
$$L_{\text{flow}} = \sum_{v,t} \lVert \hat{\mathbf{d}}_v^{(t)} - \mathbf{d}_v^{(t)} \rVert_1$$

#### Transformer 运动编码器

运动编码器的输入是每个顶点从第 2 帧到第 $T$ 帧的位移序列 $\{\mathbf{e}_v^{(t)}\}_{t=2}^{T}$。设计要点如下：

- **输入变换**：位移向量首先通过线性层映射为 $D$ 维特征 $\mathbf{g}_v^{(t)}$。
- **可学习 `[CLS]` token**：借鉴 BERT 的设计，在每帧的顶点特征序列前添加一个可学习的 `[CLS]` token，其最终输出作为该帧的聚合表示。
- **多头自注意力**：对每个注意力头 $n$，将输入特征通过投影矩阵 $\mathbf{Q}_n, \mathbf{K}_n, \mathbf{V}_n$ 变换为查询、键、值：
  $$\mathbf{q}_{v,n}^{(t)} = \mathbf{Q}_n \mathbf{g}_v^{(t)},\quad \mathbf{k}_{v,n}^{(t)} = \mathbf{K}_n \mathbf{g}_v^{(t)},\quad \mathbf{v}_{v,n}^{(t)} = \mathbf{V}_n \mathbf{g}_v^{(t)}$$
  注意力权重通过缩放点积计算：
  $$\mathbf{A}_{v,n}^{(t)} = \text{softmax}\left(\frac{\mathbf{q}_{v,n}^{(t)} \cdot \mathbf{k}_{v,n}^{(t)}}{\sqrt{D}}\right)$$
- **特征聚合**：`[CLS]` token 的输出通过对所有帧的值向量加权求和得到：
  $$\mathbf{g}_{v,n}^{\prime(1)} = \sum_{t=1}^{T} \mathbf{A}_{v,n}^{(t)} \mathbf{v}_{v,n}^{(t)}$$
- **最终输出**：拼接所有注意力头的输出并通过投影矩阵 $\mathbf{U}$ 得到 $D$ 维运动感知特征：
  $$\mathbf{h}_v = [\mathbf{g}_{v,1}^{\prime(1)}, \dots, \mathbf{g}_{v,N}^{\prime(1)}] \mathbf{U}$$

这种设计的优势在于：Transformer 的自注意力机制能够自适应地关注不同帧之间的运动模式关联，`[CLS]` token 则提供了统一的聚合表示，使得同一关节部位内的顶点获得相似的运动感知特征。

#### 绑定模块

绑定模块利用运动感知特征 $\mathbf{h}_v$ 增强 RigNet 原有的几何特征，实现两个子任务：
- **关节提取**：通过计算每个顶点与其邻居运动特征的差异并池化，定位关节部位之间的边界，从而更准确地聚类出关节位置。
- **蒙皮权重预测**：运动感知特征使同一部位内的顶点位移和聚类更加一致，从而产生更连贯的蒙皮权重。

#### 动画迁移

给定绑定后的骨骼和点云运动轨迹，通过全身逆运动学（IK）回归关节角度，再将关节角度通过 IK 重定向应用到目标网格上，完成动画迁移。

### 训练与推理路径

**训练阶段**：使用合成动画数据集（ModelsResource 与 DeformThings4D）进行监督训练。损失函数包括对应掩膜损失 $L_{\text{mask}}$、对应 InfoNCE 损失 $L_{\text{corr}}$、变形 L1 损失 $L_{\text{flow}}$，以及绑定相关的关节定位损失和蒙皮权重损失。整个流水线端到端可微，梯度从最终绑定损失回传至对应关系模块。

**推理阶段**：给定目标网格和点云序列，依次执行对应关系预测、变形对齐、运动编码和绑定推断。动画迁移时，通过 IK 从点云轨迹回归关节角度并重定向。据论文报告，关节拟合在 NVidia 2080Ti 上每网格约需 3 秒。

![[assets/figures/papers/paper_list_l66_https_zhan_xu_github_io_motion_rig/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of our method: (a) The correspondence module predicts partial correspondences between the mesh and each point cloud. (b) The deformation module aligns the target mesh with each point cloud frame driven by these correspondences while being robust to occlusions. (c) The motion encoder converts the resulting per-vertex trajectories to motion-aware features that are correlated with underlying articulated parts. (d) The rigging module outputs a character rig by utilizing these features. The input mesh is animated according to the rig and the point cloud motion*

## 实验与关键发现

### 评估设置与基准

MoRig 在合成与真实两类数据上进行了系统评估。训练集由 ModelsResource 与 DeformThings4D 的合成动画序列构成，测试则覆盖 ModelsResource 的 hold-out 分割以及 DFaust 和 KillingFusion 的真实扫描点云序列。评估沿用 RigNet（Xu et al., SIGGRAPH 2020）的标准指标：关节定位采用 Chamfer 距离，蒙皮质量采用 L1 蒙皮权重误差，动画质量采用顶点 L2 距离误差。蒙皮评估时，所有方法使用相同的真实骨骼以隔离蒙皮预测质量；真实扫描数据在训练中完全不可见，仅用于测试泛化能力。

### 主实验结果

**Table 1** 汇总了 MoRig 与基线方法及自身变体的定量对比，核心结果如下。

**关节定位精度。** 在 ModelsResource 测试集上，MoRig 的关节 Chamfer 距离为 **3.5%**（相对于包围盒最大轴归一化）。相比 SkeRig 的 7.5%，相对误差降低 **53%**；相比 RigNet 的 3.9%，相对误差降低 **10%**。这表明运动感知特征能够有效区分不同关节区域，使预测的关节位置更接近艺术家标注的参考骨骼。Figure 4 的定性对比进一步印证了这一点：MoRig 预测的骨骼在四肢末端、躯干分叉等关键部位与艺术家手工创建的骨骼高度一致，而 RigNet 因仅依赖静态几何，常出现关节偏移或遗漏。

**蒙皮权重质量。** MoRig 的蒙皮 L1 误差为 **0.32**，相比 RigNet 的 0.39 实现 **18%** 的相对降低。运动感知特征使同一关节部件内的顶点位移高度一致，从而在聚类生成蒙皮权重时更为连贯，减少了跨部件边界的权重泄漏。

**动画顶点误差。** 将预测的骨骼与蒙皮权重应用于动画重定向后，MoRig 的顶点 L2 距离误差为 **2.4%**，相比 RigNet 的 3.1% 降低 **22.5%**。这一指标直接衡量最终动画质量，说明运动感知绑定对动画重定向准确性的提升具有实质性影响。

**真实扫描泛化能力。** 在 DFaust 和 KillingFusion 的真实点云序列上（Table 2 / Figure 7），MoRig 的关节 IoU 达到 **65.7%**，显著高于 RigNet 的 **46.7%**（绝对提升 19.0%）；关节精确率从 44.5% 提升至 **70.0%**（+25.5%），召回率从 49.9% 提升至 **62.2%**（+12.3%）。真实数据包含严重的自遮挡、噪声和稀疏采样（如 KillingFusion 的动态融合序列），MoRig 仍能保持较高的关节定位精度，证明了变形模块对遮挡的鲁棒性以及运动编码器对噪声的容忍度。

### 消融实验

**运动编码器架构选择。** Table 1 中对比了三种运动特征聚合策略：平均池化、最大池化和 Transformer 编码器。Transformer 编码器在所有指标上均取得最优结果，验证了自注意力机制对多帧位移轨迹中关键运动模式的提取能力。平均池化因平等对待所有帧而稀释了判别性运动信息，最大池化则对噪声帧过于敏感。

**输入帧数的影响。** Figure 8 展示了动画顶点误差随输入帧数（从 2 帧到 30 帧）的变化曲线。误差随帧数增加持续下降，在约 20 帧后趋于平缓。这表明更多的运动观测能够提供更丰富的关节运动线索，有利于运动编码器学习更准确的运动感知特征。但帧数超过 20 后边际收益递减，实际应用中可根据计算预算权衡帧数。

### 失败模式与适用边界

尽管 MoRig 在多数测试场景中表现优异，论文明确指出了若干失效条件：

1. **不可见部件的绑定缺陷。** 方法假设输入点云序列展示了目标角色的所有关节运动。若某部件在序列中完全不可见（如从未摆动的尾巴），运动编码器无法提取该区域的运动特征，系统将退化为仅依赖静态几何形状，可能无法为该部件生成骨骼。Figure 7 的某些真实案例中，角色背部或附件区域的关节定位精度有所下降。

![[assets/figures/papers/paper_list_l66_https_zhan_xu_github_io_motion_rig/figures/009_Figure_7.jpg]]
*Figure 7: Rigging and animation results with real-world point cloud sequences from DFaust (top) and KillingFusion [Slavcheva et al. 2017] (bottom). For each example, we show the target mesh and representative point cloud frames from the input sequence. We also show our motion-aware features (red rectangle), along with the resulting rigs and deformed meshes corresponding to the point cloud frames (see also our video for animated results: https://youtu.be/sPxfnQ8j07Y)*

2. **初始帧质量敏感。** 变形模块以第一帧为锚点进行迭代对齐。若第一帧点云严重损坏、遮挡严重或姿态极端，初始变形将不可靠，误差会沿帧传播并影响后续运动编码和绑定质量。

3. **蒙皮模型限制。** MoRig 仅支持线性混合蒙皮（LBS），无法处理需要非线性蒙皮或网格拓扑变化的变形场景（如衣物褶皱、肌肉膨胀）。

4. **点云质量依赖。** 方法需要单视角点云序列作为输入。高噪声、极端视角变化或严重遮挡会降低对应关系模块的匹配精度，进而影响运动估计和绑定结果。在 KillingFusion 序列的部分帧中，因深度传感器噪声导致点云稀疏，关节精确率有所下降。

5. **领域差异。** 训练完全依赖合成动画数据，尽管对 DFaust/KillingFusion 展现出一定泛化能力，但合成域与真实域在点云噪声分布、角色几何复杂度等方面的差异仍可能导致性能下降。论文未提供在更大规模真实数据上微调的结果，该方向的泛化边界有待进一步验证。

### 架构细节（补充参考）

Table 3–5 分别给出了对应模块、变形模块和运动编码器的详细网络架构。对应模块基于 GMEdgeConv 层（继承自 RigNet）编码点云与网格的几何及测地邻域特征；变形模块采用改进的 GMEdgeConv 分支结构，分别处理顶点位置和附加特征；运动编码器使用多头自注意力（N 个注意力头）配合可学习的 [CLS] token 聚合时序位移特征，最终输出 D 维运动感知特征向量。这些架构细节为复现提供了完整参考，但不影响上述实验结论的独立性。

![[assets/figures/papers/paper_list_l66_https_zhan_xu_github_io_motion_rig/figures/012_Table_3.jpg]]
*Table 3: Correspondence module details. ?? is the number of input points, ?? is the number of input vertices. Note that we do not require them to be fixed. GCU is the GMEdgeConv layer as RigNet, which encodes both geodesic and topological neighbors*

![[assets/figures/papers/paper_list_l66_https_zhan_xu_github_io_motion_rig/figures/006_Table_1.jpg]]
*Table 1: Comparison with other methods and MoRig variants*

![[assets/figures/papers/paper_list_l66_https_zhan_xu_github_io_motion_rig/figures/005_Figure_4.jpg]]
*Figure 4: Comparisons with previous methods for skeleton prediction. For each character, an animator-created skeleton is shown on the left as reference. With the help of motion information, our prediction captures articulated parts more accurately resulting in skeletons that agree more with the artist-made ones*

![[assets/figures/papers/paper_list_l66_https_zhan_xu_github_io_motion_rig/figures/010_Figure_8.jpg]]
*Figure 8: Vertex error wrt different number of input frames*

## 定位与知识库关联

MoRig 的核心定位是**将运动线索引入网格骨骼绑定流程**，改变了传统方法“仅从静态几何推断骨骼”的输入范式。在现有知识库中，该工作的直接挂载点是 **RigNet**（Xu et al., SIGGRAPH 2020）所代表的基于学习的自动绑定方法。MoRig 与 RigNet 的本质差异在于改变了**输入模态与特征来源**这一关键 slot：RigNet 仅接收单个静态网格，从纯几何特征（如顶点位置、法向、测地距离等）推断关节和蒙皮权重；MoRig 则额外引入表演角色的单视角点云序列，通过一个 Transformer 运动编码器将多帧顶点位移轨迹聚合为运动感知特征，与几何特征融合后共同驱动绑定预测。

这一 slot 改变带来了一条清晰的因果链：运动编码器提取的特征能够区分不同运动区域（如大臂与小臂的旋转中心），使得关节提取更准确——在 ModelsResource 测试集上，关节 Chamfer 距离相对 RigNet 降低 10%（3.9% → 3.5%），相对另一种无运动信息的 **SkeRig** 方法降低 53%（7.5% → 3.5%）；蒙皮权重 L1 误差相对 RigNet 降低 18%（0.39 → 0.32）；最终动画顶点距离误差相对 RigNet 降低 22.5%（3.1% → 2.4%）。在真实点云扫描数据（DFaust / KillingFusion）的泛化测试中，关节 IoU 从 RigNet 的 46.7% 提升至 65.7%，精度从 44.5% 提升至 70.0%，召回从 49.9% 提升至 62.2%，表明运动感知特征在域外数据上同样有效。

与另一基线 **SkeRig** 相比，MoRig 的差异不仅在于运动信息的有无，还在于整个绑定流程的端到端可学习性——SkeRig 的具体架构和训练方式在论文中未详细说明，但从 53% 的关节误差降幅来看，MoRig 的变形-编码-绑定联合优化策略显著优于该基线。

从方法论角度，MoRig 在知识库中的另一个挂载点是**基于 Transformer 的时序特征聚合**在 3D 视觉任务中的应用。其运动编码器采用可学习的 [CLS] 类 token 机制，对逐顶点位移序列进行多头注意力聚合，消融实验证实该设计优于平均池化和最大池化等简单聚合策略。这与 DETR、Point Transformer 等工作共享“用注意力替代手工归纳偏置”的设计哲学，但 MoRig 将其适配到了网格-点云跨模态运动编码这一特定场景。

**适用边界**方面，MoRig 存在几个明确的限制条件：第一，假设参考角色（点云序列中的表演者）与目标网格角色具有相似的底层关节结构——若目标网格存在点云序列中完全不可见的部件（如从未运动的尾巴），该方法将退化到纯几何推断，可能无法为该部件生成骨骼；第二，对初始点云帧的质量敏感，若第一帧损坏导致初始变形不可靠，整个流程会失败；第三，仅支持线性混合蒙皮（LBS），无法处理拓扑变化或高度非刚体变形；第四，训练依赖合成动画数据（ModelsResource 与 DeformThings4D），尽管对真实扫描展现出一定泛化能力，领域差异仍可能限制极端噪声或遮挡场景下的性能。

**后续启发**可从以下几个方向展开：在输入层面，可探索用多视角点云或单目 RGB 视频替代单视角点云，降低对点云质量和视角覆盖的依赖；在运动编码层面，Transformer 编码器输出的运动感知特征可迁移至运动风格迁移、跨角色动作重定向等下游任务；在绑定模型层面，将 LBS 扩展至非线性蒙皮模型（如 blend shapes 或神经隐式蒙皮）可处理更复杂的变形；在训练策略层面，引入更多真实扫描数据或域适应技术可进一步缩小合成-真实域差距。此外，如何处理点云序列中不可见部件的动态绑定（如从未运动的附属物）仍是一个开放问题，可能需要引入先验知识或生成式补全策略。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/MoRig_Motion_Aware_Rigging_of_Character_Meshes_from_Point_Clouds.pdf]]
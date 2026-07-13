---
title: "PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PointWorld_Scaling_3D_World_Models_for_In_The_Wild_Robotic_Manipulation.pdf
project_link: null
code_link: null
aliases:
- PointWorld
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将状态与动作统一表示为3D点流，剥离了与实施例相关的特征，只关注机器人与场景之间基于几何的物理交互，从而使得模型能够跨多种机器人和任务进行预训练。
primary_logic: 通过在共享的3D空间中以点流形式表示场景状态和机器人动作，并利用大规模点云骨干网络（PTv3）进行预测，可以构建一个与实施例无关的3D世界模型，该模型从部分观察的RGB-D中预测全场景动力学，并能直接在真实机器人上使用MPC进行零样本任务执行，无需任何演示或微调。
claims:
- 将状态和动作统一为3D点流，使得模型能够隐式学习物体分割、材质、关节和重力等物理属性，并通过密集损失稳定训练。
- 使用PTv3骨干网络实现了参数规模的大幅扩展（957×于GBND），同时保持实时推理，并在真实世界数据上获得了显著的ℓ2精度提升（0.0390→0.0312）。
- 在真实和模拟数据集上进行联合预训练，使单个模型能够零样本泛化到未见过的真实环境，并在微调后超越专门训练的模型。
- 在MPC框架下，预训练的POINTWORLD使Franka机器人能够零样本完成刚性推物、可变形、关节和工具使用等多种任务，成功率平均约70%。
---

# PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation

> [!tip] 核心洞察
> 通过在共享的3D空间中以点流形式表示场景状态和机器人动作，并利用大规模点云骨干网络（PTv3）进行预测，可以构建一个与实施例无关的3D世界模型，该模型从部分观察的RGB-D中预测全场景动力学，并能直接在真实机器人上使用MPC进行零样本任务执行，无需任何演示或微调。

| 字段 | 内容 |
|------|------|
| 中文题名 | PointWorld：面向野外机器人操作的规模化3D世界模型 |
| 英文题名 | PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.03782) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | POINTWORLD |
| Dataset | DROID, BEHAVIOR-1K, Held-out real scenes, Real-world push/grasp/deform/articulated |

> [!tip] 效果简介
> - DROID (moving points) 上，ℓ2 mover (m) 0.0312 (PTv3-1B) vs 0.0390 (GBND) (-0.0078 (absolute, ~20% relative improvement))。
> - BEHAVIOR-1K (in-domain) 上，ℓ2 mover (m) 0.0225 (POINTWORLD B→B) vs N/A (specialist not directly compared)。
> - Held-out real scenes (zero-shot) 上，ℓ2 mover (m) 0.0300 (D+B→H) vs 0.0531 (B→H, sim-only) (-43.5% relative)。

## 概要

**问题瓶颈：** 现有机器人世界模型难以在野外环境中泛化。它们通常依赖与特定机器人实施例绑定的状态表示（如关节空间）和低效的3D动态学习机制。更深层的瓶颈在于，缺乏大规模、高质量的3D交互数据来训练统一的物理动态模型，使得模型无法跨场景、跨任务迁移。

**核心方案：** 本文提出 **POINTWORLD**，一个大规模预训练的3D世界模型。其核心洞察是：将场景状态与机器人动作统一表示在共享的3D空间中的**3D点流**（3D point flows）。状态由RGB-D反投影的全场景点云构成，动作则通过URDF正向运动学转化为机器人表面点（仅抓取器）的密集3D轨迹。这种与实施例无关的表示剥离了外观和关节空间特征，迫使模型聚焦于基于几何的物理交互，从而能够跨多种机器人和任务进行预训练。

**关键结论：**
- **规模化骨干网络：** 采用 PointTransformerV3（PTv3）作为骨干，参数规模相比图神经网络基线 **GBND** 扩展了957倍，同时保持实时推理（约0.12秒），在DROID数据集上将移动点的ℓ2误差从0.0390降至0.0312（相对提升约20%）。
- **跨域零样本泛化：** 在真实和模拟数据集上联合预训练后，单个模型能够零样本泛化到未见过的真实环境，ℓ2误差从仅用模拟数据的0.0531降至0.0300（相对降低43.5%），微调后超越专门训练的模型。
- **真实世界任务执行：** 在MPC框架下，预训练的POINTWORLD使Franka机器人无需任何演示或微调，零样本完成刚性推物、可变形物体操作、关节物体操作和工具使用等多种任务，平均成功率约70%。
- **缩放规律验证：** 模型容量与数据量均呈现对数线性增益，表明该框架具备良好的规模化潜力。

**方法谱系与知识库定位：** POINTWORLD属于**基于模型的机器人学习**范畴，与视频生成式世界模型（如UniSim、Genie）不同，它直接在3D几何空间中进行动力学预测。其技术路线继承并突破了基于图网络的动力学模型（如**GBND**），将表示从对象级图节点提升为全场景点云，将骨干从GNN替换为大规模点云Transformer，并引入运动加权损失和任意不确定性正则化来处理真实数据噪声。在动作推理端，它将预训练世界模型嵌入MPPI规划器，实现了从感知到行动的闭环。



### 野外机器人操作的核心瓶颈

让机器人在开放、非结构化的野外环境中自主完成多样化的物理交互任务，是具身智能领域的终极目标之一。这要求机器人具备一个强大的**内部世界模型**——能够根据当前观察和自身动作，预测未来场景的演化。然而，现有方法面临三重根本性挑战：

1.  **实施例依赖性**：传统世界模型通常将状态和动作表示为关节空间配置、末端执行器姿态或2D轨迹，这些表示与特定机器人的运动学结构和传感器配置深度耦合，导致模型无法跨不同机器人平台进行泛化。
2.  **低效的3D动力学学习**：主流方法如**GBND**（图神经网络动力学模型）依赖基于对象或图的稀疏表示，难以从部分可观察的RGB-D输入中学习到全场景的密集物理交互，且参数扩展性受限。
3.  **大规模3D交互数据的匮乏**：在真实世界中获取高质量、带标注的3D交互数据成本极高，现有数据集规模远不足以训练一个能够捕捉丰富物理规律（如物体分割、材质属性、关节约束、碰撞响应）的统一动力学模型。

### 现有方法的缺口

现有机器人世界模型的研究通常沿着两条路径展开：一是基于特定实施例的关节空间预测，二是基于2D图像的视频生成。前者缺乏跨平台的通用性，后者虽然视觉表现力强，但在3D几何一致性和物理准确性上存在根本缺陷。更关键的是，这些方法都未能有效利用**3D点云所蕴含的丰富几何监督信号**——一个能够同时隐式编码物体边界、接触状态和运动模式的表示空间。

### POINTWORLD的动机与核心洞察

POINTWORLD的提出源于一个简洁而深刻的洞察：**物理交互的本质是机器人与场景之间在共享3D空间中的几何接触与运动传递**。如果能够将状态和动作统一表示为与实施例无关的3D点流（3D point flows），就可以剥离关节空间、传感器配置等特异性信息，仅保留交互所需的纯几何信息。这使得模型能够：

-   从任意机器人的RGB-D观察和URDF描述中提取统一的点云表示；
-   利用大规模点云骨干网络（如PointTransformerV3）进行高效的全场景动力学预测；
-   通过密集的逐点运动监督，隐式学习分割、材质、关节、重力等物理属性；
-   在多个数据集和机器人平台上进行联合预训练，实现零样本任务执行。

这一设计将3D世界建模从“特定任务、特定机器人的动力学拟合”提升为“通用物理交互的几何预测”，为野外机器人操作开辟了一条可扩展的技术路径。



## 核心方法与创新机理

POINTWORLD的核心突破在于将机器人世界模型从“实施例依赖的特定表示”中解放出来，构建了一个**统一的、与实施例无关的3D交互几何空间**。其关键创新可归结为以下四个维度的根本性改变：

### 1. 状态-动作统一表示：3D点流

传统方法（如基于图神经网络的**GBND**）通常将状态编码为对象图或节点特征，将动作表示为关节空间命令或末端执行器位姿。POINTWORLD彻底抛弃了这一范式，将**状态与动作统一为同一3D空间中的点流**：
- **状态**：从RGB-D反投影得到的全场景3D点云 $\mathbf{s}_{t} = \{ (\mathbf{p}_{t,i}, \mathbf{f}_i^{S}) \}_{i=1}^{N_S}$，无任何对象先验或分割
- **动作**：通过URDF正运动学生成的机器人表面点流 $\{ (\mathbf{r}_{t+k,j}, \mathbf{f}_{t+k,j}^{R}) \}_{j=1}^{N_R}$，仅使用抓取器点，剥离了关节空间等实施例特征

这一设计使得模型只关注**机器人与场景之间的几何接触与物理交互**，从而天然具备跨机器人和跨任务的泛化能力。消融实验（Figure 11）证实，仅使用抓取器点流作为动作表示效果最佳，且能实现跨异质实施例的正向迁移。

### 2. 骨干网络的大规模扩展：从GNN到PTv3

POINTWORLD将骨干网络从图神经网络替换为**PointTransformerV3 (PTv3)**，采用U-Net层次结构处理拼接后的场景-机器人点云。这一替换带来了质的飞跃：
- 参数规模扩展至GBND的**957倍**（Table 1）
- 在DROID测试集上，ℓ2误差从0.0390降至**0.0312**（约20%的相对提升）
- 推理延迟保持在约**0.12秒**（PTv3-1B），满足实时性要求

缩放研究（Figure 9）进一步揭示，模型大小与数据量均呈现**对数线性增益**，验证了规模化路线的可行性。

### 3. 训练目标的重新设计：运动加权与不确定性正则化

为处理真实世界数据中的噪声和稀疏交互信号，POINTWORLD设计了全新的训练目标：
- **运动加权Huber损失**：通过软运动似然 $m_{k,i} = \sigma(\kappa(\delta_{k,i} - \tau))$ 计算逐点权重，使训练聚焦于实际移动的场景点
- **任意不确定性正则化**：预测点级对数方差 $s_{k,i}$，自适应平衡残差与不确定性惩罚

完整目标函数为：
$$\frac 1 2 \sum_{k,i}^{H,N_S} w_{k,i} \left( \rho_{\delta}(\hat{\mathbf{P}}_{t+k,i} - \mathbf{P}_{t+k,i}) e^{-s_{k,i}} + s_{k,i} \right)$$

这一设计（Figure 4）有效稳定了在真实噪声数据上的训练，使得模型能够隐式学习物体分割、材质、关节和重力等物理属性（Figure 3）。

### 4. 分块多步预测：训练与推理的一致性

传统方法通常采用单步预测，在长时域推理中累积严重漂移。POINTWORLD采用**分块多步预测**：
$$\mathcal{F}_{\theta}^{H} : (\mathbf{s}_{t}, \mathbf{a}_{t:t+H-1}) \to \mathbf{S}_{t+1:t+H}$$

单次前向传播预测 $H=10$ 步未来状态，训练与推理策略一致。消融实验（Figure 12）表明，分块预测显著减少了漂移并降低了计算量。

### 创新总结

上述四个维度的改变构成了一个完整的创新链条：**统一表示**剥离了实施例依赖，**规模化骨干**提供了强大的学习容量，**鲁棒目标**稳定了真实数据训练，**分块预测**保证了长时域一致性。这一组合使得单个预训练模型能够在未见过的真实环境中，通过MPC实现零样本任务执行，平均成功率约70%（Figure 8），覆盖刚性推物、可变形物体、关节物体和工具使用等多种任务类型。



POINTWORLD 的核心设计理念是将机器人世界建模重新定义为**以动作为条件的全场景3D点流预测**问题。其整体流程围绕一个统一的3D点云表示展开，该表示同时承载场景状态和机器人动作，从而剥离了与特定实施例（如关节空间、末端执行器类型）相关的特征，使模型能够专注于基于几何的物理交互。

### 输入模态与统一表示

系统的输入由三部分组成：
1. **多视角RGB-D观测**：来自已标定相机的RGB图像和深度图。
2. **机器人关节空间动作**：控制指令序列，通常为末端执行器轨迹。
3. **机器人描述文件（URDF）**：提供机器人的运动学模型。

这些异构输入被转换为统一的**3D点流**表示：
- **场景状态** $\mathbf{s}_t$ 表示为一组带有时间常数特征的3D点云 $\{(\mathbf{p}_{t,i}, \mathbf{f}_i^S)\}_{i=1}^{N_S}$，从RGB-D反投影生成，不依赖任何对象先验或分割。
- **机器人动作** 表示为一组随时间演化的3D点流 $\{(\mathbf{r}_{t+k,j}, \mathbf{f}_{t+k,j}^R)\}_{j=1}^{N_R}$，通过正运动学从URDF和关节配置传播机器人表面点（仅抓取器点）生成。

### 特征提取与融合

场景点和机器人点分别通过不同的特征提取管线进行处理：
- **场景点特征化**：将场景点投影到各相机视图，从冻结的DINOv3编码器中提取多层特征，并聚合为逐点特征。这一设计利用了预训练2D视觉基础模型的强大先验，为3D世界建模提供了关键的语义和几何线索。
- **机器人点特征化**：为机器人点添加时序嵌入（temporal embedding），以编码动作的时间信息。

随后，场景点云与机器人点云被**拼接为单个点云**，作为骨干网络的统一输入。这种拼接方式使得模型能够在一个共享的3D空间中同时感知场景几何和机器人动作几何，从而隐式地推理接触、碰撞和物体运动。

### 骨干网络与预测头

拼接后的点云被送入**PointTransformerV3（PTv3）**骨干网络。PTv3采用U-Net层次结构，支持大规模参数扩展（实验中扩展至1B参数，为基线GBND的957倍），同时保持实时推理能力（约0.12秒）。骨干网络提取全局-局部特征后，一个**共享的MLP预测头**输出每个场景点在每个未来时间步的位移。

### 分块多步预测

与传统的单步自回归预测不同，POINTWORLD采用**分块多步预测**策略：单次前向传播预测未来 $H=10$ 步的全场景状态：
$$\mathcal{F}_{\theta}^{H} : (\mathbf{s}_{t}, \mathbf{a}_{t:t+H-1}) \to \mathbf{S}_{t+1:t+H}$$

这种设计在训练和推理时保持一致，有效减少了自回归rollout中的累积漂移，并降低了计算开销。

### 训练目标

训练目标采用**运动加权Huber损失 + 任意不确定性正则化**：
$$\frac 1 2 \sum_{k,i}^{H,N_S} w_{k,i} \left( \rho_{\delta}(\hat{\mathbf{P}}_{t+k,i} - \mathbf{P}_{t+k,i}) e^{-s_{k,i}} + s_{k,i} \right)$$

其中运动权重 $w_{k,i}$ 通过软运动似然 $m_{k,i} = \sigma(\kappa(\delta_{k,i} - \tau))$ 计算并归一化，使训练聚焦于实际发生移动的场景点（如被推动的物体），而忽略静态背景。预测的对数方差 $s_{k,i}$ 则用于平衡残差与不确定性惩罚，处理真实数据中的标注噪声。

### 行动推理：MPC框架

在部署阶段，POINTWORLD作为动力学模型嵌入**模型预测控制（MPC）**框架中。给定初始场景状态和任务目标（由人工指定的任务点与目标位置），系统通过嵌入式MPPI规划器优化末端执行器轨迹，最小化任务代价（目标点与指定位置之间的平方距离）与控制代价（路径长度和可达性正则化）：
$$\arg\min \sum_{k=1}^T \left[ c_{\mathrm{task}}(\mathbf{s}_k) + c_{\mathrm{ctrl}}(\mathbf{E}_k) \right] \; \mathrm{s.t.} \; \mathbf{s}_{1:T} = \mathcal{F}_{\theta}^T(\mathbf{s}_0, \mathbf{a}_{1:T}), \; \mathbf{E}_0 = \mathbf{E}_{\mathrm{measured}}$$

这一框架使预训练的POINTWORLD能够在真实机器人上实现零样本任务执行，无需任何演示或微调。

### 补充图表

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/002_Figure_2.jpg]]
*Figure 2: Overview of POINTWORLD. Given calibrated RGB-D, robot joint-space actions, and a robot description file (URDF), we convert actions to robot flows and concatenate with scene to form a single point cloud serving as an embodiment-agnostic interaction geometry. Scene points are featurized with a frozen DINOv3 encoder, robot points with temporal embeddings, and a point cloud backbone predicts full-scene 3D point flows*



### 3D世界建模的形式化

POINTWORLD将3D世界建模形式化为**动作条件化的全场景3D点流预测**。与传统的单步动力学更新不同，该方法采用**分块多步（chunked）**预测范式：模型在单次前向传播中预测未来H步的场景状态，而非逐步自回归展开。这一设计在训练和推理时保持一致，显著减少了长时域预测中的漂移累积。

具体而言，给定当前场景状态 $\mathbf{s}_t$ 和未来H步的动作序列 $\mathbf{a}_{t:t+H-1}$，世界模型 $\mathcal{F}_{\theta}^{H}$ 直接输出未来状态序列：

$$\mathcal{F}_{\theta}^{H} : (\mathbf{s}_{t}, \mathbf{a}_{t:t+H-1}) \to \mathbf{S}_{t+1:t+H}$$

其中场景状态 $\mathbf{s}_t$ 被表示为一组携带时间常数特征的3D点流：

$$\mathbf{s}_{t} = \{ (\mathbf{p}_{t,i}, \mathbf{f}_i^{S}) \}_{i=1}^{N_S}$$

机器人动作同样被表示为随时间演化的3D点流，通过URDF模型和关节配置经由正运动学传播生成：

$$\{ (\mathbf{r}_{t+k,j}, \mathbf{f}_{t+k,j}^{R}) \}_{j=1}^{N_R}$$

这种统一表示的核心洞察在于：**剥离了与实施例相关的特征，仅保留机器人与场景之间基于几何的物理交互信息**，使得模型能够跨多种机器人和任务进行预训练。

### 核心模块拆解

POINTWORLD的完整推理管线由以下关键模块构成：

**深度估计与点云生成**：从标定后的RGB-D数据出发，将传感器深度替换为Foundation-Stereo估计的立体深度，通过反投影生成全场景3D点云。这一步骤是后续所有几何推理的基础。

**机器人点流生成**：根据URDF描述文件和关节空间动作，通过正运动学传播机器人表面点（仅抓取器点），生成与实施例无关的动作表示。消融实验证实，仅使用抓取器点流作为动作表示效果最佳，且能跨异质实施例正向迁移。

**DINOv3场景特征提取**：将场景点投影到各相机视图，从冻结的DINOv3编码器中提取多层特征，并聚合为逐点特征。预训练的2D视觉特征为3D几何理解提供了关键的语义先验。

**时序嵌入与特征拼接**：为机器人点添加时序嵌入以区分不同时间步的动作，随后将场景点与机器人点拼接成单个点云，作为骨干网络的统一输入。

**PTv3骨干网络**：采用PointTransformerV3（PTv3）的U-Net层次结构处理拼接点云，提取全局-局部特征。该骨干网络相比图神经网络基线（GBND）实现了957倍的参数规模扩展，同时保持实时推理能力（PTv3-1B约0.12秒延迟）。

**位移预测头**：共享的MLP头输出每个场景点在每个未来时间步的位移向量，完成从静态点云到全场景动力学的端到端预测。

### 关键损失函数设计

POINTWORLD的训练目标针对真实世界数据的噪声特性和物理交互的稀疏性进行了专门设计。核心损失函数为**运动加权的Huber损失**，并引入**任意不确定性正则化**：

$$\frac{1}{2} \sum_{k,i}^{H,N_S} w_{k,i} \left( \rho_{\delta}(\hat{\mathbf{P}}_{t+k,i} - \mathbf{P}_{t+k,i}) e^{-s_{k,i}} + s_{k,i} \right)$$

其中各变量的含义如下：

- **$w_{k,i}$**：归一化的运动权重，通过软运动似然函数计算。该权重使训练聚焦于实际发生位移的场景点，避免静态背景点主导梯度更新。
- **$\rho_{\delta}(\cdot)$**：Huber损失函数，在L1和L2之间平滑过渡，对小误差使用L2以获得平滑梯度，对大误差使用L1以增强对离群点的鲁棒性。
- **$s_{k,i}$**：模型预测的点级对数方差，用于建模任意不确定性。损失函数中 $e^{-s_{k,i}}$ 项自动降低高噪声区域的权重，而 $+s_{k,i}$ 项防止模型对所有点预测无限大方差。

运动权重 $w_{k,i}$ 由软运动似然 $m_{k,i}$ 归一化得到：

$$m_{k,i} = \sigma(\kappa(\delta_{k,i} - \tau))$$

$$w_{k,i} = m_{k,i} / \sum_{k,i} m_{k,i}$$

其中 $\delta_{k,i}$ 为点i在时间步k的真实位移范数，$\tau$ 为运动阈值，$\kappa$ 为温度参数控制软阈值锐度，$\sigma(\cdot)$ 为sigmoid函数。这一设计使得模型能够隐式学习物体分割、材质、关节和重力等物理属性——因为要准确预测全场景演化，模型必须识别哪些点属于可移动物体、理解接触约束和运动传递关系。

### MPC行动推理

在行动推理阶段，POINTWORLD作为嵌入式MPPI（Model Predictive Path Integral）规划器中的动力学模型，优化末端执行器轨迹。优化问题形式化为：

$$\arg\min \sum_{k=1}^T \left[ c_{\mathrm{task}}(\mathbf{s}_k) + c_{\mathrm{ctrl}}(\mathbf{E}_k) \right] \quad \mathrm{s.t.} \quad \mathbf{s}_{1:T} = \mathcal{F}_{\theta}^T(\mathbf{s}_0, \mathbf{a}_{1:T}), \quad \mathbf{E}_0 = \mathbf{E}_{\mathrm{measured}}$$

其中任务代价 $c_{\mathrm{task}}$ 定义为目标场景点与指定目标位置之间的平方距离：

$$c_{\mathrm{task}}(\mathbf{s}_k) = \frac{1}{|\mathcal{Z}_{\mathrm{task}}|} \sum_{i \in \mathcal{T}_{\mathrm{task}}} \| \mathbf{p}_{k,i} - \mathbf{g}_i \|_2^2$$

控制代价 $c_{\mathrm{ctrl}}$ 包含路径长度和可达性正则化项，确保生成的轨迹平滑且符合机器人的运动学约束。这一框架使得预训练的POINTWORLD能够零样本完成刚性推物、可变形物体操作、关节物体交互和工具使用等多种任务，无需任何演示或微调。

### 补充图表

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/003_Figure_3.jpg]]
*Figure 3: Rich Supervision of 3D World Modeling for Physical Interactions, when conditioned on 3D robot point flows and partial observable RGB-D. The 3D world modeling objective enjoys dense pixel-level supervision while encoding a wide range of capabilities central to robotic manipulation. To predict full-scene evolution, the model needs to implicitly segment objects of interest, identify material property and/or articulation structure, perform implicit shape completion for contact reasoning, propagate robot-object interaction for object-object dynamics, and simultaneously considering the effects of gravity, encapsulated all in a single forward pass of the learned model*

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/004_Figure_4.jpg]]
*Figure 4: Movement Weighting and Uncertainty Regularization, where the robot releases and drops a yellow cloth. (Bottom Left) The movement weighting, used in the training objective, effectively biases the training towards scene points that are moving at each timestep, computed with the ground-truth flows. (Bottom Right) The uncertainty value, predicted by the model without any ground-truth, regularizes training to prevent overfitting to points that have unreliable ground-truth. Intriguingly, we observe that it also emerges to capture action-conditioned uncertainty arising from the object’s physical properties (e.g., larger variability along the edge of the cloth)*

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/012_Figure_11.jpg]]
*Figure 11: Action representations. Representing actions as point flows on grippers balances effective, efficient contact reasoning and enables positive transfer across heterogeneous embodiments*

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/014_Figure_12.jpg]]
*Figure 12: Ablation on Chunked Prediction, where we study different rollout strategies in training and testing. Chunked rollouts at both training and inference time lead to significantly less drift than other baselines while amortizing compute with only a single forward pass of the model*



## 实验与关键发现

### 评估协议与指标

POINTWORLD 的评估围绕其作为 3D 动力学预测器的核心能力展开。论文采用 **ℓ₂ mover** 作为主要量化指标，该指标计算预测时间窗口内所有**发生运动**的场景点在每个时间步上的逐点 ℓ₂ 距离。这一设计避免了静态背景点主导损失，从而更精确地衡量模型对物理交互的建模能力。所有实验均在固定训练/测试划分上进行，真实世界数据的标注质量通过专家置信度过滤进行控制。

### 骨干网络与规模化路线图

Table 1 展示了不同骨干网络的性能对比，核心发现是 **PTv3** 在参数规模与精度上均显著优于先前基于图神经网络的 **GBND**。PTv3-1B 的参数量达到 GBND 的 957 倍，但推理延迟仅约 0.12 秒，保持了实时性。在 DROID 测试集上，ℓ₂ mover 从 GBND 的 0.0390 降至 PTv3-1B 的 0.0312，相对提升约 20%。

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/010_Table_1.jpg]]
*Table 1: Backbone Comparisons. PTv3 [152] enables massive parameter scaling while retaining similar memory and efficient inference (latency in milliseconds, PTv3-1B ≈ 0.12 s)*

Figure 7 进一步揭示了规模化路线图中的关键增益来源：从基础架构升级到 PTv3、引入运动加权与不确定性正则化、添加冻结的 DINOv3 特征，以及扩大数据规模，每一步都带来了一致的精度提升。Figure 9 的缩放研究则表明，无论是模型参数量还是训练数据量，均呈现**对数线性**的增益趋势，验证了 POINTWORLD 的规模化潜力。

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/007_Figure_7.jpg]]
*Figure 7: Roadmap for Scaling 3D World Models, measured by*

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/008_Figure_9.jpg]]
*Figure 9: Scaling Study. Scaling POINTWORLD in either data or model size yields roughly log-linear gains in prediction accuracy*

### 跨域泛化与零样本迁移

Table 2 系统评估了 POINTWORLD 的泛化能力。在 BEHAVIOR-1K 仿真域内（B→B），模型取得了 0.0225 的 ℓ₂ mover。更具挑战性的是跨域零样本泛化：仅在仿真数据上训练的模型迁移到真实场景（B→H）时，ℓ₂ mover 高达 0.0531；而联合 DROID 真实数据与 BEHAVIOR-1K 仿真数据预训练后（D+B→H），误差降至 0.0300，相对降低 43.5%。值得注意的是，在该真实场景上进行有监督微调后（D+B→H ft），误差进一步降至 0.0280，超越了从头训练的专用模型（0.0332）。Figure 10 以搬运反光玻璃瓶为例，定性地展示了零样本与微调后的 rollout 质量差异。

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/011_Figure_10.jpg]]
*Figure 10: Zero-Shot and Finetuned Generalization to Held-Out Real-World Scenes, where the robot transports a reflective glass bottle. POINTWORLD pre-trained on DROID or jointly on DROID and BEHAVIOR (D+B) are capable of zero-shot generalizing to unseen environment and motion from a held-out DROID lab’s scene, closing the gap to the specialist variant trained on that lab’s data. POINTWORLD pre-trained on only simulation data fail to generalize zero-shot. Further finetuning yields more accurate object trajectories of grasped objects*

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/013_Table_2.jpg]]
*Table 2: Generalization of POINTWORLD across in-domain, cross-domain, heldout real environments under zero-shot and finetuned settings. D denotes DROID, B denotes B1K, H denotes held-out real-world scenes. “From Scratch” denotes specialist trained on the held-out lab’s data. Evaluations are done on unseen samples from the corresponding dataset. POINTWORLD generalizes within domains, zero-shot transfers to unseen real-world environments, surpasses specialists if finetuned with 20x fewer updates, and benefits from real-sim co-training*

### 真实世界零样本操控

在真实机器人实验中，POINTWORLD 被嵌入 MPC 框架（MPPI 规划器），直接作为动力学模型使用，无需任何任务演示或微调。Figure 8 展示了 Franka 机器人在 8 项野外任务上的零样本成功率：

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/009_Figure_8.jpg]]
*Figure 8: Real-World Action Inference. POINTWORLD runs zero-shot with MPC for rigid, deformable, articulated, and tool-use tasks in the wild. Success rates are on top*

- **刚性物体**：TissueBox 推动 80%，Book 推动 70%
- **可变形物体**：ScarfFold 折叠 60%，PillowPlace 放置 50%
- **关节物体**：Microwave 开门 30%，DrawerClose 关抽屉 70%
- **工具使用**：DusterSweep 清扫 70%，BroomSweep 清扫 50%

平均成功率约 70%，但在需要精确接触推理的任务（如微波炉开门）上表现明显下降，这揭示了模型在处理小接触面、高精度关节约束时的局限性。

### 消融研究

**动作表示**（Figure 11）：对比了全臂点流、末端执行器位姿、抓取器点流等不同动作表示。结果表明，仅使用抓取器点流作为动作表示效果最佳，且能在异质机器人实施例之间实现正向迁移。这验证了“实施例无关”设计的核心假设——只需保留与接触相关的几何信息即可。

**分块预测策略**（Figure 12）：对比了训练与测试阶段不同的 rollout 策略。在训练和推理中均使用分块预测（chunked），可显著减少累积漂移，并降低单步推理的计算量。这证实了多步一致性训练的必要性。

**部分可观察性鲁棒性**（Figure 13）：训练时随机化相机数量（模拟不同的遮挡和视野条件），使模型在测试时对不同相机配置具有更强的鲁棒性，验证了该数据增强策略对野外部署的价值。

### 失败模式与局限性

1. **精细操作与高精度约束**：在微波炉开门等任务中成功率仅 30%，模型难以精确推理小接触面的物理交互。
2. **完全动态初始条件**：当前模型仅预测场景点的位移，无法生成新点或处理流体、碎裂等拓扑变化场景。
3. **目标指定依赖人工**：MPC 中的任务代价需要人工指定目标点或区域，缺乏自动化的语义目标理解。
4. **物理一致性无保证**：模型不显式融合物理先验（如接触力学、动量守恒），在极端情况下可能违反物理规律。
5. **标注噪声残留**：尽管采用了优化的 3D 标注流程（Figure 5），在精细小物体和复杂遮挡场景下仍存在标注挑战，训练时依赖不确定性正则化来缓解。

### 数据预处理与训练配置

Table 3 至 Table 5 汇总了关键的数据预处理与训练配置。数据集总计约 200 万条轨迹、500 小时，涵盖 DROID 真实数据和 BEHAVIOR-1K 仿真数据。预处理中，传感器深度被替换为 Foundation-Stereo 估计的立体深度，相机外参经过优化后中位平移误差 1.8 cm、旋转误差 1.9°。训练采用运动加权的 Huber 损失与任意不确定性正则化，分块预测长度 H=10，并应用随机相机数量增强。

### 补充图表

![[assets/figures/papers/paper_list_l2645_https_arxiv_org_abs_2601_03782/figures/015_Figure_13.jpg]]
*Figure 13: Ablation on Partial Observability, where we train variants of POINTWORLD with varying number of cameras and evaluate them on all settings at test time. POINTWORLD is robust to different levels of partial observability and benefits from additional cameras in both training and inference. Training with randomized camera counts yields the best performance across all test settings*



## 定位与知识库关联

### 1. 方法谱系：从特定实施例建模到通用3D世界模型

POINTWORLD的核心突破在于将机器人世界模型从“与实施例强耦合”的范式推向“与实施例无关”的通用物理交互建模。现有世界模型通常依赖关节空间状态、对象中心图或2D轨迹作为状态-动作表示，这使其难以跨机器人平台和任务泛化。POINTWORLD通过将状态和动作统一为**3D点流**，剥离了与特定机器人形态相关的特征，只保留机器人与场景之间基于几何的物理交互信息。

**与基线方法的对比**：在骨干网络层面，POINTWORLD将基线模型**GBND**（基于图神经网络的动力学模型）替换为**PointTransformerV3 (PTv3)**，实现了参数规模的大幅扩展（957倍于GBND），同时保持实时推理能力（PTv3-1B延迟约0.12秒）。Table 1显示，这一替换使DROID数据集上的ℓ2 mover指标从0.0390降至0.0312，相对提升约20%。在表示层面，POINTWORLD用全场景3D点云（从RGB-D反投影得到，无对象先验）替代了基于对象或图的表示，并用来自URDF的机器人点流（仅抓取器点）替代了关节空间命令或末端执行器姿态。Figure 11的消融实验证实，仅使用抓取器点流作为动作表示效果最佳，且能跨异质实施例实现正向迁移。

**损失函数与训练策略的演进**：POINTWORLD将标准L2损失升级为**运动加权Huber损失 + 任意不确定性正则化**（Equation 1），有效聚焦于场景中实际运动的点，并处理真实数据中的标注噪声。Figure 4展示了该损失在机器人释放并掉落黄色布料场景中的效果——运动加权将训练重心偏向移动点，不确定性正则化则自动降低高噪声区域的权重。此外，POINTWORLD采用**分块多步预测**（H=10步）替代单步预测，Figure 12表明这一策略在训练和推理中的一致性显著减少了长时域预测的漂移。

### 2. 知识库定位：大规模预训练与零样本行动推理

POINTWORLD将3D世界模型定位为一种**可预训练的基础模型**，其知识来源于大规模多源数据集（约200万条轨迹、500小时）的联合训练。Table 2显示，在模拟数据（BEHAVIOR-1K）和真实数据（DROID）上进行联合预训练后，单个模型能够零样本泛化到未见的真实环境（held-out real scenes），ℓ2 mover从纯模拟训练的0.0531降至0.0300（相对降低43.5%），并在微调后超越专门训练的模型（0.0300 vs 0.0332）。

**缩放规律**：Figure 9揭示了模型大小和数据量均呈对数线性增益的缩放规律，表明POINTWORLD的架构和训练范式具备持续扩展的潜力。Figure 7的扩展路线图进一步量化了逐步改进骨干、目标函数、视觉特征和训练规模带来的累积精度提升。

**零样本行动推理**：POINTWORLD在MPC框架下实现了真正的零样本任务执行——无需任何演示或微调。Figure 8显示，预训练模型使Franka机器人能够完成刚性推物（TissueBox 80%）、可变形物体（ScarfFold 60%）、关节物体（DrawerClose 70%）和工具使用（DusterSweep 70%）等多种任务，平均成功率约70%。这一能力源于模型在3D点流预测中隐式学习到的物理属性（物体分割、材质、关节、重力等，如Figure 3所示），以及MPC优化框架中任务代价函数（Equation 2）的灵活指定。

### 3. 适用边界与局限性

尽管POINTWORLD展示了令人瞩目的泛化能力，其适用边界和局限性同样明确：

**表示层面的限制**：当前模型仅预测场景点的位移（即点流），不能直接生成新的点或处理完全动态的初始条件（如流体、易碎物体的碎裂）。这意味着模型本质上是一个“点跟踪器”而非“点生成器”，在涉及拓扑变化或新表面暴露的场景中可能失效。

**行动推断的依赖**：零样本MPC的成功严重依赖人工指定的任务点或目标位置（通过Equation 2中的$c_{\mathrm{task}}$）。模型本身不具备自动设计奖励函数或理解高层任务语义的能力，这限制了其在非结构化任务中的自主性。

**数据与标注的约束**：尽管POINTWORLD的3D标注管线（使用FoundationStereo深度估计和优化后的外参，Figure 5）相比DROID原始发布版本有显著提升（中位平移误差1.8 cm，旋转误差1.9度），但在精细小物体和复杂遮挡场景下仍面临挑战。真实数据集的规模和多样性也受限，训练数据主要来自预录制数据集DROID和BEHAVIOR-1K，可能无法完全覆盖所有野外环境。

**物理合理性的缺失**：模型不显式融合物理先验（如接触力学、动量守恒），可能在极端情况下违反物理规律。当前仅支持刚性机器人链接，无法处理软体机器人或变形链接。

**硬件平台的单一性**：真实机器人实验仅在Franka平台上进行，且任务目标通过人机交互指定，其在其他机器人平台上的可迁移性需要进一步验证。

### 4. 开放问题与未来方向

基于上述局限性，POINTWORLD开启了若干关键研究方向：

1. **动态初始条件扩展**：如何将点流世界模型扩展到具有完全动态初始条件的环境（如流体模拟、易碎物体交互）？这可能需要引入点生成机制或混合表示。

2. **自动化目标指定**：能否从视觉语言模型（VLM）自动指定MPC中的任务代价或目标位置，以实现完全自主的操作任务？这将消除当前对人机交互的依赖。

3. **物理先验融合**：如何将显式物理定律（如接触力学、刚体动力学）融入学习框架，以提高预测的物理合理性？一种可能路径是在损失函数中引入物理约束项，或采用物理信息神经网络（PINN）的架构设计。

4. **数据与模型扩展**：Figure 9的缩放规律暗示了进一步扩展的巨大潜力——如何系统性地扩展数据集（覆盖更多场景多样性、机器人平台和长时域任务）和模型规模，以持续提升泛化能力？

5. **范式迁移**：能否将点流世界模型用于更广泛的机器人学习范式？例如，作为离线强化学习中的动力学模型，或为策略训练提供高保真模拟环境。POINTWORLD与实施例无关的特性使其天然适合作为跨平台策略学习的基础。

**需要人工验证的点**：关于GBND的具体作者、会议和年份信息在提供的分析材料中未明确给出，建议查阅原始论文以补充完整的引用元数据。



## 原文 PDF

![[paperPDFs/CVPR_2026/PointWorld_Scaling_3D_World_Models_for_In_The_Wild_Robotic_Manipulation.pdf]]

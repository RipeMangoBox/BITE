---
title: "Zero-Shot 4D Lidar Panoptic Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Zero_Shot_4D_Lidar_Panoptic_Segmentation.pdf
code_link: null
project_link: https://research.nvidia.com/labs/dvl/projects/sal4d
aliases:
- S4SAL4
- ZS4LPS
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用多模态传感器（摄像机+LiDAR）作为桥梁，将视频对象分割（VOS）和视觉-语言基础模型（CLIP）蒸馏到LiDAR空间，通过短时间窗口的可靠伪标签生成与跨窗口关联，建立时空连续的自监督训练信号。"
primary_logic: "通过滑动时间窗口内的VOS传播与CLIP特征提取，后续利用精确的3D-IoU跨窗口关联和时空平整化（flatten），可为任意长序列生成时空一致的实例级伪标签；在这些噪声但去相关的伪标签上训练，能够蒸馏出具有零样本识别能力的端到端4D激光雷达分割模型。"
claims:
- "SAL-4D在3D零样本激光雷达全景分割上超越先前方法超过5 PQ。"
- "跨窗口关联使LSTQ提升1.9个百分点，并显著改善零样本识别（S_cls +2.6）。"
- "时空一致伪标签相比单帧伪标签，语义识别相对提升15% PQ，分割质量相对提升20% mIoU。"
- "SAL-4D在SemanticKITTI 4D-LPS上达到42.2 LSTQ，约为顶级监督方法的59%。"
---

# Zero-Shot 4D Lidar Panoptic Segmentation

> [!tip] 核心洞察
> 通过滑动时间窗口内的VOS传播与CLIP特征提取，后续利用精确的3D-IoU跨窗口关联和时空平整化（flatten），可为任意长序列生成时空一致的实例级伪标签；在这些噪声但去相关的伪标签上训练，能够蒸馏出具有零样本识别能力的端到端4D激光雷达分割模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 零样本4D激光雷达全景分割 |
| 英文题名 | Zero-Shot 4D Lidar Panoptic Segmentation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2504.00848) · [Project](https://research.nvidia.com/labs/dvl/projects/sal4d) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SAL-4D (Segment Anything in Lidar–4D) |
| Dataset | SemanticKITTI (4D-LPS, zero-shot), Panoptic nuScenes (4D-LPS, SemanticKITTI (3D-LPS, zero-shot, frustum), full point cloud) |

> [!tip] 效果简介
> - SemanticKITTI (4D-LPS, zero-shot) 上，LSTQ 为 42.2，对比 30.3 (SW zero-shot baseline)，变化 +11.9。
> - Panoptic nuScenes (4D-LPS, zero-shot) 上，LSTQ 为 45.0，对比 30.3 (SW zero-shot baseline)，变化 +14.7。
> - SemanticKITTI (3D-LPS, zero-shot, frustum) 上，PQ 为 38.2，对比 33.1 (SAL)，变化 +5.1。

## 概要

### 问题与瓶颈

4D激光雷达全景分割要求对点云序列中的每个点同时进行**实例分割、时序关联与语义识别**。现有方法依赖大量人工标注数据，且类别词汇固定，无法泛化至训练时未见的新对象。核心瓶颈在于：**人工标注的4D激光雷达数据稀缺且类别词汇封闭**，限制了方法对任意新对象进行时空一致分割和识别的能力。

### 核心思路

SAL-4D（Segment Anything in Lidar–4D）提出了一条**无需任何语义标注**的零样本学习路径。其关键洞察是：利用多模态传感器（摄像机+LiDAR）作为桥梁，将视频对象分割（VOS）和视觉-语言基础模型（CLIP）的能力蒸馏到LiDAR空间。具体而言，通过**短时间窗口内的可靠伪标签生成**与**跨窗口关联**，建立时空连续的自监督训练信号，使模型能够端到端地学习4D实例分割，并在测试时通过文本提示实现零样本识别（Figure 1）。

### 方法定位

该方法属于**自监督蒸馏型零样本4D全景分割**范式。与仅处理单帧点云的零样本方法（如SAL）不同，SAL-4D直接在点云序列上联合完成分割、跟踪与识别。其核心架构由两部分构成：

- **多模态伪标签引擎**（Figure 2）：通过Track–Lift–Flatten流水线，在滑动时间窗口内利用SAMv2进行视频对象传播，经LiDAR-相机投影提升到3D空间，再通过时空平整化与跨窗口3D-IoU关联，生成全序列一致的实例级伪标签和CLIP语义特征。
- **4D分割模型**（Figure 3）：以Minkowski U-Net为骨干处理叠加点云体积，Transformer实例解码器预测时空掩码、对象置信度及CLIP token，训练时仅依赖自生成的伪标签。

### 主要结果

- **3D零样本全景分割**：在SemanticKITTI上，SAL-4D以38.2 PQ超越先前最优方法SAL超过5个PQ点（Table 4）。
- **4D零样本全景分割**：在SemanticKITTI上达到42.2 LSTQ，约为顶级全监督方法Mask4D的59%；在Panoptic nuScenes上达到45.0 LSTQ，显著优于所有零样本基线（Table 5）。
- **消融验证**：跨窗口关联使LSTQ提升1.9个百分点，零样本识别得分S_cls提升2.6（Table 1）；时空一致伪标签相比单帧伪标签，语义识别相对提升15% PQ，分割质量相对提升20% mIoU（Table 3）；FrankenFrustum数据增广使模型从仅处理相机视锥区域（14%点数）泛化至全360°点云，LSTQ从8.3跃升至42.2（Table 13）。
- **零样本能力**：模型可正确分割标准数据集词汇以外的对象（如广告牌、电箱），验证了开放词汇识别的有效性（Figure 6）。

### 局限与开放问题

当前伪标签仅生成于相机视锥重叠区域，全点云分割质量仍落后于视锥内；跨窗口关联在快速运动或严重遮挡场景下可能出现ID断裂。零样本识别能力受限于CLIP模型的语义知识边界，且训练与伪标签生成依赖较大算力（8×A100 GPU）。未来方向包括：摆脱对同步图像的依赖、缩小与全监督方法的差距（目前约40%性能差距）、以及探索更丰富的视觉基础模型蒸馏策略。

### 问题背景

4D激光雷达全景分割（4D Lidar Panoptic Segmentation, 4D-LPS）要求对点云序列中的每个点同时赋予语义类别和实例身份，并保持跨时间的实例身份一致性。这一任务对自动驾驶、机器人导航等场景至关重要，因为它提供了对动态场景的完整时空理解。然而，现有方法面临一个根本性瓶颈：**人工标注的4D激光雷达数据极度稀缺，且标注词汇固定**，导致训练出的模型只能识别预定义的封闭类别集合，无法泛化到训练时未见过的任意新对象。

### 现有方法缺口

当前零样本激光雷达全景分割方法主要存在以下结构性缺陷：

1. **时空隔离处理**：现有零样本方法（如SAL）将每一帧点云独立处理，完全忽略了连续帧之间的时间关联性。这种单帧范式无法捕捉对象的运动轨迹和时空一致性，导致跨帧实例身份断裂。

2. **伪标签质量受限**：单帧伪标签生成依赖单帧CLIP特征平均，语义信息噪声大且不稳定。缺乏跨帧关联机制使得同一对象在不同帧可能被赋予不同的语义特征，削弱了训练信号的可靠性。

3. **4D时空建模空白**：尽管全监督方法（如Mask4D、EfficientLPS+KF）已在4D-LPS上取得显著进展，但零样本设定下尚无方法能够直接在4D点云序列上进行端到端的时空联合分割与识别。

4. **多模态桥梁未充分利用**：自动驾驶平台天然配备LiDAR与多路摄像机，但现有工作未能系统性地将视频对象分割（VOS）和视觉-语言基础模型（如CLIP）的知识蒸馏到LiDAR空间，以构建时空连续的自监督训练信号。

### 核心动机

本文的核心动机源于一个关键洞察：**通过滑动时间窗口内的VOS传播与CLIP特征提取，辅以精确的3D-IoU跨窗口关联和时空平整化，可以为任意长序列生成时空一致的实例级伪标签**。在这些噪声但去相关的伪标签上训练，能够蒸馏出具有零样本识别能力的端到端4D激光雷达分割模型。

具体而言，SAL-4D旨在回答以下问题：能否利用多模态传感器（摄像机+LiDAR）作为桥梁，将成熟的2D基础模型能力迁移到4D LiDAR空间，从而在完全无需人工语义标注的条件下，实现对任意文本提示指定的对象进行时空一致的分割与跟踪？这一目标的实现将从根本上突破标注词汇对感知系统的限制，使自动驾驶系统能够灵活应对开放世界中层出不穷的新对象类别。

## 核心方法与创新机理

### 1. 问题瓶颈与因果杠杆

4D激光雷达全景分割的核心瓶颈在于：**人工标注的4D数据极度稀缺，且封闭的类别词汇表限制了模型对任意新对象的时空一致分割与识别能力**。SAL-4D的因果杠杆是：利用多模态传感器（摄像机+LiDAR）作为桥梁，将视频对象分割（VOS）和视觉-语言基础模型（CLIP）的能力蒸馏到LiDAR空间——通过短时间窗口内的可靠伪标签生成与跨窗口关联，构建时空连续的自监督训练信号。

核心洞察可概括为：**滑动时间窗口内的VOS传播与CLIP特征提取，辅以精确的3D-IoU跨窗口关联和时空平整化（flatten），可为任意长序列生成时空一致的实例级伪标签；在这些噪声但去相关的伪标签上训练，能够蒸馏出具有零样本识别能力的端到端4D激光雷达分割模型。**

### 2. 关键创新点（Changed Slots）

相较于零样本单帧激光雷达全景分割基线SAL（单帧点云输入，无跨帧关联），SAL-4D在以下六个维度实现了根本性改变：

#### 2.1 输入时空范围：从3D到4D体积

SAL-4D的输入不再是单帧点云，而是**固定大小时间窗口内的叠加点云（4D体积）**。模型直接在时空体素上操作，使网络能够学习对象的运动模式和时序连续性，而非孤立地处理每一帧。

#### 2.2 伪标签时间一致性：跨窗口关联实现全局实例ID

这是SAL-4D最关键的创新。基线方法仅在单帧内生成伪标签，实例ID在不同帧之间无关联。SAL-4D则采用两步策略：
- **窗口内独立标注**：对每个滑动窗口独立运行Track–Lift–Flatten流水线；
- **跨窗口关联**：利用匈牙利算法和3D-IoU代价（$c_{ij} = 1 - \mathrm{IoU}_{3\mathrm{D}}(\tilde{m}_{i,k-1}, \tilde{m}_{j,k})$）将相邻窗口的实例关联，形成全序列一致的实例ID。

消融实验表明，跨窗口关联使LSTQ提升1.9个百分点，并显著改善零样本识别（S_cls +2.6）（Table 1）。这一设计使模型能够学习到跨越长序列的时空一致表示。

#### 2.3 语义信息源：序列级CLIP特征聚合

基线方法仅在单帧内平均CLIP特征。SAL-4D在跨窗口关联后，**在整个序列上平均CLIP token**，得到语义更一致的实例特征（Pseudo-labels v2）。实验证明，v2伪标签相比v1（仅窗口内）将关联得分S_assoc从67.2提升至77.2（Table 12），约15%的相对提升，证明了全局一致标签的监督价值。

#### 2.4 模型输出头：预测CLIP token而非语义类别

SAL-4D的输出头不预测固定的语义类别，而是预测**时空掩码、对象置信度以及d维CLIP token**。测试时，通过CLIP语言编码器与预测token的点积实现开放词汇分类，使得模型能够识别训练词汇表之外的新类别（如广告牌、电箱，Figure 6）。

#### 2.5 训练损失：多目标联合优化

SAL-4D的训练损失扩展为三项联合优化：
$$\mathcal{L}_{SAL-4D} = \mathcal{L}_{obj} + \mathcal{L}_{seg} + \mathcal{L}_{token}$$
其中$\mathcal{L}_{obj}$为对象性交叉熵损失，$\mathcal{L}_{seg}$为分割损失（BCE+Dice），$\mathcal{L}_{token}$为CLIP token余弦距离损失。附录中进一步增加了辅助CLIP token损失$\mathcal{L}_{token.aux}$。

#### 2.6 数据增广：FrankenFrustum突破视锥限制

伪标签仅生成在相机视锥重叠的点云区域（SemanticKITTI中仅14%的点）。SAL-4D引入**FrankenFrustum增广**，随机组合不同帧的视锥区域，迫使模型学习视锥之外的点云分割。这一增广是全点云评估的关键：全点云LSTQ从8.3跃升至42.2（Table 13），使模型从视锥区域泛化至360°全点云。

### 3. 方法架构概览

SAL-4D由两大核心组件构成：

**伪标签引擎（Pseudo-label Engine，Figure 2）**：
- **Track**：在视频首帧用SAM网格提示发现对象，使用SAMv2在滑动窗口内传播掩码；
- **Lift**：通过LiDAR-相机投影将2D掩码提升到3D点云，并用DBSCAN修正传感器对齐误差；
- **Flatten**：基于掩码体积排序和交并比（IoM）抑制重叠掩码，确保每个点至多属于一个实例；
- **Cross-window Association**：通过3D-IoU线性分配将窗口间实例关联，生成全序列一致的伪标签。

**SAL-4D模型（Figure 3）**：
- **Minkowski U-Net骨干**：用稀疏3D卷积编码叠加点云的多分辨率特征，融合傅里叶位置编码以保留时空信息；
- **Transformer实例解码器**：通过可学习查询与体素特征交互，预测时空掩码、对象性分数和CLIP token；
- **近在线推理**：对滑动窗口输出进行跨时间3D-IoU关联获得完整轨迹，使用CLIP语言编码器与预测token的点积实现零样本分类。

### 4. 创新有效性验证

决定性的实验证据包括：
- **3D零样本全景分割**：SAL-4D在SemanticKITTI上超越先前方法超过5 PQ（Table 4）；
- **4D零样本全景分割**：在SemanticKITTI上LSTQ达42.2，超越最强零样本基线11.9点，约为顶级监督方法的59%（Table 5）；
- **时空一致性收益**：4D伪标签相比单帧伪标签，语义识别相对提升15% PQ，分割质量相对提升20% mIoU（Table 3）；
- **零样本能力**：模型可正确分割标准数据集词汇以外的对象（如广告牌、电箱，Figure 1和Figure 6）。

### 5. 局限与待解决问题

尽管创新显著，SAL-4D仍存在以下局限：
- 伪标签仅覆盖相机视锥区域，全点云分割质量仍落后于视锥内；
- 跨窗口关联依赖3D-IoU匹配，在快速运动、严重遮挡时可能出现ID断裂；
- 零样本识别受限于CLIP模型的语义知识，对长尾类别可能失效；
- 训练和伪标签生成依赖较大算力（8×A100 GPU），轻量化部署未讨论。

SAL-4D 由两个核心组件构成：**多模态伪标签引擎**（Pseudo-label Engine）与**端到端可训练模型** `f_θ`。前者利用未标注的 LiDAR 序列与同步多路视频，自动生成时空一致的自监督训练信号；后者在固定大小的 4D 体积上学习实例级分割，并预测每个轨迹的 CLIP token，以支持测试时的零样本文本提示分类。整体流程如图 2 与图 3 所示。

### 输入与数据流

系统假定输入为一个 LiDAR 序列 `P = {P_t}_{t=1}^T`（每帧 `P_t ∈ R^{N_t×4}` 包含三维坐标与强度），以及 `C` 路未标注的同步视频。这两个模态通过传感器标定参数在空间上对齐，构成多模态桥梁。

数据流分为两个阶段：
1. **伪标签生成阶段**：伪标签引擎以离线方式处理整个序列，输出代理数据集 `D_proxy`，其中每个样本包含一个固定大小时间窗口内的叠加点云、实例级时空掩码、全局一致的实例 ID 以及序列级 CLIP 语义特征。
2. **模型训练阶段**：模型 `f_θ` 以 `D_proxy` 中的窗口化 4D 体积为输入，输出每个查询对应的二值时空掩码、对象性置信度以及 `d` 维 CLIP token。训练损失由对象性交叉熵、分割损失（BCE + Dice）和 CLIP token 余弦距离三部分组成。

### 伪标签引擎：Track–Lift–Flatten 流水线

伪标签引擎的核心是一条“先跟踪、再提升、后平整化”的三阶段流水线，在滑动时间窗口内独立运行，再通过跨窗口关联形成全局一致标签。

**阶段一：滑动窗口分割与传播（Track）**  
以步长 `S`、窗口大小 `K` 在序列上滑动。对每个窗口的首帧视频，使用 SAM 的网格提示策略自动发现对象候选，随后利用 SAMv2 在整个窗口内传播掩码。同时，对每个传播得到的掩码提取 CLIP 视觉特征，作为该实例在该窗口内的语义表示。

**阶段二：2D 到 3D 语义提升（Lift）**  
利用 LiDAR-相机投影关系，将图像空间的掩码提升到 3D 点云。为修正传感器标定误差和视差引起的对齐偏差，对每帧提升后的点云独立运行 DBSCAN 聚类，去除离群点并精修实例边界。

**阶段三：时空平整化（Flatten）**  
窗口内多个实例掩码可能存在重叠。引擎首先计算每个实例的时空体积 `V_i = Σ_{t∈T_k} |m̃_{i,t}|`，然后按体积降序排列，基于交并最小体积比（IoM）抑制重叠较大的掩码，确保每个点至多属于一个实例。消融实验表明，将平整化操作从“先平整化再提升”改为“先提升再平整化”，使单帧类别无关分割的 PQ 提升 +3.1（Table 9）。

### 跨窗口关联与语义特征聚合

相邻窗口的实例通过线性分配进行关联。代价矩阵基于聚合掩码的 3D-IoU 计算：

$$c_{ij} = 1 - \mathrm{IoU}_{3\mathrm{D}}(\tilde{m}_{i,k-1}, \tilde{m}_{j,k})$$

使用匈牙利算法求解最优匹配，从而将窗口内的局部实例 ID 链接为全局一致的轨迹 ID。关联完成后，对同一轨迹在所有窗口中的 CLIP token 进行平均，得到序列级语义特征（即 v2 伪标签）。相比仅在窗口内平均的 v1 标签，v2 标签将关联得分 `S_assoc` 从 67.2 提升至 77.2，证明了全局一致语义监督的价值（Table 12）。

### 模型架构与推理

模型 `f_θ` 采用 Minkowski U-Net 作为骨干网络，在叠加的 4D 点云体积上提取多分辨率稀疏体素特征，并融合傅里叶位置编码以保留时空信息。Transformer 实例解码器通过一组可学习查询与体素特征交互，预测时空掩码、对象性分数和 CLIP token。

推理时采用近在线策略：对每个滑动窗口输出掩码，通过跨时间的 3D-IoU 二分匹配关联为完整轨迹。零样本分类则使用 CLIP 语言编码器对测试时指定的文本提示进行编码，与预测的 CLIP token 计算点积，取 argmax 得到语义类别。

### 关键设计决策

- **窗口大小**：K=4~8 时性能最优。`S_assoc` 在 K=8 时继续提升，但 `S_cls` 在 K=4 时即饱和（Table 1），表明语义特征的时间聚合收益有限。
- **自车运动补偿**：训练时以 10% 概率随机不对齐自车运动（Mix 策略），可获得最佳 LSTQ 53.2，优于纯对齐或纯不对齐（Table 2）。这表明模型需要同时学习运动模式与时空外观特征。
- **FrankenFrustum 增广**：由于伪标签仅生成在相机视锥重叠区域（SemanticKITTI 中仅占 14% 点数），该增广通过合成非视锥区域的训练样本，使模型泛化至全 360° 点云，全点云 LSTQ 从 8.3 跃升至 42.2（Table 13）。

SAL-4D的核心架构由**多模态伪标签引擎**与**4D分割模型**两大组件构成，二者通过自蒸馏形成闭环：伪标签引擎从未标注的多模态序列中生成时空一致的训练信号，模型则学习从4D点云体积中直接预测实例分割与CLIP语义特征。

### 多模态伪标签引擎

伪标签引擎（Figure 2）采用**Track–Lift–Flatten**流水线，在滑动时间窗口内独立生成伪标签，再通过跨窗口关联获得全序列一致的实例ID。

**Track（跟踪与传播）**：对每个长度为$K$、步长为$S$的滑动窗口，在首帧图像上用SAM进行网格提示发现对象，随后利用SAMv2在整个窗口内传播掩码，同时为每个传播得到的masklet提取CLIP视觉特征。

**Lift（2D到3D提升）**：通过LiDAR-相机投影将图像掩码提升至3D点云空间。由于传感器标定误差，提升后的点云掩码可能存在噪点，因此对每帧独立应用DBSCAN聚类进行精修。消融实验（Table 8）表明，逐帧DBSCAN修正优于对全窗口统一修正，后者会损害动态对象的分割质量。

**Flatten（时空平整化）**：提升后的masklet可能存在重叠——同一点被多个实例声明。平整化步骤按masklet的时空体积$V_i$降序排列，利用交叠率（IoM）抑制重叠掩码：

$$\mathrm{IoM}_{ij} = \frac{\sum_{t \in T_k} |\tilde{m}_{i,t} \cap \tilde{m}_{j,t}|}{\min(V_i, V_j)}$$

其中masklet的时空体积定义为窗口内各帧点数的总和：

$$V_i = \sum_{t \in T_k} |\tilde{m}_{i,t}|$$

当$\mathrm{IoM}_{ij}$超过阈值时，保留体积较大的masklet，确保每个点至多属于一个实例。

**跨窗口关联**：相邻滑动窗口$(w_{k-1}, w_k)$的重叠帧内，通过匈牙利算法进行线性分配，关联成本基于聚合掩码的3D交并比：

$$c_{ij} = 1 - \mathrm{IoU}_{3\mathrm{D}}(\tilde{m}_{i,k-1}, \tilde{m}_{j,k})$$

成功关联的实例共享同一全局ID，其CLIP特征在整个序列上进行平均，得到更一致的语义表示（v2伪标签）。Table 1显示，跨窗口关联使LSTQ提升1.9个百分点，零样本识别得分$S_{cls}$提升2.6；Table 12进一步表明，v2伪标签相比仅窗口内平均的v1，关联得分$S_{assoc}$从67.2跃升至77.2。

### 4D分割模型

模型（Figure 3）采用**tracking-before-detection**设计，在固定大小的4D体积上直接预测时空一致的实例分割。

**骨干网络**：使用Minkowski U-Net对叠加点云进行稀疏3D卷积编码，提取多分辨率体素特征，并融合傅里叶位置编码以保留时空位置信息。

**Transformer实例解码器**：一组可学习查询与体素特征交叉注意力交互，并行输出三组预测：
- 时空掩码$\mathcal{M} \in \mathbb{R}^{M \times T \times H \times W}$（$M$为查询数量）
- 对象性分数$\mathcal{O} \in \mathbb{R}^{M \times 2}$
- CLIP token $f \in \mathbb{R}^{M \times d}$

**训练损失**由三项组成：

$$\mathcal{L}_{SAL-4D} = \mathcal{L}_{obj} + \mathcal{L}_{seg} + \mathcal{L}_{token}$$

其中$\mathcal{L}_{obj}$为对象性交叉熵损失，$\mathcal{L}_{seg}$为分割损失（BCE + Dice），$\mathcal{L}_{token}$为预测CLIP token与伪标签CLIP特征之间的余弦距离损失。附录A.2.4给出了包含辅助token损失的完整形式。

**推理与零样本分类**：推理时，将sigmoid激活后的掩码与对象性分数加权，通过argmax为每个点分配实例：

$$\operatorname{mask} = \operatorname{argmax}(\operatorname{sigmoid}(\mathcal{M}) \cdot \operatorname{score}, \dim=0)$$

其中$\operatorname{score} = \max(\mathcal{O} \in \mathbb{R}^{M \times 2}, \dim = -1)$。跨窗口的实例通过3D-IoU双图匹配进行近在线关联，形成完整轨迹。零样本分类时，使用CLIP语言编码器编码测试时指定的类别提示词，与预测的CLIP token计算点积，取argmax得到语义类别。

### 关键设计决策的消融支撑

- **窗口尺寸**：Table 1显示，$K=4\sim8$时性能最佳，$S_{assoc}$在$K=8$时最优，进一步增大窗口收益饱和。
- **自车运动对齐**：Table 2表明，训练时以10%概率随机不对齐自车运动（混合策略）可获得最佳LSTQ 53.2，优于纯对齐或纯不对齐。
- **FrankenFrustum增广**：Table 13证明，该增广是将模型从相机视锥（仅14%点数）泛化至全360°点云的关键，全点云LSTQ从8.3跃升至42.2。
- **Lift-Flatten顺序**：Table 9表明，将流水线从Flatten-Lift改为Lift-Flatten（先提升到3D再平整化），使类别无关分割PQ提升+3.1；引入按实例DBSCAN精修和基于覆盖度的平整化后，合计提升+6.6 PQ。

## 实验与关键发现

### 核心实验设置

SAL-4D在两个自动驾驶数据集上验证：**SemanticKITTI**（64线LiDAR，序列00-08训练/09-10验证）和**Panoptic nuScenes**（32线LiDAR，700/150/150序列划分）。所有零样本方法均未使用任何语义类别标注进行训练，仅依靠无标签多模态数据（LiDAR+多路相机）。测试时所有方法使用相同的CLIP文本编码器及相同的类别提示词，保证语义评估公平。

4D全景分割采用**LSTQ**指标：`LSTQ = √(S_assoc × S_cls)`，即时空关联得分与语义分类得分的几何平均，解耦了时空一致性与零样本识别能力的评估。3D全景分割沿用标准**PQ**指标：`PQ = SQ × RQ`。

### 主结果：4D零样本全景分割

**Table 5** 报告了4D-LPS基准的核心结果。SAL-4D在SemanticKITTI上达到**42.2 LSTQ**，相较最强零样本基线SW（Stationary World，30.3 LSTQ）提升**+11.9**；在Panoptic nuScenes上达到**45.0 LSTQ**，提升**+14.7**。这一结果约为顶级全监督方法（Mask4D 71.0 LSTQ）的**59%**，表明零样本与全监督之间仍存在显著差距，但SAL-4D已大幅缩小了这一鸿沟。

值得关注的是，SAL-4D在关联得分（S_assoc）上表现尤为突出：SemanticKITTI上S_assoc达77.2，远超MOT基线（45.1）和VIS基线（MinVIS，44.8），证明时空一致伪标签对跟踪能力的蒸馏效果显著。语义分类得分（S_cls）上，SAL-4D（23.0）同样优于SW（20.3）和MOT（19.8），验证了跨窗口CLIP特征平均对零样本识别的增益。

### 主结果：3D零样本全景分割

**Table 4** 展示了3D-LPS评估。在相机视锥内（frustum）评估中，SAL-4D达到**38.2 PQ**，超越单帧零样本基线SAL（33.1 PQ）**+5.1**；在全点云评估中，SAL-4D达到**30.8 PQ**，超越SAL（25.3 PQ）**+5.5**。这一结果验证了核心洞察：在时空一致伪标签上训练4D模型，可以反哺单帧3D分割质量。

### 消融实验：伪标签引擎

**Table 1** 系统消融了伪标签引擎的两个关键设计。

**时间窗口尺寸**：窗口大小K=4~8时性能最佳。关联得分（S_assoc）随K增大持续改善（K=2时73.7，K=8时77.2），但语义得分（S_cls）在K=4时即饱和（20.8），进一步增大窗口收益递减。K=16时LSTQ反而下降（49.2 vs K=8的51.1），表明过长窗口可能引入传播误差。

**跨窗口关联**：移除跨窗口关联导致LSTQ从51.1降至49.2（**-1.9**），其中S_cls下降2.6（20.8→18.2），S_assoc下降1.2（77.2→76.0）。这表明跨窗口关联不仅改善跟踪连续性，更关键的是通过全序列CLIP特征平均提升了语义识别质量——这一机制在Table 12中得到进一步验证：使用v2伪标签（跨窗口关联后）训练，S_assoc从67.2跃升至77.2（**+10.0**），证明全局一致标签的监督价值远超窗口内独立标注。

**Table 3** 量化了时空一致伪标签相比单帧伪标签的质量优势：语义识别（PQ）相对提升**超过15%**，分割质量（mIoU）相对提升**超过20%**。这一结果直接支撑了论文的核心主张——时间传播与跨窗口平整化是伪标签质量的关键保障。

### 消融实验：模型训练策略

**Table 2** 揭示了训练中的关键发现。

**自车运动补偿策略**：训练时随机不对齐自车运动（10%概率）的混合策略（Mix）获得最佳LSTQ 53.2，优于纯对齐（51.1）或纯不对齐（50.0）。这表明适度的坐标扰动作为一种正则化，迫使模型学习更鲁棒的时空特征，而非过拟合到精确的运动补偿模式。

**FrankenFrustum数据增广**：这是将模型从相机视锥（仅14%点云）泛化至全360°点云的决定性技术。**Table 13**显示，无此增广时全点云LSTQ仅8.3，引入后跃升至42.2。该增广通过合成非视锥区域的伪点云与伪标签，使模型学会分割相机视野之外的对象——这是SAL-4D能够进行全点云评估的核心使能技术。

### 消融实验：单帧伪标签改进

**Table 9** 报告了单帧伪标签流水线的逐步改进。将流水线从Flatten-Lift改为Lift-Flatten（即先在3D空间提升再平整化），使类别无关分割PQ提升**+3.1**。进一步引入“按实例DBSCAN精修”和“基于覆盖度的平整化”，合计提升**+6.6 PQ**（类别无关）和**+2.4 PQ**（零样本）。这些改进直接提升了伪标签的基础质量，为4D蒸馏提供了更可靠的监督信号。

**Table 8** 的DBSCAN消融表明，逐帧独立修正优于对全窗口统一修正——后者会损害动态对象的时空分割质量，因为动态物体在不同帧的空间位置差异较大，统一聚类容易将不同实例错误合并。

### 失败模式与局限性

尽管整体表现强劲，SAL-4D仍存在以下可识别的失败模式：

1. **全点云质量衰减**：全点云上的分割质量（30.8 PQ）显著落后于视锥内（38.2 PQ）。虽然FrankenFrustum增广实现了从无到有的突破，但非视锥区域的伪标签本质上是合成生成的，其精度无法与真实多模态伪标签匹敌。

2. **跨窗口关联的脆弱性**：关联依赖3D-IoU匹配，在快速自车运动、严重遮挡或物体进出视野频繁时，可能出现ID断裂（同一对象被分配不同ID）或融合错误（不同对象被合并）。Table 1中S_assoc在K=16时下降（76.4）即反映了长窗口中的关联退化。

3. **零样本语义的粒度限制**：识别能力受限于CLIP模型的语义知识。对于非常细粒度或长尾类别（如特定型号车辆、罕见道路设施），CLIP特征可能缺乏足够的判别力。Figure 6虽展示了广告牌、电箱等标准词汇外对象的成功分割，但这类能力的边界尚未系统量化。

4. **数据依赖性**：伪标签生成需要同步的多传感器数据（LiDAR+多路相机），限制了方法在仅有LiDAR的场景中的直接应用。

5. **算力需求**：训练和伪标签生成均依赖较大算力（8 × A100 GPU），轻量化部署方案未讨论。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2504_00848/figures/008_Table_4.jpg]]
*Table 4: 3D-LPS evaluation. Training our SAL-4D model on the temporal consistent 4D pseudo-labels yields superior 3D (singlescan) performance compared to 3D baselines. We evaluate on the SemanticKITTI validation set. SAL-4D evaluated not only in the frustum was trained with the FrankenFrustum [62] augmentation*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2504_00848/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative results. We compare our 4D pseudo-labels (obtained over windows of 2&8 frames) to GT labels, and singlescan labels. By contrast to GT, our automatically-generated labels cover both thing and stuff classes. As can be seen, the temporal coherence of labels improves over larger window sizes*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2504_00848/figures/004_Table_1.jpg]]
*Table 1: Pseudo-label ablations on temporal window size and cross-window association: We ablate our approach on temporal window sizes of size K \ = \ $\{$ 2 , 4 , 8 , 1 6 $\}$ with stride $\frac { K } { 2 }$ on SemanticKITTI validation set. We average CLIP features for each instance across time. We observe association score ( $S _ { a s s o c }$ ) improve up to 8 frames, while zero-shot recognition ( $S _ { c l s }$ ) saturates at 4 frames. Without the cross-window association (Sec. 3.2.2), the L S T Q drops by 1.9 percentage points*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2504_00848/figures/010_Table_5.jpg]]
*Table 5: Zero-Shot 4D Lidar Panoptic Segmentation benchmark: We compare SAL-4D to several supervised baselines for 4D Panoptic Lidar Segmentation and zero-shot baselines. While there is still a gap between supervised methods and zero-shot approaches, SAL-4D significantly narrows down this gap. On SemanticKITTI, our model SAL-4D reaches 59% of the topperforming supervised model, and on nuScenes, 72%, even though it is not trained using any labeled data*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2504_00848/figures/015_Table_8.jpg]]
*Table 8: Pseudo-label ablations on DBSCAN settings, per-frame or all-frame: We show the effect of doing DBSCAN per scan separately or on all the scans within the temporal window together on the KITTI validation set. The temporal window size is set to 2. The results show that doing DBSCAN per-frame gives the best result*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2504_00848/figures/016_Table_9.jpg]]
*Table 9: Single-scan 3D pseudo-label improvements: We report class-agnostic and zero-shot single-scan Lidar Panoptic Segmentation (LPS) results with several improvements added to the original [62] pseudo-labels. Evaluation is performed in the camera frustum of the SemanticKITTI validation set. Table 10. Pseudo-label ablations on nuScenes dataset on temporal window size: We ablate on temporal window sizes 2 − 4 frames. The quality of pseudo labels with 4 frame temporal window drops significantly. The stride is set as half the window size*

## 定位与知识库关联

### 与基线方法的关系

SAL-4D 的核心贡献在于将**零样本激光雷达全景分割**从单帧（3D）扩展到时序（4D），并通过自监督伪标签蒸馏实现开放词汇识别。其方法定位可通过与以下基线的对比来理解：

**单帧零样本基线：SAL**。SAL（Zhang et al.）是首个在激光雷达点云上实现零样本全景分割的方法，其核心是利用 SAM 生成类别无关掩码，再通过 CLIP 特征在测试时进行开放词汇分类。SAL-4D 在单帧评估上直接超越 SAL：在 SemanticKITTI 视锥内评估中，PQ 从 33.1 提升至 38.2（+5.1）；在全点云评估中，PQ 从 25.3 提升至 30.8（+5.5）（Table 4）。这一提升的因果机制在于：SAL-4D 在时空一致的 4D 伪标签上训练，蒸馏出了更鲁棒的实例分割能力和更稳定的 CLIP token 预测——Table 3 显示，时空伪标签相比单帧伪标签在语义识别上相对提升超过 15% PQ，分割质量相对提升超过 20% mIoU。

**零样本 4D 基线**。作者构建了三类零样本 4D 基线：(1) **Stationary World (SW)** 基线，基于自车运动将单帧预测传播到相邻帧；(2) **MOT 基线**（adapted from ），使用卡尔曼滤波和线性分配进行零样本多目标跟踪；(3) **VIS 基线**（MinVIS），基于视频实例分割的查询匹配范式。在 SemanticKITTI 4D-LPS 基准上，SAL-4D 的 LSTQ 达到 42.2，而最强零样本基线 SW 仅为 30.3，提升 +11.9；在 Panoptic nuScenes 上，LSTQ 从 30.3 提升至 45.0（+14.7）（Table 5）。这一显著差距的根源在于：SW/MOT/VIS 基线均将时序关联作为后处理步骤，而 SAL-4D 通过滑动窗口内的联合分割与跟踪，以及跨窗口 3D-IoU 关联，在训练阶段就学习了时空一致的实例表示。

**全监督上界**。SAL-4D 在 SemanticKITTI 上的 LSTQ（42.2）约为顶级监督方法 **Mask4D** 和 **EfficientLPS+KF** 的 59%（Table 5）。这一差距主要源于：(1) 伪标签仅在相机视锥区域生成（SemanticKITTI 中仅覆盖约 14% 的点云），全点云上的分割质量受限于 FrankenFrustum 增广的泛化能力；(2) 零样本识别依赖 CLIP 的语义知识，对细粒度或长尾类别区分能力有限。

### 适用边界

**传感器配置依赖**。SAL-4D 的伪标签引擎需要 LiDAR 与多路摄像机的同步标定数据——SAMv2 在图像空间进行分割与传播，CLIP 在图像空间提取语义特征，再通过 LiDAR-相机投影提升到 3D。这一多模态依赖既是其核心创新（利用成熟视觉基础模型作为桥梁），也是其应用约束：在仅有 LiDAR 的场景或相机不可靠（如极端光照、遮挡）时，伪标签质量会显著下降。

**动态场景的鲁棒性边界**。跨窗口关联依赖 3D-IoU 匹配（Eq. (1)），在快速自车运动、严重遮挡或物体频繁进出视野时，可能出现 ID 断裂或融合错误。Table 1 的消融显示，窗口尺寸 K 从 2 增至 8 时，关联得分 S_assoc 持续提升，但进一步增大至 16 时收益饱和——这表明当前方法在长程关联上仍存在瓶颈。

**语义覆盖的边界**。零样本识别能力受限于 CLIP 模型的语义知识空间。Figure 6 展示了模型对标准数据集词汇外对象（如广告牌、电箱）的正确分割，证明了一定的开放词汇能力，但对于非常规或高度专业化的类别，CLIP token 的区分度可能不足。

### 局限与开放问题

**全点云泛化的代价**。伪标签仅生成在相机视锥内，全点云评估依赖于 FrankenFrustum 数据增广——Table 13 显示，若无此增广，全点云 LSTQ 从 42.2 骤降至 8.3。即使有增广，全点云性能仍显著低于视锥内评估，说明模型对非视锥区域的几何结构学习尚不充分。

**计算资源需求**。伪标签生成和模型训练均依赖较大算力（8 × A100 GPU），轻量化部署方案未被讨论，限制了在资源受限平台上的应用。

**跨域泛化未验证**。当前仅在 SemanticKITTI 和 Panoptic nuScenes 两个自动驾驶数据集上验证，缺乏在不同环境（如室内、越野）、不同传感器配置（如不同线数 LiDAR、不同相机布局）上的泛化证据。

**开放问题**包括：(1) 能否设计仅依赖 LiDAR 的伪标签方案，摆脱对同步图像的依赖？(2) 如何进一步缩小与全监督方法之间约 40% 的性能差距？(3) 模型能否处理开放世界中未见过的新型动态对象并保持一致的跟踪？(4) 当前的 CLIP 蒸馏策略是否可以从更多样的预训练视觉模型（如 DINOv2）中受益？(5) 如何将 4D 时空信息反馈到单帧零样本分割中，以在不运行完整 4D 推理的情况下提升单帧质量？这些问题指向了零样本 4D 感知从“能用”走向“好用”的关键路径。

## 原文 PDF

![[paperPDFs/CVPR_2025/Zero_Shot_4D_Lidar_Panoptic_Segmentation.pdf]]

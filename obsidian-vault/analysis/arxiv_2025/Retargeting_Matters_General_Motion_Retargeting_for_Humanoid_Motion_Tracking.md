---
title: "Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Retargeting_Matters_General_Motion_Retargeting_for_Humanoid_Motion_Tracking.pdf
aliases:
- GMRG
- RMGMRHMT
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 运动重定向中的尺度变换策略（特别是对源运动关节点和根位移的缩放方式与优化顺序）是控制伪影产生的关键因素。通过非均匀局部缩放并配合统一根位移缩放，可有效避免脚滑动和地面穿透。
primary_logic: 通过基于身高比例与关节个体特异性尺度的非均匀局部缩放，消除因全局缩放或SMPL模型拟合不准确引入的运动伪影；随后采用两阶段逆运动学优化——第一阶段优先匹配末端执行器的朝向与位置，第二阶段微调全身关节位置——生成高保真且物理可行的参考动作。结合独立于重定向的训练框架（BeyondMimic），可在不进行大量奖励工程的情况下显著提升运动跟踪策略的成功率和感知保真度。
claims:
- 在21个LAFAN1序列的仿真评估中，GMR的平均全局位置误差（E_g-mpbpe）为104.1 mm，显著低于PHC的247.8 mm和ProtoMotions的139.7 mm。
- 用户研究（N=20）表明，GMR重定向动作的感知保真度显著优于PHC和ProtoMotions，与闭源Unitree数据集的重定向结果接近。
- 低成功率的重定向参考动作中包含明显伪影，如Dance 1中的地面穿透（PHC）、Run (stop & go)中的自相交（ProtoMotions）以及Dance 5中GMR的关节值突变，这些伪影直接导致策略难以学习或完全失败。
- LAFAN1 subset (21 motions, sim) 上 E_g-mpbpe Mean (mm) = 104.1
---

# Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking

> [!tip] 核心洞察
> 通过基于身高比例与关节个体特异性尺度的非均匀局部缩放，消除因全局缩放或SMPL模型拟合不准确引入的运动伪影；随后采用两阶段逆运动学优化——第一阶段优先匹配末端执行器的朝向与位置，第二阶段微调全身关节位置——生成高保真且物理可行的参考动作。结合独立于重定向的训练框架（BeyondMimic），可在不进行大量奖励工程的情况下显著提升运动跟踪策略的成功率和感知保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重定向至关重要：面向人形机器人运动跟踪的通用运动重定向方法 |
| 英文题名 | Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2510.02252v1) · [Code](https://github.com/kevinzakka/mink) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | General Motion Retargeting (GMR) |
| Dataset | LAFAN1 subset |

> [!tip] 效果简介
> - LAFAN1 subset (21 motions, sim) 上，E_g-mpbpe Mean (mm) 104.1 vs 247.8 (-143.7)；E_mpjpe Mean (1e-3 rad) 561.7 vs 778.5 (-216.8)。

## 概述

人形机器人运动跟踪的核心挑战之一，是如何将来自任意人体运动源的参考动作高质量地映射到目标机器人上。现有运动重定向方法——如基于SMPL模型优化的**PHC**（Luo et al., ICCV 2023）和采用Mink差分IK的**ProtoMotions**（Tessler et al., 2024）——在处理人体到人形机器人的尺度差异时，普遍采用全局均匀缩放或SMPL拟合缩放策略。这些策略会在重定向结果中引入地面穿透、脚滑动、自相交和关节值突变等严重伪影。当这些包含伪影的参考动作被送入强化学习策略进行训练时，策略的学习难度显著增加，鲁棒性和成功率大幅削弱——这一问题在缺乏大量奖励工程的情况下尤为突出。

本文提出**General Motion Retargeting (GMR)**，一种通用运动重定向方法。其核心洞察在于：运动重定向中的尺度变换策略是控制伪影产生的关键因果节点。GMR通过**非均匀局部缩放**替代全局缩放——基于身高比例与各关键身体部位的自定义局部缩放因子，对源运动关节点和根位移分别进行差异化缩放，从根源上避免脚滑动和地面穿透。随后，采用**两阶段逆运动学优化**：第一阶段优先匹配末端执行器的朝向与位置，获得无穿透的粗略姿态；第二阶段在关节限位约束下微调全身关节位置，生成高保真且物理可行的参考动作。GMR直接兼容BVH格式输入，无需SMPL中间转换。

在21个LAFAN1序列的仿真评估中，GMR的全局位置误差（E_g-mpbpe）均值为104.1 mm，显著低于PHC的247.8 mm和ProtoMotions的139.7 mm。用户研究（N=20）表明，GMR重定向动作的感知保真度显著优于两种基线方法，接近闭源Unitree数据集的重定向质量。低成功率案例的归因分析直接验证了伪影与策略失败之间的因果关系：PHC在“Dance 1”中的地面穿透、ProtoMotions在“Run (stop & go)”中的自相交，以及GMR在极少数情况下的关节值突变，均导致策略难以学习或完全失败。所有策略均使用独立的BeyondMimic框架训练，未针对任何重定向方法进行奖励调优，确保了比较的公平性。

## 背景与动机

### 人形机器人运动跟踪的核心挑战

让双足人形机器人在现实世界中复现人类运动的敏捷性与多样性，是机器人学习领域的长期目标。基于强化学习（RL）的运动跟踪策略近年来取得了显著进展，其基本范式是：将人类运动数据通过**运动重定向（motion retargeting）**转换为机器人可执行的参考动作，随后训练策略网络以尽可能精确地复现该参考动作。在这一范式中，重定向环节的质量直接决定了参考动作的物理可行性与感知保真度，进而深刻影响下游策略的学习难度与最终表现。

然而，现有重定向方法在处理人体到人形机器人的**尺度差异**（包括身高比例、肢体长度、关节构型差异）时暴露出系统性缺陷，成为制约运动跟踪策略成功率的关键瓶颈。

### 现有重定向方法的伪影问题

当前主流的重定向方法主要分为两类：

- **基于SMPL模型的优化重定向**（如**PHC**，Luo et al., ICCV 2023；He et al., 2024）：将源运动拟合到SMPL人体模型，再优化机器人姿态以最小化与SMPL关节目标的位置误差。该流程依赖SMPL拟合的准确性，且需从BVH等格式转换，可能引入额外误差。
- **基于全局缩放的优化重定向**（如**ProtoMotions**，Tessler et al., 2024）：采用全局轴对齐缩放处理人体与机器人的尺度差异，随后通过Mink差分IK最小化关节位置与朝向误差。

这两种方法在尺度变换策略上的共同局限是：**要么采用全局均匀缩放，要么依赖SMPL模型的拟合缩放**。这种粗粒度的处理方式无法精确匹配人体与机器人各身体部位的个体尺度差异，导致重定向结果中出现一系列严重伪影：

- **地面穿透**：机器人足部陷入地面以下，破坏接触约束
- **脚滑动**：支撑脚在应当固定的帧中出现位移
- **自相交**：机器人肢体穿透自身躯干或其他肢体
- **关节值突变**：相邻帧之间关节角度出现不连续的跳变

这些伪影作为参考动作输入RL策略后，显著增加了策略的学习难度。策略不仅需要学习复现目标运动，还必须“对抗”参考动作中物理不可行的部分，导致训练不稳定、收敛缓慢，甚至在缺乏大量奖励工程的情况下完全失败。实验证据表明，低成功率的策略其参考动作中均包含上述典型伪影（见**Figure 3**），如PHC在“Dance 1”序列中产生地面穿透，ProtoMotions在“Run (stop & go)”中产生自相交，直接导致策略无法学习。

### 本文动机与核心思路

本文的核心观察是：**重定向环节中的尺度变换策略——特别是对源运动关节点和根位移的缩放方式与优化顺序——是控制伪影产生的关键因果杠杆**。基于此，作者提出了一种通用运动重定向方法 **General Motion Retargeting (GMR)**，其设计目标是在不依赖特定人体模型（如SMPL）的前提下，从任意BVH格式源运动生成高保真、物理可行的机器人参考动作，从而在不进行大量奖励工程的情况下显著提升运动跟踪策略的成功率和感知保真度。

GMR的核心创新在于两个相互配合的设计选择：

1. **非均匀局部缩放**：基于身高比例与各关键身体部位的个体特异性尺度因子，对源运动进行差异化缩放，并对根位移采用统一缩放因子以避免脚滑动伪影。
2. **两阶段逆运动学优化**：第一阶段优先匹配末端执行器的朝向与位置，得到无穿透的粗略姿态；第二阶段在关节限位约束下微调全身关节位置，提升整体跟踪精度。

通过将GMR与独立于重定向的训练框架（BeyondMimic）结合，本文系统性地验证了：**重定向质量是决定运动跟踪策略性能的上游关键因素**，而GMR所采用的尺度变换与优化策略能够有效消除现有方法的典型伪影，使开源重定向流程的性能接近闭源高质量数据集（Unitree）的水平。

## 核心创新

本文的核心贡献在于提出了一种**通用运动重定向方法（General Motion Retargeting, GMR）**，其关键创新并非强化学习策略本身，而是对上游重定向流水线中**尺度变换策略**与**优化求解顺序**的重新设计。现有方法（如 **PHC** 重定向，Luo et al., ICCV 2023; He et al., 2024，以及 **ProtoMotions** 重定向，Tessler et al., 2024）在将人体运动映射到人形机器人时，因尺度差异处理不当而引入严重伪影，这些伪影作为参考动作输入策略后，显著增加了学习难度，削弱了策略的鲁棒性。

GMR 通过以下三个核心改进槽位，系统性地解决了上述瓶颈：

**1. 非均匀局部缩放（Non-Uniform Local Scaling）替代全局均匀缩放**

现有方法采用全局均匀缩放（ProtoMotions）或基于 SMPL 模型的拟合缩放（PHC），这导致重定向结果中出现地面穿透、脚滑动和自相交等典型伪影。GMR 的核心洞察在于：**对根位移与各身体部位采用差异化的缩放策略**。

具体而言，对于非根身体部位，其目标位置由身高比例与局部缩放因子共同决定：

$$\mathbf{p}_{b}^{\mathrm{target}} = \frac{h}{h_{\mathrm{ref}}} s_b (\mathbf{p}_{j}^{\mathrm{source}} - \mathbf{p}_{\mathrm{root}}^{\mathrm{source}}) + \frac{h}{h_{\mathrm{ref}}} s_{\mathrm{root}} \mathbf{p}_{\mathrm{root}}^{\mathrm{source}}$$

其中 $h/h_{\mathrm{ref}}$ 为通用身高比例因子，$s_b$ 为各关键身体部位的自定义局部缩放因子。而对于根位移，则采用统一缩放因子 $s_{\mathrm{root}}$ 以避免引入脚滑动伪影——这是论文明确验证的关键设计选择（Step 3, “we find that scaling the root translation by a uniform scaling factor is crucial to avoid introducing foot sliding artifacts”）。

**2. 两阶段逆运动学优化替代单阶段求解**

PHC 和 ProtoMotions 均采用单阶段优化（分别最小化关节位置误差或联合位置与朝向误差），这容易在复杂姿态下陷入局部极小解，产生关节值突变。GMR 将优化过程解耦为两个阶段：

- **第一阶段**：仅优化身体朝向和末端执行器位置误差，忽略中间身体的位置约束：

$$\operatorname*{min}_{\mathbf{q}} \sum_{(i,j)\in\mathcal{M}} (w_1)_{i,j}^{R} \| R_i^{h} \ominus R_j(\mathbf{q}) \|_2^2 + \sum_{(i,j)\in\mathcal{M}_{\mathrm{ee}}} (w_1)_{i,j}^{p} \| \mathbf{p}_i^{\mathrm{target}} - \mathbf{p}_j(\mathbf{q}) \|_2^2$$

这一阶段优先保证末端执行器的空间匹配质量，得到粗略但无穿透的初始姿态。

- **第二阶段**：以第一阶段解为初始值，使用不同的权重集合，同时优化所有关键身体的朝向和位置误差，并在关节限位约束下进行微调：

$$\operatorname*{min}_{\mathbf{q}} \sum_{(i,j)\in\mathcal{M}} \left[ (w_2)_{i,j}^{R} \| R_i^{h} \ominus R_j(\mathbf{q}) \|_2^2 + (w_2)_{i,j}^{p} \| \mathbf{p}_i^{\mathrm{target}} - \mathbf{p}_j(\mathbf{q}^{r}) \|_2^2 \right] \quad \mathrm{s.t.} \ \mathbf{q}^{-} \le \mathbf{q} \le \mathbf{q}^{+}$$

这种“先粗后精”的优化顺序有效避免了关节值突变，同时提升了整体跟踪精度。

**3. 直接兼容 BVH 格式，消除中间格式转换误差**

PHC 和 ProtoMotions 需要将 BVH 格式转换为 SMPL 或 SMPL-X 格式，这一过程本身可能引入额外的拟合误差。GMR 直接支持 BVH 格式输入（Section III-B），减少了误差传播链路中的不确定性环节。

**创新效果的因果链路验证**

上述创新的有效性通过严格的消融与对照实验得到验证。在 21 个 LAFAN1 序列的仿真评估中，使用 GMR 重定向数据训练的策略，其全局位置误差（$E_{\mathrm{g-mpbpe}}$）均值仅为 104.1 mm，显著低于 PHC 的 247.8 mm 和 ProtoMotions 的 139.7 mm（TABLE II）。更重要的是，低成功率的重定向参考动作中可明确观察到与缩放策略直接相关的伪影：PHC 在 “Dance 1” 中出现严重地面穿透，ProtoMotions 在 “Run (stop & go)” 中出现自相交（Fig. 3），这些伪影直接导致对应策略学习失败或成功率极低。值得注意的是，所有策略均使用独立的 BeyondMimic 框架训练，未针对任何重定向方法进行奖励函数调优，这确保了性能差异可归因于重定向质量本身。

## 整体框架

General Motion Retargeting (GMR) 是一个五阶段的运动重定向流水线，旨在将任意人体运动源（BVH 格式）转换为目标人形机器人的关节轨迹。该流水线以模块化方式依次执行以下步骤：

1. **人-机器人关键身体匹配 (Key Body Matching)**：用户定义人体骨骼与机器人身体部件之间的映射关系，以及各身体部件在后续优化中的跟踪权重。
2. **笛卡尔空间静止姿态对齐 (Rest Pose Alignment)**：将人体和机器人的默认站立姿态在笛卡尔空间下对齐，为后续缩放提供一致的参考坐标系。
3. **非均匀局部缩放 (Non-Uniform Local Scaling)**：基于身高比例计算通用缩放因子，并结合各关键身体部位的自定义局部缩放因子，对源运动关节点及根位移进行缩放。其中根位移采用统一缩放因子，以避免引入脚滑动伪影。
4. **第一阶段逆运动学 (IK with Rotation Constraints)**：仅优化身体朝向和末端执行器的位置误差，忽略中间身体的位置约束，得到粗略但无穿透的初始姿态。
5. **第二阶段微调 (Fine Tuning)**：使用与第一阶段不同的权重，同时优化所有关键身体的朝向和位置误差，以第一阶段解为初始值并在关节限位约束下进行微调，提升整体跟踪精度。

对于运动序列，GMR 逐帧处理，将前一帧的重定向结果作为当前帧优化的初始猜测。序列处理完成后，通过高度后处理步骤（减去序列中最小身体高度）修正全局浮动或地面穿透伪影。

整个流水线的输入为 BVH 格式的源运动数据，输出为可直接用于强化学习策略训练或机器人执行的关节位置序列。该流水线与下游策略训练框架（如 BeyondMimic）完全解耦，无需针对重定向方法进行奖励函数调优。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2510_02252v1/figures/002_Figure_2.jpg]]
*Figure 2: General Motion Retargeting (GMR) Pipeline*

## 核心模块与公式推导

GMR 流水线由五个顺序模块构成（Fig. 2），其核心设计围绕一个关键因果机制展开：**非均匀局部缩放消除伪影，两阶段 IK 在无穿透约束下逐步恢复跟踪精度**。以下仅展开与公式直接关联的三个关键模块。

### 非均匀局部缩放（Step 3）

该模块是整个流水线的**因果旋钮**——它直接决定了重定向参考动作中是否会出现地面穿透、脚滑动或自相交等伪影。与 PHC（基于 SMPL 模型拟合的隐式缩放）和 ProtoMotions（全局轴对齐均匀缩放）不同，GMR 采用两层缩放策略：

1. **通用身高比例因子**：基于源人体骨架身高 $h$ 与参考身高 $h_{\text{ref}}$ 的比值。
2. **局部缩放因子**：为每个关键身体部位 $b$ 定义独立的缩放系数 $s_b$，允许对不同肢体（如手臂、腿）进行差异化调整。

对于非根身体部位，目标位置由下式给出：

$$\mathbf{p}_{b}^{\text{target}} = \frac{h}{h_{\text{ref}}} s_b (\mathbf{p}_{j}^{\text{source}} - \mathbf{p}_{\text{root}}^{\text{source}}) + \frac{h}{h_{\text{ref}}} s_{\text{root}} \mathbf{p}_{\text{root}}^{\text{source}}$$

其中 $\mathbf{p}_{j}^{\text{source}}$ 为源运动中关节点 $j$ 的全局位置，$\mathbf{p}_{\text{root}}^{\text{source}}$ 为源运动根关节位置。该公式的关键设计在于：根位移使用**统一的缩放因子** $s_{\text{root}}$ 而非局部因子，论文明确指出这一选择对避免引入脚滑动伪影至关重要（“scaling the root translation by a uniform scaling factor is crucial to avoid introducing foot sliding artifacts”）。

### 第一阶段 IK：朝向与末端执行器约束（Step 4）

第一阶段 IK 的目标是获得一个**粗略但无穿透**的初始姿态。优化问题仅考虑身体朝向误差和末端执行器的位置误差，**刻意忽略中间关节（如肘、膝）的位置约束**，从而为优化器提供更大的可行空间以避免自相交：

$$\operatorname*{min}_{\mathbf{q}} \sum_{(i,j)\in\mathcal{M}} (w_1)_{i,j}^{R} \| R_i^{h} \ominus R_j(\mathbf{q}) \|_2^2 + \sum_{(i,j)\in\mathcal{M}_{\text{ee}}} (w_1)_{i,j}^{p} \| \mathbf{p}_i^{\text{target}} - \mathbf{p}_j(\mathbf{q}) \|_2^2$$

其中 $\mathcal{M}$ 为全部关键身体映射对集合，$\mathcal{M}_{\text{ee}} \subset \mathcal{M}$ 仅为末端执行器映射子集；$R_i^h$ 为源运动第 $i$ 个身体的朝向矩阵，$R_j(\mathbf{q})$ 为机器人第 $j$ 个身体在关节配置 $\mathbf{q}$ 下的朝向；$\ominus$ 表示 SO(3) 上的测地距离；$(w_1)_{i,j}^{R}$ 和 $(w_1)_{i,j}^{p}$ 为第一阶段权重。

### 第二阶段微调 IK（Step 5）

第二阶段以第一阶段解 $\mathbf{q}^r$ 为初始值，在**关节限位约束**下对全身所有关键身体的位置和朝向进行联合微调：

$$\operatorname*{min}_{\mathbf{q}} \sum_{(i,j)\in\mathcal{M}} \left[ (w_2)_{i,j}^{R} \| R_i^{h} \ominus R_j(\mathbf{q}) \|_2^2 + (w_2)_{i,j}^{p} \| \mathbf{p}_i^{\text{target}} - \mathbf{p}_j(\mathbf{q}^r) \|_2^2 \right] \quad \mathrm{s.t.} \ \mathbf{q}^{-} \le \mathbf{q} \le \mathbf{q}^{+}$$

其中 $(w_2)_{i,j}^{R}$ 和 $(w_2)_{i,j}^{p}$ 为**不同于第一阶段**的权重集合，$\mathbf{q}^{-}$ 和 $\mathbf{q}^{+}$ 为机器人关节角度的下界和上界。两阶段权重差异是设计的核心——第一阶段优先保证末端执行器的空间可达性，第二阶段再恢复全身关节位置的精确跟踪。

### 序列处理与高度后处理

对于完整运动序列，GMR 逐帧应用上述流程，并使用前一帧的重定向结果作为当前帧 Step 4 优化的初始猜测，以保证时序连续性。最后，通过计算序列中所有身体部位的最小高度，将其从全局平移中减去，以修正可能出现的全局浮动或地面穿透伪影。

## 实验与分析

### 核心瓶颈：重定向伪影如何破坏策略学习

运动重定向的核心矛盾在于人体与人形机器人之间存在显著的尺度差异。现有方法采用全局均匀缩放（ProtoMotions）或基于SMPL模型的拟合缩放（PHC），这两种策略在重定向过程中会引入三类典型伪影：**地面穿透**、**脚滑动**与**自相交**，以及**关节值突变**。当这些包含伪影的重定向结果作为参考动作输入强化学习策略时，策略需要同时学习模仿目标运动和补偿运动学不可行性，显著增加了学习难度。

**Fig. 3** 直观展示了低成功率重定向参考动作中的典型伪影：Dance 1序列中PHC重定向出现严重地面穿透；Run (stop & go)序列中ProtoMotions重定向产生自相交；Dance 5序列中GMR重定向出现关节值突变。这些伪影直接导致对应策略完全无法学习或成功率极低。这一发现揭示了重定向质量是运动跟踪策略性能的**因果性前置条件**——在缺乏大量奖励工程的情况下，低质量参考动作会从根本上限制策略的上限。

### 主结果：成功率与跟踪精度双重优势

**TABLE I** 汇总了各重定向方法在三种评估环境下的策略成功率。实验选取LAFAN1数据集中21个运动序列（时长5秒至2分钟，排除含非足部接触的动作），采用严格的成功定义：策略必须完整执行整个参考动作序列且无过早终止（如机器人倒地）。评估环境覆盖：

- **sim**：训练仿真器（IsaacSim），无域随机化，每策略100次试验
- **sim-dr**：训练仿真器，启用域随机化（含观测噪声、模型参数估计误差、网络延迟），每策略4096次试验
- **sim2sim**：MuJoCo/ROS环境模拟真实硬件部署条件，每策略100次试验

在21个序列中，有11个动作在所有重定向方法下均达到98%以上的成功率，表明这些动作本身对重定向质量不敏感。然而，在剩余挑战性序列上，方法间差异显著：基于Unitree闭源数据集训练的策略在所有动作上均接近完美性能，构成性能上界；GMR策略的成功率显著高于PHC和ProtoMotions，且在多数序列上接近Unitree水平。

**TABLE II** 给出了仿真环境（sim）下100次评估的跟踪误差定量比较。GMR的全局位置误差（E_g-mpbpe）均值为**104.1 mm**，相比PHC的247.8 mm降低143.7 mm（相对降低58.0%），相比ProtoMotions的139.7 mm降低35.6 mm（相对降低25.5%）。在关节角度误差（E_mpjpe）上，GMR均值为**561.7 × 10⁻³ rad**，同样显著优于PHC的778.5和ProtoMotions的643.4。这表明GMR重定向不仅提升了策略的成功率，也实质性地改善了跟踪的几何精度。

### 感知保真度：用户研究验证

为评估重定向动作对人类观察者的主观保真度，作者进行了双盲用户研究（N=20）。参与者观看源动作视频后，需从两个匿名重定向视频（GMR与Unitree/PHC/ProtoMotions之一）中选择更接近源动作的版本。每位参与者完成45组比较（15个动作 × 3种对比方法），视频顺序随机化。

**Fig. 4** 显示，GMR重定向动作的感知保真度显著优于PHC和ProtoMotions，且与闭源Unitree数据集的重定向结果接近。这一主观评估与客观成功率指标形成交叉验证，进一步确认GMR重定向质量的有效性。

### 消融发现：起始帧选择的关键影响

**TABLE III** 揭示了训练框架之外的一个重要影响因素：参考动作的起始帧选择。实验表明，同一策略从不同起始帧启动时，sim2sim环境下的成功率可在**14%至100%**之间剧烈波动。这一发现说明，重定向参考动作的初始姿态对策略的启动稳定性具有决定性影响——某些起始帧可能对应运动学上不稳定的姿态，导致策略在部署初期即失败。该结果也解释了TABLE I中部分序列成功率波动的原因（标注*的条目），并为实际部署中的参考动作预处理提供了重要指导。

### 公平性保障措施

实验设计中的公平性措施值得关注：
- 所有策略均使用独立的**BeyondMimic**框架训练，未针对任何重定向方法进行奖励函数调优或特殊域随机化
- 评估采用统一的严格成功标准，确保可比性
- sim2sim环境引入观测噪声、模型参数误差和网络延迟，模拟真实部署条件
- 用户研究采用双盲设计，排除主观偏差

### 失败模式与局限性

尽管GMR在整体上表现优越，分析仍揭示了若干值得关注的失败模式：

1. **关节值突变伪影**：GMR在极少数情况下仍可能出现优化伪影，如Dance 5序列中的关节值突然跳变（Fig. 3），默认参数无法完全消除此类问题。
2. **数据集局限性**：实验仅基于LAFAN1数据集，未在AMASS或单目视频重建等分布外动作数据上验证。
3. **机器人平台泛化性**：仅针对Unitree G1一款人形机器人评估，在其他形态差异较大的平台上的泛化性尚不明确。
4. **交互动作未覆盖**：未评估重定向方法对包含环境交互（与物体、场景或其他机器人）的运动序列的影响。

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2510_02252v1/figures/006_Figure_3.jpg]]
*Figure 3: Example artifacts found in the retargeted references with low success rates*

这些局限性指向若干开放问题：非均匀局部缩放策略在应对骨骼比例极端差异的非拟人形态时是否依然有效？两阶段优化中的权重能否根据运动类型自动调整以减少手动调参需求？如何建立通用启发式规则来确定安全的起始与结束帧？

### 补充图表

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2510_02252v1/figures/003_Table.jpg]]
*Table: I: Evaluation success rates (%) in IsaacSim (training simulator) without domain randomization (sim, 100 trials per policy), with domain randomization (sim-dr, 4096 trials per policy), and MuJoCo/ROS simulator (sim2sim, 100 trials per policy). PM = ProtoMotions, U = Unitree. *See Section V-D TABLE II: Tracking errors for each policy measured over the 100 evaluation rollouts in the sim setting. Lower values are better. Best values are bold, second best are underlined*

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2510_02252v1/figures/004_Figure.jpg]]
*Figure: (a) Ground penetration (PHC, “Dance 1”) (b) Self-intersection (ProtoMotions, “Run (stop & go)”) (c) Sudden jumps in the waist roll and pitch values (GMR, “Dance 5”)*

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2510_02252v1/figures/005_Table.jpg]]
*Table: III: Evaluation success rates (%) in sim2sim (Mu-JoCo) as a function of the start frame of the reference motion. PM = ProtoMotions, U = Unitree*

![[assets/figures/papers/paper_list_l38_https_arxiv_org_abs_2510_02252v1/figures/001_Figure_1.jpg]]
*Figure 1: For the user study, participants were shown videos of the reference motion (a), and asked to choose which retarget video (b) was more similar to it*

## 方法谱系与知识库定位

### 与现有重定向方法的关系

GMR 直接对标的是当前人形机器人运动跟踪社区中两种主流的运动重定向范式，二者在尺度变换策略上的根本差异构成了 GMR 的核心改进动机。

**PHC 重定向**（Luo et al., ICCV 2023; He et al., 2024）采用基于 SMPL 模型的拟合缩放。其流程先将源运动拟合到 SMPL 人体模型，再从 SMPL 模型中提取关节位置作为目标，通过最小化机器人关节与目标位置间的 L2 误差来求解姿态。这一范式的瓶颈在于：SMPL 拟合本身可能引入误差，且全局性的模型缩放无法处理人体与机器人特定身体部位（如上臂、大腿）间的比例差异，导致重定向结果中出现严重的地面穿透和脚滑动伪影。实验证据表明，PHC 重定向在 “Dance 1” 序列中产生了明显的地面穿透，其训练策略的全局位置误差（E_g-mpbpe）高达 247.8 mm，约为 GMR 的 2.4 倍。

**ProtoMotions 重定向**（Tessler et al., 2024）使用 Mink 差分 IK 进行优化，在尺度变换上采用全局轴对齐缩放。该方法将源运动关节沿各轴进行统一缩放后，最小化缩放后人体与机器人关键身体间的关节位置和朝向误差。其瓶颈在于全局均匀缩放忽略了不同身体部位的长度比例差异，导致 “Run (stop & go)” 等序列中出现自相交伪影。ProtoMotions 训练策略的全局位置误差为 139.7 mm，虽优于 PHC，但仍显著高于 GMR 的 104.1 mm。

GMR 与上述方法的本质区别在于三个关键设计槽位的变化：

1. **尺度变换策略**：从全局均匀缩放（ProtoMotions）或 SMPL 拟合缩放（PHC）转向非均匀局部缩放。GMR 为每个关键身体部位定义独立的局部缩放因子 s_b，同时使用基于身高比例 h/h_ref 的统一缩放框架。特别地，对根位移采用统一缩放因子 s_root，而非各轴独立缩放，这被证明是避免脚滑动伪影的关键——“We find that scaling the root translation by a uniform scaling factor is crucial to avoid introducing foot sliding artifacts.”

2. **优化策略**：从单阶段优化转向两阶段优化。第一阶段仅优化身体朝向和末端执行器位置误差，忽略中间身体的位置约束，以获得粗略但无穿透的初始解；第二阶段使用不同于第一阶段的权重，同时优化所有关键身体的朝向和位置误差，并以关节限位为约束进行微调。这种分阶段策略有效避免了单阶段优化中目标冲突导致的局部最优问题。

3. **源运动格式**：GMR 直接兼容 BVH 格式输入，无需经过 SMPL 或 SMPL-X 的中间格式转换，消除了格式转换环节可能引入的额外误差。

### 在运动跟踪知识库中的定位

GMR 在人形机器人运动跟踪的完整知识链中扮演**上游参考动作生成器**的角色，其设计哲学与下游策略训练框架解耦。论文明确采用 **BeyondMimic** 作为独立的策略训练框架，所有对比方法（PHC、ProtoMotions、Unitree、GMR）均使用相同的策略训练流程，未针对任何重定向方法进行奖励函数调优或特殊域随机化。这种解耦设计使得重定向方法的效果可以被独立归因，而非与策略训练的超参数调优混淆。

从技术谱系上看，GMR 继承了基于逆运动学的优化重定向传统（与 PHC、ProtoMotions 同属优化范式，区别于基于学习的重定向方法），但在尺度变换和优化策略上引入了关键创新。其非均匀局部缩放的思想与机器人运动学中的身体部位特异性建模理念一致，而两阶段优化策略则借鉴了分层求解的思想——先保证末端执行器的全局约束，再微调全身姿态。

与闭源的 **Unitree 重定向数据集**相比，GMR 在感知保真度和策略成功率上均达到了接近上界的水平。用户研究（N=20）显示，GMR 重定向动作的感知保真度显著优于 PHC 和 ProtoMotions，与 Unitree 数据集的重定向结果接近。在策略成功率方面，Unitree 数据训练的策略在所有 21 个测试序列上均达到近乎完美的表现，而 GMR 在多数序列上也取得了 98% 以上的成功率，验证了高质量重定向对下游策略性能的决定性影响。

### 适用边界与局限

**已知局限**：

1. **运动数据分布**：实验仅基于 LAFAN1 数据集的 21 个序列进行评估，未在 AMASS 或单目视频重建等其他分布的动作数据上验证泛化性。LAFAN1 序列排除了涉及非足部接触的动作，因此 GMR 在处理爬行、翻滚等全身接触动作时的表现尚不明确。

2. **机器人平台单一性**：仅针对 Unitree G1 一款人形机器人进行了评估。该机器人的骨骼比例与人体较为接近，GMR 在形态差异更大的人形平台（如上半身比例显著不同或具有非拟人关节配置的机器人）上的泛化性尚不明确。

3. **环境交互缺失**：未评估重定向方法对包含环境交互（如与物体、场景或其它机器人互动）的运动序列的影响。在需要精确接触约束的场景中，纯运动学优化可能无法保证物理可行性。

4. **残余伪影**：GMR 在极少数情况下仍可能出现优化伪影，如 “Dance 5” 序列中观察到的腰部关节值突然跳变。默认参数并非对所有运动类型都能完全消除此类问题，可能需要针对特定运动进行参数调整。

**开放性研究问题**：

- **极端形态差异**：GMR 的非均匀局部缩放策略在应对人类与机器人骨骼比例极端差异的非拟人形态时是否依然有效？当机器人缺少某些关键身体部位（如无头部或无独立腕关节）时，关键身体映射的自动生成策略如何设计？

- **自适应权重**：两阶段优化中的权重能否根据运动类型或动态程度自动调整？当前权重需手动设定，对于高频动态运动与缓慢舞蹈动作，最优权重配置可能显著不同，自适应机制有望减少手动调参需求。

- **起始帧鲁棒性**：消融实验揭示了一个重要的脆弱性来源——参考动作的起始帧选择对策略成功率有显著影响，同一策略从不同帧启动，成功率可在 14% 到 100% 之间波动。如何建立通用启发式规则来确定安全的起始与结束帧，保证策略在任意运动中稳定启动和停止，是一个尚未解决的问题。

- **多平台扩展**：该重定向方法能否无缝扩展至多款人形机器人平台？如何自动生成高质量的关键身体映射，以及如何根据机器人运动学约束自动调整局部缩放因子，是实现 “一次重定向，多平台部署” 的关键挑战。

## 原文 PDF

![[paperPDFs/arxiv_2025/Retargeting_Matters_General_Motion_Retargeting_for_Humanoid_Motion_Tracking.pdf]]

---
title: "MobileH2R: Learning Generalizable Human to Mobile Robot Handover Exclusively from Scalable and Diverse Synthetic Data"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusively_from_Scalable_and_Diverse_Synthetic_Data.pdf
project_link: https://MobileH2R.github.io
code_link: null
aliases:
- MobileH2R
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 合成人体运动数据的规模与多样性、安全且利于模仿的演示生成管线、融合4D点云输入与协调基座-臂部动作输出的策略网络。
primary_logic: 可泛化的交接技能可在模拟器中仅使用高质量合成数据（人体运动、物体资产和机器人演示）进行开发，无需真实世界演示。
claims:
- Our method outperforms baselines in all settings, achieving at least +15% improvement in success rate.
- Scaling up demonstrations to 100k improves success rate by 3.3% on average over 10k, while 1k leads to 13.9% decrease.
- Future obstacle avoidance and imitation-friendly losses reduce human contacts by about 1/3 and increase success rate by 11.6%.
- m0 (简单人体运动) 上 成功率 (%) = 63.80
---

# MobileH2R: Learning Generalizable Human to Mobile Robot Handover Exclusively from Scalable and Diverse Synthetic Data

> [!tip] 核心洞察
> 可泛化的交接技能可在模拟器中仅使用高质量合成数据（人体运动、物体资产和机器人演示）进行开发，无需真实世界演示。

| 字段 | 内容 |
|------|------|
| 中文题名 | MobileH2R：从可扩展多样的合成数据中学习可泛化的人到移动机器人交接 |
| 英文题名 | MobileH2R: Learning Generalizable Human to Mobile Robot Handover Exclusively from Scalable and Diverse Synthetic Data |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://MobileH2R.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MobileH2R |
| Dataset | m0, n0, s0 |

> [!tip] 效果简介
> - m0 (简单人体运动) 上，成功率 (%) 63.80 vs 46.80 (GenH2R reprod.) (+17.0%)。
> - n0 (复杂人体运动) 上，成功率 (%) 53.40 vs 32.90 (GenH2R reprod.) (+20.5%)。
> - s0 (真实mocap数据) 上，成功率 (%) 77.78 vs 61.11 (GenH2R reprod.) (+16.7%)。

## 概要

人向移动机器人（mobile robot）的物体交接（handover）要求机器人同时协调**移动基座**与**机械臂**的动作，并在动态人类面前保持安全交互。然而，现有方法面临两大瓶颈：**大规模、多样化且安全的合成训练数据匮乏**，以及**缺乏有效的端到端移动底盘-机械臂协同交接策略学习方法**。

针对上述问题，本文提出 **MobileH2R**——一个完全在模拟器中利用高质量合成数据学习可泛化交接技能的框架。其核心洞察是：**可泛化的交接技能可以在模拟器中仅使用合成数据（人体运动、物体资产和机器人演示）进行开发，无需任何真实世界演示**。

MobileH2R 围绕三个关键模块构建：
- **可扩展的多样化全身人机交接运动合成管线**：利用生成式人体运动扩散模型（GMD）、大语言模型提示与运动学优化，合成大规模、多样化的交互式全身运动数据。
- **安全且利于模仿的演示自动生成管线**：基于 CHOMP 规划器，通过未来时间窗口内的障碍物回避、最终姿态约束以及视觉神经损失，生成既安全又易于策略模仿的机器人轨迹。
- **场景融合的 4D 模仿学习策略**：以双相机分割点云与 ICP 流为输入，通过 PointNet++ 编码器提取 4D 场景特征，直接输出 9D 协调动作（6D 机械臂末端动作 + 3D 移动基座动作），实现端到端的基座-臂部协同控制。

实验表明，MobileH2R 在所有测试场景下均显著优于基线方法，**成功率提升至少 15%**（Table 1）。消融实验进一步验证了各设计选择的有效性：将演示数量从 1k 扩展到 100k 可使成功率平均提升 3.3%（Table 2）；未来障碍避免与视觉神经损失使人体接触率降低约 1/3，成功率提升 11.6%（Table 3）。在真实世界实验中，MobileH2R 同样展现出稳定的 sim-to-real 迁移能力（Table 5, Table 9）。



人机交接（Human-to-Robot Handover）是服务机器人实现物理协作的核心环节，要求机器人在动态环境中安全、高效地从人类手中接过物体。然而，当机器人具备移动能力时，交接任务面临双重挑战：机器人不仅需要精准控制机械臂末端抵达交接位置，还必须协调移动底盘的位姿以应对人的运动，确保在接近过程中不发生碰撞。现有方法大多依赖真实世界遥操作或人类演示数据进行策略学习，但这类数据的采集成本高昂、场景覆盖有限，难以支撑大规模训练，导致策略在未见人体运动、新物体或复杂场景下的泛化能力严重不足。

合成数据为解决数据匮乏提供了潜在路径，但直接将现有合成数据生成范式应用于移动交接任务仍存在三个关键缺口。第一，缺乏能够生成大规模、多样化且交互式全身人体运动的合成管线——现有工作或局限于简单的轨迹随机化，或仅覆盖有限的动作捕捉子集，无法模拟交接过程中人的自然移动、手臂伸出与姿态变化。第二，自动生成的机器人演示往往忽视安全性与可模仿性：基于当前时刻的碰撞检测无法规避未来时间窗口内的潜在接触，且未显式优化视觉-动作关联，导致生成的轨迹难以被视觉策略有效学习。第三，固定基座的端到端交接策略（如 **GenH2R**）仅输出6自由度机械臂动作，无法同时协调移动底盘的3自由度运动，难以在移动场景中实现基座-臂部的协同控制。

上述缺口共同构成了一个根本性瓶颈：**大规模、多样化且安全的合成训练数据匮乏，同时缺乏有效的模拟器中端到端移动底盘-机械臂协同交接策略学习方法**。针对这一瓶颈，MobileH2R 提出了一条完整的合成数据驱动框架，核心假设是：**可泛化的移动交接技能可以在模拟器中仅使用高质量合成数据（人体运动、物体资产和机器人演示）进行开发，无需真实世界演示**。该框架通过三个技术模块协同作用——可扩展的全身运动合成管线、安全且利于模仿的演示自动生成方法，以及融合4D场景信息的模仿学习策略——从数据、演示到策略层面系统性地填补了上述缺口。



## 核心方法与创新机理

MobileH2R 的核心创新在于构建了一套全合成数据驱动的端到端移动交接框架，通过三大关键槽位（changed slots）的系统性升级，解决了从固定基座交接向移动基座-机械臂协同交接泛化的瓶颈。

### 1. 动作空间：从6D机械臂到9D基座-臂部协同控制

最根本的架构创新在于将策略输出从传统的6D机械臂末端动作（3D平移+3D旋转）扩展为9D协同动作空间，同时输出6D机械臂动作和3D移动基座动作（2D平移+1D旋转）。这一设计使得策略能够学习基座与臂部的协调配合，而非将移动基座仅作为独立的定位模块。消融实验（Table 4）表明，将臂部与基座动作分离解码会导致成功率下降17.8%，验证了联合输出9D动作的必要性。对应的监督信号采用加权损失函数：

$$\mathcal{L} = \lambda_{1} \mathcal{L}_{\mathrm{base}} + \lambda_{2} \mathcal{L}_{\mathrm{arm}} + \lambda_{3} \mathcal{L}_{\mathrm{pred}}$$

其中基座损失、臂部损失与抓取预测损失共同约束9D动作的学习（Section 3.3）。

### 2. 人体运动生成：从受限子集到两阶段多样化全身合成

基线方法（如GenH2R）依赖简单随机化的手-物体轨迹或受限的动作捕捉子集，缺乏全身运动的多样性和真实感。MobileH2R引入两阶段合成管线（Section 3.1, Figure 2）：
- **预交接阶段**：利用Guided Motion Diffusion（GMD）扩散模型，结合大语言模型提示和AMASS数据集先验，生成多样化的全身运动；
- **交接阶段**：通过任务专用运动学优化器合成手臂动作，在关节约束和交接先验下优化手部关节参数，并注入适当随机化以增强多样性。

这一管线使得合成数据的规模和多样性远超基线，实验表明将演示数量从10k扩展到100k可使平均成功率提升3.3%，而缩减至1k则导致13.9%的下降（Table 2），直接验证了大规模多样化数据的关键作用。

### 3. 演示生成：从当前碰撞检测到未来安全与模仿友好优化

基线演示生成仅基于当前时刻的碰撞检测，缺乏对未来动态的考虑和视觉-动作关联的显式优化。MobileH2R在CHOMP规划器中引入两项关键改进（Section 3.2, Figure 3）：
- **未来障碍物回避**：在时间窗口内预测并避免人机碰撞，同时约束机器人最终姿态位于人前方。消融实验（Table 3）显示，移除未来障碍避免导致成功率下降4.0%，人体接触率从10.9%升至16.1%；
- **视觉神经损失**：通过姿态预测网络（Pose Prediction Network）和状态恢复估计器（Vision-State Recovery Estimator）间接优化视觉-动作关联，使生成的演示更易于视觉策略模仿。该设计使成功率提升11.6%，人体接触减少约1/3。

### 4. 感知架构：场景融合4D点云输入

策略网络采用双相机（头部+腕部）点云分割与ICP流估计，通过区分采样半径的PointNet++编码器融合人体、手部和物体的4D场景特征（Section 3.3）。消融实验（Table 4）表明，移除点云流信息导致成功率平均下降12.1%，移除人体信息导致下降12.5%，仅使用头部相机则下降13.5%~27.1%（Table 8），证明了4D多源融合的必要性。

**证据强度评估**：上述创新点均有消融实验支撑（置信度0.95），核心结论来自Table 1-4的多维度对比。需注意当前框架基于Galbot机器人（3-DoF全向基座+7-DoF臂）验证，对其他形态的泛化性尚未检验。



MobileH2R 构建了一套从合成数据生成到移动机器人交接策略学习的完整流水线，其核心逻辑是：**在模拟器中仅使用高质量合成数据（人体运动、物体资产与机器人演示）开发可泛化的交接技能，无需任何真实世界演示**。框架由三个紧密耦合的模块组成（Figure 1、Figure 2）：

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/001_Figure_1.jpg]]
*Figure 1: The overview of MobileH2R. We propose a framework for generalizable human-to-mobile-robot handover, including a scalable pipeline for diverse full-body human motion synthesis (a), an automatic method for producing safe, imitation-friendly demonstrations (b), an efficient 4D imitation learning approach to learn coordinated base-arm actions (c), and successful sim2real transfer (d)*

1. **可扩展多样化全身人机交接运动合成管线（MobileH2R-Sim）**：负责大规模生成包含全身运动与手-物体交互的合成数据。该管线采用两阶段设计——预交接阶段利用 Guided Motion Diffusion (GMD) 扩散模型生成多样化全身运动，交接阶段通过任务专用运动学优化器合成手臂动作，并结合大语言模型提示、SMPL-X 整合与 DexGraspNet 物体抓取姿态，最终输出高多样性的交互式全身运动序列。

2. **安全且利于模仿的演示自动生成管线**：以 CHOMP 优化规划器为专家，在轨迹优化中引入未来时间窗口内的障碍物回避与最终姿态约束，确保演示的安全性；同时设计视觉神经损失（Figure 3），通过姿态预测网络与状态恢复估计器间接优化视觉-动作关联，使生成的演示更易于下游策略模仿。

3. **场景融合 4D 模仿学习策略**：接收双相机（头部与腕部）分割后的人体、手部与物体点云数据，通过 ICP 流估计与区分采样半径的 PointNet++ 编码器提取 4D 场景特征，最终输出 9D 协调控制动作（6D 机械臂末端位姿 + 3D 移动基座动作），实现端到端的基座-臂部协同交接。

**输入输出流**：系统输入为双相机实时点云（经 SAM2 分割后的人体、手、物体区域），输出为增量式 9D 位置指令。训练阶段以加权损失函数 $\mathcal{L} = \lambda_{1} \mathcal{L}_{\mathrm{base}} + \lambda_{2} \mathcal{L}_{\mathrm{arm}} + \lambda_{3} \mathcal{L}_{\mathrm{pred}}$ 监督基座动作、臂部动作与抓取预测，实现从感知到动作的直接映射。

**关键设计决策**：与固定基座端到端方法 GenH2R（仅输出 6D 臂部动作）相比，MobileH2R 将动作空间扩展为 9D 协调控制，避免了通过逆运动学间接求解基座动作带来的信息损失；与基于抓取估计与规划的“Grasp Selection + Trajectory Planning”非端到端基线相比，MobileH2R 的端到端范式消除了模块间误差累积，在复杂人体运动场景（n0）中成功率提升达 20.5%（Table 1）。



### 模块一：可扩展多样化全身交接运动合成管线

该管线旨在以自动化方式大规模生成多样化的人体全身交接运动数据，解决真实数据稀缺与多样性不足的瓶颈。其核心流程分为两个阶段：

- **预交接阶段：基于GMD的全身运动生成。** 利用在AMASS数据集上预训练的引导式运动扩散模型（Guided Motion Diffusion, GMD），通过大语言模型生成多样化的文本提示，驱动GMD产生丰富的全身运动序列。生成的SMPL参数可直接驱动人体模型。
- **交接阶段：任务专用手臂运动学优化。** 将预交接阶段的身体运动与来自DexGraspNet的MANO手-物体抓取姿态进行整合（Figure 6）。随后，手臂运动学优化器在关节约束和交接任务先验（如手部最终位置应位于人体前方适当区域）下，求解最优的手臂关节参数，并引入适当的随机化以增强数据多样性（Figure 7）。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/010_Figure_6.jpg]]
*Figure 6: Combine the body motion and the hand-object pose. In our pipeline, the body motions are SMPL [29] parameters obtained from GMD [23], and the hand-object poses are MANO [42] parameters obtained from DexGraspNet [47]. Here we combine these parameters with SMPL-X [38] model, as well as update the object poses relative to the human body*

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/011_Figure_7.jpg]]
*Figure 7: Visualization for the arm kinematic optimizer. Given the final pose of the hand, the optimizer determines the optimal hand joint parameters by optimizing under joint constraints and handover task priors. Practically, we add proper randomization to generate diverse data*

该管线将合成数字资产库、生成模型与运动学工具链深度整合，实现了从大规模数据中蒸馏人体运动先验，再针对交接任务进行条件化精炼的数据生成范式。

### 模块二：安全且利于模仿的演示自动生成管线

该模块的核心目标是自动生成既安全（避免人机碰撞）又利于后续策略模仿（视觉-动作关联强）的机器人演示轨迹。它以CHOMP优化规划器为基础，引入了三项关键改进：

- **未来障碍物回避（Future Obstacle Avoidance）。** 不同于仅检测当前时刻碰撞的常规做法，该方法在规划的时间窗口内显式约束机器人与动态人体之间的未来碰撞，从而生成具有预见性的安全轨迹。
- **最终姿态约束（Final Pose Constraints）。** 强制机器人末端执行器在交接完成时的最终姿态位于人体前方可达区域，确保交接动作的自然性与可完成性。
- **视觉神经损失（Vision Neural Loss）。** 这是提升演示“可模仿性”的关键创新。如Figure 3所示，其机制为：
    1. 训练一个**姿态预测网络**，以视觉输入（点云）预测物体姿态，其预测误差定义为视觉神经损失。
    2. 训练一个**视觉-状态恢复估计器**，以状态为输入，估计上述视觉神经损失。
    3. 在基于状态的轨迹优化过程中，该估计器作为可微分的代理损失函数，引导规划器隐式地优化视觉-动作关联，使得生成的演示轨迹更容易从视觉观测中学习。

### 模块三：场景融合4D模仿学习策略

该策略网络将4D场景特征映射为9D协调动作，实现端到端的移动底盘-机械臂协同控制。

- **输入表示：4D场景点云。** 从头部和腕部两个相机获取RGB-D图像，利用SAM2进行实时分割，提取人体、手部和物体的点云。通过ICP算法计算两帧之间的点云流，为网络提供显式的运动信息。最终形成融合空间几何与时间动态的4D输入。
- **网络架构：差异化采样半径的PointNet++。** 针对不同语义部分（人体、手部、物体）采用不同的采样半径进行层次化特征提取，以捕捉不同尺度的几何结构。提取的特征进行场景融合编码。
- **输出与监督：9D协调动作。** 网络同时输出6D机械臂末端动作（3D平移 + 3D旋转）和3D移动基座动作（2D平移 + 1D旋转），形成9D协调控制指令。训练采用行为克隆范式，损失函数为基座损失、臂部损失与抓取预测损失的加权和：

$$
\mathcal{L} = \lambda_{1} \mathcal{L}_{\mathrm{base}} + \lambda_{2} \mathcal{L}_{\mathrm{arm}} + \lambda_{3} \mathcal{L}_{\mathrm{pred}}
$$

其中 $\mathcal{L}_{\mathrm{base}}$ 为基座动作的均方误差，$\mathcal{L}_{\mathrm{arm}}$ 为臂部动作的均方误差，$\mathcal{L}_{\mathrm{pred}}$ 为辅助抓取姿态预测任务的交叉熵损失。该联合损失函数驱动网络学习基座与臂部的协调运动模式，以及从场景感知中推断抓取意图的能力。

### 补充图表

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our framework. First, we propose an automatic pipeline to scale up synthetic and diverse full-body motion data for the handover task by integrating various synthetic digital asset libraries, generative models, and useful toolkits. Second, we introduce an automatic pipeline to scale up mobile robot demonstrations for safety and imitation-friendliness. Our approach aims to avoid collisions while enhancing the vision-action correlation through carefully designed loss functions. Third, we employ a 4D imitation learning policy to learn 9D coordinated arm-base actions. We process point clouds of both objects and human bodies by modified PointNet++*

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/003_Figure_3.jpg]]
*Figure 3: Visualization for the vision neural loss. The Pose Prediction Network takes vision inputs and predicts the object pose. The prediction error is defined as the vision neural loss. The Vision-State Recovery Estimator takes states as input and estimates the vision neural loss, guiding the state-based trajectory optimization towards imitation-friendly demonstration generation*



## 实验与关键发现

### 4.1 整体性能对比

MobileH2R 在三个测试集上对所有基线方法均取得显著优势（Table 1）。在简单人体运动场景 m0 中，MobileH2R 成功率达到 63.80%，比最佳基线 GenH2R (reprod.) 高出 17.0 个百分点；在复杂场景 n0 中，成功率为 53.40%，领先 20.5 个百分点；在真实 mocap 数据 s0 上，成功率高达 77.78%，领先 16.7 个百分点。平均成功指标（AS，定义为 $\mathrm{AS} = \int_{0}^{1} \mathrm{Success}(t) \mathrm{d} t$）同样全面领先，m0 上为 34.81，n0 上为 28.68，s0 上为 50.65，表明 MobileH2R 不仅成功率高，且完成任务的速度更快。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/004_Table_1.jpg]]
*Table 1: Evaluation on different methods. We compare our method against baselines across three test sets: the relatively simple humaninvolved scenario ”m0”, complex scenarios ”n0”, and real mocap data ”s0”. The ”time” metric combines both computation and execution time. Since computation time varies depending on GPU and CPU configurations, we standardized it using an idle RTX 3090 with 32 CPU cores. Our policy outperforms the baselines in success rate and average success, while maintaining relatively low time cost*

与基于抓取选择加轨迹规划的非端到端方法相比，MobileH2R 在 n0 场景下成功率提升 26.3%，时间缩短 5.06 秒，AS 提升 28.6%。与固定基座端到端交接方法 GenH2R 相比，MobileH2R 的优势主要来自 9D 协调动作空间——GenH2R 仅输出 6D 臂部动作，基座通过逆运动学求解，缺乏端到端协调能力。所有方法均在相同 10k n0 训练场景上训练，评估硬件统一为 RTX 3090 与 32 CPU 核心，时间指标同时包含推理与动作执行时间。

### 4.2 数据规模与资产多样性消融

Table 2 展示了演示数量与资产多样性的影响。将演示数量从 10k 扩展到 100k，三个测试集上的平均成功率提升 3.3%，表明大规模合成数据持续带来收益。相反，将演示缩减至 1k 导致成功率平均下降 13.9%，证明充足的数据规模是策略泛化的必要条件。在资产多样性方面，增加物体和场景资产种类同样带来正向收益，验证了合成数据管线在覆盖视觉与交互多样性方面的有效性。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/005_Table_2.jpg]]
*Table 2: Evaluation on varying demonstration numbers and Assets. We compare the policy’s success rate across three testing sets, examining the impact of different demonstration sizes within brown braces and asset variations within green braces*

### 4.3 演示生成策略消融

Table 3 系统评估了安全与利于模仿的演示生成策略的贡献。移除未来障碍避免（FOA）后，成功率下降 4.0%，同时人体接触率从 10.9% 升至 16.1%（Table 7），表明未来时间窗口内的碰撞检测对安全交接至关重要。移除最终姿态约束（FPC）同样导致成功率下降。两项安全策略联合作用使人体接触减少约 1/3，成功率提升 11.6%。视觉神经损失（Figure 3）通过姿态预测网络与状态恢复估计器间接优化视觉-动作关联，使策略更容易从视觉输入中学习演示行为，消融实验证实其对成功率的正向贡献。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/006_Table_3.jpg]]
*Table 3: Evaluation on different demonstration generation strategies. We compare the policy’s success rate across three testing sets. They all trained on “n0”*

### 4.4 策略设计消融

Table 4 揭示了 4D 模仿学习策略各模块的关键作用。移除点云流信息导致成功率平均下降 12.1%，说明 ICP 流估计提供的时序动态信息对理解人-物运动趋势不可或缺。移除人体信息使成功率下降 12.5%，验证了融合人体点云对交接意图理解的重要性。将臂部与基座动作分离解码导致成功率大幅下降 17.8%，这是所有消融中影响最大的单一因素，充分证明 9D 协调动作空间的必要性。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/009_Table_4.jpg]]
*Table 4: Ablations on different policy designs. We conduct ablations on various modules, including flow information, human information, and coordinated base-arm actions*

在感知输入方面（Table 8），仅使用头部相机导致成功率下降 13.5% 至 27.1%，表明手腕相机提供的近距离手部-物体细节对精确抓取至关重要。不同融合策略的对比进一步确认了区分采样半径的 PointNet++ 编码器在整合多源点云信息方面的优势。

### 4.5 失败模式分析

Table 6 按训练场景细分了失败类型。主要失败模式包括人体接触（Contact）和物体掉落（Drop）。在复杂场景 n0 中，人体接触率约为 10.9%，物体掉落率约为 15.7%。当训练数据仅包含简单场景 m0 时，在 n0 上的接触率升至 18.6%，表明训练场景的复杂度直接影响策略的安全性。使用 n0 数据训练可显著降低接触和掉落率，验证了合成复杂人体运动数据的价值。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/012_Table_6.jpg]]
*Table 6: Evaluation on different training scenes. We train our method on three training sets and evaluate it across three test sets: the relatively simple human-involved scenario (”m0”), complex scenarios (”n0”), and real mocap data (”s0”). ”Contact” means human contact, ”Drop” means object drop*

### 4.6 Sim-to-Real 迁移

Table 5 展示了真实世界实验的定量结果。MobileH2R 在简单与复杂两种设置下均显著优于 GenH2R (reprod.)。用户研究（Table 9）由五名参与者对六种物体进行评估，MobileH2R 在真实移动交接系统中的成功率始终高于基线，与仿真实验结果一致。失败场景主要包括与人体碰撞、物体掉落或超时（$T_{max} = 25$ 秒）。Figure 4 提供了仿真与真实场景下的定性对比，直观展示了 MobileH2R 在协调基座-臂部动作和避障方面的优势。

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results. We compare different methods in detail in the simulated scene and the real-world scene*

![[assets/figures/papers/paper_list_l1741_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusiv/figures/017_Table_9.jpg]]
*Table 9: User study for sim-to-real experiments. our method and GenH2R(reprod.) method were evaluated by five individuals for six objects in both the simple and complex settings. Failure scenarios included collisions with the human body, dropping on the ground, or exceeding the time limit*



## 定位与知识库关联

### 1. 与现有基线的系统化关系

MobileH2R 在人到移动机器人交接任务上构建了一套完整的合成数据驱动框架，其定位可以通过与三类代表性基线的对比来精确刻画。

**（1）非端到端规划基线：Grasp Selection + Trajectory Planning**

该基线代表了一种经典的模块化范式：先估计抓取姿态，再执行轨迹规划。MobileH2R 与之相比，在 m0 简单场景上成功率提升 26.3%，时间缩短 5.06 秒，平均成功（AS）提升 28.6%（见 Section 4.1）。这一巨大差距揭示了一个因果瓶颈：模块化管道中的误差累积——抓取估计的微小偏差会被规划器放大，而 MobileH2R 的端到端 9D 动作输出绕过了这一脆弱环节。

**（2）固定基座端到端基线：GenH2R**

GenH2R 是 MobileH2R 最直接的前身，它证明了端到端模仿学习在固定基座交接上的可行性，但仅输出 6D 臂部动作。MobileH2R 将其动作空间扩展为 9D 协调控制（6D 臂部 + 3D 基座），这一架构变更在 n0 复杂场景上带来 20.5% 的绝对成功率提升（53.40% vs. 32.90%，Table 1）。这验证了核心假设：移动基座不仅是空间可达性的补充，更是动态调整机器人整体位姿以适应人体运动的关键自由度。

**（3）重训练基线：GenH2R (reprod.)**

该基线在 MobileH2R 的 n0 数据上重训练 GenH2R，虽增加了移动基座但通过逆运动学求解。其性能仍显著低于 MobileH2R（m0: 46.80% vs. 63.80%；s0: 61.11% vs. 77.78%），这排除了“数据质量差异”作为主要解释，将性能增益归因于 MobileH2R 的独特设计：场景融合 4D 点云编码、9D 协调动作解码、以及安全且利于模仿的演示生成策略。

### 2. 适用边界与泛化约束

MobileH2R 的成功建立在一组明确的技术前提之上，这些前提也划定了其当前适用边界：

- **机器人形态依赖**：当前实验基于 Galbot 机器人（3-DoF 全向基座 + 7-DoF 机械臂）。对于双足人形机器人或其他运动形态，策略网络架构可能需要重新设计，泛化能力未经验证。
- **控制模态限制**：策略输出为增量位置指令，依赖鲁棒的位置控制器。未考虑速度控制或力控等更先进的控制模态，这限制了交互柔顺性的进一步提升空间。
- **感知鲁棒性边界**：真实世界部署中，SAM2 分割和深度相机偶尔产生噪声与误差。策略未经过随机扰动训练或混合真实数据微调，对感知异常的鲁棒性仍有提升空间。
- **人类行为覆盖**：合成数据虽具有规模和多样性优势，但可能未覆盖真实世界中对抗性、非合作或高度动态的人类行为。框架尚未与强化学习等方法进行对比，复杂交互场景下 RL 的安全性挑战未深入探讨。

### 3. 局限与开放问题

基于上述边界，以下开放问题值得后续工作关注：

1. **跨形态迁移**：如何将 9D 协调控制框架扩展到双足人形机器人或其他先进平台？不同运动形态可能需要专用策略网络设计，而非简单的参数调整。
2. **控制模态升级**：如何从当前位置控制扩展为力控或速度控制，以提升交互柔顺性和安全性？这需要重新设计演示生成管线和策略输出表示。
3. **感知鲁棒性增强**：如何通过训练中注入随机扰动或结合少量真实数据微调，增强策略对真实世界感知噪声的鲁棒性？合成数据与真实数据的混合训练策略值得探索。
4. **安全探索机制**：是否可以在保持安全性的前提下引入强化学习，以应对更动态、对抗性的人类行为？这需要在安全约束与探索效率之间找到平衡点。
5. **sim2real 鸿沟弥合**：如何将合成数据与真实数据混合训练，以进一步缩小 sim2real 鸿沟并提高在非结构化环境中的表现？当前 sim2real 实验仅覆盖有限场景（Table 5），更广泛的真实世界评估是必要的。



## 原文 PDF

![[paperPDFs/CVPR_2025/MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Handover_Exclusively_from_Scalable_and_Diverse_Synthetic_Data.pdf]]

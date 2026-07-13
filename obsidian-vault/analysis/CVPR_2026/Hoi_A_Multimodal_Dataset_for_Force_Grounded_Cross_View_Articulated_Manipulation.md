---
title: Hoi! - A Multimodal Dataset for Force-Grounded, Cross-View Articulated Manipulation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hoi_A_Multimodal_Dataset_for_Force_Grounded_Cross_View_Articulated_Manipulation.pdf
project_link: "https://hoi-dataset.ethz.ch"
code_link: null
aliases:
- HDCAP
- HMDFGCVAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 数据集提供的同步多模态力触觉信号与多视角对齐，使得研究者可以直接研究视觉外观与物理力模式之间的关联，并评估跨执行器泛化。
primary_logic: 通过联合捕获视觉、力和触觉信号，并在人类与机器人执行同一任务时进行对齐，可以建立视觉感知与触觉动作之间的桥梁，从而促进操作技能的跨实体迁移。
claims:
- 数据集包含3048条序列、381个关节物体和38个环境，覆盖四种执行器（人手、手+腕部相机、UMI夹爪、Hoi!夹爪），均配合同步的RGB-D、力/扭矩、触觉及多视角视频。
- Hoi!夹爪集成了GelSight Digit触觉传感器和6-DoF力/扭矩传感器，首次实现了野外环境中对关节操纵力的精确记录。
- 现有视觉力预测模型ForceSight在Hoi!上的RMSE显著升高（如kitchen_7达3.531 N，而原数据集为0.404 N），突显了域适应和力-视觉对齐的挑战。
- 该数据集填补了先前数据集中缺少力触觉传感、多视角和跨执行器对齐记录的空白（见表1），为力来自视觉、关节参数估计、跨视角迁移等研究提供基准。
---

# Hoi! - A Multimodal Dataset for Force-Grounded, Cross-View Articulated Manipulation

> [!tip] 核心洞察
> 通过联合捕获视觉、力和触觉信号，并在人类与机器人执行同一任务时进行对齐，可以建立视觉感知与触觉动作之间的桥梁，从而促进操作技能的跨实体迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | Hoi! - 面向力觉与跨视角关节操纵的多模态数据集 |
| 英文题名 | Hoi! - A Multimodal Dataset for Force-Grounded, Cross-View Articulated Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Engelbracht_Hoi_-_A_Multimodal_Dataset_for_Force-Grounded_Cross-View_Articulated_Manipulation_CVPR_2026_paper.html) · [Project](https://hoi-dataset.ethz.ch) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Hoi! Dataset Collection and Annotation Pipeline |
| Dataset | Hoi! Articulation Estimation, Hoi! Tactile Force Prediction, Hoi! Visual Force Estimation |

> [!tip] 效果简介
> - Hoi! Articulation Estimation (type recall) 上，Type Recall (%) 71.9 (GPT-5 egocentric)。
> - Hoi! Tactile Force Prediction 上，Combined RMSE (N) 3.86 (Sparsh w/DINO)。
> - Hoi! Visual Force Estimation (projected) 上，RMSE (N) kitchen_7: 3.531, office_1: 2.325 (ForceSight) vs 0.404 on original ForceSight dataset (substantial degradation (up to ~8.7× higher error))。

## 概要

### 问题与瓶颈

具身智能体在真实世界中操作铰接物体（抽屉、门、冰箱等）时，不仅需要理解视觉几何，还必须感知和预测物理交互力。然而，现有数据集普遍缺乏**力/触觉传感**、**多视角对齐**以及**跨执行器（人手与机器人夹爪）的对应记录**，使得视觉感知与触觉动作之间的桥梁难以建立，严重制约了人类到机器人的技能迁移研究。这一数据空白是当前物理交互理解的核心瓶颈。

### 核心贡献与方法定位

**Hoi!** 数据集（CVPR 2026）针对上述缺口，提出了一个面向力觉与跨视角关节操纵的多模态数据采集与标注管线。其核心设计体现在三个关键维度：

1. **力/触觉原生记录**：通过自研的 Hoi! 夹爪，首次在野外环境中集成了 **GelSight Digit 触觉传感器**与 **Bota SensONE 6-DoF 力/扭矩传感器**，实现了对关节操纵力的精确、同步记录。
2. **多视角时空对齐**：每个交互序列同步捕获自我中心（Project Aria）、第三视角（iPhone 13 Pro）及腕部视角的 RGB-D 视频，并通过 QR 码时间戳与高分辨率激光扫描（Leica RTC360）进行时空对齐，统一到共享世界坐标系。
3. **跨执行器对应**：同一铰接物体在四种执行器模式下操作——人手、人手+腕部相机、UMI 夹爪、Hoi! 夹爪——建立了人类演示与机器人执行之间的直接对应。

### 知识库定位

在现有数据生态中，**Hoi!** 填补了此前数据集在力触觉、多视角与跨执行器对齐三个维度上的系统性空白（见表1）。相较于仅提供视觉或稀疏力信息的 **ArtiPoint**（Werby et al., 2025）、**ArtGS**（Liu et al., 2025）等铰接估计基准，以及 **ForceSight**（Collins et al., 2023）等视觉力预测方法的原始训练域，Hoi! 提供了更丰富、更具挑战性的测试平台，为力来自视觉、关节参数估计、跨视角迁移等下游研究奠定了基准。

### 主要结果速览

数据集包含 **3048 条序列**、**381 个铰接物体**，覆盖 **38 个真实室内环境**。基准实验揭示了当前方法的显著挑战：

- **视觉力预测**：ForceSight 在 Hoi! 上的 RMSE 大幅升高（如 kitchen_7 达 3.531 N，而原数据集仅 0.404 N），误差增大约 **8.7 倍**，突显了域适应与力-视觉对齐的严峻挑战。
- **触觉力预测**：Sparsh（Higuera et al., CoRL 2024）在组合测试集上 RMSE 为 3.86 N，表明从触觉图像到精确力值的映射仍有较大提升空间。
- **铰接估计**：零样本语言模型 GPT-5 在自我中心图像上的类型召回率为 71.9%，为铰接类型识别提供了初步基准。

这些结果表明，**Hoi!** 所引入的力觉、多视角与跨执行器复杂性，对当前感知模型构成了实质性的泛化考验，同时也为构建视觉-力觉联合表征和跨实体技能迁移开辟了新的研究路径。



### 关节操纵中力觉与跨视角理解的缺失

日常室内环境中充斥着可动关节物体——抽屉、门、冰箱、洗碗机——人类能够毫不费力地操控它们，依赖的不仅是视觉，还有丰富的力觉与触觉反馈。然而，当前用于理解此类交互的数据集存在三个系统性缺口，严重阻碍了对物理交互的深入理解以及人类到机器人技能的迁移研究。

**第一，力/触觉信号的普遍缺失。** 如 Table 1 所示，现有主流的人-物交互数据集（如 EPIC-KITCHENS、Ego4D、HOI4D 等）几乎不记录任何力或触觉数据。少数包含力觉的数据集要么局限于实验室环境，要么仅提供稀疏的抓取力，缺乏对关节操纵过程中连续力曲线的精确记录。这使得研究者无法系统性地回答“视觉外观与物理力模式之间存在何种关联”这一核心问题。

**第二，多视角对齐的匮乏。** 大多数数据集仅提供单一视角（通常是自我中心或第三视角），且不同视角之间缺乏时空对齐。即使少数数据集同时包含多视角，它们也未能将自我中心、第三视角和腕部视角的观测统一到共享的世界坐标系中，限制了跨视角表征学习的研究。

**第三，跨执行器对齐记录的空白。** 现有数据集要么仅记录人类操作，要么仅记录机器人执行，几乎没有在同一任务上对齐人类和机器人的多模态数据。这导致研究者无法直接比较不同执行器在完成相同操作时的力与运动模式差异，从而难以建立跨实体技能迁移的桥梁。

### Hoi! 的动机与设计目标

针对上述缺口，Hoi! 数据集（Figure 1）提出了一个统一的采集与标注框架，其核心动机是**建立视觉感知与触觉动作之间的桥梁**，从而促进操作技能的跨实体迁移。具体而言，Hoi! 通过以下设计实现这一目标：

- **同步多模态力触觉信号**：通过定制的 Hoi! 夹爪（Figure 3），首次在野外环境中集成了 GelSight Digit 触觉传感器和 6-DoF 力/扭矩传感器，实现了对关节操纵力的精确记录。
- **多视角时空对齐**：同步采集自我中心（Project Aria）、第三视角（iPhone 13 Pro）及腕部视角的视频流，并通过时间对齐（QR 码编码 Unix 时间戳）和空间对齐（利用高分辨率 3D 扫描进行视觉定位）将各传感器轨迹统一到世界坐标系。
- **跨执行器记录**：同一任务在四种执行器（人手、手+腕部相机、UMI 夹爪、Hoi! 夹爪）上重复执行，使得研究者可以直接评估力模式与视觉外观在不同执行器间的泛化能力。

### 现有基线在 Hoi! 上的暴露

Hoi! 的挑战性在现有模型的性能退化中得到了印证。以视觉力预测模型 **ForceSight**（Collins et al., 2023）为例，该模型在其原始数据集上取得了 0.404 N 的 RMSE，但在 Hoi! 的 kitchen_7 场景中误差飙升至 3.531 N，退化幅度高达约 8.7 倍（Table 6）。这一显著的性能下降揭示了域适应和力-视觉对齐的深层挑战，也印证了 Hoi! 作为新基准的独特价值。



## 核心方法与创新机理

Hoi! 数据集的根本创新在于**首次将同步的多模态力触觉信号、多视角对齐与跨执行器记录统一纳入一个面向关节物体操纵的数据集**，从而填补了现有基准中长期存在的三个结构性空白（表1）。其核心设计围绕一个因果调控变量展开：通过在同一任务上联合捕获视觉外观与物理力模式，并使其在人类与机器人执行器之间对齐，研究者得以直接探究视觉感知与触觉动作之间的关联，进而推动操作技能的跨实体迁移。

### 关键维度创新

**1. 力/触觉传感的野外集成**  
此前数据集普遍缺失力/扭矩与触觉信号（表1）。Hoi! 通过自研的 Hoi! 夹爪（图3），将 **GelSight Digit 触觉传感器** 与 **Bota SensONE 6-DoF 力/扭矩传感器** 集成于手持式平行夹爪中，首次在野外家具环境中实现了对关节操纵力的精确记录。力信号被分解为法向与切向分量，并统一到与 Digit 传感器对齐的交互坐标系中，外部力由力/扭矩传感器经旋转变换获得，内部夹持力则通过扭矩-电流关系、雅可比矩阵及负载相关标定因子估算（第4.2节）。这一设计使力触觉信号从实验室走向真实场景，成为可量化的研究变量。

**2. 多视角时空对齐**  
现有数据集多为单视角或未严格对齐（表1）。Hoi! 提供了三种同步视角：**自我中心视角**（Project Aria 眼镜，含 RGB、SLAM、眼动与手部姿态）、**两个静态第三视角**（iPhone 13 Pro），以及腕部视角。时间对齐通过以 25 Hz 频率拍摄编码 Unix 时间戳的 QR 码实现，空间对齐则借助高分辨率 Leica RTC360 激光扫描点云进行视觉定位，将各传感器轨迹通过单一刚性变换 $\mathbf{T}_{\mathrm{world}}^{\mathrm{query}}$ 统一到世界坐标系（第3节）。这一对齐机制是多模态融合与跨视角迁移研究的必要前提。

**3. 跨执行器对应记录**  
先前数据集通常将人类与机器人演示分离，缺乏直接对应（表1）。Hoi! 要求每个关节物体在 **四种执行器** 上完成相同操作：（i）人手、（ii）人手+腕部相机、（iii）手持 UMI 夹爪、（iv）Hoi! 夹爪。这种设计使得同一任务在视觉、力觉和触觉模态上的跨实体差异可被直接测量，为研究人类技能向机器人策略的迁移提供了结构化对比基准。

**4. 场景级稠密真值**  
除操作层面的标注外，Hoi! 在每个环境操作前后均使用 Leica RTC360 激光扫描仪获取高分辨率 3D 点云，作为全局几何真值。这为空间对齐、轨迹评估和关节参数估计提供了可靠的地面真值参考。

### 创新性验证

上述设计选择的有效性在实验中得到了间接但有力的验证。当现有视觉力预测模型 **ForceSight**（Collins et al., 2023）直接在 Hoi! 上评估时，其 RMSE 从原数据集的 0.404 N 急剧恶化至 kitchen_7 场景的 3.531 N（约 8.7 倍）和 office_1 的 2.325 N（表6）。这一显著退化并非模型本身的问题，而是揭示了 Hoi! 所引入的**域差异**——野外环境、多视角条件和跨执行器力模式——正是此前数据集所系统性回避的挑战。换言之，Hoi! 的“难度增量”恰恰构成了其核心研究价值：它为力-视觉对齐、域适应和跨执行器泛化等开放问题提供了迄今最严苛的测试平台。



Hoi! 数据集的构建围绕一个核心目标展开：在野外室内环境中，同步捕获人类对关节物体的操作过程，并记录多视角视觉、末端执行器力/扭矩和触觉信号，最终实现跨执行器（人手、手持夹爪）的对齐。为此，作者设计了一套完整的采集与标注流水线，其整体架构可分为四个关键模块：**多执行器数据采集**、**时间对齐**、**空间对齐**以及**标注与真值生成**。

### 多执行器数据采集

该模块是整个流水线的数据源头。为覆盖从人类自然操作到机器人夹爪操作的形态差异，数据集为同一关节物体设计了四种操作模式（embodiments）：
1.  **人手**（human hand）
2.  **人手 + 腕部相机**（human hand with wrist-mounted camera）
3.  **手持 UMI 夹爪**（handheld UMI gripper）
4.  **定制 Hoi! 夹爪**（custom Hoi! gripper）

其中，Hoi! 夹爪是专门为力触觉记录而设计的硬件核心。它集成了两个对置的 **GelSight Digit 触觉传感器**（提供高分辨率触觉图像）和一个 **Bota SensONE 六维力/扭矩传感器**（测量腕部交互力），首次实现了在野外环境中对关节操纵力的精确记录（Figure 3）。视觉方面，所有模式均通过自我中心相机（Project Aria，提供 RGB、SLAM、眼动和手部姿态）和两个静态第三视角相机（iPhone 13 Pro）进行多视角同步录制（Figure 6, Figure 7）。此外，每个场景在操作前后均使用 **Leica RTC360 激光扫描仪**捕获高分辨率 3D 点云，作为场景级几何真值。

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/004_Figure_3.jpg]]
*Figure 3: Hoi! Gripper. The 2-finger parallel gripper is operated through the load cell, where the measured load is translated into gripping force. Interaction force and tactile contact pressure are measured through the Digit and Force-Torque sensors respectively. Aria Glasses and a stereo camera provide pose estimation and wrist-view observations. We will release the design as open source*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/008_Figure_6.jpg]]
*Figure 6: Overview of the dataset collection setup. The dataset consists of 3048 multimodal sequences capturing human interactions with 381 articulated objects across 38 locations using multiple viewpoints (egocentric and third-person cameras) and manipulation conditions (hand, gripper-based). Ground truth data includes trajectories, contacts, haptic feedback, force measurements, and high-resolution 3D point clouds of each environment*

### 时间对齐

多模态数据流（RGB-D 视频、力/扭矩、触觉图像）来自不同传感器，其时间戳体系各异。为实现精确同步，采集系统在录制过程中以 25 Hz 的频率向每个相机画面中投射编码了当前 Unix 时间戳的 QR 码。通过检测和解析这些 QR 码，所有数据流被统一对齐到同一时间轴上，从而保证了后续力-视觉关联分析的时序一致性。

### 空间对齐

不同传感器（自我中心相机、第三视角相机、夹爪传感器）的观测处于各自的局部坐标系中。空间对齐模块的目标是建立一个共享的世界坐标系，将所有传感器轨迹统一其中。其核心思路是利用操作前后的高分辨率 3D 激光扫描点云作为静态参考地图：通过视觉定位技术，为每个传感器轨迹估计一个单一的刚性变换 $\mathbf{T}_{\mathrm{world}}^{\mathrm{query}}$，将其从局部传感器坐标系变换到世界坐标系。这一步骤使得跨视角的力、触觉和视觉信息在空间上可关联。

### 标注与真值生成

在原始多模态数据完成时空对齐后，标注模块负责生成下游任务所需的监督信号。主要标注内容包括：
-   **关节参数**：使用扩展的标注工具为每个物体部件标注关节类型（旋转或平移）及 3D 关节轴。
-   **3D 语义掩码**：为操作部件添加 3D 语义掩码和语言描述。
-   **力分解**：将六维力/扭矩传感器测得的外部力分解为法向和切向分量，并统一表达在与 Digit 触觉传感器对齐的交互坐标系中。夹爪的内部抓取力则通过力矩-电流关系、雅可比矩阵和负载相关标定因子进行估计。

### 数据流总结

整体流水线以“场景 + 操作者 + 执行器”为输入，经过多执行器同步采集，产出 RGB-D 视频流、力/扭矩序列、触觉图像序列以及场景激光扫描点云。这些原始数据随后依次通过时间对齐（基于 QR 码）和空间对齐（基于 3D 扫描定位）模块，形成时空一致的多模态数据体。最后，标注模块在此基础上添加关节参数、语义掩码和分解后的力分量，最终构成可供**关节参数估计**、**触觉力预测**和**视觉力估计**等基准任务直接使用的完整数据集。



Hoi!数据集的核心技术贡献在于其多模态采集管线与时空对齐机制，而非提出新的学习算法。本节聚焦于构成该管线关键能力的三个模块：**多执行器同步采集**、**时间对齐**与**空间对齐**，以及**力分解与真值生成**。

### 多执行器同步采集

数据集的根本创新在于同一关节操作任务在四种执行器形态下被重复记录：人手、人手+腕部相机、UMI夹爪，以及定制的Hoi!夹爪。Hoi!夹爪（Figure 3）是这一管线的核心硬件——它将两个GelSight Digit触觉传感器与一个Bota SensONE六自由度力/扭矩传感器集成于一个手持式平行夹爪中，首次在野外环境中实现了对关节操纵力的精确记录。每种执行器形态均通过自我中心相机（Project Aria）和两个静态第三视角相机（iPhone 13 Pro）同步采集RGB-D视频流，形成多视角对齐的观测数据。

### 时间对齐

多传感器数据流的精确同步是力觉-视觉对齐的前提。采集过程中，系统以25 Hz的频率在每个相机画面中显示一个编码了Unix时间戳的QR码。通过检测QR码中的时间信息，所有RGB-D视频流、力/扭矩传感器读数、触觉图像以及SLAM位姿估计被统一到同一时间轴上，实现了跨模态数据的帧级对齐。

### 空间对齐

空间对齐的目标是将各传感器在各自局部坐标系下的轨迹统一到共享的世界坐标系中。具体做法是利用操作前后采集的高分辨率Leica RTC360激光扫描点云作为场景级真值，通过视觉定位技术为每个传感器轨迹估计一个单一的刚性变换，将其对齐到世界坐标系：

$$\mathbf{T}_{\mathrm{world}}^{\mathrm{query}}$$

其中，$\mathbf{T}_{\mathrm{world}}^{\mathrm{query}}$ 表示将传感器坐标系（query）中的点映射到世界坐标系（world）的齐次变换矩阵。这一变换使得自我中心视角、第三视角以及腕部视角的所有观测能够在统一的空间参考系中进行关联，为后续的关节参数估计和力预测任务提供了空间一致的真值基础。Table 3通过与Qualisys运动捕捉系统的对比验证了Aria设备导出轨迹的精度，头部和腕部的位置RMSE均低至0.005 m。

### 力分解与真值生成

为生成可用于监督学习的力真值，系统将六自由度力/扭矩传感器测量的外力分解到与Digit触觉传感器对齐的公共交互坐标系中。外力被分解为法向和切向分量，而夹爪内部的夹持力则通过力矩-电流关系、雅可比矩阵以及负载依赖的校准因子进行估计。这一分解使得触觉力预测任务（Table 5）和视觉力估计任务（Table 6）能够分别在法向、切向和合力的维度上进行评估，为力觉感知研究提供了精细化的真值信号。

### 补充图表

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/009_Figure_7.jpg]]
*Figure 7: Viewpoint recordings. Recorded viewpoints for articulated part interactions. Each row corresponds to a different setup, showing synchronized exocentric (left), egocentric (center), and wrist-mounted (right) perspectives for both human and robot executions*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/006_Figure_4.jpg]]
*Figure 4: Example of the measured interaction forces for several articulated elements. Each curve corresponds to a different component (highlighted in matching colors below), illustrating how force magnitudes vary across types of articulated parts*



## 实验与关键发现

### 核心实验设计

为验证Hoi!数据集的多模态特性及其对现有方法的挑战，作者围绕三个互补任务构建了基准测试：**关节参数估计**、**触觉力预测**和**视觉力估计**。这三个任务分别考察模型对物体运动学结构的理解能力、从触觉信号推断交互力的能力，以及从视觉外观预测所需操作力的跨模态推理能力。实验选取了多个代表性基线方法，包括零样本大语言模型**GPT-5**、基于RGB-D视频的**ArtiPoint**（Werby et al., 2025）和**ArtGS**（Liu et al., 2025）、触觉力预测模型**Sparsh**（Higuera et al., CoRL 2024），以及视觉力预测模型**ForceSight**（Collins et al., 2023），在Hoi!数据集上直接评估其性能。

### 关节参数估计

关节参数估计任务要求模型从单张交互前图像或自我中心视频出发，预测关节类型（转动副或移动副）并在三维空间中估计关节轴参数。评估指标包括类型召回率（Type Recall）、轴角度误差（$\theta_{\text{err}}$）和转动副的距离误差（$d_{\text{L2}}$）。

**Table 4** 展示了各方法在Hoi!数据集上的表现。零样本大语言模型**GPT-5**在自我中心视角下取得了71.9%的类型召回率，显著优于基于视频的方法，表明语言先验对常见关节物体的类型判断具有一定泛化能力。然而，在需要精确三维几何推理的轴估计任务上，GPT-5的表现受限。**ArtiPoint**在Hoi!数据集上的性能明显下降，其移动副类型召回率仅为26.90%，远低于其在原始数据集上的表现。分析指出，这一退化主要源于Hoi!数据集中的单目深度估计尺度不确定性——ArtiPoint依赖精确的深度信息进行关节参数解算，而野外环境下的深度噪声破坏了这一假设。**ArtGS**通过三维高斯泼溅（3D Gaussian Splatting）从视频中重建场景几何，在一定程度上缓解了深度噪声问题，但其轴估计误差仍然较高，说明野外环境下的关节参数估计仍是一个开放挑战。

值得注意的是，实验揭示了现有方法的一个关键瓶颈：**视觉几何推理与物理交互先验的脱节**。基于视觉的方法在缺乏力觉信号的情况下，难以区分外观相似但操作方式不同的关节机构（如推拉门与平开门），而纯语言模型虽然具备常识推理能力，却无法处理精细的空间定位任务。

### 触觉力预测

触觉力预测任务旨在从GelSight Digit触觉传感器的图像直接回归交互力。任务将力分解为切向分量和法向分量，评估指标为均方根误差（RMSE，单位牛顿）。

**Table 5** 汇总了**Sparsh**模型在两种视觉编码器（DINO和DINOv2）下的表现。Sparsh w/DINO取得了切向RMSE 3.07 N、法向RMSE 3.45 N、综合RMSE 3.86 N的最优结果。Sparsh w/DINOv2表现略逊，综合RMSE为4.11 N。这一结果表明，触觉图像中确实编码了可被提取的力信息，但预测精度仍受限于触觉传感器的空间分辨率、接触几何的复杂性以及不同物体材质带来的非线性响应。

该实验的核心价值在于**首次在野外环境中建立了触觉图像到力信号的基准映射**。与受控实验室环境不同，Hoi!数据集中的触觉数据包含真实世界的不确定性——不规则的接触面、变化的抓取姿态以及多样化的物体纹理——使得该基准更贴近实际机器人操作场景。

### 视觉力估计

视觉力估计任务要求模型从RGB-D观测和操作目标（如“打开抽屉”）出发，预测执行动作所需的三维交互力。这是三个任务中最具挑战性的跨模态推理任务，因为它要求模型建立视觉外观与物理力需求之间的隐式映射。

**Table 6** 报告了**ForceSight**模型在Hoi!数据集不同场景下的力预测RMSE。结果揭示了显著的域迁移问题：ForceSight在其原始数据集上取得了0.404 N的RMSE，但在Hoi!的kitchen_7场景中，投影方向上的RMSE飙升至3.531 N（约为原始误差的8.7倍），在office_1场景中也达到2.325 N。即使在相对简单的场景中，误差也显著高于原始数据集水平。

这一剧烈退化揭示了当前视觉力预测方法的根本局限：**模型过度依赖训练数据的场景外观统计，而非学习可迁移的物理力模式**。当面对新的物体几何、材质和操作方式时，纯视觉模型无法准确推断所需的力大小。Hoi!数据集通过提供同步的视觉和力信号真值，为研究**力-视觉对齐**和**跨场景力泛化**提供了关键的训练和评估资源。

### 轨迹精度验证

为保证多模态数据的空间对齐质量，作者使用Qualisys运动捕捉系统对Project Aria眼镜的轨迹估计精度进行了定量评估。**Table 3** 显示，头部轨迹的位置RMSE为0.005 m，腕部为0.005 m，夹爪为0.006 m。这一精度水平足以支撑后续的力分解和跨视角对齐任务，验证了基于视觉SLAM的野外轨迹估计方案在数据采集场景中的可靠性。

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/010_Table_3.jpg]]
*Table 3: Trajectory Evaluation. Trajectory error of Ariaderived quantities, evaluated against Qualisys motion-capture trajectories*

### 实验总结与关键发现

综合三项基准实验，Hoi!数据集揭示了以下核心发现：

1. **力触觉信号的缺失是当前操作感知研究的系统性盲区**。视觉力预测模型在跨域场景中的大幅退化表明，纯视觉方法无法可靠地推断物理交互力，亟需融合力触觉信号的多模态学习方法。

2. **跨执行器对齐数据为技能迁移研究提供了独特资源**。Hoi!数据集中同一任务在四种执行器上的对齐记录，使研究者能够直接比较人类与机器人在执行相同操作时的视觉和力模式差异，为从人类演示中学习机器人策略提供了新的研究范式。

3. **野外环境下的关节参数估计仍面临严峻挑战**。现有方法在受控环境中表现良好，但在Hoi!的多样化场景中暴露出对深度噪声、视角变化和物体外观差异的敏感性，表明需要更加鲁棒的三维理解方法。

需要指出的是，当前基准实验主要评估了各模型的零样本或直接迁移性能，未进行针对性的域适应训练。Hoi!数据集提供的丰富标注（关节参数、力分解、三维掩码等）为后续的微调和联合训练提供了充分条件，预期经过适配的模型将取得显著更好的性能。

### 补充图表

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/002_Table_1.jpg]]
*Table 1: Commonly used datasets for human interactions and articulated environments. Views: Numbers indicate available camera viewpoints; columns show Egocentric (Ego), Exocentric (Exo), and Wrist-mounted (Wrist). Embodiments: Columns show Human (H), Robot (R), and Tool/Gripper (T) Modalities: RGB, Depth, Force/Torque, Haptic/Tactile, Hand Tracking, Audio, Joint States, Eyetracking, 3D Model / Digital Twin, Language*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/005_Table_2.jpg]]
*Table 2: Recording setup. Each manipulation condition comprises several recording modules producing multiple time-aligned data streams*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/011_Table_4.jpg]]
*Table 4: Articulation Estimation. Given a single image before interaction (for GPT) or the egocentric video (for ArtGS and ArtiPoint), methods estimate the type of articulation as well as the exact articulation axis in 3D. We report type recall*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/012_Table_5.jpg]]
*Table 5: Interaction Force Prediction. Based on measurements from the DIGIT tactile pressure sensor. RMSE (95% CI) in Newtons, averaged over all validation environments*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/013_Table_6.jpg]]
*Table 6: Visual Force Estimation. Given an RGB-D observation and a manipulation goal (e.g., “open the drawer”), the model predicts the 3D interaction force required to perform the action. We report the force RMSE (in N, lower is better) of ForceSight [5] across different locations in our dataset. Projected denotes evaluation on force components aligned with the gripper’s motion direction*

![[assets/figures/papers/paper_list_l821_https_openaccess_thecvf_com_content_CVPR2026_html_Engelbracht_Hoi_A_Mult/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Hoi! Dataset: A multimodal dataset for force-grounded, cross-view articulated manipulation in wild indoor environments. The dataset captures human interactions with common articulated objects (drawers, doors, fridges, dishwashers) with synchronized RGB, depth, force, tactile sensing, and multi-view videos from egocentric and exocentric perspectives. Each interaction is annotated with articulation parameters (e.g. axis, type), supporting research on multimodal perception, manipulation learning, and embodied reasoning*



## 定位与知识库关联

### 1. 现有数据集的瓶颈与Hoi!的填补

Hoi!的核心贡献在于系统性地填补了当前具身交互数据生态中“力触觉缺失”与“跨执行器对齐缺失”两大瓶颈。**Table 1** 的横向对比揭示了关键空白：现有大规模数据集（如Ego4D、HOI4D、ARCTIC）虽提供丰富的视觉与手部姿态标注，但普遍缺乏6-DoF力/扭矩和触觉信号；少数包含力觉的数据集（如ManiWAV、RH20T）则未覆盖多视角同步记录，或仅局限于单一执行器形态。Hoi!首次在同一任务上以四种执行器（人手、手+腕部相机、UMI夹爪、Hoi!夹爪）进行记录，并同步提供自我中心、第三视角和腕部视角的RGB-D流，使得视觉外观与物理力模式之间的关联研究成为可能。

### 2. 硬件与感知范式定位

Hoi!夹爪（**Figure 3**）的硬件设计将两种互补的力感知模态耦合在同一末端执行器上：**GelSight Digit触觉传感器**提供高分辨率接触形变图像，**Bota SensONE 6-DoF力/扭矩传感器**测量腕部交互力。这一组合区别于纯视觉力估计（如ForceSight，Collins et al., 2023）和纯触觉力估计（如Sparsh，Higuera et al., CoRL 2024）的单一模态范式，为多模态融合提供了真值基准。在方法谱系上，Hoi!夹爪的设计理念继承了GelSight系列触觉传感器在机器人操作中的应用传统，但首次将其与力/扭矩传感器在野外环境（家具店、公寓）中集成，而非局限于实验室桌面场景。

### 3. 基线方法的适用边界与域迁移挑战

论文在三个基准任务上评估了现有方法，其结果揭示了显著的域迁移退化：

- **关节参数估计**：**ArtiPoint**（Werby et al., 2025）在Hoi!自我中心RGB-D上表现显著下降（棱柱关节召回率仅26.90%，Table 4），主要原因是其依赖的度量深度在野外场景中退化为尺度模糊的单目深度估计。**ArtGS**（Liu et al., 2025）通过3D Gaussian Splatting从视频重建场景，对深度质量的依赖较低，但在Hoi!复杂背景和动态交互下的鲁棒性仍需验证。**GPT-5**的零样本关节类型预测（自我中心视角召回率71.9%）虽提供上界参考，但其依赖的语言先验无法提供精确的3D轴参数。

- **触觉力预测**：**Sparsh**（Higuera et al., CoRL 2024）在Hoi!的GelSight Digit图像上进行力回归，使用DINO特征提取器时综合RMSE为3.86 N（Table 5）。该误差水平表明，从触觉图像到交互力的映射在野外多物体、多操作模式下仍具挑战，尤其是法向力与切向力的解耦预测。

- **视觉力估计**：**ForceSight**（Collins et al., 2023）的跨数据集泛化退化最为显著——在kitchen_7场景中RMSE从原数据集的0.404 N飙升至3.531 N（约8.7倍，Table 6）。这一结果表明，ForceSight所学的视觉-力映射高度依赖其训练域的特定视觉外观和操作模式，Hoi!中多样的家具纹理、光照条件和关节机构构成了严峻的分布外测试。

### 4. 知识库中的独特定位与下游任务接口

Hoi!在知识库中的独特价值体现在三个层面：

1. **力-视觉对齐的基准平台**：数据集提供了同步的视觉观测与力触觉真值，可直接支持“从视觉预测力”和“从触觉预测力”两类任务的训练与评估，并为多模态融合方法（如视觉-触觉联合编码器）提供对齐数据。

2. **跨执行器迁移的测试床**：同一任务在四种执行器上的记录使得研究者可以评估策略或表征在不同形态间的可迁移性。例如，从人手演示中学习视觉力先验，并将其迁移到Hoi!夹爪的执行中。

3. **关节物体理解的增强数据源**：高分辨率Leica RTC360激光扫描点云提供了操作前后的场景级真值，结合标注的关节轴、类型和3D语义掩码，为关节物体参数估计和动态场景重建提供了比现有数据集更丰富的监督信号。

### 5. 局限与开放问题

**适用边界**：
- 数据集聚焦于末端执行器（夹爪）力，缺失全手或全身力分布信息。对于需要全身协调的操作任务（如推重型家具），当前数据无法直接支持力模式分析。
- 场景扫描为静态前后对比，未记录操作过程中的动态变形。对于柔性关节物体或操作中发生显著位移的场景，真值精度受限。
- 采集环境以家具店和有限居住空间为主，虽覆盖常见关节类别，但极端工况（如生锈铰链、重型工业门）和特殊机构（如多轴联动）的泛化性未经验证。

**开放问题**：
- 如何将Hoi!的力觉信号作为强化学习的奖励或约束，以提升操作策略对接触力敏感的鲁棒性？
- 能否利用Hoi!的跨执行器对齐数据训练视觉-力觉联合表征，实现从人类操作视频到机器人策略的零样本迁移？
- 如何将当前以物体为中心的感知任务（关节估计、力预测）扩展至端到端策略学习，实现感知与动作的联合优化？
- 数据集未提供预训练模型，直接用于下游策略学习需要额外的特征工程和架构设计，这一工程化路径仍有待探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/Hoi_A_Multimodal_Dataset_for_Force_Grounded_Cross_View_Articulated_Manipulation.pdf]]

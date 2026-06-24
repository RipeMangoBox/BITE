---
title: "EgoXtreme: A Dataset for Robust Object Pose Estimation in Egocentric Views under Extreme Conditions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoXtreme_A_Dataset_for_Robust_Object_Pose_Estimation_in_Egocentric_Views_under_Extreme_Conditions.pdf
project_link: "https://taegyoun88.github.io/EgoXtreme/"
code_link: null
aliases:
- ED
- EgoXtreme
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 极端视觉条件（动态光照、运动模糊、烟雾）造成的图像特征丢失和分布偏移是导致姿态估计失败的直接原因；通过混合时间策略利用帧间信息可以部分缓解运动模糊，但单纯图像复原（去模糊、去雾、低光增强）无法恢复用于精确匹配的判别性特征，甚至引入噪声。
primary_logic: EgoXtreme数据集首次系统性地揭示了在自我中心极端环境下，现有零样本6D姿态估计模型的脆弱性；图像复原预处理不仅无法提升性能，反而可能引入噪声并进一步降低精度；而基于置信度评估的动态混合时间跟踪策略是提升快速运动场景下鲁棒性的有效方向。
claims:
- 在极端光照与无烟条件下，PicoPose在Emergency场景的ADD(S)@0.3d从标准光下的67.83%降至极端光下的36.23%，性能损失超过31个百分点。
- 图像复原预处理（去模糊、去雾、低光增强）不仅未能提升姿态估计性能，反而在多个场景下导致召回率下降约5-8%p，例如组合预处理在Maintenance场景将0.3d召回率降低约5%p。
- 混合时间跟踪策略（Hybrid）在Sports场景中显著优于Direct方法，例如Tennis的ADD(S)@0.3d从22.77%（Direct）回升至50.55%（Hybrid），接近Per-frame的50.91%。
- GDRNPP实例级方法在Tennis标准光下达到96.50%的0.3d精度，验证了GT标注的可靠性；而模型无关方法OnePose++在相同条件下仅20.96%，凸显了极端运动的挑战性。
---

# EgoXtreme: A Dataset for Robust Object Pose Estimation in Egocentric Views under Extreme Conditions

> [!tip] 核心洞察
> EgoXtreme数据集首次系统性地揭示了在自我中心极端环境下，现有零样本6D姿态估计模型的脆弱性；图像复原预处理不仅无法提升性能，反而可能引入噪声并进一步降低精度；而基于置信度评估的动态混合时间跟踪策略是提升快速运动场景下鲁棒性的有效方向。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoXtreme：面向极端条件下自我中心视角的鲁棒物体姿态估计数据集 |
| 英文题名 | EgoXtreme: A Dataset for Robust Object Pose Estimation in Egocentric Views under Extreme Conditions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25135) · [Project](https://taegyoun88.github.io/EgoXtreme/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | EgoXtreme Dataset |
| Dataset | EgoXtreme Sports, EgoXtreme Maintenance, EgoXtreme Emergency, EgoXtreme Sports tracking |

> [!tip] 效果简介
> - EgoXtreme Sports (Standard vs Extreme, no smoke) 上，ADD(S) @0.1d (FoundPose) 0.53 (Standard) vs 0.18 (Extreme) (-66.0%)。
> - EgoXtreme Maintenance (Standard vs Extreme, no smoke) 上，ADD(S) @0.1d (GigaPose) 33.64 (Standard) vs 13.78 (Extreme) (-58.9%)。
> - EgoXtreme Emergency (Standard vs Extreme, no smoke) 上，ADD(S) @0.1d (FoundPose) 6.31 (Standard) vs 0.10 (Extreme) (-98.4%)。

## 概述

**问题瓶颈**：现有零样本6D物体姿态估计模型（如FoundPose、GigaPose、PicoPose）在向自我中心视角的真实极端场景迁移时，泛化能力急剧下降——低光照条件下尤为严重。其根本原因在于，这些模型在训练和评估阶段均缺乏覆盖极端视觉条件（剧烈光照变化、严重运动模糊、烟雾遮挡）的基准数据集，导致面对特征丢失和分布偏移时无法保持鲁棒性。

**核心发现**：EgoXtreme数据集首次系统性地揭示了这一脆弱性。实验表明，在极端光照条件下，PicoPose在Emergency场景的ADD(S)@0.3d从标准光的67.83%骤降至36.23%，性能损失超过31个百分点；FoundPose在同一场景的0.1d精度更是从6.31%跌至0.10%，降幅达98.4%。更为反直觉的是，图像复原预处理（去模糊、去雾、低光增强）不仅无法提升姿态估计精度，反而因引入噪声导致召回率进一步下降约5-8个百分点。相比之下，基于置信度评估的动态混合时间跟踪策略在快速运动场景中展现出显著优势——GigaPose在Tennis场景的ADD(S)@0.3d从直接时间传播的22.77%回升至50.55%，接近逐帧方法的50.91%，有效抑制了误差传播。

**方法定位**：EgoXtreme并非提出新的姿态估计算法，而是构建了一个面向极端条件下鲁棒性评估的系统性基准。数据集通过Aria眼镜采集15名参与者的775.5分钟自我中心RGB视频，覆盖运动（Sports）、工业维护（Maintenance）和紧急救援（Emergency）三类场景，并利用OptiTrack动捕系统以120fps获取高精度6D真值。其贡献在于填补了现有基准在极端视觉条件下的空白，为后续鲁棒姿态估计研究提供了标准化评测平台。

**主要结果**：（1）所有零样本通用模型在极端光照下均出现严重退化，低光照是最致命的单一因素；（2）现有图像复原方法无法恢复用于精确匹配的判别性特征，反而损害下游性能；（3）混合时间策略是提升快速运动场景鲁棒性的有效方向，但单纯直接时间传播会放大误差。

## 背景与动机

6D物体姿态估计是增强现实、机器人操作和手物交互理解中的核心任务。近年来，基于RGB的零样本通用姿态估计模型取得了显著进展，代表性方法包括**FoundPose**（粗对齐结合MegaPose精修）、**GigaPose**（同架构路线）以及端到端粗到精的**PicoPose**。这些模型在标准基准上展现出令人瞩目的泛化能力，然而其评估主要局限于光照良好、静态或缓慢运动的场景。

真实世界中的自我中心应用——如工业维护、运动训练和紧急救援——往往伴随着极端视觉条件：剧烈光照变化、严重运动模糊、烟雾遮挡等。当通用姿态估计模型迁移到此类环境时，性能急剧退化。EgoXtreme数据集的系统评估揭示了一个核心瓶颈：**现有零样本6D姿态估计模型在极端光照、运动模糊和烟雾等自我中心真实场景下泛化失效，低光照条件下的性能损失尤为严重**。

具体而言，PicoPose在Emergency场景中，从标准光照下的67.83% ADD(S)@0.3d骤降至极端光照下的36.23%，性能损失超过31个百分点；FoundPose在Sports场景的ADD(S)@0.1d从0.53降至0.18，降幅达66%。这些数据表明，极端视觉条件造成的图像特征丢失和分布偏移是姿态估计失败的直接因果机制。

一个直观的应对思路是引入图像复原预处理——去模糊、低光增强、去雾等——试图恢复退化图像中的判别信息。然而，EgoXtreme的实验发现了一个反直觉的关键洞察：**图像复原预处理不仅无法提升姿态估计性能，反而可能引入噪声并进一步降低精度**。例如，同时使用去模糊与低光增强在Emergency场景将PicoPose的0.1d召回率从23.39%降至4.74%；组合预处理在Maintenance场景将0.3d召回率降低约5个百分点。这一发现表明，现有恢复方法在“修复”图像外观的同时，破坏了用于精确匹配的判别性特征，单纯依赖图像复原无法解决极端条件下的姿态估计难题。

与静态图像评估不同，自我中心视频天然携带时序信息。EgoXtreme对时间跟踪策略的探索揭示了另一条有效路径：基于置信度评估的**混合时间跟踪策略（Hybrid）**在快速运动场景中显著优于直接时间传播（Direct）。在Tennis场景中，Hybrid策略将GigaPose的ADD(S)@0.3d从22.77%（Direct）回升至50.55%，接近逐帧评估的50.91%。这一结果表明，利用帧间信息可以部分缓解运动模糊的影响，但必须谨慎处理误差传播——直接传播在动态体育场景中可导致高达46个百分点的召回率下降。

上述发现共同指向一个迫切需求：**构建一个系统覆盖极端视觉条件的自我中心基准数据集，以诊断现有方法的脆弱性、验证直觉假设的真伪，并为鲁棒姿态估计研究提供方向指引**。这正是EgoXtreme数据集的核心动机。

## 核心创新

EgoXtreme 的核心贡献不在于提出新的姿态估计模型，而在于**构建了首个系统性覆盖极端视觉条件的自我中心 6D 物体姿态估计基准数据集**，并基于该基准揭示了现有零样本姿态估计方法的两大关键瓶颈与一条有效改进方向。

### 1. 极端条件基准：填补分布外评估的空白

现有 6D 姿态估计数据集（如 LINEMOD、YCB-Video、HOPE）主要在受控光照和低动态场景下采集，无法反映自我中心应用中常见的极端视觉退化。EgoXtreme 针对这一缺口，构建了覆盖三大场景（Sports、Maintenance、Emergency）、多种光照条件（normal、middle light、low light、flashlight、headlight、warning light 等）及烟雾干扰的数据集，总计 775.5 分钟自我中心 RGB 视频，来自 15 名参与者佩戴 Aria 眼镜采集。

**关键设计决策**：
- **多传感器同步真值获取**：采用 OptiTrack 动捕系统以 120fps 获取头显与物体的 6D 真值，通过 Umeyama 方法将 Aria SLAM 轨迹与动捕轨迹对齐，并使用卡尔曼滤波补偿 SLAM 漂移，最终以手动时间偏移校正解决 RGB 曝光延迟问题。
- **极端条件分类体系**：将光照、烟雾、运动速度等维度结构化，形成多维鲁棒性评估框架（Table 2），使得性能退化可以按条件维度归因。

### 2. 核心发现：图像复原预处理对姿态估计的反直觉损害

EgoXtreme 最关键的实验发现是：**针对极端条件的图像复原预处理（去模糊、低光增强、去雾）不仅未能提升下游姿态估计性能，反而普遍导致精度下降**。这一发现挑战了“先复原再估计”的直觉管线。

具体证据（Table 4）：
- 在 Maintenance 场景，PicoPose 无预处理时 ADD(S)@0.3d 为 63.32%，单独去雾后降至 57.55%（**-9.1%**），去模糊与低光增强组合预处理后进一步降低约 5%p。
- 在 Emergency 场景，去模糊与低光增强组合将 PicoPose 的 0.1d 召回率从 23.39% 降至仅 4.74%（**-79.7%**）。

**因果机制分析**：现有图像复原方法在去除视觉退化时，会引入纹理失真、边缘模糊或伪影，这些人工痕迹破坏了用于精确 6D 匹配的判别性局部特征。对于依赖细粒度几何纹理配准的零样本姿态估计器而言，复原引入的噪声比原始退化更具破坏性。

### 3. 时间跟踪策略：混合置信度机制缓解运动模糊

针对高动态场景（如 Sports 中的 Tennis、Bat 运动），EgoXtreme 系统性地比较了三种时间跟踪策略：
1. **Direct**：直接将 $t-1$ 帧的完整姿态作为当前帧初始输入。
2. **Fusion**：融合 $t-1$ 帧的旋转姿态与当前帧粗对齐的平移姿态。
3. **Hybrid**：基于置信度评估动态选择 Direct 或 Per-frame 策略。

关键消融结果（Table 5）：
- 在 Tennis 场景，GigaPose 的 ADD(S)@0.3d 从 Direct 的 22.77% 回升至 Hybrid 的 50.55%（**+122%**），接近 Per-frame 的 50.91%。
- 在 Bat 场景，Hybrid 达到 64.46%，而 Direct 仅 14.29%（**+351%**）。

**创新本质**：Hybrid 策略通过置信度门控机制，在帧间姿态一致性高时利用时间信息弥补单帧特征丢失，在快速运动导致大位移时回退到单帧估计，有效抑制了 Direct 策略因误差传播导致的灾难性退化（最高达 46%p）。

### 4. 方法谱系与知识库定位

EgoXtreme 作为基准数据集，其定位区别于以下工作：

| 维度 | 现有基准（LINEMOD/YCB-V/HOPE） | EgoXtreme |
|------|-------------------------------|-----------|
| 视角 | 第三人称固定/手持 | 自我中心头戴（Aria 眼镜） |
| 光照 | 受控/均匀 | 极端动态光照（低光、频闪、应急灯） |
| 运动 | 静态/低速 | 高速运动（最高 1.37 m/s） |
| 视觉退化 | 无 | 运动模糊、烟雾遮挡 |
| 真值获取 | 手动标注/RGB-D 重建 | 动捕+SLAM 融合 |

在方法谱系上，EgoXtreme 评估的基线模型覆盖了当前零样本姿态估计的主要范式：**FoundPose** 和 **GigaPose** 采用粗对齐加 MegaPose 精化的两阶段策略，**PicoPose** 则采用端到端粗到细一体化架构。实验表明，这些在标准基准上表现良好的模型在 EgoXtreme 极端条件下均出现显著性能崩塌，例如 FoundPose 在 Emergency 极端光照下的 ADD(S)@0.1d 从 6.31% 降至 0.10%（**-98.4%**），验证了该基准的挑战性和必要性。

### 5. 局限与待验证方向

- 数据集缺乏手部姿态标注，无法评估手物交互上下文对姿态估计的影响，这一问题在极端运动模糊下尤为突出。
- 采集环境限于室内，尚未覆盖夜间户外等更极端的光照条件。
- 混合时间策略的置信度门控阈值需要场景特定调优，其自适应泛化能力有待进一步验证。

## 整体框架

EgoXtreme 并非提出新的姿态估计算法，而是构建了一套面向极端条件下自我中心视角的**基准评估框架**。该框架的核心由三个递进层次构成：**数据采集与真值生成**、**零样本基线评估**、以及**鲁棒性诊断与改进方向验证**。

### 数据采集与真值生成管线

框架的输入基础是多传感器同步采集系统。其数据流如下：

1. **多模态同步采集**：参与者佩戴 Project Aria 眼镜以 30fps 记录自我中心 RGB 视频，同时通过 OptiTrack 光学动捕系统以 120fps 获取头显与物体的 6D 姿态真值。Aria 内置的 SLAM 系统以 1000fps 提供头显轨迹，动捕系统则提供亚毫米级精度的物体位姿。
2. **坐标系统一**：由于 Aria SLAM 轨迹与动捕轨迹处于不同坐标系，框架采用 **Umeyama 方法**进行轨迹对齐，将两者统一到全局坐标系下。
3. **漂移补偿与时间校正**：针对 SLAM 在运动过程中产生的累积漂移，应用**卡尔曼滤波**对轨迹对齐进行精化。此外，由于 RGB 相机曝光延迟会导致毫秒级的时间错位，框架通过**人工视觉校验**进行时间偏移校正，确保真值投影与图像内容精确匹配。
4. **真值输出**：经过上述处理后，每一帧 RGB 图像对应一个精确的物体 6D 姿态真值，构成后续评估的基础。

### 评估与诊断框架

在真值数据之上，框架对现有零样本 6D 姿态估计模型进行系统性评估。评估分为三个维度：

- **静态帧评估**：将 FoundPose、GigaPose、PicoPose 等模型直接应用于单帧图像，测量其在标准光照与极端光照（低光、强光、烟雾）下的 ADD(S) 召回率及空间误差（MSSD/MSPD）。
- **预处理影响分析**：在姿态估计前插入图像复原模块（去模糊、低光增强、去雾），量化这些预处理对下游任务的实际影响，验证“复原是否等于提升”的假设。
- **时间跟踪策略消融**：在视频序列上对比三种时间传播策略——**Direct**（直接传播前一帧完整姿态）、**Fusion**（融合前一帧旋转与当前帧粗平移）、**Hybrid**（基于置信度评估动态选择是否采用前一帧姿态）——以诊断运动模糊场景下的误差传播机制。

### 框架的因果诊断逻辑

该评估框架的核心贡献在于揭示了从“视觉退化”到“姿态估计失败”的因果链条：

- **直接原因**：极端光照、运动模糊、烟雾导致图像判别性特征丢失，使基于特征匹配的零样本模型无法建立可靠的 2D-3D 对应关系。
- **关键发现**：图像复原预处理不仅无法恢复这些判别性特征，反而可能引入伪影和噪声，进一步降低姿态估计精度。例如，在 Emergency 场景下，同时使用去模糊与低光增强将 PicoPose 的 0.1d 召回率从 23.39% 降至 4.74%。
- **有效干预方向**：基于置信度评估的混合时间跟踪策略（Hybrid）能够有效抑制误差传播，在快速运动场景下将召回率从 Direct 策略的个位数提升至接近逐帧评估的水平。

整个框架的输入是同步采集的 RGB 视频与动捕真值，输出是模型在极端条件下的性能诊断报告与改进方向验证结果，为后续鲁棒姿态估计研究提供了标准化的测试平台。

### 补充图表

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/006_Figure_4.jpg]]
*Figure 4: Diagram for data collection*

## 核心模块与公式推导

EgoXtreme本身是一个数据集工作，不提出新的6D姿态估计模型或数学公式。其核心贡献在于**构建了一套高精度多传感器真值采集管线**，为下游模型在极端条件下的鲁棒性评估提供可靠基准。以下梳理该管线的关键模块。

### 多传感器同步采集模块

数据采集使用**Aria眼镜**记录30fps的RGB视频，同时通过**OptiTrack动捕系统**以120fps获取头显与物体的6D真值。Aria内置的SLAM系统以1000fps运行，提供头显在局部坐标系下的轨迹。这一多源异构同步是该数据集真值质量的基础保障。

### 坐标系对齐与漂移补偿模块

Aria SLAM轨迹与OptiTrack动捕轨迹处于不同坐标系，需要进行刚性对齐。管线采用**Umeyama方法**将两条轨迹统一到全局坐标系。然而，SLAM在运动过程中存在漂移，因此进一步应用**卡尔曼滤波器**对轨迹对齐进行精化，补偿漂移误差。这两个模块的级联确保了长时间序列下真值标注的空间一致性。

### 时间偏移校正模块

由于Aria的RGB曝光延迟与SLAM时间戳之间存在毫秒级的时间错位，直接插值会导致真值投影偏差。管线通过**视觉校验**的方式，人工检查投影结果并手动调整时间偏移量，最终再进行插值。这一步虽然简单，但对于高速运动场景（如Sports场景中物体速度可达1.37 m/s，见Table 2）下的标注精度至关重要。

---

**关于公式：** 本文未提出新的数学公式。Umeyama方法的闭式解、卡尔曼滤波的预测-更新递归方程均为经典算法，原文未重新推导。若需了解具体公式形式，请参考Umeyama (1991)和标准卡尔曼滤波文献。

## 实验与分析

### 核心瓶颈与实验设计逻辑

现有零样本6D姿态估计模型（如FoundPose、GigaPose、PicoPose）在标准基准上表现优异，但它们在EgoXtreme上的表现揭示了根本性的泛化瓶颈：**极端视觉条件（动态光照、运动模糊、烟雾）造成的图像特征丢失和分布偏移是导致姿态估计失败的直接原因**。实验设计围绕三个维度展开——(1) 极端环境下的基准性能评估，(2) 图像复原预处理的效用检验，(3) 时间跟踪策略的消融——以系统性地量化这些瓶颈并探索缓解路径。

### 数据集配置与评估协议

EgoXtreme涵盖三个场景（Sports、Maintenance、Emergency），每个场景包含标准光照与极端光照两种条件，并可选地加入烟雾（仅Maintenance与Emergency）。详细配置见Table 2。评估采用ADD(S)召回率（阈值0.1d/0.2d/0.3d，其中d为物体直径）和空间精度指标MSSD/MSPD。主实验使用GT边界框解耦检测误差，以聚焦姿态估计本身的鲁棒性；端到端结果（使用CNOS检测器）见Table C1。

### 极端环境下的基准性能崩塌

Table 3展示了三个基线模型在标准光与极端光（无烟）下的性能对比，所有模型均出现大幅退化：

- **低光照是最致命的退化因素**。在Emergency场景下，PicoPose的ADD(S)@0.3d从标准光的67.83%骤降至极端光的36.23%，性能损失超过31个百分点；FoundPose在@0.1d阈值下从6.31%降至0.10%，退化幅度高达98.4%。
- **运动模糊加剧退化**。Sports场景中物体平均速度达1.37 m/s（Table 2），FoundPose在@0.1d下从标准光的0.53%降至极端光的0.18%，GigaPose在Maintenance场景@0.1d下从33.64%降至13.78%（-58.9%）。
- **烟雾引入额外退化**。GigaPose在Maintenance场景加入烟雾后，性能进一步下降约9.91个百分点（Table 3）。

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/007_Table_3.jpg]]
*Table 3: 6D object pose estimation on EgoXtreme. Performance is evaluated using ADD(S) recall at thresholds of 0.1d, 0.2d, 0.3d (↑) and spatial accuracy metrics MSSD/MSPD (↓), where d denotes the object diameter*

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/004_Table_2.jpg]]
*Table 2: EgoXtreme datasets configuration*

Figure 5的定性结果显示，极端光照下预测姿态（红色）与真值（绿色）严重偏离，尤其在低纹理物体和严重遮挡情况下，模型几乎完全失效。

### 图像复原预处理：不仅无效，反而有害

一个关键发现是：**简单应用图像复原预处理（去模糊、低光增强、去雾）无法提升姿态估计性能，反而可能引入噪声并进一步降低精度**。Table 4报告了PicoPose在不同预处理下的表现：

- 在Maintenance场景中，组合预处理（去模糊+低光增强）将@0.3d召回率降低约5个百分点（从63.32%降至约58%）。
- 在Emergency场景中，去雾处理导致@0.1d召回率从23.39%暴跌至4.74%，表明现有去雾方法引入的伪影严重破坏了用于精确匹配的判别性特征。
- 定性结果（Figure 6）显示，预处理后的图像虽然视觉上更清晰，但姿态估计结果反而恶化，验证了“视觉质量≠下游任务性能”的结论。

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/009_Figure_6.jpg]]
*Figure 6: Example 6D Pose estimation results with preprocessing. The top row shows the original, non-preprocessed images. The bottom row displays the corresponding images after applying specific preprocessing: deblurring (left), light enhancement (middle), and dehazing (right)*

### 时间跟踪策略消融：混合策略的有效性

针对快速运动场景，实验比较了三种时间策略（Table 5，基于GigaPose在Sports正常光下）：

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/011_Table_5.jpg]]
*Table 5: 6D object pose tracking for GigaPose. Applied to sports normal scenario*

- **Direct（直接传播）**：将上一帧的全姿态作为当前帧初始输入。在动态场景下，该方法导致严重误差累积——Tennis场景@0.3d召回率仅22.77%，Pingpong仅6.58%。
- **Per-frame（逐帧独立）**：不使用时间信息，Tennis场景@0.3d为50.91%，Pingpong为20.44%。
- **Hybrid（置信度混合）**：基于置信度评估动态选择是否使用上一帧信息。该方法有效抑制了误差传播——Tennis场景@0.3d回升至50.55%（接近Per-frame），Pingpong为16.53%（虽低于Per-frame但远优于Direct），Bat场景高达64.46%（vs Direct的14.29%）。

消融结论清晰：**直接时间传播在快速运动物体上可导致高达46个百分点的召回率下降，而基于置信度评估的动态混合策略是提升快速运动场景下鲁棒性的有效方向**。

### 实例级模型的验证与局限

GDRNPP（实例级方法，需针对特定物体训练）在Tennis标准光下达到96.50%的@0.3d精度（Table C2），验证了GT标注的可靠性。然而，模型无关方法OnePose++在相同条件下仅20.96%，凸显了极端运动对无先验方法的挑战性。实例级模型虽表现良好，但需针对新物体重新训练，限制了其在零样本设置下的直接应用。

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/016_Table.jpg]]
*Table: C2. Additional baseline results on the Tennis sequence*

### 检测瓶颈的额外证据

Table C1展示了使用CNOS检测器的端到端评估结果，性能远低于使用GT边界框的Table 3，说明**检测模块是另一个重要瓶颈**——在极端条件下，检测失败会进一步放大姿态估计的误差。

### 失败模式总结

1. **低光照**：特征提取失效，模型无法建立可靠的2D-3D对应关系。
2. **运动模糊**：单帧信息严重退化，直接时间传播导致误差累积。
3. **烟雾遮挡**：部分遮挡使模型误匹配，去雾预处理引入伪影进一步降低精度。
4. **检测-姿态级联失败**：检测器在极端条件下召回率下降，导致姿态估计输入缺失。

### 补充图表

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/010_Table_4.jpg]]
*Table 4: 6D object pose estimation with pre-processing for PicoPose*

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/003_Table_1.jpg]]
*Table 1: Datasets for object pose estimations*

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/008_Figure_5.jpg]]
*Figure 5: Example 6D Pose estimation results on baseline models. The red line is prediction and green is GT. (a), (b), and (c) are the industry maintenance, sports, and emergency rescue scenarios, respectively. The top row indicates standard light condition, and the bottom row indicates extreme light condition*

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/014_Table.jpg]]
*Table: C1. End-to-end 6D object pose estimation using CNOS detections*

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/017_Table.jpg]]
*Table: D2. 6D object pose tracking for GigaPose*

![[assets/figures/papers/paper_list_l2716_https_arxiv_org_abs_2603_25135/figures/021_Table.jpg]]
*Table: E1. 6D object pose estimation with pre-processing under conditions*

## 方法谱系与知识库定位

### 1. 零样本6D姿态估计的基准线

EgoXtreme数据集的核心贡献不在于提出新的姿态估计方法，而是构建了一个系统性暴露现有方法脆弱性的评估基准。论文选取了三类具有代表性的零样本（zero-shot）通用6D姿态估计器作为评估对象：

- **FoundPose**：基于RGB的零样本姿态估计器，采用粗对齐（coarse alignment）与 **MegaPose** 精化（refinement）的两阶段流水线。在EgoXtreme的标准光照条件下，FoundPose在Sports场景中仅能达到0.53%的ADD(S)@0.1d精度，表明其在高动态场景下已面临根本性困难。
- **GigaPose**：同样采用MegaPose作为精化模块的RGB零样本方法。在Maintenance标准光下达到33.64%的ADD(S)@0.1d，为三者中相对最稳健的方法，但在极端光照下同样出现剧烈衰减。
- **PicoPose**：集成的由粗到精（coarse-to-fine）RGB零样本方法。在Emergency标准光下达到67.83%的ADD(S)@0.3d，但在极端光照下降至36.23%，性能损失超过31个百分点。

此外，论文还引入了实例级方法 **GDRNPP** 作为真值质量验证手段。GDRNPP在Tennis标准光下达到96.50%的ADD(S)@0.3d，证实了数据集标注的可靠性；而模型无关方法 **OnePose++** 在相同条件下仅20.96%，凸显了极端运动对几何匹配方法的挑战。

### 2. 方法适用边界

EgoXtreme的实验揭示了现有零样本方法的三个关键适用边界：

**光照边界**：极端低光照是导致性能崩溃的首要因素。在Emergency场景中，FoundPose的ADD(S)@0.1d从标准光的6.31%骤降至极端光的0.10%（降幅98.4%），GigaPose在Maintenance场景中也从33.64%降至13.78%（降幅58.9%）。这表明现有方法依赖的视觉特征提取在严重光照退化下几乎完全失效。

**运动边界**：高速运动（Sports场景中物体速度可达1.37 m/s）带来的运动模糊导致帧间信息断裂。直接时间传播策略（Direct temporal）在动态场景下性能退化高达46个百分点（@0.3d），说明基于单帧独立估计的零样本方法缺乏有效的运动先验利用机制。

**预处理的不适用性**：一个反直觉的发现是，图像复原预处理（去模糊、去雾、低光增强）不仅未能提升姿态估计性能，反而系统性降低了精度。组合预处理在Maintenance场景将PicoPose的0.3d召回率降低约5个百分点，在Emergency场景降低约8个百分点。去雾方法在Emergency场景甚至导致0.1d召回率从23.39%骤降至4.74%。这表明现有复原方法引入的伪影和噪声破坏了对精确6D匹配至关重要的判别性特征。

### 3. 与相关数据集的定位关系

EgoXtreme在6D姿态估计数据集谱系中占据了独特的“自我中心+极端条件”生态位。相较于现有基准：

- **BOP挑战赛数据集**（如LM-O、YCB-V、T-LESS）聚焦于桌面或工业场景的标准光照条件，缺乏运动模糊和动态光照变化。
- **HOT3D**等自我中心数据集虽提供了手物交互标注，但未系统覆盖极端视觉退化条件。
- EgoXtreme通过三类场景（Sports、Maintenance、Emergency）和多种光照/烟雾条件的因子化设计，首次实现了对极端条件下零样本泛化能力的细粒度诊断。

### 4. 局限与开放问题

**数据集本身的局限**：

1. **缺乏手部姿态标注**：数据集未提供精确的3D手部姿态真值，无法评估手物交互的完整上下文，限制了在AR/VR操控任务中的应用验证。
2. **环境覆盖有限**：采集环境均为室内场景，尚未覆盖夜间户外、雨雪天气等更极端的真实光照和天气条件。
3. **烟雾场景单一**：烟雾分布不均匀且仅覆盖特定场景，可能无法代表火灾现场等真实救援环境中的复杂视觉遮挡模式。
4. **实例级方法的泛化鸿沟**：虽然GDRNPP等实例级方法表现良好，但需针对每个新物体重新训练，无法直接应用于零样本设置。

**值得进一步探索的开放问题**：

1. **极端运动下的手部标注**：如何在高速运动和严重模糊条件下生成准确的3D手部姿态真值？这可能需要融合多传感器信息（如IMU、电磁跟踪）或设计专门的优化框架。
2. **室外扩展**：如何将数据集扩展到包含复杂天气（雨、雪、雾）和更丰富自然光照的室外真实环境，同时保持6D真值的精度？
3. **面向姿态估计的专用复原**：现有图像复原方法为人类视觉设计，如何设计专门保留或增强判别性特征的复原模块（如保持纹理细节的去模糊、保持边缘的去雾），使其真正服务于下游姿态估计而非引入噪声？
4. **自适应时间融合**：混合时间跟踪策略在Sports场景中展现了显著优势（Tennis的ADD(S)@0.3d从22.77%回升至50.55%），但如何在维持实时性的前提下，自适应地融合多帧信息并处理严重遮挡？这涉及置信度评估机制的设计和计算效率的平衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/EgoXtreme_A_Dataset_for_Robust_Object_Pose_Estimation_in_Egocentric_Views_under_Extreme_Conditions.pdf]]
---
title: "Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Rethinking_Camera_Choice_An_Empirical_Study_on_Fisheye_Camera_Properties_in_Robotic_Manipulation.pdf
project_link: "https://robo-fisheye.github.io/"
code_link: "https://github.com/kaustubh-sadekar/OmniCV-Lib"
aliases:
- RSAR
- RCCESFCPRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过随机尺度增强（Random Scale Augmentation, RSA）迫使策略学习相对空间关系（如物体相对于夹爪的尺度），而非记忆绝对像素尺寸。
primary_logic: 鱼眼相机的超大视场角（FoV）能捕获更多背景特征点，从而提升空间定位能力；但这依赖于环境的视觉丰富度。在具备足够多样性的训练场景下，鱼眼相机能带来远优于标准相机的场景泛化能力；而跨镜头泛化的核心障碍是尺度过拟合，可通过RSA有效缓解。
claims:
- 鱼眼相机的空间定位优势严重依赖于环境的视觉特征丰富度；在特征贫乏的背景中收益甚微。
- 在具有足够场景多样性的训练下，鱼眼相机的场景泛化能力超越标准针孔相机，且随着训练场景数增加性能提升更快。
- 跨镜头迁移失败的根本原因是策略对绝对物体尺度的过拟合，而随机尺度增强（RSA）通过强迫策略学习相对尺度关系，显著缓解了该问题。
- Robomimic / MimicGen (six tasks in simulation) 上 Success Rate = Fisheye (Single) average 0.66 on feature-rich backgrounds
---

# Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation

> [!tip] 核心洞察
> 鱼眼相机的超大视场角（FoV）能捕获更多背景特征点，从而提升空间定位能力；但这依赖于环境的视觉丰富度。在具备足够多样性的训练场景下，鱼眼相机能带来远优于标准相机的场景泛化能力；而跨镜头泛化的核心障碍是尺度过拟合，可通过RSA有效缓解。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新思考相机选择：鱼眼相机在机器人操作中的属性实证研究 |
| 英文题名 | Rethinking Camera Choice: An Empirical Study on Fisheye Camera Properties in Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.02139) · [Project](https://robo-fisheye.github.io/) · [Code](https://github.com/kaustubh-sadekar/OmniCV-Lib) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Random Scale Augmentation (RSA) |
| Dataset | Robomimic / MimicGen, Real‑world Pick Cup task, Cross‑camera transfer on six simulation tasks, Real‑world cross‑camera transfer |

> [!tip] 效果简介
> - Robomimic / MimicGen (six tasks in simulation) 上，Success Rate Fisheye (Single) average 0.66 on feature-rich backgrounds vs Pinhole (Single) average 0.34 on feature-rich backgrounds (+0.32)。
> - Real‑world Pick Cup task (scene diversity scaling) 上，Zero‑shot Success Rate Fisheye policy > 95% with 8 training scenes vs Pinhole policy < 60% with 8 training scenes (> +35%)。
> - Cross‑camera transfer on six simulation tasks (Seen Param → unseen Params) 上，Average Success Rate RSA policy maintains high success across all unseen parameters vs Standard Aug. policy collapses on Params 4/5 (e.g., ~0.0 success) (RSA prevents catastrophic drop)。

## 概要

机器人操作策略高度依赖视觉输入，但相机模型的选择——尤其是鱼眼相机与标准针孔相机——对策略的空间推理、泛化能力和跨硬件迁移鲁棒性的影响，此前缺乏系统性实证研究。该工作围绕这一空白，构建了从仿真到真实世界的完整分析框架，系统拆解了四个关键因子：**相机模型**（鱼眼 vs 针孔）、**场景复杂度**（视觉特征贫乏 vs 丰富）、**场景多样性**（单场景 vs 多场景训练）以及**相机参数**（内参变化导致的几何域偏移）。

研究的核心瓶颈在于：当策略在不同鱼眼镜头之间迁移时，会严重**过拟合于物体的绝对像素尺度**，导致空间推理失效——例如，将因镜头参数变化而“变大”的物体误判为更近，进而产生灾难性动作决策。针对这一问题，作者提出了**随机尺度增强（Random Scale Augmentation, RSA）**：在训练时从均匀分布 $s \sim U(0.7, 1.3)$ 采样随机尺度因子，对图像进行中心裁剪并缩放至固定输入尺寸；当 $s > 1.0$ 时执行“zoom-out”并以零值填充，迫使策略学习物体相对于夹爪的**相对空间关系**，而非记忆绝对像素尺寸。

实验揭示了三项决定性发现：
1. **空间定位依赖于视觉丰富度**：鱼眼相机的超宽视场角（仿真 235°，真实 180°）能捕获更多背景特征点，从而显著提升空间定位能力，但这一优势在缺乏明显视觉特征的纯色背景中大幅衰减。
2. **场景多样性解锁泛化能力**：在具备足够多样性的训练场景下，鱼眼相机的场景泛化能力远超针孔相机——真实世界中，仅用 8 个训练场景，鱼眼策略的零样本成功率即突破 95%，而针孔策略不足 60%。
3. **RSA 有效缓解跨镜头迁移失败**：标准增强策略在未见相机参数下性能崩溃（成功率近乎为 0），而 RSA 策略在仿真六项任务上维持高成功率，在真实世界跨镜头迁移中将窄视场镜头得分从 0.500 提升至 0.950，宽视场镜头得分从 0.003 提升至 0.600。

在方法谱系上，该工作以 **Diffusion Policy**（Chi et al., RSS 2023）为模仿学习骨架，将固定尺度裁剪替换为 RSA，并在仿真中采用无预训练 ResNet-18、真实世界中采用 CLIP ViT-B/16 作为纯视觉编码器，刻意移除本体感受输入以独立评估视觉定位质量。鱼眼仿真管线基于 MuJoCo 物理引擎，通过立方体贴图→等距柱状投影→鱼眼视角的两阶段投影实现，支持 EUCM/双球面等畸变模型。整体框架定位于**视觉机器人学习的传感器选择与数据增强交叉地带**，为后续超广角视觉策略的设计提供了明确的因果机理和可复现的基准。



### 机器人操作中的视觉感知瓶颈

机器人操作策略长期依赖标准针孔相机作为视觉输入源。然而，针孔相机的视场角（Field of View, FoV）通常局限在 60°–90° 范围内，这在操作任务中引入了一个根本性矛盾：当机械臂接近目标物体时，相机与物体之间的距离急剧缩小，导致物体部分或完全移出视野。这种“近视”效应迫使策略要么依赖本体感受信息补偿视觉信息的缺失，要么在关键操作阶段陷入视觉盲区。

现有模仿学习框架——如 **Diffusion Policy**（Chi et al., RSS 2023）——已在多种操作任务上取得显著进展，但其视觉骨干几乎无一例外地针对标准针孔图像设计。这留下了一个未被系统审视的问题：**相机模型本身的选择是否构成了当前操作策略性能上限的隐性约束？**

### 鱼眼相机的未被充分利用

鱼眼相机提供远超针孔相机的视场角（典型可达 180° 甚至 235°），理论上能够在机械臂全工作空间内维持对目标物体和周围环境的持续观测。这种“始终可见”的特性对操作任务尤为关键：策略无需依赖记忆或本体感受推断物体位置，而是可以直接从视觉信号中提取空间关系。

然而，鱼眼相机在机器人操作社区中始终处于边缘地位。这一方面源于仿真环境中缺乏真实的鱼眼相机模型，使得大规模策略训练无法开展；另一方面，社区对鱼眼相机的实际收益缺乏定量认知——宽视场角究竟在何种条件下转化为性能提升？是否存在隐藏的代价？

### 三个核心研究缺口

本文围绕以下三个未被充分解答的问题展开：

1. **空间定位能力（RQ1）**：鱼眼相机的宽视场角是否确实增强了策略的空间定位能力？这种增益是否依赖于环境的视觉特征丰富度？
2. **场景泛化能力（RQ2）**：在训练场景有限的条件下，鱼眼相机能否帮助策略抵抗背景过拟合？其泛化能力如何随训练场景多样性扩展？
3. **跨硬件迁移能力（RQ3）**：当策略从训练时的鱼眼镜头迁移至不同内参的镜头时，性能崩溃的根本原因是什么？能否通过数据增强缓解？

### 本文的核心动机

本文的出发点并非主张“鱼眼相机永远优于针孔相机”，而是试图建立一套系统性的实证分析框架，揭示相机选择对策略行为的因果影响机制。通过在 MuJoCo 物理引擎中实现真实鱼眼相机仿真管线（两阶段投影：立方体贴图 → 等距柱状投影 → 鱼眼视角，支持 EUCM/双球面等畸变模型），本文首次在受控条件下对上述三个问题进行大规模定量研究。

更重要的是，本文识别出跨镜头迁移失败的**核心瓶颈**——策略对物体绝对像素尺度的过拟合——并提出 **Random Scale Augmentation (RSA)** 作为针对性缓解方案。这一发现不仅解释了鱼眼相机使用中的一个关键痛点，也为未来的相机无关策略学习提供了方法论启示。



## 核心方法与创新机理

### 1. 问题诊断：跨镜头迁移失败的根源是绝对尺度过拟合

本文通过系统的跨相机参数迁移实验，首次明确诊断出机器人模仿学习策略在鱼眼镜头间迁移失败的**核心瓶颈**：策略并非学习物体的空间位置或相对关系，而是**过拟合于物体在图像中的绝对像素尺度**。当相机内参（如视场角、焦距）改变导致同一物体的像素尺寸发生变化时，策略会产生严重的空间推理错误——例如，将因镜头变化而“变大”的物体误判为距离夹爪更近，从而输出错误的抓取动作（见 Figure 9）。

这一诊断是整篇工作的逻辑起点，直接引出了后续的解决方案设计。

### 2. 方法创新：随机尺度增强 (Random Scale Augmentation, RSA)

针对上述瓶颈，本文提出了**随机尺度增强 (Random Scale Augmentation, RSA)**，一种简单但高效的训练时数据增强策略。其核心机制如下：

- **尺度采样**：对每张训练图像，从宽均匀分布 $s \sim U(0.7, 1.3)$ 中随机采样一个尺度因子 $s$。
- **中心裁剪与缩放**：以该尺度因子对图像进行中心裁剪，并缩放至网络标准输入尺寸。当 $s > 1.0$ 时，操作等效于“缩小”（zoom‑out），超出边界的区域以零值填充。
- **强迫相对尺度学习**：RSA 迫使网络在训练过程中持续观察目标物体与夹爪手指在不同相对尺度下的视觉模式，从而打破对绝对像素尺寸的依赖，转而学习**物体相对于夹爪的尺度关系**等空间不变特征。

与基线方法（**Diffusion Policy** (Chi et al., RSS 2023) 使用的固定尺度裁剪，如 0.95）相比，RSA 的关键区别在于尺度采样的**随机性**和**宽范围**（见 Figure 3）。固定裁剪仅提供单一尺度，无法覆盖跨镜头迁移中出现的尺度变化。

### 3. 跨镜头泛化的因果调节变量

RSA 的提出建立在一个清晰的因果逻辑之上：跨镜头迁移性能下降的**因果调节变量**是策略对绝对尺度的依赖程度。RSA 通过随机化训练时的物体尺度，直接干预这一变量，从而显著提升策略对未见相机参数的鲁棒性。实验证据表明：

- 在仿真六任务平均中，标准增强策略在未见相机参数（Params 4/5）上成功率**塌缩至约 0.0**，而 RSA 策略维持了高成功率（见 Figure 10）。
- 在真实世界跨镜头迁移中，RSA 将窄视场镜头（150°）的归一化得分从 0.500 提升至 **0.950**，将宽视场镜头（220°）的得分从 0.0025 恢复至 **0.600**（见 Table S10）。

### 4. 与现有工作的关系

RSA 并非对模仿学习算法架构的修改，而是作用于**数据增强层面**的轻量级改进。它可以与不同的策略骨干网络结合使用——本文在 **Diffusion Policy** 和 **π0.5** 两种架构上均验证了其有效性（见 Table S9），表明 RSA 的增益独立于具体策略架构，具有较好的通用性。

从方法论谱系来看，RSA 属于**域随机化 (Domain Randomization)** 在视觉尺度维度的定向应用。与传统的颜色抖动、随机裁剪等增强不同，RSA 专门针对相机内参变化引起的尺度域偏移问题，是对机器人操作中视觉泛化技术栈的有针对性补充。



本研究构建了一套系统性的分析框架，旨在解耦并评估鱼眼相机在机器人操作策略学习中的关键属性。如图 1 所示，该框架围绕四个核心维度展开：(a) **相机模型**（鱼眼 vs. 针孔）作为主对比基线；(b) **场景复杂度**（特征贫乏 vs. 特征丰富）用于探究空间定位能力（RQ1）；(c) **场景多样性**（单场景 vs. 多场景训练）用于评估场景泛化能力（RQ2）；(d) **相机参数**（不同内参配置）用于测试跨硬件迁移能力（RQ3）。

### 方法管线

整个实验管线的核心模块及数据流如下：

1.  **鱼眼相机仿真（Fisheye Camera Simulation）**：在 MuJoCo 物理引擎中实现了一个两阶段投影管线（立方体贴图 → 等距柱状投影 → 鱼眼视角），支持 EUCM 和双球面等畸变模型，以逼真地模拟 235°（仿真）和 180°（真实世界）视场角的鱼眼成像过程（图 2）。真实世界数据则直接通过物理鱼眼镜头采集。

2.  **视觉编码器（Visual Encoder）**：仿真实验采用无预训练的 ResNet‑18，真实世界实验采用 CLIP ViT‑B/16。**关键设计选择**是移除了所有本体感受（proprioception）输入，使策略完全依赖视觉信号进行空间推理，从而独立测试鱼眼相机的视觉定位能力。

3.  **动作预测骨干（Diffusion Policy）**：采用 **Diffusion Policy**（Chi et al., RSS 2023）作为模仿学习核心算法，使用 U‑Net 架构和 DDIM 调度器建模多模态动作分布。仿真中使用相对帧间变换的 delta action，真实世界中使用相对于动作块首帧的 relative action。

4.  **随机尺度增强（Random Scale Augmentation, RSA）**：针对跨镜头迁移的核心瓶颈——策略对绝对物体尺度的过拟合——提出的关键数据增强模块。对于每张训练图像，从均匀分布 $s \sim U(0.7, 1.3)$ 采样随机尺度因子，进行中心裁剪并缩放至网络输入尺寸。当 $s > 1.0$ 时执行“zoom-out”操作并以零值填充边缘区域。RSA 通过强制策略观察物体和夹爪在不同相对尺度下的视觉关系，迫使其学习相对空间关系而非记忆绝对像素尺寸（图 3）。

5.  **评估协议**：仿真评估遵循标准 Robomimic/MimicGen 协议（50 次 rollout 计算成功率）；真实世界评估采用多阶段归一化评分机制：

    $$\mathrm{Normalized~Score} = \frac{\mathrm{Total~points~earned}}{\mathrm{Total~number~of~stages}}$$

    该指标将每个任务分解为 2‑3 个关键阶段，累积计分并归一化，提供比二元成功率更细粒度的性能信号。

### 数据流与公平性控制

整个管线的输入输出流清晰：**输入**为鱼眼或针孔相机采集的 RGB 图像（无本体感受），经视觉编码器提取特征后送入 Diffusion Policy 预测动作；**输出**为末端执行器的相对位姿变换。所有对比实验严格控制**总数据量不变**（Fixed Total Data Volume），排除数据规模对结论的干扰。仿真与真实世界均排除第三人称视角相机，确保性能差异仅归因于腕部相机类型的选择。视觉编码器在不同域中统一选用常用架构，超参数对齐现有工作，保证比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the four factors analyzed to address our Research Questions (RQs). We study: (a) Camera Model (fisheye vs. pinhole) as our primary comparison; (b) Scene Complexity (poor vs. rich) for spatial localization (RQ1); (c) Scene Diversity (1 vs. N scenes) for scene generalization (RQ2); and (d) Camera Parameters (varied intrinsics) for hardware generalization (RQ3)*



### 鱼眼相机仿真管线

本文在 MuJoCo 物理引擎中实现了一个两阶段投影管线，以逼真地模拟鱼眼相机的成像过程（Figure 2）：

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/002_Figure_2.jpg]]
*Figure 2: The implementation pipeline of fisheye camera simulation in MuJoCo [48]*

1. **立方体贴图渲染**：首先将场景渲染到立方体贴图的六个面上，捕获全向视觉信息。
2. **等距柱状投影转换**：将立方体贴图转换为等距柱状投影（equirectangular projection）格式。
3. **鱼眼视角采样**：从等距柱状投影中采样目标鱼眼视角，支持多种畸变模型（如 EUCM、双球面模型等），最终输出模拟的鱼眼图像。

该管线参考了 **OmniCV-Lib**（Sadekar et al., 2020）的设计思路，能够在仿真中灵活调整鱼眼相机的视场角（FoV）和内参，为后续的系统性消融实验提供了可控的测试平台。

### 随机尺度增强（Random Scale Augmentation, RSA）

RSA 是本文提出的核心数据增强方法，旨在解决策略跨相机镜头迁移时的性能崩溃问题。其根本机制是打破策略对物体绝对像素尺度的过拟合，迫使网络学习相对空间关系（如物体相对于夹爪的尺度）。

#### 操作流程

对于每个训练图像，RSA 执行以下步骤（Figure 3）：

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/003_Figure_3.jpg]]
*Figure 3: Random Crop Augmentation (fixed scale) vs. Random Scale Augmentation (RSA) for cross-camera generalization*

1. **随机尺度采样**：从均匀分布中采样尺度因子 $s$：
   $$s \sim U(0.7, 1.3)$$

2. **中心裁剪与缩放**：以采样尺度 $s$ 对图像进行中心裁剪，并缩放至网络标准输入尺寸。

3. **Zoom-out 处理**：当 $s > 1.0$ 时，裁剪区域超出原始图像边界，此时对超出部分进行补零填充（zero-padding），等效于“缩小”操作。这使得网络能够观察到物体在图像中变小的情形，打破其对特定像素尺度的记忆。

#### 与固定尺度裁剪的对比

标准增强方法通常采用固定尺度裁剪（如始终裁剪至原图的 95%），导致训练过程中物体始终以相近的绝对像素尺寸出现。当策略迁移到不同内参的相机时，同一物体在图像中的像素尺寸发生显著变化，策略因无法适应而崩溃。RSA 通过大范围的随机尺度扰动（0.7× 至 1.3×），使网络在训练阶段就暴露于多样化的物体尺度下，从而习得尺度不变的空间推理能力。

### 真实世界评估：归一化多阶段评分

为在真实世界实验中提供细粒度的性能信号，本文定义了归一化多阶段评分指标：

$$\mathrm{Normalized~Score} = \frac{\mathrm{Total~points~earned}}{\mathrm{Total~number~of~stages}}$$

其中，每个操作任务被分解为 2–3 个关键阶段（如 Pick Cup 任务分为“接近杯子”、“抓取杯子”、“举起杯子”），策略在每个阶段成功完成则获得相应分数。最终得分归一化至 $[0, 1]$ 区间。该指标相较于简单的二元成功率，能够更精细地反映策略的部分能力，尤其在策略未完全失败但表现退化时提供有用信号。

### 策略学习框架

本文采用 **Diffusion Policy**（Chi et al., RSS 2023）作为视觉模仿学习的核心算法，使用 U-Net 架构和 DDIM 调度器建模多模态动作分布。为独立测试视觉定位能力，实验中移除了本体感受输入（state-free 设置），视觉编码器在仿真中使用 ResNet-18（无预训练），在真实世界中使用 CLIP ViT-B/16。动作空间在仿真中采用相对连续帧的增量动作，在真实世界中采用相对动作块首帧的相对变换。



## 实验与关键发现

### 实验设置概览

为系统回答三个核心研究问题（RQ1–RQ3），本文在仿真和真实世界两个域中构建了统一的评估框架。仿真实验基于 MuJoCo 物理引擎，选取 Robomimic/MimicGen 基准中的六个操作任务：**Square**、**Tool Hang**、**Coffee**、**Threading**、**Assembly** 和 **Mug Cleanup**（Figure 4）。真实世界实验在配备可更换背景幕布的 Franka Emika Panda 机械臂平台上进行，覆盖三个任务：**Pick Cup**、**Fold Towel** 和 **Hang Chinese Knot**（Figure 5）。

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/004_Figure_4.jpg]]
*Figure 4: The six tasks in simulation experiments*

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/005_Figure_5.jpg]]
*Figure 5: (a) The real-world experiment setup, which includes changeable backgrounds for scene complexity (RQ1) and scene generalization (RQ2) experiments. (b) The three tasks in real-world experiments: Pick Cup, Fold Towel and Hang Chinese Knot*

所有对比实验严格控制总数据量不变（Fixed Total Data Volume），排除数据规模对结论的干扰。仿真与真实世界均移除第三人称视角相机，仅依赖腕部相机输入，以独立分析鱼眼相机效应。策略采用无本体感受的纯视觉编码器（仿真：ResNet-18 无预训练；真实世界：CLIP ViT-B/16），动作空间在仿真中使用 delta action，真实世界中使用 relative action。真实世界评估引入多阶段归一化评分：

$$\mathrm{Normalized~Score} = \frac{\mathrm{Total~points~earned}}{\mathrm{Total~number~of~stages}}$$

该指标将每个任务分解为 2–3 个关键阶段，累积计分后归一化，提供比二元成功率更细粒度的性能信号。

### RQ1：鱼眼相机的空间定位优势依赖于视觉特征丰富度

**核心发现：鱼眼相机的宽 FoV 优势并非无条件成立，而是严重依赖于环境中的视觉特征密度。在特征贫乏的场景中，鱼眼相机的性能增益大幅缩水甚至消失。**

仿真结果（Table 1）显示：在特征丰富的背景（feature-rich）下，单腕鱼眼相机（Fisheye Single）平均成功率达到 0.66，而针孔相机（Pinhole Single）仅为 0.34，绝对提升 +0.32。然而，当背景切换为特征贫乏的纯色幕布（feature-poor）时，鱼眼相机的优势显著收窄，部分任务甚至出现性能倒退。真实世界实验（Figure 6）进一步验证了这一趋势：在特征丰富背景下，鱼眼相机在三个任务上的归一化得分平均增益为 +0.39；而在特征贫乏背景下，增益骤降至 +0.18。

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/006_Figure_6.jpg]]
*Figure 6: Real-world performance of fisheye / pinhole cameras with different scene complexity (feature-poor v.s. feature-rich) in three tasks (RQ1)*

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/007_Table_1.jpg]]
*Table 1: Simulation performance of fisheye / pinhole cameras with different scene complexity (feature-poor v.s. feature-rich) (RQ1). Performance in feature-rich backgrounds is shown with the absolute difference (in parentheses) compared to the feature-poor background baseline for the same camera*

为量化视觉编码器的空间感知质量，本文设计了本体感受预测代理任务：在预训练视觉编码器上微调轻量级 MLP 头，预测机器人末端执行器的位姿。Table 2 的结果表明，鱼眼编码器在特征丰富环境下的平移预测误差仅为 1.73 cm，显著优于针孔编码器；但在特征贫乏环境中，两者的差距急剧缩小。这从表示层面证实：宽 FoV 的空间定位优势源于对更多背景特征点的捕获能力，当环境缺乏可区分的视觉锚点时，该优势自然瓦解。

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/009_Table_2.jpg]]
*Table 2: Quantitative probing of visual encoder spatial awareness using proprioception prediction as a proxy task (RQ1). We evaluate the quality of learned spatial representations by fine-tuning a lightweight MLP head on the pre-trained visual encoder to predict the robot’s proprioceptive state in three real-world tasks*

**消融实验**进一步排除了本体感受输入的混淆效应。Table S3 显示，移除本体感受后，针孔相机策略的成功率从 0.62 骤降至 0.34（-45%），而鱼眼相机仅从 0.75 降至 0.66（-12%），证明鱼眼相机的视觉定位能力远更鲁棒。更引人注目的是，在真实世界中，无本体感受的鱼眼策略（归一化得分 0.67）甚至超过了有本体感受的针孔策略（0.52）（Table S4），凸显出宽 FoV 在空间感知上的绝对优势。此外，即使额外添加第三人称视角相机，鱼眼相机仍保持平均 +0.05 的成功率优势（Table S5），表明其增益并非冗余。

### RQ2：场景多样性是解锁鱼眼泛化潜力的关键

**核心发现：在训练场景多样性不足时，鱼眼策略更容易过拟合于简单场景；但当训练场景数量增加时，其场景泛化能力超越针孔相机，且性能提升速度更快。**

Figure 8 展示了策略零样本泛化性能随训练场景数增加的缩放曲线。在仿真 Coffee 任务中，当仅使用 1 个训练场景时，鱼眼策略的泛化成功率低于针孔策略，表现出更强的过拟合倾向；但随着训练场景数增至 5 个，鱼眼策略迅速反超。真实世界 Pick Cup 任务的趋势更为显著：使用 8 个多样化训练场景后，鱼眼策略在未见环境上的零样本成功率超过 95%，而针孔策略仍低于 60%，差距超过 35 个百分点。

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/010_Figure_8.jpg]]
*Figure 8: The policy performance improves with the number of training scenes in (a) simulation experiments on Coffee task and (b) real-world experiments on Pick Cup task (RQ2)*

这一现象揭示了鱼眼相机的双重性：宽 FoV 捕获了更多背景信息，在训练场景单一时，这些额外信息成为干扰源，导致策略记忆特定场景的视觉模式而非学习可迁移的技能；但当训练场景足够多样时，宽 FoV 反而提供了更丰富的空间线索，使策略能够学习到跨场景鲁棒的空间关系。该发现具有重要的实践指导意义：部署鱼眼相机时，必须配合充分的场景多样性训练，否则其优势可能逆转为劣势。

### RQ3：跨镜头迁移的核心障碍是尺度过拟合

**核心发现：策略在跨鱼眼镜头迁移时严重过拟合于物体的绝对像素尺度，导致空间推理失效。随机尺度增强（RSA）通过迫使策略学习相对尺度关系，显著缓解了该问题。**

跨镜头迁移的失败模式具有高度一致性：当训练镜头的 FoV 与测试镜头不同时，同一物体在图像中的像素尺寸发生变化，策略会因此产生系统性误判——例如将变大的物体误认为更近，或对变小的物体“视而不见”（Figure 9）。这揭示出标准模仿学习策略并非在推理物体的三维空间位置，而是在记忆“特定任务中物体应有的像素尺寸”。

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/012_Figure_9.jpg]]
*Figure 9: The failure cases of cross-hardware generalization (RQ3). The policy tends to overfit the absolute scale*

针对这一瓶颈，本文提出 **Random Scale Augmentation (RSA)**：对每个训练图像，从均匀分布 $s \sim U(0.7, 1.3)$ 采样随机尺度因子，中心裁剪至该尺度后缩放至网络输入尺寸。当 $s > 1.0$ 时，该操作实现“zoom-out”效果，超出图像边界的区域以零填充（Figure 3）。RSA 的核心机制在于：它打破了物体绝对像素尺寸与空间位置之间的虚假相关性，迫使策略关注物体相对于夹爪的尺度关系等真正具有空间意义的线索。

Figure 10 展示了 RSA 在仿真六任务上的跨镜头泛化效果。标准增强策略（蓝色）在未见相机参数（Params 4/5）上出现灾难性性能崩塌，平均成功率趋近于 0；而 RSA 策略（橙色）在所有未见参数上维持了高成功率，呈现出宽广的泛化平台。在真实世界跨镜头迁移实验中（Table S10），使用 π0.5 架构配合 RSA 后，窄角镜头（150° FoV）的归一化得分从 0.500 恢复至 0.950，广角镜头（220° FoV）从 0.003 恢复至 0.600。详细的尺度扰动消融（Table S9）进一步证实：RSA 在不同尺度偏移下始终优于标准增强，例如在 $S=0.70$ 的极端缩小场景下，Diffusion Policy 的成功率从 0.000 恢复至 0.725。

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/011_Figure_10.jpg]]
*Figure 10: The policy performance under different unseen camera parameters , averaged across six tasks in simulation (RQ3)*

![[assets/figures/papers/paper_list_l2646_https_arxiv_org_abs_2603_02139/figures/034_Table_S.10.jpg]]
*Table S.10: Real-world Cross-camera Generalization with RSA*

### 失败模式与局限性分析

尽管 RSA 大幅缓解了跨镜头迁移的性能下降，但并未完全解决该问题。最显著的残余失败出现在真实世界的广角镜头（220° FoV）场景：RSA 策略的归一化得分仅恢复至 0.600，与训练镜头的性能（约 0.95）仍有显著差距。这表明，除绝对尺度外，鱼眼镜头特有的径向畸变分布变化等几何域偏移仍构成独立挑战——RSA 无法模拟不同畸变模型下物体形状的系统性扭曲。

另一重要局限在于仿真与真实世界之间的视觉复杂度鸿沟。本文报告仿真环境的特征密度约为真实世界的 1/13，这意味着仿真中观察到的“特征贫乏”与真实世界中的“特征贫乏”可能处于不同的绝对水平。这一差异可能影响 RQ1 结论的跨域一致性，需要在实际部署时进行针对性校准。

最后，真实世界实验仅覆盖三个任务和三种镜头配置（180° 训练，150°/220° 测试），RSA 在更多样化任务（如高精度装配、动态操作）和更极端镜头参数下的泛化能力仍有待验证。视觉编码器消融（Table S7）虽已证明宽 FoV 的优势独立于 ResNet 或 CLIP 等具体架构选择，但在更大规模的视觉-语言-动作模型（VLA）预训练场景下，鱼眼相机数据和 RSA 增强的系统性价值仍是开放问题。



## 定位与知识库关联

### 1. 在模仿学习与数据增强谱系中的定位

本文的核心学习框架建立在 **Diffusion Policy**（Chi et al., RSS 2023）之上，采用 U‑Net 架构与 DDIM 调度器来建模多模态动作分布。与标准 Diffusion Policy 的固定尺度裁剪增强（如固定裁剪比例 0.95）不同，本文提出的 **Random Scale Augmentation (RSA)** 将尺度因子从均匀分布 $s \sim U(0.7, 1.3)$ 中随机采样，并在 $s > 1.0$ 时执行“缩小”（zoom‑out）并补零填充。这一改动看似微小，却直接针对了跨镜头迁移的核心瓶颈——策略对物体绝对像素尺度的过拟合。

在视觉编码器选择上，本文在仿真中使用无预训练的 ResNet‑18，在真实世界中使用 CLIP ViT‑B/16，并通过消融实验（Table S7）证明鱼眼相机的优势独立于具体编码器架构。值得注意的是，本文刻意移除了本体感受输入（proprioceptive input），以纯粹测试视觉定位能力——这与当前主流方法（如 **π0.5** 等大规模架构通常融合多模态状态）形成对比。实验表明，无本体感受的鱼眼策略（0.67）甚至超过了有本体感受的针孔策略（0.52），这为纯视觉操作策略的设计提供了有力论据。

### 2. 与鱼眼视觉及全向感知工作的关系

本文在仿真中实现了基于 MuJoCo 的两阶段投影管线（立方体贴图 → 等距柱状投影 → 鱼眼视角），并支持 EUCM/双球面等畸变模型，其设计灵感来自 **OmniCV‑Lib**（Sadekar et al., 2020）。这一仿真管线使得在物理引擎中系统研究鱼眼相机属性成为可能，填补了此前机器人操作领域缺乏可控鱼眼仿真环境的空白。

与现有全向视觉工作相比，本文的独特贡献在于将鱼眼相机的分析从“能否使用”推进到“何时有效”和“如何泛化”的机制层面。具体而言：
- 本文揭示了鱼眼相机空间定位优势的**条件性**：在特征丰富的背景中，鱼眼相机平均成功率较针孔相机提升 +0.32（仿真）和 +0.39（真实世界归一化得分）；但在特征贫乏的背景中，这一优势显著衰减。这一发现对盲目推广鱼眼相机提出了审慎警告。
- 本文证明了鱼眼相机的场景泛化能力需要**足够的训练场景多样性**作为前提：当训练场景数从 1 增加到 8 时，鱼眼策略的零样本成功率从不足 60% 迅速超过 95%，而针孔策略的增长明显更慢。

### 3. 适用边界与局限性

尽管 RSA 在跨镜头迁移中展现出显著效果，其适用边界仍需明确：

**已识别的局限：**
1. **仿真‑真实视觉复杂度鸿沟**：仿真环境与真实世界在特征密度上存在约 13 倍的差距，这可能影响部分结论的跨域一致性。本文虽在真实世界中验证了核心结论，但更复杂的真实场景（如动态光照、遮挡）仍有待测试。
2. **任务与硬件覆盖有限**：真实世界实验仅覆盖 Pick Cup、Fold Towel、Hang Chinese Knot 三个任务和有限硬件配置（180° 训练，150°/220° 测试）。RSA 在更多样化任务和极端镜头参数下的泛化能力有待验证。
3. **跨镜头迁移未完全解决**：RSA 虽将 Wide Lens（220°）的性能从 0.0025 恢复至 0.6000，但距离训练域性能仍有差距。这表明绝对尺度之外的因素——如径向畸变分布的变化——仍构成几何域偏移的残余挑战。
4. **无本体感受的权衡未深入探讨**：本文为纯净测试视觉能力而移除本体感受，但在实际系统中融入本体感受可能进一步提升鲁棒性，这一设计空间的权衡未展开分析。

### 4. 开放问题与未来方向

**增强策略的自适应化：**
RSA 的尺度采样范围 $U(0.7, 1.3)$ 是固定的。一个自然的问题是：能否根据目标相机的内参动态调整采样分布，以进一步最小化跨镜头迁移的性能损失？例如，当目标镜头 FoV 更宽时，可能需要更大的尺度下界来覆盖更极端的缩小场景。

**大规模预训练中的泛化潜力：**
本文在补充实验中验证了 RSA 在 **π0.5** 架构上的有效性，这暗示鱼眼相机数据与 RSA 增强可能系统性地提升更大规模视觉‑语言‑动作模型（VLA）的泛化能力。在 **GEN‑0**（Generalist AI Team, 2025）等强调物理交互规模化的具身基础模型框架中，鱼眼相机的大 FoV 优势是否能转化为更高效的空间推理学习，是一个值得探索的方向。

**畸变感知的表征学习：**
除尺度外，鱼眼镜头特有的径向畸变分布对策略学习的具体影响机制尚不清楚。能否设计畸变感知的增强策略或表示学习方法（如对比学习），使策略对畸变参数的变化具有内在鲁棒性？这可能需要将相机内参显式地注入视觉编码器。

**环境多样性的替代方案：**
本文表明，当训练数据缺乏环境多样性时，鱼眼相机的泛化潜力无法释放。是否存在其他数据增强或表示学习方法可以部分替代真实场景多样性？例如，通过域随机化或生成式背景增强，能否在有限真实场景下解锁鱼眼相机的泛化能力？

**传感器配置的对称性：**
本文结论是否对称地适用于其他超广角或全向视觉传感器配置（如多相机环视系统、360° 全景相机）？不同传感器配置可能引入不同的遮挡模式和几何先验，其对空间定位和泛化的影响机制值得系统研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Rethinking_Camera_Choice_An_Empirical_Study_on_Fisheye_Camera_Properties_in_Robotic_Manipulation.pdf]]

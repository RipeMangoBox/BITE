---
title: "Motion-2-to-3: Leveraging 2D Motion Data to Boost 3D Motion Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation.pdf
code_link: null
project_link: https://zju3dv.github.io/Motion-2-to-3
aliases:
- M23
- Motion-2-to-3
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将运动解耦为局部关节运动（相对根节点）与全局根运动，并通过预训练2D局部运动扩散模型学习丰富的局部运动先验，再结合3D数据微调多视图生成模块，以同时确保多视图一致性和全局运动。
primary_logic: 从2D视频中学习到的局部人体运动模式具有通用性，通过根解耦可将其与全局运动分离；利用这一先验在3D数据有限的情况下大幅提升生成质量并扩展运动类型。
claims:
- 在HumanML3D基准上，Motion-2-to-3的FID达到0.321，显著优于所有基线，最优基线OMG的FID为0.381。
- 在新颖文本提示的用户研究中，Motion-2-to-3获得51.43%的最佳动作率，远高于MDM和MLD。
- 消融实验表明，去除2D预训练导致FID从0.321恶化至4.950，验证了2D数据预训练的关键作用。
- HumanML3D 上 FID = 0.321
---

# Motion-2-to-3: Leveraging 2D Motion Data to Boost 3D Motion Generation

> [!tip] 核心洞察
> 从2D视频中学习到的局部人体运动模式具有通用性，通过根解耦可将其与全局运动分离；利用这一先验在3D数据有限的情况下大幅提升生成质量并扩展运动类型。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion-2-to-3：利用2D运动数据提升3D运动生成 |
| 英文题名 | Motion-2-to-3: Leveraging 2D Motion Data to Boost 3D Motion Generation |
| 会议/期刊 | ICCV 2025 |
| Links |  [Project](https://zju3dv.github.io/Motion-2-to-3)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Motion-2-to-3 |
| Dataset | HumanML3D, Novel Text Prompts |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.321 vs 0.381 (OMG / SOTA) (-0.060)。
> - Novel Text Prompts (user study) 上，Best Motion Rate 51.43% vs MDM/MLD (lower) (N/A (significantly higher))。

## 概要

**问题瓶颈**：现有文本驱动的3D人体运动生成模型严重依赖3D运动捕捉数据（如HumanML3D），其规模与多样性远不及海量的2D视频数据。然而，真实世界2D视频中的人体运动同时混合了相机运动和人体自身的全局运动（Figure 2），导致直接利用2D数据训练3D生成模型极为困难——缺乏有效的机制从2D数据中提取纯净的人体运动先验并将其桥接到3D生成任务中。

**核心洞察**：本文的关键思路是将人体运动解耦为**局部关节运动**（相对于根节点的运动）与**全局根运动**。局部运动模式（如“挥手”、“踢腿”）在2D与3D之间具有高度的通用性，而全局运动（如“向前走”、“绕圈跑”）则受相机视角和3D空间位置的影响。通过从2D视频中分离出局部运动序列，可以学习到丰富的运动先验，再结合少量3D数据恢复多视图一致性和全局轨迹，从而在3D数据受限的情况下大幅提升生成质量并扩展运动类型。

**方法定位**：本文提出**Motion-2-to-3**流水线，属于“2D数据驱动的3D运动生成”范式。与仅使用3D数据的扩散模型（如**MDM** (Tevet et al., ICLR 2023)、**MLD** (Kong et al., ICCV 2023)）或开放词汇生成方法（**OMG** (Liang et al., CVPR 2024)）不同，Motion-2-to-3先在解耦后的大规模2D局部运动上预训练单视图扩散模型，再冻结预训练层并增加多视图注意力层与根速度预测头，利用3D数据进行微调，最终通过三角化和根轨迹累积恢复完整的3D运动。

**主要结果**：在HumanML3D基准上，Motion-2-to-3的FID达到**0.321**，显著优于最优基线OMG的0.381（Table 1）。在新颖文本提示的用户研究中，该方法获得**51.43%**的最佳动作率，远超MDM和MLD（Table 2）。消融实验表明，去除2D预训练会导致FID从0.321急剧恶化至4.950，验证了2D数据预训练的关键作用（Table 4）。



### 3D人体运动生成的瓶颈

数据驱动的3D人体运动生成近年来取得了长足进步，但其根本瓶颈在于高质量3D标注数据的稀缺。现有的文本条件3D运动生成模型——如**MDM**（Tevet et al., ICLR 2023）、**MLD**（Kong et al., ICCV 2023）和**OMG**（Liang et al., CVPR 2024）——几乎完全依赖3D运动捕捉（MoCap）数据进行训练。然而，3D动捕数据的采集成本极高，需要专业的硬件设备、受控的室内环境和大量的人工标注，导致公开可用的3D运动数据集在规模和多样性上均十分有限。以最常用的HumanML3D数据集为例，其涵盖的动作类型远不足以覆盖真实世界中丰富的人类行为。

### 2D数据利用的核心挑战

一个自然的思路是利用海量的2D视频数据来弥补3D数据的不足。互联网上存在数以万计的包含人体运动的视频，通过现成的2D姿态估计器可以从中提取大量2D运动序列。然而，从真实世界视频中提取的2D运动数据存在一个根本性挑战：2D观测同时混合了**人体自身的局部运动**和**摄像机的全局运动**（Figure 2）。当摄像机在3D空间中移动时，即使人体保持静止，其在图像平面上的投影位置也会发生变化。这种耦合使得直接使用2D运动数据训练3D生成模型变得极为困难——模型无法区分哪些运动变化来自人体关节的旋转，哪些来自相机运动或人体的全局位移。

### 现有方法的缺口

此前已有工作尝试利用2D运动数据辅助3D运动生成，例如**MAS**通过生成多视图2D运动来间接获得3D结果，但该方法缺乏文本控制能力，无法支持文本条件生成。另一种策略是利用预训练的3D运动特征提取器（如**MotionBERT**，Zhu et al., ICCV 2023）从2D数据中提取特征作为条件信号，但这种方式未能从根本上解决2D与3D运动表示之间的鸿沟，尤其在生成全局运动方面表现不佳。总体而言，现有方法缺乏一种有效的机制，能够从大规模2D数据中提取通用的运动先验，并将其无缝桥接到3D运动生成任务中。

### 本文的核心动机

Motion-2-to-3的核心动机源于一个关键洞察：**从2D视频中学习到的局部人体运动模式具有跨维度的通用性**。如果将运动解耦为相对于根节点的局部关节运动与描述全局位移的根运动，那么局部运动部分在2D和3D之间共享相同的运动学结构——它描述的是人体各关节相对于身体中心的位置变化，与相机视角和全局位置无关。基于这一洞察，本文提出通过**根解耦**策略，从大规模2D视频中学习局部运动先验，再结合有限的3D数据进行多视图一致性微调，从而在3D数据受限的条件下大幅提升生成质量并扩展可生成的运动类型。



## 核心方法与创新机理

Motion-2-to-3 的核心创新在于**将 2D 运动数据中的局部人体运动先验桥接到 3D 运动生成任务**，通过运动解耦与多视图扩散两个关键设计，突破了现有 3D 运动生成模型受限于动捕数据规模与多样性的瓶颈。

### 瓶颈突破：从 2D 视频中提取可迁移的运动先验

现有 3D 人体运动生成模型（如 **MDM**，Tevet et al., ICLR 2023；**MLD**，Kong et al., ICCV 2023；**OMG**，Liang et al., CVPR 2024）完全依赖 3D 运动捕捉数据（如 HumanML3D）进行训练。这类数据采集成本高昂，导致数据规模与运动类型多样性严重受限。大规模 2D 视频数据虽然蕴含丰富的运动模式，却因混合了相机运动与人体全局运动而无法直接用于训练——2D 投影中观察到的运动是两者耦合的结果（Figure 2）。

Motion-2-to-3 的因果开关在于**将运动解耦为局部关节运动（相对根节点）与全局根运动**。这一解耦使得从 2D 视频中学习到的局部运动模式（如“挥手”、“踢腿”的关节相对运动）具有通用性，不再受相机视角或人体全局位移的干扰。消融实验强有力地验证了这一设计：去除 2D 预训练后，FID 从 0.321 急剧恶化至 4.950（Table 4），证明 2D 局部运动先验对生成质量的决定性作用。

### 关键设计：changed slots 分析

相较于仅使用 3D 数据的基线方法，Motion-2-to-3 在以下四个维度进行了系统性改进：

**1. 运动表示：从全局 3D 到解耦的 2D/3D 局部运动 + 根速度**

基线方法通常使用 263 维的全局 3D 表示（包含根位置与关节旋转）。Motion-2-to-3 将运动重新定义为解耦的局部运动与根速度序列：2D 局部运动 $\mathcal{M}_l \in \mathbb{R}^{N \times (J-1) \times 2}$ 捕获关节相对于根节点的运动模式，根速度序列则独立编码全局位移。这一表示天然适配 2D 数据的特性，同时为后续多视图一致性的 3D 恢复奠定基础。

**2. 训练数据源：从纯 3D 动捕到大规模 2D 视频 + 3D 数据联合**

这是最根本的 changed slot。Motion-2-to-3 首次将大规模 2D 视频数据引入 3D 运动生成的训练流程。2D 数据用于预训练阶段学习丰富的局部运动先验，3D 数据则用于微调阶段确保多视图一致性与全局运动的准确性。Table 3 的对比实验表明，与使用 MotionBERT 特征（Zhu et al., ICCV 2023）或直接使用 2D 条件相比，该解耦策略在生成全局运动方面具有明显优势——基线方法无法生成带有全局位移的运动（Figure 5）。

**3. 模型架构：从单视图扩散到“预训练 2D 单视图 + 微调多视图”**

基线方法采用单视图文本条件扩散模型直接生成 3D 运动。Motion-2-to-3 采用两阶段架构：首先在 2D 局部运动上预训练单视图扩散模型 $\mathcal{D}_{2D}$，学习局部运动先验；随后在 $\mathcal{D}_{2D}$ 基础上增加多视图注意力层和根速度头，构建多视图扩散模型 $\mathcal{D}_{mv}$。多视图注意力层负责在 V 个虚拟视角之间建立一致性约束，根速度头则专门预测全局运动信息。

**4. 训练策略：从端到端到冻结预训练层**

在微调阶段，$\mathcal{D}_{2D}$ 的原始层被冻结，仅训练新增的多视图注意力层和根速度头（Section 3.2）。这一策略保护了从大规模 2D 数据中学到的局部运动先验不被 3D 数据的有限规模所覆盖，同时将学习重点聚焦于视角一致性和全局运动建模。消融实验中的“w/ CB”变体（Table 4）试图引入显式的一致性约束模块，反而导致 FID 升至 0.642，表明冻结预训练层配合隐式多视图注意力机制已能充分保证一致性。

### 从 2D 先验到 3D 输出的因果链路

整个 pipeline 的因果链路可概括为：2D 局部运动预训练提供通用运动先验 → 多视图扩散模型在 3D 数据微调下生成多视图一致的 2D 局部运动与根速度 → 三角化模块将多视图 2D 局部运动恢复为 3D 局部运动 → 根速度累积得到 3D 全局轨迹 $x_{r3d}^{f+1} = x_{r3d}^{f} + v_{r3d}^{f} \Delta t$ → 两者结合形成完整 3D 运动。该链路的核心洞察在于：**局部运动的“语义”具有视角不变性**，2D 数据中学到的局部运动模式可直接迁移到 3D 生成的各个视角中，从而在 3D 数据有限的情况下大幅扩展可生成的运动类型。



Motion-2-to-3 的整体 pipeline 围绕一个核心洞察构建：**将人体运动解耦为局部关节运动与全局根运动**，从而让模型能够从大规模 2D 视频数据中学习通用的局部运动先验，再通过 3D 数据微调来恢复多视图一致的三维运动。整个框架由四个关键模块串联而成，形成从文本到可驱动 3D 角色的端到端生成流程。

### 1. 2D 运动扩散模型（预训练阶段）

第一阶段在**纯 2D 域**进行。给定从视频中提取的 2D 人体姿态序列，首先将每帧的根节点位置减去，得到与全局位移无关的局部运动表示 $\mathcal{M}_l \in \mathbb{R}^{N \times (J-1) \times 2}$。基于此，训练一个 transformer 架构的扩散模型 $\mathcal{D}_{2D}$，以 CLIP 文本嵌入 $\mathcal{T} \in \mathbb{R}^{77 \times 768}$ 为条件，学习 2D 局部运动的分布。该模型的核心作用是**从海量 2D 数据中习得丰富的人体局部运动先验**，为后续 3D 生成提供语义与运动模式的底层支撑。

### 2. 多视图扩散模型（微调阶段）

第二阶段将预训练好的 $\mathcal{D}_{2D}$ 扩展为多视图扩散模型 $\mathcal{D}_{mv}$。具体改动包括：
- **新增多视图注意力层**：在原有单视图 transformer 层之间插入跨视图注意力机制，使不同虚拟摄像机视角下的 2D 运动生成能够相互感知，确保多视图一致性。
- **新增根速度预测头**：在输出端增加一个分支，同步预测每个视角下的根速度 $\mathcal{M}_{vr}$，从而恢复被解耦掉的全局运动信息。
- **冻结预训练参数**：遵循迁移学习的最佳实践，原始 $\mathcal{D}_{2D}$ 的所有层被冻结，仅训练新增的多视图注意力层和根速度头。输入为加噪的多视图 2D 局部运动 $\mathcal{M}_{vl}^t \in \mathbb{R}^{N \times V \times (J-1) \times 2}$ 及相应的根速度噪声 $\mathcal{M}_{vr}^t$，同时注入虚拟摄像机的相对姿态嵌入 $\mathcal{C}_{rel} \in \mathbb{R}^{V \times 4}$ 作为条件。

### 3. 三角化恢复 3D 局部运动

推理时，$\mathcal{D}_{mv}$ 从纯噪声出发，通过迭代去噪生成 $V$ 个视角的干净 2D 局部运动与根速度。随后，利用已知的虚拟摄像机参数，对多视图 2D 局部关节位置进行**三角化**，直接恢复出 3D 空间中的局部关节坐标。这一步将 2D 先验转化为具有空间一致性的 3D 骨架运动。

### 4. 根轨迹累积与 SMPL 拟合

最后，将每帧预测的 3D 根速度按时间累积，得到完整的 3D 根轨迹：

$$x_{r3d}^{f+1} = x_{r3d}^{f} + v_{r3d}^{f} \Delta t$$

将 3D 局部运动与全局根轨迹结合，即获得完整的 3D 人体运动序列。为得到可直接驱动角色的参数化表示，再通过 SMPLify 将恢复的 3D 关节位置拟合到 SMPL 模型上，输出姿态参数。

### 数据流与模块关系总览

整个 pipeline 的数据流可概括为：**文本 → 2D 局部运动先验（$\mathcal{D}_{2D}$）→ 多视图 2D 运动（$\mathcal{D}_{mv}$）→ 3D 局部运动（三角化）→ 3D 全局运动（根轨迹累积）→ SMPL 姿态**。其中，2D 预训练阶段与 3D 微调阶段的解耦设计是方法成功的关键——消融实验表明，去除 2D 预训练将导致 FID 从 0.321 急剧恶化至 4.950（Table 4），充分验证了 2D 局部运动先验对最终生成质量的决定性作用。

### 补充图表

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Our Pipeline. We design a Multi-view Diffusion model (a) to generate multi-view results (for simplicity, camera embedding is omitted in the figure). During inference, the Multi-view Diffusion model predicts 2D local motion and root velocity (b). Then, we use triangulation [23] to recover 3D local joint positions (c) and accumulate root velocity to obtain 3D global trajectory (d), resulting in the final 3D motion (e)*

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our key idea. (a) Our approach leverages 2D motion data to improve 3D motion generation by unifying 2D and 3D motion data. (b) Our framework yields better FID and generates a broader range of motion types*



Motion-2-to-3 的核心思路是：将运动解耦为**局部关节运动**（相对于根节点的运动）与**全局根运动**，从而让模型从大规模2D视频数据中学习通用的局部运动先验，再通过多视图机制恢复3D一致性。整个管线由四个关键模块串联构成。

### 2D运动解耦与表示

原始2D运动数据同时包含人体自身运动与相机运动，直接建模会引入歧义（Figure 2）。为此，论文将2D人体运动 $\mathcal{M} \in \mathbb{R}^{N \times J \times 2}$（$N$ 帧，$J$ 个关节）分解为两部分：

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Challenge of 2D motion from the real world. In the real-world videos [30], both the camera and humans move in 3D space, resulting in 2D motion that combines both movements*

- **2D局部运动** $\mathcal{M}_l \in \mathbb{R}^{N \times (J-1) \times 2}$：将每帧根节点位置从所有关节位置中减去，得到相对于根的局部关节运动。
- **根速度** $\mathcal{M}_r \in \mathbb{R}^{N \times 1 \times 2}$：相邻帧根节点位置的差分，编码全局位移。

这一解耦的因果逻辑是：局部运动模式（如“挥手”“蹲下”）具有跨视角、跨场景的通用性，而全局轨迹（如“向前走”“绕圈”）则与场景和相机绑定。分离后，2D视频中的局部运动即可作为干净的训练信号。

### 2D局部运动扩散模型（$\mathcal{D}_{2D}$）

第一阶段在**大规模2D视频数据**上预训练一个单视图扩散模型，仅建模局部运动 $\mathcal{M}_l$。模型采用 Transformer 架构的扩散框架，以 CLIP 文本嵌入 $\mathcal{T} \in \mathbb{R}^{77 \times 768}$ 作为条件，学习文本到局部运动的映射。

该阶段的核心作用是**建立丰富的局部运动先验**——2D视频数据规模远超3D动捕数据，覆盖的动作类型更广，使模型在3D数据稀缺的情况下仍能生成多样且自然的局部姿态。

### 多视图扩散模型（$\mathcal{D}_{mv}$）

第二阶段在 $\mathcal{D}_{2D}$ 的基础上扩展为多视图生成器，并用**少量3D数据微调**。具体改动包括：

- **多视图注意力层**：在冻结的原始 $\mathcal{D}_{2D}$ 层之间插入新的交叉注意力层，使 $V$ 个虚拟摄像机视角的生成相互一致。
- **根速度头**：新增一个输出头，预测每个视角下的2D根速度 $\mathcal{M}_{vr} \in \mathbb{R}^{N \times V \times 1 \times 2}$。
- **摄像机条件**：输入虚拟摄像机的相对姿态嵌入 $\mathcal{C}_{rel} \in \mathbb{R}^{V \times 4}$，使模型感知多视图几何关系。

扩散步 $t$ 时，输入为加噪的多视图局部运动 $\mathcal{M}_{vl}^t \in \mathbb{R}^{N \times V \times (J-1) \times 2}$ 和根速度 $\mathcal{M}_{vr}^t$，模型预测去噪后的干净信号。训练时**仅更新新增层**，预训练权重冻结，从而保留2D先验的同时强制多视图一致性。

### 三角化与3D重建

推理阶段，$\mathcal{D}_{mv}$ 输出 $V$ 个视角的干净2D局部运动和根速度后，通过以下步骤恢复完整3D运动：

1. **三角化**：利用已知的虚拟摄像机参数，将多视图2D局部关节位置三角化为3D局部关节位置。
2. **3D根轨迹累积**：将各视角预测的2D根速度通过摄像机几何提升为3D根速度 $v_{r3d}^f$，再逐帧累积得到全局3D根轨迹：

$$x_{r3d}^{f+1} = x_{r3d}^{f} + v_{r3d}^{f} \Delta t$$

其中 $x_{r3d}^f$ 为第 $f$ 帧的3D根位置，$\Delta t$ 为帧间隔。

3. **SMPLify拟合**：将恢复的3D关节位置拟合到SMPL模型，获得可直接驱动角色的姿态参数。

### 关键公式汇总

| 公式 | 含义 | 出处 |
|------|------|------|
| $\mathcal{M}_l \in \mathbb{R}^{N \times (J-1) \times 2}$ | 减去根位置后的2D局部运动序列 | Section 3.1 |
| $\mathcal{T} \in \mathbb{R}^{77 \times 768}$ | CLIP文本嵌入，作为扩散条件 | Section 3.1 |
| $\mathcal{C}_{rel} \in \mathbb{R}^{V \times 4}$ | $V$ 个虚拟摄像机的相对姿态嵌入 | Section 3.2 |
| $\mathcal{M}_{vl}^t \in \mathbb{R}^{N \times V \times (J-1) \times 2}$ | 扩散步 $t$ 的多视图2D局部运动噪声输入 | Section 3.2 |
| $\mathcal{M}_{vr}^t \in \mathbb{R}^{N \times V \times 1 \times 2}$ | 扩散步 $t$ 的多视图根速度噪声输入 | Section 3.2 |
| $x_{r3d}^{f+1} = x_{r3d}^{f} + v_{r3d}^{f} \Delta t$ | 3D根轨迹累积递推公式 | Section 3.3 |

> **注意**：以上公式均来自论文 Section 3 的明确定义，未做任何外推或推导。扩散模型的具体噪声调度、损失函数形式等细节论文未提供完整公式，此处不做猜测性补充。



## 实验与关键发现

### 瓶颈验证：2D预训练是性能核心

消融实验（Table 4）直接验证了论文的核心主张。在HumanML3D基准上，完整的Motion-2-to-3模型取得了**FID = 0.321**的最佳性能。当移除2D预训练（w/o pretrain），即多视图扩散模型从头训练而不使用2D Motion Diffusion模型的预训练权重时，FID急剧恶化至**4.950**，性能下降超过一个数量级。这一结果以0.98的置信度证实：从大规模2D视频数据中学习到的局部运动先验，是模型在3D数据有限情况下实现高质量生成的决定性因素。

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/014_Table_4.jpg]]
*Table 4: Ablation study of Multi-view Diffusion model. The best and second-best results are highlighted green and yellow*

定性结果（Figure 6）进一步印证了这一发现：无预训练的模型生成的动作不自然、存在语义错位，而完整模型的动作更加逼真且与文本描述一致。

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/013_Figure_6.jpg]]
*Figure 6: Qualitative results of ablation study. Our full model generates more natural motion than the ablations. The unnatural poses are highlighted in the red boxes. The semantics misalignment is highlighted in the dashed boxes*

### 主结果：HumanML3D基准与新颖文本提示

**Table 1** 报告了在HumanML3D数据集上的文本条件运动生成对比结果。Motion-2-to-3的FID达到**0.321**，显著优于所有仅使用3D数据训练的基线方法。最优基线**OMG**（Liang et al., CVPR 2024）的FID为0.381，本方法在此基础上提升了**0.060**。其他对比方法包括**MDM**（Tevet et al., ICLR 2023）、**MLD**（Kong et al., ICCV 2023）等，性能差距更为明显。

**Table 2** 展示了在新颖文本提示（训练分布外的动作描述）上的用户研究结果。Motion-2-to-3获得了**51.43%**的最佳动作率（Best Motion Rate），远高于MDM和MLD。若随机选择，预期最佳动作率仅为33%，本方法显著超越了随机水平，表明2D数据预训练有效扩展了模型可生成的动作类型范围。

### 消融与分析

#### 2D数据利用策略对比

**Table 3** 比较了不同2D数据利用策略。与使用**MotionBERT**（Zhu et al., ICCV 2023）预训练特征或直接使用2D条件信号相比，本方法提出的根解耦策略在生成全局运动方面具有明显优势。基线方法无法生成包含全局位移的运动（Figure 5），而本方法通过解耦局部运动与根速度，成功保留了2D数据中的局部运动先验，同时实现了全局运动的可控生成。

#### 多视图扩散模型设计选择

**Table 4** 汇总了多视图扩散模型的关键消融：

1. **视图数量**：使用**4个虚拟摄像机**（View=4）取得最佳FID（0.321）。视图过少（View=3，FID=0.654）或过多（View=5，FID=0.593）均导致性能下降，表明4视图在信息充分性与模型复杂度之间取得了平衡。

2. **一致性模块（w/ CB）**：引入显式的一致性约束模块非但未提升性能，反而使FID升至**0.642**。这表明本方法的多视图注意力机制已隐式学习了足够的视图一致性，额外的硬约束反而限制了生成灵活性。

3. **冻结预训练层**：微调阶段仅训练新增的多视图注意力层和根速度头，冻结原始2D扩散层。这一策略确保了预训练先验不被破坏，同时高效适配多视图生成任务。

### 失败模式与局限

1. **2D姿态估计依赖**：最终3D运动质量受限于2D姿态估计精度。当2D关键点存在噪声或缺失时，三角化恢复的3D运动可能出现伪影。

2. **虚拟摄像机敏感性**：模型对训练时的虚拟摄像机设置（视角数、相对姿态）敏感，泛化到不同摄像机配置的能力有限。

3. **新奇动作泛化**：尽管在分布外文本提示上表现优于基线，但生成训练时完全未见过的极端姿态或复杂动作组合的能力仍然受限。

4. **多人场景未验证**：当前框架仅针对单人运动设计，尚未在多人交互或复杂场景下验证适用性。

### 公平性说明

论文未系统评估不同人口群体或运动类型的公平性。HumanML3D数据集和2D视频来源可能存在人口统计偏差，可能影响某些人群或动作类型的生成质量。该点需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/004_Table_1.jpg]]
*Table 1: Comparison of text-conditional motion synthesis on HumanML3D [20] dataset. These metrics are evaluated by the motion encoder from [20]. The right arrow → means the closer to real motion the better. The dash − denotes the results are unavailable as they do not release the code. The best and second-best results are highlighted green and yellow, respectively*

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/005_Table_3.jpg]]
*Table 3: Comparison of 2D Data utilization strategies. Our strategy for leveraging 2D data obtains superior performance compared to baseline methods*

![[assets/figures/papers/paper_list_l1892_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation on the novel text prompts. Best Motion Rate and Top-2 Motion Rate represent the proportions of being selected as the best motion and as one of the top two motions. If selected randomly, the expected rate would be 33%*



## 定位与知识库关联

### 1. 与现有工作的关系

Motion-2-to-3 处于**文本条件3D人体运动生成**这一主线，其核心贡献在于率先将大规模2D视频数据以解耦方式引入3D运动扩散模型的训练。本节从运动生成范式、2D数据利用策略、以及多视图生成三个维度定位其谱系位置。

#### 1.1 相对于3D运动扩散模型的继承与突破

在Motion-2-to-3之前，文本到3D运动的扩散模型已形成两条主要技术路线：

- **直接在原始运动空间扩散**：以 **MDM**（Tevet et al., ICLR 2023）为代表，在3D关节旋转或位置表示上执行扩散过程。此类方法受限于3D动捕数据的规模与多样性，生成的运动类型集中在数据集中高频出现的动作上。
- **在潜空间扩散**：以 **MLD**（Kong et al., ICCV 2023）为代表，通过VAE将运动压缩到低维潜空间再进行扩散，提高了采样效率，但并未解决数据稀缺带来的多样性瓶颈。

Motion-2-to-3 对此谱系的**关键突破**在于：将训练数据源从“仅3D动捕”扩展为“大规模2D视频 + 3D动捕”。这一突破的因果机制是：2D视频中蕴含的局部人体运动模式（关节相对于根节点的运动）具有跨视角通用性，通过**根解耦**可将其与混杂的相机运动和全局人体运动分离，从而提取出可迁移的局部运动先验。在HumanML3D基准上，Motion-2-to-3的FID达到0.321，显著优于仅使用3D数据训练的最优基线**OMG**（Liang et al., CVPR 2024）的0.381（Table 1），验证了2D数据引入的有效性。

#### 1.2 相对于2D数据利用策略的差异化

在Motion-2-to-3之前，已有工作尝试利用2D数据辅助3D运动生成，但存在根本性局限：

- **MotionBERT**（Zhu et al., ICCV 2023）：通过预训练的2D/3D运动编码器提取特征表示，但该特征混合了全局运动信息，无法有效迁移到需要生成全局运动的文本条件生成任务中。如Table 3所示，使用MotionBERT特征作为条件的方案在生成全局运动方面表现不佳。
- **MAS**：从2D数据生成多视图2D运动，但缺乏文本控制能力，无法实现文本到3D运动的端到端生成。

Motion-2-to-3 的差异化策略体现在**运动表示的重新定义**上：将2D人体运动显式分解为局部关节运动 $\mathcal{M}_l \in \mathbb{R}^{N \times (J-1) \times 2}$ 和根速度序列。这一表示层面的创新使得2D局部运动扩散模型 $D_{2D}$ 学到的先验（如行走、挥手等局部姿态模式）可以直接迁移到3D生成的微调阶段，而无需处理2D数据中混杂的相机运动和全局位移。

#### 1.3 相对于多视图生成范式的定位

Motion-2-to-3的多视图扩散机制借鉴了多视图图像生成的思想，但针对运动生成做了关键适配：

- **架构继承**：在预训练的单视图2D扩散模型 $D_{2D}$ 基础上，增加多视图注意力层以建模跨视图一致性，这与多视图图像扩散模型的扩展方式类似。
- **训练策略创新**：冻结 $D_{2D}$ 的原有层，仅训练新增的多视图注意力层和根速度头。这一策略确保了2D预训练知识不被破坏，同时将学习焦点集中在视图一致性约束和全局运动生成上。
- **与显式一致性约束的对比**：消融实验（Table 4）显示，引入额外的Consistency Block（w/ CB）反而导致FID从0.321升至0.642，表明所提出的隐式多视图注意力机制已足够维持视图一致性，显式约束反而过度限制了生成多样性。

### 2. 适用边界

#### 2.1 数据依赖边界

Motion-2-to-3的性能依赖于两个数据条件：

- **2D姿态估计质量**：2D局部运动从视频中通过姿态估计器提取，当2D关键点存在噪声或缺失时，预训练的先验质量下降，最终3D运动可能出现伪影。论文未量化评估不同姿态估计精度下的性能退化程度，此点需要手动验证。
- **3D微调数据规模**：尽管2D预训练大幅降低了对3D数据的需求，微调阶段仍需要一定规模的3D动捕数据（论文使用HumanML3D）。在3D数据极度稀缺（如仅数百条）的场景下，模型性能的退化曲线未被报告。

#### 2.2 摄像机配置敏感度

多视图扩散模型对虚拟摄像机的设置敏感：

- **视图数量**：消融实验（Table 4）表明，4个视图取得最优FID（0.321），视图数降至3（FID=0.654）或升至5（FID=0.593）均导致性能下降。视图过少导致三角化约束不足，视图过多则增加模型学习难度。
- **相对姿态分布**：论文未系统研究不同摄像机相对姿态配置（如视角间距、仰角范围）对生成质量的影响，这一边界的定量刻画缺失。

#### 2.3 运动类型覆盖范围

尽管论文声称支持更广泛的运动类型，但其泛化能力存在边界：

- **训练分布内的运动**：在HumanML3D覆盖的动作类型上表现优异。
- **新颖文本提示**：用户研究（Table 2）中，Motion-2-to-3在“新颖文本提示”上获得51.43%的最佳动作率，显著高于MDM和MLD，表明对分布外文本具有一定的泛化能力。
- **极端姿态与高度动态动作**：论文未测试体操、杂技等极端姿态或高动态动作的生成质量，此边界需要手动验证。

### 3. 局限与开放问题

#### 3.1 已识别的局限

1. **2D姿态估计的级联误差**：最终3D运动质量依赖2D姿态估计的精度，当2D关键点有噪声或缺失时，三角化恢复的3D局部运动会出现伪影。这是一个结构性局限，非模型设计可完全规避。

2. **摄像机配置的敏感性**：模型对训练时使用的虚拟摄像机设置（视角数、相对姿态）敏感，部署时若实际摄像机配置与训练分布不匹配，性能可能下降。

3. **复杂场景的未验证性**：尚未验证在多人交互、严重遮挡、或人物与物体交互等复杂场景下的适用性。

4. **生成运动的物理合理性**：通过SMPLify拟合获得最终姿态参数，但未显式建模物理约束（如足部接触、质心平衡），可能导致漂浮或滑动伪影。

#### 3.2 开放研究问题

1. **2D预训练范式的跨任务推广**：根解耦策略能否推广到手部运动生成、面部动画、以及人物-物体交互运动？这些任务同样面临3D数据稀缺而2D数据丰富的困境，但局部运动的定义和解耦方式需要重新设计。

2. **2D数据规模的扩展效应**：更大规模、更多样化的2D视频数据集（如包含更多运动类型、更多拍摄角度）能否进一步提高生成质量？是否存在2D数据引入的收益递减点？

3. **视图数量的最小化**：能否将多视图需求降至2个视图甚至单目设置？这将显著降低部署门槛，但需要更强的单视图3D重建先验或时序约束来弥补视图信息的减少。

4. **真实世界视频的鲁棒性**：当前2D预训练使用何种2D视频数据（论文未详细披露数据来源和规模），在真实世界in-the-wild视频（多人、遮挡、运动模糊）下的鲁棒性如何？此点需要手动验证。

5. **实时驱动与物理交互集成**：生成的3D运动能否无缝集成到游戏引擎或实时驱动管线中，并支持物理交互（如碰撞响应、环境适应）？这涉及运动表示与物理引擎的接口设计问题。

6. **公平性与偏差评估**：论文未系统评估不同人口群体或运动类型的公平性。HumanML3D和2D视频来源可能存在人口统计偏差，可能影响某些人群或动作的生成质量。此方向的方法论和评估基准均属空白。



## 原文 PDF

![[paperPDFs/ICCV_2025/Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation.pdf]]

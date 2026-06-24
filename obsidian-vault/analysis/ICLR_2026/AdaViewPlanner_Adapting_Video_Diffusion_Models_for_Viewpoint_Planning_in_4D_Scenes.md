---
title: "AdaViewPlanner: Adapting Video Diffusion Models for Viewpoint Planning in 4D Scenes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.pdf
openreview_forum_id: c2EfS9E5CJ
aliases:
- AAVDMVP4S
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "利用预训练视频扩散模型中蕴含的电影摄影先验，通过两阶段适配（先基于人体运动生成包含相机运动的视频，再从视频中提取相机姿态）实现符合文本指令的视点规划。"
primary_logic: "预训练文本到视频模型内部已经编码了丰富的电影摄影技能和场景知识，可通过注入4D场景表征（如人体运动）继承这些先验，从而在给定4D内容和文本指令时自动生成专业且多样的相机轨迹。"
claims:
- "本方法在所有基线方法上表现优越，用户偏好率超过60%。"
- "在AMASS和GTA-Human真实数据上，本方法在视点规划指标上大幅超过E.T.和DanceCam*。"
- "E.T. Testset (SMPL-based) 上 HMR (Human Missing Rate) ↓ = 0.044"
- "E.T. Testset 上 TCC (Text-Camera Consistency) ↑ = 1.125"
---

# AdaViewPlanner: Adapting Video Diffusion Models for Viewpoint Planning in 4D Scenes

> [!tip] 核心洞察
> 预训练文本到视频模型内部已经编码了丰富的电影摄影技能和场景知识，可通过注入4D场景表征（如人体运动）继承这些先验，从而在给定4D内容和文本指令时自动生成专业且多样的相机轨迹。

| 字段      | 内容                                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------------ |
| 中文题名    | AdaViewPlanner：针对4D场景的视点规划中适配视频扩散模型                                                                          |
| 英文题名    | AdaViewPlanner: Adapting Video Diffusion Models for Viewpoint Planning in 4D Scenes                          |
| 会议/期刊   | ICLR 2026                                                                                                    |
| Links   | [paper](https://openreview.net/forum?id=c2EfS9E5CJ); [Project](https://yuli0103.github.io/AdaViewPlanner/)   |
| Topic   | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method  | AdaViewPlanner                                                                                               |
| Dataset | E.T. Testset (SMPL-based), E.T. Testset, Ours Testset (curated, 240 samples)                   |

> [!tip] 效果简介
> - E.T. Testset (SMPL-based) 上，HMR (Human Missing Rate) ↓ 为 0.044，对比 0.064 (E.T.)，变化 -0.020。
> - E.T. Testset 上，TCC (Text-Camera Consistency) ↑ 为 1.125，对比 0.850 (E.T.)，变化 +0.275。
> - E.T. Testset 上，User Preference (%) ↑ 为 61.90，对比 23.81 (E.T.) / 14.29 (DanceCam*)，变化 +38.09 / +47.61。

## 概述

自动电影摄影旨在为4D场景生成专业、符合指令的相机轨迹。现有方法依赖有限数据集训练的专业模型，难以泛化到开放世界场景，且缺乏对文本指令等偏好控制的支持；手动设计相机轨迹则既繁琐又需要专业知识。

AdaViewPlanner 的核心洞察是：预训练文本到视频（T2V）扩散模型内部已经编码了丰富的电影摄影技能和场景知识。通过将4D场景表征（人体运动）注入T2V模型，可以继承这些先验，从而在给定4D内容和文本指令时自动生成专业且多样的相机轨迹。

为此，该方法提出一个两阶段范式：Stage I 通过姿态编码器和空间运动注意力将归一化4D人体运动 $M \in \mathbb{R}^{f \times k \times 3}$ 注入预训练T2V模型，生成蕴含相机运动的视频；Stage II 基于MMDiT框架，以生成视频和人体运动为条件，通过流匹配目标直接提取绝对相机姿态序列 $C \in \mathbb{R}^{f \times 9}$。

实验表明，AdaViewPlanner 在多个基准上显著超越现有方法：在E.T.测试集上，人体缺失率（HMR）从0.064降至0.044，文本-相机一致性（TCC）从0.850提升至1.125；在真实运动数据AMASS上，HMR从0.033降至0.015，镜头多样性（Dist_t）从0.422提升至1.437。用户研究中，本方法的偏好率超过60%，远高于基线方法的23.81%（E.T.）和14.29%（DanceCam*）。

## 背景与动机

4D场景的自动电影摄影旨在为动态内容（如人物表演）自动生成符合专业审美且与指令一致的相机轨迹。然而，现有方法面临一个核心瓶颈：**依赖有限数据集训练的专业模型难以泛化到开放世界场景**。例如，E.T. 仅利用点轨迹驱动相机运动，DanceCamera3D 则从音频和舞姿生成相机参数，这些方法在训练数据覆盖范围之外的场景中表现受限，且缺乏对文本指令等细粒度偏好控制的能力。与此同时，手动设计相机轨迹既繁琐又需要深厚的电影摄影专业知识，难以规模化应用。

该瓶颈背后的因果机制在于：**自动相机轨迹生成本质上需要丰富的电影摄影先验和场景理解能力，而这些能力无法从规模有限的特定任务数据集中充分习得**。预训练文本到视频（T2V）扩散模型在互联网规模的视频数据上训练，其内部已经编码了丰富的电影摄影技能（如镜头构图、运镜节奏）和场景知识。因此，一个自然的思路是：能否通过适配预训练视频扩散模型，将其蕴含的电影摄影先验“迁移”到视点规划任务中？

AdaViewPlanner 正是基于这一核心洞察而提出。该方法采用**两阶段适配范式**：第一阶段将4D场景表征（人体运动序列 $M \in \mathbb{R}^{f \times k \times 3}$）注入预训练T2V模型，通过空间运动注意力机制生成包含隐含相机运动的电影级视频；第二阶段则以生成的视频和原始人体运动为条件，通过MMDiT框架直接提取绝对相机姿态序列 $C \in \mathbb{R}^{f \times 9}$。这种设计允许模型在给定4D内容和文本指令时，自动生成既符合指令语义又具备专业电影摄影风格的多样化相机轨迹。

**证据强度**：Table 1 显示，AdaViewPlanner 在 E.T. 测试集和自建测试集上的用户偏好率分别达到 61.90% 和 63.33%，远超 E.T.（23.81%）和 DanceCam*（14.29%）；在 AMASS 真实数据上，HMR 从 E.T. 的 0.033 降至 0.015，TCC 从 0.900 提升至 1.220（Table 5）。这些结果一致表明，适配预训练视频扩散模型的策略在视点规划任务上具有显著优势。

## 核心创新

AdaViewPlanner的核心创新在于**利用预训练文本到视频（T2V）扩散模型中已编码的电影摄影先验**，通过两阶段适配框架实现开放世界场景下可控的视点规划。与现有方法相比，该方法在三个关键维度上做出了根本性改变。

### 1. 4D场景条件的注入方式：从无场景感知到运动驱动的视频合成

现有方法如E.T.仅以文本和稀疏点轨迹为条件生成相机运动，缺乏对完整4D场景结构的感知；DanceCamera3D虽从音频和舞姿生成相机，但依赖特定骨骼格式且泛化受限。AdaViewPlanner则通过**姿态编码器（Pose Encoder）**将标准化的4D人体运动 $M \in \mathbb{R}^{f \times k \times 3}$（SMPL-X 22个关节的3D位置序列）编码为运动标记 $z_m$，并通过**空间运动注意力（Spatial Motion Attention）**将其注入预训练T2V模型的DiT框架中。具体而言，视频标记 $z_v^{(t)}$ 与运动标记沿空间维度拼接为 $T = [z_v^{(t)}; z_m] \in \mathbb{R}^{f' \times (h \cdot w + k) \times d}$，经自注意力计算后仅保留更新后的视频标记部分（公式1-2）。这一设计使模型仅需人体骨骼序列即可生成包含电影摄影风格相机运动的视频，**无需任何相机参数作为输入**，从而从根本上解决了现有方法对场景先验的依赖问题。

### 2. 相机轨迹生成范式：从端到端回归到视频中介的两阶段提取

DanceCamera3D采用端到端直接生成相机参数的方式，但受限于训练数据的覆盖范围，泛化能力不足。AdaViewPlanner创新性地提出了**两阶段范式**：Stage I利用注入运动条件的T2V模型生成隐含相机运动的视频；Stage II从生成的视频中提取对齐的绝对相机姿态。这一设计的核心洞察在于：预训练T2V模型内部已经编码了丰富的电影摄影技能（如推拉摇移、环绕跟拍等），通过生成视频作为中介，Stage II可以继承这些先验知识，而无需从零开始学习复杂的相机运动规律。

消融实验直接验证了这一范式的必要性：**若去除视频模型（w/o Video Model），直接基于文本和运动生成轨迹，训练要么无法收敛，要么崩溃至单一轨迹**（Figure 7），多样性严重受限。这表明相机轨迹生成与运动控制之间存在天然的任务分歧，预训练视频模型提供的电影摄影先验是解决这一分歧的关键桥梁。

### 3. 相机姿态提取的条件设计：从特征匹配后处理到运动条件直接估计

现有方法若从生成视频中提取相机，通常依赖MegaSaM或MonST3R等基于特征匹配的估计器，但这类方法对AI生成视频中的几何畸变极为敏感，且需要复杂的后处理对齐步骤（Figure 11）。AdaViewPlanner的Stage II则采用**MMDiT三支路框架**，分别处理视频、相机和人体运动三种模态，通过拼接查询/键/值实现多模态空间注意力（公式4），以流匹配目标直接在运动坐标系中预测绝对相机参数 $C \in \mathbb{R}^{f \times 9}$（3D平移 + 6D旋转）。

消融实验揭示了这一设计的因果机制：**去除Stage II的运动条件（w/o Motion）会导致相机轨迹视点错误**，重投影IoU从0.338降至0.226（Table 3），因为模型失去了骨骼参照，虽能生成平滑轨迹但无法对准目标人物（Figure 6）；**使用相对相机预测（Relative Cam）则面临尺度感知问题**，需要后处理对齐且精度下降。这证明同时以生成视频和原始人体运动为条件的直接估计，是保证相机姿态与4D场景坐标对齐的关键。

### 4. 引导学习机制：从直接生成到课程式训练

Stage I还引入了一个关键的训练策略——**引导学习方案（Guided Learning Scheme）**：以概率 $p$ 提供真值相机标记 $z_c$ 辅助训练（公式3），使模型在自主设计相机前先学会渲染符合给定运动的视频。这一课程式设计降低了训练复杂度，使得原本发散的任务（同时学习运动跟随和相机设计）能够稳定收敛。

## 整体框架

![[assets/figures/papers/paper_list_l2_AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in/figures/002_Figure_2.jpg]]
*Figure 2: (a) Stage I model for motion-conditioned cinematic video generation: a pose encoder processes human motion data (M) from 4D scenes and integrates it with video tokens via spatial motion attention to produce videos with cinematic camera movements. Camera parameters used for guidance are denoted as C. (b) Stage II model: three branches for video, camera, and human motion are combined in an MMDiT framework to extract camera pose*

AdaViewPlanner 采用**两阶段范式**，将预训练文本到视频（T2V）扩散模型适配为4D场景的视点规划器。其核心洞察在于：预训练T2V模型内部已编码丰富的电影摄影先验和场景知识，可通过注入4D场景表征（人体运动）来继承这些先验，从而在给定4D内容和文本指令时自动生成专业且多样的相机轨迹。

### 问题形式化

给定一段4D场景中的人体运动序列 $M \in \mathbb{R}^{f \times k \times 3}$（SMPL-X的 $k=22$ 个关节在 $f$ 帧内的3D位置）和一条描述场景上下文与期望相机运动的文本提示，方法输出对齐的相机轨迹 $C \in \mathbb{R}^{f \times 9}$（每帧的3D平移与6D旋转表示），同时生成一段可视化的电影视频。

### 两阶段流水线

**Stage I：运动条件电影视频生成。** 该阶段接收文本提示和4D人体运动序列 $M$，通过自适应学习分支将运动信息注入预训练T2V模型，生成一段包含隐含相机运动的视频。关键模块包括：

- **姿态编码器（Pose Encoder）**：将人体运动数据处理为运动标记 $z_m$。
- **空间运动注意力（Spatial Motion Attention）**：在DiT框架内，将视频标记 $z_v^{(t)}$ 与运动标记沿空间维度拼接为 $T = [z_v^{(t)}; z_m] \in \mathbb{R}^{f' \times (h \cdot w + k) \times d}$，计算自注意力后仅保留更新后的视频标记部分（公式1–2），实现运动条件注入而不改变预训练权重的核心结构。
- **引导学习方案（Guided Learning Scheme）**：以概率 $p$ 额外引入真值相机标记 $z_c$ 辅助训练（公式3），形成课程学习策略——模型先学会在给定相机下渲染符合运动的视频，再逐步过渡到自主设计相机运动，降低训练复杂度。

**Stage II：相机姿态提取。** 该阶段以Stage I生成的视频和原始人体运动 $M$ 为联合条件，通过MMDiT三支路框架直接估计绝对相机姿态序列。三支路分别处理视频、噪声相机标记和人体运动三种模态，通过多模态空间注意力将查询/键/值拼接（公式4），在运动坐标系中预测绝对相机参数，避免了传统特征匹配方法（如MegaSaM/MonST3R）对AI生成视频不稳定的问题。

### 设计动机

现有自动电影摄影方法面临两个瓶颈：专业模型依赖有限数据集训练，难以泛化到开放世界场景；手动设计相机轨迹繁琐且需专业知识。AdaViewPlanner通过**继承预训练视频模型中的电影摄影先验**来突破这一瓶颈——模型无需从零学习相机运动规律，而是在已有知识基础上适配4D场景条件。消融实验证实：若完全移除视频模型（直接基于文本和运动生成轨迹），训练将无法收敛或崩溃至单一轨迹（Figure 7），说明预训练视频先验对于解决该任务的多模态发散性至关重要。

## 核心模块与公式推导

AdaViewPlanner 采用两阶段范式，将预训练视频扩散模型中蕴含的电影摄影先验适配到4D场景的视点规划任务中。核心思路是：**Stage I** 将4D人体运动注入视频扩散模型，生成隐含相机运动的电影级视频；**Stage II** 从生成视频中直接提取与运动坐标系对齐的绝对相机姿态。

### 问题形式化

给定4D场景中的人体运动序列 $M \in \mathbb{R}^{f \times k \times 3}$（$f$ 帧，$k=22$ 个SMPL-X关节的3D位置）和描述场景上下文与相机运动的文本提示，目标是生成相机轨迹 $C \in \mathbb{R}^{f \times 9}$（每帧3D平移 $t_x,t_y,t_z$ 和6D旋转，即旋转矩阵前两行）。

### Stage I：运动条件电影视频生成

Stage I 的核心是将人体运动条件注入预训练文本到视频（T2V）扩散模型，使其生成既符合人体动作、又蕴含专业相机运动的视频。关键设计包括：

**空间运动注意力（Spatial Motion Attention）**：姿态编码器将人体运动 $M$ 编码为运动标记 $z_m$，与视频标记 $z_v^{(t)}$ 沿空间维度拼接：

$$T = [ z_v^{(t)} ; z_m ] \in \mathbb{R}^{f' \times (h \cdot w + k) \times d}$$

对拼接标记执行标准自注意力后，仅保留更新后的视频标记部分：

$$z_v^{(t)} = z_v^{(t)} + \mathrm{Truncate}(\mathrm{Attn}(q, k, v))$$

这种设计使运动条件通过注意力机制自然地融入视频生成过程，同时保持预训练T2V模型的视频生成能力不被破坏。

**引导学习方案（Guided Learning Scheme）**：以概率 $p$ 引入真值相机标记 $z_c$ 辅助训练，形成课程学习策略：

$$T = \begin{cases} [z_v^{(t)}; z_m; z_c] \in \mathbb{R}^{f' \times (h \cdot w + k + 1) \times d}, & \text{with prob. } p, \\ [z_v^{(t)}; z_m] \in \mathbb{R}^{f' \times (h \cdot w + k) \times d}, & \text{with prob. } 1-p. \end{cases}$$

该机制让模型先学会在给定相机条件下渲染符合人体运动的视频，再逐步过渡到自主设计相机运动，降低了训练难度。

### Stage II：相机姿态提取

Stage II 将相机姿态提取形式化为混合条件引导的外参去噪过程。采用 **MMDiT 三支路框架**，分别处理视频、相机和人体运动三种模态。在空间注意力层中，三种模态的查询、键、值沿空间维度拼接：

$$q = [ q_v ; q_m ; q_c^{(t)} ], \quad k = [ k_v ; k_m ; k_c^{(t)} ], \quad v = [ v_v ; v_m ; v_c^{(t)} ]$$

通过多模态交叉注意力，模型以Stage I生成的视频和原始人体运动为条件，对噪声相机标记进行流匹配去噪，直接在运动坐标系中预测绝对相机参数。与依赖特征匹配的后处理方法（如MegaSaM/MonST3R）不同，这种直接估计避免了AI生成视频不稳定导致的对齐失败问题。

**关键消融证据**：去除Stage II的运动条件（w/o Motion）会导致重投影IoU从0.338降至0.226，相机视点出现错误（Table 3, Figure 6）；仅预测相对相机姿态（Relative Cam）则面临尺度感知问题，需要后处理对齐。

## 实验与分析

### 核心瓶颈与因果机制

现有自动电影摄影方法的根本瓶颈在于：基于有限数据集训练的专业模型难以泛化到开放世界场景，且无法通过文本指令控制相机偏好。AdaViewPlanner 的核心因果杠杆是**利用预训练文本到视频（T2V）扩散模型中蕴含的电影摄影先验**——这些模型在训练过程中已内化了丰富的相机运动知识和场景理解能力。通过将标准化的4D人体运动 $M \in \mathbb{R}^{f \times k \times 3}$（$f$ 帧，$k=22$ 个关节的SMPL-X 3D位置序列）注入视频扩散模型，使模型在生成视频时继承这些先验，从而在给定4D内容和文本指令时自动生成专业且多样的相机轨迹 $C \in \mathbb{R}^{f \times 9}$（每帧3D平移+6D旋转）。

### 主实验结果

**Table 1** 展示了在E.T.测试集和自建测试集上的定量对比。AdaViewPlanner（Full）在所有基线上表现优越：

![[assets/figures/papers/paper_list_l2_AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on the E.T. testset and our curated testset. Metrics: HMR (Human Missing Rate), Jerkt/Jerkr (Camera Jerk of Translation/Rotation), Distt/Distr (Shot Diversity of Translation/Rotation), TCC (Text-Camera Consistency), CSD (Cinematographic Style Diversity). DanceCam* denotes our re-implementation of DanceCamera3D using our skeleton format*

- **人体缺失率（HMR）**：在E.T.测试集上达到0.044，相比E.T.的0.064降低31.3%；在自建测试集上达到0.018，相比E.T.的0.048降低62.5%。这表明生成的相机轨迹能更好地将人体保持在画面中。
- **文本-相机一致性（TCC）**：在E.T.测试集上达到1.125（E.T.为0.850，提升32.4%）；在自建测试集上达到1.385（E.T.为0.790，提升75.3%）。说明相机运动与文本指令高度对齐。
- **镜头多样性（Dist_t）**：在E.T.测试集上达到2.826，远超E.T.的0.478，证明相机在角色周围360°空间内具有显著更丰富的分布。
- **用户偏好率**：在E.T.测试集上为61.90%（E.T.为23.81%，DanceCam*为14.29%）；在自建测试集上为63.33%。用户研究邀请了12名计算机视觉领域研究人员参与评估。

**Table 5** 进一步验证了在真实世界运动数据（AMASS和GTA-Human）上的泛化能力。在AMASS上，HMR从E.T.的0.033降至0.015，Dist_t从0.422提升至1.437，TCC从0.900提升至1.220。在GTA-Human上同样保持显著优势。

![[assets/figures/papers/paper_list_l2_AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in/figures/012_Table_5.jpg]]
*Table 5: Quantitative results of viewpoint planning on the AMASS and GTA-Human test sets*

### 消融实验

**Table 3** 揭示了各设计选择的关键作用：

![[assets/figures/papers/paper_list_l2_AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in/figures/009_Table_3.jpg]]
*Table 3: Ablations on design choices for camera-trajectory generation. The Reproject Acc is computed by reprojecting 4D human poses and comparing against the human region mask in the original video. Variants: Stage I Subopt (early-training checkpoint of Stage I), Stage II w/o Motion (no motion conditioning in Stage II), and Stage II Relative Cam (Stage II predicts relative camera poses)*

- **去除Stage II的运动条件（w/o Motion）**：重投影IoU从0.338骤降至0.226。如Figure 6所示，缺乏骨骼参照时模型虽能生成平滑轨迹，但视点错位，无法对准人体。
- **使用Stage I次优检查点（Subopt）**：当Stage I生成的视频中人体运动对齐较差时，Stage II的相机提取精度下降（IoU 0.301 vs 0.338），证实两阶段间的级联依赖关系。
- **相对相机预测（Relative Cam）**：仅估计相对位姿需要后处理对齐，且存在尺度感知问题（Figure 6），重投影精度明显低于直接绝对位姿估计。

![[assets/figures/papers/paper_list_l2_AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in/figures/008_Figure_6.jpg]]
*Figure 6: Columns 1–4 show the reprojection of 4D human skeletons by using estimated camera parameters, while Column 5 presents the rendered results in 3D space. w/o Motion exhibits viewpoint errors, whereas Relative Cam suffers from scale perception issues*

**Table 12** 验证了空间运动注意力（Spatial Motion Attention）的优越性。用CrossDiT风格或3D Motion Attention替代会导致WA-MPJPE从71.65急剧上升至127.02/131.88，表明沿空间维度拼接运动标记与视频标记进行联合自注意力是有效的条件注入方式。

**Figure 7** 的训练损失曲线揭示了视频模型的必要性：不使用视频模型（直接基于文本和运动生成轨迹）时，训练要么无法收敛，要么崩溃至单一轨迹。这印证了任务本身的发散性——仅靠文本和运动条件难以解决相机轨迹的高度不确定性，预训练视频模型提供的电影摄影先验起到了关键的引导作用。

![[assets/figures/papers/paper_list_l2_AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in/figures/010_Figure_7.jpg]]
*Figure 7: Comparison of training loss curves: Ours, DanceCam* and Ours w/o Video Model*

### 引导学习方案的消融

引导学习方案（Guided Learning Scheme）以概率 $p$ 在训练时提供真值相机标记 $z_c$：

$$T = \begin{cases} [z_v^{(t)}; z_m; z_c] \in \mathbb{R}^{f' \times (h \cdot w + k + 1) \times d}, & \text{with prob. } p, \\ [z_v^{(t)}; z_m] \in \mathbb{R}^{f' \times (h \cdot w + k) \times d}, & \text{with prob. } 1-p. \end{cases}$$

这一课程学习策略帮助模型先学会渲染符合给定运动的视频，再逐步过渡到自主设计相机。Table 3中Full模型的重投影精度（IoU 0.338）印证了该设计的有效性。

### 失败模式

**Figure 9** 展示了两类典型失败案例：(a) 生成视频中的几何畸变，表现为人体形状扭曲或背景不连贯；(b) 复杂动作下的运动不一致，如快速旋转或肢体交叉时视频帧间的人体姿态出现跳变。这些失败源于预训练T2V模型本身的生成限制，会进一步影响Stage II的相机提取精度。

### MLLM评估的可靠性

TCC和CSD指标使用Gemini 2.5 Pro进行评估（Figure 10, Table 6, Table 7），10次重复测试显示TCC标准差为0.082、CSD标准差为0.013，保证了评估一致性。Table 1中MLLM指标与规则指标（HMR等）和用户偏好率的方向一致，验证了自动化评估的可靠性。

### 推理效率

**Table 8** 报告了在单张NVIDIA A800 GPU上的推理效率。默认50步设置下，Stage I耗时31.60秒、Stage II耗时16.20秒，总计约47.8秒。减少步数至10步可将总时间压缩至约10秒，但**Table 9**显示这会带来一定的性能下降——50+50步配置在重投影IoU（0.338）和HMR（0.018）上均为最优。

### 开源模型兼容性

**Table 10** 和 **Table 11** 展示了在开源Wan-2.2-5B模型上训练的版本同样取得显著效果，在自建测试集上HMR达到0.022、TCC达到1.265，验证了方法的模型无关性。

## 方法谱系与知识库定位

### 与基线方法的关系

AdaViewPlanner 的核心定位是**利用预训练视频扩散模型中的电影摄影先验，替代现有方法对专业数据集或手工规则的依赖**。与之直接对比的两类基线代表了两种不同的技术路线：

**E.T.（文本+角色轨迹驱动）**：该方法以文本和角色点轨迹为条件直接生成相机运动。其瓶颈在于仅依赖有限数据集训练的专业模型，难以泛化到开放世界场景，且无法充分利用文本指令中的偏好控制（如“环绕拍摄”“低角度仰拍”）。实验显示，E.T. 在 AMASS 真实数据上的镜头多样性（Dist_t）仅为 0.422，而 AdaViewPlanner 达到 1.437（Table 5），差距超过 1.0，说明前者生成的相机轨迹严重局限于狭窄的运动空间。

**DanceCamera3D（音频+舞姿驱动，重新实现为 DanceCam\*）**：该方法原为音频到相机运动的端到端生成，适配后改为文本+骨骼序列输入。其根本局限在于端到端范式缺乏对场景视觉内容的显式建模，导致轨迹的文本一致性和专业性不足。用户研究中 DanceCam\* 的偏好率仅为 14.29%，远低于 AdaViewPlanner 的 61.90%（Table 1）。

AdaViewPlanner 对上述基线的替代关系体现在三个关键设计变化上：

1. **4D 场景条件注入方式**：从“无需 4D 信息”或“依赖特定骨骼格式”变为通过姿态编码器和空间运动注意力（Spatial Motion Attention）将标准归一化的 4D 人体运动 $M \in \mathbb{R}^{f \times k \times 3}$ 注入视频扩散模型。消融实验证实，用 CrossDiT 或 3D Motion Attention 替代该机制会导致 WA-MPJPE 从 71.65 飙升至 127.02/131.88（Table 12），说明该注入方式是运动控制质量的关键。

2. **相机轨迹生成范式**：从“端到端生成相机参数”变为两阶段范式——Stage I 生成隐含相机运动的视频，Stage II 从中提取绝对相机姿态。这一设计利用视频作为中间表征，既继承了预训练模型中的电影摄影先验，又避免了直接生成相机参数时的多义性。

3. **相机姿态提取条件**：从“基于特征匹配的估计（如 MegaSaM/MonST3R）”变为直接训练条件去噪模型，以生成视频和人体运动为条件预测绝对相机参数。去除 Stage II 的运动条件（w/o Motion）会导致重投影 IoU 从 0.338 降至 0.226（Table 3），且出现视点错误（Figure 6）；而仅估计相对姿态（Relative Cam）则存在尺度感知问题。

### 适用边界

**有效范围**：

- **输入条件**：4D 人体运动序列（SMPL-X 格式，22 个关节的 3D 位置）配合描述场景上下文和期望相机运动的文本提示。
- **场景类型**：以移动人类为中心的 4D 场景。在舞蹈领域（TikTok 测试集）和通用领域（自建测试集）均验证有效，且在 AMASS 和 GTA-Human 真实数据上保持性能优势（Table 4, Table 5）。
- **输出能力**：生成与人体运动坐标系对齐的绝对相机姿态序列 $C \in \mathbb{R}^{f \times 9}$（3D 平移 + 6D 旋转），同时提供对应的电影视频可视化。

**已知失效边界**：

1. **非人体动态对象**：当前方法仅考虑 4D 场景中移动的人类，尚未扩展到一般 4D 场景或非人形动态实体（论文明确指出的局限）。
2. **复杂动作下的视频生成**：Stage I 生成的视频在复杂动作下存在运动不一致，部分场景出现几何畸变（Figure 9）。这直接限制了 Stage II 的相机提取精度——使用 Stage I 次优检查点（人体运动对齐差）会导致 Stage II 重投影 IoU 从 0.338 降至 0.301（Table 3）。
3. **基础模型偏见**：方法依赖预训练 T2V 模型的内部相机知识。若基础模型本身缺乏某种运动类型的电影摄影先验或带有偏见，生成效果会受影响。使用开源 Wan-2.2-5B 替代内部模型时，性能有所下降但仍保持竞争力（Table 10, Table 11），说明框架对基础模型有一定鲁棒性。
4. **极端复杂场景**：相机轨迹多样性虽明显提升，但在部分极端复杂场景下仍可能与专业导演设计存在差距。

### 核心局限与开放问题

**结构层面的局限**：

两阶段范式的根本矛盾在于 **Stage I（运动控制）与 Stage II（相机估计）的训练目标冲突**。具体表现为三个方面：（1）运动控制偏好较大的去噪时间步以保持人体结构，而相机估计偏好较小时步以利用像素级运动线索；（2）Stage I 生成的视频存在噪声，会削弱 Stage II 可用的像素运动信号；（3）统一训练需要同时标注骨骼和相机参数的真实视频数据集，目前此类数据极度稀缺。这一冲突的直接证据是：去除视频模型直接基于文本和运动生成轨迹时，训练要么无法收敛，要么崩溃至单一轨迹（Figure 7 损失曲线），说明任务本身的发散性需要预训练视频模型提供额外引导。

**评估层面的局限**：

用户研究邀请了 12 名计算机视觉领域的研究人员参与，样本量较小且参与者具有领域专业知识，可能无法完全代表普通用户或专业电影摄影师的偏好。MLLM 评估使用 Gemini 2.5 Pro 进行 10 次重复以验证稳定性（TCC SD=0.082, CSD SD=0.013），但自动化评估与人类判断的一致性仍需进一步验证。

**开放问题**：

1. **范式统一**：如何将 Stage I 和 II 统一为单阶段模型，同时解决运动控制与相机估计的采样冲突？可能的路径包括设计共享表征空间或引入解耦训练策略。
2. **场景泛化**：能否将这套框架推广到包含非人体动态对象（如车辆、动物）的更一般 4D 场景？这需要重新设计运动表征和条件注入机制。
3. **数据瓶颈**：真实视频的相机参数自动标注仍是瓶颈。未来能否结合弱监督或自监督方法提升真实数据的可用性，从而减少对合成数据的依赖？
4. **模型升级**：随着更强大的开源视频生成模型（如 Wan-2.2-5B 已初步验证，Table 10/11）的出现，如何系统性地利用它们进一步提升轨迹质量与泛化性？
5. **简化提取**：当前从生成视频中提取相机的方法是否还可以进一步简化，例如直接联合预测相机参数和视频，而非分两阶段处理？

## 原文 PDF

![[paperPDFs/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.pdf]]

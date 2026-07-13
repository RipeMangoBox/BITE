---
title: "DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/DriveSuprim_Towards_Precise_Trajectory_Selection_for_End_to_End_Planning.pdf
project_link: null
code_link: https://github.com/William-Yao-2000/DriveSuprim
aliases:
- DriveSuprim
tags:
- AAAI_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过粗到细的候选过滤与精细评分、基于旋转的视角增强以平衡轨迹分布、以及自蒸馏框架提供软标签，提升轨迹选择的精度和鲁棒性。"
primary_logic: "在大量候选轨迹中，仅靠单次评分很难区分安全关键但差异细微的轨迹；通过逐步缩小候选空间并对困难样本进行精细化评分，结合合成转弯场景和软标签，可以显著提高对最优轨迹的辨识力。"
claims:
- "在NAVSIM v1基准上，DriveSuprim使用ViT-L骨干达到93.5% PDMS，超过此前最优方法Hydra-MDP 89.9%达3.6个百分点。"
- "在NAVSIM v2基准上，DriveSuprim使用ViT-L达到87.1% EPDMS，超过HydraMDP++ 85.6%共1.5个百分点。"
- "粗到细选择策略带来的增益（0.7%）远超单纯增加解码器层数（0.3%），证实了候选过滤的有效性。"
- "自蒸馏软标签显著优于传统平滑方法，EPDMS达到83.1，而标签平滑和温度缩放仅分别为82.5和82.7。"
---

# DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning

> [!tip] 核心洞察
> 在大量候选轨迹中，仅靠单次评分很难区分安全关键但差异细微的轨迹；通过逐步缩小候选空间并对困难样本进行精细化评分，结合合成转弯场景和软标签，可以显著提高对最优轨迹的辨识力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DriveSuprim：面向端到端规划的精确轨迹选择 |
| 英文题名 | DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning |
| 会议/期刊 | AAAI 2026 |
| Links | [paper](https://arxiv.org/abs/2506.06659) · [GitHub](https://github.com/William-Yao-2000/DriveSuprim) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | DriveSuprim |
| Dataset | NAVSIM v1, NAVSIM v2, Bench2Drive |

> [!tip] 效果简介
> - NAVSIM v1 上，PDMS 为 93.5，对比 89.9 (Hydra-MDP, ViT-L)，变化 +3.6。
> - NAVSIM v2 上，EPDMS 为 87.1，对比 85.6 (HydraMDP++, ViT-L)，变化 +1.5。
> - Bench2Drive 上，Driving Score 为 83.02，对比 78.84 (AutoVLA)，变化 +4.18。

## 概要

现有选择式端到端规划方法面临三个核心瓶颈：**硬负样本难以区分**——在数千条候选轨迹中，单次全局评分无法可靠辨识与真值轨迹几何相似但安全性差异细微的子最优轨迹；**转弯场景方向性偏差**——训练数据中直行样本占主导，导致模型在转弯场景下性能显著退化；**硬二元决策边界**——传统二元交叉熵损失使训练不稳定，对困难样本缺乏有效的梯度信号。

针对上述问题，DriveSuprim 提出三条因果链路：① **粗到细的候选过滤与精细评分**，通过轨迹解码器进行粗筛选，再由精化解码器对 Top-K 候选进行多层精细评分，逐步缩小决策空间，提升对硬负样本的辨识力；② **基于旋转的伪全景视角增强**，通过水平平移与裁剪模拟自车转弯场景，平衡轨迹分布，缓解方向性偏差；③ **教师自蒸馏软标签框架**，以学生模型的指数移动平均作为教师，生成限幅软标签，替代硬二元监督，使训练更稳定。

在 NAVSIM v1 基准上，DriveSuprim 使用 ViT-L 骨干达到 **93.5% PDMS**，超过此前最优方法 Hydra-MDP 的 89.9% 达 3.6 个百分点（Table 2）；在 NAVSIM v2 上达到 **87.1% EPDMS**，超过 HydraMDP++ 的 85.6% 共 1.5 个百分点（Table 3）；在 Bench2Drive 闭环评测中取得 **83.02 Driving Score**，领先 AutoVLA 4.18 分（Table 4）。消融实验证实，粗到细选择策略带来的增益（+0.7%）远超单纯增加解码器层数（+0.3%）（Table 6），自蒸馏软标签（EPDMS 83.1）显著优于标签平滑（82.5）和温度缩放（82.7）（Table 13）。所有对比均使用相同骨干网络与训练数据，未引入额外数据。



端到端自动驾驶的目标是直接从传感器输入（图像、激光雷达等）映射到自车的未来行驶轨迹，即 $T = \mathrm{Planner}(Img, Lidar)$。在这一范式下，**选择式规划方法**（selection-based planning）因其可解释性和可控性而受到广泛关注：模型从预定义的轨迹词汇库（trajectory vocabulary）中为每条候选轨迹预测安全评分，最终选择得分最高的轨迹作为规划输出。

然而，选择式规划面临一个核心瓶颈：**在数千条候选轨迹中精确区分子最优的“硬负样本”极其困难**。这些硬负样本与最优轨迹在几何形态上高度相似，仅在安全关键指标（如碰撞时间、偏离车道距离）上存在细微差异，单次全局评分难以有效辨识。Oracle实验（Table 1）表明，即使预测评分排序后的Top-K候选轨迹中已包含高质量轨迹，现有方法仍无法稳定地将其选出，说明**评分精度而非候选覆盖度**是当前性能的限制因素。

此外，现有选择式规划方法还存在两个结构性缺陷：

- **方向性偏差（directional bias）**：训练数据中直行场景占据主导，转弯轨迹严重不足，导致模型在转弯场景下性能显著退化。这种分布不均使模型倾向于选择直行或微调方向的轨迹，而在需要大幅度转向时表现保守甚至危险。
- **硬二元决策边界**：传统训练使用硬标签（0/1）对候选轨迹进行二元分类，但轨迹优劣本质上是一个连续谱——一条轨迹可能并非完全错误，只是略逊于最优选择。硬边界使训练信号过于严苛，导致优化不稳定，且无法捕捉轨迹间的相对优劣关系。

针对上述问题，**DriveSuprim** 提出了三条互补的技术路径：通过**粗到细的候选过滤与精细评分**逐步缩小搜索空间并对困难样本进行深度判别；通过**基于旋转的视角增强**合成转弯场景以平衡轨迹分布；通过**自蒸馏框架**引入软标签，将硬二元决策软化，提供更平滑、更稳定的训练信号。这些设计共同指向一个目标：**在大量候选轨迹中，精确、鲁棒地辨识出真正安全且符合驾驶意图的最优轨迹**。



## 核心方法与创新机理

DriveSuprim 的核心创新并非引入全新的模型架构，而是针对现有选择式端到端规划方法中三个被忽视却至关重要的瓶颈，提出了系统性的解决方案。这些瓶颈包括：(1) 在数千条候选轨迹中难以精确区分子最优的“硬负样本”；(2) 训练数据中转弯场景严重不足导致的方向性偏差；(3) 硬二元决策边界造成的训练不稳定。围绕这三个瓶颈，DriveSuprim 在候选轨迹选择策略、数据增强方式和训练优化目标三个维度上进行了关键改进。

### 粗到细两阶段轨迹选择

传统选择式方法（如 Hydra-MDP）采用单阶段全局评分，一次性从全部候选轨迹中选出最优解。然而，当候选轨迹数量庞大且彼此差异细微时，单次评分难以有效区分安全关键但视觉上极为相似的“硬负样本”。DriveSuprim 将这一过程重构为**粗过滤（Coarse Filtering）**与**精细评分（Fine-grained Scoring）**两个阶段：

- **粗过滤阶段**：Trajectory Decoder 利用图像特征对所有候选轨迹进行交叉注意力编码，通过多个预测头输出各安全指标的粗评分 $s_j^{(m)} = \mathrm{Sigmoid}(\mathrm{head}^{(m)}(g_j))$，并根据综合评分筛选出 Top-K 条有潜力的候选轨迹。
- **精细评分阶段**：Refinement Decoder 对过滤后的 Top-K 候选进行多层递进式评分，逐层输出精细化分数 $s_{j,l}^{(m)}$，使模型能够聚焦于最困难的候选轨迹，逐步提升判别精度。

消融实验（Table 6）清晰地揭示了这一策略的价值：从单阶段基线出发，仅增加解码器层数仅带来 0.3% 的 EPDMS 提升，而引入轨迹过滤机制后增益跳升至 0.7%，证实了**逐步缩小候选空间**比单纯堆叠模型容量更为有效。最佳设置（Table 10）为 3 层 Refinement Decoder 配合 Top-K=256。

### 基于旋转的视角增强

选择式规划方法在转弯场景中表现不佳的根源在于数据分布失衡——训练数据中直行场景占据主导，导致模型产生方向性偏差。DriveSuprim 提出了一种**基于旋转的伪全景视角增强方法**（Figure 3）：通过对多相机图像进行水平平移和裁剪，合成自车处于转弯状态下的视角输入。这一方法无需额外采集数据，即可显著提升训练集中转弯轨迹的出现频率（Figure 7），使模型在左转、右转等分布外场景中获得更均衡的监督信号。Table 7 的转弯场景拆分评估直接验证了该增强对方向性偏差的缓解效果。

### 自蒸馏软标签训练框架

传统选择式方法使用硬二元标签（最优轨迹为 1，其余为 0）进行训练，这种刚性决策边界在候选轨迹质量相近时会导致训练不稳定。DriveSuprim 引入**教师-学生自蒸馏框架**生成软标签：

- 教师模型由学生模型的指数移动平均（EMA）构建，其输出 $s_{i,\mathrm{teacher}}^{(m)}$ 经限幅后与真值结合，形成软标签 $\hat{y}_i^{(m)} = y_i^{(m)} + \mathrm{clip}(s_{i,\mathrm{teacher}}^{(m)} - y_i^{(m)}, -\delta_m, \delta_m)$。
- 学生模型的总损失 $\mathcal{L} = \mathcal{L}_{\mathrm{ori}} + \mathcal{L}_{\mathrm{aug}} + \mathcal{L}_{\mathrm{soft}}$ 同时接收原始数据、增强数据和软标签的监督，使训练过程更加平滑稳定。

Table 13 的对比实验表明，自蒸馏软标签（EPDMS 83.1）显著优于传统的标签平滑（82.5）和温度缩放（82.7），证实了教师模型提供的结构化软信号比简单的分布平滑更具信息量。

### 创新协同效应

上述三项创新并非孤立生效，而是形成协同增益。Table 5 的逐步消融显示：引入多阶段选择后 EPDMS 从基线 81.4 提升至 82.4，加入旋转数据增强后升至 82.7，叠加自蒸馏后达到 83.1。三者叠加带来的总增益（+1.7%）大于各模块独立增益之和，表明粗到细选择为增强数据和软标签提供了更精准的优化空间，而软标签又反过来稳定了多阶段训练的收敛过程。



![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/002_Figure_1.jpg]]
*Figure 1: Overall pipeline of our method. Selection-based methods struggle to distinguish suboptimal trajectories, perform poorly in turning, and utilize hard binary labels in training. DriveSuprim introduces coarse-to-fine refinement and a rotation-based data augmentation method with self-distillation to address these weaknesses. The green trajectory is the ground-truth trajectory, and the red and orange trajectories are obviously unsafe and seemingly correct trajectory candidates in the trajectory vocabulary*

DriveSuprim 的整体流水线围绕三个核心瓶颈展开：选择式端到端规划方法难以在数千条候选轨迹中精确区分子最优的“硬负样本”，训练数据中转弯场景严重不足导致方向性偏差，以及硬二元决策边界使训练不稳定。为解决这些问题，方法在统一的端到端框架中集成了**粗到细轨迹选择**、**基于旋转的数据增强**和**自蒸馏软标签训练**三个关键模块，其整体架构如 Figure 2 所示。

### 输入与特征提取

系统接收多相机图像作为输入，通过图像编码器 $Enc_i$ 提取视觉特征 $\mathcal{E}_{img}$。同时，预定义的轨迹词汇表中的每条候选轨迹 $\tau_j$ 经轨迹编码器 $Enc_t$ 编码为轨迹特征 $f_j$。这一双流编码构成了后续评分与选择的基础。

### 粗到细轨迹选择范式

轨迹选择采用两阶段级联结构，逐步缩小候选空间并对困难样本进行精细化评分：

1. **粗过滤阶段 (Coarse Filtering)**：轨迹解码器 $TransDec$ 利用图像特征对全部 $N$ 条候选轨迹进行交叉注意力，输出每条轨迹在多个安全指标上的粗评分 $s_j^{(m)}$。根据评分排序，系统筛选出 Top-K 条最有潜力的候选轨迹 $T_{filter}$，大幅压缩后续精细评分的搜索空间。

2. **精细评分阶段 (Fine-grained Scoring)**：精化解码器 $RefineDec$ 仅对过滤后的 Top-K 条轨迹进行多层深度评分，逐层输出更精确的指标分数 $s_{j,l}^{(m)}$。这种“先过滤、再精评”的策略使模型能够将计算资源集中于区分安全关键但差异细微的硬负样本。

最终，系统根据精细评分选择最优轨迹作为规划输出。推理时，教师模型（学生模型的指数移动平均）被用于生成最终的规划轨迹。

### 数据增强与训练策略

为解决转弯场景的方向性偏差，DriveSuprim 引入基于旋转的数据增强方法：通过对伪全景视图进行水平平移和裁剪，合成自车转弯视角的增强样本（Figure 3），显著提升了训练数据中转弯轨迹的分布频率。

在训练优化方面，自蒸馏框架以教师模型生成的软标签替代传统的硬二元分类目标。教师模型的输出经限幅后与真值结合，构成软标签 $\hat{y}_i^{(m)}$，为学生模型提供更平滑、更稳定的训练信号。学生模型的总训练损失由三部分组成：

$$\mathcal{L} = \mathcal{L}_{ori} + \mathcal{L}_{aug} + \mathcal{L}_{soft}$$

其中 $\mathcal{L}_{ori}$ 为原始数据上的模仿损失与二元交叉熵，$\mathcal{L}_{aug}$ 为增强数据上的对应损失，$\mathcal{L}_{soft}$ 为软标签监督损失。这一联合训练框架有效缓解了硬决策边界导致的训练不稳定问题。

### 模块间协同关系

三个核心模块并非孤立运作，而是形成互补闭环：粗到细选择解决了候选轨迹中硬负样本的区分难题，旋转增强弥补了转弯场景的数据缺口，自蒸馏软标签则为整个选择过程提供了更平滑的优化目标。消融实验（Table 5）证实，各模块叠加使用带来持续的性能提升，最终在 NAVSIM v1 和 v2 基准上分别达到 93.5% PDMS 和 87.1% EPDMS 的最优性能。



DriveSuprim 的核心架构围绕三个紧密协作的模块展开：**粗到细轨迹选择**（Coarse-to-Fine Trajectory Selection）、**基于旋转的数据增强**（Rotation-based Data Augmentation）以及**自蒸馏软标签训练**（Self-distillation with Soft-labeling）。三者分别针对选择式端到端规划中“硬负样本难以区分”、“转弯场景方向性偏差”和“硬二元决策边界导致训练不稳定”三个关键瓶颈。

### 粗到细轨迹选择

该模块将传统的单阶段全局评分替换为两阶段级联结构，由轨迹粗过滤和精细化评分组成。

**轨迹粗过滤**：给定图像输入 $I$ 和预定义的轨迹词汇表 $\{\tau_j\}_{j=1}^N$，图像编码器 $\mathrm{Enc}_i$ 和轨迹编码器 $\mathrm{Enc}_t$ 分别提取视觉特征与轨迹特征：

$$\mathcal{E}_{\mathrm{img}} = \mathrm{Enc}_i(I), \quad f_j = \mathrm{Enc}_t(\tau_j)$$

轨迹解码器 $\mathrm{TransDec}$ 利用交叉注意力将图像特征注入轨迹特征：

$$g_j = \mathrm{TransDec}(\mathcal{E}_{\mathrm{img}}, f_j)$$

随后，多个预测头 $\mathrm{head}^{(m)}$ 对每条轨迹在安全指标 $m$（如碰撞、偏离车道等）上输出粗评分：

$$s_j^{(m)} = \mathrm{Sigmoid}(\mathrm{head}^{(m)}(g_j))$$

基于综合评分排序，模型筛选出 Top-$K$ 条候选轨迹进入精细化阶段。

**精细化评分**：精化解码器 $\mathrm{RefineDec}$ 对筛选后的候选轨迹进行多层迭代评分。第 $l$ 层输出的指标 $m$ 分数为：

$$s_{j,l}^{(m)} = \mathrm{Sigmoid}(\mathrm{head}^{(m)}(h_{j,l}))$$

其中 $h_{j,l}$ 为精化解码器第 $l$ 层的隐状态。粗阶段损失由模仿损失与二元交叉熵组成：

$$\mathcal{L}_{\mathrm{coarse}} = \mathcal{L}_{\mathrm{imi}} + \sum_{m,i} \mathrm{BCE}(s_i^{(m)}, y_i^{(m)})$$

消融实验表明，从单阶段到粗到细的演变中，轨迹过滤带来的增益（+0.7% EPDMS）远超单纯增加解码器层数（+0.3%），证实了逐步缩小候选空间对区分硬负样本的有效性（Table 6）。最优精细评分设置为 3 层精化解码器配合 Top-$K=256$（Table 10）。

### 基于旋转的数据增强

针对训练数据中转弯场景严重不足导致的方向性偏差，DriveSuprim 提出一种基于旋转的伪全景视角增强方法。该方法通过对多相机图像进行水平平移和裁剪，模拟自车转弯时的视角变化，合成出原本稀缺的转弯场景样本（Figure 3）。增强后的数据集显著提高了转弯轨迹的出现频率，使模型在左转（NAVTESTl）、近直行（NAVTESTf）和右转（NAVTESTr）三个子集上的 EPDMS 均获得提升（Table 7）。

### 自蒸馏软标签训练

为缓解硬二元标签带来的训练不稳定问题，DriveSuprim 引入教师-学生自蒸馏框架。教师模型为学生模型的指数移动平均（EMA），其输出的评分经限幅后与真值标签融合，生成软标签：

$$\hat{y}_i^{(m)} = y_i^{(m)} + \mathrm{clip}(s_{i,\mathrm{teacher}}^{(m)} - y_i^{(m)}, -\delta_m, \delta_m)$$

其中 $\delta_m$ 为指标 $m$ 的限幅阈值，控制软标签偏离真值的程度。学生模型的总训练损失由原始数据损失、增强数据损失和软标签损失三部分构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{ori}} + \mathcal{L}_{\mathrm{aug}} + \mathcal{L}_{\mathrm{soft}}$$

推理阶段仅使用教师模型输出规划轨迹。自蒸馏软标签在 EPDMS 上达到 83.1，显著优于标签平滑（82.5）和温度缩放（82.7），验证了教师模型提供的结构化软监督信号比传统平滑方法更有效（Table 13）。



## 实验与关键发现

### 主要结果

DriveSuprim 在三个主流基准上均取得最优性能，且在不同视觉骨干下表现出一致的领先优势。

在 **NAVSIM v1**（开环规划）上，DriveSuprim 以 ViT-L 骨干达到 **93.5% PDMS**，超过此前最优方法 **Hydra-MDP**（Li et al., arXiv 2024）的 89.9%，提升幅度达 **3.6 个百分点**（Table 2）。在轻量级 ResNet34 骨干下，DriveSuprim 也达到 89.9% PDMS，领先 **DiffusionDrive**（Liao et al., CVPR 2025）1.8 个百分点。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/005_Table_2.jpg]]
*Table 2: Evaluation on NAVSIM v1. Results are grouped by backbone types. Table 3: Evaluation on NAVSIM v2. Results are grouped by backbone types*

在 **NAVSIM v2**（更严格的开环评估）上，DriveSuprim 以 ViT-L 达到 **87.1% EPDMS**，超过 **HydraMDP++** 的 85.6%，提升 **1.5 个百分点**（Table 3）。ResNet34 骨干下同样领先 HydraMDP++ 1.7 个百分点（83.1 vs 81.4）。

在 **Bench2Drive**（闭环驾驶）上，DriveSuprim 取得 **83.02 Driving Score** 和 **60.00 Success Rate**，相比此前最优的 **AutoVLA**（Zhou et al., arXiv 2025）在 Driving Score 上提升 **4.18 分**（Table 4）。值得注意的是，DriveSuprim 在 Bench2Drive 上采用两阶段轨迹预测进行纵向控制，所有方法均使用相同数据集训练，未引入额外数据。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/006_Table_4.jpg]]
*Table 4: Evaluation on Bench2Drive*

### 消融实验

#### 各模块贡献（Table 5）

以 ResNet34 骨干在 NAVSIM v2 上的 EPDMS 为指标，逐步加入各模块的增益如下：


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/007_Table_5.jpg]]
*Table 5: Ablation study on different proposed modules. “Multi-stage” denotes using coarse-to-fine selection, “Aug Data” denotes introducing rotation-based augmentation data, and “Self-distill” denotes adopting self-distillation*

- **基线（单阶段选择）**：81.4
- **+ 多阶段粗到细选择**：82.4（+1.0）
- **+ 旋转数据增强**：82.7（+0.3）
- **+ 自蒸馏软标签**：83.1（+0.4）

三个模块均带来正向增益，其中粗到细选择策略贡献最大，验证了精细评分对区分硬负样本的关键作用。

#### 单阶段到粗到细的演变（Table 6）

进一步拆解选择策略的演变路径，揭示了一个重要洞察：


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/008_Table_6.jpg]]
*Table 6: Ablation study of the evolution from single-stage selection to coarse-to-fine selection*

- 单阶段 + 1 层 Decoder → + 6 层 Decoder：EPDMS 从 81.4 提升至 81.7（**+0.3%**）
- 6 层 Decoder + 层间评分（layer-wise scoring）：81.9（+0.2%）
- 6 层 Decoder + 层间评分 + 轨迹过滤（即粗到细选择）：**82.4（+0.7%）**

单纯增加解码器层数带来的增益（0.3%）远小于引入轨迹过滤机制的增益（0.7%）。这证实了核心洞察：在数千条候选轨迹中，仅靠单次评分难以区分安全关键但差异细微的轨迹，逐步缩小候选空间并对困难样本进行精细化评分是提升辨识力的关键。

#### 精化设置消融（Table 10）

最优精细评分配置为：**Refinement Decoder 3 层，Top-K = 256**。该设置在计算开销与性能间取得最佳平衡。将过滤策略扩展到更多阶段未能带来额外提升，表明当前的两阶段设计已接近该框架的收益上限。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/015_Table_10.jpg]]
*Table 10: Ablation on refinement setting. “Stage Layer” is the layer number of the Refinement Decoder, and “Top-K” denotes the number of trajectories selected by the coarse filtering stage. Table 11: Results with different soft label thresholds. $\delta _ { m }$ denotes the soft label threshold in the Equation 9*

#### 自蒸馏与平滑方法对比（Table 13）

自蒸馏软标签（EPDMS 83.1）显著优于传统平滑方法：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/014_Table_13.jpg]]
*Table 13: Comparison of different smoothing methods. Table 14: Comparison of parameter and inference speed*

- 标签平滑（Label Smoothing）：82.5
- 温度缩放（Temperature Scaling）：82.7
- 自蒸馏：**83.1**

这表明教师模型提供的结构化软标签比简单的标签软化包含更丰富的轨迹质量信息，能更有效地稳定训练过程。

#### 转弯场景分析（Table 7）

在按转弯方向划分的数据子集上，DriveSuprim 在左转（NAVTESTl）、近直行（NAVTESTf）和右转（NAVTESTr）场景中均取得领先，验证了旋转数据增强对缓解方向性偏差的有效性。Figure 7 进一步显示，增强后数据集中转弯轨迹的出现频率显著提升，原本严重不足的转弯样本分布得到有效均衡。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/009_Table_7.jpg]]
*Table 7: EPDMS on three dataset splits. NAVTESTl, NAVTESTf, and NAVTESTr involve left-turning scenarios, near-forward scenarios, and right-turning scenarios*

### 失败模式与局限性

尽管 DriveSuprim 在整体指标上表现优异，论文明确指出将过滤策略扩展到更多阶段未能带来额外提升，模型在极端或边缘场景下仍有提升空间。这暗示当前的两阶段粗到细框架可能已触及该范式的性能瓶颈，更复杂的多阶段细化策略需要更根本性的设计突破。

### 推理效率（Table 14）

在参数量和推理速度的对比中，DriveSuprim 在保持领先精度的同时，未显著增加推理开销，具备实际部署的可行性。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2506_06659/figures/001_Table_1.jpg]]
*Table 1: PDM score of the best trajectory in the top-K candidates on ranked predicted scores*


*Table 8: The inference coefficients on each metric of NAVSIM v1. “Imi” denotes the imitation metric, “Mul” denotes the multiplied penalties, an$d ^ { \mathrm { \bullet } } \mathrm { A v g } ^ { \mathrm { \bullet } }$ denotes the weighted averages. Table 9: The inference coefficients on each metric of NAVSIM v2. “Imi” denotes the imitation metric, “Mul” denotes the multiplied penalties, and “Avg” denotes the weighted averages





## 定位与知识库关联

### 选择式端到端规划的方法脉络

DriveSuprim 处于**选择式端到端规划**（selection-based end-to-end planning）这一技术路线中。该路线将规划问题建模为从预定义的候选轨迹集合中选出最优轨迹，与直接回归轨迹的生成式方法形成互补。在这一谱系中，DriveSuprim 的直接前驱和对比对象包括：

- **Hydra-MDP** (Li et al., arXiv 2024)：多教师蒸馏的选择式规划方法，采用单阶段全局评分从候选轨迹中选出最优解。DriveSuprim 在 NAVSIM v1 上以 93.5% PDMS 超越其 89.9%，核心差异在于粗到细的候选过滤与精细评分机制。
- **HydraMDP++**：Hydra-MDP 的增强版本，在 NAVSIM v2 上达到 85.6% EPDMS，被 DriveSuprim 以 87.1% 超越（+1.5 个百分点）。
- **DiffusionDrive** (Liao et al., CVPR 2025)：采用截断扩散模型生成轨迹，代表生成式路线。在 NAVSIM v1 上使用 ResNet34 骨干时，DriveSuprim 以 89.9% PDMS 超越其 88.1%。
- **Transfuser** (Chitta et al., TPAMI 2023)：基于 Transformer 的传感器融合模仿学习基线，代表早期端到端方法。
- **UniAD** (Hu et al., CVPR 2023)：规划导向的端到端自动驾驶基线，将检测、跟踪、建图与规划统一。
- **AutoVLA** (Zhou et al., arXiv 2025)：基于视觉-语言-动作模型的闭环方法，在 Bench2Drive 上达到 78.84 Driving Score，被 DriveSuprim 的 83.02 超越（+4.18）。

### 核心改进槽位与适用边界

DriveSuprim 相对于选择式规划基线的改进集中在三个关键槽位：

| 改进槽位 | 基线做法 | DriveSuprim 做法 | 增益机制 |
|---------|---------|-----------------|---------|
| 候选轨迹选择策略 | 单阶段全局评分 | 粗到细两阶段过滤与精细评分 | 先粗筛 Top-K 候选，再对困难样本多层精细化评分，有效区分“硬负样本” |
| 数据增强 | 无或标准视角输入 | 基于旋转的伪全景视角增强 | 通过水平平移和裁剪模拟自车转弯场景，缓解转弯数据不足导致的方向性偏差 |
| 训练优化目标 | 硬二元分类损失 | 教师自蒸馏产生的软标签损失 | 用 EMA 教师模型提供限幅软标签，替代硬决策边界，稳定训练过程 |

消融实验（Table 5）证实了各模块的独立贡献：引入粗到细多阶段选择后 EPDMS 从 81.4 提升至 82.4；加入旋转数据增强后进一步提升至 82.7；自蒸馏最终推至 83.1。Table 6 进一步揭示，轨迹过滤带来的增益（+0.7%）远超单纯增加解码器层数（+0.3%），说明候选空间的有效缩减是性能提升的核心驱动力。

**适用边界**：DriveSuprim 的设计假设候选轨迹词汇表能覆盖安全驾驶所需的行为空间。在开环基准（NAVSIM v1/v2）和闭环基准（Bench2Drive）上均验证有效，且与不同骨干网络（ResNet34、V2-99、ViT-L）兼容。所有实验使用相同训练数据，未引入额外数据源，对比公平。

### 局限与开放问题

**已知局限**：
- 将过滤策略扩展到多于两个阶段未能带来额外提升（原文明确指出），表明当前粗到细框架的边际收益已趋于饱和。
- 模型在极端或边缘场景下仍有提升空间，特别是候选词汇表未覆盖的长尾安全关键情形。

**开放问题**：
1. **更有效的多阶段细化策略**：当前两阶段设计已达瓶颈，如何设计能持续带来增益的层次化选择机制（如自适应阶段数、基于不确定性的候选扩充）是值得探索的方向。
2. **安全约束的显式建模**：当前方法依赖模仿学习和评分损失隐式学习安全行为，能否结合强化学习的安全约束或可达性分析，构建更鲁棒的规划系统，是一个重要的开放问题。
3. **候选词汇表的动态生成**：DriveSuprim 依赖固定的预定义轨迹词汇表，在开集场景下可能覆盖不足。如何将粗到细选择与在线轨迹生成相结合，平衡效率与覆盖度，值得进一步研究。



## 原文 PDF

![[paperPDFs/AAAI_2026/DriveSuprim_Towards_Precise_Trajectory_Selection_for_End_to_End_Planning.pdf]]

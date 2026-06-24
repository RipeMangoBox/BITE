---
title: PICO Reconstructing 3D People In Contact with Objects
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/PICO_Reconstructing_3D_People_In_Contact_with_Objects.pdf
aliases:
- PF
- PR3PCO
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过PICO-db数据集提供双向身体-物体接触对应关系，并以此引导PICO-fit三阶段优化过程，显式建立身体与物体网格间的3D接触约束，实现物体位姿求解与人体姿态细化。
primary_logic: 身体接触可以通过PCA自动参数化为接触轴，仅需两次点击即可将其投射到物体网格上，实现低成本的密集接触标注；利用这些标注，可以从PICO-db中检索最近邻接触对应，作为强约束迭代拟合3D人体与物体网格，从而在无训练的情况下泛化到全新的物体类别。
claims:
- PICO-fit*在InterCap上取得PA-CD_h+o 8.36 cm，显著优于所有基线方法(PHOSA*为13.28 cm，CONTHO*为12.81 cm)，验证了密集接触对应的作用。
- 在DAMON自然图像的感知研究中，PICO-fit*在74.4%的比较中被评选为更真实的人-物接触重建，远超HDM (20.1%)和CONTHO* (24.7%)。
- 消融实验表明，Stage 1的接触初始化使PA-CD_h+o从12.9降至8.40，Stage 3的人体姿态细化进一步降至8.36，证明三阶段设计的必要性。
- InterCap 上 PA-CD_h+o (cm) (without GT contact) = 10.33
---

# PICO Reconstructing 3D People In Contact with Objects

> [!tip] 核心洞察
> 身体接触可以通过PCA自动参数化为接触轴，仅需两次点击即可将其投射到物体网格上，实现低成本的密集接触标注；利用这些标注，可以从PICO-db中检索最近邻接触对应，作为强约束迭代拟合3D人体与物体网格，从而在无训练的情况下泛化到全新的物体类别。

| 字段 | 内容 |
|------|------|
| 中文题名 | PICO：从单张图像重建与物体接触的3D人体 |
| 英文题名 | PICO Reconstructing 3D People In Contact with Objects |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PICO-fit |
| Dataset | InterCap, DAMON |

> [!tip] 效果简介
> - InterCap 上，PA-CD_h+o (cm) (without GT contact) 10.33 vs 13.14 (CONTHO), 13.38 (PHOSA), 13.6 (HDM) (-2.81 ~ -3.27)；PA-CD_h+o (cm) (with GT contact) 8.36 vs 13.28 (PHOSA*), 12.81 (CONTHO*) (-4.92 ~ -4.45)。
> - DAMON (in-the-wild) 上，Perceptual Preference Rate 74.4% vs 20.1% (HDM), 24.7% (CONTHO*), 32.0% (PHOSA*) (+42.4% ~ +54.3%)。

## 概述

从单张自然图像重建与物体接触的3D人体，是计算机视觉中长期悬而未决的难题。现有方法要么依赖手工设计的类别级接触约束（如PHOSA），要么在合成数据集上训练回归模型（如HDM、CONTHO），均无法稳健恢复物体的3D形状以及人与物体之间的密集3D接触对应，导致3D人-物交互（HOI）重建无法泛化到开放物体类别与野外场景。

PICO针对这一瓶颈提出了系统性解决方案。其核心洞察在于：**身体接触可以通过PCA自动参数化为接触轴，仅需两次点击即可将其投射到物体网格上**，从而实现低成本的密集双向接触标注。基于这一机制，PICO构建了PICO-db——首个在自然图像上提供顶点级身体-物体接触对应的数据集；并进一步设计了PICO-fit，一种**无需训练的优化方法**，通过从PICO-db中检索最近邻接触对应作为强约束，迭代拟合3D人体与物体网格。

PICO-fit采用三阶段优化策略：首先利用接触约束求解物体位姿，随后通过物体掩膜对齐与穿透抑制细化物体姿态，最后在保持接触的前提下细化人体姿态。这种设计使PICO-fit能够处理627种物体类别，远超PHOSA（8类）和CONTHO/HDM（30类），在InterCap基准上取得PA-CD_h+o 8.36 cm的精度，显著优于所有基线方法；在DAMON自然图像的感知研究中，74.4%的比较中被评选为更真实的人-物接触重建。

尽管PICO在泛化性和精度上取得了突破，其性能仍受限于接触预测（DECO）的偏差和物体检索的准确性，尤其是在脚部接触误报和严重遮挡场景下存在失败风险。

## 背景与动机

从单张自然图像中重建人与物体交互的三维场景（3D HOI）是计算机视觉中的核心挑战。其关键难点在于，真实世界中人与物体的接触关系极其复杂：同一类物体（如椅子）可以以数十种不同方式被人体接触，而不同类物体（如行李箱与滑板）又可能共享相似的接触模式。这使得传统的类别级先验难以覆盖开放场景中的交互多样性。

现有方法在这一瓶颈上存在两类根本性缺口。**基于优化的方法**（如 **PHOSA**）依赖手工设计的类别级接触约束，无法处理训练中未见过的物体类别，且缺乏精确的顶点级接触对应，导致重建结果在接触区域出现穿透或悬空。**基于回归的方法**（如 **HDM** 在合成数据集 ProciGen 上训练，**CONTHO** 在 BEHAVE 数据集上训练）虽然速度较快，但其泛化能力被训练数据的物体类别和交互模式所限制，难以迁移到野外自然图像中的任意物体。

上述缺口的本质原因在于：**现有数据集中缺乏对“身体-物体”双向密集三维接触对应的标注**。DAMON 数据集仅标注了人体侧的接触区域，却缺少物体侧的对应点；而其他 HOI 数据集或仅有类别级交互标签，或局限于受控实验室环境。这使得现有方法无法显式地建立身体顶点与物体表面点之间的一一对应关系，从而丧失了求解物体位姿与细化人体姿态的最强约束信号。

本文的动机正是填补这一空白。核心思路是：如果能以低成本获取身体与物体间的密集接触对应，并将其作为强约束引入三维拟合过程，就有可能在无需训练的情况下，从单张图像中泛化到全新的物体类别与交互方式。为此，本文提出 **PICO** 框架，包含两个关键组件：（1）**PICO-db**——一个通过 PCA 轴参数化与两次点击标注构建的双向接触对应数据集；（2）**PICO-fit**——一个三阶段优化方法，利用从 PICO-db 检索到的接触对应，迭代求解物体位姿并细化人体姿态。

## 核心创新

PICO 的核心创新在于**首次构建了面向自然图像的双向密集 3D 人-物接触对应数据集 PICO-db**，并以此为因果调节器驱动一个无需训练的优化框架 PICO-fit，实现了从单张野外图像重建任意物体类别与人体交互的 3D 网格。其关键 changed slots 如下：

### 1. 接触约束来源：从类别级先验到密集顶点级对应

现有方法要么完全缺乏物体接触标注（如 DAMON 仅标注人体），要么依赖手工设计的类别级接触规则（如 **PHOSA** 使用固定接触先验），无法泛化到开放物体类别。PICO 的突破在于：

- **PICO-db 构建**：复用 DAMON 在自然图像上的人体接触标注，通过 PCA 自动提取每个接触片段的接触轴（第一主成分方向），仅需标注者在物体网格上点击两次（指定轴的起点和方向），即可将人体接触点投射到物体表面，建立**双向身体-物体顶点级接触对应**（Figure 2, Figure 3）。这一设计将标注成本降至极低，使得大规模密集接触标注成为可能。
- **接触驱动的检索与匹配**：给定输入图像，PICO-fit 首先预测人体接触区域（DECO + GPT-4V 精炼），然后在 PICO-db 中检索最近邻的人体接触，并提取对应的物体接触点集 S = {(v_i, p_i)}，其中 v_i 为人体顶点，p_i 为物体表面点。这一检索机制使得接触约束从“类别级猜测”升级为“实例级匹配”。

### 2. 物体形状获取：从类别特定模型到开放词汇检索

- **Baseline 局限**：PHOSA 依赖类别特定的 3D 模型库进行检索，HDM 在合成数据集 ProciGen 上训练回归，CONTHO 在 BEHAVE 数据集上训练——这些方法均受限于预定义的物体类别集合。
- **PICO 方案**：采用 **OpenShape** 基础模型在 **Objaverse-LVIS** 数据库中进行开放词汇的最近邻检索，无需任何物体类别先验。结合 GPT-4V 预测的实例级物体缩放初始化，PICO-fit 可处理训练集中从未出现过的物体类别（Figure 7 展示了在背包、滑板、拐杖等全新类别上的重建结果）。

### 3. 拟合策略：从单阶段优化到三阶段接触驱动迭代

PICO-fit 将重建过程分解为三个具有明确因果关系的阶段（Figure 4），每个阶段仅优化特定变量并引入针对性损失：

- **Stage 1（基于接触的物体位姿求解）**：固定人体网格，仅优化物体的旋转与平移，最小化接触损失：
  $$\mathcal{L}_c = \frac{1}{|\mathbb{S}|} \sum_{(v_i, p_i) \in \mathbb{S}} \| v_i - p_i \|_2$$
  这一阶段利用密集接触对应直接“注册”物体到人体上，解决了物体位姿初始化难题。消融实验表明，去除 Stage 1 后 PA-CD_{h+o} 从 8.36 cm 升至 12.9 cm（Table S.1）。

- **Stage 2（物体与图像对齐）**：在保持接触约束的同时，引入物体掩膜损失 $\mathcal{L}_o^m = 1 - \mathrm{IoU}(M_o, \bar{M}_o)$（基于 SAM 检测掩膜）和穿透损失 $\mathcal{L}_p = \sum_{v_i \in \mathcal{O}} \Omega_h(v_i)$（使用 SDF 惩罚任意深度的穿透，包括极端穿透），微调物体位姿与缩放。

- **Stage 3（人体姿态细化）**：固定物体网格，仅优化接触链上的肢体关节姿态参数，最小化人体掩膜损失 $\mathcal{L}_h^m = 1 - \mathrm{IoU}(M_h, \bar{M}_h)$ 与姿态正则项 $\mathcal{L}_{\theta_c} = \|\theta - \theta^*\|_2$，同时保持接触损失约束。消融实验表明，Stage 3 将 PA-CD_{h+o} 从 8.40 cm 进一步降至 8.36 cm（Table 2）。

### 4. 穿透处理：从浅表惩罚到 SDF 深度穿透抑制

PHOSA 仅惩罚浅表穿透，无法处理严重的人-物交叉。PICO-fit 采用 SDF 定义的穿透损失 $\Omega_h(v_i) = -\min(\mathrm{SDF}(v_i), 0)$，对物体顶点穿透人体网格的深度进行精确惩罚，有效消除了极端穿透伪影。

**方法定位**：PICO-fit 属于基于优化的 render-and-compare 范式，与回归方法（HDM、CONTHO）形成互补。其核心优势在于**零样本泛化能力**——无需在特定 HOI 数据集上训练，即可通过 PICO-db 检索适配全新的物体类别与交互模式。在 InterCap 基准上，PICO-fit* 的 PA-CD_{h+o} 达到 8.36 cm，显著优于 PHOSA*（13.28 cm）和 CONTHO*（12.81 cm）；在 DAMON 野外图像的感知研究中，74.4% 的比较中 PICO-fit* 被评选为更真实的重建（Table 1）。

## 整体框架

PICO-fit 是一个基于优化的三阶段人-物交互（HOI）三维重建框架，其核心目标是从单张自然图像中恢复彼此真实配准的3D人体网格与物体网格。整个pipeline的输入为一张RGB图像，输出为SMPL-X参数化人体网格与检索得到的物体网格在三维空间中的联合配准结果，以及两者之间的密集接触对应关系。

框架遵循“初始化—接触驱动物体位姿求解—图像对齐与穿透抑制—人体姿态细化”的四步信息流，如图4所示。

**初始化模块** 负责为后续优化提供所有必要的先验估计。具体而言：
- **人体初始化**：通过OSX回归器从图像推断SMPL-X人体网格，获得初始姿态参数 $\theta^*$ 与形状参数。
- **物体初始化**：利用OpenShape基础模型在Objaverse-LVIS数据库中进行特征检索，获取与图像中物体最匹配的三维网格，并借助GPT-4V预测实例级缩放因子 $s_o^*$。
- **接触初始化**：首先由DECO预测人体表面的接触区域，经GPT-4V精炼后，在PICO-db中检索最近邻的身体-物体接触对应关系 $\mathbb{S} = \{(v_i, p_i)\}$，其中 $v_i$ 为人体接触顶点，$p_i$ 为物体表面上的对应点。

**Stage 1（基于接触的物体位姿求解）** 在固定人体姿态的前提下，仅优化物体的旋转与平移参数。其核心驱动力为接触损失：

$$\mathcal{L}_c = \frac{1}{|\mathbb{S}|} \sum_{(v_i, p_i) \in \mathbb{S}} \| v_i - p_i \|_2$$

该损失最小化人体接触顶点与物体表面对应点之间的欧氏距离，从而将物体“注册”到人体上，为后续阶段提供合理的位姿初始值。

**Stage 2（物体与图像对齐）** 在Stage 1的基础上进一步优化物体的旋转、平移与缩放参数，使物体网格与图像证据对齐。该阶段引入三项新损失：
- 物体掩膜损失 $\mathcal{L}_o^m = 1 - \mathrm{IoU}(M_o, \bar{M}_o)$，基于SAM检测的物体掩膜 $M_o$ 与渲染掩膜 $\bar{M}_o$ 的IoU度量。
- 穿透损失 $\mathcal{L}_p = \sum_{v_i \in \mathcal{O}} \Omega_h(v_i)$，利用SDF惩罚物体顶点穿透人体网格，其中 $\Omega_h(v_i) = -\min(\mathrm{SDF}(v_i), 0)$，可处理任意深度的穿透。
- 缩放损失 $\mathcal{L}_o^s = \| s_o - s_o^* \|_2$，约束物体缩放不偏离GPT-4V的初始估计。

Stage 2的总损失为上述四项的加权和：

$$L_2 = \lambda_c \mathcal{L}_c + \lambda_p \mathcal{L}_p + \lambda_o^m \mathcal{L}_o^m + \lambda_o^s \mathcal{L}_o^s$$

其中权重设定为 $\lambda_c=4$，$\lambda_p=100$，$\lambda_o^m=0.4$，$\lambda_o^s=4$。

**Stage 3（人体姿态细化）** 在物体位姿已与图像对齐后，进一步优化接触肢体链上的关节姿态参数，使人体更好地贴合接触约束与图像掩膜。该阶段优化接触损失 $\mathcal{L}_c$、穿透损失 $\mathcal{L}_p$、人体掩膜损失 $\mathcal{L}_h^m = 1 - \mathrm{IoU}(M_h, \bar{M}_h)$ 以及姿态正则项 $\mathcal{L}_{\theta_c} = \|\theta - \theta^*\|_2$（限制接触链上的姿态参数不偏离初始值）。总损失为：

$$L_3 = \lambda_c \mathcal{L}_c + \lambda_p \mathcal{L}_p + \lambda_h^m \mathcal{L}_h^m + \lambda_{\theta_c} \mathcal{L}_{\theta_c}$$

权重设定为 $\lambda_c=4$，$\lambda_p=50$，$\lambda_h^m=0.1$，$\lambda_{\theta_c}=0.05$。

**模块间的因果依赖关系** 清晰且可验证：Stage 1的接触驱动物体位姿求解是整个pipeline的瓶颈——消融实验表明，去除Stage 1后PA-CD_h+o从8.36升至12.9（Table S.1）；Stage 2的掩膜对齐与穿透抑制将误差进一步降至8.40；Stage 3的人体姿态细化带来最终的8.36（Table 2）。接触损失 $\mathcal{L}_c$ 是最关键的约束信号，移除后性能崩溃至26.63（Table S.1），证实了PICO-db密集接触对应在整个框架中的核心驱动作用。

### 补充图表

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/004_Figure_4.jpg]]
*Figure 4: Overview of PICO-fit, a novel method for fitting interacting 3D body and object meshes to an image. It initializes (Sec. 4.1) 3D body shape and pose via OSX [50], 3D object shape via OpenShape [53], and body-object contacts via retrieval from PICO-db (Sec. 3). Then, it takes three steps: (1) It exploits contacts to solve for object pose, to register the object to the body (Sec. 4.2). (2) It refines object pose (Sec. 4.3) and (3) body pose (Sec. 4.4) to align these to an object and human mask, respectively, detected in the image while satisfying contacts and avoiding penetrations. For every stage we show inputs, outputs, losses, and optimizable variables. ü Zoom in to see details*

## 核心模块与公式推导

PICO-fit 采用“初始化—三阶段优化”的流水线架构，其核心设计在于将 PICO-db 中检索到的密集双向接触对应作为显式几何约束，驱动物体位姿求解与人体姿态细化。以下按模块拆解其关键公式与变量含义。

### 初始化模块

给定单张 RGB 图像 $I$，初始化模块并行完成三项任务（见 Figure 4 概览）：
1. **人体初始化**：使用 OSX 回归器推断 SMPL-X 身体网格 $H$，获得初始姿态 $\theta^*$ 与形状参数。
2. **物体初始化**：通过 OpenShape 基础模型在 Objaverse-LVIS 数据库中进行最近邻检索，获取物体网格 $O$，并由 GPT-4V 预测实例级初始缩放 $s_o^*$。
3. **接触初始化**：利用 DECO 预测身体接触区域，经 GPT-4V 精炼后，从 PICO-db 中检索匹配的物体接触对应集合 $\mathbb{S} = \{(v_i, p_i)\}$，其中 $v_i$ 为人体顶点，$p_i$ 为物体表面上的对应点。

### Stage 1：基于接触的物体位姿求解

Stage 1 的核心目标是在固定人体的前提下，利用接触对应求解物体的旋转与平移，实现物体到人体的初始配准。其唯一驱动力是**接触损失** $\mathcal{L}_c$：

$$\mathcal{L}_c = \frac{1}{|\mathbb{S}|} \sum_{(v_i, p_i) \in \mathbb{S}} \| v_i - p_i \|_2$$

该损失最小化人体接触顶点 $v_i$ 与物体表面对应点 $p_i$ 之间的欧氏距离。此阶段仅优化物体的 6-DoF 位姿参数（旋转与平移），不涉及缩放。$\mathcal{L}_c$ 的设计直接体现了 PICO 的核心洞察：密集接触对应可作为强几何约束，无需依赖类别级先验或合成数据即可完成初始配准。

### Stage 2：物体掩膜对齐与穿透抑制

Stage 2 在 Stage 1 的基础上进一步优化物体的旋转、平移与缩放，使物体网格与图像证据对齐。该阶段的总损失为：

$$L_2 = \lambda_c \mathcal{L}_c + \lambda_p \mathcal{L}_p + \lambda_o^m \mathcal{L}_o^m + \lambda_o^s \mathcal{L}_o^s$$

其中各损失项定义如下：

**物体掩膜损失** $\mathcal{L}_o^m$：度量 SAM 检测的物体掩膜 $M_o$ 与可微渲染掩膜 $\bar{M}_o$ 的一致性：
$$\mathcal{L}_o^m = 1 - \mathrm{IoU}(M_o, \bar{M}_o)$$

**穿透损失** $\mathcal{L}_p$：利用有符号距离函数（SDF）惩罚物体顶点穿透人体网格，可处理任意深度的穿透（包括极端穿透）：
$$\mathcal{L}_p = \sum_{v_i \in \mathcal{O}} \Omega_h(v_i), \quad \Omega_h(v_i) = -\min(\mathrm{SDF}(v_i), 0)$$

其中 $\mathcal{O}$ 为物体顶点集合，$\Omega_h(v_i)$ 仅在物体顶点位于人体内部（$\mathrm{SDF}(v_i) < 0$）时产生非零惩罚。

**物体缩放损失** $\mathcal{L}_o^s$：约束优化后的缩放 $s_o$ 不偏离 GPT-4V 的初始估计 $s_o^*$：
$$\mathcal{L}_o^s = \| s_o - s_o^* \|_2$$

权重配置为 $\lambda_c=4$，$\lambda_p=100$，$\lambda_o^m=0.4$，$\lambda_o^s=4$（见 S.3.1）。$\lambda_p$ 的高权重反映了对穿透的严格抑制需求。

### Stage 3：人体姿态细化与接触保持

Stage 3 固定 Stage 2 输出的物体位姿，优化接触肢体链上的姿态参数，使人体与像素对齐的物体之间接触更精确。总损失为：

$$L_3 = \lambda_c \mathcal{L}_c + \lambda_p \mathcal{L}_p + \lambda_h^m \mathcal{L}_h^m + \lambda_{\theta_c} \mathcal{L}_{\theta_c}$$

其中：

**人体掩膜损失** $\mathcal{L}_h^m$：与物体掩膜损失类似，度量 SAM 检测的人体掩膜 $M_h$ 与渲染掩膜 $\bar{M}_h$ 的一致性：
$$\mathcal{L}_h^m = 1 - \mathrm{IoU}(M_h, \bar{M}_h)$$

**姿态正则项** $\mathcal{L}_{\theta_c}$：限制接触链上的姿态参数 $\theta$ 不偏离初始值 $\theta^*$，防止过拟合导致姿态失真：
$$\mathcal{L}_{\theta_c} = \|\theta - \theta^*\|_2$$

权重配置为 $\lambda_c=4$，$\lambda_p=50$，$\lambda_h^m=0.1$，$\lambda_{\theta_c}=0.05$（见 S.3.1）。与 Stage 2 相比，穿透惩罚权重降低（100→50），因为此阶段主要优化人体姿态，物体已相对固定；人体掩膜权重较低（0.1），以避免过度驱动姿态偏离接触约束。

### 设计逻辑总结

三阶段的递进关系体现了从粗到精的优化策略：Stage 1 仅依赖接触约束求解物体位姿，避免图像噪声干扰；Stage 2 引入掩膜与穿透约束，将物体与像素证据对齐；Stage 3 在物体固定的前提下微调人体姿态，同时保持接触一致性。消融实验（Table 2 与 Table S.1）验证了这一设计的必要性：移除 Stage 1 导致 PA-CD$_{h+o}$ 从 8.36 升至 12.9 cm；移除 $\mathcal{L}_c$ 则使误差飙升至 26.63 cm，证实接触损失是整个流水线的核心驱动因素。

### 补充图表

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/003_Figure_3.jpg]]
*Figure 3: Example contact patches with their contact axis*

## 实验与分析

### 核心实验结果

PICO-fit 在 InterCap 数据集和 DAMON 野外图像感知研究中均表现出显著优势，验证了密集接触对应在 3D HOI 重建中的核心作用。

**InterCap 定量评估**：在没有 GT 接触标注的条件下，PICO-fit 取得 PA-CD_h+o 10.33 cm，显著优于 CONTHO（13.14 cm）、PHOSA（13.38 cm）和 HDM（13.6 cm）。当使用 GT 接触标注时（PICO-fit*），性能进一步提升至 PA-CD_h+o 8.36 cm，相比 PHOSA*（13.28 cm）和 CONTHO*（12.81 cm）分别降低 4.92 cm 和 4.45 cm（Table 1）。值得注意的是，所有方法均未在 InterCap 上训练，该结果直接衡量跨数据集泛化能力。

**野外感知研究**：在 DAMON 自然图像上，PICO-fit* 在 74.4% 的比较中被评选为更真实的人-物接触重建，远超 HDM（20.1%）、CONTHO*（24.7%）和 PHOSA*（32.0%）（Table 1 右列）。公平性处理包括将 HDM 输出的点云转换为网格以避免可视化偏差。

**关键瓶颈**：PICO-fit 在 InterCap 上的物体重建误差较高（PA-CD_o 21.85 cm），主要瓶颈为接触预测准确性（DECO 偏差导致约 85/500 失败，尤其脚部误报严重）和物体检索准确性（类别/几何匹配错误导致约 12/500 失败）。当人体接触预测正确时，仍可能出现无效的物体接触对应检索（20/500 失败）；人体姿态初始化错误（OSX）导致约 5/500 失败。

### 消融实验

三阶段设计的必要性通过严格消融得到验证（Table 2, Table S.1）：

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/006_Table_2.jpg]]
*Table 2: Ablation study for PICO-fit’s three fitting stages. We evaluate on the InterCap [32] dataset, and report the Procrustes-Aligned Chamfer Distance (PA-CD) for the human (h), object (o), and their combination (h+o). The middle columns show the losses and optimized variables. For qualitative ablation, see Sup. Mat*

- **Stage 1（接触驱动物体位姿求解）必不可少**：去除 Stage 1 后，PA-CD_h+o 从 8.36 升至 12.9 cm（Table S.1），表明基于接触的物体位姿初始化是后续对齐的基础。
- **Stage 3（人体姿态细化）带来增益**：仅使用 Stage 1+2 得到 PA-CD_h+o 8.40 cm，加入 Stage 3 后降至 8.36 cm，验证了在物体对齐后细化接触肢体姿态的必要性。
- **接触损失 L_c 至关重要**：移除 L_c 后 PA-CD_h+o 从 8.36 飙升至 26.63 cm（Table S.1），证实密集接触约束是重建精度的决定性因素。
- **GPT-4V 精炼接触预测提升性能**：DECO+GPT-4V 将接触 F1 从 0.29 提升至 0.35，并降低 PA-CD_h+o 从 11.76 到 10.33 cm（S.2），说明 VLM 常识推理可有效纠正纯视觉接触预测的偏差。

### 失败模式分析

PICO-fit 的主要失败模式可归纳为三类：

1. **接触预测错误**（最主要）：DECO 对人体接触区域的误判（尤其是脚部假阳性）导致检索到的物体接触对应无效，进而使后续优化陷入错误局部最优（Figure S.9, Rows 1-3）。
2. **物体检索错误**：OpenShape 对严重遮挡或小尺寸物体的 3D 形状检索不准确，导致物体几何与图像证据不匹配（Figure S.10, Bottom row）；即使人体接触正确，也可能检索到无效的物体接触对应（Figure S.9, Rows 4-5）。
3. **人体姿态初始化错误**：OSX 在复杂交互场景下的姿态估计偏差导致后续接触检索和拟合均失败（Figure S.10, Top row）。

### 重要图表结论

- **Table 1** 确立 PICO-fit 在 3D HOI 重建上的 SOTA 地位，无论是 GT 接触还是预测接触条件下均显著优于优化方法（PHOSA）和回归方法（CONTHO, HDM）。
- **Table 2** 量化三阶段贡献：Stage 1 提供最大增益（接触初始化），Stage 2 通过掩膜对齐和穿透抑制巩固物体位姿，Stage 3 实现人体姿态微调。
- **Figure 6** 定性展示 PICO-fit* 在接触真实性和空间对齐上明显优于 CONTHO* 和 PHOSA*，尤其在物体-人体接触区域的几何一致性上。
- **Figure 7** 证明 PICO-fit 可泛化到训练数据未覆盖的全新物体类别（如滑板、行李箱），验证了检索式接触对应方法的零样本能力。
- **Figure S.9** 系统揭示失败案例的因果链：接触预测偏差 → 无效接触检索 → 优化崩溃，为后续改进指明方向。

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/005_Table_1.jpg]]
*Table 1: Evaluation on 3D HOI reconstruction. Middle column: Evaluation on InterCap [32] (Sec. 5.1). Since no method trains on InterCap, this evaluates generalization. Right column: Evaluation on in-the-wild images via a perceptual study (Sec. 5.2). We report the preference rate of results from the competing method (denoted as “X”) over our PICO-fit∗. Left column: “Type” denotes regression or optimization. Using GT contact is highlighted with ∗*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative evaluation of CONTHO∗, HDM and PHOSA∗ alongside PICO-fit∗ on object categories handled by all baselines. From left to right: input image, pseudo-GT contact annotations in PICO-db, and 3D reconstructions (a side and top-down view per method). Reconstructions from PICO-fit∗ have better 3D human-object contact and spatial alignment. For more comparisons, see Sup. Mat*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/009_Figure_7.jpg]]
*Figure 7: HOI reconstructions from PICO-fit∗ on new, previously untackled object categories. Each row (left to right) shows, for three input RGB images, PICO-fit∗’s estimated meshes overlaid on the image (camera view) and a side view. For more results, see Sup. Mat*

### 补充图表

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/013_Table.jpg]]
*Table: S.1. Additional ablations, extending Tab. 2 of the paper*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/017_Figure.jpg]]
*Figure: RGB Image Stage 1 Stage 2 Stage 3 Figure S.8. Ablation study for PICO-fit’s stages*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/019_Figure.jpg]]
*Figure: Reconstruction Figure S.9. Example interactions where PICO-fit lookups on PICO-db fail. Each row from left to right: input image, predicted body contact from DECO + GPT-4V, looked-up contact from PICO-db and 3D reconstructions overlaid on the images. Rows 1-3: incorrect human contact prediction. Rows 4-5: incorrect object contact retrieval*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/020_Figure.jpg]]
*Figure: S.10. Failure cases of PICO-fit. Each row (from left to right) shows two input images and corresponding PICO-fit reconstructions overlaid on the image. Top row: incorrect human pose initialization. Bottom row: incorrect object retrieval*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of PICO-fit vs PHOSA on internet images used for evaluation in the PHOSA paper [97]*

![[assets/figures/papers/paper_list_l1745_PICO_Reconstructing_3D_People_In_Contact_with_Objects/figures/002_Figure_2.jpg]]
*Figure 2: PICO-db dataset annotations. Left to right: Color image. Contacts (shown in various colors) annotated on the body and object. Contact annotations establish bijective body-object correspondences, denoted with color-coding*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

从单张自然图像重建与物体接触的3D人体，长期受困于两个相互纠缠的瓶颈：(1) 物体3D形状的获取缺乏对开放类别的泛化能力；(2) 人与物体之间缺乏密集、双向的3D接触对应约束。现有方法或依赖类别级的手工接触先验（如PHOSA），或依赖合成数据训练的回归模型（如HDM、CONTHO），导致在野外场景和未见物体类别上的重建质量急剧下降。PICO的核心洞察在于：**身体接触可以通过PCA自动参数化为接触轴，仅需两次点击即可将其投射到物体网格上**，从而以极低的标注成本构建密集的双向接触对应数据集PICO-db；该数据集进而驱动一个无需训练的优化框架PICO-fit，通过检索最近邻接触对应作为强约束，迭代拟合3D人体与物体网格。

### 2. 与基线方法的关系定位

PICO-fit在方法谱系中占据“基于优化的开放类别HOI重建”这一独特位置，与现有工作的关系可从以下维度展开：

**vs. PHOSA（基于优化的类别级方法）**：PHOSA采用单阶段优化，使用手工设计的类别级接触约束（如“骑摩托车时手应接触车把”），且物体形状来自类别特定的检索数据库。PICO-fit与之共享优化范式，但根本性差异在于：(1) 接触约束从类别级手工规则升级为实例级密集顶点对应，来源从先验知识变为PICO-db的数据驱动检索；(2) 物体形状获取从类别受限检索升级为基于OpenShape基础模型的开放类别检索；(3) 优化从单阶段升级为三阶段递进式拟合。在InterCap基准上，PICO-fit*的PA-CD_h+o为8.36 cm，相比PHOSA*的13.28 cm降低37%，证实了密集接触对应替代类别级约束的显著收益。

**vs. CONTHO（基于回归的联合重建方法）**：CONTHO在BEHAVE数据集上训练，输出人体与物体的联合重建。PICO-fit与之的核心差异在于范式选择——回归vs.优化。回归方法的优势在于推理速度快，但劣势在于泛化能力受限于训练数据分布。PICO-fit的优化范式使其无需在HOI数据上训练，从而天然具备对全新物体类别的泛化能力。在InterCap上（所有方法均未在该数据集上训练），PICO-fit*的PA-CD_h+o为8.36 cm，优于CONTHO*的12.81 cm，验证了优化范式在跨域泛化场景下的优势。在DAMON野外图像的感知研究中，PICO-fit*以74.4%的偏好率远超CONTHO*的24.7%，进一步证实了其在真实场景下的鲁棒性。

**vs. HDM（基于回归的点云方法）**：HDM在合成数据集ProciGen上训练，输出人体与物体的点云表示。PICO-fit与HDM的分歧不仅在于回归vs.优化的范式选择，更在于输出表示——网格vs.点云。网格表示天然支持接触对应、穿透检测和可微渲染，为三阶段优化提供了技术基础。在InterCap上，PICO-fit的PA-CD_h+o为10.33 cm，优于HDM的13.6 cm；在感知研究中，PICO-fit*的偏好率为74.4%，远超HDM的20.1%。

### 3. 技术谱系中的关键创新槽位

PICO-fit相对于基线方法的技术创新可归纳为以下关键槽位的变更：

| 槽位 | 基线方法取值 | PICO-fit取值 | 证据锚点 |
|------|-------------|-------------|---------|
| 接触约束来源 | 无(DAMON)或类别级手工规则(PHOSA) | PICO-db密集双向接触对应，通过PCA轴+两次点击标注 | Sec. 3.2, Fig. 3 |
| 物体形状获取 | 类别特定检索(PHOSA)或合成数据(HDM) | OpenShape在Objaverse-LVIS中最近邻检索，支持任意类别 | Sec. 3.1, 4.1 |
| 拟合策略 | 单阶段优化(PHOSA)或端到端回归(CONTHO, HDM) | 三阶段递进：接触驱动物体位姿→掩膜对齐与穿透抑制→人体姿态细化 | Sec. 4.2-4.4, Fig. 4 |
| 穿透处理 | 仅惩罚浅表穿透(PHOSA) | SDF惩罚任意深度穿透 | Sec. 4.3, L_p |
| 物体缩放 | 每类别固定缩放(PHOSA) | GPT-4V实例级预测+Stage 2微调 | Sec. 4.1, 4.3, S.2 |

### 4. 适用边界与局限

PICO-fit的适用边界由其技术架构的内在约束决定：

**接触预测依赖链的脆弱性**：PICO-fit的性能高度依赖DECO接触预测→PICO-db检索→接触对应建立这一链条的准确性。消融实验表明，移除接触损失L_c后PA-CD_h+o从8.36骤升至26.63（Table S.1），揭示系统对接触信号极度敏感。实际失败模式包括：(1) DECO接触预测偏差（约85/500重建失败），尤其脚部接触假阳性严重；(2) 即使人体接触正确，物体接触对应检索仍可能无效（约20/500）；(3) 物体检索的类别与几何匹配错误（约12/500）。这些失败模式在Figure S.9和S.10中有详细可视化。

**物体重建的精度瓶颈**：在InterCap上，PICO-fit的物体重建误差PA-CD_o为21.85 cm，显著高于人体重建的7.43 cm（Table 1）。这一不对称性源于：人体由OSX提供强先验初始化，而物体仅依赖OpenShape检索的近似形状，缺乏像素级几何约束。Stage 2的掩膜对齐仅提供轮廓级监督，难以纠正检索物体的拓扑错误。

**优化范式的固有代价**：三阶段优化依赖多个超参数权重（λ_c=4, λ_p=100/50, λ_o^m=0.4, λ_h^m=0.1, λ_θ_c=0.05），需针对不同场景手动调整。优化过程本身也较慢，不适合实时应用场景。此外，人体姿态初始化（OSX）的错误会导致约5/500的失败，且三阶段优化难以完全纠正初始化的严重偏差。

**PICO-db覆盖范围的限制**：PICO-fit的泛化能力受限于PICO-db中存储的接触对应模式。对于全新的交互类型（如非标准姿态下的物体操作），最近邻检索可能无法提供合适的接触对应，导致优化缺乏有效约束。

### 5. 开放问题与后续工作方向

基于上述局限，以下研究方向值得关注：

1. **接触预测的鲁棒性提升**：DECO在脚部的假阳性是当前最主要的失败来源。一个直接方向是训练专门针对HOI场景的接触预测模型，或利用视觉-语言模型（VLMs）的常识推理能力过滤不合理预测。

2. **前馈接触对应预测**：当前PICO-db的最近邻检索可被替换为训练一个前馈网络，直接从图像预测身体-物体接触对应，从而消除检索失败模式并加速推理。这需要PICO-db本身作为训练数据。

3. **物体形状检索的增强**：OpenShape对严重遮挡、小尺寸物体的检索能力不足。结合多视角信息或利用VLMs的语义理解辅助检索，可能提升物体形状初始化的准确性。

4. **优化效率的提升**：三阶段优化的计算开销限制了PICO-fit的实时应用。探索隐式神经表示或可微渲染加速技术，可能在不牺牲精度的前提下大幅缩短优化时间。

5. **扩展到动态场景**：PICO-db的标注流程和PICO-fit的优化框架目前限于单张图像。将其扩展到视频序列和多人体交互场景，需要解决时序一致性和多人接触分配等新挑战。

## 原文 PDF

![[paperPDFs/CVPR_2025/PICO_Reconstructing_3D_People_In_Contact_with_Objects.pdf]]
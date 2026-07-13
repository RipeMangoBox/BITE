---
title: EasyHOI Unleashing the Power of Large Models for Reconstructing Hand Object Interactions in the Wild
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Object_Interactions_in_the_Wild.pdf
code_link: null
project_link: https://lym29.github.io/EasyHOI-page
aliases:
- EUPLMRHOIW
tags:
- CVPR_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 利用预训练的大型分割、修复和三维重建模型提供强视觉与几何先验，并通过三阶段先验引导优化（相机对齐、接触对齐、手部参数细化）强制物理与图像一致性。
primary_logic: 即使独立使用大型模型存在估计误差，通过一个联合优化框架统一坐标、对齐接触并细化手部参数，可以生成物理合理的手物交互，无需额外标注训练数据。
claims:
- 大型模型（LISA、扩散修复、InstantMesh、HaMeR）能够为手物交互重建提供强大的视觉和几何先验。
- 三阶段优化（相机设置、接触对齐、手部细化）有效解决坐标不一致、估计误差和遮挡问题。
- 方法在多个数据集上超越了现有基线，展现出强大的零样本泛化能力。
- Arctic 上 MPVPE (cm) = 1.48
---

# EasyHOI Unleashing the Power of Large Models for Reconstructing Hand Object Interactions in the Wild

> [!tip] 核心洞察
> 即使独立使用大型模型存在估计误差，通过一个联合优化框架统一坐标、对齐接触并细化手部参数，可以生成物理合理的手物交互，无需额外标注训练数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | EasyHOI：释放大型模型在野外手物交互重建中的力量 |
| 英文题名 | EasyHOI Unleashing the Power of Large Models for Reconstructing Hand Object Interactions in the Wild |
| 会议/期刊 | CVPR 2025 |
| Links |  [Project](https://lym29.github.io/EasyHOI-page)|
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | EasyHOI |
| Dataset | Arctic |

> [!tip] 效果简介
> - Arctic 上，MPVPE (cm) 1.48 vs 1.14 (HaMeR) (+0.34 (更差))；MPJPE (cm) 0.95 vs 1.05 (HaMeR) (-0.10)。

## 概要

### 问题与瓶颈

从单张野外图像重建手与物体的三维交互（Hand-Object Interaction, HOI）是一项极具挑战的任务。其核心瓶颈在于：单视图固有的严重遮挡使物体几何高度不完整；二维图像到三维几何的深度歧义难以消解；手与物体分别独立重建导致坐标系统不一致；此外，高质量的三维手物交互标注数据稀缺，使现有基于训练的方法难以泛化到多样化的野外场景。

### 核心思路

EasyHOI 的核心洞察在于：即使独立使用现有的大型预训练模型（视觉分割、图像修复、三维重建、手部姿态估计）各自存在估计误差，只要通过一个精心设计的**联合优化框架**统一坐标系统、对齐接触区域并细化手部参数，就能在无需额外标注训练数据的前提下，生成物理上合理的手物交互重建。

该方法将大型模型视为强视觉与几何先验的提供者，而非端到端的求解器。因果调控的关键在于三阶段先验引导优化：**相机系统对齐**解决坐标不一致问题；**接触区域对齐**利用二维接触掩码与三维几何的射线投射建立手物空间关系；**手部参数细化**通过多损失联合优化（掩码一致性、穿透惩罚、接触吸引、姿态正则化）强制物理与图像双重约束。

### 方法定位

EasyHOI 并非一个端到端网络，而是一个**基于大型模型先验的多阶段优化管线**。其方法谱系可定位于：

- **物体重建**：利用扩散修复模型去除手部遮挡，结合 SAM 分割完整物体，再由大型重建模型 InstantMesh 生成三维网格。相比依赖训练数据的 AlignSDF（Zhang et al., CVPR 2024）和隐式形状场 gSDF（Ye et al., CVPR 2022），EasyHOI 的物体重建完全零样本，无需在目标数据集上训练。
- **手部重建**：以 HaMeR（Pavlakos et al., CVPR 2024）的 Transformer 姿态估计作为初始值，随后通过优化框架对 MANO 参数进行物理一致性细化，而非单纯依赖网络回归。
- **交互对齐**：与以往独立重建后简单拼接的方法不同，EasyHOI 通过接触区域驱动的 ICP 配准与掩码约束优化交替迭代，在三维空间中显式建立手物接触关系。

### 主要结果

在 Arctic、OakInk 和 DexYCB 三个公开数据集上的实验表明，EasyHOI 在零样本设定下一致超越现有基线。以 Arctic 数据集为例：当使用真实物体几何时，手部关节误差 MPJPE 从 HaMeR 的 1.05 cm 降至 0.95 cm；当使用预测物体几何时，手部顶点误差 MPVPE 为 1.48 cm，略逊于 HaMeR 的 1.14 cm，但整体交互质量（仿真位移、交叉体积）显著更优。消融实验证实，完整的相机对齐—接触对齐—手部细化三阶段流程在所有数据集上均取得最佳效果，且各损失项（穿透损失、接触损失、正则化损失）对物理合理性均有不可替代的贡献。

### 局限与开放问题

需注意的局限包括：预测物体几何时，物体重建误差会耦合进手部优化，导致手部精度略低于 HaMeR 独立估计；多模型级联与迭代优化带来较高计算成本，可能不适合实时场景；对指间严重遮挡或非标准抓握姿态的鲁棒性仍有待验证。开放问题指向：如何使大型视觉模型更专门地适配手物交互任务以提升效率与鲁棒性；能否扩展至动态视频或多手交互；以及如何减少级联依赖，设计更端到端的轻量方案。

手物交互（Hand-Object Interaction, HOI）重建是理解人类日常行为的关键技术，在机器人学习、增强现实和具身智能等领域具有广泛应用。其核心任务是从视觉输入中同时恢复手部姿态和物体几何，并确保二者之间的物理合理性。

### 单视图重建的核心挑战

从单张野外图像重建手物交互面临多重根本性困难。首先，**严重遮挡**是首要瓶颈：手部抓握物体时，手指和物体表面相互遮挡，导致可见区域极度有限。其次，单视图输入天然存在**几何歧义**——深度信息缺失使得从二维投影反推三维结构成为病态问题。此外，手部和物体的**独立重建**通常在不同的坐标系统中进行，缺乏统一的参考框架，导致重建结果在空间上不一致。最后，现有方法普遍依赖**高质量标注数据**进行监督训练，而手物交互的三维真值标注成本极高，限制了方法的泛化能力。

### 现有方法的缺口

传统方法通常将手部重建和物体重建视为两个独立任务，分别使用专用模型估计MANO手部参数和物体形状。例如，**HaMeR**（Pavlakos et al., CVPR 2024）基于Transformer架构实现了较强的野外手部姿态估计，而**gSDF**（Ye et al., CVPR 2022）和**AlignSDF**（Zhang et al., CVPR 2024）则通过隐式形状场或SDF对齐技术重建物体几何。然而，这些方法存在两个关键缺陷：一是**缺少显式的交互建模**，手和物体之间没有物理约束，容易产生穿透、悬空等不合理结果；二是**坐标系统不统一**，独立估计的手部和物体无法在统一空间中形成一致的交互关系。此外，基于训练的方法在跨域泛化时性能显著下降，难以应对野外场景的多样性。

### 大型模型的机遇与局限

近年来，预训练大型模型在分割、图像修复和三维重建等任务上展现出强大的视觉与几何先验能力。例如，**LISA**等视觉-语言模型能够通过推理分割出手部和物体区域，扩散修复模型可以移除遮挡恢复完整物体外观，而**InstantMesh**等大型重建模型能从单张图像直接生成三维网格。这些模型为摆脱对标注训练数据的依赖提供了可能。然而，直接组合这些独立模型存在**累积误差**问题：每个模型的估计偏差会在流水线中传播和放大，且模型之间缺乏协调机制，无法保证最终重建的物理一致性。

### 本文动机

基于上述分析，本文的核心动机是：**能否利用大型预训练模型提供的强先验，通过一个统一的优化框架来解决坐标不一致、估计误差和遮挡等根本问题，从而在无需额外训练数据的情况下实现物理合理的手物交互重建？** 这一思路的关键洞察在于——即使单个大型模型的估计存在误差，通过联合优化统一坐标系统、对齐接触区域并细化手部参数，可以强制重建结果同时满足二维图像一致性和三维物理约束，从而生成高质量的手物交互。

## 核心方法与创新机理

EasyHOI 的核心创新并非提出全新的网络架构，而是**构建了一套以大型预训练模型为强先验、以物理与图像一致性为约束的三阶段联合优化框架**，从而在无需额外标注训练数据的条件下，实现野外单视图手物交互的物理合理重建。其关键创新点可归纳为以下三个维度的 changed slots。

### 1. 统一坐标系统：从独立估计到全局对齐

传统方法（如 **HaMeR** / Pavlakos et al., CVPR 2024 对手部，**gSDF** / Ye et al., CVPR 2022 对物体）独立重建手部与物体，二者的坐标系统互不统一，导致后续无法进行有物理意义的交互分析。

EasyHOI 的 **Camera System Setup** 阶段将物体坐标系设为全局参考系，通过可微渲染与最优传输理论联合优化相机参数。具体而言，该阶段最小化渲染物体掩码与修复后物体掩码之间的软 IoU 损失（Eq. 1）与 Sinkhorn 距离（Eq. 3）：

$$ \mathcal{L}_{\mathrm{obj-mask}} = \mathrm{IOU}(M_o^r, \hat{M}_o) = \frac{M_o^r \cdot \hat{M}_o}{|M_o^r| + |\hat{M}_o| - M_o^r \cdot \hat{M}_o} $$

$$ \mathcal{L}_{\mathrm{OT}} = W\left(\frac{M_o}{|\hat{M}_o|}, \frac{\hat{M}_o}{|\hat{M}_o|}\right) $$

这一设计将手部与物体从“各自为政”的独立估计，转变为统一坐标系下的联合表示，为后续接触对齐与物理约束优化奠定了基础。

### 2. 交互对齐策略：从无约束重建到接触感知配准

现有手物重建方法通常缺乏显式的交互对齐机制，导致手部与物体在三维空间中相互穿透或悬空。

EasyHOI 的 **HOI Contact Alignment** 阶段引入了一种交替优化策略，在“掩码约束优化”与“基于接触的 ICP 配准”之间迭代。其核心机制是：首先从 2D 接触掩码通过射线投射生成 3D 接触点候选（Figure 4），然后利用这些接触点驱动手部全局姿态的刚性对齐。这一策略将原本无约束的重建结果，强制拉向满足接触几何约束的物理合理状态。

### 3. 手部优化损失函数：从单一掩码损失到多目标物理约束

传统手部重建方法通常仅依赖掩码损失进行优化，忽略了手物交互中至关重要的物理约束。

EasyHOI 的 **Hand Parameter Refinement** 阶段联合优化手部的全局姿态 $\phi_h \in \mathbb{R}^6$ 与关节参数 $\theta_h \in \mathbb{R}^{45}$，并引入四项损失函数的组合（Eq. 5）：

$$ \mathcal{L}_{\mathrm{hand}} = \lambda_{1} \mathcal{L}_{\mathrm{hand-mask}} + \lambda_{2} \mathcal{L}_{\mathrm{penetr}} + \lambda_{3} \mathcal{L}_{\mathrm{contact}} + \lambda_{4} \mathcal{L}_{\mathrm{reg}} $$

其中，**穿透损失** $\mathcal{L}_{\mathrm{penetr}}$（Eq. 6）惩罚手部顶点进入物体内部的行为，**接触损失** $\mathcal{L}_{\mathrm{contact}}$（Eq. 7）鼓励接触区域顶点贴近物体表面，**正则化损失** $\mathcal{L}_{\mathrm{reg}}$（Eq. 8）防止优化后的姿态偏离 HaMeR 初始估计过远。消融实验（Table 4）证实，去除穿透损失会导致交叉体积从 4.11 飙升至 9.62，而去除接触损失则使仿真位移从 3.08 恶化至 3.94，验证了每一项损失对物理合理性的关键贡献。

### 创新本质：先验注入而非数据驱动

EasyHOI 的创新本质在于**将大型模型的强视觉-几何先验（LISA 分割、扩散修复、InstantMesh 重建、HaMeR 姿态估计）通过一个精心设计的优化框架进行“物理蒸馏”**。与需要大量标注数据训练的 **AlignSDF**（Zhang et al., CVPR 2024）等方法不同，EasyHOI 完全以零样本方式工作，其泛化能力来源于预训练模型的先验知识，而非对特定数据分布的拟合。这一设计使其能够处理野外场景中多样化的手物配置与严重遮挡——这是传统数据驱动方法难以覆盖的长尾分布。

EasyHOI 的整体 pipeline 分为两大阶段：**初始重建**与**手物交互优化**（见 Figure 2）。初始重建阶段利用多个现成的大型预训练模型为手和物体分别提供强视觉与几何先验；交互优化阶段则通过三步骤的“先验引导优化”将独立估计的结果统一到物理一致的坐标系中，并强制接触与图像约束。整体流程从单张野外图像输入，最终输出物理合理的手物三维网格。

![[assets/figures/papers/paper_list_l1732_EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Obj/figures/002_Figure_2.jpg]]
*Figure 2: The illustration of our pipeline. We first extract hand and object masks through HOI reasoning for object reconstruction and recovering hand mesh from the input image. With these initial reconstructions, we employ a three-stage prior-guided optimizer to establish a camera system for object, align hand and object by analyzing contact points, and finally refines hand parameters to ensure physical plausibility*

### 初始重建：从单图到手物独立估计

初始重建的目标是从输入图像中分别恢复手部姿态和物体的完整几何，核心挑战在于手部遮挡导致物体外观不完整。流程依次调用以下大型模型：

1. **LISA**（视觉-语言分割模型）：通过 HOI 推理提取手部掩码和物体掩码，将手与物体区域分离。
2. **扩散修复模型**：移除手部区域，对遮挡部分进行修复，恢复物体的完整外观。
3. **SAM**（通用分割模型）：从修复后的图像中分割出完整的物体轮廓。
4. **InstantMesh**（大型重建模型）：从单张修复图像重建物体的三维网格。
5. **HaMeR**（基于 Transformer 的手部姿态估计）：从原始输入图像恢复 MANO 手部网格参数，包括全局 6-DoF 姿态 $\phi_h \in \mathbb{R}^6$ 和关节姿态 $\theta_h \in \mathbb{R}^{45}$。

Figure 3 展示了遮挡消除过程：原始图像中物体因手部遮挡被分割为两个不连通区域，修复后形成完整物体轮廓，SAM 再基于采样点和边界框提示完成分割。

### 手物交互优化：三阶段先验引导

初始重建得到的物体网格和手部网格来自不同模型，坐标系统不统一，且各自存在估计误差。交互优化阶段将两者统一到物体坐标系下，并通过以下三个步骤逐步修正：

1. **相机系统建立**：以重建物体的坐标系为全局参考，通过可微渲染优化相机参数。目标函数最小化渲染物体掩码与修复后物体掩码之间的软 IoU 损失（Eq. 1），并引入基于 Sinkhorn 算法的最优传输距离（Eq. 2–3），以处理掩码空间分布差异。

2. **HOI 接触对齐**：交替执行两种优化——掩码约束优化与基于接触的 ICP 配准。首先通过 2D 接触区域射线投射确定 3D 接触点候选（Figure 4），然后利用接触点信息对齐手部的全局姿态，使手与物体在接触区域实现几何一致性。

3. **手部参数细化**：联合优化手部的全局姿态 $\phi_h$ 和关节参数 $\theta_h$，目标函数为四项损失的加权组合（Eq. 5）：
   - $\mathcal{L}_{\mathrm{hand-mask}}$：渲染手部掩码与真值掩码的软 IoU 损失（Eq. 4）
   - $\mathcal{L}_{\mathrm{penetr}}$：穿透损失，惩罚手部顶点进入物体内部的深度（Eq. 6）
   - $\mathcal{L}_{\mathrm{contact}}$：接触损失，鼓励手部接触区域靠近物体表面（Eq. 7）
   - $\mathcal{L}_{\mathrm{reg}}$：L1 正则化，防止优化后的姿态偏离 HaMeR 初始估计过远（Eq. 8）

### 关键设计逻辑

该框架的核心洞察在于：**即使单个大型模型的估计存在误差，通过一个联合优化框架统一坐标、对齐接触并细化手部参数，可以生成物理合理的手物交互，且无需额外标注训练数据**。三阶段设计遵循“先全局对齐、再局部接触、最后细节精修”的递进逻辑，每一阶段为下一阶段提供更好的初始化，从而在严重遮挡和几何歧义条件下仍能收敛到合理解。

EasyHOI 的核心由一个**初始重建阶段**和一个**三阶段先验引导优化框架**构成，二者通过可微渲染与物理约束将独立的大型模型输出统一为物理合理的手物交互。

### 初始重建阶段

该阶段利用多个现成的大型模型从单张野外图像中提取手部与物体的初始几何。

1. **分割与修复**：首先使用视觉-语言分割模型 **LISA** 提取手部和物体的掩码。随后，一个**扩散修复模型**移除手部区域，恢复被遮挡的物体完整外观。接着 **SAM** 从修复后的图像中分割出完整物体。
2. **三维重建**：大型重建模型 **InstantMesh** 从单张图像重建物体的三维网格；同时，基于 Transformer 的手部姿态估计器 **HaMeR** 恢复 MANO 手部模型的参数（全局姿态 $\phi_h \in \mathbb{R}^6$ 和关节姿态 $\theta_h \in \mathbb{R}^{45}$）。

此时，物体与手部是在各自独立的坐标系中重建的，缺乏统一的几何参照和物理交互约束。

### 三阶段先验引导优化

优化框架以物体坐标系为全局参考，通过三个阶段逐步对齐手物关系并细化手部参数。

#### 阶段一：相机系统建立

目标是通过优化相机参数，使渲染的物体掩码与修复后的物体掩码在图像空间中对齐。损失函数结合了软 IoU 损失和基于 Sinkhorn 的最优传输损失：

$$
\mathcal{L}_{\mathrm{obj-mask}} = \mathrm{IOU}(M_o^r, \hat{M}_o) = \frac{M_o^r \cdot \hat{M}_o}{|M_o^r| + |\hat{M}_o| - M_o^r \cdot \hat{M}_o}
$$

其中 $M_o^r$ 为可微渲染的物体掩码，$\hat{M}_o$ 为修复后的物体掩码真值。为处理掩码间空间分布差异较大时 IoU 梯度信号弱的问题，引入 Wasserstein 距离：

$$
W(M_{\alpha}, M_{\beta}) = \left( \inf_{\gamma \in \Pi(M_{\alpha}, M_{\beta})} \sum_{i,j} \sum_{k,l} \|(i,j)-(k,l)\|^2 \gamma_{ijkl} \right)^{1/2}
$$

实际使用其 Sinkhorn 近似作为最优传输损失 $\mathcal{L}_{\mathrm{OT}}$，将归一化后的掩码视为离散分布进行匹配。

#### 阶段二：手物接触对齐

在统一相机系统后，该阶段将手部全局姿态与物体对齐。核心机制是**掩码约束优化**与**基于接触区域的 ICP 配准**交替进行：

- 首先通过分析手部与物体掩码的交界区域确定 2D 接触区域。
- 从接触区域像素发射射线，分别与物体和手部几何求交，取极值交点（物体取最近/最远点，手部取掌侧极值点）作为 3D 接触点候选。
- 基于接触点对应关系进行 ICP 配准，调整手部全局姿态。

#### 阶段三：手部参数细化

在接触对齐的基础上，联合优化手部的全局姿态 $\phi_h$ 和关节参数 $\theta_h$，目标函数为四项损失的加权组合：

$$
\mathcal{L}_{\mathrm{hand}} = \lambda_{1} \mathcal{L}_{\mathrm{hand-mask}} + \lambda_{2} \mathcal{L}_{\mathrm{penetr}} + \lambda_{3} \mathcal{L}_{\mathrm{contact}} + \lambda_{4} \mathcal{L}_{\mathrm{reg}}
$$

其中各损失项定义如下：

- **手部掩码损失**（$\mathcal{L}_{\mathrm{hand-mask}}$）：渲染手部掩码 $M_h^r$ 与 LISA 提取的手部掩码 $M_h$ 之间的软 IoU，形式与 $\mathcal{L}_{\mathrm{obj-mask}}$ 一致。
- **穿透损失**（$\mathcal{L}_{\mathrm{penetr}}$）：惩罚手部顶点穿入物体内部的程度。对每个手部顶点 $v$，$d(v)$ 为其到物体表面的有符号距离（内部为负），则：

  $$
  \mathcal{L}_{\mathrm{penetr}} = \frac{1}{N} \sum_{v \in \mathcal{H}} \max(0, -d(v))
  $$

- **接触损失**（$\mathcal{L}_{\mathrm{contact}}$）：鼓励手部接触区域 $\mathcal{H}_C$ 的顶点靠近物体表面，但不穿入：

  $$
  \mathcal{L}_{\mathrm{contact}} = \sum_{v \in \mathcal{H}_C} \max(0, d(v))
  $$

- **正则化损失**（$\mathcal{L}_{\mathrm{reg}}$）：L1 正则化，防止优化后的关节参数 $\theta_h$ 偏离 HaMeR 的初始估计 $\theta_h^0$ 过远：

  $$
  \mathcal{L}_{\mathrm{reg}} = \| \theta_h - \theta_h^0 \|_1
  $$

权重设置为 $\lambda_1=5$，$\lambda_2=10$，$\lambda_3=5$，$\lambda_4=0.1$。消融实验证实，移除 $\mathcal{L}_{\mathrm{penetr}}$ 会导致交叉体积从 4.11 激增至 9.62，移除 $\mathcal{L}_{\mathrm{contact}}$ 使仿真位移从 3.08 升至 3.94，验证了各损失项对物理合理性的关键作用。

![[assets/figures/papers/paper_list_l1732_EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Obj/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the segmentation process after inpainting. (a) Original input image. (b) Hand and object contours, showing the object split into two disconnected regions due to hand occlusion. (c) Inpainted image with the hand region removed. (d) Object segmentation results, consisting of sampled points and a bounding box, used as prompts to segment the inpainted image*

![[assets/figures/papers/paper_list_l1732_EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Obj/figures/004_Figure_4.jpg]]
*Figure 4: Converting 2D contact regions to 3D contact points. Rays emitted from contact mask pixels intersect object and hand geometries. Contact point candidates are constrained to the extremal ray intersections: nearest or farthest points relative to the camera for the object, and palmar-side extremal points for the hand*

## 实验与关键发现

### 零样本物体重建质量

EasyHOI 在三个公开数据集（Arctic、OakInk、DexYCB）上评估了物体重建质量，并与 **AlignSDF**（Zhang et al., CVPR 2024）和 **gSDF**（Ye et al., CVPR 2022）进行零样本比较。由于 AlignSDF 和 gSDF 均在 DexYCB 上训练，为公平起见，DexYCB 上的结果不参与零样本对比。

如 **Table 1** 所示，EasyHOI 在所有数据集上取得了最低的 Chamfer 距离（Arctic 1.089、OakInk 1.035、DexYCB 1.628）和最高的 F-score（F5/F10），表明重建的物体几何与真实物体高度吻合。更重要的是，EasyHOI 在物理合理性指标上显著领先：仿真位移（S.D.）在三个数据集上分别为 2.25 cm、3.08 cm、2.43 cm，交叉体积（I.V.）分别为 4.67 cm³、4.11 cm³、4.52 cm³，均大幅低于基线方法。这一优势源于大型重建模型 InstantMesh 提供的强几何先验，以及后续优化阶段对相机参数和接触关系的精确校准。

![[assets/figures/papers/paper_list_l1732_EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Obj/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation for object quality in HOI reconstruction. Since AlignSDF and gSDF were trained on DexYCB, we exclude their DexYCB results from our zero-shot comparisons. The metrics F5 and F10 measure the F score of points from reconstructed object within 5mm and 10mm of the GT object, respectively. The metric C.D. denotes the Chamfer Distance between reconstructed object and GT object, S.D. denotes Simulation Displacement(in cm) and I.V. represents Intersection Volume(in cm3)*

### 手部姿态精度

手部姿态精度通过 MPVPE（平均每顶点位置误差）和 MPJPE（平均每关节位置误差）评估，结果见 **Table 2**。当使用真实物体几何时，EasyHOI 的 HOI 优化流程能够进一步细化 **HaMeR**（Pavlakos et al., CVPR 2024）的初始估计，MPJPE 从 1.05 cm 降至 0.95 cm。然而，当使用预测的物体几何时，手部结果略差于 HaMeR 单独估计（MPVPE 1.48 cm vs 1.14 cm），这表明物体重建误差会通过耦合优化传播到手部参数估计中，是方法的一个固有限制。

### 三阶段优化的消融分析

**Table 3** 展示了 HOI 优化方案各阶段的消融结果。完整的三个阶段——相机系统设置、HOI 接触对齐、手部参数细化——在所有数据集上均取得最佳效果。移除任一阶段都会导致仿真位移和交叉体积的显著增加。**Figure 5** 通过可视化展示了渐进式改进：初始重建结果存在明显的坐标不对齐和穿透问题；相机设置阶段统一了坐标系；接触对齐阶段使手与物体表面贴合；手部参数细化阶段进一步消除了残留穿透并优化了抓握姿态。

### 手部细化损失项的消融分析

在 OakInk 数据集上对手部参数细化中的四个损失项进行了消融（**Table 4** 和 **Figure 7**）：

![[assets/figures/papers/paper_list_l1732_EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Obj/figures/015_Figure_7.jpg]]
*Figure 7: A visualization of the ablation study on loss terms in hand parameter refinement. Each loss term was individually removed from the total loss function, and hand parameter refinement was performed to observe the resulting effects. The top row shows the input viewpoint, while the bottom row provides an alternative viewpoint to more clearly illustrate the differences*

- **移除穿透损失（L_penetr）** 导致交叉体积从 4.11 cm³ 飙升至 9.62 cm³，这是最关键的损失项，直接约束手部顶点不得进入物体内部。
- **移除正则化损失（L_reg）** 使仿真位移升至 3.24 cm，交叉体积升至 4.47 cm³。缺少 L1 正则化对初始姿态的约束，优化后的手部姿态可能偏离 HaMeR 估计过远，产生不自然的关节角度。
- **移除接触损失（L_contact）** 使仿真位移增至 3.94 cm，表明接触点引导对于维持手物贴合至关重要。
- **移除手部掩码损失（L_hand-mask）** 的影响相对较小，但仍不可忽视，因为它确保了优化后的手部在二维投影上与输入图像保持一致性。

### 定性结果

**Figure 6** 展示了 EasyHOI 在 Arctic、OakInk 和 DexYCB 数据集上的重建结果画廊。方法能够处理多样化的手物交互场景，包括不同抓握类型（捏取、包裹、支撑）和不同物体类别（工具、容器、运动器材）。从相机视角和另一视角的渲染结果可见，重建的 HOI 网格在几何精度和物理合理性之间取得了良好平衡。

### 失败模式与局限性

1. **物体重建误差的传播**：当预测物体几何存在较大误差时，耦合优化会导致手部姿态精度下降，甚至低于 HaMeR 的独立估计。这主要发生在物体被严重遮挡或外观纹理稀少的场景。
2. **严重遮挡下的接触分析退化**：当手指间存在严重自遮挡或手物接触区域在二维图像中不可见时，基于射线投射的 3D 接触点转换（**Figure 4**）可能产生不准确的接触约束，导致手部关节姿态偏离真实值。
3. **计算效率**：方法依赖多个大型预训练模型（LISA、扩散修复、SAM、InstantMesh、HaMeR）和迭代优化，计算成本较高，限制了实时应用场景。

![[assets/figures/papers/paper_list_l1732_EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Obj/figures/009_Table_3.jpg]]
*Table 3: Ablation study for the HOI prior-guided optimization scheme*

## 定位与知识库关联

### 任务定位与核心瓶颈

EasyHOI 面向**单视图野外手物交互重建**，其核心瓶颈在于：单一二维图像固有的严重遮挡与几何歧义、缺乏大规模高质量三维标注数据，以及独立重建手部与物体时坐标系统不一致导致交互关系物理上不合理。现有方法通常依赖特定数据集训练（如 DexYCB），在野外场景泛化能力有限。

### 基线方法谱系

EasyHOI 的对比基线覆盖了物体重建与手部重建两条技术路线：

**物体重建基线：**
- **AlignSDF**（Zhang et al., CVPR 2024）：基于符号距离场的物体重建方法，需在 DexYCB 上训练，零样本泛化能力受限。
- **gSDF**（Ye et al., CVPR 2022）：隐式形状场方法，同样依赖训练数据，在未见场景下表现下降。

**手部重建基线：**
- **HaMeR**（Pavlakos et al., CVPR 2024）：基于 Transformer 的手部姿态估计方法，从单张图像恢复 MANO 参数，是 EasyHOI 手部初始估计的来源，也是手部精度的直接对比对象。

### 关键设计差异（Changed Slots）

EasyHOI 与基线方法的核心差异体现在三个关键改进点上：

| 改进维度 | 基线做法 | EasyHOI 方案 | 证据锚点 |
|---------|---------|-------------|---------|
| **坐标系统** | 手与物体独立重建，坐标不统一 | 统一于物体坐标系，通过可微渲染结合软 IoU 损失与 Sinkhorn 最优传输距离优化相机参数 | Sec 3.4, Camera System Setup |
| **交互对齐** | 无显式交互对齐机制 | 基于接触区域分析的掩码约束优化与 ICP 配准交替进行 | Sec 3.4, HOI Contact Alignment |
| **手部优化损失** | 仅使用掩码损失 | 组合掩码损失、穿透损失、接触损失与正则化损失四项联合优化 | Eq. (5) |

### 方法谱系中的位置

EasyHOI 处于**“预训练大模型先验 + 后优化”**这一新兴范式之中。与端到端学习方法不同，它不依赖手物交互的配对三维标注，而是将多个现成大模型（LISA 分割、扩散修复、InstantMesh 重建、HaMeR 手部估计）作为强先验提供者，再通过一个三阶段优化框架（相机对齐 → 接触对齐 → 手部细化）强制物理一致性与图像一致性。该方法在谱系上可视为**零样本优化驱动方法**，其核心洞察在于：即使各独立模型存在估计误差，联合优化框架能通过统一坐标、对齐接触和细化手部参数来生成物理合理的结果。

### 适用边界与局限

1. **手部精度耦合**：当使用预测的物体几何时，最终手部结果在 MPVPE 指标上略差于 HaMeR 单独估计（Arctic 数据集上 1.48 cm vs 1.14 cm），因为物体重建误差被引入耦合优化中。仅在提供真值物体几何时，HOI 优化才能进一步改善 HaMeR 的初始结果（MPJPE 从 1.05 cm 降至 0.95 cm）。

2. **计算成本**：方法依赖多个大型预训练模型（LISA、扩散修复模型、SAM、InstantMesh、HaMeR）和复杂的多阶段可微渲染优化，计算开销较高，可能不适合实时或低延迟应用场景。

3. **极端姿态鲁棒性**：手部关节的约束主要依赖接触先验和 L1 正则化（防止偏离 HaMeR 初始估计过远），对严重的指间自遮挡或高度非标准的抓握姿态可能不够鲁棒。消融实验表明，去除正则化损失会导致仿真位移和交叉体积同时上升（S.D. 3.24, I.V. 4.47 vs 完整模型 3.08, 4.11）。

4. **零样本泛化边界**：虽然方法在 Arctic、OakInk 和 DexYCB 三个数据集上展现了零样本能力，但其性能上界受限于所依赖大模型各自的能力边界——例如分割模型对复杂纹理物体的处理、修复模型对大面积遮挡的补全质量等。

### 开放问题

1. **大模型专用化**：如何使大型视觉模型更专门地适应手物交互任务，以提高效率和对重度遮挡的鲁棒性？
2. **时序与多手扩展**：能否将框架扩展至处理动态视频或多手交互场景，同时保持时序一致性和物理合理性？
3. **端到端轻量化**：如何减少对多个级联模型的依赖，设计更端到端且轻量的手物交互重建方案，降低计算成本？

## 原文 PDF

![[paperPDFs/CVPR_2025/EasyHOI_Unleashing_the_Power_of_Large_Models_for_Reconstructing_Hand_Object_Interactions_in_the_Wild.pdf]]

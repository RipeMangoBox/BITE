---
title: "Good Can Sometimes be Bad: A Unified Attack against 3D Point Cloud Classifier by a Flexible Isotropic Resampling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Good_Can_Sometimes_be_Bad_A_Unified_Attack_against_3D_Point_Cloud_Classifier_by_a_Flexible_Isotropic_Resampling.pdf
project_link: null
code_link: null
aliases:
- Good_Can_Sometim
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 灵活各向同性重采样（FIR）通过调整射线方向（η, γ）和起始点密度（k），能够生成具有不同点分布的合法化点云。该重采样过程既是后门触发器的注入载体，也是对抗扰动施加的几何约束，其可微性使后门角度优化和对抗梯度更新可以在同一框架内完成，从而在提升点云质量的伪装下实现攻击。
primary_logic: 将恶意扰动伪装成点云质量提升（即各向同性重采样），打破了攻击隐蔽性与扰动幅度之间的强耦合。利用可调参数的射线重采样框架，既允许在后门攻击中通过优化射线方向来学习统一的触发器特征，又允许在对抗攻击中沿射线方向施加受约束的梯度扰动，从而统一后门注入与对抗样本生成，并实现对动态权限的适应性。
claims:
- UAtt3D在ModelNet40上实现了接近最优的ASR（>96%），同时CUD和KUV指标大幅优于所有对比攻击，表明方法在确保攻击有效性的同时显著提高了点云质量（各向同性）。
- 在人类主观检查中，被UAtt3D攻击的点云被选为最自然的比例高达80.62%，远高于良性点云的19.31%，证明该攻击能有效规避人工审查。
- 在显著性防御下，UAtt3D的后门ASR几乎保持不变，而PointBA‑I的ASR从接近100%骤降至15.13%，突出其攻击模式对基于显著性点的防御具有内在鲁棒性。
- 在STRIP防御下，UAtt3D的后门样本分布与良性样本分布重叠更大，优于PointPBA-I，进一步显示了其隐蔽性和反防御能力。
---

# Good Can Sometimes be Bad: A Unified Attack against 3D Point Cloud Classifier by a Flexible Isotropic Resampling

> [!tip] 核心洞察
> 将恶意扰动伪装成点云质量提升（即各向同性重采样），打破了攻击隐蔽性与扰动幅度之间的强耦合。利用可调参数的射线重采样框架，既允许在后门攻击中通过优化射线方向来学习统一的触发器特征，又允许在对抗攻击中沿射线方向施加受约束的梯度扰动，从而统一后门注入与对抗样本生成，并实现对动态权限的适应性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 好事有时变坏事：基于灵活各向同性重采样的统一3D点云分类器攻击 |
| 英文题名 | Good Can Sometimes be Bad: A Unified Attack against 3D Point Cloud Classifier by a Flexible Isotropic Resampling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Fan_Good_Can_Sometimes_be_Bad_A_Unified_Attack_against_3D_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UAtt3D |
| Dataset | ModelNet40, Human inspection survey, ScanObjectNN |

> [!tip] 效果简介
> - ModelNet40 (backdoor) 上，ASR (PointConv / PointNet++ / DGCNN / CurveNet) 97.62 / 98.94 / 96.03 / 99.91 vs PointBA-I 可达到 100（但隐蔽性极差） (ASR 处于领先水平，同时隐蔽性全面占优)；点云各向同性 - CUD / KUV 62.27 / 0.33 (all models) vs 传统攻击的 CUD/KUV 明显更高 (大幅改善（值越低越好）)。
> - ModelNet40 (untargeted adversarial, PointConv / PointNet++) 上，ASR 100 / 100 vs 其他对抗攻击的 ASR（未列出具体值） (达到最优)。
> - Human inspection survey 上，被选为最自然的比例 (human preference rate) 80.62% vs 良性点云 19.31% (+61.31%)。

## 概要

### 问题背景与瓶颈

3D点云分类器在自动驾驶、机器人等安全关键场景中日益普及，但其安全性研究长期处于“攻防割裂”状态：**对抗攻击**（推理阶段施加扰动以诱导误分类）与**后门攻击**（训练阶段植入触发器以实现隐蔽控制）被分别设计，各自依赖不同的扰动策略与权限假设。这种分离导致两大瓶颈：

1. **权限适应性不足**：实际部署中攻击者的权限是动态变化的——可能从训练阶段的后门注入切换到推理阶段的对抗扰动，现有方法无法在统一框架下同时应对。
2. **隐蔽性-攻击强度的强耦合**：为保证攻击不被察觉，现有方法普遍采用限制扰动幅度（如ℓ∞/ℓ2约束）的策略，但这不仅牺牲了攻击强度，还会引入非均匀、不可控的异常点，反而降低了点云质量，增加了暴露风险。

### 核心思路：以“质量提升”掩盖“恶意行为”

UAtt3D的核心洞察在于**打破隐蔽性与扰动幅度的绑定关系**——与其通过“降低质量”来隐藏攻击，不如通过“提升质量”来伪装攻击。具体而言，UAtt3D提出**灵活各向同性重采样（Flexible Isotropic Resampling, FIR）**，将恶意扰动伪装成点云质量提升的过程：

- FIR通过从三个正交平面发射平行射线，与近似表面网格求交，生成分布均匀、各向同性的重采样点云。
- 通过调节射线方向参数（η, γ）和起始点密度（k），FIR可灵活控制点分布，生成多种合法化的点云形态。
- **整个重采样过程保持可微**，使得后门触发器的优化（通过梯度下降寻找最优射线方向）和对抗扰动的施加（沿射线方向投影梯度）可以在同一框架内完成。

这一设计使得UAtt3D成为**首个同时支持后门攻击与对抗攻击的统一框架**：后门攻击通过优化射线方向来学习统一的触发器特征；对抗攻击则沿射线方向施加受约束的梯度扰动，在保持点位于几何表面附近的前提下误导分类器。

### 方法定位与知识库坐标

在3D点云攻击方法谱系中，UAtt3D的定位可从三个维度刻画：

| 维度 | 传统方法 | UAtt3D |
|------|----------|--------|
| **隐蔽性实现方式** | 限制扰动幅度（ℓ∞/ℓ2约束），导致非均匀异常点 | 通过各向同性重采样提升点云质量，扰动表现为规则化点位置调整 |
| **重采样灵活性** | 基于几何特征（如曲率）的固定重采样，输出高度相似 | 基于可调参数（η, γ, k）的射线重采样，可生成多种点分布 |
| **攻击框架** | 对抗攻击与后门攻击分开设计，需特定权限 | 统一在FIR框架下完成，支持动态权限场景 |

与典型基线对比：
- **后门攻击方面**：相比PointBA（Li et al., ICCV 2021）、PCBA（Xiang et al., ICCV 2021）、IRBA（Gao et al., TIFS 2024）、NRBdoor/IBAPC（Fan et al., AAAI 2024）等方法，UAtt3D在保持竞争性攻击成功率的同时，点云各向同性指标（CUD/KUV）大幅占优。
- **对抗攻击方面**：相比GeoA3（Wen et al., TPAMI 2020）、AdvPC（Hamdi et al., ECCV 2020）、SIA（Huang et al., CVPR 2022）、HiT（Lou et al., CVPR 2024）等方法，UAtt3D在非目标攻击下达到100%攻击成功率，且生成的点云更自然。

### 主要结果概览

UAtt3D在多个维度验证了其有效性、隐蔽性与鲁棒性：

- **攻击有效性**：在ModelNet40上针对PointConv/PointNet++/DGCNN/CurveNet的后门攻击成功率（ASR）分别达97.62%/98.94%/96.03%/99.91%；非目标对抗攻击ASR达100%。
- **隐蔽性**：点云各向同性指标CUD和KUV显著优于所有对比攻击；人类主观检查中，UAtt3D攻击点云被选为“最自然”的比例高达80.62%（良性点云仅19.31%）。
- **防御鲁棒性**：在显著性点过滤防御下，UAtt3D的后门ASR几乎不变，而PointBA-I的ASR从接近100%骤降至15.13%；在STRIP防御下，UAtt3D样本分布与良性分布高度重叠，优于PointPBA-I。
- **真实数据适应性**：在包含噪点、孔洞、稀疏等缺陷的点云及ScanObjectNN真实扫描数据上，UAtt3D仍保持高有效性与强隐蔽性。

> **注意**：UAtt3D的单样本生成时间约0.528秒，慢于iBA（0.463s）、PCBA（0.493s）和IBAPC（0.381s），且针对自适应防御（如PointCVaR）的对抗攻击ASR会从95.78%降至78.42%，表明计算效率与极端防御下的鲁棒性仍有提升空间。

### 3D点云分类器的安全威胁：后门攻击与对抗攻击

深度神经网络在3D点云分类任务中取得了显著成功，但其安全性正面临两类典型攻击的严峻挑战。**后门攻击**通过在训练阶段注入带有特定触发器（trigger）的样本，使受害模型在推理时对包含该触发器的输入错误地输出攻击者指定的目标标签，而对良性样本的分类性能几乎不受影响。其训练目标可形式化为：

$$\operatorname*{min}_{\theta} \sum_{P \in D_{clean}} L(F(P,\theta), y) + \sum_{P \in D_{backdoor}} L(F(T(P),\theta), y^{t})$$

其中 $T(\cdot)$ 为触发器植入函数，$y^{t}$ 为攻击者指定的目标标签。**对抗攻击**则发生在推理阶段，攻击者对输入点云施加精心构造的微小扰动 $A(\cdot)$，使得分类器输出与正确标签不一致：

$$F(A(P),\theta) \neq y$$

现有工作针对这两类威胁分别设计了专门的攻击方法。后门攻击方面，**PointBA**（Li et al., ICCV 2021）、**PCBA**（Xiang et al., ICCV 2021）、**IRBA**（Gao et al., TIFS 2024）、**NRBdoor**和**IBAPC**（Fan et al., AAAI 2024）等方法通过不同的几何变换或点插入策略植入触发器；对抗攻击方面，**GeoA3**（Wen et al., TPAMI 2020）、**AdvPC**（Hamdi et al., ECCV 2020）、**SIA**（Huang et al., CVPR 2022）、**HiT**（Lou et al., CVPR 2024）、**SS-Attack**（Zhang et al., Information Sciences 2024）和**Eidos**（Sicre et al., DEPENDABLE SOFTWARE ENGINEERING 2025）等方法通过约束扰动幅度来生成对抗样本。

### 核心瓶颈：攻击隐蔽性与有效性的矛盾

现有3D攻击方法面临一个根本性困境：**攻击隐蔽性与攻击有效性之间存在强耦合**。为保证攻击不被察觉，现有方法普遍采用限制扰动幅度的策略（如 $\ell_{\infty}$ 或 $\ell_2$ 约束），但这种“降低点云质量以换取隐蔽性”的做法带来了两个关键问题：

1. **隐蔽性本身难以保证**：幅度约束本质上是对失真程度的限制，而非对攻击痕迹的消除。在3D点云中，即使扰动幅度很小，也可能产生非均匀、不可控的异常点分布，在人类视觉或自动检测下暴露攻击痕迹。

2. **攻击强度受到制约**：严格的扰动幅度限制直接压缩了攻击空间，使得攻击者难以在隐蔽性约束下实现高成功率的攻击，尤其是在需要兼顾特征移动（对抗攻击）和特征学习（后门攻击）的统一场景中。

### 统一攻击的缺失：权限动态变化带来的新挑战

更关键的是，现有后门攻击和对抗攻击被**割裂设计**，使用完全不同的触发器、扰动生成策略和优化目标。然而，在实际部署环境中，攻击者的权限往往是**动态变化**的——攻击者可能在训练阶段拥有数据投毒权限（可实施后门攻击），也可能仅在推理阶段拥有输入修改权限（可实施对抗攻击），甚至可能在不同时间点拥有不同级别的权限。现有的“分而治之”范式无法适应这种权限的动态切换，缺乏一个能够在不同权限级别下统一运作的攻击框架。

### 本文动机：以“质量提升”伪装“恶意行为”

针对上述瓶颈，本文提出了一种全新的攻击范式：**将恶意扰动伪装成点云质量提升**。核心洞察在于，如果攻击行为在几何上表现为对点云的各向同性重采样（isotropic resampling）——一种通常被视为点云预处理或质量增强的操作——那么攻击不仅不会降低点云质量，反而会使其在视觉和统计指标上显得更加“自然”和“规则”。这一思路从根本上打破了隐蔽性与扰动幅度之间的强耦合：攻击不再依赖“少做坏事”，而是通过“做好事”来掩盖“坏事”。

基于这一动机，本文设计了**灵活各向同性重采样（Flexible Isotropic Resampling, FIR）**，并将其作为统一攻击框架 **UAtt3D** 的核心机制。FIR通过可调参数（射线方向 $\eta, \gamma$ 和起始点密度 $k$）控制重采样点的分布，既可作为后门触发器的注入载体（通过优化射线方向学习统一的触发器特征），也可作为对抗扰动的几何约束（沿射线方向施加梯度扰动），从而在统一框架下同时支持后门注入与对抗样本生成，并自适应于攻击者权限的动态变化。

## 核心方法与创新机理

### 问题瓶颈：隐蔽性-扰动幅度的强耦合与攻击权限的割裂

现有3D点云攻击方法面临两个根本性瓶颈。第一，**攻击隐蔽性与扰动幅度之间存在强耦合**：无论是基于ℓ∞/ℓ2约束的对抗攻击（如**GeoA3** (Wen et al., TPAMI 2020)、**AdvPC** (Hamdi et al., ECCV 2020)、**SIA** (Huang et al., CVPR 2022)）还是后门攻击（如**PointBA** (Li et al., ICCV 2021)、**PCBA** (Xiang et al., ICCV 2021)），都通过限制扰动幅度来减小失真，但这会引入非均匀、不可控的异常点，反而降低了点云的自然性。第二，**对抗攻击与后门攻击被分开设计**，使用不同的触发器或扰动生成策略，需要特定的攻击权限，无法适应实际部署环境中攻击者权限的动态变化——当攻击者从训练阶段（后门注入权限）切换到推理阶段（对抗扰动权限）时，需要两种完全不同的攻击机制。

### 核心洞察：将恶意扰动伪装成点云质量提升

UAtt3D的核心创新在于**打破了隐蔽性与扰动幅度之间的强耦合**，开辟了一条全新的隐蔽性实现路径：**通过提升点云质量来隐藏攻击，而非降低点云质量**。具体而言，该方法将恶意扰动伪装成一种各向同性重采样（isotropic resampling）操作，使攻击后的点云在几何上表现为规则化、均匀分布的点位置调整，从而在提升点云各向同性指标的同时完成攻击注入。这一设计使攻击行为（bad thing）被点云质量提升（good thing）所掩盖，从根本上改变了攻击隐蔽性的实现逻辑。

### 关键技术：灵活各向同性重采样（FIR）

为实现上述洞察，论文设计了**灵活各向同性重采样（Flexible Isotropic Resampling, FIR）**，这是UAtt3D统一攻击框架的基础算子。FIR的核心机制如下：

**射线驱动的可微重采样。** FIR从三个正交的起始点平面发射平行射线，计算射线与近似三角网格的交点作为重采样点。通过调节射线方向参数——极角η和方位角γ——以及起始点密度k，可以生成具有不同点分布的重采样点云。关键的是，整个重采样过程保持可微，使得后门角度优化和对抗梯度更新可以在同一框架内完成。

**双模式攻击的统一载体。** 在后门攻击模式下，利用FIR的可微性，通过梯度下降优化射线方向(η*, γ*)，使得代理模型在重采样点云上的特征趋向目标类别，从而学习统一的触发器特征；在对抗攻击模式下，在重采样点云上计算分类损失梯度，将梯度分解为自由扰动分量和沿射线方向的投影分量，每次移动由这两个向量合成，迭代直到误导分类器，同时保持点位于几何表面附近。这两种模式共享同一个FIR框架，实现了对动态权限场景的适应性。

### 与Baseline的核心差异

| 创新维度 | 现有方法 | UAtt3D |
|---------|---------|--------|
| **隐蔽性实现方式** | 限制扰动幅度（ℓ∞/ℓ2约束），引入非均匀异常点 | 提升点云质量（各向同性重采样），扰动表现为规则化点位置调整 |
| **重采样灵活性** | 基于几何特征（如曲率）的固定重采样，输出高度相似 | 基于可调参数(η, γ, k)的射线重采样，可生成多种点分布 |
| **攻击框架** | 对抗攻击与后门攻击分开设计，需特定权限 | 统一在FIR框架下完成，支持动态权限场景 |

这一创新范式的有效性得到了充分验证：在ModelNet40上，UAtt3D的后门攻击成功率（ASR）达到97.62%~99.91%（Table 1），同时点云各向同性指标CUD和KUV大幅优于所有对比攻击；在人类主观检查中，被UAtt3D攻击的点云被选为最自然的比例高达80.62%，远高于良性点云的19.31%（Figure 5），证明该攻击能有效规避人工审查。

UAtt3D 的核心设计思想是将恶意攻击行为伪装成点云质量的提升，从而在统一的框架下同时支持后门攻击与对抗攻击。如图2所示，整个pipeline由四个关键模块串联构成，形成从原始点云到攻击样本的端到端可微流程。

**输入与输出流**：系统接收良性点云 `P_Benign` 作为输入。首先通过**表面近似**模块从可能包含噪点、孔洞或稀疏缺陷的原始点云中快速重建出近似的三角网格表面；随后，**灵活各向同性重采样（FIR）** 模块在该近似表面上发射平行射线，生成具有均匀点分布的重采样点云 `P_Resample`。这一重采样过程由三个可调超参数——射线极角 `η`、方位角 `γ` 以及起始点密度 `k`——灵活控制点的空间排列。在推理阶段，根据攻击者当前权限的不同，系统分叉为两条路径：若执行**基于FIR的对抗攻击**，则在 `P_Resample` 上沿射线方向施加受几何约束的梯度扰动，生成对抗样本 `P_Adv`；若执行**基于FIR的后门攻击**，则利用可微的FIR通过梯度下降优化射线方向 `(η*, γ*)`，将重采样本身转化为统一的触发器注入机制，生成后门样本 `P_Backdoor`。

**模块间的因果耦合**：FIR模块是整个框架的“因果旋钮”。其可微性使得后门攻击中的触发器学习（优化射线方向以最小化代理损失）与对抗攻击中的特征移动（沿射线方向施加梯度扰动）可以在同一几何约束下完成。表面近似模块为FIR提供了必要的碰撞表面，而FIR输出的各向同性点云则为后续两种攻击提供了高质量的伪装基底——攻击扰动在几何上表现为规则化、均匀分布的点位置调整，而非传统方法中引入的非均匀异常点，从而打破了攻击隐蔽性与扰动幅度之间的强耦合。

![[assets/figures/papers/paper_list_l2257_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_Good_Can_Sometimes/figures/001_Figure_1.jpg]]
*Figure 1: The proposed UAtt3D can adapt to backdoor attack and adversarial attack at the same time. The malicious behavior (bad thing) is covered by the point cloud quality improvement (good thing) powered by the designed flexible isotropic resampling (FIR), instead of quality decrease like existing attacks*

UAtt3D 的统一攻击能力建立在**灵活各向同性重采样（Flexible Isotropic Resampling, FIR）** 之上。FIR 将攻击行为伪装成点云质量提升，同时为后门注入和对抗扰动提供可微的操作空间。整个框架由四个核心模块串联构成。

### 模块一：表面近似（Surface Approximation）

FIR 需要射线与物体表面求交以确定重采样点的位置。为在不依赖水密网格的前提下实现这一点，UAtt3D 采用改进的 Alpha Shapes 算法对输入点云进行凹壳重建，生成可能交叉重叠的三角网格。该步骤包含两个关键设计：(1) 引入离群点去除以提升点云平滑度；(2) 采用自适应半径的球形搜索，使方法能够容忍原始点云中的噪声、孔洞和稀疏等缺陷。最终得到的三角网格仅用于射线碰撞检测，不要求几何精度。

### 模块二：灵活各向同性重采样（FIR）

FIR 是整个攻击的几何载体。其核心思想是从三个相互正交的起始平面发射平行射线，计算射线与三角网格的交点作为重采样点，从而将任意点云映射为具有各向同性分布的新点云。

设点云的外接球面上一点用极坐标表示为：

$$p_{c} = (\eta_{c}, \gamma_{c}, r)$$

其中 $\eta_{c}$ 为极角，$\gamma_{c}$ 为方位角，$r$ 为外接球半径。该点确定了一个切平面，在切平面上以均匀间距 $d$ 布置射线起始点：

$$p_{s} = p_{c} + d \cdot u + d \cdot v$$

其中 $u$ 和 $v$ 为切平面内的一对正交方向向量。三个正交起始平面各自发射平行的射线束，射线方向由 $(\eta, \gamma)$ 参数化，起始点密度由参数 $k$ 控制。整个重采样过程可表示为：

$$P_{Resample} = T(P_{Benign}, \eta_{c}, \gamma_{c}, k)$$

**关键性质**：通过调节 $(\eta, \gamma)$ 和 $k$，FIR 可以为同一输入生成具有不同点分布的重采样点云。更重要的是，射线与三角网格的求交运算保持了端到端的可微性，使得后续的后门角度优化和对抗梯度更新可以在同一框架内完成。

### 模块三：基于 FIR 的对抗攻击

在对抗攻击场景下，攻击者以误导分类器为目标：

$$F(A(P), \theta) \neq y$$

UAtt3D 的对抗扰动施加在 FIR 重采样后的点云上。每次迭代中，首先计算分类损失关于重采样点云的梯度向量 $\vec{r}$，然后将该梯度分解为两个分量：(1) 自由扰动分量，允许点在表面附近移动；(2) 沿射线方向的投影分量 $\vec{s} \cdot t_s$，其中 $\vec{s}$ 为梯度 $\vec{r}$ 在采样射线方向上的投影。每个重采样点的单步移动由这两个向量合成。迭代过程持续进行，直到 $P_{Resample}$ 被分类器误分类为止。

这一设计的核心优势在于：扰动被约束在几何表面附近，且点云在重采样后本身已具备各向同性，因此对抗样本在视觉上表现为规则、均匀的点分布，而非传统攻击中常见的异常离散点。

### 模块四：基于 FIR 的后门攻击

后门攻击的目标是让受害模型在训练阶段学习从触发器到目标标签 $y^t$ 的映射：

$$\operatorname*{min}_{\theta} \sum_{P \in D_{clean}} L(F(P,\theta), y) + \sum_{P \in D_{backdoor}} L(F(T(P),\theta), y^{t})$$

UAtt3D 将 FIR 本身作为后门触发器 $T(\cdot)$。与固定触发器不同，FIR 的射线方向 $(\eta, \gamma)$ 是可学习的。攻击者利用可微的 FIR，在代理模型 $F_s(\cdot, \theta_s)$ 上通过梯度下降优化射线方向，使重采样点云的特征向目标类别靠拢：

$$\eta^{*}, \gamma^{*} = \operatorname*{argmin}_{(\eta,\gamma), P\in\mathcal{D}_{clean}} \sum L(F_{s}(T(P,\eta,\gamma),\theta_{s}), y^{t})$$

优化得到的最优角度 $(\eta^{*}, \gamma^{*})$ 即为统一的触发器参数。在训练阶段，攻击者将投毒样本（经 FIR 以 $(\eta^{*}, \gamma^{*})$ 重采样后的点云）注入受害模型的训练集，使模型将这种特定的重采样模式与目标标签关联。在推理阶段，任意测试样本经过相同参数的 FIR 重采样后即可触发后门。

### 统一性分析

上述四个模块揭示了 UAtt3D 统一后门攻击与对抗攻击的因果机制：

- **共享的几何载体**：FIR 同时充当后门触发器和对抗扰动的施加空间，避免了分别设计触发器和扰动生成策略的需要。
- **可微性桥梁**：FIR 的可微性使后门角度优化（通过梯度下降在代理模型上搜索最优射线方向）和对抗梯度更新（沿射线方向施加约束扰动）共享同一计算图。
- **隐蔽性解耦**：传统攻击通过限制扰动幅度来保证隐蔽性，这直接限制了攻击强度。UAtt3D 转而通过提升点云质量（各向同性重采样）来隐藏攻击，打破了隐蔽性与扰动幅度之间的强耦合，使攻击者在动态权限场景下可以灵活切换或组合两种攻击模式。

![[assets/figures/papers/paper_list_l2257_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_Good_Can_Sometimes/figures/003_Figure_3.jpg]]
*Figure 3: The designed adversarial attack based on FIR. One adversarial movement consists of loss gradient vector ⃗r and ray projection vector*

## 实验与关键发现

### 主要结果

**后门攻击有效性。** 在 ModelNet40 上，UAtt3D 针对四种受害模型均取得了极具竞争力的攻击成功率（ASR）：PointConv 97.62%、PointNet++ 98.94%、DGCNN 96.03%、CurveNet 99.91%（Table 1）。与 PointBA‑I 等可达到接近 100% ASR 的基线相比，UAtt3D 在攻击有效性上处于同一领先水平，但其隐蔽性优势是传统攻击无法企及的。

**隐蔽性的量化突破。** 传统攻击为追求隐蔽性通常限制扰动幅度，这反而导致点云各向同性恶化。UAtt3D 则通过提升点云质量来隐藏攻击：在 ModelNet40 上，其 CUD 指标降至 62.27，KUV 降至 0.33，在所有对比攻击中大幅领先（Table 1，值越低表示各向同性越好）。这一优势在定性可视化中同样显著——UAtt3D 生成的攻击点云在视觉上比良性点云更自然（Figure 4）。

**人类主观检验的压倒性优势。** 在线问卷调查显示，被 UAtt3D 攻击的点云被参与者选为“最自然”的比例高达 80.62%，而良性点云仅为 19.31%（Figure 5）。这意味着攻击样本不仅没有被察觉，反而比原始数据更受人类观察者信任，证明了“以提升质量掩盖恶意”这一范式的有效性。

**对抗攻击性能。** 在非目标对抗攻击设置下，UAtt3D 在 ModelNet40 上针对 PointConv 和 PointNet++ 均达到 100% ASR（Table 2），同时保持优异的各向同性指标，表明统一的 FIR 框架在对抗攻击场景下同样高效。

**真实缺陷数据的鲁棒性。** 在 ScanObjectNN 真实扫描数据上，UAtt3D 的后门 ASR 达到 97.66%（PointNet++），显著优于传统攻击（Table 3, Table 4）。即使在合成加入离群点、孔洞、稀疏等缺陷的 ModelNet40 上，UAtt3D 仍保持有竞争力的攻击效果和点云质量提升（Table 3），显示出对真实世界数据缺陷的强适应性。

### 防御鲁棒性分析

**显著性防御。** 基于显著性点删除的防御对 UAtt3D 几乎无效——删除前 60 个显著点后，其后门 ASR 基本保持不变，而 PointBA‑I 的 ASR 从接近 100% 骤降至 15.13%（Figure 7）。这是因为 UAtt3D 的触发器通过 FIR 均匀分布在点云表面，不依赖于少数异常显著点。

**STRIP 防御。** 在 STRIP 检测下，UAtt3D 后门样本的熵分布与良性样本高度重叠，重叠程度明显大于 PointPBA‑I（Figure 8），表明其攻击模式能有效规避基于预测熵的检测。

**频率过滤防御。** 基于频率的过滤方法对 UAtt3D 影响极小：ASR 仅从 98.77% 降至 98.29%，而 IBAPC 和 PointBA‑I 分别降至 25.31% 和 4.33%。UAtt3D 的扰动在频域上不产生可检测的异常模式，隐蔽性内在更强。

**自适应防御的挑战。** 尽管 UAtt3D 对多种通用防御表现出强鲁棒性，但针对性的 PointCVaR 净化能够将对抗攻击 ASR 从 95.78% 降至 78.42%。这说明当防御方采用与攻击机理相匹配的自适应策略时，UAtt3D 仍存在一定失效风险，这一边界值得进一步研究。

### 消融实验

**目标标签敏感性。** UAtt3D 的攻击性能对目标标签 $y^t$ 的变化不敏感，无论选择哪个类别作为后门目标，均可达到优异的 ASR（Figure 9a），表明 FIR 学习的触发器特征具有跨类别的泛化注入能力。

**投毒率控制。** 增加投毒率 $\alpha$ 会单调提升后门 ASR（Figure 9b），验证了攻击强度可通过训练数据污染比例灵活控制，且不需要高投毒率即可达到高 ASR。

**网格重构质量。** 从 UAtt3D 攻击点云重构的三角网格能够避免孔洞出现，其面片法向一致性（16.48）优于从良性点云重构的网格（23.15）（Figure 10）。这进一步佐证了 FIR 重采样在提升表面几何质量方面的客观效果。

### 效率与局限性

**时间开销。** UAtt3D 生成单个样本的平均耗时为 0.528 秒，慢于 iBA（0.463s）、PCBA（0.493s）和 IBAPC（0.381s），但仍处于可接受范围。效率瓶颈主要在于表面近似和射线求交计算，是未来优化的重点方向。

**评估范围。** 当前实验覆盖 ModelNet40、ShapeNet16、ScanObjectNN 三个数据集和 PointConv、PointNet++、DGCNN、CurveNet 四个分类器，对分割、检测等其他 3D 任务的泛化性尚未验证。此外，人类检查实验通过在线问卷进行，参与者的专业背景和显示设备差异可能引入偏差，该结论需谨慎推广。

![[assets/figures/papers/paper_list_l2257_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_Good_Can_Sometimes/figures/004_Table_1.jpg]]
*Table 1: Performance of our UAtt3D for backdoor attack. The best is in bold, and the second best is underlined. CUD and KUV represent the isotropy of 3D point cloud. Lower is better. The proposed UAtt3D achieves competitive ASR and BAc comparing with existing adversarial & backdoor attacks. Furthermore, its promotion on point cloud quality is outstanding*

![[assets/figures/papers/paper_list_l2257_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_Good_Can_Sometimes/figures/006_Figure_5.jpg]]
*Figure 5: One example of our human inspection experiment*

![[assets/figures/papers/paper_list_l2257_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_Good_Can_Sometimes/figures/007_Figure_4.jpg]]
*Figure 4: Attacked 3D point cloud. Our UAtt3D promises stealthiness by improving its quality. Its naturalness is more conducive to evading the defender’s observation, compared with previous attacks. More instances are shown in Appendix 7.2*

![[assets/figures/papers/paper_list_l2257_https_openaccess_thecvf_com_content_CVPR2026_html_Fan_Good_Can_Sometimes/figures/010_Table_4.jpg]]
*Table 4: Advantages of UAtt3D on SON with Backdoor Attack*

## 定位与知识库关联

### 1. 问题瓶颈与现有方法谱系

3D点云深度学习面临两类主要攻击威胁：**对抗攻击**（推理阶段施加微小扰动以误导分类器）与**后门攻击**（训练阶段注入触发器，使模型在测试时对含触发器的样本输出目标标签）。现有方法在这两条路径上独立发展，形成了各自的方法谱系，但存在三个结构性缺陷：

**（1）权限假设的割裂。** 对抗攻击默认攻击者仅能访问测试样本（黑盒或白盒查询），而后门攻击要求攻击者能污染训练数据或控制训练过程。实际部署环境中攻击者的权限往往是动态变化的，单一攻击无法覆盖从训练到推理的全生命周期威胁。

**（2）隐蔽性策略的瓶颈。** 现有攻击几乎全部采用“限制扰动幅度”的策略来保证隐蔽性——对抗攻击通过 ℓ∞ 或 ℓ2 范数约束扰动大小，后门攻击则试图使用微小几何形变（如 **PointBA** (Li et al., ICCV 2021)、**PCBA** (Xiang et al., ICCV 2021)、**IRBA** (Gao et al., TIFS 2024)、**NRBdoor** (Fan et al., AAAI 2024)、**IBAPC** (Fan et al., AAAI 2024)）或特征空间扰动来隐藏触发器。然而，这种“压制扰动”的策略存在内在矛盾：扰动幅度越小，攻击强度越受限；且对点云施加非均匀的小扰动反而会引入不可控的异常点分布，破坏点云的几何一致性，在主观审查下反而更易暴露。

**（3）攻击机制的不兼容。** 对抗攻击需要沿梯度方向移动点特征以跨越决策边界（特征移动），而后门攻击需要学习一个能将任意样本映射到目标类别的触发器特征（特征学习）。现有方法分别设计扰动生成策略和触发器植入策略，缺乏统一框架来同时兼顾这两种需求。

### 2. UAtt3D的方法定位与变更槽

UAtt3D的核心创新在于**将攻击行为伪装成点云质量提升**，从而在方法谱系中开辟了一条新路径。下表总结了其相对于现有方法的关键“变更槽”（changed slots）：

| 维度 | 现有方法基线 | UAtt3D方案 | 变更逻辑 |
|------|-------------|-----------|---------|
| **隐蔽性实现方式** | 通过限制扰动幅度（ℓ∞/ℓ2约束）减小失真，但引入非均匀异常点 | 通过提升点云质量（各向同性重采样）隐藏攻击，扰动表现为规则化、均匀分布的点位置调整 | 打破“隐蔽性=低扰动”的强耦合，利用“质量提升”作为攻击载体 |
| **重采样灵活性** | 基于几何特征（如曲率）的固定重采样，对给定输入输出高度相似的分布 | 基于可调参数（η, γ, k）的射线重采样，可生成多种点分布，支持后门特征学习与对抗特征移动 | 将重采样从固定几何操作变为可微的可控参数化过程 |
| **攻击框架** | 对抗攻击与后门攻击分开设计，使用不同策略，需特定权限 | 统一在FIR框架下：后门攻击优化射线方向以最小化代理损失，对抗攻击沿射线方向施加梯度扰动 | 实现训练-推理全生命周期的统一攻击，适应动态权限 |

**方法定位：** UAtt3D属于“伪装型统一攻击”（stealth-by-quality unified attack），其技术路线不同于现有的任何单一对抗或后门攻击。在对抗攻击谱系中，它区别于 **GeoA3** (Wen et al., TPAMI 2020)、**AdvPC** (Hamdi et al., ECCV 2020)、**SIA** (Huang et al., CVPR 2022)、**HiT** (Lou et al., CVPR 2024)、**SS-Attack** (Zhang et al., Information Sciences 2024)、**Eidos** (Sicre et al., DEPENDABLE SOFTWARE ENGINEERING 2025) 等基于梯度扰动或几何变形的方案；在后门攻击谱系中，它区别于 PointBA、PCBA、IRBA、NRBdoor、IBAPC 等基于点级触发器或特征空间注入的方案。

### 3. 适用边界与条件依赖

UAtt3D的有效性依赖以下前提条件：

- **表面可近似性：** FIR模块使用改进的Alpha Shapes进行表面近似，要求输入点云能形成有意义的几何表面。对于极度稀疏、碎片化或完全无序的点云，表面近似质量下降将影响重采样的各向同性和攻击隐蔽性。
- **代理模型可用性：** 后门攻击阶段需要代理模型来优化射线方向（η*, γ*），其性能依赖于代理模型与受害者模型的特征空间相似性。实验验证基于PointConv/PointNet++/DGCNN/CurveNet等主流架构，对架构差异极大的受害者模型的迁移性需进一步验证。
- **数据集规模与类别分布：** 实验在ModelNet40（40类）、ShapeNet16（16类）和ScanObjectNN（15类）上进行，类别数中等。在更大规模类别空间下，后门触发器与目标类别的特征绑定可能面临更多干扰。

### 4. 局限性分析

**（1）计算效率。** UAtt3D生成单个攻击样本的平均时间约为0.528秒，虽然仍在可接受范围，但慢于IBAPC (0.381s)、iBA (0.463s) 和 PCBA (0.493s)。时间开销主要来自Alpha Shapes表面近似和射线-网格求交计算，在实时或大规模攻击场景下可能成为瓶颈。

**（2）对抗净化防御的脆弱性。** 尽管UAtt3D对多种通用防御（显著性过滤、STRIP、频率过滤）表现出强鲁棒性——例如显著性防御下后门ASR几乎不变，而PointBA-I从接近100%骤降至15.13%——但针对性的PointCVaR净化能够将对抗攻击ASR从95.78%降至78.42%。这表明在强自适应防御下，基于表面重采样的攻击模式仍存在可被检测和净化的特征痕迹。

**（3）任务与模型泛化性未验证。** 实验主要基于三个分类数据集和四个分类器，对3D点云分割、目标检测、场景理解等任务的泛化性尚未探索。FIR框架的可微性理论上支持扩展到其他任务，但需要验证在这些任务中“各向同性”是否仍能有效伪装攻击。

**（4）主观评估偏差。** 人类检查实验通过在线问卷进行，参与者背景（是否具备3D视觉专业经验）和显示设备（2D屏幕渲染3D点云）可能导致偏差。80.62%的自然度偏好率需要在更受控的3D可视化环境下复现验证。

### 5. 开放问题

1. **效率优化路径：** 能否通过预计算射线-网格碰撞表、GPU并行化射线求交、或采用更轻量的隐式表面表示（如神经隐式场）来显著降低FIR的计算开销，使其满足实时攻击需求？

2. **跨模态范式迁移：** “通过质量提升来掩盖攻击”的核心思想能否推广到2D图像（如通过超分辨率或去噪来隐藏对抗扰动）、文本（如通过语法优化来隐藏后门触发器）或多模态模型，形成跨数据格式的统一攻击框架？这需要重新定义各模态下的“质量”指标及其可微实现。

3. **动态防御环境下的适应性边界：** 在模型在线持续学习、防御策略自适应调整的实际部署环境中，UAtt3D能否保持其攻击有效性？特别是当防御者知晓FIR机制并针对性地监控点云各向同性指标时，攻击者需要如何调整策略？

4. **FIR可微性的防御利用：** 是否可以利用FIR的可微性设计更强的自适应防御机制？例如，通过优化逆向FIR过程来检测和还原被重采样的点云，从而在不影响良性性能的前提下识别基于重采样的攻击。这本质上是一个攻击-防御的博弈问题——FIR既是攻击工具，也可能成为防御的突破口。

## 原文 PDF

![[paperPDFs/CVPR_2026/Good_Can_Sometimes_be_Bad_A_Unified_Attack_against_3D_Point_Cloud_Classifier_by_a_Flexible_Isotropic_Resampling.pdf]]

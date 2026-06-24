---
title: "Copy-Transform-Paste: Zero-Shot Object-Object Alignment Guided by Vision-Language and Geometric Constraints"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Copy_Transform_Paste_Zero_Shot_Object_Object_Alignment_Guided_by_Vision_Language_and_Geometric_Constraints.pdf
project_link: null
code_link: null
aliases:
- CTPC
- Copy-Transform-Paste
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入分阶段优化的可微渲染管线，联合CLIP语义损失、分数化软ICP附着损失和穿透惩罚，并通过逐步增强几何权重与相机对焦策略，在测试时从粗到精地定位接触区域。
primary_logic: 无需训练新模型，仅通过测试时优化即可利用预训练的视觉-语言模型和经典几何约束，引导两网格的相对位姿与尺度对齐至语义正确且物理合理的配置。
claims:
- 在50对网格-文本基准上，本方法在所有三个语义指标（CLIP、ALIGN、SigLIP）上均取得最高分，同时交叉体积（Intersection）保持竞争力。
- 在VLM自动评估（GPTEval3D）中，本方法在所有报告指标上均排名第一。
- 用户研究中，本方法在“匹配描述”上获得85.24%，在“物理合理”上获得79.65%，显著优于所有基线。
- OOA Benchmark (50 mesh-prompt pairs) 上 CLIP Score ↑ = 最高 (显著优于所有基线)
---

# Copy-Transform-Paste: Zero-Shot Object-Object Alignment Guided by Vision-Language and Geometric Constraints

> [!tip] 核心洞察
> 无需训练新模型，仅通过测试时优化即可利用预训练的视觉-语言模型和经典几何约束，引导两网格的相对位姿与尺度对齐至语义正确且物理合理的配置。

| 字段 | 内容 |
|------|------|
| 中文题名 | 复制-变换-粘贴：基于视觉语言与几何约束引导的零样本物体对齐 |
| 英文题名 | Copy-Transform-Paste: Zero-Shot Object-Object Alignment Guided by Vision-Language and Geometric Constraints |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gatenyo_Copy-Transform-Paste_Zero-Shot_Object-Object_Alignment_Guided_by_Vision-Language_and_Geometric_Constraints_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Copy-Transform-Paste (CTP) |
| Dataset | OOA Benchmark, User Study |

> [!tip] 效果简介
> - OOA Benchmark (50 mesh-prompt pairs) 上，CLIP Score ↑ 最高 (显著优于所有基线) vs 最佳基线 (SceneTeller 或 SnapPaste) (明显提升)；ALIGN Score ↑ 最高 vs 最佳基线 (明显提升)；SigLIP Score ↑ 最高 vs 最佳基线 (明显提升)。
> - User Study (15 instances, 47 participants) 上，Matches description (%) ↑ 85.24% vs 最佳基线 (OOR-diffusion 等) (大幅领先 (基线均低于60%))；Physically plausible (%) ↑ 79.65% vs 最佳基线 (大幅领先)。

## 概述

**问题瓶颈**：物体-物体对齐（Object-Object Alignment, OOA）——给定两个三维网格和一段自然语言描述，自动调整源物体相对于目标物体的位姿与尺度，使其语义上符合描述且几何上物理合理——长期受困于两个根本性限制：一是缺乏大规模标注数据集和预训练模型，二是现有方法要么依赖纯几何的ICP系列算法（完全无法利用语言先验），要么需要专门训练的扩散模型（如 **OOR-diffusion**，Baik et al., arXiv 2025），无法在开放域语言描述下实现零样本高精度对齐。

**核心洞察**：本文提出 **Copy-Transform-Paste (CTP)**，其关键创新在于**无需训练任何新模型**，仅通过测试时优化即可联合利用预训练的视觉-语言模型（CLIP）和经典几何约束，将两网格的相对位姿与尺度引导至语义正确且物理合理的配置。这一思路将问题从“需要大规模配对数据”转化为“在预训练模型的联合嵌入空间中进行可微优化”。

**方法定位**：CTP构建了一个分阶段优化的可微渲染管线，核心因果机制包括三个协同模块：（1）**CLIP语义损失**——通过可微渲染器生成多视角图像，计算其与文本提示在CLIP联合空间的余弦相似度，提供语言引导梯度；（2）**分数化软ICP附着损失**——仅对最近 *r* 比例的源顶点施加概率软对应，实现可控的表面接触程度；（3）**穿透损失**——沿目标表面外法线方向惩罚源网格侵入，带可配置软边距以允许轻微凹陷。这三个损失通过分阶段调度（逐步增强几何权重与相机对焦策略）从粗到精地定位接触区域，并辅以LLM预测穿透策略、初始尺度比和附着比例等场景先验。

**主要结果**：在50对网格-文本基准上，CTP在所有三个语义指标（CLIP、ALIGN、SigLIP）上均取得最高分，同时在交叉体积（Intersection Volume）上保持竞争力——在语义-几何权衡图中位于右下最优区（Fig. 7）。在VLM自动评估（GPTEval3D）中，CTP在所有报告指标上排名第一（Tab. 1）。用户研究（47名参与者，15个实例）进一步验证：CTP在“匹配描述”上获得85.24%，在“物理合理”上获得79.65%，显著优于所有基线（Tab. 3）。消融实验确认每个模块均为必要——移除CLIP损失导致语义偏离，移除软ICP或穿透损失导致接触质量下降或穿透增加，移除分阶段调度则陷入局部极小（Tab. 2, Fig. 8）。

**局限与开放问题**：当前方法仍存在视点歧义（“旁边”“左右”等谓词可能不稳定）、极端尺度差异下小物体梯度不可靠、严重遮挡（如插入腔体）时性能退化等局限。未来方向包括引入多视图一致性损失克服视点歧义、扩展至非刚性变形或铰接物体的交互对齐，以及降低对LLM超参数预测的依赖。

## 背景与动机

### 问题定义：物体-物体对齐

三维场景构建中，将两个独立网格按语义描述进行空间配置——即**物体-物体对齐（Object-Object Alignment, OOA）**——是数字内容创作、机器人仿真和具身AI的关键步骤。给定源网格、目标网格和一段自然语言提示（如“帽子挂在衣帽架上”），任务要求输出源网格相对于目标网格的6自由度位姿与各向同性尺度，使得最终配置既符合文本语义，又满足物理合理性（表面接触、无穿透）。这与传统的场景生成或物体放置不同：OOA不生成新几何，也不构建完整场景，而是聚焦于两物体间精确的相对空间关系。

### 现有方法的根本瓶颈

当前解决OOA的路径主要分为两类，但均存在结构性缺陷：

**纯几何方法**以迭代最近点（ICP）系列为代表，如 **SnapPaste**（Sharf et al., Visual Computer 2006）和 **Blender Shrinkwrap**（Blender Online Community, 2025）。它们通过最小化表面距离实现网格贴合，完全不利用语言先验，因此无法理解“挂”“放”“插入”等语义差异——对它们而言，“帽子在衣帽架上”与“帽子在衣帽架旁”的几何目标可能完全相同。

**基于学习的方法**则走向另一极端。**OOR-diffusion**（Baik et al., arXiv 2025）从预训练的2D扩散模型中学习空间关系，需要专门训练且依赖大规模标注数据；**SceneTeller**（Ocal et al., ECCV 2024）和**SceneMotifCoder**（Tam et al., 3DV 2025）利用大语言模型直接生成场景布局，但缺乏细粒度的几何约束，难以保证物理合理性。

**核心瓶颈**在于：OOA领域缺乏大规模标注数据集和预训练模型，现有方法要么依赖纯几何ICP系列而忽视语义，要么需要专门训练的扩散模型而无法在开放域语言描述下实现零样本高精度对齐。语义理解与几何精度的割裂，构成了该问题的根本性挑战。

### 本文动机：测试时优化的第三条路径

本文提出一个关键洞察：**无需训练新模型，仅通过测试时优化即可利用预训练的视觉-语言模型和经典几何约束，引导两网格的相对位姿与尺度对齐至语义正确且物理合理的配置。**

这一思路的可行性源于三个观察：
1. **CLIP等视觉-语言模型**已在联合嵌入空间中建立了图像与文本的强对齐，通过可微渲染可将语义梯度反向传播至3D位姿参数；
2. **软ICP与穿透惩罚**等经典几何工具成熟可靠，只需适当改造即可与语义损失协同工作；
3. **分阶段优化调度**可以模拟从粗到精的认知过程——先在大范围内寻找语义合理的区域，再逐步收紧几何约束实现精细贴合。

基于此，本文提出**Copy-Transform-Paste (CTP)**框架，将OOA重新定义为测试时优化问题：复制源网格，通过可微渲染器在CLIP语义损失、分数化软ICP附着损失和穿透损失的联合引导下优化其位姿与尺度，最终“粘贴”到目标网格上。该方法无需任何训练数据，不引入新模型参数，仅依赖预训练组件和经典几何算法，在开放域文本描述下实现零样本对齐。

## 核心创新

Copy-Transform-Paste (CTP) 的核心创新在于**将零样本物体-物体对齐（Object-Object Alignment, OOA）重构为一个测试时优化问题**，通过可微渲染管线联合预训练的视觉-语言模型（VLM）与经典几何约束，在不训练任何新模型的前提下实现语义正确且物理合理的相对位姿估计。其关键创新点可归纳为以下五个“changed slots”：

### 1. 语义引导方式：从纯几何/训练依赖到 CLIP 可微渲染语义损失

现有方法要么依赖纯几何 ICP 系列（如 **SnapPaste**, Sharf et al., Visual Computer 2006）完全忽略语言语义，要么需要专门训练的扩散模型（如 **OOR-diffusion**, Baik et al., arXiv 2025）来学习空间关系。CTP 首次将 CLIP 的联合嵌入空间直接用作测试时优化的语义监督信号：通过可微渲染器生成 N 个相机视图，计算渲染图像的 CLIP 嵌入与文本提示嵌入的平均余弦相似度作为语义损失：

$$\mathcal{L}_{\mathrm{clip}} = -\frac{1}{N} \sum_{i=1}^{N} \mathrm{sim}(e_i, e_t), \quad \mathrm{sim}(e_i, e_t) = \frac{e_i \cdot e_t}{\|e_i\| \|e_t\|}$$

该损失通过可微渲染器将图像空间的梯度反向传播到源网格的平移、旋转（单位四元数）和各向同性缩放参数，使位姿优化直接受语言描述驱动。这一设计使得 CTP 能够处理任意开放域文本提示，无需任务特定训练数据。

### 2. 几何附着策略：从无约束/全顶点 ICP 到分数化软 ICP

标准软 ICP 对所有源顶点施加软对应，难以控制接触区域的范围。CTP 提出**分数化软 ICP**：仅对距离目标表面最近的 $r$ 比例源顶点施加软对应损失（$r \in (0,1]$），通过概率软对应 $\alpha_{ij}$ 加权期望平方距离：

$$\mathcal{L}_{\mathrm{icp}}(r) = \frac{1}{K} \sum_{i \in W} \sum_{j=1}^{N_T} \alpha_{ij} E_{ij}, \quad \alpha_{ij} = \frac{\exp(-E_{ij}/(2\sigma^2))}{\sum_{j'} \exp(-E_{ij'}/(2\sigma^2))}$$

其中 $W$ 为选定的最近 $r$ 比例源顶点集合。该设计实现了**可控附着**：$r=1.0$ 时鼓励广泛表面接触，$r$ 减小时接触区域相应收缩，使对齐行为与文本描述（如“放在上面”vs“轻触边缘”）保持一致。

### 3. 穿透处理：从无惩罚到有向深度穿透损失

现有几何方法通常缺乏穿透约束。CTP 引入基于有向深度的穿透损失，沿目标表面外法线方向惩罚源网格的侵入：

$$\mathcal{L}_{\mathrm{pen}} = \sum_{j=1}^{N_T} \max\big(0, (v_j^T - v_{i^*(j)}^S)^{\top} n_j^T - c_{\mathrm{pen}}\big)$$

其中 $c_{\mathrm{pen}}$ 为可配置软边距，允许轻微凹陷以模拟软质材料（如布料、食物）的合理嵌入。该损失与附着损失形成互补：附着鼓励接近，穿透惩罚过度侵入，二者联合约束产生物理合理的接触配置。

### 4. 优化调度：从固定权重单阶段到多阶段粗到精调度

CTP 采用 $P=3$ 阶段的分阶段优化，通过两条调度曲线逐步增强几何约束：
- **几何权重调度**：分数化软 ICP 权重 $\lambda_{\mathrm{ICP}}$ 与穿透损失权重 $\lambda_{\mathrm{pen}}$ 跨阶段对数增长，使优化从语义主导的粗探索过渡到几何主导的精细调整。
- **相机调度**：相机注视点从目标重心逐步插值到源重心，同时相机距离缩小：

$$\mathbf{c}^{(p)} = (1 - \beta_p) \mathbf{c}_t + \beta_p \mathbf{c}_s^{(p)}, \quad 0 = \beta_1 < \cdots < \beta_P \leq 1$$

该设计使早期阶段在广角视野下进行全局搜索，后期阶段聚焦于接触区域进行局部精化，有效缓解了局部极小问题。

### 5. 超参数选择：从手动固定到 LLM 场景先验预测

CTP 利用大语言模型（LLM）根据文本提示和物体名称自动预测三个关键超参数：穿透策略（布尔值，指示最终配置是否应包含穿透）、初始尺度比（基于真实世界尺寸比的估计）和附着比例（对接触程度的粗略评估）。LLM 提供的场景先验使方法能够自适应不同物体类别和交互类型，在 61 个留出实例上，LLM 预测的初始尺度（MAE 0.46）和附着比例（MAE 0.25）均显著优于随机基线（分别为 3.30 和 0.33）。

### 创新协同机制

上述五个创新点并非孤立存在，而是通过联合目标函数形成协同效应：

$$\mathcal{L} = \lambda_{\mathrm{CLIP}} \mathcal{L}_{\mathrm{clip}} + \lambda_{\mathrm{ICP}} \mathcal{L}_{\mathrm{icp}} + \lambda_{\mathrm{pen}} \mathcal{L}_{\mathrm{pen}}$$

在分阶段调度框架下，语义损失提供全局方向引导，分数化软 ICP 实现可控表面附着，穿透损失保证物理合理性，LLM 预测提供合理的优化起点，随机重启与 Best-of-N 选择进一步提升鲁棒性。消融实验（Tab. 2, Fig. 8）验证了每个模块的必要性：移除任一组件均导致语义对齐度下降或穿透增加。

## 整体框架

**Copy-Transform-Paste (CTP)** 是一种测试时优化的零样本物体-物体对齐框架。给定两个三角网格（目标网格与源网格）和一段自由形式的文本提示，CTP 直接优化源网格相对于目标网格的 **7 自由度位姿参数** $\theta = (\tau, q, s)$——即平移 $\tau$、单位四元数旋转 $q$ 和各向同性缩放 $s$——而无需任何预训练或微调。

核心思想是将语义理解与几何约束统一在一个可微渲染管线中：通过可微渲染器将 3D 场景投影为多视角 2D 图像，利用预训练的 **CLIP** 视觉-语言模型计算渲染视图与文本提示的语义对齐损失，同时引入两类几何损失——**分数化软 ICP** 鼓励可控的表面附着，**穿透损失** 惩罚物理不合理的网格侵入——形成联合目标函数进行端到端梯度优化。

### 管线模块与数据流

整个管线由以下关键模块串联构成，数据流如图 2 所示：

1. **Auto-Align 规范化**：首先将目标网格通过对称性估计重定向到统一的直立坐标系，消除朝向歧义，为后续语义监督提供稳定的观测基准。

2. **可微渲染与语义引导**：在每个优化阶段，将组合后的场景通过可微渲染器 $\mathcal{R}$ 渲染为 $N$ 个相机视图，提取 CLIP 图像嵌入 $e_i$，与文本提示嵌入 $e_t$ 计算平均余弦相似度的负数作为语义损失：
   $$\mathcal{L}_{\mathrm{clip}} = -\frac{1}{N} \sum_{i=1}^{N} \mathrm{sim}(e_i, e_t)$$
   梯度通过渲染器反向传播至 3D 位姿参数，驱动源网格向语义描述对齐。

3. **分数化软 ICP**：仅对最近 $r$ 比例的源顶点施加软对应，计算期望平方距离损失 $\mathcal{L}_{\mathrm{icp}}(r)$，通过调节 $r \in (0,1]$ 控制附着区域的大小——$r=1.0$ 鼓励大面积表面接触，$r$ 减小则收缩接触区域（见图 3）。

4. **穿透损失**：沿目标表面外法线方向，惩罚源网格顶点侵入超过软边距 $c_{\mathrm{pen}}$ 的深度：
   $$\mathcal{L}_{\mathrm{pen}} = \sum_{j=1}^{N_T} \max\big(0, (v_j^T - v_{i^*(j)}^S)^{\top} n_j^T - c_{\mathrm{pen}}\big)$$
   正边距允许轻微凹陷以模拟软质材料（见图 4）。

5. **分阶段优化调度**：优化分为 $P=3$ 个阶段。跨阶段应用两种调度策略：(i) 分数化软 ICP 权重 $\lambda_{\mathrm{ICP}}$ 与穿透损失权重 $\lambda_{\mathrm{pen}}$ 按对数增长，使搜索从粗粒度探索过渡到精细局部调整；(ii) 相机注视点从目标重心逐步插值到源重心，同时拉近相机距离，实现渐进式聚焦。每阶段的最优结果初始化下一阶段（见图 5）。

6. **LLM 超参数预测**：利用大语言模型根据文本提示和物体名称预测三个场景先验——是否允许穿透、初始尺度比和附着比例 $r$——为优化提供合理的初始化超参数。

7. **随机重启与 Best-of-N 选择**：多个随机初始化并行运行相同目标函数，最终选取总损失最低的位姿，缓解局部极小问题（见图 6a）。不同提示可引导相同网格对收敛到语义不同的配置（见图 6b）。

### 总目标函数

联合损失形式为：
$$\mathcal{L} = \lambda_{\mathrm{CLIP}} \mathcal{L}_{\mathrm{clip}} + \lambda_{\mathrm{ICP}} \mathcal{L}_{\mathrm{icp}} + \lambda_{\mathrm{pen}} \mathcal{L}_{\mathrm{pen}}$$
其中 $\lambda_{\mathrm{CLIP}}$ 保持固定，$\lambda_{\mathrm{ICP}}$ 和 $\lambda_{\mathrm{pen}}$ 随阶段递增。使用 Adam 优化器更新 $\theta$，整个流程无需训练任何新模型，完全依赖预训练 CLIP 和经典几何约束在测试时完成对齐。

### 补充图表

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed pipeline. Given two meshes and a text prompt, we optimize the relative pose and scale to produce a text-consistent alignment over P phases. In each phase, we compose the scene, render with a differentiable renderer to obtain a semantic loss, and compute geometric losses. The best result of phase i initializes phase i{+}1 ; across phases we increase the fractional soft-ICP and penetration weights and progressively zoom the cameras in. The final output is an aligned 3D placement of the two meshes*

## 核心模块与公式推导

### 3.1 问题形式化与优化变量

给定目标网格 $\mathcal{M}_T$、源网格 $\mathcal{M}_S$ 和一条文本提示 $t$，CTP 在测试时直接优化源网格相对于目标网格的**位姿参数** $\theta = (\tau, q, s)$，其中 $\tau \in \mathbb{R}^3$ 为平移向量，$q$ 为单位四元数表示旋转，$s \in \mathbb{R}^+$ 为各向同性缩放因子。优化目标是在不训练任何新模型的前提下，使两网格的相对空间配置同时满足语义一致性与物理合理性。

### 3.2 语义引导：CLIP 可微渲染损失

CTP 的核心创新在于将预训练的视觉-语言模型 **CLIP** 作为语义监督信号。通过可微渲染器 $\mathcal{R}$ 从 $N$ 个相机视角渲染组合场景，获得渲染图像嵌入 $e_i$，并与文本提示嵌入 $e_t$ 计算余弦相似度：

$$
\mathcal{L}_{\mathrm{clip}} = -\frac{1}{N} \sum_{i=1}^{N} \mathrm{sim}(e_i, e_t), \quad \mathrm{sim}(e_i, e_t) = \frac{e_i \cdot e_t}{\|e_i\| \|e_t\|} \tag{1}
$$

**变量含义**：$e_i = \mathrm{CLIP}_{\mathrm{image}}(\mathcal{R}(\mathcal{M}_T, \mathcal{M}_S(\theta); \pi_i))$ 为第 $i$ 个相机位姿 $\pi_i$ 下的渲染视图 CLIP 图像嵌入；$e_t = \mathrm{CLIP}_{\mathrm{text}}(t)$ 为文本提示的 CLIP 文本嵌入。该损失通过可微渲染器将图像空间的语义梯度反向传播至 3D 位姿参数，驱动源网格向符合文本描述的空间位置移动。

### 3.3 几何约束：分数化软ICP与穿透惩罚

仅靠语义损失无法保证物理合理的表面接触——CLIP 对精确的 3D 几何关系不敏感。CTP 引入两项几何损失来弥补这一缺陷。

#### 3.3.1 分数化软ICP损失

标准软 ICP 对所有源顶点施加软对应，可能鼓励过度附着。CTP 提出**分数化变体**，仅对距离目标表面最近的 $r$ 比例源顶点计算软对应期望平方距离：

$$
\mathcal{L}_{\mathrm{icp}}(r) = \frac{1}{K} \sum_{i \in W} \sum_{j=1}^{N_T} \alpha_{ij} E_{ij}, \quad \alpha_{ij} = \frac{\exp(-E_{ij}/(2\sigma^2))}{\sum_{j'} \exp(-E_{ij'}/(2\sigma^2))} \tag{2}
$$

**变量含义**：$W$ 为选定的最近 $r$ 比例源顶点索引集，$K = |W|$；$N_T$ 为目标网格顶点数；$E_{ij} = \|v_i^S - v_j^T\|^2$ 为源顶点 $v_i^S$ 与目标顶点 $v_j^T$ 的平方欧氏距离；$\alpha_{ij}$ 为通过 softmax 温度 $\sigma$ 计算的软对应概率。比率 $r \in (0,1]$ 控制附着区域的范围——$r=1.0$ 鼓励大面积表面接触，$r$ 减小则接触区域相应收缩（见 Figure 3）。

#### 3.3.2 穿透损失

为防止源网格不合理地侵入目标网格内部，CTP 沿目标表面外法线方向惩罚侵入深度：

$$
\mathcal{L}_{\mathrm{pen}} = \sum_{j=1}^{N_T} \max\big(0, (v_j^T - v_{i^*(j)}^S)^{\top} n_j^T - c_{\mathrm{pen}}\big) \tag{3}
$$

**变量含义**：$n_j^T$ 为目标顶点 $v_j^T$ 的单位外法线；$i^*(j) = \arg\min_i \|v_i^S - v_j^T\|$ 为距离 $v_j^T$ 最近的源顶点索引；$(v_j^T - v_{i^*(j)}^S)^{\top} n_j^T$ 为沿法线方向的有向深度（正值表示源顶点在目标表面内侧）；$c_{\mathrm{pen}} \geq 0$ 为软边距，允许轻微凹陷以模拟软质材料的压痕效果（见 Figure 4）。

### 3.4 总目标函数与分阶段优化调度

三项损失加权组合构成总优化目标：

$$
\mathcal{L} = \lambda_{\mathrm{CLIP}} \mathcal{L}_{\mathrm{clip}} + \lambda_{\mathrm{ICP}} \mathcal{L}_{\mathrm{icp}} + \lambda_{\mathrm{pen}} \mathcal{L}_{\mathrm{pen}} \tag{4}
$$

CTP 采用 $P=3$ 阶段的分阶段优化策略。跨阶段应用两项关键调度：

- **几何权重调度**：$\lambda_{\mathrm{ICP}}$ 和 $\lambda_{\mathrm{pen}}$ 随阶段对数递增，使优化从语义主导的粗探索逐步过渡到几何约束主导的局部精调。
- **相机调度**：相机注视点从目标重心 $\mathbf{c}_t$ 逐步插值至源当前重心 $\mathbf{c}_s^{(p)}$：
  $$
  \mathbf{c}^{(p)} = (1 - \beta_p) \mathbf{c}_t + \beta_p \mathbf{c}_s^{(p)}, \quad 0 = \beta_1 < \cdots < \beta_P \leq 1
  $$
  同时相机距离逐步缩小，实现对源网格的渐进聚焦（见 Figure 5）。前一阶段的最优结果作为下一阶段的初始化，配合多次随机重启与 Best-of-N 选择缓解局部极小问题。

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/004_Figure_5.jpg]]
*Figure 5: Visualization of phased optimization with scheduled weights. Rooster and comb across three phases. As the weights increase across phases, the search transitions from broad exploration to a focused zoom-in and local refinement. Phase-best results are marked with $\star$ and initialize the next phase*

### 补充图表

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/005_Figure_4.jpg]]
*Figure 4: Penetration loss geometry. For target vertex*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/003_Figure_3.jpg]]
*Figure 3: Effect of the alignment ratio r on a grilled-toast pair. The two objects are optimized with the same prompt, “grilled cheese toasts”, while varying r. With r=1.0, the top toast aligns directly above the bottom toast, producing broad surface contact; as r decreases, attachment is encouraged over a smaller subset of vertices and the contact region correspondingly shrinks*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/006_Figure_6.jpg]]
*Figure 6: Initialization variability and prompt controllability. (a) Two random initializations of the carrot w.r.t. Bugs Bunny converge to distinct yet plausible attachments; we run several restarts and pick the best by a CLIP text–image score (higher is better). (b) With the same meshes, two prompts steer optimization to promptconsistent placements, demonstrating language controllability*

## 实验与分析

### 核心实验设置

本方法在自建的 **OOA Benchmark**（50 对网格-文本提示）上进行评估，覆盖多样化的物体-物体空间关系。优化过程采用 **P=3 阶段**分阶段调度，每对运行 **2,000 步**，每步渲染 **8 个相机视图**的批量。分数化软ICP权重与穿透损失权重按对数增长跨阶段递增，相机焦点从目标重心逐步插值至源重心并拉近（详见 Sec. 3.4）。超参数方面，穿透策略、初始尺度比和附着比例由 LLM 根据文本提示和物体名称自动预测，替代手动调参。

### 主结果：语义对齐与物理合理性

**Table 1** 报告了与几何基线（SnapPaste、Blender Shrinkwrap）和语言驱动基线（SceneTeller、SceneMotifCoder）的全面对比。CTP 在所有三个语义指标上均取得最高分，同时交叉体积保持竞争力：

- **CLIP Score ↑**：CTP 显著优于所有基线，验证了可微渲染 CLIP 损失对语义引导的有效性。
- **ALIGN Score ↑ 与 SigLIP Score ↑**：同样排名第一，表明语义对齐能力不依赖于特定视觉-语言模型的选择。
- **Intersection Volume ↓**：CTP 的穿透量虽略高于纯几何方法，但在 **Figure 7** 的语义-几何权衡图中，CTP 始终位于**右下最优区域**，即同时实现高语义一致性与低穿透的最佳组合。

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/007_Figure_7.jpg]]
*Figure 7: Trade-off plot. CLIP, ALIGN score vs. intersection volume score. Down and to the right is better. The full visualization, including SigLIP, is provided in the supplementary*

**VLM 自动评估**（GPTEval3D）进一步佐证：CTP 在 Text–Asset、3D Plausibility、Text–Geometry 及 Overall 所有子项上均排名第一，说明大语言模型评估器同样认可其生成质量。

**用户研究**（Table 3）提供了最强的人类偏好证据：在 15 个实例、47 名参与者的评估中，CTP 在“匹配描述”（**85.24%**）和“物理合理”（**79.65%**）两项上大幅领先所有基线（基线均低于 60%）。这一结果表明，分阶段优化管线生成的接触配置在人类感知中兼具语义忠实度和物理可信度。

### 定性分析

**Figure 9** 展示了四组不同物体-物体配对的定性对比。CTP 的结果在语义忠实度和接触质量上均优于基线：几何方法（SnapPaste、Shrinkwrap）缺乏语言引导，常产生语义错误的附着位置；语言驱动方法（SceneTeller、SceneMotifCoder）虽能捕捉语义，但物理接触往往粗糙或穿透严重。

**Figure 10** 与训练过的扩散模型 **OOR-diffusion**（Baik et al., arXiv 2025）进行定性比较。由于 OOR-diffusion 无公开代码/权重，作者仅复现其论文示例并匹配资产与相机。结果显示，CTP 在零样本条件下即可达到与专门训练的扩散模型相当甚至更优的对齐质量，凸显了测试时优化的优势。

### 消融实验

**Table 2** 和 **Figure 8**（衣帽架与帽子示例）系统验证了各模块的必要性：

| 消融变体 | 主要退化表现 |
|---------|------------|
| 无 CLIP 语义损失 | 失去语言引导，对齐结果偏离提示描述 |
| 无分数化软ICP | 表面接触质量下降，出现间隙或错位，交叉体积增加 |
| 无穿透损失 | 网格间穿透显著增加，物理合理性恶化 |
| 无分阶段调度 | 过早陷入局部极小，无法精细调整，语义与几何指标均下降 |
| 无相机缩放 | 远距小物体的梯度减弱，语义对齐精度降低 |

完整方法在所有消融变体中始终取得最优的语义对齐分数和最低的穿透体积，证实了语义损失、几何约束、分阶段调度和相机策略的协同必要性。

### LLM 超参数预测的有效性

**Table 4** 在 61 个留出物体对实例上评估 LLM 超参数预测的准确性。LLM 预测的初始尺度比 MAE 为 **0.46**，显著优于随机基线的 **3.30**；附着比例 MAE 为 **0.25**，优于随机基线的 **0.33**。这一结果表明，LLM 能有效利用常识知识提供合理的场景先验，减少手动调参负担。

### 失败模式分析

**Figure 12** 揭示了 CTP 的三类典型失败情况：

1. **多视图歧义与腔体插入**：当源物体需插入目标腔体（如将笔插入笔筒）时，有限视角监督可能产生仅在采样角度正确但 3D 全局错误的对齐；视角敏感谓词（如“旁边”“左右”）也可能导致不稳定结果。
2. **极端尺度差异**：小物体在渲染视图中占比过小，导致 CLIP 梯度不可靠，语言引导失效。
3. **残余穿透**：最终结果可能仍有轻微穿透，通常可通过增加穿透权重或重新运行缓解，但无法完全根除。

这些失败模式指向了当前框架的边界：依赖有限视角的语义监督在遮挡或尺度极端场景下鲁棒性不足，且仅支持两网格对齐的设定限制了多物体一次性全局优化的可能性。

### 补充图表

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/009_Table_1.jpg]]
*Table 1: Baseline comparison. Semantic alignment (CLIP/ALIGN/SigLIP; higher is better), physical plausibility (intersection volume; lower is better), and VLM evaluator scores (Text–Asset, 3D Plausibility, Text–Geometry, Overall; higher is better)*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/010_Table_2.jpg]]
*Table 2: Ablation comparison. Ablated variants across semantic alignment (CLIP/ALIGN/SigLIP; higher is better), physical plausibility (intersection volume; lower is better), and VLM evaluator scores (Text–Asset, 3D Plausibility, Text–Geometry, Overall; higher is better)*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/011_Table_3.jpg]]
*Table 3: User study results. Percentage of votes across 15 instances and 47 participants. Higher is better*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/008_Figure_8.jpg]]
*Figure 8: Ablations on coatrack (target) and hat (source). The full method yields the most plausible, text-aligned placement; ablating individual components produces degradations*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative comparison across four object–object pairs. Top row: input prompt and meshes. Rows 1–5: final placements from our method and baselines. Our approach yields semantically faithful and physically plausible alignments, while baselines vary in semantic faithfulness and contact quality*

![[assets/figures/papers/paper_list_l2380_https_openaccess_thecvf_com_content_CVPR2026_html_Gatenyo_Copy_Transform/figures/015_Figure_10.jpg]]
*Figure 10: Qualitative comparison to OOR-diffusion. OORdiffusion panels are reproduced from their paper; we matched assets and camera setups where possible*

## 方法谱系与知识库定位

### 1. 问题定位与关键瓶颈

物体-物体对齐（Object-Object Alignment, OOA）的目标是：给定两个独立的3D网格和一个描述其空间关系的自然语言提示，自动求解源网格相对于目标网格的相对位姿（平移、旋转、各向同性缩放），使最终配置既符合语义描述，又在几何上物理合理。该任务的核心瓶颈在于**语义与几何的双重要求难以在零样本条件下同时满足**：

- **纯几何方法**（如ICP系列）完全不利用语言先验，无法理解“放在上面”“靠在旁边”等语义约束，只能实现无意义的表面贴合。
- **基于生成模型的方法**（如扩散模型）需要大规模标注数据进行训练，且受限于训练分布，难以泛化到开放域物体和任意文本描述。
- **基于LLM的场景生成方法**直接输出布局参数，缺乏对几何细节的精细控制，常导致穿透或错位。

本文提出的**Copy-Transform-Paste (CTP)**方法从根本上改变了这一格局：它**不需要任何训练数据或预训练模型**，仅通过测试时优化（test-time optimization）即可联合利用预训练的视觉-语言模型（CLIP）和经典几何约束，在零样本条件下实现高精度的语义对齐与物理合理配置。

### 2. 方法谱系与基线对比

CTP位于**测试时优化驱动的零样本3D对齐**这一新兴范式，其设计思想与以下几条技术路线形成对比或互补。

#### 2.1 基于扩散模型的生成式对齐

**OOR-diffusion**（Baik et al., arXiv 2025）是当前唯一直接针对OOA任务进行训练的文本条件扩散模型。它从预训练的2D扩散模型中学习物体间的空间关系，通过去噪过程直接生成相对位姿。然而，该方法的局限性显著：(1) 需要专门的训练数据和模型权重，泛化能力受限于训练分布；(2) 由于无公开代码和权重，复现困难，本文仅能通过论文示例进行定性比较；(3) 扩散模型的随机性导致结果不稳定，且缺乏显式的几何约束来防止穿透。相比之下，CTP通过可微渲染直接利用CLIP的开放域语义理解能力，无需任何训练，且通过分数化软ICP和穿透损失提供硬几何保障。

#### 2.2 基于LLM的场景生成方法

**SceneTeller**（Öcal et al., ECCV 2024）和**SceneMotifCoder**（Tam et al., 3DV 2025）代表了另一类方法：利用LLM理解语言描述并直接生成3D场景布局。SceneTeller通过LLM将文本转化为场景图，再映射为物体位姿；SceneMotifCoder则从示例中学习编排模式。这些方法的共同问题是：(1) LLM输出的位姿参数缺乏细粒度的几何优化，常导致穿透或悬空；(2) 对语言理解的依赖过重，忽略了视觉-几何闭环验证。CTP仅在超参数选择（穿透策略、初始尺度比、附着比例）上借助LLM提供场景先验，核心对齐过程完全由视觉和几何损失驱动，实现了“LLM提供粗先验，优化实现精对齐”的分工。

#### 2.3 基于纯几何的交互式对齐

**SnapPaste**（Sharf et al., Visual Computer 2006）和**Blender Shrinkwrap**（Blender Online Community, 2025）代表了传统的几何驱动对齐方法。SnapPaste基于ICP实现交互式网格合成，Shrinkwrap通过几何投影约束将源网格贴合到目标表面。这些方法完全不理解语义，只能实现“表面贴合”而无法区分“放在上面”与“靠在旁边”等语义差异。CTP通过CLIP语义损失弥补了这一缺陷，同时通过分数化软ICP保留了可控的表面附着能力——通过调节附着比例$r \in (0,1]$，用户或LLM可以精确控制接触区域的大小（见Figure 3）。

#### 2.4 关键改进槽位总结

下表总结了CTP相对于基线方法的核心改进维度：

| 改进维度 | 基线方法 | CTP方法 |
|---------|---------|---------|
| 语义引导方式 | 无语言引导（纯几何ICP）或LLM直接生成布局 | CLIP可微渲染语义损失，直接测量渲染视图与文本提示的余弦相似度 |
| 几何附着策略 | 无接触约束或标准软ICP使用全部顶点 | 分数化软ICP，仅对最近$r$比例源顶点施加软对应，实现可控附着 |
| 穿透处理 | 无穿透惩罚 | 基于有向深度的穿透损失，带软边距$c_{pen}$，允许轻微凹陷 |
| 优化调度 | 固定权重单阶段优化，全局相机 | 多阶段($P=3$)分阶段优化，几何损失权重与穿透惩罚逐步增加，相机焦点从目标中心插值到源中心并拉近 |
| 超参数选择 | 手动固定超参数 | 利用LLM根据文本提示和物体名称预测穿透策略、初始尺度比和附着比例 |

### 3. 适用边界与局限

CTP在50对网格-文本基准上展示了显著的零样本对齐能力，但其适用边界和局限性同样值得关注：

#### 3.1 视角敏感性与多视图歧义

CTP的语义监督依赖于从有限视角（每步8个相机视图）渲染的图像。这导致两个潜在问题：(1) **视角敏感谓词**（如“旁边”“左右”）可能仅在采样角度上正确，而在其他视角下出现3D全局错误；(2) **多视图歧义**：当物体具有对称性或自相似纹理时，不同视角可能提供冲突的语义梯度，导致优化陷入局部极小。Figure 12中的失败案例明确展示了这一问题。解决方向可能包括引入多视图一致性损失或增加视角采样密度。

#### 3.2 极端尺度与遮挡退化

当源网格与目标网格的尺度差异极大时（例如“针放在桌面上”），小物体在渲染图像中占比过小，CLIP的图像嵌入可能无法提供可靠的语义梯度。类似地，当对齐涉及**插入腔体**（如“笔插入笔筒”）时，严重遮挡会使渲染视图几乎无法反映物体的实际空间关系，导致性能退化。Figure 12同样记录了这类失败模式。LLM预测的初始尺度比在一定程度上缓解了尺度问题（Table 4显示LLM预测的初始尺度MAE为0.46，远优于随机基线的3.30），但极端情况仍需更鲁棒的初始化策略。

#### 3.3 穿透残留与权重调优

尽管穿透损失有效抑制了大部分物理不合理的交叉，最终结果仍可能残留轻微穿透。论文指出可通过增加穿透权重或重新运行来缓解，但这引入了手动调参的负担。此外，分阶段调度中的权重增长曲线（对数增长）和相机缩放策略虽经验有效，但其最优性缺乏理论保证。

#### 3.4 双物体限制与多物体扩展

CTP当前仅支持两个网格的对齐。对于多物体组装（如Figure 1中的汉堡迭代合成），需要通过将前一阶段的输出作为下一阶段的输入来迭代完成。这种贪心策略无法保证全局最优，且误差会累积。如何实现一次性全局优化多物体对齐是一个开放问题。

#### 3.5 LLM依赖与超参数鲁棒性

LLM超参数预测器（预测穿透策略、初始尺度比、附着比例）在61个留出实例上显著优于随机基线（Table 4），但其性能依赖于底层LLM的质量。对于LLM知识覆盖不足的物体类别或复杂提示，预测可能出错。如何降低对LLM的依赖，实现完全自动的超参数自适应，是进一步提升鲁棒性的方向。

### 4. 开放问题与未来方向

基于CTP的当前局限和方法谱系中的技术空白，以下开放问题值得后续研究关注：

1. **物理仿真集成**：当前穿透损失仅提供静态的几何惩罚，无法模拟重力、碰撞响应等动态物理行为。引入轻量级物理仿真（如基于粒子的弹簧系统或刚体动力学）可进一步提升物理合理性，特别是对于“堆叠”“悬挂”等涉及力学关系的描述。

2. **多视图一致性优化**：克服视角歧义的一个直接方向是引入多视图一致性损失，强制不同视角下的语义预测保持一致。这与NeRF/3DGS等新视角合成技术中的多视图约束有天然联系。

3. **非刚性与铰接扩展**：CTP当前仅优化刚体变换（平移、旋转、各向同性缩放）。许多实际对齐涉及非刚性变形（如“围巾缠绕在脖子上”）或铰接物体（如“盖子盖在盒子上”）。将优化变量扩展为变形场或关节参数是一个有前景的方向。

4. **完全自动的超参数自适应**：当前LLM仅用于初始化超参数，优化过程中权重调度仍依赖人工设计的对数增长曲线。元学习或强化学习方法可能学习到更优的自适应调度策略，消除对手动设计的依赖。

5. **复杂场景鲁棒性**：在动态背景、多物体交互、复杂光照等更接近真实应用的场景中，CTP的可微渲染-语义反馈回路是否仍能保持鲁棒性，是一个需要验证的问题。这可能涉及域适应技术或更强的视觉骨干网络。

## 原文 PDF

![[paperPDFs/CVPR_2026/Copy_Transform_Paste_Zero_Shot_Object_Object_Alignment_Guided_by_Vision_Language_and_Geometric_Constraints.pdf]]

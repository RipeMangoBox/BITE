---
title: "HOG-Layout: Hierarchical 3D Scene Generation, Optimization and Editing via Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HOG_Layout_Hierarchical_3D_Scene_Generation_Optimization_and_Editing_via_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- HL
- HOG-Layout
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入层次化支撑关系树，将场景中的物体按父子支撑关系组织为不同层级；将布局约束统一抽象为方向分解的连续力（水平力、垂直力、旋转扭矩），并通过迭代力导向优化消除冲突。
primary_logic: 将场景优化建模为基于层次结构的力导向物理仿真，通过将复杂的空间约束转化为可叠加的力，使VLM预测的初始布局逐步收敛至物理上稳定、语义上合理的最终状态，同时利用死锁检测打破局部最优。
claims:
- 相比LayoutGPT、Holodeck和LayoutVLM，HOG-Layout在保真度、物理合理性、CLIP相似度和语义合理性上均显著占优。
- 移除层次化优化模块（w/o HierOpt）后，物体碰撞率COL_ob从5.28%飙升至36.46%，COL_sc从16.00%升至65.00%，OOR从43.09%降至35.85%，表明优化对物理可行性和保真度至关重要。
- 层次化力导向优化器在生成时间（70.44秒）上远快于梯度优化器（147.93秒），且所有关键指标均更优。
- SceneEval 上 OOR% (Object-Object Relationship fidelity) = 43.09
---

# HOG-Layout: Hierarchical 3D Scene Generation, Optimization and Editing via Vision-Language Models

> [!tip] 核心洞察
> 将场景优化建模为基于层次结构的力导向物理仿真，通过将复杂的空间约束转化为可叠加的力，使VLM预测的初始布局逐步收敛至物理上稳定、语义上合理的最终状态，同时利用死锁检测打破局部最优。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOG-Layout：基于视觉语言模型的分层3D场景生成、优化与编辑 |
| 英文题名 | HOG-Layout: Hierarchical 3D Scene Generation, Optimization and Editing via Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10772) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HOG-Layout |
| Dataset | SceneEval |

> [!tip] 效果简介
> - SceneEval 上，OOR% (Object-Object Relationship fidelity) 43.09 vs 38.09 (LayoutVLM) (+5.00)；OAR% (Object-Architecture Relationship fidelity) 75.74 vs 61.99 (LayoutVLM) (+13.75)；COL_ob% (Object-level collision, lower better) 5.28 vs 29.44 (LayoutVLM) (-24.16)。

## 概要

现有基于视觉语言模型（VLM）的3D场景生成方法普遍缺乏对物理一致性的显式建模，常导致物体碰撞、不合理放置和较低的语义遵循度。其根本瓶颈在于：纯文本或视觉输出无法保证场景中物体的空间关系、支撑逻辑与边界约束。

针对这一问题，**HOG-Layout** 提出了一种层次化3D场景生成、优化与编辑框架。其核心洞察是：将场景优化建模为基于层次结构的力导向物理仿真——通过将复杂的空间约束转化为可叠加的连续力（水平力、垂直力、旋转扭矩），使VLM预测的初始布局逐步收敛至物理稳定、语义合理的最终状态，并利用死锁检测机制打破局部最优。

在方法谱系上，HOG-Layout区别于三类基线路径：**LayoutGPT** 仅通过LLM单步生成布局，缺乏优化步骤；**Holodeck** 引入硬约束求解器保证物理可行性，但忽视软语义约束；**LayoutVLM** 采用可微分优化，但需预定义物体集且优化耗时。HOG-Layout的关键改进在于：(1) 按支撑关系构建层次化父子树，将场景组织为不同层级；(2) 基于RAG检索模板规则库进行场景规划，并按功能区域分组迭代生成布局；(3) 以力导向迭代优化统一处理物理与语义约束。

实验结果表明，HOG-Layout在SceneEval基准上全面超越基线方法：物体间关系保真度（OOR）达43.09%，较LayoutVLM提升5个百分点；物体与建筑关系保真度（OAR）达75.74%，提升13.75个百分点；物体级碰撞率（COL_ob）仅5.28%，较LayoutVLM降低24.16个百分点；语义合理性得分（SP）为69.69，且高分段密度显著优于其他方法。消融实验进一步证实，移除层次化优化模块后碰撞率从5.28%飙升至36.46%，验证了优化的必要性；同时，力导向优化器在生成时间（70.44秒）上较梯度优化器（147.93秒）快约2.1倍，且所有关键指标均更优。

该方法的局限性包括：移动指令编辑成功率相对较低（80%），源于自然语言空间描述的固有歧义性；依赖现有3D资产库，对库外物体需借助生成式管线；当前实验局限于室内场景，户外及大规模环境下的泛化性有待验证。



3D场景生成是计算机视觉与图形学中的核心任务，其目标是根据自然语言指令自动合成包含合理物体布局的室内外环境。近年来，大语言模型（LLM）与视觉语言模型（VLM）在该领域展现出巨大潜力，能够将文本描述直接映射为场景中物体的位置、朝向与类别。然而，**现有基于VLM的3D场景生成方法普遍缺乏对物理一致性的显式建模**，导致生成的布局频繁出现物体碰撞、不合理放置（如悬空物体）以及较低的语义遵循度。纯文本或视觉输出的生成范式无法保证场景中物体的空间关系、支撑逻辑和边界约束，这成为制约该技术走向实际应用的核心瓶颈。

具体而言，当前主流方法可归纳为三类范式，各有其结构性缺陷：

- **直接布局生成**（如LayoutGPT）：基于LLM一步生成物体坐标，完全缺失优化步骤，碰撞与出界问题严重。
- **硬约束求解**（如Holodeck）：引入空间关系约束并通过DFS/MILP求解器保证硬物理约束，但忽视了软语义约束（如邻近关系、朝向偏好），且求解过程缺乏灵活性。
- **可微分优化**（如LayoutVLM）：利用VLM联合文本与视觉信息进行梯度下降优化，但需预定义物体集，且优化过程极为耗时。

上述方法的共同症结在于：**场景中的物体被视作平坦的列表，缺乏显式的结构组织**。在真实世界中，物体之间存在天然的支撑层级关系——例如，地板支撑家具、桌面支撑物品——这种层次结构是维持物理稳定性的基础。忽视该结构意味着优化算法无法区分不同层级的约束优先级，也难以将复杂的空间规则有效分解。

本文的核心动机在于：**将场景优化建模为基于层次结构的力导向物理仿真**。通过将复杂的空间约束（碰撞、边界、支撑、邻近、靠墙、朝向、对齐）统一转化为可叠加的连续力——包括水平力、垂直力和旋转扭矩——使VLM预测的初始布局在迭代过程中逐步收敛至物理上稳定、语义上合理的最终状态。同时，引入死锁检测机制以打破局部最优，确保优化过程的高效与鲁棒。这一思路将3D场景生成从“一次性预测”转变为“层次化迭代精炼”，从根本上弥补了现有方法在物理可行性上的系统性缺陷。



## 核心方法与创新机理

HOG-Layout 的核心创新在于将 3D 场景生成重新定义为**层次化力导向物理仿真问题**，通过三个相互耦合的机制设计，系统性解决了现有 VLM 方法在物理一致性上的根本缺陷。

### 1. 层次化支撑关系树：从平坦列表到结构化解空间

现有方法（LayoutGPT、Holodeck、LayoutVLM）均将场景建模为平坦的物体列表，缺乏对物体间支撑关系的显式表征。HOG-Layout 引入了**层次化父-子树结构**：根据支撑关系将物体组织为不同层级——所有直接接触地板的物体以地板为父节点构成同一层级，墙面、天花板或特定物体 ID 同样可作为父节点锚定其支撑的子物体。这一设计将原本耦合的全局布局问题**分解为层级内独立可解的局部子问题**，使 VLM 和优化模块只需关注同层物体间的依赖关系，显著降低了推理空间的复杂度。

### 2. 约束到力的统一抽象：物理与语义的连续化表达

布局优化中的约束类型繁杂——碰撞避免、边界限制、支撑逻辑、邻近关系、靠墙偏好、朝向对齐等——传统方法或忽略优化（LayoutGPT），或采用硬约束求解器保证物理可行性但忽视软语义约束（Holodeck），或依赖耗时的梯度下降（LayoutVLM）。HOG-Layout 的关键突破在于将所有复杂布局规则**统一抽象为方向分解的连续力**：

- **水平力** $F_{i, \mathrm{plane}}(t)$：处理同层碰撞、边界、邻近、靠墙等平面约束
- **垂直力** $F_{i, \mathrm{vert}}(t)$：处理跨层碰撞、垂直边界、支撑逻辑
- **旋转扭矩** $\tau_i(t)$：处理朝向对齐约束

这种力分解策略使得物理可行性与语义合理性在统一框架下被同时优化，且力的可叠加性允许系统高效地并行处理多约束交互。

### 3. 死锁感知的迭代优化：打破局部最优的逃逸机制

力导向优化在复杂约束下容易陷入局部最优——物体在狭窄空间中来回震荡而无法收敛。HOG-Layout 设计了**死锁检测与回避机制**：当物体在时间窗口内的累计移动距离超过阈值 $\mathcal{D}_1$，但窗口首尾的绝对位移小于阈值 $\mathcal{D}_2$ 时判定为死锁。水平死锁通过施加垂直于死锁方向的逃逸力解决，垂直死锁则通过沿 Z 轴收缩物体尺度来突破。这一机制使优化器能够在保持稳定收敛的同时主动跳出局部极小，是层次化力导向优化器在效率（70.44秒）上远超梯度优化器（147.93秒）且指标全面占优的关键使能技术。

### 4. 分组迭代生成与优化的闭环

不同于单步生成全场景的基线方法，HOG-Layout 采用**按功能区域分组迭代**的策略：首组基于空场景俯视图生成布局并优化，优化后的场景俯视图作为下一组生成的视觉上下文输入 VLM。这种“生成-优化-反馈”的闭环使后续组的布局能够感知已优化物体的空间占位，从源头减少跨组冲突，与层次化优化形成协同效应。



HOG-Layout 是一个面向文本驱动 3D 场景合成与编辑的模块化流水线，由四个核心组件串联构成：**场景规划（Scene Planning）**、**布局生成（Layout Generation）**、**层次化优化（Hierarchical Optimization）** 和 **场景编辑（Scene Editing）**。其核心设计理念是将场景中的物体按支撑关系组织为层次化的父子结构，并将物理可行性与语义逻辑约束统一抽象为可叠加的连续力，通过迭代力导向仿真驱动布局收敛至稳定状态。

### 输入输出流与模块协作

系统以自然语言场景描述作为输入，整体数据流如下：

1. **场景规划** 接收用户文本，通过 RAG 机制从模板规则库（基于 FAISS 向量库存储，使用 Qwen3-Embedding-4B 编码为 1024 维特征向量）检索最相关的布局约束规则，交由 LLM 生成包含物体列表、房间信息、功能分组及场景描述的完整规划。
2. **布局生成** 将场景规划嵌入 VLM 提示，配合带网格线与坐标的俯视图，按功能区域**分组迭代生成**物体位姿：首组以空场景视图为条件，后续组以当前已优化场景的俯视图为条件输入。每组生成后立即调用**物体检索模块**——先由 SBERT 粗检索（Top-60），再由 OpenCLIP 计算图文相似度精排，最后结合尺寸几何对齐进行加权评分（公式见 3.2 节），从 3D-FUTURE 及 Objavaverse 资产库中选取最佳 3D 资源。
3. **层次化优化** 在每组布局生成后介入，将所有空间约束（同级碰撞、边界、支撑、邻近、靠墙、朝向、对齐）分解为水平力、垂直力和旋转扭矩三个正交分量，在层次化支撑关系树上进行迭代力导向优化。优化器内建**死锁检测与回避**机制：当物体在时间窗口内的累积移动距离超过阈值 $\mathcal{D}_1$ 而起止位置净位移小于阈值 $\mathcal{D}_2$ 时判定为死锁，水平死锁施加垂直方向的逃逸力，垂直死锁则沿 Z 轴压缩物体尺度以打破僵局。优化收敛条件为系统残差力 $F_{residual}(t) < \epsilon_{\mathrm{conv}}$。
4. **场景编辑** 作为独立的交互通道，将任意文本编辑指令由 LLM 路由为 `plan` / `add` / `delete` / `move` 四种基本命令，随后复用布局生成与层次化优化模块完成实时修改，确保编辑后场景仍满足物理一致性约束。

Figure 2 和 Figure 3 分别展示了生成流水线与编辑流水线的完整架构。Figure 8 补充说明了物体获取的两种可选路径：检索式管线（基于语义与视觉相似度匹配固定数据库）与生成式管线（通过图像生成与 3D 重建获取库外物体）。

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of HOG-Layout. In the layout generation phase, layouts are generated sequentially according to groups and then optimized. The optimized scene is used as input for generating the layout for the next group. In the optimization phase, iterative optimization is performed according to the parent-child hierarchy, with optimization occurring simultaneously across different layers*



HOG-Layout 由四个关键模块构成：**场景规划 (Scene Planning)**、**布局生成 (Layout Generation)**、**层次化优化 (Hierarchical Optimization)** 和 **场景编辑 (Scene Editing)**。本节聚焦于前三个核心模块及其关键公式。

### 场景规划：基于 RAG 的约束检索与规划生成

场景规划模块负责将用户的文本描述转化为结构化的场景蓝图。其核心机制是检索增强生成（RAG）：系统预先构建一个布局约束规则模板库，使用文本嵌入模型（Qwen3-Embedding-4B）将每条规则编码为1024维特征向量，并存入 FAISS 向量数据库。当用户输入到来时，检索出最相关的三条布局规则，与用户输入一同送入 LLM，直接生成包含物体列表、房间信息、功能分组及场景描述的布局规划。

这一设计的关键在于：LLM 并非凭空生成约束，而是从可验证的规则库中检索先验知识，从而提升规划的结构化程度与语义合理性。

### 布局生成：分组迭代与多阶段物体检索

布局生成模块将场景规划嵌入 VLM 提示，并通过带网格线和坐标的俯视图逐组生成物体位姿。生成采用分组迭代策略：第一组使用空场景视图输入，后续组则使用当前已优化场景的俯视图作为输入——这种“生成-优化-再生成”的循环使得 VLM 能够感知已放置物体的空间上下文，避免全局一次性生成带来的冲突累积。

物体检索采用多阶段策略，从 3D 资产库（3D-FUTURE 及 Objaverse）中为每个规划物体匹配最佳 3D 模型。最终评分公式为：

$$Score_{Final}(i) = w_1 \cdot S_{sbert}(i) + w_2 \cdot S_{clip}(i) + w_3 \cdot S_{size}(i)$$

其中 $S_{sbert}(i)$ 为 SBERT 编码的语义相似度（用于粗检索，Top-60），$S_{clip}(i)$ 为 OpenCLIP 计算的图文相似度（用于精排），$S_{size}(i)$ 为物体尺寸与规划尺寸的几何对齐度，$w_1, w_2, w_3$ 为权重系数。消融实验（Table 4）证实，结合语义、视觉和几何三种信息后，检索准确率 CNT 从仅用 CLIP 的 75.34% 提升至 77.86%，ATR 从 63.05% 提升至 64.21%。

### 层次化优化：力导向物理仿真的数学框架

层次化优化是 HOG-Layout 的核心创新。其核心思想是：将所有复杂的场景布局规则——包括物理可行性（碰撞、边界）和语义逻辑（邻近、靠墙、对齐、朝向）——统一抽象并转化为模拟的连续物理力，通过迭代力导向优化使系统收敛至物理稳定、语义合理的状态。

#### 系统状态定义

整个场景在时刻 $t$ 的状态定义为所有物体状态的集合：

$$\mathcal{S}(t) = \{ O_1(t), O_2(t), \ldots, O_N(t) \}$$

单个物体 $i$ 的状态包含位置、偏航角和尺度：

$$O_i(t) = \{ p_i(t), \theta_i(t), s_i(t) \}$$

#### 力的分解与合成

优化器将约束力按方向分解为三个独立分量，分别驱动物体的不同自由度：

**水平合力**（驱动 XY 平面位移）：
$$F_{i, \mathrm{plane}}(t) = \sum_{k=1}^{K} \Delta F_{i, \mathrm{plane}}(k)$$

**垂直合力**（驱动 Z 轴位移）：
$$F_{i, \mathrm{vert}}(t) = \sum_{k=1}^{K} \Delta F_{i, \mathrm{vert}}(k)$$

**旋转扭矩**（驱动偏航角变化）：
$$\tau_i(t) = \sum_{k=1}^{K} \tau_k$$

其中 $K$ 为约束类型总数，包括：同级碰撞约束、边界约束、支撑约束（父子层级间）、邻近约束、靠墙约束、朝向约束和对齐约束。这种方向分解的设计使得不同自由度的优化可以独立进行，显著提升了收敛效率——实验表明，层次化力导向优化器（70.44秒）比梯度优化器（147.93秒）快约 2.1 倍。

#### 状态更新（欧拉积分）

每个时间步，物体状态根据合力与步长进行更新：

平面位置更新：
$$p_{i, \mathrm{plane}}(t+1) = p_{i, \mathrm{plane}}(t) + \alpha_{\mathrm{trans}} \cdot F_{i, \mathrm{plane}}(t)$$

垂直位置更新：
$$p_{i, \mathrm{vert}}(t+1) = p_{i, \mathrm{vert}}(t) + \alpha_{\mathrm{vert}} \cdot F_{i, \mathrm{vert}}(t)$$

偏航角更新：
$$\theta_i(t+1) = \theta_i(t) + \alpha_{\mathrm{rot}} \cdot \tau_i(t)$$

其中 $\alpha_{\mathrm{trans}}$、$\alpha_{\mathrm{vert}}$、$\alpha_{\mathrm{rot}}$ 分别为平移、垂直和旋转步长。

#### 死锁检测与回避

当物体在局部最优中振荡时，系统通过死锁检测机制介入：在时间窗口内，若物体在水平或垂直方向的累积移动距离超过阈值 $\mathcal{D}_1$，但窗口首尾的绝对位移小于阈值 $\mathcal{D}_2$，则判定为死锁。水平死锁通过施加垂直于死锁方向的力来打破；垂直死锁则直接沿 Z 轴收缩物体尺度。

#### 收敛判据

系统收敛通过残差力衡量——所有活跃约束力的总和：

$$F_{residual}(t) = \sum_{i=1}^{N} \left( \| F_{i, \mathrm{plane}}^{\prime}(t) \| + | F_{i, \mathrm{vert}}^{\prime}(t) | + | \tau_i(t) | \right)$$

当残差力低于收敛阈值 $\epsilon_{\mathrm{conv}}$ 时，优化终止：

$$F_{residual}(t) < \epsilon_{\mathrm{conv}}$$

消融实验（Table 3）为这一模块提供了决定性证据：移除层次化优化后（w/o HierOpt），物体碰撞率 COL_ob 从 5.28% 飙升至 36.46%，场景碰撞率 COL_sc 从 16.00% 升至 65.00%，保真度 OOR 从 43.09% 骤降至 35.85%，充分证明层次化力导向优化是保证物理可行性的关键机制。

### 补充图表

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/003_Figure_3.jpg]]
*Figure 3: The editing pipeline of HOG-Layout*

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/014_Figure_8.jpg]]
*Figure 8: Optional object acquisition methods. (a) The retrieval-based pipeline matches query text and geometry against a fixed database using semantic and visual similarity. (b) The generative pipeline replaces retrieval with generative objects: generating an image from text (e.g., via DALL-E) and then converting it to a 3D model (e.g., via Hunyuan 3D)*



## 实验与关键发现

### 核心性能对比

HOG-Layout 在 SceneEval 基准上对所有基线方法取得了全面且显著的领先。Table 1 报告了自动评估的完整指标，此处聚焦最能反映方法核心优势的几组关键数据。

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/004_Table_1.jpg]]
*Table 1: Evaluation results of different methods*

**物理合理性：碰撞与出界率大幅降低。** 物体级碰撞率 COL_ob 仅为 **5.28%**，相比最强基线 LayoutVLM 的 29.44% 降低了 **24.16 个百分点**；场景级碰撞率 COL_sc 为 16.00%，远低于 LayoutVLM 的 33.13%。出界率 OOB 控制在 2.45%，表明层次化力导向优化器对物理约束的建模极为有效。作为参照，LayoutGPT 无优化步骤，COL_ob 高达 39.07%；Holodeck 虽引入硬约束求解，COL_ob 仍为 27.47%，说明仅靠硬约束难以兼顾所有物理规则。

**保真度：语义关系遵循度最高。** 物体-物体关系保真度 OOR 达 **43.09%**，领先 LayoutVLM 5.00 个百分点；物体-建筑关系保真度 OAR 达 **75.74%**，领先 LayoutVLM 13.75 个百分点。支撑关系准确率 SUP 为 81.17%，进一步验证层次化支撑树结构对空间依赖建模的关键作用。

**语义合理性与视觉一致性。** 语义合理性评分 SP 为 **69.69**（GPT-5 评分，0-100），CLIP 相似度 CLIPsim 为 18.61，均优于所有基线。Figure 4 的 SP 得分核密度估计分布显示，HOG-Layout 在高分段（>70）的密度明显高于其他方法，表明其生成的场景在语义连贯性上具有稳定优势。

**生成效率。** HOG-Layout 平均生成时间 **70.44 秒**，约为 LayoutVLM 梯度优化器（147.93 秒，见 Table 3 中 w/ GradOpt）的一半，验证了力分解策略在优化效率上的显著优势。

### 人工评估

Table 2 报告了 15 名用户对生成场景的 7 分制评分。HOG-Layout 在物理合理性上得分 **5.33 ± 0.88**，在语义对齐度上得分 **5.75 ± 0.87**，均显著高于所有基线（LayoutGPT 分别为 3.87 和 4.13，Holodeck 分别为 4.53 和 4.67，LayoutVLM 分别为 4.93 和 5.07）。人工评估与自动指标高度一致，说明 SceneEval 的自动度量能够有效反映人类感知的质量差异。

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/007_Table_2.jpg]]
*Table 2: Human evaluation results*

### 消融实验

Table 3 系统拆解了 HOG-Layout 各组件的贡献，结论清晰且证据强度极高。

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/008_Table_3.jpg]]
*Table 3: Results of ablation study*

**层次化优化器是关键支柱。** 移除层次化优化模块（w/o HierOpt）后，系统退化为纯 VLM 生成，所有物理指标崩溃：COL_ob 从 5.28% 飙升至 **36.46%**，COL_sc 从 16.00% 飙升至 **65.00%**，OOB 从 2.45% 升至 7.30%。保真度 OOR 从 43.09% 骤降至 35.85%，SP 从 69.69 降至 67.77。这直接证明了力导向优化对物理可行性和语义保真度的决定性作用。

**力导向优化优于梯度优化。** 将层次化力导向优化器替换为 LayoutVLM 的梯度下降优化器（w/ GradOpt），生成时间从 70.44 秒延长至 **147.93 秒**，且 OOR 降至 38.09%，COL_ob 升至 29.44%。力分解策略不仅更快，而且优化质量更高，原因在于梯度优化易陷入局部最优，而力导向方法配合死锁检测能有效跳出。

**RAG 模板规则库提升语义规划。** 移除 RAG（w/o RAG）后，OOR 降至 37.89%，SP 降至 67.08，表明检索增强的布局约束模板对 LLM 场景规划中的语义合理性有实质贡献。

**场景规划各组件均有贡献。** 仅保留房间规划（only room planning）导致 OOR 降至 37.34%、COL_ob 升至 11.44%；移除布局描述（w/o layout description）或物体数据（w/o object data）同样使各项指标全面下滑，其中物体数据的影响最大（OOR 降至 36.79%，SP 降至 67.07），说明详细的物体规格信息是 VLM 生成精确布局的前提。

**多阶段检索优于单一模态。** Table 4 对比了三种检索策略：仅 CLIP 的 CNT 为 75.34%、ATR 为 63.05%；CLIP+SBERT 提升至 77.01% 和 63.85%；加入尺寸对齐（CLIP+SBERT+SIZE）后达到最优 **77.86% CNT、64.21% ATR**。语义、视觉和几何信息的互补性得到了量化验证。

### 场景编辑评估

Table 7 报告了编辑模块的量化结果。添加（add）和删除（delete）指令的编辑成功率 ESR 均达到 **100%**，场景级碰撞率仅 5%，出界率 0%。移动（move）指令的成功率为 **80%**，伴有 10% 的碰撞和出界率——这一差距源于自然语言空间描述的固有歧义（“移到桌子旁边”缺乏精确距离定义），是当前方法的主要瓶颈。Table 5 显示编辑操作在简单场景中平均耗时约 15-20 秒，复杂场景约 35-45 秒，具备实时交互的可行性。

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/019_Table_7.jpg]]
*Table 7: Quantitative results of scene editing. We report the Editing Success Rate (ESR), Scene-level Collision*

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/010_Table_5.jpg]]
*Table 5: Editing time results*

### 可视化分析

Figure 5 的定性对比直观展示了 HOG-Layout 的优势：LayoutGPT 常产生物体重叠和位置不合理；Holodeck 虽满足硬约束，但物体朝向和语义分组欠佳；LayoutVLM 在复杂场景中出现物体遗漏。HOG-Layout 生成的场景在物体位置、朝向、分组和指令遵循上均最接近预期。Figure 6 的编辑示例验证了移动、添加、删除操作的端到端可行性。

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/006_Figure_5.jpg]]
*Figure 5: Generation Examples of different methods on the benchmark*

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/009_Figure_6.jpg]]
*Figure 6: Editing Examples*

### 失败模式与局限

消融实验中 w/o HierOpt 的碰撞率飙升（COL_sc 65%）揭示了纯 VLM 输出的根本缺陷：VLM 缺乏对物理连续约束的隐式建模能力，仅靠视觉推理无法保证碰撞避免和边界遵循。移动指令 80% 的成功率暴露了自然语言空间指代的解析瓶颈，需要交互式消歧或更精确的空间锚定机制。此外，当前框架依赖预定义 3D 资产库，对库外物体的生成式获取耗时较长（≥10 秒）且质量不稳定，限制了开放词汇场景合成的实用性。

### 补充图表

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/005_Figure_4.jpg]]
*Figure 4: Results of SP Score Distribution (Kernel Density Estimation, KDE) of different methods*

![[assets/figures/papers/paper_list_l2170_https_arxiv_org_abs_2604_10772/figures/011_Table_4.jpg]]
*Table 4: Comparison of retrieval methods*



## 定位与知识库关联

### 问题瓶颈与核心思路

现有基于 VLM 的 3D 场景生成方法普遍存在一个根本性瓶颈：**缺乏对物理一致性的显式建模**。纯文本或视觉输出的布局生成无法保证场景中物体的空间关系、支撑逻辑和边界约束，常导致碰撞、不合理放置以及较低的语义遵循度。HOG-Layout 的核心洞察在于将场景优化建模为**基于层次结构的力导向物理仿真**——通过将复杂的空间约束转化为可叠加的连续力，使 VLM 预测的初始布局逐步收敛至物理上稳定、语义上合理的最终状态。

### 与现有方法的本质差异

HOG-Layout 与三类代表性基线方法在场景组织方式、布局生成策略和优化机制三个关键维度上存在根本性分歧：

**LayoutGPT** 采用基于 LLM 的单步文本到布局生成范式，将场景视为平坦的物体列表，缺乏显式的结构组织与优化步骤。其输出直接依赖语言模型的推理能力，无法对碰撞、支撑等物理约束进行后验修正。HOG-Layout 则引入层次化支撑关系树，将场景中的物体按父子支撑关系组织为不同层级（如 floor 作为父节点，所有直接接触地面的物体作为其子节点），并通过迭代力导向优化消除冲突。

**Holodeck** 虽然引入了空间关系约束，但其核心策略是通过 DFS/MILP 求解器保证硬物理约束，本质上是一种离散约束满足方法。该方法忽视了软语义约束（如“靠近墙壁”“面向窗户”等模糊描述），且求解过程与语义生成完全解耦。HOG-Layout 将所有约束——无论是物理可行性（碰撞、边界）还是语义逻辑（邻近、靠墙、朝向、对齐）——统一抽象为方向分解的连续力（水平力、垂直力、旋转扭矩），在同一个优化框架内同时处理硬约束与软约束。

**LayoutVLM** 利用 VLM 联合文本与视觉信息进行可微分优化，是最接近 HOG-Layout 的基线。然而，该方法需要预定义物体集，且其梯度下降优化器耗时极长（147.93秒 vs HOG-Layout 的 70.44秒）。HOG-Layout 的层次化力导向优化器在效率上实现约 2.1 倍加速的同时，所有关键物理/语义指标均显著占优（Table 3, w/ GradOpt vs HOG-Layout），证明了力分解和层级优化的结构性优势。

### 关键设计决策的因果链

1. **层次化组织 → 分解推理空间**：通过将场景按支撑关系分层，VLM 和优化模块只需关注同一层级内的物体间依赖关系，降低了联合推理的复杂度。这是 HOG-Layout 在保真度（OOR: 43.09% vs LayoutVLM 38.09%）和物理合理性（COL_ob: 5.28% vs LayoutVLM 29.44%）上取得显著提升的结构性原因。

2. **力分解 → 优化效率与稳定性**：将复杂约束分解为水平力、垂直力和旋转扭矩三个独立分量，使状态更新可以采用简单的欧拉积分（公式 7-9），避免了梯度优化中的高维搜索和局部震荡问题。消融实验表明，移除层次化优化模块（w/o HierOpt）后，物体碰撞率 COL_ob 从 5.28% 飙升至 36.46%，场景碰撞率 COL_sc 从 16.00% 升至 65.00%，保真度 OOR 从 43.09% 降至 35.85%（Table 3），验证了优化模块对生成质量的决定性作用。

3. **死锁检测与回避 → 突破局部最优**：力导向优化本身容易陷入局部极小值。HOG-Layout 通过监测时间窗口内的累积移动距离与绝对位移的比值来判定死锁（Section 3.3.3），并对水平死锁施加垂直方向的逃逸力，对垂直死锁直接缩放物体尺寸，这一机制是优化器能够收敛到全局可行解的关键保障。

4. **RAG 模板规则库 → 语义合理性**：通过 FAISS 向量数据库检索最相关的布局约束模板，将其嵌入 LLM 的场景规划提示中，使生成布局在语义上更符合常识。移除 RAG 后，保真度 OOR 下降至 37.89%，语义合理性 SP 降至 67.08（Table 3），证实了检索增强的模板规则对布局规划质量的提升作用。

### 适用边界与局限

1. **场景类型的泛化性未经验证**：当前实验局限于室内场景（SceneEval 基准），层次化支撑树的构建逻辑（floor/wall/ceiling 作为父节点）天然适配室内环境，但尚未验证在户外或大规模开放场景下的有效性。户外场景中物体的支撑关系更为复杂（如地形起伏、动态物体），力导向优化的超参数可能需要重新校准。

2. **移动指令的编辑鲁棒性不足**：场景编辑中移动指令的成功率相对较低（80%），且伴有 10% 的碰撞和出界率（Table 7）。这主要源于自然语言空间描述固有的歧义性——例如“移到桌子旁边”缺乏精确的距离和方向定义，力导向优化在此类欠约束条件下难以确定唯一解。

3. **资产获取的闭环依赖**：HOG-Layout 依赖现有的 3D 资产库（3D-FUTURE 及 Objaverse）进行多阶段检索（SBERT 粗检索 + OpenCLIP 精排 + 尺寸对齐），对于库中不存在的物体需借助生成式对象获取，但生成式管线耗时较长（≥10秒）且质量不稳定。这限制了方法在开放词汇场景下的适用性。

4. **物理仿真的简化假设**：当前力导向优化仅考虑碰撞、边界、支撑、邻近、靠墙、朝向和对齐等约束，未引入摩擦力、重力、动量等更丰富的物理仿真要素。这意味着优化结果虽然避免了穿透和悬空，但未必符合真实世界的力学平衡条件。

### 开放问题与后续方向

1. **层次化力导向框架的跨域迁移**：能否将该框架扩展到室外场景或包含动态物体的环境中？这需要重新定义层次结构的构建规则和约束力的计算方式。

2. **生成式资产获取的集成**：能否完全使用生成式 AI 替代检索式资产获取，实现零样本、开放词汇的场景合成？这需要解决生成质量与推理速度的权衡问题。

3. **物理仿真的深化**：引入摩擦力、重力等更丰富的物理仿真能否进一步提升布局的真实性？这可能需要在力导向优化与刚体物理引擎之间建立接口。

4. **交互式编辑的消歧机制**：如何提高移动指令的编辑鲁棒性？可能的路径包括交互式消歧（主动询问用户精确位置）或更精确的空间指代解析（如结合点云或深度信息）。

5. **超参数的自适应校准**：力导向优化中的大量超参数（权重、步长、死锁阈值等）虽经自动调参，但在不同场景规模下可能需要重新校准。开发场景规模自适应的参数调节机制是提升泛化性的关键。



## 原文 PDF

![[paperPDFs/CVPR_2026/HOG_Layout_Hierarchical_3D_Scene_Generation_Optimization_and_Editing_via_Vision_Language_Models.pdf]]

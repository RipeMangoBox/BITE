---
title: "RobotSeg: A Model and Dataset for Segmenting Robots in Image and Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RobotSeg_A_Model_and_Dataset_for_Segmenting_Robots_in_Image_and_Video.pdf
project_link: null
code_link: "https://github.com/showlab/RobotSeg"
aliases:
- RobotSeg
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过结构增强的记忆关联模块（SEMA）注入机器人结构先验，并利用机器人提示生成器（RPG）实现自动分割，同时采用仅需首帧掩码的标注高效训练策略（LET）打破标签稀缺瓶颈，从而系统性地提升分割准确性和时序稳定性。
primary_logic: 在SAM 2基础上，引入边界感知的结构记忆、可学习类别令牌与历史聚类对象令牌，结合循环一致性、语义一致性和块一致性损失仅用首帧标注进行视频训练，使模型习得结构感知且时序一致的自主分割能力。
claims:
- 引入结构增强记忆关联器、机器人提示生成器和标注高效训练策略，在仅用首帧掩码的条件下实现了自动、结构感知的视频机器人分割。
- 在VRS数据集全自动设置下，RobotSeg相比RoVi-Aug和RoboEngine提升至少4.9 J&F，参数量仅41.3M。
- 消融实验证明所有组件（SEMA的多尺度感知与记忆引导调制，RPG的类令牌与对象令牌，LET的层次损失）均带来稳定提升，全模型J&F达到85.1。
- VRS (Whole Robot) 上 J&F (AU) = 87.9
---

# RobotSeg: A Model and Dataset for Segmenting Robots in Image and Video

> [!tip] 核心洞察
> 在SAM 2基础上，引入边界感知的结构记忆、可学习类别令牌与历史聚类对象令牌，结合循环一致性、语义一致性和块一致性损失仅用首帧标注进行视频训练，使模型习得结构感知且时序一致的自主分割能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | RobotSeg：机器人图像和视频分割的基础模型与数据集 |
| 英文题名 | RobotSeg: A Model and Dataset for Segmenting Robots in Image and Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22950) · [Code](https://github.com/showlab/RobotSeg) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RobotSeg |
| Dataset | VRS, Computational Efficiency |

> [!tip] 效果简介
> - VRS (Whole Robot) 上，J&F (AU) 87.9 vs 38.9 (RoVi-Aug) (+49.0)；mIoU (AU) 85.1 vs 73.6 (SAM 2.1 Finetuned) (+11.5)。
> - VRS (Robot Arm) 上，mIoU (AU) 75.6 vs 23.8 (EVF-SAM) (+51.8)。
> - Computational Efficiency 上，FLOPs (G) 319.8 vs 284.3 (SAM 2.1) (+35.5)。

## 概述

机器人分割是视觉感知中的一项基础任务，在策略学习、数据增强、3D重建和操作等下游应用中扮演关键角色。然而，现有通用分割模型（如SAM 2、RoboEngine）在面对机器人场景时暴露出三个系统性瓶颈：

1. **铰接结构多样性**：机器人的多关节形态、快速形变和与背景的混淆，导致分割不完整且时序不一致。
2. **人工提示依赖**：主流模型需要手动提供点击或边界框，无法支持自主分割。
3. **标注成本过高**：视频分割通常需要逐帧掩码标注，而机器人视频的标注成本远超自然场景。

针对上述问题，**RobotSeg** 在SAM 2基础之上引入三项关键创新，构建了首个结构感知、自动且标注高效的视频机器人分割框架：

- **结构增强记忆关联器（SEMA）**：通过边缘图调制、多尺度结构感知和记忆引导的结构图生成，将机器人边界先验注入时序特征精炼过程。
- **机器人提示生成器（RPG）**：利用可学习类别令牌和历史特征聚类生成的对象令牌，替代人工提示实现自主分割。
- **标注高效训练策略（LET）**：仅需首帧掩码标注，通过循环一致性、语义一致性和块一致性三层损失驱动视频级自监督学习。

在VRS数据集的全自动设置下，RobotSeg以仅41.3M参数量达到85.1 J&F，相比微调后的SAM 2.1提升11.5个百分点，较RoVi-Aug和RoboEngine分别领先49.0和4.9 J&F。消融实验证实，SEMA的多尺度感知与记忆引导调制、RPG的类令牌与对象令牌、以及LET的层次化损失均带来稳定且可叠加的性能增益。

在方法谱系上，RobotSeg位于**视频实例分割**与**机器人感知**的交叉点。它继承SAM 2的记忆注意力范式，但通过结构先验注入和提示生成机制将其改造为领域专用架构；与RoVi-Aug、RoboEngine等图像级方法相比，它首次实现了视频层面的时序一致分割；相较于CLIPSeg、LISA、EVF-SAM等语言条件分割模型，它不依赖文本描述即可完成自主分割，且精度大幅领先（在机械臂分割上领先EVF-SAM达51.8 mIoU）。

## 背景与动机

机器人正从受控的工业产线走向非结构化环境，与人类共享物理空间并执行复杂操作。在这一趋势下，精确地从图像和视频中分割出机器人本体——包括机械臂、夹爪等铰接部件——成为场景理解、人机交互、数据增强和策略学习等下游任务的共性基础。然而，机器人分割面临着独特的挑战：机器人形态高度多样（单臂、双臂、移动机械手等），铰接结构导致快速且非刚性的形变，且常与背景纹理相似，极易引发混淆。

通用分割模型在这些挑战面前表现乏力。以 **SAM 2.1** 为代表的提示式视频分割模型虽然具备强大的泛化能力，但缺乏对机器人铰接结构的建模，导致分割结果不完整、边界模糊且时序不一致（Figure 1）。专门面向机器人的图像分割方法如 **RoVi-Aug** 和 **RoboEngine** 虽然引入了领域先验，却无法处理视频输入，且在全自动设置下精度有限。语言条件的分割方法（如 **CLIPSeg**、**LISA**、**EVF-SAM**）依赖文本描述来定位目标，但机器人部件的语义描述往往过于抽象，难以精确对应视觉特征，尤其在夹爪等细小部件上表现不佳。

更深层的瓶颈在于标注成本。视频分割通常需要逐帧标注掩码，而机器人视频的帧数庞大、形变剧烈，使得全标注几乎不可行。这导致现有的机器人分割数据集规模极小——例如 RoboEngine 仅包含 3,629 张静态图像，缺乏视频级别的时序标注，无法支撑视频分割模型的训练。

上述缺口共同指向一个核心矛盾：**通用模型不懂机器人结构，专用模型不懂视频时序，而两者都受困于标注稀缺**。RobotSeg 正是在这一背景下提出的，旨在构建一个结构感知、自动执行且标注高效的视频机器人分割基础模型。

## 核心创新

RobotSeg 的核心创新在于系统性地解决了通用分割基础模型（以 SAM 2 为代表）在机器人场景中的三个关键瓶颈：**缺乏对铰接结构的适应能力**、**依赖人工提示**、以及**需要逐帧密集标注**。为此，RobotSeg 在 SAM 2 架构上引入了三个相互协同的“changed slots”，形成了结构感知、自主提示、标注高效的统一框架。

### 结构增强的记忆关联器（SEMA）：从时序集成到结构感知

SAM 2 的标准记忆关联器仅执行时序特征集成，缺乏对机器人铰接边界的显式建模。SEMA 通过双分支设计注入结构先验：

- **上分支（时序集成）**：当前帧特征 $F_t$ 经自注意力和与记忆 $M_t$ 的交叉注意力后，通过 MLP 精炼得到时序增强特征 $F_t'$：
  $$F_{t}^{\prime} = \mathrm{MLP}\big(\mathrm{CrossAttn}(\mathrm{SelfAttn}(F_{t}), M_{t})\big)$$

- **下分支（结构感知）**：用 Canny 算子提取边缘图 $E_t$ 对特征进行调制 $F_{t}^{\mathrm{edge}} = F_{t} \odot (1 + E_{t})$，再经多尺度感知器提取多尺度结构特征 $\boldsymbol{F}_{t}^{\mathrm{ms}}$，与记忆做交叉注意力后通过 sigmoid 生成结构图 $\boldsymbol{S}_{t}$：
  $$\begin{array}{r} \boldsymbol{F}_{t}^{\mathrm{ms}} = \boldsymbol{\mathcal{MS}}(\boldsymbol{F}_{t}^{\mathrm{edge}}), \\ \boldsymbol{S}_{t} = \sigma(\mathrm{CrossAttn}(\boldsymbol{F}_{t}^{\mathrm{ms}}, \boldsymbol{M}_{t})) \end{array}$$

- **结构增强融合**：将结构图 $\boldsymbol{S}_{t}$ 与可学习权重 $\alpha$ 叠加回时序特征：
  $$F_{t}^{\prime\prime} = F_{t}^{\prime} \odot \left(1 + \alpha S_{t}\right)$$

这一设计的关键因果机制在于：边缘调制使模型对机器人关节、夹爪等结构边界敏感，而记忆引导的结构图生成则利用历史掩码信息抑制背景混淆。消融实验证实，仅添加多尺度感知和结构调制即可将 J&F 从 73.6 提升至 80.1（Table 4）。

### 机器人提示生成器（RPG）：从人工提示到自主分割

SAM 2 依赖用户提供的点击或边界框来初始化分割。RPG 通过两类可学习令牌实现完全自主的语义提示：

- **类令牌（Class Tokens）**：从可学习令牌库中根据目标类别（如“机械臂”、“夹爪”、“整体机器人”）检索，提供语义先验。
- **对象令牌（Object Tokens）**：通过层次聚类策略（Algorithm 1）从历史记忆特征中动态提取。该策略先在掩码区域内划分宏区域（macro regions），再在每个区域内进行微聚类（micro clusters），生成代表不同实例或部件的对象令牌，传递时序线索。

这两类令牌共同替代了人工提示，使模型能够在无任何用户输入的情况下自主启动分割。消融实验表明，引入类令牌和对象令牌后，全自动设置下的 J&F 从 80.1 进一步提升至 83.4（Table 4）。

### 标注高效训练策略（LET）：从逐帧标注到首帧掩码

SAM 2 的训练需要视频每一帧的掩码标注，这在机器人数据上成本极高。LET 仅需首帧真值掩码 $G_0$，通过三个层次的一致性损失实现自监督：

- **视频级循环一致性损失**：前向传播掩码 $M_0^f$ 和后向传播掩码 $M_0^b$ 分别与首帧真值计算 Dice 损失，强制时序传播的闭环一致性：
  $$\mathcal{L}_{\mathrm{cyc}} = \mathcal{D}(M_{0}^{f}, G_{0}) + \mathcal{D}(M_{0}^{b}, G_{0})$$

- **对象级语义一致性损失**：强制中间帧预测掩码的对象语义特征 $\mathbf{f}_{x}$ 与首帧特征 $\mathbf{f}_{0}$ 对齐：
  $$\mathcal{L}_{\mathrm{sem}} = 1 - \frac{1}{|\mathcal{T}|} \sum_{x \in \mathcal{T}} \left( \frac{\mathbf{f}_{x} \cdot \mathbf{f}_{0}}{\|\mathbf{f}_{x}\| \|\mathbf{f}_{0}\|} \right)$$

- **块级一致性损失**：利用 DINOv3 特征传播生成伪标签 $P_x$，在下采样 16 倍的分辨率上用 IoU 损失监督预测掩码：
  $$\mathcal{L}_{\mathrm{patch}} = \frac{1}{|T|} \sum_{x \in \mathcal{T}} \mathcal{D}^{\prime}(M_{x}^{\downarrow 16}, P_{x})$$

总掩码损失为三者加权和：
$$\mathcal{L}_{\mathrm{mask}} = w_{\mathrm{cyc}} \mathcal{L}_{\mathrm{cyc}} + w_{\mathrm{sem}} \mathcal{L}_{\mathrm{sem}} + w_{\mathrm{patch}} \mathcal{L}_{\mathrm{patch}}$$

消融实验验证了层次化设计的有效性：逐步添加循环、语义和块一致性损失使 J&F 从 73.6 单调提升至 77.4（Table 4）。

### 创新协同与证据强度

三个 changed slots 并非独立运作，而是形成正向协同：SEMA 提供的结构感知特征为 RPG 的对象聚类提供了更干净的历史特征；RPG 生成的自主提示使 LET 的循环传播有了准确的起点；LET 的首帧训练策略则降低了对大规模标注的依赖，使整个框架在实际机器人数据上可部署。全模型在 VRS 数据集上达到 85.1 J&F，相比微调后的 SAM 2.1（73.6）提升 +11.5，参数量仅从 39.0M 微增至 41.3M（Table 5、Table 8），所有组件贡献均通过消融实验得到验证。

## 整体框架

RobotSeg 以 SAM 2 为基础骨架，将其重构为面向机器人的视频分割框架。模型输入为一段视频序列，输出为每帧中指定目标（整体机器人、机械臂或夹爪）的分割掩码，同时支持自动分割与用户交互（点击、边界框）两种模式。如图 4 所示，整个 pipeline 由四个核心模块串联构成：

1. **逐帧视觉编码**：图像编码器（与 SAM 2 共享）独立提取每帧的多尺度视觉特征 $F_t$。
2. **结构增强记忆关联器（SEMA）**：将历史帧特征与掩码编码为记忆 $M_t$，通过交叉注意力对当前帧特征进行时序精炼，并利用边缘感知分支注入机器人结构先验，输出结构增强的时序特征 $F_t''$。
3. **机器人提示生成器（RPG）**：从可学习的类别令牌库中检索语义令牌，同时对记忆中的历史掩码区域特征进行层次聚类生成对象令牌，二者共同构成自动分割的提示输入。
4. **掩码解码器**：以图像嵌入、提示令牌和机器人令牌为条件，预测当前帧的分割掩码。

训练阶段，RobotSeg 采用标注高效训练策略（LET），仅需首帧的真实掩码 $G_0$，通过循环一致性、语义一致性和块一致性三个层次的损失函数驱动模型学习时序稳定的分割能力，从而打破逐帧标注的瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/006_Figure_4.jpg]]
*Figure 4: Overview of our RobotSeg. Building upon SAM 2 [44], it introduces a structure-enhanced memory associator, a robot prompt generator, and a label-efficient training strategy to enable structure-aware, automatic, and training-label-efficient robot segmentation*

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/027_Figure_18.jpg]]
*Figure 18: Architecture details of the mask decoder*

## 核心模块与公式推导

RobotSeg 在 SAM 2 基础之上引入三个关键模块：结构增强记忆关联器（SEMA）、机器人提示生成器（RPG）和标注高效训练策略（LET）。三个模块协同工作，使模型在仅需首帧掩码的条件下实现结构感知、时序一致的全自动视频机器人分割。

### 结构增强记忆关联器（SEMA）

SEMA 的核心设计思想是：标准记忆注意力缺乏对机器人铰接边界和结构拓扑的感知能力，导致分割在关节处断裂或与背景混淆。SEMA 通过双分支架构同时进行时序上下文集成和结构感知增强（Figure 5）。

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/007_Figure_5.jpg]]
*Figure 5: Illustration of the structure-enhanced memory associator. It encodes previous features and masks into memory to guide temporal context integration in the top branch and robot boundary perception in the bottom branch, where detected boundaries are used for structure enhancement of the top features*

**时序特征精炼**：当前帧特征 $F_t$ 首先经过自注意力，再与记忆 $M_t$（编码了历史帧特征和掩码）进行交叉注意力，最后通过 MLP 得到精炼特征：

$$F_{t}^{\prime} = \mathrm{MLP}\big(\mathrm{CrossAttn}(\mathrm{SelfAttn}(F_{t}), M_{t})\big)$$

**边界感知调制**：并行地，对当前帧应用 Canny 边缘检测得到边缘图 $E_t$，用以显式增强机器人边界信息：

$$F_{t}^{\mathrm{edge}} = F_{t} \odot (1 + E_{t})$$

**多尺度结构感知与记忆引导**：将边缘调制后的特征 $F_{t}^{\mathrm{edge}}$ 送入多尺度感知器 $\mathcal{MS}$ 提取多尺度结构特征，再与记忆 $M_t$ 做交叉注意力，经 sigmoid 激活生成结构图 $S_t$：

$$\begin{array}{r} \boldsymbol{F}_{t}^{\mathrm{ms}} = \boldsymbol{\mathcal{MS}}(\boldsymbol{F}_{t}^{\mathrm{edge}}), \\ \boldsymbol{S}_{t} = \sigma(\mathrm{CrossAttn}(\boldsymbol{F}_{t}^{\mathrm{ms}}, \boldsymbol{M}_{t})) \end{array}$$

**结构增强融合**：最终将结构图 $S_t$ 与可学习权重 $\alpha$ 叠加到时序精炼特征上，得到结构增强的帧特征：

$$F_{t}^{\prime\prime} = F_{t}^{\prime} \odot \left(1 + \alpha S_{t}\right)$$

这一设计的因果机制在于：边缘图提供底层几何线索，多尺度感知器捕获不同粒度的结构模式，记忆引导的交叉注意力则将历史结构信息注入当前帧，三者叠加使模型对机器人铰接边界和部件拓扑具有显式感知。

### 机器人提示生成器（RPG）

RPG 解决了 SAM 2 依赖人工点击或框提示的瓶颈，实现全自动分割。其核心是生成两类机器人令牌（Figure 6）：

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/008_Figure_6.jpg]]
*Figure 6: Illustration of the robot prompt generator. It generates two types of robot tokens: class tokens retrieved according to the segmentation target (e.g., arm, gripper, or robot), and object tokens derived by clustering historical features within masked regions*

- **类令牌**：从一个可学习的令牌库中根据目标类别（如整体机器人、机械臂、夹爪）检索对应语义先验，为分割提供类别级引导。
- **对象令牌**：通过对历史记忆特征在掩码区域内的层次聚类动态提取，传递时序对象线索。层次聚类策略（Algorithm 1）先划分宏观区域再细分微观簇，确保令牌覆盖机器人不同部件。

两类令牌与图像嵌入、提示令牌（如有）一同输入掩码解码器，使模型在无人工干预下自主定位并分割机器人。

### 标注高效训练策略（LET）

LET 的瓶颈突破在于：仅用视频首帧的真值掩码 $G_0$ 即可完成视频级训练，无需逐帧标注。其核心是三个层次的一致性损失（Figure 7）：

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/009_Figure_7.jpg]]
*Figure 7: Illustration of our label-efficient training strategy. It enables video learning using only the ground-truth mask of the first frame. It consists of (1) a video-level cycle consistency loss, (2) an object-level semantic consistency loss, and (3) a patch-level consistency loss*

**视频级循环一致性损失**：将首帧掩码沿时间轴前向传播至末帧再反向传播回首帧，约束传播结果与真值一致：

$$\mathcal{L}_{\mathrm{cyc}} = \mathcal{D}(M_{0}^{f}, G_{0}) + \mathcal{D}(M_{0}^{b}, G_{0})$$

其中 $\mathcal{D}$ 为 Dice 损失与二元交叉熵损失的组合，$M_{0}^{f}$ 和 $M_{0}^{b}$ 分别为前向和后向传播回首帧的预测掩码。

**对象级语义一致性损失**：强制中间帧预测掩码的对象语义与首帧对齐，通过特征余弦相似度约束：

$$\mathcal{L}_{\mathrm{sem}} = 1 - \frac{1}{|\mathcal{T}|} \sum_{x \in \mathcal{T}} \left( \frac{\mathbf{f}_{x} \cdot \mathbf{f}_{0}}{\|\mathbf{f}_{x}\| \|\mathbf{f}_{0}\|} \right)$$

其中 $\mathcal{T}$ 为中间帧集合，$\mathbf{f}_{x}$ 和 $\mathbf{f}_{0}$ 分别为第 $x$ 帧和首帧预测掩码区域的特征向量。

**块级一致性损失**：利用 DINOv3 的块相似度将首帧真值掩码传播至其他帧生成伪标签 $P_x$，在下采样 16 倍的分辨率上监督预测掩码：

$$\mathcal{L}_{\mathrm{patch}} = \frac{1}{|T|} \sum_{x \in \mathcal{T}} \mathcal{D}^{\prime}(M_{x}^{\downarrow 16}, P_{x})$$

其中 $\mathcal{D}^{\prime}$ 为 IoU 损失。

**总掩码损失**为三者的加权和：

$$\mathcal{L}_{\mathrm{mask}} = w_{\mathrm{cyc}} \mathcal{L}_{\mathrm{cyc}} + w_{\mathrm{sem}} \mathcal{L}_{\mathrm{sem}} + w_{\mathrm{patch}} \mathcal{L}_{\mathrm{patch}}$$

消融实验（Table 4）验证了三个损失的层次化叠加带来稳定提升：仅微调 SAM 2.1 得 73.6 J&F，依次加入循环、语义和块一致性损失后提升至 77.4，验证了 LET 在标签稀缺条件下的有效性。

## 实验与分析

### 核心实验设置

所有实验均在统一条件下进行：训练使用8张NVIDIA RTX A5000 GPU，统一25个epoch，优化器和学习率调度完全一致。所有对比方法均在同一VRS数据集上训练或评估，使用官方实现或公开权重，确保公平比较。主要评价指标为J&F（区域相似度与轮廓准确度的均值）和mIoU，覆盖全自动（AU）、1-点击（1C）、3-点击（3C）、边界框（BB）和在线交互（OI）五种分割设置。

### 视频机器人分割主结果（Table 2）

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/012_Table_2.jpg]]
*Table 2: Comparisons of the video robot segmentation under five settings (i.e., automatic AU, 1-click 1C, 3-click 3C, bounding-box BB, and online-interactive OI) on the VRS dataset. “–” denotes that the method does not support this setting*

在VRS数据集的全自动设置下，RobotSeg取得**87.9 J&F**，相比RoVi-Aug（38.9）和RoboEngine（83.0）分别提升**+49.0**和**+4.9**。在1-点击、3-点击和边界框设置下，RobotSeg同样全面优于所有现有方法，且参数量仅**41.3M**，远小于RoVi-Aug（≥638.5M）等模型。

值得注意的是，SAM 2.1在未使用机器人数据微调时仅得38.2 J&F，经领域数据微调后提升至73.6，凸显了领域适应对机器人分割的关键作用。RobotSeg在此基础上通过三个创新模块将性能进一步提升至85.1 mIoU（Table 5），证明了结构感知与自主提示机制的有效性。

### 图像机器人分割结果（Table 3）

在RoboEngine图像数据集上，RobotSeg同样表现出色。全自动设置下，RobotSeg以显著优势超越RoboEngine和RoVi-Aug，在1-点击、3-点击和边界框设置下也保持领先。这验证了RobotSeg不仅在视频场景中有效，在静态图像分割任务上也具备强泛化能力。

### 分类型细粒度分析（Tables 5-7）

按10种机器人形态细分后，RobotSeg在“整体机器人”（Table 5）、“机械臂”（Table 6）和“夹爪”（Table 7）三个子任务上均展现出一致优势。以机械臂分割为例，RobotSeg全自动设置下达到**75.6 mIoU**，而EVF-SAM仅得23.8，差距高达**+51.8**。在夹爪分割中，EVF-SAM常将暗色夹爪与背景混淆，RobotSeg则能稳定分割正确组件并保持时序一致性（Figure 15）。

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/024_Figure_15.jpg]]
*Figure 15: Qualitative comparison of robot gripper segmentation under the automatic setting. EVF-SAM [74] frequently misidentifies the gripper or mistakes background regions for the target, while our RobotSeg consistently segments the correct component with stable temporal behavior*

### 消融实验（Table 4）

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/013_Table_4.jpg]]
*Table 4: Ablation studies. “✓” indicates the component is enabled. “–” denotes unavailable results*

消融实验逐层验证了各组件的贡献：
- **基线微调**：SAM 2.1在机器人数据上微调后，J&F从38.2提升至73.6，构成后续改进的起点。
- **标注高效训练（LET）**：逐步引入循环一致性损失、语义一致性损失和块一致性损失，使J&F从73.6提升至77.4，验证了层次化自监督在仅用首帧掩码条件下的有效性。
- **机器人提示生成器（RPG）**：引入类令牌和对象令牌后，模型支持自动分割，J&F进一步提升。
- **结构增强记忆关联器（SEMA）**：加入多尺度感知和记忆引导的结构调制后，全模型达到**85.1 J&F**，所有组件均带来稳定增益，无冗余设计。

### 计算效率对比（Table 8）

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/021_Table_8.jpg]]
*Table 8: Comparison of the computational efficiency of different methods. For each method, we list model parameters, FLOPs, and average inference time per frame*

RobotSeg参数量为41.3M，FLOPs为319.8G，相比SAM 2.1（39.0M，284.3G）仅增加约12%的计算开销，但性能提升显著。单帧平均推理时间保持在同一量级，在精度与效率之间取得了良好平衡。

### 定性分析与失败模式

**成功案例**：Figure 13-15展示了全自动设置下的定性对比。RoboEngine在全自动整体分割中存在明显的时序不一致和掩码不完整问题，而RobotSeg输出准确且时序稳定的掩码。EVF-SAM在机械臂和夹爪分割中常将背景物体误判为目标，RobotSeg则能提供部件级精确预测。

**提示交互场景**：在单点击（Figure 16）和边界框（Figure 17）提示下，SAM 2.1常产生不完整掩码或将暗色夹爪与背景混淆，RobotSeg则能生成完整且干净的跨帧分割结果。

**数据增强应用**：Figure 10展示了分割质量对下游任务的影响。RoboEngine和SAM 2.1的不精确掩码导致机器人合成图出现断裂或不真实伪影，而RobotSeg的精确掩码能实现结构准确的数据增强。

**已知局限**：在个别外观特殊的机器人类别上，RobotSeg并非所有指标均排第一，表明仍可结合更极致的形态相关建模。此外，相对于原始SAM 2.1的计算开销增加（约12%），在资源受限的嵌入式平台上仍有轻量化空间。这些发现需要在实际部署中手动验证具体类别的性能边界。

### 补充图表

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/022_Figure_13.jpg]]
*Figure 13: Qualitative comparison of whole-robot segmentation under the automatic setting. RoboEngine [69] exhibits clear inaccuracies and temporal inconsistencies, while our RobotSeg produces accurate and stable masks across frames*

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/023_Figure_14.jpg]]
*Figure 14: Qualitative comparison of robot arm segmentation under the automatic setting. EVF-SAM [74] struggles to localize the articulated arm and often confuses background objects, whereas our RobotSeg provides accurate, component-specific, and temporally consistent predictions*

![[assets/figures/papers/paper_list_l2101_https_arxiv_org_abs_2511_22950/figures/001_Figure_1.jpg]]
*Figure 1: Although existing state-of-the-art segmentation models (e.g., RoboEngine [69] and SAM 2.1 [44]) are highly capable, surprisingly they struggle to segment robots: they fail to cope with diverse embodiments (1-3 columns), often confuse robots with cluttered backgrounds (4th column), break down when facing complex structures (5th column), and fail to handle rapid shape changes (6th-7th columns). In contrast, our RobotSeg model (last row) achieves robust robot segmentation across diverse embodiments and scenes, and further supports user-provided prompts (e.g., clicks or bounding boxes) to refine the segmentation results (last column)*

## 方法谱系与知识库定位

### 1. 与基础模型的继承与改造

RobotSeg 并非从零构建，而是以 **SAM 2**（Ravi et al., ICLR 2024）为基础骨架进行领域适配与功能增强。SAM 2 作为通用视频分割基础模型，提供了图像编码器、记忆注意力机制和掩码解码器等核心组件，但其设计面向通用对象，未考虑机器人铰接结构的特殊性。RobotSeg 在三个关键维度上对 SAM 2 进行了系统性改造：

- **记忆关联器**：将 SAM 2 的标准记忆注意力替换为**结构增强记忆关联器（SEMA）**，通过 Canny 边缘图调制和多尺度结构感知分支注入机器人边界先验（见 Figure 5）。
- **提示生成**：将 SAM 2 依赖的人工点击/框输入替换为**机器人提示生成器（RPG）**，利用可学习类别令牌和历史聚类对象令牌实现自主分割（见 Figure 6）。
- **训练监督**：将 SAM 2 所需的逐帧掩码标注替换为**标注高效训练策略（LET）**，仅用首帧真值掩码配合循环一致性、语义一致性和块一致性损失进行视频级训练（见 Figure 7）。

这一改造路径体现了“通用基础模型 + 领域结构先验 + 标注高效适配”的范式，与同期工作如 **SAM-Adapter**（Chen et al., ICCV 2023）针对特定域适配 SAM 的思路一脉相承，但 RobotSeg 将适配从图像扩展到视频，并引入了结构感知和自动提示生成两个独特维度。

### 2. 与机器人分割方法的对比

在机器人分割这一细分领域，现有方法可分为三类，RobotSeg 在每一类中均展现出显著优势：

**图像级机器人分割方法**：**RoVi-Aug** 和 **RoboEngine** 是当前代表性的机器人图像分割模型。在 VRS 数据集全自动设置下，RobotSeg 的 J&F 达到 87.9，而 RoVi-Aug 仅为 38.9（+49.0），RoboEngine 的差距同样显著（见 Table 2）。更关键的是，这些方法仅处理单帧图像，缺乏时序一致性建模，导致视频场景中出现闪烁和不完整的掩码（见 Figure 13）。RobotSeg 通过 SEMA 的记忆机制天然保证了时序稳定性。

**语言条件分割方法**：**CLIPSeg**（Lüddecke & Ecker, CVPR 2022）、**LISA**（Lai et al., CVPR 2024）、**EVF-SAM**（Zhang et al., ECCV 2024）和 **VideoLISA** 通过文本描述引导分割，理论上可为机器人提供语义提示。然而，在机械臂分割任务中，EVF-SAM 的 mIoU 仅为 23.8，而 RobotSeg 达到 75.6（+51.8，见 Table 6）。语言提示的模糊性使其难以精确界定铰接结构的边界，尤其在机械臂与背景纹理相似时容易误分割（见 Figure 14）。

**开放词汇概念分割**：**SAM 3** 支持开放词汇概念分割，但其通用设计未针对机器人铰接结构进行优化，在复杂场景下同样面临边界模糊和时序不一致的问题。

### 3. 适用边界与局限

RobotSeg 的设计围绕 RGB 视频输入展开，其适用边界受以下因素制约：

- **模态依赖**：仅依赖 RGB 外观信息，当机器人颜色/纹理与背景高度相似、或光照条件极端时，结构感知分支可能无法可靠检测边界。融合深度、运动或触觉等额外模态是潜在的扩展方向，但当前版本不支持。
- **形态泛化**：尽管 VRS 数据集覆盖 10 类机器人形态，消融实验显示在个别外观特殊的类别上 RobotSeg 并非所有指标都排第一（见 Table 5-7），表明结构先验的建模仍有细化空间。
- **计算开销**：相对 SAM 2.1，RobotSeg 的 FLOPs 从 284.3G 增至 319.8G（+12.5%），参数量从 39.0M 升至 41.3M（见 Table 8）。在资源受限的嵌入式平台上，轻量化是必要的后续工作。

### 4. 开放问题与未来方向

基于当前工作的局限，以下方向值得进一步探索：

- **多模态融合**：如何有效融合深度、运动光流或触觉信号，以解决纯 RGB 难以处理的歧义情况（如黑色夹爪与暗背景的混淆）？
- **轻量化设计**：能否通过知识蒸馏或更轻量的结构感知模块设计，在保持鲁棒性的同时大幅降低计算成本，使其适配边缘设备？
- **闭环系统集成**：将 RobotSeg 集成到闭环机器人系统中，研究其对下游任务（3D 重建、策略学习、操作、导航）的实际影响。Figure 20 已初步展示了 RobotSeg 对 3D 重建的改善，但更广泛的下游任务验证仍有待开展。
- **更极致的形态建模**：针对个别外观特殊的机器人类别，探索更精细的形态相关建模策略，如基于部件图的显式铰接结构推理。

## 原文 PDF

![[paperPDFs/CVPR_2026/RobotSeg_A_Model_and_Dataset_for_Segmenting_Robots_in_Image_and_Video.pdf]]

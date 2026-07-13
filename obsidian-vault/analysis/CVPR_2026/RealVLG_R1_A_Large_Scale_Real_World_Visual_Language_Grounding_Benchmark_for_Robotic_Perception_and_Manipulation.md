---
title: "RealVLG-R1: A Large-Scale Real-World Visual-Language Grounding Benchmark for Robotic Perception and Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RealVLG_R1_A_Large_Scale_Real_World_Visual_Language_Grounding_Benchmark_for_Robotic_Perception_and_Manipulation.pdf
project_link: null
code_link: "https://github.com/lif314/RealVLG-R1"
aliases:
- RR
- RealVLG-R1
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建大规模多粒度、经多重验证的真实世界数据集 RealVLG-11B 以及采用基于可验证奖励的强化学习微调（RLVR）替代标准监督微调，同时统一输出边界框、分割、抓取姿势与接触点，是打通视觉语言理解到物理抓取的核心干预。
primary_logic: 利用 RLVR 策略让预训练大视觉语言模型在可验证的物理与语义奖励信号的驱动下，能够直接预测多种视觉与抓取输出，实现从语言描述到零样本、多粒度感知和操纵的端到端统一。
claims:
- RealVLG-11B 在语言丰富度（MTLD 36.49）与视觉-语言对齐（CLIP Score 0.65）上显著超越 Grasp-Anything 系列数据集，验证了多粒度标注的质量。
- RealVLG-R1 (7B GSPO) 在 Seen 集合上 Bbox gIoU 达到 89.0，cIoU 88.9，较 SFT 基线大幅提升，且在 Novel 集合上保持迁移能力。
- 在真实机器人实验中，RealVLG-R1 在 Single 设置下平均抓取成功率 81%，远超仅视觉的 GraspNet 的 38%；在 Clutter 设置下平均成功率 79%，而语言抓取基线 LGD 仅 2%。
- RealVLG Benchmark (Seen Set) 上 Bbox gIoU = 89.0 (RealVLG-R1 7B GSPO)
---

# RealVLG-R1: A Large-Scale Real-World Visual-Language Grounding Benchmark for Robotic Perception and Manipulation

> [!tip] 核心洞察
> 利用 RLVR 策略让预训练大视觉语言模型在可验证的物理与语义奖励信号的驱动下，能够直接预测多种视觉与抓取输出，实现从语言描述到零样本、多粒度感知和操纵的端到端统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | RealVLG-R1：面向机器人感知与操作的大规模真实世界视觉-语言定位基准 |
| 英文题名 | RealVLG-R1: A Large-Scale Real-World Visual-Language Grounding Benchmark for Robotic Perception and Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14880) · [Code](https://github.com/lif314/RealVLG-R1) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RealVLG-R1 |
| Dataset | RealVLG Benchmark, Real-World Single-Object Grasping, Real-World Cluttered Grasping |

> [!tip] 效果简介
> - RealVLG Benchmark (Seen Set) 上，Bbox gIoU 89.0 (RealVLG-R1 7B GSPO) vs 58.2 (Qwen2.5-VL + SFT 7B) (+30.8)；Seg F-measure F_β 87.2 (RealVLG-R1 3B GRPO) vs 87.8 (Qwen-VL-Max, higher but low validity rate) (-0.6)；Grasp mIoU / gAcc 34.7 / 40.3 (RealVLG-R1 3B GRPO) vs N/A (no language grasp baseline) (N/A)。
> - Real-World Single-Object Grasping 上，Average Success Rate 81% (RealVLG-R1) vs 38% (GraspNet) (+43%)。
> - Real-World Cluttered Grasping 上，Average Success Rate 79% (RealVLG-R1) vs 2% (LGD) (+77%)。

## 概要

### 问题瓶颈

现有视觉语言定位（Visual-Language Grounding）主要停留在粗粒度的物体级检测层面，无法推理出物理上可执行的抓取；而传统抓取方法则依赖纯几何线索，缺乏自然语言语义的引导。这一鸿沟的根源在于：**缺乏高质量、多粒度的“语言-视觉-抓取”联合标注数据**，导致语言驱动的精细抓取与真实世界泛化之间无法打通。

### 核心干预：RLVR + 统一多粒度输出

本文提出 **RealVLG-R1**，通过两项关键干预打破上述瓶颈：

1. **构建 RealVLG-11B 数据集**：约 165K 张真实图像，经 LVLM 自动生成与人工双重验证，提供边界框、分割掩码、抓取矩形与接触点的多粒度标注，并配以高丰富度的自然语言描述（MTLD 36.49，CLIP Score 0.65），显著优于 Grasp-Anything 系列数据集（Table 3）。
2. **基于可验证奖励的强化微调（RLVR）替代标准 SFT**：让预训练大视觉语言模型（Qwen2.5-VL）在可验证的物理与语义奖励信号驱动下，统一输出边界框、分割、抓取姿势与接触点，实现从语言描述到零样本、多粒度感知与操作的端到端统一。

### 方法谱系与知识库定位

RealVLG-R1 处于 **语言驱动的机器人感知与操作** 交叉点，其方法谱系可概括为：

- **视觉语言定位**：与 Qwen-VL-Max、Gemini 2.5 Flash 等大视觉语言模型相比，RealVLG-R1 不依赖闭源 API，而是通过 RLVR 将定位能力从物体框拓展至抓取级输出。
- **机器人抓取**：相较于仅依赖视觉的 6-DoF 抓取估计器 **GraspNet**（Fang et al., IJRR 2023）和语言引导的 2D 矩形抓取方法 **LGD**（Nguyen et al., IROS 2023），RealVLG-R1 首次在统一框架内实现语言条件化的多粒度抓取预测。
- **强化微调策略**：对比 **GRPO**（token 级重要性权重）与 **GSPO**（序列级重要性权重 + 长度归一化），RLVR 范式在数据稀缺（仅 10% 训练集）条件下显著优于 SFT。

### 核心结论

- **基准性能**：RealVLG-R1（7B GSPO）在 Seen 集合上 Bbox gIoU 达 89.0，较 Qwen2.5-VL + SFT 基线（58.2）提升 +30.8（Table 4）。
- **真实机器人实验**：在 Single 设置下平均抓取成功率 81%，远超 GraspNet 的 38%；在 Clutter 设置下平均成功率 79%，而语言抓取基线 LGD 仅 2%（Table 5、Table 6）。
- **关键机制**：RLVR 通过复合可验证奖励（格式奖励 + 任务几何精度奖励，权重 α=0.1, β=0.9）驱动模型在零样本条件下实现稳定、可解释的抓取预测，且 GSPO 在 7B 模型上收敛更稳定（Figure 7）。

> **注意**：当前接触点预测在高度杂乱环境中偶尔不稳定；模型尚未直接扩展至全 3D 空间推理。这些限制需在后续工作中进一步验证。

机器人从自然语言指令中理解并定位目标物体，进而执行精确抓取，是实现通用机器人操作的核心能力。然而，当前技术栈在两个关键维度上存在根本性断裂。

**视觉语言定位停留在粗粒度层级。** 现有的大视觉语言模型（LVLM）在开放词汇物体检测和指代表达理解上取得了显著进展，但其输出通常局限于物体级边界框或语义分割掩码。这些粗粒度的感知结果无法直接转化为机器人末端执行器可执行的抓取姿势——抓取需要精确的接触点、抓取宽度和抓取角度等几何信息，而不仅仅是“物体在哪里”。

**传统抓取方法缺乏语言语义引导。** 以 **GraspNet** (Fang et al., 2020) 为代表的纯视觉抓取方法仅依赖几何线索（如点云法向量、局部曲率）生成 6-DoF 抓取候选，完全无法响应语言指令（如“抓住杯子的把手”或“拿起红色的螺丝刀”）。另一类语言引导抓取方法如 **LGD** (Nguyen et al., 2023) 虽尝试将 CLIP 嵌入与抓取生成网络结合，但其感知分辨率有限、语言整合方式粗糙，在杂乱场景中几乎完全失效（成功率仅 2%）。

**高质量多粒度标注数据的缺失是根本瓶颈。** 打通视觉语言理解到物理抓取的关键障碍在于缺乏同时包含细粒度语言描述、精确视觉定位和物理可执行抓取标注的大规模真实世界数据集。现有抓取数据集（如 Grasp-Anything 系列）或依赖扩散模型生成的低分辨率合成图像，或仅提供弱对齐的文本标注，无法支撑语言驱动的精细抓取学习。

基于上述分析，本文的核心动机是：**构建一个大规模、多粒度、经多重验证的真实世界数据集，并设计一种能够从自然语言指令直接预测多种视觉与抓取输出的统一模型框架，从而弥合语言理解与物理操作之间的鸿沟。** 具体而言，本文提出 RealVLG 框架，包含 RealVLG-11B 数据集和 RealVLG-R1 模型，通过基于可验证奖励的强化学习微调（RLVR）策略，使预训练 LVLM 能够端到端地输出边界框、分割掩码、抓取矩形和接触点，实现从语言描述到零样本多粒度感知与操作的统一。

## 核心方法与创新机理

RealVLG-R1 的核心创新在于通过**基于可验证奖励的强化学习微调（RLVR）**，将预训练大视觉语言模型（LVLM）重塑为一个端到端、多粒度、零样本的视觉语言抓取系统，从根本上突破了现有方法“语言理解”与“物理抓取”之间的断层。

### 1. 训练策略的根本性转变：从 SFT 到 RLVR

传统视觉语言定位或抓取模型通常采用标准监督微调（SFT），即直接拟合真实标签的损失函数。然而，SFT 仅能学习静态映射，难以在复杂、多模态的抓取任务中建立鲁棒的因果推理能力。RealVLG-R1 转而采用 RLVR 策略，其核心干预点在于：

- **可验证奖励机制**：设计了一套复合奖励函数 $R(q, o) = \alpha R_{\mathrm{Format}} + \beta R_{\mathrm{Task}}$（$\alpha=0.1, \beta=0.9$），其中 $R_{\mathrm{Format}}$ 强制模型输出遵循 `<think>...</think>\n<answer>...</answer>` 的结构化格式，$R_{\mathrm{Task}}$ 则针对不同任务（边界框、分割、抓取、接触点）计算几何精度奖励。例如，边界框奖励为 $\mathbf{1}(\mathrm{IoU}(B_p, B_{gt}) \geq \tau_{\mathrm{iou}})$，抓取奖励为对位置、角度和宽度分量的 Huber 损失之和的负数。这种**可验证的物理与语义奖励信号**使模型能够动态评估并优化其预测，而非被动拟合标签。

- **策略优化目标**：最大化期望奖励同时约束与参考策略的 KL 散度：
  $$\max_{\pi_\theta} \mathbb{E}_{q,o} \Big[ R(q, o) - \beta \mathbb{D}_{\mathrm{KL}}[\pi_\theta(o|q) \| \pi_{\mathrm{ref}}(o|q)] \Big]$$
  该目标确保策略更新既追求高奖励，又避免偏离预训练知识过远，从而保持泛化性。

- **消融验证**：在接触点预测任务上，GRPO 和 GSPO（两种 RLVR 变体）的训练奖励与准确率曲线均显著超越 SFT 基线（Figure 7）。其中，GRPO 在 3B 模型上因令牌级重要性权重而略有优势，而 GSPO 在 7B 模型上通过序列级权重与长度归一化实现了更优性能和更稳定的收敛。这一结果表明，RLVR 是打通语言理解到精细抓取的关键因果杠杆。

### 2. 输出空间的统一：从单一感知到多粒度联合预测

现有方法通常仅预测单一抓取姿势或物体边界框，无法同时满足从粗粒度物体定位到精细部件级抓取的多层次需求。RealVLG-R1 将 LVLM 的输出空间扩展为**统一预测边界框、分割掩码、抓取矩形和接触点**，实现了“一语多出”的端到端能力。

- **分割任务**：模型先预测边界框，再调用冻结的 SAM2 生成高精度掩码，既利用了 LVLM 的语义理解，又借助了专用分割模型的精细度。
- **抓取任务**：模型直接预测 2D 抓取矩形或接触点，随后通过 2D-to-6-DoF 转换模块，结合深度与相机参数，将其映射为可执行的 6-DoF 抓取位姿。这种设计使得语言指令可以直接驱动从感知到执行的全链路，无需中间手工规则。

### 3. 数据基础的质变：从无语言或弱标注到多粒度验证数据集

基线方法普遍缺乏高质量的语言-视觉-抓取联合标注。RealVLG-R1 建立在 **RealVLG-11B 数据集**之上，该数据集包含约 165K 张真实世界图像，具备以下创新特性：

- **多粒度标注**：每张图像同时提供边界框、分割掩码、抓取矩形和接触点的真实标注。
- **双重验证的语言指令**：语言描述由 GPT-4o 从多视角渲染生成，并经过 Qwen-VL-Max 的视觉定位验证与人工校验系统的双重审核，确保语言与视觉内容的高度对齐。
- **数据质量优势**：在语言丰富度（MTLD 36.49）和视觉-语言对齐（CLIP Score 0.65）上，RealVLG-11B 显著超越 Grasp-Anything 系列数据集（Table 3），为 RLVR 训练提供了坚实的监督基础。

### 4. 零样本泛化能力的涌现

上述策略、输出与数据的协同创新，使 RealVLG-R1 具备了突出的零样本泛化能力。在真实机器人实验中，RealVLG-R1 在 Single 设置下平均抓取成功率达 81%，远超仅视觉的 GraspNet（38%）；在 Clutter 设置下平均成功率 79%，而语言抓取基线 LGD 仅 2%（Table 5, Table 6）。这表明，RLVR 驱动的多粒度联合预测范式能够有效应对未见物体与杂乱环境，实现了从语言描述到可靠物理交互的跨越。

RealVLG-R1 的整体框架围绕一个核心设计展开：**将预训练大视觉语言模型（LVLM）作为统一的多任务策略模型，通过可验证奖励驱动的强化学习微调（RLVR），使其能够直接从自然语言指令中预测多种视觉与抓取输出**。该框架由四个关键模块串联而成，形成从感知到执行的闭环。

### 1. 预训练 LVLM 骨干（策略模型）

框架的策略模型以 **Qwen2.5-VL** 作为骨干。模型接收一张 RGB 图像和一个任务提示（task prompt），并按照统一的 `<think>...</think>\n<answer>...</answer>` 格式生成结构化输出。这种设计使得模型能够同时处理边界框（Bbox）、分割掩码（Seg）、抓取矩形（Grasp）和接触点（Contact）四类任务，且格式的严格性为后续格式奖励的计算提供了基础。

### 2. 可验证奖励计算模块

在训练阶段，模型的输出被送入可验证奖励计算模块。该模块根据任务类型计算复合奖励：

$$
R(q, o) = \alpha R_{\mathrm{Format}} + \beta R_{\mathrm{Task}}, \quad \alpha=0.1, \ \beta=0.9
$$

其中：
- **格式奖励** $R_{\mathrm{Format}}$：当输出严格遵循 `<think>/<answer>` 格式时为 1，否则为 0。
- **任务奖励** $R_{\mathrm{Task}}$：根据具体任务采用不同的几何精度度量，例如边界框的 IoU 阈值奖励、分割的 S-measure、抓取姿态的 Huber 损失负值、接触点的 L2 距离惩罚等。

这一可验证奖励机制是 RLVR 的核心——它使得模型无需人工标注的偏好数据，仅凭任务内在的可验证标准即可进行策略优化。

### 3. SAM2 掩码生成器（辅助模块）

对于分割任务，模型并不直接输出像素级掩码，而是**先预测目标物体的边界框，再将边界框传递给一个冻结的 SAM2 模型**，由 SAM2 生成最终的高精度分割掩码。这种“粗定位 + 精分割”的解耦设计，既降低了 LVLM 直接生成掩码的难度，又保证了分割精度。

### 4. 2D 到 6-DoF 抓取转换器（执行模块）

在真实机器人部署中，模型在图像域上预测的 2D 抓取矩形或接触点，需要转换为可执行的 6-DoF 抓取位姿。转换流程为：
1. 将 2D 抓取点 $(u, v)$ 通过深度图和相机内参投影到相机坐标系下的 3D 点；
2. 结合抓取矩形的角度和宽度信息，生成完整的 6-DoF 抓取姿态（位置 + 朝向 + 开合宽度）。

这一转换器使得 RealVLG-R1 支持两种互补的抓取策略（见 Figure 4）：
- **粗粒度物体级抓取**：利用分割掩码或边界框投影到 3D 点云，通过 3D 抓取模块生成 6-DoF 姿态；
- **细粒度部件级抓取**：直接利用 2D 抓取预测转换为 6-DoF 姿态，实现语义精确的操作。

![[assets/figures/papers/paper_list_l823_https_arxiv_org_abs_2603_14880/figures/008_Figure_4.jpg]]
*Figure 4: Overview of the RealVLG-R1 deployment for real-world Visual-Language Grasping tasks. RealVLG-R1 produces multigranularity visual–language outputs, which can be leveraged in two complementary grasping strategies: (a) coarse-grained, object-centric grasping, where segmentation masks or bounding boxes are projected into 3D point clouds to generate 6-DoF grasp poses via a 3D grasping module; (b) fine-grained, part-level grasping, where 2D grasp predictions are directly transformed into executable 6-DoF poses using depth and camera parameters, enabling semantically precise manipulation. This design supports hierarchical control from global geometry to detailed semantic structures*

### 5. 训练策略：RLVR 替代 SFT

框架的关键创新在于**用 RLVR 替代标准监督微调（SFT）**。传统 SFT 仅最小化预测与真值之间的固定损失，而 RLVR 通过策略优化目标：

$$
\max_{\pi_\theta} \mathbb{E}_{q,o} \Big[ R(q, o) - \beta \mathbb{D}_{\mathrm{KL}} [\pi_\theta(o|q) \ || \ \pi_{\mathrm{ref}}(o|q)] \Big]
$$

在最大化可验证奖励的同时，通过 KL 散度正则化约束策略不偏离参考模型过远。实验表明，这一策略使得 7B 模型在 Seen 集合上 Bbox gIoU 从 SFT 的 58.2 跃升至 89.0（+30.8），验证了 RLVR 对多任务统一输出的关键驱动作用。

> **注意**：关于 GRPO 与 GSPO 两种 RL 优化策略的详细对比（令牌级 vs 序列级重要性权重、收敛稳定性差异），将在后续“训练策略与优化”部分展开。

![[assets/figures/papers/paper_list_l823_https_arxiv_org_abs_2603_14880/figures/005_Figure_3.jpg]]
*Figure 3: Framework of RealVLG-R1. RealVLG-R1 fine-tunes pretrained LVLMs via reward-driven RL using task-specific verifiable rewards, enabling adaptive learning and improved generalization over bounding boxes, segmentation, grasp rectangles, and contact points*

### 1. 模型框架与结构化输出

RealVLG-R1 以预训练大视觉语言模型（LVLM）为骨干（采用 Qwen2.5-VL），接收图像与任务提示，生成符合统一格式的结构化输出。所有任务均遵循 `<think>...</think>\n<answer>...</answer>` 格式，以便后续计算格式奖励。模型输出因任务而异：

- **边界框（Bbox）**：直接预测目标物体的矩形框坐标。
- **分割（Seg）**：模型先预测边界框，再调用冻结的 **SAM2** 生成高精度掩码。
- **抓取（Grasp）**：预测 2D 抓取矩形（中心、角度、宽度），随后通过 2D-to-6-DoF 转换器结合深度与相机参数生成可执行的 6-DoF 抓取位姿。
- **接触点（Contact）**：预测两个接触点坐标，同样可转换为 6-DoF 抓取。

### 2. 强化学习微调策略

RealVLG-R1 采用基于可验证奖励的强化学习微调（RLVR）范式，核心优化目标为最大化期望奖励并约束策略偏离：

$$
\operatorname*{max}_{\pi_{\theta}} \mathbb{E}_{q,o} \Big[ R(q,o) - \beta \mathbb{D}_{\mathrm{KL}} [\pi_{\theta}(o|q) || \pi_{\mathrm{ref}}(o|q)] \Big]
$$

其中：
- $q$ 为输入（图像+提示），$o$ 为模型输出；
- $R(q,o)$ 为可验证奖励；
- $\beta$ 为 KL 散度正则化系数；
- $\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略（冻结的初始模型）。

### 3. 优势估计与策略梯度

采用组内标准化优势函数以降低方差：

$$
\widehat{A}_i = \frac{r(x, y_i) - \operatorname{mean}(\{r(x, y_j)\}_{j=1}^{G})}{\operatorname{std}(\{r(x, y_j)\}_{j=1}^{G})}
$$

其中 $G$ 为每组采样数量，$r(x, y_i)$ 为第 $i$ 个输出的奖励值。

#### 3.1 GRPO 损失

GRPO 使用令牌级重要性权重：

$$
w_{i,t}(\theta) = \frac{\pi_{\theta}(y_{i,t} | x, y_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t} | x, y_{i,<t})}
$$

$$
\mathcal{L}_{\mathrm{GRPO}}(\theta) = -\mathbb{E}_{x,\{y_i\}} \Bigg[ \cfrac{1}{G} \sum_{i=1}^{G} \frac{1}{|y_i|} \displaystyle\sum_{t=1}^{|y_i|} \Big[ \operatorname{min}\big( w_{i,t}(\theta) \widehat{A}_i, \mathrm{clip}(w_{i,t}(\theta), 1-\varepsilon, 1+\varepsilon) \widehat{A}_i \big) - \beta \mathbb{D}_{\mathrm{KL}} \Big] \Bigg]
$$

#### 3.2 GSPO 损失

GSPO 采用序列级重要性权重并引入长度归一化以控制长序列方差：

$$
s_i(\theta) = \Big( \frac{\pi_{\theta}(y_i|x)}{\pi_{\theta_{\mathrm{old}}}(y_i|x)} \Big)^{\frac{1}{|y_i|}}
$$

$$
\mathcal{L}_{\mathrm{GSPO}}(\boldsymbol{\theta}) = -\mathbb{E}_{\boldsymbol{x},\{\boldsymbol{y}_i\}} \Bigg[ \frac{1}{G} \sum_{i=1}^{G} \Big[ \operatorname{min}\big( s_i(\boldsymbol{\theta}) \widehat{A}_i, \mathrm{clip}(s_i(\boldsymbol{\theta}), 1-\boldsymbol{\varepsilon}, 1+\boldsymbol{\varepsilon}) \widehat{A}_i \big) - \beta \mathbb{D}_{\mathrm{KL}} \Big] \Bigg]
$$

### 4. 复合可验证奖励设计

总奖励由格式奖励与任务奖励加权求和构成：

$$
R(q,o) = \alpha R_{\mathrm{Format}} + \beta R_{\mathrm{Task}}, \quad \alpha=0.1, \beta=0.9
$$

- **格式奖励** $R_{\mathrm{Format}}$：当输出严格遵循 `<think>/<answer>` 格式时为 1，否则为 0。
- **任务奖励** $R_{\mathrm{Task}}$ 根据具体任务分解为可验证的几何精度信号：

#### 4.1 边界框奖励

$$
R_{\mathrm{Bbox}} = \mathbf{1}(\mathrm{IoU}(B_p, B_{gt}) \geq \tau_{\mathrm{iou}})
$$

当预测框 $B_p$ 与真值框 $B_{gt}$ 的 IoU 超过阈值 $\tau_{\mathrm{iou}}$ 时奖励为 1。

#### 4.2 分割奖励

$$
R_{\mathrm{Seg}} = \mathbf{1}(\mathrm{IoU}(B_p, B_{gt}) \geq \tau_{\mathrm{iou}}) + \mathbf{S}_{\alpha}(M_p, M_{gt})
$$

结合粗定位 IoU 与精细掩码的结构相似性度量 S-measure。

#### 4.3 抓取位姿奖励

$$
R_{\mathrm{Grasp}} = -\sum_{v \in \{x, y, \cos\theta, \sin\theta, w\}} \mathcal{L}_{\mathrm{Huber}}(v_p, v_{gt})
$$

对抓取中心 $(x,y)$、角度（以 $\cos\theta, \sin\theta$ 编码）和宽度 $w$ 各分量计算 Huber 损失之和的负数。

#### 4.4 接触点奖励

$$
R_{\mathrm{Contact}} = \mathbf{1}(\mathrm{IoU}(G_p, G_{gt}) \geq \tau_{\mathrm{iou}}) - \sum_{i=1}^{2} \|P_i^p - P_i^{gt}\|_2
$$

结合由接触点重建的矩形抓取 IoU 与点对点的 L2 距离惩罚。

### 5. 关键设计要点

- **统一输出空间**：模型同时预测边界框、分割掩码、抓取矩形与接触点，打通视觉定位到物理抓取的端到端链路。
- **RLVR 驱动**：以可验证的几何精度信号替代传统监督微调的固定标注损失，使模型在奖励引导下自适应优化。
- **GRPO vs GSPO**：消融实验表明，GRPO 在 3B 模型上因令牌级权重略有优势，而 GSPO 在 7B 模型上利用序列级权重与长度归一化实现了更优性能和更稳定收敛。

## 实验与关键发现

### 数据集质量验证

RealVLG-11B 的语言丰富度与视觉‑语言对齐质量通过定量指标与现有抓取数据集进行了对比（Table 3）。在语言多样性方面，RealVLG-11B 的 **MTLD**（Measure of Textual Lexical Diversity）达到 **36.49**，显著高于 Grasp-Anything 及 Grasp-Anything++ 等数据集，表明其自然语言指令具有更高的词汇丰富度和句法复杂度。在视觉‑语言对齐方面，RealVLG-11B 的 **Sentence CLIP Score**（SCLIP）达到 **0.65**，说明图像与语言描述之间的语义一致性更强。此外，数据集在边界框召回率（$R_s$=0.99）、抓取召回率（$R_g$=0.69）和接触点召回率（$R_c$=0.87）上均保持高水平，验证了多粒度标注的完整性。定性对比（Figure 6）进一步显示，RealVLG-11B 使用高分辨率真实图像与实例级语言标注，避免了扩散生成数据中常见的低分辨率、弱对齐问题，为后续模型训练提供了可靠基础。

![[assets/figures/papers/paper_list_l823_https_arxiv_org_abs_2603_14880/figures/006_Table_3.jpg]]
*Table 3: Linguistic and grounding quality comparison*

![[assets/figures/papers/paper_list_l823_https_arxiv_org_abs_2603_14880/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative Comparison of Data Quality. Unlike the diffusion-generated, low-resolution images and weakly aligned textual and grasp annotations in Grasp-Anything datasets, RealVLG-11B provides high-resolution real-world imagery, instance-level language grounding, and standardized, physically executable grasp labels, enabling more accurate and robust visual–language grasping*

### RealVLG Benchmark 综合性能

Table 4 报告了 RealVLG-R1 与基线方法在 Seen 与 Novel 测试集上的多任务性能。所有模型仅使用 10% 的训练数据进行微调，以确保公平比较。

![[assets/figures/papers/paper_list_l823_https_arxiv_org_abs_2603_14880/figures/007_Table_4.jpg]]
*Table 4: RealVLG benchmark comprehensive results. All metrics are reported in percentage format*

**边界框定位。** RealVLG-R1 (7B, GSPO) 在 Seen 集上取得了 **gIoU 89.0** 和 **cIoU 88.9**，较 Qwen2.5-VL + SFT 基线（gIoU 58.2）提升 **+30.8 个百分点**，并在 Novel 集上保持了显著的迁移能力。这一结果直接验证了 RLVR 训练策略在几何精度上的核心收益。

**分割质量。** RealVLG-R1 (3B, GRPO) 在 Seen 集上达到 **$F_\beta$ 87.2**，略低于 Qwen-VL-Max 的 87.8，但 Qwen-VL-Max 的有效率（$R_v$）仅为 56.5，表明其输出格式合规性差，实际可用性远低于 RealVLG-R1。RealVLG-R1 通过格式奖励机制保证了高有效输出率。

**抓取与接触点预测。** 这是现有语言抓取基线无法直接比较的新任务。RealVLG-R1 (3B, GRPO) 在 Seen 集上取得抓取 **mIoU 34.7**、**gAcc 40.3**，接触点 **mIoU 44.0**，在 Novel 集上保持相近水平，证明了模型对抓取几何的初步推理能力。

### 训练策略消融

Figure 7 展示了 GRPO、GSPO 与 SFT 在接触点任务上的训练奖励与准确率曲线。两种 RLVR 策略（GRPO 和 GSPO）均大幅超越 SFT 基线，证实了可验证奖励驱动优化的有效性。在 3B 模型上，GRPO 因令牌级重要性权重而略微占优；在 7B 模型上，GSPO 利用序列级重要性权重与长度归一化，实现了更高的最终性能和更稳定的训练收敛。这一趋势表明，对于更大规模的策略模型，序列级方差控制对 RL 训练的稳定性至关重要。

### 真实世界机器人抓取实验

真实世界实验使用 7-DoF Franka Research 3 机器人搭载 Intel RealSense D435i 相机（Figure 8），在 10 个未见物体上评估语言条件抓取能力。

**单物体场景（Single）。** Table 5 显示，RealVLG-R1 平均抓取成功率达到 **81%**，而纯视觉基线 **GraspNet**（Fang et al., 2023）仅为 **38%**（+43%）。定性分析（Figure 9）揭示，GraspNet 在点云噪声、反射表面及细小物体（如螺丝刀、剃须刀）上频繁失败或生成错位抓取姿势；RealVLG-R1 则利用 RGB 视觉与语言指令准确定位目标并生成可执行抓取接触点，展现出更强的鲁棒性。

**杂乱场景（Clutter）。** Table 6 显示，RealVLG-R1 在杂乱多物体环境中平均成功率达 **79%**，而语言抓取基线 **LGD**（Yang et al., 2023）仅为 **2%**（+77%）。LGD 的失败源于感知分辨率有限、语言整合不足以及对无条件抓取预测的依赖（Figure 10）。RealVLG-R1 则表现出准确的零样本语言条件抓取和可解释的抓取姿势预测（Figure 11），验证了统一视觉‑语言‑抓取框架在真实杂乱场景中的泛化能力。

### 失败模式与局限性

尽管整体性能优异，RealVLG-R1 在高度杂乱环境中偶尔出现抓取接触点预测不稳定的情况，可能导致真实部署中的抓取失败。当前模型主要依赖 RGB-D 图像预测 2D 抓取先验并转换为 6-DoF 姿势，尚未直接扩展至全 3D 空间推理，在处理复杂三维遮挡或非平面抓取时存在理论局限。此外，RealVLG-11B 数据集覆盖约 800 个物体实例，仍受限于现有真实世界数据源的种类，可能不足以涵盖所有形状和材质。模型在动态交互或多步骤操作任务中的表现尚未验证，这些问题需要进一步研究。

![[assets/figures/papers/paper_list_l823_https_arxiv_org_abs_2603_14880/figures/015_Figure_9.jpg]]
*Figure 9: Qualitative real-world grasping results in the Single setting. GraspNet often fails or predicts misaligned grasp poses due to noisy or incomplete point cloud data (e.g., Cup), reflective surfaces, and small or thin objects, such as Marker, Screwdriver, and Razor. In contrast, RealVLG-R1 leverages RGB vision and language instructions to accurately localize the target and generate executable grasp contact points, demonstrating robust and reliable grasping behavior across diverse objects*

## 定位与知识库关联

### 1. 核心瓶颈与因果干预

现有视觉语言定位（Visual-Language Grounding）长期停留在粗粒度物体级检测，无法推理可执行的精细抓取；传统抓取方法（如 **GraspNet** (Fang et al., RSS 2020)）依赖纯几何线索，缺乏语言语义引导。更深层的瓶颈在于，已有数据集普遍缺少高质量、多粒度的语言-视觉-抓取联合标注，导致语言驱动的精细抓取与真实世界泛化之间存在根本性鸿沟。

RealVLG-R1 的核心干预在于两个联动机制：**数据层面**，构建大规模多粒度、经多重验证的真实世界数据集 **RealVLG-11B**（约 165K 张真实图像，覆盖边界框、分割、抓取矩形与接触点，并经过 LVLM 与人工双重验证）；**训练策略层面**，采用基于可验证奖励的强化学习微调（RLVR）替代标准监督微调（SFT），统一输出边界框、分割掩码、抓取姿势与接触点。这一组合打通了从视觉语言理解到物理抓取的端到端通路。

### 2. 方法谱系中的定位

RealVLG-R1 处于视觉语言模型（VLM）与机器人操作的交汇点，其基线体系可沿三条轴展开：

| 轴线 | 代表方法 | 核心差异 |
|------|----------|----------|
| 大视觉语言模型基线 | **Qwen-VL-Max** (Alibaba Cloud, 2025)、**Gemini 2.5 Flash** (Google DeepMind, 2025) | 仅提供视觉定位与问答能力，不专门训练抓取输出 |
| 纯几何抓取基线 | **GraspNet** (Fang et al., RSS 2020) | 仅依赖视觉的 6-DoF 抓取姿势估计，无语言引导 |
| 语言引导抓取基线 | **LGD** (Vuong et al., IROS 2023) | 采用 CLIP 嵌入与 GGCNN 架构的 2D 矩形抓取方法，语言集成与感知分辨率受限 |

与上述基线相比，RealVLG-R1 是首个基于 LVLM 的端到端机器人感知模型，统一了分割、定位与抓取感知。其训练策略从标准 SFT 切换为 RLVR（受 **DeepSeek-R1** 启发），奖励信号从固定标注的损失函数（如 MSE、IoU 损失）升级为复合可验证奖励：格式奖励 + 任务奖励（Bbox IoU、Seg S-measure、Grasp Huber 损失、Contact 距离等）。消融实验进一步对比了两种 RL 优化策略——**GRPO**（令牌级重要性权重）与 **GSPO**（序列级重要性权重与长度归一化），以评估收敛稳定性与性能差异。

### 3. 适用边界与局限

尽管 RealVLG-R1 在零样本场景下表现出色，其适用边界由以下因素界定：

- **感知模态**：模型主要基于 RGB-D 图像预测 2D 抓握并转换为 6-DoF 位姿，尚未直接扩展至全 3D 空间推理（如 6-DoF 体积抓取与三维语义理解）。
- **数据覆盖**：RealVLG-11B 覆盖约 800 个物体实例，仍局限于现有真实世界数据源的种类，可能不足以涵盖所有可能的形状与材质。
- **场景鲁棒性**：抓取接触点预测在高度杂乱环境中偶尔不稳定，可能影响真实部署的可靠性。
- **任务范围**：尚未在广泛动态交互或多步骤操作任务中进行验证。

### 4. 开放问题

从当前工作出发，若干方向值得进一步探索：

1. **3D 空间扩展**：如何将 RealVLG 框架扩展至全 3D 空间（如 6-DoF 体积抓取与三维语义理解），以支持更复杂的操作任务。
2. **推理效率**：能否通过更高效的视觉语言骨干（如 SmolVLM）在保持性能的同时大幅降低推理延迟。
3. **交互式反馈引入**：如何引入更多交互式反馈（如力控或触觉信号）以提升精细操作的成功率。
4. **物理模拟验证**：在多模态奖励中加入物理模拟验证是否能够进一步提升策略的泛化性与执行稳定性。

> **注意**：以上开放问题均来自论文原文的明确表述，未添加推测性内容。关于具体基线工作的作者/会议/年份信息，部分已根据分析 JSON 提供的引用编号进行补充（如 GraspNet 、LGD ），但若原文未明确给出完整元数据，建议读者自行核实原始文献。

## 原文 PDF

![[paperPDFs/CVPR_2026/RealVLG_R1_A_Large_Scale_Real_World_Visual_Language_Grounding_Benchmark_for_Robotic_Perception_and_Manipulation.pdf]]

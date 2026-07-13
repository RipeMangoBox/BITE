---
title: "AutoFly: Vision-Language-Action Model for UAV Autonomous Navigation in the Wild"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AutoFly_Vision_Language_Action_Model_for_UAV_Autonomous_Navigation_in_the_Wild.pdf
project_link: https://xiaolousun.github.io/AutoFly
code_link: null
openreview_forum_id: 88RKxlFUNY
aliases:
- AutoFly
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过伪深度编码器从单目RGB中恢复深度信息，增强三维空间几何理解，并利用Siamese投影实现深度特征与视觉-语言特征的对齐。"
primary_logic: "伪深度编码器赋予VLA模型三维空间推理能力，使其能够基于简短的粗略指令端到端地执行障碍物避免、目标识别和路径规划，摆脱对精确逐步指令的依赖，在未知环境下实现鲁棒自主飞行。"
claims:
- "AutoFly整体成功率47.9%，显著超越OpenVLA（44.0%）和RT-2（41.9%）。"
- "移除伪深度编码器后成功率立即下降3.9%，碰撞率上升2.6%。"
- "在动态障碍物场景下，伪深度编码器将成功率提升9.9%，碰撞率降低9.5%，效果最为显著。"
- "简单的数据扩充、更强的RGB编码器或增加训练数据均无法替代伪深度编码器的增益（+3.9% vs +1.2% max）。"
---

# AutoFly: Vision-Language-Action Model for UAV Autonomous Navigation in the Wild

> [!tip] 核心洞察
> 伪深度编码器赋予VLA模型三维空间推理能力，使其能够基于简短的粗略指令端到端地执行障碍物避免、目标识别和路径规划，摆脱对精确逐步指令的依赖，在未知环境下实现鲁棒自主飞行。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoFly：面向野外无人机自主导航的视觉-语言-动作模型 |
| 英文题名 | AutoFly: Vision-Language-Action Model for UAV Autonomous Navigation in the Wild |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=88RKxlFUNY) · [Project](https://xiaolousun.github.io/AutoFly) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AutoFly |
| Dataset | Our Dataset (Overall), Sim-to-Real (Indoor) |

> [!tip] 效果简介
> - Our Dataset (Overall) 上，SR 为 47.9，对比 OpenVLA 44.0，变化 +3.9。
> - Our Dataset (Overall) 上，CR 为 21.9，对比 OpenVLA 24.5，变化 -2.6。
> - Our Dataset (Overall) 上，PER 为 77.3，对比 OpenVLA 75.1，变化 +2.2。

## 概要

无人机自主导航的核心挑战在于：**现有视觉-语言导航（VLN）系统依赖逐步式的精确航点指令，无法在仅有粗略方向引导和未知动态环境中进行自主决策、三维避障与空间推理**。这一瓶颈限制了无人机在野外、森林等非结构化场景中的实际部署能力。

针对上述问题，本文提出 **AutoFly**，一个端到端的视觉-语言-动作（VLA）模型。其核心调控机制是引入**伪深度编码器**：利用 Depth Anything V2 从单目 RGB 中恢复深度信息，并通过 Siamese MLP 投影器将深度特征与视觉-语言特征对齐，从而赋予 VLA 模型三维空间几何理解能力。这一设计使得模型能够基于简短的粗略指令端到端地完成障碍物避免、目标识别与路径规划，摆脱对精确逐步指令的依赖。

**核心结论：**
- AutoFly 在整体成功率上达到 **47.9%**，显著超越 OpenVLA（44.0%）和 RT-2（41.9%），碰撞率降至 **21.9%**（Table 2）。
- 移除伪深度编码器后，成功率立即下降 **3.9%**，碰撞率上升 **2.6%**（Table 4），验证了空间感知模态的关键作用。
- 在动态障碍物场景中，伪深度编码器带来的增益最为显著：成功率提升 **9.9%**，碰撞率降低 **9.5%**（Table 8），证明几何推理在高度动态环境中的不可替代性。
- 简单的数据扩充、更强的 RGB 编码器或增加训练数据均无法替代伪深度编码器的增益（+3.9% vs 最大 +1.2%），进一步确认**三维几何理解是性能提升的根本原因**（Table 9）。

**方法定位：** AutoFly 属于 VLA 范式下的无人机导航方法，在空间感知模态（RGB + 伪深度）、训练策略（视觉-语言对齐预训练 + 空间感知动作微调两阶段）以及数据集平衡（基于语义分割的重要性采样）三个维度上对现有 VLA 基线进行了系统性改进。其架构由视觉编码器（SigLIP-DINOv2）、伪深度生成器（Depth Anything V2）、Siamese 深度投影器、大语言模型（LLaMA2 7B）和动作解令牌器五个模块构成流水线。

**证据强度：** 核心结论均有严格消融实验支撑，置信度达 0.95 以上；仿真到真实环境的迁移实验（室内 60%，室外 55%）进一步验证了方法的实用性。需注意，当前方法在全局探索能力、360 度感知范围以及与环境交互的自适应学习方面仍存在局限。



无人机在野外环境中的自主导航是机器人领域的核心挑战之一，要求系统同时具备目标识别、三维空间推理和动态避障能力。近年来，视觉-语言-动作（Vision-Language-Action, VLA）模型在具身智能任务中展现出强大的泛化潜力，为无人机视觉语言导航（VLN）开辟了新路径。

然而，现有无人机VLN系统存在一个根本性瓶颈：**它们依赖详细的逐步导航指令**（如"左转30度，前进5米，绕过左侧柱子"），这些指令预先规定了明确的航路点和机动动作。在真实野外场景中，人类往往只能提供粗略的方向性引导（如"向前飞，避开树木，找到灰色椅子"），无法给出精确的逐步指示。当面对未知动态环境时，现有系统缺乏自主决策、三维避障和空间推理能力，难以将简短的粗粒度指令转化为安全有效的飞行行为。

这一瓶颈的深层原因在于**空间感知模态的缺失**。当前主流VLA基线（如**RT-2**和**OpenVLA**）仅依赖RGB图像作为视觉输入，使用SigLIP-DINOv2等二维视觉编码器提取特征。尽管这些编码器在语义理解上表现优异，但它们无法从单目图像中恢复三维几何信息，导致模型缺乏对深度、距离和空间关系的显式理解。在需要精确避障的飞行场景中，这种平面化的感知方式成为性能上限的关键制约。

AutoFly的动机正是填补这一空间推理缺口。其核心洞察在于：**通过引入伪深度编码器，赋予VLA模型三维空间推理能力**，使其能够基于简短的粗略指令端到端地执行障碍物避免、目标识别和路径规划，摆脱对精确逐步指令的依赖，在未知环境下实现鲁棒自主飞行。这一设计选择由因果性消融实验强力支撑：移除伪深度编码器后，成功率立即下降3.9%，碰撞率上升2.6%；而在动态障碍物场景中，伪深度编码器带来的增益更为显著——成功率提升9.9%，碰撞率降低9.5%（Table 8）。更重要的是，简单的数据扩充、更强的RGB编码器或增加训练数据均无法替代这一几何推理能力（Table 9），证明三维空间理解是无人机VLA导航中不可替代的关键要素。



## 核心方法与创新机理

AutoFly的核心创新在于赋予VLA模型**三维空间几何理解能力**，使其摆脱对精确逐步导航指令的依赖，在仅有粗略方向引导的未知动态环境中实现端到端自主飞行。这一能力通过三个关键设计实现，构成一个完整的因果链条。

### 伪深度编码器：从单目RGB中恢复空间几何

现有VLA基线（如OpenVLA、RT-2）仅依赖RGB视觉特征，缺乏对场景三维结构的显式建模，导致在障碍物密集或动态环境中碰撞率居高不下。AutoFly引入**伪深度编码器**（Pseudo-Depth Encoder），利用Depth Anything V2从单目RGB观测中生成高保真深度图，再通过专门的深度投影器将深度信息转化为与视觉令牌维度对齐的几何令牌序列。这一设计使LLM骨干能够同时感知场景的语义内容（来自SigLIP-DINOv2视觉编码器）和空间结构（来自伪深度编码器），从而在推理时实现三维避障和空间路径规划。

消融实验直接验证了这一创新的因果效应：移除伪深度编码器后，整体成功率立即从**47.9%下降至44.0%（−3.9%）**，碰撞率从**21.9%上升至24.5%（+2.6%）**（Table 4）。更关键的是，在动态障碍物场景中，伪深度编码器的增益最为显著——成功率从40.8%跃升至**50.7%（+9.9%）**，碰撞率从30.2%降至**20.7%（−9.5%）**（Table 8），证明该模块正是解决动态环境空间推理瓶颈的核心因果开关。

### 两阶段训练策略：先对齐后微调

AutoFly采用**渐进式两阶段训练范式**，区别于基线模型的单阶段VLA微调：

- **阶段一（视觉-语言对齐预训练）**：基于Prismatic-VLMs的prism-siglip-7b配置初始化，冻结视觉编码器和LLM，仅训练视觉-语言投影器，建立稳健的跨模态语义对齐。
- **阶段二（空间感知动作微调）**：联合微调伪深度编码器与VLA骨干，使模型在已对齐的语义空间基础上，进一步融合几何空间线索进行动作预测。

这一设计解决了直接端到端训练时视觉、深度、语言三种模态难以有效对齐的问题。阶段一提供了稳定的语义锚点，阶段二则在此基础上注入空间推理能力，避免了模态间的相互干扰。

### 数据集重平衡：消除行为偏差

原始专家演示数据存在严重的**行为偏差**——避障行为占据主导，导致模型倾向于保守避障而忽视目标导向的路径规划。AutoFly通过基于语义分割的轨迹标注（将每帧标记为“避障”或“目标搜索”阶段），结合重要性采样对数据集进行重平衡，确保模型在学习过程中同等重视两种核心行为。

这一设计的必要性由Table 6的消融实验证实：**未重平衡的基线成功率仅为16.6%**，碰撞率高达32.9%，路径效率低至43.7%。重平衡后成功率飙升至47.9%，提升幅度超过31个百分点，说明解决数据偏差是实现有效空间推理的前提条件。

### 深度-视觉对齐的Siamese投影

伪深度编码器的有效性高度依赖于深度特征与视觉特征的**对齐方式**。AutoFly采用Siamese MLP投影器——深度投影器和视觉投影器共享参数，确保两种模态在统一的特征空间中进行融合。Table 7显示，Siamese方案（47.9% SR）较非Siamese方案（43.3% SR）提升**3.3%**成功率，验证了参数共享对跨模态对齐的关键作用。

值得注意的是，简单的替代方案无法弥补伪深度编码器的增益。Table 9表明，增加1000条额外训练数据仅提升1.2%成功率，使用更强的RGB编码器仅提升0.7%，均远低于伪深度编码器带来的3.9%增益。这证明**显式的几何推理能力不可被更多数据或更强的语义特征所替代**，是野外未知环境下鲁棒导航的刚需。



![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_88RKxlFUNY/figures/002_Figure_2.jpg]]
*Figure 2: Framework of AutoFly. AutoFly takes RGB observations and linguistic instructions as inputs and directly outputs high-level actions. These actions, combined with initial actions derived from coarse-grained positional or directional information, form action sequences*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_88RKxlFUNY/figures/010_Figure_4.jpg]]
*Figure 4: Comparison of three paradigms for integrating depth information during fine-tuning: (a) Siamese MLP projector, (b) Non-Siamese MLP projector, (c) Direct depth integration*

AutoFly 是一个端到端的视觉-语言-动作（VLA）模型，其核心设计目标是将路径规划、目标识别与障碍物避免统一到单一架构中，使无人机能够基于简短的粗略自然语言指令（如“向前飞行，避开树木，到达灰色椅子”）在未知环境中自主导航。与此前依赖逐步精确航点指令的方法（Lee et al., 2024; Liu et al., 2023b）形成根本性差异，AutoFly 仅需粗粒度的位置或方向信息作为初始动作引导（Figure 1）。

### 流水线模块与数据流

AutoFly 的推理流水线由五个核心模块串联构成（Figure 2）：

1. **Vision Encoder（视觉编码器）**：采用 SigLIP-DINOv2 融合编码器，从单目 RGB 观测 $z^{l-1}$ 中提取视觉令牌。该编码器结合了 SigLIP 的对比语言-图像预训练能力与 DINOv2 的自监督视觉特征，为后续多模态融合提供丰富的语义表征。

2. **Pseudo-Depth Generator（伪深度生成器）**：基于 Depth Anything V2（Yang et al., 2024）从同一 RGB 输入生成高保真度深度图。该模块是赋予模型三维空间推理能力的关键——无需额外深度传感器，仅从单目视觉中恢复场景几何信息。

3. **Pseudo-Depth Projector（伪深度投影器）**：采用 Siamese MLP 结构，将深度图划分为 patch 后进行线性投影，使其维度与视觉令牌对齐。投影后的深度令牌与视觉令牌通过拼接操作融合，形成统一的多模态嵌入序列 $\hat{\mathbf{z}}^l$：
   $$\hat{\mathbf{z}}^l = \mathrm{Concat}(\mathrm{Proj}(\mathrm{Proj}_{\mathbf{d}}(\mathrm{DPATv2}(z^{l-1}))), \mathrm{Proj}(\mathrm{SigLIP-DINOv2}(z^{l-1})))$$
   Siamese 设计（即深度投影器与视觉投影器共享参数）确保了跨模态特征空间的一致性，消融实验表明该设计较非 Siamese 方案成功率提升 3.3%（Table 7）。

4. **Large Language Model（大语言模型）**：以 LLaMA2 7B 为骨干，接收融合后的视觉-深度嵌入与 Token 化的语言指令 $q^l$，自回归地生成动作令牌：
   $$\hat{\mathbf{a}}^l = \mathrm{LLM}(\mathrm{Concat}(\hat{\mathbf{z}}^l, \mathrm{Tokenizer}(q^l)))$$

5. **Action De-tokenizer（动作解令牌器）**：将 LLM 输出的离散动作令牌映射为连续的三维速度指令 $\mathbf{a}^l$，直接控制无人机的平移与偏航运动：
   $$\mathbf{a}^l = \mathrm{De-Tokenizer}(\hat{\mathbf{a}}^l)$$
   具体实现沿用 OpenVLA 的方法，利用 LLaMA2 词表中最后 256 个令牌作为动作空间。

### 训练范式

AutoFly 采用渐进式两阶段训练策略（Section 3.4）：

- **阶段一（视觉-语言对齐预训练）**：以 Prismatic-VLMs 的 prism-siglip-7b 配置初始化模型，冻结视觉编码器与 LLM，仅训练两层 MLP 投影器，在大规模视觉-语言数据上建立跨模态对齐。
- **阶段二（空间感知动作微调）**：核心创新在于将伪深度编码器与预训练的 VLA 骨干联合微调。此阶段引入导航数据集，使模型学习利用几何空间线索进行端到端决策。训练采用标准的自回归交叉熵损失。

### 部署架构

实际部署中，模型运行于远程服务器，通过局域网与无人机通信（Figure 13）。系统采用多进程并行推理流水线（Figure 14）：视觉处理管线与 LLM 推理管线并发执行——在初始串行周期后，第 $t+1$ 帧的视觉处理与第 $t$ 帧的 LLM 推理重叠进行，将单帧延迟从 120ms 降至 85ms，实现约 15 FPS 的实时控制。



AutoFly 的核心架构由五个模块级联构成，形成从单目感知到连续动作的端到端流水线。

**Vision Encoder（视觉编码器）** 采用 SigLIP-DINOv2 融合骨干，从 RGB 观测 $z^{l-1}$ 中提取视觉令牌。该编码器继承自 Prismatic-VLMs 的 prism-siglip-7b 配置，为后续多模态融合提供语义丰富的视觉表征。

**Pseudo-Depth Generator（伪深度生成器）** 是赋予模型三维空间推理能力的关键创新。它利用 Depth Anything V2 从单目 RGB 图像生成高保真深度图，无需额外深度传感器。生成的深度图保留了场景的几何结构信息，使模型能够感知障碍物距离和空间布局。

**Pseudo-Depth Projector（伪深度投影器）** 采用 Siamese MLP 结构，将深度图划分为 patch 后进行线性投影，使深度令牌维度与视觉令牌对齐。其双分支共享参数的设计（Figure 4a）确保了跨模态表征的一致性，消融实验表明该设计较非 Siamese 方案成功率提升 3.3%（47.9% vs 43.3%，Table 7）。

多模态嵌入的准备过程由公式 (1) 描述：

$$\hat{\mathbf{z}}^l = \mathrm{Concat}(\mathrm{Proj}(\mathrm{Proj}_{\mathbf{d}}(\mathrm{DPATv2}(z^{l-1}))), \mathrm{Proj}(\mathrm{SigLIP-DINOv2}(z^{l-1})))$$

其中 $\mathrm{DPATv2}(z^{l-1})$ 为 Depth Anything V2 从上一帧观测生成的深度图，$\mathrm{Proj}_{\mathbf{d}}$ 为 Siamese MLP 深度投影，$\mathrm{Proj}$ 为视觉投影，$\mathrm{Concat}$ 将深度令牌与视觉令牌拼接为统一的视觉嵌入序列 $\hat{\mathbf{z}}^l$。

**Large Language Model（大语言模型）** 采用 LLaMA2 7B，负责融合视觉嵌入与语言指令并生成动作令牌。动作令牌生成由公式 (2) 给出：

$$\hat{\mathbf{a}}^l = \mathrm{LLM}(\mathrm{Concat}(\hat{\mathbf{z}}^l, \mathrm{Tokenizer}(q^l)))$$

其中 $q^l$ 为当前步骤的语言指令，$\mathrm{Tokenizer}$ 将其转换为语言令牌，与视觉嵌入 $\hat{\mathbf{z}}^l$ 拼接后送入 LLM，输出离散动作令牌序列 $\hat{\mathbf{a}}^l$。

**Action De-tokenizer（动作解令牌器）** 将 LLM 输出的离散令牌映射为连续的三维速度指令。沿用 OpenVLA 的方法，使用 LLaMA2 词汇表中最后 256 个令牌作为动作令牌空间，通过解令牌化得到连续动作向量：

$$\mathbf{a}^l = \mathrm{De-Tokenizer}(\hat{\mathbf{a}}^l)$$

最终，任务形式化为最优策略 $\pi^{*} : ({\bar{O}}, {\bar{L}}) \to A$，将观测序列与语言指令映射到三维动作空间，涵盖避障、目标识别与路径规划的统一决策。

**训练范式** 采用两阶段策略：第一阶段基于 Prismatic-VLMs 的 prism-siglip-7b 配置进行视觉-语言对齐预训练；第二阶段联合微调伪深度编码器与 VLA 骨干，使用自回归训练范式和标准交叉熵损失，使模型能够利用几何空间线索进行导航决策。



## 实验与关键发现

### 4.1 评估指标与实验设置

AutoFly采用三个核心指标评估导航性能，定义如下：

$$\mathrm { S R } = | \mathcal { S } | / N , \quad \mathrm { C R } = | \mathcal { C } | / N , \quad \mathrm { P E R } = | \mathcal { E } | / | \mathcal { S } |$$

其中SR（Success Rate）为成功到达目标且偏差满足阈值的试验比例，CR（Collision Rate）为发生碰撞的试验比例，PER（Path Efficiency Rate）为成功试验中路径效率的均值。模型采用自回归训练范式，保持基础语言模型的交叉熵损失函数，直接输出机器人动作指令。

### 4.2 整体性能对比

**Table 2** 展示了AutoFly与三类VLA基线在仿真环境下的综合性能对比。AutoFly在整体成功率上达到**47.9%**，显著超越当前最强基线OpenVLA（44.0%，+3.9%）和RT-2（41.9%，+6.0%），同时将碰撞率降至21.9%（OpenVLA为24.5%，降低2.6%），路径效率提升至77.3%（+2.2%）。这一优势在未见场景和未见目标条件下均保持稳定，验证了伪深度编码器赋予的三维空间推理能力对导航鲁棒性的关键作用。


![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_88RKxlFUNY/figures/015_Table_2.jpg]]
*Table 2: Overall performance metrics for quadrotor (all values in %). Here, we report three metrics: Success Rate (SR↑), Collision Rate (CR↓), and Path Efficiency Rate (PER↑). Detailed baseline implementations are provided in the Appendix A.4.1*

早期VLA基线RT-1仅取得24.3%的成功率，表明简单的EfficientNet+FiLM架构难以应对复杂三维导航任务。RT-2将动作视为文本Token的策略虽有改进（41.9%），但仍受限于缺乏显式几何理解。OpenVLA凭借DINOv2视觉特征和动作块机制达到44.0%，但AutoFly通过引入伪深度编码器实现了决定性的性能跃升。

**Figure 7** 按目标类别分解的性能分布显示，AutoFly在各类别上均保持稳定的PER（76.8%-78.1%），CR在Geometry类别上最低（12.4%），在Vehicle类别上最高（30.9%），反映出不同目标形状和尺寸对避障难度的差异化影响。

### 4.3 仿真到真实迁移

**Table 3** 报告了仿真到真实场景的迁移成功率。在室内环境中，当仿真-真实数据比例为10K:1K时，AutoFly达到**60%**的成功率；室外森林场景下达到**55%**。值得注意的是，随着仿真数据比例从0K:1K增至10K:1K，室内PER从61.1%提升至76.5%，表明大规模仿真预训练对路径效率的持续增益。CR在中间比例出现峰值，提示数据量增加初期可能引入更具挑战性的场景分布。

### 4.4 消融实验

#### 4.4.1 伪深度编码器的核心作用

**Table 4** 的深度编码器消融实验直接验证了本文核心主张：移除伪深度编码器后，成功率从47.9%下降至44.0%（**-3.9%**），碰撞率从21.9%上升至24.5%（+2.6%），路径效率从77.3%下降至75.1%（-2.2%）。这三个指标的同步退化表明，伪深度编码器提供的几何空间信息同时惠及避障决策质量和路径规划效率。


![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_88RKxlFUNY/figures/018_Table_4.jpg]]
*Table 4: Results (%) for depth encoder ablation*

#### 4.4.2 深度投影器设计的影响

**Table 5** 对比了三种深度投影方案：本文的专用深度投影器（47.9% SR）显著优于使用SigLIP（42.4%）和DINOv2（41.3%）作为深度投影器的方案。后两者的PER分别降至64.8%和65.1%，远低于本文方案的77.3%，说明通用视觉编码器无法有效提取深度图中的几何结构信息，专用投影器对空间特征编码至关重要。

**Table 7** 进一步检验了深度-视觉-语言对齐方式：Siamese MLP投影器（参数共享）达到47.9% SR，而非Siamese方案仅43.3%（**-4.6%**），验证了参数共享对跨模态特征一致性的关键作用。直接深度集成方案性能更低，说明简单的通道拼接无法实现有效的多模态融合。

#### 4.4.3 数据集重平衡的必要性

**Table 6** 揭示了数据分布偏差的严重性：未进行重平衡的基线配置成功率仅为16.6%，碰撞率高达32.9%，路径效率仅43.7%。重平衡后成功率跃升至47.9%（**+31.3%**），碰撞率降低11.0%，路径效率提升33.6%。这一巨大差距源于原始数据集中避障行为占主导，导致模型偏向保守的避障策略而忽视目标导向的路径规划。基于语义分割和重要性采样的重平衡策略有效解决了这一行为偏差问题。

#### 4.4.4 挑战性场景下的增益分析

**Table 8** 在三种挑战性场景下对比了有无伪深度编码器的性能：


![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_88RKxlFUNY/figures/028_Table_8.jpg]]
*Table 8: Overall performance metrics for quadrotor in challenging scenarios (all values in %). Here, we report three metrics: Success Rate (SR↑), Collision Rate (CR↓), and Path Efficiency Rate (PER↑). The last line represents the gain*

- **动态障碍物场景**：增益最为显著，SR提升**9.9%**（40.8%→50.7%），CR降低9.5%。动态环境对实时深度感知的需求最为迫切，伪深度编码器提供的几何线索使模型能够预测障碍物运动趋势并及时调整路径。
- **密集柱体场景**：SR提升**7.7%**，CR降低7.9%。密集排列的柱体要求精确的间隙判断，深度信息直接辅助了可通过性评估。
- **密集森林场景**：SR提升**8.1%**，CR降低9.0%。非结构化的自然障碍物形态复杂，深度图提供的三维结构信息弥补了纯RGB特征在纹理重复区域的歧义性。

增益幅度随场景难度递增而增大的趋势表明，伪深度编码器的价值在几何推理需求越高的场景中越突出。

#### 4.4.5 简单替代方案的局限性

**Table 9** 系统排除了其他可能解释性能增益的混淆因素：


![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_88RKxlFUNY/figures/029_Table_9.jpg]]
*Table 9: Comparison with simpler alternative approaches (all values in %). Here, we report three metrics: Success Rate (SR↑), Collision Rate (CR↓), and Path Efficiency Rate (PER↑)*

- **增加1000条训练数据**仅提升1.2% SR，远低于伪深度编码器的3.9%增益。
- **更强的RGB编码器**（如更大规模的视觉骨干）仅提升0.7%。
- **数据扩充策略**（如随机裁剪、色彩抖动）提升约0.5%。

这些结果表明，性能增益的本质来源是**几何推理能力**而非数据规模或视觉表征质量，简单的工程优化无法替代显式的三维空间理解。

### 4.5 失败模式分析

尽管AutoFly在整体指标上表现优异，实验仍揭示了若干系统性失败模式：

1. **视野外目标丢失**：当目标不在前视相机视野内时，模型缺乏系统搜索策略，导致在需要大角度转向的场景中成功率显著下降。这是单目前向感知的固有局限。

2. **动态障碍物交互失败**：在动态障碍物场景中，虽然伪深度编码器带来了最大增益，但绝对碰撞率仍达21.9%，说明模型对高速移动或突然出现的障碍物反应不足。当前监督微调范式无法通过与环境交互学习自适应避障策略。

3. **语义歧义导致的路径偏差**：当语言指令中的目标描述与场景中多个相似物体匹配时，模型可能选择错误的导航目标，尤其在Furniture和Equipment类别中CR相对较高（Figure 7）。

4. **仿真到真实的感知差距**：真实场景中的光照变化、纹理差异和传感器噪声导致深度估计质量下降，室外场景成功率（55%）低于室内（60%），提示伪深度编码器对域偏移的鲁棒性仍有提升空间。



## 定位与知识库关联

### 1 问题定位：从逐步指令到粗略引导的范式跃迁

现有无人机视觉-语言导航（VLN）系统，如 **ANDH** 和 **AerialVLN**，其核心假设是系统能够获得详细的逐步导航指令——这些指令预先规定了明确的航点与飞行动作序列（Figure 1 左）。这一范式将无人机的自主性局限在执行层面：模型只需忠实地将指令映射为动作，而无需理解空间几何、进行避障决策或动态路径规划。

AutoFly 的根本性突破在于**将导航范式从“指令执行”提升为“目标导向的自主决策”**。系统仅接收简短的粗略自然语言指令（如“向前移动并避开堆叠的障碍物，到达红色跑车”），以及粗粒度的位置或方向信息，便需端到端地完成障碍物避免、目标识别与路径规划的全部推理（Figure 1 右）。这一设定更贴近真实野外场景——操作员无法预知环境中的所有障碍物分布，只能给出方向性引导。

这一范式跃迁对应的**核心瓶颈**是：现有 VLA 模型（如 **OpenVLA**、**RT-2**）仅依赖 RGB 视觉特征，缺乏三维空间几何理解能力，无法在仅有粗略引导的条件下进行可靠的避障与空间推理。AutoFly 通过引入**伪深度编码器**（Pseudo-Depth Encoder）解决了这一瓶颈。

### 2 方法谱系：VLA 模型在无人机导航中的演进

#### 2.1 基线方法定位

AutoFly 建立在 VLA（Vision-Language-Action）模型的最新进展之上。其直接基线包括：

- **RT-1**：基于 EfficientNet 视觉骨干和 FiLM 条件机制的早期 VLA 模型，将视觉观测和语言指令融合后输出离散化动作。在 AutoFly 的评估中，RT-1 仅取得 24.3% 的成功率（Table 2），反映出其架构在处理复杂三维导航任务时的根本性不足。

- **RT-2**：将动作建模为文本 Token，利用大规模视觉-语言模型的推理能力进行机器人控制。RT-2 在 AutoFly 数据集上取得 41.9% 的成功率（Table 2），较 RT-1 有显著提升，但仍受限于对空间几何的隐式建模。

- **OpenVLA**：基于开源 Prismatic VLM（prism-siglip-7b 配置，使用 SigLIP-DINOv2 视觉编码器与 LLaMA2 7B 语言骨干）的强 VLA 基线，采用动作块（action chunks）输出。OpenVLA 在 AutoFly 数据集上取得 44.0% 的成功率（Table 2），是当前最强的开源 VLA 基线。

#### 2.2 AutoFly 的方法创新：四个关键槽位

AutoFly 在 OpenVLA 架构的基础上，通过四个关键槽位的变更实现了性能跃升：

| 槽位 | 基线值（OpenVLA） | AutoFly 方案 | 证据锚点 |
|------|-------------------|-------------|---------|
| **空间感知模态** | 仅 RGB（SigLIP-DINOv2） | RGB + 伪深度（Depth Anything V2 → Siamese MLP 投影） | Section 3.2 |
| **训练策略** | 单阶段 VLA 微调 | 两阶段：视觉-语言对齐预训练 + 空间感知动作微调 | Section 3.4 |
| **数据集平衡** | 原始不平衡分布（避障行为占主导） | 基于语义分割和重要性采样的重平衡 | Section 3.3 |
| **深度-视觉对齐** | 无深度或直接拼接 | Siamese MLP 投影器（参数共享） | Section 3.4, Table 7 |

**伪深度编码器**是 AutoFly 区别于所有现有 VLA 基线的核心模块。其设计包含三个关键决策：

1. **深度生成**：使用 Depth Anything V2 从单目 RGB 生成高保真深度图，避免依赖额外的深度传感器（Section 3.2）。
2. **深度投影**：通过专门的 MLP 投影器将深度图划分为 patch 并线性投影，与视觉 Token 维度对齐。消融实验表明，专用深度投影器（47.9% SR）显著优于直接使用 SigLIP（42.4%）或 DINOv2（41.3%）处理深度图（Table 5）。
3. **Siamese 参数共享**：深度投影器采用 Siamese 结构（两个分支共享参数），确保深度特征与视觉特征在投影空间中的一致性。非 Siamese 方案的成功率下降至 43.3%（Table 7），验证了参数共享对跨模态对齐的关键作用。

**两阶段训练策略**进一步强化了空间感知能力（Section 3.4）：
- **阶段一**：视觉-语言对齐预训练，使用 Prismatic-VLMs 的 prism-siglip-7b 初始化。
- **阶段二**：空间感知动作微调，联合优化伪深度编码器与 VLA 骨干，使模型能够利用几何空间线索进行导航决策。

### 3 知识库定位：与相关工作的边界

#### 3.1 与地面 VLN 的差异

地面 VLN 数据集（如 R2R、RxR、REVERIE）通常提供逐步导航指令，且环境约束相对简单（二维平面运动）。AutoFly 面向的是**三维空间中的无人机导航**，需要同时处理高度变化、六自由度运动与三维避障。Table 1 的系统对比显示，现有无人机 VLN 数据集（ANDH、AerialVLN、CityNav 等）在轨迹数量、指令多样性、真实世界覆盖等方面均存在局限，AutoFly 构建的数据集在规模和多样性上均有显著提升。

#### 3.2 与端到端无人机导航的差异

传统的端到端无人机导航方法（如基于深度强化学习的方案）通常依赖精确的坐标目标或航点，而非自然语言指令。AutoFly 将自然语言理解与三维空间推理统一在 VLA 框架内，实现了从语言到动作的直接映射。

#### 3.3 伪深度 vs. 真实深度 vs. 更强 RGB 编码器

一个关键问题是：伪深度编码器的增益是否可被更简单的方案替代？Table 9 给出了明确的否定答案：
- 增加 1000 条训练数据仅提升 1.2% 成功率
- 更强的 RGB 编码器（更大规模的视觉骨干）仅提升 0.7%
- 伪深度编码器带来 3.9% 的增益

这表明**几何推理能力是视觉特征无法替代的独立信息维度**。伪深度编码器提供的不是更精细的纹理或语义，而是对三维空间结构的显式建模。

### 4 适用边界与失效模式

#### 4.1 已知局限

AutoFly 在以下场景中存在明确的性能边界：

1. **全局探索能力缺失**：当目标不在前视相机视野内时，AutoFly 缺乏系统性的搜索策略。模型只能基于当前观测做出反应，无法规划“回头搜索”或“绕行寻找”等全局行为（Section Limitations）。

2. **感知范围受限**：仅依赖前向单目 RGB 和伪深度，无法感知 360° 环境中的障碍物或地标。在需要侧向或后方避障的场景中，模型可能因信息缺失而失败。

3. **动态场景的适应性不足**：当前训练范式为监督微调（SFT），模型无法与环境直接交互以学习自适应策略。尽管伪深度编码器在动态障碍物场景中带来了最大的相对增益（SR 提升 9.9%，Table 8），但整体成功率仍仅为 50.7%，表明高度动态场景仍是显著挑战。

#### 4.2 数据集偏差与泛化边界

数据集重平衡实验（Table 6）揭示了原始数据中存在严重的行为偏差：未重平衡时成功率仅为 16.6%，重平衡后跃升至 47.9%。这表明 AutoFly 的性能高度依赖训练数据的分布质量。在分布外场景（如极端天气、完全未见的环境类型）中，性能可能显著下降。

Sim-to-Real 迁移实验（Table 3）显示，室内场景成功率为 60%，室外森林场景为 55%。室内外差异主要源于室外环境的非结构化特性（不规则树木、光照变化等），说明模型对结构化环境的依赖仍然较强。

### 5 开放问题与未来方向

基于上述分析，AutoFly 框架面临以下关键开放问题：

1. **大范围全局探索**：如何在 VLA 框架内引入显式的搜索策略或记忆机制，使模型能够在目标不可见时进行系统性探索？

2. **多传感器融合**：如何集成 LiDAR、环视相机等传感器，突破前向单目感知的物理限制，实现全方位环境感知？

3. **在线学习与自适应**：如何在训练中引入强化学习或在线适应机制，使模型能够通过与环境的交互学习更鲁棒的行为策略，特别是在高度动态场景中？

4. **指令粒度的自适应**：当前模型在“粗略指令”设定下表现出色，但如何在指令信息量变化时自适应调整依赖程度——当有更详细指令时充分利用，当仅有模糊引导时保持鲁棒——仍是一个开放问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/AutoFly_Vision_Language_Action_Model_for_UAV_Autonomous_Navigation_in_the_Wild.pdf]]

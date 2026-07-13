---
title: "EE-RL: Vision Language Guided Reinforcement Learning with Explorer and Expert model for End-to-End Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EE_RL_Vision_Language_Guided_Reinforcement_Learning_with_Explorer_and_Expert_model_for_End_to_End_Autonomous_Driving.pdf
project_link: null
code_link: "https://github.com/CAVTestLab/EE-RL"
aliases:
- EE-RL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入经LoRA微调的视觉语言模型（VLM）作为专家，提供稀疏关键场景的语义推理与奖励生成，同时通过StateHash算法跳过冗余VLM调用，并与RL探索者共享双经验回放缓冲区，从而将VLM的常识推理能力注入RL训练。
primary_logic: 利用RL探索者处理常规驾驶任务并从环境中试错，同时部署VLM专家专门负责稀疏关键场景的推理和奖励构造，两者产生的经验存入双回放缓冲区联合优化策略，用感知哈希（StateHash）消除冗余VLM推理以降低延迟，实现高效协同训练。
claims:
- EE-RL在Town03的驾驶分数（DS）相比VLM-RL提升19.82%，违章分数（IS）提升20.98%
- EE-RL在Town05–06实现0%闯红灯事故概率和平均驾驶分数80.09
- StateHash将单VLM产生的专家经验从8126条提升至53783条，双VLM从17733条提升至90566条
- CARLA Town03 上 Driving Score (↑) = 69.35 (EE-RL SAC)
---

# EE-RL: Vision Language Guided Reinforcement Learning with Explorer and Expert model for End-to-End Autonomous Driving

> [!tip] 核心洞察
> 利用RL探索者处理常规驾驶任务并从环境中试错，同时部署VLM专家专门负责稀疏关键场景的推理和奖励构造，两者产生的经验存入双回放缓冲区联合优化策略，用感知哈希（StateHash）消除冗余VLM推理以降低延迟，实现高效协同训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | EE-RL：基于视觉语言引导的探索者-专家强化学习端到端自动驾驶框架 |
| 英文题名 | EE-RL: Vision Language Guided Reinforcement Learning with Explorer and Expert model for End-to-End Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_EE-RL_Vision_Language_Guided_Reinforcement_Learning_with_Explorer_and_Expert_CVPR_2026_paper.html) · [Code](https://github.com/CAVTestLab/EE-RL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EE-RL |
| Dataset | CARLA Town03, CARLA Town05 Long, CARLA Town05–06 |

> [!tip] 效果简介
> - CARLA Town03 上，Driving Score (↑) 69.35 (EE-RL SAC) vs 44.33 (RL-VLM-F) (+25.02 pp)；Infraction Score (↑) 72.33 (EE-RL SAC) vs 54.39 (VLM-RL) (+17.94 pp)。
> - CARLA Town05 Long 上，Driving Score (↑) 69.57 (EE-RL TD3) vs 64.03 (Interfuser) (+5.54 pp)。
> - CARLA Town05–06 上，Composite Score (↑) 80.09 (EE-RL SAC) vs 57.82 (VLM-RL) (+22.27 pp)。

## 概要

端到端自动驾驶旨在直接从传感器输入映射到控制指令，但现有强化学习（RL）方法在稀疏关键场景中严重退化——行人横穿、突发避障、红绿灯识别等安全关键事件发生频率低，试错探索难以获得足够的奖励信号，导致策略优化陷入瓶颈。

**EE-RL** 针对这一瓶颈提出“探索者-专家”协同范式：RL探索者负责常规驾驶任务的试错学习，经LoRA微调并INT4量化的视觉语言模型（VLM）作为专家，专门对稀疏关键场景进行语义推理并构造奖励信号。两者产生的经验存入双回放缓冲区联合优化策略，同时通过**StateHash**算法（基于RGB感知哈希与车辆状态相似度加权）跳过冗余VLM推理，在保证语义指导质量的前提下大幅降低计算延迟。

核心结论如下：

- **稀疏关键场景性能跃升**：在CARLA Town03上，EE-RL（SAC变体）驾驶分数（DS）达69.35，相比VLM-RL提升**19.82%**，违章分数（IS）提升**20.98%**；在Town05–06长距离泛化测试中，实现**0%闯红灯事故概率**，平均驾驶分数80.09。
- **StateHash显著提升专家经验产出**：单VLM配置下，专家经验从8126条增至53783条；双VLM配置下从17733条增至90566条。
- **框架组件协同有效**：多层注意力机制对碰撞率（CoR）影响最大，移除后CoR上升60.26%；双回放缓冲区中专家经验采样比在19%–24%时可最快完成红绿灯与避障任务。

在方法谱系中，EE-RL区别于纯IL基线（如**Transfuser** (Prakash et al., CVPR 2021)、**Interfuser** (Shao et al., CoRL 2023)）和RL专家蒸馏基线（如**Roach** (Zhang et al., ICCV 2021)），也不同于仅用VLM生成静态奖励函数的方案（**VLM-RM** (Rocamonde et al., arXiv 2023)、**RL-VLM-F** (Wang et al., arXiv 2024)），其关键创新在于将VLM作为持续运行的在线专家融入RL训练闭环，并通过StateHash与双回放缓冲区实现高效协同。方法仅在CARLA仿真环境验证，VLM推理的实时性与幻觉问题仍是实际部署的潜在限制。

端到端自动驾驶旨在将传感器输入直接映射为车辆控制指令，省去传统模块化流水线中的中间表征与人工规则设计。近年来，基于模仿学习（IL）和强化学习（RL）的方法在CARLA仿真环境中取得了显著进展，代表性工作包括**Transfuser**（Prakash et al., CVPR 2021）、**Interfuser**（Shao et al., CoRL 2023）和**Roach**（Zhang et al., ICCV 2021）等。然而，现有方法在稀疏关键场景中暴露出系统性缺陷。

**核心瓶颈**在于：安全关键事件（如行人突然横穿、前车紧急制动、红绿灯违规）在真实驾驶中发生频率极低，导致RL代理在试错过程中难以获得足够的奖励信号。常规驾驶任务（车道保持、定速巡航）的密集奖励会淹没稀疏关键场景的微弱反馈，使策略优化偏向安全保守行为，却无法有效应对突发危险。这一问题在仅使用规则奖励函数的RL基线中尤为突出——规则奖励缺乏对复杂交通语义的理解能力，无法区分“在绿灯时通过路口”与“闯红灯通过路口”的本质差异。

为弥补语义理解的缺口，近期工作尝试引入视觉语言模型（VLM）作为奖励信号源。**VLM-RL**（Huang et al., Transportation Research Part C 2025）将VLM生成的语义奖励引入RL训练，在一定程度上提升了场景理解能力；**RL-VLM-F**（Wang et al., arXiv 2024）进一步利用VLM偏好自动生成奖励函数。但这些方法存在两个根本性局限：其一，VLM仅被用作静态奖励生成器，而非持续参与训练的推理专家，无法在训练过程中动态适应策略的进化；其二，每次环境交互均调用VLM进行推理，引入巨大的计算延迟，严重制约了训练效率。

**本文的动机**由此明确：能否设计一种协同学习框架，让RL代理专注于常规驾驶任务的试错优化，同时让VLM作为持续运行的推理专家，专门负责稀疏关键场景的语义理解与奖励构造？这一“探索者-专家”范式需要解决三个关键技术挑战：（1）如何在不显著增加推理延迟的前提下，让VLM专家持续参与训练；（2）如何将RL探索经验与VLM专家经验有效融合，避免两类经验相互干扰；（3）如何保证VLM在自动驾驶场景中的推理准确性与一致性。

EE-RL正是在这一动机驱动下提出的解决方案：通过双回放缓冲区联合存储两类经验并按比例混合采样，实现常规场景与关键场景的平衡学习；通过StateHash算法对RGB图像和车辆运动状态进行感知哈希，跳过高度相似状态的冗余VLM推理，大幅降低计算开销；通过对VLM进行LoRA微调与INT4量化，在保持推理质量的同时压缩模型规模。这一设计使得VLM的常识推理能力能够高效注入RL训练过程，从而在稀疏关键场景中实现可靠的决策优化。

## 核心方法与创新机理

EE-RL的核心创新在于构建了一套**探索者-专家协同强化学习范式**，将经LoRA微调的视觉语言模型（VLM）作为持续运行的专家嵌入RL训练循环，专门解决端到端自动驾驶中稀疏关键场景（如避障、行人横穿、红绿灯识别）因安全事件稀少导致奖励信号不足的瓶颈。该框架通过三个关键机制实现了VLM常识推理与RL试错学习的高效融合。

### 探索者-专家双经验生成架构

传统RL基线（如**VLM-RL** (Huang et al., Transportation Research Part C 2025)、**RL-VLM-F** (Wang et al., arXiv 2024)）通常仅用VLM生成静态奖励函数，或每次状态均调用VLM导致计算冗余。EE-RL将系统解耦为两个角色：**Explorer（RL Agent）** 基于Actor-Critic架构与环境交互，收集常规驾驶经验；**Expert（VLM）** 由两个Qwen2.5-VL-32B经LoRA微调并INT4量化后持续运行，专门负责稀疏关键场景的语义推理与奖励生成，其中一个VLM在训练后期专注于该类场景。两者产生的经验分别存入双回放缓冲区，按比例混合采样联合优化策略，使RL策略同时受益于环境试错和语义指导。

### StateHash：感知哈希驱动的冗余推理消除

VLM推理的高延迟是实时训练的主要障碍。EE-RL设计了**StateHash算法**，通过RGB三通道独立离散余弦变换（DCT）计算图像感知哈希，并与车辆运动学状态相似度加权求和（$S_{total} = 0.7 S_{image} + 0.3 S_{state}$），跳过与历史状态高度相似的VLM推理。消融实验表明，StateHash在单VLM配置下将有效专家经验从8,126条提升至53,783条，双VLM下从17,733条提升至90,566条，显著加速训练并降低推理延迟。

### 多层注意力机制增强多模态感知

Explorer的Actor-Critic骨干网络集成了**多层注意力机制**：空间注意力通过$1 \times 1$卷积和Sigmoid从图像嵌入生成权重，增强关键局部特征感知；多模态联合特征经缩放点积注意力（$\mathbf{h}' = \mathrm{Softmax}(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}})\mathbf{V}$）实现跨模态理解。消融研究证实，该机制对碰撞率（CoR）影响最大——移除后CoR上升60.26%，是框架中最重要的增强组件。

### 与基线的本质差异

| 创新维度 | 基线方法 | EE-RL |
|---------|---------|-------|
| 专家角色 | 无VLM专家或仅生成静态奖励 | 两个LoRA微调VLM持续运行，专注稀疏关键场景推理 |
| 经验存储 | 单一RL回放缓冲区 | 双回放缓冲区（$B_{rl}$与$B_{vlm}$），按比例$\rho$混合采样 |
| VLM调用决策 | 每次状态均调用 | StateHash跳过冗余推理，大幅提升有效经验密度 |

这些创新协同作用，使EE-RL在CARLA Town03上相较VLM-RL实现驾驶分数（DS）+19.82%、违章分数（IS）+20.98%的提升，并在Town05–06上达到0%闯红灯事故概率。

EE-RL 的核心设计理念是**探索者–专家协同范式**（Explorer–Expert Paradigm）：让基于 Actor-Critic 的 RL 智能体（探索者）处理常规驾驶任务并从环境试错中学习，同时部署经 LoRA 微调的视觉语言模型（专家）专门负责稀疏关键场景的语义推理与奖励构造。两者产生的经验存入双回放缓冲区，按比例混合采样以联合优化策略，并通过 StateHash 算法消除冗余 VLM 推理，实现高效协同训练。

### 模块组成与数据流

框架由三个核心模块构成，其交互关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2656_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EE_RL_Vision_Langua/figures/002_Figure_2.jpg]]
*Figure 2: The overview of the proposed EE-RL framework*

1. **Explorer（RL 探索者）**：基于 Actor-Critic 架构，集成多层注意力机制。探索者直接与环境交互，接收单目前置摄像头图像和车辆状态（速度、转向角等），输出驾驶动作，并将交互产生的经验存入 RL 回放缓冲区 $B_{rl}$。多层注意力机制包含空间注意力（Spatial Attention）和多头自注意力（Scaled Dot-Product Attention），前者通过 $1 \times 1$ 卷积和 Sigmoid 从图像嵌入中生成空间注意力权重以增强关键局部特征感知，后者对多模态联合特征进行跨模态融合。

2. **Expert（VLM 专家）**：由两个 Qwen2.5-VL-32B 模型经 LoRA 微调并 INT4 量化后构成。专家持续运行，其中一个在训练后期专注于稀疏关键场景的推理。专家接收当前状态（RGB 图像与车辆运动学状态），输出语义推理结果和奖励信号 $r_t^e$，并将专家经验存入 VLM 回放缓冲区 $B_{vlm}$。为减少计算开销，StateHash 算法通过对 RGB 图像进行分通道离散余弦变换（DCT）感知哈希，并与车辆状态相似度加权计算总相似度 $S_{total} = 0.7 S_{image} + 0.3 S_{state}$，当相似度超过阈值时跳过 VLM 推理。

3. **Dual Replay Buffer（双回放缓冲区）**：同时维护 $B_{rl}$ 和 $B_{vlm}$ 两个经验池。每次训练迭代按比例 $\rho$ 从两个缓冲区混合采样：$n_{rl} = \lfloor \frac{\rho}{\rho+1} n \rfloor$ 条来自 RL 探索经验，$n_{vlm} = n - n_{rl}$ 条来自 VLM 专家经验。这一设计使策略既能从常规驾驶场景的试错中学习，又能从稀疏关键场景的语义指导中受益。

### 训练流程

训练过程中，探索者与环境交互产生状态-动作-奖励序列，同时专家对当前状态进行 VLM 推理（经 StateHash 筛选后）生成专家奖励 $r_t^e$。智能体的总奖励由规则奖励和专家奖励组合：$r_t = r_t^r + r_t^e$，并经过归一化处理 $\widehat{r_t} = \frac{r_t - r_{min}}{r_{max} - r_{min}}$ 以对齐不同数值范围。双回放缓冲区中的混合经验被用于优化 Actor-Critic 策略网络，使探索者逐步掌握稀疏关键场景的应对能力。

### 关键设计权衡

框架的核心权衡在于**推理效率与语义质量**：VLM 专家提供高质量的常识推理和奖励信号，但每次推理带来显著延迟。StateHash 通过感知哈希快速判断状态相似度，在保证语义质量的前提下大幅减少 VLM 调用次数——实验表明，使用单 VLM 时，StateHash 将专家经验从 8126 条提升至 53783 条；使用双 VLM 时，从 17733 条提升至 90566 条。双回放缓冲区的采样比例 $\rho$ 则平衡了试错学习与语义指导的权重，消融实验显示红绿灯任务在 19% 专家采样比时完成最快，避障任务在 24% 时最优。

EE-RL 框架由三个核心模块协同构成：**Explorer（RL探索者）**、**Expert（VLM专家）** 和 **Dual Replay Buffer（双回放缓冲区）**。以下逐一剖析各模块的设计机理与关键公式。

### Explorer：多层注意力 Actor-Critic 骨干

Explorer 基于 Actor-Critic 架构构建，负责与环境交互并收集常规驾驶经验。其核心创新在于集成了**多层注意力机制**，以增强对关键局部特征的感知能力和跨模态理解能力。

**空间注意力** 模块从图像嵌入中提取关键区域权重。给定图像嵌入 $\mathbf{z}_{img}$，通过 $1\times1$ 卷积和 Sigmoid 激活生成空间注意力图：

$$\mathbf{A}_{spatial} = \mathrm{Sigmoid}( \mathrm{Conv}_{1 \times 1}( \mathbf{z}_{img} )) \tag{1}$$

随后对注意力加权后的特征进行自适应平均池化，得到紧凑的图像特征表示：

$$\mathbf{f}_{img} = \mathrm{AdaptiveAvgPool}( \mathbf{A}_{spatial} \odot \mathbf{z}_{img} ) \tag{2}$$

**缩放点积自注意力** 用于融合多模态联合特征（图像、车辆状态等），通过标准的多头注意力机制实现跨模态信息整合：

$$\mathbf{h}' = \mathrm{Softmax}\left( \frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}} \right) \mathbf{V} \tag{4}$$

其中 $\mathbf{Q}$、$\mathbf{K}$、$\mathbf{V}$ 分别为查询、键、值矩阵，$d_k$ 为键向量的维度。该机制使 Explorer 能够在常规驾驶场景中有效建模时空依赖关系，为后续与 VLM 专家的协同奠定基础。

消融实验（Table 6）证实，多层注意力机制对碰撞率（CoR）的影响最大——移除后 CoR 上升 **60.26%**，验证了其在安全关键感知中的核心地位。

### Expert：StateHash 加速的 VLM 推理

Expert 由两个经 LoRA 微调的 **Qwen2.5-VL-32B** 视觉语言模型组成，专门负责稀疏关键场景（如红绿灯识别、行人横穿、避障）的语义推理与奖励生成。为解决 VLM 推理延迟高的问题，EE-RL 设计了 **StateHash** 算法来跳过冗余调用。

**StateHash 的核心思想**：对每个新状态，计算其与已处理状态的综合相似度，若超过阈值则复用历史推理结果，避免重复调用 VLM。

**图像相似度** 通过改进的感知哈希计算。对 RGB 三个通道分别进行 $8\times8$ 块的二维离散余弦变换（DCT）：

$$\mathbf{D}_c(u,v) = \sum_{x=0}^{63}\sum_{y=0}^{63} I_c(x,y) \cos\left[ \frac{\pi}{64}(x+\frac12)u \right] \cos\left[ \frac{\pi}{64}(y+\frac12)v \right], \quad c \in \{R,G,B\} \tag{6}$$

对 DCT 系数进行二值化得到各通道的哈希码，进而计算图像相似度 $S_{image}$。**车辆状态相似度** $S_{state}$ 基于速度、转向角等运动学参数计算。

**综合相似度** 以加权和形式融合两者：

$$S_{total} = 0.7 S_{image} + 0.3 S_{state} \tag{5}$$

权重分配反映了视觉信息在场景判别中的主导地位。当 $S_{total}$ 超过预设阈值时，StateHash 判定当前状态与历史状态高度相似，跳过 VLM 推理，直接复用已有的语义分析结果。

StateHash 的效果在 Section 4.4 中得到量化验证：在单 VLM 配置下，有效专家经验从 **8126 条提升至 53783 条**；双 VLM 配置下从 **17733 条提升至 90566 条**，大幅加速了训练并降低了推理延迟。

**VLM 的 LoRA 微调**：为让通用 VLM 适配自动驾驶场景，EE-RL 采用低秩适配（LoRA）对 Qwen2.5-VL-32B 进行微调。权重更新公式为：

$$\mathbf{W} \leftarrow \mathbf{W} + \mathbf{B A}, \quad \mathbf{B} \in \mathbb{R}^{m \times r}, \quad \mathbf{A} \in \mathbb{R}^{r \times n} \tag{11}$$

其中秩 $r=64$，引入约 120M 可训练参数。合并后的权重进一步量化为 **INT4** 精度以加速推理，同时保持思维链推理过程固定不变。

### Dual Replay Buffer：平衡试错与语义指导

传统 RL 仅使用单一回放缓冲区存储环境交互经验，在稀疏关键场景中难以获得足够的正向奖励信号。EE-RL 设计了**双回放缓冲区**，同时存储两类经验：
- **$B_{rl}$**：Explorer 与环境交互产生的常规驾驶经验
- **$B_{vlm}$**：Expert 对稀疏关键场景的语义推理与奖励经验

每批训练样本按比例 $\rho$ 从两个缓冲区混合采样，采样数量由下式确定：

$$n_{rl} = \left\lfloor \frac{\rho}{\rho+1} n \right\rfloor, \quad n_{vlm} = n - n_{rl} \tag{12}$$

其中 $n$ 为批次总样本数，$n_{rl}$ 和 $n_{vlm}$ 分别为从 RL 回放池和 VLM 回放池采样的数量。消融实验（Figure 6）揭示了 $\rho$ 对任务完成效率的影响：红绿灯任务在专家经验采样比 **19%** 时完成最快，避障任务则在 **24%** 时最优。这一机制使得策略能够同时从常规场景的试错学习和关键场景的语义指导中获益，有效缓解了稀疏奖励问题。

## 实验与关键发现

### 核心瓶颈与实验动机

端到端强化学习在CARLA仿真中面临一个根本性瓶颈：安全关键事件（行人横穿、前车急刹、红绿灯违规、障碍物避让）在驾驶过程中极为稀疏，RL探索者难以通过随机试错获得足够的正向奖励信号。这导致策略在常规场景下表现尚可，但在稀疏关键场景中性能严重退化。EE-RL的核心实验目标正是验证“VLM专家语义推理 + 双回放缓冲区 + StateHash冗余跳过”这一组合能否系统性地解决该问题。

### 训练性能评估（Table 2）

Table 2展示了在CARLA四个城镇（Town01–04）上的训练性能，评估指标包括碰撞率（CoR ↓）、违章分数（IS ↑）和驾驶分数（DS ↑）。EE-RL在三个off-policy Actor-Critic变体（SAC、TD3、DDPG）上均表现出跨方法一致的性能优势：

- **Town01（最简城镇）**：EE-RL SAC取得CoR 1.37、IS 92.16、DS 88.35，EE-RL TD3取得CoR 1.25、IS 88.82、DS 86.43，均显著优于所有IL和RL基线。
- **Town03（复杂城镇，含多路口和密集交通）**：EE-RL SAC的DS达到69.35，相比最强RL基线VLM-RL（DS 57.89）提升**+19.82%**，IS从54.39提升至72.33（**+20.98%**）；相比RL-VLM-F（DS 44.33）提升**+25.02个百分点**。这一结果表明，VLM专家在复杂场景中的语义推理能力是性能跃升的关键驱动力。
- **跨RL算法泛化性**：EE-RL TD3和EE-RL DDPG同样在Town03上取得DS 65.81和63.52，分别超过VLM-RL 7.92和5.63个百分点，证明该框架不依赖特定RL算法。

### 测试性能与泛化性（Table 3, Table 4）

![[assets/figures/papers/paper_list_l2656_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EE_RL_Vision_Langua/figures/008_Table_3.jpg]]
*Table 3: Testing performance evaluation. Results indicate that EE-RL and its variants exhibit superior generalization and scene understanding across diverse environments, demonstrating stable transferability among off-policy actor–critic frameworks*

![[assets/figures/papers/paper_list_l2656_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EE_RL_Vision_Langua/figures/009_Table_4.jpg]]
*Table 4: Performance evaluation of the Town05 benchmark*

Table 3评估了模型在未见城镇（Town05、Town06）上的泛化能力。EE-RL SAC在Town05–06的平均综合分数（CS）达到**80.09**，相比VLM-RL（57.82）提升**+22.27个百分点**，相比Interfuser（59.25）提升+20.84个百分点。值得注意的是，EE-RL在Town05–06实现了**0%闯红灯事故概率**（Abstract），这是稀疏关键场景推理能力的直接证据。

Table 4进一步在Town05基准上对比了短路线和长路线性能。EE-RL TD3在长路线上取得DS 69.57，超过Interfuser（64.03）+5.54个百分点，超过Transfuser（31.44）一倍以上。长路线对持续决策能力要求更高，EE-RL的优势说明双回放缓冲区中的VLM专家经验有效缓解了长程依赖问题。

### 稀疏关键场景专项分析（Table 5）

![[assets/figures/papers/paper_list_l2656_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EE_RL_Vision_Langua/figures/010_Table_5.jpg]]
*Table 5: The performance comparison on sparse-critical scenarios*

Table 5专门针对稀疏关键场景（红绿灯识别、行人避让、障碍物规避）的事故概率进行对比。EE-RL在这些场景中的事故概率显著低于所有基线方法。这一结果直接验证了论文的核心假说：VLM专家通过语义推理为稀疏关键事件生成高质量奖励信号，弥补了RL探索者在这些场景中的试错盲区。

### 双回放缓冲区采样比消融（Figure 6）

![[assets/figures/papers/paper_list_l2656_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EE_RL_Vision_Langua/figures/011_Figure_6.jpg]]
*Figure 6: The Result of the Dual Replay Buffer Sampling*

Figure 6展示了双回放缓冲区中VLM专家经验采样比例ρ对任务完成时间的影响。关键发现：

- **红绿灯任务**：在ρ对应采样比约**19%**时，任务完成时间最短，说明适度的VLM指导对红绿灯合规性学习最有效。
- **障碍物避让任务**：最优采样比约为**24%**，略高于红绿灯任务，暗示避障场景需要更多的语义推理经验。
- 采样比过高或过低均导致性能下降：过低时VLM指导不足，过高时RL探索经验被稀释，策略失去对常规驾驶场景的泛化能力。

### StateHash加速效果消融（Figure 7）

![[assets/figures/papers/paper_list_l2656_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EE_RL_Vision_Langua/figures/012_Figure_7.jpg]]
*Figure 7: Experimental results on accelerating the VLM process. “1 VLM” and “2 VLM” denote training models inferred with one and two VLMs, respectively, without applying the StateHash mechanism*

Figure 7对比了有无StateHash机制下VLM专家经验的生成数量：

- 单VLM配置：无StateHash时仅生成**8,126条**专家经验，启用StateHash后提升至**53,783条**（**+561%**）。
- 双VLM配置：从**17,733条**提升至**90,566条**（**+411%**）。

StateHash通过RGB图像感知哈希（Eq. 6的2D DCT）与车辆状态相似度加权（Eq. 5，图像权重0.7，状态权重0.3）跳过高度相似状态的VLM推理，在保证推理质量的同时大幅提升经验生成效率。这是EE-RL能够在有限训练时间内获得充足VLM指导的关键工程手段。

### 框架组件消融（Table 6）

Table 6对EE-RL的各增强组件进行了消融研究：

- **多层注意力机制**：移除后碰撞率（CoR）上升**60.26%**，是所有组件中影响最大的。空间注意力（Eq. 1–2）增强关键局部特征感知，自注意力（Eq. 4）融合多模态输入，两者对安全驾驶至关重要。
- **LoRA微调**：移除后性能显著下降，验证了领域微调对VLM专家推理质量的必要性。LoRA以秩r=64引入约120M可训练参数，在保持通用常识能力的同时注入驾驶领域知识。
- **INT4量化**：移除量化后推理延迟增加，但精度提升有限，说明量化在效率与质量之间取得了良好平衡。

### 公平性说明

为公平比较，实验给VLM-RL方法额外引入了语义奖励机制以处理红绿灯合规性（Table 1备注），其他基线保持原样。此外，EE-RL仅使用**单目前置摄像头**，而部分基线（如Interfuser、Transfuser）使用多摄像头+LiDAR，EE-RL在传感器配置劣势下仍取得更优性能，进一步凸显了VLM专家推理的补偿作用。

### 失败模式与局限性

尽管EE-RL在CARLA基准上表现优异，但以下局限性需要关注：

1. **仿真到真实的迁移未验证**：所有实验均在CARLA仿真环境中完成，真实世界的传感器噪声、天气变化和动态交互可能导致VLM推理质量下降。
2. **VLM推理延迟**：尽管StateHash大幅减少了VLM调用次数，32B参数的Qwen2.5-VL模型在实时驾驶场景中仍可能引入不可忽略的延迟，这在论文中未给出具体延迟数值，需要手动验证。
3. **VLM幻觉风险**：在极端边缘场景中，VLM的推理一致性可能不足，生成的奖励信号可能误导策略优化。论文未对VLM幻觉率进行定量分析。
4. **微调数据依赖**：LoRA微调需要高质量驾驶场景标注数据，构建成本和专家注释需求限制了方法的可扩展性。

### 开放问题

- 能否用更轻量的VLM（如7B级别）替代32B模型，在保持推理质量的同时进一步降低延迟？
- 双回放缓冲区的采样比ρ目前为固定值，是否可以在训练过程中自适应调整以匹配不同训练阶段的需求？
- EE-RL如何与BEV感知、轨迹预测等模块整合，以进一步提升整体决策水平？

## 定位与知识库关联

### 一、与基线方法的关系

EE-RL 处于端到端自动驾驶中 **RL + VLM 协同** 这一新兴技术路线上。与已有工作的关系可从三个维度梳理：

**1. 纯模仿学习（IL）基线：传感器融合的先行者**

**Transfuser**（Prakash et al., CVPR 2021）和 **Interfuser**（Shao et al., CoRL 2023）代表了基于多模态融合的端到端 IL 方案。前者通过 Transformer 融合单目前视图像与 LiDAR 点云，后者进一步扩展为多视图多模态融合架构。这类方法的根本瓶颈在于：IL 受限于专家演示数据的分布，对稀疏关键场景（如突然横穿的行人、罕见红绿灯状态）缺乏鲁棒性。EE-RL 放弃了 IL 范式，转而采用 RL 从环境中试错学习，从根本上避开了分布外泛化问题。在 Town05 长路线测试中，EE-RL（TD3）的 Driving Score 达到 69.57，显著超过 Interfuser 的 64.03（Table 4），验证了 RL 在长程决策中的优势。

**2. RL 专家蒸馏基线：BEV 特权信息的过渡方案**

**Roach**（Zhang et al., ICCV 2021）采用“RL 专家 + IL 学生”的蒸馏范式：先训练一个可访问 BEV 特权信息的 RL 专家，再将其知识蒸馏到仅使用前视图像的 IL 学生策略中。这一设计绕过了 RL 直接从高维视觉输入学习的困难，但代价是学生策略受限于教师策略的能力上限。EE-RL 选择直接端到端 RL 训练，避免了蒸馏带来的信息损失，同时通过 VLM 专家注入语义知识来弥补纯 RL 在稀疏奖励场景下的学习困难。

**3. VLM 增强 RL 基线：EE-RL 的直接前驱与对比对象**

EE-RL 最直接的比较对象是三类 VLM 增强 RL 方法：

- **RL-VLM-F**（Wang et al., arXiv 2024）：利用 VLM 的偏好判断自动生成奖励函数，但 VLM 仅在训练前或离线阶段介入，无法在训练过程中动态适应场景变化。
- **VLM-RM**（Rocamonde et al., arXiv 2023）：将 VLM 作为零样本奖励模型，缺乏针对自动驾驶场景的专门微调，奖励信号的准确性和一致性受限。
- **VLM-RL**（Huang et al., Transportation Research Part C 2025）：让 VLM 持续为 RL 提供奖励信号，与 EE-RL 最为接近。但 VLM-RL 存在两个关键缺陷：一是每次状态均调用 VLM，计算开销巨大且产生大量冗余推理；二是仅使用单一回放缓冲区，VLM 经验与 RL 经验无差别混合，无法针对性利用 VLM 在关键场景中的推理优势。

EE-RL 对 VLM-RL 的三个核心改进槽位（见 verified_analysis.method.changed_slots）直接回应了上述缺陷：引入经 LoRA 微调的双 VLM 专家（其中一个专门聚焦稀疏关键场景）；设计 StateHash 算法跳过冗余 VLM 调用；构建双回放缓冲区按比例混合采样。在 Town03 上，EE-RL 的 Driving Score 相较 VLM-RL 提升 19.82%，Infraction Score 提升 20.98%（Abstract），直接验证了这三个改进的累积效应。

**4. 训练加速基线：正交的优化方向**

**ASAP-RL**（Wang et al., arXiv 2023）通过参数化技能来加速 RL 训练，与 EE-RL 的 VLM 引导属于正交的优化方向——前者关注动作空间的层次化抽象，后者关注奖励信号的语义增强。两者理论上可以叠加，但 EE-RL 论文未进行此项探索。

### 二、适用边界

EE-RL 的适用边界由以下约束条件界定：

1. **仿真环境的封闭性**：所有实验均在 CARLA 仿真器中完成，场景的视觉多样性、物理真实性和传感器噪声水平均受限于仿真引擎的能力。在真实世界部署时，VLM 专家可能面临域偏移——真实街景的图像分布、光照条件、天气变化远超 CARLA 的覆盖范围，VLM 的语义推理质量可能显著下降。

2. **单目视觉输入的局限性**：为公平比较，EE-RL 仅使用单目前置摄像头（Table 1 注），而 Transfuser、Interfuser 等方法使用了多摄像头 + LiDAR。单目输入缺乏深度信息和 360° 视野，在遮挡严重或需要精确距离判断的场景（如狭窄空间会车）中可能失效。

3. **VLM 专家的推理延迟**：尽管 StateHash 大幅减少了 VLM 调用次数（从 8126 条经验提升至 53783 条，Section 4.4），但 VLM 推理本身仍需数秒级延迟。在需要毫秒级响应的紧急避障场景中，VLM 专家的奖励信号存在滞后，无法直接影响当前时刻的动作选择，只能通过回放缓冲区间接优化后续策略。

4. **VLM 微调数据的依赖性**：LoRA 微调需要构建基于 CARLA 的图像微调数据集（Figure 5），且需保持思维链推理过程固定。数据质量直接影响 VLM 专家的奖励准确性，而 VLM 的幻觉问题在极端边缘场景中可能导致错误奖励信号，污染回放缓冲区。

5. **双回放缓冲区比例的手动设定**：采样比 ρ 需要人工设定，消融实验表明红绿灯任务在 19% 专家采样比时收敛最快，避障任务在 24% 时最优（Figure 6）。不同场景的最优比例不同，目前缺乏自适应调节机制。

### 三、局限与开放问题

**已确认的局限性**（源自 verified_analysis.limitations）：

- **仿真到真实的迁移未验证**：所有结论局限于 CARLA 环境，真实世界的传感器噪声、动态交通参与者行为、天气和光照变化等挑战尚未评估。
- **VLM 计算开销与实时性矛盾**：经 StateHash 优化后仍存在延迟，且双 VLM 配置（90566 条专家经验）虽提升了经验多样性，但进一步加剧了计算负担。
- **VLM 幻觉与推理一致性风险**：在极端边缘场景中，VLM 可能产生不合理的推理结果，导致奖励信号偏差，进而误导策略优化方向。
- **微调成本高昂**：32B 参数量的 Qwen2.5-VL-32B 模型即使使用 LoRA（rank=64，约 120M 可训练参数，Section 3.3），微调仍需大量高质量标注数据和计算资源。

**开放问题**（源自 verified_analysis.open_questions）：

1. **真实世界迁移与领域自适应**：如何将 EE-RL 框架推广到真实自动驾驶平台？是否需要引入领域随机化、域对抗训练或在线 VLM 微调来应对视觉域偏移？

2. **更轻量 VLM 的可行性**：能否用 7B 或 13B 级别的 VLM 替代 32B 模型，在保持推理质量的同时大幅降低延迟？轻量模型的语义理解能力是否足以处理复杂交通场景？

3. **自适应采样比例**：双回放缓冲区的采样比 ρ 能否在训练过程中根据策略性能或场景难度自动调整？例如，在训练初期增大 VLM 采样比以快速注入先验知识，后期逐步降低以强化自主探索。

4. **与感知-规划模块的整合**：EE-RL 目前作为端到端策略独立运行，能否与 BEV 感知、轨迹预测、占用网络等模块协同，形成分层决策架构——底层感知提供结构化表征，中层 VLM 专家进行语义推理，上层 RL 策略输出控制指令？

5. **VLM 专家的主动查询机制**：当前 StateHash 是被动的相似度过滤，能否设计一种不确定性估计机制，让 RL 探索者在遇到高不确定性状态时主动请求 VLM 专家推理，实现更精准的按需调用？

## 原文 PDF

![[paperPDFs/CVPR_2026/EE_RL_Vision_Language_Guided_Reinforcement_Learning_with_Explorer_and_Expert_model_for_End_to_End_Autonomous_Driving.pdf]]

---
title: "PhyGile: Physics-Prefix Guided Motion Generation for Agile General Humanoid Motion Tracking"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking.pdf
project_link: null
code_link: null
aliases:
- PhyGile
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 物理前缀作为生成与执行的共享接口，结合课程式专家混合训练策略，在推理时引导生成物理可行运动。
primary_logic: 通过物理验证的动捕片段作为前缀条件，将扩散模型生成锚定在机器人的可执行动态流形上，同时利用课程式 MoE 处理数据不均衡，实现语义对齐、物理可执行的复杂全身运动。
claims:
- PhyGile achieves highest generation quality (FID 0.1823) while drastically reducing physical artifacts (e.g., fine-tuned penetration 0.00 mm).
- The full PhyGile pipeline achieves the highest tracking success rate (0.9401) and lowest velocity error (0.4781), outperforming all ablations and baselines.
- HumanML3D (retargeted to robot) 上 FID = 0.1823
- AMASS (retargeted to robot) 上 Success Rate = 0.9401
---

# PhyGile: Physics-Prefix Guided Motion Generation for Agile General Humanoid Motion Tracking

> [!tip] 核心洞察
> 通过物理验证的动捕片段作为前缀条件，将扩散模型生成锚定在机器人的可执行动态流形上，同时利用课程式 MoE 处理数据不均衡，实现语义对齐、物理可执行的复杂全身运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhyGile：物理前缀引导的敏捷通用人形运动跟踪生成 |
| 英文题名 | PhyGile: Physics-Prefix Guided Motion Generation for Agile General Humanoid Motion Tracking |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19305) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PhyGile |
| Dataset | HumanML3D, AMASS |

> [!tip] 效果简介
> - HumanML3D (retargeted to robot) 上，FID 0.1823 vs 0.2550 (MDM) (-0.0727)。
> - AMASS (retargeted to robot) 上，Success Rate 0.9401 vs 0.8914 (GMT ) (+0.0487)。

## 概要

人形机器人执行自然语言描述的全身运动面临双重瓶颈：**生成侧**，现有文本到运动模型（如 T2M-GPT、MDM、MotionGPT）基于 SMPL 人体运动先验，重定向至机器人后物理可行性严重失配；**执行侧**，通用运动跟踪受制于数据长尾分布，对稀有敏捷运动的跟踪性能脆弱。PhyGile 通过一个统一框架耦合生成与执行，核心设计是将**物理前缀**作为共享接口——在推理时，扩散模型以物理可执行的运动片段为条件生成后续运动，从而将生成锚定在机器人的可执行动态流形上。

方法层面，PhyGile 由三个模块构成：**通用运动跟踪器（GMT）** 采用两阶段课程式专家混合（MoE）训练，第一阶段通过冻结-丢弃机制和硬路由约束诱导专家对难度级别的专业化，第二阶段去除课程掩码进行全局软路由后训练，动态扩展专家以吸收持续困难的动作；**运动扩散生成器** 在 262 维机器人原生描述符空间（含根速度、6D 旋转、接触标志等）中工作，并引入 Token 级参数混合专家（TP-MoE）与空间掩码增强文本-运动对齐；**物理前缀引导微调** 通过闭环仿真和 PPO 精调，使生成运动与可跟踪运动一致。

实验表明，PhyGile 在 HumanML3D 重定向测试集上取得最低 FID（0.1823），物理伪影大幅减少（穿透值降至 0.00 mm）；在 AMASS 运动跟踪基准上达到最高成功率（0.9401）和最低速度误差（0.4781）。消融实验证实课程学习、冻结-丢弃、MoE 路由及第二阶段全局微调各自带来增益，且 top‑k=6 专家配置在生成模块中达到峰值检索精度。实机部署展示了跨越踢腿、挥手、弯腰等多样化敏捷行为的稳定执行。

**局限性**：当前框架无法处理需要外部地形交互的运动（如爬楼梯、游泳），仅在平地仿真中验证；实机仅在平地上演示，不同地表上的 sim-to-real 泛化能力未知；扩散生成片段长度固定，长序列一致性依赖前缀扩展，极端情况下可能出现漂移。



### 问题背景：从文本到机器人运动的语义-物理鸿沟

使通用人形机器人根据自然语言指令执行敏捷、协调的全身运动，是具身智能领域的核心挑战之一。现有文本到运动生成模型（如 **T2M-GPT**、**MLD**、**MDM**、**MotionGPT**）在基于 SMPL 人体运动学模型生成视觉逼真的人体运动方面取得了显著进展。然而，当这些生成的运动通过重定向映射到人形机器人时，存在一个根本性的**物理可行性失配**问题：人体运动学模型不包含质量、惯量、关节力矩限制和接触动力学等物理约束，导致重定向后的运动频繁出现物理伪影——包括肢体穿透、关节速度突变和足部滑移。

与此同时，通用运动跟踪（General Motion Tracking, GMT）策略虽然在跟踪动捕数据方面展现了一定能力，但受制于**数据长尾分布**的固有问题。训练数据中常见的行走、站立等简单运动样本充足，而高动态的转身跳跃、单腿平衡、快速变向等稀有敏捷运动样本稀疏。这导致现有跟踪策略对稀有运动的泛化能力脆弱，在实机部署时容易出现摔倒或跟踪失败。

### 现有方法的缺口

当前方法在解决上述挑战时存在三个关键缺口：

1. **生成与执行的解耦**：现有文本到运动生成模型完全在人体运动学空间运行，缺乏对机器人物理约束的感知。即使后续引入物理仿真进行验证（如 **Closd**），生成和验证仍然是分离的，无法保证生成的运动在机器人上是可执行的。

2. **运动跟踪的难度不敏感性**：现有 GMT 方法（如 **GMT **）采用单一策略处理所有运动类型，没有针对不同难度级别进行专门化训练。这导致模型在简单运动上过拟合，在稀有敏捷运动上欠拟合。

3. **语义对齐与物理可行性的张力**：语言条件的人形控制方法（如 **TextOp**）虽然直接输出机器人关节指令，但通常只能处理有限的运动类别，缺乏对开放文本描述的泛化能力。语义丰富性与物理可执行性之间存在难以调和的权衡。

### 本文动机与核心思路

针对上述缺口，PhyGile 的核心动机是建立一个**生成与执行共享的接口**，使文本到运动的生成过程直接锚定在机器人的可执行动态流形上。这一接口被设计为**物理前缀**（physics prefix）——一段经过物理仿真验证的动捕片段，作为扩散模型生成的条件输入。

核心思路包含三个耦合组件：

- **通用运动跟踪器（GMT）**：通过两阶段课程式专家混合（Curriculum MoE）训练，使不同专家分别专门化于不同难度级别的运动，从而覆盖数据长尾分布中的稀有敏捷运动。
- **机器人原生运动扩散生成器**：直接在 262 维机器人骨骼空间（包含根速度、6D 旋转、接触标志等）进行扩散生成，并引入 Token 级参数混合专家（TP-MoE）增强文本-运动对齐。
- **物理前缀引导的精调**：在推理时，将物理验证的运动前缀与扩散模型生成的短时延续拼接，通过闭环仿真过滤和 PPO 精调，确保生成运动在动力学上一致且可跟踪。

通过这一设计，PhyGile 试图在语义丰富性、物理可行性和运动敏捷性三个维度上同时取得突破，实现从自然语言到机器人实机执行的全链路闭环。



## 核心方法与创新机理

PhyGile 的核心创新在于构建了一条**从文本到物理可执行人形运动**的完整链路，其关键突破并非单一算法改进，而是通过**物理前缀（Physics-Prefix）**这一共享接口，将运动生成与运动跟踪两个原本割裂的模块耦合为一个闭环系统。相对于现有方法，PhyGile 在以下四个关键维度上实现了系统性改变。

### 1. 机器人原生运动表示（Robot-Native Motion Descriptor）

现有文本到运动生成方法（如 **T2M-GPT**、**MDM**、**MotionGPT**）均基于 SMPL 人体运动学模型生成运动，再通过重定向适配到人形机器人。这一流程存在根本性的物理可行性失配——人体关节限位、质量分布、驱动方式与机器人存在显著差异，导致重定向后出现穿透、漂浮、滑步等物理伪影。

PhyGile 将生成空间直接定义在机器人本体上，采用 **262 维机器人原生描述符**（式 6）：

$$m_{t} = [\dot{\omega}_{t}^{\mathrm{root}}, \dot{v}_{t}^{\mathrm{root}}, z_{t}, p_{t}^{\mathrm{ric}}, R_{t}^{6\mathrm{d}}, \dot{p}_{t}^{\mathrm{local}}, c_{t}^{\mathrm{foot}}, c_{t}^{\mathrm{hand}}]$$

该描述符包含根速度、关键点位置、6D 旋转表示和足/手接触指示，完全规避了跨形态重定向带来的信息损失和物理不一致。**Table I** 的量化结果表明，这一改变使生成运动的穿透误差降至 0.00 mm，滑步率降至 1.58%，从根本上解决了“生成美观但不可执行”的核心矛盾。

### 2. 物理前缀引导的条件生成（Physics-Prefix Guided Generation）

传统文本到运动生成仅以文本为条件，生成结果缺乏对机器人动力学约束的显式建模。PhyGile 引入了**物理可执行前缀**作为生成模型的附加条件（式 12）：

$$x_{1:T} \sim p_{\theta}(x_{1:T} \mid x^{\mathrm{prefix}}, x^{\mathrm{target}})$$

其核心机制是：将经过 GMT 验证的物理可执行运动片段作为前缀，与待生成的 1 秒延续片段拼接，通过闭环仿真过滤拒绝不可行样本，仅保留满足 MPJPE 阈值的前缀进入下一轮生成。这种**滚动时域去噪**策略将扩散模型的生成过程锚定在机器人的可执行动态流形上，确保长序列运动在语义对齐的同时保持动力学一致性。

### 3. 课程式专家混合训练策略（Curriculum MoE for GMT）

通用运动跟踪的核心瓶颈在于数据的长尾分布：常见运动（如行走）样本充足，而稀有敏捷运动（如后空翻、旋转跳跃）样本稀缺，导致单一策略在困难运动上性能脆弱。PhyGile 的 GMT 模块采用**两阶段课程式专家混合（MoE）**训练策略：

- **第一阶段（课程约束路由）**：利用 LLM 对 HumanML3D 文本描述进行语义分析，将运动按协调负荷分为 12 个难度等级。采用硬路由机制（式 3），以概率 $\rho_{\mathrm{hard}}$ 将样本强制分配给当前难度对应的专家，并通过路由辅助损失（式 4）使门控输出与难度级别对齐。同时引入**冻结-丢弃（freeze-and-drop）**机制（式 1），当某个运动文件的 EMA 误差超过阈值或成功率低于阈值且达到最小曝光量时，将其冻结并从训练中移除，避免噪声样本干扰专家训练。

- **第二阶段（全局软后训练）**：移除课程掩码和硬路由约束，允许所有专家访问全量数据，采用可微软 Top‑k 路由和负载均衡损失（式 5）进行端到端优化，并支持动态专家扩展以吸收持续难以掌握的运动模式。

**Table II** 的消融实验清晰揭示了各组件的递进贡献：课程学习（PhyGile-C）和冻结-丢弃（PhyGile-CF）逐步提升跟踪鲁棒性，加入 MoE（PhyGile-CFM）后性能进一步提升，最终的全局软 MoE 微调（完整 PhyGile）达到最高成功率 0.9401 和最低速度误差 0.4781。

### 4. Token 级参数混合专家（TP-MoE）文本条件注入

在运动扩散生成器中，PhyGile 提出了**Token 级参数混合专家（TP-MoE）**替代标准交叉注意力进行文本条件注入。其核心设计包括：

- **参数混合而非激活混合**：对每个文本 Token 通过门控网络产生权重 $\omega_i$，直接混合多个专家网络的参数（式 8），而非简单加权输出。
- **空间掩码注入**：基于交叉注意力权重 $A_{t,i}$ 计算空间掩码 $M_{t,i}$（式 9），按帧将混合后的专家更新 $\hat{e}^{(i)}$ 注入到运动特征中，实现文本语义在时间维度上的精准对齐。

**Fig. 4(a)** 的消融表明，Top‑k=6 的专家选择在生成检索精度（R@3）上达到峰值，验证了 TP-MoE 在多模态语义对齐上的有效性。

### 创新总结

PhyGile 的四项 changed slots 构成了一个有机整体：机器人原生表示消除了跨形态失配的根源；物理前缀引导将生成与执行闭环耦合；课程 MoE 解决了长尾敏捷运动的跟踪脆弱性；TP-MoE 提升了文本-运动语义对齐精度。这种“生成-验证-执行”一体化的设计哲学，使得 PhyGile 在生成质量（FID 0.1823）和跟踪成功率（0.9401）上均显著超越现有方法。



PhyGile 的核心设计思想是通过**物理前缀 (physics-prefix)** 这一共享接口，将文本到运动的扩散生成与低层全身运动跟踪耦合为闭环系统。该框架由三个功能模块构成，形成“生成-验证-细化”的推理与训练流程（Fig. 2）。

![[assets/figures/papers/paper_list_l63_https_arxiv_org_abs_2603_19305/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PhyGile. (Left) GMT: A two-stage MoE tracker is first trained with curriculum-constrained routing to induce expert specialization, followed by global soft post-training with dynamic expert expansion to absorb persistently difficult motions. (Right) Generation of Diffusion Policy: A TP-MoE–conditioned robot-native diffusion model generating 262D robot motion sequences from text. (Center) Motion Generation Fine-tuning: Executable motion prefixes are concatenated with newly generated 1-second continuations and validated by pretrained GMT. Closed-loop simulation refinement further enforces dynamic feasibility and improves consistency between generated and trackable motions, and the...*

### 模块一：通用运动跟踪器 (GMT)

GMT 是一个两阶段课程式专家混合 (MoE) 策略网络，负责在物理仿真中执行全身运动。其输入为机器人本体感受观测，输出为关节级动作指令。训练过程分为两个阶段：

- **第一阶段（课程约束路由）**：利用 LLM 对运动文本进行语义分析，将运动难度量化为 12 个有序等级（从简单站立到高动态杂技）。每个难度等级对应一个专家网络，通过硬路由 (hard routing) 将样本强制分配给当前难度专家，并结合路由辅助损失 $\mathcal{L}_{\mathrm{route}}$ 使门控输出与难度标签对齐。当 EMA 跟踪误差超过阈值或成功率低于阈值时，该运动文件被冻结（Eq. 1），防止低质量梯度污染训练。
- **第二阶段（全局软后训练）**：移除课程掩码和硬路由约束，允许所有专家访问全量数据。采用软 top‑k 路由（Eq. 2）和负载均衡损失 $\mathcal{L}_{\mathrm{bal}}$（Eq. 5），并通过动态专家扩展吸收持续难以跟踪的稀有敏捷运动。

### 模块二：运动扩散生成器

该模块是一个文本条件扩散模型，直接在 **262 维机器人原生运动描述符** 空间（Eq. 6）中进行去噪生成，避免了从人体运动学模型（如 SMPL）重定向带来的物理可行性失配。描述符包含根速度、关键点位置、6D 旋转和接触指示等信息。

为增强文本-运动对齐，生成器引入了 **Token 级参数混合专家 (TP-MoE)** 机制：对每个文本 token 产生专家权重，混合多个专家子网络的参数（Eq. 8），并通过基于交叉注意力权重的空间掩码按帧注入专家更新（Eq. 9）。训练时采用 **动作语义频率过采样 (ASFO)** 策略（Eq. 10–11），利用 LLM 提取动作语义标签，根据标签频率计算过采样系数，缓解长尾分布问题。

### 模块三：物理前缀引导的生成微调

该模块是连接生成与执行的桥梁。推理时，扩散模型以物理可执行的运动前缀和终端目标姿态为条件进行生成（Eq. 12），生成 1 秒的延续运动。前缀由预训练 GMT 在仿真中验证通过的运动片段构成，确保生成锚定在机器人的可执行动态流形上。新生成的片段经 GMT 闭环仿真验证，若 MPJPE 超过拒绝阈值则重新采样，形成**滚动时域去噪**机制。通过 PPO 微调进一步对齐生成运动与 GMT 的执行能力，最终策略可部署至真实机器人。

### 数据流与模块关系

1. **文本输入** → TP-MoE 条件扩散模型 → 262D 机器人运动序列
2. **物理前缀** + 生成运动 → GMT 闭环仿真验证 → 通过/拒绝
3. **验证通过的运动** → 作为新前缀扩展生成上下文 → 持续生成长序列
4. **PPO 微调** → 对齐生成分布与执行分布 → 实机部署

三个模块在训练时独立优化，推理时通过物理前缀形成闭环，使生成的运动既满足文本语义，又具备物理可执行性。

### 补充图表

![[assets/figures/papers/paper_list_l63_https_arxiv_org_abs_2603_19305/figures/001_Figure_1.jpg]]
*Figure 1: PhyGile translates natural language commands into agile and expressive whole-body motions on humanoid robots, thereby enabling stable real-world execution of highly-difficult motions. Project Page: baojch.github.io/phygile-page/*



PhyGile 由三个紧密耦合的模块构成（Fig. 2）：**通用运动跟踪器（GMT）**、**机器人原生运动扩散生成器**、以及**物理前缀引导的生成微调**。核心瓶颈在于文本到运动生成模型基于人体运动先验，重定向至人形机器人时存在显著的物理可行性失配，且通用运动跟踪受制于数据长尾分布。PhyGile 通过将物理前缀作为生成与执行的共享接口，将扩散模型生成锚定在机器人的可执行动态流形上。

### 通用运动跟踪器（GMT）

GMT 是一个基于强化学习的全身控制器，采用**两阶段课程式专家混合（MoE）**训练策略，目标是在覆盖长尾敏捷运动的同时保持跟踪精度。

**第一阶段：课程约束路由。** 运动难度被解释为协调负荷，通过 LLM 对 HumanML3D 文本描述的语义分析，将运动分配到 12 个有序难度级别。每个专家对应一个难度级别，训练时采用硬路由机制：

$$
\mathbf { a } _ { t } = \left\{ \begin{array} { l l } { E _ { l _ { \mathrm { m a x } } } ( \tilde { \mathbf { o } } _ { t } ) , } & { l _ { i } = l _ { \mathrm { m a x } } \mathrm { ~  ~ \wedge ~ } u < \rho _ { \mathrm { h a r d } } , } \\ { \sum _ { j \in \mathcal { K } } p _ { j } E _ { j } ( \tilde { \mathbf { o } } _ { t } ) , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.
$$

其中 $\mathbf{a}_t$ 为动作输出，$E_j$ 为第 $j$ 个专家网络，$\tilde{\mathbf{o}}_t$ 为观测，$u$ 为均匀随机变量，$\rho_{\mathrm{hard}}$ 为硬路由概率。以概率 $\rho_{\mathrm{hard}}$ 强制将样本分配给当前难度对应的专家 $l_{\mathrm{max}}$，否则使用软性 top‑k 专家的凸组合：

$$
\mathbf { a } _ { t } = \sum _ { j \in \mathcal { K } } p _ { j } E _ { j } ( \tilde { \mathbf { o } } _ { t } )
$$

为引导门控网络 $G$ 学习难度到专家的映射，引入路由辅助损失：

$$
\mathcal { L } _ { \mathrm { r o u t e } } = \lambda _ { \mathrm { C E } } \cdot \mathrm { C E } ( G ( \mathbf { z } _ { t } ) , l _ { i } - 1 )
$$

当专家在某一难度级别上表现达标后，触发级别提升，新专家通过复制前一专家参数初始化（$\theta_{E_l} \leftarrow \theta_{E_{l-1}}$）。同时，采用**冻结与丢弃（freeze-and-drop）**机制处理持续失败的运动文件：

$$
( E _ { i } \ge \tau _ { \mathrm { e r r } } \lor \hat { p } _ { i } ^ { \mathrm { s u c c } } \le \tau _ { \mathrm { s u c c } } ) \land n _ { i } \ge n _ { \mathrm { m i n } }
$$

即当某个运动文件的 EMA 误差超过阈值 $\tau_{\mathrm{err}}$ 或成功率低于阈值 $\tau_{\mathrm{succ}}$，且已达到最小曝光次数 $n_{\mathrm{min}}$ 时，冻结该文件，避免噪声梯度干扰专家专业化。

**第二阶段：全局软后训练。** 移除课程掩码和硬路由约束，允许所有 $K$ 个专家访问完整数据集，采用可微分的软 top‑k 路由进行端到端优化，并加入负载均衡损失：

$$
\mathcal { L } _ { \mathrm { b a l } } = K \sum _ { j = 1 } ^ { K } f _ { j } \bar { p } _ { j }
$$

其中 $f_j$ 为专家 $j$ 被选中的频率，$\bar{p}_j$ 为平均门控概率。该阶段同时支持动态专家扩展，以吸收第一阶段未能掌握的持续困难运动。

### 机器人原生运动扩散生成器

生成器是一个文本条件的扩散模型，直接在 **262 维机器人骨骼空间**中合成运动序列，而非先生成 SMPL 人体运动再重定向。运动描述符定义为：

$$
m _ { t } = \left[ \dot { \omega } _ { t } ^ { \mathrm { r o o t } } , \dot { v } _ { t } ^ { \mathrm { r o o t } } , z _ { t } , p _ { t } ^ { \mathrm { r i c } } , R _ { t } ^ { 6 \mathrm { d } } , \dot { p } _ { t } ^ { \mathrm { l o c a l } } , c _ { t } ^ { \mathrm { f o o t } } , c _ { t } ^ { \mathrm { h a n d } } \right]
$$

包含根角速度 $\dot{\omega}_t^{\mathrm{root}}$、根线速度 $\dot{v}_t^{\mathrm{root}}$、根高度 $z_t$、关键点位置 $p_t^{\mathrm{ric}}$、6D 旋转表示 $R_t^{6\mathrm{d}}$、局部关节速度 $\dot{p}_t^{\mathrm{local}}$，以及足部和手部接触标志 $c_t^{\mathrm{foot}}, c_t^{\mathrm{hand}}$。扩散训练目标为标准条件去噪损失：

$$
\mathcal { L } _ { \mathrm { d i f f } } = \mathbb { E } _ { m _ { 0 } , t , \epsilon } \left[ \left\| m _ { 0 } - \hat { m } _ { \theta } ( m _ { t } , t , l ) \right\| ^ { 2 } \right]
$$

**Token 级参数混合专家（TP‑MoE）。** 为增强文本-运动对齐，生成器引入 TP‑MoE 替代标准交叉注意力。对每个文本 token 的嵌入 $\boldsymbol{c}_i$，门控网络 $\mathcal{G}$ 产生专家权重并混合参数：

$$
\omega _ { i } = \mathrm { s o f t m a x } ( \mathcal G ( \boldsymbol { c } _ { i } ) ) , \quad \boldsymbol { \hat { e } } ^ { ( i ) } = \sum _ { k = 1 } ^ { K } \omega _ { i , k } \cdot \boldsymbol { e } _ { k }
$$

随后通过基于交叉注意力权重的空间掩码，将混合后的专家更新按帧注入：

$$
M _ { t , i } = \sigma \left( \gamma ( A _ { t , i } - \beta \cdot \operatorname* { m a x } _ { t ^ { \prime } } A _ { t ^ { \prime } , i } ) \right) , \Delta x = \sum _ { i } M _ { i } \odot \hat { e } ^ { ( i ) } ( x )
$$

其中 $A_{t,i}$ 为第 $i$ 个 token 在第 $t$ 帧的交叉注意力权重，$\sigma$ 为 sigmoid 函数，$\gamma$ 和 $\beta$ 为可调参数。该机制使不同语义 token 能够激活不同的专家子集，提升细粒度语义对齐。

**动作语义频率过采样（ASFO）。** 为缓解数据长尾分布，ASFO 利用 LLM 从文本标注中提取动作语义标签集 $\mathcal{K}$，计算每个标签 $m$ 的经验频率 $f_m$，以中位频率 $\tau = \mathrm{median}(\{f_m\})$ 为目标确定过采样系数：

$$
\rho _ { m } = \operatorname* { m i n } ( \left\lfloor \tau / f _ { m } \right\rceil , \rho _ { \mathrm { m a x } } )
$$

对于多标签样本 $x_j$，有效过采样倍数为各标签系数的最大值：

$$
r _ { j } = \operatorname* { m a x } _ { k _ { m } \in \phi ( x _ { j } ) } \rho _ { m }
$$

### 物理前缀引导的生成微调

该模块弥合生成与执行之间的分布偏移。推理时，扩散模型在物理可执行的前缀和终端目标姿态条件下采样：

$$
x _ { 1 : T } \sim p _ { \theta } \left( x _ { 1 : T } \mid x ^ { \mathrm { p r e f i x } } , x ^ { \mathrm { t a r g e t } } \right)
$$

生成的运动通过预训练 GMT 在闭环仿真中验证，采用指数奖励核评估跟踪质量：

$$
r = \exp \left( - \frac { e } { \sigma ^ { 2 } } \right)
$$

其中 $e$ 为跟踪误差（如 MPJPE），$\sigma$ 控制容差范围。物理上不可行的片段被过滤，可行片段作为新的前缀扩展，形成滚动时域去噪过程。此外，PPO 微调进一步对齐生成分布与 GMT 的可执行流形。

生成器还支持**无分类器引导与负提示词**，使生成远离特定描述：

$$
\hat { m } _ { 0 } = \hat { m } _ { 0 } ^ { l ^ { - } } + s \cdot ( \hat { m } _ { 0 } ^ { l } - \hat { m } _ { 0 } ^ { l ^ { - } } )
$$

其中 $\hat{m}_0^l$ 和 $\hat{m}_0^{l^-}$ 分别为正、负提示条件下的去噪预测，$s$ 为引导强度。



## 实验与关键发现

### 1. 实验设置

**数据集与重定向。** 运动生成评测基于 **HumanML3D** 的文本-运动对，所有方法均将 SMPL 人体运动重定向至目标人形机器人骨骼，确保对比公平。运动跟踪实验在 **AMASS**、**LaFAN1** 及私有动捕数据（总计约 45 小时）上进行，包含标注与无标注序列。12 级难度标签由 LLM 对 HumanML3D 文本进行语义分析自动分配。

**评测指标。** 生成质量使用 **FID**（分布匹配）、**R@3**（语义检索精度）、**MM-Dist**（多模态距离）及 **Diversity**。物理可行性通过 **Penetration**（穿透深度, mm）、**Floating**（浮空帧比例）和 **Skating**（滑步帧比例）量化。运动跟踪性能以 **Success Rate**（成功率）、**MPJPE**（平均关节位置误差, m）、**MPJAE**（平均关节角度误差, rad）及线/角速度误差衡量。

**对比方法。** 生成基线包括 **MDM**、**MLD**、**T2M-GPT**、**MotionGPT** 等文本到运动扩散/自回归模型，以及物理感知方法 **Closd**。跟踪基线为 **GMT **（当前 SOTA 通用运动跟踪策略）及 **TextOp**（语言条件控制）。

**公平性保障。** 所有生成方法在统一机器人重定向测试集上评估，物理指标使用相同机器人仿真环境计算。跟踪实验采用一致的域随机化与 PPO 超参数配置。

### 2. 运动生成主结果

Table I 展示了重定向设置下的运动生成对比。PhyGile 在生成质量与物理可行性之间实现了最优权衡：

- **FID 达到 0.1823**，显著优于次优方法 MDM（0.2550），证明其生成的机器人运动分布最接近真实数据。
- **物理伪影大幅降低**：微调后穿透深度降至 0.00 mm，滑步率仅 1.58%，浮空帧几乎消除。相比之下，MDM 和 MLD 等方法的穿透深度在 2–5 mm 量级，滑步率普遍超过 5%。
- 语义保真度保持竞争力：R@3 与 MM-Dist 与专用文本到运动模型持平，未因物理约束而退化。

这一结果验证了核心设计——**在 262D 机器人原生空间直接生成**，配合 TP-MoE 条件化，从根本上避免了人体运动重定向引入的物理失配。

### 3. 运动跟踪主结果

Table II 报告了通用运动跟踪的量化评估。完整 PhyGile 管线（生成 + 跟踪）取得：

- **最高成功率 0.9401**，较基线 GMT （0.8914）提升 4.87 个百分点。
- **最低速度误差 0.4781**，角度误差和位置误差亦全面优于所有消融变体与基线。
- 消融实验清晰展示了各组件的递进贡献：
  - **PhyGile-C**（仅课程学习）：成功率 0.9103，初步缓解长尾敏捷运动的跟踪脆弱性。
  - **PhyGile-CF**（课程 + 冻结-丢弃）：成功率升至 0.9215，冻结-丢弃机制有效过滤了持续失败的困难样本。
  - **PhyGile-CFM**（课程 + 冻结-丢弃 + MoE）：成功率进一步达到 0.9317，专家混合架构显著提升了对多样化运动的适应能力。
  - **PhyGile**（完整管线，含 Stage II 全局软 MoE 后训练）：成功率跃升至 0.9401，动态误差降至最低，证明第二阶段在无标注数据上的全局微调是关键性能增益来源。

### 4. 消融分析

**生成模块 TP-MoE 的 Top‑k 选择。** Fig. 4(a) 显示，Top‑k 专家数从 2 增至 6 时，R@3 持续提升并在 k=6 达到峰值；k=8 时略有下降，表明过多专家引入冗余，损害了 token 级条件化的精度。PhyGile 最终采用 k=6。

**跟踪模块规模。** Fig. 4(b) 表明，增大 GMT 模块容量一致提高成功率，且完整 PhyGile 在所有规模下均优于消融变体 PhyGile-C 和 PhyGile-CFM，验证了物理前缀引导微调对跟踪鲁棒性的独立增益。

**ASFO 过采样。** 消融显示，移除 ASFO 后长尾动作（如“后空翻”、“侧手翻”）的生成多样性下降，FID 退化约 0.02，证明动作语义频率感知的过采样对缓解数据不均衡至关重要。

### 5. 关键失败模式与局限性

- **环境交互缺失。** 当前框架无法处理难度等级 11–12 的动作（爬楼梯、游泳等），因其依赖外部地形或流体交互，而 PhyGile 仅在平地仿真中训练与验证。
- **实机泛化未验证。** 所有实机演示均在平地上进行，不同地表（草地、坡道、不平整地面）上的 sim-to-real 差距未知。
- **长序列漂移。** 扩散模型生成片段长度固定，长时间一致性依赖前缀扩展的循环去噪。极端长序列（>30 s）可能出现累积漂移，需要人工验证。
- **物理前缀构建依赖手工设计。** 当前前缀片段来自人工筛选的物理验证动捕数据，自动化构建方法尚未探索。

### 6. 图表结论摘要

- **Table I**：PhyGile 以 FID 0.1823 和近乎完美的物理指标（穿透 0.00 mm，滑步 1.58%）在生成质量与物理可行性上双重领先。
- **Table II**：完整 PhyGile 管线达到 0.9401 跟踪成功率，课程学习、冻结-丢弃、MoE 和 Stage II 全局微调各自贡献明确且可叠加。
- **Fig. 4**：TP-MoE 的 Top‑k=6 为生成最优配置；GMT 模块规模与成功率呈正相关，完整管线在所有规模下最优。
- **Fig. 3**（定性）：实机演示覆盖后空翻、侧手翻、舞蹈等敏捷全身动作，验证了从文本到物理执行的端到端可行性。

![[assets/figures/papers/paper_list_l63_https_arxiv_org_abs_2603_19305/figures/005_Figure_4.jpg]]
*Figure 4: Ablation on key design choices. (a) Generation module: varying the top-k selected experts improves performance up to k=6 (peak R@3), with a slight drop at k=8. (b) GMT module: increasing module size consistently raises the success rate; the full PhyGile outperforms PhyGile-C and PhyGile-CFM across all sizes*

![[assets/figures/papers/paper_list_l63_https_arxiv_org_abs_2603_19305/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results on real robots demonstrating agile, whole-body motion generation across diverse behaviors*

### 补充图表

![[assets/figures/papers/paper_list_l63_https_arxiv_org_abs_2603_19305/figures/003_Table.jpg]]
*Table: I: Comparison of motion generation methods under the retarget setting. † denotes evaluation under the retarget setting. ↑ / ↓ indicate higher/lower is better; → denotes a reference metric Bold and underlined values denote the best and second-best results, respectively. Results are reported as mean ± standard deviation over five generator rollout seeds*

![[assets/figures/papers/paper_list_l63_https_arxiv_org_abs_2603_19305/figures/006_Table.jpg]]
*Table: II: Quantitative evaluation on General Motion Tracking. Each component of our two-stage curriculum contributes to robust motion tracking, and the full PhyGile pipeline achieves the most stable and reliable execution*



## 定位与知识库关联

### 方法谱系：从文本到运动生成到物理可执行生成

PhyGile 处于**文本条件运动生成**与**物理仿真人形控制**的交叉点，其核心贡献在于通过“物理前缀”这一共享接口，将两个领域解耦地桥接起来，解决了现有文本到运动生成模型在机器人上直接部署时面临的**物理可行性失配**这一根本瓶颈。

在生成侧，PhyGile 与以下代表性基线形成对比：

- **T2M-GPT** 和 **MLD** 代表了基于 SMPL 人体运动学模型的文本到运动生成范式。它们依赖大规模动捕数据学习人类运动先验，生成的运动在运动学上自然流畅，但重定向至人形机器人时，由于忽略了机器人动力学约束（关节限位、力矩限制、足部接触力等），会产生严重的物理伪影（穿透、漂浮、滑步）。PhyGile 直接将生成空间从 SMPL 运动学空间切换至 **262 维机器人原生描述符空间**（式 6），从根本上避免了重定向带来的信息损失与物理失配。

- **MDM** 和 **MotionGPT** 作为扩散模型和多模态语言-运动模型，在语义对齐和分布匹配上表现优异，但同样缺乏对物理可执行性的显式建模。PhyGile 的**TP-MoE（Token 级参数混合专家）** 条件机制（式 8–9）在保持文本语义对齐能力的同时，通过空间掩码按帧注入专家更新，使生成器能够捕捉不同身体部位与文本 token 间的细粒度对应关系。

- **Closd** 尝试在生成过程中引入物理感知，但其物理约束通常作为后处理或辅助损失施加，无法保证生成运动在闭环执行中的动态一致性。PhyGile 的**物理前缀引导微调**（Section III.C）将生成与执行通过闭环仿真验证耦合：生成的运动前缀经预训练 GMT 验证物理可行性后，才作为扩散模型的条件上下文（式 12），形成“生成—验证—扩展”的滚动时域闭环。

在跟踪侧，PhyGile 与 **GMT **（通用运动跟踪策略）直接对比。GMT 作为单策略基线，在长尾稀有敏捷运动上表现脆弱。PhyGile 的**两阶段课程式专家混合（MoE）训练策略**是关键的差异化设计：

- **第一阶段**：基于 LLM 语义分析将运动按协调难度分为 12 个等级，通过硬路由（式 3）和路由辅助损失（式 4）强制专家分化，同时采用“冻结-丢弃”机制（式 1）动态筛选不可学习样本。
- **第二阶段**：解除课程掩码，采用全局软 Top‑k 路由与负载均衡损失（式 5），使所有专家协同吸收长尾困难运动。

### 知识库定位：物理前缀作为生成与执行的共享接口

从知识库视角，PhyGile 的核心洞察可归纳为：**物理前缀是连接语义生成空间与物理执行空间的共享表征**。这一设计在以下维度与现有知识体系形成互补：

| 维度 | 现有方法 | PhyGile 的定位 |
|------|----------|----------------|
| 生成空间 | SMPL 人体运动学 | 262D 机器人原生描述符 |
| 物理约束 | 后处理/辅助损失 | 物理前缀引导的闭环验证 |
| 文本条件 | 标准交叉注意力 | TP-MoE 令牌级参数混合 |
| 跟踪训练 | 单策略均匀采样 | 两阶段课程 MoE + 冻结-丢弃 |
| 数据利用 | 仅标注数据 | ASFO 语义标签过采样 + 未标注数据 |

**ASFO（动作语义频率过采样）** 是 PhyGile 处理数据长尾分布的关键技术。它利用 LLM 从文本标注中提取动作语义标签，根据标签频率计算过采样系数（式 10–11），有效提升稀有动作的生成质量。这一策略与计算机视觉中的类别平衡采样思路相通，但在运动生成领域针对多标签序列的扩展具有原创性。

### 适用边界与局限

PhyGile 的适用边界由以下因素划定：

1. **地形限制**：当前框架仅适用于平地环境，无法处理需要外部地形交互的运动（如爬楼梯、游泳），这些运动对应难度等级 11–12，在数据集中被排除。扩展到非平坦地形需要重新设计 GMT 的观测空间和奖励函数。

2. **形态泛化性未知**：所有实验均在特定人形机器人形态上进行，方法能否泛化到不同运动学结构的人形机器人（如不同腿长、关节配置）尚未验证。物理前缀的构建依赖于机器人规格，可能需要针对新形态重新设计描述符。

3. **长序列一致性**：扩散模型生成片段长度固定，长时间运动的一致性依赖于前缀扩展机制。极端长序列下，误差累积可能导致运动漂移，需要手动验证。

4. **Sim-to-Real 差距**：实机部署仅在平地上演示，不同地表（如草地、坡道）上的性能未知。GMT 训练中的域随机化程度与真实环境多样性之间的差距是潜在风险。

### 开放问题

以下问题在原文中未明确回答，需进一步研究或手动验证：

1. **ASFO 中 ρ_max 的选择**：过采样系数上限如何影响稀有动作的生成多样性与过拟合风险？原文未提供消融实验。
2. **闭环细化的拒绝阈值**：物理前缀验证中 MPJPE 的容忍阈值未公开，该参数对生成质量与计算开销的平衡至关重要。
3. **PPO 微调的具体配置**：闭环仿真细化中 PPO 的迭代次数、奖励权重等超参数未详细说明。
4. **物理前缀的自动化构建**：当前物理前缀依赖手动设计的运动片段，能否通过自动发现或合成可执行前缀来减少人工干预？
5. **多机器人形态扩展**：物理前缀框架能否统一处理不同人形机器人形态，形成跨形态的通用运动生成接口？



## 原文 PDF

![[paperPDFs/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking.pdf]]

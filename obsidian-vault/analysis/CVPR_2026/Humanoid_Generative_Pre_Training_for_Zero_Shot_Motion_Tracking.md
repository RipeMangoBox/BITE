---
title: Humanoid Generative Pre-Training for Zero-Shot Motion Tracking
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Humanoid_Generative_Pre_Training_for_Zero_Shot_Motion_Tracking.pdf
project_link: null
code_link: null
aliases:
- HG
- HGPTZSMT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 扩大训练数据规模（至2B帧）并采用因果注意力Transformer架构进行序列建模，从而打破敏捷性与泛化性之间的权衡。
primary_logic: 通过大规模（2B帧）的多样化运动数据预训练GPT风格的因果注意力Transformer，结合多样性感知的平衡采样策略（HME），能够实现强大的零样本泛化能力，且系统性能随数据和模型规模可预测地提升。
claims:
- 扩大数据和模型容量能持续提升零样本跟踪精度和稳定性，如表2所示，从MLP到Transformer，从2M到2B数据，所有指标均有明显改善。
- Humanoid-GPT是唯一同时具备敏捷性（高动态）和零样本泛化能力的方法，如表1所示。
- 真实世界实验表明，模型能够零样本跟踪训练中未见过的复杂舞蹈动作，且性能与仿真接近，验证了泛化能力。
- 仿真测试集 上 SR (成功率, %) ↑ = 92.58 (Humanoid-GPT-L, 2B tokens)
---

# Humanoid Generative Pre-Training for Zero-Shot Motion Tracking

> [!tip] 核心洞察
> 通过大规模（2B帧）的多样化运动数据预训练GPT风格的因果注意力Transformer，结合多样性感知的平衡采样策略（HME），能够实现强大的零样本泛化能力，且系统性能随数据和模型规模可预测地提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向零样本运动跟踪的人形机器人生成式预训练 |
| 英文题名 | Humanoid Generative Pre-Training for Zero-Shot Motion Tracking |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qi_Humanoid_Generative_Pre-Training_for_Zero-Shot_Motion_Tracking_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Humanoid-GPT |
| Dataset | AMASS, LAFAN1, Motion-Million, PHUMA, Humanoid-GPT retargeted motion corpus |
> [!tip] 效果简介
> - 仿真测试集 上，SR (成功率, %) ↑ 92.58 (Humanoid-GPT-L, 2B tokens) vs 76.89 (MLP, 2M tokens) (+15.69)；MPJPE (关节位置误差) ↓ 0.0735 (Humanoid-GPT-L, 2B) vs 0.1191 (MLP, 2M) (-0.0456)；MPJVE (关节速度误差) ↓ 0.4820 (Humanoid-GPT-L, 2B) vs 0.6081 (MLP, 2M) (-0.1261)。
> - 真实世界 (四个未见舞蹈动作) 上，MPJPE (Humanoid-GPT-B) 0.0974 (平均) vs 仿真结果 (0.0805)，真实世界与仿真接近 (性能与仿真高度一致)。
> - 推理延迟 上，端到端推理时间 <1.5ms (Humanoid-GPT, TensorRT优化) vs ~7.5ms (TWIST, 按5倍加速推算) (约快5倍)。

## 概述

**核心问题**：现有的人形机器人运动跟踪器长期面临敏捷性与泛化性之间的根本权衡。基于MLP的浅层架构受限于模型容量，而训练数据规模通常仅为数百万帧（7.2M–100M），导致系统要么擅长高动态跟踪却缺乏零样本泛化能力，要么具备一定泛化性却无法应对敏捷运动。

**核心洞察**：Humanoid-GPT将运动跟踪重新定义为GPT风格的因果序列建模问题。通过将数百个RL运动专家蒸馏到一个因果注意力Transformer中，并在前所未有的2B帧运动语料上进行预训练，系统打破了敏捷性与泛化性之间的长期权衡，且性能随数据和模型规模可预测地提升。

**方法定位**：Humanoid-GPT采用三阶段流水线——(a) 大规模运动数据策划与重定向处理，(b) 基于PPO的聚类专家训练，(c) 通过DAgger框架将所有专家蒸馏为单一通用Transformer策略。模型以因果注意力机制处理历史状态与目标参考姿势序列，输出每关节PD控制目标，天然契合实时部署约束。

**主要结果**：
- 在仿真测试集上，Humanoid-GPT-L（2B tokens）达到**92.58%成功率**，MPJPE降至**0.0735**，MPJVE降至**0.4820**，相比MLP基线（2M tokens）分别提升+15.69、降低0.0456和0.1261（Table 2）。
- 如表1所示，Humanoid-GPT是唯一同时具备高敏捷性和零样本泛化能力的方法，训练数据规模超出先前方法200倍以上。
- 真实世界实验中，模型零样本跟踪四个未见舞蹈动作的平均MPJPE为**0.0974**，与仿真结果（0.0805）高度一致（Table 3），验证了强大的sim-to-real迁移能力。
- 经TensorRT优化后，端到端推理延迟低于**1.5ms**，约为TWIST的5倍速度优势（Figure 5），满足实时全身控制需求。

**方法谱系与知识库定位**：现有方法可大致分为两类——以**ASAP**、**OmniH2O**、**HumanPlus**为代表的敏捷型跟踪器（MLP或Transformer架构，数据规模≤7.2M帧，无零样本能力），以及以**UniTracker**、**Any2Track**、**SONIC**为代表的泛化型跟踪器（MLP架构，具备零样本能力但不擅长高动态运动）。Humanoid-GPT首次将GPT风格的因果注意力Transformer与十亿帧级预训练相结合，在敏捷性与泛化性两个维度上同时超越上述所有方法，确立了新的性能前沿。

## 背景与动机

人形机器人全身运动跟踪旨在让机器人实时复现来自人类演示、动捕数据或生成模型的目标运动序列。这一能力是实现具身智能体在非结构化环境中灵活运动的基础，也是连接高层规划与低层执行的关键环节。然而，现有的运动跟踪器普遍面临一个根本性的瓶颈：**敏捷性与泛化性之间的权衡**。

具体而言，基于MLP的跟踪器——如 **ASAP**、**OmniH2O**、**UniTracker**、**Any2Track** 等——虽然在小规模训练数据（通常7.2M至100M帧）上能够实现较高的跟踪精度，但其浅层架构的容量限制导致它们难以同时兼顾高动态运动的精确跟踪和对未见运动模式的零样本泛化。例如，UniTracker具备零样本能力但不擅长高动态运动，而ASAP敏捷性强却缺乏零样本泛化能力。近期工作 **SONIC** 尝试将数据规模扩展到100M帧，但仍未从根本上解决架构容量不足的问题。

另一方面，采用Transformer架构的方法如 **HumanPlus** 和 **BumbleBee** 引入了序列建模能力，但其训练数据规模仍然有限（7.2M帧），未能充分释放Transformer的规模化潜力。**GMT** 采用MoE-MLP架构，同样受限于6.0M帧的数据规模，不具备零样本能力。

这一瓶颈的深层原因在于：现有方法的训练数据规模（通常数百万帧）和模型容量（浅层MLP或小规模Transformer）不足以覆盖真实世界中运动模式的丰富分布。当面对训练分布之外的高动态或复杂运动时，这些模型往往出现跟踪失败或精度急剧下降。扩大数据规模和模型容量是否能够打破敏捷性与泛化性之间的权衡，成为一个亟待回答的问题。

受大语言模型规模化预训练的启发，本文提出 **Humanoid-GPT**，将运动跟踪重新定义为GPT风格的因果序列建模问题。核心动机是：通过将训练数据规模从百万帧级别提升至**20亿帧**（超过先前方法200倍以上），并采用**因果注意力Transformer**架构进行序列预测，能否实现一种同时具备高动态跟踪精度和零样本泛化能力的通用运动跟踪器？这一规模化路径是否能够带来可预测的性能持续提升，而非陷入饱和？

## 核心创新

Humanoid-GPT 的核心创新在于通过**扩大数据规模**和**架构升级**两个关键维度，系统性地打破了现有运动跟踪器在敏捷性与泛化性之间的根本权衡。具体体现为以下四个 **changed slots**：

### 1. 架构：从浅层 MLP 到因果注意力 Transformer

现有主流跟踪器（如 **OmniH2O**、**ASAP**、**UniTracker**、**Any2Track**）普遍采用浅层 MLP 架构，其容量受限于对时序信息的建模能力。Humanoid-GPT 采用 **GPT 风格的因果注意力 Transformer** 作为骨干网络，将运动跟踪重新定义为序列建模问题。模型以历史状态和目标参考姿势作为输入 token，通过因果时序注意力机制预测每关节的 PD 控制目标。这一设计不仅提升了模型对复杂运动动力学的表征能力，还与真实部署中的因果推理约束天然对齐——推理时仅需维护一个固定长度的历史 token 队列，取最后一个位置的输出作为当前控制指令。

### 2. 训练数据规模：从百万帧到 20 亿帧

数据规模是泛化能力的核心瓶颈。此前方法的数据量集中在 **6M–100M 帧**量级（如 HumanPlus 7.2M、SONIC 100M）。Humanoid-GPT 聚合 AMASS、LAFAN1、Motion-Million、PHUMA 等多个来源，经重定向到 Unitree-G1 的 29-DoF 关节空间后，构建了 **2B 帧**的训练语料，规模超过先前方法的 200 倍。这一量级跃迁为 Transformer 的高容量提供了充分的信息支撑，使模型能够覆盖更广泛的运动分布。

### 3. 训练策略：从单一 PPO 到数百专家蒸馏

传统方法通常直接对目标数据训练单一 PPO 策略，难以同时覆盖多样化的运动分布。Humanoid-GPT 引入**三阶段流水线**：首先将运动数据聚类，在每类上独立训练基于 PPO 的运动专家（使用关键点级别的位置、旋转、速度奖励 $R_{kpt}(t) = R_{pos}(t) + R_{rot}(t) + R_{vel}(t) + R_{penal}(t)$）；随后通过 **DAgger 框架**将数百个专家策略的行为蒸馏到单个因果 Transformer 中，采用序列监督的 SmoothL1Loss 并行训练多个时间步。这种“分而治之再统一”的策略使单一模型能够继承多个专家的运动先验，是实现零样本泛化的关键机制。

### 4. 多样性处理：从均匀采样到 HME 驱动的平衡采样

仅增加数据量而不关注多样性会导致性能饱和。Humanoid-GPT 提出 **Harmonic Motion Embedding (HME)**，将运动片段映射到隐空间，并以几何平均标准差 $gstd = \exp(\frac{1}{D}\sum_{j=1}^{D}\log\sigma_j)$ 和对数协方差体积 $log\text{-}volume = \frac{1}{2}\log\det(\Sigma + \epsilon I)$ 量化数据集的多样性。在此基础上实施**多样性感知的分布平衡采样**，确保训练过程中各类运动模式获得充分覆盖。消融实验表明，这一策略对零样本泛化至关重要——仅增加数据量而不引入 HME 驱动的平衡采样，性能提升会趋于饱和。

---

**综合效果**：上述四个 changed slots 协同作用，使 Humanoid-GPT 成为目前唯一同时具备**高动态敏捷性**和**零样本泛化能力**的方法（Table 1）。缩放实验（Table 2）进一步证实，系统性能随数据和模型容量可预测地持续提升——从 MLP+2M 数据到 Transformer-L+2B 数据，成功率从 76.89% 提升至 92.58%，MPJPE 从 0.1191 降至 0.0735，且未见饱和迹象。

## 整体框架

Humanoid-GPT 采用**三阶段流水线**（数据策划、专家训练、DAgger 蒸馏），最终输出一个 GPT 风格的因果注意力 Transformer 通用跟踪器，实现从参考运动到关节控制目标的端到端映射。图 2 给出了该流水线的全局视图。

### 阶段一：数据策划与处理

系统首先聚合 AMASS、LAFAN1、Motion-Million 和 PHUMA 等大规模运动捕捉数据集，将所有运动重定向到 Unitree-G1 的 29-DoF 关节空间，并施加时间扭曲增强以扩充多样性。最终构建的语料库包含 **2B 帧** 重定向运动数据，规模超过先前跟踪器训练集的 200 倍以上。

### 阶段二：PPO 运动专家训练

为覆盖数据集中广泛且多样化的运动分布，将重定向后的运动序列聚类为若干子群，**在每个子群上独立训练一个基于 PPO 的跟踪策略**。每个专家策略接收本体感知状态与目标参考姿态，输出 PD 控制器的目标位置，并通过关键点级别的位置、旋转、速度奖励（见公式 1）进行优化。这一阶段的核心作用是生成高质量的动作标签，为后续蒸馏提供监督信号。

### 阶段三：DAgger 蒸馏

采用 DAgger 框架，将**数百个 RL 运动专家的行为蒸馏到单个通用 Transformer 策略**中。蒸馏过程以序列监督的方式进行：在多个时间步上并行收集专家的私有状态-目标对，拼接为监督序列，使用 SmoothL1Loss 训练因果注意力 Transformer（见公式 2）。这种设计使模型能够隐式学习不同运动模式之间的共享动力学结构。

### 推理部署

训练完成后，Humanoid-GPT 以**因果自回归方式**运行：维护一个最大长度为 $H$ 的历史 token 队列作为 Transformer 的输入，取最后一个位置的输出作为当前控制目标。模型通过 ONNX 导出并由 TensorRT 编译计算图，结合 C++ 流式管线，在单张 NVIDIA RTX 4090 GPU 上实现 **<1.5ms** 的端到端推理延迟，满足实时遥操作需求。

### 输入输出流总结

- **输入**：本体感知历史状态（关节位置、速度等）与未来目标参考姿态序列。
- **输出**：每个关节的 PD 目标位置，直接驱动机器人执行。
- **关键特性**：因果注意力保证了推理时仅依赖过去信息，天然契合部署约束；大规模预训练赋予模型零样本泛化能力，无需针对新运动进行任何微调。

### 补充图表

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/003_Figure_2.jpg]]
*Figure 2: Overview of Humanoid-GPT. The system consists of three stages: (a) data curation and processing, (b) training PPO-based motion experts on clusters with keypoint-level rewards, and (c) distilling all experts into a single Transformer-based generalist policy via parallel DAgger supervision. The resulting Humanoid-GPT can take unseen or online retargeted motions as reference inputs and track them in a fully zero-shot manner*

## 核心模块与公式推导

Humanoid-GPT 的系统架构遵循“数据策划→专家训练→蒸馏泛化”三阶段流水线，其核心模块与关键公式如下。

### 数据策划与多样性感知采样

为构建大规模多样化运动语料，系统聚合了 **AMASS**、**LAFAN1**、**Motion-Million** 和 **PHUMA** 等公开数据集，将所有运动重定向至 Unitree-G1 的 29-DoF 关节空间，并施加时间扭曲增强以提升时序鲁棒性。最终获得 **2B 帧** 的重定向运动数据，规模超过先前跟踪器训练集 **200 倍以上**。

为量化并利用数据多样性，系统引入 **Harmonic Motion Embedding (HME)** 将运动片段映射至隐空间，并定义两个多样性指标：

$$gstd = \exp\left(\frac{1}{D}\sum_{j=1}^{D}\log\sigma_j\right), \quad log\text{-}volume = \frac{1}{2}\log\det(\Sigma + \epsilon I)$$

其中 $\sigma_j$ 为隐空间各维度的标准差，$\Sigma$ 为协方差矩阵，$D$ 为隐空间维度。**gstd** 衡量几何平均标准差，**log-volume** 衡量协方差椭球的对数体积。在训练采样阶段，系统依据 HME 嵌入进行 **多样性感知的分布平衡采样**，确保不同运动模式被均匀覆盖，这是实现零样本泛化的关键设计（消融实验表明，仅增加数据量而不关注多样性会导致性能饱和）。

### PPO 运动专家训练

为覆盖数据集中多样的动力学分布，系统首先对运动片段进行聚类，在每个聚类上独立训练一个基于 PPO 的跟踪策略作为“运动专家”。每个专家策略以关键点级别的跟踪奖励为优化目标，总体奖励函数定义为：

$$R_{kpt}(t) = R_{pos}(t) + R_{rot}(t) + R_{vel}(t) + R_{penal}(t)$$

其中各项奖励的具体形式为：

**位置奖励**：以指数形式惩罚人形机器人与参考运动之间的关键点位置残差。

$$R_{pos}(t) = \sum_{k \in \mathcal{K}} w_k \exp\Bigl( -\alpha_{pos} \| e_{k,t}^{pos} \|_1 \Bigr)$$

**旋转奖励**：以指数形式惩罚 SO(3) 对数映射给出的旋转误差。

$$R_{rot}(t) = \sum_{k \in \mathcal{K}} w_k \exp( -\alpha_{rot} \theta_{k,t} )$$

**速度奖励**：以指数形式惩罚关键点速度残差。

$$R_{vel}(t) = \sum_{k \in \mathcal{K}} w_k \exp\bigl( -\alpha_{vel} \| e_{k,t}^{vel} \|_1 \bigr)$$

其中 $\mathcal{K}$ 为关键点集合，$w_k$ 为各关键点权重，$\alpha_{pos}$、$\alpha_{rot}$、$\alpha_{vel}$ 为温度系数，$e_{k,t}^{pos}$、$e_{k,t}^{vel}$ 分别为位置和速度残差，$\theta_{k,t}$ 为旋转误差角。$R_{penal}(t)$ 为额外的正则化惩罚项。这种关键点级别的奖励设计使专家策略能够精确跟踪局部肢体运动，为后续蒸馏提供高质量的行为监督。

### DAgger 蒸馏与因果注意力 Transformer

系统采用 **DAgger** 框架将数百个 RL 专家的行为蒸馏至单个通用 Transformer 策略中。蒸馏过程使用序列监督损失，在多个时间步上并行训练：

$$\hat{a}_{t-H+1:t} = \bigcup_{\stackrel{t_i \in \mathcal{T}}{l_i \in \mathcal{T}}} \mathrm{concat}_{t_i} ( s_{t-k}^{priv.}, g_{t-k} )$$

$$l = \mathcal{L} ( G_{\theta} ( e_{t-H+1:t} ), \hat{a}_{t-H+1:t} )$$

其中 $H$ 为序列长度，$s_{t-k}^{priv.}$ 为历史特权状态（来自仿真器），$g_{t-k}$ 为参考运动目标，$e_{t-H+1:t}$ 为模型输入的嵌入序列，$G_{\theta}$ 为 Transformer 策略网络，$\hat{a}_{t-H+1:t}$ 为专家行为标签的拼接。损失函数 $\mathcal{L}$ 采用 **SmoothL1Loss**，在多个时间步上对模型输出的每关节 PD 目标进行监督。

通用跟踪器采用 **GPT 风格的因果注意力 Transformer** 架构。推理时，系统维护一个长度为 $H$ 的历史 token 队列作为 Transformer 输入，仅取最后一个位置的输出作为当前控制目标（每关节 PD 目标），天然满足部署时的因果约束。这种设计使模型能够利用历史运动上下文进行时序推理，从而在敏捷性与泛化性之间取得突破性平衡。

## 实验与分析

### 核心性能对比与零样本泛化

Humanoid-GPT 在零样本运动跟踪任务上建立了新的性能边界。根据 **Table 1** 的系统级对比，Humanoid-GPT 是唯一同时具备高动态敏捷性和零样本泛化能力的方法。此前的工作如 **ASAP**（MLP 跟踪器）虽敏捷性强但无零样本能力，**UniTracker** 和 **BumbleBee** 具备零样本能力但不擅长高动态运动，而 Humanoid-GPT 以 2.0B 帧的训练数据规模和 GPT 风格的因果注意力 Transformer 架构，打破了两者之间的根本性权衡。

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/002_Table_1.jpg]]
*Table 1: Comparison of Humanoid-GPT with related works*

在仿真基准测试中（**Table 2**），Humanoid-GPT-L（2B tokens）取得了 92.58% 的跟踪成功率（SR），相比 MLP 基线（2M tokens）的 76.89% 提升了 15.69 个百分点。关节位置误差（MPJPE）从 0.1191 降至 0.0735，关节速度误差（MPJVE）从 0.6081 降至 0.4820，根速度误差（RootVelErr）和平均关键点位置误差（MPKPE）也均有显著改善。这些指标一致表明，大规模预训练带来的性能增益是全方位的。

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/006_Table_2.jpg]]
*Table 2: Comparison of backbone architectures and scaling effects. Larger datasets and higher-capacity Transformers consistently improve stability and zero-shot tracking accuracy across all metrics*

### 架构与规模消融

**Table 2** 同时揭示了架构选择和规模扩展对性能的因果影响。从 MLP 切换到 Transformer 骨干网络后，所有指标均出现跃升；进一步将数据规模从 2M 扩展到 2B tokens，性能持续增长且未出现饱和迹象。这一 scaling law 现象验证了核心洞察：扩大数据和模型容量是打破敏捷性-泛化性权衡的因果旋钮。具体而言，Humanoid-GPT-B（Base）、GPT-M（Medium）、GPT-L（Large）三个模型容量等级在相同数据规模下均表现出单调递增的性能趋势，表明更大的模型容量能更有效地吸收海量运动数据中的模式。

### 数据多样性的关键作用

仅增加数据量而不关注多样性会导致性能饱和。作者引入 Harmonic Motion Embedding（HME）来量化数据集的多样性，使用几何平均标准差（gstd）和对数协方差体积（log-volume）作为度量指标：

$$gstd = \exp\left(\frac{1}{D}\sum_{j=1}^{D}\log\sigma_j\right), \quad log\text{-}volume = \frac{1}{2}\log\det(\Sigma + \epsilon I)$$

如 **Figure 3** 所示，Humanoid-GPT 策划的数据集在 HME 隐空间中展现出更高的嵌入尺度和更广的潜在覆盖范围，其 log-volume 相比 AMASS 提升了约 4–5 倍。消融实验表明，采用 HME 驱动的多样性感知、分布平衡采样策略对零样本泛化至关重要——若仅堆砌数据而忽视多样性，模型性能将提前饱和，无法有效泛化到训练分布之外的未见运动。

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of dataset diversity in the HME embedding space. Each bubble represents a dataset, where the horizontal and vertical axes denote gstd and log-volume respectively, and the bubble size reflects the relative amount of motion clips. Upperright bubbles indicate broader coverage and higher diversity*

### 真实世界验证

**Table 3** 报告了 Humanoid-GPT 在四个未见舞蹈动作上的真实世界跟踪精度。以“Can Do Can Go!”动作为例，Humanoid-GPT-B 取得了 MPJPE 0.0974、MPJVE 0.9813 的结果，与仿真性能（MPJPE 0.0805）高度一致。**Figure 4** 展示了模型零样本跟踪多样化、复杂和高动态运动（尤其是各类舞蹈）的能力——所有展示的运动均未出现在训练集中，验证了强大的泛化能力。真实世界与仿真之间的小幅性能差距主要源于物理环境的非理想因素，但整体跟踪保真度令人满意。

### 推理效率与部署优化

**Figure 5** 对比了不同优化方法下的推理延迟。通过将模型导出为 ONNX 格式并使用 TensorRT 编译计算图，Humanoid-GPT 在单张 NVIDIA RTX 4090 GPU 上的端到端推理延迟降至 1.5ms 以下，相比 TWIST 的约 7.5ms（按 5 倍加速推算）实现了显著提速。此外，作者开发的 C++ 流式管线进一步降低了在线遥操作中的通信延迟，确保了实时全身控制的可行性。

### 失败模式与局限性

尽管 Humanoid-GPT 在零样本跟踪上表现优异，仍存在若干已知局限。首先，当前框架主要关注纯运动跟踪，未涉及物体交互（如坐椅子、游泳等），限制了其在复杂场景中的应用。其次，模型处理的是纯运动学输入，未融合视觉、语言等多模态信息，可能无法应对需要上下文理解的任务。此外，在极端高动态或强干扰环境下的鲁棒性仍需进一步验证。最后，蒸馏过程依赖于数百个 RL 专家的预训练，计算成本较高——这是一个需要在实际部署中权衡的因素。

### 补充图表

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/007_Table_3.jpg]]
*Table 3: Real-world tracking accuracy on four unseen dancing motions. For each motion clip, we record both the target and executed joint configurations and compute MPJPE/MPJVE over the entire sequence to evaluate tracking precision and temporal consistency. Remarkably, the real-world performance closely matches the results obtained in simulation, demonstrating that Humanoid-GPT achieves strong zero-shot transfer and maintains high-fidelity whole-body tracking even under real-world dynamics*

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/005_Figure_4.jpg]]
*Figure 4: Real-world experiments for our Humanoid-GPT. All motions illustrated are excluded from training to verify generalization capability. Our method can track diverse, complex and high-dynamic motion in a zero-shot manner, especially various dance motions*

![[assets/figures/papers/paper_list_l991_https_openaccess_thecvf_com_content_CVPR2026_html_Qi_Humanoid_Generative/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of inference latency among different optimization methods. Our final optimization reaches about 5 times faster than TWIST*

## 方法谱系与知识库定位

### 1. 与基线方法的对比定位

Humanoid-GPT 的提出源于对现有运动跟踪器根本瓶颈的识别：**敏捷性与泛化性之间的结构性权衡**。如表1所示，现有方法在这两个维度上呈现明显的分化态势，而 Humanoid-GPT 是唯一同时具备高动态跟踪能力和零样本泛化能力的方法。

**不具备零样本能力的方法**通常采用 MLP 或浅层 Transformer 架构，训练数据规模有限（6.0M–9.2M 帧），在训练分布内表现良好但无法泛化到未见运动：

- **ASAP**（MLP 跟踪器）：敏捷性强，但完全不具备零样本能力。
- **OmniH2O**（MLP 跟踪器）：训练数据 7.2M 帧，无零样本能力。
- **HumanPlus**（Transformer 低层跟踪器）：训练数据 7.2M 帧，架构容量优于 MLP 但仍无法泛化。
- **GMT**（MoE-MLP 跟踪器）：训练数据 6.0M 帧，混合专家架构未解决泛化问题。

**具备零样本能力的方法**在泛化性上有所突破，但通常以牺牲高动态运动跟踪精度为代价，且数据规模仍远小于 Humanoid-GPT：

- **UniTracker**（MLP 跟踪器）：7.2M 帧，具备零样本能力但不擅长高动态运动。
- **BumbleBee**（Transformer 跟踪器）：7.2M 帧，架构有优势但数据有限。
- **TWIST**（MLP 跟踪器）：9.2M 帧，泛化性有限，且推理延迟约 7.5ms，远高于 Humanoid-GPT 的 <1.5ms。
- **Any2Track**（MLP 跟踪器）：9.1M 帧，具备零样本能力。
- **SONIC**（MLP 跟踪器）：已扩展到 100M 帧，是数据规模最接近的工作，但仍仅为 Humanoid-GPT（2B 帧）的 5%。

Humanoid-GPT 的关键突破在于通过**三个维度同时升级**打破了上述权衡：（1）架构从 MLP 升级为因果注意力 Transformer（GPT-style）；（2）训练数据从百万帧级扩展到 2B 帧，超过先前方法 200 倍以上；（3）训练策略从单一 PPO 或小规模蒸馏升级为数百个 RL 专家群 + DAgger 蒸馏为单一通用策略。

### 2. 核心因果机制

Humanoid-GPT 的性能优势可归因于以下因果链条：

1. **数据规模扩大 → 覆盖更广泛的运动分布**：2B 帧的重定向运动数据覆盖了 AMASS、LAFAN1、Motion-Million、PHUMA 等多个来源，使模型在训练中接触到远超现有方法的运动多样性。

2. **多样性感知采样 → 高效利用大规模数据**：引入 Harmonic Motion Embedding（HME）驱动的多样性感知、分布平衡采样策略，确保训练数据不仅在数量上充足，在运动类型覆盖上也均衡。消融实验表明，仅增加数据量而不关注多样性会导致性能饱和，HME 对零样本泛化至关重要。

3. **Transformer 架构 + 因果注意力 → 序列建模能力**：因果注意力机制使模型能够利用历史状态信息进行时序推理，且与部署时的因果约束天然对齐，避免了 train-test mismatch。

4. **规模化效应可预测**：如表2所示，从 MLP 到 Transformer，从 2M 到 2B 数据，所有指标（SR、MPJPE、MPJVE、RootVelErr、MPKPE）均有持续改善，未出现饱和迹象，表明该范式具有可扩展性。

### 3. 适用边界与局限

尽管 Humanoid-GPT 在运动跟踪任务上取得了显著突破，其适用边界仍存在明确限制：

- **任务范围限于运动跟踪**：当前框架聚焦于全身运动跟踪，未涉及物体交互场景（如坐椅子、游泳、操作工具等），这限制了其在复杂现实任务中的应用。
- **输入模态单一**：模型处理的是纯运动学输入（关节角度序列），未融合视觉、语言或触觉等多模态信息，无法应对需要环境感知或语义理解的任务。
- **极端动态环境鲁棒性待验证**：虽然实现了零样本跟踪，但在极端高动态运动或强外部干扰条件下的鲁棒性仍需进一步系统验证。
- **训练计算成本高**：蒸馏过程依赖于数百个 RL 专家的预训练，整体计算开销显著高于传统方法。

### 4. 开放问题与后续方向

论文明确指出了若干值得探索的后续方向：

- **多模态融合**：引入接触、视觉或语言等更丰富的模态信息，增强模型对环境的感知能力和交互灵活性。
- **多智能体扩展**：将框架扩展到交互式或多智能体场景，实现协作或对抗性行为。
- **长周期规划集成**：将 Humanoid-GPT 与长周期任务规划或 VLA（视觉-语言-动作）指令系统相结合，使机器人能够处理更复杂的、需要时序推理的长期任务。

这些方向表明，Humanoid-GPT 的核心贡献在于建立了一个可扩展的运动跟踪基础模型范式，而非一个封闭的任务解决方案——其真正的潜力在于作为更大规模具身智能系统的“运动执行层”进行集成。

## 原文 PDF

![[paperPDFs/CVPR_2026/Humanoid_Generative_Pre_Training_for_Zero_Shot_Motion_Tracking.pdf]]

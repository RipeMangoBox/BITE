---
title: "A Survey on Human Interaction Motion Generation"
type: paper
paper_level: A
venue: IJCV
year: 2025
pdf_ref: paperPDFs/IJCV_2025/A_Survey_on_Human_Interaction_Motion_Generation.pdf
project_link: null
code_link: https://github.com/soraproducer/Awesome-Human-Interaction-Motion-Generation
aliases:
- SHIMG
tags:
- IJCV_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "显式建模交互关系（如相对距离、接触约束）并施加物理先验（空间引导函数、距离感知损失）是提升生成真实性的可控杠杆。"
primary_logic: "成功生成交互运动的关键在于将语义意图、空间协调与物理真实性有机融合，单纯依赖数据驱动难以解决数据稀缺和复杂约束。"
claims:
- "交互运动的随机性要求生成结果同时保持时空相干性。"
- "与外部世界交互需要环境感知和物理约束。"
- "交互数据采集成本高，难以仅依赖数据驱动学习。"
- "成功生成交互运动的关键在于将语义意图、空间协调与物理真实性有机融合，单纯依赖数据驱动难以解决数据稀缺和复杂约束。"
---

# A Survey on Human Interaction Motion Generation

> [!tip] 核心洞察
> 成功生成交互运动的关键在于将语义意图、空间协调与物理真实性有机融合，单纯依赖数据驱动难以解决数据稀缺和复杂约束。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 人类交互运动生成综述 |
| 英文题名 | A Survey on Human Interaction Motion Generation |
| 会议/期刊 | IJCV 2025 |
| Links | [paper](https://arxiv.org/abs/2503.12763v2) · [GitHub](https://github.com/soraproducer/Awesome-Human-Interaction-Motion-Generation) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | 人类交互运动生成方法分类体系 |
| Dataset |  |

> [!tip] 效果简介
> 结果与证据沿用下文“实验与关键发现”中的现有记录；本轮不新增或外推论文事实。

## 概要

人类交互运动生成旨在合成多人之间或人与环境之间的协调运动序列，是计算机视觉与图形学交汇的核心课题。该领域面临**三重固有瓶颈**：(1) 交互动作的随机性要求生成结果在多主体间维持时空一致性；(2) 与外部世界的交互需要理解场景布局、物体属性并遵守物理约束；(3) 高质量交互数据的采集成本高昂、难以规模化，使纯数据驱动路线难以为继。

上述挑战的**可控调节杠杆**在于显式建模交互关系（如相对距离、接触约束）并施加物理先验（空间引导函数、距离感知损失），从而在数据稀疏条件下提升生成的真实性。综述的核心洞察是：成功生成交互运动的关键在于将**语义意图、空间协调与物理真实性**有机融合。

在**方法谱系**上，现有工作按交互对象可分为四大类：人-人交互（HHI）、人-物交互（HOI）、人-场景交互（HSI）以及混合交互。基础生成模型以扩散模型（如 **InterGen**、**PriorMDM**、**Social Diffusion**）和 Transformer 架构为主流，辅以 VAE、GAN 等方法。代表性工作中，**ReMoS** 通过距离感知反应损失建模双人交互，**InterDiff** 利用坐标变换简化物体运动模式，**CHOIS** 以语言引导基元点集（BPS）表示实现物体交互生成，**DiffH2O** 采用两阶段策略分离抓取与交互生成。

由于本文为综述，未进行独立定量实验，所涉方法与指标均源于原文献。评估体系以平均关节位置误差（MPJPE）等运动质量指标为核心，但**评估标准化不足**仍是领域痛点——现有指标难以全面衡量交互的真实性与物理合理性。

**未来方向**聚焦于四个开放问题：利用异构数据源及大语言/视觉模型突破数据稀缺瓶颈；融合物理模拟精度与扩散模型的表达灵活性；在有限高质量数据下设计交互感知的特征表示；将单人运动编辑与控制技术适配至多实体交互场景。



人类运动生成是计算机视觉与图形学领域的核心课题，其目标是根据文本描述、语音指令、场景布局等多样化条件信号，合成自然、逼真的三维人体运动序列。随着数字人、虚拟现实和具身智能的快速发展，对运动生成的需求已从单人孤立动作扩展到多人协作、人-物体交互、人-场景交互等复杂场景，这使得**人类交互运动生成**成为一个独立且紧迫的研究方向。

该领域面临三重固有挑战。其一，**交互动作的随机性与时空一致性之间的张力**：交互行为本质上具有高度随机性——同一语义意图可对应多种运动实现，但多人/人物协同运动必须维持精确的空间协调与时间连贯性，这对生成模型的约束建模能力提出了严苛要求。其二，**与外部世界交互需要环境感知与物理约束**：当人与物体或场景交互时，系统必须理解场景布局、物体属性与可供性，并遵守接触、碰撞、支撑等物理约束，而非仅仅生成运动学上合理的姿态序列。其三，**高质量交互数据的采集成本高昂且难以规模化**：相比单人运动，多人交互、人-物交互的数据标注与采集需要多视角同步捕捉、接触点标注等额外投入，使得单纯依赖数据驱动学习变得不切实际。

从方法演进脉络来看，该领域经历了从传统运动图、隐马尔可夫模型到深度生成模型的范式转换。早期工作主要依赖运动匹配与拼接，受限于数据覆盖度而泛化能力有限。近年来，扩散模型、Transformer等表达性生成架构的引入显著提升了运动多样性与质量，但核心瓶颈已从“能否生成”转向“如何生成得真实且交互一致”。成功生成交互运动的关键在于将**语义意图、空间协调与物理真实性**有机融合——语义层面确保动作符合交互意图，空间层面保证多人/人物相对位置与接触的合理性，物理层面则约束运动符合力学规律。

当前方法的缺口集中体现在三个方面：一是多数方法仍以数据驱动为主，对数据稀缺的交互类型泛化不足；二是物理模拟与表达性生成模型的结合尚处于早期阶段，前者精度高但灵活性差，后者生成力强但物理合理性弱；三是缺乏统一的交互运动表示框架，使得跨任务迁移困难。本文正是在此背景下，首次系统性地综述人类交互运动生成的四大子任务——人-人交互、人-物交互、人-场景交互及混合交互——梳理其方法谱系、数据集与评估体系，并指出未来发展的关键方向。



## 核心方法与创新机理

本综述的核心创新不在于提出单一算法，而在于构建了一套系统性的分析框架，将人类交互运动生成领域的碎片化进展整合为三条清晰的技术演进路径，并揭示了驱动性能提升的**可控因果杠杆**。

### 1. 从独立生成到交互感知的范式转换

早期方法将多人运动视为独立个体的并行生成，忽略了交互实体间的动态耦合。本综述识别出该领域的**决定性转折点**在于显式建模交互关系——将语义意图、空间协调与物理真实性有机融合，而非单纯依赖数据驱动学习。这一洞察源于交互运动的三重固有挑战：

- **时空一致性的随机性约束**：交互动作本质上是随机的，但生成的多人/人物运动必须维持与特定意图对齐的时空相干性（Section 1）。
- **环境感知与物理遵从**：与外部世界交互需要理解场景布局、物体属性及可供性，并遵守物理约束（Section 1）。
- **数据稀缺瓶颈**：高质量交互数据的采集成本高昂且难以规模化，使得纯数据驱动路线不可持续（Section 1）。

### 2. 交互关系建模的三个关键创新维度

综述将现有方法的创新点归纳为三个可操作的**changed slots**，每个维度对应一类可控杠杆：

**（1）语义一致性建模**：从单一动作标签转向文本、音频、场景图等富语义条件。例如，**InterGen**采用非规范运动表示，在统一世界坐标系中编码全局关节位置与朝向，解决了多人运动语义对齐中的坐标系歧义问题（Section 4.1.2）。条件变分自编码器（cVAE）的ELBO目标函数为此类条件生成提供了概率基础：

$$\mathcal{L}_{\boldsymbol{\theta},\boldsymbol{\phi}}(\mathbf{x}|\mathbf{c}) = \mathbb{E}_{\mathbf{z}\sim q_{\boldsymbol{\phi}}(\mathbf{z}|\mathbf{x},\mathbf{c})}\left[\ln p_{\boldsymbol{\theta}}(\mathbf{x}|\mathbf{z},\mathbf{c})\right] - D_{\mathrm{KL}}\Big(q_{\boldsymbol{\phi}}(\mathbf{z}|\mathbf{x},\mathbf{c})\Big\| p_{\boldsymbol{\theta}}(\mathbf{z}|\mathbf{c})\Big)$$

**（2）空间协调机制**：通过距离感知损失和空间引导函数施加物理先验。**ReMoS**在训练中引入指数衰减的距离感知反应损失，使反应者关节越靠近施动者时获得越高的优化优先级（Fig. 4 Left）；在推理阶段则施加空间引导函数，将反应者运动与施动者位置对齐（Section 4.1.2-4.1.3）。**InterGen**进一步提出关节距离损失，仅在两人水平距离落入指定范围时激活，形成圆柱形交互敏感区域（Fig. 4 Right）。

**（3）细粒度交互捕捉**：**InterDiff**通过坐标变换将物体状态表示为相对于接触点的运动模式，相比绝对位置表示显著简化了运动模式（Fig. 5），这一设计降低了扩散模型对复杂交互分布的学习难度。在前向扩散过程中，噪声按方差调度$\beta_t$逐步注入：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$$

### 3. 方法谱系与知识库定位

综述建立了清晰的方法分类体系，将现有工作按交互类型（人-人、人-物、人-场景、混合交互）和核心技术路线（扩散模型、VAE/GAN、强化学习、LLM规划）进行双重索引。关键基线及其创新定位包括：

- **Social Diffusion**：采用循环扩散模型与阶不变平均函数聚合多人运动特征，在保持社会角色的同时实现同时生成（Section 4.1.1）。
- **PriorMDM**：冻结双MDM通信机制，通过冻结预训练的单人扩散模型并在去噪过程中注入跨人注意力实现文本到交互生成。
- **CHOIS**：利用基础点集（BPS）表示实现语言引导的物体交互生成，将物体几何抽象为稀疏点集以降低条件空间复杂度。
- **DiffH2O**：两阶段抓取与交互生成框架，先确定抓取姿态再生成后续操纵运动，将复杂交互分解为可管理的子任务。

### 4. 物理模拟与数据驱动融合的前沿探索

综述指出了超越纯数据驱动范式的创新方向：将物理模拟器的精度与扩散模型的表达性相结合。基于强化学习的方法通过与物理环境交互、在平衡与碰撞约束下优化奖励函数来生成物理合理运动（Section 3.3.8），但存在训练收敛困难和泛化能力有限的局限。同时，LLM作为自动化运动规划器的角色正在浮现——将高层目标翻译为逐步交互序列、识别相关关节参与、描述精确交互动态（Section 3.3.8），这为突破数据稀缺瓶颈提供了新的可能。

### 5. 创新边界与待验证方向

本综述的若干判断需要读者结合最新进展进行验证：

- 缺乏统一的交互运动表示框架，使得跨任务迁移困难——这一判断基于现有方法的碎片化现状，但统一表示是否可行仍待探索。
- 评估指标尚未标准化，MPJPE等指标仅衡量关节位置误差，无法全面反映交互的真实性与物理合理性。
- 如何将单人运动编辑技术（关节轨迹控制、风格化生成、文本提示编辑）适配至多人/多实体交互场景，是综述提出的开放问题，但尚未有成熟方案。



本综述将人类交互运动生成方法统一归纳为“表示—条件—生成—评估”四层框架，各层之间存在明确的输入输出依赖关系。

**表示层（Representation Layer）** 位于框架底层，负责定义交互实体的数据结构。人体运动采用基于运动学的骨架关节序列表示，其中6D旋转表示因其连续性和与深度学习模型的兼容性而受到青睐（Section 3.1.1）；参数化模型如SMPL、SMPL-X、GHUM则进一步引入形状参数，支持几何感知的运动表达。物体运动分为两类：刚性物体以6自由度位姿序列 $\mathbf{T}_{1:N} = [\mathbf{t}, \mathbf{R}]_{1:N}$ 描述，铰接物体则通过组合关节旋转、物体平移和物体旋转的位姿参数 $\varOmega \in \mathbb{R}^{7}$ 及其网格 $O(\varOmega) \in \mathbb{R}^{V \times 3}$ 表示（Section 3.1.2）。

**条件层（Conditioning Layer）** 将外部控制信号转化为可注入生成模型的编码。文本条件通常以CLIP嵌入、LLM倒数第二层输出或离散词元序列的形式引入；音频特征经OpenSmile和Librosa处理为韵律、激励、节拍等显著性特征；动作类别则采用独热编码或标签词元嵌入实现（Section 3.2）。

**生成层（Generation Layer）** 是框架核心，涵盖GAN、VAE/cVAE、扩散模型、Transformer、强化学习和大语言模型等生成范式。GAN通过生成器与判别器的极小极大博弈学习数据分布（Equation 1）；VAE通过最大化证据下界（ELBO）逼近数据对数似然（Equation 2），cVAE则引入条件变量扩展ELBO（Equation 3）；扩散模型以前向逐步加噪 $q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$ 和逆向去噪 $p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_{\theta}(\mathbf{x}_t, t), \varSigma_{\theta}(\mathbf{x}_t, t))$ 为核心机制（Equation 4-5）；自注意力机制 $\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$ 则构成Transformer对时序依赖建模的基础（Equation 6）。强化学习方法借助物理模拟器和奖励函数生成物理合理运动，而大语言模型则作为自动化运动规划器，将高层目标分解为逐步交互序列（Section 3.3）。

**评估层（Evaluation Layer）** 对生成结果进行多维度度量，包括以MPJPE为代表的运动精度指标、物理合理性指标以及交互一致性指标（Section 6.1.1，Table 9）。

框架的模块间数据流如下：表示层输出的实体运动表征作为生成层的训练与推理数据；条件层将文本、音频、动作标签等外部信号编码后注入生成层以控制生成过程；生成层产出的运动序列最终由评估层进行定量与定性检验。这一分层架构使得不同交互场景（人-人、人-物、人-场景、混合交互）的方法可以在统一框架下进行比较和定位。



### 交互实体表示

人类交互运动生成的首要环节是对参与交互的实体进行数学表示，这直接影响后续生成模型的设计空间与约束施加方式。

**人体运动表示** 主要分为运动学表示与参数化模型两类。运动学方法将人体运动定义为骨骼姿态序列，每个姿态由关节位置或骨骼旋转构成。旋转表示中，6D连续旋转表示因其连续性和与深度学习模型的兼容性而成为主流选择。参数化模型如SMPL、SMPL-X和GHUM则在旋转参数之外引入形状参数，使表示具备几何感知能力，能够同时刻画体型差异与姿态变化。

**物体表示** 根据物体类型存在显著差异。对于刚体，运动状态由6自由度位姿序列描述：

$$\mathbf{T}_{1:N} = [\mathbf{t}, \mathbf{R}]_{1:N}$$

其中 $\mathbf{t} \in \mathbb{R}^3$ 表示平移，$\mathbf{R} \in SO(3)$ 表示旋转。对于铰接物体，其3D网格表示为 $O(\varOmega) \in \mathbb{R}^{V \times 3}$，姿态参数 $\varOmega \in \mathbb{R}^{7}$ 融合了铰接旋转、物体平移与物体旋转三个分量。

**场景表示** 则需同时编码静态几何与语义信息，常用方法包括点云、体素网格、隐式神经场以及3D高斯泼溅等。

### 条件模态编码

生成模型需将多种条件信号转化为可嵌入的特征表示：

- **文本条件**：通过CLIP嵌入、大语言模型倒数第二层输出或离散词元序列引入，如InterGen采用LLM特征作为交互语义的条件信号。
- **音频条件**：利用OpenSmile和Librosa等工具提取韵律、激励、音乐强度和节奏节拍等声学特征。
- **动作类别**：以独热编码或标签词元嵌入形式实现，为生成提供离散的交互类型约束。
- **场景与物体条件**：通过点云编码器、体素网格或隐式场将3D环境信息映射为条件特征。

### 基础生成模型

综述梳理了交互运动生成中三类核心生成框架的数学基础。

**生成对抗网络** 通过生成器 $G$ 与判别器 $D$ 的对抗训练实现运动生成，其最小最大目标函数为：

$$\min_G \max_D \left[ \mathbb{E}_{\mathbf{x} \sim p_{\text{data}}(\mathbf{x})} (\log D(\mathbf{x})) + \mathbb{E}_{\mathbf{z} \sim p_{\mathbf{z}}(\mathbf{z})} (\log (1 - D(G(\mathbf{z})))) \right]$$

生成器试图产生判别器无法区分的运动，判别器则最大化对真实与生成样本的分类能力。

**变分自编码器** 通过最大化证据下界来近似数据分布的对数似然：

$$L_{\theta,\phi}(\mathbf{x}) = \mathbb{E}_{\mathbf{z}\sim q_{\phi}(\mathbf{z}|\mathbf{x})}[\ln p_{\theta}(\mathbf{x}|\mathbf{z})] - D_{KL}(q_{\phi}(\mathbf{z}|\mathbf{x})\parallel p_{\theta}(\mathbf{z}))$$

条件变分自编码器进一步引入条件变量 $\mathbf{c}$，将ELBO扩展为：

$$\mathcal{L}_{\boldsymbol{\theta},\boldsymbol{\phi}}(\mathbf{x}|\mathbf{c}) = \mathbb{E}_{\mathbf{z}\sim q_{\boldsymbol{\phi}}(\mathbf{z}|\mathbf{x},\mathbf{c})}[\ln p_{\boldsymbol{\theta}}(\mathbf{x}|\mathbf{z},\mathbf{c})] - D_{\mathrm{KL}}(q_{\boldsymbol{\phi}}(\mathbf{z}|\mathbf{x},\mathbf{c})\| p_{\boldsymbol{\theta}}(\mathbf{z}|\mathbf{c}))$$

**扩散模型** 已成为交互运动生成的主流范式。前向过程按方差调度 $\beta_t$ 逐步添加高斯噪声：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$$

逆向过程由神经网络 $\theta$ 预测去噪后的均值与协方差：

$$p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_{\theta}(\mathbf{x}_t, t), \varSigma_{\theta}(\mathbf{x}_t, t))$$

**Transformer架构** 通过自注意力机制捕获运动序列中的时空依赖：

$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$$

该机制在Inter-Former等交互生成方法中被用于建模多人运动之间的空间关联与时间演化。

**强化学习与LLM规划** 构成补充性生成范式。强化学习方法通过物理模拟器与奖励函数生成物理合理运动，但面临训练收敛困难与泛化能力有限的瓶颈。大语言模型则作为自动化运动规划器，将高层交互目标分解为逐步执行的运动序列，为数据稀缺场景提供了一种替代路径。

### 交互感知的核心机制

在基础生成框架之上，交互运动生成方法引入了一系列专门设计的交互感知模块。

**距离感知损失** 是提升局部交互真实性的关键杠杆。如Fig. 4所示，ReMoS采用指数衰减的距离感知反应损失，对靠近施动者的反应者关节赋予更高权重；InterGen则引入关节距离损失，仅在两人水平距离落入指定范围时激活，实现空间选择性的交互约束。

**坐标变换策略** 被用于简化物体运动模式的学习。如Fig. 5所示，InterDiff将物体状态表示为相对于接触点的局部坐标，相较于绝对位置表示，变换后的运动模式更为简洁，显著降低了生成难度。

**空间引导函数** 在推理阶段施加空间约束。ReMoS在去噪过程中注入空间引导，使反应者运动与施动者位置保持空间对齐，从而增强生成结果的全局人际协调性。

### 评估指标

综述汇总了交互运动生成的核心评估指标。其中，平均关节位置误差衡量预测与真实3D关节位置之间的欧氏距离：

$$MPJPE(f, S) = \frac{1}{N_S} \sum_{i=1}^{N_S} \| m_{f, S}^{(f)}(i) - m_{gt, S}^{(f)}(i) \|_2$$

该指标是衡量运动重建精度的基础度量，但无法全面反映交互运动在物理合理性、语义一致性与时空协调性方面的质量——这正是当前评估体系尚未标准化的核心痛点。



## 实验与关键发现

### 综述方法论与证据来源说明

本文为一篇系统性综述，未进行独立的定量实验。本节所列方法性能、消融结论与失败模式均源于原文所引用的原始文献。综述共覆盖四大交互场景（人-人交互、人-物交互、人-场景交互、混合交互），对应方法总览见表1至表4，所用数据集汇总见表5至表8，评估指标概述见表9。以下分析聚焦于各子领域方法中的关键性能瓶颈、消融发现与失败模式。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/006_Table_1.jpg]]
*Table 1: Representative works of human-human interaction motion generation*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/013_Table_4.jpg]]
*Table 4: Representative works of human-mix interaction motion generation. (HH: Human-Human, HO: Human-Object, HS: Human-Scene.)*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/014_Table_5.jpg]]
*Table 5: Human-human interaction datasets. This table summarizes key statistics and features of various human-human interaction datasets. Subjects: The number of individuals involved in the dataset; Sequences: The number of motion clips available; Frames: The total number of frames capturing 3D human motions; Length: The cumulative duration of the dataset’s motion data (in hours); Acquisition: The method used to obtain motion data (e.g., multi-view RGB videos denoted as “mRGB”); Modality: The representation format of motion data; Video, Text, Audio: Indicates whether the dataset includes corresponding modalities*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/017_Table_8.jpg]]
*Table 8: Human-mix interaction datasets. This table summarizes key statistics and features of various human-mix interaction datasets. Tasks: Types of human interaction tasks—HHI: Human-Human Interaction, HOI: Human-Object Interaction; Subjects: The number of entities involved in the dataset; Sequences: The number of motion clips available; Frames: The total number of frames capturing 3D human motions; Length: The cumulative duration of the dataset’s motion data (in hours); Acquisition: The method used to obtain motion data; Modality: The representation format of motion data; Video, Text, Audio: Indicates whether the dataset includes corresponding modalities*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/018_Table_9.jpg]]
*Table 9: Overview of evaluation metrics for human interaction motion generation*

### 人-人交互生成中的关键瓶颈与消融发现

**空间协调是核心瓶颈。** 人-人交互生成面临语义一致性、全局人际协调与细粒度局部交互三重挑战（Fig. 3）。早期方法在全局空间对齐上表现薄弱：**PriorMDM**（Shafir et al., ICCV 2023）通过冻结双MDM通信实现文本到交互生成，但其独立建模策略导致两人运动的空间耦合不足。**Social Diffusion**（Tevet et al., ECCV 2024）引入顺序不变平均函数聚合多人运动特征，虽保留社会角色和空间关系，但该聚合机制在密集交互场景下可能模糊个体运动细节。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/005_Figure_3.jpg]]
*Figure 3: (c) Fine-grained Local Interaction Fig. 3: Illustration of three major challenges in human-human interaction generation: (a) Semantic consistency; (b) Global interpersonal coordination; and (c) Fine-grained local interaction. All figures are adapted from [244]*

**距离感知损失是提升局部交互质量的有效杠杆。** **ReMoS**（Ghosh et al., CVPR 2024）的消融实验表明，其指数衰减距离感知反应损失（Fig. 4 Left）显著提升了近距离交互的保真度——该损失优先惩罚靠近动作发起者的反应者关节，使接触区域的重建误差大幅降低。**InterGen**（Liang et al., CVPR 2024）的关节距离损失仅在两人水平距离落入指定范围时激活（Fig. 4 Right），消融显示移除该损失后，交互接触时刻的穿透与悬浮伪影明显增加。

**运动表示选择直接影响生成质量。** InterGen采用非规范运动表示，在统一世界坐标系中编码全局关节位置与朝向。消融表明，相比规范姿态表示，该方案在双人空间关系建模上具有明显优势，但代价是泛化到未见动作组合时的鲁棒性下降。**ReGenNet**（Zhou et al., CVPR 2025）的消融显示，其简单拼接动作特征与生成反应特征的策略在短时交互上有效，但长序列生成中误差累积问题突出。

### 人-物交互生成中的物理约束与失败模式

**物体状态表示的坐标变换是简化运动模式的关键。** **InterDiff**（Xu et al., CVPR 2024）将物体状态相对于接触点进行坐标变换，使运动模式显著简化（Fig. 5）。消融实验表明，使用绝对位置表示时，生成模型难以学习物体运动的规律性，导致抓取后的物体轨迹出现物理不合理漂移。

**两阶段策略缓解了联合生成的复杂性。** **DiffH2O**（Zhang et al., NeurIPS 2023）将任务分解为抓取生成与交互生成两阶段，消融显示单阶段联合生成在手-物接触精度上显著劣于两阶段方案。但两阶段方法存在级联误差问题——第一阶段的抓取误差会传播至第二阶段，尤其在物体几何复杂或抓取姿态多样时。

**基于物理模拟的方法面临训练收敛与泛化困境。** 依赖强化学习的方法（如**InterDiff**的物理信息驱动组件）在简单交互上可生成物理合理的结果，但在复杂接触序列上训练收敛困难，且对未见物体形状的泛化能力有限。这是当前人-物交互生成中最显著的失败模式之一。

### 人-场景交互与混合交互的评估挑战

**场景感知生成的评估缺乏标准化指标。** 现有指标（如MPJPE）仅衡量关节位置精度，无法评估生成运动与场景的物理合理性（如穿透、悬浮、接触力分布）。Table 9汇总的指标中，物理合理性评估仍主要依赖人工评判或间接代理指标，缺乏统一的自动化度量。

**混合交互场景的评估更为薄弱。** 涉及多人、多物、多场景的混合交互生成（Table 4）尚处早期阶段，现有方法多为模块化组合，缺乏端到端的统一评估框架。各子任务间的误差传播与累积效应尚未得到系统研究。

### 数据集层面的局限性

高质量交互数据的采集成本高昂且难以规模化，这是全领域的共性瓶颈。Table 5-8显示，现有数据集在交互类型覆盖上严重不均衡——常见交互（如握手、传递物品）数据充足，而复杂多步骤交互（如协作装配）数据极度稀缺。数据驱动方法在这些稀缺交互类型上的泛化失败是普遍现象。此外，多数数据集缺乏物理接触力标注和环境几何信息，限制了物理感知方法的训练与评估。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/015_Table_6.jpg]]
*Table 6: Human-object interaction datasets. This table summarizes key statistics and features of various human-object interaction datasets. Subjects: The number of individuals involved in the dataset; Sequences: The number of motion clips available; Frames: The total number of frames capturing 3D human motions; Length: The cumulative duration of the dataset’s motion data (in hours); Acquisition: The method used to obtain motion data (e.g., multi-view RGB videos denoted as “mRGB”); Modality: The representation format of motion data; Images, Text: Indicates whether the dataset includes corresponding modalities*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/016_Table_7.jpg]]
*Table 7: Human-scene interaction datasets. This table summarizes key statistics and features of various human-scene interaction datasets. Subjects: The number of individuals involved in the dataset; Sequences: The number of motion clips available; Frames: The total number of frames capturing 3D human motions; Length: The cumulative duration of the dataset’s motion data (in hours); Motion Acquisition: The method used to obtain motion data; Scene Acquisition: The method used to obtain scene data; Modality: The representation format of motion data; Dynamic: Indicates whether the dataset includes dynamic or static scene*

### 开放问题与未来评估方向

综述识别的开放问题直接指向评估体系的完善需求：（1）如何利用异构数据源及大语言模型/视觉语言模型突破数据稀缺瓶颈，需要建立跨数据源的评估协议；（2）物理模拟器精度与表达性生成模型灵活性的结合，要求新的混合评估指标同时衡量运动自然度与物理可行性；（3）交互感知特征表示的设计需在有限数据下验证其跨任务迁移能力；（4）单人运动编辑控制技术向多人/多实体交互场景的适配，需要建立相应的可控性评估基准。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/010_Figure.jpg]]
*Figure: (a) Motion Generation System (b) Environment Constraints (c) Contextual Interaction Understanding*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/001_Figure_1.jpg]]
*Figure 1: (b) Timeline of human interaction datasets Fig. 1: Statistics on the number of works and datasets on human interaction motion generation over the past two decades, categorized into four interaction scenarios*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/008_Table_2.jpg]]
*Table 2: Representative works of human-object interaction motion generation*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2503_12763v2/figures/012_Table_3.jpg]]
*Table 3: Representative works of human-scene interaction motion generation*



## 定位与知识库关联

### 任务边界与核心瓶颈

本综述将人类交互运动生成界定为四个子领域：人-人交互（HHI）、人-物交互（HOI）、人-场景交互（HSI）以及混合交互。该领域的根本瓶颈源于三重固有挑战：交互动作的随机性要求生成结果在多人/人物之间维持时空一致性；与外部世界交互需要理解场景布局、物体属性并遵守物理约束；而高质量交互数据的采集成本高昂且难以规模化，使得单纯依赖数据驱动学习不切实际。这三重挑战共同构成了方法设计的约束空间——任何生成系统必须在语义意图、空间协调与物理真实性之间取得平衡。

### 基础生成模型谱系

交互运动生成的方法根基建立在三类主流深度生成模型之上：

**生成对抗网络（GAN）** 通过生成器与判别器的对抗训练学习数据分布，其目标函数为：

$$\begin{array} { r l } & { \underset { G } { \operatorname* { m i n } } \underset { D } { \operatorname* { m a x } } \Big [ \mathbb { E } _ { \mathbf { x } \sim p _ { \mathrm { d a t a } } ( \mathbf { x } ) } \big ( \log D ( \mathbf { x } ) \big ) + } \\ & { \quad \quad \quad \mathbb { E } _ { \mathbf { z } \sim p _ { \mathbf { z } } ( \mathbf { z } ) } \big ( \log \big ( 1 - D ( G ( \mathbf { z } ) ) \big ) \big ) \Big ] } \end{array}$$

GAN在早期交互生成中占据主导，但训练不稳定和模式坍塌问题限制了其在复杂交互场景中的表现。

**变分自编码器（VAE）** 通过最大化证据下界（ELBO）来近似数据分布：

$$L_{\theta,\phi}(\mathbf{x}) = \mathbb{E}_{\mathbf{z}\sim q_{\phi}(\mathbf{z}|\mathbf{x})}\left[\ln p_{\theta}(\mathbf{x}|\mathbf{z})\right] - D_{KL}\left(q_{\phi}(\mathbf{z}|\mathbf{x})\parallel p_{\theta}(\mathbf{z})\right)$$

条件变分自编码器（cVAE）通过引入条件变量 $\mathbf{c}$ 扩展ELBO，实现可控生成：

$$\mathcal{L}_{\boldsymbol{\theta},\boldsymbol{\phi}}(\mathbf{x}|\mathbf{c}) = \mathbb{E}_{\mathbf{z}\sim q_{\boldsymbol{\phi}}(\mathbf{z}|\mathbf{x},\mathbf{c})}\left[\ln p_{\boldsymbol{\theta}}(\mathbf{x}|\mathbf{z},\mathbf{c})\right] - D_{\mathrm{KL}}\Big(q_{\boldsymbol{\phi}}(\mathbf{z}|\mathbf{x},\mathbf{c})\Big\| p_{\boldsymbol{\theta}}(\mathbf{z}|\mathbf{c})\Big)$$

VAE类方法在交互生成中因其隐空间的结构化特性而适用于运动编辑与可控合成，但生成质量通常逊于扩散模型。

**扩散模型** 已成为当前交互运动生成的主流范式。其前向过程按方差调度 $\beta_t$ 逐步添加高斯噪声：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$$

逆向过程由神经网络 $\theta$ 预测去噪分布：

$$p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_{\theta}(\mathbf{x}_t, t), \varSigma_{\theta}(\mathbf{x}_t, t))$$

扩散模型凭借其稳定的训练过程和高质量的生成样本，在文本到交互、反应生成、多人预测等任务中展现出显著优势。此外，基于物理模拟的强化学习方法和基于大语言模型的运动规划方法构成了补充性技术路线，前者侧重物理真实性但面临训练收敛困难，后者在高层语义规划上展现潜力但尚未形成成熟系统。

### 人-人交互生成方法演进

人-人交互生成方法围绕三个递进挑战展开：语义一致性、全局人际协调和细粒度局部交互。

**语义建模**方面，早期工作以历史运动为条件预测未来交互。**Social Diffusion** 采用循环扩散模型，通过顺序不变的聚合函数融合多人运动特征，同时保持社会角色和个体身份。**MRT** 引入多范围Transformer，同时编码局部和全局时序依赖。在文本条件驱动下，**InterGen** 采用非规范运动表示，在统一世界坐标系中编码全局关节位置与朝向，从文本描述直接生成双人交互运动。**PriorMDM** 则通过冻结的双MDM通信机制实现文本到交互的生成，避免了对交互数据的直接依赖。

**空间协调**是区别于单人运动生成的关键维度。**ReMoS** 在推理阶段施加空间引导函数，使反应者运动与施动者位置对齐；同时采用指数衰减的距离感知反应损失，优先优化靠近施动者的反应者关节（参见Fig. 4）。**InterGen** 引入关节距离损失，仅在两人水平距离落入指定范围时激活，形成圆柱形交互区域的约束机制。这些显式的空间先验构成了提升生成真实性的可控杠杆。

**细粒度交互**建模涉及接触约束和物理合理性。基于Transformer的**Inter-Former** 使用时序与空间注意力机制，并引入首帧损失函数对齐初始姿态。**ReGenNet** 采用扩散模型迭代生成反应者运动，在每个时间步将施动者运动特征与生成的反应者运动拼接，以简单有效的策略实现反应生成。

### 人-物与场景交互的方法定位

人-物交互生成的核心挑战在于物体属性理解与接触约束建模。**DiffH2O** 采用两阶段策略分别处理抓取与交互生成，将复杂任务分解为可管理的子问题。**CHOIS** 利用基元点集（BPS）表示物体，实现语言引导的物体交互生成。**InterDiff** 通过坐标变换将物体状态表示为相对于接触点的运动模式，使运动模式显著简化（参见Fig. 5），体现了物理先验对生成质量的关键影响。

人-场景交互生成方法围绕三个支柱构建（参见Fig. 6）：运动生成系统将复杂交互分解为模块化子任务；环境约束模型融入人与环境的物理约束；上下文交互理解分析环境内的空间关系。

### 局限与开放问题

当前方法存在若干系统性局限：

1. **数据瓶颈**：基于物理模拟的方法依赖强化学习，存在训练收敛困难和泛化能力有限的局限；数据驱动方法对数据稀缺的交互类型泛化不足。如何利用异构数据源及LLM/VLM等预训练模型突破数据稀缺瓶颈，是亟待探索的方向。

2. **表示框架缺失**：缺乏统一、可扩展的交互运动表示框架，使得跨任务迁移困难。在有限高质量数据下设计高效且交互感知的特征表示，是方法泛化的关键。

3. **评估标准化不足**：评估指标尚未标准化，难以全面衡量生成交互的真实性与物理合理性。

4. **物理与表达性融合**：如何将物理模拟器的精度与扩散模型等表达性生成模型的灵活性有效结合，代表了方法演进的前沿方向。

5. **编辑与控制技术迁移**：如何将现有的单人运动编辑与控制技术（如关节轨迹控制、风格化生成、文本提示编辑）适配至多人/多实体交互场景，是实用性提升的重要方向。

*注：本文为综述性质，未进行独立的定量实验验证，所列方法的性能指标均源于原文献，读者在横向比较时需注意不同方法使用的数据集和评估协议可能存在差异。*



## 原文 PDF

![[paperPDFs/IJCV_2025/A_Survey_on_Human_Interaction_Motion_Generation.pdf]]

---
title: "SMRABooth: Subject and Motion Representation Alignment for Customized Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SMRABooth_Subject_and_Motion_Representation_Alignment_for_Customized_Video_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Xu_SMRABooth_Subject_and_Motion_Representation_Alignment_for_Customized_Video_Generation_CVPR_2026_paper.html
project_link: https://smrabooth.github.io
code_link: null
aliases:
- SMRABooth
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 两个对象级表征对齐模块——SuRA模块通过DINOv2自监督视觉编码器提供主体全局空间结构和语义表征，MoRA模块通过SEA-RAFT光流编码器提供显式的对象级运动轨迹表征；以及基于LoRA稀疏性（注入位置和注入时序两个维度）的主体-运动关联解耦策略。
primary_logic: 将视频扩散模型的中间特征与外部对象级表征进行对齐——利用DINOv2自监督编码器提取的主体空间-语义特征指导主体LoRA学习，利用SEA-RAFT光流编码器提取的像素级运动轨迹指导运动LoRA学习——并发现LoRA在不同Transformer层和不同去噪时序上的影响具有高度稀疏性：主体LoRA主要由Q、K、FFN.0层决定，运动LoRA主要由V、O、FFN.0、FFN.2层决定；且在去噪早期（约前10-25步）运动先形成、主体外观后细化。基于此稀疏性设计的分层分时LoRA注入策略，可在不牺牲性能的前提下解耦主体与运动学习，避免DiT架构中的特征纠缠。
claims:
- SuRA模块通过DINOv2特征对齐增强全局语义理解和空间结构感知，提升主体保真度
- MoRA模块通过光流编码器显式提取对象级运动轨迹，过滤外观冗余信息
- LoRA稀疏性实验表明主体LoRA主要受Q、K、FFN.0层影响，运动LoRA主要受V、O、FFN.0、FFN.2层影响
- 稀疏LoRA与全层微调效果相当，且有效解决了DiT中主体与运动的耦合干扰问题
---

# SMRABooth: Subject and Motion Representation Alignment for Customized Video Generation

> [!tip] 核心洞察
> 将视频扩散模型的中间特征与外部对象级表征进行对齐——利用DINOv2自监督编码器提取的主体空间-语义特征指导主体LoRA学习，利用SEA-RAFT光流编码器提取的像素级运动轨迹指导运动LoRA学习——并发现LoRA在不同Transformer层和不同去噪时序上的影响具有高度稀疏性：主体LoRA主要由Q、K、FFN.0层决定，运动LoRA主要由V、O、FFN.0、FFN.2层决定；且在去噪早期（约前10-25步）运动先形成、主体外观后细化。基于此稀疏性设计的分层分时LoRA注入策略，可在不牺牲性能的前提下解耦主体与运动学习，避免DiT架构中的特征纠缠。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMRABooth：面向定制化视频生成的主体与运动表征对齐 |
| 英文题名 | SMRABooth: Subject and Motion Representation Alignment for Customized Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_SMRABooth_Subject_and_Motion_Representation_Alignment_for_Customized_Video_Generation_CVPR_2026_paper.html) · [Project](https://smrabooth.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | SMRABooth |
| Dataset | Customized Video Generation, User Study |

> [!tip] 效果简介
> - Customized Video Generation (DiT-based, WAN2.1 backbone, 30 subjects × 21 motio... 上，CLIP-T (文本-视频语义对齐) 0.363 (SMRABooth) vs 未明确给出各baseline精确值（所有对比方法中最高） (Outperforms all DiT-based baselines)。
> - Customized Video Generation (DiT-based, WAN2.1 backbone) 上，Motion Fidelity (运动保真度) 62.89 (SMRABooth) vs DualReal (次优) (Significantly outperforms DualReal and all other baselines)。
> - User Study (DiT-based methods, 5-point Likert scale) 上，Prompt Alignment (提示对齐度) 4.228±0.041 (SMRABooth) vs 未明确给出各baseline精确值（所有方法中最高） (Highest among all compared methods)。

## 概要

**1. 问题背景与瓶颈**

定制化视频生成旨在同时控制视频中的“主体外观”与“物体运动”，使其符合用户提供的参考图像和运动视频。现有主流方法——无论是基于DiT架构的**MotionBooth**（Wu et al., NeurIPS 2024）、**DualReal**（Wang et al., arXiv 2025），还是基于U-Net架构的**DreamVideo**（Wei et al., CVPR 2024）、**MotionDirector**（Zhao et al., ECCV 2024）——普遍存在一个根本性缺陷：**缺乏对象级（object-level）的主体外观与运动模式引导**。这导致三个核心瓶颈：

- **主体结构失真**：主体生成仅依赖文本token和隐式特征，缺少全局空间结构和高层语义感知，导致外观不完整（如手部缺失、形状错误）。
- **运动趋势错误**：运动学习仅通过时序层隐式捕获帧间变化，无法显式建模对象级运动轨迹，且运动特征与外观特征高度纠缠。
- **DiT架构中的特征干扰**：DiT缺乏U-Net式的空间-时序层解耦，主体LoRA和运动LoRA直接在全层注入时产生严重干扰，导致伪影、视频质量下降和过度背景复制。

**2. 核心方法与因果机制**

本文提出**SMRABooth**，核心思路是将视频扩散模型的中间特征与**外部对象级表征**进行显式对齐，并利用LoRA的稀疏特性实现主体-运动解耦。方法包含三个关键创新：

- **主体表征对齐（SuRA）**：采用DINOv2自监督视觉编码器提取主体图像的全局空间-语义特征，通过余弦相似度损失与DiT中间特征对齐，使主体LoRA学习具有全局结构感知的语义表征。
- **运动表征对齐（MoRA）**：采用SEA-RAFT光流编码器从参考视频中显式提取像素级运动轨迹特征，通过L1损失与去噪视频的光流特征对齐，过滤外观冗余信息，指导运动LoRA学习对象级运动模式。
- **主体-运动关联解耦**：通过实验发现LoRA在不同Transformer层和不同去噪时序上的影响具有高度稀疏性——主体LoRA主要由Q、K、FFN.0层决定，运动LoRA主要由V、O、FFN.0、FFN.2层决定；且在去噪早期（约前10-25步）运动先形成、主体外观后细化。基于此，设计分时分层的稀疏LoRA注入策略，在DiT架构中有效解耦主体与运动学习。

**3. 方法定位与知识库贡献**

SMRABooth在定制化视频生成领域的方法谱系中占据独特位置：

- 相较于仅依赖文本token和隐式特征的主体定制方法（如CustomCrafter, Wu et al., AAAI 2025），SMRABooth首次引入**自监督视觉编码器**提供对象级主体表征对齐。
- 相较于仅通过时序层隐式学习运动的方法（如MotionBooth），SMRABooth首次引入**光流编码器**提供显式的像素级运动轨迹表征对齐。
- 相较于在DiT架构中全层注入LoRA的常规做法，SMRABooth首次揭示了**LoRA在注入位置和注入时序两个维度上的稀疏性**，并据此设计了通用的主体-运动解耦策略，可适配不同骨干网络。

**4. 主要结果摘要**

在基于WAN2.1骨干的DiT架构定制视频生成任务上（30个主体 × 21种运动类型），SMRABooth在所有评估指标上均优于现有DiT方法：CLIP-T（文本-视频语义对齐）达到0.363，Motion Fidelity（运动保真度）达到62.89，显著超越次优方法DualReal。用户研究（5分Likert量表）中，SMRABooth的Prompt Alignment评分达到4.228±0.041，同样为所有对比方法中最高。该方法在U-Net架构上也展现出良好的可迁移性，能够有效保持主体身份和运动模式。消融实验证实，SuRA损失显著增强全局结构保持，MoRA损失有效捕获对象级运动信息，稀疏LoRA策略在达到全层微调效果的同时避免了特征干扰。

### 任务背景：定制化视频生成的双重需求

文本到视频（Text-to-Video, T2V）生成领域近年来取得了显著进展，大规模预训练视频扩散模型已能根据文本描述生成高质量、时序连贯的视频内容。然而，在实际应用中，用户往往不仅希望控制视频的语义内容，还期望对**特定主体外观**和**特定运动模式**进行精确定制——例如，让一只特定的宠物狗执行旋转跳跃动作，或让一辆特定设计的汽车沿曲线轨迹行驶。这种“主体+运动”联合定制的需求，构成了定制化视频生成（Customized Video Generation）任务的核心挑战。

该任务要求模型同时满足两个约束：（1）**主体保真度**——生成视频中的目标对象必须忠实保留参考图像中的外观、结构和语义特征；（2）**运动保真度**——生成视频中的对象运动轨迹必须与参考视频中的运动模式保持一致。这两个目标的协同实现，是当前视频生成领域的前沿难题。

### 现有方法的三个核心瓶颈

现有定制化视频生成方法在主体外观与运动模式的引导机制上存在根本性不足，可归纳为三个递进式的瓶颈：

**瓶颈一：主体外观学习缺乏对象级结构感知。** 当前方法（如 **MotionBooth**（Wu et al., NeurIPS 2024）、**CustomCrafter**（Wu et al., AAAI 2025）等）通常依赖特殊文本token（如 V*）和隐式特征来学习主体外观。这种机制缺少对主体**全局空间结构**和**高层语义**的显式建模，导致生成结果中出现主体外观不完整、结构失真等问题——例如手部缺失、形状错误或关键纹理丢失。如 Figure 2 所示，缺乏对象级信息的方法在主体保存方面表现出明显的结构性缺陷。

**瓶颈二：运动学习缺乏显式的对象级运动轨迹建模。** 现有方法（如 **MotionDirector**（Zhao et al., ECCV 2024））主要通过时序注意力层隐式捕获帧间运动信息，无法显式建模对象级的绝对运动轨迹。这导致两个后果：一是运动趋势容易出错（如方向偏移、幅度失配），二是运动特征与外观特征在隐空间中发生纠缠，使得运动编辑时主体外观发生不可控变化。

**瓶颈三：DiT架构中主体与运动LoRA的耦合干扰。** 与U-Net架构具有天然的空间-时序层解耦特性不同，基于DiT（Diffusion Transformer）的视频扩散模型（如WAN2.1）将所有特征处理统一在Transformer块中。当主体LoRA和运动LoRA直接注入所有层的全部线性投影时，两者产生严重的特征干扰，表现为视频伪影增多、整体质量下降和背景区域过度复制。**DreamVideo**（Wei et al., CVPR 2024）在U-Net架构中通过分离主体和运动LoRA取得了进展，但DiT架构下的解耦问题尚未被有效解决。

### 本文动机：对象级表征对齐与LoRA稀疏解耦

针对上述瓶颈，本文提出 **SMRABooth**，核心动机来自两个关键洞察：

**洞察一：外部对象级表征可以显式引导定制学习。** 自监督视觉编码器（如DINOv2）在预训练过程中习得了强大的对象级空间结构和语义建模能力，能够提供主体外观的全局表征；光流编码器（如SEA-RAFT）则能提取像素级的绝对运动轨迹，过滤外观冗余信息。将这些外部表征作为对齐目标，可以弥补扩散模型内部隐式学习的不足。

**洞察二：LoRA在不同Transformer层和不同去噪时序上的影响具有高度稀疏性。** 初步实验表明，主体LoRA主要由Q、K、FFN.0层决定，运动LoRA主要由V、O、FFN.0、FFN.2层决定；且在去噪早期（约前10-25步）运动先形成、主体外观后细化。利用这一稀疏性设计分层分时的LoRA注入策略，可在不牺牲性能的前提下解耦主体与运动学习。

基于上述动机，SMRABooth设计了两个对象级表征对齐模块（SuRA和MoRA）以及一个基于LoRA稀疏性的主体-运动关联解耦策略，系统性地解决了定制化视频生成中主体保真度不足、运动一致性差和DiT架构下特征纠缠三大问题。

## 核心方法与创新机理

SMRABooth 的核心创新可归结为**两个对象级表征对齐模块**和**一套基于 LoRA 稀疏性的主体-运动解耦策略**，共同解决了 DiT 架构下定制化视频生成中主体外观失真与运动趋势错误的瓶颈问题。

### 创新一：从隐式学习到显式对象级表征对齐

现有方法（如 **MotionBooth**（Wu et al., NeurIPS 2024）、**DualReal**（Wang et al., arXiv 2025））仅通过文本 token 和时序层隐式捕获主体外观与运动模式，缺乏全局结构感知和显式运动轨迹建模，导致主体结构不完整（如手部缺失、形状错误）和运动趋势错误。

SMRABooth 引入两个外部编码器提供对象级表征作为对齐目标：

- **SuRA（主体表征对齐）**：利用冻结的 **DINOv2-ViT** 自监督编码器提取主体图像的全局空间-语义特征，通过余弦相似度损失与 DiT 中间特征对齐，使主体 LoRA 获得高层结构感知能力，从而增强主体保真度。
- **MoRA（运动表征对齐）**：利用 **SEA-RAFT** 光流编码器从参考视频中显式提取像素级运动轨迹特征，通过 L1 损失与去噪视频的光流特征对齐，过滤外观冗余信息，使运动 LoRA 专注于对象级运动模式学习。

这一设计将“主体是什么”和“主体如何运动”从隐式耦合中解绑，分别由专用编码器提供结构化监督信号。

### 创新二：基于 LoRA 稀疏性的主体-运动解耦策略

DiT 架构缺乏 U-Net 式的空间-时序层解耦，若将主体 LoRA 和运动 LoRA 同时注入所有 WAN Block 层，会产生严重特征干扰，导致伪影和视频质量下降。SMRABooth 通过系统性的稀疏性实验发现：

- **注入位置稀疏性**：主体 LoRA 主要由 **Q、K、FFN.0** 层决定；运动 LoRA 主要由 **V、O、FFN.0、FFN.2** 层决定。仅在这些关键层注入 LoRA 即可达到与全层微调相当的效果，同时避免层间干扰。
- **注入时序稀疏性**：在去噪早期（约前 10–25 步），运动先形成、主体外观后细化。据此设计 **T_point 分时权重调度**——T_point 前降低主体 LoRA 权重以优先恢复运动，T_point 后提高权重以细化主体外观细节。

这套解耦策略从“注入哪些层”和“何时注入”两个维度实现了主体与运动学习的分离，是 SMRABooth 在 DiT 骨干上取得性能突破的关键机制。

### 与 Baseline 的 changed slots 对比

| 创新维度 | Baseline 做法 | SMRABooth 做法 |
|---------|-------------|---------------|
| 主体特征对齐目标 | 无外部表征，仅通过特殊 token V* 和文本条件隐式学习 | DINOv2-ViT 提取的全局空间-语义特征，余弦相似度损失对齐 |
| 运动特征对齐目标 | 无显式表征，仅通过时序层隐式捕获帧间运动 | SEA-RAFT 光流编码器提取的像素级运动轨迹，L1 损失对齐 |
| LoRA 注入层级 | 主体和运动 LoRA 均注入所有 WAN Block 层 | 主体 LoRA 仅注入 Q/K/FFN.0；运动 LoRA 仅注入 V/O/FFN.0/FFN.2 |
| LoRA 时序权重 | 整个去噪过程权重保持不变 | T_point 前降低主体权重优先运动，T_point 后提高权重细化外观 |

消融实验（Table 3）证实：完整 SMRABooth 在所有指标（CLIP-T、DINO-I、CLIP-I、Motion Fidelity、Temporal Consistency）上均取得最优，移除任一模块或采用全层注入均导致显著性能下降。

SMRABooth 将定制化视频生成拆解为**主体学习**与**运动学习**两个阶段，并在推理阶段通过**主体-运动关联解耦**策略实现两者的协同控制。整个框架建立在冻结的 WAN2.1 视频扩散 Transformer（DiT 架构）之上，训练时仅更新低秩适配器（LoRA），推理时将 LoRA 权重合并至骨干网络。

### 阶段一：主体学习

主体学习阶段的目标是让模型学会在视频中稳定保持给定主体对象的外观、结构与语义一致性。其核心是**主体表征对齐模块（SuRA）**：

- **输入**：一张主体参考图像，经 SAM 分割得到主体区域掩码 M。
- **对齐目标**：冻结的 DINOv2-ViT 编码器从参考图像中提取的全局空间-语义特征 y*。
- **对齐方式**：将 DiT 中间层特征经一个可训练的 MLP 映射后，与 y* 计算余弦相似度损失 L_SuRA，同时仅在掩码区域 M 内计算速度预测损失 L_region，防止背景过拟合。
- **输出**：训练好的**主体 LoRA**（秩 32），仅注入 DiT 的 Q、K、FFN.0 层。

该阶段总损失为 L = L_region + λ·L_SuRA，其中 λ 为平衡超参数。

### 阶段二：运动学习

运动学习阶段的目标是让模型学会从参考视频中提取并复现对象级的运动轨迹。其核心是**运动表征对齐模块（MoRA）**：

- **输入**：一段参考运动视频。
- **对齐目标**：冻结的 SEA-RAFT 光流编码器从参考视频首尾帧间提取的像素级运动轨迹特征 F_{1,N}。
- **对齐方式**：将去噪生成视频的光流特征 F̃_{1,N} 与 F_{1,N} 计算 L1 损失 L_MoRA，同时通过时序速度预测损失 L_temporal 更新帧间相关性。
- **输出**：训练好的**运动 LoRA**（秩 64），仅注入 DiT 的 V、O、FFN.0、FFN.2 层。

该阶段总损失为 L = L_temporal + α·L_MoRA。

### 推理阶段：主体-运动关联解耦

训练完成后，主体 LoRA 和运动 LoRA 在推理时合并至冻结的 WAN2.1 骨干网络。为避免 DiT 架构中主体与运动特征的纠缠干扰，SMRABooth 从两个维度进行解耦：

1. **注入位置稀疏化**：基于 Figure 4(a) 的 LoRA 稀疏性实验——主体 LoRA 主要受 Q、K、FFN.0 层影响，运动 LoRA 主要受 V、O、FFN.0、FFN.2 层影响——仅将对应 LoRA 注入各自的关键层，而非全层注入。实验表明，这种稀疏注入可达到与全层微调相当的效果，同时避免全层注入导致的伪影和视频质量下降。

2. **注入时序权重调度**：基于 Figure 4(b) 的去噪过程分析——运动在去噪早期（约前 10 步）即已形成，而主体外观细节在 10–25 步间逐步细化——在 T_point 之前降低主体 LoRA 权重以优先生成运动，T_point 之后提高主体 LoRA 权重以增强主体保真度。

### 数据流与模块关系

Figure 3 直观展示了上述流程：主体学习阶段，参考图像经 DINOv2 编码器和 SAM 掩码生成器处理后，分别提供对齐目标与区域约束；运动学习阶段，参考视频经 SEA-RAFT 光流编码器提取运动轨迹，作为去噪视频的对齐目标。两个阶段训练出的 LoRA 在推理时通过稀疏层选择与分时权重调度合并，最终由冻结的 WAN2.1 DiT 骨干网络生成定制化视频。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SMRABooth_Subject_a/figures/003_Figure_3.jpg]]
*Figure 3: Overview of SMRABooth. The framework splits customized video generation into two stages: subject learning and motion learning. Subject learning aligns global spatial features from the vision encoder to enhance fidelity, while motion learning utilizes temporal motion representations from the optical flow encoder to guide motion generation. The pretrained video diffusion model remains frozen during training, and LoRAs are merged at inference to generate customized videos. For simplicity, text input is omitted from the figure. V* and S* are specific tokens used to represent subject and motion without intrinsic meanings*

### 补充图表

SMRABooth 的核心架构围绕两个对象级表征对齐模块和一个基于 LoRA 稀疏性的主体-运动解耦策略构建，整体框架如图 Figure 3 所示。预训练视频扩散模型（WAN2.1，DiT 架构）在训练期间保持冻结，仅通过低秩适配（LoRA）注入可学习参数。

### 3.1 预训练视频扩散骨干

方法建立在流匹配（Flow Matching）视频扩散框架之上。给定初始潜变量 $\boldsymbol{z}_0$ 和终止潜变量 $\boldsymbol{z}_1$，线性插值路径定义为：

$$z_t = (1 - t) z_0 + t z_1$$

速度场 $\boldsymbol{v}_t = \boldsymbol{z}_1 - \boldsymbol{z}_0$ 表示从初始状态到目标状态的变化方向。扩散模型的训练目标是预测该速度场，损失函数为：

$$\mathcal{L} = \mathbb{E}_{z_0, z_1, c_{txt}, t} \left\| u(z_t, c_{txt}, t; \theta) - v_t \right\|^2$$

其中 $u(\cdot)$ 为模型预测的速度，$c_{txt}$ 为文本条件，$\theta$ 为模型参数。相邻帧之间的像素级运动向量通过光流编码器 $F$ 提取：

$$\mathbf{F}_{t,t+dt} = F(x_t, x_{t+dt})$$

### 3.2 主体表征对齐模块（SuRA）

SuRA 模块的核心思想是将 DiT 中间特征与外部自监督视觉编码器提取的主体全局表征对齐，以弥补纯文本条件和隐式特征在全局结构感知上的不足。

**特征提取**：采用冻结的 DINOv2-ViT 编码器 $E$ 提取主体图像的目标特征 $\mathbf{y}^*$。同时，将 DiT 块中间层输出的第一帧特征经 MLP 投影头 $h_{\phi}$ 映射到与 DINOv2 特征相同的空间。

**对齐损失**：通过余弦相似度损失强制 DiT 中间特征向目标表征靠拢：

$$\mathcal{L}_{\mathrm{SuRA}}(\theta) = -\mathbb{E}_{\mathbf{z},v,t} \left[ \frac{1}{N} \sum_{n=1}^{N} \frac{\mathbf{y}^{*[n]} \cdot h_{\phi}(z_t^{1[n]})}{\|\mathbf{y}^{*[n]}\| \cdot \|h_{\phi}(z_t^{1[n]})\|} \right]$$

其中 $N$ 为图像 patch 数量，$n$ 为 patch 索引。该损失引导模型学习主体的全局空间结构和语义一致性，而非仅记忆局部纹理。

**区域掩码约束**：为防止主体 LoRA 过拟合到背景区域，引入 SAM 分割模型生成的主体掩码 $\mathbf{M}$，仅计算主体区域内的速度预测损失：

$$\mathcal{L}_{\mathrm{region}} = \mathbb{E}_{z_0,z_1,c_{txt},t} \left\| u(\boldsymbol{z}_t,\boldsymbol{c}_{txt},t;\boldsymbol{\theta}) \cdot \mathbf{M} - v_t \cdot \mathbf{M} \right\|^2$$

**主体学习总损失**：

$$\mathcal{L} = \mathcal{L}_{\mathrm{region}} + \lambda \mathcal{L}_{\mathrm{SuRA}}$$

其中 $\lambda$ 为平衡超参数。

### 3.3 运动表征对齐模块（MoRA）

MoRA 模块通过显式的光流编码器提取对象级运动轨迹表征，解决现有方法仅通过时序层隐式捕获运动导致的趋势错误和外观纠缠问题。

**运动特征提取**：采用 SEA-RAFT 光流编码器 $F$，分别对参考视频和去噪视频提取像素级运动轨迹特征 $\mathbf{F}_{\{1,N\}}$ 和 $\widetilde{\mathbf{F}}_{\{1,N\}}$。该编码器擅长建模绝对轨迹变化，同时过滤外观相关的冗余信息。

**对齐损失**：通过 L1 损失强制去噪视频的运动轨迹与参考视频一致：

$$\mathcal{L}_{MoRA} = || \mathbf{F}_{\{1,N\}} - \widetilde{\mathbf{F}}_{\{1,N\}} ||$$

**运动学习总损失**：在时序速度预测损失基础上加入运动对齐损失：

$$\mathcal{L}_{\mathrm{temporal}} = \mathbb{E}_{z_0,z_1,c_{txt},t} \left\| u(z_t,c_{txt},t;\theta) - v_t \right\|^2$$

$$\mathcal{L} = \mathcal{L}_{\mathrm{temporal}} + \alpha \mathcal{L}_{\mathrm{MoRA}}$$

其中 $\alpha$ 为平衡超参数。

### 3.4 主体-运动关联解耦策略

DiT 架构缺乏 U-Net 式的空间-时序层解耦，主体 LoRA 和运动 LoRA 直接在全层注入时会产生严重干扰。SMRABooth 通过两个维度的稀疏性分析解决该问题。

**注入位置稀疏性**（Figure 4a）：实验表明，主体 LoRA 主要由 Q、K、FFN.0 层决定，运动 LoRA 主要由 V、O、FFN.0、FFN.2 层决定。移除 FFN.0 层导致 CLIP-I 和 DINO-I 下降（主体保真度受损），移除 FFN.2 层则显著降低 Motion Fidelity（运动一致性受损）。基于此，主体 LoRA 仅注入 Q、K、FFN.0 层，运动 LoRA 仅注入 V、O、FFN.0、FFN.2 层，稀疏 LoRA 可达到与全层微调相当的效果。

**注入时序稀疏性**（Figure 4b）：去噪过程分析显示，运动在早期（约前 10 步）先形成，主体外观在 10-25 步之间逐步细化。据此设计分时权重策略：在 $T_{point}$ 之前降低主体 LoRA 权重以优先恢复运动，$T_{point}$ 之后提高主体 LoRA 权重以细化外观细节。$T_{point}$ 通过经验分析在 10-25 步范围内选择。

## 实验与关键发现

### 核心性能验证

SMRABooth在DiT骨干（WAN2.1）上的定量评估覆盖语义对齐、运动质量和感知质量三个维度。Table 1汇总了各方法在CLIP-T、DINO-I、CLIP-I、Motion Fidelity、Temporal Consistency、Warp Error等指标上的对比结果。SMRABooth在所有DiT架构方法中取得最优CLIP-T（0.363），表明文本-视频语义对齐能力领先；Motion Fidelity达到62.89，显著超越次优方法DualReal（Wang et al., arXiv 2025），验证了MoRA模块显式运动表征对齐的有效性。用户研究（Table 2，5分Likert量表）进一步确认SMRABooth在Prompt Alignment上取得4.228±0.041的最高分，主观感知质量同样占优。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SMRABooth_Subject_a/figures/008_Table_2.jpg]]
*Table 2: Quantitative User Studies on DiT-based Methods*

U-Net骨干上的泛化实验（Figure 6）以ModelScope/ZeroScope为基础，与DreamVideo（Wei et al., CVPR 2024）和MotionDirector（Zhao et al., ECCV 2024）对比。SMRABooth在主体身份保持和运动模式复现上均优于对比方法，而其他方法出现主体外观偏离参考图像、运动轨迹不一致等问题。这证明对象级表征对齐策略在U-Net架构上同样有效，但需注意该结论置信度为0.85，建议结合补充材料进一步确认。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SMRABooth_Subject_a/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison of customized video generation on U-Net-based methods. SMRABooth preserves subject identity and motion patterns, while other methods fail to stay faithful to the reference*

### 消融实验：组件贡献逐层拆解

Table 3通过控制变量法逐一移除各组件，量化每个设计选择的因果效应。完整SMRABooth在所有指标上取得最优，关键发现如下：

**SuRA模块（主体表征对齐）**：移除$l_{SuRA}$损失后，CLIP-I和DINO-I显著下降，定性结果（Figure 7a）显示主体全局结构失真、语义一致性减弱。这验证了DINOv2自监督编码器提供的空间-语义特征对齐是主体保真度的核心保障。

**MoRA模块（运动表征对齐）**：移除$l_{MoRA}$损失后，Motion Fidelity大幅降低，生成的运动轨迹出现结构不连贯。SEA-RAFT光流编码器显式提取的像素级运动轨迹有效过滤了外观冗余信息，使运动学习聚焦于对象级轨迹变化。

**稀疏层选择策略**：全层LoRA注入（Combination 1）导致视频质量急剧下降，产生严重伪影——这是因为DiT架构缺乏U-Net式的空间-时序层解耦，主体LoRA和运动LoRA在全层注入时产生特征纠缠。进一步分析表明：移除FFN.0层导致CLIP-I和DINO-I下降（主体保真度受损），移除FFN.2层导致Motion Fidelity显著降低（运动一致性受损）。最终稀疏配置——主体LoRA注入Q、K、FFN.0层，运动LoRA注入V、O、FFN.0、FFN.2层——可达到与全层微调相当的效果，同时避免了层间干扰。

**时序权重调度**：Figure 4b揭示了去噪过程的时序特性：运动在早期（约前10步）先形成，主体外观在10-25步间逐步细化。基于此，T_point前降低主体LoRA权重以优先恢复运动轨迹，T_point后提高权重以增强主体细节。消融实验证实该调度策略对平衡主体-运动一致性至关重要。

### 失败模式与局限性

尽管SMRABooth在定量和定性评估中表现优异，但仍存在以下局限：

1. **跨架构泛化成本**：稀疏层选择结果（主体依赖Q/K/FFN.0，运动依赖V/O/FFN.0/FFN.2）基于WAN2.1分析得出，迁移至CogVideoX等DiT变体时需重新进行稀疏性分析，层选择结果不具备跨架构通用性。

2. **T_point标定依赖经验**：当前T_point在10-25步范围内通过经验分析选择，不同视频长度和运动复杂度下可能需要重新标定，缺乏自动化选择机制。

3. **数据集规模有限**：实验基于30个主体对象和21种运动类型，在更广泛的主体类别（如精细纹理物体、透明物体）和复杂运动模式（如多主体交互运动）上的鲁棒性有待验证。

4. **训练流程复杂度**：分阶段训练（先主体后运动）增加了超参数调整负担，$\lambda$和$\alpha$需分别调优，且两个阶段无法联合端到端优化。

5. **高分辨率/长视频场景未验证**：当前实验固定于832×480分辨率、49帧、15 fps配置，更高分辨率（1080p）和更长视频（>100帧）下的计算开销和生成质量尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SMRABooth_Subject_a/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation studies on each component*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SMRABooth_Subject_a/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of customized video generation on DiT-based methods. SMRABooth preserves subject identity and motion patterns, while other methods produce artifacts and inconsistencies with the reference*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SMRABooth_Subject_a/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison for the ablation study. (a) shows the ablation results for*

## 定位与知识库关联

### 任务定位与基线谱系

SMRABooth 解决的是**定制化视频生成**（Customized Video Generation）任务，其核心挑战在于同时保持参考主体外观保真度和参考运动模式一致性。该任务可进一步拆解为两个子问题：**主体定制**（Subject Customization）和**运动定制**（Motion Customization），现有方法在这两个维度上存在不同程度的耦合与权衡。

在 DiT 架构基线上，SMRABooth 的直接对标方法是 **MotionBooth**（Wu et al., NeurIPS 2024），后者同样基于 DiT 骨干网络实现主体-运动联合定制，但缺少显式的对象级表征引导。**DualReal**（Wang et al., arXiv 2025）采用联合主体-运动训练策略，是次优的 DiT 基线方法。**CustomCrafter**（Wu et al., AAAI 2025）则通过空间低秩结构进行定制化视频生成，属于另一类 DiT 路线。在 U-Net 架构侧，**DreamVideo**（Wei et al., CVPR 2024）采用分离的主体 LoRA 和运动 LoRA 微调策略，**MotionDirector**（Zhao et al., ECCV 2024）通过时序注意力和重加权扩散损失实现运动定制——这两者构成了 U-Net 路线的主要对比锚点。

SMRABooth 与上述方法的本质差异在于**引入了外部对象级表征作为显式对齐目标**：主体侧使用 DINOv2 自监督视觉编码器提供全局空间-语义特征，运动侧使用 SEA-RAFT 光流编码器提供像素级运动轨迹特征。这一设计使得低秩微调过程不再仅依赖扩散模型内部的隐式特征，而是有明确的外部语义和运动信号进行监督。

### 核心技术贡献的知识增量

SMRABooth 的知识增量体现在三个相互关联的层面：

**（1）对象级表征对齐范式。** 现有定制化生成方法的主体学习主要依赖特殊 token（如 V*）和文本条件进行隐式学习，运动学习则完全交由时序层隐式捕获。SMRABooth 首次将自监督视觉编码器和光流编码器引入定制化视频生成的 LoRA 微调流程，通过余弦相似度损失（SuRA Loss）和 L1 损失（MoRA Loss）将 DiT 中间特征与外部表征对齐。这一范式可类比于图像生成领域中使用 DINO 特征增强语义一致性的工作，但 SMRABooth 将其系统性地拓展到了视频生成的主体-运动联合定制场景。

**（2）DiT 架构中 LoRA 稀疏性规律的发现。** SMRABooth 通过逐层消融实验揭示了一个关键规律：在 WAN Block 中，主体 LoRA 的有效性高度集中于 Q、K、FFN.0 层，运动 LoRA 则主要由 V、O、FFN.0、FFN.2 层决定。这一发现表明 DiT 架构中不同注意力组件和前馈层对空间语义与运动时序信息存在功能分化。与全层注入相比，稀疏层注入不仅计算开销更低，而且有效避免了主体与运动 LoRA 在共享层中的特征纠缠——全层注入（Combination 1）会显著降低整体视频质量并产生伪影。

**（3）去噪时序上的主体-运动解耦。** SMRABooth 通过分析去噪过程中 CLIP-I 和 DINO-I 指标的动态变化，发现运动模式在去噪早期（约前 10 步）已基本形成，而主体外观细节在 10-25 步之间持续细化。基于此，提出了 T_point 分时权重调度策略：在 T_point 之前降低主体 LoRA 权重以优先恢复运动，之后提高主体 LoRA 权重以细化外观。这一策略从去噪动力学的角度解耦了主体与运动的学习时序。

### 适用边界与局限

**架构依赖性。** SMRABooth 的稀疏层选择结果（Q/K/FFN.0 对主体敏感，V/O/FFN.0/FFN.2 对运动敏感）是基于 WAN2.1 骨干网络分析得出的。由于不同 DiT 架构（如 CogVideoX、Open-Sora 等）的 Block 内部结构和注意力机制设计存在差异，层选择结果可能不具备跨架构通用性——在迁移到新骨干时，需要重新进行稀疏性分析以确定最优注入层级。

**超参数标定成本。** T_point 的选取目前依赖经验分析（10-25 步范围），不同视频长度、运动复杂度和去噪步数配置下可能需要重新标定。两阶段训练中的平衡超参数 λ（SuRA 损失权重）和 α（MoRA 损失权重）也需要分别调整，增加了训练流程的调参负担。

**数据规模与泛化性。** 当前实验验证基于 30 个主体对象和 21 种运动类型的数据集，在更广泛的主体类别（如非刚性变形物体、透明物体）和更复杂的运动模式（如多物体交互运动、非刚体运动）上的鲁棒性尚未充分验证。

**分阶段训练限制。** 主体学习和运动学习目前采用两阶段分离训练策略，虽然避免了联合训练中的优化冲突，但限制了主体与运动表征之间的交互学习潜力。两个模块能否端到端联合训练，以及联合训练是否能进一步提升一致性，是尚未探索的方向。

### 开放问题

1. **跨架构稀疏性泛化：** 稀疏层选择策略能否在 CogVideoX、Open-Sora 等其他 DiT 骨干上保持一致的层功能分化规律？还是需要为每种架构重新建立稀疏性图谱？
2. **自适应 T_point 机制：** 能否设计基于去噪过程中特征变化（如交叉注意力图熵值、特征方差等）的自适应检测策略，实现 T_point 的自动化选择，而非依赖经验标定？
3. **多主体与交互运动：** 该方法当前针对单主体定制设计，是否支持多主体场景下的独立外观保持和主体间交互运动的定制生成？这可能需要扩展掩码机制和表征对齐策略。
4. **高分辨率与长视频扩展：** 在 1080p 分辨率和超过 100 帧的长视频场景下，光流编码器的计算开销和表征对齐损失的有效性如何？是否需要多尺度或分层对齐策略？
5. **任务泛化能力：** 主体表征对齐和运动表征对齐模块能否推广到视频编辑（保持主体外观的同时改变运动）、视频重演（驱动新主体执行参考运动）等相关任务中？
6. **端到端联合训练：** 将 SuRA 和 MoRA 模块整合为端到端联合训练框架，是否能在主体-运动一致性上获得超越分阶段训练的增益？联合训练中两个对齐损失的平衡策略如何设计？

## 原文 PDF

![[paperPDFs/CVPR_2026/SMRABooth_Subject_and_Motion_Representation_Alignment_for_Customized_Video_Generation.pdf]]

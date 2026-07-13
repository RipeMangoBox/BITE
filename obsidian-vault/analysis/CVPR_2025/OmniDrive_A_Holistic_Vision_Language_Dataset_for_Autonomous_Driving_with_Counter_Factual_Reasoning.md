---
title: "OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counter Factual Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/OmniDrive_A_Holistic_Vision_Language_Dataset_for_Autonomous_Driving_with_Counter_Factual_Reasoning.pdf
project_link: null
code_link: https://github.com/NVlabs/OmniDrive
aliases:
- OOLOQA
- OmniDrive
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入基于反事实推理的数据集（OmniDrive），通过模拟替代轨迹和规则检查生成密集的QA对，将语言推理与规划轨迹对齐。"
primary_logic: "利用模拟轨迹的反事实推理可有效识别关键交通元素，并以结构化方式简化3D场景表示，使GPT-4能够生成高质量的3D驾驶问答数据，从而增强模型的3D理解与决策能力。"
claims:
- "OmniDrive 通过反事实推理生成高质量 QA 数据，将规划轨迹与语言推理建立起更紧密的联系。"
- "反事实清单利用规则验证碰撞、闯红灯等场景，并结合 GPT-4 评估安全性与合规性。"
- "在 DriveLM Q&A 基准和 nuScenes 开环规划上，使用 OmniDrive 预训练带来了显著提升。"
- "基于 VLM 对齐的 Omni-L 在规划中碰撞率更低（1.90%），优于基于 3D 感知集成的 Omni-Q（3.79%），揭示 2D VLM 向 3D 迁移的潜力。"
---

# OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counter Factual Reasoning

> [!tip] 核心洞察
> 利用模拟轨迹的反事实推理可有效识别关键交通元素，并以结构化方式简化3D场景表示，使GPT-4能够生成高质量的3D驾驶问答数据，从而增强模型的3D理解与决策能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OmniDrive：一种面向自动驾驶的整体视觉语言数据集，利用反事实推理 |
| 英文题名 | OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counter Factual Reasoning |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2405.01533) · [GitHub](https://github.com/NVlabs/OmniDrive) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OmniDrive (with Omni-L and Omni-Q agents) |
| Dataset | DriveLM Q&A benchmark, nuScenes open-loop planning, OmniDrive counterfactual reasoning (safety) |

> [!tip] 效果简介
> - DriveLM Q&A benchmark 上，Score 为 0.58 (Omni-L w/ OmniDrive + LLaVA665k pretraining)，对比 0.53 (w/o OmniDrive pretraining)，变化 +0.05。
> - nuScenes open-loop planning 上，Collision (%)↓ Avg. 为 1.90 (Omni-L)，对比 3.22 (Omni-L w/o OmniDrive data)，变化 -1.32。
> - OmniDrive counterfactual reasoning (safety) 上，Precision (%) 为 72.1 (Omni-L)，对比 68.6 (Omni-Q)，变化 +3.5。

## 概要

### 问题与瓶颈

当前自动驾驶视觉语言模型（VLM）面临一个核心瓶颈：**监督信号稀疏**。现有方法主要依赖专家驾驶轨迹作为唯一的监督来源，然而轨迹本身仅提供了“如何开”的稀疏信息，无法捕捉驾驶决策背后复杂的因果推理过程。这导致模型难以将 2D 视觉-语言推理能力有效迁移至 3D 空间理解与规划任务中。

### 核心思想

本文提出 **OmniDrive**，一个面向自动驾驶的整体视觉语言数据集，其核心创新在于引入**反事实推理** 机制来生成密集的监督信号。具体而言，该方法利用模拟轨迹生成替代驾驶方案，并通过规则化清单与 GPT-4 对这些替代轨迹进行安全性评估，从而自动生成涵盖场景描述、注意力、推理与规划的高质量问答对。这一策略将语言推理与规划轨迹紧密对齐，有效弥补了专家轨迹监督稀疏的缺陷。

### 方法定位

OmniDrive 在方法谱系上属于**数据驱动的 VLM 对齐方案**，其定位介于以下两条技术路线之间：

- **2D VLM 向 3D 迁移**：以 **Omni-L** 为代表，在 LLaVA 架构基础上扩展多图输入，引入可学习的 3D 位置编码，通过 MLP 投影实现视觉-语言对齐。
- **3D 感知集成 VLM**：以 **Omni-Q** 为代表，基于 BEV 感知架构（如 StreamPETR），利用检测查询与载体查询的 Q-Former 设计，将 3D 检测任务监督融入 VLM 训练。

相较于纯规划基线如 **ST-P3** (Hu et al., NeurIPS 2022)、**UniAD** (Hu et al., CVPR 2023) 和 **VAD-Base** (Jiang et al., arXiv 2023)，OmniDrive 的独特贡献在于通过反事实推理数据生成，将规划与语言推理统一于同一训练框架，而非将二者分离处理。

### 主要结果

在 **DriveLM Q&A 基准**上，使用 OmniDrive 预训练后，Omni-L 的得分从 0.53 提升至 0.58，验证了反事实推理数据对语言推理能力的增益。在 **nuScenes 开环规划**任务中，Omni-L 的碰撞率降至 1.90%，显著优于未使用 OmniDrive 数据的 3.22%。值得注意的是，基于 VLM 对齐的 Omni-L 在反事实推理安全性任务上的精确率达到 72.1%，优于基于 3D 感知集成的 Omni-Q (68.6%)，揭示了 2D VLM 向 3D 安全推理迁移的潜力。

### 局限与开放问题

当前工作存在两点主要局限：其一，反事实模拟尚未考虑其他交通参与者对自车行为的动态响应；其二，开环评估对自车状态存在内禀偏置，且场景复杂度有限，可能过拟合专家轨迹。开放问题包括：反事实推理相对于标准专家轨迹监督的量化增益边界、GPT-4 在边缘情况下的推理可靠性，以及闭环规划场景下 OmniDrive 代理模型的交互式安全表现。



自动驾驶系统的核心挑战之一在于，智能体不仅需要精准感知周围环境，更需具备对复杂交通场景的深层理解与安全决策能力。近年来，视觉语言模型（VLMs）在二维图像理解与推理任务中展现出强大潜力，然而将其迁移至自动驾驶的三维空间理解与规划任务时，仍面临显著瓶颈。

**核心瓶颈：稀疏监督与三维推理鸿沟。** 现有自动驾驶视觉语言模型主要依赖专家驾驶轨迹作为监督信号。这种监督方式存在天然缺陷：专家轨迹仅提供“如何操作”的稀疏示范，无法揭示“为何如此决策”的深层推理过程。当模型仅模仿轨迹而缺乏对场景因果关系的理解时，其面对长尾场景的泛化能力与安全性均难以保障。更关键的是，二维 VLM 的推理能力与三维空间规划之间存在天然鸿沟——模型难以将图像平面的语义理解有效映射至鸟瞰视角下的时空轨迹规划。

**现有数据集的局限。** 当前主流的自动驾驶问答数据集多聚焦于二维场景描述或简单问答，缺乏将语言推理与三维规划轨迹对齐的机制。这导致模型在回答“前方车辆为何减速”等描述性问题时表现尚可，但在“本车应如何安全变道”这类需要空间推理与决策的问题上捉襟见肘。

**核心洞见：反事实推理驱动密集对齐。** OmniDrive 的核心动机在于，通过引入反事实推理机制，将稀疏的专家轨迹转化为密集的问答对，从而在语言推理与规划轨迹之间建立因果联系。其关键思路是：利用模拟替代轨迹，通过规则化清单验证碰撞、闯红灯等关键安全事件，并结合 GPT-4 评估驾驶行为的安全性与合规性，进而识别出影响决策的关键交通元素。这种机制不仅提供了丰富的监督信号，还以一种结构化方式简化了三维场景表示，使语言模型能够生成高质量的三维驾驶问答数据，最终增强模型的 3D 理解与决策能力。



## 核心方法与创新机理

OmniDrive 的核心创新在于通过**反事实推理（counterfactual reasoning）** 将稀疏的专家轨迹监督转化为密集的视觉语言问答对，从而将语言推理与规划轨迹在 3D 空间中建立起紧密的对齐关系。这一思路直接回应了现有自动驾驶视觉语言模型的核心瓶颈：监督信号过于稀疏，难以捕捉复杂决策过程中的关键因果因素。

围绕这一中心思想，OmniDrive 在**监督信号设计**和**模型架构对齐**两个维度上引入了实质性的 changed slots。

### 1. 监督信号：从稀疏轨迹到反事实密集 QA

传统方法仅依赖专家轨迹作为监督信号，这只能告诉模型“该怎么做”，却无法解释“为什么这么做”以及“不这么做会怎样”。OmniDrive 通过以下机制将监督信号从稀疏升级为密集：

- **反事实轨迹模拟**：基于 nuScenes 和 OpenLane-v2 的 3D 标注，生成偏离实际行驶路径的替代轨迹。
- **规则化清单验证**：针对固定类别（如碰撞物体、碰撞道路边界、闯红灯），利用 3D 目标检测和道路拓扑标注进行规则检查，自动判定反事实轨迹的安全性与合规性。
- **GPT-4 语义评估**：将拼接后的多视图图像与上下文信息送入 GPT-4，由大模型分析驾驶行为的安全性，并生成四类结构化响应：场景描述、注意力区域、决策推理和规划指令。

这一 pipeline 的关键洞察在于：**利用模拟轨迹的反事实推理可有效识别关键交通元素，并以结构化方式简化 3D 场景表示，使 GPT-4 能够生成高质量的 3D 驾驶问答数据**。由此，原本仅提供“正确答案”的专家轨迹，被扩展为包含“错误答案及其后果”的对比性监督，显著增强了模型对 3D 空间理解与决策边界的感知能力。

### 2. 模型架构：两条对齐路径的差异化设计

OmniDrive 探索了两条将视觉语言模型与 3D 驾驶任务对齐的技术路线，分别对应不同的 changed slots：

**Omni-L：从 2D VLM 向 3D 的轻量扩展**

相对于 LLaVA 的单图 MLP 投影设计，Omni-L 引入了两个关键改动：

- **多图输入**：将 LLaVA 的单图输入扩展为多视图图像，通过 MLP 投影将多视图特征展平后送入 LLM。
- **可学习 3D 位置编码**：在多视图图像特征上叠加 3D 位置编码，且权重初始化为零。这一设计允许模型在训练过程中逐步学习 3D 空间信息，而不会在初期破坏预训练的 2D 视觉语言对齐。

该设计的核心优势在于**以最小架构改动实现 2D VLM 向 3D 场景的迁移**，实验表明其在反事实推理安全性任务上的精确率（72.1%）优于基于 3D 感知集成的 Omni-Q（68.6%），揭示了 2D VLM 在 3D 推理中的潜力。

**Omni-Q：从 3D 感知向语言空间的深度集成**

相对于标准 Q-Former 仅做视觉-文本对齐的设计，Omni-Q 在 BEV 感知架构上引入了双查询机制：

- **检测查询（detection queries）**：受 StreamPETR 启发，用于预测 3D 目标的类别与坐标，接受 3D 检测任务的显式监督。
- **载体查询（carrier queries）**：利用 3D 几何先验，通过自注意力与检测查询交换信息，再通过交叉注意力从多视图图像特征中收集信息。

两类查询之间的自注意力机制（公式见 Section 3.1）使感知信息与语言空间形成双向流通，从而增强了模型在碰撞检测等感知密集型任务上的召回率（72.6% vs Omni-L 的较低召回率）。

### 3. 两条路线的互补性与局限

Omni-L 与 Omni-Q 的设计哲学形成鲜明对比：前者从语言端向 3D 空间“生长”，后者从 3D 感知端向语言空间“对齐”。这种互补性在消融实验中得到了验证——移除 Omni-Q 的 3D 感知监督（No Object / No Lane）会导致所有指标下降，而 Omni-L 在安全推理上更优但在感知召回上较弱。这表明**更好的视觉-语言对齐有利于高层安全推理，而显式 3D 感知集成有利于底层感知精度**，如何将两者融合仍是一个开放问题。

此外，需要指出的是，当前反事实结果的模拟尚未考虑其他智能体对自车行为的动态响应，这限制了其在交互式场景中的泛化能力。开环评估本身也存在对自车状态的内禀偏置，可能过拟合专家轨迹。



![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_01533/figures/002_Figure_2.jpg]]
*Figure 2: The proposed counterfactual-based synthetic Q&A data generation pipeline integrates semantic key-frame selection, counterfactualbased checklist and prompt design, and human-in-the-loop quality checks to create high-quality Q&A pairs*

OmniDrive 构建了一套从数据生成到模型训练的整体框架，旨在弥合 2D 视觉-语言推理与 3D 驾驶任务之间的鸿沟。其核心思路是：**利用反事实推理生成密集的 QA 监督信号，替代传统稀疏的专家轨迹监督，从而将语言推理与规划轨迹对齐**（图 Figure 2）。

### 数据生成流水线

数据生成分为四个关键模块：

1. **面向规划的关键帧选择**：从 nuScenes 数据集中，首先提取前视图的 CLIP 嵌入，通过 K-means 聚类选取 20% 的聚类中心作为语义代表性帧。随后基于车辆未来轨迹再次进行 K-means 聚类（200 个中心），以捕捉停车、直行、左转、右转等不同驾驶行为模式。

2. **反事实清单与提示设计**：针对物体碰撞、道路边界碰撞、闯红灯等固定类别，利用 nuScenes 的 3D 检测标注和 OpenLane-v2 的中心线及道路元素拓扑标注进行规则化验证。在此基础上，将拼接的多视图图像（三张前视图与三张后视图分别拼接为两张图）输入 GPT-4，由 GPT-4 分析图像并评估驾驶行为的安全性与合规性（Table 1）。

3. **人机协同质量保证**：人工核验关键帧上生成的 QA 质量，迭代优化提示与清单设计，直至满足泛化要求。

4. **大规模数据迭代**：最终生成涵盖**场景描述、注意力、推理、规划**四种响应类型的密集 QA 对（Table 1 底部）。

### 代理模型架构

OmniDrive 探索了两条将视觉信息与语言空间对齐的技术路线（图 Figure 3）：

- **Omni-L**：从 2D VLM 出发向 3D 集成扩展。基于 LLaVA 架构，将单图 MLP 投影扩展为多图输入，对多视图图像特征进行展平处理，并引入**可学习的 3D 位置编码**（权重初始化为零），最终通过 MLP 层实现视觉-语言对齐后送入大语言模型。

- **Omni-Q**：从 3D BEV 感知出发向语言空间对齐。受 StreamPETR 的 BEV 架构启发，初始化**检测查询（detection queries）**和**载体查询（carrier queries）**，两者通过自注意力交换信息：
  
  $$(Q,K,V) = ([Q_c, Q_d], [Q_c, Q_d], [Q_c, Q_d]), \quad \tilde{Q} = \mathbf{Multi-headAttention}(Q,K,V).$$

  随后通过交叉注意力从加有 3D 位置编码的多视图图像特征中收集信息：
  
  $$(Q,K,V) = ([Q_c, Q_d], P_m + F_m, F_m), \quad \tilde{Q} = \mathbf{Multi-headAttention}(Q,K,V).$$

  其中检测查询预测类别与坐标，载体查询利用几何先验增强定位能力。该架构整体对齐 Q-Former 设计。

### 训练策略

两种模型均采用两阶段训练：

- **2D 预训练**：在通用视觉-语言数据上进行对齐预训练。
- **3D 微调**：在 OmniDrive 生成的驾驶 QA 数据上进行微调。

两个阶段均**仅计算文本生成损失**，不使用 BLIP-2 中的对比学习和匹配损失。

### 输入输出流

统一输入为多视图环视图像，经视觉编码器（EVA-02-L，通过掩码图像建模蒸馏 CLIP）提取特征后，分别经 Omni-L 的 MLP 投影或 Omni-Q 的 Q-Former 结构映射至语言嵌入空间，最终由大语言模型（LLaMA2-7B）完成文本生成，输出包括场景描述、注意力热区、推理链和规划决策等多类响应。



OmniDrive 提出两种互补的代理架构，分别从 3D 感知集成和 2D 视觉-语言对齐两个方向探索 VLM 在自动驾驶中的 3D 理解能力。两种架构共享相同的视觉编码器（EVA-02-L）和语言模型（LLaMA2-7B），差异集中在视觉-语言投影器的设计上。

### Omni-Q：基于 3D 感知集成的 Q-Former 架构

Omni-Q 从 3D BEV 感知视角出发，将 Q-Former 架构与 StreamPETR 的 BEV 检测范式相结合。其核心设计在于引入两类可学习查询向量——**载体查询**（carrier queries）$Q_c$ 和**检测查询**（detection queries）$Q_d$——并通过自注意力与交叉注意力机制实现多视图特征聚合与信息交换。

**查询间自注意力。** 载体查询与检测查询首先通过自注意力交换信息：

$$(Q,K,V) = ([Q_c, Q_d], [Q_c, Q_d], [Q_c, Q_d]), \quad \tilde{Q} = \mathbf{Multi\text{-}headAttention}(Q,K,V).$$

**查询到多视图特征的交叉注意力。** 随后，更新后的查询从加有 3D 位置编码的多视图图像特征中收集空间信息：

$$(Q,K,V) = ([Q_c, Q_d], P_m + F_m, F_m), \quad \tilde{Q} = \mathbf{Multi\text{-}headAttention}(Q,K,V).$$

其中 $F_m$ 为第 $m$ 个视角的图像特征，$P_m$ 为对应的 3D 位置编码。检测查询额外受 3D 检测任务监督，预测目标类别与坐标；载体查询则利用几何先验整合场景级信息，最终输入 LLM 进行文本生成。

### Omni-L：基于 2D VLM 的 3D 扩展

Omni-L 遵循 LLaVA 的 2D VLM 设计，将单图输入扩展为多视图输入。具体而言，多视图图像特征被展平后通过 MLP 投影器映射至语言嵌入空间，同时引入可学习的 3D 位置编码以注入空间先验。该位置编码的权重初始化为零，在训练过程中逐步习得有意义的空间表示。与 Omni-Q 的 Q-Former 相比，Omni-L 的投影器更为轻量，未显式建模 3D 检测任务。

### 训练策略

两种架构均采用两阶段训练：**2D 预训练**阶段使用通用视觉-语言数据（如 LLaVA665k）对齐视觉与语言空间；**3D 微调**阶段引入 OmniDrive 数据集和 3D 感知任务监督。两个阶段均仅计算文本生成损失，不使用 BLIP-2 中的对比学习与匹配损失。



## 实验与关键发现

### 3D 规划与推理的双轨评估

OmniDrive 的实验设计围绕两条主线展开：一是在标准自动驾驶规划基准上的定量对比，二是在自建反事实推理基准上的安全性评估。作者统一使用 **EVA-02-L** 作为视觉编码器、**LLaMA2-7B** 作为语言模型，并基于 BEV-Planner（Li et al., arXiv 2023）的复现设置进行公平比较。

**nuScenes 开环规划**（Table 2）是核心主战场。Omni-L 与 Omni-Q 的完整版本（含自车状态）在 L2 误差和碰撞率上均大幅超越传统基线。其中 **Omni-Q++** 取得了碰撞率 0.30%、路口违规率 3.00% 的最佳安全表现，而 **Omni-L++** 则在 L2 位移误差上更优（1s=0.15m, 2s=0.36m, 3s=0.70m, 平均 0.40m），表明 VLM 对齐路径在轨迹精度上具备竞争力。值得注意的是，ST-P3（Hu et al., NeurIPS 2022）的官方实现被指出使用了部分错误的真值标注，其数据点需谨慎解读。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_01533/figures/005_Table_2.jpg]]
*Table 2: Comparison on nuScenes Open-loop planning. For a fair comparison, we referred to the reproduced results in BEV-Planner [22]. †: The official implementation of ST-P3 (ID-0) utilized partial erroneous ground truth. ‡: The model was trained using only the trajectory prediction task for open-loop planning, without utilizing our generated OmniDrive Q&A data*

**DriveLM Q&A 基准**（Table 3）衡量模型的场景理解与语言推理能力。在加入 OmniDrive 预训练和 LLaVA665k 通用视觉问答数据后，Omni-L 的得分从 0.53 提升至 0.58（+0.05），验证了反事实推理数据对语言能力的正向迁移。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_01533/figures/006_Table_3.jpg]]
*Table 3: The performance of Omni-L on the DriveLM benchmark. We added pre-training with OmniDrive and LLaVA665k, which significantly improves performance*

**反事实推理安全性**（Table 4）是 OmniDrive 自建的评估维度。Omni-L 在安全性判断上的精确率达到 72.1%，优于 Omni-Q 的 68.6%（+3.5 个百分点），但在碰撞检测的召回率上略逊于 Omni-Q（72.6% vs Omni-L 的对应值）。这一差异揭示了两种架构的本质分工：**VLM 对齐路径（Omni-L）更擅长高层安全推理，而 3D 感知集成路径（Omni-Q）在感知层面的碰撞检测上更具优势**。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_01533/figures/007_Table_4.jpg]]
*Table 4: Analysis on OmniDrive counterfactual reasoning and open-loop planning (without ego status). P and R represent Precision and Recall respectively. “No Object” and “No Lane” indicate no corresponding 3D perception supervision in Omni-Q*

### 关键消融发现

**自车状态的杠杆效应**（Table 2）是最显著的单一因素。无论哪种模型架构，加入自车状态后 L2 误差和碰撞率均大幅下降。例如 Omni-L 的碰撞率从 3.22% 降至 1.90%，降幅达 1.32 个百分点。这揭示了开环评估的一个结构性偏置：模型可以从历史自车状态中学习到强先验，而非纯粹依赖场景理解做出规划决策。

**3D 感知监督的必要性**（Table 4）在 Omni-Q 上得到验证。移除目标检测监督（No Object）和车道线监督（No Lane）后，所有指标均出现下降，证实了 3D 感知任务对空间定位能力的支撑作用。

**架构选择的权衡**（Table 5）通过 BEV-MLP 基线得以量化。该基线在语言能力（CIDEr）和规划 AP 上均显著弱于 Omni-L/Q，说明简单的 BEV 特征到文本的映射不足以捕获复杂的驾驶语义。Omni-L 在规划碰撞率（1.90%）和语言指标上整体最优，而 Omni-Q 在路口违规率等感知相关指标上表现更好。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_01533/figures/008_Table_5.jpg]]
*Table 5: Analysis on nuScenes open-loop planning and OmniDrive counterfactual reasoning and language ability*

### 失败模式与已知局限

1. **开环评估的内禀偏置**：自车状态的强杠杆效应暗示模型可能过拟合专家轨迹的统计模式，而非真正理解场景语义。在简单场景下，依赖历史轨迹的惯性外推即可获得低误差，这削弱了开环指标对决策质量的区分力。

2. **反事实模拟的单向性**：当前的反事实推理仅考虑自车轨迹变化，未模拟其他交通参与者对替代行为的动态响应。这意味着生成的 QA 对可能高估了某些替代决策的安全性。

3. **Omni-Q 的安全推理短板**：尽管 Omni-Q 在 3D 感知上更精确，但其安全性精确率（68.6%）低于 Omni-L（72.1%），表明将 3D 感知特征有效映射到安全决策语言空间仍存在瓶颈。

4. **闭环验证缺失**：所有实验均在开环设定下完成，OmniDrive 数据集与代理模型在交互式闭环场景中的实际安全增益尚未被验证。



## 定位与知识库关联

### 与现有基线工作的关系

OmniDrive 在开环规划任务上与多条代表性基线进行了对比，所有复现结果均基于 **BEV-Planner**（Li et al., arXiv 2023）的统一设置以保证公平性（Table 2）。对比对象覆盖了从纯感知-规划集成到端到端学习的多个流派：

- **ST-P3**（Hu et al., NeurIPS 2022）和 **UniAD**（Hu et al., CVPR 2023）属于将感知、预测、规划统一为可微分管线的代表性工作。OmniDrive 在碰撞率和 L2 误差上均优于这些方法，但其核心差异在于 OmniDrive 引入了语言推理能力，而 ST-P3/UniAD 仅输出轨迹，缺乏可解释的决策链。需要注意的是，ST-P3 的官方实现使用了部分错误的真值标注，因此 Table 2 中的对比结果需谨慎解读。

- **VAD-Base**（Jiang et al., arXiv 2023）和 **BEV-Planner / BEV-Planner++**（Li et al., arXiv 2023）代表了基于矢量化场景表征的轻量规划方法。Omni-L++ 和 Omni-Q++ 在 L2 误差（1s/2s/3s）和碰撞率上均取得了有竞争力的结果，其中 Omni-Q++ 的碰撞率低至 0.30%（Table 2）。这表明在规划能力不降的前提下，OmniDrive 额外赋予了模型语言推理能力。

- **Ego-MLP**（仅使用自车状态）作为下界基线，揭示了自车状态信息对开环规划的显著偏置效应。加入自车状态后，所有模型的 L2 误差和碰撞率均大幅下降（Table 2），这暗示开环评估本身存在内禀偏置——模型可能过度依赖历史运动模式而非场景理解来预测轨迹。

在 VLM 架构层面，Omni-L 直接继承自 **LLaVA** 的单图 MLP 投影设计，核心改动在于将单图输入扩展为多视图输入，并引入可学习的 3D 位置编码（初始化为零）。Omni-Q 则借鉴了 **BLIP-2** 的 Q-Former 架构和 **StreamPETR** 的 BEV 感知设计，通过检测查询和载体查询实现 3D 感知与语言空间的对齐。

### 适用边界与关键局限

1. **开环评估的固有偏置**：nuScenes 开环规划基准对自车状态存在强依赖（Table 2 中 Ego Status 带来的提升佐证了这一点），且场景可能过于简单，容易过拟合专家轨迹。这意味着在开环指标上的提升未必能线性转化为闭环交互场景中的安全增益。

2. **反事实模拟的静态假设**：当前的反事实推理管线在模拟替代轨迹时，未考虑其他交通参与者对自车行为变化的动态响应。这一简化使得生成的反事实 QA 可能低估了真实交互场景中的级联风险。

3. **GPT-4 推理的可靠性边界**：反事实清单中的高层决策评估（安全性、合规性）依赖 GPT-4 的视觉推理能力，但论文未提供 GPT-4 在边缘情况下的量化准确率分析。对于罕见但高风险的场景，数据质量可能存在系统性偏差。

4. **3D 感知与语言空间的对齐鸿沟**：消融实验（Table 4）显示，移除 Omni-Q 的 3D 感知监督（No Object, No Lane）会导致所有指标下降，而 Omni-L 在反事实推理安全性任务上的精确率（72.1%）高于 Omni-Q（68.6%），但在碰撞检测召回率上略低（Table 4）。这表明两条技术路线各有侧重——VLM 对齐有利于安全推理，3D 感知集成有利于感知精度——但二者的最优融合方式仍是开放问题。

### 开放问题

- **反事实推理的量化增益**：相对于标准专家轨迹监督，反事实推理具体在哪些 3D 空间理解子任务上带来了显著提升？目前仅在整体指标上观察到改进，缺乏细粒度的归因分析。

- **闭环规划验证**：OmniDrive 数据集和代理模型在闭环规划下的表现如何？语言推理能力能否在交互式场景中真正提升安全性，而非仅在开环指标上体现优势？

- **3D 感知栈与语言空间的对齐**：如何更有效地将传统 3D 感知栈（检测、跟踪、建图）的几何先验注入 VLM，以同时获得感知精度和推理能力的提升？Omni-Q 的载体查询设计是初步尝试，但更系统的对齐机制仍有待探索。

- **反事实推理的保真度**：GPT-4 生成的替代轨迹和推理链在物理可行性和交通规则一致性上的量化保真度如何？是否存在系统性错误模式（如过度保守或过度激进）？



## 原文 PDF

![[paperPDFs/CVPR_2025/OmniDrive_A_Holistic_Vision_Language_Dataset_for_Autonomous_Driving_with_Counter_Factual_Reasoning.pdf]]

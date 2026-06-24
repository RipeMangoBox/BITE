---
title: "DriveCritic: Towards Context-Aware, Human-Aligned Evaluation for Autonomous Driving with Vision-Language Models"
type: paper
paper_level: A
venue: ICRA
year: 2026
pdf_ref: paperPDFs/ICRA_2026/DriveCritic_Towards_Context_Aware_Human_Aligned_Evaluation_for_Autonomous_Driving_with_Vision_Language_Models.pdf
aliases:
- DriveCritic
tags:
- ICRA_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入视觉语言模型（VLM）作为可微调的评估器，通过多模态输入（前向三摄图像、BEV地图、自车状态、EPDMS子分数）和两阶段强化学习训练，使评估器能够像人类一样综合考虑视觉与符号信息，做出上下文感知的偏好判断。"
primary_logic: "利用VLM的常识推理能力，将驾驶场景的视觉与符号线索映射到人类偏好，是克服规则化指标‘语境盲点’的关键；通过精心构造的成对偏好数据集和RLVR训练，VLM可以内化安全、进度与社会规范的复杂权衡，从而产生与专家高度对齐的评估。"
claims:
- "人类专家轨迹在EPDMS上不能获得满分，且EP和LK子分数明显偏低（navtrain EP 0.88, LK 0.90；navtest EP 0.87, LK 0.87），表明规则化指标无法完美反映人类偏好。"
- "DriveCritic在成对偏好测试集上达到76.0%的准确率，远超EPDMS的41.4%和零样本Qwen2.5-VL-7B的48.0%，证明微调VLM显著提升了与人类判断的对齐。"
- "消融实验显示，仅用强化学习（无监督预热）会降低准确率，而完整的SFT + DAPO + 格式与准确率奖励方案获得最高76.0%的准确率，说明两阶段训练和准确率奖励不可或缺。"
- "轨迹位置交换鲁棒性测试中，DriveCritic的鲁棒率（RR）达到81.8%，说明模型未过度依赖轨迹呈现顺序，保证了评估的客观性。"
---

# DriveCritic: Towards Context-Aware, Human-Aligned Evaluation for Autonomous Driving with Vision-Language Models

> [!tip] 核心洞察
> 利用VLM的常识推理能力，将驾驶场景的视觉与符号线索映射到人类偏好，是克服规则化指标‘语境盲点’的关键；通过精心构造的成对偏好数据集和RLVR训练，VLM可以内化安全、进度与社会规范的复杂权衡，从而产生与专家高度对齐的评估。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DriveCritic：面向自动驾驶的上下文感知、与人类对齐的视觉语言模型评估 |
| 英文题名 | DriveCritic: Towards Context-Aware, Human-Aligned Evaluation for Autonomous Driving with Vision-Language Models |
| 会议/期刊 | ICRA 2026 |
| Links | [paper](https://arxiv.org/abs/2510.13108); [Project](https://song-jingyu.github.io/DriveCritic) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DriveCritic |
| Dataset | DriveCritic test set |

> [!tip] 效果简介
> - DriveCritic test set 上，Accuracy 为 0.760，对比 0.414，变化 +0.346。
> - DriveCritic test set 上，Accuracy 为 0.760，对比 0.480，变化 +0.280。
> - DriveCritic test set 上，Accuracy 为 0.760，对比 0.645，变化 +0.115。

## 概述

### 问题背景

自动驾驶规划器的评估长期依赖规则化开环指标，其中**扩展预测驾驶模型得分（EPDMS）** 是当前最先进的开环评估指标（Cao et al., CoRL 2025）。EPDMS 通过将安全惩罚项乘积与轨迹质量子分数的加权平均相结合来量化驾驶表现：

$$\mathrm{EPDMS} = \left( \prod_{m \in \mathcal{M}_{\mathrm{pen}}} s_m \right) \cdot \frac{\sum_{m \in \mathcal{M}_{\mathrm{avg}}} w_m s_m}{\sum_{m \in \mathcal{M}_{\mathrm{avg}}} w_m}$$

然而，这类规则化指标存在根本性的“语境盲点”：它们无法识别人类驾驶员在复杂场景下的合理行为——例如为保持安全横向缓冲而进行的轻微车道微调，或因谨慎而采取的保守进度策略。实证证据表明，人类专家轨迹在 EPDMS 上无法获得满分：navtrain 分割上 EPDMS 仅为 0.92，navtest 上为 0.90；其中自车进度（EP）和车道保持（LK）子分数明显偏低（navtrain EP 0.88, LK 0.90；navtest EP 0.87, LK 0.87），揭示规则化指标与人类专家判断之间存在系统性偏差（Table I）。

### 核心方法

**DriveCritic** 提出了一种范式转换：将视觉语言模型（VLM）作为可微调的上下文感知评估器，替代硬编码规则。其核心洞见在于，VLM 的常识推理能力可以将驾驶场景的视觉与符号线索映射到人类偏好，从而克服规则化指标的语境盲点。

方法设计包含三个关键创新：

1. **多模态输入融合**：将前向三摄图像、BEV 地图叠加候选轨迹、自车状态以及 EPDMS 子分数（如 EP、LK）作为联合输入，使模型能够同时感知视觉场景和符号化驾驶质量信号。
2. **成对偏好评估范式**：将评估任务形式化为轨迹 A 与 B 的成对比较，输出结构化推理文本和偏好标签，而非单一的连续标量分数。
3. **两阶段训练流程**：先通过监督微调（SFT）在 GPT-5 生成的推理轨迹上预热模型，再通过强化学习微调（RLVR with DAPO）以格式遵从和准确率双重奖励进一步优化，使 VLM 内化安全、进度与社会规范的复杂权衡。

### 核心结论

在精心构造的 DriveCritic 成对偏好测试集上，**DriveCritic 达到 76.0% 的准确率**，显著超越所有基线方法：规则化 EPDMS 仅 41.4%，零样本 Qwen2.5-VL-7B 为 48.0%，监督学习分类器（ResNet-101）为 64.5%（Table IV）。消融实验证实，完整的 SFT + DAPO + 双重奖励方案是获得最优性能的关键——单独使用 RL 微调（无 SFT 预热）反而会降低准确率，而仅用格式奖励也会导致性能下降（Table V）。此外，轨迹位置交换鲁棒性测试中，DriveCritic 的鲁棒率达到 81.8%，表明模型未过度依赖轨迹呈现顺序，评估具有较好的客观性（Table VI）。

### 方法定位

DriveCritic 在方法谱系中处于**基于 VLM 的评估器**这一新兴方向，区别于传统规则化指标和纯监督学习分类器。其核心贡献在于证明了通过精心设计的偏好数据集和两阶段强化学习训练，VLM 可以被塑造为与人类高度对齐的驾驶评估器。然而，当前方法仍面临若干局限：数据集仅覆盖 NAVSIM 中的两种特定场景模式，泛化性有待验证；偏好标注由单一专家完成，可能存在主观偏差；VLM 推理的计算成本远高于规则化指标，制约大规模部署。

## 背景与动机

自动驾驶系统的闭环评估高度依赖开环指标来筛选候选规划器，因为在真实世界中穷举测试每一种驾驶场景既不安全也不经济。然而，当前最先进的开环评估指标——扩展预测驾驶模型得分（EPDMS，Cao et al., CoRL 2025）——虽然通过组合安全惩罚项与轨迹质量子分数实现了多维度量化，却暴露了一个根本性的“语境盲点”：它无法理解驾驶行为的上下文合理性。

这一缺陷的实证证据来自人类专家轨迹在EPDMS上的得分分析。如Table I所示，人类驾驶员在NAVSIM的navtrain和navtest两个子集上的EPDMS总分分别仅为0.92和0.90，远未达到理论满分。进一步拆解子分数发现，自车进度（EP）和车道保持（LK）两项指标明显偏低——navtrain上EP为0.88、LK为0.90，navtest上EP为0.87、LK为0.87。这意味着，即使是经验丰富的人类驾驶员所执行的安全、高效轨迹，也会被规则化指标系统性地“扣分”。

问题的根源在于EPDMS各子指标的硬编码阈值缺乏场景感知能力。以车道保持（LK）为例，其判定逻辑为：当车辆横向偏移车道中心超过0.5米且持续2秒以上时即触发违规。这一规则无法区分真正的危险偏离与人类驾驶员为保持安全横向缓冲而做出的合理微调。类似地，自车进度得分 $\mathrm{EP} = \min\left(1, \frac{d_{\mathrm{ego}}}{d_{\mathrm{ref}}}\right)$ 仅以自车前进距离与参考距离的比值衡量进度，完全忽略了场景中是否存在需要保守驾驶的合理因素（如视野遮挡、潜在风险等）。

Figure 1中的动机示例直观地展示了这一矛盾：轨迹A为与相邻车辆保持安全距离而短暂向左微调，这在上下文语境中是恰当且安全的操作；轨迹B虽然严格保持在车道线内，却因未做避让而进度过低。人类专家显然偏好轨迹A，但EPDMS却因A触发了车道保持惩罚而给出更低分数，最终错误地偏向轨迹B。

这种评估与人类判断的严重不一致带来了两个连锁风险：其一，在开环评测阶段，真正符合人类偏好的规划器可能被规则化指标错误地淘汰；其二，以EPDMS为优化目标的规划器可能学会“应试”行为——刻意避免任何触发惩罚的动作，即使这些动作在真实驾驶中是必要且安全的。

因此，本文的核心动机在于：构建一个能够像人类专家一样综合视觉场景信息与符号化指标、做出上下文感知偏好判断的评估器，从而填补规则化指标在“语境理解”上的根本性缺口。

## 核心创新

DriveCritic 的核心创新在于将自动驾驶轨迹评估从**硬编码规则空间迁移到可微调的视觉语言模型（VLM）空间**，从而赋予评估器上下文感知的类人判断能力。以下从评估器类型、输入模态、训练范式和输出形式四个维度，系统梳理其相对于现有基线的关键变化。

### 评估器类型：从规则化指标到可微调VLM

当前最先进的开环评估指标 **EPDMS**（Cao et al., CoRL 2025）完全依赖手工设计的规则——通过安全惩罚项乘积与轨迹质量子分数加权平均的复合公式计算标量得分。这一范式存在根本性局限：规则是静态的、上下文无关的，无法区分“真正的车道偏离”与“为保持安全横向缓冲而做出的合理微调”。

DriveCritic 将评估器替换为以 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）为骨干的 VLM。这一转变的本质是利用 VLM 在海量预训练中获得的常识推理能力，将驾驶场景的视觉与符号线索映射到人类偏好空间。实验证据强烈支持这一改变的有效性：零样本 Qwen2.5-VL-7B 在 DriveCritic 测试集上仅获得 48.0% 的准确率（Table V, row A），而经过领域微调后跃升至 76.0%（Table IV），证明**将通用 VLM 适配为领域评估器**是可行的技术路径，但领域微调不可或缺。

### 输入模态：从单一符号分数到多模态融合

EPDMS 的输入仅为符号化的子分数数值（如 LK、EP 等），完全忽略了驾驶场景的视觉上下文。DriveCritic 将输入扩展为四类多模态信息（Sec. IV-B.1; Fig. 2）：

1. **拼接三摄前视图**：提供自车前方的视觉场景信息；
2. **BEV 地图叠加候选轨迹**：在鸟瞰视角下分别叠加两条候选轨迹，呈现空间布局；
3. **自车状态**：速度、加速度等车辆动力学信息；
4. **EPDMS 子分数（EP 和 LK）**：保留规则化指标的数值信号作为辅助参考。

这一输入设计的关键在于**同时提供视觉场景和符号信号**，使 VLM 能够像人类专家一样综合考虑场景上下文（如“前方是否有障碍物需要微调避让”）与量化指标（如“偏离车道中心线的距离”），从而做出上下文感知的判断。Table I 的数据揭示了仅依赖符号分数的局限性：人类专家轨迹在 EPDMS 上的 EP 和 LK 子分数明显偏低（navtrain EP 0.88, LK 0.90；navtest EP 0.87, LK 0.87），说明规则化指标无法完美反映人类偏好，而多模态输入正是弥合这一差距的关键。

### 训练范式：两阶段微调实现人类对齐

DriveCritic 的训练采用**监督微调（SFT）+ 强化学习微调（RLVR with DAPO）**的两阶段策略（Sec. IV-B.2），这是将通用 VLM 转化为可靠评估器的核心机制：

- **SFT 阶段**：在 1,100 个样本上使用 GPT-5（OpenAI, 2025）生成的推理轨迹进行微调，预热模型的基本评估能力和推理格式。消融实验（Table V）表明，跳过 SFT 直接进行 RL 微调会导致准确率低于基础模型（row B vs A），说明 SFT 对稳定训练不可或缺。
- **RLVR 阶段**：采用 DAPO 算法，以格式遵从和准确率双重奖励进一步优化模型。Table V 的消融对比显示，在 SFT 基础上加入 RL 并使用准确率奖励（row D）比仅用格式奖励（row E）进一步提升准确率，最终完整方案（SFT + DAPO + 格式与准确率双重奖励）获得 76.0% 的最高准确率（row F）。

这一训练范式的核心洞察是：**SFT 提供稳定的初始策略，RLVR 通过偏好反馈进一步对齐人类判断**，二者缺一不可。

### 输出形式：从连续标量到结构化推理与偏好标签

EPDMS 输出单一连续标量分数，无法解释评估依据。DriveCritic 将评估任务形式化为**成对偏好判决问题**（Sec. IV-A），输出包含两部分：

1. **结构化推理文本**：模型生成对场景的分析推理，解释为何偏好某条轨迹；
2. **偏好标签**：明确给出“A 更优”或“B 更优”的判断。

这一输出形式的变化使评估过程**可解释**——如图 1 的动机示例所示，DriveCritic 能够识别轨迹 A 的微调是“为保持安全横向缓冲的上下文适当行为”，而非真正的车道偏离，并生成与人类专家相似的推理。此外，轨迹位置交换鲁棒性测试（Table VI）显示，DriveCritic 的鲁棒率达到 81.8%，说明模型未过度依赖轨迹呈现顺序，保证了评估的客观性。

### 创新总结

DriveCritic 的四项核心改变构成了一条完整的创新链条：**多模态输入提供上下文信息，VLM 骨干提供常识推理能力，两阶段训练实现人类偏好对齐，结构化输出保证可解释性与客观性**。这一链条使得评估器能够内化安全、进度与社会规范的复杂权衡，从而在成对偏好测试中以 76.0% 的准确率远超 EPDMS（41.4%）和零样本 VLM（48.0%）。

**需要手动验证的点**：当前数据集仅覆盖 NAVSIM 中的两种特定场景类型（车道-进度权衡与纯进度对比），模型在更广泛驾驶场景下的泛化能力尚未验证；偏好标注由单一领域专家完成，标注准则的普适性有待多评分者间信度分析确认。

## 整体框架

DriveCritic 的整体框架围绕一个核心洞察构建：**利用视觉语言模型（VLM）的常识推理能力，将驾驶场景的视觉与符号线索映射到人类偏好，是克服规则化指标“语境盲点”的关键**。该框架将自动驾驶轨迹评估重新定义为一个**成对偏好判断任务**，并通过精心设计的多模态输入和两阶段训练，使 VLM 评估器能够内化安全、进度与社会规范的复杂权衡。

### 框架总览

如图 2 所示，DriveCritic 框架由两个紧密耦合的部分组成：**DriveCritic 数据集**和 **DriveCritic 模型**。数据集从 NAVSIM 中采样并构造具有挑战性的场景，标注以成对的人类专家偏好；模型则接收丰富的多模态输入，经过两阶段微调后输出与人类对齐的评估决策。

### 多模态输入预处理

模型的条件输入由四部分构成，旨在为 VLM 提供与人类驾驶员判断相近的信息基础：

1. **拼接三摄前视图**：将前向三摄像头图像水平拼接，提供场景的视觉上下文。
2. **BEV 地图叠加候选轨迹**：在鸟瞰视角地图上分别叠加两条候选轨迹（A 和 B）的航点，使模型能够直观比较空间路径。
3. **自车状态**：包含速度、加速度等基本动力学信息。
4. **EPDMS 子分数**：仅提取 EP（自车进度）和 LK（车道保持）两个子分数作为符号化线索，因为这两个指标在人类专家轨迹上系统性地偏低（navtrain EP 0.88, LK 0.90；navtest EP 0.87, LK 0.87，见 Table I），是规则化评估失准的主要瓶颈。

### VLM 骨干与输出

框架采用 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）作为基础 VLM 骨干，处理上述多模态令牌并生成两阶段输出：
- **结构化推理文本**：模型首先生成自然语言推理，阐述其判断依据（如“轨迹 A 轻微向左调整以保持安全侧向缓冲，这在当前场景下是合理的”）。
- **成对偏好标签**：最终输出明确的偏好决策（A 更优或 B 更优），而非连续标量分数，从而直接对齐人类的比较判断模式。

### 两阶段训练流程

训练是框架的核心因果调节旋钮。DriveCritic 采用**监督微调（SFT）+ 强化学习微调（RLVR）**的两阶段策略：

**第一阶段：监督微调（SFT）**
- 使用 GPT-5（OpenAI, 2025）作为“教师模型”，在 1,100 个样本上生成推理轨迹。
- 以此对 Qwen2.5-VL-7B 进行 5 个 epoch 的微调（LoRA，学习率 1e-4，单设备批次大小 1），预热模型的基本评估能力。
- 消融实验表明，**仅用 RL 微调而无 SFT 预热会导致准确率低于基础模型**（Table V, row B vs A），说明 SFT 对稳定训练不可或缺。

**第二阶段：强化学习微调（RLVR + DAPO）**
- 在 RLVR 范式下，使用 EasyR1 库（基于 verl 框架）进行训练，配置为 16 块 NVIDIA A100 GPU、全局批次大小 256、rollout 数量 8、学习率 1e-6，共 4 个 epoch。
- 采用**双重奖励设计**：格式遵从奖励（确保输出结构正确）与准确率奖励（偏好预测是否正确）。
- 消融实验证实，在 SFT 基础上加入准确率奖励比仅用格式奖励进一步提升准确率（Table V, row D vs E），最终完整方案（SFT + DAPO + 格式与准确率双重奖励）获得 **76.0%** 的最高准确率（Table V, row F）。

### 偏好输出与评估闭环

训练完成后，DriveCritic 接收任意轨迹对的多模态输入，输出推理文本与偏好标签。这一输出可直接用于：
- 开环评估中对规划器轨迹进行与人类对齐的打分；
- 作为奖励信号反馈至端到端规划器的训练（文中将其列为开放问题）。

框架的鲁棒性通过轨迹位置交换测试得到验证：交换 A/B 顺序后，模型的鲁棒率（RR）达到 **81.8%**（Table VI），表明其未过度依赖轨迹呈现顺序，保证了评估的客观性。

### 关键设计选择与局限

| 设计维度 | 基线（EPDMS） | DriveCritic |
|---------|-------------|-------------|
| 评估器类型 | 硬编码规则 | VLM 微调 |
| 输入模态 | 仅符号化子分数 | 三摄图像 + BEV 地图 + 自车状态 + EP/LK 子分数 |
| 训练范式 | 无训练 | SFT + RLVR（DAPO） |
| 输出形式 | 连续标量分数 | 成对偏好标签 + 推理文本 |

当前框架的主要局限包括：数据集仅覆盖 NAVSIM 中两种特定场景（车道-进度权衡与纯进度对比），泛化性尚未在更多数据集上验证；偏好标注由单一领域专家完成，可能存在个人主观偏差；模型缺乏时序上下文，无法处理需要时序推理的动态场景；VLM 推理的计算成本远高于规则化指标，大规模部署时面临算力与能耗瓶颈。

## 核心模块与公式推导

### 规则化基线的结构缺陷：EPDMS 公式解析

当前开环评估的 SOTA 指标 **EPDMS**（Extended Predictive Driver Model Score，Cao et al., CoRL 2025）采用乘积-加权混合结构：

$$\mathrm{EPDMS} = \left( \prod_{m \in \mathcal{M}_{\mathrm{pen}}} s_m \right) \cdot \frac{\sum_{m \in \mathcal{M}_{\mathrm{avg}}} w_m s_m}{\sum_{m \in \mathcal{M}_{\mathrm{avg}}} w_m}$$

其中 $\mathcal{M}_{\mathrm{pen}}$ 为安全惩罚指标集合（如无碰撞 NC、驾驶方向合规 DDC），$s_m$ 为各子分数，$w_m$ 为加权权重。该公式的核心逻辑是：**安全违规通过乘法连乘直接“清零”总分**，而轨迹质量指标（如进度、舒适度）仅以加权平均形式贡献。

问题出在 $\mathcal{M}_{\mathrm{avg}}$ 中的两个关键子分数——**自车进度 EP** 和 **车道保持 LK**：

$$\mathrm{EP} = \min\left(1, \frac{d_{\mathrm{ego}}}{d_{\mathrm{ref}}}\right)$$

EP 以自车前进距离 $d_{\mathrm{ego}}$ 与参考距离 $d_{\mathrm{ref}}$ 的比值衡量进度，裁切至 $[0,1]$。LK 则检测自车是否在车道内无长时间偏离：当横向偏移 $d > 0.5\text{ m}$ 且持续超过 2 秒时触发违规惩罚。这两个指标的硬阈值设计使其**完全不具备上下文感知能力**——人类驾驶员为保持安全侧向缓冲而做出的短暂车道微调会被 LK 惩罚，在复杂场景下选择保守进度策略则会被 EP 压低分数。Table I 直接验证了这一点：人类专家轨迹在 navtrain 上 EP 仅 0.88、LK 仅 0.90，navtest 上 EP 0.87、LK 0.87，远未达到满分。

### DriveCritic 多模态输入管线

DriveCritic 将评估重新定义为**成对偏好判断问题**，其核心模块为多模态输入预处理管线（Fig. 2）：

1. **三摄前视图拼接**：将前向三摄像头图像拼接为单张宽幅视图，提供丰富的视觉上下文（道路几何、交通参与者、障碍物等）。
2. **BEV 地图叠加候选轨迹**：在鸟瞰视角地图上分别叠加两条候选轨迹 A 和 B 的路径点，使模型能够直接观察轨迹的空间形态。
3. **自车状态提取**：提取当前速度、朝向等自车状态信息作为符号化输入。
4. **EPDMS 子分数注入**：仅提取 EP 和 LK 两个子分数作为数值提示，而非使用完整 EPDMS 公式——这保留了规则化指标的信号，但将最终判断权交给 VLM 的上下文推理。

### 两阶段训练管线

DriveCritic 的训练分为两个关键阶段，消融实验（Table V）证明二者缺一不可：

- **监督微调（SFT）**：在 1,100 个样本上，使用 GPT-5 作为教师模型生成推理轨迹，对基础 VLM（Qwen2.5-VL-7B）进行 5 轮 LoRA 微调。此阶段让模型获得基本的评估推理能力，为后续强化学习提供稳定起点。Table V 显示，仅用 RL 而无 SFT 预热（ID B）的准确率甚至低于零样本基线（ID A），说明 SFT 对稳定训练不可或缺。

- **强化学习微调（RLVR + DAPO）**：采用 RLVR 范式，使用 DAPO 算法进行进一步优化。奖励函数包含两个分量：**格式奖励**（确保输出符合结构化推理格式）和**准确率奖励**（奖励与人类偏好一致的判断）。Table V 显示，在 SFT 基础上加入准确率奖励（ID D vs E）比仅用格式奖励进一步提升准确率，最终完整方案（SFT + DAPO + 双重奖励，ID F）达到 76.0% 的最高准确率。

### 鲁棒性保障机制

轨迹位置交换鲁棒性测试（Table VI）定义了鲁棒率指标：

$$\mathrm{RR} = \frac{1}{|D|} \sum_{i=1}^{|D|} \mathbb{I}[y^i = \hat{y}^{\bar{i}}]$$

其中 $y^i$ 为原始顺序下的预测标签，$\hat{y}^{\bar{i}}$ 为交换 A/B 轨迹位置后的预测标签。该指标衡量模型是否过度依赖轨迹呈现顺序而非轨迹本身的质量。DriveCritic 的 RR 达到 81.8%，表明模型在绝大多数情况下保持了评估的客观性。

## 实验与分析

### 核心实验结果

DriveCritic 在成对偏好测试集上取得了 **76.0%** 的准确率，大幅超越所有基线方法。这一结果验证了微调 VLM 作为上下文感知驾驶评估器的可行性。

**与规则化指标的对比**：当前 SOTA 开环指标 EPDMS（Cao et al., CoRL 2025）在同一测试集上仅获得 41.4% 的准确率（Table IV），几乎等同于随机猜测。这直接印证了核心瓶颈——规则化指标缺乏上下文感知能力，无法识别人类驾驶员在复杂场景下的合理行为（如为保持安全侧向缓冲而进行的轻微车道调整）。

**与零样本 VLM 的对比**：未经领域微调的 Qwen2.5-VL-7B（Bai et al., arXiv 2025）零样本准确率为 48.0%，GPT-5（OpenAI, 2025）零样本准确率为 64.5%。尽管 GPT-5 展现出一定的常识推理能力，但距离可用的评估精度仍有显著差距。DriveCritic 通过两阶段微调，将准确率分别提升了 28.0 和 11.5 个百分点，证明领域适配对于获得可靠的评估能力至关重要。

**与监督学习基线的对比**：基于 ResNet-101 编码器和 MLP 融合多模态特征的监督成对分类器准确率仅为 52.3%，远低于 DriveCritic。这表明简单的特征拼接和判别式训练无法有效捕获驾驶场景中需要常识推理的复杂偏好模式，VLM 的生成式推理能力在此任务中具有结构性优势。

### 消融实验：训练策略的因果作用

Table V 的系统消融揭示了各训练组件对最终性能的因果贡献：

| 配置 ID | SFT | RL 算法 | 奖励设计 | 准确率 |
|---------|-----|---------|----------|--------|
| A | ✗ | 无 | 无 | 48.0% |
| B | ✗ | GRPO | 格式+准确率 | 低于 A |
| C | ✓ | 无 | 无 | 显著提升 |
| D | ✓ | GRPO | 仅准确率 | 进一步提升 |
| E | ✓ | GRPO | 格式+准确率 | 进一步提升 |
| F | ✓ | DAPO | 格式+准确率 | **76.0%** |

**关键发现一：SFT 预热不可或缺。** 直接对基础 VLM 进行强化学习微调（配置 B）反而导致准确率下降，低于零样本基线。这说明 RL 探索在没有良好初始化时会破坏模型已有的常识推理能力。SFT 阶段通过 GPT-5 生成的推理轨迹（1100 个样本）为模型提供了稳定的评估“锚点”，是后续 RL 优化的必要前提。

**关键发现二：准确率奖励是核心驱动力。** 在 SFT 基础上，仅使用格式奖励的 RL 微调效果有限；加入准确率奖励后性能显著跃升（配置 D vs E）。这表明 RLVR 范式下，奖励信号必须直接对齐最终评估目标——偏好判断的正确性——而非仅约束输出格式。

**关键发现三：DAPO 优于 GRPO。** 在相同 SFT 预热和双重奖励条件下，DAPO 算法（配置 F）比 GRPO（配置 E）带来额外增益。DAPO 的动态采样策略可能更有效地探索了偏好空间的困难样本，从而提升了模型在边界案例上的判别能力。

### 鲁棒性分析

**轨迹顺序鲁棒性**（Table VI）：将测试集中每条样本的轨迹 A/B 位置交换后，DriveCritic 的鲁棒率（Robustness Rate, RR）达到 **81.8%**。RR 定义为交换前后预测一致的样本比例：

$$\mathrm{RR} = \frac{1}{|D|} \sum_{i=1}^{|D|} \mathbb{I}[y^i = \hat{y}^{\bar{i}}]$$

这一结果表明模型并未过度依赖轨迹呈现顺序，其偏好判断主要基于场景内容而非位置先验。然而，仍有约 18% 的样本在交换后预测翻转，说明模型在部分场景下存在一定的位置偏差，这可能是 VLM 固有的注意力模式或 SFT 数据中的标注模式所致。

### 人类专家轨迹的“不完美”得分

Table I 提供了理解规则化指标局限性的关键证据：人类专家轨迹在 EPDMS 上并未获得满分（navtrain 0.92, navtest 0.90），且 EP（自车进度）和 LK（车道保持）子分数明显偏低——navtrain 上 EP 为 0.88、LK 为 0.90，navtest 上 EP 为 0.87、LK 为 0.87。

这揭示了 EPDMS 的结构性缺陷：人类驾驶员在复杂场景下会主动进行车道微调（如避让路边障碍物）或采取保守进度策略（如路口减速观察），这些行为在规则化框架中被错误地惩罚为“车道偏离”或“进度不足”。DriveCritic 通过多模态输入（拼接三摄前视图、BEV 地图叠加候选轨迹、自车状态、EP/LK 子分数）和 VLM 的常识推理，能够区分“合理的上下文适应”与“真正的驾驶失误”，从而做出与人类专家一致的判断。

### 失败模式与局限性

尽管整体性能显著优于基线，DriveCritic 仍存在以下可识别的失败模式：

1. **时序上下文缺失**：模型仅使用静态 BEV 地图和子分数，无法处理需要时序推理的动态场景（如交通灯状态变化、运动交互）。在涉及多帧因果关系的场景中，评估准确率可能下降。

2. **场景覆盖有限**：训练数据仅来自 NAVSIM 数据集中的两种特定场景模式——车道-进度权衡（Case 1）和纯进度对比（Case 2）。在更丰富的驾驶场景（如复杂路口博弈、异常行为检测）上的泛化能力尚未验证。

3. **标注主观性风险**：偏好标注由单一领域专家完成，未进行多评分者间信度分析。在存在合理分歧的边界案例上，模型的“对齐目标”本身可能带有个人偏差。

4. **计算成本约束**：微调需 16 块 A100 GPU，推理需完整 VLM 前向传播。相比规则化指标的毫秒级计算，VLM 评估器的部署成本高出数个数量级，制约了大规模闭环评测中的实时应用。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2510_13108/figures/004_Table.jpg]]
*Table: II: Trajectory sampling pattern for the two focused case studies. Each sampled trajectory pair consists of the human trajectory and a vocabulary trajectory that matches the sub-scores pattern. The other subscores of the sampled trajectories are perfect. TABLE III: Number of trajectory pairs by split and data source. Case 1: lane-progress trade-off; Case 2: progress-only contrast*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2510_13108/figures/002_Table.jpg]]
*Table: I: EPDMS and sub-scores of human expert trajectories on the navtrain and navtest splits of NAVSIM. Abbreviations in Sec. III-A*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2510_13108/figures/006_Table.jpg]]
*Table: EPDMS: TABLE IV: Overall accuracy on the DriveCritic test set. “Fine-tuning” indicates whether the model was fine-tuned on DriveCritic data beyond its Trajectory A: it maintoriginal pretraining*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2510_13108/figures/007_Table.jpg]]
*Table: V: Ablation on the DriveCritic training recipe. Checkmarks (✓) indicate enabled components. ‘Acc.’ under Rewards denotes an accuracybased reward. Final column reports accuracy on the DriveCritic test set. ID legend: A = base Qwen2.5-VL-7B (zero-shot); B = GRPO only (format + accuracy rewards); C = SFT only; D = SFT + GRPO (accuracy reward); E = SFT + GRPO (format + accuracy rewards); F = SFT + DAPO (format + accuracy rewards)*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2510_13108/figures/008_Table.jpg]]
*Table: VI: Robustness under trajectory-position flip on the DriveCritic test set. “No-flip acc.” and “flip acc.” are the standard accuracies before and after swapping the trajectory order. RR denotes robustness rate as defined above*

## 方法谱系与知识库定位

### 1. 方法谱系：从规则化指标到VLM评估器

**规则化评估的瓶颈。** 当前开环评估的SOTA指标**EPDMS**（Cao et al., CoRL 2025）采用硬编码规则，将安全惩罚项乘积与轨迹质量子分数的加权平均相结合：

$$\mathrm{EPDMS} = \left( \prod_{m \in \mathcal{M}_{\mathrm{pen}}} s_m \right) \cdot \frac{\sum_{m \in \mathcal{M}_{\mathrm{avg}}} w_m s_m}{\sum_{m \in \mathcal{M}_{\mathrm{avg}}} w_m}$$

其子分数如车道保持（LK）和自车进度（EP）基于固定阈值判断——例如LK将横向偏移超过0.5米且持续2秒以上即判为违规。这种设计在人类专家轨迹上暴露了根本性缺陷：人类驾驶员的EP和LK子分数明显偏低（navtrain EP 0.88, LK 0.90；navtest EP 0.87, LK 0.87），总EPDMS得分也未能达到满分（Table I）。原因在于，规则无法区分“为保持安全横向缓冲而短暂压线”与“真正的车道偏离”，也无法理解“面对复杂交通流时保守前进”的合理性——这正是规则化指标的“语境盲点”。

**监督学习基线的尝试。** 论文引入了一个基于ResNet-101编码器的监督成对分类器，通过MLP融合多模态特征来预测偏好。该基线在测试集上达到64.5%的准确率（Table IV），显著优于EPDMS的41.4%，证明学习范式本身优于手工规则。但其性能仍远低于DriveCritic的76.0%，说明纯视觉编码器缺乏VLM所具备的常识推理和语言理解能力，难以内化安全、进度与社会规范的复杂权衡。

**零样本VLM的局限。** 论文测试了两个零样本VLM基线：**Qwen2.5-VL-7B**（Bai et al., arXiv 2025）和**GPT-5**（OpenAI, 2025）。前者在未微调的情况下仅获得48.0%的准确率，后者虽被用作SFT教师模型生成推理轨迹，但其零样本评估能力同样有限。这表明，即使是最先进的通用VLM，在缺乏领域特定的偏好数据和微调时，也无法可靠地执行自动驾驶评估任务。

**DriveCritic的定位。** DriveCritic处于规则化指标与通用VLM之间的交叉地带：它继承了VLM的常识推理和多模态理解能力，但通过精心构造的成对偏好数据集和两阶段强化学习训练（SFT + DAPO + 格式与准确率双重奖励），将通用能力“锚定”到自动驾驶评估的特定需求上。这种“通用基础模型 + 领域对齐微调”的范式，代表了评估方法从“硬编码规则”向“可学习的上下文感知判断”的范式转变。

### 2. 适用边界与关键局限

**场景覆盖的有限性。** DriveCritic数据集仅从NAVSIM中采样了两种特定场景：车道-进度权衡（Case 1）和纯进度对比（Case 2），共5,730个轨迹对（Table II & III）。这意味着模型的评估能力主要集中在对LK和EP子分数冲突的上下文理解上，对于涉及复杂动态交互（如多交通参与者博弈、交通灯状态变化）的场景，其泛化能力尚未验证。数据集场景分布可能偏向NAVSIM采集的特定地理区域和交通模式，跨域迁移能力存疑。

**时序上下文的缺失。** 模型输入仅包含静态BEV地图、拼接的三摄前视图、自车状态和EP/LK子分数，缺乏连续帧的时序信息。这使得DriveCritic无法处理需要时序推理的动态场景——例如判断“减速是否因为前方交通灯即将变红”或“变道是否因为旁车正在加速逼近”。这一局限直接制约了其在闭环评测中的应用前景。

**标注主观性与单一专家偏差。** 偏好标注由单一领域专家完成，未进行多评分者间信度分析。尽管成对偏好任务本身比绝对评分更稳健，但个体专家对“安全”、“合理进度”的判断仍可能带有主观色彩，标注准则的普适性有待进一步检验。

**计算成本与部署瓶颈。** 微调使用了16块A100 GPU，推理需完整的VLM前向传播。与EPDMS的轻量计算相比，DriveCritic在大规模开环评估（如处理数万条轨迹）时的计算开销和能耗显著增加，制约了其在实时或资源受限场景中的部署。

**鲁棒性的未验证维度。** 尽管轨迹位置交换鲁棒性测试表现良好（RR=81.8%，Table VI），但模型在以下维度的稳定性未系统测试：提示词措辞变化、传感器配置差异（如摄像头数量或视角变化）、BEV地图精度下降等。这些因素在实际部署中可能显著影响评估一致性。

### 3. 开放问题与未来方向

**效率与性能的权衡。** 如何降低VLM评估器的计算成本，使其能够在大规模闭环评测中实时运行？可能的方向包括：通过知识蒸馏将大型VLM的评估能力迁移到小型模型；设计轻量化的多模态融合架构；或采用级联策略，仅对规则化指标判为“边界”的案例调用VLM进行深度评估。

**从评估到优化的闭环。** 能否将DriveCritic的偏好评估信号用于端到端规划器的强化学习训练，实现从人类反馈的规划优化（RLHF）？这需要解决奖励信号的稀疏性、VLM推理延迟与训练吞吐量的矛盾，以及偏好判断的噪声处理等问题。

**数据集规模与标注质量。** 如何构建更大规模、多标注者的一致性偏好数据集？引入多位专家进行交叉标注并计算评分者间信度，或采用众包方式扩大标注规模但通过质量控制机制筛选高共识样本，都是可行的扩展路径。此外，自动生成高质量偏好标签（如利用GPT-5作为教师）的方法也需要进一步验证其与人类判断的一致性。

**时序推理能力的融入。** 如何有效融合时序信息以处理动态场景？可能的方案包括：输入连续帧的视频而非静态图像；引入时序位置编码或记忆机制；或显式建模交通参与者的运动预测作为评估的辅助输入。

**评估标准的可解释性。** DriveCritic生成的推理文本提供了评估的可解释性，但如何系统验证推理的正确性和完整性？如何确保模型不是因为“学会了说正确的话”而非“真正理解了场景”才做出正确判断？这需要设计更具挑战性的反事实测试和推理忠实度评估方法。

## 原文 PDF

![[paperPDFs/ICRA_2026/DriveCritic_Towards_Context_Aware_Human_Aligned_Evaluation_for_Autonomous_Driving_with_Vision_Language_Models.pdf]]

---
title: "Do 3D Large Language Models Really Understand 3D Spatial Relationships?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Do_3D_Large_Language_Models_Really_Understand_3D_Spatial_Relationships.pdf
openreview_forum_id: 3vlMiJwo8b
aliases:
- R3B3RF3F
- D3LLMRU3SR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "问题的3D依赖性：通过对比完整3D模型与纯文本盲模型在相同问题上的表现差异，过滤掉3D无关问题，并引入视角旋转鲁棒性评估，从而迫使评估聚焦于真正的3D理解。"
primary_logic: "通过过滤语言可解问题并施加多视角一致性检验，可以暴露现有3D-LLM对语言捷径的依赖；在此基础上提出3D感知重加权微调策略，依据3D依赖度动态调整样本损失权重，能显著提升模型对真实3D空间关系的推理性能。"
claims:
- "盲微调语言模型（仅文本）在SQA3D等多个基准上可达到甚至超越原始3D-LLM的性能。"
- "Real-3DQA过滤后，所有3D-LLM的性能相比SQA3D大幅下降，如LEO从49.4 EM降至14.3 EM。"
- "在视角旋转测试中，所有模型的正确次数从一次到四次急剧下降，最高仅0.5%，表明视角一致性极差。"
- "3D重加权微调（3DR-FT）在Real-3DQA上相比普通微调提升显著，LEO的EM_R从19.1升至29.3。"
---

# Do 3D Large Language Models Really Understand 3D Spatial Relationships?

> [!tip] 核心洞察
> 通过过滤语言可解问题并施加多视角一致性检验，可以暴露现有3D-LLM对语言捷径的依赖；在此基础上提出3D感知重加权微调策略，依据3D依赖度动态调整样本损失权重，能显著提升模型对真实3D空间关系的推理性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 3D大语言模型真的理解3D空间关系吗？ |
| 英文题名 | Do 3D Large Language Models Really Understand 3D Spatial Relationships? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3vlMiJwo8b); [Project](https://real-3dqa.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Real-3DQA Benchmark and 3D Reweighted Finetuning (3DR-FT) |
| Dataset | Real-3DQA (LEO), Real-3DQA (Chat-Scene), Real-ScanQA (LEO), SQA3D vs Real-3DQA (LEO) |

> [!tip] 效果简介
> - Real-3DQA (LEO) 上，EM_R 为 29.3，对比 19.1 (SFT)，变化 +10.2。
> - Real-3DQA (Chat-Scene) 上，EM_R 为 33.9，对比 22.1 (SFT)，变化 +11.8。
> - Real-ScanQA (LEO) 上，EM_R 为 13.9，对比 6.1 (SFT)，变化 +7.8。

## 概述

现有3D大语言模型（3D-LLM）在3D问答基准测试上的高表现，很大程度上源于语言捷径而非真正的空间推理能力。核心瓶颈在于：当前基准（如SQA3D）中存在大量仅凭文本线索即可回答的问题，使得盲文本微调模型也能达到甚至超越完整3D-LLM的性能（**Figure 2**），这严重削弱了基准评估真实3D理解的有效性。

针对这一发现，本文提出两条互补路径：在评估层面构建**Real-3DQA基准**，通过过滤3D无关问题并引入视角旋转鲁棒性检验，迫使评估聚焦于真正的3D空间关系理解；在训练层面设计**3D感知重加权微调策略（3DR-FT）**，依据问题对3D信息的依赖程度动态调整样本损失权重，引导模型从3D上下文中提取证据。

关键结论：过滤后，所有3D-LLM在Real-3DQA上的性能大幅下降（如LEO的EM从49.4降至14.3），视角旋转测试中最高仅0.5%的模型能保持四次一致回答，暴露了现有模型视角鲁棒性的严重不足。而3DR-FT在Real-3DQA上相比标准微调显著提升了真实3D推理性能（LEO的EM_R从19.1升至29.3，Chat-Scene从22.1升至33.9），验证了该策略的有效性。

在方法谱系上，Real-3DQA与3DR-FT定位于3D-LLM评估与训练的公平性改进：相较于仅依赖点云编码的**3D-LLM**（Hong et al., NeurIPS 2023）、结合多视图图像的**LEO**（Huang et al., ICML 2024）以及基于2D VLM的**GPT4Scene**（Qi et al., ICLR 2026）等基线模型，本工作通过系统性地剥离语言捷径并强化3D依赖性，为3D空间推理提供了更严格的评估基准和更有效的训练范式。

## 背景与动机

3D大语言模型（3D-LLM）旨在将点云等三维表示与语言模型结合，以执行三维场景问答（3D-QA）、视觉定位等空间推理任务。近年来，**3D-LLM**（Hong et al., NeurIPS 2023）、**Chat-3D v2**（Huang et al., ArXiv 2024）、**LEO**（Huang et al., ICML 2024）、**Chat-Scene**（Huang et al., NeurIPS 2024）以及基于2D VLM的**GPT4Scene**（Qi et al., ICLR 2026）等模型在SQA3D等主流基准上取得了持续的性能提升。然而，一个根本性问题始终悬而未决：这些模型的高分究竟源于真实的3D空间推理能力，还是依赖语言先验中的捷径？

### 现有基准的语言捷径危机

本研究的核心发现揭示了一个令人担忧的事实：**一个完全不接收任何3D输入的纯文本语言模型，仅通过文本问答对进行盲微调（Blind Finetuned），就能在多个3D-QA基准上达到甚至超越最先进的3D-LLM**。如Figure 2所示，在ScanQA、SQA3D和MSR3D三个基准上，盲微调模型的Exact Match（EM）分数（分别为33.0、50.2、40.3）与原始3D-LLM（32.3、49.4、39.9）持平或略高。这意味着现有基准中存在大量仅凭文本线索即可回答的问题——模型无需真正理解三维空间结构，仅靠“窗户通常在墙上”、“桌子通常在地面上”这类常识性语言先验即可给出正确答案。

进一步对LEO模型的推理消融实验（Table 6）证实了这一判断：移除3D输入后，模型仍能获得32.4%的EM分数，而移除情境描述对性能的影响几乎可忽略（EM仅下降0.1）。这说明模型在相当程度上依赖问题和选项中的文本线索进行“猜测”，而非基于对三维场景的深层理解。

### 视角一致性：被忽视的评估维度

即使模型在单个视角下回答正确，这也不足以证明其具备真实的3D空间推理能力。一个真正理解三维场景的模型，应当在观察者朝向发生变化时仍能保持回答的一致性——例如，当观察者旋转90°后，“我的右边是什么”的正确答案应从“白板”变为“书架”。然而，现有基准完全缺乏对多视角一致性的评估，导致模型可能在单一视角下通过记忆特定场景-答案映射而获得虚高分数。

### 本文动机

上述分析表明，现有3D-QA基准存在两个关键缺陷：（1）**3D无关问题泛滥**，大量问题可通过语言捷径回答，无法有效衡量真实的3D理解；（2）**缺乏视角鲁棒性评估**，无法检验模型是否真正内化了三维空间关系。因此，亟需一个经过严格去偏的基准，以及一种能够迫使模型真正依赖3D信息进行推理的训练策略。本文正是围绕这两个目标展开——构建Real-3DQA基准以过滤语言捷径，并提出3D重加权微调策略以增强模型的3D依赖性。

## 核心创新

本文的核心创新在于对3D大语言模型（3D-LLM）评估范式的根本性反思：**现有基准无法衡量真实的3D空间推理，因为它们充斥着语言捷径**。基于这一诊断，工作从评估和训练两个维度提出了系统性的解决方案。

### 1. 诊断：揭示语言捷径的欺骗性

通过构建**盲微调（Blind Fine-tuning）**对照实验——仅用文本问答对微调语言模型、完全剥离3D输入——发现一个关键事实：盲模型在SQA3D、ScanQA等多个3D问答基准上可以达到甚至超越原始3D-LLM的性能（Figure 2）。例如，LEO在SQA3D上的EM为49.4，而移除3D输入后模型仍能获得32.4的EM（Table 6），说明模型对3D信息的真实依赖远低于表面指标所暗示的水平。这一发现直接动摇了现有基准的评估有效性。

### 2. 评估创新：Real-3DQA基准与视角旋转鲁棒性

针对语言捷径问题，工作提出了**Real-3DQA基准**，其核心机制是通过双重过滤移除3D无关问题：

- **模型对比过滤**：若某问题同时被完整3D模型和其盲微调版本正确回答，则判定为3D无关问题，予以剔除。过滤采用多模型并集策略（$\bar{Q}_{\mathrm{3D-filtered}} = Q_A \cup Q_B \cup Q_C$）以增强鲁棒性。
- **GPT文本过滤**：进一步移除仅凭文本即可被GPT-4o-mini正确回答的问题，得到最终过滤集 $Q_{\mathrm{final}} = Q' \setminus \bar{Q}_{\mathrm{GPT}}$。

此外，引入**视角旋转得分（Viewpoint Rotation Score, VRS）**作为多视角一致性检验：对同一场景生成四个旋转视角（0°、90°、180°、270°）的变体问题，计算模型至少正确回答k个视角问题的平均百分比 $\mathrm{VRS} = \frac{1}{4} \sum_{k=1}^{4} P_k$。这一设计迫使评估聚焦于真正的空间关系理解，而非单视角记忆。

### 3. 训练创新：3D感知重加权微调（3DR-FT）

基于“不同问题对3D上下文的依赖程度不同”的洞察，提出**3D重加权微调（3DR-FT）**策略，其核心机制是动态调整样本损失权重以增强3D依赖性：

- **惊喜比权重**：定义权重函数 $w_j(\boldsymbol{y}, \boldsymbol{x}_{\mathrm{text}}) = \frac{S_{\phi}(\boldsymbol{y}, \boldsymbol{x}_{\mathrm{text}})}{S_{\theta}(\boldsymbol{y}, \boldsymbol{x}_{\mathrm{text}})}$，即盲模型φ与当前模型θ对给定文本上下文预测答案token的惊喜比。当盲模型对某token的预测更“意外”（对数概率更低）时，说明该token的预测更需要3D信息，权重随之增大。
- **重加权损失**：训练目标变为 $\mathcal{L}_{\mathrm{3DR-FT}}(\theta) = \mathbb{E}_{\mathcal{D}} [-\sum_{j=1}^{T} w_j \log p_{\theta}(\boldsymbol{y}_j | y_{<j}, \boldsymbol{x}_{\mathrm{text}}, \boldsymbol{x}_{\mathrm{3D}})]$，使模型在3D依赖样本上受到更强的学习信号。

这一策略与标准微调（SFT）和盲微调（BF）形成鲜明对比：SFT对所有样本等权处理，BF完全忽略3D输入，而3DR-FT依据3D依赖度自适应地分配注意力。

### 4. 效果验证

3DR-FT在Real-3DQA上带来显著提升：LEO的EM_R从SFT的19.1提升至29.3（+10.2），Chat-Scene从22.1提升至33.9（+11.8）（Table 4）。注意力分析进一步验证了机制的有效性——3DR-FT后模型对3D token的平均注意力得分显著提高（Figure 5），证实了3D依赖性的实质性增强。

## 整体框架

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_3vlMiJwo8b/figures/005_Figure_3.jpg]]
*Figure 3: Overview of Real-3DQA Construction Process. Real-3DQA provides a fair and rigorous evaluation framework for 3D spatial reasoning in 3D-LLMs. The construction process begins with Filtering 3D-independent Questions, which removes questions that can be correctly answered by both the 3D-LLM model M _ { x } and its text-only M _ { x } ^ { b l i n d } counterpart, as well as those answerable by the GPT model without 3D input. The remaining high-quality questions Q _ { F i n a l } are then augmented using GPT, generating spatially consistent variations through viewpoint rotations while preserving the underlying 3D relationships. Finally, expert reviews eliminate redundancy and invalid data, ensuri...*

本文的核心工作围绕一个核心矛盾展开：现有3D问答基准测试（如SQA3D）存在大量语言捷径，使得仅依赖文本的盲微调模型也能达到甚至超越完整3D-LLM的性能，因此这些基准无法有效衡量真实的3D空间推理能力。为解决这一问题，作者构建了一套从评估到训练的完整框架，包含两大组件：**Real-3DQA基准测试**和**3D重加权微调策略（3DR-FT）**。

### 框架总览

整体pipeline遵循“诊断→过滤→增强→重训”的逻辑链条：

1. **诊断阶段**：对比原始3D-LLM与其盲微调版本（仅接收文本输入、无3D上下文）在同一问题上的表现，暴露语言捷径的存在——盲模型在SQA3D等多个基准上可匹配甚至超越原始模型（Figure 2）。
2. **过滤阶段**：基于诊断结果，构建Real-3DQA过滤集，移除3D无关问题，并引入视角旋转变体以评估多视角一致性。
3. **训练阶段**：提出3DR-FT策略，依据每个问题的3D依赖度动态调整样本损失权重，迫使模型在预测时真正利用3D上下文。

### Real-3DQA基准构建流程

Figure 3给出了基准构建的完整流程，核心包含两个串行模块：

#### 3D独立问题过滤模块

该模块的目标是从原始测试集中剔除仅凭文本线索即可正确回答的问题。具体分两步执行：

- **模型对比过滤**：对于每个3D-LLM模型 $X$，若某问题 $q$ 同时被原始模型 $M_X$ 和其盲微调版本 $M_X^{\text{blind}}$ 正确回答，则判定为3D无关问题：
  $$Q_X = \{ q \in Q \mid M_X(q) = M_X^{\text{blind}}(q) = \text{correct} \}$$
  为提高鲁棒性，取三个模型（LEO、Chat-Scene、3D-LLM）的3D无关问题集的并集：
  $$\bar{Q}_{\text{3D-filtered}} = Q_A \cup Q_B \cup Q_C$$
  从原始测试集 $Q$ 中移除这些并集问题，得到中间集 $Q' = Q \setminus \bar{Q}_{\text{3D-filtered}}$。

- **GPT辅助过滤**：进一步利用GPT-4o-mini仅凭文本输入回答问题，移除 $Q'$ 中GPT也能正确回答的问题：
  $$Q_{\text{final}} = Q' \setminus \bar{Q}_{\text{GPT}}$$
  $Q_{\text{final}}$ 即为Real-3DQA的最终过滤测试集。

#### 视角旋转数据增强模块

为评估模型的空间一致性，该模块利用GPT根据场景图生成旋转后的情境描述和答案（Figure 4）。具体而言，对每个问题生成四个视角（原始方向及90°、180°、270°旋转），保持底层3D空间关系不变，仅改变观察者朝向。由此引入**视角旋转得分（VRS）**作为新的评估指标：
$$P_k = \frac{N_k}{N_{\text{total}}} \times 100, \quad \text{VRS} = \frac{1}{4} \sum_{k=1}^{4} P_k$$
其中 $P_k$ 表示在一组四个旋转问题中至少回答正确 $k$ 个的实例百分比。VRS越低，说明模型的多视角一致性越差。

### 3D重加权微调策略（3DR-FT）

在训练侧，3DR-FT的核心思想是：对于盲模型（$\phi$，仅文本）难以预测、而当前模型（$\theta$，含3D输入）能够利用3D上下文预测的token，应当赋予更高的训练权重。这通过**惊喜比**（ratio of surprise）来实现：
$$w_{j}(\pmb{y}, \pmb{x}_{\mathrm{text}}) := \frac{S_{\phi}(\pmb{y}, \pmb{x}_{\mathrm{text}})}{S_{\theta}(\pmb{y}, \pmb{x}_{\mathrm{text}})} = \frac{\log p_{\phi}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\mathrm{text}})}{\log p_{\theta}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\mathrm{text}})}$$

该权重 $w_j$ 衡量盲模型相对于当前模型的“惊讶程度”：当盲模型对某token的预测概率极低（高惊讶），而当前模型能利用3D信息提高预测置信度时，权重增大。最终损失函数为：
$$\mathcal{L}_{\mathrm{3DR-FT}}(\theta) := \mathbb{E}_{\mathcal{D}} \Big[ - \sum_{j=1}^{T} w_{j}(\pmb{y}, \pmb{x}_{\mathrm{text}}) \log p_{\theta} \big( \pmb{y}_{j} \mid y_{<j}, \pmb{x}_{\mathrm{text}}, \pmb{x}_{\mathrm{3D}} \big) \Big]$$

这一设计将训练焦点从“所有样本均等对待”转向“优先学习3D依赖样本”，从而抑制模型对文本捷径的过拟合。

### 模块间数据流关系

```
SQA3D原始测试集 Q
    │
    ├─→ 3D独立问题过滤模块 ─→ Q_final (Real-3DQA过滤集)
    │       │
    │       ├─ 模型对比过滤 (LEO/Chat-Scene/3D-LLM 盲版本对比)
    │       └─ GPT辅助过滤 (GPT-4o-mini 纯文本回答)
    │
    └─→ 视角旋转增强模块 ─→ 旋转变体问题 (0°/90°/180°/270°)
            │
            └─→ VRS评估 (多视角一致性得分)

SQA3D训练集
    │
    └─→ 3D重加权微调模块 (3DR-FT)
            │
            ├─ 盲模型 φ 计算惊喜度 S_φ
            ├─ 当前模型 θ 计算惊喜度 S_θ
            └─ 加权损失 L_3DR-FT → 更新 θ
```

### 关键设计决策

| 设计要素 | 基线做法 | 本文方案 | 设计动机 |
|---------|---------|---------|---------|
| 评估数据 | 使用完整SQA3D测试集 | Real-3DQA过滤集（移除3D无关问题） | 消除语言捷径对评估的污染 |
| 评估指标 | EM / EM_R | 新增VRS（视角旋转得分） | 衡量多视角空间一致性 |
| 训练目标 | 标准交叉熵损失 | 惊喜比加权交叉熵损失 | 提升3D依赖样本的训练权重 |
| 训练数据使用 | 均匀对待所有样本 | 依据盲模型惊喜比动态重加权 | 迫使模型真正利用3D上下文 |

该框架的一个显著特征是**评估与训练的闭环设计**：过滤阶段利用盲模型诊断语言捷径，训练阶段则利用盲模型的惊喜比指导权重分配，两者共享“盲模型作为3D依赖度探针”这一核心思想。Table 1将Real-3DQA与现有基准进行了系统对比，突出其在去偏、视角鲁棒性评估和问题多样性方面的优势。

## 核心模块与公式推导

### 3D独立问题过滤模块

该模块的目标是从原始SQA3D测试集中剥离语言捷径可解的问题，构建Real-3DQA。核心逻辑是：若一个问题同时被完整3D-LLM $M_X$ 和其盲微调版本 $M_X^{\text{blind}}$ 正确回答，则该问题被视为3D无关。

对于单个模型 $X$，其3D无关问题集定义为：

$$Q_X = \{ q \in Q \mid M_X(q) = M_X^{\text{blind}}(q) = \text{correct} \}$$

为提升过滤鲁棒性，取三个模型（3D-LLM、Chat-3D v2、LEO）的并集：

$$\bar{Q}_{\text{3D-filtered}} = Q_A \cup Q_B \cup Q_C$$

从原始测试集中移除这些3D无关问题后得到中间集 $Q' = Q \setminus \bar{Q}_{\text{3D-filtered}}$。进一步，利用GPT-4o-mini在纯文本条件下作答，移除其也能正确回答的问题，得到最终过滤集：

$$Q_{\text{final}} = Q' \setminus \overline{Q}_{\text{GPT}}$$

### 视角旋转数据增强与评估模块

为检验模型是否真正理解3D空间关系而非记忆固定视角答案，该模块利用GPT根据场景图生成四个旋转视角（0°、90°、180°、270°）下的情境描述和对应答案。评估指标为**视角旋转得分（Viewpoint Rotation Score, VRS）**，衡量模型在四个视角下至少回答正确 $k$ 个问题的平均百分比：

$$P_k = \frac{N_k}{N_{\text{total}}} \times 100, \quad \text{VRS} = \frac{1}{4} \sum_{k=1}^{4} P_k$$

其中 $N_k$ 表示在四视角问题组中至少正确回答 $k$ 个的组数，$N_{\text{total}}$ 为总组数。VRS越高，模型的多视角一致性越强。

### 3D重加权微调模块（3DR-FT）

该模块的核心思想是：利用盲模型 $\phi$（仅文本）与当前训练模型 $\theta$（含3D输入）对同一文本上下文的“惊喜”差异，量化每个词元对3D信息的依赖程度，并以此作为损失权重，迫使模型在预测时主动利用3D上下文。

**重加权函数**定义为盲模型惊喜与当前模型惊喜之比：

$$w_{j}(\pmb{y}, \pmb{x}_{\text{text}}) := \frac{S_{\phi}(\pmb{y}, \pmb{x}_{\text{text}})}{S_{\theta}(\pmb{y}, \pmb{x}_{\text{text}})} = \frac{\log p_{\phi}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\text{text}})}{\log p_{\theta}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\text{text}})}$$

其中 $\pmb{y}_j$ 为当前目标词元，$\pmb{y}_{<j}$ 为上文，$\pmb{x}_{\text{text}}$ 为纯文本输入。当盲模型对该词元更“惊讶”（即 $p_{\phi}$ 低，$S_{\phi}$ 高）而当前模型因引入3D信息而更“确定”（$S_{\theta}$ 低）时，权重 $w_j > 1$，该样本在训练中被放大惩罚，从而鼓励模型依赖3D上下文。

**3DR-FT损失函数**为加权交叉熵：

$$\mathcal{L}_{\text{3DR-FT}}(\theta) := \mathbb{E}_{\mathcal{D}} \Big[ - \sum_{j=1}^{T} w_{j}(\pmb{y}, \pmb{x}_{\text{text}}) \log p_{\theta} \big( \pmb{y}_{j} \mid y_{<j}, \pmb{x}_{\text{text}}, \pmb{x}_{\text{3D}} \big) \Big]$$

### 条件独立间隙（辅助分析工具）

为量化3D上下文对单个词元预测的贡献，定义**条件独立间隙** $\delta_j$：

$$\delta_{j} := \frac{p_{\theta}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\text{text}}, \pmb{x}_{\text{3D}}) - p_{\theta}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\text{text}})}{p_{\theta}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\text{text}})}$$

$\delta_j > 0$ 表明引入3D上下文后该词元的预测概率相对提升，即模型确实利用了3D信息。该指标在附录E中用于分析模型行为，而非训练或评估的核心组件。

## 实验与分析

### 核心发现：现有基准的语言捷径与崩溃

本工作的核心实验动机源自一个反直觉的观察：**盲微调语言模型（Blind Finetuned）**——即完全移除3D输入、仅用文本问答对微调的模型——在多个主流3D问答基准上能够匹配甚至超越原始3D-LLM的性能（Figure 2）。这一发现直接暴露了现有基准测试设计的根本缺陷：大量问题可以通过语言先验和常识推理解决，而非真正的3D空间理解。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_3vlMiJwo8b/figures/003_Figure_2.jpg]]
*Figure 2: Our finding: A language model fine-tuned only on text QA pairs without any 3D inputs (Blind Finetuned) can match or even surpass state-of-the-art 3D-LLMs (Original) on multiple 3D-QA benchmarks. This exposes a critical weakness in current benchmark design and calls into question their ability to assess genuine 3D reasoning despite linguistic shortcuts*

基于此，作者构建了**Real-3DQA**过滤基准，并在此基准上对五个代表性模型进行了系统评估。Table 2展示了SQA3D与Real-3DQA之间的性能对比，结果揭示了当前3D-LLM真实空间推理能力的严重不足：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_3vlMiJwo8b/figures/007_Table_2.jpg]]
*Table 2: Performance comparison on SQA3D and our Real-3DQA. We see a significant performance drop in our new benchmark*

- **性能断崖式下跌**：所有模型在Real-3DQA上的Exact Match（EM）均大幅下降。以LEO为例，其EM从SQA3D的49.4骤降至Real-3DQA的14.3，降幅达35.1个百分点。即便性能最强的**GPT4Scene**（Qi et al., ICLR 2026），EM也从60.6降至33.1。
- **瓶颈定位**：这一降幅表明，SQA3D中超过70%的问题（以LEO为参考）实际上可以通过语言捷径解决，而非依赖3D空间推理。Real-3DQA通过过滤3D无关问题，成功将评估焦点收缩至真正的3D依赖问题。

### 视角旋转鲁棒性：从一致性崩溃到VRS量化

为了进一步检验模型是否真正“理解”3D空间关系，作者引入了**视角旋转鲁棒性测试**：对同一场景从四个旋转方向（0°、90°、180°、270°）分别提问，考察模型能否在所有视角下给出正确回答。Table 3展示了各模型在Real-3DQA上的旋转鲁棒性对比，结果揭示了现有模型在空间一致性上的严重缺陷：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_3vlMiJwo8b/figures/008_Table_3.jpg]]
*Table 3: Rotation Robustness Comparison on Real-3DQA. The table shows the performance of different 3D-LLMs (using refined exact match metric) when tested with varying numbers of correct rotations. All models demonstrate a clear performance degradation as the required number of correct rotations increases, highlighting the challenge of rotation robustness in 3D understanding*

- **一致性崩溃**：当要求四个旋转视角全部正确时，所有模型的EM Refined均趋近于零。即使是表现最好的GPT4Scene，从单视角正确的55.5%暴跌至四视角全对的0.5%，其余模型则几乎归零。
- **VRS指标**：Viewpoint Rotation Score（VRS）作为四个正确次数阈值的平均得分，GPT4Scene仅获得18.2分，而**3D-LLM**（Hong et al., NeurIPS 2023）和**Chat-3D v2**（Huang et al., ArXiv 2024）分别仅为9.6和6.6。这一结果表明，现有模型在面对视角变化时几乎不具备空间一致性推理能力，其“正确回答”更可能源于统计关联而非几何理解。

Figure 8进一步以折线图形式展示了这一下降趋势：所有模型的EM Refined随所需正确旋转次数增加而单调递减，且下降斜率极为陡峭，证实了视角鲁棒性是当前3D-LLM的普遍瓶颈。

### 3D重加权微调（3DR-FT）：主结果与消融分析

针对上述瓶颈，作者提出了**3D重加权微调（3DR-FT）**策略，其核心机制是通过计算盲模型与当前模型对文本上下文的“惊喜比”作为样本权重，在训练中提升3D依赖样本的惩罚力度。Table 4展示了训练策略的消融实验结果：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_3vlMiJwo8b/figures/010_Table_4.jpg]]
*Table 4: Ablation Study on Training Strategies. Columns group results by model and dataset: LEO on ScanQA/Real-ScanQA (left) and SQA3D/Real-3DQA (center), and Chat-Scene on SQA3D/Real-3DQA (right). 3D-reweighted fine-tuning (3DR-FT) delivers consistent gains across both datasets and models, with the largest improvements on the 3D-dependent sets—Real-3DQA and Real-ScanQA—while Supervised FT remains strongest on SQA3D*

- **Real-3DQA上的显著提升**：3DR-FT在LEO上实现了29.3的EM Refined，相比标准微调（SFT）的19.1提升了10.2点，相比盲微调（BF）的13.6提升了15.7点。在Chat-Scene上，3DR-FT达到33.9，相比SFT的22.1提升了11.8点。
- **Real-ScanQA上的跨数据集泛化**：在Real-ScanQA上，3DR-FT将LEO的EM Refined从SFT的6.1提升至13.9，提升幅度达7.8点，验证了该策略在不同数据集上的迁移能力。
- **SQA3D上的性能回退及其归因**：值得注意的是，3DR-FT在原始SQA3D上的EM Refined反而低于SFT（LEO: 48.3 vs 52.2）。Figure 6揭示了这一现象的根源：在Chat-Scene上，3DR-FT导致591个问题从正确变为错误，其中441个来自过滤集（即3D无关问题）。因为SQA3D混合了3D依赖和3D无关问题，强调3D证据的3DR-FT策略会损害模型对语言捷径的依赖，从而降低在3D无关问题上的准确率。这一现象恰恰验证了3DR-FT的有效机制——它迫使模型从语言捷径转向3D推理。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_3vlMiJwo8b/figures/011_Figure_6.jpg]]
*Figure 6: Why 3DR-FT reduces SQA3D performance? For Chat-Scene, 591 questions flip from correct to wrong after 3DR-FT; 441 of these come from the Filtered Set (green box with diagonal hatching). Because SQA3D mixes 3Ddependent questions (Real-3DQA) with 3D-independent ones (Filtered Set), emphasizing 3D evidence via 3DR-FT can hurt the latter set, lowering the overall SQA3D score*

### 3D依赖性的注意力验证

为了直接验证3DR-FT是否确实增强了模型对3D信息的利用，作者分析了模型对3D令牌的注意力得分分布（Figure 5）。结果显示，经过3DR-FT后，模型对3D令牌的平均注意力得分显著提高，表明模型在预测答案时更多地关注了3D上下文。这一注意力层面的证据与性能提升相互印证，构成了一条完整的因果链：重加权损失→增强3D注意力→提升3D依赖问题的推理性能。

### 推理消融：3D先验从何而来？

Table 6对LEO在SQA3D上的推理过程进行了组件消融，以追溯其性能来源。完整模型（包含情境描述、问题和3D输入）的EM为49.4。移除3D输入后，EM降至32.4，降幅显著但模型仍能回答近三分之二的问题——这再次印证了语言捷径的贡献。而移除情境描述仅导致EM下降0.1，表明情境文本对LEO的贡献几乎可以忽略。这一消融清晰地分解了LEO的三大信息源：3D输入贡献约17个EM点，语言先验贡献约32个EM点，情境描述贡献近乎为零。

### 问题类型细粒度分析

Table 5和Figure 7展示了各模型在Real-3DQA十种问题类型上的能力分布。雷达图（Figure 7）显示GPT4Scene在所有类别上均表现最优，但各模型在空间关系、形状识别和推理任务上普遍存在一致的缺陷。这一细粒度分析不仅揭示了当前3D-LLM的能力边界，也为未来的定向改进提供了明确的靶点。

## 方法谱系与知识库定位

### 问题诊断：语言捷径主导的虚假评估

本工作的核心出发点是对现有3D问答基准的**诊断性批判**。研究发现，SQA3D等主流基准中存在大量**3D无关问题**——即仅凭文本上下文和语言先验即可正确回答的问题。这一发现通过两类实验得到验证：

- **盲微调对照**：将语言模型仅微调于文本问答对（不含任何3D输入），其在SQA3D上的EM可达甚至超越原始3D-LLM（Figure 2）。这意味着基准的评估信号被语言捷径污染，无法有效衡量真实的3D空间推理能力。
- **输入消融**：对LEO（Huang et al., ICML 2024）的推理阶段消融显示，移除3D输入后EM仅从49.4降至32.4，而移除情境描述对性能几乎无影响（EM仅下降0.1，Table 6）。这进一步证实了情境文本对模型决策的贡献微乎其微。

这一诊断直接挑战了以SQA3D为代表的现有3D-QA基准的有效性，构成了方法设计的因果前提。

### 方法定位：从基准净化到训练干预

本文的方法贡献沿两条轴线展开：**评估层的基准净化**（Real-3DQA）和**训练层的3D依赖增强**（3DR-FT）。两者在逻辑上形成闭环——前者暴露问题并定义评估标准，后者针对性地修复问题。

**Real-3DQA基准**的构建包含三个递进的过滤步骤：
1. **模型对比过滤**：对于每个问题，若原始3D-LLM与其盲微调版本均能正确回答，则标记为3D无关问题；取三个模型（LEO、Chat-Scene、3D-LLM）的并集以增强鲁棒性。
2. **GPT文本过滤**：进一步移除GPT-4o-mini仅凭文本即可正确回答的问题。
3. **视角旋转增强**：对保留的3D依赖问题，生成四个旋转视角（0°、90°、180°、270°）的变体，并引入视角旋转得分（VRS）作为多视角一致性的度量指标。

**3D重加权微调（3DR-FT）** 的策略核心是**惊喜比加权**：对于每个词元，计算盲模型φ与当前模型θ在给定文本上下文下的负对数似然之比作为权重。当盲模型对某词元的预测更困难（惊喜更大）时，该词元获得更高权重，从而在训练中放大3D上下文对预测的贡献。损失函数形式为：

$$\mathcal{L}_{\mathrm{3DR-FT}}(\theta) := \mathbb{E}_{\mathcal{D}} \Big[ - \sum_{j=1}^{T} w_{j}(\pmb{y}, \pmb{x}_{\mathrm{text}}) \log p_{\theta} \big( \pmb{y}_{j} \mid y_{<j}, \pmb{x}_{\mathrm{text}}, \pmb{x}_{\mathrm{3D}} \big) \Big]$$

其中重加权函数为：

$$w_{j}(\pmb{y}, \pmb{x}_{\mathrm{text}}) := \frac{S_{\phi}(\pmb{y}, \pmb{x}_{\mathrm{text}})}{S_{\theta}(\pmb{y}, \pmb{x}_{\mathrm{text}})} = \frac{\log p_{\phi}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\mathrm{text}})}{\log p_{\theta}(\pmb{y}_{j} \mid \pmb{y}_{<j}, \pmb{x}_{\mathrm{text}})}$$

### 与现有工作的关系

**基线方法**：本文实验涉及五类3D-LLM基线，包括基于点云编码的**3D-LLM**（Hong et al., NeurIPS 2023）、**Chat-3D v2**（Huang et al., ArXiv 2024）、结合多视图图像的**LEO**（Huang et al., ICML 2024）、**Chat-Scene**（Huang et al., NeurIPS 2024），以及基于2D VLM的3D感知模型**GPT4Scene**（Qi et al., ICLR 2026）。训练策略层面，以标准监督微调（SFT）和盲微调（BF）作为对照。

**与基准工作的差异**：Table 1系统对比了Real-3DQA与ScanQA、SQA3D、MSR3D等七个基准在六个维度上的差异。Real-3DQA是唯一同时具备情境化问题、LLM辅助文本收集、去偏处理、视角鲁棒性评估、人工验证和多类型问题覆盖的基准。其核心创新在于**主动过滤而非被动收集**——通过模型对比和GPT过滤移除语言可解问题，而非仅依赖人工标注的质量控制。

**训练策略的创新性**：3DR-FT区别于标准的数据增强或对抗训练，其权重设计**动态依赖盲模型与当前模型的信息差**，使得训练信号天然地偏向3D依赖样本。这与基于固定权重或启发式规则的课程学习策略有本质区别。

### 适用边界与局限

1. **视角旋转的粒度限制**：当前VRS仅支持四个基本旋转方向，更细粒度的旋转（如12个方向）需要复杂的规则和重新标注，这一扩展在当前框架下不可行。

2. **过滤偏差风险**：Real-3DQA的过滤过程依赖于三个特定3D-LLM（LEO、Chat-Scene、3D-LLM）的表现，可能引入模型特定的偏差——被某一模型判定为3D无关的问题，可能对其他模型仍是3D依赖的。取并集的策略缓解但未消除这一风险。

3. **SQA3D混合数据集的性能折损**：3DR-FT在增强3D依赖性的同时，可能导致模型在3D无关问题上表现下降。Figure 6显示，Chat-Scene经3DR-FT后，有591个问题从正确翻转为错误，其中441个来自过滤集（3D无关问题）。这意味着在SQA3D这类混合数据集上，3DR-FT的整体准确率可能不升反降——这是方法设计的**有意权衡**，而非失败。

4. **场景与语言限制**：评估局限于英语场景和SQA3D的数据结构（以ScanNet室内场景为主），尚未在更多样化的3D场景或其他语言上验证。

5. **对GPT-4o-mini的依赖**：GPT文本过滤步骤依赖GPT-4o-mini的判断能力，若GPT本身存在语言理解偏差，可能影响过滤质量。论文中提及了人工验证步骤，但未详细报告验证的覆盖率和一致性。

### 开放问题

1. **细粒度视角鲁棒性**：如何设计支持更细粒度旋转（如12个方向）的评估框架，同时保持问答的一致性和场景图的正确性？

2. **架构层面的旋转不变性**：当前3DR-FT仅在训练目标层面增强3D依赖，未涉及模型架构的改进。将旋转不变特征编码集成到3D-LLM架构中，能否从根本上提升视角鲁棒性，而非仅依赖数据增强和重加权？

3. **跨任务泛化**：3DR-FT策略能否推广到其他3D视觉-语言任务，如3D描述（3D captioning）、3D定位（3D grounding）？这些任务中语言捷径的表现形式可能不同，需要重新设计盲模型对照。

4. **替代性去偏方法**：除过滤和重加权外，对抗训练、因果干预等方法是否也能有效移除语言捷径？这些方法在样本效率和泛化性上可能各有优劣。

5. **动态场景扩展**：在包含物体运动、场景变化的动态3D环境中，语言捷径和3D依赖的边界可能更加模糊，该方法是否仍能有效提升3D理解？

## 原文 PDF

![[paperPDFs/ICLR_2026/Do_3D_Large_Language_Models_Really_Understand_3D_Spatial_Relationships.pdf]]

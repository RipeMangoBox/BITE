---
title: "From Seeing to Experiencing: Scaling Navigation Foundation Models with Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Seeing_to_Experiencing_Scaling_Navigation_Foundation_Models_with_Reinforcement_Learning.pdf
project_link: https://vail-ucla.github.io/S2E
code_link: null
openreview_forum_id: 0c7nAZjyr5
aliases:
- SESLF
- FSESNFMRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在离线预训练之后引入强化学习在线交互训练，通过仿真环境中试错获得的奖励信号（碰撞惩罚、目标到达激励等）直接注入避障与动态交互能力。"
primary_logic: "S2E框架通过锚点引导的高斯混合模型(AGDM)在预训练时稳定地建模多模态导航行为，再通过残差注意力模块(RAM)在RL微调时仅修改与交互直接相关的交叉注意力层，从而在不破坏预训练泛化视觉表征的前提下获得反应性交互能力。"
claims:
- "增加离线数据量（250k→750k）仅提升2%成功率，而RL微调在不使用额外离线数据的情况下将成功率绝对提升15%。"
- "在NavBench-GS基准的四种场景（空旷/障碍物/行人/混合）中，S2E的成功率和路径完成度全面超越GNM、ViNT、NoMaD等先前模型，且训练数据量远少于部分方法（100h vs 700-2000h）。"
- "仅微调残差注意力模块(RAM)的策略优于全参数微调(DecFT-RL)和仅行为克隆预训练(S2E-BC)，且在复杂障碍物场景中避免梯度爆炸和灾难性遗忘。"
- "RL后训练（S2E-RL）随训练计算量增加仍能维持或提升成功率，而监督微调（S2E-SFT）出现严重过拟合，证明RL在机器人学习中比SFT更具鲁棒性。"
---

# From Seeing to Experiencing: Scaling Navigation Foundation Models with Reinforcement Learning

> [!tip] 核心洞察
> S2E框架通过锚点引导的高斯混合模型(AGDM)在预训练时稳定地建模多模态导航行为，再通过残差注意力模块(RAM)在RL微调时仅修改与交互直接相关的交叉注意力层，从而在不破坏预训练泛化视觉表征的前提下获得反应性交互能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从看到体验：利用强化学习扩展导航基础模型 |
| 英文题名 | From Seeing to Experiencing: Scaling Navigation Foundation Models with Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0c7nAZjyr5) · [Project](https://vail-ucla.github.io/S2E) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Seeing-to-Experiencing (S2E) learning framework |
| Dataset | NavBench-GS (Empty场景), NavBench-GS-Obstacle (消融实验), 真实世界轮式机器人 (障碍物+行人) |

> [!tip] 效果简介
> - NavBench-GS (Empty场景) 上，Success Rate (SR) ↑ 为 0.82，对比 0.61 (MBRA, next best)，变化 +0.21。
> - NavBench-GS-Obstacle (消融实验) 上，Success Rate (SR) ↑ 为 0.57 (S2E-Full)，对比 0.42 (S2E-BC, 仅预训练)，变化 +0.15。
> - 真实世界轮式机器人 (障碍物+行人) 上，Success Rate (SR) ↑ 为 0.51，对比 0.33 (S2E-BC)，变化 +0.18。

## 概要

### 瓶颈与核心发现

当前导航基础模型普遍采用**离线行为克隆**范式——从大规模人类驾驶视频中学习“看-走”映射。然而，这一范式存在两个根本性瓶颈：

1. **离线数据的因果盲区**：仅依靠视频数据的模仿学习忽略了环境交互中的因果反馈，导致模型缺乏障碍物规避、行人绕行等反应性安全行为。模型学到的是“在什么场景下人类做了什么”，而非“我的动作会引发什么后果”。

2. **数据规模收益迅速饱和**：单纯扩大离线数据量带来的性能提升极为有限——从250k样本增至750k样本，成功率仅提升约2%（Figure 7a），说明离线行为克隆已触及瓶颈。

本文的核心洞察在于：**导航智能体必须像人类一样，在“看到”的基础上通过交互“体验”环境反馈，才能获得可行动的安全技能**。基于此，作者提出**Seeing-to-Experiencing (S2E)** 学习框架，将离线视频预训练与强化学习在线交互训练相结合，在不破坏预训练泛化视觉表征的前提下注入反应性交互能力。

### 方法定位

S2E框架在方法谱系中处于**离线预训练 + 在线RL微调**的混合范式位置，其关键技术创新体现在两个层面：

| 技术组件 | 核心机制 | 解决的问题 |
|---------|---------|-----------|
| **锚点引导的高斯混合模型 (AGDM)** | 通过K-Means锚点引导的多模高斯混合，建模城市导航中天然多模态的行为分布（如避障时左绕/右绕） | 离线预训练时稳定学习多样化运动模式，避免单模回归的模式坍缩 |
| **残差注意力模块 (RAM)** | 冻结预训练的交叉注意力层，训练并行的零初始化副本，通过门控线性层渐进注入交互知识 | RL微调时仅修改与交互直接相关的注意力层，避免灾难性遗忘和梯度爆炸 |

相比现有导航基础模型，S2E的差异化定位在于：

- **vs. GNM/ViNT/NoMaD** (Shah et al., 2023a/2023b; Sridhar et al., 2024)：这些方法依赖纯离线行为克隆，缺乏交互学习环节；S2E通过RL后训练引入碰撞惩罚、目标奖励等因果信号。
- **vs. MBRA/CityWalker** (Liu et al., 2024b)：这些方法通过扩大离线数据量（700h-2000h）追求性能，但数据效率低；S2E仅用100h视频数据加RL微调即实现全面超越。
- **vs. 全参数微调/解码器微调**：RAM的残差设计在训练稳定性（避免梯度爆炸）和显存效率（37GB vs 40GB）上均优于直接微调方案。

### 主要结果摘要

**仿真基准 (NavBench-GS)**：在空旷、障碍物、行人、混合四种场景中，S2E的成功率和路径完成度**全面超越**GNM、ViNT、NoMaD、MBRA、CityWalker等先前模型（Table 1）。其中在空旷场景下，S2E成功率达0.82，较次优方法MBRA（0.61）提升**+0.21**。

**RL有效性的关键证据**：RL微调在不使用额外离线数据的情况下，将成功率绝对提升约15%（Figure 7a）；且随训练计算量增加，RL仍能维持或提升性能，而监督微调（SFT）出现严重过拟合（Figure 7b），证明RL在机器人学习中比SFT更具鲁棒性。

**真实世界验证**：在轮式机器人（障碍物+行人场景）上，S2E成功率达0.51，较仅预训练版本（S2E-BC, 0.33）提升**+0.18**（Table 2）。

**消融实验确认**：仅微调RAM的策略优于全参数微调（DecFT-RL）和仅行为克隆预训练（S2E-BC），在复杂障碍物场景中成功率达0.57（vs. S2E-BC的0.42），且避免了梯度爆炸和灾难性遗忘（Table 3）。

### 局限与开放问题

当前S2E依赖纯视觉输入，缺乏显式3D深度或占据感知，在复杂障碍物场景中仍会出现碰撞；且框架以局部导航为主，长距离任务需外部路径规划支持。RL与SFT在机器人学习中的扩展规律是否具有普适性、如何高效引入3D感知以进一步提升安全性，是值得进一步探索的方向。



### 机器人导航的离线学习瓶颈

端到端视觉导航的近期进展主要依赖大规模离线视频数据的行为克隆（Behavior Cloning, BC）：从人类遥操作或脚本策略收集的轨迹中，模型学习将RGB观测直接映射为动作指令。这一范式催生了**GNM**（Shah et al., 2023a）、**ViNT**（Shah et al., 2023b）、**NoMaD**（Sridhar et al., 2024）等导航基础模型，它们通过扩大数据规模（70–100小时视频）获得了令人瞩目的泛化能力。

然而，纯离线学习存在一个根本性瓶颈：**行为克隆仅能模仿观测到的动作，无法获取环境交互中的因果反馈**。当机器人执行模型预测的轨迹时，任何微小的分布偏移都可能将机器人带入训练分布之外的“未知地带”——例如前方突然出现障碍物或行人横穿路径——此时模型缺乏从碰撞、卡死等失败经验中学习的能力。具体表现为：

- **缺乏反应性安全行为**：离线训练的模型在空旷场景表现良好，但面对静态障碍物和动态行人时，无法产生绕行、减速、等待等交互性动作。
- **数据效率的边际递减**：单纯扩大离线数据量带来的性能提升迅速饱和。Figure 7(a) 显示，将训练样本从250k增加到750k仅带来约2%的成功率提升，说明“更多数据”并非解决交互能力缺失的有效路径。

### 从“看到”到“体验”：强化学习的引入

本文的核心动机源自一个直觉类比：**正如人类学习驾驶不仅需要观察示范，还需要在真实环境中试错并获得反馈，AI导航智能体同样需要“体验”物理交互**（Figure 2）。强化学习（Reinforcement Learning, RL）通过在仿真环境中让机器人实际执行动作并接收奖励信号（如碰撞惩罚、目标到达激励），能够将避障和动态交互能力直接注入策略。

但将RL直接应用于大规模预训练模型面临两个关键挑战：

1. **灾难性遗忘**：全参数RL微调可能破坏预训练阶段学到的泛化视觉表征和多样化的导航行为模式。
2. **训练不稳定性**：导航策略的高维连续动作空间与多模态行为分布使得RL训练容易遭遇梯度爆炸或策略坍缩。

### S2E框架的设计动机

针对上述挑战，本文提出**Seeing-to-Experiencing (S2E)** 学习框架，其核心设计逻辑是：

- **离线预训练阶段**：采用**锚点引导的高斯混合模型（Anchor-Guided Distribution Matching, AGDM）** 稳定地建模真实世界中多模态的导航行为（如在人行道分叉口的多种合理路径），为后续RL训练提供表达力强且结构化的动作先验。
- **在线RL微调阶段**：设计**残差注意力模块（Residual-Attention Module, RAM）**，仅微调与交互直接相关的交叉注意力层，通过零初始化残差分支渐进注入避障知识，从而在不破坏预训练泛化表征的前提下获得反应性交互能力。

这一“预训练-后训练”的混合范式旨在回答一个关键问题：**能否用极少的交互经验（RL微调），弥补海量离线数据（行为克隆）所无法提供的安全交互能力？** 后续实验表明，RL微调在不使用额外离线数据的情况下，将成功率绝对提升15%（Figure 7a），且其鲁棒性显著优于监督微调（SFT）——后者随训练计算量增加出现严重过拟合（Figure 7b）。



## 核心方法与创新机理

S2E框架的核心创新在于系统性地填补了“仅依靠离线视频预训练”与“安全交互导航”之间的因果鸿沟。其技术路径可归结为两个**changed slots**：**动作分布表示**从单峰高斯/离散类别升级为锚点引导的高斯混合模型（AGDM），以及**后训练范式**从纯行为克隆（BC）转向强化学习（RL）微调。第三个changed slot——**微调模块选择**（残差注意力模块RAM）——则为上述范式转换提供了关键的稳定性保障。

### 瓶颈与因果调节变量

现有导航基础模型（GNM、ViNT、NoMaD等）的**真实瓶颈**在于：行为克隆仅模仿离线视频中的专家轨迹，完全缺失环境交互中的因果反馈信号。这导致模型在遇到障碍物或动态行人时缺乏反应性避让能力，且单纯扩大离线数据量带来的性能提升迅速饱和——从250k样本增加到750k样本，成功率仅提升约2%（Figure 7(a)）。

S2E引入的**因果调节变量**是：在离线预训练之后，通过强化学习让模型在仿真环境中进行试错交互。碰撞惩罚、目标到达激励等奖励信号直接注入避障与动态交互能力，使模型从“看到”轨迹升级为“体验”交互后果。

### 创新点一：锚点引导的高斯混合动作表示（AGDM）

传统导航模型将动作分布建模为单峰高斯（ViNT）或离散动作类别（GNM），难以捕捉城市导航中天然存在的多模态性——例如在岔路口，左转、直行、右转可能都是合理选择。

AGDM通过以下机制实现多模态建模：
- 在机器人前方均匀采样**M个空间锚点**（通过K-Means获得），每个锚点对应一个高斯分量，代表一种高层行为意图。
- 模型对每个锚点预测其**轨迹得分** $q_m$（即该意图的置信度）、**归一化偏移量** $(\mu_x^m, \mu_y^m, \sigma_x^m, \sigma_y^m, \rho^m)$ 及**速度尺度** $v$。
- 最终动作分布表示为锚点引导的混合模型：

$$q(w_t|o_{t-k+1:t}) = \sum_{m=1}^M q_m \cdot \mathcal{N}_m(w_x-\mu_x^m,\sigma_x^m; w_y-\mu_y^m,\sigma_y^m; \rho^m)$$

训练时，选择与真值轨迹最匹配的锚点 $h$，对其施加负对数似然损失与分类损失：

$$\mathcal{L}_{nll,i} = -\log \mathcal{N}_h(\hat{w}_x-\mu_x^h,\sigma_x^h; \hat{w}_y-\mu_y^h,\sigma_y^h; \rho^h) - \log(q_h)$$

**消融证据**：将锚点数从1增加到64时，minADE从0.21降至0.09，mAP从0.57升至0.69（Table 7, App. D.5）。在障碍物场景中，多锚点混合建模（S2E-BC）相比单模回归（S2E-BC-Single）成功率提升9%，碰撞时间降低0.64（Table 8, App. D.5）。

### 创新点二：强化学习后训练替代监督微调

先前工作（GNM、ViNT、NoMaD）均停留在纯离线行为克隆阶段。S2E首次在导航基础模型中引入PPO强化学习后训练，利用仿真交互中的奖励信号：

$$R = R_{\mathcal{G}} + R_{\mathcal{R}} + R_{\mathcal{H}}$$

其中 $R_{\mathcal{G}}$ 为目标到达激励，$R_{\mathcal{R}}$ 为规则正则化（碰撞惩罚等），$R_{\mathcal{H}}$ 为人类相似性奖励。PPO训练目标为：

$$\min_{\Theta_r} \mathcal{L}_{ram} = -\mathcal{L}_{policy} + \alpha \mathcal{L}_{value} - \beta \mathcal{H}_\pi$$

其中 $\mathcal{H}_\pi$ 为GMM熵近似正则项，防止策略过早坍缩到单模：

$$\mathcal{H}_\pi \approx \sum_{m=1}^M q_m \cdot \left[\frac12 \log((2\pi e)^2 \sigma_x^{m2} \sigma_y^{m2})\right] - \sum_{m=1}^M q_m \log q_m$$

**决定性证据**：RL微调在不使用额外离线数据的情况下，将成功率绝对提升15%（Figure 7(a)）。更重要的是，RL后训练（S2E-RL）随训练计算量增加仍能维持或提升成功率，而监督微调（S2E-SFT）出现严重过拟合（Figure 7(b)），这揭示了RL在机器人学习中相比SFT的鲁棒性优势。

### 创新点三：残差注意力模块（RAM）保障安全微调

直接对预训练模型进行全参数RL微调面临两大风险：**灾难性遗忘**（破坏预训练获得的泛化视觉表征）和**梯度爆炸**（仿真-真实域差异导致训练不稳定）。

RAM的设计机制：
- **冻结**预训练的交叉注意力层参数 $\Theta_D$，保留其泛化知识。
- **并行训练**一个零初始化的副本分支，其输出通过门控线性层 $\mathcal{Z}$ 控制注入量：

$$Q' = \psi_D(Q;K,V;\Theta_D) + \mathcal{Z}(\psi_D(\mathcal{Z}(Q);K,V;\Theta_l))$$

- 零初始化保证训练初始时 $Q' = \psi_D(Q;K,V;\Theta_D)$，输出与预训练模型完全一致，随后渐进引入交互知识，形成结构性课程学习。

**消融证据**：RAM微调在NavBench-GS-Obstacle场景成功率（0.57）显著优于全参数微调DecFT-RL（0.42）和纯BC预训练S2E-BC（0.42），且显存占用更低（37GB vs 40GB），避免了梯度爆炸问题（Table 3, Figure 16, App. D.3）。

### 综合效能

在NavBench-GS基准的四种场景中，S2E的成功率和路径完成度全面超越GNM、ViNT、NoMaD、MBRA、CityWalker等先前模型，且训练数据量远少于部分方法（100h vs 700-2000h）。真实世界实验中，S2E-Full在轮式机器人障碍物+行人场景达到0.51成功率，较S2E-BC的0.33提升18个百分点（Table 2）。

**需注意的局限**：当前模型依赖纯视觉输入，缺乏显式3D深度或占据感知，在复杂障碍物场景中仍会出现碰撞；RL微调依赖仿真物理交互，仿真到真实的外观和动力学差异可能在边缘情况导致性能下降，但RAM冻结视觉编码器的设计已显著缓解该问题。



![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_0c7nAZjyr5/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of S2E framework. The model receives continuous RGB frames as context information, goal point or goal image as guidance, and uses spatial anchors as queries for prediction. First, context embeddings are fused via a self-attention module. The outputs are then used as keys (K) and values (V). Meanwhile, the anchor features $f _ { \mathcal { P } }$ serve as queries (Q). Subsequently, RAM blocks compute weighted features from K and V based on the anchor queries Q, and produce refined anchor features. A classification and a regression head decode the anchor features to predict scores and normalized trajectories with a velocity scale. In the pretraining stage, the model is trained end-...*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_0c7nAZjyr5/figures/005_Figure_4.jpg]]
*Figure 4: Illustration of anchor-guided distribution matching. (a) Illustration of anchor-guided Gaussian Mixture behaviors in a sidewalk scenario, where anchors guide diverse behavior generation. (b) Comparison of predicted action distributions between different representations*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_0c7nAZjyr5/figures/006_Figure_5.jpg]]
*Figure 5: Residual attention module*

### 核心瓶颈与设计动机

仅依靠离线视频数据的行为克隆存在两个根本性缺陷。第一，**因果反馈缺失**：模型在训练时从未经历碰撞或行人干扰的后果，因此无法习得障碍物规避、行人绕行等反应性安全行为。第二，**数据效率饱和**：将离线数据量从250k样本扩大到750k样本，导航成功率仅提升约2个百分点（Figure 7a），说明单纯堆砌被动观测数据已触及性能天花板。

S2E框架的核心洞察在于：**将离线预训练与在线强化学习解耦，通过试错交互注入安全行为，同时保护预训练阶段获得的泛化视觉表征不被破坏**。

### 整体管线架构

S2E采用两阶段混合学习范式，其完整管线如Figure 3所示：

**第一阶段：离线预训练（行为克隆）**。模型接收连续RGB帧作为历史上下文，以及目标点或目标图像作为导航指引。视觉编码器（冻结的DINOv3）将每帧图像编码为帧级特征（10个token）和路径级特征（64个token），随后通过时序自注意力模块融合历史帧信息，生成用于交叉注意力的键$K$和值$V$。以空间锚点为查询$Q$，交叉注意力层输出动作相关表示，最终由分类与回归头预测锚点引导的高斯混合分布参数。

**第二阶段：在线微调（强化学习）**。在仿真环境中，机器人根据预测的航点轨迹执行动作，接收来自环境的奖励信号——包括目标到达激励、碰撞惩罚等。微调仅作用于**残差注意力模块（RAM）**：冻结预训练的交叉注意力层，训练一个并行的、零初始化的副本分支，通过门控线性层渐进注入交互知识。RAM的输出为：

$$Q' = \psi_D(Q; K, V; \Theta_D) + \mathcal{Z}(\psi_D(\mathcal{Z}(Q); K, V; \Theta_l))$$

其中$\psi_D$为冻结的预训练交叉注意力，$\mathcal{Z}$为零初始化门控，$\Theta_l$为可训练的残差分支参数。零初始化保证了微调起始时刻RAM输出与原预训练模型完全一致，形成结构化的课程学习。

### 模块功能与数据流

| 模块 | 功能 | 状态 |
|------|------|------|
| DINOv3视觉编码器 | 将10帧历史图像编码为帧级和路径级特征 | 全程冻结 |
| 时序自注意力模块 | 融合历史帧上下文，输出键$K$和值$V$ | 预训练阶段训练 |
| RAM交叉注意力块 | 以锚点特征为查询$Q$，对$K$/$V$计算注意力 | RL阶段仅微调残差分支 |
| 分类与回归头 | 每锚点输出轨迹得分、高斯分量参数及速度尺度 | 两阶段均训练 |
| 可微运动控制器 | 将航点轨迹转换为轮式/四足机器人的控制指令 | 无参数 |

### 训练环境与评估基准

Figure 6展示了从数据到评估的完整链路。真实世界数据（Figure 6a）提供逼真的外观但缺乏物理交互；仿真环境（Figure 6b）补充了丰富的碰撞、行人互动等交互信号；NavBench-GS基准（Figure 6c）则利用3D高斯泼溅技术渲染高保真场景，在四种难度梯度（空旷/障碍物/行人/混合）下进行标准化评估。

### 关键设计选择

**动作分布的多模态建模**：与单峰高斯或离散动作类别不同，S2E采用锚点引导的高斯混合模型（AGDM），锚点通过K-Means从训练数据中获得，每个锚点对应一个高斯分量，模型预测各分量的均值、标准差、相关性及混合权重。这使模型能够同时表达“直行”“左转”“右转”等多种行为意图。

**微调模块的精确选择**：消融实验表明（Table 3），仅微调RAM残差分支的策略优于全参数微调（DecFT-RL）和纯行为克隆预训练（S2E-BC）。全参数微调在复杂障碍物场景中遭遇梯度爆炸和灾难性遗忘，而RAM通过冻结视觉编码器和原始交叉注意力层，将显存占用从40GB降至37GB，同时训练更稳定。



### 3.1 锚点引导的动作分布建模（AGDM）

离线预训练的核心挑战在于真实世界导航行为天然具有多模态性——同一观测下存在多种合理轨迹（如绕行左侧或右侧）。S2E通过**锚点引导的高斯混合模型（Anchor-Guided GMM）**来解决这一问题。

**锚点定义与作用。** 在机器人前进方向上均匀采样 $M$ 个空间锚点，每个锚点对应一种高层行为意图（如"左转绕行""直行通过""右转避让"）。锚点通过K-Means聚类获得，作为交叉注意力模块的查询向量 $Q$，引导模型从视觉特征中提取与该意图相关的动作信息。

**动作分布表示。** 给定观测历史 $o_{t-k+1:t}$，动作 $w_t$ 的分布建模为 $M$ 个高斯分量的混合：

$$q(w_t|o_{t-k+1:t}) = \sum_{m=1}^M q_m \cdot \mathcal{N}_m(w_x-\mu_x^m,\sigma_x^m;\ w_y-\mu_y^m,\sigma_y^m;\ \rho^m)$$

其中每个锚点 $m$ 对应一个二元高斯分量 $\mathcal{N}_m$，模型预测其均值 $(\mu_x^m, \mu_y^m)$、标准差 $(\sigma_x^m, \sigma_y^m)$、相关系数 $\rho^m$，以及该分量的混合权重（得分）$q_m$。这种表示同时捕捉了行为的多模态性和每个模态内的不确定性结构（Figure 4）。

**预训练损失函数。** 对于每个训练样本，选择与真值航点 $\hat{w}$ 最匹配的锚点 $h$（基于马氏距离），计算其负对数似然损失：

$$\mathcal{L}_{nll,i} = -\log \mathcal{N}_h(\hat{w}_x-\mu_x^h,\sigma_x^h;\ \hat{w}_y-\mu_y^h,\sigma_y^h;\ \rho^h) - \log(q_h)$$

第一项监督轨迹方向的精确回归，第二项监督锚点选择的分类准确性。此外，速度尺度 $v$ 通过独立的L2回归损失优化：

$$\mathcal{L}_{reg,i} = ||\hat{v} - v||_2^2$$

总预训练损失为上述两项的加权组合，端到端训练除视觉编码器外的全部参数。

---

### 3.2 残差注意力模块（RAM）

RL微调面临的核心矛盾是：仿真交互训练虽然能注入避障等反应性行为，但直接微调会导致对预训练泛化视觉表征的灾难性遗忘。S2E通过**残差注意力模块（RAM）**解决此问题（Figure 5）。

**结构设计。** RAM在预训练的交叉注意力层 $\psi_D$ 旁引入一个结构相同的可训练副本 $\psi_D(\cdot; \Theta_l)$，并通过零初始化门控线性层 $\mathcal{Z}$ 控制其输出：

$$Q' = \psi_D(Q; K, V; \Theta_D) + \mathcal{Z}\left(\psi_D(\mathcal{Z}(Q); K, V; \Theta_l)\right)$$

其中 $\Theta_D$ 为冻结的预训练参数，$\Theta_l$ 为可训练的残差分支参数。门控层 $\mathcal{Z}$ 的权重和偏置在RL开始时为零，保证初始输出 $Q'$ 完全等于预训练输出，从而在结构层面实现了"先保持后适应"的课程式学习。

**关键机制。** 该设计的核心优势在于：
- **避免遗忘：** 冻结原始交叉注意力层，保留预训练阶段学到的通用视觉-动作映射能力；
- **渐进注入：** 零初始化门控使残差分支从零开始学习仿真交互知识，训练初期不干扰已有表征，随着训练推进逐步注入避障、绕行等反应性行为；
- **训练稳定性：** 相比直接微调解码器层（DecFT-RL），RAM避免了梯度爆炸问题，且显存占用更低（37GB vs 40GB，Table 3）。

**RL训练目标。** 仅优化RAM残差分支参数 $\Theta_r$，采用PPO算法，总体目标为：

$$\min_{\Theta_r} \mathcal{L}_{ram} = -\mathcal{L}_{policy} + \alpha \mathcal{L}_{value} - \beta \mathcal{H}_\pi$$

其中 $\mathcal{L}_{policy}$ 为PPO-clip策略损失，$\mathcal{L}_{value}$ 为价值网络均方误差，$\mathcal{H}_\pi$ 为GMM策略的熵正则项。由于多模高斯混合没有闭式熵，采用忽略相关性后的下界近似（Appendix E.4）：

$$\mathcal{H}_\pi \approx \sum_{m=1}^M q_m \cdot \left[\frac{1}{2}\log((2\pi e)^2 \sigma_x^{m2} \sigma_y^{m2})\right] - \sum_{m=1}^M q_m \log q_m$$

熵奖励防止策略过早坍缩到单一锚点模态，维持行为多样性以应对仿真中多样的交互场景。



## 实验与关键发现

### 核心瓶颈与因果机制

S2E框架要解决的根本瓶颈是：**仅依靠离线视频数据的行为克隆（BC）忽略了环境交互中的因果反馈**，导致模型缺乏障碍物规避和行人绕行等反应性安全行为。同时，单纯扩大离线数据量带来的性能提升迅速饱和——从250k样本增加到750k样本，成功率仅提升2个百分点（Figure 7a）。这一发现直接指向了离线学习的边际收益递减问题。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_0c7nAZjyr5/figures/012_Figure_7.jpg]]
*Figure 7: Effectiveness of reinforcement learning. (a) Success rates of policies trained with varying amounts of data, showing gain from RL fine-tuning over only supervised learning. Dotted lines indicate the performance of prior methods. (b) Performance comparison between SFT and RL policies under increasing training cost*

因果调节变量是**在离线预训练之后引入强化学习（RL）在线交互训练**。通过仿真环境中试错获得的奖励信号（碰撞惩罚、目标到达激励等），避障与动态交互能力被直接注入模型。Figure 7a的核心证据表明：RL微调在不使用任何额外离线数据的情况下，将成功率绝对提升15%，这15个百分点的增益完全来自交互经验的注入，而非数据量的堆砌。

### NavBench-GS基准主结果

Table 1展示了S2E与7种导航基础模型在NavBench-GS四种场景下的全面对比。S2E在所有场景的成功率（SR）和路径完成度（RC）上均取得最优：

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_0c7nAZjyr5/figures/013_Table_1.jpg]]
*Table 1: NavBench-GS Benchmark. Comparison of navigation foundation models across four tasks*

| 场景 | S2E SR | 次优方法 SR | 增益 |
|------|--------|-------------|------|
| Empty（空旷） | 0.82 | 0.61（MBRA） | +0.21 |
| Obstacle（障碍物） | 0.57 | 0.32（CityWalker*） | +0.25 |
| Pedestrian（行人） | 0.74 | 0.55（CityWalker*） | +0.19 |
| Obstacle+Pedestrian（混合） | 0.51 | 0.33（CityWalker*） | +0.18 |

值得注意的是，S2E的训练数据量（100小时视频）远少于MBRA（700小时）和CityWalker（2000小时），却在所有场景取得显著优势。这验证了“交互质量优于数据数量”的核心主张。在最具挑战性的障碍物+行人混合场景中，S2E的碰撞时间（CT）仅为0.69，远低于CityWalker*的1.25，表明RL微调确实赋予了模型反应性避障能力。

真实世界实验（Table 2）进一步验证了这一结论：在轮式机器人上，S2E-Full的成功率为0.51，相比仅预训练的S2E-BC（0.33）提升18个百分点；在四足机器人上，成功率从0.38提升至0.63。

### RL vs SFT：扩展规律的鲁棒性差异

Figure 7b揭示了一个具有方法论意义的现象：**RL后训练随训练计算量增加仍能维持或提升成功率，而监督微调（S2E-SFT）出现严重过拟合**。随着训练FLOPs的增加，SFT的成功率先升后降，最终低于RL约15个百分点。这表明在机器人学习中，RL比SFT具有更强的扩展鲁棒性——监督信号来自固定离线分布，而RL信号来自持续的环境交互，天然避免了分布外泛化崩溃。

这一发现与Table 5（App. D.2）中在ViNT*基线上重复实验的结果一致：对ViNT*进行RL微调后，所有指标均显著提升，证明RL的有效性不限于特定模型架构。

### RAM消融：微调策略的关键选择

Table 3的消融实验对比了四种微调策略在NavBench-GS-Obstacle场景下的表现：

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_0c7nAZjyr5/figures/018_Table_3.jpg]]
*Table 3: Effectiveness of RAM*

| 方法 | SR ↑ | CT ↓ | 显存占用 |
|------|------|------|----------|
| S2E-BC（仅预训练） | 0.42 | 1.33 | — |
| S2E-SFT（全参数监督微调） | 0.45 | 1.10 | — |
| DecFT-RL（解码器层RL微调） | 0.47 | 0.92 | 40 GB |
| **S2E-Full（RAM-RL微调）** | **0.57** | **0.69** | **37 GB** |

仅微调残差注意力模块（RAM）的策略在成功率和碰撞避免上均优于全参数微调（DecFT-RL），且显存占用更低。App. D.3的Figure 16进一步显示，DecFT-RL在训练过程中出现梯度爆炸，而RAM微调保持稳定——这归功于零初始化门控线性层提供的结构性课程学习：微调初期残差分支贡献为零，模型输出完全等于冻结的预训练输出，随后渐进注入交互知识，避免了灾难性遗忘。

### 动作表示消融：锚点GMM的必要性

Table 4（NavBench-GS基准的动作表示消融）和Table 8（App. D.5）共同验证了锚点引导GMM的优势：

- **锚点数影响**（Table 7）：锚点数从1增加到64时，minADE从0.21降至0.09，mAP从0.57升至0.69，表明更多锚点能更好地覆盖多模态行为空间。
- **多模态 vs 单模态**（Table 8）：使用多锚点混合建模（S2E-BC）相比单模回归（S2E-BC-Single）在障碍物场景成功率提升9个百分点（0.42 vs 0.33），碰撞时间降低0.64。这证明城市导航中确实存在多模态行为分布（如绕行左侧或右侧），单模高斯无法有效捕捉。
- **与其他表示对比**（Table 4）：锚点GMM（S2E-BC）在障碍物场景的成功率（0.42）优于离散分类（0.34）和扩散策略（0.35），验证了结构化多模态建模的有效性。

### 仿真环境设计的影响

Table 9（App. D.6）的消融显示，重新设计的仿真环境布局（更符合真实城市结构）相比默认URBAN-SIM环境，在障碍物场景成功率从0.47提升至0.57。这强调了RL训练环境的空间分布对最终策略质量的重要影响——更贴近真实部署分布的仿真布局能产生更有效的交互经验。

### 定性结果与失败模式

Figure 14的轨迹对比显示，NoMaD和CityWalker在障碍物场景中频繁碰撞或停滞，而S2E能够平滑绕行。Figure 8的真实世界可视化进一步展示了S2E在行人密集场景中的合理绕行行为。

当前模型的主要失败模式集中在：**纯视觉输入缺乏显式3D深度感知**，在复杂障碍物场景中仍会出现碰撞（SR仅0.57）。S2E以局部导航为主，长距离任务依赖外部路径规划。RL微调依赖仿真物理交互，仿真到真实的外观和动力学差异可能在边缘情况导致性能下降，但RAM冻结视觉编码器的设计已显著缓解了该问题——App. D.4的Δ_feat分析显示，冻结编码器使真实-仿真特征偏移保持在较低水平。



## 定位与知识库关联

### 1. 与现有导航基础模型的关系

S2E 框架在**离线预训练 + 在线后训练**的混合范式上与现有导航基础模型形成明确的技术分水岭。

**离线行为克隆范式的瓶颈**。当前主流导航基础模型——**GNM** (Shah et al., 2023a)、**ViNT** (Shah et al., 2023b)、**NoMaD** (Sridhar et al., 2024)、**MBRA** 和 **CityWalker** (Liu et al., 2024b)——均采用纯离线行为克隆训练，仅从人类驾驶视频中学习驾驶行为。这一范式的根本缺陷在于：视频数据天然缺少环境交互中的**因果反馈**——模型无法观测到“如果当时选择另一条轨迹是否会撞上障碍物”的反事实结果。因此，这些模型虽能在空旷场景中表现良好，但在需要避障和行人绕行的场景中缺乏反应性安全行为。S2E 的核心突破在于将**强化学习在线交互训练**引入导航基础模型的后训练阶段，通过仿真环境中的试错奖励信号（碰撞惩罚、目标到达激励）直接注入避障与动态交互能力。

**数据扩展的边际收益递减**。S2E 的实证分析揭示了一个关键发现：单纯扩大离线数据量带来的性能提升迅速饱和。Figure 7(a) 显示，将离线训练样本从 250k 增加到 750k 仅带来约 2% 的成功率提升；而 RL 微调在不使用任何额外离线数据的情况下，将成功率绝对提升 15%。这一发现直接挑战了“更多数据即可解决交互问题”的假设，为导航基础模型的训练范式提供了新的经验规律。

**训练效率的显著优势**。在 NavBench-GS 基准（Table 1）的四种场景（空旷/障碍物/行人/混合）中，S2E 的成功率和路径完成度全面超越所有先前模型，且训练数据量远少于部分方法（S2E 使用 100h 视频数据，而 MBRA 使用 700h，CityWalker 使用 2000h）。这表明 S2E 的混合范式在数据效率和最终性能之间取得了更优的平衡。

### 2. 方法组件与相关技术的关系

**动作分布建模：从单峰到锚点引导的混合高斯**。先前导航模型通常采用单峰高斯（如 ViNT）或离散动作分类（如 GNM）来表示动作分布，这限制了模型对多模态驾驶行为的建模能力。S2E 提出的**锚点引导高斯混合模型（AGDM）**通过 K-Means 聚类获得空间锚点，每个锚点对应一个高斯分量，模型同时预测各分量的均值、方差、相关性及混合得分（Equation 1）。消融实验（App. D.5）证实，多锚点混合建模相比单模回归在障碍物场景中成功率提升 9%，碰撞时间降低 0.64。锚点数从 1 增加到 64 时，minADE 从 0.21 降至 0.09，mAP 从 0.57 升至 0.69，验证了多模态建模的持续收益。

**后训练范式：RL vs SFT 的鲁棒性差异**。S2E 的 Figure 7(b) 揭示了一个具有潜在普适性的发现：RL 后训练随训练计算量增加仍能维持或提升成功率，而监督微调（SFT）出现严重过拟合。这一现象可能源于 RL 的试错机制天然提供了分布外探索的正则化效应，而 SFT 在有限交互数据上容易坍缩到窄分布。该发现为机器人学习中的后训练范式选择提供了重要的经验指导，但其在导航之外的普适性仍需进一步验证。

**参数高效微调：RAM 与 LoRA/Adapter 的关系**。S2E 提出的**残差注意力模块（RAM）**在思想上与 LoRA 和 Adapter 等参数高效微调方法同源，但在设计上针对导航任务做了关键适配：RAM 冻结预训练的交叉注意力层，训练并行的零初始化副本，通过门控线性层渐进注入交互知识（Equation 6）。零初始化保证了微调起始时刻输出与预训练模型完全一致，形成结构化的课程学习。消融实验（Table 3）表明，RAM 微调优于全参数微调（DecFT-RL）和仅行为克隆预训练（S2E-BC），且在复杂障碍物场景中避免了梯度爆炸和灾难性遗忘，显存占用也更低（37GB vs 40GB）。

### 3. 适用边界与局限

**感知模态的局限**。S2E 当前依赖纯视觉输入（DINOv3 编码器），缺乏显式 3D 深度或占据感知。在复杂障碍物场景中，模型仍会出现碰撞——NavBench-GS-Obstacle 场景下 S2E 的成功率仅为 0.57，碰撞时间（CT）为 0.69，表明纯视觉策略在密集障碍物环境中的感知能力存在天花板。如何高效引入 3D 感知（如深度估计或占据网络）而不显著增加计算开销，是提升安全性的关键方向。

**导航范围的局限**。S2E 以局部导航（连续航点间）为主，长距离任务需依赖外部路径规划器，未构建全局地图或长期记忆。这限制了其在需要全局推理的大规模环境中的直接应用。

**仿真到真实的迁移风险**。RL 微调依赖于仿真的物理交互，仿真到真实的外观和动力学差异可能在边缘情况导致性能下降。尽管 RAM 冻结视觉编码器的设计已显著缓解该问题（通过保持预训练的泛化视觉表征），真实世界实验中 S2E 在轮式机器人障碍物+行人场景的成功率仅为 0.51，仍有较大提升空间。

### 4. 开放问题

1. **RL vs SFT 扩展规律的普适性**：Figure 7(b) 揭示的 RL 鲁棒性优势是否适用于更广泛的机器人任务（如操作、空中导航）？在更大规模模型和数据下，RL 微调是否也会面临收益递减，届时需要何种新的后训练范式？

2. **3D 感知的高效融合**：如何在不大幅增加计算开销的前提下，将深度估计或占据网络集成到 S2E 框架中，以进一步提升复杂障碍物场景的安全性？

3. **动作表示的维度扩展**：锚点引导的 GMM 目前用于 2D 航点预测，是否可以推广到更高维的动作空间（如全向移动底盘）或更复杂的动作参数化？

4. **全局规划与局部策略的协同**：S2E 的局部导航能力如何与全局路径规划器更紧密地耦合，以支持长距离、跨区域的自主导航任务？



## 原文 PDF

![[paperPDFs/ICLR_2026/From_Seeing_to_Experiencing_Scaling_Navigation_Foundation_Models_with_Reinforcement_Learning.pdf]]

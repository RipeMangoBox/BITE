---
title: "NavForesee: A Unified Vision-Language World Model for Hierarchical Planning and Dual-Horizon Navigation Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NavForesee_A_Unified_Vision_Language_World_Model_for_Hierarchical_Planning_and_Dual_Horizon_Navigation_Prediction.pdf
project_link: null
code_link: null
aliases:
- NavForesee
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将语言规划与世界模型预测统一在单个VLM中，通过层次化子目标规划和双时域环境特征预测，形成内部感知-规划-预测-动作的闭环。
primary_logic: 借鉴人类依靠里程碑进行导航的方式，高层次子指令规划与双时域（短期执行与长期里程碑）环境特征预测相互强化，为导航决策提供目标导向的指导。
claims:
- NavForesee在R2R-CE上达到66.2%成功率和78.4%的神谕成功率，显著优于缺乏规划或预测的变体。
- 同时移除深度和语义预测会造成明显的性能崩塌，表明两种模态的世界模型对导航均不可或缺。
- 层次化VLM规划、长期预测和短期预测三个模块中任何一个被移除，都会导致成功率大幅下降。
- R2R-CE Val-Unseen 上 Success Rate (SR) = 66.2%
---

# NavForesee: A Unified Vision-Language World Model for Hierarchical Planning and Dual-Horizon Navigation Prediction

> [!tip] 核心洞察
> 借鉴人类依靠里程碑进行导航的方式，高层次子指令规划与双时域（短期执行与长期里程碑）环境特征预测相互强化，为导航决策提供目标导向的指导。

| 字段 | 内容 |
|------|------|
| 中文题名 | NavForesee：面向分层规划与双时域导航预测的统一视觉-语言世界模型 |
| 英文题名 | NavForesee: A Unified Vision-Language World Model for Hierarchical Planning and Dual-Horizon Navigation Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01550) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NavForesee |
| Dataset | R2R-CE Val-Unseen, RxR-CE Val-Unseen |

> [!tip] 效果简介
> - R2R-CE Val-Unseen 上，Success Rate (SR) 66.2%；Oracle Success Rate (OSR) 78.4%；Navigation Error (NE) 3.94。
> - RxR-CE Val-Unseen 上，Success Rate (SR) 66.3%。

## 概要

视觉-语言导航中，长序列指令执行面临一个根本瓶颈：现有 VLM 代理缺乏层次化的语言规划能力和对未来的预测远见。这导致代理在未见环境中容易出现语义幻觉和空间漂移，难以维持稳健的长期决策。NavForesee 的核心洞察是借鉴人类依靠里程碑进行导航的方式——将高层次子指令规划与双时域环境特征预测相互强化，为导航决策提供目标导向的指导。

该方法将语言规划与世界模型预测统一在单个 VLM 框架内，通过层次化子目标规划和双时域（短期执行与长期里程碑）环境特征预测，形成感知-规划-预测-动作的内部闭环。在 R2R-CE 基准上，NavForesee 达到 66.2% 成功率和 78.4% 的神谕成功率，显著优于缺乏规划或预测的变体。消融实验进一步揭示：同时移除深度和语义预测会造成明显的性能崩塌，而层次化 VLM 规划、长期预测和短期预测三个模块中任何一个被移除，都会导致成功率大幅下降，验证了各组件对导航性能的不可或缺性。



视觉语言导航（VLN）要求具身智能体在未见环境中依据自然语言指令进行连续决策。现有VLN方法大致可分为两类：**端到端反应式策略**和**基于世界模型的规划方法**。前者直接从感知映射到动作，缺乏对未来环境状态的显式建模，在长序列任务中容易积累空间漂移和语义幻觉；后者虽引入了环境预测能力，但通常仅预测短期动力学，且预测目标局限于低层像素或隐空间状态，难以与高层语义规划形成有效闭环。

更深层的瓶颈在于：**长序列导航任务中，现有VLM代理缺乏层次化的语言规划和预测远见**。人类在陌生环境中导航时，会自然地将长指令分解为一系列里程碑（如“上楼梯→左转进入第二个门→走向床尾”），并在执行每一步时预测即将遇到的环境特征，从而提前调整行为。然而，现有VLM方法要么将完整指令一次性编码为固定上下文，要么仅生成扁平的动作序列，未能显式建模任务进展、追踪里程碑完成状态，也无法为未来决策提供目标导向的环境预测。

这一瓶颈导致两个关键缺口：
1. **规划缺口**：缺乏层次化子目标分解与进展追踪机制，使得模型在长指令执行中容易遗忘已完成步骤或偏离后续子任务。
2. **预测缺口**：现有世界模型预测范围过短（通常仅1-2步），且未区分短期执行与长期里程碑两个时域的需求差异——短期需要精确的深度和语义特征以指导即时动作，长期需要粗粒度的环境想象以维持全局方向感。

NavForesee的动机正是填补上述缺口：**将语言规划与世界模型预测统一在单个VLM中，通过层次化子目标规划和双时域环境特征预测，形成内部感知-规划-预测-动作的闭环**。核心洞见借鉴了人类依靠里程碑进行导航的方式——高层次子指令规划与双时域（短期执行与长期里程碑）环境特征预测相互强化，为导航决策提供目标导向的指导。这一设计使得模型不仅能“知道接下来要做什么”，还能“预见接下来会看到什么”，从而在未见环境中维持稳健的长期决策能力。



## 核心方法与创新机理

NavForesee 的核心创新在于将 **层次化语言规划** 与 **双时域世界模型预测** 统一于单个视觉-语言模型（VLM）框架内，形成感知-规划-预测-动作的闭环。与现有方法相比，它在四个关键维度上实现了范式转变。

### 1. 规划范式：从端到端反应式映射到层次化语言规划

传统 VLN 方法通常采用端到端反应式动作映射，或依赖独立的世界模型进行辅助预测，缺乏对长指令的结构化理解。NavForesee 引入 **层次化 VLM 规划**，使模型能够将长指令分解为里程碑式的子指令，追踪任务进度，并生成下一步子目标。这一设计直接解决了长序列导航中的语义漂移问题——消融实验表明，移除该模块后成功率从 66.2% 骤降至 52.6%（Table II），印证了层次化规划对维持长期决策一致性的关键作用。

### 2. 预测能力：从无预测/单一短期预测到双时域环境特征预测

现有世界模型方法或完全缺乏预测能力，或仅预测短期动力学。NavForesee 设计了 **双时域预测机制**：

- **短期预测**：固定步长 $k=5$ 个路径点，预测未来的深度图和语义特征（DINOv2、SAM）；
- **长期预测**：自适应里程碑 $M_t$ 的环境特征预测，为远距离决策提供目标导向的指导。

消融实验证实，同时移除深度和语义预测会造成显著性能崩塌（SR 从 66.2% 降至 60.0%，Table V），表明两种模态的世界模型对导航均不可或缺。

### 3. 动作策略输入：从仅依赖历史观测到融合双时域预测特征

传统动作策略仅依赖历史视觉观测。NavForesee 的动作策略通过 **逆动力学模型** 学习，其输入不仅包含历史观测 $O_{t-H:t}$ 和指令 $l$，还融合了短期 dream 嵌入 $E_S$ 和长期 dream 嵌入 $E_L$：

$$\hat{a}_{t:t+k} = M_{inv}(E_S, E_L \mid E_a)$$

这使得动作决策能够同时受益于即时环境预测和远期里程碑信息，形成从预测到执行的直接闭环。

### 4. 注意力机制：从标准自注意力到结构化双时域掩码

为支持双时域预测的因果依赖关系，NavForesee 设计了 **结构化注意力掩码**：
- 长期预测查询 $Q_L$ 可关注短期预测查询 $Q_S$，确保长期预测建立在对短期动态的理解之上；
- 深度查询与语义查询之间的交叉注意力被显式阻断，防止跨模态特征泄漏。

这一设计确保了双时域、双模态预测在统一骨干网络中的解耦与协同，是模型能够同时输出高质量深度图和语义特征的关键工程创新。

### 创新总结

NavForesee 的四个 changed slots 并非孤立改进，而是相互强化的系统设计：层次化规划提供语义层面的任务分解，双时域预测补充环境层面的几何与语义远见，结构化注意力保证多任务学习的稳定性，最终通过预测特征驱动的动作策略实现规划-预测-执行的统一。这种“规划指导预测，预测赋能行动”的闭环机制，是其在 R2R-CE 上取得 66.2% SR 和 78.4% OSR 的结构性原因。



NavForesee 构建了一个统一的视觉-语言世界模型，将**层次化语言规划**与**双时域环境特征预测**整合在单一 VLM 框架内，形成感知-规划-预测-动作的闭环。其核心设计思想借鉴了人类依靠里程碑进行导航的方式：高层次子指令规划为导航提供目标导向的指导，而双时域（短期执行与长期里程碑）环境特征预测则相互强化，共同支撑稳健的决策。

### 系统架构

模型以 **Qwen2.5-VL-3B-Instruct** 作为多模态骨干网络，在其基础上扩展了两个互补的功能模块（Figure 3）：

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of NavForesee. The model is built on the Qwen2.5-VL-3B-Instruct backbone, integrating two complementary functionalities: (1) VLM-based hierarchical planning and (2) world model-based dual-horizon visual prediction. For hierarchical planning, textual instruction and visual observations are encoded via Qwen’s original multimodal encoders to produce auto-regressive sub-goal plans. For prediction, a position encoder encodes the agent’s relative pose, and short- and long-horizon dream queries (depth and semantic subqueries) are appended to multimodal embeddings. These queries, processed through structured attention, feed lightweight convolutional decoders for environmental p...*

1. **VLM 层次化规划**：将长指令分解为序列化的子指令，跟踪任务进度并生成下一步子目标。
2. **世界模型双时域预测**：预测未来短期固定步长和长期自适应里程碑处的深度图与高层语义特征（DINOv2、SAM）。

### 输入输出流

整体 pipeline 的数据流如下：

**输入**包括三部分：自然语言导航指令 $l$、历史视觉观测序列 $O_{t-H:t}$（$H$ 帧 RGB 图像），以及智能体的相对位姿状态 $s_{t-H:t}$。

**层次化规划分支**将指令与视觉观测送入 Qwen 原始的多模态编码器，自回归地生成子目标规划文本。

**预测分支**则引入两组可学习的 **dream queries**——短期查询 $Q_S \in \mathbb{R}^{L \times d}$ 和长期查询 $Q_L \in \mathbb{R}^{L \times d}$，每组查询内部进一步分为深度子查询和语义子查询。位置编码器 $h(\cdot)$ 将智能体的相对位姿编码为状态嵌入，与多模态嵌入拼接后，在**结构化注意力掩码**的控制下，通过骨干网络依次提取：

$$
E_S = f(l, O_{t-H:t}, h(s_{t-H:t}) \mid Q_S)
$$
$$
E_L = f(l, O_{t-H:t}, h(s_{t-H:t}), Q_S \mid Q_L)
$$

结构化注意力掩码的设计遵循因果依赖原则：长期预测自然依赖于短期预测，因此 $Q_L$ 可以关注 $Q_S$，反之则被阻断；同时，深度查询与语义查询之间的交叉注意力被屏蔽，以防止跨模态特征泄漏。

提取的 dream 嵌入 $E_S$ 和 $E_L$ 分别送入**轻量世界模型解码器** $D(\cdot)$，输出双时域预测：

$$
p_{t+k} = D(E_S) = [d_p(t), c_p(t)]
$$
$$
p_{t+M_t} = D(E_L) = [d_p(t+M_t), c_p(t+M_t)]
$$

其中 $k$ 为短期预测的固定步长（最优值为 5 个路径点），$M_t$ 为长期预测的自适应里程碑位置。

**动作策略模块**将动作查询 $Q_a$ 经骨干网络生成动作嵌入 $E_a$，随后通过一个简单的 MLP（两层线性层加 ReLU 激活）构成的逆动力学模型 $M_{inv}$，结合双时域预测特征生成连续路径点序列：

$$
E_a = f(l, O_{t-H:t}, h(s_{t-H:t}), Q_S, Q_L \mid Q_a)
$$
$$
\hat{a}_{t:t+k} = M_{inv}(E_S, E_L \mid E_a)
$$

每个路径点定义为 $w_t = [x_t, y_t, \sin\theta_t, \cos\theta_t, c_t]$，包含平面位置、朝向角的正弦/余弦表示以及停止标志。

### 训练目标

总损失由三部分加权求和：

$$
L = \alpha L_d + \beta L_c + L_a
$$

其中 $L_d$ 为深度预测的 SiLogLoss，$L_c$ 为语义特征损失，$L_a$ 为动作预测的 MSE 损失。这一多任务训练目标使得规划、预测和动作执行三个环节在统一的 VLM 框架内协同优化，形成完整的闭环。

### 关键设计决策

框架的核心创新在于将原本分离的规划与预测功能统一到单个 VLM 中，通过 dream queries 和结构化注意力机制实现双时域预测的解耦与协同。消融实验（Table II）表明，移除层次化 VLM 规划、长期预测或短期预测三个模块中的任何一个，都会导致成功率大幅下降（如完全体 66.2% 降至无规划变体的 52.6%），验证了各模块在闭环中的不可或缺性。

### 补充图表

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/001_Figure_1.jpg]]
*Figure 1: NavForesee integrates hierarchical language planning with dual-horizon predictive foresight. The planner decomposes instructions into milestone-based sub-goals, while the world model predicts high-level environmental features for long- and short-term guidance, producing coherent navigation actions*



NavForesee 以 **Qwen2.5-VL-3B-Instruct** 为统一骨干，在其上扩展了两类互补功能模块：层次化 VLM 规划与双时域世界模型预测。以下聚焦核心计算模块及其关键公式。

### 1. 路径点参数化

动作空间被定义为一个连续路径点序列。每个路径点 $w_t$ 包含平面位置、朝向的三角函数表示以及停止标志：

$$w_{t} = \left[ x_{t}, y_{t}, \sin \theta_{t}, \cos \theta_{t}, c_{t} \right]$$

其中 $(x_t, y_t)$ 为平面坐标，$\theta_t$ 为朝向角，$c_t$ 为二值停止标志（Section III-A）。

### 2. 双时域 Dream 嵌入提取

为实现世界模型预测，NavForesee 引入两组可学习的 dream queries：短期查询 $Q_S \in \mathbb{R}^{L \times d}$ 和长期查询 $Q_L \in \mathbb{R}^{L \times d}$。在结构化注意力掩码控制下，Qwen2.5-VL 骨干依次提取时间对齐的特征嵌入：

$$E_{S} = f(l, O_{t-H:t}, h(s_{t-H:t}) \mid Q_{S})$$

$$E_{L} = f(l, O_{t-H:t}, h(s_{t-H:t}), Q_{S} \mid Q_{L})$$

其中 $l$ 为语言指令，$O_{t-H:t}$ 为历史视觉观测，$h(s_{t-H:t})$ 为位置编码器对智能体相对位姿的编码。长期嵌入 $E_L$ 的提取以短期查询 $Q_S$ 为条件，体现长时域预测对短时域预测的自然因果依赖（Section III-D）。

### 3. 双时域预测解码

轻量世界模型解码器 $D$ 将 dream 嵌入映射为深度图和语义特征（DINOv2、SAM）的预测：

$$p_{t+k} = D(E_{S}) = [d_{p}(t), c_{p}(t)]$$

$$p_{t+M_{t}} = D(E_{L}) = [d_{p}(t+M_{t}), c_{p}(t+M_{t})]$$

短期预测固定步长 $k$（消融实验确定 $k=5$ 最优），长期预测对应自适应里程碑时刻 $M_t$（Section III-D）。

### 4. 结构化注意力掩码

为保证双时域预测的因果合理性并防止模态间特征泄漏，NavForesee 设计了**结构化注意力掩码**（Figure 3）。其核心约束为：
- 长期预测查询可关注短期预测查询，但反之不可；
- 深度查询与语义查询之间的交叉注意力被完全阻断，防止跨模态信息泄漏（Section III-C）。

### 5. 动作策略学习

动作预测通过逆动力学模型实现。首先，动作查询 $Q_a$ 经骨干生成动作嵌入 $E_a$：

$$E_{a} = f(l, O_{t-H:t}, h(s_{t-H:t}), Q_{S}, Q_{L} \mid Q_{a})$$

随后，逆动力学模型 $M_{inv}$（一个简单的两层 MLP，中间含 ReLU 激活）以双时域 dream 嵌入 $E_S, E_L$ 为条件，预测连续动作序列 $\hat{a}_{t:t+k}$：

$$\hat{a}_{t:t+k} = M_{inv}(E_{S}, E_{L} \mid E_{a})$$

动作预测主要依赖双时域预测特征，而非直接依赖原始视觉嵌入，这强化了规划-预测-动作的闭环（Section III-E）。

### 6. 训练损失

总损失由深度预测损失 $L_d$（SiLogLoss）、语义特征损失 $L_c$ 和动作损失 $L_a$（MSE）加权求和：

$$L = \alpha L_{d} + \beta L_{c} + L_{a}$$

其中 $\alpha, \beta$ 为平衡系数，控制各损失项的贡献权重（Section III-F）。



## 实验与关键发现

### 核心性能瓶颈与因果验证

NavForesee 要解决的核心瓶颈是：长序列视觉语言导航（VLN）中，现有 VLM 代理缺乏层次化的语言规划与预测远见，导致语义幻觉和空间漂移，在未见环境中难以维持稳健的长期决策。其因果调节变量在于将语言规划与世界模型预测统一在单个 VLM 中，通过层次化子目标规划和双时域环境特征预测形成内部“感知-规划-预测-动作”闭环。以下实验围绕这一因果链条展开验证。

### 主结果：R2R-CE 与 RxR-CE 基准

Table I 给出了 NavForesee 在 R2R-CE 和 RxR-CE Val-Unseen 分割上与现有方法的全面对比。NavForesee 在 R2R-CE 上取得 **66.2% 成功率（SR）** 和 **78.4% 神谕成功率（OSR）**，在 RxR-CE 上取得 **66.3% SR**，两项 OSR 均为所有方法中最高。这表明统一的规划-预测框架在标准 VLN 基准上具有高度竞争力。

值得注意的是，OSR 的高值揭示了模型具备较强的路径规划能力——当提供神谕停止信号时，其路径质量显著优于端到端反应式方法。这直接验证了“层次化语言规划提供目标导向指导”的核心洞察。

### 消融实验：三大模块的因果贡献

Table II 对 NavForesee 的三个关键模块进行了消融：
- **移除层次化 VLM 规划**：SR 从 66.2% 骤降至 52.6%，降幅超过 13 个百分点。这是所有消融中最大的性能崩塌，证实语言规划是系统中最关键的组件。
- **移除长期预测**：SR 显著下降，说明仅靠短期预测无法为长距离导航提供足够的里程碑指导。
- **移除短期预测**：同样导致 SR 明显降低，表明即时环境感知对执行级决策不可或缺。

三者中任一缺失都会造成显著性能退化，验证了“规划-长期预测-短期预测”三者协同的必要性。

### 世界模型模态消融：深度与语义的互补性

Table V 针对世界模型预测的模态进行了消融：
- **完整模型**：SR 66.2%，导航误差（NE）3.94，SPL 59.7。
- **关闭深度预测**：SR 降至 61.8%，SPL 降低 4.8 点，说明几何信息对路径效率至关重要。
- **关闭语义预测**：SR 进一步降至 60.0%，NE 增高，表明语义特征对场景理解和目标识别不可或缺。

同时移除两种模态会造成更严重的性能崩塌，证实深度与语义预测在导航中具有互补且不可替代的作用。

### 短期预测窗口的选择

Table III 探索了短期预测窗口 k 的取值（3 至 5 个路径点）。结果表明 **k=5 取得最优 SR（66.2%）**，k=3 或 k=4 均导致性能下降。这与动作策略输出 5 个路径点的设计一致——预测窗口与动作空间对齐时，世界模型能为策略提供最有效的先验。

### 预测质量定量分析

Table IV 将模型的深度和语义预测与“身份基线”（直接复制对应时刻的真值）进行对比：
- **深度预测**：在 T+2 步内优于身份基线，说明模型具备短期几何推理能力。
- **语义特征预测（DINOv2 CosSim）**：在 T+3 步内显著优于身份基线，表明模型能有效推断未来时刻的高层语义布局。

这一结果验证了世界模型并非简单记忆，而是学习了环境的动力学规律。

### 定性分析：预测与规划的可视化

**Fig. 4** 展示了短期深度和语义预测的定性结果。模型能准确预测未来帧的深度分布和语义分割（基于 DINOv2 特征），即使面对楼梯、转弯等复杂几何结构也能保持合理的空间一致性。

**Fig. 5** 进一步展示了不同运动模式下的几何-语义特征想象能力：直线运动中的环境动态预测准确，转弯场景下泛化良好，甚至能从短暂的门缝一瞥中推断出房间内部的物体几何和深度分布。

**Fig. 7** 对比了短期与长期深度预测。短期预测在固定步长内保持较高精度，而长期预测在接近里程碑时退化较明显——这是方法的一个已知局限：无人为提供里程碑位置时，长期深度预测准确性下降。

**Fig. 6** 展示了分层规划的实际输出。模型能准确识别路径上的里程碑，总结已完成的子指令，并生成与上下文一致的下一子指令，验证了“借鉴人类依靠里程碑导航”的设计理念。

### 失败模式与局限性

1. **长期预测退化**：如图7所示，长期深度预测在接近里程碑时精度下降，可能影响复杂环境下的远期决策。
2. **特征级预测的限制**：世界模型预测依赖预计算特征（DINOv2、SAM、深度），未实现端到端像素级生成，限制了其在需要精细细节任务中的适用性。
3. **环境泛化未验证**：评估仅限于 R2R-CE 和 RxR-CE，未在动态物体、多人环境或其他 VLN 基准上测试。

### 公平性说明

所有训练仅使用公开的 R2R-CE 和 RxR-CE 数据集，评估遵循标准 Val-Unseen 分割。对比方法结果直接取自原文或通过统一协议复现。消融实验在完全相同的超参数和硬件条件下进行，确保变量控制。

### 补充图表

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/004_Table.jpg]]
*Table: I: Comparison with other methods on the Val-Unseen split of R2R-CE and RxR-CE TABLE II: Performance comparison between VLM planning and dual-horizon world model prediction*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/011_Table.jpg]]
*Table: V: Performance comparison between depth prediction and semantics prediction*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/010_Table.jpg]]
*Table: IV: Prediction Quality. Model (Pred) vs. Identity Baselines (copying GT at T { + i } ) as predictions for $T { \mathrm { + 5 } }$*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/006_Table.jpg]]
*Table: III: Ablation study of Short-term horizon*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/005_Figure_4.jpg]]
*Figure 4: Short-term depth and semantics predictions. From top to bottom: frames with timestamps, future ground truth frames with timestamps, future depth prediction for future frames, semantics predictions for future frames. Semantic features are DinoV2 features and visualized by a pretrained segmentation head. Instructions: UP the stairs. Turn to the left and enter into the second open door on the left. Walk towards the foot of the bed. Turn right and enter the open door to the bathroom*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/007_Figure_5.jpg]]
*Figure 5: NavForesee’s geometric-semantic feature imagination across different motion modes. The model accurately predicts environmental dynamics in straight motion, generalizes effectively to turning scenarios, and infers detailed object geometry and depth distribution from minimal visual input, such as a brief glimpse into a room*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/009_Figure_7.jpg]]
*Figure 7: Short-term and long-term depth predictions. From top to bottom: frames with timestamps, future ground truth frames with timestamps, short-term depth predictions for future frames, and long-term depth predictions for milestones. Instruction: ”Up the stairs. Turn to the left and enter the second open door on the left. Walk towards the foot of the bed. Turn right and enter the open door to the bathroom.”*

![[assets/figures/papers/paper_list_l2173_https_arxiv_org_abs_2512_01550/figures/008_Figure_6.jpg]]
*Figure 6: Hierarchical planning examples generated by NavForesee for the instruction ”Go up the stairs and straight forward the doorway. Turn right, move forward, and enter the doorway on the right. Move forward into the bedroom and stop in front of the toilet”. From top to bottom: frames with timestamps, global navigation map, and navigation planning outputs. NavForesee accurately identifies milestones along the route, summarizes completed sub-instructions, and generates the next sub-instruction in accordance with the instruction context*



## 定位与知识库关联

NavForesee 的核心贡献在于将**层次化语言规划**与**双时域世界模型预测**统一在单个 VLM 框架内，这一定位使其在方法谱系中处于视觉-语言导航（VLN）与基于模型强化学习的交汇地带。以下从规划范式、预测机制和动作策略三个维度，梳理其与前序工作的继承与断裂关系，并明确其适用边界与开放问题。

### 与现有 VLN 方法的关系

传统 VLN 方法可大致分为两类：**端到端反应式策略**与**显式规划式方法**。前者直接学习从视觉观测到动作的映射，缺乏对长期目标的显式建模；后者虽引入规划，但多依赖独立的规划模块或外部知识，规划与感知、执行之间的耦合较弱。NavForesee 的突破在于将规划内化于 VLM 的自回归生成过程中——模型不仅输出动作，更主动将长指令分解为里程碑式的子指令，持续追踪任务进度并生成下一子目标。这种“规划即生成”的范式，使得规划不再是与导航策略并行的辅助模块，而是与预测、动作形成闭环的核心组件。

在**世界模型预测**方面，现有工作或完全缺乏预测能力，或仅预测短期动力学（如单步或固定步长的未来帧）。NavForesee 的双时域设计——短期固定步长（$k=5$）的深度/语义预测与长期自适应里程碑的特征预测——填补了“执行级”与“里程碑级”预测之间的空白。消融实验（Table II）表明，移除任一预测时域均导致成功率显著下降，证实了双时域设计的必要性。

### 关键技术决策的因果机制

NavForesee 的性能提升可从以下因果链条理解：

1. **层次化规划 → 减少语义漂移**：长指令被分解为可管理的子指令后，模型在每个时刻只需关注局部子目标，降低了语言理解与视觉观测之间的语义对齐难度。Table II 显示，移除层次化 VLM 规划后成功率从 66.2% 骤降至 52.6%，这是所有消融中幅度最大的性能崩塌。

2. **双时域预测 → 提供目标导向的指导**：短期预测为即时动作选择提供局部环境先验，长期预测则提供里程碑级别的空间上下文。结构化注意力掩码确保长期预测因果依赖于短期预测，同时阻断深度与语义查询间的交叉注意，防止特征泄漏——这一设计是预测质量与动作策略稳健性的关键。

3. **多模态世界模型 → 互补的导航线索**：Table V 显示，单独移除深度预测使成功率降至 61.8%，单独移除语义预测进一步降至 60.0%，而同时移除两者则造成更严重的性能崩塌。这表明深度（几何结构）和语义（DINOv2、SAM 特征）为导航提供了互补且不可或缺的信息通道。

### 适用边界与局限

NavForesee 的设计存在明确的适用边界：

- **环境静态性假设**：世界模型预测依赖预计算的特征（DINOv2、SAM 和深度图），未涉及动态物体建模。在包含移动障碍物或行人的场景中，预测的准确性将显著退化，规划与执行之间的闭环可能断裂。
- **数据集依赖性**：训练仅使用 R2R-CE 和 RxR-CE 的公开数据，评估限于 Val-Unseen 分割。模型在更复杂的环境（如多楼层、室外混合场景）或多智能体交互场景中的泛化能力尚未验证。
- **长期预测的退化**：论文明确指出，长期深度预测在无人为提供里程碑位置时准确性下降，尤其在接近里程碑时退化较明显（Figure 7）。这意味着在需要精确空间推理的复杂导航中，长期预测的可靠性可能不足以支撑稳健决策。
- **特征级预测而非像素级生成**：世界模型解码器输出的是深度图和语义特征，而非 RGB 图像。这限制了其在需要精细视觉细节的任务（如物体识别、文字阅读）中的适用性。

### 开放问题

1. **预测-规划-控制的紧耦合**：当前框架中，预测特征通过逆动力学模型映射为动作，但规划子目标与预测特征之间的交互仍以隐式注意力为主。如何将预测的环境特征更直接地用于在线重规划或错误恢复（例如在预测到碰撞风险时提前调整子目标），是缩小规划与执行鸿沟的关键方向。

2. **动态环境扩展**：将双时域世界模型扩展至动态物体建模，需要处理物体运动的不确定性与智能体自身运动的耦合。这涉及预测目标的重新定义（从静态场景特征到时空特征）以及训练数据中动态标注的获取。

3. **规模化行为**：NavForesee 的性能随训练数据规模和多样性如何变化，是理解其泛化能力上限的核心问题。当前约 1.5M 训练样本的规模是否已触及瓶颈，还是仍有显著的规模化增益，需要进一步实验验证。

4. **像素级预测的可行性**：从特征级预测升级为像素级 RGB 生成，将显著增加计算开销和训练难度，但可能解锁更细粒度的视觉推理能力。这一方向的技术挑战在于如何平衡预测质量、推理速度与导航性能。

5. **跨具身迁移**：NavForesee 的规划-预测框架是否可迁移至其他具身任务（如物体操作、移动操作），以及如何适配不同的动作空间和感知模态，是验证其方法通用性的重要方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/NavForesee_A_Unified_Vision_Language_World_Model_for_Hierarchical_Planning_and_Dual_Horizon_Navigation_Prediction.pdf]]

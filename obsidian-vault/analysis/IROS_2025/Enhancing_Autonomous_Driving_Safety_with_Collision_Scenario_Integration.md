---
title: "Enhancing Autonomous Driving Safety with Collision Scenario Integration"
type: paper
paper_level: A
venue: IROS
year: 2025
pdf_ref: paperPDFs/IROS_2025/Enhancing_Autonomous_Driving_Safety_with_Collision_Scenario_Integration.pdf
code_link: null
project_link: https://nvlabs.github.io/SafeHydra/
aliases:
- EADSCSI
tags:
- IROS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过 CollisionGen 生成多样化碰撞场景，并利用 SafeFusion 的多目标知识蒸馏训练框架，以 PDM 模拟分数作为监督信号，使规划器无需真实避撞演示即可学习避撞。"
primary_logic: "合成碰撞场景与模拟器引导的训练相结合，能显著提高规划器在危险场景中的避撞能力，同时维持常规驾驶性能。"
claims:
- "SafeFusion 在 Collision2k 测试集上的总 PDM 分数达到 0.415，较 Hydra-GT 的 0.266 提升 56.0%。"
- "SafeFusion 将 OpenScene 困难样本的 TTC 从 0.007 提升至 0.308，总分从 0.264 提升至 0.400。"
- "在常规驾驶 OpenScene 测试集上，SafeFusion 总分 0.832 与 Hydra-GT 的 0.833 基本持平，无性能退化。"
- "Collision2k test set 上 PDM Total score = 0.415 (SafeFusion)"
---

# Enhancing Autonomous Driving Safety with Collision Scenario Integration

> [!tip] 核心洞察
> 合成碰撞场景与模拟器引导的训练相结合，能显著提高规划器在危险场景中的避撞能力，同时维持常规驾驶性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过碰撞场景集成增强自动驾驶安全性 |
| 英文题名 | Enhancing Autonomous Driving Safety with Collision Scenario Integration |
| 会议/期刊 | IROS 2025 |
| Links | [paper](https://arxiv.org/abs/2503.03957) · [Project](https://nvlabs.github.io/SafeHydra/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SafeFusion |
| Dataset | Collision2k test set, OpenScene test set (regular driving), OpenScene hard samples |

> [!tip] 效果简介
> - Collision2k test set 上，PDM Total score 为 0.415 (SafeFusion)，对比 0.266 (Hydra-GT)，变化 +0.149 (+56.0%)。
> - OpenScene test set (regular driving) 上，PDM Total score 为 0.832 (SafeFusion)，对比 0.833 (Hydra-GT)，变化 -0.001 (-0.1%)。
> - OpenScene hard samples 上，PDM Total score 为 0.400 (SafeFusion)，对比 0.264 (Hydra-GT)，变化 +0.136 (+51.5%)。

## 概要

自动驾驶规划器在常规驾驶场景中取得了显著进展，但在碰撞等危险场景下仍表现脆弱。其根本瓶颈在于：**真实碰撞数据极难收集，且即使获得碰撞数据，其中也缺乏成功的避撞轨迹演示**，导致依赖模仿学习的规划器无法从中学习避撞策略；同时，将碰撞数据与常规驾驶数据混合训练会引发数据不平衡与域差异问题。

针对上述挑战，本文提出了一套“生成-融合”框架，包含两个核心组件：

- **CollisionGen**：一个可扩展的碰撞场景生成管道，以大语言模型（GPT-4o）作为语言解释器，结合生成式变换器与基于规则的两阶段过滤（车道合规与碰撞检查、避撞可行性验证），从文本描述批量生成多样化、物理合理的碰撞场景，构建了 Collision2k 数据集。
- **SafeFusion**：一个多目标知识蒸馏训练框架，移除传统模仿学习组件，转而以 PDM 模拟器对规划轨迹词汇表的评分作为监督信号，使规划器无需真实避撞演示即可学习避撞。同时采用随机批次采样与自适应损失权重策略，缓解碰撞与常规数据的域差异。

**核心结论**：SafeFusion 在碰撞场景测试集 Collision2k 上的 PDM 总分达到 0.415，较 SOTA 学习型规划器 Hydra-GT（0.266）提升 **56.0%**；在 OpenScene 困难样本上，TTC 指标从 0.007 跃升至 0.308，总分提升 51.5%；而在常规驾驶 OpenScene 测试集上，总分 0.832 与 Hydra-GT 的 0.833 基本持平，**无性能退化**。

**方法定位**：SafeFusion 属于“数据增强 + 知识蒸馏”路线，与依赖真实避撞演示的模仿学习范式（如 PlanTF）和纯规则规划器（如 PDM-closed）形成互补。其核心创新在于将合成碰撞场景与模拟器引导的评分蒸馏相结合，为解决自动驾驶长尾安全问题提供了一条不依赖真实事故数据的可行路径。



### 自动驾驶安全的核心瓶颈

自动驾驶系统在常规驾驶场景中已取得显著进展，但在高风险碰撞场景中的表现仍然是制约其安全部署的关键瓶颈。这一困境的根源在于**数据层面的结构性缺陷**：真实世界的碰撞数据极难收集，且即便获得，这些数据也天然缺乏成功的避撞轨迹——碰撞事件本身意味着避撞失败。这使得当前主流的基于模仿学习的规划器（如 **Hydra-MDP**，Li et al., arXiv 2024）在碰撞场景中面临根本性失效：它们需要专家演示作为监督信号，而碰撞数据中恰恰不存在这样的演示。

更棘手的是，即使能够获取少量碰撞数据，将其与常规驾驶数据混合训练也会引发**数据不平衡**和**域差异**问题。常规场景数量远超碰撞场景，导致模型在优化过程中被常规样本主导，难以有效学习避撞行为；同时，两种场景的动力学分布差异使得简单的联合训练可能损害模型在常规场景中的已有性能。

### 现有方法的局限

现有应对方案存在明显不足。基于规则的规划器（如 **PDM-closed**，Dauner et al., CoRL 2023）虽然不依赖数据，但缺乏对复杂场景的泛化能力。基于学习的规划器则受限于训练数据的覆盖范围：它们从未见过碰撞场景，因此在危险情境中往往无法做出正确的避撞决策。如 Figure 1 所示，传统规划器在面临碰撞威胁时，要么反应迟钝，要么选择了错误的规避方向，最终导致碰撞。

### 本文动机

上述分析揭示了一个核心矛盾：**碰撞数据虽难以获取且缺乏避撞演示，但恰恰是提升规划器安全性的关键训练资源**。本文的动机由此展开：

1. **数据生成**：能否以可扩展的方式合成高质量、多样化的碰撞场景，绕过真实数据采集的瓶颈？
2. **训练范式**：能否设计一种不依赖避撞演示的学习框架，使规划器在仅有碰撞场景的条件下学会避撞？
3. **性能平衡**：能否在显著提升碰撞场景安全性的同时，不牺牲常规驾驶场景的已有性能？

这三个问题构成了本文工作的核心驱动力，分别对应 **CollisionGen** 碰撞场景生成管道和 **SafeFusion** 安全融合训练框架的设计目标。



## 核心方法与创新机理

SafeFusion 的核心创新在于**解耦了避撞能力对真实避撞轨迹演示的依赖**，通过合成碰撞数据与模拟器引导的知识蒸馏，使基于学习的规划器首次在无避撞演示的条件下获得显著的避撞能力。其关键突破体现在以下三个维度的“changed slots”上。

### 1. 训练数据：从纯常规驾驶到碰撞-常规混合采样

现有基于学习的规划器（如 **Hydra-GT** (Li et al., arXiv 2024)）仅使用常规驾驶数据集（如 OpenScene）训练，导致模型在危险场景中缺乏避撞行为的先验。SafeFusion 引入 CollisionGen 生成的 **Collision2k 碰撞数据集**，并设计了一种**随机批次采样策略**：每个训练批次以概率 $p_R$ 从常规数据 $D_R$ 采样、以概率 $p_C$ 从碰撞数据 $D_C$ 采样，同时为两类数据分配自适应损失权重 $w_R$ 和 $w_C$（Algorithm 1, Section III-B）。这一机制有效缓解了碰撞数据与常规数据之间的**数据不平衡和域差异**——消融实验证实，10:1 的随机批次比例在 Collision2k 和 OpenScene 上均取得最优总分，优于直接拼接训练和梯度累积策略（TABLE VI, TABLE VII）。

### 2. 学习范式：移除模仿学习，纯化知识蒸馏

Hydra-MDP 等基线方法依赖**模仿学习组件**，需要真实轨迹演示作为监督信号。然而碰撞数据中**缺乏成功的避撞轨迹**——碰撞场景的定义本身就意味着原始轨迹导致了碰撞，因此模仿学习在此类数据上完全失效。SafeFusion 的解决方案是**彻底移除模仿学习组件**（Section III-B），转而采用纯粹的**多目标知识蒸馏**：以 PDM 模拟器对轨迹词汇表中每条候选轨迹的模拟评分作为监督信号，通过二元交叉熵损失对齐模型预测的评分分布。这一范式转换使得规划器无需任何避撞演示即可学习避撞策略——消融实验表明，去除知识蒸馏后 Collision2k 总分从 0.415 降至 0.352，验证了蒸馏机制的必要性（TABLE VI）。

### 3. 避撞轨迹来源：从“需要演示”到“模拟器评分驱动”

传统方法要求数据集中存在成功的避撞轨迹作为训练目标，这在碰撞数据中天然缺失。SafeFusion 的关键突破在于**将避撞轨迹的发现从数据收集阶段转移至训练阶段**：CollisionGen 在过滤阶段通过 PDM 模拟器对轨迹词汇表进行**避撞可行性检查**（Collision Avoidance Feasibility Check, Section III-A.2），仅保留至少存在一条可行避撞轨迹的场景；在 SafeFusion 训练阶段，PDM 模拟器再次对所有候选轨迹评分，模型通过蒸馏学习预测这些评分，从而在推理时能够选择高分避撞轨迹。这一“生成-过滤-蒸馏”闭环构成了 SafeFusion 的**因果调节旋钮**：合成碰撞场景提供危险情境的暴露，模拟器评分提供避撞行为的隐式指导，知识蒸馏完成从模拟器知识到模型参数的迁移。

### 4. 创新效果：安全提升与常规性能保持的“双赢”

上述三个 changed slots 的协同作用产生了决定性证据：在 Collision2k 测试集上，SafeFusion 的总 PDM 分数达到 **0.415**，较 Hydra-GT 的 0.266 提升 **56.0%**（TABLE III）；在 OpenScene 困难样本上，TTC（Time-to-Collision）从 0.007 跃升至 **0.308**，总分从 0.264 提升至 0.400（TABLE V）；同时，在常规驾驶 OpenScene 测试集上，SafeFusion 总分 0.832 与 Hydra-GT 的 0.833 基本持平，**无性能退化**（TABLE IV）。这表明 SafeFusion 成功实现了碰撞场景安全性与常规场景驾驶能力的解耦优化。



![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_03957/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline begins by taking text descriptions of collision scenarios as input. A generator with a language interpreter and a generative transformer is then applied, followed by the use of predefined rules and a PDM simulator [46] to filter out qualified collision scenarios. These filtered scenarios are subsequently used for the training and evaluation processes of planners*

SafeFusion 的整体 pipeline 由两个核心子系统串联构成：**CollisionGen**（碰撞场景生成管道）与 **SafeFusion 训练框架**。前者负责从文本描述中合成多样化、可避撞的碰撞场景，后者将这些合成数据与常规驾驶数据融合，通过多目标知识蒸馏训练神经规划器。

### 管道总览

图 2 展示了从文本输入到可训练场景的完整流程：

1. **文本输入**：用户提供碰撞场景的自然语言描述 *C*（如“自车在十字路口左转时与直行车辆碰撞”）。
2. **CollisionGen 生成**：语言解释器将 *C* 转换为结构化表示 *z*，生成器结合地图 *m* 生成交通场景 *τ*。
3. **规则过滤**：依次通过车道合规与碰撞过滤、避撞可行性检查，筛选出既包含碰撞又存在可行避撞轨迹的场景。
4. **数据集构建**：通过 CollisionGen 生成 **Collision2k** 数据集，包含 2,000 个高质量碰撞场景（训练集 1,600，测试集 400）。
5. **SafeFusion 训练**：将碰撞数据 *D_C* 与常规驾驶数据 *D_R*（OpenScene）混合，采用随机批次采样与自适应损失权重，通过多目标知识蒸馏训练规划器。

### CollisionGen：碰撞场景生成管道

CollisionGen 由三个关键组件构成：

**生成器（Generator）**：基于 LCTGen 架构，包含四个子模块：
- **语言解释器**：通过 GPT-4o 将碰撞文本描述 *C* 转换为结构化表示 *z*，包含智能体数量、类型、碰撞位置、运动属性等语义信息。
- **地图编码器**：将车道段编码为嵌入向量 *e^lane*。
- **智能体查询生成器**：根据 *z* 生成智能体查询 *q^i*。
- **生成式 Transformer 与场景解码器**：交叉注意力机制融合查询与车道嵌入，预测智能体在车道段上的位置概率分布：

$$\hat{p}_i = \mathrm{softmax}(e_i^{agent} \times [e_1^{lane}, \ldots, e_S^{lane}]^T)$$

同时通过 K 路高斯混合模型预测智能体的航向、速度、尺寸等属性：

$$[\mu_i, \Sigma_i, \pi_i] = \mathrm{MLP}(q^i)$$

**过滤系统**：分两步筛选生成场景：
- **Step 1 — 车道合规与碰撞过滤**：确保车辆在车道中心线横向偏差阈值 *D_thres* 内，且航向与车道方向偏差在 *Θ_thres* 内；同时验证碰撞确实发生。
- **Step 2 — 避撞可行性检查**：利用 PDM 模拟器对轨迹词汇表中的所有候选轨迹评分，仅保留至少存在一条可行避撞轨迹的场景。

车道合规检查的核心公式为：

$$d_i = \min_{v_j \in m} \{ \mathrm{Distance}((x_i, y_i), v_j) \}$$

$$\theta_i = \arccos \frac{v_{ego,i} \cdot v_{lane,j^*}}{\|v_{ego,i}\| \|v_{lane,j^*}\|}$$

### SafeFusion：碰撞感知训练框架

SafeFusion 的核心设计解决两个瓶颈：碰撞数据缺乏成功避撞轨迹（无法直接用于模仿学习），以及碰撞与常规数据的域差异。

**架构设计**（图 3）：
- **环境编码器**：从常规数据 *D_R* 和碰撞数据 *D_C* 中分别提取环境特征 *F_env*。
- **轨迹 Transformer 解码器**：基于 Hydra-MDP 的规划词汇表解码器，生成候选轨迹的潜表示。
- **预测头与多目标知识蒸馏**：预测各候选轨迹的 PDM 模拟分数 *S_i^m*，通过二元交叉熵损失对齐真实模拟分数：

$$\mathcal{L} = -\sum_{m,i} \hat{S}_i^m \log S_i^m + (1 - \hat{S}_i^m) \log(1 - S_i^m)$$

其中 *m* 遍历 PDM 子指标（TTC、舒适度、自车进度等），*i* 遍历候选轨迹。

**关键设计决策**：
- **移除模仿学习组件**：Hydra-GT 原有的模仿学习分支被完全移除，纯以 PDM 模拟分数作为监督信号。这使得即使碰撞数据中无成功避撞演示，规划器也能通过模拟器评分学习避撞。
- **随机批次采样**：以概率 *p_R* 和 *p_C* 随机选择常规或碰撞批次，配合自适应损失权重 *w_R*、*w_C*，避免拼接训练中的梯度冲突与数据不平衡问题。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| CollisionGen 生成 | 文本描述 *C* + 地图 *m* | 交通场景 *τ* |
| 过滤 | 生成场景 *τ* + PDM 模拟器 | 合格碰撞场景 |
| SafeFusion 训练 | *D_R*（常规）+ *D_C*（碰撞） | 规划器模型权重 |
| 推理 | 环境观测 | 规划轨迹 |

整个管道实现了从文本描述到安全规划器的端到端闭环：合成数据弥补真实碰撞数据的稀缺，知识蒸馏克服避撞轨迹缺失的监督困境，随机批次采样解决域差异与不平衡问题。



SafeFusion 框架的核心由三个关键模块构成：**碰撞场景生成器 (CollisionGen)**、**环境编码与轨迹解码器**，以及**多目标知识蒸馏训练循环**。本节逐一展开其内部机制与关键公式。

### CollisionGen：从文本到可训练碰撞场景

CollisionGen 解决的核心瓶颈是碰撞数据稀缺且缺乏可行避撞轨迹的问题。其管道包含三个串联模块：

1. **语言解释器 (Language Interpreter)**：基于 GPT-4o，将碰撞文本描述 $C$ 转换为结构化表示 $z$。$z$ 编码了场景中智能体的数量、类型、交互关系及碰撞语义，作为后续生成的条件信号。

2. **生成器 (Generator)**：基于 LCTGen 架构，以 $z$ 和地图 $m$ 为输入，生成交通场景 $\tau$。其内部包含四个子模块：
   - **地图编码器 (Map Encoder)**：将车道段编码为嵌入序列 $[e_1^{lane}, \ldots, e_S^{lane}]$。
   - **智能体查询生成器 (Agent Query Generator)**：从 $z$ 生成智能体查询向量 $q^i$。
   - **生成式变换器 (Generative Transformer)**：以自回归方式解码场景。
   - **场景解码器 (Scene Decoder)**：输出每个智能体的位置、属性及轨迹。

   智能体位置通过 softmax 在车道段上预测：
   $$\hat{p}_i = \mathrm{softmax}(e_i^{agent} \times [e_1^{lane}, \ldots, e_S^{lane}]^T)$$
   其中 $e_i^{agent}$ 为第 $i$ 个智能体的查询嵌入，$\hat{p}_i$ 给出其在各车道段上的概率分布。

   智能体属性（航向、速度、尺寸、位置偏移）通过 $K$ 路高斯混合模型建模：
   $$[\mu_i, \Sigma_i, \pi_i] = \mathrm{MLP}(q^i)$$
   该设计允许生成多样化的智能体行为，同时保持对物理约束的遵从。

3. **规则过滤 (Filtering)**：生成场景需通过两步筛选才能进入训练集。
   - **步骤一：车道合规与碰撞验证**。对每个时间步 $i$，计算车辆位置到最近车道段中心线的垂直距离：
     $$d_i = \min_{v_j \in m} \{ \mathrm{Distance}((x_i, y_i), v_j) \}$$
     以及车辆航向与最近车道方向的角度偏差：
     $$\theta_i = \arccos \frac{v_{ego,i} \cdot v_{lane,j^*}}{\|v_{ego,i}\| \|v_{lane,j^*}\|}$$
     要求 $d_i \leq D_{thres}$ 且 $\theta_i \leq \Theta_{thres}$，同时验证碰撞确实发生。
   - **步骤二：避撞可行性检查**。利用 PDM 模拟器对预定义的轨迹词汇表进行评分，仅保留至少存在一条可行避撞轨迹的场景。这一步至关重要：它确保了即使碰撞数据中不包含避撞演示，规划器仍有可学习的“安全出口”。

### SafeFusion 训练框架：统一碰撞与常规数据

SafeFusion 的核心设计在于通过**多目标知识蒸馏**将碰撞数据无缝融入训练，无需依赖模仿学习。

**环境编码器**分别从常规数据集 $D_R$ 和碰撞数据集 $D_C$ 中提取环境特征 $F_{env}$，共享编码器权重以保证特征空间的一致性。

**轨迹变换器解码器**基于 Hydra-MDP 的规划词汇表架构，生成候选轨迹的潜表示。与 Hydra-MDP 的关键区别在于：SafeFusion **移除了模仿学习组件**，完全依赖 PDM 模拟器提供的评分信号作为监督。这一设计直接解决了碰撞数据中缺乏真实避撞轨迹的问题——模型不再需要“正确的”演示，只需学会预测哪些轨迹在模拟器中得分更高。

**预测头与多目标知识蒸馏**：对每条候选轨迹 $i$ 和每个评分维度 $m$（包括无责碰撞 NC、可行驶区域合规 DAC、碰撞时间 TTC、舒适度 C、自车进度 EP），模型输出预测分数 $S_i^m$。训练目标是最小化预测分数与 PDM 模拟器真实评分 $\hat{S}_i^m$ 之间的二元交叉熵：
$$\mathcal{L} = -\sum_{m,i} \hat{S}_i^m \log S_i^m + (1 - \hat{S}_i^m) \log(1 - S_i^m)$$

PDM 总分则通过以下公式聚合各维度：
$$PDM_{score} = NC \cdot DAC \cdot DDC \cdot \frac{(5 \cdot TTC + 2 \cdot C + 5 \cdot EP)}{12}$$
其中 NC 和 DAC 作为乘性因子起到“一票否决”作用（任何碰撞或偏离可行驶区域都会将总分归零），而 TTC、C、EP 通过加权平均贡献安全、舒适与效率维度。

**混合批次训练循环**：为处理碰撞数据与常规数据之间的分布差异，SafeFusion 采用随机批次采样策略。以概率 $p_R$ 从 $D_R$ 采样，以概率 $p_C$ 从 $D_C$ 采样，并分别施加自适应损失权重 $w_R$ 和 $w_C$。消融实验（TABLE VI, TABLE VII）表明，10:1 的采样比例在碰撞性能和常规驾驶性能之间取得最佳平衡，显著优于简单拼接训练或梯度累积方案。

### 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|----------|------|
| $\hat{p}_i = \mathrm{softmax}(e_i^{agent} \times [e_1^{lane}, \ldots, e_S^{lane}]^T)$ | $e_i^{agent}$：智能体查询嵌入；$e_j^{lane}$：车道段嵌入 | 预测智能体在车道段上的位置分布 |
| $[\mu_i, \Sigma_i, \pi_i] = \mathrm{MLP}(q^i)$ | $q^i$：智能体查询向量；$\mu_i, \Sigma_i, \pi_i$：GMM 参数 | 生成多样化的智能体属性 |
| $d_i = \min_{v_j \in m} \{ \mathrm{Distance}((x_i, y_i), v_j) \}$ | $(x_i, y_i)$：车辆位置；$v_j$：车道段 | 车道合规检查：横向偏差 |
| $\theta_i = \arccos \frac{v_{ego,i} \cdot v_{lane,j^*}}{\|v_{ego,i}\| \|v_{lane,j^*}\|}$ | $v_{ego,i}$：车辆航向；$v_{lane,j^*}$：最近车道方向 | 车道合规检查：航向对齐 |
| $\mathcal{L} = -\sum_{m,i} \hat{S}_i^m \log S_i^m + (1 - \hat{S}_i^m) \log(1 - S_i^m)$ | $S_i^m$：预测评分；$\hat{S}_i^m$：模拟器真实评分 | 多目标知识蒸馏损失 |
| $PDM_{score} = NC \cdot DAC \cdot DDC \cdot \frac{(5 \cdot TTC + 2 \cdot C + 5 \cdot EP)}{12}$ | NC：无责碰撞；DAC：可行驶区域合规；DDC：方向合规；TTC：碰撞时间；C：舒适度；EP：自车进度 | 综合规划评分 |

### 方法边界与未解问题

当前框架存在几个明确的局限：自适应损失权重 $w_R$ 和 $w_C$ 的具体计算公式在论文中未给出，需手动验证；过滤阈值 $D_{thres}$ 和 $\Theta_{thres}$ 为手工设定，缺乏自适应机制；轨迹词汇表固定，可能限制在完全未预见场景中的灵活性。此外，整个管道仅在合成数据上验证，真实世界碰撞数据下的表现仍是开放问题。



## 实验与关键发现

### 实验设置

SafeFusion 的评估在两个互补的测试集上进行：**Collision2k** 测试集（合成碰撞场景）和 **OpenScene** 测试集（真实常规驾驶场景）。Collision2k 由 CollisionGen 生成并经两步过滤后构建，专门用于衡量规划器在碰撞临界情况下的避撞能力。OpenScene 则用于验证方法是否在常规驾驶性能上出现退化。

评估指标采用 **PDM 评分**（Dauner et al., CoRL 2023），其综合了无过错碰撞（NC）、可行驶区域合规（DAC）、碰撞时间（TTC）、舒适度（C）和自车进度（EP）：

$$PDM_{score} = NC \cdot DAC \cdot DDC \cdot \frac{(5 \cdot TTC + 2 \cdot C + 5 \cdot EP)}{12}$$

基线方法包括基于规则的 **PDM-closed**（Dauner et al., CoRL 2023）、基于变换器的 **PlanTF**，以及基于学习的 SOTA 规划器 **Hydra-GT**（Li et al., arXiv 2024）。SafeFusion 以 Hydra-GT 的架构为基础，但移除了其模仿学习组件，仅保留多目标知识蒸馏。

### 主实验结果

**碰撞场景性能（TABLE III）。** SafeFusion 在 Collision2k 测试集上的总 PDM 分数达到 **0.415**，较 Hydra-GT 的 0.266 提升 **56.0%**（+0.149）。这一提升主要源于 TTC 子指标的显著改善——SafeFusion 的 TTC 为 0.308，而 Hydra-GT 仅为 0.007，表明模型在无真实避撞演示的情况下成功学会了避撞策略。PDM-closed 作为基于规则的基线获得 0.515，但其依赖手工规则，缺乏学习方法的泛化性。

**常规驾驶性能保持（TABLE IV）。** 在 OpenScene 测试集上，SafeFusion 的总分 0.832 与 Hydra-GT 的 0.833 基本持平（-0.1%），证明碰撞数据集成训练未导致常规驾驶能力退化。这一结果验证了随机批次采样和自适应损失权重策略在平衡两类数据时的有效性。

**困难样本泛化（TABLE V）。** OpenScene 困难样本子集上的测试进一步揭示了 SafeFusion 的鲁棒性。SafeFusion 的总分从 Hydra-GT 的 0.264 提升至 **0.400**（+51.5%），TTC 从 0.007 跃升至 **0.308**。这表明即使在未专门训练的真实困难场景中，模型仍能迁移避撞能力。

### 消融实验

**训练数据混合策略（TABLE VI, TABLE VII）。** 对比了三种混合策略：拼接训练（concatenation）、梯度累积（gradient accumulation）和随机批次选择（random batch selection，比例 10:1）。随机批次选择在 Collision2k（0.415）和 OpenScene（0.832）上均获得最佳总分，验证了其在缓解数据不平衡和域差异方面的优势。

**知识蒸馏的必要性（TABLE VI）。** 移除知识蒸馏组件后，Collision2k 总分从 0.415 降至 **0.352**，降幅达 15.2%。这确认了 PDM 模拟分数作为监督信号的核心作用——在碰撞数据缺乏真实避撞轨迹的情况下，知识蒸馏是唯一有效的学习通路。

### 生成质量与过滤效率

**场景真实度（TABLE I）。** CollisionGen 在 MMD² 位置指标上达到 0.0612，mADE 为 1.189，与 TrafficGen 和 LCTGen 等通用生成模型相比具有竞争力，证明专门设计的碰撞提示系统和过滤管道未损害生成场景的物理真实度。

**过滤管道效率（TABLE II）。** 从 53,510 个生成场景出发，第一步车道合规与碰撞过滤后保留 3,126 个场景（通过率约 5.8%），第二步避撞可行性检查后最终获得 **1,516 个有效碰撞场景**（通过率约 2.8%）。低通过率反映了生成高质量、可学习避撞的碰撞场景的内在难度，也凸显了过滤管道在数据集构建中的关键作用。

### 失败模式与局限

尽管 SafeFusion 在碰撞场景中取得了显著提升，其 Collision2k 总分 0.415 仍低于 PDM-closed 的 0.515，表明基于学习的方法在极端安全临界情况下与规则方法之间仍存在差距。此外，所有评估均在合成数据上进行，缺少真实世界碰撞数据集的验证。碰撞生成管道依赖 GPT-4o 进行文本解释，可能引入语言模型偏差；过滤阈值（D_thres, Θ_thres）为手工设定，对不同地理区域的泛化性尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_03957/figures/004_Table.jpg]]
*Table: I: TRAFFIC SCENARIO GENERATION REALISM EVALUATION. TABLE II: SUCCESSFUL COLLISION SCENARIOS AFTER TWO FILTERING STEPS FROM 53,510 TOTAL SCENARIOS. STEP 1 IS LANE COMPLIANCE AND COLLISION FILTERING. STEP 2 IS COLLISION AVOIDANCE FEASIBILITY CHECK*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_03957/figures/006_Table.jpg]]
*Table: III: EVALUATION ON COLLISION SCENARIOS FROM THE COLLISION2K TEST SET. “IMI.” STANDS FOR IMITATION LEARNING, AND “KD” STANDS FOR KNOWLEDGE DISTILLATION. THESE ABBREVIATIONS ALSO APPLY TO THE TABLE BELOW. OUR METHOD SIGNIFICANTLY ENHANCES THE PLANNER’S PERFORMANCE IN COLLISION CORNER CASES AND SURPASSES PREVIOUS APPROACHES BY A NOTABLE MARGIN IN PDM SCORES. TABLE IV: EVALUATION ON REGULAR DRIVING SCENARIOS FROM THE OPENSCENE TEST SET. OUR METHOD PRESERVES THE PLANNER’S PERFORMANCE IN REGULAR DRIVING SCENARIOS, EVEN AFTER TARGETED TRAINING FOCUSED ON COLLISION SCENARIOS. TABLE V: PERFORMANCE ON OPENSCENE HARD SAMPLES. TABLE VI: ABLATION STUDY ON COLLISION2K TEST SET. TABLE VII: ABLATION STUDY...*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_03957/figures/005_Table.jpg]]



## 定位与知识库关联

### 1. 基线关系与差异化

SafeFusion 的核心设计建立在对现有基于学习的规划器两大瓶颈的回应之上：碰撞数据稀缺性，以及碰撞数据中缺乏成功避撞轨迹导致模仿学习失效。其基线关系可概括为以下三条脉络。

**相对于 Hydra-MDP 系列（Li et al., arXiv 2024 ）**：SafeFusion 直接继承 Hydra-MDP 的规划轨迹词汇表解码器与多目标知识蒸馏策略，但做出了关键性减法——**完全移除模仿学习组件**。在 Hydra-GT 中，模仿学习要求提供真实避撞轨迹作为监督信号，这在碰撞数据中天然缺失。SafeFusion 转而仅依赖 PDM 模拟器对轨迹词汇表进行评分，以二元交叉熵损失对齐预测分数与模拟分数，从而绕过对演示数据的依赖。这一改动使得碰撞数据首次可被有效纳入训练，而不需要人工采集危险的避撞演示。在 Collision2k 测试集上，SafeFusion（无模仿学习、仅知识蒸馏）的 PDM 总分达到 0.415，较 Hydra-GT（模仿学习 + 知识蒸馏）的 0.266 提升 56.0%（TABLE III），验证了该设计选择的正确性。

**相对于 PDM-closed（Dauner et al., CoRL 2023 ）**：PDM-closed 是基于规则的规划器，不依赖学习，因此在碰撞场景中天然具有避撞能力（Collision2k 总分 0.378，TABLE III）。SafeFusion 作为学习型方法，在该指标上超越了规则基线（0.415 vs. 0.378），证明合成碰撞数据与知识蒸馏的结合能够使学习型规划器在安全性上匹敌甚至超越手工规则，同时保留学习方法的泛化潜力。

**相对于 PlanTF**：PlanTF 作为基于 Transformer 的规划器，在 Collision2k 上仅获得 0.261 的 PDM 总分（TABLE III），与 Hydra-GT 接近但显著低于 SafeFusion。该结果表明，仅依靠架构改进而不解决碰撞数据缺失与训练范式适配问题，难以在危险场景中获得实质收益。SafeFusion 的增益来源是**数据层面**（CollisionGen 生成的 Collision2k）与**训练范式层面**（多目标知识蒸馏 + 混合批次采样）的联合改进，而非模型架构创新。

### 2. 适用边界

SafeFusion 的有效性建立在以下前提之上，这些前提同时划定了其适用边界：

- **数据层面**：依赖 CollisionGen 生成的合成碰撞数据。生成管道采用 GPT-4o 进行文本到结构化表示的转换，并以 LCTGen 为基础生成交通场景。生成质量受限于语言模型的文本理解偏差和生成模型的分布覆盖能力。当目标碰撞类型超出文本描述系统的表达能力时（如极端物理交互、多车连锁碰撞），生成质量可能下降。
- **过滤机制**：场景过滤依赖手工设定的阈值 D_thres（横向偏差）和 Θ_thres（航向角偏差），以及 PDM 模拟器的可行性检查。阈值选择直接影响保留场景的多样性与质量——过严可能滤除有效的边缘案例，过松则引入噪声。论文未报告阈值敏感性分析。
- **规划器架构**：SafeFusion 基于固定轨迹词汇表进行候选轨迹评分，这限制了规划器在未预见场景中的行为灵活性。当最优避撞轨迹不在词汇表内时，规划器只能选择词汇表中最接近的次优解，可能无法实现真正最优的避撞行为。
- **场景类型**：当前框架仅针对碰撞场景设计。在极端天气、传感器失效、道路结构突变等其他危险场景中的有效性未经验证，需要额外的场景生成管道与评分机制适配。
- **验证范围**：所有实验均在合成数据（Collision2k）和真实常规驾驶数据（OpenScene）上进行，缺少真实世界碰撞数据集的验证。合成数据与真实碰撞数据之间的域差异可能导致性能退化，这一风险尚未量化。

### 3. 局限与开放问题

**已识别的局限**：

1. **真实碰撞数据验证缺失**：论文明确指出仅在合成碰撞数据上训练与评估，缺少真实世界碰撞数据集验证。合成场景虽然在 MMD² 指标上接近真实数据分布（TABLE I，MMD Position 0.0612），但分布相似性不等价于避撞行为的可迁移性。
2. **场景类型单一**：仅关注碰撞场景，未扩展到其他危险情况（如极端天气、传感器故障、道路施工等）。框架的模块化设计（文本描述 → 场景生成 → 过滤 → 训练）理论上可扩展，但需要为每类危险场景设计新的提示系统与过滤规则。
3. **生成管道依赖**：碰撞生成管道依赖 GPT-4o 进行文本解释，可能引入语言模型的系统性偏差；过滤阈值 D_thres 和 Θ_thres 为手工设定，缺乏自适应机制。
4. **词汇表约束**：基于固定轨迹词汇表的规划框架可能限制在未预见场景中的灵活性，最优避撞轨迹可能超出词汇表覆盖范围。

**开放问题**：

1. **真实世界迁移性**：SafeFusion 在真实世界碰撞数据集上的表现如何？合成-真实的域差异是否会导致显著的性能退化？需要真实碰撞数据集的采集与验证。
2. **自适应损失权重**：论文提到使用自适应损失权重 w_R 和 w_C 来平衡常规数据与碰撞数据的训练，但未公开具体公式。该权重的设计原则是什么？是否随训练进程动态调整？这直接影响两类数据在优化过程中的相对影响力。
3. **最佳混合比例**：随机批次采样比例（论文中常规:碰撞 = 10:1 在消融实验中表现最优，TABLE VI 和 TABLE VII）是否随数据集规模、碰撞场景多样性、或常规数据分布而变化？是否存在更系统的方法来确定该比例？
4. **危险场景泛化**：如何将 SafeFusion 的训练范式扩展到碰撞以外的危险场景？是否需要为每类危险场景设计独立的评分机制，还是 PDM 模拟器的通用性足以覆盖？
5. **词汇表扩展**：能否通过动态词汇表生成或在线轨迹优化来突破固定词汇表的限制，在保持知识蒸馏有效性的同时提升避撞灵活性？
6. **过滤阈值敏感性**：D_thres 和 Θ_thres 的变化如何影响最终规划器的安全性与常规驾驶性能？是否存在一个帕累托前沿，需要在场景多样性与数据质量之间做出权衡？



## 原文 PDF

![[paperPDFs/IROS_2025/Enhancing_Autonomous_Driving_Safety_with_Collision_Scenario_Integration.pdf]]

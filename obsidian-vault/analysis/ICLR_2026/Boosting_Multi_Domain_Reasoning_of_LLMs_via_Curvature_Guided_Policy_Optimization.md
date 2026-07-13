---
title: "Boosting Multi-Domain Reasoning of LLMs via Curvature-Guided Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Boosting_Multi_Domain_Reasoning_of_LLMs_via_Curvature_Guided_Policy_Optimization.pdf
project_link: null
code_link: null
openreview_forum_id: R2EZtdHWJT
aliases:
- CGPOC
- BMDRLCGPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "随机顺序的跨领域更新引入隐式曲率-梯度交互，使优化路径趋向梯度对齐区域。"
primary_logic: "受牛顿法启发，通过随机化领域更新顺序可近似黑塞矩阵与梯度的交叉乘积，无需显式计算二阶信息，从而在极低额外开销下促进跨领域协调。"
claims:
- "CGPO在3B和7B模型上均取得最佳平均多领域性能。"
- "随机化领域顺序的CGPO显著优于固定顺序版本。"
- "混合系数α=1.2在多项指标上取得最优或次优结果。"
- "CGPO在大规模模型（32B/72B）上的额外耗时仅约5%，远低于联合学习。"
---

# Boosting Multi-Domain Reasoning of LLMs via Curvature-Guided Policy Optimization

> [!tip] 核心洞察
> 受牛顿法启发，通过随机化领域更新顺序可近似黑塞矩阵与梯度的交叉乘积，无需显式计算二阶信息，从而在极低额外开销下促进跨领域协调。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于曲率引导策略优化的多领域推理增强 |
| 英文题名 | Boosting Multi-Domain Reasoning of LLMs via Curvature-Guided Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=R2EZtdHWJT) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Curvature-Guided Policy Optimization (CGPO) |
| Dataset | Multi-domain (Math, Code, Science, Writing) – Qwen2.5-3B, Writing) – Qwen2.5-7B, Math+Code subset (Qwen2.5-7B), Math+Creative Writing subset (Qwen2.5-7B) |

> [!tip] 效果简介
> - Multi-domain (Math, Code, Science, Writing) – Qwen2.5-3B 上，AVG score (Table 1) 为 50.42，对比 best baseline (likely Joint Learning or FAMO)，变化 significant。
> - Multi-domain (Math, Code, Science, Writing) – Qwen2.5-7B 上，AVG score (Table 1) 为 59.59，对比 best baseline，变化 significant。
> - Math+Code subset (Qwen2.5-7B) 上，AVG (MATH500, AMC, HumanEval, MBPP) 为 73.56，对比 72.26 (FAMO)，变化 +1.30。

## 概要

多领域大语言模型（LLM）强化学习面临一个核心瓶颈：不同领域（如数学推理、代码生成、科学问答、创意写作）的梯度更新方向往往相互冲突，导致参数更新彼此抵消——一个领域的性能提升常以其他领域性能下降为代价。现有方法或直接混合数据联合训练，或通过动态损失加权平衡各领域进展，但均未有效利用参数空间的曲率信息来协调跨领域优化路径。

**Curvature-Guided Policy Optimization (CGPO)** 提出了一种轻量级解决方案：受牛顿法启发，CGPO 在每轮更新中随机排列领域顺序，逐领域进行顺序参数更新。这一简单机制在不显式计算黑塞矩阵的前提下，自然诱导出跨领域的黑塞-梯度乘积交互项，使优化路径倾向于梯度对齐的区域，从而缓解多领域冲突。更新后，CGPO 通过混合系数 α 将新参数与原始参数插值，进一步稳定训练过程。

**核心结论：**
- **性能显著提升**：在 Qwen2.5-3B 和 7B 模型上，CGPO 在多领域基准测试中均取得最佳平均性能（Table 1），超越联合学习、**FAMO**（Liu et al., 2023）等基线方法。
- **冲突敏感性强**：在高冲突领域对（数学+创意写作）中，CGPO 相对增益（+2.38）大于中等冲突对（数学+编码，+1.30），验证了方法对跨领域冲突程度的针对性缓解能力（Tables 6-7）。
- **计算开销极低**：CGPO 仅引入边际额外耗时——7B 模型每步增加约 0.30 分钟，大规模模型（32B/72B）额外开销仅约 5%，远低于联合学习（Table 2, Table 5）。
- **机制验证明确**：消融实验证实随机化领域顺序是关键设计（随机顺序比固定顺序平均分提升 1.11，Table 3），混合系数 α=1.2 达到最优综合性能（Table 4）。

**方法定位：** CGPO 属于多领域强化学习的参数更新策略优化，通过随机顺序更新隐式引入曲率引导，无需二阶优化器或额外网络模块，可与现有 RL 框架（如 GRPO）无缝集成。



### 多领域强化学习的核心瓶颈

将大语言模型（LLM）通过强化学习（RL）在数学、编程、科学、创意写作等多个领域同时进行后训练微调，已成为提升模型综合推理能力的主流范式。然而，这一过程面临一个根本性困境：**不同领域的梯度更新方向往往相互冲突**。当模型参数沿某一领域的梯度方向更新时，可能损害其在另一领域的已有能力，导致单领域增益以牺牲其他领域性能为代价。这种梯度冲突使得简单的联合训练（Joint Learning）——即直接在多领域混合数据上聚合梯度后一次性更新——难以实现真正的跨领域协调优化。

### 现有方法的局限

当前应对多领域冲突的策略可大致分为两类：

- **权重/步长调度方法**：如 **FAMO**（Liu et al., 2023）通过动态调整各领域损失权重来平衡进展速度，本质上是在一阶梯度层面进行加权协调。这类方法虽然改善了领域间的更新步长分配，但未触及参数空间中梯度方向本身的对齐问题。
- **课程学习方法**：如 **Omni-Thinker**（Li et al., 2025a）采用渐进式课程安排，或基于任务难度的自步学习（Self-paced CL），通过控制训练数据的呈现顺序来缓解冲突。但这些方法的调度策略通常是启发式的，缺乏对参数空间几何结构的显式利用。

上述方法的共同局限在于：**它们仅操作于一阶梯度信息，忽视了损失景观的二阶曲率结构**。而曲率信息恰恰刻画了不同领域梯度之间的相互作用——即一个领域的参数更新如何影响另一领域的梯度方向。

### 牛顿法的启示与计算困境

经典优化理论中，牛顿法通过黑塞矩阵的逆对梯度进行预条件处理：

$$\theta_{t+1} = \theta_t - \mathbf{H}(\theta_t)^{-1} \mathbf{g}(\theta_t)$$

这一更新规则能够自动校正梯度方向，使优化路径避开曲率陡峭的方向，从而在多个目标之间实现更协调的参数更新。在多领域场景中，跨领域的黑塞-梯度乘积 $\mathbf{H}_j \mathbf{g}_i$ 恰好量化了领域 $i$ 的更新对领域 $j$ 梯度的二阶影响，是协调跨领域优化的关键信号。

然而，对于参数量动辄数十亿的LLM，显式计算和存储完整的黑塞矩阵在计算上完全不可行。即使采用近似二阶优化器（如SOAP），其状态内存需求对于7B模型即高达每设备120 GB，且需要定期进行昂贵的特征分解，远超当前RL训练管线的硬件承受能力。

### 本文动机

上述分析揭示了一个明确的研究缺口：**如何在极低计算开销下，将曲率引导的预条件机制引入LLM的多领域RL训练**。本文的核心动机正是弥合这一缺口——设计一种轻量级方法，在不显式计算任何二阶量的前提下，隐式地利用跨领域曲率交互来促进梯度对齐，从而在多个推理领域上实现协调且高效的能力增强。



## 核心方法与创新机理

### 瓶颈：多领域梯度冲突

多领域强化学习中，各领域损失表面差异显著，直接聚合梯度进行参数更新会导致**梯度冲突**——一个领域的增益往往以牺牲其他领域性能为代价。这种冲突在领域差异较大时尤为突出，例如数学推理与创意写作之间的优化方向可能相互抵消。现有方法（如联合学习 Joint Learning、动态权重调整 FAMO）试图缓解此问题，但缺乏对参数空间几何结构的显式利用。

### 核心机制：通过随机顺序更新诱导跨领域曲率交互

CGPO 的核心创新在于**将牛顿法的二阶预条件思想转化为极轻量的随机顺序更新机制**，无需显式计算黑塞矩阵。其因果链条如下：

1. **顺序更新产生隐式交互**：在每一轮迭代中，CGPO 随机打乱领域顺序，依次对每个领域计算 GRPO 梯度并更新参数。当领域 $j$ 在领域 $i$ 之后更新时，$j$ 的梯度变化近似包含 $\mathbf{H}_j \mathbf{g}_i$ 项（黑塞矩阵与梯度的乘积），即**领域 $i$ 的曲率信息通过参数变化传递给了领域 $j$**。

2. **随机排列对称化交互**：通过对领域顺序进行随机排列，任意两个领域对 $(i, j)$ 在期望上都能获得对称化的交互项 $\mathbf{H}_i \mathbf{g}_j + \mathbf{H}_j \mathbf{g}_i$，该表达式等价于**梯度内积的梯度** $\frac{\partial}{\partial \theta} (\mathbf{g}_i^\top \mathbf{g}_j)$。这意味着 CGPO 在期望上**最大化领域间梯度内积**，从而引导参数向梯度对齐的区域移动，自然缓解冲突。

3. **参数插值稳定训练**：顺序更新后的参数 $\phi_K$ 与原始参数 $\phi_0$ 按混合系数 $\alpha$ 进行插值：$\theta_{\text{new}} = \phi_0 + \alpha(\phi_K - \phi_0)$。这一操作平衡了曲率利用与训练稳定性，消融实验表明 $\alpha=1.2$ 取得最优综合性能。

### 与基线方法的关键差异

| 设计维度 | 基线方法 | CGPO |
|---------|---------|------|
| **参数更新顺序** | 所有领域梯度聚合后一次更新 | 随机排列领域顺序，逐领域顺序更新 |
| **跨领域交互** | 仅通过共享参数隐式发生 | 通过顺序更新显式引入 $\mathbf{H}_j \mathbf{g}_i$ 交互项 |
| **二阶信息** | 无 | 隐式近似，无额外计算开销 |
| **梯度缩放** | 按批次大小直接聚合 | 按 minibatch 比例缩放并归一化，保持更新幅度可比 |
| **训练稳定性** | 依赖 PPO/GRPO 自身裁剪机制 | 额外引入参数插值（$\alpha$ 混合） |

### 证据强度

- **随机顺序的必要性**：消融实验（Table 3）显示，固定顺序版本 CGPOfix 平均分 58.48，随机顺序版本 CGPO 达到 59.59，提升 1.11 分，置信度 0.95。
- **计算开销极低**：7B 模型上 CGPO 每步仅增加 0.30 分钟（Table 2），大规模模型（32B/72B）额外耗时约 5%（Table 5），远低于联合学习的线性扩展。
- **冲突敏感性验证**：在高冲突领域对（数学+创意写作）中，CGPO 相对 FAMO 提升 2.38 分（Table 7）；在中等冲突对（数学+编码）中提升 1.30 分（Table 6），表明方法对冲突程度具有区分性响应。

### 局限与开放问题

- 随机顺序调度尚有改进空间，更精细的调度策略（如基于冲突程度的自适应排序）可能进一步提升跨领域协调效率。
- 方法效果依赖于各领域奖励信号的覆盖度和质量，创意写作等主观领域使用单一 LLM 裁判可能引入风格偏差。
- CGPO 在预训练阶段相对于数据混合策略的优势仍是开放问题。



![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_R2EZtdHWJT/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of CGPO (one update step). After generating responses, computing rewards, and estimating advantages for each domain, CGPO randomly permutes the domain order and applies updates sequentially, followed by interpolation with the original model. The parameter change ∆θ can be approximately decomposed into a single-domain gradient term—capturing per-domain learning—and a cross-domain interaction term that facilitates transfer across domains. Note that CGPO introduces only negligible additional computation overhead (see Section 4.3 for details)*

CGPO 的整体 pipeline 围绕一个核心操作展开：**在每轮更新中，随机排列领域顺序并执行序列化的参数更新，从而隐式地引入跨领域曲率-梯度交互**。这一设计将牛顿法中黑塞矩阵与梯度耦合的思想，转化为无需显式计算二阶信息的轻量级机制。

### Pipeline 模块与数据流

CGPO 的一步更新包含四个紧密衔接的模块，如 Figure 1 所示：

1. **批次采样与响应生成**  
   从 $K$ 个领域各自采样 prompt，使用当前的旧策略 $\pi_{\theta_{\text{old}}}$ 为每个 prompt 生成 $G$ 组候选响应。这一阶段产生各领域的（prompt, response）对，作为后续奖励评估的输入（Algorithm 1 Lines 6-7）。

2. **奖励计算与优势估计**  
   按领域特定的奖励函数 $R_k(\mathbf{x}, \mathbf{y})$ 计算每组响应的奖励，随后基于 GRPO 框架估计优势函数。GRPO 的核心在于群组归一化：对同一 prompt 的 $G$ 个响应，将奖励减去组内均值并除以组内标准差，得到归一化优势 $\hat{A}^{(i)}$，再结合裁剪机制与 KL 正则项 $\beta D_{\text{KL}}$ 形成替代目标（Equation 1, Section 2.2）。这一步骤为每个领域产出一个可用于策略梯度更新的损失信号。

3. **随机排列与顺序更新**  
   这是 CGPO 区别于所有基线方法的关键模块。在获得各领域的梯度信息后，CGPO **随机打乱 $K$ 个领域的更新顺序**，得到一个随机排列 $\sigma$。随后，从初始参数 $\phi_0$ 出发，依次用每个领域的 GRPO 梯度更新参数：
   - 领域 $\sigma(k)$ 的梯度在参数 $\phi_{k-1}$ 上计算，$\phi_{k-1}$ 已经包含了前 $k-1$ 个领域更新的累积效应。
   - 这一序列化更新使得后续领域的梯度计算天然地“看到”了先前领域的参数变化，从而产生跨领域的黑塞-梯度乘积项 $\mathbf{H}_{\sigma(k)}(\phi_0) \mathbf{g}_{\sigma(l)}(\phi_0)$（Equation 3, Section 3.3）。
   - 为避免有效学习率膨胀，每个领域的梯度按其 minibatch 大小缩放，并除以所有领域总规模进行归一化（Section 3.3 Discussion）。

4. **参数插值**  
   完成一轮序列更新后，得到参数 $\phi_K$。CGPO 将其与原始参数 $\phi_0$ 按混合系数 $\alpha$ 进行线性插值：$\theta_{\text{new}} = \phi_0 + \alpha(\phi_K - \phi_0)$（Algorithm 1 Line 15）。这一步骤起到稳定训练的作用，防止单轮序列更新导致的过度偏移。消融实验表明 $\alpha=1.2$ 在多项指标上取得最优或次优结果（Table 4）。

### 从顺序更新到梯度对齐：因果机制

CGPO 的有效性根植于一个可推导的因果链条：

- **序列更新诱导跨领域交互**：一轮序列更新后，参数总变化可分解为两项——所有领域一阶梯度的聚合项，以及跨领域黑塞-梯度乘积的交互项（Equation 5, Section 3.3）。
- **随机排列使交互对称化**：对随机排列 $\sigma$ 取期望后，跨领域交互项对称化为 $\frac{\partial}{\partial \phi_0}(\mathbf{g}_i^\top \mathbf{g}_j)$，即**梯度内积的梯度**（Appendix B.4）。这意味着优化过程在期望上被推向梯度对齐的方向——领域间的梯度夹角减小，冲突减弱。
- **无显式二阶计算**：整个过程仅需标准的一阶梯度计算和参数更新，额外的计算开销仅来自序列化更新本身。在 7B 模型上，CGPO 每步仅增加约 0.30 分钟（Table 2），在大规模模型（32B/72B）上额外耗时约 5%（Table 5），远低于联合学习之外需要显式冲突处理的方案。

### 输入输出流总结

- **输入**：各领域的 prompt 数据集 $\{\mathcal{D}_k\}_{k=1}^K$，领域特定奖励函数 $\{R_k\}_{k=1}^K$，初始策略参数 $\theta$。
- **输出**：经多领域协调优化后的策略参数，在保持各领域性能的同时促进跨领域协同。
- **关键控制变量**：领域排列的随机种子、混合系数 $\alpha$、学习率 $\eta$。



CGPO 的核心机制是将牛顿法中的曲率-梯度耦合思想压缩为一种无需显式计算黑塞矩阵的轻量级过程。其关键洞察在于：**顺序更新会自然诱导跨领域梯度变化，而这一变化恰好近似了黑塞矩阵与梯度的乘积**。

### 关键模块

CGPO 的单步更新包含四个关键模块（见 Algorithm 1）：

1. **批次采样与响应生成**：从各领域采样 prompt，使用旧策略生成多组响应。
2. **奖励计算与优势估计**：按领域特定奖励函数计算奖励，基于 GRPO 估计优势。
3. **随机排列与顺序更新**：随机打乱领域顺序，每个领域基于当前参数计算 GRPO 梯度并依次更新。
4. **参数插值**：将顺序更新后的参数与原始参数按混合系数 α 混合，稳定训练。

其中，模块 3 是方法的核心创新，模块 4 是防止训练不稳定的关键工程手段。

### 核心公式推导

**动机**：经典牛顿更新为 $\theta_{t+1} = \theta_t - \mathbf{H}(\theta_t)^{-1} \mathbf{g}(\theta_t)$，其乘积 $\mathbf{H}\mathbf{g}$ 包含跨领域项，其中领域 $j$ 的曲率调制领域 $i$ 的梯度，有望协调冲突梯度。但显式计算黑塞矩阵在大规模 LLM 中不可行。

**核心近似**：CGPO 通过顺序更新隐式生成跨领域交互项。当对领域 $i$ 执行一步更新后，领域 $j$ 的梯度变化近似为：

$$\mathbf{g}_j(\theta_{\mathrm{post}}^{(i)}) - \mathbf{g}_j(\theta_{\mathrm{pre}}^{(i)}) \approx \eta \mathbf{H}_j(\theta_{\mathrm{pre}}^{(i)}) \mathbf{g}_i(\theta_{\mathrm{pre}}^{(i)})$$

该式表明，**顺序更新自然产生了所需的黑塞-梯度乘积 $\mathbf{H}_j \mathbf{g}_i$**，无需任何二阶计算。

**序列展开**：在一次随机排列 $\sigma$ 下，领域 $\sigma(k)$ 在第 $k-1$ 步的梯度可展开为：

$$\mathbf{g}_{\sigma(k)}(\phi_{k-1}) = \mathbf{g}_{\sigma(k)}(\phi_0) - \sum_{l=1}^{k-1} \frac{\eta |D_{\sigma(l)}|}{\sum_{s=1}^K |D_{\sigma(s)}|} \mathbf{H}_{\sigma(k)}(\phi_0) \mathbf{g}_{\sigma(l)}(\phi_0) + \mathcal{O}(\eta^2)$$

其中 $\phi_0$ 为初始参数，$|D_{\sigma(l)}|$ 为领域 $\sigma(l)$ 的 minibatch 大小。该展开显式展示了跨领域二阶交互项。

**参数总变化**：一轮序列更新并经过 α 插值后，参数总变化为：

$$\alpha(\phi_K - \phi_0) = -\frac{\alpha\eta}{K} \sum_{k=1}^K \mathbf{g}_k(\phi_0) + \frac{\alpha\eta^2}{K^2} \sum_{k=1}^K \sum_{l=1}^{k-1} \mathbf{H}_{\sigma(k)}(\phi_0) \mathbf{g}_{\sigma(l)}(\phi_0) + \mathcal{O}(\eta^2)$$

第一项为聚合的一阶梯度，第二项为跨领域曲率-梯度交互项。**随机排列的期望使交互项对称化**：

$$\mathbf{H}_i(\phi_0) \mathbf{g}_j(\phi_0) + \mathbf{H}_j(\phi_0) \mathbf{g}_i(\phi_0) = \frac{\partial}{\partial \phi_0} \left( \mathbf{g}_i(\phi_0)^\top \mathbf{g}_j(\phi_0) \right)$$

这意味着 CGPO 在期望上**最大化领域间梯度内积**，即鼓励梯度对齐，从而引导参数走向多领域联合增益的区域。

### 变量含义

| 符号 | 含义 |
|------|------|
| $\theta$ / $\phi$ | 策略参数 |
| $\mathbf{g}_k$ | 领域 $k$ 的梯度 |
| $\mathbf{H}_k$ | 领域 $k$ 的黑塞矩阵 |
| $\eta$ | 学习率 |
| $\sigma$ | 领域的随机排列 |
| $\alpha$ | 参数插值混合系数（推荐 1.2） |
| $K$ | 领域总数 |
| $|D_k|$ | 领域 $k$ 的 minibatch 规模 |

### 设计要点

- **梯度缩放**：每个领域梯度按 minibatch 大小缩放并除以领域总规模，避免学习率膨胀。
- **随机化必要性**：消融实验（Table 3）证实，随机化领域顺序的平均分（59.59）显著优于固定顺序（58.48），验证了随机排列对跨领域曲率信息传播的关键作用。
- **α 的选择**：α=1.2 在多项指标上取得最优或次优结果（Table 4），过小则曲率利用不足，过大则训练不稳定。



## 实验与关键发现

### 核心瓶颈：多领域强化学习中的梯度冲突

在多领域强化学习后训练中，一个被广泛观察但缺乏低成本解决方案的瓶颈是：不同领域的梯度更新方向往往相互冲突，导致参数更新相互抵消。联合学习（Joint Learning）直接将所有领域数据混合训练，但单领域的收益常以其他领域性能下降为代价。这一现象在奖励曲线和最终评测中表现为“零和博弈”：某些领域提升的同时，另一些领域停滞甚至退化。

CGPO 的关键发现是：**随机化的领域更新顺序可以隐式地引入跨领域曲率-梯度交互**，使优化路径趋向梯度对齐的区域，从而协调多领域更新方向。这一机制无需显式计算黑塞矩阵，计算开销极低。

### 主实验结果

**Table 1** 报告了在 Qwen2.5-3B-Instruct 和 Qwen2.5-7B-Instruct 两个模型规模上的多领域评测结果。CGPO 在两个模型上均取得最佳平均性能：

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_R2EZtdHWJT/figures/002_Table_1.jpg]]
*Table 1: Performance of models (Qwen2.5-3B-Instruct and Qwen2.5-7B-Instruct) trained on the multi-domain dataset with different methods, evaluated on multiple benchmarks. The bold font indicates the best result and an underline indicates the second-best result*

- **3B 模型**：CGPO 平均分 50.42，显著优于最强基线。
- **7B 模型**：CGPO 平均分 59.59，在所有方法中排名第一。

四个评测领域包括数学（MATH500, AMC）、代码生成（HumanEval, MBPP）、科学问答（GPQA-diamond, SuperGPQA）和创意写作（WritingBench）。CGPO 的优势并非依赖某一领域的极端提升，而是在多个领域上实现均衡增益，体现了跨领域协调的有效性。

**Figure 2** 的训练奖励曲线进一步验证了 CGPO 的加速效果：在数学、代码、科学问答和创意写作四个领域上，CGPO 的奖励曲线均持续高于联合学习，且提升速度更快。值得注意的是，即使在初始奖励水平相近的领域，CGPO 仍表现出不同程度的加速，这一点作者指出其深层原因有待进一步研究。

### 计算开销分析

CGPO 的理论优势在于避免了显式二阶计算，但实际工程开销如何？**Table 2** 给出了 3B 和 7B 模型上一个 epoch 的耗时对比：

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_R2EZtdHWJT/figures/013_Table_2.jpg]]
*Table 2: Computation cost comparison between joint learning and CGPO (1 epoch). Note that the units of total time and per-step time are different (hours vs. minutes)*

- **3B 模型**：CGPO 总耗时比联合学习多 1.2 小时（约 8.1%），每步仅增加约 0.46 分钟。
- **7B 模型**：CGPO 总耗时多 0.8 小时（约 4.5%），每步增加约 0.30 分钟。

**Table 5** 进一步展示了大规模模型（32B/72B）上的墙钟时间对比。在 32B（16 卡）和 72B（32 卡）配置下，CGPO 的每步耗时增加均控制在约 5% 左右，远低于联合学习可能需要的额外调参或失败重试成本。这一边际开销使得 CGPO 在实际部署中具有较高的性价比。

### 消融实验

#### 领域顺序随机化的必要性

**Table 3** 对比了固定领域顺序（CGPOfix）与随机顺序（CGPOrand）的效果。在 7B 模型上，随机顺序的平均分达到 59.59，固定顺序仅为 58.48，差距为 1.11 分。这一结果直接支持了 CGPO 的核心设计：随机排列是跨领域曲率交互的前提，固定的更新顺序无法充分传播曲率信息。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_R2EZtdHWJT/figures/011_Table_3.jpg]]
*Table 3: Ablation study on domain order randomization in CGPO with Qwen2.5-7B-Instruct. The bold font indicates the better result*

#### 混合系数 α 的影响

**Table 4** 测试了混合系数 α ∈ {0.9, 1.2, 1.5} 的效果。α=1.2 在平均分上取得最优（59.59），α=0.9 为次优。所有 α 值均优于最强基线 FAMO，表明参数插值机制本身具有鲁棒性。α 的作用是在原始参数和顺序更新后的参数之间进行平衡：过小的 α 可能抑制曲率交互的收益，过大的 α 则可能引入不稳定性。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_R2EZtdHWJT/figures/012_Table_4.jpg]]
*Table 4: Ablation study on the effect of the mixing coefficient α in CGPO with Qwen2.5-7B-Instruct. The bold font indicates the best result and an underline indicates the second-best result*

### 多领域扩展与冲突敏感性

CGPO 在不同领域组合下的表现揭示了其对冲突程度的敏感性：

- **数学+代码**（**Table 6**）：这两个领域被认为冲突程度中等。CGPO 平均分 73.56，FAMO 为 72.26，提升 1.30 分。
- **数学+创意写作**（**Table 7**）：这两个领域冲突程度更高。CGPO 平均分 67.02，FAMO 为 64.64，提升 2.38 分，相对增益明显大于数学+代码组合。这一结果表明，CGPO 的曲率引导机制在高冲突场景下发挥了更显著的协调作用。
- **六领域扩展**（**Table 8**）：在数学、代码、科学问答、创意写作、逻辑、表格六个领域的联合训练中，CGPO 平均分 57.81，FAMO 为 56.08，提升 1.73 分。CGPO 在 9 个子基准中的 7 个上取得更优结果。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_R2EZtdHWJT/figures/016_Table_7.jpg]]
*Table 7: Performance of models (Qwen2.5-7B-Instruct) trained on the multi-domain dataset (math + creative writing) with different methods, evaluated on multiple benchmarks. The bold font indicates the best result*

### 失败模式与局限性

尽管 CGPO 在多数场景下表现优异，但仍存在以下局限：

1. **奖励模型的偏差风险**：创意写作领域依赖单一 LLM 裁判进行奖励评估，可能引入风格偏好，影响该领域增益的可靠性。这一风险在 Table 1 和 Table 7 的 WritingBench 指标中需要谨慎解读。
2. **领域覆盖的依赖性**：CGPO 的效果受领域奖励函数的覆盖度和粒度影响。若某一领域的奖励信号稀疏或噪声较大，曲率交互可能无法有效传播有用信息。
3. **顺序策略的改进空间**：当前采用纯随机排列，但更精细的调度策略（如基于冲突程度的自适应排序）可能进一步提升性能。
4. **预训练阶段的适用性未知**：当前验证集中于推理阶段的后训练微调，CGPO 在预训练阶段相对于数据混合策略的优势仍是开放问题。



## 定位与知识库关联

### 问题定位：多领域RL中的梯度冲突瓶颈

多领域强化学习的核心矛盾在于：不同领域（如数学推理、代码生成、创意写作）的奖励信号往往指向不同的参数更新方向，导致梯度冲突。当使用联合学习（Joint Learning）直接在混合数据上训练时，聚合梯度会掩盖这些冲突，使单领域增益以牺牲其他领域性能为代价。CGPO将这一瓶颈形式化为**跨领域梯度对齐问题**——即如何在不显式计算二阶信息的前提下，引导参数更新进入多个领域共同受益的区域。

### 方法谱系：从联合学习到曲率引导的顺序更新

CGPO处于多领域策略优化的演进线上，其核心改造在于**参数更新顺序**和**跨领域交互机制**两个维度。

**基线方法层级：**

- **Joint Learning**：最直接的基线，将多领域数据混合后统一训练，不区分领域来源，无冲突处理机制。其优势在于实现简单，但完全忽略了领域间梯度方向的不一致。
- **Omni-Thinker**（Li et al., 2025a）：采用渐进课程学习策略，通过控制领域引入顺序和难度来缓解冲突。然而，课程设计依赖先验知识，且无法在训练过程中动态感知梯度层面的冲突。
- **Self-paced CL**：基于任务难度的自步课程学习，根据模型当前能力动态调整样本权重。其局限在于仅从“难度”维度调度，未触及参数空间中的几何冲突。
- **FAMO**（Liu et al., 2023）：通过动态调整各领域损失权重来平衡进展速度，属于损失层面的协调方法。FAMO在多个实验中作为最强基线出现，但其权重调整基于标量进展信号，缺乏参数空间中的方向性引导。

**CGPO的关键改造（changed slots）：**

1. **参数更新顺序**：从“所有领域梯度聚合后一次更新”改为“随机排列领域顺序，逐领域顺序更新”。这一改造是CGPO的核心——顺序更新使得前序领域的参数变化能够通过曲率信息影响后续领域的梯度计算，从而隐式地引入跨领域Hessian-梯度乘积项（见公式 $\mathbf{g}_j(\theta_{\text{post}}^{(i)}) - \mathbf{g}_j(\theta_{\text{pre}}^{(i)}) \approx \eta \mathbf{H}_j \mathbf{g}_i$），无需显式计算二阶矩阵。

2. **更新混合系数 $\alpha$**：从无混合（或$\alpha=1$）改为通过$\alpha$混合原始参数与顺序更新后的参数（$\alpha \in [0.9, 1.5]$）。该插值机制在稳定训练的同时，控制曲率交互的强度——$\alpha$越大，跨领域二阶项的影响越显著（见公式 $\alpha(\phi_K - \phi_0)$ 的展开）。

3. **梯度缩放**：从按批次大小直接聚合改为每个领域梯度按minibatch大小缩放并除以领域总规模，确保不同领域对参数更新的贡献幅度可比，避免大规模领域主导更新方向。

### 核心机制：随机排列如何促进梯度对齐

CGPO的理论洞察源于对牛顿法更新 $\theta_{t+1} = \theta_t - \mathbf{H}^{-1}\mathbf{g}$ 的轻量化改造。牛顿项中的跨领域分量 $\mathbf{H}_j \mathbf{g}_i$ 传递了领域$j$的曲率对领域$i$梯度的调制信号，理论上可以协调冲突方向。然而，显式计算Hessian在LLM规模下不可行。

CGPO的替代方案是：**通过随机化领域更新顺序，在期望上对称化跨领域交互项**。一轮顺序更新后的参数总变化可分解为：

$$\alpha(\phi_K - \phi_0) = -\frac{\alpha\eta}{K} \sum_{k=1}^K \mathbf{g}_k(\phi_0) + \frac{\alpha\eta^2}{K^2} \sum_{k=1}^K \sum_{l=1}^{k-1} \mathbf{H}_{\sigma(k)}(\phi_0) \mathbf{g}_{\sigma(l)}(\phi_0) + \mathcal{O}(\eta^2)$$

其中第一项是标准的一阶梯度和，第二项是跨领域交互项。当对随机排列$\sigma$取期望时，交互项对称化为：

$$\mathbf{H}_i(\phi_0) \mathbf{g}_j(\phi_0) + \mathbf{H}_j(\phi_0) \mathbf{g}_i(\phi_0) = \frac{\partial}{\partial \phi_0} \left( \mathbf{g}_i(\phi_0)^\top \mathbf{g}_j(\phi_0) \right)$$

该对称项恰为**领域间梯度内积的梯度**，意味着CGPO在期望上鼓励梯度对齐——即推动参数进入使不同领域梯度方向更一致的区域。这是CGPO区别于所有基线方法的根本机制：它不是在损失或样本层面协调，而是在参数空间的几何层面引导优化路径。

### 证据强度与适用边界

**决定性证据：**

- **主实验（Table 1）**：CGPO在Qwen2.5-3B和7B上均取得最佳平均多领域性能（3B: 50.42, 7B: 59.59），显著优于FAMO等基线。置信度0.98。
- **随机化消融（Table 3）**：随机顺序的CGPO（59.59）显著优于固定顺序版本（58.48），平均提升1.11分，直接验证了随机排列对跨领域交互的必要性。置信度0.95。
- **混合系数消融（Table 4）**：$\alpha=1.2$达到最优综合性能，且所有$\alpha$值（0.9, 1.2, 1.5）均优于最强基线FAMO，说明方法对超参数具有一定鲁棒性。置信度0.95。
- **计算开销（Table 2, Table 5）**：CGPO在3B/7B模型上每步仅增加约0.30-0.46分钟；在32B/72B大规模模型上额外耗时仅约5%，远低于联合学习的潜在替代方案。置信度0.95。
- **冲突敏感性验证（Tables 6-7）**：在高冲突领域对（数学+创意写作）中，CGPO相对FAMO的增益（+2.38）大于中等冲突对（数学+编程，+1.30），验证了方法对梯度冲突程度的响应能力。置信度0.9。

**适用边界与局限：**

1. **奖励信号依赖性**：CGPO的效果受领域奖励覆盖度和质量影响。创意写作评估采用单一LLM裁判，可能引入风格偏好偏差，在奖励模型不完善的领域，曲率引导的方向可能并非真正的质量提升方向。
2. **领域数量扩展性**：当前实验覆盖4-6个领域，随机排列的期望对称化在领域数量进一步增加时是否保持效率仍是开放问题——排列空间增大可能导致交互信号稀释。
3. **调度策略的改进空间**：随机排列是最简单的对称化方案，更精细的调度策略（如基于冲突检测的自适应排序）或结构化协调机制可能进一步提升性能，但尚未探索。
4. **预训练阶段的适用性**：当前验证集中于推理阶段的后训练微调（RLHF范式），CGPO在预训练阶段相对于数据混合与采样策略的优势仍是开放问题。

### 开放问题

- CGPO的曲率先验在领域数量大幅增加（如10+领域）时，随机排列的期望对称化是否仍能有效传递跨领域交互信号？
- 是否可以设计基于实时梯度冲突检测的自适应调度策略，替代纯随机排列以最大化跨领域交互效率？
- 跨领域冲突的具体来源（语义差异、奖励形状、输出格式要求）如何量化并针对性地缓解？当前方法仅在参数空间中间接协调，未对冲突进行显式建模。
- CGPO在纯预训练场景中的表现是否也能超越数据混合与采样策略，以及其与大规模多任务预训练中已有的梯度操作方法（如GradNorm、PCGrad）的关系如何？



## 原文 PDF

![[paperPDFs/ICLR_2026/Boosting_Multi_Domain_Reasoning_of_LLMs_via_Curvature_Guided_Policy_Optimization.pdf]]

---
title: "Constraint Matters: Multi-Modal Representation for Reducing Mixed-Integer Linear programming"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Constraint_Matters_Multi_Modal_Representation_for_Reducing_Mixed_Integer_Linear_programming.pdf
project_link: null
code_link: null
openreview_forum_id: vqNg2Vl8o1
aliases:
- CBMRMMRO
- CMMMRRMILP
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/non_convex
core_operator: "通过信息论引导的Tight Constraints Priority (TCP) 启发式规则，根据固定约束强度ρ优先选择高信息增益的关键紧约束 (CTC)；并利用多模态表示融合抽象模型类别信息与实例级图特征，准确预测这些CTC并将其转化为等式约束，从而大幅缩小可行域，加速MILP求解。"
primary_logic: "约束类型决定其固定后的信息增益：固定约束强度ρ越小（如集合打包、集合划分），局部熵减ΔH = -log ρ 越大，越能有效降低问题不确定性。多模态表示通过跨注意力与门控机制捕捉此类类别信息，提升关键约束的预测准确率，实现约束降维与变量降维的协同。"
claims:
- "信息论启发的TCP模块根据固定约束强度ρ（Definition 2）计算熵减（Proposition 3），优先选择低ρ约束（如 Set Packing, ρ=n/(n+1)）作为关键紧约束（CTC），并通过算法1实现选择。"
- "多模态表示将抽象模型文本嵌入与实例级二部图通过Cross-Attention（Eq.4）和门控机制（Eq.6-7）融合，显著提升CTC预测准确度；在CA数据集上400s时相对原始GNN改善primal gap达12%。"
- "在四个合成基准（CA, MIS, MVC, WA）及真实数据集MMCN上，方法结合SCIP/Gurobi均显著超越基线；gap_abs平均改善51.06%，计算时间（PDI）降低17.47%，且在大规模实例及presolve消融中保持优势。"
- "CA (800s, SCIP) 上 gap_abs = 104.72"
---

# Constraint Matters: Multi-Modal Representation for Reducing Mixed-Integer Linear programming

> [!tip] 核心洞察
> 约束类型决定其固定后的信息增益：固定约束强度ρ越小（如集合打包、集合划分），局部熵减ΔH = -log ρ 越大，越能有效降低问题不确定性。多模态表示通过跨注意力与门控机制捕捉此类类别信息，提升关键约束的预测准确率，实现约束降维与变量降维的协同。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 约束至关重要：面向混合整数线性规划降维的多模态表征 |
| 英文题名 | Constraint Matters: Multi-Modal Representation for Reducing Mixed-Integer Linear programming |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vqNg2Vl8o1) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/non_convex |
| Method | Constraint-based Model Reduction with Multi-Modal Representation (Ours) |
| Dataset | CA (800s, SCIP), MVC (800s, Gurobi+presolve), Large-scale CA (800s, MMCN (real-world, SCIP, 800s) |

> [!tip] 效果简介
> - CA (800s, SCIP) 上，gap_abs 为 104.72，对比 565.61 (Gurobi) / 492.78 (SCIP with (10,0) setting, as proxy)，变化 -81.5% (vs Gurobi) / -78.7% (vs SCIP proxy)。
> - MVC (800s, Gurobi+presolve) 上，PDI 为 4.56，对比 72.31 (Gurobi+presolve)，变化 -93.7%。
> - Large-scale CA (800s, SCIP) 上，gap_abs 为 5955.86，对比 7009.58 (SCIP)，变化 -15.0%。

## 概要

混合整数线性规划（MILP）是现代运筹优化的核心范式，其求解效率直接制约供应链、交通、芯片设计等关键应用的决策时效。现有学习增强方法多聚焦于变量降维，通过预测部分变量取值来缩小搜索空间，却忽略了约束侧的巨大加速潜力。**核心瓶颈在于：直接预测所有紧约束的高维向量极其困难，且不同紧约束对求解加速的影响差异显著——最佳固定可带来数十倍加速，最劣固定则严重恶化性能（Table 1）——缺乏有效识别关键约束并可靠预测的方法，同时存在选择性学习偏差导致模型偏向简单非关键约束。**

本文提出**基于约束的模型降维方法**，核心思想是：通过信息论引导的启发式规则，从众多紧约束中筛选出少数**关键紧约束（Critical Tight Constraints, CTC）**，将其转化为等式约束，从而大幅缩小可行域，加速MILP求解。方法包含三个关键创新：

1. **多模态表示**：将抽象模型类别信息（约束类型、文本语义）与实例级二部图特征通过跨注意力（Cross-Attention）与门控机制融合，提升对约束类型的判别能力。
2. **紧约束优先级（TCP）启发式**：基于信息论，定义固定约束强度 $\rho$（Definition 2），推导局部熵减 $\Delta H = -\log \rho$（Proposition 3），优先选择低 $\rho$ 约束（如集合打包、集合划分）作为CTC，最大化信息增益。
3. **焦点损失训练**：采用Focal Loss缓解简单样本与困难样本的不平衡，抑制选择性学习偏差。

在四个合成基准（CA、MIS、MVC、WA）及真实数据集MMCN上的实验表明，方法结合SCIP/Gurobi均显著超越基线：gap_abs平均改善51.06%，计算时间（PDI）降低17.47%，且在大规模实例及presolve消融中保持优势（Table 3, Table 4, Table 5, Table 12）。消融实验进一步证实，去除多模态表示导致primal gap升高约12%（Figure 4），增加错误固定约束比例则迅速恶化求解性能（Table 11）。

方法的主要局限在于依赖预定义约束类型与人工强度估计，对非原型约束可能失效；TCP为局部贪婪策略，实例级通用性有待提升。未来方向包括开发自动化关键约束识别方法，以及将约束降维与变量降维、割平面生成等更紧密地联合学习。



混合整数线性规划（MILP）是运筹学与组合优化的核心范式，其标准形式为：

$$\operatorname*{min} \mathbf{c}^{\top} \mathbf{x} \quad \mathrm{s.t.} \quad \mathbf{A} \mathbf{x} \leq \mathbf{b} \quad \mathrm{and} \quad \mathbf{x} \in \mathbb{Z}^{q} \times \mathbb{R}^{n-q}$$

实际的 MILP 求解器（如 SCIP、Gurobi）依赖分支定界与割平面等精确算法，但面对大规模实例时，搜索空间呈指数级膨胀，导致求解时间不可接受。近年来，基于学习的变量降维方法（如 Predict-and-Search, PS）通过图神经网络预测部分变量取值并固定，显著压缩了搜索空间。然而，这类方法存在两个结构性盲区：**只缩减变量维度，完全忽略约束维度**；且对“哪些约束真正决定求解难度”缺乏判别能力。

### 约束降维的潜力与挑战

约束降维的核心操作是将部分不等式约束转化为等式（即固定为紧），从而直接削减可行域的维度。动机实验（Table 1）揭示了这一操作的双面性：在 CA_easy 数据集上，选择“最佳”紧约束固定后，求解时间从原始的 378.23s 骤降至 1.85s；而选择“最劣”紧约束固定后，时间反而恶化至 465.74s。在 WA 数据集上，最佳固定将不可解（>3600s）变为 50.73s 可解，最劣固定则保持不可解。这表明**约束选择的质量是决定加速效果的唯一杠杆**，盲目固定会适得其反。

### 根本瓶颈：关键约束的识别与可靠预测

直接预测所有紧约束的高维向量极其困难，原因有三：

1. **约束异质性**：不同紧约束对求解加速的影响差异巨大。某些约束固定后极大缩小可行域（如集合打包类约束），而另一些固定后几乎不改变问题难度。缺乏有效区分“关键”与“非关键”约束的机制。
2. **选择性学习偏差**：模型在训练中倾向于拟合易于预测的非关键约束，而忽略真正重要但预测困难的约束，导致在实际部署时选择的是“容易正确”而非“真正有用”的约束。
3. **表征不足**：现有方法仅依赖实例级二部图 GNN 编码，无法捕捉约束的**抽象类别信息**（如约束是 Set Packing 还是 Set Covering 类型），而这些类别信息恰恰决定了约束固定后的信息增益大小。

这些瓶颈共同指向一个核心缺口：**需要一种既能识别关键约束、又能可靠预测其紧性的方法，同时克服选择性学习偏差**。本文正是从这一缺口出发，提出基于多模态表征的约束降维框架，将变量降维与约束降维协同，实现更高效的 MILP 求解加速。



## 核心方法与创新机理

本工作相对于现有 MILP 加速方法，在三个关键维度上做出了根本性改变，形成“约束降维 + 多模态表征 + 信息论选择”的协同创新体系。

### 从变量降维到变量-约束联合降维

现有基于学习的 MILP 加速方法（如 Predict-and-Search）仅对变量进行固定，将部分变量预测值锁定后求解约化问题。本方法首次将约束也纳入降维对象：将选定的不等式约束转化为等式约束，从而大幅缩小可行域。这一转变的动机来自直接实验证据——Table 1 显示，固定不同的紧约束对求解时间的影响差异巨大（CA_easy 上最佳固定仅需 1.85 秒，最劣固定则需 465.74 秒），表明约束选择的质量直接决定加速效果的上限。方法通过同时减少变量和约束，使可行域在两个方向上收缩，产生乘数效应。

### 从实例图到多模态图表征

基线方法（PS、ConPaS）仅使用实例级二部图 GNN 编码单个 MILP 实例的结构信息。本方法提出多模态表征框架，额外引入**抽象模型图**：将 MILP 问题类（如组合拍卖、顶点覆盖）的约束类型作为类别节点，用预训练语言模型（如 T5-base）嵌入约束的文本语义作为初始特征。两个图之间通过跨层消息传递进行融合：

- **Cross-Attention 发送/接收**（Eq. 4）：将实例节点特征聚合到对应类别节点，实现实例→抽象的跨模态信息流动；
- **门控机制**（Eq. 6-7）：学习门控系数 $\alpha \in [0,1]$，自适应地融合来自抽象模型和实例模型的类别特征，再通过 Hadamard 积注入实例节点。

这一设计的核心洞察在于：约束的“类型”决定了其被固定后的信息增益。例如，Set Packing 约束（$\sum x_i \leq 1$）固定为等式后，可行解数量从 $n+1$ 骤降至 1，而一般线性约束的缩减效果则弱得多。多模态表征使模型能够捕捉此类类别级别的语义信息，从而更准确地预测哪些紧约束值得固定。

### 从无差别固定到信息论驱动的关键约束选择

ConPaS 对所有预测为紧的约束进行固定，但 Table 1 表明并非所有紧约束都有益。本方法提出 **Tight Constraints Priority (TCP)** 启发式规则，基于信息论原理对约束进行优先级排序：

- **固定约束强度** $\rho(C_i) = |S_{\hat{C}_i}| / |S_{C_i}|$（Definition 2）：衡量固定约束后可行空间与原空间的比值，$\rho$ 越小约束越“强”；
- **熵减加速** $\Delta H_{C_i} = -\log \rho$（Proposition 3）：固定该约束带来的局部信息增益，$\rho$ 越小信息增益越大。

TCP 据此优先选择低 $\rho$ 的约束类型（如 Set Packing 的 $\rho = n/(n+1)$、Set Covering 的 $\rho = n/(2^n-1)$）作为**关键紧约束（CTC）**，并通过 Algorithm 1 按比例平衡选择，避免偏向某一类型。这一选择准则将“固定哪个约束”从经验试错提升为有理论依据的决策。

### 从交叉熵到焦点损失

训练中直接使用交叉熵损失会导致模型偏向预测大量简单样本（非紧约束），而对少数关键紧约束的预测精度不足——即选择性学习偏差。本方法采用 **Focal Loss**（Eq. 13），通过焦点参数 $\gamma$ 降低简单样本的权重，迫使模型聚焦于困难样本（紧约束）。最终损失函数（Eq. 14）将解预测和约束识别的焦点损失加权组合，实现联合优化。

### 创新协同效应

上述四个改变并非孤立改进，而是形成因果链条：多模态表征提供约束类别的语义先验 → TCP 利用该先验计算信息增益并选择 CTC → 焦点损失确保模型能可靠预测这些 CTC → 联合变量-约束降维最大化可行域收缩。消融实验（Figure 4）证实了这一协同关系：去除多模态表征后，CA 数据集 400 秒时 primal gap 相对完整方法升高约 12%；而完全去除约束降维则使性能进一步恶化。



![[assets/figures/papers/iclr26_0009_vqNg2Vl8o1_Constraint_Matters_Multi-Modal_Representation_fo/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our framework, which comprises three components: 1) Multi-modal representation, 2) Identification of Critical Tight Constraints, and 3) Model reduction. In 1), the textual semantics are first embedded as initial features for the abstract model, after which both the instance and abstract model are transformed into bipartite graph. In 2), a subset of tight-constraints is selected and labeled as critical constraints. In 3), multi-modal representation and critical constraints are fed into the learning architecture in Section 4.1 to predict the reduced variables and constraints*

本方法的核心思路是**将约束降维与变量降维协同执行**，通过多模态表示准确识别关键紧约束（Critical Tight Constraints, CTCs），并将其转化为等式约束，从而大幅缩小MILP的可行域，加速求解。整体框架由三个紧密耦合的组件构成，如图2所示。

### 输入与预处理

给定一个MILP实例 $\operatorname*{min} \mathbf{c}^{\top}\mathbf{x}\; \mathrm{s.t.}\; \mathbf{A}\mathbf{x} \leq \mathbf{b}$，框架同时构建两个互补的图表示：

- **实例模型图（Instance Graph）**：标准二部图，变量节点与约束节点通过系数矩阵 $\mathbf{A}$ 中的非零元素连接，节点特征沿用Gasse et al. (2019)的嵌入方式。
- **抽象模型图（Abstract Model Graph）**：基于问题类别的先验知识构建，将约束按类型（如Set Packing、Set Covering、Knapsack等，共10种原型，见表2）聚合为类别节点，并通过预训练语言模型（如T5-base）将约束的数学表达式嵌入为文本语义特征，作为类别节点的初始表示。

### 组件一：多模态表示（Multi-Modal Representation）

该组件通过**层内消息传递**与**层间消息传递**实现实例级与抽象级信息的深度融合：

1. **层内消息传递**：在实例模型图和抽象模型图内部分别执行GNN更新，各自捕获局部结构信息。
2. **层间消息传递**：通过Cross-Attention机制实现跨模态融合。具体而言，实例变量节点的特征被聚合后作为Query，抽象类别节点的特征作为Key和Value，经由Cross-Attention生成“实例感知”的类别特征 $\tilde{h}_{V_j}^{(k)}$（公式4）；反之亦然，形成双向信息交换。
3. **门控融合**：引入门控机制（公式6-7），计算系数 $\alpha \in [0,1]$ 来平衡来自实例模型和抽象模型的类别特征，并通过Hadamard积将融合后的类别特征注入实例变量节点，使每个变量节点同时携带其所属约束类型的类别信息。

这一设计的因果作用在于：约束的类型（如Set Packing的 $\rho = n/(n+1)$）决定了其固定后的信息增益，而多模态表示通过跨注意力与门控机制有效捕捉此类类别信息，为后续准确预测关键紧约束提供了更强的表征基础。

### 组件二：关键紧约束识别（CTC Identification）

该组件解决“固定哪些紧约束”这一核心决策问题：

1. **紧约束判定**：基于当前LP松弛解，识别所有在松弛解中等号成立的约束作为候选紧约束。
2. **TCP启发式排序**：对每个候选紧约束 $C_i$，计算其**固定约束强度** $\rho(C_i) = |S_{\hat{C}_i}| / |S_{C_i}|$（定义2），即固定该约束为等式后的可行空间与原可行空间的比值。$\rho$ 越小，约束越“紧”，固定后带来的**局部熵减** $\Delta H_{C_i} = -\log \rho$（命题3）越大，信息增益越高。
3. **优先级选择**：TCP模块（算法1）根据 $\rho$ 升序排列候选紧约束，优先选择低 $\rho$ 类型（如Set Packing、Set Covering）的约束作为CTC，并控制各约束类型的固定比例以保持多样性。

### 组件三：模型降维执行（Model Reduction）

1. **变量固定**：利用GNN预测的二值解，将高置信度变量固定为其预测值，保留低置信度变量在邻域 $\Delta$ 内自由优化。
2. **约束固定**：将选出的 $k_c$ 个CTC转化为等式约束，直接缩减可行域的维度。
3. **降维MILP求解**：将固定后的变量和等式约束代入原MILP，得到一个规模显著缩小的子问题，交由SCIP或Gurobi在剩余时间预算内求解。若固定错误导致不可行，则回退至原始问题。

### 训练策略

为缓解选择性学习偏差（模型偏向简单非关键约束），采用**Focal Loss**（公式13）替代标准交叉熵损失，通过焦点参数 $\gamma$ 降低简单样本的权重，迫使模型关注困难样本。最终损失函数为解预测损失与约束识别损失的加权和：$\mathscr{L}(\theta) = \lambda \mathscr{L}_{\mathrm{Focal}}^{\mathrm{sol}} + (1-\lambda) \mathscr{L}_{\mathrm{Focal}}^{\mathrm{con}}$（公式14）。

### 关键因果链路总结

**约束类型 → 固定约束强度 $\rho$ → 熵减 $\Delta H$ → TCP优先级排序 → 多模态表示提升CTC预测准确率 → 约束降维缩小可行域 → 求解加速。** 实验表明，错误固定约束的比例一旦达到10-20%，求解性能即显著恶化甚至不可行（表11），这从反面验证了准确识别CTC是整个框架有效性的瓶颈所在。



### 多模态表示（Multi-Modal Representation）

方法的第一个核心组件是多模态表示模块，其目标是将抽象模型层面的类别信息与实例级图结构信息进行融合，为后续的关键紧约束预测提供更具表达力的特征基础。该模块由**抽象模型图**和**实例模型图**两个并行子网络构成，并通过层内消息传递和层间消息传递实现信息交换。

**抽象模型图**以约束类别作为节点，通过文本嵌入（如预训练语言模型编码的约束语义描述）初始化节点特征，并利用类别级GNN进行层内更新。设 $V_j$ 为类别节点，其第 $k$ 层的更新公式为：

$$
\hat{h}_{V_j}^{(k)} \equiv \hat{f}_2^{(k)}\Big(\hat{h}_{V_j}^{(k-1)}, \hat{f}_1^{(k)}\big(\{\hat{h}_U^{(k-1)} : U \in N(V_j)\}\big)\Big)
$$

**实例模型图**则采用标准的二部图GNN（Gasse et al., 2019），对变量节点和约束节点进行层内消息传递。设 $v_i$ 为实例节点，其更新公式为：

$$
h_{v_i}^{(k)} \equiv f_2^{(k)}\Big(\{h_{v_i}^{(k-1)}, f_1^{(k)}\big(\{h_u^{(k-1)} : u \in N(v_i)\}\big)\}\Big)
$$

**层间消息传递**是实现跨模态融合的关键。模块通过Cross-Attention机制将实例节点特征发送至对应的抽象类别节点，使类别表示能够感知实例层面的信息：

$$
\tilde{h}_{V_j}^{(k)} = \mathrm{CrossAttention}\left(\hat{h}_{V_j}^{(k)}, \mathbf{MLP}(\{h_{v_i}^{(k)}\}), \mathbf{MLP}(\{h_{v_i}^{(k)}\})\right), \quad v_i \in V_j
$$

随后，通过**门控机制**动态平衡来自抽象模型和实例模型的类别特征。门控系数 $\alpha$ 由拼接后的特征经可学习Gate函数计算得到：

$$
\alpha = \mathrm{Gate}\left(\bar{h}_{V_j}^{(k)} \parallel \hat{h}_{V_j}^{(k)}\right), \quad \alpha \in [0,1]
$$

最终，实例节点特征通过门控融合后的类别特征进行更新：

$$
h_{v_i}^{(k)} = \left(\alpha \bar{h}_{V_j}^{(k)} + (1-\alpha) \hat{h}_{V_j}^{(k)}\right) \odot h_{v_i}^{(k)}, \quad v_i \in V_j
$$

其中 $\odot$ 表示Hadamard积。这一设计使每个实例节点能够自适应地吸收其所属约束类别的全局信息，从而提升对关键紧约束的判别能力。

### 关键紧约束识别（Critical Tight Constraints Identification）

第二个核心组件是**Tight Constraints Priority (TCP)** 启发式规则，用于从所有紧约束中筛选出对求解加速贡献最大的关键紧约束（Critical Tight Constraints, CTCs）。该规则的信息论基础体现在以下定义和命题中。

**定义 2（固定约束强度）**：对于任意原型约束 $C_i$，定义其固定约束强度 $\rho(C_i)$ 为固定该约束后的局部可行空间大小与原可行空间大小的比值：

$$
\rho(C_i) := \frac{|S_{\hat{C}_i}|}{|S_{C_i}|}, \quad \rho \in [0,1]
$$

其中 $S_{C_i} := \{\mathbf{x} \in \mathcal{D}_i \mid C_i(\mathbf{x}) \text{ 被满足}\}$ 表示满足该原型约束的变量赋值集合。$\rho$ 越小，意味着固定该约束后可行空间收缩越剧烈，约束的“强度”越高。

**命题 3（熵驱动加速）**：固定一个约束所带来的局部熵减（信息增益）由固定约束强度 $\rho$ 直接导出：

$$
\Delta H_{C_i} = -\log \rho
$$

该命题揭示了一个核心洞察：**约束类型决定了其固定后的信息增益**。例如，Set Packing 约束（$\rho = \frac{n}{n+1}$）的熵减远小于 Set Covering 约束（$\rho = \frac{n}{2^n - 1}$），因此后者在固定后能更大幅度地降低问题的不确定性。TCP启发式据此优先选择 $\rho$ 最小的前 $k_c$ 个紧约束作为CTC，并通过算法1（详见附录D）实现选择。

### 约束降维执行与训练损失

**模型降维执行**：将多模态表示预测的变量赋值与TCP筛选的CTC转化为等式约束，构建缩减后的MILP子问题。为保障可行性，引入信任域 $\Delta_c$ 限制搜索范围（详见附录C.5）。

**Focal Loss训练**：为缓解选择性学习偏差——即模型偏向预测简单的非关键约束而忽视困难的关键约束——采用Focal Loss替代传统交叉熵损失：

$$
\mathcal{L}_{\mathrm{Focal}} = -\alpha (1 - \hat{y}_i)^\gamma y_i \log \hat{y}_i + (1 - \alpha) \hat{y}_i^\gamma (1 - y_i) \log (1 - \hat{y}_i)
$$

其中 $\alpha$ 为类别平衡系数，$\gamma$ 为聚焦参数，通过降低易分类样本的损失权重使训练集中于困难样本。最终损失函数将解预测损失与约束识别损失进行加权融合：

$$
\mathscr{L}(\theta) = \lambda \mathscr{L}_{\mathrm{Focal}}^{\mathrm{sol}} + (1 - \lambda) \mathscr{L}_{\mathrm{Focal}}^{\mathrm{con}}
$$

### 模块间因果链路

上述三个模块形成一条清晰的因果链路：多模态表示通过跨注意力与门控机制捕捉约束的类别信息（如Set Packing、Set Covering等原型约束的语义），使模型能够准确预测哪些紧约束属于低 $\rho$ 的高信息增益类型；TCP启发式则基于预测结果和 $\rho$ 的先验估计，优先选择熵减最大的约束进行固定；Focal Loss确保训练过程中模型不会因简单约束的压倒性数量而忽视关键约束的预测。三者协同实现了约束降维与变量降维的联合优化，从而大幅缩小MILP的可行域并加速求解。

> **注意**：固定约束强度 $\rho$ 的推导依赖于对10种原型约束类型（Table 2）的人工定义和组合计数，具体推导过程见附录B.2。对于未预定义的约束类型，该方法需要手动扩展原型库，其实例级通用性存在局限。



## 实验与关键发现

### 核心瓶颈与动机验证

直接预测所有紧约束并固定为等式面临两个根本困难：一是高维预测空间使准确率难以保证，二是不同紧约束对求解加速的影响差异悬殊。Table 1 的动机实验清晰揭示了这一现象：在 CA_easy 数据集上，原始求解时间为 378.23 秒，最佳约束固定可将时间骤降至 1.85 秒，而最劣固定反而恶化至 465.74 秒；在 WA 数据集上，原始实例在 3600 秒内无法求解，最佳固定仅需 50.73 秒，最劣固定同样无法求解。这意味着**约束选择的质量直接决定降维是加速还是破坏**，简单固定所有紧约束的策略不可行。


![[assets/figures/papers/iclr26_0009_vqNg2Vl8o1_Constraint_Matters_Multi-Modal_Representation_fo/figures/003_Table_1.jpg]]
*Table 1: We conducted motivation experiments via fixing different tight constraints on two datasets. Please refer Appendix H.1 to see details of this experiment*

这一瓶颈的因果机制在于：紧约束的"固定约束强度" $\rho(C_i)$（Definition 2，Eq. (9)）——即固定后可行空间与原可行空间的比值——在不同约束类型间存在数量级差异。例如，Set Packing 约束的 $\rho = n/(n+1)$ 较大，而 Set Covering 约束的 $\rho = n/(2^n-1)$ 极小。根据信息论视角（Proposition 3），固定一个约束带来的局部熵减为 $\Delta H_{C_i} = -\log \rho$，$\rho$ 越小则信息增益越大，越能有效缩小搜索空间。因此，**优先选择低 $\rho$ 的关键紧约束（CTC）是降维的核心因果杠杆**。

### 主要结果：整体性能

Table 3 汇总了在四个合成基准（CA, MIS, MVC, WA）上 800 秒时限内的主实验结果。以 SCIP 为后端求解器，所提方法（Ours）在 gap_abs 指标上平均改善 51.06%，在 PDI（Primal-Dual Integral，衡量收敛速度）上平均降低 17.47%。具体而言：


![[assets/figures/papers/iclr26_0009_vqNg2Vl8o1_Constraint_Matters_Multi-Modal_Representation_fo/figures/005_Table_3.jpg]]
*Table 3: Comparison of Different Methods on Four Datasets (800s time limit). The last column shows our method’s improvement over the traditional solver (↓ means lower is better). The best are in bold*

- **CA 数据集**：Ours 的 gap_abs 为 104.72（配合 presolve，Table 12），而 Gurobi 基线为 565.61，改善幅度达 81.5%；SCIP 基线为 492.78，改善 78.7%。
- **MVC 数据集**：Ours 的 PDI 仅为 4.56（配合 presolve，Table 12），而 Gurobi+presolve 基线为 72.31，降低 93.7%。
- **MIS 和 WA 数据集**：Ours 在 gap_abs 和 PDI 两个指标上均一致优于 SCIP、PS（Predict-and-Search，变量降维基线）和 ConPaS（约束预测基线）。


![[assets/figures/papers/iclr26_0009_vqNg2Vl8o1_Constraint_Matters_Multi-Modal_Representation_fo/figures/021_Table_12.jpg]]
*Table 12: Presolve ablation on MVC and CA. Lower $\mathrm { \Delta g a p _ { a b s } }$ and PDI indicate better performance

Figure 3 展示了 SCIP 求解过程中相对 primal gap 随运行时间的变化曲线。Ours 的曲线下降速度明显快于 ConPaS 和 PS，说明**约束降维与变量降维的协同作用不仅改善了最终解质量，还显著加速了收敛过程**。


![[assets/figures/papers/iclr26_0009_vqNg2Vl8o1_Constraint_Matters_Multi-Modal_Representation_fo/figures/006_Figure_3.jpg]]
*Figure 3: The relative primal gap (the lower the better) as a function of runtime, averaged over 100 test instances, within 800s time limits*

### 大规模与真实数据泛化

Table 4 报告了在大规模 CA 和 MVC 实例上的泛化结果。在 CA 上，Ours 的 gap_abs 为 5955.86，相比 SCIP 的 7009.58 降低 15.0%；在 MVC 上，Ours 的 gap_abs 为 0.55，PDI 为 24.54，均为最优。这表明方法能够扩展至更大规模问题，多模态表示捕捉的约束类别信息在规模增大时仍保持有效。

Table 5 展示了在真实世界数据集 MMCN 上的表现。Ours 的 gap_abs 为 3547.08，PDI 为 246.89，显著优于 PS（gap_abs 420.47）和 ConPaS。值得注意的是，PS 在 MMCN 上已优于 SCIP 原始求解，而 Ours 在此基础上进一步改善 41.2%，验证了**约束降维在实际应用场景中的增量价值**。

### 消融实验

**多模态表示的贡献**（Figure 4）：去除多模态表示（仅保留实例 GNN）后，在 CA 数据集 400 秒时 primal gap 相对完整方法升高约 12%。这证实了抽象模型文本嵌入与实例级图特征通过 Cross-Attention（Eq. (4)）和门控机制（Eq. (6)-(7)）融合的有效性——类别信息帮助模型更准确地识别关键约束。


![[assets/figures/papers/iclr26_0009_vqNg2Vl8o1_Constraint_Matters_Multi-Modal_Representation_fo/figures/009_Figure_4.jpg]]
*Figure 4: Ablation study results: the relative primal gap as a function of runtime*

**约束降维 vs 变量降维**（Figure 4）：同时去除约束降维（仅保留变量降维，等价于 PS）后，primal gap 进一步上升，说明约束降维与变量降维是互补的，单独使用任一组件的效果均不及联合使用。

**Presolve 互补性**（Table 12）：将学习到的模型降维与求解器内部的 presolve 结合可获得最佳性能。在 MVC 上，Ours+presolve 的 gap_abs 降至 0，PDI 降至 4.56；在 CA 上，gap_abs 降至 104.72。这表明**学习降维与求解器 presolve 是互补关系而非冲突**——presolve 处理简单的代数简化，而学习降维处理需要语义理解的复杂约束选择。

### 失败模式与敏感性分析

**错误固定约束的退化**（Table 11）：当错误固定约束的比例增加时，求解性能迅速恶化。在 CA 实例上，错误固定比例达到 10-20% 时，部分实例变为不可行（N/A），目标值亦显著恶化。这揭示了方法的一个关键脆弱性：**预测准确率是降维有效性的硬约束**，当模型置信度低时，过度固定可能导致问题不可行或解质量严重下降。

**约束固定数量的权衡**（Table 10）：增大固定约束数 $k_c$ 会降低解的质量（gap_abs 上升）但提升收敛速度（PDI 略有改善），存在帕累托前沿权衡。这意味着在实际部署中需要根据求解目标（优先解质量还是求解速度）来调节 $k_c$。

### 关键图表结论

- **Table 1**：约束选择质量决定降维效果，最佳固定可加速两个数量级，最劣固定导致恶化。
- **Table 2**：10 种原型约束的固定约束强度 $\rho$ 是 TCP 优先级排序的理论基础。
- **Table 3**：Ours 在四个基准上一致超越 SCIP、PS 和 ConPaS，gap_abs 平均改善 51.06%。
- **Figure 3**：Ours 的 primal gap 收敛曲线下降最快，验证了约束降维的加速效果。
- **Figure 4**：多模态表示和约束降维各自贡献显著，去除任一组件均导致性能退化。
- **Table 11**：错误固定约束比例超过 10% 即可能导致不可行，预测准确率至关重要。
- **Table 12**：学习降维与 presolve 互补，结合使用达到最佳性能。



## 定位与知识库关联

### 1. 与基线方法的关系

本方法在**降维类型**、**表示学习**和**约束选择准则**三个维度上对现有工作进行了系统性扩展。

**相对于变量降维方法（Predict-and-Search, PS）**：PS 仅通过 GNN 预测解值并固定部分变量，再在信任域内进行局部搜索。该方法未触及约束空间，导致可行域的缩减有限。本方法在此基础上引入约束降维，将选定的关键紧约束（CTC）转化为等式，从变量和约束两个维度协同压缩搜索空间。实验表明，在 CA 数据集上，本方法相对 PS 的 gap_abs 改善显著（Table 3），且在 MMCN 真实数据集上 gap_abs 从 PS 的 420.47 降至 3547.08（Table 5）——需注意此处 PS 的 gap_abs 异常低，可能源于该数据集上 PS 的特殊行为，建议读者核实原文背景。

**相对于约束预测方法（ConPaS）**：ConPaS 虽涉及约束预测，但缺乏对关键约束的甄别机制，且未利用约束的类型信息。本方法通过信息论引导的 TCP 启发式规则（Algorithm 1），依据固定约束强度 $\rho$ 计算熵减 $\Delta H = -\log \rho$（Proposition 3），优先选择低 $\rho$ 约束（如 Set Packing 的 $\rho = n/(n+1)$）作为 CTC，从而将约束选择从“预测所有紧约束”降维为“识别高信息增益的关键子集”。Table 3 中本方法在四个合成基准上均显著优于 ConPaS。

**表示学习层面的升维**：PS 和 ConPaS 均依赖实例级二部图 GNN（Gasse et al., 2019），仅编码实例特征。本方法构建多模态图，将抽象模型的文本嵌入与实例图通过 Cross-Attention（Eq. 4）和门控机制（Eq. 6-7）融合，使模型能够捕捉约束的类别信息（如 Set Packing、Set Covering 等原型约束的语义）。消融实验（Figure 4）证实，去除多模态表示后，在 CA 数据集 400 秒时 primal gap 相对完整方法升高约 12%，验证了类别信息对 CTC 预测的关键作用。

### 2. 适用边界与前提条件

**对约束类型的先验依赖**：TCP 启发式需要预定义原型约束类型并手动计算其固定约束强度 $\rho$（Table 2 列出 10 种类型，推导见 Appendix B.2）。对于未包含在预定义集合中的约束类型，$\rho$ 的估计可能不准确，导致优先级排序失效。这一依赖限制了方法在完全陌生的问题类上的即插即用能力。

**预测精度的敏感性**：Table 11 显示，当错误固定约束的比例达到 10-20% 时，部分实例变为不可行（N/A），目标值亦显著恶化。这意味着方法对多模态模型的 CTC 预测准确率有较高要求，在预测置信度低的场景下需谨慎设置固定数量 $k_c$。

**与求解器 presolve 的互补性**：Table 12 的消融表明，学习方法与求解器内置 presolve 结合使用可获得最佳性能，二者并非替代关系。presolve 负责消除冗余约束和变量，而本方法侧重于语义层面的关键约束识别，两者作用于不同层次。

### 3. 局限性与失效模式

1. **TCP 的局部贪婪性**：虽然 TCP 基于信息论推导，但其本质是逐约束的局部熵减最大化策略。在约束间存在强相互作用的实例上，局部最优的 CTC 集合未必对应全局最优的搜索空间缩减。Table 1 的动机实验已揭示，不同紧约束固定组合的求解时间差异可达两个数量级（CA_easy：1.85s vs 465.74s），暗示全局最优选择的重要性。

2. **计算开销**：多模态表示引入 Cross-Attention 和双层消息传递，训练时间约为普通 GNN 的 2-3 倍（Appendix E 给出复杂度 $O(n \cdot d^2 + |E| \cdot d^2)$）。对于超大规模实例，这一开销可能成为瓶颈。

3. **文本嵌入的质量依赖**：多模态表示的性能部分依赖于抽象模型文本描述的语义质量。Table 14 显示方法对预训练语言模型的选择（T5-base vs OpenAI Embed）不敏感，但若问题本身的文本描述语义模糊或缺失，类别信息的增益可能有限。

4. **约束固定数量 $k_c$ 的帕累托权衡**：Table 10 表明，增大 $k_c$ 会降低解质量（gap_abs 上升）但提升收敛速度（PDI 略有改善），需要在求解精度与速度间进行任务特定的调参。

### 4. 开放问题

- **自动化约束类型发现**：能否摆脱对预定义原型约束和人工 $\rho$ 估计的依赖，直接从实例数据中学习约束的“信息增益潜力”？这可能涉及约束嵌入空间的聚类或无监督关键性评分。

- **端到端联合学习**：当前方法将表示学习、CTC 识别和模型降维作为串行模块。能否将约束降维与变量降维、割平面生成、分支策略等组件纳入统一的端到端学习框架，实现全局协同优化？

- **跨问题泛化**：多模态表示中的“抽象模型”概念能否推广至其他组合优化问题（如 SAT、CP、MINLP），构建统一的抽象-实例双层建模范式？

- **理论保证**：能否从理论上刻画 TCP 选择的近似最优性边界，以及固定约束对 branch-and-bound 搜索树大小的解析影响？当前的信息论分析仅涉及局部熵减，缺乏对全局求解过程的严格刻画。

- **在线自适应**：在求解过程中，能否根据搜索树的状态动态调整 CTC 选择，而非仅在预处理阶段一次性固定？这需要模型具备对求解器内部状态的感知能力。



## 原文 PDF

![[paperPDFs/ICLR_2026/Constraint_Matters_Multi_Modal_Representation_for_Reducing_Mixed_Integer_Linear_programming.pdf]]

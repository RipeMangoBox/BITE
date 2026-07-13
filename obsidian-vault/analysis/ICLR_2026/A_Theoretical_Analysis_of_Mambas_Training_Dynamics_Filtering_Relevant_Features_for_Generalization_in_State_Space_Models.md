---
title: "A Theoretical Analysis of Mamba’s Training Dynamics: Filtering Relevant Features for Generalization in State Space Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Theoretical_Analysis_of_Mambas_Training_Dynamics_Filtering_Relevant_Features_for_Generalization_in_State_Space_Models.pdf
project_link: null
code_link: null
aliases:
- SMBIDGTLM
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "门控向量w_Δ（通过sigmoid函数控制输入更新和状态保持的强度）"
primary_logic: "门控参数在训练中被优化以放大与类别相关特征的对齐，同时抑制无关特征，从而在结构化数据中实现类似注意力的特征选择效应，但通过选择性状态空间实现"
claims:
- "在多数投票数据上，门控向量w_Δ与类别相关特征的内积下界为 ηT/(8L^2) * Θ((α_r L - α_c L)^2)，而与无关特征的内积上界为 O(1/poly(d))。"
- "在局部结构数据上，门控向量w_Δ与无关特征的内积被驱动为负，从而有效过滤无关特征。"
- "在多数投票数据上，当样本数 N ≥ Ω(L^2 d / (η^2 (α_r - α_c)^2)) 且迭代步数 T = Θ(L^2 / (η (α_r - α_c)^2)) 时，模型可以实现零泛化误差。"
- "在局部结构数据上，样本复杂度和迭代次数由正负样本中类别相关token距离的差值主导，即 [(1/2)^{ΔL_{o_+}^+} - (1/2)^{ΔL_{o_+}^-}] 的倒数。"
---

# A Theoretical Analysis of Mamba’s Training Dynamics: Filtering Relevant Features for Generalization in State Space Models

> [!tip] 核心洞察
> 门控参数在训练中被优化以放大与类别相关特征的对齐，同时抑制无关特征，从而在结构化数据中实现类似注意力的特征选择效应，但通过选择性状态空间实现

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Mamba训练动力学的理论分析：状态空间模型中相关特征过滤以实现泛化 |
| 英文题名 | A Theoretical Analysis of Mamba’s Training Dynamics: Filtering Relevant Features for Generalization in State Space Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hvpKqEYJjj) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | Simplified Mamba block with input-dependent gating and two-layer MLP |
| Dataset | Synthetic majority-voting data, Synthetic locality-structured data |

> [!tip] 效果简介
> - Synthetic majority-voting data 上，Convergence speed (epochs) 为 Larger gap (α_r - α_c)，对比 Smaller gap (α_r - α_c)，变化 Reduced epochs。
> - Synthetic locality-structured data 上，Convergence (epochs) 为 Smaller ΔL (local concentration)，对比 Larger ΔL (dispersed tokens)，变化 Faster convergence。
> - Synthetic locality-structured data 上，Classification accuracy 为 Mamba，对比 Transformer (global attention)，变化 Superior performance。

## 概要

本文从训练动力学的角度对状态空间模型 Mamba 的泛化能力进行了理论分析，核心问题是：**输入依赖的门控机制如何在梯度下降下自动选择与类别相关的特征并忽略无关特征，从而保障高效泛化**。研究工作围绕一个简化的单层 Mamba 块与两层 MLP 的组合展开，其中离散化步长 $\Delta_t = \log(1+e^{\boldsymbol{w}_\Delta^\top \boldsymbol{x}_t})$ 由门控向量 $\boldsymbol{w}_\Delta$ 实现数据依赖，同时 $B, C$ 参数也被改为输入依赖，这是 Mamba 区别于传统 S4 的关键设计。分析方法定位为在两类合成数据模型（多数投票数据与局部结构数据）上，对全批量梯度下降训练过程推导非渐近的样本复杂度和收敛速度界。

理论核心发现：**门控向量 $\boldsymbol{w}_\Delta$ 在训练中逐步学会放大与类别相关特征的对齐，并抑制无关特征**，从而通过选择性状态空间实现一种类似于注意力但通过递归实现的特征过滤。在多数投票数据下，$\boldsymbol{w}_\Delta$ 与正类相关特征的内积具有下界 $\langle \boldsymbol{w}_\Delta^{(T)}, \boldsymbol{o}_+\rangle \geq \frac{\eta T}{8L^2}\,\Theta((\alpha_r L - \alpha_c L)^2)$，而与无关特征的内积维持在 $\widetilde{\mathcal{O}}(1/\mathrm{poly}(d))$；在局部结构数据下，$\boldsymbol{w}_\Delta$ 与无关特征的内积被驱动为负，主动过滤噪声。基于此，论文建立了泛化保证：对于多数投票数据，当样本数 $N \geq \Omega\!\big(L^2 d/(\eta^2 (\alpha_r - \alpha_c)^2)\big)$ 且迭代步数 $T = \Theta\!\big(L^2/(\eta (\alpha_r - \alpha_c)^2)\big)$ 时，模型可实现零泛化误差；对于局部结构数据，样本复杂度和迭代次数由正负样本中类别相关 token 距离的指数差值 $\big[(\frac{1}{2})^{\Delta L_{o_+}^+} - (\frac{1}{2})^{\Delta L_{o_+}^-}\big]^{-1}$（及平方）主导。

合成实验验证了上述理论：更大的多数投票差距或更集中的类别相关 token 显著加速收敛；Mamba 在局部结构数据上表现优于全局注意力与局部注意力基线；5 层 Mamba 模型中，门控向量与 MLP 权重均与类别相关特征呈强正对齐（余弦相似度分别达 0.53 和 0.73），去除门控机制后测试精度大幅下降，印证了门控的选择性作用。

当前分析限于单层单头架构与合成数据设定，未包含残差连接、层归一化等组件，也未与门控 Transformer 等模型进行系统比较。这些局限为未来将理论推广至更深、更真实场景指明了方向。



序列数据的建模长期由 Transformer 主导，其自注意力机制能够动态捕捉上下文依赖，但平方级的计算复杂度驱动了对高效替代方案的研究。状态空间模型（State Space Model, SSM）因具备线性时间复杂度而成为极具竞争力的候选。其中，Mamba 模型通过引入**输入依赖的选择机制**，将传统 S4 中数据无关的离散化步长 $\Delta$ 替换为 $\log(1+e^{\boldsymbol{w}_\Delta^\top \boldsymbol{x}_t})$，并通过可学习的 $\boldsymbol{W}_B^\top \boldsymbol{x}_t$ 和 $\boldsymbol{W}_C^\top \boldsymbol{x}_t$ 生成输入/输出投影（Eq. (2)–(3)），从而实现了类似递推注意力的选择性信息处理。尽管 Mamba 在多项任务中表现优异，其训练过程中的动力学行为与泛化能力的理论基础几乎空白：已有理论分析主要传统 SSM 的表示能力或 Transformer 的注意力训练动态，尚未触及 Mamba 的核心——**门控向量如何在梯度下降优化下动态筛选特征并保障泛化**。

这一缺口导致两个关键问题未被回答：（1）在何种数据和训练条件下，Mamba 能够收敛到零泛化误差？（2）其选择机制如何通过参数更新来实现对类别相关特征的放大和对无关特征的抑制？实践观察表明，Mamba 在局部结构数据上显著优于全局注意力 Transformer 和局部注意力模型（Figure 6），且门控向量 $\boldsymbol{w}_\Delta$ 与类别相关特征的余弦相似度可达 0.53（5-block 模型，Table 3），但缺乏理论解释禁锢了架构改进与风险控制。

本文的动机即在于**为 Mamba 的训练动力学建立首个严格的理论框架**。通过构造一个简化的单层 Mamba 块配合两层 MLP 的分析模型，我们在两类典型的合成数据分布——多数投票（majority-voting）与局部结构（locality-structured）——上，证明了梯度下降能够驱动 $\boldsymbol{w}_\Delta$ 放大类别相关特征（与相关特征的内积下界为 $\Omega(\eta T(\alpha_r-\alpha_c)^2/L^2)$）并压制无关特征（内积 $O(1/\mathrm{poly}(d))$），从而揭示了选择性状态空间具备与注意力机制相似的特征滤波效应，但其实现途径是**通过门控递推而非全局交互**。更进一步，我们建立了非渐近的样本复杂度下界 $N \ge \Omega(L^2 d / (\eta^2 (\alpha_r-\alpha_c)^2))$ 与收敛迭代步数上界 $T = \Theta(L^2 / (\eta (\alpha_r-\alpha_c)^2))$（Theorem 1），以及局部结构数据下由类别相关 token 间距决定的泛化条件（Theorem 2）。这一理论不仅解释了 Mamba 在合成实验中的行为，也为后续扩展至多层、多头架构及更复杂数据分布奠定了分析基础。



## 核心方法与创新机理

本工作的核心创新在于**首次从训练动力学角度揭示 Mamba 输入依赖门控机制的特征过滤作用**，并量化它与泛化性能之间的因果关系。相比传统结构化状态空间模型（如 S4），关键创新体现在两个 **changed slots**：数据驱动的离散化步长 Δ 和输入依赖的投影矩阵 B、C。正是这些变化，使得梯度下降能够自动放大与类别相关特征的对齐，同时抑制或忽略无关特征，从而在不需要全局注意力的条件下实现高效的特征选择。

### 1. 门控驱动特征选择的理论机制

论文构建了简化的 Mamba 块与两层 MLP 结构，通过梯度下降分析展示 **门控向量 $\boldsymbol{w}_\Delta$** 的训练动态。对于多数投票数据，Lemma 4.1 导出 $\langle \boldsymbol{w}_\Delta^{(T)}, \boldsymbol{o}_+ \rangle$ 的下界为 $\frac{\eta T}{8 L^2} \Theta\big((\alpha_r L - \alpha_c L)^2\big)$，而与第 3 类及以上无关特征的内积上界仅为 $\widetilde{\mathcal{O}}(1/\mathrm{poly}(d))$（Eq. 10–12）。在局部结构数据中，Lemma 4.2 进一步表明 $\boldsymbol{w}_\Delta$ 与无关特征的内积被**主动驱向负值**，即门控不仅忽略，还主动压制干扰信息（Eq. 16–18）。这一设计使 Mamba 获得了类似注意力的“相关特征聚焦”能力，但通过选择性递归实现，而非成对交互。

### 2. 架构创新：数据依赖的 Δ 与 B、C

相对于 S4 的数据无关标量 Δ 和固定 B、C 矩阵，所分析的 Mamba 架构引入两个决定性变化（Eq. 2–3）：

- **输入依赖的离散化步长**：$\Delta_t = \log\big(1 + e^{\boldsymbol{w}_\Delta^{\top} \boldsymbol{x}_t}\big)$。门控向量 $\boldsymbol{w}_\Delta$ 控制每一步的状态更新强度，从而根据输入内容调节记忆/遗忘行为。
- **输入依赖的投影矩阵**：$\boldsymbol{b}_t = \boldsymbol{W}_B^{\top} \boldsymbol{x}_t$，$\boldsymbol{c}_t = \boldsymbol{W}_C^{\top} \boldsymbol{x}_t$。这使得序列混合权重与当前 token 内容直接耦合，强化上下文敏感的表征。

上述变化在论文中被形式化为两个可训练的 slot（即 $\boldsymbol{w}_\Delta$ 驱动的 Δ 和 B、C 的输入投影），并证明它们是特征选择能力得以实现的**充分条件**。移除门控的消融实验导致测试准确率大幅下降（Figure 11, 12），进一步验证了这些 changed slots 的关键性。

### 3. 泛化保证：样本复杂度与收敛速度的量化

基于门控的特征过滤效应，论文建立了非渐近泛化界。对于多数投票数据，Theorem 1 给出样本复杂度下界 $N \geq \Omega\big(L^2 d / (\eta^2 (\alpha_r - \alpha_c)^2)\big)$，所需迭代次数 $T = \Theta\big(L^2 / (\eta (\alpha_r - \alpha_c)^2)\big)$（Eq. 13–14）。对于局部结构数据，Theorem 2 显示样本复杂度与迭代数按 $\big[(1/2)^{\Delta L_{o_+}^+} - (1/2)^{\Delta L_{o_+}^-}\big]^{-1}$ 或其平方增长（Eq. 19–21）。这些结果首次将 Mamba 的训练效率与数据中有效信号强度（相关 token 比例差、空间集中度）直接挂钩，并揭示门控在**弱信号下过滤噪声**是泛化的关键瓶颈。

值得注意的是，在局部结构数据上 Mamba 优于全局注意力和局部注意力（Figure 6），因为门控能有效屏蔽位置分散的混淆特征，而注意力机制更容易被此类噪声干扰。这一现象与论文证明的门控负向抑制机制相呼应，表明 selective SSM 在结构性序列中具备隐式的归纳偏置优势。



该理论分析采用一个简化的 Mamba 模型用于二分类任务，其核心管道由三个模块串联组成：**选择性状态空间模块（Mamba block）** → **两层 MLP** → **固定权重的输出聚合层**。整个模型以长度为 `L` 的 token 序列 `X = (x_1, …, x_L)` 为输入，通过梯度下降（GD）在全批量经验风险上联合训练除输出权重 `v` 以外的所有参数，最终实现特征选择驱动的泛化。

### 1. 选择性状态空间模块（Mamba block）
此模块通过**输入依赖的门控机制**将序列转换为每个位置上的隐藏表示 `y_l`，是模型实现特征选择的核心。

- **参数化门控**：不同于 S4 中的标量 `Δ`，Mamba 的门控向量 `w_Δ` 为每个 token `x_t` 动态生成离散化步长：
  ```latex
  Δ_t = \log\big(1 + e^{w_Δ^\top x_t}\big)  \quad \text{(Eq. 2)}
  ```
  同时，输入投影 `b_t` 和输出投影 `c_t` 也变为输入依赖：`b_t = W_B^\top x_t`，`c_t = W_C^\top x_t`。
- **输入门与遗忘门**：将 `Δ_t` 代入 `σ(·)` 得到一对互补的门：
  ```latex
  \bar{b}_t = σ(w_Δ^\top x_t) b_t, \qquad \bar{a}_t = 1 - σ(w_Δ^\top x_t) \quad \text{(Eq. 3)}
  ```
  其中 `\bar{b}_t` 控制当前输入的强度，`\bar{a}_t` 控制上一时刻状态的保留程度。
- **递归输出表示**：拼接上述门控后，Mamba block 在位置 `t` 的输出可写为一系列衰减乘积和的形式：
  ```latex
  y_t = \sum_{s=1}^{t} \biggl( \prod_{j=s+1}^{t} \bigl(1 - σ(w_Δ^\top x_j)\bigr) \biggr) \cdot σ(w_Δ^\top x_s) (W_B^\top x_s)^\top (W_C^\top x_t) x_s \quad \text{(Eq. 5)}
  ```
  这一形式揭示了门控向量的关键作用：它通过 `σ(w_Δ^\top x_t)` 对每个 token 加权，并通过递推乘积实现**依赖序列的上下文衰减**。理论分析（Lemma 4.1, 4.2）表明，梯度更新会驱动 `w_Δ` 与类别相关特征的内积升高，而与无关特征的内积被压低或变为负值，从而动态抑制噪声、放大信号。

### 2. 两层 MLP 与输出聚合
Mamba block 输出的每个 `y_l ∈ ℝ^d` 随后被送入一个两层 MLP：
```latex
F(X) = \frac{1}{L} \sum_{l=1}^{L} \sum_{i=1}^{m} v_i \, \phi\bigl(W_{O(i,\cdot)} y_l(X)\bigr) \quad \text{(Eq. 6)}
```
- **隐藏层**：`m` 个神经元对 `y_l` 执行 `W_O` 的线性变换后通过 ReLU 激活 `ϕ(·)`。
- **固定输出层**：每个神经元的输出乘以固定的随机标量 `v_i ∈ {±1/√m}`，这些权重在训练中保持不变。
- **池化**：所有 token 位置上的贡献被平均，得到最终的标量预测 `F(X)`。

### 3. 训练与泛化目标
模型训练采用 **hinge 损失**的最小化（见 Appendix A.1）：
```latex
\ell(X, z) = \max\bigl(0,\, 1 - z \cdot F(X)\bigr)
```
使用梯度下降在全训练集上优化可训练参数 `Ψ = (W_O, w_Δ, W_B, W_C)`，而 `v` 固定于随机初始化。泛化性能通过总体期望风险 `f(Ψ) = 𝔼_{(X,z)∼𝒟} ℓ(X,z)`（Eq. 9）评估。理论分析证明，在上述结构下，只要样本量满足 `N ≥ Ω(…)` 且步数 `T` 充分，`w_Δ` 即可完成对相关/无关特征的分离，最终实现零泛化误差（Theorem 1, 2）。

> **模块关系小结**：输入序列 ⇨ `w_Δ` 生成门控 ⇨ 递归合成 `y_l` ⇨ MLP 激活+固定加权 ⇨ 平均池化 ⇨ 标量输出。其中 `w_Δ` 是贯穿始终的**因果旋钮**，其与特征的对齐/抑制直接决定了训练动态与泛化能力。



该理论分析聚焦于一个简化的模型架构：一个选择性状态空间模块（Mamba块）后接一个两层MLP，通过全批量梯度下降优化hinge损失。核心机制在于输入依赖的门控向量 $\boldsymbol{w}_\Delta$ 如何动态选择相关特征、压制无关特征，从而实现高效泛化。以下给出关键模块与伴随的核心公式。

### 1. 输入依赖参数生成
对于序列中的第 $t$ 个 token $\boldsymbol{x}_t \in \mathbb{R}^d$，三个数据依赖的参数由可训练的线性投影产生：
$$
\boldsymbol b _ { t } = \boldsymbol W _ { B } ^ { \top } \boldsymbol x _ { t } , \qquad 
\Delta _ { t } = \log \big ( 1 + e ^ { \boldsymbol w _ { \Delta } ^ { \top } \boldsymbol x _ { t } } \big ) , \qquad 
\boldsymbol c _ { t } = \boldsymbol W _ { C } ^ { \top } \boldsymbol x _ { t }
$$
- $\boldsymbol{W}_B, \boldsymbol{W}_C \in \mathbb{R}^{d \times m}$：输入/输出投影矩阵。
- $\boldsymbol{w}_\Delta \in \mathbb{R}^d$：门控参数向量，是选择性机制的核心。
- $\Delta_t$：通过 softplus 函数 $\log(1+e^u)$ 得到的正数值，控制离散化步长和遗忘速度（Eq. 2）。

### 2. 门控信号
基于 $\boldsymbol{w}_\Delta^\top \boldsymbol{x}_t$ 通过 sigmoid $\sigma(\cdot)$ 产生输入门 $\bar{b}_t$ 与遗忘门 $\bar{a}_t$：
$$
\bar { b } _ { t } = \sigma ( \pmb { w } _ { \Delta } ^ { \top } \pmb { x } _ { t } ) \; b _ { t } , \qquad 
\bar { a } _ { t } = 1 - \sigma ( \pmb { w } _ { \Delta } ^ { \top } \pmb { x } _ { t } )
$$
- 当 $\sigma(\boldsymbol{w}_\Delta^\top \boldsymbol{x}_t) \approx 1$ 时，新输入被放大，旧状态被遗忘；当接近 $0$ 时，输入被压制，状态被保留（Eq. 3）。

### 3. 选择性状态空间输出
Mamba块的循环计算可解耦为一种带门控的线性注意力形式，第 $l$ 个输出 token $\boldsymbol{y}_l$ 为：
$$
\sum _ { s = 1 } ^ { t } \Big ( \prod _ { j = s + 1 } ^ { t } \big ( 1 - \sigma ( \pmb { w } _ { \Delta } ^ { \top } \pmb { x } _ { j } ) \big ) \Big ) \cdot 
\sigma ( \pmb { w } _ { \Delta } ^ { \top } \pmb { x } _ { s } ) \;
( \pmb { W } _ { B } ^ { \top } \pmb { x } _ { s } ) ^ { \top } ( \pmb { W } _ { C } ^ { \top } \pmb { x } _ { t } ) \;
\pmb { x } _ { s }
$$
- 乘积项 $\prod (1-\sigma)$ 代表从位置 $s$ 到 $t$ 的累积遗忘（长程衰减）。
- $(\boldsymbol{W}_B^\top \boldsymbol{x}_s)^\top (\boldsymbol{W}_C^\top \boldsymbol{x}_t)$ 度量内容相似度，与注意力机制的内核相似（Eq. 5）。

### 4. 整体预测模型
Mamba的输出经过两层 MLP（带 ReLU）并对所有 token 平均池化：
$$
F ( \pmb { X } ) = \frac { 1 } { L } \sum _ { l = 1 } ^ { L } \sum _ { i = 1 } ^ { m } v _ { i } \;
\phi \bigl( \pmb { W } _ { O ( i , \cdot ) } \pmb { y } _ { l } ( \pmb { X } ) \bigr)
$$
- $\boldsymbol{W}_O \in \mathbb{R}^{m \times d}$：MLP 权重（可训练）。
- $\phi$：ReLU 激活函数。
- $\boldsymbol{v} \in \mathbb{R}^m$：固定随机向量，每个分量独立采样自 $\{\pm 1/\sqrt{m}\}$（训练期间保持不变），起符号分配和幅值归一化作用（Eq. 6）。

### 5. 训练动态中的特征过滤公式
理论推导揭示了梯度下降如何驱动门控向量 $\boldsymbol{w}_\Delta$ 实现特征选择：

**多数投票数据**  
- 门控向量与类别相关特征 $\boldsymbol{o}_+$ 的内积下界为 $\frac{\eta T}{8 L^2} \Theta\bigl((\alpha_r L - \alpha_c L)^2\bigr)$（Eq. 10），而与无关特征 $\boldsymbol{o}_j\;(j\ge 3)$ 的内积上界为 $\widetilde{\mathcal{O}}\bigl(1/\mathrm{poly}(d)\bigr)$（Eq. 12）。  
- 达成零泛化误差的样本复杂度与迭代次数分别满足：
$$
N \geq \Omega\!\Biggl( \frac { L ^ { 2 } d } { \eta ^ { 2 } ( \alpha _ { r } - \alpha _ { c } ) ^ { 2 } } \Biggr) , \qquad
T = \Theta\!\Biggl( \frac { L ^ { 2 } } { \eta ( \alpha _ { r } - \alpha _ { c } ) ^ { 2 } } \Biggr)
$$
其中 $\alpha_r$、$\alpha_c$ 分别为序列中类别相关 token 与混淆 token 的比例，$L$ 为序列长度，$\eta$ 为学习率（Eq. 13–14）。

**局部结构数据**  
- 门控向量与无关特征的内积被驱动为负，即对无关特征进行主动抑制（Lemma 4.2）。  
- 样本复杂度和迭代次数由正/负样本中类别相关 token 距离的差值主导：
$$
N \geq \Omega\!\left( \frac { L ^ { 2 } d } { \eta ^ { 2 } \bigl[ (1/2)^{ \Delta L_{o_{+}}^{+} } - (1/2)^{ \Delta L_{o_{+}}^{-} } \bigr]^{2} } \right)
$$
其中 $\Delta L_{o_{+}}^{+}$ 与 $\Delta L_{o_{+}}^{-}$ 分别度量正、负样本中类别相关 token 的集中程度（Eq. 19）。以上公式的严格推导依赖于对梯度更新的逐项分解（见原文第4.4节）。



## 实验与关键发现

本节通过两类合成序列分类任务（多数投票数据与局部结构数据）验证理论分析的核心结论：训练过程中，Mamba 的输入依赖门控机制能够动态放大类别相关特征、抑制无关特征，从而以可控的样本复杂度和收敛速度实现泛化。所有实验均使用单层单头简化 Mamba 块后接两层 MLP 的模型，优化采用全批量梯度下降和合页损失。

### 合成数据集与评估设定

- **多数投票数据**：每个序列包含 $L$ 个 token，其中 $\alpha_r$ 比例的 token 携带类别相关特征 $o_+$，$\alpha_c$ 比例携带混淆特征 $o_-$，其余为无关特征。标签由类别相关特征的多数投票决定。
- **局部结构数据**：类别相关特征 $o_+$ 集中出现在序列的某一个局部窗口内，而混淆特征 $o_-$ 分布在其他位置，通过 $\Delta L_{o_+}^+$（类别相关 token 之间的最大距离）和 $\Delta L_{o_+}^-$（混淆 token 到类别相关区域的距离）刻画局部集中程度。

我们追踪门控向量 $w_\Delta$、MLP 权重 $W_O$ 与各类特征的对齐度（以余弦相似度或内积度量），并比较不同设定下的收敛速度与最终精度。

### 主实验结果

#### 多数投票数据的收敛与特征选择

理论预测（Theorem 1）表明，样本复杂度和所需迭代步数由类别相关比例与混淆比例之差 $\alpha_r - \alpha_c$ 主导。图 Figure 1 展示了不同 $\alpha_r - \alpha_c$ 下的训练收敛曲线：差值越大，模型收敛所需的 epoch 数显著减少，验证了理论推导的缩放规律。同时，Figure 2 记录了门控向量 $w_\Delta$ 与类别相关特征 $o_+$ 的余弦相似度在训练中持续上升，而与无关特征的相似度几乎不变，直接证实了 Lemma 4.1 的结论——门控向量在梯度下降过程中被驱使与类别相关特征正向对齐，而与无关特征保持 $O(1/\operatorname{poly}(d))$ 量级。

![[assets/figures/papers/repair_max_hvpKqEYJjj_Mamba_Dynamics/figures/002_Figure_1.jpg]]
*Figure 1: Convergence vs. majority-voting gap*

![[assets/figures/papers/repair_max_hvpKqEYJjj_Mamba_Dynamics/figures/005_Figure_2.jpg]]
*Figure 2: Alignment of $\pmb { w } _ { \Delta }$ for majority-voting data. Figure 4: Alignment of ${ \pmb$ w $} _ { \Delta }$ for localitystructured data

#### 局部结构数据的收敛与抑制机制

在局部结构设定下，Theorem 2 指出收敛速度依赖于 $\big[(1/2)^{\Delta L_{o_+}^+} - (1/2)^{\Delta L_{o_+}^-}\big]^{-1}$。Figure 3 显示，当类别相关 token 更加集中（即 $\Delta L_{o_+}^+$ 较小）时，收敛显著加快；而分散的类别相关特征（较大的 $\Delta L$）则导致收敛迟缓，这一定量趋势与理论下界一致。Figure 4 进一步展示，在训练过程中门控向量 $w_\Delta$ 与无关特征的内积被推至负值（或接近零），即主动抑制无关信息；与类别相关特征的对齐则因结构特性维持在零附近（不干扰其他神经元的学习），这吻合 Lemma 4.2 的分析。

![[assets/figures/papers/repair_max_hvpKqEYJjj_Mamba_Dynamics/figures/004_Figure_3.jpg]]
*Figure 3: Convergence under locality-structured data*

#### 与 Transformer 及局部注意力的对比

在局部结构数据上，Figure 6 对比了 Mamba、全局注意力 Transformer 和局部注意力模型。结果显示 Mamba 取得最优分类精度，而全局注意力模型性能接近随机猜测，局部注意力居中。这表明 Mamba 通过选择性状态空间实现的特征选择效应，能够比密集注意力更有效地处理局部结构化信息，避免了无关特征的干扰。

![[assets/figures/papers/repair_max_hvpKqEYJjj_Mamba_Dynamics/figures/008_Figure_6.jpg]]
*Figure 6: Mamba outperforms on locality data*

#### 多层 Mamba 的验证

在 5‑block 的实际 Mamba 模型（多层、每层包含完整的门控与 MLP 结构）上，进一步测量了组件与特征的对齐度（Table 3）。5‑block 模型的 MLP 权重 $W_O$ 与类别相关特征的余弦相似度达到 0.73，同一模型的门控向量 $w_\Delta$ 与类别相关特征的相似度为 0.53，而与无关特征的相似度均接近零。这一定量结果表明理论所揭示的“幸运神经元”对齐行为和门控的特征过滤作用在深层架构中依然显著。

![[assets/figures/papers/repair_max_hvpKqEYJjj_Mamba_Dynamics/figures/011_Table_3.jpg]]
*Table 3: Cosine similarity alignment in the 5-block Mamba model*

### 消融研究

#### 门控机制的必要性

去除输入依赖门控（即令 $\Delta_t$ 固定，使模型退化为无选择的状态空间）后，测试精度在多数投票和局部结构数据上均出现大幅下降（Figure 11、Figure 12），证实 $w_\Delta$ 引导的输入门控是模型捕获类别相关信息、实现高效泛化的关键组件。

![[assets/figures/papers/repair_max_hvpKqEYJjj_Mamba_Dynamics/figures/014_Figure_11.jpg]]
*Figure 11: Test accuracy with and without gating on the majority-voting data*

#### 维度与混淆比例的影响

为进一步验证理论样本复杂度对维度 $d$ 和混淆比例 $\alpha_c$ 的依赖，我们分别改变了特征维度（$d = 32, 64, 128$）和混淆比例（Figure 13‑18）。实验观察到的收敛趋势与理论给出的 $N \ge \Omega(L^2 d / [\eta^2 (\alpha_r - \alpha_c)^2])$ 下界定性一致：更大的 $d$ 和更小的 $\alpha_r - \alpha_c$ 均需更多样本或迭代步数才能达到相同的泛化水平。

### 失败模式与局限性

尽管理论与实验均展示出清晰的泛化保证，但在局部结构数据中，当类别相关 token 极其分散（$\Delta L_{o_+}^+$ 很大）且混淆 token 嵌入类别相关区域（$\Delta L_{o_+}^-$ 很小）时，样本复杂度和收敛速度会急剧恶化；Figure 3 中 $\Delta L$ 较大曲线的缓慢收敛即反映了这一情形。此时门控信号不足以有效区分相关与无关特征，模型需要远多于理论最小需求的样本。此外，所有分析均限于单层单头架构，实际多层 Mamba 中的残差连接、层归一化等组件的影响尚未纳入理论框架，实验中虽观察到深层模型仍继承了特征选择行为，但其定量缩放规律有待进一步研究。

### 重要图表结论总结

- **Table 1、Table 2**：定义符号体系，为理论结果提供参考。
- **Figure 1‑2**：证实多数投票设置下 $\alpha_r - \alpha_c$ 控制收敛速度，门控向量与类别相关特征的正对齐是训练的结果。
- **Figure 3‑4**：证实局部结构设置下 $\Delta L$ 影响收敛，门控向量主动抑制无关特征，而类别相关特征的对齐保持在零附近。
- **Figure 5**：MLP 权重 $W_O$ 在训练中逐步朝类别相关特征的方向增长，与“幸运神经元”现象吻合。
- **Figure 6**：Mamba 在局部结构数据上优于全局注意力 Transformer 和局部注意力，说明选择性状态空间适合处理这类分布。
- **Table 3**：5‑block Mamba 中门控向量和 MLP 权重均显著偏向类别相关特征，验证理论在多层的延伸。
- **消融图（Figure 11‑18）**：移除门控导致性能崩坏，改变 $d$ 和 $\alpha_c$ 的实验支持理论样本复杂度缩放律。



## 定位与知识库关联

本文对Mamba的训练动力学展开理论剖析，属于状态空间模型（SSM）理论框架下的一个工作。相较于此前基于固定参数化SSM（如S4）的研究，本文的核心贡献在于揭示了**输入依赖门控**（以$\boldsymbol{w}_\Delta$为控制旋钮）如何在梯度下降训练中自动实现特征选择，即放大与类别相关特征的对齐并抑制无关特征。这一机制在结构化数据中模拟了注意力机制的特征筛选效应，但其实现路径是通过选择性递归而非softmax注意力或局部窗口。因此，该分析填补了Mamba泛化能力在优化层面的理论空白，并将训练动力学、样本复杂度和收敛速度与数据中的信号强度（如多数投票差距$\alpha_r-\alpha_c$、局部token距离$\Delta L$）定量关联。

### 与基线工作的关系

论文在局部结构合成的数据上直接将Mamba与两类基线进行对比：**Transformer with global attention**和**local attention model**。实验显示（Figure 6），Mamba的分类性能显著优于两者，而全局注意力在该数据上接近随机猜测水平。这一结果印证了理论分析：当位置信息对分类至关重要时，选择性状态空间的逐token门控能够根据上下文抑制远距离的混淆特征，而全局注意力的等权重聚合反而引入噪声；局部注意力虽能避免远程噪声，但缺乏根据输入内容动态调整接受域的能力。因此，Mamba的门控向量$\boldsymbol{w}_\Delta$本质上充当了一种**软性、可学习的相关性过滤器**，其训练行为能够使模型自动从序列中抽取具有判别力的局部或全局模式，具体取决于数据中的结构特征——这一点在多数投票数据和局部结构数据上均得到梯度演化证明（Lemma 4.1, Lemma 4.2）。

需要指出的是，该对比仅局限于合成数据设定，并未涵盖真实语言或视觉任务，也未与门控Transformer、Hyena或RWKV等其他非注意力式模型进行系统的实验或理论比较。因此，目前“Mamba优于注意力”的结论仅适用于所研究的简洁数据分布，其现实泛化强度仍需验证。

### 适用边界

本文的理论结果严格限定于以下设定：

- **数据模型**：二分类任务，输入由带高斯噪声的正交模式$\mathbf{x} = \mathbf{o} + \boldsymbol{\xi}$构成，数据生成遵循两种特定分布——多数投票型与局部结构型。这些分布虽然抽象地捕捉了“相关token占比”与“相关token间距”两类信号特性，但远不能涵盖自然序列中普遍存在的长程依赖、层次化语义或多义性等复杂属性。
- **模型架构**：采用**单层单头简化Mamba块**加**两层MLP**的结构（Eq. (5)-(6)），省略了实际Mamba中的多层堆叠、残差连接、层归一化及卷积起始层等组件。门控参数由$\Delta_t = \log(1+e^{\boldsymbol{w}_\Delta^\top \boldsymbol{x}_t})$引入的softplus形式控制（Eq. (2)-(3)），而输出层的权重$\mathbf{v}$随机固定、MLP第二层权重$\mathbf{W}_O$可训练。
- **优化设定**：采用全批量梯度下降训练hinge损失，学习率固定，且$\boldsymbol{w}_\Delta$的初始化为零向量。理论结果依赖于该初始化带来的对称性破缺过程中的“幸运神经元”动态（Appendix A.2）。
- **泛化保证**：在多数投票数据上，零泛化误差的样本复杂度和迭代次数分别下界为$N \geq \Omega(L^2 d / (\eta^2 (\alpha_r - \alpha_c)^2))$和$T = \Theta(L^2 / (\eta (\alpha_r - \alpha_c)^2))$（Theorem 1）；在局部结构数据上，指标由相关token的位置差$\Delta L_{o_+}^+$和$\Delta L_{o_+}^-$的指数差值的倒数控制（Theorem 2）。这些界限说明，当信号强度（$\alpha_r-\alpha_c$或局部聚集程度）增强时，所需样本和训练步数迅速下降。

任何超出上述假设的扩展（如更深的模型、不同的损失函数、随机优化器等）均不能直接套用本文给出的定量结论。

### 局限与开放问题

该工作的主要局限包括：
1. 理论分析独立于实际Mamba架构的多数组件，如深度叠加、多头机制、残差流和归一化层，因此其结论在完整系统中的保持性未知。
2. 数据生成过程高度简化，仅包含正交特征与高斯噪声，无法模拟现实世界中特征的共现、相关、上下文依赖等复杂性。
3. 与competitor的对比缺乏广泛性：虽比较了Transformer与局部注意力，但未纳入门控线性单元、门控Transformer或其它SSM变体（如Mamba-2），也未提供理论层面的统一分析。
4. 分析依赖特定的梯度下降设置和初始化条件（$\boldsymbol{w}_\Delta = \mathbf{0}$，$\mathbf{v}$固定），对于其他优化器或初始化策略不具通用性。
5. 实验仅在合成数据上开展，虽能验证理论趋势，但无法评估真实任务上的泛化极限。

相应的开放问题包括：
- 如何将分析框架从单层推广至多层、多头Mamba体系？隐式特征场的交互是否会导致新的动态现象？
- 当数据中存在更丰富的依赖结构（如组合特征、层次性、时序因果关系）时，选择性状态空间的门控是否会涌现更复杂的滤波策略？
- 该理论能否为门控Transformer或Mamba-Transformer混合架构提供解释？门控向量与注意力的训练动力学存在何种本质共性和根本分界？
- 门控机制是否天然对某些类型的分布外样本更鲁棒？该特性能否转化为泛化界给予严格刻画？

总体而言，本文为选择性SSM的训练与泛化行为搭建了扎实的首个理论台阶，但其知识库定位更偏向“机制解释”而非“实用指导”。未来工作需在深度架构和真实数据两个方向上同步推进，方能将理论洞见转化为具有广泛适用性的设计原则。



## 原文 PDF

![[paperPDFs/ICLR_2026/A_Theoretical_Analysis_of_Mambas_Training_Dynamics_Filtering_Relevant_Features_for_Generalization_in_State_Space_Models.pdf]]

---
title: "Muon Outperforms Adam in Tail-End Associative Memory Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Muon_Outperforms_Adam_in_Tail_End_Associative_Memory_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: twbMFL0DMp
aliases:
- MOATEAML
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "Muon updates associative-memory matrices with the orthogonal factor of the matrix gradient, removing singular-value magnitude bias."
primary_logic: "It applies spectral-normalized updates mainly to VO and FFN matrices, balancing high- and low-frequency fact directions in long-tail learning."
claims:
- "Muon’s gains concentrate in VO and FFN components that behave like linear associative memories."
- "Spectral normalization produces more isotropic weight spectra than Adam."
- "The note reports lower FineWeb validation loss and better tail-class accuracy than Adam."
---

# Muon Outperforms Adam in Tail-End Associative Memory Learning

> [!tip] 核心洞察
> Muon 将矩阵梯度替换为正交因子更新，削弱奇异值幅度差异带来的频率偏置；这一谱范数几何与 Transformer 的 VO/FFN 联想记忆结构匹配，因此更利于尾部事实学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Muon Outperforms Adam in Tail-End Associative Memory Learning |
| 英文题名 | Muon Outperforms Adam in Tail-End Associative Memory Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=twbMFL0DMp) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

在长尾分布下的语言模型预训练中，不同事实的出现频率差异悬殊，导致基于梯度幅度的优化器（如 Adam）倾向于优先学习高频事实，而尾部事实的学习则明显滞后。论文 **《Muon Outperforms Adam in Tail-End Associative Memory Learning》** 针对这一问题，提出将 Muon 优化器应用于 Transformer 的关键权重矩阵，以实现对高频与低频事实的更均衡学习。

核心结论是：**Muon 在验证损失上显著优于 Adam**。在 160M 参数 NanoGPT 模型（非门控 FFN）的 FineWeb 基准上，训练至 10,000 步时，纯 Muon 的验证损失为 **3.565**，而纯 Adam 为 **3.924**，绝对改善达 **-0.359**（见 Figure 1(d)）。这一优势源于 Muon 更新规则与线性联想记忆外积结构的天然对齐——Muon 通过将原始梯度替换为其归一化正交因子之和，实质上是对谱范数执行最陡下降，从而在更新中为各正交“事实”分量赋予均等权重，无论其在梯度中的原始系数大小。

方法定位上，Muon 并非全面替代 Adam，而是**选择性应用于 Transformer 中最具联想记忆特性的组件**。实验表明，仅对 Value-Output（VO）投影和 FFN 模块施加 Muon，即可几乎完全复现全模型 Muon 的训练轨迹；而仅对 Query-Key（QK）施加 Muon 则收益有限。这揭示出 VO 和 FFN 是 Muon 发挥优势的关键瓶颈模块。

主要结果包括：Muon 使权重矩阵的奇异值谱在训练全程保持更高的各向同性（更高的 SVD 熵与有效秩，更低的 Top-10 能量占比）；在重尾知识任务上，Muon 对低频类别的首 token 准确率提升尤为突出，有效缩小了头尾差距。这些发现共同指向一个机制性解释：Muon 通过谱归一化抵消了梯度中由频率差异引入的幅度偏差，从而在联想记忆学习中实现了更均匀的事实获取。



大规模语言模型预训练的核心挑战之一，在于数据天然服从**重尾分布**：少量高频模式与大量长尾模式共存。在这种分布下，优化器的选择直接影响模型对尾部知识的吸收能力。传统优化器如 Adam 虽然收敛迅速，但其逐元素归一化的更新机制会**破坏梯度矩阵的内在结构**，导致不同知识项的更新强度失衡——头部类被过度强化，而尾部类学习不足。

这一结构性问题在 Transformer 的线性层中尤为突出。Transformer 的注意力模块和 FFN 模块均可表示为矩阵乘法与 softmax/激活函数的组合，其权重矩阵的梯度自然呈现**外积结构**。然而，Adam 对梯度每个元素独立进行符号提取和尺度归一化，使得更新方向偏离了梯度矩阵的谱结构，削弱了对尾部关联记忆的有效编码。

Muon 优化器（Bernstein & Newhouse, 2024）提出了一种根本不同的更新范式：**用梯度矩阵的最近（半）正交矩阵替代原始梯度**，等价于在谱范数约束下执行最陡下降。这一操作保留了梯度的外积结构，使所有更新方向的强度趋于均衡——从奇异值分布角度看，Muon 更新矩阵的奇异值近乎相同，而 Adam 的更新矩阵则呈现高度集中的能量分布。

本文的核心动机在于**系统性地揭示 Muon 在尾部关联记忆学习中的优势机制**。具体而言，作者试图回答：Muon 为何能在重尾分布下实现比 Adam 更平衡的类间学习？这一优势在真实 Transformer 训练中如何体现？通过将 Transformer 的 FFN 层抽象为线性关联记忆模型，结合理论分析和受控实验，本文建立了从优化器更新规则到尾部知识获取能力的因果链条，并在一系列规模化的语言模型预训练任务上验证了 Muon 的显著增益。



## 核心方法与创新机理

Muon 的核心创新在于**将权重矩阵的更新规则从逐元素符号/幅度归一化，转向基于矩阵谱范数的结构归一化**。具体而言，Muon 在每一步对动量累加器 $B_t$ 计算（或近似）奇异值分解 $B_t = U_t S_t V_t^\top$，然后抛弃奇异值矩阵 $S_t$，仅保留正交因子 $O_t = U_t V_t^\top$ 作为更新方向。这一操作可被解释为在谱范数约束下的最速下降（Bernstein & Newhouse, 2024），其更新形式为：

$$\Delta \mathbf{W}^* = -\frac{\operatorname{tr}(\Sigma)}{\lambda} \cdot \mathbf{U} \mathbf{V}^\top$$

相比之下，Adam 在动量机制退化为 SignGD 时，等价于在 $\ell_\infty$ 范数下的最速下降，其更新仅保留梯度的逐元素符号：

$$\Delta \mathbf{w}^* = -\frac{\lVert \mathbf{g} \rVert_1}{\lambda} \cdot \mathrm{sign}(\mathbf{g})$$

这一 **changed slot**——从“逐元素符号”到“矩阵正交因子”——是 Muon 区别于 Adam 的根本机制差异。

**为什么这个改变对 Transformer 有效？** 论文给出的核心洞察是：Transformer 中的 Value-Output（VO）通路和 Feed-Forward Network（FFN）在功能上构成线性联想存储器，其权重天然具有外积结构 $W = \sum_i e_{o_i} e_{s_i}^\top$。当训练数据呈长尾分布时，梯度 $G = \sum_i s_i u_i v_i^\top$ 中高频“事实”对应较大的奇异值 $s_i$，低频“事实”对应较小的奇异值。Adam 的符号更新会保留这种奇异值幅度差异，导致低频事实学习不足；而 Muon 通过归一化掉 $S_t$，强制更新 $O_t = \sum_i u_i v_i^\top$ 对所有正交方向赋予等权重，从而**平衡高频与低频事实的学习速度**。

**关键证据支撑：**

1. **组件消融实验**（Figure 1）：在 160M NanoGPT 非门控 FFN 模型上，仅对 VO 和 FFN 权重应用 Muon 即可几乎完全复现全模型 Muon 的验证损失轨迹（step 10,000 时 Muon 损失 3.565 vs Adam 3.924，差距 -0.359）。而对 QK 权重单独应用 Muon 收益有限，表明 Muon 的增益高度集中在具有外积结构的 VO 和 FFN 模块——这正是联想存储器假设所预测的。

2. **权重谱各向同性分析**（Figure 2）：Muon 训练出的 VO 和 FFN 权重矩阵在 SVD 熵、有效秩（eRank）等指标上显著高于 Adam，且从训练初期即表现出更强的各向同性。这意味着 Muon 确实在机制层面抑制了少数主导奇异值对权重更新的垄断。

3. **长尾知识任务验证**（Figure 3）：在人工构造的幂律分布知识任务上，Muon 对低频类别的首 token 准确率（FTA）显著优于 Adam，且 Muon(VO,FFN)/Adam(QK) 的混合配置大幅缩小了头尾类别差距，而 Muon(QK)/Adam(VO,FFN) 则无此效果——直接验证了“Muon 通过 VO/FFN 的外积结构实现尾类学习平衡”的因果链条。

**实践中的近似实现：** 完整 SVD 计算开销较大，实践中 Muon 使用固定次数（如 5 次）的 Newton-Schulz 迭代近似 $B_t (B_t^\top B_t)^{-1/2}$，在保持谱归一化效果的同时避免了显式 SVD。

综上，Muon 的创新并非简单的优化器调参，而是**将优化器的几何假设从向量 $\ell_\infty$ 空间切换到矩阵谱范数空间**，这一切换恰好匹配了 Transformer 中 VO 和 FFN 权重的联想存储器结构，从而系统性地改善了对长尾分布数据的学习。



论文围绕一个核心命题展开：Muon 优化器在 Transformer 的长尾关联记忆学习中为何优于 Adam。研究框架由三个层次构成——**经验分解**、**机制解释**和**理论验证**，逐层递进地揭示 Muon 的优势来源。

### 经验分解层

首先在标准语言建模任务（FineWeb，160M NanoGPT，非门控 FFN）上定位 Muon 的有效作用域。通过将 Transformer 的权重矩阵分组为 VO（$W_V, W_O$）、QK（$W_Q, W_K$）和 FFN（$W_{\text{in}}, W_{\text{out}}$），并对不同组分别施加 Muon 或 Adam，系统性地测量各组对性能增益的贡献。核心发现是：**Muon 的主要增益集中在 VO 和 FFN 矩阵上**，仅对 VO+FFN 使用 Muon 几乎可以恢复全 Muon 的训练轨迹（Figure 1(b,d)），而对 QK 使用 Muon 的边际收益有限。

### 机制解释层

基于经验分解的结果，将 VO 和 FFN 矩阵统一建模为**线性关联记忆**（linear associative memories），其权重矩阵具有外积结构 $W = \sum_{i=1}^{K} e_{o_i} e_{s_i}^{\top}$。在这一视角下，梯度 $G$ 的 SVD 分解 $G = U S V^{\top} = \sum_{i=1}^{d} s_i u_i v_i^{\top}$ 中的奇异值 $s_i$ 反映了不同“事实”在梯度中的强度差异——高频事实对应大奇异值，低频尾类事实对应小奇异值。Adam 等基于梯度幅度的优化器天然偏向大奇异值方向，导致尾类学习不足；而 Muon 通过计算 $O = U V^{\top}$ **归一化掉了奇异值 $S$**，使更新在各正交事实上分配等量权重，从而实现对高频和低频事实的均衡学习。

为验证这一机制，研究从两个维度展开：
- **权重谱各向同性分析**：在训练过程中持续监测 VO 和 FFN 矩阵的 SVD 熵、有效秩（eRank）、Top-10 能量占比（Top10E）和四分位比（Q75/Q25）。Muon 从训练初期就产生显著更各向同性的奇异值谱（Figure 2），表明其权重矩阵更均衡地利用了所有方向。
- **长尾知识任务验证**：在人工构造的幂律分布知识任务上，Muon 在低频尾类上取得显著更高的首 token 准确率（FTA），且不同频率类别间的收敛速度更均匀（Figure 3）。进一步消融确认，将 Muon 施加于 VO+FFN 即可显著缩小头尾差距，而仅施加于 QK 则效果有限。

### 理论验证层

为隔离并形式化 Muon 的均衡学习性质，构建了一个简化的单层模型：保留关联记忆矩阵 $W$ 和语言模型头，将前置模块替换为给定的正交特征嵌入 $E, \tilde{E}$（其正交性在 Llama3-8b-instruct 的 FFN 层中得到实证验证，角度接近 90°，Figure 4(a)）。在此设定下，分析三种简化优化器（关闭动量）：GD、SignGD（Adam 的特例，$\beta_1 = \beta_2 = 0$）和 Muon。定义最大概率差距 $\Delta(W) := \max_{i,j} [f_W(E_i)]_i - [f_W(E_j)]_j$ 来量化学习不平衡程度。

理论结果（Theorem 4.3）表明：在数据分布存在不平衡比 $r \in (0,1]$ 的情况下，GD 一步更新的最小正确类概率上界为 $\varrho_{\text{GD}}^{\varepsilon} = O(\epsilon^{-r(\alpha,\beta)} K^{r(\alpha,\beta)-1})$，随不平衡程度恶化；而 Muon 一步更新的对应下界为 $\varrho_{\text{Muon}}^{\varepsilon} \geq 1 - \epsilon(1 + O(\frac{\log K}{K}))$，几乎不受数据不平衡影响。这一理论预测与一步和多步实验结果定性一致（Figure 4(b,c)）：GD 在 $\Delta(W)$ 上表现出显著不平衡，而 Muon 始终保持高度均衡。

### 输入输出流

整体框架的输入为 Transformer 各权重矩阵的训练梯度，输出为优化器更新后的权重。信息流如下：

1. **分组决策**：根据经验分解结果，将权重矩阵划分为 VO+FFN（Muon 高增益组）和 QK（Adam 基线组）。
2. **Muon 更新路径**：对 VO+FFN 组，累积动量 $B_t$，通过 Newton-Schulz 迭代（实践中 5 次）近似计算 $O_t = U_t V_t^{\top}$（等价于 SVD 后归一化奇异值），形成与谱范数最速下降方向对齐的更新。
3. **Adam 更新路径**：对 QK 组，保持标准的 $\ell_{\infty}$ 范数最速下降更新。
4. **权重更新**：各组更新合并后施加于对应权重矩阵，完成一步训练。



### Transformer 中的线性联想记忆结构

论文将 Transformer 中的注意力模块和前馈模块统一抽象为线性联想记忆（Linear Associative Memory）的形式。对于一个存储了 $K$ 条事实的记忆矩阵，其构造为：

$$W = \sum_{i=1}^{K} e_{o_i} e_{s_i}^{\top}$$

其中 $e_{s_i}$ 和 $e_{o_i}$ 分别为第 $i$ 条事实的输入嵌入和输出嵌入。Transformer 的两个核心模块可表示为该结构的实例化：

**注意力模块**（第 $\ell$ 层）：

$$H^{(\ell)} = X^{(\ell-1)} + \sum_{h=1}^{H} W_{O,h}^{(\ell)} W_{V,h}^{(\ell)} X^{(\ell-1)} \mathsf{sm}\big( X^{(\ell-1),\top} W_{K,h}^{(\ell),\top} W_{Q,h}^{(\ell)} X^{(\ell-1)} \big)$$

其中 $W_O W_V$ 构成一个隐式的联想记忆矩阵，$W_Q$ 和 $W_K$ 负责生成查询和键。

**前馈模块**（非门控，第 $\ell$ 层）：

$$X^{(\ell)} = H^{(\ell)} + W_{\mathrm{out}}^{(\ell)} \sigma( W_{\mathrm{in}}^{(\ell)} H^{(\ell)} )$$

其中 $W_{\mathrm{in}}$ 和 $W_{\mathrm{out}}$ 分别对应输入和输出嵌入矩阵，$\sigma$ 为激活函数。门控变体则引入额外的门控权重 $W_{\mathrm{gate}}$。

### Muon 优化器的核心更新规则

Muon 的关键创新在于将原始梯度替换为其归一化正交因子之和。给定动量累加器 $B_t$，Muon 的更新步骤为：

1. 计算 $B_t$ 的奇异值分解（SVD）：$B_t = U_t S_t V_t^{\top}$
2. 构造最近（半）正交矩阵：$O_t = U_t V_t^{\top}$
3. 以 $O_t$ 作为更新方向

在工程实现中，可通过固定次数（如 5 次）的 Newton-Schulz 迭代近似 $O_t$，避免完整 SVD 计算，同时保留尺度归一化效果。

### 梯度 SVD 与 Muon 更新的关联

对于线性联想记忆的损失函数梯度 $G = \nabla_W \mathcal{L}$，其 SVD 为：

$$G = U S V^{\top} = \sum_{i=1}^{d} s_i u_i v_i^{\top}$$

其中 $s_i$ 为奇异值，反映了第 $i$ 个正交方向上的梯度强度。Muon 通过归一化去除 $S$，构造更新：

$$O = U V^{\top} = \sum_{i=1}^{d} u_i v_i^{\top}$$

这意味着 Muon 对所有正交方向赋予等权重，不受原始梯度幅值差异的影响——这正是其在长尾分布中能更均衡地学习高频和低频事实的核心机制。

### 优化器的最速下降解释

附录 D 从最速下降框架统一解释了各优化器：

- **Muon**：在权重矩阵上施加谱范数约束时的最速下降方向，更新为 $\Delta \mathbf{W}^{*} = -\frac{\mathrm{tr}(\Sigma)}{\lambda} \cdot \mathbf{U} \mathbf{V}^{\top}$
- **Adam**（简化至 SignGD 时）：在展平参数向量上施加 $\ell_{\infty}$ 范数约束时的最速下降方向，更新为 $\Delta \mathbf{w}^{*} = -\frac{\lVert \mathbf{g} \rVert_1}{\lambda} \cdot \mathrm{sign}(\mathbf{g})$

这一解释揭示了 Muon 与 Adam 的本质差异：前者在矩阵空间中以谱范数几何进行优化，后者在向量空间中以无穷范数几何进行优化。



## 实验与关键发现

### 主要结果：Muon 在 NanoGPT 基准上的验证损失优势

在 FineWeb 语料上训练 160M 参数 NanoGPT（非门控 FFN）的验证损失对比中，Muon 显著优于 Adam。Figure 1(d) 的柱状图给出了 step 10,000 时的验证损失：纯 Muon 达到 **3.565**，纯 Adam 为 **3.924**，差距 **-0.359**。这一结果直接锚定了 Muon 在该基准上的性能优势。


![[assets/figures/papers/iclr26_0009_twbMFL0DMp_Muon_Outperforms_Adam_in_Tail-End_Associative_Me/figures/004_Figure_1.jpg]]
*Figure 1: Validation loss comparison on the 160M NanoGPT model with non-gated FFN under different Muon/Adam assignments. Panels (a) and (b) show the validation loss over training steps for the Independent Blocks and Combined Configurations settings, respectively. Panels (c) and (d) report the corresponding validation loss at step 10,000 for each mode, summarizing the final performance of the Independent Blocks and Combined Configurations*

混合配置进一步揭示了优化器分配的关键性。Muon(VO, FFN) / Adam(QK) 组合的验证损失约为 3.586–3.678，几乎完全恢复纯 Muon 的训练轨迹。这表明 **Muon 的增益主要来自 VO（Value-Output）权重和 FFN 权重**，而非 QK（Query-Key）权重。

### 组件级消融：哪些权重矩阵从 Muon 受益最大？

Figure 1(a–b) 的消融实验系统拆解了不同权重矩阵对 Muon 的敏感度：

- **VO 权重是核心瓶颈**：仅对 W_V 或仅对 W_O 应用 Muon，已产生远大于对 QK 应用 Muon 的增益。Figure 1(c) 显示，Muon on VO / Adam on QK and FFN 的验证损失曲线显著低于反向配置。
- **W_O 比 W_V 更具影响力**：Figure 1(b) 中，V+FFN 变体的损失下降幅度更大，表明 W_O 在 VO+FFN 组合中承担更关键的角色。
- **VO+FFN 几乎等价于全 Muon**：Observation 1 指出，仅对 VO 和 FFN 应用 Muon 即可接近全 Muon 轨迹。这为实际部署提供了计算效率更高的混合策略。

这些消融结果与 Muon 的核心机制一致：Muon 的更新规则 $O = UV^\top$ 通过 SVD 归一化去除奇异值 $S$，使更新在正交事实上分配均等权重。VO 和 FFN 权重天然具有外积结构（$W_O W_V$ 和 $W_{\text{out}} W_{\text{in}}$），与 Muon 的归一化特性高度契合；而 QK 权重通过 softmax 非线性耦合，不直接受益于这种谱归一化。

### 谱各向同性：Muon 训练出更均匀的权重结构

Figure 2 从权重矩阵的奇异值分布角度揭示了 Muon 与 Adam 的本质差异。在训练全程中，Muon 持续产生比 Adam 更各向同性的权重：


![[assets/figures/papers/iclr26_0009_twbMFL0DMp_Muon_Outperforms_Adam_in_Tail-End_Associative_Me/figures/005_Figure_2.jpg]]
*Figure 2: Spectral Dynamics of Transformer Weight Matrices During Training. Each panel reports four metrics characterizing singular value distributions: SVD entropy, Top10E, eRank, and Q75/Q25 ratio. The four subplots correspond to different weight matrix groups: (a) VO and (b) $W _ { \mathrm { o u t } }$*

- **SVD 熵**（$H_{\text{norm}}$）和 **有效秩**（eRank）在 Muon 下显著更高；
- **Top-10 能量占比**（Top10E）和 **Q75/Q25 比值**在 Muon 下显著更低。

这意味着 Muon 的权重矩阵利用更多奇异方向，而非将能量集中于少数主导方向。这一谱特性从训练初期即显现，与 Muon 更新规则中“归一化去除 $S$”的操作直接对应——通过强制各奇异方向贡献均等，Muon 阻止了权重向少数高频模式坍缩。

### 重尾知识任务：Muon 对低频类别的学习优势

在人工构造的重尾知识任务中（类别频率服从幂律分布），Muon 展现出对尾部类别的显著学习优势。Figure 3(b–d) 和 Table 2–4 给出了关键证据：


![[assets/figures/papers/iclr26_0009_twbMFL0DMp_Muon_Outperforms_Adam_in_Tail-End_Associative_Me/figures/033_Table_2.jpg]]
*Table 2: Heavy-tail knowledge task: Group performance by optimizer (2,000 steps)*

- **收敛速度与均匀性**：Muon 在所有频率类别上实现更快且更均匀的收敛，误差棒更紧。Table 4（10,000 steps）显示 Muon 在 Group 11/13/15 上分别达到 1.000/1.000/0.976，而 Adam 在 Group 15 上仅为 0.558。
- **头尾差距缩小**：Muon 有效降低了高频与低频类别之间的性能差距。Figure 3(e–f) 的消融确认，**Muon on VO+FFN 是缩小头尾差距的关键**，而 Muon on QK 对此贡献有限。


![[assets/figures/papers/iclr26_0009_twbMFL0DMp_Muon_Outperforms_Adam_in_Tail-End_Associative_Me/figures/035_Table_4.jpg]]
*Table 4: Heavy-tail knowledge task: Group performance by optimizer (10,000 steps)*

这一结果直接验证了 Section 3.1 的理论直觉：Muon 通过归一化奇异值，使更新在正交事实上分配均等权重，从而对高频和低频事实进行更均衡的学习。Adam 基于梯度幅值（sign）的更新则天然偏向高频事实，导致尾部类别学习不足。

### 门控 FFN 的扩展验证

在门控 FFN 架构上的重尾知识任务中，Muon 的优势保持一致。Figure 12 和 Table 5–7 显示：


![[assets/figures/papers/iclr26_0009_twbMFL0DMp_Muon_Outperforms_Adam_in_Tail-End_Associative_Me/figures/041_Figure_12.jpg]]
*Figure 12: Performance comparison of different optimizers on a heavy-tailed knowledge task with gated feed-forward networks. (a) The distribution of samples per class follows a power law. (b-d) Performance of Muon, Adam, and SGD+Momentum optimizers. (e) Muon (VO, FFN)/Adam (QK). (f) Muon (QK)/Adam (VO, FFN)*

- Muon 在所有组别上持续优于 Adam 和 SGD+Momentum；
- Muon(VO, FFN) 变体几乎完全复现全 Muon 性能（Table 7：Group 11/13 均达到 1.000±0.000）；
- Group 15（最尾部类别）上，Muon 达到 0.976，而 Adam 仅为 0.558。

这表明 Muon 的增益不依赖于特定 FFN 架构（门控/非门控），具有较好的泛化性。

### 失败模式与局限

需要手动验证的潜在问题：

- **QK 权重的负迁移风险**：消融实验一致表明 Muon 对 QK 的增益有限甚至无增益。若将 Muon 盲目应用于所有矩阵，QK 部分的额外计算开销（Newton-Schulz 迭代近似 SVD）可能无法被收益覆盖。
- **小批量下的 SVD 近似质量**：论文使用固定次数（如 5 次）的 Newton-Schulz 迭代近似 $O_t$，在小批量或高条件数场景下，近似的正交性可能退化。当前实验未系统评估这一边界。
- **长尾外的泛化**：重尾知识任务是人工构造的，Wikitext-103（Figure 15）提供了初步的自然语料验证，但更大规模、更多样化的自然语言基准仍需补充。

### 补充图表

![[assets/figures/papers/iclr26_0009_twbMFL0DMp_Muon_Outperforms_Adam_in_Tail-End_Associative_Me/figures/014_Figure_14.jpg]]
*Figure 14: (a) Average Angles Between $E _ { i } / \widetilde { E } _ { i }$ (b) One-step Optimization Results (c) Multi-step Optimization Results*




## 定位与知识库关联

### 与基线方法的关系

Muon 与 Adam 的核心差异源于优化几何的不同选择。在 steepest descent 框架下，Adam 可理解为在向量 $\ell_\infty$ 范数下的最速下降，其更新等价于 $\Delta\mathbf{w}^* = -\frac{\|\mathbf{g}\|_1}{\lambda} \cdot \mathrm{sign}(\mathbf{g})$；而 Muon 则在矩阵谱范数下进行最速下降，更新形式为 $\Delta\mathbf{W}^* = -\frac{\mathrm{tr}(\Sigma)}{\lambda} \cdot \mathbf{U}\mathbf{V}^\top$。这一几何差异使得 Muon 天然适配线性联想记忆的外积结构——记忆矩阵 $W = \sum_{i=1}^{K} e_{o_i} e_{s_i}^\top$ 本身就是外积之和，而 Muon 通过对梯度 $G = U S V^\top$ 的奇异值进行归一化（丢弃 $S$），形成更新 $O = U V^\top$，从而对高频和低频事实分配均等的更新权重。相比之下，Adam 的更新幅度由梯度幅值主导，在高频项上分配更多更新资源，导致尾部类学习不足。

在实验层面，FineWeb 验证损失（160M NanoGPT，非门控 FFN，第 10,000 步）显示：纯 Muon 达到 3.565，纯 Adam 为 3.924，差距为 -0.359（置信度 0.95，见 Figure 1(d)）。这一差距在重尾知识任务中进一步分化为：Muon 在低频（尾部）类别上的首 token 准确率（FTA）显著优于 Adam，且误差条更紧致（Figure 3）。

### 适用边界与组件特异性

Muon 的增益并非均匀分布在所有 Transformer 组件上。关键发现是：**Muon 对 VO（Value-Output）和 FFN 权重最有效，对 QK（Query-Key）权重增益有限**。

具体而言：
- 仅对 VO+FFN 应用 Muon、其余用 Adam 的配置，几乎完全恢复了全 Muon 的训练轨迹（Figure 1(b)）。
- 仅对 $W_V$ 或仅对 $W_O$ 应用 Muon 的增益，远大于仅对 QK 应用 Muon 的增益（Figure 1(a, c)）。
- 在 VO+FFN 内部，$W_O$ 比 $W_V$ 更具影响力（Figure 1(b, d)），V+FFN 变体的损失下降幅度更大。

这一组件特异性在重尾知识任务中得到印证：Muon(VO,FFN)/Adam(QK) 显著缩小了头尾类差距，而 Muon(QK)/Adam(VO,FFN) 的改善有限（Figure 3(e-f)）。

从机制角度，这种差异源于 VO 和 FFN 权重直接参与联想记忆的外积构建（$W_O W_V$ 和 $W_{\mathrm{out}} W_{\mathrm{in}}$），而 QK 权重通过 softmax 非线性间接影响记忆检索，其外积结构被注意力归一化所稀释。

### 局限与开放问题

**局限：**

1. **组件适用性有限**：Muon 对 QK 权重的增益不显著，意味着并非所有矩阵参数都受益于谱范数最速下降。这限制了 Muon 作为通用优化器替代 Adam 的直接性——实践中需要选择性应用。
2. **理论分析限于单步与简化设定**：理论保证（Theorem 4.3）建立在单步优化、无动量、嵌入正交（Assumption 4.1）的简化模型上。虽然 Llama3-8b-instruct 的 FFN 层中 $E_i$ 与 $\widetilde{E}_i$ 的平均夹角接近 90°（Figure 4(a)），为假设提供了经验支撑，但多步、带动量的实际训练场景尚未得到严格理论刻画。
3. **计算开销**：Muon 每步需要 SVD 或 Newton-Schulz 迭代来近似正交矩阵，虽然实践中可用固定次数（如 5 次）迭代近似，但相比 Adam 的逐元素 sign 操作仍有额外计算成本。

**开放问题：**

1. **高阶张量积的扩展**：论文明确指出，Muon 对线性联想记忆外积结构的适配性可能扩展到高阶张量积，这是一个值得探索的方向（part_007）。
2. **组件选择的理论判据**：什么结构特征决定了某个 Transformer 组件是否受益于 Muon？目前仅有经验观察（VO/FFN 受益，QK 不显著），缺乏理论判据来预测新架构中 Muon 的适用位置。
3. **与动量机制的深层交互**：理论分析中为清晰起见禁用了动量（$\beta_1 = \beta_2 = 0$），但实际 Muon 使用动量累积矩阵 $B_t$。动量如何与谱归一化交互、是否引入新的动力学效应，尚待分析。
4. **更大规模验证**：当前主要结果基于 160M NanoGPT 和重尾知识任务，Muon 在更大规模模型（如 7B+）和更通用预训练任务上的表现需进一步验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/Muon_Outperforms_Adam_in_Tail_End_Associative_Memory_Learning.pdf]]

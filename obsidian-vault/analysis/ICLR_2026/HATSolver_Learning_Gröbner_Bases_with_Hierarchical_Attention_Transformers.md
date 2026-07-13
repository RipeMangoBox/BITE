---
title: "HATSolver: Learning Gröbner Bases with Hierarchical Attention Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: "paperPDFs/ICLR_2026/HATSolver_Learning_Gröbner_Bases_with_Hierarchical_Attention_Transformers.pdf"
project_link: null
code_link: null
openreview_forum_id: 5C3LljOEGC
aliases:
- HHATGBB
- HATSolver
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "采用树状分层注意力机制替代全局注意力，通过局部层内注意力和跨层交叉注意力大幅降低序列长度和计算复杂度，并辅以课程学习逐步提升难度。"
primary_logic: "多项式系统天然具有系统→方程→项→符号的树形层次结构，将注意力限定在局部和父子节点之间，既保留了长程依赖，又使复杂度从O(L²d)降至O(L^{1+1/n}d)，从而突破扩展性瓶颈。"
claims:
- "在相同训练时间内，HATSolver-2和-3比基线Transformer收敛更快、准确率更高（Figure 2）。"
- "HATSolver-3在13变量系统上完全匹配准确率达61.2%，而STD-FGLM仅6.1%，Msolve仅4.5%，推理时间也更短（Table 1）。"
- "去除课程学习后，13变量90%密度下准确率从61.2%骤降至33.85%，但仍优于经典算法（Table 2）。"
- "基线Transformer在n=10时准确率为0%，而HATSolver-3达到8%（Figure 5）。"
---

# HATSolver: Learning Gröbner Bases with Hierarchical Attention Transformers

> [!tip] 核心洞察
> 多项式系统天然具有系统→方程→项→符号的树形层次结构，将注意力限定在局部和父子节点之间，既保留了长程依赖，又使复杂度从O(L²d)降至O(L^{1+1/n}d)，从而突破扩展性瓶颈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | HATSolver：基于分层注意力变换器的Gröbner基学习方法 |
| 英文题名 | HATSolver: Learning Gröbner Bases with Hierarchical Attention Transformers |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=5C3LljOEGC) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | HATSolver（Hierarchical Attention Transformer for Gröbner bases） |
| Dataset | 13-variable systems, density 90%, F7, density 30%, 6-variable systems, density 33% |

> [!tip] 效果简介
> - 13-variable systems, density 90%, F7 上，Success rate (%) 为 61.2，对比 6.1 (STD-FGLM)，变化 +55.1%。
> - 13-variable systems, density 90%, F7 上，Runtime (s) 为 292，对比 1129 (STD-FGLM)，变化 -837s。
> - 13-variable systems, density 30%, F7 上，Success rate (%) 为 52.5，对比 33.5 (STD-FGLM)，变化 +19%。

## 概要

Gröbner基是代数几何与符号计算中的核心工具，广泛应用于多项式方程求解、理想成员判定和代数系统化简。然而，经典算法（如Buchberger算法、Faugère的F4/F5算法）在最坏情形下具有双指数复杂度，且高度依赖专家设计的启发式策略，难以扩展到大规模多元多项式系统。近年来，基于Transformer的深度学习方法尝试从数据中学习Gröbner基的预测模式，但标准Transformer的扁平自注意力机制在处理多元多项式系统时，序列长度随变量数和次数急剧增长，导致二次复杂度的计算与内存瓶颈，限制了可求解系统的规模。

HATSolver（Hierarchical Attention Transformer for Gröbner bases）针对上述扩展性瓶颈，提出了一种树状分层注意力变换器架构。其核心洞察在于：多项式系统天然具有“系统→方程→项→符号”的树形层次结构，将注意力限定在局部层内和父子节点之间的交叉注意力，既能保留长程依赖，又将计算复杂度从 $O(L^2d)$ 降至 $O(L^{1+1/n}d)$，从而突破了标准Transformer的扩展性限制。此外，HATSolver引入课程学习策略，在训练过程中逐步提升样本难度，进一步提升了模型在更大规模系统上的收敛性和泛化能力。

实验结果表明，HATSolver在有限域 $\mathbb{F}_7$ 上成功计算了多达 **13个变量、最高次数11** 的多项式系统Gröbner基，远超此前基于Transformer的方法（**Kera et al., NeurIPS 2024**）。在13变量、90%密度的系统上，HATSolver-3的完全匹配准确率达到 **61.2%**，而经典符号计算算法STD-FGLM仅 **6.1%**，Msolve仅 **4.5%**；推理时间也从STD-FGLM的1129秒缩短至 **292秒**（Table 1）。在相同训练时间预算下，HATSolver-2和-3相比基线Transformer收敛更快、准确率更高（Figure 2）。消融实验进一步表明，课程学习是关键组件——去除后13变量90%密度下的准确率从61.2%骤降至33.85%，但仍优于经典算法（Table 2 vs Table 1）。

需要指出的是，当前方法仅在形状位置理想和有限域上验证，训练数据由特定的后向生成算法构造，其分布可能与真实多项式系统存在偏差，分布外泛化性能有待进一步检验。

### 多项式系统求解与Gröbner基

多元多项式系统的求解是计算代数几何的核心问题，在密码学、机器人运动规划、化学反应网络分析等领域有广泛应用。给定理想 $I \subseteq k[x_1, \ldots, x_n]$，其**Gröbner基**是一组具有良好消元性质的多项式生成元，使得理想成员判定、方程求解等问题变得可计算。然而，Gröbner基的计算复杂度极高——在最坏情况下，其计算复杂度是**双指数级**的，这严重限制了经典符号算法（如F4/F5、FGLM）在大规模系统上的可扩展性。

### 现有方法及其瓶颈

经典符号计算方法主要分为两类路径：
- **直接计算lex顺序Gröbner基**：如**Msolve**（Berthomieu et al., 2021），在高变量数下常因中间表达式膨胀而超时。
- **两阶段策略（STD-FGLM）**：先计算grevlex顺序的Gröbner基，再通过FGLM算法转换为lex顺序。该方法在13变量、90%密度系统上仅达6.1%成功率，且大量实例在2小时时限内失败（Table 1）。

近年来，**Kera et al.（NeurIPS 2024）**首次将Transformer引入Gröbner基预测，将问题建模为序列到序列的生成任务。然而，该方法受限于标准Transformer的**扁平自注意力机制**：当多项式系统的变量数 $n$ 和次数增大时，token序列长度急剧增长，注意力计算的二次复杂度 $O(L^2 d)$ 导致显存和计算时间迅速膨胀。实验表明，该基线模型在 $n=10$ 时准确率始终为0%（Figure 5），在 $n=7$、密度0.25时同样完全失败（Figure 4）。

### 核心瓶颈与本文动机

上述扩展性瓶颈的根源在于：标准Transformer将多项式系统视为扁平的token序列，忽略了其天然的**树形层次结构**。一个多项式系统天然呈现“系统→方程→项→符号”的层级组织——同一项内的符号之间、同一方程内的项之间、同一系统内的方程之间，其交互强度和信息密度存在本质差异。全局注意力不加区分地计算所有token对之间的交互，既浪费了大量计算资源，又引入了噪声。

本文的核心动机正是利用这一层次结构先验，设计一种**计算高效的层次化注意力机制**，在保留必要长程依赖的前提下，将注意力限定在局部和父子节点之间，从而突破标准Transformer的扩展性瓶颈。同时，辅以**课程学习策略**逐步提升训练难度，使模型能够稳定地学习更大规模系统的Gröbner基计算模式。

## 核心方法与创新机理

HATSolver的核心创新在于将标准Transformer的扁平自注意力替换为**树状分层注意力机制**，以突破多元多项式系统Gröbner基预测的扩展性瓶颈。这一设计源于一个关键洞察：多项式系统天然具有“系统→方程→项→符号”的树形层次结构，将注意力限定在局部和父子节点之间，既能保留长程依赖，又能将计算复杂度从扁平注意力的 $O(L^2 d)$ 降至 $O(L^{1+1/n} d)$。

具体而言，HATSolver在以下四个关键槽位上对基线模型（**Kera et al., NeurIPS 2024** 的标准Transformer）进行了系统性改造：

### 1. 注意力机制：从全局自注意力到分层双向注意力
基线模型在所有token之间执行全局自注意力，序列长度 $L$ 随变量数和次数急剧膨胀，导致二次复杂度瓶颈。HATSolver将注意力操作分解为两个连续阶段（Section 3.2）：

- **自下而上局部自注意力**：从叶节点（符号级）开始，在每一层级内部执行局部自注意力，随后通过池化聚合为父节点表示，逐层向上传递。第 $i$ 层的自注意力计算为：
  $$\pmb{\mathsf{Y}}^{(i)} = \mathsf{Att}(\pmb{\mathsf{X}}^{(i)} \pmb{W}_q^{(i)}, \pmb{\mathsf{X}}^{(i)} \pmb{W}_k^{(i)}, \pmb{\mathsf{X}}^{(i)} \pmb{W}_v^{(i)})$$
  其中注意力仅在每层的局部组内计算，而非跨所有token。

- **自上而下交叉注意力**：在自下而上完成后，从根节点向叶节点反向传播信息。父节点表示 $\mathbf{Z}^{(i+1)}$ 通过交叉注意力精炼子节点表示 $\mathbf{Y}^{(i)}$：
  $$\mathbf{Z}^{(i)} = \mathbf{Y}^{(i)} + \mathrm{Att}(\mathbf{Y}^{(i)}, \mathbf{Z}^{(i+1)} U_k^{(i)}, \mathbf{Z}^{(i+1)} U_v^{(i)})$$
  这一自上而下的交叉注意力阶段是标准层次模型（如Hi-Transformer）所不具备的（Section 5），它使得高层系统级信息能够显式地指导低层符号级表示的更新。

复杂度分析（Section 3.3）表明，分层注意力的总计算量为：
$$C = 3 L_0 d_{-1} d_0 + \sum_{i=1}^{n-1} 5 L_i d_{i-1} d_i + \sum_{i=0}^{n-1} 2 L_i d_i (\ell_i + \ell_{i+1})$$
通过合理选择各层嵌入维度 $d_i$，可控制复杂度由投影或注意力主导，从而在参数量与计算效率之间取得平衡。

### 2. 训练策略：课程学习替代均匀采样
基线模型从固定分布中均匀采样训练数据，难以扩展到更大规模系统。HATSolver引入**课程学习策略**（Section 1.1, Appendix B），通过高斯采样调度器在训练过程中渐进式提高样本难度。训练步 $t$ 抽取数据集 $i$ 的概率为：
$$p(t,i) = \frac{\exp\left(-\frac{(i-\mu(t))^2}{2\sigma^2}\right)}{\sum_{j=0}^{n-1}\exp\left(-\frac{(j-\mu(t))^2}{2\sigma^2}\right)}$$
其中课程重心 $\mu(t) = v \cdot \lfloor t / \text{steps per epoch} \rfloor$ 随训练线性移动。这一策略使得模型能够先掌握简单系统，再逐步泛化到高变量、高密度的困难实例。

消融实验（Table 2 vs Table 1）证实了课程学习的关键作用：去除课程学习后，HATSolver-3在13变量90%密度上的完全匹配准确率从61.2%骤降至33.85%，降幅达27.35个百分点，但仍显著优于经典算法STD-FGLM的6.1%。

### 3. 位置编码：从1D到多维可学习嵌入
基线模型使用标准的一维正弦或可学习位置编码，无法有效表达多项式系统的多维树状结构。HATSolver采用**多维可学习位置嵌入**（Section 3.5），将位置编码分解为各轴嵌入之和：
$$\mathrm{PE}(i_{n-1}, \ldots, i_0) = \sum_{j=0}^{n-1} E_{i_j}^{(j)}$$
其中 $E^{(j)}$ 是第 $j$ 个层次轴的可学习嵌入矩阵。这种设计使模型能够区分同一符号在不同方程、不同项中的位置角色。

### 4. 层次深度配置：HATSolver-2与HATSolver-3
HATSolver提供两种层次深度配置（Section 4.1）：
- **HATSolver-2**：两层结构，level 0在项内token间进行注意力，level 1跨所有方程的所有项聚合。
- **HATSolver-3**：三层结构，level 0处理项内token，level 1在多项式内跨项聚合，level 2跨整个方程系统聚合。

实验表明（Figure 2），在相同训练时间（52小时，8×V100 GPU）内，HATSolver-2和HATSolver-3均比基线Transformer收敛更快、准确率更高。在更大规模系统上（Figure 5），基线Transformer在n=10时准确率为0%，而HATSolver-3达到8%，验证了分层注意力在扩展性上的决定性优势。

---

**证据强度说明**：以上创新点的核心证据（Figure 2, Table 1, Table 2, Figure 5）置信度均在0.9以上，因果关系明确。课程学习消融实验提供了直接的因果证据。复杂度分析的理论推导与实验观察一致，但更深层次（n>3）的扩展行为尚未验证，需进一步探索。

HATSolver 的整体流水线由五个核心模块串联构成，围绕“后向数据生成→层次化编码→自回归解码→课程调度”这一闭环展开，目标是在给定多元多项式系统后直接预测其约化Gröbner基。

**数据生成模块**采用后向生成策略（Kera et al., NeurIPS 2024），从随机采样的Gröbner基出发，通过可逆变换构造对应的非Gröbner基多项式系统，形成有监督训练对 $(F, G)$。这一反向构造保证了每个训练样本都有精确的Ground Truth标签，但同时也引入了分布偏差——生成系统的统计特性可能与真实多项式系统不同，构成泛化能力的潜在瓶颈。

**Tokenization模块**将多项式系统映射为树状token序列。系统被组织为 $n$ 层树结构：叶节点（level 0）对应单个符号token，向上依次聚合成项、多项式，最终到达系统根节点。以二元系统为例（Figure 1），方程 $p_1 = x_0^2 x_1^2 + 5 x_0^2 x_1$ 和 $p_2 = 3 x_0^3 + 2 x_1$ 被展开为系统→方程→项→符号的四层嵌套结构，每层通过填充（padding）保证维度一致。

**层次化编码器（Hierarchical Encoder）**是方法的核心创新，替代了标准Transformer的扁平自注意力。它分两个阶段运行：自下而上阶段从叶节点开始，在每层内部执行局部自注意力，再通过池化将信息向上聚合到父节点；自上而下阶段通过交叉注意力将父节点的全局信息反向传播到子节点，精炼叶节点表示（详见Section 3.2，公式2-5）。这一设计将计算复杂度从标准注意力的 $O(L^2 d)$ 降至 $O(L^{1+1/n} d)$，其中 $L$ 为总token数，$n$ 为树层数，使模型能够扩展到13变量、次数11的系统。

**层次化解码器（Hierarchical Decoder）**基于编码器输出的层次化表示，自回归地生成Gröbner基的token序列。解码过程同样利用树状结构约束注意力范围，与编码器保持对称。

**课程调度器（Curriculum Scheduler）**控制训练过程中样本难度的渐进式提高。具体而言，它维护一个高斯采样分布，其中心 $\mu(t)$ 随训练步数线性移动，使得模型从低变量数、低密度的简单系统逐步过渡到高变量数、高密度的困难系统（详见Appendix B）。消融实验表明，去除课程学习后HATSolver-3在13变量90%密度上的准确率从61.2%骤降至33.85%，但仍优于经典算法（Table 2 vs Table 1），说明层次化架构和课程学习各自贡献显著且可叠加。

整体输入输出流为：多项式系统 $F$ → 树状token序列 → 层次化编码器（含多维位置编码 $\mathrm{PE}(i_{n-1}, \ldots, i_0) = \sum_{j=0}^{n-1} E_{i_j}^{(j)}$）→ 层次化解码器 → Gröbner基token序列。训练时，课程调度器动态选择训练样本的难度分布；推理时，模型直接端到端生成预测结果。

**关键局限**：整个框架目前仅适用于形状位置（shape position）理想和有限域（$\mathbb{F}_7, \mathbb{F}_{16}, \mathbb{F}_{17}$），向一般理想或特征零域的推广尚未验证。此外，后向数据生成引入的分布偏差可能导致模型在真实多项式系统上的分布外性能下降，这一点需要在实际部署时手动评估。

HATSolver的核心创新在于将标准Transformer的全局扁平自注意力替换为**树状分层注意力机制**（Hierarchical Attention），并辅以课程学习策略。以下按模块拆解其设计逻辑。

### 1. 分层注意力机制：自下而上 + 自上而下

多项式系统天然具有“系统→方程→项→符号”的树形层次结构。HATSolver利用这一归纳偏置，将注意力操作限定在局部层级内和父子节点之间，从而将复杂度从标准Transformer的 $O(L^2 d)$ 降至 $O(L^{1+1/n} d)$，突破扩展性瓶颈。

该机制分为两个阶段：

**自下而上阶段（Bottom-up）**：从叶节点（符号级）开始，逐层向上计算局部自注意力并池化。

设输入为 $n$ 层树张量 $\mathbf{X}^{(0)} \in \mathbb{R}^{\ell_{n-1} \times \cdots \times \ell_1 \times \ell_0 \times d}$，其中 $\ell_0$ 为每项的符号数，$\ell_1$ 为每方程项数，依此类推。

- **叶节点局部自注意力**（第0层）：

$$\mathbf{Y}^{(0)} = \mathsf{Att}(\mathbf{X}^{(0)} \mathbf{W}_q^{(0)}, \mathbf{X}^{(0)} \mathbf{W}_k^{(0)}, \mathbf{X}^{(0)} \mathbf{W}_v^{(0)}) \in \mathbb{R}^{\ell_{n-1}\times\cdots\times\ell_1\times\ell_0\times d_0}$$

其中 $\mathbf{W}_{q,k,v}^{(0)} \in \mathbb{R}^{d \times d_0}$ 为可训练投影矩阵。注意力仅在属于同一项的符号之间计算，而非全局所有token。

- **池化生成上层输入**（第 $i$ 层，$i>0$）：

$$\mathbf{X}^{(i)} = p(\mathbf{Y}^{(i-1)}) \in \mathbb{R}^{\ell_{n-1}\times\cdots\times\ell_i\times d_{i-1}}$$

池化函数 $p(\cdot)$ 将下层输出聚合为父节点表示，可选均值池化或取第一个子节点。

- **第 $i$ 层局部自注意力**：

$$\mathbf{Y}^{(i)} = \mathsf{Att}(\mathbf{X}^{(i)} \mathbf{W}_q^{(i)}, \mathbf{X}^{(i)} \mathbf{W}_k^{(i)}, \mathbf{X}^{(i)} \mathbf{W}_v^{(i)}) \in \mathbb{R}^{\ell_{n-1}\times\cdots\times\ell_i\times d_i}$$

注意力仅在属于同一父节点的子节点之间计算（如方程内的项之间、系统内的方程之间）。

**自上而下阶段（Top-down）**：通过交叉注意力将父节点的全局信息回传给子节点，精炼表示。

$$\mathbf{Z}^{(i)} = \mathbf{Y}^{(i)} + \mathsf{Att}(\mathbf{Y}^{(i)}, \mathbf{Z}^{(i+1)} \mathbf{U}_k^{(i)}, \mathbf{Z}^{(i+1)} \mathbf{U}_v^{(i)}) \in \mathbb{R}^{\ell_{n-1}\times\cdots\times\ell_i\times d_i}, \quad \forall i < n-1$$

其中 $\mathbf{U}_k^{(i)}, \mathbf{U}_v^{(i)}$ 为可训练的投影矩阵。子节点 $\mathbf{Y}^{(i)}$ 作为查询，父节点 $\mathbf{Z}^{(i+1)}$ 提供键和值，实现自上而下的信息流动。这一交叉注意力阶段是HATSolver区别于标准层次模型（如Hi-Transformer）的关键设计。

### 2. 复杂度分析

分层注意力的总计算复杂度为各层自下而上与自上而下成本之和：

$$C = 3 L_0 d_{-1} d_0 + \sum_{i=1}^{n-1} 5 L_i d_{i-1} d_i + \sum_{i=0}^{n-1} 2 L_i d_i (\ell_i + \ell_{i+1})$$

其中 $L_i = \prod_{j=i}^{n-1} \ell_j$ 为第 $i$ 层的节点数。通过合理选择各层嵌入维度 $d_i$，可使复杂度由投影操作或注意力机制主导，从而灵活控制计算瓶颈。与标准Transformer的 $O(L^2 d)$ 相比，分层设计将序列长度 $L$ 拆分为各层局部窗口 $\ell_i$，使复杂度降至亚二次级别。

### 3. 多维位置编码

为保留树状结构中的位置信息，HATSolver采用多维可学习位置嵌入，将各轴的位置嵌入求和：

$$\mathrm{PE}(i_{n-1}, \ldots, i_0) = \sum_{j=0}^{n-1} E_{i_j}^{(j)}$$

其中 $E^{(j)}$ 为第 $j$ 个层次轴的可学习嵌入矩阵，$i_j$ 为该轴上的位置索引。该设计替代了标准Transformer的一维正弦位置编码，适应多维张量输入。

### 4. 课程学习调度器

训练采用高斯采样调度器，在训练步 $t$ 从数据集 $i$ 采样的概率为：

$$p(t,i) = \frac{\exp\left(-\frac{(i-\mu(t))^2}{2\sigma^2}\right)}{\sum_{j=0}^{n-1}\exp\left(-\frac{(j-\mu(t))^2}{2\sigma^2}\right)}$$

其中课程重心 $\mu(t) = v \cdot \lfloor t / \text{steps per epoch} \rfloor$ 随训练线性移动，控制样本难度从简单到困难的渐进式提升。消融实验表明，去除课程学习后，HATSolver-3在13变量90%密度上的完全匹配准确率从61.2%骤降至33.85%，但仍优于经典算法STD-FGLM的6.1%（Table 1 vs Table 2）。

### 5. 整体流水线

HATSolver的完整处理流水线包括：①后向数据生成（构造Gröbner基与非Gröbner基系统的监督训练对）；②树状tokenization（将多项式系统编码为层次化token序列）；③分层编码器（执行上述自下而上+自上而下注意力）；④分层解码器（基于编码器输出自回归生成Gröbner基）；⑤课程调度器（控制训练难度渐进）。其中编码器是核心创新所在，解码器沿用标准Transformer的自回归架构。

## 实验与关键发现

### 核心结果：13变量系统的突破

HATSolver-3在13变量、有限域$\mathbb{F}_7$上的Gröbner基预测任务中，展现出对经典符号计算方法的显著优势。Table 1汇总了核心对比结果：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_5C3LljOEGC/figures/003_Table_1.jpg]]
*Table 1: Performance of HATSolver-3 on computing Grobner bases for polynomial systems ¨ with 13 variables over $\mathbb { F } _ { 7 }$ , across varying system densities with comparison to traditional algorithms STD-FGLM Greuel et al. (2009); Faugere et al. (1993) and ` $\mathtt { M s o l v e }$ Berthomieu et al. (2021). The density (%) indicates the proportion of nonzero terms in the matrix $U _ { 2 }$ in backward generation 2.4, controlling the sparsity of the systems. Success denotes the exact match test accuracy, i.e. the percentage of the test set instances for which the model generated the exact correct Grobner ¨ basis. Support Acc. measures the accuracy when only the support (i.e., the set of monomi...

- **完全匹配准确率**：在密度$\rho=90\%$时，HATSolver-3达到**61.2%**，而**STD-FGLM**（Greuel et al., 2009; Faugère et al., 1993）仅为6.1%，**Msolve**（Berthomieu et al., 2021）仅为4.5%。在$\rho=30\%$的稀疏设置下，HATSolver-3仍以52.5%对33.5%领先STD-FGLM。
- **推理时间**：在$\rho=90\%$时，HATSolver-3的生成阶段耗时**292秒**，而STD-FGLM为1129秒。需注意，该推理时间未进行KV缓存或推理引擎优化，而经典算法在2小时时限后视为失败。
- **支持准确率**：当仅考虑单项式集合（忽略系数）时，HATSolver-3在$\rho=90\%$下达到**94.0%**，表明模型准确捕捉了Gröbner基的项结构，系数预测是主要误差来源。

上述结果的确证强度高（置信度0.95），直接支撑了核心洞察：分层注意力突破了标准Transformer的扩展瓶颈，使模型能够处理此前经典算法也难以应对的大规模系统。

### 训练动态：收敛速度与准确率的双重提升

Figure 2展示了在6变量、$\rho=0.33$、$\mathbb{F}_7$系统上训练52小时（8×V100 GPU）的动态对比。**Kera et al. (2024)基线Transformer**训练30万步后准确率趋于饱和，而**HATSolver-2**和**HATSolver-3**在45万步时仍持续提升，且最终准确率显著更高。这一结果直接验证了方法瓶颈分析：标准Transformer的扁平自注意力在多项式系统规模增长时遭遇二次复杂度瓶颈，而分层注意力通过局部化和跨层交叉注意力，在相同计算预算下实现了更高效的训练。

### 消融实验：课程学习与架构的贡献解耦

为分离分层架构与课程学习的各自贡献，Table 2报告了HATSolver-3在**无课程学习**（仅在$\rho_{\text{train}}=0.9$上训练）时的表现：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_5C3LljOEGC/figures/004_Table_2.jpg]]
*Table 2: To disentangle the contribution of the hierarchical attention architecture from the benefits of curriculum learning, we conducted an ablation study where HATSolver-3 was trained on a single dataset configuration without any staged progression. Specifically, we trained directly on a dataset of size 1 million samples with n = 1 3 variables over the same finite field at density $\rho$ = 0 . 9 Table 2: (Exact Match) Accuracy of HATSolver-3 trained without curriculum on n = 1 3 variables over $\mathbb { F } _ { 7 }$ at $\rho _ { \mathrm { t r a i n } }$ = 0 . 9 evaluated across densities $\rho _ { \mathrm { t e s t } } \in \{$ 0 . 1 , 0 . 2 , $\ldots$ , 1 . 0 $\}$ Each test set contains 1000 systems. Model...

- 在训练密度$\rho=0.9$上，完全匹配准确率从61.2%骤降至**33.85%**。
- 跨密度泛化表现有限：在$\rho=0.1$时仅14.40%，$\rho=1.0$时仅15.53%。

这揭示了一个关键因果机制：**课程学习是HATSolver性能的关键推手**，它通过渐进提高难度使模型逐步学习复杂模式；而分层架构本身已具备优于经典算法的能力——即使无课程学习，33.85%的准确率仍远超STD-FGLM的6.1%。

### 架构消融：宽度优于深度

Figure 3和附录C.1的参数量预算实验表明，在固定计算预算下，**更宽的模型**（如3层/3层编码解码器，嵌入维度1024）比较深的模型（6层/6层，嵌入维度512或8层/8层，嵌入维度512）表现更好。这一发现对分层架构设计具有指导意义：在多项式系统任务中，每层的表示容量（宽度）比层次深度更重要。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_5C3LljOEGC/figures/007_Figure_3.jpg]]
*Figure 3: Training base models with varying embedding dimensions and number of layers for 48 hours on multivariate datasets of n = 3 variables over finite field $\mathbb { F } _ { 7 }$ and density $\rho$ = 0 . 5 Each configuration is run with 3 seeds and the plotted lines are smoothened averages. Hyperparameters: batch size = 3 2 , learning rate = 3 $\cdot$ 1 $0 ^ { - 5 }$ with 1000 warm up steps. Training on 1 $\times$ V 1 0 0 per experiment for 48 hours

### 层次模型对比：HATSolver vs Hi-Transformer

附录C.3将HATSolver与**Hi-Transformer**（Wu et al., 2021，句子/文档双层Transformer）进行了对比。Hi-Transformer在5变量、$\rho=0.67$上可达75%准确率，但在13变量上完全失败，且训练速度远慢于HATSolver-3。这表明：

1. 简单的两层层次结构不足以处理大规模多项式系统的复杂依赖关系。
2. HATSolver的三层树状结构（符号→项→方程→系统）更贴合多项式系统的天然层次。
3. HATSolver的自上而下交叉注意力阶段（式5）是Hi-Transformer所缺失的关键设计。

### 跨域泛化：有限域迁移能力

Table 3和Table 5报告了HATSolver在$\mathbb{F}_7$、$\mathbb{F}_{16}$、$\mathbb{F}_{17}$上的跨域表现。在5变量设置下，模型在各有限域上均取得可用准确率（$\mathbb{F}_7$上$\rho=100\%$时33.63%，$\mathbb{F}_{16}$上24.01%，$\mathbb{F}_{17}$上22.82%）。在7变量设置下，$\mathbb{F}_{17}$上$\rho=100\%$时准确率为5.75%，$\mathbb{F}_{16}$上为5.41%。这表明模型学习到的模式具有一定程度的域迁移能力，但随变量数和密度增加，性能下降明显——这是方法局限性的直接体现。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_5C3LljOEGC/figures/005_Table_3.jpg]]
*Table 3: Exact Match Accuracy (%) of our model on Grobner basis prediction of multivariate poly- ¨ nomial systems with $\mathbf { n }$ = 5 variables across different densities over multiple finite fields. Training is done on 1 A100 GPU per field for 24 hours using the backward data generation method from Kera et al. (2025). Model parameters are 2 encoder layers, 6 decoder layers, 1024 embedding dimensions*

### 基线Transformer的扩展极限

Table 4报告了基线Transformer配合课程学习在2至7变量系统上的表现。在7变量、$\rho=100\%$时，完全匹配准确率仅为**0.0%**（支持准确率2.0%）。Figure 5进一步显示，在10变量、$\rho=0.1$上，基线Transformer准确率始终为0%，而HATSolver-3达到**8%**，且训练步数多3倍以上。这构成了分层注意力优于扁平注意力的最直接证据：当序列长度随变量和密度急剧增长时，标准Transformer的二次复杂度使其完全无法学习，而HATSolver的分层设计将复杂度从$O(L^2 d)$降至$O(L^{1+1/n} d)$，从而在极端规模下仍能捕获有效信号。

### 失败模式与公平性警示

尽管HATSolver取得了显著进展，但以下局限性需在解读结果时审慎考虑：

1. **分布偏差**：训练数据由后向生成算法构造，其分布可能与真实多项式系统不同，导致分布外泛化能力存疑。
2. **域限制**：所有实验均限于形状位置理想和有限域（$\mathbb{F}_7$、$\mathbb{F}_{16}$、$\mathbb{F}_{17}$），推广到一般理想或特征零域尚不明确。
3. **推理公平性**：HATSolver的推理时间未进行优化，与高度优化的经典代数软件（如Msolve）对比可能存在不公平；但即便在此条件下，HATSolver在13变量上仍展现出速度优势。
4. **资源消耗**：模型训练需多GPU长时间计算（如Table 1实验使用特定超参数配置，见Table 12），且超参数搜索空间有限，可能未充分调优。
5. **准确率天花板**：在$\rho=100\%$时完全匹配准确率仅60.8%，对序列偏差敏感，仍有较大提升空间。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_5C3LljOEGC/figures/008_Figure_4.jpg]]
*Figure 4: Training dynamics comparison; training models for 7 2 hours on multivariate datasets of n = 7 variables and density $\rho$ = 0 . 2 5*


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_5C3LljOEGC/figures/014_Table_8.jpg]]
*Table 8: Statistical Comparison of Forward and Backward Generation Datasets for n = 3 over $\mathbb { F } _ { 7 }$*

## 定位与知识库关联

### 与基线模型的关系

HATSolver 直接建立在 **Kera et al. (NeurIPS 2024)** 的 Transformer 基线之上。该基线首次将序列到序列的 Transformer 架构应用于 Gröbner 基预测任务，但受限于标准扁平自注意力的二次复杂度，仅能处理最多 5 变量、密度 0.2 的系统。HATSolver 将基线模型中的标准自注意力层替换为分层注意力层，其余架构组件（编码器-解码器框架、后向数据生成流程、形状位置理想的约束）保持不变。这一替换的本质是将多项式系统天然的树形层次结构（系统→方程→项→符号）显式编码为注意力计算的归纳偏置，从而将计算复杂度从 $O(L^2 d)$ 降至 $O(L^{1+1/n} d)$，突破了基线模型的扩展性瓶颈。

决定性证据来自 Figure 2：在相同训练时间（52 小时，8×V100 GPU）和相同超参数配置下，HATSolver-2 和 HATSolver-3 在 6 变量系统上比基线 Transformer 收敛更快、准确率更高。更关键的是，基线 Transformer 在 10 变量系统上准确率始终为 0%，而 HATSolver-3 达到 8%（Figure 5），表明分层注意力是实现规模扩展的因果性机制。

与另一层次化模型 **Hi-Transformer** (Wu et al., 2021) 的对比进一步凸显 HATSolver 设计的独特性。Hi-Transformer 采用句子/文档双层注意力，在 n=5、ρ=0.67 上可达 75% 准确率，但在 n=13 上完全失败，且训练速度远慢于 HATSolver-3（Appendix C.3）。HATSolver 的两个关键差异化设计是：(1) 自上而下交叉注意力阶段，使父节点信息能回流精炼叶节点表示，这是 Hi-Transformer 所不具备的；(2) 多维可学习位置编码，按轴求和以适配树状张量结构。

### 与经典符号计算算法的关系

HATSolver 的对比对象包括两类经典算法：**STD-FGLM**（Greuel et al., 2009; Faugère et al., 1993），先计算 grevlex 序的 Gröbner 基再用 FGLM 算法转换为 lex 序；以及 **Msolve**（Berthomieu et al., 2021），一个高效的开源 Gröbner 基计算软件。在 13 变量系统上，HATSolver-3 在 90% 密度下的完全匹配准确率达 61.2%，而 STD-FGLM 仅 6.1%，Msolve 仅 4.5%（Table 1）。推理时间方面，HATSolver-3 为 292 秒，STD-FGLM 为 1129 秒，且经典算法在 2 小时时限内超时率高达 93.5%（全密度样本）。

然而，这一对比存在公平性方面的注意事项：HATSolver 的推理时间未进行 KV 缓存或推理引擎优化，而 STD-FGLM 和 Msolve 是高度优化的代数软件。此外，HATSolver 的离线训练需消耗大量 GPU 资源，无法像经典算法那样动态集成代数知识。

### 适用边界与局限

HATSolver 的适用边界由以下约束定义：

1. **理想类型限制**：模型仅在形状位置（shape position）理想上训练和验证。推广到一般理想需要不同的数据生成策略和架构适配，目前尚不明确。

2. **有限域限制**：所有实验均在有限域 $\mathbb{F}_7$、$\mathbb{F}_{16}$、$\mathbb{F}_{17}$ 上进行。跨域泛化实验（Table 3, Table 5）显示模型在不同有限域上可取得可比性能，但扩展到特征零域（如 $\mathbb{Q}$ 或 $\mathbb{R}$）面临系数表示和训练数据生成的本质困难。

3. **训练数据分布偏差**：后向生成算法构造的训练数据分布可能偏离真实多项式系统。当训练密度为 0.9 时，模型在低密度测试集上的准确率显著下降（Table 2），表明分布偏移会严重影响性能。这种分布敏感性暗示模型可能更多拟合了数据生成的统计表面特征，而非真正学习 Buchberger 算法的核心步骤。

4. **完全匹配准确率的天花板**：即使在最优配置下，13 变量 100% 密度的完全匹配准确率仅为 60.8%（Table 1），支持准确率可达 94%。这表明模型在系数预测上仍有较大提升空间，且对序列偏差高度敏感——一个 token 错误即导致完全匹配失败。

5. **架构深度固定**：分层架构的深度固定为 2 或 3 层，未探索更深层次对更复杂系统的影响。更深的层次可能进一步降低复杂度，但训练稳定性未知。

### 开放问题

1. **学习机制的本质**：模型学习到的模式是真正捕捉了 Buchberger 算法中 S-多项式的构造与约化步骤，还是仅拟合了训练数据的统计表面特征？这需要通过对注意力权重的可解释性分析或对中间表示与代数不变量（如首项理想）的关联研究来回答。

2. **更深层次架构的可行性**：分层注意力能否在更多层次（如引入单项式序的层次）下保持稳定训练，并继续降低复杂度？这涉及梯度传播和表示瓶颈的权衡。

3. **域泛化的根本性突破**：能否将训练扩展到特征零域或更一般的理想上？可能需要将符号计算的知识（如系数环的代数结构）显式编码到模型架构中。

4. **混合系统的潜力**：是否可以将 HATSolver 与经典代数软件混合使用，例如用 HATSolver 快速生成候选 Gröbner 基，再用 STD-FGLM 进行验证和后处理？这种混合策略可能结合学习方法的效率和符号计算的正确性保证。

5. **数据生成策略的鲁棒性**：不同的采样分布（如改变后向生成中矩阵 $U_2$ 的稀疏模式）会对模型的泛化能力和鲁棒性产生多大影响？这直接关系到模型在真实代数几何问题上的实用性。

## 原文 PDF

![[paperPDFs/ICLR_2026/HATSolver_Learning_Gröbner_Bases_with_Hierarchical_Attention_Transformers.pdf]]

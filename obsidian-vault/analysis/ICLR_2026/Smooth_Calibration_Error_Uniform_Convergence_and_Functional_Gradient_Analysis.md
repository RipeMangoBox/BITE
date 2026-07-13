---
title: "Smooth Calibration Error: Uniform Convergence and Functional Gradient Analysis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Smooth_Calibration_Error_Uniform_Convergence_and_Functional_Gradient_Analysis.pdf
project_link: null
code_link: null
openreview_forum_id: qXVmmj8J0T
aliases:
- SCEUCFGA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "控制函数梯度范数和模型复杂度，以减小平滑校准误差。"
primary_logic: "首先建立平滑校准误差的一致收敛界，将总体平滑CE分解为训练平滑CE与泛化间隙；其次证明训练平滑CE可由损失函数关于预测的函数梯度的L1范数控制，从而为梯度提升树、核提升和两层神经网络提供了统一的校准理论保证。"
claims:
- "平滑CE的一致收敛界：总体平滑CE ≤ 训练平滑CE + 泛化间隙（覆盖数/Rademacher复杂度）。"
- "训练平滑CE可由函数梯度的L1范数上界控制：smCE^σ(g, S_tr) ≤ (1/n) Σ|∇_g ℓ_ent(g(X_i), Y_i)|。"
- "梯度提升树（梯度提升树）的训练平滑CE在固定步长下以O(1/√T)收敛。"
- "组合优化界与泛化界可同时保证平滑CE和误分类率小于任意ε。"
---

# Smooth Calibration Error: Uniform Convergence and Functional Gradient Analysis

> [!tip] 核心洞察
> 首先建立平滑校准误差的一致收敛界，将总体平滑CE分解为训练平滑CE与泛化间隙；其次证明训练平滑CE可由损失函数关于预测的函数梯度的L1范数控制，从而为梯度提升树、核提升和两层神经网络提供了统一的校准理论保证。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 平滑校准误差：一致收敛与函数梯度分析 |
| 英文题名 | Smooth Calibration Error: Uniform Convergence and Functional Gradient Analysis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qXVmmj8J0T) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | 平滑校准误差的一致收敛与函数梯度分析框架 |
| Dataset | Toy dataset (Eq. (34)) / UCI Breast Cancer, Difficult separability toy data (Eq. (35)) |

> [!tip] 效果简介
> - Toy dataset (Eq. (34)) / UCI Breast Cancer 上，Smooth CE on training and test sets 为 训练平滑CE随迭代数T增加而下降，测试平滑CE随训练样本量n增加而下降，对比 无直接对照算法，展示分析框架预测的行为趋势，变化 趋势一致（定性验证）。
> - Toy dataset (Eq. (34)) / UCI Breast Cancer 上，Functional gradient norm (L1/L2) 为 训练函数梯度范数随迭代数T单调递减，与理论界一致，对比 无直接对照，变化 单调递减。
> - Difficult separability toy data (Eq. (35)) 上，Test Smooth CE 为 即使分离性较弱，测试平滑CE仍随n增加而单调下降，对比 无直接对照，变化 单调递减。

## 概要

现代学习算法在高精度预测方面取得了显著进展，但在有限样本下能否同时实现良好的校准（calibration）性能，仍缺乏系统的理论保证。校准误差衡量模型预测概率与真实条件概率之间的偏离程度，对于医疗诊断、金融风控等风险敏感应用至关重要。现有校准误差度量（如分箱ECE、MMCE）往往缺乏一致收敛性质，难以建立从训练到测试的泛化理论。

本文的核心贡献是**建立平滑校准误差（Smooth CE）的一致收敛与函数梯度分析框架**，为梯度提升树、核提升和两层神经网络三类主流算法提供了统一的校准理论保证。具体而言，该框架包含两个关键环节：

1. **一致收敛界**：证明总体平滑CE可由训练平滑CE加上一个仅依赖函数类覆盖数（或Rademacher复杂度）的泛化间隙所控制（Theorem 1, Theorem 2）。该界不涉及Lipschitz复合函数类的复杂度，具有较好的紧致性。

2. **函数梯度控制**：证明训练平滑CE被损失函数关于预测的函数梯度的L1范数所上界：$\mathrm{smCE}^{\sigma}(g, S_{\mathrm{tr}}) \leq \frac{1}{n} \sum_{i=1}^{n} |\nabla_g \ell_{\mathrm{ent}}(g(X_i), Y_i)|$（Eq. 5）。这意味着通过优化算法减小函数梯度范数，即可间接最小化训练校准误差。

将上述两部分结合，本文为三种算法推导出**校准误差与分类误差的同时保证**：梯度提升树在固定步长下训练平滑CE以$O(1/\sqrt{T})$收敛（Theorem 3），组合优化界与泛化界后可达到任意精度（Corollary 3）；核提升和两层神经网络也获得了类似的理论保证（Corollary 4, Corollary 5）。

实验在合成数据集和UCI乳腺癌数据集上验证了理论预测的趋势：训练平滑CE随迭代次数$T$增加而下降，测试平滑CE随训练样本量$n$增加而单调递减，函数梯度范数单调减小。值得注意的是，过浅树（$m<d$）与较深树（$m \geq d$）的校准行为相似，而两层神经网络中增加隐藏单元数并未改善测试校准。

该框架的主要局限在于依赖较强的边际假设（Assumption 2, 3），且当前分析仅限于二分类任务和固定步长优化。如何扩展到多分类校准、更弱的假设条件以及更一般的优化算法，是重要的开放问题。



现代机器学习模型在分类准确率上取得了显著进展，但高准确率并不自动保证良好的概率校准——即模型输出的预测概率与真实标签的条件期望一致。校准误差在医疗诊断、自动驾驶、金融风控等高风险决策场景中尤为关键：一个准确但校准不良的模型可能给出系统性偏差的置信度估计，导致决策失误。

校准评估长期面临一个根本性困境：经典的**分箱期望校准误差（Binning ECE）**虽然直观且广泛使用，但缺乏一致收敛的理论保证。具体而言，Binning ECE依赖于将预测概率离散化为固定区间，这一离散化操作使得训练集上的Binning ECE无法通过标准统计学习理论控制总体Binning ECE。更严重的是，已有工作证明，存在简单的分布和预测器，使得Binning ECE的训练-测试泛化间隙无法一致收敛，这意味着基于Binning ECE的校准分析在有限样本下缺乏可靠的理论根基。

**平滑校准误差（Smooth CE）**的提出为这一困境提供了突破口。与Binning ECE不同，Smooth CE定义在所有1-Lipschitz函数上取上确界，避免了离散化带来的理论障碍：

$$
\operatorname{smCE}(f, \mathcal{D}) := \sup_{h \in \operatorname{Lip}_1([0,1],[-1,1])} \mathbb{E}[h(f(X)) \cdot (Y - f(X))]
$$

Błasiok等人（2023）证明，Smooth CE同时给出了Binning ECE的上界和下界，使其成为理论上合理的校准代理。然而，尽管Smooth CE在度量层面解决了理论一致性问题，一个核心瓶颈仍然存在：**现代学习算法缺乏有限样本下校准性能的理论保证，难以同时实现高精度和良好校准**。

具体来说，现有工作存在三个关键缺口：

1. **缺乏一致收敛分析**：虽然Smooth CE的定义规避了离散化问题，但尚未建立其训练-测试泛化间隙的一致收敛界。这导致无法从训练集上的Smooth CE推断总体校准性能。

2. **缺乏训练过程的校准控制**：即使建立了泛化界，还需要理解训练算法本身如何影响Smooth CE。现有校准方法（如温度缩放、直方图分箱）多为后处理技术，无法在训练过程中主动控制校准误差。

3. **缺乏统一的算法分析框架**：梯度提升树、核提升、神经网络等主流学习算法在校准行为上表现各异，但缺乏统一的理论语言来解释和预测其校准性能。

本文的核心洞察在于：**通过建立Smooth CE的一致收敛界，并将训练Smooth CE与损失函数的函数梯度范数联系起来，可以为多种学习算法提供统一的校准理论保证**。具体而言，本文首先证明总体Smooth CE可被分解为训练Smooth CE与泛化间隙之和；其次发现训练Smooth CE可由交叉熵损失关于预测的函数梯度的L1范数所控制：

$$
\mathrm{smCE}^{\sigma}(g, S_{\mathrm{tr}}) \leq \frac{1}{n} \sum_{i=1}^{n} |\nabla_g \ell_{\mathrm{ent}}(g(X_i), Y_i)|
$$

这一关系将校准误差转化为一个可在训练过程中直接监控和优化的量。基于此框架，本文对梯度提升树、核提升和两层神经网络分别推导了校准与分类误差的同时保证，为理解这些算法的校准行为提供了统一的理论基础。



## 核心方法与创新机理

本文的核心创新在于为**平滑校准误差（smooth CE）**建立了首个统一的有限样本理论保证框架。该框架将校准分析分解为两个可独立控制的模块，从而为梯度提升树、核提升和两层神经网络等广泛使用的学习算法同时提供分类精度和校准性能的理论保证。

### 创新一：平滑校准误差的一致收敛界

现有校准理论的一个根本瓶颈是缺乏有限样本下的泛化保证。本文首先建立了平滑CE的**训练-测试一致收敛界**，将总体平滑CE分解为训练平滑CE与泛化间隙之和。

具体而言，对于任意函数类 $\mathcal{F}$，平滑CE的训练-测试间隙满足以下覆盖数界（Theorem 1）：

$$
\sup_{f \in \mathcal{F}} |\operatorname{smCE}(f, S_{\mathrm{te}}) - \operatorname{smCE}(f, S_{\mathrm{tr}})| \leq \inf_{\epsilon \ge 0} 8\epsilon + 24 \int_{\epsilon}^{1} \sqrt{\frac{\ln N(\epsilon', \mathcal{F}, \|\cdot\|_{\infty})}{n}} d\epsilon' + 2 \sqrt{\frac{\log \delta^{-1}}{n}}
$$

该界的关键优势在于**仅依赖函数类本身的覆盖数**，而不涉及Lipschitz复合函数类的复杂度，这显著降低了对模型容量的要求。同时，本文还给出了基于Rademacher复杂度的等价形式（Theorem 2），为不同模型类提供了灵活的分析工具。

### 创新二：函数梯度范数作为校准代理

本文的第二个核心发现是：**训练平滑CE可以被损失函数关于预测的函数梯度的L1范数所控制**（Section 4, Eq. (5)）：

$$
\mathrm{smCE}^{\sigma}(g, S_{\mathrm{tr}}) \leq \frac{1}{n} \sum_{i=1}^{n} |\nabla_g \ell_{\mathrm{ent}}(g(X_i), Y_i)|
$$

这一关系将校准误差直接与优化过程的**函数梯度范数**联系起来，使得校准性能可以通过监控和约束梯度范数来间接控制。这是本文区别于现有工作的关键changed slot：传统方法通常仅最小化经验损失，缺乏对校准的直接控制机制；而本文显式地利用函数梯度范数作为校准代理，结合模型复杂度控制（覆盖数/Rademacher复杂度）共同约束平滑CE。

### 创新三：统一的三类算法校准保证

基于上述两个模块，本文为三类学习算法推导了**校准与误分类率的同时保证**：

- **梯度提升树**（Theorem 3, Corollary 3）：在固定步长和边际假设下，训练平滑CE以 $O(1/\sqrt{T})$ 收敛；结合泛化界后，总体平滑CE上界为 $O(1/T + 1/\sqrt{n} + wT\sqrt{2^m \log n d / n})$，通过合理选择迭代轮数 $T$ 和步长 $w$ 可达到任意精度。

- **核提升**（Corollary 4）：在RKHS中近似函数梯度，训练平滑CE界为 $O(1/\sqrt{wT})$，总体界同样可通过超参数控制达到任意小。

- **两层神经网络**（Corollary 5）：在神经正切核（NTK）机制下，函数梯度范数的平方平均以 $O(1/T)$ 衰减，从而保证平滑CE和误分类率同时收敛。

### 创新四：校准与精度的统一理论

本文首次证明：**能够控制函数梯度范数的算法，可以同时实现小的平滑CE和小的误分类率**。这一结论将校准理论与优化理论深度耦合，为设计同时兼顾精度和校准的学习算法提供了理论指导。与现有工作仅关注校准误差的度量或后处理方法不同，本文从训练动态的角度揭示了校准性能的内在驱动机制。



本文提出一个两阶段分析框架，为平滑校准误差（Smooth Calibration Error, smCE）提供有限样本下的理论保证。核心思路是：**首先建立平滑CE的一致收敛界，将总体误差分解为训练平滑CE与泛化间隙；然后证明训练平滑CE可由损失函数关于预测的函数梯度的L1范数控制**，从而将校准优化问题转化为函数梯度范数的最小化问题。

### 模块一：一致收敛分析

该模块的目标是建立平滑CE的训练-测试泛化界。关键结果包括：

- **覆盖数版本**（Theorem 1）：对任意函数类 $\mathcal{F}$，训练集与测试集上平滑CE的差异被一致收敛界控制，该界仅依赖函数类的覆盖数 $\ln N(\epsilon, \mathcal{F}, \|\cdot\|_\infty)$，而**不涉及Lipschitz复合类的额外复杂度**——这是该框架的关键技术优势。

- **Rademacher版本**（Theorem 2）：用函数类的Rademacher复杂度 $\Re_{\mathcal{D},n}(\mathcal{F})$ 表达总体平滑CE界，第一项 $C_2/\sqrt{n}$ 反映Lipschitz函数类的固有复杂度。

总体平滑CE的分解形式为：
$$\text{总体 smCE} \leq \text{训练 smCE} + \text{泛化间隙（覆盖数/Rademacher复杂度）}$$

### 模块二：函数梯度控制

该模块证明训练平滑CE可由函数梯度的L1范数上界控制。核心不等式为：
$$\mathrm{smCE}^{\sigma}(g, S_{\mathrm{tr}}) \leq \frac{1}{n} \sum_{i=1}^{n} |\nabla_g \ell_{\mathrm{ent}}(g(X_i), Y_i)|$$

这一关系建立在平滑CE与后处理间隙（post-processing gap）的对偶联系之上：平滑CE的平方与后处理间隙相互上下界（Eq. (1)），而函数梯度范数恰好刻画了损失函数沿最陡下降方向的可改进量。

### 模块三：算法实例化分析

将上述框架应用于三类学习算法，分别推导校准与分类误差的同时保证：

| 算法 | 核心机制 | 训练平滑CE界 | 总体保证 |
|------|---------|-------------|---------|
| 梯度提升树（GBT） | 迭代近似函数梯度 $g^{(t+1)} = g^{(t)} - w_t \psi_t$ | $O(1/\sqrt{T})$ 收敛（Theorem 3） | Corollary 3：可同时使平滑CE和误分类率小于任意 $\varepsilon$ |
| 核提升（Kernel Boosting） | 在RKHS中近似函数梯度 | $\frac{1}{\gamma}\sqrt{\frac{L_n(g^{(0)})}{wT}}$（Section 4.2） | Corollary 4：类似保证 |
| 两层神经网络 | 梯度下降进行函数空间优化 | 平均梯度范数平方以 $O(1/T)$ 衰减（Section 4.3） | Corollary 5：类似保证 |

### 输入-输出流

1. **输入**：训练数据 $S_{\mathrm{tr}}$、函数类 $\mathcal{F}$（由算法和超参数决定）、损失函数（交叉熵）
2. **一致收敛模块**：给定 $\mathcal{F}$ 的复杂度度量（覆盖数或Rademacher复杂度），输出泛化间隙上界
3. **函数梯度模块**：在训练过程中监控 $\nabla_g \ell_{\mathrm{ent}}$ 的L1范数，输出训练平滑CE的上界
4. **组合**：将两模块的界相加，得到总体平滑CE的高概率保证
5. **输出**：对给定置信度 $\delta$，平滑CE和误分类率的联合上界

### 关键假设与局限性

框架依赖较强的边际假设（Assumption 2, 3），即存在 $\gamma > 0$ 使得 $|f(X) - Y| \geq \gamma$ 几乎处处成立。该假设并非对所有实际数据都成立，限制了理论在弱分离场景下的适用性。此外，核提升的RKHS范数分析目前仅对极少数核（如Laplace核）严格成立，因为需要RKHS对Lipschitz复合封闭。



本工作的理论框架由两个核心模块构成：**一致收敛分析**与**函数梯度控制**。前者将总体平滑校准误差分解为训练平滑CE与泛化间隙；后者证明训练平滑CE可由损失函数的函数梯度范数上界，从而为各类学习算法提供统一的校准保证。

### 模块一：平滑CE的一致收敛界

该模块的目标是建立平滑校准误差从训练集到总体分布的泛化保证。核心策略是：不直接对复合函数类（Lipschitz函数与预测函数的复合）求复杂度，而是利用平滑CE的定义结构，将泛化间隙仅与预测函数类 $\mathcal{F}$ 的复杂度挂钩。

**经验平滑CE**定义为在训练集 $S_n$ 上对所有1-Lipschitz函数取上确界：

$$\operatorname{smCE}(f, S_n) := \sup_{h \in \operatorname{Lip}_1([0,1],[-1,1])} \frac{1}{n} \sum_{i=1}^{n} h(f(X_i)) \cdot (Y_i - f(X_i))$$

**覆盖数版本的一致收敛界**（Theorem 1）：对任意函数类 $\mathcal{F}$，以高概率成立

$$\sup_{f \in \mathcal{F}} |\operatorname{smCE}(f, S_{\mathrm{te}}) - \operatorname{smCE}(f, S_{\mathrm{tr}})| \leq \inf_{\epsilon \ge 0} \left\{ 8\epsilon + 24 \int_{\epsilon}^{1} \sqrt{\frac{\ln N(\epsilon', \mathcal{F}, \|\cdot\|_{\infty})}{n}} d\epsilon' \right\} + 2\sqrt{\frac{\log \delta^{-1}}{n}}$$

其中 $N(\epsilon', \mathcal{F}, \|\cdot\|_{\infty})$ 是 $\mathcal{F}$ 在无穷范数下的覆盖数。该界的核心洞察是：积分项仅依赖 $\mathcal{F}$ 自身的覆盖数，不涉及Lipschitz复合类的覆盖数膨胀，这使得界在实际模型中可计算。

**Rademacher复杂度版本**（Theorem 2）给出总体平滑CE的界：

$$\sup_{f \in \mathcal{F}} |\operatorname{smCE}(f, \mathcal{D}) - \operatorname{smCE}(f, S_{\mathrm{tr}})| \leq \frac{C_2}{\sqrt{n}} + 4 \Re_{\mathcal{D}, n}(\mathcal{F}) + 2\sqrt{\frac{\log(2/\delta)}{n}}$$

其中 $\Re_{\mathcal{D}, n}(\mathcal{F})$ 是 $\mathcal{F}$ 的Rademacher复杂度，$C_2$ 是反映Lipschitz函数类复杂度的常数。该界将总体平滑CE分解为训练平滑CE与两个泛化项之和。

### 模块二：函数梯度控制训练平滑CE

该模块的核心发现是：训练平滑CE可以被损失函数关于预测的函数梯度的 $L_1$ 范数所上界。这为校准优化提供了可直接操作的代理指标。

**核心不等式**（Section 4, Eq. (5)）：对logit函数 $g$ 定义的dual平滑CE，有

$$\operatorname{smCE}^{\sigma}(g, S_{\mathrm{tr}}) \leq \frac{1}{n} \sum_{i=1}^{n} |\nabla_g \ell_{\mathrm{ent}}(g(X_i), Y_i)|$$

其中 $\nabla_g \ell_{\mathrm{ent}}(g(X_i), Y_i)$ 是交叉熵损失对logit的函数梯度在样本点 $X_i$ 处的取值。该不等式将校准误差与优化过程直接关联：**算法在每次迭代中减小函数梯度范数，等价于减小训练平滑CE**。

这一关系通过**后处理间隙**（post-processing gap）建立桥梁。在平方损失下，平滑CE与后处理间隙满足：

$$\operatorname{smCE}(f, \mathcal{D})^2 \leq \operatorname{pGap}(f, \mathcal{D}) \leq 2\operatorname{smCE}(f, \mathcal{D})$$

后处理间隙度量了当前预测函数与最优1-Lipschitz后处理函数之间的损失差距，而函数梯度正是该间隙在优化动态中的体现。

### 模块三：算法实例化分析

将上述两模块组合，可对三类学习算法同时给出平滑CE和误分类率的保证。

**梯度提升树**（Section 4.1）：更新规则为 $g^{(t+1)}(x) = g^{(t)}(x) - w_t \psi_t(x)$，其中 $\psi_t$ 近似函数梯度。在边际假设（Assumption 2）下，训练平滑CE以 $O(1/T)$ 衰减：

$$\operatorname{smCE}^{\sigma}(\bar{g}^{(T)}, S_n) \leq \frac{L_n(g^{(0)})}{\gamma B w T} + \frac{w B}{8 \gamma}$$

结合泛化界得到总体平滑CE的完整上界（Corollary 2），其中包含训练项 $O(1/T)$、模型复杂度项 $O(w T \sqrt{2^m \log n d / n})$ 和基础泛化项 $O(1/\sqrt{n})$。通过选择合适的迭代数 $T$ 和步长 $w$，可使平滑CE和误分类率同时小于任意 $\varepsilon$（Corollary 3）。

**核提升**（Section 4.2）：在再生核Hilbert空间中，函数梯度近似为 $\mathcal{T}_k \nabla_g L_n(g) / \|\mathcal{T}_k \nabla_g L_n(g)\|_{\mathcal{H}}$，其中 $\mathcal{T}_k$ 是经验核算子。训练平滑CE的界为：

$$\operatorname{smCE}^{\sigma}(\bar{g}^{(T)}, S_{\mathrm{tr}}) \leq \frac{1}{\gamma} \sqrt{\frac{L_n(g^{(0)})}{w T}}$$

该界以 $O(1/\sqrt{T})$ 衰减，与梯度提升树相比收敛速率较慢，但避免了树结构带来的指数复杂度项。

**两层神经网络**（Section 4.3）：logit函数为 $g_{\theta}(x) = \frac{1}{m^{\beta}} \sum_{r=1}^{m} a_r \phi(\theta_r \cdot x)$。在梯度下降动态下，函数梯度范数的平方平均满足：

$$\frac{1}{T} \sum_{t=0}^{T-1} \| \nabla_g \ell_{\mathrm{ent}}(g_{\theta^{(t)}}(X), Y) \|_{L_1(S_n)}^2 \leq \frac{K_1}{\gamma^2 T} \left( \frac{m^{2\beta-1}}{w} + K_2 \right)$$

该界揭示了网络宽度 $m$、缩放指数 $\beta$ 和步长 $w$ 对校准性能的影响。实验表明，增加隐藏单元数（从10到100）并未改善测试平滑CE（Figure 6），仅训练指标改善，与理论预测一致。



## 实验与关键发现

### 实验设置

实验在两个合成数据集和一个真实数据集上进行，旨在定性验证理论框架预测的行为趋势，而非与特定校准方法进行基准对比。

**数据集**：
- **Toy dataset (Eq. 34)**：标准二分类合成数据，特征维度 $d=30$，具有较好的线性可分性。
- **Difficult separability toy data (Eq. 35)**：对称结构合成数据，分离性较弱，用于检验边际假设不满足时的校准行为。
- **UCI Breast Cancer**：真实二分类数据集，特征维度 $d=30$。

**评估指标**：训练/测试交叉熵损失、准确率、函数梯度范数（L1/L2）、分箱ECE（binning ECE）、最大平均校准误差（MMCE）和平滑CE（Smooth CE）。

**被分析算法**：梯度提升树（GBT）和两层神经网络。实验通过控制迭代次数 $T$ 和训练样本量 $n$ 两个核心变量，观察各指标的动态变化。

---

### 主要结果

#### 1. 平滑CE随迭代次数和样本量的变化趋势

理论预测训练平滑CE应随迭代数 $T$ 增加而下降，测试平滑CE应随训练样本量 $n$ 增加而下降。实验在两个数据集上均观察到与理论一致的趋势：

- **梯度提升树（Figure 1, 2, 3）**：在Toy dataset上，训练平滑CE随 $T$ 单调递减；测试平滑CE在不同 $n$（500, 1000, 2000）下呈阶梯式下降，样本量越大，测试平滑CE越低。在UCI Breast Cancer数据集上观察到相同模式（Figure 3）。
- **两层神经网络（Figure 4）**：训练平滑CE随迭代次数 $T$ 下降，测试平滑CE随样本量 $n$ 增加而改善，与理论预测一致。

![[assets/figures/papers/iclr26_0011_qXVmmj8J0T_Smooth_Calibration_Error_Uniform_Convergence_and/figures/007_Figure_1.jpg]]
*Figure 1: GBT experiments on the toy dataset defined in Eq. (34) with m $\geq$ d*

![[assets/figures/papers/iclr26_0011_qXVmmj8J0T_Smooth_Calibration_Error_Uniform_Convergence_and/figures/023_Figure_4.jpg]]
*Figure 4: Two-layer neural network using toydata defined in Eq. (34)*

![[assets/figures/papers/iclr26_0011_qXVmmj8J0T_Smooth_Calibration_Error_Uniform_Convergence_and/figures/019_Figure_3.jpg]]
*Figure 3: GBT experiments for UCI breast cancer dataset d = 30*

**置信度**：0.95。趋势定性一致，但未提供严格的统计显著性检验。

#### 2. 函数梯度范数的单调递减

理论核心机制是训练平滑CE被函数梯度的L1范数所控制（Eq. 5），因此优化过程中函数梯度范数的下降直接导致校准改善。

- **梯度提升树（Figure 1(a), 4(a) 左列）**：训练函数梯度范数（L1和L2）随迭代数 $T$ 单调递减，与理论界 $O(1/\sqrt{T})$ 的收敛速率定性吻合。
- **两层神经网络（Figure 4(a) 左列）**：函数梯度范数同样随 $T$ 单调下降。

**置信度**：0.9。梯度范数下降趋势明确，但未进行定量收敛速率检验。

#### 3. 弱分离条件下的校准行为

当数据分离性较弱时（Eq. 35 的对称玩具数据），边际假设可能不成立。实验显示（Figure 5），两层神经网络在该数据上的测试平滑CE仍随样本量 $n$ 增加而单调下降，表明理论框架的结论在较弱条件下仍可能成立，尽管当前理论证明依赖于强边际假设。

![[assets/figures/papers/iclr26_0011_qXVmmj8J0T_Smooth_Calibration_Error_Uniform_Convergence_and/figures/026_Figure_5.jpg]]
*Figure 5: Two-layer neural network using toy dataset defined in Eq. (35)*

**置信度**：0.9。仅在一组参数下验证，需要更多实验确认。

---

### 消融分析

#### 1. 树深度对梯度提升树校准的影响

比较 Figure 1（$m \geq d$，较深树）和 Figure 2（$m < d$，较浅树）可知，两种设置下训练/测试平滑CE、函数梯度范数等指标的行为高度相似。Figure 3 在真实数据上进一步验证了 $m=30$ 和 $m=3$ 的校准行为一致性。这表明梯度提升树的校准性能对树深度具有较好的鲁棒性。

![[assets/figures/papers/iclr26_0011_qXVmmj8J0T_Smooth_Calibration_Error_Uniform_Convergence_and/figures/013_Figure_2.jpg]]
*Figure 2: GBT experiments on the toy dataset defined in Eq. (34) with m \< d*

**置信度**：0.9。仅在有限深度范围内验证，极端深度（如决策树桩 vs 完全生长树）的行为未探索。

#### 2. 隐藏单元数对两层神经网络校准的影响

Figure 6 比较了隐藏单元数为10和100的两层神经网络在UCI Breast Cancer上的表现。增加隐藏单元数仅改善了训练集上的损失和校准指标，但测试平滑CE并未获得显著改善。这一现象与理论分析一致：增加模型容量虽然可以提升训练性能，但泛化间隙（由覆盖数/Rademacher复杂度控制的项）也随之增大，导致总体平滑CE的改善有限。

![[assets/figures/papers/iclr26_0011_qXVmmj8J0T_Smooth_Calibration_Error_Uniform_Convergence_and/figures/032_Figure_6.jpg]]
*Figure 6: UCI breast cancer dataset d = 3 0*

**置信度**：0.9。仅在两个容量级别上比较，未进行更系统的容量缩放实验。

---

### 失败模式与过拟合

#### 1. 测试集上的过拟合现象

多个实验揭示了校准指标的过拟合行为：

- **梯度提升树（Figure 1(a) 中间列）**：测试交叉熵损失和平滑CE在迭代后期出现反弹上升，而训练指标持续下降。这表明存在训练-测试平滑CE的折中，与理论界中训练项递减而复杂度项递增的结构一致（Corollary 2）。
- **两层神经网络（Figure 4(a) 中间列）**：测试损失和平滑CE在训练后期同样出现回升，且回升幅度随样本量减小而增大（$n=500$ 时最明显）。

**置信度**：0.95。过拟合现象在多个设置下稳定出现。

#### 2. 一致收敛界的常数因子问题

理论界（Corollary 2）中包含与维度 $d$、树深度 $m$ 等相关的对数因子和常数项（如 $C_3 w T \sqrt{2^m \log n d / n}$）。实验未对这些常数的紧致性进行数值验证，实际可达到的平滑CE水平与理论上界的差距需要进一步量化。**此点需人工核实**。

---

### 重要图表结论

- **Figure 1, 2, 3**：梯度提升树的训练平滑CE和函数梯度范数随 $T$ 单调递减，测试平滑CE随 $n$ 阶梯下降，树深度对校准行为影响不显著。
- **Figure 4**：两层神经网络的函数梯度范数和平滑CE随 $T$ 下降，测试平滑CE随 $n$ 改善，但存在过拟合风险。
- **Figure 5**：即使在弱分离条件下，测试平滑CE仍随样本量增加而改善，提示理论可能具有超出当前假设的适用性。
- **Figure 6**：增加隐藏单元数仅改善训练校准，测试平滑CE未获显著收益，验证了模型复杂度与泛化校准之间的折中。
- **Table 1**：提供交叉熵损失和平方损失的Savage表示，为一般proper评分规则下的平滑CE分析提供理论工具，实验部分未直接使用。

---

### 实验局限

1. **定性验证为主**：实验旨在展示理论预测的行为趋势，未进行严格的收敛速率检验或统计假设检验。
2. **数据集规模有限**：仅在两个合成数据集和一个真实数据集上验证，泛化性存疑。
3. **未涉及公平性评估**：所有实验均为标准二分类设置，未考察不同子群体上的校准差异。
4. **核提升未实验验证**：理论分析涵盖的核提升算法未进行实验验证，其校准行为的实证证据缺失。**此点需人工核实**。



## 定位与知识库关联

### 理论谱系中的位置

本文的分析框架建立在两条理论线索的交汇处：**校准误差的度量理论**与**函数空间优化的收敛分析**。

在度量理论一侧，Błasiok et al. (2023) 证明平滑CE提供了分箱ECE的上下界，使其成为理论上可靠的校准代理。本文继承这一定义，但将其从度量工具提升为可优化的目标——通过建立平滑CE与后处理间隙（post-processing gap）的双向不等式 $\operatorname{smCE}(f, \mathcal{D})^2 \leq \operatorname{pGap}(f, \mathcal{D}) \leq 2\operatorname{smCE}(f, \mathcal{D})$，将校准误差与损失函数的可改进量直接挂钩，为函数梯度分析提供了桥梁。

在优化理论一侧，Mason et al. (1999) 建立了梯度提升作为函数空间梯度下降的解释，Nitanda et al. (2019) 将两层神经网络在特定超参数设置下与神经正切核（NTK）的提升过程联系起来。本文的核心贡献在于将这两条线索耦合：**证明训练平滑CE可由损失函数关于预测的函数梯度的L1范数上界控制**，从而将校准误差的优化转化为函数梯度范数的减小问题。

### 适用边界与假设依赖

框架的适用性受以下关键假设约束：

1. **边际假设（Assumption 2, 3）**：要求存在常数 $\gamma > 0$ 使得对所有训练样本有 $|f(X_i) - Y_i| \geq \gamma$。这是一个较强的条件，本质上限定了数据在预测概率空间中的可分离性。当数据线性不可分或存在标签噪声时，该假设可能被违反，此时理论界中的 $1/\gamma$ 项会发散。实验部分（Figure 5）在较难分离的对称玩具数据上进行了验证，但该验证仍是定性且受控的。

2. **二分类限制**：整个分析框架——包括平滑CE的定义、对偶形式、以及函数梯度控制定理——均针对二分类任务构建。多分类校准误差（如顶部标签校准）需要不同的度量定义和理论工具。

3. **固定步长梯度下降**：梯度提升树和核提升的分析假设固定步长 $w$，两层神经网络的分析也基于固定学习率的梯度下降。该分析未覆盖自适应步长、动量方法或Adam等现代优化器。

4. **RKHS的Lipschitz复合封闭性**：核提升部分（Section 4.2）要求RKHS对Lipschitz函数复合保持封闭，以便将函数梯度范数转化为RKHS范数。目前该性质仅对极少数核（如Laplace核）严格成立，限制了直接范数分析的适用范围。

### 已知局限

1. **常数因子未优化**：一致收敛界中包含与维度 $d$、树深度 $m$ 相关的对数因子（如 $\sqrt{2^m \log n d / n}$），以及通用常数 $C_2, C_3$。这些常数在实际应用中可能较大，使得理论界在有限样本下的指导意义受限。

2. **过拟合现象的定性观察**：实验显示（Figure 1(a) 中面板，Figure 4(a) 中面板），交叉熵损失和平滑CE在测试集上随迭代数 $T$ 增加可能出现上升，表明存在过拟合。理论分析（Corollary 2）虽然揭示了训练-泛化折中，但未给出避免过拟合的早停准则或显式正则化方案。

3. **容量增加未改善测试校准**：两层神经网络实验中（Figure 6），将隐藏单元数从10增加到100仅改善了训练指标，测试平滑CE未见提升。这说明单纯扩大模型容量不会自动改善校准，但理论框架尚未对此现象提供解释。

### 开放问题

1. **弱化假设条件**：能否在无边际假设或可验证的较弱条件下（如仅假设边缘分布的光滑性）获得类似的平滑CE保证？这是将理论推向实际应用的关键障碍。

2. **多分类扩展**：如何将函数梯度控制的分析框架扩展到多分类校准误差？需要同时解决度量定义（如类别级校准与置信度校准的关系）和优化分析（多输出函数的梯度结构）两个层面的问题。

3. **一般proper评分规则**：当前分析深度依赖交叉熵损失的特定函数梯度形式（$\nabla_g \ell_{\text{ent}} = \sigma(g) - y$）。对于一般的proper评分规则（如Brier分数），是否也能建立类似的函数梯度控制定理？Table 1给出的Savage表示可能为此提供起点。

4. **校准正则化的设计**：理论框架揭示了函数梯度范数作为校准代理的角色，能否据此设计新的校准正则化项或训练算法？例如，显式惩罚函数梯度的L1范数可能直接改善校准，而不依赖边际假设。

5. **与其他校准方法的理论联系**：温度缩放、直方图分箱等后处理方法在实践中被广泛使用，但缺乏基于函数梯度的理论保证。本框架能否为理解这些方法的有效性提供统一视角？

6. **优化器扩展**：分析假设固定步长梯度下降，如何扩展到自适应优化器（如Adam）或随机梯度下降的校准保证？这需要处理随机梯度噪声对函数梯度范数估计的影响。



## 原文 PDF

![[paperPDFs/ICLR_2026/Smooth_Calibration_Error_Uniform_Convergence_and_Functional_Gradient_Analysis.pdf]]

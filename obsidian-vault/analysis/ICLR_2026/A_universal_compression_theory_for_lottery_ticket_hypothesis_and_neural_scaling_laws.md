---
title: "A universal compression theory for lottery ticket hypothesis and neural scaling laws"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_universal_compression_theory_for_lottery_ticket_hypothesis_and_neural_scaling_laws.pdf
project_link: null
code_link: null
aliases:
- UCMMC
- UCTLTHNSL
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/theory
core_operator: "控制压缩质量的关键因素是矩匹配阶数 k 和聚类直径：通过保留前 k 阶张量矩并将对象分组到小直径聚类中，可以在几乎不损失信息的情况下显著减少对象数量。"
primary_logic: "任意光滑的置换对称函数可以被压缩到仅需 polylog(d) 个加权对象，而误差随对象数量增加而趋于零；这一压缩率是最优的。"
claims:
- "通用压缩定理（定理 4）证明 d 个对象可以被压缩到 d′ 个加权对象，误差界为 O(d(d′)^{1-(k+1)/m})。"
- "最优压缩率下界（定理 8）表明无法用少于 polylog(d) 个对象实现有限误差压缩。"
- "压缩数据集在教师-学生任务上的测试 MSE 与完整数据集几乎一致，而随机子采样明显偏离。"
- "压缩神经网络（动态彩票假说）在整个训练过程中与原网络保持相同的训练动态。"
---

# A universal compression theory for lottery ticket hypothesis and neural scaling laws

> [!tip] 核心洞察
> 任意光滑的置换对称函数可以被压缩到仅需 polylog(d) 个加权对象，而误差随对象数量增加而趋于零；这一压缩率是最优的。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 彩票假说与神经尺度定律的通用压缩理论 |
| 英文题名 | A universal compression theory for lottery ticket hypothesis and neural scaling laws |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vxkzW4ljeX) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/theory |
| Method | Universal Compression via Moment Matching and Clustering |
| Dataset | teacher–student function fitting (Eq. 13), cylindrical harmonic function learning, teacher–student (neural scaling law, data), cylindrical harmonic (neural scaling law, width) |

> [!tip] 效果简介
> - teacher–student function fitting (Eq. 13) 上，Test MSE loss (dataset compression) 为 compressed dataset d′=10³ (k=5)，对比 original dataset d=10⁴，变化 loss curves nearly overlap。
> - cylindrical harmonic function learning 上，Test MSE loss (network width compression) 为 compressed width d′=10³ (k=5)，对比 original width d=10⁴，变化 training dynamics indistinguishable。
> - teacher–student (neural scaling law, data) 上，MSE loss vs. dataset size 为 compressed dataset scaling exponent α̂≈0.60，对比 original dataset scaling exponent α≈0.13，变化 Δα = +0.47。

## 概要
大规模神经网络与海量训练数据普遍面临维度灾难，导致训练成本极高;然而，对称性——尤其是模型权重与数据样本之间的置换不变性——为非平凡压缩提供了可能。本工作为彩票假说和神经尺度定律建立了一套统一的通用压缩理论:任意光滑的置换对称函数都可以被无损压缩到仅需约 $O(\operatorname{polylog} d)$ 个加权对象，且这一压缩率被证明是最优的。

核心控制手段是**矩匹配阶数 $k$ 与聚类直径**。算法先通过聚类将对象分组为小直径子集，再在每个子集内调整权重，使得前 $k$ 阶张量矩保持不变;这一过程可将 $d$ 个对象压缩为 $d'$ 个带权对象。通用压缩定理(定理 4)给出误差界
$$\bigl|\phi(c')-\phi(c)\bigr| = O\!\left(d\,(d')^{1-\frac{k+1}{m}}\right),$$
其中 $m$ 是对象所在空间的维数。最优性下界(定理 8)表明，以有限误差压缩时，所需对象数必须满足 $d'=\Omega(\operatorname{polylog}d)$，因此 $O(\operatorname{polylog}d)$ 是渐近最优的。

方法层面，压缩可分为三个步骤:聚类(如 $k$-均值)、矩匹配(依赖 Tchakaloff 约化，见算法 2)、以及加权前向/反向传播。对于动态彩票假说，进一步将等变更新规则应用于压缩后的加权对象，保证压缩子网络在整个训练过程中与原网络保持相同的训练动态(定理 5)。

实验主要结论如下:
- 在教师-学生函数拟合任务中，使用 $k=5$ 矩匹配将 $d=10^4$ 的数据集压缩到 $10^3$ 后，测试损失曲线几乎与原数据完全重合，而随机子采样则明显偏离(图 3)。
- 在柱谐函数学习任务中，同样使用 $k=5$ 将宽度为 $10^4$ 的两层网络压缩到 $10^3$，训练过程中的损失动态无法区分;随机子网络则无法复现原动态(图 4)。
- 压缩大幅改进了神经尺度定律:将数据集或网络宽度压缩 $d\to d'\approx 16\sqrt{d}$ 后，幂律指数 $\alpha$ 从约 0.1 提升至约 0.6(图 5)，数据效率显著提高。
- 消融实验验证矩匹配阶数 $k$ 越高，误差随 $d$ 衰减的幂律指数越接近理论预测的 $(k+1)/m+0.5$(图 2e);压缩至 $O(\log^m d)$ 个对象后误差随 $d$ 增大而趋于零(图 8)。

需要注意的是，理论严格依赖于函数的 Taylor 光滑性假设，实验仅基于合成任务，对 ReLU 等非光滑激活尚未建立等强度的误差界;聚类环节使用启发式策略，其理论保证亦未完全覆盖混合算法。此外，压缩算法在实际大模型和真实数据集上的有效性与公平性仍有待验证。



现代深度学习的成功很大程度上依赖于不断增长的数据集规模和模型参数量，但这种扩展也带来了严重的“维度灾难”：当数据点数量 $d$ 或网络神经元数量变得极大时，训练所需的计算开销与存储成本急剧上升，而边际性能提升却逐渐降低。大量经验观察表明，损失函数 $L$ 随数据规模 $d$ 的衰减通常服从幂律形式

$$
L(d) \propto d^{-\alpha},
$$

其中缩放指数 $\alpha$ 在典型的训练任务中往往仅约 $0.1$ 左右。这意味着欲使损失下降一个数量级，需要将数据或参数规模扩大数百倍，严重制约了实际应用的可扩展性。

与此同时，深度网络与训练数据本身具有显著的**置换对称性**。以两层网络为例，前向传播可写作

$$
f(x) = \sum_{i=1}^d v_i\,\sigma(w_i^\top x),
$$

任何对神经元对 $(v_i,w_i)$ 的置换都不会改变网络输出；类似地，平均损失

$$
L = \frac{1}{d}\sum_{i=1}^d \ell(x_i,y_i,\theta)
$$

对数据点的排列也是不变的。根据 Deep Set 表示定理，任意光滑的置换不变函数都可以表示为聚合形式

$$
f(w_1,\dots,w_d) = h\!\left(\sum_{i=1}^d g(w_i)\right),
$$

这意味着高维函数本质上由许多低维“对象”通过对称性组合而成。当对象数量十分巨大时，相似的对象会挤在紧邻区域中，使得多数对象在函数计算中近乎冗余（示意图见 Figure 1）。因此，若能精确保留这些对象的**集合矩信息**，就有可能用远远少于 $d$ 的加权对象来复现函数输出，从而摆脱维度灾难的桎梏。

然而，已有压缩与剪枝方法（如随机丢弃一个子集）在实际中往往导致训练动态偏离原模型。例如，随机子采样网络神经元后，损失轨迹会与完整网络产生明显分离，无法保持相同的训练动态（对照 Figure 4 的绿色与蓝色曲线）；类似地，从数据集中随机抽取子集进行训练，其最终测试误差明显高于完整数据集，说明单纯的随机降采样无法保留足够的信息（对照 Figure 3 的绿色与蓝色曲线）。这些缺口揭示出一个根本问题：**如何在几乎不损失信息的前提下，将大量对称对象压缩成极少数目的加权对象，并让压缩后的系统在训练过程中保持与原系统近乎一致的动态行为？**

本文正是围绕上述问题展开。我们基于置换对称性与矩匹配理论，提出一个**通用压缩理论**：对任意光滑的 $d$ 元对称函数，可以利用前 $k$ 阶张量矩的保持，将 $d$ 个对象压缩为仅 $d' = O(\mathrm{polylog}\,d)$ 个加权对象，且压缩误差随对象数增加而趋于零；同时证明这一压缩率在渐近意义下是最优的。将该理论分别应用于数据点和神经元，可以得到：**（1）** 在原数据集上保持训练动态的压缩数据集，使缩放指数 $\alpha$ 从约 $0.13$ 跃升至约 $0.60$；**（2）** 压缩后的子网络能在整个训练过程中完美复现原网络的损失轨迹，从而严格证明了“动态彩票假说”。这些发现表明，利用置换对称性进行结构化压缩，不仅能大幅降低计算与存储成本，更有望从原理上提升神经缩放定律的效率，为大规模神经网络的高效训练提供新的理论基石。



## 核心方法与创新机理

本文的核心创新在于**通过保持置换对称函数的前 k 阶张量矩，并利用小直径聚类，将大规模对象集（神经元或数据点）压缩为极少数加权对象，同时几乎不损失信息**。这一压缩策略直接改变了三个影响性能与控制代价的关键槽位（changed slots），使得原本难以优化的维度灾难问题得到有效缓解。

### 1. 关键槽位变化：数量、权重与训练动态

相对于随机构造子集（random subsampling）基线，本方法在以下三个维度上进行了根本性的重新设计：

- **对象数量（$d \to d'$）**：基线采用全部 $d$ 个对象，而提出方法将对象数压缩至远小于 $d$ 的 $d'$，典型为 $\operatorname{polylog}(d)$ 或 $O(d^{\sigma})$ 规模。理论上，通用压缩定理（定理 4）给出误差界 $|\phi(c')-\phi(c)| = O\big(d (d')^{1-(k+1)/m}\big)$，并证明了在允许误差 $\varepsilon(d)$ 的条件下，$d' = O\big(\log^m\frac{d}{\varepsilon(d)}\big)$ 是最优压缩率（定理 7、定理 8）。

- **加权方案**：基线使用均匀权重（$c_i=1$），而提出方法引入非负权重 $c_j$，在减少支撑点数量的同时精确保持前 $k$ 阶矩不变（定义 2 与算法 2）。这一加权组合使压缩后的表示仍然能够完整保留原始集合的低阶统计结构，是逼近精度得以保证的核心微观机制。

- **训练动态**：基线直接对所有对象施加梯度更新，而提出方法采用等变压缩动态，通过加权矩以及调整后的梯度（如 $c_j^{-1}$ 因子）来维持与原始网络相同的行为轨迹（定义 5、附录 C）。这使得压缩后的子网络在整个训练过程中的损失曲线与原始网络几乎完全重合，而随机抽样的子网络则显著偏离（Figure 4）。

### 2. 从对称性到维度灾难的化解

因果链条的核心是**置换对称性**与**光滑性**的共同作用。当损失函数或网络参数对神经元/数据点的排列保持不变时（如 $\frac{1}{d}\sum_i \ell(x_i,y_i,\theta)$ 或 $f(x)=\sum_i v_i\sigma(w_i^T x)$），其行为完全由各对象的矩张量 $p_k = \frac{1}{d}\sum_i w_i^{\otimes k}$ 决定（Deep Set 表示，Eq. (4)）。在 $d$ 极大时，对象在高维空间中趋于拥挤，光滑性保证较短距离内的函数变化很小，因此使用**聚类**将邻近对象聚合，再通过**矩匹配**裁剪冗余对象，就可以在几乎不影响整体性能的前提下大规模削减对象数量。这一压缩过程将原本随 $d$ 线性增长的计算开销，转变为准对数规模，从而打破了维度灾难对大型网络和数据集训练成本的限制。

实验证据直接支持这一论断：在教师‑学生函数拟合任务中，使用 $k=5$ 阶矩匹配将 $d=10^4$ 数据集压缩至 $d'=10^3$ 后，测试 MSE 曲线与完整数据集几乎重叠，而随机子采样则明显偏离（Figure 3）。类似地，在柱谐函数学习任务中，压缩宽度 $d'=10^3$ 网络的训练动态与原始宽度 $d=10^4$ 网络无法区分（Figure 4(b–d)）。此外，压缩后神经尺度定律的幂律指数从约 0.1 提升至约 0.6，意味着数据效率获得质的提高（Figure 5）。

### 3. 压缩流水线的三大模块

压缩的实现依赖于三个可模块化的构件，共同完成了“聚类—矩保持—加权训练”的闭环：

- **聚类（Clustering）**：例如使用 $k$-均值或贪婪策略，将对象分组到小直径的簇内，为局部矩匹配提供高分簇分辨基础（Algorithm 1 步骤 1，附录 D）。
- **矩匹配（Moment Matching）**：基于 Tchakaloff 缩减（定理 2），在每一簇内调整权重，使得支撑点数量减少但前 $k$ 阶矩严格不变（Algorithm 2）。该步骤的构造性证明确保了方法的工程可实现性。
- **加权前/反向传播**：在压缩后的网络上，通过加权输出与调整后的梯度，保证训练过程的等变性，从而维持网络动态与原模型一致（Eq. (15)，附录 C）。

尽管理论误差界针对贪婪策略给出严格证明，而实验采用混合 $k$-均值/贪婪策略，后者目前缺乏同样强的理论保证（附录 D）；同时，高阶矩匹配的计算复杂度随 $k$ 和对象维度 $m$ 快速增长，在极高维应用场景中仍需进一步优化。总体而言，这一创新框架将彩票假说与神经尺度定律统一在压缩理论的视角下，为理解大规模模型的对称性与压缩性提供了坚实且可操作的数学基础。



![[assets/figures/papers/iclr26_0004_vxkzW4ljeX_A_universal_compression_theory_for_lottery_ticke/figures/001_Figure_1.jpg]]
*Figure 1: (a) Illustration of the main idea behind the compressibility of neural networks and datasets. (1) Permutation symmetry allows a high-dimensional function to be decomposed into a composition of d lowdimensional “objects” (dots in the figure). (2) When d is large, these objects become crowded, and those lying in denser regions are essentially redundant; they can be compressed into $d ^ { \prime }$ = O ( $\mathrm { p o l y l o g }$ d ) objects. The potential curse of dimensionality can thus be mitigated, or even removed, when the underlying function is smooth—a lesson well known in nonparametric statistics. (b) Decomposing the linear weights of a neural network into “objects” of symmetric status

置换对称性是大规模神经网络和数据集的内在结构：损失函数对神经元（或数据点）的交换保持不变。当对象数量 $d$ 急剧增长时，维度灾难使参数分布高度密集，大量对象几乎冗余。通用压缩理论的核心即利用这一对称性，通过 **聚类** 与 **矩匹配** 两个核心模块，将 $d$ 个原始对象压缩为 $d^{\prime} \ll d$ 个加权对象，并在后续训练或推理中以几乎零信息损失使用这些压缩表示。整体流水线及模块关系如下：

1. **聚类**（Clustering）—— 将原始对象集 $\{w_i\}_{i=1}^{d}$ 划分为若干直径极小（一般 $O(d^{-1/m})$ 量级）的子集 $S_1, S_2, \dots$ 。实验采用启发式策略（如 $k$-means），仅在目标压缩尺寸 $d^{\prime}$ 接近时切换至贪心策略；理论误差界（定理 4、7）仅针对纯贪心策略严格成立，混合策略尚无同等强保证。此步骤的因果意义在于：小直径簇内的对象高阶矩变化甚微，从而可通过后续矩匹配大幅削减支持却不引入显著逼近误差。

2. **矩匹配**（Moment Matching）—— 对每个簇内的对象，通过求解线性规划（Tchakaloff 约化，算法 2）保留 **前 $k$ 阶张量矩**
   $$p_k = \frac{1}{d}\sum_{i=1}^{d} w_i^{\otimes k}$$
   并将该簇的原始 $|S|$ 个对象替换为至多 $N_{m,k}$ 个加权对象 $\{(c_j, w_j)\}$，权重 $c_j \ge 0$ 满足矩不变条件。其核心机制是：光滑置换对称函数可由其前 $k$ 阶矩近似，当 $k$ 足够大且簇直径足够小时，**压缩误差上界**为
   $$\mathcal{E} = |\phi(c^{\prime}) - \phi(c)| = O\!\left(d\,(d^{\prime})^{1-\frac{k+1}{m}}\right),$$
   即误差随 $d^{\prime}$ 的增加而多项式衰减。理论进一步表明，当允许误差 $\varepsilon(d)$ 趋于零时，所需加权对象数可降至
   $$d^{\prime} = O\!\left(\log^m \frac{d}{\varepsilon(d)}\right),$$
   这是渐近最优压缩率（定理 8 给出了匹配下界）。

3. **加权前向/反向传播**（Weighted Forward/Backward Pass）—— 对于数据集压缩，损失函数从 $\frac{1}{d}\sum_{i=1}^d \ell(x_i, y_i, \theta)$ 变为对加权压缩样本 $\{(c_j, x_j, y_j)\}$ 的求和形式。对于神经网络压缩（动态彩票假说），等效地将前向传播 $f(x)=\sum_{j} c_j v_j\sigma(w_j^T x)$ 与梯度更新规则中的学习率按 $c_j^{-1}$ 重新标度，以保证压缩子网络的训练动态与原网络一致（定义 5，图 4 实验证实动态曲线几乎不可区分）。

**输入**：$d$ 个对象（可以是训练数据点，也可以是神经元参数对 $(v_i, w_i)$）。  
**输出**：$d^{\prime} \ll d$ 个加权对象 $\{(c_j, w_j)\}_{j=1}^{d^{\prime}}$，满足前 $k$ 阶矩保留，且支持集直径控制在理论要求的量级。该压缩后的加权表示可直接嵌入原损失函数或网络前向计算，实现训练或推理。

该框架的关键调控旋钮是 **矩匹配阶数 $k$** 与 **最终压缩尺寸 $d^{\prime}$**（由聚类粒度决定）：增大 $k$ 能提升近似精度（图 2(e) 显示误差指数 $\alpha\approx (k+1)/m + 0.5$），以更高阶矩计算为代价；减小聚类直径可压缩更多对象，但带来聚类开销。整体而言，流水线把“置换对称”这一结构性先验转化为可控的压缩‑精度折中，并将神经尺度定律的幂指数从 $\sim$0.1 大幅提升至 $\sim$0.6（图 5），从根本上提高了数据与参数的利用效率。

需注意的薄弱环节：目前实验仅在合成任务上验证；$k$-means 等启发式聚类虽在实践中高效，却缺乏严格误差上界；非光滑激活（如 ReLU）的支持还缺乏理论保证，且高维对象（$m$ 大）时矩匹配的计算复杂度急剧上升。以上证据强度高（定理 4、7、8 置信度 0.95；图 3、4 实验一致性置信度 0.9‑0.95），但对真实大模型场景仍需手动谨慎评估。



### 关键压缩模块

压缩流程由三个模块构成，它们通过“聚类缩小邻域 → 矩匹配降样本 → 加权等变训练”的因果链，将 $d$ 个对象压缩为 $d'$ 个加权对象，并保持函数值或训练动态几乎不变。

1. **聚类（Clustering）**  
   将空间上相近的对象归入同一簇，使簇直径控制在 $O(|{\rm supp}(c)|^{-1/m})$ 量级。小直径是矩匹配实现高精度泰勒截断的前提（Algorithm 1 Step 1）。实际实现中采用混合策略：先用粗粒度的 k‑means 聚类，当支撑集接近目标尺寸 $d'$ 时切换至贪心聚类以获得更强的理论保证（附录 D）。该步骤控制了压缩误差的上界瓶颈。

2. **矩匹配（Moment Matching / Tchakaloff 缩减）**  
   在单个簇内，通过调整非负权重 $c_j$，使得压缩前后的前 $k$ 阶张量矩保持不变：
   
$$
p_k = \frac{1}{d}\sum_{i=1}^d w_i^{\otimes k} = \frac{1}{\sum_j c_j}\sum_{j} c_j w_j^{\otimes k}, \quad k=0,1,\dots
$$

   同时将支撑集大小缩减至至多 $N_{m,k}$ 个对象（Algorithm 2，即 Tchakaloff 定理的构造性证明）。**矩匹配阶数 $k$ 是压缩质量的核心控制变量**：$k$ 越大，高阶矩信息保留越多，压缩误差衰减越快。

3. **加权前向/反向传播（Weighted Forward/Backward Pass）**  
   压缩后的加权对象直接参与网络输出和梯度计算。为实现与原网络一致的等变训练动态，将原始参数 $w_j$ 的梯度更新替换为 $c_j^{-1}\,\partial L/\partial w_j$（附录 C，定义 5）。此模块确保压缩网络在整个训练过程中的损失曲线与原网络重合（Figure 4），从而证明了动态彩票假说。

### 核心公式与变量含义

下列公式是压缩理论与尺度定律改进的数学骨架，所有符号均基于已给出的原文定义，没有外推公式。

**对称函数的表示与矩**  
两层网络的输出（Eq. 3）：
$$f(x)=\sum_{i=1}^d v_i\,\sigma(w_i^T x),$$
其中 $(v_i,w_i)$ 可任意交换，体现了置换对称性。任意光滑对称函数可写成 Deep Set 形式（Eq. 4）：
$$f(w_1,\dots,w_d)=h\!\left(\sum_{i=1}^d g(w_i)\right).$$
定义 **$k$ 阶张量矩**（Eq. 5）：
$$p_k = \frac{1}{d}\sum_{i=1}^d w_i^{\otimes k}.$$
压缩后的加权集合记为 $\boldsymbol{\theta}' = \{(c_1,w_1),\dots,(c_{d'},w_{d'})\}$，权重满足 $\sum_j c_j w_j^{\otimes l} = \sum_i w_i^{\otimes l}$（$l=0,\dots,k$）。

**通用压缩误差上界（定理 4）**  
使用 $k$ 阶矩匹配将 $d$ 个 $m$ 维对象压缩至 $d'$ 个加权对象时，逼近误差满足：
$$|\phi(c') - \phi(c)| = O\!\left(d\,(d')^{1-\frac{k+1}{m}}\right),\tag{9}$$
其中 $\phi$ 为任意光滑对称函数。该界的因果机制是：聚类将对象限制在半径 $r\sim (d')^{-1/m}$ 的球内，矩匹配保留了该球上的 $k$ 阶泰勒展开，截断误差为 $O(r^{k+1})$，乘以对象数 $d$ 即得上界。当 $k+1>m$ 时，即使 $d'$ 远小于 $d$，误差也随 $d'$ 增大而多项式下降。

**最优 polylog 压缩尺度（定理 7 与定理 8）**  
若允许误差 $\varepsilon(d)$ 随 $d$ 趋向零，所需的最少加权对象数可达渐近下界：
$$d' = O\!\left(\log^m \frac{d}{\varepsilon(d)}\right).\tag{45}$$
该尺寸是 **信息论最优**：定理 8（Eq. 65）构造了一个对称函数实例，证明任何保持 $\varepsilon$ 误差的压缩方案必须使用至少 $\Omega(\log^m(d/\varepsilon))$ 个对象。因此，压缩率不可能超越 polylog$(d)$ 阶。

**压缩提升的尺度定律**  
标准化经验尺度定律为 $L(d) \propto d^{-\alpha}$（Eq. 1）。压缩后，损失随压缩尺寸 $d'$ 的标度变为 $L(d') \propto (d')^{-\hat{\alpha}}$，实验测得指数 $\hat{\alpha}$ 从原始 $\approx 0.1$ 提升至 $\approx 0.6$（Figure 5）。这是因为压缩移除了稠密区域中的冗余对象，使有效数据量指数增长，从而打破了原尺度定律的高维度灾难瓶颈。

> **边界与局限**：上述误差界假设激活函数光滑（如 sigmoid）；对 ReLU 等非光滑情形仅进行了实验验证，缺乏严格界。实际采用的混合 k‑means/贪心聚类策略尚未获得与纯贪心策略等同的理论保证。高阶矩匹配的计算复杂度随 $k$ 和维度 $m$ 快速增长，限制了对高维对象的直接应用。



## 实验与关键发现

我们在一系列合成对称函数和教师‑学生任务上验证通用压缩理论的三个核心主张：**压缩误差以多项式速率随对象数衰减**，**压缩数据集/子网络能够复现完整训练动态（动态彩票假说）**，以及**压缩操作可系统性地提高神经尺度定律的指数**。

### 压缩误差定标与消融
图 2 展示了用矩匹配算法压缩一般对称函数 $f$（公式 13）时的误差定标曲线。  
- **主结论**：匹配更高阶数的张量矩（更大的 $k$）导致更快的误差衰减。拟合指数 $\hat\alpha$ 接近 $(k+1)/m + 0.5$（图 2(e)），与定理 4 的理论上界 $O(d (d')^{1-(k+1)/m})$ 一致。  
- **消融含义**：$k$ 直接控制压缩质量——增大 $k$ 相当于保留更多泰勒级数信息，从而指数级地压低了近似误差。当 $k$ 固定时，误差随原对象数 $d$ 的增长而下降，但在小 $d$ 区域可能出现非单调波动（图 2(a–d)）。  
- **因果瓶颈**：误差来自低阶矩匹配丢弃的高阶泰勒项，阶数越高此项的系数量级越小；但代价是矩匹配步骤的计算复杂度随 $k,m$ 快速增长。

### 数据集压缩（教师‑学生任务）
在教师‑学生函数拟合任务中（公式 13），我们比较：  
- 原始数据集大小 $d=10^4$（绿虚线）  
- 用 $k=5$ 矩匹配压缩至 $d'=10^3$ 的加权数据集（橙线）  
- 随机抽取 $10^3$ 样本的子集（蓝线）  

图 3 显示，压缩数据集的测试 MSE 曲线与原始数据集几乎完全重合，而随机子采样则明显偏离。这表明**前 k 阶矩匹配能保留训练所需的分布信息**，而朴素子采样丢失了这些信息。该实验直接支撑定理 4 的结论：置换对称下，通过匹配低阶矩可将数据集高效压缩。

![[assets/figures/papers/iclr26_0004_vxkzW4ljeX_A_universal_compression_theory_for_lottery_ticke/figures/011_Figure_3.jpg]]
*Figure 3: Compression of the training dataset in a teacher–student setup. Green dashed line: training with the original dataset of size d = 1 0 ^ { 4 } ; Orange line: training with a compressed dataset of size 1 0 ^ { 3 } , using order 5 moment matching. Blue line: training with a size-103 subset of the original dataset. Each run uses a cosine annealing learning-rate scheduler, annealing from the value shown in the plot titles to 0. Test MSE loss values are plotted every 10 epochs. It is observed that learning with the compressed dataset closely approximates the original dataset, whereas learning with a naively subsampled dataset does not*

### 动态彩票假说——网络宽度压缩
图 4 使用圆柱谐波任务 $f(x_1,x_2)=J_6(20r)\cos(6\theta)$ 训练两层神经网络（宽度 $d=10^4$），并压缩至宽度 $d'=10^3$（$k=5$ 矩匹配）。  
- **核心发现**：压缩网络的训练动力学（橙线）与原始网络（绿线）在相同小批次顺序下完全重叠，而随机子网络（蓝线）动态偏离严重。  
- **机制**：压缩子网络的权重通过加权梯度的反向传播（式 15；附录 C 中 `c_j^{-1}` 因子）得以保持与前 k 阶矩一致，即网络的前向传播和反向梯度更新都是等变映射的降维近似，从而保证了整个训练轨迹的可重复性（定理 5）。  
- **消融**：去掉矩匹配的单子网络不能维持任何阶段的动态，证明权重化贡献和矩保留是压缩子网络成功复现训练动态的必要条件。

### 神经尺度定律改进
图 5 分别展示了数据集规模与网络宽度的尺度定律变化。  
- **数据集规模**（图 5(a)）：原数据集 MSE 尺度指数 $\alpha \approx 0.13$；用 $k=6$ 矩匹配压缩后，压缩数据集的指数 $\hat\alpha \approx 0.60$，提升约 0.47。  
- **网络宽度**（图 5(b)）：原宽度尺度指数 $\alpha \approx 0.11$，压缩宽度的指数 $\hat\alpha \approx 0.60$，提升约 0.49。  

这些提升源于压缩去除了冗余对象，使剩余加权对象更具信息密度，因此损失随着压缩尺寸 $d'$ 更快衰减。该操作在理论上是将幂律尺度的指数从原始值推到接近 $(k+1)/m$ 的上限（定理 4 推论），实验中几乎提升了 4‑5 倍。

### 算法运行时间
图 6 报告混合压缩算法（k‑means 粗聚类 + 后期贪婪聚类 + 矩匹配）的运行时间。在 $m=1\sim5$ 维立方体上，总时间大致与原始对象数 $d$ 成比例增长，但维度 $m$ 增加时上升显著（$m=5$ 时 $d=10^5$ 约 $10^4$ 秒）。注意此处 $k=5$ 固定，实际 $k$ 更高时的复杂度会急剧上升，当前缺乏严格的复杂度分析。

### Polylog 压缩极限验证
图 8 通过遍历不同的矩匹配阶数 $k$ 寻找最小误差，展示误差随 $d$ 增大的变化。在允许的误差限制下，所需的压缩对象数 $d' = O(\log^m d)$ 级，误差随 $d$ 增长而趋于零。这与定理 7 的 polylog 压缩上界一致，并呼应定理 8 的下界：不能用少于 polylog(d) 个对象实现有限误差压缩。

### 失败模式与局限
尽管实验结果支持理论预测，但存在若干本质限制：
1. **光滑性假设**：理论保证依赖于函数的 Taylor 可展性，实验中使用的 sigmoid 等激活满足此条件，而实际网络中常用的 ReLU 等非光滑激活缺乏严格的误差界（仅实验验证，无证明）。
2. **高维对象的计算瓶颈**：矩匹配步骤需要处理高达 $k$ 阶的张量特征，维度 $m$ 较大时计算量和内存需求急剧膨胀，目前无法直接用于现代大模型的高维神经元或 Token。
3. **启发式聚类的理论空白**：实验采用 k‑means 粗聚类加速，仅在接近目标压缩尺寸时切换为贪婪策略。定理 4 和定理 7 的误差界仅对纯贪婪策略成立，混合策略缺乏理论保障，其压缩质量存在不可预测的退化风险。
4. **合成场景的限制**：所有实验均在人工构造的教师‑学生任务或圆柱谐波函数上进行，还未在真实语言、视觉任务或大规模预训练模型中验证。压缩在真实分布偏移、优化器选择以及混合精度训练下的鲁棒性尚不明确。

以上局限意味着，当前压缩方法从理论到实际大规模系统的迁移仍需要大量验证，尤其是非光滑激活下的误差控制和启发式聚类策略的理论分析是待解决的关键开放问题。

### 补充图表

![[assets/figures/papers/iclr26_0004_vxkzW4ljeX_A_universal_compression_theory_for_lottery_ticke/figures/015_Figure_4.jpg]]
*Figure 4: Dynamical LTH (Theorem 5). The demonstrated task is learning a bivariate function from noisy training data. (a) Ground-truth function f ( $x _ { 1 } , x _ { 2 }$ ) ~ = ~ $J _ { 6 }$ ( 2 0 r ) $\cos$ ( 6 $\theta$ ) , where $r ^ { 2 }$ ~ = ~ $x _ { 1 } ^ { 2 } + x _ { 2 } ^ { 2 }$ and $\theta = \arctan ( x _ { 2 } / x _ { 1 }$ ) , known as a cylindrical harmonic. (b–d) MSE loss vs epoch under three different update rules. Green dashed line: randomly initialized network of width { 1 0 $} ^ { 4 }$ ; Orange line: compressed network of width 1 $0 ^ { 3 }$ , using k = 5 moment matching; Blue line: random subnetwork of the 1 $0 ^ { 4 }$ -width network, also of width 1 $0 ^ { 3 }$ . Loss values are plotted every 50 epoch...

![[assets/figures/papers/iclr26_0004_vxkzW4ljeX_A_universal_compression_theory_for_lottery_ticke/figures/017_Figure_5.jpg]]
*Figure 5: Improving neural scaling laws through compression. (a) MSE loss of the teacher–student task after training on an original dataset of size d vs a compressed dataset of size $d ^ { \prime }$ . (b) MSE loss of the cylindrical harmonic task after training a two-layer neural network of width d versus its compressed counterpart of width $d ^ { \prime }$ . In both panels, we compress d objects to $d ^ { \prime }$ = [ 1 6 $\sqrt { d }$ ] using k = 6 moment matching. The exponent α is obtained by fitting L $\propto d ^ { - \hat { \alpha _ { } } } \mathrm { o r } d ^ { \prime - \alpha }$

![[assets/figures/papers/iclr26_0004_vxkzW4ljeX_A_universal_compression_theory_for_lottery_ticke/figures/007_Figure_2.jpg]]
*Figure 2: Error scaling for compressing a general symmetric function (Eq. (13)) using the moment-matching method. (a–d): each point shows the error in f after compressing d $\to \operatorname { \bar { m a x } }$ ( [ 0 . 1 d ] , $N _ { m , k }$ ) input objects. Matching higher-order moments leads to faster error decay. (e): α is the fitted exponent in | f ( $\theta$ ) - f ( $\mathbf { \hat { \theta } } ^ { \prime }$ ) ∣ ∝ $d ^ { - \alpha }$ The dashed lines indicate { ( k + 1 ) } / { m } + 0 . 5 , which show good agreement with the numerical results

![[assets/figures/papers/iclr26_0004_vxkzW4ljeX_A_universal_compression_theory_for_lottery_ticke/figures/021_Figure_8.jpg]]
*Figure 8: Error scaling of compressing a general symmetric function using the moment-matching method. Here, various different values of k (the order of moment matching) are attempted, from small to large, until the smallest error is found. Each data point is an average over 5 random instances, plotting the average with error bar standing for one standard deviation*



## 定位与知识库关联

本文的“通用压缩”框架将神经网络权重或数据点视为置换对称的“对象”，通过**矩匹配**（保留前 k 阶张量矩）与**聚类**（控制对象直径）将 d 个对象压缩为仅 d′ 个加权对象。其核心因果旋钮是**矩匹配阶数 k** 和**聚类直径**：提高 k 或缩小聚类直径可直接降低压缩误差，代价是更高的算法复杂度。

### 与基线的比较
- **随机子采样（random subsampling）**：最简单的压缩基线，直接丢弃部分对象，权重保持均匀。该基线完全忽略对象间的对称结构与矩信息，如图 3、图 4 所示（蓝色曲线），随机子采样得到的模型在学习动态和最终测试误差上均明显偏离全量对象，而本文的压缩方法（橙色曲线）与“原始未压缩模型（original uncompressed）”几乎一致（置信度 0.9~0.95）。这确立了矩匹配在保持置换不变函数行为上的决定性作用。
- **原始未压缩模型**：作为性能上界，本文在教师‑学生任务（Figure 3）与圆柱谐波任务（Figure 4）上验证了压缩后模型与原始模型在**训练动态**和**测试 MSE** 上的高度吻合，证明压缩几乎没有牺牲信息。在尺度定律实验中（Figure 5），压缩还将数据/宽度规模指数从约 0.1 提升到约 0.6，进一步显示压缩能显著提高数据效率。

### 与后续工作的关系和知识库定位
本文为**动态彩票假说（dynamical lottery ticket hypothesis）**提供了首个严格证明（定理 5，Definition 5）：压缩网络不仅在初始化时存在匹配的子网络，且在整个训练过程中保持相同的动态。压缩方法还被推广到 Transformer 注意力头（Figure 7），表明其潜在适用于更多对称结构。然而，当前工作尚处于理论构建与合成验证阶段，未来研究可延伸到：
- 将压缩理论从光滑激活（如 sigmoid）推广到**非光滑激活（如 ReLU）**，并建立严格的误差界；
- 将矩匹配与**量化、剪枝、低秩分解**等传统压缩技术结合，形成实用的混合压缩管道；
- 在真实大规模语言或视觉模型中检验其训练动态一致性。

### 适用边界与局限
1. **光滑性假设**：理论误差界依赖于函数的 Taylor 可展性（Theorem 4，Eq. 9）。实验虽在 sigmoid 任务上成功，但对于广泛使用的 ReLU 网络，仅有启发式推广，缺乏严格保证。
2. **维度与阶数瓶颈**：压缩算法的复杂度随对象维度 m 和矩阶数 k 快速增长，当 m 较大（如高维对象）时，矩匹配的计算开销可能难以承受。
3. **聚类策略的理论缝隙**：实际使用的混合算法（k‑means 初始聚类 + 贪婪精调，Appendix D）在理论误差界上并不完全覆盖——定理 4/定理 7 仅对纯贪婪聚类策略提供保证，混合策略的误差上界仍是开放问题。
4. **任务与数据的受控性**：所有实验均在合成任务（如 teacher‑student 回归、圆柱谐波函数拟合）上进行，尚未在真实数据集或现代大模型上验证压缩效果及公平性影响（例如数据分布偏移）。
5. **压缩极限的渐近性质**：最优压缩率下界（定理 8，Eq. 65）表明无法用少于 polylog(d) 个对象实现有限误差，但该下界是渐近的，实际中很难在有限规模上精确达到理论极限。

### 开放问题
- 对于**非光滑激活函数**（ReLU、GELU 等），能否建立类似的压缩误差界，或者在何种条件下可保证动态等价？
- **聚类‑矩匹配混合算法**的误差上界如何分析？其计算最优复杂度（作为 m, k, d 的函数）是什么？
- 压缩方法在**多模态、大规模预训练**场景下的鲁棒性如何？直接压缩神经元或注意力头是否仍能保持训练动态与下游任务性能一致？
- 矩匹配技术能否和**量化、蒸馏、剪枝**等成熟模型压缩手段深度融合，从而在推理阶段同时减少权重数量和精度位宽？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_universal_compression_theory_for_lottery_ticket_hypothesis_and_neural_scaling_laws.pdf

![[paperPDFs/ICLR_2026/A_universal_compression_theory_for_lottery_ticket_hypothesis_and_neural_scaling_laws.pdf]]

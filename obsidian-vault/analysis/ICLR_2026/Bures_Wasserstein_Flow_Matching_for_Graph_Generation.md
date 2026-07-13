---
title: "Bures-Wasserstein Flow Matching for Graph Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bures_Wasserstein_Flow_Matching_for_Graph_Generation.pdf
project_link: null
code_link: null
openreview_forum_id: 5Bl5qf3fON
aliases:
- BBWFM
- BWFMGG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将图建模为马尔可夫随机场（GraphMRF），利用Bures‑Wasserstein最优传输距离构建联合概率路径与速度场，捕获节点-边的协同演化，避免启发式路径操纵。"
primary_logic: "通过GraphMRF将图结构转化为具有闭式Bures‑Wasserstein距离的彩色高斯分布，从而能够解析地构造连续平滑的最优传输插值路径和速度场，保证图组件的一体化演化与训练/采样一致性。"
claims:
- "线性插值不能保证图生成中的最优传输位移。"
- "BWFlow在平面图和SBM数据集上相比基线模型获得更高的V.U.N.和更低的A.Ratio。"
- "BW插值相比线性、几何和调和插值在平面图和SBM上表现出明显优势。"
- "BWFlow在少采样步数下（如50步）仍能生成高质量图，而线性流失败。"
---

# Bures-Wasserstein Flow Matching for Graph Generation

> [!tip] 核心洞察
> 通过GraphMRF将图结构转化为具有闭式Bures‑Wasserstein距离的彩色高斯分布，从而能够解析地构造连续平滑的最优传输插值路径和速度场，保证图组件的一体化演化与训练/采样一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于图生成的Bures-Wasserstein流匹配 |
| 英文题名 | Bures-Wasserstein Flow Matching for Graph Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5Bl5qf3fON) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | BWFlow (Bures-Wasserstein Flow Matching) |
| Dataset | Plain Graph Generation (Planar), Small Sampling Steps (Planar, 50 steps), Small Sampling Steps (SBM |

> [!tip] 效果简介
> - Plain Graph Generation (Planar) 上，V.U.N. ↑ 为 84.8 ± 6.44，对比 77.5 ± 8.37 (DeFoG)，变化 +7.3。
> - Plain Graph Generation (Planar) 上，A.Ratio ↓ 为 2.4 ± 0.9，对比 3.5 ± 1.7 (DeFoG)，变化 −1.1。
> - Small Sampling Steps (Planar, 50 steps) 上，V.U.N. ↑ 为 77.0 ± 4.0，对比 22.5 ± 5.0 (DeFoG‑1)，变化 +54.5。

## 概要

图生成任务中，现有扩散模型和流模型在构造概率路径时，通常对节点特征和边进行独立的线性插值。这种做法破坏了图组件之间的相互依赖与协同演化关系，导致训练路径不平滑、速度估计不准确，采样收敛困难。为此，现有方法不得不引入目标引导、时间扭曲等启发式路径操纵技术，增加了模型设计的复杂性。

本文提出 **BWFlow（Bures-Wasserstein Flow Matching）**，一种面向图生成的流匹配框架。其核心思路是将图建模为**马尔可夫随机场（GraphMRF）**，从而将图结构转化为具有闭式Bures-Wasserstein距离的彩色高斯分布。基于这一表示，BWFlow能够解析地构造连续平滑的最优传输插值路径和速度场，保证节点与边的一体化演化，无需额外的路径操纵。

主要贡献可概括为：
- **瓶颈定位**：揭示了线性插值无法保证图生成中最优传输位移的根本问题。
- **方法创新**：利用GraphMRF推导出图分布间的闭式Wasserstein距离，并构造Bures-Wasserstein插值作为流匹配的概率路径。
- **性能验证**：在平面图和SBM数据集上，BWFlow相比最优基线DeFoG在V.U.N.指标上提升7.3个百分点（84.8 vs. 77.5），A.Ratio降低1.1（2.4 vs. 3.5）。在仅50步采样的条件下，BWFlow在平面图上V.U.N.达77.0，而线性流方法DeFoG-1仅22.5，展现出显著的采样效率优势。消融实验进一步表明，关闭所有路径操纵技术后，BW插值在平面图和SBM上均大幅优于线性、几何和调和插值。



### 图生成中的概率路径瓶颈

图生成模型（扩散模型与流匹配模型）的核心任务是学习一个从简单先验分布到复杂数据分布的概率演化路径。现有方法在构造这一路径时，普遍采用**逐组件线性插值**策略：对图的节点特征矩阵 $X$ 和边邻接矩阵 $E$ 分别独立地进行线性混合，即 $X_t = (1-t)X_0 + t X_1$，$E_t = (1-t)E_0 + t E_1$（见 Eq.5）。这一做法虽然实现简单，但存在根本性缺陷。

**瓶颈的因果链条**：图的结构（边）与节点特征之间存在强相互依赖——边的连接模式决定了节点特征的平滑性约束，而节点特征又反过来影响边的语义。线性插值将这两个组件割裂开来独立演化，破坏了图组件之间的协同演化关系。其直接后果是：

1. **训练路径不平滑**：从先验分布到数据分布的插值路径出现尖锐过渡（sharp transitions），导致中间时刻的样本分布偏离真实数据流形，速度估计不准确。
2. **采样收敛困难**：不平滑的路径迫使模型依赖启发式路径操纵技术（目标引导、预测-校正、时间扭曲、随机性注入等）来修正采样轨迹，增加了设计复杂度和不稳定性。
3. **最优传输位移无法保证**：如 Section 2.2 所述，“linearly interpolating nodes/edges with Eq. (5) cannot guarantee the OT displacement in graph generation”——线性插值无法保证图对象在概率空间中沿最优传输测地线移动。

Figure 1 通过概率路径可视化直观展示了这一问题：线性插值路径（Figure 1a）在训练时偏离数据分布，需要额外的路径操纵（Figure 1b）才能勉强接近理想路径，而理想路径应当是平滑且紧贴数据流形的。

### 现有方法的应对与局限

以 DeFoG 为代表的流模型和以 DiGress、DisCo、Cometh 为代表的扩散模型，虽然在图生成任务上取得了进展，但本质上仍沿用逐组件独立建模的范式 $p(G) = p(X)p(E)$。它们通过引入各种启发式路径操纵策略来缓解线性插值的缺陷，而非从根本上解决路径构造问题。这些操纵策略包括：

- **目标引导（target guidance）**：在采样时向目标分布施加额外梯度
- **预测-校正器（predictor-corrector）**：交替进行预测步和校正步
- **时间扭曲（time warping）**：重新分配各时间步的概率质量
- **随机性注入（stochasticity injection）**：向路径添加噪声以增加探索

这些策略虽能部分改善性能，但增加了模型的超参数负担和设计复杂度，且在不同数据集上需要独立调优，缺乏统一的数学基础。

### 本文动机：从最优传输视角统一图演化

本文的核心动机在于：**将图重新建模为一个整体对象，利用最优传输理论构造联合的、平滑的概率演化路径，从而从根本上消除对启发式路径操纵的依赖**。

具体而言，本文借鉴统计关系学习的思想，将图建模为**马尔可夫随机场（GraphMRF）**。在 GraphMRF 框架下，图的节点特征和边结构被统一表示为一个有色高斯分布，其协方差结构由图的拉普拉斯矩阵 $L$ 的伪逆 $\Lambda^\dagger$ 决定（Definition 2）：

$$p(\mathcal{G}; G) = p(\mathcal{X}, \mathcal{E}; X, W) \quad \text{其中} \quad \text{vec}(\mathcal{X}) \sim \mathcal{N}(X, \Lambda^{\dagger}), \quad \Lambda = (\nu I + L) \otimes V^{\top} V$$

这一表示的关键优势在于：两个图分布之间的最优传输距离具有**闭式 Bures-Wasserstein 距离**（Proposition 1），从而可以解析地构造连续平滑的**Bures-Wasserstein 插值路径**（Proposition 2），以及相应的**条件速度场**（Proposition 3）。这条路径天然保证了图组件（节点与边）的一体化协同演化，训练与采样阶段共享同一数学框架，无需额外的路径操纵。

基于此，本文提出 **BWFlow（Bures-Wasserstein Flow Matching）**——一个利用最优概率路径进行图生成的流匹配框架，旨在以数学上更优雅、实践上更稳定的方式解决图生成中的路径构造问题。



## 核心方法与创新机理

现有图生成流模型（如DeFoG）在构造概率路径时，对节点特征和边结构分别进行独立线性插值，这一做法存在根本性缺陷：**线性插值无法保证图生成中的最优传输位移**（Section 2.2），导致训练路径不平滑、存在尖锐过渡，速度估计不准确。为弥补这一缺陷，现有方法不得不引入目标引导、时间扭曲、随机性注入等启发式路径操纵技术（Figure 1b），但这些策略缺乏理论保证，且增加了采样复杂度。

BWFlow的核心创新在于**从根本上改变了概率路径的构造方式**，通过三个紧密关联的changed slots实现突破：

### 1. 图建模粒度：从节点-边独立建模到GraphMRF联合建模

基线方法将图分解为节点特征和边的独立分布 $p(\mathcal{G}) = p(\mathcal{X})p(\mathcal{E})$，忽略了图组件之间的相互依赖关系。BWFlow引入**图马尔可夫随机场（GraphMRF）**（Definition 2），将图建模为联合概率分布：

$$p(\mathcal{G}; G) = p(\mathcal{X}, \mathcal{E}; X, W) \text{ where } \mathcal{E} \sim \delta(W) \text{ and } \text{vec}(\mathcal{X}) \sim \mathcal{N}(X, \Lambda^{\dagger}), \, \Lambda = (\nu I + L) \otimes V^{\top} V$$

其中节点特征服从有色高斯分布，其协方差结构通过图拉普拉斯矩阵 $L$ 显式编码了边结构的影响；边则服从以邻接矩阵 $W$ 为中心的Dirac分布。这一建模方式的关键优势在于：**GraphMRF显式捕获了节点-边依赖关系，同时保留了有色高斯分布的闭式性质**（Remark 1），为后续的解析路径构造奠定了基础。

### 2. 概率路径构造：从独立线性插值到Bures-Wasserstein最优传输插值

基线方法的线性插值路径（Eq.5）对每个节点和每条边独立操作，无法保证图对象整体的最优传输位移。BWFlow利用GraphMRF将图转化为具有闭式Bures-Wasserstein距离的彩色高斯分布（Proposition 1），进而构造沿测地线演化的最优传输插值（Proposition 2）：

$$L_t^{\dagger} = L_0^{1/2}\big((1-t)L_0^{\dagger} + t (L_0^{\dagger/2} L_1^{\dagger} L_0^{\dagger/2})^{1/2}\big)^2 L_0^{1/2}, \quad X_t = (1-t)X_0 + t X_1$$

该插值的核心机制是：节点特征沿欧氏空间线性插值，而图结构通过拉普拉斯伪逆沿Wasserstein测地线协同演化。**这一插值本身即提供了平滑的概率路径，无需额外启发式操纵**（Figure 1a vs. Section 3.2）。消融实验（Table 7）证实：在关闭所有路径操纵技术后，BW插值在平面图上达到84.75%的V.U.N.，而调和插值仅为0.00%；在SBM上BW插值达到58.70%，调和插值仅为5.00%，线性插值和几何插值同样表现不佳。

### 3. 速度估计：从线性条件速度到BW解析速度场

基线方法的条件速度场 $u_t(x_v \mid G_0, G_1) = [X_1]_v - [X_0]_v$ 仅是节点特征的简单差分，无法反映图结构的协同演化。BWFlow基于BW插值推导出解析的条件速度场（Proposition 3），对于连续边分布：

$$v_t(E_t \mid G_0, G_1) = \operatorname{diag}(\dot{L}_t) - \dot{L}_t, \quad v_t(X_t \mid G_0, G_1) = \frac{1}{1-t}(X_1 - X_t)$$

对于离散伯努利边分布，速度场进一步转化为（Eq.14）：

$$v_t(E_t \mid G_1, G_0) = (1 - 2E_t) \frac{\dot{W}_t}{W_t \circ (1 - W_t)}$$

这一速度场的关键特性是**平滑且与插值路径一致**，使得训练时的条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$ 能够准确引导模型学习，采样时即使步数很少也能保持高质量生成。实验表明（Table 3），在仅50个采样步数下，BWFlow在平面图上达到77.0%的V.U.N.，而采用线性流的DeFoG-1仅为22.5%；在SBM上BWFlow达到52.0%，DeFoG-1仅为28.5%。

### 创新协同效应

上述三个changed slots并非孤立改进，而是形成因果链条：GraphMRF联合建模使得Bures-Wasserstein距离的闭式推导成为可能，进而支撑了最优传输插值和解析速度场的构造。这一链条的最终效果是**训练-采样一致性**：训练阶段的速度估计与采样阶段的路径演化遵循同一几何规律，避免了线性流中训练路径与采样路径不匹配的问题。收敛分析（Figure 3c/Figure 8）证实，BW流相比线性流在训练过程中收敛更快，验证了路径质量对优化效率的直接提升。

**需注意的边界条件**：当前推导假设两个图的发射矩阵 $V$ 相同，限制了其对异构图的直接处理能力；路径构造涉及 $O(N^3)$ 的线性代数运算，尽管LSQR近似可在不显著损害生成质量的前提下缓解（Table 6，平面图V.U.N. 85.0 vs. 84.8）。



![[assets/figures/papers/iclr26_0010_5Bl5qf3fON_Bures-Wasserstein_Flow_Matching_for_Graph_Genera/figures/004_Figure_2.jpg]]
*Figure 2: Schematic overview of BWFlow, which consists of: a) Sample the marginal graph condition $G _ { 0 }$ and $G _ { 1 }$ ; b) Convert graphs to $\mathbf { M R F s ; c ) }$ Interpolate to get intermediate points; d) Convert back to get $G _ { t } ; \mathrm { e }$ ) Train velocity based on $G _ { t }$ ; and f) Generate new points with the trained velocity

BWFlow 的整体流程围绕“将图转化为马尔可夫随机场（GraphMRF）→在 MRF 空间沿 Bures-Wasserstein 测地线构造概率路径→训练速度模型→迭代采样”这一核心闭环设计，如图 2 所示。该框架避免了现有流/扩散模型中对节点和边独立线性插值所带来的路径不平滑与速度估计不准确问题（Section 2.2 指出线性插值“cannot guarantee the OT displacement in graph generation”）。

### 模块关系与数据流

整个 pipeline 可分解为六个顺序模块，形成“采样-转换-插值-生成-训练-采样”的闭环：

1. **样本对采样**：从参考分布 $p_0$ 和数据分布 $p_1$ 分别采样图 $G_0$ 与 $G_1$（Figure 2a）。
2. **GraphMRF 转换**：将 $G_0$、$G_1$ 转换为 MRF 表示，提取节点均值矩阵 $X$ 和图 Laplacian $L$（Figure 2b；Algorithm 1）。GraphMRF 将图建模为联合分布 $p(\mathcal{G}; G) = p(\mathcal{X}, \mathcal{E}; X, W)$，其中边服从 Dirac 分布 $\mathcal{E} \sim \delta(W)$，节点特征服从有色高斯 $\text{vec}(\mathcal{X}) \sim \mathcal{N}(X, \Lambda^{\dagger})$，$\Lambda = (\nu I + L) \otimes V^{\top} V$（Definition 2）。这一建模粒度从“节点与边独立”升级为“节点-边联合依赖”，是后续构造协同演化路径的基础。
3. **Bures-Wasserstein 插值**：在 MRF 空间沿 BW 测地线计算中间时间点 $t$ 的插值（Figure 2c）。插值公式由 Proposition 2 给出：
   $$L_t^{\dagger} = L_0^{1/2}\big((1-t)L_0^{\dagger} + t (L_0^{\dagger/2} L_1^{\dagger} L_0^{\dagger/2})^{1/2}\big)^2 L_0^{1/2}, \quad X_t = (1-t)X_0 + t X_1$$
   节点特征 $X_t$ 线性插值，图结构通过 Laplacian 伪逆 $L_t^{\dagger}$ 沿最优传输测地线演化，从而保证图组件的一体化协同演化。
4. **中间图生成**：从插值结果 $L_t^{\dagger}$、$X_t$ 重构出训练所需的中间图 $G_t$（Figure 2d）。
5. **速度模型训练**：基于 $G_t$ 训练 x‑prediction 模型 $f_\theta$（Figure 2e；Algorithm 1）。训练目标为条件流匹配（CFM）的等价形式——通过预测干净图 $G_1$ 的似然来学习速度场：
   $$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{G_1\sim p_1, G_0\sim p_0, t\sim\mathcal{U}, G_t\sim p_{t|0,1}} \big[\log p_{1|t}^{\theta}(G_1 \mid G_t)\big]$$
   速度模型参数化方式见表 4（x‑prediction 方案），连续情形下的条件速度场由 Proposition 3 给出：$v_t(X_t \mid G_0, G_1) = \frac{1}{1-t}(X_1 - X_t)$，$v_t(E_t \mid G_0, G_1) = \operatorname{diag}(\dot{L}_t) - \dot{L}_t$；离散边情形下采用 Eq. (14) 的伯努利速度公式。
6. **迭代采样**：利用训练好的速度模型，从参考分布出发迭代生成新图（Figure 2f；Algorithm 2）。采样过程沿 BW 插值路径推进，无需额外的启发式路径操纵（如目标引导、时间扭曲、随机性注入等），BW 插值本身提供平滑路径。

### 关键设计决策

- **概率路径构造的切换**：从“独立线性插值节点和边”（Eq. 5）切换为“基于 GraphMRF 的 BW 插值”（Proposition 2），这是整个框架的核心因果旋钮。消融实验（Table 7）表明，在关闭所有路径操纵技术后，BW 插值在平面图上的 V.U.N. 达到 84.75，而调和插值仅为 0.00，线性插值也远低于 BW 插值。
- **速度估计的切换**：从线性插值下的条件速度 $u_t = [X_1]_v - [X_0]_v$ 切换为基于 BW 插值的解析条件速度场（Proposition 3 / Eq. 14），保证训练与采样阶段的速度一致性。
- **无需路径操纵**：现有方法（如 DeFoG）需要启发式策略平滑路径（Figure 1b 概念性可视化），而 BWFlow 通过最优传输插值本身提供平滑路径，简化了算法设计并提升了少采样步数下的鲁棒性（Table 3：50 步时 BWFlow 在 Planar 上 V.U.N. 为 77.0，DeFoG‑1 仅为 22.5）。

### 计算开销与近似

BW 插值涉及 Laplacian 伪逆的矩阵运算，带来额外的 $O(N^3)$ 线性代数开销。论文验证了采用 LSQR 近似矩阵求逆不会明显损害生成质量（Table 6：平面图 V.U.N. 85.0 vs 84.8），为实际部署提供了可行的近似方案。



### 3.1 图马尔可夫随机场（GraphMRF）

现有流模型将图生成分解为节点特征与边的独立建模 $p(\mathcal{G}) = p(\mathcal{X}) p(\mathcal{E})$，破坏了图组件之间的协同依赖关系。BWFlow 的核心创新在于将图建模为**图马尔可夫随机场**（GraphMRF），以捕获节点-边的联合演化。

**Definition 2 (GraphMRF)** 将图的联合概率密度定义为：

$$p(\mathcal{G}; G) = p(\mathcal{X}, \mathcal{E}; X, W) = p(\mathcal{X}; X, W) \cdot p(\mathcal{E}; W)$$

其中边服从 Dirac 分布 $\mathcal{E} \sim \delta(W)$，节点特征的向量化形式服从有色高斯分布：

$$\text{vec}(\mathcal{X}) \sim \mathcal{N}(X, \Lambda^{\dagger}), \quad \Lambda = (\nu I + L) \otimes V^{\top} V$$

这里 $L$ 为图拉普拉斯矩阵，$V$ 为节点特征的发射矩阵，$\nu$ 为正则化参数。GraphMRF 的节点特征密度可分解为节点势函数与边势函数：

$$p(\mathcal{X}; \boldsymbol{X}, W) \propto \prod_v \exp\{ - (\nu + d_v) \| V x_v - \mu_v \|^2 \} \prod_{u,v} \exp\{ w_{uv} [ (V x_u - \mu_u)^\top (V x_v - \mu_v) ] \}$$

**关键洞察**：GraphMRF 将离散的图结构转化为连续的有色高斯分布，使得后续可以利用 Bures-Wasserstein 最优传输理论构造具有闭式解的概率路径与速度场，同时保证路径始终位于图流形上。

### 3.2 Bures-Wasserstein 距离与插值

两个图分布 $\mathcal{G}_0, \mathcal{G}_1$ 之间的图 Wasserstein 距离定义为节点与边 Wasserstein 距离之和：

$$d_{BW}(\mathcal{G}_0, \mathcal{G}_1) := \mathcal{W}_c(\eta_{\mathcal{G}_0}, \eta_{\mathcal{G}_1}) = \mathcal{W}_c(\eta_{\mathcal{X}_0}, \eta_{\mathcal{X}_1}) + \mathcal{W}_c(\eta_{\mathcal{E}_0}, \eta_{\mathcal{E}_1})$$

**Proposition 1** 给出了该距离的闭式解——Bures-Wasserstein 距离：

$$d_{BW}(\mathcal{G}_0, \mathcal{G}_1) = \|X_0 - X_1\|_F^2 + \beta \operatorname{trace}\big(L_0^{\dagger} + L_1^{\dagger} - 2(L_0^{\dagger/2} L_1^{\dagger} L_0^{\dagger/2})^{1/2}\big)$$

其中第一项为节点特征的 Frobenius 范数，第二项通过拉普拉斯伪逆的矩阵平方根运算捕获图结构的差异。$\beta$ 为平衡节点与边贡献的超参数。

**Proposition 2** 在此基础上构造了沿 BW 测地线的最优传输插值路径：

$$L_t^{\dagger} = L_0^{1/2}\big((1-t)L_0^{\dagger} + t (L_0^{\dagger/2} L_1^{\dagger} L_0^{\dagger/2})^{1/2}\big)^2 L_0^{1/2}, \quad X_t = (1-t)X_0 + t X_1$$

该插值的核心机制是：节点特征沿欧氏空间线性插值，图结构则通过拉普拉斯伪逆在谱几何空间沿测地线演化。与线性插值 $p_t = (1-t)p_0 + t p_1$ 相比，BW 插值保证了图组件的一体化、协同演化，避免了训练路径中的尖锐过渡。

### 3.3 条件速度场

**Proposition 3** 给出了连续流匹配下的解析条件速度场：

$$v_t(E_t \mid G_0, G_1) = \operatorname{diag}(\dot{L}_t) - \dot{L}_t, \quad v_t(X_t \mid G_0, G_1) = \frac{1}{1-t}(X_1 - X_t)$$

对于离散伯努利边分布，条件速度由 Eq. (14) 给出：

$$v_t(E_t \mid G_1, G_0) = (1 - 2E_t) \frac{\dot{W}_t}{W_t \circ (1 - W_t)}$$

其中 $\dot{W}_t$ 为边概率矩阵沿 BW 插值的时间导数，$\circ$ 表示逐元素乘积。

### 3.4 训练与采样

训练阶段采用 **x-prediction** 参数化（Eq. 4），通过预测干净图 $G_1$ 的似然来等价实现条件流匹配目标：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{G_1\sim p_1, G_0\sim p_0, t\sim\mathcal{U}, G_t\sim p_{t|0,1}} \big[\log p_{1|t}^{\theta}(G_1 \mid G_t)\big]$$

训练流程（Algorithm 1）包含五个关键步骤：(a) 从参考分布和数据分布分别采样 $G_0, G_1$；(b) 将图转换为 GraphMRF 表示；(c) 通过 Proposition 2 计算 BW 插值得到中间点；(d) 转换回图表示得到 $G_t$；(e) 基于 $G_t$ 训练速度模型 $f_\theta$。

采样阶段（Algorithm 2）利用训练好的速度模型，通过 Eq. (12)（连续）或 Eq. (14)（离散）计算条件速度，迭代生成新图：$\hat{G}_{t+dt} \sim \hat{G}_t + v_\theta(\hat{G}_t) dt$。

**方法优势**：与现有流模型需要启发式路径操纵（目标引导、时间扭曲、随机性注入）不同，BW 插值本身提供平滑路径，无需额外操纵即可保证训练/采样一致性。消融实验（Table 7）证实，在关闭所有路径操纵技术下，BW 插值在平面图和 SBM 上的有效性（V.U.N. 84.75）显著优于线性、几何和调和插值（调和插值 V.U.N. 降至 0.00）。



## 实验与关键发现

### 核心实验设置

为公平评估概率路径构造本身的影响，主实验统一关闭了现有流模型的路径操纵技术（目标引导、预测-校正、时间扭曲、随机性注入等），仅比较不同插值路径的生成质量。平面图评估采用累计平均（CAVG）并应用指数滑动平均以稳定结果，每组实验采样 5 次，每次生成 40 个图。

### 平面图生成（主结果）

在 Planar、Tree、SBM 三个基准上，BWFlow 在关闭路径操纵的条件下显著优于现有扩散模型和流模型。关键瓶颈在于：线性插值独立处理节点特征和边，破坏了图组件间的协同演化关系，导致训练路径不平滑、速度估计不准确。

**Table 1 核心数据（CAVG 设置）：**

![[assets/figures/papers/iclr26_0010_5Bl5qf3fON_Bures-Wasserstein_Flow_Matching_for_Graph_Genera/figures/005_Table_1.jpg]]
*Table 1: Plain graph generation performance. The path manipulation methods, e.g. target guidance in Qin et al. (2024) and predictor-corrector in Siraudin et al. (2024), are disabled to purely evaluate the impact of path construction. This table unifies the path distortion designs as in Table 10 and presents the CAVG results. We reproduce the state-of-the-art diffusion/flow model for comparison, while other models evaluated on best-checkpoint results are in the Table 11. The full statistics in Table 13. Table 2: Quantitative experimental results on 3D Molecule Generation with explicit hydrogen*

- **Planar 数据集**：BWFlow 的 V.U.N. 达到 84.8 ± 6.44，比最强流模型 DeFoG（77.5 ± 8.37）提升 7.3 个百分点；A.Ratio 降至 2.4 ± 0.9，显著低于 DeFoG 的 3.5 ± 1.7。这表明 BW 插值生成的图在有效性和图统计量匹配度上均有实质性改善。
- **SBM 数据集**：BWFlow 的 V.U.N. 为 84.5 ± 4.0，与 DeFoG（85.0 ± 3.5）持平，但 A.Ratio 为 2.3 ± 0.5，远低于 DeFoG 的 3.4 ± 0.9——说明 BW 插值生成的图在图统计量分布上更接近真实数据。
- **Tree 数据集**：BWFlow 表现相对较弱，V.U.N. 为 52.0 ± 8.0，低于 DeFoG 的 68.0 ± 5.0。这是一个明确的失败模式，可能源于树图的拉普拉斯谱能量分布与平面图和 SBM 差异较大，BW 插值在该谱结构上的优势未能充分体现。

### 少采样步数下的鲁棒性

**Table 3** 展示了采样步数减少至 50 步时的性能对比。这是检验概率路径平滑度的关键实验——路径越平滑，少步数采样越能保持生成质量。

![[assets/figures/papers/iclr26_0010_5Bl5qf3fON_Bures-Wasserstein_Flow_Matching_for_Graph_Genera/figures/006_Table_3.jpg]]
*Table 3: Model performance in small sampling steps. DeFoG-1 and DeFoG 2 are without and with path manipulation respectively*

- **Planar（50 步）**：BWFlow 的 V.U.N. 为 77.0 ± 4.0，而 DeFoG-1（关闭路径操纵）骤降至 22.5 ± 5.0，差距达 54.5 个百分点。DeFoG-2（开启路径操纵）也仅为 73.5 ± 6.5。这直接验证了 BW 插值本身提供的平滑路径无需额外操纵即可在少步采样下保持高质量。
- **SBM（50 步）**：BWFlow 的 V.U.N. 为 52.0 ± 7.0，DeFoG-1 仅 28.5 ± 11.0，差距 23.5 个百分点。进一步确认了 BW 速度场的平滑性优势。

因果机制：线性插值在少步数下离散化误差大，速度估计不准导致采样发散；BW 插值沿测地线构造连续速度场，离散化容忍度更高。

### 3D 分子生成

**Table 2** 报告了 QM9 数据集（显式氢）上的分子生成结果。BWFlow 在分子稳定性（Mol.Stab.）上达到 97.84，优于 MiDi（约 96.19）和 FlowMol 等 SOTA 模型，提升约 1.65 个百分点。V.U.N. 达到 96.45，同样处于领先水平。

需要注意的是，大分子生成（Guacamol）上 BWFlow 的 Val. 为 98.8，略低于 DeFoG 的 99.0（Table 14），表明 BW 插值在该场景下未带来额外增益，可能需要手动验证是否与数据集规模或谱特性有关。

### 消融研究

**插值方法消融（Table 7）** 是最关键的消融实验，在关闭所有路径操纵技术下比较 BW、线性、几何、调和四种插值：

![[assets/figures/papers/iclr26_0010_5Bl5qf3fON_Bures-Wasserstein_Flow_Matching_for_Graph_Genera/figures/016_Table_7.jpg]]
*Table 7: Ablation study on interpolation methods when probability path manipulation techniques are all disabled. The clustering and orbit ratios in tree graphs are omitted, given that in the training set, the corresponding statistics are 0. The results go over exponential moving average (decay 0.999) for the last 5 checkpoints. The table is produced with Marginal boundary distributions, without time distortion*

- **Planar**：BW 插值的 Validity 为 84.75，线性为 79.50，几何为 80.00，调和插值仅为 0.00。调和插值的完全失败表明，不考虑图结构特性的插值策略会彻底破坏生成质量。
- **SBM**：BW 插值的 Validity 为 58.70，线性为 56.75，几何为 57.50，调和仅为 5.00。BW 插值在两个数据集上均显著优于调和插值，与线性/几何插值相比也有稳定提升。

**收敛分析（Figure 3c / Figure 8）**：BW 流相比线性流在训练过程中收敛更快。Figure 3c 显示 BW 插值在 Planar 数据集上约 60k 步即达到较高准确率，而线性插值需要更多步数。这归因于 BW 插值在训练初期暴露模型于更多样的中间图分布，加速了速度场的学习。

![[assets/figures/papers/iclr26_0010_5Bl5qf3fON_Bures-Wasserstein_Flow_Matching_for_Graph_Genera/figures/009_Figure_3.jpg]]
*Figure 3: (a) The evolution of graph statistics ra-(b) The impact of interpolation (c) Convergence analysis of BW-Flow tio along the probability path. methods on the performance. and flows with linear interpolations. Figure 3: Ablation studies for Bures-Wasserstein Flow Matching*

**LSQR 近似消融（Table 6）**：为缓解 BW 插值中拉普拉斯伪逆计算的 $O(N^3)$ 开销，采用 LSQR 近似矩阵求逆。Planar 上 V.U.N. 为 85.0（精确计算 84.8），Tree 上为 54.0（精确计算 52.0），表明近似不会明显损害生成质量，为大规模图应用提供了可行性路径。

### 概率路径可视化

**Figure 3a** 展示了沿概率路径的图统计量（如聚类系数、轨道比）演化曲线。BW 插值路径相比线性插值更平滑，统计量单调过渡，无尖锐跳变——这是速度估计准确性的直接证据。

**Figure 6** 展示了训练时 Planar、Tree、QM9 三个数据集上的概率路径对比，BW 插值在所有数据集上均表现出更连续的中间分布演化。

**Figure 7** 展示了采样阶段 Planar 和 SBM 上的概率路径重建能力，BWFlow 能更准确地复现从先验到目标分布的过渡过程。

### 失败模式与局限

1. **树图性能不足**：BWFlow 在 Tree 数据集上 V.U.N. 仅 52.0，显著低于 DeFoG 的 68.0。可能原因在于树图的拉普拉斯谱较宽，BW 距离的测地线结构在该谱分布下未能有效捕获生成所需的关键统计特性。需进一步验证谱能量分布对 BW 插值适用性的影响。
2. **大分子场景无增益**：Guacamol 上 Val. 略低于 DeFoG（98.8 vs 99.0），说明 BW 插值在该场景下未超越线性流加路径操纵的组合。
3. **计算开销**：BW 插值涉及 $O(N^3)$ 的线性代数运算（拉普拉斯伪逆），虽可通过 LSQR 近似缓解，但对于大稀疏图仍需进一步优化。
4. **多关系类型未支持**：离散版本仅处理二元边类型，未显式支持多键型（如分子中的单键/双键/三键）的图生成。

### 补充图表

![[assets/figures/papers/iclr26_0010_5Bl5qf3fON_Bures-Wasserstein_Flow_Matching_for_Graph_Genera/figures/003_Figure_1.jpg]]
*Figure 1: Probability path visualization. Since the probability is intractable, the average maximum mean discrepancy ratio (y-axis) of graph statistics between interpolants and the data points is used as a proxy for the probability. Lower means closer to the data distribution (details in Section I.6)*



## 定位与知识库关联

### 在图生成模型中的位置

BWFlow 处于图生成模型中“连续时间流匹配”与“统计关系学习”的交汇点。其直接对话对象是两类主流范式：

**扩散模型（DiGress, DisCo, HSpectre, GruM, Cometh）** 将图生成视为逐步去噪过程，通过估计 score function 逆转扩散过程。这些方法在训练和采样阶段均依赖线性高斯转移核，对节点特征和边独立建模 $p(\mathcal{G}) = p(\mathcal{X})p(\mathcal{E})$，忽略了图组件间的结构依赖。BWFlow 通过 GraphMRF 将这种独立性替换为联合建模，在理论层面更完整地刻画了图的统计特性。

**流模型（DeFoG, MiDi, FlowMol）** 直接构造从先验到数据的概率路径与速度场。DeFoG 作为最直接的可比基线，采用节点和边的独立线性插值（Eq.5），并依赖目标引导、时间扭曲、随机性注入等启发式策略来平滑路径（Figure 1b 概念性展示）。BWFlow 的核心差异在于**路径构造本身即为最优传输测地线**，无需额外操纵即可获得平滑速度场——这一差异在关闭所有路径操纵技术的统一评估中得到严格验证（Table 1, Table 7）。

### 适用边界

**有效场景：**
- **平面图与随机块模型（SBM）**：BWFlow 在 V.U.N. 和 A.Ratio 两个核心指标上显著超越 DeFoG（平面图 V.U.N. 84.8 vs. 77.5，A.Ratio 2.4 vs. 3.5），且路径质量优势随采样步数减少而急剧放大（50 步下平面图 V.U.N. 77.0 vs. 22.5）。这源于 BW 插值在低维结构图上的测地线性质与图统计量演化高度一致。
- **3D 分子生成（QM9 显式氢）**：BWFlow 在分子稳定性（Mol.Stab. 97.84）和有效性（V.U.N. 96.45）上达到或超越 MiDi、FlowMol 等专用分子生成模型，表明 GraphMRF 框架可自然适配分子图的价键约束。
- **少步采样场景**：BW 插值提供的平滑速度场使模型在 50 步甚至更少步数下仍能保持生成质量，而线性流在此条件下急剧退化（Table 3）。

**受限场景：**
- **树图**：BWFlow 在树图上的表现不及平面图和 SBM，可能源于树图的拉普拉斯谱能量分布较宽，BW 插值的测地线假设与树图的结构演化动力学存在偏差。该点需要手动验证具体数值。
- **大分子生成（Guacamol）**：BWFlow 的有效性（Val. 98.8）略低于 DeFoG（99.0），表明在大规模、高多样性的分子库中，BW 插值的优势被削弱，线性流配合路径操纵可能更具竞争力。
- **多关系类型图**：当前 BWFlow 的离散边版本仅处理二元边类型（Eq.14），未显式支持多键型（如单键/双键/三键）的联合生成。

### 核心局限

**计算开销**：BW 插值涉及 $\mathcal{O}(N^3)$ 的线性代数运算（Laplacian 伪逆及矩阵平方根），对于大图构成实际瓶颈。LSQR 近似可缓解此问题（平面图 V.U.N. 85.0 vs. 84.8，Table 6），但近似误差在谱结构复杂的图上可能累积。需注意该开销仅影响路径构造阶段，不改变模型推理复杂度。

**同构发射矩阵假设**：当前推导假设两个图的发射矩阵 $V$ 相同，这限制了 BWFlow 直接处理异构图（节点特征维度或语义空间不同的图）的能力。该假设是获得闭式 BW 距离的关键前提，放松它将需要求解非闭式最优传输问题。

**排列不变性缺失**：BW 距离依赖于图的特定节点排序，未内置排列不变性。在最优传输意义上，理想的距离应自动对齐图节点，但当前框架未解决此问题，可能导致概率路径对节点索引敏感。

### 开放问题

1. **多关系与混合类型扩展**：如何将 BW 插值推广到多关系图（如知识图谱）以及连续/离散混合特征类型，是提升框架通用性的关键。可能的路径包括在乘积空间上定义 BW 距离，或引入关系特定的拉普拉斯算子。

2. **MRF 空间直接参数化**：当前速度模型在原始图空间 $G_t$ 上操作，再通过 x-prediction 间接关联到 MRF 空间。能否直接在 MRF 空间参数化速度场，并利用 KL 散度直接优化概率路径？这将避免图与 MRF 之间的双向转换，可能提升训练效率。

3. **大稀疏图的高效路径构造**：对于节点数 $N > 10^4$ 的稀疏图，$\mathcal{O}(N^3)$ 的路径构造开销不可接受。除 LSQR 外，是否可利用稀疏 Cholesky 分解、随机化 SVD 或图谱粗化策略进一步降低复杂度？

4. **排列不变最优传输**：如何将图匹配或图核方法嵌入 BW 距离计算，实现节点排列的自动对齐？这涉及在 BW 测地线求解之前或之中引入离散最优传输，是一个组合优化与连续优化的交叉问题。

5. **异构图马尔可夫随机场**：是否可将 BWFlow 推广到异构图 MRF（如 H2MN）以处理节点类型不同、边类型多样的复杂图结构？这需要重新定义异构图上的联合高斯分布及其 BW 距离。



## 原文 PDF

![[paperPDFs/ICLR_2026/Bures_Wasserstein_Flow_Matching_for_Graph_Generation.pdf]]

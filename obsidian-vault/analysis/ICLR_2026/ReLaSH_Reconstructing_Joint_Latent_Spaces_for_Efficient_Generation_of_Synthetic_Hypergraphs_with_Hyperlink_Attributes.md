---
title: "ReLaSH: Reconstructing Joint Latent Spaces for Efficient Generation of Synthetic Hypergraphs with Hyperlink Attributes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Efficient_Generation_of_Synthetic_Hypergraphs_with_Hyperlink_Attributes.pdf
project_link: null
code_link: null
aliases:
- ReLaSH
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "ReLaSH 通过以下设计解决该瓶颈：（1）使用基于似然的模型将超链接和属性联合嵌入到低维连续潜在空间；（2）利用分布自由的得分基生成器重构该潜在空间分布；（3）通过已学习的似然模型将采样得到的潜在表示解码回超链接和属性。这样就将高维离散生成问题转化为低维连续潜在空间生成加结构似然映射。"
primary_logic: "核心洞察在于：高维超链接和属性的生成误差可以分解为潜在嵌入的学习误差和潜在分布的学习误差，而通过利用超图的特殊结构构建联合似然模型，整体误差率由低维潜在空间主导，而非原始高维空间，从而规避了维度灾难。"
claims:
- "KL 散度分解（Lemma 1, Theorem 2）表明高维生成误差可归结为低维潜在空间误差（Δ_{(Z_n,B,α,γ)} + Δ_{P_U} + Δ_{\\text{latent-recon}}）。"
- "联合嵌入模型在温和条件下可识别（Theorem 1）且达到一致性误差率 δ_{m,n,p}（Corollary 1）。"
- "在医疗记录生成任务上，ReLaSH-(7,0,2) 的 FED 为 0.532，远优于 Gau-Diff 的 39.731（Table 1）。"
- "消融实验验证了三部分潜在空间（(2,2,2)）比统一潜在空间（(0,6,0)）的 FED 更低（0.1756 vs 0.6432，Table 17）。"
---

# ReLaSH: Reconstructing Joint Latent Spaces for Efficient Generation of Synthetic Hypergraphs with Hyperlink Attributes

> [!tip] 核心洞察
> 核心洞察在于：高维超链接和属性的生成误差可以分解为潜在嵌入的学习误差和潜在分布的学习误差，而通过利用超图的特殊结构构建联合似然模型，整体误差率由低维潜在空间主导，而非原始高维空间，从而规避了维度灾难。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReLaSH：通过重构联合潜在空间高效生成带有超链接属性的合成超图 |
| 英文题名 | ReLaSH: Reconstructing Joint Latent Spaces for Efficient Generation of Synthetic Hypergraphs with Hyperlink Attributes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SG3kS2h44t) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | ReLaSH |
| Dataset | MIMIC-III ICU patient profiles (symptom co-occurrence hypergraph), Co-citation hypergraph generation, Recipe hypergraph generation |

> [!tip] 效果简介
> - MIMIC-III ICU patient profiles (symptom co-occurrence hypergraph) 上，FED 为 0.532 (ReLaSH-(7,0,2))，对比 39.731 (Gau-Diff)，变化 -39.199。
> - Co-citation hypergraph generation 上，Δ_{H_v} 为 1.626 (ReLaSH-(8,8,8))，对比 21.587 (VAE)，变化 -19.961。
> - Recipe hypergraph generation 上，FED 为 0.180 (ReLaSHc-(5,0,16))，对比 varies; observed best among baselines is higher，变化 not directly listed, but ReLaSHc improves substantially。

## 概要

生成带有超链接属性的真实合成超图面临三类根本性挑战：超链接的离散性（节点与超链接的隶属关系为二元变量）、超链接的稀疏性以及超链接与属性形成的混合数据类型（连续数值与类别标签共存）。现有的连续数据生成模型（如扩散模型、GAN）和图生成模型难以直接处理这些特性，而通用表格数据生成方法则完全忽略超图的结构依赖关系，并且在超链接数量增多时遭遇严重的可扩展性问题。

ReLaSH 通过“先嵌入、再生成、后解码”的框架突破上述瓶颈。其核心做法是：首先训练一个基于似然的联合嵌入模型，将高维的超链接存在性（离散）和超链接属性（连续）联合映射到一个低维连续潜在空间；随后在此低维空间内采用分布自由的得分基生成器重构潜在分布；最后借助已学习的似然模型将采样得到的潜在表示随机解码为新的超链接及其属性。这一范式将原本高维、离散且受结构约束的生成问题转化为低维连续潜在空间生成加上一个结构化的似然映射，从而大幅降低生成难度。

该方法的关键理论洞察体现在生成误差的分解上：通过 Lemma 1 和 Theorem 2 证明，真实联合分布与生成联合分布之间的 KL 散度可拆解为嵌入模型估计误差、潜在分布估计误差以及潜在重构误差三部分之和。在温和条件下，嵌入模型具有可识别性（Theorem 1），且该误差率由低维潜在空间的维度主导，而非原始高维数据维度（Corollary 1），因此规避了维度灾难。

在方法定位上，ReLaSH 区别于现有工作的核心设计包括：（1）将联合潜在空间划分为三个块 $(k_1,k_2,k_3)$，分别对应仅与属性相关的变异、属性与超链接共享的变异以及仅与超链接相关的变异，从而精细捕获数据依赖结构；（2）超链接的生成采用 logistic 链路模型，属性生成采用线性–高斯模型，并通过最大化联合似然学习嵌入参数；（3）潜在生成器基于得分匹配与逆向随机微分方程，保持对数据分布的弱假设。与直接在高维拼接向量上进行扩散或对抗训练的方法（如 Gau‑Diff、WGAN）相比，ReLaSH 将超图结构先验显式编码进似然模型，使生成过程更高效、可控。

在医疗记录、共引超图和食谱三个真实超图任务上的实验充分验证了 ReLaSH 的效果。以 MIMIC‑III 患者档案生成为例，ReLaSH‑(7,0,2) 取得的 FED（Fréchet Embedding Distance）为 0.532，而最强基线 Gau‑Diff 的 FED 高达 39.731，性能提升近两个数量级（Table 1）。在共引超图生成任务中，ReLaSH‑(8,8,8) 的 $\Delta_{\mathcal{H}_{\mathrm{v}}}$ 仅为 1.626，远低于 VAE 的 21.587（Table 2）；食谱生成中同样展现出显著优势（Table 3）。消融实验进一步证实，三部分潜在空间的结构至关重要：统一使用单一潜在块 (0,6,0) 的 FED 为 0.6432，而分离为 (2,2,2) 后 FED 降至 0.1756（Table 17）。所提出的 HTT 维度选择算法在 30 次重复中 27 次正确选出最优维度组合（Table 12），表明维度选择具有鲁棒性。

总体而言，ReLaSH 为带有超链接属性的超图合成提供了一种误差可控、结构感知的生成框架，其理论和实验结果为此类任务建立了新的基线。当前版本仍假设节点集合固定，尚不能直接生成全新节点或处理动态超图，未来可向更多模态和更大规模场景扩展。



超图（hypergraph）作为一种推广图结构的数学模型，允许一条超边（超链接）同时连接任意多个节点，从而更自然地刻画许多现实世界中复杂的高阶交互关系。例如，在医疗领域，一份包含多个症状的病人档案可被建模为一条带有多维属性的超链接，属性涵盖疾病持续时间、用药方案等；在学术领域，一组作者的合著或共引关系同样构成超链接，并附有引用量、出版年份等属性。生成具有真实感的合成超图，特别是在超链接级别携带丰富属性的数据，已成为隐私保护、数据增强和科学模拟中的核心需求。

然而，当前生成模型在此任务上面临根本性瓶颈。一方面，超链接的生成需要处理离散组合空间中的稀疏多项式分布：每个超链接对应一个节点子集，其可能状态数为 $2^n-1$（$n$ 为节点总数），而真实数据集中每个超链接通常只连接极少数节点，使得分布高度稀疏。另一方面，超链接与属性之间存在结构依赖，且属性本身可能包含连续变量（如检测数值）和离散类别变量（如疾病类型），形成混合数据类型。现有的连续生成模型（如面向图像或文本的扩散模型、GAN）无法直接生成离散的超链接结构，而面向图的生成方法通常仅处理成对边，未考虑超图的高阶拓扑。虽有一些通用表格数据生成方法（如CTGAN、TabPFGen等），但它们将每个超链接展平为一行特征向量，完全丢弃了超链接变量与属性间的结构关联，且当节点或属性维度较高时迅速遭遇维度灾难。

为突破上述困境，本文提出 **ReLaSH**（Reconstructing Joint Latent Spaces for Efficient Generation of Synthetic Hypergraphs with Hyperlink Attributes）。其核心洞察在于：高维超链接和属性的生成误差可被分解为低维潜在空间的嵌入误差与分布重构误差之和（见 Theorem 2 中的 KL 散度分解）；通过构造可识别的联合似然嵌入模型，将超链接的存在性与属性值映射到低维连续潜在空间，再借助分布自由的基于得分函数的生成器学习该潜在分布，最后通过对偶解码还原超链接与属性，整体误差率由低维潜在空间的维度而非原始高维维度主导，从而巧妙规避了维度灾难。理论分析（Lemma 1, Theorem 2）严格刻画了该分解，并在温和条件下（Theorem 1）保证了嵌入的可识别性与一致性（Corollary 1 中的 $\delta_{m,n,p}$ 边界）。实验表明，在医疗档案、共引网络和食谱生成等多个任务上，ReLaSH 显著优于现有基线方法（如 Gau-Diff 在 FED 指标上从 39.73 降至 0.532，Table 1）。这些证据共同勾勒出一条高效生成高维结构化超图数据的新范式，也为后续的条件生成、动态超图建模等拓展方向提供了理论基础。



## 核心方法与创新机理

现有生成方法（如 Gau-Diff、RealNVP、WGAN、VAE）直接在拼接后的高维超链接‑属性向量上进行扩散或对抗训练，而表格生成方法（如 ForestDiffusion、TabPFGen、CTAB‑GAN）则完全忽略超图的结构依赖。两类基线均面临“维度灾难”与混合数据类型（离散超链接 + 连续属性）带来的建模困难。ReLaSH 通过三项**关键设计变更（changed slots）**系统性地克服了该瓶颈：**（1）生成范式的转变**——从高维原始空间生成变为“低维连续潜在空间生成 + 结构似然解码”；**（2）超图敏感的联合似然建模**——用 logistic 链路捕捉超链接存在性并以共享潜在维度耦合属性；**（3）三部分分解的潜在空间**——将潜在空间显式划分为仅属性、属性‑超链接联合、仅超链接三个子块，从而实现可识别且灵活的表征。

### 1. 生成范式：高维离散 → 低维连续 + 似然解码

**Baseline 做法**：直接将超链接矩阵（$\mathbf{1}_{\{i\in e_j\}}$，规模 $n\times m$）与属性矩阵（$X\in\mathbb{R}^{m\times p}$）展平为 $(n+p)$ 维向量，在其上训练扩散模型或 GAN（如 Gau‑Diff、WGAN）。这种做法迫使生成器在极高的环境维度中学习分布，且需要同时处理离散和连续噪声，导致训练极不稳定，在真实数据上 FED 高达 39.731（Table 1）。

**ReLaSH 做法**：将整个生成过程拆分为三个模块（Figure 2）：
- **联合嵌入模型**（Section 2.3）：通过最大化联合似然，将超链接和属性映射到低维连续潜在变量 $U$、节点嵌入 $Z$ 及回归参数 $B,\alpha,\gamma$ 中；
- **潜在空间重构**（Section 2.4）：在学得的低维潜在分布 $\mathbb{P}_U$ 上训练得分基生成器（score‑based generator），然后通过逆向 SDE 从噪声中采样新嵌入 $\tilde{U}$；
- **解码生成**（Section 2.2）：利用已估计的似然模型（logistic 链路 + 线性‑高斯分布）将 $\tilde{U}$ 随机解码为新的超链接 $\tilde{E}$ 和属性 $\tilde{X}$。

这一转变的**核心洞察**由 **Theorem 2** 截获：真实分布与生成分布之间的 KL 散度可分解为三项误差

$$
d_{\mathrm{KL}}(\mathbb{P}_{(E,X,U)}\parallel\mathbb{P}_{(\tilde{E},\tilde{X},\tilde{U})}) = \Delta_{(\mathcal{Z}_n,B,\alpha,\gamma)\text{-estimation}} + \Delta_{\mathbb{P}_U\text{-estimation}} + \Delta_{\text{latent-reconstruction}},
$$

即高维生成误差由低维潜在空间误差主导，从而**绕开了环境维度的指数级惩罚**。实验上，ReLaSH‑(7,0,2) 在患者档案生成任务上的 FED 仅为 0.532，比 Gau‑Diff 降低两个数量级（Table 1）。

### 2. 超图结构建模：从忽略到逻辑‑高斯联合似然

**Baseline 做法**：表格生成基线（如 CTGAN、TabPFGen）将超图展平为特征矩阵，完全忽略“哪些节点属于同一超链接”这一核心结构信息。它们仅学习边缘属性分布，无法捕捉超链接内部的依赖模式，导致生成超图的结构保真度极低（$\Delta_{\mathcal{H}_v}$ 在共引超图任务上高达 21.587，Table 2）。

**ReLaSH 做法**：引入一个**结构感知的似然模型**（Section 2.3）：
- 超链接存在性建模为 logistic 概率：
  
$$
p_i(u^{(23)}) = \sigma\bigl(u^{(23)\top} z_i + \alpha_i\bigr), \quad i\in[n],
$$

  其中 $u^{(23)}$ 是超链接在共享潜在空间中的表示，$z_i$ 是节点嵌入，$\alpha_i$ 为节点偏置。
- 属性重建采用线性‑高斯模型：
  
$$
x_j = \gamma + B\,u_j^{(12)} + \epsilon_j, \quad \epsilon_j\sim\text{sub‑Gaussian},
$$

  其中 $u_j^{(12)}$ 是超链接的属性相关嵌入。
联合目标函数 $\ell(U, Z, B, \alpha, \gamma) = \ell_H + \lambda \ell_A$（式 3）使超图结构和属性在**同一批潜在变量**的驱动下协调优化，从而自然捕捉超链接组成与其属性之间的依赖。

该模型的**可识别性**由 **Theorem 1** 保证：在温和的满秩条件和稀疏性假设下，联合参数在正交变换意义下唯一确定。相应的**一致性误差率**为

$$
\delta_{m,n,p} = \frac{\sqrt{(m\vee n)\exp(\bar{\alpha}_{m,n})\log(m\vee n) + 4\lambda^2(m\vee p)}}{\sqrt{m}\bigl(\exp(-C_{m,n})\wedge\lambda\bigr)},
$$

且当 $m\asymp n\asymp p$ 时，该误差以 $\log n/n$ 的速度收缩（Corollary 1, Theorem 3），为下游生成提供了理论保障。

### 3. 潜在空间结构：从单一块到三块分解

**Baseline 做法**：典型的变分自编码器或统一嵌入方法将整个潜在空间视为单一实体（例如仅 $(0,6,0)$ 配置），缺乏对属性和超链接不同变异的解耦，易导致特征纠缠与生成质量下降。

**ReLaSH 做法**：将联合潜在空间的维度**显式划分为三个块** $k_1, k_2, k_3$（Section 2.2）：
- $k_1$ 维：**仅作用于属性**的潜在因子（通过 $B$ 回归到 $X$）；
- $k_2$ 维：**同时影响属性与超链接**的公共因子（出现在 $u^{(12)}$ 和 $u^{(23)}$ 中）；
- $k_3$ 维：**仅影响超链接结构**的因子（仅用于 logistic 链路）。

这一设计的动机来源于 **Theorem 1** 的可识别性条件：分离仅属性、公共与仅结构的变化方向，使参数空间具有充分的约束，从而保证 $Z_n, B, \alpha, \gamma$ 的估计一致性。

**消融实验**直接验证了该设计的必要性：
- 在患者档案任务上，三块结构 $(2,2,2)$ 的 FED 为 0.1756，而统一空间 $(0,6,0)$ 的 FED 高达 0.6432（Table 17），表明将属性与结构的潜在变化混杂会严重恶化生成质量。
- 维度选择算法 **HTT** 在 30 次独立重复实验中，以 27/30 的频次正确识别出 $(k_1,k_2,k_3)=(4,4,4)$（Table 12），证明了结构选择的有效性。
- 当固定 $k_1=k_2=k_3$ 时，最优维度 $(4,4,4)$ 在各指标上均优于过小 $(2,2,2)$ 或过大 $(6,6,6)$ 的配置（Table 13），说明三块分解在表达能力和过拟合之间取得了平衡。

综上，ReLaSH 通过“范式迁移 × 结构似然 × 空间解耦”的三重创新，将超图‑属性生成问题转化为可控的低维连续生成任务，并在三项真实任务上均显著超越忽略结构的扩散/表格基线。



![[assets/figures/papers/iclr26_0014_SG3kS2h44t_ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Ef/figures/002_Figure_2.jpg]]
*Figure 2: The general pipeline of ReLaSH*

ReLaSH 针对高维超链接与属性联合生成中的差异性瓶颈（离散性、稀疏性、混合数据类型），设计了一种“嵌入‑重构‑解码”的三阶段流水线。整体思路是：将高维生成问题拆解为低维连续潜在空间的分布学习问题和结构约束的似然映射问题，从而规避直接在高维空间中训练的维度灾难（该洞察由 Theorem 2 的 KL 散度分解显式保证）。

### 1. 流水线总览

正如 **Figure 2** 所示，ReLaSH 依次执行三个核心模块：

1. **联合嵌入模型 (Joint Embedding Model)**  
   输入：训练集中的超图邻接关系 `E`（超链接成员组成）与超链接属性矩阵 `X`。  
   输出：低维联合潜在表示 `U`（按维度划分为三个子块）、节点嵌入 `Z` 以及映射参数 `B, α, γ`。  

   该模块通过最大化联合似然并施加可识别约束，将离散超链接和混合型属性投影到连续空间（Section 2.3; Appendix B.1）。其中超链接存在性由 logistic 链路建模，属性采用线性‑高斯模型，两者共享部分潜在维度，从而在低维表示中显式捕获超图结构依赖。联合优化目标为超链接负对数似然 `ℓ_H` 与属性重构误差 `ℓ_A` 的加权和（Section 2.3 式 (2)）。Theorem 1 给出了嵌入的可识别性条件，Corollary 1 给出了误差率 `δ_{m,n,p}`，为后续生成提供了统计保障。

2. **潜在空间重构（得分基生成器）**  
   输入：第一阶段估计的嵌入 `U` 的经验分布。  
   输出：与 `U` 同分布的新潜在嵌入 `Ũ`。  

   该模块采用分布自由的得分基生成模型（Section 2.4）：先用得分匹配训练得分网络 `s_θ` 以近似真实得分；再通过逆向随机微分方程从高斯噪声中逐步重构潜在样本。由于重构仅发生在低维的 `(k₁+k₂+k₃)` 空间而非原始的 `(n+p)` 维，计算效率和样本效率显著提升。

3. **解码生成超链接与属性**  
   输入：生成的新嵌入 `Ũ` 以及已学习好的参数 `B, γ, α` 和节点嵌入 `Z`。  
   输出：合成超图 `(Ẽ, X̃)`（即新的超链接成员关系和对应的属性）。  

   解码过程直接利用已学习的似然模型（Section 2.2）：对每个潜在向量 `ũ`，通过 logistic 概率 `p_i = σ(ũ^{(23)⊤}z_i + α_i)` 采样节点成员，构成超链接；同时根据 `x̃ = γ + B ũ^{(12)}`（加入 sub‑Gaussian 噪声）生成属性。

### 2. 潜在空间的结构化分解

为避免将所有变化耦合在单一连续块中，ReLaSH 将联合潜在空间分解为三部分 `(k₁, k₂, k₃)`（Section 2.2, Figure 2）：
- `k₁` 维：仅与属性有关。
- `k₂` 维：属性与超链接共享，捕获跨类型依赖。
- `k₃` 维：仅与超链接有关。

这一结构化先验使得优化和生成过程能分离不同来源的变化，消融实验（Table 17）证实了三部分分解显著优于统一潜在空间（FED 0.1756 vs. 0.6432），HTT 维度选择算法在 30 次重复中 27 次正确识别了维度组合（Table 12）。

### 3. 理论支撑

Theorem 2 将整体生成误差（以 KL‑散度衡量）分解为三项：
- 嵌入估计误差 `Δ_{Ζₙ, B, α, γ}`  
- 潜在分布估计误差 `Δ_{P_U}`  
- 潜在重构误差 `Δ_{latent‑reconstruction}`

在温和条件下，高维项由低维嵌入的估计误差主导（Theorem 3），从而实现对环境维度的规避。这一分解揭示了 ReLaSH 流水线的模块化优势：每阶段可被独立改进（如替换更强的生成器或更精确的嵌入模型），而整体误差仍然受低维空间控制。



ReLaSH 将高维超链接与属性生成问题分解为两个阶段：(1) 利用基于似然的模型将离散超链接和连续/类别属性联合嵌入到低维连续潜在空间；(2) 在该潜在空间上运行无分布的得分基生成器学习分布，并通过逆向 SDE 生成新样本。最终，通过已学习的似然映射将生成的低维嵌入解码回超链接和属性。这一设计使得整体生成误差由低维潜在空间主导，避免了维度灾难。以下详述关键模块及其核心公式，并给出理论保障的误差分解形式。

### 1. 联合嵌入模型

嵌入阶段同时建模超链接存在性与属性值。给定包含 $m$ 个超链接、$n$ 个节点、$p$ 维属性的超图，联合潜在空间被划分为三个维度块：$k_1$ 仅与属性相关，$k_2$ 与两者共享，$k_3$ 仅与超链接相关。超链接嵌入记为 $U_m^{(23)} \in \mathbb{R}^{m \times (k_2+k_3)}$，属性相关嵌入记为 $U_m^{(12)} \in \mathbb{R}^{m \times (k_1+k_2)}$，节点嵌入为 $\mathcal{Z}_n \in \mathbb{R}^{n \times (k_2+k_3)}$。

**超链接概率模型**采用 logistic 链路：

$$
p_i(u_j^{(23)}) = \sigma\!\left( u_j^{(23)\top} z_i + \alpha_i \right), \qquad \sigma(v) = \frac{1}{1+e^{-v}}.
$$

其中 $\alpha_i$ 为节点 $i$ 的偏置，描述节点固有的参与倾向。该模型将超链接的非齐次交互压缩为嵌入空间中的内积加偏置的 logit 形式。

基于此，超图结构的负对数似然为：

$$
\ell_H = -\sum_{j=1}^m \sum_{i=1}^n \Big[ \mathbf{1}_{\{i \in e_j\}} \theta_{ji}^H - \log\!\big(1 + \exp(\theta_{ji}^H)\big) \Big],\quad \theta_{ji}^H = u_j^{(23)\top} z_i + \alpha_i.
$$

**属性模型**采用线性‑高斯形式，即假设属性向量条件独立且服从正态分布。相应的重构损失为均方误差：

$$
\ell_A = \sum_{j=1}^m \big\| x_j - \gamma - B\, u_j^{(12)} \big\|_2^2,
$$

其中 $B \in \mathbb{R}^{p \times (k_1+k_2)}$ 为映射矩阵，$\gamma \in \mathbb{R}^p$ 为偏置向量。该形式可视为对属性和嵌入间线性关系的惩罚。

**联合优化目标**为两者的加权和：

$$
\ell(U,Z,B,\alpha,\gamma) = \ell_H + \lambda \,\ell_A,
$$

约束于可识别性区域 $\mathscr{F}(\Theta)$（见 Theorem 1）。通过最小化该联合损失，可得到嵌入以及映射参数的估计值。

### 2. 潜在空间重构生成器

获得估计的嵌入后，ReLaSH 在联合潜在空间上训练一个基于得分的生成模型（score‑based generative model）。具体地，对潜在分布 $p^{\text{e}}(U)$，训练一个得分网络 $\mathbf{s}_{\hat{\theta}}(U, t)$ 以逼近真实得分 $\nabla \log p^{\text{e}}(U)$。训练目标为得分匹配（score matching），在理论分析中假设达到 $\varepsilon_0^2$ 的近似误差（Assumption 3）。生成阶段从高斯先验出发，使用逆向随机微分方程（reverse SDE）逐步采样得到新的潜在嵌入 $\tilde{U}$。

该模块的关键收益在于：直接在高维空间（维度可达 $n+p$）训练生成器极易受维度灾难影响，而 ReLaSH 将生成器局限在低维（通常 $k_1+k_2+k_3 \ll n+p$）连续空间，大幅降低了模型容量和训练难度。

### 3. 解码器

生成器输出新的潜在嵌入 $\tilde{U}$ 后，解码器利用训练好的似然模型随机生成超链接和属性，从而保证生成数据与训练数据服从相同的结构假设：

- **超链接生成**：对每个超链接 $j$，按独立伯努利分布采样节点成员关系：
  
$$
e_{ji} \sim \mathrm{Bernoulli}\big( \sigma(\tilde{u}_j^{(23)\top} z_i + \alpha_i) \big).
$$

- **属性生成**：从条件正态分布采样属性向量：
  
$$
\tilde{x}_j \sim \mathcal{N}\big( \gamma + B\,\tilde{u}_j^{(12)}, \sigma^2 I \big),
$$

  其中 $\sigma^2$ 可在嵌入阶段作为超参数固定或与嵌入一同估计（本文主要在连续属性场景使用该模型，类别属性需额外处理）。

此解码方式不需要额外训练，直接复用嵌入阶段的似然结构，从而保证生成数据与原数据分布之间的一致性。

### 4. 误差分解理论（核心设计的理论支撑）

ReLaSH 的核心动机可通过 KL 散度分解进行形式化（Theorem 2，Section 3）。设真实分布为 $\mathbb{P}_{(E,X,U)}$，生成的联合分布为 $\mathbb{P}_{(\tilde{E},\tilde{X},\tilde{U})}$，则有：

$$
d_{\mathrm{KL}}\big(\mathbb{P}_{(E,X,U)} \,\big\|\, \mathbb{P}_{(\tilde{E},\tilde{X},\tilde{U})}\big) = 
\Delta_{(\mathcal{Z}_n,B,\alpha,\gamma)\text{-estimation}} + \Delta_{\mathbb{P}_U\text{-estimation}} + \Delta_{\text{latent-reconstruction}}.
$$

三项分别对应：(1) 嵌入参数估计误差；(2) 潜在分布估计误差；(3) 得分生成器的重构误差（由得分近似、先验误差和离散化误差组成）。在正则条件及稀疏性假设下，嵌入估计误差的逐维收敛速率为

$$
\frac{1}{(n\vee p)} \Delta_{(\mathcal{Z}_n,B,\alpha,\gamma)\text{-estimation}} = O_p\!\left( \frac{\log(m \vee n)}{\min\{m,n,p\}} \right) \quad (\text{Theorem~3}).
$$

这一结果说明，当样本量增长时，整体生成质量由低维潜在空间而非原始高维空间决定，从而从理论上验证了 ReLaSH 规避维度灾难的设计。详细的误差界推导、可识别性约束以及一致性分析见原文 Appendix A–C。



## 实验与关键发现

### 1. 主结果：ReLaSH 在多种真实超图生成任务上全面超越基线方法

#### 1.1 患者档案生成（MIMIC‑III ICU 症状共现超图）
在基于 MIMIC‑III 的 ICU 患者档案生成任务中，ReLaSH‑(7,0,2) 取得了 **FED = 0.532**，而最强直接生成基线 Gau‑Diff 的 FED 高达 39.731（Table 1）。这意味着 ReLaSH 将 Fréchet 嵌入距离缩小了近两个数量级，充分体现了“低维潜在空间生成 + 结构似然解码”策略在混合离散‑连续高维数据上的巨大优势。在超图结构方差指标 Δℋv 上，ReLaSH‑(7,0,2) 亦远优于所有直接生成模型（例如 Gau‑Diff 的 Δℋv 为 0.0392，ReLaSH 仅 0.0004）。定性方面，Figure 1 展示的合成 ICU 病历表单已具备合理的症状共现模式和属性分布，难以从表面分辨其为合成样本。


![[assets/figures/papers/iclr26_0014_SG3kS2h44t_ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Ef/figures/003_Table_1.jpg]]
*Table 1: Results for patient profile generation. Scales of $\Delta _ { \mathcal { H } _ { \mathrm { v } } } , \Delta _ { \mathcal { X } _ { \mathrm { m } } } \Delta _ { \mathcal { X } _ { \mathrm { v } } }$ , FED, a-FED are 1 $0 ^ { - 4 }$ , 1 $0 ^ { - 3 } , \overline { { 1 0 ^ { - 1 } } }$ , 1 $0 ^ { - 2 }$ , 1 $0 ^ { - 1 }$ , respectively

#### 1.2 共引超图生成
在作者共引超图生成任务中，ReLaSH‑(8,8,8) 将超图结构误差 **Δℋv 降至 1.626**，而 VAE 的 Δℋv 为 21.587（Table 2）。校准版本 ReLaSHc‑(2,7,8) 进一步将 FED 压至 0.947，a‑FED 为 0.706，明显优于所有直接生成基线（Gau‑Diff、RealNVP、WGAN、VAE 的最优 FED 为 2.928）。值得注意的是，即使在属性生成误差 Δ𝒳v 上，ReLaSH 也做到了与直接生成方法可比甚至更优的水平（ReLaSH‑(8,8,8) 的 Δ𝒳v 为 1.832，Gau‑Diff 为 1.824），而后续校准步骤（ReLaSHc）虽可能略微增加属性方差误差，但换来了结构和分布层面的全面领先。


![[assets/figures/papers/iclr26_0014_SG3kS2h44t_ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Ef/figures/004_Table_2.jpg]]
*Table 2: Results for the co-citation hypergraph generation task. Scales of $\Delta _ { \mathcal { H } _ { \mathrm { v } } } , \Delta _ { \mathcal { X } _ { \mathrm { m } } } , \Delta _ { \mathcal { X } _ { \mathrm { v } } }$ , FED, a-FED are 1 $0 ^ { - 3 }$ , 1 $0 ^ { - 2 }$ , 1 $0 ^ { - 1 }$ , 1 $0 ^ { - 1 }$ , 1 $0 ^ { - 1 }$ ， respectively. Distance) used in evaluating visual generation tasks (Heusel et al., 2017), adapted to the hypergraph generation setting. In addition, we report a-FED, a further variant of FED that adjusts for the potential bias of FED when training the embedding machine. Details of these metrics are provided in Appendix B. For each metric, a lower value indicates better performance

#### 1.3 食谱生成
在食谱超图生成任务中，校准版本 **ReLaSHc‑(5,0,16) 取得 FED = 0.180**，远低于直接生成基线（Table 3）。Figure 3 进一步显示了一个合成食谱“Mediterranean Fisherman’s Bean Stew”，该食谱在训练集中不存在任何完全相同的记录，证明方法并非简单记忆，而是能够泛化生成新颖且合理的食谱实例。


![[assets/figures/papers/iclr26_0014_SG3kS2h44t_ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Ef/figures/005_Table_3.jpg]]
*Table 3: Results for recipe generation. Scales of $\Delta _ { \mathcal { H } _ { \mathrm { v } } } , \Delta _ { \mathcal { X } _ { \mathrm { m } } } , \Delta _ { \mathcal { X } _ { \mathrm { v } } }$ FED and a-FED are 1 $0 ^ { - 3 }$ , 1 $\breve { 0 } ^ { - 2 }$ , 1 $0 ^ { - 2 }$ , 1 $0 ^ { - 1 }$ , 1 $0 ^ { - 1 }$ , respectively

**一致性观察**：三个任务显示 ReLaSH 在 FED 和超图结构指标上相对直接生成方法具有绝对优势，同时在校准后能进一步缩小分布距离；属性层面的指标（Δ𝒳m, Δ𝒳v）虽可能受校准影响而轻微上升，但仍保持竞争性，且这一代价远小于结构保真度的收益。

### 2. 消融实验

#### 2.1 潜在空间划分的必要性
显式将联合潜在空间划分为三部分（分别对应纯属性、属性‑超链接联合、纯超链接）是方法成功的关键。Table 17 的实验数据显示：在相同总维度下，三分空间 (k₁,k₂,k₃) = (2,2,2) 的 **FED 仅为 0.1756**，而将全部维度集中为统一潜在块 (0,6,0) 时 FED 急剧上升至 0.6432。这证实了三部分结构既捕获了属性与超链接各自的专属变异，又通过联合块编码其交互，比强行压缩到单一块更能保持数据的真实联合分布。


![[assets/figures/papers/iclr26_0014_SG3kS2h44t_ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Ef/figures/060_Table_17.jpg]]
*Table 17: Result of setting a unified latent space of total dimension k = k _ { 1 } + k _ { 2 } + k _ { 3 } . Each value comes from the mean of 20 repetitions*

#### 2.2 维度选择算法的效力
HTT 算法（基于 Heuristic Threshold Test）用于自动确定最优潜在维度。Table 12 显示在 30 次重复实验中，HTT **正确选择 (k₁,k₂,k₃) = (4,4,4) 的频率为 27/30**，表明该算法在中等噪声条件下具有高可靠性。结合手动固定维度的消融实验（Table 13）：当维度设为 (4,4,4) 时各指标达到最优，减小至 (2,2,2) 或增大至 (6,6,6) 均导致性能下降，印证了维度选择对生成质量的重要性以及 HTT 选择的有效性。


![[assets/figures/papers/iclr26_0014_SG3kS2h44t_ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Ef/figures/055_Table_12.jpg]]
*Table 12: Result of latent dimension selection across 30 repetitions*

#### 2.3 校准步骤的影响
校准版本 ReLaSHc 通过匹配节点度序列进一步校正生成超图的结构偏差。从 Table 2 和 Table 3 可见，校准后 FED 和超图结构指标通常得到显著改善，但 Δ𝒳v 可能略微升高（例如共引超图中 ReLaSHc‑(2,7,8) 的 Δ𝒳v 为 2.102，而最优 Δ𝒳v 基线为 1.824）。这说明校准实质上是一种偏差‑方差权衡：提升结构真实性的同时可能会引入额外的属性解码噪声。

### 3. 公平性讨论与指标解读

应注意直接比较不同方法的 RMSE 可能不公平，因为 RMSE 仅反映训练数据与基准之间的误差，而 ReLaSH 的生成过程还包含“生成数据 vs 训练数据”的额外误差层。论文在 Table 6 中报告了 ReLaSH 与基线的 RMSE 对比（k=6 模拟环境），结果显示 ReLaSH 在均值和协方差恢复上仍表现良好。此外，不同数据集的评估指标量级差异较大（如医疗记录 FED 量级为 10⁻²，共引/食谱为 10⁻¹），读者在横向对比时应注意任务规模与稀疏度差异。

### 4. 失败模式与局限性

理论假设与实际数据之间存在差距，导致以下失败模式或受限场景：

1. **固定节点集的限制**：现有模型假定超图的节点集合固定，无法直接生成含有新节点的超图。这限制了其在动态增长型关系网络中的应用。
2. **属性类型的约束**：属性生成模块当前基于线性‑高斯模型（sub‑Gaussian 噪声），对类别属性或更复杂的分布支持不足。虽然可通过 logistic 模型处理部分离散属性，但未形成通用方案。
3. **HTT 算法的鲁棒性**：尽管在多数实验中工作良好，但当数据极端稀疏或信噪比过低时，HTT 可能给出次优维度选择（Table 12 中仍有 3/30 的失败案例）。
4. **稀疏性与可识别性假设**：理论误差界（Corollary 1）依赖于稀疏性和可识别性条件，并非所有真实超图都满足这些条件，在这些情形下嵌入估计可能不一致，进而影响生成质量。
5. **生成器本身的空间**：当前实现采用标准得分基扩散模型作为潜在空间生成器，尚未探索如流模型、GAN 或更先进的扩散变体是否能在保持效率的同时进一步提升重构质量。

### 5. 理论‑实验连接

Theorem 2 将真实样本与生成样本之间的 KL 散度分解为嵌入估计误差、潜在分布估计误差与潜在重构误差三项，且 Theorem 3 与 Corollary 1 指出嵌入误差随 log(m∨n)/min{m,n,p} 衰减。数值实验（Figure 4–Figure 12）与理论速率的吻合（例如误差随样本量和节点数增加的下降斜率与理论预测一致）为方法的统计可扩展性提供了强有力的支持。这些理论保证解释了大维度差异下 ReLaSH 仍能维持低生成误差的根本机制：低维潜在空间主导了整体误差，从而避免了原始高维空间的维度灾难。



## 定位与知识库关联

ReLaSH 瞄准同时生成超链接（离散、稀疏）与超链接属性（混合连续-类别型）这一此前未充分解决的数据生成难题，提出“嵌入-生成-解码”双阶段框架，在生成模型谱系中处于表格生成、图生成与基于扩散/似然的深度生成方法的交叉地带。相比直接将超图数据扁平化为独立特征的表格生成模型（CTAB‑GAN, CTGAN, TabPFGen, ForestDiffusion），其核心差异在于显式建模超图结构而非把超链接参与关系当作一组无关维度处理，从而避免因忽略超边高阶共现而导致生成性能严重退化。例如在患者档案生成任务上，直接在高维拼接空间训练扩散模型的 Gau‑Diff 的 FED 高达 39.731，而 ReLaSH‑(7,0,2) 仅为 0.532（Table 1，置信度 1.0）。同样，其他通用生成模型（RealNVP, WGAN, VAE）在相同任务上均表现不佳（Table 1），根源在于它们试图直接学习 (n+p) 维联合分布，遭遇维度灾难与结构化稀疏性。

**与基线方法的本质差异**。ReLaSH 通过三处关键设计变更，将生成问题从高维原始空间转移到低维结构化潜在空间：

1. **生成范式变更**：基线方法直接生成拼接后的高维向量；ReLaSH 先通过基于似然的嵌入模型将超链接与属性联合映射到 k₁+k₂+k₃ 维连续潜在空间（Section 2.2, Figure 2），再用分布自由的得分基生成器重建该潜在分布，最后解码回超链接与属性（Section 2.2 → 2.4）。这一变动使得生成误差的主导项由潜在空间维度而非原始维度控制：KL 散度可分解为 Δ_{(Zₙ,B,α,γ)-estimation} + Δ_{P_U-estimation} + Δ_{latent-recon}（Theorem 2, Section 3），其中前两项受低维嵌入影响，而原始高维离散误差通过似然映射被边际化。理论分析进一步表明，当 m ≍ n ≍ p 时，嵌入估计造成的每维误差速率为 Oₚ(log(m∨n)/min{m,n,p})（Theorem 3），规避了高维原始空间下的样本复杂度灾难。

2. **超图建模变更**：基线通常忽略超图结构，将超链接视为独立二进制特征。ReLaSH 采用 logistic 似然对超链接存在性建模（pᵢ(u^{(23)}) = σ(u^{(23)⊤}zᵢ + αᵢ)，Section 2.3），并通过联合优化超图负对数似然 ℓₕ 与属性重构损失 ℓₐ（Joint Loss, Section 2.3）显式捕获节点‑超链接‑属性三者的依赖。在共引超图生成实验中，这种结构感知使 ReLaSH‑(8,8,8) 的 Δₕᵥ 降至 1.626，而最佳基线 VAE 为 21.587（Table 2，置信度 1.0），表明建模超边关系对超边计数分布保真度至关重要。

3. **潜在空间结构变更**：与仅使用单一潜空间的 VAE 等模型不同，ReLaSH 将潜在空间分解为 (k₁, k₂, k₃) 三块，分别对应仅属性变化、属性‑超链接联合变化、仅超链接结构变化（Section 2.2, Theorem 1）。消融实验（Table 17）中，总维数固定为 6 时，(2,2,2) 配置的 FED 为 0.1756，而统一块配置 (0,6,0) 的 FED 为 0.6432（置信度 0.95），表明解耦不同来源的潜在变化有助于更精准地重建联合分布。HTT 维度选择算法在 30 次重复中有 27 次正确选出 (4,4,4)，为实际应用提供了可靠的自动维度配置（Table 12，置信度 0.95）。

**适用边界**。ReLaSH 的强假设决定了其最适合的数据特征：节点集合固定、超链接稀疏但数目足够、属性主要为连续型且满足 sub‑Gaussian 噪声条件。其理论保障建立在可识别性条件（Theorem 1）以及一定的稀疏上界（Corollary 1 中 δ_{m,n,p} 包含 e^{ᾱ_{m,n}} 项）之上，因此若超图过于稠密或真实分布偏离线性‑logistic 模型，嵌入偏差将通过 Δ_{(Zₙ,B,α,γ)-estimation} 项放大最终生成误差。此外，当前版本不支持新增节点，对类别型属性需单独设计似然模型，这构成了明确的功能边界。在对比校验方法（ReLaSHc）时需注意公平性：RMSE 仅反映训练数据与基准之间的误差，而 ReLaSH 需额外承担生成数据与训练数据之间的分歧，因此直接比较 RMSE 可能不公允。

**局限与失败模式**。
1. 节点集固定，无法生成包含新节点的超图，限制其在演化超图或零样本场景的应用。
2. 超链接属性建模目前仅通过线性‑高斯处理连续属性，类别型属性需要特殊化（如 logistic 链路），统一性不足。
3. HTT 维度选择虽在多数实验有效（30 次中 27 次正确），但在极端数据条件下可能失效，导致嵌入维度选择偏误并损害生成质量。
4. 理论证明依赖的可识别性条件与稀疏性假设并非所有真实数据集都满足；当假设违背时，式 (3) 的约束优化可能无法达到相合估计，进而将偏差传入后续生成步骤。
5. 当前实现中潜在空间重构采用标准扩散模型，尚未与更先进的生成模型（如流、一致性模型）进行系统对比和优化（limitation 5）。

**开放问题与后续方向**。上述局限与需求引出以下值得探索的方向：
* 将 ReLaSH 扩展至动态/时序超图、加权超链接以及文本、图像等多模态属性（open question 1）；
* 引入条件生成机制，允许以部分节点、属性或结构约束为条件定向合成，支撑反事实推断和目标模拟（open question 2）；
* 对生成结果进行不确定性量化，并给出更紧的离散化误差界，完善理论保真度分析（open question 3）；
* 提升可扩展性以处理百万级节点和超链接的大规模超图（open question 4）；
* 开发超越 FED 与平均 RMSE、能全面刻画超图拓扑与属性联合保真度的评估指标（open question 5）。

这些工作有望将“结构感知的联合潜在空间重构”范式从当前固定节点、连续属性的有限场景推广到更广泛的复杂多模态超图生成任务中。



## 原文 PDF

![[paperPDFs/ICLR_2026/ReLaSH_Reconstructing_Joint_Latent_Spaces_for_Efficient_Generation_of_Synthetic_Hypergraphs_with_Hyperlink_Attributes.pdf]]

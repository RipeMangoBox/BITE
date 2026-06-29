---
title: Unsupervised Learning of Robust Spectral Shape Matching
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Unsupervised_Learning_of_Robust_Spectral_Shape_Matching.pdf
project_link: null
code_link: "https://github.com/dongliangcao/Unsupervised-Learning-of-Robust-Spectral-Shape-Matching"
aliases:
- URSSM
- ULRSSM
tags:
- SIGGRAPH_2023
- topic/other_unclear
core_operator: 引入可微耦合损失（L_couple），强制从特征相似性导出的软逐点映射与泛函图保持一致；同时，在推理时采用测试时自适应（Test-Time Adaptation）联合优化泛函图和逐点映射，使网络直接输出高质量的点对应，摆脱后处理依赖。
primary_logic: 通过耦合泛函图与逐点映射的训练和自适应，让网络学习到能够直接生成精确点对应的一致性特征，从根本上解决了传统两阶段流程中泛函图与点对应脱节的问题，大幅提升了对非等距、部分形状及拓扑噪声的鲁棒性。
claims:
- 提出新的无监督耦合损失，将泛函图与逐点映射相关联，从而直接获得逐点映射，无需任何后处理。
- 提出测试时自适应策略，在推理过程中同时优化泛函图和对应的逐点映射。
- 方法直接强制泛函图与逐点映射相关联，并同时优化两者。
- 关键见解：现有方法仅优化泛函图并依赖后处理，导致次优结果。
---

# Unsupervised Learning of Robust Spectral Shape Matching

> [!tip] 核心洞察
> 通过耦合泛函图与逐点映射的训练和自适应，让网络学习到能够直接生成精确点对应的一致性特征，从根本上解决了传统两阶段流程中泛函图与点对应脱节的问题，大幅提升了对非等距、部分形状及拓扑噪声的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 鲁棒谱形状匹配的无监督学习 |
| 英文题名 | Unsupervised Learning of Robust Spectral Shape Matching |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://dongliangcao.github.io/urssm/) · [Code](https://github.com/dongliangcao/Unsupervised-Learning-of-Robust-Spectral-Shape-Matching) |
| Topic | #topic/other_unclear |
| Method | Unsupervised Robust Spectral Shape Matching |
| Dataset | SHREC'16 CUTS, SHREC'16 CUTS → HOLES, SHREC'16 HOLES, TOPKIDS |

> [!tip] 效果简介
> - SHREC'16 CUTS (partial) 上，Mean geodesic error 3.3 vs 8.4 (ConsistFMaps) (-5.1)。
> - SHREC'16 CUTS → HOLES (generalization) 上，Mean geodesic error 13.7 vs 23.7 (ConsistFMaps) (-10.0)。
> - SHREC'16 HOLES (partial) 上，Mean geodesic error 9.1 vs 17.9 (ConsistFMaps) (-8.8)。

## 概要

现有深度泛函图方法存在一个根本性瓶颈：训练时仅优化泛函图，推理时依赖不可微的后处理（如ZoomOut）恢复逐点映射。这种两阶段流程割裂了泛函图与点对应之间的内在耦合，导致在非等距变形、部分形状和拓扑噪声等挑战场景下性能次优，且对谱分辨率敏感。

本文提出首个无监督鲁棒谱形状匹配方法，核心创新包括两方面。其一，引入可微耦合损失 $L_{\mathrm{couple}}$，强制从特征相似性导出的软逐点映射与泛函图保持一致，使网络在训练阶段即学习到能够直接生成精确点对应的一致性特征。其二，提出测试时自适应策略，在推理过程中联合优化泛函图和逐点映射，摆脱对后处理的依赖。

实验表明，该方法在近等距、非等距、部分形状及拓扑噪声等多种基准上大幅超越先前最优方法，甚至优于近期有监督方法。例如，在SHREC'16 CUTS部分匹配上测地误差从8.4降至3.3，在TOPKIDS拓扑噪声数据上从>20降至9.2。方法定位为完全无监督的谱域形状匹配框架，是首个同时处理非等距和部分形状的无监督学习方法。

## 核心方法与创新机理

### 问题瓶颈：泛函图与逐点映射的脱节

现有深度泛函图方法（如 **FMNet** (Litany et al., 2017a)、**Roufosse et al.** (2019)、**ConsistFMaps** (Cao and Bernard, 2022)）遵循一个共同的两阶段范式：首先训练特征提取器以优化泛函图 $C_{MN}$ 的结构正则化损失 $\mathcal{L}_{\mathrm{fmap}}$，然后在推理阶段依赖不可微的后处理技术（如最近邻搜索或 ZoomOut 迭代优化）从泛函图恢复逐点对应。这一流程的根本缺陷在于：泛函图的优化目标与最终逐点映射的质量之间缺乏直接的梯度通路，导致特征学习无法感知逐点对应的需求。在非等距变形、部分形状和拓扑噪声等挑战性场景下，这种脱节使得泛函图虽在谱域满足结构约束，却无法转化为高质量的顶点级对应。

### 核心创新：可微耦合与端到端一致性

本文的核心洞察在于：泛函图 $C_{MN}$ 与逐点映射 $\Pi_{NM}$ 之间存在严格的数学约束关系——有效的泛函图必须能够由某个逐点置换矩阵通过谱基变换生成。形式化地，泛函图的可行域应被约束为：

$$\left\{ C_{MN} \mid \exists \Pi_{NM}, \mathrm{s.t.}\ C_{MN} = \Phi_N^{\dagger} \Pi_{NM} \Phi_M \right\}$$

其中 $\Phi_M, \Phi_N$ 为两个形状的谱基矩阵，$\Phi_N^{\dagger}$ 为 $\Phi_N$ 的 Moore-Penrose 伪逆。现有方法在优化 $C_{MN}$ 时完全忽略了这一约束，导致泛函图与逐点映射的生成过程相互独立。

本文提出两项关键机制来弥合这一鸿沟：

1. **可微耦合损失（Coupling Loss）**：在训练阶段引入 $L_{\mathrm{couple}}$，强制泛函图与从特征相似性导出的软逐点映射保持一致。
2. **测试时自适应（Test-Time Adaptation）**：在推理阶段对每个测试形状对进行迭代优化，联合调整逐点映射和泛函图，进一步收窄两者之间的残差。

### 方法框架与模块顺序

整体框架（Fig. 3）包含以下模块，按训练和推理两条路径组织：

![[assets/figures/papers/paper_list_l9_https_dongliangcao_github_io_urssm/figures/005_Figure_3.jpg]]
*Figure 3: Overview of our unsupervised robust spectral shape matching method. First, the feature extractor with shared weights Θ takes a pair of shapes M and N and extracts vertex-wise features*

**训练路径**：
1. **特征提取器**（Siamese 共享权重网络）为形状对 $\mathcal{M}, \mathcal{N}$ 的每个顶点提取 $d$ 维特征 $F_M, F_N$。
2. **泛函图求解器**（可微但不可训练）基于特征和谱基计算双向泛函图 $C_{MN}, C_{NM}$。
3. **可微逐点映射模块**通过特征相似度的 softmax 生成软对应矩阵 $\Pi_{NM}$。
4. **耦合损失**度量 $C_{MN}$ 与 $\Pi_{NM}$ 经谱基变换后的一致性，与结构正则化损失 $\mathcal{L}_{\mathrm{fmap}}$ 联合训练特征提取器。

**推理路径**：
1. 特征提取器直接输出特征 $F_M, F_N$。
2. 通过特征空间最近邻（或谱最近邻）直接获得离散逐点映射 $\Pi_{NM}$，**无需泛函图求解器和任何后处理**。
3. 可选地，通过测试时自适应对单个形状对迭代优化总损失，更新特征提取器参数，联合优化逐点映射与泛函图。

### Changed Slot 1：逐点映射计算——从后处理到可微直接输出

**Baseline 做法**：两阶段流程——先求解泛函图 $C_{MN}$，再通过不可微后处理（如 ZoomOut）恢复逐点映射。特征提取器在训练时从未感知逐点对应的质量。

**本文做法**：训练时通过特征相似度的 softmax 直接计算可微逐点软映射：

$$\Pi_{NM} = \mathrm{Softmax}\left(F_N F_M^T / \tau\right)$$

其中 $\tau$ 为温度参数，控制软分配的锐度。该软映射矩阵 $\Pi_{NM}$ 是连续、可微的，允许梯度从逐点对应质量回传至特征提取器。推理时，直接从特征空间最近邻得到硬对应：

$$\Pi_{NM} = \mathrm{NN}(F_N, F_M)$$

对于近等距形状，还可使用谱最近邻变体 $\Pi_{NM}^{\mathrm{iso}} = \mathrm{NN}(\Phi_N \Phi_N^{\dagger} \Pi_{NM} \Phi_M, \Phi_M)$ 进行低通滤波，保留低频一致性。

**因果链路**：软映射的可微性 → 耦合损失可计算 → 特征学习感知逐点对应 → 推理时无需后处理即可直接输出高质量对应。

### Changed Slot 2：损失函数——从纯泛函图正则化到耦合一致性

**Baseline 做法**：仅使用泛函图结构正则化损失 $\mathcal{L}_{\mathrm{fmap}} = \lambda_{\mathrm{bij}} \mathcal{L}_{\mathrm{bij}} + \lambda_{\mathrm{orth}} \mathcal{L}_{\mathrm{orth}}$，其中：

- 双向性正则化：$L_{\mathrm{bij}} = \|C_{MN} C_{NM} - I\|_F^2 + \|C_{NM} C_{MN} - I\|_F^2$
- 正交性正则化：$L_{\mathrm{orth}} = \|C_{MN}^{\top} C_{MN} - I\|_F^2 + \|C_{NM}^{\top} C_{NM} - I\|_F^2$

这些损失仅约束泛函图在谱域的性质，与逐点映射无关。

**本文做法**：总损失扩展为：

$$L_{\mathrm{total}} = L_{\mathrm{fmap}} + \lambda_{\mathrm{couple}} L_{\mathrm{couple}}$$

其中耦合损失定义为：

$$L_{\mathrm{couple}} = \left\| C_{MN} - \Phi_N^{\dagger} \Pi_{NM} \Phi_M \right\|_F^2$$

该损失直接度量泛函图与软逐点映射经谱基变换后的 Frobenius 范数差异。其核心作用在于：当 $L_{\mathrm{couple}}$ 被最小化时，$C_{MN}$ 被强制约束在由 $\Pi_{NM}$ 生成的可行子空间内，反之 $\Pi_{NM}$ 也被迫与谱域最优的 $C_{MN}$ 保持一致。

**因果链路**：耦合损失 → 泛函图与逐点映射双向约束 → 特征必须同时满足谱域结构正则化和空间域对应一致性 → 特征更具判别力和鲁棒性。

### Changed Slot 3：推理策略——测试时自适应联合优化

**Baseline 做法**：固定特征提取器，计算泛函图后转后处理，推理阶段无任何优化。

**本文做法**：提出测试时自适应策略，对单个测试形状对 $\mathcal{M}, \mathcal{N}$ 迭代最小化 $L_{\mathrm{total}}$，更新特征提取器参数 $\Theta$。对于非等距匹配，额外引入 Dirichlet 能量平滑项：

$$L_{\mathrm{dirichlet}} = \| \Pi_{NM} X_{\mathcal{M}} \|_{L_N}^2$$

其中 $X_{\mathcal{M}}$ 为形状 $\mathcal{M}$ 的顶点坐标，$\|\cdot\|_{L_N}$ 为形状 $\mathcal{N}$ 上的 Laplace-Beltrami 算子诱导的范数。该平滑项鼓励相邻顶点被匹配到相邻顶点，对非等距变形提供几何正则化。

测试时自适应的关键设计：
- 在推理时完全放弃泛函图求解器，直接使用特征相似性获得点映射。
- 自适应过程中同时优化 $L_{\mathrm{fmap}}$ 和 $L_{\mathrm{couple}}$，使泛函图与逐点映射相互收窄。
- 仅需少量迭代步数（通常 10-20 步），计算开销可控。

**因果链路**：测试时自适应 → 针对特定形状对微调特征 → 泛函图与逐点映射残差进一步缩小 → 匹配精度提升，尤其在分布外形状对上。

### 关键公式变量含义与模块间因果关系

**谱基与泛函图**：$\Phi_M \in \mathbb{R}^{n_M \times k}$ 为形状 $\mathcal{M}$ 的前 $k$ 个 Laplace-Beltrami 特征向量构成的谱基矩阵。泛函图 $C_{MN} \in \mathbb{R}^{k \times k}$ 将函数从 $\mathcal{M}$ 的谱系数映射到 $\mathcal{N}$ 的谱系数。

**特征提取器**：DiffusionNet 架构，输入为形状的几何信号（如 HKS、WKS），输出为每顶点 $d$ 维特征。Siamese 权重共享确保特征空间的一致性。

**模块间因果链**：
1. 特征提取器 $\Theta$ → 特征 $F_M, F_N$ → 软映射 $\Pi_{NM}$（Eq. 6）→ 耦合损失 $L_{\mathrm{couple}}$（Eq. 8）
2. 特征 $F_M, F_N$ + 谱基 → 泛函图 $C_{MN}$（Eq. 1）→ 结构损失 $L_{\mathrm{fmap}}$（Eq. 2）
3. $L_{\mathrm{couple}}$ 与 $L_{\mathrm{fmap}}$ 联合 → 梯度回传至 $\Theta$ → 特征同时满足谱域和空间域约束
4. 训练后 $\Theta$ → 推理时直接 NN → $\Pi_{NM}$（Eq. 11）→ 无后处理输出
5. 测试时自适应 → 对 $L_{\mathrm{total}} + L_{\mathrm{dirichlet}}$ 迭代优化 $\Theta$ → $\Pi_{NM}$ 与 $C_{MN}$ 联合精化

### 软映射 vs 硬映射的设计考量

本文采用 softmax 生成的软对应矩阵 $\Pi_{NM}$ 而非硬置换矩阵，其优势在于：
- 软映射提供了连续的梯度信号，允许特征提取器感知匹配的“不确定性”。
- 在非等距和部分形状场景下，一对多或多对一的软对应为优化提供了更大的灵活性。
- 消融实验证实：用 Gumbel-Softmax 硬映射替代软映射后，SMAL 数据集上误差从 3.9 升至 4.4，验证了软映射的优越性。

### 训练与推理路径总结

| 阶段 | 泛函图求解器 | 逐点映射来源 | 优化目标 | 后处理 |
|------|-------------|-------------|---------|--------|
| 训练 | 使用（可微） | 特征 softmax（可微） | $L_{\mathrm{fmap}} + \lambda_{\mathrm{couple}} L_{\mathrm{couple}}$ | 无 |
| 推理（无自适应） | 不使用 | 特征 NN（硬对应） | 无优化 | 无 |
| 推理（测试时自适应） | 不使用 | 特征 NN → 迭代更新 | $L_{\mathrm{total}} + L_{\mathrm{dirichlet}}$ | 无 |

这一设计实现了从“训练优化泛函图 + 推理后处理恢复点映射”到“训练联合优化 + 推理直接输出点映射”的根本转变，消除了传统两阶段流程中泛函图与逐点映射脱节的系统性缺陷。

![[assets/figures/papers/paper_list_l9_https_dongliangcao_github_io_urssm/figures/004_Figure_2.jpg]]
*Figure 2: Common pipeline of deep functional map methods. First, the feature extractor computes per-vertex features for each of the two input shapes. Then the functional map solver is used to compute the (bidirectional) functional map based on the extracted features. To train the feature extractor, structural regularisation is imposed on the computed functional maps*

## 实验与关键发现

### 近等距匹配与跨数据集泛化

在标准近等距基准上，本文方法以完全无监督的方式取得了极具竞争力的结果。在 FAUST 数据集上，**本文方法**的测地误差为 **1.6**，优于大多数监督方法（如 FMNet 的 2.4、GeomFMaps 的 1.9），仅略逊于使用 ZoomOut 后处理的最优监督方法。在 SCAPE 和 SHREC'19 数据集上，本文方法分别取得 **2.2** 和 **5.7** 的测地误差，显著优于同期无监督方法 ConsistFMaps（2.7 和 8.0）。更关键的是，**跨数据集泛化**场景下本文方法的优势更加突出：在 FAUST 上训练、SCAPE 上测试时误差仅 2.2，而 GeomFMaps 为 3.1，DUO-FMNet 为 4.0，表明耦合训练学到的特征具有更强的泛化能力。

### 非等距匹配

SMAL 数据集（不同动物类别间的非等距匹配）是检验方法鲁棒性的核心 benchmark。本文方法取得 **3.9**（×100）的测地误差，大幅超越此前最优的无监督方法（ConsistFMaps 约 8.0），甚至优于多数监督方法（GeomFMaps 约 5.0，DUO-FMNet 约 5.5）。这一结果表明，耦合损失与测试时自适应的联合机制使得网络即使在严重非等距变形下也能学习到一致的对应关系，而不依赖后处理来弥合泛函图与点映射之间的鸿沟。

### 部分形状匹配

在 SHREC'16 CUTS 基准上，本文方法取得 **3.3** 的测地误差（Table 7），而此前最优的无监督方法 ConsistFMaps 为 8.4，提升幅度达 **-5.1**。在更具挑战性的 HOLES 子集上，本文方法为 **9.1**（ConsistFMaps 为 17.9，提升 **-8.8**）。值得关注的是，在 CUTS 训练、HOLES 测试的泛化设定下，本文方法取得 **13.7**，而 ConsistFMaps 高达 23.7（提升 **-10.0**），验证了方法对未见部分形状类型的强泛化能力。这一性能甚至超越了有监督的 DPFM（专门针对部分匹配设计），标志着无监督方法首次在部分匹配上弥合了与监督方法之间的巨大性能差距。

![[assets/figures/papers/paper_list_l9_https_dongliangcao_github_io_urssm/figures/019_Table_7.jpg]]
*Table 7: Partial shape matching on SHREC’16. The numbers in parentheses show refined results using the indicated post-processing technique. Our method is the first unsupervised approach that bridges the huge performance gap between supervised and unsupervised methods*

### 拓扑噪声鲁棒性

在 TOPKIDS 数据集（含拓扑噪声的等距形状对）上，本文方法取得 **9.2**（×100）的测地误差，而此前最优方法（包括监督和无监督）的误差普遍超过 20。这一显著优势源于耦合损失对泛函图与点映射一致性的强制约束，使得网络不会因拓扑变化产生的虚假谱对应而产生错误匹配。

### 各向异性网格鲁棒性

在 FAUST 和 SCAPE 的原始网格与重网格化版本之间进行匹配时，本文方法在大多数设置下均优于此前最优方法。例如，FAUST 原始↔重网格化场景下，本文方法误差为 **2.0**，而 GeomFMaps 为 2.8，ConsistFMaps 为 2.5。这表明耦合训练使特征对网格采样的变化不敏感。

### 关键消融实验

Table 8 在 SMAL 数据集上系统拆解了各组件的贡献：

![[assets/figures/papers/paper_list_l9_https_dongliangcao_github_io_urssm/figures/020_Table_8.jpg]]
*Table 8: Ablation study on SMAL. The first row shows the network trained only with*

- **移除耦合损失 L_couple**：仅使用 L_fmap 训练，测地误差从 3.9 飙升至 **10.3**，验证了耦合损失是方法性能的核心支柱。
- **不使用测试时自适应**：误差升至 **5.5**，表明推理阶段的联合优化可进一步收窄泛函图与点映射之间的残差。
- **移除 Dirichlet 平滑项**：在测试时自适应中去除 L_dirichlet，误差升至 **4.3**，说明平滑先验对非等距匹配有益。
- **用 Gumbel 硬映射替代软映射**：误差升至 **4.4**，证实软映射提供的连续松弛为梯度优化提供了更大的灵活性。
- **作为公理化方法独立优化**：若对每对形状独立优化（无集体训练），误差高达 **43.1**（Table 9），这从根本上验证了无监督集体训练对学习可泛化特征的必要性。

![[assets/figures/papers/paper_list_l9_https_dongliangcao_github_io_urssm/figures/024_Table_9.jpg]]
*Table 9: Non-isometric matching on SMAL. We compare our unsupervised training strategy to the individual optimisation strategy. We observe a large performance drop when using our method as an axiomatic approach*

### 谱分辨率鲁棒性

与 GeomFMaps 的对比实验（Fig. 13 right）表明，本文方法对谱基数量（谱分辨率）的选择高度鲁棒：在不同谱分辨率下性能保持稳定。而 GeomFMaps 在增加谱基数量时性能出现明显波动甚至下降，暴露了其两阶段流程对谱表示的敏感性。

![[assets/figures/papers/paper_list_l9_https_dongliangcao_github_io_urssm/figures/021_Figure_13.jpg]]
*Figure 13: Inference time and robustness to spectral resolution. We compare our method to the state-of-the-art supervised method GeomFMaps [Donati et al. 2020] (with and without ZoomOut [Melzi et al. 2019b]). Left: Runtime comparison with a different number of vertices. Compared to GeomFMaps, our method requires more computational time due to the choice of a larger number of eigenfunctions (200 versus 30). Nevertheless, for shapes with higher resolution, the runtime between GeomFMaps and our approach become comparable. Middle: Runtime comparison with a different number of eigenfunctions (while the number of vertices for shapes is fixed to 10k). Our method is faster than GeomFMaps when the number of ei...*

### 方法边界与适用条件

尽管本文方法在多个挑战性场景下取得了显著提升，但需注意以下边界条件：测试时自适应需要额外的推理时间（每对形状进行数十步迭代优化），在实时性要求极高的场景下可能不适用；方法在极端非等距变形（如 SMAL 中某些跨物种对）下仍存在一定误差，未能完全消除匹配失败的情况；此外，耦合损失依赖于特征相似度的 softmax 计算，当形状顶点数极大时计算开销会显著增加。

## 定位与知识库关联

本文在深度泛函图（Deep Functional Maps）这一技术路线上做出了一个关键性的**范式转换**：将传统“先求泛函图、后通过不可微后处理恢复逐点映射”的两阶段流程，替换为**泛函图与逐点映射联合优化**的单阶段框架。这一改变的实质，是将整个管线中“逐点映射计算”这一槽位从不可学习的后处理模块，提升为训练和推理过程中与泛函图直接耦合的可优化组件。

具体而言，相对于既有深度泛函图方法——无论是监督式的 **FMNet**（Litany et al., 2017）、**GeomFMaps**（Donati et al., 2020）、**DUO-FMNet**（Donati et al., 2022），还是无监督式的 **Roufosse et al. 2019**、**Halimi et al. 2019**、**ConsistFMaps**（Cao and Bernard, 2022）——本文改变的槽位可以精确描述为：

- **逐点映射计算**：从“泛函图求解 → ZoomOut/最近邻后处理”变为“特征相似度 softmax → 可微软对应矩阵 $Π_{NM}$”。这一改变使得逐点映射在训练时即可接收来自耦合损失 $L_{\text{couple}}$ 的梯度信号，从而让特征提取器学习到**直接服务于点对应质量**的特征表示，而非仅服务于泛函图结构正则化。
- **损失函数**：从仅包含 $L_{\text{fmap}}$（双向性 + 正交性正则）扩展为 $L_{\text{total}} = L_{\text{fmap}} + λ_{\text{couple}} L_{\text{couple}}$。新增的耦合损失 $L_{\text{couple}} = \| C_{MN} - Φ_N^† Π_{NM} Φ_M \|_F^2$ 在数学上强制了泛函图必须能够由某个有效的逐点映射生成（Eq. 7 的约束集），从而弥合了泛函图与点对应之间的语义鸿沟。
- **推理策略**：从“固定特征提取器 + 泛函图求解器 + 后处理”变为两种可选模式：(1) 直接使用特征最近邻获得硬对应 $Π_{NM} = \text{NN}(F_N, F_M)$，完全放弃泛函图求解器；(2) 可选的**测试时自适应**（Test-Time Adaptation），对单个测试形状对迭代最小化 $L_{\text{total}} + L_{\text{dirichlet}}$，同时更新特征提取器、逐点映射和泛函图。这种推理时的联合优化在现有深度泛函图方法中并无先例。

从知识库挂载的角度，本文的核心贡献可以挂载到以下节点：

1. **深度泛函图匹配**（Deep Functional Map Matching）：本文属于该技术路线，但通过引入可微逐点映射和耦合损失，将原本分离的泛函图优化与点对应恢复统一为端到端可训练框架。知识库中可标记为“首个实现泛函图-逐点映射联合无监督学习的工作”。

2. **无监督形状匹配**（Unsupervised Shape Matching）：本文完全不需要任何标注对应关系，仅依赖结构正则化和耦合损失进行训练。在无监督设定下，本文在近等距、非等距、部分形状和拓扑噪声等多个基准上大幅超越既有方法，甚至优于部分监督方法（如 DPFM、AttentiveFMaps），因此可挂载为“无监督形状匹配的新 state-of-the-art”。

3. **测试时自适应**（Test-Time Adaptation）：本文在形状匹配任务中引入了测试时优化的策略，这一思想与域自适应、元学习等领域有潜在交叉。知识库中可关联到“推理时优化”（optimization at inference）这一类方法。

**适用边界**方面，本文方法的设计使其在以下场景具有显著优势：

- **非等距匹配**：耦合损失和软映射机制允许模糊对应，测试时自适应中的 Dirichlet 平滑项 $L_{\text{dirichlet}}$ 进一步鼓励局部光滑性，使方法对大幅拉伸和姿态变化具有鲁棒性。
- **部分形状匹配**：软对应矩阵 $Π_{NM}$ 通过 softmax 归一化自然支持部分匹配（目标形状顶点可无对应），无需专门的外点检测模块。
- **拓扑噪声**：谱域操作天然对拓扑变化具有一定容忍度，耦合损失进一步约束了低频对应的一致性。
- **跨数据集泛化**：由于不依赖特定数据集的标注，无监督训练的特征具有更强的泛化能力，在 FAUST→SCAPE、FAUST→SHREC'19 等跨数据集设置下表现突出。

但该方法也存在一些**隐含边界**：

- 方法依赖于有意义的谱基（Laplacian eigenbasis），如果输入形状的谱结构受到极端噪声破坏（如严重不完整采样或极度非均匀网格），谱基本身的质量会成为瓶颈。消融实验表明，若将方法退化为公理化方法（每对形状独立优化，不进行集体训练），误差从 3.9 飙升至 43.1（Table 9），说明**集体无监督训练所学习到的特征先验是方法性能的关键支撑**，在完全脱离训练分布的形状对上可能退化。
- 测试时自适应虽然提升了精度，但引入了额外的推理时间开销，在实时性要求高的场景下需要权衡。

**后续启发**方面，本文的工作打开了若干有价值的方向：

- **耦合损失的推广**：$L_{\text{couple}}$ 的核心思想——强制隐空间表示（泛函图）与显式对应（逐点映射）一致——可以推广到其他涉及隐式对应学习的任务，如点云配准、图像匹配中的特征匹配等。
- **软映射机制的深化**：消融实验表明，软映射（softmax）相比硬映射（Gumbel）提供了更大的匹配灵活性（误差 3.9 vs 4.4），这提示在对应问题中保持概率性的中间表示可能比过早离散化更优，值得在理论上进一步探索。
- **测试时自适应的系统化**：本文的测试时自适应目前仅针对单对形状优化，未来可探索批量测试时自适应、或将其与元学习结合，使特征提取器本身具备快速适应新分布的能力。
- **与有监督方法的融合**：本文在无监督设定下已接近甚至超越部分有监督方法，若将耦合损失作为辅助正则项引入有监督训练，可能进一步提升监督方法的泛化性和鲁棒性。

**总结**：本文在深度泛函图管线中将“逐点映射计算”从不可微后处理提升为可微耦合组件，通过 $L_{\text{couple}}$ 和测试时自适应实现了泛函图与点对应的联合优化，从根本上解决了传统两阶段流程中两者脱节的问题。该方法在知识库中应定位为“深度泛函图匹配的范式改进工作”，其核心槽位改变和耦合损失机制对后续对应学习研究具有明确的启发价值。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Unsupervised_Learning_of_Robust_Spectral_Shape_Matching.pdf]]
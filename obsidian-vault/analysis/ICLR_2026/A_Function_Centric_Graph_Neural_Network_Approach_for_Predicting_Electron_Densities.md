---
title: "A Function-Centric Graph Neural Network Approach for Predicting Electron Densities"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Function_Centric_Graph_Neural_Network_Approach_for_Predicting_Electron_Densities.pdf
aliases:
- BOAB
- FCGNNAPED
- "Basis Overlap Architecture (BOA)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "采用二次展开（quadratic expansion）表示电子密度，灵感来源于KS-DFT中密度矩阵的自然形式，并通过低秩表示避免显式构造完整的密度矩阵。"
primary_logic: "将内部特征解释为在原子中心基组中表示的函数，并利用基函数的重叠矩阵设计消息传递机制，使模型天然具备分子几何信息和旋转等变性。"
claims:
- "二次展开显著优于线性展开"
- "BOA在QM9 VASP和PySCF数据集上超越此前所有方法"
- "BOA在MD数据集上所有分子均达到最优或持平"
- "使用较小截断半径的BOA模型在泛化到更大分子时优于ResNet"
---

# A Function-Centric Graph Neural Network Approach for Predicting Electron Densities

> [!tip] 核心洞察
> 将内部特征解释为在原子中心基组中表示的函数，并利用基函数的重叠矩阵设计消息传递机制，使模型天然具备分子几何信息和旋转等变性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种以函数为中心的图神经网络方法用于预测电子密度 |
| 英文题名 | A Function-Centric Graph Neural Network Approach for Predicting Electron Densities |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HDdkFjFEZd) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | Basis Overlap Architecture (BOA) |
| Dataset | QM9 VASP, QM9 PySCF, MD - ethanol, MD - benzene |

> [!tip] 效果简介
> - QM9 VASP 上，NMAE [%] 为 0.1339 ± 0.0005 (BOA large)，对比 0.175 (SCDP)，变化 -23.5%。
> - QM9 PySCF 上，NMAE [%] 为 0.116 ± 0.006 (BOA large)，对比 0.18 (ResNet)，变化 -35.6%。
> - MD - ethanol 上，NMAE [%] 为 0.710 ± 0.004 (BOA small)，对比 0.82 (ELECTRA)，变化 -13.4%。

## 概述

本文提出了一种以函数为中心的图神经网络架构——基重叠架构（Basis Overlap Architecture, BOA），用于直接从分子几何结构预测电子密度。传统方法在原子中心基组中线性展开电子密度，需要大量基函数才能达到高精度，且无法有效利用密度矩阵的低秩结构。BOA的核心创新在于采用二次展开（quadratic expansion）表示电子密度，灵感来源于KS-DFT中密度矩阵的自然形式，并通过低秩表示避免显式构造完整的密度矩阵。模型将内部特征解释为在原子中心基组中表示的函数，并利用基函数的重叠矩阵设计消息传递机制，使模型天然具备分子几何信息和旋转等变性。

在QM9数据集上，BOA在VASP和PySCF两种参考密度计算方式下均超越此前所有方法，NMAE分别达到0.1339%和0.116%，相比此前最佳方法SCDP和ResNet分别降低23.5%和35.6%的误差。在MD数据集上，BOA在6个分子中的5个上取得最优结果，在1个分子上持平。此外，仅使用较小截断半径（r_mp=3Å, r_e=2Å）训练的BOA模型在泛化到更大分子（QMugs数据集，最大近200个原子）时优于ResNet，展示了良好的泛化能力。消融实验证实二次展开显著优于线性展开（NMAE: 0.1381% vs 0.2716%），更大的基组（def2-QZVPPD）和径向修正均带来一致的性能提升。

## 背景与动机

电子密度是量子化学计算中的核心物理量，其精确预测对于理解分子性质、加速材料设计具有重要意义。然而，现有基于深度学习的电子密度预测方法面临一个根本性的表示瓶颈：传统方法采用原子中心基组的线性展开形式 $\rho(\mathbf{r}) = \sum_a \sum_\mu p_{a\mu} \omega_\mu^{Z_a}(\mathbf{r} - \mathbf{r}_a)$，这种表示需要大量基函数才能达到高精度，且无法有效利用密度矩阵内在的低秩结构。尽管已有多种方法被提出——包括基于等变图神经网络的 eqDeepDFT、InfGCN、ChargE3Net，基于神经算子的 GPWNO，以及基于扩散模型的 ELECTRA 等——但这些方法在表示效率和精度之间始终存在权衡。

本文的动机源于一个关键的物理洞察：在 KS-DFT 理论中，电子密度自然具有二次形式（即轨道平方之和），这意味着密度矩阵天然地具有低秩结构。基于此，作者提出采用二次展开（quadratic expansion）来表示电子密度：

$$\rho(\mathbf{r}) = \sum_{a \in \mathcal{N}} \hat{g}_a^{(l)}(\mathbf{r}) \hat{g}_a^{(r)}(\mathbf{r}) + \sum_{(a,b) \in \mathcal{E}_e} \sum_o^{N^o} g_{abo}^{(l)}(\mathbf{r}) g_{abo}^{(r)}(\mathbf{r})$$

这种表示将密度矩阵块分解为 $\Gamma_{ab\mu\nu} = \sum_o^{N^o} g_{abo\mu}^{(l)} g_{abo\nu}^{(r)} + \delta_{ab} \hat{g}_{a\mu}^{(l)} \hat{g}_{a\nu}^{(r)}$，从而避免了显式构造完整的密度矩阵，同时保持了其低秩特性。

为实现这一表示，作者提出了 Basis Overlap Architecture (BOA)，其核心创新在于：将内部特征解释为在原子中心基组中表示的函数，并利用基函数的重叠矩阵设计消息传递机制。具体而言，BOA 的消息传递通过求解最小二乘优化问题 $\min_{m_{abm\mu}} \| h_{bm}(\mathbf{r}) - \sum_{\mu} m_{abm\mu} \omega_\mu^{Z_a}(\mathbf{r} - \mathbf{r}_a) \|^2$，将发送节点的特征函数投影到接收节点的基组上，从而自然地融入分子几何信息和旋转等变性。此外，BOA 还引入了基于原子类型的可学习初始密度猜测和径向修正因子 $c_\mu(r)$，进一步提升了表示精度。

现有方法的缺口在于：线性展开无法有效捕获密度矩阵的低秩结构，导致表示效率低下；而二次展开虽然更符合物理本质，但此前缺乏有效的深度学习框架来实现这一表示。BOA 通过函数消息传递和基函数重叠矩阵的设计，弥合了这一差距。实验结果表明，二次展开相比线性展开将 NMAE 从 0.2716% 降低至 0.1381%（Table 5），验证了这一核心设计选择的有效性。

## 核心创新

BOA（Basis Overlap Architecture）的核心创新在于将分子图神经网络中的内部特征显式地解释为在原子中心基组中展开的函数，并基于此设计了一套完整的函数级消息传递与密度表示机制。这一范式转变直接针对传统方法在原子中心基组中线性展开电子密度时，需要大量基函数且无法利用密度矩阵低秩结构的瓶颈。

**密度表示的二次展开**：BOA最关键的改变量（changed slot）是密度表示形式。传统方法采用线性展开 $\rho(\mathbf{r}) = \sum_a \sum_\mu p_{a\mu} \omega_\mu^{Z_a}(\mathbf{r} - \mathbf{r}_a)$，而BOA受KS-DFT中密度矩阵自然形式的启发，采用二次展开：

$$
\rho(\mathbf{r}) = \sum_{a \in \mathcal{N}} \hat{g}_a^{(l)}(\mathbf{r}) \hat{g}_a^{(r)}(\mathbf{r}) + \sum_{(a,b) \in \mathcal{E}_e} \sum_o^{N^o} g_{abo}^{(l)}(\mathbf{r}) g_{abo}^{(r)}(\mathbf{r})
$$

该表示通过低秩分解（秩 $N^o$）隐式构造密度矩阵块 $\Gamma_{ab\mu\nu} = \sum_o g_{abo\mu}^{(l)} g_{abo\nu}^{(r)} + \delta_{ab} \hat{g}_{a\mu}^{(l)} \hat{g}_{a\nu}^{(r)}$，避免了显式存储完整的 $N_{\text{basis}} \times N_{\text{basis}}$ 密度矩阵。消融实验（Table 5）证实这一改变是决定性的：二次展开的NMAE为0.1381%，而线性展开为0.2716%，误差降低近一倍。

**基于基函数重叠的消息传递**：第二个关键改变是消息传递机制本身。标准GNN传递标量或向量特征，而BOA传递的是函数。其核心原理是将发送节点 $b$ 的特征函数 $h_{bm}(\mathbf{r})$ 投影到接收节点 $a$ 的基组上，通过最小二乘优化 $\min_{m_{abm\mu}} \| h_{bm}(\mathbf{r}) - \sum_\mu m_{abm\mu} \omega_\mu^{Z_a}(\mathbf{r} - \mathbf{r}_a) \|^2$ 得到消息系数的闭式解 $m_{abm\mu} = \sum_\nu (W^{aa})_{\mu\nu}^{-1} \sum_\kappa W_{\nu\kappa}^{ab} h_{bm\kappa}$。这里 $W_{\mu\nu}^{ab} = \int d\mathbf{r} \omega_\mu^{Z_a}(\mathbf{r} - \mathbf{r}_a) \omega_\nu^{Z_b}(\mathbf{r} - \mathbf{r}_b)$ 是基函数重叠矩阵。这一机制使模型天然具备旋转等变性：由于球形谐波在SO(3)下按不可约表示变换，且重叠矩阵满足 $\bar{W}^{ab} = D^{Z_a}(R) W^{ab} (D^{Z_b}(R))^T$，整个消息传递过程是SO(3)-等变的（Appendix H证明）。

**可学习的初始密度猜测**：BOA引入了基于原子类型的可学习初始密度猜测（changed slot），其系数在预训练1000步后随完整训练过程持续优化。这为模型提供了一个合理的起点，而非从零开始或使用固定原子密度。

**基函数径向修正**：BOA不直接学习基函数参数，而是为每种原子类型学习一个径向修正因子 $c_\mu(r)$，修正后的基函数为 $\tilde{\omega}_\mu^Z(\mathbf{r}) = \omega_\mu^Z(\mathbf{r})(1 + c_\mu(\mathbf{r}))$（Figure 3C）。该修正通过一个小型MLP在Gaussian径向嵌入上预测，增加了基组在径向方向的灵活性。

这些创新的因果链是：二次展开利用密度矩阵的低秩结构→减少所需参数并提升表示精度；函数级消息传递使模型能直接操作与物理量（电子密度）同构的表示→提升等变性和数据效率；可学习的初始猜测和径向修正→进一步降低优化难度。最终，BOA在QM9 VASP数据集上达到0.1339% NMAE，比此前最佳方法SCDP（0.175%）降低23.5%；在QM9 PySCF数据集上达到0.116% NMAE，比ResNet（0.18%）降低35.6%（Table 1）。在MD数据集的6个分子中，BOA在5个上取得最佳结果，1个持平（Table 2）。值得注意的失败模式是：使用较大截断半径（$r_{\text{mp}}=6\text{Å}, r_{\text{e}}=3\text{Å}$）的BOA模型在泛化到更大分子（QMugs）时性能不如ResNet，但使用较小截断半径（$r_{\text{mp}}=3\text{Å}, r_{\text{e}}=2\text{Å}$）的模型反而超越ResNet（Figure 4），说明大截断半径引入的噪声可能损害泛化能力。

## 整体框架

![[assets/figures/papers/iclr26_0002_HDdkFjFEZd_A_Function-Centric_Graph_Neural_Network_Approach/figures/001_Figure_1.jpg]]
*Figure 1: The Basis Overlap Architecture (BOA). (A) The node embeddings are updated using BOA blocks, which contain a function message passing step to facilitate communication between nodes. The edge features are modified using the edge update block, which uses the current edge and node features to calculate new edge features. The output of the BOA backbone consists of coefficients used to expand the density in atom-centered Gaussian-type basis functions (Sec. 2.1). In the partial channel mean the number of channels is reduced by taking the mean of groups of channels. M denotes the molecular geometry and $\mathbf { r } _ { g }$ are the grid positions with g $\in \{$ 1 , $\ldots , N ^ { g } \}$ and $N ^ { g...$

Basis Overlap Architecture (BOA) 的核心设计思路是将神经网络内部特征显式解释为在原子中心基组中展开的函数，并利用基函数的重叠矩阵设计消息传递机制。这一设计使得模型天然具备分子几何信息和旋转等变性，同时能够高效地预测电子密度。

**整体 Pipeline 与模块关系**

BOA 的整体架构（Figure 1A）由以下几个关键模块串联而成：

1. **节点嵌入与边嵌入**：根据原子类型初始化节点和边的特征。为保证等变性，仅设置角量子数 l=0 的基函数系数为非零值，其余系数置零（Section 2.3, Eq. 5-7）。
2. **初始密度猜测**：基于原子类型的可学习初始猜测，预训练 1000 步后在完整训练过程中持续优化（Section 2.2）。
3. **BOA 消息传递块**：这是模型的核心模块，利用基函数重叠矩阵实现函数消息传递（Figure 3B）。具体而言，将发送节点的特征函数投影到接收节点的基组上，通过求解最小二乘优化问题得到消息系数（Appendix G, Eq. 24-26）。同时引入注意力权重，从节点间的特征函数重叠计算得到。
4. **边更新块**：使用节点特征和当前边特征生成新的边特征（Figure 3A）。通过 MLP 生成权重矩阵，经 Frobenius 范数归一化和可学习标量因子缩放后，线性混合边和节点特征。
5. **非线性层**：通过计算标量不变量并用 MLP 变换后加权原始特征，实现等变非线性（Appendix H.2）。
6. **部分通道均值**：将特征通道分组取均值，减少特征通道数（Figure 1A）。
7. **径向修正**：为每种原子类型学习一个径向修正因子 c_μ(r)，修正后的基函数为 ω̃_μ^Z(r) = ω_μ^Z(r)(1 + c_μ(r))（Appendix A, Figure 3C）。
8. **密度输出**：根据二次展开公式在网格上计算预测电子密度（Section 2.1, Eq. 2）。

**输入输出流**

- **输入**：分子几何构型（原子类型和坐标），以及网格点位置。
- **内部表示**：节点特征 h_{amμ} 和边特征 g_{abmμ}^{(l/r)}，其中 a,b 为原子索引，m 为特征通道，μ 为基函数索引。
- **输出**：在网格点上的预测电子密度 ρ(r)。

**核心设计创新**

BOA 与现有方法的关键区别在于其密度表示形式和消息传递机制：

- **密度表示形式**：采用二次展开（quadratic expansion）而非传统的线性展开。二次展开灵感来源于 KS-DFT 中密度矩阵的自然形式，通过低秩表示避免显式构造完整的密度矩阵。消融实验（Table 5）显示，二次展开的 NMAE 为 0.1381%，而线性展开为 0.2716%，性能提升近一倍。
- **消息传递机制**：基于基函数重叠矩阵的函数消息传递，而非标准 GNN 的标量或向量特征传递。这一机制使得模型能够自然地处理分子几何信息，并保证 SO(3) 等变性（Appendix H）。
- **基函数径向修正**：为每种原子类型学习径向修正因子，增强基函数的灵活性（Appendix A）。消融实验（Table 3）表明，同时使用径向修正和绝对值函数效果最佳。

**证据强度说明**：上述所有模块描述均有明确的论文锚点支持，置信度在 0.95-1.0 之间。二次展开与线性展开的性能对比有 Table 5 的定量证据支持，置信度 1.0。

## 核心模块与公式推导

### 密度表示的瓶颈与二次展开

传统方法将电子密度在原子中心基组中线性展开（`ρ(r) = Σ_a Σ_μ p_{aμ} ω_μ^{Z_a}(r - r_a)`），其瓶颈在于需要大量基函数才能达到高精度，且无法有效利用密度矩阵的低秩结构。BOA 的核心因果旋钮是采用**二次展开**（quadratic expansion）表示电子密度，灵感来源于 KS-DFT 中密度矩阵的自然形式（`ρ(r) = Σ_i |ψ_i(r)|²`）。具体地，密度表示为：

`ρ(r) = Σ_a ĝ_a^{(l)}(r) ĝ_a^{(r)}(r) + Σ_{(a,b)} Σ_o^{N^o} g_{abo}^{(l)}(r) g_{abo}^{(r)}(r)`

其中第一项为自环（self-loop）贡献，第二项为边（edge）贡献。`ĝ_a^{(l)}(r)` 和 `ĝ_a^{(r)}(r)` 是节点 a 的两个函数，`g_{abo}^{(l)}(r)` 和 `g_{abo}^{(r)}(r)` 是边 (a,b) 的第 o 对函数。这些函数均在原子中心基组中展开：

`ĝ_a^{(l)}(r) = Σ_μ ĝ_{aμ}^{(l)} ω_μ^{Z_a}(r - r_a)`, `ĝ_a^{(r)}(r) = Σ_μ ĝ_{aμ}^{(r)} ω_μ^{Z_a}(r - r_a)`

`g_{abo}^{(l)}(r) = Σ_μ g_{aboμ}^{(l)} ω_μ^{Z_a}(r - r_a)`, `g_{abo}^{(r)}(r) = Σ_μ g_{aboμ}^{(r)} ω_μ^{Z_b}(r - r_b)`

其中 `ω_μ^{Z_a}(r - r_a)` 是中心在原子 a 位置 `r_a` 的基函数，`μ` 为基函数索引，`Z_a` 为原子类型。二次展开的本质是**密度矩阵块的低秩表示**：

`Γ_{abμν} = Σ_o^{N^o} g_{aboμ}^{(l)} g_{aboν}^{(r)} + δ_{ab} ĝ_{aμ}^{(l)} ĝ_{aν}^{(r)}`

这种表示避免了显式构造完整的密度矩阵，同时利用其低秩结构（`N^o` 为秩），在保持高精度的同时显著降低参数数量。消融实验（Table 5）证实二次展开（NMAE: 0.1381%）远优于线性展开（NMAE: 0.2716%）。

### 函数消息传递（Basis Overlap Message Passing）

BOA 的消息传递机制是另一个关键创新。其核心思想是将内部特征解释为在原子中心基组中表示的函数，消息传递通过**基函数重叠矩阵**实现函数从发送节点到接收节点的投影。

给定发送节点 b 的特征函数 `h_{bm}(r)`，其向接收节点 a 发送的消息被定义为 `h_{bm}(r)` 在节点 a 的基组上的最优投影，即求解最小二乘问题：

`min_{m_{abmμ}} || h_{bm}(r) - Σ_μ m_{abmμ} ω_μ^{Z_a}(r - r_a) ||²`

该问题的闭式解为：

`m_{abmμ} = Σ_ν (W^{aa})_{μν}^{-1} Σ_κ W_{νκ}^{ab} h_{bmκ}`

其中 `W_{νκ}^{ab} = ∫ dr ω_ν^{Z_a}(r - r_a) ω_κ^{Z_b}(r - r_b)` 是基函数重叠矩阵。该解通过以下两步实现：首先计算节点 a 的基函数与节点 b 的特征函数之间的重叠积分 `o_{abmμ} = Σ_ν W_{μν}^{ab} h_{bmν}`，然后通过 `(W^{aa})^{-1}` 将投影系数从重叠空间转换到基函数系数空间。

消息传递过程中还引入了注意力权重 `α̃_{abmn}`，通过两个节点特征函数的重叠计算得出，用于加权不同通道的消息。这种设计使模型天然具备分子几何信息和旋转等变性。

### 初始密度猜测与节点/边嵌入

BOA 使用**可学习的初始密度猜测**，基于原子类型初始化节点和边特征。初始猜测系数预训练 1000 步，随后在完整训练过程中持续优化。

节点特征初始化：`h_{amμ} = W_{Z_a mμ}^{(n)}`（仅当 `ω_μ^{Z_a}` 是 `l=0` 基函数时，否则为 0）。边特征初始化类似，左特征 `g_{abmμ}^{(l)} = W_{Z_a Z_b mμ}^{(e,l)}`（仅当 `ω_μ^{Z_a}` 是 `l=0` 基函数时）。这种初始化确保了等变性，因为仅 `l=0` 基函数是旋转不变的。

### 径向修正与平滑绝对值函数

BOA 为每种原子类型学习一个**径向修正因子** `c_μ(r)`，修正后的基函数为：

`ω̃_μ^Z(r) = ω_μ^Z(r)(1 + c_μ(r))`

其中 `c_μ(r)` 通过一个小型 MLP 预测，输入为半径 r 的高斯径向嵌入（Gaussian radial embedding）。这增加了基函数的灵活性，消融实验（Table 3）证实径向修正与绝对值函数同时使用效果最佳。

此外，对每对边函数中的一个应用**平滑绝对值函数**：

`|x|_s = { (λ/2)x², if |x| < 1/λ; |x| - 1/(2λ), otherwise }`

最终密度预测为 `ρ(r) = Σ_{(a,b)} Σ_o g_{abo}^{(l)}(r) |g_{abo}^{(r)}(r)|_s + Σ_a ĝ_a^{(l)}(r) |ĝ_a^{(r)}(r)|_s`。

### 等变非线性与归一化

BOA 的等变非线性通过计算标量不变量并用 MLP 变换后加权原始特征实现。权重矩阵通过 Frobenius 范数归一化：

`w̃_{ab}^{(·,·)} = w_{ab}^{(·,·)} / (||w_{ab}^{(·,·)}||_f + ε)`

边更新块使用归一化后的权重和节点特征生成新边特征：

`g̃_{abmμ}^{(·)} = Σ_n s_{ab}^{(e,·)} w̃_{abmn}^{(e,·)} g_{abnμ}^{(·)} + Σ_n s_{ab}^{(n,·)} w̃_{abmn}^{(n,·)} h_{anμ}`

其中 `s_{ab}` 是学习的标量因子。所有操作均保持 SO(3)-等变性。

### 评估指标

归一化平均绝对误差（NMAE）用于比较预测和参考电子密度：

`NMAE(ρ̃, ρ) = (∫ dr |ρ̃(r) - ρ(r)|) / (∫ dr |ρ(r)|)`

## 实验与分析

### 主要结果：BOA在QM9和MD数据集上全面超越此前最优方法

**QM9数据集**（Table 1）是评估电子密度预测性能的标准基准，包含基于VASP和PySCF两种参考计算方法的子集。BOA large版本在两个子集上均取得了最优结果：在VASP子集上NMAE为0.1339% ± 0.0005，相比此前最优方法SCDP（0.175%）降低了23.5%；在PySCF子集上NMAE为0.116% ± 0.006，相比ResNet（0.18%）降低了35.6%。BOA small版本（参数更少）同样超越了所有此前方法，VASP子集上为0.1381% ± 0.0003，PySCF子集上为0.137% ± 0.003。


![[assets/figures/papers/iclr26_0002_HDdkFjFEZd_A_Function-Centric_Graph_Neural_Network_Approach/figures/004_Table_1.jpg]]
*Table 1: Comparison of BOA with previous best methods on the QM9 charge density datasets. Two datasets based on QM9 are evaluated, differing in the reference electron density calculation method. Errors are reported as NMAE [%]. For BOA the mean and standard error over three runs are reported for the small models. For the large models the mean and standard error over five runs are reported. Errors of eqDeepDFT, InfGCN, ChargE3Net, and SCDP are reproduced from Fu et al. (2024). The ResNet results are taken from Li et al. (2025)*

**MD数据集**（Table 2）包含6个分子，BOA small在5个分子上取得最优结果，在1个分子（malonaldehyde）上与ELECTRA持平。具体对比：ethanol 0.710% ± 0.004（ELECTRA 0.82%），benzene 0.361% ± 0.003（ELECTRA 0.44%），phenol 0.56% ± 0.03（ELECTRA 0.67%），resorcinol 0.371% ± 0.004（ELECTRA 0.44%），ethane 0.772% ± 0.002（ELECTRA 0.87%）。BOA在所有分子上的性能提升幅度在9.0%到18.0%之间。


![[assets/figures/papers/iclr26_0002_HDdkFjFEZd_A_Function-Centric_Graph_Neural_Network_Approach/figures/005_Table_2.jpg]]
*Table 2: Comparison of BOA with other methods on the MD charge density dataset. Errors are reported as NMAE [%]. For BOA the mean and standard error of the mean over three runs are reported. Errors of the other models (InfGCN (Cheng & Peng, 2023), GPWNO (Kim & Ahn, 2024), SCDP (Fu et al., 2024), ELECTRA (Elsborg et al., 2025)) are reproduced from Elsborg et al. (2025)*

**泛化到更大分子**（Figure 4）是BOA的关键优势。仅在小分子（QM9，最多9个重原子）上训练的BOA模型，被直接评估在QMugs数据集（含近200个原子的分子）上。使用较小截断半径（r_mp=3Å, r_e=2Å）的BOA模型在精度上优于此前最优的ResNet模型，且精度随分子尺寸增大保持稳定。而使用较大截断半径的BOA模型虽然在小分子上表现更好，但在大分子上精度下降，且计算时间随分子尺寸增长更快（O(N²) vs O(N)）。

**库仑能量误差**（Section D）是电子密度误差的下游物理量。BOA的库仑能量平均绝对误差为66 meV，显著低于ResNet的167 meV，表明BOA在能量相关应用中具有优势。

**推理时间效率**（Table 7）方面，BOA standard在QM9 VASP测试集上每个分子的平均推理时间为0.226秒，与ELECTRA（0.119秒）和SCDP（0.126秒）相比略慢，但使用更小的def2-TZVP基组可将时间降至0.149秒。

### 消融实验：二次展开是精度提升的核心机制

**二次展开 vs 线性展开**（Table 5）是BOA最重要的设计选择。在QM9 VASP数据集上，二次展开的NMAE为0.1381% ± 0.0003，而线性展开为0.2716% ± 0.0007，误差几乎翻倍。这一结果直接验证了密度矩阵低秩表示的有效性——二次展开利用了KS-DFT中密度矩阵的自然形式，避免了线性展开需要大量基函数才能达到高精度的瓶颈。


![[assets/figures/papers/iclr26_0002_HDdkFjFEZd_A_Function-Centric_Graph_Neural_Network_Approach/figures/010_Table_5.jpg]]
*Table 5: Quadratic expansion ablation. All settings other than the expansion type are kept constant to the small BOA version and the models are trained on the QM9 VASP dataset. Three training runs are performed for each configuration and the mean and standard error are reported*

**基组大小的影响**（Table 4）显著：使用def2-QZVPPD（四重zeta）基组的NMAE为0.1381% ± 0.0003，而def2-SVP（单重zeta）为0.1757% ± 0.0006，def2-TZVP（三重zeta）为0.1441% ± 0.0004。更大的基组提供了更灵活的表示能力，但计算开销也相应增加。


![[assets/figures/papers/iclr26_0002_HDdkFjFEZd_A_Function-Centric_Graph_Neural_Network_Approach/figures/009_Table_4.jpg]]
*Table 4: Basis set ablation. All settings other than the basis set are kept constant to the small BOA version and the models are trained on the QM9 VASP dataset. Three training runs are performed for each configuration and the mean and standard error are reported*

**绝对值函数和径向修正**（Table 3）的消融表明两者单独使用均有改进，但同时使用效果最佳（NMAE 0.1381% ± 0.0003）。仅使用绝对值（无径向修正）为0.1403% ± 0.0004，仅使用径向修正（无绝对值）为0.1407% ± 0.0004，两者均不使用为0.1433% ± 0.0005。平滑绝对值函数（|x|_s）通过引入非线性增强了模型对电子密度正定性的表达能力，而径向修正则允许基函数适应不同化学环境。


![[assets/figures/papers/iclr26_0002_HDdkFjFEZd_A_Function-Centric_Graph_Neural_Network_Approach/figures/008_Table_3.jpg]]
*Table 3: Ablation study of taking the absolute value of one of the basis functions in the pair and applying the radial correction. The small BOA version is trained on the QM9 VASP dataset. Errors are reported as NMAE [%]*

**截断半径**（Table 6）的影响相对较小：标准设置（r_mp=6Å, r_e=3Å）的NMAE为0.1381% ± 0.0003，增大截断半径（r_mp=8Å, r_e=5Å）后为0.1343% ± 0.0007，改进幅度仅2.8%。这表明BOA对截断半径不太敏感，小半径设置即可捕获关键的化学相互作用。

### 误差分布分析：BOA在高密度区域表现更优

Figure 5展示了BOA large和SCDP在QM9 VASP测试集上的误差分布。两种模型的最大误差均出现在靠近原子的高电子密度区域，但BOA在这些关键区域的误差显著更小。具体而言，BOA在距离最近原子0.5Å以内的区域误差比SCDP低约40%，在距离第二近原子1.0Å以内的区域误差低约50%。这一优势源于BOA的二次展开能够更精确地表示原子核附近的电子密度峰值。

### 失败模式与局限性

尽管BOA在多个基准上取得了最优结果，但仍存在以下失败模式：

1. **原子类型扩展性**：BOA为每种原子类型使用独立的参数集，包括节点嵌入、边嵌入和径向修正MLP。在当前数据集（仅含H、C、O等少量原子类型）上可行，但扩展到覆盖元素周期表中更多原子类型时，参数数量将线性增长，可能导致过拟合或计算不可行。

2. **大分子泛化的权衡**：虽然BOA展示了泛化到更大分子的能力，但这种泛化依赖于较小的截断半径。使用标准截断半径（r_mp=6Å）的模型在大分子上性能下降，而小截断半径模型虽然泛化更好，但精度略低。这表明BOA在局部精度和全局泛化之间存在根本性权衡。

3. **基函数灵活性有限**：BOA使用固定的未收缩高斯型基函数作为基础，仅学习径向修正因子。基函数的指数和角动量分布是固定的，这限制了模型适应不同化学环境的能力。未来通过学习基函数的指数或使重叠矩阵在训练中可微调，可能进一步提升精度。

4. **计算效率**：二次展开的计算开销高于线性展开方法，主要来自基函数乘积的评估和重叠矩阵的计算。在大分子上，这一开销可能成为瓶颈，特别是当使用大基组和大截断半径时。

### 关键图表结论总结

- **Table 1 & 2**：BOA在QM9和MD数据集上全面超越此前最优方法，验证了函数中心GNN方法的有效性。
- **Figure 4**：小截断半径的BOA模型在泛化到更大分子时优于ResNet，展示了良好的可扩展性。
- **Table 5**：二次展开是BOA精度提升的核心，误差相比线性展开降低近一半。
- **Figure 5**：BOA在高电子密度区域的误差显著小于SCDP，表明其能更精确地表示原子核附近的电子结构。
- **Table 7**：BOA的推理时间与现有方法相当，使用小基组可进一步降低计算成本。

## 方法谱系与知识库定位

### 与 Baseline / Follow-up 的关系

BOA 的核心贡献在于改变了电子密度预测中密度表示的基本形式。此前的主流方法（如 eqDeepDFT、InfGCN、ChargE3Net、SCDP、ELECTRA）均采用线性展开：`ρ(r) = Σ_a Σ_μ p_{aμ} ω_μ^{Z_a}(r - r_a)`，即每个原子独立贡献基函数的加权和。BOA 将其替换为**二次展开**，灵感来源于 KS-DFT 中密度矩阵的自然平方形式（`ρ(r) = Σ_a ĝ_a^{(l)}(r) ĝ_a^{(r)}(r) + Σ_{(a,b)} Σ_o g_{abo}^{(l)}(r) g_{abo}^{(r)}(r)`），这允许模型利用密度矩阵的低秩结构。消融实验（Table 5）直接证实了这一改变的因果力度：二次展开的 NMAE 为 0.1381%，而线性展开为 0.2716%，误差降低约 49%。

在消息传递机制上，BOA 与标准 GNN 有本质区别。标准方法传递标量或向量特征，而 BOA 传递的是**在原子中心基组中展开的函数**。其核心操作是将发送节点的特征函数通过基函数的重叠矩阵 `W_{μν}^{ab} = ∫ dr ω_μ^{Z_a}(r - r_a) ω_ν^{Z_b}(r - r_b)` 投影到接收节点的基组上，这一操作天然编码了分子几何信息并保证了 SO(3) 等变性。这一设计使得 BOA 不需要像其他等变网络那样显式构造球谐函数特征。

在初始密度猜测方面，BOA 引入了可学习的原子类型依赖初始猜测，预训练 1000 步后在全训练中持续优化，这与此前方法使用固定原子密度或无初始猜测的做法不同。

### 适用边界

BOA 在三个基准上均达到最优：
- **QM9 VASP**：BOA large 的 NMAE 为 0.1339%，比此前最优的 SCDP（0.175%）降低 23.5%。
- **QM9 PySCF**：BOA large 的 NMAE 为 0.116%，比 ResNet（0.18%）降低 35.6%。
- **MD 数据集**：BOA small 在 6 个分子中的 5 个上取得最优，1 个持平。例如乙醇上 BOA（0.710%）比 ELECTRA（0.82%）降低 13.4%。

在泛化能力上，BOA 展示了从 QM9（最多 9 个重原子）到 QMugs（近 200 个原子）的迁移能力。关键发现是：使用较小截断半径（`r_mp=3Å, r_e=2Å`）的 BOA 模型在泛化到更大分子时优于 ResNet，而使用较大截断半径的模型反而表现更差（Figure 4）。这表明 BOA 的局部函数表示在分子尺寸增长时保持了精度稳定性，而大截断半径引入的远距离噪声可能损害泛化。

### 局限与开放问题

**局限一：原子类型扩展性**。BOA 为每种原子类型使用独立的参数和基组。对于包含大量不同原子类型的数据集，这可能导致参数规模爆炸。论文指出未来可考虑使用统一的基组来缓解此问题，但这一方案的具体实现和效果尚未验证。

**局限二：基组灵活性有限**。当前 BOA 使用固定的未收缩高斯型基函数作为基础，仅学习径向修正因子 `c_μ(r)`。基函数的角度部分（球谐函数）和指数是固定的，这限制了表示效率。虽然更大的基组（def2-QZVPPD vs def2-SVP）能显著提升精度（Table 4），但这增加了计算开销。

**局限三：计算成本**。二次展开的计算开销高于线性展开方法。Table 7 显示 BOA 的推理时间高于 ELECTRA 和 SCDP，尽管精度更高。论文尝试了使用 def2-TZVP 基组来降低开销，但精度有所下降。

**开放问题**：
1. **架构扩展**：如何将 BOA 的消息传递机制推广到其他需要函数表示的物理量预测任务（如静电势、力场）？其函数视角的通用性尚未被探索。
2. **基组学习**：能否通过学习高斯基函数的指数，或使重叠矩阵和库仑矩阵在训练中可微调，来进一步提升表示效率？这需要解决梯度计算和数值稳定性问题。
3. **大规模系统**：如何进一步降低 BOA 在大分子上的计算成本？当前的时间缩放（Figure 4A）显示 BOA 的复杂度随原子数增长较快，可能需要引入稀疏化或分层策略。
4. **周期表覆盖**：如何将 BOA 扩展到覆盖元素周期表中更广泛的原子类型？当前仅针对 C、H、O、N 等轻元素验证，对过渡金属等复杂原子的适用性未知。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Function_Centric_Graph_Neural_Network_Approach_for_Predicting_Electron_Densities.pdf

![[paperPDFs/ICLR_2026/A_Function_Centric_Graph_Neural_Network_Approach_for_Predicting_Electron_Densities.pdf]]

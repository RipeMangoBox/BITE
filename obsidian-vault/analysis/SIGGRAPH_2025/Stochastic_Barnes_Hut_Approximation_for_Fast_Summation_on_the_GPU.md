---
title: "Stochastic Barnes-Hut Approximation for Fast Summation on the GPU"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Stochastic_Barnes_Hut_Approximation_for_Fast_Summation_on_the_GPU.pdf
project_link: https://www.dgp.toronto.edu/projects/stochastic-barnes-hut/
aliases:
- SBHA
- SBHAFSG
tags:
- SIGGRAPH_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "随机路径长度（基于远场比率的俄罗斯轮盘赌概率）与贡献交换（将Barnes-Hut层级近似作为控制变量）"
primary_logic: "将细节层次（LOD）近似族视为控制变量，构建无偏蒙特卡洛估计器，用少量随机路径样本替代完整确定性树遍历，大幅降低GPU线程发散并提升速度。"
claims:
- "随机方法在8 ms计算超过4万亿粒子对相互作用，Barnes-Hut需14 ms，暴力方法需2800 ms。"
- "在相同中位数误差下，随机方法比优化的Barnes-Hut快至多9.4倍。"
- "在116个网格数据集上，S=1时平均误差比Barnes-Hut低约5倍，中位数误差低约17倍，同时速度快2倍以上。"
- "提出的估计器具有无偏性（Theorem 3.1）。"
---

# Stochastic Barnes-Hut Approximation for Fast Summation on the GPU

> [!tip] 核心洞察
> 将细节层次（LOD）近似族视为控制变量，构建无偏蒙特卡洛估计器，用少量随机路径样本替代完整确定性树遍历，大幅降低GPU线程发散并提升速度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于GPU快速求和的随机Barnes-Hut近似 |
| 英文题名 | Stochastic Barnes-Hut Approximation for Fast Summation on the GPU |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2506.02219); [Project](https://www.dgp.toronto.edu/projects/stochastic-barnes-hut/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | Stochastic Barnes-Hut Approximation |
| Dataset | Power station Coulomb potential, 222 surface sources, 1000² slice plane (Fig. 1), 116 meshes, Coulomb potential, M=2^20 sources, grid 100³ (Table 1), Winding numbers, 2^20 sources, Stanford bunny (Fig. 7) |

> [!tip] 效果简介
> - Power station Coulomb potential, 222 surface sources, 1000² slice plane (Fig. 1) 上，Runtime 为 8 ms，对比 14 ms (Barnes-Hut), 2800 ms (brute force)，变化 1.75× vs Barnes-Hut, 350× vs brute force。
> - 116 meshes, Coulomb potential, M=2^20 sources, grid 100³ (Table 1) 上，Time (ms) 为 4.04 ± 1.12，对比 8.61 ± 2.89 (Barnes-Hut β=2)，变化 2.13× faster。
> - 116 meshes, Coulomb potential, M=2^20 sources, grid 100³ (Table 1) 上，Median Abs. Error 为 7.45e-06 ± 4.45e-06，对比 1.67e-04 ± 1.58e-04 (Barnes-Hut β=2)，变化 22× lower。

## 概述

大规模核函数求和（如引力势、缠绕数、平滑距离场）是计算物理与图形学中的基础运算。给定 $M$ 个源点和一个核函数 $f$，对每个查询点 $\mathbf{q}$ 需计算 $F(\mathbf{q}) = \sum_{i=1}^{M} m_i f(\mathbf{p}_i, \mathbf{q})$，暴力求和的复杂度为 $O(MN)$，在 GPU 上亦难以实时完成——例如 Fig. 1 所示场景中暴力方法耗时 2800 ms。

Barnes-Hut（BH）算法（Barnes and Hut, Nature 1986）通过空间树将远距离源点聚合为质心近似，将复杂度降至 $O(M \log M)$。然而，**标准 BH 在 GPU 上因深度树遍历导致严重的线程发散和内存访问延迟，难以高效并行化**。其 GPU 优化实现（栈式遍历 + warp voting）在 Fig. 1 场景中仍需 14 ms，且近似本身是有偏的。

本文提出 **随机 Barnes-Hut 近似（Stochastic Barnes-Hut Approximation）**，核心思路是将 BH 的细节层次（LOD）近似族视为**控制变量（control variate）**，构建一个**无偏的蒙特卡洛估计器**。具体而言：

- 将每个源点的精确贡献表示为沿树路径的**伸缩和（telescoping sum）**；
- 用基于远场比率的**俄罗斯轮盘赌（Russian roulette）概率**随机截断路径，大幅减少需要访问的树节点；
- 通过**贡献交换（contribution swap）**将对偶采样引入估计器以降低方差。

该方法用少量随机路径样本替代完整确定性树遍历，从根本上缓解了 GPU 线程发散问题。在 NVIDIA RTX 4090 上，**随机方法在 8 ms 内计算超过 4 万亿粒子对相互作用**，比 GPU 优化的 BH 快约 1.75 倍，比暴力方法快 350 倍（Fig. 1）。在 116 个网格数据集上，$S=1$ 时平均误差比 BH 低约 5 倍，中位数误差低约 17 倍，同时速度快 2 倍以上（Table 1）。在相同中位数误差下，随机方法比优化的 BH 快至多 9.4 倍（Fig. 5）。

方法的理论保证在于估计器的**无偏性**（Theorem 3.1，附录 A 给出完整证明）。其应用范围涵盖库仑势、引力势、缠绕数和平滑距离场等多种全局支撑核函数。

## 背景与动机

大规模核函数求和是计算机图形学与科学计算中的基础运算，广泛出现在引力势场计算、缠绕数评估、平滑距离场生成等场景中。给定 $M$ 个携带质量 $m_i$ 的源点 $\mathbf{p}_i$，对查询点 $\mathbf{q}$ 的精确全对求和为：

$$F(\mathbf{q}) = \sum_{i=1}^{M} m_i f(\mathbf{p}_i, \mathbf{q})$$

当源点数量达到百万级、查询点为密集三维网格时，暴力求和的计算复杂度为 $O(MN)$，在 GPU 上也需要数秒才能完成，难以满足实时交互需求。

**Barnes-Hut 方法**（Barnes and Hut, Nature 1986）是经典的快速近似方案。它通过构建空间八叉树，将远场粒子群以聚合节点的质心和总质量近似替代，将复杂度降至 $O(M \log M)$。其核心决策依赖于远场条件：

$$\frac{\|\mathbf{q} - \tilde{\mathbf{p}}_\alpha\|}{|B_\alpha|} \geq \beta$$

当查询点到节点质心的距离与节点包围盒尺寸之比超过阈值 $\beta$ 时，该节点被视为"远场"，直接使用其聚合信息参与求和，不再深入子节点。由此产生的 Barnes-Hut 估计器为：

$$F_{BH}(\mathbf{q}, \beta) = \sum_{T_a \in D(\mathbf{q}, \beta)} \tilde{m}_a f(\tilde{\mathbf{p}}_a, \mathbf{q})$$

尽管 Barnes-Hut 在 CPU 上取得了巨大成功，其 GPU 并行化却面临根本性困难。**核心瓶颈在于深度树遍历导致的线程发散**：不同查询点的远场条件判定结果各异，使得各线程需要遍历的树深度和路径截然不同。即便采用栈式遍历和 warp voting 等 GPU 优化策略，线程束内的执行路径分歧仍然严重，导致内存访问延迟和计算资源浪费。这一瓶颈使得标准 Barnes-Hut 在 GPU 上的效率远未达到硬件潜力。

本文的**核心动机**正是突破这一并行化瓶颈。作者洞察到：Barnes-Hut 的细节层次（LOD）近似族本质上可视为控制变量——它不是被抛弃的近似，而是构建更优估计器的基石。通过将确定性树遍历替换为随机路径采样，并用俄罗斯轮盘赌概率控制路径长度，可以构造一个**无偏的蒙特卡洛估计器**。该估计器用少量随机路径样本替代完整的确定性遍历，从根本上减少线程发散，在保持甚至提升精度的同时实现显著的 GPU 加速。

## 核心创新

本文的核心创新在于将**确定性的层次细节（LOD）近似族重新诠释为控制变量**，构建了一个**无偏的蒙特卡洛估计器**，从而将GPU上原本因深度树遍历而严重发散的线程执行，转化为统一、可预测的随机路径采样过程。这一范式转换通过三个关键机制实现。

### 从确定树遍历到随机路径采样

标准Barnes-Hut方法（Barnes and Hut, Nature 1986）通过远场条件 $\beta$ 决定是否继续向子节点深入，形成一条确定性的截断路径。该方法在GPU上因不同查询点触及不同深度的节点，导致严重的**线程发散**和内存访问延迟——这是其难以高效并行化的根本瓶颈。

本文提出的**随机Barnes-Hut近似**将这一过程彻底随机化：路径的截断长度不再由 $\beta$ 硬性决定，而是由基于远场比率的**俄罗斯轮盘赌概率** $\rho_{i,k}(\mathbf{q})$ 随机决定（Eq. 5）。具体而言，路径从当前节点 $k$ 延续到子节点 $k+1$ 的概率为：

$$\rho_{i,k}(\mathbf{q}) = \min\left(1, \frac{\max(1, \tilde{\beta}_i(\mathbf{q}, k))}{\tilde{\beta}_i(\mathbf{q}, k+1)}\right)$$

其中 $\tilde{\beta}_i(\mathbf{q}, k)$ 是查询点 $\mathbf{q}$ 到节点 $k$ 的远场比率。该概率在远场区域趋近于 $1/d$（$d$ 为每维分支因子），保证了路径在远场的自然截断倾向；在近场区域则被夹紧至有效范围。这一设计使得所有线程执行**统一长度的随机路径**，大幅减少线程发散。

### 贡献交换：Barnes-Hut作为控制变量

将Barnes-Hut的LOD近似族视为控制变量，是本文最核心的理论洞察。对于每条源点 $i$ 沿树路径的伸缩和表示（Eq. 3）：

$$F_{\mathcal{P}_i}(\mathbf{q}) = m_i f(\tilde{\mathbf{p}}_{i,0}, \mathbf{q}) + \sum_{k=1}^{d_i} m_i (f(\tilde{\mathbf{p}}_{i,k}, \mathbf{q}) - f(\tilde{\mathbf{p}}_{i,k-1}, \mathbf{q}))$$

Barnes-Hut等价于在 $\beta$ 决定的截断长度 $\ell_i(\beta)$ 处截断该路径（Eq. 4）。本文的估计器则通过**贡献交换** $\Delta_{i,k}$（Eq. 6）将对偶采样引入：

$$\Delta_{i,k} = \left(\sum_{c \in C(T_{i,k})} \tilde{m}_c f(\tilde{\mathbf{p}}_c, \mathbf{q})\right) - \tilde{m}_{i,k} f(\tilde{\mathbf{p}}_{i,k}, \mathbf{q})$$

其中 $C(T_{i,k})$ 是节点 $T_{i,k}$ 的所有子节点集合。$\Delta_{i,k}$ 本质上是**父节点近似与子节点精确和之间的差异**——这正是Barnes-Hut近似所忽略的误差项。通过将这一差异作为控制变量纳入估计器，单路径无偏估计器（Eq. 7）得以构建：

$$\hat{F}_1(\mathbf{q}) = \tilde{m}_{I,0} f(\tilde{\mathbf{p}}_{I,0}, \mathbf{q}) + \sum_{k=1}^{K} \frac{\Delta_{I,k-1}}{p(I \in T_{I,k-1}) p(K \geq k)}$$

该估计器的无偏性在Theorem 3.1中得到严格证明（见Appendix A），使得**首次在快速求和中同时获得Barnes-Hut的速度和无偏估计的统计保证**。

### 并行策略的根本性改变

标准Barnes-Hut的GPU优化（栈式遍历 + warp voting）虽已代表较高实现水平，但本质上仍受限于线程发散。本文通过以下并行策略的改变实现根本性加速：

- **统一随机路径采样**：所有查询点执行相同结构的随机路径，跨warp使用相同种子产生一致的RNG状态，消除因路径深度差异导致的发散。
- **树分支因子从8增至64**（每维 $d=2 \rightarrow d=4$）：更宽的分支因子使得路径在更少步数内到达远场截断，进一步减少路径长度差异。
- **域分层**：以根节点的直接子节点作为路径起点，在子域间均匀分配样本，提供基础的分层采样结构。

### 性能与误差的显著提升

在116个网格数据集上（Table 1），$S=1$ 时本方法的**平均误差比Barnes-Hut（$\beta=2$）低约5倍，中位数误差低约17倍**，同时**速度快2倍以上**。在Fig. 1的电力塔电势场计算中，随机方法在**8 ms内计算超过4万亿粒子对相互作用**，Barnes-Hut需14 ms，暴力方法需2800 ms。在相同中位数误差下，随机方法**比优化的Barnes-Hut快至多9.4倍**（Fig. 5）。

值得注意的是，这些加速并非通过缩水基线获得——Barnes-Hut已采用栈式遍历和warp voting进行GPU优化，而本方法通过根本性的算法重构实现了超越。

## 整体框架

本文提出的随机Barnes-Hut近似方法将传统Barnes-Hut的细节层次（LOD）近似族重新解释为控制变量，构建了一个无偏的蒙特卡洛估计器，从而将GPU上原本因深度树遍历导致的线程发散问题转化为统一的随机路径采样问题。其整体pipeline由以下核心模块串联而成：

### 1. 空间树构建（预处理）

在CPU上构建一棵空间树（octree），分支因子为 $d=4$（总分支因子 $64$），并为每个节点预计算聚合质量 $\tilde{m}_a$ 和质心 $\tilde{\mathbf{p}}_a$。该步骤与Barnes-Hut的预处理一致，两种方法在树构建上条件相同，构建时间均不计入GPU运行时间。

### 2. 域分层（Domain Stratification）

为降低估计器方差，将源点集按空间树结构划分为多个子域。默认策略直接使用根节点的直接子节点作为子域，每个子域独立进行后续的随机路径采样。这一设计在实现简单性和方差降低之间取得了平衡，作者同时指出未来可利用Barnes-Hut贡献节点 $D(\mathbf{q},\beta)$ 进行更优的分层。

### 3. 随机路径索引采样

对于每个查询点 $\mathbf{q}$，从各子域中均匀采样路径索引 $I$，确定一条从子域根节点到叶节点的完整树路径 $\mathcal{P}_I$。路径索引的RNG状态在warp内所有线程间保持一致，从而大幅减少GPU线程发散。

### 4. Russian Roulette路径截断

沿采样路径从根节点向下推进，在每个节点 $k$ 处根据远场比率计算延续概率：

$$\rho_{i,k}(\mathbf{q}) = \min\left(1, \frac{\max(1, \tilde{\beta}_i(\mathbf{q}, k))}{\tilde{\beta}_i(\mathbf{q}, k+1)}\right)$$

其中 $\tilde{\beta}_i(\mathbf{q}, k) = \|\mathbf{q} - \tilde{\mathbf{p}}_{i,k}\| / |B_{i,k}|$ 为当前节点的远场比率。以概率 $\rho_{i,k}$ 继续到子节点，以概率 $1 - \rho_{i,k}$ 在当前节点截断路径。该设计使得路径在远场（远近比率相近）时倾向于截断，在近场（远近比率变化剧烈）时倾向于深入，实现了自适应计算量分配。

### 5. 贡献交换（Contribution Swap）计算

在路径的每个截断步 $k$ 处，计算父节点与所有子节点贡献之差作为对偶采样项：

$$\Delta_{i,k} = \left(\sum_{c \in C(T_{i,k})} \tilde{m}_c f(\tilde{\mathbf{p}}_c, \mathbf{q})\right) - \tilde{m}_{i,k} f(\tilde{\mathbf{p}}_{i,k}, \mathbf{q})$$

这一交换项将父节点的粗糙近似替换为子节点集合的更精细近似，作为控制变量大幅降低估计器方差。该步骤需要扫描节点的所有 $64$ 个子节点，在高样本数时可能成为计算瓶颈。

### 6. 估计器聚合

最终的单一采样路径无偏估计器形式为：

$$\hat{F}_1(\mathbf{q}) = \tilde{m}_{I,0} f(\tilde{\mathbf{p}}_{I,0}, \mathbf{q}) + \sum_{k=1}^{K} \frac{\Delta_{I,k-1}}{p(I \in T_{I,k-1}) \, p(K \geq k)}$$

其中第一项为路径根节点的贡献（控制变量基值），第二项为沿截断路径的交换项经重要性加权后的累加。通过多条路径（$S$ 个样本）取平均可进一步降低噪声，但收敛率仅为 $O(S^{-1/2})$。

### 输入输出流

- **输入**：$M$ 个源点 $\{\mathbf{p}_i, m_i\}$ 及核函数 $f$，$N$ 个查询点 $\mathbf{q}_j$。
- **输出**：每个查询点的场值估计 $\hat{F}(\mathbf{q}_j)$，估计器具有无偏性（Theorem 3.1）。
- **可控参数**：每子域采样数 $S$（控制精度-速度权衡）。

### 与传统Barnes-Hut的流程对比

| 模块 | Barnes-Hut | 随机Barnes-Hut |
|------|-----------|---------------|
| 树分支因子 | $d=2$（8叉树） | $d=4$（64叉树） |
| 遍历机制 | 确定性深度遍历，根据 $\beta$ 条件停止 | 随机路径采样，Russian roulette决定截断 |
| 估计器性质 | 有偏近似 | 无偏估计器 |
| 并行策略 | 栈式遍历 + warp voting，仍存在线程发散 | 统一随机采样，跨warp一致RNG状态 |
| 贡献聚合 | 直接使用贡献节点质心求和 | 贡献交换 + 重要性加权 |

整体而言，该方法将Barnes-Hut的“是否深入子节点”的确定性决策替换为“以多大概率深入”的随机决策，从而将原本导致GPU线程发散的变长树遍历转化为统一长度的随机路径采样，实现了显著的并行加速。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_02219/figures/006_Figure_5.jpg]]
*Figure 5: Convergence of our method vs Barnes-Hut, for 1 million random and grid query points, and $2 ^ { 1 5 }$ and $2 ^ { 2 0 }$ source points sampled from the Stanford bunny. Each point on the curves for our method (green) correspond to the number of samples per subdomain ?? from 1 to 32; each point on the curves for Barnes-Hut (orange) correspond to the accuracy parameter $\beta$ from 1 to 40. The ?? = 1 point on each curve for our method is outlined in black, and the point on the Barnes-Hut curve that achieves the same error is also marked (found by linear interpolation on the log-log plot). Across all source point sets and query distributions, and for both mean and median error, our method is roughly...*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_02219/figures/009_Figure_7.jpg]]
*Figure 7: Ground Truth Fig. 7. Winding numbers computed via fast stochastic summation from 2 ^ { 2 0 } sources. A full evaluation via brute force takes 887ms, while our method takes 7.80ms with 1 sample per subdomain, and 119ms with 16 samples per subdomain*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_02219/figures/011_Figure_8.jpg]]
*Figure 8: Ground Truth Fig. 8. Smooth distances computed via fast stochastic summation from 2 ^ { 2 0 } source points. A full evaluation via brute force takes 710ms, and our method takes 7.10ms with 1 sample per subdomain 605ms with 64 samples per subdomain*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_02219/figures/008_Figure_6.jpg]]
*Figure 6: In the example from Fig. 1, Barnes-Hut (left) exhibits discontinuous error patterns when the far field condition causes a change in contribution nodes, while our method (right) does not exhibit such artifacts and instead is more concentrated in regions where the field rapidly changes, while being lower on average than Barnes-Hut*

## 核心模块与公式推导

### 3.1 空间树构建与Barnes-Hut回顾

**树构建模块**：对 $M$ 个源点 $\mathbf{p}_i$（带质量 $m_i$）构建空间八叉树（octree），每个节点 $T_a$ 存储聚合质量 $\tilde{m}_a$ 和质心 $\tilde{\mathbf{p}}_a$。该预处理在CPU上完成，不计入GPU运行时。

**Barnes-Hut近似**：给定查询点 $\mathbf{q}$ 和远场阈值 $\beta$，从根节点遍历树，当满足远场条件时停止深入：

$$\frac{\|\mathbf{q} - \tilde{\mathbf{p}}_\alpha\|}{|B_\alpha|} \geq \beta$$

其中 $|B_\alpha|$ 为节点包围盒尺寸。满足条件的节点构成贡献节点集合 $D(\mathbf{q}, \beta)$，近似求和为：

$$F_{BH}(\mathbf{q}, \beta) = \sum_{T_a \in D(\mathbf{q}, \beta)} \tilde{m}_a f(\tilde{\mathbf{p}}_a, \mathbf{q}) \tag{2}$$

该近似是有偏的确定性估计，且GPU并行化时因深度树遍历导致严重的线程发散和内存访问延迟。

### 3.2 路径解释与伸缩和表示

**核心洞察**：将每个源点 $i$ 沿树路径的贡献表示为伸缩和（telescoping sum）。设路径 $\mathcal{P}_i$ 从根节点 $T_{i,0}$ 到叶节点 $T_{i,d_i}$，则精确贡献为：

$$F_{\mathcal{P}_i}(\mathbf{q}) = m_i f(\tilde{\mathbf{p}}_{i,0}, \mathbf{q}) + \sum_{k=1}^{d_i} m_i \left(f(\tilde{\mathbf{p}}_{i,k}, \mathbf{q}) - f(\tilde{\mathbf{p}}_{i,k-1}, \mathbf{q})\right) \tag{3}$$

Barnes-Hut等价于将所有路径在 $\beta$ 决定的截断长度 $\ell_i(\beta)$ 处截断：

$$F_{BH}(\mathbf{q}, \beta) = \sum_i F_{\mathcal{P}_{i,\ell_i(\beta)}}(\mathbf{q}) \tag{4}$$

这一表示为构建无偏蒙特卡洛估计器奠定了基础。

### 3.3 随机路径采样与无偏估计器

**模块一：域分层（Domain Stratification）**

将源点按空间子域分组，每个子域独立采样路径。实现中直接使用根节点的直接子节点作为子域，每个子域采样 $S$ 条路径。

**模块二：随机路径索引采样**

从子域内源点中均匀采样路径索引 $I$，跨warp使用相同种子保证RNG状态一致，减少线程发散。

**模块三：Russian Roulette路径长度决策**

定义远场比率 $\tilde{\beta}_i(\mathbf{q}, k) = \frac{\|\mathbf{q} - \tilde{\mathbf{p}}_{i,k}\|}{|B_{i,k}|}$，路径从节点 $k$ 延续到 $k+1$ 的概率为：

$$\rho_{i,k}(\mathbf{q}) = \min\left(1, \frac{\max(1, \tilde{\beta}_i(\mathbf{q}, k))}{\tilde{\beta}_i(\mathbf{q}, k+1)}\right) \tag{5}$$

该设计利用了远场下 $\tilde{\beta}_i(\mathbf{q}, k) \approx \tilde{\beta}_i(\mathbf{q}, k+1)$ 的收敛性质（Fig. 3），使概率在远场接近 $1/d$（$d$ 为每维分支因子），近场则自然截断。

**模块四：贡献交换（Contribution Swap）**

作为对偶采样（antithetic sampling）降低方差，计算父节点贡献与所有子节点贡献之和的差：

$$\Delta_{i,k} = \left(\sum_{c \in C(T_{i,k})} \tilde{m}_c f(\tilde{\mathbf{p}}_c, \mathbf{q})\right) - \tilde{m}_{i,k} f(\tilde{\mathbf{p}}_{i,k}, \mathbf{q}) \tag{6}$$

其中 $C(T_{i,k})$ 为节点 $T_{i,k}$ 的子节点集合。该交换项作为控制变量，将Barnes-Hut层级近似族纳入估计框架。

**模块五：估计器聚合**

单条随机截断路径的无偏估计器为：

$$\hat{F}_1(\mathbf{q}) = \tilde{m}_{I,0} f(\tilde{\mathbf{p}}_{I,0}, \mathbf{q}) + \sum_{k=1}^{K} \frac{\Delta_{I,k-1}}{p(I \in T_{I,k-1}) \, p(K \geq k)} \tag{7}$$

其中 $K$ 为随机截断长度，分母为路径索引和路径长度的联合概率。多子域多采样下的最终估计器为各路径估计的均值。**Theorem 3.1**（附录A）证明了该估计器的无偏性。

**与Barnes-Hut的关键差异**：本方法将细节层次（LOD）近似族视为控制变量，用少量随机路径样本替代完整确定性树遍历，从根本上消除了线程发散问题。树分支因子从Barnes-Hut的 $d=2$（总分支8）提升至 $d=4$（总分支64），进一步适配随机采样策略。

## 实验与分析

### 主要性能对比

本文在多个大规模求和任务上对比了随机Barnes-Hut近似与GPU优化的确定性Barnes-Hut实现（栈式遍历 + warp voting）以及暴力求和方法。核心发现是：**在相同或更低的误差水平下，随机方法实现了显著的加速**。

**Teaser场景（Fig. 1）**：在电力塔电势场计算中，222个表面采样源点对1000²切片平面上的每个查询点进行核函数求和。使用每个子域1个样本（S=1），随机方法在8 ms内计算了超过4万亿粒子对相互作用，而GPU优化的Barnes-Hut需要14 ms，暴力方法需要2800 ms。随机方法不仅速度快1.75倍，且视觉上几乎无可见artifact。

**大规模网格数据集（Table 1）**：在116个网格数据集上，使用引力势核函数在100³网格上评估。源点数量M分别为2^15、2^17和2^20，从每个网格表面采样。Barnes-Hut使用典型参数β=2，随机方法使用S=1：
- **时间**：随机方法平均4.04 ms（M=2^20时），Barnes-Hut为8.61 ms，加速约2.13倍。
- **中位绝对误差**：随机方法为7.45e-06，Barnes-Hut为1.67e-04，误差降低约22倍。
- **平均误差**：随机方法同样显著更低（约5倍），表明随机方法的误差分布更集中。

**收敛性对比（Fig. 5）**：在Stanford bunny模型上，源点数量为2^15和2^20，查询点分别为100万随机点和网格点。随机方法通过改变S（1到32）扫描误差-时间曲线，Barnes-Hut通过改变β（1到40）扫描。结果显示：
- 随机方法在S=1时即可达到Barnes-Hut需要2-8倍执行时间才能匹配的误差水平。
- 在所有源点集和查询分布下，随机方法比Barnes-Hut快约2-9倍。
- 随机方法的误差随S增加以O(S^{-1/2})速率收敛，在高样本数时性能优势减弱。

**误差分布特性（Fig. 6）**：Barnes-Hut因远场条件导致贡献节点离散切换，产生跳跃式的不连续误差模式；随机方法则无此类artifact，误差更集中于场快速变化的区域，且平均误差更低。

### 应用扩展

**缠绕数计算（Fig. 7）**：将随机求和方法应用于inside/outside测试，从2^20个源点计算缠绕数。暴力方法需887 ms，随机方法S=1时仅需7.80 ms（加速114倍），S=16时需119 ms。

**平滑距离场（Fig. 8）**：从2^20个源点计算平滑距离。暴力方法需710 ms，随机方法S=1时仅需7.10 ms（加速100倍），S=64时需605 ms。需注意的是，平滑距离场通过log-sum-exp估计引入额外偏差，不再保持无偏性。

### 消融实验

**俄罗斯轮盘赌策略（Fig. 9, Appendix C）**：对比了三种路径截断策略：
- **禁用Russian roulette**：产生几乎无噪声的结果，但速度慢约5倍。
- **固定概率1/2**：产生显著误差，因为近场节点被过早截断。
- **所提概率方案**：在略微增加误差（与禁用方案接近）的情况下达到约5倍加速，验证了基于远场比率设计概率的有效性。

**样本数影响（Fig. 5）**：增加S可减少噪声和误差，但收敛率为O(S^{-1/2})。在需要极高精度时，高样本数的随机方法可能不如Barnes-Hut高效，因为贡献交换的计算开销（需扫描节点所有子节点）在高样本数时可能成为瓶颈。

### 公平性说明

两种方法使用不同的树分支因子：Barnes-Hut使用d=2（总分支因子8），随机方法使用d=4（总分支因子64）。这是为各自算法最佳性能所做的选择，但可能影响直接比较的公平性。Barnes-Hut的实现已采用栈式遍历和warp voting进行GPU优化，代表了当前较高的GPU实现水平；随机方法通过统一随机路径采样和跨warp一致RNG状态减少线程发散，实现了本质性的并行策略改进。树构建均在CPU上完成，未计入GPU运行时间，两者条件一致。

### 失败模式与局限

1. **高样本数效率衰减**：当需要极高精度时，O(S^{-1/2})的收敛率导致性能优势减弱，贡献交换的计算开销可能成为瓶颈。
2. **平滑距离场的偏差**：log-sum-exp估计引入额外偏差，不再保持无偏性。
3. **异常值误差**：均匀采样路径索引未引入重要性采样，可能产生类似渲染中fireflies的异常值误差。
4. **域分层未优化**：仅使用根节点的直接子节点作为子域，未利用Barnes-Hut贡献节点进行更优分层。
5. **端到端效率**：树构建在CPU进行，未集成GPU树构建器（如fVDB），整体端到端加速受限。
6. **内存带宽**：未对节点数据进行量化和压缩优化，在未来扩展中可能成为障碍。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_02219/figures/010_Table_1.jpg]]
*Table 1: Timings and errors of our method and Barnes-Hut on a dataset of 116 meshes, run with typical parameter settings. Barnes-Hut is evaluated with $\beta$ = 2 , , and our algorithm is evaluated with S = 1 $\left( \mathrm { i . e . } \right$. , one sample per subdomain). We vary the number of source samples ?? to be $2 ^ { 1 5 }$ \ : ( 3 2 , 7 6 8 ) , $2 ^ { 1 7 }$ (131,072), and $2 ^ { 2 0 }$ \ : ( 1 , 0 4 8 , 5 7 6 )$_ { \div }$ , draw them from each mesh surface in the dataset, and their total gravitational potential kernel on a grid of 1 0 $0 ^ { 3 }$ points. The mean and standard deviation for each error statistic across the dataset are reported, and the better metric is highlighted in bold at each sourc...

## 方法谱系与知识库定位

### 1. 与基线方法的关系

本方法的核心创新在于将**Barnes-Hut**（Barnes and Hut, Nature 1986）从确定性近似框架迁移到蒙特卡洛估计框架，具体通过三个关键改造实现：

- **遍历机制替换**：标准Barnes-Hut采用确定性树遍历，根据远场条件 $\beta$ 决定是否继续深入子节点，产生贡献节点集合 $D(\mathbf{q}, \beta)$ 后直接求和。该方法在GPU上因深度树遍历导致严重线程发散和内存访问延迟。本方法将遍历替换为随机路径采样，路径长度由基于远场比率的Russian roulette概率 $\rho_{i,k}$ 决定，大幅降低线程发散。
- **估计器性质转换**：Barnes-Hut给出的是有偏的确定性近似 $F_{BH}(\mathbf{q}, \beta)$，偏差取决于 $\beta$ 的选择。本方法通过将LOD近似族视为控制变量，构建了**无偏**的蒙特卡洛估计器（Theorem 3.1），用贡献交换 $\Delta_{i,k}$ 作为对偶采样项降低方差。
- **树结构与并行策略适配**：Barnes-Hut在GPU上采用栈式遍历+warp voting优化，分支因子通常为 $d=2$（总分支因子8）。本方法将分支因子增至 $d=4$（总分支因子64），并采用统一随机路径采样，跨warp使用相同种子产生一致RNG状态，进一步减少发散。

在性能对比中，**Brute-force summation**（$O(MN)$）作为精确求和基准，在本文实验中计算2^20源点的缠绕数需887 ms，而本方法仅需7.80 ms（S=1），加速约114倍（Fig. 7）。

论文在讨论中提及**Fast Multipole Method (FMM)**（Greengard and Rokhlin, J. Comput. Phys. 1987）作为替代快速求和方法，但未将其作为直接实验基线进行系统对比。

### 2. 适用边界与条件

本方法在以下条件下表现出显著优势：

- **大规模全局核求和**：适用于引力势、库仑势、缠绕数、平滑距离场等全局支撑核函数的空间变化场计算。在电力塔电势场计算中，8 ms完成超过4万亿粒子对相互作用（Fig. 1）。
- **GPU友好场景**：方法专为GPU并行设计，通过随机路径采样消除确定性遍历的线程发散瓶颈。在116个网格数据集上，S=1时比优化的Barnes-Hut快约2.13倍，同时中位数误差低约22倍（Table 1）。
- **低到中等精度需求**：样本数S较小（如S=1）时即可获得优于Barnes-Hut典型参数（$\beta=2$）的误差水平。在相同中位数误差下，比Barnes-Hut快至多9.4倍。

方法在以下场景存在局限：

- **极高精度需求**：收敛率为 $O(S^{-1/2})$，高样本数时性能优势减弱（Fig. 5），可能不如调高 $\beta$ 的Barnes-Hut。
- **平滑距离场**：通过log-sum-exp估计引入额外偏差，不再保持无偏性。
- **端到端效率**：树构建仍在CPU完成，未集成GPU树构建器（如fVDB），整体端到端加速受限。

### 3. 已知局限与失败模式

- **域分层策略简单**：仅使用根节点的直接子节点作为子域，未利用Barnes-Hut贡献节点 $D(\mathbf{q}, \beta)$ 进行更优分层，可能损失方差缩减机会。
- **采样效率瓶颈**：采用均匀采样路径索引，未引入重要性采样，可能产生类似渲染中fireflies的异常值误差。
- **贡献交换开销**：需要扫描节点所有子节点计算 $\Delta_{i,k}$，在高样本数时可能成为瓶颈。
- **内存带宽未优化**：未对节点数据进行量化和压缩，未来扩展时内存带宽可能成为障碍。
- **固定概率方案的失败**：消融实验表明，使用固定概率1/2的Russian roulette会产生显著误差，验证了所提基于远场比率的概率设计的必要性（Fig. 9, Appendix C）。

### 4. 开放问题与未来方向

论文明确提出的开放问题包括：

1. **重要性采样设计**：如何设计无线程发散的重要性采样方案，基于查询点距离优化路径索引采样，以提高样本效率？
2. **样本重用机制**：能否借鉴ReSTIR思路，在空间和时间上重用路径样本，进一步提升效率？
3. **连续积分推广**：能否将方法推广到连续积分，提供类似于Walk on Spheres与有限元方法之间的替代方案？
4. **线程发散完全消除**：是否可能使用单次估计器（single-term estimators）和不同数据结构完全消除线程发散？
5. **数据压缩**：通过量化和压缩节点数据是否能在不引入偏差的前提下显著降低内存流量？
6. **最优概率计算**：能否结合零方差理论预先为给定查询点计算所有Russian roulette概率以最小化方差？
7. **去噪结合**：如何将随机求和方法与去噪器（如深度学习降噪）结合，消除低样本时的噪声artifact？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Stochastic_Barnes_Hut_Approximation_for_Fast_Summation_on_the_GPU.pdf]]

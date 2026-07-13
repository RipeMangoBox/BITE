---
title: "Fast Escape, Slow Convergence: Learning Dynamics of Phase Retrieval under Power-Law Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Fast_Escape_Slow_Convergence_Learning_Dynamics_of_Phase_Retrieval_under_Power_Law_Data.pdf
project_link: null
code_link: null
openreview_forum_id: Ae4eZpkXBX
aliases:
- TPGFAAPR
- FESCLDPRUPLD
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "输入协方差的幂律谱衰减指数 a（a > 1 控制谱的厚尾程度）"
primary_logic: "各向异性相位检索的梯度流呈现三阶段轨迹：（i）快速逃离低相关性平庸区；（ii）汇总统计量的缓慢收敛；（iii）小特征值方向的谱尾学习。这一分解揭示了逃离-收敛权衡，并导出了显式的MSE缩放定律，收敛时间和最终误差由谱衰减指数 a 定量决定。"
claims:
- "各向异性下收敛速度显著慢于各向同性指数衰减，反映了学习小特征值方向的困难。"
- "梯度流下关键指标展现清晰的三阶段演化：快速逃离、缓慢收敛、谱尾学习。"
- "动力学系统是无限维的，由移位算子和秩一扰动生成，无法有限维闭合。"
- "利用Duhamel公式和Volterra方程化简，推导出显式的MSE缩放律。"
---

# Fast Escape, Slow Convergence: Learning Dynamics of Phase Retrieval under Power-Law Data

> [!tip] 核心洞察
> 各向异性相位检索的梯度流呈现三阶段轨迹：（i）快速逃离低相关性平庸区；（ii）汇总统计量的缓慢收敛；（iii）小特征值方向的谱尾学习。这一分解揭示了逃离-收敛权衡，并导出了显式的MSE缩放定律，收敛时间和最终误差由谱衰减指数 a 定量决定。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 快速逃离，缓慢收敛：幂律数据下相位检索的学习动力学 |
| 英文题名 | Fast Escape, Slow Convergence: Learning Dynamics of Phase Retrieval under Power-Law Data |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Ae4eZpkXBX) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | Three-phase Gradient Flow Analysis for Anisotropic Phase Retrieval |
| Dataset | Synthetic Phase Retrieval under Power-Law Covariance (Online SGD, d=10^4), Synthetic Data (Population GD, d=1000), d=300) |

> [!tip] 效果简介
> - Synthetic Phase Retrieval under Power-Law Covariance (Online SGD, d=10^4) 上，MSE decay 为 Slower power-law decay for a>1，对比 Exponential decay (isotropic case a=0)，变化 Qualitatively different non-exponential decay。
> - Synthetic Data (Population GD, d=10^4) 上，Summary statistics (u, s) evolution 为 Three-phase trajectory with plateau，对比 Two-phase decay (isotropic)，变化 Extended plateau phase and slow convergence。
> - Synthetic Data (Population GD, d=1000) 上，Correlation u(t) growth rate 为 Faster escape for larger a，对比 Uniform growth (isotropic)，变化 Larger a leads to faster initial growth。

## 概要

相位检索（Phase Retrieval）是一类典型的非凸逆问题：从无相位测量 $y = \langle x, w^\star \rangle^2 + \xi$ 中恢复未知信号 $w^\star$，其中输入 $x \sim \mathcal{N}(0, Q)$ 服从各向异性高斯分布。当输入协方差 $Q$ 具有幂律谱 $\lambda_i \propto i^{-a}$（$a > 1$）时，学习动力学呈现出与各向同性情形（$Q = I$）截然不同的行为。

**核心瓶颈**在于：各向异性输入协方差使得梯度流动力学无法简化为低维系统，而是形成一个无限维耦合方程层次，其中与小特征值相关的方向学习极其缓慢，构成收敛的主要瓶颈。这一结构直接导致“快速逃离，缓慢收敛”的权衡——谱指数 $a$ 越大（谱越厚尾），初始阶段相关性增长越快，但随后的 MSE 衰减却越慢。

**核心洞察**是将梯度流轨迹分解为三个定性不同的阶段：
1. **Phase I — 快速逃离平庸区**：利用 Duhamel 公式和 Volterra 积分方程，证明低相关性状态下系统以指数速率逃离，且逃离速度随 $a$ 增大而加快。
2. **Phase II — 汇总统计量缓慢收敛**：两个标量汇总统计量 $s(t) = \|w(t)\|_Q^2$ 和 $u(t) = \langle w(t), w^\star \rangle_Q$ 向真值收敛，但收敛时间随维度 $d$ 和 $a$ 显著延长，期间 MSE 几乎不下降。
3. **Phase III — 谱尾学习**：当汇总统计量接近收敛后，每个坐标以速率 $8\lambda_i$ 向真值指数弛豫，小特征值方向的学习主导了最终 MSE 的幂律衰减。

**方法定位**：本文提出了一套基于 Duhamel 表示与分阶段近似的分析框架，将无限维耦合 ODE 系统化简为可处理的积分方程，并由此导出显式的 MSE 缩放定律。这一框架无需依赖各向同性假设或有限维闭合，直接刻画了谱衰减指数 $a$ 如何定量决定收敛时间和最终误差。

**主要实验发现**：
- 在线 SGD 和总体梯度下降均展现清晰的三阶段轨迹（Figure 1, Figure 2），验证了理论分解的合理性。
- 谱指数 $a$ 越大，Phase I 中相关性 $u(t)$ 增长越快（Figure 3），但后续 MSE 衰减越慢，形成明确的逃离-收敛权衡。
- Phase III 中冻结汇总统计量的近似与完整总体动力学高度吻合（Figure 4），支持缩放定律的推导。
- 在线 SGD 的噪声不改变三阶段定性结构，但 $a$ 增大会放大波动幅度（Figure 5）。

**局限与开放问题**：当前分析建立在总体梯度流（连续时间、无噪声）和精确幂律谱假设之上。如何将 Duhamel-Volterra 框架推广到离散时间 SGD 和有限样本设置，以及如何拓展到更一般的非线性模型（如多指数族或神经网络），是尚待解决的关键问题。



相位检索（Phase Retrieval）是一类典型的非线性逆问题：给定无相位量测 $y = \langle x, w^\star \rangle^2 + \xi$，其中 $x \sim \mathcal{N}(0, Q)$ 为各向异性高斯输入，目标是从观测中恢复未知信号 $w^\star$。该问题广泛存在于光学成像、X射线晶体学和无线通信等领域，其学习动力学在高维非凸优化中具有重要的理论标杆意义。

传统相位检索的理论分析长期依赖于**各向同性高斯数据**假设（即 $Q = I$），在此设定下，总体损失可被两个标量汇总统计量完全刻画：

$$\mathcal{L}(w) = 3s^2 + 3s_\star^2 - 4u^2 - 2s_\star s$$

其中 $s = \|w\|_Q^2$ 和 $u = \langle w, w^\star \rangle_Q$ 将高维动力学压缩为二维系统，收敛呈现指数衰减。然而，真实数据几乎总是各向异性的——输入特征在不同方向上具有差异极大的方差，其协方差谱通常呈现厚尾衰减。这一根本性的模型失配导致现有理论无法解释实际训练中观察到的缓慢收敛现象，构成了该领域的核心缺口。

本文直面这一缺口，研究**幂律谱数据**下的相位检索学习动力学。具体而言，假设协方差矩阵 $Q$ 的特征值按幂律衰减：

$$\lambda_i = \frac{i^{-a}}{\sum_{j=1}^d j^{-a}}, \quad a > 1$$

其中参数 $a$ 控制谱的厚尾程度：$a$ 越大，小特征值方向的方差衰减越剧烈，数据分布的异质性越强。这一设定捕捉了高维数据分析中普遍存在的低秩或近似低秩结构，使得问题从可化简的二维系统跃迁为**无限维耦合动力学**。

核心动机在于回答一个根本性问题：**输入谱的衰减如何定量地支配非线性回归的有限时间收敛行为？** 初步实验证据已揭示了令人意外的现象：如 Figure 1 所示，当 $a > 1$ 时，在线 SGD 下的 MSE 衰减远慢于各向同性情形的指数收敛，且 $a$ 越大收敛越慢。与此同时，Figure 3 却表明，较大的 $a$ 反而加速了初始阶段相关性 $u(t)$ 的增长——这暗示着一种“快速逃离、缓慢收敛”的内在权衡。这一矛盾现象无法被现有各向同性理论解释，迫切需要新的分析框架来揭示各向异性谱与学习轨迹之间的因果机制。



## 核心方法与创新机理

本工作的核心创新在于将各向异性相位检索的梯度流动力学分解为三个可分析的阶段，并在此基础上导出了显式的MSE缩放定律。这一分解突破了传统各向同性假设下动力学可有限维闭合的限制，揭示了输入协方差谱对收敛速度的定量控制机制。

### 关键变更点：从各向同性到各向异性幂律谱

传统相位检索的动力学分析通常假设输入协方差为单位阵（$Q = I$），此时损失函数仅依赖于两个汇总统计量 $s(t) = \|w(t)\|^2$ 和 $u(t) = \langle w(t), w^\star \rangle$，动力学系统可简化为二维ODE。本工作将这一假设替换为**各向异性幂律谱**：

$$\lambda_i = \frac{i^{-a}}{\sum_{j=1}^d j^{-a}}, \quad a > 1$$

其中谱衰减指数 $a$ 成为控制学习动力学的核心因果旋钮。在这一设定下，梯度流在每个坐标上的演化由特征值加权：

$$\dot{w}_i(t) = 4\lambda_i (s_\star - 3s(t)) w_i(t) + 8\lambda_i u(t) w_i^\star$$

这一变更是根本性的：它使得动力学系统不再能简化为有限维ODE，而是形成一个无限维耦合方程层次（Proposition 3, Eq. 3.4）。小特征值对应的方向学习极其缓慢，成为收敛的主要瓶颈。

### 三阶段动力学分解

为驯服这一无限维系统，本工作提出了三阶段分解策略，每个阶段采用不同的近似手段：

**Phase I：快速逃离平庸区。** 在初始阶段，估计量 $w(t)$ 与真值 $w^\star$ 的相关性 $u(t)$ 从接近零的水平快速增长至常数阶。利用Duhamel公式将无限维系统投影为关于 $u(t)$ 的封闭Volterra积分方程：

$$u(t) = a_0(t) + 8\int_0^t K(t-\tau)u(\tau)d\tau$$

分析表明，逃离时间 $T_1 = O(\log d)$，且谱指数 $a$ 越大，逃离速度越快（Figure 3）。这一反直觉现象源于厚尾谱将更多能量集中在少数大特征值方向，使信号更快被捕获。

**Phase II：汇总统计量的缓慢收敛。** 在相关性建立后，$s(t)$ 和 $u(t)$ 向1收敛。通过谱分割技术——将特征值以截断值 $\lambda_c$ 分为“头部”和“尾部”——本工作证明收敛时间满足 $T_2 = T_1' + O(\varepsilon^{-2a/(a-1)}\log(1/\varepsilon))$。关键发现是：$a$ 越大，Phase II收敛越慢，这与Phase I的逃离速度形成**逃离-收敛权衡**。

**Phase III：谱尾学习。** 当汇总统计量接近1后，各坐标的动力学近似为独立的指数弛豫：

$$\dot{w}_i(t) \approx 8\lambda_i (w_i^\star - w_i(t))$$

冻结 $u$ 和 $s$ 后，MSE的演化由谱混合函数 $\widehat{S}_d(\tau)$ 主导：

$$\mathrm{MSE}(T_2+\tau) = (1+O(\varepsilon))\mathrm{MSE}(T_2)\widehat{S}_d(\tau) + O\left(\varepsilon^2\tau^2 \frac{1}{d}s_\star^{(2)}\right)$$

这一近似在数值实验中得到验证（Figure 4），其误差可控，足以捕捉MSE缩放定律的渐进行为。

### 方法论创新：Duhamel-Volterra框架

本工作在技术上引入了一个系统性的分析框架：将无限维相关动力学提升为移位算子 $B$ 加秩一扰动 $S$ 的紧凑算子形式：

$$\dot{U}(t) = \big(4(1-3s(t))B + 8S\big) U(t)$$

然后通过Duhamel公式获得显式解表示，再投影回低维量获得可分析的Volterra方程。这一“提升-求解-投影”策略使得原本无法有限维闭合的系统变得可处理，为分析其他各向异性非线性学习问题提供了可复用的模板。

### 证据强度总结

三阶段分解的核心主张得到了多层次的实验验证：Figure 2在总体梯度流下清晰展示了MSE、$u(t)$ 和 $s(t)$ 的三阶段演化轨迹；Figure 1证实在线SGD下各向异性收敛显著慢于各向同性指数衰减；Figure 3验证了Phase I中 $a$ 越大逃离越快的反直觉预测；Figure 4证实了Phase III近似的有效性。理论方面，Proposition 3和Lemma 1严格建立了无限维系统的Duhamel表示，Theorem 2和Corollary 3导出了显式的MSE缩放律。所有关键主张的证据置信度均在0.9以上。



本文提出了一套**三阶段梯度流分析框架**（Three-phase Gradient Flow Analysis），用于解析各向异性输入协方差下相位检索问题的学习动力学。该框架的核心思想是：将原本无法有限维闭合的无限维耦合常微分方程系统，通过**升维-求解-投影**的策略，分解为三个具有不同主导机制的连续阶段，从而在每个阶段内应用有针对性的近似，最终导出均方误差（MSE）的显式缩放定律。

### 问题设定与输入

系统接收的输入为：

- **数据分布**：$x \sim \mathcal{N}(0, Q)$，其中协方差矩阵 $Q$ 的特征值服从幂律衰减
  $$\lambda_i = \frac{i^{-a}}{\sum_{j=1}^d j^{-a}}, \quad a > 1$$
  谱指数 $a$ 是控制各向异性程度的核心因果旋钮——$a$ 越大，谱的厚尾越显著，小特征值方向占比越重。

- **观测模型**：$y = \langle x, w^\star \rangle^2 + \xi$，即二次非线性相位检索问题，目标是从测量值中恢复真实权重 $w^\star$。

- **损失函数**：总体损失仅依赖于两个汇总统计量——加权范数 $s(t) = \|w(t)\|_Q^2$ 和加权内积 $u(t) = \langle w(t), w^\star \rangle_Q$：
  $$\mathcal{L}(w) = 3s^2 + 3s_\star^2 - 4u^2 - 2s_\star s$$
  这一低维结构（Proposition 1）是后续分析的基础，但在各向异性下，$s(t)$ 和 $u(t)$ 的演化本身并不封闭，需要引入更高阶的加权重叠量。

### 核心瓶颈与无限维层次结构

在各向同性情形（$Q = I$）下，动力学可简化为关于 $s(t)$ 和 $u(t)$ 的二维封闭系统，收敛呈指数衰减。然而，当 $Q$ 为各向异性幂律谱时，梯度流在每个坐标上的分量为：
$$\dot{w}_i(t) = 4\lambda_i (s_\star - 3s(t)) w_i(t) + 8\lambda_i u(t) w_i^\star$$
其中 $\lambda_i$ 对每个坐标施加不同的缩放，导致必须引入一族高阶加权统计量：
$$s^{(k)}(t) = \|w(t)\|_{Q^k}^2, \quad u^{(k)}(t) = \langle w(t), w^\star \rangle_{Q^k}$$
这些量构成一个**无限维耦合常微分方程层次**（Proposition 3），无法有限维闭合——这是各向异性下收敛缓慢的根本瓶颈。

### 三阶段分解与模块关系

框架将梯度流轨迹分解为三个连续阶段（Figure 2 提供了典型轨迹的可视化验证），每个阶段由不同的主导机制刻画，对应不同的分析模块：

| 阶段 | 模块名称 | 核心角色 | 关键分析工具 |
|------|----------|----------|--------------|
| **Phase I** | 逃离平庸区 | 从低相关性初始状态快速建立与信号的常数阶相关性 $u(t)$ | Duhamel公式 + Volterra积分方程 |
| **Phase II** | 汇总统计量收敛 | 使 $s(t)$ 和 $u(t)$ 逼近其目标值 $1$，为后续逐坐标学习铺路 | 谱分割 + 截断Volterra方程 |
| **Phase III** | 谱尾学习 | 在小特征值方向上逐坐标指数弛豫至真值，决定最终MSE衰减律 | 冻结汇总统计量近似 + 谱平均渐近分析 |

**Phase I** 利用 Duhamel 公式将无限维系统升维至算子空间：
$$\dot{U}(t) = \big(4(1-3s(t))B + 8S\big) U(t)$$
其中 $B$ 为右移算子，$S$ 为秩一扰动。通过投影回 $u(t)$，得到封闭的 Volterra 积分方程：
$$u(t) = a_0(t) + 8\int_0^t K(t-\tau)u(\tau)d\tau$$
借此可分析 $u(t)$ 的指数增长率，确定逃离时间 $T_1 = O(\log d)$。一个反直觉的发现是：**$a$ 越大，Phase I 逃离越快**（Figure 3 验证），因为大特征值方向的信号被更有效地放大。

**Phase II** 在 $u(t)$ 达到常数阶后，分析 $s(t)$ 向 $1$ 的收敛。通过将谱分割为“头部”（$\lambda_i \ge \lambda_c$）和“尾部”（$\lambda_i < \lambda_c$），在 Volterra 框架下控制误差 $\Delta(t) = 1 - s(t)$，得到收敛时间：
$$T_2 = T_1' + O\big(\varepsilon^{-2a/(a-1)} \log(1/\varepsilon)\big)$$
此阶段结束时，MSE 仍维持在初始水准附近（Proposition 4），尚未显著下降。

**Phase III** 是决定最终精度的关键。当汇总统计量充分接近 $1$ 后，冻结 $s(t) \approx 1$ 和 $u(t) \approx 1$，每个坐标的动力学退耦为独立的指数弛豫：
$$\dot{w}_i(t) \approx 8\lambda_i (w_i^\star - w_i(t))$$
由此导出 MSE 的显式分解（Theorem 2）：
$$\text{MSE}(T_2+\tau) = (1+O(\varepsilon))\,\text{MSE}(T_2)\,\widehat{S}_d(\tau) + O\big(\varepsilon^2\tau^2 \tfrac{1}{d}s_\star^{(2)}\big)$$
其中 $\widehat{S}_d(\tau)$ 是谱混合函数，其渐近行为由谱指数 $a$ 定量决定，在早、中、晚三个时间尺度呈现不同的衰减律（Corollary 3）。

### 输出与缩放定律

框架的最终输出是 **MSE 的显式缩放定律**：收敛不再是各向同性的指数衰减，而是由幂律谱指数 $a$ 决定的多尺度行为。$a$ 越大，Phase I 逃离越快，但 Phase II 和 Phase III 的收敛越慢——形成一种**“逃离-收敛”权衡**。这一权衡在 Figure 1 的在线 SGD 实验中得到验证：$a > 1$ 时 MSE 衰减显著慢于各向同性情形，且衰减曲线呈现定性的非指数特征。

### 局限与边界

框架当前建立在**总体梯度流**（连续时间、无噪声）假设之上，对离散时间 SGD 和有限样本效应的量化推广仍是开放问题。此外，分析严格依赖高斯输入和精确幂律谱假设；实际数据谱的偏离可能导致缩放定律的定量差异。Figure 5 的在线 SGD 实验表明三阶段定性结构对随机扰动具有鲁棒性，但 $a$ 增大会放大波动幅度，暗示有限样本下的理论推广需要新的分析工具。



### 问题设定与损失几何

考虑各向异性相位检索模型：观测 $y = \langle x, w^\star \rangle^2 + \xi$，其中输入 $x \sim \mathcal{N}(0, Q)$，协方差矩阵 $Q$ 具有幂律谱：

$$\lambda_i = \frac{i^{-a}}{\sum_{j=1}^d j^{-a}}, \quad a > 1$$

参数 $a$ 控制谱的厚尾程度——$a$ 越大，小特征值衰减越快，对应方向的信号能量越弱。

该问题的总体损失（population loss）仅依赖于两个汇总统计量 $s(t) = \|w(t)\|_Q^2$ 和 $u(t) = \langle w(t), w^\star \rangle_Q$：

$$\mathcal{L}(w) = 3s^2 + 3s_\star^2 - 4u^2 - 2s_\star s$$

其中 $s_\star = \|w^\star\|_Q^2$ 为常数。这一低维参数化是各向同性情形下动力学可简化为二维系统的原因——但在各向异性下，该简化失效。

---

### 无限维耦合层次：动力学无法闭合

梯度流在每个坐标上的演化由 $Q$ 的特征值加权（Proposition 3）：

$$\dot{w}_i(t) = 4\lambda_i (s_\star - 3s(t)) w_i(t) + 8\lambda_i u(t) w_i^\star$$

为描述整体动力学，需引入高阶加权重叠量：

$$s^{(k)}(t) := \|w(t)\|_{Q^k}^2, \quad u^{(k)}(t) := \langle w(t), w^\star \rangle_{Q^k}$$

其中 $k=1$ 即原始的 $s(t), u(t)$。这些量满足耦合的ODE层次（Proposition 3）：

$$\dot{s}^{(k)}(t) = 8(s_\star - 3s(t)) s^{(k+1)}(t) + 16 u(t) u^{(k+1)}(t)$$

**核心瓶颈**：与各向同性情形不同，该层次是无限维的，无法简化为有限维闭合系统。每个 $k$ 阶量依赖 $k+1$ 阶量，形成无穷递归——这正是各向异性下收敛缓慢的数学根源。

---

### Duhamel表示与Volterra化简

为处理无限维系统，将相关量提升至序列空间 $U(t) = (u^{(k)}(t))_{k \ge 1}$，动力学可紧凑表示为（Lemma 1）：

$$\dot{U}(t) = \big(4(1-3s(t))B + 8S\big) U(t)$$

其中 $B$ 为右移算子，$S$ 为秩一扰动。利用Duhamel公式得到显式解：

$$U(t) = e^{4B\Theta(t)}U_0 + 8\int_0^t e^{4B(\Theta(t)-\Theta(\tau))}(Bs_\star^\infty)u^{(1)}(\tau)d\tau$$

其中 $\Theta(t) = \int_0^t (1-3s(\tau))d\tau$。将该表示投影回第一分量 $u(t) = u^{(1)}(t)$，得到封闭的Volterra积分方程：

$$u(t) = a_0(t) + 8\int_0^t K(t-\tau)u(\tau)d\tau$$

这一化简是后续三阶段分析的基石：它将无限维耦合转化为关于 $u(t)$ 的单变量积分方程，使得各阶段的增长速率可被显式刻画。

---

### 三阶段分解与MSE缩放律

基于上述框架，轨迹被分解为三个连续阶段（Theorem 1, Theorem 2）：

**Phase I：快速逃离平庸区**。利用Volterra方程分析低相关性区域的指数增长，逃离时间 $T_1 = O(\log d)$。有趣的是，$a$ 越大逃离越快——因为大特征值方向的信号更强，初始相关性增长更迅速（Figure 3）。

**Phase II：汇总统计量缓慢收敛**。$s(t)$ 和 $u(t)$ 向1收敛，收敛时间 $T_2 = T_1' + O(\varepsilon^{-2a/(a-1)}\log(1/\varepsilon))$。此阶段结束时MSE仍维持在初始水平附近：

$$|\mathrm{MSE}(T_2) - \sigma_\star^2| \lesssim \Big(\frac{\varepsilon^{-a}}{d}\Big)^{1/3} + \Big(\frac{\log d}{d}\Big)^{1/3}$$

**Phase III：谱尾学习**。当汇总统计量接近1后，各坐标近似独立弛豫：

$$\dot{w}_i(t) \approx 8\lambda_i (w_i^\star - w_i(t))$$

冻结 $u, s$ 后，MSE的演化由谱混合函数 $\widehat{S}_d(\tau)$ 主导（Theorem 2）：

$$\mathrm{MSE}(T_2+\tau) = (1+O(\varepsilon))\mathrm{MSE}(T_2)\widehat{S}_d(\tau) + O\Big(\varepsilon^2\tau^2 \frac{1}{d}s_\star^{(2)}\Big)$$

其中均匀权重的谱平均 $S_d(\tau)$ 在三个时间尺度上呈现不同渐进行为：

$$S_d(\tau) = \begin{cases} 1-\frac{16}{d}\tau + O(\frac{\tau^2}{d}), & \beta_d\tau \ll 1,\\ 1-\Gamma(1-\frac{1}{a})\frac{x_d}{d}+o(\frac{x_d}{d}), & 1\ll x_d \ll d,\\ \le \exp(-\beta_d\tau d^{-a}), & x_d \gtrsim d. \end{cases}$$

这一缩放律直接揭示了**逃离-收敛权衡**：$a$ 越大，Phase I逃离越快，但Phase II/III中小特征值方向的谱尾学习越慢，整体MSE衰减从指数退化为幂律。



## 实验与关键发现

### 主实验结果

实验在合成相位检索任务上验证理论预测，数据生成遵循 $y = \langle x, w^\star \rangle^2 + \xi$，$x \sim \mathcal{N}(0, Q)$，协方差矩阵 $Q$ 的特征值按幂律 $\lambda_i \propto i^{-a}$ 衰减（$a > 1$）。所有实验均采用随机初始化，目标权重 $w^\star$ 的各分量独立同分布采样。

**各向异性下的 MSE 衰减。** Figure 1 展示了在线 SGD 下不同谱指数 $a$ 的 MSE 演化（对数-对数尺度，$d=10^4$）。核心发现是：当 $a > 1$ 时，收敛速度显著慢于各向同性情形（$a=0$）的指数衰减，且 $a$ 越大，衰减越慢。这直接验证了核心瓶颈——与小特征值相关的方向学习极其缓慢，导致整体收敛呈现幂律尾而非指数衰减。该现象在不同 $a$ 值下定性一致，表明结论对谱衰减强度具有鲁棒性。

**三阶段动力学轨迹。** Figure 2 在总体梯度下降（population GD）下追踪了 MSE、汇总统计量 $u(t) = \langle w, w^\star \rangle_Q$ 和 $s(t) = \|w\|_Q^2$ 的演化（$a=2$，$d=10^4$）。轨迹清晰呈现理论预测的三阶段结构：
- **Phase I（快速逃离）**：$u(t)$ 从接近零的初始值迅速增长至常数阶，逃离低相关性平庸区；
- **Phase II（缓慢收敛）**：$s(t)$ 和 $u(t)$ 经历漫长的平台期后逐步收敛至 1，MSE 在此期间几乎不下降；
- **Phase III（谱尾学习）**：汇总统计量接近 1 后，MSE 开始以幂律速度衰减，对应小特征值方向的指数弛豫。

Table 1 总结了各阶段停止时间的符号与量级：Phase I 逃离时间 $T_1 = O(\log d)$；Phase II 收敛时间 $T_2$ 以 $\varepsilon^{-2a/(a-1)} \log(1/\varepsilon)$ 的速度增长；Phase III 的 MSE 衰减则由谱平均函数 $S_d(\tau)$ 的渐近行为主导。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Ae4eZpkXBX/figures/004_Table_1.jpg]]
*Table 1: Summary of the different stopping times*

### 消融与分析

**谱指数 $a$ 的双重效应。** Figure 3 对比了不同 $a$ 值下相关性 $u(t)$ 的增长曲线（$d=1000$）。结果显示 $a$ 越大，Phase I 中 $u(t)$ 的逃离速度越快——这是因为大 $a$ 意味着协方差谱更集中于少数大特征值方向，信号在这些方向上的投影更强，从而加速了初始对齐。然而，Figure 1 同时表明 $a$ 越大，后续 MSE 衰减越慢。这揭示了各向异性相位检索中固有的“逃离-收敛”权衡：强各向异性有利于快速建立信号相关性，但代价是小特征值方向的谱尾学习更加困难，延长了整体收敛时间。

**Phase III 近似的有效性。** Figure 4 直接比较了 Phase III 近似（冻结 $u$ 和 $s$ 于 1，即 $\dot{w}_i(t) \approx 8\lambda_i(w_i^\star - w_i(t))$）与完整总体动力学的 MSE 演化（$d=300$）。两条曲线高度吻合，证实该近似足以捕捉缩放定律的渐进行为，为 Theorem 2 和 Corollary 3 的推导提供了经验支撑。需要手动验证的是，该近似在 $a$ 接近 1 的临界情形下是否仍然成立——此时谱衰减极慢，Phase II 和 Phase III 的分离可能不再清晰。

**随机梯度噪声的鲁棒性。** Figure 5 展示了在线 SGD 下不同 $a$ 值的完整动态（$d=1000$）。尽管存在随机梯度噪声，三阶段定性结构依然保持：Phase I 的快速逃离、Phase II 的平台期、Phase III 的缓慢衰减均可辨识。但 $a$ 增大时，噪声引起的波动幅度也相应放大，这在小特征值方向上尤为明显——因为这些方向的梯度信号本身较弱，噪声相对占比更高。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Ae4eZpkXBX/figures/006_Figure_5.jpg]]
*Figure 5: Dynamics of online SGD for different a , d = 1 0 0 0 , $\eta$ = 1 $0 ^ { - 3 }$*

### 失败模式与边界条件

理论分析建立在总体梯度流（连续时间、无噪声）假设之上，实验虽验证了离散 SGD 的定性一致性，但以下边界条件值得注意：

1. **离散时间效应**：理论预测的停止时间 $T_1, T_2$ 及其对 $\varepsilon$ 和 $a$ 的依赖关系在离散 SGD 中尚未充分量化。当学习率较大时，Phase II 平台期可能出现振荡，偏离理论预测的单调收敛。

2. **有限维效应**：MSE 的缩放定律（Theorem 2）包含维度 $d$ 的渐近项。当 $d$ 较小时（如 Figure 4 中 $d=300$），谱平均 $S_d(\tau)$ 的渐近展开精度有限，需要更大的 $d$ 才能观察到清晰的幂律区域。

3. **谱偏离理想幂律**：所有实验均假设协方差谱精确服从 $\lambda_i \propto i^{-a}$。实际数据的谱可能存在交叉点或多重缩放区域，此时三阶段分解是否仍然成立需要手动验证。

4. **初始化依赖**：理论对初始化条件提供了高概率保证，但极端初始化（如初始 $u(0)$ 恰好为零或 $s(0)$ 过大）可能导致 Phase I 逃离失败或时间延长。



## 定位与知识库关联

### 问题设定与理论定位

本文研究的是**各向异性高斯输入下的相位检索（phase retrieval）**，即从二次测量 $y = \langle x, w^\star \rangle^2$ 中恢复信号 $w^\star$，其中 $x \sim \mathcal{N}(0, Q)$，协方差矩阵 $Q$ 具有**幂律衰减特征值谱** $\lambda_i \propto i^{-a}$（$a > 1$）。这一设定区别于经典的各向同性相位检索文献——后者通常假设 $Q = I$，此时梯度流动力学可约化为关于两个汇总统计量 $u(t) = \langle w(t), w^\star \rangle$ 和 $s(t) = \|w(t)\|^2$ 的**有限维封闭系统**，收敛呈指数衰减。

本文的核心贡献在于揭示了：当输入协方差偏离各向同性时，动力学系统**无法有限维闭合**，而是形成由移位算子 $B$ 和秩一扰动 $S$ 生成的**无限维耦合 ODE 层次**（Proposition 3, Lemma 1）。这一无限维结构是各向异性下收敛缓慢的根本瓶颈，也是本文与现有理论工作的本质分野。

### 与现有工作的关系

#### 各向同性相位检索的动力学分析

各向同性相位检索的梯度流分析已较为成熟：损失函数 $\mathcal{L}(w)$ 仅依赖于 $u$ 和 $s$ 两个标量汇总统计量，动力学可降维为二维 ODE 系统。本文在 Proposition 1 中恢复了这一经典结果，但其核心推进在于**将分析从各向同性推广到各向异性幂律谱**。在这一推广中，各向同性情形对应于谱衰减指数 $a = 0$（所有特征值相等），而 $a > 1$ 则引入了小特征值方向的“谱尾学习”困难，导致收敛从指数衰减退化为**幂律或更慢的衰减**（Figure 1）。

#### 高维统计中的谱效应研究

本文的方法论与高维统计中利用**谱分解和积分方程**分析动力学的工作一脉相承，但在技术路径上有显著创新：

- **Duhamel公式与Volterra方程的联合使用**：本文通过将无限维耦合系统提升至 $\ell^2$ 空间，利用 Duhamel 公式获得显式解表示 $U(t) = e^{4B\Theta(t)}U_0 + 8\int_0^t e^{4B(\Theta(t)-\Theta(\tau))}(Bs_\star^\infty)u^{(1)}(\tau)d\tau$，再投影回 $u(t)$ 得到封闭的 Volterra 积分方程 $u(t) = a_0(t) + 8\int_0^t K(t-\tau)u(\tau)d\tau$。这种“提升—求解—投影”的策略为处理无限维耦合系统提供了系统性的分析框架。
- **三阶段分解范式**：不同于以往工作中将动力学视为单一阶段的做法，本文提出将轨迹分解为（i）快速逃离低相关性平庸区、（ii）汇总统计量缓慢收敛、（iii）小特征值方向谱尾学习的三个阶段，并在每个阶段采用不同的近似和控制策略。这一分解由实证观察驱动（Figure 2），并在理论上得到了严格的停止时间刻画（Table 1）。

#### 幂律谱与收敛速率的定量关系

本文导出的显式 MSE 缩放定律（Theorem 2, Corollary 3）将收敛速率与谱衰减指数 $a$ 直接挂钩：
- Phase I 逃离时间 $T_1 = O(\log d)$，且**更大的 $a$ 反而加速逃离**（Figure 3），因为大特征值方向的信号更集中；
- Phase II 收敛时间 $T_2 = T_1' + O(\varepsilon^{-2a/(a-1)} \log(1/\varepsilon))$，随 $a$ 增大而急剧增长；
- Phase III 的 MSE 由谱混合函数 $\widehat{S}_d(\tau)$ 主导，其渐近行为在早、中、晚三个时间尺度有不同缩放（Theorem 2, Eq. (4.2)）。

这种“快速逃离—缓慢收敛”的权衡是本文的核心洞察，为理解各向异性数据下非线性回归的训练动力学提供了新的理论视角。

### 适用边界与局限

1. **连续时间梯度流的假设**：所有理论分析建立在总体梯度流（population gradient flow）之上，即连续时间、无噪声、无限样本的极限。尽管 Figure 5 表明在线 SGD 保留了相同的三阶段定性结构，但**离散时间、有限样本效应的定量推广尚未完成**。这是从理论到实践的关键缺口。

2. **精确幂律谱的依赖**：分析假设 $Q$ 的特征值严格服从 $\lambda_i \propto i^{-a}$。实际数据的协方差谱可能偏离理想幂律（例如存在多个缩放区段或交叉点），此时三阶段分解和缩放定律的定量形式可能需要修正，但定性结构是否保持仍是开放问题。

3. **二次非线性的限制**：当前分析仅限于相位检索的二次测量模型。扩展到更一般的单指数族或多指数族模型，乃至浅层神经网络，可能需要发展新的分析工具。不过，作者在 Remark 2 中指出，各向异性梯度流可视为 $Q$-预条件化的各向同性流（$\dot{z}(t) = -Q \nabla \mathcal{L}_I(z(t))$），这一视角可能为推广提供桥梁。

4. **初始化与目标权重的依赖**：理论结果对初始化条件（小随机初始化）和目标权重的生成方式有一定依赖，但提供了高概率保证。Phase II 结束时的 MSE 界 $|\mathrm{MSE}(T_2) - \sigma_\star^2| \lesssim (\varepsilon^{-a}/d)^{1/3} + (\log d / d)^{1/3}$（Proposition 4）表明 MSE 在 Phase II 结束时仍维持在初始方差附近，尚未显著下降，这一“平台期”的持续时间对初始化敏感。

### 开放问题

1. **从梯度流到离散 SGD 的推广**：如何将当前的 Duhamel-Volterra 分析框架从连续时间梯度流推广到带噪声的离散时间 SGD，并量化有限样本效应？这是将理论预测与实验观测进行定量对比的前提。

2. **非理想谱的鲁棒性**：若输入协方差偏离精确幂律（如存在谱交叉或多次缩放），三阶段分解和缩放定律是否仍然成立？能否建立对谱扰动的稳定性理论？

3. **更广泛非线性模型的拓展**：能否将类似的三阶段分解拓展到更一般的非线性模型（如单/多指数族）或两层神经网络？Remark 2 中的预条件化视角可能为这一推广提供起点，但秩一扰动 $S$ 的结构在更复杂模型中可能不再保持。

4. **过渡区的精确刻画**：Phase II 和 Phase III 之间的过渡能否在更宽松的条件（如非高斯数据）下维持？显式常数是否可以被精确计算，而非仅给出渐近量级？

5. **逃离—收敛权衡的实践利用**：各向异性是否在网络训练中天然引发“逃离—收敛”权衡？实践中能否通过调整优化器或数据预处理策略来利用这一权衡——例如，在训练早期利用大特征值方向快速逃离，后期通过谱自适应学习率加速小特征值方向的收敛？



## 原文 PDF

![[paperPDFs/ICLR_2026/Fast_Escape_Slow_Convergence_Learning_Dynamics_of_Phase_Retrieval_under_Power_Law_Data.pdf]]

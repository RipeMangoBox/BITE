---
title: "Conformal Robustness Control: A New Strategy for Robust Decision"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Conformal_Robustness_Control_A_New_Strategy_for_Robust_Decision.pdf
project_link: null
code_link: null
openreview_forum_id: bt4Ahpemmi
aliases:
- CRCC
- CRCNSRD
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "将预测集优化中的约束从覆盖概率约束（P{Y∈U(X)}≥1-α）替换为显式的决策鲁棒性概率约束（P{φ(Y,z(X))≤r(X)}≥1-α），直接调节模型对鲁棒性水平的满足程度，消除结构性保守偏差。"
primary_logic: "直接优化预测集在鲁棒性约束下的性能指标（期望风险证书），可消除因使用覆盖代理约束带来的保守偏差，并通过统计学习理论保证非渐近鲁棒性和最优性，在多个任务中实现更低的风险证书与决策损失。"
claims:
- "在示例投资组合优化中，CRC在相同90%鲁棒性要求下将风险证书从CRO的1.93降至1.25，决策效率显著提升。"
- "定理3.1证明预测集优化问题与原始风险厌恶决策问题等价，从理论上保证CRC框架没有性能损失。"
- "在15维美国股票投资组合优化中，CRC-E的风险证书和决策损失均显著低于CRO-E和E2E-E，同时将鲁棒性保持在目标水平附近。"
- "理论结果（定理3.2和3.3）给出了鲁棒性差距与风险证书最优性的非渐近界，收敛速率为O(√(d log n / n))。"
---

# Conformal Robustness Control: A New Strategy for Robust Decision

> [!tip] 核心洞察
> 直接优化预测集在鲁棒性约束下的性能指标（期望风险证书），可消除因使用覆盖代理约束带来的保守偏差，并通过统计学习理论保证非渐近鲁棒性和最优性，在多个任务中实现更低的风险证书与决策损失。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 保形鲁棒控制：一种鲁棒决策的新策略 |
| 英文题名 | Conformal Robustness Control: A New Strategy for Robust Decision |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=bt4Ahpemmi) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Conformal Robustness Control (CRC) |
| Dataset | US Stock Portfolio Optimization |

> [!tip] 效果简介
> - US Stock Portfolio Optimization 上，Risk Certificate 为 CRC-E: 1.028±0.047，对比 CRO-E: 1.723±0.032，变化 -0.695。
> - US Stock Portfolio Optimization 上，Decision Loss 为 CRC-E: 0.251±0.015，对比 CRO-E: 0.319±0.009，变化 -0.068。

## 概要

**问题瓶颈**：传统基于覆盖的鲁棒优化（CRO）方法通过强制预测集满足覆盖概率约束 $P\{Y \in \mathcal{U}(X)\} \ge 1-\alpha$ 来间接保证决策鲁棒性。然而，覆盖概率仅是鲁棒性的充分条件而非必要条件，这一代理约束导致决策过于保守——风险证书远高于名义要求的鲁棒性水平。

**核心思路**：CRC 将优化约束从覆盖概率替换为显式的决策鲁棒性概率约束 $P\{\phi(Y, z(X)) \le r(X)\} \ge 1-\alpha$，直接调节模型对鲁棒性水平的满足程度，从结构上消除了保守偏差。理论等价性由定理3.1保证：预测集优化问题与原始风险厌恶决策问题在最小化期望风险证书的同时维持鲁棒性控制方面完全等价。

**方法定位**：CRC 属于“学习预测集以驱动下游决策”的方法谱系，与两类基线形成对比——**CRO**（Sun et al., 2023）采用覆盖约束与事后校准的“先预测后校准”范式；**端到端方法（E2E）**（Chenreddy & Delage, 2024; Yeh et al., 2024）通过直接最小化下游任务损失来学习不确定性集合。CRC 的核心差异在于将鲁棒性约束直接嵌入预测集优化目标，而非依赖覆盖代理或间接损失对齐。

**主要结果**：
- 在示例投资组合优化中，CRC 在相同 90% 鲁棒性要求下将风险证书从 CRO 的 1.93 降至 1.25（Figure 1），决策效率显著提升。
- 在美国股票投资组合优化（15维）中，CRC-E 的风险证书（1.028±0.047）和决策损失（0.251±0.015）均显著低于 CRO-E（1.723±0.032, 0.319±0.009），同时鲁棒性保持在目标水平 90.8% 附近（Table 1）。
- 理论层面，定理3.2和3.3给出了鲁棒性差距与风险证书最优性的非渐近界，收敛速率为 $O(\sqrt{d \log n / n})$。

**方法框架**：CRC 包含三个核心模块：（1）参数化预测集合构建（盒子、椭圆、多面体），将决策与风险证书参数化；（2）经验鲁棒性控制优化器（Algorithm 1），通过平滑对偶问题的梯度优化直接最小化期望风险证书；（3）测试时校准器（Algorithm 2, Cal-CRC），基于样本分割与保形推理提供有限样本鲁棒性保证。

在数据驱动的风险厌恶决策中，一个核心挑战是如何在不确定环境下做出既鲁棒又高效的决策。标准的条件风险优化（CRO）框架通过构建预测集来刻画结果变量的不确定性，然后在该集合上求解最坏情况下的决策问题。其基本逻辑是：先保证预测集以高概率覆盖真实结果，再基于该集合进行鲁棒优化。

然而，这一框架存在一个根本性的结构性偏差。CRO强制要求预测集满足覆盖概率约束：

$$\mathbb{P}\{Y \in \mathcal{U}(X)\} \ge 1 - \alpha$$

但覆盖概率仅仅是鲁棒性的充分条件，而非必要条件。一个预测集即使以恰好 $1-\alpha$ 的概率覆盖真实结果，其对应的鲁棒决策可能远超过实际所需的保守程度。换言之，**覆盖约束迫使决策者承担了超出名义鲁棒性要求的多余代价**。

这一偏差在Figure 1的示例投资组合优化中清晰可见：在相同的90%鲁棒性要求下，CRO方法产生的风险证书（risk certificate）为1.93，而CRC方法仅需1.25即可满足相同的鲁棒性水平。这意味着CRO框架因使用覆盖代理约束而引入了约55%的决策效率损失。

现有的改进尝试包括端到端（E2E）方法，通过直接最小化下游任务损失来学习不确定性集合。但这类方法缺乏对鲁棒性水平的显式控制，无法提供有限样本下的鲁棒性保证，且在实践中往往表现出不稳定的鲁棒性水平。

本文的核心动机在于：**将预测集优化中的约束从间接的覆盖概率约束替换为显式的决策鲁棒性概率约束**，从而消除结构性保守偏差。具体而言，直接要求：

$$\mathbb{P}\{\phi(Y, z(X)) \le r(X)\} \ge 1 - \alpha$$

即决策损失不超过风险证书的概率至少为 $1-\alpha$。这一约束直接对准了决策者真正关心的目标——决策本身的鲁棒性，而非预测集的统计覆盖性质。

通过这一约束替换，CRC框架在理论上实现了与原风险厌恶决策问题的等价性（定理3.1），消除了因使用代理约束带来的性能损失。同时，借助保形推理的样本分割校准机制，CRC能够提供有限样本下的鲁棒性保证，填补了现有方法在统计保证方面的空白。

## 核心方法与创新机理

CRC 的核心创新在于将预测集优化的约束条件从**覆盖概率约束**替换为**显式的决策鲁棒性概率约束**，从而消除传统 CRO 框架中固有的结构性保守偏差。

### 约束替换：从覆盖代理到鲁棒性直接控制

传统 CRO 方法（Sun et al., 2023）通过强制预测集满足覆盖概率约束 $\mathbb{P}\{Y \in \mathcal{U}(X)\} \ge 1 - \alpha$ 来间接保证鲁棒性。这一策略的根本缺陷在于：覆盖概率是鲁棒性的**充分条件而非必要条件**——预测集覆盖真实标签确实能保证决策鲁棒，但满足鲁棒性要求并不需要预测集完全覆盖标签空间。这种逻辑上的不对称导致 CRO 框架产生过度保守的决策，表现为风险证书（risk certificate）远高于名义要求。

CRC 将优化问题中的约束直接替换为决策鲁棒性概率约束：

$$\min_{\theta\in\Theta} \mathbb{E}[r_{\theta}(X)] \quad \mathrm{s.t.} \quad \mathbb{P}\{\phi(Y, z_{\theta}(X)) \le r_{\theta}(X)\} \ge 1-\alpha$$

这一改动是框架层面的根本性转变：优化目标不再要求预测集以高概率“包含”真实标签，而是直接要求决策损失不大于风险证书的概率达到指定水平。如 Figure 1 所示，在相同的 90% 鲁棒性要求下，CRO 的风险证书为 1.93，而 CRC 降至 1.25，决策效率显著提升。

### 理论等价性保证

CRC 的约束替换并非启发式简化。**定理 3.1** 证明了预测集优化问题与原始风险厌恶决策策略优化问题（RA-DPO）在最小化期望风险证书并维持鲁棒性控制方面是等价的。这一等价性从理论上保证了 CRC 框架没有因约束替换而引入性能损失——它精确地求解了 RA-DPO 问题，而 CRO 的覆盖约束则是对该问题的保守松弛。

### 经验优化与有限样本保证

为实现梯度优化，CRC 引入了两个关键机制：

1. **平滑对偶优化**（Algorithm 1）：通过高斯误差函数 $\tilde{\mathbf{1}}\{a \le b\} = \frac{1}{2}(1 + \mathrm{erf}(\frac{b - a}{\sqrt{2}\sigma}))$ 平滑指示函数，将约束优化转化为可微的拉格朗日对偶问题，支持端到端的梯度训练。

2. **测试时校准**（Algorithm 2, Cal-CRC）：基于样本分割与保形推理（full conformal prediction），对优化后的预测集进行单一半径参数的校准，提供有限样本鲁棒性保证（定理 4.1）。消融实验（Table 6）表明，校准步骤在保持较低风险证书的同时，将覆盖率从 59.8% 提升至 90.5%，是框架实用性的关键组件。

### 理论收敛性

定理 3.2 和 3.3 分别给出了鲁棒性差距与风险证书最优性的非渐近界，收敛速率为 $O(\sqrt{d \log n / n})$，为 CRC 的统计有效性提供了理论支撑。


保形鲁棒控制（Conformal Robustness Control, CRC）框架的核心思路是**将鲁棒决策问题转化为预测集合的参数化优化问题**，并通过显式的鲁棒性概率约束替代传统方法中的覆盖率代理约束，从根本上消除结构性保守偏差。整个框架由三个紧密协作的模块组成。

### 问题形式化：从覆盖率约束到鲁棒性约束

传统的情境鲁棒优化（Contextual Robust Optimization, CRO）方法通过构造预测集合 $\mathcal{U}(X)$ 来间接保证决策鲁棒性，其核心约束是覆盖率条件：

$$\mathbb{P}\{Y \in \mathcal{U}(X)\} \geq 1 - \alpha$$

然而，覆盖率只是鲁棒性的**充分条件而非必要条件**——即使预测集合完美覆盖了标签，决策损失 $\phi(Y, z(X))$ 超出风险证书 $r(X)$ 的概率仍可能远低于 $\alpha$，导致过度保守。

CRC 框架直接面向真正的鲁棒性需求：

$$\mathbb{P}\{\phi(Y, z(X)) \leq r(X)\} \geq 1 - \alpha$$

该约束显式要求决策损失不超过风险证书的概率至少为 $1-\alpha$，从而**直接调节模型对鲁棒性水平的满足程度**。定理 3.1 证明，预测集合优化问题（4）与原始的风险厌恶决策策略优化问题（3）在最小化期望风险证书方面是等价的，从理论上保证了 CRC 框架没有性能损失。

### 三模块 Pipeline

CRC 框架由以下三个模块串联构成：

**模块一：参数化预测集合构建。** 定义预测集合的几何结构，将决策 $z_\theta(X)$ 与风险证书 $r_\theta(X)$ 参数化为模型参数 $\theta$ 的函数。支持的集合形状包括：
- **盒形集（Box）**：由上下界函数 $h_\theta^{\mathrm{hi}}(X)$ 和 $h_\theta^{\mathrm{lo}}(X)$ 定义
- **椭圆集（Ellipsoid）**：由均值 $\mu_\theta(X)$ 和协方差 $\Sigma_\theta(X)$ 定义
- **多面体集（Polyhedron）**：由线性不等式组定义

对于给定的预测集合，决策与风险证书通过内部最大化问题确定：$z_\theta(X) = \arg\min_{z \in \mathcal{Z}} \max_{y \in \mathcal{U}_\theta(X)} \phi(y, z)$，$r_\theta(X) = \max_{y \in \mathcal{U}_\theta(X)} \phi(y, z_\theta(X))$。

**模块二：经验鲁棒性控制优化器（Algorithm 1）。** 在训练数据上求解参数化优化问题：

$$\min_{\theta \in \Theta} \mathbb{E}[r_\theta(X)] \quad \mathrm{s.t.} \quad \mathbb{P}\{\phi(Y, z_\theta(X)) \leq r_\theta(X)\} \geq 1-\alpha$$

为支持梯度优化，该模块使用高斯误差函数的平滑近似替代指示函数：

$$\tilde{\mathbf{1}}\{a \leq b\} = \frac{1}{2}\left(1 + \mathrm{erf}\left(\frac{b - a}{\sqrt{2}\sigma}\right)\right)$$

通过拉格朗日对偶方法将约束优化转化为无约束的极小极大问题，利用投影梯度上升更新拉格朗日乘子 $\lambda$，实现期望风险证书的最小化与鲁棒性约束的平衡。

**模块三：测试时校准器（Algorithm 2, Cal-CRC）。** 基于样本分割与完全保形推理，对优化后的预测集合进行半径校准。具体而言，将数据集划分为训练集 $\mathcal{D}_{\mathrm{train}}$ 和校准集 $\mathcal{D}_{\mathrm{cal}}$，在训练集上获得模型参数 $\hat{\theta}_0$，随后通过调节单一半径参数 $t \in \mathbb{R}^+$ 对预测集合进行嵌套扩展（如盒形集扩展为 $\{y: h_\theta^{\mathrm{lo}}(x) - t \leq y \leq h_\theta^{\mathrm{hi}}(x) + t\}$，椭圆集扩展为 $\{y: (y-\mu_\theta(x))^\top \Sigma_\theta^{-1}(x)(y-\mu_\theta(x)) \leq t\}$）。校准步骤为每个候选标签 $y$ 计算满足经验覆盖率约束的最小半径 $\hat{t}^y$，最终在测试时输出校准后的预测集合 $\mathcal{U}_{\mathrm{Cal}}(X_{n+1})$。定理 4.1 保证该过程提供**有限样本鲁棒性保证**：

$$\mathbb{P}\left\{\phi\left(Y_{n+1}, z_{\mathcal{U}_{\mathrm{Cal}}}(X_{n+1})\right) \leq r_{\mathcal{U}_{\mathrm{Cal}}}(X_{n+1})\right\} \geq 1 - \alpha$$

### 输入输出流

整个 Pipeline 的输入为标注数据集 $\mathcal{D}_n = \{(X_i, Y_i)\}_{i=1}^n$、名义鲁棒性水平 $\alpha$、以及预测集合的参数化形式选择（盒形/椭圆/多面体）。输出为训练好的模型参数 $\hat{\theta}$（或校准后的预测集合构造规则），以及对应的决策函数 $z_{\hat{\theta}}(X)$ 和风险证书函数 $r_{\hat{\theta}}(X)$。在推理阶段，给定新的协变量 $X_{n+1}$，框架输出决策 $z(X_{n+1})$ 及其风险证书 $r(X_{n+1})$，同时保证决策损失不超过风险证书的概率至少为 $1-\alpha$。

### 理论保证

理论分析（定理 3.2 和 3.3）给出了非渐近的鲁棒性差距上界与风险证书最优性上界，收敛速率为 $O(\sqrt{d \log n / n})$，其中 $d$ 为模型参数空间的覆盖数相关量，$n$ 为样本量。具体而言，鲁棒性差距 $\Delta_n$ 满足：

$$\mathbb{P}\{\phi(Y, z_{\hat{\theta}}(X)) \leq r_{\hat{\theta}}(X) \mid \mathcal{D}_n\} \geq 1-\alpha - \Delta_n$$

且 $\Delta_n$ 随样本量增大以 $O(\sqrt{d \log n / n})$ 速率收敛至零。这些保证为 CRC 框架的统计可靠性提供了严格的理论基础。

### 1. 从覆盖约束到鲁棒性约束：核心洞察

传统分布鲁棒优化（CRO）框架通过构建预测集 $\mathcal{U}(X)$ 来间接保证决策鲁棒性，其核心约束为覆盖概率条件：

$$\mathbb{P}\{Y \in \mathcal{U}(X)\} \ge 1 - \alpha$$

然而，覆盖概率仅是鲁棒性的**充分条件而非必要条件**——预测集包含真实标签并不意味着决策损失一定可控，反之亦然。这一结构性偏差导致CRO产生过度保守的决策，风险证书远超名义要求（如Figure 1所示，CRO在90%覆盖率下风险证书为1.93）。

CRC的核心创新在于将约束**从覆盖概率替换为显式的决策鲁棒性概率约束**：

$$\mathbb{P}\{\phi(Y, z(X)) \le r(X)\} \ge 1 - \alpha$$

其中 $\phi(y, z)$ 为决策损失函数，$z(X)$ 为决策变量，$r(X)$ 为风险证书。这一替换直接调节模型对鲁棒性水平的满足程度，从根源上消除了结构性保守偏差。

### 2. 预测集参数化与优化问题

CRC通过参数化预测集将鲁棒性约束转化为可优化形式。给定参数化预测集 $\mathcal{U}_\theta(\cdot)$，决策与风险证书定义为：

$$z_\theta(x) = \arg\min_{z \in \mathcal{Z}} \max_{y \in \mathcal{U}_\theta(x)} \phi(y, z), \quad r_\theta(x) = \max_{y \in \mathcal{U}_\theta(x)} \phi(y, z_\theta(x))$$

核心优化问题为在显式鲁棒性约束下最小化期望风险证书：

$$\min_{\theta \in \Theta} \mathbb{E}[r_\theta(X)] \quad \mathrm{s.t.} \quad \mathbb{P}\{\phi(Y, z_\theta(X)) \le r_\theta(X)\} \ge 1 - \alpha$$

**定理3.1**证明该预测集优化问题与原始风险厌恶决策问题等价，从理论上保证CRC框架无性能损失。

### 3. 经验优化与平滑对偶算法

为支持梯度优化，CRC构建经验对偶问题。首先通过样本平均近似目标与约束：

$$\hat{\theta} = \arg\min_{\theta\in\Theta} \frac{1}{n}\sum_{i=1}^n r_\theta(X_i) \quad \mathrm{s.t.} \quad \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{\phi(Y_i, z_\theta(X_i)) \le r_\theta(X_i)\} \ge 1-\alpha$$

由于指示函数不可微，采用高斯误差函数平滑近似：

$$\tilde{\mathbf{1}}\{a \le b\} = \frac{1}{2}\left(1 + \mathrm{erf}\left(\frac{b - a}{\sqrt{2}\sigma}\right)\right)$$

随后构建拉格朗日对偶问题，通过交替更新模型参数 $\theta$ 和拉格朗日乘子 $\lambda$ 进行优化（Algorithm 1）。乘子更新采用投影梯度上升：$\lambda \leftarrow \max\{0, \lambda + \eta \tilde{g}(\theta)\}$。

### 4. 测试时校准与有限样本保证

优化后的预测集虽在训练集上满足经验约束，但缺乏有限样本鲁棒性保证。CRC引入**样本分割校准程序**（Algorithm 2, Cal-CRC）：

1. 将数据划分为训练集 $\mathcal{D}_{\mathrm{train}}$ 和校准集 $\mathcal{D}_{\mathrm{cal}}$
2. 在训练集上优化预测集参数 $\hat{\theta}_0$
3. 基于校准集，通过保形推理调整单一半径参数 $t$，构建嵌套预测集族（以椭圆集为例）：

$$\mathcal{U}_{\theta, t}(x) = \{y \in \mathbb{R}^q : (y - \mu_\theta(x))^\top \Sigma_\theta^{-1}(x)(y - \mu_\theta(x)) \le t\}$$

4. 对每个候选标签 $y$，计算满足经验覆盖约束的最小半径 $\hat{t}^y$，构建最终预测集 $\mathcal{U}_{\mathrm{Cal}}(X_{n+1})$

**定理4.1**保证该程序提供精确的有限样本鲁棒性：

$$\mathbb{P}\left\{\phi\left(Y_{n+1}, z_{\mathcal{U}_{\mathrm{Cal}}}(X_{n+1})\right) \le r_{\mathcal{U}_{\mathrm{Cal}}}(X_{n+1})\right\} \ge 1 - \alpha$$

### 5. 非渐近理论保证

CRC提供两个关键理论保证（定理3.2和3.3）：

- **鲁棒性差距界**：$\Delta_n = O(\sqrt{d \log n / n})$，保证经验解的鲁棒性水平以 $\Delta_n$ 的速率收敛至名义水平 $1-\alpha$
- **风险证书最优性界**：经验解与略微放宽鲁棒性水平下的最优解之间的期望风险证书差距同样以 $O(\sqrt{d \log n / n})$ 速率收敛

值得注意的是，鲁棒性约束在模型参数上**不满足单调性**（Remark 3.1），这与保形风险控制形成本质区别，使得标准保形校准方法无法直接适用，必须采用本文提出的专用优化与校准框架。

## 实验与关键发现

### 核心性能对比：消除保守偏差的实证证据

CRC框架的核心主张——用显式鲁棒性约束替代覆盖代理约束可消除结构性保守偏差——在多个基准上得到一致验证。表1展示了美国股票投资组合优化问题上的主结果：在名义鲁棒性水平α=0.1下，**CRC-E**的风险证书仅为1.028±0.047，而**CRO-E**（Sun et al., 2023）高达1.723±0.032，降幅约40%；决策损失同样从0.319±0.009降至0.251±0.015。与此同时，CRC-E将鲁棒性维持在90.8±0.7%，恰好贴近目标水平，而CRO-E过度保守地达到99.5±0.3%。这一对比直接印证了图1的定性结论：覆盖概率只是鲁棒性的充分条件而非必要条件。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_bt4Ahpemmi/figures/010_Table_1.jpg]]
*Table 1: The results of risk certificate, decision loss, and robustness under nominal levels $\alpha$ = 0 . 1 and $\alpha$ = 0 . 2 on the US stock problem

合成数据实验进一步揭示了CRC的行为模式。图2显示，在不同名义水平α下，CRC-E的风险证书和决策损失始终低于CRO-E和E2E-E，且鲁棒性精准跟踪目标水平（灰色虚线），而两个基线方法均显著高于目标。值得注意的是，CRC的覆盖率远低于鲁棒性水平——这正是方法动机的直接验证：模型无需维持高覆盖概率即可满足鲁棒性要求。图3表明，随着样本量从500增至2000，所有方法的性能均改善，但CRC-E的优势保持稳定，且其鲁棒性始终贴近名义水平，而基线方法即使在n=2000时仍存在明显保守偏差。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_bt4Ahpemmi/figures/005_Figure_2.jpg]]
*Figure 2: The results of risk certificate, decision loss, robustness, and coverage on synthetic data when varying nominal level α with identical sample size n = 1 5 0 0 . The horizontal gray dashed lines refer to robustness levels. The prediction sets are ellipsoids*

### 预测集合形状的泛化性

CRC框架的有效性不限于特定预测集合几何结构。表5汇报了多面体预测集下的仿真结果：**CRC-P**的风险证书为1.493，决策损失为0.852，均显著优于CRO-P和E2E-P，而覆盖率仅为23.5%。这表明CRC的核心机制——直接约束决策鲁棒性而非覆盖概率——在不同集合参数化下均能发挥作用。盒形集（CRC-B）和椭圆集（CRC-E）在表1中同样表现出一致的优势模式。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_bt4Ahpemmi/figures/025_Table_5.jpg]]
*Table 5: The simulation results under polyhedral prediction set with nominal level $\alpha$ = 0 . 1 , where the sample size is n = 2 0 0 0*

### 消融实验：校准步骤的关键作用

表6的消融实验揭示了校准模块的贡献。未经校准的**CRC-E**风险证书最低（8.641±0.043），但覆盖率仅59.8±1.8%，鲁棒性为88.4±0.6%，略低于90%目标。引入保形校准后，**Cal-CRC-E**将覆盖率提升至90.5±1.2%，鲁棒性达到90.9±1.1%，恰好满足名义要求，代价是风险证书小幅增至8.716±0.059。这一结果与定理4.1的有限样本鲁棒性保证一致：校准以微小的效率损失换取严格的鲁棒性满足。作为对照的**Cal-E**（仅校准而无CRC优化）风险证书高达9.471±0.087，表明CRC优化阶段对降低风险证书至关重要。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_bt4Ahpemmi/figures/026_Table_6.jpg]]
*Table 6: The results of CRC ablation experiments with nominal level $\alpha$ = 0 . 1 , where the sample size is n = 1 5 0 0 . The prediction sets are ellipsoids*

### 超参数敏感性分析

CRC框架对关键超参数表现出良好的鲁棒性。表2显示，平滑参数σ在0.01至0.20范围内变化时，风险证书在8.64附近波动，鲁棒性稳定在89%-90%区间，决策损失和覆盖率同样保持稳定。这表明梯度优化中使用的平滑近似对最终解质量影响有限。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_bt4Ahpemmi/figures/017_Table_2.jpg]]
*Table 2: The results of different smoothing parameters sensitivity of CRC at the nominal level $\alpha$ = 0 . 1 , where the sample size is n = 1 5 0 0 . The prediction sets are ellipsoids*

表3考察了拉格朗日乘子λ的更新频率。当λ更新步长从每1步增至每8步时，风险证书从8.641略微降至8.452，覆盖率从59.8%小幅升至62.0%，鲁棒性和决策损失保持稳定。更频繁的乘子更新对约束满足有轻微促进作用，但整体影响不显著，说明算法对乘子更新策略不敏感。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_bt4Ahpemmi/figures/018_Table_3.jpg]]
*Table 3: The results of lagrange multiplier update schedule of CRC at the nominal level $\alpha$ = 0 . 1 where the sample size is n = 1 5 0 0 . The prediction sets are ellipsoids*

### 与离散化方法的对比

表4将CRC与基于离散化的风险厌恶控制方法**RAC**进行对比。CRC-E在风险证书（1.384±0.049）和决策损失（0.541±0.065）上均优于所有RAC变体，但覆盖率仅为36.1%，远低于RAC方法的约90%。这一结果再次验证了CRC的核心洞察：高覆盖率并非低决策风险的必要条件。RAC方法的性能随离散化精度（J, L参数）提升而改善，但即使在最高精度设置下仍不及CRC，且面临离散化带来的计算开销与精度损失。

### 电池存储问题上的验证

图4和图5展示了电池存储问题上的结果，进一步扩展了任务类型的覆盖范围。在椭圆集（图4）和盒形集（图5）两种参数化下，CRC在两个α水平上均实现了更低的风险证书和决策损失，同时鲁棒性更贴近目标水平。这表明CRC的优势不限于金融领域，在具有不同损失函数结构的运营决策问题中同样成立。

### 失败模式与局限性

尽管CRC在多个基准上表现优异，但仍存在若干值得注意的局限：

1. **校准阶段的离散化开销**：当标签空间连续时，Cal-CRC需要遍历候选标签以确定校准半径（Algorithm 2），尽管离散化可缓解，但在高维标签空间中计算开销显著。表4中RAC方法的离散化困境从侧面反映了这一问题。

2. **凸性假设的边界**：当前理论分析和实验均基于凸损失函数和规则化预测集合（盒子、椭圆、多面体）。向非凸损失或更复杂集合形状的扩展尚缺乏理论和实证支撑。

3. **理论最优性间隙**：定理3.3的最优性保证建立在略微放宽的鲁棒性水平上（$1-\alpha-\Delta_n$），与原始名义水平$1-\alpha$之间存在微小间隙，该间隙以$O(\sqrt{d\log n / n})$速率收敛，在小样本下可能不可忽略。

4. **覆盖率与鲁棒性的解耦程度**：虽然低覆盖率是CRC方法动机的实证验证，但在某些应用场景中，预测集本身的覆盖质量可能具有独立价值（如可解释性需求），此时CRC的低覆盖率特性可能成为劣势。

## 定位与知识库关联

### 1 问题定位：从覆盖代理到显式鲁棒约束

CRC 的核心贡献在于重构了分布鲁棒优化（DRO）中预测集的作用边界。传统 CRO 方法——以 **CRO with conformal prediction sets**（Sun et al., 2023）为代表——将预测集 $\mathcal{U}(X)$ 的覆盖概率约束 $\mathbb{P}\{Y \in \mathcal{U}(X)\} \ge 1-\alpha$ 作为鲁棒性的代理条件，随后在预测集上求解极小极大决策。这一范式的结构性缺陷在于：覆盖概率只是鲁棒性的**充分条件而非必要条件**。当预测集包含某些“无害”区域（即这些区域内的 $Y$ 不会导致最坏情况损失超过风险证书），覆盖约束仍强制要求将其纳入，造成预测集膨胀，进而推高风险证书。

CRC 将约束直接替换为决策鲁棒性概率约束 $\mathbb{P}\{\phi(Y, z_\theta(X)) \le r_\theta(X)\} \ge 1-\alpha$，切断了覆盖与鲁棒性之间的间接链路。这一替换的等价性由 **Theorem 3.1** 保证：预测集优化问题与原始风险厌恶决策问题在最小化期望风险证书的意义下等价，因此 CRC 框架理论上没有性能损失。

### 2 与端到端方法的对比

另一条基线是 **End-to-end (E2E) method**（Chenreddy & Delage, 2024; Yeh et al., 2024），它通过直接最小化下游任务损失来学习不确定性集合，绕过显式的覆盖或鲁棒性约束。E2E 的核心局限在于：它不提供有限样本的鲁棒性保证，且优化目标中缺乏对鲁棒性水平的显式控制机制，导致实际鲁棒性偏离名义目标。

CRC 与 E2E 的关键差异体现在两个层面：
- **约束形式**：CRC 保留了显式的鲁棒性概率约束，使其能够通过拉格朗日对偶框架（Algorithm 1）精确调节鲁棒性水平；E2E 则将鲁棒性隐式地编码在损失函数中，缺乏可调节的约束边界。
- **理论保证**：CRC 提供了非渐近的鲁棒性差距界（Theorem 3.2）和风险证书最优性界（Theorem 3.3），收敛速率为 $O(\sqrt{d \log n / n})$；E2E 缺乏此类统计学习理论支撑。

在 US Stock Portfolio Optimization 实验中（Table 1, $\alpha=0.1$），CRC-E 的风险证书为 $1.028 \pm 0.047$，显著低于 CRO-E 的 $1.723 \pm 0.032$ 和 E2E-E 的对应值，同时鲁棒性保持在 $90.8 \pm 0.7\%$，接近名义目标 $90\%$，而 CRO-E 的鲁棒性高达 $99.5 \pm 0.3\%$，暴露出严重的保守偏差。

### 3 与保形风险控制（Conformal Risk Control）的区别

保形风险控制（Conformal Risk Control, CRC 的命名可能引发混淆）通常要求风险函数关于模型参数具有单调性，以便通过阈值调优实现风险控制。CRC 框架中的鲁棒性约束 $\mathbb{P}\{\phi(Y, z_\theta(X)) \le r_\theta(X)\}$ 虽然可视为一种特殊风险，但**不具备参数单调性**（Remark 3.1），因此无法直接套用标准保形风险控制的多重假设检验范式。CRC 转而采用拉格朗日对偶优化与事后校准的两阶段策略，绕过了单调性要求。

### 4 适用边界与局限

**适用边界**：
- **损失函数**：当前框架主要适用于凸损失函数（如投资组合优化中的线性损失 $\phi(y, z) = -y^\top z$），向非凸损失的扩展尚不明确。
- **预测集几何**：支持盒子（box）、椭圆（ellipsoid）和多面体（polyhedron）三种规则化参数化形式。这些集合的嵌套性质（通过单一半径参数 $t$ 调节大小）是校准步骤（Algorithm 2）成立的前提。
- **决策空间**：适用于连续或可离散化的决策空间；当决策空间与标签空间均为连续时，校准过程需要遍历候选标签，离散化可缓解但高维情况仍存在计算开销与精度损失。

**已知局限**：
1. **校准的计算开销**：Cal-CRC 对每个测试点需要在候选标签网格上执行全保形预测，计算复杂度随标签维度增长。
2. **平滑近似的依赖**：经验优化（Algorithm 1）使用高斯误差函数 $\tilde{\mathbf{1}}\{a \le b\} = \frac{1}{2}(1 + \mathrm{erf}(\frac{b-a}{\sqrt{2}\sigma}))$ 替代指示函数，引入平滑参数 $\sigma$。消融实验（Table 2）表明 CRC-E 对 $\sigma \in [0.01, 0.20]$ 不敏感，但在极端取值下可能影响优化稳定性。
3. **理论最优性的间隙**：Theorem 3.3 的最优性保证建立在略微放宽的鲁棒性水平 $1-\alpha-\Delta_n$ 上，与原始名义水平 $1-\alpha$ 之间存在 $\Delta_n$ 的间隙，该间隙以 $O(\sqrt{d \log n / n})$ 速率收敛，有限样本下不可忽略。

### 5 开放问题

1. **优化算法改进**：当前拉格朗日对偶优化依赖投影梯度上升更新乘子，消融实验（Table 3）显示更频繁的乘子更新（从 1 步到 8 步）仅略微降低风险证书（$8.641 \to 8.452$），表明优化效率存在提升空间。开发对平滑近似和超参数调优依赖更小的优化算法是重要方向。
2. **非凸损失与非参数化集合**：将 CRC 扩展到非凸损失函数和更复杂的预测集形状（如非规则化深度生成模型产生的集合）需要重新设计校准机制，因为当前的全保形校准依赖于嵌套集合结构。
3. **高维标签空间的校准策略**：针对多维时间序列等任务，设计面向特定任务的预测集参数化方法和高效校准策略，以在保持有限样本保证的同时降低计算开销。
4. **与在线决策场景的结合**：当前 CRC 假设批量学习设置，其在在线或自适应决策场景下的扩展（如结合在线保形推理）尚未探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Conformal_Robustness_Control_A_New_Strategy_for_Robust_Decision.pdf]]

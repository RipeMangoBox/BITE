---
title: "A Relative Error-Based Evaluation Framework of Heterogeneous Treatment Effect Estimators"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Relative_Error_Based_Evaluation_Framework_of_Heterogeneous_Treatment_Effect_Estimators.pdf
project_link: null
code_link: null
aliases:
- HRREBHEF
- REBEFHTEE
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/causality
core_operator: "通过精心设计加权最小二乘损失函数和平衡正则化器，利用倾向得分与结果回归模型之间的内在联系，使得相对误差估计量在结果回归模型有偏时仍保持 n-一致性和渐近正态性，仅需倾向得分模型以快于 n^{-1/4} 的速率一致。"
primary_logic: "通过共享表示 Φ(X) 和新的损失函数设计，使得泰勒展开中的一阶项 Δ_β₀ 和 Δ_β₁ 在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响，实现仅依赖倾向得分一致性的鲁棒估计。"
claims:
- "所提出的相对误差估计量在倾向得分模型正确指定且 γ̌, β̌₀, β̌₁ 以快于 n^{-1/4} 速率收敛时，是 n-一致且渐近正态的，即使结果回归模型不一致。"
- "在IHDP和Twins数据集上，所提方法在HTE估计（√ε_PEHE和ε_ATE）上取得最佳或接近最佳的性能。"
- "所提方法在覆盖率和选择准确率上均优于Gao (2025)的方法。"
- "去除约束损失 L_const 会导致性能严重下降，表明该损失对HTE估计精度和置信区间构建至关重要。"
---

# A Relative Error-Based Evaluation Framework of Heterogeneous Treatment Effect Estimators

> [!tip] 核心洞察
> 通过共享表示 Φ(X) 和新的损失函数设计，使得泰勒展开中的一阶项 Δ_β₀ 和 Δ_β₁ 在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响，实现仅依赖倾向得分一致性的鲁棒估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于相对误差的异质性处理效应评估框架 |
| 英文题名 | A Relative Error-Based Evaluation Framework of Heterogeneous Treatment Effect Estimators |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gubSyVxWdG) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/causality |
| Method | 基于相对误差的鲁棒HTE评估框架（Robust Relative Error-based HTE Evaluation Framework） |
| Dataset | IHDP |

> [!tip] 效果简介
> - IHDP 上，√ε_PEHE^in 为 0.638 ± 0.138，对比 0.896 (TARNet)，变化 -0.258。
> - IHDP 上，ε_ATE^in 为 0.090 ± 0.087，对比 0.279 (TARNet)，变化 -0.189。
> - IHDP 上，√ε_PEHE^out 为 0.670 ± 0.150，对比 0.920 (TARNet)，变化 -0.250。

## 概要

异质性处理效应（HTE）估计的评估是因果推断中的核心挑战。现有基于相对误差的评估方法（Gao, 2025）要求所有 nuisance 参数估计量（倾向得分和结果回归模型）均以快于 $n^{-1/4}$ 的速率一致，这一条件在实践中过于严格——结果回归模型严重依赖模型外推，在治疗组与对照组分布差异大时容易产生偏差。

本文提出一个鲁棒的相对误差评估框架，核心洞察在于：通过设计加权最小二乘损失函数 $\mathcal{L}_{\mathrm{wls}}$ 和平衡正则化器 $\mathcal{L}_{\mathrm{const}}$，利用倾向得分与结果回归模型之间的内在联系，使得泰勒展开中的一阶项在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响。具体地，该方法采用基于 Dragonnet 的共享表示架构，三个头部（控制结果、处理结果、倾向得分）共享表示 $\Phi(X)$，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{wls}} + \lambda_1 \mathcal{L}_{\mathrm{ce}} + \lambda_2 \mathcal{L}_{\mathrm{const}}$。

**核心理论结果**（Theorem 1）：若倾向得分模型正确指定且 $\check{\gamma}, \check{\beta}_0, \check{\beta}_1$ 以快于 $n^{-1/4}$ 的速率收敛，则所提相对误差估计量 $\check{\delta}(\hat{\tau}_1, \hat{\tau}_2; \check{\gamma}, \check{\beta}_0, \check{\beta}_1)$ 是 $n$-一致且渐近正态的，即使结果回归模型不一致。该方法无需样本分割，可直接使用全数据集进行估计。

**主要实验结果**：在 IHDP 和 Twins 两个基准数据集上，所提方法在 HTE 估计性能（$\sqrt{\epsilon_{\mathrm{PEHE}}}$ 和 $\epsilon_{\mathrm{ATE}}$）上取得最佳或接近最佳的结果。例如在 IHDP 上，样本外 $\sqrt{\epsilon_{\mathrm{PEHE}}}$ 为 $0.670 \pm 0.150$，显著优于 TARNet 的 $0.920 \pm 0.160$。在覆盖率和选择准确率上，该方法均优于 Gao (2025) 的方法，在 IHDP 上实现 0.96 的覆盖率和 0.80 的选择准确率。消融研究验证了约束损失 $\mathcal{L}_{\mathrm{const}}$ 对 HTE 估计精度的关键作用——去除该损失导致性能严重下降（IHDP 上 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从 0.670 升至 1.576）。



异质性处理效应（HTE）估计是因果推断的核心任务之一，其目标是在给定协变量 $X$ 的条件下估计个体处理效应 $\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X=x]$。由于真实 $\tau(x)$ 不可观测，如何评估不同 HTE 估计量的优劣成为一个关键挑战。

**现有方法的瓶颈**：评估 HTE 估计量 $\hat{\tau}$ 的常用指标是均方误差 $\phi(\hat{\tau}) = \mathbb{E}[(\hat{\tau}(X) - \tau(X))^2]$。由于 $\tau(X)$ 不可观测，直接计算 $\phi$ 不可行。Gao (2025) 提出了基于相对误差 $\delta(\hat{\tau}_1, \hat{\tau}_2) = \phi(\hat{\tau}_1) - \phi(\hat{\tau}_2)$ 的半参数估计框架，其核心优势在于仅依赖 $\tau$ 的一阶项，从而降低了对 $\tau$ 估计误差的敏感性。然而，该框架要求所有 nuisance 参数估计量（倾向得分 $e(X)$ 和结果回归模型 $\mu_a(X)$）均以快于 $n^{-1/4}$ 的速率一致（即 Condition 2）。这一条件在实践中过于严格：结果回归模型严重依赖模型外推，在治疗组与对照组协变量分布差异较大时极易产生偏差，导致估计量不再满足 $n$-一致性。

**因果机制与核心洞察**：本文的核心洞察在于，通过精心设计加权最小二乘损失函数和平衡正则化器，可以利用倾向得分与结果回归模型之间的内在联系，使得相对误差估计量在结果回归模型有偏时仍保持 $n$-一致性和渐近正态性。具体机制是：通过共享表示 $\Phi(X)$ 和新的损失函数设计，使得泰勒展开中的一阶项在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响。这相当于将严格条件“所有 nuisance 参数一致”放松为仅要求倾向得分模型以快于 $n^{-1/4}$ 的速率一致。

**方法缺口与本文动机**：现有工作（如 Gao, 2025）未能解决结果回归模型误设定带来的鲁棒性问题，且需要样本分割，降低了数据利用效率。本文动机是提出一个更鲁棒的 HTE 评估框架，能够在倾向得分模型正确指定但结果回归模型可能不一致的情况下，仍提供有效的相对误差估计和置信区间。该框架通过三个关键设计实现：基于 Dragonnet 的共享表示架构（三个头部共享 $\Phi(X)$）、加权最小二乘损失 $\mathcal{L}_{\mathrm{wls}}$（权重依赖于倾向得分和候选 HTE 估计量之差）、以及强制倾向得分满足平衡性质的约束损失 $\mathcal{L}_{\mathrm{const}}$。总训练损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{wls}} + \lambda_1 \mathcal{L}_{\mathrm{ce}} + \lambda_2 \mathcal{L}_{\mathrm{const}}$。



## 核心方法与创新机理

本文的核心创新在于设计了一个**对结果回归模型偏差鲁棒的相对误差估计框架**，从根本上放宽了现有方法（Gao, 2025）对 nuisance 参数一致性的严苛要求。

**瓶颈与因果旋钮：** 现有基于相对误差的 HTE 评估方法（Gao, 2025）要求所有 nuisance 参数（倾向得分和结果回归模型）均以快于 $n^{-1/4}$ 的速率一致。这在实践中过于严格，因为结果回归模型严重依赖模型外推，在治疗组和对照组分布差异大时极易产生偏差。本文的因果旋钮在于：通过精心设计加权最小二乘损失函数和平衡正则化器，利用倾向得分与结果回归模型之间的内在联系，使得相对误差估计量在结果回归模型有偏时仍保持 $\sqrt{n}$-一致性和渐近正态性，**仅需倾向得分模型以快于 $n^{-1/4}$ 的速率一致**。

**核心洞察：** 通过共享表示 $\Phi(X)$ 和新的损失函数设计，使得泰勒展开中的一阶项 $\Delta_{\beta_0}$ 和 $\Delta_{\beta_1}$ 在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响，实现仅依赖倾向得分一致性的鲁棒估计。

**关键 changed slots 及其证据：**

1.  **结果回归模型损失函数：** 从标准均方误差（MSE）改为**加权最小二乘损失** $\mathcal{L}_{\mathrm{wls}}$。该损失的权重依赖于倾向得分和候选 HTE 估计量之差，具体形式为：
    
$$
\mathcal{L}_{\mathrm{wls}}(\beta_0, \beta_1; \tilde{\gamma}) = \frac{1}{n} \sum_{i=1}^n (\hat{\tau}_1(X_i) - \hat{\tau}_2(X_i)) \left[ \frac{(1-A_i)\tilde{e}(X_i)}{1-\tilde{e}(X_i)} (Y_i - \Phi(X_i)^\top\beta_0)^2 + \frac{A_i(1-\tilde{e}(X_i))}{\tilde{e}(X_i)} (Y_i - \Phi(X_i)^\top\beta_1)^2 \right]
$$

    这一设计是定理 1 成立的关键，它确保了在倾向得分正确指定时，结果回归参数的估计误差不会污染相对误差估计。

2.  **倾向得分估计约束：** 引入**平衡正则化器** $\mathcal{L}_{\mathrm{const}}$，强制倾向得分估计满足平衡性质。消融实验（Table 5）表明，去除 $\mathcal{L}_{\mathrm{const}}$ 导致 IHDP 和 Twins 数据集上性能严重下降（例如，IHDP 上 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从 0.670 升至 1.576），在 Jobs 数据集上甚至导致灾难性性能下降（Table 13），证实该损失对 HTE 估计精度和置信区间构建至关重要。

3.  **神经网络架构：** 采用基于 **Dragonnet 的共享表示架构**，三个头部（控制结果、处理结果、倾向得分）共享表示层 $\Phi(X)$。去除共享表示（分别估计）导致 IHDP 上 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从 0.670 升至 1.576（Table 8），验证了共享表示对稳定 nuisance 学习的重要性。

4.  **样本分割要求：** 与 Gao (2025) 不同，所提方法**无需样本分割**，使用全数据集进行估计，提高了数据利用效率。

**决定性证据：** 定理 1 提供了理论保证：在倾向得分模型正确指定且 $\check{\gamma}, \check{\beta}_0, \check{\beta}_1$ 以快于 $n^{-1/4}$ 速率收敛时，所提估计量 $\check{\delta}$ 是 $\sqrt{n}$-一致且渐近正态的：

$$
\sqrt{n}\{\check{\delta}(\hat{\tau}_1, \hat{\tau}_2; \check{\gamma}, \check{\beta}_0, \check{\beta}_1) - \delta(\hat{\tau}_1, \hat{\tau}_2)\} \xrightarrow{d} \mathcal{N}(0, \sigma^2)
$$

实验上，该方法在 IHDP 和 Twins 数据集上的 HTE 估计（$\sqrt{\epsilon_{\mathrm{PEHE}}}$ 和 $\epsilon_{\mathrm{ATE}}$）取得最佳或接近最佳性能（Table 1），并在覆盖率和选择准确率上均优于 Gao (2025) 的方法（Table 2, Figure 1, Figure 2）。



该论文提出一个基于相对误差的鲁棒HTE评估框架，其核心创新在于通过精心设计的损失函数和神经网络架构，使得相对误差估计量在结果回归模型有偏时仍保持 $\sqrt{n}$-一致性和渐近正态性，仅需倾向得分模型以快于 $n^{-1/4}$ 的速率一致。

**输入输出流**：框架的输入为一组候选HTE估计量 $\hat{\tau}_1, \hat{\tau}_2, \ldots$（如TARNet、Causal Forest、X-learner等）和观测数据 $(X_i, A_i, Y_i)$；输出为候选估计量之间MSE差异 $\delta(\hat{\tau}_1, \hat{\tau}_2)$ 的估计值及其置信区间，以及一个聚合的增强型HTE估计量 $\tilde{\tau}(x)$。

**整体Pipeline**：

1. **共享表示学习**：输入协变量 $X$ 首先通过多个全连接层生成共享表示 $\Phi(X) \in \mathbb{R}^m$。该表示被三个头部共享：控制结果头部 $\mu_0(x)$、处理结果头部 $\mu_1(x)$ 和处理头部 $e(x)$（通过sigmoid激活估计倾向得分）。这种架构继承自Dragonnet框架，旨在减少nuisance参数之间的依赖关系。

2. **多任务联合训练**：网络通过总损失函数 $\mathcal{L} = \mathcal{L}_{\text{wls}} + \lambda_1 \mathcal{L}_{\text{ce}} + \lambda_2 \mathcal{L}_{\text{const}}$ 进行端到端训练。其中：
   - $\mathcal{L}_{\text{wls}}$ 是加权最小二乘损失，用于估计结果回归参数 $(\beta_0, \beta_1)$。该损失中的权重依赖于倾向得分估计 $\tilde{e}(X)$ 和候选HTE估计量之差 $(\hat{\tau}_1(X) - \hat{\tau}_2(X))$，其设计目的是使得泰勒展开中的一阶项在倾向得分模型正确指定时具有零期望，从而消除结果回归偏差的影响。
   - $\mathcal{L}_{\text{ce}}$ 是交叉熵损失，用于估计倾向得分参数 $\gamma$。
   - $\mathcal{L}_{\text{const}}$ 是约束正则化项，强制估计的倾向得分满足平衡性质，提高估计稳定性。

3. **相对误差估计**：训练完成后，使用估计的nuisance参数 $(\check{\gamma}, \check{\beta}_0, \check{\beta}_1)$ 计算相对误差估计量 $\check{\delta}(\hat{\tau}_1, \hat{\tau}_2; \check{\gamma}, \check{\beta}_0, \check{\beta}_1)$。该估计量保持与原始半参数估计量 $\hat{\delta}(\hat{\tau}_1, \hat{\tau}_2)$ 相同的形式，但具有更强的鲁棒性。根据Theorem 1，在倾向得分模型正确指定且nuisance参数收敛快于 $n^{-1/4}$ 的条件下，该估计量是 $\sqrt{n}$-一致且渐近正态的。

4. **推断与选择**：基于估计的渐近方差 $\hat{\sigma}^2$ 构建置信区间 $\check{\delta} \pm z_{\eta/2} \sqrt{\hat{\sigma}^2 / n}$，用于判断两个HTE估计量的相对优劣（若置信区间不包含0，则存在显著差异）。

5. **增强型HTE估计**：利用估计的结果回归函数 $\check{\mu}_1(x; \hat{\tau}_k, \hat{\tau}_{k'})$ 和 $\check{\mu}_0(x; \hat{\tau}_k, \hat{\tau}_{k'})$，对所有候选估计量对进行均匀平均，得到聚合HTE估计量 $\tilde{\tau}(x)$。该估计量在实验中取得了优于所有基线的性能。

**模块关系**：共享表示层 $\Phi(X)$ 是核心枢纽，三个头部（控制结果、处理结果、倾向得分）共享该表示但使用不同的损失函数进行优化。加权最小二乘损失 $\mathcal{L}_{\text{wls}}$ 和交叉熵损失 $\mathcal{L}_{\text{ce}}$ 分别驱动结果回归和倾向得分参数的更新，而约束损失 $\mathcal{L}_{\text{const}}$ 则作为正则化项连接两者。这种设计的关键在于，通过共享表示和加权损失，使得结果回归参数的估计误差在相对误差估计量的一阶项中相互抵消，从而放松了对结果回归模型一致性的要求。

**与现有方法的区别**：与Gao (2025)的方法相比，本框架不需要样本分割（使用全数据集进行估计），且放松了对所有nuisance参数一致性的要求（仅需倾向得分模型一致）。消融实验（Table 5）表明，去除约束损失 $\mathcal{L}_{\text{const}}$ 会导致性能严重下降，而去除交叉熵损失 $\mathcal{L}_{\text{ce}}$ 仅导致适度性能下降，验证了各模块的关键作用。



### 问题设定与评估指标

论文聚焦于异质性处理效应（HTE）的评估。HTE定义为给定协变量 $X=x$ 时个体处理效应的条件期望：

$$
\tau(x) = \mathbb{E}[Y_i(1) - Y_i(0) \mid X_i = x]
$$

评估HTE估计量 $\hat{\tau}$ 的绝对性能常用均方误差（MSE）：

$$
\phi(\hat{\tau}) \triangleq \mathbb{E}[(\hat{\tau}(X) - \tau(X))^2]
$$

然而，由于真实 $\tau(X)$ 不可观测，$\phi(\hat{\tau})$ 无法直接计算。相对误差方法通过比较两个估计量 $\hat{\tau}_1$ 和 $\hat{\tau}_2$ 的MSE之差来规避此问题：

$$
\delta(\hat{\tau}_1, \hat{\tau}_2) \triangleq \phi(\hat{\tau}_1) - \phi(\hat{\tau}_2) = \mathbb{E}[\hat{\tau}_1^2(X) - \hat{\tau}_2^2(X) - 2(\hat{\tau}_1(X) - \hat{\tau}_2(X))\tau(X)]
$$

该表达式的关键在于，它仅依赖于不可观测的 $\tau(X)$ 的一阶项，从而降低了对 $\tau$ 估计误差的敏感性。

### 现有方法的瓶颈与核心洞察

现有基于相对误差的半参数估计量 $\hat{\delta}(\hat{\tau}_1, \hat{\tau}_2)$ 要求所有 nuisance 参数（倾向得分 $e(X)$ 和结果回归模型 $\mu_0(X), \mu_1(X)$）的估计量均以快于 $n^{-1/4}$ 的速率一致（Condition 2）。该条件在实践中过于严格，因为结果回归模型严重依赖模型外推，在治疗组和对照组分布差异大时容易产生偏差。

论文的核心洞察在于：通过精心设计加权最小二乘损失函数和平衡正则化器，利用倾向得分与结果回归模型之间的内在联系，使得相对误差估计量在结果回归模型有偏时仍保持 $n$-一致性和渐近正态性，仅需倾向得分模型以快于 $n^{-1/4}$ 的速率一致。其机制是，在泰勒展开中，一阶项 $\Delta_{\beta_0}$ 和 $\Delta_{\beta_1}$ 在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响。

### 提出的方法：模型与损失函数

论文采用基于Dragonnet框架的神经网络架构，包含一个共享表示层 $\Phi(X)$ 和三个头部：控制结果头部 $\mu_0(x)$、处理结果头部 $\mu_1(x)$ 和处理头部 $e(x)$（通过sigmoid激活估计倾向得分）。模型假设如下：

**倾向得分模型**（逻辑回归）：

$$
e(X) = \mathbb{P}(A=1|X) = e(\Phi(X), \gamma) = \frac{\exp(\Phi(X)^\mathsf{T}\gamma)}{1 + \exp(\Phi(X)^\mathsf{T}\gamma)}
$$

**结果回归模型**（每个处理臂的线性模型，使用共享表示 $\Phi(X)$）：

$$
\mu_a(X) = \mathbb{E}(Y|X, A=a) = \mu_a(\Phi(X), \beta_a) = \Phi(X)^\top \beta_a, \quad a=0,1
$$

**加权最小二乘损失**（核心创新）：

$$
\mathcal{L}_{\mathrm{wls}}(\beta_0, \beta_1; \tilde{\gamma}) = \frac{1}{n} \sum_{i=1}^n (\hat{\tau}_1(X_i) - \hat{\tau}_2(X_i)) \left[ \frac{(1-A_i)\tilde{e}(X_i)}{1-\tilde{e}(X_i)} (Y_i - \Phi(X_i)^\top\beta_0)^2 + \frac{A_i(1-\tilde{e}(X_i))}{\tilde{e}(X_i)} (Y_i - \Phi(X_i)^\top\beta_1)^2 \right]
$$

该损失函数通过权重 $(\hat{\tau}_1(X_i) - \hat{\tau}_2(X_i))$ 耦合了候选估计量的差异，并通过倾向得分加权（$\frac{\tilde{e}}{1-\tilde{e}}$ 和 $\frac{1-\tilde{e}}{\tilde{e}}$）确保在倾向得分正确指定时，泰勒展开中的一阶偏差项期望为零。

**总训练损失**：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{wls}} + \lambda_1 \mathcal{L}_{\mathrm{ce}} + \lambda_2 \mathcal{L}_{\mathrm{const}}
$$

其中 $\mathcal{L}_{\mathrm{ce}}$ 是倾向得分估计的交叉熵损失，$\mathcal{L}_{\mathrm{const}}$ 是约束损失，用于强制倾向得分满足平衡性质，提高估计稳定性。

### 理论保证

**定理1**：若倾向得分模型正确指定，且 $\check{\gamma}, \check{\beta}_0, \check{\beta}_1$ 以快于 $n^{-1/4}$ 的速率收敛到其概率极限，则所提相对误差估计量是 $n$-一致且渐近正态的：

$$
\sqrt{n}\{\check{\delta}(\hat{\tau}_1, \hat{\tau}_2; \check{\gamma}, \check{\beta}_0, \check{\beta}_1) - \delta(\hat{\tau}_1, \hat{\tau}_2)\} \xrightarrow{d} \mathcal{N}(0, \sigma^2)
$$

该结果的关键在于：条件仅要求倾向得分模型一致，结果回归模型可以不一致。渐近方差 $\sigma^2$ 的一致估计量为：

$$
\hat{\sigma}^2 = \frac{1}{n} \sum_{i=1}^n \left\{ \varphi(Z_i; \check{u}_0, \check{u}_1, \check{e}) - \check{\delta}(\hat{\tau}_1, \hat{\tau}_2; \check{\gamma}, \check{\beta}_0, \check{\beta}_1) \right\}^2
$$

由此可构建 $\delta(\hat{\tau}_1, \hat{\tau}_2)$ 的渐近 $(1-\eta)$ 置信区间：

$$
\check{\delta}(\hat{\tau}_1, \hat{\tau}_2; \check{\gamma}, \check{\beta}_0, \check{\beta}_1) \pm z_{\eta/2} \sqrt{\hat{\sigma}^2 / n}
$$

### 增强的HTE估计量

从训练好的结果回归函数 $\check{\mu}_0(x; \hat{\tau}_k, \hat{\tau}_{k'})$ 和 $\check{\mu}_1(x; \hat{\tau}_k, \hat{\tau}_{k'})$ 可导出新的HTE估计量：

$$
\check{\tau}(x; \hat{\tau}_k, \hat{\tau}_{k'}) = \check{\mu}_1(x; \hat{\tau}_k, \hat{\tau}_{k'}) - \check{\mu}_0(x; \hat{\tau}_k, \hat{\tau}_{k'})
$$

对所有候选估计量对进行均匀平均，得到聚合HTE估计量：

$$
\tilde{\tau}(x) = \frac{2}{|\mathcal{K}|(|\mathcal{K}|-1)} \sum_{k,k' \in \mathcal{K}} \check{\mu}_1(x; \hat{\tau}_k, \hat{\tau}_{k'}) - \check{\mu}_0(x; \hat{\tau}_k, \hat{\tau}_{k'})
$$

该聚合估计量在实验中取得了最佳或接近最佳的性能，但论文指出当前均匀平均方案可能无法充分利用各估计量的异质性优势，这是未来工作的方向。

### 关键变量含义汇总

| 符号 | 含义 |
|------|------|
| $\tau(x)$ | 异质性处理效应 |
| $\phi(\hat{\tau})$ | HTE估计量的MSE |
| $\delta(\hat{\tau}_1, \hat{\tau}_2)$ | 两个HTE估计量MSE之差（相对误差） |
| $e(X)$ | 倾向得分 $\mathbb{P}(A=1|X)$ |
| $\mu_a(X)$ | 结果回归函数 $\mathbb{E}(Y|X, A=a)$ |
| $\Phi(X)$ | 共享表示层 |
| $\mathcal{L}_{\mathrm{wls}}$ | 加权最小二乘损失 |
| $\mathcal{L}_{\mathrm{ce}}$ | 交叉熵损失 |
| $\mathcal{L}_{\mathrm{const}}$ | 约束损失 |
| $\check{\delta}$ | 相对误差估计量 |
| $\tilde{\tau}(x)$ | 聚合HTE估计量 |



## 实验与关键发现

### 主结果：HTE估计与相对误差推断

在三个基准数据集（IHDP、Twins、Jobs）上的实验验证了所提框架的有效性。

**HTE估计性能（Table 1）**：在IHDP数据集上，所提方法在样本内和样本外均取得最优性能。样本外 $\sqrt{\epsilon_{\mathrm{PEHE}}}$ 为 $0.670 \pm 0.150$，较最优基线TARNet（0.920）降低27%；$\epsilon_{\mathrm{ATE}}$ 为 $0.105 \pm 0.099$，较TARNet（0.266）降低61%。在Twins数据集上，所提方法同样取得最优结果，样本外 $\sqrt{\epsilon_{\mathrm{PEHE}}}$ 为 $0.286 \pm 0.007$，$\epsilon_{\mathrm{ATE}}$ 为 $0.009 \pm 0.006$。在Jobs数据集上（Table 11），所提方法在策略风险 $R_{\mathrm{pol}}$ 和ATT估计误差 $\epsilon_{\mathrm{ATT}}$ 上均优于所有基线，样本外 $R_{\mathrm{pol}}$ 为 $0.131 \pm 0.030$，$\epsilon_{\mathrm{ATT}}$ 为 $0.053 \pm 0.039$。

![[assets/figures/papers/iclr26_0003_gubSyVxWdG_A_Relative_Error-Based_Evaluation_Framework_of_H/figures/005_Table_1.jpg]]
*Table 1: HTE estimation performance on the IHDP and Twins datasets (in-sample and out-of-sample). The best results are bolded*

**相对误差推断（Table 2, Figures 1 & 2）**：在覆盖率和选择准确率两个维度上，所提方法均显著优于Gao (2025)的方法。在IHDP上，所提方法达到0.96的覆盖率和0.80的选择准确率，而Gao (2025)的覆盖率仅为0.89、选择准确率为0.66。在Twins上，所提方法覆盖率为0.94、选择准确率为0.94，Gao (2025)分别为0.90和0.88。这表明所提框架能有效提供可靠的HTE估计器选择建议。

![[assets/figures/papers/iclr26_0003_gubSyVxWdG_A_Relative_Error-Based_Evaluation_Framework_of_H/figures/006_Table_2.jpg]]
*Table 2: δ Inference with Different Nuisance*

### 消融研究

**约束损失 $L_{\mathrm{const}}$ 的关键作用（Table 5）**：去除 $L_{\mathrm{const}}$ 导致IHDP上 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从0.670急剧上升至1.587，Twins上从0.286上升至0.383。在Jobs数据集上（Table 13），去除 $L_{\mathrm{const}}$ 带来"灾难性"性能下降，$R_{\mathrm{pol}}^{\mathrm{out}}$ 从0.131恶化至0.213。这证实平衡正则化器对维持倾向得分估计质量和整体HTE精度至关重要。

![[assets/figures/papers/iclr26_0003_gubSyVxWdG_A_Relative_Error-Based_Evaluation_Framework_of_H/figures/009_Table_5.jpg]]
*Table 5: Ablation study results on the IHDP and Twins datasets*

**共享表示的必要性（Table 8）**：在IHDP上，分别估计倾向得分和结果回归（去除共享表示）导致 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从0.670恶化至1.576，选择准确率从0.80降至0.25。若所有网络参数均独立估计，性能进一步崩溃至7.133。这表明共享表示 $\Phi(X)$ 是连接倾向得分与结果回归、实现偏差鲁棒性的核心机制。

**交叉熵损失 $L_{\mathrm{ce}}$ 的贡献（Table 5）**：去除 $L_{\mathrm{ce}}$ 仅导致适度性能下降，IHDP上 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从0.670升至0.882，Twins上从0.286升至0.304。这说明加权最小二乘损失 $L_{\mathrm{wls}}$ 承担了主要的估计任务，但倾向得分建模仍是必要的辅助约束。

### 敏感性分析

**超参数稳健性（Tables 4, 12, 15, 16）**：在IHDP和Twins上，约束损失权重 $\lambda_2$ 在 $10^{-3}$ 至 $10^{-1}$ 范围内性能稳定；交叉熵权重 $\lambda_1$ 和平衡正则化器权重 $\rho$ 的敏感性分析同样显示性能波动较小。在Jobs上，$\lambda_1$、$\lambda_2$、$\rho$ 在广泛取值范围内保持稳定。

![[assets/figures/papers/iclr26_0003_gubSyVxWdG_A_Relative_Error-Based_Evaluation_Framework_of_H/figures/008_Table_4.jpg]]
*Table 4: Sensitivity analysis on the hyperparameter $\lambda _ { 2 }$ (weight of constraint loss) for IHDP and Twins datasets. The best hyperparameter values and results are in bold*

**倾向得分误设定敏感性（Table 6）**：通过对倾向得分施加不同程度的扰动（添加噪声），所提方法在IHDP上 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 从0.670升至0.785，选择准确率从0.80降至0.68，表明对倾向得分误设定具有合理鲁棒性，但极端误设定仍会损害性能。

![[assets/figures/papers/iclr26_0003_gubSyVxWdG_A_Relative_Error-Based_Evaluation_Framework_of_H/figures/010_Table_6.jpg]]
*Table 6: Sensitivity Analysis on Propensity Score*

### 计算效率（Table 3）

所提方法的运行时间随样本量和候选估计器数量线性增长。在 $n=5000$、$K=10$ 时，单次运行约需42秒，与现有方法处于可比范围。

### 失败模式与局限性

1. **倾向得分依赖**：定理1要求倾向得分模型正确指定且以快于 $n^{-1/4}$ 的速率一致。当倾向得分严重误设定时，估计量的渐近性质不再成立，性能显著下降（Table 6证实了这一趋势）。
2. **均匀平均的次优性**：当前对所有候选估计器对采用简单均匀平均来构造聚合HTE估计量，无法充分利用各估计器在不同子群上的异质性优势。这为自适应加权策略留下了改进空间。
3. **评估维度局限**：框架仅关注HTE的MSE差异，未涉及个体处理效应（ITE）或潜在结果联合分布等更全面的评估维度。

### 补充图表

![[assets/figures/papers/iclr26_0003_gubSyVxWdG_A_Relative_Error-Based_Evaluation_Framework_of_H/figures/007_Table_3.jpg]]
*Table 3: Running Time under Different Settings*



## 定位与知识库关联

### Baseline/Follow-Up 关系

本文所提方法直接定位于解决 Gao (2025) 相对误差评估框架的核心瓶颈。Gao (2025) 的估计量要求所有 nuisance 参数（倾向得分和结果回归模型）均以快于 $n^{-1/4}$ 的速率一致收敛（Condition 2）。这一要求在实证中过于严格，因为结果回归模型严重依赖模型外推，在治疗组与对照组协变量分布差异大时极易产生偏差（见论文 Section 3 Motivation）。本文通过三个关键设计改变来解除这一约束：

1. **损失函数重构**：将标准均方误差损失替换为加权最小二乘损失 $\mathcal{L}_{\mathrm{wls}}$，其权重依赖于倾向得分 $\tilde{e}(X)$ 和候选 HTE 估计量之差 $\hat{\tau}_1(X) - \hat{\tau}_2(X)$。这一设计使得泰勒展开中的一阶项 $\Delta_{\beta_0}$ 和 $\Delta_{\beta_1}$ 在倾向得分模型正确指定时具有零期望，从而消除结果回归模型偏差对相对误差估计的影响。
2. **引入平衡正则化器**：新增约束损失 $\mathcal{L}_{\mathrm{const}}$，强制倾向得分满足平衡性质，降低对结果回归模型精度的依赖。
3. **共享表示架构**：采用 Dragonnet 启发的神经网络架构，使倾向得分头部、控制结果头部和处理结果头部共享表示层 $\Phi(X)$，从而利用倾向得分与结果回归模型之间的内在联系。

这些改变使得新估计量在理论上仅需倾向得分模型以快于 $n^{-1/4}$ 的速率一致（Theorem 1），即使结果回归模型不一致也能保持 $\sqrt{n}$-一致性和渐近正态性。此外，本文方法无需样本分割（Gao, 2025 的必需步骤），可充分利用全数据集进行估计。

### 适用边界

**理论边界**：Theorem 1 的成立前提是倾向得分模型正确指定，且 $\check{\gamma}, \check{\beta}_0, \check{\beta}_1$ 以快于 $n^{-1/4}$ 的速率收敛。当倾向得分严重误设定时，方法性能可能下降。消融实验（Table 5, Table 13）表明，去除约束损失 $\mathcal{L}_{\mathrm{const}}$ 在 IHDP 和 Twins 上导致性能严重下降，在 Jobs 数据集上甚至导致灾难性失败，说明平衡正则化器对估计稳定性至关重要。

**实证边界**：方法在三个标准因果推断基准数据集（IHDP、Twins、Jobs）上验证，覆盖不同数据规模和生成机制。在 IHDP 上，所提方法在 $\sqrt{\epsilon_{\mathrm{PEHE}}}^{\mathrm{out}}$ 上达到 0.670（TARNet 基线为 0.920），在 Twins 上达到 0.286（TARNet 基线为 0.312）。在 Jobs 数据集上，方法在 $R_{\mathrm{pol}}^{\mathrm{out}}$ 上达到 0.131（TARNet 基线为 0.141）。超参数敏感性分析（Table 4, Table 12）表明方法对 $\lambda_1, \lambda_2, \rho$ 的变化不敏感，倾向得分误设定敏感性分析（Table 6）表明方法对倾向得分扰动具有合理鲁棒性。

### 局限与开放问题

**当前局限**：
1. 方法仍要求倾向得分模型正确指定，在倾向得分严重误设定时性能可能下降。
2. 聚合 HTE 估计量采用简单的均匀平均方案（对所有候选估计量对取平均），可能无法充分利用各估计量的异质性优势。
3. 评估框架仅关注 HTE 的 MSE 差异，未考虑 ITE 或潜在结果联合分布等更全面的评估维度。
4. 实证验证限于三个基准数据集，在更广泛实际应用场景中的泛化能力有待进一步验证。

**开放问题**：
1. 如何开发自适应加权策略，以更好地利用各候选估计量的异质性优势？
2. 如何纳入“最坏情况性能”视角以提高评估的鲁棒性，可能通过放宽强可忽略性假设（如 Huang et al., 2024 的思路）？
3. 如何通过研究 ITE 或潜在结果联合分布，提供更全面的 HTE 评估？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Relative_Error_Based_Evaluation_Framework_of_Heterogeneous_Treatment_Effect_Estimators.pdf

![[paperPDFs/ICLR_2026/A_Relative_Error_Based_Evaluation_Framework_of_Heterogeneous_Treatment_Effect_Estimators.pdf]]

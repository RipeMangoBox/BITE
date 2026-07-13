---
title: "Hyperparameter Trajectory Inference with Conditional Lagrangian Optimal Transport"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Hyperparameter_Trajectory_Inference_with_Conditional_Lagrangian_Optimal_Transport.pdf
project_link: null
code_link: null
openreview_forum_id: P5B97gZwRb
aliases:
- NCLOTC
- HTICLOT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过学习条件拉格朗日函数（包含数据依赖的势能项和基于度量的动能项），将最小作用量原理和流形假设编码为归纳偏置，引导推断路径穿越数据密集区并遵循高效传输路径。"
primary_logic: "将超参数轨迹推断形式化为条件轨迹推断（CTI）任务，提出神经条件拉格朗日最优传输（CLOT）方法，联合学习拉格朗日成本函数、最优传输映射与测地线，从而构建可泛化的代理模型，实现推理时超参数的连续调整。"
claims:
- "提出基于条件拉格朗日最优传输的方法，联合学习拉格朗日函数、最优传输映射和测地线以构建代理模型。"
- "在学习的拉格朗日中引入两种归纳偏置：基于流形假设的密度遍历偏置和基于最小作用量原理的偏置。"
- "扩展Pooladian et al. (2024)，加入条件OT设置、数据依赖的势能项和更富表达力的度量参数化。"
- "在多个HTI应用中，完整方法（K_θ - Û）重建条件概率路径的表现优于所有替代方法。"
---

# Hyperparameter Trajectory Inference with Conditional Lagrangian Optimal Transport

> [!tip] 核心洞察
> 将超参数轨迹推断形式化为条件轨迹推断（CTI）任务，提出神经条件拉格朗日最优传输（CLOT）方法，联合学习拉格朗日成本函数、最优传输映射与测地线，从而构建可泛化的代理模型，实现推理时超参数的连续调整。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于条件拉格朗日最优传输的超参数轨迹推断 |
| 英文题名 | Hyperparameter Trajectory Inference with Conditional Lagrangian Optimal Transport |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=P5B97gZwRb) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Neural Conditional Lagrangian Optimal Transport (CLOT) |
| Dataset | Semicircles (CTI), Cancer therapy (PPO reward), Reacher (PPO reward) |

> [!tip] 效果简介
> - Semicircles (CTI) 上，NLL (↓) 为 -0.662 (0.046)，对比 105.713 (2.42) (K_I，恒等度量无偏置)，变化 -106.375。
> - Semicircles (CTI) 上，CD (↓) 为 0.016 (0.001)，对比 0.323 (0.003) (K_I)，变化 -0.307。
> - Cancer therapy (PPO reward) 上，Reward (↑) 为 102.49 (5.46)，对比 98.72 (NLOT)，变化 +3.77。

## 概要

**问题背景**：现代深度学习系统常需针对不同场景调整超参数（如正则化强度、分位数水平、RL奖励权重），传统做法是逐个训练独立模型，计算成本高昂且无法连续探索超参数空间。超参数轨迹推断（Hyperparameter Trajectory Inference, HTI）将该问题形式化为：从有限个已训练模型（锚点分布）出发，推断超参数连续变化时模型输出分布的演化轨迹，从而构建可泛化的代理模型。

**核心瓶颈**：现有轨迹推断方法存在两个关键缺陷。其一，简单插值方法（如条件流匹配 CFM，Lipman et al., 2023）在复杂、非欧几里德的超参数动力学下生成不可行的代理路径——推断轨迹可能穿越低概率区域或违背系统内在约束。其二，现有神经最优传输方法（如 NLOT，Pooladian et al., 2024）缺乏对条件信息的有效建模，无法处理“给定输入 x，超参数 λ 如何影响输出分布”的条件轨迹推断任务。

**方法定位**：本文提出**神经条件拉格朗日最优传输（Neural Conditional Lagrangian Optimal Transport, CLOT）**，将 HTI 形式化为条件轨迹推断（Conditional Trajectory Inference, CTI）任务。CLOT 的核心创新在于将物理启发的归纳偏置编码到最优传输的成本函数中：通过联合学习条件拉格朗日函数、最优传输映射与测地线，使推断路径同时遵循最小作用量原理（偏好高效传输路径）和流形假设（穿越数据密集区）。相较于 NLOT，CLOT 引入了三个关键扩展：数据依赖的势能项、基于 FiLM 层的条件调制机制、以及基于特征分解的可学习度量参数化。

**主要结果**：在多个 HTI 应用场景中，完整 CLOT 方法一致优于所有基线。在二维半圆条件轨迹推断任务上，CLOT 的负对数似然（NLL）较恒等度量基线降低 106.375（Table 1）；在癌症治疗策略代理任务中，平均 PPO 奖励达到 102.49，优于 NLOT 的 98.72（Table 2）；在 ETTm2 分位数回归代理任务中，预测区间与真实区间高度吻合（Figure 3），MSE 达到 0.608（Table 5）。消融实验证实，学习度量和势能偏置各自贡献显著，且在数据稀疏设置下 CLOT 的性能退化最小，验证了归纳偏置在困难插值区域的关键作用。

超参数调整是深度学习落地的核心瓶颈之一：不同超参数配置（如正则化系数、分位数水平、奖励权重）会诱导出截然不同的模型行为，而穷举训练所有配置的计算代价往往不可接受。现有应对策略大致分为两类：一是训练少量锚点模型后对输出进行简单插值；二是使用条件生成模型（如条件流匹配）直接推断中间配置的条件分布。然而，这两类方法共享一个根本性缺陷——它们对超参数驱动下的输出动力学缺乏结构性建模。

具体而言，当超参数变化时，神经网络输出的演化轨迹通常嵌入在低维流形上，并遵循某种高效路径（最小作用量原理）。简单的逐点插值或无条件流匹配忽略了这一几何结构，在复杂、非欧几里德的超参数动力学下容易生成不可行的代理路径——例如穿越低密度区域的“捷径”，或违反物理约束的跳跃。现有方法无法有效处理条件信息，且缺乏将数据流形结构和动力学先验编码进推断过程的机制。

本文的核心动机是将超参数轨迹推断（Hyperparameter Trajectory Inference, HTI）形式化为一个**条件轨迹推断（Conditional Trajectory Inference, CTI）**任务。其目标是：给定少量锚点超参数下的模型输出分布，学习一个代理模型，能够在推理时连续调整超参数并生成对应的条件概率路径。这一设定将问题从“插值输出”提升为“学习超参数驱动的条件动力学”。

为此，本文提出**神经条件拉格朗日最优传输（Neural Conditional Lagrangian Optimal Transport, CLOT）**方法。其核心洞察是：通过学习一个条件拉格朗日函数——包含数据依赖的势能项和基于可学习度量的动能项——将最小作用量原理和流形假设编码为归纳偏置，引导推断路径穿越数据密集区并遵循高效传输路径。该方法联合学习拉格朗日成本函数、最优传输映射与测地线，从而构建可泛化的代理模型。

与现有工作的关键差异在于：**Pooladian et al. (2024)** 提出的神经拉格朗日最优传输（NLOT）仅处理无条件设定，且使用固定特征值的度量参数化（仅适用于二维）。本文将其扩展为条件最优传输框架，引入数据依赖的势能项 $\hat{\mathcal{U}}(q|x) = \alpha \log(\hat{p}(q|x) + \epsilon)$ 以施加密集遍历偏置，并设计基于特征分解和Givens旋转的可学习度量 $G_{\theta_G}$，支持任意维度且避免退化解。这些改进使得CLOT能够在稀疏锚点下可靠地推断条件概率路径，并在多个HTI应用场景中一致优于条件流匹配（CFM, Lipman et al., 2023）、度量流匹配（MFM, Kapusniak et al., 2024）等基线方法。

## 核心方法与创新机理

本文提出**神经条件拉格朗日最优传输（Neural CLOT）**，将超参数轨迹推断形式化为**条件轨迹推断（CTI）**任务，并围绕三个核心维度对现有方法进行系统性改进。其根本动机在于：现有轨迹推断方法无法有效处理条件信息，且简单插值（如条件流匹配）在复杂、非欧几里德的超参数动力学下生成不可行的代理路径。

### 创新点一：数据依赖势能项——密集遍历偏置

CLOT 在拉格朗日成本函数中引入基于流形假设的势能项，将“推断路径应穿越数据密集区”的先验知识编码为归纳偏置。具体而言：

- **基线状态**：**NLOT**（Pooladian et al., 2024）仅使用动能项 $K(q_t, \dot{q}_t|x) = \frac{1}{2}\dot{q}_t^T G(q_t|x) \dot{q}_t$，缺乏对数据分布的显式建模。
- **改进方案**：CLOT 通过 Nadaraya-Watson 估计器估计条件密度 $\hat{p}(q|x)$，并定义势能项 $\hat{\mathcal{U}}(q|x) = \alpha \log(\hat{p}(q|x) + \epsilon)$。在数据密集区域，势能较大，拉格朗日成本函数 $c$ 引导测地线优先穿越这些区域；在稀疏区域，势能较小，路径不受额外约束。
- **机制**：该偏置使拉格朗日函数 $\mathcal{L} = K - \mathcal{U}$ 同时编码了“最小作用量”（动能项）和“流形遍历”（势能项）双重归纳偏置，从根本上改变了成本函数的几何性质。

消融实验证实：加入势能偏置 $\hat{\mathcal{U}}$ 后，推断路径能有效穿越数据密集区域，在稀疏时间点上的泛化性能显著提升（Figure 1b, 1d）。

### 创新点二：条件最优传输框架——从无条件到条件建模

CLOT 将 NLOT 的无条件轨迹推断提升为完整的条件轨迹推断框架，使代理模型能够根据输入条件 $x$ 生成不同的概率路径。

- **基线状态**：NLOT 学习的是与条件无关的全局动力学，无法区分不同输入条件下的输出分布演化。
- **改进方案**：通过 FiLM（Feature-wise Linear Modulation）层将条件信息 $x$ 注入所有核心网络模块——Kantorovich 对偶网络 $g_{\theta_g,k}$、传输映射网络 $T_{\theta_{T,k}}$、测地线网络 $S_{\theta_S}$ 以及度量网络 $G_{\theta_G}$。这使得最优传输映射、测地线参数和度量矩阵均成为条件的函数。
- **机制**：条件调制实现了“同一超参数变化在不同输入下产生不同输出轨迹”的核心能力。例如，在癌症治疗 RL 任务中，相同 $\lambda_{nk}$ 变化在不同患者状态下产生不同的策略调整路径。

### 创新点三：可学习度量参数化——从固定度量到自适应几何

CLOT 提出基于特征分解和 Givens 旋转的度量参数化方案，突破了 NLOT 在度量学习上的维度限制和退化风险。

- **基线状态**：NLOT 采用固定对角矩阵加神经旋转的参数化，仅适用于二维空间，且固定特征值限制了度量的表达能力。
- **改进方案**：CLOT 将度量矩阵参数化为 $G_{\theta_G} = R_{\theta_G} E_{\theta_G} R_{\theta_G}^T$，其中 $R_{\theta_G}$ 通过 Givens 旋转序列实现正交矩阵，$E_{\theta_G}$ 为对角正定矩阵且约束特征值之和为非零常数。该参数化天然保证正定性、避免退化解，并支持任意维度。
- **证据**：在 2D 实验中，基于特征分解的 $G_{\theta_G}$ 相较于固定特征值度量，在 Cancer 任务上将平均奖励从 98.72 提升至 102.49（Table 7）；在半圆 CTI 任务上，学习度量使 NLL 从 -0.532 降至 -0.662（Table 1）。

### 创新点四：联合学习范式——端到端的度量-传输-测地线协同优化

CLOT 通过极小-极大优化框架联合学习拉格朗日成本函数（由度量 $G_{\theta_G}$ 和势能 $\hat{\mathcal{U}}$ 参数化）、条件最优传输映射 $T_{\theta_{T,k}}$ 和近似测地线 $S_{\theta_S}$，形成闭环的代理模型构建流程。

- **内层最大化**：固定度量参数 $\theta_G$，训练 Kantorovich 对偶网络 $g_{\theta_g,k}$ 以最大化半对偶 OT 目标，估计相邻时间点间的条件 OT 成本。
- **外层最小化**：固定对偶网络，优化度量参数 $\theta_G$ 以最小化估计的 OT 成本，寻求使传输最高效的黎曼几何。
- **摊销加速**：同时训练传输映射网络和测地线网络，避免推理时的嵌套优化，使 c-变换计算和路径采样可在常数时间内完成。

这一范式将“学习传输成本”与“学习传输路径”统一为单一优化问题，使得代理模型在推理时可直接根据条件 $x$ 和目标超参数 $\lambda$ 生成对应的输出分布样本，而无需重新训练或访问原始训练过程。

本文提出的**神经条件拉格朗日最优传输（Neural CLOT）**方法，将超参数轨迹推断（HTI）形式化为一个条件轨迹推断（CTI）任务：给定一组在离散超参数值 $\lambda \in \Lambda_{\text{obs}}$ 上训练得到的神经网络输出分布 $\{p_{\theta_\lambda}(y|x)\}_{\lambda \in \Lambda_{\text{obs}}}$，目标是学习超参数 $\lambda$ 诱导的连续动态 $\lambda \mapsto p_{\theta_\lambda}(y|x)$，从而构建一个可泛化的代理模型，在推理时实现超参数的连续调整。

CLOT 的核心瓶颈在于：现有方法（如条件流匹配）在复杂、非欧几里德的超参数动力学下，简单插值会生成不可行的代理路径。CLOT 通过将**最小作用量原理**和**流形假设**编码为归纳偏置，引导推断路径穿越数据密集区并遵循高效传输路径，从而解决这一瓶颈。

### Pipeline 总览

整体训练流程围绕一个极小-极大优化框架展开，交替学习三个核心组件：

1. **度量网络 $G_{\theta_G}$**：学习拉格朗日动能项中的度量矩阵，通过特征分解和 Givens 旋转参数化以保证正定性和非零体积（§4.3）。
2. **Kantorovich 对偶网络 $g_{\theta_g,k}$**：学习相邻时间点间的 Kantorovich 势函数，最大化半对偶 OT 目标以估计条件 OT 成本（§4.2）。
3. **传输映射网络 $T_{\theta_T,k}$ 与测地线网络 $S_{\theta_S}$**：分别近似条件传输映射和拉格朗日最短路径的参数，用于加速 c-变换优化和推断时采样（§4.2）。

此外，**势能估计模块**（§4.1）独立于上述优化循环，使用 Nadaraya-Watson 估计器计算条件密度并定义对数势能 $\hat{\mathcal{U}}(q|x) = \alpha \log(\hat{p}(q|x) + \epsilon)$，将密集遍历偏置注入拉格朗日成本函数。

### 输入输出流

**输入**：条件变量 $x$（如状态、上下文）和离散超参数值 $\lambda_k$ 对应的神经网络输出样本 $\{y_k \sim p_{\theta_{\lambda_k}}(\cdot|x)\}_{k=0}^K$。

**输出**：对于任意目标超参数 $\lambda^*$ 和条件 $x$，推断的代理输出 $\bar{\hat{y}}_{\lambda^*}$。

**推断流程**：
1. 确定 $\lambda^*$ 所在的相邻锚点区间 $[\lambda_k, \lambda_{k+1}]$。
2. 通过测地线网络 $S_{\theta_S}$ 估计连接 $y_k$ 和 $y_{k+1}$ 的近似拉格朗日最短路径参数 $\varphi = S_{\theta_S}(y_k, y_{k+1}, x)$。
3. 将目标时间归一化 $s^* = (\lambda^* - \lambda_k) / (\lambda_{k+1} - \lambda_k)$，在测地线上采样 $\bar{\hat{y}}_{\lambda^*} = q_\varphi(s^*)$。

### 条件调制机制

所有网络（$G_{\theta_G}$、$g_{\theta_g,k}$、$T_{\theta_T,k}$、$S_{\theta_S}$）均通过 **FiLM 层**将条件 $x$ 注入第一层激活值，实现条件依赖的动态建模。这使得整个框架能够根据不同的条件上下文，自适应地调整传输路径和度量结构。

### 训练目标

外层最小化估计的 CLOT 成本以寻求最优度量 $G_{\theta_G}$，内层最大化半对偶目标以学习最优 Kantorovich 势 $g_{\theta_g,k}$，形成极小-极大博弈：

$$\min_{\theta_G} \sum_k \mathbb{E}_x \left[ \max_{\theta_{g,k}} \mathbb{E}_{y_k \sim \mu_k(\cdot|x)} [g_{\theta_{g,k}}^c(y_k|x)] + \mathbb{E}_{y_{k+1} \sim \mu_{k+1}(\cdot|x)} [g_{\theta_{g,k}}(y_{k+1}|x)] \right]$$

其中 c-变换 $g_{\theta_{g,k}}^c(y_k|x)$ 的计算通过传输映射网络 $T_{\theta_T,k}$ 暖启动，并利用测地线网络 $S_{\theta_S}$ 高效近似拉格朗日成本函数，避免了嵌套优化。

### 条件轨迹推断问题形式化

设 $\lambda \in \Lambda$ 为单个连续超参数（充当“时间”），在观测锚点集 $\Lambda_{\text{obs}}$ 上已知条件分布 $\{p_{\theta_\lambda}(y|x)\}_{\lambda \in \Lambda_{\text{obs}}}$。HTI 的目标是学习超参数诱导的动态 $\lambda \mapsto p_{\theta_\lambda}(y|x)$，从而在推理时对任意 $\lambda^* \notin \Lambda_{\text{obs}}$ 估计 $p_{\theta_{\lambda^*}}(y|x)$。本文将此任务形式化为**条件轨迹推断**（Conditional Trajectory Inference, CTI）。

### 条件最优传输的半对偶形式

CTI 的核心数学工具是条件最优传输。给定条件 $x$ 下的两个边缘分布 $\mu_0(\cdot|x)$ 和 $\mu_1(\cdot|x)$，原始条件 OT 问题为：

$$\mathrm{COT}_c(\mu_0(\cdot|x), \mu_1(\cdot|x)) = \inf_{\pi(\cdot,\cdot|x) \in \Pi(\mu_0(\cdot|x), \mu_1(\cdot|x))} \int_{\mathcal{Y}_0 \times \mathcal{Y}_1} c(y_0, y_1|x) d\pi(y_0, y_1|x)$$

其中 $c(y_0, y_1|x)$ 为条件成本函数，$\Pi$ 为满足边缘约束的联合分布族。为便于优化，本文采用基于 **c-变换**的半对偶形式：

$$g^c(y_0|x) := \inf_{y_1' \in \mathcal{V}_1} \{ c(y_0, y_1'|x) - g(y_1'|x) \}$$

利用 c-变换，半对偶 COT 转化为对单个 Kantorovich 势函数 $g(\cdot|x)$ 的无约束优化：

$$\mathrm{COT}_c(\mu_0(\cdot|x), \mu_1(\cdot|x)) = \sup_{g(\cdot|x) \in L^1(\mu_1(\cdot|x))} \int_{\mathcal{Y}_0} g^c(y_0|x) d\mu_0(y_0|x) + \int_{\mathcal{Y}_1} g(y_1|x) d\mu_1(y_1|x)$$

从最优势函数 $g^*$ 可恢复条件传输映射：

$$T_c(y_0|x) \in \underset{y_1' \in \mathcal{V}_1}{\mathrm{argmin}} \{ c(y_0, y_1'|x) - g^*(y_1'|x) \}$$

### 拉格朗日成本函数

成本函数 $c$ 是嵌入系统动力学知识的关键位置。本文采用基于最小作用量原理的拉格朗日成本：

$$c(y_0, y_1|x) = \inf_{q: q_0=y_0, q_1=y_1} \int_0^1 \mathcal{L}(q_t, \dot{q}_t|x) dt$$

其中拉格朗日函数取经典形式——动能减势能：

$$\mathcal{L}(q_t, \dot{q}_t|x) = K(q_t, \dot{q}_t|x) - \mathcal{U}(q_t|x) = \frac{1}{2} \dot{q}_t^T G(q_t|x) \dot{q}_t - \mathcal{U}(q_t|x)$$

这里 $G(q_t|x)$ 为条件依赖的黎曼度量矩阵，$\mathcal{U}(q_t|x)$ 为势能函数。最小化作用量的曲线即为连接 $y_0$ 和 $y_1$ 的测地线。

### 势能估计模块：密集遍历偏置

势能 $\hat{\mathcal{U}}(q|x)$ 的设计是实现流形假设归纳偏置的核心。其定义为条件密度估计的对数形式：

$$\hat{\mathcal{U}}(q|x) = \alpha \log(\hat{p}(q|x) + \epsilon)$$

其中 $\alpha$ 为缩放系数，$\epsilon$ 防止数值溢出。条件密度 $\hat{p}(q|x)$ 通过 Nadaraya-Watson 估计器计算：

$$\hat{p}(q|x) = \frac{\sum_{i=1}^{N} K_{h_y}(q - y_i) K_{h_x}(x - x_i)}{\sum_{j=1}^{N} K_{h_x}(x - x_j)}$$

核函数采用高斯核：

$$K_{h_y}(u) = (2\pi h_y^2)^{-D_y/2} \exp\left(-\frac{||u||^2}{2h_y^2}\right), \quad K_{h_x}(v) = (2\pi h_x^2)^{-D_x/2} \exp\left(-\frac{||v||^2}{2h_x^2}\right)$$

该设计的机制是：在数据密集区域 $\hat{p}(q|x)$ 较大，$\hat{\mathcal{U}}$ 较大，拉格朗日成本中的势能项使测地线倾向于穿越这些区域；在数据稀疏区域则相反。这迫使推断路径遵循数据流形，避免生成不可行的代理输出。

### 度量学习网络：特征分解参数化

动能项中的度量矩阵 $G_{\theta_G}$ 需要保证正定性且避免退化解。本文采用基于特征分解的参数化：

$$G_{\theta_G} = R_{\theta_G} E_{\theta_G} R_{\theta_G}^T$$

其中 $R_{\theta_G}$ 为通过 Givens 旋转构建的正交矩阵，$E_{\theta_G}$ 为对角特征值矩阵。特征值被约束为正且总和为非零的“特征值预算”，从而保证度量非退化。相比 Pooladian et al. (2024) 的固定对角矩阵加神经旋转（仅适用于二维），该参数化可推广至任意维度。

### 极小-极大训练目标

CLOT 联合学习度量 $G_{\theta_G}$ 和相邻时间点间的 Kantorovich 势函数 $g_{\theta_{g,k}}$。训练目标为极小-极大形式：

$$\min_{\theta_G} \sum_k \mathbb{E}_x \left[ \max_{\theta_{g,k}} \mathbb{E}_{y_k \sim \mu_k(\cdot|x)} [g_{\theta_{g,k}}^c(y_k|x)] + \mathbb{E}_{y_{k+1} \sim \mu_{k+1}(\cdot|x)} [g_{\theta_{g,k}}(y_{k+1}|x)] \right]$$

内层最大化近似相邻边缘间的条件 OT 成本，外层最小化该成本以寻求最优度量。为加速 c-变换计算，引入测地线网络 $S_{\theta_S}$ 通过样条参数化输出近似拉格朗日最短路径的参数 $\varphi = S_{\theta_S}(y_k, y_{k+1}, x)$，并最小化路径损失：

$$\mathcal{L}_{\text{path}}(\theta_S) = \mathbb{E}\left[ \mathcal{S}(q_\varphi | x) \right]$$

同时训练传输映射网络 $T_{\theta_{T,k}}$ 近似条件传输映射 $T_{c,k}$，用于暖启动 c-变换优化。

### 条件调制与推理采样

条件信息 $x$ 通过 FiLM 层注入所有网络（$g_{\theta_{g,k}}$、$T_{\theta_{T,k}}$、$S_{\theta_S}$、$G_{\theta_G}$）的第一层激活值，实现条件动态建模。推理时，对目标超参数 $t^*$，先归一化到局部参数 $s^* = (t^* - t_k) / (t_{k+1} - t_k)$，再通过测地线网络输出路径参数并求值 $\bar{\hat{y}}_{t^*} = q_\varphi(s^*)$，从而获得任意超参数下的代理输出。

## 实验与关键发现

### 核心实验设置与评估维度

本文在三个应用领域验证CLOT方法：条件轨迹推断（CTI）合成任务、强化学习奖励权重代理建模、以及时间序列分位数回归预测。所有实验均与四个基线对比：**Direct**（监督MLP插值）、**CFM**（Lipman et al., 2023）、**MFM**（Kapusniak et al., 2024）和**NLOT**（Pooladian et al., 2024）。评估指标包括负对数似然（NLL）、圆距（CD）、Wasserstein距离（WD）、代理奖励和MSE，具体取决于任务特性。

### 条件轨迹推断：半圆合成实验

在半圆CTI任务中（Figure 1, Table 1），完整方法（$K_\theta - \hat{\mathcal{U}}$）在保留时间点$t \in \{0.25, 0.75\}$上取得NLL $-0.662 \pm 0.046$，相比恒等度量无偏置基线（$K_I$）的$105.713 \pm 2.42$，提升超过106个单位。CD指标上，完整方法达到$0.016 \pm 0.001$，而$K_I$为$0.323 \pm 0.003$，降低约95%。视觉检查（Figure 1）显示，完整方法的推断轨迹正确遵循半圆几何结构，在条件间保持清晰分离，而消融模型出现路径交叉或偏离数据流形的现象。


![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_P5B97gZwRb/figures/002_Table_1.jpg]]
*Table 1: NLL and CD at t $\in {0.25, 0.75}$*

消融分析揭示了两个归纳偏置的各自贡献：学习度量$G_{\theta_G}$相比恒等度量将NLL从$-0.532$提升至$-0.662$，表明度量学习对捕捉曲率至关重要；加入势能偏置$\hat{\mathcal{U}}$使得路径能穿越数据密集区域，在稀疏观察点上的泛化性能显著改善（Figure 1b, 1d）。基于特征分解和Givens旋转的度量参数化在多个2D任务中优于固定特征值度量（Table 7），验证了其在避免退化解和支持任意维度方面的优势。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_P5B97gZwRb/figures/010_Table_7.jpg]]
*Table 7: $G _ { \theta _ { G } }$ ablations in 2D experiments*

### 强化学习奖励权重代理建模

在癌症治疗（Cancer）环境中（Table 2），完整方法在$\lambda_{nk} \in \{1,2,3,4,6,7,8,9\}$上取得平均代理奖励$102.49 \pm 5.46$，优于NLOT的$98.72$和CFM的$101.27$。Figure 2显示代理策略的NK细胞惩罚曲线与真实PPO策略高度吻合。在Reacher环境（Table 3）中，完整方法取得$-6.093 \pm 0.036$，略优于NLOT的$-6.122$，提升幅度较小但一致。在非线性奖励的Cancer_nl设置（Table 4）中，完整方法取得$91.94 \pm 11.46$的最高奖励，表明方法对奖励函数形式具有鲁棒性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_P5B97gZwRb/figures/004_Table_2.jpg]]
*Table 2: Average surrogate Cancer reward across $\lambda _ { \mathrm { { n k } } } \in \{$ 1 , $\bar { 2 }$ , 3 , 4 , $\bar { 6 }$ , 7 , 8 , 9 $\}$

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_P5B97gZwRb/figures/006_Table_4.jpg]]
*Table 4: Average surrogate Cance$r_$nl reward across $\lambda _ { \mathrm { { n k } } } \in \{$ 1 , 2 , 3 , 4 , 6 , 7 , 8 , 9 $\}$

稀疏性消融（Figure 5）表明，当可用锚点分布密度降低时，CLOT的性能退化最小，验证了归纳偏置在困难插值区域的重要性——这一优势源于势能偏置引导路径穿越数据密集区，以及度量学习提供的几何先验。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_P5B97gZwRb/figures/020_Figure_5.jpg]]
*Figure 5: Surrogate model reward in Cancer (left) and Reacher (right)*

### 时间序列分位数回归

在ETTm2分位数回归任务中（Table 5），完整方法取得MSE $0.608 \pm 0.034$，优于所有基线。Figure 3的定性对比显示，CLOT生成的80%预测区间与真实区间最为接近，而Direct方法产生过度平滑的预测，CFM和MFM在边界分位数（$\tau=0.1, 0.9$）上出现明显偏差。这一结果验证了拉格朗日成本函数中编码的动力学知识对捕捉分位数间依赖关系的有效性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_P5B97gZwRb/figures/008_Table_5.jpg]]
*Table 5: MSE of surrogate ETTm2 forecasts compared to NNs trained across quantiles τ ∈ {0.1, 0.25, 0.5, 0.75, 0.9}*

### 失败模式与局限性

尽管CLOT在多个任务上表现优异，实验也揭示了若干局限。首先，当前方法仅直接适用于**单个连续超参数**，扩展到多超参数场景面临根本性挑战：主曲线方法会破坏邻域结构，而希尔伯特曲线等空间填充方法会破坏局部性。其次，当真实超参数动力学为混沌或高度非线性时，从稀疏观察中推断可能非常困难——这在Cancer_nl任务中体现为奖励方差较大（标准差11.46）。势能偏置虽然有助于密集遍历，但在非均匀密度区域可能导致路径过度集中，需要进一步校准$\alpha$参数。所有实验主要限于较低维度输出空间（2D至中维度），推广到高维输出时的计算可扩展性尚未验证。

### 关键图表索引

- **Figure 1**: 四种消融模型在半圆CTI任务上的轨迹重建对比（散点为真实样本，连线为推断轨迹）。
- **Table 1**: 各消融模型在保留时间点上的NLL和CD量化结果。
- **Table 2**: Cancer环境中各方法的平均代理奖励对比。
- **Figure 2**: 真实PPO策略与代理策略的NK细胞惩罚随$\lambda_{nk}$变化曲线。
- **Table 4**: 非线性奖励Cancer_nl下的代理奖励对比。
- **Table 5**: ETTm2分位数回归的MSE对比。
- **Figure 3**: ETTm2预测区间的定性对比（Direct/CFM/MFM/CLOT）。
- **Figure 5**: 稀疏性消融研究，展示不同锚点密度下的奖励退化。
- **Table 7**: 度量参数化$G_{\theta_G}$的消融实验（2D任务）。

## 定位与知识库关联

### 技术谱系与基线关系

本文提出的**神经条件拉格朗日最优传输（Neural CLOT）**方法直接继承并扩展了**NLOT**（Pooladian et al., 2024）的无条件神经拉格朗日最优传输框架。NLOT 通过学习拉格朗日函数和最优传输映射来推断轨迹，但其核心局限在于：仅包含动能项（无势能偏置）、使用固定特征值的度量参数化（仅适用于二维空间）、且无法处理条件信息。CLOT 在这三个维度上进行了系统性扩展：

1. **势能项引入**：在拉格朗日函数中增加数据依赖的势能项 $\hat{\mathcal{U}}(q|x) = \alpha \log(\hat{p}(q|x) + \epsilon)$，通过 Nadaraya-Watson 条件密度估计将流形假设编码为密集遍历偏置，引导推断路径穿越数据密集区域而非走捷径。

2. **度量参数化升级**：将 NLOT 的固定对角矩阵加神经旋转（仅限二维）替换为基于特征分解和 Givens 旋转的可学习度量 $G_{\theta_G}$，支持任意维度并避免退化解——这是方法可扩展性的关键改进。

3. **条件建模**：通过 FiLM 层将条件信息注入所有网络模块，将无条件轨迹推断提升为条件轨迹推断（CTI），使代理模型能够根据上下文动态调整推断路径。

与更广泛的方法谱系相比，CLOT 的定位清晰：**Direct**（直接 MLP 插值）和**CFM**（Lipman et al., 2023）代表了简单插值和连续归一化流路线，它们在复杂非欧几里德动力学下生成不可行路径；**MFM**（Kapusniak et al., 2024）引入了数据依赖的黎曼度量，但缺乏势能偏置和条件建模。CLOT 的核心优势在于将最小作用量原理和流形假设同时编码为拉格朗日成本函数的归纳偏置，从而在稀疏观察和困难插值区域保持路径的物理可行性。

### 适用边界与局限

当前方法的适用边界明确受限于以下条件：

- **单连续超参数**：方法仅直接适用于单个连续超参数 $\lambda$ 的轨迹推断。扩展到多超参数面临根本性挑战——主曲线方法会破坏邻域结构，希尔伯特曲线等方法则会破坏局部性，使得拉格朗日动力学建模失效。
- **可微输出空间**：方法依赖基于梯度的优化和 OT 对偶公式，要求输出空间具有可微结构。
- **观察密度下限**：虽然 CLOT 在稀疏设置下表现出最强的鲁棒性（见 Figure 5 消融实验），但当观察时间点极度稀疏且真实动力学为混沌或高度非线性时，从稀疏快照推断连续轨迹本质上是不适定问题。

已识别的具体局限包括：

- **势能偏置的校准问题**：对数密度势能 $\hat{\mathcal{U}}$ 在非均匀密度区域可能导致路径过度集中于高密度区，牺牲对低密度但关键区域的覆盖——这在分布存在多模态且模态间密度差异显著时尤为突出。
- **高维可扩展性**：实验主要限于低维输出空间（2D 合成数据、RL 策略输出、分位数预测），度量矩阵 $G_{\theta_G}$ 的参数量随维度平方增长，在高维输出空间（如高分辨率图像生成）的计算成本需进一步验证。
- **条件密度估计质量**：势能偏置依赖于 Nadaraya-Watson 估计的准确性，在条件空间维度较高或样本稀疏时，核密度估计的方差会显著增大，影响偏置的可靠性。

### 开放问题与未来方向

1. **多超参数与离散超参数扩展**：如何有效处理多个连续或离散超参数的联合轨迹推断，同时保持合理的局部性和计算复杂度？这可能需要引入张量积结构或层次化分解策略。

2. **与贝叶斯优化的深度整合**：HTI 代理模型提供了推理时的连续超参数调整能力，能否将其与贝叶斯优化框架深度结合，利用代理模型的不确定性估计指导更高效的在线超参数搜索？

3. **高维输出空间的保真度保证**：在更一般的高维输出空间中，如何保证所学习拉格朗日函数的保真度并避免数值不稳定？这可能需要在度量参数化中引入低秩结构或稀疏约束。

4. **通用动态系统推断**：条件拉格朗日最优传输框架的核心思想——通过学习能量函数和度量来编码动力学偏置——能否推广到更一般的动态系统推断任务，如物理系统建模、细胞轨迹推断等？这需要验证框架在不同类型动力学先验下的泛化能力。

5. **势能偏置的自适应校准**：如何根据数据分布特性自动调整势能偏置的强度系数 $\alpha$，避免在密度均匀区域过度约束路径或在密度差异极大区域产生偏置失效？

## 原文 PDF

![[paperPDFs/ICLR_2026/Hyperparameter_Trajectory_Inference_with_Conditional_Lagrangian_Optimal_Transport.pdf]]

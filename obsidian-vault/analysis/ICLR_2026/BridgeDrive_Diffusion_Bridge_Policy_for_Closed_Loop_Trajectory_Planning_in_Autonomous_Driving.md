---
title: "BridgeDrive: Diffusion Bridge Policy for Closed-Loop Trajectory Planning in Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BridgeDrive_Diffusion_Bridge_Policy_for_Closed_Loop_Trajectory_Planning_in_Autonomous_Driving.pdf
openreview_forum_id: dJKhjK4zpp
aliases:
- BridgeDrive
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "采用扩散桥（diffusion bridge）范式替代截断扩散，保证前向与逆向过程的理论对称性，从而稳定地利用锚点先验进行上下文感知规划。"
primary_logic: "将闭环轨迹规划形式化为条件扩散桥过程：从粗糙锚点轨迹（人类专家典型行为）出发，通过扩散桥直接映射到精细化、场景自适应的轨迹，在继承锚点先验的同时完整保留扩散模型的表达能力和多模态生成优势。"
claims:
- "BridgeDrive formulates planning as a diffusion bridge that directly transforms coarse anchor trajectories into refined, context-aware plans, ensuring theoretical consistency betwe..."
- "BridgeDrive achieves a 7.72% improvement in success rate over prior SOTA on Bench2Drive with PDM-Lite dataset, and a 2.45% improvement on LEAD dataset."
- "Geometric path waypoints representation yields +15.09% success rate improvement over temporal waypoints for BridgeDrive, validating the design choice."
- "Removing anchor diffusion (using only a single anchor without iterative refinement) or using only anchor classification without diffusion drastically drops performance, confirming..."
---

# BridgeDrive: Diffusion Bridge Policy for Closed-Loop Trajectory Planning in Autonomous Driving

> [!tip] 核心洞察
> 将闭环轨迹规划形式化为条件扩散桥过程：从粗糙锚点轨迹（人类专家典型行为）出发，通过扩散桥直接映射到精细化、场景自适应的轨迹，在继承锚点先验的同时完整保留扩散模型的表达能力和多模态生成优势。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BridgeDrive：面向自动驾驶闭环轨迹规划的扩散桥策略 |
| 英文题名 | BridgeDrive: Diffusion Bridge Policy for Closed-Loop Trajectory Planning in Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dJKhjK4zpp); [GitHub](https://github.com/shuliu-ethz/BridgeDrive) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | BridgeDrive |
| Dataset | Bench2Drive (PDM-Lite expert), LEAD dataset (LEAD expert) |

> [!tip] 效果简介
> - Bench2Drive (PDM-Lite expert) 上，Driving Score 为 87.99，对比 85.07 (SimLingo)，变化 +2.92。
> - Bench2Drive (PDM-Lite expert) 上，Success Rate (%) 为 74.99，对比 67.27 (SimLingo / TransFuser++)，变化 +7.72。
> - LEAD dataset (LEAD expert) 上，Success Rate (%) 为 89.25，对比 86.8 (TFv6)，变化 +2.45。

## 概述

### 问题背景与瓶颈

自动驾驶闭环轨迹规划要求模型在复杂动态场景中生成安全、可行且多模态的驾驶行为。近年来，扩散模型因其强大的表达能力和多模态生成优势被引入该领域，典型代表如 **DiffusionDrive**（Liao et al., 2025）等基于锚点（anchor）的扩散规划器。然而，这类方法存在一个根本性的理论缺陷：它们采用**截断扩散调度（truncated diffusion schedule）**，前向加噪过程仅进行到中间时刻 $T_{\text{trunc}}$，而逆向去噪过程却从噪声锚点直接回归真实轨迹，导致前向与逆向过程**不对称**，违背了扩散模型的理论核心。这种不对称性使得规划行为不可预测，在安全性上存在隐患。

### 核心思路

**BridgeDrive** 提出以**扩散桥（diffusion bridge）**范式替代截断扩散，从根本上解决上述理论不一致问题。其核心洞见是：将闭环轨迹规划形式化为一个条件扩散桥过程——从粗糙的锚点轨迹（代表人类专家典型驾驶行为）出发，通过扩散桥直接映射到精细化、场景自适应的轨迹。这一范式在继承锚点先验的同时，完整保留了扩散模型的表达能力和多模态生成优势，确保前向与逆向过程的理论对称性。

具体而言，BridgeDrive 将前向过程定义为从真实轨迹 $x_0$ 扩散至锚点 $x_T$，逆向过程则从锚点沿对称路径去噪恢复 $x_0$。训练时，去噪网络直接学习如何从锚点逐步去噪至与场景一致的规划，并通过一个分类器选取最优锚点作为扩散桥起点。

### 方法定位

在方法谱系上，BridgeDrive 属于**锚点引导的扩散策略**，其关键改进体现在三个层面：

- **扩散过程对称性**：以扩散桥替代截断扩散，保证前向与逆向过程的理论一致性。
- **轨迹表示形式**：采用几何路径路点（geometric path waypoints）替代传统的时间速度路点（temporal speed waypoints），将等空间间隔的未来坐标与独立速度标量解耦，更易泛化且更符合路由要求。
- **锚点引导机制**：锚点作为扩散桥终点 $x_T$，去噪网络显式建模从锚点到场景一致规划的扩散桥，而非简单地从噪声锚点回归真实轨迹。

### 主要结果

在 **Bench2Drive** 闭环评测基准（PDM-Lite 专家）上，BridgeDrive 取得了当时最优性能：

- **驾驶得分（Driving Score）**：87.99，较此前最佳方法 **SimLingo**（Renz et al., 2025）的 85.07 提升 +2.92。
- **成功率（Success Rate）**：74.99%，较此前最佳的 SimLingo/TransFuser++ 的 67.27% 提升 **+7.72%**。

在 **LEAD** 数据集（LEAD 专家）上，BridgeDrive 同样表现优异：成功率达到 89.25%，较 **TFv6** 的 86.8% 提升 +2.45%；驾驶得分 96.34，较 TFv6 的 95.2 提升 +1.14。

消融实验进一步验证了关键设计选择的有效性：几何路径路点表示相较时间路点带来 **+15.09%** 的成功率提升；去除锚点扩散桥（仅分类器选择锚点而不经迭代优化）导致成功率骤降至 ≤36.36%，证实扩散桥迭代优化不可或缺。

### 局限与开放问题

BridgeDrive 在舒适性（Comfortness）和礼让（Give Way）指标上表现欠佳，倾向于频繁刹车以追求安全，可能牺牲乘客体验。此外，模型难以有效处理分布外场景（如累积误差导致的不合时机变道），且尚未集成视觉语言模型（VLA）的先验知识。如何在不牺牲安全性的前提下改善舒适性、高效蒸馏为单步规划器以降低推理延迟，以及融入 VLA 先验或通过强化学习后训练处理分布外场景，是值得进一步探索的方向。

## 背景与动机

自动驾驶闭环轨迹规划要求模型在复杂动态场景中生成安全、可执行且多模态的未来轨迹。近年来，扩散模型因其强大的高维分布建模能力和多模态生成优势，被引入该领域作为轨迹解码器。然而，现有基于锚点的扩散规划器——最具代表性的是 **DiffusionDrive**（Liao et al., 2025）——在理论层面存在一个根本性缺陷：其采用**截断扩散调度（Truncated Diffusion）**。

具体而言，DiffusionDrive 的前向过程仅将真实轨迹加噪至某个中间时刻 $T_\text{trunc}$，而非标准扩散的纯噪声终点；逆向去噪过程则从噪声化的锚点轨迹出发，直接回归真实轨迹。这导致**前向扩散路径与逆向去噪路径不对称**，违背了扩散模型“前向加噪—逆向去噪”互为逆过程的理论核心。这一理论不一致性带来的直接后果是：规划行为不可预测，安全性与可靠性受限。

从因果机制来看，问题的关键在于**锚点先验的利用方式**。锚点（通常由 K-means 聚类人类专家轨迹得到）蕴含了典型驾驶行为的强先验，但截断扩散仅将其作为去噪的起始点，并未建立从锚点到精细化轨迹的结构化映射。模型被训练为从任意噪声锚点“跳回”真实轨迹，而非沿一条与锚点信息保持一致的连续路径逐步去噪。

BridgeDrive 的核心洞察在于：**将闭环轨迹规划形式化为条件扩散桥（Diffusion Bridge）过程**。扩散桥是一种特殊的扩散范式，其前向过程从真实轨迹 $x_0$ 扩散至指定的锚点 $x_T$，逆向过程则从锚点沿对称路径去噪恢复 $x_0$，从而保证前向与逆向过程的理论一致性。这相当于从粗糙锚点轨迹出发，通过扩散桥直接映射到精细化、场景自适应的轨迹，在继承锚点先验的同时完整保留扩散模型的表达能力和多模态生成优势。

此外，轨迹表示形式的选择也是影响规划性能的重要瓶颈。现有方法普遍采用**时间速度路点（Temporal Speed Waypoints）**——以等时间间隔采样未来坐标，速度信息隐含于相邻路点间距中。这种表示在跨场景泛化时面临困难，且与路由规划中“等空间间隔”的自然要求不匹配。BridgeDrive 转而采用**几何路径路点（Geometric Path Waypoints）**：以等空间间隔采样未来坐标，并附加独立的速度标量，使轨迹表示更易泛化且与驾驶任务结构对齐。

综上，BridgeDrive 的动机源于两个层面的改进需求：**理论层面**，以扩散桥替代截断扩散，恢复前向—逆向过程的对称性；**表示层面**，以几何路径路点替代时间路点，提升轨迹表示的泛化能力和任务适配性。这两项设计共同构成了一个理论一致、锚点引导的扩散规划框架。

## 核心创新

BridgeDrive 的核心创新在于将闭环轨迹规划重新形式化为**条件扩散桥（Conditional Diffusion Bridge）过程**，从根本上解决了现有基于锚点的扩散规划器（如 DiffusionDrive）中前向与逆向过程不对称的理论缺陷。

### 瓶颈洞察：截断扩散的理论不一致

现有锚点引导的扩散规划器普遍采用**截断扩散（Truncated Diffusion）**策略：前向过程仅将真实轨迹加噪至某一中间时刻 $T_{\text{trunc}}$，而非完整的噪声分布；逆向过程则从噪声锚点直接回归真实轨迹。这种不对称设计违背了扩散模型“前向加噪—逆向去噪”的理论核心，导致规划行为不可预测、安全性受限。

BridgeDrive 的关键洞察在于：与其将锚点视为扩散的**起点**（加噪后的中间状态），不如将锚点定义为扩散桥的**终点**。这一视角转换使得前向与逆向过程在理论上天然对称。

### 核心机制：扩散桥范式

BridgeDrive 将规划问题分解为两步生成过程：

$$p_d(x, y, z) = p_d(x|y, z) \, p_d(y|z) \, p_d(z)$$

其中 $x$ 为真实轨迹，$y$ 为锚点（K-means 聚类中心），$z$ 为场景条件。扩散桥 SDE 直接连接真实轨迹 $x_0$ 与锚点 $x_T$：

$$\mathrm{d}x_t = f(t) x_t \mathrm{d}t + g(t)^2 \nabla_{x_t} \log q(x_T | x_t) + g(t) \mathrm{d}w_t, \quad x_0 \sim p_d, \ x_T = y$$

这一形式保证了前向扩散与逆向去噪的**理论对称性**：逆向过程从锚点 $x_T$ 出发，沿对称路径逐步去噪，最终恢复与场景一致的精细化轨迹 $x_0$。该过程可通过概率流 ODE 高效模拟，兼容快速采样器。

### 关键设计变更

| 设计维度 | 现有方法（DiffusionDrive 等） | BridgeDrive |
|---------|---------------------------|-------------|
| **扩散过程对称性** | 截断扩散：前向仅加噪至 $T_{\text{trunc}}$，逆向从噪声锚点直接回归 GT，路径不匹配 | 扩散桥：前向从 $x_0$ 扩散至 $x_T$，逆向从 $x_T$ 沿对称路径去噪恢复 $x_0$ |
| **轨迹表示** | 时间速度路点（等时间间隔坐标，速度隐含于间距） | 几何路径路点（等空间间隔坐标 + 独立速度标量） |
| **锚点引导** | 以 K-means 锚点为起始点，训练目标为从噪声锚点回归 GT | 锚点作为扩散桥终点 $x_T$，去噪网络学习从锚点逐步去噪至场景自适应轨迹 |
| **训练目标** | 标准条件去噪 MSE 损失，仅预测 $x_0$ | 条件扩散桥去噪损失 + 锚点分类交叉熵损失，确保目标与扩散桥结构对齐 |

### 证据强度

消融实验提供了强因果证据：

- **几何路径路点**：相比时间路点，BridgeDrive 成功率提升 **+15.09%**（Table 2），验证了表示形式对扩散规划的显著影响。
- **扩散桥必要性**：仅使用分类器选择锚点而不经扩散桥优化（Anchor-only），成功率骤降至 **≤36.36%**（Table 10），证明迭代去噪过程不可替代。
- **锚点引导必要性**：去除锚点（$k=1$）仅依赖扩散桥时，性能与全扩散模型相当，但仍远优于无扩散桥模型，表明锚点引导与扩散桥互为必要组件。
- **锚点分类精度敏感性**：选择次优或第三优锚点会使成功率从 74.99% 显著下降至 57.72%（Table 9），说明分类器性能对整体系统影响显著。

### 局限性

尽管扩散桥范式在理论上更优雅，但其性能增益高度依赖锚点分类器的精度。当分类器选择错误锚点时，扩散桥可能将轨迹引导至不合理方向（Figure 1 红色轨迹示例）。此外，模型在舒适性指标上表现欠佳，倾向于频繁刹车以追求安全，且无法有效处理分布外场景（如累积误差导致的不合时机变道，Figure 7）。

## 整体框架

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_dJKhjK4zpp/figures/002_Figure_2.jpg]]
*Figure 2: Diagram for the planning procedure of BridgeDrive in Algorithm 3. The model architecture of the neural network denoiser $x _ { \theta } ( x _ { t }$ , t , $x _ { T }$ , z ) is detailed in the light blue box*

BridgeDrive 将闭环轨迹规划形式化为一个**条件扩散桥（conditional diffusion bridge）**过程，其核心思想是：从一组代表人类专家典型行为的粗糙锚点轨迹出发，通过扩散桥直接映射到精细化、场景自适应的轨迹，在继承锚点先验的同时完整保留扩散模型的表达能力和多模态生成优势。

整个 pipeline 由三个核心模块串联构成，其数据流与模块关系如图 2 所示：

### 1. 感知模块（Perception Module）

感知模块基于预训练的 **TransFuser++**（Zimmerlin et al., 2024）构建，负责从多传感器输入中提取场景上下文条件 $z$。具体输出包括：
- BEV 语义特征
- 动态目标检测框
- 交通信号状态
- 多传感器融合特征

该模块为下游的规划过程提供统一的场景条件信息，所有对比基线方法均共享相同的感知模块以保证公平比较。

### 2. 锚点分类器模块（Anchor Classifier Module）

锚点分类器接收 BEV 特征和融合特征，通过交叉注意力与所有预定义的锚点集合 $\mathcal{Y} = \{y^i\}_{i=1}^{N_{\text{anchor}}}$ 进行交互，输出每个锚点的选择概率。推理时选取最高概率的锚点作为扩散桥的终点 $x_T$。

锚点本身是通过 K-means 聚类从训练集轨迹中提取的离散原子行为，包含几何路径路点 $x_y^{\text{geo}}$ 和速度标量 $v_y$，代表典型的驾驶操作（如直行、左转、变道等）。

### 3. 去噪器模块（Denoiser Module）

去噪器是扩散桥的核心计算单元，其输入包括：
- 当前噪声轨迹 $x_t$
- 扩散时间步 $t$
- 选定的锚点 $x_T$
- 场景条件 $z$

去噪器首先通过可变形交叉注意力（deformable cross-attention）与 BEV 特征交互，再与融合特征进行交叉注意力，最终由 MLP 预测去噪后的平均轨迹 $x_\theta(x_t, t, x_T, z)$。该预测值随后被用于近似条件得分函数，驱动 PF-ODE 从锚点 $x_T$ 逐步去噪至最终规划轨迹 $x_0$。

### 推理流程

BridgeDrive 的推理遵循 Algorithm 3 的规划流程：
1. 感知模块提取场景条件 $z$
2. 锚点分类器选择最优锚点 $x_T = y^*$
3. 以 $x_T$ 为起点，通过 PF-ODE 求解器迭代去噪（如 Euler 或 DPM-Solver），每一步调用去噪器 $x_\theta$ 预测 $x_0$，并利用式 (10) 的得分近似计算梯度方向
4. 输出最终去噪轨迹 $x_0$ 作为闭环控制信号

### 训练流程

训练阶段（Algorithm 1）是 **simulation-free** 的：给定真实轨迹 $x_0$ 和对应的锚点 $x_T$，直接从解析高斯转移核 $q(x_t | x_0, x_T)$ 采样中间噪声状态 $x_t$，最小化去噪器预测与 $x_0$ 之间的均方误差（式 9）。同时，锚点分类器通过交叉熵损失学习预测与 $x_0$ 最近的锚点（式 11）。这种训练方式无需模拟前向 SDE，显著提升了训练效率。

### 与截断扩散的关键区别

与 **DiffusionDrive**（Liao et al., 2025）等采用截断扩散的基线方法不同，BridgeDrive 的扩散桥范式保证了前向扩散过程与逆向去噪过程的理论对称性。在截断扩散中，前向仅加噪至中间时刻 $T_{\text{trunc}}$，逆向从噪声锚点直接回归 GT，二者并不匹配；而 BridgeDrive 的前向过程从真实轨迹 $x_0$ 扩散至锚点 $x_T$，逆向过程沿对称路径从 $x_T$ 去噪恢复 $x_0$，从根本上消除了理论不一致性。

## 核心模块与公式推导

### 轨迹表示：从时间路点到几何路点

BridgeDrive 首先在轨迹表示层面对现有扩散规划器进行了关键修正。传统方法（如 **DiffusionDrive**，Liao et al., 2025）采用**时间速度路点**（Temporal speed waypoints）：

$$\dot{\boldsymbol{x}} := \boldsymbol{x}^{\mathrm{temp}} \in \mathbb{R}^{N_{\mathrm{point}} \times 2}$$

该表示以等时间间隔采样未来坐标，速度信息隐含于相邻点间距中，导致泛化困难。BridgeDrive 改用**几何路径路点**（Geometric path waypoints）：

$$\overline{\boldsymbol{x}} := (x^{\mathrm{geo}}, \boldsymbol{v}) \in \mathbb{R}^{N_{\mathrm{point}} \times 2} \times \mathbb{R}$$

即以等空间间隔采样未来坐标，并显式分离速度标量。消融实验（Table 2）表明，仅此改动即为 BridgeDrive 带来 **+15.09%** 的成功率提升，验证了几何表示更契合扩散规划的需求。

### 扩散桥：前向-逆向对称性的理论保证

BridgeDrive 的核心创新在于用**扩散桥**（Diffusion Bridge）范式替代现有方法的截断扩散调度。截断扩散（如 DiffusionDrive）的前向过程仅加噪至中间时刻 $T_{\text{trunc}}$，逆向过程从噪声锚点直接回归真值，前向与逆向路径不对称，违背扩散模型理论基础。

BridgeDrive 将规划形式化为条件扩散桥过程：从真实轨迹 $x_0$ 出发，通过前向 SDE 直接扩散至锚点 $x_T = y$：

$$\mathrm{d}x_t = f(t) x_t \mathrm{d}t + g(t)^2 \nabla_{x_t} \log q(x_T | x_t) + g(t) \mathrm{d}w_t, \quad x_0 \sim p_d, \ x_T = y$$

该 SDE 保证前向过程精确终止于指定锚点，且存在解析的高斯转移核：

$$q(x_t | x_0, x_T) = \mathcal{N}(x_t | a_t x_T + b_t x_0, c_t^2 I)$$

逆向过程则沿对称路径从锚点去噪恢复精细化轨迹，通过概率流 ODE 实现高效采样：

$$\frac{\mathrm{d}x_t}{\mathrm{d}t} = f(t) x_t - g(t)^2 \left( \frac{\nabla_{x_t} \log q(x_t | x_T, z)}{2} - \nabla_{x_t} \log q(x_T | x_t) \right)$$

这一设计从理论上保证了前向与逆向过程的一致性，使锚点先验被稳定地利用。

### 训练目标与得分函数近似

训练去噪网络 $x_\theta$ 时，BridgeDrive 最小化条件扩散桥去噪损失：

$$\operatorname*{min}_{\theta} \mathbb{E}_{p(t)p_d(x_0,x_T,z)q(x_t|x_0,x_T)} \left[ w(t) \| x_{\theta}(x_t, t, x_T, z) - x_0 \|^2 \right]$$

训练过程是 simulation-free 的——无需模拟前向 SDE，可直接从高斯转移核采样 $x_t$。训练完成后，条件得分函数可通过去噪网络近似：

$$\nabla_{x_t} \log q(x_t | x_T, z) \approx \frac{a_t x_T + b_t x_{\theta}(x_t, t, x_T, z) - x_t}{c_t^2}$$

### 锚点分类器与联合训练

BridgeDrive 的锚点选择并非简单的最近邻检索，而是训练一个专用分类器 $h_\phi$，以交叉熵损失预测给定场景条件 $z$ 下最优锚点 $y$：

$$\mathcal{L}_{\text{cls}} = -\log h_\phi(y | z)$$

该分类器与去噪网络联合训练，确保锚点选择与扩散桥去噪目标对齐。推理时，分类器选取最高概率锚点作为 $x_T$，再由去噪网络沿 PF-ODE 迭代生成规划轨迹。

### 架构概览

BridgeDrive 的神经网络由三个模块组成：

- **感知模块**：基于预训练 **TransFuser++**（Zimmerlin et al., 2024）提取 BEV 语义、动态目标框、交通信号及多传感器融合特征，作为条件信息 $z$。
- **去噪模块**：接收噪声轨迹 $x_t$、时间步 $t$、锚点 $x_T$ 和条件 $z$，通过可变形交叉注意力与 BEV 交互，再与融合特征交叉注意力，最终由 MLP 预测去噪后的平均轨迹。
- **锚点分类器模块**：利用 BEV 和融合特征与所有锚点进行交叉注意力，输出每个锚点的概率分布。

## 实验与分析

### 核心性能对比

BridgeDrive 在 Bench2Drive 闭环评测上达到 SOTA：Driving Score 87.99，成功率 74.99%，较此前最优方法 **SimLingo**（Renz et al., 2025）分别提升 +2.92 和 +7.72 个百分点（Table 1）。值得注意的是，BridgeDrive 未使用视觉语言模型（VLA）先验，却显著超越了同样未用 VLA 的扩散基线 **DiffusionDrive**（Liao et al., 2025）的两个适配版本（DiffusionDrive_temp 成功率 56.08%，DiffusionDrive_geo 成功率 59.90%），以及集成了 VLA 的 **ORION diffusion**（Fu et al., 2025，成功率 59.37%）。这直接验证了扩散桥范式的理论优势——对称的前向-逆向过程使锚点引导的扩散规划更稳定、更安全。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_dJKhjK4zpp/figures/003_Table_1.jpg]]
*Table 1: Comparison between BridgeDrive and previous baselines on Bench2Drive. Our method shows SOTA performance on both Driving Score (DS) and Success Rate (SR). Notably, by using a principled diffusion bridge model, our method achieves significant improvements over previous diffusion baselines (including those with prior knowledge from VLA), demonstrating the effectiveness of the diffusion module in the autonomous driving task when following our paradigm as discussed in Section 3.2. A potential avenue to further improve our method is to integrate prior knowledge from VLA, which is left as future work*

在 LEAD 数据集上的泛化实验中，BridgeDrive 成功率达 89.25%，Driving Score 96.34，分别超过 LEAD 基线 TFv6 2.45 和 1.14 个百分点（Table 3/Table 11），证明方法在不同专家策略下具有鲁棒的迁移能力。

### 关键设计消融

**轨迹表示形式**（Table 2）是影响性能的核心因素。将时间速度路点替换为几何路径路点后，BridgeDrive 成功率从 59.90% 跃升至 74.99%（+15.09 个百分点），Driving Score 从 79.67 升至 87.99。这一增益在 DiffusionDrive 和 Full Diffusion 变体上也一致出现，说明几何等距路点 + 独立速度标量的表示更利于扩散模型学习场景自适应的规划，同时天然契合路由约束。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_dJKhjK4zpp/figures/008_Table_2.jpg]]
*Table 2: Ablation study for the effects of temporal and geometric path waypoints for Diffusion-Drive, full diffusion, and BridgeDrive. All methods use identical expert and modules except for the diffusion part. Our BridgeDrivegeo achieves SOTA DS and SR, prioritizing safety over Comfortness*

**扩散桥的必要性**由 Table 10 给出强证据：
- 仅用锚点分类直接输出轨迹（Anchor-only），成功率仅 36.36%，说明离散锚点本身不足以覆盖场景多样性；
- 仅用锚点回归（无扩散迭代），成功率 42.24%，虽有改善但仍远低于 BridgeDrive 的 74.99%；
- 去除锚点引导（k=1，即纯扩散桥），成功率 59.90%，与全扩散模型相当，但比有锚点引导的 BridgeDrive 低 15.09 个百分点。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_dJKhjK4zpp/figures/017_Table_10.jpg]]
*Table 10: Influence of the number of anchors on the performance of BridgeDrive and anchor-based classification and regression planning models*

这组消融确立了 BridgeDrive 的两个必要组件：**锚点引导提供粗粒度先验，扩散桥提供细粒度迭代优化**，二者缺一不可。

**锚点数量与分类精度**（Table 10, Table 9）揭示了多样性-精度权衡：锚点数从 1 增至 60 时成功率持续上升，超过 60 后因分类器精度下降而回落。选择次优锚点会使成功率从 74.99% 骤降至 67.27%，第三优则进一步降至 57.72%（Table 9），说明锚点分类器是整体性能的关键瓶颈。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_dJKhjK4zpp/figures/016_Table_9.jpg]]
*Table 9: Influence of anchor classification accuracy on the performance of BridgeDrive*

### 多维能力与安全-舒适权衡

在多维能力评测（Table 6）中，BridgeDrive 在并道（+11.17）、交通标志响应（+7.02）、紧急制动（90.00%）等场景显著领先，但在礼让（Give Way）和超车（Overtake）上并非最优。结合 Table 5 的全面对比，BridgeDrive 的舒适性指标（Comfort 20.98）明显低于多数基线（如 SimLingo 28.11），呈现典型的**安全优先策略**：模型倾向于频繁刹车以确保不碰撞，代价是牺牲乘客舒适度。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_dJKhjK4zpp/figures/012_Table_6.jpg]]
*Table 6: Multi-ability evaluation results on Bench2Drive. BridgeDrive outperforms all baselines in all categories except for Give Way and Overtake*

### 定性分析：锚点引导如何影响行为

Figure 3-6 的对比案例直观展示了锚点引导的作用：
- **超车场景**：BridgeDrive_temp（时间路点，无锚点引导）在超车时速度控制失当，与旁车碰撞（Figure 3）；BridgeDrive_geo（几何路点 + 锚点引导）在同一场景下顺利完成超车（Figure 4）。
- **变道场景**：Full Diffusion（无锚点）错过变道时间窗口，撞上护栏（Figure 5）；BridgeDrive 借助锚点引导及时变道，成功通过岔路（Figure 6）。

这些案例表明，锚点提供了“典型人类行为”的强先验，使扩散过程不至于偏离到危险轨迹空间。

### 推理效率

Table 7 显示 BridgeDrive 的推理耗时约是全扩散模型的 2 倍（因增加了锚点交叉注意力模块），但在未做任何推理优化的情况下仍达到可部署水平。论文指出这是可接受的实时性代价，且可通过蒸馏为单步规划器进一步加速。

### 已知失败模式

1. **分布外场景**：Figure 7 展示了因累积误差导致的不合时机变道，训练数据中缺乏此类样本，模型无法正确处理。
2. **舒适性不足**：安全优先策略导致频繁刹车，在礼让和舒适性指标上表现欠佳。
3. **锚点分类错误**：当分类器选错锚点时，扩散桥从错误起点出发，难以恢复到合理轨迹（Table 9, Figure 1 红色轨迹）。

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果调控

现有基于锚点的扩散规划器（如 **DiffusionDrive**，Liao et al., 2025）采用**截断扩散调度**（Truncated Diffusion）：前向过程仅加噪至中间时刻 $T_{\text{trunc}}$，逆向过程则从噪声锚点直接回归真实轨迹。这种前向与逆向过程的**不对称性**违背了扩散模型的理论核心——生成过程应与破坏过程互为逆映射。其直接后果是：去噪网络学习到的映射缺乏理论保证，导致规划行为不可预测，安全性受限。

BridgeDrive 的因果调控旋钮是：**以扩散桥（Diffusion Bridge）范式替代截断扩散**。扩散桥将前向过程定义为一个连接真实轨迹 $x_0$ 和锚点 $x_T$ 的条件扩散过程：

$$
\mathrm{d}x_t = f(t) x_t \mathrm{d}t + g(t)^2 \nabla_{x_t} \log q(x_T | x_t) + g(t) \mathrm{d}w_t, \quad x_0 \sim p_d, \ x_T = y
$$

该过程保证了前向与逆向的**理论对称性**：逆向过程从锚点 $x_T$ 出发，沿对称路径去噪恢复 $x_0$。这使得模型能够稳定地利用锚点先验进行上下文感知规划，同时完整保留扩散模型的表达能力和多模态生成优势。

### 2. 方法定位与基线关系

BridgeDrive 定位于**闭环轨迹规划**任务，与以下基线工作形成对比：

| 基线方法 | 范式 | 关键差异 |
|---------|------|---------|
| **TCP-traj** (Wu et al., 2022) | 端到端相机规划 | 无扩散机制，缺乏多模态生成能力 |
| **UniAD-Base** (Hu et al., 2023) | 全栈端到端框架 | 统一多任务，但规划模块非扩散式 |
| **VAD** (Jiang et al., 2023) | 矢量化端到端规划 | 基于矢量化场景表征，未使用扩散 |
| **DriveTransformer** (Jia et al., 2025) | 任务并行端到端规划 | 依赖时序融合，无锚点引导 |
| **ORION / ORION diffusion** (Fu et al., 2025) | VLA 规划器 | 引入视觉语言先验，扩散组件为截断式 |
| **DiffusionDrive** (Liao et al., 2025) | 锚点引导扩散规划 | **最直接的前身**：使用截断扩散，前向-逆向不对称 |
| **SimLingo** (Renz et al., 2025) | VLA 规划器 | 当前 SOTA，BridgeDrive 在 SR 上超越 +7.72% |
| **TransFuser++** (Zimmerlin et al., 2024) | 感知基础规划器 | CARLA 挑战赛亚军，BridgeDrive 复用其感知模块 |

BridgeDrive 与 **DiffusionDrive** 的关系最为密切，可视为其**理论修正版**。两者共享锚点引导的思想，但在三个关键维度上存在本质差异：

1. **扩散过程对称性**：DiffusionDrive 的截断扩散前向仅加噪至中间时刻，逆向从噪声锚点直接回归 GT，无法匹配前向路径。BridgeDrive 的扩散桥保证前向从 $x_0$ 扩散至 $x_T$，逆向从 $x_T$ 沿对称路径恢复 $x_0$。

2. **训练目标对齐**：DiffusionDrive 使用标准条件扩散去噪 MSE 损失，仅预测 $x_0$，与截断过程不匹配。BridgeDrive 的条件扩散桥去噪损失（Eq. 9）结合锚点分类交叉熵损失（Eq. 11），确保去噪目标与扩散桥结构对齐。

3. **锚点角色**：DiffusionDrive 以 K-means 锚点为起始点，但训练任务为从噪声锚点回归 GT，并未显式建模从锚点到 GT 的扩散桥。BridgeDrive 将锚点作为扩散桥终点 $x_T$，去噪网络直接学习如何从锚点逐步去噪至与场景一致的规划。

### 3. 适用边界与局限

#### 3.1 已知局限

- **舒适性指标欠佳**：BridgeDrive 在 Comfortness 指标上表现低于多数基线（20.98 vs. SimLingo 的 26.25），倾向于频繁刹车以追求安全性，可能牺牲乘客体验（Table 5）。
- **礼让场景薄弱**：在 Give Way 类别上未能超越所有基线（Table 6），说明模型在交互博弈场景中的决策仍不够精细。
- **分布外泛化不足**：模型无法有效处理因累积误差导致的不合时机变道（Figure 7），此类场景在训练数据中缺乏覆盖。
- **未集成 VLA 先验**：当前模型未融合视觉语言模型的先验知识，可能限制对复杂语义场景的理解深度。

#### 3.2 适用条件

- 适用于有锚点先验可用的闭环规划场景（如城市道路、高速公路）。
- 依赖高质量的感知模块（当前复用 TransFuser++），感知误差会累积影响规划质量。
- 锚点分类器性能对整体效果影响显著：选择次优锚点会导致成功率从 74.99% 显著下降至 65.74%（Table 9）。

### 4. 开放问题

1. **安全-舒适权衡**：如何在保持高安全性的前提下改善舒适性和礼让指标？是否需要引入多目标优化或奖励塑形？

2. **推理加速**：当前 BridgeDrive 的推理速度约为全扩散模型的两倍（Table 7），如何将扩散桥策略高效蒸馏为单步规划器，在保持生成质量的同时进一步降低延迟？

3. **分布外鲁棒性**：如何融入 VLA 先验知识或通过强化学习后训练（post-training）处理分布外场景？ORION 等 VLA 方法已验证语言先验的价值，将其与扩散桥结合是自然延伸。

4. **路点表示的理论分析**：几何路径路点相对于时间路点的 +15.09% 成功率提升（Table 2）是否具有普适性？两种表示在不同驾驶任务（如跟车 vs. 变道）中的根本作用及最优融合方式仍需深入探索。

5. **锚点多样性与分类精度的最优平衡**：锚点数量从 1 增加到 60 时成功率逐步上升，超过 60 后因分类精度下降而回落（Table 10）。如何动态调整锚点数量或设计更鲁棒的分类机制以适应不同场景复杂度？

## 原文 PDF

![[paperPDFs/ICLR_2026/BridgeDrive_Diffusion_Bridge_Policy_for_Closed_Loop_Trajectory_Planning_in_Autonomous_Driving.pdf]]

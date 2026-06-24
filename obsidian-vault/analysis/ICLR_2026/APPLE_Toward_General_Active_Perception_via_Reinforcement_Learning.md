---
title: "APPLE: Toward General Active Perception via Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/APPLE_Toward_General_Active_Perception_via_Reinforcement_Learning.pdf
aliases:
- AAPPL
- APPLE
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "APPLE将主动感知建模为POMDP，并把可微预测损失并入强化学习奖励来联合训练策略与预测器。"
primary_logic: "共享Transformer骨干处理观测序列，同时输出控制动作和属性预测，再用SAC或CrossQ优化信息采集与推断。"
claims:
- "APPLE只需POMDP环境和可微损失即可应用到触觉、视觉分类、体积回归与定位任务。"
- "将预测损失写入奖励使策略梯度和监督学习梯度在同一目标下协同优化。"
- "APPLE-SAC和APPLE-CrossQ在MHSB、CircleSquare和TactileMNIST等任务上优于HAM或随机探索基线。"
---

# APPLE: Toward General Active Perception via Reinforcement Learning

> [!tip] 核心洞察
> 通过将预测损失作为奖励的一部分，策略梯度与监督学习梯度可自然分解，从而在统一框架下同时学习信息采集和属性推断。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | APPLE：基于强化学习的通用主动感知方法 |
| 英文题名 | APPLE: Toward General Active Perception via Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hU2gT2Ucua); [Project](https://timschneider42.github.io/apple) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | APPLE (Active Perception Policy Learning) |
| Dataset | MHSB (触觉分类), CircleSquare (视觉分类), TactileMNIST (触觉分类), TactileMNISTVolume (触觉体积回归) |

> [!tip] 效果简介
> - MHSB (触觉分类) 上，最终预测准确率 为 ~100% (APPLE-SAC/CrossQ, 250K步)，对比 68% (HAM, 1M步)，变化 +32%。
> - CircleSquare (视觉分类) 上，最终预测准确率 为 97% (APPLE-SAC), 96% (APPLE-CrossQ)，对比 随机猜测 (HAM), 68% (APPLE-RND)，变化 +29% (vs APPLE-RND)。
> - TactileMNIST (触觉分类) 上，最终预测准确率 为 87% (APPLE-SAC), 89% (APPLE-CrossQ)，对比 74% (APPLE-RND)，变化 +15% (APPLE-CrossQ vs RND)。

## 概述

本文提出 **APPLE (Active Perception Policy Learning)**，一个将强化学习与监督学习相结合的通用主动感知框架。APPLE 将主动感知建模为部分可观测马尔可夫决策过程（POMDP），通过联合优化基于 Transformer 的感知模块和决策策略，使智能体能够在与环境交互的过程中主动采集信息并推断目标属性。该方法仅需可微损失函数和 POMDP 环境即可应用，不限于特定任务。

APPLE 的两个变体——APPLE-SAC（基于 SAC Haarnoja et al. (2018)）和 APPLE-CrossQ（基于 CrossQ Bhatt et al. (2019)）——在触觉分类、体积回归、物体定位和视觉分类等五个基准任务上进行了评估。实验结果表明，APPLE 在多个任务上显著优于现有基线方法 HAM (Fleer et al., 2020) 和随机策略基线。

## 背景与动机

**现有瓶颈**：现有主动感知方法通常针对特定任务设计，依赖贪婪信息增益启发式或假设物体静止，缺乏通用性。例如，HAM (Fleer et al., 2020) 使用基于 REINFORCE 的 LSTM 模型，在简单任务上表现良好，但在需要更复杂探索策略的任务上难以超越随机猜测。

**核心动机**：主动感知问题天然适合 POMDP 框架——智能体必须在不确定性下行动，通过主动采集信息来减少关于目标属性的模糊性。然而，现有方法未能充分利用监督学习信号与强化学习策略之间的协同效应。

## 核心创新

APPLE 的核心创新在于：

1. **统一优化框架**：将主动感知目标函数定义为期望折扣回报最大化，其中奖励由 RL 奖励和可微预测损失组成。目标函数的梯度自然分解为策略梯度与负监督损失梯度，从而在统一框架下同时学习信息采集和属性推断。

2. **共享 Transformer 骨干网络**：感知模块和决策策略共享基于 Transformer 的骨干网络，联合处理观测序列并输出预测和动作。这种架构比 LSTM 具有更快的收敛速度。

3. **奖励函数设计**：总奖励 $\tilde{r}(h_t, y^*_t, a_t, y_t) = r(h_t, a_t) - \ell(y^*_t, y_t)$，其中 $r(h_t, a_t)$ 用于正则化动作（如动作幅度惩罚），$\ell(y^*_t, y_t)$ 是可微预测损失。这种设计使得预测损失既作为监督信号又作为奖励信号的一部分。

## 整体框架

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_hU2gT2Ucua_APPLE_Toward_General_Act/figures/001_Figure_1.jpg]]
*Figure 1: Our method Active Perception Policy Learning (APPLE) aims to infer properties, such as object classes, of its environment based on limited per-step information. To do so, it jointly optimizes an action policy for information gathering and a prediction model for inference. Both the action policy and prediction models use a shared transformer-based backbone to process input sequences. Shown at the top are four benchmark tasks we use to evaluate APPLE.*

APPLE 的整体框架如 Figure 1 和 Figure 2 所示：

**Figure 1**: 方法概览与基准任务展示

**Figure 2**: 主动感知过程示意图

框架包含以下核心模块：

- **Vision Transformer (ViT) 编码器**：将触觉图像（如 32×32 像素）编码为嵌入向量
- **Transformer 序列处理器**：类似 Video-Vision-Transformer (ViViT) 的架构，处理时间序列上的嵌入与状态信息
- **预测头 (Prediction Head)**：从隐藏状态输出当前步的标签预测 $\hat{y}_t$
- **策略头 (Policy Head)**：从隐藏状态输出控制动作 $a_t$
- **Q 网络 (Critic)**：估计动作价值，用于策略优化（SAC/CrossQ）

## 核心模块与公式推导

### 5.1 主动感知目标函数

APPLE 将主动感知建模为 POMDP，其中隐藏状态分解为 $h_t$ 和真实标签 $y^*_t$，动作空间分解为控制动作 $a_t$ 和预测 $y_t$。目标函数为：

$$J(\pi) = \mathbb{E}_{p(\mathbf{h}, \mathbf{\check{y}}, \mathbf{o}, \mathbf{a}, \mathbf{y})} \left[ \sum_{t=0}^{\infty} \gamma^t \tilde{r}(h_t, \check{y}_t, a_t, y_t) \right]$$

### 5.2 奖励函数分解

总奖励由 RL 奖励和预测损失组成：

$$\tilde{r}(h_t, y^*_t, a_t, y_t) = r(h_t, a_t) - \ell(y^*_t, y_t)$$

其中 $r(h_t, a_t)$ 通常为动作幅度惩罚（如 $10^{-3} \|a_t\|^2$），$\ell(y^*_t, y_t)$ 为可微预测损失（如交叉熵或 MSE）。

### 5.3 梯度分解

目标函数的梯度自然分解为策略梯度与负监督损失梯度：

$$\frac{\partial}{\partial \theta} J(\pi_\theta) = \text{policy gradient} - \text{prediction loss gradient}$$

这一分解使得策略优化和预测学习可以同时进行，无需交替训练或任务特定的启发式。

### 5.4 Critic 损失函数 (APPLE-SAC)

Q 网络的贝尔曼残差损失为：

$$\mathcal{L}_{\mathrm{critic}} = \mathbb{E}_{\mathcal{D}} \left[ \frac{1}{2} \left( Q_\theta(o_{0:t}, a_t) - \left( r_t - \ell_{\pi_\theta}(\check{y}_t, o_{0:t}) + \gamma \mathbb{E}_{\pi_\theta}[Q_{\bar{\theta}}(o_{0:t+1}, a_{t+1})] \right) \right)^2 \right]$$

其中奖励动态重计算包含预测损失，使得 Q 网络能够学习到信息采集的价值。

### 5.5 任务特定损失函数

- **CircleSquare 二分类交叉熵损失**：$\ell(y_t^*, y_t) = -\sum_{c \in \{\mathrm{circle, square}\}} \delta(y_t^*, c) \log(p_c(y_t))$
- **TactileMNIST 10分类交叉熵损失**：$\ell(\dot{\boldsymbol{y}}_t, \boldsymbol{y}_t) = -\sum_{c=1}^{10} \delta(\boldsymbol{y}_t^*, c) \log(p_c(\boldsymbol{y}_t))$

## 实验与分析

### 6.1 主要实验结果

**Figure 4**: 各任务预测准确率/误差对比


![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_hU2gT2Ucua_APPLE_Toward_General_Act/figures/004_Figure_4.jpg]]
*Figure 4: Average and final prediction accuracies for our methods APPLE-SAC and APPLE-CrossQ, HAM Fleer et al. (2020), and APPLE-RND across various tasks. MHSB refers to the tactile classification task used in Fleer et al. (2020). All methods were trained with 5 seeds. Shaded areas represent one standard deviation. Metrics are computed on evaluation tasks with unseen objects, except for CircleSquare and the MHSB classification task, which have only two or four, respectively.*

| 基准任务 | 指标 | APPLE-SAC | APPLE-CrossQ | HAM | APPLE-RND |
|---------|------|-----------|-------------|-----|----------|
| MHSB (触觉分类) | 最终准确率 | ~100% (250K步) | ~100% (250K步) | 68% (1M步) | ~100% |
| CircleSquare (视觉分类) | 最终准确率 | 97% | 96% | 随机猜测 | 68% |
| TactileMNIST (触觉分类) | 最终准确率 | 87% | 89% | - | 74% |
| TactileMNISTVolume (体积回归) | 最终MAE (cm³) | 0.99 | 1.05 | - | 1.07 |
| Toolbox (触觉定位) | 位置/角度误差 | 较低精度 | 1.9cm, 13° | - | 较低精度 |
| CIFAR10 (视觉分类) | 最终准确率 | 76% | 73% | - | 67% |

### 6.2 关键发现

1. **MHSB 任务**：APPLE 方法约 250K 步即接近 100% 准确率，而 HAM 在 1M 步后仅达 68%。HAM 在 5M 步后最终收敛到良好性能，但 APPLE 的收敛速度显著更快。

2. **CircleSquare 任务**：APPLE-SAC 和 APPLE-CrossQ 分别达到 97% 和 96% 的最终预测准确率，而 HAM 无法超越随机猜测。APPLE-RND 仅达 68%，表明主动探索带来的增益显著。

3. **TactileMNIST 分类**：APPLE-SAC 和 APPLE-CrossQ 分别达到 87% 和 89% 的最终准确率，而 APPLE-RND 停滞在 74%。Figure 5 显示主动智能体比随机智能体更快地收集信息且对类别判断更确定。


![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_hU2gT2Ucua_APPLE_Toward_General_Act/figures/005_Figure_5.jpg]]
*Figure 5: Exploration efficiency of final policies on the TactileMNIST task. Shown are the predicted probability of the correct label (top) and accuracy (bottom) after N glances.*

**Figure 5**: TactileMNIST 上正确标签概率与准确率随步数变化

4. **Toolbox 定位**：APPLE-CrossQ 达到平均 1.9cm 和 13° 的最终精度，而 APPLE-SAC 和 APPLE-RND 停滞在较低精度。Figure 12 展示了 APPLE-CrossQ 学到的圆形搜索模式。

**Figure 6**: Toolbox 任务结果

**Figure 12**: Toolbox 上学到的探索策略可视化

5. **CIFAR10 视觉分类**：APPLE-SAC 达到 76% 最终准确率，APPLE-CrossQ 达 73%，APPLE-RND 为 67%。

**Figure 21**: CIFAR10 任务结果

### 6.3 消融研究

**Figure 15**: Transformer vs LSTM 消融——Transformer 模型在收敛速度上优于 LSTM 模型。

**Figure 16**: 纯 RL 消融——将预测损失作为普通 RL 奖励的变体效率低下且不稳定，APPLE-SAC-PURE-RL 仅短暂达到 80% 准确率。

**Figure 17**: 启发式网格搜索消融——网格搜索策略停滞在 73% 最终准确率，远低于 APPLE 变体。

**Figure 18**: 稀疏奖励实验——在仅最后一步计分的 CircleSquare 上，APPLE 变体仍能学习。

**Figure 19**: CircleSquareHideAndSeek 实验——使用标签/损失的 APPLE-CrossQ 显著优于纯 RL 变体。

### 6.4 公平性说明

- 所有方法均使用 5 个随机种子训练，报告平均值和标准差
- 超参数通过 HEBO (Cowen-Rivers et al., 2022) 贝叶斯优化器在 CircleSquare 和 TactileMNIST 上统一调优
- HAM 和 PPO 基线也经过广泛超参数搜索
- APPLE-CrossQ 的视觉编码器超参数直接应用于非视觉任务时未观察到性能下降

**Table 1**: 超参数设置


![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_hU2gT2Ucua_APPLE_Toward_General_Act/figures/038_Table_1.jpg]]
*Table 1: Hyperparameters determined by the HEBO Cowen-Rivers et al. (2022) Bayesian optimizer for APPLE-SAC and APPLE-CrossQ. The no vision-encoder configuration was trained on the CircleSquare environment, while the vision-encoder configuration was trained on the TactileMNIST environment. Hyperparameters with Rel. are relative to the total number of steps throughout the training.*

### 6.5 局限性

- 依赖大量训练数据，触觉感知任务需高达 5M 步，样本效率较低
- 当前实验仅使用单触觉传感器，多指手和多模态感知的可扩展性尚未验证
- 未探索物体姿态估计、形状重建或材料属性推断等更实际的任务
- Transformer 架构与 RL 策略优化的结合导致计算成本较高（单次 5M 步运行约 40-50 小时）

### 补充图表

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_hU2gT2Ucua_APPLE_Toward_General_Act/figures/002_Figure_2.jpg]]
*Figure 2: Active perception process in the APPLE framework. In this task, the agent’s goal is to classify the digit using touch alone. At each step, it receives a tactile reading and state information (e.g., sensor position). A Vision Transformer encodes the tactile input, which is concatenated with state data and processed as a sequence over time by a transformer. At every step, the model outputs a label prediction $y _ { t }$ , , evaluated against the ground truth $\stackrel { * } { y }$ via a loss function ℓ, and an action $a _ { t }$ that controls the sensor’s next movement.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_hU2gT2Ucua_APPLE_Toward_General_Act/figures/003_Figure_3.jpg]]


## 方法谱系与知识库定位

APPLE 属于主动感知与强化学习交叉领域的方法。其核心思想源于 Bajcsy (1988) 的主动感知概念，并受到 Mnih et al. (2014) 的 Recurrent Models of Visual Attention (RAM) 和 Fleer et al. (2020) 的 Haptic Attention Model (HAM) 的启发。

与现有方法的关键区别：
- **相比 HAM**：APPLE 使用离策略 RL 算法（SAC/CrossQ）而非 REINFORCE，使用 Transformer 而非 LSTM，并利用可微损失函数实现联合优化
- **相比 Li et al. (2023) 的 IRRL**：APPLE 将预测损失直接作为奖励的一部分，而非作为内部奖励
- **相比好奇心驱动方法**：APPLE 的探索发生在每个 episode 内部，用于学习 POMDP 的隐藏状态，而非作为策略学习的替代

**开放问题**：
- 预训练 Transformer 模型能否提升 APPLE 的样本效率？
- APPLE 如何扩展到多指机器人手和多模态感知（如视觉+触觉）？
- APPLE 在物体姿态估计、形状重建或材料属性推断等任务上的表现如何？
- 将 APPLE 与好奇心驱动的内在奖励方法（如 ICM 或 RND）结合是否能加速学习？
- APPLE 能否通过域随机化等技术实现从仿真到真实的迁移？

## 原文 PDF

![[paperPDFs/ICLR_2026/APPLE_Toward_General_Active_Perception_via_Reinforcement_Learning.pdf]]

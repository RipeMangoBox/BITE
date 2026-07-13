---
title: "Structured Flow Autoencoders: Learning Structured Probabilistic Representations with Flow Matching"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Structured_Flow_Autoencoders_Learning_Structured_Probabilistic_Representations_with_Flow_Matching.pdf
project_link: null
code_link: null
openreview_forum_id: KYdfvF2SZN
aliases:
- SFAS
- SFALSPRFM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将隐变量显式引入流匹配，利用边际向量场可分解为条件向量场后验期望的性质（定理3.1），提出结构化条件流匹配(SCFM)目标，通过匹配条件向量场的期望而非直接匹配边际分布，使模型在保持生成质量的同时学习结构化隐变量。"
primary_logic: "定理3.1证明边际向量场可由条件向量场在后验分布下的期望完全生成，因此通过优化条件向量场和近似后验，可以在不牺牲边际密度估计精度的前提下，为任意图模型结构提供流匹配似然。"
claims:
- "SCFM目标在Pinwheel数据集上的W1距离与标准FM相当（0.024 vs 0.025），远优于VAE系列"
- "在MNIST上，SFA生成样本的多样性（Vendi: 1675.9）远高于LatentFM（380.5），同时SSIM接近（0.694 vs 0.709）"
- "LDS-SFA在摆锤数据集上将隐变量RMSE降低了5倍以上（1.526 vs 8.090），远超结构化VAE"
- "定理3.1从理论上保证边际向量场的后验期望形式，为SCFM提供数学基础"
---

# Structured Flow Autoencoders: Learning Structured Probabilistic Representations with Flow Matching

> [!tip] 核心洞察
> 定理3.1证明边际向量场可由条件向量场在后验分布下的期望完全生成，因此通过优化条件向量场和近似后验，可以在不牺牲边际密度估计精度的前提下，为任意图模型结构提供流匹配似然。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 结构化流自编码器：利用流匹配学习结构化概率表示 |
| 英文题名 | Structured Flow Autoencoders: Learning Structured Probabilistic Representations with Flow Matching |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=KYdfvF2SZN) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Structured Flow Autoencoders (SFA) |
| Dataset | Pinwheel, MNIST, MNIST (clustering) |

> [!tip] 效果简介
> - Pinwheel 上，W1 distance (↓) 为 0.024 (SFA)，对比 0.025 (FM)，变化 -0.001。
> - MNIST 上，SSIM (↑) 为 0.694 (SFA)，对比 0.709 (LatentFM)，变化 -0.015。
> - MNIST 上，Vendi (↑, diversity) 为 1675.9 (SFA)，对比 380.5 (LatentFM)，变化 +1295.4。

## 概要

深度生成模型长期面临一个核心矛盾：流匹配（Flow Matching, FM）等现代生成模型能够实现高保真度的样本生成，却无法捕获数据中隐含的结构化表示；而变分自编码器（VAE）虽能学习可解释的隐变量结构，其生成质量却显著落后。这一瓶颈的根源在于，现有方法无法在保持精确边际密度估计的同时，显式建模结构化隐变量。

本文提出**结构化流自编码器（Structured Flow Autoencoders, SFA）**，通过将条件连续归一化流（Conditional CNF）引入概率图模型框架，统一了高保真生成与结构化表示学习。方法的核心是一个新的训练目标——结构化条件流匹配（Structured Conditional Flow Matching, SCFM），其理论基础由定理3.1保证：边际向量场可分解为条件向量场在后验分布下的期望，因此通过匹配条件向量场的期望而非直接匹配边际分布，SFA能够在学习结构化隐变量的同时不牺牲生成质量。

实验结果表明，SFA在密度估计上达到与标准FM相当的水平（Pinwheel数据集上W1距离分别为0.024与0.025），同时显著提升了隐空间的结构化程度——在MNIST上生成多样性指标Vendi从LatentFM的380.5提升至1675.9，在摆锤动态系统中隐变量RMSE从GLD-SVAE的8.090降至1.526。SFA支持多种图模型结构（连续隐变量、有限混合模型、线性动态系统），且无需像β-VAE那样通过超参数平衡重建与KL正则化。

**方法定位**：SFA处于流匹配与结构化概率模型的交叉地带。与纯流匹配（FM）相比，SFA引入了可学习的隐变量后验；与VAE系列（VAE、VampVAE、Mixture-SVAE）相比，SFA将高斯解码器替换为条件CNF，将ELBO目标替换为SCFM目标，从根本上避免了VAE中重建质量与隐变量解耦之间的固有权衡。

深度生成模型的核心目标是学习复杂高维数据（如图像、单细胞转录组、动态系统轨迹）的底层分布。当前该领域存在两条主要技术路线，各自拥有显著优势，却面临截然不同的瓶颈。

**流匹配模型的生成保真度与结构缺失。** 以连续归一化流（Continuous Normalizing Flow, CNF）和流匹配（Flow Matching, FM）为代表的现代生成模型，通过学习从简单先验到数据分布的向量场变换，在图像生成、密度估计等任务上取得了极高的样本保真度。然而，这类模型将生成过程建模为从噪声到数据的单一确定性映射，缺乏对数据内在结构的显式表征——它们无法回答“这个样本属于哪个子群”、“哪些潜在因子驱动了观测变化”等结构化问题。换言之，FM 擅长“画得像”，却不理解“为什么这样画”。

**变分自编码器的结构化优势与生成质量瓶颈。** 变分自编码器（VAE）及其结构化扩展（如 Mixture-SVAE、GLD-SVAE）天然具备学习隐变量结构的能力。通过在隐空间引入图模型（如连续隐变量、有限混合模型、线性动态系统），VAE 能够将数据分解为可解释的潜在因子。然而，这一结构化能力以牺牲生成质量为代价：VAE 的参数化解码器（通常为对角高斯分布）表达力有限，导致生成样本模糊、缺乏细节；同时，ELBO 目标中重建项与 KL 正则项之间的固有张力，迫使模型在“忠实重建”与“规整隐空间”之间进行艰难的权衡（如 β-VAE 需要手动调节超参数）。

**核心缺口：高保真生成与结构化隐变量学习的统一。** 上述两条路线长期处于割裂状态——流匹配模型无法捕获隐结构，VAE 则无法实现高质量生成。根本原因在于，现有流匹配框架将生成过程定义为纯边际分布变换，隐变量在理论推导中被边缘化，缺乏将其显式纳入训练目标的数学工具。因此，领域亟需一种既能保持流匹配级生成质量，又能像结构化 VAE 一样学习可解释隐变量的统一框架。

本文提出的**结构化流自编码器（Structured Flow Autoencoders, SFA）**正是针对这一缺口。其核心洞察源于一个关键的数学性质：**边际向量场可以被分解为条件向量场在后验分布下的期望**（定理 3.1）：

$$v_t(\pmb{x}) = \int v_t(\pmb{x}|z) \frac{p_t(\pmb{x}|z) p(z)}{\int p_t(\pmb{x}|z') p(z') dz'} dz = \mathbb{E}_{p_t(z|\pmb{x})}[v_t(\pmb{x}|z)]$$

这一分解意味着，如果我们能够同时学习条件向量场 $v_t(\pmb{x}|z)$ 和近似后验 $q_t(z|\pmb{x})$，就可以在不牺牲边际密度估计精度的前提下，将任意图模型结构注入流匹配框架。基于此，SFA 用条件 CNF 替代 VAE 的高斯解码器作为似然模型，用结构化条件流匹配（SCFM）目标替代 ELBO，从而消除了重建-KL 权衡，使隐变量天然地捕获有意义的结构信息，同时保持与纯 FM 相当的生成质量。

## 核心方法与创新机理

### 问题瓶颈：流匹配的“盲生成”与VAE的“低保真”

当前深度生成模型面临一个两难困境。流匹配（Flow Matching, FM）模型虽能实现高保真生成，但其隐空间缺乏可解释的结构——模型仅学习从噪声到数据的映射，无法显式捕获数据背后的类别、连续因子或动态演化等结构化信息。反观变分自编码器（VAE）及其结构化变体，虽能通过图模型对隐变量施加结构先验，但受限于高斯解码器等简单似然模型，生成质量远不及流匹配方法。这一瓶颈的核心在于：**缺乏一种既能保持流匹配级别生成保真度，又能显式建模结构化隐变量的统一框架**。

### 核心洞察：边际向量场的后验期望分解

SFA的关键理论突破来自**定理3.1**：若条件向量场 $v_t(\mathbf{x}|z)$ 生成条件概率路径 $\{p_t(\mathbf{x}|z)\}$，则边际向量场 $v_t(\mathbf{x})$ 可完全由条件向量场在后验分布下的期望表示：

$$v_t(\mathbf{x}) = \mathbb{E}_{p_t(z|\mathbf{x})}[v_t(\mathbf{x}|z)]$$

这一等式揭示了流匹配框架中隐变量的天然入口：**只需匹配条件向量场的后验期望与预定义的参考向量场，即可在不牺牲边际密度估计精度的前提下，为任意图模型结构提供流匹配似然**。这相当于将原本“盲”的流匹配过程，解耦为条件生成模型与隐结构成分的联合学习问题。

### 关键改造槽位：从VAE到SFA的四项结构性替换

相较于以VAE为代表的结构化隐变量模型，SFA在四个核心组件上进行了根本性替换：

| 改造槽位 | 基线方案（VAE系列） | SFA方案 | 机制与收益 |
|----------|---------------------|---------|-----------|
| **似然模型** | 高斯分布等参数化解码器 | 条件连续归一化流（Conditional CNF, Eq. 7） | 将流匹配的高保真生成能力注入条件似然，从根本上解决VAE生成模糊的问题 |
| **训练目标** | ELBO（变分下界），需平衡重建与KL散度 | 结构化条件流匹配（SCFM, Eq. 6）：$\mathcal{R}(\theta, q) = \mathbb{E}_{x_1, x_t, t}\left\| \mathbb{E}_{q_t(z_t|x_t)}[v_t(x_t|z_t;\theta)] - u_t(x_t|x_1) \right\|^2$ | 通过匹配条件向量场的期望而非直接匹配边际分布，天然规避了VAE中重建-KL权衡的超参数调试问题 |
| **后验近似族** | 对角高斯等简单参数族 | 灵活选择：高斯族、条件CNF、Gumbel-Softmax等，支持图模型结构 | 可根据隐变量结构（连续、离散混合、动态系统）适配后验形式，无需强制共轭假设 |
| **隐变量集成方式** | 通过KL散度正则化注入先验信息 | 通过SCFM目标中的期望匹配自然引入隐变量 | 隐变量不再作为“正则化项”存在，而是通过解混（de-mixing）机制主动捕获数据结构，避免了β-VAE式的超参数敏感问题 |

### 理论保证与实证验证

**定理3.1**为上述改造提供了严格的数学基础（证明见附录A.1），确保SCFM目标在理论上等价于学习正确的边际概率路径。实证层面，Table 1显示SFA在Pinwheel数据集上的W1距离（0.024）与标准FM（0.025）几乎持平，远优于VAE系列，直接验证了“不牺牲边际密度估计”的理论承诺。同时，Figure 1中SFA的生成样本按后验隐变量着色后呈现出与真实类别一致的聚类结构，证明隐变量确实捕获了有意义的语义因子——这是纯FM模型无法实现的。

### 与LatentFM的本质区别

需特别区分SFA与在隐空间使用流匹配的LatentFM。LatentFM仅在隐空间建模，其生成过程为 $z \sim p(z), x \sim p(x|z)$，但训练时并未显式利用条件结构。SFA的核心差异在于SCFM目标中的**期望匹配机制**：通过在后验 $q_t(z_t|x_t)$ 下对条件向量场求期望，迫使模型在每一时刻 $t$ 都保持条件结构与边际分布的一致性，从而实现生成质量与结构表征的联合优化。Table 2中SFA的生成多样性（Vendi: 1675.9）远超LatentFM（380.5），而SSIM仅微降（0.694 vs 0.709），正是这一机制的直接体现。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_KYdfvF2SZN/figures/013_Figure_12.jpg]]
*Figure 12: (a) SFA framework*

### 核心问题与设计动机

现有深度生成模型面临一个根本性的权衡：流匹配（Flow Matching, FM）等连续归一化流（CNF）模型能够实现高保真度的生成，但缺乏对数据潜在结构的显式建模能力；变分自编码器（VAE）虽然可以学习结构化的隐变量表示，但其生成质量受限于高斯似然假设和ELBO优化中的重建-KL权衡。**结构化流自编码器（Structured Flow Autoencoders, SFA）** 旨在打破这一僵局——将隐变量显式引入流匹配框架，在保持边际密度估计精度的同时，学习可解释的结构化隐变量表示。

### 理论基石：边际向量场的后验期望分解

SFA的核心理论保证来自**定理3.1**：给定生成条件概率路径 $\{p_t(\mathbf{x}|\mathbf{z})\}$ 的条件向量场 $v_t(\mathbf{x}|\mathbf{z})$，边际向量场 $v_t(\mathbf{x})$ 可通过条件向量场在后验分布下的期望精确表示：

$$v_t(\mathbf{x}) = \int v_t(\mathbf{x}|\mathbf{z}) \frac{p_t(\mathbf{x}|\mathbf{z}) p(\mathbf{z})}{\int p_t(\mathbf{x}|\mathbf{z}') p(\mathbf{z}') d\mathbf{z}'} d\mathbf{z} = \mathbb{E}_{p_t(\mathbf{z}|\mathbf{x})}[v_t(\mathbf{x}|\mathbf{z})]$$

这一分解意味着：**只要能够学习条件向量场 $v_t(\mathbf{x}|\mathbf{z};\theta)$ 和近似后验 $q_t(\mathbf{z}|\mathbf{x})$，就可以在不牺牲边际密度估计质量的前提下，为任意概率图模型结构提供流匹配似然**。这正是SFA区别于纯流匹配模型和传统VAE的根本所在。

### SCFM训练目标

基于上述定理，SFA提出**结构化条件流匹配（Structured Conditional Flow Matching, SCFM）** 目标函数：

$$\mathcal{R}(\theta, q) = \mathbb{E}_{\substack{\mathbf{x}_1\sim p_{\text{data}},\; \mathbf{x}_t\sim p_t(\mathbf{x}|\mathbf{x}_1),\\ t\sim \mathcal{U}[0,1]}} \left\| \mathbb{E}_{q_t(\mathbf{z}_t|\mathbf{x}_t)}[v_t(\mathbf{x}_t|\mathbf{z}_t;\theta)] - u_t(\mathbf{x}_t|\mathbf{x}_1) \right\|^2$$

该目标的核心机制是“解混”（de-mixing）：将观测信号分解为两部分——(1) 由条件CNF定义的数据生成模型 $p(\mathbf{x}|\mathbf{z})$，以及 (2) 由近似后验 $q(\mathbf{z}|\mathbf{x})$ 捕获的隐结构。与VAE的ELBO不同，SCFM不需要通过KL散度超参数（如β-VAE中的β）来平衡重建质量与隐变量正则化——隐变量天然地在匹配条件向量场期望的过程中被约束，从而消除了重建-KL权衡。

### Pipeline模块架构

SFA的整体pipeline由以下核心模块构成，形成“编码-生成”统一的流匹配框架：

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| **条件CNF似然** | 给定隐变量 $\mathbf{z}$，通过ODE $\frac{d}{dt}\phi_t(\mathbf{x}) = v_t(\phi_t(\mathbf{x})|\mathbf{z};\theta)$ 生成观测数据 | 替代VAE的高斯解码器，提供灵活的分布建模能力 |
| **后验近似器** | 近似后验 $q_t(\mathbf{z}_t|\mathbf{x}_t)$，可选高斯族、条件CNF或Gumbel-Softmax等 | 根据图模型结构灵活选择；简单参数族在训练稳定性和计算开销上优于条件CNF |
| **SCFM训练目标** | 联合优化条件向量场和近似后验 | 通过期望匹配而非KL散度驱动学习，无需重建-KL权衡 |
| **隐变量先验（可选）** | 训练后学习 $p(\mathbf{z})$，用于无条件生成 | 从后验样本中拟合，支持 $\mathbf{z}_1 \sim p_1(\mathbf{z}_1), \mathbf{x}_1 \sim p_1(\mathbf{x}_1|\mathbf{z}_1)$ 的采样 |

### 输入输出流

**训练阶段**：输入为观测数据 $\mathbf{x}_1 \sim p_{\text{data}}$，通过线性插值路径 $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$（其中 $\mathbf{x}_0 \sim p_0$ 为基分布）构建条件概率路径。SCFM目标在每一时间步 $t$ 上，将近似后验 $q_t(\mathbf{z}_t|\mathbf{x}_t)$ 下的条件向量场期望与预定义的参考向量场 $u_t(\mathbf{x}_t|\mathbf{x}_1)$ 对齐，同时反向传播梯度以更新条件CNF参数 $\theta$ 和后验参数。

**推理/生成阶段**：从先验采样 $\mathbf{z}_1 \sim p_1(\mathbf{z}_1)$，通过条件CNF的ODE求解器生成 $\mathbf{x}_1 \sim p_1(\mathbf{x}_1|\mathbf{z}_1)$。**隐变量编码**则通过近似后验 $\tilde{\mathbf{z}}_1 \sim q_1(\mathbf{z}_1|\mathbf{x}_1)$ 实现，无需额外的编码器网络。

### 支持的图模型结构

SFA框架具有图模型结构无关性，可适配多种隐变量结构（Figure 2）：

- **连续隐变量模型**：$\mathbf{z} \sim p(\mathbf{z}), \mathbf{x}|\mathbf{z} \sim p(\mathbf{x}|\mathbf{z})$，适用于无监督表示学习
- **隐有限混合模型**：引入离散类别变量 $\xi$ 和连续隐变量 $\mathbf{z}$ 的层次结构，SCFM目标中对 $\xi$ 和 $\mathbf{z}$ 求联合期望（Eq. 8）
- **隐线性动态系统**：处理序列数据，SCFM目标中对序列索引 $s \in [S]$ 求和以捕获时序依赖（Eq. 9）

**关键设计选择**：当隐变量维度远小于观测维度时，后验模型可以比似然模型更轻量；在多组件联合学习时，简单参数后验族（如高斯族）相比条件CNF后验具有更好的训练稳定性，这在实验中得到了验证。

### 3.1 核心理论：边际向量场的后验期望分解

SFA 的理论基石是定理 3.1，它揭示了流匹配中边际向量场与条件向量场之间的本质关系。给定一组条件向量场 $v_t(\pmb{x}|z)$，它们各自生成条件概率路径 $p_t(\pmb{x}|z)$，则边际概率路径 $p_t(\pmb{x}) = \int p_t(\pmb{x}|z)p(z)dz$ 可由如下边际向量场生成：

$$v_t(\pmb{x}) = \int v_t(\pmb{x}|z) \frac{p_t(\pmb{x}|z) p(z)}{\int p_t(\pmb{x}|z') p(z') dz'} dz = \mathbb{E}_{p_t(z|\pmb{x})}[v_t(\pmb{x}|z)]$$

**变量含义**：
- $v_t(\pmb{x})$：边际向量场，驱动观测变量 $\pmb{x}$ 的边际概率路径
- $v_t(\pmb{x}|z)$：条件向量场，在给定隐变量 $z$ 的条件下驱动 $\pmb{x}$ 的条件概率路径
- $p_t(z|\pmb{x})$：时刻 $t$ 的后验分布，即给定当前观测 $\pmb{x}$ 时隐变量 $z$ 的概率分布
- $p(z)$：隐变量的先验分布

**关键洞察**：该定理表明，边际向量场完全由条件向量场在后验分布下的期望所决定。这意味着我们无需直接建模复杂的边际分布，只需学习条件向量场和一个近似的后验分布，即可间接生成正确的边际概率路径。这为在流匹配框架中显式引入结构化隐变量提供了严格的数学保证。

### 3.2 结构化条件流匹配目标（SCFM）

基于定理 3.1，SFA 的核心训练目标——结构化条件流匹配（Structured Conditional Flow Matching, SCFM）被定义为：

$$\mathcal{R}(\theta, q) = \mathbb{E}_{\substack{\pmb{x}_1\sim p_{\text{data}},\; \pmb{x}_t\sim p_t(\pmb{x}|\pmb{x}_1),\\ t\sim \mathcal{U}[0,1]}} \left\| \mathbb{E}_{q_t(\pmb{z}_t|\pmb{x}_t)}[v_t(\pmb{x}_t|\pmb{z}_t;\theta)] - u_t(\pmb{x}_t|\pmb{x}_1) \right\|^2$$

**变量含义**：
- $\theta$：条件向量场 $v_t$ 的可学习参数
- $q$：近似后验族 $q_t(\pmb{z}_t|\pmb{x}_t)$，用于逼近真实后验 $p_t(z|\pmb{x})$
- $\pmb{x}_1$：从真实数据分布 $p_{\text{data}}$ 中采样的观测样本
- $\pmb{x}_t$：沿条件概率路径 $p_t(\pmb{x}|\pmb{x}_1)$ 在时刻 $t$ 的中间状态
- $u_t(\pmb{x}_t|\pmb{x}_1)$：预定义的参考向量场（如线性插值路径对应的向量场）
- $\mathbb{E}_{q_t(\pmb{z}_t|\pmb{x}_t)}[v_t(\pmb{x}_t|\pmb{z}_t;\theta)]$：对近似后验求期望后的条件向量场

**机制解释**：SCFM 本质上是一个“解混”（de-mixing）问题——它将观测信号分解为两部分：(1) 由条件 CNF 建模的数据生成机制 $p(\pmb{x}|z)$；(2) 由近似后验捕获的隐结构成分。通过匹配条件向量场的期望与参考向量场，SCFM 联合优化似然模型和近似后验，而无需像 VAE 那样在重建损失与 KL 正则项之间进行超参数权衡。

### 3.3 条件连续归一化流（Conditional CNF）

SFA 使用条件连续归一化流作为似然模型 $p(\pmb{x}|z)$，其定义为：

$$\frac{d}{dt}\phi_t(\pmb{x}) = v_t(\phi_t(\pmb{x})|z;\theta), \quad \phi_0(\pmb{x}) = \pmb{x}_0, \quad \pmb{x}_0 \sim p_0(\pmb{x})$$

**变量含义**：
- $\phi_t(\pmb{x})$：从初始状态 $\pmb{x}_0$ 到时刻 $t$ 状态的流映射
- $v_t(\cdot|z;\theta)$：以隐变量 $z$ 为条件的向量场，参数化为神经网络
- $p_0(\pmb{x})$：基础分布（通常为标准高斯）

该模块将隐变量 $z$ 作为条件注入向量场，使得同一个流模型可以根据不同的 $z$ 生成不同模式的观测数据，从而实现结构化生成。

### 3.4 后验近似族的设计

SFA 对后验近似族 $Q$ 的选择保持灵活，支持多种参数化形式：

- **参数族**（如对角高斯）：训练稳定、计算开销小，在隐变量维度较低时已足够
- **条件 CNF**：表达力更强，但训练稳定性较差，适用于需要复杂后验建模的场景
- **Gumbel-Softmax**（混合模型）：用于离散隐变量（如类别标签 $\xi$）的近似后验

后验近似族的选择遵循一个实用原则：当隐变量维度远小于观测维度时，较小的后验模型即可满足需求；当需要同时学习多个组件时，简单的参数族通常比条件 CNF 更稳定。

### 3.5 扩展：混合隐变量与动态系统

SCFM 框架可自然扩展到更复杂的图模型结构。

**隐有限混合模型**（Latent Finite Mixture）：引入离散隐变量 $\xi$（类别标签）和连续隐变量 $z$，SCFM 目标扩展为对两者的联合期望：

$$\operatorname*{inf}_{\boldsymbol{q}\in Q,\boldsymbol{\theta}\in\Theta} \mathbb{E}_{\mathbf{x}_1\sim p_{\text{data}}} \left\| \mathbb{E}_{\boldsymbol{q}_t(\xi_t|\mathbf{x}_t) \boldsymbol{q}_t(\boldsymbol{z}_t|\mathbf{x}_t, \xi_t)} [\boldsymbol{v}_t(\mathbf{x}_t|\boldsymbol{z}_t;\boldsymbol{\theta})] - u_t(\mathbf{x}_t|\mathbf{x}_1) \right\|^2$$

**隐线性动态系统**（Latent LDS）：对于序列数据，SCFM 目标在序列索引 $s \in [S]$ 上求和，以捕获时序依赖关系。具体形式见 Eq. 9，其核心仍是定理 3.1 在序列图模型上的直接推广。

## 实验与关键发现

### 核心实验设计逻辑

实验围绕一个中心问题展开：**SFA能否在保持流匹配级别生成保真度的同时，学到有结构的隐变量表示？** 为此，作者设计了三个层次的验证：(1) 在玩具数据上验证密度估计能力是否与标准流匹配持平；(2) 在图像数据上检验隐变量的结构捕获能力与生成多样性；(3) 在科学数据（单细胞转录组、动力系统）上验证框架的跨领域适用性。

---

### 密度估计：SFA不牺牲边际质量

**Table 1** 给出了Pinwheel数据集上的W1距离（Earth Mover's Distance）对比。核心发现是：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_KYdfvF2SZN/figures/001_Table_1.jpg]]
*Table 1: Comparing generated samples to data samples with W1 metric (Earth Mover’s Distance). W1 metric is evaluated with samples from marginal data distribution p ( $\pmb { x } _ { 1 }$ ) and that generated from $\tilde { p } _ { 1 } ( { \pmb$ x $} _ { 1 }$ ) = $\begin{array} { r } { \int p _ { 1 } \big ( { \pmb x } _ { 1 } | { \pmb z } _ { 1 } \big ) q _ { 1 } \big ( { \pmb z } _ { 1 } \big ) d { \pmb z } _ { 1 } } \end{array}$ . SFA and FM achieve comparable performance on marginal density estimations

- SFA的W1距离为0.024，与标准FM的0.025几乎一致，二者均显著优于VAE系列（VAE: 0.056, VampVAE: 0.055, Mixture-SVAE: 0.049）。
- 这表明SCFM目标在引入隐变量的同时，**没有损害边际密度估计精度**——这正是定理3.1的理论保证在实践中的体现：边际向量场可由条件向量场的后验期望完全生成，因此优化条件流和近似后验不会牺牲边际似然。

**Figure 1** 的定性结果进一步佐证：SFA生成的Pinwheel样本在簇结构和分布形态上与FM及真实数据高度一致，而VAE系列存在明显的模糊或模式缺失。

---

### 图像生成：多样性大幅领先，重建质量接近

**Table 2** 汇总了MNIST数据集上的多维指标对比。关键结论如下：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_KYdfvF2SZN/figures/015_Table_2.jpg]]
*Table 2: Comparison of metrics for MNIST dataset between VAE, latent FM and SFA. Evaluated on a held-out set of size 1000. The OOD dataset consists of first 10 classes of letters and the first 10 classes of digits in EMNIST. The clustering is done in the latent space via k-means with k given*

| 指标 | SFA | LatentFM | VAE | 解读 |
|------|-----|----------|-----|------|
| SSIM (↑) | 0.694 | 0.709 | 0.729 | SFA重建质量略低于LatentFM和VAE，但差距很小 |
| Vendi (↑, 多样性) | **1675.9** | 380.5 | 1045.3 | SFA的生成多样性远超LatentFM（4.4倍）和VAE |
| NMI (聚类, ↑) | **0.490** | 0.394 | 0.382 | 隐空间聚类质量显著优于对比方法 |

**瓶颈分析**：LatentFM虽在隐空间使用流匹配，但缺乏对隐变量的显式建模，导致后验崩塌（posterior collapse）——隐变量未能捕获有意义的结构，生成多样性极低（Vendi仅380.5）。SFA通过SCFM目标中的后验期望匹配，迫使隐变量编码数据中的变化因素，从而在保持重建质量的同时大幅提升多样性。

**Figure 3b** 提供了直观证据：在MNIST上采样得到的轨迹 $\{z_t\}$ 和 $\{x_t\}$ 经1D PCA投影后，不同数字的条件路径在 $t \in [0,1]$ 上不发生交叉，证实了学到的后验编码了低维结构信息。**Figure 6** 的t-SNE可视化进一步显示，SFA的隐空间按数字类别形成了清晰的分离，而LatentFM的隐空间几乎无结构。

---

### 混合隐变量与子空间聚类

**Table 3** 展示了引入离散隐变量（类别标签 $\xi$）后的子空间聚类结果。Mixture-SFA的NMI达到0.489，而Mixture-SVAE仅为0.161——差距超过3倍。**Figure 4** 定性对比揭示原因：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_KYdfvF2SZN/figures/016_Table_3.jpg]]
*Table 3: Subspace clustering on MNIST with latent mixtures models Mixture-SVAE and Mixture-SFA. Evaluated on a held-out set of size 1000*

- Mixture-SVAE的后验预测样本模糊，类别分配概率 $\xi_i$ 混乱，隐空间 $z$ 的t-SNE投影中不同数字严重重叠。
- Mixture-SFA的生成样本清晰，类别分配准确，隐空间按数字类别形成紧凑的簇。

**因果机制**：Mixture-SVAE依赖ELBO中的KL项来正则化隐变量，但KL项与重建项的权衡常导致隐变量被忽略。SCFM通过直接匹配条件向量场的期望，无需KL权衡，使离散和连续隐变量都能有效捕获数据结构。

---

### 科学数据验证

**Table 4a**（Kang HVG scRNA-seq，观测维度5000）表明：

- SFA的聚类NMI（0.633）略优于LatentFM（0.617），但生成多样性Vendi（737.7 vs 5.801）领先两个数量级。
- **Figure 5** 的t-SNE可视化显示，SFA的隐空间呈现更清晰的细胞类型分离结构。

**Table 4b**（Pendulum动力系统）是结构化隐变量建模的强证据：

- LDS-SFA的隐变量RMSE为1.526，GLD-SVAE为8.090——**误差降低5倍以上**。
- 观测空间的RMSE_x同样大幅领先（1.630 vs 10.906）。
- **Figure 10** 的轨迹对比显示，LDS-SFA生成的摆锤轨迹紧贴真实值，而GLD-SVAE的轨迹迅速偏离。

**关键洞察**：动力系统场景中，隐变量遵循线性动态系统（LDS）的图模型结构。SCFM通过Eq. 9中的序列求和项 $\sum_{s \in [S]}$ 显式建模时序依赖，而VAE系列缺乏这种结构化归纳偏置。

---

### 消融实验与设计选择

**随机隐变量 vs 确定性编码器**：Table 2中SFA-det（确定性编码器）的SSIM达到0.732，高于随机SFA的0.694，但Vendi多样性从1675.9骤降。这验证了随机隐变量对生成多样性的关键作用——确定性编码器退化为类似标准自编码器的行为，牺牲了隐空间的结构化表征能力。

**后验近似族的选择**：实验发现，当隐变量维度远小于观测维度时，简单的参数族（如高斯分布）比条件CNF后验更受青睐。原因有二：(1) 条件CNF后验训练不稳定，尤其在多组件联合学习时；(2) 低维隐变量场景下，简单后验已足够捕获结构，额外的复杂度带来的收益有限。这一发现直接回应了方法设计中的权衡：**"sufficiently expressive while not so complex as to destabilize the training"**。

**无需重建-KL权衡**：与VAE系列不同，SFA无需通过 $\beta$ 超参数平衡重建质量与KL正则化。SCFM目标天然将隐变量学习与边际密度估计解耦——隐变量通过条件向量场的期望匹配自然涌现，不依赖显式的KL惩罚。这一特性在Pinwheel（Table 1）和Pendulum（Table 4b）上得到了跨任务验证。

---

### 失败模式与局限

1. **高维观测下的似然评估**：Table 4a中scRNA-seq数据的对数似然无法通过伴随ODE直接计算（观测维度5000），限制了CNF似然的直接评估。这是条件CNF在高维场景下的已知瓶颈。

2. **后验族选择的经验性**：当隐变量维度远小于观测维度时，如何系统选择后验族仍无理论指导，目前依赖经验试探。

3. **架构兼容性**：当解码器采用UNet等跳跃连接架构时，隐变量可能被绕过（信息经跳跃连接直接传递），相应的架构设计要求尚不明确。

4. **训练稳定性**：条件CNF作为后验时训练不稳定，尤其在多组件联合学习场景下。简单参数族虽稳定，但可能限制后验的表达能力。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_KYdfvF2SZN/figures/019_Table_4.jpg]]
*Table 4: Comparison of metrics across different datasets and methods. (a) Kang HVG dataset evaluated on a held-out set of size 500. The observation has dimension 5000, due to the size, the log likelihood for CNF cannot be directly computed by solving adjoint-ODE, therefore left out of the comparison. (b) Pendulum dataset over posterior samples of observed ( $\mathrm { R M S E } _ { x }$ ) , , and latent (RMSEz). Evaluated on a held-out set of size 300. (a) HVG Single-Cell RNA-Seq*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_KYdfvF2SZN/figures/020_Table_5.jpg]]
*Table 5: (b) Pendulum Trajectory*

## 定位与知识库关联

### 1. 与基线方法的关系

SFA 的核心贡献在于将**结构化隐变量**显式引入流匹配框架，从而在两类方法之间架起桥梁：一类是以 VAE 为代表的隐变量生成模型，另一类是以 Flow Matching 为代表的纯生成流模型。

**与 VAE 家族的关系。** VAE 通过最大化证据下界（ELBO）来学习隐变量表示，其似然模型通常采用简单的参数化分布（如高斯分布）。SFA 在以下关键维度上对 VAE 进行了根本性改造：

- **似然模型升级**：SFA 将 VAE 的参数化解码器替换为**条件连续归一化流（Conditional CNF）**（Eq. 7）。这一替换使似然模型具备任意表达能力，从根本上解决了 VAE 生成质量差的问题。
- **训练目标重构**：VAE 依赖 ELBO 中的 KL 散度项来正则化隐变量，这引入了著名的“重构-KL 权衡”困境——提高生成质量往往以牺牲隐变量结构为代价（β-VAE 等变体试图通过超参数缓解此问题）。SFA 的 SCFM 目标（Eq. 6）通过匹配条件向量场的期望来联合学习似然和后验，**无需任何重建-KL 权衡**。实验表明，SFA 在 Pinwheel 数据集上的 W1 距离（0.024）与纯 FM 模型（0.025）相当（Table 1），而 VAE 系列方法在此指标上远逊于两者，验证了 SFA 在保持生成质量方面的优势。
- **后验族灵活性**：SFA 支持多种后验近似族，包括对角高斯、条件 CNF、Gumbel-Softmax 等，而传统 VAE 通常局限于均值场高斯族。在 MNIST 实验中，Mixture-SFA 的聚类 NMI 达到 0.489，远超 Mixture-SVAE 的 0.161（Table 3），表明 SFA 框架下的结构化后验能更有效地捕获数据中的隐结构。

**与纯 Flow Matching 模型的关系。** 标准 FM 和 LatentFM 虽然生成保真度高，但缺乏对隐结构的显式建模。SFA 通过定理 3.1 证明：边际向量场可由条件向量场在后验分布下的期望完全生成。这一理论保证使 SFA 在**不牺牲边际密度估计精度**的前提下，为任意图模型结构提供流匹配似然。在 MNIST 上，SFA 的 SSIM（0.694）接近 LatentFM（0.709），但生成多样性指标 Vendi 高达 1675.9，远超 LatentFM 的 380.5（Table 2），说明 SFA 成功解耦了生成质量与结构表征。

**与结构化 VAE 的关系。** 在动态系统建模任务中，LDS-SFA 将隐变量 RMSE 从 GLD-SVAE 的 8.090 降至 1.526（Table 4b），降幅超过 5 倍。这一显著提升源于 SFA 的条件 CNF 似然比结构化 VAE 的高斯似然更能捕捉复杂动态。

### 2. 适用边界与局限

**适用场景。** SFA 特别适用于以下情形：
- 数据存在可解释的隐结构（聚类、动态、层次），且需要同时保持高保真生成；
- 下游任务依赖隐空间表征（如聚类、轨迹推断），且对生成多样性有要求；
- 观测数据维度适中，隐变量维度远低于观测维度。

**已知局限。**
1. **后验族选择缺乏系统指导**：当隐变量维度远小于观测维度时，如何系统选择后验族仍依赖经验试探。实验表明，简单参数族（如高斯）在多个任务中训练更稳定且已足够，但这一结论缺乏理论支撑。
2. **架构兼容性未明**：当解码器采用 UNet 等跳跃连接架构时，隐变量可能被绕过，导致后验崩塌。论文明确指出相应的架构设计要求尚不明确。
3. **可扩展性未验证**：实验仅在 Apple M2 Pro 上进行，未验证大规模数据或多 GPU 训练下的表现。
4. **离线训练限制**：SCFM 的训练过程依赖完整观测序列，无法进行在线学习，限制了其在流式数据场景的应用。

### 3. 开放问题与后续方向

1. **图模型结构扩展**：SFA 目前支持连续隐变量、有限混合模型和线性动态系统。能否扩展到离散隐变量、树结构或更复杂的概率图模型（如隐马尔可夫模型的高阶变体）仍待探索。
2. **高维后验稳定性**：对于高维数据，使用条件 CNF 作为后验可能导致训练不稳定。如何设计更稳定的高维后验近似方案是一个开放挑战。
3. **下游任务收益量化**：SFA 的隐空间表征在哪些具体下游任务中能比纯流匹配模型带来实质收益，目前仅在聚类和动态系统推断中进行了初步验证，更广泛的任务评估有待开展。
4. **大模型隐变量注入**：如何在大规模架构（如 UNet）中有效注入隐变量以防止后验崩塌，是 SFA 走向实际应用的关键工程问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Structured_Flow_Autoencoders_Learning_Structured_Probabilistic_Representations_with_Flow_Matching.pdf]]

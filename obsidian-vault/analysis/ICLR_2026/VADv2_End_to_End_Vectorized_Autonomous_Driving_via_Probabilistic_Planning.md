---
title: "VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VADv2_End_to_End_Vectorized_Autonomous_Driving_via_Probabilistic_Planning.pdf
openreview_forum_id: 0a4dA6eUHN
aliases:
- VADv2
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将规划重新定义为动作空间上的概率分布，并通过大规模驾驶演示学习该分布。具体做法是将动作空间离散化为规划词汇表，利用场景信息预测每个动作的概率，从中采样安全、多模态的驾驶动作。"
primary_logic: "通过离散化动作空间并学习场景条件下的概率分布，可有效建模驾驶中的多模态不确定性，避免确定性回归的模糊输出，提升闭环规划的安全性和鲁棒性。"
claims:
- "在CARLA Town05 Long闭环基准上，VADv2以仅使用相机的方式达到DS 85.1，显著超越此前最佳的相机方法（Rao et al. 2024的74.9）及多数相机+激光雷达融合方法。"
- "在NAVSIM navtest上，VADv2获得PDMS 89.3，超越Transfuser、PRIX等基线。"
- "概率规划在所有交通密度下均优于确定性规划，尤其在高密度下PDMS领先1.9点（87.7 vs 85.8）。"
- "使用4096大小的规划词汇表，结合最远轨迹采样（FTS）能最好地覆盖动作空间，取得最低碰撞率（3s 0.039%）。"
---

# VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning

> [!tip] 核心洞察
> 通过离散化动作空间并学习场景条件下的概率分布，可有效建模驾驶中的多模态不确定性，避免确定性回归的模糊输出，提升闭环规划的安全性和鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VADv2: 基于概率规划的端到端矢量化自动驾驶 |
| 英文题名 | VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0a4dA6eUHN); [GitHub](https://github.com/hustvl/VAD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VADv2 |
| Dataset | CARLA Town05 Long, NAVSIM navtest, 3DGS Closed-loop |

> [!tip] 效果简介
> - CARLA Town05 Long 上，DS (Driving Score) 为 85.1，对比 61.9 (VAD)，变化 +23.2。
> - CARLA Town05 Long 上，RC (Route Completion) 为 98.4，对比 87.3 (VAD)，变化 +11.1。
> - NAVSIM navtest 上，PDMS 为 89.3，对比 88.0 (TransFuser)，变化 +1.3。

## 概述

现有端到端自动驾驶规划方法普遍采用确定性范式——直接从场景特征回归出单一的未来轨迹或控制信号。然而，驾驶员行为本质上是多模态和高度不确定的：在同一场景下，存在多种合理且安全的操作（如变道或保持车道），可行解空间往往是非凸的。确定性建模在此类场景下容易产生模糊甚至不安全的中间动作，导致闭环规划失败。

针对这一瓶颈，VADv2 将规划重新定义为**动作空间上的场景条件概率分布学习问题**。其核心思路是：首先将连续的动作空间离散化为一个大规模“规划词汇表”（planning vocabulary），然后通过大规模驾驶演示数据学习场景到动作概率分布的映射，最终从该分布中采样出安全且符合场景的多模态驾驶动作。这种概率规划范式有效避免了确定性回归的模糊输出，显著提升了闭环场景下的安全性和鲁棒性。

在方法谱系上，VADv2 延续了其前作 **VAD**（Jiang et al., ICCV 2023）的矢量化场景表示思路，但在规划范式上做出了根本性转变——从确定性动作回归转向概率分布建模。相比于 **Transfuser**（Prakash et al., TPAMI 2022）、**UniAD**（Hu et al., Arxiv 2022）等端到端基线，以及 **GenAD**（Zheng et al., ECCV 2024）等自回归生成方法，VADv2 的关键差异在于动作空间的离散化表示和概率场函数的引入，使其能够显式建模驾驶行为的不确定性。

主要实验结果验证了这一范式的有效性：在 CARLA Town05 Long 闭环基准上，VADv2 仅使用相机输入即达到 **DS 85.1**，显著超越此前最佳的相机方法（Rao et al., TIV 2024 的 74.9）及多数相机-激光雷达融合方法；在 NAVSIM navtest 上获得 **PDMS 89.3**；在 3DGS 闭环基准上碰撞率降至 **0.270%**。消融实验进一步证实，概率规划在所有交通密度下均优于确定性规划，且分布损失与冲突损失对模型性能至关重要。

## 背景与动机

端到端自动驾驶的核心目标是直接从传感器输入映射到驾驶动作，省去传统模块化架构中感知、预测、规划之间的手工接口。近年来，以 **UniAD**（Hu et al., Arxiv 2022）和 **VAD**（Jiang et al., ICCV 2023）为代表的矢量化端到端方法，通过将场景表示为实例级令牌，显著提升了规划的可解释性与性能。然而，这些方法在规划环节普遍采用**确定性范式**——即给定场景观测 $o$，直接回归唯一的动作序列 $a$。

确定性规划的根本缺陷在于：驾驶行为本质上是高度不确定的。同一场景下，驾驶员可能选择不同的安全轨迹（如变道时机、让行策略），可行解空间往往呈**非凸分布**。当模型被强制输出单一动作时，确定性回归容易产生模糊的中间动作——即多个合理轨迹的“平均”——这种平均轨迹在实际执行中可能落入不可行区域，导致碰撞或偏离路线。现有方法（如 **Transfuser**, Prakash et al., TPAMI 2022）虽引入了多模态预测，但规划输出仍以单步回归为主，未能从根本上建模动作空间的不确定性。

这一瓶颈在闭环评测中尤为突出：开环指标相近的模型，闭环性能可能差距悬殊。**VADv2** 的作者指出，问题的症结不在于场景理解能力的不足，而在于规划策略对不确定性的处理方式。因此，本文的核心动机是：**将规划从确定性动作回归重新定义为场景条件下的概率分布学习**，使模型能够显式地建模“在当前场景下，哪些动作是合理的、安全的”，而非强求唯一的“最优”动作。

具体而言，VADv2 将连续的动作空间离散化为一个大规模的**规划词汇表**（Planning Vocabulary），每个词汇项代表一条预采样的候选轨迹；然后通过概率场函数学习场景到动作概率的映射 $p(a|o)$，并从大规模驾驶演示中通过 KL 散度监督该分布。这一范式转换使得模型能够自然输出多模态的安全动作，在非凸解空间中避免确定性回归的模糊输出问题。

## 核心创新

VADv2 的核心创新在于将端到端自动驾驶的规划从**确定性动作回归**重新定义为**场景条件概率分布建模**，从而系统性地应对驾驶行为中固有的多模态不确定性。这一范式转换通过三个紧密耦合的技术槽位实现，构成了方法的主干创新链。

### 从确定性回归到概率分布建模

传统端到端规划方法（如 **VAD**（Jiang et al., ICCV 2023）、**UniAD**（Hu et al., 2022））通常将规划视为连续动作空间上的回归任务，直接输出未来轨迹坐标。然而，驾驶场景与最优动作之间并不存在确定的映射关系——当可行解空间非凸时，确定性回归易产生模糊的“平均”输出，导致不安全的中间动作。VADv2 将规划策略建模为场景条件下的非平稳随机过程 $p(a|o)$，从大规模驾驶演示中学习动作空间的概率分布，而非直接回归单一轨迹。这一核心洞察（**Figure 1**）构成了整个方法的理论基础：通过捕捉驾驶行为的多模态性，模型能够在复杂场景下采样出安全、合理的动作，避免了确定性建模的模糊输出问题。

### 离散化规划词汇表：动作空间的令牌化

为实现概率分布建模，VADv2 将连续的动作空间离散化为一个固定大小的**规划词汇表**（planning vocabulary）。具体而言，动作 $a$ 被定义为未来 $T$ 个路径点的序列 $a = (x_1, y_1, x_2, y_2, ..., x_T, y_T)$，词汇表 $\mathcal{V}$ 包含 $N=4096$ 个预采样的代表性轨迹。采样策略采用**最远轨迹采样**（Furthest Trajectory Sampling, FTS），从大规模驾驶演示中迭代选取彼此距离最大的轨迹，以最大化对动作空间的覆盖（**Algorithm 1**）。消融实验证实，FTS 在词汇覆盖度和最终规划性能上均优于 k-means、K-disks 等策略（**Table 13**），且词汇量从 256 增至 4096 时，3s L2 误差从 0.337 降至 0.290，碰撞率从 0.057% 降至 0.039%（**Table 10**）。

### 概率场与级联 Transformer 解码器

为建模从动作空间到概率的连续映射，VADv2 引入**概率场函数**（probabilistic field function）。每个动作令牌通过正弦位置编码映射到高维嵌入空间：

$$E(\pmb{a}) = (\Gamma(x_i), \Gamma(y_i))_{i=1}^T, \quad \Gamma(\mathrm{pos}) = (\gamma(\mathrm{pos}, j))_{j=0}^{L-1}$$

其中 $\gamma(\mathrm{pos}, j) = (\cos(\mathrm{pos}/10000^{2\pi j/L}), \sin(\mathrm{pos}/10000^{2\pi j/L}))$。该编码捕捉了轨迹坐标的高频连续场特性。随后，级联 Transformer 解码器将动作嵌入与场景令牌 $E_{\mathrm{scene}}$ 交互，融合导航令牌 $E_{\mathrm{navi}}$ 和自车状态令牌 $E_{\mathrm{state}}$，通过 MLP 和 Sigmoid 输出每个动作的概率：

$$p(\pmb{a}) = \sigma(\mathrm{MLP}(\phi(E(\pmb{a}), E_{\mathrm{scene}}) + E_{\mathrm{navi}} + E_{\mathrm{state}}))$$

这一设计使得模型能够为词汇表中所有 4096 个动作并行预测概率分布，实现高效的多模态推理。

### 分布监督与安全先验的联合训练

训练损失函数的设计同样体现了从回归到分布建模的转变。VADv2 采用 **KL 散度/交叉熵损失**作为分布监督：

$$\mathcal{L}_{\mathrm{distribution}} = -\sum_{a\in\mathcal{V}} p_{\mathrm{data}}(a) \cdot \log p_{\mathrm{pred}}(a)$$

该损失直接最小化数据分布与预测分布之间的差异，而非拟合单一轨迹坐标。此外，**冲突损失**（conflict loss）为模型注入安全先验：

$$\mathcal{L}_{\mathrm{conflict}} = \sum_{\pmb{a}\in\mathcal{V}} \mathbb{1}_{\mathrm{conflict}}(\pmb{a}) \cdot \log p_{\mathrm{pred}}(\pmb{a})$$

该损失惩罚与未来真值轨迹或道路边界冲突的动作，降低其预测概率。消融实验表明，去除分布损失或冲突损失均导致规划精度大幅下降（3s L2 升高），证实了概率分布监督和安全先验的不可或缺性（**Table 7**）。总损失为三者之和：$\mathcal{L} = \mathcal{L}_{\mathrm{distribution}} + \mathcal{L}_{\mathrm{conflict}} + \mathcal{L}_{\mathrm{token}}$。

### 推理策略：从分布采样到安全过滤

推理阶段，VADv2 从预测分布中采样 Top-K 动作，通过基于规则的包裹器筛选安全动作，再由优化后处理器细化平滑轨迹。这一策略与确定性方法的单步回归加 PID 控制形成鲜明对比。消融表明，概率规划在所有交通密度下均优于确定性规划，尤其在高密度下 PDMS 领先 1.9 点（87.7 vs 85.8）（**Table 8**）。闭环实验中，VADv2 在 CARLA Town05 Long 上以纯相机输入达到 DS 85.1，显著超越此前最佳的相机方法（Rao et al. 2024 的 74.9）及多数融合方法（**Table 1**），验证了概率规划范式的有效性。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_0a4dA6eUHN/figures/004_Figure_2.jpg]]
*Figure 2: Overall architecture of VADv2. VADv2 takes multi-view image sequences as input in a streaming manner, tokenizes sensor data and planning action space, outputs the probabilistic distribution of action, and samples one action to control the vehicle. Large-scale driving demonstrations and scene constraints are used to supervise the predicted distribution*

VADv2 的整体架构围绕“场景条件概率规划”这一核心思想构建。其输入为多视角图像序列，输出为动作空间上的概率分布，最终通过采样获得一个安全、多模态的驾驶动作以控制车辆。

**输入流与场景编码。** 系统以流式方式接收多视角图像序列，首先通过场景编码器（Scene Encoder）将传感器数据转化为实例级的场景令牌（scene tokens）$E_{\mathrm{scene}} \in \mathbb{R}^{M \times D}$。这些令牌承载了地图结构、交通参与者、交通信号等高层语义信息。同时，导航信息与自车状态分别编码为导航令牌 $E_{\mathrm{navi}}$ 和状态令牌 $E_{\mathrm{state}}$，共同构成完整的观测表示 $o = (E_{\mathrm{scene}}, E_{\mathrm{navi}}, E_{\mathrm{state}})$。

**规划词汇表构建。** 与传统方法在连续空间直接回归轨迹坐标不同，VADv2 将动作空间离散化为一个大规模的规划词汇表 $\mathcal{V} = \{\pmb{a}^i\}_{i=1}^{N}$（默认 $N = 4096$）。每个动作 $\pmb{a}$ 定义为未来 $T$ 个路径点的序列 $\pmb{a} = (x_1, y_1, ..., x_T, y_T)$。词汇表的构建采用最远轨迹采样（Furthest Trajectory Sampling, FTS）策略，从大规模驾驶演示中选取覆盖不同驾驶模式的代表性轨迹，以最大化动作空间的覆盖度。

**概率场建模与动作评分。** 每个规划词汇表中的动作令牌通过正弦位置编码 $\Gamma(\cdot)$ 映射到高维空间，以捕捉轨迹坐标的高频连续场特性。随后，一个级联 Transformer 解码器 $\phi$ 将动作嵌入与场景令牌进行交互，融合导航和自车状态嵌入后，通过 MLP 和 Sigmoid 函数输出该动作在当前场景下的概率：

$$p(\pmb{a}) = \sigma(\mathrm{MLP}(\phi(E(\pmb{a}), E_{\mathrm{scene}}) + E_{\mathrm{navi}} + E_{\mathrm{state}}))$$

这一过程将规划策略建模为场景条件下的非平稳随机过程 $p(a|o)$，本质上是在动作空间上学习一个连续的概率场，从而捕捉驾驶行为的多模态不确定性。

**训练监督。** 训练阶段通过三个损失函数联合优化：分布损失（Distribution Loss）以 KL 散度或交叉熵形式最小化预测分布与数据分布之间的差异；冲突损失（Conflict Loss）惩罚与未来真值轨迹或道路边界冲突的动作，注入驾驶安全先验；令牌损失（Token Loss）则监督场景令牌的感知质量。总损失为三者之和：$\mathcal{L} = \mathcal{L}_{\mathrm{distribution}} + \mathcal{L}_{\mathrm{conflict}} + \mathcal{L}_{\mathrm{token}}$。

**推理与后处理。** 闭环推理时，系统从预测分布中采样 Top-K 个高概率动作，经基于规则的过滤器剔除不安全候选，再通过优化后处理器细化轨迹的平滑性，最终由 PID 控制器将选定的动作转换为方向盘、油门和刹车的控制信号。

整体架构的因果逻辑链清晰：**大规模驾驶演示 → 离散化动作空间（规划词汇表）→ 场景条件概率场建模 → 分布匹配与安全约束联合监督 → 概率采样与安全过滤 → 闭环控制**。这一设计从根本上将规划从确定性回归转变为不确定性感知的概率推断，是后续实验性能提升的结构性基础。

## 核心模块与公式推导

### 3.1 场景编码器（Scene Encoder）

VADv2 的场景编码器以流式方式接收多视角图像序列，将其转化为实例级令牌嵌入 $E_{\mathrm{scene}} \in \mathbb{R}^{M \times D}$。该模块提取四类高层语义令牌：

- **地图令牌（Map Tokens）**：编码道路拓扑与静态环境结构。
- **智能体令牌（Agent Tokens）**：编码周围交通参与者的运动状态。
- **交通元素令牌（Traffic Element Tokens）**：分为交通灯令牌与停止标志令牌，分别通过 MLP 预测交通灯状态和停止标志重叠情况，采用 Focal Loss 监督。
- **图像令牌（Image Tokens）**：保留原始视觉特征。

此外，系统维护导航令牌 $E_{\mathrm{navi}}$ 和自车状态令牌 $E_{\mathrm{state}}$，共同构成完整观测 $o = (E_{\mathrm{scene}}, E_{\mathrm{navi}}, E_{\mathrm{state}})$。

### 3.2 概率规划核心机制

#### 问题形式化

VADv2 将规划策略建模为场景条件的非平稳随机过程 $p(a|o)$。动作 $a$ 定义为未来 $T$ 个路径点的序列：

$$a = (x_1, y_1, x_2, y_2, ..., x_T, y_T)$$

#### 规划词汇表构建

为离散化连续动作空间，VADv2 采用最远轨迹采样（Furthest Trajectory Sampling, FTS）从大规模驾驶演示中提取代表性轨迹，构建固定大小的规划词汇表 $\bar{\nu} = \{\pmb{a}^i\}^{\dot{N}}$，默认 $N=4096$。FTS 策略在词汇覆盖度上显著优于 k-means、K-disks 等替代方案（Table 13）。

#### 动作令牌嵌入

每个路径点坐标通过正弦函数映射到高维空间，以捕捉高频连续场：

$$E(\pmb{a}) = (\Gamma(x_i), \Gamma(y_i))_{i=1}^T$$

$$\Gamma(\mathrm{pos}) = (\gamma(\mathrm{pos}, j))_{j=0}^{L-1}, \quad \gamma(\mathrm{pos}, j) = \left(\cos\left(\frac{\mathrm{pos}}{10000^{2\pi j/L}}\right), \sin\left(\frac{\mathrm{pos}}{10000^{2\pi j/L}}\right)\right)$$

#### 概率场与动作预测

级联 Transformer 解码器 $\phi$ 将动作嵌入与场景令牌交互，融合导航和状态嵌入后，经 MLP 和 Sigmoid 输出动作概率：

$$p(\pmb{a}) = \sigma(\mathrm{MLP}(\phi(E(\pmb{a}), E_{\mathrm{scene}}) + E_{\mathrm{navi}} + E_{\mathrm{state}}))$$

该设计将离散词汇表上的概率预测转化为动作空间上的连续概率场映射。

### 3.3 训练监督信号

#### 分布损失（Distribution Loss）

通过最小化数据分布 $p_{\mathrm{data}}$ 与预测分布 $p_{\mathrm{pred}}$ 之间的 KL 散度，使模型学习专家驾驶行为的概率分布：

$$\mathcal{L}_{\mathrm{distribution}} = D_{\mathrm{KL}}(p_{\mathrm{data}} || p_{\mathrm{pred}}) = \sum_{a\in\mathcal{V}} p_{\mathrm{data}}(a) \cdot \log \frac{p_{\mathrm{data}}(a)}{p_{\mathrm{pred}}(a)}$$

由于 $p_{\mathrm{data}}$ 在训练时固定，KL 散度等价于交叉熵损失：

$$\mathcal{L}_{\mathrm{distribution}} = -\sum_{a\in\mathcal{V}} p_{\mathrm{data}}(a) \cdot \log p_{\mathrm{pred}}(a)$$

消融实验（Table 7）表明，去除分布损失（ID 1）会导致 3s L2 误差和碰撞率显著上升，验证了概率分布监督的关键作用。

#### 冲突损失（Conflict Loss）

利用场景约束惩罚不安全的动作预测，将碰撞先验注入概率分布：

$$\mathcal{L}_{\mathrm{conflict}} = \sum_{\pmb{a}\in\mathcal{V}} \mathbb{1}_{\mathrm{conflict}}(\pmb{a}) \cdot \log p_{\mathrm{pred}}(\pmb{a})$$

其中 $\mathbb{1}_{\mathrm{conflict}}(\pmb{a})$ 指示动作 $\pmb{a}$ 是否与未来真值轨迹或其他道路参与者发生冲突。去除冲突损失（Table 7，ID 2）同样导致规划精度大幅下降，证明安全先验不可或缺。

#### 总损失

三项损失的加权和（系数均为 1）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{distribution}} + \mathcal{L}_{\mathrm{conflict}} + \mathcal{L}_{\mathrm{token}}$$

其中 $\mathcal{L}_{\mathrm{token}}$ 为场景令牌的感知监督损失（含交通元素令牌的 Focal Loss）。

### 3.4 推理后处理

闭环推理时，VADv2 从预测分布中采样 Top-K 动作（默认 Top-1），经基于规则的包裹器过滤不安全动作，再通过优化后处理器细化轨迹平滑性，最终由 PID 控制器转换为方向盘转角、油门和刹车控制信号。

## 实验与分析

### 核心实验设置

VADv2 在四个闭环基准上进行了全面评估：CARLA Town05 Long、NAVSIM navtest、NAVSIMv2 以及基于 3DGS 的闭环基准。规划输出为 3 秒未来轨迹，包含 6 个路径点（间隔 0.5 秒，即 $T=6$）。所有延迟测试统一在 RTX 4090 上进行，确保时间比较的一致性。

### 主结果分析

**CARLA Town05 Long（Table 1）**：VADv2 以纯相机输入取得 **DS 85.1、RC 98.4、IS 0.87**，显著超越此前最佳的相机方法（Rao et al., TIV 2024 的 DS 74.9），并超过多数相机+激光雷达融合方法。相比前作 **VAD**（Jiang et al., ICCV 2023）的 DS 61.9，提升达 +23.2 点，路线完成率从 87.3 跃升至 98.4。这一飞跃的核心驱动力在于概率规划范式对驾驶不确定性的有效建模——当可行解空间非凸时，确定性回归容易产生模糊甚至不安全的中间动作，而 VADv2 通过在大规模驾驶演示上学习场景条件的动作概率分布，从根本上规避了这一问题。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_0a4dA6eUHN/figures/005_Table_1.jpg]]
*Table 1: Closed-loop evaluation on the Town05 Long benchmark*

**NAVSIM navtest（Table 2）**：VADv2 取得 **PDMS 89.3**，超越 **TransFuser**（Prakash et al., TPAMI 2022）的 88.0 和 **PRIX** 等基线。PDMS 作为综合闭环指标，反映了规划的安全性与舒适性，VADv2 的优势表明概率分布在处理多模态驾驶行为方面具有本质优势。

**NAVSIMv2（Table 3）**：在扩展指标上，VADv2 取得 **NC 98.0、DAC 98.3、DDC 99.4**，在 10 项指标中的 7 项上达到最优或并列最优。与 **HydraMDP++** 和 **PRIX** 相比，VADv2 在驾驶区域合规性（DAC）和交通灯合规性（TL 99.8）上表现突出，这得益于其场景令牌中对交通元素（交通灯、停止标志）的显式建模与监督。

**3DGS 闭环基准（Table 4）**：所有方法在此基准上采用相同感知骨干，确保比较公平。VADv2 的碰撞率（CR）降至 **0.270**，低于 TransFuser 的 0.320 和 **GenAD**（Zheng et al., ECCV 2024）的 0.285；动态碰撞率（DCR）为 0.240，静态碰撞率（SCR）仅 0.030。这表明概率规划在真实世界 3DGS 重建场景中同样有效，且对静态障碍物的规避尤为可靠。

**Bench2Drive（Table 5）**：VADv2 以 **DS 76.15** 领先 **SparseDrive**、**MomAD**、**DriveTransformer** 等方法，进一步验证了概率规划范式在不同闭环环境下的泛化能力。

### 消融实验：概率规划 vs. 确定性规划

**Table 12** 直接对比两种规划范式：概率规划将闭环 DS 从 74.6 提升至 85.1，但开环 L2 指标相近。这说明概率分布监督的核心价值不在轨迹拟合精度，而在于闭环安全性——通过建模多模态分布，模型能够避免确定性回归在非凸解空间中的模糊输出。

**Table 8** 按交通密度分层分析显示，概率规划在所有密度下均优于确定性规划，且差距随密度增大而扩大：低密度下 PDMS 领先 1.2（90.6 vs. 89.4），高密度下领先 1.9（87.7 vs. 85.8）。这验证了核心论点——交通密度越高，可行解空间的非凸性越强，确定性建模的局限性越显著，概率分布的优势越明显。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_0a4dA6eUHN/figures/012_Table_8.jpg]]
*Table 8: Ablation on the performance under different planning manners and traffic densities*

### 消融实验：损失函数设计

**Table 7** 揭示了两个关键损失的必要性：


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_0a4dA6eUHN/figures/011_Table_7.jpg]]
*Table 7: Ablations on design choices. “Dist.”: Distribution; “Traf. Token”: Traffic Element Token*

- **去除分布损失（ID 1）**：3s L2 误差从 0.290 升至 0.615，3s 碰撞率从 0.039% 升至 0.075%。分布损失通过 KL 散度（等价于交叉熵）将预测分布对齐到大规模驾驶演示的数据分布，是模型学习专家行为的主要驱动力。公式为：
  $$\mathcal{L}_{\mathrm{distribution}} = -\sum_{a\in\mathcal{V}} p_{\mathrm{data}}(a) \cdot \log p_{\mathrm{pred}}(a)$$

- **去除冲突损失（ID 2）**：3s L2 升至 0.370，碰撞率升至 0.056%。冲突损失通过惩罚与未来真值轨迹或道路边界冲突的动作，为模型注入关键的安全先验：
  $$\mathcal{L}_{\mathrm{conflict}} = \sum_{\pmb{a}\in\mathcal{V}} \mathbb{1}_{\mathrm{conflict}}(\pmb{a}) \cdot \log p_{\mathrm{pred}}(\pmb{a})$$

- **同时去除两者**：3s L2 飙升至 0.810，碰撞率达 0.088%，性能全面崩溃。

此外，去除交通元素令牌（ID 6）导致 3s L2 升至 0.345，碰撞率升至 0.057%，说明交通灯和停止标志的显式感知对规划安全至关重要。总损失为三者的等权和：
  $$\mathcal{L} = \mathcal{L}_{\mathrm{distribution}} + \mathcal{L}_{\mathrm{conflict}} + \mathcal{L}_{\mathrm{token}}$$

### 消融实验：规划词汇表设计

**词汇量大小（Table 10）**：将词汇量从 256 逐步增加到 4096，3s L2 误差从 0.337 降至 0.290，碰撞率从 0.057% 降至 0.039%。继续增加到 8192 时收益递减（L2 0.282，碰撞率 0.036%），但计算成本显著增加。默认设置 4096 在覆盖度与效率之间取得了最佳平衡。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_0a4dA6eUHN/figures/015_Table_10.jpg]]
*Table 10: Ablation on vocabulary size*

**采样策略（Table 13）**：最远轨迹采样（FTS）在所有指标上均优于 k-means、K-disks 和 nuScenes 基线。FTS 的平均离散化误差仅 0.102，最大误差 0.181，最终 PDMS 达 89.3。其优势在于主动覆盖动作空间的边界区域，而非仅聚类中心，从而更好地捕捉罕见但关键的驾驶模式（如急转弯、快速变道）。Figure 5 可视化了 FTS 构建的规划词汇表，展现了覆盖广泛角度和曲率的扇形轨迹分布。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_0a4dA6eUHN/figures/018_Table_13.jpg]]
*Table 13: Ablation on the discretization error and performance of vocabulary sampling strategies*

**训练数据规模（Table 11）**：训练片段从 1e5 增加到 3e6，3s L2 误差从 0.461 大幅降至 0.225，碰撞率从 0.055% 降至 0.007%。这表明概率分布学习对数据规模高度敏感，更大规模的驾驶演示能显著提升分布估计的精度。

### 多模态输出分析

**Table 6** 显示，Top-1 采样（选择最高概率动作）获得最优 PDMS 89.3，而 Top-5 提供多样性但性能略降（PDMS 87.2）。这说明在大多数场景下，分布峰值已能给出安全动作，多模态输出在需要备选方案时（如高交互场景）具有潜在价值，但当前推理策略尚未充分利用这一能力。

### 失败模式与局限性

尽管 VADv2 在各项基准上表现优异，但分析揭示了以下局限：

1. **词汇表覆盖边界**：固定 4096 大小的词汇表在极端场景（如紧急避让、非结构化道路）仍可能出现覆盖不足，Figure 5 中轨迹分布集中在常见驾驶模式区域。

2. **数据分布依赖**：分布学习完全依赖大规模驾驶演示，sim-to-real gap 的量化验证尚不充分。3DGS 基准虽使用真实世界重建场景，但传感器模型和行为模型仍与真实环境存在差异。

3. **推理复杂度**：Top-K 采样、基于规则的包裹器和优化后处理器虽然提升了安全性与平滑性，但增加了系统复杂性，且规则包裹器的参数敏感性未充分讨论。

4. **规划时域限制**：当前仅规划 3 秒内的轨迹，对于需要更长时域决策的场景（如复杂交叉口、高速汇入）可能不够。

### 关键图表结论总结

- **Table 1**：VADv2 在 CARLA Town05 Long 上以纯相机取得 DS 85.1，确立新的 state-of-the-art。
- **Table 8**：概率规划在所有交通密度下优于确定性规划，高密度下优势最显著（+1.9 PDMS）。
- **Table 7**：分布损失和冲突损失是性能支柱，去除任一均导致规划精度和安全性大幅下降。
- **Table 10 + Table 13**：4096 大小的 FTS 词汇表在覆盖度与效率间取得最优平衡。
- **Table 11**：训练数据规模从 1e5 增至 3e6 片段，碰撞率降低近 8 倍（0.055% → 0.007%），表明规模化是进一步提升性能的关键路径。

## 方法谱系与知识库定位

### 与前作 VAD 的继承与变革

VADv2 直接继承自 **VAD**（Jiang et al., ICCV 2023）的矢量化场景表示范式，但在规划核心上发生了根本性转变。VAD 采用确定性动作回归，直接从连续动作空间输出单一轨迹，并通过 PID 控制器转化为控制信号。VADv2 保留了 VAD 的场景编码器骨架——将多视角图像序列转化为实例级场景令牌（地图、智能体、交通元素、图像令牌），但将规划范式从“回归一个最优动作”重构为“学习动作空间上的概率分布”。这一转变的因果逻辑在于：驾驶行为本质上是多模态且不确定的，可行解空间非凸时，确定性回归容易产生模糊的中间动作，导致闭环规划失败。

### 与生成式规划方法的对比

**GenAD**（Zheng et al., ECCV 2024）将规划建模为自回归生成任务，逐时间步预测未来路径点。VADv2 与之不同之处在于：GenAD 关注轨迹的时序生成过程，而 VADv2 关注动作空间的全局概率建模——一次性预测整个轨迹词汇表中每个候选动作的概率，然后从中采样。两者均试图捕捉多模态性，但 VADv2 的概率场方法避免了自回归过程中的误差累积问题。

**LeapVAD** 和 **HydraMDP++** 同样探索了规划词汇表或多模态规划的思路，但 VADv2 的差异化在于：（1）采用最远轨迹采样（FTS）构建词汇表，在覆盖度上优于 k-means 等聚类策略（Table 13）；（2）引入概率场函数（正弦位置编码 + 级联 Transformer 解码器）将离散词汇表映射为连续概率分布，而非简单的分类头；（3）通过冲突损失显式编码安全先验，惩罚与未来真值或道路边界冲突的动作。

### 与端到端集成范式的定位

**UniAD**（Hu et al., Arxiv 2022）将感知、预测、规划集成为统一框架，强调模块间的信息流动。VADv2 同样采用矢量化场景表示并监督感知令牌，但其核心贡献不在于模块集成，而在于规划层本身的概率化重构。在 CARLA Town05 Long 基准上，VADv2 以纯视觉输入达到 DS 85.1，显著超越 UniAD 以及此前最佳的纯视觉方法 **Rao et al. 2024**（TIV 2024，DS 74.9），甚至超过多数相机+激光雷达融合方法（Table 1）。

**Transfuser**（Prakash et al., TPAMI 2022）是基于 CNN 和 Transformer 的经典端到端基线。在 NAVSIM navtest 上，VADv2 取得 PDMS 89.3，超越 Transfuser 的 88.0（Table 2）；在 3DGS 闭环基准上，VADv2 将碰撞率从 Transfuser 的 0.320 降至 0.270（Table 4）。

### 适用边界与局限

1. **词汇表覆盖的固定性**：规划词汇表大小固定为 4096，虽通过 FTS 策略最大化覆盖度，但极端场景（如罕见避障模式）仍可能出现覆盖不足。词汇表无法动态扩展以适应未知环境，需要重新采样和训练。

2. **数据分布依赖**：概率分布的学习完全依赖大规模驾驶演示（消融显示训练片段从 1e5 增至 3e6 时 L2 误差从 0.461 降至 0.225，Table 11）。泛化能力受限于训练数据的分布，sim-to-real gap 仍需在真实世界数据上进一步验证。

3. **规划时域限制**：当前仅规划未来 3 秒内的轨迹（6 个路径点，间隔 0.5s），对于需要更长时域决策的场景（如复杂路口博弈）可能不够充分。

4. **推理管线复杂性**：推断时采用 Top-K 采样 + 基于规则的过滤 + 优化后处理器的多阶段管线，虽然提升了安全性与平滑性，但引入了额外的参数敏感性和系统复杂度。作者声称即使去除规则包裹器也能稳定运行，但该声明的证据强度需要手动验证。

### 开放问题

- 如何利用更大规模、更多样化的专家驾驶数据来进一步缩小仿真与现实之间的差距？
- 概率规划词汇能否动态扩展以适应未知环境，而不需要重新训练整个分布？
- 如何将更先进的视觉语言模型（VLM）或大语言模型（LLM）融入概率规划框架，以处理需要复杂意图推理的驾驶场景？

## 原文 PDF

![[paperPDFs/ICLR_2026/VADv2_End_to_End_Vectorized_Autonomous_Driving_via_Probabilistic_Planning.pdf]]

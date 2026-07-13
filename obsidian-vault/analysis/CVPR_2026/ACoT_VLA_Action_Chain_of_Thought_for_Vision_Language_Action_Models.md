---
title: "ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ACoT_VLA_Action_Chain_of_Thought_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: "https://github.com/AgibotTech/ACoT-VLA"
aliases:
- AV
- ACoT-VLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将Chain-of-Thought范式从语言或视觉空间转移到动作空间，直接生成结构化的粗粒度动作意图序列作为推理步骤（即Action Chain-of-Thought），提供运动学上一致的动作引导。
primary_logic: 通过显式动作推理器（EAR）生成粗参考轨迹，与隐式动作推理器（IAR）从VLM内部表征中提取的潜在动作先验相结合，在动作空间内提供互补的显式和隐式引导，使策略学习更加扎实。
claims:
- ACoT将思维过程重新定义为结构化动作意图序列，而非语言或视觉子目标
- EAR与IAR协同提供互补的动作空间引导，显著提升策略性能
- 在LIBERO基准上，方法平均成功率提升1.6%，并在长程任务上表现突出
- LIBERO 上 平均成功率 (%) = 98.5
---

# ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models

> [!tip] 核心洞察
> 通过显式动作推理器（EAR）生成粗参考轨迹，与隐式动作推理器（IAR）从VLM内部表征中提取的潜在动作先验相结合，在动作空间内提供互补的显式和隐式引导，使策略学习更加扎实。

| 字段 | 内容 |
|------|------|
| 中文题名 | ACoT-VLA：面向视觉-语言-动作模型的行动链式思维 |
| 英文题名 | ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.11404) · [Code](https://github.com/AgibotTech/ACoT-VLA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ACoT-VLA |
| Dataset | LIBERO, LIBERO-Plus, VLABench, Genie-Sim 3.0 |

> [!tip] 效果简介
> - LIBERO 上，平均成功率 (%) 98.5 vs 96.9 (π0.5) (+1.6%)。
> - LIBERO-Plus (监督微调) 上，平均成功率 (%) 88.0 vs 75.7 (π0.5) (+12.3%)。
> - VLABench 上，意图得分 (IS) / 进度得分 (PS) 63.5% / 47.4% vs 54.1% / 40.2% (π0.5) (+9.4% / +7.2%)。

## 概要

**问题瓶颈**：现有视觉-语言-动作（VLA）策略的推理过程主要在视觉-语言空间中展开，存在**语义-运动学差距**——高阶语义表示与低层精确动作执行之间缺乏直接联系，导致引导信息间接且不充分，难以实现精确的动作生成。

**核心方法**：本文提出**行动链式思维（Action Chain-of-Thought, ACoT）**范式，将推理过程重新定义为结构化的粗粒度动作意图序列，直接在动作空间中提供运动学一致的引导。基于此范式构建的 **ACoT-VLA** 架构引入两个互补组件：**显式动作推理器（EAR）** 生成粗参考轨迹作为显式引导，**隐式动作推理器（IAR）** 从 VLM 内部表征中提取潜在动作先验作为隐式引导，二者通过**动作引导预测头（AGP）** 融合后条件化最终的降噪过程。

**主要结果**：在 LIBERO 基准上，ACoT-VLA 平均成功率达 **98.5%**，较此前最优方法 π0.5 提升 **1.6%**，在长程任务（LIBERO-Long）上提升尤为显著。在 LIBERO-Plus 监督微调设置下，成功率从 75.7% 提升至 **88.0%**（+12.3%）。在 VLABench 上，意图得分和进度得分分别提升 **+9.4%** 和 **+7.2%**。模拟到真实迁移实验中，真实世界成功率从 77.5% 提升至 **82.9%**（+5.4%）。消融实验证实 EAR 与 IAR 协同互补：单独添加 EAR 使 LIBERO-Plus 成功率从 75.7% 升至 83.7%，单独添加 IAR 升至 80.4%，二者结合达到最高 84.1%。

### 机器人策略中的语义-运动学鸿沟

通用机器人操作策略的核心任务是根据视觉观察 $o_t$ 和语言指令 $l$ 预测动作序列 $a_{t:t+H-1}$。近年来，视觉-语言模型（VLM）的引入极大地提升了策略对多模态输入的理解能力，使机器人能够处理复杂的语义指令。然而，现有VLA（Vision-Language-Action）策略存在一个根本性瓶颈：**推理过程主要发生在视觉-语言空间中，而动作生成却发生在运动学空间中**。高阶语义表示（如“拿起杯子”）与低层精确动作执行（如关节角度序列）之间缺乏直接联系，导致引导信息间接且不充分，难以实现精确的动作生成。这一语义-运动学差距构成了当前通用机器人策略性能提升的关键障碍。

### 现有Chain-of-Thought范式的局限

为弥合高层推理与低层执行之间的鸿沟，研究者借鉴大语言模型中的Chain-of-Thought（CoT）范式，在机器人策略中引入中间推理步骤。如图1所示，现有工作主要沿两条路径展开：

- **语言CoT**：将推理过程表述为子任务序列（如“先移动到物体上方，再抓取”），在语言空间中提供语义引导。然而，语言子目标本质上仍是抽象的语义描述，无法直接转化为精确的运动约束。
- **视觉CoT**：通过合成目标图像或未来帧来引导动作策略，在视觉空间中提供引导。虽然视觉子目标比语言更接近动作空间，但图像到动作的映射仍然是非平凡的，且视觉生成本身引入了额外的计算开销和不确定性。

这两种范式的共同局限在于：**引导信号与被引导的动作处于不同的表示空间**。语言和视觉引导是异质的、间接的，策略仍需自行学习从这些异质信号到精确动作的复杂映射。

### 核心动机：将推理转移到动作空间

本文的核心洞察是：**如果推理步骤本身就是动作，那么引导信号与最终输出将处于同一空间，从而消除表示鸿沟**。基于这一洞察，我们提出**Action Chain-of-Thought（ACoT）范式**——将推理过程重新定义为结构化的粗粒度动作意图序列，而非抽象的语言或视觉子目标。这是首个将策略的推理过程直接置于动作空间中的工作。

ACoT范式的关键优势在于**同质引导**：中间推理步骤（粗参考轨迹）与最终输出（精确动作序列）共享相同的运动学表示，使引导信号具有直接的可执行性和运动学一致性。这一设计从根本上缩短了从感知到执行的推理路径，为策略学习提供了更扎实的归纳偏置。

## 核心方法与创新机理

ACoT-VLA的核心创新在于将Chain-of-Thought范式从语言或视觉空间**迁移到动作空间**，直接以结构化的粗粒度动作意图序列作为推理步骤，弥合VLA策略中高阶语义与低层动作执行之间的“语义-运动学差距”。这一范式转换通过两个互补的动作空间引导机制实现。

### 1. 动作空间Chain-of-Thought范式

现有VLA策略的推理过程主要发生在视觉-语言（输入）空间：语言CoT预测子任务作为中间推理，视觉CoT合成目标图像作为引导（Figure 1）。这些引导信号与最终的动作输出处于**不同模态空间**，导致引导信息间接且不充分。ACoT直接将推理过程定义为动作空间内的结构化意图序列，使引导信号与策略输出同构，提供运动学上一致的直接引导。

### 2. 显式动作推理器（EAR）

EAR是一个轻量Transformer模块，**自主合成粗参考轨迹**作为显式动作空间引导。其关键设计包括：

- **层间交叉注意力**：EAR的每层对参考动作隐状态进行自注意力，并与VLM对应层的KV缓存进行交叉注意力（公式4），使参考轨迹的生成深度依赖于多模态上下文。
- **流匹配去噪**：EAR以噪声动作序列为输入，通过流匹配生成去噪后的参考动作序列 $a_{t:t+H^{ref}-1}^{ref}$（公式6），为下游动作头提供可执行的显式运动先验。
- **残差前馈更新**：每层通过残差FFN更新表示（公式5），保证深层梯度流动。

与基线方法直接预测动作序列不同，EAR引入了**中间推理产物**——粗参考轨迹，使策略学习从“端到端黑箱映射”转变为“先推理后执行”的结构化过程。

### 3. 隐式动作推理器（IAR）

IAR从VLM内部表征中提取**潜在动作先验**，提供与EAR互补的隐式引导。其核心机制为：

- **降采样投影**：通过可学习线性子网络将VLM各层的KV缓存映射到低维空间（公式7），降低计算开销。
- **跨层聚合**：对每层VLM表征，使用可学习查询通过交叉注意力提取隐式动作语义 $\boldsymbol{z}_i^{\mathrm{im}}$，经池化与MLP投影后跨层聚合为 $Z^{\mathrm{im}}$（公式8）。
- **表征级先验**：与EAR生成的显式轨迹不同，IAR提供稠密的表征级行为先验，捕获VLM内部隐含的动作相关线索。

### 4. 显式-隐式协同融合

动作引导预测头（AGP）通过**双路交叉注意力**融合两种引导：

$$S^{\mathrm{ex}} = \mathrm{CrossAttn}(Q_{action}, Z^{\mathrm{ex}}, Z^{\mathrm{ex}})$$
$$S^{\mathrm{im}} = \mathrm{CrossAttn}(Q_{action}, Z^{\mathrm{im}}, Z^{\mathrm{im}})$$

拼接后经自注意力融合为统一动作引导 $\bar{h}$（公式11），条件化最终的流匹配去噪过程。消融实验证实二者**本质互补**：单独添加EAR使LIBERO-Plus成功率从75.7%提升至83.7%，单独添加IAR提升至80.4%，二者结合达到最高84.1%（Table 9）。

### 5. 与基线的关键差异

| 设计维度 | 基线方法（如π0.5） | ACoT-VLA |
|---------|-------------------|----------|
| 推理空间 | 视觉-语言空间 | **动作空间** |
| 引导信号 | 无显式动作引导 | EAR生成粗参考轨迹 + IAR提取隐式动作先验 |
| 中间推理产物 | 无 | 结构化动作意图序列 |
| 动作头条件化 | 仅依赖VLM嵌入 | 融合显式与隐式动作引导的双路交叉注意力 |

这一设计使ACoT-VLA在LIBERO基准上平均成功率提升1.6%（98.5% vs. 96.9%），在长程任务上表现尤为突出，并在LIBERO-Plus监督微调设置下实现12.3%的显著提升（88.0% vs. 75.7%）。

ACoT-VLA 的核心设计思路是将思维链（Chain-of-Thought）从语言或视觉空间迁移到**动作空间**，直接生成结构化的粗粒度动作意图序列作为中间推理步骤，从而弥合高层语义表示与低层精确动作执行之间的**语义-运动学差距**。

### 框架总览

整个框架构建在一个共享的预训练 VLM 骨干之上，由三个核心模块协同工作：**显式动作推理器（Explicit Action Reasoner, EAR）**、**隐式动作推理器（Implicit Action Reasoner, IAR）** 和 **动作引导预测头（Action-Guided Prediction, AGP）**。其工作流程如下：

1. **多模态编码**：给定视觉观察 $o_t$ 和语言指令 $l$，预训练的 VLM（SigLIP 视觉编码器 + Gemma 2B 语言骨干，共 $N=18$ 层）将其编码为逐层的键值缓存：

   $$(K_{1:N}^{VLM}, V_{1:N}^{VLM}) = \mathrm{VLM}(o_t, l)$$

2. **显式动作引导生成**：EAR 以噪声动作序列和 VLM 各层 KV 缓存为输入，通过流匹配（flow matching）逐步去噪，合成一条粗参考轨迹 $a_{t:t+H^{ref}-1}^{ref}$。这条参考轨迹直接在动作空间中提供可执行的显式运动学引导。

3. **隐式动作先验提取**：IAR 通过可学习的降采样子网络将 VLM 各层的 KV 缓存投影到低维空间，再以可学习查询（learnable queries）进行交叉注意力，跨层聚合出隐式动作语义表示 $Z^{\mathrm{im}}$。这些特征捕获了 VLM 内部表征中蕴含的潜在行为先验。

4. **双路引导融合与动作生成**：AGP 头接收 EAR 的显式动作嵌入 $Z^{\mathrm{ex}}$ 和 IAR 的隐式动作特征 $Z^{\mathrm{im}}$，通过双路交叉注意力分别与动作查询（action queries）交互，得到显式引导表示 $S^{\mathrm{ex}}$ 和隐式引导表示 $S^{\mathrm{im}}$：

   $$S^{\mathrm{ex}} = \mathrm{CrossAttn}(Q_{action}, Z^{\mathrm{ex}}, Z^{\mathrm{ex}})$$
   $$S^{\mathrm{im}} = \mathrm{CrossAttn}(Q_{action}, Z^{\mathrm{im}}, Z^{\mathrm{im}})$$

   随后将二者拼接并通过自注意力融合，形成统一的动作引导：

   $$\bar{h} = \mathrm{Self-Attn}([S^{\mathrm{ex}}; S^{\mathrm{im}}])$$

   最终由动作头 $\pi_{\theta}^{\mathrm{head}}$ 基于融合引导 $\bar{h}$ 预测去噪后的可执行动作序列 $a_{t:t+H-1}$。

### 模块间的协同关系

EAR 和 IAR 是**内在互补**的：EAR 提供显式的粗粒度运动轨迹引导，直接约束动作输出的运动学可行性；IAR 则从 VLM 的深层表征中提取稠密的表示级行为先验，为策略提供隐式的“行为灵感”。两者在动作空间内形成同质的引导信号，使下游的动作头能够在更扎实的条件下进行去噪预测，而非像传统 VLA 策略那样仅依赖视觉-语言嵌入直接映射到动作。

### 训练目标

整个框架以端到端方式联合训练，总损失为 EAR 和动作头两个流匹配 MSE 损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_1 \mathcal{L}_{\pi_{\theta}^{\mathrm{ref}}} + \lambda_2 \mathcal{L}_{\pi_{\theta}^{\mathrm{head}}}$$

其中 $\lambda_1 = \lambda_2 = 0.5$，参考动作预测 horizon $H^{ref}=15$，动作策略输出 horizon $H=10$，对应的动作偏移（action shift）分别为 2 和 1。训练时采用 teacher forcing 稳定化策略，推理时切换为自条件模式。

> **证据强度说明**：上述框架描述均来自论文的方法论章节（Section 3.2–3.4）及对应公式，置信度 ≥ 0.9。架构总览图见 **Figure 2**。

![[assets/figures/papers/paper_list_l2368_https_arxiv_org_abs_2601_11404/figures/002_Figure_2.jpg]]
*Figure 2: Architectural Overview of ACoT-VLA. The framework consists of three main components operating on features from a shared VLM backbone. (a) The Explicit Action Reasoner (EAR) is a Transformer-based module that synthesizes a coarse reference trajectory, providing explicit action-space guidance. (b) The Implicit Action Reasoner (IAR) employs a cross-attention mechanism with learnable queries to extract latent action priors from the VLM’s internal representations. (c) The Action-Guided Prediction (AGP) head synergistically integrates both explicit and implicit guidances via cross-attention to condition the final denoising process, producing the executable action sequence*

ACoT-VLA 的核心架构建立在共享的 VLM 骨干之上，由三个关键模块协同构成：**显式动作推理器（EAR）**、**隐式动作推理器（IAR）** 和 **动作引导预测头（AGP）**。以下逐一剖析各模块的公式化机制与变量含义。

### VLM 骨干：多模态编码

预训练的视觉-语言模型将视觉观察 $o_t$ 与语言指令 $l$ 编码为 $N$ 层的键值缓存（KV-Cache），作为下游模块的统一多模态表示基础：

$$(K_{1:N}^{\mathrm{VLM}}, V_{1:N}^{\mathrm{VLM}}) = \mathrm{VLM}(o_t, l) \tag{3}$$

其中 $K_i^{\mathrm{VLM}}, V_i^{\mathrm{VLM}}$ 分别表示第 $i$ 层的键和值张量。视觉编码器采用 **SigLIP**，语言骨干实例化为 **Gemma 2B** 架构（$N=18$ 层）。

### 显式动作推理器（EAR）：粗参考轨迹生成

EAR 是一个轻量级 Transformer，其核心功能是从噪声动作序列出发，逐层与 VLM 的 KV 缓存进行交叉注意力，生成运动学上可执行的粗参考轨迹，作为显式的动作空间引导。

**逐层更新机制**：EAR 的每一层 $i$ 对参考动作的隐状态 $h_{i-1}^{\mathrm{ref}}$ 执行自注意力，并与对应 VLM 层的缓存进行交叉注意力：

$$\tilde{h}_i^{\mathrm{ref}} = \mathrm{Self\text{-}Attn}(h_{i-1}^{\mathrm{ref}}) + \mathrm{CrossAttn}(h_{i-1}^{\mathrm{ref}}, K_i^{\mathrm{VLM}}, V_i^{\mathrm{VLM}}) \tag{4}$$

随后通过残差前馈网络完成表示更新：

$$h_i^{\mathrm{ref}} = h_{i-1}^{\mathrm{ref}} + \mathrm{FFN}(\tilde{h}_i^{\mathrm{ref}}) \tag{5}$$

**去噪动作生成**：EAR 采用流匹配（flow matching）范式，以噪声动作序列 $\tilde{a}_{t:t+H^{\mathrm{ref}}-1}$ 为输入，输出去噪后的参考动作序列：

$$a_{t:t+H^{\mathrm{ref}}-1}^{\mathrm{ref}} = \pi_{\theta}^{\mathrm{ref}}(\tilde{a}_{t:t+H^{\mathrm{ref}}-1}, K_{1:N}^{\mathrm{VLM}}, V_{1:N}^{\mathrm{VLM}}) \tag{6}$$

其中 $H^{\mathrm{ref}}$ 为参考动作的预测时域（固定为 15），$\pi_{\theta}^{\mathrm{ref}}$ 表示 EAR 的去噪函数。该参考轨迹提供了与最终动作同质的显式运动引导，直接桥接语义理解与运动执行之间的鸿沟。

### 隐式动作推理器（IAR）：潜在动作先验提取

IAR 从 VLM 的内部表征中提取隐式动作语义，作为补充的行为先验。其核心机制是通过可学习查询与降采样后的 KV 缓存进行交叉注意力，跨层聚合动作相关的隐式信息。

**降采样投影**：为降低计算开销，IAR 首先通过可学习的线性投影将 VLM 各层的 KV 缓存映射到低维空间：

$$Q_i' = Q_i W_Q^{(i)}, \quad K_i' = K_i^{\mathrm{VLM}} W_K^{(i)}, \quad V_i' = V_i^{\mathrm{VLM}} W_V^{(i)} \tag{7}$$

其中 $Q_i$ 为第 $i$ 层初始化的可学习查询矩阵，$W_Q^{(i)}, W_K^{(i)}, W_V^{(i)}$ 为对应的降采样投影权重。

**隐式语义提取**：对投影后的表示进行交叉注意力、池化和 MLP 投影，得到第 $i$ 层的隐式动作语义：

$$\boldsymbol{z}_i^{\mathrm{im}} = \mathbf{MLP}(\operatorname{Pool}(\operatorname{CrossAttn}(Q_i', K_i', V_i'))) \tag{8}$$

跨层聚合后的特征 $Z^{\mathrm{im}}$ 即为隐式动作空间引导 $g_{\mathrm{action}}^{\mathrm{im}}$。与 EAR 的显式轨迹引导不同，IAR 提供的是稠密的表示级先验，从 VLM 内部激活中捕捉行为模式。

### 动作引导预测头（AGP）：双路融合与动作生成

AGP 负责将显式与隐式动作引导融合，并条件化最终的降噪过程以生成可执行动作序列。

**双路交叉注意力**：动作查询 $Q_{\mathrm{action}}$ 分别与显式动作嵌入 $Z^{\mathrm{ex}}$（来自 EAR 的参考轨迹编码）和隐式动作特征 $Z^{\mathrm{im}}$ 进行交叉注意力：

$$S^{\mathrm{ex}} = \mathrm{CrossAttn}(Q_{\mathrm{action}}, Z^{\mathrm{ex}}, Z^{\mathrm{ex}}) \tag{9}$$

$$S^{\mathrm{im}} = \mathrm{CrossAttn}(Q_{\mathrm{action}}, Z^{\mathrm{im}}, Z^{\mathrm{im}}) \tag{10}$$

**引导融合**：将两条路径的注意力输出拼接后，经自注意力机制融合为统一的动作引导表示：

$$\bar{h} = \mathrm{Self\text{-}Attn}([S^{\mathrm{ex}}; S^{\mathrm{im}}]) \tag{11}$$

融合后的表示 $\bar{h}$ 馈入动作头 $\pi_{\theta}^{\mathrm{head}}$，通过流匹配生成去噪后的最终动作序列 $a_{t:t+H-1}$（$H=10$，动作偏移为 1）。

### 训练目标

整体训练损失为 EAR 与动作头两者的流匹配 MSE 损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_1 \mathcal{L}_{\pi_{\theta}^{\mathrm{ref}}} + \lambda_2 \mathcal{L}_{\pi_{\theta}^{\mathrm{head}}} \tag{12}$$

其中平衡因子 $\lambda_1 = \lambda_2 = 0.5$。训练时采用 teacher forcing 策略以保证稳定性，推理时切换至自条件模式。

## 实验与关键发现

### 核心发现与瓶颈突破

ACoT-VLA的设计动机源于VLA策略中一个关键的**语义-运动学差距**：现有方法在视觉-语言（输入）空间中推理，生成语言子目标或视觉目标图像作为中间引导，但这些引导与最终的低层动作执行之间缺乏直接联系，导致策略难以实现精确的动作生成。ACoT将思维链范式从语言或视觉空间**转移到动作空间**，直接生成结构化的粗粒度动作意图序列作为推理步骤，提供运动学上一致的动作引导。

实验在模拟和真实世界环境中系统验证了这一设计。与当前SOTA方法**π0.5**相比，ACoT-VLA在LIBERO基准上平均成功率提升**1.6%**（98.5% vs. 96.9%），在长程任务（LIBERO-Long）上表现尤为突出。在LIBERO-Plus的监督微调设置下，提升幅度达到**+12.3%**（88.0% vs. 75.7%），表明动作空间引导在分布外泛化场景中具有更强的鲁棒性。

### 主要基准结果

**LIBERO基准**（Table 1）：ACoT-VLA在四个子任务套件上均取得最优或次优结果——Spatial（99.4%）、Object（99.6%）、Goal（98.8%）、Long（96.0%），平均成功率98.5%。值得注意的是，多数对比方法（包括π0.5）冻结了LLM骨干（以⋄标示），ACoT-VLA在相同约束下仍保持领先，说明性能增益来自EAR/IAR引导机制而非额外的大模型调优。

**LIBERO-Plus基准**（Table 2）：该基准评估对相机、机器人初始状态、语言指令、光照、背景、噪声和布局变化的泛化能力。在零样本迁移设置下，ACoT-VLA在机器人初始状态变化（+3.2%）和语言变化（+4.2%）子项上显著优于π0.5，验证了动作空间引导对视觉-语言分布偏移的鲁棒性。在监督微调设置下，ACoT-VLA在所有7个子项上全面超越π0.5，平均提升12.3%。

**VLABench基准**（Table 3）：该基准衡量长期任务的意图理解（Intention Score, IS）和进度执行（Progress Score, PS）。ACoT-VLA分别达到63.5% IS和47.4% PS，较π0.5提升**+9.4%/+7.2%**，证明动作链式思维在需要多步推理的复杂任务中具有优势。

**Genie-Sim 3.0模拟→真实迁移**（Table 11）：在模拟环境中，ACoT-VLA达到84.2%成功率（π0.5为75.7%）；迁移到真实机器人后，成功率为82.9%（π0.5为77.5%），模拟-真实差距仅1.3%，表明EAR生成的粗参考轨迹具有良好的运动学可迁移性。

### 消融实验：显式与隐式引导的互补性

模块消融实验（Table 9，LIBERO-Plus监督微调设置）揭示了EAR和IAR的独立贡献与协同效应：

![[assets/figures/papers/paper_list_l2368_https_arxiv_org_abs_2601_11404/figures/013_Table_9.jpg]]
*Table 9: Module ablations on LIBERO-Plus benchmark. The performance is gradually improved with the addition of proposed methods. Note that models are directly optimized on LIBERO-Plus dataset, with the LLM backbone frozen during training*

- **仅EAR**：将成功率从基线75.7%提升至83.7%（+8.0%），证明显式粗参考轨迹是强有力的动作空间引导信号。
- **仅IAR**：将成功率提升至80.4%（+4.7%），表明从VLM内部表征中提取的隐式动作先验同样提供有效的补充信息。
- **EAR+IAR**：达到最高成功率84.1%（+8.4%），显式与隐式引导的协同增益超越了各自独立贡献的简单叠加，证实了二者在动作空间内的**互补性**——EAR提供运动学上可执行的轨迹级引导，IAR从VLM表征中提取稠密的行为先验，二者共同条件化下游动作头。

### 关键设计参数分析

**EAR参数量与去噪步数**（Table 10）：适度的EAR参数量（300M）获得最佳性能，过度参数化（500M）导致性能下降，暗示过大的EAR可能引入过拟合或优化困难。去噪步数从10步增加到20步带来小幅提升，但进一步增加收益递减。

**参考动作参数**（Table 5）：不同的参考动作配置（horizon、shift等）普遍带来性能提升，表明EAR对参数选择具有一定鲁棒性。论文固定参考动作horizon为15，动作策略输出horizon为10，shift分别为2和1。

**IAR的KV缓存交互策略**（Table 6）：跨层交叉注意力聚合优于仅使用单层或简单拼接，验证了从VLM多层表征中提取隐式动作语义的必要性。

### 效率与性能权衡

ACoT-VLA的推理模块引入了额外计算开销，延迟从91ms增加到112ms（Table 12）。这一21ms的增量在多数机器人平台上可接受，但对于资源极度受限的嵌入式系统可能构成瓶颈。论文将此列为已知局限，并提出了降低推理延迟的开放问题。

![[assets/figures/papers/paper_list_l2368_https_arxiv_org_abs_2601_11404/figures/016_Table_12.jpg]]
*Table 12: Ablation experiment on model efficiency and performance. Note that the evaluation protocol in LIBERO-Plus is Supervised Fine-Tuning*

### 失败模式与局限

1. **扁平动作表示的局限**：当前动作表示采用扁平的动作块（关节角/末端位姿序列），缺乏显式的几何结构或空间信息。这限制了ACoT在3D空间中进行更高层次推理（如物体中心协调、接触几何）的潜力。在需要精确空间推理的任务中，粗参考轨迹可能无法充分捕捉必要的几何约束。

2. **计算开销**：EAR和IAR模块增加了约23%的推理延迟。在需要高频控制（>50Hz）的场景中，这一开销可能影响实时性能。

3. **长程任务的参考轨迹质量**：虽然ACoT在LIBERO-Long上表现突出，但EAR生成的粗参考轨迹在极长程任务（horizon远超15步）中可能积累误差，需要进一步验证其扩展性。

### 实验公平性保障

所有仿真实验严格遵循官方训练分割，不引入额外数据；模型训练超参数统一（学习率、优化器、EMA），各任务仅在训练步数上适配；基准比较中LLM骨干多数被冻结，确保比较公平；采用teacher forcing stabilization保证训练稳定，推理时切换到自条件模式。

![[assets/figures/papers/paper_list_l2368_https_arxiv_org_abs_2601_11404/figures/003_Table_1.jpg]]
*Table 1: Comparison on the LIBERO benchmark. Our proposed approach is trained on the LIBERO dataset. ⋄ represents that the LLM backbone is frozen during training. All metrics are average success rates (%). The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2368_https_arxiv_org_abs_2601_11404/figures/004_Table_2.jpg]]
*Table 2: Comparison on the LIBERO-Plus benchmark. Methods under Zero-Shot Transfer are trained on LIBERO dataset and directly evaluated on LIBERO-Plus. Supervised Fine-Tuning denotes models trained on the LIBERO-Plus training set. An asterisk (*) denotes results reproduced by utilizing officially released checkpoints, while ⋄ represents that the LLM backbone is frozen during training. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2368_https_arxiv_org_abs_2601_11404/figures/005_Table_3.jpg]]
*Table 3: Comparison on the VLABench benchmark. IS and PS represent Intention score and Progress score, respectively. All models are trained for 60K steps. ⋄ indicates that the LLM backbone is frozen during training. The best results are highlighted in bold*

## 定位与知识库关联

### 1. 核心范式定位：从语言/视觉CoT到动作CoT

ACoT-VLA的方法学根基在于对VLA策略中“思维链”（Chain-of-Thought）范式的空间转移。现有工作可沿引导信号的空间维度划分为三个谱系：

- **语言空间CoT**：以 **OpenVLA**、**OpenVLA-OFT**、**VLA-Adapter**、**π0** 为代表，在文本令牌空间中预测子任务或语言描述作为中间推理步骤，为动作策略提供高层语义引导。这类引导与最终执行的动作块处于不同模态空间，存在固有的语义-运动学鸿沟。
- **视觉空间CoT**：以 **CoT-VLA**、**WorldVLA**、**DreamVLA**、**UniVLA** 为代表，通过生成目标图像或未来视觉帧作为动作策略的条件信号。视觉引导虽比语言更接近感知-运动循环，但图像到动作的映射仍需隐式跨越表示空间，引导信号的精确性和可执行性受限。
- **动作空间CoT（本文）**：ACoT-VLA首次将推理过程直接定义为动作空间内的结构化粗粒度意图序列，使引导信号与最终输出处于同构空间。这一范式转移的根本动机在于消除跨空间引导带来的信息损失——语言和视觉引导本质上是对动作需求的间接编码，而动作空间引导直接提供运动学上可执行的参考轨迹。

### 2. 与基线方法的技术关系

ACoT-VLA以 **π0.5** 作为主要构建基线和直接对标对象。π0.5本身采用流匹配（flow matching）在VLM特征基础上进行动作去噪，但不具备任何形式的动作空间引导机制。本文在保留π0.5的VLM骨干（SigLIP视觉编码器 + Gemma 2B LLM）和流匹配动作头的基础上，插入了三个关键模块，形成差异化贡献：

| 技术槽位 | π0.5 基线 | ACoT-VLA 改进 | 证据强度 |
|---------|----------|-------------|---------|
| 动作空间引导 | 无，直接预测动作 | EAR生成粗参考轨迹作为显式引导 | Table 9: +8.0% |
| 隐式动作先验 | 不使用VLM内部表征 | IAR跨层聚合隐式动作语义 | Table 9: +4.7% |
| 引导融合 | 无 | AGP双路交叉注意力融合 | Table 9: 组合达最优 |

**Diffusion Policy** 和 **Octo** 作为更早期的对比基线，分别代表纯扩散策略和通用机器人策略路线，均不涉及VLM推理或动作空间引导，与ACoT-VLA存在代际差异。

### 3. 知识库定位：贡献与增量

ACoT-VLA的核心知识贡献可概括为以下三个层面：

1. **范式层面**：首次将VLA策略的推理过程从语言/视觉空间迁移到动作空间，提出Action Chain-of-Thought概念。这一定位填补了现有CoT方法在机器人操作领域的一个空白——此前的工作（语言CoT、视觉CoT）均未触及动作空间内的结构化推理。

2. **机制层面**：揭示了显式引导（EAR生成的粗参考轨迹）与隐式引导（IAR从VLM表征中提取的潜在动作先验）的互补性。消融实验（Table 9）表明，单独添加EAR可将LIBERO-Plus成功率从75.7%提升至83.7%（+8.0%），单独添加IAR提升至80.4%（+4.7%），两者结合达到84.1%（+8.4%），验证了互补假说。

3. **工程层面**：提出了EAR的轻量化Transformer设计（300M参数获得最优性能，Table 10）、IAR的降采样KV缓存交叉注意力策略（Table 6对比了不同交互策略）、以及AGP的双路融合机制，为后续工作提供了可复用的模块化设计范式。

### 4. 适用边界与局限

**适用场景**：
- 多任务通用操作（LIBERO、LIBERO-Plus、VLABench、Genie-Sim 3.0等基准上的广泛验证）
- 长程任务（LIBERO-Long子集上表现突出）
- 零样本分布外泛化（LIBERO-Plus的Zero-Shot设置下对相机、机器人初始状态、语言指令等分布偏移具有鲁棒性）
- 仿真到真实迁移（Genie-Sim 3.0模拟到真实实验验证）

**已知局限**：
1. **推理延迟增加**：EAR和IAR模块引入了额外计算开销，推理延迟从π0.5的91ms增加到112ms（Table 12），增幅约23%。对于需要极高频率实时控制的机器人平台（如灵巧手、高速动态操作），这一延迟可能构成瓶颈。
2. **动作表示的几何贫乏**：当前动作表示采用扁平的动作块（关节角序列或末端位姿序列），缺乏显式的3D几何结构（如关键点、接触图、物体中心坐标）。这限制了ACoT在需要空间推理的任务（如物体间协调、接触规划）中进行更高层次推理的潜力。
3. **EAR参数敏感性**：Table 10显示，EAR参数量的增加并不单调提升性能——500M参数配置下成功率反而下降，表明粗参考轨迹的生成需要适度的模型容量，过度参数化可能引入过拟合或不稳定的运动学先验。

### 5. 开放问题与后续工作方向

1. **动作表示的几何丰富化**：能否将动作表示从扁平序列扩展为包含空间几何信息的形式（如3D关键点轨迹、物体中心运动、接触热图），使ACoT能在几何可解释的3D空间中推理？这将直接提升方法在复杂场景（如多物体协调、精细操作）中的适用性。

2. **推理效率优化**：如何在不显著损失性能的前提下降低推理延迟？可能的路径包括EAR/IAR的模型蒸馏、KV缓存的更激进降采样、或推理时自适应计算（简单任务跳过部分推理步骤）。

3. **异构多模态输入的稳健合成**：EAR需要从视觉观察和语言指令中合成高维动作线索，当前方法依赖于VLM骨干的表征质量。如何设计更稳健的合成机制，特别是在视觉输入退化（遮挡、光照变化）或语言指令模糊时仍能生成合理的参考轨迹，是一个待探索的问题。

4. **动作CoT的可解释性**：EAR生成的粗参考轨迹是否具有可解释的运动学语义（如“接近物体→抓取→提升”）？能否利用这一中间表示进行人机交互或故障诊断？当前工作未对此进行深入分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/ACoT_VLA_Action_Chain_of_Thought_for_Vision_Language_Action_Models.pdf]]

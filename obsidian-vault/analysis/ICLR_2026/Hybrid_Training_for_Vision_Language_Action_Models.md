---
title: "Hybrid Training for Vision-Language-Action Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Hybrid_Training_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: null
openreview_forum_id: IBJtOltTbx
aliases:
- HTH
- HTVLAM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "引入模态变量（modality variable），在训练时联合学习“直接动作预测”（act）和“思维链+动作”（think）等多种条件分布，使模型能够在推理时跳过思维生成、直接输出动作，同时保留思维训练带来的性能提升。"
primary_logic: "CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须产生中间思维；通过混合训练（HyT），单一模型能够学习到以模态为条件的多种动作分布，在保持快速推理的同时，达到与传统 CoT 方法相当甚至更优的任务性能。"
claims:
- "HyT 通过设置模态变量为 <act>，使模型直接输出动作，推理速度与标准 VLA 相同，无额外延迟。"
- "在 ClevrSkills 基准上，HyT 在所有数据集规模下性能均优于 ECoT 和 HiRobot，且显著高于标准 VLA。"
- "LIBERO 基准测试中，HyT 取得平均 93.7% 的成功率，优于对比方法。"
- "真实世界实验中，HyT 总体成功率达 63%±7，远高于 OpenVLA 的 41%±7，尤其在分布外任务上优势明显。"
---

# Hybrid Training for Vision-Language-Action Models

> [!tip] 核心洞察
> CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须产生中间思维；通过混合训练（HyT），单一模型能够学习到以模态为条件的多种动作分布，在保持快速推理的同时，达到与传统 CoT 方法相当甚至更优的任务性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉-语言-动作模型的混合训练 |
| 英文题名 | Hybrid Training for Vision-Language-Action Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IBJtOltTbx) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Hybrid Training (HyT) |
| Dataset | ClevrSkills (9 tasks, 3000 demos), LIBERO (4 suites, 100 episodes each), 真实机器人操作 (Real-world tasks, 26 trials total), 真实机器人 分布外任务 (OOD) |

> [!tip] 效果简介
> - ClevrSkills (9 tasks, 3000 demos) 上，成功率的聚合平均 (Aggregated Success Rate) 为 ≈0.54，对比 ECoT ≈0.51，变化 +0.03。
> - LIBERO (4 suites, 100 episodes each) 上，平均成功率 (Avg. Success Rate) 为 93.7%，对比 OFT (OpenVLA fine-tuned) 未见精确值，但明显低于 HyT，变化 显著提升，尤其 Goal/Long suite。
> - 真实机器人操作 (Real-world tasks, 26 trials total) 上，总体成功率 (Overall Success Rate) 为 63% ± 7，对比 OpenVLA 41% ± 7，变化 +22%。

## 概要

视觉-语言-动作（Vision-Language-Action, VLA）模型在引入思维链（Chain-of-Thought, CoT）后虽能提升任务性能，却面临一个关键瓶颈：生成冗长的中间思维文本会显著拖慢推理速度，降低动作执行频率，难以满足机器人部署的实时性要求。本文提出 **混合训练（Hybrid Training, HyT）** 框架，核心思路是在训练阶段联合学习多种条件动作分布，使单一模型在推理时能够跳过思维生成、直接输出动作，同时保留 CoT 训练带来的性能增益。

HyT 的关键机制是引入一个**模态变量（modality variable）** $m \in \{\text{<act>}, \text{<think>}, \text{<follow>}\}$，将动作分布分解为三个可独立采样的部分：直接动作预测（act）、先自生成思维再预测动作（think）、以及跟随给定指令预测动作（follow）。训练目标通过蒙特卡洛采样实现，以采样概率替代损失加权，推荐系数为 $w_a=0.25, w_\tau=0.5, w_f=0.25$。推理时只需将模态变量设为 `<act>`，模型即可直接输出动作，推理速度与标准 VLA 相同。

实验结果表明，HyT 在多个基准和真实场景下均取得显著提升：

- **ClevrSkills 基准**：HyT 在所有数据集规模（300–3000 个演示）下性能均优于 ECoT 和 HiRobot，且显著高于标准 VLA（Figure 3）。
- **LIBERO 基准**：HyT 取得平均 **93.7%** 的成功率，优于对比方法（Figure 5）。
- **真实世界实验**：HyT 总体成功率达 **63%±7**，远高于 OpenVLA 的 **41%±7**；在分布外任务上优势尤为突出，例如“将橡皮鸭放入绿碗”任务中 HyT 达 50%，而 OpenVLA 为 0%（Table 1）。

消融研究进一步揭示：`think` 分布在小数据量时贡献最大，而 `follow` 分布在大数据量时带来额外增益；在 `act` 和 `think` 两种推理模式下，HyT 模型的性能几乎无差异，说明 CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须生成中间思维。

**局限与待验证点**：当前模态变量在任务开始时设定后不再更改，未探索动态切换的潜力；实验环境以桌面操作为主，尚未在需要长期记忆或复杂抽象推理的任务上验证；思维标注依赖 oracle 求解器或启发式方法；真实世界实验的统计可靠性有限。HyT 与模型架构的耦合性也意味着其迁移到非 Transformer 模型族的效果尚未可知。



视觉-语言-动作模型（VLA）通过在视觉-语言模型基础上加入动作预测能力，使机器人能够根据视觉观察和语言指令直接生成控制命令。然而，标准 VLA 模型在面对复杂操作任务时性能有限，尤其是在需要多步推理的场景中表现不佳。

为提升 VLA 的推理能力，研究者引入了具身思维链（Embodied Chain-of-Thought, ECoT）方法。ECoT 在预测动作之前先生成中间推理文本（如子任务分解、物体关系描述），再基于这些思维输出动作。这种方法确实带来了显著的性能提升，但引入了一个关键瓶颈：**生成冗长的思维文本会大幅增加推理时间，降低动作执行频率，严重影响实际部署的实时性**。如 Figure 1 所示，ECoT 虽然将成功率提升至约 51%，但其推理频率从标准 VLA 的约 3 Hz 骤降至约 1 Hz，在需要快速响应的机器人操作场景中难以接受。

现有方法在性能与推理速度之间存在明显的权衡困境：
- **标准 VLA**：推理速度快（~3 Hz），但任务成功率较低（~47%）。
- **ECoT**：性能更高（~51%），但推理速度慢（~1 Hz），因为每次动作预测都必须生成完整的思维链。
- **HiRobot 等分层方法**：通过高层规划与低层执行分离来缓解延迟，但架构复杂度增加，且性能提升有限。

本文的核心洞察在于：**CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须产生中间思维**。这意味着，如果能在训练阶段让模型从思维中学习，而在推理阶段跳过思维生成、直接输出动作，就有可能在保持快速推理的同时获得 CoT 带来的性能提升。

基于这一洞察，本文提出 **混合训练（Hybrid Training, HyT）** 框架。HyT 通过引入一个**模态变量（modality variable）**，在训练时联合学习多种条件分布——包括直接动作预测（`act`）、自生成思维后动作预测（`think`）以及跟随给定指令的动作预测（`follow`）。这使得单一模型能够在推理时通过简单切换模态令牌来选择行为模式：设为 `<act>` 时直接输出动作，推理速度与标准 VLA 完全相同，无额外延迟。

如 Figure 1 所示，HyT 成功打破了性能与速度的权衡——在 ClevrSkills 基准上达到与 ECoT 相当甚至更优的成功率（~53%），同时保持标准 VLA 的 3 Hz 推理频率。这一特性使得 HyT 在真实机器人部署中具有显著的实用优势。



## 核心方法与创新机理

HyT 的核心创新在于引入**模态变量（modality variable）**作为条件开关，使单一 VLA 模型在训练时同时学习多种动作分布，从而在推理时无需生成中间思维即可获得思维训练带来的性能增益。这一设计直接解决了现有 CoT 方法的核心瓶颈：思维链虽能提升任务性能，但生成冗长的思维文本会显著降低推理频率，影响机器人部署的实时性（Figure 1）。

### 关键机制：以模态为条件的多分布学习

HyT 在输入端引入可训练嵌入的模态令牌 $m \in \{ \texttt{<act>}, \texttt{<think>}, \texttt{<follow>} \}$，将动作的条件分布分解为三个可独立采样的分量（Eq. 2）：

$$p(a_t | x_t, l) = \underbrace{p_\theta(a_t | x_t, l, m^a) p_\theta(m^a)}_{\text{act}} + \underbrace{p_\theta(a_t | x_t, l, \tau_t) p_\theta(\tau_t | x_t, l, m^\tau) p_\theta(m^\tau)}_{\text{think}} + \underbrace{p_\theta(a_t | x_t, \tau_t, m^f) p_\theta(m^f)}_{\text{follow}}$$

- **act 分布**：模型直接从观察和指令预测动作，跳过思维生成。
- **think 分布**：模型先生成思维链 $\tau_t$，再基于思维预测动作，保留 CoT 训练对内部表征的优化效果。
- **follow 分布**：模型接收给定的指令（如 oracle 思维）并执行，用于提升指令跟随能力。

训练时，通过蒙特卡洛采样近似上述联合分布，损失函数为三个负对数似然的加权和（Eq. 3）：

$$\min_\theta \mathcal{L}_{\text{hyt}}(\theta) = w_a \mathcal{L}_{\text{act}}(\theta) + w_\tau \mathcal{L}_{\text{think}}(\theta) + w_f \mathcal{L}_{\text{follow}}(\theta)$$

其中推荐系数为 $w_a = 0.25$、$w_\tau = 0.5$、$w_f = 0.25$，权重同时充当采样概率。消融实验表明，小数据场景下 think 分布贡献最大，大数据场景下 follow 分布带来额外收益（Figure 6）。

### 推理时的灵活切换

推理时，只需改变输入的模态令牌即可动态选择行为模式：

- 设置 $m^a = \texttt{<act>}$：模型直接输出动作，推理频率与标准 VLA 相同（~3 Hz），无额外延迟。
- 设置 $m^\tau = \texttt{<think>}$：模型生成思维后再输出动作，用于需要可解释性或复杂推理的场景。
- 设置 $m^f = \texttt{<follow>}$：模型跟随提供的指令执行动作。

关键发现是：**HyT 训练的模型在 act 和 think 模式下的性能几乎无差异**（Section 5.1），证明 CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须生成中间思维。这一发现从根本上改变了 VLA 领域对思维链必要性的认知。

### 与 baseline 的对比

| 对比维度 | 标准 VLA | ECoT | HyT |
|---------|---------|------|-----|
| 训练目标 | 直接动作预测 | 思维链+动作联合预测 | 多模态条件分布混合训练 |
| 推理速度 | 快（~3 Hz） | 慢（~1 Hz） | 快（~3 Hz，act 模式） |
| 性能 | 低 | 高 | 高（与 ECoT 相当或更优） |
| 推理灵活性 | 单一模式 | 固定思维模式 | 可动态切换三种模式 |

HyT 的关键优势在于打破了“性能提升必须牺牲推理速度”的 trade-off：在 ClevrSkills 基准上，HyT 在所有数据规模下均优于 ECoT 和 HiRobot（Figure 3）；在 LIBERO 基准上取得 93.7% 的平均成功率（Figure 5）；在真实世界实验中总体成功率达 63%±7，远超 OpenVLA 的 41%±7（Table 1），尤其在分布外任务上优势显著（如 banana in green bowl → rubber duck 任务中 HyT 50% vs OpenVLA 0%）。



![[assets/figures/papers/iclr26_0011_IBJtOltTbx_Hybrid_Training_for_Vision-Language-Action_Model/figures/002_Figure_2.jpg]]
*Figure 2: Hybrid Training (HyT) framework. Given a set of inputs, on the left, including a modality variable, the VLA model learns to conditionally generate a variety of outputs. Examples for the ‘think’ and ‘act’ conditional distributions are presented on the right*

HyT 框架的核心思想是将 VLA 模型的动作预测分布，显式地边缘化到一组可独立采样的条件分布上。如 Definition 4.1 所示，动作 $a_t$ 在观测 $x_t$ 和任务指令 $l$ 下的分布可写作：

$$p(a_t | x_t, l) = \sum_i \sum_j p_\theta(a_t, \tau^i, m^j | x_t, l) = \sum_i \sum_j p_\theta(a_t, \tau^i | x_t, l, m^j) p(m^j)$$

其中 $\tau$ 为思维 token，$m$ 为模态变量（modality variable）。这一边缘化将动作预测分解为三个可独立采样的条件分布（Eq. 2）：

$$p(a_t | x_t, l) = \underbrace{p_\theta(a_t | x_t, l, m^a) p_\theta(m^a)}_{\text{act}} + \underbrace{p_\theta(a_t | x_t, l, \tau_t) p_\theta(\tau_t | x_t, l, m^\tau) p_\theta(m^\tau)}_{\text{think}} + \underbrace{p_\theta(a_t | x_t, \tau_t, m^f) p_\theta(m^f)}_{\text{follow}}$$

- **act 分布**：模型直接根据观测和指令预测动作，完全跳过思维生成。
- **think 分布**：模型首先生成思维链 $\tau_t$，再基于思维链预测动作。
- **follow 分布**：模型接收外部给定的指令（如 oracle 提供的子任务描述），直接跟随指令预测动作。

训练时，HyT 通过蒙特卡洛采样近似上述边缘化目标，损失函数为三个负对数似然的加权和（Eq. 3）：

$$\min_\theta \mathcal{L}_{hyt}(\theta) = w_a \mathcal{L}_{act}(\theta) + w_\tau \mathcal{L}_{think}(\theta) + w_f \mathcal{L}_{follow}(\theta)$$

其中权重 $w_a$、$w_\tau$、$w_f$ 同时充当各分布的采样概率。默认系数设置为 $w_a=0.25$、$w_\tau=0.5$、$w_f=0.25$（Section 4.1）。消融实验表明，这一配置在不同数据量下均能取得较好的数据效率与最终性能平衡——小数据时 think 分布贡献尤为关键，大数据时 follow 分布则带来额外增益（Figure 6, Appendix A.1）。

### 推理模式切换

HyT 的核心优势在于推理时的灵活性。通过简单地设置输入的模态令牌，单一模型即可在三种行为模式间切换（Section 4.2）：
- 设置 $m^a = \texttt{<act>}$：模型直接输出动作，推理速度与标准 VLA 完全相同，无额外延迟。
- 设置 $m^\tau = \texttt{<think>}$：模型先生成思维链再输出动作，适合需要可解释性或调试的场景。
- 设置 $m^f = \texttt{<follow>}$：模型接收外部提供的指令序列并执行，可用于人机协作或分层控制。

### 模型架构与数据流

HyT 框架与标准 VLA 架构完全兼容，其 pipeline 包含四个核心模块（Figure 2）：

1. **视觉编码器**：将 224×224 的 RGB 图像转换为视觉 token 序列。
2. **语言编码与模态注入**：将任务描述文本与模态令牌（如 `<act>`、`<think>`、`<follow>`）转换为 token 序列，与视觉 token 拼接后输入骨干网络。
3. **骨干大语言模型**：基于 Transformer 的自回归解码器（实验中采用 PaliGemma-2 3B 或 OpenVLA），对多模态输入序列进行自回归生成。
4. **动作解码器**：从 LLM 输出中提取动作 token，转换为 7 维动作命令 $[\Delta x, \Delta \phi, \text{gripper}]$，支持离散或连续预测。

关键瓶颈在于：ECoT 等方法在推理时必须生成冗长的思维文本，导致动作执行频率显著下降。HyT 通过将思维生成限制在训练阶段，使推理时可直接使用 `<act>` 模式，从而在保持 CoT 训练带来的性能提升的同时，完全消除推理延迟（Figure 1）。实验进一步证实，HyT 训练后的模型在 act 和 think 模式下的性能几乎没有差异，说明 CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须产生中间思维（Section 5.1）。



### 问题瓶颈与核心思路

视觉-语言-动作（VLA）模型引入思维链（CoT）后，虽能提升任务成功率，但生成冗长的思维文本会显著降低推理频率（从约3 Hz降至1 Hz），在真实部署中难以满足实时性要求（见 Figure 1）。Hybrid Training (HyT) 的核心洞察是：CoT 训练的主要收益来源于模型内部表征的改进，而非推理时必须显式生成中间思维。因此，HyT 在训练时联合学习多种条件分布，使单一模型在推理时可跳过思维生成、直接输出动作，同时保留思维训练带来的性能提升。

### 关键模块

HyT 框架在标准 VLA 架构上引入一个可训练的**模态变量（modality variable）**，其余模块与现有 VLA 管线一致：

- **视觉编码器（Vision Encoder）**：将 224×224 的 RGB 图像转换为视觉 tokens，供后续 Transformer 处理。
- **语言编码与模态注入（Language & Modality Tokenizer）**：将任务描述文本和模态令牌（如 `<act>`、`<think>`、`<follow>`）转换为 token 序列，与视觉 token 拼接后输入骨干模型。
- **骨干大语言模型（LLM Backbone）**：基于 Transformer 的因果语言模型（PaliGemma-2 3B 或 OpenVLA），对多模态输入进行自回归解码。
- **动作解码器（Action Decoder）**：从 LLM 输出中提取动作 tokens，转换为 7 维动作命令 $[\Delta x, \Delta \phi, \text{gripper}]$，支持离散或连续预测。

模态变量 $m \in \{m^a, m^\tau, m^f\}$ 是 HyT 的核心创新，对应三种行为模式：
- $m^a = \texttt{<act>}$：直接预测动作
- $m^\tau = \texttt{<think>}$：先生成思维链，再预测动作
- $m^f = \texttt{<follow>}$：基于给定的指令思维预测动作

### 核心公式推导

**定义 4.1（混合训练）** HyT 通过对思维 token $\tau$ 和模态变量 $m$ 进行边缘化，定义动作的条件分布：

$$p(a_t \mid x_t, l) = \sum_i \sum_j p_\theta(a_t, \tau^i, m^j \mid x_t, l) = \sum_i \sum_j p_\theta(a_t, \tau^i \mid x_t, l, m^j) \, p(m^j)$$

其中 $x_t$ 为视觉输入，$l$ 为任务指令，$\theta$ 为模型参数。

**公式 2（混合条件动作分布）** 将上述边缘化分解为三个可独立采样的条件分布：

$$p(a_t \mid x_t, l) = \underbrace{p_\theta(a_t \mid x_t, l, m^a) \, p_\theta(m^a)}_{\text{act}} + \underbrace{p_\theta(a_t \mid x_t, l, \tau_t) \, p_\theta(\tau_t \mid x_t, l, m^\tau) \, p_\theta(m^\tau)}_{\text{think}} + \underbrace{p_\theta(a_t \mid x_t, \tau_t, m^f) \, p_\theta(m^f)}_{\text{follow}}$$

- **act 项**：直接动作预测，不生成思维
- **think 项**：模型自生成思维链 $\tau_t$，再基于思维预测动作
- **follow 项**：给定外部提供的指令思维（如 oracle 思维），直接预测动作

**公式 3（混合训练损失函数）** 训练目标为三个负对数似然损失的加权和，实际通过蒙特卡洛采样实现，权重充当采样概率：

$$\min_\theta \mathcal{L}_{\text{hyt}}(\theta) = w_a \mathcal{L}_{\text{act}}(\theta) + w_\tau \mathcal{L}_{\text{think}}(\theta) + w_f \mathcal{L}_{\text{follow}}(\theta)$$

默认系数设置为 $w_a = 0.25$，$w_\tau = 0.5$，$w_f = 0.25$。消融实验（Figure 6）表明：小数据量（300 demos）时 `think` 分布贡献最大；数据量增大后，包含 `follow` 分布的模型性能更优。

### 推理模式切换

训练完成后，模型可通过改变输入的模态令牌动态选择推理模式（Section 4.2）：
- 设置 $m^a = \texttt{<act>}$：模型直接输出动作，推理速度与标准 VLA 相同，无额外延迟
- 设置 $m^\tau = \texttt{<think>}$：模型先生成思维链，再输出动作
- 设置 $m^f = \texttt{<follow>}$：模型跟随给定的指令思维输出动作

关键发现：在 `act` 和 `think` 模式下，HyT 模型的性能几乎没有差异（Section 5.1），证明训练后的内部表征已足够强大，无需在推理时生成思维。这验证了核心假设——CoT 训练的收益源于表征改进，而非推理时的显式思维生成。



## 实验与关键发现

### 核心性能权衡：推理速度与任务成功率

VLA 模型引入思维链（CoT）后，性能提升的代价是推理延迟显著增加。ECoT 方法需要逐 token 生成冗长的思维文本，导致动作执行频率从标准 VLA 的约 3 Hz 骤降至约 1 Hz（Figure 1）。HyT 通过模态变量 $m^a = \langle act \rangle$ 使模型在推理时跳过思维生成、直接输出动作，推理速度与标准 VLA 完全相同，同时保持了接近甚至超越 ECoT 的任务成功率。这一权衡关系的打破是 HyT 最直接的实用优势。

![[assets/figures/papers/iclr26_0011_IBJtOltTbx_Hybrid_Training_for_Vision-Language-Action_Model/figures/001_Figure_1.jpg]]
*Figure 1: Hybrid Training (HyT) of VLAs increases the agent’s performance similarly to ECoT, but also maintains the same fast inference as standard VLAs. Performance refers to the ClevrSkills experiments (9 tasks, 3000 demos) in the Experiments section*

### 模拟基准：ClevrSkills 与 LIBERO

**ClevrSkills 基准**（9 个任务，涵盖放置、堆叠等操作）上，HyT 在所有数据集规模（300 至 3000 条演示）下均稳定优于 ECoT 和 HiRobot，且显著高于标准 VLA（Figure 3）。以 3000 条演示为例，HyT 聚合成功率约 0.54，ECoT 约 0.51，标准 VLA 约 0.47。误差带显示该优势具有统计显著性。在 Stack Tower 4 obj 等最困难任务上，HyT 的优势进一步扩大（Figure 8）。

![[assets/figures/papers/iclr26_0011_IBJtOltTbx_Hybrid_Training_for_Vision-Language-Action_Model/figures/004_Figure_3.jpg]]
*Figure 3: ClevrSkills benchmark Aggregated performance on 9 ClevrSkills environments (examples shown on the left). Shaded areas indicate standard errors*

**LIBERO 基准**（4 个任务套件，每套 100 个评估回合）上，HyT 取得了 93.7% 的平均成功率，优于对比方法（Figure 5）。尤其在 Goal 和 Long 等复杂套件上，HyT 的提升更为明显。值得注意的是，当基于 OpenVLA 预训练模型进行微调时，HyT 与基线 OFT 方法均接近性能饱和（整体成功率 95.3%±0.1），差异不再显著——这提示在强预训练基础上，HyT 的增益空间可能受限。

### 真实世界实验

真实机器人操作实验包含 4 个任务（如“将香蕉放入绿色碗中”、“红色方块放入棕色袋子”等），每个方法进行 26 次试验。HyT 总体成功率达 63%±7，远高于 OpenVLA 的 41%±7（Table 1）。在分布内任务上，HyT 为 72%±9 vs OpenVLA 52%±10；在分布外（OOD）任务上，HyT 的优势更为突出——例如“将橡胶鸭放入绿色碗中”任务，HyT 成功率为 50%，而 OpenVLA 完全失败（0%）。这一结果表明，HyT 训练所强化的内部表征具有良好的泛化能力，不完全依赖训练分布中的表面模式。

![[assets/figures/papers/iclr26_0011_IBJtOltTbx_Hybrid_Training_for_Vision-Language-Action_Model/figures/008_Table_1.jpg]]
*Table 1: Real-world experiments. Success rates with standard error on the real-world tasks (on the left). Additional details about experimental settings are provided in the Appendix*

### 推理模态分析：思维生成在测试时是否必要？

一个关键发现是：**经过 HyT 训练的模型，在 $\langle act \rangle$ 模式和 $\langle think \rangle$ 模式下的性能几乎没有差异**。这意味着 CoT 训练带来的性能收益主要来源于训练过程中对模型内部表征的改进，而非推理时必须显式生成中间思维。这一结论直接支持了 HyT 的核心设计理念——训练时利用思维，推理时跳过思维。

然而，当使用 oracle（最优求解器）生成的思维时，$\langle think \rangle$ 和 $\langle follow \rangle$ 模式的性能均有所提升（Figure 4）。这揭示了一个瓶颈：模型自生成的思维质量不足，限制了思维条件分布的潜力。当前思维标注依赖基于抓取/释放位置的启发式方法（详见附录 A.5），其质量上限受限于规则设计的完备性。

### 消融实验：训练系数与分布选择

**系数选择**：默认系数 $w_a=0.25$（act）、$w_\tau=0.5$（think）、$w_f=0.25$（follow）在不同数据量下均表现稳健（Figure 6）。小数据场景（300 条演示）下，$\langle think \rangle$ 分布的贡献尤为关键；随着数据量增大，包含 $\langle follow \rangle$ 分布的模型逐渐表现出优势。这提示数据效率与最终性能之间存在可调节的权衡。

![[assets/figures/papers/iclr26_0011_IBJtOltTbx_Hybrid_Training_for_Vision-Language-Action_Model/figures/010_Figure_6.jpg]]
*Figure 6: Ablating HyT coefficients used during training on the ClevrSkills benchmark*

**$\langle follow \rangle$ 分布的贡献**：在指令跟随基准上，包含 $w_f=0.25$ 的 HyT 变体显著优于仅使用 act 和 think 分布的变体（Figure 7），尤其在 Stack Tower 4 obj 等高难度任务上。$\langle follow \rangle$ 分布使模型学会“跟随给定的指令序列执行动作”，这一能力在需要精确执行多步规划的场景中具有独立价值。

![[assets/figures/papers/iclr26_0011_IBJtOltTbx_Hybrid_Training_for_Vision-Language-Action_Model/figures/011_Figure_7.jpg]]
*Figure 7: Ablation on the inclusion of the ‘follow’ distribution during HyT training in the instruction-following benchmark*

### 失败模式与局限性

1. **思维质量瓶颈**：自生成思维的质量限制了 $\langle think \rangle$ 和 $\langle follow \rangle$ 模式的性能上限。当前启发式思维提取方法无法覆盖复杂推理需求，自动化生成高质量思维的能力有待提升。
2. **模态静态设定**：模态变量在任务开始时设定后不再更改，未探索推理时动态切换模态（如从 act 切换到 think 以应对突发困难）的潜在收益。
3. **任务范围有限**：实验环境主要基于桌面操作和简单的放置/堆叠任务，尚未在需要长期记忆、空间规划或工具使用的任务上验证。
4. **真实世界规模不足**：真实实验仅涉及 4 个任务和 26 次试验，统计可靠性有限，OOD 任务的多样性也较窄。
5. **预训练饱和效应**：在强预训练模型（OpenVLA）上微调时，HyT 与基线的性能差异消失，提示方法增益可能与基础模型能力存在交互。

### 需要人工核实的内容

- Figure 5（LIBERO 基准）的完整数值对比（OFT 基线的精确成功率）在当前材料中未明确给出，仅提供了 HyT 的 93.7% 均值。
- Table 1 的完整表格内容未在可见材料中呈现，仅通过文字描述了关键数据点，建议核实完整的任务级成功率及标准误差。
- 消融实验（Figure 6、Figure 7）的具体数值和统计检验结果需要对照原文确认，当前仅依赖分析摘要中的定性描述。



## 定位与知识库关联

### 与基线方法的结构性对比

HyT 的核心贡献在于引入**模态变量（modality variable）**作为条件开关，使单一 VLA 模型能够学习多种动作分布，从而在推理时绕过思维链生成，直接输出动作。这一设计直接回应了 ECoT 和 HiRobot 等方法的根本瓶颈：CoT 训练虽能提升性能，但推理时必须生成冗长的思维文本，导致动作执行频率大幅下降（Figure 1 中 ECoT 约 1 Hz，而标准 VLA 约 3 Hz）。

与三类基线方法的结构性差异如下：

- **Standard VLA**：直接从观察和指令预测动作 $p(a_t | x_t, l)$，推理快但缺乏思维训练带来的表征改进。HyT 保留了其快速推理路径（设置模态变量为 `<act>`），同时通过混合训练注入思维学习的收益。

- **ECoT（Embodied CoT）**：训练时学习联合分布 $p(a_t, \tau_t | x_t, l)$，推理时必须先生成思维链 $\tau_t$ 再预测动作。HyT 将这一过程解耦为可选的 `think` 条件分布，推理时可通过模态变量跳过思维生成。实验表明，HyT 在 `act` 和 `think` 两种推理模式下性能几乎无差异（Section 5.1），说明 CoT 训练的收益主要来自内部表征改进，而非推理时的中间文本生成。

- **HiRobot**：分层架构中高层生成子任务规划、低层执行动作，本质上是固定层次结构。HyT 的 `follow` 分布提供了更灵活的指令跟随能力——模型可直接接收给定的子任务描述（如 oracle 思维）并据此生成动作，无需依赖固定的分层架构。Figure 4 显示，使用 oracle 思维时 HyT 在 `follow` 模式下性能进一步提升，验证了这一灵活性。

- **OFT（OpenVLA fine-tuned）**：基于 OpenVLA 的微调方法。HyT 可与 OFT 结合使用（Section 5.2），在 LIBERO 的 Goal 和 Long 等复杂任务套件上进一步提升了性能（Figure 5）。真实世界实验中，HyT 总体成功率 63%±7 显著优于 OpenVLA 的 41%±7（Table 1），尤其在分布外任务上差距更为悬殊（如 rubber duck in green bowl: HyT 50% vs OpenVLA 0%）。

### 适用边界

HyT 的有效性已在以下条件下验证：

- **任务类型**：桌面操作任务，包括物体放置、堆叠和简单指令跟随（ClevrSkills 9 个环境、LIBERO 4 个任务套件、4 个真实世界任务）。
- **模型架构**：基于 Transformer 的因果语言模型骨干（PaliGemma-2 3B 和 OpenVLA），视觉输入为 224×224 RGB 图像。
- **动作空间**：7 维动作命令 $[\Delta x, \Delta \phi, \text{gripper}]$，支持离散化和连续预测（L1 head）。
- **思维标注来源**：依赖 oracle 求解器或启发式方法（如基于抓取/释放位置的子任务提取，Appendix A.5），尚未验证自动化思维生成的质量。
- **模态切换时机**：当前仅在任务开始时设定模态令牌，推理过程中不再更改。

以下场景超出已验证范围，需谨慎推广：

- 需要长期记忆或复杂抽象推理的任务（如空间规划、工具使用）。
- 非 Transformer 架构的 VLA 模型。
- 动态环境变化需要推理时自适应切换模态的场景。
- 大规模预训练 VLA 上的应用（LIBERO 上 OpenVLA 预训练模型微调时出现饱和现象，Table 2 显示两种方法均达到 95.3%±0.1，性能无差异）。

### 局限与开放问题

**已识别的局限**：

1. **模态变量静态设定**：推理过程中模态令牌固定不变，未探索动态切换（如从 `act` 切换到 `think`）对复杂环境适应的潜在增益。
2. **思维标注依赖**：高质量思维依赖 oracle 或启发式规则，自动化生成方法尚未验证。HyT 的一个优势是思维不必覆盖全数据集（Section 6），但思维质量对训练效果的影响程度仍需量化。
3. **任务覆盖面窄**：真实世界实验仅 4 个任务、26 次试验，统计可靠性有限。模拟实验集中在桌面操作，未涉及导航、移动操作等更广泛的具身任务。
4. **架构耦合**：当前方法在 PaliGemma-2 和 OpenVLA 上验证，迁移到其他模型族的效果未知。
5. **预训练饱和**：在 OpenVLA 预训练模型上微调时，HyT 与基线均接近性能上限（95.3%），方法增益被掩盖。

**待探索的开放问题**：

- **动态模态切换**：推理时根据环境不确定性动态选择 `act` 或 `think` 模式，能否在不显著牺牲速度的前提下提升鲁棒性？
- **复杂推理任务**：对于需要多步规划或因果推理的任务，测试时生成思维是否仍然必要？当前“act 和 think 模式性能无差异”的结论是否在更复杂场景下失效？
- **自动化思维提取**：能否通过强化学习或自监督方法从成功轨迹中自动提取有用思维，减少对 oracle 的依赖？
- **跨模态推广**：HyT 的模态条件化思想能否扩展到力觉、触觉、听觉等其他具身输入模态？
- **大规模预训练**：在大规模预训练 VLA 上应用 HyT 是否会进一步激发性能，还是存在饱和现象？LIBERO 上的饱和结果（Table 2）需要更大规模基准验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/Hybrid_Training_for_Vision_Language_Action_Models.pdf]]

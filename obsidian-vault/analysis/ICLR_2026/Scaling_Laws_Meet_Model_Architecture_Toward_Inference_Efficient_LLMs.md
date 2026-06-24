---
title: "Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scaling_Laws_Meet_Model_Architecture_Toward_Inference_Efficient_LLMs.pdf
aliases:
- CSL
- SLMMATIEL
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: |
  将隐藏大小、MLP与注意力参数比和GQA等架构因素纳入Chinchilla缩放律，通过条件校准与局部搜索在损失约束下优化推理吞吐量。
primary_logic: |
  先训练不同规模和架构的小模型拟合基础Chinchilla最优损失，再用乘法或加法条件项刻画隐藏大小和MLP/attention参数比的U形损失影响，最后在损失阈值内搜索推理高效架构并对GQA做离散局部调优。
claims:
- "隐藏大小和MLP与注意力参数比与训练损失呈U形关系，存在内部最优架构配置。"
- "GQA对损失的影响非连续且高度波动，因此本文采用枚举可行值和早停的局部搜索。"
- "Panda-1B和Panda-3B在9个下游任务平均准确率上分别达到57.0和62.5，高于对应LLaMA-3.2基线。"
---

# Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs

> [!tip] 核心洞察
> 隐藏大小和MLP与注意力参数比与训练损失呈U形关系，存在内部最优值；GQA对损失的影响非连续且高度波动，因此通过局部搜索而非连续缩放律来调优。基于此，本文提出条件缩放律，将架构因素纳入Chinchilla框架，实现推理高效且准确的模型搜索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 缩放律遇见模型架构：迈向推理高效的大语言模型 |
| 英文题名 | Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0TmVqOpBbK) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | 条件缩放律（Conditional Scaling Law） |
| Dataset | 9个下游任务平均准确率, 推理吞吐量（A100, vLLM, 4k/1k） |

> [!tip] 效果简介
> - 9个下游任务平均准确率 上，Avg. accuracy 为 57.0 (Panda-1B)，对比 54.9 (LLaMA-3.2-1B)，变化 +2.1%。
> - 9个下游任务平均准确率 上，Avg. accuracy 为 62.5 (Panda-3B)，对比 61.9 (LLaMA-3.2-3B)，变化 +0.6%。
> - 推理吞吐量（A100, vLLM, 4k/1k） 上，tokens/s 为 Surefire-1B > LLaMA-3.2-1B，对比 LLaMA-3.2-1B，变化 Surefire模型持续更高（具体值见图7）。

## 概述

本文提出**条件缩放律（Conditional Scaling Law）**，将架构因素（隐藏大小、MLP与注意力参数比、分组查询注意力）纳入Chinchilla缩放律框架，以同时优化训练损失和推理效率。现有缩放律仅关注训练损失，忽略了大规模部署LLM时的主导开销——推理成本。本文通过训练超过200个模型（参数规模从80M到3B，训练token从8B到100B），系统建模了架构因素对训练损失和推理吞吐量的影响。实验表明，在相同训练预算下，优化后的架构相比LLaMA-3.2实现了高达2.1%的准确率提升和42%的推理吞吐量提升。

## 背景与动机

现有缩放律（如Chinchilla scaling law, Hoffmann et al., 2022）仅考虑参数数量N和训练token数D，忽略了架构因素对推理效率的影响。然而，推理成本是大规模部署LLM时的主导开销。此外，架构因素（隐藏大小、MLP与注意力参数比、分组查询注意力）对推理效率和准确率的影响未被系统建模。

先前考虑推理成本的缩放律（Sardana et al., 2023）需要估计模型整个生命周期的总生成token数，不实用。先前扩展Chinchilla的架构缩放律（Bian et al., 2025）仅考虑宽高比（隐藏大小/层数），且缺乏通用框架。

本文的核心动机是：在固定参数预算下，通过调整隐藏大小d_model、MLP与注意力参数比r_mlp/attn和GQA值，同时优化推理吞吐量和训练损失。

## 核心创新

本文的核心创新包括：

1. **条件缩放律**：提出一种两步骤方法，将架构因素纳入Chinchilla框架。首先从Chinchilla缩放律获得最优损失L_opt(N,D)作为参考点，然后校准架构变体的损失相对于该参考点。

2. **U形关系发现**：发现隐藏大小和MLP与注意力参数比与训练损失呈U形关系，存在内部最优值。Figure 4和Figure 5分别展示了损失与隐藏大小、损失与MLP与注意力参数比之间一致的U形曲线。

3. **GQA局部搜索**：由于GQA对损失的影响非连续且高度波动（Figure 24），本文通过局部搜索（枚举可行值+早停）而非连续缩放律来调优GQA。

4. **推理高效准确模型搜索框架**：在损失约束下最大化推理效率，得到最优d_model和r_mlp/attn，然后通过局部搜索优化GQA。

## 整体框架

本文的整体框架包含以下步骤：

1. **训练小模型拟合Chinchilla缩放律**：获得最优损失L_opt(N,D)作为参考点。
2. **条件校准**：使用乘法或加法校准公式，建模隐藏大小和MLP与注意力参数比对损失的U形影响。
3. **求解约束优化问题**：在损失约束下最大化推理效率，得到最优d_model和r_mlp/attn。
4. **GQA局部搜索**：枚举可行GQA值，应用早停以最大化推理效率。

Figure 1展示了推理吞吐量和缩放律预测的训练损失等高线，随隐藏大小和MLP与注意力参数比变化。Figure 2比较了Qwen2.5-1.5B和Qwen3-0.6B的推理吞吐量，说明架构因素的重要性。

## 核心模块与公式推导

## 1 Chinchilla缩放律

模型损失作为参数数量N和训练token数D的函数：

$$L(N, D) = E + \frac{A}{N^\alpha} + \frac{B}{D^\beta}$$

其中A、B、E、α、β为可学习参数。

## 2 注意力参数缩放关系

注意力参数数量与隐藏大小的平方成正比：

$$4 d_{\mathrm{model}}^2 \propto N_{\mathrm{attn}} = N_{\mathrm{non-embed}} \times \frac{r}{r+1}$$

## 3 乘法条件缩放律

乘法校准：架构变体的损失等于最优损失乘以隐藏大小项和MLP与注意力参数比项的乘积，假设两者对损失的影响可分离：

$$L(d/\sqrt{N}, r \mid N, D) = (a_0 + a_1 \log(\frac{d}{\sqrt{N}}) + a_2 \frac{\sqrt{N}}{d}) \cdot (b_0 + b_1 \log r + \frac{b_2}{r}) \cdot L_{\mathrm{opt}}$$

## 4 加法条件缩放律

加法校准：架构变体的损失等于最优损失加上隐藏大小项和MLP与注意力参数比项的和：

$$L(d/\sqrt{N}, r \mid N, D) = (a_0 + a_1 \log(\frac{d}{\sqrt{N}}) + a_2 \frac{\sqrt{N}}{d}) + (b_1 \log r + \frac{b_2}{r}) + L_{\mathrm{opt}}$$

## 5 推理高效准确模型搜索的优化问题

在损失不超过阈值L_t的约束下，最大化推理效率I_N(P)：

$$\mathrm{argmax}_P I_N(P), \qquad \mathrm{s.t.} \quad L(P \mid N, D) \leq L_t$$

## 6 总推理非嵌入FLOPs

总推理非嵌入FLOPs包括QKV投影、输出投影、注意力掩码和前馈网络的计算：

$$\mathrm{Total-FLOPs} = n_{\mathrm{layers}} (2 d_{\mathrm{model}} d_q + 2 d_{\mathrm{model}} d_{kv} + 2 d_{\mathrm{model}} d_{kv} + 2 d_{\mathrm{model}} d_q + 2 T d_q + 3 \cdot 2 d_{\mathrm{model}} f_{\mathrm{size}})$$

简化后的总推理FLOPs：

$$\mathrm{Total-FLOPs} = 2 P_{\mathrm{non-emb}} + 2 n_{\mathrm{layers}} T d_q$$

## 实验与分析

## 1 主要结果

Table 1展示了大规模模型结果：

| 模型 | 损失 | 平均准确率（9个下游任务） |
|------|------|--------------------------|
| LLaMA-3.2-1B | 2.803 | 54.9 |
| Panda-1B | 2.782 | 57.0 |
| Surefire-1B | 2.804 | 55.4 |
| LLaMA-3.2-3B | 2.625 | 61.9 |
| Panda-3B | 2.619 | 62.5 |
| Surefire-3B | 2.620 | 62.6 |

Panda-1B相比LLaMA-3.2-1B实现了2.1%的准确率提升。Surefire模型在推理吞吐量方面持续优于LLaMA-3.2基线，最高达42%（Figure 7）。

Table 6展示了推理吞吐量的详细结果：

| 模型 | 框架 | GPU | 吞吐量（tokens/s） |
|------|------|-----|-------------------|
| LLaMA-3.2-1B | SGLang | H200 | 8608.57 |
| Surefire-1B | SGLang | H200 | 12645.55 |
| LLaMA-3.2-3B | SGLang | H200 | 4183.09 |
| Surefire-3B | SGLang | H200 | 4877.16 |

Surefire-1B在H200 GPU上使用SGLang框架实现了46.9%的吞吐量提升。

## 2 消融实验

**隐藏大小和MLP与注意力参数比的U形关系**：Figure 4和Figure 5显示，在80M、145M、297M模型变体中，训练损失与d_model/√N和r_mlp/attn均呈现一致的U形曲线。

**GQA的非连续影响**：Figure 24显示，GQA对损失的影响在不同模型规模下变化显著，不适合纳入连续缩放律。

**校准方法比较**：乘法校准和加法校准在MSE和Spearman相关性上表现几乎相同（Figure 25）。联合非可分校准（joint non-separable）的MSE更高、Spearman更低，性能劣于乘法校准（Figure 26）。

**异常值影响**：排除极端异常值（r_mlp/attn < 0.5 或 > 5）可改善缩放律拟合（Figure 25）。

**拟合数据策略**：仅使用1B数据拟合缩放律，预测3B模型损失时MSE更低、Spearman更高（Figure 8）。

## 3 公平性说明

- 所有模型使用相同的训练数据Dolma-v1.7。
- 训练超参数主要遵循先前工作（如LLaMA-3.2），并针对不同模型规模进行调优。
- 推理效率评估使用vLLM和SGLang框架，在相同硬件（NVIDIA A100 40GB或H200）上以相同输入/输出长度（4096/1024 tokens）进行，取5次运行平均值。
- 下游任务评估采用零样本设置，使用lm-eval-harness框架，涵盖9个标准基准：ARC-Easy、ARC-Challenge、LAMBADA、HellaSwag、OpenBookQA、PIQA、SciQ、WinoGrande、CoQA。

## 方法谱系与知识库定位

本文的方法谱系定位如下：

- **基础缩放律**：Chinchilla scaling law (Hoffmann et al., 2022) —— 仅考虑参数N和训练token D，忽略架构因素。
- **推理感知缩放律**：Sardana et al. (2023) —— 考虑推理成本，但需要估计模型整个生命周期的总生成token数，不实用。
- **架构感知缩放律**：Bian et al. (2025) —— 扩展Chinchilla的架构缩放律，但仅考虑宽高比（隐藏大小/层数），且缺乏通用框架。
- **本文方法**：条件缩放律 —— 将隐藏大小、MLP与注意力参数比、GQA纳入Chinchilla框架，实现推理高效且准确的模型搜索。

本文的局限性包括：
- 固定了层数，未研究层数（宽高比）对推理效率和准确率的影响。
- 条件缩放律假设隐藏大小和MLP与注意力参数比对损失的影响是可分离的。
- GQA对损失的影响非连续且高度波动，本文仅通过局部搜索调优，缺乏理论预测模型。
- 缩放律拟合基于80M至1B的小模型，外推至3B时可能存在偏差。
- 本文仅研究稠密Transformer模型，MoE架构的初步分析（Figure 27）表明类似趋势，但未系统纳入缩放律。
- 推理效率评估仅考虑单GPU场景。
- 下游任务评估限于9个标准基准。

## 整体框架

![[assets/figures/papers/iclr26_0002_0TmVqOpBbK_Scaling_Laws_Meet_Model_Architecture_Toward_Infe/figures/001_Figure_1.jpg]]

## 实验与分析

### 补充图表

![[assets/figures/papers/iclr26_0002_0TmVqOpBbK_Scaling_Laws_Meet_Model_Architecture_Toward_Infe/figures/015_Table_1.jpg]]
*Table 1: Large-Scale Model Results. We evaluate the scaling laws at 1B and 3B scales by training Panda-1B, Surefire-1B, and Panda-3B, and compare them with LLaMA-3.2-1B and LLaMA-3.2- 3B, respectively. The Avg. column reports the mean accuracy across the nine downstream tasks. Panda-1B and 3B are trained using the optimal architectural configurations predicted by our scaling laws, whereas Surefire-1B and 3B satisfy the loss constraint in Eq. (4) and achieve Pareto optimality.*

![[assets/figures/papers/iclr26_0002_0TmVqOpBbK_Scaling_Laws_Meet_Model_Architecture_Toward_Infe/figures/019_Table_2.jpg]]
*Table 2: 3B Model Ablations. We assess the robustness of fitting-data strategy at 3B scale by training Panda-3B (using 80M, 145M, and 297M data) and Panda-3B◦ (using only on 1B data), and compare both with LLaMA-3.2-3B. Avg. denotes mean accuracy across nine downstream tasks.*

![[assets/figures/papers/iclr26_0002_0TmVqOpBbK_Scaling_Laws_Meet_Model_Architecture_Toward_Infe/figures/022_Table_3.jpg]]
*Table 3: Open-Weighted Model Architectures. We list the architectural configurations of all models used in this paper. $n _ { \mathrm { l a y e r s } }$ is the number of layers, $d _ { \mathrm { m o d e l } }$ is the hidden size, $n _ { \mathrm { h e a d s } }$ is the number of attention heads, and $f _ { \mathrm { s i z e } }$ is the intermediate size.

![[assets/figures/papers/iclr26_0002_0TmVqOpBbK_Scaling_Laws_Meet_Model_Architecture_Toward_Infe/figures/023_Table_4.jpg]]
*Table 4: Model Architectures. We list the architectural configurations of all models trained in this paper. $N _ { \mathrm { n o n - e m b e d } }$ is the total number of non-embedding parameters, $n _ { \mathrm { l a y e r s } }$ is the number of layers, $d _ { \mathrm { m o d e l } }$ is the hidden size, $n _ { \mathrm { h e a d s } }$ is the number of attention heads, $f _ { \mathrm { s i z e } }$ is the intermediate size, and $r _ { \mathrm { m l p / a t t n } }$ is the MLP-to-attention ratio.

![[assets/figures/papers/iclr26_0002_0TmVqOpBbK_Scaling_Laws_Meet_Model_Architecture_Toward_Infe/figures/027_Table_8.jpg]]

## 原文 PDF

![[paperPDFs/ICLR_2026/Scaling_Laws_Meet_Model_Architecture_Toward_Inference_Efficient_LLMs.pdf]]

---
title: "Boomerang Distillation Enables Zero-Shot Model Size Interpolation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Boomerang_Distillation_Enables_Zero_Shot_Model_Size_Interpolation.pdf
project_link: null
code_link: https://github.com/dcml-lab/boomerang-distillation
aliases:
- BD
- BDEZSMSI
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "Boomerang Distillation trains a layer-pruned student with CE, KL, and cosine alignment so teacher blocks can be patched back zero-shot."
primary_logic: "It initializes each student layer from a teacher block, distills the student to align hidden states with block outputs, then replaces selected student layers with teacher layer blocks to interpolate model sizes."
claims:
- "Teacher-initialized students plus cosine alignment enable smooth zero-shot size interpolation."
- "Student patching produces intermediate models without training each size separately."
- "The note reports large FLOP savings over independently distilling every intermediate model."
---

# Boomerang Distillation Enables Zero-Shot Model Size Interpolation

> [!tip] 核心洞察
> 在教师权重初始化和对齐蒸馏（特别是余弦距离损失）的条件下，将教师层块插回蒸馏后的学生模型可以零样本地生成性能平滑插值的中间尺寸模型，且无需额外训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 回旋镖蒸馏：零样本模型尺寸插值 |
| 英文题名 | Boomerang Distillation Enables Zero-Shot Model Size Interpolation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=4ZU8v4s3IR) · [GitHub](https://github.com/dcml-lab/boomerang-distillation) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Boomerang Distillation |
| Dataset | 10个分类数据集（平均）, 3个生成数据集（平均）, WikiText, Qwen3-4B-Base 教师模型 |

> [!tip] 效果简介
> - 10个分类数据集（平均） 上，分类准确率 为 平滑插值，在中间尺寸上优于剪枝基线，对比 Naive Layer Pruning: 在小于4B参数时显著下降，变化 显著优于。
> - 3个生成数据集（平均） 上，精确匹配准确率 为 平滑插值，在较小模型上保持较高生成性能，对比 Naive Layer Pruning: 生成性能快速下降，变化 显著优于。
> - WikiText 上，困惑度 为 在学生和教师之间平滑插值，对比 Naive Layer Pruning: 随层数减少困惑度急剧上升，变化 显著优于。

## 概要

本文提出 **Boomerang Distillation**（回旋镖蒸馏），一种能够零样本（zero-shot）生成任意中间尺寸语言模型的高效方法。核心思想是：首先将大型教师模型通过层剪枝（layer pruning）初始化为一个小型学生模型，然后使用包含余弦距离对齐损失的蒸馏目标训练该学生模型；训练完成后，通过将学生层替换为对应的教师层块（student patching），无需任何额外训练即可生成一系列尺寸和性能平滑插值的中间模型。实验表明，该方法在多个模型族（Qwen3、Pythia、Llama-3.2）上均有效，相比朴素层剪枝和随机初始化蒸馏基线显著更优，且计算开销仅为独立蒸馏每个中间模型的 1/14.53 至 1/19.17。



现有方法为每个模型尺寸独立训练，成本高昂且只能提供粗粒度的尺寸选项，无法在部署时灵活适应多样化的硬件约束。例如，标准知识蒸馏（Hinton et al., 2015）和模型族构建方法（Muralidharan et al., 2024）需要为每个目标尺寸单独训练一个模型。层剪枝方法（如 LaCo、ShortGPT）虽然可以快速生成小模型，但性能随层数减少急剧下降，尤其在生成任务上。本文旨在解决这一瓶颈：**如何在不重新训练的情况下，从单一训练过程获得任意中间尺寸的高性能模型？**



## 核心方法与创新机理

Boomerang Distillation 的核心洞察是：在教师权重初始化和对齐蒸馏（特别是余弦距离损失）的条件下，将教师层块插回蒸馏后的学生模型可以零样本地生成性能平滑插值的中间尺寸模型，且无需额外训练。具体创新点包括：

1. **学生初始化**：通过层剪枝从教师模型初始化学生模型，保持隐藏维度一致。
2. **对齐蒸馏**：在标准知识蒸馏损失基础上，加入每层余弦距离对齐损失，确保学生层输出接近对应教师块输出。
3. **学生修补（Student Patching）**：训练后，将学生层替换为对应的教师层块，零样本生成中间尺寸模型。




![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_4ZU8v4s3IR_Boomeran/figures/001_Figure_1.jpg]]
*Figure 1: Figure 1: Overview of boomerang distillation. ➀ In this example, the student model is initialized by dropping layers from the pretrained teacher model. ➁ The teacher model is distilled into the student model with cross-entropy loss, knowledge distillation loss, and cosine distance loss (Equation 1). ➂ After training the student model, a block of teacher layers corresponding to a student layer is inserted back into the model to get the zero-shot interpolated model.*

Boomerang Distillation 包含三个步骤（Figure 1）：

1. **学生初始化（Student Initialization）**：将教师模型的 N 个 Transformer 层划分为 M 个连续块，取每块第一层初始化学生模型，保持嵌入层和 LM 头不变。
2. **知识蒸馏（Knowledge Distillation）**：使用交叉熵、KL 散度和余弦距离损失的联合目标训练学生模型，使其输出和隐藏状态与教师对齐。
3. **学生修补（Student Patching）**：将蒸馏后的学生层替换为对应的教师层块，零样本生成中间尺寸模型；嵌入层和 LM 头根据首尾层来源选择。



### 5.1 学生初始化

将教师模型的 N 层划分为 M 个连续块，每个块包含 ℓ_i 到 ℓ_{i+1}-1 层。学生模型初始化为：

$$\pmb{\theta}_S^{(i)} = \pmb{\theta}_T^{(\ell_i)}, \quad i = 1, \dots, M$$

嵌入层和 LM 头直接继承教师：$\pmb{\theta}_S^E = \pmb{\theta}_T^E$, $\pmb{\theta}_S^D = \pmb{\theta}_T^D$。

### 5.2 知识蒸馏目标

学生模型训练的总损失为（Equation 1）：

$$\mathcal{L}(x, \pmb{\theta}_S) = \mathcal{L}_{\mathrm{CE}}(x_j \mid x_{<j}; \pmb{\theta}_S) + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}(x_{<j}; \pmb{\theta}_S) + \lambda_{\mathrm{cos}} \sum_{i=1}^M \mathcal{L}_{\mathrm{cos}}^{(i)}(x_{<j}; \pmb{\theta}_S)$$

其中：

- **交叉熵损失** $\mathcal{L}_{\mathrm{CE}}$：标准语言建模损失。
- **KL 散度损失**（知识蒸馏损失）：

$$\mathcal{L}_{\mathrm{KL}}(\boldsymbol{x}_{<j}; \boldsymbol{\theta}_S) = \boldsymbol{\tau}^2 \cdot \mathrm{KL}\big(\mathrm{softmax}(\boldsymbol{z}_j^T / \boldsymbol{\tau}) ~ \lVert ~ \mathrm{softmax}(\boldsymbol{z}_j^S / \boldsymbol{\tau})\big)$$

温度 τ 控制软化程度。

- **余弦距离损失**（对齐损失）：

$$\mathcal{L}_{\mathrm{cos}}^{(i)}(x_{<j}; \boldsymbol{\theta}_S) = 1 - \frac{\boldsymbol{x}_j^{(S,i)} \cdot \boldsymbol{x}_j^{(T,l_{i+1}-1)}}{||\boldsymbol{x}_j^{(S,i)}|| ~ ||\boldsymbol{x}_j^{(T,l_{i+1}-1)}||}$$

鼓励学生第 i 层隐藏状态接近对应教师块输出（第 ℓ_{i+1}-1 层）的隐藏状态。

### 5.3 学生修补

将第 i 个学生层替换为对应的教师层块：

$$b^{(i)} = (\theta_T^{(\ell_i)}, \dots, \theta_T^{(\ell_{i+1}-1)})$$

得到插值模型：

$$(\theta_S^{(1)}, \dots, \theta_S^{(i-1)}, b^{(i)}, \theta_S^{(i+1)}, \dots, \theta_S^{(M)})$$

嵌入层和 LM 头根据首尾层来源选择：若首层来自学生，则使用学生嵌入层；若首层来自教师，则使用教师嵌入层；LM 头同理。



## 实验与关键发现


### 6.1 主要结果

**Table 1** 列出了所有使用的教师和学生模型的参数规模。**Table 2** 列出了训练超参数。


![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_4ZU8v4s3IR_Boomeran/figures/012_Table_1.jpg]]
*Table 1: Table 1: The sizes of the initialized student models after pruning the layers from the teacher model. We note that the Pythia models do not employ weight tying, so their train and inference parameters are equivalent. On the other hand, the Qwen and Llama models weight tie their embedding layers and LM heads, so their inference-time parameters are higher than their training parameters. This is because both the embedding layer and LM head are used during inference.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_4ZU8v4s3IR_Boomeran/figures/013_Table_2.jpg]]
*Table 2: Table 2: Hyperparameters used to train the student model. We choose the training hyperparameters to align with the values used in Pythia training (Biderman et al., 2023) and set the KLDiv and cosine distance weights such that the cross entropy, KLDiv, and cosine distance loss are approximately equal in magnitude at the beginning of training.*

**Figure 2** 展示了 Boomerang Distillation 在 Qwen3-4B-Base 上的主要结果：插值模型的分类准确率和生成准确率在学生和教师之间平滑插值，一致优于朴素层剪枝和随机初始化蒸馏基线。


![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_4ZU8v4s3IR_Boomeran/figures/002_Figure_2.jpg]]
*Figure 2: Qwen3-4B-Base Distilled models Pruned models Interpolated models*

| 基准测试 | 指标 | 提出方法 | 基线 | 提升 |
|---------|------|---------|------|------|
| 10个分类数据集（平均） | 分类准确率 | 平滑插值 | Naive Layer Pruning: 小于4B参数时显著下降 | 显著优于 |
| 3个生成数据集（平均） | 精确匹配准确率 | 平滑插值 | Naive Layer Pruning: 生成性能快速下降 | 显著优于 |
| WikiText | 困惑度 | 在学生和教师之间平滑插值 | Naive Layer Pruning: 随层数减少困惑度急剧上升 | 显著优于 |
| Qwen3-4B-Base | 计算开销 (FLOPS) | 4.31e19 | Standard distillation: 8.27e20 | 19.17x 加速 |

**Figure 3** 验证了 Boomerang Distillation 在 Qwen3-8B、Pythia-6.9B 和 Llama-3.2-3B 模型族上的泛化性。

**Figure 4** 显示插值模型与标准蒸馏模型性能相当，在较大尺寸上甚至更优，可能因为标准蒸馏在低质量语料上存在灾难性遗忘。

### 6.2 消融实验

**Figure 5**（损失项消融）：每层余弦距离损失带来最平滑的插值，但无该损失时 Boomerang Distillation 仍发生，表明初始化提供了大量对齐信息。

**Figure 6**（现成模型验证）：在 DistilBERT/BERT 和 DistilGPT2/GPT2 上零样本插值成功，优于朴素层剪枝。

**Figure 7**（与剪枝方法对比）：Boomerang Distillation 在所有中间尺寸上显著优于 LaCo 和 ShortGPT，尤其在生成任务上，剪枝方法在移除少量层后生成能力即崩溃至接近零。

**Figure 8**（学生模型尺寸消融）：每3层初始化产生类似每2层的插值行为，但更小的学生模型（每4/5层）无法平滑插值。

**Figure 10**（训练数据量消融）：增加训练 token 预算可提升插值模型性能；0.5B token 训练的学生模型性能平庸，导致插值行为消失。

### 6.3 计算效率

**Table 3** 显示 Boomerang Distillation 相比独立蒸馏每个中间模型可节省 14.53-19.17 倍 FLOPS。


![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_4ZU8v4s3IR_Boomeran/figures/036_Table_3.jpg]]
*Table 3: Table 3: Boomerang distillation provides significant computational speedup compared to individually distilling intermediate models. For Qwen3-4B-Base, Pythia-2.8B, and Llama-3.2-3B, we report the FLOPS required to individually distill each intermediate model versus boomerang distillation for the same number of training tokens (2.1B tokens). We can reduce FLOPs by 19.17x for Qwen, 17.01x for Pythia, and 14.53x for Llama using boomerang distillation.*

| 模型 | 标准蒸馏 FLOPS | Boomerang FLOPS | 加速比 |
|------|---------------|-----------------|--------|
| Qwen3-4B-Base | 8.27e20 | 4.31e19 | 19.17x |
| Pythia-2.8B | 2.82e20 | 1.66e19 | 17.01x |
| Llama-3.2-3B | 3.63e20 | 2.50e19 | 14.53x |

### 6.4 余弦相似度分析

**Figure 23-27** 对 Llama-3.2-3B 进行了逐层余弦相似度分析，发现：
- 标准初始化下，除首尾层外，学生层与教师块输出余弦相似度较低。
- 从首层开始修补（而非末层）可缓解对齐问题。
- 保留前两层教师权重的替代初始化可显著提高余弦相似度，产生更平滑的插值。
- 修补层数越多，插值模型与教师模型的最后一层余弦相似度越高。

### 6.5 公平性说明

- 所有实验均使用公开可用的模型和数据集，未涉及敏感属性或偏见分析。
- 计算效率分析仅关注 FLOPS，未考虑内存占用或能耗。
- 学生模型训练使用 The Pile 数据集，其潜在偏见可能影响下游任务性能。

### 补充图表

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_4ZU8v4s3IR_Boomeran/figures/040_Table_4.jpg]]
*Table 4: Table 4: Hyperparameters used to create LaCo models in Figures 7, 19, 22, 34, and 38*




## 定位与知识库关联

Boomerang Distillation 位于以下研究方向的交叉点：

1. **知识蒸馏（Knowledge Distillation）**：继承自 Hinton et al. (2015) 的蒸馏框架，但创新性地使用层剪枝初始化和对齐损失。
2. **模型剪枝（Model Pruning）**：与 LaCo (Yang et al., 2024) 和 ShortGPT (Men et al., 2024) 等层剪枝方法对比，Boomerang Distillation 通过蒸馏而非直接剪枝保留性能。
3. **弹性模型（Elastic Models）**：与 Cai et al. (2025) 的 LLamaflex 等需要训练时路由的方法不同，Boomerang Distillation 在训练后零样本生成中间模型。
4. **现成蒸馏模型**：在 DistilBERT/BERT 和 DistilGPT2/GPT2 上的成功验证表明，该现象在现有开源模型中已存在。

**局限性**：
- 需要训练一个蒸馏学生模型，计算成本仍然存在。
- 要求学生通过层剪枝创建，与宽度剪枝或注意力头剪枝结合时可能因隐藏维度不匹配而失效。
- 修补顺序可能导致不稳定，需根据余弦相似度分析调整。
- 目前仅在语言模型上验证，在其他模态（视觉、语音）的泛化性未知。
- 学生模型性能是插值成功的关键：若学生模型在目标任务上性能平庸，则插值模型性能也受限。

**开放问题**：
- 能否在不保留教师权重在内存中的情况下实现同等性能和稳定性？
- Boomerang Distillation 在大规模 LLM 上使用大量 token 预算蒸馏时的表现如何？
- 能否扩展到其他模态（如视觉 Transformer、语音模型）？



## 原文 PDF

![[paperPDFs/ICLR_2026/Boomerang_Distillation_Enables_Zero_Shot_Model_Size_Interpolation.pdf]]

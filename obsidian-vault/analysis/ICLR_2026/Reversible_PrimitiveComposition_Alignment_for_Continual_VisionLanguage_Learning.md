---
title: "Reversible Primitive–Composition Alignment for Continual Vision–Language Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Reversible_PrimitiveComposition_Alignment_for_Continual_VisionLanguage_Learning.pdf
aliases:
- CR
- RPCACVLL
- COMPO-REALIGN
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "用可逆正交组合头保持持续视觉语言学习中的原语组合绑定。"
primary_logic: "COMPO-REALIGN冻结编码器，只训练原始塑造器、Cayley正交作曲家和谱信任区域下的多正例对齐头。"
claims:
- "持续适应会保留属性和物体原始识别，却破坏属性-物体组合绑定关系。"
- "正交Cayley核心使原语到组合嵌入的映射可逆并降低组合结构漂移。"
- "多正例InfoNCE同时对齐文本组合嵌入和由原语组合得到的嵌入。"
- "谱信任区域通过梯度裁剪限制雅可比敏感性，降低遗忘并提升CRR。"
---

# Reversible Primitive–Composition Alignment for Continual Vision–Language Learning

> [!tip] 核心洞察
> 通过一个可逆的原始-组合对齐头（包含正交核心的作曲家、多正例InfoNCE损失和谱信任区域），可以在不依赖大量图像重放的情况下，显式地保持组合结构的可逆性和几何稳定性，从而显著提升组合保留率并降低遗忘。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向持续视觉语言学习的可逆原语-组合对齐 |
| 英文题名 | Reversible Primitive–Composition Alignment for Continual Vision–Language Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eiTy6AYeQi) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | COMPO-REALIGN |
| Dataset | 组合DIL + 多域MTIL（Track A+B） |

> [!tip] 效果简介
> - 组合DIL + 多域MTIL（Track A+B） 上，Avg R@1 (Image→Text) 为 58.8，对比 56.4 (C-CLIP/DIKI)，变化 +2.4。
> - 组合DIL + 多域MTIL（Track A+B） 上，Avg R@1 (Text→Image) 为 45.1，对比 43.0 (C-CLIP/DIKI)，变化 +2.1。
> - 组合DIL + 多域MTIL（Track A+B） 上，CRR 为 0.91，对比 0.88 (C-CLIP/DIKI)，变化 +0.03。

## 概述

本文提出 **COMPO-REALIGN**，一种用于持续视觉-语言模型（VLM）的轻量级对齐头，旨在解决持续学习中组合结构（属性与物体的绑定关系）的退化问题。核心发现是：在持续适应过程中，模型能够保持原始（属性/物体）识别能力，但会丧失组合结构，即属性与物体的绑定关系。COMPO-REALIGN 通过三个关键设计——可逆作曲家（正交 Cayley 核心）、多正例 InfoNCE 损失和谱信任区域——在不依赖大量图像重放的情况下，显式地保持组合结构的可逆性和几何稳定性。在组合 DIL 和多域 MTIL 检索任务上，该方法相比最强基线（C-CLIP/DIKI）在 Avg R@1 (Image→Text) 上提升了 +2.4，遗忘率降低了约 40%。

## 背景与动机

持续视觉-语言学习的目标是让模型在顺序任务中不断适应新数据，同时不遗忘已学知识。现有方法（如 EWC、LwF、Replay）主要关注整体性能的保持，但忽略了组合结构（即属性与物体的绑定关系）的退化问题。

**探索性研究**（Figure 1）揭示了关键瓶颈：在顺序微调（FT）过程中，原始识别（属性和物体）保持稳定，但组合准确率随任务索引下降，组合保留率（CRR）降至 1 以下，零样本组合准确率受影响最大。这表明模型能够记住“红色”和“汽车”这两个概念，但无法保持“红色的汽车”这一组合关系。

**误差分析**（Figure 2）进一步表明，组合误差与雅可比谱半径和循环一致性误差（CCE）共同增加。文本中心微缓冲区能够同时抑制谱敏感性和不可逆性，扩大低误差区域。**子空间漂移热图**（Figure 3）显示，FT 在深层和后期任务中产生显著的子空间漂移，EWC 有所缓解，而 Replay-Text 漂移最小。

## 核心创新

COMPO-REALIGN 的核心创新在于将组合结构的保持问题转化为几何可逆性和稳定性问题，通过三个互补的设计实现：

1. **可逆作曲家**：通过正交 Cayley 核心将原始嵌入映射到组合嵌入，保证映射的可逆性（R^T R = I，R^{-1} = R^T），从而支持从组合嵌入中精确重建原始嵌入。

2. **多正例 InfoNCE 损失**：将文本组合嵌入和从原始组合的嵌入都作为图像的正例，隐式地将两者对齐，无需额外的循环损失或集合损失。

3. **谱信任区域**：通过裁剪梯度来限制雅可比矩阵的最大奇异值，而非添加额外的损失项，从而稳定对齐几何结构。

## 整体框架

![[assets/figures/papers/iclr26_0001_eiTy6AYeQi_Reversible_PrimitiveComposition_Alignment_for_Co/figures/001_Figure_1.jpg]]

COMPO-REALIGN 的整体框架如下：

- **冻结的编码器**：使用冻结的 CLIP 风格视觉编码器 f_v 和文本编码器 f_t，输出进行 L2 归一化。
- **原始塑造器**：通过轻量适配器 A 和 MLP φ 调整原始嵌入，得到适应原始堆栈 U_p。
- **可逆作曲家**：对适应原始嵌入取平均，然后通过正交映射 R(Θ) 混合，产生组合嵌入 ê_c。
- **多正例 InfoNCE 损失**：联合对齐视觉嵌入与文本组合嵌入及组合后的嵌入。
- **谱信任区域**：当雅可比矩阵敏感性过高时，通过因子 α = min{1, γ/σ̂_max} 缩放梯度。

训练仅更新 Θ、A、φ 三个轻量组件，编码器保持冻结，无需任务 ID。

## 核心模块与公式推导

### 5.1 归一化嵌入

来自冻结编码器的 L2 归一化视觉、文本组合和原始嵌入：

$$z_v = \frac{f_v(x)}{\|f_v(x)\|_2}, \quad e_c = \frac{f_t(y_c)}{\|f_t(y_c)\|_2}, \quad e_{p,i} = \frac{f_t(p_i)}{\|f_t(p_i)\|_2} \in \mathbb{R}^d$$

### 5.2 适应原始堆栈

经过轻量适配器 A 和 MLP φ 调整后的原始嵌入的行式堆栈：

$$U_p = [\phi(A e_{p,1}); \ldots; \phi(A e_{p,m})] \in \mathbb{R}^{m \times d}$$

### 5.3 可逆作曲家（正交 Cayley 核心）

平均适应原始嵌入，然后通过正交映射 R(Θ) 混合以产生组合嵌入：

$$\bar{u} = \frac{1}{m} \sum_{i=1}^m \phi(A e_{p,i}), \quad \hat{e}_c = \frac{R(\Theta) \bar{u}}{\|R(\Theta) \bar{u}\|_2}$$

正交矩阵通过 Cayley 变换参数化：

$$R(\Theta) = (I - S)(I + S)^{-1}, \quad S = \frac{1}{2}(\Theta - \Theta^\top), \ \Theta \in \mathbb{R}^{d \times d}$$

这保证了 R(Θ)^T R(Θ) = I 且 R(Θ)^{-1} = R(Θ)^T，使得组合映射可逆。

### 5.4 多正例 InfoNCE 损失

图像到文本方向的多正例 InfoNCE 损失，每个图像有两个正例（文本组合嵌入和组合后的嵌入）：

$$\mathcal{L}_{v \to c} = -\frac{1}{B} \sum_{i=1}^B \log \frac{\exp(s(z_{v,i}, e_{c,i})/\tau) + \exp(s(z_{v,i}, \hat{e}_{c,i})/\tau)}{\sum_{j=1}^B [\exp(s(z_{v,i}, e_{c,j})/\tau) + \exp(s(z_{v,i}, \hat{e}_{c,j})/\tau)]}$$

总损失为图像到文本和文本到图像方向的对称平均：

$$\mathcal{L}_{\mathrm{Tri}} = \frac{1}{2}(\mathcal{L}_{v \to c} + \mathcal{L}_{c \to v})$$

### 5.5 谱信任区域

相似度分数相对于堆叠适应原始嵌入的雅可比矩阵：

$$J_p = \frac{\partial s(z_v, \hat{e}_c)}{\partial \mathrm{vec}(U_p)} \in \mathbb{R}^{1 \times md}$$

当估计的最大奇异值超过阈值 γ 时，通过因子 α 缩放梯度：

$$\mathbf{g}_\theta \leftarrow \mathbf{g}_\theta \cdot \alpha, \quad \alpha = \min\left\{1, \frac{\gamma}{\hat{\sigma}_{\max}}\right\}$$

### 5.6 诊断指标

**组合保留率（CRR）**：配对准确率与属性和物体准确率乘积的比率，越高表示绑定保留越好：

$$\mathrm{CRR}^{(t)} = \frac{A_{\mathrm{pair}}^{(t)}}{A_{\mathrm{attr}}^{(t)} \cdot A_{\mathrm{obj}}^{(t)}}$$

**循环一致性误差（CCE）**：原始嵌入与其经过组合映射再返回后的重建之间的误差：

$$\mathrm{CCE} = \| E_p - R_{pc}(R_{cp}(E_p)) \|_2$$

## 实验与分析

### 6.1 主要结果

**Table 1: 组合 DIL 和多域 MTIL 检索/ITM 结果**

![[assets/figures/papers/iclr26_0001_eiTy6AYeQi_Reversible_PrimitiveComposition_Alignment_for_Co/figures/010_Table_1.jpg]]
*Table 1: Retrieval / ITM results on compositional DIL (Track A) and multi-domain MTIL (Track B). We report averages across their respective task streams. ↑ higher is better; AF and ZSTD ↓ lower (closer to 0 for ZSTD) is better. CRR measures compositional binding retention.*

| 方法 | Avg R@1 (I→T) ↑ | Avg R@1 (T→I) ↑ | CRR ↑ | AF ↓ | ZSTD ↓ |
|------|:----------------:|:----------------:|:-----:|:----:|:------:|
| C-CLIP/DIKI | 56.4 | 43.0 | 0.88 | 5.0 | -2.5 |
| **COMPO-REALIGN** | **58.8** | **45.1** | **0.91** | **3.2** | **-1.3** |
| Δ | +2.4 | +2.1 | +0.03 | -1.8 (40%) | +1.2 |

**Table 2: 持续 VQA 结果（Track C）**

![[assets/figures/papers/iclr26_0001_eiTy6AYeQi_Reversible_PrimitiveComposition_Alignment_for_Co/figures/011_Table_2.jpg]]
*Table 2: Continual VQA (Track C). Average accuracy (%) on CLOVE-scene (DIL), CLOVE-function (TIL), and VQACL (skill×concept), plus average forgetting AF↓.*

| 方法 | CLOVE-scene ↑ | CLOVE-function ↑ | VQACL ↑ | AF ↓ |
|------|:-------------:|:----------------:|:-------:|:----:|
| C-CLIP | 62.8 | 58.1 | 54.2 | 5.2 |
| **COMPO-REALIGN** | **65.1** | **60.4** | **56.8** | **3.6** |
| Δ | +2.3 | +2.3 | +2.6 | -1.6 |

### 6.2 消融研究

**Table 3: 单因素消融**

![[assets/figures/papers/iclr26_0001_eiTy6AYeQi_Reversible_PrimitiveComposition_Alignment_for_Co/figures/012_Table_3.jpg]]
*Table 3: Single-factor ablations across Tracks A+B (Retrieval/ITM) and Track C (Continual VQA). Metrics (left): Avg R@1 ↑ (two directions), CRR ↑, AF ↓, ZSTD ↓; Metrics (right): CLOVEscene/func/VQACL accuracy ↑, AF ↓. Each row toggles exactly one component away from the full model.*

| 变体 | R@1 I→T | CRR | AF | CLOVE-scene | VQACL |
|------|:-------:|:---:|:--:|:-----------:|:-----:|
| 完整模型 | 58.8 | 0.91 | 3.2 | 65.1 | 56.8 |
| 去除组合正例 | -1.9 | -0.04 | +0.8 | -1.9 | -1.8 |
| 去除正交核心 | -2.5 | -0.03 | +1.5 | -1.6 | -1.0 |
| 禁用谱裁剪 | -1.2 | -0.02 | +1.2 | -1.4 | -1.5 |
| 消除文本缓冲区 | -1.5 | -0.03 | +1.0 | -1.7 | -1.6 |
| 去除原始塑造器 | -1.0 | -0.01 | +0.5 | -0.9 | -0.8 |

关键发现：
- 去除组合正例导致最大的性能下降，验证了多正例对齐的核心作用。
- 去除正交核心（线性混合）显著降低 CRR 并增加遗忘，验证了可逆性的重要性。
- 禁用谱裁剪增加遗忘并恶化 ZSTD，验证了几何稳定性的必要性。

### 6.3 几何-结构耦合分析

**Figure 4** 展示了三个关键相关性：
- σ_max 与 R@1 和 CRR 呈强负相关（Pearson/Spearman 系数显著）。
- CCE 与 |ZSTD| 呈正相关。
- COMPO-REALIGN 的任务轨迹（T1→T6）保持在低误差盆地中。

**Figure 5** 展示了可逆读出质量和反事实鲁棒性：
- 从组合嵌入 ê_c 进行原始读出的 PR/ROC 曲线显示，完整模型显著优于消融变体。
- 在属性交换和物体交换的反事实场景中，完整模型产生更大的对比边界，更少的硬负例命中。

### 6.4 文本作为结构锚点

**Figure 6** 验证了文本中心缓冲区的有效性：
- 更高的语义多样性与更大的 ΔCRR 正相关。
- 增益在不同模板形态和任务间保持一致。
- 优势在 EN/ZH/ES 三种语言上均成立。

### 6.5 顺序敏感性

**Figure 8-9** 显示 COMPO-REALIGN 在不同任务顺序下产生更紧的误差带和更低的变异性：
- 跨顺序的 Avg R@1 (I→T) 标准差降至 0.26（Track A）和 0.24（Track B），而强基线为 0.45-0.52。
- AF 变异性从 0.27-0.28（DIKI）降至 0.15。

### 6.6 跨域零样本稳定性

**Figure 10-11** 显示 COMPO-REALIGN 在所有域上集中在低 σ、低 |ZSTD| 区域：
- 在 6/6 个域中占据左下象限（基于中位数）。
- 域内 σ 与 |ZSTD| 的 Pearson 相关性较高，表明几何-零样本耦合强。

### 6.7 训练动态

**Figure 12** 展示了谱信任区域的效果：
- COMPO-REALIGN 的 σ̂_max 时间热图显示稀疏、短暂的尖峰，集中在早期步骤和 L12。
- No-Clip 消融显示广泛、持久的超过阈值 γ 的波段，尤其在后期。
- 触发率图显示 COMPO-REALIGN 快速衰减且方差低，而 No-Clip 持续高触发。

### 6.8 理论分析

**Section D.1** 提供了可逆组合的理论保证：
- **Lemma 1**：在相干性 μ 条件下，平均原始向量的范数有下界，成员与非成员的内积可分离。
- **Theorem 1**：当 μ < 1/(2m-1) 时，通过 top-m 解码可精确恢复原始集 S。
- **Theorem 2**：在噪声下，当 ε < Δ₀/(4+Δ₀) 时，精确恢复仍然成立。
- **概率 CRR 下界**：在亚高斯噪声下，期望 CRR 的下界随维度指数级增长。

### 补充图表

![[assets/figures/papers/iclr26_0001_eiTy6AYeQi_Reversible_PrimitiveComposition_Alignment_for_Co/figures/002_Figure_2.jpg]]

![[assets/figures/papers/iclr26_0001_eiTy6AYeQi_Reversible_PrimitiveComposition_Alignment_for_Co/figures/003_Figure_3.jpg]]
*Figure 3: (a) Composition accuracy (mean (b) CRR (higher is better). Text- (c) Zero-shot composition accuracy on ±95% CI) across tasks for FT, EWC, centric replay slows CRR decay. unseen pairs. Replay-Text.*

## 方法谱系与知识库定位

COMPO-REALIGN 属于持续视觉-语言学习领域，与以下方法谱系相关：

- **正则化/蒸馏方法**（EWC, LwF, Mod-X, ZSCL, ZAF）：通过约束参数变化或蒸馏知识来防止遗忘，但未专门处理组合结构。
- **重放方法**（IncCLIP, ConStruct-VL, SGP, GIFT, TiC-CLIP）：通过存储和重放样本来保持知识，但图像中心重放在严格预算下效率低。
- **动态架构方法**（C-CLIP, DIKI, CL-MoE）：通过动态扩展或调整模型结构来适应新任务，但未显式保持组合可逆性。
- **提示学习方法**（TRIPLET, QUAD）：通过可学习提示来适应新任务，但未解决组合绑定退化。

COMPO-REALIGN 的独特定位在于：
1. 识别了组合结构退化这一被忽视的瓶颈。
2. 将问题转化为几何可逆性和稳定性问题，而非简单的记忆保持。
3. 提出了最小化配方（一个作曲家、一个目标、一个稳定器），参数开销 <1% 的冻结骨干。
4. 提供了理论保证（相干性条件下的精确恢复和噪声鲁棒性）。

**局限性**：
- 依赖于可用的原始（属性/物体）注释。
- 理论分析假设原始嵌入具有低相干性。
- 谱信任区域引入了额外超参数 γ。
- 主要在 CLIP 风格模型上评估。

**开放问题**：
- 扩展到原始集随时间变化的场景。
- 自适应确定谱信任区域阈值 γ。
- 在更大规模 VLM（如 LLaVA）上的表现。
- 文本中心缓冲区的最佳构建策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/Reversible_PrimitiveComposition_Alignment_for_Continual_VisionLanguage_Learning.pdf]]

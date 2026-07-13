---
title: "A-TPT: Angular Diversity Calibration Properties for Test-Time Prompt Tuning of Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_TPT_Angular_Diversity_Calibration_Properties_for_Test_Time_Prompt_Tuning_of_Vision_Language_Models.pdf
project_link: https://mb-shihab-aaqil-ahamed.github.io/A-TPT/
code_link: https://github.com/MB-Shihab-Aaqil-Ahamed/A-TPT/
aliases:
- A-TPT
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/safety_security
core_operator: "最大化归一化文本特征之间的最小成对角度距离，实现类间角度均匀分布（Tammes最佳填充问题）。"
primary_logic: "角度多样性比简单的特征分散或正交化更能促进文本特征在单位超球面上均匀分布，充分利用嵌入空间，从而显著降低校准误差，同时保持准确率。"
claims:
- "A-TPT在细粒度数据集上整体ECE降至3.26，远低于C-TPT的5.42和O-TPT的4.36，且准确率持平。"
- "无论类别数大于还是小于嵌入维度，A-TPT均保持最低ECE（Group1 2.92，Group2 3.60）。"
- "在自然分布偏移数据集上，A-TPT平均ECE 3.92，低于O-TPT的4.88和C-TPT的5.82。"
- "角度多样性的梯度范数与成对角度无关，即使特征靠近也保持稳定，而O-TPT的正交性梯度在角度趋0时消失。"
---

# A-TPT: Angular Diversity Calibration Properties for Test-Time Prompt Tuning of Vision-Language Models

> [!tip] 核心洞察
> 角度多样性比简单的特征分散或正交化更能促进文本特征在单位超球面上均匀分布，充分利用嵌入空间，从而显著降低校准误差，同时保持准确率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | A-TPT：测试时提示调优的角度多样性校准特性 |
| 英文题名 | A-TPT: Angular Diversity Calibration Properties for Test-Time Prompt Tuning of Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VhlSBZebEw) · [GitHub](https://github.com/MB-Shihab-Aaqil-Ahamed/A-TPT/) · [Project](https://mb-shihab-aaqil-ahamed.github.io/A-TPT/) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/safety_security |
| Method | A-TPT |
| Dataset | Fine-grained datasets (11 datasets, CLIP ViT-B/16, overall), Fine-grained datasets (CLIP ViT-B/16, N>\ |
| D\ | and N<\ |
| D\ | ), Natural distribution shifts (ImageNet-V2/A/R/Sketch, CLIP ViT-B/16), Medical: ISIC 2018 (FPT backbone) |

> [!tip] 效果简介
> - Fine-grained datasets (11 datasets, CLIP ViT-B/16, overall) 上，ECE 为 3.26，对比 C-TPT: 5.42, O-TPT: 4.36，变化 ↓2.16 vs C-TPT, ↓1.10 vs O-TPT。
> - Fine-grained datasets (CLIP ViT-B/16, N>\|D\| and N<\|D\|) 上，ECE 为 2.92 (N>\|D\|), 3.60 (N<\|D\|)，对比 C-TPT: 5.13 (N>\|D\|), 5.72 (N<\|D\|); O-TPT: 4.23 (N>\|D\|), 4.48 (N<\|D\|)，变化 ↓2.21/0.80 vs C-TPT; ↓1.31/0.88 vs O-TPT。
> - Natural distribution shifts (ImageNet-V2/A/R/Sketch, CLIP ViT-B/16) 上，ECE 为 3.92，对比 C-TPT: 5.82, O-TPT: 4.88，变化 ↓1.90 vs C-TPT, ↓0.96 vs O-TPT。

## 概要

测试时提示调优（TPT）使视觉语言模型在无标注条件下自适应，但现有校准策略——例如 C-TPT 采用的平均文本特征分散（ATFD）和 O-TPT 引入的正交性约束——在类别数量超过嵌入维度时，无法保证文本特征在单位超球面上均匀分布，导致期望校准误差（ECE）显著升高。针对这一瓶颈，本文提出 **A-TPT**，将角度多样性正则项加入 TPT 目标，显式地最大化归一化文本特征之间的最小成对角度距离，该思路在数学上对应于 Tammes 最佳填充问题。与简单分散或强制正交相比，角度多样性能够更可靠地推动文本特征均匀散布，从而持续降低校准误差，且梯度在成对角度趋零时仍保持稳定（相较于正交性约束），避免了梯度消失。

实验在 11 个细粒度数据集上使用 CLIP ViT‑B/16 骨干进行整体评估：A‑TPT 的 ECE 降至 3.26，而 C‑TPT 和 O‑TPT 分别为 5.42 和 4.36，准确率相当；在自然分布偏移数据集上，A‑TPT 的平均 ECE 也降低至 3.92。即使类别数大于或小于嵌入维度，A‑TPT 均展现出最低的 ECE（分组结果分别为 2.92 和 3.60），且 Pareto 前沿分析确认其准确率‑校准误差权衡优于所有基线。该方法额外计算开销与 O‑TPT 相当，可作为即插即用的校准模块嵌入现有 TPT 流程，但在语义高度重叠的条件下偶尔伴有微小准确率下降，实际应用需结合任务特性综合权衡。



视觉-语言模型（如CLIP）在零样本分类任务中展现出强大能力，但其预测置信度往往与实际准确率存在显著偏差——这一校准误差（Expected Calibration Error, ECE）问题严重影响了模型在高风险应用中的可靠性。测试时提示调优（Test-Time Prompt Tuning, TPT）通过在测试阶段以无监督方式优化可学习的提示向量，在提升零样本准确率的同时，也引入了新的校准挑战：如何在不牺牲准确率的前提下，使模型的概率输出真实反映其预测的正确性。

现有工作围绕TPT的校准问题提出了两类正则化策略: C-TPT通过最大化文本特征到质心的平均L2距离（平均文本特征分散，ATFD）来分散特征，O-TPT则施加正交性约束迫使成对文本特征正交。然而，这两类方法存在根本性缺陷：它们无法保证文本特征在单位超球面上的均匀角度分布。当类别数多于嵌入维度时（N > |D|），嵌入空间不足以容纳所有正交方向，正交性约束必然失效，文本特征被迫聚集；而L2距离最大化只关注特征远离质心，但特征之间仍可能形成紧密的局部簇。这两种情况均导致校准误差升高，表现为模型在某些类别上过度自信或不够自信。

图2对比了三种优化策略的几何差异：C-TPT的ATFD优化仅增加特征与质心的距离，O-TPT的角度优化强制特征正交但在高维受限场景下失效，而A-TPT的数值优化通过求解Tammes最佳填充问题——最大化归一化文本特征之间的最小成对角度距离——实现类间角度的均匀分布。这一视角的关键洞察在于：角度多样性比简单的特征分散或正交化更能促进文本特征在单位超球面上充分利用嵌入空间，从而在根本上降低校准误差。

本文的核心动机正是揭示并解决这一瓶颈：提出角度多样性（Angular Diversity, AD）作为即插即用的正则项，以最大化最小成对角度距离为目标，促进文本特征的均匀分布。该方法具有两项关键优势。首先，梯度稳定性：A-TPT的梯度范数与成对角度无关，始终为嵌入向量模长的倒数（$1 / \|\mathbf{e}_i\|$），即使特征向量互相靠近也保持稳定优化；相比之下，O-TPT依赖的正交性梯度在角度趋近于0时消失，导致优化停滞。其次，维度无关性：无论类别数是大于还是小于嵌入维度，A-TPT均能维持均匀分布，避免了正交性约束在高类别数下的灾难性失效。由此，A-TPT在保持与TPT可比准确率的同时，能系统性地降低校准误差，如表1的整体ECE降至3.26，远低于C-TPT的5.42和O-TPT的4.36。



## 核心方法与创新机理

A-TPT 的核心创新在于针对测试时提示调优（TPT）中的校准瓶颈，提出了一种新的正则化机制——角度多样性（Angular Diversity），从根本上改变了文本特征的分布策略。

### 1. 解决的核心瓶颈

现有 TPT 校准方法（C-TPT 和 O-TPT）虽然试图通过特征分散来提升校准性能，但存在固有缺陷：
- **C-TPT（平均文本特征分散）** 仅最大化特征到质心的 L2 距离，无法保证类间特征的均匀分布，尤其在类别数 $N$ 超过嵌入维度 $|D|$ 时，特征倾向于在高维空间局部聚集。
- **O-TPT（正交性约束）** 强制成对特征正交，但在 $N > |D|$ 时理论上不可行（嵌入空间无法容纳超过维度的正交向量）；更致命的是，其梯度范数与 $\sin\theta$ 成正比，当特征角度趋近零时梯度消失（见 Figure 7），导致优化停滞。

这两种方法均**未能保证文本特征在单位超球面上的均匀角度分布**，使得预测概率过度自信或分散，校准误差（ECE）居高不下。

### 2. 核心洞察：角度多样性的均匀分布原理

A-TPT 的洞察在于：**真正的校准提升需要特征在角度空间均匀分布，而非简单的距离分散或正交化**。通过最大化归一化文本特征之间的最小成对角度距离，可以有效求解 Tammes 最佳填充问题，使得：

- 每个文本特征向量在单位超球面上指向多样化的方向，最大化类间可分离性。
- 所有成对角度都保持最小值以上，避免特征聚集或强制分离带来的校准偏差。

从图 Figure 4 的余弦相似度变化对比可见，O-TPT 在某些数据点上特征高度相关（高余弦相似度），而 A-TPT 在所有数据点上都实现了最低的平均余弦相似度，即**最大的最小成对角度距离**。这直接验证了角度多样性在分布均匀性上的优势。

### 3. 改变的"槽位"（Changed Slots）

相比基线方法，A-TPT 在两个关键设计槽位上做出了根本改变：

| 槽位 | 基线值 | 提出值 | 证据锚点 |
|------|--------|--------|----------|
| **优化目标** | 仅最小化预测熵 $\mathcal{L}_{\mathrm{TPT}}$ | $\mathcal{L}_{\mathrm{TPT}} - \lambda \cdot \mathrm{AD}$，增加角度多样性正则项 | 整体目标函数 Eq. (3) |
| **文本特征分布策略** | C-TPT: L2 距离分散；O-TPT: 正交性约束 | 角度多样性：最大化最小成对角度距离，求解 Tammes 最佳填充 | Eq. (1), (2)；Figure 2 几何对比 |

其中角度多样性项 $\mathrm{AD}$ 定义为：

$$\mathrm{AD} = \frac{1}{N} \sum_{i=1}^{N} \min_{j \in \{1,\dots,N\} \setminus \{i\}} \theta_{ij}, \quad \theta = \arccos(\hat{\mathbf{E}} \hat{\mathbf{E}}^T)$$

最大化 $\mathrm{AD}$ 等价于提升所有类别文本特征的最小角度距离，迫使特征在球面上均匀散开。

### 4. 为什么角度多样性更有效？

**梯度稳定性：** O-TPT 使用余弦相似度作为优化目标，其梯度范数 $\left\| \frac{\partial \hat{\mathbf{E}} \hat{\mathbf{E}}^T}{\partial \mathbf{e}_i} \right\| = \frac{\|\sin \theta_{ij}\|}{\|\mathbf{e}_i\|}$，当 $\theta \to 0$ 时梯度幅值趋于零，优化陷入困境。而 A-TPT 直接优化角度距离，梯度范数 $\left\| \frac{\partial \theta_{ij}}{\partial \mathbf{e}_i} \right\| = \frac{1}{\|\mathbf{e}_i\|}$，与角度值无关（见 Figure 7），即使特征靠近也能保持稳定梯度，确保优化持续推进。

**维度无关性：** 无论 $N > |D|$（类别数大于嵌入维度，Group 1）还是 $N < |D|$（Group 2），A-TPT 均保持最低 ECE（Table 1: Group1 2.92, Group2 3.60），而 O-TPT 在 Group 1 中因正交性理论不成立导致校准大幅退化（OCE 4.23）。这表明角度多样性的鲁棒性远超正交约束。

**即插即用的简洁性：** A-TPT 仅需在标准 TPT 损失后加入一个正则项，计算开销与 O-TPT 相当，无需修改模型架构或引入额外参数。正则化系数 $\lambda$ 固定为 80.0，无需逐样本动态调整即可有效（消融实验见 Appendix A.20）。

### 5. 关键证据强度

Table 1 的综合结果显示，A-TPT 在细粒度数据集上的整体 ECE 降至 **3.26**，相比 C-TPT 的 5.42 降低 2.16，相比 O-TPT 的 4.36 降低 1.10，且准确率基本持平（61.27 vs. 61.32），**验证了角度多样性并非以牺牲准确率为代价换取校准**。Pareto 前沿分析（Figure 14）进一步证实 A-TPT 在准确率-校准误差权衡上严格优于所有基线。

综上所述，A-TPT 的创新在于从"分散特征"或"强制正交"的粗粒度策略，升级为"求解角度均匀分布"的精细优化，从根源上解决了 TPT 校准中的特征坍缩与梯度消失问题。



![[assets/figures/papers/iclr26_0005_VhlSBZebEw_A-TPT_Angular_Diversity_Calibration_Properties_f/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of numerical optimization (A-TPT (Ours)) with angular optimization (O-TPT Sharifdeen et al. (2025)) and ATFD optimization (C-TPT Yoon et al. (2024))*

A-TPT 的整体流程在标准测试时提示调优（TPT）的基础上引入了一个**角度多样性校准正则项**，目标是同时提升零样本分类的准确率与校准质量。方法围绕"文本特征的均匀角度分布可显著降低校准误差"这一核心洞见构建，通过求解高维超球面上的 Tammes 最佳填充问题来显式建模类间角度分离。

整个 pipeline 包含以下关键模块和数据流：

1. **提示参数化与文本特征提取**
   - 对每张测试图像，将类别名填入可学习提示模板（如"a photo of a {class}"），并送入固定的 CLIP 文本编码器 $f_t$，生成所有 $N$ 个类的文本特征向量 $\{ \mathbf{e}_k \}_{k=1}^N$。文本特征随后被归一化为 $\hat{\mathbf{e}}_k = \mathbf{e}_k / \|\mathbf{e}_k\|$，形成归一化文本特征矩阵 $\hat{\mathbf{E}}$。

2. **图像特征提取**
   - 测试图像通过冻结的 CLIP 图像编码器 $f_i$ 得到图像特征 $\mathbf{v}$，同样进行归一化处理。

3. **TPT 熵最小化主干**
   - 使用归一化图像特征与归一化文本特征计算余弦相似度（softmax 后得预测概率），并计算预测分布的熵 $\mathcal{L}_{\mathrm{TPT}}$。通过最小化熵来无监督地调优提示参数，提升零样本精度。这一步继承自标准 TPT，旨在让模型对测试样本的预测更加确信。

4. **角度多样性正则项（A-TPT 损失）**
   - 单独对归一化文本特征矩阵 $\hat{\mathbf{E}}$ 计算角度多样性项 $\mathrm{AD}$：
     $$\mathrm{AD} = \frac{1}{N} \sum_{i=1}^{N} \min_{j \neq i} \theta_{ij}, \quad \theta_{ij} = \arccos(\hat{\mathbf{E}}_i \cdot \hat{\mathbf{E}}_j)$$
     该项衡量了所有类别的最小成对角度距离的平均值。最大化 $\mathrm{AD}$ 等效于迫使文本特征在单位超球面上尽量均匀分布（Tammes 问题），从而扩大类间角度间隔、提升校准质量。与仅依赖 L2 距离分散（C‑TPT）或强制正交性（O‑TPT）的方案不同，角度多样性天然避免了在类别数 $N$ 大于嵌入维度 $|D|$ 时出现的特征拥挤或优化失效现象，且梯度范数始终为 $1/\|\mathbf{e}_i\|$，与成对角度无关，优化过程更稳定（详见附录 A.5 梯度分析）。

5. **联合优化目标**
   - 最终的提示参数 $\mathbf{p}$ 通过下式学习：
     $$\mathbf{p}^* = \arg\min_{\mathbf{p}} \big( \mathcal{L}_{\mathrm{TPT}} + \lambda \cdot \mathcal{L}_{\mathrm{A-TPT}} \big), \quad \mathcal{L}_{\mathrm{A-TPT}} = -\mathrm{AD}$$
     其中 $\lambda$ 控制校准正则化的强度，论文中固定为 $80.0$。测试时，每张图像独立进行若干步梯度更新，更新后的提示参数直接替换用于该样本的推理，得到最终类别预测及其置信度。

**输入输出流**可以概括为：
- 输入：单张测试图像 + 可学习提示参数（跨样本共享的初始化） + 固定类别词表。
- 前向过程：图像编码器产生 $\mathbf{v}$；文本编码器根据当前提示产生 $\{\mathbf{e}_k\}$；计算 softmax 预测用于熵和校准损失。
- 反向过程：联合梯度更新提示参数，使预测熵降低的同时增大文本特征之间的最小角度。
- 输出：更新后的提示下的类别预测，以及可用于可靠性评估的置信度分数。

整体框架将校准需求直接编码进提示调优的损失函数，使得在无标签测试样本上不仅能适应分布偏移，还能提供良好校准的概率估计。与现有校准型测试时提示方法相比，A‑TPT 的计算开销与 O‑TPT 相近，但能稳定地给出更低的 ECE（预期校准误差），并且在类别维度关系 $N > |D|$ 和 $N < |D|$ 两种情境下均表现出鲁棒优势。



A‑TPT 在标准测试时提示调优（TPT）的框架上，引入一个**角度多样性正则项**，使文本特征在单位超球面上趋于均匀分布，从而显著降低预期校准误差（ECE）。其核心模块包括：(1) CLIP 图像/文本编码器，提取测试图像与类别提示的特征；(2) 无监督熵最小化模块（标准 TPT 损失）；(3) **角度多样性计算模块**，负责度量归一化文本特征之间的最小成对角度距离，并作为损失项反向传播。

### 角度多样性正则项（Angular Diversity, AD）

设每个类别的文本嵌入为 $\mathbf{e}_i$，归一化后得到 $\hat{\mathbf{E}}_i = \mathbf{e}_i / \|\mathbf{e}_i\|$。成对角度矩阵 $\theta$ 通过反余弦计算：

$$
\theta = \arccos(\hat{\mathbf{E}} \hat{\mathbf{E}}^T)
$$

角度多样性定义为所有类别与其最近类别之间角度的平均值：

$$
\mathrm{AD} = \frac{1}{N} \sum_{i=1}^{N} \min_{j \in \{1,\dots,N\} \setminus \{i\}} \theta_{ij}
\tag{1}
$$

A‑TPT 将 $\mathrm{AD}$ 的**负值**作为正则项，即最大化最小成对角度距离。这一目标本质上对应 **Tammes 最佳填充问题**——在超球面上寻找点集以最大化最小角距离——由此推动特征方向均匀铺开，避免聚集。

### 整体优化目标

结合 TPT 的熵最小化损失 $\mathcal{L}_{\mathrm{TPT}}$，提示参数 $\mathbf{p}$ 的优化目标为：

$$
\mathbf{p}^* = \arg\min_{\mathbf{p}} \big( \mathcal{L}_{\mathrm{TPT}} + \lambda \cdot \mathcal{L}_{\mathrm{A-TPT}} \big), \quad \mathcal{L}_{\mathrm{A-TPT}} = -\mathrm{AD}
\tag{2}
$$

其中 $\lambda$ 为固定超参数，实验中统一设为 80.0。该目标在无需标注样本的前提下，同时提升零样本准确率与概率校准质量。

### 数值稳定性与梯度特性

反余弦函数在输入接近 $\pm 1$ 时梯度会爆炸：

$$
\frac{\partial}{\partial x} (\arccos(x)) = -\frac{1}{\sqrt{1 - x^2}}
$$

为避免 NaN 或梯度溢出，实际计算时对余弦相似度矩阵钳位到 $[-0.99999, 0.99999]$ 范围内。此外，角度多样性的梯度范数具有一个重要性质——**与成对角度无关**：

$$
\left\| \frac{\partial \theta_{ij}}{\partial \mathbf{e}_i} \right\| = \frac{1}{\|\mathbf{e}_i\|}
$$

这意味着即使两个类别特征几乎重合（$\theta \to 0$），梯度依然保持稳定。相比之下，基于正交性约束的 O‑TPT 中，梯度的范数正比于 $\sin\theta_{ij}$，当角度趋近于 0 时梯度消失，导致优化停滞。A‑TPT 的梯度特性是其能在类别数多于或少于嵌入维度的情况下均维持低校准误差的关键原因。



## 实验与关键发现

**总体校准性能** A‑TPT 的核心优势在于显著降低预期校准误差（ECE）而不牺牲识别准确率。在覆盖细粒度、自然分布偏移和医学图像的 11 个数据集上，A‑TPT 的整体 ECE 为 **3.26**，相比 C‑TPT 的 5.42 降低 2.16，相比 O‑TPT 的 4.36 降低 1.10（Table 1）。更重要的是，这一收益在类别数大于和小于嵌入维度两种设定下均成立：当 N > |D| 时 ECE 为 2.92，N < |D| 时为 3.60，远低于 C‑TPT 的 5.13/5.72 和 O‑TPT 的 4.23/4.48（Table 2）。在自然分布偏移场景下，A‑TPT 同样保持最低平均 ECE（3.92），优于 O‑TPT 的 4.88 和 C‑TPT 的 5.82（Table 3）。医学影像任务 ISIC 2018 上，FPT + A‑TPT 将 ECE 降至 0.0794，较 FPT+O‑TPT 的 0.1381 降低近 42%（Table 4）。

![[assets/figures/papers/iclr26_0005_VhlSBZebEw_A-TPT_Angular_Diversity_Calibration_Properties_f/figures/005_Table_1.jpg]]
*Table 1: Comparison of Accuracy and ECE across methods with CLIP ViT-B/16 backbone and categories based on the number of classes and TPT text features embedding dimension (|D|)*

![[assets/figures/papers/iclr26_0005_VhlSBZebEw_A-TPT_Angular_Diversity_Calibration_Properties_f/figures/011_Table_2.jpg]]
*Table 2: Comparison of methods across fine-grained datasets for Accuracy (Acc.) and Expected Calibration Error (ECE) with CLIP ViT-B/16 and CLIP RN50 pre-trained backbone for both N > | D | and N \< | D | cases. The overall top best-performing result is in bold*

![[assets/figures/papers/iclr26_0005_VhlSBZebEw_A-TPT_Angular_Diversity_Calibration_Properties_f/figures/012_Table_3.jpg]]
*Table 3: Pre-trained Backbone: CLIP ViT-B/16 | Embedding dimension: 512-d*

**准确率‑校准平衡** Pareto 前沿分析显示，A‑TPT 在 Flowers102 和 Food101 上均位于前沿，即在不损失准确率的前提下获得最低 ECE，表明其并非以牺牲分类性能换取校准改善（Figure 14）。在所有设定中，A‑TPT 的总体准确率与基线、TPT 保持可比，在多数数据集上准确率波动小于 1‑2%。

**角度多样性的梯度稳定性与几何优势** Figure 7 揭示了为什么 A‑TPT 比 O‑TPT 更稳定：O‑TPT 基于正交性约束，其梯度范数随成对角度减小而消失；当两个特征向量接近时，优化信号几乎为零，导致特征无法被进一步推开。A‑TPT 的角度多样性梯度范数仅为嵌入向量模长的倒数（`1/||e_i||`），与角度无关，即使特征靠近仍保持恒定梯度，因此能持续驱动类间分离。这一特性从梯度层面保证了在 N > |D|（必须挤压高维空间）时依然能实现良好的均匀分布。

![[assets/figures/papers/iclr26_0005_VhlSBZebEw_A-TPT_Angular_Diversity_Calibration_Properties_f/figures/008_Figure_7.jpg]]
*Figure 7: Gradient norm comparison between A-TPT and O-TPT. A-TPT maintains constant gradient norm $1/\|$\mathbf{e}_$i\|$ regardless of pairwise angle, while O-TPT gradient vanishes as $\theta \to$ 0$.

**余弦相似度与均匀分布可视化** Figure 4 给出了更直观的证据：O‑TPT 在多数数据点上成对余弦相似度波动剧烈，甚至出现一些高相似度聚集；而 A‑TPT 在所有数据点上都保持了最低的均值余弦相似度，对应最大的最小成对角度距离。t‑SNE 可视化（Figure 3）进一步显示，经过 A‑TPT 调优的文本特征按类别形成更分散、更均匀的分布，有利于紧致分类边界和置信度校准。

![[assets/figures/papers/iclr26_0005_VhlSBZebEw_A-TPT_Angular_Diversity_Calibration_Properties_f/figures/007_Figure_4.jpg]]
*Figure 4: Comparison of mean cosine similarity changes for both categories with CLIP ViT-B/16 backbone. Where, O-TPT fails, but our A-TPT offers consistent cosine similarity values and achieves the greatest minimum pairwise angular distance among text features for all the data points. (suppl. carries more details.)*

**消融与组合能力** λ 固定为 80.0 的经验设定来自消融研究，各测试实例上均无需单独调整，简化了部署。A‑TPT 可与 C‑TPT 组合（C‑TPT + A‑TPT），在 DTD、Flowers102 和 UCF101 上进一步降低 ECE，说明角度多样性与基于 L2 距离的分散策略在几何上是互补的。不同提示模板初始化（如 "a photo of the cool [CLS]" 和 "an example of [CLS]"）下，A‑TPT 仍保持最低平均 ECE，且随机种子间 ECE 标准差极低（ViT‑B/16 下 0.08‑0.15），表明校准性能对初始化不敏感且可复现。

**高语义重叠下的表现与局限** 在类别语义高度重叠的细粒度数据集（如 Flower102、Aircraft）上，A‑TPT 偶尔会导致准确率轻微下降（<1‑2%），但 ECE 则从 9.04 大幅降至 2.08。此种准确率的微小退化可归因于最大化角度距离在类间语义邻近时可能产生过强的分离信号，需要与熵最小化的权衡。不过整体而言，A‑TPT 在该类数据集上仍实现了最佳的准确率‑校准平衡。

**重要图表结论**  
- **Table 1 & Table 2**：A‑TPT 在所有设定中取得最低 ECE，打破 C‑TPT 和 O‑TPT 在 N > |D| 时的校准瓶颈。  
- **Figure 4**：A‑TPT 的成对余弦相似度一致最低，验证了角度多样性带来的最大最小角度距离。  
- **Figure 5**：可靠性曲线表明，A‑TPT 的预测置信度与真实准确率最贴合，消除了 C‑TPT 和 O‑TPT 中常见的过度置信或置信不足。  
- **Figure 7**：梯度分析解释了 A‑TPT 的几何优势——恒定的梯度范数避免了 O‑TPT 在向量靠近时的优化停滞。  
- **Figure 14**：Pareto 前沿证实 A‑TPT 在不损失准确率的前提下取得最优校准，方法具有真实的增益而非指标间折衷。



## 定位与知识库关联

### 从分散到均匀：A-TPT在测试时提示调优谱系中的位置

测试时提示调优（TPT）的校准研究经历了三条关键路径：**平均文本特征分散（C‑TPT）**、**正交性约束（O‑TPT）**，以及本文提出的**角度多样性（A‑TPT）**。C‑TPT通过最大化文本特征到质心的平均L2距离来推动特征分离，然而这种全局分散策略仅保证特征不重叠，无法控制特征之间的相对位置，尤其在类别数超过嵌入维度时，特征被迫集中在超球面局部区域，导致校准误差居高不下（ECE 5.13，Table 1 Group 1）。O‑TPT则施加硬性的成对正交约束，意图均匀分离；但当类别数 **`N > |D|`** 时，在高维空间中不可能同时满足所有特征两两正交，约束冲突反而造成混乱，且在特征角度趋近于零时梯度消失，优化陷入停滞（Figure 7）。这两种方案共同面对一个结构瓶颈：**没有显式建模文本特征在单位超球面上的均匀角度分布**。

A‑TPT直指这一瓶颈，将问题重铸为**Tammes最佳填充**——最大化归一化文本特征之间的最小成对角度距离（Eq. 1）。该目标不追求绝对正交或简单的距离分散，而是迫使所有特征在高维空间中尽可能等角分离，从而在任何类别数条件下都能充分利用嵌入空间的表达能力。因果调节的核心是 `λ · (−AD)` 正则项，它在TPT的熵最小化过程中持续拉升最小角距，使得文本特征分布的均匀性显著增强（Figure 4）。正因如此，A‑TPT在同时满足两类场景（`N > |D|` 与 `N < |D|`）的整体ECE降至3.26，而C‑TPT和O‑TPT分别为5.42和4.36（Table 1）。值得注意的是，这种增益并非以牺牲准确率为代价——Pareto前沿分析证实A‑TPT在准确率‑校准误差平面上严格占优于所有基线（Figure 14，附录）。

A‑TPT的另一个关键改进在于**优化稳定性**。O‑TPT使用余弦相似度（等价于角度的余弦）作为损失，其梯度范数正比于 `sin(θ)/||e||`，当 `θ → 0` 时梯度消失，无法有效推开相近的特征。A‑TPT直接优化角度 `θ`，其梯度范数恒为 `1/||e||`（Eq. 4 附录），即使特征极度靠近也能提供持续且一致的梯度信号（Figure 7），确保了优化的鲁棒性。同时，为避免 `arccos` 在输入 `x → ±1` 时的梯度爆炸，实现中采用了 `[-0.99999, 0.99999]` 的钳位处理（附录A.5），保证了数值稳定性。

从与监督方法的集成来看，A‑TPT表现出极强的**即插即用性**。它能与CoOp、CoCoOp等有监督提示调优方法无缝组合，将平均ECE进一步压低至3.63和3.22（Table 7）。此外，A‑TPT还可以与C‑TPT的分散损失互补，构成C‑TPT + A‑TPT，在DTD、Flowers102等数据集上获得额外的校准增益（Table 16）。

### 适用边界与条件

A‑TPT的有效性跨越了三个关键维度：

- **类别数‑嵌入维度关系无关**：无论 `N > |D|` 还是 `N < |D|`，A‑TPT均保持最低ECE（Group 1 2.92，Group 2 3.60；Table 1），而O‑TPT在 `N > |D|` 时失效。这使得A‑TPT适用于从细粒度小鸟分类（CUB‑200, N=200）到大规模通用分类（ImageNet, N≈1000）的各类任务。
- **骨干网络鲁棒**：在CLIP ViT‑B/16（512‑d）和CLIP RN50（1024‑d）两个主流视觉骨干上均复现了相似的校准优势（Table 2），表明方法独立于图像特征的编码方式。
- **分布偏移鲁棒**：面对ImageNet‑V2、ImageNet‑A、ImageNet‑R及ImageNet‑Sketch等自然分布偏移数据集，A‑TPT平均ECE为3.92，比C‑TPT（5.82）和O‑TPT（4.88）显著更低（Table 3），证明其校准能力在分布外样本上同样保持有效。
- **领域迁移**：在医学图像（ISIC 2018）上结合FPT微调，A‑TPT将ECE从0.1381降至0.0794（Table 4），显示出跨领域的泛化潜力。

此外，A‑TPT对提示模板初始化不敏感，在不同手工提示（如"a photo of the cool [CLS]"和"an example of [CLS]"）下均稳定输出最低平均ECE（Table 14 & 15），且多次随机运行的ECE标准差极低（0.08–0.15；Table 12），说明方法的内生稳健性。

### 已知局限与代价

尽管校准性能突出，A‑TPT存在以下局限：

1. **固定正则化系数**：`λ` 在所有测试实例上一律设为80.0，缺乏针对不同数据集或样本的动态自适应机制。在语义高度重叠的细粒度类别上（如某些鸟类或花卉子类），文本特征本身区分度有限，强制施加均匀角度分布偶尔会导致轻微精度下降（1–2个百分点；Table 17），但整体准确率仍保持可比。此时固定 `λ` 可能不是最优折中。
2. **数值稳定性的工程成本**：角度损失依赖 `arccos` 操作，需通过输入钳位避免其导数在 ±1 处爆炸；这一处理本身简单，但表明该方法对特征接近同向的极端情况较为敏感。
3. **计算开销与类别数的平方关系**：角度多样性计算需要评估 `N(N−1)/2` 个成对角度距离。在类别数极大（如 `N>10k`）时，计算和内存开销可能成为瓶颈，原文虽称在细粒度任务上开销可忽略，但未讨论极端类别数场景的可扩展性。
4. **单纯依赖文本特征分布**：A‑TPT仅通过调整文本特征的几何关系来修正校准，没有引入图像侧的结构化先验或类间语义关系图，这可能限制了在视觉域剧烈变化（如强遮挡、罕见视角）时的上限。

### 后续工作与开放问题

围绕A‑TPT的核心洞察，仍有若干方向亟待探索：

- **自适应的正则化调度**：能否根据测试样本的置信度谱或特征分布的当前状态，动态调节 `λ` 的大小？这可以在不牺牲准确性的前提下进一步压低ECE，尤其在语义重叠类上避免过度正则化。该问题已在附录中被作者列为开放问题（part 005）。
- **提示模板的系统设计**：当前提示模板来自手工设计或简单变体，未来可研究如何从几何角度出发（如结合Tammes问题的构造解）直接初始化文本特征，使初始状态即具备高角度多样性，减少优化的迭代步数。
- **扩展到多模态和更大类别量**：在百万级类别或开放词汇检测任务中，A‑TPT能否保持计算可行并带来校准收益，需要通过近似近邻搜索或分治策略来验证。
- **校准‑公平性联合评估**：当类别分布不均或存在子群体时，角度多样性是否会平等地改进所有类别的校准，抑或对稀见类造成负面干扰，值得结合公平性指标（如ECE的每类分解）深入研究。
- **理论与几何支撑**：A‑TPT本质上求解Tammes问题，但其在非均匀类别先验或层次化分类树中的最优填充形态尚无理论描述，这可为设计更精细的权重方案提供依据。

综合而言，A‑TPT凭借角度多样性这一简单而本质的几何先验，在测试时提示调优中建立了新的校准基线。它不仅统一并超越了前代分散和正交策略，而且以即插即用的形式嵌入更广泛的提示学习框架，为视觉‑语言模型的不确定性校准开辟了从特征分布均匀性入手的可行路径。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_TPT_Angular_Diversity_Calibration_Properties_for_Test_Time_Prompt_Tuning_of_Vision_Language_Models.pdf

![[paperPDFs/ICLR_2026/A_TPT_Angular_Diversity_Calibration_Properties_for_Test_Time_Prompt_Tuning_of_Vision_Language_Models.pdf]]

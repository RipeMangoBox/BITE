---
title: Advancing Image Classification with Discrete Diffusion Classification Modeling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Advancing_Image_Classification_with_Discrete_Diffusion_Classification_Modeling.pdf
project_link: null
code_link: "https://github.com/omerb01/didicm"
aliases:
- DDCMD
- AICDDCM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将分类问题转化为离散扩散过程，通过对条件后验分布 P(c|y) 建模，利用 Concrete Score 执行分数匹配，从而显式地捕捉和减少预测不确定性。
primary_logic: 图像分类可视为从均匀噪声分布向类别后验分布的逆扩散过程；利用 Concrete Score 矩阵的秩一性质，只需单次模型调用即可高效模拟逆向过程，在保持可处理性的同时大幅提升高不确定性下的分类精度。
claims:
- DiDiCM (DiDiRN-50) 在所有不确定性设置下均优于标准 ResNet-50 分类器，且性能差距随不确定性增大而扩大。
- 在最高不确定性条件（分辨率 56、25% 训练数据）下，DiDiCM 相比标准分类器 Top‑1 精度提升 13.1%，Top‑5 精度提升 13.8%。
- DiDiCM-CP 仅需两步扩散（2 NFEs）即可在 56 分辨率全量 ImageNet 上达到接近理论上限的 Top‑1 精度。
- 所提出的 DiDiCM 损失是条件分数熵损失的变体，对于分类任务保持完全可处理，避免了语言域离散扩散中的可处理性障碍。
---

# Advancing Image Classification with Discrete Diffusion Classification Modeling

> [!tip] 核心洞察
> 图像分类可视为从均匀噪声分布向类别后验分布的逆扩散过程；利用 Concrete Score 矩阵的秩一性质，只需单次模型调用即可高效模拟逆向过程，在保持可处理性的同时大幅提升高不确定性下的分类精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 离散扩散分类建模推进图像分类 |
| 英文题名 | Advancing Image Classification with Discrete Diffusion Classification Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Belhasin_Advancing_Image_Classification_with_Discrete_Diffusion_Classification_Modeling_CVPR_2026_paper.html) · [Code](https://github.com/omerb01/didicm) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Discrete Diffusion Classification Modeling (DiDiCM) |
| Dataset | ImageNet |

> [!tip] 效果简介
> - ImageNet (56×56, 25% 训练比, Weak Aug) 上，Top-1 Accuracy 57.92 vs 44.86 (+13.06)；Top-5 Accuracy 80.26 vs 66.46 (+13.80)。
> - ImageNet (224×224, 100% 训练比, Strong Aug) 上，Top-1 Accuracy 80.40 vs 80.42 (-0.02)；Top-5 Accuracy 95.29 vs 94.60 (+0.69)。

## 概要

标准图像分类器通过交叉熵损失直接学习从图像到类别分布的映射，在训练数据充足、图像质量良好的条件下表现优异。然而，当面临图像损坏、低分辨率或训练数据稀缺等引入高度不确定性的场景时，这类确定性预测范式暴露出根本性缺陷——模型缺乏对预测不确定性的显式建模能力，导致性能急剧下降。

针对这一瓶颈，本文提出**离散扩散分类建模（Discrete Diffusion Classification Modeling, DiDiCM）**，将图像分类重新定义为从均匀噪声分布向类别后验分布 $P(\mathbf{c}|\mathbf{y})$ 的逆扩散过程。其核心洞察在于：分类任务中的 Concrete Score 矩阵具有秩一性质，使得逆向扩散过程仅需单次模型调用即可高效构建，在保持计算可处理性的同时，显式捕捉并逐步消解预测不确定性。

DiDiCM 提供两种推理变体：**DiDiCM-CP** 在类别概率空间上进行扩散，计算效率高但内存开销与类别数 $K$ 的平方成正比；**DiDiCM-CL** 则在离散类别标签空间上扩散，内存友好但需要更多次模型评估（NFEs），形成灵活的计算-内存权衡。

实验结果表明，DiDiCM 在 ImageNet 上展现出显著且鲁棒的优势：
- 在高不确定性条件下（分辨率 56、25% 训练数据），DiDiCM 相比标准 ResNet-50 分类器在 Top-1 精度上提升 **13.06%**，Top-5 精度提升 **13.80%**（Table 1）。
- DiDiCM-CP 仅需 **两步扩散（2 NFEs）** 即可在 56 分辨率全量数据上达到接近理论上限的 Top-1 精度（Figure 4b）。
- 在低不确定性条件下（224 分辨率、全量数据、强增强），DiDiCM 与标准分类器性能持平（Top-1 差异仅 -0.02%），证明其不会损害标准场景下的分类能力。

DiDiCM 的方法论定位介于扩散生成模型与判别式分类器之间：它借鉴了连续时间离散扩散的分数匹配框架，但将生成式扩散中存在的可处理性障碍转化为分类任务中的秩一结构优势，为高不确定性场景下的图像分类开辟了新的技术路径。



### 分类任务中的不确定性瓶颈

图像分类是计算机视觉的核心任务，其标准范式是通过深度神经网络直接预测类别后验分布 $P(\mathbf{c}|\mathbf{y})$。然而，这一范式隐含假设训练数据充足且观测质量理想。当图像分辨率降低、训练数据稀缺或增强策略受限时，标准分类器面临严重的不确定性——输入信息不足以唯一确定类别标签，而交叉熵损失训练的分类器缺乏对预测置信度的显式建模能力，导致性能急剧退化。

这一瓶颈的本质在于：**标准分类器将分类视为从图像到类别的确定性映射，忽略了观测过程固有的信息损失与不确定性**。在低分辨率、小样本等场景下，不同类别可能产生高度相似的观测，此时正确的分类策略应当是输出更“保守”但更准确的后验分布，而非强行收敛到单一类别。然而，交叉熵损失驱动的训练过程天然倾向于将概率质量集中到最可能的类别上，在高不确定性条件下反而放大了错误预测的风险。

### 现有方法的局限

当前应对分类不确定性的主流策略可分为两类：**数据增强**与**架构改进**。前者通过更强的增强策略（如 RandAugment、MixUp）提升模型的鲁棒性，后者则通过引入贝叶斯推理、集成学习或校准技术来改善不确定性估计。然而，这些方法存在共同局限：它们仍然依赖于单次前向传播输出类别分布，缺乏对后验分布结构的显式建模。换言之，它们试图让模型“更聪明地”处理不确定性，却没有改变分类器本身“看一眼就决策”的根本机制。

### 离散扩散带来的新视角

扩散模型在连续域生成任务中取得了巨大成功，其核心思想是通过迭代去噪逐步从噪声分布恢复目标分布。近期，离散扩散模型将这一框架扩展到离散状态空间，为语言建模等任务提供了新的生成范式。然而，将离散扩散应用于分类任务面临一个关键障碍：**可处理性**。在语言域中，离散扩散的逆过程需要估计复杂的分数矩阵，导致训练和推理的计算代价高昂，且难以保证数值稳定性。

本文的核心洞察在于：**分类任务中的分数矩阵天然具有秩一结构**。具体而言，当扩散过程定义在类别标签空间上时，其 Concrete Score 矩阵 $S_t$ 可分解为前向分布向量与其倒数的外积：

$$
S_t = q(\mathbf{c}_t|\mathbf{y})\left(\frac{1}{q(\mathbf{c}_t|\mathbf{y})}\right)^T
$$

这一性质使得逆扩散过程只需单次模型调用即可完整构建分数矩阵，从根本上规避了语言域离散扩散的可处理性难题。基于此，本文提出 **离散扩散分类建模（Discrete Diffusion Classification Modeling, DiDiCM）**，将图像分类重新定义为从均匀噪声分布向类别后验分布的逆扩散过程，通过迭代去噪显式捕捉和减少预测不确定性。

### 本文动机与贡献

DiDiCM 的动机源于一个朴素的问题：**如果分类器可以“反复思考”而非“一眼定论”，能否在高不确定性场景下做出更准确的判断？** 这一直觉与人类认知过程高度吻合——面对模糊或信息不足的输入时，人类倾向于反复推敲、逐步排除不可能选项，而非仓促给出确定答案。

基于此动机，本文做出以下核心贡献：

1. **提出 DiDiCM 框架**：将分类问题形式化为离散扩散过程，定义前向加噪、逆向去噪及对应的训练目标，为分类任务提供全新的建模范式。
2. **设计两种推理策略**：DiDiCM-CP（扩散类别概率）与 DiDiCM-CL（扩散离散类别标签），在计算复杂度与内存开销之间提供灵活权衡。
3. **构建 DiDiRN 架构**：在 ResNet 骨干中嵌入轻量级扩散条件模块，以最小架构改动支持扩散过程的步数和噪声标签条件。
4. **验证有效性**：在 ImageNet 上系统验证 DiDiCM 在不同不确定性设置下的性能优势，尤其在高不确定性场景下相比标准分类器实现显著提升（Table 1，最高提升 13.1% Top‑1 精度）。



## 核心方法与创新机理

### 1. 从交叉熵到条件分数熵：训练目标的根本转变

标准分类器（如 **ResNet-50**，He et al., CVPR 2016）使用交叉熵损失直接学习从图像到类别分布的映射，其训练目标为最小化预测分布与真实 one-hot 标签之间的 KL 散度。DiDiCM 的核心创新在于将训练目标替换为基于**条件分数熵**的分数匹配损失（式5）：

$$\mathcal{L}_{\mathrm{DiDiCM}}(\theta) := \mathbb{E}_{t \sim \mathcal{U}([0,1])} \left[ \frac{\sigma_t}{K} \Big( \mathbf{1}^T A(S_t(\cdot, \mathbf{c}_t; \mathbf{y})) + \mathbf{1}^T s_\theta(\mathbf{y}, \mathbf{c}_t, t) - S_t(\cdot, \mathbf{c}_t; \mathbf{y})^T \log s_\theta(\mathbf{y}, \mathbf{c}_t, t) \Big) \right]$$

其中 $A(a) = a(\log a - 1)$ 保证损失的非负性。与交叉熵损失直接优化类别预测不同，DiDiCM 损失训练网络 $s_\theta$ 去逼近 **Concrete Score 矩阵** $S_t$ 的列向量——该矩阵刻画了前向扩散过程中各类别之间的转移关系。这一转变使得模型不再仅学习“图像→类别”的静态映射，而是学习“给定图像和噪声类标签，预测去噪方向”的动态过程，从而显式建模预测中的不确定性。

### 2. 网络结构的条件化扩展：DiDiRN

标准 ResNet-50 仅接收图像作为输入，输出类别 logits。DiDiCM 提出的 **DiDiRN-50** 在保留 ResNet 核心图像处理组件（蓝色模块，Figure 3）的基础上，新增了**扩散条件模块**（绿色模块，Figure 3）：在每个残差块中嵌入 SiLU 激活 + 线性层，将扩散时间步 $t$ 和噪声类标签 $\mathbf{c}_t$ 作为条件注入网络。这使得同一骨干网络能够感知扩散过程的当前状态，从而输出与时间步和噪声水平相关的 Concrete Score 预测 $s_\theta(\mathbf{y}, \mathbf{c}_t, t)$。该条件化扩展是轻量级的——仅增加少量参数，却使网络从“静态分类器”转变为“扩散去噪器”。

### 3. 推理范式：从单次前向传播到多步逆扩散

标准分类器的推理仅需一次前向传播，直接输出类别概率分布。DiDiCM 的推理则模拟从均匀噪声分布到后验分布 $P(\mathbf{c}|\mathbf{y})$ 的**逆扩散过程**（Section 5.1, 5.2, Algorithm 2, 3）：

- **起点**：$p(\mathbf{c}_1|\mathbf{y}) = \text{Uniform}(K)$，即完全不确定的均匀分布。
- **过程**：通过多步迭代，利用预测的 Concrete Score 逐步“去噪”，逼近真实后验分布。
- **终点**：$p_\theta(\mathbf{c}_0|\mathbf{y})$ 作为最终分类预测。

这一范式的关键使能技术是 **Concrete Score 矩阵的秩一性质**（式7）：

$$S_t = q(\mathbf{c}_t | \mathbf{y}) \left( \frac{1}{q(\mathbf{c}_t | \mathbf{y})} \right)^T$$

该性质意味着完整的 $K \times K$ 分数矩阵可由单个 $K$ 维向量重建，因此每个扩散步骤仅需**一次模型调用**即可高效模拟逆向过程，在保持可处理性的同时实现了对不确定性的逐步消解。

### 4. 双模式推理：概率扩散与标签扩散

DiDiCM 提供两种互补的推理模式，在计算与内存之间灵活权衡：

- **DiDiCM-CP（Class Probabilities）**：在概率空间进行扩散，利用秩一性质，每步只需一次模型调用，计算效率高但需维护 $O(K^2)$ 的转移矩阵。
- **DiDiCM-CL（Class Labels）**：在离散标签空间进行扩散，通过采样具体类别标签来近似后验，内存开销更低，但需要更多模型调用（NFEs）以达到同等精度。

这种双模式设计使得 DiDiCM 可根据实际部署场景（内存受限 vs. 计算受限）灵活选择推理策略，而标准分类器不具备此类灵活性。

### 5. 创新总结：从“预测答案”到“消解不确定性”

上述四个 changed slots 共同构成了一条完整的创新链条：

| 维度 | 标准分类器 (ResNet-50) | DiDiCM (DiDiRN-50) |
|------|----------------------|-------------------|
| **训练目标** | 交叉熵损失 $\ell_{CE}$ | DiDiCM 损失（条件分数熵） |
| **网络结构** | 无时间/噪声条件 | 残差块中嵌入扩散条件模块 |
| **模型输入** | 仅图像 $\mathbf{y}$ | 图像 + 噪声标签 $\mathbf{c}_t$ + 时间 $t$ |
| **推理过程** | 单次前向传播 | 多步逆扩散迭代去噪 |

其本质是将分类问题重新定义为**从均匀噪声分布向类别后验分布的逆扩散过程**，通过分数匹配显式建模并逐步消解预测不确定性。这一框架在最困难的不确定性条件下（56×56 分辨率、25% 训练数据）带来了 **Top-1 精度 +13.06%、Top-5 精度 +13.80%** 的显著提升（Table 1），而在低不确定性条件下（224×224、全量数据、强增强）保持与标准分类器相当的精度（Top-1: 80.40 vs. 80.42），证明了该创新的有效性并非以牺牲常规性能为代价。



DiDiCM 将图像分类重新定义为**从均匀噪声分布到类别后验分布的逆扩散过程**。其核心洞察在于：分类器需要建模的并不是单一类别，而是给定图像 $y$ 下的完整后验分布 $P(\mathbf{c} \mid \mathbf{y})$。标准分类器以交叉熵损失直接预测该类分布，在高不确定性场景（如低分辨率、数据稀缺）下缺乏对不确定性的显式建模能力，导致性能显著下降。DiDiCM 通过引入离散扩散机制，将这一不确定性逐步“去噪”，从而在推理时获得更可靠的后验估计。

### 整体流程

DiDiCM 的 pipeline 由三个核心阶段构成：**训练阶段**学习 Concrete Score 预测器；**推理阶段**从均匀分布出发，通过多步逆扩散模拟逼近后验分布；根据任务需求，推理可选择**类别概率扩散（DiDiCM‑CP）**或**离散标签扩散（DiDiCM‑CL）**两种策略。

#### 1. 训练阶段：学习 Concrete Score

训练的目标是让网络学会预测**Concrete Score 向量** $s_\theta(\mathbf{y}, \mathbf{c}_t, t)$，该向量近似真实分数矩阵 $S_t$ 的列。训练循环（Algorithm 1）如下：

- **输入**：图像 $\mathbf{y}$、真实类别标签 $\mathbf{c}_0$（one‑hot 形式）。
- **前向扩散**：采样时间步 $t \sim \mathcal{U}([0,1])$，通过闭式解 $q(\mathbf{c}_t \mid \mathbf{y}) = U \exp(\bar{\sigma}_t \Lambda) U^{-1} \cdot q(\mathbf{c}_0 \mid \mathbf{y})$ 计算噪声分布，并从中采样噪声类标签 $\mathbf{c}_t$。
- **网络前向**：将图像 $\mathbf{y}$、噪声标签 $\mathbf{c}_t$ 和时间步 $t$ 输入 DiDiRN 网络，输出预测分数 $s_\theta(\mathbf{y}, \mathbf{c}_t, t)$。
- **损失计算**：使用 DiDiCM 损失（式 5）——条件分数熵损失的变体——度量预测分数与真实分数之间的差异，并按噪声水平 $\sigma_t$ 加权。

这一训练目标的优势在于：对于分类任务保持**完全可处理**，避免了语言域离散扩散中因大词汇表带来的可处理性障碍。

#### 2. 推理阶段：逆扩散去噪

推理从均匀分布 $p(\mathbf{c}_1 \mid \mathbf{y}) = \mathcal{U}\{1,\dots,K\}$ 开始，通过 $T$ 步逆扩散逐步逼近后验分布 $p_\theta(\mathbf{c}_0 \mid \mathbf{y})$。每一步利用预测的 Concrete Score 构建近似转移矩阵 $\overline{Q}_t^\theta$，更新当前分布：

$$p_\theta(\mathbf{c}_{t-\Delta t} \mid \mathbf{y}) = \overline{Q}_t^\theta \cdot p_\theta(\mathbf{c}_t \mid \mathbf{y})$$

核心效率保障来自分数矩阵的**秩一性质**（式 7）：$S_t = q(\mathbf{c}_t \mid \mathbf{y}) \bigl(\frac{1}{q(\mathbf{c}_t \mid \mathbf{y})}\bigr)^T$。这意味着每步扩散仅需**单次模型调用**即可构建完整的转移矩阵，避免了 $O(K^2)$ 次独立评估。

#### 3. 双模式推理：DiDiCM‑CP 与 DiDiCM‑CL

DiDiCM 提供两种推理模式，在计算与内存之间提供灵活权衡：

- **DiDiCM‑CP（类别概率扩散，Algorithm 2）**：直接对后验概率向量进行扩散。每步通过归一化 Concrete Score 得到近似前向分布 $q_\theta(\mathbf{c}_t \mid \mathbf{y})$（式 8），再结合秩一性质构建转移矩阵。计算效率高，但需维护 $O(K^2)$ 的转移矩阵，类别数极大时内存压力增大。
- **DiDiCM‑CL（离散标签扩散，Algorithm 3）**：在离散标签空间中进行扩散，每步从当前分布中采样标签并迭代更新。内存开销更低，但需要更多顺序计算步骤。

### 网络架构：DiDiRN

为支持扩散过程的条件建模，论文在 ResNet‑50 基础上设计了 **DiDiRN‑50**（Figure 3）。架构保留 ResNet 的全部核心图像处理组件（蓝色部分），仅在每个残差块中新增轻量级**条件嵌入模块**（绿色部分）：使用 SiLU 激活 + 线性层将扩散时间步 $t$ 和噪声类标签 $\mathbf{c}_t$ 编码为特征调制信号，注入到残差路径中。这一设计使 DiDiRN‑50 与 ResNet‑50 在图像处理能力上直接可比，同时具备处理扩散条件的能力。

![[assets/figures/papers/paper_list_l2067_https_openaccess_thecvf_com_content_CVPR2026_html_Belhasin_Advancing_Ima/figures/003_Figure_3.jpg]]
*Figure 3: The Discrete Diffusion Residual Network (DiDiRN) architecture. DiDiRN preserves the core image-processing components of ResNet while adding conditioning modules to support the diffusion process of DiDiCM. Original ResNet modules are shown in blue, and the newly introduced components in green*

### 模块关系与数据流

整体 pipeline 中各模块的协作关系可概括为：

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| 图像编码器（ResNet 骨干） | 提取图像高层视觉特征 | 图像 $\mathbf{y}$ | 特征图 |
| 噪声标签与时间步条件模块 | 注入扩散过程信息 | $t$, $\mathbf{c}_t$ | 调制信号 |
| 分数预测头 | 输出 Concrete Score 向量 | 融合特征 | $s_\theta(\mathbf{y}, \mathbf{c}_t, t)$ |
| 逆扩散模拟器 | 逐步恢复后验分布 | 初始均匀分布、分数预测器 | $p_\theta(\mathbf{c}_0 \mid \mathbf{y})$ |

训练时，前三个模块联合优化 DiDiCM 损失；推理时，逆扩散模拟器驱动整个去噪过程，每步调用一次分数预测网络。实验表明，仅需 **2 步扩散（2 NFEs）**，DiDiCM‑CP 即可在 56×56 分辨率全量 ImageNet 上达到接近理论上限的 Top‑1 精度（Figure 4b），验证了框架的高效性。



### 问题形式化：分类作为条件后验估计

标准图像分类器直接学习从图像 $y$ 到类别标签 $c$ 的映射，输出 $P(c|y)$ 的点估计。DiDiCM 将分类重新定义为**从均匀噪声分布向类别后验分布 $P(c|y)$ 的逆扩散过程**。核心瓶颈在于：当图像存在损坏、分辨率降低或训练数据稀缺时，观测 $y$ 携带的信息不足，导致 $P(c|y)$ 具有高熵（高不确定性），标准分类器的点估计在此场景下显著退化。

DiDiCM 通过**显式建模条件后验分布的扩散过程**来捕捉这种不确定性：在前向过程中逐步向真实后验注入噪声，在逆向过程中学习从噪声恢复后验。

### 前向扩散过程（Forward Process）

前向过程定义在连续时间 $t \in [0,1]$ 上，描述噪声类别分布 $q(c_t|y)$ 的演化，遵循连续时间马尔可夫过程：

$$
\frac{d q(\mathbf{c}_t | \mathbf{y})}{d t} = R_t \cdot q(\mathbf{c}_t | \mathbf{y}) \quad \text{s.t.} \quad R_t := \sigma_t (\mathbf{1}\mathbf{1}^T - K I)
$$

**变量含义**：
- $q(c_t|y)$：时间 $t$ 时的噪声类别分布（$K$ 维概率向量）
- $R_t$：速率矩阵，控制类别间的转移速率
- $\sigma_t$：噪声调度函数，控制噪声注入速度
- $K$：类别总数
- $\mathbf{1}$：全 1 向量

该速率矩阵的设计保证了前向过程最终收敛到均匀分布。利用 $R_t$ 的特征分解，任意噪声水平下的前向分布可通过**闭式解析解**高效计算：

$$
q(\mathbf{c}_t | \mathbf{y}) = U \exp\left(\bar{\sigma}_t \Lambda\right) U^{-1} \cdot q(\mathbf{c}_0 | \mathbf{y})
$$

其中 $U$ 和 $\Lambda$ 为 $R_t$ 的特征向量矩阵和特征值对角矩阵，$\bar{\sigma}_t = \int_0^t \sigma_s ds$ 为累积噪声。$q(c_0|y)$ 为真实后验分布（one-hot 编码的真实类别）。

### 逆向扩散过程（Reverse Process）

逆向过程的目标是从纯噪声分布 $q(c_1|y) = \text{Uniform}(K)$ 出发，逐步恢复后验分布 $p(c_0|y)$。逆向时间 ODE 定义为：

$$
\frac{d p(\mathbf{c}_{1-t} | \mathbf{y})}{d t} = \overline{R}_{1-t} \cdot p(\mathbf{c}_{1-t} | \mathbf{y})
$$

其中逆向速率矩阵 $\overline{R}_t$ 依赖于**分数矩阵（Concrete Score Matrix）** $S_t$：

$$
\overline{R}_t := S_t \odot R_t - \operatorname{diag}\left(\mathbf{1}^T (S_t \odot R_t)\right)
$$

**分数矩阵 $S_t$ 的核心性质——秩一分解**：

$$
S_t = q(\mathbf{c}_t | \mathbf{y}) \left(\frac{1}{q(\mathbf{c}_t | \mathbf{y})}\right)^T
$$

$S_t$ 是前向分布 $q(c_t|y)$ 与其逐元素倒数的外积，秩为 1。这一性质意味着：**只需单次模型调用即可构建完整的 $S_t$ 矩阵**，使逆扩散过程在计算上保持可处理。

### 分数预测网络与训练目标

DiDiCM 训练一个参数化模型 $s_\theta(y, c_t, t)$ 来近似 $S_t$ 的列向量：

$$
s_\theta(y, c_t, t) \approx [S_t(1, c_t; y), \dots, S_t(K, c_t; y)]^T
$$

**DiDiCM 损失函数**是条件分数熵损失的变体，通过分数匹配学习 Concrete Score：

$$
\mathcal{L}_{\mathrm{DiDiCM}}(\theta) := \mathbb{E}_{t \sim \mathcal{U}([0,1])} \left[ \frac{\sigma_t}{K} \Big( \mathbf{1}^T A(S_t(\cdot, \mathbf{c}_t; \mathbf{y})) + \mathbf{1}^T s_\theta(\mathbf{y}, \mathbf{c}_t, t) - S_t(\cdot, \mathbf{c}_t; \mathbf{y})^T \log s_\theta(\mathbf{y}, \mathbf{c}_t, t) \Big) \right]
$$

**变量含义**：
- $t \sim \mathcal{U}([0,1])$：从均匀分布采样扩散时间步
- $\sigma_t$：噪声权重，控制不同噪声水平的损失贡献
- $A(a) = a(\log a - 1)$：逐元素函数，保证损失非负性
- $S_t(\cdot, c_t; y)$：真实分数矩阵的第 $c_t$ 列
- $s_\theta(y, c_t, t)$：网络预测的分数向量

该损失**对分类任务保持完全可处理**，避免了语言域离散扩散模型中因大词汇表导致的可处理性障碍——原因在于类别数 $K$（如 ImageNet 的 1000 类）远小于语言模型的词汇表规模。

### 推理：两种逆扩散模拟策略

#### DiDiCM-CP（Class Probabilities 扩散）

利用 $S_t$ 的秩一性质，DiDiCM-CP 通过以下步骤高效执行逆向扩散：

1. 选择锚点类别 $j$（通常选 $j = \arg\min p_\theta(c_t|y)$ 以获得最佳性能）
2. 单次模型调用获取 $s_\theta(y, j, t)$
3. 归一化得到近似前向分布：

$$
q_\theta(\mathbf{c}_t | \mathbf{y}) = \frac{s_\theta(\mathbf{y}, j, t)}{\sum_{i=1}^K s_\theta(\mathbf{y}, j, t)_i}
$$

4. 利用 $q_\theta$ 重构完整 $S_t$ 矩阵，执行逆向扩散步：

$$
p_\theta(\mathbf{c}_{t-\Delta t} | \mathbf{y}) = \overline{Q}_t^\theta \cdot p_\theta(\mathbf{c}_t | \mathbf{y})
$$

DiDiCM-CP 每步仅需 **1 次网络前向传播（1 NFE）**，计算效率高，但需维护 $O(K^2)$ 的转移矩阵。

#### DiDiCM-CL（Class Labels 扩散）

DiDiCM-CL 直接对离散类别标签进行采样式逆向扩散，每步需 $O(K)$ 次模型调用以计算所有可能类别的转移概率，内存开销小但计算量更大。两种策略形成**计算-内存权衡**：CP 适合 $K$ 适中场景，CL 适合类别数极大的场景。

### 网络架构：DiDiRN

DiDiRN 在 ResNet-50 骨干上扩展（Figure 3），保留其核心图像处理组件（蓝色部分），在每个残差块中新增**扩散条件模块**（绿色部分）：
- **时间步嵌入**：将扩散时间 $t$ 通过 SiLU 激活 + 线性层映射为特征偏移
- **噪声标签嵌入**：将当前噪声类别 $c_t$ 的 one-hot 编码通过线性层映射为特征偏移
- 两类嵌入相加后注入残差路径，使网络感知当前扩散状态

相比标准 ResNet-50，DiDiRN 的输入从单一的图像 $y$ 扩展为三元组 $(y, c_t, t)$，输出从类别 logits 变为分数向量 $s_\theta(y, c_t, t)$。

### 补充图表

![[assets/figures/papers/paper_list_l2067_https_openaccess_thecvf_com_content_CVPR2026_html_Belhasin_Advancing_Ima/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of our DiDiCM-CP showing the evolution of the top-5 class label probabilities over time for three images, demonstrating different classification challenges*



## 实验与关键发现

### 主实验：不确定性条件下的分类精度

DiDiCM 的核心设计目标是在图像损坏、数据稀缺等高不确定性场景下提升分类鲁棒性。Table 1 系统比较了 DiDiCM（8 步扩散）与标准 ResNet-50 分类器在多种不确定性组合下的表现，涵盖图像分辨率（224×224、112×112、56×56）、训练数据比例（100%、50%、25%）和增强策略（Weak Aug、Strong Aug）三个维度的正交变化。

![[assets/figures/papers/paper_list_l2067_https_openaccess_thecvf_com_content_CVPR2026_html_Belhasin_Advancing_Ima/figures/004_Table_1.jpg]]
*Table 1: ImageNet Top-1 and Top-5 Accuracy: DiDiCM (8 steps) vs. standard classifiers under varying uncertainty. Weak Aug uses standard PyTorch augmentations [37], Strong Aug follows the state-of-the-art ResNet recipe [46] (see Appendix F for more details). Best top-1 and top-5 per column are bolded; Weak Aug models outperforming Strong Aug classifiers are highlighted in green*

**高不确定性场景下的显著增益。** 在最高不确定性条件（56×56 分辨率、25% 训练数据、Weak Aug）下，DiDiCM 相较标准分类器实现了 **Top‑1 精度 +13.06%（57.92 vs. 44.86）和 Top‑5 精度 +13.80%（80.26 vs. 66.46）** 的提升。随着不确定性降低，增益逐步收窄：在 224×224 分辨率、100% 训练数据、Strong Aug 条件下，Top‑1 精度几乎持平（80.40 vs. 80.42，−0.02%），Top‑5 精度仍保持小幅优势（95.29 vs. 94.60，+0.69%）。这一趋势与 Figure 1 的 Top‑5 精度曲线一致——DiDiCM 在所有不确定性设置下均优于标准分类器，且性能差距随不确定性增大而扩大。

**弱增强下的跨条件优势。** 值得注意的是，使用 Weak Aug 训练的 DiDiCM 在多数高不确定性条件下甚至超过了 Strong Aug 训练的标准分类器。例如，在 56×56 分辨率、25% 训练数据下，Weak Aug DiDiCM 的 Top‑1 精度（57.92）显著高于 Strong Aug 标准分类器（44.86），表明扩散建模引入的不确定性处理能力比更强的数据增强更为有效。这一发现暗示 DiDiCM 在标注数据稀缺或计算资源受限（难以应用强增强）的场景中具有独特价值。

**公平性保障。** 所有对比均使用相同的训练 recipe（Weak Aug 使用标准 PyTorch 增强，Strong Aug 遵循 SOTA ResNet 配方）和相同的不确定性条件。DiDiRN-50 架构直接扩展 ResNet-50，仅在残差块中增加轻量级条件模块（Figure 3），架构对比公平。

### 推理效率分析：NFEs 与精度的权衡

DiDiCM 的推理需要多次顺序模型评估（NFEs），Figure 4b 展示了 NFEs 与 Top‑1 精度的权衡曲线。在 56×56 分辨率、全量 ImageNet 条件下：

- **DiDiCM-CP** 仅需 **2 步扩散（2 NFEs）** 即可达到接近理论上限的 Top‑1 精度，展示了 Concrete Score 矩阵秩一性质带来的高效逆向模拟能力（单次模型调用即可构建完整分数矩阵，见公式 7）。
- **DiDiCM-CL**（基于离散类别标签的扩散）在相同 NFEs 下精度略低于 DiDiCM-CP，但具有更低的内存占用，体现了计算与内存的灵活权衡。
- 随着 NFEs 增加，两种变体的精度均逐步提升并趋于饱和，标准分类器（1 NFE）的精度作为下界参考。

### 消融实验

在 DiDiCM-CP 中，选择哪个类别作为分数模型的输入 $j$ 对性能有影响。消融实验表明，选择 $j = \arg\min p_\theta(\mathbf{c}_t|\mathbf{y})$（即当前分布中概率最小的类别）能获得最佳性能（详见 Appendix B）。这一选择策略的直觉在于：模型对低概率类别的分数预测更富含信息量，有助于逆向过程更有效地修正分布。

### 失败模式与局限性

1. **推理延迟。** 尽管 DiDiCM-CP 仅需 2 NFEs 即可接近饱和性能，相比标准分类器的单次前向传播仍有额外计算开销。在对延迟敏感的应用中，这一代价需要与精度增益进行权衡。

2. **类别数扩展性。** DiDiCM-CP 需维护 $O(K^2)$ 的转移矩阵，当类别数 $K$ 极大（如 $K > 10^6$）时可能面临内存瓶颈。DiDiCM-CL 通过离散标签采样规避了此问题，但牺牲了部分计算效率。

3. **数据集局限性。** 当前实验仅在 ImageNet 上进行，缺乏在更多样化数据集（如医学图像、自动驾驶场景、细粒度分类）上的验证。在这些领域中，不确定性可能来源于不同的损坏类型（如自然损坏、对抗扰动），DiDiCM 的泛化能力尚待检验。

4. **与现有扩散生成分类器的比较缺失。** 当前工作未给出与已有扩散生成分类器（如 Li et al., 2023）的直接定量比较，难以判断 DiDiCM 在扩散分类方法谱系中的相对位置。

### 关键图表结论

- **Figure 1** 确立了 DiDiCM 的核心优势：在所有不确定性设置下 Top‑5 精度均优于标准分类器，且优势随不确定性增大而扩大。
- **Table 1** 提供了完整的量化证据，最高不确定性下 Top‑1 提升 13.06%，Top‑5 提升 13.80%。
- **Figure 4b** 揭示了 DiDiCM-CP 的高效性：2 NFEs 即可逼近理论上限，为实际部署提供了可行的效率-精度平衡点。
- **Figure 2** 通过三张典型图像的可视化，展示了 DiDiCM-CP 逆向扩散过程中 top‑5 类别概率的演变，直观说明了不同分类难度下扩散过程的差异化行为。

![[assets/figures/papers/paper_list_l2067_https_openaccess_thecvf_com_content_CVPR2026_html_Belhasin_Advancing_Ima/figures/001_Figure_1.jpg]]
*Figure 1: ImageNet Top-5 Accuracy: DiDiCM vs. standard classifiers. DiDiRN-50 (comparable to ResNet-50) and ResNet-50 are both trained using the state-of-the-art recipe [46]. DiDiCM shows superior top-5 accuracy across all uncertainty settings*

### 补充图表

![[assets/figures/papers/paper_list_l2067_https_openaccess_thecvf_com_content_CVPR2026_html_Belhasin_Advancing_Ima/figures/005_Figure_4.jpg]]
*Figure 4: (a) DiDiCM (8 steps) vs. standard classifiers under varying uncertainty (see Appendix F for augmentation policy). (b) NFEs vs. top-1 accuracy for DiDiCM-CP, DiDiCM-CL, and the standard classifier at resolution 56 using the full training set. Numbers indicate the sample count used. Red markers denote the best-performing DiDiCM-CP and DiDiCM-CL results*



## 定位与知识库关联

### 与标准分类器的关系

DiDiCM 的直接对标基线是标准交叉熵训练的 ResNet-50 分类器（**He et al., CVPR 2016**）。两者的核心差异在于对分类不确定性的建模方式：

- **标准分类器**：通过交叉熵损失直接学习从图像 y 到类别分布的单步映射，训练目标为 ℓ_CE。推理时仅需一次前向传播，计算效率高，但在图像损坏、低分辨率或数据稀缺等场景下，模型缺乏对预测不确定性的显式建模能力，性能显著退化。
- **DiDiCM**：将分类重构为条件后验分布 P(c|y) 的逆扩散过程。训练目标从交叉熵替换为基于条件分数熵的 DiDiCM 损失（式5），网络结构从纯 ResNet-50 扩展为 DiDiRN-50（在残差块中增加 SiLU+线性层对扩散步和噪声类标签进行条件嵌入）。推理从均匀分布出发，通过多步逆扩散迭代去噪得到后验分布。

关键瓶颈在于：标准分类器在不确定性升高时，单次前向预测缺乏对分布不确定性的逐步修正机制；DiDiCM 通过 Concrete Score 矩阵的秩一性质（式7），使逆扩散过程仅需单次模型调用即可高效构建每步转移矩阵，在保持可处理性的同时大幅提升高不确定性下的分类精度。

### 与扩散生成分类器的关系

近年来，扩散模型在分类任务中的应用已有多项探索，DiDiCM 在以下维度上形成差异化定位：

- **扩散生成分类器（如 Li et al., 2023）**：通常利用连续状态扩散模型对图像空间进行生成建模，再从生成模型中导出分类器。这类方法依赖对图像分布 p(x) 的建模，计算开销大，且分类精度受限于生成质量。
- **DiDiCM**：直接在离散类别空间上定义扩散过程，前向过程为连续时间马尔可夫过程（式1），逆向过程基于分数矩阵的 ODE（式3）。该方法不建模图像生成，而是专注于类别后验分布的逐步精炼，训练目标完全可处理，避免了语言域离散扩散中常见的可处理性障碍。

当前工作尚未给出与已有扩散生成分类器（如 Li et al. 2023）的直接定量比较，这一缺失需要在后续研究中补充。

### 适用边界

DiDiCM 的优势场景与局限边界清晰：

**优势场景**：
- 高不确定性分类任务：低分辨率图像（如 56×56）、数据稀缺（如 25% 训练数据）、弱增强策略下，DiDiCM 相比标准分类器的精度提升显著（Top‑1 提升 13.06%，Top‑5 提升 13.80%）。
- 对 Top‑5 精度敏感的应用：DiDiCM 在所有不确定性设置下均优于标准分类器，且性能差距随不确定性增大而扩大（Figure 1）。

**边界与局限**：
- **推理延迟**：DiDiCM 需要多次顺序模型评估（NFEs），推理延迟高于标准单次前向分类器。即使在 DiDiCM-CP 的最优配置下（2 NFEs），仍需额外计算开销。
- **类别数扩展性**：DiDiCM-CP 需维护 O(K²) 的转移矩阵，当类别数 K 很大时可能受到内存限制。DiDiCM-CL 以计算换内存，但推理效率进一步下降。
- **不确定性类型泛化**：当前实验仅在 ImageNet 上通过分辨率降低、数据缩减和增强策略变化来模拟不确定性，缺乏在自然损坏、对抗扰动、分布外检测等更广泛不确定性类型下的验证。
- **数据集多样性**：实验仅覆盖 ImageNet，缺乏在医学图像、自动驾驶场景、细粒度分类等领域的验证。

### 开放问题

1. **架构升级**：当前 DiDiRN 基于 ResNet-50 扩展，能否设计基于 Transformer 的 DiDiRN 变体以进一步提升分类性能？
2. **推理加速**：如何通过扩散蒸馏（diffusion distillation）大幅减少推理所需 NFEs，同时保持精度优势？DiDiCM-CP 在 2 NFEs 下已接近理论上限，但进一步的加速方案尚未探索。
3. **不确定性泛化**：DiDiCM 在自然损坏（如 ImageNet-C）、对抗扰动、分布外检测等场景下的鲁棒性如何？当前实验仅覆盖分辨率、数据量和增强策略三个维度。
4. **大规模类别**：DiDiCM-CP 对极大规模类别（如 K > 10⁶）时，O(K²) 的转移矩阵内存开销是否仍然可行？DiDiCM-CL 是否能提供可行的替代方案？
5. **与其他扩散分类器的定量比较**：当前工作未给出与 Li et al. (2023) 等扩散生成分类器的直接定量比较，这一空白需要补充以明确 DiDiCM 在扩散分类方法谱系中的相对优势。



## 原文 PDF

![[paperPDFs/CVPR_2026/Advancing_Image_Classification_with_Discrete_Diffusion_Classification_Modeling.pdf]]

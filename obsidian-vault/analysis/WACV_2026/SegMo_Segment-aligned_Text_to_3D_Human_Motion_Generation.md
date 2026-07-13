---
title: "SegMo: Segment-aligned Text to 3D Human Motion Generation"
type: paper
paper_level: A
venue: WACV
year: 2026
pdf_ref: "paperPDFs/WACV_2026/SegMo:_Segment-aligned_Text_to_3D_Human_Motion_Generation.pdf"
project_link: null
code_link: null
aliases:
- SegMo
tags:
- WACV_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将文本描述与动作序列分解为语义一致的段（segment），并通过样本内对比学习实现段级对齐。
primary_logic: 在共享嵌入空间中对齐文本段与对应动作段，能够捕捉精细的跨模态对应关系，从而提升生成动作的准确性和自然度。
claims:
- 在 HumanML3D 上，SegMo 将 R-Precision Top-1 从基线 MoMask 的 0.521 提升至 0.553。
- 在 HumanML3D 上，SegMo 的 FID 从 0.045 降至 0.042，MM-Dist 从 2.958 降至 2.782。
- 均匀分割（uniform segmentation）产生最低的分割误差方差，并在生成质量上表现最优。
- 样本内段级对齐（within-sample alignment）优于批量对齐和全局对齐，保持了细粒度对应。
---

# SegMo: Segment-aligned Text to 3D Human Motion Generation

> [!tip] 核心洞察
> 在共享嵌入空间中对齐文本段与对应动作段，能够捕捉精细的跨模态对应关系，从而提升生成动作的准确性和自然度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SegMo：基于段对齐的文本到三维人体运动生成 |
| 英文题名 | SegMo: Segment-aligned Text to 3D Human Motion Generation |
| 会议/期刊 | WACV 2026 |
| Links | [paper](https://arxiv.org/abs/2512.21237) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SegMo |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 0.553 vs 0.521 (MoMask) (+0.032)；FID 0.042 vs 0.045 (MoMask) (-0.003)；MM-Dist 2.782 vs 2.958 (MoMask) (-0.176)。
> - KIT-ML 上，R-Precision Top-1 0.443 vs 0.433 (MoMask) (+0.010)；FID 0.163 vs 0.204 (MoMask) (-0.041)。

## 概要

文本到三维人体运动生成的核心挑战在于，现有方法仅在序列级别对齐文本与动作，忽略了模态内部的细粒度语义结构。这种粗粒度的对齐方式导致生成的动作出现缺失、重复或顺序错误。SegMo 提出了一种基于**段对齐**的生成框架，将文本描述与动作序列分解为语义一致的段，并通过样本内对比学习实现段级对齐，从而捕捉精细的跨模态对应关系。

方法上，SegMo 以 **MoMask**（Guo et al., CVPR 2024）为基线，在其掩码 Transformer 的基础上引入三个关键模块：文本段提取模块利用大语言模型将复杂文本描述分解为按时序排列的文本段；运动段提取模块将运动序列均匀切分为段并聚合为段表示；细粒度对齐模块在共享嵌入空间中对齐文本段与对应运动段。总损失由掩码损失与段级对齐损失加权构成：

$$\mathcal{L} = \mathcal{L}_{mask} + \lambda_{align} \mathcal{L}_{align}$$

在 HumanML3D 测试集上，SegMo 将 R-Precision Top-1 从基线的 0.521 提升至 **0.553**，FID 从 0.045 降至 **0.042**，MM-Dist 从 2.958 降至 **2.782**（Table 1）。在 KIT-ML 上同样取得一致提升（Table 2）。消融实验表明，均匀分割策略因分割误差方差最小而表现最优，样本内段级对齐优于批量对齐和全局对齐（Table 3, Table 5）。

方法仍存在若干局限：均匀分割对运动边界的精度有限；模型难以捕捉细微文本修饰词（如“in place”）；当指定运动长度较短而文本包含多个连续动作时，可能无法完整生成所有动作。



文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的动作序列。近年来，基于离散运动 token 的生成范式（如 **MoMask** (Guo et al., CVPR 2024) 的掩码建模框架）在这一任务上取得了显著进展。然而，现有方法存在一个共同的结构性缺陷：**它们仅在序列级别对文本与动作进行全局对齐，完全忽略了模态内部天然的细粒度语义结构**。

这一缺陷的直接后果是，当文本描述包含多个时序动作时（例如“一个人先向前走，然后蹲下，最后跳起来”），模型生成的运动会频繁出现**动作缺失、动作重复或时序顺序错误**等问题。本质上，模型缺乏将复杂描述拆解为有序子动作、并将每个子动作精确映射到对应运动片段的能力。

SegMo 的核心动机正是填补这一空白。其核心洞察在于：**如果将文本描述与运动序列同步分解为语义一致的段（segment），并在共享嵌入空间中实现段级对齐，就能捕捉精细的跨模态对应关系，从而系统性地提升生成动作的准确性与自然度**。图 Figure 1 直观地展示了这一思路：复杂描述与运动序列被分解为按时序排列的段，并在共享空间中对齐。



## 核心方法与创新机理

SegMo 的核心创新在于将文本到动作生成从传统的**序列级对齐**提升至**段级细粒度对齐**。现有方法（如基线 **MoMask**，Guo et al., CVPR 2024）仅使用全局 CLIP 文本特征 $T$ 作为条件，忽略了文本描述内部“先走后转再坐”等时序语义结构，导致生成动作出现缺失、重复或顺序错误。SegMo 通过三个关键改动（changed slots）解决了这一瓶颈：

1. **文本条件增强**：在原有全局 CLIP 特征 $T$ 的基础上，额外引入每个文本段的 CLIP 特征 $t_{1:A}$，使模型感知文本内部的细粒度语义结构（Section 3.3）。
2. **运动段显式提取**：将运动序列均匀分割为段，并通过 mean-max 聚合得到运动段表示 $\mathbf{m}_i = \mathrm{MLP}(\mathrm{Concat}(\operatorname{mean}(\mathbf{x}_{s_i:e_i}^0), \operatorname{max}(\mathbf{x}_{s_i:e_i}^0)))$，为段级对齐提供目标（Section 3.4, Eq. 6）。
3. **样本内段级对比损失**：在训练损失中增加对齐损失 $\mathcal{L}_{align}$，使总损失变为 $\mathcal{L} = \mathcal{L}_{mask} + \lambda_{align} \mathcal{L}_{align}$。该损失在单个样本内部执行文本段与运动段的对比学习，确保每个文本段仅与其对应的运动段靠近，避免了跨样本语义干扰（Section 3.5, Eq. 8-9）。

**因果机制**：上述三个改动形成了一个完整的因果链——LLM 将复杂文本描述分解为时序文本段，均匀分割提供稳定的运动段边界，样本内对比学习则在共享嵌入空间中强制建立文本段与运动段的精确对应。这一机制使模型能够捕捉“哪个词对应哪段动作”的细粒度跨模态关系，从而提升生成动作的准确性和自然度。

**关键证据**：在 HumanML3D 数据集上，SegMo 将 R-Precision Top-1 从 MoMask 的 0.521 提升至 0.553，FID 从 0.045 降至 0.042，MM-Dist 从 2.958 降至 2.782（Table 1）。消融实验进一步验证了均匀分割（分割误差方差最小）和样本内对齐（优于批量对齐和全局对齐）的有效性（Table 3, Table 5）。



SegMo 以 **MoMask**（Guo et al., CVPR 2024）为基线，在其掩码建模框架之上引入三个核心模块，构建从文本到三维人体运动的段级对齐生成流程。整体 pipeline 由两大阶段串联而成：**残差 VQ-VAE 编码** 与 **掩码 Transformer 生成**，后者是段级对齐模块的作用位置。

### 阶段一：残差 VQ-VAE 编码

连续运动序列 $M$ 首先通过一维卷积编码器投影到隐空间 $V = \mathrm{Encoder}(M) \in \mathbb{R}^{n \times d}$。随后，残差量化将每个隐向量 $\tilde{V}_i$ 表示为基码本与多层残差码本索引之和：

$$\tilde{V}_i = \sum_{j=0}^{k} \mathbf{z}_i^j$$

其中 $\mathbf{z}_i^0$ 为**基础 token**，$\mathbf{z}_i^j (j>0)$ 为**残差 token**。这一离散化将连续运动压缩为多尺度离散表示，为后续生成提供 token 序列。

### 阶段二：掩码 Transformer 生成与段级对齐

生成过程分为两步：
1. **掩码 Transformer** 根据文本条件预测被 mask 的基础 token——**段级对齐模块正是在此处介入**。
2. **残差 Transformer** 逐层生成残差 token，其结构与掩码 Transformer 相似。

段级对齐由三个新增模块协同完成：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Text Segment Extraction** | 利用 LLM 将原始文本描述分解为按时序排列的文本段，并用 CLIP 文本编码器提取全局特征 $T$ 与各段特征 $t_{1:A}$ | 原始文本描述 | 文本段序列及 CLIP 特征 |
| **Motion Segment Extraction** | 将运动序列均匀切分为段，通过 mean-max 聚合得到运动段表示 | 基础运动 token $\mathbf{x}^0$ | 运动段表示 $\mathbf{m}_i$ |
| **Fine-grained Text-Motion Alignment** | 在样本内对文本段与运动段执行对比学习，强制对应段在共享嵌入空间中靠近 | 文本段特征 $t_j^i$、运动段表示 $\mathbf{m}_k^i$ | 对齐损失 $\mathcal{L}_{align}$ |

### 数据流总览

文本输入经 LLM 解析为段序列（如 “A person walks.” → “A person turns around.” → “A person sits down.”），CLIP 编码后与运动编码器输出的基础 token 一同进入掩码 Transformer。运动段提取模块将基础 token 按均匀分割聚合成段表示，与文本段特征共同计算样本内对比损失。总训练目标为：

$$\mathcal{L} = \mathcal{L}_{mask} + \lambda_{align} \mathcal{L}_{align}$$

其中 $\mathcal{L}_{mask}$ 为掩码位置的基础 token 负对数似然损失，$\mathcal{L}_{align}$ 为文本-运动与运动-文本双向对比损失的均值。

**关键设计决策**：对齐仅在样本内进行，避免跨样本语义干扰，从而保持细粒度对应关系。均匀分割策略虽简单，但在分割误差方差和最终生成质量上均优于其他分割方法。

### 补充图表

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our method. Left: The Residual VQ-VAE encodes a continuous motion sequence into discrete motion tokens, including base tokens and residual tokens, which will be generated by the mask transformer and residual transformer, respectively. Right: The Mask Transformer predicts the masked base tokens conditioned on the textual description. To achieve segment-level fine-grained alignment, we introduce a Text Segment Extraction module and a Motion Segment Extraction module, which extract text and motion segments respectively, and align them through the Fine-grained Text-Motion Alignment module*



SegMo 建立在 **MoMask**（Guo et al., CVPR 2024）的掩码建模框架之上，通过三个新增模块实现段级细粒度对齐：文本段提取、运动段提取、以及细粒度文本-运动对齐。对齐模块作用于 Mask Transformer，使其在预测被掩码的基础 token 时，不仅依赖全局文本条件，还能感知段级对应关系。

### 3.1 基础框架：残差 VQ-VAE 与双 Transformer

运动序列 $M$ 首先经 1D 卷积编码器投影到隐空间：

$$V = \mathrm{Encoder}(M) \in \mathbb{R}^{n \times d}$$

随后通过残差量化将每个隐向量 $V_i$ 量化为基础 token $\mathbf{x}_i^0$ 与多层残差 token $\mathbf{x}_i^j$：

$$\tilde{V}_i = \sum_{j=0}^{k} \mathbf{z}_i^j$$

其中 $\mathbf{z}_i^0$ 来自基础码本，$\mathbf{z}_i^j$（$j \ge 1$）来自残差码本。Mask Transformer 负责根据文本条件 $\mathbf{c}$ 预测被掩码的基础 token $\mathbf{x}_i^0$，对齐模块即作用于该 Transformer；Residual Transformer 则逐层生成残差 token。

### 3.2 文本段提取

输入文本描述由 LLM 分解为按时序排列的文本段。论文测试了多种中等规模 LLM，最终选用 **Qwen 3:8B** 以获得稳定可靠的分段结果（消融验证见 Table 4）。对原始描述提取全局 CLIP 文本特征 $\mathbf{T}$，对每个文本段提取段级 CLIP 特征 $\mathbf{t}_{1:A}$，其中 $A$ 为段数（最大设为 5，可覆盖两个数据集的大部分样本）。

### 3.3 运动段提取

运动序列采用**均匀分割**策略划分为 $A$ 个段，每个段 $i$ 对应帧区间 $[s_i, e_i]$。段表示通过 Mean-Max 聚合得到：

$$\mathbf{m}_i = \mathrm{MLP}(\mathrm{Concat}(\operatorname{mean}(\mathbf{x}_{s_i:e_i}^0), \operatorname{max}(\mathbf{x}_{s_i:e_i}^0)))$$

即对段内基础 token 分别做均值池化和最大值池化，拼接后经 MLP 投影到与文本段相同的嵌入空间。消融实验（Table 4）表明，Mean-Max 聚合优于仅使用 Mean、Max 或注意力聚合。

### 3.4 细粒度文本-运动对齐

对齐模块在**样本内**执行对比学习：每个样本的 $A$ 个文本段与 $A$ 个运动段构成 $A$ 对正样本对，其余 $A-1$ 对为负样本对。文本到运动的对齐损失为：

$$\mathcal{L}_{t2m} = -\frac{1}{B \cdot A}\sum_{i=1}^{B}\sum_{j=1}^{A}\log \frac{\exp(\sin(\mathbf{t}_j^i, \mathbf{m}_j^i)/\tau)}{\sum_{k=1}^{A}\exp(\sin(\mathbf{t}_j^i, \mathbf{m}_k^i)/\tau)}$$

其中 $B$ 为批次大小，$\sin(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数（固定为 0.1）。对称地定义运动到文本的损失 $\mathcal{L}_{m2t}$，总对齐损失为两者均值：

$$\mathcal{L}_{align} = \frac{1}{2}(\mathcal{L}_{t2m} + \mathcal{L}_{m2t})$$

这种样本内设计避免了跨样本的语义干扰，保持了细粒度对应关系（消融验证见 Table 3：样本内对齐优于批量对齐和全局对齐）。

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/007_Table_3.jpg]]
*Table 3: Ablation results of replacing the segmentation and the alignment module on the HumanML3D test set. For each metric, we repeat the evaluation 20 times and report the average with a 95% confidence interval. Red and Blue indicate the best and the second-best results*

### 3.5 总损失

Mask Transformer 的训练目标为掩码损失与对齐损失的加权和：

$$\mathcal{L} = \mathcal{L}_{mask} + \lambda_{align} \mathcal{L}_{align}$$

其中掩码损失为被掩码位置基础 token 的负对数似然：

$$\mathcal{L}_{mask} = -\sum_{i \in \mathcal{M}} \log p_{\theta}(\mathbf{x}_i^0 | \mathbf{c}, \hat{\mathbf{x}^0})$$

对齐损失权重 $\lambda_{align}$ 在 HumanML3D 上设为 1.0，在 KIT-ML 上设为 0.1。

### 3.6 推理阶段的段级检索能力

训练得到的段级对齐嵌入空间在推理阶段可支持两项零样本任务：
- **运动定位**：给定查询文本段 $\mathbf{t}_q$，选择余弦相似度最高的运动段 $\mathbf{m}^{*} = \arg\max_{\mathbf{m} \in \mathcal{M}} \sin(\mathbf{t}_q, \mathbf{m})$
- **运动到文本检索**：给定查询运动段 $\mathbf{m}_q$，选择余弦相似度最高的文本段 $\mathbf{t}^{*} = \arg\max_{\mathbf{t} \in \mathcal{T}} \sin(\mathbf{t}, \mathbf{m}_q)$

Figure 5 的相似度图定性表明，SegMo 的段级对齐能产生更清晰的跨模态对应边界，而基线 MoMask 的全局对齐难以区分时序相近的动作段。

### 补充图表

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/001_Figure_1.jpg]]
*Figure 1: The main idea of our method. We decompose the complex motion description and motion sequence into simpler temporally ordered segments and align them in a shared embedding space to improve the accuracy and realism of generated motions*



## 实验与关键发现

### 主实验结果

SegMo 在两个主流基准上均取得了一致的性能提升。在 HumanML3D 测试集上，相较于基线 **MoMask**（Guo et al., CVPR 2024），SegMo 将 R-Precision Top-1 从 0.521 提升至 0.553（+0.032），FID 从 0.045 降至 0.042，MM-Dist 从 2.958 降至 2.782（见 Table 1）。在 KIT-ML 测试集上，R-Precision Top-1 从 0.433 提升至 0.443，FID 从 0.204 降至 0.163（见 Table 2）。所有指标均经 20 次重复评估并报告 95% 置信区间，结果可靠。

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/003_Table_1.jpg]]
*Table 1: Comparison of text-conditional human motion generation on the HumanML3D test set. For each metric, we repeat the evaluation 20 times and report the average with a 95% confidence interval. Red and Blue indicate the best and the second-best results*

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/004_Table_2.jpg]]
*Table 2: Comparison of text-conditional human motion generation on the KIT-ML test set. For each metric, we repeat the evaluation 20 times and report the average with a 95% confidence interval. Red and Blue indicate the best and the second-best results*

定性对比（见 Figure 3）显示，SegMo 生成的动作为每个文本段分配了更充足的时长，动作过渡更自然，而 T2M-GPT 和 MoMask 存在动作缺失或过度简化的问题。

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison of T2M-GPT, MoMask, and Ours on the HumanML3D test set. A fixed number of keyframes is shown for each motion sequence. Please refer to the supplementary video for additional comparison results*

### 消融实验

**分割策略与对齐方式。** Table 3 报告了替换分割策略和对齐模块的消融结果。均匀分割（uniform segmentation）在所有指标上均优于基于语义的分割（semantic-based）和随机分割（random），且样本内段级对齐（within-sample alignment）显著优于批量对齐（batch-level）和全局对齐（global alignment）。Table 5 进一步验证了均匀分割在 BABEL 数据集上产生最低的分割误差方差，解释了其在生成质量上的优势。

**LLM 与聚合模块。** Table 4 表明，使用 Qwen 3:8B 进行文本段提取优于 Llama 3:8B 和 Qwen 2.5:7B。在运动段聚合方式上，Mean-Max 聚合（拼接 mean 池化和 max 池化后经 MLP）优于仅使用 Mean、Max 或注意力聚合。

**段内一致性分析。** Figure 4 展示了不同分割方法下各模型的段内一致性（Intra-Segment Consistency, ISC）。SegMo 在不同训练-评估分割策略组合下均表现出更高的 ISC 和更低的变异系数（CV），表明其对分割策略变化具有更强的鲁棒性。

### 失败模式与局限性

尽管整体性能优异，SegMo 仍存在以下失败模式（见 Figure 9）：

1. **运动分割精度不足：** 均匀分割虽稳定，但无法精确捕捉动作边界，导致部分段的对齐不够精细。
2. **细微修饰词捕捉困难：** 模型有时难以理解如 “in place” 等细微文本修饰词，导致生成的动作与文本意图不完全一致。
3. **短时长多动作冲突：** 当指定运动长度较短而文本描述包含多个连续动作时，模型可能无法为每个动作分配充足的时间，导致部分动作缺失。

这些失败模式指向三个待解决问题：如何超越均匀分割以获得更精确的运动边界；如何增强模型对细微文本修饰词的捕捉能力；如何在有限运动长度内强制分配充足的时间给每个动作。

### 补充图表

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/009_Table_4.jpg]]
*Table 4: Ablation results of replacing the LLMs and the aggregation module on the HumanML3D test set. For each metric, we repeat the evaluation 20 times and report the average with a 95% confidence interval. Red and Blue indicate the best and the second-best results*

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/010_Table_5.jpg]]
*Table 5: Evaluation of different motion segmentation methods on the BABEL dataset*

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/006_Figure_4.jpg]]
*Figure 4: The Intra-Segment Consistency (ISC) of all models evaluated under different segmentation methods on the HumanML3D test set. The Coefficient of Variation (CV), defined as std(ISC)/mean(ISC), is reported to assess stability. “Train” denotes the segmentation method used for training, while “Eval” denotes the segmentation method used for evaluation*

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/008_Figure_5.jpg]]
*Figure 5: Example of motion grounding. Top: Results using the similarity map generated by our method. Bottom: Similarity map generated by MoMask [10]. In each map, the x-axis denotes the start index of the sliding window and the y-axis denotes the text segment. The motion length is 49, and the window size is 5*

![[assets/figures/papers/paper_list_l3313_https_arxiv_org_abs_2512_21237/figures/011_Figure_6.jpg]]
*Figure 6: Prompt for generating text segments using LLM*



## 定位与知识库关联

**在文本到动作生成谱系中的位置。** SegMo 建立在离散动作 token 生成范式之上，直接继承 **MoMask**（Guo et al., CVPR 2024）的残差 VQ-VAE 架构与掩码 Transformer 框架。MoMask 通过将连续运动序列量化为基础 token 与多层残差 token，再以掩码建模方式逐层生成，在当时达到了文本到动作生成的领先水平。然而，MoMask 仅在序列级别使用全局 CLIP 文本特征作为条件，未显式建模文本与动作内部的细粒度语义结构。SegMo 在保留 MoMask 整体生成管线的前提下，将文本条件从单一的全局特征 $T$ 扩展为 $T + t_{1:A}$（$A$ 个文本段特征），并在掩码 Transformer 中引入段级对齐损失 $\mathcal{L}_{align}$，使总目标变为 $\mathcal{L} = \mathcal{L}_{mask} + \lambda_{align} \mathcal{L}_{align}$。这一改动不改变生成架构的核心结构，而是通过增加训练信号来强化跨模态对应关系。

**与同期细粒度对齐方法的关系。** 在文本到动作领域，已有工作尝试通过时空注意、层次化文本编码等方式增强文本与动作的交互，但多数方法停留在序列级对齐或隐式注意力层面。SegMo 的关键区别在于显式地将文本与动作分解为语义一致的段（segment），并通过样本内对比学习实现段级对齐。这种“分解—对齐”策略与视觉-语言领域的细粒度对齐方法（如 FILIP、PACL）在思路上有相似之处，但 SegMo 针对运动模态的特殊性——动作边界天然模糊、缺乏显式分割标注——设计了均匀分割策略，并以分割误差方差最小化为理论依据，而非依赖外部解析器或人工标注。

**适用边界。** SegMo 的段对齐机制在以下条件下最为有效：（1）文本描述包含多个可按时间顺序分解的子动作（如“先走路，再转身，然后坐下”）；（2）运动序列长度足以容纳所有文本段对应的动作。当文本描述为单一简单动作或运动长度过短而文本段数较多时，段对齐的增益会减弱。此外，SegMo 的对齐模块作用于掩码 Transformer 的基础 token 生成阶段，残差 Transformer 的逐层生成过程不直接参与对齐，因此细粒度语义的捕捉主要集中在前端。

**局限与开放问题。** 论文明确指出了三个主要局限。第一，均匀分割虽在实验中表现最优且稳定，但其分割边界并非语义边界，对细粒度对齐的精度构成上限。第二，模型有时难以捕捉细微的文本修饰词（如“in place”），导致生成的动作在空间范围或速度上与描述存在偏差。第三，当指定运动长度较短而文本描述包含多个连续动作时，模型可能无法为每个动作分配充足的时间，导致部分动作缺失或压缩。这些局限指向三个开放问题：如何获得更精确的运动边界以实现超越均匀分割的细粒度对齐；如何增强模型对细微文本修饰词的感知能力；如何在有限运动长度内强制分配充足的时间给每个语义段。



## 原文 PDF

![[paperPDFs/WACV_2026/SegMo:_Segment-aligned_Text_to_3D_Human_Motion_Generation.pdf]]

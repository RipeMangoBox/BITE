---
title: "A Rich Knowledge Space for Scalable Deepfake Detection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Rich_Knowledge_Space_for_Scalable_Deepfake_Detection.pdf
project_link: null
code_link: null
aliases:
- SSDD
- RKSSDD
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/privacy_fairness
core_operator: "构建大规模、多模态、统一预处理的数据集MMI-DD，并设计多模态视觉-语言学习框架SD²，通过细粒度分类、文本标签分离和双对比学习等目标，使模型能够有效利用大规模异构数据。"
primary_logic: "通过将来自多个数据集的图像统一标注为五种类型（REAL, FS, FR, EFS, FE），并利用VLM生成的面部和环境描述进行多模态对齐，可以构建一个丰富的深度伪造知识空间，使模型在数据量增加时持续提升性能，而非饱和或退化。"
claims:
- "随着训练数据从100K增加到3M，SD²的跨域mAUC从82.90%提升到87.79%，而基线方法性能饱和或下降。"
- "SD²在跨域检测中达到mAUC 87.79%，优于所有基线方法。"
- "消融实验表明，CLAM模块带来1.6%的AUC提升，所有组件组合达到最佳性能。"
- "11个数据集的域内检测 上 mAUC = 95.76"
---

# A Rich Knowledge Space for Scalable Deepfake Detection

> [!tip] 核心洞察
> 通过将来自多个数据集的图像统一标注为五种类型（REAL, FS, FR, EFS, FE），并利用VLM生成的面部和环境描述进行多模态对齐，可以构建一个丰富的深度伪造知识空间，使模型在数据量增加时持续提升性能，而非饱和或退化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向可扩展深度伪造检测的丰富知识空间 |
| 英文题名 | A Rich Knowledge Space for Scalable Deepfake Detection |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hNd5L7WnjC) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/privacy_fairness |
| Method | SD² (Scalable Deepfake Detection) |
| Dataset | 11个数据集的域内检测, 4个跨域数据集 (UADFV, WildDeepFake, DFDC, DF40-Test), GenImage (跨模型AIGC检测) |

> [!tip] 效果简介
> - 11个数据集的域内检测 上，mAUC 为 95.76，对比 最佳基线CLIP-SVD: 93.82，变化 +1.94。
> - 4个跨域数据集 (UADFV, WildDeepFake, DFDC, DF40-Test) 上，mAUC 为 87.79，对比 最佳基线CLIP-SVD: 82.90，变化 +4.89。
> - GenImage (跨模型AIGC检测) 上，mACC 为 88.50，对比 最佳基线CLIP-SVD: 86.50，变化 +2.00。

## 概要

深度伪造检测面临的核心瓶颈在于：现有方法通常在单一数据集上训练，模型仅能捕捉有限的伪造痕迹，对未见过的数据泛化能力差。更关键的是，随着训练数据规模增大，传统基于CLIP的适配方法性能反而饱和甚至下降。本文提出SD²（Scalable Deepfake Detection）框架，通过构建大规模、多模态、统一预处理的数据集MMI-DD（整合11个数据集、约360万张图像），并设计多模态视觉-语言学习策略，有效解决了这一可扩展性问题。

SD²的核心洞察在于：将来自多个数据集的图像统一标注为五种细粒度类型（REAL, FS, FR, EFS, FE），并利用VLM（InternVL2.5）生成面部和环境描述，从而构建一个丰富的深度伪造知识空间，使模型在数据量增加时持续提升性能。方法层面，SD²包含三个关键创新：(1) Cross-Layer Attention Module (CLAM)融合CLIP所有Transformer层的[CLS]特征；(2) 细粒度图像-文本分类损失区分五种类型；(3) 文本标签分离损失和双对比损失分别用于强制类型嵌入正交化和多模态对齐。

实验结果表明：SD²在域内检测中达到mAUC 95.76%，优于最佳基线CLIP-SVD的93.82%；在跨域检测中达到mAUC 87.79%，较基线提升4.89%；在跨模型AIGC检测（GenImage）上达到mACC 88.50%。消融实验证实各组件均贡献显著，其中CLAM模块带来1.6%的AUC提升。最关键的是，随着训练数据从100K增加到3M，SD²的跨域mAUC从82.90%持续提升到87.79%，而基线方法性能饱和或下降，验证了其可扩展性。



深度伪造检测面临的核心瓶颈在于：现有方法大多在单一数据集上训练（如 FaceForensics++），导致模型仅能学习到该数据集特有的有限伪造痕迹，对未见过的伪造类型或生成方法泛化能力极差。更关键的是，随着训练数据规模的增大，传统的 CLIP 适配方法（如线性探测、全参数微调、LoRA 等）性能不仅不提升，反而出现饱和甚至下降，无法从大规模异构数据中获益。这一“数据越多，性能越差”的反直觉现象，揭示了当前方法在构建可扩展的深度伪造知识空间上的根本性缺陷。

该问题的因果根源在于两个被忽视的设计缺口：**数据层面的碎片化**与**学习目标层面的粗粒度**。在数据侧，现有工作各自为政，数据集之间缺乏统一的标注体系和预处理标准，模型无法在跨数据集的共享伪造特征上进行学习。在学习目标侧，二分类（真实/伪造）的设定过于粗糙，无法区分不同伪造类型（如面部替换、面部重演、完整面部合成、面部编辑）所蕴含的差异化伪造痕迹；同时，仅依赖简单的图像-文本对比损失（如 SigLIP），未能充分利用视觉语言模型（VLM）的细粒度对齐能力。

基于此，本文的动机是构建一个**丰富的深度伪造知识空间**，使模型能够随着数据规模的增加持续提升性能，而非饱和或退化。核心思路包含三个层面：第一，构建大规模、多模态、统一预处理的数据集 **MMI-DD**，整合 11 个数据集、360 万张图像，并通过人工标注将图像统一划分为五种类型（REAL, FS, FR, EFS, FE），同时利用 VLM 生成面部和环境描述；第二，设计多模态视觉-语言学习框架 **SD²**，通过交叉层注意力模块（CLAM）融合 CLIP 各层的 [CLS] 特征，捕获从低层纹理到高层语义的跨层级伪造线索；第三，引入三个互补的优化目标——细粒度图像-文本分类损失（区分五种类型）、文本标签分离损失（强制不同类型文本嵌入正交化）、双图像-文本对比损失（分别对齐面部和环境描述），使模型能够从大规模异构数据中系统性地提取和泛化伪造知识。

这一设计的核心洞察在于：**伪造痕迹是多模态、多粒度的**，仅靠单一数据源或二分类目标无法捕获其全貌。通过将数据统一标注为细粒度类型，并利用 VLM 生成的多模态描述进行对齐，模型能够构建一个结构化的知识空间，其中不同类型伪造的视觉特征与对应的文本语义形成清晰的对应关系。实验证据表明（见 Table 6），当训练数据从 100K 扩展到 3M 时，SD² 的跨域 mAUC 从 82.90% 提升到 87.79%，而所有基线方法均出现饱和或下降，验证了这一思路的有效性。



## 核心方法与创新机理

SD² 的核心创新在于通过构建大规模、多模态、统一预处理的数据集 MMI-DD，并设计多模态视觉-语言学习框架，从根本上解决了现有深度伪造检测方法在数据规模增大时性能饱和甚至下降的瓶颈问题。其关键改变体现在以下五个方面：

1.  **训练数据规模与多样性**：从在单一数据集（如 FaceForensics++）上训练，转变为在包含 11 个数据集、360 万张图像的 MMI-DD 上训练（Table 1）。这一改变是性能可扩展性的基础，使得模型能够接触到更广泛的伪造痕迹和分布。

2.  **分类粒度**：从简单的二分类（真实/伪造）升级为五分类（REAL, FS, FR, EFS, FE）。这种细粒度分类不仅提供了更丰富的监督信号，还迫使模型学习区分不同伪造技术的特异性特征，从而构建更鲁棒的深度伪造知识空间。

3.  **视觉特征提取**：从仅使用 CLIP 图像编码器最后一层 [CLS] 特征，转变为使用 Cross-Layer Attention Module (CLAM) 融合所有 Transformer 层的 [CLS] 特征。这一改变的关键在于，不同伪造痕迹可能出现在不同层级的特征中（例如，低级纹理异常 vs. 高级语义不一致），CLAM 通过多头自注意力自适应地聚合这些多层级线索，从而获得更具判别力的视觉表示（Figure 6 显示其显著提升了特征的可分离性）。

4.  **文本标签**：从使用简单的固定标签（如 'a photo of a [real/fake] image'），转变为为每类生成约 30 个由 GPT-o1 生成并人工筛选的增强标签。这丰富了类别语义空间，为细粒度分类提供了更稳健的文本锚点。

5.  **训练目标**：从仅使用图像-文本对比损失，转变为联合优化三个互补目标：细粒度图像-文本分类损失（$\mathcal{L}_C$）、文本标签分离损失（$\mathcal{L}_S$）和双对比损失（$\mathcal{L}_D$）。其中，$\mathcal{L}_S$ 通过强制不同类别的文本嵌入正交化（Figure 4），解决了原始 CLIP 空间中各类文本标签相似度过高的问题，为分类提供了清晰的决策边界。$\mathcal{L}_D$ 则通过将图像与 VLM 生成的面部描述和环境描述分别对齐，引入了更丰富的语义上下文，增强了模型对伪造痕迹的泛化能力。

**决定性证据**：消融实验（Table 5）量化了各组件的贡献：CLAM 带来 1.6% 的 AUC 提升，文本标签分离损失带来 4.61% 的提升，双对比损失进一步带来 2.94% 的提升。最终，SD² 在跨域检测中达到 mAUC 87.79%，显著优于所有基线方法（Table 3）。更重要的是，随着训练数据从 100K 增加到 3M，SD² 的性能持续提升（82.90% → 84.85% → 87.79%），而基线方法性能饱和或下降（Table 6），这直接验证了其可扩展性的核心优势。



![[assets/figures/papers/iclr26_0003_hNd5L7WnjC_A_Rich_Knowledge_Space_for_Scalable_Deepfake_Det/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our S $\mathcal { D } ^ { 2 }$ training framework. S $\mathcal { D } ^ { 2 }$ employs CLIP text and image encoders, both fine-tuned with LoRA. The Cross-Layer Attention Module (CLAM) enhances visual features by fusing low-to-high-level information. The model is optimized with three objectives: Classification Loss ( $\mathcal { L } _ { \mathrm { C } }$ ) to distinguish real and four fake types, Text Label Separation Loss ( $\mathcal { L } _ { \mathrm { S } }$ ) to enforce separation among types, and Dual Contrastive Loss ( $\mathcal { L } _ { \mathrm { D } }$ ) to align image-text pairs

SD²（Scalable Deepfake Detection）是一个基于CLIP的多模态视觉-语言学习框架，其核心目标是通过构建丰富的深度伪造知识空间，使模型能够在训练数据规模增加时持续提升检测性能，而非饱和或退化。该框架的瓶颈在于：现有方法在单一数据集上训练，仅能学习有限的伪造痕迹，泛化能力差；且传统CLIP适配方法在大规模数据下性能反而下降。SD²通过三个关键设计解决该问题：大规模异构数据集、跨层级特征融合模块、以及多目标联合优化。

**整体Pipeline与模块关系**（见Figure 3）：

1. **输入流**：图像经过统一预处理（MTCNN人脸检测、中心裁剪、视频数据集均匀采样32帧）后，进入CLIP-ViT-L/14图像编码器。同时，每张图像关联三类文本信息：五分类类型标签（REAL, FS, FR, EFS, FE，每类约30个由GPT-o1生成并人工筛选的增强标签）、VLM（InternVL2.5）生成的面部描述和环境描述。

2. **视觉特征提取**：CLIP图像编码器的所有Transformer层的[CLS]特征被收集，输入**Cross-Layer Attention Module (CLAM)**。CLAM对这些层级特征序列应用多头自注意力（公式1），将输出与最终层表示拼接后，通过两层线性网络和GELU激活得到最终视觉表示（公式2）。CLAM的作用是融合低层到高层的多尺度伪造线索——消融实验表明，加入CLAM带来1.6%的AUC提升（Table 5）。图像和文本编码器均通过LoRA（r=8, α=32, dropout=0.1）高效微调。

3. **多目标联合优化**（公式6：L_SD² = α·L_C + L_S + L_D，α=2.0）：
   - **细粒度图像-文本分类损失（L_C）**：基于图像与五类文本标签嵌入的余弦相似度计算交叉熵损失（公式3），实现五分类而非传统二分类。
   - **文本标签分离损失（L_S）**：强制不同类别的文本标签嵌入正交化（公式4），使相似度矩阵趋近单位矩阵。该损失使不同类别文本嵌入的余弦相似度趋近0（Figure 4）。
   - **双对比损失（L_D）**：基于SigLIP的二元交叉熵损失，分别对齐图像与面部描述、环境描述（公式5），增强多模态语义对齐。

4. **输出流**：测试时，使用每类最直接的文本标签（如"a photo of a Face Swapping"），将图像特征与五个文本标签的嵌入进行余弦相似度匹配，取最高相似度对应的类别作为预测结果。

**数据流与规模效应**：MMI-DD数据集整合11个数据集，包含约360万张图像，统一标注为五种类型。随着训练数据从100K增加到3M，SD²的跨域mAUC从82.90%持续提升到87.79%（Table 6），而所有基线方法（CLIP zero-shot、linear probe、full fine-tune、CLIP-SVD、LoRA）均出现性能饱和或下降（Figure 1左图）。这表明SD²的框架设计成功地将数据规模转化为检测性能的持续增益，突破了传统方法的可扩展性瓶颈。



SD² 的核心技术贡献在于三个紧密耦合的模块：跨层注意力模块（CLAM）用于增强视觉表示，以及三种互补的损失函数用于多模态对齐与分类。以下按模块逐一展开。

### 1. 跨层注意力模块（CLAM）

CLAM 的设计动机是：CLIP 视觉编码器（ViT）的不同 Transformer 层捕获了不同粒度的伪造痕迹（底层关注纹理/边界伪影，高层关注语义一致性），而传统方法仅使用最后一层的 `[CLS]` 标记，丢失了中层信息。

设 `f_cls ∈ R^(L×d)` 为所有 L 层 `[CLS]` 标记拼接而成的序列。CLAM 对该序列施加多头自注意力：

`f_sat^(h) = Attn(f_cls W_Q^(h), f_cls W_K^(h), f_cls W_V^(h))`  
`f_sat = Concat([f_sat^(h)]_(h=1)^H) · W_O`

其中 `W_Q^(h), W_K^(h), W_V^(h) ∈ R^(d×d_h)` 为第 h 头的投影矩阵，`W_O ∈ R^(H·d_h×d)` 为输出投影，H 为头数（论文默认 H=8）。该操作等价于让各层 `[CLS]` 标记相互查询，使模型能够自适应地加权融合低层到高层的线索。

随后，CLAM 输出通过一个两层适配器与最终层表示拼接：

`f = W_2 · GELU(W_1 · Concat([f_sat', f_final]))`

`f_sat'` 是 `f_sat` 经平均池化后的向量，`f_final` 是最后一层 `[CLS]` 标记。`W_1, W_2` 为可学习线性层。该设计保留了原始 CLIP 的最终层语义，同时注入跨层信息。

### 2. 细粒度图像-文本分类损失（`L_C`）

SD² 将深度伪造检测重新定义为五分类问题（REAL, FS, FR, EFS, FE），每类配有约 30 个由 GPT-o1 生成并人工筛选的增强文本标签。设 `u_c` 为第 c 类所有文本标签嵌入的均值，`f` 为图像嵌入，则分类损失为：

`L_C = -Σ_(i=1)^(|B|) log( exp(τ · sim(f_i, u_(c_i))) / Σ_(j=1)^(|C|) exp(τ · sim(f_i, u_(c_j))) )`

其中 `sim(·,·)` 为余弦相似度，τ 为可学习温度，`|C|=5`。该损失强制图像嵌入与其真实类别的文本嵌入对齐，同时远离其他类别。注意，此处使用均值嵌入而非单个标签，相当于在文本侧做了软投票，增强了标签多样性带来的鲁棒性。

### 3. 文本标签分离损失（`L_S`）

原始 CLIP 文本空间中，不同伪造类型的标签嵌入高度相似（如“Face Swapping”与“Face Editing”的余弦相似度接近 0.8），这阻碍了细粒度分类收敛。分离损失强制各类别文本嵌入正交化：

`L_S = || sim(u, u^T) - I ||_F^2`

其中 `u ∈ R^(|C|×d)` 为各类别文本嵌入均值组成的矩阵，`I` 为单位矩阵，`||·||_F` 为 Frobenius 范数。该损失最小化不同类别嵌入间的余弦相似度（趋近 0），同时保持同类嵌入的高相似度。消融实验（Table 5）表明，加入 `L_S` 后跨域 mAUC 从 80.24% 提升至 84.85%，说明正交化文本空间是细粒度分类的关键。

### 4. 双对比损失（`L_D`）

除类别标签外，SD² 还利用 VLM（InternVL2.5）为每张图像生成面部描述 `v^f` 和环境描述 `v^e`。双对比损失基于 SigLIP（Sigmoid 损失）分别对齐图像与两类描述：

`L_D = -Σ_(i=1)^(|S|) Σ_(j=1)^(|B_all|) [ log σ(z_(ij)(τ · sim(f_i, v_j^f) + b)) + log σ(z_(ij)(τ · sim(f_i, v_j^e) + b)) ]`

其中 `z_(ij) ∈ {+1, -1}` 指示正负对，`b` 为可学习偏置，`σ` 为 Sigmoid 函数。`S` 为当前批次，`B_all` 为所有批次样本（通过梯度累积实现大 batch 对比）。该损失使模型学习到与伪造类型无关的语义对齐——例如，无论图像是真实还是伪造，其面部描述都应与环境描述在语义上一致，从而抑制模型对背景等虚假关联的过拟合。

### 5. 总体目标函数

`L_(SD²) = α · L_C + L_S + L_D`

超参数 α=2.0（经 Table 7 敏感性分析确定：α=1.5 时 mAUC=83.45，α=2.0 时 84.85，α=2.5 时 83.02）。三个损失的因果角色：`L_C` 提供类别判别信号，`L_S` 清理文本嵌入空间使类别可分离，`L_D` 注入多模态语义约束防止过拟合。三者缺一不可——消融实验（Table 5）显示，仅用 `L_C` 时 mAUC 仅 80.24%，逐步加入 `L_S` 和 `L_D` 后提升至 87.79%。

### 关键超参数与实现细节

- **骨干网络**：CLIP-ViT-L/14，图像输入尺寸 224×224。
- **高效微调**：LoRA 应用于注意力投影矩阵，秩 `r_lora=8`，缩放 `α_lora=32`，dropout=0.1。
- **优化器**：AdamW，学习率 5e-7，batch size 1024（通过梯度累积实现），训练 4 个 epoch。
- **推理**：使用每类最简文本标签（如“a photo of a Face Swapping”），取余弦相似度最高的类别作为预测。



## 实验与关键发现

### 域内检测性能

SD²在包含11个数据集的域内检测中达到了mAUC 95.76%，显著优于最佳基线CLIP-SVD的93.82%（Table 2）。这一提升表明，通过细粒度五分类（REAL、FS、FR、EFS、FE）和丰富的文本标签增强，模型能够更准确地捕捉不同伪造类型的特征。值得注意的是，SD²在DF40的Face Editing子集上表现相对较弱（AUC 73.20%，Table 9），这可能是因为该类型的伪造痕迹更细微，且训练数据中该类型的样本分布不均。

![[assets/figures/papers/iclr26_0003_hNd5L7WnjC_A_Rich_Knowledge_Space_for_Scalable_Deepfake_Det/figures/005_Table_2.jpg]]
*Table 2: Intra-domain detection performance (AUC). The best results are highlighted in bold*

### 跨域检测性能

跨域检测是衡量模型泛化能力的关键指标。SD²在UADFV、WildDeepFake、DFDC和DF40-Test四个未见过的数据集上达到mAUC 87.79%，相比最佳基线CLIP-SVD的82.90%提升了4.89个百分点（Table 3）。这一显著优势的核心原因在于：SD²利用大规模异构数据构建了丰富的深度伪造知识空间，使模型能够学习到跨数据集的通用伪造特征，而非过拟合于单一数据集的特定痕迹。

![[assets/figures/papers/iclr26_0003_hNd5L7WnjC_A_Rich_Knowledge_Space_for_Scalable_Deepfake_Det/figures/006_Table_3.jpg]]
*Table 3: Cross-domain detection performance (AUC)*

### 跨模型AIGC检测

在GenImage数据集上的跨模型评估中，SD²达到mACC 88.50%，优于CLIP-SVD的86.50%（Table 4）。这表明SD²不仅适用于传统深度伪造检测，还能有效泛化到扩散模型等AIGC生成图像，验证了多模态对齐策略对新兴伪造技术的适应性。

![[assets/figures/papers/iclr26_0003_hNd5L7WnjC_A_Rich_Knowledge_Space_for_Scalable_Deepfake_Det/figures/007_Table_4.jpg]]
*Table 4: Cross-model evaluation performance (ACC) on the GenImage dataset. While the results are directly sourced from (Yan et al., 2025a), we additionally implement CLIP-SVD, a.k.a. Effort, from (Yan et al., 2025b) following its official code*

### 可扩展性分析

这是论文最核心的实验发现。Table 6展示了随训练数据从100K增加到3M（完整MMI-DD），SD²的跨域mAUC从82.90%持续提升至84.85%再到87.79%。相比之下，所有基线方法（包括CLIP full fine-tune和CLIP-SVD）在数据量超过一定阈值后性能饱和甚至下降。这一结果直接验证了核心洞察：传统CLIP适配方法在数据规模增大时出现性能退化，而SD²通过多模态对齐和细粒度分类目标，能够有效利用大规模异构数据。

![[assets/figures/papers/iclr26_0003_hNd5L7WnjC_A_Rich_Knowledge_Space_for_Scalable_Deepfake_Det/figures/008_Table_5.jpg]]
*Table 5: Ablation studies analyzing the impact of key components. All models are trained on our integrated dataset and tested on four crossdomain datasets in Sec. 5.2.1. Table 6: Performance (mAUC) across training data scales, from 100K to 3M (full dataset)*

**失败模式分析**：基线方法性能下降的因果机制在于——当训练数据来自多个分布差异大的数据集时，单一的二分类目标和简单的CLIP适配策略无法统一异构的伪造特征，导致模型在不同数据集间产生冲突的梯度更新。SD²通过五分类和文本标签正交化（$\mathcal{L}_S$）缓解了这一问题。

### 消融实验

Table 5的消融实验揭示了各组件的贡献机制：

- **仅分类损失（$\mathcal{L}_C$）**：跨域mAUC为80.24%，已超过所有基线，说明细粒度分类目标本身是有效的。
- **+CLAM模块**：AUC提升1.6%至81.84%。CLAM通过融合所有Transformer层的[CLS]特征（公式1-2），捕获了从低级纹理到高级语义的多层级伪造线索。Figure 6的可视化显示，CLAM使真实与伪造样本在嵌入空间中形成更清晰的分离簇，而非CLAM时两者高度纠缠。
- **+文本标签分离损失（$\mathcal{L}_S$）**：AUC进一步提升至84.85%。该损失强制不同类别的文本嵌入接近正交（Figure 4显示相似度趋近0），避免了文本标签间的语义冗余，使分类边界更清晰。
- **+双对比损失（$\mathcal{L}_D$）**：最终AUC达到87.79%。该损失将图像与VLM生成的面部描述和环境描述分别对齐（公式5），引入了更丰富的语义监督信号。

### 超参数敏感性

Table 7显示，分类损失权重α=2.0时性能最佳（mAUC 84.85%），α=1.5时83.45%，α=2.5时83.02%。LoRA秩r_lora=8达到最佳（84.85%），r_lora=4为82.97%，r_lora=16为84.37%。这表明模型对超参数具有一定鲁棒性，但α和秩的选择仍需谨慎调优。

### 需人工验证的观察

论文声称CLAM模块使特征空间形成"更清晰的分离簇"（Figure 6），但该可视化仅展示了二维t-SNE投影，缺乏定量指标（如聚类纯度或类间距离度量）来支撑这一结论。此外，VLM生成的文本描述质量依赖于InternVL2.5，论文未提供描述准确性的定量评估（如人工评分或与真实描述的一致性指标）。

### 补充图表

![[assets/figures/papers/iclr26_0003_hNd5L7WnjC_A_Rich_Knowledge_Space_for_Scalable_Deepfake_Det/figures/002_Table_1.jpg]]
*Table 1: Summary of our integrated dataset, MMI-DD, including the numbers of real and fake images and their type annotations*



## 定位与知识库关联

SD² 的核心贡献在于重新定义了深度伪造检测中“知识”的构建方式——从依赖单一数据集上训练的二分类器，转向在大规模、多模态、细粒度标注数据上学习的可扩展视觉-语言框架。这一转变直接回应了现有方法的根本瓶颈：当训练数据规模增大时，传统 CLIP 适配方法的性能反而饱和或下降，表明它们无法有效利用异构数据中的丰富信息（Figure 1）。

**与基线方法的关系。** SD² 的基线选择覆盖了 CLIP 适配的主流范式：零样本分类、线性探测、全参数微调、SVD 分解（CLIP-SVD）和 LoRA 微调。实验表明，所有基线方法在数据量从 100K 增加到 3M 时性能停滞或退化，而 SD² 的跨域 mAUC 从 82.90% 持续提升至 87.79%（Table 6）。这一对比揭示了瓶颈的因果机制：传统方法仅使用 CLIP 的最后一层 [CLS] 特征和简单二分类目标，丢失了多层级伪造线索和细粒度类型信息。SD² 通过 CLAM 模块融合所有 Transformer 层的特征，并用五个组件——细粒度分类损失、文本标签分离损失、双对比损失——分别解决特征提取、类型区分和语义对齐三个子问题。消融实验量化了每个组件的贡献：CLAM 带来 1.6% AUC 提升，分离损失贡献 4.61%，双对比损失进一步带来 2.94% 提升（Table 5）。

**适用边界。** SD² 的有效性建立在三个前提之上：（1）有大规模、多来源、统一标注的面部伪造数据——MMI-DD 整合了 11 个数据集、360 万张图像，人工标注为五种类型；（2）有强视觉-语言骨干（CLIP-ViT-L/14）和高质量文本生成器（InternVL2.5）；（3）训练资源充足（4 epoch, batch size 1024）。当这些条件不满足时，SD² 的优势可能减弱。例如，在 DF40-Test FE（Face Editing）子集上，SD² 的 ACC 为 90.43%，但 WildDeepFake 上仅 69.16%（Table 10），表明对某些未见过的伪造类型仍存在泛化缺口。此外，SD² 仅处理面部图像，不适用于全身伪造、音频或视频时序伪造。

**局限与开放问题。** 论文未讨论公平性——数据集包含多个来源（如 KoDF 含韩国人脸），但未按人口统计群体分析检测性能差异。VLM 生成的文本描述可能引入与种族、性别等相关的虚假关联，论文虽提及通过生成全面描述来解耦，但未提供定量验证。文本标签分离损失强制不同类别嵌入正交，可能丢失类型间的语义关联（如 Face Swapping 和 Face Editing 在真实场景中可能共存）。在更大规模数据上 SD² 是否会继续提升或最终饱和，仍是开放问题。最后，SD² 的推理速度和计算开销未分析，可能限制在实时部署场景中的应用。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Rich_Knowledge_Space_for_Scalable_Deepfake_Detection.pdf

![[paperPDFs/ICLR_2026/A_Rich_Knowledge_Space_for_Scalable_Deepfake_Detection.pdf]]

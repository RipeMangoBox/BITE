---
title: "Semi-Supervised Semantic Segmentation via Marginal Contextual Information"
type: paper
paper_level: A
venue: TMLR
year: 2024
pdf_ref: paperPDFs/TMLR_2024/Semi_Supervised_Semantic_Segmentation_via_Marginal_Contextual_Information.pdf
aliases:
- SSSSMCI
tags:
- TMLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "利用相邻像素的边际上下文信息计算事件联合概率，重新评估每个像素的置信度，从而放松伪标签传播的阈值，在不降低标签质量的前提下增加可用训练信号。"
primary_logic: "分割图中的标签具有强空间相关性；将孤立像素的预测替换为相邻像素组的联合概率，可以放大类别差异并抑制错误传播，缓解确认偏差。"
claims:
- "S4MC 在 PASCAL VOC 12 仅用 366 张标注图像时达到 79.09 mIoU，比 UniMatch 提升 1.39 mIoU。"
- "S4MC 在训练早期显著增加伪标签数量，同时提高伪标签精度。"
- "S4MC 在 Cityscapes 1/16 分区 (186 张) 上比 UniMatch 高 1.01 mIoU。"
- "PASCAL VOC 12 (1/4 partition, 366 labeled) 上 mIoU = 79.09 ± 0.18"
---

# Semi-Supervised Semantic Segmentation via Marginal Contextual Information

> [!tip] 核心洞察
> 分割图中的标签具有强空间相关性；将孤立像素的预测替换为相邻像素组的联合概率，可以放大类别差异并抑制错误传播，缓解确认偏差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于边际上下文信息的半监督语义分割 |
| 英文题名 | Semi-Supervised Semantic Segmentation via Marginal Contextual Information |
| 会议/期刊 | TMLR 2024 |
| Links | [paper](https://arxiv.org/abs/2308.13900); [Project](https://s4mcontext.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | S4MC |
| Dataset | PASCAL VOC 12 (1/4 partition, 366 labeled), Cityscapes (1/16 partition, 186 labeled), MS COCO (1/256 partition, 463 labeled) |

> [!tip] 效果简介
> - PASCAL VOC 12 (1/4 partition, 366 labeled) 上，mIoU 为 79.09 ± 0.18，对比 77.7 (UniMatch)，变化 +1.39。
> - Cityscapes (1/16 partition, 186 labeled) 上，mIoU 为 77.0，对比 75.99 (UniMatch)，变化 +1.01。
> - MS COCO (1/256 partition, 463 labeled) 上，mIoU 为 40.4，对比 38.9 (Supervised Baseline, Table 5)，变化 +1.5。

## 概述

半监督语义分割的核心瓶颈在于：基于置信度的伪标签过滤策略过于严格，导致大量无标签数据无法被有效利用，训练信号不足，尤其在低标注比例下模型容易过拟合。S4MC 提出利用**边际上下文信息**——即相邻像素的类别事件联合概率——重新评估每个像素的置信度，从而在保持伪标签质量的前提下放松传播阈值，增加可用训练信号。

**核心思路**：分割图中的标签具有强空间相关性。将孤立像素的预测替换为相邻像素组的联合概率估计，可以放大类别差异并抑制错误传播，缓解半监督学习中的确认偏差。S4MC 在教师-学生框架的基础上，引入**动态分位数阈值调整**和**边际上下文细化模块**，对教师模型的预测进行后处理后再用于学生模型训练。

**主要结果**：
- 在 PASCAL VOC 12 仅用 366 张标注图像时达到 **79.09 mIoU**，比当前最优方法 UniMatch 提升 **+1.39 mIoU**（Table 1）。
- 在 Cityscapes 1/16 分区（186 张标注）上达到 **77.0 mIoU**，比 UniMatch 提升 **+1.01 mIoU**（Table 4）。
- 在 MS COCO 1/256 分区（463 张标注）上达到 **40.4 mIoU**，比有监督基线提升 **+1.5 mIoU**（Table 5）。

**方法定位**：S4MC 属于基于伪标签的半监督分割方法，继承自 FixMatch 的置信度过滤范式，并在 UniMatch 的基础上通过空间上下文建模实现改进。其边际上下文细化机制可视为一种即插即用的伪标签后处理模块，不改变主干网络结构。

## 背景与动机

语义分割的标注成本极高——像素级标签需要专业标注员为每张图像的每个像素分配类别，这使得大规模全监督训练在多数应用场景中难以实现。半监督语义分割旨在同时利用少量精确标注图像和大量未标注图像，在降低标注依赖的同时逼近全监督性能，因而成为密集预测领域的研究热点。

当前半监督分割的主流范式建立在**伪标签自训练**之上：教师模型对未标注图像生成预测，将高置信度像素的类别作为伪标签，用于训练学生模型。代表性方法如 **FixMatch**（Sohn et al., NeurIPS 2020）采用固定阈值过滤低置信度预测，**UniMatch**（Yang et al., CVPR 2023）在此基础上引入特征级和图像级强增强，取得了当前最优性能。

然而，这一范式存在一个根本性瓶颈：**基于置信度的伪标签过滤过于严格**。模型仅将预测概率高于预设阈值的像素纳入训练，大量无标签数据因置信度不足而被丢弃。在低标注比例下（如 PASCAL VOC 12 仅用 366 张标注图像），可用的监督信号极度匮乏，模型容易过拟合到少量标注样本，形成**确认偏差**——模型不断强化自身已有的错误预测，难以自我纠正。

问题的症结在于**孤立地评估每个像素的置信度**。现有方法对每个像素独立计算最大概率或 margin 值，完全忽略了分割任务的内在属性：分割图中的标签具有强空间相关性，相邻像素极大概率属于同一类别。这种空间相干性是语义分割的基本先验，但未被现有伪标签过滤机制所利用。

本文的核心洞察是：**将孤立像素的预测替换为相邻像素组的联合概率，可以放大类别差异并抑制错误传播**。直观上，若某像素的类别预测不确定，但其邻域像素对该类别有高置信度，则联合考虑这些像素应能提升该像素的置信度。这一思想通过**事件联合概率**的形式化建模——计算“至少一个相邻像素属于某类别”的概率——实现了伪标签置信度的重新评估，从而在**不降低标签质量的前提下放松传播阈值**，显著增加可用训练信号。

具体而言，本文提出 **S4MC**，在教师-学生框架中嵌入**边际上下文细化模块**，利用邻域像素的边际信息重新计算每个像素的类别概率，并结合**动态分位数阈值调整（DPA）**策略，使模型在训练早期就能生成更多且更高质量的伪标签（见 Figure 4），有效缓解确认偏差，突破低标注场景下的性能瓶颈。

## 核心创新

S4MC 的核心创新在于用**边际上下文信息（Marginal Contextual Information）**重新定义伪标签的置信度评估，从而打破传统基于单像素置信度过滤的瓶颈。其关键设计可拆解为两个相互协同的 changed slots。

### 1. 从孤立像素到邻域联合：伪标签置信度的重新定义

传统半监督分割方法（如 **FixMatch** (Sohn et al., NeurIPS 2020) 及 **UniMatch** (Yang et al., CVPR 2023)）依赖单像素的最大类别概率或 margin 值来决定是否采用某个伪标签。这种逐像素独立判决的方式在低标注比例下过于严苛，导致大量正确但置信度略低的像素被丢弃，训练信号严重不足。

S4MC 的因果调节旋钮在于：**利用分割图中标签的强空间相关性，将孤立像素的置信度替换为相邻像素组的事件联合概率**。具体而言，对于像素 $x_{j,k}^i$ 的类别 $c$，不再直接使用其原始预测概率 $p_c(x_{j,k}^i)$，而是在其邻域内寻找能最大化联合概率的邻居 $x_{\ell,m}^i$，计算二者属于同一类别 $c$ 的事件联合概率上界：

$$p_c(x_{j,k}^i \cup x_{\ell,m}^i) \leq p_c(x_{j,k}^i) + p_c(x_{\ell,m}^i) - p_c(x_{j,k}^i) \cdot p_c(x_{\ell,m}^i)$$

随后取邻域内使该上界最大的邻居作为细化后的类别概率：

$$\tilde{p}_c(x_{j,k}^i) = \max_{\ell,m} p_c(x_{j,k}^i \cup x_{\ell,m}^i)$$

这一操作的深层机制在于：当某个像素的预测存在不确定性时，若其邻近像素对同一类别有较高置信度，联合概率会被显著放大；反之，若邻域内不存在支持证据，联合概率不会产生虚假提升。这等价于在空间维度上对类别差异进行**放大**，同时**抑制孤立噪声的传播**，从而缓解半监督学习中典型的确认偏差（confirmation bias）问题。

Figure 1 直观展示了这一机制的效果：在“猫”类别的分割中，未经细化的伪标签存在大量空洞和缺失，而经过边际上下文细化后，同一模型输出的伪标签覆盖了更多正确区域。红色方框标注的像素在细化前，最高两类概率分别为 0.45 和 0.41，margin 极小，无法通过阈值；细化后，最高概率提升至 0.72，成功被纳入训练。

### 2. 阈值调度与细化解耦：让更多像素通过而不牺牲质量

仅有置信度细化并不足以充分发挥作用——如果阈值调度机制与细化过程耦合不当，性能提升将大打折扣。S4MC 的第二个关键设计是**将阈值计算与伪标签过滤解耦**：

- **阈值计算**：使用教师模型**未细化前的原始预测** $p_c(x_{j,k}^i)$ 来计算动态分区阈值（Dynamic Partition Adjustment, DPA），该阈值基于当前批次置信度的分位数线性衰减，初始分位数比例 $\alpha_0 = 0.4$（即训练初期允许 60% 的像素通过阈值，见 Table 6）。
- **伪标签过滤**：使用**细化后的概率** $\tilde{p}_c(x_{j,k}^i)$ 与上述阈值进行比较，决定是否采用该像素的伪标签。

这种解耦的精妙之处在于：细化操作系统性地抬升了正确像素的置信度，而阈值本身并未改变。因此，**更多像素自然通过原有的阈值门槛，伪标签数量显著增加，同时细化机制保证了这些新增标签的质量**。

Figure 4 的定量证据直接支撑了这一因果链条：在 PASCAL VOC 12 的 366 张标注图像设置下，S4MC 在训练早期显著提升了通过阈值的像素比例（Figure 4a），同时伪标签的精度也明显高于不使用细化的基线（Figure 4b）。这说明 S4MC 并非简单降低阈值来“放水”，而是在不牺牲标签质量的前提下扩大了训练信号的覆盖范围。

### 3. 消融证据：两个组件的独立贡献与协同效应

Table 8 的消融实验清晰揭示了两个 changed slots 各自的贡献与交互关系：

- **伪标签细化模块（PLR）单独使用时**，在 UniMatch 基础上提升 **1.09 mIoU**，证明了边际上下文信息本身的有效性。
- **动态阈值调整（DPA）单独使用时**，反而对性能有害。这是因为在没有细化的情况下，盲目降低阈值会引入大量噪声标签，加剧确认偏差。
- **PLR 与 DPA 联合使用时**，取得最优性能，验证了二者的协同机制：细化提升置信度质量，DPA 在此基础上动态调节阈值以充分利用细化带来的增益。

此外，Table 7 表明 **3×3 邻域内选择最高概率邻居** 进行联合估计效果最优，继续增大邻域收益递减；Table F.1 表明 **$\kappa_{\mathrm{margin}}$（最高与次高概率之差）** 作为置信度函数优于 $\kappa_{\max}$ 和 $\kappa_{\mathrm{ent}}$，在 1/4 分区下表现最佳。

### 4. 创新边界与局限

S4MC 的创新高度依赖**空间相干性假设**——即相邻像素大概率属于同一类别。这一假设在自然图像的分割任务中成立，但在医学影像等纹理复杂、边界模糊的领域可能失效，需要手动验证。此外，当前方法采用固定形状的方形邻域，未利用物体的结构信息（如分割区域或超像素），这构成了进一步改进的空间。

## 整体框架

S4MC 沿用半监督语义分割中经典的**教师-学生框架**，并在此基础上引入两个关键改进：**动态分区阈值调整 (DPA)** 与**边际上下文细化模块**。整体 pipeline 如下：

### 1. 双网络结构与 EMA 更新

系统包含结构相同的教师网络 $f_{\theta_t}$ 与学生网络 $f_{\theta_s}$。学生网络同时接受有标签数据与无标签数据的训练，而教师网络不参与梯度反向传播，其参数通过学生参数的指数移动平均 (EMA) 更新：

$$\theta_t^{\eta} = \tau \theta_t^{\eta-1} + (1 - \tau) \theta_s^{\eta}$$

教师网络负责对无标签数据生成预测，这些预测经细化后作为伪标签监督学生网络，形成自训练闭环。

### 2. 损失函数构成

总损失为有监督损失与无监督损失的加权和：

$$\mathcal{L} = \mathcal{L}_s + \lambda \mathcal{L}_u$$

- **有监督损失** $\mathcal{L}_s$：对有标签像素计算标准交叉熵损失。
- **无监督损失** $\mathcal{L}_u$：以教师网络生成并经细化后的伪标签为目标，对学生网络在无标签数据上的预测计算交叉熵损失。仅置信度超过动态阈值的像素参与损失计算。

### 3. 伪标签生成与 DPA 阈值调度

教师网络对无标签图像预测类别概率分布后，首先计算每个像素的置信度得分 $\kappa$（采用 margin 形式，即最高与次高概率之差）。随后，**DPA 模块**根据当前批次置信度分位数动态确定阈值 $\gamma_t$：初始分位数比例 $\alpha_0 = 0.4$（即初始时 60% 的像素可通过阈值），阈值随训练进程线性衰减，逐步增加伪标签数量。

### 4. 边际上下文细化模块

这是 S4MC 的核心创新。在 DPA 确定阈值之前，先对教师预测进行**像素级置信度细化**：对每个像素，在其 $3\times3$ 邻域内寻找能使事件联合概率上界最大的邻居，用该联合概率替代原始类别概率。联合概率上界基于独立性假设计算：

$$p_c(x_{j,k}^i \cup x_{\ell,m}^i) \leq p_c(x_{j,k}^i) + p_c(x_{\ell,m}^i) - p_c(x_{j,k}^i) \cdot p_c(x_{\ell,m}^i)$$

细化后的概率 $\tilde{p}_c$ 用于过滤伪标签，而 DPA 阈值的计算仍基于细化前的原始预测 $p_c$。这一设计的精妙之处在于：**阈值本身不变，但因细化后更多像素的置信度越过阈值，伪标签数量自然增加，同时标签质量因邻域联合概率的放大效应而得以保持甚至提升**。

### 5. 数据流总结

1. 有标签数据 → 学生网络 → 计算 $\mathcal{L}_s$
2. 无标签数据 → 教师网络 → 原始预测 $p_c$ → 边际上下文细化 → 细化预测 $\tilde{p}_c$
3. 原始预测 $p_c$ → DPA 计算动态阈值 $\gamma_t$
4. 细化预测 $\tilde{p}_c$ 经 $\gamma_t$ 过滤 → 伪标签 $\hat{y}$
5. 无标签数据 → 学生网络 → 以伪标签为目标计算 $\mathcal{L}_u$
6. 学生参数 EMA → 更新教师参数

该框架的核心因果机制在于：**利用分割图中天然的像素空间相关性，将孤立像素的置信度评估替换为邻域联合概率评估，从而在不降低伪标签精度的前提下大幅增加可用训练信号，缓解低标注比例下的过拟合与确认偏差**。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/015_Figure.jpg]]
*Figure: A.2: Qualative results of our method comparison to UniMatch baseline over COCO with 1/32 of the labeled examples. The segmentation map Left to right: Ground Truth, UniMatch prediction, S4MC Prediction*

## 核心模块与公式推导

### 教师-学生框架与损失函数

S4MC 沿用半监督语义分割中经典的教师-学生范式。学生网络 $f_{\theta_s}$ 同时在有标注数据和无标注数据上训练，教师网络 $f_{\theta_t}$ 通过指数移动平均（EMA）从学生参数更新：

$$\theta_t^{\eta} = \tau \theta_t^{\eta-1} + (1 - \tau) \theta_s^{\eta}$$

其中 $\eta$ 为训练步数，$\tau$ 为动量系数。教师网络负责为无标注图像生成伪标签，学生网络则利用这些伪标签进行学习。

总损失函数为有监督损失与无监督损失的加权和：

$$\mathcal{L} = \mathcal{L}_s + \lambda \mathcal{L}_u$$

有监督损失 $\mathcal{L}_s$ 对标注图像中所有像素计算标准交叉熵：

$$\mathcal{L}_s = \frac{1}{M_l} \sum_{\mathbf{x}_i^\ell, \mathbf{y}_i \in B_l} \ell_{CE}\big(f_{\theta_s}(\mathbf{x}_i^\ell), \mathbf{y}_i\big)$$

无监督损失 $\mathcal{L}_u$ 以教师网络生成的伪标签为目标，仅在伪标签通过置信度筛选的像素上计算：

$$\mathcal{L}_u = \frac{1}{M_u} \sum_{\mathbf{x}_i^u \in \mathcal{B}_u} \ell_{CE}(f_{\theta_s}(\mathbf{x}_i^u), \hat{\mathbf{y}}_i)$$

其中 $M_l$、$M_u$ 分别为有标注和无标注批次中的有效像素数，$\hat{\mathbf{y}}_i$ 为分配后的伪标签。

---

### 伪标签分配与置信度度量

伪标签的分配遵循阈值过滤规则。对于无标注图像中的像素 $x_{j,k}^i$，当置信度得分 $\kappa$ 超过动态阈值 $\gamma_t$ 时，将最高概率类别作为伪标签；否则忽略该像素：

$$\hat{\mathbf{y}}_{j,k}^i = \begin{cases} \arg\max_c \{p_c(x_{j,k}^i)\} & \text{if } \kappa(x_{j,k}^i; \theta_t) > \gamma_t, \\ \text{ignore} & \text{otherwise} \end{cases}$$

S4MC 采用 margin 作为置信度度量函数，即最高类别概率与次高类别概率之差，相比直接使用最大概率更为稳定：

$$\kappa_{\mathrm{margin}}(x_{j,k}^i) = \max_c \{p_c(x_{j,k}^i)\} - \operatorname*{max2}_c \{p_c(x_{j,k}^i)\}$$

---

### 动态分区阈值调整（DPA）

阈值 $\gamma_t$ 并非固定不变，而是通过动态分区阈值调整（Dynamic Partition Adjustment, DPA）机制随训练进程自适应变化。DPA 根据当前批次中所有像素置信度得分的分位数线性衰减阈值，使得训练初期即有大量像素通过筛选，逐步收紧标准。关键设计在于：**DPA 使用教师网络未细化的原始预测 $p_c(x_{j,k}^i)$ 计算分位数阈值，但按细化后的置信度 $\tilde{p}_c(x_{j,k}^i)$ 过滤伪标签**。这意味着细化操作放大了类别差异，使更多像素在不降低阈值的情况下通过筛选，从而在不牺牲标签质量的前提下增加训练信号。初始分位数比例 $\alpha_0 = 0.4$，即训练开始时 60% 的原始预测可通过阈值（Table 6）。

---

### 边际上下文细化模块

这是 S4MC 的核心创新。基于分割图中标签的空间相干性假设，S4MC 利用相邻像素的边际上下文信息重新估计每个像素的类别置信度，以缓解确认偏差。

对于像素 $x_{j,k}^i$ 及其邻域像素 $x_{\ell,m}^i$，定义事件联合概率——即两个像素中至少有一个属于类别 $c$ 的概率。在独立性假设下，该联合概率的上界为：

$$p_c(x_{j,k}^i \cup x_{\ell,m}^i) \leq p_c(x_{j,k}^i) + p_c(x_{\ell,m}^i) - p_c(x_{j,k}^i) \cdot p_c(x_{\ell,m}^i)$$

基于此上界，S4MC 提出两种细化策略：

**最大邻居选择**：在 $3\times3$ 邻域内，选择能使联合概率上界最大的邻居，以该联合概率作为更新后的类别概率：

$$\tilde{p}_c(x_{j,k}^i) = \max_{\ell,m} p_c(x_{j,k}^i \cup x_{\ell,m}^i)$$

**多邻居空间加权细化**：通过空间距离加权融合多个邻居的信息：

$$\tilde{p}_c(x_{j,k}^i) = p_c(x_{j,k}^i) + \beta_{\ell,m}\big[p_c(x_{\ell,m}^i) - p_c(x_{j,k}^i, x_{\ell,m}^i)\big]$$

其中 $\beta_{\ell,m}$ 为基于空间距离的权重因子。消融实验表明，$3\times3$ 邻域内选择最高概率邻居进行联合估计效果最优，继续增大邻域收益递减（Table 7）。

细化后的概率 $\tilde{p}_c$ 用于计算 margin 置信度 $\kappa_{\mathrm{margin}}$，进而决定伪标签的分配。这一设计的因果机制在于：当邻域像素对同一类别具有较高置信度时，联合概率显著高于单像素概率，使原本处于阈值边缘的正确预测得以通过筛选；反之，孤立的高置信度噪声则难以从邻域获得支持，从而被有效抑制。

## 实验与分析

### 核心实验设置

S4MC 基于教师-学生框架构建。教师网络参数 $\theta_t$ 通过学生参数 $\theta_s$ 的指数移动平均（EMA）更新：

$$\theta_{t}^{\eta} = \tau \theta_{t}^{\eta-1} + (1 - \tau) \theta_{s}^{\eta}$$

有监督损失 $\mathcal{L}_s$ 对标注像素计算标准交叉熵，无监督损失 $\mathcal{L}_u$ 以细化后的伪标签为目标计算交叉熵，总损失为二者的加权和：

$$\mathcal{L} = \mathcal{L}_s + \lambda \mathcal{L}_u$$

伪标签分配遵循阈值过滤机制：当像素的置信度得分 $\kappa(x_{j,k}^i; \theta_t)$ 超过动态阈值 $\gamma_t$ 时，将最高概率类别作为伪标签，否则忽略该像素。置信度得分采用 margin 函数：

$$\kappa_{\mathrm{margin}}(x_{j,k}^i) = \max_c \{p_c(x_{j,k}^i)\} - \operatorname*{max2}_c \{p_c(x_{j,k}^i)\}$$

阈值 $\gamma_t$ 由动态分区阈值调整（DPA）策略决定：使用教师网络**细化前**的预测计算分位数阈值，但按**细化后**的置信度进行过滤，从而在阈值不变的前提下让更多像素通过筛选。初始分位数比例 $\alpha_0 = 0.4$，即训练初期有 60% 的原始预测通过阈值。

---

### 主要结果

S4MC 在三个主流语义分割基准上均取得一致且显著的提升，验证了边际上下文信息对伪标签质量的关键作用。

**PASCAL VOC 12（ResNet-101 骨干，1/4 分区，366 张标注图像）**：S4MC 达到 **79.09 ± 0.18 mIoU**，比当前最优方法 **UniMatch**（Yang et al., CVPR 2023）的 77.7 mIoU 提升 **+1.39 mIoU**（Table 1）。在更低标注比例下（1/16 分区，92 张标注图像），S4MC 在 ResNet-50 骨干上达到 72.62 mIoU（Table 2）。在增广 PASCAL VOC 12 数据集上（含 Hariharan et al. 2011 的弱标注数据），CutMix-Seg + S4MC 在 1/16 分区（662 张标注图像）达到 78.84 mIoU（Table 3）。

**Cityscapes（ResNet-101 骨干，1/16 分区，186 张标注图像）**：S4MC 达到 **77.0 mIoU**，比 UniMatch 的 75.99 mIoU 提升 **+1.01 mIoU**（Table 4）。

**MS COCO（Xception-65 骨干，1/256 分区，463 张标注图像）**：S4MC 达到 **40.4 mIoU**，比有监督基线提升 **+1.5 mIoU**（Table 5）。在极端低标注场景（1/1024 分区，183 张标注图像）下，S4MC 的边界 IoU 同样优于 FixMatch（Table 9）。

---

### 消融实验

**各组件贡献（Table 8）**：在 UniMatch 基础上单独加入伪标签细化模块（PLR）即可提升 **1.09 mIoU**，验证了边际上下文细化的独立价值。值得注意的是，动态阈值调整（DPA）**单独使用反而有害**，这表明 DPA 降低阈值带来的伪标签数量增加，必须在 PLR 提供的高质量置信度评估前提下才能转化为性能增益。两者联合使用时，PLR 确保伪标签精度，DPA 放大可用训练信号，形成互补。

**邻域大小与邻居选择策略（Table 7）**：在 $3 \times 3$ 邻域内选择能使联合概率最大化的邻居效果最优。继续增大邻域（如 $5 \times 5$ 或引入距离加权）收益递减，说明局部空间相干性是最主要的信息来源，过大的邻域可能引入语义不相关的像素，稀释有效信号。

**置信度函数选择（Table F.1）**：在 1/4 分区下，$\kappa_{\mathrm{margin}}$（最高与次高概率之差）优于 $\kappa_{\max}$（仅取最高概率）和 $\kappa_{\mathrm{ent}}$（基于熵）。margin 函数对类别混淆更敏感，能更稳定地反映预测可靠性，这与 FixMatch（Sohn et al., NeurIPS 2020）的设计理念一致，但在分割场景下通过边际上下文进一步放大。

**初始分位数比例 $\alpha_0$（Table 6）**：$\alpha_0 = 0.4$ 取得最佳性能。过高的 $\alpha_0$（更严格的初始阈值）限制了早期训练信号，过低的 $\alpha_0$ 则引入过多噪声伪标签。

---

### 伪标签质量与数量分析

Figure 4 从训练过程角度揭示了 S4MC 的作用机制：

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/004_Figure_4.jpg]]
*Figure 4: (b) Accuracy of the pseudo labels. S4MC produces more quality pseudo labels during the training process, most notably at the early stages. Figure 4: pseudo label quantity and quality on PASCAL VOC 12 (Everingham et al., 2010) with 366 labeled images using our margin (5) confidence function. The training was performed using S4MC; metrics with and without S4MC were calculated*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/020_Figure.jpg]]
*Figure: (a) The spatial agreement as we define in in 9 compared between different variations of Unimatch and S4MC. (b) The spatial agreement, compared between different variations of (Yang et al., 2023) and S4MC over time. Figure F.1: Spatial agreement analysis off diffrent methods on PASCAL VOC 12 using ResNet-101 backbone*

- **伪标签数量（Figure 4a）**：S4MC 在整个训练过程中通过阈值的像素比例始终高于无细化版本，尤其在训练早期差异显著。这说明边际上下文细化有效放松了伪标签传播的阈值约束。
- **伪标签质量（Figure 4b）**：尽管通过阈值的像素更多，S4MC 的伪标签精度反而更高，尤其在训练早期。这直接验证了核心洞察——利用邻域像素的联合概率可以放大类别差异并抑制错误传播，缓解确认偏差。

Figure 1 提供了单类（Cat）的定性示例：红色方框标注的像素在细化前，前两类的预测概率接近，导致伪标签缺失；细化后类别差异被放大，正确伪标签得以传播。

---

### 失败模式与适用边界

1. **空间相干性假设的局限**：S4MC 的核心机制依赖相邻像素属于同一类别的先验，这在自然图像中通常成立，但在医学影像、遥感图像等非自然图像域可能失效。若目标区域呈碎片化分布或类别边界极其复杂，邻域像素的联合概率估计可能引入有害偏差，反而降低伪标签质量。该风险在论文中未被实验验证，需在实际部署前进行领域适配评估。

2. **固定方形邻域的限制**：当前方法使用固定形状的方形窗口选择邻居，未利用物体的结构信息（如分割区域或超像素）。当目标物体呈细长形状或位于边界处时，方形邻域可能包含大量无关像素，限制细化效果。Table 7 中增大邻域收益递减的现象也间接支持这一判断。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/011_Table_7.jpg]]
*Table 7: The effect of neighborhood size and neighbor selection criterion on the Pascal VOC 12 with 1/4 labeled data and ResNet-101 backbone. We denote the number of neighbors as k. We compared choosing one neighbor at random, the one with the highest cosine similarity to the pixel embedding, max probable neighbor and min probable neighbor. The idea of similar neighboring pixel is explained in the paper, while comparing to minimum probable neighbor try to see if the spatial information can contradict the prediction, reducing the likelihood to assign pseudo label to the predicted class*

3. **小规模标注数据的偏差放大**：在半监督场景下，模型仅使用少量标注数据，这些数据可能无法充分代表整体分布中的长尾类别或边缘案例。S4MC 虽然通过伪标签扩展了训练信号，但伪标签的质量仍受限于标注数据的初始偏差，可能在某些类别上持续表现不佳。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/005_Table_1.jpg]]
*Table 1: Comparison between our method and prior art on the PASCAL VOC 12 val (1,464 original annotated images out of 10,582 in total) under different partition protocols using ResNet-101 backbone. The caption describes the share of the training set used as labeled data and the actual number of labeled images. * denotes reproduced results using official implementation. ± denotes the standard deviation over three runs*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/006_Table_2.jpg]]
*Table 2: Comparison between our method and prior art on the PASCAL VOC 12 val (1,464 original annotated images out of 10,582 in total) under different partition protocols using ResNet-50 backbone. The caption describes the share of the training set used as labeled data*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/007_Table_3.jpg]]
*Table 3: Comparison between our method and prior art on the augmented PASCAL VOC 12 val dataset under different partitions, utilizing additional unlabeled data from Hariharan et al. (2011) (total of 10,582 training images, 9,118 weakly annotated) and using ResNet-101 backbone. We included the number of labeled images in parentheses for each partition ratio. * denotes reproduced results using official implementation*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/008_Table_4.jpg]]
*Table 4: Comparison between our method and prior art on the Cityscapes val dataset (total of 2,976 training images) under different partition protocols using ResNet-101 backbone. Labeled and unlabeled images are selected from the Cityscapes training dataset. For each partition protocol, the caption gives the share of the training set used as labeled data and the number of labeled images. * denotes reproduced results using official implementation*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/009_Table_5.jpg]]
*Table 5: Comparison between our method and prior art on COCO (Lin et al., 2014) val (total of 118,336 training images) on different partition protocols using Xception-65 backbone. For each partition protocol, the caption gives the share of the training set used as labeled data and the number of labeled images. * denotes reproduced results using official implementation*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/010_Table_6.jpg]]
*Table 6: The effect of α0, the initial proportion of confidence pixels for the Pascal VOC 12 with 1/4 labeled data and ResNet-101 backbone*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/012_Table_8.jpg]]
*Table 8: Ablation study on the different components of S4MC on top of UniMatch for the augmented Pascal VOC 12 with 1 / 2 labeled data and ResNet-101 backbone. PLR is the pseudo label refinement module and DPA is dynamic partition adjustment*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2308_13900/figures/013_Table_9.jpg]]
*Table 9: Evaluation of Boundary IoU (Cheng et al., 2021) comparing models trained with UniMatch+S4MC and with FixMatch using 183 (1/1024) annotated images on COCO, both uses Xception-65 backbone as in Table 5*

## 方法谱系与知识库定位

### 1. 方法继承与基线关系

S4MC 的核心框架建立在半监督学习的教师-学生范式和基于阈值的伪标签传播策略之上，其直接的方法论源头可追溯至两个关键工作：

- **FixMatch**（Sohn et al., NeurIPS 2020）：S4MC 继承了 FixMatch 的阈值化伪标签分配逻辑。具体而言，FixMatch 对弱增强的无标签图像进行教师预测，仅保留置信度超过固定阈值的像素作为伪标签，用于强增强版本的学生训练。S4MC 保留了这一基本流程，但对其中的两个关键环节进行了改造：置信度评估方式和阈值调度策略。

- **UniMatch**（Yang et al., CVPR 2023）：作为当前半监督语义分割的最先进方法，UniMatch 是 S4MC 的直接基线。S4MC 在 UniMatch 的教师-学生框架之上，引入了边际上下文细化模块和动态分位数阈值调整。在 PASCAL VOC 12 的 1/4 分区（366 张标注图像）上，S4MC 以 ResNet-101 为骨干网络达到 79.09 mIoU，比 UniMatch 的 77.7 mIoU 提升 1.39 个百分点（Table 1）；在 Cityscapes 1/16 分区（186 张标注图像）上，S4MC 达到 77.0 mIoU，比 UniMatch 的 75.99 mIoU 提升 1.01 个百分点（Table 4）。消融实验进一步表明，仅将伪标签细化模块（PLR）加入 UniMatch 即可带来 1.09 mIoU 的提升（Table 8），验证了边际上下文信息独立于基线的增益。

此外，S4MC 还与 **CutMix-Seg** 等方法进行了集成验证。在增广 PASCAL VOC 12 数据集上，CutMix-Seg + S4MC 在 1/16 分区（662 张标注图像）下达到 78.84 mIoU（Table 3），表明 S4MC 的细化策略可与不同的半监督分割基线协同工作。

### 2. 核心机制与知识库定位

S4MC 的方法论贡献在于对伪标签传播机制中两个关键环节的重新设计，其本质是对半监督学习中“确认偏差”问题的空间化解决方案：

**瓶颈识别**：基于置信度的伪标签过滤存在固有矛盾——严格的阈值保证了标签质量，却导致大量无标签数据被丢弃，训练信号不足，尤其在低标注比例下模型容易过拟合。这是半监督分割领域的共性瓶颈。

**因果调节变量**：S4MC 引入“边际上下文信息”作为调节变量。其核心洞察是：分割图中的标签具有强空间相关性；将孤立像素的预测替换为相邻像素组的事件联合概率，可以放大类别差异并抑制错误传播。具体而言，对于像素 $x_{j,k}^i$ 的类别 $c$，S4MC 计算其与邻域像素 $x_{\ell,m}^i$ 的联合概率上界：

$$\tilde{p}_c(x_{j,k}^i) = \max_{\ell,m} \left\{ p_c(x_{j,k}^i) + p_c(x_{\ell,m}^i) - p_c(x_{j,k}^i) \cdot p_c(x_{\ell,m}^i) \right\}$$

这一操作使得原本置信度不足的像素因邻域支持而获得更高的置信度得分，从而在不降低伪标签精度的前提下，显著增加了通过阈值的像素数量。Figure 4 的训练过程对比证实：S4MC 在训练早期即大幅增加了伪标签数量，同时提高了伪标签精度。

**阈值调度创新**：S4MC 采用动态分位数阈值调整（DPA），使用未细化的教师预测计算分位数阈值，但按细化后的置信度过滤伪标签。这意味着阈值本身保持不变，但更多像素因细化而满足了通过条件。初始分位数比例 $\alpha_0 = 0.4$（即 60% 的原始预测在训练初期通过阈值）取得最佳性能（Table 6）。

**消融关键发现**：值得注意的是，DPA 单独使用时反而有害（Table 8），只有在与 PLR 模块配合时才能发挥正向作用。这表明单纯的阈值放松会引入噪声，而边际上下文细化通过空间约束有效抑制了错误标签的传播，两者形成了必要的互补关系。

### 3. 适用边界与局限

S4MC 的有效性建立在两个核心假设之上，这些假设同时定义了其适用边界：

**空间相干性假设**：S4MC 假设相邻像素倾向于属于同一类别，这一假设在自然图像的语义分割中普遍成立（Figure F.1 的空间一致性分布分析提供了经验支持），但在以下场景可能失效：
- **医学影像等非自然图像域**：组织边界模糊、纹理异质性强，空间相干性假设不一定成立，可能引入有害偏差。该问题在论文中被明确列为局限性，但未提供实验验证。
- **细粒度边界区域**：在物体边界处，邻域像素可能属于不同类别，联合概率计算可能模糊边界。尽管 Table 9 的边界 IoU 评估显示 S4MC 优于 FixMatch，但固定形状的方形邻域本质上无法区分边界与内部区域。

**固定邻域形状的限制**：S4MC 采用固定大小的方形邻域（消融实验表明 3×3 最优，Table 7），未利用物体的结构信息。论文已指出这一局限，并提出了使用分割区域或超像素定义自适应邻域的开放问题，但未给出解决方案。

**任务泛化限制**：该方法专为密集预测任务设计，难以直接推广到图像分类等非密集任务。论文提出的开放问题——如何利用样本间关系替代空间邻域——目前尚无答案。

### 4. 开放问题与后续方向

基于 S4MC 的方法论框架和已知局限，以下研究方向值得关注：

- **自适应邻域构建**：能否利用分割区域、超像素或注意力机制定义内容感知的邻域，以更好地建模物体结构并处理边界区域？这直接回应了固定方形邻域的局限性。

- **跨任务迁移**：边际上下文的核心思想——利用相关样本的联合概率放大信号——是否可推广到非密集任务？例如，在少样本分类中利用特征空间的近邻关系，或在时序预测中利用时间邻域。

- **域外鲁棒性**：在医学影像、遥感等非自然图像域中，空间相干性假设的有效性需要系统验证。如果假设不成立，如何修正联合概率估计以适应异质性更强的数据分布？

- **与强增强策略的协同**：S4MC 目前与 CutMix-Seg 等增强策略的集成显示了初步协同效应，但更深入的机制分析（例如细化如何影响增强样本的伪标签质量）仍有待探索。

> **注意**：上述开放问题部分来自论文自身的讨论，部分基于方法局限性的合理推演。关于医学影像等域外应用的结论，论文仅提出了担忧而未提供实验证据，需要后续工作验证。

## 原文 PDF

![[paperPDFs/TMLR_2024/Semi_Supervised_Semantic_Segmentation_via_Marginal_Contextual_Information.pdf]]

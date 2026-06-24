---
title: "On The Effectiveness of Out-of-Distribution Data in Self-Supervised Long-Tail Learning"
type: paper
paper_level: A
venue: ICLR
year: 2023
pdf_ref: paperPDFs/ICLR_2023/On_The_Effectiveness_of_Out_of_Distribution_Data_in_Self_Supervised_Long_Tail_Learning.pdf
project_link: https://github.com/JianhongBai/COLT
aliases:
- CCODDLTL
- EODDSSLTL
tags:
- ICLR_2023
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "通过引入与少数类特征空间邻近的分布外（OOD）样本，动态扩增少数类的表示，并利用分布感知损失显式分离ID和OOD空间，从而重新平衡特征空间。"
primary_logic: "OOD样本可作为“桥梁”，在增强图中连接同一ID少数类的不同实例，提升其类内一致性和特征空间的均匀性，而无需昂贵的ID数据。"
claims:
- "COLT在多个长尾数据集上（CIFAR-10/100-LT, ImageNet-100-LT, Places-LT）大幅超越基线SimCLR，特别是少数类精度提升约12%（CIFAR-100-LT）"
- "COLT产生的特征空间更平衡（标准差Std显著降低），优于随机采样和使用ID数据的MAK方法"
- "消融实验表明分布感知损失、动态采样策略均对性能有重要贡献"
- "CIFAR-10-LT (IR=100) 上 Overall Accuracy (All) = 84.86 (BCL + COLT)"
---

# On The Effectiveness of Out-of-Distribution Data in Self-Supervised Long-Tail Learning

> [!tip] 核心洞察
> OOD样本可作为“桥梁”，在增强图中连接同一ID少数类的不同实例，提升其类内一致性和特征空间的均匀性，而无需昂贵的ID数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自监督长尾学习中分布外数据的有效性研究 |
| 英文题名 | On The Effectiveness of Out-of-Distribution Data in Self-Supervised Long-Tail Learning |
| 会议/期刊 | ICLR 2023 |
| Links | [paper](https://arxiv.org/abs/2306.04934); [GitHub](https://github.com/JianhongBai/COLT) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | COLT (Contrastive with Out-of-distribution data for Long-Tail learning) |
| Dataset | CIFAR-10-LT (IR=100), CIFAR-100-LT (IR=100), ImageNet-100-LT, Places-LT |

> [!tip] 效果简介
> - CIFAR-10-LT (IR=100) 上，Overall Accuracy (All) 为 84.86 (BCL + COLT)，对比 75.34 (SimCLR)，变化 +9.52。
> - CIFAR-100-LT (IR=100) 上，Overall Accuracy (All) 为 57.98 (BCL + COLT)，对比 47.65 (SimCLR)，变化 +10.33。
> - ImageNet-100-LT 上，Overall Accuracy (All, linear-probing) 为 72.22 (SimCLR+COLT 10K)，对比 67.08 (SimCLR)，变化 +5.14。

## 概述

自监督对比学习在长尾分布数据上存在一个关键瓶颈：多数类样本主导特征空间，少数类样本沦为稀疏的孤立点，导致少数类的线性可分性显著退化。本文提出 **COLT**（Contrastive with Out-of-distribution data for Long-Tail learning），核心洞察是——分布外（OOD）样本可以作为“桥梁”，在增强图中连接同一ID少数类的不同实例，从而提升类内一致性与特征空间的均匀性，而无需昂贵的ID数据。

COLT 包含三个关键机制：（1）**尾度分数估计**，无监督地定位头部与尾部样本；（2）**聚类预算分配与在线OOD采样**，动态选取与尾部聚类原型最相似的OOD样本；（3）**分布感知有监督对比损失**，利用域指示符显式分离ID与OOD空间。该方法可即插即用地接入 SimCLR 等主流自监督框架。

**主要结果**：在 CIFAR-10/100-LT、ImageNet-100-LT 和 Places-LT 上，COLT 大幅超越 SimCLR 基线，少数类精度提升约 12%（CIFAR-100-LT），整体精度标准差显著降低，特征空间更平衡。消融实验证实，真实图像OOD数据（如 300K Random Images）有效，而高斯噪声几乎无用；分布感知损失和动态采样策略对性能均有重要贡献。

## 背景与动机

### 长尾分布下的自监督学习困境

自监督对比学习（如 **SimCLR**）在均衡数据集上取得了显著成功，但其在长尾分布场景下的表现却大幅退化。现实世界的数据天然呈现长尾分布：少数头部类别拥有大量样本，而绝大多数尾部类别仅有稀疏实例。当直接在这种不平衡数据上训练对比学习模型时，多数类样本在特征空间中占据主导地位，其表示支配了整个嵌入空间的几何结构；少数类样本则被迫形成稀疏的孤立点，类内一致性差，线性可分性严重受损。

从特征空间的均匀性与对齐性两个维度来看，长尾问题造成的伤害是双重的。如 Figure 1 所示，标准 SimCLR 在长尾设定下，特征空间的均匀性显著恶化，少数类样本的对齐属性也远弱于多数类——这意味着同一尾部类别的不同实例在嵌入空间中彼此离散，难以形成紧凑的类簇。这种不平衡直接转化为下游任务中尾部类别的极低分类精度：在 CIFAR-100-LT（不平衡比 IR=100）上，SimCLR 的少数类（Few）精度远低于多数类（Many），整体精度仅 47.65%，且各类间精度标准差居高不下。

### 现有方法的局限

针对自监督长尾学习，已有若干方法试图缓解上述问题：

- **SDCLR** 引入自竞争机制，通过抑制头部类的过度表示来间接提升尾部类；
- **BCL** 利用记忆效应，在训练过程中动态调整样本的重要性权重；
- **MAK** 则采用外部采样策略，从额外的 ID 数据池中选取样本以平衡训练分布。

然而，这些方法存在一个共同的隐式假设：用于平衡特征空间的数据必须来自与下游任务相同的分布（ID 数据）。这一假设在实际场景中往往难以满足——获取大规模、高质量且类别均衡的 ID 数据成本高昂，甚至不可行。更根本的问题是，现有方法未能回答一个关键疑问：**分布外（OOD）数据能否替代 ID 数据，用于重新平衡自监督学习的特征空间？**

### 核心动机：OOD 数据的未开发潜力

本文的出发点正是对这一问题的正面回应。直觉上，OOD 样本如果与少数类的特征空间邻近，可以充当“桥梁”角色：在增强图中连接同一少数类的不同实例，提升其类内一致性，从而改善特征空间的均匀性。这一机制不要求 OOD 数据与 ID 数据共享类别标签，仅需其在表示空间中靠近尾部类即可。

基于此，本文提出了 **COLT（Contrastive with Out-of-distribution data for Long-Tail learning）**——一种即插即用的框架，旨在有效利用廉价、易获取的 OOD 数据，动态重新平衡长尾自监督学习的特征空间。COLT 的核心思想包括三个层面：（1）以无监督方式定位头部与尾部样本；（2）基于尾部感知的预算分配策略，在线从 OOD 池中采样对尾部类最有帮助的样本；（3）通过分布感知的有监督对比损失，显式分离 ID 与 OOD 表示空间，避免域混淆。

### 问题定位与贡献概要

综上，本文瞄准的核心瓶颈是：**自监督对比学习中，长尾数据导致特征空间不平衡，少数类表示质量差**。其因果调控手段为：**引入与少数类特征空间邻近的 OOD 样本，动态扩增尾部表示**。核心洞察在于：OOD 样本可作为“桥梁”，在增强图中连接同一 ID 少数类的不同实例，提升类内一致性和特征空间的均匀性，而无需昂贵的 ID 数据。

后续章节将依次展开 COLT 的完整方法设计、实验验证与深入分析，系统论证 OOD 数据在自监督长尾学习中的有效性及其作用机理。

## 核心创新

COLT的核心创新在于**将分布外（OOD）数据从“需要防御的噪声”重新定位为“可主动利用的平衡资源”**，并通过三个紧密耦合的机制实现长尾自监督特征空间的再平衡。

### 1. 无监督尾度感知与动态预算分配

COLT不依赖任何类别标签，而是从对比学习的内部信号中提取“尾度分数”（Tailness Score），用于无监督地定位头部与尾部样本。其关键洞察在于：**少数类样本在对比损失中对负样本的预测概率更高**——因为它们的特征表示稀疏且缺乏足够的正样本支撑。基于此，尾度分数定义为每个ID样本的top-k%最大负对数概率的负和：

$$s_t^i = - \sum_{\mathrm{top}-k\%} p_i^-$$

其中 $p_i^-$ 为样本 $i$ 对负样本的softmax概率。该分数通过动量更新进行平滑，以提高鲁棒性和判别力。随后，对ID特征进行K-means聚类，计算每簇的平均尾度分数，并通过softmax归一化将总采样预算 $K$ 按簇分配：

$$K' = K \cdot \text{softmax}(\widetilde{s_t^c} / \tau_c)$$

这一机制使得尾部聚类获得更多OOD采样配额，实现了**面向特征空间的、细粒度的动态再平衡**，而非简单的类别频率补偿。

### 2. 在线OOD采样作为“特征桥梁”

COLT从外部OOD池中，定期选取与各聚类原型余弦相似度最高的样本，动态注入训练过程。其核心作用机制不同于传统的数据增强或重采样：**OOD样本在增强图中充当“桥梁”**，连接同一ID少数类的不同实例，提升其类内一致性和特征空间的均匀性。

消融实验（Figure 3a）提供了关键因果证据：将OOD数据集替换为高斯噪声几乎无帮助，而使用真实图像数据集（300K Random Images、STL、ImageNet等）则带来显著增益。这表明OOD数据的有效性源于其**语义邻近性**——与尾部类特征空间接近的OOD样本能够扩增少数类的表示支撑，而纯噪声缺乏这种语义结构。

### 3. 分布感知有监督对比损失

引入OOD数据后，COLT面临一个新问题：如何防止ID和OOD特征空间的无序混合？为此，COLT引入**分布感知的有监督对比损失**（$L_{SCL}$），利用域指示符 $\phi(x_i) \in \{+1, -1\}$ 区分ID和OOD样本：

$$\mathcal{L}_{SCL} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{|P(i)|} \sum_{p \in P(i)} -\log \frac{\exp(z_i \cdot z_p / \tau)}{\exp(z_i \cdot z_p / \tau) + \sum_{n \in N(i)} \exp(z_i \cdot z_n / \tau)}$$

其中正样本 $P(i)$ 为与锚点同域的样本，负样本 $N(i)$ 为异域样本。该损失**显式分离ID和OOD两个域**，使模型在利用OOD扩增尾部表示的同时，保持域间边界清晰。最终损失为：

$$\mathcal{L}_{COLT} = \mathcal{L}_{CL} + \alpha \mathcal{L}_{SCL}$$

消融实验（Figure 3c）证实，分布感知损失既提升了整体精度，也显著降低了各类间精度的标准差——这是特征空间更平衡的直接证据。

### 与基线方法的核心差异

| 机制维度 | SimCLR（基线） | COLT（本文） |
|---------|--------------|------------|
| 训练数据 | 仅长尾ID数据 | ID数据 + 在线动态采样的OOD数据 |
| 采样策略 | 无外部采样 | 基于尾度分数和聚类预算的定向采样 |
| 损失函数 | 标准对比损失 $L_{CL}$ | $L_{CL} + \alpha L_{SCL}$（增加域分离） |
| 尾部处理 | 隐式依赖数据增强 | 显式通过OOD桥梁扩增尾部表示 |

COLT可以即插即用地集成到大多数自监督框架（SimCLR、SDCLR、BCL）中，其增益在多个基准上得到验证：在CIFAR-100-LT（IR=100）上，BCL+COLT相比SimCLR提升10.33个百分点；在ImageNet-100-LT上提升5.14个百分点（Table 1, Table 2）。更重要的是，COLT在相同采样预算下显著优于随机采样和基于ID数据的MAK方法（Table 3, Table 4），证明了其采样策略和OOD利用机制的有效性。

## 整体框架

COLT 是一个即插即用的长尾自监督学习增强框架，其核心设计思路是**利用分布外数据动态重平衡特征空间**。整个框架由四个关键模块串联构成，形成一条从“定位尾部样本”到“引入 OOD 样本”再到“显式分离域”的完整流水线。

### 模块关系与数据流

COLT 的输入包含两个数据源：**长尾分布的 ID 数据集**和**外部 OOD 数据集**。框架的工作流程如下：

1. **尾度分数估计**：在每轮训练中，利用当前模型的对比损失分量，为每个 ID 样本计算尾度分数 $s_t^i$，并通过动量更新使其更鲁棒。该分数在无监督条件下定位头部与尾部样本。

2. **聚类预算分配**：对 ID 样本的当前表示进行 K-means 聚类，计算每个聚类的平均尾度分数 $s_t^{c_i}$，然后通过 softmax 归一化将总采样预算 $K$ 按比例分配给各聚类——尾部聚类获得更多预算。

3. **在线 OOD 采样**：每隔 $r$ 个 epoch，从 OOD 池中为每个聚类选取与其原型余弦相似度最高的样本，动态补充到训练集中。

4. **分布感知对比损失**：将 ID 和 OOD 样本分别赋予域指示符 $\phi(x_i) = +1$（ID）和 $\phi(x_i) = -1$（OOD），在标准 SimCLR 对比损失 $\mathcal{L}_{CL}$ 之上叠加有监督对比损失 $\mathcal{L}_{SCL}$，强制模型在嵌入空间中拉近同域样本、推远异域样本。

最终损失函数为两者的加权和：

$$\mathcal{L}_{COLT} = \mathcal{L}_{CL} + \alpha \mathcal{L}_{SCL}$$

### 核心机制

COLT 的关键洞察在于：OOD 样本并非被当作额外的“伪类别”来学习，而是充当**连接同一 ID 少数类不同实例的桥梁**。如 Figure 5 的增强图可视化所示，OOD 样本在表示空间中与尾部 ID 实例形成新的边，提升了少数类的类内一致性和特征空间的均匀性。分布感知损失则确保 ID 和 OOD 两个域在嵌入空间中保持显式分离，避免 OOD 样本污染 ID 类的判别边界。

整个框架对基础 SSL 方法透明——Figure 2 中以红色标注的组件均可直接插入 SimCLR、SDCLR、BCL 等现有框架，无需修改其核心训练逻辑。

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Contrastive with Out-of-distribution data for Long-Tail learning (COLT). COLT can be easily plugged into most SSL frameworks. Proposed components are denoted as red*

## 核心模块与公式推导

COLT 由四个核心模块串联构成，其设计围绕一个中心逻辑：**无监督定位尾部样本 → 按簇分配采样预算 → 在线选取邻近的 OOD 样本 → 利用域标签显式分离 ID/OOD 特征空间**。

### 模块一：尾度分数估计（Tailness Score Estimation）

**动机**：长尾自监督学习中缺乏类别标签，无法直接识别头部/尾部样本。COLT 利用对比损失的负样本概率来无监督地量化每个样本的“尾部程度”。

**机制**：对于 ID 数据集中的每个实例 $x_i$，定义其尾度分数为 top-$k\%$ 最大负样本对数概率之和的负值：

$$s_t^i = -\sum_{\text{top-}k\%} p_i^-$$

其中 $p_i^-$ 是实例 $i$ 对负样本 $z_i^-$ 的 Softmax 概率：

$$p_i^{-} = \frac{\exp(z_i \cdot z_i^{-} / \tau)}{\exp(z_i \cdot z_i^{+} / \tau) + \sum_{z_i^{-} \in Z^{-}} \exp(z_i \cdot z_i^{-} / \tau)}$$

**直觉**：头部样本特征已充分聚集，其负样本概率分布较为均匀；尾部样本因特征稀疏，会被多数类样本强烈排斥，导致部分负样本概率异常高。因此尾部样本的 $s_t^i$ 值更大。

**动量更新增强鲁棒性**：为减少训练初期的不稳定性，对尾度分数施加指数移动平均：

$$s_t^{i,0} = s_t^{i}, \quad s_t^{i,n} = m s_t^{i,n-1} + (1-m) s_t^{i,n}$$

尾度分数估计的有效性在 Fig 3e 中得到验证：尾部样本的尾度分数显著高于头部样本，且动量更新使估计更加稳定（Table 8）。

---

### 模块二：簇级预算分配（Cluster-wise Budget Allocation）

**动机**：OOD 采样需要精确投向最需要增强的尾部区域，而非均匀撒布。

**机制**：
1. 对当前 batch 的 ID 特征进行 K-means 聚类，得到 $C$ 个簇。
2. 计算每个簇的尾度分数 $s_t^c$，为该簇内所有实例尾度分数的均值：

$$s_t^{c_i} = \frac{\sum_{z_j \in c_i} s_t^j}{|c_i|}$$

3. 对簇尾度分数标准化后，通过带温度系数 $\tau_c$ 的 softmax 分配总采样预算 $K$：

$$K' = K \cdot \text{softmax}\left(\widetilde{s_t^c} / \tau_c\right), \quad \widetilde{s_t^c} = \frac{s_t^c - \text{mean}(s_t^c)}{\text{std}(s_t^c)}$$

**效果**：尾度分数高的簇（富含尾部样本）获得更多 OOD 采样配额，头部簇获得较少配额。消融实验（Table 9）表明，簇数目 $C$ 在 10 到 100 范围内对精度影响不大，且无监督聚类表现接近有监督 Oracle 聚类。

---

### 模块三：在线 OOD 采样（Online OOD Sampling）

**机制**：每 $r$ 个 epoch，从外部 OOD 池中为每个簇选取与簇原型余弦相似度最高的 $K'$ 个样本，并入当前训练 batch。采样间隔 $r=25$ 时性能最优（Fig 3d）。

**关键设计**：
- **相似度选取而非随机选取**：确保 OOD 样本与目标尾部簇在特征空间邻近，从而有效充当“桥梁”。
- **动态更新**：随着训练推进，特征空间演变，簇原型和采样结果同步更新，保证 OOD 样本始终适配当前表示。

---

### 模块四：分布感知有监督对比损失（Distribution-Aware Supervised Contrastive Loss）

**动机**：单纯将 OOD 样本混入训练可能造成 ID/OOD 特征混杂。需要显式引导模型区分两个域。

**机制**：为每个样本引入域指示符 $\phi(x_i)$：

$$\phi(x_i) = \begin{cases} +1, & x_i \in S_{id} \\ -1, & x_i \in S_{ood} \end{cases}$$

基于域标签构造有监督对比损失 $\mathcal{L}_{SCL}$，拉近同域样本（ID-ID 或 OOD-OOD），推远异域样本（ID-OOD）：

$$\mathcal{L}_{SCL} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{|P(i)|} \sum_{p \in P(i)} -\log \frac{\exp(z_i \cdot z_p / \tau)}{\exp(z_i \cdot z_p / \tau) + \sum_{n \in N(i)} \exp(z_i \cdot z_n / \tau)}$$

其中 $P(i)$ 是与 $x_i$ 同域的正样本集，$N(i)$ 是异域负样本集。

**最终损失**：COLT 的总损失为 SimCLR 对比损失与分布感知损失的加权和：

$$\mathcal{L}_{COLT} = \mathcal{L}_{CL} + \alpha \mathcal{L}_{SCL}$$

其中标准 SimCLR 对比损失为：

$$\mathcal{L}_{CL} = \frac{1}{N} \sum_{i=1}^{N} -\log \frac{\exp(\boldsymbol{z}_i \cdot \boldsymbol{z}_i^{+} / \tau)}{\exp(\boldsymbol{z}_i \cdot \boldsymbol{z}_i^{+} / \tau) + \sum_{\boldsymbol{z}_i^{-} \in \boldsymbol{Z}^{-}} \exp(\boldsymbol{z}_i \cdot \boldsymbol{z}_i^{-} / \tau)}$$

**消融验证**（Fig 3c）：加入 $\mathcal{L}_{SCL}$ 后，整体精度提升的同时，各类间精度标准差（Std）显著下降，证明分布感知损失有效促进了特征空间的平衡。

## 实验与分析

### 主实验结果

COLT在多个长尾基准上一致且显著地提升了自监督对比学习基线的性能，尤其在少数类上增益突出，同时降低了类别间精度的标准差，表明特征空间更加平衡。

**CIFAR-10/100-LT**（Table 1）：在不平衡比率IR=100的设置下，COLT以SimCLR为基础框架，在CIFAR-10-LT上将整体精度从75.34%提升至84.86%（+9.52个百分点），标准差从6.19降至3.55；在CIFAR-100-LT上，整体精度从47.65%提升至57.98%（+10.33个百分点），标准差从9.48降至2.27。COLT的增益可叠加于其他长尾自监督方法之上：BCL+COLT在CIFAR-100-LT上达到57.98%，相比BCL自身的52.96%提升约5个百分点。

**ImageNet-100-LT与Places-LT**（Table 2）：在更大规模数据集上，COLT同样有效。以SimCLR为基线，COLT在ImageNet-100-LT上整体精度从67.08%提升至72.22%（+5.14个百分点），标准差从3.74降至3.48；在Places-LT上从44.78%提升至46.36%（+1.58个百分点），标准差从3.93降至3.83。值得注意的是，Places-LT上增益相对较小，可能与场景类数据集中少数类的语义特征更为分散、OOD样本的桥接效率下降有关，但该推测需要进一步验证。

**分组精度分析**：COLT对“Few”组（样本数最少的尾部类）的改善最为显著。以CIFAR-100-LT为例，SimCLR基线在Few组仅约41%，COLT提升至约55.8%（Table 1），相对提升超过35%。这表明OOD样本的引入确实有效补偿了尾部类在特征空间中的稀疏性问题。

### 与采样策略的对比消融

为验证COLT的采样策略优于简单基线，论文在相同OOD池和采样预算下进行了系统对比（Table 3）。

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/005_Table_3.jpg]]
*Table 3: Compare the proposed COLT with random sample and MAK under the same sampling pool and sampling budget. The best performance under each setting is marked as bold*

**与随机采样对比**：在300K Random Images作为OOD池、采样预算10K的条件下，COLT在ImageNet-100-LT上达到72.22%，而随机采样仅为68.94%。随机采样甚至在某些情况下低于不使用OOD的SimCLR基线（67.08%），说明不加区分地引入OOD样本可能引入噪声，反而损害表示学习。

**与MAK对比**：MAK（Jiang et al., 2021）是一种使用ID数据进行采样平衡的方法。在相同OOD池下，COLT（72.22%）显著优于MAK（69.52%），且COLT仅使用分布标签（ID vs OOD），而MAK需要真实类别标签。更关键的是，即使MAK使用完全同域的ID数据进行采样（Table 4），COLT使用OOD数据仍能达到可比甚至更优的性能（COLT 72.4±0.3 vs MAK-ID 72.0±0.5），而COLT无需任何ID类别标签，这在实际应用中具有显著优势。

**与半监督方法对比**（Table 5）：当同时利用OOD数据时，COLT（自监督）在ImageNet-100-LT上优于半监督方法FixMatch+OOD和Semi-SL。这暗示标准的半监督学习框架可能无法有效利用分布外数据，而COLT通过显式的分布感知对比损失和动态采样机制，更充分地挖掘了OOD数据的价值。

### 消融与超参数分析

**分布感知损失的作用**（Fig 3c）：移除分布感知有监督对比损失（L_SCL）后，整体精度下降约1.5个百分点，且标准差显著上升。这表明L_SCL不仅提升整体精度，更关键的是通过显式分离ID和OOD特征空间，防止OOD样本污染ID表示，从而维持了特征空间的平衡性。

**OOD数据集的影响**（Fig 3a）：COLT的性能高度依赖于OOD数据集的语义丰富度。使用300K Random Images（从互联网随机收集）作为OOD池时增益最大；使用STL-10或CIFAR-100等较小数据集时增益减弱；使用高斯噪声作为OOD几乎无帮助。这说明OOD样本需要具备真实的图像语义结构才能有效桥接ID样本。

**采样预算K**（Fig 3b）：在CIFAR-100-LT上，采样预算从0增至10K时精度快速提升，10K至15K时增益趋于饱和。这表明存在一个“有效OOD样本量”的阈值，超出后边际收益递减。

**采样间隔r**（Fig 3d）：采样间隔r=25时性能最优。间隔过小（频繁更新OOD样本）导致训练不稳定，间隔过大则OOD样本的桥接效应滞后于特征空间的变化。

**尾度分数估计**（Fig 3e, Table 8）：论文定义了尾度比率φ_tail来衡量尾部样本发现能力——即top-γ%尾度分数样本中真实尾部样本占比与全局尾部样本占比之比。实验表明，COLT的尾度分数能有效定位尾部样本，且动量更新机制对估计的鲁棒性至关重要（Table 8）。

**聚类数量C**（Table 9）：簇数目C在10到100范围内对最终精度影响不显著，且无监督K-means聚类与使用真实标签的Oracle聚类表现接近，表明COLT对聚类数量不敏感，具有良好的鲁棒性。

**OOD数据不平衡与规模鲁棒性**（Table 10, Table 11）：即使OOD数据集本身也存在类别不平衡，COLT仍能保持有效增益；OOD数据集规模从10K增至300K时性能持续提升但逐渐饱和。

### 特征空间定性分析

**归一化误分类矩阵（NMM）**（Figure 4）：NMM值越接近1.0表示各类间误分类越均衡。SimCLR在平衡CIFAR-100上NMM接近1.0（均匀分布），但在长尾CIFAR-100上NMM严重偏离1.0，多数类主导了误分类。加入COLT后，NMM显著向1.0回归，直观验证了特征空间平衡度的改善。

**增强图可视化**（Figure 5）：通过构造增强图（augmentation graph），将同一实例的不同增强视图连接起来，可以观察特征空间的连通性。在长尾设置下，少数类实例之间缺乏有效连接，形成孤立子图。引入OOD样本后，OOD样本作为“桥梁”连接了原本孤立的少数类实例（图中红色边），显著改善了少数类的类内一致性和特征空间均匀性。

**聚类尾度分数与少数类比例的相关性**（Figure 6）：在CIFAR-100-LT、ImageNet-100-LT和Places-LT上，聚类内少数类样本比例与聚类尾度分数之间存在显著的线性正相关，验证了尾度分数作为无监督尾部定位信号的有效性。

### 失败模式与局限性

1. **OOD数据质量敏感**：COLT的性能高度依赖OOD数据集的语义丰富度。使用高斯噪声或语义过于单一的OOD数据集时增益消失（Fig 3a）。如何系统性地选择和构建最优OOD数据集仍是一个开放问题。

2. **Places-LT上增益有限**：在Places-LT上COLT仅提升约1.6个百分点，远低于CIFAR和ImageNet上的增益。可能原因是场景类图像的语义粒度更细、类间差异更小，OOD样本的桥接效应被削弱。该假设需要进一步实验验证。

3. **缺乏理论分析**：论文仅从经验上证明了OOD样本的有效性，但未给出严格的理论解释——例如，为何与尾部类特征空间邻近的OOD样本能改善表示学习的泛化性，以及OOD样本的最优分布应满足何种条件。

4. **计算开销**：COLT需要定期进行K-means聚类、尾度分数计算和OOD采样，增加了训练过程中的计算开销。论文未详细报告这一额外开销的具体数值。

### 补充图表

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/008_Figure_3.jpg]]
*Figure 3: Analytical experiments of COLT on CIFAR-100-LT. (3a): accuracy when changing the external OOD dataset. (3b): accuracy when sampling different numbers of OOD samples on 300K Random Images. (3c): Top-1 accuracy and standard derivation (Std) of COLT with or without the proposed distribution loss. (3d): accuracy with various sampling intervals r. (3e): A higher ϕtail and a lower $\phi _ { h e a d }$ implies mining tail samples more precisely. (3f): accuracy with various k*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/011_Figure_4.jpg]]
*Figure 4: Normalized Misclassification Matrix (NMM) on the test set of CIFAR-100 with different frameworks and train sets. (4a): SimCLR trained on balanced CIFAR-100. (4b): SimCLR trained on long-tailed CIFAR-100. (4c): implement COLT on top of SimCLR trained on long-tailed CIFAR-100*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/012_Figure.jpg]]
*Figure: (a) SimCLR (majority classes’ mean connectivity: 0.73 minority classes’ mean connectivity: 0.46) (b) SimCLR+COLT (majority classes’ mean connectivity: 0.76 minority classes’ mean connectivity: 0.67)*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/013_Figure_6.jpg]]
*Figure 6: Linear regression results between the minority proportion in a cluster and the cluster’s tailness score on long-tailed CIFAR, ImageNet-100, and Places. We set cluster number C = 10*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/014_Figure_5.jpg]]
*Figure 5: The augmentation graph of CIFAR-10. Similar to (Wang et al., 2021), We choose a random subset of test images and randomly augment them 20 times. Then, we calculate the instance distance in the representation space and draw edges for image pairs whose smallest view distance is below a small threshold. We visualize the samples with t-SNE and denote edges between ID instances in black and edges between ID and OOD samples, forming new connections in red. (a) CIFAR-10-LT*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/001_Figure_1.jpg]]
*Figure 1: (1a): Feature space uniformity of different SSL frameworks. (1b): Visualization of the alignment property of samples in minority classes and majority classes w/ or w/o COLT. The experiment is conducted with ResNet-18 on CIFAR-100-LT*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/003_Table_1.jpg]]
*Table 1: Test accuracy (%) and balancedness (Std↓) on CIFAR-10-LT and CIFAR-100-LT*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/004_Table_2.jpg]]
*Table 2: Test accuracy (%) and balancedness (Std↓) on ImageNet-100-LT and Places-LT*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/006_Table_4.jpg]]
*Table 4: Compare the test accuracy (%) on ImageNet-100-LT of the proposed COLT with MAK which use ID data. The best performance is marked as bold*

![[assets/figures/papers/paper_list_l1501_https_arxiv_org_abs_2306_04934/figures/007_Table_5.jpg]]
*Table 5: Comparison of semi-supervised and self-supervised methods when leveraging OOD data*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

COLT建立在自监督对比学习框架之上，其核心基线为 **SimCLR**，后者通过最大化同一实例不同增强视图之间的互信息来学习表示。在长尾分布下，SimCLR的特征空间呈现严重的不平衡：多数类样本占据主导地位，少数类样本形成稀疏孤立点，导致少数类的线性可分性显著下降（见 Figure 1 的对齐性可视化）。COLT并不修改SimCLR的基础对比损失 $\mathcal{L}_{CL}$，而是通过引入OOD数据和分布感知损失来重新平衡特征空间。

在长尾自监督学习领域，COLT与以下方法形成直接对比：

- **SDCLR**：通过自竞争机制缓解长尾问题，但仅利用ID数据内部的信息。COLT可即插即用地叠加在SDCLR之上，在CIFAR-100-LT上进一步将整体精度从53.99%提升至58.88%（Table 1），说明OOD数据带来的增益与ID内部的自竞争机制是互补的。

- **BCL**：基于记忆效应的长尾对比学习方法，同样仅依赖ID数据。COLT与BCL结合后在CIFAR-100-LT上达到57.98%，相比BCL单独使用（55.61%）提升2.37个百分点（Table 1），验证了OOD数据对不同长尾SSL框架的通用适配性。

- **MAK**：使用外部ID数据进行采样平衡的方法。COLT与MAK的关键区别在于：MAK需要与ID数据同域的额外标注或未标注样本，而COLT仅需廉价的OOD数据。在相同采样池和预算下，COLT在ImageNet-100-LT上以72.22%的整体精度优于随机采样（68.28%）和MAK（69.44%）（Table 3）。更值得注意的是，即使MAK使用完全同域的ID数据进行采样（72.0±0.5%），COLT使用OOD数据仍能达到72.4±0.3%（Table 4），表明精心挑选的OOD样本在特征空间平衡方面可媲美甚至超越同域采样。

### 2. 方法适用边界

COLT的有效性依赖于以下关键条件：

**OOD数据的质量要求**：消融实验（Figure 3a）表明，使用高斯噪声作为OOD数据几乎无增益，而真实图像数据集（300K Random Images、STL-10、ImageNet等）均能带来显著提升。这说明OOD数据必须包含与ID少数类特征空间邻近的、具有语义结构的视觉模式，纯噪声无法充当“桥梁”连接少数类实例。

**OOD数据规模与不平衡度的鲁棒性**：COLT对OOD数据集的规模和不平衡度表现出良好的鲁棒性（Table 10, Table 11）。采样预算增加至10K-15K后增益趋于饱和（Figure 3b），但始终优于随机采样基线。

**采样策略的敏感性**：动态采样间隔 $r$ 对性能有显著影响，$r=25$ 时性能最佳，过大或过小均导致精度下降（Figure 3d）。簇数目 $C$ 在10到100范围内对精度影响不大（Table 9），且无监督K-means聚类接近Oracle（有监督标签）的表现，降低了方法对标注的依赖。

**OOD数据集类型的迁移性**：在不同OOD数据集上的实验（Table 6, Table 7）显示，COLT在ImageNet-100上使用300K Random Images、Places、Open Images等不同OOD源均能获得一致的增益，验证了方法的跨OOD域泛化能力。

### 3. 局限与开放问题

**理论分析缺失**：当前工作仅从经验层面验证了OOD数据对长尾自监督学习的有效性，缺乏严格的理论分析来解释为何OOD样本能有效提升特征空间的均匀性与对齐性。增强图的可视化（Figure 5）直观展示了OOD样本如何作为“桥梁”连接同一少数类的不同实例，但这一机制的定量刻画仍是空白。

**OOD数据选择的最优策略**：对于给定的长尾ID数据集，如何确定最优的OOD数据集（包括类型、规模、分布特性）以获得最大增益，仍是一个开放问题。当前工作通过实验表明真实图像数据集有效，但未提供系统性的OOD数据选择准则。

**OOD与ID的替代关系**：COLT在Table 4中展示了OOD数据可媲美ID数据的效果，但OOD样本能否完全替代ID样本用于长尾学习，以及在何种条件下可以替代，尚未得到充分探索。

**与半监督方法的对比优势**：Table 5显示COLT在利用OOD数据时比半监督方法表现更好，但这一现象的原因尚不明确，可能涉及自监督预训练与半监督学习中OOD数据利用机制的本质差异。

**最低数据需求**：COLT的有效性对OOD数据规模和分布的最低要求是什么？当前实验覆盖了从数千到数十万规模的OOD数据，但未系统探索性能骤降的临界点。

## 原文 PDF

![[paperPDFs/ICLR_2023/On_The_Effectiveness_of_Out_of_Distribution_Data_in_Self_Supervised_Long_Tail_Learning.pdf]]

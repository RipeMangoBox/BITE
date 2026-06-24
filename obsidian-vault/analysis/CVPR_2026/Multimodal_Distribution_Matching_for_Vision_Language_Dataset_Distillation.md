---
title: Multimodal Distribution Matching for Vision-Language Dataset Distillation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multimodal_Distribution_Matching_for_Vision_Language_Dataset_Distillation.pdf
project_link: null
code_link: "https://github.com/kakaobrain/coyo-dataset"
aliases:
- MMDM
- MDMVLDD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过数据层面（K-means联合空间聚类初始化）、模型层面（角度引导的权重空间插值）和损失层面（测地线核能量匹配一致性与差异性方向+对比学习）的三层干预，实现高效、可泛化的分布匹配蒸馏。
primary_logic: 在归一化超球面上，通过测地线高斯核能量直接匹配真实与合成数据在跨模态一致性和差异方向上的分布，配合聚类播种和模型插值，以极低计算代价保留多模态语义并增强跨架构泛化。
claims:
- 在Flickr8k和COCO的多数设置下MDM优于轨迹匹配基线MTT-VL和TESLAwBCE，并接近或超越LoRS。
- 跨架构评估中MDM在所有设置下均显著优于LoRS，表现出强泛化能力。
- MDM比LoRS节省93%至98%的总蒸馏时间，计算效率大幅提升。
- Flickr8k (100 pairs) 上 Mean R@1/5/10 = 21.9
---

# Multimodal Distribution Matching for Vision-Language Dataset Distillation

> [!tip] 核心洞察
> 在归一化超球面上，通过测地线高斯核能量直接匹配真实与合成数据在跨模态一致性和差异方向上的分布，配合聚类播种和模型插值，以极低计算代价保留多模态语义并增强跨架构泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉-语言数据集蒸馏的多模态分布匹配 |
| 英文题名 | Multimodal Distribution Matching for Vision-Language Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jeong_Multimodal_Distribution_Matching_for_Vision-Language_Dataset_Distillation_CVPR_2026_paper.html) · [Code](https://github.com/kakaobrain/coyo-dataset) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MDM (Multimodal Distribution Matching) |
| Dataset | Flickr8k, COCO |

> [!tip] 效果简介
> - Flickr8k (100 pairs) 上，Mean R@1/5/10 21.9 vs 19.4 (LoRS) (+2.5)。
> - COCO (100 pairs) 上，Mean R@1/5/10 10.3 vs 9.4 (LoRS) (+0.9)。
> - Flickr8k (100 pairs, cross-arch) 上，R@Mean (aggregated over R@1/5/10) 13.9 vs 10.3 (LoRS) (+3.6)。

## 概述

视觉-语言数据集蒸馏旨在将大规模图像-文本对压缩为极少量合成样本，同时保持下游多模态任务的性能。现有方法主要依赖**训练轨迹匹配**（如**MTT-VL**，Wu et al., TMLR 2024），需回放完整训练轨迹，计算与存储开销巨大，且对训练架构存在偏倚，跨架构泛化能力薄弱。

针对上述瓶颈，本文提出**多模态分布匹配**（Multimodal Distribution Matching，**MDM**），将数据集蒸馏从轨迹匹配范式转向分布匹配范式。核心思路是在归一化超球面上，通过测地线高斯核能量直接匹配真实数据与合成数据的联合图像-文本分布，从而以极低计算代价实现高效蒸馏。

MDM 在三个层面进行系统性干预：**数据层面**，采用联合嵌入空间的 K-means 聚类初始化合成样本，确保覆盖多模态语义模式并减少冗余；**模型层面**，通过角度引导的权重空间插值融合多个微调专家，构建具有跨架构泛化能力的混合教师模型；**损失层面**，同时优化一致性分布匹配、差异性分布匹配与双向对比学习损失，在保持图文配对的同时对齐全局分布结构。

实验表明，MDM 在 Flickr8k 和 COCO 等标准图文检索基准上，以 100 对合成数据取得 Mean R@1/5/10 分别为 21.9 和 10.3 的结果，优于轨迹匹配基线 MTT-VL 和 TESLAwBCE，并接近或超越同期分布匹配方法 **LoRS**（Xu et al., ICML 2024）。在跨架构评估中，MDM 在所有设置下均显著优于 LoRS（Flickr8k 上聚合 R@Mean 领先 3.6 个百分点），展现出更强的泛化能力。同时，MDM 比 LoRS 节省 93% 至 98% 的总蒸馏时间，计算效率大幅提升。

消融研究进一步验证了三层干预各自的有效性：联合 K-means 聚类初始化、角度引导权重插值、以及一致性-差异性联合损失均对最终性能有显著贡献。

## 背景与动机

### 数据集蒸馏的范式演进

深度学习模型训练长期依赖大规模数据集，但存储、传输和训练成本随数据规模急剧攀升。数据集蒸馏（Dataset Distillation）通过将大型真实数据集压缩为极少量合成样本，使下游模型在合成数据上训练即可逼近原始数据性能，成为缓解数据瓶颈的关键技术。

早期蒸馏方法可归为四类：**性能匹配**（performance matching）直接优化代理模型在合成数据上的精度；**参数匹配**（parameter matching）对齐在真实与合成数据上训练得到的模型参数；**分布匹配**（distribution matching, DM）在特征空间对齐真实与合成数据的嵌入分布；**轨迹匹配**（trajectory matching, MTT）则重放专家模型在真实数据上的训练轨迹来指导合成数据优化。其中，轨迹匹配方法（如MTT）在图像分类数据集蒸馏中取得领先性能，但其依赖昂贵的双层优化——需存储完整的训练轨迹快照并反复重放，计算和存储开销极大。

### 多模态蒸馏的独特瓶颈

当数据集蒸馏从单模态图像分类扩展到多模态视觉-语言检索场景时，面临三个核心挑战：

**第一，模态间语义对齐的脆弱性。** 视觉-语言数据集的核心价值在于图像与文本的细粒度配对关系。现有方法如**MTT-VL**（Wu et al., TMLR 2024）直接将MTT的轨迹匹配框架迁移到多模态，通过重放图像-文本对的训练轨迹来保持配对信息；**TESLAwBCE**（Cui et al., ICML 2023）在轨迹匹配基础上引入双向对比损失。然而，轨迹匹配本身对训练架构存在天然偏差——合成数据在蒸馏时所用的代理模型上表现良好，但切换到不同架构的下游模型时性能急剧退化，跨架构泛化能力成为瓶颈。

**第二，计算效率的不可持续性。** 轨迹匹配需要存储多步训练快照并进行双层优化，蒸馏时间随数据量和模型规模线性增长。这在视觉-语言场景下尤为突出，因为图像和文本编码器往往规模庞大（如NFNet视觉编码器与BERT文本编码器），使得轨迹存储和重放的计算成本难以承受。

**第三，初始化策略的忽视。** 现有方法多采用随机采样或单模态聚类初始化合成数据，忽视了联合嵌入空间中图像-文本对的几何结构。同时，蒸馏过程通常基于单一预训练或微调模型，未能有效利用多个专家模型的互补知识来增强合成数据的泛化性。

### 本文动机与核心思路

针对上述瓶颈，本文提出**多模态分布匹配（Multimodal Distribution Matching, MDM）**框架，从数据、模型和损失三个层面进行系统性干预：

- **数据层面**：在联合图像-文本嵌入空间进行K-means聚类，以聚类代表样本初始化合成数据，为优化提供更优的几何起点。
- **模型层面**：通过角度引导的权重空间插值，融合多个微调专家模型构建混合教师，打破单一架构偏差，增强跨架构泛化。
- **损失层面**：在归一化超球面上，通过测地线高斯核能量直接匹配真实与合成数据的联合分布，同时沿一致性方向（agreement）和差异性方向（discrepancy）施加分布约束，辅以双向InfoNCE保持模态内配对。

与轨迹匹配的双层优化不同，MDM采用单层分布匹配，无需存储和重放训练轨迹，从根本上降低了计算开销。该方法在Flickr8k、Flickr30k和COCO三个多模态检索基准上，以仅相当于LoRS方法2%至7%的蒸馏时间，取得具有竞争力的检索性能，并在跨架构泛化实验中显著超越所有基线方法。

## 核心创新

MDM的核心创新在于将多模态数据集蒸馏从**昂贵的轨迹匹配范式**彻底转向**单层、几何感知的分布匹配范式**，并通过数据、模型、损失三个层面的协同干预，同时解决了计算效率、跨架构泛化与多模态语义保持三大瓶颈。

### 范式转移：从轨迹匹配到分布匹配

现有主流多模态蒸馏方法（如**MTT-VL** (Wu et al., TMLR 2024)）依赖匹配训练轨迹，需要存储和重放完整的专家模型训练路径，导致巨大的计算与存储开销，且对训练架构存在偏差，跨架构泛化能力差。MDM直接匹配真实数据与合成数据在联合嵌入空间中的分布，将双层优化问题转化为单层分布匹配（Fig. 1），从根本上消除了轨迹重放的计算瓶颈——这一范式转移是后续所有效率提升的源头。

### 三层协同干预机制

MDM的每个关键创新槽位（changed slot）都针对一个明确的瓶颈，且三层设计相互增强：

**数据层 — 联合空间聚类初始化**：传统方法采用随机采样或单模态聚类初始化合成数据，忽略了图像-文本对的联合语义结构。MDM在图像和文本编码器的联合嵌入空间中执行K-means聚类，从每个簇中选择最接近质心的真实样本作为合成数据种子。这一“聚类播种”策略使合成数据天然覆盖联合语义空间的主要模式，避免冗余，为后续分布匹配提供了高质量的优化起点。消融实验（Table 4a）证实，联合K-means初始化将平均检索分数从随机初始化的20.6提升至21.9。

**模型层 — 角度引导的权重空间插值**：现有方法通常使用单个微调模型或固定预训练模型作为教师，限制了蒸馏数据的架构泛化能力。MDM提出角度引导的权重空间插值策略：对两个在不同随机种子下微调的专家模型，逐层计算其权重位移向量之间的角度，并据此动态调节合并比例——角度偏差越大，越依赖预训练锚点，以此避免破坏性冲突。这一设计使合成的教师模型兼具多专家知识与预训练稳定性，为合成数据注入了跨架构泛化的“基因”。消融实验（Table 4b）表明，该策略将平均检索分数从简单加权求和的19.6提升至21.9。

**损失层 — 测地线核能量匹配与对比学习**：这是MDM最核心的技术创新。传统分布匹配直接在特征空间上使用欧氏距离，忽视了多模态特征在高维归一化超球面上的几何结构。MDM将图像和文本特征映射到单位超球面，构造两个关键的跨模态方向向量：一致性方向 $u = \text{normalize}(z^v + z^t)$ 和差异性方向 $g = \text{normalize}(z^v - z^t)$。随后，以测地线高斯核能量（GKE）分别匹配真实数据与合成数据在两个方向上的分布，确保合成数据既保留图像-文本的对齐语义，又维持模态间的合理差异。同时，双向InfoNCE损失强制合成图像与文本的正确配对。消融实验（Table 5）证明，三者联合使用达到最高平均检索分数21.94，而单独使用InfoNCE仅有20.98，验证了跨模态分布匹配损失的独立增益。

### 创新协同的因果链

三层创新并非孤立叠加，而是形成了一条清晰的因果链：**聚类播种**提供覆盖全面的初始化，降低了分布匹配的优化难度；**权重插值**构建的泛化教师使匹配目标本身更具迁移性；**测地线核能量匹配**则在正确的几何空间上精确对齐分布。三者共同作用，使得MDM在Flickr8k（100对）上以21.9的平均检索分数超越LoRS的19.4（Table 1），同时在跨架构评估中以13.9对10.3的显著优势碾压LoRS（Table 2），而总蒸馏时间仅为后者的2%–7%（Table 3）。这一“精度-泛化-效率”三重优势的同步实现，正是三层协同干预的直接证据。

## 整体框架

MDM 的整体流程如图2所示，由三个互补的模块级联构成：**数据层面的合成数据初始化**、**模型层面的图像-文本编码器初始化**，以及**损失层面的多模态分布匹配**。与依赖昂贵训练轨迹回放的 MTT 范式（图1左）不同，MDM（图1右）直接在联合嵌入空间中对齐真实与合成数据的分布，将双层优化简化为单层分布匹配，从而大幅降低计算开销。

### 输入输出流

- **输入**：原始多模态数据集 $\mathcal{D}_{\text{real}} = \{(X_i, T_i)\}_{i=1}^{N}$，包含真实图像-文本对；目标合成数据量 $K$；预训练的图像编码器与文本编码器。
- **输出**：合成数据集 $\mathcal{D}_{\text{syn}}^{\star} = \{(\tilde{X}_j, \tilde{T}_j)\}_{j=1}^{K}$，其中 $K \ll N$，合成数据在极低压缩率下保留原始数据的多模态语义与检索性能。

### 模块关系与数据流

1. **合成数据初始化（第3.2节）**  
   首先将全部真实图像-文本对通过冻结的联合编码器映射到共享嵌入空间，在该空间执行 K-means 聚类，从每个簇中选取距离聚类中心最近的样本作为合成数据的初始种子。这一步确保合成数据覆盖联合语义空间的主要模态，避免随机初始化带来的冗余与语义空洞。

2. **图像-文本模型初始化（第3.3节）**  
   在蒸馏开始前，对图像编码器和文本投影模块进行权重空间插值：分别微调两个专家模型，计算其相对预训练锚点的位移向量，再根据位移向量间的角度计算自适应合并比率 $t_{\ell}^{m}$，最终得到融合两个专家知识的混合教师模型 $\theta_{*,\ell}^{m}$。该教师模型为后续分布匹配提供更具泛化能力的特征提取器。

3. **多模态分布匹配损失（第3.4节）**  
   在归一化超球面 $\mathbb{S}^{d-1}$ 上，将真实和合成数据的图像-文本特征分别沿一致性方向 $u = \text{normalize}(z^v + z^t)$ 和差异性方向 $g = \text{normalize}(z^v - z^t)$ 投影，构建跨模态图。通过测地线高斯核能量（GKE）匹配两类图的一致性分布（$\mathcal{L}_{\text{agr}}$）与差异性分布（$\mathcal{L}_{\text{dis}}$），同时辅以双向 InfoNCE 损失（$\mathcal{L}_{\text{InfoNCE}}$）维持合成图像与文本的正确配对关系。总损失为三者的加权组合：
   $$\mathcal{L}_{\text{MDM}} = \mathcal{L}_{\text{InfoNCE}} + \lambda_{\text{agr}} \cdot \mathcal{L}_{\text{agr}} + \lambda_{\text{dis}} \cdot \mathcal{L}_{\text{dis}}$$

4. **优化与收敛**  
   合成数据在梯度反传下直接更新，无需维护专家轨迹或进行元梯度计算。如图4所示，MDM 在极少的迭代次数内即可收敛至优于基线方法的性能水平。

### 与基线方法的本质差异

| 维度 | MTT-VL / TESLAwBCE | LoRS | MDM（本文） |
|------|-------------------|------|------------|
| 优化层级 | 双层（轨迹回放） | 单层（低秩相似度） | 单层（分布匹配） |
| 数据初始化 | 随机采样 | 随机采样 | 联合空间 K-means 聚类 |
| 教师模型 | 单一微调模型 | 单一预训练模型 | 角度引导的权重插值 |
| 匹配目标 | 训练轨迹 | 低秩相似度矩阵 | 超球面测地线核能量 + InfoNCE |
| 跨架构泛化 | 弱（依赖特定架构轨迹） | 中等 | 强（分布匹配对架构不敏感） |

这一三层干预设计——聚类播种保证语义覆盖、权重插值增强架构泛化、测地线核能量匹配保留多模态分布结构——构成了 MDM 以极低计算代价实现高效蒸馏的核心机制。

### 补充图表

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/002_Figure_2.jpg]]
*Figure 2: OverviewofMDMOurMDMmetodcosistsof(i)syntheticdatainitilationusingk-meanscustering(ii)imagetextoel initilzationusigeghsaceitepolatiteapretraddfeuedodelsdultiodalisrutioatingtat minimizes geodesic kernel energy between real and synthetic pairs on the unit hypersphere*

## 核心模块与公式推导

MDM 的核心由三个互补的技术模块构成：数据层面的合成数据初始化、模型层面的教师模型构建，以及损失层面的多模态分布匹配。以下逐一展开其关键机制与公式。

### 多模态分布匹配框架

MDM 将单模态的分布匹配范式扩展到多模态场景，直接在联合图像-文本嵌入空间中最小化真实数据分布与合成数据分布之间的距离：

$$ \mathcal{D}_{\mathrm{syn}}^\star = \arg\min \phi\left( \mathbb{E}_{(X,T)\sim\mathcal{D}_{real}}[\Psi(X,T)],\; \mathbb{E}_{(\tilde{X},\tilde{T})\sim\mathcal{D}_{syn}}[\Psi(\tilde{X},\tilde{T})] \right) $$

其中 $\Psi(\cdot,\cdot)$ 为联合特征提取函数，将图像-文本对映射到共享嵌入空间；$\phi(\cdot,\cdot)$ 为分布距离度量。该框架避免了轨迹匹配方法（如 MTT）所需的双层优化和训练轨迹重放，将问题转化为单层分布匹配，显著降低了计算开销。

### 合成数据初始化：联合空间 K-means 聚类

合成数据的初始质量对蒸馏效果至关重要。MDM 在图像编码器和文本编码器的联合嵌入空间中对真实数据执行 K-means 聚类，然后从每个簇中选取最接近簇中心的样本作为初始合成对：

$$ \mathcal{D}_{\mathrm{syn}}^{(0)} = \{ (x_{j_k}, t_{j_k}) \}_{k=1}^{K},\quad j_k = \arg\max_{n\in\mathcal{C}_k} \frac{f_n^\top c_k}{\|f_n\|_2\|c_k\|_2} $$

其中 $\mathcal{C}_k$ 为第 $k$ 个簇，$c_k$ 为簇中心，$f_n$ 为第 $n$ 个样本的联合嵌入特征。这种聚类播种策略确保合成数据覆盖联合语义空间中的主要模态，同时避免冗余采样。消融实验（Table 4a）证实，联合 K-means 初始化显著优于随机采样和单模态聚类，在 Flickr8k 上将平均检索分数从 20.6 提升至 21.9。

### 教师模型构建：角度引导的权重空间插值

为增强合成数据的跨架构泛化能力，MDM 采用角度引导的权重空间插值构建混合教师模型。给定预训练锚点模型 $\theta_0$ 和两个在不同配置下微调的专家模型，首先计算各层权重位移 $\Delta_{1,\ell}^m = \theta_{1,\ell}^m - \theta_{0,\ell}^m$ 和 $\Delta_{2,\ell}^m = \theta_{2,\ell}^m - \theta_{0,\ell}^m$，然后根据两个位移向量之间的角度自适应确定合并系数：

$$ t_{\ell}^{m} = \frac{2 \langle \Delta_{1,\ell}^{m}, \Delta_{2,\ell}^{m} \rangle}{\|\Delta_{1,\ell}^{m}\|_2 \|\Delta_{2,\ell}^{m}\|_2 + \langle \Delta_{1,\ell}^{m}, \Delta_{2,\ell}^{m} \rangle} $$

最终合并权重为：

$$ \theta_{*,\ell}^m = \theta_{0,\ell}^m + \alpha t_\ell^m \cdot \frac{1}{2}(\Delta_{1,\ell}^m + \Delta_{2,\ell}^m) $$

其中 $\alpha$ 为全局缩放因子。$t_\ell^m$ 的设计机制是：当两个专家位移方向一致时，$t_\ell^m \to 1$，合并权重接近专家均值；当位移方向分歧较大时，$t_\ell^m$ 减小，保留更多预训练锚点信息。这种角度感知插值比简单加权求和更能保持语义一致性，消融实验（Table 4b）显示平均检索分数从 19.6 提升至 21.9。

### 多模态分布匹配损失

MDM 的蒸馏损失在单位超球面 $\mathbb{S}^{d-1}$ 上操作，充分利用归一化特征的几何结构。给定图像特征 $z^v$ 和文本特征 $z^t$，首先构造两个跨模态方向向量：

- **一致性方向** $u = \mathrm{normalize}(z^v + z^t)$：捕捉图像与文本共享的语义信息。
- **差异性方向** $g = \mathrm{normalize}(z^v - z^t)$：保留模态特有的互补信息。

在超球面上，两点之间的测地线距离由角度相似度给出：

$$ \phi(a, b) = \arccos(\langle a, b \rangle) \in [0, \pi] $$

基于此，MDM 定义测地线核能量（Geodesic Kernel Energy, GKE）来匹配真实数据与合成数据在一致性和差异性两个方向上的分布。同时，引入双向 InfoNCE 损失保持合成图像与文本的正确配对：

$$ \mathcal{L}_{\mathrm{InfoNCE}} = \frac{1}{2\tilde{B}} \sum_{j=1}^{\tilde{B}} \left[ -\log\frac{\exp(\tilde{Z}_{jj})}{\sum_k \exp(\tilde{Z}_{jk})} - \log\frac{\exp(\tilde{Z}_{jj})}{\sum_k \exp(\tilde{Z}_{kj})} \right] $$

其中 $\tilde{Z}$ 为合成批次的图像-文本相似度矩阵，$\tilde{B}$ 为合成批次大小。最终蒸馏损失为三者的加权组合：

$$ \mathcal{L}_{\mathrm{MDM}} = \mathcal{L}_{\mathrm{InfoNCE}} + \lambda_{\mathrm{agr}} \cdot \mathcal{L}_{\mathrm{agr}} + \lambda_{\mathrm{dis}} \cdot \mathcal{L}_{\mathrm{dis}} $$

其中 $\mathcal{L}_{\mathrm{agr}}$ 匹配一致性方向上的分布，$\mathcal{L}_{\mathrm{dis}}$ 匹配差异性方向上的分布，$\lambda_{\mathrm{agr}}$ 和 $\lambda_{\mathrm{dis}}$ 为平衡超参数。消融实验（Table 5）表明，三个组件协同作用达到最优性能：完整 MDM 损失的平均检索分数为 21.94，而单独使用 InfoNCE 仅为 20.98，验证了分布匹配项对保留多模态语义的关键贡献。

## 实验与分析

### 主要结果：图像-文本检索性能

Table 1 报告了在 Flickr8k、Flickr30k 和 MS-COCO 三个数据集上，不同合成数据量（100、200、500对）下的图像-文本检索平均分数（R@1/5/10 的均值）。MDM 在绝大多数设置下取得最优或次优结果。

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/003_Table_1.jpg]]
*Table 1: Image-textretrievalresultsfor10o,2Oo,and5OOsyntheticpairsusingtheoreset methodsanddistilationmethod.The condensationratefr{Fcr8,ckrk,ndCC}atassareapproximately{1.7%,3%0.8%},{.3%,0.7%7%,{.% 1.7%,4.4%o}for100,2O0,and5OO pairs.Bestandrunnerupresultsare indicatedinboldfaceand underline,respectively*

**Flickr8k（100对）**：MDM 达到 21.9 的平均检索分数，优于轨迹匹配方法 **MTT-VL**（Wu et al., TMLR 2024）的 17.7 和低秩相似度匹配方法 **LoRS**（Xu et al., ICML 2024）的 19.4，领先 LoRS 达 +2.5 个百分点。在 200 对和 500 对设置下，MDM 分别达到 26.7 和 29.7，持续超越所有蒸馏基线。

**MS-COCO（100对）**：MDM 以 10.3 的平均分数优于 LoRS 的 9.4（+0.9），显著领先于 MTT-VL 的 7.7。随着合成数据量增加至 500 对，MDM 达到 17.7，与 LoRS（17.8）基本持平，但远高于其他方法。

**Flickr30k**：MDM 在所有合成数据量下均取得最优，100 对时达到 26.4，500 对时达到 41.0，相比 LoRS 分别提升 +2.0 和 +1.2。

值得注意的是，核心集方法（Random、Herding、K-Center、Forgetting）在所有设置下均显著弱于蒸馏方法，表明简单的样本选择无法有效保留多模态语义信息。

### 跨架构泛化能力

Table 2 展示了跨架构评估结果，这是衡量蒸馏方法实用价值的关键指标。在源模型（NFNet-F0）上蒸馏后，直接迁移到不同架构（NFNet-F1 至 F6 变体）进行检索评估。

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/005_Table_2.jpg]]
*Table 2: Cross-arcecturegeealatiWeeportteeagdsultserralmetricsicudingI@K={.oteat thsourcemodelresultsotdith‘renotaveraged,ndthestresultsareinoldace.(a)-(c):NFetNF-ResetN-eget*

**核心发现**：MDM 在所有目标架构上均显著优于 LoRS。以 Flickr8k（100对）为例，MDM 跨架构聚合平均分数为 13.9，而 LoRS 仅为 10.3，差距达 +3.6。在 COCO（100对）上，MDM 以 6.8 对 5.4 领先 LoRS。

这一优势源于 MDM 的**角度引导权重空间插值**（Sec 3.3）策略：通过融合多个微调专家的权重位移方向构建混合教师模型，使合成数据在蒸馏过程中接触到更丰富的模型参数空间，从而避免了对单一训练架构的过拟合。相比之下，LoRS 虽在源架构上表现接近，但跨架构时性能退化明显，暴露出其对训练架构的偏向性。

### 计算效率分析

Table 3 统计了不同合成数据量下的总蒸馏时间。MDM 展现出显著的计算效率优势：

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/006_Table_3.jpg]]
*Table 3: Compute statistics for different # of data pairs*

- **100对设置**：MDM 总蒸馏时间约 0.3 小时，LoRS 约 5.0 小时，MTT-VL 约 2.5 小时。MDM 相比 LoRS 节省约 **94%** 的时间。
- **500对设置**：MDM 约 1.8 小时，LoRS 约 28.0 小时，节省约 **93.6%**。

这一效率提升的根本原因在于 MDM 采用**单层分布匹配**优化，直接最小化真实与合成数据的联合特征分布距离，无需像 MTT-VL 那样回放训练轨迹（双层优化），也避免了 LoRS 中低秩矩阵分解的计算开销。Figure 4 进一步显示，MDM 在极少的优化迭代次数内即可收敛至高性能水平。

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/007_Figure_4.jpg]]
*Figure 4: Performance curve across datasets and data pairs.Ours consistently achieves higher performance at remarkably smaller iterations than the baseline [58]*

### 消融研究

#### 数据初始化策略（Table 4a）

在 Flickr8k（100对）设置下，比较了四种合成数据初始化方式：

- **随机采样**：平均检索分数 20.6
- **图像空间 K-means**：20.8
- **文本空间 K-means**：20.9
- **联合空间 K-means（MDM）**：**21.9**

联合嵌入空间的聚类初始化相比随机初始化提升 +1.3，验证了在图像-文本联合语义空间中选取代表性样本的有效性。该策略确保了合成数据覆盖多样的跨模态语义模式，同时避免冗余。

#### 模型初始化策略（Table 4b）

比较了四种教师模型构建方式：

- **预训练固定模型**：19.6
- **简单权重平均**：20.4
- **均匀权重插值**：20.8
- **角度引导插值（MDM）**：**21.9**

角度引导的权重空间插值相比固定预训练模型提升 +2.3，证明了融合多个微调专家知识的重要性。该策略通过计算微调位移向量间的夹角动态调整合并系数（Eq 5），在专家分歧较大时更依赖预训练锚点，避免知识冲突。

#### 损失组件消融（Table 5）

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/009_Table_5.jpg]]
*Table 5: Ablation study on the loss components.We report the average retrieval scores over K={1,5,10}*

在 Flickr8k（100对）上分析各损失项的贡献：

- **仅 InfoNCE**：20.98
- **InfoNCE + L_agr**：21.48
- **InfoNCE + L_dis**：21.52
- **InfoNCE + L_agr + L_dis（MDM）**：**21.94**

单独使用双向 InfoNCE 已能提供较强的配对对齐信号。加入一致性分布匹配损失（L_agr）使真实与合成数据在跨模态一致方向上的分布对齐，带来 +0.50 增益。加入差异性损失（L_dis）进一步匹配差异方向分布，额外贡献 +0.42。三者联合使用时达到最优，验证了测地线核能量匹配在超球面上同时约束一致性和差异性方向的有效性。

### 定性结果

Figure 3 展示了合成数据的定性比较。左侧为 K-means 聚类初始化后的样本，右侧为经过 MDM 蒸馏优化后的合成样本。蒸馏后的图像-文本对在语义一致性和视觉质量上均有明显改善，文本描述更加精准地对应图像内容。

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results of synthesized data. We compare the initial (left)and distilled samples (right)*

### 局限性与讨论

1. **编码器依赖性**：MDM 的性能依赖于预训练图像和文本编码器的质量。当编码器能力不足或缺乏预训练时，联合嵌入空间的语义表征可能不够鲁棒，从而影响聚类初始化和分布匹配的效果（Sec 5）。

2. **合成数据量上限**：虽然 MDM 在 100-500 对的范围内表现优异，但合成数据量进一步增加时的性能饱和行为及计算开销变化仍需进一步探索。

3. **跨领域泛化**：当前实验集中在通用图像-文本检索数据集，MDM 在更专业的垂直领域（如医学影像、遥感）中的表现有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/008_Table_4.jpg]]
*Table 4: Ablations across synthetic data and model initializations. (a) Synthetic Data Initialization*

![[assets/figures/papers/paper_list_l2660_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_Multimodal_Distr/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between prior multimodal dataset distillation based on matching training trajectories (MTT, left) and our Multimodal Distribution Matching (MDM, right).While MTT replays image-text trajectories at high compute and storage cost, MDM directly matches the joint image-text distribution in the joint embedding space,yielding compact synthetic data with strong cross-architecture generalization under much lower distillation cost. The red arrow indicates the direction of gradient backpropagation*

## 方法谱系与知识库定位

### 1. 方法谱系：从轨迹匹配到分布匹配的范式迁移

MDM 的提出直接回应了多模态数据集蒸馏（Multimodal Dataset Distillation, MDD）领域的核心瓶颈：**轨迹匹配方法（MTT）计算代价高昂且存在架构偏差**。理解 MDM 的定位，需要将其置于从单模态到多模态、从双层优化到单层优化的演化脉络中。

**上游继承：单模态分布匹配。** MDM 的损失层面设计继承了单模态数据集蒸馏中分布匹配（Distribution Matching, DM）的核心思想——直接对齐真实数据与合成数据在特征空间中的分布，避免回放训练轨迹。论文将这一范式显式扩展至多模态场景，在联合图像-文本嵌入空间中构造匹配目标（Eq 2），从而绕开了 MTT 所需的双层优化和轨迹存储。

**直接竞争对手：MTT-VL、TESLAwBCE、LoRS。** 在多模态蒸馏赛道中，**MTT-VL**（Wu et al., TMLR 2024）将单模态轨迹匹配迁移至视觉-语言任务，但继承了其高计算开销和架构依赖；**TESLAwBCE**（Cui et al., ICML 2023）和 **LoRS**（Xu et al., ICML 2024）分别从低秩相似度和压缩角度切入，代表了同期工作在效率与性能之间的不同权衡。MDM 与这些方法的根本分歧在于：它放弃了“模拟训练过程”的路径，转而直接建模多模态联合分布。

**技术组件溯源。** MDM 的三个关键模块各有来源：
- **K-means 联合空间聚类初始化**（Sec 3.2）借鉴了核心集选择（coreset selection）中通过聚类覆盖数据流形的思路，但将其从单模态扩展至图像-文本联合嵌入空间，以同时捕获跨模态语义模式。
- **角度引导的权重空间插值**（Sec 3.3）源于模型合并（model merging）领域的几何感知插值技术，论文将其适配为构建混合教师模型的手段，通过位移向量间的角度计算合并比率 $t_\ell^m$，平衡预训练锚点与微调专家的贡献。
- **测地线核能量匹配**（Sec 3.4）是 MDM 最具原创性的设计：在归一化超球面 $\mathbb{S}^{d-1}$ 上，将图像-文本对分解为一致性方向 $u = \text{normalize}(z^v + z^t)$ 和差异性方向 $g = \text{normalize}(z^v - z^t)$，分别用测地线高斯核能量匹配真实与合成数据的分布，同时辅以双向 InfoNCE 保持配对关系。

### 2. 适用边界与条件依赖

MDM 的性能优势存在明确的适用前提，超出这些边界时需要谨慎预期其效果。

**编码器依赖是首要约束。** 论文在 Sec 5 中明确指出，方法依赖预训练的图像编码器（NFNet）和文本编码器（BERT）提取特征。当预训练编码器能力不足或领域不匹配时，联合嵌入空间的质量将直接限制聚类初始化、分布匹配和最终检索性能的上限。这一约束意味着 MDM 在低资源语言、专业领域图像等缺少强预训练模型的场景中可能表现受限。

**数据集规模与压缩比范围。** Table 1 的实验覆盖了 Flickr8k（100/200/500 对，压缩比约 1.7%–8.3%）、Flickr30k（对应约 0.3%–1.7%）和 COCO（对应约 0.8%–4.4%）三个数据集。在极低压缩比（如 0.3%）下，MDM 仍能保持对核心集方法的优势，但论文未探索更极端的设置（如 10 对以下）或更大规模数据集（如千万级图文对），这些场景下的行为需要额外验证。

**架构泛化的已知边界。** Table 2 的跨架构评估在 NFNet 系列变体（NFNet-F0 至 F6）上进行，MDM 在所有设置下均显著优于 LoRS，展现出强泛化能力。但论文未涉及 Transformer 架构的图像编码器（如 ViT）或不同文本编码器的组合，跨架构泛化的完整边界尚待进一步验证。

### 3. 局限与开放问题

**计算效率的结构性优势。** Table 3 显示 MDM 比 LoRS 节省 93% 至 98% 的总蒸馏时间，这一优势来自单层优化对双层优化的结构性替代——无需回放训练轨迹、无需维护专家模型的多步更新。然而，蒸馏后的合成数据在下游微调中的性能是否与全量数据训练的模型一致，论文未提供系统性的下游任务评估。

**合成数据的语义保真度。** Figure 3 的定性结果展示了蒸馏前后样本的变化，但论文未量化合成数据的语义多样性或覆盖度。在极端压缩下，合成数据是否可能坍缩到少数语义模式，是一个值得关注的开放问题。

**损失组件的解耦程度。** Table 5 的消融表明，$\mathcal{L}_{\text{InfoNCE}}$、$\mathcal{L}_{\text{agr}}$ 和 $\mathcal{L}_{\text{dis}}$ 三者联合使用达到最优（平均检索分数 21.94），单独使用 InfoNCE 降至 20.98。但各损失项之间的交互机制（如一致性损失与差异性损失是否存在对抗效应）未被深入分析。

**LLM 使用声明。** 论文在 Sec 5 中声明使用了大型语言模型辅助编辑和格式化，但不干预原创思想。这一声明不影响方法本身的可复现性，但在解读论文写作风格时需加以注意。

## 原文 PDF

![[paperPDFs/CVPR_2026/Multimodal_Distribution_Matching_for_Vision_Language_Dataset_Distillation.pdf]]

---
title: "Accelerating Benchmarking of Functional Connectivity Modeling via Structure-aware Core-set Selection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerating_Benchmarking_of_Functional_Connectivity_Modeling_via_Structure_aware_Core_set_Selection.pdf
project_link: null
code_link: https://github.com/lzhan94swu/SCLCS
aliases:
- SSACLCSS
- ABFCMSACSS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "在保持SPI相对性能排名的前提下，用仅占原数据集10%的高质量核心集替代完整数据集进行评估，即可将计算成本降低一个数量级以上，同时保留排名信息。"
primary_logic: "通过Transformer学习样本特定的FC同步结构，并利用训练过程中的结构扰动评分（SPS）量化结构稳定性，从而筛选出代表基础连接原型的稳定样本；再结合密度平衡采样策略，在稳定样本池中提升低密度区域的采样权重，确保核心集的结构多样性与分布代表性，最终以极小的数据量忠实地保留全套SPI的排名关系。"
claims:
- "在REST-meta-MDD数据集上，仅使用10%的样本，SCLCS在排名一致性（nDCG@k）上比最先进的基线方法高出23.2%，有效保留了完整的SPI排名。"
- "使用naïve多头注意力平均的变体SPS_MHA在所有任务中性能极差，证实了均匀平均会扩大注意力支持集并膨胀熵，破坏结构特异性（定理1）。"
- "密度感知采样（SCLCS_Dense）在MDD诊断任务中表现持续优于纯top-k选择，其nDCG@20在50%采样比下达到89.45，而简单top-k因聚类偏向导致排名失真（定理3）。"
- "修正后的Transformer能够以低MSE逼近16种不同类型的SPI算子（如lcss_constraint的测试MSE=0.002），验证了其通用逼近能力（定理2）。"
---

# Accelerating Benchmarking of Functional Connectivity Modeling via Structure-aware Core-set Selection

> [!tip] 核心洞察
> 通过Transformer学习样本特定的FC同步结构，并利用训练过程中的结构扰动评分（SPS）量化结构稳定性，从而筛选出代表基础连接原型的稳定样本；再结合密度平衡采样策略，在稳定样本池中提升低密度区域的采样权重，确保核心集的结构多样性与分布代表性，最终以极小的数据量忠实地保留全套SPI的排名关系。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过结构感知核心集选择加速功能连接建模基准测试 |
| 英文题名 | Accelerating Benchmarking of Functional Connectivity Modeling via Structure-aware Core-set Selection |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0RYazbfSzW) · [GitHub](https://github.com/lzhan94swu/SCLCS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | SCLCS (Structure-aware Contrastive Learning for Core-set Selection) |
| Dataset | REST-meta-MDD (Brain Fingerprinting & MDD Diagnosis), 计算成本 (266 个 SPI 在 4520 个样本上的完整基准) |

> [!tip] 效果简介
> - REST-meta-MDD (Brain Fingerprinting & MDD Diagnosis) 上，nDCG@k 排名一致性 为 SCLCS / SCLCS_Dense，对比 9 种 SOTA 核心集选择方法 (AUM, CCS, Forgetting 等)，变化 最高提升 23.2%（10% 采样比）；SCLCS 在脑指纹任务 0.1 比率的 nDCG@5 = 81.21，显著高于所有基线。
> - 计算成本 (266 个 SPI 在 4520 个样本上的完整基准) 上，CPU 天 为 SCLCS 核心集 (10%) + 仅对选出的 SPI 进行全量验证，对比 穷举评估 (full dataset + all SPIs)，变化 从 >990 CPU 天降至约 100 CPU 天以内，同时保持排名高度一致。

## 概要

对大规模 fMRI 数据集（如 REST-meta-MDD）上的数百种功能连接（FC）建模候选方法（SPI）进行穷举评估时，模型‑数据配对的组合爆炸使计算开销高达数百 CPU 天，导致系统化的 SPI 基准测试无法成为常规预处理步骤。现有的核心集选择方法聚焦于单个分类模型的精度保持，难以迁移至需要保留整个方法集合相对性能排名的全新任务。

本文提出 **SCLCS**（Structure-aware Contrastive Learning for Core-set Selection），以极少量样本忠实地保留完整 SPI 排名为核心目标，设计了三个关键组件：  
1) **自适应多头注意力编码器**：通过可学习权重融合多个注意力头，为每个样本生成特定的功能连接结构图，作为与任何具体 SPI 解耦的通用结构探针；  
2) **结构扰动评分（SPS）**：量化样本注意力结构在训练过程中的逐轮波动，低 SPS 样本被视为基础连接原型、结构最为稳定；  
3) **结构感知密度平衡采样**：首先剔除高 SPS 的不稳定样本，再在稳定池中利用核密度估计提升低密度区域样本的采样权重，兼顾结构稳健性与分布多样性。  
整个框架采用被试身份的对比损失进行自监督训练，使学习到的嵌入保留个体特异性指纹。

在 REST-meta-MDD 数据集（904 名受试者，4 520 个滑动窗口段）上，SCLCS 仅需 **10%** 的样本，即在脑指纹识别和抑郁症诊断两项 SPI 排名任务中以 **nDCG@k** 指标保留完整排名，且最高优于当前最优基线方法 **23.2%**。同时，完整基准测试的计算成本从 **超过 990 CPU 天** 压缩至 **约 100 CPU 天以内**。消融实验证实，自适应注意力融合、SPS 稳定性度量和密度平衡策略对排名保持均不可或缺。这一工作将核心集选择从传统“保精度”范式拓展至“保排名”范式，为实现大规模 fMRI 连接组学方法的常态化基准评估提供了高效、可扩展的解决方案。

在功能连接（FC）分析中，研究社区往往会提出大量的信号处理与推断（SPI）算子，期望从中选出最优的建模管线。然而，对大规模 fMRI 数据集上数百种候选 SPI 进行穷举评估时，模型–数据配对的组合爆炸导致计算开销急剧膨胀——仅对一组代表性算子集在数千个样本上运行完整基准，耗时即可超过 990 CPU 天。这种极高的计算门槛使系统化的 SPI 基准测试难以成为常规的预处理步骤，研究者通常被迫依赖少量经验选定的算子而非全面比较，从而埋下了次优建模的风险。

从优化视角看，该困境可以形式化为一个排名保持的核心集选择问题：给定一个受试fMRI样本集合 $\mathcal{X}$ 和一个 SPI 池 $\mathcal{S}$，目标是找出一个预算为 $c$ 的子集 $\mathcal{X}_c^*$，使得在该子集上评估 $\mathcal{S}$ 得到的性能排名与在全量数据上得到的排名尽可能一致：
$$
\mathcal{X}_c^* = \argmin_{\mathcal{X}' \subset \mathcal{X}, |\mathcal{X}'| = c} \mathcal{D}\big(\mathrm{Rank}(\mathcal{S}, \mathcal{X}), \mathrm{Rank}(\mathcal{S}, \mathcal{X}')\big).
$$
本质上，我们需要一种能够替代全量数据的“核心样本”集合，它们能够忠实地保留 SPI 之间的相对优劣关系，同时将评估成本降低一个数量级以上。

已有的核心集选择方法（如 Forgetting、Entropy、EL2N、AUM 等）几乎全部围绕单个分类模型的训练动态设计，其评分准则与特定模型的决策边界深度耦合。当面对一组未知的、类型各异的 SPI 时，这些方法无法保证所选子集能够泛化到不同计算原理和复杂度特征的算子上，因此难以支撑可靠的排名保持。此外，纯 top‑k 全局排序选择易在特征空间密集区过度聚集，忽略低密度但具有重要结构信息的样本，进一步加剧了排名失真。

基于上述缺口，本文提出**结构感知对比学习的核心集选择（SCLCS）框架**。其动机源自一个核心观察：通过自适应融合多头注意力的 Transformer 学习样本特定的 FC 同步结构，并以训练过程中结构图的稳定性——即**结构扰动评分（SPS）**——作为与任何特定 SPI 解耦的样本重要性指标，可以识别出代表基础连接原型的稳定样本。进一步，配合密度平衡采样策略，在稳定样本池中提升低密度区域的采样权重，能够在不牺牲排名保持能力的前提下大幅度增强核心集的结构多样性与分布代表性。在 REST‑meta‑MDD 数据集上，仅使用 **10%** 的样本，SCLCS 在排名一致性指标 nDCG@k 上较最强基线提升 **23.2%**，同时将整体基准计算开销从数百 CPU 天降至约 100 CPU 天以内，为大规模功能连接建模的加速自动化评估提供了可行路径。

## 核心方法与创新机理

SCLCS 针对功能连接（FC）建模基准测试中“模型-数据组合爆炸”的瓶颈，提出了三项关键变更，从根本上区别于仅面向单模型分类性能的现有核心集选择方法。这些创新聚焦于**样本重要性评分准则**、**样本表示学习**以及**采样策略**，协同实现了以极少样本保留全量 SPI（相似性处理接口）排名关系的目标。

### 1. 评分准则：从分类动态转向结构扰动度量

现有方法（如 Forgetting, Entropy, EL2N, AUM 等）均基于某个特定分类器在训练过程中的动态信号（遗忘事件、预测熵、误差 L2 范数、分类边际变化）来评估样本“难度”或“不确定性”。这类评分本质上捕获的是样本对单个决策边界的影响，与所关心的 SPI 排名保持目标并不直接匹配。

SCLCS 提出了**结构扰动评分 (Structural Perturbation Score, SPS)**，完全不依赖任何外部分类器，而是利用模型自身学习到的注意力结构在训练过程中的稳定性来判断样本的核心程度。其定义为
$$
\mathrm{SPS}(\mathbf{X}) = \frac{1}{L}\sum_{e=1}^{L} \left\| \mathbf{A}_{(\mathbf{X})}^{(e)} - \mathbf{A}_{(\mathbf{X})}^{(e-1)} \right\|_F^{2},
$$
其中 $\mathbf{A}_{(\mathbf{X})}^{(e)}$ 是第 $e$ 个训练 epoch 时样本 $\mathbf{X}$ 的归一化注意力结构矩阵（即样本特定的 FC 探针）。低 SPS 表示该样本的功能连接模式在训练过程中保持纯净稳定，更接近某个“基础连接原型”；高 SPS 则意味着结构在多个原型间漂移，属于混合或不稳定的样本。该评分与任何具体的 SPI 算子解耦，是一种**通用的结构质量度量**。

理论支持上，定理 1 证明了朴素均匀平均多头注意力会导致熵膨胀而破坏结构特异性，从反面论证了学习融合权重的必要性；定理 2 则以理论保证该自适应 Transformer 能逼近任意的连续 SPI 算子（表 4 给出 16 种 SPI 算子的测试 MSE 最低达 0.002），为 SPS 作为高质量指标奠定了基础。在消融实验中，采用均匀平均注意力的变体 SPS_MHA 在所有任务中排名一致性急剧下降（nDCG<15%），充分验证了准确评估结构稳定性对样本筛选的决定性作用（参见 Section 4.2, Proposition 1, Theorem 2, Table 4）。

### 2. 表示学习：从浅层特征到自适应 Transformer 结构探针

以往核心集选择通常直接在原始 BOLD 时间序列或浅层相关矩阵上操作，未显式建模脑区间的功能交互。SCLCS 设计了一个**自适应多头 Transformer 编码器**，通过可学习的标量权重 $\alpha_h$ 融合多个注意力头，为每个样本生成高度特异的 FC 结构图
$$
\mathbf{A}_{\theta}(\mathbf{X}) = \sum_{h=1}^{H} \alpha_{h}\,\mathrm{softmax}\!\left(\frac{\mathbf{X}\mathbf{W}_h^Q(\mathbf{W}_h^K)^{\top}\mathbf{X}^{\top}}{\tau}\right),\quad \alpha\in\Delta^{H-1}.
$$
这一结构不仅将脑区间的同步模式显式编码为图，还由定理 2 保证了其对广泛 SPI 算子的通用逼近能力，使其成为后续 SPS 评估的理想“探针”。

为了赋予该结构有意义的功能指纹，模型进一步采用**被试身份自监督对比学习**：以同一被试的不同时间窗口作为正样本对，其他被试为负样本，通过对比损失
$$
\mathcal{L}_{\text{contrast}} = \frac{1}{|\mathcal{P}|} \sum_{(i,j)\in\mathcal{P}} -\log\frac{\exp(\mathrm{sim}(\mathbf{z}_i,\mathbf{z}_j)/\tau)}{\sum_{k\in\bar{\mathcal{N}}(i)}\exp(\mathrm{sim}(\mathbf{z}_i,\mathbf{z}_k)/\tau)}
$$
学习可区分个体指纹的图级嵌入。这种纯数据驱动的监督方式完全不依赖任务标签，既保留了结构的个体特异性，又避免了因分类目标带来的选择偏差。实验表明，与直接采用分类标签（如 MDD）监督的基线相比，SCLCS 的核心集在站点和类别分布上均保持更好的平衡性（图 2），且在排名保持上取得显著优势（参见 Section 4.1, 4.4, Theorem 1, Table 2）。

### 3. 采样策略：从全局 Top-K 到稳定性筛选＋密度平衡

常见核心集选择通常根据评分进行全局 Top-K 排序采样，极易造成过度聚集（样本集中在高密度区域）且易受类别倾斜影响（例如，图 2 中 Entropy 方法在低采样比下几乎全选 MDD 患者）。SCLCS 引入**结构感知密度平衡采样**来纠正这一问题：

1. **稳定性筛除**：先丢弃 SPS 最高的 $\beta$ 分位不稳定样本，形成稳定候选池 $\tilde{\mathcal{X}}$，确保入选样本均为基础连接原型的纯正代表。
2. **密度平衡重加权**：在稳定池内，使用高斯核密度估计得到每个样本的局部密度 $\rho(\mathbf{X})$，并以密度的倒数 $w(\mathbf{X})=1/(\rho(\mathbf{X})+\epsilon)$ 作为采样权重，由此对低密度区域进行上加权，显式提升采样多样性（式(14)-(16)）。

该策略在保留低 SPS 稳定性的同时，显著改善了核心集的结构覆盖度和分布代表性（定理 3、4 提供了理论支撑）。最终表现呈现任务依赖性：在 MDD 诊断排名任务中，密度增强的 SCLCS_Dense 取得了更优的排名一致性（nDCG@20 达 89.45），证明多样性校正对复杂临床分类的必要性；而在脑指纹任务中，纯低 SPS 的 Top-k 选择（SCLCS）波动更小且指标更佳，揭示不同下游任务对结构多样性的需求存在差异。换言之，采样策略不再是一成不变的全局排序，而是一个可根据任务特性灵活配置的稳定性‑多样性权衡框架（参见 Section 4.3, Theorem 3, Theorem 4, Table 2/3, Figure 2）。

通过上述三项创新的协同，SCLCS 在 REST‑meta‑MDD 数据集上仅使用 10% 的样本即可保留全套 266 个 SPI 方法的正确排名，其排名一致性（nDCG@k）比最强基线高出 23.2%，并将穷举基准测试的计算成本从超过 990 CPU 天压缩至约 100 CPU 天以内，使功能连接建模的系统化评估首次变得几乎实时可行（参见 ABSTRACT, Appendix H.1）。

![[assets/figures/papers/repair_max_0RYazbfSzW_Functional_Connectivity/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the SCLCS framework for ranking-preserving core-set selection. Contrasting with selection for single-model classification (top left), our task is to preserve the performance ranking of SPIs (top right). Our method (bottom) achieves this using a Transformer to learn structures, our novel SPS metric to ensure stability, and a density-aware strategy to promote diversity*

SCLCS 的整体目标是在保持 SPI 性能排名一致性的前提下，通过选择高信息密度核心集替代完整数据集，将穷举基准测试的计算成本从数百 CPU 天降低一个数量级以上。为此，框架引入一个结构感知的样本评分与选择管道，其核心逻辑链为：**学习样本特有的功能连接结构 → 度量结构在训练中的稳定性 → 利用稳定性和密度多样性构造核心集**，同时通过对比学习为整个过程提供有意义的表示空间。

如 Figure 1 所示，框架与传统面向分类的核心集选择不同——后者依赖单个模型的训练动态（遗忘事件、预测熵等）度量样本价值，而 SCLCS 的评分与任何特定 SPI 解耦，直接捕捉脑区间的同步结构原型。整体管道由四个模块串接：

1. **Attention-based FC Learning（注意力结构学习）**  
   输入为被试的 BOLD 时间序列切片，通过自适应多头 Transformer 编码器为每个样本生成归一化的功能连接结构探针 $\mathbf{A}_{\theta}(\mathbf{X})$。该模块的关键设计是使用可学习的标量权重 $\alpha\in\Delta^{H-1}$ 聚合多个注意力头（公式 (2)），避免了均匀平均导致的熵膨胀与结构特异性丧失（Theorem 1）。修正后的 Transformer 被证明能够以任意精度逼近连续 SPI 算子（Theorem 2，表 Table 4 对 16 种 SPI 的逼近 MSE 可达 0.002），从而赋予了结构探针对 SPI 行为的通用代表性。

2. **Structural Perturbation Score (SPS) 计算**  
   在对比学习的每个训练 epoch，对样本 $\mathbf{X}$ 计算其注意力结构矩阵的逐 epoch 平方 Frobenius 距离之和（公式 (10)），该得分量化了结构在训练过程中的不稳定程度。低 SPS 表示样本的 FC 结构靠近某个基础原型、波动小，高 SPS 则反映样本处于多个原型的混合区。这一度量与 SPI 性能排名之间的经验关联构成了核心集选择的基础：保留低 SPS 样本相当于保留基础连接模式，从而忠实维持不同 SPI 的性能差异。

3. **Structure-aware Density-balanced Sampling（结构感知密度平衡采样）**  
   先根据 SPS 阈值（$Q_{1-\beta}$）剔除最不稳定的样本以形成稳定池 $\tilde{\mathcal{X}}$，然后在池内利用高斯核密度估计计算样本密度，并以其倒数作为采样权重（公式 (14)-(16)）。该策略对低密度区域显式上加权，防止纯 top‑k 选择导致的聚类偏向与分布偏移（Theorem 3, Theorem 4）。最终通过加权无放回抽样得到核心集 $\mathcal{X}_c^*$，在结构稳定性和分布多样性之间取得平衡。

4. **Contrastive Learning（对比学习）**  
   以被试身份为监督信号构造正负样本对：正样本来自同一被试的不同时间窗口，负样本为其他被试。通过对比损失（公式 (17)）驱动模型学习能够区分个体指纹的图级嵌入，使注意力矩阵充分捕获受试特异性的功能连接结构，从而为 SPS 计算提供稳定且可分离的表示空间。

上述模块构成一个端到端的核心集构建流程：输入原始 fMRI 时间序列，经 Transformer 得到注意力结构 → 训练过程中计算 SPS 作为样本重要性评分的替代 → 稳定池筛选 + 密度感知采样输出最终核心集。该核心集随后用于 SPI 的全量基准评估（即仅对核心集计算所有 SPI，再对选出的高性能 SPI 在全量数据上验证），由此将总计算量控制在约 100 CPU 天以内（原穷举评估需 >990 CPU 天），同时以最高 23.2% 的 nDCG@k 优势保留完整排名（Table 2, Table 3）。

SCLCS 通过四个顺序组件实现面向 SPI 排名保持的核心集选择：基于注意力融合的功能连接结构学习、结构扰动评分 (SPS)、结构感知的密度平衡采样，以及对比学习。整个流水线围绕一个根本目标：在给定核心集预算 $c$ 下，使完整数据集 $\mathcal{X}$ 与所选子集 $\mathcal{X}'$ 诱导的 SPI 性能排名差异最小化，即

$$
\mathcal{X}_c^* = \operatorname*{argmin}_{\mathcal{X}'\subset\mathcal{X},\,|\mathcal{X}'|=c} \, \mathcal{D}\big(\mathrm{Rank}(\mathcal{S},\mathcal{X}), \mathrm{Rank}(\mathcal{S},\mathcal{X}')\big).
$$

下面逐个模块展开。

### 1. 注意力融合的 FC 结构学习 (Attention-based FC Learning)

该模块是通用的样本特定同步结构探针。对于输入时间序列 $\mathbf{X}$，Transformer 计算 $H$ 个注意力头，然后通过可学习的标量权重 $\alpha_h$（满足 $\sum_h \alpha_h = 1,\;\alpha_h\ge 0$）自适应融合，得到归一化的功能连接结构矩阵：

$$
\mathbf{A}_{\theta}(\mathbf{X}) := \sum_{h=1}^{H} \alpha_h \,\operatorname{softmax}\!\Bigl(\frac{\mathbf{X}\mathbf{W}_h^Q(\mathbf{W}_h^K)^{\top}\mathbf{X}^{\top}}{\tau}\Bigr),\quad \alpha\in\Delta^{H-1},\;\tau>0.
$$

其中 $\mathbf{W}_h^Q,\mathbf{W}_h^K$ 分别为第 $h$ 个头的查询和键矩阵，$\tau$ 为温度参数。**关键瓶颈**：直接对各头注意力做朴素平均（即 $\alpha_h = 1/H$）会扩大每个头的支持集并膨胀熵（定理 1），导致结构特异性丧失，这一点被消融实验证实——变体 SPS_MHA 在所有任务中表现极差（nDCG < 15%）。**因果机制**：自适应融合赋予了架构通用逼近连续 FC 算子的能力（定理 2），经验上该 Transformer 可以以极低测试 MSE（如 lcss_constraint 的 0.002）逼近 16 种差异显著的 SPI 算子（表 4），这为后续的稳定性和多样性评分提供了可靠的结构表征。

### 2. 结构扰动评分 (Structural Perturbation Score, SPS)

SPS 量化样本在对比学习训练过程中的结构波动，作为样本无关的稳定性度量。对于样本 $\mathbf{X}$，设第 $e$ 轮训练得到的注意力矩阵为 $\mathbf{A}_{(\mathbf{X})}^{(e)}$，则 SPS 定义为跨 $L$ 轮训练的累计平方 Frobenius 距离：

$$
\mathrm{SPS}(\mathbf{X}) = \frac{1}{L}\sum_{e=1}^{L} \big\|\mathbf{A}_{(\mathbf{X})}^{(e)} - \mathbf{A}_{(\mathbf{X})}^{(e-1)}\big\|_F^2.
$$

**因果关系**：若将每个样本视为多个基础连接原型的混合，则 SPS 的期望与原型间距离和各原型的混合权重直接相关（命题 1）。**瓶颈**：高 SPS 表示样本在多个原型之间持续漂移，其结构不纯净；低 SPS 则表示样本稳定附着于某一原型，这些样本构成“基础原型”，其相对性能在不同 SPI 下更为一致，因而更适合作为核心集候选。实验显示低 SPS 样本的注意力图快速收敛，而高 SPS 样本呈现持续波动（图 3），验证了该度量的物理意义。

### 3. 结构感知的密度平衡采样 (Structure-aware Density-balanced Sampling)

该模块解决单纯低 SPS 排序所导致的聚类偏向与分布漂移问题。具体流程为：

1. **不稳定样本剔除**：设定分位阈值 $\beta$，仅保留 SPS 不超过 $Q_{1-\beta}$ 的样本构成稳定池 $\tilde{\mathcal{X}}$。
2. **密度反比权重**：在稳定池中，通过高斯核密度估计 $\rho(\mathbf{X})$ 计算每个样本的局部密度，赋予其采样权重为
   
$$
w(\mathbf{X}) = \frac{1}{\rho(\mathbf{X}) + \epsilon},
$$

   其中 $\epsilon>0$ 防止除零。
3. **加权无放回采样**：以 $w(\mathbf{X})$ 为概率权重抽取核心集，显式提升低密度区域的样本概率，确保核心集的结构多样性与分布代表性。

**证据差异**：在脑指纹任务中，纯低 SPS 的 top‑k 选择 (SCLCS) 方差更小、性能最优；而在 MDD 诊断任务中，密度增强的 SCLCS_Dense 在 50% 采样比下达到 nDCG@20 = 89.45，持续优于所有基线（表 3）。这表明最优采样策略依赖于下游任务的结构特征（定理 3、4）。此外，密度感知采样可迁移至其他基于分数的选择方法，但需谨慎调节密度准则与原始分数的交互，以防意外降低多样性或排名保持能力。

### 4. 对比学习

对比损失以被试身份作为自监督信号，为上述模块提供具有判别性的图级嵌入。对于正样本对（同一被试的不同时间窗口）和负样本（不同被试），损失函数为

$$
\mathcal{L}_{\mathrm{contrast}} = \frac{1}{|\mathcal{P}|}\sum_{(i,j)\in\mathcal{P}} -\log \frac{\exp(\mathrm{sim}(\mathbf{z}_i,\mathbf{z}_j)/\tau)}{\sum_{k\in\bar{\mathcal{N}}(i)} \exp(\mathrm{sim}(\mathbf{z}_i,\mathbf{z}_k)/\tau)},
$$

其中 $\mathbf{z}_i$ 为样本 $i$ 的嵌入向量，$\mathrm{sim}(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为对比温度。**因果角色**：对比学习迫使模型在嵌入空间中保持个体特异性指纹，从而为 SPS 计算提供有意义的注意力结构演化轨迹，并保证结构探针在不同个体间具有可比较的动态范围。整个模型通过 Adam 优化器联合训练，核心集选择本身不引入额外的外部分类器，仅依赖这一自监督目标。

**综合因果链**：自适应融合的 Transformer 作为通用 FC 结构探针 → 对比学习赋予其个体级判别能力 → SPS 区分“纯净/混合”样本 → 密度平衡采样在稳定池中提升低密度区域覆盖率 → 最终以仅 10% 的样本（如 REST‑meta‑MDD 中 452 个样本）高度忠实地保留 266 种 SPI 的排名关系，计算成本从 >990 CPU 天降低至约 100 CPU 天。

## 实验与关键发现

### 主结果：排名保持能力与计算效率

SCLCS 的核心目标是**以极小比例的核心集完整保留 266 个 SPI（功能连接建模候选方法）的性能排名**，从而将穷举式基准测试的计算成本降低一个数量级以上。实验在 REST‑meta‑MDD 数据集的 DMN‑33 ROI 子集上展开，包含 4 520 个被试样本。评估使用 nDCG@k 测量核心集与完整数据集产生的 SPI 排名的偏离程度，k 取 5, 10, 20，采样比率设为 0.1, 0.3, 0.5。比较对象包括 9 种先进的核心集选择基线：Random、k‑Means、Forgetting、Entropy、EL2N、AUM、CCS、EVA 和 BOSS。

在**脑指纹（Brain Fingerprinting）排名**任务中，SCLCS 在最低采样比（0.1）下即取得 nDCG@5 = 81.21（表 2），**比最佳基线提升最高达 23.2%**（ABSTRACT 声明）。当采样比增大时，SCLCS 继续保持领先且方差更小，表明其排名保持的稳健性。

![[assets/figures/papers/repair_max_0RYazbfSzW_Functional_Connectivity/figures/003_Table_2.jpg]]
*Table 2: Performance of different methods on brain fingerprinting ranking task (mean ± std) and nDCG@k is reported as percentage (×100)*

在 **MDD 诊断排名**任务中，SCLCS_Dense（加入密度感知采样的变体）表现尤为突出（表 3）：50% 采样比下 nDCG@20 达到 89.45，且在多个采样比和评估深度上均稳定优于所有基线。SCLCS（纯低 SPS 的 top‑k）在脑指纹任务中更优，而 SCLCS_Dense 在 MDD 诊断任务中更优，说明最优采样策略具有**任务依赖性**（Section 5.2 消融分析）。

![[assets/figures/papers/repair_max_0RYazbfSzW_Functional_Connectivity/figures/004_Table_3.jpg]]
*Table 3: Performance of different methods on MDD diagnosis ranking task ( $\mathrm { m e a n } \pm \mathrm { s t d }$ ) and nDCG@k is reported as percentage (×100)

计算成本方面，完整数据集上穷举评估 266 个 SPI 需超过 **990 CPU 天**；而 SCLCS 仅用 10% 样本选出 SPI 子集后再进行全量验证，总成本降至约 **100 CPU 天以内**，同时保持排名高度一致（Appendix H.1, Figure A1）。这验证了框架能够将 SPI 基准测试从数百 CPU 天压减为常规预处理步骤。

### 消融实验

#### 自适应注意力融合 vs. 均匀平均

移除可学习融合权重、改用 naïve 多头注意力平均的变体 **SPS_MHA 在所有任务中性能极差**（表 2 与表 3，多数设置下 nDCG < 15%）。该结果与定理 1 一致：均匀平均会扩大注意力支持集、膨胀熵，破坏头特异性结构（Section 4.1）。这直接证明了自适应加权融合对于学习紧凑的样本特异 FC 结构是必需的。

#### 密度感知采样 vs. 纯稳定性 top‑k

消融实验对比了 **SCLCS**（仅按 SPS 排序取 top‑k）与 **SCLCS_Dense**（先剔除高 SPS 不稳定样本，再在稳定池中进行核密度反加权采样）。在脑指纹任务中，SCLCS 因结构异构性相对较低而表现更优且方差更小；在 MDD 诊断任务中，SCLCS_Dense 通过显式提升低密度区域的采样权重，缓解了纯 top‑k 选择导致的分布聚集与排名失真（Section 5.2, Theorem 3 论述），实现了最高 nDCG@20 = 89.45（表 3）。这表明**密度校正能够在稳定性评分不足以单独保留全局排序时提供关键的多样性信号**。

#### Transformer 的通用逼近能力

为检验自适应注意力架构对任意连续 FC 算子的表达能力（定理 2），表 4 报告了修正后的 Transformer 对 **16 种不同类型的 SPI 算子**的逼近性能。训练末期的 MSE 普遍很低，测试 MSE 如 `lcss_constraint` 仅为 0.002，表明模型能够精确拟合并泛化到结构差异极大的 SPI，从而支撑 SPS 作为通用结构探针的合理性。

![[assets/figures/papers/repair_max_0RYazbfSzW_Functional_Connectivity/figures/005_Table_4.jpg]]
*Table 4: Empirical validation of Theorem 2. Our modified Transformer approximates a diverse set of SPIs. The model demonstrates effective fitting and generalization*

#### 样本覆盖的公平性分析

图 2 分析了各方法所选核心集在**被试身份（S‑I Balance）与诊断类别（M‑H Balance）**上的分布均衡性（通过 L1 距离衡量）。SCLCS 和 SCLCS_Dense 在站点与 MDD/HC 类别上均保持较低方差，维持了良好的平衡；而某些基线如 Entropy 在低采样比下**极端偏向 MDD 类别**，可能引入严重的选择偏差。该结论说明，SCLCS 在节约计算量的同时并未牺牲代表性。

![[assets/figures/papers/repair_max_0RYazbfSzW_Functional_Connectivity/figures/007_Figure_2.jpg]]
*Figure 2: Sample coverage balance on subjects and MDD/HC of baselines*

### 失败模式与分析局限

尽管 SCLCS 系统性领先，但若干局限在实验与理论层面浮现，构成了该方法的当前失效模式：

1. **均匀平均的灾难性退化**：SPS_MHA 的失败直接验证了，若结构特异性被均摊操作抹除，SPS 将无法区分稳定基础原型，导致排名保持能力的彻底崩溃（表 2、表 3）。因此**避免任何冲刷头特定结构的操作**是实现本方法的前提条件。

2. **纯稳定性 top‑k 在某些任务中的不足**：当数据内在的类别结构（如 MDD 诊断）导致稳定样本天然聚集时，仅依靠低 SPS 选择会引入聚类偏向，使核心集无法覆盖下游任务的多样性需求。此时手动切换到密度感知策略可以获得实质补救，但**缺乏自适应策略选择机制**，增加了调参与先验知识依赖。

3. **任务与数据的泛化缺口**：当前所有实验均基于 REST‑meta‑MDD 的 DMN‑33 ROI 子集，未在其他脑区、其他图谱（如 AAL‑90）、其他临床人群（阿尔茨海默病、ADHD）或多元时间序列模态上进行验证。因此**跨数据集、跨模态的排名保持能力未知**，尚不能宣称通用性。

4. **理论‑经验鸿沟**：SPS 依赖对比学习训练过程中的注意力结构波动，虽经验上与 SPI 排名保持强相关，但**从编码器训练动态到 SPI 排名行为的严格因果关系或信息论桥梁尚未建立**，致使部分高 SPS 样本被丢弃的理论正当性仍不完整。

5. **可视化佐证**：图 3 展示了低 SPS 样本的注意力图在训练早期即快速收敛至稳定模式，而高 SPS 样本的注意力图在 epoch 间持续大幅波动，这一现象定性支持了“低 SPS 对应基础原型、高 SPS 对应混合或边界样本”的直觉，但尚不能转化为可计算的排名保证。

![[assets/figures/papers/repair_max_0RYazbfSzW_Functional_Connectivity/figures/010_Table_5.jpg]]
*Table 5: Table A2: Computational cost for core-set selection methods*

## 定位与知识库关联

SCLCS 瞄准的核心任务——在功能连接建模（FC）基准测试中保持全局的 SPI（功能连接计算算子）性能排名——与传统核心集选择方法所解决的问题有根本性差异。现有基线（包括 Random、k‑Means、Forgetting、Entropy、EL2N、AUM、CCS、EVA、BOSS 等）几乎全部源于面向单一分类模型训练的样本筛选框架，其评分机制（遗忘事件数、预测熵、早期误差 L2 范数、分类边际动态等）反映的是样本在特定分类边界上的信息量或难度，而非样本在多算子排名保持中的结构性价值（V/A analysis, “changed_slots” 第一条）。这一出发点决定了它们无法天然适配以“维持尽量多 SPI 的相对优劣顺序”为目标的评估加速场景：SCLCS 被置于一个与这些方法并列但任务定义不同的位置，它在谱系中属于**面向模型排名保持的结构感知核心集选择**，是此项任务的首个系统性解决方案。

SCLCS 与基线之间的关系可通过三个关键设计槽点具体刻画。

1. **样本重要性准则：从分类边界动态到结构扰动评分（SPS）**。所有基于训练动态的基线都假定存在一个特定的分类目标，并用该目标下的预测波动或遗忘来赋分。对于数百种 SPI 的基准评估，不存在唯一的分类目标；因此，SCLCS 借助自监督对比学习得到一个与任何具体 SPI 解耦的通用结构探针，并定义了 SPS——衡量样本在 Transformer 训练过程中学习到的注意力结构矩阵的逐轮弗罗贝尼乌斯平方波动 `SPS(X) = (1/L) ∑_{e=1}^L ‖A_{(X)}^{(e)} - A_{(X)}^{(e-1)}‖_F^2`（Eq. 10）。低 SPS 样本结构收敛迅速，代表了稳定的基础连接原型；相比之下，Forgetting、Entropy 等方法完全依赖分类误差流形，容易在无监督的多 SPI 排名场景中失效（V/A analysis, “decisive_evidence” 第三条；Table 2、Table 3 中 SPS_MHA 及多数基线在采样比 0.1 时 nDCG 极低）。

2. **样本表示学习：从原始时间序列到自适应融合的多头注意力结构图**。基线方法通常直接使用 BOLD 时间序列或浅层特征，忽略脑区之间的交互建模。SCLCS 采用可学习融合权重 `α ∈ Δ^{H−1}` 聚合多头注意力 `A_θ(X) = Σ_{h=1}^H α_h softmax( X W_h^Q (W_h^K)^⊤ X^⊤ / τ )`（Eq. 2），并证明统一平均会膨胀熵、破坏头特异性（Theorem 1），而可学习融合赋予架构对连续 FC 算子的通用逼近能力（Theorem 2，实证验证见 Table 4）。这一设计使表示本身蕴含了样本的同步结构指纹，为 SPS 和后续密度感知采样提供了几何空间。

3. **采样策略：从全局 top‑k 排序到稳定池内的密度平衡采样**。传统方法直接依赖评分对全数据集排序取前 k 个，易造成严重的分布聚集和标签/站点偏差（例如 Entropy 在低采样比下几乎全选 MDD 被试；见 Figure 2 和 fairness_notes）。SCLCS 首先以 β 分位数剔除高 SPS 的不稳定样本，然后在稳定池 `X̃` 内通过高斯核密度估计的反向权重 `w(X) = 1/(ρ(X) + ϵ)`（Eq. 14‑16）进行有放回的加权采样，主动提升低密度区域样本的出现概率。这一策略在理论上可提高核心集对整体结构分布的代表性（Theorem 3、Theorem 4），在 MDD 诊断排序任务中将 nDCG@20 推至 89.45（50% 采样比），而纯低 SPS 的 top‑k 选择在脑指纹任务中波动更小但边际收益不同，揭示了策略‑任务之间的互相作用（V/A analysis, ablations）。

因此，SCLCS 并非对已有核心集选择方法的简单改进，而是通过重新定义对象（由单一分类模型转为 SPI 组）、引入结构稳定性探针、和嵌入密度差异的采样机制，在谱系中开辟了一条新的设计路径。这些组件之间形成因果链：通用结构学习（Theorem 2）→ SPS 捕捉原型纯度（Theorem 1+Perturbation 分析）→ 稳定池剔除非原型噪声 → 密度采样校正聚集偏倚 → 最终排名保持性能的显著提升（nDCG@k 最高领先基线 23.2%，见 ABSTRACT 和 Table 2/3），同时将计算成本从 990+ CPU 天削减至 100 CPU 天以内（Appendix H.1）。

### 适用边界

SCLCS 的适用性受以下几个关键条件约束。

- **任务必须具有“多候选算子的评估集”**：当只关心单一模型的性能而非一组方法的相对优劣时，传统分类导向的核心集方法可能更直接且成本更低。SCLCS 的优势仅在需要系统比较数十甚至数百个 SPI（或更一般地，大量数据处理管道）的排名时才能充分体现。
- **数据结构必须存在可学习的个体级同步结构**：该方法依赖 fMRI 的脑区时间序列和个体身份的对比学习；对于非时间序列或缺乏个体重复观测的模态，结构学习模块可能需重新设计。
- **最佳采样策略具有任务依赖性**：在脑指纹（身份识别）排序任务中，纯 SPS 驱动的低方差选择更优（SCLCS 在 0.1 比率的 nDCG@5=81.21 且方差较低），而 MDD 诊断排序任务则需要密度增强采样来提升 top‑20 的排名保持（SCLCS_Dense 的 nDCG@20=89.45）。这种差异暗示采样策略的选择并非一成不变，需要根据下游任务的结构多样性需求进行调节，目前尚缺自动化选择机制。
- **样本规模与异构性**：当前验证均在 REST-meta-MDD 的 DMN-33 ROI 约 4500 样本上完成；对于更小数据集或极高维的全脑图谱（如 AAL-90），采样比、密度估计带宽和 SPS 阈值可能需要重新校准，且结构学习稳定性可能受制于对比学习的批尺度。

### 局限与挑战

1. **理论桥梁不完整**：SPS 的稳定性高低与各类 SPI 排名保持之间的因果或信息论关系尚未严格建立，目前的证据停留在经验关联层面。这使得无法从理论高度预测在何种 SPI 属性（如线性/非线性、计算复杂度）下选择策略会失效。
2. **手动的采样策略切换**：纯稳定 top‑k 与密度平衡版本的最优性随任务变化，但无自动化判别机制，增加了面向新任务时的调参和试错负担。
3. **泛化性待验证**：实验仅限 REST-meta-MDD 的一个子集（7 站点，DMN-33 ROI）。在其它脑图谱、神经精神疾病（如阿尔茨海默病）、以及多模态时间序列（如同时采集的 EEG+fMRI）上的表现仍属未知，特别是站点异质性和信号特性变化可能扰乱 SPS 的稳定性评估。
4. **异质扫描类型兼容性**：如果数据集中混有静息态和任务态 fMRI，个体身份的一致性假设被打破，同一个体的功能状态差异会导致 SPS 噪声升高，框架直接失效。如何将结构稳定性概念泛化到跨状态可比较的表示空间是一个待解的开放难题。

### 开放问题

- 能否通过扩展 SPS 的数学定义或引入信息论工具，严格推导 SPS 与任意 SPI 排名偏差的上界，从而为实践提供可保证的筛选阈值？
- 元学习或启发式方法是否可以根据数据集的描述符（如类别平衡度、站点分布、SPI 候选数量）自动选择纯 SPS 或密度感知策略，以及自动设定 β 和密度带宽？
- 在全脑图谱或高维 ROI 上，结构学习模块的计算成本和排名保持的采样比之间的帕累托前沿形态如何？核心集规模与 SPI 数量之间是否存在缩放定律？
- 不同类别的 SPI 算子（例如基于相关、偏相关、动态因果模型等）对结构扰动评分的敏感性差异是否可以提前表征，以设计针对性的选择器？
- 密度加权与其他评分方法（如 Forgetting、AUM 等）结合时的交互规律——在什么条件下可产生正迁移，什么条件下会破坏原有评分的信息结构？这一规律对于将密度机制泛化为通用后处理模块至关重要。
- 当数据包含多种扫描协议或条件（静息、任务）时，如何构建可以跨状态对齐的结构探针，使框架同时适用于更加符合实际的基准测试设置？

## 原文 PDF

![[paperPDFs/ICLR_2026/Accelerating_Benchmarking_of_Functional_Connectivity_Modeling_via_Structure_aware_Core_set_Selection.pdf]]

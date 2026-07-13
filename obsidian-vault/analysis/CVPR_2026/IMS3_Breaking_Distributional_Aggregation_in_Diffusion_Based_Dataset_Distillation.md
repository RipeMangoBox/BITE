---
title: "IMS3: Breaking Distributional Aggregation in Diffusion-Based Dataset Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IMS3_Breaking_Distributional_Aggregation_in_Diffusion_Based_Dataset_Distillation.pdf
project_link: null
code_link: null
aliases:
- IIMSSS
- IMS3
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: DDIM反演过程的内在数值不稳定性使反演轨迹偏离高密度区域并漂移到低密度区域，这一现象可被主动利用来扩大分布覆盖。
primary_logic: 利用扩散反演的不稳定性作为正面引导信号，通过时间对齐的潜在匹配（Inversion-Matching）将模型推向低密度区域，并结合质心驱动的选择性子组采样（S³）提升类间可分离性，从而同时解决分布覆盖不足和判别多样性弱的问题。
claims:
- t-SNE 可视化表明，ImS³ 生成的特征分布比 DiT 和 Minimax 更广泛地覆盖原始数据特征空间，说明分布覆盖显著改善。
- 在 ImageWoof 基准上，ImS³ 在多种 IPC 和骨干网络设置下均取得最高准确率，例如 IPC=10 ResNetAP-10 达到 41.8%，超过 Minimax (35.7%) 和 DDVLCP (39.5%)。
- 消融实验证明，同时使用 IM 微调和 S³ 采样比单独使用任一模块带来更大幅度的性能提升，验证了两个互补策略的必要性。
- 1−σ 余弦相似度损失在 IM 微调中优于 L1 和 L2 损失，表明分布感知的对齐方式更有利于反转对齐。
---

# IMS3: Breaking Distributional Aggregation in Diffusion-Based Dataset Distillation

> [!tip] 核心洞察
> 利用扩散反演的不稳定性作为正面引导信号，通过时间对齐的潜在匹配（Inversion-Matching）将模型推向低密度区域，并结合质心驱动的选择性子组采样（S³）提升类间可分离性，从而同时解决分布覆盖不足和判别多样性弱的问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | IMS3：打破扩散数据集蒸馏中的分布聚合 |
| 英文题名 | IMS3: Breaking Distributional Aggregation in Diffusion-Based Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13960) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ImS³ (Inversion-Matching + Selective Subgroup Sampling) |
| Dataset | ImageWoof, ImageNet-1K |

> [!tip] 效果简介
> - ImageWoof 上，Top-1 Accuracy (IPC=10, ResNetAP-10) 41.8±0.3 vs 35.7±0.3 (Minimax) (+6.1)；Top-1 Accuracy (IPC=20, ResNetAP-10) 45.8±1.2 vs 43.3±0.3 (Minimax) (+2.5)；Top-1 Accuracy (IPC=50, ResNet-18) 60.1±1.1 vs 53.9±0.6 (Minimax) (+6.2)。
> - ImageNet-1K 上，Top-1 Accuracy (IPC=10) 45.6±0.3 vs 44.3±0.5 (Minimax) / 45.5±0.1 (MGD3) (+1.3 / +0.1)。

## 概要

### 问题背景

扩散模型已成为数据集蒸馏（Dataset Distillation）的核心生成范式，其目标是将大规模真实数据集压缩为极少量高信息密度的合成样本，使下游模型在合成数据上训练后仍能保持竞争力。然而，扩散模型的内在生成特性使其天然倾向于数据分布的高密度区域，导致合成数据集在决策边界等低密度区域覆盖严重不足——这一现象被称为**分布聚合（distributional aggregation）**。分布聚合直接损害蒸馏数据的判别质量：合成样本缺乏对类间模糊区域的覆盖，下游分类器难以学习到清晰的决策边界。

### 核心洞察

本工作发现，DDIM 反演过程存在内在的数值不稳定性，这一不稳定性使反演轨迹自发偏离高密度区域并漂移至低密度区域。**IMS3 的核心思想是将这一通常被视为缺陷的不稳定性，转化为主动扩大分布覆盖的正向引导信号**。具体而言，通过时间对齐的潜在匹配（Inversion-Matching），将扩散模型的去噪轨迹拉向反演轨迹所覆盖的低密度区域；同时引入质心驱动的选择性子组采样（S³），在采样阶段提升类间可分离性，从而同时解决分布覆盖不足和判别多样性弱这两个相互纠缠的瓶颈。

### 方法定位

IMS3 由两个互补模块构成：

- **Inversion-Matching（IM）微调**：在预训练 DiT-XL/2 上通过 Difffit 进行参数高效微调，以 $1 - \sigma(\mathbf{z}_t^{\mathrm{inv}}, \mathbf{z}_t)$ 余弦相似度损失对齐去噪潜在与反演潜在，总损失 $\mathcal{L} = \mathcal{L}_{\mathrm{Diff}} + \lambda_{\mathrm{IM}} \mathcal{L}_{\mathrm{IM}}$（$\lambda_{\mathrm{IM}} = 0.002$）。IM 在保持高密度区域生成保真度的同时，将模型推向低密度区域，扩大整体分布覆盖。

- **Selective Subgroup Sampling（S³）**：在采样阶段为每类生成 $G$ 个候选子组，利用冻结的 ResNet-18 特征提取器计算子组质心与真实类质心的接近度以及与其他类质心的分离度，通过训练免费的 $\mathcal{L}_{\mathrm{S}^3}$ 目标函数进行贪婪搜索，选择每类最优子组构建蒸馏数据集。S³ 无需额外训练，仅通过推理时的子组筛选即可提升判别多样性。

与现有扩散蒸馏方法相比，IMS3 的核心差异在于：**首次将反演不稳定性作为主动引导机制用于分布扩展，而非仅依赖标准扩散损失或极小极大准则**；同时通过 S³ 在特征空间显式建模类间可分离性，弥补了独立类采样策略在判别性上的不足。

### 主要结果

在 ImageWoof 基准上，IMS3 在多种 IPC 和骨干网络设置下均取得最高准确率：

- **IPC=10, ResNetAP-10**：IMS3 达到 **41.8%**，较 Minimax Diffusion（35.7%）提升 +6.1 个百分点，较 DDVLCP（39.5%）提升 +2.3 个百分点。
- **IPC=20, ResNetAP-10**：IMS3 达到 **45.8%**，较 Minimax（43.3%）提升 +2.5 个百分点。
- **IPC=50, ResNet-18**：IMS3 达到 **60.1%**，较 Minimax（53.9%）提升 +6.2 个百分点。

在更大规模的 ImageNet-1K（IPC=10）上，IMS3 同样取得 **45.6%** 的竞争性结果。t-SNE 可视化（Figure 1）直观证实，IMS3 生成的合成数据在特征空间中覆盖了比 DiT 和 Minimax 更广泛的原始数据分布区域，且类内聚类更紧凑、类间分离更清晰。

消融实验证明，IM 微调与 S³ 采样的组合带来显著增益：单独使用 IM 为 38.7%，单独使用 S³ 为 37.4%，而两者结合达到 41.8%，验证了两个互补策略的必要性。1−σ 余弦相似度损失在 IM 微调中显著优于 L1 和 L2 损失，表明分布感知的对齐方式对反演对齐至关重要。



### 数据集蒸馏的范式与瓶颈

数据集蒸馏（Dataset Distillation）旨在将大规模原始数据集 $\mathcal{D}_r$ 压缩为极小规模的合成数据集 $\mathcal{D}_s$（$M \ll N$），使得在 $\mathcal{D}_s$ 上训练的模型能够逼近在原始数据上的性能。近年来，基于扩散模型（diffusion models）的蒸馏方法凭借强大的生成先验，在合成数据的视觉质量和信息丰富度上取得了显著进展，成为该领域的主流范式。

然而，扩散模型存在一个固有特性：其生成过程天然倾向于数据分布的高密度区域（high-density regions）。这一倾向在数据集蒸馏场景中引发了一个关键问题——**分布聚合（distributional aggregation）**：合成数据集过度集中于高密度区域，而在决策边界等**低密度区域**（low-density regions）的覆盖严重不足。低密度区域往往携带关键的判别信息，其缺失直接损害了蒸馏数据的判别质量，导致下游分类模型的性能受限。

### 现有方法的缺口

当前基于扩散的蒸馏方法主要沿两条路径展开：一类方法直接利用预训练扩散模型生成数据后筛选，如 **DiT** 仅依赖标准扩散损失 $\mathcal{L}_{\mathrm{Diff}} = \|\epsilon_\theta(\mathbf{z}_t, c) - \epsilon\|_2^2$ 进行无条件或条件生成，未对分布覆盖做任何针对性优化；另一类方法通过微调扩散模型来提升合成质量，例如 **Minimax Diffusion** 采用极小极大准则微调模型，**DDVLCP** 引入视觉-语言联合约束，**D³HR** 结合域映射和组采样。但这些方法的微调目标仍以保真度或全局分布匹配为主，未能有效驱动模型主动探索低密度区域。此外，在采样阶段，现有方法通常对每类独立采样，不考虑类间的判别关系，导致合成数据在特征空间中缺乏足够的类间可分离性。

### 核心动机：利用反演不稳定性作为正面信号

本文的关键洞察在于：**DDIM 反演（DDIM inversion）过程存在内在的数值不稳定性**。具体而言，DDIM 反演将真实图像映射为逐时间步的噪声潜在序列 $\mathbf{z}_t^{\mathrm{inv}}$，但 Euler 近似引入的累积误差使得反演轨迹天然偏离高密度区域，向低密度区域漂移。这一现象在传统生成任务中被视为需要克服的缺陷，但本文首次将其**重新定位为可利用的正面引导信号**——通过主动对齐去噪潜在与反演潜在，可以引导扩散模型扩展其分布覆盖范围，从而缓解分布聚合问题。

基于这一动机，本文提出 **ImS³（Inversion-Matching + Selective Subgroup Sampling）** 框架，通过两个互补策略同时解决分布覆盖不足和判别多样性弱的问题：**Inversion-Matching（IM）微调**利用反演不稳定性将模型推向低密度区域，**Selective Subgroup Sampling（S³）** 则在采样阶段通过质心驱动的子组选择提升类间可分离性。



## 核心方法与创新机理

### 问题本质：扩散蒸馏中的“分布聚合”瓶颈

扩散模型因最大似然训练的特性，天然倾向于生成高概率密度区域的样本，导致合成数据集在决策边界等低密度区域覆盖严重不足。这一现象被称为**分布聚合（distributional aggregation）**，直接损害了蒸馏数据的判别质量——分类器在缺乏边界样本的情况下难以学习到紧致的决策边界。t-SNE 可视化（Figure 1）直观地揭示了这一问题：DiT 和 Minimax 生成的样本特征分布明显收缩于原始数据分布的中心区域，而边缘和类间过渡带几乎未被覆盖。

### 核心洞察：将反演不稳定性转化为分布扩展的正向信号

本工作的关键洞察在于对 DDIM 反演过程性质的重新审视。DDIM 反演旨在将真实图像映射回扩散模型的噪声潜在空间，但其内在的**数值不稳定性**使得反演轨迹天然地偏离高密度区域，漂移到低密度甚至离群区域。传统方法通常视此为需要抑制的缺陷，而 ImS³ 首次将其**主动利用为分布覆盖的引导信号**：通过强制扩散模型的去噪轨迹与反演轨迹在对应时间步上对齐，模型被推向那些原本难以覆盖的低密度区域，从而实现分布边界的系统性扩展。

### 两大核心机制：IM 微调与 S³ 采样

基于上述洞察，ImS³ 由两个互补的创新模块构成，分别解决“覆盖不足”和“判别性弱”两个子问题。

**Inversion-Matching (IM) 微调** 是参数高效的扩散模型微调策略。其核心操作是在每个时间步上，将扩散去噪过程中采样的噪声潜在 $\mathbf{z}_t$ 与 DDIM 反演得到的反演潜在 $\mathbf{z}_t^{\mathrm{inv}}$ 进行对齐，损失函数采用分布感知的余弦相似度形式：

$$\mathcal{L}_{\mathrm{IM}} = 1 - \sigma(\mathbf{z}_t^{\mathrm{inv}}, \mathbf{z}_t)$$

该损失与标准扩散损失 $\mathcal{L}_{\mathrm{Diff}} = \|\epsilon_{\theta}(\mathbf{z}_t, c) - \epsilon\|_2^2$ 联合优化（$\lambda_{\mathrm{IM}}=0.002$），在保持高密度区域生成保真度的同时，将模型分布向外推展。为降低计算开销，IM 采用 Difffit 进行参数高效微调，仅在注意力/MLP 块中插入轻量级适配器，冻结扩散主干网络。

**Selective Subgroup Sampling (S³)** 是训练无关的采样阶段策略，旨在提升合成数据的类间可分离性。其流程为：为每类生成 $G$ 个候选子组，利用冻结的 ResNet-18 特征提取器计算每个子组的归一化质心 $\mathbf{c}_{i,g_i}$，并与真实类质心 $\mathbf{r}_i$ 进行比较。S³ 通过最小化如下目标函数进行贪婪搜索，为每类选出最优子组：

$$\mathcal{L}_{\mathrm{S}^3}(\mathbf{g}) = \alpha \sum_{i=1}^{C} \log(1 - \sigma(\mathbf{c}_{i,g_i}, \mathbf{r}_i)) - \frac{\beta}{(C-1)G} \sum_{i=1}^{C} \sum_{j=1}^{C} \sum_{g=1}^{G} \log(1 - \sigma(\mathbf{c}_{i,g_i}, \mathbf{c}_{j,g}))$$

第一项鼓励子组质心靠近真实质心（代表性），第二项推动不同类子组质心彼此远离（判别性），超参数 $\alpha$ 和 $\beta$ 控制二者的权衡。

### 关键设计选择与消融验证

消融实验（Table 4）证实了 IM 与 S³ 的互补性：在 ImageWoof IPC=10 设置下，单独使用 IM 为 38.7%，单独使用 S³ 为 37.4%，二者结合达到 41.8%，较 DiT 基线（34.2%）提升 7.6 个百分点。损失函数消融（Table 7）进一步表明，$1-\sigma$ 余弦相似度损失优于 L1（38.7%）和 L2（39.0%），验证了分布感知对齐的有效性。超参数分析（Figure 3）显示平衡的 $\alpha$ 和 $\beta$ 取值取得最优性能，印证了代表性与判别性之间的内在权衡。



ImS³ 的整体流程由两个互补阶段构成，分别解决扩散数据集蒸馏中的分布覆盖不足与判别多样性弱这两个核心瓶颈。如图 Figure 2 所示，第一阶段**Inversion‑Matching (IM) 微调**对预训练扩散模型进行参数高效微调，利用 DDIM 反演的不稳定性将生成分布推向低密度区域；第二阶段**Selective Subgroup Sampling (S³)** 在采样阶段以训练自由的方式从候选子组中筛选出兼具代表性与类间可分离性的合成样本，构建最终蒸馏数据集。

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed*

### 阶段一：Inversion‑Matching (IM) 微调

该阶段的目标是扩展预训练扩散模型的生成分布覆盖，尤其改善决策边界等低密度区域的合成质量。其核心洞察在于：DDIM 反演过程存在固有的数值不稳定性，使反演轨迹天然地从高密度区域漂移到低密度区域。IM 微调主动利用这一特性作为正向引导信号。

具体而言，对于每张真实图像，首先通过 DDIM 反演（Euler 近似，Eq. (3)）计算其逐时间步的反演噪声潜在 $\mathbf{z}_t^{\mathrm{inv}}$。同时，从初始潜在 $\mathbf{z}_0$ 直接采样对应时间步的噪声潜在 $\mathbf{z}_t$（Eq. (4)）。微调时，在标准扩散损失 $\mathcal{L}_{\mathrm{Diff}}$（Eq. (6)）的基础上，引入 Inversion‑Matching 损失：

$$\mathcal{L}_{\mathrm{IM}} = 1 - \sigma(\mathbf{z}_t^{\mathrm{inv}}, \mathbf{z}_t)$$

该损失以 $1-\sigma$ 余弦相似度的形式，显式地对齐去噪潜在与反演潜在，将模型推向反演轨迹所覆盖的低密度区域。总微调损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{Diff}} + \lambda_{\mathrm{IM}} \mathcal{L}_{\mathrm{IM}}$（Eq. (7)），其中 $\lambda_{\mathrm{IM}}=0.002$ 平衡保真度与覆盖扩展。

为控制计算开销，IM 微调采用参数高效微调策略（通过 **Difffit** 在注意力/MLP 块中插入轻量级适配器），仅更新这些适配器参数而冻结扩散主干网络。微调过程仅需 8 个 epoch，显著降低了可训练参数量和训练成本。Algorithm 1 给出了该阶段的完整伪代码。

### 阶段二：Selective Subgroup Sampling (S³)

微调后的扩散模型具备了更广的分布覆盖，但逐类独立采样仍可能产生判别性不足的样本。S³ 阶段在采样时引入类间关系感知的子组选择机制，以训练自由的方式提升蒸馏数据集的判别多样性。

其工作流程为：
1. **候选子组生成**：对每个类别 $i$，从微调后的扩散模型中采样 $G$ 个候选子组 $S_{i,1}, \dots, S_{i,G}$，每个子组包含 $K$ 张合成图像。
2. **特征提取与质心计算**：使用冻结的轻量级特征提取器 $\phi$（默认 ResNet‑18）将所有候选图像映射到归一化嵌入空间，计算每个子组的质心 $\mathbf{c}_{i,g_i}$（Eq. (9)），同时利用少量真实样本计算各类的真实类质心 $\mathbf{r}_i$（Eq. (8)）。
3. **子组选择优化**：定义 S³ 损失函数（Eq. (10)）：

$$\mathcal{L}_{\mathrm{S}^3}(\mathbf{g}) = \alpha \sum_{i=1}^{C} \log(1 - \sigma(\mathbf{c}_{i,g_i}, \mathbf{r}_i)) - \frac{\beta}{(C-1)G} \sum_{i=1}^{C} \sum_{j=1}^{C} \sum_{g=1}^{G} \log(1 - \sigma(\mathbf{c}_{i,g_i}, \mathbf{c}_{j,g}))$$

其中第一项鼓励所选子组质心靠近真实类质心（保证代表性），第二项推动不同类子组质心彼此远离（增强判别性），$\alpha$ 和 $\beta$ 平衡两者的权重。通过贪婪搜索最小化该损失，得到每类最优子组索引 $\mathbf{g}^*$（Eq. (11)），最终构建蒸馏数据集。Algorithm 2 给出了该阶段的完整伪代码。

### 模块关系与数据流

两个阶段在逻辑上串行、功能上互补。IM 微调在**生成侧**扩展分布覆盖，使扩散模型能够合成低密度区域的样本；S³ 在**选择侧**从扩展后的候选池中筛选判别性最优的子组。消融实验（Table 4）证实：单独使用 IM 或 S³ 均能带来性能提升，但两者联合使用产生更大的增益——在 ImageWoof IPC=10 上，IM+S³ 达到 41.8%，而仅用 IM 为 38.7%、仅用 S³ 为 37.4%（基线 DiT 为 34.2%），验证了覆盖扩展与判别筛选的协同必要性。

整个框架中，IM 微调需要访问真实图像以计算反演潜在，S³ 需要少量真实样本以计算类质心（对真实数据的依赖程度将在后续章节的消融实验中进一步分析）。最终输出的蒸馏数据集可直接用于下游分类器的标准训练，无需任何特殊适配。



ImS³ 由两个互补的核心模块构成：**Inversion-Matching (IM) 微调**与**Selective Subgroup Sampling (S³)**。前者在微调阶段利用扩散反演的不稳定性将生成模型推向低密度区域，后者在采样阶段通过质心驱动的子组选择提升合成数据集的判别多样性。

---

### 3.1 DDIM 反演模块

DDIM 反演是 IM 微调的信号来源。给定真实图像，通过确定性 DDIM 采样器的反向过程将其映射为一系列噪声潜在变量。DDIM 的前向去噪更新为：

$$
\mathbf{z}_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \hat{\mathbf{z}}_0(z_t, t) + \sqrt{1 - \bar{\alpha}_{t-1}} \varepsilon_\theta(\mathbf{z}_t, t) \tag{1}
$$

其中预测的清晰潜在 $\hat{\mathbf{z}}_0$ 由下式给出：

$$
\hat{\mathbf{z}}_0(\mathbf{z}_t, t) = \frac{\mathbf{z}_t - \sqrt{1 - \bar{\alpha}_t} \varepsilon_\theta(\mathbf{z}_t, t)}{\sqrt{\bar{\alpha}_t}} \tag{2}
$$

反演过程采用 Euler 近似将图像逐步映射为反演噪声潜在：

$$
\mathbf{z}_{t_i} = \mathbf{z}_{t_{i-1}} + (\sigma_{t_i} - \sigma_{t_{i-1}}) \varepsilon_\theta(\mathbf{z}_{t_{i-1}}, t_{i-1}) \tag{3}
$$

该反演过程存在内在的数值不稳定性，使得反演轨迹会从高密度区域漂移到低密度区域。ImS³ 将这一通常被视为缺陷的特性转化为正面引导信号。

---

### 3.2 Inversion-Matching (IM) 微调

IM 微调的核心思想是：**在扩散模型微调过程中，对齐去噪潜在与反演潜在，迫使模型学习覆盖反演轨迹所触及的低密度区域**。

具体而言，对于每个训练样本，首先从初始潜在 $\mathbf{z}_0$ 采样噪声潜在：

$$
\mathbf{z}_t = \sqrt{\bar{\alpha}_t} \mathbf{z}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon \tag{4}
$$

同时通过 DDIM 反演获得对应时间步的反演噪声潜在 $\mathbf{z}_t^{\mathrm{inv}}$。IM 损失定义为两者之间的余弦相似度损失：

$$
\mathcal{L}_{\mathrm{IM}} = 1 - \sigma(\mathbf{z}_t^{\mathrm{inv}}, \mathbf{z}_t) \tag{5}
$$

其中 $\sigma(\cdot, \cdot)$ 表示余弦相似度。该损失鼓励模型在去噪过程中朝着反演潜在的方向调整，从而扩展分布覆盖。

为保持高密度区域的生成质量，IM 损失与标准扩散损失联合优化。标准扩散损失为预测噪声与真实噪声的均方误差：

$$
\mathcal{L}_{\mathrm{Diff}} = \left\| \epsilon_{\theta}(\mathbf{z}_t, c) - \epsilon \right\|_2^2 \tag{6}
$$

总微调损失为两者的加权组合：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{Diff}} + \lambda_{\mathrm{IM}} \mathcal{L}_{\mathrm{IM}} \tag{7}
$$

其中 $\lambda_{\mathrm{IM}} = 0.002$ 控制匹配强度。微调采用参数高效策略（Difffit），在注意力/MLP 块中插入轻量级适配器，仅更新这些适配器参数而冻结主干网络，在保持性能的同时显著减少可训练参数和计算开销。

---

### 3.3 Selective Subgroup Sampling (S³)

S³ 在采样阶段运作，无需额外训练。其目标是从每类的生成候选池中选出最具代表性和判别性的子组，构建最终蒸馏数据集。

**质心计算。** 对于类 $i$，使用冻结的特征提取器 $\phi$（轻量级 ResNet-18）将真实样本映射至归一化嵌入空间，计算真实类质心：

$$
r_i = \left\| \frac{1}{K_i} \sum_{\mathbf{x} \in \mathcal{D}_i} \phi(\mathbf{x}) \right\|_2 \in \mathbb{S}^{C_{\mathrm{Channel}}} \tag{8}
$$

对于类 $i$ 的第 $g_i$ 个候选合成子组 $S_{i,g_i}$，其子组质心为：

$$
c_{i,g_i} = \left\| \frac{1}{K} \sum_{\mathbf{x} \in S_{i,g_i}} \phi(\mathbf{x}) \right\|_2 \in \mathbb{S}^{C_{\mathrm{Channel}}} \tag{9}
$$

**S³ 选择目标函数。** 最优子组的选择通过最小化以下损失函数实现：

$$
\mathcal{L}_{\mathrm{S}^3}(\mathbf{g}) = \alpha \sum_{i=1}^{C} \log(1 - \sigma(c_{i,g_i}, r_i)) - \frac{\beta}{(C-1)G} \sum_{i=1}^{C} \sum_{j=1}^{C} \sum_{g=1}^{G} \log(1 - \sigma(c_{i,g_i}, c_{j,g})) \tag{10}
$$

该损失由两项构成：
- **第一项**鼓励子组质心靠近真实类质心，保证代表性；
- **第二项**推动子组质心彼此远离，增强类间判别性。

超参数 $\alpha$ 和 $\beta$ 平衡代表性与区分性之间的权衡。消融实验（Figure 3）表明，平衡的 $\alpha$ 和 $\beta$ 取值能取得最优性能。

**贪婪搜索。** 最优子组索引通过贪婪搜索获得：

$$
\mathbf{g}^* = \arg \min_{\mathbf{g}} \mathcal{L}_{\mathrm{S}^3}(\mathbf{g}) \tag{11}
$$

搜索过程为每类独立选择使整体损失最小的子组索引，构建最终的蒸馏数据集。

---

### 3.4 模块间协同机制

IM 微调与 S³ 之间存在因果互补关系：IM 微调扩展了扩散模型的分布覆盖范围，为 S³ 提供了更丰富多样的候选样本池；S³ 则从这些扩展后的候选中筛选出最具判别力的子组，将分布覆盖的优势转化为下游分类性能的提升。消融实验（Table 4）证实：在 ImageWoof IPC=10 设置下，单独使用 IM 达到 38.7%，单独使用 S³ 达到 37.4%，而两者结合（ImS³）达到 41.8%，验证了双模块协同的必要性。



## 实验与关键发现

### 主实验结果

ImS³ 在多个基准上系统性地超越了现有扩散型数据集蒸馏方法，尤其在细粒度分类任务上优势显著。Table 1 报告了 ImageWoof 数据集上的核心对比：在 IPC=10、骨干网络为 ResNetAP-10 的设置下，ImS³ 达到 **41.8%** 的 Top-1 准确率，较 Minimax Diffusion 的 35.7% 提升 **+6.1 个百分点**，较 DDVLCP 的 39.5% 提升 +2.3 个百分点。当 IPC 提升至 20 时，ImS³ 以 45.8% 继续领先 Minimax（43.3%）和 D³HR（44.2%）。在更大骨干网络 ResNet-18 上，IPC=50 时 ImS³ 达到 60.1%，相比 Minimax 的 53.9% 提升 +6.2 个百分点，验证了方法在不同模型容量下的鲁棒性。

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/003_Table_1.jpg]]
*Table 1: Comparison of SOTA dataset distillation methods on ImageWoof under various IPC and backbone settings. The best results are marked as bold, and the second are underlined*

在 ImageNette 数据集上（Table 2），ImS³ 同样保持领先：IPC=10 时达到 79.8%，超过 Minimax（76.3%）和 D³HR（78.5%）；IPC=50 时达到 89.0%，超过 Minimax（86.8%）和 DDVLCP（88.0%）。在 ImageIDC 医学图像数据集上（Table 3），ImS³ 在 IPC=10 和 50 下分别达到 51.8% 和 63.0%，均优于 Minimax（47.3%、57.8%）和 D³HR（50.5%、61.0%），表明方法对领域偏移具有较好的适应能力。

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/004_Table_2.jpg]]
*Table 2: Comparison on ImageNette under different IPC settings. All the results are obtained on ResNetAP-10. The best results are marked as bold and the second are underlined*

在更大规模的 ImageNet-100 上（Table 5），ImS³ 在 IPC=10 时达到 61.4%，超过 Minimax（58.2%）和 D³HR（59.8%）；在 ImageNet-1K 全量数据集上（Table 12），IPC=10 时 ImS³ 达到 45.6%，与当前最优方法 MGD³（45.5%）持平，同时超越 Minimax（44.3%），验证了方法在大规模场景下的竞争力。

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/009_Table_5.jpg]]
*Table 5: Performance comparison on ImageNet-100 under different IPC and backbone settings. Results are Top-1 accuracy*

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/016_Table_12.jpg]]
*Table 12: ImageNet-1K results (IPC=10)*

跨架构泛化实验（Table 11）表明，ImS³ 生成的蒸馏数据在 ConvNet、ResNet-18、ResNet-101、VGG-11 和 MobileNetV2 等多种架构上均取得最优或次优结果，证实合成数据具有良好的架构无关判别特征。

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/015_Table_11.jpg]]
*Table 11: Cross-architecture evaluation on ImageWoof*

### 消融实验

**IM 与 S³ 的互补性。** Table 4 的消融实验清晰分离了两个核心组件的贡献。在 ImageWoof IPC=10 设置下，基线 DiT（仅使用预训练扩散模型生成）准确率为 34.2%；单独加入 IM 微调提升至 38.7%（+4.5 pp）；单独使用 S³ 采样提升至 37.4%（+3.2 pp）；两者联合使用（完整 ImS³）达到 41.8%，相比基线提升 **+7.6 个百分点**，且显著优于任一单独组件。在 ImageNette IPC=10 上同样呈现一致趋势：基线 69.5%，仅 IM 74.0%，仅 S³ 73.2%，完整 ImS³ 79.8%。这一结果直接验证了核心洞察——分布覆盖扩展（IM）与判别多样性增强（S³）是两个互补且缺一不可的策略。

**相似度损失函数的选择。** Table 7 对比了 IM 微调中不同损失函数的效果。1−σ 余弦相似度损失（即 $\mathcal{L}_{\mathrm{IM}} = 1 - \sigma(\mathbf{z}_t^{\mathrm{inv}}, \mathbf{z}_t)$）在 ImageWoof IPC=10 上达到 41.8%，优于 L1 损失（38.7%）和 L2 损失（39.0%）；在 ImageNette IPC=10 上，1−σ 损失达到 79.8%，同样优于 L1（76.5%）和 L2（77.2%）。这表明分布感知的余弦相似度对齐比逐像素的 L1/L2 损失更有效地引导模型覆盖低密度区域，因为余弦相似度在归一化潜在空间中对方向匹配更为敏感，而非绝对值差异。

**S³ 损失中 α 与 β 的权衡。** Figure 3 的热力图展示了 S³ 损失函数中代表性权重 α 和区分性权重 β 对分类准确率的影响。当 α 和 β 取值均衡时性能最优；过度偏向 α（过度强调与真实质心的接近）会牺牲类间分离度，导致判别边界模糊；过度偏向 β（过度强调类间分离）则可能选择偏离真实分布的异常子组，损害代表性。这一结果验证了 S³ 损失设计中双目标平衡的必要性。

**特征提取器的选择。** Table 8 表明，轻量级 ResNet-18 作为特征提取器 φ 用于质心计算时，在 ImageWoof 上取得最优性能（41.8%），优于更深的 ResNet-50（40.5%）、ResNet-101（39.8%）、EfficientNet-B0（40.2%）以及多模态 CLIP 编码器（38.9%）。较浅的网络可能提供更平滑、更具泛化性的特征空间，有利于质心匹配和子组选择，而过深的网络或跨模态特征可能引入与分类任务无关的偏差。

**匹配强度 λ_IM 的敏感性。** Figure 5 展示了不同 λ_IM 取值下的验证准确率曲线。在 IPC=10、20、50 三种设置下，λ_IM=0.002 附近均取得最优或接近最优的性能；过小的 λ_IM（如 0.0005）导致分布扩展效果不足，过大的 λ_IM（如 0.01）则可能过度扭曲扩散模型的原始生成分布，损害高密度区域的保真度。阴影区域表明在最优值附近的性能波动较小，方法对 λ_IM 的选择具有一定鲁棒性。

**子组池大小 G 的影响。** Figure 6 分析了候选子组数量 G 对性能的影响。在低 IPC 设置下（IPC=10），增大 G 可提供更丰富的候选多样性，性能随 G 增加而提升直至饱和；但过大的 G（如 G≥20）引入冗余或劣质候选，导致贪婪搜索收敛到次优解，性能反而下降。在高 IPC 下（IPC=50），由于每类已有较多样本，候选多样性的边际收益递减，最优 G 值相对较小。

**真实样本预算 K_i 的分析。** Figure 4 表明，使用适量真实样本计算类质心时子组选择更稳定：K_i 过小（如 1-2 个样本）会引入显著的质心估计噪声，导致选择不稳定和性能下降；K_i 过大则收益递减，且增加对真实数据的依赖。实验显示中等数量的真实样本即可获得可靠的质心估计。

### 失败模式与局限性

尽管 ImS³ 在多数设置下表现优异，但存在以下已知局限：

1. **对真实数据质心的依赖。** S³ 采样需要访问真实数据的类质心以计算 $\mathcal{L}_{\mathrm{S}^3}$ 损失。在完全无数据的隐私敏感场景下，只能使用生成数据近似质心（如 Table 13 所示），此时性能有所下降，限制了方法在严格数据受限场景的应用。

2. **贪婪搜索的局部最优。** S³ 中的子组选择采用贪婪搜索策略（Algorithm 2, Eq. 11），理论上可能收敛到局部最优解，尤其在候选池较大且类间质心分布复杂时。全局最优搜索的计算代价过高，目前的方法在效率与最优性之间做了折中。

3. **子组池大小 G 的手动调整。** G 的最优值随 IPC 和数据集特征变化（Figure 6），需要针对不同设置手动调整，增加了超参数选择的工程负担。

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/014_Figure_6.jpg]]
*Figure 6: Effect of subgroup pool size G under different IPC settings on ImageWoof. A moderate increase in G provides richer intra-class variation and improves selection quality, especially in low-IPC regimes. However, excessively large pools introduce redundant or noisy candidates, which destabilizes selection and leads to degraded performance*

4. **任务范围限制。** 当前验证仅覆盖图像分类任务，尚未探索在文本-图像多模态蒸馏、目标检测或分割等跨任务场景的泛化能力。IM 微调对扩散模型生成分布的修改是否会影响其他下游任务的合成质量，仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/007_Table_4.jpg]]
*Table 4: Ablation study of IM and*

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/012_Table_7.jpg]]
*Table 7: Ablation study of different similarity losses used in the IM on ImageWoof and ImageNette under*

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/006_Figure_3.jpg]]
*Figure 3: Heatmap of classification accuracy under different combinations of α and*

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/010_Figure_5.jpg]]
*Figure 5: Validation accuracy under different matching strengths. Performance of our method across a range of matching coefficients*

![[assets/figures/papers/paper_list_l2686_https_arxiv_org_abs_2603_13960/figures/013_Table_8.jpg]]
*Table 8: Ablation study on feature extractors for centroid selection on ImageWoof. Top-1 accuracy (%)*



## 定位与知识库关联

### 1. 问题定位：扩散蒸馏中的“分布聚合”瓶颈

扩散模型在数据集蒸馏（Dataset Distillation）中展现出强大的生成能力，但其固有的生成特性——倾向于拟合训练分布的高密度区域——导致合成数据集在决策边界等低密度区域覆盖严重不足。这一现象被本文系统性地定义为**分布聚合（Distributional Aggregation）**问题，其直接后果是蒸馏数据的判别质量受损，难以支撑下游分类器的鲁棒训练。

现有基于扩散的蒸馏方法，如 **DiT**（预训练扩散模型直接生成，无微调）、**Minimax Diffusion**（极小极大准则微调）和 **DDVLCP**（扩散+视觉语言联合蒸馏），均未显式解决低密度覆盖问题。它们或依赖标准扩散损失保持生成保真度，或通过对抗式微调提升样本质量，但本质上仍受限于模型对高密度区域的偏好。**D³HR** 和 **D⁴M** 虽引入了域映射、组采样或原型学习等机制，但其改进方向侧重于特征空间的判别性增强，而非从扩散模型的采样动力学层面打破分布聚合。

### 2. 核心洞察：将反演不稳定性转化为正面引导信号

本文的关键洞察在于重新审视扩散反演（DDIM Inversion）的内在性质。DDIM反演过程存在固有的数值不稳定性，使得反演轨迹天然倾向于偏离高密度区域并漂移至低密度区域。以往工作通常将这种不稳定性视为需要抑制的噪声，而本文首次将其识别为可主动利用的分布扩展信号。

基于此洞察，提出的 **ImS³** 方法构建了两阶段互补框架：
- **Inversion-Matching (IM) 微调**：在预训练扩散模型（DiT-XL/2）上，通过时间对齐的潜在匹配损失（$1 - \sigma(\mathbf{z}_t^{\mathrm{inv}}, \mathbf{z}_t)$，即反演潜在与采样噪声潜在之间的余弦相似度损失）进行参数高效微调（Difffit适配器），引导模型覆盖低密度区域，同时通过标准扩散损失 $\mathcal{L}_{\mathrm{Diff}}$ 保持高密度区域的生成保真度。
- **Selective Subgroup Sampling (S³)**：在采样阶段，为每类生成多个候选子组，基于子组质心与真实类质心的接近度（代表性）以及与其他类质心的分离度（判别性）进行训练免费的贪婪选择，构建最终蒸馏数据集。

### 3. 与基线工作的关系

| 方法 | 核心机制 | 分布覆盖策略 | 判别性增强 | 本文关系 |
|------|----------|-------------|-----------|---------|
| **DiT** | 预训练扩散生成 | 无 | 无 | 基础生成器，ImS³在其上微调 |
| **Minimax Diffusion** | 极小极大准则微调 | 隐式（对抗训练） | 隐式 | 对比基线，ImS³显式扩展覆盖 |
| **DDVLCP** | 扩散+视觉语言联合 | 无 | 语言引导 | 对比基线 |
| **D³HR** | 域映射+组采样 | 域适应 | 组采样 | 部分共享组采样思想，但无IM机制 |
| **D⁴M** | 原型学习 | 无 | 原型约束 | 对比基线 |
| **SRe²L** | 非生成式蒸馏 | 不适用 | 特征匹配 | 不同范式，非扩散方法 |
| **RDED / CaO²** | 扩散蒸馏变体 | 无显式覆盖 | 变体策略 | 对比基线 |

ImS³ 与上述方法的本质区别在于：**首次从扩散反演的动力学特性出发，将不稳定性转化为分布扩展的主动引导信号**，而非依赖对抗训练、语言先验或后处理采样来间接改善覆盖。同时，S³ 的质心驱动选择策略在训练免费的前提下，实现了代表性与判别性的显式平衡，区别于 D³HR 等方法的隐式组采样。

### 4. 方法适用边界与局限

**适用场景**：
- 中等及以上 IPC（如 IPC≥10）的图像分类蒸馏任务，此时 IM 微调的分布扩展效果和 S³ 的子组多样性优势可充分发挥。
- 允许访问少量真实数据以计算类质心的场景（如 Table 13 所示，完全无数据时性能有所下降，但仍具竞争力）。

**已知局限**：
1. **对真实质心的依赖**：S³ 需要真实数据的类质心作为参考锚点。在隐私敏感或数据完全不可访问的场景下，只能使用生成数据替代，导致选择质量下降。这是该方法从“少数据蒸馏”迈向“零数据蒸馏”的核心障碍。
2. **额外训练开销**：IM 微调虽通过 Difffit 实现了参数高效（仅更新轻量适配器），但仍需约 8 个 epoch 的额外训练，相较于纯训练免费的数据选择方法（如 S³ 单独使用）增加了计算时间。
3. **超参数敏感性**：S³ 中的子组池大小 $G$ 需针对不同 IPC 手动调整——低 IPC 时较大 $G$ 提供候选多样性以提升性能，但过大 $G$ 引入冗余或劣质候选导致性能下降（Figure 6）。此外，平衡代表性（$\alpha$）和判别性（$\beta$）的权重需通过热力图搜索确定（Figure 3），增加了调参负担。
4. **贪婪搜索的局部最优**：S³ 采用贪婪搜索最小化 $\mathcal{L}_{\mathrm{S}^3}$，可能收敛到局部最优子组组合，而非全局最优解。
5. **任务泛化未验证**：当前仅在图像分类任务上验证，尚未探索在文本-图像等多模态蒸馏或目标检测、分割等跨任务场景的泛化能力。

### 5. 开放问题

1. **彻底消除真实数据依赖**：能否通过扩散模型自身生成近似质心并迭代自我引导，实现“零真实数据”蒸馏？例如，利用 IM 微调后模型生成多样本估计类质心，再以自举方式逐步精炼，形成闭环。
2. **跨生成范式的推广**：IM 损失的核心思想——利用反演/逆向过程的不稳定性扩展分布覆盖——是否可推广到 Flow Matching、一致性模型（Consistency Models）等其他生成范式？这些范式的逆向过程是否具有类似的可利用不稳定性？
3. **可微分子组选择**：S³ 的贪婪搜索能否用可微分的可学习路由网络替代？使子组选择过程联合优化，并自适应地调整候选池大小，避免手动调参和局部最优问题。
4. **极端低 IPC 下的判别增强**：在 IPC=1 的极端压缩场景下，S³ 的子组多样性优势消失，如何进一步增强单样本的判别能力？可能需要探索将类间区分信息直接注入到单样本生成过程中的新机制。
5. **与训练时蒸馏方法的融合**：IM 微调本质上改变了扩散模型的采样分布，这是否能与基于元学习或梯度匹配的训练时蒸馏方法（如 MTT、DC）结合，在合成数据上进一步优化下游任务性能？



## 原文 PDF

![[paperPDFs/CVPR_2026/IMS3_Breaking_Distributional_Aggregation_in_Diffusion_Based_Dataset_Distillation.pdf]]

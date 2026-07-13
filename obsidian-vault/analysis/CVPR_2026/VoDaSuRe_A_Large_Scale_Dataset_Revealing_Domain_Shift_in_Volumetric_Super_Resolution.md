---
title: "VoDaSuRe: A Large-Scale Dataset Revealing Domain Shift in Volumetric Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VoDaSuRe_A_Large_Scale_Dataset_Revealing_Domain_Shift_in_Volumetric_Super_Resolution.pdf
project_link: "https://augusthoeg.github.io/VoDaSuRe/"
code_link: null
aliases:
- VDB
- VoDaSuRe
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 训练数据的退化类型：通过下采样合成的低分辨率配对数据 vs. 实际采集的多分辨率扫描配对数据。
primary_logic: 为了真正提升体积超分辨率在现实场景中的性能，必须使用包含真实低分辨率扫描的配对数据集进行训练和评估，因为下采样无法模拟真实采集中的对比度变化、噪声和伪影。
claims:
- 下采样数据训练的模型在真实低分辨率数据上产生平滑预测，而真实数据训练的模型无法恢复细节。
- 在VoDaSuRe实际扫描数据上，最佳模型在4倍放大时PSNR仅16.24 dB，远低于下采样数据的19.08 dB。
- 跨域实验表明，在降采样数据上训练的模型在真实扫描上测试时性能严重下降。
- VoDaSuRe (Downsampled) 上 PSNR (2×) = 25.50 (RRDBNet3D)
---

# VoDaSuRe: A Large-Scale Dataset Revealing Domain Shift in Volumetric Super-Resolution

> [!tip] 核心洞察
> 为了真正提升体积超分辨率在现实场景中的性能，必须使用包含真实低分辨率扫描的配对数据集进行训练和评估，因为下采样无法模拟真实采集中的对比度变化、噪声和伪影。

| 字段 | 内容 |
|------|------|
| 中文题名 | VoDaSuRe: 揭示体积超分辨率中领域偏移的大规模数据集 |
| 英文题名 | VoDaSuRe: A Large-Scale Dataset Revealing Domain Shift in Volumetric Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hoeg_VoDaSuRe_A_Large-Scale_Dataset_Revealing_Domain_Shift_in_Volumetric_Super-Resolution_CVPR_2026_paper.html) · [Project](https://augusthoeg.github.io/VoDaSuRe/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | VoDaSuRe (dataset and benchmark) |
| Dataset | VoDaSuRe |

> [!tip] 效果简介
> - VoDaSuRe (Downsampled) 上，PSNR (2×) 25.50 (RRDBNet3D) vs 23.32 (HAT) (+2.18)。
> - VoDaSuRe (Registered) 上，PSNR (2×) 18.25 (RRDBNet3D) vs 17.44 (HAT) (+0.81)；PSNR (4×) 16.22 (RRDBNet3D) vs 14.95 (mDCSRN) (+1.27)。

## 概要

体积超分辨率（Volumetric Super-Resolution, VSR）旨在从低分辨率三维扫描中恢复高分辨率细节，在医学影像、材料科学等领域具有重要应用价值。然而，当前VSR研究几乎完全依赖**通过下采样人工合成的低分辨率数据**进行训练与评估，这掩盖了一个关键问题：**真实采集的低分辨率扫描与下采样数据之间存在显著的领域偏移（domain shift）**。下采样无法模拟真实CT采集中的对比度变化、噪声、射束硬化及运动伪影等物理效应，导致模型在真实场景中的表现远低于实验室指标。

针对这一瓶颈，本文提出了**VoDaSuRe**——一个大规模、多分辨率的体积超分辨率基准数据集。VoDaSuRe包含16个配对样本（共32个体积扫描），总计约194.0 × 10⁹个体素，覆盖竹材、硬木、软木、中密度纤维板、动物骨骼、人类椎骨和股骨等多种结构复杂度迥异的材料。所有样本均在同一CT设备上以固定4倍分辨率差采集高/低分辨率扫描，从而**隔离了纯分辨率差异的影响**，避免了多模态数据集中因成像设备不同而引入的混淆因素。

核心发现可归纳为三点：

1. **性能悬崖**：在VoDaSuRe的真实低分辨率扫描（registered）上，最佳模型（RRDBNet3D）在4倍放大时PSNR仅16.24 dB，远低于下采样数据上的19.08 dB（Table 2），揭示了现有方法在真实场景中的显著不足。

2. **平滑预测困境**：在下采样数据上训练的模型应用于真实低分辨率扫描时，预测结果趋于平滑平均，丢失高频结构细节；而在真实数据上训练的模型同样无法有效恢复缺失的细节（Figure 1, Figure 5）。

3. **跨域泛化失败**：跨域实验（Table 3）表明，无论训练域是下采样数据还是真实扫描数据，模型在跨域测试时性能均大幅下降，证实了两种退化类型之间存在不可忽视的分布差异。

在方法层面，VoDaSuRe并非提出新的SR模型，而是构建了一套完整的数据管线和基准：通过ITK-Elastix进行LR-HR体积配准，采用CDF匹配稳定强度分布，并基于OME-Zarr格式实现高效的3D分块采样。该基准评估了包括HAT、RCAN、EDDSR、SuperFormer、MFER、mDCSRN、MTVNet和RRDBNet3D在内的多种代表性VSR方法，所有模型在统一硬件和超参数下训练，确保了对比的公平性。

VoDaSuRe的建立揭示了体积超分辨率领域从“合成退化”走向“真实退化”研究的迫切需求，为后续鲁棒VSR模型的设计提供了关键基准和方向指引。

### 体积超分辨率中的“理想化”陷阱

体积超分辨率（Volumetric Super-Resolution, VSR）旨在从低分辨率三维图像（如CT、MRI扫描）重建高分辨率体积，在医学影像、材料科学等领域具有重要应用价值。然而，当前该领域的研究存在一个根本性的瓶颈：**几乎所有VSR模型的训练和评估都依赖于通过下采样合成得到的低分辨率-高分辨率配对数据**。这种合成退化（synthetic degradation）——通常是对高分辨率图像进行双三次或高斯下采样——过于理想化，无法模拟真实采集过程中引入的复杂退化因素，如对比度变化、噪声、射束硬化伪影和运动模糊。

这一“理想化”假设导致了严重的领域偏移（domain shift）问题：在下采样数据上表现优异的模型，一旦应用于真实低分辨率扫描，性能便急剧下降。具体表现为模型倾向于预测平滑的平均值，丢失了高频细节和精细结构，而这恰恰是超分辨率任务的核心目标。

### 现有数据集的结构性缺陷

体积超分辨率领域的另一个关键制约因素是**缺乏大规模、多分辨率的真实配对数据集**。现有体积图像数据集（如CTSpine1K、LIDC-IDRI、LiTS）虽然在医学图像分析中广泛使用，但它们通常仅提供单一分辨率的数据，超分辨率研究依赖对高分辨率数据进行人工下采样来构造训练对。这种做法的根本问题在于：**下采样退化与真实采集退化之间存在本质差异**，模型学到的映射关系无法泛化到实际场景。

此外，即使存在少量多分辨率配对数据集，其规模和多样性也远不足以支持深度学习模型的鲁棒训练。如表1所示，VoDaSuRe在总对应体素对数量和平均体积尺寸上，是现有配对分辨率三维数据集的数倍。

### 核心动机：揭示并弥合领域偏移

本文的核心动机在于**系统性地揭示体积超分辨率中的领域偏移现象**，并为社区提供一个能够真实评估模型泛化能力的基准平台。具体而言，VoDaSuRe通过以下方式填补了现有研究的关键缺口：

1. **真实配对采集**：对同一物体进行多分辨率嵌套CT扫描，获得真实采集的低分辨率与高分辨率配对数据，而非依赖下采样合成。
2. **隔离分辨率差异**：与多模态数据集不同（如micro-CT与临床CT的差异源于不同成像设备），VoDaSuRe在相同成像模态下仅改变空间分辨率，从而**隔离了纯分辨率差异的效应**。
3. **大规模基准**：包含16个配对扫描（共32个体积），总计约$194.0 \times 10^9$个体素，覆盖木材、骨骼等多种结构复杂度各异的样本。

### 关键发现预览

实验揭示了一个令人警醒的现实：在VoDaSuRe的真实低分辨率扫描数据上，最佳模型在4倍放大时的PSNR仅为16.24 dB，远低于同模型在下采样数据上的19.08 dB。跨域实验进一步证实，**在下采样数据上训练的模型在真实扫描上测试时性能严重下降**。这些发现表明，体积超分辨率领域亟需从“合成退化假设”转向“真实退化感知”的研究范式。

## 核心方法与创新机理

本文的核心贡献并非提出新的超分辨率模型架构，而是通过构建**VoDaSuRe数据集**，首次系统性地揭示并量化了体积超分辨率任务中的**领域偏移（domain shift）**问题。其关键创新体现在以下三个维度：

### 1. 揭示“合成退化 vs. 真实退化”的本质差异

体积超分辨率领域长期依赖对高分辨率图像进行下采样来构造训练配对数据。VoDaSuRe通过采集同一物体在**真实不同分辨率**下的CT扫描，构造了包含真实退化的配对数据集。这一设计使得研究者能够直接对比模型在两种退化类型下的行为差异。

核心发现是：**在下采样数据上训练的模型，面对真实低分辨率扫描时性能急剧下降**——最佳模型在4×放大时，真实扫描数据上的PSNR仅为16.24 dB，远低于下采样数据上的19.08 dB（Table 2）。更关键的是，下采样数据训练的模型倾向于产生视觉上锐利但内容不准确的预测，而真实数据训练的模型则输出平滑平均、丢失高频细节的预测（Figure 1, Figure 5）。这一现象表明，**合成退化无法模拟真实采集中的对比度变化、噪声和物理伪影**，导致模型习得的映射关系在真实场景中失效。

### 2. 构建首个大规模体积超分辨率真实退化基准

VoDaSuRe在数据规模和实验设计上具有独特优势：

- **规模优势**：包含16个配对扫描（共32个体积），总计约$194.0 \times 10^9$体素，在配对多分辨率体积数据集中体素总量最大（Table 1）。
- **退化隔离**：不同于多模态数据集（如micro-CT与clinical CT配对），VoDaSuRe固定HR与LR采集之间的分辨率为**精确4倍差异**，在相同CT设备上采集，从而**隔离了纯分辨率差异的影响**，排除了模态转换、设备差异等混淆因素。
- **标准化处理管道**：通过ITK-Elastix配准、CDF强度匹配和OME-Zarr多分辨率金字塔存储，提供了可直接用于3D分块训练的高效数据接口（Figure 3）。

### 3. 建立跨域评估方法论

VoDaSuRe不仅提供数据，更定义了**四种训练/测试配置**的实验范式（Table 3）：同域下采样、同域真实扫描、跨域（下采样训练→真实扫描测试）及其反向。这一设计使得研究者能够系统评估模型的领域泛化能力。

跨域实验结果表明，模型在跨域场景下的性能衰减具有**不对称性**：在下采样数据上训练、真实扫描上测试时，PSNR从25.50 dB骤降至约16 dB（2×放大），降幅近40%。消融实验进一步揭示了几个关键调控因素：

- **配准误差**会显著降低真实低分辨率数据上的SR精度（Figure 7a）。
- 添加**感知损失（LPIPS）**不仅未能提升真实数据上的重建质量，反而可能导致性能下降（Figure 7b），暗示基于特征的损失函数在真实退化场景下可能引入额外的分布不匹配。
- 即使对HR和真实LR数据同时进行进一步下采样，性能差距仍然存在（Figure 7c），说明问题根源不在于绝对分辨率高低，而在于**退化过程的物理差异**。
- 排除特定类型样本（如骨骼或木材）会显著影响对应类别的重建效果（Figure 7d），表明模型的领域偏移具有**类别依赖性**。

### 方法谱系与知识库定位

VoDaSuRe作为基准数据集，其评估覆盖了当前主流的体积超分辨率方法，包括基于注意力的**HAT**、残差通道注意力的**RCAN**、稠密连接的**EDDSR**、Transformer架构的**SuperFormer**、多尺度特征提取的**MFER**、医学影像专用的**mDCSRN**、多任务学习的**MTVNet**以及3D扩展的**RRDBNet3D**。这些方法在传统下采样基准上表现优异（如CTS spine1K上2×放大PSNR可达40 dB以上），但在VoDaSuRe的真实扫描数据上性能骤降，表明**现有架构的设计假设（即退化可被理想下采样近似）在真实场景中不再成立**。

VoDaSuRe的核心启示在于：体积超分辨率模型的**因果调控旋钮**应从模型架构创新转向**训练数据的退化类型**。未来研究需要关注如何设计能同时处理合成退化与物理退化的鲁棒模型，或探索能直接从真实低分辨率数据中学习高频细节恢复机制的新范式。

VoDaSuRe 并非提出新的超分辨率模型架构，而是一个**揭示体积超分辨率领域偏移的大规模基准数据集与评估框架**。其核心贡献在于构建了一条从真实多分辨率 CT 扫描到可训练配对数据的完整数据处理管道，从而使得在真实采集退化下评估 SR 模型成为可能。

### 管道总览

整个数据处理管道由四个关键模块串联而成，形成从原始采集到模型训练输入的完整链路：

1. **多分辨率嵌套 CT 扫描采集**：对同一样本分别进行高分辨率（HR）和低分辨率（LR）扫描，两者之间保持固定的 4 倍分辨率差异。这种设计使得 LR 数据并非由 HR 下采样合成，而是真实采集所得，从而保留了实际成像过程中的对比度变化、噪声和伪影。

2. **ITK-Elastix 配准**：将低分辨率扫描体积配准到高分辨率图像的坐标空间中。配准是实现像素级监督的关键步骤，但也是误差来源之一——消融实验表明，配准误差会显著降低在真实 LR 数据上的 SR 精度（Figure 7a）。

3. **强度匹配（CDF 匹配）**：对配准后的每个 LR 切片的累积分布函数进行匹配，使其与对应下采样 HR 切片的强度分布对齐。这一步骤旨在稳定训练，但论文也指出它可能改变了真实 LR 数据的统计分布，引入潜在的分布偏移。

4. **OME-Zarr 转换与分块采样**：所有数据被转换为 OME-Zarr 格式的多分辨率金字塔存储，以支持高效的外存随机采样。训练时采用 3D 分块策略，所有方法的 LR 分块大小统一设为 $32^3$。

### 输入输出流

管道的输入是一组同一物体的**多分辨率嵌套 CT 扫描**（HR 扫描 + LR 扫描），输出是两种可用于训练和评估的配对数据配置：

- **下采样配置（Downsampled）**：对 HR 数据进行 4 倍下采样生成合成 LR，模拟传统 SR 训练场景。
- **配准配置（Registered）**：将真实采集的 LR 扫描配准到 HR 坐标空间，保留真实采集退化特性。

这两种配置使得同一模型可以在合成退化和真实退化下分别训练和评估，从而量化领域偏移的影响。实验表明，在下采样数据上训练的模型在真实 LR 扫描上测试时性能严重下降（Table 3），这直接验证了管道所揭示的核心瓶颈：**合成下采样无法模拟真实采集中的物理退化过程**。

### 训练协议

所有基线模型在统一协议下训练以保证公平比较：使用单块 NVIDIA H100 80GB GPU，AdamW 优化器（$\beta_1=0.9, \beta_2=0.999$），L1 损失函数，训练 100K 次迭代。对于 4 倍放大任务，在 2 倍放大预训练模型基础上以 batch size 8 微调额外 100K 次迭代。

![[assets/figures/papers/paper_list_l810_https_openaccess_thecvf_com_content_CVPR2026_html_Hoeg_VoDaSuRe_A_Large/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of our data curation pipeline for VoDaSuRe. We collect multi-resolution nested CT scans of the same sample, after which we crop and register the LR data to the downsampled HR volumes. LR and HR volumes are masked and their intensity histograms are matched. All scans are saved to OME-Zarr with up to four resolution levels, using separate groups for HR, LR, and registered data*

VoDaSuRe 本身是一个数据集与基准工作，而非提出新模型架构的方法论文。其核心贡献在于构建了一条完整的数据处理管道，使真实采集的低分辨率体积图像能够与高分辨率图像配对，从而支持有监督的体积超分辨率训练与评估。以下聚焦该管道中的关键模块。

### 3.1 多分辨率嵌套CT采集

管道的第一步是获取同一物体在高低两种分辨率下的CT扫描图像。作者采用**固定4倍分辨率差**（a fixed resolution difference of 4 between all HR and LR acquisitions），在完全相同的CT设备上对同一样本进行两次扫描，仅改变扫描分辨率参数。这一设计的核心动机在于**隔离纯分辨率差异的效应**：不同于多模态数据集（如micro-CT与clinical-CT之间的跨设备差异），VoDaSuRe中LR与HR数据来源于同一成像模态和同一设备，从而将领域偏移的根源聚焦于分辨率本身，而非对比度变化、射束硬化或不同扫描几何带来的混淆因素。

### 3.2 配准模块：ITK-Elastix

真实采集的LR扫描与HR扫描之间不存在逐像素的空间对应关系，必须通过配准将LR体积映射到HR坐标空间。管道采用 **ITK-Elastix** 进行LR/HR体积的配准。配准是整个管道的核心瓶颈之一：配准误差（misregistration）会直接导致LR-HR像素对错误匹配，使模型学习到错误的映射关系。消融实验（Figure 7(a)）证实，配准误差显著降低了在真实低分辨率数据上的SR精度。

### 3.3 强度匹配模块：CDF匹配

配准后的LR体积与下采样HR体积之间存在强度分布差异。为稳定训练，管道对每个配准后LR体积的所有被遮罩切片，将其累积分布函数（CDF）匹配到对应下采样HR切片的CDF。这一操作虽然在训练稳定性上起到积极作用，但也引入了潜在的分布偏移风险——CDF匹配改变了真实低分辨率数据的统计特性，可能掩盖了真实采集退化的某些特征。

### 3.4 数据存储与采样模块：OME-Zarr

为支持大规模体积数据的高效随机采样，所有数据被转换为 **OME-Zarr** 格式，并以多达四个分辨率级别存储为金字塔结构。HR、LR和配准后的数据分别存放在独立的Zarr组中。这一设计使得训练管道能够以out-of-core方式高效采样3D分块（patch），块大小统一设为 $32^3$。

### 3.5 训练配置

所有基线模型在统一条件下训练：单块NVIDIA H100 80GB GPU、AdamW优化器（$\beta_1 = 0.9$, $\beta_2 = 0.999$）、L1损失函数、100K次迭代。对于4倍放大任务，模型在2倍放大预训练权重基础上再微调100K次迭代，batch size设为8。

### 关于公式

本文未引入新的数学公式或推导。所有SR模型的损失函数均为标准L1损失：

$$\mathcal{L}_{L1} = \frac{1}{N} \sum_{i=1}^{N} \| \hat{y}_i - y_i \|_1$$

其中 $\hat{y}_i$ 为模型预测的SR体积，$y_i$ 为HR ground truth，$N$ 为像素总数。消融实验（Figure 7(b)）表明，添加感知损失（LPIPS）未能提升在真实低分辨率数据上的SR质量，甚至可能导致性能下降，这进一步说明当前领域偏移问题的本质在于退化模型的差异，而非损失函数的选择。

## 实验与关键发现

### 核心瓶颈：理想化下采样与真实采集退化之间的鸿沟

实验的核心发现直指体积超分辨率（Volumetric SR）领域长期被忽视的关键问题：**在合成下采样数据上表现优异的模型，面对真实低分辨率扫描时性能急剧坍塌**。这种性能退化并非源于模型容量不足或优化策略不当，而是训练数据的退化类型（下采样 vs. 真实采集）构成了因果开关——一旦训练域与测试域在退化分布上失配，模型倾向于输出平滑的平均预测，丢失高频结构细节。

Figure 1 直观展示了这一现象：对竹子样本，下采样训练的模型（上行）能恢复部分纹理，但在纸板样本上同样策略的输出则模糊不清；而使用真实低分辨率数据训练的模型（下行）在两类样本上均无法有效恢复细节。这揭示了一个深层困境：**当前SR方法在真实低分辨率数据上似乎只能学习预测平滑平均值，能否通过架构设计恢复缺失的高频细节仍是一个悬而未决的问题**。

### 主要定量结果：VoDaSuRe揭示的性能落差

Table 2 汇总了8种主流3D SR模型在多个数据集上的定量对比，结果呈现出鲜明的层次分化：

![[assets/figures/papers/paper_list_l810_https_openaccess_thecvf_com_content_CVPR2026_html_Hoeg_VoDaSuRe_A_Large/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of state-of-the-art SR models on datasets CTSpine1K, LiTS, LIDC-IDRI and VoDaSuRe using downsampled and registered LR input data. The best performance metrics PSNR ↑ / SSIM ↑ / NRMSE ↓ / LPIPS ↓ are highlighted in bold*

**在医学影像数据集（CTSpine1K、LiTS、LIDC-IDRI）上**，所有模型均使用下采样LR训练和测试，表现稳健。以2×放大为例，顶尖方法PSNR可达40 dB以上；4×放大时仍能维持35 dB以上。这表明现有架构在合成退化场景下已相当成熟。

**在VoDaSuRe下采样子集上**，性能显著下降。最佳模型 **RRDBNet3D** 在2×放大时PSNR仅为25.50 dB，4×放大时降至19.08 dB。这一落差源于VoDaSuRe样本具有远高于医学影像的结构复杂度和纹理密度（参见Figure 2中竹材、木材、骨骼等样本的多样性）。

**在VoDaSuRe真实扫描（Registered）子集上**，性能进一步崩溃。2×放大时最佳PSNR为18.25 dB（RRDBNet3D），4×放大时仅16.22 dB。与下采样子集相比，真实扫描上的PSNR损失约7–8 dB（2×）和3 dB（4×），这直接量化了领域偏移的严重程度。

值得注意的是，**HAT** 作为2D SR领域的强基线，在3D任务中表现最弱（2×下采样PSNR 23.32 dB，真实扫描17.44 dB），说明2D架构直接迁移到体积数据存在固有局限。**mDCSRN** 在4×真实扫描上表现最差（14.95 dB），进一步印证了轻量级医学SR模型在复杂自然纹理面前的不足。

### 跨域实验：训练-测试域失配的系统性影响

Table 3 的跨域实验是理解领域偏移因果机制的关键证据。实验设计了四种训练/测试配置：
- **Downsampled → Downsampled**：域内设置，性能上界
- **Registered → Registered**：真实数据域内设置
- **Downsampled → Registered**：跨域泛化，模拟实际部署场景
- **Registered → Downsampled**：反向跨域

![[assets/figures/papers/paper_list_l810_https_openaccess_thecvf_com_content_CVPR2026_html_Hoeg_VoDaSuRe_A_Large/figures/007_Table_3.jpg]]
*Table 3: Quantitative results for cross-domain experiments on Vo-DaSuRe registered and downsampled at 2× and 4× upscaling*

以RRDBNet3D在2×放大为例：域内下采样PSNR为25.50 dB，域内真实扫描为18.25 dB；当使用下采样训练、真实扫描测试时，PSNR骤降至16.38 dB——**比域内真实扫描训练还低约2 dB**。这证实了下采样训练的模型不仅无法泛化，甚至不如直接在真实数据上从头训练的模型。反向跨域（真实扫描训练→下采样测试）同样表现不佳，说明两种退化类型之间存在本质差异，无法通过简单的域适应弥合。

Figure 6 从视觉层面印证了这一结论：下采样训练+真实测试的预测（最右列）呈现出过度平滑和结构丢失，而真实数据训练+真实测试的预测（第三列）虽能保留更多结构，但仍远逊于HR真值。

### 消融实验：解耦领域偏移的影响因素

Figure 7 的四组消融实验系统性地排除了若干可能的混淆因素：

![[assets/figures/papers/paper_list_l810_https_openaccess_thecvf_com_content_CVPR2026_html_Hoeg_VoDaSuRe_A_Large/figures/010_Figure_7.jpg]]
*Figure 7: Ablation experiments on VoDaSuRe*

**(a) 配准误差的影响**：通过向HR-LR对引入已知偏移来模拟配准不准确，结果显示配准误差确实会降低SR精度，但其影响量级远不足以解释下采样与真实扫描之间的全部性能差距。这意味着**领域偏移的主体并非来自配准不完美**。

**(b) 感知损失的作用**：引入LPIPS感知损失不仅未能提升真实低分辨率数据上的SR质量，反而可能导致性能下降。这与2D自然图像SR中感知损失提升视觉质量的普遍认知相悖，暗示**在体积数据上，感知损失可能引入与真实退化不兼容的偏置**。所有主实验均使用纯L1损失训练，这一选择在消融中得到了事后验证。

**(c) 进一步下采样**：同时对HR和真实LR数据进行下采样后再训练和测试，性能差距仍然存在。这排除了“绝对分辨率差异”作为领域偏移根源的假设——**问题不在于分辨率高低，而在于退化过程的物理本质不同**。

**(d) 样本类型排除**：排除特定类别样本（如骨骼或木材）会显著影响对应类别的重建效果，表明数据集的类别多样性对模型泛化至关重要，且领域偏移在不同材质上表现不一致。

### 失败模式与局限性

综合实验证据，当前体积SR方法在VoDaSuRe上暴露出以下系统性失败模式：

1. **高频细节的不可恢复性**：无论使用何种训练数据，模型在真实低分辨率扫描上均无法恢复接近HR真值的细节。Figure 5 中RRDBNet3D的预测在总变分（TV）指标上远低于HR数据，说明输出趋于平滑。这引发了一个根本性问题：**真实低分辨率扫描中是否保留了足够的信息以支持高频重建，还是信息在采集过程中已不可逆地丢失？**

![[assets/figures/papers/paper_list_l810_https_openaccess_thecvf_com_content_CVPR2026_html_Hoeg_VoDaSuRe_A_Large/figures/008_Figure_5.jpg]]
*Figure 5: Visualizations from VoDaSuRe. Top row: HR data, middle row: SR predictions using downsampled LR data, bottom row: SR predictions using real LR data. All outputs are obtained at 4× upscaling using RRDBNet3D. Total variation (TV) is shown for each slice*

2. **跨材质的不均衡退化**：Figure 2 展示的样本涵盖竹材、纸板、榆木、落叶松、MDF、橡木、柏木、动物骨骼、人类椎骨和股骨，不同材质在真实扫描中的退化模式差异显著。模型在纹理规则的材料（如木材）上表现相对较好，而在无定形或多孔结构（如骨骼、纸板）上几乎完全失效。

3. **强度匹配的潜在代价**：数据处理管道中的CDF匹配步骤虽稳定了训练，但可能改变了真实低分辨率数据的统计分布，引入额外的分布偏移。这一预处理策略的必要性与副作用之间的权衡尚未被充分消融。

4. **数据集规模的局限**：VoDaSuRe目前仅包含16个配对扫描（32个体积），虽在总体素数量上领先（约194.0 gigavoxels），但样本多样性仍有限，未覆盖临床MRI/CT等多种成像模态。跨模态泛化能力仍是未知数。

### 对领域发展的启示

VoDaSuRe的实验结果传递了一个清晰的信号：**体积超分辨率社区长期依赖的下采样评估协议严重高估了模型的真实能力**。在真实部署场景中，模型面对的是包含对比度变化、噪声和采集伪影的低分辨率扫描，而非理想化的双三次/双线性下采样图像。未来的研究需要直面这一领域偏移，探索能够同时处理合成退化和真实采集退化的鲁棒架构，或设计更真实的下采样模拟策略以桥接训练与测试分布。

![[assets/figures/papers/paper_list_l810_https_openaccess_thecvf_com_content_CVPR2026_html_Hoeg_VoDaSuRe_A_Large/figures/005_Figure_4.jpg]]
*Figure 4: Visual comparison of SR predictions on CTSpine1K, LIDC-IDRI and VoDaSuRe at scale 4×. From top to bottom: CTSpine1K, LIDC-IDRI, VoDaSuRe (downsampled), and VoDaSuRe (registered) – two examples. The LR inputs and corresponding HR ground truth images are shown on the left, separated by the red line*

## 定位与知识库关联

### 数据集定位：填补体积超分辨率领域的真实退化空白

VoDaSuRe 的核心贡献不在于提出新的超分辨率模型架构，而在于构建了首个大规模、多分辨率配对的真实低分辨率体积扫描数据集。在它之前，体积超分辨率研究几乎完全依赖通过下采样（bicubic 等）合成的低分辨率-高分辨率配对数据进行训练和评估。这种范式隐含假设真实低分辨率采集与理想下采样在统计上等价，而 VoDaSuRe 通过系统性的实验设计揭示并量化了这一假设的失败。

从数据集规模看，VoDaSuRe 包含 16 个配对扫描（32 个体积），总计约 $194.0 \times 10^9$ 个体素，在配对多分辨率体积数据集中按体素总量计为最大（Table 1）。其平均体积尺寸约为 $3330 \times 1820 \times 1870$，远超现有医学影像数据集（如 CTSpine1K、LIDC-IDRI）的单体积规模。与多模态数据集（如 micro-CT 与临床 CT 的跨设备配对）不同，VoDaSuRe 在同一 CT 设备上以固定 4 倍分辨率差异采集高低分辨率扫描，从而**隔离了纯分辨率差异的效应**，排除了成像设备差异引入的混淆因素。

### 数据管线的技术谱系

VoDaSuRe 的数据处理管道（Figure 3）整合了多项成熟技术，形成了一套可复现的配准与标准化流程：

1. **ITK-Elastix 配准**：将实际采集的低分辨率体积配准到高分辨率体积的坐标空间。这是弥合真实采集与下采样之间几何差异的关键步骤，但配准本身引入的误差（misregistration）被后续消融实验证实会显著降低 SR 精度（Figure 7a）。

2. **CDF 强度匹配**：通过匹配配准后低分辨率切片与对应下采样高分辨率切片的累积分布函数，稳定训练过程中的强度分布。这一操作虽然工程上有效，但本质上是**对真实数据的分布进行了人为干预**，可能掩盖或改变了真实采集中的对比度特征，构成一个潜在的分布偏移来源。

3. **OME-Zarr 多分辨率存储**：将数据转换为 OME-Zarr 金字塔格式，支持高效的外存（out-of-core）三维分块随机采样。这一设计使得在 $32^3$ 的 patch 尺寸下训练大规模 3D 模型成为可能，解决了体积数据 I/O 瓶颈。

### 基准模型覆盖与公平性设计

论文在 VoDaSuRe 上评估了 8 个代表性的体积超分辨率方法，涵盖了从经典残差网络到 Transformer 架构的谱系：**HAT**、**RCAN**、**EDDSR**、**SuperFormer**、**MFER**、**mDCSRN**、**MTVNet** 和 **RRDBNet3D**。所有模型在统一硬件（NVIDIA H100 80GB GPU）和训练配置下评估：AdamW 优化器（$\beta_1=0.9$, $\beta_2=0.999$），L1 损失，100K 次迭代；4 倍放大时在 2 倍模型基础上微调 100K 次迭代。这种统一的评估协议保证了跨模型比较的公平性，避免了因训练配置差异导致的性能偏差。

### 关键发现与领域知识的冲突

VoDaSuRe 揭示的核心矛盾在于：**在下采样数据上表现优异的模型，在真实低分辨率数据上性能急剧下降**。具体而言：

- 在 VoDaSuRe 下采样测试集上，最佳模型（RRDBNet3D）在 4 倍放大时达到 19.08 dB PSNR；而在配准的真实低分辨率数据上，同一模型仅获得 16.22 dB（Table 2）。这一约 3 dB 的差距直接量化了合成退化与真实退化之间的领域偏移。
- 跨域实验（Table 3）进一步证实：在下采样数据上训练、在真实扫描上测试时，所有模型的性能均显著下降，预测结果趋于平滑平均，无法恢复高频结构细节（Figure 5, Figure 6）。
- 值得注意的是，即使同时对高分辨率和真实低分辨率数据进行下采样后再比较，性能差距仍然存在（Figure 7c），说明**问题不在于绝对分辨率的高低，而在于退化过程的本质差异**——真实采集中的噪声、射束硬化、散射等物理效应无法被简单的下采样算子建模。

### 适用边界与局限

VoDaSuRe 的适用范围和局限性需要明确界定：

**适用边界**：
- 适用于研究**同模态、同设备下的纯分辨率退化**问题，排除了跨模态、跨设备的混淆因素。
- 为体积超分辨率模型的**领域泛化能力评估**提供了标准化测试平台。
- 数据管道的设计（OME-Zarr、分块训练）可迁移至其他大规模体积数据处理任务。

**已知局限**：
1. **样本多样性与数量有限**：仅 16 个配对扫描，覆盖木材、骨骼等材料，但远未穷尽实际应用中的样本类型。未包含临床 MRI 或其他成像模态的数据。
2. **强度匹配的副作用**：CDF 匹配虽然稳定了训练，但改变了真实低分辨率数据的统计分布，可能使模型学习到的映射偏离真实物理过程。
3. **损失函数的单一性**：所有模型仅使用 L1 损失训练。消融实验（Figure 7b）表明，添加感知损失（LPIPS）未能提升真实数据上的 SR 质量，甚至可能导致性能下降，但这一结论是否适用于其他感知损失或对抗训练策略仍有待验证。
4. **配准误差的干扰**：真实低分辨率数据需要配准到高分辨率坐标才能用于监督训练，配准误差本身成为性能下降的一个混淆因素，难以与退化差异完全解耦。

### 开放问题与未来方向

VoDaSuRe 的发现引发了一系列深层次问题：

1. **高频细节的可恢复性**：当前方法在真实低分辨率数据上倾向于预测平滑平均值，这是否意味着真实采集过程中丢失的高频信息在根本上不可恢复？还是现有架构缺乏对真实退化过程的显式建模能力？

2. **退化解耦**：领域偏移的根源究竟是退化模型的数学差异（线性下采样 vs. 复杂物理过程），还是真实采集中的物理效应（射束硬化、散射、运动伪影）？如何设计实验将这两种因素解耦分析？

3. **鲁棒 SR 模型设计**：是否存在一种模型架构或训练策略，能够同时处理下采样退化和真实采集退化，而无需针对每种退化类型单独训练？这可能需要引入退化感知的 conditioning 机制或元学习框架。

4. **评估指标的局限性**：PSNR/SSIM 等传统指标在真实退化场景下是否仍能准确反映感知质量？VoDaSuRe 中引入的 Total Variation（TV）作为补充指标（Figure 5），提示需要更全面的评估体系。

5. **数据规模的扩展路径**：如何以可控成本扩展真实配对数据的规模？是否可以通过物理模拟（如蒙特卡洛 CT 仿真）生成更接近真实退化的合成数据，作为数据增强的补充手段？

## 原文 PDF

![[paperPDFs/CVPR_2026/VoDaSuRe_A_Large_Scale_Dataset_Revealing_Domain_Shift_in_Volumetric_Super_Resolution.pdf]]

---
title: "DynamicEarthNet: Daily Multi-Spectral Satellite Dataset for Semantic Change Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/DynamicEarthNet_Daily_Multi_Spectral_Satellite_Dataset_for_Semantic_Change_Segmentation.pdf
code_link: null
project_link: https://codalab.lisn.upsaclay.fr/competitions/2882
aliases:
- DS
- DynamicEarthNet
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "利用每日未标注样本进行半监督一致性训练或通过时序架构融合多天观测，可提升语义分割精度；然而过高的日间相关性导致长序列训练不稳定，反向影响性能。"
primary_logic: "语义变化分割需同时关注像素的二值变化检测和变化区域的语义类别；解耦评估的SCS指标比全图mIoU更能真实反映方法在变化场景下的能力。"
claims:
- "CAC半监督方法利用每日未标注数据在测试集上达到43.6% mIoU，显著优于仅用月度标注的完全监督基线（37.9% mIoU），证明未标注时序信息的有用性。"
- "所有基线方法的BC（二值变化检测）指标约在10%左右，表明检测变化本身极具挑战，并凸显了新评估协议的必要性。"
- "时空模型在使用每日输入时性能下降（例如U-TAE daily test mIoU降至36.1%），说明通用时序架构难以处理高相关的逐日卫星序列，需设计专门方法。"
- "DynamicEarthNet 测试集 (LULC 语义分割) 上 mIoU = 43.6 (CAC daily, 半监督)"
---

# DynamicEarthNet: Daily Multi-Spectral Satellite Dataset for Semantic Change Segmentation

> [!tip] 核心洞察
> 语义变化分割需同时关注像素的二值变化检测和变化区域的语义类别；解耦评估的SCS指标比全图mIoU更能真实反映方法在变化场景下的能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DynamicEarthNet：面向语义变化分割的每日多光谱卫星数据集 |
| 英文题名 | DynamicEarthNet: Daily Multi-Spectral Satellite Dataset for Semantic Change Segmentation |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2203.12560) · [Project](https://codalab.lisn.upsaclay.fr/competitions/2882) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | DynamicEarthNet 数据集 + SCS 语义变化分割评估指标 |
| Dataset | DynamicEarthNet 测试集 (LULC 语义分割), DynamicEarthNet 测试集 (语义变化分割), DynamicEarthNet 测试集 (二进制变化检测) |

> [!tip] 效果简介
> - DynamicEarthNet 测试集 (LULC 语义分割) 上，mIoU 为 43.6 (CAC daily, 半监督)，对比 37.6 (U-Net monthly, 全监督)，变化 +6.0。
> - DynamicEarthNet 测试集 (语义变化分割) 上，SCS (BC & SC average) 为 18.5 (CAC daily)，对比 17.3 (U-Net monthly)，变化 +1.2。
> - DynamicEarthNet 测试集 (二进制变化检测) 上，BC (Binary Change IoU) 为 10.3 (CAC daily)，对比 10.1 (U-Net monthly)，变化 +0.2。

## 概要

**核心问题**：现有卫星变化检测数据集缺乏每日频率的像素级语义标注，导致模型无法捕捉地表覆盖的细粒度时序变化；同时，传统评估指标（如全图mIoU）无法有效解耦“是否变化”的二值检测与“变化成什么”的语义分割，掩盖了方法在变化场景下的真实能力。

**核心发现**：语义变化分割（Semantic Change Segmentation）需要同时关注变化检测和变化区域的语义分类两个子任务。通过解耦评估协议SCS（Semantic Change Segmentation score）——将二值变化IoU（BC）与变化区域语义mIoU（SC）取平均——能更真实地反映方法性能。实验表明，利用每日未标注样本进行半监督一致性训练可将语义分割mIoU从37.9%提升至43.6%（Table 4），证明高密度未标注时序信息的有用性；但通用时空架构（如U-TAE）在处理每日全量输入时性能反而下降至36.1%（Table 3），揭示高时间相关性序列对训练稳定性的负面影响。

**方法定位**：本文主要贡献为DynamicEarthNet数据集（75个AOI、每日多光谱观测、月度语义标注）和SCS评估指标，而非提出新的分割模型。基线实验覆盖静态语义分割（U-Net）、时空融合（U-TAE、U-ConvLSTM、3D-Unet）和半监督学习（CAC + DeepLabv3+）三类范式，为后续研究提供基准。

**关键结果**：所有方法在二值变化检测上表现极低（BC约10%，Table 5），表明检测变化本身是核心瓶颈；半监督方法在SCS上仅小幅领先（18.5 vs. 17.3），稀有类别（湿地、农业）的语义分割精度普遍低下，且当前方法未能有效改善。

地球表面处于持续变化之中，城市化、森林砍伐、农业轮作等过程每天都在发生。精确监测这些变化对于城市规划、灾害响应和生态保护至关重要。卫星遥感因其广覆盖、周期性的观测能力，成为地表变化监测的核心数据源。然而，当前卫星变化检测研究面临一个根本性瓶颈：**现有公开数据集普遍缺乏高频（每日）的像素级语义标注**，导致方法研究无法充分探索时序信息的潜力。

### 现有数据集的缺口

主流卫星变化检测数据集在三个维度上存在明显不足。第一，**时间分辨率低**：多数数据集仅提供双时相（变化前后各一帧）或稀疏月度观测，如 SpaceNet 7 为月度序列，而 Onera Satellite Change Detection 仅有两次观测。这使得模型无法学习地表变化的精细时序动态。第二，**标注粒度粗**：许多数据集仅提供二值变化标签（变/未变），缺乏变化区域的语义类别信息，无法支持语义变化分割这一更精细的任务。第三，**地理多样性有限**：现有数据集常局限于单一城市或特定区域，模型泛化能力难以评估。

Table 1 系统对比了公开卫星数据集的关键特征，DynamicEarthNet 在重访频率（每日）、标注密度（月度语义图）和地理覆盖（六大洲 75 个关注区域）上具有独特优势。

### 评估协议的缺陷

除数据问题外，现有评估指标同样制约了进展。传统语义分割任务使用全图 mIoU 评估，但在变化分割场景下，这一指标存在严重偏差：**未变化像素通常占图像面积的绝大部分（>80%），其分割精度会掩盖模型在变化区域——恰恰是任务核心关注区域——上的真实表现**。因此，一个能解耦变化检测精度与语义分割精度的评估协议成为迫切需求。

### 本文动机与核心思路

针对上述缺口，本文提出两项核心贡献：

1. **DynamicEarthNet 数据集**：覆盖 2018–2019 年全球 75 个关注区域，提供每日 Planet Fusion 多光谱影像（RGB+NIR，3m GSD）与对应月度土地利用/覆盖（LULC）语义标注。每日观测密度使得研究者可以探索时序信息对语义分割的辅助作用，以及变化过程的细粒度建模。

2. **语义变化分割（SCS）评估指标**：将评估解耦为两个独立组件——二值变化分数（BC）衡量“是否变化”的检测能力，语义变化分数（SC）衡量“变化成什么”的分类能力——并取平均得到综合 SCS 分数。这一设计确保模型必须在变化检测和语义识别两方面同时表现良好才能获得高分，避免了传统 mIoU 的虚假乐观。

### 核心洞察

本文的关键洞察在于：**语义变化分割必须同时关注像素的二值变化检测和变化区域的语义类别识别**。解耦评估的 SCS 指标比全图 mIoU 更能真实反映方法在变化场景下的能力。实验表明，所有基线方法的 BC 指标仅约 10%（Table 5），说明变化检测本身极具挑战，也验证了新评估协议的必要性。此外，半监督方法利用每日未标注数据可将 mIoU 从 37.9% 提升至 43.6%（Table 4），证明未标注时序信息的有用性；但时空模型在使用每日全量输入时反而性能下降（U-TAE daily test mIoU 降至 36.1%，Table 3），揭示了高相关时序序列训练的稳定性难题。这些发现共同指向一个开放方向：需要专门设计能稳定利用高密度卫星时序数据的网络架构与训练策略。

## 核心方法与创新机理

### 瓶颈与动机

现有卫星变化检测数据集普遍存在两个结构性缺陷：

1. **时间密度不足**：主流数据集如 SpaceNet 7、Onera SCD 或 LEVIR-CD 仅提供双时相或稀疏时序图像，缺乏每日级别的高频观测，无法刻画地表变化的精细时序过程。
2. **评估指标失效**：传统语义分割的 mIoU 在变化场景下严重偏向占绝对多数的“未变化”像素，无法有效解耦**变化检测**与**语义分割**两个核心子任务。

DynamicEarthNet 的核心设计正是针对上述瓶颈展开：提供全球 75 个 AOI 的每日 Planet Fusion 多光谱影像（2018-2019），并配套月度像素级 LULC 标注，使日级变化过程可观测、可评估。

### 关键创新：SCS 语义变化分割评估协议

论文的核心方法论创新并非一个新的网络架构，而是一套**解耦评估协议**——语义变化分割分数（Semantic Change Segmentation, SCS）。其设计逻辑直接回应了传统 mIoU 在变化检测中的失效问题：

1. **二值变化分数 (BC)**：仅计算预测变化图与真值变化图的 IoU，公式为
   $$\mathrm{BC}(\mathbf{b}, \hat{\mathbf{b}}) = \frac{|\{\mathbf{b}=1\} \cap \{\hat{\mathbf{b}}=1\}|}{|\{\mathbf{b}=1\} \cup \{\hat{\mathbf{b}}=1\}|}$$
   其中 $\mathbf{b}$ 由相邻帧语义标签差异定义（$\mathbf{b}_{t,i,j} := 1$ 若 $\mathbf{y}_{t,i,j} \neq \mathbf{y}_{t-1,i,j}$）。BC 完全聚焦于“哪里变了”，避免未变化像素的虚高贡献。

2. **语义变化分数 (SC)**：在真值发生变化的像素子集上，计算所有语义类别的平均 IoU：
   $$\operatorname{SC}(\mathbf{y}, \hat{\mathbf{y}} | \mathbf{b}) = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \frac{|\{\mathbf{b}=1\} \cap (\{\mathbf{y}=c\} \cap \{\hat{\mathbf{y}}=c\})|}{|\{\mathbf{b}=1\} \cap (\{\mathbf{y}=c\} \cup \{\hat{\mathbf{y}}=c\})|}$$
   SC 独立衡量“变了的地方，语义标对了没有”。

3. **SCS 综合分数**：取 BC 与 SC 的算术平均：
   $$\mathrm{SCS}(\mathbf{y}, \hat{\mathbf{y}}) = \frac{1}{2} \big( \mathrm{BC}(\mathbf{b}, \hat{\mathbf{b}}) + \mathrm{SC}(\mathbf{y}, \hat{\mathbf{y}} | \mathbf{b}) \big)$$

这一设计将变化检测的成败与语义分类的准确性**强制解耦**，使得方法在变化场景下的真实能力得以暴露。

### 关键实证发现：SCS 揭示的真相

SCS 协议的应用揭示了现有方法在变化分割上的根本性困境，这是传统 mIoU 完全掩盖的信息：

| 指标 | 最佳结果 | 核心发现 |
|------|---------|---------|
| BC（二值变化 IoU） | ~10.3% | **所有方法的 BC 均在 10% 左右**（Table 5），表明单纯检测“是否变化”本身极具挑战，远非 mIoU 数值所暗示的乐观局面 |
| SC（变化区域语义 IoU） | ~26.7% | 语义分类在变化区域的表现远低于全图 mIoU，说明变化区域的语义识别是独立难点 |
| SCS（综合） | ~18.5% | 综合分数暴露了变化分割的双重困难，为后续研究提供了明确的改进方向 |

**关键对比**：CAC 半监督方法在 LULC 语义分割上达到 43.6% test mIoU（Table 4），但在语义变化分割的 SCS 上仅 18.5%（Table 5）。这种巨大落差正是 SCS 解耦评估的核心价值——mIoU 的虚高无法反映方法在变化场景下的真实失效。

### Changed Slot：未标注时序数据的利用策略

论文在方法层面最重要的 changed slot 是**训练数据利用策略的转变**：

| 维度 | 全监督基线 | 半监督方案 |
|------|-----------|-----------|
| 标注数据 | 仅每月第 1 天的带标注图像 | 同左 |
| 未标注数据 | 不使用 | 当月所有每日未标注图像 |
| 训练机制 | 标准交叉熵监督 | CAC 一致性正则：对未标注图像随机裁剪，约束重叠区域预测一致 |
| LULC test mIoU | 37.6%（U-Net monthly） | 43.6%（CAC daily） |
| 提升幅度 | — | **+6.0% mIoU** |

这一 changed slot 的核心洞察在于：每日未标注影像中蕴含的时序一致性信息，可以通过半监督一致性训练被有效提取，从而显著提升语义分割精度。实验进一步表明，使用每周采样（weekly）的中间密度时，CAC 的 mIoU 回落至 37.9%（Table 4），证实**更高密度的未标注数据是性能提升的关键因素**。

### 反直觉发现：高密度时序的“双刃剑”效应

时空融合方法（U-TAE、U-ConvLSTM、3D-Unet）的实验揭示了一个反直觉现象：

- **周采样优于日采样**：U-TAE weekly 达到 39.7% test mIoU，而 daily 仅 36.1%（Table 3），甚至低于静态 U-Net 的 37.6%
- **原因**：每日序列的相邻帧高度相关，导致长序列训练不稳定，通用时序架构无法有效处理这种冗余性

这一发现构成了一个重要的**因果调节变量**：未标注时序数据在**半监督框架**中是有益的（CAC daily 最优），但在**时序融合架构**中过高的日间相关性反而损害性能。这为后续专用架构设计提供了明确方向——需要能够稳定处理高相关长序列的时序建模方法。

### 创新边界与局限

1. **变化检测本身未解决**：BC 仅约 10%，论文未提出专门的变化检测模块，SCS 只是暴露问题而非解决问题。
2. **稀有类别困境**：湿地、农业等类别在所有方法中精度低下，半监督和时空方法均未带来实质改善。
3. **多时相评估未定**：当前 SCS 基于双时相设定，多时相变体虽能平滑分数（Table 6，最高 27.7 SCS），但会降低对精确变化时刻的惩罚力度，论文倾向保留双时相方案。
4. **辅助数据质量问题**：额外提供的 Sentinel-2 数据存在约 26% 轻微和 5% 严重的质量问题，可能影响多模态融合实验的可靠性。

DynamicEarthNet 工作并非提出一个端到端的黑盒模型，而是构建了一套“数据–任务–评估”闭环，其核心 pipeline 围绕**每日多光谱卫星序列 → 月度语义变化分割**这一目标展开。整体框架可解耦为三个逻辑层：**数据流与预处理**、**语义分割与变化检测方法族**、以及**解耦评估协议（SCS）**。

### 数据流与预处理

输入为 Planet Fusion 的每日无云多光谱影像（RGB + 近红外，共 4 波段），覆盖全球 75 个 AOI，时间跨度为 2018-01-01 至 2019-12-31。数据预处理模块（Appendix C）执行以下标准化操作：

- **归一化**：基于整个数据集计算全局均值与标准差（见公式），对每个波段进行 Z-score 标准化。
- **数据增强**：训练时采用随机尺寸缩放、裁剪（crop）和水平翻转，以提升模型对空间变化的鲁棒性。

真值标注为**月度语义图**，由专业标注人员逐月绘制，包含不透水面、农业、森林与植被、湿地、土壤、水体、雪/冰等 7 个 LULC 类别。雪/冰类别因仅在 2 个 AOI 出现，在评估中被排除。训练时，每月仅第 1 天的图像携带完整标注（全监督基线），其余日期的图像作为未标注数据（半监督设置）或时序上下文（时空方法）。

### 方法族：从静态分割到时序融合与半监督

框架中的方法并非单一模型，而是围绕同一输入输出接口的一组基线方法族，用于系统性地探索每日数据在不同范式下的潜力。所有方法的共同输出为**月度语义分割图**（或进一步导出的语义变化分割结果）。

1. **静态语义分割骨干（全监督）**：以 **U-Net** 为代表，仅使用每月第 1 天的带标注图像进行训练。该基线直接处理单帧多光谱图像，生成逐像素的 7 类语义标签，完全不利用时序信息。其 mIoU 在测试集上为 37.6%（Table 3），是方法族的下界参考。

2. **时空融合方法**：在 U-Net 等骨干网络的基础上，引入**时序融合模块**，将一个月内连续多天的观测融合为单一的月度语义预测。论文考察了三种典型时序架构：
   - **U-ConvLSTM**：使用 ConvLSTM 进行时序特征聚合。
   - **3D-Unet**：通过 3D 卷积同时编码空间与时间维度。
   - **U-TAE**：基于自注意力的时序融合架构（Temporal Attention Encoder）。
   
   这些方法的输入是连续多天的图像序列，输出仍为月度语义图。关键发现是：**周采样（每周 1 张，共约 6 张/月）普遍优于每日全量输入**。例如 U-TAE 在周采样下测试 mIoU 为 39.7%，而每日输入下降至 36.1%（Table 3），说明过长的、高时间相关性的序列会损害训练稳定性。

3. **半监督方法**：采用 **CAC（Context-Aware Consistency）** 框架，以 DeepLabv3+ 为骨干网络。其核心机制是**半监督一致性训练模块**：对未标注的每日图像进行随机裁剪，并约束两个裁剪重叠区域的预测一致性，从而从未标注数据中提取监督信号。训练策略分为三种密度：
   - **monthly**：仅使用月度标注图像（等价于全监督）。
   - **weekly**：使用月度标注 + 每周 1 张未标注图像。
   - **daily**：使用月度标注 + 当月所有未标注的每日图像。
   
   每日半监督设置（CAC daily）在测试集上达到 43.6% mIoU，显著优于全监督的 37.9%（Table 4），证明未标注的时序信息确实可被有效利用。

### 语义变化分割的导出与评估协议

上述方法族的直接输出是**各时刻的语义分割图**，而非变化检测结果。语义变化分割通过**后处理步骤**从连续两帧的语义预测中导出：

- **二值变化图**由相邻两帧的语义标签差异直接计算（Eq. 1）：若某像素在 $t$ 时刻与 $t-1$ 时刻的语义类别不同，则该像素标记为变化（1），否则为未变化（0）。
- 变化区域的**语义类别**则直接取自预测的语义分割图。

为评估这一任务，论文提出了**SCS（Semantic Change Segmentation）评估协议**，将变化检测与语义分割解耦为两个独立指标：

- **BC（Binary Change IoU）**：仅计算预测的二值变化图与真值变化图之间的 IoU，聚焦于“是否发生变化”的检测能力（Eq. 2）。
- **SC（Semantic Change IoU）**：在真值发生变化的像素子集上，计算所有语义类别的平均 IoU，衡量“变化区域内的语义是否正确”（Eq. 4）。
- **SCS** 取 BC 与 SC 的算术平均（Eq. 5），作为单一综合分数。

该协议的核心设计动机在于：传统的全图 mIoU 会被大量未变化像素（通常占主导）稀释，无法真实反映方法在变化场景下的能力。实验表明，所有基线方法的 BC 指标仅在 10% 左右（Table 5），揭示了变化检测本身的极高难度，也印证了解耦评估的必要性。

### 输入–输出流总览

```
每日多光谱序列 (4波段, 1–30天/月)
        │
        ├─ 预处理: 归一化 + 数据增强
        │
        ├─ 方法分支:
        │   ├─ 静态语义分割 (U-Net, 仅用月度标注)
        │   ├─ 时空融合 (U-ConvLSTM / 3D-Unet / U-TAE, 用多天观测)
        │   └─ 半监督 (CAC + DeepLabv3+, 用月度标注 + 未标注每日数据)
        │
        ↓
月度语义分割图 (7类 LULC)
        │
        ├─ 相邻两帧语义图差分 → 二值变化图
        │
        ↓
语义变化分割结果
        │
        └─ SCS 评估: BC (变化检测 IoU) + SC (变化区域语义 IoU) → SCS
```

该框架的核心价值在于**模块化地解耦了数据利用策略、语义分割架构与变化评估协议**，使得研究者可以独立地改进任一层面的方法，并通过统一的 SCS 指标进行公平对比。当前框架的瓶颈在于：时空方法未能有效利用完整的每日序列（高相关性导致训练不稳定），且二值变化检测（BC）的性能极低，表明需要专门针对变化检测的架构设计，而非简单依赖语义分割图的差分。

### 1. 任务形式化：从语义标签到二值变化图

语义变化分割的核心操作是将两帧语义标签图的差异转化为二值变化图，再在变化区域上评估语义分割质量。给定时间 $t$ 的像素级语义标签 $\mathbf{y}_{t,i,j}$，二值变化图 $\mathbf{b}_t$ 定义为：

$$
\mathbf{b}_{t,i,j} := \begin{cases} 1, & \text{if } \mathbf{y}_{t,i,j} \neq \mathbf{y}_{t-1,i,j}, \\ 0, & \text{else}. \end{cases}
$$

该定义将多类语义变化检测退化为类无关的二值变化检测问题：只要相邻两帧的语义类别不同，即标记为“发生变化”。这一步骤是后续解耦评估的数学基础（Sec. 4.1, Eq. 1）。

---

### 2. SCS 评估协议：解耦变化检测与语义分割

论文的核心贡献之一是提出 **语义变化分割分数（SCS）**，将评估拆解为两个独立组件，避免传统 mIoU 因“无变化”像素占主导而掩盖变化区域的性能缺陷。

#### 2.1 二值变化分数（BC）

BC 计算预测二值变化图 $\hat{\mathbf{b}}$ 与真值 $\mathbf{b}$ 在“变化”类上的 IoU：

$$
\mathrm{BC}(\mathbf{b}, \hat{\mathbf{b}}) = \frac{|\{\mathbf{b}=1\} \cap \{\hat{\mathbf{b}}=1\}|}{|\{\mathbf{b}=1\} \cup \{\hat{\mathbf{b}}=1\}|}
$$

该指标仅关注发生变化的像素子集，有效规避了无变化区域占比过大导致的虚高精度（Sec. 4.2, Eq. 2）。

#### 2.2 语义变化分数（SC）

SC 在真值变化像素子集 $\{\mathbf{b}=1\}$ 上，计算所有语义类别 $\mathcal{C}$ 的平均 IoU：

$$
\operatorname{SC}(\mathbf{y}, \hat{\mathbf{y}} \mid \mathbf{b}) = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \frac{|\{\mathbf{b}=1\} \cap (\{\mathbf{y}=c\} \cap \{\hat{\mathbf{y}}=c\})|}{|\{\mathbf{b}=1\} \cap (\{\mathbf{y}=c\} \cup \{\hat{\mathbf{y}}=c\})|}
$$

该公式确保语义分割精度的评估被严格限定在“真正发生变化”的像素上，从而分离变化检测错误与语义分类错误（Sec. 4.2, Eq. 4）。

#### 2.3 综合分数（SCS）

SCS 取 BC 与 SC 的算术平均：

$$
\mathrm{SCS}(\mathbf{y}, \hat{\mathbf{y}}) = \frac{1}{2} \big( \mathrm{BC}(\mathbf{b}, \hat{\mathbf{b}}) + \mathrm{SC}(\mathbf{y}, \hat{\mathbf{y}} \mid \mathbf{b}) \big)
$$

该设计使得模型必须同时擅长“检测变化的发生”和“正确识别变化后的语义类别”才能获得高分（Sec. 4.2, Eq. 5）。

---

### 3. 实验流水线中的关键模块

论文并未提出新的网络架构，而是通过系统性地组合现有模块来验证数据集与评估协议的价值。实验流水线包含以下核心组件：

- **多光谱数据预处理与归一化**：对 RGB+NIR 四波段计算全局均值与标准差进行归一化，参数为 $\mathrm{mean} = [1042.59, 915.62, 671.26, 2605.21]$，$\mathrm{std} = [957.96, 715.55, 596.94, 1059.90]$（Appendix C），并结合随机尺寸缩放、裁剪与水平翻转进行数据增强。

- **语义分割骨干网络**：采用 **U-Net**（全监督基线）或 **DeepLabv3+**（半监督基线中的分割头）进行逐像素语义分类（Sec. 5.1）。

- **时序融合模块**（仅时空基线使用）：将连续多天观测融合为单一月度预测，具体架构包括 **U-ConvLSTM**（ConvLSTM 时序融合）、**3D-UNet**（3D 卷积融合）和 **U-TAE**（自注意力时序融合）（Sec. 5.1）。

- **半监督一致性训练模块**：基于 **CAC**（Context-Aware Consistency）方法，对未标注图像进行随机裁剪并约束重叠区域的预测一致性，从而利用每日未标注数据提升语义分割精度（Sec. 5.1）。

---

### 4. 关键因果机制与证据强度

- **半监督利用未标注时序数据的有效性**：CAC 使用每日未标注样本在测试集上达到 **43.6% mIoU**，显著优于仅用月度标注的全监督基线（37.9% mIoU），提升 **+6.0 个百分点**（Table 4）。该结果的证据强度高（置信度 0.98），直接证明了高密度未标注时序信息对语义分割的增益。

- **长序列高相关性对时空架构的负面影响**：U-TAE 在每日全量输入下测试 mIoU 降至 **36.1%**，而周采样（6 张/月）可达 **39.7%**（Table 3）。这表明通用时序架构难以处理高度相关的逐日卫星序列，训练稳定性受损。该发现的证据强度高（置信度 0.95），揭示了当前方法在利用高频时序数据上的根本瓶颈。

- **二值变化检测的极端困难性**：所有基线方法的 BC 指标均在 **10% 左右**（Table 5），说明即使语义分割能力提升，检测“是否发生变化”本身仍极具挑战。该结果的证据强度高（置信度 0.95），凸显了 SCS 解耦评估的必要性——mIoU 会掩盖变化检测的严重失效。

## 实验与关键发现

### 核心实验设计与评估基准

论文围绕两个递进任务展开系统实验：(1) **土地利用与土地覆盖（LULC）语义分割**——对单帧月度影像预测7类语义标签；(2) **语义变化分割**——在连续两帧间同时检测变化区域并识别其语义类别。所有实验在DynamicEarthNet数据集上执行，按AOI划分训练/验证/测试集（55/10/10），稀有类别雪/冰因仅出现在2个AOI而不纳入评估。

评估体系采用论文提出的**SCS（Semantic Change Segmentation）指标**，其核心设计逻辑是将变化检测与语义分割解耦：
- **BC（Binary Change IoU）**：仅计算变化类（$\\mathbf{b}=1$）的IoU，避免无变化类占比过高带来的虚高精度；
- **SC（Semantic Change IoU）**：在真值发生变化的像素子集上计算所有语义类别的平均IoU；
- **SCS**：取BC与SC的算术平均，综合衡量两方面的能力。

这一解耦设计的必要性在实验中得到了充分验证：全图mIoU会掩盖方法在变化区域上的真实表现差异。

### 主要结果

#### LULC语义分割：半监督方法显著优于全监督基线

Table 4展示了半监督方法CAC（Context-Aware Consistency）在不同未标注数据密度下的表现。核心发现是：

- **全监督U-Net月度基线**在测试集上达到37.6% mIoU（Table 3），但仅使用每月第1天的标注图像进行训练；
- **CAC月度（仅标注数据）**的测试mIoU为37.9%，与全监督基线相当；
- **CAC每日（利用当月所有未标注每日图像）**将测试mIoU大幅提升至**43.6%**，相对月度基线提升**+6.0个百分点**，验证了未标注时序信息对语义分割的有用性（Table 4，置信度0.98）。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/005_Table_3.jpg]]
*Table 3: Quantitative results of spatio-temporal methods. We compare the performance of different spatio-temporal architectures on the task of LULC segmentation. Individual values denote the intersection-over-union score for individual classes (cols. 3-8), as well as the averaged scores over the whole validation set (9th col.) and test set (10th col.). The monthly U-Net baseline is generally less accurate than the considered temporal architectures*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/006_Table_4.jpg]]
*Table 4: Quantitative results of semi-supervised methods. The table shows the semantic segmentation results of using the context-aware consistency-based semi-supervised approach [21] on our DynamicEarthNet dataset. We further present the IoU scores per class for the validation set. ‘Monthly’ indicates that the architecture is trained in a supervised manner. Using unlabelled satellite images improves the results over the fully supervised baseline*

这一结果表明，即使未标注的每日观测本身不提供额外标签，通过一致性正则化约束模型在不同扰动下的预测一致性，能够有效利用高密度时序数据中的信息冗余来改善表征学习。

#### 时空方法：周采样优于日采样，长序列训练存在稳定性问题

Table 3报告了时空融合方法的LULC分割结果。一个违反直觉的发现是：**使用每日全量输入反而导致性能下降**。具体而言：

- **U-TAE（自注意力时序融合）**在周采样（每月6张）设置下达到39.7%测试mIoU，优于U-Net月度基线的37.6%；
- 但当输入变为每日全量（每月约30张）时，U-TAE测试mIoU**降至36.1%**，甚至低于静态U-Net基线；
- U-ConvLSTM和3D-Unet呈现类似趋势，周采样均优于日采样。

这一现象揭示了**高时间相关性序列的训练瓶颈**：连续多天的卫星影像之间差异极小（尤其在无云条件下），过长的相关序列导致梯度传播不稳定或模型过拟合于噪声，反而损害泛化能力。这表明通用时序架构（ConvLSTM、3D卷积、自注意力）并非为处理此类高密度、高相关的遥感时序设计，需要专门的方法创新。

#### 语义变化分割：变化检测本身极具挑战

Table 5报告了所有方法在语义变化分割任务上的完整结果。最引人注目的发现是**二进制变化检测（BC）的准确率普遍极低**：

- 所有方法的BC指标均在**10%–11%**左右（U-Net月度10.1%，CAC每日10.3%），表明检测“哪些像素发生了变化”本身就是一个极具挑战的问题；
- 变化区域上的语义分割（SC）表现相对较好，CAC每日达到26.7%，显著高于U-Net月度的24.4%；
- 最终SCS分数方面，CAC每日以**18.5%**领先于U-Net月度的17.3%，但绝对水平仍然很低。

这一结果揭示了当前方法的一个根本性弱点：**模型难以可靠地定位变化区域，而一旦定位成功，对变化类别的语义识别相对可行**。这也验证了SCS指标解耦设计的价值——全图mIoU无法暴露变化检测环节的严重不足。

### 消融实验与分析

#### 未标注数据密度的影响

Table 4中CAC方法的月/周/日三组对比构成了一项关键的消融实验：
- **月度**（仅标注数据）：37.9% mIoU
- **周度**（标注+每周1张未标注）：37.9% mIoU，与月度持平
- **每日**（标注+当月所有未标注）：43.6% mIoU，显著提升

周度采样未能带来增益，说明**低密度的未标注数据不足以提供有效的一致性约束信号**；只有当未标注样本密度达到每日级别时，半监督学习的优势才得以体现。这从侧面印证了DynamicEarthNet每日标注频率的独特价值。

#### 时空方法输入频率的影响

Table 3中U-TAE的周采样（39.7% mIoU）与日采样（36.1% mIoU）对比构成另一项重要消融。日采样带来的性能退化不是偶然的——U-ConvLSTM（周37.8% vs 日36.3%）和3D-Unet（周37.6% vs 日35.4%）均呈现一致趋势。这排除了单一架构缺陷的解释，指向**高密度时序输入本身带来的训练困难**是一个系统性问题。

#### 双时相与多时相评估协议的对比

Table 6对比了双时相（仅相邻月份对）和多时相（所有月份对）两种SCS计算方式。多时相设置下SCS分数显著更高（最高27.7 vs 双时相的18.5），但这种提升源于**平滑效应**——对多个月份对取平均会稀释单次错误预测的惩罚。论文因此倾向于保留双时相设定，以更严格地衡量方法对精确变化时刻的捕捉能力。

### 失败模式与类别级分析

#### 稀有类别分割精度低下

Table 3和Table 4的逐类IoU揭示了明显的类别不均衡问题：
- **不透水面**和**森林**等常见类别IoU可达50%–60%以上；
- **湿地**和**农业**的IoU普遍低于20%，且在半监督和时空方法中均未明显改善；
- Figure 7的混淆矩阵进一步显示，湿地常被误分为土壤，农业与草地/灌木之间存在严重的混淆。

这反映了两个深层问题：(1) 类别本身的视觉歧义性（湿地与土壤在多光谱特征上可能高度相似）；(2) 类别分布的长尾效应导致模型对稀有类欠拟合。简单的数据增强或半监督训练未能有效解决这一问题，需要类别重加权或专门的数据增强策略。

#### 变化检测的普遍失败

Table 5中BC指标约10%的结果表明，所有方法在检测“是否发生变化”这一基础问题上都表现糟糕。结合Figure 2展示的日级变化过程（如建筑逐日建造、森林逐步砍伐），这种失败可能源于：
- 变化本身的渐进性——相邻两帧之间的差异可能极其细微；
- 季节性变化（如植被物候）与永久性土地利用变化之间的混淆；
- 云层、阴影等噪声导致伪变化。

#### 时空方法在日输入下的退化

Figure 5展示了U-TAE、U-ConvLSTM、3D-Unet在日输入下的定性预测对比。可以观察到，日输入模型倾向于产生更碎片化的预测，边界模糊且小目标丢失严重，这与周采样模型相对连贯的预测形成鲜明对比。这进一步印证了长序列训练的不稳定性。

### 实验公平性保障

论文在实验设计上采取了多项措施确保公平对比：
- **数据划分**：按AOI划分训练/验证/测试（55/10/10），避免空间自相关导致的信息泄露，并确保各类别在不同子集间分布尽可能均衡；
- **实现透明**：所有方法的实现细节与超参数在附录C中完整公开，包括Adam/SGD优化器选择、学习率、批大小、归一化参数（全局均值$[1042.59, 915.62, 671.26, 2605.21]$，标准差$[957.96, 715.55, 596.94, 1059.90]$）等；
- **数据质量警示**：额外提供的Sentinel-2辅助图像存在约26%轻微质量和5%严重质量问题，论文明确提醒研究者注意相关AOI的潜在影响。

### 方法谱系与知识库定位

本节实验涉及的方法可定位为以下谱系：

| 方法类别 | 代表方法 | 核心机制 | 在DynamicEarthNet上的表现 |
|---------|---------|---------|--------------------------|
| 静态语义分割 | U-Net（全监督） | 单帧编码器-解码器 | 37.6% mIoU（月度），作为基线 |
| 时空融合 | U-TAE（自注意力） | 时序自注意力融合多帧特征 | 39.7% mIoU（周采样），但日采样降至36.1% |
| 时空融合 | U-ConvLSTM | ConvLSTM时序建模 | 37.8% mIoU（周采样），同样日采样退化 |
| 时空融合 | 3D-Unet | 3D卷积融合时序维度 | 37.6% mIoU（周采样），日采样退化最严重 |
| 半监督 | CAC + DeepLabv3+ | 一致性正则化利用未标注数据 | **43.6% mIoU（每日）**，取得最优结果 |

这一对比揭示了一个重要结论：**在当前的DynamicEarthNet基准上，利用未标注数据的半监督学习比设计复杂的时序融合架构更为有效**。但这并不意味着时序信息不重要——CAC的每日训练本质上也在隐式地利用时序信息（通过多帧数据增强），只是其利用方式（一致性约束）比显式时序建模（自注意力/ConvLSTM）在当前条件下更稳定。

### 开放问题与未来方向

基于上述实验结果，论文识别出以下关键开放问题：
1. **如何设计能稳定训练长序列每日数据的专用网络架构？** 当前通用时序架构在高相关序列上普遍退化，需要针对遥感时序特点（高相关性、噪声、云层遮挡）设计专门的归一化或正则化策略；
2. **如何提升二进制变化检测（BC）的准确率？** 10%左右的BC指标表明变化检测本身是瓶颈，可能需要专门的变化检测头、对比学习预训练或时序差分特征；
3. **如何改善湿地、农业等稀有类的分割精度？** 类别重加权、针对性数据增强或多任务学习可能是潜在方向；
4. **如何定义能适应不同变化周期的多时相评估指标？** 双时相设定对渐进式变化过于严格，但多时相平滑又会降低评估敏感性，需要在两者之间找到平衡。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative results on validation set. Semantic maps (bottom row) of the semi-supervised baseline CAC [21] trained on daily images. The input sequence consists of 5 images (middle row) from September to October, spanning one month. For the first and last semantic map of the considered sequence, we show ground-truth labels (bottom right, bottom left). The three middle columns show predictions of [21]. For each sample, we magnify a specific area to highlight the temporal transition from forest & other vegetation to soil, marked red for ground-truth and pink for baseline predictions [21]. Notably, this development is captured with high fidelity by our baseline [21]. On the other hand, in certa...*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/013_Figure.jpg]]
*Figure: Daily U-TAE Daily U-ConvLSTM Monthly CAC Weekly CAC *

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/014_Figure.jpg]]
*Figure: Daily 3D-Unet Daily CAC *

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/015_Figure_7.jpg]]
*Figure 7: Confusion matrices. We show confusion matrices corresponding to the LULC segmentation results in Sec. 5.2 on the validation set. The goal is to provide a fine-grained analysis of which classes frequently get misclassified as certain other classes. Each column of an individual confusion matrix is normalized, meaning that it shows the relative distribution of predictions (in percent) for a given, true class. Results are shown for both spatio-temporal (left column) and semi-supervised baselines (right column) with three different settings each*


![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/007_Table_5.jpg]]
*Table 5: Quantitative results of semantic change segmentation on our test set. This table shows semantic change segmentation results of all methods on our DynamicEarthNet dataset*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2203_12560/figures/010_Table_6.jpg]]
*Table 6: Quantitative results of our metric variant on our test set. The first row shows the bi-temporal, and the second row shows the multi-temporal results on weekly data. The first row results are identical to the weekly results in Tab. 5*

## 定位与知识库关联

### 1. 任务定位与核心贡献

DynamicEarthNet 将自身定位在**语义变化分割**（Semantic Change Segmentation）这一新兴任务的交叉点上。该任务同时要求模型完成两个子任务：(1) 检测两帧影像之间哪些像素发生了变化（二值变化检测）；(2) 对发生变化区域的像素赋予正确的语义类别标签。这一设定区别于传统的二值变化检测（仅输出变化/未变化掩码）和静态语义分割（不关注时序变化），构成了独立的方法评估维度。

论文的核心贡献并非提出一种新的模型架构，而是贡献了**数据集 + 评估协议**这一基础设施层面的工作：
- **DynamicEarthNet 数据集**：首个提供每日重访频率且具备像素级月度语义标注的全球多光谱卫星数据集，覆盖75个兴趣区域（AOI），时间跨度2018-2019年。
- **SCS（Semantic Change Segmentation）评估指标**：将评估解耦为二值变化分数（BC）和变化区域语义分割分数（SC），取算术平均作为最终得分，避免传统全图mIoU因未变化类占比过高而掩盖变化检测能力的缺陷。

### 2. 基线方法谱系

论文在 DynamicEarthNet 上评估了三类代表性基线，形成了从静态分割到时序融合再到半监督学习的完整方法谱系：

#### 2.1 静态语义分割基线
**U-Net**（Ronneberger et al., MICCAI 2015）作为全监督静态分割的基准。该基线仅在每月第1天的标注图像上训练，完全不利用时序信息，在测试集上达到37.6% mIoU（LULC分割）和17.3 SCS（语义变化分割）。这一基线定义了“不使用时序信息”的性能下界。

#### 2.2 时空融合基线
三类经典的时序融合架构被纳入评估，核心思路是将连续多天的观测融合为单一月度语义预测：

- **U-ConvLSTM**：基于 ConvLSTM 的时空融合方案，将 U-Net 编码器提取的单帧特征送入 ConvLSTM 进行时序建模。
- **3D-UNet**：使用3D卷积直接在时空体上操作，一次性融合多帧输入。
- **U-TAE**（Garnot et al., 2020）：基于自注意力机制的时序融合架构，通过时间自注意力对多帧特征进行加权聚合。

这些时空方法在**周采样**（每月约6张影像）设置下普遍优于静态U-Net基线：U-TAE weekly 达到39.7% test mIoU，U-ConvLSTM 和 3D-UNet 分别为37.4%和37.1%。然而，当使用**每日全量输入**（每月约30张）时，性能反而下降——U-TAE daily test mIoU降至36.1%，低于月度U-Net的37.6%。这一反直觉现象揭示了通用时序架构在处理高相关逐日卫星序列时的训练不稳定问题，构成重要的方法适用边界。

#### 2.3 半监督基线
**CAC**（Context-Aware Consistency, Lai et al., 2021）结合 DeepLabv3+（Chen et al., ECCV 2018）作为骨干网络，通过一致性正则化利用未标注数据。该方法对未标注图像进行随机裁剪，约束重叠区域的预测一致性。

在 DynamicEarthNet 上的实验揭示了未标注时序数据的价值：
- CAC monthly（仅用月度标注）：37.9% test mIoU
- CAC weekly（加入每周未标注样本）：37.9% test mIoU，未见提升
- CAC daily（加入每日未标注样本）：**43.6% test mIoU**，显著提升+5.7个百分点

这表明高密度的未标注时序数据在半监督框架下确实能提供有用的语义先验，但需要足够的采样密度才能生效。

### 3. 方法适用边界与失效模式

#### 3.1 时空架构的“日采样诅咒”
每日序列的高时间相关性导致通用时空架构训练不稳定，性能反而不如周采样甚至静态基线。U-TAE daily 的36.1% mIoU低于U-Net monthly的37.6%，说明当前的自注意力时序融合机制无法有效从高度冗余的日序列中提取增量信息，反而引入了优化噪声。这一发现为后续工作提出了明确的方法设计要求：需要专门针对高相关时序设计正则化或采样策略。

#### 3.2 二值变化检测的全局瓶颈
所有基线方法在BC（二进制变化检测）指标上均仅约10%（Table 5），表明检测“哪里发生了变化”本身极具挑战。即使CAC daily在SCS上达到18.5，其BC也仅为10.3，与U-Net monthly的10.1几乎无差异。这说明现有方法的变化检测能力严重不足，且半监督和时序融合均未实质性改善这一问题。BC的低分也验证了SCS指标解耦评估的必要性——若仅看全图mIoU，这一关键短板将被掩盖。

#### 3.3 稀有类别的系统性失败
湿地（wetland）和农业（agriculture）类别在所有方法设置下均表现最差。混淆矩阵（Figure 7）显示湿地常被误分为土壤，农业常与植被混淆。这一失效在半监督和时空方法中均未明显改善，表明仅靠增加未标注数据或时序融合不足以解决类别不平衡和视觉相似性带来的语义歧义。

### 4. 与相关工作的关系

#### 4.1 数据集层面的定位
Table 1 将 DynamicEarthNet 与现有公开卫星数据集进行了系统对比。在重访频率维度上，最接近的工作是提供月度观测的数据集，而 DynamicEarthNet 是首个在多样化的全球AOI上提供**每日**观测的数据集。在标注维度上，现有变化检测数据集多提供二值变化标签或单类变化标签，缺乏密集的像素级多类语义标注。

#### 4.2 评估协议层面的定位
传统语义分割采用全图mIoU，变化检测采用F1或IoU，但两者均无法同时评估“检测变化”和“分类变化”两个维度。SCS指标通过BC和SC的解耦设计，填补了这一评估空白。Table 5 中全图mIoU与SCS的差异（如CAC daily的mIoU 43.6 vs SCS 18.5）量化地证明了传统指标对变化检测能力的虚假高估。

### 5. 开放问题与后续工作方向

论文明确指出的开放问题为后续方法研究提供了直接切入点：

1. **长序列稳定训练架构**：如何设计能稳定处理每日高相关序列的专用网络？可能的路径包括时序去冗余采样、对比学习预训练、或引入物理约束的正则化。

2. **变化检测的专项提升**：BC仅约10%的现状要求专门针对变化检测设计损失函数或架构模块，而非依赖语义分割模型的间接输出。从二进制变化出发直接预测语义类别（而非依赖两帧语义图差异）是一个值得探索的方向。

3. **稀有类别的针对性处理**：湿地和农业类别的持续低分需要类别重加权、针对性数据增强或长尾学习策略的介入。

4. **多时相评估协议的完善**：当前SCS基于双时相设定，Table 6 显示多时相变体因平滑效应产生虚高分数。如何定义能同时惩罚短时误差并适应不同变化周期的评估指标仍待解决。

5. **数据质量对多模态融合的影响**：辅助Sentinel-2数据存在约26%轻微和5%严重质量问题，提醒后续多模态工作需关注数据质量对融合效果的潜在干扰。

## 原文 PDF

![[paperPDFs/CVPR_2022/DynamicEarthNet_Daily_Multi_Spectral_Satellite_Dataset_for_Semantic_Change_Segmentation.pdf]]

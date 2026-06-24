---
title: "MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MedGMAE_Gaussian_Masked_Autoencoders_for_Medical_Volumetric_Representation_Learning.pdf
aliases:
- MedGMAE
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "将预训练重构目标从体素强度预测改为3D高斯原语参数预测，利用连续几何建模使模型学习空间连贯的解剖表征。"
primary_logic: "医学体积中解剖结构呈连续分布但整体稀疏；采用3D高斯原语作为中间表征，能以极少参数量捕捉几何形状、位置与方向，引导掩码自编码器学习具有语义连续性的解剖先验，同时使解码器获得可迁移的零样本重建能力。"
claims:
- "MedGMAE在AMOS和FLARE'22的1%少样本分割任务上分别超越先前最佳方法VoCo 2.98%和5.06% DSC。"
- "75%掩码比例与K=512高斯原语在分割迁移和零样本CT重建上同时达到最优效率-性能平衡。"
- "高斯解码器零样本初始化使CT重建训练时间相较3DGR减少约37%（1.58倍加速），同时保持最终重建质量（PSNR 46.2 ± 1.17, SSIM 98.5 ± 0.29）。"
- "频谱分析显示高斯MAE在高频区域方差比体素MAE低25%，表明其自然抑制噪声，更贴近真实频谱衰减。"
---

# MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning

> [!tip] 核心洞察
> 医学体积中解剖结构呈连续分布但整体稀疏；采用3D高斯原语作为中间表征，能以极少参数量捕捉几何形状、位置与方向，引导掩码自编码器学习具有语义连续性的解剖先验，同时使解码器获得可迁移的零样本重建能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MedGMAE：面向医学三维表征学习的高斯掩码自编码器 |
| 英文题名 | MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Z2XIRLv535); [GitHub](https://github.com/windrise/MedGMAE) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | MedGMAE |
| Dataset | AMOS multi-organ segmentation (1% labeled data), AMOS multi-organ segmentation (100% labeled data), FLARE'22 segmentation (1% labeled data), SegTHOR segmentation (100% labeled data) |

> [!tip] 效果简介
> - AMOS multi-organ segmentation (1% labeled data) 上，DSC (%) 为 58.79，对比 55.81 (VoCo)，变化 +2.98。
> - AMOS multi-organ segmentation (100% labeled data) 上，DSC (%) 为 84.90，对比 84.44 (VoCo)，变化 +0.46。
> - FLARE'22 segmentation (1% labeled data) 上，DSC (%) 为 62.72，对比 57.66 (VoCo, inferred from delta)，变化 +5.06。

## 概述
自监督预训练已成为医学影像分析的重要范式，其中基于掩码图像建模的方法通过对随机遮挡区域的重建来学习表征。然而，现有方法普遍采用体素级别的直接重建，难以建模医学体积中解剖结构的空间连续性与形状一致性，导致编码器缺乏几何抽象，且解码器在预训练后无法迁移利用。同时，医学体积中解剖结构虽然稀疏，却需要大量参数进行体素建模，造成参数效率低下。

针对上述问题，本文提出 **MedGMAE**（面向医学三维表征学习的高斯掩码自编码器），其核心创新是以 **3D 高斯原语参数预测** 取代传统的体素强度重建，作为预训练代理任务。MedGMAE 使用掩码自编码器架构，解码器输出一组 3D 高斯原语（包含位置、尺度、旋转、强度等 11 维参数），并通过可微分体渲染生成重建体积。这种连续、稀疏的高斯表示能够以极少量参数捕捉解剖结构的几何形状、位置和方向，迫使编码器学习具有语义连续性的空间先验，同时赋予解码器零样本迁移至新 CT 体积重建的能力。

实验结果表明，MedGMAE 在多个医学影像下游任务上均取得显著提升：在 AMOS 和 FLARE‘22 多器官分割中，仅使用 1% 标注数据即分别超越先前最佳方法 **VoCo 2.98% 和 5.06% DSC**；在 CT-RATE 疾病分类、脑部配准等任务上也保持优势。尤其值得注意的是，预训练的高斯解码器可作为 CT 重建的优良初始化，使训练时间缩短约 **37%**，同时保持相当的重建质量。消融研究进一步验证了 75% 掩码率与约 512 个高斯原语为最优的效率‑性能平衡点。频谱分析显示，高斯重建的高频区域方差较体素重建低 25%，自然抑制噪声，更贴近真实频谱衰减；解码器还能根据器官体积和复杂度自适应分配高斯原语数量，体现出对解剖结构的智能感知。

综上，MedGMAE 通过引入 3D 高斯表征，实现了从“离散体素重建”到“连续几何建模”的范式转换，为医学三维表征学习提供了高效且可迁移的自监督预训练框架。

## 背景与动机

医学体积数据（如CT和MRI）是现代临床诊断与定量分析的核心信息载体，但其精确标注极度耗费专家资源。为缓解标注瓶颈，基于大规模无标注体积数据的自监督表征学习已成为关键研究方向。其中，掩码图像建模（Masked Image Modeling, MIM）通过从部分可见体素重建被遮挡区域，迫使编码器学习具有判别力的体素特征，从而为下游任务提供有效初始化。然而，医学体积中存在一个根本性挑战：解剖结构通常呈连续、空间连贯的组织分布（如器官和血管），但整体占据的体积比例极低——典型腹部CT中，解剖器官仅占扫描空间约11.8%（Figure 1）。这种显著的稀疏性与连续性对掩码预训练提出了双重需求：既要高效利用稀疏信号，又必须保护形状的空间一致性。

主流MIM方法（例如MAE、SparK）存在三大结构性缺口。**第一，离散体素级重建目标破坏了语义连续性。** 这类方法直接回归每个体素的强度值，但体素之间不存在几何或拓扑约束，导致编码器学到的表征缺乏对解剖形状、位置和方向的抽象，本质上是欠约束的低层强度拟合。**第二，解码器不可迁移。** 由于预训练解码器专为体素预测设计，其输出仅为强度图，无法在下游任务中直接为需要几何建模的任务（如CT重建）提供有用初始化，往往在微调阶段被完全丢弃。**第三，参数效率低下。** 对整体积进行稠密体素重建需要与输入体积规模相当的参数量，在稀疏体积中浪费了大量容量，并容易引入高频噪声。实验证据表明，体素级重建的频谱在高频段呈现出更大的方差，与真实体积的平滑衰减特性偏离明显（Figure 7, Section 7.10）。

为弥合这些缺口，本文提出MedGMAE。其核心动机是将预训练的重构目标从体素强度预测 **重新定义为3D高斯原语（3D Gaussian primitive）的参数预测**。3D高斯原语作为一种连续几何表示，能以极少参数显式建模解剖结构的形状、位置、尺度、旋转和强度，天然契合医学体积的稀疏连续特性。在预训练阶段，编码器仅从少量可见体素块中提取特征，解码器则通过一组可学习的高斯查询标记聚合上下文信息，直接输出完整的高斯参数集合；随后的可微高斯渲染器将这些原语合成预测体积，以端到端方式最小化重构损失。这种设计迫使编码器学习具有空间连贯性的解剖抽象，而非孤立体素；同时，解码器因掌握连续几何知识，在预训练结束后可作为CT高斯重建任务的强力初始化，直接实现训练加速和零样本高质量重建（Table 4, Figure 1(c)）。通过这种“连续几何先验驱动”的掩码预训练范式，MedGMAE在多个医学下游任务中显著超越先前最优体素重建方法（例如在AMOS和FLARE’22的1%少样本分割上分别提升2.98%和5.06% DSC），同时将CT重建训练时间缩短约37%，验证了以高斯原语为中间表示的几何感知表征学习路线的有效性。

## 核心创新

MedGMAE 的核心创新在于**将预训练重构目标从离散体素强度预测转变为连续 3D 高斯原语参数预测**，从而使掩码自编码器从像素值拟合提升为几何语义抽象学习。这一设计直击医学掩码建模的根本瓶颈：现有方法（如 MAE、SparK、VoCo）依赖逐体素重建，无法建模解剖结构的空间连续性与形状一致性，导致编码器所获表征缺乏几何抽象能力，解码器仅输出体素值而不可迁移，且在医学体积天然稀疏（器官仅占约 11.8% 空间）的背景下参数效率极低。

### 变更槽位与因果机制

**重构目标（reconstruction_target）**  
从离散体素强度改为 11 维 3D 高斯参数向量（位置 `μ`、尺度 `s`、旋转 `q`、强度 `I`）。模型通过预测少量可学习高斯原语（最优 K=512）的完整参数，隐式习得解剖结构的体积连续性与形状一致性，而非逐体素复现场值（Section 3.2, Abstract）。这一转变使重构计算复杂度由 `O(N×H×W×D)` 降至 `O(N×M)`，并实现 99.25% 的参数缩减（Figure 1, Table 11）。

**解码器架构（decoder_architecture）**  
传统体素解码器预训练后即被丢弃；MedGMAE 采用轻量 Transformer 解码器，利用可学习高斯查询标记 `q_j`（与掩码块数量解耦）从编码器可见块中聚合信息，直接预测 K 组高斯参数。该解码器具备迁移性：零样本阶段即可为三维高斯重建网络提供高质量初始化，使 3DGR 重建训练时间缩短约 37%（1.58 倍加速），且最终重建质量保持在 PSNR 46.2 ± 1.17、SSIM 98.5 ± 0.29（Section 3.2, Table 4, Figure 1(c)）。

**渲染管线（rendering_pipeline）**  
引入可微高斯泼溅渲染（Equation 2），取代直接体素输出。解码器预测的高斯参数通过马氏距离计算贡献度（Equation 1），仅在有效半径内局部求和生成体积强度，既保证端到端可微，又利用稀疏渲染显著降低计算成本（Section 3.1, 7.6）。该渲染方式天然抑制高频噪声：频谱分析显示 Gaussian MAE 的高频区域方差较 Voxel MAE 低约 25%（std 0.0031 vs 0.0041），功率谱衰减更贴近真实医学图像（Figure 7, Section 7.10）。

**层次化扩展（MedGMAE\*）**  
基础框架之上加入多层次残差块（Figure 2(b)），通过从粗到细的尺度递减策略（$\Delta s^1=0.02$, $\Delta s^2=0.05$，Equation 4）预测更多高斯原语，以捕获细粒度器官细节。该扩展在低剂量 CT 重建中进一步将训练时间压缩至 251 分钟（原始 3DGR 需 397 分钟），并在分割任务上带来小幅增益（Table 4, Table 1）。

### 核心洞察与自主涌现行为

医学体积中解剖结构连续分布但整体稀疏，以 3D 高斯原语作为重构目标，强制模型从稀疏可见块推断出描述整个体积的几何基元集合。这种中间表征能以极少参数捕捉形状、位置与方向，引导编码器学习具有语义连续性的解剖先验，并赋予解码器零样本迁移能力。值得关注的是，高斯解码器在无显式监督下展现出**自适应容量分配**：在 BTCV 数据上，体积占比 60.9% 的肝脏被分配 1665 个原语，而体积占比仅 1.0% 的胆囊仅分配 26 个原语，且模型会根据器官复杂度动态调整原语半径（Table 14, Section 7.11），验证了高斯原语作为几何抽象的有效性。

### 证据要点

- **少样本分割突破**：AMOS（1% 标注）DSC 58.79%，较先前最佳 VoCo 提升 2.98 个百分点；FLARE’22（1%）提升 5.06 个百分点（Table 1，置信度 0.95）。
- **全量数据竞争力**：AMOS（100%）DSC 84.90%，超越 VoCo 0.46%（Table 1）。
- **多任务迁移**：CT-RATE 分类 AUC 76.40%（+0.38% vs VoCo-160K）；OASIS 脑配准 DSC 85.7%（+1.3% vs VoCo）（Table 2, Table 3）。
- **效率最优配置**：掩码率 75%、高斯原语数 K=512 在分割迁移和零样本重建上实现最佳效率‑性能平衡（Table 10–13）。

### 开放性局限

预训练固定于 $96^3$ 分辨率和单一 CT 模态，向多模态、多分辨率数据的泛化尚待验证；零样本 CT 重建仍受 FBP 重建噪声影响；高斯原语数量 K 需人工设定，未实现完全自适应；当仅存分割标注而无强度信息时，高斯解码器的零样本优势可能受限。此外，频谱分析中平均频谱 L2 距离与体素重建无显著差异（p=0.12），提示整体频谱保真度仍处同一量级（Figure 7 附注）。

## 整体框架

![[assets/figures/papers/iclr26_0014_Z2XIRLv535_MedGMAE_Gaussian_Masked_Autoencoders_for_Medical/figures/001_Figure_1.jpg]]
*Figure 1: MedGMAE overview. (a) our MedGMAE pre-training with 3D Gaussian Splatting reconstruction leverages CT volume sparsity (anatomical organs occupy only 11.8% of space) to achieve 99.25% parameter reduction and superior coherence compared to voxel-based MIM methods. (b) Pre-trained encoder fine-tuning for downstream tasks: our MedGMAE could learn a strong encoder representation for downstream segmentation, registration, and classification tasks across multiple medical datasets. (c) our MedGMAE could bring a zero-shot capability for 3DGR-based CT reconstruction with 1.39× speed-up*

![[assets/figures/papers/iclr26_0014_Z2XIRLv535_MedGMAE_Gaussian_Masked_Autoencoders_for_Medical/figures/002_Figure_2.jpg]]
*Figure 2: MedGMAE architecture. (a) MedGMAE pre-training framework that processes patchified and masked input through an encoder-decoder architecture to predict 3D Gaussian parameters, which are then rendered and optimized via reconstruction loss. (b) Extended MedGMAE* with multi-level residual blocks for progressive Gaussian parameters refinement*

MedGMAE 是一种自监督预训练框架，其核心设计是将传统掩码自编码器的重建目标从离散体素强度替换为连续的三维高斯原语参数预测。这一转变使模型在预训练阶段即能学习空间连续、几何一致的解剖表征，同时赋予解码器可迁移的零样本重建能力，用于加速三维医学影像重建等下游任务。

**整体流水线**可分为四个模块：ViT Large 编码器、轻量 Transformer 解码器、高斯参数预测头以及可微高斯渲染器。输入的三维医学体积（典型分辨率 $96^3$）首先被分块（patchify），随后随机施加掩码（掩码率默认为 75%），仅保留可见块（约原体素数的 25%）送入编码器。编码器负责从可见块中提取高维视觉特征，输出一组潜在嵌入。解码器接收由**类别标记**、**K 个可学习高斯查询标记**（$q_j$）以及**编码器可见块标记**拼接而成的序列（式 3）。这些查询标记通过交叉注意力聚合编码器特征，并驱动四个专门的线性预测头分别输出 K 组 11 维高斯参数：位置 $\mu$、尺度 $s$、旋转 $q$ 和强度 $I$。该解码器设计关键优势在于高斯数量 $K$ 独立于掩码标记数量，可灵活控制表示容量；实验表明 $K=512$ 在分割迁移和零样本重建上实现最优效率-性能平衡。

预测出的高斯参数随即被送入**可微高斯渲染器**。渲染器依据高斯贡献函数（式 1）和局部加权求和（式 2）重建完整体积强度分布，仅在掩码区域计算重建损失，从而引导模型学习从稀疏观测中推断完整几何形状。这种“高斯代理任务”使模型更自然地对齐于医学体积中的连续解剖结构，频谱分析证实高斯 MAE 的高频方差比体素 MAE 低约 25%，表明其抑制噪声的能力更强。

**输入-输出流**总结如下：输入为随机掩码的三维 patch 序列 → 编码器提取可见块特征 → 解码器整合类别标记、查询标记和编码器标记，输出 K 组高斯参数 → 渲染器依据高斯参数渲染出完整体积 → 计算渲染体积与原始体积的差异（通常为掩码区域的归一化 L2 误差）并反向传播优化编码器、解码器及预测头。

在扩展版本 **MedGMAE\*** 中，解码器增加多层次残差块，允许从粗到细预测更多高斯原语。每一层在基础高斯参数上预测位置、尺度、强度残差（采用 tanh 激活约束残差范围），并通过尺度减量（$\Delta s^1=0.02$, $\Delta s^2=0.05$）保证层次化递减的细节粒度。该设计提升了模型对精细解剖结构的捕获能力。

整体框架以 75% 掩码率和 $K=512$ 个高斯原语为默认配置。预训练完成后，编码器可直接微调用于分割、分类、配准等下游任务；高斯解码器亦可直接作为 3DGR-CT 重建方法的零样本初始化，使训练时间减少约 37%（1.58 倍加速），同时保持较高重建质量（PSNR 46.2 ± 1.17，SSIM 98.5 ± 0.29）。

## 核心模块与公式推导

MedGMAE 以 3D 高斯原语参数预测替代传统体素强度重建，使掩码自编码器在医学体积中学习空间连续的解剖先验。其核心瓶颈在于传统离散体素重构无法建模结构的连续性，且解码器不可迁移；通过将重建目标改为 11 维高斯参数（位置、尺度、旋转四元数、强度），模型可从稀疏可见块中推测全局几何抽象，解码器亦获得零样本重建能力（Section 3.2、Abstract）。以下分述关键模块与核心公式。

### 1. Vision Transformer 编码器
采用 ViT Large 骨干（Table 6），将体积切分为立方体块（$16^3$ 或 $12^3$），以掩码率 $r=0.75$ 随机遮蔽后仅将可见块送入编码器。编码器输出高维特征，仅处理约 25% 的块，显著降低预训练计算量（Section 3.2、7.4）。

### 2. 轻量 Transformer 解码器与高斯查询机制
解码器输入由三类标记拼接（公式 3）：

$$
X_{dec} = \{ \hat{x}_1 \} \cup \{ q_j \}_{j=1}^{k} \cup \{ \hat{x}_i \}_{i=2}^{n}
$$

$\hat{x}_1$ 为类别标记，$\{q_j\}$ 是 $k$ 个可学习的高斯查询标记（典型值 $k=512$，与掩码数量解耦），$\{\hat{x}_i\}$ 为编码器输出的可见块特征。解码器为轻量 Transformer（Table 7），通过自注意力与交叉注意力将全局信息聚合到查询标记上。每个查询标记经四个独立线性头映射为 11 维高斯参数：位置（3 维）、尺度（3 维）、旋转（4 维四元数）、强度（1 维）。各预测头采用特定初始化（如尺度头偏置 $-1.386$）以稳定训练（Section 7.5、Table 8）。

### 3. 可微高斯渲染与体积重建
基于预测的高斯参数，通过可微 splatting 渲染完整体积。单高斯贡献定义为马氏距离加权的强度衰减（公式 1）：

$$
G_i( X | g_i ) = I_i \cdot e^{ -\frac{1}{2} ( X - \mu_i )^{T} \Sigma_i^{-1} ( X - \mu_i ) }
$$

$g_i$ 表示第 $i$ 个高斯，包含中心 $\mu_i$、协方差矩阵 $\Sigma_i$（控制形状与方向）和强度 $I_i$。体素 $X$ 的最终强度由该点有效半径内的所有高斯贡献局部求和得到（公式 2）：

$$
V( X | g_i ) = \sum_{ i: \| X - \mu_i \| \leq d_i } G_i( X | g_i )
$$

$d_i$ 为根据尺度参数确定的截断半径。渲染采用稀疏策略，仅对每个高斯 $2\sigma$ 邻域内的被掩码像素计算贡献，将复杂度从 $O(N \times HWD)$ 降至 $O(N \times M)$（$M$ 为掩码像素数），大幅提升效率（Section 7.6 前伪代码、Section 3.1）。

### 4. 层次化残差预测（MedGMAE*）
扩展版 MedGMAE* 引入多级残差块，实现由粗到细的高斯 densification（Figure 2(b)）。基础高斯参数由主解码器生成，后续层级通过残差模块预测偏移量。所有残差预测均采用 $\tanh$ 激活以限制输出范围。以尺度更新为例，第 $l$ 级尺度参数为（公式 4）：

$$
s^l = s^0 + \hat{s}^l \cdot \sigma_{scale} - \Delta s^l,\quad \sigma_{scale}=0.1,\;\Delta s^1=0.02,\;\Delta s^2=0.05
$$

$\hat{s}^l$ 为预测残差，$\sigma_{scale}$ 控制残差幅度，递减偏置 $\Delta s^l$ 保证高层次高斯具有更小尺度，使模型能同时捕获大尺度结构与小尺度细节。其余参数（位置、强度）采用类似残差更新公式（part_003 手稿注释），同样受基础高斯约束以维持空间一致性。

### 模块总结
上述设计使 MedGMAE 将体积重建抽象为连续几何原语的学习：编码器被迫从高度稀疏的输入中推断解剖结构的位置、形态与连续性，从而获得具有语义抽象能力的表征；解码器因直接输出 3D 高斯参数而天然具备可迁移性，可在下游 CT 重建任务中提供零样本初始化（相比 3DGR 方法训练时间减少 37%，Table 4）。掩码率 75% 与高斯数量 $K=512$ 被证明为精度‑效率最优配置，且高斯原语会根据器官体积和复杂度自适应分配容量（Table 14、Section 7.11）。

## 实验与分析

### 主结果：少样本分割显著超越，全量微调持续领先

MedGMAE 的核心优势体现在低标注比例下的泛化能力。**在 AMOS 和 FLARE’22 的 1% 少样本分割任务上，MedGMAE 分别超越此前最佳方法 VoCo 2.98% 和 5.06% DSC**（Table 1），证明高斯原语重构所学习的几何连续性表征比体素重建更能弥补标注稀缺。在 100% 标注条件下，MedGMAE 仍稳定优于 VoCo（AMOS 84.90% vs 84.44%，SegTHOR 89.15% vs 约 88.52%），显示出预训练先验的增益并不因微调而消失。配准任务进一步佐证其表征通用性：OASIS 数据集上 DSC 提升 1.3%（85.7% vs VoCo 84.4%，Table 3）。

![[assets/figures/papers/iclr26_0014_Z2XIRLv535_MedGMAE_Gaussian_Masked_Autoencoders_for_Medical/figures/003_Table_1.jpg]]
*Table 1: Comparison of different methods with different proportions on AMOS (Ji et al., 2022), FLARE’22 (Ma et al., 2024), BTCV (Landman et al., 2015) and SegTHOR (Lambert et al., 2020). The DSC (%) is reported. val (bold) / val (underline) : top method / second method. † denotes we utilize official pre-training weights. ‡ denotes the results are copied from VoCo (Wu et al., 2024b). base Gaussian constraints, significantly enhancing the model’s ability to capture fine-grained details in CT reconstruction*

分类任务上，CT-RATE 疾病的 AUC 从 VoCo-160K 的 76.02% 提升至 76.40%（Table 2），雷达图揭示 MedGMAE 在多数疾病类别上均保持优势（Figure 5）。值得注意的是，**解码器的零样本 CT 重建能力提供了额外的效率收益**：以 MedGMAE 预测的高斯点初始化替代 3DGR 的随机初始化，使 80 个投影角度的重建训练时间减少约 37%（从 397 分钟降至 251 分钟，Table 4），同时保持最终重建质量（PSNR 46.2±1.17，SSIM 98.5±0.29）。这一加速直接源于预训练解码器对解剖结构的高斯抽象，其参数仅为体素表达量的 0.75% 却保留了核心几何信息。

![[assets/figures/papers/iclr26_0014_Z2XIRLv535_MedGMAE_Gaussian_Masked_Autoencoders_for_Medical/figures/007_Table_4.jpg]]
*Table 4: Comprehensive reconstruction comparison across different projection views. 3DGR refers to the initialization method employed in the original paper (Li et al., 2025), whereas MedGMAE and MedGMAE* indicate initialization using Gaussian points estimated through zero-shot inference by our proposed model. Values are reported as mean ± standard deviation. The best results are in bold*

### 消融分析：掩码率与高斯原语数量决定性能均衡

**掩码率 75% 与高斯原语数 K=512 构成了跨任务的最优效率-性能平衡点**。在 AMOS 和 SegTHOR 分割迁移上，降低掩码率（如 50%）会削弱编码器学习难度，导致 DSC 下降（Table 10）；进一步提高至 90% 则因可见块过少而损害重建与表征质量。同样，K=256 不足以捕捉所有解剖结构，而 K=768 引入冗余致使分割性能轻微回落（Table 11）。零样本 CT 重建也呈现相同规律：75% 掩码率与 K=512 取得最高 PSNR/SSIM，超过或低于该组合均导致重建噪声增加（Table 12、13）。这一非单调特征表明，高斯原语不仅是一种低维投影，更是对体积固有稀疏性的显式建模——过少的原语无法覆盖所有器官，过多的原语则破坏稀疏先验，迫使模型拟合无效细节。

**代理任务的直接对比（Table 5）揭示了瓶颈所在**：将体素 SSL 替换为高斯 SSL 在相同 ViT Large 编码器下使 AMOS DSC 从 80.03% 飙升至 84.90%，证实离散体素重建无法驱动的连续几何抽象正是此前方法的性能瓶颈。频谱分析（Figure 7）提供了频域解释：高斯 MAE 重建的功率谱在高频区域方差比体素 MAE 低约 25%（std 0.0031 vs 0.0041），更贴近真实图像的频谱衰减规律，说明高斯原语天然抑制了高频噪声而非试图逐体素拟合噪声，这一内在去噪特性是迁移性能提升的物理根源。

![[assets/figures/papers/iclr26_0014_Z2XIRLv535_MedGMAE_Gaussian_Masked_Autoencoders_for_Medical/figures/009_Table_5.jpg]]
*Table 5: Transfer ablation on MedGMAE. The DSC (%) is reported*

![[assets/figures/papers/iclr26_0014_Z2XIRLv535_MedGMAE_Gaussian_Masked_Autoencoders_for_Medical/figures/023_Figure_7.jpg]]
*Figure 7: Radial power spectrum comparison across 10 validation samples from BTCV dataset. Average power spectral density curves for Ground Truth (black), Voxel MAE (red), and Gaussian MAE (green) are shown with ± standard deviation error bands (shaded regions). Both reconstruction methods accurately preserve the dominant low-frequency components ( $\omega$ ~ $\leq$ ~ 0 . 3 ) which contain over 99% of the spectral energy. In the high-frequency regime $\mathrm { ( \omega \sim 0 . 3 , }$ , marked by the dashed vertical line), Gaussian MAE demonstrates superior stability with 25% lower variance (std: 0.0031) compared to Voxel MAE (std: 0.0041), exhibiting smoother spectral decay that more closely follows the...

**器官级原语统计（Table 14）验证了自适应解剖建模**：解码器无需任何器官监督，自动为占体积 60.9% 的肝脏分配 1665±747 个原语，而仅占 1.0% 的胆囊仅分配 26±12 个原语；复杂器官（如胃、胰腺）具有更小的平均高斯半径，以更细粒度刻画不规则边界。这种无监督的容量分配直接源自高斯原语的连续几何表达能力，是体素模型无法做到的。

### 失败模式与局限性

尽管高斯解码器提供零样本初始化加速，**低剂量 CT 重建任务仍受滤波反投影（FBP）噪声限制**，初始化质量存在提升空间——当前方法仅在静态体积内预测高斯，缺乏对投影噪声的显式建模。**预训练域单一**（固定分辨率 96³ 的 CT 数据），向多模态、多分辨率医学影像的泛化尚待验证。此外，高斯原语数量 K 需手工选择，缺乏针对输入体积复杂度的自适应机制。最后，高斯解码器的零样本能力依赖于强度重建任务，**对于仅有分割标注而无强度信息的纯语义下游任务（如部分肿瘤分割），解码器难以提供等价初始化收益**，这是目前设计的边界。

## 方法谱系与知识库定位

MedGMAE 从根本上改变了医学掩码自编码器的表征学习范式：将重构目标从离散的体素强度转换为 11 维 3D 高斯原语参数预测。这一设计与现有体素级掩码自编码器（如通用 MAE、SparK）以及此前最佳的医学自监督方法 VoCo（同样依赖体素重建）形成鲜明对比。体素重建的瓶颈在于不能建模解剖结构的空间连续性与形状一致性，编码器提取的特征缺乏几何抽象，而体素解码器通常后训练即丢弃，无法再利用。MedGMAE 通过预测连续的高斯原语（位置 μ、尺度 s、旋转 q、强度 I），以极少的参数（默认 K=512）捕获全局几何先验，迫使编码器学习空间连贯的解剖表征；与此同时，轻量 Transformer 解码器由可学习的查询标记生成高斯参数，不再依赖掩码标记数量，并借助可微体积渲染计算掩码区域的重建损失，使得解码器本身具有显式的几何结构，可直接作为下游物体重建的高质量初始化。实验显示，该因果机制有效：在 AMOS 和 FLARE 22 的 1% 少样本分割上，MedGMAE 超越 VoCo 分别达 2.98% 和 5.06% DSC（Table 1）；零样本 CT 重建中，预训练的高斯解码器使训练时间相对从零开始的 3DGR 缩短约 37%（1.58× 加速），最终质量与随机初始化相当（PSNR 46.2 ± 1.17, SSIM 98.5 ± 0.29，Table 4, Figure 4）。

在方法谱系中，MedGMAE 是掩码自编码器（MAE）与 3D 高斯打点（3DGS）的协同产物。它保留了 ViT Large 编码器、块化掩码、编码器‑解码器不对称结构这些经典设计，但以 “高斯代理任务” 替代 “体素代理任务”（changed_slots: reconstruction_target, decoder_architecture, rendering_pipeline）。相较于通用的 MAE 将解码器视为辅助，MedGMAE 的解码器通过预测可渲染的高斯参数而具有可迁移性：对于消融中的 CT 重建，直接使用预训练高斯解码器的预测作为 3DGR（Li et al.）的初始化，在 80、120、160 投影下均大幅减少训练时间与收敛迭代次数。同时，解码器不囿于固定数量的掩码块，K 值可独立设定，提供了参数效率与表示容量的灵活平衡 —— 消融证实 K=512 在分割迁移与零样本重建上达到最优（Table 11, Table 13），过多的原语反而引入冗余造成性能下降。频谱分析则从信号角度揭示了高斯代理任务的优越性：高斯 MAE 的高频区域方差约为体素 MAE 的 75%（标准差 0.0031 vs 0.0041），径向功率谱衰减更平滑，表明其对医学体积中与解剖无关的噪声具有天然抑制作用（Figure 7, Section 7.10）。

适用边界受当前预训练协议限制。所有基础实验均基于 CT 模态、固定输入分辨率 96³、掩码率 75% 与高斯数量 K=512，这些配置在消融中验证为接近最优（Table 10, Table 11），但向多模态（如 MRI）或多分辨率的泛化尚未验证。编码器通过微调即可适应多种下游任务（分割、分类、配准），但解码器的零样本能力严格依赖于强度重建损失 —— 对于无体素强度监督的纯分割标注场景，直接提供初始化存在困难。此外，低剂量 CT 任务中仍受滤波反投影（FBP）重建噪声影响，零样本初始化质量有进一步提升空间；即便如此，预训练的几何先验仍展现出有效的去噪趋势（频谱方差降低），为后续改进留下可能。

基于上述边界，主要局限与开放问题包括：（1）FBP 重建噪声 —— 能否构建多视角 3D 高斯基础模型以直接抑制 FBP 噪声，使得 CT 重建初始化质量更高？（2）解码器的强度依赖性 —— 在无强度监督的纯分割或下游任务中，是否可通过域适应或辅助任务使高斯解码器提供有用的几何初始化？（3）原语数量 K 的手动设定 —— 尽管解码器已表现出根据器官体积和复杂度自适应分配密度的能力（如肝脏占体积 60.9% 分配约 1665 个原语，胆囊 1.0% 体积仅分配 26 个，且复杂器官使用较细粒度的高斯，Table 14），但 K 作为全局超参数仍需人工选择，设计动态容量选择机制将进一步提升自适应性。（4）多模态与时序扩展 —— 当前预训练限于 3D CT，所提炼的几何先验能否高效迁移到多模态（MRI/超声）或 4D 血管／呼吸运动分析中，构成重要的开放方向。（5）解码器的通用可迁移性 —— 目前仅在 CT 重建任务中验证了加速效果，是否可将其用于零样本异常检测、形状补全等任务仍未有实验覆盖，需要进一步考察。上述问题的解决有望将几何感知的自监督框架从单一 CT 体积表征推向更广泛的医学影像理解。

## 原文 PDF

![[paperPDFs/ICLR_2026/MedGMAE_Gaussian_Masked_Autoencoders_for_Medical_Volumetric_Representation_Learning.pdf]]

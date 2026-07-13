---
title: "Depth Any Panoramas: A Foundation Model for Panoramic Depth Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Depth_Any_Panoramas_A_Foundation_Model_for_Panoramic_Depth_Estimation.pdf
project_link: https://insta360-researchteam.github.io/DAP
code_link: null
aliases:
- DDAP
- DAPFMPDE
tags:
  - CVPR_2026
  - topic/vision_multimodal_applications
  - topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 数据环路中的大规模多域数据构建与三阶段伪标签精炼策略，结合几何与清晰度感知的多损失优化。
primary_logic: 通过融合大规模标注和伪标注全景数据，采用渐进式伪标签精炼训练管线，并设计几何一致性（法线、点云损失）与清晰度导向（密集保真度、梯度损失）的优化目标，可构建一个在室内外场景均具有强零样本泛化能力的全景深度基础模型。
claims:
- DAP 数据引擎构建了约 2M 样本的全景数据集，覆盖室内/室外与合成/真实四个域，远超先前方法的数据规模与多样性。
- 三阶段流水线通过场景不变标注器、真实感不变标注器及最终 DAP 训练，逐步弥合合成–真实与室内–室外域差距，并利用 PatchGAN 判别器筛选高置信度伪标签。
- DAP 在 DAP-Test 基准上大幅超越 DAC 和 Unik3D，AbsRel 分别降低 0.2416 和 0.1736，δ1 分别提升 0.4177 和 0.3284。
- 消融实验证实，失真图、几何损失（L_normal, L_pts）和清晰度损失（L_DF, L_grad）的叠加能持续提升性能，且可插拔范围掩码头有效过滤不可靠远距预测。
---

# Depth Any Panoramas: A Foundation Model for Panoramic Depth Estimation

> [!tip] 核心洞察
> 通过融合大规模标注和伪标注全景数据，采用渐进式伪标签精炼训练管线，并设计几何一致性（法线、点云损失）与清晰度导向（密集保真度、梯度损失）的优化目标，可构建一个在室内外场景均具有强零样本泛化能力的全景深度基础模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 深度任意全景图：一个全景深度估计的基础模型 |
| 英文题名 | Depth Any Panoramas: A Foundation Model for Panoramic Depth Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16913) · [Project](https://insta360-researchteam.github.io/DAP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DAP (Depth Any Panoramas) |
| Dataset | DAP-Test |

> [!tip] 效果简介
> - DAP-Test 上，AbsRel 0.0781 vs 0.3197 (DAC) (-0.2416)；RMSE 6.804 vs 8.799 (DAC) (-1.995)；δ1 0.9370 vs 0.5193 (DAC) (+0.4177)。

## 概要

全景深度估计旨在从单张 360° 等距柱状投影（ERP）图像中恢复稠密的度量深度，是三维场景理解与沉浸式视觉应用的基础任务。然而，现有方法面临一个根本性瓶颈：**全景深度估计数据集规模有限且缺乏多样性**，导致模型难以泛化到真实世界室外场景，尤其在远距离和复杂几何区域表现脆弱。本文提出 **DAP（Depth Any Panoramas）**，一个面向全景深度估计的基础模型，其核心洞察在于：通过构建大规模多域数据引擎，并设计渐进式伪标签精炼训练管线，同时引入几何一致性与清晰度导向的多损失优化，可显著提升模型在室内外场景下的零样本泛化能力。

DAP 的方法定位可从四个关键维度理解：

- **数据规模与域覆盖**：DAP 数据引擎构建了约 2M 样本的全景数据集，覆盖合成/真实与室内/室外四个域（Table 1），远超先前方法（如 PanDA、Unik3D、DAC）的领域特定有限数据（<1M），为模型提供了统一且全面的数据基础。

- **训练管线设计**：采用三阶段渐进式伪标签精炼策略（Figure 2）。阶段一在高质量合成数据上训练“场景不变标注器”，为真实无标注数据生成初始伪标签；阶段二引入“真实感不变标注器”，利用 PatchGAN 判别器筛选高置信度伪标签（室内/室外各 30 万），弥合合成与真实域差距；阶段三在所有标注与伪标注数据上联合训练最终 DAP 模型，实现大规模半监督学习。

- **网络架构**：以 **DINOv3-Large** 为视觉骨干，配合失真感知深度解码器与可插拔范围掩码头（支持 10/20/50/100 m 距离阈值），自适应过滤不可靠远距区域（Figure 3）。

- **损失函数体系**：在标准 SILog 损失基础上，叠加失真图补偿 ERP 非均匀像素密度，并引入几何损失（法线损失 $L_{normal}$ 与点云损失 $L_{pts}$）和清晰度损失（密集保真度损失 $L_{DF}$ 与梯度损失 $L_{grad}$），从表面法向、三维点云、Gram 矩阵结构相似度和边缘清晰度等多层次约束深度预测。

实验结果表明，DAP 在 DAP-Test 基准上大幅超越度量深度基线 **DAC**（Guo et al., CVPR 2025）和 **Unik3D**（Piccinelli et al., CVPR 2025）：AbsRel 分别降低 0.2416 和 0.1736，δ1 分别提升 0.4177 和 0.3284（Table 4）。消融实验证实，失真图、几何损失和清晰度损失的叠加能持续累积增益，范围掩码头可有效滤除不可靠远距预测并稳定训练（Table 5, Table 6）。在 Stanford2D3D 和 Deep360 等基准上的零样本测试中，DAP 同样取得最优结果，验证了大规模数据缩放与域一致性训练的有效性。



全景深度估计旨在从 360° 等距柱状投影（ERP）图像中恢复稠密的度量深度信息，是三维场景理解、虚拟现实与自动驾驶等应用的基础任务。然而，该领域长期受制于一个核心瓶颈：**现有全景深度估计数据集规模有限且缺乏多样性，模型难以泛化到真实世界室外场景，特别是远距离和复杂几何区域**。此前方法（如 **PanDA**（Cao et al., CVPR 2025）、**DAC**（Guo et al., CVPR 2025）、**Unik3D**（Piccinelli et al., CVPR 2025））所依赖的训练数据通常局限于单一域或特定场景，数据量远低于百万级（见 Table 1），导致模型在面对未见过的真实室外全景时性能急剧退化。

从因果机制来看，全景深度估计的性能瓶颈并非仅在于模型架构设计，更深层的原因在于**数据规模与域覆盖的不足**直接限制了模型的零样本泛化能力。合成数据虽然易于获取精确深度真值，但与真实图像之间存在显著的域差距；真实全景数据虽然场景丰富，但深度标注成本极高，难以大规模获取。这一矛盾构成了全景深度估计走向“基础模型”级泛化能力的关键障碍。

本文的核心动机即在于打破上述数据与泛化之间的因果僵局。作者提出 **DAP（Depth Any Panoramas）**，通过构建一个包含约 200 万样本、覆盖合成/真实与室内/室外四个域的大规模数据引擎（DAP-2M），从根本上扩大数据规模与多样性。在此基础上，设计三阶段渐进式伪标签精炼管线，逐步弥合合成–真实与室内–室外的域差距，并辅以几何一致性（法线损失、点云损失）与清晰度导向（密集保真度损失、梯度损失）的多损失优化策略，最终实现一个在室内外场景均具有强零样本泛化能力的全景深度基础模型。

> **需手动验证**：本文未明确引用全景深度估计在自动驾驶等具体下游任务中的定量需求分析，相关应用背景描述需结合原文 Introduction 部分进一步确认。



## 核心方法与创新机理

DAP 的核心创新并非单一算法突破，而是围绕 **数据规模瓶颈** 与 **多域泛化鸿沟** 构建的系统性解法：通过大规模多域数据引擎、三阶段渐进式伪标签精炼管线，以及几何与清晰度感知的多损失优化，首次将全景深度估计推向“基础模型”级别的零样本泛化能力。

### 关键改进槽位

相较于 DAC（Guo et al., CVPR 2025）、Unik3D（Piccinelli et al., CVPR 2025）等近期工作，DAP 在以下四个关键维度实现了根本性改变：

| 改进槽位 | 基线方案 | DAP 方案 | 改进逻辑 |
|:---|:---|:---|:---|
| **训练数据规模与域覆盖** | 领域特定有限数据（<1M 样本） | DAP-2M 数据引擎：约 2M 样本，覆盖合成/真实 × 室内/室外四域 | 直接突破全景深度数据匮乏的核心瓶颈，为模型提供足够的场景多样性与几何复杂性 |
| **视觉骨干网络** | 标准卷积网络或较小 ViT | DINOv3-Large 预训练骨干 | 利用大规模预训练视觉先验，增强对未见场景的特征提取鲁棒性 |
| **损失函数组合** | 仅 SILog 损失 | SILog + 失真图补偿 + 几何损失（$\mathcal{L}_{normal}$, $\mathcal{L}_{pts}$）+ 清晰度损失（$\mathcal{L}_{DF}$, $\mathcal{L}_{grad}$）+ 掩码损失 | 从单一尺度不变监督升级为多层级几何一致性与结构清晰度联合约束 |
| **范围掩码机制** | 无 | 可插拔双头范围掩码，支持 10/20/50/100 m 距离阈值 | 滤除远距离不可靠预测区域，稳定训练并提升整体指标 |

### 创新一：大规模多域数据引擎

全景深度估计长期受困于数据规模与多样性不足——现有数据集或局限于室内合成场景，或仅覆盖特定室外环境。DAP 的数据引擎从四个维度统一数据来源（合成/真实 × 室内/室外），构建了约 2M 样本的全景数据集（Table 1）。其中，室内 500K、室外 1.5M，合成数据 300K、真实数据 1.7M。这一规模远超 PanDA、Unik3D、DAC 等方法所使用的数据体量，为模型学习跨域泛化的深度表征提供了基础。

### 创新二：三阶段渐进式伪标签精炼

单纯扩大数据规模不足以解决合成到真实、室内到室外的域鸿沟。DAP 设计了三级递进训练管线（Figure 2）：

- **阶段一（场景不变标注器）**：在高品质合成室内/室外数据上训练初始模型，为真实无标注数据生成初始伪深度标签，建立跨场景的几何先验。
- **阶段二（真实感不变标注器）**：引入 PatchGAN 判别器，从伪标签中筛选高置信度样本（室内/室外各 30 万），再训练模型以弥合合成与真实之间的真实感差异。
- **阶段三（DAP 最终训练）**：在所有标注与伪标注数据上联合训练，实现大规模半监督学习。

这一管线通过逐步缩小域差距，使得最终模型能够在未见过的真实场景中保持度量一致性与几何合理性。

### 创新三：几何与清晰度感知的多损失优化

DAP 的损失函数设计（Equation 6）从三个层次约束深度预测质量：

1. **失真图补偿**：引入失真图 $M_{distort}$ 对各损失项加权，补偿等距柱状投影（ERP）造成的非均匀像素密度，确保两极区域与赤道区域获得平衡的梯度贡献。
2. **几何一致性损失**：$\mathcal{L}_{normal}$（Equation 4）约束表面法向量的 L1 误差，$\mathcal{L}_{pts}$（Equation 5）约束球形 3D 点云的 L1 误差，二者在三维空间直接强化几何结构一致性。
3. **清晰度导向损失**：$\mathcal{L}_{DF}$（Equation 2）通过 12 个透视视图的 Gram 矩阵相似度增强局部清晰度与结构保真度；$\mathcal{L}_{grad}$（Equation 3）仅作用于 Sobel 边缘掩码区域，提升物体边界的锐度。

消融实验（Table 5）证实，在 SILog 基线之上逐步叠加失真图、几何损失和清晰度损失，Stanford2D3D 和 Deep360 上的 AbsRel 与 δ1 持续改善，各分量对性能均有累积增益。

### 创新四：可插拔范围掩码机制

全景场景的深度分布极不均匀——近处物体需要高精度度量，而远处天空区域往往无有效深度约束。DAP 设计了轻量级的范围掩码头，预测二值掩码 $M$，通过 Equation 1 的加权 BCE 与 Dice 损失进行监督。该掩码与度量深度头的输出逐元素相乘，以可插拔方式滤除超出距离阈值的不可靠区域。消融实验（Table 6）表明，采用 100 m 阈值的范围掩码在 DAP-2M-Labeled 和 Deep360 上取得最优综合指标；移除该模块则性能显著下降，验证了其对训练稳定性和远距预测质量的关键作用。



DAP 的整体框架围绕三个核心组件构建：**大规模多域数据引擎**、**渐进式三阶段训练管线**和**几何与清晰度感知的网络架构**。Figure 2 给出了三阶段管线的完整概览，Figure 3 展示了网络架构的详细设计。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed progressive three-stage pipeline. Stage 1 trains a Scene-Invariant Labeler on high-quality synthetic indoor and outdoor data to provide strong initialization. Stage 2 introduces a Realism-Invariant Labeler, where a PatchGAN-based discriminator selects 300K indoor and 300K outdoor high-confidence pseudo-labeled samples to mitigate domain gaps between synthetic and real data. Stage 3 performs DAP training on all labeled and pseudo-labeled data, enabling large-scale semi-supervised learning and strong generalization across real-world panoramic scenes*

### 数据引擎：DAP-2M

数据引擎是整个框架的基础。与先前方法依赖领域特定、规模有限的训练集不同，DAP 的数据引擎统一了合成与真实、室内与室外四个域的全景数据源，构建了约 **2M 样本**的大规模全景数据集（Table 1）。其中包含约 500K 室内和 1.5M 室外全景，合成数据约 300K，真实世界数据约 1.7M。这一数据规模与域覆盖远超 **DAC**（Guo et al., CVPR 2025）、**Unik3D**（Piccinelli et al., CVPR 2025）和 **PanDA**（Cao et al., CVPR 2025）等先前方法，为全景深度基础模型的训练提供了统一且全面的数据基础（Sec 3.1）。

### 三阶段渐进式训练管线

为有效利用大规模标注与无标注数据，DAP 采用渐进式三阶段训练策略（Figure 2）：

- **阶段1 — 场景不变标注器**：在高品质合成室内/室外数据上训练初始模型，为真实无标注数据生成初始伪深度标签，提供强初始化。
- **阶段2 — 真实感不变标注器**：引入 PatchGAN 判别器，从阶段1生成的伪标签中筛选高置信度样本（各 30 万室内/室外），再训练模型以弥合合成与真实数据之间的域差距。
- **阶段3 — DAP 最终训练**：在所有标注和伪标注数据上联合训练最终模型，实现大规模半监督学习。

这一管线逐步弥合合成–真实与室内–室外的域差距，是模型获得强零样本泛化能力的关键因果机制。

### 网络架构与输入输出流

DAP 网络（Figure 3）以单张全景图像为输入，由以下模块组成流水线式处理：

1. **视觉骨干网络**：采用 **DINOv3-Large** 预训练编码器提取强大视觉特征，替代先前方法中常用的标准卷积网络或较小 ViT。
2. **失真感知深度解码器**：结合失真图 $M_{distort}$ 适应等距柱状投影（ERP）的非均匀像素分布，将编码器特征解码为深度表示。
3. **双头输出**：
   - **度量深度头**：预测稠密度量深度图 $D$。
   - **范围掩码头**：预测二值掩码 $M$，支持 10/20/50/100 m 等可配置距离阈值，以可插拔方式滤除超出阈值的不可靠远距区域。
4. **最终输出**：深度图与掩码逐元素相乘 $M \odot D$，得到最终度量深度估计。

### 多损失优化目标

训练由多层级损失函数联合驱动（Eq 6），总损失为各损失项的加权组合，并引入失真图 $M_{distort}$ 补偿 ERP 投影的非均匀像素密度：

$$\mathcal{L}_{total} = M_{distort} \odot \left( \lambda_1 \mathcal{L}_{SILog} + \lambda_2 \mathcal{L}_{DF} + \lambda_3 \mathcal{L}_{grad} + \lambda_4 \mathcal{L}_{normal} + \lambda_5 \mathcal{L}_{pts} + \lambda_6 \mathcal{L}_{mask} \right)$$

其中：
- $\mathcal{L}_{SILog}$：尺度不变对数损失，保证度量一致性；
- $\mathcal{L}_{DF}$：密集保真度损失（Eq 2），基于 12 个透视视图的 Gram 矩阵相似度增强局部清晰度；
- $\mathcal{L}_{grad}$：梯度损失（Eq 3），仅作用于 Sobel 边缘掩码区域，提升物体边界清晰度；
- $\mathcal{L}_{normal}$：法线损失（Eq 4），预测与真实表面法向量的 L1 损失，增强几何一致性；
- $\mathcal{L}_{pts}$：点云损失（Eq 5），直接在三维球面坐标空间强化几何一致性；
- $\mathcal{L}_{mask}$：掩码损失（Eq 1），加权 BCE 与 Dice 损失监督范围掩码预测。

损失权重设置为 $\lambda_1 = 1.0$，$\lambda_2 = 0.4$，$\lambda_3 = 5.0$，$\lambda_4 = 2.0$，$\lambda_5 = 2.0$，$\lambda_6 = 2.0$。消融实验（Table 5）证实，从仅使用 $\mathcal{L}_{SILog}$ 的基线出发，逐步叠加失真图、几何损失和清晰度损失，在 Stanford2D3D 和 Deep360 上均取得持续的性能增益，验证了各损失分量的累积贡献。



DAP 的核心架构由三个关键模块构成：**失真感知深度解码器**、**可插拔范围掩码头**与**度量深度头**，并通过多层级几何与清晰度感知损失函数进行联合优化。以下逐一剖析各模块的设计逻辑与公式含义。

---

### 失真感知深度解码器

等距柱状投影（ERP）在全景图像中引入严重的非均匀像素密度——两极区域像素被过度拉伸，赤道区域相对压缩。为补偿这一畸变，DAP 在解码器中引入**失真图** $M_{distort}$，对损失函数进行逐像素加权，使网络在训练时对畸变区域的梯度贡献进行平衡。该机制并非独立的网络模块，而是贯穿于总损失计算之中（见式 (6)），确保优化过程对 ERP 投影的几何特性具有感知能力。

---

### 可插拔范围掩码头

全景深度估计的核心挑战之一是远距离区域深度值高度不确定，直接预测会引入大量噪声并导致训练不稳定。DAP 采用一个轻量级的**范围掩码头**，以可插拔方式预测二值掩码 $M$，用于标识可靠深度区域：

$$ \mathcal{L}_{mask} = \|M - M_{gt}\|^2 + 0.5 \mathcal{L}_{Dice}(M, M_{gt}) $$

其中 $M_{gt}$ 为根据距离阈值（支持 10/20/50/100 m）生成的真值掩码，$\mathcal{L}_{Dice}$ 为 Dice 损失。该头采用加权二值交叉熵与 Dice 损失的组合进行监督，使网络学会自动过滤超出阈值的不可靠区域。消融实验证实，移除该模块会导致性能显著下降，而 100 m 阈值在 DAP-2M-Labeled 和 Deep360 上取得最优综合指标（AbsRel 0.0793 / 0.0862，δ1 0.9353 / 0.8719），证明其有效滤除不可靠远距预测并稳定训练。

---

### 度量深度头

度量深度头预测稠密的度量深度图 $D$，并与范围掩码 $M$ 逐元素相乘得到最终输出 $\hat{D} = M \odot D$。该设计使模型能够显式区分“可预测区域”与“应屏蔽区域”，避免在不可靠区域上施加错误的深度监督。

---

### 多层级损失函数

DAP 的优化目标由六项损失加权组合而成，从尺度一致性、几何结构到边界清晰度逐层约束：

#### 1. 尺度不变对数损失（SILog）

作为度量深度估计的基础损失，$\mathcal{L}_{SILog}$ 对绝对尺度误差具有不变性，是全景深度估计的通用基线。

#### 2. 密集保真度损失

$$ \mathcal{L}_{DF} = \frac{1}{N} \sum_{k=1}^{N} \left\| \left(D_{pred}^{(k)} \odot D_{pred}^{(k)}\right)^{\top} - D_{gt}^{(k)} \odot D_{gt}^{(k)} \right\|_F^2 $$

该损失基于 **12 个透视视图**的 Gram 矩阵相似度：将全景深度图投影到 12 个不同方向的透视视图，计算各视图深度图的 Gram 矩阵（$D \odot D^{\top}$），并约束预测与真值 Gram 矩阵的 Frobenius 范数差异。Gram 矩阵编码了深度图内部的局部结构相关性，因此该损失能有效增强深度图的**局部清晰度与结构一致性**。

#### 3. 梯度损失

$$ \mathcal{L}_{grad} = \mathcal{L}_{SILog}(M_E \odot D_{pred}, M_E \odot D_{gt}) $$

该损失**仅作用于边缘掩码区域** $M_E$——通过 Sobel 算子提取深度图的梯度幅值并筛选出高梯度边缘像素。在边缘区域施加 SILog 损失，可针对性地提升**物体边界的清晰度**，避免平滑区域过度约束导致边界模糊。

#### 4. 法线损失

$$ \mathcal{L}_{normal} = \| \mathbf{n}_{pred}(i,j) - \mathbf{n}_{gt}(i,j) \|_1 $$

从深度图计算表面法向量 $\mathbf{n}$，并约束预测法线与真值法线的 L1 距离。该损失在**表面几何一致性**层面提供监督，使预测深度图的局部表面朝向与真实几何对齐。

#### 5. 点云损失

$$ \mathcal{L}_{pts} = \|\mathbf{P}_{pred}(i,j) - \mathbf{P}_{gt}(i,j)\|_1 $$

将全景深度图反投影至**球形 3D 点云** $\mathbf{P}$，直接在三维坐标空间约束 L1 距离。与法线损失互补，点云损失在**全局三维结构**层面强化几何一致性，对远距离区域的深度精度尤为重要。

#### 6. 总损失

$$ \mathcal{L}_{total} = M_{distort} \odot \left( \lambda_1 \mathcal{L}_{SILog} + \lambda_2 \mathcal{L}_{DF} + \lambda_3 \mathcal{L}_{grad} + \lambda_4 \mathcal{L}_{normal} + \lambda_5 \mathcal{L}_{pts} + \lambda_6 \mathcal{L}_{mask} \right) $$

所有损失项通过失真图 $M_{distort}$ 加权后求和。超参数设置为 $\lambda_1 = 1.0$，$\lambda_2 = 0.4$，$\lambda_3 = 5.0$，$\lambda_4 = 2.0$，$\lambda_5 = 2.0$，$\lambda_6 = 2.0$。消融实验证实，在仅使用 $\mathcal{L}_{SILog}$ 的基线基础上逐步叠加失真图、几何损失（$\mathcal{L}_{normal}$、$\mathcal{L}_{pts}$）和清晰度损失（$\mathcal{L}_{DF}$、$\mathcal{L}_{grad}$），在 Stanford2D3D 和 Deep360 上分别取得最佳 AbsRel（0.1084 / 0.0862）和 δ1（0.8576 / 0.8719），各损失分量对性能均有累积增益。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/004_Figure_3.jpg]]
*Figure 3: Architecture of the proposed DAP network. Built upon DINOv3-Large [38] as the visual backbone, our model adopts a distortion-aware depth decoder and a plug-and-play range mask head for adaptive distance control across diverse scenes. Training is guided by multi-level geometric and sharpness-aware losses, including*



## 实验与关键发现

DAP 的实验评估围绕三个层次展开：零样本泛化能力、DAP-Test 基准上的综合性能，以及各设计组件的消融贡献。所有实验均采用 DINOv3-Large 作为统一视觉骨干并进行完全微调，以排除外部视觉先验对公平性的干扰。

### 零样本泛化评估

DAP 在 Stanford2D3D、Matterport3D 和 Deep360 三个基准上进行了零样本度量深度估计测试，与当前主流方法进行对比（Table 3）。结果表明，DAP 在所有数据集上均取得最优性能，且无需针对目标域进行任何微调。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/008_Table_3.jpg]]
*Table 3: Zero-shot comparison of panoramic metric depth estimation on three benchmarks. The best and second best metric depth performances are highlighted. Our DAP consistently achieves the best results across all datasets, demonstrating strong generalization without fine-tuning. We also include several scale-invariant methods only for reference from DA2 [25]*

在室内场景 Stanford2D3D 上，DAP 的 AbsRel 达到 0.0921，RMSE 为 0.3820，δ1 为 0.9135；在 Matterport3D 上，AbsRel 为 0.1186，RMSE 为 0.7510，δ1 为 0.8518。在室外场景 Deep360 上，DAP 同样表现突出，AbsRel 低至 0.0659，RMSE 为 5.224，δ1 高达 0.9525。这一跨域一致性验证了大规模多域数据引擎与三阶段训练管线对泛化能力的关键支撑。

### DAP-Test 基准对比

为系统评估全景深度估计在真实世界复杂场景下的表现，作者构建了 DAP-Test 基准。Table 4 的定量对比显示，DAP 在所有指标上均大幅超越现有度量深度方法。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/009_Table_4.jpg]]
*Table 4: Quantitative comparison on the proposed DAP-Test benchmark. Our DAP achieves the best performance across all metrics, demonstrating the effectiveness of large-scale data scaling and domain-consistent training*

与 **DAC**（Guo et al., CVPR 2025）相比，DAP 的 AbsRel 从 0.3197 降至 0.0781，降幅达 0.2416；RMSE 从 8.799 降至 6.804；δ1 从 0.5193 提升至 0.9370，提升 0.4177。与 **Unik3D**（Piccinelli et al., CVPR 2025）相比，AbsRel 从 0.2517 降至 0.0781，RMSE 从 10.56 降至 6.804，δ1 从 0.6086 提升至 0.9370。这些结果表明，DAP 的数据规模化与域一致性训练策略在真实世界全景深度估计中具有显著优势。

定性对比（Figure 4、Figure 5）进一步印证了定量结果：DAP 在物体边界清晰度、全局几何平滑性以及远距离和天空区域的鲁棒性方面均优于 DAC 和 Unik3D，在 Stanford2D3D 上能更好地保留细粒度结构细节并展现优越的尺度感知能力。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison across diverse real-world indoor and outdoor scenes. Our DAP produces sharper object boundaries, smoother global geometry, and superior robustness in distant and sky regions compared to DAC [15] and Unik3D [32]*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison on Stanford2D3D. Our method preserves fine structural details and demonstrates superior scaleawareness*

### 消融实验

消融实验从模型组件和范围掩码配置两个维度展开，揭示了各设计选择的因果贡献。

**模型组件消融（Table 5）**。以仅使用 SILog 损失的配置作为基线，逐步叠加失真图、几何损失（$\mathcal{L}_{normal}$、$\mathcal{L}_{pts}$）和清晰度损失（$\mathcal{L}_{DF}$、$\mathcal{L}_{grad}$）。实验在 Stanford2D3D 和 Deep360 上分别进行。结果显示，各损失分量的叠加带来持续的性能增益：失真图的引入改善了等距柱状投影下的优化稳定性；几何损失增强了结构一致性；清晰度损失则提升了局部细节保真度。最终完整配置在两个数据集上分别取得最佳 AbsRel（0.1084 / 0.0862）和最佳 δ1（0.8576 / 0.8719），证实了多损失联合优化的累积效应。

**范围掩码消融（Table 6）**。可插拔范围掩码头支持 10 m、20 m、50 m、100 m 四种距离阈值。实验在 DAP-2M-Labeled 和 Deep360 上进行。采用 100 m 阈值时取得最优综合指标（AbsRel 0.0793 / 0.0862，δ1 0.9353 / 0.8719）；去除范围掩码后性能显著下降。这表明范围掩码头能够有效滤除不可靠的远距离预测区域，同时起到稳定训练的作用。

### 训练配置

所有实验采用 Adam 优化器，视觉骨干学习率为 $5 \times 10^{-6}$，解码器学习率为 $5 \times 10^{-5}$。总损失函数中各权重系数 $\lambda_1$ 至 $\lambda_6$ 分别设置为 1.0、0.4、5.0、2.0、2.0、2.0，以平衡不同损失项的梯度贡献。

### 数据规模与多样性分析

Table 1 对比了 DAP 与以往全景深度估计方法的训练数据构成。DAP 数据引擎构建了约 2M 样本的全景数据集，涵盖室内（500K）与室外（1.5M）、合成（300K）与真实（1.7M）四个域，远超 PanDA、Unik3D、DAC 等方法的数据规模与域覆盖范围。Table 2 进一步列出了训练所涉及的具体数据集及其标注状态。这一数据基础是 DAP 实现强零样本泛化的根本前提。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/002_Table_1.jpg]]
*Table 1: Comparison of training data compositions used by recent panoramic depth estimation methods. Unlike previous approaches, which rely on limited or domain-specific datasets, our DAP data engine scales up to 2M panoramas across both indoor/outdoor and synthetic/real domains, providing a unified and comprehensive data foundation for panoramic depth modeling. * in DA2 refers to pseudo-panoramic data generated from perspective images through P2E projection and out-painting model*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/005_Table_2.jpg]]
*Table 2: Overview of datasets used for training DAP, covering synthetic and real, labeled and unlabeled panoramic data*

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/010_Table_5.jpg]]
*Table 5: Ablation study on the proposed components. The best and second best performances are highlighted*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/011_Table_6.jpg]]
*Table 6: Ablation on the range mask head (m). The best and second best results are highlighted*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2512_16913/figures/001_Figure_1.jpg]]
*Figure 1: Metric depth visualizations generated by DAP from diverse panoramic inputs. For clarity, each depth map is displayed using its own adaptive truncation range. DAP achieves robust, metrically consistent panoramic depth across diverse real-world scenes, highlighting the power of large-scale data and model designing*



## 定位与知识库关联

### 全景深度估计的技术演进

全景深度估计经历了从**受限场景**到**开放世界泛化**的范式迁移。早期工作主要依赖特定领域的有限标注数据，在室内或室外单一场景下训练，泛化能力严重受限。**DAP** 的出现标志着该领域向基础模型范式的重要转向。

**尺度不变方法**：以 **PanDA**（Cao et al., CVPR 2025）为代表，采用无监督学习策略，输出尺度不变的相对深度。这类方法无需度量真值即可训练，但在需要真实物理尺度的下游任务（如三维重建、机器人导航）中适用性受限。DAP 将其作为参考基线，而非直接竞争对手。

**度量深度方法**：**DAC**（Guo et al., CVPR 2025）通过统一相机几何实现度量深度估计，在室内场景表现较好，但受限于训练数据的域覆盖范围，在室外远距离区域和复杂几何结构上性能退化明显。**Unik3D**（Piccinelli et al., CVPR 2025）采用球面坐标进行通用深度估计，试图弥合不同投影方式的差异，但其训练数据规模（<1M）和域多样性仍不足以支撑强零样本泛化——在 DAP-Test 基准上，Unik3D 的 AbsRel 高达 0.2517，而 DAP 仅为 0.0781。

### DAP 的方法定位与核心差异化

DAP 并非在现有方法框架内进行增量改进，而是从**数据规模**和**训练范式**两个维度进行了系统性重构：

| 维度 | 先前方法 | DAP |
|------|----------|-----|
| 数据规模 | <1M 样本，域特定 | ~2M 样本，四域覆盖 |
| 训练策略 | 单阶段监督学习 | 三阶段渐进式伪标签精炼 |
| 视觉骨干 | 标准 CNN 或较小 ViT | DINOv3-Large 预训练骨干 |
| 几何约束 | SILog 损失为主 | 几何+清晰度多损失联合优化 |
| 远距处理 | 无专门机制 | 可插拔范围掩码头 |

**数据环路的突破**：DAP 的数据引擎（Table 1）统一了合成室内、合成室外、真实室内、真实室外四个域，构建了约 2M 样本的全景数据集。这一规模远超 PanDA、Unik3D、DAC 等先前方法使用的领域特定有限数据（通常 <1M），为模型的零样本泛化提供了数据基础。

**训练范式的创新**：三阶段流水线（Figure 2）通过场景不变标注器→真实感不变标注器→最终联合训练的递进策略，逐步弥合合成-真实与室内-室外的域差距。其中 PatchGAN 判别器筛选高置信度伪标签（各 30 万室内/室外）的机制，是大规模半监督学习中质量控制的关键设计。

**损失函数的多层次设计**：DAP 的损失函数组合（Eq 6）从三个层次约束深度预测质量——SILog 损失保证度量一致性，几何损失（$\mathcal{L}_{normal}$、$\mathcal{L}_{pts}$）增强三维结构合理性，清晰度损失（$\mathcal{L}_{DF}$、$\mathcal{L}_{grad}$）提升局部细节保真度。消融实验（Table 5）证实，各损失分量的叠加带来累积增益：在 Stanford2D3D 上，仅使用 SILog 损失的基线 AbsRel 为 0.1185，叠加全部损失后降至 0.1084。

### 适用边界与局限

**强适用场景**：DAP 在室内外真实场景的零样本全景深度估计中表现优异，尤其擅长处理远距离区域和复杂几何结构。DAP-Test 基准上的 δ1 达到 0.9370，相比 DAC（0.5193）提升 0.4177，表明其在度量一致性上的显著优势。

**潜在局限**：范围掩码头虽然有效滤除不可靠远距预测（Table 6 消融证实），但其距离阈值（10/20/50/100 m）需要根据场景预设，缺乏完全自适应的阈值选择机制。此外，三阶段训练管线虽然效果显著，但训练流程的复杂性高于单阶段方法，可能增加复现和部署成本。

### 开放问题与后续方向

DAP 为全景深度估计的基础模型范式奠定了数据和方法论基础，但以下方向仍待探索：

1. **动态场景扩展**：当前 DAP 主要面向静态场景，如何将大规模数据引擎和伪标签精炼策略扩展到包含运动物体的动态全景视频深度估计，是一个自然的延伸方向。

2. **自适应范围控制**：范围掩码头的距离阈值目前需手动预设，开发基于场景内容的自适应阈值选择机制，可进一步提升模型的自动化程度和边缘场景的鲁棒性。

3. **跨任务迁移**：DAP 学习到的全景几何先验能否迁移到全景语义分割、全景三维重建等相关任务，值得系统验证。DINOv3-Large 骨干的强视觉先验为此类迁移提供了潜在基础。

4. **数据引擎的持续扩展**：当前 DAP 数据引擎覆盖四个域，进一步纳入更多样化的真实世界场景（如极端光照、恶劣天气）和更多传感器模态（如 LiDAR 稀疏深度），有望持续提升模型的泛化边界。



## 原文 PDF

![[paperPDFs/CVPR_2026/Depth_Any_Panoramas_A_Foundation_Model_for_Panoramic_Depth_Estimation.pdf]]

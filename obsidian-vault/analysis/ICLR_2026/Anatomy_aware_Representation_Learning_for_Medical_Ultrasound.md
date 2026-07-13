---
title: "Anatomy-aware Representation Learning for Medical Ultrasound"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Anatomy_aware_Representation_Learning_for_Medical_Ultrasound.pdf
project_link: null
code_link: null
aliases:
- AARLA
- AARLMU
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: |
  通过解剖条件可变形Transformer将16类解剖上下文注入ViT注意力，并联合MIM、对抗性损失和自蒸馏损失进行超声自监督表示学习。
primary_logic: |
  先用解剖类别嵌入生成条件特征作为注意力key/value，使patch query按器官上下文自适应提取特征，再用局部重建、高频散斑保留和全局语义对齐的多目标训练获得可迁移超声表示。
claims:
- "ARL在5.2M张超声图像和16个解剖类别上预训练A-ViT，学习器官感知表示。"
- "在BUSI乳腺癌分类上，A-ViT微调准确率达到93.66%，AUROC达到0.9742。"
- "消融结果显示ACDT、对抗性损失、自蒸馏损失和自适应加权共同提升乳腺癌分类性能。"
---

# Anatomy-aware Representation Learning for Medical Ultrasound

> [!tip] 核心洞察
> 通过将解剖上下文显式注入Vision Transformer的注意力机制（ACDT中解剖条件特征作为key/value，原始patch作为query），并结合掩码图像建模、对抗性损失（保留高频散斑）和自蒸馏损失（全局语义对齐）的多目标自监督学习框架，ARL能够学习到器官感知且泛化性强的超声图像表示。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向医学超声的解剖感知表示学习 |
| 英文题名 | Anatomy-aware Representation Learning for Medical Ultrasound |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5ThIWuDkEf) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Anatomy-aware Representation Learning (ARL) |
| Dataset | Breast Cancer (BUSI), Thyroid Cancer |

> [!tip] 效果简介
> - Breast Cancer (BUSI) 上，Accuracy 为 93.66，对比 90.85 (iBOT on US)，变化 +2.81。
> - Breast Cancer (BUSI) 上，AUROC [CI] 为 0.9742 (0.95,0.99)，对比 0.9662 (iBOT on US)，变化 +0.008。
> - Thyroid Cancer 上，Accuracy 为 87.07，对比 85.77 (USFM)，变化 +1.30。

## 概要

本文提出**Anatomy-aware Representation Learning (ARL)**，一个专门为医学超声图像设计的自监督表示学习框架。ARL的核心是**Anatomy-aware Vision Transformer (A-ViT)**，它通过引入**解剖条件可变形Transformer (ACDT)**模块，将16种解剖类别的先验知识显式注入特征提取过程，使模型能够根据目标器官自适应调整感受野和特征提取策略。ARL在大规模医学超声数据集（520万张图像，16个解剖类别，来自11个公开数据集和15家医疗机构）上进行自监督预训练，联合使用掩码图像建模（MIM）、对抗性损失和自蒸馏损失进行多目标优化。在下游任务中，A-ViT在乳腺癌分类（93.66%准确率，0.9742 AUROC）、心脏视图分类（91.80% Top-1准确率）、甲状腺癌分类（87.07%准确率）、COVID-19识别（91.44%准确率）、胆囊肿瘤分类（89.89%准确率）和心脏左心室分割（92.16 Dice）等六个任务上均显著超越现有自监督基线方法。

### 2.1 医学超声图像与自然图像的差异

医学超声图像具有与自然图像显著不同的特性（Figure 1(a)）：
- **散斑噪声（speckle noise）**：超声图像特有的相干噪声模式，包含重要的组织微结构信息。
- **灰度低变化（gray-scale with low color variation）**：缺乏自然图像丰富的色彩信息。
- **器官特异性图像属性（anatomy-specific image attributes）**：不同解剖部位（如乳腺、甲状腺、心脏）具有截然不同的纹理、形状和回声模式。

### 2.2 现有方法的不足

现有自监督学习方法（如MAE、DINO、iBOT、MoCo v3、SigLIP2）主要在自然图像（如ImageNet）上预训练，无法有效处理医学超声图像特有的上述属性，导致在下游超声任务中性能不佳。即使是在超声图像上预训练的领域专用方法（如DMAE、USFM），也缺乏对解剖上下文的显式建模。

### 2.3 核心洞察

本文的核心洞察是：**通过将解剖上下文显式注入Vision Transformer的注意力机制，并结合多目标自监督学习框架，可以学习到器官感知且泛化性强的超声图像表示。** 具体而言，ACDT中解剖条件特征作为key/value，原始patch嵌入作为query，使模型能够根据目标器官自适应调整特征提取；同时，联合MIM（局部结构恢复）、对抗性损失（保留高频散斑）和自蒸馏损失（全局语义对齐）的多目标框架，能够全面捕获超声图像的多层次特征。

## 核心方法与创新机理

### 3.1 解剖条件可变形Transformer (ACDT)

ACDT是ARL的核心创新模块，它通过以下方式实现解剖感知的特征提取：

1. **解剖条件编码**：将16种解剖类别编码为one-hot向量，通过可学习的嵌入层投影为解剖上下文表示 $AC \in \mathbb{R}^{B \times C}$。
2. **解剖条件特征生成**：将解剖上下文嵌入与patch嵌入相加，通过可变形卷积生成解剖条件特征 $y_P$。可变形卷积的偏移量 $\Delta p_k$ 由解剖上下文条件决定（公式1）。
3. **可变形注意力**：在多头注意力机制中，解剖条件特征 $y_P$ 作为key和value，原始patch嵌入 $x_P$ 作为query（公式2），实现器官自适应的特征提取。

### 3.2 多目标自监督学习框架

ARL联合优化三个自监督目标：

1. **掩码图像建模（MIM）损失**（公式3）：对掩码patch的均方误差重建损失，学习局部结构特征。
2. **对抗性损失**（公式4）：判别器区分真实patch与重建patch，生成器欺骗判别器，迫使模型保留高频散斑模式。
3. **自蒸馏损失**（公式5）：教师网络与学生网络输出分布之间的交叉熵，学习全局语义表示。

总损失函数（公式6）通过自适应梯度加权平衡MIM和对抗损失：$\lambda = \nabla L_{MIM} / (\nabla L_{adv}^{(G)} + \varepsilon)$。

### 3.3 大规模医学超声数据集

构建了包含520万张图像的大规模医学超声数据集，覆盖16个解剖类别，图像来自线性、凸阵和相控阵探头，分辨率从64×64到1280×960，成像深度达24 cm。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_5ThIWuDkEf_Anatomy/figures/001_Figure_1.jpg]]
*Figure 1: (a) Difference between medical US and natural images. (b) PCA of the features using Dino v3 and the proposed scheme.(c) Distribution of the proposed large-scale US dataset.*

ARL的整体框架（Figure 2）包含以下模块：

1. **Patch Embedding**：将输入超声图像分割为patch并嵌入为向量序列。
2. **解剖条件嵌入**：将16类解剖one-hot编码投影为解剖上下文表示。
3. **ACDT模块**：核心模块，将解剖上下文嵌入与patch嵌入相加，通过可变形卷积生成解剖条件特征，并在多头注意力中将其作为key/value。
4. **MIM Decoder**：重建被掩码的patch区域。
5. **Discriminator**：区分真实patch与重建patch。
6. **Self-Distillation Head**：学生-教师网络跨视图对齐。

### 5.1 可变形卷积（公式1）

$$y_P(p) = \sum_{k=1}^K w_k \cdot S(x_P, p + \Delta p_k)$$

其中 $w_k$ 为核权重，$S$ 为双线性采样，偏移量 $\Delta p_k$ 由解剖上下文条件决定。

### 5.2 可变形注意力（公式2）

$$DeformAttn(x_P, y_P) = Softmax\left( \frac{(x_P W^Q)(y_P W^K)^\top}{\sqrt{d_k}} \right) (y_P W^V)$$

解剖条件特征 $y_P$ 作为key和value，原始patch嵌入 $x_P$ 作为query。

### 5.3 掩码图像建模损失（公式3）

$$L_{MIM} = \frac{1}{|\Omega|} \sum_{i \in \Omega} ||x_i - \hat{x}_i||_2^2$$

### 5.4 对抗性损失（公式4）

判别器：$L_{adv}^{(D)} = -\mathbb{E}_x[\log D(x)] - \mathbb{E}_{\hat{x}}[\log(1 - D(\hat{x}))]$

生成器：$L_{adv}^{(G)} = -\mathbb{E}_{\hat{x}}[\log D(\hat{x})]$

### 5.5 自蒸馏损失（公式5）

$$L_{SD} = -\sum_{i=1}^N z_t^{(i)} \log z_s^{(i)}$$

### 5.6 总自监督损失（公式6）

$$L = L_{SD} + (L_{MIM} + \lambda L_{adv}^{(G)}), \quad \lambda = \frac{\nabla L_{MIM}}{\nabla L_{adv}^{(G)} + \varepsilon}$$

## 实验与关键发现

### 6.1 主要结果

#### 乳腺癌分类（Table 2）

| 方法 | 线性探测准确率 | 微调准确率 | 微调AUROC [CI] |
|------|---------------|------------|----------------|
| MAE (ImageNet) | 72.67 | 83.09 | 0.9123 (0.87,0.95) |
| DINO (ImageNet) | 76.00 | 84.50 | 0.9215 (0.88,0.96) |
| iBOT (ImageNet) | 78.00 | 88.02 | 0.9456 (0.91,0.98) |
| MoCo v3 (ImageNet) | 74.67 | 85.37 | 0.9289 (0.89,0.96) |
| SigLIP2 (ImageNet) | 76.67 | 86.59 | 0.9351 (0.90,0.97) |
| MAE (US) | 78.00 | 89.43 | 0.9523 (0.92,0.98) |
| DINO (US) | 80.00 | 90.14 | 0.9578 (0.93,0.98) |
| iBOT (US) | 81.33 | 90.85 | 0.9662 (0.94,0.99) |
| DMAE (US) | 80.67 | 91.46 | 0.9689 (0.95,0.99) |
| USFM (US) | 82.00 | 92.07 | 0.9701 (0.95,0.99) |
| **A-ViT (Ours)** | **86.62** | **93.66** | **0.9742 (0.95,0.99)** |

#### 多任务评估（Table 4）

| 任务 | 指标 | A-ViT (Ours) | 最佳基线 | 提升 |
|------|------|-------------|----------|------|
| 心脏分割 (EchoNet-Dynamic) | Dice | **92.16** | 91.42 (USFM) | +0.74 |
| 心脏分割 (EchoNet-Dynamic) | mIoU | **85.67** | 84.37 (USFM) | +1.30 |
| 心脏视图分类 | Top-1准确率 | **91.80** | 89.40 (USFM) | +2.40 |
| 心脏视图分类 | Top-3准确率 | **99.22** | 98.93 (USFM) | +0.29 |
| 甲状腺癌分类 | 准确率 | **87.07** | 85.77 (USFM) | +1.30 |
| 甲状腺癌分类 | AUROC [CI] | **0.9475 (0.93,0.96)** | 0.9362 (USFM) | +0.0113 |
| COVID-19识别 | 准确率 | **91.44** | 90.20 (USFM) | +1.24 |
| COVID-19识别 | AUROC [CI] | **0.9714 (0.97,0.98)** | 0.9648 (USFM) | +0.0066 |
| 胆囊肿瘤分类 | 准确率 | **89.89** | 88.05 (USFM) | +1.84 |
| 胆囊肿瘤分类 | AUROC [CI] | **0.9511 (0.93,0.97)** | 0.9384 (USFM) | +0.0127 |

### 6.2 消融实验

#### 损失函数与ACDT的影响（Table 3）

| 配置 | 准确率 | AUROC [CI] |
|------|--------|------------|
| MIM (MAE) | 89.43 | 0.9523 (0.92,0.98) |
| MIM + ACDT | 90.87 | 0.9601 (0.93,0.98) |
| MIM + ACDT + $L_{adv}$ | 92.87 | 0.9689 (0.95,0.99) |
| MIM + ACDT + $L_{SD}$ | 92.96 | 0.9695 (0.95,0.99) |
| MIM + ACDT + $L_{adv}$ + $L_{SD}$ (固定加权) | 92.95 | 0.9701 (0.95,0.99) |
| **MIM + ACDT + $L_{adv}$ + $L_{SD}$ (自适应加权)** | **93.66** | **0.9742 (0.95,0.99)** |

关键发现：
- ACDT模块带来2.79%的准确率提升（从90.87%到93.66%）。
- 对抗性损失带来0.79%的准确率提升（从92.87%到93.66%）。
- 自蒸馏损失带来0.70%的准确率提升（从92.96%到93.66%）。
- 自适应损失加权优于固定加权（93.66% vs 92.95%准确率，0.9742 vs 0.9701 AUROC）（Table 9）。

#### 条件机制对比（Table 8）

| 条件机制 | 准确率 | AUROC [CI] |
|----------|--------|------------|
| Cross-attention | 90.84 | 0.9598 (0.93,0.98) |
| FiLM | 90.14 | 0.9572 (0.93,0.98) |
| LoRA | 92.25 | 0.9675 (0.94,0.99) |
| **ACDT (Ours)** | **93.66** | **0.9742 (0.95,0.99)** |

#### 预训练数据规模的影响（Table 6）

| 预训练数据规模 | 准确率 | AUROC [CI] |
|---------------|--------|------------|
| 5.2M | **93.66** | **0.9742 (0.95,0.99)** |
| 520K | 91.46 | 0.9658 (0.94,0.99) |
| 52K | 87.23 | 0.9353 (0.90,0.97) |

#### 自然图像 vs 超声图像预训练（Table 7）

| 方法 | 自然图像预训练 | 超声图像预训练 |
|------|---------------|---------------|
| MAE | 83.09% | **89.43%** |
| DINO | 84.50% | **90.14%** |
| iBOT | 88.02% | **90.85%** |

### 6.3 可视化分析

- **特征PCA/t-SNE（Figure 3）**：A-ViT在不同超声域上产生比MAE更具判别性和解剖忠实性的特征表示。
- **掩码图像重建对比（Figure 5）**：A-ViT重建的图像保留了超声特有的散斑模式和精细结构细节，而标准MAE重建结果模糊且丢失高频信息。

### 6.4 计算成本（Table 10）

| 模型 | 参数量 | FLOPs | 推理速度 |
|------|--------|-------|----------|
| ViT-B/16 | 86M | 17.58G | 12.1 ms/image |
| **A-ViT (Ours)** | **95M** | **17.66G** | **16.6 ms/image** |

A-ViT仅引入适度的参数和计算开销，同时在下游任务中提供显著提升的解剖感知表示。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_5ThIWuDkEf_Anatomy/figures/003_Table_1.jpg]]
*Table 1: Overview of the downstream datasets.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_5ThIWuDkEf_Anatomy/figures/004_Table_2.jpg]]
*Table 2: Quantitative assessment of breast cancer classification under linear probing and fine-tuning.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_5ThIWuDkEf_Anatomy/figures/005_Table_3.jpg]]
*Table 3: Ablation study on the effect of loss functions and ACDT in breast cancer classification.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_5ThIWuDkEf_Anatomy/figures/007_Table_4.jpg]]
*Table 4: Quantitative assessments of the networks across multiple US downstream tasks.*

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_5ThIWuDkEf_Anatomy/figures/010_Table_5.jpg]]
*Table 5: Summary of ultrasound datasets used for representation learning and downstream applications.*

## 定位与知识库关联

### 7.1 方法谱系

ARL属于**医学图像自监督表示学习**领域，具体位于以下技术交叉点：

1. **掩码自编码器（MAE）**：继承MIM框架，但针对超声图像特性进行改进。
2. **自蒸馏（DINO/iBOT）**：集成自蒸馏损失进行全局语义对齐。
3. **对抗性学习**：引入对抗性损失保留高频散斑信息。
4. **条件计算**：通过解剖条件注入实现器官自适应特征提取。
5. **可变形卷积/注意力**：利用可变形操作实现自适应感受野。

### 7.2 与现有方法的对比

| 维度 | 自然图像SSL (MAE/DINO) | 医学超声SSL (DMAE/USFM) | ARL (本文) |
|------|----------------------|------------------------|------------|
| 预训练数据 | ImageNet | 超声图像 | 大规模超声图像（16类解剖） |
| 解剖感知 | 无 | 无 | 显式解剖条件注入 |
| 高频保留 | 无 | 部分 | 对抗性损失 |
| 多目标学习 | 单一目标 | 单一/双目标 | MIM+对抗+自蒸馏（自适应加权） |

### 7.3 知识库定位

ARL在以下方面填补了医学超声表示学习的空白：
- **数据层面**：构建了目前最大规模的医学超声预训练数据集（5.2M图像，16类解剖）。
- **方法层面**：首次将解剖先验显式注入Vision Transformer的自监督学习框架。
- **评估层面**：在6个下游任务（涵盖分类和分割）上进行了系统评估，展示了方法的通用性。

### 7.4 局限性与开放问题

**局限性**：
- 未报告在自然图像预训练基线上心脏分割、心脏视图分类、甲状腺癌、COVID-19和胆囊肿瘤任务的完整对比结果。
- 未讨论在不同超声设备、探头类型或成像参数下的域迁移能力。
- 未提供在非超声医学影像模态（如CT、MRI）上的迁移实验。
- 未报告模型训练的总计算成本和收敛曲线。
- 未进行统计显著性检验。

**开放问题**：
- ACDT中的可变形卷积偏移量能否学习到有意义的解剖结构对应关系？
- ARL框架能否扩展到CT、MRI等其他医学影像模态？
- 16个解剖类别是否足够覆盖所有超声诊断场景？
- 自适应损失加权中的 $\varepsilon$ 值如何选择？
- ARL在无监督域适应或跨设备泛化场景下的表现如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/Anatomy_aware_Representation_Learning_for_Medical_Ultrasound.pdf]]

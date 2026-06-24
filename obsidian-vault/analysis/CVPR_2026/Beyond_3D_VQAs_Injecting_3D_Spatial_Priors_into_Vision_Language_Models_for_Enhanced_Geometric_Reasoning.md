---
title: "Beyond 3D VQAs: Injecting 3D Spatial Priors into Vision-Language Models for Enhanced Geometric Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_3D_VQAs_Injecting_3D_Spatial_Priors_into_Vision_Language_Models_for_Enhanced_Geometric_Reasoning.pdf
project_link: null
code_link: null
aliases:
- GGASP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 在LLM的Transformer层中注入一个轻量级对应头，利用来自大规模视频场景的真值点对应和深度一致性双重重监督信号，直接训练内部视觉自注意力表示使其具有几何感知能力。
primary_logic: 真正的空间智能应源自对基本几何知觉信号（如视觉对应和深度一致性）的学习，而非高层VQA监督。通过在LLM所有层施加深层几何约束（对应头仅在训练时使用），可以迫使模型形成视角不变的内部表示，为下游空间推理任务提供更通用的基础。
claims:
- 标准VLMs的内部视觉对应匹配准确率极低（通常低于5%），表明其缺少基本的几何感知内部表征。
- 基线的置信度-准确率呈现负相关（ρ ≈ -0.22），是系统性位置偏差的统计特征，预测置信度越高反而对应错误匹配。
- GASP将LLM内部逐层对应匹配的最高准确率提升至70%以上，并维持超过85%的时间稳健性，而基线在超过8帧的时间距离上表现崩溃。
- GASP在未使用任何3D VQA数据训练的情况下，在下游空间推理基准上取得显著提升：All-Angles Bench相机姿态估计提升+18.2%，VSI-Bench物体计数提升+29.0%，BLINK相对深度估计提升+15.0%。
---

# Beyond 3D VQAs: Injecting 3D Spatial Priors into Vision-Language Models for Enhanced Geometric Reasoning

> [!tip] 核心洞察
> 真正的空间智能应源自对基本几何知觉信号（如视觉对应和深度一致性）的学习，而非高层VQA监督。通过在LLM所有层施加深层几何约束（对应头仅在训练时使用），可以迫使模型形成视角不变的内部表示，为下游空间推理任务提供更通用的基础。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越3D视觉问答：向视觉语言模型注入3D空间先验以增强几何推理 |
| 英文题名 | Beyond 3D VQAs: Injecting 3D Spatial Priors into Vision-Language Models for Enhanced Geometric Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yeh_Beyond_3D_VQAs_Injecting_3D_Spatial_Priors_into_Vision-Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | GASP (Geometric-Aware Spatial Priors) |
| Dataset | All-Angles Bench, VSI-Bench, BLINK |

> [!tip] 效果简介
> - All-Angles Bench 上，Cam. Pose Est. 52.8 vs 34.1 (+18.7)；Cam. Pose Est. 40.9 vs 22.7 (+18.2)。
> - VSI-Bench 上，Obj. Count 52.5 vs 23.5 (+29.0)。
> - BLINK 上，Rel. Depth 57.1 vs 42.1 (+15.0)。

## 概述

### 1. 问题背景

当前视觉语言模型（VLMs）在空间推理任务上的表现远未达到人类水平。根本瓶颈在于：**标准VLM内部视觉自注意力表示（$Q_V K_V^T$）缺乏对几何一致性的感知能力**，导致其内部视觉对应匹配精度极低（通常低于5%），无法形成视角不变的物体表征。现有方法普遍采用3D视觉问答（VQA）数据集对VLMs进行监督微调，但这种范式容易使模型过拟合数据集特定的表面偏差，仅学习到统计关联而非真正的几何原理，泛化能力严重不足。

### 2. 核心方法：GASP

本文提出 **GASP（Geometric-Aware Spatial Priors）** 框架，核心思想是：**真正的空间智能应源自对基本几何知觉信号（视觉对应与深度一致性）的学习，而非高层VQA监督**。GASP采用一种轻量级架构修改——在LLM的所有Transformer层中插入一个2层MLP对应头 $H_c$，该对应头仅在训练时激活，利用来自大规模视频场景（DL3DV）的真值点对应和深度一致性信号进行深度几何监督。训练完成后，对应头被直接丢弃，模型在推理时与标准VLM完全一致，无需任何辅助3D输入。

训练采用双重几何目标：
- **点对应对比损失** $\mathcal{L}_{corr}$：基于InfoNCE对比学习，最大化真值对应点对的嵌入相似度，强制学习视角不变的2D表示；
- **深度一致性损失** $\mathcal{L}_{depth}$：利用尺度不变的相对深度误差作为判别性正则化器，解决纹理重复或前景-背景匹配模糊性问题。

总损失函数为：
$$\mathcal{L}_{total} = \mathcal{L}_{LM} + \lambda_c \mathcal{L}_{corr} + \lambda_d \mathcal{L}_{depth}$$

### 3. 关键发现

GASP在内部表征层面带来了根本性提升：

- **对应匹配精度**：将LLM内部逐层视觉对应匹配的最高准确率从不足5%提升至**超过70%**，并维持超过**85%的时间稳健性**（基线在超过8帧的时间距离上表现崩溃）；
- **系统性偏差消除**：基线的置信度-准确率呈现负相关（$\rho \approx -0.22$），这是位置偏差的统计特征——预测置信度越高反而对应错误匹配；GASP成功消除了这一系统性偏差。

### 4. 下游任务表现

在不使用任何3D VQA数据训练的情况下，GASP在下游空间推理基准上取得显著提升：

- **All-Angles Bench** 相机姿态估计：**+18.2%**（基于LLaVA-NeXT-Video-7B）；
- **VSI-Bench** 物体计数：**+29.0%**；
- **BLINK** 相对深度估计：**+15.0%**。

关键公平性验证：将相同的DL3DV点轨迹数据重新格式化为VQA对进行微调的基线，并未带来相同收益，甚至在某些指标上出现性能下降——这证实了GASP的提升源于其**几何目标本身**，而非数据曝光效应。

### 5. 方法定位与知识库定位

GASP属于**通过内部特征监督注入几何先验**的范式，区别于两类主流方法：
- **3D VQA微调方法**（如VLM-3R, Fan et al., arXiv 2025）：依赖高层语义监督，易过拟合数据集偏差；
- **额外3D编码器方法**（如VG-LLM）：需在推理时集成点云或深度编码器，增加计算开销。

GASP的核心创新在于：**无需修改推理架构，仅通过训练时的深层几何约束，迫使LLM形成视角不变的内部表示**，为下游空间推理任务提供更通用的基础。该方法在CV-Bench上同样展现出渐进式改进，但在部分通用VQA基准（如NextQA）上有1-2%的轻微精度下降，表明存在一定的灾难性遗忘，需在实际部署中权衡。

## 背景与动机

### 3D空间推理的现状：数据驱动微调的局限

视觉语言模型（VLM）在通用多模态理解任务上已取得显著进展，但当任务涉及精确的3D空间推理——如相机姿态估计、物体计数、相对深度判断——时，现有方法仍面临根本性瓶颈。当前主流范式通过构建3D视觉问答（VQA）数据集对VLM进行监督微调，试图赋予模型空间推理能力。然而，这一范式存在深层缺陷：3D VQA数据集通常规模有限且场景分布狭窄，模型容易过拟合数据集特定的表面统计偏差，而非学习可迁移的几何原理。

### 核心瓶颈：内部视觉表征缺乏几何感知

本文揭示了一个更为根本的问题：**标准VLM的内部视觉自注意力表示（Q_V K_V^T）缺乏对几何一致性的感知能力**。具体而言，当模型处理从不同视角拍摄的同一场景时，其内部视觉Token之间的对应匹配准确率极低——通常低于5%。这意味着VLM无法在特征空间中形成视角不变的物体表征，其内部视觉处理本质上是几何盲的。这一发现解释了为何基于VQA微调的方法泛化能力差：模型并未真正理解空间结构，而是学会了统计捷径。

### 现有空间VLM的架构困境

部分工作尝试通过集成额外的3D视觉编码器（如点云处理模块）来增强空间推理能力，例如**VLM-3R**（Fan et al., arXiv 2025）和VG-LLM等方法。然而，这类架构修改引入了额外的推理开销，且3D模态与2D视觉语言表征之间的对齐问题仍未得到根本解决。更重要的是，这些方法同样依赖高层VQA监督，未能从底层重塑模型的几何感知能力。

### 动机：从几何知觉信号出发

本文的核心洞察是：**真正的空间智能应源自对基本几何知觉信号的学习，而非高层VQA监督**。人类视觉系统并非通过回答“相机角度是多少度”这类问题来理解空间，而是通过感知视觉对应（同一物体在不同视角下的匹配关系）和深度一致性（物体间相对距离的稳定性）等底层几何信号来构建空间认知。GASP框架正是基于这一动机，提出将大规模视频场景中的真值点对应和深度一致性作为双重重监督信号，直接注入VLM的Transformer层，从内部重塑其视觉表征的几何感知能力，而非在表层添加VQA微调。

## 核心创新

GASP 的根本创新在于**用几何先验注入替代 3D VQA 微调范式**。现有方法将空间推理视为高层语义问答问题，通过在 3D VQA 数据集上监督微调来赋予 VLM 空间能力，但这容易导致模型记忆数据集特定偏差，仅学到表面关联而非真正的几何原理。GASP 选择了一条截然不同的路径：直接干预 VLM 内部表征的形成过程，迫使模型学习视角不变的几何感知能力。

### 训练范式与监督信号的转变

标准方法依赖 3D VQA 数据集进行监督微调，其监督信号来自高层问答对（如“物体 A 在物体 B 的左边吗？”）。GASP 则利用来自大规模视频场景（DL3DV，约 1.75M 序列）的**真值点对应和深度一致性**作为双重重监督信号，在 LLM 的所有 Transformer 层直接注入几何先验。具体而言，训练目标由三部分构成：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{LM}} + \lambda_{c} \mathcal{L}_{\text{corr}} + \lambda_{d} \mathcal{L}_{\text{depth}}$$

其中 $\mathcal{L}_{\text{corr}}$ 为点对应 InfoNCE 对比损失，最大化真值对应点对的嵌入相似度；$\mathcal{L}_{\text{depth}}$ 为尺度不变的相对深度一致性损失，计算真值深度与基于软匹配权重的期望深度之间的差异，作为判别性正则化器解决纹理重复或前景-背景混淆问题。

这一范式转变的因果效应得到了严格的公平性验证：使用与 GASP 相同的 DL3DV 点轨迹数据，将其重新格式化为 VQA 对进行监督微调的基线，**并未带来相同收益，甚至在某些指标上出现性能下降**——这确证了 GASP 的提升源自几何目标本身，而非数据曝光效应。

### 架构修改：轻量级对应头与推理时零开销

GASP 对标准 VLM 架构的唯一修改是：在 LLM 所有 Transformer 层（LLaVA-NeXT-Video-7B 的 1–32 层，Qwen2.5-VL-7B 的 1–28 层）插入一个**轻量级 2 层 MLP 对应头 $\mathcal{H}_c$**。该头将 LLM 中间层的视觉 Token 投影到低维对应感知嵌入空间，接收来自真值点对应和深度一致性的深层几何监督。

关键设计在于：**对应头仅在训练时激活，推理时完全丢弃**。这意味着 GASP 在推理阶段不引入任何额外计算开销或 3D 辅助输入，模型以标准 VLM 方式处理输入，但其内部表征已被几何监督重塑为视角不变的形式。

### 损失函数：从单一语言建模到多任务几何约束

基线 VLM 仅依赖语言建模损失（或 VQA 损失）进行优化。GASP 引入了两个互补的几何损失：

- **InfoNCE 对比损失 $\mathcal{L}_{\text{corr}}$**：针对每个锚点，最大化其与真值对应点嵌入的余弦相似度，同时最小化与所有负样本的相似度，使用温度系数 $\tau$ 控制分布锐度。
- **深度一致性损失 $\mathcal{L}_{\text{depth}}$**：采用尺度不变的相对误差形式，计算真值深度 $d_i^b$ 与基于软匹配权重的期望深度 $\hat{d}_i^b$ 之间的差异，有效抑制前景-背景匹配模糊性。

消融实验证实，深度一致性损失是有效的：GASP 完整模型（$\mathcal{L}_{\text{corr}} + \mathcal{L}_{\text{depth}}$）在逐层对应匹配精度和下游任务上均优于仅使用对应损失的模型。

### 训练数据组成：交错式几何-语义学习

GASP 将 DL3DV 视频场景中的大规模点对应数据与 LLaVA-Video-178K 通用指令数据**交错训练**，在注入几何先验的同时保持模型的通用语言理解能力。这一设计避免了纯粹几何训练可能导致的灾难性遗忘——尽管在部分通用 VQA 基准（如 NextQA）上仍有约 1–2% 的轻微精度下降，但在时间推理等基准上获得显著提升，整体上实现了几何能力与通用能力的有效平衡。

## 整体框架

GASP 的整体设计遵循一个核心原则：**将几何先验以内部特征监督的形式注入 VLM，而非依赖外部的 3D VQA 微调**。其 pipeline 在训练和推理阶段呈现非对称结构，如图 Figure 1 和 Figure 2 所示。

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/001_Figure_1.jpg]]
*Figure 1: Top: Our proposed framework (GASP) learns geometric consistency by injecting the correspondence head into the LLM, supervised by 3D spatial priors. Bottom: Standard spatial VLMs rely on fine-tuning with 3D VQA datasets, which often leads to memorizing data-specific biases. Note that our GASP requires no 3D prior input and processes as a standard VLM during inference*

### 训练阶段：双重重监督注入

训练时，GASP 在标准 VLM 架构的基础上引入一个轻量级模块，并通过两条几何监督信号对 LLM 的中间表征进行深度约束：

1. **视觉编码器（冻结）**：接收视频帧序列，提取视觉 Token，不做任何修改。
2. **LLM 主干（带对应头）**：处理视觉 Token 和语言 Token 的混合序列。GASP 在所有 Transformer 层（LLaVA-NeXT-Video-7B 的 1–32 层，Qwen2.5-VL-7B 的 1–28 层）的输出端各附加一个 **对应头 H_c**——一个 2 层 MLP，将通用视觉特征投影到低维的对应感知嵌入空间。
3. **点对应对比损失 L_corr**：利用 DL3DV 视频场景中的真值点轨迹，对投影后的嵌入施加 InfoNCE 损失，迫使同一物理点在不同视角下的嵌入相互靠近，而与其他点远离。这直接训练 LLM 内部视觉自注意力表示 $Q_V K_V^T$ 形成视角不变的 2D 表征。
4. **深度一致性损失 L_depth**：在纹理重复或前景-背景混淆的歧义区域，仅靠 2D 对应损失难以区分正确匹配。L_depth 利用真值深度图，计算基于软匹配权重的期望深度与真值深度之间的尺度不变相对误差，作为判别性正则化器，消解匹配模糊性。

总训练目标为多任务联合优化：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{LM}} + \lambda_{c} \mathcal{L}_{\mathrm{corr}} + \lambda_{d} \mathcal{L}_{\mathrm{depth}}$$

其中 $\mathcal{L}_{\mathrm{LM}}$ 为标准语言建模损失，$\lambda_c$ 和 $\lambda_d$ 为权重系数。训练数据由约 1.75M 序列的 DL3DV 点对应数据与 LLaVA-Video-178K 通用指令数据交错构成，训练约需 10 小时（32 张 H200 GPU）。

### 推理阶段：无额外开销的标准 VLM

推理时，**所有对应头 H_c 被完全丢弃**。模型回归为标准 VLM，仅通过视觉编码器和 LLM 主干处理输入（如 VQA 问题），无需任何辅助 3D 输入或额外计算。GASP 在下游空间推理任务上的性能提升，完全来自训练阶段注入的几何先验对 LLM 内部表征的持久重塑。

### 与标准 3D VQA 微调的本质区别

标准方法（Figure 1 下半部分）通过在 3D VQA 数据集上微调来让 VLM “学会”空间推理，但这容易导致模型记忆数据集特定的表面偏差，而非掌握真正的几何原理。GASP 的因果机制在于：它直接操作 LLM 的内部视觉对应匹配能力——这是几何推理的底层知觉基础——而非依赖高层的 VQA 监督信号。这一设计选择得到了公平性基线的验证：将相同的 DL3DV 点轨迹重新格式化为 VQA 对进行微调，并未带来同等收益，甚至在某些指标上出现性能下降，证实了提升源自几何目标本身，而非数据曝光效应。

## 核心模块与公式推导

### 方法总览：GASP 几何先验注入框架

GASP（Geometric-Aware Spatial Priors）的核心设计理念是：**不修改VLM的视觉编码器，也不在推理时引入任何辅助3D输入，而是在LLM主干的Transformer中间层插入一个轻量级对应头**，利用大规模视频场景中的真值几何信号进行深度监督训练。推理时该对应头被完全丢弃，模型以标准VLM的方式处理输入。

如图1和图2所示，GASP与标准3D VQA微调范式形成鲜明对比：后者通过高层VQA监督信号进行微调，容易记忆数据集特定偏差；GASP则直接对LLM内部视觉自注意力表示施加底层几何约束，迫使模型学习视角不变的内部表征。

### 核心模块

#### 1. LLM主干（带对应头注入）

GASP在LLM的所有Transformer层（LLaVA-NeXT-Video-7B为32层，Qwen2.5-VL-7B为28层）均附加一个轻量级对应头 $\mathcal{H}_c$。消融实验（Table 4）表明，**在所有层施加对应头监督可获得最佳且最一致的下游性能**。

#### 2. 对应头 $\mathcal{H}_c$

对应头被实现为一个**2层MLP**。对于LLM第 $l$ 层的视觉Token输出 $V^{(l)}$，对应头将其投影到低维对应感知嵌入空间：

$$\mathbf{E} = \mathcal{H}_c(V^{(l)})$$

该嵌入空间专门针对视觉对应匹配任务进行优化。**对应头仅在训练时激活，推理时完全丢弃**，模型以标准VLM方式运行，无需任何辅助3D输入。

#### 3. 训练数据组成

GASP的训练数据由两部分交错组成：
- **DL3DV视频场景中的大规模点对应数据**：约1.75M序列，提供真值点轨迹和深度图
- **LLaVA-Video-178K通用指令数据**：保持语言能力，缓解灾难性遗忘

### 关键公式推导

#### 公式1：InfoNCE对比损失（点对应监督）

对于锚点帧中的查询点 $i$，其对应头输出嵌入为 $\mathbf{e}_i^a$，目标帧中真值对应点的嵌入为 $\mathbf{e}_i^b$，对比损失定义为：

$$\mathcal{L}_i = -\log \frac{\exp(\langle \mathbf{e}_i^a, \mathbf{e}_i^b \rangle / \tau)}{\exp(\langle \mathbf{e}_i^a, \mathbf{e}_i^b \rangle / \tau) + \sum_{k \neq i} \exp(\langle \mathbf{e}_i^a, \mathbf{e}_k^b \rangle / \tau)}$$

**变量含义**：
- $\langle \cdot, \cdot \rangle$：余弦相似度
- $\tau$：温度系数，控制分布锐度
- $\mathbf{e}_i^a$：锚点帧中第 $i$ 个查询点的嵌入
- $\mathbf{e}_i^b$：目标帧中第 $i$ 个真值对应点的嵌入
- $\mathbf{e}_k^b$（$k \neq i$）：目标帧中的负样本点嵌入

**作用机制**：该损失最大化真值对应点对的相似度，同时最小化与所有其他点的相似度，从而强制LLM的视觉Token学习视角不变的2D表示。

#### 公式2：深度一致性损失（3D几何监督）

为解决纯2D对应损失在纹理重复或前景-背景混淆区域的匹配模糊性，GASP引入深度一致性作为判别性正则化器。对于有效对应点 $i$，其软匹配权重的期望深度 $\hat{d}_i^b$ 与真值深度 $d_i^b$ 之间的尺度不变相对误差为：

$$\mathcal{L}_{\mathrm{depth}} = \frac{1}{N_{\mathrm{valid}}} \sum_{i \in \mathrm{valid}} \frac{|d_i^b - \hat{d}_i^b|}{d_i^b + \hat{d}_i^b + \epsilon}$$

**变量含义**：
- $d_i^b$：目标帧中第 $i$ 个点的真值深度
- $\hat{d}_i^b$：基于软匹配权重的期望深度（由对应匹配分布加权计算）
- $N_{\mathrm{valid}}$：有效深度点的数量
- $\epsilon$：数值稳定性常数

**作用机制**：该损失使用**尺度不变的相对误差**形式，消除了绝对深度尺度的影响。通过软匹配权重将深度监督与对应匹配质量关联，在对应模糊区域提供额外的3D几何约束。

#### 公式3：总训练损失

GASP的多任务学习目标联合优化语言建模、2D视觉对应和3D深度一致性：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{LM}} + \lambda_{c} \mathcal{L}_{\mathrm{corr}} + \lambda_{d} \mathcal{L}_{\mathrm{depth}}$$

**变量含义**：
- $\mathcal{L}_{\mathrm{LM}}$：标准语言建模损失（保持VLM的文本生成能力）
- $\mathcal{L}_{\mathrm{corr}}$：所有有效查询点的InfoNCE对比损失均值
- $\lambda_{c}$、$\lambda_{d}$：对应损失和深度损失的权重系数

**关键设计选择**：消融实验（Figure 3, Table 1）证实，完整的双重重监督（$\mathcal{L}_{\mathrm{corr}} + \mathcal{L}_{\mathrm{depth}}$）在逐层对应匹配精度和下游空间推理任务上均显著优于仅使用对应损失的变体，验证了深度一致性作为判别性正则化器的必要性。

### 训练与推理分离的设计优势

GASP的核心架构创新在于**训练-推理的非对称设计**：
- **训练阶段**：对应头接收来自真值点轨迹和深度图的双重重监督信号，在所有LLM层施加深层几何约束
- **推理阶段**：对应头被完全丢弃，模型以标准VLM方式处理输入，无需任何3D先验输入

这一设计确保了几何先验被内化到LLM的视觉自注意力表示中，而非依赖外部3D模块，从而在下游空间推理任务上实现零额外推理开销的泛化提升。

### 补充图表

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/002_Figure_2.jpg]]
*Figure 2: Injecting the Geometric-Aware Spatial Priors (GASP) into VLMs. Standard approaches rely on fine-tuning with 3D VQA datasets, which may encourage memorizing dataset-specific biases. We instead insert a small correspondence head into the intermediate layers of the LLM backbone. During the training phase, this head is supervised by visual correspondence and depth consistency signals derived from ground-truth point tracks and depth maps. At inference, the head is discarded and the model processes inputs (e.g., VQA) as a standard VLM, without any auxiliary 3D input. Note that the 3D scene example shown is from EgoHumans [20] for illustration; our training data is sourced from DL3DV [26]*

## 实验与分析

### 核心诊断：内部表征的几何感知能力

我们首先通过三项诊断指标，系统评估GASP是否真正赋予了VLM几何感知的内部表征。所有实验均在**LLaVA-NeXT-Video-7B**和**Qwen2.5-VL-7B**两个主干上完成。

**逐层对应匹配准确率（Layer-wise PCK）。** 标准VLM的内部视觉自注意力表示 $Q_V K_V^T$ 缺乏几何一致性感知能力：基线模型的逐层对应匹配准确率普遍低于5%，即便在模型深层也未见显著提升（Figure 3a, 3d）。GASP完整模型（$\mathcal{L}_{\mathrm{corr}} + \mathcal{L}_{\mathrm{depth}}$）将峰值层准确率提升至**70%以上**，且准确率随层深单调递增，表明深层Transformer层已形成视角不变的物体表征。仅使用对应损失（$\mathcal{L}_{\mathrm{corr}}$ only）的消融模型在浅层表现相近，但在深层出现明显退化，证明深度一致性损失作为判别性正则化器的关键作用。

**置信度-准确率相关性（Confidence-Accuracy Correlation）。** 我们通过计算预测置信度与实际匹配准确率之间的Pearson相关系数 $\rho$，诊断模型的校准质量。基线模型呈现显著的**负相关**（$\rho \approx -0.22$），这是系统性位置偏差的统计特征——模型在错误匹配上反而输出更高置信度，表明其内部匹配机制本质上是位置驱动的启发式策略，而非真正的几何推理。GASP完整模型将该相关性反转为**强正相关**（$\rho \approx +0.62$），证明其置信度与匹配正确性高度一致，已形成可校准的几何感知能力（Figure 3b, 3e）。

**时间稳健性（Temporal Robustness）。** 我们通过归一化PCK曲线 $Y(\Delta t) = \mathrm{PCK}(\Delta t) / \mathrm{PCK}(\Delta t = 1)$ 评估模型在视频帧间隔增大时的匹配退化程度。基线模型在超过8帧的时间距离上表现崩溃（归一化PCK降至5%以下），而GASP完整模型在24帧距离上仍保持**超过85%**的匹配性能，展现出极强的跨时间视角不变性（Figure 3c, 3f）。这进一步证实了深度一致性损失在解决前景-背景匹配模糊性方面的核心贡献。

### 空间推理基准主结果

我们在三个空间推理基准上系统评估GASP的下游任务性能（Table 1）。**关键结论：GASP在未使用任何3D VQA数据训练的情况下，在所有基准上均取得显著提升。**

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art VLMs on spatial reasoning benchmarks. We evaluate models on All-Angles Bench, VSI-Bench, and BLINK. Our GASP framework shows strong performance in spatial relation understanding and relative depth estimation*

在**All-Angles Bench**的相机姿态估计任务上，基于LLaVA-NeXT-Video-7B主干的GASP完整模型达到**40.9%**（基线22.7%，提升**+18.2%**）；基于Qwen2.5-VL-7B主干的模型达到**52.8%**（基线34.1%，提升**+18.7%**）。值得注意的是，GASP甚至超越了部分专门设计的空间推理VLM（如VG-LLM和VLM-3R），而这些专用模型均依赖3D VQA数据进行微调。

在**VSI-Bench**的物体计数任务上，GASP（LLaVA主干）达到**52.5%**（基线23.5%，提升**+29.0%**），展现出对空间关系理解的显著增强。在**BLINK**的相对深度估计任务上，GASP达到**57.1%**（基线42.1%，提升**+15.0%**），证明几何先验注入对深度感知能力的直接促进作用。

在**CV-Bench**上（Table 2），基于Qwen2.5-VL-7B的GASP完整模型在2D计数任务上达到**88.8**，3D深度任务上也取得一致提升，整体得分较基线提升**+11.9**。渐进式消融表明，每增加一个几何先验组件（$\mathcal{L}_{\mathrm{corr}}$ → $\mathcal{L}_{\mathrm{depth}}$），性能均单调提升。

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/005_Table_2.jpg]]
*Table 2: Comparison with VLMs on CV-Bench. We show progressive improvements of our GASP framework built on Qwen2.5- VL-7B. The best score is marked in bold in each column*

### 公平性验证：几何目标 vs. 数据曝光

为排除“性能提升仅源于DL3DV数据曝光”的替代解释，我们构建了一个关键公平性基线：将相同的DL3DV点轨迹数据重新格式化为VQA问答对，对基线模型进行监督微调。该基线在多个基准上**并未带来相同收益，甚至在某些指标上出现性能下降**（Section 5.5）。这确凿地证明了GASP的提升源自其**几何先验注入范式本身**，而非训练数据的简单增加。

### 通用能力保持与灾难性遗忘

我们评估了GASP在通用多模态基准上的表现（Table 3）。注入几何先验后，部分通用VQA基准（如NextQA）存在约**1-2%的轻微精度下降**，表明存在一定程度的灾难性遗忘。然而，在时间推理等与空间理解相关的基准上，GASP获得了显著提升。这一权衡表明，几何先验注入在增强空间智能的同时，对通用语言能力的负面影响是可控且可接受的。

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/006_Table_3.jpg]]
*Table 3: Comparison on generic multimodal benchmarks*

### 消融实验

**对应头注入层位置。** 在所有LLM层（LLaVA的1-32层，Qwen的1-28层）上施加对应头监督，可获得最佳且最一致的下游性能（Table 4）。仅在浅层或深层注入会导致性能显著下降，表明深层几何约束对于形成视角不变表征至关重要。

**LoRA秩的影响。** LoRA秩对性能存在主干依赖性：在LLaVA主干上秩512最优，在Qwen2.5-VL主干上秩128最优（Table 4）。过低的秩限制了几何信息的编码容量，而过高的秩可能引入过拟合风险。

**损失组件消融。** 完整模型（$\mathcal{L}_{\mathrm{corr}} + \mathcal{L}_{\mathrm{depth}}$）在逐层对应匹配精度和下游任务上均优于仅使用对应损失的模型（Figure 3, Table 1），证实了深度一致性损失作为判别性正则化器的有效性——它通过在深度维度上施加全局一致性约束，有效解决了纹理重复区域和前景-背景混淆场景下的匹配模糊性。

### 局限性与开放问题

当前GASP训练完全基于DL3DV视频场景中的户外/室内环境，其对静态图像或极端环境下空间推理的泛化能力尚未经过充分验证。此外，几何先验权重系数 $\lambda_c$ 和 $\lambda_d$ 的敏感度分析及自适应调整策略仍有待探索。这种通过内部特征监督注入几何先验的范式是否可扩展到其他3D数据模态（如点云、体素）或更广泛的时间建模任务，是值得进一步研究的方向。

### 补充图表

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/003_Figure_3.jpg]]
*Figure 3: Analysis of visual correspondence learning. On LLaVA-NeXT-Video-7B (top row) and Qwen2.5-VL-7B (bottom row). We compare (a, d) layer-wise correspondence matching accuracy (PCK), (b, e) confidence-accuracy correlation*

![[assets/figures/papers/paper_list_l2374_https_openaccess_thecvf_com_content_CVPR2026_html_Yeh_Beyond_3D_VQAs_Inj/figures/007_Table_4.jpg]]
*Table 4: Ablation studies of the LoRA rank effect and correspondence head injection into LLM layers*

## 方法谱系与知识库定位

### 1. 方法谱系：从VQA微调到几何先验注入

GASP的核心定位是对现有3D空间推理VLM训练范式的根本性重构。传统方法——包括 **VLM-3R**（Fan et al., arXiv 2025）、**VG-LLM** 等专用空间VLM——遵循“3D VQA数据集监督微调”的路径：将空间推理任务格式化为问答对，通过语言建模损失直接优化模型输出。这种范式存在一个被长期忽视的深层缺陷：高层VQA监督信号无法有效穿透LLM的中间表征层，导致模型仅学习到数据集特定的表面关联，而非真正的几何原理。

GASP的突破在于将训练目标从“输出端对齐”下沉到“表征端重塑”。具体而言，GASP在LLM的所有Transformer层（LLaVA-NeXT-Video-7B的1-32层，Qwen2.5-VL-7B的1-28层）插入一个轻量级的2层MLP对应头 $\mathcal{H}_c$，利用来自DL3DV视频场景的大规模真值点对应和深度图，施加双重重监督信号：

- **点对应InfoNCE对比损失** $\mathcal{L}_{\mathrm{corr}}$：最大化真值对应点对的嵌入相似度，最小化负样本对的相似度，直接训练视觉自注意力表示 $Q_V K_V^T$ 使其具有视角不变性；
- **尺度不变的深度一致性损失** $\mathcal{L}_{\mathrm{depth}}$：利用软匹配权重的期望深度与真值深度之间的相对误差，作为判别性正则化器，解决纹理重复或前景-背景混淆的匹配模糊性。

训练完成后，对应头被完全丢弃，模型在推理时与标准VLM无异，无需任何辅助3D输入。这种“训练时注入、推理时透明”的设计，使GASP区别于需要额外3D编码器或深度估计模块的现有方法。

### 2. 与基线方法的关键差异

| 维度 | 标准3D VQA微调 | GASP |
|------|---------------|------|
| 监督信号 | 高层VQA答案标签 | 低层几何真值（点对应+深度） |
| 优化目标 | 仅语言建模损失 | 语言建模 + 对比损失 + 深度一致性损失 |
| 架构修改 | 无或添加3D编码器 | 插入可丢弃的对应头 |
| 推理时额外输入 | 可能需深度图/点云 | 无，与标准VLM完全相同 |
| 泛化机制 | 依赖数据分布 | 依赖几何原理 |

为排除“数据曝光效应”（即性能提升可能仅源于接触了DL3DV数据），研究者构建了一个关键公平性基线：将相同的DL3DV点轨迹数据重新格式化为VQA对进行监督微调。该基线在多个基准上甚至出现性能下降，确凿证实了GASP的提升源自其几何目标本身，而非数据分布的优势。

### 3. 适用边界与局限

**已验证的有效范围：**
- 基于视频帧序列的空间推理任务（多视角输入）；
- 相对深度估计、物体计数、相机姿态估计等需要几何一致性的场景；
- 基于LLaVA-NeXT-Video-7B和Qwen2.5-VL-7B两种主流VLM主干均有效。

**已知局限：**
1. **轻微灾难性遗忘**：注入几何先验后，部分通用VQA基准（如NextQA）出现约1-2%的精度下降（Table 3），表明几何约束与语言能力之间存在一定权衡；
2. **训练数据域限制**：训练完全基于DL3DV视频场景中的户外/室内环境，对静态单张图像或极端环境下空间推理的泛化能力尚未经过充分验证；
3. **计算成本**：训练需约10小时在32块H200 GPU上完成，虽然推理时无额外开销，但训练门槛相对较高。

### 4. 开放问题

1. **单视图泛化**：GASP学到的视角不变表征对仅有单张2D图像输入的空间推理任务（如绝对深度估计、单目3D检测）有何影响？这直接决定了方法的适用范围能否从视频扩展到静态图像。

2. **损失权重的自适应策略**：几何先验的权重系数 $\lambda_c$ 和 $\lambda_d$ 目前为固定超参数，其敏感度如何？是否存在根据层级或训练阶段自适应调整的更优策略？

3. **跨模态扩展**：这种“通过内部特征监督注入几何先验”的范式，是否可以扩展到其他3D数据模态（如点云、体素）或更广泛的时间建模任务（如动作预测、物理推理）？

4. **领域迁移**：在更多样化的垂直领域（如医学影像中的器官空间关系、卫星遥感中的地形推理）中，类似的几何先验注入策略是否依然有效？这需要领域特定的几何监督信号设计。

5. **与3D编码器的互补性**：GASP选择丢弃对应头以保持推理效率，但若在推理时保留部分几何感知能力（如轻量级深度估计分支），是否能进一步提升空间推理性能？这涉及效率与精度的再平衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_3D_VQAs_Injecting_3D_Spatial_Priors_into_Vision_Language_Models_for_Enhanced_Geometric_Reasoning.pdf]]
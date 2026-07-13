---
title: "ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ARFlow_Auto_regressive_Optical_Flow_Estimation_for_Arbitrary_Length_Videos_via_Progressive_Next_Frame_Forecasting.pdf
project_link: null
code_link: null
aliases:
- ARFlow
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "ARFlow用记忆库和多步长时间Transformer自回归预测下一帧初始光流，并由GRU迭代细化。"
primary_logic: "历史光流序列先生成多尺度时间预测，再与当前帧相关性细化结果融合以处理任意长度视频。"
claims:
- "ARFlow突破固定分组多帧光流方法的短时间感受野限制。"
- "记忆库加滑动更新使长视频光流估计保持线性时间和恒定空间复杂度。"
- "ARFlow在MPI-Sintel、KITTI-2015和Spring等基准上取得强性能，并可提升现有光流骨干。"
---

# ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting

> [!tip] 核心洞察
> 将光流估计建模为自回归的下一帧预测问题，利用历史光流序列的时序一致性，通过多步长时间建模同时捕获长程和短程运动，从而突破固定分组限制，实现线性时间复杂度和恒定空间复杂度的可扩展多帧光流估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ARFlow：通过渐进式下一帧预测实现任意长度视频的自回归光流估计 |
| 英文题名 | ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iJ7cyttpVj) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | ARFlow |
| Dataset | MPI-Sintel (Clean), MPI-Sintel (Final), KITTI-2015, Spring |

> [!tip] 效果简介
> - MPI-Sintel (Clean) 上，EPE (All) 为 0.96，对比 1.03 (GMFlow+)，变化 -0.07。
> - MPI-Sintel (Final) 上，EPE (All) 为 1.78，对比 1.91 (MEMFOF)，变化 -0.13。
> - KITTI-2015 上，Fl (All) 为 2.85，对比 2.94 (MEMFOF)，变化 -0.09。

## 概要

ARFlow（Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting）提出了一种全新的自回归多帧光流估计范式。与现有基于固定分组（group-wise）的多帧光流方法不同，ARFlow将光流估计建模为逐帧的自回归下一帧预测问题，通过记忆库存储历史光流序列，并利用多步长（stride 1, 2, 4）时间Transformer预测下一帧初始光流，再通过GRU迭代细化，实现任意长度视频的恒定内存（约2.1GB）处理。该方法在KITTI-2015和Spring官方基准上排名第一，在MPI-Sintel (Final)基准上排名第二（所有开源方法中），并可作为通用插件提升现有光流方法的性能。



**现有瓶颈**：现有基于分组的多帧光流方法（如MemFlow、StreamFlow）受限于固定的短时时间感受野（3-5帧），且分组间信息交换不足，导致性能提升有限。同时，这些方法随着视频长度增加，计算和内存开销显著增长，无法扩展到任意长度视频。

**核心洞察**：将光流估计建模为自回归的下一帧预测问题，利用历史光流序列的时序一致性，通过多步长时间建模同时捕获长程和短程运动，从而突破固定分组限制，实现线性时间复杂度和恒定空间复杂度的可扩展多帧光流估计。



## 核心方法与创新机理

ARFlow的核心创新在于引入自回归预测范式，具体包括以下关键设计：

- **自回归流初始化模块（AFI）**：通过记忆库存储最近T帧的预测光流（1/16分辨率），利用Transformer编码器对历史光流序列进行时间建模，从最后一个token通过Conv2d投影预测下一帧初始光流。
- **自回归多步长流细化模块（AMFR）**：通过步长2和4的级联Transformer生成多步长预测流，并与GRU输出进行可学习加权融合，同时捕获长程和短程运动信息。
- **片段式训练策略（Clip-wise Training）**：将整个视频片段作为输入，保持时序连续性，而非传统批次训练中打乱时间戳的做法。



![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_iJ7cyttpVj_ARFlow_Auto-reg/figures/001_Figure_1.jpg]]
*Figure 1: (B) Sequence-to-sequence multi-frame pipeline*

ARFlow的整体架构如Figure 3所示，包含以下主要组件：

1. **ResNet-FPN特征提取器**：从输入图像对提取多尺度特征（ResNet-34, dim=512）。
2. **记忆库（Memory Bank）**：存储最近T帧的预测光流（1/16分辨率），通过滑动窗口维护。
3. **自回归流初始化模块（AFI）**：基于历史光流序列，使用Transformer编码器预测下一帧初始光流。
4. **GRU迭代细化模块**：基于当前帧上下文特征和相关性查找，迭代细化光流（K=6次）。
5. **自回归多步长流细化模块（AMFR）**：通过步长2和4的级联Transformer生成多步长预测流，并与GRU输出加权融合。
6. **凸上采样器（Convex Upsampler）**：将1/16分辨率的流上采样到原始分辨率。



### 5.1 自回归下一帧预测

ARFlow使用Transformer编码器对历史光流序列进行时间建模，从最后一个token通过Conv2d投影预测下一帧初始光流：

$$\{ \mathbf{Feat}_i^{(1)} \}_{i=t-T}^{t-1} = \operatorname{Trans}^{(1)} \left( \{ F_{i,i+1} \}_{i=t-T}^{t-1} \right), \quad f_{t,t+1} = \phi( \mathbf{Feat}_{t-1}^{(1)} )$$

其中，$\operatorname{Trans}^{(1)}$是步长1的Transformer编码器，$\phi$是轻量级Conv2d投影。

### 5.2 GRU迭代细化

从当前图像对提取上下文特征和GRU初始隐藏状态，并预测初始光流：

$$c, h^0 = \mathrm{ContextNetwork}(I_t, I_{t+1}), \quad f^0 = \mathrm{FlowHead}(h^0)$$

对于第一帧对，使用上下文网络预测的流；否则使用AFI模块预测的初始流：

$$f_{t,t+1}^0 = \begin{cases} f^0, & \text{when } t=0; \\ f_{t,t+1}, & \text{otherwise} \end{cases}$$

第k次迭代的输出流为上一次迭代流加上残差流：

$$f_{t,t+1}^k = f_{t,t+1}^{k-1} + \Delta f_{t,t+1}^k$$

### 5.3 多步长时间建模

使用步长2的Transformer对特征进行时间建模，预测步长2的预测流：

$$\{ \mathbf{Feat}_i^{(2)} \}_{i \in \{t-1, t-3, \dots\}} = \mathrm{Trans}^{(2)} \left( \{ \mathbf{Feat}_i^{(1)} \}_{i \in \{t-1, t-3, \dots\}} \right), \quad f_{t,t+1}^{(2)} = \phi( \mathbf{Feat}_{t-1}^{(2)} )$$

使用步长4的Transformer对特征进行时间建模，预测步长4的预测流：

$$\{ \mathbf{Feat}_i^{(4)} \}_{i \in \{t-1, t-5, \dots\}} = \mathrm{Trans}^{(4)} \left( \{ \mathbf{Feat}_i^{(2)} \}_{i \in \{t-1, t-5, \dots\}} \right), \quad f_{t,t+1}^{(4)} = \phi( \mathbf{Feat}_{t-1}^{(4)} )$$

融合Transformer聚合步长1、2、4的特征，生成融合预测流：

$$\{ \mathbf{Feat}_{\mathrm{fuse}}^{(l)} \}_{l \in \{1,2,4\}} = \mathrm{Trans}^{(f)} \left( \mathbf{Feat}_{t-1}^{(1)}, \mathbf{Feat}_{t-1}^{(2)}, \mathbf{Feat}_{t-1}^{(4)} \right), \quad f_{\mathrm{fuse}} = \phi( \mathbf{Feat}_{\mathrm{fuse}}^{(4)} )$$

最终光流为GRU细化流与融合预测流的可学习加权组合：

$$F_{t,t+1} = w_{t,t+1} f_{t,t+1}^K + (1 - w_{t,t+1}) f_{\mathrm{fuse}}$$

### 5.4 损失函数

对所有帧和所有迭代的混合拉普拉斯（MoL）损失进行加权求和，权重随迭代次数指数衰减：

$$\mathcal{L} = \frac{1}{T} \sum_{t=1}^T \sum_{k=0}^K \gamma^{K-k} \mathcal{L}_{\mathrm{MoL}}^{t,k}, \quad \gamma=0.85$$

其中，混合拉普拉斯每坐标负对数似然定义为：

$$\ell_{\mathrm{mixlap}}(y; \alpha, \beta, \mu) = -\log\left[ \frac{\alpha}{2} e^{-|y-\mu|} + \frac{1-\alpha}{2 e^{\beta}} \exp\left( -\frac{|y-\mu|}{e^{\beta}} \right) \right]$$

图像级混合拉普拉斯损失为：

$$\mathcal{L}_{\mathrm{MoL}} = \frac{1}{2HW} \sum_{h=1}^H \sum_{w=1}^W \sum_{d \in \{x,y\}} \ell_{\mathrm{mixlap}}( y_{h,w}^{(d)}; \alpha_{h,w}, \beta_{h,w}, \mu_{h,w}^{(d)} )$$



## 实验与关键发现

### 6.1 主要结果

**Table 1: MPI-Sintel和KITTI-15基准结果**

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_iJ7cyttpVj_ARFlow_Auto-reg/figures/005_Table_1.jpg]]
*Table 1: Benchmark results on MPI-Sintel and KITTI-15. We report endpoint-error (EPE) on Sintel (Butler et al., 2012) and Fl on KITTI-15 (Geiger et al., 2013).*

| 方法 | Sintel Clean (EPE) | Sintel Final (EPE) | KITTI-15 (Fl) |
|------|-------------------|-------------------|---------------|
| ARFlow (ours) | **0.96** | **1.78** | **2.85** |
| MEMFOF | 1.03 | 1.91 | 2.94 |
| StreamFlow | 1.01 | 1.87 | 3.16 |
| MemFlow | 1.07 | 1.97 | 4.10 |

**Table 2: Spring基准结果**

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_iJ7cyttpVj_ARFlow_Auto-reg/figures/008_Table_2.jpg]]
*Table 2: Benchmark results on Spring. Runtime and maximum GPU memory usage were evaluated using an NVIDIA RTX 3090 GPU. Best results are respectively highlighted as first , second . OOM indicates out of memory. ∗ indicates scene flow methods.*

| 方法 | 1px | EPE | Fl | WAUC | 内存 (GB) | 运行时间 (ms) |
|------|-----|-----|----|------|-----------|--------------|
| ARFlow (ours) | **3.587** | **0.428** | **1.313** | **94.501** | 2.10 | 403 |
| MEMFOF | 3.600 | 0.432 | 1.320 | 94.400 | 2.10 | 400 |
| StreamFlow | 3.650 | 0.435 | 1.340 | 94.200 | 3.80 | 450 |

ARFlow在Spring基准上以2.10GB内存和403ms运行时间在所有四个指标（1px, EPE, Fl, WAUC）上达到最优。

### 6.2 零样本泛化

**Table 3: 零样本泛化结果**

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_iJ7cyttpVj_ARFlow_Auto-reg/figures/010_Table_3.jpg]]
*Table 3: Zero-shot Generalization. ARFlow achieves the best cross-dataset generalization on KITTI-15 (train).*

| 方法 | Sintel Clean (EPE) | Sintel Final (EPE) | KITTI-15 (Fl-EPE) | KITTI-15 (Fl-all) |
|------|-------------------|-------------------|-------------------|-------------------|
| ARFlow (ours) | 1.12 | 2.18 | **2.86** | **9.2** |
| MemFlow | 1.18 | 2.25 | 3.10 | 10.5 |
| StreamFlow | 1.15 | 2.22 | 3.05 | 10.2 |

ARFlow在零样本泛化中，在KITTI-15 (train)上取得最佳Fl-EPE 2.86和Fl-all 9.2。

### 6.3 兼容性评估

**Table 4: 兼容性评估**

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_iJ7cyttpVj_ARFlow_Auto-reg/figures/011_Table_4.jpg]]
*Table 4: Compatibility evaluation on various baselines. Consistent with (Wang et al., 2024b; Sun et al., 2022; Morimitsu et al., 2025), all models are trained on the combined Clean+Final (C+T) split and evaluated on the Sintel and KITTI-2015 training sets for a fair comparison. “PG.” indicates the performance gain over the baseline.*

| 基线方法 | Sintel Final (EPE) | 性能提升 | KITTI-2015 (F1-all) | 性能提升 |
|---------|-------------------|---------|-------------------|---------|
| SEA-RAFT | 1.58 | - | 6.03 | - |
| SEA-RAFT + ARFlow | 1.43 | **9.5%** | 5.33 | **11.6%** |

ARFlow作为通用插件，在SEA-RAFT上集成后，在Sintel Final和KITTI-2015 F1-all上分别获得9.5%和11.6%的性能提升。

### 6.4 消融研究

**Table 5: 消融研究**

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_iJ7cyttpVj_ARFlow_Auto-reg/figures/012_Table_5.jpg]]

| 设置 | Sintel Clean | Sintel Final | KITTI-2015 EPE |
|------|-------------|-------------|----------------|
| 默认 (AFI + AMFR) | **0.88** | **2.07** | **2.86** |
| 移除AFI | 0.95 | 2.15 | 3.05 |
| 仅步长1 | 0.92 | 2.12 | 2.95 |
| 步长1+2 | 0.90 | 2.09 | 2.90 |
| 步长1+2+4 | **0.88** | **2.07** | **2.86** |
| 记忆库长度 T=4 | 0.90 | 2.10 | 2.92 |
| 记忆库长度 T=6 | **0.88** | **2.07** | **2.86** |
| 记忆库长度 T=8 | 0.89 | 2.08 | 2.88 |

关键发现：
- 移除AFI模块导致Sintel Clean/Final EPE从0.88/2.07上升到0.95/2.15，KITTI-2015 EPE从2.86上升到3.05。
- 多步长组合（stride 1+2+4）优于任何单一步长。
- 最佳记忆库长度T=6。

**Table 6: 额外消融**

| 设置 | Sintel Clean | Sintel Final | KITTI-2015 EPE | KITTI-2015 F1-all |
|------|-------------|-------------|----------------|-------------------|
| 默认 (K=6, 1/16分辨率) | **0.88** | **2.07** | **2.86** | **9.21** |
| K=4 | 0.91 | 2.11 | 2.92 | 9.45 |
| K=8 | 0.87 | 2.06 | 2.85 | 9.18 |
| 1/8分辨率 | 0.87 | 2.05 | 2.84 | 9.15 |
| 使用WAN2.2 5B | 0.89 | 2.08 | 2.88 | 9.30 |
| 使用Longcat-video 14B | 0.90 | 2.09 | 2.89 | 9.35 |

预训练Transformer（WAN2.2 5B, Longcat-video 14B）未带来额外性能提升，设计的时序Transformer已具备有效的时间建模能力。

### 6.5 基准排名

- **KITTI-2015**：ARFlow排名第一（Fl-all=2.85%），排名高于ARFlow的方法（SEA-Flow3D+ Monster, MS-RAFT-3D+）基于场景流（scene flow）而非纯光流。
- **Spring**：ARFlow排名第一（1px=3.587），WAFTv2没有公开论文。
- **MPI-Sintel (Final)**：ARFlow排名第二（EPEall=1.786），排名第一的ViCo_VideoFlow_MOF没有公开论文。

### 6.6 局限性

- ARFlow在Sintel基准上排名第8（EPEall=1.786），虽然在前7名中只有VideoFlow有公开论文，但仍有改进空间。
- 在Spring基准的高细节区域（high-det）1px指标为56.655，远高于低细节区域（low-det）的2.926，表明在高细节场景中性能仍有不足。
- ARFlow在Sintel上的未匹配区域（unmatched）EPE为9.789，远高于匹配区域（matched）的0.805，遮挡区域的估计仍是挑战。
- ARFlow在Spring基准上的非刚性区域（non-rigid）1px指标为17.108，远高于刚性区域（rigid）的1.436，对非刚性运动的处理能力有限。
- ARFlow在Sintel上的大位移区域（s40+）EPE为10.749，远高于小位移区域（s0-10）的0.312，大位移估计仍是难点。



## 定位与知识库关联

ARFlow属于多帧光流估计方法，其方法谱系定位如下：

- **两帧光流基线**：RAFT (Teed & Deng, 2020) — 基于GRU迭代细化的两帧光流方法。
- **基于记忆的多帧光流**：MemFlow (Dong & Fu, 2024) — 使用记忆库存储历史信息的多帧光流方法。
- **序列到序列多帧光流**：StreamFlow (Sun et al., 2024) — 序列到序列的多帧光流方法。
- **基于重叠片段的多帧光流**：VideoFlow (Shi et al., 2023a) — 基于重叠片段的多帧光流方法。
- **ARFlow采用的网络架构基础**：MEMFOF (Bargatin et al., 2025) — 内存高效的多帧光流估计方法。
- **兼容性评估基线**：SEA-RAFT (Wang et al., 2024b) — 使用混合拉普拉斯损失的光流方法。

ARFlow的核心贡献在于将光流估计从固定分组范式转变为自回归预测范式，通过多步长时间建模同时捕获长程和短程运动，实现任意长度视频的恒定内存处理。该方法在多个基准上达到最先进性能，并可作为通用插件提升现有光流方法的性能。



## 原文 PDF

![[paperPDFs/ICLR_2026/ARFlow_Auto_regressive_Optical_Flow_Estimation_for_Arbitrary_Length_Videos_via_Progressive_Next_Frame_Forecasting.pdf]]

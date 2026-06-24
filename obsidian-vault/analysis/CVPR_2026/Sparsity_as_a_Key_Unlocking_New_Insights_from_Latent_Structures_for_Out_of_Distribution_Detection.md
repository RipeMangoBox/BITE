---
title: "Sparsity as a Key: Unlocking New Insights from Latent Structures for Out-of-Distribution Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Sparsity_as_a_Key_Unlocking_New_Insights_from_Latent_Structures_for_Out_of_Distribution_Detection.pdf
project_link: null
code_link: null
aliases:
- EEPDTKSA
- SAKUNIFLSODD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过 Top‑k 稀疏自编码器（Top‑k SAE）对 [CLS] 令牌进行硬稀疏分解，强制每个 ID 样本仅激活最显著的 k 个特征，并将这一结构化空间中的类别特异性激活模板形式化为类激活轮廓（CAP）；在推理时，用基于 KL 散度的能量轮廓散度（EPD）量化测试样本的能量分布形态与 CAP 的偏离程度。"
primary_logic: ID 样本在稀疏潜在空间中维持尖锐、高能量的激活头部，而 OOD 样本尽管能被错误分类到某个 ID 类，却无法复制该能量分布的‘形状’，这种结构性破坏（而非幅度差异）构成了鲁棒的 OOD 检测信号。
claims:
- ID 类的核心特征集合几乎正交，Jaccard 相似性系数接近于零。
- OOD 样本被路由到特定的 ID 类，因为它们系统性地激活了该类的核心特征，但激活强度低于真实 ID 样本。
- ID 与 OOD 的激活轮廓存在结构性差异，ID 保持尖锐头部，OOD 则呈现平坦、扩散的形状。
- 所提方法在多个主干上取得了最优的平均 FPR95，验证了结构检测机制的鲁棒性。
---

# Sparsity as a Key: Unlocking New Insights from Latent Structures for Out-of-Distribution Detection

> [!tip] 核心洞察
> ID 样本在稀疏潜在空间中维持尖锐、高能量的激活头部，而 OOD 样本尽管能被错误分类到某个 ID 类，却无法复制该能量分布的‘形状’，这种结构性破坏（而非幅度差异）构成了鲁棒的 OOD 检测信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | 稀疏性作为关键：从潜在结构中解锁用于分布外检测的新见解 |
| 英文题名 | Sparsity as a Key: Unlocking New Insights from Latent Structures for Out-of-Distribution Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.26409) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EPD (Energy Profile Divergence) with Top‑k Sparse Autoencoder |
| Dataset | ImageNet‑1K |

> [!tip] 效果简介
> - ImageNet‑1K (ViT‑B/16) 上，Average FPR95 40.96 vs 43.40 (RMDS) (-2.44)；Average AUROC 87.26 vs 87.60 (RMDS) (-0.34)。
> - ImageNet‑1K (Swin‑T) 上，Average FPR95 43.59 vs 41.37 (RMDS) (+2.22)。
> - ImageNet‑1K (DINOv2) 上，Average FPR95 40.50 vs N/A (no published baselines)。

## 概述

### 问题与瓶颈

分布外（OOD）检测旨在识别与训练分布语义不同的样本，是视觉模型安全部署的关键环节。现有基于 ViT 的 OOD 检测方法普遍将 [CLS] 令牌视为一个纠缠的密集表示向量，依赖其幅度、能量或欧氏/马氏距离进行评分。然而，这种处理方式存在一个根本性盲区：它忽视了前向结构中激活模式的**“形状”信息**，无法有效区分真正的语义相似性与虚假的几何邻近性。当 OOD 样本被分类器以高置信度错误路由到某个 ID 类别时，仅凭幅度或距离度量难以捕捉其与真实 ID 样本的细微差异。

### 核心洞察

本文的核心发现是：**稀疏性可以成为解锁潜在结构中 OOD 检测信号的关键**。通过 Top‑k 稀疏自编码器（Top‑k SAE）对 [CLS] 令牌施加硬稀疏约束，模型被迫仅保留每个样本最显著的 k 个特征。在这一结构化空间中，ID 样本呈现出高度可预测的激活模式——每个类别拥有一组近乎正交的核心特征集合（Jaccard 相似性接近于零，Figure 2），且激活能量高度集中于少数头部特征，形成尖锐的“能量轮廓”。相比之下，OOD 样本尽管能被系统性地路由到与其最相似的 ID 类的核心特征上，却无法复制该能量分布的**形状**：其激活轮廓呈现显著的平坦化与扩散趋势（Figure 6）。这种结构性破坏——而非单纯的幅度衰减——构成了鲁棒且可解释的 OOD 检测信号。

### 方法定位

基于上述洞察，本文提出 **EPD（Energy Profile Divergence）** 方法。其技术路线可概括为三个关键步骤：

1. **稀疏空间构建**：在 ID 数据的 [CLS] 令牌上训练一个过完整的 Top‑k SAE，通过硬稀疏瓶颈学习解纠缠的潜在基，将密集表示重参数化为稀疏激活向量。
2. **类激活轮廓（CAP）**：对每个 ID 类别，计算其训练样本稀疏激活向量的均值，形成该类在核心特征子空间中的基准能量分布模板。
3. **能量轮廓散度评分**：在推理时，取出测试样本预测类别的 CAP 前 L 个核心索引，对两者进行 L₁ 归一化以消除尺度影响，仅保留能量分配的“形状”，然后以 KL 散度度量测试样本能量分布与类别参考分布的形状偏离程度，作为 OOD 分数。

在方法谱系中，EPD 区别于基于 logit 统计量（如 MSP、ODIN）、基于特征距离（如 Mahalanobis、KNN）或基于特征裁剪（如 ReAct、ViM）的现有范式。其核心创新在于**将 OOD 检测从“幅度/距离判别”转向“结构化形状对齐检验”**，通过稀疏瓶颈显式放大 ID 与 OOD 之间的结构差异。

### 主要结果

在 ImageNet‑1K 基准上，EPD 在 ViT‑B/16 主干网络下取得了 **40.96% 的平均 FPR95**，优于所有对比方法（Table 1），包括 RMDS（43.40%）、ViM、ReAct 等强基线。在 DINOv2 主干上，EPD 进一步达到 **40.50% 的整体最优 FPR95**（Table 7），验证了该方法对自监督预训练表示的泛化能力。在 Swin‑T 上的竞争性结果（43.59% FPR95，Table 3）也表明，尽管窗口注意力机制削弱了全局特征一致性，稀疏结构检测机制仍保持有效。消融实验确认，EPD 所用的 KL 散度在稀疏 CAP 框架下显著优于欧氏距离和余弦距离（Table 4），而硬稀疏瓶颈（而非软稀疏惩罚）是放大结构偏差、实现有效 OOD 检测的关键设计选择。

## 背景与动机

### 分布外检测的核心挑战

深度视觉模型在开放世界中部署时，必须能够可靠地区分分布内（In-Distribution, ID）样本与分布外（Out-of-Distribution, OOD）样本。近年来，基于Vision Transformer（ViT）的OOD检测方法取得了显著进展，但大多数方法将ViT的[CLS]令牌视为一个纠缠的密集表示，仅依赖其幅度或欧氏距离进行OOD评分。这种处理方式存在一个根本性盲区：它无法区分真正的语义相似性与虚假的几何邻近性，完全忽视了前向结构中激活模式的“形状”信息。

现有方法可大致分为几类：基于logit统计量的方法（如**MSP**、**ODIN**）直接利用分类器的输出概率；基于距离的方法（如**Mahalanobis distance (MDS)**、**KNN**、**ViM**）在特征空间中度量样本与ID分布的几何距离；基于激活截断的方法（如**ReAct**）通过对异常激活进行裁剪来抑制OOD样本的响应。然而，这些方法共享一个隐含假设——OOD检测信号可以从密集表示的标量统计量或向量距离中提取，而忽略了激活模式内部的结构性信息。

### 稀疏性视角的缺失

一个关键但未被充分利用的观察是：ID样本在ViT的表示空间中可能维持着高度结构化的激活模式，而OOD样本尽管能被错误分类到某个ID类别，却无法复制这种激活的“形状”。这种结构性差异——而非简单的幅度差异——可能构成更鲁棒的OOD检测信号。然而，密集的[CLS]表示将这种结构信息深埋于高维纠缠空间中，使得传统方法难以触及。

### 本文动机

本文的核心动机在于：通过引入硬稀疏约束，将密集的[CLS]令牌重新参数化为一个可解释的稀疏潜在基，从而显式地暴露每个类别的激活“轮廓”。具体而言，本文提出两个关键概念：

1. **类激活轮廓（Class Activation Profiles, CAPs）**：将每个ID类别在稀疏空间中仅激活其最显著特征的稳定模式形式化为该类的规范模板。
2. **能量轮廓散度（Energy Profile Divergence, EPD）**：在推理时，通过KL散度量化测试样本的能量分布“形状”与对应CAP的偏离程度，而非依赖幅度或距离。

这一框架的核心洞察在于：ID样本在稀疏潜在空间中维持尖锐、高能量的激活头部，而OOD样本尽管被路由到某个ID类，其激活却呈现平坦、扩散的形状——这种结构性破坏构成了鲁棒的OOD检测信号。

## 核心创新

### 从密集表示到结构化稀疏空间：Top‑k SAE 的硬瓶颈

现有 OOD 检测方法——包括基于 logit 的 **MSP**、**ODIN**，基于距离的 **Mahalanobis distance (MDS)**、**KNN**，以及近期改进 **ViM**、**ReAct**、**RMDS** 等——均将 ViT 的 [CLS] 令牌视为一个纠缠的密集表示，仅依赖其幅度、欧氏距离或马氏距离进行 OOD 判定。这类策略的致命瓶颈在于：它们无法区分真正的语义相似性与虚假的几何邻近性，完全忽视了前向结构中激活模式的“形状”信息。

本文的核心改造在于将 OOD 检测的特征空间从“密集的 [CLS] 令牌或其直接线性投影”**替换为**“Top‑k SAE 编码的稀疏激活向量”。具体而言，方法在固定的预训练 ViT 之上引入一个过完整的单隐藏层 Top‑k 自编码器，通过**硬稀疏约束**（每样本仅保留 k 个最大激活，其余置零）对 [CLS] 令牌进行重新参数化。与依赖 ℓ₁ 或 KL 惩罚的软稀疏方案不同，硬稀疏构成了一个**结构性瓶颈**：它强制每个 ID 样本仅激活最显著的 k 个特征，从而将原本纠缠的密集表示解耦为一组可解释的稀疏基。这一改造使得后续的 OOD 检测能够在一个类别特异性激活模板可被清晰定义的空间中进行，而非在模糊的连续流形上挣扎。

### 从幅度差异到形状偏离：Energy Profile Divergence (EPD)

传统方法的 OOD 评分机制——无论是 logit 统计量、能量分数，还是欧氏/马氏距离——本质上都在度量“幅度”或“距离”层面的异常。本文的评分机制被**替换为** **Energy Profile Divergence (EPD)**：在核心特征子空间内，对 L₁ 归一化的能量轮廓计算 KL 散度。

具体流程分为两步。首先，对每个类别计算其训练样本稀疏激活向量的均值，形式化为**类激活轮廓（Class Activation Profiles, CAPs）**——这是传统方法中不存在的结构化类别参考。CAP 捕捉了每个 ID 类在稀疏空间中“能量如何分配”的基准形状。其次，在推理时，取测试样本预测类别 CAP 的前 L 个核心索引，分别构建测试样本和 CAP 的 L₁ 归一化能量分布 $ \mathbf{P} $ 和 $ \mathbf{Q} $，并计算 KL 散度作为 OOD 分数：

$$ \mathrm{EPD~Score} = D_{\mathrm{KL}}(\mathbf{P} \parallel \mathbf{Q}) = \sum_{i=1}^L \mathbf{P}_i \log\left(\frac{\mathbf{P}_i}{\mathbf{Q}_i}\right) $$

这一设计的核心洞察在于：ID 样本在稀疏潜在空间中维持尖锐、高能量的激活头部，而 OOD 样本尽管能被错误分类到某个 ID 类，却无法复制该能量分布的“形状”——其激活轮廓呈现平坦、扩散的结构。EPD 通过 L₁ 归一化消除了幅度差异的影响，专门捕捉这种结构性破坏，从而构成了比幅度差异更鲁棒的 OOD 检测信号。

### 创新机制的证据链

上述创新的有效性由多项实验证据支撑。**Figure 2** 的热力图显示，不同 ID 类的核心特征集合几乎正交，Jaccard 相似性系数接近于零，验证了稀疏空间为每个类提供了近乎独立的特征子空间。**Figure 5** 和 **Figure 6** 则揭示了 OOD 样本的行为模式：它们系统性地激活了所预测 ID 类的核心特征，但激活强度低于真实 ID 样本，且激活轮廓呈现显著的平坦化——这正是 EPD 所捕获的结构性差异。消融实验进一步证实，在同一稀疏 CAP 框架下，EPD（KL 散度）在所有评估分裂上均优于欧氏距离和余弦距离，而硬稀疏本身是区分 ID 与 OOD 的关键：软稀疏会允许 OOD 输入产生弥漫的低幅度激活，模糊结构差异，硬瓶颈则放大了这种偏差。

### 需注意的边界

尽管创新点清晰且证据充分，仍有几点值得关注：硬稀疏的 k 值目前通过网格搜索固定为 128，是否可设计为类别或样本自适应的动态机制以进一步提升近 OOD 检测性能，尚待探索；此外，Top‑k SAE 学到的稀疏基中每个活跃神经元对应的高层视觉语义尚未被细粒度可视化，这限制了创新机制的可解释性边界。

## 整体框架

EPD 方法将 OOD 检测重新表述为一个**结构匹配问题**，而非传统的幅度或距离比较。其核心 pipeline 由两个阶段构成：**设置阶段**与**推理阶段**（参见 Figure 1）。

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our OOD detection framework. In the (a) Setup Phase, a Top-k SAE is trained on [CLS] tokens extracted from a fixed, pre-trained ViT using ID data. This process learns disentangled latent features, which are aggregated to form CAPs. In the (b) Inference Phase, the latent activation distribution of a test sample is compared against the predicted class’s CAP using our Energy Profile Divergence (EPD) score to compute the final OOD score*

### 设置阶段：稀疏空间构建与类模板提取

该阶段的目标是在 ID 数据上建立一个解纠缠的稀疏表示空间，并为每个类别提取一个规范化的激活模板。

1.  **特征提取**：使用一个冻结的预训练 ViT 对 ID 训练集进行前向传播，提取其 `[CLS]` 令牌作为密集特征向量。
2.  **稀疏重参数化**：训练一个过完整的单隐藏层 Top‑k 稀疏自编码器（Top‑k SAE）。该 SAE 的输入和输出均为 `[CLS]` 令牌，但其瓶颈层施加了**硬稀疏约束**：对每个样本，仅保留激活值最大的 $k$ 个神经元，其余全部置零。训练目标为最小化重建损失（MSE）与辅助损失之和：
    $$ \mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Recon}} + \alpha \mathcal{L}_{\mathrm{AuxK}} $$
    其中辅助损失 $\mathcal{L}_{\mathrm{AuxK}}$ 用于鼓励“死神经元”参与重建。此步骤将密集的 `[CLS]` 令牌重新参数化为一个稀疏、可解释的潜在基。
3.  **CAP 构建**：对于每个类别 $c$，收集其所有 ID 训练样本的稀疏激活向量，计算均值向量 $\bar{\mathbf{h}}^c$，并将其定义为该类别的**类激活轮廓（CAP）**。CAP 捕捉了该类在稀疏空间中特有的、规范化的激活模式，作为后续比较的基准。

### 推理阶段：基于能量轮廓散度的 OOD 评分

给定一个测试样本，推理阶段量化其激活模式的“形状”与预测类别 CAP 的偏离程度。

1.  **稀疏编码与类别预测**：将测试样本的 `[CLS]` 令牌输入训练好的 Top‑k SAE，得到其稀疏激活向量 $\mathbf{h}^s$。同时，利用 ViT 的分类头获得其预测类别 $\hat{c}$。
2.  **核心特征对齐**：选取预测类别 CAP（$\bar{\mathbf{h}}^{\hat{c}}$）中均值最大的前 $L$ 个索引 $M^{\hat{c}}$，从 CAP 和样本激活 $\mathbf{h}^s$ 中分别取出对应的 $L$ 维核心向量：
    $$ \mathbf{C}_i = \bar{\mathbf{h}}_{M_i^{\hat{c}}}^{\hat{c}}, \quad \mathbf{S}_i = \mathbf{h}_{M_i^{\hat{c}}}^s $$
3.  **能量轮廓归一化**：对两个核心向量进行 $L_1$ 归一化，将其投影到单纯形上，得到仅反映能量分配“形状”的概率分布轮廓 $\mathbf{P}$（样本）和 $\mathbf{Q}$（类别基准）：
    $$ \mathbf{P}_i = \frac{\mathbf{S}_i}{\sum_{i=1}^L \mathbf{S}_i}, \quad \mathbf{Q}_i = \frac{\mathbf{C}_i}{\sum_{i=1}^L \mathbf{C}_i} $$
4.  **散度评分**：计算 $\mathbf{P}$ 相对于 $\mathbf{Q}$ 的 KL 散度，作为最终的 OOD 分数——**能量轮廓散度（EPD）**：
    $$ \mathrm{EPD~Score} = D_{\mathrm{KL}}(\mathbf{P} \parallel \mathbf{Q}) = \sum_{i=1}^L \mathbf{P}_i \log\left(\frac{\mathbf{P}_i}{\mathbf{Q}_i}\right) $$
    该分数直接度量了测试样本的能量分布形态与 ID 类基准的**结构性偏离**：ID 样本的 $\mathbf{P}$ 与 $\mathbf{Q}$ 形状高度一致（低 EPD），而 OOD 样本即使能激活部分核心特征，其能量分布也呈现平坦、扩散的形态，无法复制 CAP 的尖锐头部，从而产生高 EPD 分数。

## 核心模块与公式推导

### 整体框架

EPD 方法由两个阶段构成（Figure 1）。在设置阶段，一个 Top‑k 稀疏自编码器（Top‑k SAE）在固定预训练 ViT 的 [CLS] 令牌上训练，将密集表示重新参数化为稀疏、可解释的潜在基。随后，对每个 ID 类别聚合训练样本的稀疏激活向量，构建类激活轮廓（Class Activation Profiles, CAPs）。在推理阶段，测试样本的潜在激活分布与其预测类别的 CAP 进行对比，通过能量轮廓散度（Energy Profile Divergence, EPD）计算最终的 OOD 分数。

### 关键模块一：Top‑k 稀疏自编码器

**设计动机。** 现有 OOD 检测方法将 ViT [CLS] 令牌视为一个纠缠的密集表示，仅依赖幅度或欧氏距离，无法区分真正的语义相似性与虚假的几何邻近性。Top‑k SAE 通过硬稀疏约束，强制每个输入仅激活最显著的 k 个特征，将密集表示分解为结构化的稀疏激活向量，从而暴露前向结构中激活模式的“形状”信息。

**硬稀疏机制。** 与使用 ℓ₁ 或 KL 散度惩罚实现平均稀疏的传统 SAE 不同，Top‑k SAE 执行逐样本硬稀疏：在编码器输出中，仅保留激活值最高的 k 个神经元，其余全部置零。这一硬瓶颈放大了 ID 样本的稳定激活模式与 OOD 样本的破坏性模式之间的结构差异。

**损失函数。** 总损失由重建损失和辅助损失组成：

$$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{Recon}} + \alpha \mathcal{L}_{\mathrm{AuxK}}$$

其中 $\mathcal{L}_{\mathrm{Recon}}$ 为均方误差（MSE）重建损失，$\mathcal{L}_{\mathrm{AuxK}}$ 为鼓励“死神经元”参与重建的辅助损失，$\alpha$ 为平衡系数。该损失函数旨在学习一个过完整的单隐藏层自编码器，使其稀疏潜在空间既能保持重建能力，又能形成类别特异性的激活模板。

### 关键模块二：类激活轮廓（CAP）

**构建方式。** 对于每个 ID 类别 $c$，CAP 定义为该类所有训练样本的稀疏激活向量的均值：

$$\bar{\mathbf{h}}^c = \frac{1}{N_c} \sum_{j=1}^{N_c} \mathbf{h}_j^c$$

其中 $\mathbf{h}_j^c$ 为类别 $c$ 中第 $j$ 个样本经过 Top‑k SAE 编码后的稀疏激活向量，$N_c$ 为该类样本数。CAP 捕捉了每个类别在稀疏潜在空间中的典型能量分配模式，作为该类别的基准参考模板。

**核心特征索引。** 定义 $M^c$ 为类别 $c$ 的 CAP $\bar{\mathbf{h}}^c$ 中激活值最大的 $L$ 个神经元的索引数组。这 $L$ 个核心特征索引用于后续的能量轮廓提取与散度计算。

### 关键模块三：能量轮廓散度（EPD）

**核心激活向量提取。** 对于测试样本 $s$，首先通过 Top‑k SAE 编码器获得稀疏激活向量 $\mathbf{h}^s$。设其预测类别为 $c$，从类别 CAP 和样本激活中分别取出 $L$ 个核心索引对应的值，形成 $L$ 维核心激活向量：

$$\mathbf{C}_i = \bar{\mathbf{h}}_{M_i^c}^c, \quad \mathbf{S}_i = \mathbf{h}_{M_i^c}^s$$

其中 $M_i^c$ 为类别 $c$ 的第 $i$ 个核心特征索引。

**L₁ 归一化。** 将核心激活向量投影到 $(L-1)$ 维单纯形上，消除尺度影响，仅保留能量分配的“形状”信息：

$$\mathbf{P}_i = \frac{\mathbf{S}_i}{\sum_{i=1}^L \mathbf{S}_i}, \quad \mathbf{Q}_i = \frac{\mathbf{C}_i}{\sum_{i=1}^L \mathbf{C}_i}$$

$\mathbf{P}$ 为测试样本的归一化能量分布轮廓，$\mathbf{Q}$ 为预测类别的归一化基准轮廓。

**EPD 评分。** 使用 KL 散度度量两个能量分布轮廓之间的“形状”偏离：

$$\mathrm{EPD~Score} = D_{\mathrm{KL}}(\mathbf{P} \parallel \mathbf{Q}) = \sum_{i=1}^L \mathbf{P}_i \log\left(\frac{\mathbf{P}_i}{\mathbf{Q}_i}\right)$$

高 EPD 值表示测试样本的能量分布形状与 ID 类别的基准轮廓存在显著结构性差异，即样本破坏了 ID 类的核心特征层次，从而被判定为 OOD。这一机制的核心优势在于：ID 样本在稀疏潜在空间中维持尖锐、高能量的激活头部，而 OOD 样本尽管可能被错误分类到某个 ID 类，却无法复制该能量分布的“形状”，呈现平坦、扩散的轮廓——这种结构性破坏（而非幅度差异）构成了鲁棒的 OOD 检测信号。

### 超参数配置

经网格搜索确定的关键超参数为：潜在维度 $D_{\mathrm{latent}} = 7680$，稀疏度 $k = 128$，激活头比例 $p = 0.15$（即 $L = p \times D_{\mathrm{latent}}$）。消融实验表明，$p$ 在 0.12–0.20 范围内性能稳定，所选配置在 FPR95 和 AUROC 之间取得最佳平衡。

### 补充图表

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/002_Figure_2.jpg]]
*Figure 2: Pairwise Jaccard similarity of core feature sets across all 1,000 ImageNet classes. Each cell represents the overlap between the core feature of a class pair. The off-diagonal region indicates near-zero similarity between the core feature sets of different classes. Lighter colors indicate low similarity, while darker colors indicate high similarity*

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/003_Figure_3.jpg]]
*Figure 3: Activation affinity of OOD samples to specific ID core features. The plots compare activations of ID samples (Blue) and misclassified OOD samples (Red) on specific core feature sets. Top: OOD samples from iNaturalist predicted as ‘Class 738 (plantpot)’ show high activation on the core features of Class 738. Bottom: The same OOD samples show negligible activation on the core features of an unrelated class (‘Class 989, rosehip’). This illustrates that OOD samples are not random but structurally align with their predicted class*

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/006_Figure_6.jpg]]
*Figure 6: Structural differences in ID and OOD activation. We compare the mean activation profiles of ID samples (Blue) and misclassified OOD samples (Red) sorted by the ID CAP. Top: iNaturalist vs. ID (Class 986). Bottom: OpenImage-O vs. ID (Class 309). In both cases, ID samples maintain a sharp, concentrated head, whereas OOD samples exhibit a flattened, diffused profile. Shaded regions indicate variance*

## 实验与分析

### 主实验结果

在 ImageNet-1K 基准上，EPD 方法在 ViT-B/16 主干网络下取得了最优的平均 FPR95（40.96%），超越所有对比基线，包括 **RMDS**（43.40%），FPR95 绝对值降低 2.44 个百分点（Table 1）。在 AUROC 指标上，EPD 以 87.26% 的平均值位居第二，与第一名 RMDS（87.60%）差距仅为 0.34 个百分点，表明该方法在保持高可分离性的同时，显著降低了高置信度误判率。

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/007_Table_1.jpg]]
*Table 1: OOD detection performance on ViT-B/16 (ID Acc: 81.14%). Results are averaged across Near-OOD and Far-OOD datasets. Best results are in bold; second and third-best are underlined. Our method achieves the best average FPR95*

按数据集细分（Table 2），EPD 在多个场景下展现出差异化的优势：在 OpenImage-O 上 FPR95 低至 26.03%（AUROC 92.12%），在 iNaturalist 上 FPR95 为 17.84%（AUROC 95.17%），表现出对远分布 OOD 样本的强鲁棒性；在近分布 OOD 的 SSB-Hard 上 FPR95 为 82.41%（AUROC 72.21%），性能下降明显，反映出近分布语义混淆场景仍是该方法的薄弱环节。

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/008_Table_2.jpg]]
*Table 2: Detailed our OOD detection performance on ViT-B/16. Best results are in bold; second and third-best are underlined*

### 跨架构泛化分析

在 Swin Transformer（Swin-T）上，EPD 的平均 FPR95 为 43.59%（Table 3），弱于 ViT-B/16 上的 40.96%，且被 RMDS（41.37%）反超。这一退化与 Swin Transformer 的局部窗口注意力和层次化特征聚合机制有关：全局一致性的减弱导致 CAP 的激活头部尖锐度降低，从而削弱了基于形状对齐的 EPD 评分对结构性差异的敏感度。

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/009_Table_3.jpg]]
*Table 3: OOD detection performance on Swin Transformer (ID Acc: 81.60%). Results are averaged across Near-OOD and Far-OOD datasets. Best results are in bold; second and third-best are underlined*

在 DINOv2 B/14 上，EPD 取得了所有主干中的最佳整体 FPR95（40.50%），且该主干本身具有最高的 ID 分类准确率（84.64%）（Table 7）。该结果验证了更强的自监督预训练表示能够为稀疏分解提供更高质量的特征基底，进而提升结构检测机制的效能。需要指出的是，DINOv2 上的对比仅限于内部比较，缺乏已发表 OOD 基准的完整竞争力分析，该结论的泛化性需进一步验证。

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/018_Table_7.jpg]]
*Table 7: OOD Detection performance of our method across different architectures. Detailed OOD detection performance on ImageNet-1K benchmarks for our proposed method (EPD) applied to DINOv2 B/14 (ID Acc: 84.64%), ViT-B/16 (ID Acc: 81.14%), and Swin-T (ID Acc: 81.60%)*

### 消融实验

**度量方式消融**（Table 4）：在相同的稀疏 CAP 框架下，将 EPD 的 KL 散度替换为欧氏距离或余弦距离，在所有评估分裂上均导致 FPR95 上升和 AUROC 下降。这一结果验证了 KL 散度在 (L-1) 维单纯形上度量能量分布“形状”偏离的独特优势——欧氏距离和余弦距离无法有效捕捉高维稀疏向量中能量分配的层次结构差异。

**稀疏性机制消融**：硬稀疏（Top-k）是区分 ID 与 OOD 的关键瓶颈。软稀疏惩罚（如 ℓ₁ 或 KL 正则）允许 OOD 输入产生弥漫的低幅度激活，模糊了 ID 类特有的尖锐激活头部与 OOD 样本平坦扩散轮廓之间的结构差异。Top-k 通过强制每样本仅保留 k 个最大激活并清零其余，放大了这一结构性偏差，使 EPD 能够可靠地检测到形状破坏信号（Section 4.2）。

**超参数敏感性**（Figure 10）：对潜在维度 L 和稀疏度 k 进行网格搜索的结果表明，所选配置（L=7680, k=128）在 FPR95 和 AUROC 之间取得了最优平衡。更大的 L 或更小的 k 虽能进一步提升稀疏性，但会导致信息损失和 AUROC 下降。

**激活头比例 p 的稳定性**（Figure 11）：在 p ∈ [0.12, 0.20] 的范围内，EPD 在多个 OOD 基准上的 FPR95 和 AUROC 均保持稳定，所选 p=0.15 位于该稳定区间内，表明方法对该超参数不敏感。

### 失败模式与局限性

1. **近分布 OOD 退化**：在 SSB-Hard 等语义高度重叠的近分布 OOD 场景中，EPD 的 FPR95 高达 82.41%。此时 OOD 样本与 ID 类的核心特征集合存在显著重叠，激活轮廓的形状差异不足以提供清晰的分离边界。

2. **Swin Transformer 上的性能衰减**：如前所述，层次化局部注意力架构削弱了全局激活轮廓的尖锐度，导致 CAP 的判别力下降。该问题反映了方法对 Transformer 变体的全局表示质量存在依赖性。

3. **DINOv2 对比不完整**：该主干上的对比缺乏已发表的 OOD 基线结果，无法进行完整的竞争力评估。

4. **架构范围受限**：当前验证仅覆盖 ViT 家族（ViT-B/16、Swin-T、DINOv2），尚未扩展到 ConvNeXt 等 CNN 架构或多模态模型，方法的架构通用性有待进一步验证。

5. **训练与存储开销**：SAE 训练虽为一次性成本（约 17 分钟），但在极高维特征空间或实时部署场景中，过完备字典的存储和推理开销仍需关注。

### 补充图表

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/015_Table_4.jpg]]
*Table 4: Metric Ablation on ViT-B/16. EPD outperforms Euclidean and cosine distance across all evaluation splits, validating the use of KL divergence over normalized energy profiles*

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/013_Figure_10.jpg]]
*Figure 10: Hyperparameter sensitivity analysis. FPR95 (blue, lower is better) and AUROC (red, higher is better) across combinations of latent dimension (L) and sparsity level (k). Darker colors indicate better performance. The selected configuration*

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/014_Figure_11.jpg]]
*Figure 11: Sensitivity analysis of the activation head ratio (p). Performance metrics, FPR95 (Left) and AUROC (Right), are evaluated across various OOD benchmarks as a function of the activation head ratio (p). The ratio determines the size of the sorted latent feature set used for divergence calculation. The results demonstrate the stability of our proposed method EPD across the empirically derived meaningful range (p = 0.12 to p = 0.20), validating the robust selection of the chosen value (p = 0.15) used in the main paper*

![[assets/figures/papers/paper_list_l931_https_arxiv_org_abs_2604_26409/figures/005_Figure_5.jpg]]
*Figure 5: Global statistics of activation intensity. We aggregate mean activations on core indices across all classes for two OOD datasets: iNaturalist (Left) and OpenImage-O (Right). ID Ground Truth (Blue, Left): Strong activation on ground-truth core features. OOD Matched (Red, Middle): OOD samples activate the core features of their predicted class, but with lower intensity than ID. OOD Other Classes (Red, Right): OOD samples show minimal activation on unrelated classes*

## 方法谱系与知识库定位

### 1. 与现有 OOD 检测范式的关键分歧

本工作与现有基于 ViT 的 OOD 检测方法存在一个根本性的设计分歧：**特征空间从“纠缠的密集表示”转向“结构化的稀疏潜在表示”**。

现有方法——包括 **MSP**（最大 softmax 概率）、**ODIN**、基于 **Mahalanobis 距离** 的 MDS 及其变体 **RMDS**、**ViM**、**ReAct**、**KNN**，以及作者自行实现的 **MDS++** 和 **RMDS++**——均将 ViT 的 [CLS] 令牌视为一个完整的密集向量。它们的 OOD 评分机制依赖 logit 统计量、能量函数、欧氏距离或马氏距离，本质上是在度量幅度或几何邻近性。这一范式的瓶颈在于：密集表示中语义相似性与虚假的几何邻近性相互纠缠，无法区分“真正的分布外”与“落在 ID 流形边缘的分布内样本”。

本工作提出的 **EPD（Energy Profile Divergence）** 框架做出了四个关键替换：

| 组件 | 现有范式 | 本工作 |
|------|---------|--------|
| 特征空间 | 密集的 ViT [CLS] 令牌或其线性投影 | Top‑k SAE 编码的稀疏激活向量 |
| 稀疏约束 | 无稀疏性或软稀疏惩罚（ℓ₁ / KL） | 硬稀疏（Top‑k，每样本仅保留 k 个最大激活） |
| 类别参考 | 无结构化类别模板 | 类激活轮廓（CAP）：每个类的 L 维核心特征均值向量 |
| OOD 评分 | logit 统计量 / 能量 / 欧氏距离 / 马氏距离 | Energy Profile Divergence（EPD）：L₁ 归一化能量轮廓的 KL 散度 |

核心洞察在于：**ID 样本在稀疏潜在空间中维持尖锐、高能量的激活头部，而 OOD 样本尽管能被错误分类到某个 ID 类，却无法复制该能量分布的“形状”**。这种结构性破坏（而非幅度差异）构成了鲁棒的 OOD 检测信号。消融实验（Table 4）证实，在同一稀疏 CAP 框架下，EPD（KL 散度）在所有评估分裂上均优于欧氏距离和余弦距离，验证了“形状度量”优于“幅度度量”的设计选择。

### 2. 与稀疏自编码器文献的关系

本工作采用 **Top‑k SAE**（Gao et al., 2024; Makhzani & Frey, 2014）作为特征解纠缠的工具，但其使用方式与 SAE 在语言模型可解释性中的典型应用存在重要差异：

- **目的不同**：传统 SAE 用于从语言模型残差流中提取可解释的单体特征（monosemantic features），追求重建保真度与稀疏性的平衡。本工作使用 SAE 的目标不是重建损失最小化或距离度量，而是将密集的 ViT [CLS] 令牌重新参数化为一个稀疏的、可解释的潜在基，服务于下游的 OOD 检测。
- **稀疏约束的选择**：本工作明确选择了硬稀疏（Top‑k）而非软稀疏（ℓ₁ 或 KL 惩罚）。消融分析（Section 4.2）表明，软稀疏会允许 OOD 输入产生弥漫的低幅度激活，模糊 ID 与 OOD 之间的结构差异；而 Top‑k 的硬瓶颈强制每样本仅激活 k 个最显著特征，放大了 ID 稳定模式（CAP）与 OOD 破坏模式之间的结构性偏差。这一发现构成了本工作的关键因果旋钮。

### 3. 适用边界与跨架构泛化

本方法的有效性已在三个 ViT 家族主干上得到验证，但性能表现揭示了清晰的适用边界：

- **ViT‑B/16**：取得最优平均 FPR95（40.96%），在所有对比方法中排名第一（Table 1）。在 OpenImage‑O（FPR95 26.03%）和 iNaturalist（FPR95 17.84%）等 Far‑OOD 数据集上表现尤为突出，但在 SSB‑Hard（FPR95 82.41%）等 Near‑OOD 场景下仍面临挑战。
- **DINOv2**：取得所有主干中的最佳整体 FPR95（40.50%）（Table 7），但该实验仅进行了内部比较，缺乏已发表 OOD 基准的完整竞争力分析，该结论需要手动验证。
- **Swin‑T**：整体性能弱于 ViT‑B/16（平均 FPR95 43.59% vs. 40.96%），且被 RMDS（41.37%）超越。作者将此归因于 Swin Transformer 基于窗口的局部注意力和层次化特征聚合导致全局一致性较弱，CAP 的尖锐度降低，影响了形状对齐的效果。这一退化揭示了本方法对“全局一致的特征表示”的依赖性——当主干网络无法产生足够紧凑的类别表征时，稀疏分解带来的结构性优势会被削弱。

当前方法仅针对图像分类任务中的 ViT 家族验证，尚未扩展到其他架构（如 ConvNeXt）或多模态模型。

### 4. 已知局限

1. **语义可解释性缺失**：尽管 Top‑k SAE 学到的稀疏基在功能上有效，但未对单个潜在神经元的语义进行细粒度可视化，无法明确揭示哪些视觉概念（如物体部件、纹理）被编码。这限制了方法在需要可解释 OOD 决策的场景中的应用。

2. **主干依赖性**：如 Swin‑T 实验所示，当主干网络的全局表示能力不足时，CAP 的尖锐度下降，EPD 的形状对齐效果减弱。方法对“高质量全局特征”的依赖构成了实际部署中的潜在风险。

3. **计算开销**：SAE 训练虽为一次性成本（约 17 分钟），但在极高维或实时场景中，训练和存储开销仍需关注。此外，推理时需要额外的前向传播通过 SAE 编码器。

4. **DINOv2 评估不完整**：该主干上的对比仅限于内部比较，缺乏与其他已发表 OOD 方法的直接竞争力分析。

### 5. 开放问题

1. **稀疏基的语义对齐**：Top‑k SAE 学到的稀疏基中，每个活跃神经元对应的高层视觉语义如何与人类可解释概念（如物体部件、纹理）对齐？这需要结合特征可视化技术进行系统研究。

2. **自适应稀疏度**：当前硬稀疏的 k 值是全局固定的。是否可以设计类别自适应或样本自适应的动态 k 值机制，以进一步提升近 OOD 检测性能？

3. **跨模态迁移**：该框架是否能迁移到文本‑图像多模态 Transformer（如 CLIP）的表示空间？如何构建模态共享的 CAP 是一个具有挑战性的开放问题。

4. **CAP 的在线更新**：在持续学习或分布逐渐漂移的场景下，CAP 是否需要在线更新以维持其作为不变参考的有效性？静态 CAP 在非平稳环境中的退化行为尚未被研究。

5. **更优的发散度量**：除了 KL 散度，是否存在更适合高维稀疏单纯形的几何发散度量（如 Wasserstein 距离或 Hellinger 距离），可进一步放大结构性差异？当前消融仅比较了欧氏距离和余弦距离，更广泛的度量空间探索仍属空白。

## 原文 PDF

![[paperPDFs/CVPR_2026/Sparsity_as_a_Key_Unlocking_New_Insights_from_Latent_Structures_for_Out_of_Distribution_Detection.pdf]]

---
title: "Unlearning without Forgetting: Securely Removing Targeted Concepts from Large-Scale Vision-Language Open-Vocabulary Detectors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unlearning_without_Forgetting_Securely_Removing_Targeted_Concepts_from_Large_Scale_Vision_Language_Open_Vocabulary_Detectors.pdf
project_link: null
code_link: null
aliases:
- Unlearning_witho
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将参数更新约束到保留知识嵌入的零空间，通过构建零空间投影 P_null 并只应用 P_null · ΔW，从数学上阻止遗忘更新影响保留概念方向。
primary_logic: 利用 VLM 嵌入空间的线性可分解性，通过离线构建保留概念的零空间，将遗忘与保留几何解耦，实现安全且无干扰的遗忘。
claims:
- 无约束 MU 的遗忘更新在保留子空间上有非零投影，导致几何纠缠干扰。
- 通过零空间投影，参数更新被约束到保留子空间的正交补，消除一阶干扰。
- SafeDetect 在 UOD-Bench 上比 NPO 遗忘效果提升 64.75%，且保持稳定保留和优秀零样本泛化。
- SafeDetect 收敛速度比迭代方法快 1.5 倍，在 500 步内稳定收敛，NPO 约需 750 步。
---

# Unlearning without Forgetting: Securely Removing Targeted Concepts from Large-Scale Vision-Language Open-Vocabulary Detectors

> [!tip] 核心洞察
> 利用 VLM 嵌入空间的线性可分解性，通过离线构建保留概念的零空间，将遗忘与保留几何解耦，实现安全且无干扰的遗忘。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无遗忘的遗忘学习：安全移除大规模视觉-语言开放词汇检测器中的目标概念 |
| 英文题名 | Unlearning without Forgetting: Securely Removing Targeted Concepts from Large-Scale Vision-Language Open-Vocabulary Detectors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_Unlearning_without_Forgetting_Securely_Removing_Targeted_Concepts_from_Large-Scale_Vision-Language_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SafeDetect |
| Dataset | UOD-Bench, LVIS-minival zero-shot generalization, Training Convergence |

> [!tip] 效果简介
> - UOD-Bench (OD task, 1% forget ratio, LLM-Det Swin-T) 上，U-Score (↑) 23.5 vs NPO (更低，具体值未提供) (显著优于 NPO，遗忘效果提升 64.75%)。
> - LVIS-minival zero-shot generalization 上，AP Avg. Drop (↓) 8.3 vs 14.2 (NPO) (5.9 点的平均下降更少，泛化性能更好)。
> - Training Convergence (steps to stabilize) 上，Convergence Steps 500 vs ~750 (NPO) (1.5× 加速收敛)。

## 概要

大规模视觉-语言模型（VLM）驱动的开放词汇检测器（OvOD）能够识别任意文本描述的目标，但其训练数据源自互联网大规模爬取，不可避免地包含隐私敏感、版权受限或不合规的视觉概念。传统的解决方案——从零开始重新训练——在计算成本和时间上均不可行。机器遗忘（Machine Unlearning, MU）旨在从已训练模型中高效移除特定知识，但在开放词汇检测场景下面临一个根本性瓶颈：**VLM 嵌入空间的线性可分解性导致几何纠缠干扰**。

具体而言，VLM 文本嵌入具有可分解结构，一个概念的嵌入可表示为全局偏移量与若干语义因子理想词向量的线性组合（Eq. 2.1）。这意味着遗忘目标（如“人脸”）与保留概念（如“人”）共享底层语义因子。当无约束的 MU 方法对模型参数施加遗忘更新 $\Delta W$ 时，该更新在保留概念嵌入方向 $\mathbf{f}_c$ 上产生非零投影，形成一阶对齐干扰 $\Delta^{(1)}\mathrm{align}(c) = \langle \Delta W, \mathbf{f}_c \rangle \neq 0$（Eq. 2.3）。这种干扰不仅损害保留类别的检测性能，还严重削弱零样本泛化能力。

针对上述瓶颈，本文提出 **SafeDetect**——一个几何约束的检测遗忘框架。其核心洞察是：利用 VLM 嵌入空间的线性可分解性，通过离线构建保留概念嵌入的零空间投影 $P_{\mathrm{null}}$，将参数更新约束至保留子空间的正交补，从数学上阻断遗忘更新对保留概念的干扰。具体而言，SafeDetect 的参数更新遵循 $W' = W + P_{\mathrm{null}} \cdot \Delta W$（Eq. 4.6），确保对任意保留概念 $c$ 均满足 $\langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0$（Eq. 4.4），实现遗忘与保留的几何解耦。在此基础上，SafeDetect 通过单向流损失驱动遗忘类别输出趋向均匀分布，并结合跨模态解耦损失在解码器查询特征层面实现深层语义排斥，完成安全、无干扰的概念移除。

实验结果表明，SafeDetect 在 UOD-Bench 基准上相较于 **NPO**（Zhang et al., 2024）等无约束遗忘方法，遗忘效果提升 **64.75%**，同时保持稳定的保留性能和显著更优的零样本泛化能力（LVIS-minival 上平均 AP 仅下降 8.3 点，而 NPO 下降 14.2 点）。此外，SafeDetect 收敛速度比迭代方法快 **1.5 倍**，在 500 步内即可稳定收敛。

### 开放词汇检测中的遗忘困境

大规模视觉-语言模型（VLMs）的开放词汇检测能力依赖于网络规模数据的预训练，这使其能够检测几乎任意文本描述的目标。然而，这种无差别的检测能力也带来了严重的隐私与合规风险：模型可能检测到人脸、身份证号等敏感概念，而传统的解决方案——从零开始重新训练——在大规模模型时代已变得成本高昂且不切实际。因此，**机器遗忘（Machine Unlearning, MU）** 作为一种高效、经济的替代方案应运而生，其目标是在不重新训练的前提下，选择性地移除模型中的特定概念。

### 现有方法的几何纠缠瓶颈

当前主流的机器遗忘方法采用无约束的参数更新策略，通过平衡遗忘损失与保留损失来优化模型。其典型形式为：

$$
\mathcal{L}_{\mathrm{MU}} = \lambda_f \mathcal{L}_{\mathrm{forget}} + \lambda_r \mathcal{L}_{\mathrm{retain}}.
$$

然而，这类方法在开放词汇检测场景下暴露出一个根本性问题：**几何纠缠干扰（Geometric Entanglement Interference）**。VLM 的文本嵌入空间具有线性可分解性——一个概念的嵌入可表示为全局偏移量与构成因子理想词向量的叠加：

$$
\bar{\ell}_{z} = \bar{\ell}_{0} + \sum_{i=1}^{k} \bar{\ell}_{z_i}, \quad \mathrm{where} \quad \sum_{z_i \in \mathcal{Z}_i} \bar{\ell}_{z_i} = \mathbf{0}.
$$

正是这种共享语义因子的组合性，使得遗忘更新不可避免地投影到保留概念的子空间上。从数学上看，遗忘更新 $\Delta W_f$ 对保留概念 $c$ 产生的一阶对齐干扰非零：

$$
\Delta^{(1)} \mathrm{align}(c) = \langle \Delta W_f, \mathbf{f}_c \rangle \neq 0.
$$

这意味着，当我们试图遗忘“人脸”时，与“人脸”共享底层语义因子（如“人”）的相关概念也会受到干扰，导致保留性能下降和零样本泛化能力受损。**NPO**（Negative Preference Optimization, Zhang et al., 2024）等现有方法正是受困于这种几何纠缠——它们缺乏一种机制来将遗忘更新与保留知识的几何结构解耦。

### 核心动机：几何安全遗忘

本文的核心动机源于一个关键洞察：**利用 VLM 嵌入空间的线性可分解性，可以通过离线构建保留概念的零空间，将遗忘与保留在几何上彻底解耦**。具体而言，如果能将参数更新约束到保留知识嵌入的正交补空间（即零空间），就能从数学上阻止遗忘更新影响保留概念方向，实现一阶干扰的消除：

$$
\Delta^{(1)} \mathrm{align}(c) = \langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0, \quad \forall c \in \mathcal{C}_{\mathrm{retain}}.
$$

这一几何约束范式为安全、无干扰的遗忘提供了理论保障，也是 SafeDetect 方法设计的根本出发点。

## 核心方法与创新机理

SafeDetect 的核心创新在于将机器遗忘问题从“损失平衡”范式重新定义为“几何约束”范式。传统方法（如 **NPO**，Zhang et al., 2024）通过加权组合遗忘损失和保留损失 $ \mathcal{L}_{\mathrm{MU}} = \lambda_f \mathcal{L}_{\mathrm{forget}} + \lambda_r \mathcal{L}_{\mathrm{retain}} $ 来驱动参数更新，但这种无约束的梯度更新在 VLM 嵌入空间中会不可避免地产生几何纠缠干扰。

### 瓶颈洞察：几何纠缠干扰

SafeDetect 的关键洞察建立在对 VLM 嵌入线性可分解性的分析之上。在开放词汇检测器中，概念嵌入 $ \bar{\ell}_{z} $ 可分解为全局偏移量与构成因子理想词向量的和：

$$ \bar{\ell}_{z} = \bar{\ell}_{0} + \sum_{i=1}^{k} \bar{\ell}_{z_i}, \quad \mathrm{where} \quad \sum_{z_i \in \mathcal{Z}_i} \bar{\ell}_{z_i} = \mathbf{0}. $$

这种组合性意味着遗忘概念与保留概念在嵌入空间中共享语义因子。当无约束的遗忘更新 $ \Delta W_f $ 发生时，其与保留概念嵌入 $ \mathbf{f}_c $ 的内积非零，产生一阶对齐干扰：

$$ \Delta^{(1)} \mathrm{align}(c) = \langle \Delta W_f, \mathbf{f}_c \rangle \neq 0. $$

这解释了为何现有方法在遗忘目标概念时会不可避免地损害语义相关概念的检测能力（如遗忘 "face" 时干扰 "man"、"boy" 的检测）。

### 核心机制：零空间投影约束

SafeDetect 的核心创新是将参数更新约束到保留知识嵌入的零空间中，从数学上彻底消除一阶干扰。具体而言，方法离线构建保留概念的嵌入矩阵 $ \mathbf{F}_r $，通过 SVD 分解获得保留子空间的正交基 $ \mathbf{U}_r $，进而构造零空间投影器：

$$ P_{\mathrm{null}} = I - P_{\mathrm{keep}} = I - \mathbf{U}_r \mathbf{U}_r^T. $$

参数更新被分解为切向分量（干扰保留）和法向分量（保留不变）：

$$ \Delta W = P_{\mathrm{keep}} \Delta W + P_{\mathrm{null}} \Delta W. $$

仅保留法向分量进行参数更新 $ W^{\prime} = W + P_{\mathrm{null}} \cdot \Delta W $，从而确保：

$$ \Delta^{(1)} \mathrm{align}(c) = \langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0, \quad \forall c \in \mathcal{C}_{\mathrm{retain}}. $$

### 三层 changed slots 对比

相较于以 NPO 为代表的无约束遗忘基线，SafeDetect 在三个关键维度上实现了范式转变：

| 维度 | 基线方法 (NPO) | SafeDetect | 证据锚点 |
|------|---------------|------------|----------|
| **参数更新机制** | 无约束梯度更新 $ \Delta W = -\eta\nabla_W \mathcal{L}_{\mathrm{MU}} $ | 零空间投影更新 $ W^{\prime} = W + P_{\mathrm{null}} \cdot \Delta W $ | Eq. 4.6 |
| **遗忘目标函数** | 平衡遗忘和保留损失 $ \mathcal{L}_{\mathrm{MU}} = \lambda_f \mathcal{L}_{\mathrm{forget}} + \lambda_r \mathcal{L}_{\mathrm{retain}} $ | 单向流损失 $ \mathcal{L}_{\mathrm{flow}} $（驱动输出趋近均匀分布）与跨模态解耦损失 $ \mathcal{L}_{\mathrm{decouple}} $ 的组合 | Eq. 4.7, 4.8, 4.9 |
| **跨模态遗忘深度** | 仅抑制最终分类输出（浅层遗忘） | 在解码器查询特征级别进行语义排斥，实现深层表征遗忘 | Sec 4.3, Eq. 4.8 |

### 遗忘深度的创新：从输出抑制到表征解耦

SafeDetect 的第二个关键创新是将遗忘从分类头输出层面推进到解码器查询特征层面。跨模态解耦损失 $ \mathcal{L}_{\mathrm{decouple}} $ 通过最小化视觉查询特征与遗忘概念文本嵌入的相似度矩阵对角元素，在表征空间中主动排斥遗忘概念：

$$ \mathcal{L}_{\mathrm{decouple}} = \mathbb{E}_{(v,f) \in \mathcal{D}_f} \left[ \ell_{\mathrm{CE}}(-\mathbf{S}, \mathbf{I}) + \ell_{\mathrm{CE}}(-\mathbf{S}^{\top}, \mathbf{I}) \right] / 2. $$

消融实验证实了这一设计的有效性：在解码器查询特征级别进行解耦的 U-Score 为 23.5，显著优于在 bbox 头部特征级别解耦的 19.8（1% 遗忘比例，Table 5）。这表明深层表征解耦比浅层输出抑制更能实现彻底的语义遗忘。

### 几何约束的实证优势

零空间约束带来的优势在多个维度得到验证。在收敛性上，SafeDetect 在 500 步内稳定收敛，比 NPO（约需 750 步）快 1.5 倍（Figure 5）。在零样本泛化保护上，移除零空间投影（w/o Null）导致 LVIS 上的平均 AP 下降从 3.8 增加到 9.6（Table 4），证实了零空间约束对保护泛化能力的关键作用。

SafeDetect 的整体框架围绕一个核心几何约束展开：**将遗忘更新限制在保留知识嵌入的零空间中**，从而在数学上阻断遗忘操作对保留概念的干扰。该框架由离线构建与在线训练两个阶段组成，如图1所示。

### 离线阶段：零空间构建

在训练开始前，框架首先利用保留概念的文本嵌入矩阵 $\mathbf{F}_r$ 进行奇异值分解，构建保留子空间的正交投影算子 $P_{\mathrm{keep}} = \mathbf{U}_r \mathbf{U}_r^T$。由此得到零空间投影器：

$$P_{\mathrm{null}} = I - P_{\mathrm{keep}} = I - \mathbf{U}_r \mathbf{U}_r^T$$

该投影器确保任意参数更新 $\Delta W$ 被分解为切向分量 $P_{\mathrm{keep}} \Delta W$（与保留子空间对齐，造成干扰）和法向分量 $P_{\mathrm{null}} \Delta W$（与保留子空间正交，安全无害）。框架仅保留法向分量用于参数更新，从根源上消除一阶对齐干扰：

$$\Delta^{(1)} \mathrm{align}(c) = \langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0, \quad \forall c \in \mathcal{C}_{\mathrm{retain}}$$

### 在线阶段：约束遗忘训练

在线训练阶段，SafeDetect 在零空间约束下优化两个互补的损失函数，实现深层语义遗忘：

1. **单向流遗忘损失** $\mathcal{L}_{\mathrm{flow}}$：驱动遗忘类别的检测输出概率趋近均匀分布 $\mathcal{U}$，使模型对遗忘概念产生“非检测”状态：
   $$\mathcal{L}_{\mathrm{flow}}^{(\mathcal{D}_f)} = \mathbb{E}_{\boldsymbol{x} \in \mathcal{D}_f} \mathrm{KL}(\mathrm{softmax}(\mathbf{z}_{\theta}(x)/\tau), \mathcal{U})$$

2. **跨模态解耦损失** $\mathcal{L}_{\mathrm{decouple}}$：在解码器查询特征级别进行视觉与文本模态间的语义排斥，推动遗忘概念的跨模态相似度矩阵对角元素最小化：
   $$\mathcal{L}_{\mathrm{decouple}} = \mathbb{E}_{(v,f) \in \mathcal{D}_f} \left[ \ell_{\mathrm{CE}}(-\mathbf{S}, \mathbf{I}) + \ell_{\mathrm{CE}}(-\mathbf{S}^{\top}, \mathbf{I}) \right] / 2$$

最终的参数更新在零空间投影约束下执行：

$$W^{\prime} = W + P_{\mathrm{null}} \cdot \Delta W$$

统一优化目标为：

$$\mathcal{L}_{\mathrm{total}}^{(\mathcal{D}_f)} = \lambda_{\mathrm{flow}} \mathcal{L}_{\mathrm{flow}}^{(\mathcal{D}_f)} + \lambda_{\mathrm{decouple}} \mathcal{L}_{\mathrm{decouple}}^{(\mathcal{D}_f)}$$

### 模块间数据流

框架的数据流可概括为以下步骤：

1. **文本嵌入提取**：从保留类别文本中提取嵌入向量，构建 $\mathbf{F}_r$，离线计算 $P_{\mathrm{null}}$。
2. **参数更新计算**：前向传播计算 $\mathcal{L}_{\mathrm{flow}}$ 和 $\mathcal{L}_{\mathrm{decouple}}$，反向传播得到原始梯度 $\Delta W$。
3. **零空间投影**：将 $\Delta W$ 乘以 $P_{\mathrm{null}}$，滤除与保留子空间对齐的分量。
4. **约束参数应用**：将投影后的更新 $P_{\mathrm{null}} \cdot \Delta W$ 应用到检测模型的分类头、解码器查询特征以及 LoRA 适配器参数上。

该设计使得遗忘更新在几何上与保留知识完全解耦——图4的 T-SNE 可视化证实，SafeDetect 在遗忘“face”概念时，语义相关类（man, boy）的聚类结构保持紧凑，而 NPO 方法则因几何纠缠导致相关类别出现显著分散。训练收敛方面，SafeDetect 在 500 步内即可稳定收敛，相比 NPO（约 750 步）实现 1.5 倍加速（图5）。

![[assets/figures/papers/paper_list_l802_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unlearning_without/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the unlearning challenge and our proposed method. (a) Previous Methods: Large-scale pretraining on webscraped data leads to uncontrolled detection, creating (c) significant privacy/compliance risks. Retraining is prohibitively costly. (b) Our method decomposes updates into tangential component Pkeep · ∆W (discarded, causes interference) and normal component Pnull · ∆W (retained, safe). Applying null-space projection (W ′ = W + Pnull · ∆W ) avoids geometric entanglement between related concepts (e.g., “Woman” and “Person”). (d) This achieves safe, reliable unlearning by selectively forgetting targets while retaining generalized concepts at minimal cost*

### 问题形式化：几何纠缠干扰的数学根源

开放词汇检测器依赖视觉-语言模型（VLM）的文本嵌入空间进行概念匹配。该嵌入空间具有**线性可分解性**：概念 $z$ 的嵌入 $\bar{\ell}_{z}$ 可分解为全局偏移量 $\bar{\ell}_{0}$ 与构成因子理想词向量 $\bar{\ell}_{z_i}$ 的和，且因子向量和为零：

$$
\bar{\ell}_{z} = \bar{\ell}_{0} + \sum_{i=1}^{k} \bar{\ell}_{z_i}, \quad \mathrm{where} \quad \sum_{z_i \in \mathcal{Z}_i} \bar{\ell}_{z_i} = \mathbf{0}.
$$

这种组合性意味着遗忘概念与保留概念在嵌入空间中共享语义因子。当传统机器遗忘方法施加无约束参数更新 $\Delta W$ 时，遗忘损失 $\mathcal{L}_{\mathrm{MU}} = \lambda_f \mathcal{L}_{\mathrm{forget}} + \lambda_r \mathcal{L}_{\mathrm{retain}}$ 产生的梯度更新会对保留概念 $c$ 产生**一阶对齐干扰**：

$$
\Delta^{(1)} \mathrm{align}(c) = \langle \Delta W_f, \mathbf{f}_c \rangle \neq 0.
$$

该非零内积量化了遗忘更新在保留概念方向上的投影，导致保留性能下降和零样本泛化能力受损。

### 核心模块一：保留嵌入矩阵构建与零空间投影

SafeDetect 的核心原理是将参数更新约束到保留知识嵌入的零空间中。设 $\mathbf{F}_r \in \mathbb{R}^{d \times |\mathcal{C}_{\mathrm{retain}}|}$ 为保留概念文本嵌入矩阵，要求所有参数更新 $\Delta W$ 满足 $\Delta W \cdot \mathbf{F}_r = \mathbf{0}$。

通过对 $\mathbf{F}_r$ 进行奇异值分解（SVD），构建保留子空间投影 $P_{\mathrm{keep}}$ 和零空间投影 $P_{\mathrm{null}}$：

$$
P_{\mathrm{null}} = I - P_{\mathrm{keep}} = I - \mathbf{U}_r \mathbf{U}_r^T.
$$

其中 $\mathbf{U}_r$ 为 $\mathbf{F}_r$ 的前 $r$ 个左奇异向量构成的矩阵。该投影器将任意参数更新 $\Delta W$ 分解为切向分量 $P_{\mathrm{keep}} \Delta W$（干扰保留）和法向分量 $P_{\mathrm{null}} \Delta W$（保留不变）：

$$
\Delta W = P_{\mathrm{keep}} \Delta W + P_{\mathrm{null}} \Delta W.
$$

通过仅保留法向分量，一阶对齐干扰被严格消除：

$$
\Delta^{(1)} \mathrm{align}(c) = \langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0, \quad \forall c \in \mathcal{C}_{\mathrm{retain}}.
$$

最终的约束参数更新形式为：

$$
W^{\prime} = W + P_{\mathrm{null}} \cdot \Delta W.
$$

该模块离线预计算保留文本嵌入 $\{\mathbf{f}_c\}$ 和零空间投影器 $\tilde{P}_{\mathrm{null}}$，对不同模块（分类头、解码器查询、LoRA 适配器）分别应用相应的零空间投影，确保参数更新正交于保留子空间。

### 核心模块二：单向流遗忘损失

为驱动遗忘类别的检测输出趋向不可检测状态，SafeDetect 采用单向流遗忘损失，通过最小化遗忘类别预测分布与均匀分布 $\mathcal{U}$ 之间的 KL 散度实现：

$$
\mathcal{L}_{\mathrm{flow}}^{(\mathcal{D}_f)} = \mathbb{E}_{\boldsymbol{x} \in \mathcal{D}_f} \mathrm{KL}(\mathrm{softmax}(\mathbf{z}_{\theta}(x)/\tau), \mathcal{U}).
$$

其中 $\mathbf{z}_{\theta}(x)$ 为检测输出 logits，$\tau$ 为温度系数。该损失直接推动模型对遗忘概念产生无偏预测，实现“非检测”状态，而非仅抑制最终分类输出。

### 核心模块三：跨模态解耦损失

为在解码器查询特征级别实现深层表征遗忘，SafeDetect 引入跨模态解耦损失。设视觉解码器查询特征与遗忘概念文本嵌入的相似度矩阵为 $\mathbf{S}$，通过最小化其对角元素实现语义排斥：

$$
\mathcal{L}_{\mathrm{decouple}} = \mathbb{E}_{(v,f) \in \mathcal{D}_f} \left[ \ell_{\mathrm{CE}}(-\mathbf{S}, \mathbf{I}) + \ell_{\mathrm{CE}}(-\mathbf{S}^{\top}, \mathbf{I}) \right] / 2.
$$

该损失推动解码器查询特征与遗忘概念文本嵌入的对角相似度趋向负值，在视觉与文本模态间建立语义排斥关系，实现超越表层输出抑制的深层表征解耦。

### 统一遗忘目标

在零空间约束下，组合单向流遗忘损失和跨模态解耦损失构成统一优化目标：

$$
\mathcal{L}_{\mathrm{total}}^{(\mathcal{D}_f)} = \lambda_{\mathrm{flow}} \mathcal{L}_{\mathrm{flow}}^{(\mathcal{D}_f)} + \lambda_{\mathrm{decouple}} \mathcal{L}_{\mathrm{decouple}}^{(\mathcal{D}_f)}.
$$

训练时启用 LoRA（rank $r=128$，$\alpha=256$）进行参数高效微调，$\lambda_{\mathrm{flow}}$ 和 $\lambda_{\mathrm{decouple}}$ 均设为 1.0，$\tau=0.07$，学习率为 $2 \times 10^{-5}$。

## 实验与关键发现

### 主实验结果：多任务遗忘性能

SafeDetect 在 UOD-Bench 上进行了全面的多任务评估，覆盖目标检测（OD）、短语定位（PG）和指代表达理解（REC）三项核心能力，并在四个遗忘比例（1%、5%、10%、15%）下与多个基线方法进行对比。UOD-Bench 包含 14.7K 张图像和 67.3K 个区域-短语对，为评估提供了标准化的遗忘-保留权衡基准。

**核心性能指标** 采用 U-Score——遗忘下降幅度与保留性能的调和平均值，越高表示遗忘与保留的综合平衡越好。在 LLM-Det (Swin-T) 骨干网络下，SafeDetect 在 OD 任务 1% 遗忘比上取得 U-Score 23.5，相比 **NPO**（Zhang et al., 2024）实现 64.75% 的遗忘效果提升，同时保持更优的保留性能（Table 1）。这一提升的根源在于零空间投影机制从数学上阻止了遗忘更新对保留概念子空间的干扰：无约束 MU 方法中，遗忘更新 $\Delta W_f$ 与保留概念嵌入 $\mathbf{f}_c$ 的一阶对齐 $\Delta^{(1)} \mathrm{align}(c) = \langle \Delta W_f, \mathbf{f}_c \rangle \neq 0$，导致几何纠缠干扰；而 SafeDetect 通过 $P_{\mathrm{null}}$ 投影确保 $\Delta^{(1)} \mathrm{align}(c) = \langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0, \forall c \in \mathcal{C}_{\mathrm{retain}}$，从根本上消除了一阶干扰。

随着遗忘比例从 1% 增至 15%，SafeDetect 的遗忘 mAP 从 17.8% 上升至 30.8%（Table 3, Full 配置），表明遗忘强度与遗忘概念数量呈正相关，但始终在 U-Score 上保持对 NPO 的显著优势。在 PG 和 REC 任务上，SafeDetect 同样展现出精确的目标概念移除能力，同时保留其他概念的检测性能，而 NPO 则出现不完全遗忘和保留类别性能退化的问题。

![[assets/figures/papers/paper_list_l802_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unlearning_without/figures/008_Table_3.jpg]]
*Table 3: Ablation study of SafeDetect’s core components on UOD-Bench with LLM-Det (Swin-T) for OD task*

### 零样本泛化能力

遗忘操作对模型零样本泛化能力的影响是评估方法安全性的关键维度。Table 2 展示了在 LVIS-minival 和 COCO 数据集上的泛化表现：SafeDetect 在 LVIS 上的平均 AP 下降仅为 8.3 点，而 NPO 为 14.2 点，差距达 5.9 点。这表明零空间投影不仅保护了已知保留概念的检测能力，还通过保持嵌入空间的几何结构完整性，维护了模型对未见概念的泛化能力。

![[assets/figures/papers/paper_list_l802_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unlearning_without/figures/007_Table_2.jpg]]
*Table 2: Impact of unlearning on zero-shot generalization. We evaluate on LVIS-minival [18] and COCO [32] with LLM-Det (Swin-T). Higher is better*

消融实验（Table 4）进一步验证了这一结论：移除零空间投影后（w/o Null），LVIS 上的平均 AP 下降从 3.8 点急剧增加至 9.6 点，证实零空间约束是保护零样本泛化的核心机制。

### 收敛速度与训练效率

SafeDetect 在训练效率上展现出显著优势。如 Figure 5 所示，几何约束的遗忘训练在 500 步内稳定收敛至负值稳定状态，而 NPO 约需 750 步才能收敛，实现了 1.5 倍的加速。更重要的是，NPO 在高遗忘比例下出现越来越大的训练震荡，这是几何纠缠干扰的直接表现：当遗忘子空间与保留子空间的交集增大时，无约束梯度更新的冲突加剧。SafeDetect 通过将更新约束至保留子空间的正交补，避免了这种震荡，保持稳定的收敛曲线。

![[assets/figures/papers/paper_list_l802_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unlearning_without/figures/005_Figure_5.jpg]]
*Figure 5: Training loss comparison across four forgetting ratios (1%, 5%, 10%, 15%). Green (Ours): Geometrically constrained unlearning converges rapidly within 500 steps with stable negative values. Red (NPO): NPO exhibits increasing oscillations at higher ratios due to geometric entanglement interference (Eq. 2.3) between larger forget/retain subspaces*

### 消融研究：核心组件贡献

Table 3 系统性地消融了 SafeDetect 的三大核心组件：

- **完整 SafeDetect（Flow + Decouple + Null）**：在 OD 任务 1% 遗忘比下，遗忘 mAP 为 17.8%，10% 时为 30.8%，综合性能最优。
- **移除零空间投影（w/o Null）**：遗忘效果虽有所保留，但保留性能和泛化能力显著下降，证实零空间是保护保留知识的关键。
- **移除跨模态解耦损失（w/o Decouple）**：遗忘效果下降，说明仅靠输出层面的流损失不足以实现深层表征遗忘。
- **仅使用流损失（Flow only）**：遗忘能力最弱，表明深层语义排斥对于彻底遗忘至关重要。

跨模态解耦的深度选择（Table 5）揭示了另一个关键发现：在解码器查询特征级别进行解耦比在 bbox 头部特征级别更有效，U-Score 分别为 23.5 和 19.8（1% 比例）。这是因为解码器查询特征处于更深层的语义表征空间，在此层面进行模态间语义排斥能够更彻底地切断遗忘概念的视觉-语言关联，而非仅仅抑制最终分类输出。

### 鲁棒性分析

Table 6 展示了 SafeDetect 对语义扰动的鲁棒性。在原始类别名称（如 "dog"）和同义词（如 "canine"）两种条件下，SafeDetect 均能保持稳定的遗忘性能。这一鲁棒性源于跨模态解耦损失在解码器查询特征层面的深层语义排斥机制，使得遗忘不仅针对特定文本标签，而是对遗忘概念的语义簇产生泛化效应。

### 定性分析

Figure 4 的 T-SNE 可视化直观展示了遗忘 "face" 概念时特征空间的变化。原始模型中，face 样本形成紧密聚类；NPO 由于几何纠缠干扰，导致语义相关类（man、boy）的特征分布显著分散；而 SafeDetect 通过零空间保护，保持了所有保留类别的紧凑聚类结构。Figure 2 和 Figure 6 的定性检测结果进一步证实：SafeDetect 能够精确移除目标概念（如 face、woman），同时完整保留其他类别（如 bowl、chair）的检测能力，而现有方法则出现遗忘不彻底或保留类别丢失的问题。

![[assets/figures/papers/paper_list_l802_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unlearning_without/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative comparison of unlearning effectiveness on open-vocabulary object detection. Given text prompt with retain categories (bowl, chair, cup, dining table, knife) and forget targets (face, woman): (a) Open detectors detect all categories including privacy-sensitive concepts. (b) Existing methods struggle to forget targets and degrade retain categories (bowl detection lost). (c) SafeDetect achieves precise forgetting while preserving detection capabilities*

![[assets/figures/papers/paper_list_l802_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Unlearning_without/figures/004_Figure_4.jpg]]
*Figure 4: T-SNE visualization of feature space when unlearning “face”. Square markers indicate semantically related classes (man, boy) sharing features with the forget target; circle markers denote general classes. In Original, face samples (red triangles) cluster tightly with clear boundaries. Retrain achieves perfect concept removal but requires costly full retraining. NPO exhibits significant dispersion in related classes due to geometric entanglement interference*

Figure 7 展示了跨模态对齐的演化过程：解耦目标驱动解码器查询特征与遗忘概念文本嵌入的相似度从接近零下降至 -0.6 至 -0.8 的强负值，实现了视觉与文本模态间的语义排斥，这超越了浅层输出抑制，达到了深层表征级别的解耦。

### 待验证观察与开放问题

尽管 SafeDetect 在 UOD-Bench 上表现优异，以下方面仍需进一步验证或探索：

- **不同架构的泛化性**：当前实验基于 LLM-Det 骨干，SafeDetect 在 GroundingDINO 等其他 VLM 检测架构上的表现需要手动验证。
- **高度重叠概念的鲁棒性**：对于语义高度重叠的概念对（如 "dog" 与 "puppy"），零空间构建的区分能力是否足够，论文未提供专门实验。
- **动态连续遗忘**：当前实验为单次遗忘设定，多次连续遗忘不同概念时零空间的累积效应和更新策略是重要的开放问题。
- **对抗安全性**：遗忘后模型面对特征提取攻击时的安全性尚未评估，这是实际部署中需要关注的风险点。

## 定位与知识库关联

### 问题定位：开放词汇检测中的机器遗忘

开放词汇目标检测（OvOD）利用视觉-语言模型（VLM）的联合嵌入空间，实现了对任意文本描述的目标检测。然而，大规模网络数据预训练使得模型可能检测到隐私敏感或合规受限的概念（如人脸、特定身份），而完全重新训练的成本过高。现有机器遗忘（Machine Unlearning, MU）方法主要针对分类任务设计，直接迁移到 OvOD 场景时面临根本性挑战：VLM 嵌入的线性可分解性导致遗忘更新与保留概念在几何空间产生纠缠干扰。

具体而言，根据 Eq. 2.1 的可分解嵌入性质，概念 $z$ 的嵌入可表示为 $\bar{\ell}_{z} = \bar{\ell}_{0} + \sum_{i=1}^{k} \bar{\ell}_{z_i}$，其中 $\sum_{z_i \in \mathcal{Z}_i} \bar{\ell}_{z_i} = \mathbf{0}$。这意味着语义相关概念（如“woman”与“person”）共享构成因子，导致无约束 MU 方法（Eq. 2.2: $\mathcal{L}_{\mathrm{MU}} = \lambda_f \mathcal{L}_{\mathrm{forget}} + \lambda_r \mathcal{L}_{\mathrm{retain}}$）产生的参数更新 $\Delta W_f$ 在保留子空间上产生非零投影，形成一阶对齐干扰 $\Delta^{(1)} \mathrm{align}(c) = \langle \Delta W_f, \mathbf{f}_c \rangle \neq 0$（Eq. 2.3），从而损害保留类别的检测性能和零样本泛化能力。

### 方法谱系：从无约束遗忘到几何约束遗忘

**NPO (Negative Preference Optimization)**（Zhang et al., 2024）代表了当前无约束知识遗忘的典型范式。NPO 通过平衡遗忘损失和保留损失的加权组合进行参数更新，其核心思路是在损失函数层面同时优化两个对抗性目标。然而，如本文所揭示，NPO 在 OvOD 场景中面临几何纠缠干扰：当遗忘比例增大时，遗忘子空间与保留子空间的交叠加剧，导致训练损失出现递增振荡（Fig. 5），收敛缓慢（约需 750 步），且对语义相关类别产生显著的性能退化（Fig. 4 的 T-SNE 可视化显示 NPO 导致相关类别特征分散）。

**SafeDetect** 在方法论上实现了从“损失平衡”到“几何解耦”的范式转变。其核心创新在于三个层面的方法改进：

**1. 参数更新机制的根本重构。** 无约束方法采用 $\Delta W = -\eta\nabla_W \mathcal{L}_{\mathrm{MU}}$ 进行全空间梯度更新，而 SafeDetect 引入零空间投影器 $P_{\mathrm{null}} = I - \mathbf{U}_r \mathbf{U}_r^T$（Eq. 4.2），将参数更新约束为 $W' = W + P_{\mathrm{null}} \cdot \Delta W$（Eq. 4.6）。这一约束从数学上保证了对所有保留概念 $c \in \mathcal{C}_{\mathrm{retain}}$ 的一阶对齐变化为零：$\Delta^{(1)} \mathrm{align}(c) = \langle P_{\mathrm{null}} \Delta W, \mathbf{f}_c \rangle = 0$（Eq. 4.4），实现了遗忘与保留在几何空间的正交解耦。

**2. 遗忘目标的单向流设计。** 相比传统方法需要精心平衡 $\lambda_f$ 和 $\lambda_r$ 两个超参数，SafeDetect 采用单向流损失 $\mathcal{L}_{\mathrm{flow}}^{(\mathcal{D}_f)} = \mathbb{E}_{\boldsymbol{x} \in \mathcal{D}_f} \mathrm{KL}(\mathrm{softmax}(\mathbf{z}_{\theta}(x)/\tau), \mathcal{U})$（Eq. 4.7），直接驱动遗忘类别的检测输出趋向均匀分布 $\mathcal{U}$，使其进入“不可检测”状态。该设计避免了保留损失带来的优化冲突，简化了超参数调优。

**3. 跨模态遗忘深度的拓展。** 无约束方法通常仅在最终分类输出层面抑制遗忘概念（浅层遗忘），而 SafeDetect 引入跨模态解耦损失 $\mathcal{L}_{\mathrm{decouple}}$（Eq. 4.8），在解码器查询特征层面最小化视觉特征与遗忘概念文本嵌入的相似度，实现深层表征的语义排斥。消融实验（Table 5）证实，解码器特征级别的解耦（U-Score 23.5）显著优于 bbox 头部特征级别（U-Score 19.8），验证了深层遗忘的必要性。

### 适用边界与局限性

**适用前提。** SafeDetect 的有效性建立在 VLM 嵌入空间的线性可分解性假设之上（Eq. 2.1），该假设在基于 Transformer 的 VLM（如 LLM-Det）中得到了经验验证。方法要求能够获取保留概念的文本嵌入以离线构建零空间投影器 $P_{\mathrm{null}}$，因此适用于保留概念集合已知且可枚举的场景。

**计算开销。** 零空间投影器的构建涉及对保留嵌入矩阵 $\mathbf{F}_r$ 的 SVD 分解，计算复杂度为 $O(n d^2)$（其中 $n$ 为保留概念数，$d$ 为嵌入维度）。但该过程完全离线完成，不增加训练时的计算负担。配合 LoRA（rank=128, α=256）进行参数高效微调，整体遗忘训练仅需约 500 步即可收敛，比 NPO 快 1.5 倍。

**语义重叠边界。** 当遗忘概念与保留概念高度语义重叠时（如“dog”与“puppy”），它们在嵌入空间中的因子共享程度更高，零空间的有效维度可能显著缩小，从而限制可用的安全更新方向。Table 6 的同义词扰动实验表明，SafeDetect 对语义变体（如“dog” vs “canine”）仍保持一定的鲁棒性，但极端重叠场景下的性能边界仍需进一步验证。

### 开放问题

1. **架构泛化性。** 当前验证基于 LLM-Det（Swin-T 和 ResNet-50 骨干），SafeDetect 在其他 VLM 检测架构（如 GroundingDINO、OWL-ViT）上的有效性尚待确认。不同架构的嵌入空间几何结构可能存在差异，影响零空间构建的质量。

2. **动态遗忘场景。** 当前方法假设一次性遗忘固定概念集合。在实际应用中，可能需要多次连续遗忘不同概念（如按法规更新逐步移除新受限制类别）。每次遗忘后保留嵌入矩阵和零空间投影器需要更新，累积的近似误差对长期遗忘稳定性的影响需要研究。

3. **自动化概念发现。** SafeDetect 依赖人工指定需要遗忘的文本标签。如何自动识别模型中存储的敏感概念（如通过嵌入空间聚类或对抗探测）是一个开放问题，直接影响方法在实际部署中的可用性。

4. **安全性保障的完备性。** 虽然零空间投影从数学上消除了一阶对齐干扰，但面对自适应攻击（如通过精心设计的提示词工程或中间特征提取尝试恢复遗忘概念）时，模型的鲁棒性尚未得到充分评估。深层表征解耦（Eq. 4.8）提供了一定程度的保护，但其对抗鲁棒性的理论下界尚不明确。

5. **多模态遗忘的一致性。** 当前方法侧重于文本到视觉的单向遗忘（通过文本嵌入定义遗忘目标）。在真正的多模态场景中，遗忘概念可能通过视觉特征相似性被间接恢复，跨模态遗忘的一致性问题值得深入探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Unlearning_without_Forgetting_Securely_Removing_Targeted_Concepts_from_Large_Scale_Vision_Language_Open_Vocabulary_Detectors.pdf]]

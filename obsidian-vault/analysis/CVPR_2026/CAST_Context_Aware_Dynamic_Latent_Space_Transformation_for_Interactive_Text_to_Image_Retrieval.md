---
title: "CAST: Context-Aware Dynamic Latent Space Transformation for Interactive Text-to-Image Retrieval"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CAST_Context_Aware_Dynamic_Latent_Space_Transformation_for_Interactive_Text_to_Image_Retrieval.pdf
project_link: null
code_link: "https://github.com/HuiGuanLab/CAST"
aliases:
- CCALSTCCASR
- CAST
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 对话上下文（用户意图演变）驱动的多模态特征空间动态变换：低秩投影方向（CLP）决定语义搜索方向，上下文引导调制强度（CGM）决定变换幅度。
primary_logic: 通过引入上下文感知低秩投影（CLP）和上下文引导调制（CGM）两种轻量级机制，首次在交互式文本到图像检索中实现多模态特征空间随对话语义动态演变。CLP学习在低秩子空间中投影特征，沿意图相关方向变形语义流形；CGM根据初始与当前上下文语义差异自适应调节变换强度，确保稳定且表达力强的空间演化，从而实现细粒度检索对齐。
claims:
- 现有方法将对话文本和图像映射到固定的嵌入流形，导致语义模糊，难以捕捉意图的微妙变化。
- CAST通过动态变换文本和视觉表示的共同潜在空间，根据随对话演变的用户意图实现自适应语义对齐。
- CLP学习投影方向，CGM控制投影强度，两者协同使特征空间随用户意图动态变换。
- VisDial 上 R@1 (Round 1) = 43.60%
---

# CAST: Context-Aware Dynamic Latent Space Transformation for Interactive Text-to-Image Retrieval

> [!tip] 核心洞察
> 通过引入上下文感知低秩投影（CLP）和上下文引导调制（CGM）两种轻量级机制，首次在交互式文本到图像检索中实现多模态特征空间随对话语义动态演变。CLP学习在低秩子空间中投影特征，沿意图相关方向变形语义流形；CGM根据初始与当前上下文语义差异自适应调节变换强度，确保稳定且表达力强的空间演化，从而实现细粒度检索对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向交互式文本到图像检索的上下文感知动态潜在空间变换 |
| 英文题名 | CAST: Context-Aware Dynamic Latent Space Transformation for Interactive Text-to-Image Retrieval |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lin_CAST_Context-Aware_Dynamic_Latent_Space_Transformation_for_Interactive_Text-to-Image_Retrieval_CVPR_2026_paper.html) · [Code](https://github.com/HuiGuanLab/CAST) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CAST (Context-Aware Latent Space Transformation)，核心模块为CASR (Context-Aware Space Regulator) |
| Dataset | VisDial |

> [!tip] 效果简介
> - VisDial 上，R@1 (Round 1) 43.60% vs 42.78% (ChatIR) (+0.82%)；R@1 (Round 10) 57.56% vs 53.15% (ChatIR) (+4.41%)；R@1 (Round 1) 43.60% vs 40.31% (BLIP zero-shot) (+3.29%)。

## 概要

交互式文本到图像检索（I-TIR）要求系统根据多轮对话逐步理解并精炼用户的搜索意图。现有方法在**整个对话过程中始终使用固定的多模态嵌入空间**进行跨模态匹配，这一静态范式导致用户意图随对话轮次演变的语义变化无法被捕捉——当用户新增属性（如“黑色的”）或细化对象关系（如“在草地上”）时，细微的上下文线索极易在静态特征空间中丢失，限制了细粒度检索精度。

针对这一瓶颈，本文提出 **CAST**（Context-Aware Latent Space Transformation，上下文感知动态潜在空间变换），其核心思想是让多模态特征空间**随对话语义动态演变**，而非保持静态。CAST 通过一个轻量级的上下文感知空间调节器 **CASR**（Context-Aware Space Regulator）实现这一目标，该模块由两个协同组件构成：

- **上下文感知低秩投影器（CLP）**：学习在低秩子空间中预测投影方向，沿意图相关方向变形语义流形，决定特征空间“往哪里变”。
- **上下文引导调制器（CGM）**：根据初始上下文与当前上下文的语义差异自适应调节变换强度，决定特征空间“变多少”。

这种“方向 + 强度”的双重控制机制，使 CAST 能够稳定且表达力强地驱动特征空间随用户意图演化，从而在每一轮对话中实现更精准的文本-图像语义对齐。此外，CAST 可**无缝集成**到现有 I-TIR 架构中，仅需极小的计算开销（在秩 r=8 时，约 0.002 秒即可完成 50,000 张图像的特征变换）。

在 VisDial 基准上的实验表明，CAST 在对话后期轮次中优势尤为显著：第 10 轮 R@1 达到 57.56%，相比最优基线 ChatIR（53.15%）提升 **+4.41 个百分点**，验证了动态空间变换在捕捉累积上下文语义方面的关键价值。

### 交互式文本到图像检索的现实需求

文本到图像检索旨在根据自然语言描述从大规模图像库中找到相关图像。在许多真实场景中，用户往往难以用单次查询精确表达其需求，因此需要通过多轮对话逐步澄清和细化搜索意图。这种**交互式文本到图像检索（Interactive Text-to-Image Retrieval, I-TIR）**范式允许用户通过问答循环不断调整查询，直到定位到目标图像。

### 现有方法的瓶颈：静态多模态特征空间

当前主流的交互式检索方法——包括基于大语言模型（LLM）进行对话生成和查询重写的**ChatIR**（Levy et al., NeurIPS 2023）、即插即用式对话上下文生成的**PlugIR**（Lee et al., ACL 2024），以及利用多模态大模型统一推理的**ImageScope**（Luo et al., WWW 2025）——在架构上共享一个根本性局限：**它们在整个多轮对话过程中使用固定的多模态嵌入空间进行跨模态匹配**。

具体而言，这些方法将对话历史和候选图像分别编码后，在同一个静态特征空间中计算余弦相似度作为检索得分：

$$s_t = \text{sim}(f_T(\mathcal{H}_t), f_I(I))$$

其中 $\mathcal{H}_t = C_0, (Q_1, A_1), (Q_2, A_2), \ldots, (Q_t, A_t)$ 表示第 $t$ 轮对话历史。

这种静态表述带来了一个关键问题：**用户意图随对话轮次不断演变，但特征空间的几何结构始终保持不变**。当用户在第1轮询问“一只狗”而在第10轮细化到“一只在草地上奔跑的黑色拉布拉多”时，静态空间难以有效捕捉这些新增属性（颜色、动作、场景）和细化的对象关系。原文明确指出，这种静态形式“容易导致语义模糊，难以捕捉用户更新意图中的微妙嵌入偏移”（Abstract）。结果是，细粒度的上下文线索在固定的语义流形中易于丢失，限制了后期对话轮次的检索精度。

### 核心动机：特征空间应随对话语义动态演变

本文的核心动机如图1所示：**不同于在整个搜索过程中使用单一静态多模态特征空间，我们应当根据逐步细化的用户搜索意图，自适应地利用多个动态特征空间**。每个动态空间应针对用户在对应轮次所关注的特定“主题”具有更强的判别力。

这一动机催生了本文的核心科学问题：**能否设计一种轻量级机制，使多模态特征空间随对话上下文的演变而动态变换，从而在每一轮对话中提供更具语义区分度的检索空间？**

### 技术挑战

实现上述目标面临两个直接挑战：

1. **变换方向的选择**：特征空间应向哪个方向变形，才能沿着用户意图相关的语义维度增强判别力？这需要一个能够根据对话上下文预测投影方向的机制。
2. **变换强度的控制**：不同对话轮次之间用户意图的变化幅度不同——从“一只狗”到“一只黑狗”的语义偏移远小于从“一只狗”到“一只在草地上奔跑的黑色拉布拉多”。因此，变换的幅度需要自适应调节，而非固定不变。

本文提出的**CAST（Context-Aware Latent Space Transformation）**框架通过两个协同模块——**上下文感知低秩投影器（CLP）**和**上下文引导调制器（CGM）**——分别解决上述两个挑战，首次在交互式文本到图像检索中实现了多模态特征空间随对话语义的动态演变。

## 核心方法与创新机理

CAST的核心创新在于**首次将交互式文本到图像检索中的多模态特征空间从“静态固定”转变为“上下文感知动态演变”**。现有方法（如ChatIR、PlugIR、ImageScope）在整个多轮对话过程中始终使用同一个预训练好的嵌入空间进行跨模态相似度计算，这一静态范式导致用户意图随对话轮次逐步细化的语义变化无法被特征空间捕捉，细微的上下文线索（如新增的颜色属性、细化的空间关系）容易在固定的语义流形中被淹没。

CAST通过一个轻量级的**上下文感知空间调节器（Context-Aware Space Regulator, CASR）** 解决了上述瓶颈。CASR由两个协同工作的模块组成，分别控制特征空间变换的**方向**和**强度**：

- **上下文感知低秩投影器（Context-Aware Low-Rank Projector, CLP）**：负责学习特征空间变换的投影方向。CLP根据当前对话上下文$u_t$预测两个低秩投影矩阵$A_t, B_t \in \mathbb{R}^{d \times r}$（$r \ll d$），将原始特征$x_t$先投影到一个紧凑的低秩子空间，再回升到原始维度，形成上下文条件的方向性变换$\mathcal{P}(x_t \mid u_t) = (x_t \hat{B}_t) \hat{A}_t^{\top}$。这一机制使特征空间能够沿用户意图相关的语义方向变形，例如当对话聚焦于颜色属性时，空间会被重塑以突出颜色差异。

- **上下文引导调制器（Context-Guided Modulator, CGM）**：负责自适应控制变换的幅度。CGM通过比较初始上下文$u_0$与当前上下文$u_t$的语义差异，预测一个调制系数$\alpha_t = \sigma(\mathrm{MLP}([u_0; u_t]))$，用于缩放CLP的投影输出$\mathcal{F}(x_t \mid u_t) = \alpha_t \cdot \mathcal{P}(x_t \mid u_t)$。这一设计确保当用户意图发生显著变化时施加更大的空间变换，而在意图微调时保持适度调整，避免过度扭曲语义结构。

最终的动态空间变换采用残差连接和层归一化实现：$\mathcal{G}(x_t \mid u_t) = \mathrm{LN}(x_t + \mathcal{F}(x_t \mid u_t))$，文本和图像特征分别经过变换后得到$z_t^T$和$z_t^I$，再在新空间中计算余弦相似度进行检索排序。

**与baseline的核心差异**可归纳为以下changed slots：

| 模块 | 静态baseline（ChatIR等） | CAST |
|------|--------------------------|------|
| 多模态特征空间 | 固定静态，全对话轮次共享 | 根据对话上下文$u_t$动态变换 |
| 特征变换机制 | 无（仅使用预训练编码器输出） | CASR：CLP控制方向 + CGM控制强度 |
| 检索相似度计算 | 原始特征空间中的余弦相似度 | 经CASR变换后的动态空间中的余弦相似度 |

消融实验（Table 2）验证了每个模块的独立贡献：引入CLP将10轮平均R@10从79.89提升至80.90，进一步加入CGM后达到82.05。对比实验（Table 3, Table 4）表明，低秩分解结构优于非分解的上下文感知矩阵（82.05 vs 80.57），上下文引导调制器优于上下文无关的可学习标量（82.05 vs 81.51），证实了“方向-强度”协同设计的必要性。

此外，CAST具备**即插即用**的特性——它可以无缝集成到现有的交互式检索框架中，仅需对文本和图像编码器的输出特征施加CASR变换，计算开销极低（在秩$r=8$时，约0.002秒即可完成50,000张图像的特征变换）。

CAST 的整体流水线围绕一个核心观察展开：传统交互式文本到图像检索（I-TIR）在整个多轮对话过程中使用固定的多模态嵌入空间进行跨模态匹配，导致用户意图随对话轮次演变时产生的细微语义变化无法被特征空间捕捉。CAST 通过一个轻量级的上下文感知空间调节器（Context-Aware Space Regulator, CASR），将静态的多模态特征空间动态变换为与当前对话上下文对齐的新空间，从而实现自适应语义对齐。

### 流水线总览

CAST 的完整检索流水线包含四个主要阶段，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2297_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_CAST_Context_Aware/figures/002_Figure_2.jpg]]
*Figure 2: (a) A traditional interactive text-to-image retrieval framework using a static multimodal latent space for cross-modal alignment. (b) Illustration of our proposed context-aware dynamic latent space transformation, which aims to dynamically transform the static multimodal latent space into a new space according to the user’s search intention. (c) The CASR consists of two key modules: The CLP module provides the direction for the feature space transformation, while the CGM module controls the strength of the transformation*

1. **对话上下文生成**：给定第 $t$ 轮的对话历史 $\mathcal{H}_t = C_0, (Q_1, A_1), (Q_2, A_2), \ldots, (Q_t, A_t)$，利用大语言模型（LLM）整合对话历史，生成上下文摘要 $C_t = \mathrm{LLM}(\mathcal{H}_t)$，再通过文本编码器 $f_T$ 将其编码为语义条件向量 $u_t = f_T(C_t)$，作为后续空间变换的引导信号。

2. **上下文感知低秩投影（Context-Aware Low-Rank Projector, CLP）**：CLP 以语义条件 $u_t$ 为输入，通过两个独立的 MLP 分别预测低秩投影矩阵 $A_t, B_t \in \mathbb{R}^{d \times r}$（其中秩 $r \ll d$）。经过列式 L2 归一化后，特征 $x_t$ 首先被投影到低秩子空间 $x_t \hat{B}_t$，再通过 $\hat{A}_t^\top$ 回升到原始维度，形成上下文条件的方向性变换 $\mathcal{P}(x_t \mid u_t) = (x_t \hat{B}_t) \hat{A}_t^\top$。CLP 决定了特征空间沿何种语义方向变形。

3. **上下文引导调制（Context-Guided Modulator, CGM）**：CGM 通过拼接初始上下文 $u_0$ 与当前上下文 $u_t$，经 MLP 和 sigmoid 函数预测自适应调制系数 $\alpha_t = \sigma(\mathrm{MLP}([u_0; u_t]))$。该系数根据对话过程中语义偏离初始意图的程度，动态控制空间变换的幅度：$\mathcal{F}(x_t \mid u_t) = \alpha_t \cdot \mathcal{P}(x_t \mid u_t)$。

4. **空间变换与检索**：将调制后的特征通过残差连接和层归一化得到最终变换特征 $\mathcal{G}(x_t \mid u_t) = \mathrm{LN}(x_t + \mathcal{F}(x_t \mid u_t))$。文本特征 $x_t^T$ 和所有候选图像特征 $x_t^I$ 均经过同一 CASR 变换，得到 $z_t^T$ 和 $z_t^I$，随后在变换后的动态空间中计算余弦相似度 $s_t^{(k)} = \text{sim}(z_t^T, z_t^{I_k})$ 完成检索排序。

### 模块关系与设计逻辑

CLP 和 CGM 构成 CASR 的两个协同子模块，分别解决“往哪个方向变”和“变多少”的问题。CLP 通过低秩分解学习紧凑的投影方向，避免了直接学习全秩变换矩阵 $W \in \mathbb{R}^{d \times d}$ 带来的参数量爆炸和过拟合风险；消融实验（Table 3）证实，低秩分解结构（Avg. R@10: 82.05）优于非分解的上下文感知矩阵（Avg. R@10: 80.57）。CGM 则通过对比初始与当前上下文的语义差异来调节变换强度，相比使用上下文无关的可学习标量（Avg. R@10: 81.51），上下文引导调制显著提升了检索精度。

### 输入输出流

- **输入**：第 $t$ 轮的对话历史 $\mathcal{H}_t$，以及预提取的图像特征集合 $\{f_I(I_k)\}$。
- **中间表示**：LLM 生成的上下文摘要 $C_t$ → 语义条件 $u_t$ → 低秩投影矩阵 $\hat{A}_t, \hat{B}_t$ → 调制系数 $\alpha_t$。
- **输出**：经过 CASR 变换的文本特征 $z_t^T$ 和图像特征 $\{z_t^{I_k}\}$，以及基于动态空间余弦相似度的排序结果。

CAST 的设计使其可作为即插即用模块集成到现有 I-TIR 架构中。Figure 4 的实验表明，将 CASR 添加到 ChatIR、PlugIR 等基线方法后，各方法在 VisDial 上的性能均获得一致提升，验证了该模块的通用性。在效率方面，当低秩维度 $r=8$ 时，CAST 可在约 0.002 秒内完成对 50,000 张图像特征的变换，额外计算开销极小。

### 问题形式化

交互式文本到图像检索的核心任务可形式化如下：给定第 $t$ 轮对话历史 $\mathcal{H}_t = C_0, (Q_1, A_1), (Q_2, A_2), \ldots, (Q_t, A_t)$，其中 $C_0$ 为初始上下文，$(Q_i, A_i)$ 为问答对，系统需从图像库中检索与用户意图最匹配的图像。传统方法在静态特征空间中计算文本嵌入 $f_T(\mathcal{H}_t)$ 与图像嵌入 $f_I(I)$ 的相似度得分 $s_t = \text{sim}(f_T(\mathcal{H}_t), f_I(I))$，这一固定流形无法捕捉用户意图随对话轮次的语义演变。

### 上下文感知空间调节器（CASR）

CAST 的核心是上下文感知空间调节器 CASR，其整体变换框架为：

$$\mathcal{G}(x_t \mid u_t) = \mathrm{LN}\big(x_t + \mathcal{F}(x_t \mid u_t)\big)$$

该模块通过残差连接和层归一化实现上下文条件的特征空间动态变换，分为三个阶段。

#### 阶段一：对话上下文生成

首先利用大语言模型整合对话历史，生成上下文摘要 $C_t$，再通过文本编码器 $f_T$ 编码为语义条件向量 $u_t$：

$$C_t = \mathrm{LLM}(\mathcal{H}_t), \quad u_t = f_T(C_t)$$

$u_t$ 作为后续所有模块的条件信号，承载当前轮次用户意图的语义信息。

#### 阶段二：上下文感知低秩投影器（CLP）

CLP 负责学习特征空间变换的**方向**。它通过两个 MLP 从语义条件 $u_t$ 预测低秩投影矩阵 $A_t, B_t \in \mathbb{R}^{d \times r}$（秩 $r \ll d$）：

$$A_t = \mathrm{MLP}_A(u_t), \quad B_t = \mathrm{MLP}_B(u_t)$$

对矩阵进行列式 L2 归一化以保证数值稳定性：

$$\hat{A}_t = \frac{A_t}{\lVert A_t \rVert_2}, \quad \hat{B}_t = \frac{B_t}{\lVert B_t \rVert_2}$$

条件低秩投影操作定义为：先将特征 $x_t$ 经 $\hat{B}_t$ 压缩到低秩子空间，再经 $\hat{A}_t^{\top}$ 回升到原始维度：

$$\mathcal{P}(x_t \mid u_t) = (x_t \hat{B}_t) \hat{A}_t^{\top}$$

这一“压缩-回升”过程在低秩子空间中学习上下文条件的方向变换，沿用户意图相关的语义方向变形特征流形。

#### 阶段三：上下文引导调制器（CGM）

CGM 负责控制特征空间变换的**强度**。它根据初始上下文 $u_0$ 与当前上下文 $u_t$ 的语义差异，自适应预测调制系数 $\alpha_t$：

$$\alpha_t = \sigma(\mathrm{MLP}([u_0; u_t]))$$

其中 $[\cdot;\cdot]$ 表示向量拼接，$\sigma$ 为 sigmoid 函数。最终的调制函数将 CLP 的投影输出与 CGM 的强度系数相乘：

$$\mathcal{F}(x_t \mid u_t) = \alpha_t \cdot \mathcal{P}(x_t \mid u_t)$$

### 动态空间中的检索

文本特征 $x_t^T$ 和图像特征 $x_t^I$ 经 CASR 变换后得到上下文自适应的表示：

$$z_t^T = \mathcal{G}(x_t^T \mid u_t), \quad z_t^I = \mathcal{G}(x_t^I \mid u_t)$$

在动态特征空间中通过余弦相似度进行检索排序：

$$s_t^{(k)} = \text{sim}(z_t^T, z_t^{I_k}) = \frac{z_t^T \cdot z_t^{I_k}}{\lVert z_t^T \rVert \lVert z_t^{I_k} \rVert}$$

### 训练目标

CAST 采用上下文引导的对比损失（Context-guided Contrastive Loss）进行端到端训练，在上下文自适应子空间中对齐文本和图像嵌入：

$$\mathcal{L}_{\mathrm{cgc}} = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(\text{sim}(z_{t_i}^{T_i}, z_{t_i}^{I_i}) / \tau)}{\sum_{j=1}^{B} \exp(\text{sim}(z_{t_i}^{T_i}, z_{t_i}^{I_j}) / \tau)}$$

其中 $B$ 为批次大小，$\tau$ 为温度系数。该损失函数使正样本对（匹配的文本-图像）在动态变换后的空间中距离更近，负样本对距离更远。

### 关键设计动机

CLP 与 CGM 的协同设计解决了两个核心问题：**方向**与**幅度**。仅使用 CLP 会导致变换方向有语义意义但幅度不可控；仅使用 CGM 则缺乏方向引导。两者结合使特征空间能够沿用户意图相关的语义方向（CLP），以对话轮次间语义差异决定的幅度（CGM）进行稳定且表达力强的动态演化。消融实验证实了这一协同效应：引入 CLP 使平均 R@10 从 79.89 提升至 80.90，进一步增加 CGM 后提升至 82.05。

## 实验与关键发现

### 主实验结果

CAST 在 VisDial 基准上与现有最先进方法进行了对比，所有对比方法均采用静态多模态潜在空间进行检索，而 CAST 使用动态潜在空间。**Table 1** 展示了详细的性能对比结果。

![[assets/figures/papers/paper_list_l2297_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_CAST_Context_Aware/figures/003_Table_1.jpg]]
*Table 1: Performance comparison with the state-of-the-art methods on VisDial. Note that the compared methods all utilize a static multimodal latent space for retrieval, while our proposed method uses dynamic latent spaces according to the dialogue context. The results demonstrate the effectiveness of our proposed context-aware dynamic latent space for interactive text-to-image retrieval*

关键发现如下：

- **早期对话轮次**：在第 1 轮，CAST 的 R@1 达到 43.60%，相比 **ChatIR**（Levy et al., NeurIPS 2023）的 42.78% 提升 0.82 个百分点，相比零样本 **BLIP**（Li et al., ICML 2022）的 40.31% 提升 3.29 个百分点。这表明即使对话上下文尚不丰富，动态空间变换也能提供更好的初始检索对齐。

- **后期对话轮次优势显著**：CAST 的核心优势在对话深入后更加突出。第 10 轮时，CAST 的 R@1 达到 57.56%，相比 ChatIR 的 53.15% 提升 4.41 个百分点。这一趋势验证了核心假设：静态特征空间无法有效捕捉随对话轮次演变的用户意图语义变化，而 CAST 通过 CASR 持续重塑文本和视觉嵌入，实现了逐步细化的文本意图与视觉内容对齐。

- **跨对话风格鲁棒性**：**Figure 3** 展示了使用不同对话源时的性能对比。CAST 在三种不同对话风格来源上均持续取得最佳平均召回率，证明了其对不同对话风格的强适应性。这一结果说明 CASR 的上下文感知变换机制不依赖于特定的对话生成范式。

![[assets/figures/papers/paper_list_l2297_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_CAST_Context_Aware/figures/004_Figure_3.jpg]]
*Figure 3: Performance comparison using different dialogue sources. Our proposed method consistently outperforms previous works, demonstrating its strong adaptability to various dialogue styles*

### 消融实验

消融实验系统性地验证了 CASR 各组件的贡献，所有结果均报告 10 轮平均召回性能。

**Table 2** 展示了核心组件的消融结果：

- **CLP 的贡献**：引入上下文感知低秩投影器（CLP）后，Avg. R@10 从基线的 79.89 提升至 80.90。CLP 通过上下文条件空间变换，将嵌入流形沿有意义的语义方向变形，使特征空间能更好地捕捉用户意图的细微变化。

- **CGM 的增量收益**：在 CLP 基础上增加上下文引导调制器（CGM），Avg. R@10 进一步提升至 82.05。CGM 根据对话轮次间的上下文语义差异自适应控制变换强度，防止了过度变换或变换不足的问题。

**Table 3** 对比了不同投影结构的性能：

- 低秩矩阵分解方案（CLP，r 远小于 d）的 Avg. R@10 为 82.05，优于非分解的上下文感知矩阵 W（80.57）。低秩分解通过将特征投影到紧凑子空间再回升，实现了参数高效且有正则化效果的方向变换，避免了全秩矩阵可能引入的过拟合和计算开销。

**Table 4** 对比了不同调制策略：

- 上下文引导调制器（CGM，基于 u₀ 和 u_t 的语义差异预测 α_t）的 Avg. R@10 为 82.05，优于上下文无关的可学习标量（81.51）。这验证了根据初始与当前上下文语义差异自适应调节变换强度的必要性——固定的变换幅度无法适应不同对话轮次中意图变化的程度差异。

### 即插即用特性

**Figure 4** 展示了将 CASR 作为即插即用模块集成到现有 I-TIR 框架的效果。在 VisDial 数据集上，无论基础方法是什么，加入 CASR 后性能均获得一致提升。这表明 CAST 不依赖特定架构，可作为通用增强模块应用于各类交互式文本到图像检索系统。

### 效率分析

CAST 的设计充分考虑了实际部署效率。低秩投影的秩 r 设为 8 时，CASR 可在约 0.002 秒内完成 50,000 张图像的特征变换。这一极低的计算开销源于低秩分解大幅减少了投影矩阵的参数量（从 d×d 降至 2×d×r），使得动态空间变换在实际检索场景中几乎不引入额外延迟。

### 失败模式与局限性

论文未明确报告失败案例分析。从实验设计推断，潜在局限包括：

- 对 LLM 上下文总结质量的依赖性：CASR 的语义条件 u_t 依赖于 LLM 生成的对话摘要 C_t，若 LLM 对长对话或歧义查询的总结质量下降，可能影响空间变换的准确性。该点需在后续工作中进一步验证。

- 极长对话场景下的调制饱和：论文未讨论超过 10 轮的对话场景中 CGM 的调制行为是否会趋于饱和，需要手动验证。

- 跨模型泛化性：当前实验基于 BLIP 特征空间，CAST 能否直接适配 CLIP 等其他预训练视觉语言模型的特征空间，论文未提供证据。

![[assets/figures/papers/paper_list_l2297_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_CAST_Context_Aware/figures/006_Table_2.jpg]]
*Table 2: Ablation study on the VisDial dataset. All results report the 10-round averaged Recall performance*

![[assets/figures/papers/paper_list_l2297_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_CAST_Context_Aware/figures/008_Table_3.jpg]]
*Table 3: Performance comparison between our proposed contextaware space regulator and the alternative projection structures*

![[assets/figures/papers/paper_list_l2297_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_CAST_Context_Aware/figures/009_Figure_5.jpg]]
*Figure 5: T-SNE visualization shows the 100 images about the topic of dog. The red bounding box marks a sample image, with its local region zoomed-in to illustrate space transformation. When the input dialogue context is “a black dog”, the feature space seems to be transformed into a new space of emphasizing color distinctions. As a result, images with the “black” attribute are brought closer together in the transformed space. Similarly, when the dialogue context is “a dog on the grass”, the space adjusts to prioritize scene, bringing images in grassy environments closer together. This demonstrates how the input context dynamically transforms the representation of the images, highlighting the model’s...*

## 定位与知识库关联

### 1. 问题定位：从静态空间到动态流形

现有交互式文本到图像检索（I-TIR）方法，包括基于大语言模型进行对话生成与查询重写的 **ChatIR** (Levy et al., NeurIPS 2023)、即插即用式对话上下文生成的 **PlugIR** (Lee et al., ACL 2024) 以及利用多模态大模型统一推理的 **ImageScope** (Luo et al., WWW 2025)，其共同技术前提是将对话文本和候选图像映射到一个**固定的多模态嵌入空间**中，并在此静态流形上计算余弦相似度进行检索。这一静态范式构成了性能瓶颈的根源：用户意图随对话轮次演变所产生的细微语义变化（如新增颜色属性、细化空间关系）无法被特征空间捕捉，导致后续轮次的检索精度受限。

CAST 的核心突破在于首次将多模态特征空间从“静态背景”提升为“可优化的动态变量”。其核心模块 CASR（Context-Aware Space Regulator）通过两个协同子模块——上下文感知低秩投影器（CLP）和上下文引导调制器（CGM）——实现了特征空间随对话语义的动态演变。这一设计将检索问题从“在固定空间中寻找最近邻”转化为“先根据意图变换空间，再寻找最近邻”，本质上是对特征流形的几何结构进行上下文条件化的变形。

### 2. 技术谱系与差异化贡献

从技术路径来看，CAST 与现有工作的关系可归纳为以下谱系分支：

| 方法类别 | 代表工作 | 核心机制 | CAST 的差异化 |
|---------|---------|---------|-------------|
| 零样本基线 | **BLIP** (Li et al., ICML 2022) | 预训练视觉-语言模型的固定特征空间 | 在 BLIP 编码器之上叠加动态空间变换，无需重新训练编码器 |
| LLM 对话重写 | **ChatIR** (Levy et al., NeurIPS 2023) | 利用 LLM 重写查询文本以适应对话上下文 | 不修改查询文本，而是直接变换特征空间的几何结构 |
| 即插即用 LLM 增强 | **PlugIR** (Lee et al., ACL 2024) | LLM 生成对话上下文后输入固定检索器 | 将上下文信息注入特征空间本身，而非仅注入文本端 |
| 多模态大模型推理 | **ImageScope** (Luo et al., WWW 2025) | 利用 MLLM 进行统一推理和检索 | 轻量级模块化设计，可无缝集成到现有框架（Figure 4 验证） |

CAST 的方法学贡献不在于替换现有检索框架，而在于提出了一种**特征空间级别的动态调节机制**。CLP 在低秩子空间中学习投影方向，决定了“向哪个方向变换语义流形”；CGM 根据初始上下文 $u_0$ 与当前上下文 $u_t$ 的语义差异自适应预测调制强度 $\alpha_t = \sigma(\mathrm{MLP}([u_0; u_t]))$，决定了“变换多少”。这种“方向-强度”解耦设计使得空间变换既具有语义可解释性，又保持了数值稳定性。

### 3. 适用边界与关键约束

基于论文提供的实验证据和分析，CAST 的适用边界可归纳如下：

**已验证的有效范围：**
- **数据集**：VisDial 基准（Table 1），以及三种不同对话风格来源的数据（Figure 3），展示了跨对话风格的鲁棒性。
- **对话轮次**：1-10 轮，尤其在后期轮次（Round 10）优势显著（R@1: 57.56% vs. ChatIR 53.15%，提升 +4.41%）。
- **集成能力**：可作为即插即用模块增强现有 I-TIR 框架，包括 ChatIR、PlugIR 和 ImageScope（Figure 4 验证了一致性提升）。
- **计算效率**：在秩 $r=8$ 时，约 0.002 秒内完成 50,000 张图像的特征变换（Section 6），表明低秩设计有效控制了计算开销。

**需要手动验证的边界与约束：**
- **极长对话场景**（>10 轮）：论文未提供 10 轮以上的实验证据。CGM 的调制系数 $\alpha_t$ 是否会随对话延长趋于饱和，导致空间变换失效，需要进一步验证。
- **LLM 上下文总结质量的依赖性**：CASR 的第一阶段依赖 LLM 生成对话上下文摘要 $C_t = \mathrm{LLM}(\mathcal{H}_t)$。若替换为更轻量级的编码器（如直接使用对话历史的平均嵌入），性能是否会显著下降，论文未提供消融实验。
- **预训练编码器的迁移性**：论文实验基于 BLIP 编码器。CAST 能否直接迁移到其他视觉-语言模型（如 CLIP、SigLIP）而不损失有效性，尚未验证。
- **低秩投影秩 $r$ 的敏感性**：论文未系统报告不同 $r$ 值对性能和效率的影响。最优秩可能随数据集规模和特征维度变化。

### 4. 开放问题与未来方向

1. **动态空间变换的理论解释**：CLP 学习到的低秩投影方向是否对应可解释的语义维度（如颜色、纹理、空间关系）？Figure 5 的 t-SNE 可视化提供了初步的定性证据，但缺乏系统性的语义解耦分析。

2. **跨任务泛化性**：动态空间变换机制是否适用于其他交互式多模态任务（如对话式视觉问答、具身导航中的指令理解）？核心思想——根据任务上下文动态调整特征空间——具有通用性，但需要任务特定的验证。

3. **多模态大模型时代的定位**：随着 GPT-4V、Gemini 等端到端多模态大模型的发展，特征空间级别的显式变换是否会被隐式上下文理解所取代？CAST 的轻量级、模块化设计在计算效率和可解释性方面仍具优势，但需要在更强基线（如端到端 MLLM 检索）下进行评估。

4. **多轮对话中的累积误差**：CASR 在每一轮独立计算空间变换，未显式建模轮次间的变换连续性。引入递归或动量机制以平滑空间演化，可能进一步提升长对话场景下的稳定性。

## 原文 PDF

![[paperPDFs/CVPR_2026/CAST_Context_Aware_Dynamic_Latent_Space_Transformation_for_Interactive_Text_to_Image_Retrieval.pdf]]

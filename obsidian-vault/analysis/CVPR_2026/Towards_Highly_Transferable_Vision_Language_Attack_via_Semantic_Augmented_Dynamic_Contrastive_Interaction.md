---
title: Towards Highly Transferable Vision-Language Attack via Semantic-Augmented Dynamic Contrastive Interaction
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Highly_Transferable_Vision_Language_Attack_via_Semantic_Augmented_Dynamic_Contrastive_Interaction.pdf
project_link: null
code_link: "https://github.com/LiYuanBoJNU/SADCA"
aliases:
- SSADCA
- THTVLASADCI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 动态对比交互机制（迭代式交替更新对抗图像与文本，并利用正负样本对比学习）和语义增强模块（局部图像增强与混合文本增强）是提升迁移性的关键因素。
primary_logic: 通过动态对比学习框架引入正负样本的排斥与吸引力，引导对抗样本持续偏离语义中心，同时增强输入语义多样性以丰富梯度方向，实现跨模型与跨任务的高迁移性对抗攻击。
claims:
- SADCA 通过动态交互逐步破坏跨模态对齐，并利用对比学习最大化与负样本的相似性而最小化与正样本的相似性。
- 语义增强模块增加对抗样本的多样性和泛化性。
- SADCA 在多个数据集和模型上显著超越现有方法，取得最高的平均攻击成功率。
- 动态对比交互和语义增强机制有效促进语义发散，使对抗样本探索更广泛的攻击方向。
---

# Towards Highly Transferable Vision-Language Attack via Semantic-Augmented Dynamic Contrastive Interaction

> [!tip] 核心洞察
> 通过动态对比学习框架引入正负样本的排斥与吸引力，引导对抗样本持续偏离语义中心，同时增强输入语义多样性以丰富梯度方向，实现跨模型与跨任务的高迁移性对抗攻击。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于语义增强动态对比交互的高迁移性视觉语言攻击 |
| 英文题名 | Towards Highly Transferable Vision-Language Attack via Semantic-Augmented Dynamic Contrastive Interaction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.04839) · [Code](https://github.com/LiYuanBoJNU/SADCA) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SADCA (Semantic-Augmented Dynamic Contrastive Attack) |
| Dataset | Flickr30K, RefCOCO+, MSCOCO |

> [!tip] 效果简介
> - Flickr30K 上，Average TR R@1 across black-box models (ALBEF as source) 88.35 vs 83.85 (SA-AET(LI)+SIA) (+4.50)；Average IR R@1 across black-box models (ALBEF as source) 88.92 vs 86.12 (SA-AET(LI)+SIA) (+2.80)。
> - RefCOCO+ (Visual Grounding) 上，Val accuracy (lower is better) 46.78 vs 49.37 (SA-AET) (-2.59)。
> - MSCOCO (Image Captioning) 上，CIDEr (lower is better) 50.3 vs 54.8 (SA-AET) (-4.5)。

## 概要

视觉语言预训练模型（VLP）在图文检索、视觉定位等任务中表现优异，但其对抗鲁棒性不足。现有对抗攻击方法（如 **SGA**、**SA-AET**）依赖静态跨模态交互，仅利用正样本对优化对抗样本，忽视了负样本对语义决策边界的影响，导致对抗样本在语义空间中分离不充分，跨模型迁移性受限。

针对上述瓶颈，本文提出 **SADCA**（Semantic-Augmented Dynamic Contrastive Attack），核心思路是通过**动态对比交互**与**语义增强**两大机制，持续破坏图文间的跨模态语义对齐，从而生成高迁移性的多模态对抗样本。具体而言，SADCA 引入正负样本对比学习框架：在迭代过程中交替更新对抗图像与文本，最大化对抗样本与负样本的相似度、同时最小化与正样本的相似度，引导对抗样本持续偏离语义中心。此外，语义增强模块对图像进行局部裁剪变换、对文本进行混合拼接，丰富了输入的语义多样性，使梯度方向更加泛化。

实验表明，SADCA 在图文检索（Flickr30K、MSCOCO）、视觉定位（RefCOCO+）和图像字幕（MSCOCO）等多个任务上，均显著超越现有最优方法。以 ALBEF 为源模型时，SADCA 在 Flickr30K 黑盒迁移攻击中的平均 TR R@1 达到 88.35%，IR R@1 达到 88.92%，分别比最强基线 SA-AET(LI)+SIA 提升 4.50 和 2.80 个百分点。在跨任务迁移方面，SADCA 同样表现最佳，验证了其攻击的广泛适用性。消融实验进一步证实，动态对比交互与语义增强模块的协同作用是性能提升的关键来源。

**方法定位**：SADCA 属于多模态对抗攻击方法，与 SGA、SA-AET 等基于跨模态交互的攻击同源，但在交互范式（动态迭代 vs. 静态一次/两次）、样本利用（正负样本对比 vs. 仅正样本）和输入增强策略（语义增强 vs. 有限输入变换）三个维度上实现了根本性改进。

视觉语言预训练模型（VLP）在图像文本检索、视觉问答等跨模态任务中取得了显著进展，但其对抗鲁棒性问题日益受到关注。对抗攻击旨在生成人眼难以察觉的扰动样本，诱使模型产生错误输出。在视觉语言领域，对抗攻击的关键在于破坏图像与文本模态之间的跨模态语义对齐。

现有视觉语言对抗攻击方法主要依赖**静态跨模态交互**。以 SGA 和 SA-AET 为代表的方法仅在攻击过程中进行一次或两次模态间交互，且交互范围局限于正样本对（即原始匹配的图文对）。这种静态交互策略存在根本性局限：**仅关注正样本对而忽视负样本对在语义决策边界中的排斥作用**，导致生成的对抗样本在语义空间中与原始样本分离不足，难以跨越不同模型架构的决策边界，迁移性受到严重制约。

具体而言，现有方法的瓶颈体现在三个层面：
1. **交互深度不足**：单次或两次的静态交互无法充分探索跨模态语义空间中的对抗方向，对抗扰动容易陷入局部最优。
2. **样本利用单一**：仅利用正样本对引导语义偏移，缺少负样本提供的排斥力，使得对抗样本无法持续远离原始语义中心。
3. **输入多样性有限**：现有输入变换策略（如尺度不变性变换）对语义信息的丰富程度不足，限制了梯度方向的多样性，进而影响对抗样本的泛化能力。

针对上述缺口，本文提出 **SADCA（Semantic-Augmented Dynamic Contrastive Attack）**，核心动机在于：通过引入**动态对比交互机制**和**语义增强模块**，使对抗样本在语义空间中持续偏离正样本对齐中心、同时向负样本方向靠拢，从而获得更强的跨模型和跨任务迁移能力。

## 核心方法与创新机理

现有视觉语言（VL）攻击方法的一个根本瓶颈在于，它们依赖**静态跨模态交互**，且仅使用**正样本对**来生成对抗扰动。例如，SGA 与 SA-AET 仅在图像与文本模态之间进行一至两次静态交互，完全忽视了负样本对语义决策边界的约束作用，导致对抗样本在语义空间中分离不足，迁移性受限。

SADCA 通过三个关键创新打破上述瓶颈，实现了高迁移性的视觉语言对抗攻击。

### 1. 动态对比交互机制

SADCA 的核心创新在于引入了**动态对比交互**（Dynamic Contrastive Interaction）机制，将传统的静态跨模态交互转变为迭代式交替更新过程。具体而言：

- **迭代交互**：对抗图像与对抗文本在 I 次迭代中交替更新，逐步破坏跨模态语义对齐，而非一次性生成对抗样本。
- **正负样本对比学习**：在每一次迭代中，SADCA 同时利用正样本对和负样本对，通过对比损失引导语义偏移——最小化对抗样本与正样本的相似度，同时最大化与负样本的相似度。这一策略使对抗样本在语义空间中持续偏离语义中心，探索更广泛的攻击方向。

如 **Figure 1(c)** 所示，与 SGA 和 SA-AET 的静态交互形成鲜明对比，SADCA 通过动态对比交互实现了持续的跨模态语义破坏。

### 2. 语义增强模块

SADCA 提出了**语义增强模块**（Semantic Augmentation Module），通过增加输入样本的语义多样性来丰富梯度方向，进一步提升对抗样本的泛化能力。该模块包含两个子组件：

- **局部语义图像增强**：对对抗图像进行随机裁剪、缩放与变换，生成 S 个增强图像副本，如 **Equation (7)** 所示：
  $$V_{sa}' = \{ A_s( Resize( Crop( v'; r_s ) ) ) \}_{s=1}^{S}$$
- **混合语义文本增强**：随机拼接两个不同的对抗文本，生成 S 个增强文本，如 **Equation (8)** 所示：
  $$T_{sa}' = \{ t_s = Concat( t_i', t_j' ) \mid t_i', t_j' \in T', i \neq j \}_{s=1}^{S}$$

消融实验（**Table 6**）表明，语义增强模块相比传统的 DIM、SIA、BSR 等输入变换方法，能更有效地提升攻击迁移性。

### 3. 正样本对齐策略

不同于现有方法直接将原始图文对作为正样本，SADCA 首先通过**正样本对齐模块**获得语义中心对齐的正图像表示。如 **Equation (2)** 所示，SADCA 最大化良性图像与多个文本描述的余弦相似度：
$$v_p = \underset{v_p \in B[v, \epsilon_v]}{\arg\max} \sum_{m=1}^{M} Cos(v, t_m)$$
这一策略确保了正样本在语义空间中的中心性，为后续的对比学习提供了更稳定的参考基准。

### 创新点总结

| 创新维度 | 现有方法 | SADCA |
|---------|---------|-------|
| 跨模态交互方式 | 静态交互（1-2次），仅正样本 | 动态迭代交互（I次），正负样本对比学习 |
| 样本对利用 | 仅正样本对 | 正样本+负样本对，对比损失引导语义偏移 |
| 输入增强 | 有限变换（如尺度不变性） | 语义增强模块：局部图像增强+混合文本增强 |
| 正样本对齐 | 原始图文对直接作为正样本 | 语义中心对齐的正图像表示 |

这些创新机制协同作用，使 SADCA 能够有效促进语义发散，引导对抗样本在语义空间中探索更广泛的攻击方向，从而实现跨模型与跨任务的高迁移性对抗攻击。

SADCA 的整体流程围绕一个核心思想构建：**通过动态对比交互持续破坏图文语义对齐，并利用语义增强丰富对抗样本的多样性**。其 pipeline 由四个紧密协作的模块组成，形成一条从正样本对齐到最终对抗样本生成的完整链路。

### 1. 正样本对齐模块

传统攻击方法直接将原始图文对作为正样本，而 SADCA 首先在语义空间中**将良性图像与多个文本描述对齐**，获得一个语义中心化的正图像表示 $v_p$：

$$v _ { p } = \underset { v _ { p } \in B [ v , \epsilon _ { v } ] } { \arg \max } \sum _ { m = 1 } ^ { M } C o s ( v , t _ { m } )$$

该操作通过最大化图像与 $M$ 个文本描述的余弦相似度，使正图像在语义空间中处于更稳定的中心位置，为后续对比学习提供更可靠的“排斥参考点”。

### 2. 动态对比交互模块

这是 SADCA 的核心创新。与 SGA 和 SA-AET 仅进行一至两次静态交互且仅使用正样本对不同，SADCA 引入了**迭代式交替更新对抗图像与文本**的机制（共 $I$ 次交互），并在每次交互中同时利用正样本和负样本进行对比学习。

具体而言，在第 $i$ 次交互中：

- **更新对抗图像** $v_i'$：最小化其与对抗文本 $t_i'$ 的相似度，同时最大化其与 $K$ 个负文本 $t_{nk}$ 的相似度：

$$\min _ { v _ { i } ^ { \prime } } \mathcal { L } \left( v _ { i } ^ { \prime } , T _ { i } ^ { \prime } , T _ { n } \right) = \sum _ { m = 1 } ^ { M } C o s ( v _ { i } ^ { \prime } , t _ { i m } ^ { \prime } ) - \lambda \sum _ { k = 1 } ^ { K } C o s ( v _ { i } ^ { \prime } , t _ { n k } )$$

- **更新对抗文本** $t_i'$：最小化其与对抗图像 $v_i'$ 的相似度，同时最大化其与 $K$ 个负图像 $v_{nk}$ 的相似度：

$$\min _ { t _ { i } ^ { \prime } } \mathcal { L } \left( t _ { i } ^ { \prime } , v _ { i } ^ { \prime } , V _ { n } \right) = C o s ( v _ { i } ^ { \prime } , t _ { i } ^ { \prime } ) - \lambda \sum _ { k = 1 } ^ { K } C o s ( v _ { n k } , t _ { i } ^ { \prime } )$$

这种“推—拉”机制使对抗样本在语义空间中持续偏离正样本中心，同时被负样本吸引，从而探索更广泛的攻击方向。消融实验（Figure 4）证实，动态对比交互与语义增强模块联合使用带来了显著的性能提升。

### 3. 语义增强模块

在每次交互迭代中，SADCA 对对抗图像和文本分别施加语义增强，以增加输入多样性并丰富梯度方向：

- **局部语义图像增强**：随机裁剪图像局部区域并缩放，再应用随机增强操作，生成 $S$ 个增强图像：

$$V _ { s a } ^ { \prime } = \{ A _ { s } \left( R e s i z e \left( C r o p \left( v ^ { \prime } ; r _ { s } \right) \right) \right) \} _ { s = 1 } ^ { S }$$

- **混合语义文本增强**：随机拼接两个不同的对抗文本，生成 $S$ 个增强文本，丰富语义多样性：

$$T _ { s a } ^ { \prime } = \{ t _ { s } = C o n c a t ( t _ { i } ^ { \prime } , t _ { j } ^ { \prime } ) | t _ { i } ^ { \prime } , t _ { j } ^ { \prime } \in T ^ { \prime } , i \neq j \} _ { s = 1 } ^ { S }$$

消融实验（Table 6）表明，语义增强模块相比传统的 DIM、SIA、BSR 等输入变换方法，能更有效地提升攻击迁移性。

### 4. 对抗样本生成模块

该模块基于动量迭代方式整合上述三个模块的输出，最终生成高迁移性对抗样本。整体流程如 Algorithm 1 所述：在 $I$ 次迭代中，交替执行图像增强、文本增强、动态对比损失计算和动量更新，最终输出对抗图像 $v'$ 和对抗文本 $t'$。

### 输入输出流总结

- **输入**：良性图像 $v$、良性文本 $t$、负样本池（负图像 $V_n$ 和负文本 $T_n$）、扰动预算 $\epsilon_v$ 和 $\epsilon_t$。
- **输出**：满足扰动约束的对抗图像 $v'$ 和对抗文本 $t'$，其在语义空间中与正样本对齐被破坏，同时被推向负样本方向。
- **关键参数**：交互次数 $I$、增强数量 $S$、负样本数 $K$、对比权重 $\lambda$。参数敏感性分析（Figure 3）提供了这些超参数对攻击成功率的影响趋势，需根据具体场景手动调优。

### 与现有框架的核心差异

Figure 1 清晰地展示了 SADCA 与 SGA、SA-AET 的架构差异：SGA 和 SA-AET 仅进行有限的静态交互且仅使用正样本对，而 SADCA 通过**多轮动态对比交互**持续破坏跨模态对齐，并借助语义增强策略丰富数据样本，从而在语义空间中探索更广泛的攻击方向。

![[assets/figures/papers/paper_list_l789_https_arxiv_org_abs_2603_04839/figures/001_Figure_1.jpg]]
*Figure 1: A comparison of our SADCA and existing frameworks. (a) and (b) illustrate the core concepts of SGA [18] and SA-AET [7], respectively, where only one or two static interactions are performed between the visual and textual modalities, with the interactions being limited solely to positive pairs. (c) illustrates the core idea of the proposed SADCA, which continuously disrupts cross-modal interactions through dynamic contrastive interactions with both positive and negative pairs. Additionally, it leverages a semantic augmentation strategy to enrich the data samples, thereby diversifying the semantic information. The arrow represents the interaction between the visual and textual modalities. The...*

SADCA 的核心由三个模块构成：**正样本对齐模块**、**动态对比交互模块**和**语义增强模块**。三个模块协同工作，通过正负样本对比学习持续破坏跨模态语义一致性，同时增强输入多样性以丰富梯度方向。

### 正样本对齐模块

现有方法直接使用原始图文对作为正样本，但单一文本描述可能无法充分覆盖图像的语义中心。SADCA 首先将良性图像与多个文本描述在语义空间中对齐，获得一个语义中心化的正图像表示：

$$v _ { p } = \underset { v _ { p } \in B [ v , \epsilon _ { v } ] } { \arg \max } \sum _ { m = 1 } ^ { M } C o s ( v , t _ { m } )$$

其中 $v$ 为良性图像，$\{t_m\}_{m=1}^M$ 为对应的 $M$ 个文本描述，$Cos(\cdot)$ 为余弦相似度，$B[v, \epsilon_v]$ 表示扰动量约束。该公式通过最大化图像与多个文本的相似度之和，获得一个语义中心对齐的正图像 $v_p$，作为后续动态交互中的正样本锚点。

### 动态对比交互模块

这是 SADCA 的核心创新。与 SGA、SA-AET 等仅进行一至两次静态交互且仅使用正样本对的方法不同，SADCA 引入迭代式动态交互机制，交替更新对抗图像与对抗文本，并在每次更新中同时利用正样本和负样本进行对比学习。

**对抗图像更新**：在第 $i$ 次交互中，对抗图像 $v_i'$ 的优化目标为最小化与正文本的相似度，同时最大化与负文本的相似度：

$$\min _ { v _ { i } ^ { \prime } } \mathcal { L } \left( v _ { i } ^ { \prime } , T _ { p } , T _ { n } \right) = \sum _ { m = 1 } ^ { M } C o s ( v _ { i } ^ { \prime } , t _ { p m } ) - \lambda \sum _ { k = 1 } ^ { K } C o s ( v _ { i } ^ { \prime } , t _ { n k } )$$

其中 $T_p = \{t_{pm}\}_{m=1}^M$ 为正文本集合，$T_n = \{t_{nk}\}_{k=1}^K$ 为从批次中随机选取的负文本集合，$\lambda$ 为平衡正负样本贡献的权重因子。

**对抗文本更新**：对称地，对抗文本 $t_i'$ 的优化目标为：

$$\min _ { t _ { i } ^ { \prime } } \mathcal { L } \left( t _ { i } ^ { \prime } , v _ { p } , V _ { n } \right) = C o s ( v _ { p } , t _ { i } ^ { \prime } ) - \lambda \sum _ { k = 1 } ^ { K } C o s ( v _ { n k } , t _ { i } ^ { \prime } )$$

其中 $v_p$ 为正样本对齐模块获得的正图像，$V_n = \{v_{nk}\}_{k=1}^K$ 为负图像集合。

**动态交互损失**：在后续迭代中，对抗图像和对抗文本不再与原始正样本对齐，而是彼此之间进行对抗性交互，持续破坏跨模态对齐：

$$\min _ { v _ { i } ^ { \prime } } \mathcal { L } \left( v _ { i } ^ { \prime } , T _ { i } ^ { \prime } , T _ { n } \right) = \sum _ { m = 1 } ^ { M } C o s ( v _ { i } ^ { \prime } , t _ { i m } ^ { \prime } ) - \lambda \sum _ { k = 1 } ^ { K } C o s ( v _ { i } ^ { \prime } , t _ { n k } )$$

$$\min _ { t _ { i } ^ { \prime } } \mathcal { L } \left( t _ { i } ^ { \prime } , v _ { i } ^ { \prime } , V _ { n } \right) = C o s ( v _ { i } ^ { \prime } , t _ { i } ^ { \prime } ) - \lambda \sum _ { k = 1 } ^ { K } C o s ( v _ { n k } , t _ { i } ^ { \prime } )$$

其中 $T_i' = \{t_{im}'\}_{m=1}^M$ 为当前迭代步的对抗文本集合。公式 (5) 和 (6) 分别最小化对抗图像与对抗文本之间的相似度，同时最大化它们与负样本的相似度，形成“排斥正样本、吸引负样本”的对比效应，引导对抗样本在语义空间中持续偏离原始语义中心。

### 语义增强模块

为增加对抗样本的语义多样性，SADCA 设计了局部语义图像增强和混合语义文本增强两种策略。

**局部语义图像增强**：对对抗图像 $v'$ 随机裁剪局部区域并缩放，然后应用随机增强操作，生成 $S$ 个增强图像：

$$V _ { s a } ^ { \prime } = \{ A _ { s } \left( R e s i z e \left( C r o p \left( v ^ { \prime } ; r _ { s } \right) \right) \right) \} _ { s = 1 } ^ { S }$$

其中 $Crop(v'; r_s)$ 表示以随机比例 $r_s$ 裁剪局部区域，$Resize(\cdot)$ 将裁剪区域缩放至原始尺寸，$A_s(\cdot)$ 为随机数据增强操作。

**混合语义文本增强**：从对抗文本集合 $T'$ 中随机选取两个不同的对抗文本进行拼接，生成 $S$ 个增强文本：

$$T _ { s a } ^ { \prime } = \{ t _ { s } = C o n c a t ( t _ { i } ^ { \prime } , t _ { j } ^ { \prime } ) | t _ { i } ^ { \prime } , t _ { j } ^ { \prime } \in T ^ { \prime } , i \neq j \} _ { s = 1 } ^ { S }$$

该模块通过增加输入的语义多样性，使对抗样本能够探索更广泛的攻击方向。消融实验（Table 6）表明，语义增强模块相比传统的 DIM、SIA、BSR 等输入变换方法，能更有效地提升攻击迁移性。

### 整体优化目标

SADCA 的最终优化目标可统一表述为在扰动量约束下最小化对抗图像与对抗文本的特征相似度：

$$\left\{ \begin{array} { l l } { \operatorname* { m i n } J \left( F _ { I } \left( v ^ { \prime } \right) , F _ { T } \left( t ^ { \prime } \right) \right) } \\ { \mathrm { s . t . } v ^ { \prime } \in B \left[ v , \epsilon _ { v } \right] , t ^ { \prime } \in B \left[ t , \epsilon _ { t } \right] } \end{array} \right.$$

其中 $F_I$ 和 $F_T$ 分别为图像和文本编码器，$J(\cdot)$ 为相似度损失函数，$\epsilon_v$ 和 $\epsilon_t$ 分别为图像和文本的扰动预算。通过动量迭代方式更新对抗样本，结合上述三个模块，SADCA 生成具有高跨模型和跨任务迁移性的多模态对抗样本。

## 实验与关键发现

### 核心实验设置

实验主要在 **Flickr30K** 和 **MSCOCO** 两个图文检索基准上评估跨模型与跨任务的对抗迁移性，同时考察对视觉接地（RefCOCO+）和图像字幕（MSCOCO）的下游攻击效果。攻击生成以 ALBEF 或 CLIP 架构作为替代模型，在多个黑盒 VLP 模型上测量 Rank-1 攻击成功率（ASR），并以 **TR R@1** 和 **IR R@1** 分别表示文本检索和图像检索的攻击成功率。对抗图像扰动预算固定为 $\epsilon_v = 8/255$，文本扰动预算 $\epsilon_t$ 依任务设定。

### 图文检索主结果

**Table 1** 报告了以 ALBEF 为源模型、Flickr30K 为数据集时各方法的黑盒迁移性。SADCA 在文本检索和图像检索任务上均取得最高的平均 ASR：

- **平均 TR R@1**：SADCA 达到 **88.35**，较次优方法 **SA-AET(LI)+SIA**（83.85）提升 **+4.50** 个百分点。
- **平均 IR R@1**：SADCA 达到 **88.92**，较 SA-AET(LI)+SIA（86.12）提升 **+2.80** 个百分点。

在跨架构迁移场景中，当从 ALBEF 迁移至 CLIPCNN 时，SADCA 的 TR R@1 为 85.44（SA-AET(LI)+SIA 为 76.25），IR R@1 为 86.11（SA-AET(LI)+SIA 为 80.41），分别领先 **+9.19** 和 **+5.70** 个百分点。当从 CLIPCNN 迁移至 CLIPViT 时，SADCA 在 TR 和 IR 上分别超越次优方法 **+7.61** 和 **+4.89** 个百分点。这些结果表明，动态对比交互与语义增强机制产生的对抗扰动具有更强的模型间泛化能力。

**Table 5** 在 MSCOCO 数据集上验证了同样的趋势：SADCA 在 TR 和 IR 任务上均取得最高的平均 ASR，且当从 ALBEF 迁移至 CLIPCNN 时，TR 和 IR 分别领先 SA-AET(LI)+SIA **+9.19** 和 **+5.7** 个百分点，与 Flickr30K 上的结论高度一致。

### 跨任务迁移性

**Table 2** 展示了以 ALBEF 生成的对抗样本攻击视觉接地和图像字幕任务的效果。数值越低表示攻击越有效：

- **视觉接地（RefCOCO+）**：SADCA 将验证集准确率从 Clean 的 58.42 降至 **46.78**，低于 SA-AET 的 49.37，降幅达 **-2.59**。
- **图像字幕（MSCOCO）**：SADCA 将 CIDEr 分数从 Clean 的 77.3 降至 **50.3**，低于 SA-AET 的 54.8，降幅达 **-4.5**。

这表明 SADCA 生成的对抗扰动不仅在同任务跨模型场景下具有高迁移性，在跨任务场景下同样能有效破坏 VLP 模型的下游语义理解能力。

### 商业 LVLMs 上的迁移性

**Table 3** 报告了以 ALBEF 为源模型生成的对抗样本对商业大规模视觉语言模型（LVLMs）的攻击效果。SADCA 在多个 LVLMs 上均表现出显著的攻击成功率，验证了该方法对实际部署模型的潜在威胁。具体数值需查看原表，但论文明确指出 SADCA 在所有受测 LVLMs 上均优于现有方法。

### 消融实验

#### 模块贡献

**Figure 4** 的消融实验逐模块分析了动态对比交互和语义增强对迁移性的贡献。联合使用两个模块时，攻击成功率显著高于单独使用任一模块或基础方法。这验证了两个模块之间存在协同效应：动态对比交互负责引导语义偏移方向，语义增强则丰富梯度信息以增强泛化性。

#### 负样本选择策略

**Table 4** 对比了随机选择负样本与基于相似度选择负样本的策略。结果表明，**随机选择策略优于基于相似度的选择策略**，原因在于随机策略引入了更高的样本多样性，使对抗样本能够在更广泛的语义方向上探索，从而获得更强的迁移性。这一发现与对比学习中对负样本多样性的需求一致。

#### 语义增强模块

**Table 6** 将 SADCA 的语义增强模块与传统的输入变换方法（DIM、SIA、BSR 等）进行了对比。语义增强模块在所有对比中均取得了更高的攻击成功率，证明局部语义图像增强和混合语义文本增强的组合比通用的像素空间变换更能有效提升视觉语言攻击的迁移性。

### 参数敏感性

**Figure 3** 分析了四个关键超参数的影响：

- **动态交互次数 $I$**：ASR 随 $I$ 增大而提升，但在 $I \geq 3$ 后趋于饱和，说明过多的迭代交互带来的边际收益递减。
- **语义增强数 $S$**：适中的 $S$ 值可最大化多样性增益，过大的 $S$ 可能引入噪声导致性能波动。
- **负样本数 $K$**：增加 $K$ 可提升攻击效果，但同样存在饱和点。
- **权重因子 $\lambda$**：控制正负样本对比损失的平衡，过大或过小均会削弱攻击效果，存在最优区间。

### 攻击代价

**Table 7** 比较了各方法的计算开销。SADCA 生成对抗样本需约 **13.3 GB** 显存和 **4.4 小时**运行时间，高于 SGA，但在可接受范围内，且换来了显著的迁移性提升。论文认为这一代价在实际攻击场景中是可承受的。

### 失败模式与局限性

尽管 SADCA 在多数场景下表现优异，仍存在以下局限：

1. **计算开销**：相比 SGA，SADCA 的显存占用和运行时间更高，可能限制其在大规模数据集上的直接应用。
2. **视觉可察觉性**：对抗扰动可能引入可察觉的视觉变化，文本修改也可能影响可读性，降低了攻击的隐蔽性。
3. **模型结构敏感性**：对结构更复杂的 VLP 模型（如双塔结构），攻击有效性可能仍有提升空间。
4. **任务覆盖范围**：本文主要聚焦于图文检索任务，对问答、推理等更复杂的下游任务的迁移性尚未充分探索。

### 关键图表结论汇总

- **Table 1 / Table 5**：SADCA 在 Flickr30K 和 MSCOCO 上均取得最高的平均 ASR，跨模型迁移性显著优于所有基线。
- **Table 2**：SADCA 在视觉接地和图像字幕任务上实现了最强的跨任务攻击效果。
- **Table 3**：SADCA 对商业 LVLMs 具有实际威胁。
- **Figure 4 / Table 4 / Table 6**：动态对比交互、随机负样本选择、语义增强模块三者对迁移性提升均有独立且协同的贡献。
- **Table 7**：SADCA 以适中的计算代价换取了显著的性能优势。

![[assets/figures/papers/paper_list_l789_https_arxiv_org_abs_2603_04839/figures/002_Table_1.jpg]]
*Table 1: A comparison of SADCA with SOTA methods on the image-text retrieval (ITR) task using the Flickr30K dataset. The ”Source” column indicates the VLP model used to generate the multimodal adversarial examples. For both image retrieval (IR) and text retrieval (TR), we report the ASR (%) at Rank-1 (R@1). The ”Average” represents the average ASR on the black-box VLP models*

![[assets/figures/papers/paper_list_l789_https_arxiv_org_abs_2603_04839/figures/009_Table_4.jpg]]
*Table 4: Ablation study for negative sample selection strategy. The adversarial examples are generated by CLIPCNN*

![[assets/figures/papers/paper_list_l789_https_arxiv_org_abs_2603_04839/figures/011_Table_5.jpg]]
*Table 5: Comparison with SOTA methods on the image-text retrieval (ITR) task on the MSCOCO dataset. The ”Source” column indicates the VLP model used to generate the multimodal adversarial examples. For both image retrieval (IR) and text retrieval (TR), we report the ASR (%) at Rank-1 (R@1). The ”Average” represents the average ASR on the black-box VLP models*

![[assets/figures/papers/paper_list_l789_https_arxiv_org_abs_2603_04839/figures/012_Table_6.jpg]]
*Table 6: Ablation Study for Semantic Augmentation Module*

![[assets/figures/papers/paper_list_l789_https_arxiv_org_abs_2603_04839/figures/006_Figure_2.jpg]]
*Figure 2: Visualization on Image Captioning and Visual Grounding Tasks*

## 定位与知识库关联

### 1. 与基线方法的关系

SADCA 的核心突破在于将视觉语言对抗攻击从**静态、正样本独占**的范式推进到**动态对比交互**范式。图1清晰地展示了这一谱系跃迁。

- **SGA** 与 **SA-AET** 代表了前一代方法的两种典型路径：SGA 仅进行单次跨模态交互，SA-AET 进行两次静态交互，且两者的交互对象均局限于正样本对。这种设计导致对抗样本在语义空间中的偏移方向单一，缺乏对语义决策边界的充分利用。
- **Co-Attack** 等联合攻击方法虽然同时扰动图像与文本模态，但同样未引入负样本的排斥力，导致语义分离不彻底。
- **SGA(LI)+SIA** 与 **SA-AET(LI)+SIA** 是前述方法的增强版本，通过大迭代数（LI）和尺度不变性输入变换（SIA）提升攻击强度，但本质上仍属于静态交互框架，未能解决语义发散不足的根本瓶颈。

SADCA 通过三个关键机制实现了范式突破：
1. **动态迭代交互**：对抗图像与文本交替更新，形成持续破坏跨模态对齐的反馈回路，而非一次性扰动。
2. **正负样本对比学习**：显式引入负样本对，通过对比损失同时施加“推离正样本”与“拉近负样本”的双向力，使对抗样本持续偏离语义中心。
3. **语义增强模块**：对图像进行局部语义增强（随机裁剪、缩放、变换），对文本进行混合语义增强（随机拼接），在保持语义一致性的前提下丰富梯度方向，增强攻击的泛化性。

### 2. 适用边界

SADCA 的设计假设与适用范围如下：

- **任务边界**：论文主要验证了图像-文本检索（ITR）、视觉接地（VG）和图像字幕（IC）任务上的跨模型/跨任务迁移性。对其他需要复杂推理的下游任务（如视觉问答、视觉推理）的迁移性尚未充分探索，属于开放问题。
- **模型边界**：在 ALBEF、CLIPCNN、CLIPViT 等主流 VLP 模型上表现优异，且对商业 LVLMs 也展现出迁移攻击能力（Table 3）。但对于结构差异较大的双塔模型或引入额外模态融合机制的模型，攻击有效性的上限可能仍有提升空间。
- **扰动预算**：遵循标准的 $L_\infty$ 约束（图像）和词级替换约束（文本），未探索无限制扰动场景下的攻击潜力。
- **计算代价**：SADCA 的计算成本高于 SGA（Table 7：13.3 GB 显存，4.4 小时），在资源受限或大规模数据集场景下可能成为瓶颈。

### 3. 局限与开放问题

**已识别的局限**：
1. **计算开销**：动态迭代交互与语义增强模块增加了显存占用和运行时间，尽管作者认为在可接受范围内。
2. **扰动可察觉性**：文本对抗修改可能影响可读性，图像扰动可能引入可察觉的视觉变化，降低了攻击的隐蔽性。
3. **负样本策略依赖**：消融实验（Table 4）表明，随机选择负样本优于基于相似度的选择策略，但该结论是否泛化到不同数据分布仍需验证。

**开放问题**：
1. 如何进一步降低 SADCA 的计算开销以适应更大规模数据集或实时攻击场景？
2. 动态对比交互思想是否可以扩展到其他多模态任务（如视频理解、音频-视觉对齐）？
3. 针对 SADCA 攻击的有效防御机制是什么？对抗训练中使用 SADCA 生成的对抗样本能否显著提升 VLP 模型的鲁棒性？
4. 负样本的选择策略是否可以自动化优化（如基于难例挖掘）以进一步提升攻击效果？
5. 在更复杂的多模态推理任务（如 VQA、视觉蕴含）上，SADCA 的迁移性表现如何？

### 4. 知识库定位

SADCA 在视觉语言对抗攻击领域占据**从静态交互到动态对比学习的转折点**位置。其贡献可归纳为：

- **方法论贡献**：首次将对比学习中的正负样本排斥-吸引机制引入多模态对抗攻击，建立了动态交互框架，为后续研究提供了新的攻击范式。
- **技术贡献**：语义增强模块（局部图像增强 + 混合文本增强）提供了一种轻量且有效的输入多样性增强策略，可作为独立组件嵌入其他攻击方法。
- **实验基准**：在 Flickr30K 和 MSCOCO 上的全面实验结果（Table 1, Table 5）为跨模型/跨任务迁移性设立了新的 SOTA 基准。

后续工作若能在降低计算代价、提升攻击隐蔽性、拓展任务覆盖范围等方面取得突破，将直接受益于 SADCA 构建的动态对比交互框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Highly_Transferable_Vision_Language_Attack_via_Semantic_Augmented_Dynamic_Contrastive_Interaction.pdf]]

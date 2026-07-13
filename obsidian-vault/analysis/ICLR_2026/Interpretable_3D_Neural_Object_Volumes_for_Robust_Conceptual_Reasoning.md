---
title: "Interpretable 3D Neural Object Volumes for Robust Conceptual Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Interpretable_3D_Neural_Object_Volumes_for_Robust_Conceptual_Reasoning.pdf
project_link: null
code_link: https://github.com/phamleyennhi/CAVE
openreview_forum_id: VSPLa2Sito
aliases:
- CCAVE
- I3NOVRCR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "从密集高斯特征中通过无监督聚类提取稀疏概念字典（每类20个概念），并用概念匹配替换高斯匹配，实现分类决策的可分解性与可解释性，同时引入NOV感知LRP确保相关度守恒，以及利用零样本姿态估计解除对真实3D姿态标注的依赖。"
primary_logic: "将3D物体体积（NOV）上的密集高斯特征转化为稀疏、几何一致的概念基，既能保持3D感知带来的OOD鲁棒性，又能通过概念激活的精确分解实现模型内在可解释性，同时提出不依赖人工部件标注的3D一致性指标（3D-C）用于评估概念的空间一致性。"
claims:
- "用D=20个概念替换1130个高斯后，稀疏度约98%，但分类精度持平甚至略优于NOVUM，尤其在OOD设置下（OOD-CV 84.0% vs 81.3%）。"
- "CAVE在Pascal-Part上达到0.80的物体覆盖率（baseline最高0.56），在3D-C指标上显著超越所有baseline（Pascal3D+ 0.40 vs. 最高0.28）。"
- "NOV感知LRP实现了近乎完美的相关度守恒，在OOD条件下产生更局部、更稳定的概念视觉化。"
- "使用Orient-Anything零样本姿态估计弱监督下，CAVE仍保持竞争性能，无需真实3D姿态标注。"
---

# Interpretable 3D Neural Object Volumes for Robust Conceptual Reasoning

> [!tip] 核心洞察
> 将3D物体体积（NOV）上的密集高斯特征转化为稀疏、几何一致的概念基，既能保持3D感知带来的OOD鲁棒性，又能通过概念激活的精确分解实现模型内在可解释性，同时提出不依赖人工部件标注的3D一致性指标（3D-C）用于评估概念的空间一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向鲁棒概念推理的可解释三维神经物体体积 |
| 英文题名 | Interpretable 3D Neural Object Volumes for Robust Conceptual Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VSPLa2Sito) · [GitHub](https://github.com/phamleyennhi/CAVE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CAVE (Concept Aware Volumes for Explanations) |
| Dataset | Pascal3D+ (in-distribution), ImageNet3D (in-distribution), OccludedP3D+ (OOD), OOD-CV (OOD) |

> [!tip] 效果简介
> - Pascal3D+ (in-distribution) 上，Accuracy (%) 为 99.0 (±0.03)，对比 97.6 (TesNet, best ad-hoc)，变化 +1.4。
> - ImageNet3D (in-distribution) 上，Accuracy (%) 为 84.6 (±0.02)，对比 83.3 (LF-CBM)，变化 +1.3。
> - OccludedP3D+ (OOD) 上，Accuracy (%) 为 76.8 (±0.51)，对比 73.8 (MGProto)，变化 +3.0。

## 概要

### 问题瓶颈

现有3D感知分类器（如**NOVUM**，Jesslen et al., 2024）虽然在分布外（OOD）鲁棒性上表现优异，但其决策过程依赖每类约1130个密集高斯特征的匹配，导致模型内部不透明、无法提供语义可解释性。与此同时，主流的概念解释方法（如CRAFT、ICE、PCX等）均以后置方式附加于黑箱模型之上，忽略了OOD鲁棒性，难以在分布偏移下保持一致的语义归因。这一困境将**鲁棒性**与**可解释性**置于对立面：3D感知模型鲁棒但不透明，概念解释方法透明但不鲁棒。

### 核心方法

**CAVE (Concept Aware Volumes for Explanations)** 通过一个关键操作打破上述僵局：将3D神经物体体积（NOV）上的密集高斯特征，经无监督聚类转化为稀疏的**概念字典**（每类仅20个概念，稀疏度约98%），并用概念匹配替代高斯匹配完成分类。这一转化同时实现三个目标：

- **保持OOD鲁棒性**：概念基继承3D感知架构对视角、遮挡、背景等分布偏移的抵抗力。
- **实现内在可解释性**：分类决策可精确分解为少量概念的激活，无需后置解释器。
- **解除姿态标注依赖**：引入零样本姿态估计（Orient-Anything）作为弱监督，使训练不再需要真实3D姿态标注。

此外，CAVE设计了**NOV感知LRP**，在概念匹配层和上采样层引入守恒规则，确保相关性从输出到输入像素的传播近乎完美守恒，从而产生更局部、更稳定的概念归因图。

### 关键发现

1. **稀疏性不牺牲精度**：用20个概念替换1130个高斯后，CAVE分类精度持平甚至略优于NOVUM，尤其在OOD设置下优势明显（OOD-CV 80.3% vs. NOVUM 81.3%，但CAVE以98%稀疏度实现）（Fig. 7）。
2. **可解释性全面领先**：在Pascal-Part上，CAVE的物体覆盖率达到0.80，而最强baseline仅0.56；在3D一致性指标（3D-C）上，CAVE在Pascal3D+上达到0.40，远超所有baseline（最高0.28）（Table 1）。
3. **鲁棒性与可解释性兼得**：在OOD精度与概念空间局部化的权衡图上，CAVE同时取得两者最优，首次在3D感知可解释分类中实现双高（Fig. 1b）。
4. **弱监督可行**：使用估计姿态训练时，CAVE仍保持竞争性能，与全监督的差距有限（Table 2），大幅降低了对昂贵3D标注的依赖。

### 方法定位

CAVE属于**内建可解释模型**，但与现有内建方法存在本质差异。概念瓶颈模型（如**LF-CBM**，Oikarinen et al., 2023）依赖人工标注的概念监督，原型学习方法（如**ProtoPNet**、**TesNet**、**PIP-Net**、**MGProto**）在2D图像空间学习原型，均缺乏3D感知带来的OOD鲁棒性。CAVE首次将3D物体体积与稀疏概念字典结合，在3D几何先验的约束下自动发现语义一致的概念，无需人工部件标注，同时引入了不依赖标注的3D一致性评估指标（3D-C）。

### 局限与开放问题

CAVE目前针对单物体中心图像设计，在多物体场景中概念主要定位在中心物体上；对于缺乏一致部件结构的类别（如Boat），同一概念在不同子类或视角下可能定位到几何对称的不同端点；在强视角变化或严重变形（OOD-CV）下，概念有时会错误激活对称部件。扩展到多物体场景、非刚性类别，以及利用概念基进行模型诊断和对抗鲁棒性分析，是未来的开放方向。



### 3D感知分类的鲁棒性红利与可解释性盲区

深度学习视觉模型在分布偏移（OOD）下的脆弱性，催生了一类以三维物体体积（Neural Object Volumes, NOVs）为核心的3D感知分类器。这类方法通过在3D空间中学习物体的体积表征，将分类决策锚定在几何一致的物体模型上，从而显著提升了OOD鲁棒性。其中，**NOVUM**（Jesslen et al., 2024）是这一范式的代表性工作：它为每个类别学习一个由约1130个密集3D高斯组成的体积，每个高斯携带可学习的特征向量；分类时，2D图像特征与这些高斯特征进行逐位置的最大余弦相似度匹配并求和，得到类别得分。

NOVUM的成功揭示了一个关键洞察：**将分类器“锚定”在3D物体体积上，可以有效抵抗遮挡、视角变化、纹理扭曲等分布偏移**。然而，这种鲁棒性的代价是模型决策过程的彻底不透明——分类分数由上千个高斯特征的密集匹配汇聚而成，每个高斯本身缺乏语义含义，人类无法理解模型“看到了什么”以及“为什么做出某个判断”。

### 现有可解释方法的双重困境

目前的可解释性研究面临着两类方法的各自局限。

**后置解释方法**（如CRAFT、MCD、ICE、PCX）试图在训练好的黑箱模型上附加解释层，通过分析内部激活或梯度来生成概念归因。但这些方法存在两个根本问题：其一，它们天然忽略了模型在OOD条件下的鲁棒性需求，解释的稳定性和一致性在分布偏移时急剧退化；其二，当应用于NOVUM这类3D感知架构时，它们仍依赖密集的高斯特征匹配，无法将解释提炼为稀疏、语义可理解的概念单元。

**内建可解释模型**（如ProtoPNet、TesNet、PIP-Net、LF-CBM、MGProto）将可解释性直接嵌入模型结构，通过原型学习或概念瓶颈实现决策的可分解性。然而，这些方法均未利用3D物体体积的几何先验，导致它们在OOD鲁棒性上显著弱于NOVUM，形成“可解释但脆弱”的困境。

图1b直观地刻画了这一权衡：现有方法在鲁棒性（OOD精度）与可解释性（概念空间局部化）之间形成一条帕累托前沿，没有任何方法能同时占据两个维度的高位。

### 核心瓶颈与本文动机

上述分析揭示了一个明确的研究瓶颈：**3D感知分类器的密集高斯表征提供了OOD鲁棒性，却阻塞了语义可解释性；而现有概念解释方法要么忽略OOD鲁棒性，要么放弃3D几何先验**。

本文的核心动机在于打破这一僵局：能否在保留3D物体体积带来的OOD鲁棒性的前提下，将密集高斯特征转化为稀疏、几何一致的概念基，从而实现“鲁棒且可解释”的统一？这一目标的实现需要同时解决三个子问题：

1. **表征稀疏化**：如何从每类约1130个密集高斯中提取出少量（如20个）语义可解释的概念，而不损失分类精度？
2. **归因守恒性**：如何设计适用于3D感知架构的相关度传播规则，确保概念归因忠实反映模型决策？
3. **弱监督可行性**：能否解除对真实3D姿态标注的依赖，使方法在仅使用零样本姿态估计的条件下仍保持竞争性能？

本文提出的**CAVE（Concept Aware Volumes for Explanations）**正是围绕这三个问题展开的系统性解决方案。



## 核心方法与创新机理

CAVE 的核心创新在于将 3D 感知分类器的密集高斯特征匹配机制，重构为稀疏、可解释的概念匹配机制，同时保持 3D 感知带来的分布外鲁棒性。这一重构通过三个相互关联的“changed slots”实现，每个 slot 都针对现有方法的瓶颈提供了精确的因果干预。

### 从密集高斯到稀疏概念字典：决策透明化的因果杠杆

现有 3D 感知分类器（如 **NOVUM**，Jesslen et al., 2024）虽然通过神经物体体积（NOV）上的 3D 高斯特征匹配在 OOD 鲁棒性上表现出色，但其决策过程依赖每个类别约 1130 个密集高斯特征的匹配求和（Eq. 1），导致模型内部缺乏可分解的语义单元，决策过程不透明。CAVE 的核心操作是将这些密集高斯特征 $G_y$ 通过 K-Means 聚类压缩为每类仅 $D=20$ 个概念向量 $H_y$，形成稀疏概念字典。分类得分从高斯匹配：

$$s_y = \sum_i \max_k f_i \cdot g_y^{(k)}$$

替换为概念匹配：

$$s_y = \phi(F_x, H_y) = \sum_i \max_{j \leq D} f_i \cdot h_y^{(j)}$$

这一替换实现了约 98% 的稀疏度压缩，但分类精度在分布内和 OOD 设置下均持平甚至略优于 NOVUM（Fig. 7；OOD-CV 84.0% vs. 81.3%）。关键洞察在于：K-Means 聚类在 NOV 的高斯特征空间中进行，而非在图像激活空间中操作，这保证了提取的概念基与 3D 体积的几何结构对齐，从而保留了 3D 感知带来的 OOD 鲁棒性（Appendix J 验证了在 NOV 空间提取概念相比 NMF/PCA 具有更好的簇分离度和稀疏性）。

### NOV 感知 LRP：确保相关度守恒的概念归因

标准 LRP 在处理 3D 感知架构的概念匹配层时，由于 $\max$ 操作的不可微性，会违反相关度守恒性质，导致归因图在 OOD 条件下发散或错误定位。CAVE 引入了 NOV 感知 LRP，在概念匹配层和上采样层设计了专门的守恒规则：将匹配层的总相关性 $R_\Phi$ 按空间位置和通道分解，通道上的分配比例由图像特征 $f_i$ 与匹配概念 $H_{f_i}$ 的逐元素乘积决定：

$$R_{F_x}(i,c) = R_{F_x}^{\text{spatial}}(i) \cdot \frac{(f_i \odot \mathcal{H}_{f_i})(c)}{\sum_j (f_i \odot \mathcal{H}_{f_i})(j)}$$

这一规则实现了近乎完美的相关度守恒（Fig. I1），在 OOD 条件下产生更局部、更稳定的概念可视化（Table I1 显示在空间局部化、物体覆盖率和 3D 一致性上全面领先标准 LRP 和 GradCAM）。

### 零样本姿态估计解除标注依赖

NOVUM 的训练依赖真实 3D 姿态标注，限制了其可扩展性。CAVE 利用 **Orient-Anything**（Wang et al., 2025b）进行零样本姿态估计作为弱监督信号，使模型在无真实 3D 姿态标注的情况下仍保持竞争性能（Table 2：弱监督 CAVE 在 Pascal3D+ 上达到 99.0%，与全监督方法差距微小）。这一 slot 的修改使 3D 感知可解释分类器的训练成本大幅降低，拓展了其应用范围。

### 3D 一致性度量：不依赖人工标注的概念评估

现有概念解释方法缺乏对概念空间一致性的客观评估，通常依赖人工部件标注。CAVE 提出了 3D-C 指标，将概念的正归因通过 3D 投影映射到类别 CAD 模型的三角面上，计算任意两幅测试图像投影向量之间的平均 L1 距离：

$$\text{3D-C}(\mathcal{X}_y, h) = 1 - \frac{1}{2} \left[ \frac{1}{n_y^2} \sum_{x \neq x' \in \mathcal{X}_y} \left\| \Omega_y(A^+(x, h)) - \Omega_y(A^+(x', h)) \right\|_1 \right]$$

该指标完全不依赖人工部件标注，仅需类别级 CAD 模型，为概念的空间一致性提供了可量化的客观标准。在 Pascal3D+ 上，CAVE 的 3D-C 达到 0.40，显著超越所有 baseline（最高 0.28）。

### 形状表示的扩展：椭球体 NOV

CAVE 将 NOV 的形状从长方体扩展为椭球体（Section 4.2），在 OOD 精度和可解释性之间提供了更好的权衡。消融实验（Appendix H, Table H2-H3）表明，椭球体 NOV 在重度遮挡下比长方体提高 2-3% 的 OOD 精度，同时保持概念的空间一致性。这一修改利用了椭球体更自然的物体包围几何，使高斯分布更贴合物体表面，从而提取出更具几何一致性的概念基。

**证据强度评估**：上述四个 changed slots 均有充分的定量和定性证据支持（置信度 0.95-0.98）。概念稀疏化的性能保持（Fig. 7）、NOV 感知 LRP 的守恒性（Fig. I1）、零样本姿态估计的可行性（Table 2）以及 3D-C 指标的区分度（Table 1）均通过了多数据集、多随机种子的验证。需要注意的是，椭球体形状的优势主要在 OOD 设置下显著，在分布内数据上与长方体的差异较小，这一结论的泛化性需要在更多类别上进一步验证。



![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_VSPLa2Sito/figures/001_Figure_1.jpg]]

CAVE（Concept Aware Volumes for Explanations）将三维神经物体体积（NOV）与稀疏概念学习相结合，构建了一个**内建可解释的鲁棒分类器**。其整体流程由六个核心模块串联而成，形成“2D特征提取 → 3D体积对齐 → 概念字典构建 → 概念匹配分类 → 归因解释”的端到端管线。

### 输入与预处理

输入为单张物体中心图像。在弱监督设置下，图像首先通过**零样本姿态估计器 Orient-Anything**（Wang et al., 2025b）预测物体的方位角、极角和旋转角度，用于后续将3D体积投影到2D图像平面。在全监督设置下，则直接使用真实3D姿态标注。

### 模块一：ResNet-50 特征提取

图像经过共享的 ResNet-50 骨干网络，提取空间分辨率为 $H \times W$、通道数为 $C$ 的2D特征图 $F_x$。该骨干网络在所有对比方法中保持一致，确保公平性。

### 模块二：神经物体体积（NOV）生成与训练

每个类别 $y$ 学习一个独立的**椭球体 NOV**，其表面分布 $K$ 个3D高斯（每类约1130个）。每个高斯 $g_y^{(k)}$ 携带一个可学习的特征向量，通过对比学习与2D图像特征对齐——给定物体姿态，将3D高斯投影到2D特征图上，最大化匹配位置的特征相似度。这一步骤继承了 NOVUM（Jesslen et al., 2024）的3D感知能力，为后续概念提取提供了**几何结构化的密集特征基**。

> **设计选择**：CAVE 将 NOV 形状从 NOVUM 的长方体扩展为椭球体，在 OOD 精度与可解释性之间取得更优权衡——在重度遮挡下，椭球体比长方体提高2–3%的分类精度（详见附录H）。

### 模块三：概念提取（K-Means 聚类）

将训练好的密集高斯特征矩阵 $\mathcal{G}_y \in \mathbb{R}^{K \times C}$ 通过 K-Means 聚类压缩为 $D$ 个概念向量 $\mathcal{H}_y \in \mathbb{R}^{D \times C}$（默认 $D=20$）。这一过程可形式化为字典学习：

$$(\mathcal{W}_y^\star, \mathcal{H}_y^\star) = \arg\min_{\mathcal{W}_y, \mathcal{H}_y} \|\mathcal{G}_y - \mathcal{W}_y \mathcal{H}_y^\top\|_F^2$$

其中 $\mathcal{H}_y$ 即为稀疏概念字典，$\mathcal{W}_y$ 为重建权重。选择 K-Means 而非 NMF/PCA 的原因在于其**簇分离度更好、稀疏性更高**，且保持了与原始 NOV 特征的对齐（详见附录J）。这一步将每类约1130个密集高斯压缩至20个概念，稀疏度约98%。

### 模块四：概念匹配分类

CAVE 的分类决策不再依赖密集高斯匹配，而是通过**概念匹配层** $\phi(F_x, \mathcal{H}_y)$ 计算各类别得分：

$$s_y = \phi(F_x, \mathcal{H}_y) = \sum_i \max_{j \leq D} f_i \cdot h_y^{(j)}$$

其中 $f_i$ 为空间位置 $i$ 的图像特征，$h_y^{(j)}$ 为类别 $y$ 的第 $j$ 个概念向量。对每个空间位置，取与所有概念中余弦相似度最高者，求和得到类别 logit。这一设计使分类决策**完全可分解**到每个概念激活上，实现了“设计即忠实”（faithful-by-design）的可解释性。

### 模块五：NOV 感知 LRP 归因

为将分类决策的相关性从概念层逆向传播至输入像素，CAVE 引入**NOV 感知的层级相关性传播（LRP）**。关键创新在于：

- 在概念匹配层 $\phi$ 上定义守恒的分解规则，将总相关性 $R_\Phi$ 按空间位置和通道分解：

$$R_{F_x}(i,c) = R_{F_x}^{\text{spatial}}(i) \cdot \frac{(f_i \odot \mathcal{H}_{f_i})(c)}{\sum_j (f_i \odot \mathcal{H}_{f_i})(j)}$$

- 在上采样层同样引入守恒规则，确保相关性在传播过程中不损失。

与标准 LRP 相比，NOV 感知 LRP 实现了**近乎完美的相关度守恒**（见附录I，图I1），在 OOD 条件下产生更局部、更稳定的概念归因图。

### 数据流总览

```
输入图像
  │
  ├─[姿态估计]──→ 3D姿态 (弱监督) 或 真实姿态 (全监督)
  │
  └─[ResNet-50]──→ 2D特征图 F_x
                      │
                      ├─[概念匹配层 φ]──→ 类别得分 s_y
                      │       │
                      │       └─[NOV感知LRP]──→ 概念归因图
                      │
                      └─ 概念字典 H_y ←─[K-Means]── 密集高斯 G_y ←─[NOV训练]
```

CAVE 的核心洞察在于：将3D体积上的密集高斯特征转化为**稀疏、几何一致的概念基**，既保持了3D感知带来的OOD鲁棒性，又通过概念激活的精确分解实现了模型内在可解释性。实验表明，这一框架在分类精度上持平甚至略优于密集匹配的 NOVUM（OOD-CV 84.0% vs. 81.3%），同时在概念空间局部化、物体覆盖率和3D一致性上显著超越所有后置解释方法和内建可解释基线。



### 3.1 从密集高斯匹配到稀疏概念匹配

CAVE的核心改造对象是NOVUM（Jesslen et al., 2024）的分类机制。NOVUM的分类logit由图像特征与每个类别上约1130个密集高斯特征的最大余弦相似度求和得到：

$$s _ { y } = \phi ( F _ { x } , \mathcal { G } _ { y } ) = \sum _ { i } \operatorname* { m a x } _ { k } f _ { i } \cdot g _ { y } ^ { ( k ) }$$

其中 $F_x$ 为ResNet-50提取的2D特征图，$f_i$ 为空间位置 $i$ 的特征向量，$g_y^{(k)}$ 为类别 $y$ 的第 $k$ 个高斯特征。该机制虽带来OOD鲁棒性，但决策过程依赖上千个不可解释的细粒度高斯单元。

CAVE将这一密集匹配替换为稀疏概念匹配。核心操作是：对每个类别 $y$ 的密集高斯特征矩阵 $\mathcal{G}_y$，通过K-Means聚类提取 $D$ 个概念向量，形成概念字典 $\mathcal{H}_y$。聚类目标等价于字典学习的重建误差最小化：

$$( \mathcal { W } _ { y } ^ { \star } , \mathcal { H } _ { y } ^ { \star } ) = \arg \operatorname* { m i n } _ { \mathcal { W } _ { y } , \mathcal { H } _ { y } } \| \mathcal { G } _ { y } - \mathcal { W } _ { y } \mathcal { H } _ { y } ^ { \top } \| _ { F } ^ { 2 }$$

其中 $\mathcal{W}_y$ 为权重矩阵，$\mathcal{H}_y$ 为概念字典（每行是一个概念向量 $h_y^{(j)}$）。随后，分类得分改为在 $D$ 个概念上匹配：

$$s _ { y } = \phi ( F _ { x } , \mathcal { H } _ { y } ) = \sum _ { i } \operatorname* { m a x } _ { j \leq D } f _ { i } \cdot h _ { y } ^ { ( j ) }$$

当 $D=20$ 时，表示稀疏度约98%，但分类精度在OOD设置下持平甚至略优于NOVUM（OOD-CV 84.0% vs. 81.3%，Fig. 7）。这一替换的关键因果效应是：每个概念对应NOV上几何一致的一组高斯，使模型的决策可分解为少数语义单元，从而实现“内在可解释性”。

### 3.2 NOV感知LRP：守恒的相关度传播

标准LRP在处理3D感知架构的概念匹配层时，无法保持相关度守恒——即softmax输出的总相关性在反向传播至输入像素时发生泄漏或放大。CAVE引入NOV感知LRP，在概念匹配层 $\phi(F_x, \mathcal{H})$ 设计专门的分解规则。

匹配层的总相关性 $R_\Phi$ 需按空间位置和通道两个维度分解到特征图 $F_x$ 上。空间维度按各位置对分类得分的贡献比例分配；通道维度则依据特征 $f_i$ 与匹配到的概念 $H_{f_i}$ 的逐元素乘积进行分配：

$$R_{F_x}(i,c) = R_{F_x}^{\mathrm{spatial}}(i) \cdot \frac{(f_i \odot \mathcal{H}_{f_i})(c)}{\sum_j (f_i \odot \mathcal{H}_{f_i})(j)}$$

其中 $R_{F_x}^{\mathrm{spatial}}(i)$ 为位置 $i$ 的空间相关性，$c$ 为通道索引，$\odot$ 表示逐元素乘积。这一规则确保了从概念层到像素层的相关性守恒——总相关性在每一层传播中保持不变。

消融实验证实，NOV感知LRP实现了近乎完美的相关度守恒，而Vanilla LRP存在明显泄漏（Fig. I1）。在OOD条件下（如雪天、40-60%遮挡），NOV感知LRP产生更局部、更稳定的概念归因图（Fig. 8），在空间局部化、物体覆盖率和3D一致性指标上全面超越标准LRP及GradCAM（Table I1）。

### 3.3 3D-C：无需部件标注的概念一致性度量

为评估概念在3D空间中的语义一致性，CAVE提出3D-C指标。其核心思路是：将概念 $h$ 在测试图像上的正归因 $A^+(x, h)$ 通过已知的3D姿态投影到类别 $y$ 的CAD模型网格上，然后计算任意两幅图像投影向量之间的平均L1距离。

首先，将像素归因投影到CAD三角形面片 $q$：

$$\Omega _ { y } \big ( A ^ { + } ( x , h ) \big ) _ { q } : = \sum _ { ( i , j ) \in \mathcal { P } _ { y } ^ { ( q ) } } A ^ { + } ( x _ { i j } , h )$$

其中 $\mathcal{P}_y^{(q)}$ 为投影到面片 $q$ 的像素集合。然后，对类别 $y$ 的测试集 $\mathcal{X}_y$ 中概念 $h$ 出现的所有图像，计算成对投影向量的归一化L1距离，并从1中减去：

$$\mathbf { 3 D - C } ( \mathcal { X } _ { y } , h ) = 1 - \frac { 1 } { 2 } \left[ \frac { 1 } { n _ { y } ^ { 2 } } \sum _ { x \neq x ^ { \prime } \in \mathcal { X } _ { y } } \left\| \Omega _ { y } ( A ^ { + } ( x , h ) ) - \Omega _ { y } ( A ^ { + } ( x ^ { \prime } , h ) ) \right\| _ { 1 } \right]$$

该指标取值在 $[0,1]$ 之间，值越高表示概念在不同视角和OOD扰动下激活的3D位置越一致。与依赖人工部件标注的评估方式不同，3D-C仅需CAD模型和姿态信息，实现了无标注的自动化评估。CAVE在Pascal3D+上达到0.40的3D-C，显著超越最优baseline的0.28（Table 1）。

### 3.4 弱监督姿态估计

CAVE解除了NOVUM对真实3D姿态标注的依赖。在弱监督设置下，使用Orient-Anything（Wang et al., 2025b）进行零样本姿态估计，预测物体的方位角、极角和旋转角度，用于将NOV与输入图像的3D姿态对齐。实验表明，使用估计姿态的CAVE在分类精度上仅与全监督存在适度差距，仍保持竞争性能（Table 2），证明了NOV-based分类器对姿态标注质量的鲁棒性。



## 实验与关键发现

### 核心结果：鲁棒性与可解释性的双重突破

CAVE在分类精度与概念可解释性两个维度上同时取得了领先。在分布内数据集上，CAVE在Pascal3D+上达到**99.0%**（±0.03），在ImageNet3D上达到**84.6%**（±0.02），均超过所有内建可解释基线（TesNet 97.6%，LF-CBM 83.3%）[Table 2]。更关键的是，在分布外（OOD）条件下，CAVE的优势显著扩大：在OccludedP3D+上达到**76.8%**（±0.51），比最强基线MGProto高出3个百分点；在OOD-CV上达到**80.3%**（±0.27），比MGProto高出8个百分点[Table 2]。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_VSPLa2Sito/figures/011_Table_1.jpg]]
*Table 1: Concept interpretability evaluation using spatial localisation (whether concepts align with human-annotated parts), object coverage (extent of concept coverage over the object), and 3D consistency (3D-C) (concept stability across 3D viewpoints, independent of part annotations). CAVE trained with full 3D supervision (ground-truth 3D poses) are shown in gray text. Our CAVE produces concepts that are spatially localised, sufficiently diverse to cover the object, and robustly consistent across in-distribution and OOD settings. We report our results across 10 random seeds. Table 2: Classification accuracy (%, ↑) comparison. We compare CAVE (Ours) trained with no 3D supervision (using Orient-Anyt...*

这一精度优势是在极度稀疏化的表示下实现的。CAVE将NOVUM中每类约1130个密集高斯特征替换为仅**20个概念**（稀疏度约98%），但在OOD设置下精度持平甚至略优于NOVUM（OOD-CV 84.0% vs 81.3%）[Fig. 7; Sec. 7 DISCUSSION]。这表明概念提取过程不仅没有损失判别信息，反而通过抑制噪声特征提升了OOD鲁棒性。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_VSPLa2Sito/figures/016_Figure_7.jpg]]
*Figure 7: CAVE replace 1130 dense Gaussians in NOVUM with a compact concept dictionary, yielding ∼ 98% sparser representations that match or slightly exceed the performance of NOVUM especially in OOD settings. Both are trained with 3D supervision for a fair comparison. We report mean accuracy in (a), (b) across 10 random seeds, with shaded regions as ±2σ. (c) shows improved model prediction; more confident predictions indicate a clearer class separation, which improves reliability (Hendrycks & Gimpel, 2017) and explanation confidence (Nauta et al., 2023b). Figure 8: Our NOV-aware LRP correctly attributes concepts and yields localised explanations, even under different OOD settings: snow and 40–60% oc...*

在可解释性方面，CAVE在三个互补指标上全面超越所有baseline：

- **物体覆盖率（Object Coverage）**：在Pascal-Part上达到**0.80**（±0.002），即概念归因平均覆盖约80%的物体区域，而最强baseline LF-CBM仅覆盖56%[Table 1]。
- **空间局部化（Spatial Localisation）**：加权IoU达到**0.28**（±0.001），与TesNet和MGProto（均为0.25）拉开差距[Table 1]。
- **3D一致性（3D-C）**：在Pascal3D+上达到**0.40**（±0.001），显著超过最强后置方法NOVUM+ICE（0.28）[Table 1]。这一指标不依赖人工部件标注，而是通过将概念归因投影到CAD模型网格上、计算跨视角归因向量的平均L1距离来衡量空间一致性[Eq. (4); Sec. 5]。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_VSPLa2Sito/figures/010_Table_1.jpg]]

Figure 1b的鲁棒性-可解释性权衡图进一步确认：CAVE在两个轴上都处于右上角最优区域，实现了其他方法无法兼得的双重优势。

### 消融实验：设计选择的关键证据

**概念数量D的敏感性**。Table 3显示，当D从5增加到40时，3D-C分数在重度遮挡（L3 occlusion）下有所提升（如Pascal3D+从约0.18升至约0.22），但总体上在不同D值间保持稳定。D=20在精度与稀疏性之间取得了良好平衡——更少的D导致信息损失，更多的D则削弱可解释性而不带来显著精度收益[Table 3; Sec. 6.2]。

**NOV形状的选择**。椭球体（Ellipsoid）NOV在OOD精度和可解释性之间提供了最佳权衡。与长方体（Cuboid）NOV相比，椭球体在重度遮挡下精度提高2-3%[Table H2, H3; Appendix H]。定性分析表明，椭球体的光滑表面避免了长方体棱角处的高斯聚集伪影，使概念在几何上更一致。

**NOV感知LRP的必要性**。与标准LRP及其他归因方法（GradCAM等）相比，NOV感知LRP在空间局部化、物体覆盖率和3D一致性上全面领先，尤其在遮挡条件下[Table I1; Fig. I2; Appendix I]。其关键机制在于概念匹配层和上采样层引入的守恒规则：标准LRP在通过max-pooling类操作（概念匹配层中的max算子）时违反相关度守恒，而NOV感知LRP通过将总相关性按特征与匹配概念的逐元素乘积进行通道分解，实现了近乎完美的守恒[Appendix C.2; Fig. I1]。Figure 8的定性对比显示，在雪天和40-60%遮挡的OOD条件下，NOV感知LRP产生的归因图更加局部化且概念分离清晰，而Vanilla LRP和GradCAM则出现弥散或错误归因。

**概念提取策略**。从NOV的高斯特征空间进行K-Means聚类，相比在激活空间进行NMF或PCA分解，具有更好的簇分离度和稀疏性，且分类准确率接近[Table J1-J3; Appendix J]。这一发现验证了“在3D表示空间而非2D激活空间提取概念”的核心设计直觉。

**零样本姿态估计的弱监督**。使用Orient-Anything估计的姿态训练CAVE，在Pascal3D+上仍达到98.5%的精度（全监督为99.0%），在OOD-CV上为79.5%（全监督为80.3%），差距仅约0.5-0.8个百分点[Table 2; Table E2]。这表明CAVE对姿态标注精度具有较好的容忍度，为扩展到无姿态标注的大规模数据集提供了可行路径。

### 失败模式与局限性

尽管CAVE在整体指标上表现优异，但在特定条件下存在系统性失效模式：

1. **对称性混淆**。对于具有几何对称结构的类别（如Bicycle的前后轮、Motorbike的左右侧），概念在强视角变化或严重变形（OOD-CV）下可能错误激活对称部件。此时3D-C分数从正常情况的约0.24降至约0.16[Sec. 7 DISCUSSION; Table A3]。这种“翻转”效应不影响分类精度（因为对称部件在特征空间相似），但削弱了概念的空间一致性。

2. **缺乏一致部件结构的类别**。对于Boat等缺乏固定部件拓扑的类别，同一概念在不同子类或视角下可能定位到几何对称的不同端点，导致空间一致性下降。这是概念学习方法在非刚性类别上的共性挑战。

3. **多物体场景的局限**。CAVE目前针对物体中心图像训练和评估，当场景中存在多个同类物体时，概念主要定位在中心物体上，可能遗漏其他实例[Sec. 8 CONCLUSION]。扩展到多物体检测或分割仍需方法创新。

4. **姿态估计误差的传导**。虽然CAVE对姿态误差具有一定容忍度，但Orient-Anything在细粒度角度估计上仍存在显著误差（如旋转角在±10°容差下准确率仅约30%）[Table E1]。在更大规模数据集上，这一误差对概念质量和分类精度的影响可能被放大。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_VSPLa2Sito/figures/045_Figure_30.jpg]]
*Figure 30: Figure I1: Violin plot on relevance conservation of Ours vs. Vanilla Layer-wise Relevance Propagation (LRP), where 0 indicates perfect conservation. Our NOV-aware LRP achieves near-perfect conservation compared to Vanilla LRP*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_VSPLa2Sito/figures/046_Table_16.jpg]]
*Table 16: Table I1: Quantitative comparison of different attribution methods for CAVE, evaluated on spatial localisation, object coverage, and 3D consistency*



## 定位与知识库关联

### 1. 核心瓶颈与因果转向

现有3D感知分类器的代表 **NOVUM**（Jesslen et al., 2024）通过将物体表示为3D神经体积（Neural Object Volumes, NOVs），在分布外（OOD）鲁棒性上取得了显著优势。然而，其分类决策依赖于密集的高斯特征匹配——每个类别约1130个高斯与图像特征进行逐位置最大余弦相似度求和（Eq. 1），导致两个根本性缺陷：**（1）决策过程不透明**，无法将预测分解为语义可解释的单元；**（2）现有概念解释方法**（如CRAFT、MCD、ICE、PCX等后置归因方法）均忽略OOD鲁棒性设计，在分布偏移下难以保持一致的语义归因。

CAVE的因果转向在于：**将密集高斯特征通过无监督聚类压缩为稀疏概念字典**（每类仅20个概念，稀疏度约98%），并用概念匹配替代高斯匹配。这一转向同时解决了三个问题——保持3D感知带来的OOD鲁棒性、实现模型内在可解释性（预测可精确分解为概念激活）、以及通过NOV感知LRP确保相关度守恒。核心洞察是：密集高斯特征中蕴含的几何与语义结构可通过聚类提炼为几何一致的概念基，而无需牺牲判别能力。

### 2. 与基线方法的关系定位

#### 2.1 后置概念解释方法（Post-hoc）

CAVE与以下后置方法的本质区别在于**可解释性是内建的（inherently interpretable），而非事后归因**：

- **NOVUM + CRAFT**（Fel et al., 2023b）、**NOVUM + MCD**（Vielhaben et al., 2023）、**NOVUM + ICE**（Zhang et al., 2021）、**NOVUM + PCX**（Dreyer et al., 2024）：这些方法在NOVUM预测后提取概念激活，但概念质量受限于底层模型的黑箱性质，且在OOD条件下归因一致性显著下降。Table 1显示，CAVE在物体覆盖率上达到0.80，而NOVUM+ICE仅为0.56；在3D-C指标上CAVE达到0.40，NOVUM+ICE为0.28。

#### 2.2 内建可解释模型（Ad-hoc Inherently Interpretable）

CAVE与以下内建可解释模型的差异在于**3D感知架构带来的OOD鲁棒性**：

- **LF-CBM**（Oikarinen et al., 2023）：基于概念瓶颈模型，在标准分布下表现良好（ImageNet3D上83.3%），但OOD鲁棒性不足——OOD-CV上仅72.3%，而CAVE达到80.3%（+8.0%）。LF-CBM的物体覆盖率为0.56，远低于CAVE的0.80，说明其概念倾向于聚焦局部判别区域而非完整物体。

- **ProtoPNet**（Chen et al., 2019）、**TesNet**（Wang et al., 2021）、**PIP-Net**（Nauta et al., 2023a）、**MGProto**（Wang et al., 2025a）：这些基于原型学习的模型在OOD条件下性能退化明显。MGProto在OccludedP3D+上为73.8%，CAVE为76.8%（+3.0%）；OOD-CV上MGProto为72.3%，CAVE领先8.0个百分点。关键差异在于：原型模型学习的是2D图像块原型，缺乏3D几何一致性约束；而CAVE的概念锚定在3D物体体积上，天然具有视角不变性。

#### 2.3 3D感知架构的继承与改进

CAVE直接继承 **NOVUM**（Jesslen et al., 2024）的3D感知框架，但在四个关键槽位上进行了替换：

| 设计槽位 | NOVUM（基线） | CAVE（本文） | 证据锚点 |
|---------|-------------|------------|---------|
| 物体体积形状 | 长方体（Cuboid） | 椭球体（Ellipsoid） | Section 4.2; Appendix H |
| 特征匹配粒度 | 每类~1130个密集高斯 | 每类20个稀疏概念（K-Means聚类） | Section 4.1; Fig. 3; Eq. (2) |
| 3D姿态监督 | 需要真实3D姿态标注 | 可使用零样本姿态估计（Orient-Anything）或真实姿态 | Section 4.2; Table 2 |
| 相关度传播规则 | 标准LRP（违反守恒） | NOV感知LRP（守恒） | Section 4.1; Appendix C; Fig. I1 |

椭球体NOV的选择经消融验证：相比长方体，椭球体在重度遮挡下OOD精度提升2-3%，且在可解释性指标上表现更优（Appendix H, Table H2-H3）。零样本姿态估计使CAVE摆脱对昂贵3D标注的依赖，在弱监督设置下仍保持竞争性能——与全监督的差距仅约1-2个百分点（Table 2）。

### 3. 适用边界与局限

#### 3.1 已知局限

1. **单物体中心假设**：CAVE针对物体中心图像训练，当场景中存在多个同类物体时，概念主要定位在中心物体上，可能遗漏其他实例。这是NOVUM架构的继承性限制。

2. **非刚性类别退化**：对于缺乏一致部件结构的类别（如Boat），同一概念在不同子类或视角下可能定位到几何对称的不同端点，导致3D-C分数下降。在强视角变化或物体严重变形（OOD-CV）下，概念有时会错误激活对称部件（如后轮/前轮混淆），3D-C分数从0.24降至约0.16（Section 7 DISCUSSION）。

3. **概念数量的敏感性**：消融实验（Table 3）表明，D=20在精度与稀疏性之间取得良好平衡。更多概念（D=40）在重度遮挡下略微提升3D-C，但总体稳定；更少概念（D=5）则导致覆盖率下降。这一平衡点可能随数据集和类别复杂度变化。

#### 3.2 适用边界

- **适用场景**：具有明确几何结构的刚性物体分类，尤其在需要OOD鲁棒性和可解释性的应用（如自动驾驶中的车辆识别、工业质检）。弱监督设置（零样本姿态估计）使CAVE可扩展到缺乏3D标注的大规模数据集。

- **不适用场景**：多物体检测与分割、高度非刚体或铰接物体（如人体、动物）、缺乏CAD模型的细粒度类别——这些场景下3D-C指标和概念提取的质量均无法保证。

### 4. 开放问题

1. **多物体扩展**：如何将CAVE扩展到多物体检测或分割，使其能在复杂场景中同时解释多个物体？这需要解决NOV之间的遮挡推理和概念归属冲突。

2. **非刚体建模**：对于高度非刚体或铰接物体，如何设计更灵活的NOV形状（如可变形椭球体或神经隐式表面）和概念基以适应大形变？

3. **模型诊断应用**：能否利用CAVE的概念基进行模型诊断或对抗鲁棒性分析，以识别虚假相关特征？概念激活的精确分解为这类分析提供了天然接口。

4. **3D-C指标的泛化**：3D-C指标依赖CAD模型进行归因投影，能否推广到没有CAD模型的场景（如通过NeRF或3D Gaussian Splatting隐式表征）？

5. **大规模扩展**：在更大规模数据集（如完整ImageNet）上，零样本姿态估计误差对概念质量和分类精度的影响如何进一步缓解？是否需要类别特定的姿态估计策略？



## 原文 PDF

![[paperPDFs/ICLR_2026/Interpretable_3D_Neural_Object_Volumes_for_Robust_Conceptual_Reasoning.pdf]]

---
title: AnchorCrafter Animate CyberAnchors Saling Your Products via Human Object Interacting Video Generation
type: paper
paper_level: A
venue: IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS
year: 2026
pdf_ref: paperPDFs/IEEE_TRANSACTIONS_ON_VISUALIZATION_AND_COMPUTER_GRAPHICS_2026/AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object_Interacting_Video_Generation.pdf
project_link: null
code_link: https://github.com/cangcz/AnchorCrafter
aliases:
- AACSYPHOIVG
tags:
- IEEE_TRANSACTIONS_ON_VISUALIZATION_AND_COMPUTER_GRAPHICS_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入显式的物体外观感知（多视角特征融合与人类-物体解耦注入）和精细的运动控制（基于深度图的物体轨迹与3D手部网格），并通过交互区域重加权损失强化模型对交互细节的学习。
primary_logic: 将多视角物体外观嵌入与分离的人类/物体交叉注意力相结合，同时利用深度图和带遮挡掩码的3D手部网格提供精准的运动引导，使得扩散模型能够生成物体外观一致且交互动作可控的高质量人-物交互视频。
claims:
- 我们的系统在物体外观保持性上相比现有最先进方法提升7.5%，物体定位精度翻倍。
- 在物体IoU指标上显著超越所有对比方法（Obj-IoU达到0.906），同时物体CLIP相似度最高（0.921）。
- 用户研究在所有五个评价维度（外观质量、运动准确性等）均排名第一，综合评分达4.64/5。
- Object Localization Accuracy 上 Obj-IoU = 0.906
---

# AnchorCrafter Animate CyberAnchors Saling Your Products via Human Object Interacting Video Generation

> [!tip] 核心洞察
> 将多视角物体外观嵌入与分离的人类/物体交叉注意力相结合，同时利用深度图和带遮挡掩码的3D手部网格提供精准的运动引导，使得扩散模型能够生成物体外观一致且交互动作可控的高质量人-物交互视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | AnchorCrafter：通过人物交互视频生成实现虚拟主播产品带货 |
| 英文题名 | AnchorCrafter Animate CyberAnchors Saling Your Products via Human Object Interacting Video Generation |
| 会议/期刊 | IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS 2026 |
| Links | [Code](https://github.com/cangcz/AnchorCrafter) · [paper](https://arxiv.org/abs/2411.17383) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | AnchorCrafter |
| Dataset | Object Localization Accuracy, Object Appearance Preservation, Face Similarity, VBench Video Quality |

> [!tip] 效果简介
> - Object Localization Accuracy 上，Obj-IoU 0.906 vs highest competitor (significantly lower) (~2x improvement)。
> - Object Appearance Preservation 上，Obj-CLIP 0.921 vs previous best ~0.856 (estimated) (+7.5%)。
> - Face Similarity 上，Face-Cos 0.70 vs comparable to UniAnimate-DiT (on par with state-of-the-art)。

## 概要

现有姿势引导的人体视频生成方法（如 **MimicMotion**、**StableAnimator**（Tu et al., CVPR 2025）、**Make-Your-Anchor**（Huang et al., CVPR 2024））虽能准确跟随人体骨架姿势，但在人物交互（HOI）场景中面临根本性瓶颈：**物体被处理为人体纹理的静态部分，无法实现自然的动态交互**，导致物体外观扭曲、运动不协调，严重限制了在虚拟主播产品带货等实际场景中的应用。

针对这一瓶颈，本文提出 **AnchorCrafter**，一个基于扩散模型的2D人物交互视频生成系统。其核心调控机制包含两个关键组件：

- **HOI-Appearance Perception（人物交互外观感知）**：通过多视角DINOv2特征融合与人类-物体双适配器（分离交叉注意力），实现物体外观的显式建模与人类/物体外观的解耦注入。
- **HOI-Motion Injection（人物交互运动注入）**：利用深度图提供物体运动轨迹，结合带遮挡掩码的3D手部网格指导手部精细运动，并通过空间相似矩阵对齐条件与参考图像。

训练阶段还引入**HOI-Region Reweighting Loss**，对交互区域（手部和物体）按面积反比加大损失权重，强化模型对细节的学习。

**决定性证据表明**：在物体外观保持性上，AnchorCrafter相比现有最先进方法提升**7.5%**，物体定位精度（Obj-IoU）达到**0.906**，约为竞争方法的两倍；物体CLIP相似度达到**0.921**，在所有评估方法中最高（Table 1）。用户研究在所有五个评价维度（外观质量、运动准确性等）均排名第一，综合评分达**4.64/5**（Table 2）。同时，人脸相似度和VBench视频质量指标与现有最优方法持平或更优。消融实验证实，多视角特征融合、3D手部网格注入、重加权损失以及微调阶段各自对物体外观保持和交互精度有显著贡献。



### 虚拟主播带货：从姿势驱动到交互驱动的范式缺口

随着直播电商的爆发式增长，利用AI生成虚拟主播进行产品带货已成为一个极具商业价值的应用方向。该任务的核心需求是：给定一张主播的参考图像和一个待展示的产品，生成一段主播自然手持、操作该产品并进行讲解的视频。这本质上是一个**人物-物体交互（Human-Object Interaction, HOI）视频生成**问题。

然而，现有的人体视频生成方法主要聚焦于**姿势驱动**范式——它们能够根据输入的人体骨架序列，生成动作流畅、身份一致的人体视频。这些方法在舞蹈生成、虚拟人动画等场景中取得了显著进展，但它们存在一个根本性的能力缺口：**缺乏对人-物体交互的建模能力**。

具体而言，当需要生成主播手持产品（如手机、化妆品）的视频时，现有方法倾向于将物体简单地处理为人体外观的一部分——即一种附着在手上的“静态纹理”，而非一个需要独立建模的、与手部发生动态交互的三维实体。这导致了两个典型失败模式：

1. **物体外观退化**：物体的纹理细节在生成过程中丢失或扭曲，无法保持产品的外观一致性。
2. **交互动作失准**：物体随手的运动呈现不自然的滑动、穿透或静止，缺乏真实的物理交互感（如抓握、旋转、开合）。

如 Fig. 1 所示，现有方法虽然能准确跟随人体姿势，但在手部-物体交互区域表现不佳，常将物体误解为人体的一部分，导致生成的是“静态贴图”而非动态交互。

### 现有方法的技术局限

从技术路线来看，当前主流方法可归为以下几类，但均未有效解决HOI视频生成问题：

- **姿势驱动人体视频生成方法**（如 **MimicMotion**、**StableAnimator**（Tu et al., CVPR 2025））：这些方法以人体骨架或关键点作为运动条件，擅长保持人体外观和动作一致性，但其条件信号中不包含任何物体信息，因此无法建模手部与物体的交互关系。
- **个性化主播生成方法**（如 **Make-Your-Anchor**（Huang et al., CVPR 2024））：虽然面向主播场景，但其关注点在于人物身份的保持和口型同步，同样未显式建模物体交互。
- **HOI图像生成方法**（如 **VirtualModel**（Chen et al., arXiv 2024））：这些方法在单帧图像层面实现了人物与物体的交互合成，但缺乏时序一致性建模能力，无法直接扩展到视频生成。
- **视频手部交互方法**（如 **HOI-Swap**（Xue et al., NeurIPS 2024）、**ReHold**（Fan et al., CVPR 2025））：这些工作聚焦于手部区域的物体替换或交互重建，但通常局限于手部局部区域，无法同时保持全身人物的一致性和自然运动。

### 核心挑战

实现高质量的HOI视频生成面临两个紧密耦合的挑战：

1. **外观解耦与保持**：如何让模型同时理解并保持“人”和“物”两个独立实体的外观，避免两者在生成过程中相互污染？这要求模型能够从多视角感知物体外观，并将其与人体外观在特征空间中有效分离。

2. **精细运动控制**：如何提供足够的运动引导信号，使得手部与物体的相对运动自然、准确？仅靠人体骨架姿势远远不够——手部关键点的稀疏性使得手指级别的精细动作难以约束，而物体在三维空间中的运动轨迹更是完全缺失。

### 本文动机与核心思路

针对上述缺口，**AnchorCrafter** 提出了一种基于扩散模型的人物-物体交互视频生成框架，其核心洞察在于：**将多视角物体外观嵌入与分离的人类/物体交叉注意力相结合，同时利用深度图和带遮挡掩码的3D手部网格提供精准的运动引导，使得扩散模型能够生成物体外观一致且交互动作可控的高质量HOI视频。**

具体而言，AnchorCrafter通过三个关键设计来解决上述挑战：

- **HOI外观感知模块**：利用DINOv2提取多视角物体特征并进行融合，通过人类-物体双适配器（分离的交叉注意力机制）将人体和物体外观解耦注入UNet，避免特征混淆。
- **HOI运动注入模块**：引入物体深度图提供空间轨迹引导，结合含遮挡掩码的3D手部网格精确约束手部姿态，并通过空间相似矩阵实现条件与参考图像的对齐。
- **HOI区域重加权损失**：在训练时对交互区域（手部和物体所在区域）施加更高的损失权重，迫使模型更关注这些关键区域的细节学习。

这种设计使得AnchorCrafter在物体外观保持性上相比现有最优方法提升7.5%，物体定位精度（Obj-IoU）翻倍，在用户研究中所有评价维度均排名第一，综合评分达到4.64/5。



## 核心方法与创新机理

AnchorCrafter 的核心创新在于首次将**人-物体交互（HOI）显式建模**引入姿势驱动的人体视频生成框架，解决了现有方法将物体视为人体静态纹理附庸的根本缺陷。其创新路径可归纳为三个相互协同的**changed slots**：

### 1. 物体外观的显式解耦注入

**Baseline 状态**：现有姿势驱动人体视频生成方法（如 MimicMotion、StableAnimator 等）缺乏对物体的独立外观建模，物体被隐含地编码为人体外观的一部分，导致生成过程中物体纹理失真、外观漂移。

**AnchorCrafter 方案**：提出 **HOI-Appearance Perception** 模块，通过两条技术路线实现物体外观的独立编码与解耦注入：

- **多视角物体特征融合**：利用预训练 DINOv2-large 模型从物体的三个不同视角提取嵌入特征 $E_O$，经自注意力机制和线性投影融合为统一的物体外观表征 $f_O$（见 Fig. 5）。这使模型能够从任意多视角捕捉物体的完整外观信息，而非依赖单一视角的片面特征。

- **人类-物体双适配器**：将扩散 UNet 中的标准交叉注意力层替换为并行的 **Human Cross-Attention** 和 **Object Cross-Attention**，分别计算：

  $$\text{HumanCA} := \text{Softmax}\left(\frac{Q K_H^T}{\sqrt{d}}\right) \cdot V_H$$

  $$\text{ObjectCA} := \text{Softmax}\left(\frac{Q K_O^T}{\sqrt{d}}\right) \cdot V_O$$

  通过分离的 Key-Value 投影，人体特征和物体特征被独立注入去噪过程，从架构层面强制实现外观解耦（见 Sec. 4.2.2）。

**因果机制**：多视角融合提供物体外观的完备表征，双适配器则确保该表征在生成过程中不被人体外观污染——这是物体外观保持性提升 7.5%（Obj-CLIP 达 0.921）的直接原因。

### 2. 精细的交互运动控制

**Baseline 状态**：现有方法仅依赖人体骨架姿势（如 DWPose 提取的关键点）作为运动条件，缺乏对物体运动轨迹和手部精细姿态的引导，导致物体在视频中呈现“粘附在手上”的静态效果。

**AnchorCrafter 方案**：提出 **HOI-Motion Injection** 模块，引入两类额外运动条件：

- **物体深度图轨迹**：通过深度图 $D$ 编码物体在视频序列中的空间位置变化，为物体运动提供明确的轨迹引导。
- **3D 手部网格与遮挡掩码**：引入 3D 手部网格 $H$，包含手部关节的完整三维姿态信息，并附带遮挡掩码指示手部与物体的空间关系。这使模型能够理解手部何时位于物体前方、何时抓握物体侧面等复杂空间关系。

此外，为解决输入姿势序列与参考人体图像之间的空间错位问题，模块从姿势序列的第一帧估计与参考图像姿势的**空间相似矩阵**，并将其应用于所有运动条件（骨架 $P$、手部网格 $H$、深度图 $D$），实现条件与参考图像的空间对齐（见 Sec. 4.4）。

**因果机制**：深度图提供物体“在哪里”，3D 手部网格提供手“怎么动”，空间对齐确保这些条件正确映射到参考人体——三者结合使物体定位精度翻倍（Obj-IoU 达 0.906）。

### 3. 交互区域重加权损失

**Baseline 状态**：标准扩散模型训练使用均匀权重的 $L_{diff}$ 损失，对所有像素一视同仁。

**AnchorCrafter 方案**：观察到标准损失导致模型难以充分学习物体外观细节，提出 **HOI-Region Reweighting Loss**：

$$L_{object} = \eta \frac{S}{S_{obj} + S_{hand}} M_{inter} \odot L_{diff}$$

其中 $M_{inter}$ 为交互区域掩码（覆盖手部和物体像素），$\eta$ 为平衡系数。损失按交互区域面积的反比进行加权——交互区域越小，权重越大，迫使模型聚焦于手部和物体的精细细节。

最终训练损失为交互区域内外损失的加权组合：

$$L_{final} = (1 - M_{inter}) \odot L_{diff} + L_{object}$$

**因果机制**：重加权损失直接回应了交互区域像素占比小但视觉重要性高的矛盾，消融实验证实移除该损失会导致物体细节明显退化（见 Table 1, Fig. 7 “w/o reweight”）。

### 创新协同效应

三个 changed slots 并非孤立运作：外观解耦确保物体“长什么样”不受人体干扰，运动控制决定物体“怎么动”，重加权损失则强制模型在训练中优先学习交互区域的生成质量。消融实验（Table 1, Fig. 7）表明，移除任一模块均导致性能显著下降——多视角融合缺失降低 Obj-CLIP，手部网格缺失增大手部关键点误差（LMD），重加权损失缺失损害交互区域细节。三者的协同构成了 AnchorCrafter 在物体外观保持（+7.5%）和定位精度（翻倍）上超越现有方法的因果基础。



AnchorCrafter 是一个基于扩散模型的视频生成系统，其核心目标是给定一张主播参考图像、一个目标商品的多视角图像以及一系列运动控制条件，生成一段该主播与商品自然交互的高保真带货视频。系统通过两阶段学习范式实现这一目标：**大规模 HOI 视频分布预训练**与**目标商品微调**。

### 两阶段学习范式

第一阶段，模型在多样化的人-物交互视频数据集上进行训练，学习通用的 HOI 视频生成分布。训练时，系统接收主播参考图像 $I_H$、商品三视角图像 $I_O = \{i_O^1, i_O^2, i_O^3\}$，以及多重运动控制条件——包括人体骨架序列 $P$、3D 手部网格序列 $H$ 和物体深度图序列 $D$。这些条件共同描述了交互过程中人体姿态、手部精细动作和物体空间轨迹的完整运动信息。

第二阶段，针对特定商品，系统仅需该商品的一分钟交互视频即可进行微调，使模型适配新商品的外观纹理和交互特性。微调完成后，模型可为任意新主播生成该商品的推广视频，支持未见过的动作序列驱动（见 Figure 3）。

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/003_Figure_3.jpg]]
*Figure 3: Fine-tuning for new products and inference for new anchors. Fine-tuning the model with a one-minute video to achieve a customized model for new objects. After finetuning, our method could generate arbitrary anchor videos selling the product with various unseen motions*

### 核心 Pipeline 架构

训练 pipeline 以视频扩散 UNet 为骨干网络，通过三个关键模块实现人-物交互的精确控制（见 Figure 4）：

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/004_Figure_4.jpg]]
*Figure 4: Training pipeline for AnchorCrafter: Based on a video diffusion model, AnchorCrafter injects human and multiview object references into the video via HOI-appearance perception. The motion is controlled through HOI-motion injection, with the training objective reweighted in the HOI region*

**1. 视频扩散骨干网络**
系统基于潜空间视频扩散模型，将输入视频帧编码至潜空间后进行去噪训练。基础训练目标为标准扩散损失：

$$L_{diff} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,I), Z, c, t} [ \| \epsilon - \epsilon_\theta(Z_t, c, t) \|_2^2 ]$$

其中 $Z_t$ 为加噪潜变量，$c$ 为条件信息，$\epsilon_\theta$ 为去噪网络。

**2. HOI-Appearance Perception（外观感知模块）**
该模块负责将主播和商品的外观信息解耦注入生成过程。首先通过多视角物体特征融合，利用预训练 DINOv2-large 模型分别提取商品三个视角的嵌入特征，经自注意力机制和线性投影融合为统一的物体外观表征 $f_O$。随后，人体-物体双适配器将 UNet 中的标准交叉注意力层替换为两个并行的交叉注意力分支：

$$HumanCA := \text{Softmax}\left(\frac{Q K_H^T}{\sqrt{d}}\right) \cdot V_H$$

$$ObjectCA := \text{Softmax}\left(\frac{Q K_O^T}{\sqrt{d}}\right) \cdot V_O$$

这两个分支分别对人体特征和物体特征进行独立的交叉注意力计算，实现外观表征的解耦，避免物体被错误地融合为人体纹理的一部分。

**3. HOI-Motion Injection（运动注入模块）**
该模块提供精细的运动控制信号。物体深度图 $D$ 描述商品在视频中的空间轨迹，3D 手部网格 $H$ 含遮挡掩码指导手部姿态的精确合成。为解决输入姿态序列与参考人体图像之间的空间不对齐问题，系统从姿态序列首帧估计相似变换矩阵，并将其应用于所有运动条件（$P$、$H$、$D$），确保生成结果与参考图像的空间一致性。

**4. HOI-Region Reweighting Loss（交互区域重加权损失）**
标准扩散损失对画面各区域施加均匀权重，导致模型难以充分学习手部和物体等小区域的交互细节。为此，系统引入交互区域重加权机制：

$$L_{object} = \eta \frac{S}{S_{obj} + S_{hand}} M_{inter} \odot L_{diff}$$

其中 $M_{inter}$ 为交互区域掩码，$S$ 为全图面积，$S_{obj} + S_{hand}$ 为物体与手部区域面积之和，$\eta$ 为平衡系数。最终训练损失为：

$$L_{final} = (1 - M_{inter}) \odot L_{diff} + L_{object}$$

该设计在非交互区域保留标准扩散损失，在交互区域按面积反比增大权重，迫使模型重点关注手部-物体交互的细节生成。

### 输入输出流总结

- **输入**：主播参考图像 $I_H$、商品多视角图像 $I_O$、人体骨架序列 $P$、3D 手部网格序列 $H$、物体深度图序列 $D$
- **外观注入**：多视角 DINOv2 特征融合 → 人体-物体双适配器并行交叉注意力 → UNet 潜空间特征调制
- **运动控制**：深度图 + 3D 手部网格 + 空间相似变换对齐 → 运动条件注入
- **训练优化**：交互区域重加权损失强化手部-物体细节学习
- **输出**：主播与商品自然交互的高保真带货视频

### 补充图表

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/002_Figure_2.jpg]]
*Figure 2: We propose AnchorCrafter, a diffusion-based human video generation framework for creating high-fidelity anchorstyle product promotion videos by animating reference human images with specific products and motion controls. By incorporating human-object interaction into the generation process, AnchorCrafter achieves high preservation of object appearance and enhanced interaction awareness*



AnchorCrafter 的核心架构建立在视频扩散模型之上，围绕三个关键模块解决人-物交互视频生成中的外观解耦与运动控制难题。

### 视频扩散骨干

系统采用标准的视频扩散 UNet 作为生成骨干，在潜空间中进行去噪训练。给定编码后的视频潜变量 $Z$ 和条件信号 $c$，训练目标为最小化噪声预测误差：

$$L_{diff} = \mathbb{E}_{\epsilon \sim \mathcal{N}(0,I), Z, c, t} [ \| \epsilon - \epsilon_\theta(Z_t, c, t) \|_2^2 ]$$

其中 $\epsilon_\theta$ 为 UNet 预测的噪声，$t$ 为扩散时间步。该损失为后续模块的重加权提供了基础。

### HOI外观感知模块

该模块是本方法的核心创新，旨在将物体外观从人体外观中解耦出来，实现独立的物体外观注入。其结构如 Fig. 5 所示，包含两个子组件：

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/005_Figure_5.jpg]]
*Figure 5: HOI-appearance perception: The feature of the target object*

**多视角物体特征融合**：针对单视角无法完整捕捉物体外观的问题，系统从三个不同视角拍摄物体图像 $I_O = \{i_O^1, i_O^2, i_O^3\}$，分别通过预训练的 DINOv2-large 模型提取嵌入 $E_O$。随后，这些嵌入经过两个独立的可学习线性投影层生成 Query 和 Key/Value，通过自注意力机制融合为统一的物体特征 $f_O$。该设计使得模型能够从多视角推断物体的完整三维外观。

**人类-物体双适配器**：传统交叉注意力将人体和物体特征混合注入，导致外观纠缠。AnchorCrafter 将 UNet 各层的交叉注意力替换为两个并行的交叉注意力分支——人体交叉注意力（HumanCA）和物体交叉注意力（ObjectCA），分别处理人体参考特征 $f_H$ 和物体融合特征 $f_O$：

$$HumanCA := \text{Softmax}\left(\frac{Q K_H^T}{\sqrt{d}}\right) \cdot V_H$$

$$ObjectCA := \text{Softmax}\left(\frac{Q K_O^T}{\sqrt{d}}\right) \cdot V_O$$

其中 $Q$ 来自 UNet 中间特征，$K_H, V_H$ 和 $K_O, V_O$ 分别由人体和物体特征投影得到，$d$ 为特征维度。两个注意力输出相加后送入后续层，实现外观的解耦注入。

### HOI运动注入模块

运动控制通过三种条件信号实现：人体骨架序列 $P$、3D手部网格 $H$（含遮挡掩码）和物体深度图 $D$。这些条件通过 ControlNet 类分支注入 UNet，为物体轨迹和手部交互提供精细的空间引导。

一个关键细节是空间对齐：输入姿势序列与参考人体图像之间存在空间差异，直接注入会导致扭曲。系统从姿势序列 $P$ 的第一帧估计到参考图像 $I_H$ 的相似变换矩阵，并将该矩阵应用于所有运动条件（$P, H, D$），确保条件信号与参考人体的空间位置一致。

### HOI区域重加权损失

标准扩散损失对所有像素均匀加权，导致模型无法充分学习手部和物体等小区域的细节。为解决此问题，系统引入了交互区域重加权机制。

首先通过手部关键点和物体掩码生成交互区域掩码 $M_{inter}$，标识手部和物体所在像素。然后对交互区域内的损失按面积反比进行加权：

$$L_{object} = \eta \frac{S}{S_{obj} + S_{hand}} M_{inter} \odot L_{diff}$$

其中 $\eta$ 为平衡超参数，$S$ 为图像总面积，$S_{obj}$ 和 $S_{hand}$ 分别为物体和手部区域面积。最终训练损失将标准损失与重加权损失组合：

$$L_{final} = (1 - M_{inter}) \odot L_{diff} + L_{object}$$

该设计使得模型在训练时对交互区域施加更大的优化力度，从而显著提升物体外观保持和手部交互的生成质量。消融实验证实，移除该损失会导致交互区域物体细节明显退化（见 Table 1 和 Fig. 7 的 "w/o reweight" 行）。



## 实验与关键发现

### 1. 实验设置

#### 1.1 数据集与评估协议

AnchorCrafter采用两阶段训练策略。第一阶段在多样化的HOI视频数据集上进行大规模预训练，使模型学习通用的人-物交互视频分布；第二阶段针对特定新产品，使用约一分钟的交互视频进行微调（Fig. 3）。训练使用7块40GB GPU，第一阶段共迭代12,000次，输入分辨率为512×768，每样本包含10帧。

评估采用自建的HOI测试集，所有对比方法均使用官方实现或论文推荐配置。评估维度覆盖物体定位精度（Obj-IoU）、物体外观保持性（Obj-CLIP）、人脸相似度（Face-Cos）、视频质量（VBench的Subject Consistency、Background Consistency、Motion Smoothness），以及手部关键点误差（LMD）。

#### 1.2 对比方法

选取的基线方法涵盖姿势驱动人体视频生成、人脸动画、个性化主播生成、人物交互图像生成、手部交互物体替换和手部交互视频重建等多个方向：

- **MimicMotion**：姿势驱动人体视频生成基线
- **StableAnimator**（Tu et al., CVPR 2025）：高精度人脸动画方法
- **Make-Your-Anchor**（Huang et al., CVPR 2024）：个性化主播视频生成
- **VirtualModel**（Chen et al., arXiv 2024）：人物交互图像生成
- **HOI-Swap**（Xue et al., NeurIPS 2024）：视频手部交互物体替换
- **ReHold**（Fan et al., CVPR 2025）：手部交互视频重建

### 2. 主要定量结果

**Table 1** 展示了AnchorCrafter与上述基线方法及消融变体的全面定量对比，核心结论如下：

**物体交互能力遥遥领先。** AnchorCrafter在物体定位精度上达到Obj-IoU 0.906，相比最优竞争方法提升约一倍（Abstract宣称“doubles the object localization accuracy”）。物体外观保持性方面，Obj-CLIP达到0.921，较此前最佳水平提升约7.5%。这两个指标直接验证了HOI-Appearance Perception和HOI-Motion Injection两大模块的有效性——多视角物体特征融合与分离交叉注意力确保了物体外观的准确重建，深度图和3D手部网格则提供了精确的空间运动引导。

**人体保持能力与现有SOTA持平。** 在人脸相似度（Face-Cos 0.70）上，AnchorCrafter与UniAnimate-DiT等高性能方法表现相当，证明在引入复杂交互建模的同时并未牺牲人物身份保持。

**视频生成质量处于第一梯队。** VBench的三个核心指标——Subject Consistency（95.43）、Background Consistency（94.96）、Motion Smoothness（98.91）——均达到或接近最优水平，表明生成的带货视频在主体一致性、背景稳定性和运动流畅性方面具有专业级质量。

### 3. 用户研究

**Table 2** 报告了用户主观评价结果。评估者从五个维度（外观质量、运动准确性、交互自然度、物体保真度、整体质量）对生成视频进行1-5分评分。AnchorCrafter在所有五个维度均排名第一，整体质量评分达到4.64/5，显著领先于最优竞争方法（如VirtualModel约3.5分，差距达+1.14）。这一结果与定量指标相互印证，表明本方法不仅在自动评估指标上表现优异，在人类感知层面同样具有压倒性优势。

### 4. 消融实验

**Table 1** 的消融部分和 **Fig. 7** 的定性对比系统验证了各核心模块的贡献：

**多视角物体特征融合至关重要。** 移除多视角自注意力、仅使用单视角特征（w/o multi-view）时，Obj-CLIP分数明显下降。Fig. 7显示此时物体纹理细节丢失严重，证实多视角融合对物体外观重建的关键作用。

**3D手部网格注入显著提升手部精度。** 移除3D手部网格条件（w/o hand mesh）导致手部关键点误差（LMD）增大，Fig. 7中手部姿态出现明显畸变。这验证了带遮挡掩码的3D手部网格对精确手部合成的贡献。

**HOI区域重加权损失强化交互细节。** 去掉重加权损失（w/o reweight）后，交互区域的物体细节变差，手部与物体的接触边界模糊。该消融证实了公式（4-5）中按面积反比加权策略的有效性——通过加大对小面积交互区域的训练权重，迫使模型更精细地学习手-物交互模式。

**微调阶段是学习精细纹理的关键。** **Fig. 8** 的微调消融显示，经过一分钟视频微调后，模型能准确学习物体的纹理细节（如产品Logo、材质反光），Obj-CLIP分数显著提升。这解释了为何两阶段策略对于产品定制化场景不可或缺。

### 5. 定性分析与能力边界

**Fig. 6** 的定性对比直观展示了AnchorCrafter的核心优势：其他方法要么将物体处理为附着在人体上的静态纹理（如MimicMotion），要么无法保持物体外观一致性（如HOI-Swap），而AnchorCrafter生成的视频中物体随人手自然运动，外观始终保持清晰可辨。

**Fig. 9** 展示了模型对复杂交互动作的适应能力——成功生成“打开耳机盒”这类需要精细手部操作的动作序列，证明深度图轨迹和3D手部网格的组合运动控制具有足够的表达力。

**Fig. 10** 验证了模型对相似形状物体的泛化能力：使用一部手机的交互视频驱动另一部不同型号手机的外观生成，仍能保持合理的交互效果。

### 6. 失败模式与局限性

**Fig. 11** 和论文明确指出了以下失败模式：

- **透明物体处理困难。** 对玻璃制品等透明物体，模型容易出现镜像穿透、折射错误或外观丢失，这是因为深度估计和外观特征提取对透明表面缺乏有效表征。
- **错误条件导致干扰。** 当输入的手部姿态估计（如DWPose）出现左右手误标等错误时，模型会生成错误的手-物交互结果，表明方法对条件信号的准确性有较高依赖。
- **非刚性物体泛化有限。** 当前设计主要面向刚性物体（手机、化妆品等），对布料、食品等可变形物体的交互生成能力尚未验证。
- **微调成本。** 虽然仅需一分钟视频，但对每个新产品进行微调仍增加了部署流程的复杂度，限制了即时批量应用。

### 7. 公平性说明

需注意，AnchorCrafter在训练阶段额外收集了每人一分钟的交互视频用于微调，相比无需微调的基线方法（如MimicMotion、StableAnimator）具有数据资源优势。论文认为该成本在直播带货等应用场景中可接受，但在严格公平对比中应予以考虑。

### 补充图表

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/007_Table_1.jpg]]
*Table 1: The quantitative results of our method were compared with those of SOTAs and ablation studies. Our method significantly outperforms existing approaches regarding numerical performance for spatial movement and appearance preservation of objects while also matching or exceeding current methods in image and video quality and human pose control capability. Subject consistency (Subj-Cons) and background consistency (Back-Cons) are percentages*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/011_Table_2.jpg]]
*Table 2: User study scores. The rating score is on a scale from one to five, where five is the highest score and one is the lowest*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/008_Figure_7.jpg]]
*Figure 7: Ablation studies. Our modules improve the preservation of the object and its interactions with the hands. The error section has been enlarged in the lower right corner*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/009_Figure_8.jpg]]
*Figure 8: Ablation study of fine-tuning. After fine-tuning, the model can learn the texture details of objects*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/001_Figure_1.jpg]]
*Figure 1: Existing methods accurately follow human poses but struggle with realistic hand-object interactions, often misinterpreting the object as part of the human, leading to static animations. In contrast, our approach ensures natural and dynamic movement by precisely synthesizing humanobject interactions while preserving object appearance*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/014_Figure_9.jpg]]
*Figure 9: Anchorcrafter is able to perform the action of ”opening the headphone case”, demonstrating the adaptability and interactive ability of our model in complex scenarios*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/012_Figure_10.jpg]]
*Figure 10: Generalization over similar object shapes. Driving iPhone interaction videos with another mobile phone*

![[assets/figures/papers/paper_list_l1912_AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object/figures/013_Figure_11.jpg]]
*Figure 11: Limitations. Handling transparent objects remains challenging, and erroneous conditions introduce interference*



## 定位与知识库关联

### 1. 任务定位与核心瓶颈

AnchorCrafter 瞄准的是**人物交互（Human-Object Interaction, HOI）视频生成**这一新兴任务，其应用场景为虚拟主播产品带货视频的自动生成。该任务处于人体视频生成、物体外观保持和交互动作控制三者的交叉点。

现有姿势引导的人体视频生成方法（如 **MimicMotion**、**StableAnimator** (Tu et al., CVPR 2025)）虽然能够准确跟随人体骨架姿势，但其核心瓶颈在于**缺乏对人-物体交互的建模能力**：物体被隐式地处理为人体纹理的一部分，无法产生自然的动态交互，导致生成结果中物体呈现为静态贴图。这一根本缺陷使得现有方法无法直接应用于带货视频等需要精细手部-物体协同运动的场景。

### 2. 与现有工作的关系

#### 2.1 姿势驱动人体视频生成

AnchorCrafter 继承了扩散模型驱动的人体视频生成范式，与 **MimicMotion**、**StableAnimator** (Tu et al., CVPR 2025) 等方法共享基于骨架姿势的运动控制思路。然而，这些基线方法仅关注人体自身的运动保真度，AnchorCrafter 在此基础上**引入了物体运动控制维度**，通过深度图提供物体轨迹、通过3D手部网格指导手部精细运动，将控制空间从单一人体扩展到人-物联合空间。

#### 2.2 个性化主播视频生成

**Make-Your-Anchor** (Huang et al., CVPR 2024) 是直接面向主播视频生成的同领域方法，但其设计目标为个性化主播外观保持，并未显式建模手持物体的外观与运动。AnchorCrafter 在该工作的基础上增加了完整的HOI生成能力，可视为对主播视频生成任务的实质性功能扩展。

#### 2.3 人物交互图像/视频生成

在人物交互生成领域，**VirtualModel** (Chen et al., arXiv 2024) 面向图像层面的HOI生成，**HOI-Swap** (Xue et al., NeurIPS 2024) 专注于视频中手部交互物体的替换，**ReHold** (Fan et al., CVPR 2025) 则针对手部交互视频的重建。AnchorCrafter 与这些工作的关键区别在于：

- **生成范式不同**：AnchorCrafter 是从参考图像直接生成完整交互视频，而非替换或重建已有视频中的物体；
- **外观建模更精细**：通过多视角DINOv2特征融合和人类-物体双适配器实现外观解耦注入，这是上述方法未采用的技术路线；
- **控制条件更丰富**：同时使用深度图和3D手部网格（含遮挡掩码）作为运动条件，提供了比单一条件更精准的交互控制。

#### 2.4 定量关系

在定量对比中（Table 1），AnchorCrafter 在物体定位精度（Obj-IoU 达到 0.906）和物体外观保持（Obj-CLIP 达到 0.921）上显著超越所有对比方法，其中物体外观保持相比现有最佳方法提升约7.5%，物体定位精度约为对比方法的两倍。在人脸保持（Face-Cos 0.70）和视频质量指标（VBench）上，AnchorCrafter 与当前最优方法（如 UniAnimate-DiT）持平或略优。

### 3. 技术贡献的知识增量

AnchorCrafter 的核心知识贡献体现在三个技术槽位的改变：

| 技术槽位 | 基线方案 | AnchorCrafter方案 | 知识增量 |
|---------|---------|-----------------|---------|
| 物体外观注入 | 无显式物体建模，物体作为人体纹理 | 多视角DINOv2特征融合 + 人类-物体双适配器（分离交叉注意力） | 首次在视频扩散模型中实现人-物外观的解耦注入 |
| 交互运动控制 | 仅依赖人体骨架姿势 | 深度图（物体轨迹）+ 3D手部网格（含遮挡掩码）+ 空间相似矩阵对齐 | 将运动控制从单一人体扩展到人-物联合空间 |
| 训练损失函数 | 标准扩散损失（均匀权重） | HOI区域重加权损失，按交互区域面积反比加权 | 引入空间自适应的损失重加权机制，强化小区域细节学习 |

消融实验（Table 1, Fig. 7）证实了每个模块的独立贡献：移除多视角自注意力导致物体CLIP分数下降；移除3D手部网格注入使手部关键点误差增大；去掉HOI区域重加权损失使交互区域物体细节变差。微调阶段被证明是学习精细物体纹理的关键步骤（Fig. 8）。

### 4. 适用边界与局限

#### 4.1 适用场景

AnchorCrafter 适用于以下条件：
- **物体类型**：刚性物体（如手机、耳机盒、化妆品包装等），具有相对固定的几何形状；
- **交互类型**：手持物体的展示、操作等动作，手部与物体有明确的空间关系；
- **数据条件**：每个新产品需要约一分钟的交互视频用于微调，可接受该部署成本。

#### 4.2 已知局限

1. **透明物体处理困难**（Fig. 11）：对玻璃制品等透明物体，模型容易出现镜像穿透或外观丢失，这源于扩散模型对透明材质的光学特性建模不足；
2. **条件敏感性**：对错误的手部姿态条件（如DWPose误标左右手）敏感，会导致错误的生成结果，表明模型对条件信号的鲁棒性有待提升；
3. **非刚性物体泛化有限**：当前方法主要面向刚性物体，对衣物、食品等可变形物体的交互生成可能泛化能力不足；
4. **微调成本**：虽然仅需一分钟视频，但对每个新产品进行微调增加了部署成本，限制了大规模SKU场景下的应用效率。

### 5. 开放问题

1. **材质泛化**：如何将方法扩展到透明物体和非刚性物体的交互生成？可能需要引入材质先验或物理模拟约束；
2. **条件鲁棒性**：能否通过更鲁棒的姿态估计模型（如升级版DWPose或融合多模态信号）减轻条件错误带来的影响？
3. **少样本/零样本定制**：是否可以进一步减少微调所需数据，甚至通过物体类别先验实现零样本或少量样本的产品定制？
4. **多主体扩展**：在多主体交互或多人协作场景下（如两人共同展示产品），方法应如何扩展控制条件和解耦机制？
5. **实时性优化**：当前基于扩散模型的生成范式在推理速度上可能难以满足实时直播需求，模型蒸馏或高效采样策略是潜在方向。



## 原文 PDF

![[paperPDFs/IEEE_TRANSACTIONS_ON_VISUALIZATION_AND_COMPUTER_GRAPHICS_2026/AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object_Interacting_Video_Generation.pdf]]

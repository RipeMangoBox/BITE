---
title: Visual Persona Foundation Model for Full Body Human Customization
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization.pdf
project_link: https://cvlab-kaist.github.io/Visual-Persona
code_link: https://github.com/
aliases:
- VP
- VPFMFBHC
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过身体部位分解和基于Transformer的编码器-解码器架构，将局部外观信息编码为密集的身份嵌入，并引入大规模配对数据集（Visual Persona-500K）进行跨图像训练。
primary_logic: 将人体分解为多个独立区域并分别提取局部特征，能够更精细地保留全身外观细节，避免传统全局特征融合造成的信息丢失；同时，利用视觉语言模型自动构建的配对数据集有效缓解了对身份无关属性（如背景、姿态）的过拟合。
claims:
- Visual Persona 在 PPR10K 上的身份保持指标 D-I 达到 7.30，远高于 StoryMaker 的 6.80，并在 D-H 上以 6.85 对 6.63 领先。
- 相比 StoryMaker，Visual Persona 能够实现大幅度的姿态和表情变化，同时保持服装细节，生成更逼真的纹理。
- 消融实验表明，身体部位分解使 D-H 从 6.40 提升至 6.85，且增加身份嵌入 token 长度从 4x4 到 16x16 显著提高了身份保持。
- SSHQ 上 D-H (Harmonic Mean of D-I and D-T) = 6.99
---

# Visual Persona Foundation Model for Full Body Human Customization

> [!tip] 核心洞察
> 将人体分解为多个独立区域并分别提取局部特征，能够更精细地保留全身外观细节，避免传统全局特征融合造成的信息丢失；同时，利用视觉语言模型自动构建的配对数据集有效缓解了对身份无关属性（如背景、姿态）的过拟合。

| 字段 | 内容 |
|------|------|
| 中文题名 | Visual Persona：面向全身人体定制的基础模型 |
| 英文题名 | Visual Persona Foundation Model for Full Body Human Customization |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://cvlab-kaist.github.io/Visual-Persona) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Visual Persona |
| Dataset | SSHQ, PPR10K |

> [!tip] 效果简介
> - SSHQ 上，D-H (Harmonic Mean of D-I and D-T) 6.99 vs 6.71 (StoryMaker) (+0.28)。
> - PPR10K 上，D-H 6.85 vs 6.63 (StoryMaker) (+0.22)。

## 概要

**核心问题与瓶颈**：现有的人体定制方法（如 IP-Adapter-FaceID、InstantID、PhotoMaker）主要聚焦于面部区域的身份保持，难以在全身尺度上同时实现外观一致性与文本对齐。根本瓶颈在于：缺乏大规模、多图像的配对全身体数据集，导致模型在单图像重建训练中容易过拟合姿态、背景等身份无关属性；同时，全局特征编码方式会丢失服装纹理、体型等局部细节。

**核心洞察与方法定位**：Visual Persona 提出将人体**分解为多个独立部位图像**（全身、面部、躯干、腿、鞋），通过 DINOv2 提取保留空间信息的局部特征，再由 Body-Partitioned Transformer Decoder 将其投影为密集的身份嵌入（可达 16×16 tokens），注入冻结的 SDXL 扩散模型。这一“分解-独立编码-密集注入”的设计，使模型能够精细保留全身外观细节，避免全局特征融合的信息损失。为支撑跨图像训练，论文利用视觉语言模型（LLaVA）自动构建了 **Visual Persona-500K** 数据集（580K 图像，100K 身份），通过面部一致性筛选与服装一致性验证，确保同一身份的多张图像具有稳定的全身外观。

**方法谱系与知识库定位**：在身份定制方法谱系中，Visual Persona 处于“全身人体定制”这一新兴节点，区别于仅处理面部的 **IP-Adapter-FaceID**、**InstantID**、**PhotoMaker**，也超越了直接处理全图的通用图像定制方法 **IP-Adapter** 和早期全身方法 **StoryMaker**。其关键创新在于：（1）将身体部位分解引入扩散模型的条件注入流程；（2）用 Transformer 解码器替代简单的线性投影，实现从局部特征到密集身份嵌入的映射；（3）利用 VLM 自动化构建大规模配对数据集，将训练范式从单图像重建转变为跨图像身份保持。

**主要结果**：在 PPR10K 基准上，Visual Persona 的身份保持指标 D-I 达到 7.30（StoryMaker 为 6.80），综合指标 D-H 以 6.85 对 6.63 领先 StoryMaker（Table 2）。定性对比（Figure 5、Figure 7）显示，该方法能在大幅度姿态和表情变化下保持服装细节，生成更逼真的纹理。消融实验证实，身体部位分解使 D-H 从 6.40 提升至 6.85（Table 4），将身份嵌入 token 长度从 4×4 增加到 16×16 进一步显著提升了身份保持（Table 5）。

**局限与开放问题**：方法仍受 SDXL 固有缺陷影响，可能产生不准确的身体比例（如手指融合、多余肢体），目前通过负向提示部分缓解。身份无关属性泄漏（如输入图像中被遮挡的背景元素被错误保留）是另一已知局限，论文计划通过前景分割模型改进。开放问题包括：如何彻底消除属性泄漏而不依赖手动掩码？负向提示策略能否自动化？该方法在极端遮挡或多人交互场景下的鲁棒性尚待验证。

### 研究问题与核心瓶颈

文本到图像生成模型的最新进展使得高质量图像合成成为可能，但在**全身人体定制**（Full-Body Human Customization）这一任务上仍面临根本性挑战。该任务要求模型在给定单张人物图像后，能够生成该人物在不同姿态、场景和风格下的多样化图像，同时精确保留其全身外观细节（包括面部特征、服装纹理、体型比例等）。

现有工作的核心瓶颈体现在两个层面：

1. **身份保持范围的局限**：主流的人体定制方法（如 **IP-Adapter-FaceID**、**InstantID**、**PhotoMaker**）将关注点集中于面部区域的身份保持，依赖人脸识别模型提取全局语义特征。当任务扩展到全身外观时，这类方法无法有效捕捉服装细节、体型特征和身体各部位的纹理信息，导致生成结果在面部以下区域出现身份漂移。

2. **数据与训练策略的根本缺陷**：此前的方法（包括 **IP-Adapter** 和 **StoryMaker** 等通用图像定制方法）普遍采用**重建训练**策略——即输入图像与目标输出为同一张图像。这种训练方式使得模型极易过拟合于身份无关属性，如背景、光照条件、姿态和构图方式，从而在推理时难以泛化到新的文本描述和场景。此外，缺乏大规模、高质量的多图像配对数据集进一步加剧了这一困境：现有数据集要么仅覆盖面部领域，要么每个身份仅包含单张图像，无法为跨图像训练提供监督信号。

### 关键洞察与动机

Visual Persona 的核心洞察在于：**将人体分解为多个独立区域并分别提取局部特征，能够更精细地保留全身外观细节，避免传统全局特征融合造成的信息丢失**。这一设计源于以下观察：

- 人体的外观信息是高度结构化的——面部、躯干、腿部和鞋履各自承载着独特的身份线索，而直接对整张图像进行全局编码会将这些线索混合在一起，导致细粒度信息的损失。
- 通过身体部位分解（Body Part Decomposition），模型可以独立关注每个区域的局部特征，从而在生成过程中更精确地复现服装纹理、体型比例和配饰细节。

同时，该方法认识到**训练数据的质量决定了身份保持的上限**。为此，Visual Persona 引入了一条基于视觉语言模型（VLM）的数据筛选管线，自动构建了一个包含 580K 张图像、覆盖 100K 个不同身份的大规模配对数据集 **Visual Persona-500K**。这一数据集使得**跨图像训练**成为可能——输入与输出为同一人物的不同图像，迫使模型学习身份本质特征而非身份无关属性，从而在根本上缓解了过拟合问题。

### 方法定位

Visual Persona 在方法谱系中处于**身份定制扩散模型**与**细粒度视觉特征编码**的交汇点。与仅关注面部身份的方法（如 IP-Adapter-FaceID、InstantID）相比，它将定制范围扩展至全身；与 StoryMaker 等已有的全身定制方法相比，它通过身体部位分解和跨图像训练策略，显著提升了对服装细节和纹理的保持能力，同时降低了对姿态、表情等身份无关属性的过拟合风险。在知识库定位上，该方法的核心贡献在于证明了**密集的局部身份嵌入**（通过 16×16 的 token 长度实现）和**解耦的交叉注意力注入**是全身人体定制的有效范式。

## 核心方法与创新机理

### 瓶颈与因果转向

现有的人体定制方法（如 **IP-Adapter**、**PhotoMaker**、**StoryMaker**）的核心瓶颈在于：它们或局限于面部区域，或在处理全身时因缺乏大规模配对全身体数据集而难以在保持外观一致性的同时实现文本对齐。其根本原因在于，这些方法通常使用 CLIP 或人脸识别模型提取全局语义特征，并通过少量 token（通常 4–16 个）注入扩散模型，导致细粒度的服装纹理、身体比例等局部信息在特征压缩过程中严重丢失。同时，它们普遍采用“单图重建训练”（即输入与输出为同一张图像），使模型易过拟合于姿态、背景等身份无关属性，削弱了跨姿态、跨场景的泛化能力。

Visual Persona 的因果转向体现在三个相互耦合的 **changed slots** 上：

1. **从全局特征到身体部位分解的局部特征**：将人体分解为全身、面部、躯干、腿、鞋五个独立区域，利用现成的身体解析方法生成部位图像，再通过 DINOv2 提取保留空间信息的局部视觉特征。这从根本上改变了信息编码的粒度，使模型能独立保留每个部位的细节，而非在全局池化中混合丢失。

2. **从少量 token 到密集身份嵌入的投影机制**：引入 Body-Partitioned Transformer Decoder，通过交叉注意力将各部位特征分别投影为可学习的身份嵌入，再经自注意力和 MLP 精炼后拼接为密集条件向量。Token 长度从常规的 4×4 扩展至 16×16，为每个部位提供了充足的表征容量。

3. **从单图重建到跨图像配对的训练策略**：构建 Visual Persona-500K 数据集（580k 图像，100k 身份），利用视觉语言模型（LLAVA ）自动筛选同一人物穿着相同服装的不同图像作为训练对。这使得模型学会将“身份外观”与“姿态、背景”解耦，而非简单复制输入图像。

### 机制与证据链

上述三个 changed slots 之间形成了因果依赖：**部位分解**提供了精细的局部特征源，**密集嵌入**确保了这些特征不被压缩损失，**跨图像训练**则迫使模型仅从这些嵌入中重建身份，从而阻断了对身份无关属性的捷径学习。

消融实验（Table 4）直接验证了这一依赖链：若移除部位分解，仅使用 Transformer 编码器处理全图，D-H 从 6.85 降至 6.40；若进一步将身份嵌入 token 长度从 16×16 缩减至 4×4，D-H 更骤降至 5.81（Table 5）。这表明部位分解与密集嵌入各自独立贡献，且存在叠加效应。

跨图像训练的因果效应体现在定性结果中（Figure 7）：基于单图重建训练的 StoryMaker 在要求大幅姿态变化时，倾向于保留输入图像的原始姿态和表情，而 Visual Persona 能生成与文本描述对齐的新姿态，同时保持服装细节不变。

### 与 baseline 的本质差异

相较于最接近的全身定制方法 **StoryMaker**，Visual Persona 的差异并非简单的性能提升，而是架构范式的根本不同：

- **StoryMaker** 将人脸和身体粗略分割后分别编码，但其特征融合仍依赖全局注意力，且训练数据缺乏系统的跨图像配对，导致在 PPR10K 上 D-I 仅为 6.80，D-H 为 6.63。
- **Visual Persona** 通过五部位独立编码与分区 Transformer 解码，将 D-I 提升至 7.30，D-H 提升至 6.85（Table 2）。更关键的是，在需要同时保持面部身份和服装纹理的场景中（如虚拟试穿），Visual Persona 生成的纹理逼真度显著优于 StoryMaker（Figure 5）。

### 局限与开放问题

尽管架构创新有效，该方法仍存在两个由基础模型继承的局限：（1）依赖 SDXL 导致生成人体可能出现手指融合、多余肢体等解剖伪影，目前仅通过负向提示缓解；（2）身份无关属性泄漏（如输入图像中被遮挡的背景元素被错误保留）尚未根本解决，论文提出通过改进前景分割模型来应对，但这一方向仍需验证。

开放问题包括：能否将部位分解策略推广至多人交互场景而不依赖专门的多人类数据集？负向提示策略能否自动化或内化到模型训练中？这些问题指向了该框架从“单人定制”向“场景级人体生成”扩展的可能性。

Visual Persona 的整体流水线围绕一个核心洞察构建：**将人体分解为多个独立区域并分别提取局部特征，能够更精细地保留全身外观细节，避免传统全局特征融合造成的信息丢失**。其架构将这一思想系统化为四个紧密衔接的模块，形成从输入图像到定制化输出的端到端流程。

### 输入与身体部位分解

给定一张单人图像，流水线的第一步是**身体部位分解**（Body Part Decomposition）。利用现成的身体解析方法，输入图像被增强为五个独立的部位图像：全身、面部、躯干、腿和鞋（Figure 4）。这一分解策略的动机在于，人体的不同部位（如面部纹理、服装褶皱、鞋履样式）具有高度异质的外观特征，若混为一团进行全局编码，细粒度信息极易在压缩过程中丢失。消融实验证实，仅使用 Transformer 而不进行部位分解时，身份保持与文本对齐的调和均值 D-H 仅为 6.40，而引入部位分解后提升至 6.85（Table 4），验证了该设计的有效性。

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/005_Figure_4.jpg]]
*Figure 4: Body Part Decomposition*

### 特征编码：DINOv2 图像编码器

每个部位图像随后被送入一个冻结的 **DINOv2 图像编码器** 提取局部视觉特征。与基线方法常用的 CLIP 或人脸识别模型不同，DINOv2 以 patch 级别保留空间信息，能够捕捉服装纹理、身体轮廓等精细外观线索。这一选择构成了方法谱系中的第一个关键变化槽位：将语义级全局特征替换为空间敏感的局部特征表示。

### 身份嵌入生成：身体分区 Transformer 解码器

这是整个架构的核心创新——**身体分区 Transformer 解码器**（Body-Partitioned Transformer Decoder）。该模块将各部位特征通过一个可学习的查询嵌入集投影为密集的身份嵌入，具体流程如下：

1. **交叉注意力**将每个部位的隐藏嵌入与对应部位图像特征关联，更新表示：
   $$H_{ca}^{i,j} = \mathsf{C\text{-}Att}(\mathrm{LN}(H^{i,j}), F^{i}, F^{i}) + H^{i,j}$$

2. **自注意力**学习嵌入内部的相互关系：
   $$H_{sa}^{i,j} = \mathbb{S}\text{-}\mathsf{Att}\big(\mathrm{LN}(H_{ca}^{i,j}), \mathrm{LN}(H_{ca}^{i,j}), \mathrm{LN}(H_{ca}^{i,j})\big) + H_{ca}^{i,j}$$

3. **MLP** 进一步精炼表示：
   $$H^{i,j+1} = \mathsf{MLP}(\mathrm{LN}(H_{sa}^{i,j})) + H_{sa}^{i,j}$$

经过 $M$ 次迭代后，所有部位的细化嵌入沿 token 长度维度拼接，形成最终的身份条件向量：
$$C_H^* = \mathsf{Concat}([C_H^1, \ldots, C_H^N]) \in \mathbb{R}^{(N \times l_H) \times d_H}$$

这一设计相较于基线方法（通常仅投影 4–16 个全局 token）有两个关键优势：其一，**分区处理**使每个部位的特征不被其他区域稀释；其二，**密集嵌入**（token 长度可达 $16 \times 16$）保留了更丰富的局部信息。消融实验显示，将 token 长度从 $4 \times 4$ 增加到 $16 \times 16$，D-H 从 5.81 跃升至 6.85（Table 5），印证了密集表示的重要性。

### 条件注入与扩散合成

身份嵌入 $C_H^*$ 与来自详细文本描述的文本嵌入 $C_T$ 共同条件化一个**冻结的 SDXL 扩散模型**。身份信息通过一个独立的**解耦交叉注意力层**（Decoupled Cross-Attention）注入，与文本交叉注意力并行，从而避免身份条件与文本条件相互干扰。训练时，仅优化身体分区 Transformer 解码器和身份交叉注意力模块，扩散模型本身保持冻结。

训练目标为标准扩散噪声预测损失：
$$L := \mathbb{E}_{z_{Y,t}, \epsilon, t, C_T, C_H^*} \left[ \left| \left| \epsilon - \epsilon_\theta (z_{Y,t}, t, C_T, C_H^*) \right| \right|_2^2 \right]$$

### 训练策略的关键转变

与基线方法（如 IP-Adapter、StoryMaker）采用“同一图像重建”训练不同，Visual Persona 采用**跨图像训练**策略。输入图像 $X$ 和目标图像 $Y$ 来自同一人的不同照片，这迫使模型学习身份本质特征，而非过拟合背景、姿态、光照等身份无关属性（Table 3(a), Figure 7）。这一策略的可行性依赖于其自建的大规模配对数据集 **Visual Persona-500K**，该数据集包含 100K 个身份的 580K 张图像，通过人脸识别模型和视觉语言模型（LLAVA ）自动筛选全身外观一致的图像对（Figure 2, Table 1），为跨图像训练提供了数据基础。

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/002_Table_1.jpg]]
*Table 1: Comparison of datasets in state-of-the-art customized models. This table outlines the data type, database, data size, image resolution, and data domain used for each method. Unlike existing works that focus on the face domain or use a single image per individual, our approach aims to explore large-scale, real paired human data with full-body appearance consistency*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/003_Figure_2.jpg]]
*Figure 2: Data Statistics: Our curated training dataset, Visual Persona-500K, consists of 580k images representing 100k individuals. (a) illustrates the distribution of the number of images per individual, with over 50% of individuals having more than four images, and shows example image-caption pairs from the same individual. (b) highlights the diversity of individuals based on facial attributes, including race, age, and gender, which are estimated by DeepFace [73]. (c) showcases body structure diversity, segmented into five clusters—full-body, face, torso, legs, and shoes—categorized using a body-parsing method [46]*

### 整体数据流总结

输入单人图像 → 身体部位分解（5 个部位图像）→ DINOv2 编码（局部特征）→ 身体分区 Transformer 解码器（分区交叉注意力 + 自注意力 + MLP，迭代精炼）→ 拼接为密集身份嵌入 → 与文本嵌入共同注入冻结 SDXL → 输出定制化图像。整个流程中，仅解码器和身份交叉注意力模块可训练，扩散模型与图像编码器均保持冻结，在参数效率与生成质量之间取得了平衡。

Visual Persona 的核心架构由四个关键模块串联构成：**身体部位分解**、**DINOv2 图像编码器**、**身体分区 Transformer 解码器**以及**解耦身份交叉注意力**。整个流程将单张人体图像转化为密集的身份嵌入，再注入冻结的 SDXL 扩散模型以合成新图像。

### 身体部位分解（Body Part Decomposition）

利用现成的身体解析方法 将输入人体图像拆分为五个独立的部位图像：全身、面部、躯干、腿和鞋（Figure 4）。这一分解策略的动机在于：直接对全图提取全局特征会丢失各部位的局部细节（如服装纹理、鞋款），而分别编码每个区域能让模型更精细地保留全身外观信息。消融实验证实，仅使用 Transformer 而不做部位分解时，D-H 仅为 6.40；加入部位分解后 D-H 提升至 6.85（Table 4）。

### DINOv2 图像编码器

每个部位图像被送入冻结的 **DINOv2** 编码器，提取保留空间结构的局部视觉特征 $F^i$。与 CLIP 或人脸识别模型提取的全局语义特征不同，DINOv2 的 patch-level 特征能捕获服装褶皱、面料纹理等细粒度外观线索，为后续的身份嵌入学习提供更丰富的底层信息。

### 身体分区 Transformer 解码器（Body-Partitioned Transformer Decoder）

这是模型的核心创新模块。对于每个身体部位 $i$，一组可学习的身份嵌入查询 $H^{i,0}$ 通过 $M$ 层迭代精炼，每层包含三个子步骤：

**交叉注意力**将查询与对应部位特征关联：

$$H_{ca}^{i,j} = \mathsf{C\text{-}Att}\big(\mathrm{LN}(H^{i,j}),\, F^{i},\, F^{i}\big) + H^{i,j} \tag{Eq.1}$$

**自注意力**学习嵌入内部的相互关系：

$$H_{sa}^{i,j} = \mathsf{S\text{-}Att}\big(\mathrm{LN}(H_{ca}^{i,j}),\, \mathrm{LN}(H_{ca}^{i,j}),\, \mathrm{LN}(H_{ca}^{i,j})\big) + H_{ca}^{i,j} \tag{Eq.2}$$

**MLP** 进一步非线性变换：

$$H^{i,j+1} = \mathsf{MLP}\big(\mathrm{LN}(H_{sa}^{i,j})\big) + H_{sa}^{i,j} \tag{Eq.3}$$

经过 $M$ 层后，每个部位得到精炼的身份嵌入 $C_H^i = H^{i,M}$。所有部位的嵌入沿 token 长度维度拼接为**堆叠身份嵌入**：

$$C_H^* = \mathsf{Concat}\big([C_H^1, \ldots, C_H^N]\big) \in \mathbb{R}^{(N \times l_H) \times d_H} \tag{Eq.4}$$

其中 $N=5$ 为部位数量，$l_H$ 为每部位的 token 长度，$d_H$ 为嵌入维度。消融实验表明，将 $l_H$ 从 $4 \times 4$ 增加到 $16 \times 16$ 能显著提升身份保持能力，D-H 从 5.81 跃升至 6.85（Table 5），验证了密集嵌入对保留全身细节的必要性。

### 解耦身份交叉注意力（Decoupled Cross-Attention）

堆叠身份嵌入 $C_H^*$ 通过新增的交叉注意力层注入 SDXL 的 UNet，与原有的文本交叉注意力并行但解耦。具体而言，身份交叉注意力与文本交叉注意力分别作用于不同的层，避免身份信息与文本语义相互干扰。这种解耦设计使得模型能独立控制“谁”和“做什么”。

### 训练目标

仅训练身体分区 Transformer 解码器和身份交叉注意力模块，其余组件（DINOv2、SDXL UNet、文本编码器）均冻结。训练采用标准的扩散噪声预测损失，在 Visual Persona-500K 数据集上进行跨图像训练（输入 $X$ 与目标 $Y$ 为同一人的不同图像）：

$$L := \mathbb{E}_{z_{Y,t},\, \epsilon,\, t,\, C_T,\, C_H^*}\left[ \big|\big| \epsilon - \epsilon_\theta(z_{Y,t},\, t,\, C_T,\, C_H^*) \big|\big|_2^2 \right] \tag{Eq.6}$$

其中 $z_{Y,t}$ 为目标图像在时间步 $t$ 的加噪潜变量，$\epsilon$ 为添加的噪声，$C_T$ 为文本嵌入，$C_H^*$ 为堆叠身份嵌入。跨图像训练策略迫使模型学习身份本质特征而非身份无关属性（如姿态、背景），这是 Visual Persona 相较于以往重建式训练方法的关键优势（Table 3, Figure 7）。


## 实验与关键发现

### 核心定量结果

Visual Persona 在两个公开基准数据集上均取得了最优的身份保持与文本对齐综合性能。表 2 报告了基于 GPT 的评估指标 D-I（身份保持）、D-T（文本对齐）及其调和平均 D-H。在 SSHQ 数据集上，Visual Persona 的 D-H 达到 6.99，领先第二名 StoryMaker 0.28 分；在更具挑战性的 PPR10K 数据集上，D-H 为 6.85，较 StoryMaker 的 6.63 提升 0.22 分。值得注意的是，PPR10K 上的身份保持指标 D-I 达到 7.30，远高于 StoryMaker 的 6.80，表明该方法在复杂场景下对全身外观细节的保持能力显著优于现有方法。

| 数据集 | 指标 | Visual Persona | StoryMaker | 提升 |
|--------|------|---------------|-----------------|------|
| SSHQ   | D-H  | 6.99          | 6.71            | +0.28 |
| PPR10K | D-H  | 6.85          | 6.63            | +0.22 |
| PPR10K | D-I  | 7.30          | 6.80            | +0.50 |

### 定性对比分析

图 5 的定性对比揭示了 Visual Persona 相对于基线方法的关键优势。先前工作如 IP-Adapter 和 InstantID 主要关注面部身份保持，在全身外观（如服装纹理、体型比例）上出现明显失真；StoryMaker 虽面向全身定制，但在大幅姿态变化时仍存在细节丢失和过拟合问题。相比之下，Visual Persona 能够准确保持输入人物的服装细节（如衣领纹理、鞋子颜色），同时生成与文本描述高度一致的新姿态和新场景。

图 7 进一步对比了 StoryMaker 与 Visual Persona 在极端变形场景下的表现。StoryMaker 生成的图像存在面部模糊、服装纹理扭曲等问题，而 Visual Persona 在保持身份特征的同时实现了大幅度姿态和表情变化，生成的纹理更加逼真。这归因于身体部位分解策略和跨图像训练方案，有效解耦了身份特征与姿态、背景等无关属性。

### 消融实验

#### 组件分析

表 4 的组件消融实验量化了各模块的贡献。基线模型（仅使用 Transformer 编码器-解码器，无身体部位分解）的 D-H 仅为 6.40。引入身体部位分解后，D-H 提升至 6.85，增幅达 0.45，验证了将人体拆分为多个独立区域并分别编码能更精细地保留全身外观细节。进一步引入跨图像训练策略后，模型减少了对身份无关属性（如背景、光照）的过拟合，身份保持能力得到增强。

#### 身份嵌入 Token 长度分析

表 5 分析了身份嵌入 token 长度 $l_H$ 对性能的影响。当 token 长度从 4×4 增加到 16×16 时，D-H 从 5.81 持续提升至 6.85，表明密集的身份嵌入能够编码更丰富的局部外观信息，避免少量 token 造成的信息瓶颈。这一发现支持了方法的核心设计选择：通过身体部位分解和密集嵌入来最大化身份信息的保留。

### 失败模式与局限性

尽管 Visual Persona 在整体性能上表现优异，论文指出了两类典型失败模式：

1. **不准确的身体比例**：由于依赖冻结的 SDXL 扩散模型，生成图像可能出现手指融合、多余肢体等典型扩散模型伪影。通过负向提示可部分缓解，但无法根本解决。

2. **身份无关属性泄漏**：输入图像中被遮挡的背景元素（如树叶、建筑边缘）可能被错误地保留在生成图像中。例如，当输入人物身后有树枝时，生成图像可能在不相关区域出现相似的纹理碎片。论文计划通过改进前景分割模型来抑制此类泄漏，但当前方案仍依赖外部解析器的精度。

### 评估指标可靠性

论文采用的 GPT-based 评估指标（D-I、D-T、D-H）在附录 A.2 中与人类偏好进行了对齐验证。结果表明，GPT 评分与人类评估在身份保持和文本对齐两个维度上均具有较高一致性，优于传统的 I-DINO 和 I-CLIP 等自动指标。同时，论文提供了人类评估（图 6）作为补充验证，进一步增强了结论的可信度。

### 补充图表

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/001_Figure.jpg]]
*Figure: Input*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/010_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/011_Figure_7.jpg]]
*Figure 7: Comparison between StoryMaker [94] (orange) and Visual Persona (green), including full and zoomed-in images: Compared to StoryMaker, Visual Persona enables large deformations, including pose and facial expression variations, preserves clothing details, and generates realistic clothing textures. Table 3. Comparison between StoryMaker [94] and Visual Persona*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/015_Figure.jpg]]
*Figure: StoryMaker Visual Persona*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/022_Figure.jpg]]
*Figure: A.3. Human Evaluation on Facial Expression: Visual Persona outperforms prior works [90, 94] in text alignment related to facial expression. (a) Analysis on different weighting scalar (??) (b) Analysis on different layers (??) (c) Analysis on different time steps (??) Figure A.4. Analysis: Identity Cross-Attention Module. Users can balance identity preservation and text alignment by adjusting the weighting scalar λ, layers y, and time steps t. Increasing the weighting scalar λ and using later layers y and time steps t better preserve the image structure and layout from the pre-trained SDXL, while slightly compromising identity preservation from the input*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/025_Figure.jpg]]
*Figure: Input Image Generated Image*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative Comparison on PPR10K [49]: Compared to prior works that focus on face identity preservation [48, 84, 90] or fail to capture the input’s detailed appearance [90, 94], Visual Persona accurately preserves the full-body appearance while generating diverse images based on text prompts. Table 2. Quantitative Comparison*

![[assets/figures/papers/paper_list_l7_Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization/figures/013_Table_4.jpg]]
*Table 4: Component Analysis*

## 定位与知识库关联

### 方法定位与基线关系

**Visual Persona** 处于“文本引导的全身人体定制”这一新兴交叉点，其设计直接回应了现有方法在**身份保持范围**与**外观细节保真度**之间的根本张力。从方法谱系看，该工作可被定位为对三类基线方法的系统性超越：

**1. 面部定制方法的泛化瓶颈**

以 **IP-Adapter-FaceID**、**InstantID** 和 **PhotoMaker** 为代表的人脸定制方法，其核心设计是将身份信息压缩为面部嵌入，并通过少量 token（通常 4-16 个）注入扩散模型。这类方法在面部区域表现良好，但存在两个结构性局限：(a) 身份表征仅覆盖面部，无法传递服装纹理、体型比例等全身外观信息；(b) 稀疏的 token 嵌入在长序列生成中易丢失细节。Visual Persona 将身份表征从“面部嵌入”扩展为“身体部位分解的密集嵌入”，token 长度可达 16×16，从根本上突破了这一泛化瓶颈。

**2. 通用图像定制方法的细节丢失**

**IP-Adapter** 等通用图像定制方法虽可处理全身输入，但因缺乏对身体结构的显式建模，其全局特征编码方式难以保留细粒度外观（如服装褶皱、鞋款纹理）。Visual Persona 通过身体部位分解和 Body-Partitioned Transformer Decoder 的独立编码-精炼机制，将这一“全局压缩”策略替换为“局部保留-结构感知”策略，从而在保持文本对齐能力的同时显著提升外观保真度。

**3. 全身定制方法的过拟合问题**

**StoryMaker** 是目前最直接的全身人体定制基线，但其采用“单张图像重建训练”范式——即输入图像 X 与目标图像 Y 为同一张图。这种训练策略导致模型学习到“复制输入”的捷径，对背景、姿态、光照等身份无关属性产生严重过拟合。Visual Persona 的关键突破在于构建了 **Visual Persona-500K** 数据集（580k 图像，100k 身份），并采用**跨图像训练**策略——输入与输出为同一人的不同图像，迫使模型学习身份不变特征而非图像表面统计量。这一训练范式的转变是方法有效性的因果核心。

### 核心因果机制

Visual Persona 的性能优势可归因于三个相互增强的因果环节：

| 因果环节 | 机制 | 证据锚点 |
|---------|------|---------|
| **身体部位分解** | 将人体拆分为全身、面部、躯干、腿、鞋五个独立区域，分别提取局部特征，避免全局池化造成的信息丢失 | Table 4：消融实验显示，加入部位分解后 D-H 从 6.40 提升至 6.85 |
| **密集身份嵌入** | 通过 Transformer Decoder 将各部位特征投影为 16×16 的密集 token，而非传统方法的 4-16 个稀疏 token | Table 5：token 长度从 4×4 增至 16×16，D-H 从 5.81 提升至 6.85 |
| **跨图像训练** | 在配对数据集上进行跨图像训练，输入与目标为同一人的不同图像，阻断对身份无关属性的过拟合路径 | Table 3(a)：跨图像训练相比重建训练显著提升身份保持能力；Figure 7 定性展示过拟合缓解效果 |

这三个环节形成递进依赖：部位分解为密集嵌入提供了结构化的特征来源，而跨图像训练则确保这些密集嵌入学习到的是跨姿态、跨背景的身份不变表征，而非单张图像的表面纹理。

### 适用边界与局限

**已知局限**（论文明确指出的失败模式）：

1. **身体比例伪影**：由于依赖冻结的 SDXL 扩散模型，生成结果可能出现手指融合、多余肢体等解剖学错误。论文指出可通过负向提示（negative prompt）部分缓解，但未从根本上解决。这属于底层生成模型的固有局限，而非定制方法本身的设计缺陷。

2. **身份无关属性泄漏**：输入图像中被遮挡的背景元素（如树叶、栏杆）可能被错误地保留在生成图像中。这是跨图像训练策略的副作用——模型学到了某些与身份共现但不属于身份本身的视觉线索。论文计划通过改进前景分割模型来解决，但当前版本仍存在此问题。

**推断的适用边界**（基于方法设计推断，需手动验证）：

- **遮挡场景**：身体部位分解依赖现成的身体解析方法，在严重遮挡或非标准姿态下，部位分割质量可能下降，进而影响身份嵌入的准确性。
- **多人场景**：当前框架假设输入为单人图像，且身份嵌入的维度固定为 N×l_H（N 为部位数），未设计多人交互的身份分离机制。
- **极端外观变化**：Visual Persona-500K 的数据构建流程依赖 VLM 判断“是否穿着完全相同衣物”，这隐含假设同一人在不同图像中穿着相同服装。对于需要改变服装的虚拟试穿场景，该假设可能导致身份保持与服装编辑之间的张力。

### 开放问题

1. **身份无关属性泄漏的根本解决**：当前依赖手动掩码细化的方案是否可被自动化？能否通过对抗训练或信息瓶颈方法在特征层面直接抑制背景信息？

2. **负向提示的自动化**：论文提到使用负向提示缓解身体伪影，但提示设计依赖人工经验。是否可将这一过程集成到模型中，例如通过可学习的负向嵌入或质量感知的损失函数？

3. **极端遮挡与复杂交互的鲁棒性**：在拥挤场景、大幅度运动模糊或部分身体不可见的情况下，身体部位分解和特征编码的鲁棒性如何？

4. **多人定制扩展**：能否在不依赖专门多人数据集的前提下，通过身份嵌入的解耦或注意力掩码机制，将该框架扩展到多人交互场景？

5. **数据构建的覆盖完备性**：当前的 VLM 筛选流程（“是否穿着完全相同衣物”）是否遗漏了部分有效配对（如同一人换装后的图像）？这对服装编辑任务的泛化性有何影响？

## 原文 PDF

![[paperPDFs/CVPR_2025/Visual_Persona_Foundation_Model_for_Full_Body_Human_Customization.pdf]]

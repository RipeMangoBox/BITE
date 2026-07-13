---
title: "PALUM: Part-based Attention Learning for Unified Motion Retargeting"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PALUM_Part_based_Attention_Learning_for_Unified_Motion_Retargeting.pdf
project_link: null
code_link: null
aliases:
- PALUM
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将骨骼按生物力学原理划分为六个语义部位并共享连接关节，在部位内使用空间注意力池化提取固定长度的骨骼无关运动表征；结合时序Transformer与交叉注意力解码，并利用循环一致性损失保持运动语义。
primary_logic: 人体运动呈现部位局部性：同一肢体内关节高度相关，不同部位间交互较弱；通过注意力池化从各部位可变数量的关节中提取关键特征，可实现跨拓扑的一致运动表征。
claims:
- 在跨结构动作重定向中，PALUM的平均MSE误差（0.00567）显著优于最强基线MoMa（0.02340），相对降低约75.8%。
- 消融实验表明，允许组间共享关节连接可使内部结构重定向误差从0.00377降至0.00272，证明连接机制对保持全身协调至关重要。
- Mixamo Intra-Structural Retargeting (seen/unseen skeletons × seen/unseen motion... 上 MSE (归一化后) = 0.00272
- Mixamo Cross-Structural Retargeting (seen/unseen 平均值) 上 MSE (归一化后) = 0.00567
---

# PALUM: Part-based Attention Learning for Unified Motion Retargeting

> [!tip] 核心洞察
> 人体运动呈现部位局部性：同一肢体内关节高度相关，不同部位间交互较弱；通过注意力池化从各部位可变数量的关节中提取关键特征，可实现跨拓扑的一致运动表征。

| 字段 | 内容 |
|------|------|
| 中文题名 | PALUM：基于分部的注意力学习统一动作重定向 |
| 英文题名 | PALUM: Part-based Attention Learning for Unified Motion Retargeting |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.07272) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PALUM |
| Dataset | Mixamo Intra-Structural Retargeting, Mixamo Cross-Structural Retargeting |

> [!tip] 效果简介
> - Mixamo Intra-Structural Retargeting (seen/unseen skeletons × seen/unseen motion... 上，MSE (归一化后) 0.00272 vs MoMa 0.01100; PAN 0.00898; R²ET 0.00487 (相对于MoMa降低0.00828 (-75.3%))。
> - Mixamo Cross-Structural Retargeting (seen/unseen 平均值) 上，MSE (归一化后) 0.00567 vs MoMa 0.02340; PAN 0.01436 (相对于MoMa降低0.01773 (-75.8%))。

## 概要

### 问题瓶颈

现有骨骼动作重定向方法面临一个核心瓶颈：**难以在统一的框架下同时处理具有不同关节数量和拓扑结构的骨骼**。主流方法要么依赖手工指定的关节对应关系，要么采用全局注意力机制对整个骨架进行建模，但全局注意力无法有效学习人体运动的层次化特征，常引入冗余信息并导致学习困难。这限制了动作重定向在跨结构场景中的泛化能力与实用性。

### 核心方法

**PALUM**（Part-based Attention Learning for Unified Motion Retargeting）提出了一种基于分部的注意力学习框架，其核心调控机制包含三个层面：

- **语义分组与连接策略**：将骨骼按生物力学原理划分为躯干、左/右腿、左/右臂和头部六个语义部位，并令腿组与躯干共享髋关节、臂组和头组与躯干共享最上端脊椎关节，从而在部位独立性与全身协调性之间取得平衡。
- **空间注意力池化**：在每个部位内部使用可学习的查询向量，通过缩放点积注意力将可变数量的关节特征聚合为固定维度的骨骼无关运动表征，解决了跨拓扑统一编码的难题。
- **时序编码与交叉注意力解码**：时序Transformer编码器捕获运动动态与跨部位交互，解码器以随机噪声和骨架嵌入为查询，通过交叉注意力将源运动表征映射到目标骨架，并结合循环一致性损失保持运动语义。

### 方法定位

PALUM在方法谱系中处于**基于学习的统一动作重定向**分支。与需要关节数相同或手工指定对应关系的**R²ET**（Zhang et al., CVPR 2023）、独立处理各部位导致全局连贯性不足的**PAN**（Hu et al., TVCG 2024）、以及采用全局注意力处理可变关节数但引入冗余的**MoMa**（Martinelli et al., CVIU 2024）相比，PALUM通过“语义分组 + 组内注意力池化 + 组间共享连接”的组合设计，实现了对可变拓扑骨骼的统一处理，同时保持了运动的全局协调性。

### 主要结果

在Mixamo数据集上的实验表明，PALUM在跨结构动作重定向上的平均MSE误差为**0.00567**，相较于最强基线MoMa的0.02340**相对降低约75.8%**（Table 1）。内部结构重定向的平均MSE为**0.00272**，同样显著优于所有基线方法。消融实验进一步验证了组间共享关节连接的关键作用：去除共享连接后，内部结构误差从0.00272升至0.00377，并出现头部异常倾斜等运动伪影（Table 2, Figure 5）。



动作重定向（Motion Retargeting）旨在将源角色的运动序列迁移至具有不同骨骼结构的目标角色，是计算机动画与角色驱动的核心技术。随着虚拟人、游戏、影视制作对多样化角色需求的激增，手工为每个骨骼拓扑重新制作动画已不可行，自动化重定向方法成为产业刚需。然而，人体骨骼在关节数量、骨骼长度比例和拓扑连接上呈现高度异构性——例如，标准Mixamo骨架可能包含65个关节，而SMPL模型仅24个关节，MetaHuman则可达上百个关节——这使得统一处理不同骨骼结构成为长期瓶颈。

现有方法在处理这一问题上存在系统性缺陷。**R²ET**（Zhang et al., CVPR 2023）基于Transformer进行动作重定向，但要求源与目标骨架关节数一致，并需复制源旋转作为解码器初始值；其扩展版本M-R²ET虽支持不同关节数，仍需手动指定关节链对应关系，缺乏自动化能力。**PAN**（Hu et al., TVCG 2024）采用基于部位操作的图神经网络，将身体分为多个部分独立处理，但因缺乏全局协调机制，导致不同部位间运动连贯性不足。**MoMa**（Martinelli et al., CVIU 2024）通过掩码Transformer处理可变关节数，但其全局注意力机制对所有关节进行统一建模，引入了大量冗余信息，不仅增加了学习难度，更难以捕获人体运动的层次化特征——即同一肢体内部关节高度相关、不同肢体间交互相对稀疏的局部性规律。

上述方法的共同瓶颈可归结为两点：其一，缺乏对人体运动生物力学先验的有效利用，即人体运动天然呈现**部位局部性**——手臂、腿、躯干等部位内部关节协同运动，而跨部位耦合相对较弱；其二，全局或独立分组的特征聚合方式无法在保持运动全局一致性的同时，从可变数量的关节中提取固定维度的骨骼无关表征，导致跨拓扑泛化能力受限。

针对这些缺口，本文提出**PALUM（Part-based Attention Learning for Unified Motion Retargeting）**。核心思路是将骨骼按生物力学原理划分为六个语义部位（左右臂、左右腿、脊椎、头部），并在相邻部位间共享髋部和脊椎连接关节，以此在部位独立性与全身协调性之间取得平衡。在每个部位内部，通过空间注意力池化（Spatial Attention Pooling）从可变数量的关节中提取固定维度的运动特征，再经由时序Transformer编码器捕获跨部位交互与时序动态，最终通过交叉注意力解码器将运动表征映射至目标骨架。配合循环一致性损失保持运动语义，PALUM实现了无需手工指定关节对应、可处理任意关节数和拓扑结构的统一动作重定向框架。



## 核心方法与创新机理

PALUM 的核心创新在于通过**部位感知的注意力学习**，首次实现了无需手工指定关节对应关系的统一动作重定向。与现有方法相比，其关键设计变更体现在以下四个维度：

### 1. 从全局处理到语义分组与共享连接

现有方法或采用全局注意力处理所有关节（如 **MoMa**，Martinelli et al., CVIU 2024），或进行无共享的独立部位操作（如 **PAN**，Hu et al., TVCG 2024），前者引入冗余和学习困难，后者导致全局连贯性不足。PALUM 将骨骼按生物力学原理划分为六个语义部位（躯干、左腿、右腿、左臂、右臂、头部），并在组间建立共享连接——腿组与躯干共享髋关节，手臂和头部组与躯干共享最上端脊椎关节。这一设计使部位内部紧密耦合、部位间协调一致，消融实验证实：去除共享连接后，内部结构重定向 MSE 从 0.00272 升至 0.00377，并出现头部异常倾斜等伪影（Table 2, Figure 5）。

### 2. 从手工关节对应到空间注意力池化

传统方法如 **R²ET**（Zhang et al., CVPR 2023）需复制源旋转作为初始值并限制关节数相同，其扩展版 M-R²ET 仍需手动指定关节链对应。PALUM 在每组内使用**空间注意力池化**，通过可学习查询向量 $\mathbf{q}_i$ 对可变数量的关节特征进行加权聚合：

$$\alpha_{i,j} = \frac{\exp(\mathbf{q}_i^T \mathbf{x}_j / \sqrt{d})}{\sum_{k=1}^n \exp(\mathbf{q}_i^T \mathbf{x}_k / \sqrt{d})}$$

该机制从任意关节数的部位中提取固定维度的骨骼无关运动表征，无需任何手工对应规则。同时，输入特征融合了位置编码、T5 关节名称嵌入和 T-pose 嵌入，构成增强组表示 $\mathbf{X}_{enhanced}^{(i)} = \mathbf{X}^{(i)} + \mathbf{E}_{PE}^{(i)} + \mathbf{E}_{name}^{(i)} + \mathbf{E}_{T-pose}^{(i)}$，为注意力池化提供丰富的语义和结构信息。

### 3. 从复制初始化到随机噪声驱动解码

R²ET 等方法的解码器依赖复制源关节旋转作为初始值，限制了跨拓扑泛化能力。PALUM 的解码器输入完全由**随机均匀噪声**与目标骨架的嵌入相加构成：

$$\mathbf{Y}_{input}^{i} = \mathbf{Y}_{init} + \mathbf{E}_{PE}^{(t)} + \mathbf{E}_{name}^{(t)} + \mathbf{E}_{T-pose}^{i}$$

解码器通过交叉注意力从源运动表征 $\mathbf{H}$ 中查询相关信息，逐步将噪声转化为目标骨架的关节旋转。这一设计使模型不依赖源骨架的具体关节值，实现了真正的骨架无关解码。

### 4. 从单一重构损失到循环一致性约束

仅使用重构损失训练难以保证跨骨架的运动语义保持。PALUM 引入**循环一致性损失**，强制源动作编码 $\mathbf{H}_A$ 与回环重定向动作编码 $\mathbf{H}_B$ 在特征空间中对齐：

$$\mathcal{L}_{cyc} = \frac{1}{T \times B \times M \times D} \sum |\mathbf{H}_A - \mathbf{H}_B|_2^2$$

总训练目标组合了重构损失、循环一致性损失和根稳定性损失：$\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda_{cyc} \mathcal{L}_{cyc} + \lambda_{root} \mathcal{L}_{root}$，其中 $\lambda_{cyc}=20$，$\lambda_{root}=7$。这一机制是跨结构重定向性能的关键保障——在跨结构设定中，PALUM 的平均 MSE 为 0.00567，相比最强基线 MoMa 的 0.02340 降低了约 75.8%（Table 1）。

### 创新本质

上述四个 changed slots 共同指向一个核心洞察：**人体运动呈现部位局部性**——同一肢体内关节高度相关，不同部位间交互较弱。PALUM 通过部位内注意力池化提取关键特征，通过组间共享连接维持全身协调，通过循环一致性保持运动语义，从而在无需任何手工关节对应的情况下，实现了对不同关节数量和拓扑结构的统一动作重定向。



PALUM 的整体流程围绕一个**编码器-解码器架构**构建，其核心设计目标是实现与骨骼拓扑无关的统一动作重定向。该框架将源骨架的动作序列映射到任意目标骨架上，无论两者的关节数量、骨骼比例或拓扑结构是否相同。

### 输入与预处理

流程的输入包括：
- **源骨架的动作序列**：以 BVH 格式表示，包含各关节的局部旋转和根关节的全局位置/旋转。
- **目标骨架的静态信息**：关节名称、层次拓扑和 T-pose 下的关节位置。

预处理阶段，系统根据关节命名约定将源骨架和目标骨架的关节分别划分到六个语义部位组中（见 4.1 节），并剔除与运动无关的末端效应器关节。

### 编码器：骨骼无关运动表征提取

编码器负责从源动作中提取**固定维度的骨骼无关运动表征**，其处理流水线如下：

1. **关节语义分组**：将源骨架的所有关节按生物力学语义划分为六个部位组——躯干（torso）、左腿（left leg）、右腿（right leg）、左臂（left arm）、右臂（right arm）和头部（head）。关键设计是组间共享连接关节：左右腿组与躯干共享髋关节（hip joint），左右臂组和头部组与躯干共享最上方的脊椎关节（uppermost spine joint）。这一共享机制确保了身体各部位运动的全局协调性。

2. **空间注意力池化**（Section 4.2.1）：在每个部位组内部，使用可学习的查询向量（query vectors）通过缩放点积注意力对组内关节特征进行池化。注意力权重计算为：
   $$\alpha_{i,j} = \frac{\exp(\mathbf{q}_i^T \mathbf{x}_j / \sqrt{d})}{\sum_{k=1}^n \exp(\mathbf{q}_i^T \mathbf{x}_k / \sqrt{d})}$$
   该机制将每组内可变数量的关节聚合为固定维度的特征向量，从而消除骨骼拓扑差异。池化前，关节特征会增强位置编码、T5 关节名称嵌入和 T-pose 嵌入：
   $$\mathbf{X}_{enhanced}^{(i)} = \mathbf{X}^{(i)} + \mathbf{E}_{PE}^{(i)} + \mathbf{E}_{name}^{(i)} + \mathbf{E}_{T-pose}^{(i)}$$

3. **时序 Transformer 编码器**（Section 4.2.2）：六组部位的特征经池化后送入时序 Transformer，通过多头自注意力捕获运动序列的时间动态和跨部位交互，最终输出运动表征 $\mathbf{H}$。

### 解码器：骨骼特定运动生成

解码器将骨骼无关的运动表征映射回目标骨架的关节旋转：

1. **解码器输入初始化**（Section 4.3.1）：与现有方法（如 R²ET 复制源关节旋转作为初始值）不同，PALUM 的解码器输入初始化为随机均匀噪声 $\mathbf{Y}_{init}$，并加上目标骨架的位置编码、关节名称嵌入和 T-pose 嵌入：
   $$\mathbf{Y}_{input}^{i} = \mathbf{Y}_{init} + \mathbf{E}_{PE}^{(t)} + \mathbf{E}_{name}^{(t)} + \mathbf{E}_{T-pose}^{i}$$

2. **交叉注意力解码**（Section 4.3.2）：解码器通过交叉注意力机制，以目标骨架的增强输入为查询（query），从编码器输出的运动表征 $\mathbf{H}$ 中提取与目标关节相关的运动信息，生成各关节的局部旋转。

3. **正向运动学与根归一化**：根据目标骨架的拓扑层次，通过正向运动学（FK）计算全局关节位置。根关节的运动经过高度归一化处理，以适应不同骨架比例。

### 训练与推理

- **训练阶段**（Figure 2b）：采用双向重定向策略。动作 A 从骨架 A 重定向至骨架 B，再回环重定向回骨架 A。训练目标为加权组合：
  $$\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda_{cyc} \mathcal{L}_{cyc} + \lambda_{root} \mathcal{L}_{root}$$
  其中 $\mathcal{L}_{rec}$ 为自重建 MSE 损失，$\mathcal{L}_{cyc}$ 为循环一致性损失（约束源动作编码 $\mathbf{H}_A$ 与回环重定向动作编码 $\mathbf{H}_B$ 的 L2 距离），$\mathcal{L}_{root}$ 为根关节位置和旋转的 MSE 损失。超参数设置为 $\lambda_{cyc}=20$，$\lambda_{root}=7$。

- **推理阶段**（Figure 2c）：仅使用前向重定向路径，循环一致性组件被禁用。源骨架动作经编码器提取表征后，直接通过解码器生成目标骨架的动作序列。

### 关键设计决策的因果链

框架的核心因果机制可概括为：**部位分组 + 共享连接关节** → 局部运动特征的结构化提取 → **注意力池化** → 消除关节数量差异的固定维度表征 → **循环一致性训练** → 跨骨架运动语义保持。消融实验（Table 2）证实，去除组间共享连接关节会导致身体部位运动不一致，内部结构误差从 0.00272 升至 0.00377，并出现头部异常倾斜等伪影（Figure 5）。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2601_07272/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our motion retargeting framework. (a) Encoder-decoder architecture: The transformer encoder processes source motion sequences through multiple attention pooling layers to extract skeleton-agnostic motion representations. These representations are fed to an MLP that outputs key-value pairs for cross-attention in the transformer decoder. The decoder takes uniformly sampled noise and skeleton-specific embeddings to generate target motion sequences. Note that the target skeleton shown in this pipeline includes pauldron joints, demonstrating our method’s capability to handle diverse skeletal topologies. (b) Training pipeline: The model is trained using reconstruction and cycle consis...*



PALUM 的核心架构由四个关键模块串联构成：关节语义分组、空间注意力编码、时序 Transformer 编码与交叉注意力解码。以下逐一剖析各模块的机制与关键公式。

### 关节语义分组模块

该模块将任意骨架按生物力学原理划分为六个语义部位：**躯干（Torso）、左腿（Left Leg）、右腿（Right Leg）、左臂（Left Arm）、右臂（Right Arm）和头部（Head）**。分组并非完全独立——组间通过共享连接关节来维持全身运动的协调性：左右腿组与躯干共享髋关节（Hip），左右臂组和头部组与躯干共享最上端脊椎关节（Uppermost Spine）。这一设计是 PALUM 跨拓扑泛化的基础，消融实验证明去除共享连接后，身体部位运动不一致，内部结构误差从 0.00272 升至 0.00377，并出现头部异常倾斜等伪影（Table 2, Figure 5）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2601_07272/figures/007_Table_2.jpg]]
*Table 2: Quantitative ablation study results evaluating key design components of our method on both intra-structure and crossstructure motion retargeting performance. Figure 5. Qualitative results of ablation studies demonstrating the impact of key design components. We show overlaid predictions with the GT target. Without shared joints, body parts move independently, causing unnatural artifacts such as extreme head tilting. Excluding positional information reduces end-effector accuracy, while joint masking disrupts hierarchical skeletal relationships, leading to degraded motion quality*

### 空间注意力编码器

编码器需从每组内可变数量的关节中提取固定维度的骨骼无关表征。其核心操作是**注意力池化（Attention Pooling）**：为每个身体部位设置一组可学习的查询向量 $\mathbf{q}_i$，通过缩放点积注意力对组内关节特征 $\mathbf{x}_j$ 进行加权聚合：

$$\alpha_{i,j} = \frac{\exp(\mathbf{q}_i^T \mathbf{x}_j / \sqrt{d})}{\sum_{k=1}^n \exp(\mathbf{q}_i^T \mathbf{x}_k / \sqrt{d})} \tag{1}$$

其中 $d$ 为特征维度，$n$ 为该组内的关节数量。注意力权重 $\alpha_{i,j}$ 衡量查询向量 $\mathbf{q}_i$ 对各关节的关注程度，池化后的输出维度仅取决于查询向量数量而非关节数，从而实现了**关节数量的解耦**。

在池化之前，每组关节特征还需融合三种嵌入信息以增强表征能力：

$$\mathbf{X}_{enhanced}^{(i)} = \mathbf{X}^{(i)} + \mathbf{E}_{PE}^{(i)} + \mathbf{E}_{name}^{(i)} + \mathbf{E}_{T-pose}^{(i)} \tag{2}$$

- **$\mathbf{E}_{PE}^{(i)}$**：位置编码，提供关节在组内的顺序信息；
- **$\mathbf{E}_{name}^{(i)}$**：基于 T5 模型的关节名称语义嵌入，捕获关节的功能角色；
- **$\mathbf{E}_{T-pose}^{(i)}$**：T-pose 下的结构嵌入，编码骨骼的几何拓扑信息。

消融实验表明，去除位置信息（仅保留旋转）会导致末端关节精度下降，内部误差升至 0.00350（Table 2）。

### 时序 Transformer 编码器

六组池化后的特征拼接后送入标准 Transformer 编码器，通过多头自注意力机制同时捕获**时序动态**与**跨部位交互**。该模块输出运动表征 $\mathbf{H}$，作为后续解码过程的源运动语义载体。

### 交叉注意力解码器

解码器负责将源运动表征映射到目标骨架的关节旋转上。与 R²ET 等方法不同，PALUM 的**解码器输入不依赖源关节旋转作为初始值**，而是从随机均匀噪声出发，并融入目标骨架的结构信息：

$$\mathbf{Y}_{input}^{i} = \mathbf{Y}_{init} + \mathbf{E}_{PE}^{(t)} + \mathbf{E}_{name}^{(t)} + \mathbf{E}_{T-pose}^{i} \tag{3}$$

其中 $\mathbf{Y}_{init}$ 为随机均匀噪声，$\mathbf{E}_{PE}^{(t)}$、$\mathbf{E}_{name}^{(t)}$ 和 $\mathbf{E}_{T-pose}^{i}$ 分别为目标骨架的位置编码、关节名称嵌入和 T-pose 嵌入。解码器以这些增强后的目标骨架表征为查询（Query），以编码器输出的运动表征 $\mathbf{H}$ 经 MLP 投影后作为键值对（Key-Value），通过交叉注意力将源运动语义“注入”到目标骨架结构中，生成目标关节旋转。

### 正向运动学与根归一化

解码器输出的关节旋转经正向运动学（FK）计算全局关节位置。为消除骨架尺度差异对损失计算的影响，对根运动进行高度归一化处理。

### 训练目标

训练阶段采用三项损失的加权组合：

$$\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda_{cyc} \mathcal{L}_{cyc} + \lambda_{root} \mathcal{L}_{root}$$

- **重构损失** $\mathcal{L}_{rec} = \text{MSE}(\mathcal{M}_A, \mathcal{M}_{A'})$：源动作 $\mathcal{M}_A$ 与自重建动作 $\mathcal{M}_{A'}$ 之间的均方误差；
- **循环一致性损失** $\mathcal{L}_{cyc} = \frac{1}{T \times B \times M \times D} \sum |\mathbf{H}_A - \mathbf{H}_B|_2^2$：源动作编码 $\mathbf{H}_A$ 与经目标骨架重定向后再回环的编码 $\mathbf{H}_B$ 之间的 L2 距离，用于保持运动语义；
- **根稳定性损失** $\mathcal{L}_{root} = \text{MSE}(\mathbf{p}_{root}^A, \mathbf{p}_{root}^{A'}) + \text{MSE}(\mathbf{r}_{root}^A, \mathbf{r}_{root}^{A'})$：根关节位置与旋转的 MSE。

权重设置为 $\lambda_{cyc}=20$，$\lambda_{root}=7$。测试阶段仅使用前向重定向路径，循环一致性组件被禁用。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2601_07272/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results of our method and the baselines. Our method preserves the natural motion dynamics and joint relationships*



## 实验与关键发现

### 实验设置

实验基于Mixamo数据集进行，评估涵盖**内部结构重定向**（Intra-Structural Retargeting）和**跨结构重定向**（Cross-Structural Retargeting）两种场景。内部结构重定向按seen/unseen骨骼和seen/unseen动作组合划分，跨结构重定向则在完全不同的骨骼拓扑间进行。评估指标为按角色身高归一化后的均方误差（MSE）。对比基线包括基于Transformer的**R²ET**（Zhang et al., CVPR 2023）、基于部位图神经网络的**PAN**（Hu et al., TVCG 2024）以及基于掩码Transformer的**MoMa**（Martinelli et al., CVIU 2024）。

### 主要定量结果

Table 1展示了各方法在内部结构与跨结构重定向任务上的MSE对比。

**内部结构重定向**方面，PALUM取得了0.00272的平均MSE，显著优于所有基线方法。相比之下，MoMa为0.01100，PAN为0.00898，R²ET为0.00487。PALUM相对MoMa误差降低约75.3%（-0.00828），相对R²ET降低约44.1%。这一结果表明，基于部位的空间注意力池化有效捕捉了同一骨骼内部各肢体的运动特征，避免了全局注意力引入的冗余信息。

**跨结构重定向**方面，PALUM的优势更为突出，平均MSE为0.00567。MoMa为0.02340，PAN为0.01436，R²ET因需要源与目标关节数相同而无法直接处理跨结构任务。PALUM相对MoMa误差降低约75.8%（-0.01773），证明六部位分组策略和共享连接关节机制在跨拓扑泛化中的关键作用——即使目标骨骼的关节数量和骨骼比例与源骨架完全不同，模型仍能生成协调一致的运动。

### 消融实验

Table 2和Figure 5通过消融实验验证了三个核心设计组件的贡献。

**去除组间共享关节连接**（w/o share）导致内部结构误差从0.00272升至0.00377，跨结构误差也从0.00567升至0.00593。定性结果显示，身体各部位运动不一致，出现头部异常倾斜等伪影。这证实了共享髋关节和脊椎关节对维持全身运动协调的必要性——这些连接关节作为信息桥梁，使各部位在独立编码的同时保持全局连贯。

**去除位置信息**（w/o pos，仅保留旋转特征）使内部误差升至0.00350，跨结构误差升至0.00615。Figure 5显示末端关节（手、脚）精度明显下降。位置特征为模型提供了关节在空间中的绝对坐标信息，对精确定位末端效应器至关重要。

**引入随机关节掩蔽**（w/ mask，类似MoMa的训练策略）反而使内部误差升至0.00343，跨结构误差升至0.00606。这表明随机掩蔽破坏了骨骼固有的层次关系，而PALUM的部位分组策略天然保留了这种层次结构，无需额外的数据增强。

### 定性分析

Figure 4展示了各方法的定性对比。PALUM生成的运动保持了自然的运动动力学和关节关系，而MoMa和PAN在处理复杂动作时会出现肢体不协调或关节位置偏差。Figure 6进一步展示了PALUM的泛化能力：将Mixamo源动作成功重定向至SMPL和MetaHuman模型，后者具有不同的关节数量和骨骼比例。

### 失败模式与局限性

尽管PALUM在整体性能上表现优异，仍存在以下已知局限：

1. **脊椎关节数量差异**：当源骨架与目标骨架的脊椎关节数量差异较大时（如Mixamo的4关节脊椎到MetaHuman的6关节脊椎），基于T5的关节名称嵌入会导致过度弯曲。当前通过合并中间关节缓解，但可能引入人工痕迹。这一问题的根源在于名称嵌入无法充分编码关节链的长度信息。

2. **命名约定依赖**：方法依赖BVH文件的关节命名规范进行语义分组。对于非标准命名或不同语言的骨骼，需要额外的规则映射或预处理步骤。

3. **非人形骨架泛化**：当前设计基于人体生物力学原理的六部位划分，尚未在四足动物等非人形骨架上验证。推广到完全不同身体结构的模型仍需探索。

### 关键图表结论

- **Table 1**：PALUM在内部结构和跨结构重定向任务上均取得最低MSE，跨结构场景下相对MoMa降低75.8%，验证了部位注意力池化对跨拓扑泛化的有效性。
- **Table 2 & Figure 5**：共享连接关节是维持全身协调的核心机制，去除后出现部位间运动不一致；位置信息对末端关节精度至关重要；随机关节掩蔽反而破坏层次关系。
- **Figure 4**：定性对比表明PALUM在运动自然度和关节关系保持上优于所有基线。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2601_07272/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on intra-structure and cross-structure motion retargeting*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2601_07272/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2601_07272/figures/003_Figure_3.jpg]]
*Figure 3: T-pose examples after our joint elimination strategy. (1) Warrok: the pauldron joints are named as ”RightArmourx” (x=1,2,3,4,5) in the BVH file, so they match our ”RightArm” joint name selection and they are preserved. (2) BigVegas: the hair joints are named as ”HeadTop Endx” (x=1,2), which match our ”Head” joint name selection, so they are preserved*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

PALUM 瞄准的是**统一动作重定向**（unified motion retargeting）问题：将源骨架的运动序列迁移到具有不同关节数量、拓扑结构和骨骼比例的目标骨架上，而无需针对每对骨架手工指定关节映射。现有方法的根本瓶颈在于：**全局注意力机制无法有效学习层次化的骨骼运动特征**，且多数方案要求源与目标骨架具有相同的关节数或需人工指定关节对应链。人体运动呈现强烈的部位局部性——同一肢体内的关节高度相关，而不同部位间的交互相对稀疏——但此前的方法未能将这一先验结构化为网络归纳偏置。

### 2. 方法谱系与基线对比

PALUM 的方法设计可视为对以下三条技术路线的批判性综合：

| 方法 | 核心机制 | 关键局限 | PALUM 的改进 |
|------|----------|----------|--------------|
| **R²ET** (Zhang et al., CVPR 2023) | 基于 Transformer 的动作重定向，需复制源旋转作为解码器初始化 | 限制源与目标关节数相同；扩展版 M-R²ET 仍需手动指定关节链对应 | 解码器以随机噪声初始化，彻底解耦源骨架结构；通过语义分组实现自动对应 |
| **PAN** (Hu et al., TVCG 2024) | 基于部位操作的图神经网络，独立处理各身体部位 | 部位间缺乏共享连接，导致全身运动连贯性不足 | 在六组语义分组间共享髋关节和脊椎关节，保持全身协调 |
| **MoMa** (Martinelli et al., CVIU 2024) | 基于掩码 Transformer 处理可变关节数，使用全局注意力 | 全局注意力引入冗余信息，学习困难；随机掩蔽策略破坏骨骼层次关系 | 以组内空间注意力池化替代全局注意力，保留层次结构；消融实验证实随机掩蔽反而有害（Table 2） |

**技术演进逻辑**：R²ET 证明了 Transformer 在动作重定向中的潜力，但受限于结构同构假设；PAN 引入了部位分解的思想，但缺乏跨部位协调机制；MoMa 首次尝试处理可变关节数，但全局注意力缺乏结构归纳偏置。PALUM 的关键突破在于将**生物力学启发的部位分组**与**注意力池化**结合，在每个部位内从可变数量的关节中提取固定维度的骨骼无关表征，再通过时序 Transformer 捕获跨部位交互。

### 3. 核心设计决策与消融证据

PALUM 的四个关键设计槽位及其消融验证：

1. **关节分组与共享连接**（Section 4.1, Table 2）：将骨架划分为躯干、左/右腿、左/右臂、头部六个语义组，腿组与躯干共享髋关节，臂组和头组与躯干共享最上端脊椎关节。去除组间共享连接后，内部结构重定向 MSE 从 0.00272 升至 0.00377，且出现头部异常倾斜等伪影（Figure 5），证实共享连接对维持全身运动协调至关重要。

2. **空间注意力池化**（Section 4.2.1, Eq. 1-2）：每组内使用可学习查询向量 $\mathbf{q}_i$ 对关节特征进行缩放点积注意力池化，权重为 $\alpha_{i,j} = \frac{\exp(\mathbf{q}_i^T \mathbf{x}_j / \sqrt{d})}{\sum_{k=1}^n \exp(\mathbf{q}_i^T \mathbf{x}_k / \sqrt{d})}$，将可变长度关节序列压缩为固定维度表征。这一设计使编码器输出与源骨架关节数无关，是实现跨拓扑重定向的核心机制。

3. **解码器初始化策略**（Section 4.3.1, Eq. 3）：解码器输入 $\mathbf{Y}_{input}^{i} = \mathbf{Y}_{init} + \mathbf{E}_{PE}^{(t)} + \mathbf{E}_{name}^{(t)} + \mathbf{E}_{T-pose}^{i}$，其中 $\mathbf{Y}_{init}$ 为随机均匀噪声，而非复制源关节旋转。这避免了 R²ET 对源骨架结构的依赖，使解码器完全由目标骨架嵌入和交叉注意力驱动。

4. **训练目标组合**（Section 4.5）：总损失 $\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda_{cyc} \mathcal{L}_{cyc} + \lambda_{root} \mathcal{L}_{root}$，其中循环一致性损失 $\mathcal{L}_{cyc}$ 约束源运动编码 $\mathbf{H}_A$ 与回环重定向运动编码 $\mathbf{H}_B$ 的 L2 距离，是保持运动语义的关键。$\lambda_{cyc}=20$，$\lambda_{root}=7$。

### 4. 适用边界与局限

**已知局限**（论文明确讨论）：

- **脊椎链长度泛化问题**：基于 T5 的关节名称嵌入在处理脊椎关节数量差异较大的链时会导致过度弯曲（如 Mixamo 的 4 关节脊椎 → MetaHuman 的 6 关节脊椎）。当前通过合并中间关节缓解，但可能引入人工痕迹。
- **命名规范依赖**：方法依赖 BVH 关节命名约定进行语义分组和关节消除（Figure 3），对非标准命名或不同语言的骨骼需要额外适配规则。
- **骨架形态限制**：尚未在四足动物等非人形骨架上验证，泛化到完全不同身体结构的模型仍需探索。

**适用条件推断**（基于方法设计）：

- 方法假设骨架可被划分为六个语义部位，且存在可识别的髋关节和脊椎关节作为共享连接点。对于缺少明确躯干-肢体层次结构的骨架（如蛇形、软体动物），分组策略可能失效。
- 注意力池化使用固定数量的查询向量，其表征容量是否足以保留极端姿态（如体操、武术）或快速复杂运动的细节，论文未给出明确验证。

### 5. 开放问题

1. **语义鲁棒性**：能否利用骨骼长度比例、自由度约束等几何特征替代或补充命名语义，以增强对不同命名习惯的鲁棒性？
2. **循环一致性扩展**：当前循环一致性为单轮回环，是否可扩展为多轮迭代或双向训练策略，以进一步提升语义保持能力？
3. **拓扑泛化边界**：如何将该框架推广到四足动物、多足动物或任意拓扑的非人形骨骼？部位分组的定义是否需要自适应学习？
4. **表征容量**：注意力池化的固定维度表征是否足以保留极端姿态或快速复杂运动的细节？是否需要根据运动复杂度自适应调整查询数量？
5. **评估基准局限**：当前评估仅基于 Mixamo 数据集，缺乏在更广泛骨架类型（如不同体型比例、非人形角色）上的标准化基准。



## 原文 PDF

![[paperPDFs/arxiv_2026/PALUM_Part_based_Attention_Learning_for_Unified_Motion_Retargeting.pdf]]

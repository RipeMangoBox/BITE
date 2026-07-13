---
title: Text2HOI Text guided 3D Motion Generation for Hand Object Interaction
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction.pdf
project_link: null
code_link: https://github.com/JunukCha/Text2HOI
aliases:
- TTG3MGHOI
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将交互生成任务分解为“接触图生成”和“手-物体运动生成”两个子任务，并利用接触图作为运动生成的强先验，从而在有限的增强数据上学习到泛化能力强的通用几何表示。
primary_logic: 通过预测与物体类别无关的局部几何接触图，并结合物体尺度信息，可以为扩散模型提供类别无关的强先验，使得从文本生成多样化且物理正确的交互成为可能。
claims:
- 任务分解使模型能从有限数据中学习通用几何表示，缓解标注数据稀缺问题。
- 接触图作为条件显著改善了运动的物理合理性和泛化性。
- 框架在三个数据集上全面超越基线方法，验证了分解设计的有效性。
- 消融实验确认接触图、几何损失、位置编码和手部细化模块各自对最终性能的贡献。
---

# Text2HOI Text guided 3D Motion Generation for Hand Object Interaction

> [!tip] 核心洞察
> 通过预测与物体类别无关的局部几何接触图，并结合物体尺度信息，可以为扩散模型提供类别无关的强先验，使得从文本生成多样化且物理正确的交互成为可能。

| 字段 | 内容 |
|------|------|
| 中文题名 | Text2HOI：文本引导的3D手-物体交互运动生成 |
| 英文题名 | Text2HOI Text guided 3D Motion Generation for Hand Object Interaction |
| 会议/期刊 | CVPR 2024 |
| Links | [Code](https://github.com/JunukCha/Text2HOI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Text2HOI |
| Dataset | H2O, GRAB, ARCTIC |

> [!tip] 效果简介
> - H2O 上，Accuracy (top-3) ↑ 0.8295 ± 0.0015 vs 0.6463 ± 0.0014 (T2M) (+0.1832)；FID ↓ 0.1744 ± 0.0013 vs 0.2945 ± ? (IMOS) (-0.1201)。
> - GRAB 上，Physical realism ↑ 0.8839 ± 0.0005 vs best competitor (not explicitly extracted) (--)。
> - ARCTIC 上，Accuracy (top-3) ↑ 0.9205 ± 0.0012 vs best competitor (not explicitly extracted) (--)。

## 概要

**核心问题**：从自然语言文本提示生成物理上合理、语义上准确的3D手-物体交互运动，面临两大瓶颈——现有3D手-物体交互数据集在交互类型和物体类别上远未泛化，且缺乏对应的文本标签，使得直接从文本到交互运动的学习极其困难。

**核心思路**：Text2HOI 将这一复杂生成任务**分解为两个子任务**——接触图生成和手-物体运动生成。模型首先基于文本和规范物体网格预测物体表面的3D接触概率图，然后将该接触图作为强先验输入扩散模型，指导手-物体运动的生成。这种分解使得模型能从有限的增强数据中学习到与物体类别无关的通用几何表示，从而缓解标注数据稀缺的瓶颈。

**方法定位**：Text2HOI 属于**文本条件扩散生成**方法，其关键创新在于引入了接触图作为中间表示，将物理交互先验显式地注入生成过程。相比直接适配文本到运动的方法（如 **T2M** 和 **MDM**），以及基于动作标签的交互生成方法（如 **IMOS**），Text2HOI 通过接触图先验、帧级与代理级位置编码、几何感知损失函数以及前馈手部细化网络，系统性地提升了生成质量与物理真实性。

**主要结果**：在 H2O、GRAB 和 ARCTIC 三个数据集上，Text2HOI 在准确性（Accuracy）、FID、多样性（Diversity）和物理真实性（Physical realism）等指标上全面超越基线方法。例如，在 H2O 数据集上，top-3 准确率从 T2M 的 0.6463 提升至 0.8295，FID 从 IMOS 的 0.2945 降至 0.1744；在 GRAB 数据集上，物理真实性达到 0.8839。消融实验确认了接触图条件、几何损失、位置编码以及手部细化模块各自对性能的独立贡献。定性结果显示，Text2HOI 能够在训练未见过的物体上生成合理的交互运动，展现出良好的泛化能力。

在3D手-物体交互生成领域，一个核心瓶颈在于现有数据集的交互类型与物体类别远未泛化，且缺乏对应的文本标签。这使得从自然语言提示直接生成物理上合理、语义上正确的3D交互运动变得极其困难。传统的运动生成方法主要面向全身人体运动，对手部精细操作与物体交互的建模关注不足；而少数面向手-物体交互的工作又往往依赖动作标签或初始手部姿态，难以实现开放文本条件下的多样化生成。

这一困境的根源在于标注数据的稀缺性。手-物体交互涉及高维连续姿态空间与复杂的接触约束，人工标注成本极高。现有数据集虽然在特定场景下提供了高质量的运动捕捉数据，但其覆盖的物体类别和交互方式有限，导致模型在面对训练中未见过的物体或交互类型时泛化能力严重不足。与此同时，文本到运动（Text-to-Motion）领域的方法如**T2M**和**MDM**在全身人体运动生成上取得了显著进展，但其直接迁移到手-物体交互场景时，由于缺乏对接触几何和物体属性的显式建模，生成结果往往存在穿透、接触不自然等问题。**IMOS**等方法虽然考虑了物体交互，但其依赖动作标签而非自由文本，限制了使用的灵活性。

面对上述缺口，本文提出**Text2HOI**框架，其核心动机在于通过任务分解来缓解数据稀缺带来的学习困难。具体而言，将手-物体交互生成拆解为“接触图生成”和“手-物体运动生成”两个子任务。接触图刻画了物体表面哪些区域可能被手部触碰，这一几何表示与物体类别无关，因而可以从有限数据中学习到泛化能力强的通用先验。随后，运动生成模型以接触图为强条件，在扩散模型的框架下生成物理合理且语义匹配的手-物体运动序列。这一分解设计的直觉在于：接触图作为中间表示，桥接了文本语义与3D几何，使得模型无需从零开始学习复杂的交互模式，而是可以在接触先验的引导下专注于运动时序的生成。

## 核心方法与创新机理

Text2HOI 的核心创新在于将文本引导的3D手-物体交互运动生成任务**分解为两个子任务**——接触图生成与手-物体运动生成——并通过接触图作为强先验，在有限的增强数据上学习到泛化能力强的通用几何表示。这一设计直击当前领域的真实瓶颈：现有3D手-物体交互数据集在交互类型和物体类别上远未泛化，且缺乏对应文本标签，导致从文本提示生成物理与语义上合理、多样化的3D交互变得极其困难。

具体而言，Text2HOI 相对基线方法（如 T2M、MDM、IMOS）在以下几个关键维度上实现了 **changed slots**：

### 1. 运动先验：从“无接触先验”到“接触图强先验”

基线方法仅依赖文本条件直接生成运动，缺乏对手-物体空间关系的显式建模。Text2HOI 引入了一个基于 VAE 的接触预测网络 $f^{\text{contact}}$（Sec. 3.1），该网络以文本特征、规范物体网格点云、物体尺度 $s_{\text{obj}}$ 和高斯噪声为输入，预测物体表面 $N$ 个点的接触概率图 $\hat{\mathbf{m}}_{\text{contact}} \in \mathbb{R}^{N \times 1}$ 以及物体几何特征 $\mathbf{F}_{\text{obj}} \in \mathbb{R}^{1024}$。这一接触图作为扩散模型的强条件输入，为运动生成提供了**类别无关的几何先验**，使模型能够泛化到训练中未见过的物体类别（Figure 5 展示了这一泛化能力）。消融实验证实，移除接触图条件和物体尺度条件会导致手部姿态适宜性显著下降（Table 2: w/o $m_{\text{contact}}$ & $s_{\text{obj}}$）。

### 2. 位置编码：从“仅帧级编码”到“帧级+代理级双重编码”

传统方法仅使用帧级位置编码来区分时间步。Text2HOI 提出同时使用**帧级位置编码**和**代理级位置编码**（Sec. 3.2.3），后者显式区分左手、右手和物体三个代理的身份。这一设计使 Transformer 编码器能够更精细地建模多代理之间的时空关系。消融实验表明，移除帧级和代理级位置编码导致 GRAB 数据集上的准确性从 0.9218 骤降至 0.8294（Table 2）。

### 3. 几何损失：从“简单重建损失”到“距离图损失+相对方向损失”

基线方法通常仅使用 L2 重建损失。Text2HOI 的运动生成器训练损失 $L_{\text{THOI}}$ 在扩散损失 $L_{\text{diff}}$ 的基础上，额外引入了两个几何感知损失（Sec. 3.2.3）：

- **距离图损失** $L_{\text{dm}}$：仅在手-物体距离小于阈值 $\tau = 2\text{cm}$ 时激活，促使近距离交互区域的预测更准确。
- **相对方向损失** $L_{\text{ro}}$：惩罚手与物体之间预测相对旋转与真实相对旋转的差异，增强3D空间关系理解。

消融实验确认，移除 $L_{\text{dm}}$ 和 $L_{\text{ro}}$ 会导致手-物体交互质量下降（Table 2）。

### 4. 运动细化：从“无后处理”到“前馈手部细化网络”

基线方法生成运动后不做额外修正。Text2HOI 引入一个**前馈 Transformer 手部细化网络** $f^{\text{ref}}$（Sec. 3.3），该网络不涉及扩散机制，仅接收 Text2HOI 生成的手部输出、手部关节、预测接触图、变形物体点云和基于距离的注意力图作为输入，输出修正后的手部姿态。其训练损失 $L_{\text{refine}}$ 结合了简单 L2 重建损失 $L_{\text{simple}}$、穿透损失 $L_{\text{penet}}$ 和接触损失 $L_{\text{contact}}$（权重 $\lambda_1 = 5$），有效减少手部穿透物体并改善接触质量。消融实验表明，移除细化网络或其穿透/接触损失会导致物理真实性大幅下降（Table 2）。此外，该前馈细化器在物理真实性和推理速度上均优于基于扩散的细化方法（Table S1、S2：推理仅需 0.013s）。

这些 changed slots 共同构成了 Text2HOI 的核心创新体系：**接触图提供几何先验 → 双重位置编码增强代理感知 → 几何损失强化空间关系 → 细化网络修复物理瑕疵**，形成了一条从粗到精、从语义到几何的完整生成链路。

Text2HOI 的整体框架遵循“先验生成—运动扩散—后处理细化”的三阶段流水线设计，如 **Figure 2** 所示。给定一个文本提示和一个规范物体网格作为输入，系统依次完成**接触图预测**、**手‑物体运动生成**和**手部姿态细化**三个步骤，最终输出物理合理且语义匹配的 3D 手‑物体交互运动序列。

![[assets/figures/papers/paper_list_l1726_Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: Schematic diagram of the overall framework. Given a text prompt and a canonical object mesh prompt, our aim is to generate the 3D motion for hand-object interaction. We first generate a contact map from the canonical object mesh conditioned by the text prompt and object’s scale. The hand-object motion generation module removes the noise from the inputs for the denoised outputs to align with the predicted contact map and the text prompt. The denoised outputs exhibit artifacts, including the penetration. To address these artifacts, the hand refinement module adjusts the generated (denoised) hand pose parameters to restrain the penetration and to improve contact interactions*

### 阶段一：接触图预测

第一阶段的核心目标是生成一个与物体类别无关的**接触图先验**，为后续的运动生成提供强几何约束。具体而言，接触预测网络 $f^{\text{contact}}$ 接收以下输入：
- 从规范物体网格采样并归一化的点云 $\mathbf{P}_{\text{norm}}$
- 文本提示的 CLIP 特征 $f^{\text{CLIP}}(T)$
- 物体的尺度信息 $s_{\text{obj}}$
- 高斯随机噪声向量 $\mathbf{z}_{\text{contact}}$

网络输出两个关键信息：
1. **接触图** $\hat{\mathbf{m}}_{\text{contact}} \in \mathbb{R}^{N \times 1}$：在 $N$ 个物体表面点上预测的手部接触概率分布；
2. **物体几何特征** $\mathbf{F}_{\text{obj}} \in \mathbb{R}^{1024}$：编码了物体形状的全局表示。

这一阶段的设计使模型能够从有限的标注数据中学习到通用的几何表示，因为接触图仅依赖于物体表面的局部几何和文本语义，而不要求模型记忆特定的物体类别。

### 阶段二：手‑物体运动生成

第二阶段是框架的核心——基于 Transformer 的扩散运动生成器 $f^{\text{THOI}}$。该模块以加噪的运动序列 $\mathbf{x}_t$ 为输入，通过反向扩散过程预测干净的手‑物体运动 $\hat{\mathbf{x}}_0$。

运动表示 $\mathbf{x}_0$ 同时包含左右手和物体的参数序列：
$$\mathbf{x}_0 = \{ \mathbf{x}_{0,\text{lhand}}^l, \mathbf{x}_{0,\text{rhand}}^l, \mathbf{x}_{0,\text{obj}}^l \}_{l=1}^{L_{\text{max}}}$$

扩散生成器的条件输入 $c$ 由四部分组成：
- 文本特征
- 第一阶段预测的接触图 $\hat{\mathbf{m}}_{\text{contact}}$
- 物体几何特征 $\mathbf{F}_{\text{obj}}$
- 物体尺度 $s_{\text{obj}}$

**Figure 3** 详细展示了这一阶段的架构。在正向过程中，原始运动 $\mathbf{x}_0$ 按照 DDPM 公式逐步加噪：
$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_t$$

在反向过程中，Transformer 编码器接收加噪运动 $\mathbf{x}_t$、时间步嵌入 $t_{\text{emb}}$ 以及条件嵌入 $\mathbf{X}_{\text{cond}}$，预测干净运动 $\hat{\mathbf{x}}_0$。该模块的一个关键设计是同时使用**帧级位置编码**和**代理级位置编码**（区分左手、右手和物体），使模型能够精细区分不同时间步和不同交互主体的运动特征。

### 阶段三：手部姿态细化

第二阶段生成的运动可能存在手部穿透物体等物理伪影，因此第三阶段引入一个**前馈 Transformer 手部细化网络** $f^{\text{ref}}$ 进行后处理。与扩散生成器不同，$f^{\text{ref}}$ 不涉及扩散机制，也不接收文本等条件输入，仅专注于修正手部姿态。

细化网络的输入包括：
- Text2HOI 生成器输出的手部运动 $\hat{\mathbf{x}}_{0,\text{hand}}$
- 手部关节位置 $\hat{\mathbf{J}}_{\text{hand}}$
- 预测的接触图 $\hat{\mathbf{m}}_{\text{contact}}$
- 变形后的物体点云 $\hat{\mathbf{P}}_{\text{obj}}$
- 基于距离的注意力图

网络输出细化后的手部运动 $\tilde{\mathbf{x}}_{\text{hand}}$，通过组合损失进行训练：
$$L_{\text{refine}} = L_{\text{simple}} + L_{\text{penet}} + \lambda_1 L_{\text{contact}}, \quad \lambda_1 = 5$$

其中 $L_{\text{simple}}$ 为与真值手部运动的 L2 重建损失，$L_{\text{penet}}$ 惩罚手部顶点穿透物体表面的距离，$L_{\text{contact}}$ 鼓励手部关节与物体接触点保持紧密接触。该细化网络在推理时以前馈方式运行，无需测试时优化，在保证物理真实性的同时保持了高效的推理速度。

### 辅助模块

除上述三个核心阶段外，框架还包含两个轻量辅助模块：
- **手类型选择**：利用 CLIP 文本相似度自动判断交互涉及的手类型（仅左手、仅右手或双手）；
- **运动长度预测**：通过一个小型网络根据文本语义预测合适的运动序列长度 $\hat{L}$。

整个框架的设计哲学在于**任务分解与强先验注入**：接触图作为类别无关的几何先验，弥合了文本语义与 3D 物理交互之间的鸿沟；手部细化网络则作为后处理保障，在不增加扩散模型复杂度的前提下提升物理合理性。这一分解策略使得模型能够从有限且未完全泛化的标注数据中学习，并在多个数据集上展现出优于端到端基线方法的性能。

Text2HOI 的整体框架由三个级联的核心模块构成：接触图预测网络、基于扩散的 Text2HOI 运动生成器、以及手部细化网络。以下逐一展开各模块的设计逻辑与关键公式。

### 接触图预测网络

该模块的核心目标是**将文本语义与物体几何解耦**，生成一个与物体类别无关的接触先验。网络 $f^{\text{contact}}$ 接收规范物体网格的归一化点云 $\mathbf{P}_{\text{norm}}$、CLIP 文本特征 $f^{\text{CLIP}}(T)$、物体尺度 $s_{\text{obj}}$ 以及高斯随机噪声向量 $\mathbf{z}_{\text{contact}}$，输出物体表面每个点的接触概率图 $\hat{\mathbf{m}}_{\text{contact}} \in \mathbb{R}^{N \times 1}$ 和物体几何特征 $\mathbf{F}_{\text{obj}} \in \mathbb{R}^{1024}$。这一设计使得接触图仅编码“手可能触碰物体表面的哪些区域”，而不依赖具体物体类别，从而在有限标注数据下学习到可泛化的几何表示。

### Text2HOI 扩散运动生成器

运动生成器 $f^{\text{THOI}}$ 是一个基于 Transformer 编码器的扩散模型，负责从噪声中恢复干净的手-物体运动序列。

**运动表示。** 每一帧的3D运动状态 $\mathbf{x}_0^l$ 包含左手、右手和物体的参数，完整序列表示为 $\mathbf{x}_0 = \{\mathbf{x}_{0,\text{lhand}}^l, \mathbf{x}_{0,\text{rhand}}^l, \mathbf{x}_{0,\text{obj}}^l\}_{l=1}^{L_{\text{max}}}$。

**正向扩散过程。** 遵循 DDPM 范式，将真实运动 $\mathbf{x}_0$ 逐步加噪为 $\mathbf{x}_t$：

$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_t \tag{1}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度系数，$\epsilon_t \sim \mathcal{N}(0, \mathbf{I})$ 为标准高斯噪声。

**反向去噪过程。** 生成器 $f^{\text{THOI}}$ 以加噪运动 $\mathbf{x}_t$、时间步 $t$ 和条件 $c$ 为输入，直接预测干净运动 $\hat{\mathbf{x}}_0$：

$$\hat{\mathbf{x}}_0 = f^{\text{THOI}}(\mathbf{x}_t, t, c)$$

条件 $c$ 聚合了文本特征、接触图 $\hat{\mathbf{m}}_{\text{contact}}$、物体特征 $\mathbf{F}_{\text{obj}}$ 和物体尺度 $s_{\text{obj}}$，通过条件嵌入与时间步嵌入相加后输入 Transformer：$\mathbf{X}_{t,\text{cond}} = \mathbf{X}_{\text{cond}} + t_{\text{emb}}$。

**位置编码。** 与常规仅使用帧级位置编码不同，Text2HOI 同时引入**帧级**和**代理级**（左/右手、物体）位置编码，使模型能区分同一帧内不同代理的运动模式，这是消融实验中证明对准确性和多样性贡献显著的设计。

**训练损失。** 生成器的总损失由三项组成：

$$L_{\text{THOI}}(f^{\text{THOI}}) = L_{\text{diff}}(f^{\text{THOI}}) + L_{\text{dm}}(f^{\text{THOI}}) + L_{\text{ro}}(f^{\text{THOI}}) \tag{4}$$

- **扩散重建损失** $L_{\text{diff}}$：预测运动与真实运动之间的均方误差：

$$L_{\text{diff}}(f^{\text{THOI}}) = \mathbb{E}_{\mathbf{x}_t \sim q(\mathbf{x}_0|c), t \sim [1,T]} \|\mathbf{x}_0 - f^{\text{THOI}}(\mathbf{x}_t, t, c)\|_2^2 \tag{5}$$

- **距离图损失** $L_{\text{dm}}$：仅在手-物体距离小于阈值 $\tau = 2\text{cm}$ 时激活，强制近距离交互区域的预测更精确：

$$L_{\text{dm}}(f^{\text{THOI}}) = \sum \left( (\hat{\mathbf{d}}^i - \mathbf{d}^i) \cdot \mathbb{I}(\mathbf{d}^i < \tau) \right)^2 \tag{6}$$

- **相对方向损失** $L_{\text{ro}}$：惩罚手与物体之间预测相对旋转与真实相对旋转的偏差：

$$L_{\text{ro}}(f^{\text{THOI}}) = \mathbb{1}_{\text{left/right}} \| R(\hat{\mathbf{x}}_{\text{hand}}, \hat{\mathbf{x}}_{\text{obj}}) - R(\mathbf{x}_{\text{hand}}, \mathbf{x}_{\text{obj}}) \|_2^2 \tag{7}$$

后两项几何损失是 Text2HOI 区别于仅使用简单 L2 重建的基线方法的关键，消融实验证实移除它们会导致手-物体交互质量显著下降。

### 手部细化网络

扩散生成器输出的手部运动仍可能存在穿透物体或接触不紧密等瑕疵。手部细化网络 $f^{\text{ref}}$ 是一个**前馈 Transformer**，不涉及扩散机制，也不接收文本等条件输入，仅对手部运动进行局部修正。

**输入与输出。** 细化网络接收 Text2HOI 输出的手部运动 $\hat{\mathbf{x}}_{0,\text{hand}}$、手部关节 $\hat{\mathbf{J}}_{\text{hand}}$、预测接触图 $\hat{\mathbf{m}}_{\text{contact}}$、变形后的物体点云 $\hat{\mathbf{P}}_{\text{obj}}$ 以及基于距离的注意力图，输出细化后的手部运动 $\tilde{\mathbf{x}}_{\text{hand}}$。

**训练损失。** 细化网络的总损失结合了简单重建、穿透惩罚和接触鼓励：

$$L_{\text{refine}}(f^{\text{ref}}) = L_{\text{simple}}(f^{\text{ref}}) + L_{\text{penet}}(f^{\text{ref}}) + \lambda_1 L_{\text{contact}}(f^{\text{ref}}), \quad \lambda_1 = 5 \tag{8}$$

- **简单重建损失** $L_{\text{simple}}$：细化后手部运动与真实值的 L2 距离：

$$L_{\text{simple}}(f^{\text{ref}}) = \| \tilde{\mathbf{x}}_{\text{hand}} - \mathbf{x}_{\text{hand}} \|_2^2 \tag{9}$$

- **穿透损失** $L_{\text{penet}}$：惩罚手部顶点 $\tilde{v}_{\text{hand}}$ 穿透物体表面 $\hat{p}_{\text{obj}}$ 的距离：

$$L_{\text{penet}} = \mathbb{1}_{\text{left/right}} \| d(\tilde{v}_{\text{hand}}, \hat{p}_{\text{obj}}) \|^2 \tag{10}$$

- **接触损失** $L_{\text{contact}}$：鼓励靠近物体表面的手部关节 $\tilde{j}_{\text{hand}}$ 与物体接触点 $\hat{c}_{\text{obj}}$ 保持紧密接触：

$$L_{\text{contact}} = \mathbb{1}_{\text{left/right}} \| d(\tilde{j}_{\text{hand}}, \hat{c}_{\text{obj}}) \|^2 \tag{11}$$

消融实验表明，移除细化网络或其穿透/接触损失会导致物理真实性大幅下降；同时，该前馈细化器在推理速度（约 0.013s）和物理真实性上均优于基于扩散的细化方案。

![[assets/figures/papers/paper_list_l1726_Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction/figures/003_Figure_3.jpg]]
*Figure 3: The details of the text-to-3D hand-object motion generation in our framework. In the forward process, we generate the noised motion*

## 实验与关键发现

### 核心实验设置与评估维度

Text2HOI在三个公开数据集上进行了系统评估：**H2O**、**GRAB**和**ARCTIC**。评估维度覆盖运动质量、多样性和物理真实性三个层面：

- **运动质量**：采用Accuracy（top-3检索准确率）和FID（Fréchet Inception Distance）衡量生成运动与真实分布的接近程度。
- **多样性与多模态性**：使用Diversity和Multimodality指标评估生成结果的丰富度。
- **物理真实性**：通过穿透深度、接触一致性等几何度量量化手-物体交互的物理合理性。

基线方法包括**T2M**（Text2Motion，文本到运动生成的经典方法）、**MDM**（Motion Diffusion Model，基于扩散的人体运动生成方法）和**IMOS**（Interaction Motion for Objects and Scenes，动作标签引导的全身-物体交互生成方法）。所有基线均按统一方案调整输出维度以适应双手+物体的表示格式，并使用预估计或固定长度，确保比较的公平性。

### 主实验结果

Table 1汇总了Text2HOI与基线方法在三个数据集上的全面对比。总体而言，Text2HOI在所有数据集上均取得了最优或极具竞争力的结果。

**H2O数据集**上，Text2HOI的Accuracy（top-3）达到0.8295 ± 0.0015，相较T2M的0.6463 ± 0.0014提升了**18.3个百分点**；FID降至0.1744 ± 0.0013，较IMOS的0.2945降低了**0.12以上**，表明生成质量与分布匹配度显著优于所有基线。

**GRAB数据集**上，物理真实性指标达到0.8839 ± 0.0005，验证了接触图先验和手部细化模块对物理合理性的关键贡献。GRAB包含更丰富的手-物体交互动作类别，Text2HOI在该数据集上的优势进一步证实了框架的泛化能力。

**ARCTIC数据集**上，Accuracy（top-3）达到0.9205 ± 0.0012，再次领先所有对比方法。ARCTIC以双手操作场景为主，表明框架对双手协同交互的建模同样有效。

定性对比中（Figure 4），Text2HOI生成的手部姿态与物体的接触关系明显优于基线方法：T2M和MDM的生成结果常出现穿透或手-物体脱离现象，IMOS虽能生成全局合理的运动但局部接触细节不足，而Text2HOI在接触准确性和运动流畅性上均表现更优。

![[assets/figures/papers/paper_list_l1726_Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction/figures/006_Figure_4.jpg]]
*Figure 4: We compare our generated hand-object motions with other baselines’ results. Each row show the results of Text2Motion [8], MDM [27], IMOS [6], and ours*

### 消融实验

Table 2在GRAB数据集上系统消融了各核心组件的贡献。

**位置编码的作用**：同时移除帧级和代理级位置编码后，Accuracy从0.9218骤降至0.8294，降幅超过9个百分点。这表明区分不同帧和不同代理（左手、右手、物体）的位置信息对Transformer编码器理解运动时序结构和多代理关系至关重要。仅保留单一类型位置编码时性能亦有明显下降，验证了双重编码设计的必要性。

**几何损失的贡献**：移除距离图损失（$L_{\mathrm{dm}}$）和相对方向损失（$L_{\mathrm{ro}}$）后，手-物体交互质量显著下降。$L_{\mathrm{dm}}$仅在距离小于阈值$\tau = 2\mathrm{cm}$时激活，促使模型在近距离交互区域产生更精确的预测；$L_{\mathrm{ro}}$则直接监督手与物体之间的相对旋转关系，两者互补地增强了3D空间理解。

**接触图与物体尺度条件**：移除接触图条件$\mathbf{m}_{\mathrm{contact}}$和物体尺度条件$s_{\mathrm{obj}}$后，手部姿态的适宜性明显降低。接触图作为类别无关的几何先验，为扩散模型提供了物体表面哪些区域应被手部接触的强引导；物体尺度信息则帮助模型适应不同大小的物体，两者共同构成了任务分解设计的核心优势。

**手部细化网络**：完整的Text2HOI（含细化网络）与“Ours w/o $f^{\mathrm{ref}}$”的对比显示，细化网络对物理真实性有决定性贡献。进一步消融穿透损失$L_{\mathrm{penet}}$和接触损失$L_{\mathrm{contact}}$后，物理真实性大幅下降，证实了这两项损失在消除穿透和改善接触方面的关键作用。

**细化器设计对比**：Table S1比较了不同细化器设计，本文的前馈Transformer细化器在物理真实性和推理速度上均优于基于扩散的细化方法。Table S2显示前馈细化器的推理时间仅需**0.013秒**，远快于扩散细化方案，实现了质量与效率的双重优势。

### 泛化性分析

Figure 5展示了Text2HOI在训练集未见过的物体上的生成结果与对应的预测接触图。第一、二行为训练中见过的物体，第三、四行为未见过的物体。结果表明，接触预测网络对物体类别不敏感的特性使其能够为未见物体生成合理的接触图，进而引导运动生成模块产生物理上合理的交互运动。这一泛化能力源于接触图预测仅依赖物体的局部几何信息（通过PointNet提取的点云特征），而非物体类别标签。

### 失败模式与局限性

尽管Text2HOI在多个维度上表现优异，分析仍揭示了若干局限：

1. **力交互建模缺失**：当前方法仅考虑手与物体之间的相对3D位置和接触几何，未显式建模力交互（如抓取力度、物体重量对手部姿态的影响），可能导致某些需要力度感知的精细操作场景下物理真实性不足。

2. **非刚性物体泛化未充分验证**：接触图预测依赖规范物体网格作为输入，对于高度非刚性或复杂拓扑的物体（如布料、软体），当前框架的泛化能力尚未经过系统测试。

3. **文本标注规模受限**：文本标签通过人工增强现有数据集获得，标注的规模和多样性受限于原始数据集的覆盖范围，可能未能涵盖所有交互类型，尤其在长尾交互类别上可能存在性能下降。

4. **动态场景扩展挑战**：框架目前针对单一物体交互设计，拓展至多物体或动态场景时，如何在保持交互合理性的同时处理物体间的遮挡和协同关系仍是一个开放问题。

![[assets/figures/papers/paper_list_l1726_Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction/figures/004_Table_1.jpg]]
*Table 1: Comparison on H2O, GRAB, and ARCTIC datasets. † denotes our produced results. → denotes that the higher value of the metric, the closer to the GT distribution. Best results are emphasized in bold*

![[assets/figures/papers/paper_list_l1726_Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction/figures/005_Table_2.jpg]]
*Table 2: Ablation study on the positional encoding, losses, and conditions for ‘Ours w/o*

![[assets/figures/papers/paper_list_l1726_Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction/figures/013_Table.jpg]]
*Table: S1. Comparative physical realism scores for the different refiner designs*

## 定位与知识库关联

### 任务域与核心瓶颈

Text2HOI 定位于**文本引导的3D手‑物体交互运动生成**，其直接任务域介于文本‑运动生成（text‑to‑motion）与手‑物体交互建模（hand‑object interaction modeling）之间。与纯人体运动生成不同，手‑物体交互面临双重约束：语义层面需对齐文本描述，物理层面需保证手与物体之间无穿透且接触合理。现有3D手‑物体交互数据集（如H2O、GRAB、ARCTIC）在交互类型和物体类别上远未泛化，且缺乏对应文本标签，这构成该任务的核心瓶颈——**从有限且稀疏标注的数据中学习从文本到物理合理交互的映射极其困难**。

### 与基线方法的差异化设计

Text2HOI 与三类代表性基线方法形成对比：

- **T2M (Text2Motion)**：面向人体运动的文本‑运动生成方法，直接适配至手‑物体交互场景。T2M 仅依赖文本条件，缺乏对物体几何和接触关系的显式建模，导致生成的手部姿态与物体交互质量较差（H2O数据集上 Accuracy top‑3 仅 0.6463，而 Text2HOI 达到 0.8295）。

- **MDM (Motion Diffusion Model)**：基于扩散的人体运动生成方法，同样适配至手‑物体交互。MDM 虽采用扩散框架，但未引入接触图先验和物体几何特征，生成的交互运动在物理合理性上明显弱于 Text2HOI（定性对比见 Figure 4）。

- **IMOS (Interaction Motion for Objects and Scenes)**：动作标签引导的全身‑物体交互生成方法。IMOS 考虑了物体交互，但其条件为离散动作标签而非自由文本，且缺乏对接触几何的精细建模。在 H2O 数据集上，Text2HOI 的 FID 指标（0.1744）显著优于 IMOS（0.2945）。

Text2HOI 的核心差异化在于**将交互生成任务分解为接触图生成和运动生成两个子任务**，并利用接触图作为运动生成的强先验。这一分解设计的因果逻辑是：接触图预测网络（基于VAE，以文本、规范物体网格和物体尺度为输入）产出的接触概率图提供了**类别无关的局部几何先验**，使后续的扩散运动生成器（Transformer编码器架构）能够从有限增强数据中学习到泛化能力强的通用表示，而非过拟合于特定物体或交互类型。

### 方法谱系中的继承与创新

Text2HOI 继承并改进了多个技术线索：

| 技术组件 | 继承来源 | Text2HOI 的创新/改进 |
|---------|---------|---------------------|
| 扩散运动生成框架 | DDPM / MDM 等扩散模型 | 引入接触图、物体几何特征和物体尺度作为多模态条件，替代纯文本条件 |
| Transformer编码器架构 | 序列建模中的标准Transformer | 提出**帧级+代理级双重位置编码**，区分时间维度和手/物体代理身份 |
| 手部细化 | 后处理优化思路 | 设计**前馈Transformer细化网络**，结合穿透损失和接触损失，无需测试时优化，推理速度（0.013s）远快于基于扩散的细化方法 |
| 几何损失函数 | 3D重建中的距离/方向约束 | 引入**距离图损失**（仅在手‑物体距离<2cm时激活）和**相对方向损失**，增强近距离交互的几何精度 |

消融实验（Table 2）系统验证了各组件的独立贡献：去除帧级和代理级位置编码后，GRAB数据集上的准确性从 0.9218 骤降至 0.8294；移除距离图损失和相对方向损失导致手‑物体交互质量显著下降；移除接触图条件和物体尺度条件则降低了手部姿态的适宜性。

### 适用边界与局限性

1. **力交互建模缺失**：当前方法仅考虑手与物体之间的相对3D位置和接触几何，未建模两者之间的力交互（如抓握力度、摩擦力）。这限制了生成运动在需要精细力控制的场景（如拧开瓶盖、捏取小物体）中的物理真实性。

2. **对规范物体网格的依赖**：虽然接触图预测对物体类别不敏感，但仍需规范物体网格作为输入。对于高度非刚性物体（如布料、软体）或拓扑复杂物体，接触图预测的质量和泛化性未经充分测试。

3. **文本标注的规模瓶颈**：文本标注通过人工增强现有数据集获得，标注的规模和多样性受限于原数据集。在更极端的低资源场景下，框架能否保持性能尚不明确。

4. **场景复杂度受限**：当前框架针对单物体交互设计，未涉及多物体、动态障碍物或场景上下文下的手‑物体交互生成。

### 开放问题与后续方向

- **力交互的显式建模**：如何在生成过程中引入手‑物体之间的力反馈，以提升需要精细力控制的交互质量？
- **多物体与动态场景扩展**：能否将框架从单一物体扩展到多物体或动态场景，并保持交互的时空一致性？
- **低资源学习**：如何在更极端缺乏标注数据的情况下，利用自监督或预训练策略进一步减轻对文本标签的依赖？
- **非刚性物体泛化**：接触图预测网络能否通过对非刚性形变建模，扩展至衣物、绳索等柔性物体的交互生成？

## 原文 PDF

![[paperPDFs/CVPR_2024/Text2HOI_Text_guided_3D_Motion_Generation_for_Hand_Object_Interaction.pdf]]

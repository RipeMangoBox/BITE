---
title: "PersonaHOI: Effortlessly Improving Personalized Face with Human Object Interaction Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_Interaction_Generation.pdf
project_link: null
code_link: https://github.com/JoyHuYY1412/PersonaHOI
aliases:
- PersonaHOI
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过额外引入一个StableDiffusion分支并与PFD分支以空间掩模引导的方式在注意力、潜在空间和跳过连接中合并，将交互布局从SD转移到PFD，同时限制PFD的身份特征仅作用于面部区域。
primary_logic: 利用SD分支从文本提示生成初始的HOI布局图像，并通过头部掩模分割出面部区域，从而指导PFD分支只关注面部细节的生成，而非面部区域直接采用SD的交互内容，实现无训练的即插即用融合。
claims:
- PFD模型在早期注入身份时保留面部但缺乏交互，延迟注入则身份漂移。
- PersonaHOI在FastComposer上提升交互对齐20.69%，PhotoMaker上提升19.24%。
- 定性结果显示出缺失物体或身体部位，而PersonaHOI生成自然交互。
- 消融实验表明三个组件（CAC, LM, RM）的必要性，缺一不可。
---

# PersonaHOI: Effortlessly Improving Personalized Face with Human Object Interaction Generation

> [!tip] 核心洞察
> 利用SD分支从文本提示生成初始的HOI布局图像，并通过头部掩模分割出面部区域，从而指导PFD分支只关注面部细节的生成，而非面部区域直接采用SD的交互内容，实现无训练的即插即用融合。

| 字段 | 内容 |
|------|------|
| 中文题名 | PersonaHOI：轻松提升个性化人脸与人物-物体交互生成 |
| 英文题名 | PersonaHOI: Effortlessly Improving Personalized Face with Human Object Interaction Generation |
| 会议/期刊 | CVPR 2025 |
| Links |  [Code](https://github.com/JoyHuYY1412/PersonaHOI)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PersonaHOI |
| Dataset | HOI-Specific Personalized Face Generation, General Personalized Face Generation, Image Quality |

> [!tip] 效果简介
> - HOI-Specific Personalized Face Generation (FastComposer) 上，Interaction Alignment (%) 56.65 vs 35.96 (+20.69)。
> - HOI-Specific Personalized Face Generation (PhotoMaker) 上，Interaction Alignment (%) 76.01 vs 56.77 (+19.24)。
> - HOI-Specific Personalized Face Generation (IP-Adapter) 上，Interaction Alignment (%) 68.30 vs 49.83 (+18.47)。

## 概要

个性化人脸生成（Personalized Face Generation）旨在从单张参考图像中提取身份特征，并在多样化场景中保持身份一致性。然而，现有个性化人脸扩散模型（PFD）在面向人脸数据集的微调后，丧失了遵循复杂人物-物体交互（Human-Object Interaction, HOI）文本提示的能力，导致生成的肖像缺乏全身连贯性和交互性。预训练的 StableDiffusion 虽具备该能力，但无法保持身份一致性。这一瓶颈的根本原因在于：PFD 模型的身份特征被注入到整个图像空间，挤占了身体和物体的生成容量，而延迟注入身份虽能释放空间，却导致身份漂移（Figure 2b）。

PersonaHOI 提出了一种训练自由、即插即用的框架，将通用 StableDiffusion（SD）分支与 PFD 模型融合，以解决上述矛盾。其核心洞察是：利用 SD 分支从文本提示生成初始的 HOI 布局图像，通过头部掩模分割出面部区域，从而指导 PFD 分支仅关注面部细节的生成，而非面部区域则直接继承 SD 的交互内容。该方法通过三个关键模块实现这一目标——交叉注意力约束（CAC）将身份注意力限制在头部区域，潜在合并（LM）在潜空间按掩模融合面部身份与交互布局，残差合并（RM）在 U-Net 跳过连接中结合高频身份细节与低频交互结构。

实验表明，PersonaHOI 在 HOI 特定生成任务上显著提升交互对齐：FastComposer 提升 20.69%，PhotoMaker 提升 19.24%，IP-Adapter 提升 18.47%（Table 1）。在通用个性化生成任务上，身份保存和图像质量也获得一致改善。消融实验证实 CAC、LM、RM 三个组件缺一不可（Table 3），且低通-高通（Low-High）滤波器配置和递减核策略（2.5 → 0.5）达到最佳平衡（Figure 7, Table 6）。

### 个性化人脸生成与人物-物体交互的冲突

扩散模型在文本到图像生成领域取得了显著进展，尤其是在个性化人脸生成（Personalized Face Generation）方面。当前主流的个性化人脸扩散模型（PFD），如 **FastComposer** 和 **IP-Adapter**，通过将身份特征注入到扩散过程中，能够从单张参考图像生成保持身份一致的人脸图像。然而，这些模型存在一个根本性的瓶颈：由于它们通常在面向人脸的数据集上进行微调或训练，其空间布局先验被过度约束在人脸区域，导致模型丧失了遵循复杂人物-物体交互（Human-Object Interaction, HOI）文本提示的能力。

具体而言，当用户给出如“一个人在烹饪食物”或“一个人抱着猫”这类需要全身连贯性和物体交互的提示时，PFD 模型往往只能生成一张人脸，而忽略身体、物体以及人-物之间的空间关系。相比之下，预训练的 **StableDiffusion**（SD）模型在文本到图像生成中展现出强大的HOI布局生成能力，能够从文本提示中生成连贯的人物-物体交互场景，但它无法保持特定人物的身份一致性。因此，**身份保持**与**交互连贯性**之间存在一个明显的张力，构成了该领域的核心挑战。

### 身份注入时机的困境

Figure 2(b) 的分析揭示了 PFD 模型中身份注入时机对生成质量的影响。实验表明，在扩散过程的早期步骤注入身份特征（如 FastComposer 的默认策略）能够保留面部细节，但会导致生成结果缺乏连贯的HOI交互——模型倾向于只生成人脸而忽略身体和物体。相反，延迟身份注入虽然为交互布局的生成留出了空间，但身份特征会持续漂移，最终生成随机的人脸特征，丧失身份一致性。这一观察表明，**仅靠调整身份注入时机无法同时满足身份保持和交互生成的需求**，需要一种更根本的架构级解决方案。

### 核心洞见：空间布局引导的身份-交互解耦

PersonaHOI 的核心洞见来源于对 SD 和 PFD 模型各自优势的重新审视。如 Figure 2(a) 所示，SD 分支能够从文本提示中生成具有连贯HOI布局的初始图像，其中包含了人体的整体姿态、物体的位置以及人-物之间的空间关系。这一布局信息可以通过头部掩模分割（如 DensePose）被显式地提取出来，从而将图像空间划分为面部区域和非面部区域。

基于此，PersonaHOI 提出了一种**无训练、即插即用**的融合策略：利用 SD 分支生成HOI布局，并通过空间掩模引导的方式，将 PFD 分支的身份特征**仅作用于面部区域**，而非面部区域则直接采用 SD 分支生成的交互内容。这一策略从根本上解耦了身份保持和交互生成两个任务，使得 PFD 模型无需牺牲其身份保持能力，即可获得 SD 模型的HOI生成能力。

## 核心方法与创新机理

### 问题诊断：PFD 模型的身份–交互两难

现有个性化人脸扩散模型（PFD，如 **FastComposer**、**IP-Adapter**、**PhotoMaker**）在面向人脸数据集的微调过程中，丧失了遵循复杂人物-物体交互（HOI）文本提示的能力。其症结在于：身份特征的注入时机与空间作用范围存在根本性冲突。如 Figure 2(b) 所示，在去噪早期注入身份嵌入虽能保留面部细节，却导致模型忽略身体与物体的交互生成；延迟注入虽释放了交互空间，却引发严重的身份漂移，生成随机人脸特征。这揭示了一个关键瓶颈——PFD 模型的身份表征占据了整个潜空间，挤占了身体与物体的布局容量，而预训练的 StableDiffusion（SD）虽具备出色的 HOI 生成能力，却无法保持身份一致性。

### 核心洞察：以空间掩模引导的双分支解耦

PersonaHOI 的核心洞察在于：**将身份生成与交互生成解耦到两个独立分支，并通过空间掩模在注意力、潜在空间和跳过连接三个层级进行引导式融合**。具体而言，SD 分支负责从文本提示中生成初始的 HOI 布局图像，经 DensePose 分割出头部掩模后，该掩模作为空间约束信号，指导 PFD 分支仅将身份特征作用于面部区域，而非面部区域则直接继承 SD 的交互内容。这一设计将“谁生成什么”的空间决策从模型内部学习转移到外部掩模引导，实现了无需训练、即插即用的身份–交互协调。

### 三个关键 changed slots

#### Slot 1：身份特征空间作用范围——从全图到仅头部区域

| 维度 | 基线方法 | PersonaHOI |
|------|---------|------------|
| 作用范围 | 全图像（PFD 模型在整个潜空间均匀注入身份） | 仅头部区域（通过交叉注意力约束 CAC 和头部掩模限制） |
| 证据锚点 | Section 4.2, "CAC restricts identity features to specific facial regions" | 置信度：0.95 |

基线 PFD 模型在交叉注意力层中，参考图像的图像标记（image token）会与所有空间位置的查询向量计算注意力，导致身份特征向全身扩散，挤占了物体与身体的特征空间。PersonaHOI 引入**交叉注意力约束（CAC）**，将头部掩模 $M^{head}$ 应用于注意力图：

$$M_{i \in [0,1,\dots,N-1]}^{CAC} = \begin{cases} \text{Hatten}(M^{head}), & \text{if } i = img, \\ 1, & \text{otherwise} \end{cases}$$

$$A^{CAC} = A \odot (M^{CAC})^{\top}$$

其中 $i = img$ 对应参考图像的图像标记，$\text{Hatten}$ 将头部掩模展平为一维向量。该操作将图像标记的注意力严格限制在头部区域内，面部以外的空间位置被归零，从而为身体和物体的交互生成释放了充足的容量。这一约束仅在 PFD 分支中生效，SD 分支保持完整的文本条件化能力。

#### Slot 2：非面部区域生成源——从 PFD 自身到 SD 布局转移

| 维度 | 基线方法 | PersonaHOI |
|------|---------|------------|
| 生成源 | PFD 模型自身（倾向于生成人脸或忽略身体/物体） | SD 分支生成的布局（通过潜在合并和残差合并集成） |
| 证据锚点 | Section 4.3, 4.4 | 置信度：0.95 |

基线 PFD 模型在非面部区域缺乏有效的生成引导，常出现缺失物体、身体部位不完整或交互语义错误的问题（Figure 5）。PersonaHOI 通过两个互补的合并机制将 SD 的交互布局转移到 PFD 中：

- **潜在合并（LM）**：在每一步去噪中，按头部掩模在潜空间逐元素合并两个分支的潜变量：

$$z_t = M^{head} \odot z_t^{PFD} + (1 - M^{head}) \odot z_t^{SD}$$

面部区域取 PFD 的身份潜变量，非面部区域取 SD 的交互潜变量，实现了空间上的硬性分工。

- **残差合并（RM）**：在 U-Net 的跳过连接层中，利用频率域的互补性进行融合：

$$R_{merged}^l = M_R^l \odot HP(R_{PFD}^l) + (1 - M_R^l) \odot LP(R_{SD}^l)$$

其中 $HP(\cdot)$ 为高通滤波器，提取 PFD 残差中的高频身份细节（如面部纹理、边缘）；$LP(\cdot)$ 为低通滤波器，提取 SD 残差中的低频交互布局（如身体姿态、物体轮廓）。消融实验（Figure 7）验证了 Low-High 配置（SD 低通 + PFD 高通）在所有六种组合中取得最佳平衡，直接替换（Replace）或无滤波合并（NoFilter）均导致身份或交互质量的显著下降。

#### Slot 3：架构分支——从单分支到双分支并行去噪

| 维度 | 基线方法 | PersonaHOI |
|------|---------|------------|
| 分支结构 | 单一 PFD 模型（如 FastComposer） | 双分支：PFD + SD，在同一潜空间并行去噪 |
| 证据锚点 | Section 4.1, Figure 3 | 置信度：0.95 |

基线方法仅使用一个扩散模型同时承担身份保持和文本遵循双重任务，二者在参数空间内形成竞争。PersonaHOI 将架构扩展为双分支：SD 分支接收文本提示生成 HOI 布局，PFD 分支从参考图像注入身份特征，二者从同一噪声潜变量 $z_T$ 出发，在每一步去噪后通过 LM 和 RM 进行融合。这种设计的关键在于**保持两个分支的独立性**——SD 分支不受身份特征干扰，PFD 分支的身份注意力被 CAC 空间约束——仅在合并点进行信息交换，从而避免了任务间的负迁移。

### 创新点的因果链条

三个 changed slots 构成了一条完整的因果链条：CAC 解决了“身份特征往哪里放”的空间分配问题，LM 和 RM 解决了“非面部区域从哪获取内容”的信息来源问题，双分支架构则为二者提供了独立运行的载体。消融实验（Table 3）验证了这一链条的不可分割性：完整模型（CAC+LM+RM）在 FastComposer 上达到身份保存 55.28%、交互对齐 56.65%；移除 LM 或 RM 均导致两项指标显著下降；仅保留 CAC 而移除合并模块时，身份保存虽有所回升，但交互对齐骤降至接近基线水平，表明空间约束本身不足以完成布局转移，三个组件缺一不可。

### 与现有方法的本质区别

与需要针对特定身份或交互类别进行微调的现有方法不同，PersonaHOI 是一种**训练自由、调优自由**的即插即用框架。其创新不在于提出新的扩散架构或损失函数，而在于发现并利用了两个现有模型（PFD 和 SD）之间的空间互补性，通过三个轻量级的掩模引导融合策略，在不修改任何预训练权重的前提下，将 SD 的交互布局能力“嫁接”到 PFD 的身份保持能力之上。这一范式使得 PersonaHOI 可以无缝兼容 FastComposer、IP-Adapter、PhotoMaker 等多种 PFD 模型及其对应的 SD 架构，展现出极强的通用性。

PersonaHOI 的整体设计围绕一个核心矛盾展开：个性化人脸扩散模型（PFD）在微调后丧失了遵循复杂人物-物体交互（HOI）文本提示的能力，而预训练的 Stable Diffusion（SD）虽具备该能力，却无法保持身份一致性。为解决这一问题，PersonaHOI 提出了一种**训练自由、即插即用**的双分支并行去噪框架，将 PFD 模型的身份保持能力与 SD 分支的交互布局生成能力进行结构化融合。

### 框架总览

整体架构如 Figure 3 所示，包含两个并行的扩散分支和一个引导融合的头部掩模模块：

1. **Stable Diffusion（SD）分支**：接收完整的 HOI 文本提示，从噪声潜变量 $z_T$ 出发进行去噪，生成包含人物-物体交互布局的图像 $I_{SD}$。该分支负责提供全局的交互上下文和空间布局信息。

2. **个性化人脸扩散（PFD）分支**：从参考图像中提取身份特征，在相同的初始噪声 $z_T$ 上并行去噪。该分支专注于保持面部身份一致性，但其自身缺乏生成连贯身体和交互物体的能力。

3. **头部掩模分割模块**：利用 DensePose 对 SD 分支生成的图像 $I_{SD}$ 进行头部区域分割，得到头部掩模 $M^{head}$。该掩模作为后续所有融合操作的空间引导信号，决定了身份特征和交互特征的边界。

### 三阶段工作流

框架的执行分为三个有序阶段，体现了从全局布局到局部细节的渐进式融合策略：

**阶段一：布局生成与掩模提取。** SD 分支首先从文本提示生成完整的 HOI 布局图像，并通过 DensePose 分割出头部掩模。这一步的核心作用在于：利用 SD 对复杂文本的理解能力，为后续融合提供可靠的空间参考。Figure 2(a) 的分析表明，SD 的空间布局是引导 PFD 生成连贯交互的关键。

**阶段二：并行去噪与逐步融合。** SD 和 PFD 分支从相同的 $z_T$ 出发，在每一个去噪时间步 $t$ 执行三个融合操作：

- **交叉注意力约束（CAC）**：在 PFD 分支的交叉注意力层中，利用头部掩模将身份特征的注意力严格限制在面部区域，释放非面部区域的空间容量用于交互生成。
- **潜在合并（LM）**：在潜空间按掩模合并两个分支的潜变量，面部区域采用 PFD 的特征，其他区域采用 SD 的特征。
- **残差合并（RM）**：在 U-Net 的跳跃连接层中，对 PFD 残差应用高通滤波以保留高频身份细节，对 SD 残差应用低通滤波以提取低频交互布局，然后将二者按掩模合并。

**阶段三：迭代去噪至最终图像。** 上述融合在每一个时间步重复执行，从 $t=T$ 到 $t=0$，逐步将交互上下文注入个性化人脸生成过程，最终输出身份一致且交互连贯的图像。

### 设计逻辑

该框架的设计体现了三个关键洞察：

- **空间解耦**：将面部身份和非面部交互在空间上解耦，通过头部掩模实现精确的边界控制，避免了身份特征对交互区域的“污染”和交互特征对面部身份的“漂移”。
- **频域分离**：在残差合并中引入频域分离策略，利用高通/低通滤波器分别提取 PFD 的身份细节和 SD 的交互布局，实现了不同频率成分的结构化融合。
- **训练自由**：所有融合操作均作为推理时的即插即用模块，无需对 PFD 或 SD 模型进行任何微调，保证了框架的通用性和实用性。

### 模块关系

三个核心模块之间存在明确的依赖与互补关系。CAC 是基础约束层，在注意力层面限制身份特征的作用范围；LM 是潜空间融合层，在全局层面完成面部与非面部区域的合并；RM 是细节增强层，在跳跃连接中补充高频身份细节。消融实验（Table 3）表明，三个组件缺一不可：移除任一组件都会导致身份保存或交互对齐的显著下降。

### 问题形式化

给定一张参考人脸图像和一段描述人物-物体交互（HOI）的文本提示，目标是在保持身份一致性的前提下生成具有连贯交互的全身肖像。现有 PFD 模型（如 **FastComposer**、**IP-Adapter**、**PhotoMaker**）在面向人脸数据集微调后，丧失了遵循复杂 HOI 文本提示的能力（Figure 2b），而预训练的 StableDiffusion（SD）虽具备交互生成能力，却无法保持身份一致性。

PersonaHOI 的核心洞察是：SD 分支从文本提示生成初始的 HOI 布局图像，通过头部掩模分割出面区域，从而指导 PFD 分支只关注面部细节生成，而非面部区域直接采用 SD 的交互内容，实现无训练的即插即用融合。

### 预备知识：扩散模型与交叉注意力

StableDiffusion 在潜空间中进行迭代去噪。给定噪声潜变量 $\mathbf{z}_T$，每一步去噪过程为：

$$\mathbf{z}_{t-1} = \mathrm{Denoise}(\mathbf{z}_t, \epsilon(\mathbf{z}_t, t, \mathbf{C}); \theta)$$

其中 $\mathbf{C}$ 为文本条件嵌入，$\theta$ 为模型参数。在 U-Net 的交叉注意力层中，潜变量 $\mathbf{z}$ 通过线性投影生成 Query $\mathbf{Q}$，文本条件 $\mathbf{C}$ 生成 Key $\mathbf{K}$ 和 Value $\mathbf{V}$：

$$\mathbf{Q} = \mathbf{W}_q \mathbf{z},\quad \mathbf{K} = \mathbf{W}_k \mathbf{C},\quad \mathbf{V} = \mathbf{W}_v \mathbf{C}$$

$$\mathbf{A} = \mathrm{Softmax}\left(\frac{\mathbf{Q} \mathbf{K}^\top}{\sqrt{d}}\right),\quad \mathbf{z}_{\mathrm{attn}} = \mathbf{A} \mathbf{V}$$

PFD 模型在此框架中额外注入参考人脸特征作为条件，但该特征通常作用于整个潜空间，导致面部身份信息侵占身体和物体的生成空间。

### 核心模块一：交叉注意力约束（CAC）

**瓶颈**：PFD 模型的身份特征通过交叉注意力均匀注入全图，挤压了非面部区域的交互生成空间。

**机制**：CAC 利用 SD 分支预生成的头部掩模 $M^{head}$，将 PFD 中图像标记（img token）的注意力严格限制在面部区域内。具体地，对注意力图施加掩模约束：

$$M_{i \in [0,1,\dots,N-1]}^{CAC} = \begin{cases} \mathsf{Hatten}(M^{head}), & \mathrm{if~} i = img, \\ 1, & \mathrm{otherwise} \end{cases}$$

$$A^{CAC} = A \odot (M^{CAC})^{\top}$$

其中 $\mathsf{Hatten}$ 为展平操作，$\odot$ 为逐元素乘法。对于图像标记（$i = img$），其注意力被约束在头部区域；对于文本标记，注意力不受限制。这确保了身份特征仅作用于面部，为身体和物体的交互保留充分的生成空间。

### 核心模块二：潜在合并（LM）

**瓶颈**：PFD 分支独立去噪时，非面部区域缺乏交互布局引导；SD 分支独立去噪时，面部区域缺乏身份细节。

**机制**：LM 在每一步去噪 $t$ 处，利用头部掩模 $M^{head}$ 在潜空间中融合两个分支的特征：

$$z_t = M^{head} \odot z_t^{PFD} + (1 - M^{head}) \odot z_t^{SD}$$

面部区域（$M^{head}=1$）采用 PFD 的潜变量以保留身份细节，非面部区域（$M^{head}=0$）采用 SD 的潜变量以继承交互布局。该融合在每个去噪步执行，确保两个分支在统一的潜空间中协同演化。

### 核心模块三：残差合并（RM）

**瓶颈**：U-Net 的跳过连接（skip connections）传递多尺度细节信息，直接使用 PFD 或 SD 的单分支残差会导致信息丢失或冲突。

**机制**：RM 在 U-Net 的每个残差层中，利用头部掩模 $M_R^l$ 引导 PFD 和 SD 残差特征的频率选择性融合。PFD 残差经过高通滤波器（HP）提取身份细节（高频），SD 残差经过低通滤波器（LP）提取交互布局（低频）：

$$R_{merged}^l = M_R^l \odot HP(R_{PFD}^l) + (1 - M_R^l) \odot LP(R_{SD}^l)$$

融合后的残差 $R_{merged}^l$ 与 PFD 瓶颈特征拼接，传入解码路径。消融实验（Figure 7）验证了 Low-High 配置（SD 低通、PFD 高通）在所有六种滤波器组合中取得最佳的全局平衡，直接替换或无滤波融合均导致身份或交互质量的显著下降。

### 模块协同与整体流程

三个模块形成递进式约束链条：**CAC** 在注意力层面限制身份特征的注入范围 → **LM** 在潜空间层面按掩模分配生成职责 → **RM** 在跳过连接层面实现频率域解耦融合。消融实验（Table 3）表明，移除任一模块均导致性能显著下降：缺少 LM 或 RM 时，身份保存和交互对齐均大幅低于完整模型；仅保留 CAC 时交互对齐甚至低于 FastComposer 基线（红色标注），验证了三个组件的必要性。

## 实验与关键发现

### 评估设置与基准

PersonaHOI 被设计为一个即插即用的免训练框架，因此实验的核心逻辑是在多个已有的个性化人脸扩散（PFD）模型上直接叠加本方法，观察交互对齐能力的提升幅度。基线分为两类：纯文本到图像模型（**StableDiffusion v1.5**、**StableDiffusion XL**）作为交互布局的上限参考，以及三个学习型 PFD 模型——**FastComposer**、**IP-Adapter** 和 **PhotoMaker**——作为身份保存能力的基线。评估围绕两个核心维度展开：**交互对齐（Interaction Alignment）**衡量生成图像中人物与物体的交互是否符合文本提示，**身份保存（Identity Preservation）**衡量生成人脸与参考图像的身份一致性。此外，在通用个性化人脸生成任务中，还引入了**提示一致性（Prompt Consistency）**，并按配饰、风格、动作、场景四个类别分别报告（Table 2, Table 4）。图像质量评估采用 FID（越低越好）、ImageReward 和 Aesthetic Score（越高越好）（Table 5）。

![[assets/figures/papers/paper_list_l1743_PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_In/figures/008_Table_2.jpg]]
*Table 2: Comparison of Our Method with FastComposer [34] on General Personalized Face Generation. We compare across four categories of text prompts including Accessory, Style, Action, and Context, following [20, 34]. Results are formatted as “ Identity Preservation (%) / Prompt Consistency (%)” and we bold the higher number for each pair of comparison*

![[assets/figures/papers/paper_list_l1743_PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_In/figures/016_Table_5.jpg]]
*Table 5: Comparison of image quality on the task of Personalized Face with HOI Generation. Metrics include FID (lower is better), ImageReward (higher is better), and Aesthetic Score (higher is better). We use (red) scripts to denote the performance improvement and (green) scripts for the decrease*

### HOI 特定生成的主结果

Table 1 报告了 HOI 特定个性化人脸生成任务上的核心对比。在 FastComposer 上，PersonaHOI 将交互对齐从 35.96% 提升至 56.65%，绝对增益 **+20.69%**；在 PhotoMaker 上，从 56.77% 提升至 76.01%，增益 **+19.24%**；在 IP-Adapter 上，从 49.83% 提升至 68.30%，增益 **+18.47%**。三个 PFD 基线的交互对齐均获得大幅提升，验证了双分支融合策略的通用性。值得注意的是，纯 SD 模型虽然交互对齐较高，但完全不具备身份保存能力——这正是 PersonaHOI 试图弥合的鸿沟。

![[assets/figures/papers/paper_list_l1743_PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_In/figures/005_Table_1.jpg]]
*Table 1: Comparison of Our Method with Baseline Approaches on HOI-Specific Personalized Face Generation. StableDiffusion serves as the text-only baseline without subject conditioning. PersonaHOI seamlessly incorporates existing Personalized Face Diffusion models (FastComposer [34], IP-Adapter [37], PhotoMaker [17]) with their corresponding StableDiffusion architectures. We bold the higher number for each pair of comparison*

定性结果（Figure 5）进一步揭示了基线的典型失败模式：FastComposer 和 IP-Adapter 在面对“拿着某物”或“与某物交互”的提示时，经常缺失物体或生成不完整的身体部位，而 PhotoMaker 虽然能生成部分交互，但身份一致性明显漂移。PersonaHOI 增强后的版本则能生成自然的人物-物体交互，同时保持面部身份。

![[assets/figures/papers/paper_list_l1743_PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_In/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Examples of PersonaHOI and Baseline Models. Comparison of baseline models (FastComposer [34], IP-Adapter [37], PhotoMaker [17]) and their PersonaHOI-enhanced results for diverse human-object interaction prompts*

### 通用个性化人脸生成

在通用个性化人脸生成任务上（Table 2, Table 4），PersonaHOI 在 FastComposer 上的身份保存均值从 50.95% 提升至 52.84%（+1.89%），提示一致性也有小幅改善。按类别细看，在“动作”和“场景”类别中提升最为显著，这与 HOI 任务中交互布局的引入直接相关；在“配饰”和“风格”类别中，身份保存的提升相对温和，因为这些任务本身对全身交互布局的依赖较弱。定性对比（Figure 9, Figure 10）显示，PersonaHOI 增强后的 PhotoMaker 在“女人遛狗”“女人做饭”等场景中能生成更完整的身体和物体，而基线版本常出现身体截断或物体消失。

### 消融实验：三个核心组件的必要性

Table 3 以 FastComposer 为骨干，逐一移除 Cross-Attention Constraint（CAC）、Latent Merge（LM）和 Residual Merge（RM），验证各组件的独立贡献。完整模型（CAC+LM+RM）达到身份保存 55.28%、交互对齐 56.65%。移除 LM 或 RM 均导致身份保存和交互对齐的显著下降，部分配置甚至低于 FastComposer 基线（表中以红色标注），表明这三个组件缺一不可。CAC 的作用是将身份特征限制在面部区域，为身体和物体的交互腾出空间；LM 在潜空间层面完成面部与交互区域的初步划分；RM 则在 U-Net 跳跃连接中通过频域分离实现精细融合。

![[assets/figures/papers/paper_list_l1743_PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_In/figures/009_Table_3.jpg]]
*Table 3: Effect of Individual Components. We evaluate the contributions of Cross-Attention Constraint (CAC), Latent Merge (LM), and Residual Merge (RM) in PersonaHOI by selectively removing each of them. Experiments are conducted with FastComposer on HOI-specific personalized face generation. Red numbers denote the performance lower than FastComposer [34] baseline*

### 残差合并中的频域策略

Figure 7 和 Table 6 对残差合并中的滤波器配置进行了深入消融。六种配置中，**Low-High 配置**（对 SD 分支施加低通滤波以提取交互布局的低频信息，对 PFD 分支施加高通滤波以保留身份细节的高频信息）在身份保存和交互对齐之间取得了最佳平衡。直接替换（Replace）或不使用滤波器（NoFilter）均导致身份漂移或交互缺失。在高斯核尺寸的消融中（Table 6），递减核策略（从 2.5 递减至 0.5）在身份保存和交互对齐上均优于固定核尺寸，说明在去噪早期需要较大的平滑窗口来融合布局，而后期需要更精细的核来保留面部细节。

### 身份注入时机的影响

Table 7 分析了身份嵌入注入的时间步对生成质量的影响。在总共 50 步的去噪过程中，第 0 步注入身份嵌入取得了最高的身份保存，而延迟注入（如第 10 步或第 20 步）会导致身份持续漂移，生成随机的人脸特征。这一结果与 Figure 2(b) 中的动机分析一致：早期注入能锁定面部身份，但 PFD 模型自身会因此丧失交互能力；PersonaHOI 通过 SD 分支在早期提供交互布局，使得 PFD 分支可以在不牺牲交互的前提下尽早注入身份。

### 图像质量与多主体扩展

Table 5 报告了图像质量指标。以 FastComposer 为骨干时，PersonaHOI 将 FID 从 85.98 降至 82.28（降低 3.70），ImageReward 和 Aesthetic Score 均有提升，表明融合过程未引入额外的伪影或质量退化。在多主体 HOI 场景中（Figure 6），PersonaHOI 不仅保持了不同人物的身份区分，还能生成符合 SD 布局的连贯交互，而基线 FastComposer 在多主体下常出现身份混淆或交互缺失。此外，PersonaHOI 还能无缝集成 ControlNet 等空间控制模块（Figure 8），进一步扩展了可控生成的能力边界。

![[assets/figures/papers/paper_list_l1743_PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_In/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative results for multi-subject HOI generation. We compare generation outputs from SD v1.5 [24], FastComposer [34], and our PersonaHOI based on FastComposer [34] with different multi-subject interaction prompts. PersonaHOI not only preserves distinct identities but also generates coherent humanobject interactions that align with the HOI layout produced by SD v1.5*

### 失败模式与局限性

尽管 PersonaHOI 在 HOI 交互对齐上取得了显著提升，但存在以下已知局限：其一，方法依赖预训练 SD 的 HOI 生成能力，当交互极其复杂或物体罕见时，SD 分支自身无法生成合理的布局，导致融合结果失败；其二，IP-Adapter 集成后身份保存从 62.86% 下降至 55.74%（Table 1），尽管交互对齐大幅提升，但存在身份-交互的 trade-off，这与 IP-Adapter 的注意力机制特性有关；其三，头部掩模分割依赖 DensePose，在极端角度或遮挡下可能出现分割错误，进而影响融合质量；其四，双分支并行去噪增加了约一倍的推理计算开销，虽然免训练，但部署成本较高。这些局限指向了未来工作的方向：更鲁棒的掩模分割、更轻量的分支设计，以及在身份保存与交互对齐之间更精细的平衡策略。

## 定位与知识库关联

### 任务定位与瓶颈分析

PersonaHOI 面向**个性化人脸与人物-物体交互（HOI）联合生成**这一交叉任务。该任务要求同时满足两个核心约束：（1）根据参考图像保持身份一致性；（2）遵循复杂的 HOI 文本提示生成全身连贯的交互场景。现有方法在这两个约束之间存在根本性张力——个性化人脸扩散模型（PFD），如 **FastComposer**、**IP-Adapter**、**PhotoMaker**，因在面向人脸的数据集上微调，丧失了预训练 StableDiffusion 所具备的遵循复杂 HOI 文本提示的能力，倾向于生成面部特写而忽略身体和物体的交互（见 Figure 2(b) 中的身份注入时序分析：早期注入保留面部但缺乏交互，延迟注入则身份漂移）。反之，纯文本驱动的 StableDiffusion（SD v1.5、SDXL）虽能生成合理的 HOI 布局，却无法保持身份一致性。

### 方法谱系中的位置

PersonaHOI 在方法谱系中属于**训练自由（training-free）的即插即用融合框架**，其核心思路是在现有 PFD 模型基础上外挂一个 SD 分支，通过空间掩模引导的多层次特征合并，将交互布局从 SD 迁移到 PFD，同时将 PFD 的身份特征限制在面部区域。这一设计使其区别于以下几条技术路线：

- **微调型个性化方法**（如 FastComposer、PhotoMaker）：通过在含人脸的数据集上微调扩散模型来注入身份，但牺牲了文本遵循能力。PersonaHOI 直接复用这些模型，无需重新训练。
- **Adapter 型方法**（如 IP-Adapter）：通过轻量适配器注入图像条件，但同样面临 HOI 场景下的交互缺失问题。PersonaHOI 可无缝集成 IP-Adapter 并提升其交互对齐 18.47%（Table 1）。
- **纯布局引导方法**：依赖外部布局或关键点作为条件，而 PersonaHOI 利用 SD 自身从文本生成的隐式布局，无需额外标注。

### 适用边界与局限

PersonaHOI 的有效性建立在以下前提之上，超出这些边界时性能可能下降：

1. **依赖预训练 SD 的 HOI 能力**：当交互极其复杂或物体罕见时，SD 分支本身无法生成合理的布局，PersonaHOI 无法弥补这一上游缺陷。
2. **头部掩模分割质量敏感**：CAC、LM、RM 三个核心模块均依赖 DensePose 从 SD 生成图像中分割的头部掩模。在极端角度、重度遮挡或非标准光照下，分割误差会直接传导至融合过程，导致身份泄露或交互污染。
3. **身份保存与交互对齐的 trade-off**：在 IP-Adapter 集成中，身份保存从 62.86% 降至 55.74%（Table 1），尽管交互对齐提升显著（+18.47%）。这表明当 PFD 模型本身身份注入机制较弱时，PersonaHOI 的空间约束可能进一步削弱身份特征。
4. **双分支推理开销**：需同时运行 PFD 和 SD 两个扩散模型，推理计算量和显存占用约为单模型的 2 倍。论文未提供具体的延迟或显存对比数据，此点需手动验证。
5. **评估覆盖不足**：定量评估未涉及极端姿势、重度遮挡或多物体交互场景；多主体 HOI 生成仅提供了定性结果（Figure 6），缺乏系统指标。

### 消融证据与因果机制

消融实验（Table 3, Figure 7）严格验证了三个组件的必要性：

- **完整模型**（CAC + LM + RM）在 FastComposer 上达到身份保存 55.28%、交互对齐 56.65%。
- **移除 LM** 或 **RM** 均导致身份保存和交互对齐显著下降（Table 3 红色标注低于基线），表明潜在空间合并与跳过连接残差合并各自承担不可替代的功能。
- **RM 中的滤波器配置**（Figure 7）：Low-High 配置（SD 低通 + PFD 高通）取得最优平衡，验证了“SD 提供低频交互布局、PFD 提供高频身份细节”的频域分工假设。
- **高斯核递减策略**（Table 6）：核大小从 2.5 递减至 0.5 在身份保存和交互对齐上取得最佳平衡，说明去噪早期需要更大感受野的空间引导，后期需精细化。
- **身份注入时机**（Table 7）：在第 0 步注入身份嵌入达到最佳身份保存，优于延迟注入策略，与 Figure 2(b) 的动机分析一致。

### 开放问题

1. **极端条件下的鲁棒性**：如何将 PersonaHOI 扩展到极端姿势、重度遮挡或歧义性交互（如“拿着”可对应多种物体）场景，可能需要引入更强的空间先验或交互推理模块。
2. **计算效率优化**：双分支并行去噪的开销能否通过权重共享、模型蒸馏或异步去噪策略降低，是实际部署的关键瓶颈。
3. **视频 HOI 生成**：当前框架仅处理单帧图像，扩展到视频需解决时序一致的身份保存和交互连贯性问题。
4. **身份-文本一致性 trade-off 的缓解**：在 IP-Adapter 等弱身份注入模型上，如何在提升交互对齐的同时不牺牲身份保存，可能需要更精细的注意力约束策略或自适应掩模权重。

## 原文 PDF

![[paperPDFs/CVPR_2025/PersonaHOI_Effortlessly_Improving_Personalized_Face_with_Human_Object_Interaction_Generation.pdf]]

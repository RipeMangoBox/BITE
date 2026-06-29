---
title: "VToonify: Controllable High-Resolution Portrait Video Style Transfer"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/VToonify_Controllable_High_Resolution_Portrait_Video_Style_Transfer.pdf
project_link: null
code_link: "https://github.com/williamyang1991/VToonify"
aliases:
- VToonify
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
core_operator: 引入外在风格路径（Extrinsic Style Path）以分层残差方式分别调制颜色与结构风格，并配合渐进微调策略保证生成空间从源域到目标域的平滑转变，从而精准模仿示例风格。
primary_logic: 在预训练StyleGAN上添加一个残差式的、分层次的外在风格路径，并通过渐进式微调（从颜色到结构再到目标域）逐步适应，可以在保持高分辨率的同时，实现对艺术肖像颜色和复杂结构风格的灵活、高保真模仿。
claims:
- 用户调研中DualStyleGAN的平均偏好得分0.83，远超次优方法UI2I-style的0.11。
- 消融实验表明，移除面部-肖像配对监督会导致生成结果过拟合肖像风格；移除渐进微调的初始化阶段会使风格迁移完全失败。
- 调制残差块（ModRes）比AdaIN和DAT更准确地模拟了Toonify的微调行为，验证了外在风格路径的设计。
- Cartoon 上 User Preference Score = 0.93
---

# VToonify: Controllable High-Resolution Portrait Video Style Transfer

> [!tip] 核心洞察
> 在预训练StyleGAN上添加一个残差式的、分层次的外在风格路径，并通过渐进式微调（从颜色到结构再到目标域）逐步适应，可以在保持高分辨率的同时，实现对艺术肖像颜色和复杂结构风格的灵活、高保真模仿。

| 字段 | 内容 |
|------|------|
| 中文题名 | Pastiche Master: 基于示例的高分辨率肖像风格迁移 |
| 英文题名 | VToonify: Controllable High-Resolution Portrait Video Style Transfer |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://www.mmlab-ntu.com/project/vtoonify/) · [Code](https://github.com/williamyang1991/VToonify) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer |
| Method | DualStyleGAN |
| Dataset | Cartoon, Caricature, Anime |

> [!tip] 效果简介
> - Cartoon 上，User Preference Score 0.93 vs 0.05 (UI2I-style) (+0.88)。
> - Caricature 上，User Preference Score 0.79 vs 0.15 (UI2I-style) (+0.64)。
> - Anime 上，User Preference Score 0.78 vs 0.14 (UI2I-style) (+0.64)。

## 概要

现有高分辨率肖像风格迁移方法（如基于StyleGAN的微调）难以实现基于示例的灵活风格控制，尤其无法模仿艺术肖像中复杂的结构变形（如卡通的抽象、漫画的夸张），且跨域风格混合易因域间错位产生伪影。本文提出**DualStyleGAN**，在预训练StyleGAN上添加一个残差式的、分层次的外在风格路径（Extrinsic Style Path），并设计三阶段渐进微调策略（颜色迁移→结构迁移→目标域风格迁移），在保持1024×1024高分辨率的同时，实现对艺术肖像颜色与结构风格的灵活、高保真模仿。用户调研中，DualStyleGAN在卡通、漫画、动漫三种风格上的平均偏好得分达0.83，远超次优方法UI2I-style的0.11。该方法属于在预训练生成模型上引入外在条件路径并配合渐进式迁移学习的范式，为基于示例的风格迁移提供了新的架构设计思路。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有高分辨率肖像风格迁移方法（如基于 StyleGAN 微调的 Toonify）存在一个根本性瓶颈：它们将整个生成空间无条件地迁移到目标艺术域，导致模型只能生成该域的“平均”风格，无法根据给定示例灵活控制颜色和结构风格。更关键的是，艺术肖像中复杂的结构变形（如卡通中的抽象比例、漫画中的五官夸张）难以通过简单的域迁移来模仿，跨域风格混合时域间错位会产生严重伪影。

DualStyleGAN 的核心洞察是：在预训练 StyleGAN 上添加一个**残差式、分层次的外在风格路径（Extrinsic Style Path）**，并通过**渐进式微调策略**保证生成空间从源域到目标域的平滑转变，从而在保持高分辨率（1024×1024）的同时，实现对艺术肖像颜色和复杂结构风格的灵活、高保真模仿。

### 架构设计：双风格路径

DualStyleGAN 的核心架构创新在于引入了双风格路径机制，将源域风格控制与目标域风格控制解耦。

**内在风格路径（Intrinsic Style Path）**：保留预训练 StyleGAN 的原始风格调制路径，固定不变，负责控制源域（真实人脸）的身份与风格属性。给定人脸图像 $I$，通过 pSp 编码器 $E$ 提取内在风格码 $\mathbf{z}^+ = E(I)$，该码可忠实地重建原始人脸。

**外在风格路径（Extrinsic Style Path）**：新增的可训练路径，专门建模目标艺术域的风格特征。其设计遵循 StyleGAN 的层次化架构，在不同分辨率层采用不同的调制策略：
- **精细分辨率层（$64^2$–$1024^2$）**：采用与 StyleGAN 相同的颜色变换模块 $T_c$，通过仿射变换调制特征图的通道统计量，控制颜色风格。
- **粗糙分辨率层（$4^2$–$32^2$）**：引入**调制残差块（ModRes）** $T_s$，以残差方式模拟微调过程中卷积核的变化，控制结构风格（如脸型、五官比例）。

给定艺术肖像示例 $S$，其外在风格码同样通过编码器获得：$\mathbf{z}_e^+ = E(S)$。示例式风格迁移的核心公式为：

$$G(E(I), E(S), \mathbf{w})$$

其中 $\mathbf{w}$ 为风格权重向量，用于灵活控制颜色与结构的混合程度。向量 $\mathbf{w}$ 的表示形式为 $[n_1 * v_1, n_2 * v_2, \ldots]$，表示前 $n_1$ 层权重设为 $v_1$，后续 $n_2$ 层设为 $v_2$，以此类推。通过调节 $\mathbf{w}$，用户可在颜色保留与结构夸张之间自由权衡。

**调制残差块（ModRes）的设计动机**：图 5 的消融实验表明，ModRes 比 AdaIN 和 DAT 更准确地模拟了 Toonify 微调中卷积层的变化行为。其残差形式使得初始化时可将卷积滤波器置为接近零值，保证训练初期外在路径对生成结果的影响近乎为零，为渐进微调提供了平滑的起点。

### 面部去风格化：构建配对监督

艺术肖像与真实人脸之间缺乏像素级对应，直接训练外在风格路径容易导致过拟合。DualStyleGAN 提出**面部去风格化（Facial Destylization）**技术，从艺术肖像中恢复对应的真实人脸，形成锚定的“人脸-肖像”配对作为监督信号。

具体而言，给定艺术肖像 $S$，通过优化潜在码 $\mathbf{z}^+$ 来重构 $S$：

$$\hat{\mathbf{z}}_e^+ = \arg\min_{\mathbf{z}^+} \mathcal{L}_{\mathrm{perc}}(g'(\mathbf{z}^+), S) + \lambda_{\mathrm{ID}} \mathcal{L}_{\mathrm{ID}}(g'(\mathbf{z}^+), S) + \|\sigma(\mathbf{z}^+)\|_1$$

其中 $g'$ 为 StyleGAN 生成器的前几层（去除精细层以忽略纹理细节），$\mathcal{L}_{\mathrm{perc}}$ 为感知损失，$\mathcal{L}_{\mathrm{ID}}$ 为人脸身份损失，最后一项为正则化项，约束潜在码的方差。优化得到的 $\mathbf{z}_e^+$ 可同时生成艺术肖像 $G(\mathbf{z}_e^+)$ 和对应的去风格化人脸 $g(\mathbf{z}_e^+)$，后者即作为训练中的内容监督。

图 3 展示了去风格化的渐进过程：从夸张的卡通眼睛逐步恢复为真实眼睛，正则化项则防止模型过拟合与人脸无关的装饰元素（如绿色玩具）。

### 渐进式微调策略

为了在架构修改（新增外在路径）的前提下实现稳健的迁移学习，DualStyleGAN 设计了三阶段渐进微调方案（图 6），训练难度逐步递增：

**第一阶段：颜色迁移（Color Transfer）**
- 目标：训练外在路径的颜色调制能力，同时保持结构不变。
- 初始化策略：ModRes 的卷积滤波器初始化为接近零值，颜色变换模块的全连接层初始化为单位矩阵，确保外在路径初始时输出恒等映射。
- 训练数据：使用 FFHQ 源域数据，通过风格混合生成具有不同颜色风格的图像。
- 损失函数：仅对抗损失和感知损失。

**第二阶段：结构迁移（Structure Transfer）**
- 目标：在源域上训练 ModRes 捕捉中层结构风格。
- 训练方式：在源域上进行风格混合训练，损失函数为：

$$\min_G \max_D \lambda_{\mathrm{adv}} \mathcal{L}_{\mathrm{adv}} + \lambda_{\mathrm{perc}} \mathcal{L}_{\mathrm{perc}}(G(\mathbf{z}_1, \tilde{\mathbf{z}}_2, \mathbf{1}), g(\mathbf{z}_l^+))$$

其中 $\tilde{\mathbf{z}}_2$ 为采样的外在风格码，$\mathbf{z}_l^+$ 为对应的潜在码，$\mathbf{1}$ 表示全权重向量。

**第三阶段：目标域风格迁移（Target Domain Style Transfer）**
- 目标：将整个生成空间平滑迁移到目标艺术域。
- 训练数据：目标域艺术肖像及其去风格化人脸配对。
- 完整损失函数：

$$\min_G \max_D \lambda_{\mathrm{adv}} \mathcal{L}_{\mathrm{adv}} + \lambda_{\mathrm{perc}} \mathcal{L}_{\mathrm{perc}} + \mathcal{L}_{\mathrm{sty}} + \mathcal{L}_{\mathrm{con}}$$

其中风格损失 $\mathcal{L}_{\mathrm{sty}}$ 包含上下文损失和特征匹配损失：

$$\mathcal{L}_{\mathrm{sty}} = \lambda_{\mathrm{CX}} \mathcal{L}_{\mathrm{CX}}(G(\mathbf{z}, \mathbf{z}_e^+, \mathbf{1}), S) + \lambda_{\mathrm{FM}} \mathcal{L}_{\mathrm{FM}}(G(\mathbf{z}, \mathbf{z}_e^+, \mathbf{1}), S)$$

内容损失 $\mathcal{L}_{\mathrm{con}}$ 包含身份损失和权重正则化：

$$\mathcal{L}_{\mathrm{con}} = \lambda_{\mathrm{ID}} \mathcal{L}_{\mathrm{ID}}(G(\mathbf{z}, \mathbf{z}_e^+, \mathbf{1}), g(\mathbf{z})) + \lambda_{\mathrm{reg}} \|W\|_2$$

消融实验（图 10）验证了渐进微调的关键性：跳过第一阶段的初始化直接进行目标域训练，会导致生成空间严重偏离，风格迁移完全失败。

### 推理路径与风格解耦

训练完成后，DualStyleGAN 支持两种推理模式：

1. **示例式风格迁移**：$G(E(I), E(S), \mathbf{w})$——给定人脸图像 $I$ 和风格示例 $S$，通过调节 $\mathbf{w}$ 控制风格混合程度。
2. **随机艺术肖像生成**：$G(\mathbf{z}_1, N(\mathbf{z}_2), \mathbf{w})$——通过采样网络 $N$ 将高斯噪声映射到外在风格分布，实现随机艺术肖像生成。

外在风格码的前 7 行（对应粗糙层）控制结构风格，后 11 行（对应精细层）控制颜色风格，两者天然解耦。图 11 的逐层激活实验揭示了层次化结构调制的语义：低层控制整体脸型，中层夸张面部器官，高层调整局部细节。这种解耦使得用户可独立操作颜色与结构，例如通过设置 $\mathbf{w}_c = 0$ 完全保留原图颜色，仅迁移结构风格。

![[assets/figures/papers/paper_list_l100_https_www_mmlab_ntu_com_project_vtoonify/figures/002_Figure_3.jpg]]
*Figure 3: Illustration of facial destylization. The destylized results of (a) in each stage are sequentially shown in (b)-(d) with the exaggerated eyes gradually turning realistic. (e)-(g): Regularization prevents overfitting to the face-irrelevant green toy. (h)-(j)*

## 实验与关键发现

DualStyleGAN 在卡通、漫画、动画三种艺术风格上的用户偏好调研中展现出压倒性优势。**Table 1** 汇总了平均偏好得分：DualStyleGAN 在三种风格上的平均得分为 **0.83**，远超次优方法 UI2I-style 的 **0.11**。分风格来看，卡通风格上 DualStyleGAN 得分为 **0.93**（UI2I-style 仅 0.05），漫画风格上为 **0.79**（UI2I-style 为 0.15），动画风格上为 **0.78**（UI2I-style 为 0.14）。其他基线方法如 StarGAN2、GNR、U-GAT-IT、FS-Ada 等得分普遍接近零或为负值，表明其在高分辨率示例风格迁移任务上基本无法产生用户可接受的结果。

![[assets/figures/papers/paper_list_l100_https_www_mmlab_ntu_com_project_vtoonify/figures/009_Table_1.jpg]]
*Table 1: User preference scores. Best scores are marked in bold*

定性对比（**Figure 8**）进一步揭示了各方法的差异模式：StarGAN2 和 GNR 倾向于引入模糊和伪影；U-GAT-IT 虽能捕捉部分风格元素，但严重丢失输入人脸的结构信息；UI2I-style 在颜色层面有一定表现，但无法处理结构变形（如卡通中的抽象化、漫画中的夸张化）。相比之下，DualStyleGAN 不仅忠实地保留了输入人脸的身份和姿态，还精确模仿了示例中的颜色调色板和结构变形特征。

### 关键消融实验

**面部去风格化监督的必要性**（**Figure 10(a)**）：移除面部-肖像配对监督后，模型会过拟合目标肖像风格，完全忽略输入人脸的结构信息。这验证了面部去风格化模块提供的锚定配对监督对于平衡风格迁移与内容保留至关重要。

**正则化权重的影响**（**Figure 10(b)**）：当内容损失中的正则项权重 $\lambda_{\mathrm{reg}}=0$ 时，模型会过拟合示例中的发型细节，导致生成结果与输入人脸的发型不一致。实验确定 $\lambda_{\mathrm{reg}}=0.005$ 能够在内容保留与风格模仿之间取得较好平衡。

**渐进微调初始化阶段的决定性作用**（**Figure 10(c)**）：省略渐进微调的第一阶段（即颜色迁移初始化阶段）会导致生成空间严重偏离源域，后续的结构迁移和目标域风格迁移完全失效。这一消融直接证明了渐进微调策略中“从易到难”的课程学习设计是不可或缺的：第一阶段将外在风格路径的调制残差块滤波器初始化为接近零值、颜色变换块初始化为单位矩阵，确保模型在训练初期保持源域生成能力，为后续阶段提供稳定的起点。

**分层结构调制的语义解耦**（**Figure 11**）：通过独立激活外在风格路径中不同粗糙度层级的调制残差块，可以观察到清晰的语义分层——低分辨率层（前几层）控制整体脸型轮廓，中分辨率层负责夸张面部器官（如眼睛大小、鼻子形状），高分辨率层调整局部纹理细节。这一发现验证了外在风格路径继承了 StyleGAN 的层次化架构特性，并成功将其应用于跨域结构风格的解耦控制。

**调制残差块设计的验证**（**Figure 5**）：为验证 ModRes 的设计合理性，实验对比了三种调制方式模拟 Toonify 微调行为的效果：标准 AdaIN、DAT（Deformable Attention Transformer）和 ModRes。结果表明，ModRes 生成的视觉效果与直接微调整个 StyleGAN 的结果最为接近，而 AdaIN 和 DAT 均无法准确复现微调带来的结构变化。这从实证上支撑了“以残差方式模拟卷积层微调变化”的设计动机。

### 失败模式与适用边界

尽管 DualStyleGAN 在受控实验中表现优异，论文明确指出了若干限制（**Figure 16**）：

1. **非人脸区域细节丢失**：当输入照片包含帽子、复杂背景纹理等非人脸元素时，这些区域的细节在风格迁移中会被模糊或丢失。这是因为模型的设计和训练均以人脸区域为核心，外在风格路径的调制范围并未覆盖背景生成。

2. **颜色保留模式下的结构冲突**：当用户选择保留原图颜色（通过设置颜色权重 $w_c=0$ 去激活颜色相关层）时，动画风格中过度抽象的鼻子等特征会显得不自然。这表明颜色与结构风格在极端抽象风格下并非完全独立，强制分离可能导致视觉不协调。

3. **训练数据偏见**：Anime 数据集存在强烈的直发与刘海偏见，导致模型对卷发或无刘海发型的输入处理不佳。此外，对于训练集中不常见的极端风格（如超大眼睛），模型的模仿能力明显不足。这一限制源于数据驱动的学习范式，而非架构设计缺陷。

4. **未见风格的泛化困难**：当面对训练过程中完全未见的艺术风格时，DualStyleGAN 会产生欠一致性的结果。虽然可以通过后优化（latent optimization）进行一定程度的改善，但该过程会引入额外的伪影（**Figure 15**）。这表明外在风格路径学到的风格分布仍然受限于训练数据的覆盖范围，零样本泛化能力有限。

5. **用户调研的统计局限性**：主实验的用户偏好调研仅涉及 27 名受试者，且仅在三种艺术风格上进行评估，样本量和风格覆盖度均有限，结果的统计稳健性需要更大规模验证。

综上，DualStyleGAN 在训练数据覆盖的风格范围内，以显著优势超越了现有方法，但其泛化能力、数据偏见和极端风格处理仍是明确的适用边界。

![[assets/figures/papers/paper_list_l100_https_www_mmlab_ntu_com_project_vtoonify/figures/011_Figure_10.jpg]]
*Figure 10: Ablation study*

![[assets/figures/papers/paper_list_l100_https_www_mmlab_ntu_com_project_vtoonify/figures/015_Figure_14.jpg]]
*Figure 14: Performance on Pixar, Comic and Slam Dunk styles*

![[assets/figures/papers/paper_list_l100_https_www_mmlab_ntu_com_project_vtoonify/figures/004_Figure_5.jpg]]
*Figure 5: ResBlocks best simulate Toonify [29]*

![[assets/figures/papers/paper_list_l100_https_www_mmlab_ntu_com_project_vtoonify/figures/012_Figure_11.jpg]]
*Figure 11: The proposed extrinsic style path learns semantically hierarchical structure modulations*

## 定位与知识库关联

DualStyleGAN 的核心定位是**将基于示例的风格迁移从低分辨率、仅颜色层面的操控，推进到高分辨率（1024×1024）且同时涵盖颜色与复杂结构变形（如卡通抽象、漫画夸张）的层面**。要理解这一进展，需要明确它相对于已有方法究竟改变了什么，以及它在知识图谱中的挂载位置。

### 改变的 Slot：从“单一路径无条件微调”到“双路径条件化渐进微调”

在 DualStyleGAN 出现之前，基于 StyleGAN 的高分辨率风格迁移方法（如 **Toonify**）采用的是**无条件的全模型微调**策略——直接在目标域数据上微调整个 StyleGAN 生成器。这种方式将“风格”隐式地编码进模型权重中，导致两个根本性缺陷：其一，风格控制是全局且不可分解的，无法针对单一样例灵活切换风格；其二，微调后的生成空间完全偏向目标域，丧失了源域（真实人脸）的可控性。

DualStyleGAN 改变的关键 slot 在于**风格表示与调制架构**，具体体现为：

1. **从单一内在风格路径到双风格路径**：在预训练 StyleGAN 的固定内在路径之上，添加了一个**可训练的外在风格路径（Extrinsic Style Path）**。内在路径保持对源域（FFHQ 真实人脸）的完整控制能力；外在路径则专门负责编码和调制目标域（艺术肖像）的风格特征。这一设计将“域迁移”从修改模型权重转变为调节风格码，实现了条件化生成。

2. **从无配对无监督到面部去风格化配对监督**：此前的无监督方法缺乏对人脸-肖像对应关系的显式约束。DualStyleGAN 引入了**面部去风格化（Facial Destylization）**模块，从艺术肖像中恢复对应的真实人脸，形成锚定的配对监督信号。这本质上是在训练中增加了一个**身份保持的锚点**，防止模型在迁移风格时丢失输入人脸的结构信息。

3. **从直接微调到三阶段渐进微调**：由于外在风格路径引入了新的网络结构，直接端到端训练会导致生成空间剧烈偏移。DualStyleGAN 设计了**渐进微调方案**——第一阶段初始化颜色迁移（ModRes 滤波器趋近于零，色彩变换块初始化为恒等矩阵），第二阶段在源域上学习结构迁移，第三阶段才引入目标域风格损失。这一策略确保模型从源域到目标域的平滑过渡，避免了生成空间的坍塌。

4. **从 AdaIN 到调制残差块（ModRes）**：在结构风格的调制方式上，DualStyleGAN 用 **ModRes** 替代了标准的 AdaIN 或 DAT 模块。实验表明，ModRes 以残差方式模拟了 Toonify 中全模型微调时卷积层的变化行为（Figure 5），这是外在风格路径能够精确模仿目标域结构风格的关键。

### 知识库挂载点

DualStyleGAN 在知识图谱中的挂载位置可以从以下几个维度定位：

**上游依赖**：
- **StyleGAN 系列**：继承了 StyleGAN 的分层潜在空间架构和逐层风格调制机制，内在路径完全复用预训练权重。
- **pSp encoder**：用于将人脸图像嵌入到 $\\mathcal{Z}+$ 空间，提供内在风格码。
- **Toonify 方法**：DualStyleGAN 的外在路径设计动机直接源于对 Toonify 微调行为的模拟——ModRes 被设计为以参数高效的方式复现全模型微调的效果。
- **上下文损失（Contextual Loss）和特征匹配损失**：用于风格损失函数，保持与示例肖像的视觉一致性。

**平行对比**：
- **StarGAN2、GNR、U-GAT-IT**：这些方法可以在多个域之间进行图像翻译，但分辨率受限（通常 256×256），且难以处理艺术肖像中的大幅结构变形。
- **UI2I-style**：作为基于示例的风格迁移方法，在用户调研中表现次优（卡通场景偏好得分 0.05，DualStyleGAN 为 0.93），其核心瓶颈在于缺乏对结构风格的有效建模。
- **StyleCariGAN**：专门针对漫画风格迁移，但依赖 3D 形变模型进行几何夸张，泛化能力受限于特定风格域。

**下游延伸潜力**：
- 论文展示了该方法对 Pixar、Comic、Slam Dunk 等风格的迁移能力（Figure 14），以及对未见过风格的初步尝试（Figure 15），但后者会产生不一致的结果和伪影。这表明外在风格路径的泛化边界受限于训练数据的风格分布，后续工作可探索元学习或风格解耦增强来扩展这一边界。
- 训练数据偏见（如 Anime 数据集对直发和刘海的偏好）导致对卷发或无刘海发型的处理失败，这指向了**数据增强或公平性约束**的改进方向。
- 风格权重向量 $w$ 的分层控制特性（低层控制脸型、中层夸张器官、高层调整细节）揭示了外在路径内部存在**语义层次化的结构调制**，这为后续研究提供了可解释的风格操控接口。

### 适用边界与失效模式

DualStyleGAN 的适用边界清晰：**在训练数据覆盖的风格域内，对正面或近正面人像进行高分辨率风格迁移**。以下情况会触发失效：

1. **非人脸区域的信息丢失**：帽子、背景纹理等非人脸细节在迁移中会被忽略，因为面部去风格化模块只关注人脸区域。
2. **训练数据偏见**：Anime 数据集对特定发型的偏好导致对少数群体外观的迁移质量下降；对极大眼睛等不常见风格模仿不足。
3. **未见风格的泛化失败**：对完全未见的艺术风格，外在路径无法提供准确的风格码，后优化虽可改善但会引入伪影。
4. **颜色保留与结构风格的冲突**：当保留原图颜色时，动漫风中过于抽象的鼻子等结构会显得不自然，说明颜色与结构在某些风格下并非完全可分解。

### 后续启发

DualStyleGAN 的核心贡献在于证明了**在预训练生成器上添加残差式、分层的外在风格路径，配合渐进微调策略，可以实现对复杂艺术风格的高保真模仿**。这一设计范式——即“固定内在域表示 + 可训练外在域调制”的双路径架构——对后续工作的启发包括：如何将类似的双路径思想扩展到更一般的图像到图像翻译任务；如何通过风格码的解耦与组合实现零样本风格迁移；以及如何在保持高分辨率的同时，降低对配对监督和渐进训练的依赖。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/VToonify_Controllable_High_Resolution_Portrait_Video_Style_Transfer.pdf]]
---
title: "SMooDi: Stylized Motion Diffusion Model"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/SMooDi_Stylized_Motion_Diffusion_Model.pdf
project_link: https://neu-vi.github.io/SMooDi/
code_link: null
aliases:
- SMooDi
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 风格调节模块（style modulation module），包含风格适配器（style adaptor）和两种互补的风格引导机制（classifier-free style guidance 与 classifier-based style guidance），使单一模型能够从文本和参考风格序列生成风格化运动。
primary_logic: 通过微调预训练的文本到运动扩散模型（MLD）来注入风格条件，而不是为每种风格单独训练或依赖有限的风格迁移流水线，从而在保留广泛内容生成能力的同时学习多种运动风格。
claims:
- SMooDi 在风格化文本生成运动任务中风格识别准确率（SRA）达 72.418%，远超基线
- 去除基于分类器的风格引导后 SRA 下降至 20.245%，降幅达 208%
- 同时去除先验保留损失和循环损失导致 FID 恶化 229% 以上，出现严重的“内容遗忘”
- 在运动风格迁移的跨数据集泛化测试中，内容识别准确率（CRA）显著优于基线（45.555% vs. 34.444% 和 25.556%）
---

# SMooDi: Stylized Motion Diffusion Model

> [!tip] 核心洞察
> 通过微调预训练的文本到运动扩散模型（MLD）来注入风格条件，而不是为每种风格单独训练或依赖有限的风格迁移流水线，从而在保留广泛内容生成能力的同时学习多种运动风格。

| 字段 | 内容 |
|------|------|
| 中文题名 | 风格化运动扩散模型 SMooDi |
| 英文题名 | SMooDi: Stylized Motion Diffusion Model |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://neu-vi.github.io/SMooDi/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SMooDi |
| Dataset | HumanML3D + 100STYLE, Xia dataset |

> [!tip] 效果简介
> - HumanML3D + 100STYLE (stylized text2motion) 上，FID↓ 1.609 vs MLD+Aberman et al.: 3.309 (-51.38%)；SRA↑ (%) 72.418 vs MLD+Motion Puzzle: 63.769 (+13.56%)。
> - HumanML3D + 100STYLE (motion style transfer) 上，FID↓ 0.095 vs Aberman et al.: 0.338 / Motion Puzzle: 0.197 (-71.9% / -51.8%)。
> - Xia dataset (unseen, motion style transfer) 上，CRA↑ (%) 45.555 vs Aberman et al.: 34.444 / Motion Puzzle: 25.556 (+32.26% / +78.26%)。

## 概要

**瓶颈与动机** 现有文本驱动的人体运动生成方法（如 MLD）缺乏对运动*风格*的控制能力；而独立的运动风格迁移方法（如 Motion Puzzle、Aberman et al.）依赖有限风格数据集训练，与文本到运动模型串行使用时会产生误差累积。这种“内容—风格”分离的流水线无法同时满足多样内容与多种风格的需求。

**核心方法** SMooDi 提出一种**风格调节模块**，将风格条件注入预训练的文本到运动扩散模型（MLD），使单一模型能够从内容文本和参考风格序列联合生成风格化运动。该模块包含两个关键组件：1）**风格适配器**（Style Adaptor），基于 ControlNet 范式，通过零初始化线性层将风格残差融入 MLD 的 Transformer 注意力层；2）**互补的双重风格引导机制**——分类器自由风格引导（$w_s$）与基于分类器的风格引导（$\tau \nabla G$），分别负责全局风格倾向和局部细节精修。训练阶段引入**内容先验保留损失** $\mathcal{L}_{pr}$ 与**循环先验保留损失** $\mathcal{L}_{cyc}$，防止微调过程中出现“内容遗忘”。

**核心结论** 在 HumanML3D + 100STYLE 的风格化文本生成运动任务中，SMooDi 的**风格识别准确率（SRA）达 72.418%**，远超 MLD+Motion Puzzle（63.769%）和 MLD+Aberman et al.（54.367%）等串行基线（Table 1）。运动风格迁移任务中，跨数据集泛化（Xia 数据集）的**内容识别准确率（CRA）达 45.555%**，较 Aberman et al.（34.444%）和 Motion Puzzle（25.556%）分别提升 32.26% 和 78.26%（Table 2b）。消融实验证实：去除基于分类器的风格引导后 SRA 骤降至 20.245%，降幅达 208%；同时去除 $\mathcal{L}_{pr}$ 和 $\mathcal{L}_{cyc}$ 则导致 FID 恶化 229% 以上，出现严重内容遗忘（Table 3）。

**方法定位** SMooDi 属于**基于扩散模型的运动风格化方法**，在方法谱系中位于“文本到运动生成”与“运动风格迁移”的交汇点。与为每种风格单独训练模型或依赖有限风格迁移流水线的方案不同，它通过微调预训练文本到运动模型来注入风格条件，在保留广泛内容生成能力的同时学习多种运动风格。

### 问题背景

文本驱动的三维人体运动生成近年来取得了显著进展，用户可以通过自然语言描述生成多样化的运动序列。然而，现实应用不仅要求运动在语义上匹配文本内容，还期望运动表现出特定的风格特征——例如“僵尸般行走”、“优雅地舞蹈”或“疲惫地坐下”。这种**风格化运动生成**（stylized motion generation）的需求广泛存在于动画制作、游戏开发和虚拟人交互等场景中。

### 现有方法与缺口

当前解决风格化运动生成的技术路线主要分为两类，但各自存在明显局限：

**第一类：文本到运动生成模型缺乏风格控制。** 以 **MLD**（Motion Latent Diffusion Model）为代表的预训练文本到运动扩散模型能够根据内容描述生成高质量的运动，但其条件输入仅限于文本，无法接受风格参考信号。这使得用户无法指定“以何种风格”执行文本描述的动作。

**第二类：独立的运动风格迁移方法依赖有限数据集且存在误差累积。** 现有运动风格迁移方法（如 **Aberman et al.** 和 **Motion Puzzle**）可以将参考运动的风格迁移到内容运动上，但它们通常需要成对的风格化运动数据进行训练，且风格种类受限于数据集的覆盖范围。当将这些方法与文本到运动模型串行使用时——即先用文本生成内容运动、再进行风格迁移——两个阶段的误差会相互叠加，导致最终生成的运动在内容保持和风格反映两方面均出现退化。

**核心瓶颈在于：** 现有技术无法在单一模型中同时满足**多样内容**与**多种风格**的需求。文本到运动模型缺乏风格条件注入机制，而风格迁移方法依赖有限风格数据且与文本模型串行时产生误差累积。

### 本文动机

针对上述缺口，SMooDi 提出了一种新的技术思路：**通过微调预训练的文本到运动扩散模型来注入风格条件**，而非为每种风格单独训练模型或依赖有限的风格迁移流水线。这一策略的核心优势在于：

1. **保留广泛的内容生成能力**：预训练模型在海量文本-运动数据上习得的丰富内容知识得以保留，避免“内容遗忘”。
2. **学习多种运动风格**：通过精心设计的风格调节模块，单一模型即可响应来自参考风格序列的风格信号，生成与内容文本语义一致且风格鲜明的运动。
3. **避免串行误差**：将风格化生成整合到统一的扩散去噪框架中，消除了文本生成与风格迁移两阶段之间的误差累积。

SMooDi 是首个将预训练文本到运动模型适配为风格化生成模型的工作，为风格可控的运动生成开辟了新的技术路径。

## 核心方法与创新机理

SMooDi 的核心创新在于将风格条件注入冻结的文本到运动扩散模型，从而在保留广泛内容生成能力的同时，赋予单一模型对多种运动风格的控制力。这一思路通过三个紧密耦合的“changed slots”实现。

### 风格适配器：零侵入的风格条件注入

SMooDi 并未修改预训练 MLD 的参数，而是引入一个**风格适配器（Style Adaptor）**，其设计遵循 ControlNet 范式。具体而言，风格适配器是 MLD 中 Transformer Encoder 的一个可训练副本，通过**零初始化线性层**与冻结的 MLD 注意力层相连（Fig. 3）。在训练初期，零初始化确保风格残差为零，模型行为完全等同于原始 MLD；随着训练进行，适配器逐步学会将风格编码器输出的风格嵌入转化为有意义的残差特征，引导去噪过程朝向目标风格。这种“零侵入”设计使得模型在微调时不会破坏预训练权重中蕴含的内容生成知识，是后续先验保留损失能够高效工作的结构基础。

### 双重风格引导：粗粒度与细粒度的互补

SMooDi 将风格控制分解为两种互补的引导机制，形成从粗到细的风格注入管线。

**分类器自由风格引导（Classifier-Free Style Guidance）** 将标准的分类器自由引导扩展为内容与风格两个独立维度。如 Eq. (1) 所示：

$$
\epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) = \epsilon_{\theta}(z_t, t, \emptyset, \emptyset) + w_c(\epsilon_{\theta}(z_t, t, \mathbf{c}, \emptyset) - \epsilon_{\theta}(z_t, t, \emptyset, \emptyset)) + w_s(\epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) - \epsilon_{\theta}(z_t, t, \mathbf{c}, \emptyset))
$$

其中 $w_c$ 控制内容文本的忠实度，$w_s$ 控制风格反映的强度。这种分解使风格引导独立于内容引导，避免了两者在隐空间中的相互干扰（Fig. 4(a-b) 直观展示了二者的分离效果）。

**基于分类器的风格引导（Classifier-Based Style Guidance）** 提供更精细的风格调节。它利用在 100STYLE 上预训练的风格分类器（去除最后一层全连接层后作为风格特征提取器 $f$），计算预测运动 $\hat{\mathbf{x}}_0$ 与参考风格 $\mathbf{s}$ 之间风格嵌入的 L1 距离梯度，并将其附加到去噪输出上：

$$
\epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) = \epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) + \tau \nabla_{z_t} G(z_t, t, \mathbf{s}), \quad G(z_t, t, \mathbf{s}) = |f(\hat{\mathbf{x}}_0) - f(\mathbf{s})|
$$

消融实验直接验证了这一机制的关键性：去除基于分类器的风格引导后，风格识别准确率（SRA）从 72.418% 骤降至 20.245%，降幅超过 208%（Table 3）。分类器自由引导提供全局的风格方向，而分类器基础引导则在局部进行精细修正，二者协同使生成的运动在保持内容语义的同时高度贴合目标风格。

### 先验保留损失：防止“内容遗忘”的关键约束

仅使用标准扩散损失 $\mathcal{L}_{std}$ 在 100STYLE 上微调风格适配器，会导致模型逐渐遗忘文本到运动的内容生成能力——即“内容遗忘”问题。SMooDi 通过两类先验保留损失来对抗这一退化。

**内容先验保留损失 $\mathcal{L}_{pr}$** 在训练过程中额外采样 HumanML3D 数据，要求模型在这些内容样本上的去噪预测仍与真实噪声一致：

$$
\mathcal{L}_{pr} = \mathbb{E}_{\epsilon', z'} \left[ \| \epsilon_{\theta}(z_t', t, \mathbf{c}', \mathbf{s}') - \epsilon' \|_2^2 \right]
$$

**循环先验保留损失 $\mathcal{L}_{cyc}$** 在 HumanML3D 和 100STYLE 之间交换内容与风格，强制内容描述在正反向翻译中保持不变（Fig. 8 展示了该流水线）：

$$
\mathcal{L}_{cyc} = \mathbb{E}_{z, z', \epsilon, \epsilon'} \left[ \| \epsilon_{\theta}(z_t^{sh}, t, \mathbf{c}, s^{hs}) + \epsilon_{\theta}(z_t^{hs}, t, \mathbf{c}', s^{sh}) - \epsilon - \epsilon' \|_2^2 \right]
$$

消融实验给出了最具说服力的证据：**同时去除 $\mathcal{L}_{pr}$ 和 $\mathcal{L}_{cyc}$ 导致 FID 从 1.609 恶化至 5.996，降幅超过 229%**，表明模型已严重丧失内容保持能力（Table 3）。单独去除 $\mathcal{L}_{cyc}$ 则使 SRA 从 72.418% 降至 64.866%，说明循环损失对风格反映也有重要贡献。这些结果共同揭示了一个因果机制：先验保留损失并非简单的正则化项，而是使风格适配器能够在“学习新风格”与“保留旧知识”之间达成帕累托最优的核心约束。

### 创新总结

SMooDi 的创新链条可概括为：**风格适配器提供结构基础 → 双重风格引导实现从粗到细的风格控制 → 先验保留损失防止内容能力退化**。三者缺一不可：去除适配器使 FID 恶化约 80.46%（Table 3），去除分类器基础引导使 SRA 崩溃，去除先验保留损失则导致内容生成能力瓦解。这一设计使 SMooDi 成为首个在单一模型中同时实现多样化内容生成与多种风格控制的文本到运动框架。

SMooDi 的整体 pipeline 建立在对预训练文本到运动潜在扩散模型（MLD）的定制化微调之上。其核心设计思想是：**冻结基础生成骨架，通过外部风格条件模块注入风格控制信号**，从而在保留广泛内容生成能力的同时学习多种运动风格。

### 输入输出流

模型接收两类输入：
- **内容文本** $\mathbf{c}$：描述运动的语义内容（如“一个人向前走然后坐下”）
- **风格运动序列** $\mathbf{s}$：提供目标风格的参考运动片段

输出为同时满足内容语义与风格特征的人体运动序列。此外，模型也接受运动序列作为内容输入，以支持运动风格迁移任务。

### 模块组成与数据流

SMooDi 由以下核心模块构成，其协作流程如 Fig. 2 所示：

![[assets/figures/papers/paper_list_l1879_SMooDi_Stylized_Motion_Diffusion_Model/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SMooDi. Our model generates stylized human motions from content text and a style motion sequence. At the denoising step*

1. **预训练 MLD 骨架**：作为基础文本到运动生成器，扩散过程在潜在空间执行。该骨架在训练中保持冻结，仅作为被调控的目标网络。

2. **风格编码器**：由单层 Transformer Encoder 构成，将参考风格序列 $\mathbf{s}$ 编码为风格嵌入，供后续模块使用。

3. **风格适配器**：可训练的 Transformer Encoder 副本（与 MLD 中的 Transformer Encoder 结构相同），通过零初始化线性层连接到 MLD 的注意力层。在每个去噪步 $t$，风格适配器接收内容文本 $\mathbf{c}$、风格嵌入和当前噪声潜变量 $\mathbf{z}_t$，预测残差特征并注入 MLD，将预测噪声引导至目标风格方向。

4. **双重风格引导机制**：
   - **分类器自由风格引导**：将条件引导分解为无条件项、仅内容项和附加风格项三部分，通过独立的引导权重 $w_c$ 和 $w_s$ 分别控制内容保持与风格反映的强度。
   - **基于分类器的风格引导**：利用预训练风格分类器（去掉最后全连接层）提取风格特征，计算预测运动与参考风格在风格嵌入空间的 L1 距离梯度 $\tau \nabla_{\mathbf{z}_t} G(\mathbf{z}_t, t, \mathbf{s})$，精细调节生成运动朝向目标风格。两种引导机制互补协作：前者提供粗粒度的风格方向，后者进行细粒度修正。

5. **运动解码器** $\mathcal{D}$：将去噪后的干净潜变量 $\mathbf{z}_0$ 解码为最终的运动表示 $\mathbf{x}$。

### 训练策略

训练损失由三部分加权组成：
$$\mathcal{L}_{all} = \mathcal{L}_{std} + \lambda_{pr} \mathcal{L}_{pr} + \lambda_{cyc} \mathcal{L}_{cyc}$$

- $\mathcal{L}_{std}$：在 100STYLE 数据集上的标准扩散损失，训练风格适配器学习风格条件映射。
- $\mathcal{L}_{pr}$（内容先验保留损失）：在 HumanML3D 数据上额外计算扩散损失，防止微调过程中模型遗忘文本到运动的内容生成能力。
- $\mathcal{L}_{cyc}$（循环先验保留损失）：在 HumanML3D 和 100STYLE 之间交换内容与风格，鼓励内容描述在正反向翻译中保持不变（详见 Fig. 8），进一步增强内容保持能力。

消融实验证实，同时去除 $\mathcal{L}_{pr}$ 和 $\mathcal{L}_{cyc}$ 会导致 FID 从 1.609 恶化至 5.996（降幅超过 229%），出现严重的“内容遗忘”现象，验证了先验保留策略的必要性。

SMooDi 的核心架构由两个关键模块构成：**风格适配器**（Style Adaptor）和**双通路风格引导机制**。前者负责将参考风格序列的条件信息注入预训练的文本到运动扩散模型，后者则在推理阶段通过互补的引导策略精确控制生成运动的风格表现力。

### 风格适配器

风格适配器的设计遵循 ControlNet 范式，其目标是使冻结的预训练运动潜在扩散模型（MLD）能够接收额外的风格条件，同时不破坏原有的文本到运动生成能力。具体结构如下（参见 Fig. 3）：

- **可训练副本**：风格适配器是 MLD 中 Transformer Encoder 的一个可训练副本。它接收由风格编码器（一个单层 Transformer）编码的风格嵌入，并在各层输出风格相关的残差特征。
- **零初始化连接**：适配器的每一层输出通过一个线性层连接到 MLD 对应层的注意力模块。该线性层的权重和偏置均初始化为零，确保训练初期适配器不对预训练模型产生扰动，从而保证训练稳定性。
- **风格编码器**：参考风格运动序列 $s$ 首先经过一个单层 Transformer Encoder 编码为风格嵌入，再送入风格适配器进行条件注入。

### 双通路风格引导

在推理阶段，SMooDi 同时使用两种互补的风格引导机制，分别从全局和局部层面调控生成运动向目标风格靠拢。

**1. 分解的分类器自由引导**

SMooDi 将传统的分类器自由引导分解为内容引导与风格引导两个独立分量，允许分别控制二者的强度：

$$
\epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) = \epsilon_{\theta}(z_t, t, \emptyset, \emptyset) + w_c(\epsilon_{\theta}(z_t, t, \mathbf{c}, \emptyset) - \epsilon_{\theta}(z_t, t, \emptyset, \emptyset)) + w_s(\epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) - \epsilon_{\theta}(z_t, t, \mathbf{c}, \emptyset))
$$

其中：
- $z_t$ 为时刻 $t$ 的噪声潜变量
- $\mathbf{c}$ 为内容文本条件
- $\mathbf{s}$ 为参考风格序列
- $w_c$ 和 $w_s$ 分别控制内容保持和风格反映的强度

该分解使得模型能够在“无条件生成”、“仅内容条件生成”和“内容+风格条件生成”三个信号之间进行线性插值，实现灵活的风格强度调节。

**2. 基于分类器的风格引导**

为进一步精细调节生成运动与目标风格的匹配度，SMooDi 引入基于预训练风格分类器的梯度引导：

$$
\epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) = \epsilon_{\theta}(z_t, t, \mathbf{c}, \mathbf{s}) + \tau \nabla_{z_t} G(z_t, t, \mathbf{s}), \quad G(z_t, t, \mathbf{s}) = |f(\hat{\mathbf{x}}_0) - f(\mathbf{s})|
$$

其中：
- $f(\cdot)$ 为风格特征提取器，由在 100STYLE 数据集上训练的风格分类器去掉最后一层得到
- $\hat{\mathbf{x}}_0$ 为通过 DDIM 一步估计从 $z_t$ 预测的干净运动：
  $$\hat{z}_0 = \frac{z_t - \sqrt{1-\alpha_t} \varepsilon_{\theta}(z_t, t, c, s)}{\sqrt{\alpha_t}}$$
- $G(z_t, t, \mathbf{s})$ 计算预测运动与参考风格在风格嵌入空间的 L1 距离
- $\tau$ 为引导强度

该引导机制直接对去噪过程中的潜变量施加梯度，使生成运动在风格特征空间中向参考风格靠拢。消融实验表明，去除该模块后风格识别准确率（SRA）从 72.418% 骤降至 20.245%，降幅达 208%，验证了其关键作用（Table 3）。

### 训练损失函数

为防止在风格数据集上微调时发生“内容遗忘”（即丧失文本到运动的内容生成能力），SMooDi 在标准扩散损失 $\mathcal{L}_{std}$ 基础上引入两项先验保留损失：

**内容先验保留损失** $\mathcal{L}_{pr}$：使用 HumanML3D 数据集样本额外计算扩散损失，强制模型在微调过程中保持对内容文本的响应能力。

$$
\mathcal{L}_{pr} = \mathbb{E}_{\epsilon', z'} \left[ \| \epsilon_{\theta}(z_t', t, \mathbf{c}', \mathbf{s}') - \epsilon' \|_2^2 \right]
$$

**循环先验保留损失** $\mathcal{L}_{cyc}$：在 HumanML3D 和 100STYLE 之间交换内容与风格，鼓励内容描述在正反向翻译中保持不变。

$$
\mathcal{L}_{cyc} = \mathbb{E}_{z, z', \epsilon, \epsilon'} \left[ \| \epsilon_{\theta}(z_t^{sh}, t, \mathbf{c}, s^{hs}) + \epsilon_{\theta}(z_t^{hs}, t, \mathbf{c}', s^{sh}) - \epsilon - \epsilon' \|_2^2 \right]
$$

总损失为三者的加权和：

$$
\mathcal{L}_{all} = \mathcal{L}_{std} + \lambda_{pr} \mathcal{L}_{pr} + \lambda_{cyc} \mathcal{L}_{cyc}
$$

消融实验证实，同时去除 $\mathcal{L}_{pr}$ 和 $\mathcal{L}_{cyc}$ 会导致 FID 从 1.609 恶化至 5.996（恶化 229% 以上），出现严重的“内容遗忘”现象（Table 3）。

![[assets/figures/papers/paper_list_l1879_SMooDi_Stylized_Motion_Diffusion_Model/figures/013_Figure_8.jpg]]
*Figure 8: Visual pipeline of the cycle prior-preservation loss*

## 实验与关键发现

SMooDi 在风格化文本生成运动（stylized text2motion）和运动风格迁移（motion style transfer）两个核心任务上进行了系统评估。实验以 HumanML3D 提供内容文本、100STYLE 提供参考风格序列，并与三类基线方法对比：**MLD + Motion Puzzle**（文本到运动生成与运动风格迁移的串行流水线）、**MLD + Aberman et al.**（另一串行风格迁移基线）以及 **ChatGPT + MLD**（通过文本融合风格标签的直接文本驱动方法）。为保证公平性，所有基线均使用相同的 6-D 旋转表示重新训练，且训练迭代次数为 SMooDi 的 5 倍。评估风格识别准确率（SRA）时，排除了 100STYLE 中具有内容含义的 ACT 组，仅使用与内容无关的风格标签（CHAR、PER、EMO、MOT、OBJ），以避免内容与风格的语义冲突。

### 风格化文本生成运动

Table 1 展示了风格化文本生成运动任务的主要结果。SMooDi 在内容保持和风格反映两个维度上均显著优于所有基线。具体而言，SMooDi 的 FID 达到 **1.609**，相比 MLD + Aberman et al. 的 3.309 改善了 **51.38%**；风格识别准确率 SRA 为 **72.418%**，较 MLD + Motion Puzzle 的 63.769% 提升了 **13.56%**。ChatGPT + MLD 的 SRA 仅为 4.819%，表明单纯通过文本融合风格标签几乎无法实现有效的风格控制。值得注意的是，SMooDi 在 R-precision（0.129 vs. 0.122）和多样性（Diversity 9.148 vs. 8.631）上也优于最强基线，验证了其生成运动既贴合内容语义又保持丰富变化的优势。

![[assets/figures/papers/paper_list_l1879_SMooDi_Stylized_Motion_Diffusion_Model/figures/005_Table_1.jpg]]
*Table 1: Comparison with baseline methods on stylized motion generation driven by content text, using a combination of the 100STYLE (providing style) and HumanML3D datasets (providing content)*

在定性对比（Fig. 5）中，SMooDi 生成的风格化运动在步态节奏、躯干姿态等风格特征上明显更接近参考风格序列，而串行基线方法因误差累积常出现风格特征模糊或内容偏离的问题。

![[assets/figures/papers/paper_list_l1879_SMooDi_Stylized_Motion_Diffusion_Model/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparisons of our approach and baseline methods on two stylized motion generation task*

### 运动风格迁移

SMooDi 未针对运动风格迁移任务进行专门训练，仅通过 DDIM 反演将内容运动编码为潜变量，再调整引导权重实现风格迁移，这保证了与专用风格迁移方法的公平比较。在 HumanML3D 数据集上（Table 2a），SMooDi 的 FID 达到 **0.095**，相比 Aberman et al. 的 0.338 降低了 **71.9%**，比 Motion Puzzle 的 0.197 降低了 **51.8%**；SRA 为 65.147%，显著高于 Aberman et al. 的 42.878% 和 Motion Puzzle 的 42.382%。在跨数据集泛化测试中（Table 2b，Xia 数据集），SMooDi 的内容识别准确率 CRA 达到 **45.555%**，远超 Aberman et al. 的 34.444% 和 Motion Puzzle 的 25.556%，证明了其在未见数据分布上的强泛化能力。

### 消融实验

Table 3 系统消融了 SMooDi 各核心组件的作用，揭示了以下关键因果机制：

![[assets/figures/papers/paper_list_l1879_SMooDi_Stylized_Motion_Diffusion_Model/figures/008_Table_3.jpg]]
*Table 3: Ablation Studies on HumanML3D Content and 100STYLE Styles*

**风格适配器的贡献。** 移除风格适配器（w/o adaptor）后，FID 从 1.609 恶化至 2.984，降幅约 **80.46%**。这表明风格适配器不仅负责风格注入，还对生成运动的整体真实感有重要贡献——其通过零初始化线性层逐步融入的残差特征有效稳定了微调过程。

**先验保留损失防止“内容遗忘”。** 同时移除内容先验保留损失和循环先验保留损失（w/o L_pr + L_cyc）导致 FID 飙升至 **5.996**，恶化超过 **229%**，出现严重的“内容遗忘”现象。单独移除循环损失（w/o L_cyc）使 SRA 从 72.418% 降至 64.866%，风格反映能力下降约 10.4%，验证了循环先验保留损失在 HumanML3D 和 100STYLE 之间交换内容与风格以保持内容一致性的关键作用。

**双引导机制的互补性。** 去除基于分类器的风格引导（w/o classifier-based guidance）后，SRA 从 72.418% 骤降至 **20.245%**，降幅约 208%（原文报告“yielding an impressive 208% improvement”）。这一定量结果强有力地证明：分类器自由风格引导提供粗粒度的风格方向，而基于分类器的风格引导通过风格嵌入 L1 距离的梯度实现精细调节，二者互补且缺一不可。

### 推理效率与局限性

Table 5 报告了推理时间对比。SMooDi 全模型的平均每句推理时间（AITS）约 **3.11 秒**，是基础 MLD（0.21 秒）的约 10 倍以上。时间开销主要来自基于分类器的风格引导需要在每个去噪步计算梯度。风格适配器单独增加约 0.11 秒，分类器自由风格引导增加约 0.15 秒，而分类器基础引导增加约 2.64 秒，成为推理瓶颈。

![[assets/figures/papers/paper_list_l1879_SMooDi_Stylized_Motion_Diffusion_Model/figures/012_Table_5.jpg]]
*Table 5: Inference time. We report the Average Inference Time per Sentence (AITS) in seconds for baselines and each submodule of ours on stylized text2motion tasks*

此外，SMooDi 继承了预训练扩散模型的脚部滑动问题（Table 1 中 foot skating ratio 为 1.582），且基于分类器的风格引导依赖 100STYLE 训练的分类器，当内容文本与运动风格数据集分布差异较大时（如“坐下”等非运动类动作），引导效果可能下降。这些局限性指向了未来引入物理约束或真感引导的改进方向。

## 定位与知识库关联

### 1. 基线关系与创新定位

SMooDi 处于**文本到运动生成**与**运动风格迁移**两条技术路线的交叉点，其核心创新在于首次将风格条件注入预训练文本到运动扩散模型，而非采用串行流水线或独立风格模型。

**串行流水线基线**：最直接的对比来自“文本到运动生成 + 运动风格迁移”的串行组合，即先用预训练文本到运动模型（MLD）生成内容运动，再通过独立的运动风格迁移方法（如 **Motion Puzzle** 和 **Aberman et al.**）进行风格化。这种串行方案存在两个根本性缺陷：（1）风格迁移方法本身依赖有限风格数据集训练，泛化能力受限；（2）两阶段独立优化导致误差累积，内容保持与风格反映难以兼顾。实验证据充分验证了这一点：在 HumanML3D + 100STYLE 的风格化文本生成运动任务中，SMooDi 的 FID 达 1.609，相比 MLD+Aberman et al. 的 3.309 降低了 51.38%；风格识别准确率（SRA）达 72.418%，相比 MLD+Motion Puzzle 的 63.769% 提升了 13.56%（Table 1）。

**文本融合基线**：ChatGPT+MLD 方案试图通过将风格标签直接融入内容文本（如“A person walks forward in a happy style”）来驱动 MLD 生成风格化运动，但其 SRA 仅 4.819%，几乎无法反映风格特征。这表明文本空间中的风格融合无法有效传递运动风格的细粒度特征，也印证了专用风格条件注入机制的必要性。

**与运动风格迁移方法的本质差异**：在运动风格迁移任务中，SMooDi 并未专门为此训练，仅通过 DDIM 反演和调整引导权重实现，但其在 HumanML3D 上的 FID 达 0.095，相比 Aberman et al.（0.338）和 Motion Puzzle（0.197）分别降低 71.9% 和 51.8%（Table 2a）。在跨数据集泛化测试（Xia 数据集）中，SMooDi 的内容识别准确率（CRA）达 45.555%，远超 Aberman et al.（34.444%）和 Motion Puzzle（25.556%）（Table 2b），表明其风格适配器学到的风格表征具有更强的跨数据集迁移能力。

**公平性保障**：所有基线均使用相同的 6-D 旋转表示重新训练，且训练迭代次数是 SMooDi 的 5 倍，确保了比较的公平性。SRA 评估时排除了 100STYLE 中具有内容含义的风格类别（ACT 组），仅使用与内容无关的风格标签（CHAR, PER, EMO, MOT, OBJ）以避免内容冲突。

### 2. 技术继承与改造

SMooDi 的技术骨架继承自 **MLD（Motion Latent Diffusion Model）**，后者是一个在潜在空间执行扩散过程的文本到运动生成模型。SMooDi 对 MLD 的改造集中在三个关键维度：

**风格条件注入机制**：借鉴 ControlNet 的设计范式，SMooDi 引入风格适配器（Style Adaptor）——一个 MLD 中 Transformer Encoder 的可训练副本，通过零初始化线性层向冻结的 MLD 注入风格残差特征。这种设计保留了预训练模型的文本到运动生成能力，同时以最小侵入的方式添加风格条件通道。

**引导机制的双重互补设计**：SMooDi 将分类器自由引导分解为内容引导（$w_c$）和风格引导（$w_s$）两个独立分量（Eq. 1），并额外引入基于分类器的风格引导（Eq. 2），利用预训练风格分类器（去掉最后全连接层）提取的风格嵌入 L1 距离梯度进行精细调节。消融实验表明，去除基于分类器的风格引导后，SRA 从 72.418% 骤降至 20.245%（降幅达 208%），验证了该组件的关键作用（Table 3）。

**防止内容遗忘的损失设计**：仅使用标准扩散损失在 100STYLE 上微调会导致模型遗忘文本到运动的内容生成能力。SMooDi 引入内容先验保留损失 $\mathcal{L}_{pr}$（Eq. 5）和循环先验保留损失 $\mathcal{L}_{cyc}$（Eq. 6），前者使用 HumanML3D 数据维持内容生成能力，后者在 HumanML3D 和 100STYLE 之间交换内容与风格以鼓励内容描述在正反向翻译中保持不变。消融实验显示，同时去除这两项损失导致 FID 恶化至 5.996（相比完整模型的 1.609 恶化 229% 以上），出现严重的“内容遗忘”现象（Table 3）。

### 3. 适用边界与局限

**推理效率瓶颈**：SMooDi 的全模型平均推理时间（AITS）约 3.11 秒，是基础 MLD（0.21 秒）的约 10 倍以上（Table 5），主要瓶颈在于基于分类器的风格引导需要迭代计算梯度。这限制了其在实时交互场景中的应用。

**风格数据分布依赖**：基于分类器的风格引导依赖在 100STYLE 上训练的风格分类器。当内容文本描述的动作与风格运动数据集的分布差异较大时（如“坐下”等非运动类动作），引导效果可能下降。原文指出这种内容-风格冲突在局部肢体上尤为明显（Fig. 11），需要手动验证具体退化程度。

**物理真实感继承缺陷**：生成的运动仍可能出现脚部滑动等物理不真实现象，这是继承自预训练扩散模型的局限性，SMooDi 并未引入专门的物理约束或真感引导来缓解此问题。

**风格覆盖范围有限**：SMooDi 的风格空间受限于 100STYLE 数据集的 100 种风格标签，对于数据集中未包含的新风格，模型缺乏少样本适应或零样本泛化机制。

### 4. 开放问题与后续方向

1. **新风格适应**：如何将 SMooDi 扩展到 100STYLE 中未包含的新风格？基于少量样本的风格适应（few-shot style adaptation）或风格嵌入空间的插值/组合是值得探索的方向。

2. **推理加速**：能否通过减少去噪步数、采用一致性模型（consistency model）或蒸馏技术将推理时间降低到接近实时的水平？基于分类器的风格引导的计算优化（如缓存风格嵌入或近似梯度计算）也是可行的加速路径。

3. **物理约束集成**：引入物理约束或真感引导（realism guidance）是否能进一步消除脚部滑动并提升运动质量？这将使 SMooDi 更适用于游戏、动画等对物理真实感要求较高的应用场景。

4. **条件域泛化**：风格适配器的设计是否可推广到其他条件域（如骨骼结构、环境约束、交互物体）以实现更通用的条件运动生成？这涉及将“风格”概念从运动特征拓展到更广泛的条件表征空间。

## 原文 PDF

![[paperPDFs/ECCV_2024/SMooDi_Stylized_Motion_Diffusion_Model.pdf]]

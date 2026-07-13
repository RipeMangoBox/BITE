---
title: "DreamVideo: Composing Your Dream Videos with Customized Subject and Motion"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motion.pdf
project_link: null
code_link: null
aliases:
- DreamVideo
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过解耦主体学习和运动学习，分别引入轻量级身份适配器和运动适配器，并在推理时灵活组合，从而实现对任意主体和任意运动的定制。运动适配器使用外观引导来解耦运动与外观。"
primary_logic: "权重变化分析表明，空间交叉注意力层在主体外观学习中起关键作用，而所有时序层在运动学习中贡献相当；因此将身份适配器插入交叉注意力层，运动适配器插入所有时序层，并使用平行适配器设计。"
claims:
- "解耦主体与运动学习显著提升了定制灵活性和组合效果。"
- "身份适配器结合文本反转比单纯文本反转保留了更丰富的外观细节。"
- "运动适配器加入外观条件可有效避免运动学习阶段耦合外观信息。"
- "在所有指标上，DreamVideo在联合定制任务中均优于AnimateDiff、ModelScopeT2V和LoRA融合等方法。"
---

# DreamVideo: Composing Your Dream Videos with Customized Subject and Motion

> [!tip] 核心洞察
> 权重变化分析表明，空间交叉注意力层在主体外观学习中起关键作用，而所有时序层在运动学习中贡献相当；因此将身份适配器插入交叉注意力层，运动适配器插入所有时序层，并使用平行适配器设计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DreamVideo：定制主体与动作的个性化视频生成 |
| 英文题名 | DreamVideo: Composing Your Dream Videos with Customized Subject and Motion |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.04433) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DreamVideo |
| Dataset | 20个主体+30种运动模式，42条文本提示, 主体定制 (15类×8提示) |

> [!tip] 效果简介
> - 20个主体+30种运动模式，42条文本提示 上，CLIP-T 为 0.314，对比 0.298 (AnimateDiff)，变化 +0.016。
> - 20个主体+30种运动模式，42条文本提示 上，CLIP-I 为 0.665，对比 0.657 (AnimateDiff)，变化 +0.008。
> - 20个主体+30种运动模式，42条文本提示 上，DINO-I 为 0.452，对比 0.432 (AnimateDiff)，变化 +0.020。

## 概要

### 问题背景

现有视频生成定制方法面临一个关键瓶颈：它们通常只能单独控制**主体外观**或**运动模式**，无法在同一个生成框架内同时精确指定两者。以 **Textual Inversion**（Gal et al., 2023）为代表的主体定制方法能保留特定物体的外观，但缺乏对运动的控制；以 **Tune-A-Video**（Wu et al., 2023）为代表的运动定制方法能迁移运动模式，却容易在微调中耦合外观信息，导致主体特征丢失。当用户试图通过直接微调或合并 LoRA 参数来同时定制主体和运动时，不同学习目标之间会产生**融合冲突**，生成的视频往往在主体保真度、运动准确性和文本一致性三者之间顾此失彼。

### 核心思路

**DreamVideo** 的核心洞察在于：主体学习和运动学习对模型参数的影响模式截然不同。通过对预训练视频扩散模型进行权重变化分析（Figure 4），作者发现**空间交叉注意力层**在主体外观学习中起主导作用，而**所有时序层**在运动学习中的贡献相对均匀。基于这一发现，DreamVideo 将视频定制解耦为两个独立阶段：

- **主体学习**：首先通过文本反转学习一个粗粒度的文本身份标识，随后训练一个轻量级的**身份适配器**，仅插入交叉注意力层，以捕捉主体的精细外观细节。
- **运动学习**：设计一个**运动适配器**，插入所有时序层，并通过引入 CLIP 图像编码的外观条件，强制适配器专注于学习纯运动模式，避免外观信息的耦合。

两个适配器均采用瓶颈结构，参数量极小。推理时，只需将两个预训练好的适配器直接组合到冻结的基础模型上，无需任何额外训练即可生成同时保留目标主体身份和目标运动模式的视频。

### 方法定位

在方法谱系中，DreamVideo 属于**基于适配器的解耦式视频定制**方法。与 AnimateDiff（Guo et al., 2024）将运动模块附加到 DreamBooth 模型、ModelScopeT2V（Wang et al., 2023）分别微调空间/时间参数后合并、以及 LoRA 融合（Hu et al., 2021）等联合定制方案相比，DreamVideo 的核心差异在于：**训练阶段完全解耦**，推理阶段**即插即用**，从根本上避免了参数层面的融合冲突。

### 主要结果

在包含 20 个定制主体和 30 种运动模式的联合定制评测中，DreamVideo 在所有自动指标上均优于现有方法：CLIP-T 达到 0.314（AnimateDiff 为 0.298），DINO-I 达到 0.452（AnimateDiff 为 0.432）。用户调研中，DreamVideo 的运动保真度偏好率高达 82.4%，远超 AnimateDiff 的 17.6%。消融实验证实，文本反转身份学习、运动适配器以及外观引导三个组件各自对最终性能有独立贡献，移除任一组件均会导致指标下降或生成质量劣化。

### 视频生成与个性化定制的兴起

近年来，扩散模型在图像和视频生成领域取得了显著进展，催生了大量文本到视频（T2V）的基础模型。这些模型能够根据文本描述生成逼真且多样化的视频内容，展现出强大的生成能力。然而，在实际应用中，用户往往不仅希望生成通用场景，更渴望将特定的视觉主体和特定的运动模式注入生成过程，实现高度个性化的视频创作。

这种需求催生了视频定制（video customization）这一研究方向。其核心挑战在于：如何让预训练的视频生成模型在保留原始泛化能力的同时，精确地捕捉用户提供的特定主体外观和特定运动模式。

### 现有方法的局限：单一维度与融合冲突

当前视频定制方法存在一个根本性的瓶颈——它们通常只关注主体或运动的单一维度，无法同时控制两者。

在主体定制方面，以**Textual Inversion**（Gal et al., 2023）、**Dreamix**（Molad et al., 2023）和**Custom Diffusion**（Kumari et al., 2023）为代表的方法，通过微调模型参数或学习特定文本嵌入来绑定主体身份。这些方法能够较好地保留静态图像中的外观特征，但生成的视频往往缺乏运动多样性，只能呈现基础的、缺乏变化的动作。

在运动定制方面，**Tune-A-Video**（Wu et al., 2023）等方法通过对给定视频进行微调来学习运动模式。然而，这类方法在微调过程中容易将运动信息与视频中的外观信息耦合在一起，导致生成结果中主体外观被污染或替换。

当试图将两者结合时，问题更加突出。一个直观的思路是分别训练主体和运动的微调参数，然后在推理时合并——例如分别训练空间和时间的 LoRA 权重后叠加。但这种做法常常遭遇**融合冲突**：主体保真度和运动准确性相互干扰，最终生成的主体外观扭曲或运动模式模糊。直接对整个模型进行联合微调则面临过拟合风险，且计算开销巨大。

### 本文动机：解耦定制与灵活组合

上述困境的根源在于，主体外观和运动模式在视频生成模型中纠缠在共享的参数空间中。强行在同一组参数上优化两个目标，必然导致梯度冲突和表征混淆。

DreamVideo 的核心动机正是打破这种纠缠。其关键洞察是：**将视频定制解耦为主体学习和运动学习两个独立阶段**，分别引入轻量级的身份适配器和运动适配器，并在推理时灵活组合。这种解耦策略既能降低模型优化的复杂度，又能让用户像搭积木一样自由搭配任意主体与任意运动，实现前所未有的定制灵活性。

此外，为克服运动学习中的外观耦合问题，DreamVideo 在运动适配器中引入了**外观引导**机制——将训练视频中的一帧图像作为条件输入，迫使适配器仅关注运动模式本身，而非外观信息。这一设计从结构层面确保了运动与外观的真正分离。

## 核心方法与创新机理

DreamVideo 的核心创新在于将视频定制任务解耦为**主体学习**与**运动学习**两个独立阶段，从根本上解决了现有方法仅能控制单一维度（主体或运动）的瓶颈。这种解耦设计通过两个关键机制实现。

**1. 两阶段主体学习：文本反转 + 身份适配器**

传统方法如 **Textual Inversion**（Gal et al., 2023）仅学习一个伪词嵌入来表示主体，难以捕捉精细外观细节；而完全微调则易导致过拟合。DreamVideo 采用级联策略：首先通过文本反转优化一个粗粒度的“文本身份” $S^*$，然后在冻结该嵌入和基座模型的前提下，训练一个轻量级**身份适配器**来捕获主体的精细外观。该适配器采用瓶颈结构（下投影-非线性激活-上投影）加残差连接，前向过程为：

$$h_{t}' = h_{t} + \sigma\left(h_{t} * \mathbf{W}_{\mathrm{down}}\right) * \mathbf{W}_{\mathrm{up}}$$

这种设计使得主体外观信息被显式地注入到空间隐状态中，同时避免了文本嵌入空间的容量瓶颈。

**2. 外观引导的运动适配器：强制解耦运动与外观**

运动定制的主要挑战在于时空信息的耦合——直接微调时间参数（如 **Tune-A-Video**, Wu et al., 2023）会不可避免地学习外观特征，导致在组合新主体时产生冲突。DreamVideo 的解决方案是设计一个**运动适配器**，并引入**外观引导**机制：从训练视频中随机抽取一帧，通过 CLIP 图像编码器获得嵌入 $e$，将其广播后注入适配器：

$$\hat{h}_{t}^{e} = \hat{h}_{t} + \mathrm{broadcast}(e * \mathbf{W}_{\mathrm{cond}})$$

$$\hat{h}_{t}' = \hat{h}_{t} + \sigma(\hat{h}_{t}^{e} * \mathbf{W}_{\mathrm{down}}) * \mathbf{W}_{\mathrm{up}}$$

外观条件的存在迫使适配器在已知外观信息的前提下仅学习运动模式，从而在推理时与任意身份适配器组合时不会引入外观污染。

**3. 基于权重分析的适配器插入策略**

DreamVideo 并非盲目地将适配器插入所有层。作者通过分析微调过程中各层参数的权重变化率 $\Delta_{l} = \frac{\lVert \boldsymbol{\theta}_{l}' - \boldsymbol{\theta}_{l} \rVert_{2}}{\lVert \boldsymbol{\theta}_{l} \rVert_{2}}$，发现**空间交叉注意力层在主体外观学习中起关键作用**，而**所有时序层对运动学习的贡献相当**。据此，身份适配器仅插入交叉注意力层，运动适配器则插入时序 Transformer 的所有层，实现了参数效率与定制效果的最优平衡。

**4. 解耦训练与灵活组合**

与 **LoRA**（Hu et al., 2021）融合或 **AnimateDiff**（Guo et al., 2024）等需要联合训练或参数合并的方案不同，DreamVideo 的两个适配器完全独立训练，推理时直接组合。消融实验证实，这种适配器设计相比 LoRA 融合能更好地缓解冲突，实现更和谐的主体-运动组合（见 Table A4, Fig. A7）。整个过程中预训练视频扩散模型始终保持冻结，仅需优化极小部分参数。

DreamVideo 将个性化视频生成任务**解耦为主体学习与运动学习两个独立阶段**，以降低优化复杂度并提升组合灵活性。其核心 pipeline 由以下模块串联构成：

1. **冻结的预训练视频扩散模型**：作为基础生成引擎，整个训练过程保持冻结，确保基座模型的通用文本到视频生成能力不被破坏。
2. **文本反转**：在主体学习的第一阶段，为每个主体学习一个伪词 $S^*$ 的嵌入，作为粗粒度的文本身份标识。
3. **身份适配器**：在主体学习的第二阶段，以冻结的文本身份为条件，训练一个轻量级瓶颈适配器，专门捕获主体的精细外观细节。该适配器仅插入空间交叉注意力层。
4. **运动适配器**：在运动学习阶段，训练另一个轻量级瓶颈适配器来建模目标运动模式。该适配器插入时序 Transformer 的所有层，并额外接收来自 CLIP 图像编码器的外观引导，以强制解耦运动与外观信息。
5. **外观引导**：从训练视频中随机抽取一帧，经 CLIP 图像编码器提取嵌入，作为运动适配器的条件输入，避免运动学习阶段耦合外观特征。

**输入输出流**：主体学习阶段输入静态主体图像，输出文本身份嵌入与身份适配器权重；运动学习阶段输入运动参考视频，输出运动适配器权重。推理时，将两个轻量适配器直接组合加载到冻结的基础模型中，无需额外训练，即可根据任意文本提示生成同时保留指定主体身份与运动模式的视频。

这一解耦设计的核心洞察来自权重变化分析：空间交叉注意力层在主体外观学习中起关键作用，而所有时序层在运动学习中贡献相当。据此，身份适配器被精准插入交叉注意力层，运动适配器则覆盖全部时序层，并以平行适配器形式实现，以最大化定制效果。

DreamVideo 将定制视频生成解耦为主体学习与运动学习两个阶段，通过两个轻量适配器实现。整体框架如 Figure 2 所示，两个适配器的结构细节如 Figure 3 所示。

### 基础视频扩散模型

方法构建于预训练视频扩散模型之上，其训练目标为标准的噪声预测重构损失：

$$\mathcal{L} = \mathbb{E}_{z, c, \epsilon \sim \mathcal{N}(0, \mathrm{I}), t} \left[ \left\| \epsilon - \epsilon_{\theta} \left(z_{t}, \tau_{\theta}(c), t \right) \right\|_{2}^{2} \right]$$

其中 $z$ 为视频隐空间编码，$c$ 为文本条件，$\epsilon$ 为添加的高斯噪声，$\epsilon_{\theta}$ 为去噪网络，$\tau_{\theta}$ 为文本编码器，$t$ 为扩散时间步。整个训练过程中，预训练视频扩散模型的参数保持冻结。

### 身份适配器

身份适配器用于捕获主体的精细外观细节，采用瓶颈结构配合残差连接。其前向过程为：

$$h_{t}' = h_{t} + \sigma\left(h_{t} * \mathbf{W}_{\mathrm{down}}\right) * \mathbf{W}_{\mathrm{up}}$$

其中 $h_{t}$ 为空间隐状态（来自交叉注意力层），$\mathbf{W}_{\mathrm{down}}$ 和 $\mathbf{W}_{\mathrm{up}}$ 分别为下投影和上投影矩阵，$\sigma$ 为非线性激活函数。该适配器仅插入交叉注意力层，这一设计源于权重变化分析：在主体学习中，交叉注意力层的参数变化最为显著（Figure 4），是外观信息注入的关键位置。

### 运动适配器

运动适配器同样采用瓶颈结构，但额外引入了外观引导机制，以强制适配器仅学习运动模式，避免耦合外观信息。具体而言，从训练视频中随机抽取一帧，通过 CLIP 图像编码器获得嵌入 $e$，将其作为条件注入：

$$\hat{h}_{t}^{e} = \hat{h}_{t} + \mathrm{broadcast}(e * \mathbf{W}_{\mathrm{cond}})$$

其中 $\hat{h}_{t}$ 为时间隐状态，$\mathbf{W}_{\mathrm{cond}}$ 为条件线性投影矩阵，$\mathrm{broadcast}$ 表示将投影后的嵌入广播到所有帧。注入外观条件后，再通过瓶颈结构提取运动特征：

$$\hat{h}_{t}' = \hat{h}_{t} + \sigma(\hat{h}_{t}^{e} * \mathbf{W}_{\mathrm{down}}) * \mathbf{W}_{\mathrm{up}}$$

运动适配器插入时序 Transformer 的所有层，因为权重变化分析表明，在运动学习中所有时序层的贡献相当，不存在单一关键层。

### 适配器插入位置的决策依据

为了确定适配器的最佳插入位置，作者进行了权重变化分析。定义第 $l$ 层的权重变化率为：

$$\Delta_{l} = \frac{\lVert \boldsymbol{\theta}_{l}' - \boldsymbol{\theta}_{l} \rVert_{2}}{\lVert \boldsymbol{\theta}_{l} \rVert_{2}}$$

其中 $\boldsymbol{\theta}_{l}$ 为预训练参数，$\boldsymbol{\theta}_{l}'$ 为微调后参数。分析结果（Figure 4）显示：在空间参数中，交叉注意力层的 $\Delta_{l}$ 显著高于其他层，表明其是主体外观学习的关键；而在时间参数中，各层的 $\Delta_{l}$ 分布较为均匀。据此，身份适配器仅插入交叉注意力层，运动适配器则插入所有时序层。

## 实验与关键发现

### 实验设置

DreamVideo 在三个层次的定制任务上进行评估：主体定制、运动定制，以及二者的联合定制。主体定制数据集包含 20 个定制主体（9 只宠物和 11 个物体），运动定制数据集包含 30 种运动模式。对于联合定制，实验从 20 个主体和 30 种运动中随机组合，配合 42 条文本提示生成视频。所有方法统一使用相同的预训练基础模型 ModelScopeT2V（**Wang et al., 2023**），仅 AnimateDiff 和 Tune-A-Video 因方法设计限制使用 Stable Diffusion v1.5。推理阶段均采用 DDIM 50 步采样，分类器自由引导尺度 9.0，生成 32 帧、256×256 分辨率、8fps 的视频。训练与推理均在单块 NVIDIA A100 GPU 上完成。

评估指标包括：CLIP-T（文本对齐度）、CLIP-I 和 DINO-I（主体保真度），以及 Temporal Consistency（时序一致性）。联合定制任务还进行了人工用户调研，从文本对齐、主体保真度、运动保真度和时序一致性四个维度收集偏好率。

### 联合定制主结果

联合定制是 DreamVideo 的核心目标场景——同时保留指定主体的外观身份和指定运动的动态模式。Table 1 报告了与三类基线的定量对比：

- **AnimateDiff**（Guo et al., 2024）：在 DreamBooth 微调模型上附加运动模块。
- **ModelScopeT2V**（Wang et al., 2023）：分别微调空间/时间参数后合并。
- **LoRA 融合**（Hu et al., 2021）：分别训练空间/时间 LoRA 后合并。

DreamVideo 在所有指标上均取得最优：CLIP-T 达到 0.314（AnimateDiff 为 0.298），CLIP-I 达到 0.665（AnimateDiff 为 0.657），DINO-I 达到 0.452（AnimateDiff 为 0.432）。值得注意的是，DreamVideo 的适配器参数量仅为 24M，远低于 AnimateDiff 的 1.36B 和 ModelScopeT2V 的 1.7B，体现了轻量解耦设计的参数效率优势。

定性结果（Figure 5）进一步揭示：AnimateDiff 和 ModelScopeT2V 在联合定制时存在明显的融合冲突——要么主体外观退化，要么运动模式无法准确呈现。LoRA 融合虽能部分保留主体和运动，但常产生不和谐的视觉伪影。DreamVideo 通过解耦训练和推理时直接组合两个独立适配器，有效缓解了这种冲突，生成的主体身份和运动模式均保持高度保真。

![[assets/figures/papers/paper_list_l34_DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motio/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of customized video generation with both subjects and motions. DreamVideo accurately preserves both subject identity and motion pattern, while other methods suffer from fusion conflicts to some extent. Note that the results of Animate-Diff are generated by fine-tuning its provided pre-trained motion module and appending it to a DreamBooth [52] model*

用户调研（Table 4）提供了更强的主观证据：在运动保真度维度上，DreamVideo 对 AnimateDiff 的偏好率高达 82.4% vs. 17.6%；在文本对齐维度上为 72.3% vs. 27.7%；在主体保真度和时序一致性上也分别达到 62.3% 和 64.2% 的偏好率。这表明解耦策略在用户感知层面同样具有显著优势。

### 主体定制与运动定制单独评估

为验证各模块在单一维度上的能力，论文还分别在主体定制和运动定制任务上进行了独立评估。

**主体定制**（Table 2）：与 Textual Inversion（Gal et al., 2023）、Dreamix（Molad et al., 2023）等方法对比，DreamVideo 在 15 类主体 × 8 条文本提示的测试集上取得最优 DINO-I（0.475 vs. Dreamix 的 0.459）和 CLIP-T（0.295 vs. Dreamix 的 0.284）。定性结果（Figure 6）显示，纯 Textual Inversion 仅能保留粗粒度类别特征，缺乏精细外观细节；Dreamix 虽有所改进，但在某些视角下主体身份仍会漂移。DreamVideo 的两阶段策略——先用文本反转学习粗粒度概念，再用身份适配器捕获精细外观——在主体保真度上表现更稳健。

**运动定制**（Table 3）：在 20 种运动 × 6 条文本提示的测试集上，DreamVideo 的 CLIP-T 达到 0.309（ModelScopeT2V 为 0.293），Temporal Consistency 达到 0.975（ModelScopeT2V 为 0.971）。与 Tune-A-Video（Wu et al., 2023）相比，DreamVideo 的优势在于运动适配器中融入了外观引导（appearance guidance），强制适配器仅学习运动模式而非耦合外观信息。Figure 7 的定性对比证实：Tune-A-Video 在运动学习过程中会将源视频的外观“泄漏”到生成结果中，导致背景或主体颜色被污染；DreamVideo 则能有效避免这种时空信息耦合。

### 消融实验

Table 5 和 Figure 8 系统消融了 DreamVideo 的三个核心组件：

- **移除文本反转身份（w/o textual identity）**：仅使用身份适配器学习主体，CLIP-T 从 0.314 降至 0.310，DINO-I 从 0.452 降至 0.445。定性结果显示，生成的主体丢失了部分外观细节（如纹理和颜色精度下降），说明文本反转提供的粗粒度语义锚定对后续适配器学习至关重要。
- **移除运动适配器（w/o motion adapter）**：仅保留主体定制部分，CLIP-T 从 0.314 降至 0.299，Temporal Consistency 从 0.971 降至 0.964。生成视频完全无法呈现目标运动模式，验证了运动适配器在动态建模中的不可替代性。有趣的是，仅做主体定制时 CLIP-I 和 DINO-I 反而略高（0.701 vs. 0.665，0.475 vs. 0.452），这是因为运动学习引入了一定的外观扰动，属于合理的 trade-off。
- **移除外貌引导（w/o appearance guidance）**：在运动适配器中去掉 CLIP 图像条件，CLIP-T 降至 0.305，DINO-I 降至 0.445。生成视频中主体身份和背景受到轻微破坏，证实了外观引导在解耦时空信息中的关键作用——没有它，运动适配器会走“捷径”学习外观特征。

此外，附录中的补充消融（Table A4）比较了适配器与 LoRA 的融合效果：在联合定制场景下，LoRA 融合会产生更明显的冲突伪影，而适配器的瓶颈结构能更好地缓解融合冲突。Table A5 进一步表明，在运动定制中，在所有时序层使用平行适配器（parallel adapter）性能最优。

### 失败模式与局限性

尽管 DreamVideo 在多数场景下表现优异，论文明确指出了以下失败模式：

1. **多主体/多运动不支持**：当前方法仅能定制单个主体和单个运动，无法生成包含多个主体或多个运动的视频。例如，无法同时定制“一只猫”和“一只狗”各自执行不同运动。
2. **基础模型能力瓶颈**：某些在预训练中关联较弱的组合（如“狼骑自行车”）可能生成失败，这是基座模型 VideoCrafter 的固有限制，非定制方法本身可解决。
3. **单视频运动定制的精度上限**：在仅提供一个参考视频的运动定制场景中，方法仅能学习大致运动模式（如“向前跑”），无法达到逐帧精确对应。这是少样本运动学习的共性难题。
4. **主体混淆**：当组合涉及多个外观相似的物体时（如“猫”和“马”同时出现），注意力图可能发生混淆，导致主体身份混合。

这些失败模式指向了开放问题：如何设计融合模块以集成多个主体和运动？能否进一步解耦注意力图使各主体保持独立？是否可能训练一个通用的、一次推理即可完成多种定制的视频扩散模型？

![[assets/figures/papers/paper_list_l34_DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motio/figures/004_Figure_4.jpg]]
*Figure 4: Analysis of weight change on updating all spatial or temporal model weights during fine-tuning. We observe that crossattention layers play a key role in subject learning while the contributions of all layers are similar to motion learning*

![[assets/figures/papers/paper_list_l34_DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motio/figures/006_Figure.jpg]]
*Figure: cat a dog eating grass from under the snow a cat eating grass from under the sand*

![[assets/figures/papers/paper_list_l34_DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motio/figures/008_Figure.jpg]]
*Figure: a bear walking on some rocks (Single video)*

![[assets/figures/papers/paper_list_l34_DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motio/figures/017_Table.jpg]]
*Table: A3. Human evaluations on customizing motions between our method and alternatives. Table A4. Quantitative comparison of video customization between Adapter and LoRA. “T. Cons.” denotes Temporal Consistency. “Para.” means parameter number*

![[assets/figures/papers/paper_list_l34_DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motio/figures/020_Figure.jpg]]
*Figure: A1. Qualitative comparison of customized video generation with both subjects and motions. Subject Custom Diffusion DreamVideo (ours)*

## 定位与知识库关联

DreamVideo 处于视频扩散模型定制化生成的交叉地带，其核心贡献在于首次将“主体定制”与“运动定制”解耦为两个独立、可组合的学习过程。以下从基线关系、适用边界、已知局限与开放问题四个维度进行定位。

### 与基线方法的关系

**主体定制基线。** 传统图像主体定制方法如 **Textual Inversion** (Gal et al., ICLR 2023) 仅学习一个文本嵌入来表示主体，缺乏对精细外观细节的捕获能力；**Dreamix** (Molad et al., 2023) 通过对整个模型进行微调来保留主体身份，但计算开销大且难以与运动模块组合。DreamVideo 采用两阶段策略——先用 Textual Inversion 学习粗粒度文本身份，再通过冻结基座、仅训练身份适配器来捕获精细外观——在保留主体保真度的同时大幅降低了可训练参数量。定量结果（Table 2）显示，DreamVideo 在 CLIP-T 和 DINO-I 上分别达到 0.295 和 0.475，均优于 Dreamix 的 0.284 和 0.459。

**运动定制基线。** **Tune-A-Video** (Wu et al., ICCV 2023) 通过对单视频微调 UNet 的时间参数来学习运动模式，但存在严重的外观耦合问题——学习到的运动模块会“记住”训练视频中的主体外观，导致在更换主体时生成质量下降。DreamVideo 的运动适配器通过引入 CLIP 图像外观条件（Equation 3-4），强制适配器仅关注时序运动模式，有效缓解了这一耦合。Table 3 表明，DreamVideo 在运动定制任务上的 CLIP-T 达到 0.309，优于 ModelScopeT2V 的 0.293。

**联合定制基线。** 现有方法试图通过参数合并来实现联合定制：**AnimateDiff** (Guo et al., 2024) 将运动模块附加到 DreamBooth 微调后的模型上；**ModelScopeT2V** (Wang et al., 2023) 分别微调空间/时间参数后合并；**LoRA 融合** (Hu et al., 2021) 分别训练空间/时间 LoRA 后组合。这些方法均面临“融合冲突”——主体保真度与运动保真度难以兼得，因为空间和时间参数在微调时相互干扰。DreamVideo 通过解耦训练、推理时直接组合两个轻量适配器，无需额外训练即可实现和谐的组合效果。Table 1 显示，DreamVideo 在 CLIP-T、CLIP-I、DINO-I 上分别达到 0.314、0.665、0.452，全面优于 AnimateDiff 的 0.298、0.657、0.432。用户调研（Table 4）进一步表明，DreamVideo 在运动保真度上的偏好率高达 82.4%，远超 AnimateDiff 的 17.6%。

### 适用边界

DreamVideo 的适用边界由三个因素共同界定：

1. **单主体-单运动组合。** 当前方法仅支持定制单个主体与单个运动模式，无法生成包含多个主体或多个运动的视频。这是解耦设计的直接后果——身份适配器和运动适配器各为一个实体服务，缺乏多实体融合机制。

2. **基础模型的先验约束。** 生成质量受限于预训练视频扩散模型（ModelScopeT2V）的固有能力。对于预训练中关联较弱的组合（如“狼骑自行车”），模型可能无法生成合理结果，因为基础模型缺乏相应的先验知识。

3. **运动定制的粒度。** 在单视频运动定制场景下，运动适配器仅能学习大致运动模式（如“熊走路”的整体节奏），无法实现逐帧精确对应。这是因为适配器的瓶颈结构天然具有信息压缩效应，牺牲了细粒度时序细节以换取泛化性。

### 已知局限

论文明确指出的局限包括：

- **多主体混淆。** 当文本提示包含多个物体（如“猫”和“马”）时，身份适配器可能无法准确区分各主体，导致外观特征混淆。
- **运动泛化边界。** 运动适配器在训练视频与目标视频的场景差异较大时，运动迁移的保真度会下降。这一现象的因果机制尚不明确，需进一步验证。
- **推理效率。** 尽管适配器参数量小（约 50M），但推理时仍需加载完整的预训练视频扩散模型，生成一段 32 帧视频在单块 A100 上仍需数秒。

### 开放问题

论文提出了四个值得后续探索的方向：

1. **多主体多运动融合。** 如何设计融合模块以集成多个身份适配器和运动适配器，实现包含多个主体和多个运动的通用定制视频生成？这需要解决注意力图的解耦问题，使每个主体在组合时保持独立，避免混淆。

2. **通用定制模型。** 是否可以训练一个通用的视频扩散模型，在单次推理中即可完成多种主体和运动的定制，而无需为每个新主体/运动重新训练适配器？这类似于图像定制中“一次性学习”的扩展。

3. **逐帧精确运动对应。** 如何改进运动适配器的结构（例如引入光流或轨迹条件），使其在单视频定制中实现更精确的逐帧运动对应，而非仅学习统计性的运动模式？

4. **解耦注意力机制。** 能否进一步解耦交叉注意力图中的主体区域与背景区域，使身份适配器仅作用于主体对应的空间位置，从而在多主体场景下避免特征污染？

## 原文 PDF

![[paperPDFs/CVPR_2024/DreamVideo_Composing_Your_Dream_Videos_with_Customized_Subject_and_Motion.pdf]]

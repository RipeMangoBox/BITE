---
title: Customizing Motion in Text-to-Video Diffusion Models
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/Customizing_Motion_in_Text_to_Video_Diffusion_Models.pdf
project_link: https://joaanna.github.io/customizing\_motion/
code_link: null
aliases:
- CMTVDM
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 微调预训练文本到视频扩散模型的时间层和空间跨注意力层的键/值参数，使得模型能够学习新运动，并通过视频正则化和非均匀时间步采样防止遗忘和外观过拟合。
primary_logic: 利用预训练模型中的运动先验，仅调整影响运动表示的特定参数（时间层和空间K/V投影），并引入真实视频正则化与粗噪声时间步采样，可以在少量样本下学会可泛化的运动模式，同时保留原始生成能力。
claims:
- 仅微调时间层和空间K/V参数即可在运动准确率和外观复制之间取得最佳平衡。
- 真实视频正则化显著优于无正则化或合成正则化。
- 粗噪声时间步采样策略提高了运动准确性并降低了外观复制。
- Jester (custom gestures) 上 Motion Accuracy (%) = 70.6
---

# Customizing Motion in Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 利用预训练模型中的运动先验，仅调整影响运动表示的特定参数（时间层和空间K/V投影），并引入真实视频正则化与粗噪声时间步采样，可以在少量样本下学会可泛化的运动模式，同时保留原始生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 定制文本到视频扩散模型中的运动 |
| 英文题名 | Customizing Motion in Text-to-Video Diffusion Models |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2312.04966) · [Project](https://joaanna.github.io/customizing\_motion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NewMove |
| Dataset | Jester, User Study |

> [!tip] 效果简介
> - Jester (custom gestures) 上，Motion Accuracy (%) 70.6 vs DreamBooth (+42.2)；Motion Accuracy (%) 70.6 vs Textual Inversion (+70.3)。
> - User Study 上，User Preference (% votes) Significantly preferred (p<0.01) vs DreamBooth & Tune-A-Video (N/A)。

## 概要

**核心问题：** 现有文本到视频（T2V）扩散模型能够根据文本描述生成视频，但其运动模式受限于训练数据分布，无法生成训练集中未出现的新运动。传统运动迁移方法（如基于视频的运动重定向）通常无法将运动与外观完全解耦，难以泛化到新场景、新主体甚至非人形角色。

**方法定位：** 本文提出 **NewMove**，一种基于预训练T2V模型微调的运动定制方法。其核心思路是：给定少量（通常3–5个）展示同一运动模式的示例视频，通过选择性微调模型U-Net中的**时间层**（temporal convolution/attention）和**空间交叉注意力层的键/值投影**（spatial K/V），将新运动编码为一个唯一运动标识符（`V*`），从而在测试时通过文本提示（如“A robot doing the V* dance”）将该运动迁移到任意新外观和场景中。该方法在方法谱系上介于文本驱动的视频生成与少样本运动迁移之间，区别于全参数微调（如DreamBooth）、文本嵌入学习（如Textual Inversion）或仅时间层调整（如Tune-A-Video、AnimateDiff），其关键在于**参数子集的选择性微调**配合**真实视频正则化**和**非均匀时间步采样**，实现了运动-外观解耦与遗忘抑制的平衡。

**主要结果：** 在Jester手势数据集上，NewMove的运动识别准确率达**70.6%**，较DreamBooth（28.4%）和Textual Inversion（0.3%）提升显著；用户偏好研究中，NewMove在运动准确性和外观泛化性上均显著优于基线方法（p<0.01）。消融实验证实：仅微调空间K/V和时间层是运动-外观解耦的关键（Table 2a）；真实视频正则化（Jester）比无正则化在准确率上提升约27个百分点（70.6 vs 43.9，Table 2e）；粗噪声时间步采样（Coarse-noise）比均匀采样提高3.7%准确率并大幅降低外观复制分数（Table 2d）。



文本到视频生成模型近年来取得了显著进展，能够根据自然语言描述生成多样化、时序连贯的视频内容。然而，这些模型受限于训练数据的分布，难以生成训练集中未覆盖的**新运动模式**——例如特定的舞蹈动作、自定义手势或独特的相机运动轨迹。用户若希望模型生成“Carlton舞”或“滑动双指向上”等特定动作，仅凭文本描述往往无法精确传达运动细节，而模型也缺乏对这类新运动的表征能力。

现有的定制化方法主要面向**外观定制**，即通过少量样本教会模型生成特定物体或角色的外观。代表性工作包括 **Textual Inversion**（Gal et al., ICLR 2023），通过优化文本嵌入来捕获新概念；**DreamBooth**（Ruiz et al., CVPR 2023），微调整个扩散模型并结合类别先验正则化；以及 **Tune-A-Video**（Wu et al., ICCV 2023），将图像扩散模型扩展至视频领域进行微调。然而，这些方法在**运动定制**任务上表现不佳：外观定制方法难以将运动模式与外观表征解耦，导致生成结果要么无法准确复现目标运动，要么过度复制训练样本的外观，缺乏对新场景的泛化能力。

另一方面，传统的**运动迁移**方法试图将源视频中的运动转移到目标主体上，但它们通常依赖显式的结构对应（如人体姿态或光流），难以泛化到非人主体或多主体场景，且无法与文本驱动的生成流程无缝集成。

上述现状揭示了一个核心瓶颈：**如何在保留预训练文本到视频模型丰富先验知识的前提下，仅通过少量样本教会模型一种新的运动模式，并将其泛化到任意外观和场景中？** 这要求方法同时解决三个子问题：（1）确定模型中哪些参数负责表征运动信息；（2）在微调过程中防止对少量样本的过拟合和对外观的记忆；（3）确保新学到的运动不会覆盖模型原有的生成能力。

本文提出的 **NewMove** 方法正是针对这一瓶颈展开。其核心洞见在于：预训练文本到视频扩散模型的U-Net架构中，**时间层**（temporal convolution and attention layers）负责建模帧间动态，而**空间交叉注意力层的键/值投影**（key/value projections in spatial cross-attention）负责将文本标识符映射到视觉特征。通过仅微调这两类参数，并辅以**真实视频正则化**和**非均匀时间步采样**策略，NewMove 能够在少量样本下学会可泛化的运动模式，同时将运动与外观解耦，在运动准确率和外观复制之间取得最佳平衡。



## 核心方法与创新机理

本文提出的 **NewMove** 方法围绕一个核心洞察展开：预训练的文本到视频扩散模型内部已蕴含丰富的运动先验，只需对影响运动表示的特定参数子集进行微调，并辅以针对性的正则化与采样策略，即可在极少量样本下学会可泛化的新运动模式，同时保留模型的原始生成能力。

相对于现有运动定制基线方法，NewMove 的关键创新体现在以下三个 **changed slots** 上：

**1. 微调参数选择：仅更新时间层与空间K/V投影**

与 **Textual Inversion**（Gal et al., ICLR 2023）仅优化文本嵌入、或 **DreamBooth**（Ruiz et al., CVPR 2023）/ **Tune-A-Video**（Wu et al., ICCV 2023）通常微调全部或大量参数不同，NewMove 精确地将可训练参数限制在 U-Net 的**时间卷积与注意力层**以及**空间交叉注意力层的键（K）和值（V）投影**（Fig. 2）。消融实验（Table 2a）提供了决定性证据：仅训练空间层 K/V 可将外观复制分数降低两倍以上，同时运动准确率提升约 8%，在运动准确率与外观解耦之间取得了最佳平衡。这一参数选择策略的因果机制在于：时间层负责建模帧间运动动态，而空间 K/V 投影控制文本标识符到视觉特征的映射——仅调整这两个接口即可注入新运动，同时避免扰动空间外观生成能力。

**2. 正则化策略：真实视频正则化集替代合成/无正则化**

多数定制方法使用合成图像/视频或类别先验进行正则化，NewMove 则引入**真实视频正则化集** $D^r$（如 Jester 相关手势视频），在微调目标中联合优化目标运动样本与正则化样本（Eq. 3）。Table 2e 显示，使用真实正则化集（Jester）的运动准确率达 70.6%，复制分数仅 8.7%；而无正则化时复制分数虽极低（1.2%），但运动准确率灾难性下降至 43.9%。合成正则化同样远逊于真实正则化。这一设计的瓶颈突破在于：真实相关视频能有效锚定模型原有的运动知识边界，防止微调过程中的灾难性遗忘。

**3. 时间步采样：非均匀分布偏重早期去噪**

传统扩散模型训练采用均匀时间步采样，NewMove 提出非均匀概率分布 $f_{\alpha}(t) = \frac{1}{T}(1 - \alpha \cos(\frac{\pi t}{T}))$（$\alpha=0.5$），使训练采样偏重早期去噪步骤。其因果机制在于：扩散过程的早期步骤决定视频的全局运动结构，而后期步骤填充外观细节——偏重早期步骤迫使模型聚焦于学习运动模式本身，而非复制训练样本的外观。Table 2d 的消融结果证实了该策略的有效性：粗噪声采样（Coarse-noise）相比均匀采样，运动准确率从 66.9 提升至 70.6，复制分数从 15.4 降至 8.7。

值得注意的辅助发现是，全微调（Full fine-tuning）在运动准确率上远超 LoRA（70.6 vs 10.6，Table 2f），表明参数高效微调方法在该任务上存在显著局限，需进一步验证其适用边界。



**NewMove** 的整体 pipeline 围绕一个冻结的预训练文本到视频扩散模型展开，通过选择性微调与两项正则化设计，在少量样本视频上学习可泛化的运动模式。其核心模块关系与数据流如下：

### 输入与运动标识符

给定一个包含 3–5 个示例视频的小样本集 $D^{m}$，所有视频共享同一运动模式但外观不同。该运动被绑定到一个新的唯一运动标识符（如 `V* dance`），在推理时通过文本提示调用，例如 *“A female firefighter doing the V* sign”*。

### 基础模型与可训练参数选择

NewMove 使用预训练的文本到视频扩散 U-Net（基于 Modelscope T2V）作为基础模型。与传统微调策略不同，该方法仅更新两类参数：
- **时间层参数 $\theta_{t}$**：包括时间卷积和时间注意力层，负责建模帧间运动动态；
- **空间跨注意力层的键/值投影 $\theta_{s}^{k,v}$**：将运动标识符映射到视觉特征，同时解耦运动与外观。

冻结其余空间层参数，使模型保留原有的外观生成能力，避免对新运动样本的过拟合。

### 训练目标与正则化

微调采用标准加权去噪损失：

$$
\mathcal{L}_{\theta}(x, c) = \underset{\epsilon \sim \mathcal{N}(0,1)}{\mathbb{E}} [ w_t \| \epsilon_{\theta}(x, \epsilon, c, t) - \epsilon \|_2^2 ]
$$

为防止模型遗忘已学到的相关运动概念，引入**真实视频正则化集** $D^{r}$（如 Jester 数据集中与目标运动相关的其他手势视频），优化目标扩展为：

$$
\operatorname*{min}_{\theta} \sum_{(x,c) \sim D^{m} \cup D^{r}} \mathcal{L}_{\theta}(x,c)
$$

消融实验证实，真实正则化集在运动准确率（70.6%）和外观复制分数（8.7%）之间取得最优平衡，而无正则化时复制分数虽低，但运动准确率灾难性下降至 43.9%。

### 非均匀时间步采样

训练时采用偏斜的时间步采样分布，强调早期去噪步骤以聚焦于运动结构而非外观细节：

$$
f_{\alpha}(t) = \frac{1}{T}(1 - \alpha \cos(\frac{\pi t}{T}))
$$

其中 $\alpha=0.5$ 用于所有实验。该策略使运动准确率从均匀采样的 66.9% 提升至 70.6%，同时将外观复制分数从 15.4% 降至 8.7%。

### 推理流程

训练完成后，用户通过文本提示中的运动标识符调用学习到的运动。模型在推理时利用微调后的时间层和空间 K/V 投影，将运动模式泛化至新外观、多主体甚至非人形角色，同时保持时间一致性。

### 补充图表

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/003_Figure_2.jpg]]
*Figure 2: Overview. Given a small set of exemplar videos, our approach fine-tunes the U-Net of a text-to-video model using a reconstruction objective. The motion is identified with a unique motion identifier and can be used at test time to synthesize novel subjects performing the motion. To represent the added motion but preserve information from the pretrained model, we tune a subset of weights – the temporal convolution and attention layers, in addition to the key & value layers in the spatial attention layer. A set of related videos is used to regularize the tuning process*

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/001_Figure_1.jpg]]
*Figure 1: (Left) Given a few examples (“Carlton dance”), our customization method learns the dynamic motion pattern common to the input examples and incorporates it into a pre-trained text-to-video diffusion model using a new motion identifier (“V* dance”). (Right) Our approach, NewMove, abstracts the motion pattern from the appearance in the input videos and enables generation of the depicted motion across a variety of novel contexts, including with a non-humanoid subject (robot, top row), multiple motions (lady, middle row), and multiple subjects (group of nurses, bottom row). To best view the results, please view our website*



### 基础扩散去噪目标

方法建立在预训练文本到视频扩散模型之上，其基础训练目标为加权去噪损失：

$$
\mathcal{L}_{\theta}(x, c) = \underset{\epsilon \sim \mathcal{N}(0,1)}{\mathbb{E}} [ w_t \| \epsilon_{\theta}(x, \epsilon, c, t) - \epsilon \|_2^2 ]
$$

其中 $x$ 为输入视频帧，$c$ 为文本条件，$\epsilon$ 为采样自标准正态分布的噪声，$\epsilon_{\theta}$ 为U-Net预测的噪声，$t$ 为扩散时间步，$w_t$ 为时间步权重。该损失函数最小化预测噪声与真实噪声之间的L2距离，使模型学会从噪声中逐步恢复视频帧。

### 运动定制微调目标

给定少量示例视频集 $D^{m}$，方法通过微调U-Net参数 $\theta$ 来学习新运动模式。初始微调目标为仅在运动样本上的重建损失：

$$
\operatorname*{min}_{\theta} \sum_{(x,c) \sim D^{m}} \mathcal{L}_{\theta}(x,c)
$$

该目标直接驱动模型在给定运动视频上重建原始帧，但单独使用会导致灾难性遗忘——模型丧失原有运动生成能力，且外观信息被过度复制到生成结果中。

### 正则化微调目标

为缓解遗忘问题，引入真实视频正则化集 $D^{r}$（如Jester数据集中的相关手势视频），将优化目标扩展为联合损失：

$$
\operatorname*{min}_{\theta} \sum_{(x,c) \sim D^{m} \cup D^{r}} \mathcal{L}_{\theta}(x,c)
$$

正则化集在微调过程中持续向模型注入原有运动知识，使模型在学习新运动的同时保留预训练阶段习得的运动先验。消融实验证实，真实正则化集（Jester）在运动准确率（70.6）和外观复制分数（8.7）上显著优于无正则化（43.9 / 1.2）或合成正则化方案（Table 2e）。

### 非均匀时间步采样分布

标准扩散训练采用均匀采样时间步，但早期去噪步骤主要决定运动结构，后期步骤则填充外观细节。为将运动学习与外观解耦，方法引入偏斜采样分布：

$$
f_{\alpha}(t) = \frac{1}{T}(1 - \alpha \cos(\frac{\pi t}{T}))
$$

其中 $T$ 为总时间步数，$\alpha \in [0,1]$ 控制偏斜程度。该分布将概率质量集中于早期时间步，使训练过程优先学习运动动态而非外观纹理。所有实验采用 $\alpha=0.5$。消融实验表明，该粗噪声采样策略相较均匀采样将运动准确率从66.9提升至70.6，同时将外观复制分数从15.4降至8.7（Table 2d）。

### 参数选择与模块架构

方法基于Modelscope T2V预训练模型（Wang et al.），其U-Net包含空间层和时间层两大组件。微调仅作用于以下参数子集（Fig. 2）：

- **时间层微调模块**：包含时间卷积和时间注意力层，负责建模视频帧间的运动动态。单独微调时间层不足以有效学习新运动模式（Table 2a），但它是运动表示的必要组成部分。
- **空间跨注意力K/V微调模块**：仅微调空间注意力层中交叉注意力的键（Key）和值（Value）投影矩阵，将运动标识符映射到视觉特征空间。该设计使运动模式与具体外观解耦，泛化至未见过的执行主体。消融实验显示，在时间层基础上增加空间K/V训练可将外观复制分数降低两倍以上，同时运动准确率提升约8%（Table 2a）。
- **全微调与LoRA对比**：全参数微调（Full）在运动准确率上远优于LoRA方法（70.6 vs 10.6），表明运动定制任务需要足够的参数容量来编码复杂时序动态（Table 2f）。

### 运动标识符机制

每个定制运动被赋予唯一的文本标识符（如“V* dance”），该标识符在微调过程中与运动模式建立映射关系。推理时，用户可通过在文本提示中插入该标识符来触发对应运动，实现对新主体、新场景的运动迁移。

### 补充图表

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/008_Table_2.jpg]]
*Table 2: Quantitative results of the ablation study. Each table examines the design choices of our method. We report the motion recognition accuracy (“Accuracy”) obtained with a pre-trained classifier for gesture recognition. The copying score (“Copy”) is the percentage of generated videos with a detection score above a set threshold*



## 实验与关键发现

### 实验设置

为系统评估运动定制能力，作者设计了两个互补的评估方案。第一个方案采用 **Jester 手势数据集**，选取其中多种手势类别作为定制目标运动，利用预训练的手势分类器自动计算运动识别准确率（Motion Accuracy）。第二个方案为**用户研究**，从互联网收集多样化运动视频（如 Dab、Air quotes 等），由人类评判者在生成质量和运动保真度上对方法进行偏好投票，并通过统计检验（p<0.01）控制显著性。

基线方法涵盖当时主流的文本到视频定制与运动迁移方案，包括 **Textual Inversion**（Gal et al., ICLR 2023）、**DreamBooth**（Ruiz et al., CVPR 2023）、**Tune-A-Video**（Wu et al., ICCV 2023）、**AnimateDiff v1**（Guo et al., arXiv 2023）以及 **MotionDirector**（Zhao et al., arXiv 2023）。

### 主实验结果

**定量对比（Table 3）**：在 Jester 手势识别任务上，NewMove 取得了 70.6% 的运动准确率，远超 DreamBooth（28.4%）和 Textual Inversion（0.3%），相对提升分别达 +42.2 和 +70.3 个百分点。这一巨大差距揭示了核心瓶颈：外观定制方法（DreamBooth、Textual Inversion）在扩展至运动定制时几乎完全失效，因为它们缺乏将运动动态从外观中解耦的机制。

**用户研究（Fig. 6）**：在面向互联网多样化运动的用户偏好测试中，NewMove 在统计显著水平（p<0.01）上优于 DreamBooth 和 Tune-A-Video。定性结果（Fig. 3）进一步印证了这一结论：基线方法生成的视频在时间上缺乏连贯性，无法准确再现目标手势（如“双指上滑”），而 NewMove 能够在新主体（如女性消防员）上忠实地复现该手势。

**泛化能力（Fig. 4、Fig. 5）**：NewMove 展现出超越训练分布的泛化能力。在 Fig. 4 中，基于互联网视频训练的 Dab 和 Air quotes 动作可迁移至未见主体和多人场景；基于 CO3D 数据集训练的 3D 相机旋转也可应用于新场景。Fig. 5 进一步展示了运动与外观解耦的效果：尽管训练视频仅包含单人单手“握手”动作，NewMove 仍能生成“边吃汉堡边做手势”、“缓慢精确做手势”以及“多名儿童同时做手势”等复杂场景。相比之下，文本驱动的运动迁移基线无法泛化或产生时间连贯的视频。

### 消融实验

消融实验（Table 2）系统验证了每个设计选择的因果贡献，所有实验均在 Jester 数据集上以运动准确率（Accuracy）和外观复制分数（Copy）为指标。

**微调参数选择（Table 2a）**：仅训练空间跨注意力层的键/值投影（K,V）是运动准确率与外观解耦之间的关键平衡点。与仅训练时间层（Temporal only）相比，加入空间 K/V 训练将运动准确率提升约 8 个百分点，同时将外观复制分数降低两倍以上。若完全不训练空间层（No spatial），外观复制虽低，但运动准确率大幅下降。这一结果表明，空间 K/V 投影是连接运动标识符与视觉特征的核心接口，其微调使模型能够将运动概念绑定到文本 token 而不复制训练视频的外观。

**时间步采样策略（Table 2d）**：粗噪声采样（Coarse-noise，即非均匀分布 $f_\alpha(t)$ 偏重早期去噪步）显著优于均匀采样。运动准确率从 66.9% 提升至 70.6%，同时复制分数从 15.4% 降至 8.7%。因果机制在于：扩散过程的早期去噪步骤决定视频的全局结构和运动轨迹，而后期步骤主要填充纹理细节。偏重早期步骤迫使模型专注于学习运动结构，抑制对外观细节的过拟合。

**正则化策略（Table 2e）**：真实视频正则化（Real，使用 Jester 相关视频）是防止灾难性遗忘的关键。无正则化（None）条件下，复制分数极低（1.2%），但运动准确率骤降至 43.9%，表明模型在缺乏正则化时迅速遗忘预训练的运动先验。合成正则化（Generated）效果介于两者之间，说明真实视频分布对于保持原有运动知识更为有效。真实正则化集使模型在微调新运动的同时，维持对相关运动的判别能力，实现了 70.6% 准确率与 8.7% 复制分数的最佳权衡。

**微调策略（Table 2f）**：全微调（Full）远优于 LoRA，运动准确率分别为 70.6% 和 10.6%。这一显著差距说明，低秩适配无法有效捕获运动定制所需的参数变化幅度，运动动态的学习需要更充分的参数更新自由度。

### 方法谱系与知识库定位

NewMove 在可控视频生成谱系中占据独特位置（Table 1）。与文本驱动的运动迁移方法（通过自然语言描述控制运动）不同，NewMove 从少量示例视频中学习运动模式，实现了**基于示例的运动定制**。与外观定制方法（如 DreamBooth 针对主体、Textual Inversion 针对概念）不同，NewMove 将定制对象从静态外观扩展到动态运动。与视频编辑方法（如 Tune-A-Video 保持原视频结构进行局部编辑）不同，NewMove 学习可泛化的运动模式并应用于全新场景。这种“运动-外观解耦 + 少量样本学习”的范式填补了文本到视频生成中运动定制能力的空白。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/002_Table_1.jpg]]
*Table 1: Comparison of our method across different techniques for controllable video / image generation. Here*

### 补充图表

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparison with baseline methods*

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/007_Figure_6.jpg]]
*Figure 6: User preference comparison*

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results of our method. We demonstrate two custom motions: Dab and Air quotes, trained using collected internet examples as well as a 3D camera rotation trained with examples from the CO3D dataset [31]. Our method can generalize to unseen subjects and multiple people performing the action*

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/006_Figure_5.jpg]]
*Figure 5: Text-driven motion transfer methods versus our method trained on few examples of a custom motion “Shaking Hand”. Our method seamlessly renders a custom motion in novel scenarios. Despite the training videos showing only a single actor performing one motion, our method generates the custom motion alongside another action (doing the gesture while eating a burger”) and varies timing (doing the gesture slowly and precisely”) or involves multiple people (“children”). In contrast, both baselines fail to generalize or produce temporally coherent videos*

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2312_04966/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparison with baseline methods. Examples of learning a customized motion Sliding Two Fingers Up from the Jester dataset with prompt “A female firefighter doing the V* sign”. Baseline methods (top three rows) fail to capture the motion and produce a temporally coherent video*



## 定位与知识库关联

### 问题定位与核心瓶颈

现有文本到视频（T2V）生成模型虽然在通用视频合成上取得了显著进展，但其运动生成能力受限于训练数据的分布：模型无法生成训练集中未覆盖的新运动模式（novel motion patterns）。与此同时，传统的运动转移（motion transfer）方法通常依赖于显式的结构表示（如骨架、光流），难以将运动与外观彻底解耦，因而无法将学习到的运动泛化到全新的场景、主体或非人形角色上。本文的核心瓶颈在于：如何在保留预训练T2V模型原有生成能力的前提下，从极少量样本中学习一个可泛化的、与外观解耦的运动模式。

### 方法谱系与基线对比

本文的方法在可控视频生成和定制化生成的交叉点上，与多类现有技术形成对比（Table 1 给出了系统性的能力比较）：

**基于文本驱动的运动转移方法**（如 VideoComposer、FateZero、Video-P2P）依赖文本描述来指定目标运动，但其运动空间受限于文本编码器的表达能力，无法精确捕捉细粒度或非标准化的动作（如特定手势、舞蹈动作）。本文通过直接从视频样本中学习运动模式，绕过了文本描述的不精确性。

**外观定制方法**（如 **Textual Inversion** (Gal et al., ICLR 2023)、**DreamBooth** (Ruiz et al., CVPR 2023)）在图像生成领域成功实现了主体外观的定制，但将其直接扩展到运动定制时面临根本性困难：这些方法倾向于记忆训练视频中的外观信息（“复制”问题），而非抽象出纯粹的运动模式。Table 3 的定量结果表明，DreamBooth 在 Jester 手势识别任务上的运动准确率仅为 28.4%，而 Textual Inversion 几乎完全失败（0.3%），证实了外观定制范式在运动域的不适用性。

**视频定制方法**（如 **Tune-A-Video** (Wu et al., ICCV 2023)）通过对单视频的微调实现内容编辑，但缺乏从多视频中抽象共同运动模式的能力，且容易过拟合到单一场景的外观。

**运动定制方法**（如 **AnimateDiff v1** (Guo et al., arXiv 2023)、**MotionDirector** (Zhao et al., arXiv 2023)）与本文目标最为接近。AnimateDiff 通过训练通用运动模块实现动画化，但其运动模式是预定义的而非从样本中定制。MotionDirector 支持从少量视频中学习运动，但本文通过系统性的参数选择、正则化策略和采样策略的组合，在运动准确率和外观泛化之间取得了更优的平衡。

### 关键设计选择与消融证据

本文的核心贡献在于三个相互耦合的设计选择，消融实验（Table 2）提供了清晰的因果证据链：

**参数子集选择**：仅微调时间层（temporal convolution and attention layers）和空间交叉注意力的键/值投影（key & value projections in spatial cross-attention layers），而非全参数微调或 LoRA。Table 2a 显示，仅训练空间 K/V 可将外观复制分数（Copy）从 16.3 降至 8.7（降低约两倍），同时运动准确率从 63.0 提升至 70.6。Table 2f 进一步表明，全微调（Full）的运动准确率为 70.6，而 LoRA 仅为 10.6——这一巨大差距说明低秩适配在运动定制任务中几乎完全失效，需要全量更新关键参数才能有效捕获运动动态。

**真实视频正则化**：使用真实视频集（Jester 相关手势）作为正则化，而非合成视频或无正则化。Table 2e 揭示了关键的权衡关系：无正则化时复制分数极低（1.2），但运动准确率灾难性下降至 43.9，表明模型发生了灾难性遗忘；真实正则化（Real）在准确率（70.6）和复制分数（8.7）之间取得了最优平衡，显著优于合成正则化（Syn：62.9 / 18.1）。

**非均匀时间步采样**：采用偏斜分布 $f_{\alpha}(t) = \frac{1}{T}(1 - \alpha \cos(\frac{\pi t}{T}))$（$\alpha=0.5$）偏重早期去噪步骤。Table 2d 显示，粗噪声采样（Coarse-noise）相比均匀采样（Uniform）将运动准确率从 66.9 提升至 70.6，同时将复制分数从 15.4 降至 8.7。这一结果支持了核心假设：早期去噪步骤主要决定运动的全局结构，而后期步骤更关注外观细节；通过偏重早期步骤，模型被迫学习运动结构而非外观纹理。

### 适用边界与局限

本文方法在以下条件下表现出色：（1）训练样本包含清晰、可区分的运动模式；（2）目标泛化场景与训练样本在运动语义上一致但外观差异显著；（3）预训练模型具备足够丰富的运动和外观先验。然而，方法的适用边界也受限于几个因素：运动模式需要能够在少量样本中被充分观测和定义；极端的外观变化（如从真人到高度风格化的卡通角色）可能超出空间 K/V 投影的泛化能力；多运动组合场景（如 Fig. 5 中的“边握手边吃汉堡”）虽然展示了初步能力，但运动间的交互和时序协调仍可能产生不自然的伪影。

### 开放问题

本文在结论中提出了一个根本性的开放问题：如何更好地利用预训练文本到视频模型中已有的运动和外观先验，来增强新的运动模式，并在全新设定下生成这些运动？这一问题指向几个潜在的研究方向：（1）更精细的参数解耦策略，以进一步分离运动与外观的表征；（2）无需微调的运动定制方法，以降低计算成本和过拟合风险；（3）多运动组合的显式建模，以处理复杂的时序交互场景。



## 原文 PDF

![[paperPDFs/arxiv_2023/Customizing_Motion_in_Text_to_Video_Diffusion_Models.pdf]]

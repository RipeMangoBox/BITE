---
title: GenMoStyle Generative Human Motion Stylization in Latent Space
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space.pdf
project_link: null
code_link: null
aliases:
- GGHMSLS
tags:
- ICLR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将运动风格迁移的核心流程从原始姿态空间迁移到预训练自编码器的紧凑潜在空间，并引入概率风格空间与AdaIN风格注入机制，从而实现高效、解耦且可多样化的风格化。
primary_logic: 在压缩且表达力强的潜在空间中，运动代码可被解耦为确定性的时序内容代码和全局概率风格代码；利用AdaIN注入风格，辅以同风格对齐损失，能够在单一框架内支持有监督、无监督、基于运动、基于标签以及基于先验的多种风格化模式。
claims:
- 我们利用预训练自编码器的潜在空间作为运动提取和注入的更表现力、更鲁棒的表示。
- 运动代码被分解为确定性的内容代码和服从先验分布的概率风格代码，生成器重组两者以重建运动代码。
- 提出的同风格对齐技术鼓励同一序列中不同子片段的风格空间对齐，显著提升性能。
- 本文方法在保持内容的同时，性能是最先进的，且速度比Jang et al., 2022快14倍。
---

# GenMoStyle Generative Human Motion Stylization in Latent Space

> [!tip] 核心洞察
> 在压缩且表达力强的潜在空间中，运动代码可被解耦为确定性的时序内容代码和全局概率风格代码；利用AdaIN注入风格，辅以同风格对齐损失，能够在单一框架内支持有监督、无监督、基于运动、基于标签以及基于先验的多种风格化模式。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenMoStyle：潜在空间中的生成式人体运动风格化 |
| 英文题名 | GenMoStyle Generative Human Motion Stylization in Latent Space |
| 会议/期刊 | ICLR 2024 |
| Links |  [paper](https://arxiv.org/abs/2401.13505)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GenMoStyle |
| Dataset | CMU Mocap 测试集 |

> [!tip] 效果简介
> - (Aberman et al., 2020) 测试集 上，Style Accuracy (↑) 0.945±007 (Ours A) vs 0.891±007 (Park et al., 2021) (+0.054)。
> - CMU Mocap 测试集 上，Style FID (↓) 0.028±003 (Ours V) vs 0.136±011 (Park et al., 2021) (-0.108)。
> - (Xia et al., 2015) 测试集 上，Style Accuracy (↑) 0.934±006 (Ours V) vs 0.527±006 (Park et al., 2021) (+0.407)。

## 概要

人体运动风格化旨在将参考风格赋予输入运动，同时保留其原始动作内容。现有方法大多直接在原始姿态空间操作，面临表示冗余、对噪声敏感、泛化能力有限等瓶颈；同时，多数工作仅支持确定性的风格迁移，缺乏灵活的概率风格建模，难以生成多样化的风格化结果。

针对上述问题，本文提出 **GenMoStyle**，一种在潜在空间中进行生成式运动风格化的统一框架。其核心思路是：将风格迁移的关键流程从原始姿态空间迁移至预训练自编码器的紧凑潜在空间，在该空间中将运动代码解耦为确定性的时序内容代码和服从先验分布的概率风格代码，并通过 AdaIN 机制注入风格信息，辅以同风格对齐损失，在单一框架内支持有监督、无监督、基于运动、基于标签以及基于先验的多种风格化模式。

实验表明，GenMoStyle 在多个基准上取得了最优性能，同时推理速度比此前最先进的无监督方法（Jang et al., 2022）快 14 倍。消融研究验证了潜在空间表示、概率风格空间、同风格对齐以及全局运动预测等关键设计的有效性。此外，该方法可灵活嵌入下游任务（如 text2motion），为其提供风格化扩展能力。

### 方法谱系与知识库定位

GenMoStyle 处于**运动风格迁移**与**生成式潜在空间建模**的交叉点，其方法谱系可追溯至以下关键工作：

- **Aberman et al., 2020**：首次将 AdaIN 引入运动风格迁移，采用两分支管道结合预训练自编码器和对抗训练，实现了有监督的风格迁移。GenMoStyle 继承了其 AdaIN 注入机制和自编码器架构，但将操作空间从姿态空间迁移至潜在空间，并引入了概率风格建模。

- **Park et al., 2021**：基于 GAN 为每个风格标签构建独立的风格空间，支持基于运动和基于标签的确定性及多样性风格化。GenMoStyle 借鉴了其风格空间建模思路，但采用统一的概率风格空间替代每标签独立空间，显著提升了框架的灵活性和泛化能力。

- **Jang et al., 2022**：基于图神经网络从身体部件提取风格特征，实现了无监督的运动风格迁移。GenMoStyle 在无监督模式下与之对标，但在推理速度和风格化质量上均取得显著优势。

相较于上述工作，GenMoStyle 的关键贡献在于**将风格迁移的操作空间从姿态空间提升至潜在空间**，并在此基础上构建了**概率风格空间**与**同风格对齐**机制，从而在统一的生成式框架下实现了多模式、多样化的运动风格化。



### 问题背景

人体运动风格化旨在将给定运动序列的风格属性（如“老人”、“快乐”、“沉重”等）迁移到另一段内容运动上，同时保留后者的动作语义。该技术在下游应用中具有广泛前景，包括动画制作、虚拟角色控制以及文本到运动生成的后处理增强。

早期方法直接在原始姿态空间（pose space）中操作风格迁移，典型范式包括基于对抗生成网络的两分支管道或基于图神经网络的身体部件风格提取。然而，姿态空间本身具有高维冗余特性，关节旋转或位置表示对噪声敏感，导致风格化结果在泛化性和多样性上均受到制约。此外，多数现有工作仅支持单一训练范式——要么是有监督的标签驱动风格化，要么是无监督的运动驱动风格化——缺乏统一的概率建模框架来支撑多样化的推理需求。

### 现有方法缺口

当前方法存在三个关键瓶颈：

1. **表示空间冗余**：直接在姿态空间进行风格提取与注入，使得模型难以学习紧凑且鲁棒的运动表示，限制了跨数据集泛化能力。
2. **风格建模僵化**：主流方法采用确定性风格代码，无法刻画风格分布的内在多样性，也难以支持基于先验采样的无条件风格化。
3. **训练范式割裂**：有监督方法（如 **Aberman et al., 2020**）依赖风格标签但缺乏多样性生成能力；无监督方法（如 **Jang et al., 2022**）虽可从参考运动中提取风格，但无法进行基于标签的定向风格化或随机风格探索。**Park et al., 2021** 虽引入每标签风格空间建模，但仍限于姿态空间操作且训练模式单一。

### 本文动机

针对上述缺口，本文提出将运动风格迁移的核心流程从原始姿态空间迁移到预训练自编码器的紧凑潜在空间（latent space）中。潜在空间经重建任务预训练后，具备更强的表达力和鲁棒性，能够为风格解耦提供更优的表示基础。在此基础上，引入概率风格空间与自适应实例归一化（AdaIN）注入机制，将运动代码分解为确定性时序内容代码和服从高斯先验的概率风格代码，从而在单一框架内统一支持有监督、无监督、基于运动、基于标签以及基于先验采样的多种风格化模式。



## 核心方法与创新机理

GenMoStyle 的核心创新在于将运动风格迁移的完整流程从原始姿态空间迁移至预训练自编码器的紧凑潜在空间，并在此空间中构建概率风格建模与解耦机制，从而在单一框架内统一支持有监督、无监督、基于运动、基于标签以及基于先验的多种风格化模式。以下从三个关键“changed slots”展开分析。

### 1. 表示空间迁移：从姿态空间到潜在空间

现有方法（如 **Aberman et al., 2020**、**Park et al., 2021**、**Jang et al., 2022**）直接在原始姿态空间操作，面临表示冗余、对噪声敏感等问题，限制了泛化能力和风格化多样性。GenMoStyle 将核心操作迁移至预训练自编码器的潜在空间，利用其更强的表达力和鲁棒性进行运动提取与注入。

具体而言，运动自编码器 $(\mathcal{E}, \mathcal{D})$ 将姿态序列 $\mathbf{P}$ 映射为潜在运动代码 $\mathbf{z} = \mathcal{E}(\mathbf{P}) \in \mathbb{R}^{T_z \times D_z}$，并通过 $\hat{\mathbf{P}} = \mathcal{D}(\mathbf{z})$ 重建。潜在空间通过 KL 散度正则化 $\mathcal{L}_{kld}^l = \lambda_{kld}^l D_{\mathrm{KL}}(\mathbf{z} \| \mathcal{N}(0, I))$ 和 L1 平滑正则化 $\mathcal{L}_{reg}^l = \lambda_{l1} \|\mathbf{z}\|_1 + \lambda_{sms} \|\mathbf{z}_{1:T_z} - \mathbf{z}_{0:T_z-1}\|_1$ 进行约束，获得平滑且低方差的表示空间。消融实验证实，移除潜在风格化（w/o latent）会导致风格准确率从 0.945 降至 0.932（Aberman 数据集），验证了潜在空间迁移的有效性。

### 2. 风格建模方式升级：从确定性到概率风格空间

现有方法多采用确定性风格代码，缺乏对风格分布的显式建模，限制了风格化的多样性和可控性。GenMoStyle 引入概率风格空间：风格编码器 $E_s$ 以运动代码 $\mathbf{z}$ 和风格标签 $sl$ 为输入，输出高斯分布 $\mathcal{N}_s(\mu_s, \sigma_s)$，从中采样得到风格代码。

在此基础上，生成器 $G$ 通过 AdaIN 层将风格信息注入内容代码——即对每层输出进行基于风格代码和标签的仿射变换，修改其均值与方差。这种机制实现了内容与风格的解耦操作。消融实验表明，概率风格空间相比确定性风格空间，在 Aberman 数据集上将风格准确率提升约 0.032，验证了概率建模的增益。

### 3. 训练模式统一：从单一模式到多模式兼容

现有方法通常仅支持有监督或无监督中的一种训练/推理模式。GenMoStyle 通过灵活的内容-风格解耦架构，统一支持多种模式（见 Table 1）：在有监督设置下支持基于运动和基于标签的风格化；在无监督设置下支持基于运动和基于先验的风格化。推理时，风格线索可来自运动、风格标签或无条件的先验空间，极大扩展了应用灵活性。同时，该方法在保持内容准确率的前提下，推理速度比最先进的前人工作（**Jang et al., 2022**）快 14 倍。

此外，同风格对齐损失 $\mathcal{L}_{hsa} = D_{\mathrm{KL}}(\mathcal{N}_s^1(\mu_s^1, \sigma_s^1) \| \mathcal{N}_s^2(\mu_s^2, \sigma_s^2))$ 鼓励同一序列中不同子片段的风格空间对齐，在有监督设置下将内容准确率提升 13%，无监督下提升 6%，成为解耦质量的关键保障。



GenMoStyle 的整体设计遵循“先压缩、再解耦、后重组”的两阶段范式，将运动风格迁移的核心流程从原始姿态空间迁移至预训练自编码器的紧凑潜在空间，从而获得更富表达力且对噪声更鲁棒的表示。

### 两阶段流水线

**第一阶段：运动潜在空间构建。** 给定一段姿态序列 $P$，预训练的运动编码器 $\mathcal{E}$ 将其映射为潜在运动代码 $z = \mathcal{E}(P) \in \mathbb{R}^{T_z \times D_z}$；解码器 $\mathcal{D}$ 则负责从 $z$ 重建姿态序列 $\hat{P} = \mathcal{D}(z)$。该自编码器通过 KL 散度正则化 $\mathcal{L}_{kld}^l$ 和 L1 平滑正则化 $\mathcal{L}_{reg}^l$ 约束潜在空间，使其接近标准正态分布并保持低方差、时序平滑，为后续风格化提供高质量的表示基础。

**第二阶段：潜在风格化。** 在冻结或联合训练的自编码器之上，运动代码 $z$ 被进一步分解为两个编码分量：内容编码器 $\mathcal{E}_c$ 提取确定性的时序内容代码 $z_c$（通过实例归一化剥离全局风格信息），风格编码器 $\mathcal{E}_s$ 则从 $z$ 和可选风格标签 $sl$ 中生成概率风格空间——一个参数化高斯分布 $\mathcal{N}_s(\mu_s, \sigma_s)$，并从中采样风格代码 $z_s$。生成器 $G$ 以内容代码为骨架，通过 AdaIN 层逐层注入风格信息（以风格代码和标签的仿射变换修改每层输出的均值与方差），最终输出风格化后的运动代码 $\hat{z}$，再经解码器 $\mathcal{D}$ 还原为姿态序列。

### 训练与推理的统一设计

该框架在训练阶段同时优化自编码重建、风格-内容解耦、循环一致性及同风格对齐等目标，使单一模型能够支持多种工作模式。推理时（Figure 3），系统可灵活切换：
- **有监督模式**：基于运动示例的风格迁移（以风格运动提取 $z_s$ 注入内容运动）或基于标签的风格化（以目标风格标签引导 $z_s$ 采样）；
- **无监督模式**：基于运动示例的风格迁移（无需风格标签，直接从风格运动提取 $z_s$）或基于先验的风格化（从标准高斯先验随机采样 $z_s$，无需任何风格指示）。

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/004_Figure_3.jpg]]
*Figure 3: During inference, our approach can stylize input content motions with the style cues from*

此外，全局运动预测器（GMP）从局部关节运动预测根节点速度等全局量，实现风格化后的自适应步态，保证运动在全局轨迹层面的合理性。

Table 1 对比了 GenMoStyle 与代表性基线方法在训练和推理灵活性上的差异：**Aberman et al., 2020** 仅支持有监督运动风格化，**Park et al., 2021** 扩展至基于标签的多样化生成但缺乏无监督能力，**Jang et al., 2022** 专注于无监督运动风格化；而 GenMoStyle 统一覆盖了上述所有模式，并额外支持基于先验的无条件风格化。

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/002_Table_1.jpg]]
*Table 1: Our generative framework owns flexible design for training and inference*

### 补充图表

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/003_Figure_2.jpg]]
*Figure 2: Approach overview. (a) A pre-trained autoencoder E and D (Sec. 3.1) builds the mappings between motion and latent spaces. Motion (latent) code z is further encoded into two parts: content code*



GenMoStyle 的核心架构由五个模块构成，围绕“潜在空间编码—内容/风格解耦—条件生成”这一主线展开。

**运动自编码器 (E, D)** 将原始姿态序列映射到紧凑的潜在空间，并负责从潜在代码重建回姿态空间。给定姿态序列 $P$，编码器输出潜在运动代码：

$$z = \mathcal{E}(P) \in \mathbb{R}^{T_z \times D_z}$$

解码器则从潜在代码重建姿态序列：

$$\hat{P} = \mathcal{D}(z) = \mathcal{D}(\mathcal{E}(P))$$

该潜在空间的训练引入两项正则化：KL 散度正则化鼓励潜在代码接近标准正态分布 $\mathcal{L}_{kld}^l = \lambda_{kld}^l D_{\mathrm{KL}}(z || \mathcal{N}(0, I))$，以及 L1 与平滑正则化抑制潜在代码的量级和时序波动 $\mathcal{L}_{reg}^l = \lambda_{l1} \|z\|_1 + \lambda_{sms} \|z_{1:T_z} - z_{0:T_z-1}\|_1$。消融实验表明 $\lambda_{l1}=0.001, \lambda_{sms}=0.001$ 可实现最佳重建与风格化性能（Table 12）。

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/020_Table_12.jpg]]
*Table 12: Effect of hyper-parameters of autoencoder on the (Aberman et al., 2020) and (Xia et al., 2015) test sets. ± indicates 95% confidence interval. Bold face indicates the best result, while underscore refers to the second best. Results of motion-based stylization in supervised setting are presented. MPJPE is measured in millimeter*

**内容编码器 (E_c)** 从运动代码 $z$ 提取时序内容代码 $z_c$，并通过实例归一化移除全局风格信息，确保内容代码仅保留局部语义。**风格编码器 (E_s)** 则接收运动代码 $z$ 和风格标签 $sl$，输出一个向量高斯分布 $\mathcal{N}_s(\mu_s, \sigma_s)$ 作为概率风格空间，从中采样得到风格代码 $z_s$。这一概率化设计相比确定性风格空间，在 Aberman 数据集上将 Style Accuracy 提升约 0.032（Table 7）。

**生成器 (G)** 是风格注入的核心执行单元。它以内容代码 $z_c$ 为主干输入，通过 AdaIN 层将风格信息注入每一层特征——即利用风格代码和标签的仿射变换，逐层修改特征的均值与方差，生成风格化后的运动代码 $\hat{z}$。

**全局运动预测器 (GMP)** 从局部关节运动预测根节点速度等全局运动分量，使风格化后的运动具备自适应步态。消融实验显示，GMP 在 Xia et al., 2015 数据集上将风格化准确率提升约 9%（Table 9）。

训练阶段的核心损失函数包括：

- **自编码重建损失**，在潜在空间和姿态空间同时施加 L1 约束：
  $$\mathcal{L}_{rec} = \sum_{i \in \{1,2\}} \| \hat{\mathbf{z}}^i - \mathbf{z}^i \|_1 + \| \hat{\mathbf{P}}^i - \mathbf{P}^i \|_1$$

- **同风格对齐损失**，最小化同一序列两段子片段的风格分布 KL 散度，强制同序列风格空间对齐：
  $$\mathcal{L}_{hsa} = D_{\mathrm{KL}}( \mathcal{N}_s^1(\mu_s^1, \sigma_s^1) \| \mathcal{N}_s^2(\mu_s^2, \sigma_s^2) )$$
  该损失在有监督设置下将内容准确率提升 13%，无监督下提升 6%。

- **循环一致性损失**，交换内容与风格后重建回原始运动，促进内容-风格解耦：
  $$\mathcal{L}_{cyc} = \sum_{i \in \{2,3\}} \| \tilde{\mathbf{z}}^i - \mathbf{z}^i \|_1 + \| \tilde{\mathbf{P}}^i - \mathbf{P}^i \|_1$$

- **风格空间 KL 正则化**，将所有风格空间拉向标准正态分布，保证空间平滑且可采样：
  $$\mathcal{L}_{kl} = \sum_{i \in \{1,2,3,t\}} D_{\mathrm{KL}}( \mathcal{N}_s^i(\mu_s^i, \sigma_s^i) \| \mathcal{N}(\mathbf{0}, \mathbf{I}) )$$

值得注意的是，端到端训练（将自编码器与风格化模型联合优化）会导致风格化准确率暴跌至约 15%（Table 8），因此分阶段训练是当前方案的必要约束。

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/016_Table_8.jpg]]
*Table 8: Separate / End-to-end Training. Our two-stage framework can alternatively be trained in an endto-end fashion. We also conduct ablation analysis to evaluate the impact of such choice of training strategy. The results are presented in Table 8. In practice, we observed that end-to-end training posed significant challenges. The model struggled to simultaneously learn meaningful latent motion representation and effectively transfer style traits between stages. Experimental results align with this observation, revealing that stylization accuracy is merely around 15% on both datasets in the end-to-end training scenario, in contrast to the accuracy of 92% achieved by stage-by-stage training*

### 补充图表

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/021_Figure_9.jpg]]
*Figure 9: Detailed architecture of our VAE based motion latent model. The AE based latent model keeps only one convolution branch before the latent space. All convolutions, except the last layer of encoder, decoder and generator, use kernel size of 3*

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/022_Figure_10.jpg]]
*Figure 10: Detailed architecture of our motion latent stylization model in supervised setting. In unsupervised setting, the style label input is dropped. All convolutions, except the last layer of encoders and generator, use kernel size of 3*



## 实验与关键发现

### 主实验结果

GenMoStyle 在三个基准数据集上进行了系统评估，涵盖有监督和无监督两种设置。评估指标包括风格准确率（Style Accuracy）、风格FID（Style FID）、内容准确率（Content Accuracy）、测地距离（Geo Dis）和多样性（Diversity）。所有实验在测试集上重复30次，报告95%置信区间。

**在 (Aberman et al., 2020) 测试集上**，Ours (A) 变体取得风格准确率 0.945±007，相比最优基线 **Park et al., 2021** 的 0.891±007 提升 5.4 个百分点。在风格FID指标上，Ours (A) 达到 0.020±002，显著优于 Park et al., 2021 的 0.046±003。这一结果表明，潜在空间中的风格化操作在保持风格一致性的同时，能生成与真实风格分布更接近的运动。

**在 CMU Mocap 测试集上**，该数据集对潜在风格化模型完全不可见，构成零样本泛化测试。Ours (V) 变体取得风格FID 0.028±003，远低于 Park et al., 2021 的 0.136±011，降幅达 0.108。同时测地距离为 0.629±0.02，表明风格化后的运动在几何结构上与目标风格高度一致。这一零样本泛化能力归因于潜在空间的紧凑性和概率风格空间的正则化设计。

**在 (Xia et al., 2015) 测试集上**，该数据集同样未被潜在风格化模型所见。Ours (V) 取得风格准确率 0.934±006，而 Park et al., 2021 仅为 0.527±006，提升幅度高达 40.7 个百分点。内容准确率方面，Ours (A) 达到 0.674±011，相比 Park et al., 2021 的 0.441±009 提升 23.3 个百分点。这一结果表明，GenMoStyle 在保持原始动作语义的同时，实现了更精确的风格迁移。

**人类评估**（Table 4）进一步验证了定量结果。在风格一致性和内容保持两个维度上，GenMoStyle 均获得显著优于基线方法的人类偏好评分。

**推理效率**方面，GenMoStyle 的推理速度比 **Jang et al., 2022** 快 14 倍（Table 5）。这一效率优势源于风格化过程完全在低维潜在空间中进行，避免了在原始姿态空间上的高维操作。

### 消融实验

**潜在空间的作用**（Table 6）：移除潜在空间（w/o latent），直接在姿态空间进行风格化，导致风格准确率从 0.945 降至 0.932。潜在空间的引入不仅提升了性能，还带来了显著的效率增益。

**概率风格空间 vs 确定性风格空间**（Table 7）：在监督设置下，概率风格空间将风格准确率提升约 0.032。概率建模不仅增强了风格表示的鲁棒性，还使得推理阶段能够从先验分布采样，支持多样化的风格生成。

**分阶段训练 vs 端到端训练**（Table 8）：端到端训练导致风格准确率暴跌至约 15%。这表明，先预训练运动自编码器以获得稳定的潜在空间，再训练风格化模块的分阶段策略，对于模型收敛和性能至关重要。端到端训练可能导致潜在空间和风格化目标之间的优化冲突。

**同风格对齐损失（homo-style alignment）**：在有监督设置下，该损失将内容准确率提升 13%；在无监督设置下提升 6%。通过强制同一序列不同子片段的风格分布对齐，模型学习到了更一致且可泛化的风格表示。

**全局运动预测器（GMP）**（Table 9）：在 (Xia et al., 2015) 数据集上，GMP 将风格化准确率提升约 9%。该模块从局部关节运动预测根节点速度等全局运动，使得风格化后的运动能够自适应地调整步态，避免出现脚部滑动等伪影。

**自编码器超参数**（Table 12）：λ_l1=0.001 和 λ_sms=0.001 的组合实现了最佳的重建质量与风格化性能平衡。过大的正则化会过度压缩潜在空间，损害运动重建精度；过小的正则化则导致潜在空间不够平滑，影响风格化质量。

### 失败模式与局限性

**罕见动作的泛化不足**（Figure 13）：当输入动作与训练数据分布显著偏离时，模型可能无法完整保留所有身体部位的运动。例如，对 breaking dance 和 push-up 动作应用 happy 风格时，下肢运动可能丢失，尽管上肢的风格化效果仍可接受。这是因为模型在 (Aberman et al., 2020) 数据集上训练，该数据集仅包含站立动作。

**风格-内容属性冲突**：某些风格属性与运动内容特征天然耦合。例如，hurried 风格与运动速度相关，而风格化过程旨在保留内容的速度特征，导致风格迁移可能不完全符合预期。这种固有不匹配是当前框架尚未解决的根本性问题。

**VAE 与 AE 潜在模型的行为差异**：两种潜在模型在多样性、风格/内容准确率上表现不同，但其深层原因尚不清楚。VAE 的 KL 正则化可能引入额外的平滑性，影响风格化精度；AE 则可能保留更多运动细节但潜在空间结构性较弱。

### 补充图表

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/013_Table_6.jpg]]
*Table 6: Ablation study on different components of our model design. ± indicates 95% confidence interval. Bold face indicates the best result, while underscore refers to the second best. (S) and (U) denote supervised and unsupervised setting. Motion-based stylization is presented for both settings. Prob-style refers to probabilistic style space*

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/014_Table_7.jpg]]
*Table 7: Ablation study on the choice of probabilistic (P) or deterministic (D) space for content and style, in supervised setting. ± indicates 95% confidence interval. Bold face indicates the best result, while underscore refers to the second best. Motion-based stylization is presented*

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/015_Table_8.jpg]]
*Table 8: Ablation study on separately or end-to-end training the latent model and stylization model, in supervised setting. ± indicates 95% confidence interval. Bold face indicates the best result, while underscore refers to the second best. (S) and (U) denote supervised and unsupervised setting. Motion-based stylization is presented*

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/007_Table_4.jpg]]
*Table 4: Human evaluation results*

![[assets/figures/papers/paper_list_l4_GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space_motion20v2/figures/025_Figure_13.jpg]]
*Figure 13: Failure cases. Top row shows content motion; bottom row shows our corresponding results. Stylization results of breaking dance motion (left) and push-up motion (right) using happy style label are displayed*



## 定位与知识库关联

### 1. 技术脉络与关键突破

GenMoStyle 的核心贡献在于将运动风格迁移的“战场”从原始姿态空间迁移到了预训练自编码器的紧凑潜在空间，并引入了概率风格建模与 AdaIN 注入机制。这一设计选择直接回应了该领域长期存在的两个瓶颈：**表示冗余与噪声敏感**，以及**风格建模的确定性局限**。

在 GenMoStyle 之前，运动风格迁移的技术谱系大致可分为三条路径：

- **基于 AdaIN 的有监督两分支管道**：以 **Aberman et al., 2020** 为代表，首次将风格迁移中经典的 AdaIN 范式引入运动领域，利用预训练自编码器和对抗训练实现了有监督的风格迁移。然而，该方法直接在姿态空间操作，对噪声敏感，且仅支持有监督的单一样式迁移。

- **基于 GAN 的每标签风格空间建模**：**Park et al., 2021** 为每个风格标签学习独立的风格空间，支持基于运动和基于标签的确定性/多样性风格化。但其风格空间是确定性的，且训练和推理模式相对固定，缺乏对无监督和先验采样的统一支持。

- **基于图神经网络的无监督风格迁移**：**Jang et al., 2022** 从身体部件级别提取风格特征，实现了无监督的运动风格迁移，但计算开销较大，且同样受限于姿态空间的冗余表示。

GenMoStyle 在上述工作的基础上实现了三个关键“槽位”的变更：

| 槽位 | 基线方案 | GenMoStyle 方案 | 证据锚点 |
|------|---------|----------------|---------|
| **表示空间** | 原始姿态空间 | 预训练自编码器的潜在空间 | “we leverage the latent space of pretrained autoencoders as a more expressive and robust representation” |
| **风格建模** | 确定性风格代码 | 概率风格空间（高斯分布） | “our style encoder E_s … produces a vector Gaussian distribution N_s(μ_s, σ_s) to formulate the style space” |
| **训练模式** | 仅支持有监督或无监督之一 | 统一支持有监督、无监督、基于运动、基于标签、基于先验 | Table 1 |

这些变更并非孤立的设计选择，而是形成了一个因果链条：**潜在空间的压缩性与表达力** 使得运动代码可以被解耦为确定性的时序内容代码和全局概率风格代码；**概率风格空间** 又天然支持从先验分布采样，从而解锁了无监督和基于先验的多样化风格化模式；**AdaIN 注入机制** 则在生成器中以仿射变换的方式将风格信息注入内容代码，实现了高效且解耦的风格迁移。

### 2. 适用边界与局限

尽管 GenMoStyle 在多个基准上取得了最优性能，其适用边界仍受以下因素制约：

**数据分布依赖**：模型在 **Aberman et al., 2020** 数据集上训练，该数据集仅包含站立动作。当输入动作与训练分布显著偏离时（如 breaking dance、push-up），模型可能无法保留下肢运动，尽管上肢风格化仍可接受（参见 Figure 13）。这提示该方法在罕见动作或极端姿态上的泛化能力有限。

**风格-内容固有冲突**：某些风格属性与运动内容特征存在天然关联。例如，“hurried”风格与运动速度强相关，而风格化过程旨在保留内容速度，导致风格迁移可能不完全符合预期。这一矛盾并非 GenMoStyle 独有，而是该领域的一个开放问题。

**潜在模型选择的影响**：VAE 和 AE 两种潜在模型在多样性与风格/内容准确率上表现不同，但其深层原因尚不清楚。消融实验表明，端到端训练会导致风格化准确率暴跌至约 15%（Table 8），说明分阶段训练是当前方案的必要约束。

### 3. 开放问题

1. **风格-内容解耦的深层矛盾**：如何解决风格属性（如“fast”）与内容特征（如速度）之间的固有不匹配，使得风格迁移能够真正改变动作的全局属性而不破坏内容语义？这可能需要重新思考“内容”的定义边界。

2. **罕见动作的泛化**：是否可以通过增加罕见动作数据或采用数据增强策略（如姿态扰动、运动混合）来改善模型在 breaking dance 等动作上的性能？这涉及数据工程与模型鲁棒性的权衡。

3. **端到端训练的可行性**：在保持风格化质量的前提下，能否将潜在空间学习和风格化模型进行端到端训练，从而简化流程并可能释放更强的表示学习能力？当前的分阶段训练是性能保障，但也是流程复杂度的来源。

4. **正则化策略的统一**：VAE 的 KL 正则化与 AE 的 L1/平滑正则化为何导致风格化行为的差异？是否可以在未来设计统一的潜在空间正则化策略，兼顾重建质量与风格化多样性？

**注意**：以上开放问题中的部分推测（如数据增强的具体策略）基于领域常识，原文未提供直接证据，需在实际研究中验证。



## 原文 PDF

![[paperPDFs/ICLR_2024/GenMoStyle_Generative_Human_Motion_Stylization_in_Latent_Space.pdf]]

---
title: "PersonaBooth: Personalized Text-to-Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/PersonalBooth_Personalized_Text_to_Motion_Generation.pdf
code_link: null
project_link: http://boeun-kim.github.io/page-PersonaBooth
aliases:
- PersonaBooth
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过可学习的Persona Token实现文本与视觉双路径自适应，并引入Persona Cohesion Loss（监督对比学习）强制相同个性、不同内容的运动特征在特征空间中紧密聚集。
primary_logic: 将个性建模为可插拔的文本标记和视觉特征，通过对比学习解耦个性与动作内容，使得扩散模型在微调时既能注入新个性又不丢失预训练的先验，同时利用上下文感知融合处理多输入，从而生成既忠实于描述又体现独特个性的运动。
claims:
- Introduce learnable persona tokens to capture persona features from new data and propose an adaptation scheme for both text and visuals.
- Introduce a novel contrastive learning-based loss called persona cohesion loss to facilitate cohesion across motion features with different content but the same persona.
- Adding text adaptation (P*) reduces FID from 7.45 to 5.06 and adding L_pc further reduces FID to 3.18 while boosting R-Precision.
- Context-Aware Fusion (CAF) outperforms simple averaging, reducing FID from 3.52 to 2.95 and increasing Diversity to 8.12.
---

# PersonaBooth: Personalized Text-to-Motion Generation

> [!tip] 核心洞察
> 将个性建模为可插拔的文本标记和视觉特征，通过对比学习解耦个性与动作内容，使得扩散模型在微调时既能注入新个性又不丢失预训练的先验，同时利用上下文感知融合处理多输入，从而生成既忠实于描述又体现独特个性的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | PersonaBooth：个性化文本到运动生成 |
| 英文题名 | PersonaBooth: Personalized Text-to-Motion Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](http://boeun-kim.github.io/page-PersonaBooth) · [paper](https://arxiv.org/abs/2510.06504) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PersonaBooth |
| Dataset | PerMo, 100Style |

> [!tip] 效果简介
> - PerMo (Single Input) 上，FID 3.18 vs MoMo (数值未提供) / MCM-LDM (显著优于所有现有方法)。
> - PerMo (Multiple Input + CAF) 上，FID 2.95 vs Simple averaging (3.52) (-0.57)。
> - 100Style 上，R Precision Top1 0.20 vs MoMo 0.07 (+0.13)。

## 概要

**PersonaBooth** 针对现有文本到运动生成（Text-to-Motion, T2M）模型仅关注视觉条件而忽略文本适应，导致微调后个性遗忘和生成质量低的问题，提出了一种多模态个性化微调框架。其**核心瓶颈**在于：通用预训练数据（如 HumanML3D）与个性化数据（PerMo）之间存在显著分布差异，且从不同动作内容中提取一致的个性特征极为困难。

**核心思路**是将个性建模为可插拔的文本标记（Persona Token）和视觉特征，通过**文本与视觉双路径自适应**注入扩散模型，并引入**监督对比学习损失**（Persona Cohesion Loss）解耦个性与动作内容，使相同个性、不同内容的运动特征在特征空间中紧密聚集。这一机制使得扩散模型在微调时既能注入新个性又不丢失预训练先验。

**主要结果**方面：在 PerMo 数据集上，PersonaBooth 的 FID 达到 3.18，显著优于现有方法；引入文本自适应使 FID 从 7.45 降至 5.06，加入 Persona Cohesion Loss 后进一步降至 3.18，R-Precision Top1 从 0.05 提升至 0.15。在多输入设定下，上下文感知融合（CAF）将 FID 从简单平均的 3.52 降至 2.95。在 100Style 数据集上，PersonaBooth 同样取得最优 FID（3.27）和 R-Precision Top1（0.20），验证了方法的泛化能力。

**方法定位**：PersonaBooth 属于基于扩散模型的个性化运动生成方法，与零样本运动风格迁移方法 **MoMo** 和微调版本 **MCM-LDM** 形成对比。其关键创新在于首次将文本路径纳入个性化适配，并通过对比学习实现个性与内容的显式解耦。

### 任务定义：运动个性化生成

文本到运动生成（Text-to-Motion, T2M）旨在根据自然语言描述合成逼真的三维人体运动序列。传统T2M方法关注运动内容的准确表达——即“做什么”，却忽略了一个同等重要的维度：运动个性（Persona）——即“如何做”。同一动作内容（如“走路”）在不同个体身上呈现出截然不同的风格特征：步幅、节奏、姿态倾向、关节协调模式等。**运动个性化生成（Motion Personalization）** 正是为了解决这一问题而提出的新任务：给定少量体现特定个体运动个性的原子运动片段（Atomic Motions），模型需要生成既忠实于文本描述、又体现该个体独特运动风格的新运动序列。

这一任务与现有运动风格迁移（Motion Style Transfer, MST）存在本质区别。如Table 1所示，MST通常要求提供完整的源运动序列作为风格参考，且主要依赖视觉条件进行风格注入；而运动个性化生成仅需少量原子运动片段，且要求模型同时适应视觉和文本两个模态。这种多模态适应需求源于一个关键观察：**个性不仅体现在运动的空间-时间模式中，也隐含在与运动相关的语义描述中**——例如，“活泼地走路”与“慵懒地走路”在文本层面就已编码了不同的个性语义。

### 现有方法的核心瓶颈

当前主流的文本到运动扩散模型（如MDM、MLD等）在大规模通用运动数据集（如HumanML3D）上预训练，具备强大的运动先验和文本跟随能力。然而，将这些模型直接适配到个性化运动生成场景时，面临两个紧密耦合的瓶颈：

**瓶颈一：预训练数据与个性化数据之间的显著分布差异。** 通用运动数据集包含大量不同个体的运动，模型学习到的是“平均化”的运动模式。当面对特定个体的个性化数据（如PerMo数据集中某位演员的“幼稚”风格走路）时，模型倾向于生成符合预训练分布的“平均”运动，导致个性特征被稀释甚至遗忘。这种分布偏移在数据量极少的个性化场景中尤为严重——每个个性类别可能仅有几十个样本。

**瓶颈二：从不同动作内容中提取一致的个性特征极为困难。** 同一个体的个性贯穿于其所有动作之中——无论是走路、跑步还是跳跃，都应体现一致的个人风格。然而，现有方法（如MoMo、MCM-LDM等基于扩散模型的风格迁移方法）仅通过视觉条件注入风格信息，缺乏显式机制来解耦个性特征与动作内容。这导致两个问题：（1）当输入运动的内容与目标生成内容差异较大时，个性迁移质量急剧下降；（2）模型无法在不同内容之间建立个性的一致性表征，生成的运动在风格上可能前后不一致。

更关键的是，**现有方法完全忽略了文本模态的适应**。在文本到运动生成中，文本提示是控制生成内容的核心信号。如果文本编码器无法理解“以某人的风格做某事”这一语义，模型就无法在生成过程中有效协调内容指令与个性约束。仅依赖视觉条件注入个性，相当于让模型在“盲人摸象”的状态下工作——它看到了风格参考，却无法将这种风格与语言描述建立关联。

### 本文动机与核心洞察

针对上述瓶颈，本文提出核心洞察：**将个性建模为可插拔的文本标记（Persona Token）和视觉特征（Visual Persona Feature），通过对比学习显式解耦个性与动作内容，使得扩散模型在微调时既能注入新个性又不丢失预训练的先验知识。**

这一洞察基于以下推理链：

1. **双路径自适应是必要的。** 个性信息应同时注入文本编码器和视觉扩散模型。文本路径让模型“理解”个性语义，视觉路径让模型“看到”个性模式。两者协同工作，才能实现个性与内容的协调控制。

2. **对比学习是解耦的关键。** 引入Persona Cohesion Loss（监督对比损失），强制同一性个性、不同内容的运动特征在特征空间中紧密聚集，同时推开不同个性的特征。这使得个性表征对内容变化不敏感，从而在不同动作指令下都能稳定输出一致的个性风格。

3. **上下文感知融合处理多输入。** 当提供多个体现同一性个性的原子运动时，简单的特征平均会导致风格混杂。Context-Aware Fusion（CAF）根据每个输入运动与目标文本提示的语义相似度进行软加权，优先利用与目标内容最相关的参考运动，避免不相关输入干扰个性表达。

基于上述洞察，本文提出**PersonaBooth**框架，并构建了专门用于运动个性化评估的大规模数据集**PerMo**（5位演员、34种风格、10类动作内容、6,610个运动片段，配备网格和文本标注），为这一新任务建立了系统的评估基准。

## 核心方法与创新机理

PersonaBooth 的核心创新在于首次将个性化运动生成（Motion Personalization）建模为**文本与视觉双路径自适应**问题，并通过**可插拔的 Persona Token** 与**监督对比学习**实现个性与动作内容的解耦。相较于仅依赖视觉条件注入的现有运动风格迁移方法（如 MoMo、MCM-LDM），PersonaBooth 在以下四个关键维度上引入了结构性改变：

### 1. 文本路径自适应：从纯视觉条件到多模态个性注入

现有方法在微调扩散模型时仅修改视觉条件分支，文本编码器保持冻结，导致模型难以在语义层面理解“谁的个性”。PersonaBooth 引入**可学习的 Persona Token**（$P^*$），将其嵌入模板句的占位符中，并通过个性化文本编码器与原始提示嵌入进行零门控自适应融合：

$$T^* = \mathcal{X}_{clip}(T_{in}) + s_t \cdot \tanh(\gamma_t) \cdot \mathcal{X}_{clip}(\tilde{T}_{in}, P^*)$$

这一设计使得个性信息同时从视觉和文本两条路径注入扩散模型。消融实验表明，仅添加文本自适应（$+P^*$）即可将 FID 从 7.45 降至 5.06，同时 PRA 从 17.99 升至 18.26（Table 3），证明多模态个性融合既能增强个性表达，又能提升运动合理性。

### 2. Persona Cohesion Loss：强制个性特征解耦

从不同动作内容中提取一致的个性特征是运动个性化的核心瓶颈。PersonaBooth 提出 **Persona Cohesion Loss**（$L_{pc}$），在 Persona Extractor 的输出上施加监督对比学习：

$$L_{pc} = -\log \frac{\exp(\sin(h(Y_i), h(Y_j))/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\sin(h(Y_i), h(Y_k))/\tau)}$$

该损失强制相同个性、不同内容的运动特征在特征空间中紧密聚集，同时推开不同个性的特征。消融实验显示，在文本自适应基础上添加 $L_{pc}$ 后，FID 进一步从 5.06 降至 3.18，R-Precision Top1 从 0.05 跃升至 0.15（Table 3），表明对比损失有效解耦了个性与内容，显著提升了指令跟随能力。

### 3. 视觉自适应层结构升级：Self-Attention 替代 AdaIN/Cross-Attention

在扩散 Transformer 的每个块中，PersonaBooth 在自注意力层与前馈层之间插入**Self-Attention 自适应层**，以门控方式融合视觉个性特征 $V^*$：

$$z' = z + s_v \cdot \tanh(\gamma_v) \cdot \mathrm{Adapt}([z, V^*])$$

相较于 Motion Diffusion Model 中常用的 AdaIN 或 Cross-Attention，Self-Attention 结构在 FID、R-Precision 和 PRA 上均表现最优（Table 4）。这一设计使个性特征能够与隐层特征进行更灵活的交互，而非简单的仿射变换或交叉注意力注入。

### 4. Context-Aware Fusion：从简单平均到语义加权多输入融合

当提供多个参考运动时，现有方法（如 InstantBooth 的简单平均策略）容易导致风格混杂和不自然姿态。PersonaBooth 提出 **Context-Aware Fusion（CAF）**，根据每个输入运动与文本提示的语义相似度计算软加权：

$$w_i = \begin{cases} \frac{\exp(S_i)}{\sum_n \exp(S_n)} & i \in I_{\mathrm{Top-k}} \\ 0 & \mathrm{otherwise} \end{cases}$$

CAF 仅保留 Top-k 个最相关的输入运动进行加权融合，忽略无关参考。在 $|M_i|=\max$ 设定下，CAF 将 FID 从简单平均的 3.52 降至 2.95，Diversity 升至 8.12（Table 3），有效避免了多输入融合带来的运动质量退化。

### 创新总结

PersonaBooth 的四项核心改变形成了一条完整的因果链：**Persona Token + 文本自适应**使个性信息首次进入文本条件分支；**Persona Cohesion Loss** 通过对比学习解耦个性与内容，确保特征一致性；**Self-Attention 自适应层**优化了视觉个性的注入方式；**CAF** 解决了多输入推理时的融合难题。这些创新共同使 PersonaBooth 在 PerMo 和 100Style 两个基准上均显著优于现有方法，同时仅需 50 步扩散采样（MoMo 需 100 步，MCM-LDM 需 1000 步），在推理效率上也具备明显优势。

PersonaBooth 的整体 pipeline 围绕一个核心洞察构建：将“个性”（persona）建模为可插拔的文本标记与视觉特征，通过双路径自适应注入预训练的文本-运动扩散模型，实现个性化运动生成。其工作流可概括为三个阶段：**个性提取、双路径自适应注入、上下文感知融合推理**。

### 输入与输出定义

系统接收两类输入：
1. **原子输入运动** $M_i \in \mathbb{R}^{f \cdot 263}$：一段或多段体现目标个性的运动序列，$f$ 为帧数，263 维特征包含关节旋转、位置、速度及脚接触标签。
2. **文本提示** $T_{in}$：描述期望动作内容的自然语言指令（如“A person walks in a circle”）。

输出为**个性化运动序列**：既忠实执行文本描述的动作内容，又体现输入运动所蕴含的独特个性风格。

### 阶段一：个性提取（Persona Extractor）

Persona Extractor $\mathcal{E}$ 是整个框架的入口模块（Figure 2 左侧）。它基于 TMR 结构，并将其文本编码器替换为 CLIP 文本编码器后重新训练，以共享视觉-文本嵌入空间。给定输入运动 $M$，该模块同时产出两类个性表征：

![[assets/figures/papers/paper_list_l1862_PersonalBooth_Personalized_Text_to_Motion_Generation/figures/003_Figure_2.jpg]]
*Figure 2: The overall framework of PersonaBooth. PersonaBooth has two adaptation paths—visual and text—for finetuning the Motion Diffusion model (D). The Persona Extractor extracts both a visual persona feature*

- **视觉个性特征** $V^* = \mathcal{E}([\text{cls}], M)$：从运动序列中提取的全局视觉风格表征，用于后续视觉路径的自适应注入。
- **个性标记** $P^* = \text{MLP}(Y), \quad Y = V^*[0]$：将视觉特征的首个元素通过 MLP 映射到与 CLIP 文本嵌入对齐的空间，形成可嵌入自然语言模板的“文本个性标记”。

这一双输出设计是后续双路径自适应的前提：$V^*$ 负责在扩散模型的 Transformer 层中调节运动生成过程，$P^*$ 负责在文本端引导语义对齐。

### 阶段二：双路径自适应注入

PersonaBooth 的核心创新在于同时对扩散模型的文本条件路径和视觉特征路径进行个性化微调（Figure 2 中部及 Figure 3）。

**文本路径**——个性化文本编码器（Personalized Text Encoder）：
将 $P^*$ 插入模板句（如“a person with $P^*$ motion style”）的占位符中，形成个性化提示 $\tilde{T}_{in}$。随后通过零门控自适应机制融合原始提示嵌入与个性化嵌入：

$$T^* = \mathcal{X}_{clip}(T_{in}) + s_t \cdot \tanh(\gamma_t) \cdot \mathcal{X}_{clip}(\tilde{T}_{in}, P^*)$$

其中 $\gamma_t$ 为可学习的门控参数，$s_t$ 为缩放因子。该设计使模型在微调初期保持原始文本理解能力，逐步注入个性信息，避免灾难性遗忘。

**视觉路径**——视觉自适应层（Visual Adaptive Layer）：
在扩散模型每个 Transformer 块的自注意力层与前馈层之间插入自适应层（Figure 3b），以门控方式融合 $V^*$：

$$z' = z + s_v \cdot \tanh(\gamma_v) \cdot \text{Adapt}([z, V^*])$$

其中 $z$ 为隐层特征，$\text{Adapt}$ 为自适应层（实验表明 Self-Attention 结构最优，优于 AdaIN 和 Cross-Attention）。该层使扩散模型在去噪过程中持续感知目标个性特征。

### 阶段三：训练与推理

**训练目标**由两部分加权组成：

$$\mathcal{L} = \mathcal{L}_D + \lambda \mathcal{L}_{pc}$$

其中 $\mathcal{L}_D$ 为扩散重建损失（含几何正则项 $L_{geo}$），$\lambda=10^{-2}$。关键创新在于 **Persona Cohesion Loss** $\mathcal{L}_{pc}$——一种监督对比损失，作用于 Persona Extractor 的输出特征 $Y$：

$$L_{pc} = -\log \frac{\exp(\text{sim}(h(Y_i), h(Y_j))/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(h(Y_i), h(Y_k))/\tau)}$$

该损失强制同一演员、不同动作内容的运动特征在嵌入空间中紧密聚集，同时推开不同演员的特征，从而解耦个性与动作内容。

**推理时**采用 Classifier-Free Guidance（CFG），混合文本引导分支 $\mathcal{D}_T$ 与视觉引导分支 $\mathcal{D}_V$：

$$\hat{\mathcal{D}}(M^t, t, V^*, T^*) = b \mathcal{D}_T + (1-b) \mathcal{D}_V$$

通过调节平衡因子 $b$ 控制多样性与个性保真度的权衡。

**多输入推理**时，Context-Aware Fusion（CAF）模块计算各输入运动与文本提示的相似度 $S_i$，取 Top-k 进行软加权融合：

$$w_i = \begin{cases} \frac{\exp(S_i)}{\sum_n \exp(S_n)} & i \in I_{\text{Top-k}} \\ 0 & \text{otherwise} \end{cases}$$

该机制避免简单平均带来的风格混杂与不自然姿态，使模型能从多个参考运动中智能筛选最相关的个性信息。

### 模块间数据流总结

```
输入运动 M ──→ Persona Extractor ──→ V* ──→ Visual Adaptive Layers ──→ 扩散去噪 ──→ 个性化运动
                    │                                        ↑
                    └──→ P* ──→ Personalized Text Encoder ──→ T* ──→ CFG 混合推理
```

PersonaBooth 通过这一“提取-注入-融合”三段式 pipeline，在仅微调少量新增参数的前提下，实现了对预训练文本-运动扩散模型的个性化适配，既保留了预训练先验，又注入了新个性特征。

PersonaBooth 的核心架构由五个关键模块构成，围绕视觉与文本双路径自适应展开，并通过对比学习实现个性与内容的解耦。

### 3.1 Persona Extractor 与 Persona Cohesion Loss

**Persona Extractor** 负责从输入运动序列中同时提取视觉个性特征 $V^*$ 和 Persona Token $P^*$。其结构基于 TMR，但将原有的文本编码器替换为 CLIP 文本编码器并重新训练，使提取器能够将运动个性映射到与文本共享的嵌入空间。

给定输入运动 $M_i \in \mathbb{R}^{f \cdot 263}$（$f$ 为帧数，263 维包含关节旋转、位置、速度及脚接触标签），提取过程为：

$$V^* = \mathcal{E}([\text{cls}], M]) \tag{1}$$

其中 $\mathcal{E}$ 为 Persona Extractor，$[\text{cls}]$ 为类别标记。随后，取 $V^*$ 的首元素 $Y = V^*[0]$，通过 MLP 映射得到 Persona Token：

$$P^* = \mathrm{MLP}(Y) \tag{2}$$

$P^*$ 被设计为与 CLIP 文本嵌入空间对齐，使其可作为可学习的文本标记注入个性化文本编码器。

**Persona Cohesion Loss** $L_{pc}$ 采用监督对比学习方案，强制相同个性、不同内容的运动在特征空间中紧密聚集，同时推开不同个性的运动特征。该损失作用于 Persona Extractor 的输出 $Y$ 上：

$$L_{pc} = -\log \frac{\exp(\text{sim}(h(Y_i), h(Y_j))/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(h(Y_i), h(Y_k))/\tau)} \tag{3}$$

其中 $h(\cdot)$ 为投影头，$\text{sim}$ 为余弦相似度，$\tau$ 为温度参数。这一损失是解耦个性与动作内容的关键——它迫使提取器忽略内容差异，只保留个性本质。

### 3.2 Personalized Text Encoder 与 Visual Adaptive Layer

**Personalized Text Encoder** 实现文本路径的自适应。将 $P^*$ 替换模板句中的占位符后，通过零门控自适应机制融合原始文本嵌入与个性化嵌入：

$$T^* = \mathcal{X}_{\text{clip}}(T_{in}) + s_t \cdot \tanh(\gamma_t) \cdot \mathcal{X}_{\text{clip}}(\tilde{T}_{in}, P^*) \tag{4}$$

其中 $\mathcal{X}_{\text{clip}}$ 为 CLIP 文本编码器，$T_{in}$ 为原始提示，$\tilde{T}_{in}$ 为包含 $P^*$ 占位符的模板句，$s_t$ 为缩放因子，$\gamma_t$ 为可学习的门控参数。零初始化 $\gamma_t$ 使训练初期保持原始文本特征，逐步注入个性信息，避免灾难性遗忘。

**Visual Adaptive Layer** 在扩散 Transformer 的每个 block 中，于自注意力层与前馈网络之间插入自适应层，融合视觉个性特征 $V^*$：

$$z' = z + s_v \cdot \tanh(\gamma_v) \cdot \mathrm{Adapt}([z, V^*]) \tag{5}$$

其中 $z$ 为当前隐层特征，$\mathrm{Adapt}$ 为自适应层（消融实验表明 Self-Attention 结构优于 AdaIN 和 Cross-Attention），同样采用零门控机制。

### 3.3 训练目标与采样策略

微调阶段的扩散损失结合标准重建误差与预训练的几何正则项 $L_{geo}$：

$$L_D := \mathbb{E}_{M^0, t, T} \left[ \| M^0 - \mathcal{D}(M^t, t, V^*, T^*) \|_2^2 \right] + L_{geo} \tag{6}$$

最终训练目标为扩散损失与 Persona Cohesion Loss 的加权和（$\lambda = 10^{-2}$）：

$$\mathcal{L} = \mathcal{L}_D + \lambda \mathcal{L}_{pc} \tag{7}$$

推理时采用 Classifier-Free Guidance，混合文本引导分支 $\mathcal{D}_T$ 与视觉引导分支 $\mathcal{D}_V$：

$$\hat{\mathcal{D}}(M^t, t, V^*, T^*) = b \mathcal{D}_T + (1-b) \mathcal{D}_V \tag{8}$$

其中 $b$ 为平衡因子，控制多样性与个性保真度之间的权衡。

### 3.4 Context-Aware Fusion (CAF)

当提供多个参考运动时，CAF 根据各输入运动与文本提示的相似度进行软加权融合，避免简单平均带来的风格混杂。对每个输入运动 $M_i$ 计算其与提示的相似度 $S_i$，取 Top-k 进行 softmax 归一化：

$$w_i = \begin{cases} \frac{\exp(S_i)}{\sum_n \exp(S_n)} & i \in I_{\text{Top-k}} \\ 0 & \text{otherwise} \end{cases} \tag{9-10}$$

最终融合特征为加权和，忽略不相关的输入运动，使生成结果既保留个性又忠实于文本描述。

## 实验与关键发现

### 核心主张验证

PersonaBooth 的设计围绕一个核心瓶颈展开：将通用文本-运动扩散模型适配到个性化运动生成时，预训练数据（HumanML3D）与个性化数据（PerMo）之间存在显著分布差异，且从不同动作内容中提取一致的个性特征极为困难。现有方法仅关注视觉条件而忽略文本适应，导致生成质量低和个性遗忘。

针对这一问题，PersonaBooth 引入了两个关键因果调节变量：
1. **可学习的 Persona Token**，实现文本与视觉双路径自适应；
2. **Persona Cohesion Loss**（监督对比学习），强制相同个性、不同内容的运动特征在特征空间中紧密聚集。

消融实验（Table 3）系统验证了这一设计逻辑：

![[assets/figures/papers/paper_list_l1862_PersonalBooth_Personalized_Text_to_Motion_Generation/figures/008_Table_3.jpg]]
*Table 3: Ablation study of the proposed components*

| 配置 | FID ↓ | R Precision Top1 ↑ | PRA ↑ | Diversity ↑ |
|------|-------|-------------------|-------|-------------|
| Baseline（仅视觉自适应） | 7.45 | 0.05 | 17.99 | 7.74 |
| + P*（引入文本自适应） | 5.06 | 0.05 | 18.26 | 8.00 |
| + L_pc（加入对比损失） | **3.18** | **0.15** | 18.56 | 8.09 |

**文本自适应（P\*）的贡献**：引入 Persona Token 后，FID 从 7.45 降至 5.06（降幅 32%），PRA 从 17.99 升至 18.26。这表明多模态个性信息融合既能增强个性表达，又能提升运动合理性。仅依赖视觉特征时，模型难以在文本层面建立个性与描述的关联，导致生成运动虽然可能带有风格痕迹，但与文本指令的契合度不足。

**Persona Cohesion Loss（L_pc）的关键作用**：进一步加入对比损失后，FID 降至 3.18（累计降幅 57%），更值得注意的是 R Precision Top1 从 0.05 跃升至 0.15（提升 200%）。这一跳跃揭示了 L_pc 的核心机制——通过强制同一 Persona 的运动特征在嵌入空间中聚集，Persona Extractor 学会了将个性从动作内容中解耦。当内容解耦完成后，模型在推理时能更精准地跟随文本指令，因为个性特征不再与特定动作模式绑定。

**视觉自适应层类型选择**（Table 4）：Self-Attention 作为自适应层结构优于 AdaIN 和 Cross-Attention。在扩散 Transformer 的自我注意与 FFN 间插入 Self-Attention 自适应层（Eq.5），配合零门控机制 $s_v \cdot \tanh(\gamma_v)$，实现了最稳定的个性注入。这可能是由于 Self-Attention 能更好地建模运动序列内部的长程依赖与个性特征的交互，而 AdaIN 的全局统计归一化可能丢失了细粒度的时序个性线索。

### 多输入融合：Context-Aware Fusion (CAF)

当提供多个参考运动时，如何有效融合多个输入而不引入噪声是一个关键挑战。简单平均（InstantBooth 方式）在 $|M_i|=\max$ 设定下 FID 为 3.52，而 CAF 将其降至 **2.95**，Diversity 同时升至 **8.12**（Table 3）。

CAF 的工作机制（Eq.9-11）是：计算每个输入运动与文本提示的相似度 $S_i$，仅对 Top-k 相似度进行 softmax 加权，忽略与当前文本无关的参考运动。这避免了简单平均导致的“风格混杂”问题——当多个参考运动中部分与目标动作无关时，平均操作会将无关的个性特征也注入生成过程，导致不自然的姿态。Figure 5 的可视化消融也佐证了这一点：无 CAF 时生成运动出现僵硬或混杂的姿态，加入 CAF 后运动流畅性显著改善。

![[assets/figures/papers/paper_list_l1862_PersonalBooth_Personalized_Text_to_Motion_Generation/figures/007_Figure_5.jpg]]
*Figure 5: Example of the ablation study. The input motions are from the ‘Uppity’ of Actor 1. The input prompt is “A person walks in a circle.” In (a) and (b), only M1 is provided for the input, while both*

### 与现有方法的对比

**PerMo 数据集**（Table 5）：在单输入设定下，PersonaBooth 的 FID 为 3.18，显著优于 **MoMo** 和 **MCM-LDM**（微调版本）。值得注意的公平性前提是：PersonaBooth 基于 50 步扩散模型，而 MoMo 使用 100 步、MCM-LDM 使用 1000 步，因此 PersonaBooth 在推理效率上有明显优势的同时仍取得了更优的生成质量。

**100Style 数据集**（Table 6）：PersonaBooth 的 FID 为 3.27，R Precision Top1 为 0.20，而 MoMo 的 R Precision Top1 仅为 0.07。这一差距（+0.13）进一步验证了文本自适应路径在跨数据集泛化中的重要性——100Style 的运动风格分布与 PerMo 不同，但 Persona Token 的文本嵌入对齐机制使模型能快速适应新的个性表达。

### 失败模式与局限

1. **运动长度不可控**：当前模型无法自动调整生成运动长度。当目标运动短于模型默认输出长度时，序列末尾可能出现静止姿态。这是因为扩散模型在训练时以固定帧数进行重建，推理时缺乏显式的长度控制机制。

2. **复杂连续指令支持不足**：CAF 尚未支持对文本中多个连续动作（如“跑然后跳”）分别赋予不同的参考输入。这意味着当文本包含多个动作阶段时，所有阶段共享同一组个性权重，可能导致某个阶段的个性化质量下降。这是 CAF 从“全局加权”扩展到“逐阶段加权”的自然延伸方向。

3. **对比损失的定量边界**：Persona Cohesion Loss 与现有运动风格迁移中的风格解耦损失（如 MoST 的相关损失）在定量上的优劣尚未直接对比。虽然 L_pc 在 PerMo 上展现了显著效果，但其在更大规模预训练数据集上的泛化能力仍是一个开放问题。

### 关键图表指引

- **Table 3**：消融实验的核心证据表，展示了 P\*、L_pc、CAF 的逐步增益。建议重点关注 FID 的阶梯式下降和 R Precision 在加入 L_pc 后的跃升。
- **Table 4**：自适应层类型消融，确认 Self-Attention + Text Adaptation 的最优组合。
- **Table 5 & Table 6**：分别在 PerMo 和 100Style 上与 MoMo、MCM-LDM 的 SOTA 对比，验证跨数据集的泛化能力。
- **Figure 5**：消融实验的可视化示例，直观展示 L_pc 和 CAF 对生成运动自然度的影响。
- **Figure 6**：不同演员在相同“Childish”类别下的个性化生成对比，红色箭头标注了个性差异的关键帧，是定性理解 PersonaBooth 效果的重要参考。

![[assets/figures/papers/paper_list_l1862_PersonalBooth_Personalized_Text_to_Motion_Generation/figures/011_Table_5.jpg]]
*Table 5: Comparison with the state-of-the-art methods on the PerMo dataset. The comparison is made in the Single Input (SI) setting as the existing methods do not support multiple inputs. MCM-LDM* indicates the model is finetuned on the PerMo dataset*

![[assets/figures/papers/paper_list_l1862_PersonalBooth_Personalized_Text_to_Motion_Generation/figures/014_Table_6.jpg]]
*Table 6: Comparison with the state-of-the-art methods on the 100Style dataset. MCM-LDM* indicates the model is finetuned on the 100Style dataset*

![[assets/figures/papers/paper_list_l1862_PersonalBooth_Personalized_Text_to_Motion_Generation/figures/010_Table_4.jpg]]
*Table 4: Ablation study regarding adaptation. PersonaBooth (SI) indicates our complete model for single inputs*

## 定位与知识库关联

### 任务定位：从风格迁移到运动个性化

PersonaBooth 所定义的 **Motion Personalization** 任务，处于文本驱动运动生成（Text-to-Motion, T2M）与运动风格迁移（Motion Style Transfer, MST）的交汇地带，但与前两者存在本质差异。传统 T2M 仅从文本生成通用运动，不包含任何特定个体风格；而 MST 通常要求源运动与目标风格运动在内容上严格对齐（如相同的动作序列），其核心是“内容保持、风格替换”。PersonaBooth 则解耦了这一约束：它从少量原子运动（atomic motions）中提取某个演员的“个性”（persona），随后在**任意文本指令**下生成既忠实于描述又体现该个性的运动——输入运动与生成运动的内容可以完全不同。这一设定使得 PersonaBooth 更接近图像领域的个性化生成（如 DreamBooth），但在运动模态中首次系统性地引入了文本与视觉双路径自适应。

### 与现有方法的谱系关系

在运动风格迁移领域，**MoMo** 是一种基于扩散模型的零样本方法，通过将风格运动作为视觉条件注入生成过程来实现风格迁移，无需针对特定风格微调。**MCM-LDM** 则采用微调策略，对预训练扩散模型进行风格适配。PersonaBooth 在方法论上继承了扩散模型微调的范式，但其关键突破在于：

1. **多模态自适应**：MoMo 和 MCM-LDM 仅依赖视觉条件（将风格运动特征作为扩散模型的附加输入），而 PersonaBooth 引入了可学习的 Persona Token（$P^*$），通过个性化文本编码器将个性信息同时注入**文本条件分支**。这一设计源于一个关键观察：预训练的 T2M 模型在微调时，若仅修改视觉路径，文本编码器对“个性”概念完全无知，会导致文本-运动对齐退化。通过零门控（zero-gated）自适应融合原始文本嵌入与包含 $P^*$ 的个性化嵌入（Eq. 4），PersonaBooth 在注入新个性的同时保留预训练先验。

2. **对比解耦机制**：Persona Cohesion Loss（$L_{pc}$）是 PersonaBooth 的核心创新。该损失采用监督对比学习范式，强制**同一演员、不同动作内容**的运动特征在 Persona Extractor 的特征空间中紧密聚集，同时推开不同演员的特征。这与 MST 中常见的风格解耦损失（如 MoST 的对抗损失或互信息最小化）在目标上相似，但在实现路径上不同——$L_{pc}$ 直接作用于 Persona Token 的嵌入空间，且与 CLIP 文本编码器的嵌入空间对齐，使得个性特征天然具备与文本交互的能力。

3. **上下文感知融合**：在多输入推理场景下，PersonaBooth 的 Context-Aware Fusion（CAF）根据输入运动与文本提示的相似度进行 Top-k 软加权（Eq. 9-11），避免了简单平均（如 InstantBooth 的策略）带来的风格混杂和不自然姿态。消融实验表明，CAF 将 FID 从 3.52 降至 2.95，Diversity 升至 8.12（Table 3）。

### 适用边界与局限

PersonaBooth 的当前设计存在以下边界条件：

- **运动长度固定**：模型无法根据文本语义自动调整生成运动的帧数。当目标动作短于预设长度时，序列末尾可能出现静止或重复姿态，这在定性结果中有所体现。
- **复杂指令支持有限**：CAF 目前对整个文本提示赋予统一的参考运动权重，无法处理包含多个连续动作的指令（如“跑然后跳”），即不能为每个子动作分别指定不同的参考输入。这限制了在长时序、多阶段运动生成中的个性化质量。
- **数据依赖性**：Persona Extractor 基于 TMR 结构并使用 CLIP 文本编码器重新训练，其个性提取能力依赖于 PerMo 数据集的规模与多样性。PerMo 包含 5 名演员、34 种风格、6,610 个片段，在演员数量上仍有限，模型对未见演员的泛化能力尚未验证。
- **扩散步数效率**：PersonaBooth 基于 50 步扩散模型，相比 MoMo（100 步）和 MCM-LDM（1000 步）在推理速度上有明显优势，但这一优势来源于底层预训练模型的选择，而非方法本身的加速设计。

### 开放问题

1. **对比损失的定量比较**：Persona Cohesion Loss 与现有 MST 中的风格解耦损失（如 MoST 的对抗训练策略）在定量指标上的优劣尚未直接对比。虽然 $L_{pc}$ 在 PersonaBooth 的消融中表现出显著增益（FID 从 5.06 降至 3.18，R-Precision Top1 从 0.05 升至 0.15），但若将其替换为其他解耦损失，性能差异如何仍是开放问题。

2. **多阶段个性化生成**：如何将 CAF 扩展为对文本中每个序列动作单独加权，以支持“先跑后跳”等复合指令的细粒度个性化？这需要将文本解析为动作序列，并为每个子动作匹配最相关的参考运动，涉及文本-运动时序对齐与动态权重分配。

3. **跨数据集泛化**：Persona Token 的多模态适应机制在更大规模预训练数据集（如结合 HumanML3D 与更多风格数据）上的泛化能力如何？当前 PerMo 的 34 种风格类别（Table A）覆盖了情绪与动作风格，但真实世界中的人体运动个性维度远不止于此，模型能否在更细粒度或跨文化的个性表达上保持有效性，尚需验证。

4. **个性可组合性**：PersonaBooth 将个性建模为单一 Token，但真实个体的运动风格可能包含多个可分离维度（如“优雅”与“急促”的组合）。未来是否可解耦为多个子 Token 并支持个性插值或组合，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2025/PersonalBooth_Personalized_Text_to_Motion_Generation.pdf]]

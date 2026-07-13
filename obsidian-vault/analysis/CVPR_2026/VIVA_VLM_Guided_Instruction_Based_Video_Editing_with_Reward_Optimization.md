---
title: "VIVA: VLM-Guided Instruction-Based Video Editing with Reward Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VIVA_VLM_Guided_Instruction_Based_Video_Editing_with_Reward_Optimization.pdf
project_link: "https://viva-paper.github.io/"
code_link: null
aliases:
- VIVA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: VLM instructor提供的多模态视觉根植指令表示和Edit-GRPO强化学习后训练阶段。
primary_logic: 利用VLM将文本指令、源视频首帧和可选参考图像联合编码为精细的视觉根植表示，并通过基于相对奖励的GRPO直接优化编辑忠实度、内容保留和人类偏好，使得即使在简单编辑数据上训练也能实现复杂编辑的泛化。
claims:
- 在VIE-Bench基准上，VIVA在所有开源方法中取得最高的VLM评估平均分，在添加、替换、删除等任务上均大幅领先。
- 消融研究证实，VLM instructor、掩码损失、混合图像数据以及Edit-GRPO每个组件都对编辑性能有显著贡献。
- 用户研究中，VIVA在指令遵循、源视频保留和编辑质量三个维度上均被14位专家显著偏爱。
- VIE-Bench (Add task) 上 Avg. VLM Evaluation Score = 8.86
---

# VIVA: VLM-Guided Instruction-Based Video Editing with Reward Optimization

> [!tip] 核心洞察
> 利用VLM将文本指令、源视频首帧和可选参考图像联合编码为精细的视觉根植表示，并通过基于相对奖励的GRPO直接优化编辑忠实度、内容保留和人类偏好，使得即使在简单编辑数据上训练也能实现复杂编辑的泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | VIVA: 基于VLM引导的指令视频编辑与奖励优化 |
| 英文题名 | VIVA: VLM-Guided Instruction-Based Video Editing with Reward Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16906) · [Project](https://viva-paper.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VIVA |
| Dataset | VIE-Bench |

> [!tip] 效果简介
> - VIE-Bench (Add task) 上，Avg. VLM Evaluation Score 8.86 vs ICVE 7.22 (+1.64)。
> - VIE-Bench (Replace task) 上，Avg. VLM Evaluation Score 8.86 vs ICVE 7.02 (+1.84)。
> - VIE-Bench (Remove task) 上，Avg. VLM Evaluation Score 9.44 vs ICVE 7.04 (+2.40)。

## 概要

### 问题背景与瓶颈

指令驱动的视频编辑旨在根据用户的自然语言指令对视频内容进行修改，如添加、替换或删除对象。现有方法通常依赖合成的简单编辑配对数据进行训练，这些配对数据覆盖的操作类型有限（如仅包含基本的添加或删除），导致模型难以泛化到真实场景中复杂、开放域的编辑指令。核心瓶颈在于：**缺乏对指令的精细视觉根植理解**——纯文本编码器无法充分捕捉指令中涉及的目标实体、空间位置和外观细节，而合成数据的简单性又限制了模型对组合指令和细粒度编辑的响应能力。

### 核心方法定位

VIVA 针对上述瓶颈提出了两个关键创新：

1. **VLM Instructor（视觉-语言模型引导器）**：将文本编辑指令、源视频首帧和可选的参考图像联合编码为多模态条件令牌，为扩散模型提供视觉根植的指令表示。这使得模型即使在简单编辑数据上训练，也能理解复杂的编辑意图。

2. **Edit-GRPO 后训练阶段**：在标准Flow Matching预训练之后，引入基于组相对策略优化（GRPO）的强化学习阶段，通过组合奖励函数（指令遵循、源视频保留、人类偏好）直接优化编辑质量，仅更新LoRA参数，高效且稳定。

### 主要结果

在指令视频编辑基准 VIE-Bench 上，VIVA 在所有开源方法中取得了最高的 VLM 评估平均分：添加任务 8.86（对比最强基线 ICVE 的 7.22）、替换任务 8.86（对比 7.02）、删除任务 9.44（对比 7.04），分别领先 +1.64、+1.84 和 +2.40。消融研究证实，VLM instructor、掩码损失、混合图像数据训练以及 Edit-GRPO 每个组件都对编辑性能有显著贡献。用户研究中，14 位专家在指令遵循、源视频保留和编辑质量三个维度上均显著偏爱 VIVA 的结果。



指令驱动的视频编辑旨在根据自然语言指令对输入视频进行局部修改，同时保持未编辑区域不变。近年来，扩散模型在图像编辑领域的成功激发了研究者将其扩展到视频编辑的尝试。然而，视频编辑面临一个核心瓶颈：**现有方法受限于简单编辑操作的合成配对数据，难以泛化到复杂、开放域的真实指令**。

具体而言，当前指令视频编辑方法（如 **ICVE**、**InsV2V**、**Ditto** 等）通常依赖仅包含添加、删除、替换等基础操作的合成训练对。这些数据的编辑类型覆盖范围窄，且指令文本往往过于简化，导致模型在面对现实世界中细粒度、组合式的编辑需求时表现不佳。例如，用户可能要求“将画面中的咖啡杯替换为一只正在喝水的橙色虎斑猫，并保持桌面的光影一致”，这类复杂指令要求模型同时理解对象语义、空间位置、外观细节以及场景一致性，远超简单合成数据的覆盖范围。

另一个关键限制在于**指令表示的质量**。主流方法通常仅使用纯文本编码器（如 T5）将编辑指令编码为条件信号。这种纯文本表示缺乏对视频内容的视觉根植（visual grounding），模型无法将指令中的实体与视频中的具体区域和对象建立精确对应，导致编辑区域定位不准、编辑效果与指令意图偏差较大。

此外，现有方法的训练范式通常止步于监督微调阶段，缺乏对编辑质量（如指令忠实度、内容保留度、视觉美观度）的显式优化。这导致模型在复杂场景下容易产生伪影、过度编辑或编辑不足等问题。

针对上述缺口，**VIVA** 提出两条关键思路：(1) 引入 **VLM Instructor**，利用视觉-语言模型将文本指令、源视频首帧和可选参考图像联合编码为精细的视觉根植表示，弥补纯文本编码器的空间理解不足；(2) 设计 **Edit-GRPO** 后训练阶段，通过基于相对奖励的强化学习直接优化编辑的指令遵循度、源视频保留度和人类偏好。这两项设计使得即使在简单编辑数据上训练的模型也能实现对复杂编辑指令的泛化。



## 核心方法与创新机理

VIVA 的核心创新在于破解了现有指令视频编辑方法受限于简单编辑操作合成配对数据、难以泛化到复杂开放域真实指令的瓶颈。其关键调控旋钮（causal knob）由两部分构成：**VLM instructor** 提供的多模态视觉根植指令表示，以及 **Edit-GRPO** 强化学习后训练阶段。核心洞察是：利用 VLM 将文本指令、源视频首帧和可选参考图像联合编码为精细的视觉根植表示，并通过基于相对奖励的 GRPO 直接优化编辑忠实度、内容保留和人类偏好，使得即使在简单编辑数据上训练也能实现复杂编辑的泛化。

与现有基准方法相比，VIVA 在四个关键 slot 上做出了实质性改变：

### 1. 指令编码器：从纯文本到多模态视觉根植

现有方法（如 ICVE、InsV2V、Ditto 等）普遍使用纯文本编码器（如 T5）将编辑指令编码为条件信号。这种文本-only 的表示方式缺乏对源视频视觉上下文的感知，难以精确定位编辑区域和理解编辑意图。

VIVA 提出 **VLM instructor**（Section 3.1），将输入扩展为三元组——编辑指令 $\mathbf{t}_{ins}$、源视频首帧 $\mathbf{I}_{src}$ 和可选参考图像 $\mathbf{I}_{ref}$，通过 VLM 联合编码为视觉根植的多模态条件令牌：

$$\mathbf{x}_{vlm} = \mathrm{VLM}(\mathbf{t}_{ins}, \mathbf{I}_{src}, \mathbf{I}_{ref})$$

这一设计使指令表示同时包含文本语义、空间定位和视觉参考信息，大幅提升了对复杂编辑指令的理解精度。消融实验证实，引入 VLM instructor 后所有评估指标均有显著提升（Table 2）。

### 2. 训练目标：引入掩码加权的空间先验

标准 Flow Matching 损失对视频所有区域施加均匀的优化压力，缺乏对编辑区域的针对性。VIVA 将其改造为带掩码加权的版本（Eq. 3）：

$$\mathcal{L}_{\mathrm{mask}} = (\mathbf{1} + w_{m}M)\mathcal{L}_{\mathrm{FM}}$$

其中 $M$ 为编辑掩膜视频，$w_m$ 为加权系数。这一设计引入了有效的空间归纳偏置，使模型将优化重点聚焦于编辑区域，同时加速收敛并提升编辑精度。消融研究验证了掩码损失对编辑能力的显著贡献（Table 2）。

### 3. 训练数据：混合大规模图像编辑数据

现有视频编辑方法仅使用视频编辑对进行训练，受限于视频编辑数据的规模和类别覆盖。VIVA 创新性地将大规模图像编辑数据视为单帧视频混入训练（Section 3.2, Section 4.5），利用图像数据更广泛的编辑类别覆盖和更大规模，显著提升了模型的编辑能力和视觉质量。消融实验确认该策略对性能有重要贡献（Table 2）。

### 4. 后训练策略：Edit-GRPO 强化学习优化

这是 VIVA 最独特的设计。现有方法在标准监督微调后直接部署，缺乏对编辑质量的多维度显式优化。VIVA 提出 **Edit-GRPO**（Section 3.3），在 Group Relative Policy Optimization (GRPO) 框架下，通过三项组合奖励直接优化模型：

- **指令遵循奖励** $\mathbf{R}_{\mathrm{IF}}$（Eq. 4）：编辑视频与编辑描述的 CLIP 相似度减去与源描述的相似度，衡量编辑是否忠实于指令。
- **源视频保留奖励** $\mathbf{R}_{\mathrm{SP}}$（Eq. 5）：源视频与编辑视频的 CLIP 相似度，确保非编辑区域不被破坏。
- **人类偏好奖励** $\mathbf{R}_{\mathrm{PS}}$（Eq. 6）：使用 PickScore 评估编辑视频的整体质量和与指令的符合度。

总奖励为三者加权和（Eq. 7）：

$$\mathbf{R} = w_{IF}\mathbf{R}_{\mathrm{IF}} + w_{SP}\mathbf{R}_{\mathrm{SP}} + w_{PS}\mathbf{R}_{\mathrm{PS}}$$

Edit-GRPO 通过 Flow-SDE 注入随机性生成多样样本，计算相对优势后更新模型，且仅训练 LoRA 参数以保证效率。消融实验表明，应用 Edit-GRPO 后模型在指令遵循、源视频保留和视觉美观方面获得全面增益，定性结果也显示更少的伪影和更强的泛化能力（Table 2, Figure 10）。

### 创新总结

VIVA 的四项 changed slots 形成了互补的创新链条：VLM instructor 提供更强的指令理解，掩码损失提供空间先验，图像数据混合弥补数据多样性不足，Edit-GRPO 则在强化学习框架下直接优化多维度编辑质量。这一组合使得 VIVA 在 VIE-Bench 基准上全面超越所有开源方法，在添加、替换、删除任务上分别领先最强基线 ICVE 达 +1.64、+1.84 和 +2.40 分（Table 1），用户研究中也获得 14 位专家的显著偏爱（Figure 5）。



VIVA 的整体流水线围绕两个核心分支构建：一个**生成分支**负责在条件引导下生成编辑视频，一个**理解分支**负责将多模态编辑指令编码为精细的视觉根植表示。这两个分支通过可训练的 Token Refiner 进行对齐，并在后训练阶段经由 Edit-GRPO 强化学习进一步优化。

### 流水线概览

Figure 2 给出了 VIVA 的完整架构。其工作流程如下：

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of VIVA. A context-aware VLM instructor encodes the system prompt, instruction, first frame of the source video, and an optional reference image into VLM tokens. A trainable token refiner aligns these tokens to the pretrained DiT latent space. The VAE encodings of the source video and optional reference image are added to the noisy latent to form context-aware noise tokens. Finally, the DiT denoises these tokens under VLM guidance to generate the edited video*

1. **多模态条件编码**：VLM Instructor 接收系统提示、编辑指令文本、源视频首帧和可选的参考图像，输出一组多模态条件令牌 $\mathbf{x}_{vlm}$（见 Eq. 1）。这些令牌联合编码了目标实体、空间区域和编辑语义，为后续生成提供视觉根植的指令表示。

2. **条件令牌对齐**：Token Refiner 将 VLM 输出的条件令牌映射到预训练 DiT 的潜在空间，增强模型对视觉条件的响应能力。

3. **上下文感知视频令牌构建**：将源视频的 VAE 编码 $\mathbf{z}_{src}$ 与噪声潜在 $\mathbf{z}_{noise}$ 在通道维拼接后，通过可学习投影 $\mathcal{P}$ 生成上下文感知的视频令牌 $\mathbf{x}_{video}$（见 Eq. 2）。这一设计使模型在去噪过程中能够显式感知源视频的运动和结构信息。

4. **DiT 去噪生成**：Diffusion Transformer 骨干网络在 VLM 条件的引导下，对上下文感知视频令牌进行迭代去噪，最终生成编辑视频。

5. **Edit-GRPO 后训练**（Figure 3）：在基础训练完成后，引入基于 GRPO 的强化学习阶段。通过 Flow-SDE 注入随机性以生成多样化的编辑样本，利用组合奖励函数（指令遵循 $\mathbf{R}_{IF}$、源保留 $\mathbf{R}_{SP}$、人类偏好 $\mathbf{R}_{PS}$，见 Eq. 4-7）对样本评分，并基于相对优势计算 GRPO 损失来更新模型。为保持效率，此阶段仅优化 DiT 骨干上的 LoRA 参数。

### 模块间关系

流水线中的各模块形成清晰的分工与协作关系：

- **VLM Instructor → Token Refiner → DiT**：构成条件信号的传递链。VLM Instructor 负责“理解”——将模糊的文本指令根植到具体的视觉内容上；Token Refiner 负责“对齐”——弥合 VLM 与 DiT 之间的表示鸿沟；DiT 负责“执行”——在条件引导下完成视频生成。

- **上下文感知视频令牌与 VLM 条件的交互**：视频令牌保留了源视频的时空结构，VLM 条件提供了编辑目标的空间与语义指引，二者在 DiT 的交叉注意力层中融合，使编辑既能精准定位又不过度破坏未编辑区域。

- **Edit-GRPO 作为闭环优化**：基础训练阶段使用带掩码加权的 Rectified Flow 损失（Eq. 3）进行监督学习；Edit-GRPO 则通过奖励信号直接优化编辑的忠实度、内容保留和视觉质量，形成一个从“生成-评分-优化”的闭环。

### 输入输出规范

**输入**：
- 源视频 $\mathbf{V}_{src}$
- 编辑指令文本 $\mathbf{t}_{ins}$
- 可选的参考图像 $\mathbf{I}_{ref}$（用于指定编辑内容的视觉外观）

**输出**：
- 编辑后的视频 $\mathbf{V}_{edit}$

**关键中间表示**：
- $\mathbf{x}_{vlm}$：多模态条件令牌（VLM Instructor 输出）
- $\mathbf{x}_{video}$：上下文感知视频令牌（投影后输入 DiT）
- 编辑掩膜 $M$：用于加权训练损失，强化编辑区域的优化

> **注意**：训练阶段还引入了混合图像编辑数据的策略——将图像视为单帧视频，与视频编辑对联合训练，以弥补视频编辑数据在编辑类型覆盖上的不足。消融实验（Table 2）证实了这一策略对编辑能力和视觉质量的显著提升。



VIVA 的整体架构围绕一个核心设计原则展开：**将视觉-语言模型（VLM）的深层语义理解能力与扩散变换器（DiT）的生成能力深度耦合**，并通过强化学习后训练显式优化编辑行为。以下从条件编码、视频令牌构建、损失函数和奖励优化四个关键环节展开。

---

### 3.1 VLM Instructor：多模态视觉根植指令编码

现有指令视频编辑方法普遍采用纯文本编码器（如 T5）处理编辑指令，这导致两个关键瓶颈：文本难以精确描述空间区域和目标实体外观，且模型无法利用源视频本身的视觉上下文进行推理。VIVA 的 **VLM Instructor** 模块通过联合编码文本指令、源视频首帧和可选参考图像，生成视觉根植的多模态条件令牌，从根本上解决了这一问题。

设编辑指令文本为 $\mathbf{t}_{ins}$，源视频首帧为 $\mathbf{I}_{src}$，可选参考图像为 $\mathbf{I}_{ref}$，VLM Instructor 的输出定义为：

$$\mathbf{x}_{vlm} = \mathrm{VLM}(\mathbf{t}_{ins}, \mathbf{I}_{src}, \mathbf{I}_{ref}) \tag{1}$$

其中 $\mathbf{x}_{vlm}$ 取自 VLM 最后一层隐藏状态，是一组同时编码了语义意图、空间定位和视觉外观的令牌序列。当用户提供参考图像时，VLM Instructor 能够将参考图像中的目标实体外观与指令中的编辑意图对齐，从而支持基于参考的图像引导视频编辑——这一能力是现有开源方法所不具备的。

---

### 3.2 Token Refiner 与上下文感知视频令牌化

VLM 输出的条件令牌 $\mathbf{x}_{vlm}$ 与 DiT 的潜在空间存在模态差异。为解决这一问题，VIVA 引入一个可训练的 **Token Refiner**，将 VLM 令牌对齐到预训练 DiT 的潜在空间，增强模型对视觉条件的响应能力。

在视频编码侧，VIVA 采用**上下文感知视频令牌化**策略。将源视频的 VAE 潜在 $\mathbf{z}_{src}$ 与噪声潜在 $\mathbf{z}_{noise}$ 在通道维度拼接后，通过可学习投影 $\mathcal{P}$ 生成上下文感知的视频令牌：

$$\mathbf{x}_{video} = \mathcal{P}\big(\operatorname{Concat}(\mathbf{P}(\mathbf{z}_{src}), \mathbf{P}(\mathbf{z}_{noise}))^{c}\big) \tag{2}$$

这种通道拼接方式使 DiT 在去噪过程中能够显式访问源视频的运动模式和结构信息，从而在编辑目标区域的同时保持未编辑区域的时间一致性。

---

### 3.3 带掩码加权的 Rectified Flow 损失

在预训练阶段，VIVA 采用 **Rectified Flow Matching** 作为基础生成框架。为强化编辑区域的学习信号，作者在标准 Flow Matching 损失 $\mathcal{L}_{\mathrm{FM}}$ 中引入编辑掩膜 $M$ 进行空间加权：

$$\mathcal{L}_{\mathrm{mask}} = (\mathbf{1} + w_{m}M)\,\mathcal{L}_{\mathrm{FM}} \tag{3}$$

其中 $w_{m}$ 控制掩膜区域的额外权重。这一设计引入了有效的空间归纳偏置，使模型更专注于编辑区域的生成质量，同时加速收敛。消融实验证实，掩膜损失对编辑精度和收敛速度均有显著贡献（Table 2）。

---

### 3.4 Edit-GRPO：基于组合奖励的强化学习后训练

预训练阶段使用合成配对数据，模型在复杂、开放域指令上的泛化能力仍有限。为此，VIVA 提出 **Edit-GRPO** 后训练阶段，通过 Group Relative Policy Optimization（GRPO）直接优化编辑行为。该阶段仅训练 LoRA 参数以保证效率。

Edit-GRPO 的核心在于设计了三项互补的奖励函数，从不同维度评估编辑质量：

**指令遵循奖励** $\mathbf{R}_{\mathrm{IF}}$ 通过 CLIP 相似度衡量编辑视频是否真正执行了用户指令：

$$\mathbf{R}_{\mathrm{IF}} = C(\mathbf{V}_{edit}, \mathbf{t}_{edit}) - C(\mathbf{V}_{edit}, \mathbf{t}_{src}) \tag{4}$$

其中 $C(\cdot,\cdot)$ 表示 CLIP 相似度，$\mathbf{t}_{edit}$ 和 $\mathbf{t}_{src}$ 分别为编辑指令和源视频描述。该差分设计确保模型真正改变了目标内容，而非简单保留源视频。

**源视频保留奖励** $\mathbf{R}_{\mathrm{SP}}$ 约束未编辑区域不被破坏：

$$\mathbf{R}_{\mathrm{SP}} = C(\mathbf{V}_{src}, \mathbf{V}_{edit}) \tag{5}$$

**人类偏好奖励** $\mathbf{R}_{\mathrm{PS}}$ 使用 PickScore 模型评估编辑视频的整体质量和与指令的符合度：

$$\mathbf{R}_{\mathrm{PS}} = \mathrm{Pickscore}(\mathbf{V}_{edit}, \mathbf{t}_{edit}) \tag{6}$$

最终总奖励为三项的加权和：

$$\mathbf{R} = w_{IF}\mathbf{R}_{\mathrm{IF}} + w_{SP}\mathbf{R}_{\mathrm{SP}} + w_{PS}\mathbf{R}_{\mathrm{PS}} \tag{7}$$

在 Edit-GRPO 的每次迭代中，通过 Flow-SDE 引入随机性生成多样化的编辑样本，计算相对优势后通过 GRPO 损失更新 LoRA 参数。消融实验表明，Edit-GRPO 在指令遵循、源视频保留和视觉美观三个维度上均带来显著增益，定性结果也显示更少的伪影和更强的复杂编辑泛化能力（Table 2, Figure 10）。

### 补充图表

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/003_Figure_3.jpg]]
*Figure 3: Overall pipeline of Edit-GRPO. We inject stochasticity via Flow-SDE [39] to generate diverse samples, score them with our reward system, and compute a GRPO loss from the resulting relative advantages to update the model. For efficiency, we optimize a LoRA instead of full fine-tuning*

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/016_Figure_14.jpg]]
*Figure 14: VLM templates for the instruction-based video editing and reference-instruction-based video editing*




## 实验与关键发现

### 主实验结果与基准对比

VIVA 在 VIE-Bench 基准上进行了全面的定量评估。该基准涵盖添加 (Add)、替换 (Replace)、删除 (Remove)、混合编辑 (Hybrid Edit) 以及基于参考图像的编辑等任务。评估采用 VLM 评测器（Gemini-2.5-pro）进行自动评分，包含指令遵循、源视频保留和编辑质量等多个维度。

Table 1 的结果表明，VIVA 在所有开源方法中取得了最高的 VLM 评估平均分，显著优于 ICVE、Lucy-Edit-Dev、Ditto 和 InsV2V 等基线方法。在添加任务上，VIVA 达到 8.86 分，相比 ICVE 的 7.22 分提升了 +1.64；在替换任务上，VIVA 同样获得 8.86 分，领先 ICVE 的 7.02 分达 +1.84；在删除任务上，VIVA 取得 9.44 分，比 ICVE 的 7.04 分高出 +2.40，优势尤为突出。在基于参考图像的编辑任务上，由于开源方法均不支持此功能，VIVA 与商业模型 Runway Gen-4 Aleph 进行了对比，同样展现出竞争力。

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison results on the VIE-Bench [46] dataset. The best and second-best results of the open-sourced methods are highlighted in bold and underlined, respectively. As reference-based video editing is not yet supported by the open-source models, we provide our results against the commercial model Runway Gen-4 Aleph [53]*

值得注意的是，VLM 评测器的自动评分虽与人类判断具有相关性，但并非完全等价，这是定量结果解读时需要考虑的因素。

### 消融研究

Table 2 对 VIVA 各核心组件进行了系统的消融分析，验证了每个设计选择的必要性。

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/007_Table_2.jpg]]
*Table 2: Ablation study results on VIE-Bench. V: VLM instructor; M: masked loss; I: Mixing image data; E: Edit-GRPO. The last row for each task corresponds to our full method. The best and second-best results are highlighted in bold and underlined, respectively*

**VLM Instructor 的作用。** 引入 VLM instructor（Section 3.1）后，所有评估指标均大幅提升，证实了视觉根植的多模态指令表示对复杂编辑泛化的关键作用。仅使用文本编码器的基线无法有效理解空间定位和实体外观等细粒度编辑需求，而 VLM instructor 通过联合编码首帧和可选参考图像，提供了精确的视觉条件。

**掩码损失的作用。** 带掩码加权的 Rectified Flow 损失（Eq. 3）引入了有效的空间归纳偏置，显著增强了编辑区域内的响应精度，同时加速了训练收敛。消融结果显示，移除掩码损失会导致编辑区域的准确性下降。

**混合图像数据的作用。** 在训练中混合大规模图像编辑数据（将图像视为单帧视频）的策略，显著提升了编辑能力和视觉质量。这一发现的关键在于：图像编辑数据规模更大、编辑类别覆盖更广，有效弥补了视频编辑对类型覆盖的不足，使模型即使在简单合成视频数据上训练也能泛化到更复杂的编辑场景。

**Edit-GRPO 后训练的作用。** 应用 Edit-GRPO 后，模型在指令遵循、源视频保留和视觉美观三个维度上均获得全面增益。Figure 10 的定性对比显示，经过 Edit-GRPO 优化的结果具有更少的伪影和更强的泛化能力。值得注意的是，Edit-GRPO 阶段仅训练 LoRA 参数，而非全量微调，在保证性能提升的同时兼顾了训练效率。

### 用户研究

为了验证自动评测指标的有效性，研究团队邀请了14位专家进行1对1配对比较用户研究。Figure 5 的结果显示，在指令遵循、源视频保留和编辑质量三个维度上，专家均显著偏爱 VIVA 的生成结果。这一发现与 VLM 自动评测的结论一致，进一步增强了实验结果的可信度。

### 失败模式分析

Figure 9 展示了 VIVA 的典型失败案例，揭示了当前方法的局限性：

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/011_Figure_9.jpg]]
*Figure 9: Failure cases. (a) Global transformations such as changing weather sometimes cause over-editing. (a) Rapid motion might occasionally lead to blurry results, such as the woman’s hand. (c) Under-editing might be observed in removal tasks, where residual artifacts, such as cast shadows, remain*

1. **全局变换中的过度编辑。** 当编辑指令涉及全局变换（如天气或风格改变）时，模型有时会过度编辑，影响源视频中本应保留的内容区域。这表明模型在区分“需要编辑的区域”和“需要保留的区域”之间的全局边界时仍存在困难。

2. **快速运动导致的运动模糊。** 在包含快速运动的场景中，编辑结果偶尔会出现运动模糊，如人物手部的模糊。这反映了模型在处理大运动幅度时的时间一致性仍有不足。

3. **删除任务中的编辑不足。** 在某些删除任务中，模型未能完全移除目标对象，残留伪影（如阴影）仍然可见。这表明模型对物理一致性（如光照和阴影关系）的理解尚不完整。

### 实验公平性说明

需要指出的是，实验主要在合成简单编辑对和 VIE-Bench 基准上进行。虽然 VIVA 在这些受控场景下表现优异，但其对极端复杂或长视频的真实世界编辑的泛化性仍需进一步验证。此外，VLM 评测器本身可能存在系统性偏差，其评分与真实人类感知之间的差异在极端案例中可能被放大。

### 补充图表

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/012_Figure_10.jpg]]
*Figure 10: Ablation studies on Edit-GRPO. Before: without Edit-GRPO; After: with Edit-GRPO. The editing instruction is shown at the bottom*

![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative comparison of the reference-based video editing on the VIE-Bench [46]. The editing instruction is shown at the top and the reference image is shown on the left for each group of results*



![[assets/figures/papers/paper_list_l2197_https_arxiv_org_abs_2512_16906/figures/015_Figure.jpg]]
*Figure: Remove the watermark. Remove the watermark. Replace the water in the canal with flowing lava, and add a full head of black hair. Turn the asphalt road into a vibrant, rainbow-colored path*



## 定位与知识库关联

### 1. 任务定位与问题边界

VIVA 面向**基于指令的视频编辑**（instruction-based video editing）任务：给定源视频和一条自然语言编辑指令，生成符合指令且保留源视频未编辑区域内容的目标视频。该任务处于文本驱动视觉生成、视频编辑与多模态指令理解的交叉地带，其核心瓶颈在于：现有方法大多依赖合成配对数据（如简单的添加、删除、替换操作），训练得到的模型难以泛化到真实场景中复杂、开放域的编辑指令。

VIVA 通过两条关键路径突破这一瓶颈：
- **表示层面**：引入 VLM instructor 将文本指令、源视频首帧和可选参考图像联合编码为视觉根植的多模态条件表示，弥补纯文本编码器在空间定位和外观描述上的不足。
- **优化层面**：设计 Edit-GRPO 后训练阶段，通过基于相对奖励的强化学习直接优化指令遵循度、源内容保留和人类偏好，使模型即使在简单编辑数据上训练也能习得复杂编辑的泛化能力。

### 2. 与基线方法的关系

VIVA 在 VIE-Bench 基准上与以下开源方法进行了系统对比：

| 基线方法 | 方法特征 | 与 VIVA 的核心差异 |
|----------|----------|---------------------|
| **ICVE** | 指令视频编辑 | 仅使用文本编码器，无 VLM 视觉根植表示，无 RL 后训练 |
| **Lucy-Edit-Dev** | 指令视频编辑 | 同上，缺乏视觉条件编码和奖励优化机制 |
| **Ditto** | 指令视频编辑 | 同上 |
| **InsV2V** | 指令视频编辑 | 同上 |

此外，VIVA 还与商业闭源模型 **Runway Gen-4 Aleph** (Runway, 2025) 进行了定性对比。如图 1 所示，Runway 在参考图像编辑场景下存在过度编辑（同时移除手和香烟）和身份保真度不足（无法保留泰迪熊外观）的问题，而 VIVA 能够精确遵循指令并保持参考对象的身份一致性。

VIVA 相对于上述基线的方法论增量可归纳为四个关键设计槽位：

| 设计槽位 | 基线取值 | VIVA 取值 | 证据锚点 |
|----------|----------|-----------|----------|
| 指令编码器 | 纯文本编码器（如 T5） | VLM instructor（视觉+文本，编码首帧和参考图像） | Section 3.1 |
| 训练目标 | 标准 Flow Matching 损失 | 带掩码加权的 Flow Matching 损失 | Eq. 3 |
| 训练数据 | 仅视频编辑对 | 混合大规模图像编辑数据（视为单帧视频） | Section 3.2, 4.5 |
| 后训练策略 | 无 | Edit-GRPO（GRPO + 组合奖励，仅更新 LoRA） | Section 3.3 |

### 3. 方法谱系中的知识贡献

从更广的生成模型发展脉络来看，VIVA 的知识贡献体现在以下交叉领域：

**（1）扩散/流模型与多模态指令理解**

VIVA 继承了 Rectified Flow 框架，以 HunyuanVideo-T2V-13B 作为 DiT 骨干。其关键创新在于将 VLM 引入条件编码路径：不同于主流视频编辑方法将文本指令通过 CLIP/T5 编码为单一语义向量，VIVA 的 VLM instructor 直接处理首帧图像和文本，输出序列化的多模态令牌 $\mathbf{x}_{vlm} = \mathrm{VLM}(\mathbf{t}_{ins}, \mathbf{I}_{src}, \mathbf{I}_{ref})$。这种视觉根植表示使模型能够精确理解“编辑什么区域”和“编辑成什么样子”，尤其在需要空间定位的添加、替换任务上获得显著增益。

**（2）强化学习与生成模型的对齐**

Edit-GRPO 将 GRPO（Group Relative Policy Optimization）从 LLM 对齐领域迁移到视频编辑。其奖励设计包含三个维度：
- 指令遵循奖励 $\mathbf{R}_{\mathrm{IF}} = C(\mathbf{V}_{edit},\mathbf{t}_{edit}) - C(\mathbf{V}_{edit},\mathbf{t}_{src})$（Eq. 4）
- 源视频保留奖励 $\mathbf{R}_{\mathrm{SP}} = C(\mathbf{V}_{src},\mathbf{V}_{edit})$（Eq. 5）
- 人类偏好奖励 $\mathbf{R}_{\mathrm{PS}} = \mathrm{Pickscore}(\mathbf{V}_{edit},\mathbf{t}_{edit})$（Eq. 6）

三项奖励通过加权和 $\mathbf{R} = w_{IF}\mathbf{R}_{\mathrm{IF}} + w_{SP}\mathbf{R}_{\mathrm{SP}} + w_{PS}\mathbf{R}_{\mathrm{PS}}$（Eq. 7）组合，并通过 Flow-SDE 注入随机性以生成多样化样本用于相对优势计算。这种设计将编辑质量的多维目标显式化为可优化的奖励信号，是视频编辑领域 RL 后训练的早期探索之一。

**（3）数据效率与跨模态迁移**

VIVA 在训练中混合图像编辑数据（视为单帧视频），利用图像编辑数据规模更大、编辑类别覆盖更广的特点，显著提升了编辑能力和视觉质量。消融实验（Table 2）证实该策略对性能有独立贡献，表明跨模态数据迁移是缓解视频编辑对数据稀缺的有效手段。

### 4. 适用边界与局限

**已知局限**（来自论文 Figure 9 的失败案例分析）：

1. **全局变换过度编辑**：在天气改变、风格迁移等全局变换任务中，VIVA 有时会过度修改源视频内容，影响未编辑区域的保留。这源于全局编辑与局部保留之间的内在张力。
2. **快速运动模糊**：当源视频包含快速运动（如挥手）时，编辑结果可能出现运动模糊伪影。这表明 VIVA 的运动建模能力在高动态场景下仍有不足。
3. **删除任务编辑不足**：在对象删除任务中，有时残留伪影（如投射阴影）未能完全移除，反映出模型对物理一致性（如光照关系）的理解有限。

**适用边界推断**：

- VIVA 的设计假设编辑操作可通过首帧和文本指令充分描述，对于需要长时序推理的编辑（如“在人物转身后添加背包”）可能力有不逮。
- 模型在 VIE-Bench 基准上验证，该基准的视频长度和编辑复杂度有限；在长视频（数分钟）上的计算开销和时序一致性仍需进一步验证。
- 定量评测依赖 VLM 评测器（Gemini-2.5-pro）自动评分，虽与人类判断相关但非完全等价，存在评分偏差风险。

### 5. 开放问题

1. **泛化稳定性**：VIVA 在完全开放域、未见过的复杂组合指令上的泛化能力是否保持稳定？现有评测主要覆盖 VIE-Bench 定义的编辑类别，更极端的分布外测试尚缺。
2. **VLM 选择敏感性**：VLM instructor 的视觉根植能力是否对所有类型的 VLM 均有效？更换不同架构/规模的 VLM 对性能的影响尚未被系统研究。
3. **奖励设计最优性**：Edit-GRPO 的三项奖励权重是否为所有编辑类型的最优配置？是否存在更适合特定编辑类型（如风格迁移 vs. 对象删除）的奖励函数？
4. **数据多样性瓶颈**：现有的合成数据构建管线是否足以覆盖真实世界中所有可能的编辑操作？如何进一步提升数据多样性以支撑更强的泛化？
5. **实时性与长视频**：模型在长视频（如几分钟）上的推理延迟和时序一致性如何？是否能通过蒸馏或高效推理策略实现实时编辑？

> **注意**：上述开放问题中，部分（如 VLM 选择敏感性、奖励权重最优性）在论文中未被直接探讨，属于基于方法设计的合理推断，需后续工作验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/VIVA_VLM_Guided_Instruction_Based_Video_Editing_with_Reward_Optimization.pdf]]

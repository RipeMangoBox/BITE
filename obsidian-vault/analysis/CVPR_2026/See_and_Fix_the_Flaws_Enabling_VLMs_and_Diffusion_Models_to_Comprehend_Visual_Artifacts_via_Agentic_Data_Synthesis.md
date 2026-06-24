---
title: "See and Fix the Flaws: Enabling VLMs and Diffusion Models to Comprehend Visual Artifacts via Agentic Data Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/See_and_Fix_the_Flaws_Enabling_VLMs_and_Diffusion_Models_to_Comprehend_Visual_Artifacts_via_Agentic_Data_Synthesis.pdf
project_link: null
code_link: "https://huggingface.co/alimama-creative/FLUX.1-dev-Controlnet-Inpainting-Beta"
aliases:
- See_and_Fix_the_
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 自动化伪影注入与注解生成（ArtiAgent 框架），通过操作 DiT 注意力层的位置编码和值嵌入实现可控的、多样化的伪影合成。
primary_logic: 利用三层智能体（感知、合成、策划）的全自动流水线，无需人工干预即可大规模生成带有丰富注释（二值标签、边界框、局部与全局解释）的伪影图像，进而有效训练 VLM 完成伪影检测、定位和解释，并能作为奖励信号或纠正工具嵌入扩散生成流程，提升图像质量。
claims:
- ArtiAgent 是一个完全自动化的代理流水线，由感知、合成和策划三个代理组成，无需人工标注。
- 合成代理通过目标-参考补丁映射，在 DiT 自注意力层中替换位置嵌入和值嵌入，以实现结构伪影注入。
- 使用 ArtiAgent 生成的 100K 样本微调 Qwen2.5-VL-7B 后，在 ArtiBench 上的二分类准确率达到 0.627，远高于未微调的 0.501 及多个商用 VLM 基线。
- 仅用 1K 合成样本，在定位和解释任务上的表现即超越 GPT-5，且性能随数据量增长而持续提升。
---

# See and Fix the Flaws: Enabling VLMs and Diffusion Models to Comprehend Visual Artifacts via Agentic Data Synthesis

> [!tip] 核心洞察
> 利用三层智能体（感知、合成、策划）的全自动流水线，无需人工干预即可大规模生成带有丰富注释（二值标签、边界框、局部与全局解释）的伪影图像，进而有效训练 VLM 完成伪影检测、定位和解释，并能作为奖励信号或纠正工具嵌入扩散生成流程，提升图像质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 看见并修复缺陷：通过代理数据合成使视觉语言模型与扩散模型理解视觉伪影 |
| 英文题名 | See and Fix the Flaws: Enabling VLMs and Diffusion Models to Comprehend Visual Artifacts via Agentic Data Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20951) · [HuggingFace](https://huggingface.co/alimama-creative/FLUX.1-dev-Controlnet-Inpainting-Beta) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ArtiAgent |
| Dataset | ArtiBench |

> [!tip] 效果简介
> - ArtiBench 上，检测准确率 (Accuracy) 0.627 (Qwen2.5-VL-7B + ArtiAgent) vs 0.501 (Qwen2.5-VL-7B) (+0.126)；检测 F1 0.627 (Qwen2.5-VL-7B + ArtiAgent) vs 0.336 (Qwen2.5-VL-7B) (+0.291)；定位 mIoU 0.111 (Qwen2.5-VL-7B + ArtiAgent) vs 0.010 (Qwen2.5-VL-7B) (+0.101)。
> - ArtiBench (1K 训练数据) 上，解释 ROUGE / CSS 0.222 / 0.606 (ArtiAgent 1K) vs 0.156 / 0.521 (SynthScars 1K) (+0.066 / +0.085)。

## 概述

**核心问题：** 现代扩散模型（如 SD3.5、FLUX）在生成高视觉质量图像时仍频繁产生结构性伪影——肢体错位、物体融合、异常扭曲等。然而，现有视觉语言模型（VLM）对此类伪影的识别与解释能力极弱：未经微调的 Qwen2.5-VL-7B 在二分类检测任务上准确率仅 0.501，接近随机猜测。根本瓶颈在于，伪影理解数据高度依赖人工标注，成本高昂且难以覆盖扩散模型日益多样化的失败模式。

**方法定位：** 本文提出 **ArtiAgent**，一个完全自动化的代理驱动框架，无需任何人工干预即可大规模合成带有丰富注释的伪影图像。该框架由三个协同智能体构成——感知代理（层次化实体-子实体分解与定位）、合成代理（基于 DiT 注意力逆向注入的结构化伪影生成）、策划代理（质量过滤与文本解释生成）——通过操控扩散去噪过程中自注意力层的位置编码和值嵌入，实现可控、多样且符合物理常识的伪影注入。在方法谱系中，ArtiAgent 区别于依赖人工标注的 **PAL**、半监督的 **DiffDoctor** 以及统一检测-定位-解释的 **LEGION**，其核心创新在于将伪影数据生成从“人工标注”范式转变为“代理合成”范式。

**主要结果：** 使用 ArtiAgent 生成的 100K 样本微调 Qwen2.5-VL-7B 后，模型在 ArtiBench 基准上的二分类准确率达到 0.627（+12.6%），F1 从 0.336 跃升至 0.627（+29.1%），定位 mIoU 从 0.010 提升至 0.111，解释 CSS 从 0.263 提升至 0.643（+38.0%）。仅使用 1K 合成样本，模型在定位与解释任务上即超越 GPT-5，且性能随数据规模持续增长。此外，ArtiAgent 训练的 VLM 可作为奖励模型引导扩散采样生成无伪影图像，亦可指导修复模型精确纠正伪影区域。

## 背景与动机

### 扩散模型的视觉伪影危机

现代扩散模型（如 SD3.5-Large、FLUX-dev、Qwen-Image）已能生成像素级高度逼真的图像，但其输出中仍频繁出现违背物理常识的**结构性视觉伪影**。Table 1 统计了主流扩散模型的伪影出现频率：SD3.5-Large 高达 36%，FLUX-schnell 为 28%，即便表现最好的 Nano-Banana 也有 5% 的样本存在可辨识的结构缺陷。Figure 2 进一步揭示了伪影类型的分布——从肢体重复、物体融合到空间关系错乱，这些缺陷并非边缘案例，而是扩散模型内在生成机制的产物。

更关键的是，现有的视觉语言模型（VLM）对这些伪影几乎“视而不见”。Figure 1(a) 的示例表明，即便 GPT-4o、Gemini-2.5-Pro 等商用 VLM 也无法可靠地识别或解释扩散模型生成的伪影。这一能力缺口构成了严重的安全隐患：当生成图像被用于医疗、设计、新闻等场景时，未被察觉的结构性错误可能引发连锁后果。

### 现有伪影理解方法的瓶颈

伪影理解任务涵盖三个层次：**二值检测**（判断图像是否包含伪影）、**定位**（标定伪影区域）和**解释**（描述伪影的成因与表现）。现有方法的根本瓶颈在于**数据标注成本**：

- **人工标注昂贵且不可扩展**：传统伪影数据集（如 SynthScars）依赖人类标注员逐一标记伪影区域、类型和描述，成本高、速度慢，且难以覆盖现代扩散模型日益多样化的失败模式。
- **伪影类型覆盖不足**：现有基准数据集多基于早期生成模型构建，其伪影分布与 SD3.5、FLUX 等新一代 DiT 架构模型产生的结构性缺陷存在显著差异（Table 2 对比了各基准的生成来源与任务覆盖范围）。
- **商用 VLM 的零样本能力有限**：即便最先进的 GPT-5，在未经专门训练的情况下，对伪影的定位和解释能力也远低于实用需求。

### 本文动机与核心思路

上述困境催生了一个关键问题：**能否在不依赖人工标注的前提下，大规模生成带有丰富注释的伪影图像，从而有效训练 VLM 完成伪影理解？**

本文的答案是 **ArtiAgent**——一个由三个智能体（感知、合成、策划）协同工作的全自动代理流水线。其核心洞察在于：扩散模型去噪过程中的自注意力机制天然编码了图像的空间语义信息；通过精确操控 DiT 注意力层的位置编码和值嵌入，可以在任意干净图像上合成符合物理常识的结构性伪影，并自动生成边界框、局部解释和全局解释等完整注释。

这一思路将伪影理解从“依赖人工标注的被动收集”转变为“可控合成驱动的主动学习”，不仅大幅降低了数据获取成本，还使得 VLM 能够作为**奖励模型**或**纠正工具**嵌入扩散生成流程，从源头减少伪影的产生。

## 核心创新

### 从人工标注到全自动代理合成：ArtiAgent 框架

本工作的根本创新在于将视觉伪影理解的数据生产范式从**依赖人工标注**彻底转变为**全自动代理合成**。现有伪影数据集（如 SynthScars）需要人工标注者逐张勾画伪影区域并撰写描述，成本高昂且难以覆盖现代扩散模型输出的多样化结构性伪影。ArtiAgent 通过三个协同工作的智能体——**感知代理**（Perception Agent）、**合成代理**（Synthesis Agent）和**策划代理**（Curation Agent）——实现了从干净图像到带有丰富注释的伪影样本的端到端自动化流水线，全程无需人工干预（Figure 3）。

### 关键机制创新：DiT 注意力层的逆向注入

合成代理的核心技术突破在于**对扩散 Transformer（DiT）自注意力层的操控**。与传统的像素级图像编辑或生成对抗网络（GAN）注入不同，ArtiAgent 的逆向注入模块直接干预去噪过程中的空间语义编码：

- **位置嵌入注入（PE Injection）**：将目标补丁（target patch）的旋转位置编码（RoPE）替换为参考补丁（reference patch）的位置编码，使模型“误以为”去噪发生在参考位置，从而将参考区域的几何结构迁移到目标区域。
- **值嵌入注入（Value Injection）**：同步替换值嵌入，使目标位置填充参考区域的语义内容。

二者的组合效应是：PE 注入控制“在哪里”生成，值注入控制“生成什么”。这种解耦的操控方式使得合成代理能够生成符合物理常识的结构性伪影（如多余的肢体、扭曲的面部特征），而非随机的像素噪声。注入被严格限制在**早中期层**（如 FLUX 的单流块 20–38）且仅在**部分去噪步**（如 25 步中的前 15 步）中执行，以在注入伪影的同时保持背景一致性与图像自然度。

### 数据标注范式的根本转变

与基线方法的对比凸显了 ArtiAgent 在数据生产维度上的质变：

| 维度 | 基线方法（如 PAL、SynthScars） | ArtiAgent |
|------|-------------------------------|-----------|
| 伪影生成 | 依赖扩散模型自然输出或简单图像操作 | 四种工具（添加、删除、扭曲、融合）结合 DiT 注意力逆向注入 |
| 区域标注 | 人工标注边界框或分割掩码 | 感知代理通过 Grounded-SAM 自动定位实体与子实体，基于重叠率计算从属关系 |
| 文本解释 | 人工撰写或缺失 | 策划代理自动生成局部解释（描述伪影区域的具体异常）与全局解释（总结图像整体质量） |
| 质量过滤 | 人工筛选 | LPIPS 感知相似度阈值过滤（$\tau_1 \leq 1 - d_{\mathrm{LPIPS}}(x_{\mathrm{original}}, x_{\mathrm{artifact}}) \leq \tau_2$）结合 VLM 校验 |

这一转变的直接后果是：仅需 1K 个 ArtiAgent 合成样本微调 Qwen2.5-VL-7B，其在解释任务上的 CSS 得分（0.606）即显著超越同等数量的人工标注数据集 SynthScars（0.521），并在定位和解释任务上超越商用模型 **GPT-5**（Figure 6, Table 4）。这表明合成注释的质量不仅不逊于人工标注，在规模化扩展性上更是具有压倒性优势。

### 从理解到干预：VLM 作为扩散模型的质量控制器

ArtiAgent 的第二个关键创新在于将训练得到的伪影感知 VLM **嵌入扩散生成流程**，形成闭环质量控制：

- **奖励引导生成**：将微调后的 VLM 作为奖励模型，在测试时引导扩散采样过程，使生成图像逐步减少伪影。
- **迭代图像修复**：VLM 检测并定位伪影区域后，指导修复模型（如 FLUX 修复管线）进行定向纠正（Figure 8）。

这种“理解—反馈—修正”的闭环是此前工作（如 DiffDoctor 仅做分割、LEGION 仅做解释）所不具备的，将伪影理解从被动的诊断工具升级为主动的质量改进手段。

## 整体框架

ArtiAgent 是一个完全自动化的代理流水线，旨在无需人工干预的情况下，向干净的真实图像中注入多样化的结构性视觉伪影，并同步生成包含边界框、局部解释与全局解释的丰富注释。如图 1(b) 与图 3 所示，该框架由三个协同工作的智能体构成：**感知代理 (Perception Agent)**、**合成代理 (Synthesis Agent)** 与**策划代理 (Curation Agent)**，三者形成一条端到端的数据合成与标注链路。

### 流水线总览

整个流水线的输入是一张干净的真实图像，输出是一组高质量的伪影注入图像及其配套的多层次注释数据，可直接用于下游视觉语言模型（VLM）的微调训练。三个代理的职责与数据流如下：

1. **感知代理** 接收原始图像，利用即用型 VLM 将图像内容分解为层次化的实体-子实体词汇（如“狗-鼻子”），并通过 Grounded-SAM 进行定位与从属关系分析，输出可供后续扰动操作的目标候选区域。
2. **合成代理** 基于感知代理提供的定位信息，从其工具箱（四种操作：添加、删除、扭曲、融合）中选择合适的扰动策略，生成目标-参考补丁映射，并通过**逆向注入模块**在扩散模型（DiT）的去噪过程中操控自注意力层的位置编码与值嵌入，实现符合物理常识的结构化伪影合成。
3. **策划代理** 对合成结果进行质量过滤（基于 LPIPS 或 VLM 校验），并为通过筛选的样本自动生成局部与全局文本解释，最终产出训练就绪的数据集。

### 模块间关系与输入输出流

三个代理之间以串行方式衔接，但合成代理内部存在一个关键的逆向注入子模块，它直接操作扩散模型的注意力机制，是框架实现可控伪影合成的核心。

- **感知代理 → 合成代理**：传递实体与子实体的边界框坐标、类别标签及从属关系。合成代理据此决定“在哪里注入”以及“注入什么类型的伪影”。
- **合成代理内部**：工具箱负责生成目标补丁（待扰动区域）与参考补丁（提供语义内容的区域）之间的映射关系；逆向注入模块则利用这一映射，在扩散去噪的特定步骤（如前 15 步）和特定层（如 FLUX 的单流块 20–38）中，将目标补丁的位置嵌入和值嵌入替换为参考补丁的对应嵌入，从而在保持背景一致性的前提下，将参考区域的语义特征“移植”到目标区域，形成自然的伪影。
- **合成代理 → 策划代理**：传递原始图像与伪影注入图像的配对。策划代理首先计算两者之间的 LPIPS 距离，仅保留满足 $ \tau_1 \leq 1 - d_{\mathrm{LPIPS}}(x_{\mathrm{original}}, x_{\mathrm{artifact}}) \leq \tau_2 $ 的配对，以滤除伪影过弱或过强的样本；随后调用 VLM 生成针对伪影区域的局部解释与描述整体异常现象的全局解释。
- **策划代理 → 下游任务**：输出包含原始图像、伪影图像、二值标签、边界框、局部解释与全局解释的完整数据条目，直接用于 VLM 的检测、定位和解释任务训练。

### 关键设计决策

框架在设计上做出了若干关键选择以保障合成数据的质量与实用性：

- **基于真实图像的伪影注入**：与直接在扩散生成过程中引入噪声不同，ArtiAgent 以真实图像为基底，通过逆向注入机制合成伪影。同时，为消除扩散重建过程本身引入的分布偏移，流水线对源图像先执行逆向-重建操作，使原始图像与伪影图像共享相同的扩散生成特性。
- **可控的注意力操控**：逆向注入模块将 PE 注入与值注入限制在去噪过程的早中期层，并在最后若干去噪步中完全关闭注入，确保伪影只影响局部结构而不破坏整体图像的逼真度。消融实验表明，在总共 25 步去噪中注入前 15 步可获得最佳检测性能（Acc 0.586, F1 0.570）。
- **全自动注释生成**：与传统依赖人工标注的伪影数据集（如 PAL、SynthScars）相比，ArtiAgent 完全消除了人工标注的成本瓶颈，且生成的解释质量在 1K 数据规模下即显著优于同等数量的人工标注数据（CSS: 0.606 vs 0.521）。

### 数据规模与下游应用

利用该流水线，作者收集了 50K 对伪影注入图像及其原始图像，并附带完整的元数据注释。在此基础上微调 Qwen2.5-VL-7B 和 InternVL3.5-8B 等开源 VLM，可使其在 ArtiBench 基准的检测、定位和解释三项任务上全面超越 GPT-5 等商用模型。此外，训练后的 VLM 还可作为奖励模型嵌入扩散生成流程，引导文本到图像模型生成无伪影的高质量图像，或作为视觉反馈模块指导图像修复模型精准纠正伪影区域。

### 补充图表

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our challenges and approach. The red boxes indicate the regions with visual artifacts. (a) Examples of structural visual artifacts in state-of-the-art diffusion models and the inability of VLMs to recognize or explain them. (b) Overview of ArtiAgent, a novel agentic framework that synthesizes artifacts for arbitrary visual contexts without human intervention. (c) Example of VLMbased artifact comprehension via detection, explanation, and localization. (d) Application to reward-guided text-to-image generation. (e) Application to image correction, where artifact-aware VLM-guided inpainting removes the flawed regions*

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/004_Figure_3.jpg]]
*Figure 3: ArtiAgent consists of three coordinated agents: (1) the perception agent detects entities and subentities using Grounded-SAM; (2) the synthesis agent injects artifacts through patch mapping tool and the inversion-injection paradigm; and (3) the curation agent filters low-quality results and generates localized and global textual explanations*

## 核心模块与公式推导

### 感知代理：层次化实体分解与定位

感知代理是 ArtiAgent 流水线的入口模块，其核心任务是将输入图像转化为可供合成代理操作的符号化结构描述。该模块采用即用型视觉语言模型（VLM）对图像进行层次化分解，生成“实体—子实体”词汇树（如“狗”为实体，“鼻子”“耳朵”为子实体）。随后，通过 **Grounded-SAM** 对词汇中的实体与子实体进行像素级定位，并通过计算子实体掩码与实体掩码的重叠率（overlap ratio）来确定子实体与父实体的从属关系。这一层次化 grounding 为后续合成代理的目标-参考补丁映射提供了精确的空间语义锚点。

### 合成代理：工具箱与逆向注入模块

合成代理由两个子模块构成：**工具箱（Toolbox）** 与 **逆向注入模块（Inversion-Injection Module）**。

#### 工具箱：四种伪影操作

工具箱定义了四种目标-参考补丁映射工具，用于生成结构化的伪影注入方案：

- **添加（Addition）**：将参考补丁的内容复制到目标补丁位置。
- **删除（Deletion）**：移除目标补丁的内容。
- **扭曲（Distortion）**：对目标补丁施加几何或纹理扰动。
- **融合（Fusion）**：将参考补丁与目标补丁的内容进行混合。

每种工具基于感知代理提供的实体-子实体 grounding 结果，生成具体的目标补丁集合与参考补丁集合之间的映射关系。

#### 逆向注入模块：DiT 注意力层的空间语义操控

逆向注入模块是 ArtiAgent 实现可控伪影合成的核心机制。其基本原理是利用扩散模型去噪过程中自注意力对位置编码的依赖，通过替换目标补丁的位置嵌入（Positional Embedding, PE）和值嵌入（Value Embedding），在不破坏图像整体结构的前提下注入符合物理常识的伪影。

给定扩散 Transformer（DiT）第 $\ell$ 层的输入 $X^{(\ell)}$，自注意力的标准计算流程如下：

**线性投影**：将输入投影为查询（Query）、键（Key）、值（Value）三个矩阵：

$$Q^{(\ell)} = X^{(\ell)} W_Q^{(\ell)}, \quad K^{(\ell)} = X^{(\ell)} W_K^{(\ell)}, \quad V^{(\ell)} = X^{(\ell)} W_V^{(\ell)}$$

**旋转位置嵌入（RoPE）**：根据每个补丁的索引 $p$ 对查询和键施加位置编码：

$$\tilde{Q}_p^{(\ell)} = \mathrm{RoPE}(Q^{(\ell)}, p), \quad \tilde{K}_p^{(\ell)} = \mathrm{RoPE}(K^{(\ell)}, p)$$

**缩放点积注意力**：利用位置编码后的查询和键计算注意力权重，并聚合值嵌入：

$$\mathrm{Attn}^{(\ell)}(X^{(\ell)}) = \mathrm{Softmax}\left(\frac{\tilde{Q}^{(\ell)} \tilde{K}^{(\ell)\top}}{\sqrt{d}}\right) V^{(\ell)}$$

其中 $d$ 为键向量的维度。

**注入机制**：对于工具箱中确定的每一对目标补丁 $p_t$ 与参考补丁 $p_r$，逆向注入模块执行双重替换：

- **PE 注入**：将目标补丁的位置嵌入替换为参考补丁的位置嵌入，使模型“认为”去噪发生在参考补丁的位置。
- **值注入**：将目标补丁的值嵌入替换为参考补丁的值嵌入，使模型将参考补丁的语义内容填充到目标位置。

PE 注入控制去噪的“空间位置感知”，值注入提供“语义内容填充”，二者协同实现了局部伪影的自然合成。

**注入约束**：为保证伪影的自然度与背景一致性，注入操作被严格限制在以下范围内：

- **层次范围**：仅在 DiT 的早中期层执行注入（例如，在 FLUX 的单流块 20–38 层）。
- **时间步范围**：仅在去噪过程的前若干步执行注入，并在最后若干步关闭注入。消融实验表明，在总共 25 步去噪过程中，前 15 步注入可获得最佳检测性能（Acc 0.586, F1 0.570），过多或过少均导致性能下降。

### 策划代理：质量过滤与解释生成

策划代理负责对合成代理的输出进行质量把控与语义标注，其核心操作包括：

**感知质量过滤**：通过 LPIPS（Learned Perceptual Image Patch Similarity）度量原始图像 $x_{\mathrm{original}}$ 与伪影注入图像 $x_{\mathrm{artifact}}$ 之间的感知距离，仅保留满足以下条件的样本对：

$$\tau_1 \leq 1 - d_{\mathrm{LPIPS}}(x_{\mathrm{original}}, x_{\mathrm{artifact}}) \leq \tau_2$$

其中 $\tau_1$ 和 $\tau_2$ 分别为下界和上界阈值。该条件滤除了伪影过弱（难以察觉）或过强（破坏图像自然度）的样本。

**解释生成**：对通过过滤的样本，策划代理利用商用 VLM（如 GPT-4o）生成两类文本解释——局部解释（描述特定伪影区域的问题）和全局解释（概括整幅图像的伪影特征）。这些解释与二值标签、边界框共同构成下游 VLM 微调所需的完整注释。

### 补充图表

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/002_Figure_2.jpg]]
*Figure 2: Artifact type distribution of diffusion models*

## 实验与分析

### 实验设置

为系统评估 ArtiAgent 合成数据的有效性，作者构建了 **ArtiBench** 基准数据集，包含由五种前沿扩散模型（SD3.5-Large、FLUX-schnell、Qwen-Image、FLUX-dev、Nano-Banana）生成的 1K 张图像，覆盖添加、删除、扭曲、融合四类结构性伪影。与现有依赖人工标注或单一模型输出的伪影基准（如 SynthScars、MagicFix）不同，ArtiBench 的多源生成特性使其能更全面地反映现代扩散模型的真实失败模式（Table 2, Table 6）。

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/007_Table_2.jpg]]
*Table 2: Comparison of artifact benchmark datasets. If a benchmark reused another dataset as a source, we describe the generative models used in that source. The table with the full citations is provided in Appendix B.1*

微调实验以 **Qwen2.5-VL-7B** 和 **InternVL3.5-8B** 为骨干，在 ArtiAgent 生成的 100K 训练样本上进行全参数微调。评估覆盖三个递进任务：二分类检测（Accuracy/F1）、像素级定位（mIoU）、文本解释（ROUGE-L/CSS）。定位评估中，不同标注格式（边界框、分割掩码、热力图）被统一映射为二值掩码，并采用像素级 F1 以减轻边界框对过度预测的惩罚。

### 主要结果

**检测任务。** ArtiAgent 微调后的 VLM 在 ArtiBench 上显著超越所有基线。Qwen2.5-VL-7B + ArtiAgent 达到 0.627 准确率和 0.627 F1，较未微调版本分别提升 12.6 和 29.1 个百分点；InternVL3.5-8B 经微调后准确率从 0.498 提升至 0.630，相对提升 26.5%。值得注意的是，商用模型 GPT-5 的检测准确率仅为 0.534，低于 ArtiAgent 微调的开源 7B/8B 模型（Table 3a）。

**定位任务。** 伪影定位是更具挑战性的细粒度任务。Qwen2.5-VL-7B + ArtiAgent 的 mIoU 达到 0.111，而未经微调的模型几乎无法定位（mIoU = 0.010）。尽管绝对值仍较低——这反映了像素级伪影定位的固有难度——但相对提升超过 10 倍，且超越了依赖人工标注的专用方法 PAL 和 DiffDoctor（Table 3b）。

**解释任务。** 文本解释能力是 ArtiAgent 的核心优势之一。Qwen2.5-VL-7B + ArtiAgent 的 CSS 得分达到 0.643，较未微调基线（0.263）提升 0.380，且超越 GPT-5（0.589）和 Gemini-2.5-Pro（0.521）。这表明合成数据中附带的局部与全局解释有效赋予了 VLM 对伪影成因和语义的深层理解（Table 3c）。

### 数据缩放效应

Figure 6 展示了 ArtiAgent 合成数据量与 VLM 性能的缩放关系。关键发现：**仅 1K 合成样本，在定位和解释任务上的表现即超越 GPT-5**；随着数据量从 1K 增长至 100K，检测、定位、解释三项指标均呈现持续的单调提升，未出现饱和迹象。这验证了代理流水线的可扩展性——通过增加合成数据量可稳定提升伪影理解能力。

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/009_Figure_6.jpg]]
*Figure 6: Scaling effect of data generated by ArtiAgent with Qwen2.5-VL-7B. We average the results of all the benchmarks*

### 与人工标注数据的对比

在 1K 训练规模的公平对比中（Table 4），ArtiAgent 合成数据在解释任务上显著优于同等数量的人工标注数据集 SynthScars（CSS: 0.606 vs 0.521，ROUGE: 0.222 vs 0.156）。这一反直觉结果说明，代理生成的丰富结构化注释（边界框 + 局部解释 + 全局解释）在训练效率上可能超越传统的人工单一标注，且避免了人工标注的不一致性问题。

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/010_Table_4.jpg]]
*Table 4: ArtiBench result of the VLM trained on a 1K dataset*

### 消融实验

**注入步数。** Table 5 展示了在总共 25 步去噪过程中，伪影注入步数对检测性能的影响。性能在 **15 步注入时达到峰值**（Acc 0.586, F1 0.570），过多（25 步）或过少（5 步）均导致性能下降。过多的注入步数可能使伪影过于明显或不自然，削弱训练数据的真实性；过少则伪影强度不足，难以提供有效学习信号。

**注入层级与位置。** PE 注入和值注入被限制在 DiT 的早中层（如 FLUX 的单流块 20-38），并在最后去噪步中关闭（Figure 18）。消融表明，此配置在注入可控伪影的同时最大程度保持了背景一致性与图像自然度——若在深层或最后步骤继续注入，会破坏图像整体结构，导致训练数据失真。

### 下游应用验证

**奖励引导生成。** 将 ArtiAgent 训练的 VLM 作为奖励模型，嵌入扩散模型的测试时搜索框架（Figure 7），奖励值随搜索轮次稳步提升，生成的图像伪影显著减少。这证明合成数据训练的 VLM 不仅能“看见”伪影，还能作为有效的质量信号驱动生成过程。

**图像修复。** 在迭代修复循环中，ArtiAgent 微调的 VLM 识别伪影区域并生成修复提示，指导 FLUX-Controlnet-Inpainting 模型进行局部重绘（Figure 8）。修复后的图像在保持主体语义的前提下有效消除了结构性伪影，展示了伪影理解到伪影纠正的完整闭环。

### 注意力可视化

Figure 9 对比了 InternVL3.5-8B 微调前后的注意力热力图。基础模型对伪影区域几乎无响应，注意力分散于背景无关区域；微调后的模型则精确聚焦于真实伪影特征——无论这些伪影来自合成图像还是真实扩散模型输出。这从模型可解释性角度证实了 ArtiAgent 训练的有效性：VLM 真正学会了伪影的视觉特征，而非记忆训练分布的表层统计。

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/013_Figure_9.jpg]]
*Figure 9: Attention Visualization. We compare the attention maps of InternVL3.5-8B before (base) and after (fine-tuned) training on ArtiAgent. The fine-tuned model reliably focuses on genuine artifact features across both synthesized images and realworld images*

### 补充图表

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/003_Table_1.jpg]]
*Table 1: Artifact frequency of modern diffusion models*

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/014_Table_5.jpg]]
*Table 5: Ablation study on injection steps. Performance of Qwen2.5-VL-7B on ArtiBench binary detection when trained with 1K ArtiAgent samples generated using varying numbers of injection steps out of 25 total steps*

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/012_Figure_7.jpg]]
*Figure 7: As can be seen in Figure 7, the reward steadily improvesFigure 7. Reward-guided generation. ArtiAgent can train a rethroughout the search rounds, indicating that the diffusionward model that guides diffusion to generate artifact-free images*

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/011_Figure_8.jpg]]
*Figure 8: Image correction. The ArtiAgent-trained VLM can effectively guide image inpainting models to correct artifact regions*

![[assets/figures/papers/paper_list_l2591_https_arxiv_org_abs_2602_20951/figures/023_Figure_18.jpg]]
*Figure 18: Hyperparameter study on PE injection and value injection steps (1). The image in the red box shows our selected configuration*

## 方法谱系与知识库定位

### 1. 问题脉络：从人工标注到智能体合成

现有视觉伪影理解研究的核心瓶颈在于数据获取方式。传统方法如 **PAL** 和 **DiffDoctor** 依赖人工标注伪影区域与类型，成本高昂且难以覆盖现代扩散模型（如 FLUX、SD3.5）产生的多样化结构性伪影——包括肢体错位、物体融合、解剖结构异常等。**LEGION** 虽尝试统一检测、定位与解释任务，但其训练数据仍受限于人工标注的规模与多样性。

ArtiAgent 的根本性转变在于将数据生产模式从“人工标注”切换为“智能体合成”：通过感知、合成、策划三层代理的全自动流水线，在不依赖人工干预的条件下大规模生成带有多层次注释（二值标签、边界框、局部与全局解释）的伪影图像。这一范式转换直接回应了 Table 1 揭示的现实——现代扩散模型的伪影频率高达 36%（SD3.5-Large），而商用 VLM（如 GPT-4o、Gemini-2.5-Pro）对此几乎不具备可靠的检测与解释能力。

### 2. 方法坐标系：合成数据驱动的位置

ArtiAgent 在方法谱系中占据“合成数据驱动的伪影理解”这一交叉节点，其上下游关系如下：

**上游依赖：**
- **Grounded-SAM**：为感知代理提供实体与子实体的开放词汇定位能力，是层次化场景分解的基础工具。
- **DiT（Diffusion Transformer）架构**：合成代理的逆向注入模块深度依赖 DiT 的自注意力机制——通过替换目标补丁的位置嵌入（PE injection）和值嵌入（value injection），在去噪过程中操控空间语义，实现结构伪影的可控合成。该模块仅在早期至中层（如 FLUX 的单流块 20-38）和部分去噪步骤（如 25 步中的前 15 步）中执行注入，以平衡伪影自然度与背景一致性。
- **商用 VLM（GPT-4o 等）**：策划代理的解释生成与质量过滤环节依赖外部大模型，这既是当前流水线的关键支撑，也是其推理成本与潜在偏差的来源。

**下游应用：**
- **VLM 微调**：ArtiAgent 生成的 100K 样本可直接用于微调开源 VLM（Qwen2.5-VL-7B、InternVL3.5-8B），使其在检测、定位、解释三项任务上超越 GPT-5 等商用模型。
- **奖励引导生成**：微调后的 VLM 可作为奖励模型嵌入扩散采样流程，通过测试时搜索引导模型生成无伪影图像。
- **图像修复闭环**：伪影感知的 VLM 能够指导 inpainting 模型定位并修正伪影区域，形成检测-修复的自动闭环。

**与同期工作的关系：**
与 **SynthScars** 等人工标注数据集相比，ArtiAgent 合成的注释在等量数据（1K）下展现出显著更高的解释质量（CSS: 0.606 vs 0.521），证明合成注释并非“廉价替代品”，而是在多样性与描述粒度上具备独立优势。然而，ArtiAgent 目前聚焦于结构性伪影，未覆盖文本-图像对齐错误等语义层面的失败模式，这与扩散模型质量评估的更广泛谱系（如 TIFA、VQAScore）形成互补而非替代关系。

### 3. 适用边界与局限

**已验证的有效范围：**
- 结构性伪影（肢体异常、物体融合、解剖错误等）的合成与理解
- 基于 FLUX 架构的 DiT 注意力操控；对其他扩散架构（如 U-Net 基础模型）的迁移性需进一步验证
- 静态图像领域；论文未涉及视频或 3D 生成中的伪影合成

**已知局限：**
1. **伪影覆盖范围有限**：注入伪影的类型与分布由工具箱（添加、删除、扭曲、融合）和实体-子实体映射决定，可能无法穷尽真实扩散模型的所有失败模式。
2. **外部模型依赖**：流水线依赖 GPT-4o 等商用 VLM 进行解释生成与过滤，引入了外部模型的偏差、成本与可用性约束，限制了完全本地化部署的可能性。
3. **计算开销**：奖励引导生成与迭代修复需要额外的推理计算，论文未讨论在更大规模或在线环境下的部署可行性。
4. **评估基准的代表性**：ArtiBench 包含 1K 张由五个扩散模型生成的图像，其覆盖的模型范围与伪影多样性是否足以代表快速演进的生成模型生态，仍需持续更新验证。

### 4. 开放问题

1. **跨模态扩展**：ArtiAgent 的感知-合成-策划框架能否迁移至视频伪影（如时序不一致的肢体突变）或 3D 生成（如多视角几何冲突）的合成与理解？
2. **去外部依赖**：能否通过知识蒸馏或自训练策略，将商用 VLM 的解释能力压缩至本地模型，实现完全本地化的伪影理解与修正闭环？
3. **泛化边界**：在 ArtiAgent 合成数据上训练的 VLM 对 Midjourney、DALL·E 3 等商业生成软件真实输出的泛化能力，是否有进一步量化和提升的空间？
4. **伪影类型的完备性**：如何系统性地定义和覆盖扩散模型的结构性伪影类型谱系，使得合成数据驱动的训练能够逼近真实世界的伪影分布？

## 原文 PDF

![[paperPDFs/CVPR_2026/See_and_Fix_the_Flaws_Enabling_VLMs_and_Diffusion_Models_to_Comprehend_Visual_Artifacts_via_Agentic_Data_Synthesis.pdf]]
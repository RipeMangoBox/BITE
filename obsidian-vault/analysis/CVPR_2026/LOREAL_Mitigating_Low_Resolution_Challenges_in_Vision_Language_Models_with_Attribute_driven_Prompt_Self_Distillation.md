---
title: "LOREAL: Mitigating Low-Resolution Challenges in Vision-Language Models with Attribute-driven Prompt Self-Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LOREAL_Mitigating_Low_Resolution_Challenges_in_Vision_Language_Models_with_Attribute_driven_Prompt_Self_Distillation.pdf
project_link: "https://xuc865.github.io/loreal/index.html"
code_link: null
aliases:
- LOREAL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入由 LLM 生成的分辨率鲁棒属性语义，通过跨模态 meta-net 将其融入提示，并采用双学生自蒸馏框架（LLD 和 HLD）强制跨分辨率语义对齐，从而提升模型对低分辨率输入的适应能力。
primary_logic: 利用 LLM 的先验知识提取宏观、分辨率不变的属性（如物体轮廓、颜色），构建属性驱动的提示，并通过自蒸馏让不同分辨率视角下的模型互相学习属性语义和最终预测，使得模型在低分辨率下仍能捕获关键判别信息。
claims:
- LOREAL 在多个 SOTA 方法上显著缓解了低分辨率下的性能退化，如图 1 所示。
- 在 LR-B2N 基准上，当 φ=96² 时，LOREAL 为 MMA 带来 22.64% 的 HM 提升。
- 移除 LLD 或 HLD 均导致性能显著下降，证明两者对于跨分辨率语义对齐都是必要的。
- LOREAL 在 LR-CE 和 LR-DG 基准上也表现出一致的增益，特别是在低分辨率下。
---

# LOREAL: Mitigating Low-Resolution Challenges in Vision-Language Models with Attribute-driven Prompt Self-Distillation

> [!tip] 核心洞察
> 利用 LLM 的先验知识提取宏观、分辨率不变的属性（如物体轮廓、颜色），构建属性驱动的提示，并通过自蒸馏让不同分辨率视角下的模型互相学习属性语义和最终预测，使得模型在低分辨率下仍能捕获关键判别信息。

| 字段 | 内容 |
|------|------|
| 中文题名 | LOREAL：通过属性驱动的提示自蒸馏缓解视觉语言模型的低分辨率挑战 |
| 英文题名 | LOREAL: Mitigating Low-Resolution Challenges in Vision-Language Models with Attribute-driven Prompt Self-Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_LOREAL_Mitigating_Low-Resolution_Challenges_in_Vision-Language_Models_with_Attribute-driven_Prompt_CVPR_2026_paper.html) · [Project](https://xuc865.github.io/loreal/index.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LOREAL |
| Dataset | LR-B2N, LR-CE |

> [!tip] 效果简介
> - LR-B2N (φ=96²) 上，HM 63.14 (MMA+LOREAL) vs 40.50 (MMA) (+22.64%)；HM 57.25 (MaPLe+LOREAL) vs 34.85 (MaPLe) (+22.40%)；HM 61.71 (MMRL+LOREAL) vs 38.90 (MMRL) (+22.81%)。
> - LR-CE (φ=96², ImageNet) 上，Accuracy 37.65 (CoOp+LOREAL) vs 22.70 (CoOp) (+14.95%)。

## 概要

**问题瓶颈**：现有视觉语言模型（VLMs）的提示学习方法在低分辨率输入下性能退化严重。当部署于边缘设备时，降低分辨率虽能节省最高 62% 的推理内存和 64% 的推理速度（图 2），但会模糊判别性视觉特征、减少视觉令牌数量，而现有方法如 **CoOp**（Zhou et al., IJCV 2022）、**MaPLe**（Khattak et al., CVPR 2023）、**MMA**（Yang et al., CVPR 2024）、**MMRL**（Guo & Gu, arXiv 2025）均未针对此场景设计，缺乏鲁棒性。

**核心思路**：本文提出 **LOREAL**，一个属性驱动的提示自蒸馏框架。其核心洞察是：利用大语言模型（LLM）的先验知识提取分辨率不变的宏观属性（如物体轮廓、颜色），构建属性驱动的提示模板，并通过双学生自蒸馏让不同分辨率视角下的模型互相学习属性语义和最终预测，使模型在低分辨率下仍能捕获关键判别信息。

**方法定位**：LOREAL 在提示学习范式中引入了三个关键改变：（1）将固定提示模板替换为包含属性占位符和可学习属性内容的模板；（2）通过跨模态 meta-nets（LoRA 结构）将视觉特征动态映射为属性令牌，实现视觉-文本上下文化；（3）采用双学生自蒸馏训练范式，通过低层蒸馏（LLD，对比损失对齐属性语义）和高层蒸馏（HLD，KL 散度对齐预测分布）实现跨分辨率语义对齐。

**主要结果**：在 LR-B2N 基准上，当分辨率降至 φ=96² 时，LOREAL 为 MMA 带来 **+22.64%** 的调和平均数（HM）提升，为 MaPLe 和 MMRL 分别带来 **+22.40%** 和 **+22.81%** 的提升（表 1）。在 LR-CE 和 LR-DG 基准上也表现出一致的增益。消融实验证实 LLD 和 HLD 两者对于跨分辨率语义对齐都是必要的，其中 LLD 贡献更为显著。

### 低分辨率推理：边缘部署的必然选择与性能陷阱

视觉语言模型（VLMs）在图像分类、跨模态检索等任务上取得了显著进展，但其庞大的计算开销严重制约了在边缘设备上的部署。降低输入分辨率是一种直接且有效的加速手段——如图 2 所示，将分辨率从标准 $224^2$ 降至 $96^2$ 可节省最高 62% 的推理内存和 64% 的推理时间。然而，这种效率提升伴随着沉重的性能代价：低分辨率输入会模糊判别性视觉特征，同时大幅减少视觉令牌数量，导致模型难以捕获关键的细粒度信息。

### 现有提示学习方法的低分辨率盲区

为了高效适配下游任务，提示学习（Prompt Learning）已成为 VLM 微调的主流范式。代表性工作包括：

- **CoOp**（Zhou et al., IJCV 2022）：在文本编码器输入端引入可学习的连续提示令牌，替代手工设计的离散模板。
- **MaPLe**（Khattak et al., CVPR 2023）：将提示学习扩展到视觉和文本双模态，通过共享提示令牌实现跨模态知识耦合。
- **MMA**（Yang et al., CVPR 2024）：采用多模态适配器结构，在视觉和文本分支中插入轻量级可学习模块。
- **MMRL**（Guo & Gu, arXiv 2025）：通过多模态表示学习进一步挖掘视觉-文本对齐潜力。

然而，上述方法在设计时均假设标准分辨率输入，未考虑低分辨率场景下的鲁棒性需求。如图 1 所示，当输入分辨率降低时，四种 SOTA 方法在 11 个数据集上的调和平均数（HM）均出现大幅下滑——这一性能退化在极端低分辨率（$96^2$）下尤为严重。**核心瓶颈在于**：低分辨率模糊了判别性视觉特征，而现有提示学习方法缺乏对分辨率变化的结构性适应机制，其静态或仅基于类别嵌入的提示生成策略无法补偿视觉信息的损失。

### 蒸馏范式的启示与局限

知识蒸馏是提升小模型性能的经典手段，但将其应用于低分辨率 VLM 场景面临两个关键挑战：

1. **传统 KD 的师生架构不匹配**：经典知识蒸馏（Classic KD）和面向提示的 PromptKD 均依赖独立的教师模型提供监督信号，但低分辨率场景下并不存在一个天然适配的“高分辨率教师”——教师和学生输入分辨率一致，无法提供跨分辨率的知识迁移。
2. **提示空间的语义鸿沟**：直接在高维特征空间进行蒸馏容易引入噪声，而现有方法缺乏在语义层面（如物体属性）进行结构化对齐的机制。

上述分析揭示了本文的核心动机：**需要一种专门面向低分辨率场景的提示学习框架，能够在保持推理效率的同时，通过跨分辨率语义对齐来恢复低分辨率输入下的判别能力。**

## 核心方法与创新机理

LOREAL 的核心创新在于**首次将低分辨率鲁棒性引入视觉语言模型的提示学习范式**，通过三个紧密耦合的机制——LLM 驱动的属性语义挖掘、跨模态 meta-net 动态提示生成、以及双学生自蒸馏框架——系统性地解决了现有方法在低分辨率场景下性能崩溃的问题。

### 创新一：分辨率鲁棒的属性驱动提示模板

传统提示学习方法（如 **CoOp** (Zhou et al., IJCV 2022)）使用固定的上下文模板（如 `a photo of a [CLASS]`）或纯可学习令牌，这些提示在训练时针对标准分辨率优化，缺乏对低分辨率输入的结构性适应能力。LOREAL 从根本上改变了提示的设计方式：

- **属性占位符模板**：提示被重新构建为 `A photo of a [CLS] with S₁ [A₁] S₂ [A₂] ... S_K [A_K]`，其中 `[A_k]` 是 LLM 生成的、分辨率鲁棒的宏观属性（如物体轮廓、颜色、纹理），`S_k` 是由 meta-net 动态填充的可学习属性内容令牌。
- **LLM 思维链属性生成**：利用 GPT-4o 的思维链（Chain-of-Thought）推理能力，为每个类别生成 $K=5$ 个分辨率不变的描述性属性。这些属性捕捉的是物体的宏观语义特征（如“圆形轮廓”、“红色主体”），而非依赖高分辨率细节的微观纹理，因此在分辨率下降时仍具有判别力。

这一设计的关键洞察在于：**将提示从“静态文本模板”升级为“属性语义槽位 + 动态视觉填充”的混合结构**，使得文本提示能够根据输入图像的实际视觉特征自适应调整，而非一成不变地对待所有分辨率的输入。

### 创新二：跨模态 meta-net 实现视觉到文本的动态投射

传统方法中，文本提示的生成与视觉输入是解耦的——提示要么完全静态，要么仅通过类别嵌入进行简单映射。LOREAL 引入了**跨模态 meta-net**（基于 LoRA 结构的低秩投影），建立了视觉特征到属性提示令牌的直接映射通道：

$$S_k = M_k(\mathbf{f}_v) = W_{\uparrow,k}(W_{\downarrow,k}(\mathbf{f}_v))$$

其中 $W_{\downarrow,k} \in \mathbb{R}^{D_s \times D}$ 将视觉特征 $\mathbf{f}_v$ 压缩到低维瓶颈 $D_s=32$，$W_{\uparrow,k}$ 再将其投影回令牌维度。这一设计实现了两个层面的突破：

1. **视觉-文本上下文化**：每个属性令牌 $S_k$ 的内容直接来源于当前图像的视觉编码，使得提示“看到”了图像内容后再决定如何描述属性，而非预设固定描述。
2. **参数高效**：meta-net 仅引入极少的可训练参数（瓶颈维度 $D_s=32$），在保持模型主体冻结的前提下实现跨模态投射。

### 创新三：双学生自蒸馏框架实现跨分辨率语义对齐

这是 LOREAL 最核心的训练范式创新。与传统的知识蒸馏（Classic KD）或 PromptKD 不同，LOREAL 的**双学生自蒸馏**并非让学生向一个预训练的教师模型学习，而是让**两个共享参数的学生模型分别处理标准分辨率和低分辨率输入，通过互相学习来提升低分辨率下的表现**。

具体而言，框架包含两个互补的蒸馏损失：

- **低层蒸馏（Low-Level Distillation, LLD）**：通过对比损失对齐两个学生生成的属性提示内容 $S_k$，确保不同分辨率下模型对同一图像的属性语义理解一致。这是 LOREAL 最关键的组件——消融实验表明，移除 LLD 会导致性能显著下降，其贡献大于高层蒸馏。
- **高层蒸馏（High-Level Distillation, HLD）**：通过 KL 散度对齐两个学生的最终分类预测分布，促进输出层面的一致性。

训练时采用交叉生成策略：学生 α 的视觉特征用于为学生 β 生成文本提示，反之亦然（$\mathbf{f}_t^\beta = \mathcal{E}_t^\beta(\mathbf{p}(\mathbf{S}(\mathbf{f}_v^\alpha)))$）。这种设计强制模型学习分辨率无关的语义表示——无论输入分辨率如何，模型都能生成一致的属性描述和分类结果。

### 与现有方法的本质区别

| 维度 | 现有提示学习 | LOREAL |
|------|-------------|--------|
| 提示模板 | 固定上下文或纯可学习令牌 | 属性占位符 + 动态视觉填充 |
| 提示生成 | 静态或基于类别嵌入的简单映射 | 跨模态 meta-net 视觉→文本投射 |
| 训练范式 | 单分辨率标准监督训练 | 双学生自蒸馏，跨分辨率互学习 |
| 低分辨率鲁棒性 | 未考虑，性能大幅下降 | 核心设计目标，显著缓解退化 |

**证据强度**：上述三个创新均有明确的消融实验支撑。移除 LLD 或 HLD 均导致 HM 显著下降（Table 6）；meta-net 瓶颈维度 $D_s=32$ 和温度参数 $T=4$ 的最优配置通过网格搜索验证（Table 5）；属性数量 $K=5$ 和平衡系数 $\lambda_1, \lambda_2$ 的影响通过实验确定（Figure 5）。

LOREAL 的整体框架围绕一个核心矛盾展开：**低分辨率输入会模糊判别性视觉特征并减少视觉令牌数量，而现有提示学习方法对此缺乏鲁棒性**。为解决这一问题，LOREAL 构建了一个“属性驱动的提示自蒸馏”pipeline，其因果链条为：利用 LLM 的先验知识提取分辨率不变的宏观属性 → 通过跨模态 meta-net 将视觉特征动态注入属性提示 → 采用双学生自蒸馏框架强制跨分辨率语义对齐。

### 框架总览

如图 4 所示，LOREAL 包含三个紧密耦合的模块：

1. **LLM-based Attribute Generation**：利用 GPT-4o 的思维链（Chain-of-Thought）为每个类别生成 K 个分辨率鲁棒的宏观属性（如物体轮廓、颜色、纹理等），并构建包含属性占位符的提示模板：“A photo of a [CLS] with S₁ [A₁] S₂ [A₂] ... S_K [A_K]”，其中 S_k 为可学习的属性令牌内容，[A_k] 为 LLM 生成的属性语义占位符（Section 3.2）。

2. **Cross-modality Meta-Nets**：采用 LoRA 结构的轻量投影网络 M_k，将视觉编码器输出的视觉特征 f_v 映射为对应属性提示令牌 S_k = M_k(f_v) = W_{↑,k}(W_{↓,k}(f_v))，实现视觉到文本的跨模态投射。这些 meta-nets 是框架中**唯一可训练的参数**，在两个学生网络之间共享（Section 3.3, Eq. 5）。

3. **Dual-Student Self-Distillation Framework**：两个学生网络（结构相同、参数共享）分别接收标准分辨率（St.）和低分辨率（LR）输入。它们交叉生成提示：学生 α 的视觉特征 f_v^α 用于为学生 β 生成文本提示 p(S(f_v^α))，反之亦然。通过两个层次的蒸馏损失实现跨分辨率语义对齐（Section 3.4, Eq. 6）：
   - **Low-Level Distillation (LLD)**：对比损失，对齐两个学生生成的属性提示内容 S_k，确保不同分辨率下属性语义一致（Eq. 7）。
   - **High-Level Distillation (HLD)**：KL 散度损失，对齐两个学生的最终分类预测分布 ŷ，促进高层决策一致性（Eq. 8）。

### 输入输出流

- **训练阶段**：输入为同一图像的两个分辨率版本（标准分辨率与低分辨率），分别送入两个学生网络。两个学生共享 meta-nets，交叉生成属性提示并计算分类预测。总损失为 L = λ₁·L_LLD + λ₂·L_HLD，通过自蒸馏实现跨分辨率语义对齐。视觉编码器和文本编码器保持冻结。
- **推理阶段**：仅使用单个学生网络，输入低分辨率图像，meta-nets 根据视觉特征动态生成属性提示，完成分类预测。无需教师网络，推理成本与原始方法基本持平。

### 与现有蒸馏范式的区别

如图 3 所示，LOREAL 与 Classic KD 和 PromptKD 存在本质差异：前者需要全微调学生网络或依赖预训练教师，且均针对标准分辨率推理设计。LOREAL 则通过**双学生互学习**的自蒸馏机制，无需教师网络，专为低分辨率场景构建，通过属性级别的语义对齐来提升模型对低分辨率输入的鲁棒性。

![[assets/figures/papers/paper_list_l762_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_LOREAL_Mitigating/figures/004_Figure_4.jpg]]
*Figure 4: OurLOREALframework.(a):WeleveragetheLLMtogenerateseveralresolution-robustatributes.(b):Self-distllation framework.Weutilzethevisualembeddings toflltheprompatributesviameta-nets,thenleverageLow-LevelDistilltion(LDand High-LevelDtilltio(HLDforself-distllaion.Onlyemeta-etsareaable,andepramersof tollustratedmeatae sharedLRrepresentsLow-Resolution. (c): Inferencestage.Themodeltakes LRimagesandcontextualizes prompts withthe meta-nets*

LOREAL 的核心由三个模块构成：**LLM 驱动的属性生成**、**跨模态 Meta-Net 提示投射**，以及**双学生自蒸馏框架**。三者协同工作，使模型在低分辨率输入下仍能捕获判别性语义。

### 1. 分辨率鲁棒的属性生成

低分辨率导致判别性视觉特征模糊，但物体的宏观属性（如轮廓、颜色、纹理）对分辨率变化具有天然的鲁棒性。LOREAL 利用 LLM 的先验知识，通过显式思维链（Chain-of-Thought）为每个类别生成 $K$ 个分辨率鲁棒的属性描述。具体流程为：给定类别名称，LLM 首先推理该类别最具判别力的视觉特征，再从中筛选出对分辨率不敏感的属性，最终输出形如“round shape”、“red color”、“smooth texture”的属性短语。

随后，这些属性被填入上下文化提示模板中，构建可学习的属性提示：

$$p = \{\text{A photo of a [CLS] with } S_1 [A_1] S_2 [A_2] \cdots S_K [A_K]\}$$

其中 $[A_k]$ 是 LLM 生成的属性占位符，$S_k$ 是对应的可学习属性令牌内容，由后续的 meta-net 从视觉特征中动态生成。文中取 $K=5$ 作为经验最优值（见 Figure 5(b) 消融实验）。

### 2. 跨模态 Meta-Net 提示投射

传统提示学习方法中，文本提示是静态的或仅基于类别嵌入的简单映射，无法根据输入图像的具体内容自适应调整。LOREAL 引入跨模态 meta-net $M_k$，将视觉编码器输出的全局特征 $\mathbf{f}_v$ 投射为对应属性的提示令牌 $S_k$：

$$S_k = M_k(\mathbf{f}_v) = W_{\uparrow,k}\big(W_{\downarrow,k}(\mathbf{f}_v)\big)$$

其中 $W_{\downarrow,k} \in \mathbb{R}^{d \times D_s}$ 和 $W_{\uparrow,k} \in \mathbb{R}^{D_s \times d}$ 构成 LoRA 结构的低秩投影，$d$ 为视觉特征维度，$D_s$ 为中间瓶颈维度。消融实验表明 $D_s=32$ 时性能最优（Table 5 左）。

这一设计的核心作用在于：将视觉信号中的分辨率敏感信息压缩后，仅保留与属性语义相关的鲁棒成分，实现**视觉到文本的跨模态语义投射**。每个属性 $k$ 拥有独立的 meta-net $M_k$，使得模型能够学习到不同属性的差异化视觉线索。

### 3. 双学生自蒸馏框架

LOREAL 的训练范式摆脱了传统单分辨率监督学习的局限，采用双学生自蒸馏策略。两个学生网络共享视觉/文本编码器及 meta-net 参数，但分别输入标准分辨率图像 $\mathbf{x}^\alpha$ 和低分辨率图像 $\mathbf{x}^\beta$。低分辨率输入通过位置嵌入插值处理：

$$\mathcal{P} = \text{Cat}\big(\mathcal{P}[:1], \text{Intp}(\mathcal{P}[1:], \phi, \phi)\big)$$

其中 $\mathcal{P}$ 为视觉位置嵌入，$\phi$ 为目标分辨率尺寸。

两个学生交叉生成提示并进行跨分辨率知识蒸馏，包含两个层次的损失函数：

**低层蒸馏损失（LLD）**：对齐两个学生在属性提示层面的语义。学生 $\alpha$ 的视觉特征 $\mathbf{f}_v^\alpha$ 为学生 $\beta$ 生成文本提示，反之亦然：

$$\mathbf{f}_v^\alpha = \mathcal{E}_v^\alpha(\mathbf{x}); \quad \mathbf{f}_t^\beta = \mathcal{E}_t^\beta\big(p(S(\mathbf{f}_v^\alpha))\big)$$

LLD 通过对比损失强制同一属性在不同分辨率下的提示内容一致：

$$\mathcal{L}_{\text{LLD}} = -\sum_{k=1}^{K} \log \frac{\exp\big(\text{Sim}(S_k(\mathbf{f}_v^\alpha), S_k(\mathbf{f}_v^\beta)) / \tau\big)}{\sum_{k'}^{K} \exp\big(\text{Sim}(S_k(\mathbf{f}_v^\alpha), S_{k'}(\mathbf{f}_v^\beta)) / \tau\big)}$$

**高层蒸馏损失（HLD）**：对齐两个学生的最终预测分布，通过 KL 散度实现：

$$\mathcal{L}_{\text{HLD}} = \sum_{c=1}^{C} \big(\hat{y}_c^\alpha \log \hat{y}_c^\alpha - \hat{y}_c^\alpha \log \hat{y}_c^\beta\big)$$

其中 $\hat{y}_c = \frac{\exp(\text{Sim}(\mathbf{f}_v, \mathbf{f}_{t,c}) / \tau)}{\sum_{c'} \exp(\text{Sim}(\mathbf{f}_v, \mathbf{f}_{t,c'}) / \tau)}$ 为基于视觉-文本余弦相似度的分类预测。

总损失为 $\mathcal{L} = \mathcal{L}_{\text{CE}} + \lambda_1 \mathcal{L}_{\text{LLD}} + \lambda_2 \mathcal{L}_{\text{HLD}}$，其中 $\mathcal{L}_{\text{CE}}$ 为标准交叉熵分类损失。消融实验（Table 6）表明，移除 LLD 或 HLD 均导致性能显著下降，且 LLD 的贡献更为关键，验证了属性级语义对齐是跨分辨率鲁棒性的核心机制。

## 实验与关键发现

### 低分辨率基类到新类（LR-B2N）基准评估

为验证 LOREAL 对现有提示学习方法的通用增强能力，作者构建了 LR-B2N 基准，在三种分辨率设置（φ ∈ {96², 144², 192²}）下评估 11 个数据集的基类到新类泛化性能。核心结果汇总于 Table 1。

![[assets/figures/papers/paper_list_l762_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_LOREAL_Mitigating/figures/005_Table_1.jpg]]
*Table 1: Results on the LR-B2N Benchmark over three resolution settings*

**关键发现**：在最低分辨率 φ=96²（仅保留约 18.4% 的图像块令牌）时，LOREAL 为所有基线方法带来了一致且显著的提升：

- **MMA+LOREAL** 的调和平均数（HM）达到 63.14%，相较于 MMA 的 40.50%，提升幅度达 **+22.64%**。
- **MaPLe+LOREAL** 的 HM 为 57.25%，相较于 MaPLe 的 34.85%，提升 **+22.40%**。
- **MMRL+LOREAL** 的 HM 为 61.71%，相较于 MMRL 的 38.90%，提升 **+22.81%**。
- 即使对于单模态文本提示方法 **CoOp**（Zhou et al., IJCV 2022），LOREAL 也将其 HM 从 30.98% 提升至 50.70%（+19.72%）。

这一趋势在 φ=144² 和 φ=192² 下同样保持，且随着分辨率降低，LOREAL 的增益幅度增大，表明其专门针对低分辨率退化问题设计。多模态方法（MaPLe, MMA, MMRL）在结合 LOREAL 后平均 HM 提升 **+22.81%**（φ=96²），验证了属性驱动提示自蒸馏框架的跨架构通用性。

### 跨数据集评估（LR-CE）与领域泛化（LR-DG）

在 LR-CE 基准上（ImageNet 源域训练，10 个目标数据集低分辨率测试），LOREAL 同样展现了强大的迁移能力（Table 2）。以 φ=96² 为例，**CoOp+LOREAL** 的平均准确率达到 37.65%，而 CoOp 仅为 22.70%，提升 **+14.95%**。在 LR-DG 基准上（ImageNet 训练，四个变体数据集测试，Table 3），LOREAL 在所有分辨率下均带来一致的增益，验证了其对领域偏移与分辨率退化的联合鲁棒性。

![[assets/figures/papers/paper_list_l762_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_LOREAL_Mitigating/figures/006_Table_2.jpg]]
*Table 2: Results on the LR-CE Benchmark over three resolution settings*

![[assets/figures/papers/paper_list_l762_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_LOREAL_Mitigating/figures/007_Table_3.jpg]]
*Table 3: ResultsontheL-DGBenchmarkovethreresolutionsetings{96,144²,922}/ooourOREAL.nisteatioof patch tokens relative to the*

### 效率分析

Table 4 报告了 LOREAL 的计算开销。以 MaPLe 和 MMRL 为基线，添加 LOREAL 仅引入少量可训练参数（meta-nets 的 LoRA 结构），训练时间增加约 15-20%，而推理阶段由于 meta-nets 仅需一次前向传播，额外开销可忽略。结合 Figure 2 的推理效率分析（φ=96² 时可节省高达 62% 推理内存和 64% 推理时间），LOREAL 在边缘设备部署场景中具有实用价值。

### 消融实验

**模块贡献**（Table 6）：移除低层蒸馏（LLD）或高层蒸馏（HLD）均导致性能显著下降，其中 LLD 的贡献更大——这验证了属性级语义对齐是框架的核心驱动力。移除跨学生蒸馏路径（LR→St. 或 St.→LR）同样造成性能损失，证明双向知识流动的必要性。

**超参数敏感性**（Table 5, Figure 5）：
- Meta-nets 的中间维度 D_s=32 时性能最优，过大或过小均导致轻微退化。
- 对比损失温度 T=4 时达到最佳平衡。
- 平衡系数 λ₁（LLD 权重）和 λ₂（HLD 权重）在接近 1:1 时表现稳健。
- 属性提示长度 M=5 为经验最优值，过多属性引入冗余，过少则语义覆盖不足。

### 可视化分析

Figure 6 展示了 LOREAL 学习到的属性令牌语义和注意力热力图。在零样本 CLIP 设置下，结合 LOREAL 的模型在不同分辨率下均能将注意力集中于物体的判别性区域（如轮廓和纹理），而未使用 LOREAL 的模型在低分辨率下注意力分散或偏移。这直观解释了 LOREAL 如何通过属性语义引导模型关注分辨率鲁棒的视觉线索。

![[assets/figures/papers/paper_list_l762_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_LOREAL_Mitigating/figures/011_Figure_6.jpg]]
*Figure 6: Visualizations of the learned attribute tokens (Lower-Left),and attention heatmaps (Right) across varied resolution settings with or without our LOREAL on zero-shot CLIP.Note that here attention maps of different are resized for better illustration*

### 失败模式与局限

尽管 LOREAL 在多个基准上表现优异，但存在以下值得关注的方面：

1. **属性生成的依赖性**：LOREAL 依赖 GPT-4o 为每个类别生成 5 个分辨率鲁棒属性。在没有 LLM 访问的环境中，需要替代的属性获取方案，其性能影响尚未验证。
2. **属性数量 K 的经验性**：当前 K=5 为经验设定，缺乏自适应机制。不同数据集的最优 K 值可能存在差异，需手动调参。
3. **测试分辨率不匹配的泛化性**：文中仅在训练时使用的低分辨率（96², 144², 192²）上测试，当测试分辨率与训练低分辨率不匹配时，LOREAL 的泛化能力需要进一步验证。
4. **任务范围限制**：当前验证限于图像分类任务，LOREAL 在目标检测、分割等更复杂视觉语言任务上的适用性尚待探索。

![[assets/figures/papers/paper_list_l762_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_LOREAL_Mitigating/figures/009_Table_6.jpg]]
*Table 6: Ablation studies on proposed modules*

## 定位与知识库关联

### 1. 问题定位：低分辨率提示学习的空白地带

LOREAL 所瞄准的核心瓶颈在现有提示学习文献中几乎未被触及：**现有视觉语言模型（VLM）的提示学习方法在设计时均假设标准高分辨率（224²）输入，未考虑边缘设备部署中常见的低分辨率场景**。当输入分辨率降低时，判别性视觉特征被模糊化，同时视觉令牌数量急剧减少（例如从 224² 降至 96² 时，图像块令牌比例 η 仅为 18.4%），导致 CoOp、MaPLe、MMA、MMRL 等 SOTA 方法的调和平均数（HM）出现断崖式下跌（Figure 2c）。

这一问题的现实紧迫性在于：降低分辨率可带来高达 **62% 的推理内存节省和 64% 的推理时间加速**（Figure 2a,b），但若缺乏专门的鲁棒性设计，效率收益会被严重的性能退化所抵消。LOREAL 是首个系统性地将“分辨率鲁棒提示学习”作为一个独立问题提出并解决的工作。

### 2. 方法谱系：从静态提示到跨分辨率自蒸馏

LOREAL 的方法设计可从三个维度定位其在提示学习谱系中的位置：

**（1）提示模板的演化路径**

| 方法 | 提示结构 | 关键机制 | 分辨率感知 |
|------|---------|---------|-----------|
| **CoOp** (Zhou et al., IJCV 2022) | 纯可学习上下文令牌 | 文本端静态优化 | ✗ |
| **MaPLe** (Khattak et al., CVPR 2023) | 多模态提示耦合 | 视觉-文本分支交互 | ✗ |
| **MMA** (Yang et al., CVPR 2024) | 多模态适配器 | 视觉到文本的映射 | ✗ |
| **MMRL** (Guo and Gu, arXiv 2025) | 多模态表示学习 | 跨模态对齐 | ✗ |
| **LOREAL** (本文, CVPR 2026) | 属性占位符 + 可学习属性内容 | LLM 引导的属性驱动 + 跨分辨率自蒸馏 | ✓ |

LOREAL 的提示模板从固定的 `a photo of a [CLASS]` 进化为 `A photo of a [CLASS] with S₁ [A₁] S₂ [A₂] ...`，其中属性 `[Aₖ]` 由 LLM 通过思维链（CoT）生成，`Sₖ` 由跨模态 meta-net 从视觉特征动态填充。这一设计使提示内容具备了**视觉上下文感知能力和分辨率不变属性引导**，是提示模板从“静态文本”到“动态语义锚定”的关键跃迁。

**（2）知识蒸馏范式的对比**

Figure 3 清晰展示了 LOREAL 与 Classic KD 和 PromptKD 的本质差异：

- **Classic KD**：教师-学生架构，学生全量微调，教师为预训练大模型，蒸馏目标为输出 logits 对齐，设计目标为模型压缩，不涉及分辨率变化。
- **PromptKD**：引入提示作为知识传递媒介，但仍维持教师-学生单向知识流，且训练和推理均在标准分辨率下进行。
- **LOREAL**：创新性地采用**双学生自蒸馏**——两个学生是同一模型的副本，分别输入标准分辨率和低分辨率图像，通过共享的 meta-nets 实现双向知识交换。这打破了传统 KD 的师生层级结构，使两个视角下的模型互为师生，共同学习分辨率鲁棒表示。

**（3）蒸馏损失的双层设计**

LOREAL 的蒸馏并非单一维度的对齐，而是构建了**低层属性语义对齐（LLD）和高层预测分布对齐（HLD）**的双层蒸馏体系：

- **LLD**（低层蒸馏）：通过对比损失对齐两个学生生成的属性提示令牌 `Sₖ(fᵅᵥ)` 和 `Sₖ(fᵝᵥ)`，强制模型在不同分辨率下提取一致的属性语义。消融实验表明，移除 LLD 导致 HM 显著下降（Table 6），验证了属性级别对齐的核心作用。
- **HLD**（高层蒸馏）：通过 KL 散度对齐两个学生的输出预测分布，促进最终分类决策的跨分辨率一致性。消融显示 HLD 的贡献虽小于 LLD，但两者联合使用才能达到最优性能。

### 3. 知识库定位：LLM 先验与视觉提示的交叉点

LOREAL 在知识库中的独特定位在于**将 LLM 的先验知识作为分辨率鲁棒性的外部锚点引入视觉提示学习**。具体而言：

- **LLM 属性生成**：利用 GPT-4o 为每个类别生成 K=5 个宏观属性（如物体轮廓、颜色、纹理），这些属性天然具有分辨率不变性——无论图像分辨率如何降低，物体的“形状”“颜色”等高层语义描述仍然成立。
- **跨模态 meta-net**：通过 LoRA 结构的投影 `Sₖ = W_{↑,k}(W_{↓,k}(fᵥ))` 将视觉特征映射为属性令牌，实现了从视觉信号到语言属性空间的桥接。这一设计使提示内容不再是固定文本，而是**视觉输入的函数**。
- **自蒸馏框架**：将 LLM 提供的属性语义作为对齐目标，通过 LLD 和 HLD 使模型在不同分辨率下均能稳定地捕获这些鲁棒属性。

这种“LLM 先验 → 属性锚点 → 跨模态投射 → 自蒸馏对齐”的链条，使 LOREAL 同时触及了**提示学习、知识蒸馏、多模态对齐和 LLM 辅助视觉理解**四个研究方向的交叉地带。

### 4. 适用边界与局限

**适用边界**：

- LOREAL 被验证可**即插即用**地集成到 CoOp、MaPLe、MMA、MMRL 等多种提示学习方法上，在 LR-B2N、LR-CE、LR-DG 三个基准上均表现出一致的增益。
- 方法设计上不依赖特定视觉编码器架构，论文基于 CLIP-ViT-B/16 验证，理论上可扩展到其他 VLM 主干网络。
- 训练参数仅涉及 meta-nets（LoRA 结构），参数量极小（Table 4），保持了提示学习的高效性。

**局限与开放问题**：

1. **属性数量的经验性**：K=5 是经验设定，论文未提供自动确定最优属性数量的机制。当测试场景与训练类别差异较大时，固定的属性数量可能不适用。

2. **LLM 依赖性**：属性生成依赖 GPT-4o，对于无法访问 LLM 的部署环境，需要替代方案。论文未讨论基于规则或视觉特征聚类的属性生成替代路径。

3. **分辨率泛化边界**：论文在 φ ∈ {96², 144², 192²} 三个离散分辨率上训练和评估，当测试分辨率与训练时使用的低分辨率不匹配时（如 φ=80² 或更极端的 48²），LOREAL 的泛化能力尚未验证。

4. **任务范围限制**：当前验证集中于图像分类任务（基类到新类泛化、跨数据集评估、领域泛化），LOREAL 是否适用于更复杂的视觉语言任务（如目标检测、视觉问答、图像分割）仍是开放问题。

5. **模态扩展性**：自蒸馏框架的双学生设计是否可扩展到视频（时序分辨率变化）、音频（采样率变化）等其他模态的低质量输入场景，有待探索。

6. **训练效率权衡**：虽然推理阶段无额外开销（仅需单次前向传播，Figure 4c），但训练阶段需要两次前向传播（两个学生）和额外的蒸馏损失计算，训练时间有所增加（Table 4 中 Tra. time 数据显示了这一点）。

## 原文 PDF

![[paperPDFs/CVPR_2026/LOREAL_Mitigating_Low_Resolution_Challenges_in_Vision_Language_Models_with_Attribute_driven_Prompt_Self_Distillation.pdf]]

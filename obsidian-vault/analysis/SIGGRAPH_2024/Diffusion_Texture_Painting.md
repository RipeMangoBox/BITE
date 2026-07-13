---
title: "Diffusion Texture Painting"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Diffusion_Texture_Painting.pdf
code_link: https://github.com/nv-tlabs/DiffusionTexturePainting
project_link: https://research.nvidia.com/labs/toronto-ai/DiffusionTexturePainting/
aliases:
- DTP
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "对扩散模型推理过程的引导策略，通过引入基于源纹理的附加上下文（纹理引导 Texture Guidance）并在条件化阶段采用多尺度图像编码器（LoRA 微调），可以在保持生成多样性的同时显著抑制纹理漂移。"
primary_logic: "将在局部渲染空间运行的修复（inpainting）扩散模型作为图章生成器，并利用来自源纹理的伪造上下文构造纹理引导项，能够在不牺牲生成变化性的前提下强制每个图章与源纹理一致，从而实现实时、无缝且多样化的交互式绘画。"
claims:
- "直接使用条件修复扩散模型作为画笔会在几个图章后发生严重的纹理漂移，即使配合提示词反转也无法避免。"
- "采用多尺度图像编码器及 LoRA 微调的图像条件化可以减轻漂移，但仍未能完全消除。"
- "引入纹理引导（Texture Guidance, τ>0）能够在保持多样性（FID 改善）的同时大幅提升纹理一致性（SWD 改善），并几乎消除漂移。"
- "在开放的 Pexels 纹理数据集上，我们的方法（τ=1）在 FID 和 SWD 指标上均显著优于 TextureMixer、TextureAE 等基线。"
---

# Diffusion Texture Painting

> [!tip] 核心洞察
> 将在局部渲染空间运行的修复（inpainting）扩散模型作为图章生成器，并利用来自源纹理的伪造上下文构造纹理引导项，能够在不牺牲生成变化性的前提下强制每个图章与源纹理一致，从而实现实时、无缝且多样化的交互式绘画。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散纹理绘画 |
| 英文题名 | Diffusion Texture Painting |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://dl.acm.org/doi/pdf/10.1145/3641519.3657458) · [GitHub](https://github.com/nv-tlabs/DiffusionTexturePainting) · [Project](https://research.nvidia.com/labs/toronto-ai/DiffusionTexturePainting/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Diffusion Texture Painting |
| Dataset | Pexels textures (100 diverse real-world photos), Pexels textures |

> [!tip] 效果简介
> - Pexels textures (100 diverse real-world photos) 上，FID (↓) 为 1.18 ± 0.921 (Ours τ=1)，对比 4.02 ± 3.81 (TextureMixer)，变化 ↑2.84 (absolute improvement)。
> - Pexels textures 上，SWD (↓) 为 0.311 ± 0.238 (Ours τ=1)，对比 0.472 ± 0.431 (TextureMixer)，变化 ↑0.161 (absolute improvement)。

## 概要

将任意图像转化为可交互的纹理画笔，是计算机图形学中长期存在的挑战。现有方法要么依赖确定性克隆（如 Photoshop 图章工具），要么受限于闭域训练的纹理合成网络，难以在保持纹理身份一致性的同时，生成丰富多样的非重复纹理变化。**Diffusion Texture Painting** 提出了一种基于预训练扩散模型的图章式绘画框架，核心突破在于解决了扩散模型在连续交互绘画中的**纹理漂移（identity drift）**问题：当直接使用条件修复扩散模型作为画笔时，随着重叠图章的延伸，生成结果会在几个图章后迅速偏离源纹理特征。

该方法的关键洞察是：将在局部渲染空间运行的修复扩散模型作为随机图章生成器，并通过引入**纹理引导（Texture Guidance, TG）**——一种利用源纹理构造伪造上下文的去噪引导策略——在保持生成多样性的同时强制每个图章与源纹理一致。配合多尺度图像编码器与 LoRA 微调的条件化机制，该框架实现了实时、无缝且多样化的交互式纹理绘画，支持 2D 画布和 3D 网格表面。

在包含 100 张多样化真实纹理的 Pexels 数据集上，该方法（τ=1）取得了 FID 1.18、SWD 0.311 的结果，显著优于 TextureMixer（FID 4.02, SWD 0.472）等基线方法。消融实验证实，纹理引导是抑制漂移、同时提升纹理一致性与图章多样性的决定性因素。

### 问题背景：从纹理合成到交互式纹理绘画

高质量纹理是三维内容创作中不可或缺的视觉要素，但其制作过程长期依赖专业艺术家手工绘制或从照片中提取，耗时且对技能要求极高。传统的纹理合成方法——无论是基于块匹配的经典算法（如 **PatchMatch**，Barnes et al., ACM TOG 2010），还是基于深度学习的生成模型（如 **TextureMixer**，Yu et al., CVPR 2019；**TextureAE**）——通常以离线方式生成完整纹理图像，缺乏对交互式绘画场景的直接支持。在实际工作流中，艺术家更希望在三维网格表面以“画笔”的形式直接绘制纹理，而非等待一个全局合成的结果。

现有的交互式纹理绘画工具主要采用基于图章（stamp-based）的范式：将预设的纹理贴片作为画笔图章，沿笔触方向重复叠加，形成连续的纹理覆盖。然而，这些工具的图章来源存在根本性限制。以 Adobe Photoshop 为代表的商业工具提供的是确定性克隆画笔，只能机械地复制源纹理的固定区域，无法产生自然的变化。以 **NeuBE brushes**（Shugrina et al., 2022）为代表的学术方法虽然引入了神经生成能力，但其画笔仍局限于封闭域内训练的特定纹理类型，无法处理开放世界中任意复杂的纹理图像。

### 现有方法的核心缺口：扩散模型的纹理漂移问题

预训练扩散模型（Diffusion Model, DM）在图像生成领域展现了强大的开放域生成能力，理论上可以作为理想的纹理画笔生成器：给定任意一张源纹理图像，扩散模型应当能够在其条件化下，幻觉出无限多样且与源纹理一致的图章。然而，直接使用条件修复扩散模型（conditional inpainting DM）作为画笔生成器会遭遇一个关键瓶颈——**纹理身份漂移（texture identity drift）**。

如 Figure 4 所示，当使用标准的条件修复扩散模型沿笔触连续生成重叠图章时，仅经过几个图章，生成结果的纹理特征便开始与源纹理发生显著偏离。这种漂移现象即使配合提示词反转（prompt inversion）技术也无法避免。漂移的根本原因在于：扩散模型在每次去噪过程中天然倾向于产生多样性，而连续的修复操作缺乏强制性的全局纹理一致性约束，导致生成结果逐渐偏离原始纹理的身份特征。

### 本文动机：在多样性与一致性之间建立可控平衡

上述观察揭示了扩散纹理绘画的核心矛盾：**生成多样性**（避免机械重复，使纹理看起来自然）与**纹理一致性**（保持与源纹理的身份对齐）之间的张力。现有的条件化策略——包括引入多尺度图像编码器并通过 LoRA 微调——虽然能够在一定程度上减轻漂移（Figure 4d），但仍无法从根本上消除这一问题。

本文的核心动机在于：在预训练扩散模型的推理阶段引入额外的引导机制，以极低的计算代价强制每个生成图章与源纹理保持身份一致，同时不压制扩散模型本身的生成变化能力。这一思路将纹理绘画问题重新表述为**受控的去噪引导问题**：通过构造来自源纹理的伪造上下文作为引导信号，在标准分类器自由引导（CFG）的基础上叠加纹理引导项，从而在多样性与一致性之间建立可调的控制旋钮。

## 核心方法与创新机理

本文的核心创新在于将**预训练扩散模型改造为一种随机纹理画笔生成器**，并针对其直接应用于交互式绘画时暴露的致命缺陷——**纹理身份漂移（identity drift）**——提出了一套完整的“条件化 + 引导”解决方案。相比于传统的确定性克隆画笔或基于示例的块合成方法，本工作在三个关键维度上实现了根本性的改变。

### 1. 画笔生成器的范式转换：从确定性克隆到随机条件修复

传统数字绘画中的纹理画笔，无论是 Adobe Photoshop 的克隆印章，还是基于块匹配的 **PatchMatch**（Barnes et al., ACM TOG 2010），本质上都是**确定性**地从源纹理中复制或重组像素块。这种机制虽然保证了纹理一致性，却丧失了生成多样性——绘制的纹理只能是源纹理的机械重复，无法产生自然的变化。

本工作将画笔生成器重新定义为**随机条件修复扩散模型（stochastic inpainting DM）**。给定带有空洞（待填充区域）的局部画布图像 $I$ 和纹理条件 $b$，生成器 $G(I, b)$ 输出一个与周围已绘制内容无缝融合的新图章。这一转换带来了两个根本性优势：
- **多样性**：扩散模型的随机采样特性使得每次生成的图章都是源纹理的合理变体，而非简单复制；
- **无缝融合**：修复机制天然保证新生成内容与画布已有内容的边界连续性。

然而，这一范式转换也引入了新的瓶颈：预训练扩散模型在连续重叠图章的生成过程中，会迅速偏离源纹理的身份特征——这正是本文后续创新的直接动因。

### 2. 纹理条件化：多尺度图像编码器与 LoRA 微调

标准条件修复扩散模型通常依赖**文本提示词**作为条件信号，这在纹理绘画场景中面临两个问题：文本无法精确描述纹理的细粒度视觉特征；即使配合提示词反转（prompt inversion），仍无法阻止纹理漂移（Figure 4c）。

本工作将条件化方式从文本替换为**图像条件**，具体包含两个协同设计：
- **多尺度图像编码器**：将源纹理图像 $S$ 分割为不同尺度的图块，分别提取 CLIP 嵌入，再通过 Transformer 融合为统一的条件向量。这一设计使模型能够同时捕获纹理的局部细节（如单个石子的形状）和全局结构（如石路的排列规律）。
- **LoRA 微调**：通过低秩适配器（LoRA）对预训练 Stable Diffusion Inpainting 模型进行高效微调，注入可训练的低秩分解权重矩阵，使其学会将图像条件向量映射到去噪过程。相比全量微调，LoRA 大幅降低了训练成本，同时保持了基础模型的生成能力。

消融实验（Figure 4d）表明，仅靠更强的图像条件化**可以减轻漂移，但无法彻底消除**——这揭示了单纯改进条件信号本身的局限性，也为下一项创新提供了动机。

### 3. 去噪引导机制：纹理引导（Texture Guidance）

这是本文最具原创性的技术贡献。作者观察到，即使有了强图像条件化，扩散模型在去噪过程中仍然可能偏离源纹理的统计分布。为此，他们在标准分类器自由引导（CFG）的基础上，引入了一个额外的**纹理引导项（Texture Guidance, TG）**。

纹理引导的核心思想是：在去噪的每一步，除了使用当前画布上下文 $I$ 进行条件预测外，还构造一个**伪造的纹理上下文 $\hat{I}$**——该上下文完全由源纹理 $S$ 的像素填充（而非真实画布内容）——并计算两个条件预测之间的差异，以此作为额外的引导信号：

$$\hat{\epsilon}_\theta(x_t, t, b, \hat{I}) = \tilde{\epsilon}_\theta(x_t, t, b, I) + \tau \cdot (\epsilon_\theta(x_t, t, b, \hat{I}) - \epsilon_\theta(x_t, t, b, I))$$

其中 $\tau \in [0, 1]$ 控制纹理引导的强度。当 $\tau = 0$ 时，退化为标准 CFG；当 $\tau = 1$ 时，纹理引导最强。作者强调 $\tau \leq 1$ 的设计是有意为之——过强的引导会压制扩散模型的随机性，导致生成内容退化为源纹理的简单复制，丧失多样性。

定量消融实验（Table 1）证实了这一设计的有效性：$\tau = 1$ 相比 $\tau = 0$ 在 FID（多样性指标）和 SWD（纹理一致性指标）上均有显著改善，证明纹理引导能够在**不牺牲多样性的前提下强制纹理身份一致性**。

### 4. 绘画空间的扩展：从 2D 画布到 3D 网格表面

传统纹理绘画方法通常直接在 2D 画布或 UV 贴图上操作。本工作将绘画空间扩展到 **3D 网格表面**，通过在每次笔触位置构造局部切空间相机，将 3D 绘画问题转化为局部 2D 修复问题：渲染当前 UV 纹理在该视角下的图像，送入扩散模型生成新图章，再将结果反向投影回 UV 贴图。这一设计使得艺术家可以直接在 3D 模型表面进行直观的纹理绘画，而无需手动处理 UV 展开的接缝问题。

### 创新总结

上述四个创新构成了一个完整的因果链条：**随机修复生成器**提供了多样性的基础，但引入了漂移问题；**多尺度图像条件化**部分缓解了漂移，但力有不逮；**纹理引导**作为关键补丁，在去噪过程中强制施加源纹理约束，最终实现了“多样性”与“一致性”的兼得；**3D 绘画空间**则将这一能力从平面扩展到了立体表面。这一链条中的每一环都是对前一环暴露问题的直接回应，形成了逻辑严密的创新体系。

Diffusion Texture Painting 将交互式纹理绘画建模为一个**基于图章（stamp）的连续生成过程**，其核心思想是将一个经过适配的预训练扩散模型作为“画笔生成器”，在局部渲染空间中进行条件修复（inpainting），再将生成结果投影回全局纹理图像或 UV 贴图。整个 pipeline 由三个紧密耦合的模块构成，形成“渲染—生成—合成”的闭环。

### 1. 生成器抽象与需求

系统将画笔生成器抽象为一个黑盒函数 $G(I, b)$，接收一张带 alpha 通道的 RGBA 图像 $I$（其中已知区域 alpha=1，待修复区域 alpha=0）和纹理身份条件 $b$，输出修复后的 RGB 图像 $I'$。这一生成器必须满足三个硬性需求（§3.1）：

- **R1**：具备条件修复能力，能根据周围已知像素合理填充缺失区域；
- **R2**：条件化机制支持可控的画笔身份（brush identity），即生成内容必须忠实于用户指定的源纹理；
- **R3**：生成速度足够快，以支持实时交互式绘画。

### 2. 二维绘画 Pipeline

在 2D 画布上，绘画过程遵循 **Algorithm 1** 描述的图章循环（§3.2）：当用户沿笔触路径移动时，系统在每个采样点 $p_i$ 处执行以下步骤：

1. **裁剪局部上下文**：以 $p_i$ 为中心、画笔大小 $β$ 为范围，从当前画布 $I_c$ 中裁剪出一个局部区域，生成 RGBA 图像 $I$。其中已绘制区域为已知像素，待填充区域对应画笔的圆形或自定义形状。
2. **调用生成器**：将 $I$ 和纹理条件 $b$ 送入 $G$，获得修复后的 RGB 图像 $I'$。
3. **Alpha 合成**：将生成结果通过 alpha 混合写回画布：$I_c[\bar{\text{bound}}， 0:3] \gets I_\alpha \cdot I_{rgb} + \tilde{I}_\alpha \cdot I'$，其中 $\tilde{I}_\alpha$ 是 $I_\alpha$ 的补集。

这一过程通过重叠图章的方式逐步扩展纹理，生成器在每次调用时仅需填充当前画笔覆盖的局部区域，从而将全局纹理合成问题分解为一系列局部条件生成任务。

### 3. 三维绘画 Pipeline

三维绘画（§3.3，**Algorithm 2**）在 2D 框架的基础上引入了**局部切空间渲染**机制，以适应任意拓扑的网格表面：

1. **局部相机构建**：对于网格表面上的每个采样点 $p_i$，构建一个局部相机 $C_t$，其图像平面与网格在 $p_i$ 处的切平面平行，朝向由表面法线 $n$ 和笔触方向 $p_{i-1} \to p_i$ 共同决定。
2. **局部渲染**：使用渲染函数 $\mathcal{R}(F, P, F_U, U, T, W)$ 将网格面 $F$ 及其 UV 纹理 $T$ 投影到局部相机视角，生成 RGB 渲染 $I_{rgb}$、alpha 蒙版 $I_\alpha$ 和可见面索引 $f_{vis}$。画笔大小参数 $β$ 控制局部相机的视场角（FOV），从而决定每次修复的区域范围。
3. **修复与反向投影**：将渲染得到的 $I_{rgb}$ 和 $I_\alpha$ 送入生成器 $G$ 进行修复，然后将修复结果通过 UV 映射反向投影回纹理贴图 $T$，更新对应可见面 $f_{vis}$ 的纹理像素。

这一“局部渲染—修复—反向投影”的循环使得扩散模型无需感知全局 3D 几何，仅在 2D 切空间中进行生成，同时保证了生成内容与网格表面的无缝贴合。

### 4. 扩散模型适配与引导

上述 pipeline 对生成器 $G$ 的核心要求——**在保持纹理身份的同时产生合理变化**——直接驱动了扩散模型端的三个关键设计（§4）：

- **多尺度图像编码器 + LoRA 微调**（§4.2）：将源纹理图像 $S$ 通过 CLIP 提取多尺度 patch 嵌入，经 Transformer 融合后作为修复扩散模型的条件向量，替代传统的文本提示词。LoRA 低秩适配器以极少的可训练参数实现高效的条件注入。
- **纹理引导（Texture Guidance, TG）**（§4.3）：在标准分类器自由引导（CFG）的基础上，引入由源纹理构造的“伪上下文”图像 $\hat{I}$ 作为额外引导信号，通过公式 $\hat{\epsilon}_\theta = \tilde{\epsilon}_\theta + \tau \cdot (\epsilon_\theta(x_t, t, b, \hat{I}) - \epsilon_\theta(x_t, t, b, I))$ 修正去噪方向，其中 $\tau \in [0,1]$ 控制引导强度，以在纹理一致性和生成多样性之间取得平衡。

这三个模块的协同作用构成了完整的纹理画笔生成器，其有效性在消融实验中得到了充分验证：直接使用原始条件修复扩散模型会在几个图章后出现严重的纹理漂移（Figure 4b），即使配合提示词反转也无法避免（Figure 4c）；引入多尺度图像条件化可减轻漂移但仍未完全消除（Figure 4d）；只有进一步加入纹理引导（$\tau > 0$）才能几乎消除漂移，同时保持生成多样性（Figure 4e, Table 1）。

![[assets/figures/papers/paper_list_l20_https_dl_acm_org_doi_pdf_10_1145_3641519_3657458/figures/009_Figure.jpg]]
*Figure: Photoshop Texture Mixer TextureAE Gcorr (not real-time) Ours (a) Strokes: baselines vs. our method on strokes painted top to bottom, given the frst patch as target. (b) Texture Transitions: baselines vs. our method on generating natural transitions. Although stochastic, longer transitions remain consistent (right)*

![[assets/figures/papers/paper_list_l20_https_dl_acm_org_doi_pdf_10_1145_3641519_3657458/figures/001_Figure_1.jpg]]
*Figure 1: Di usion texture painting can turn any image into a brush. Our method allows interactive painting on the surface of 3D meshes, producing complex, non-repeating seamlessly tiling textures, such as stone path and rock details on this lawn, gingerbread house roof or realistic crochet patterns on the toy. 3D models from Sketchfab: house by LowlyPoly and stu ed dino by Andrey.Chegodaev*

### 3.1 图章生成器：条件修复扩散模型

Diffusion Texture Painting 将预训练的潜在扩散模型（Latent Diffusion Model）改造为一个**随机条件修复生成器** $G(I, b)$。该生成器接收带有二值 alpha 通道（0 或 1）的 RGBA 图像 $I$ 和条件 $b$（纹理身份），输出修复后的 RGB 图像 $I'$。生成器需满足三个核心要求（§3.1）：

- **R1**：具备条件修复能力，能在已知画布内容的约束下生成新内容；
- **R2**：条件机制支持可控制的画笔身份（即纹理样式）；
- **R3**：生成速度足够快，以支持交互式绘画。

在实际绘画循环中，生成器以重叠图章（stamp）的方式运行：每次在当前画布上取一个局部区域作为 $I$，生成器填充该区域内的空白部分，输出 $I'$ 再通过 alpha 合成写回画布（Algorithm 1, §3.2）。

### 3.2 多尺度图像条件编码器

为了让扩散模型以**图像**而非文本作为纹理条件，本文设计了一个多尺度图像编码器（Figure 5, §4.2）。该编码器从源纹理 $S$ 中提取不同尺度的特征：

1. 将源纹理 $S$ 分割为多个尺度的 CLIP 图像块（patches）；
2. 每个尺度的块分别通过 CLIP 图像编码器提取嵌入向量；
3. 所有尺度的嵌入经 Transformer 融合后，作为修复扩散模型的条件向量 $b$。

在此基础上，通过 **LoRA**（Low-Rank Adaptation）对预训练的 Stable Diffusion Inpainting 模型进行高效微调：仅注入可训练的低秩分解权重矩阵，使模型学会根据图像条件 $b$ 而非文本提示词进行修复生成（§4.2）。实验表明，这一更强的图像条件化能减轻纹理漂移，但尚未完全消除（Figure 4d）。

### 3.3 纹理引导（Texture Guidance）

纹理引导是本文抑制纹理漂移的核心机制（§4.3）。其关键思想是：在标准分类器自由引导（CFG）的基础上，引入一个由源纹理构造的**伪造上下文** $\hat{I}$，强制生成结果与源纹理保持一致。

#### 3.3.1 标准分类器自由引导（CFG）

对于修复任务，标准 CFG 通过缩放因子 $s > 1$ 将去噪方向推向条件 $b$：

$$\tilde{\epsilon}_\theta(x_t, t, b, I) = \epsilon_\theta(x_t, t, \emptyset, I) + s \cdot (\epsilon_\theta(x_t, t, b, I) - \epsilon_\theta(x_t, t, \emptyset, I)) \tag{Eq. 3}$$

其中：
- $x_t$：时间步 $t$ 的噪声潜在表示；
- $\epsilon_\theta$：去噪网络预测的噪声；
- $b$：纹理条件（来自多尺度编码器）；
- $\emptyset$：空条件（无条件预测）；
- $I$：待修复的 RGBA 图像（含 alpha 蒙版）。

#### 3.3.2 纹理引导项

纹理引导在 CFG 基础上增加一个修正项：

$$\hat{\epsilon}_\theta(x_t, t, b, \hat{I}) = \tilde{\epsilon}_\theta(x_t, t, b, I) + \tau \cdot (\epsilon_\theta(x_t, t, b, \hat{I}) - \epsilon_\theta(x_t, t, b, I)) \tag{Eq. 4}$$

其中：
- $\hat{I}$：纹理引导的上下文图像，由源纹理 $S$ 构造的“伪造”修复输入（Figure 6 展示了 $\hat{I}$ 的生成方式：将源纹理的随机裁剪与当前画布内容进行像素级组合）；
- $\tau \in [0, 1]$：纹理引导强度。$\tau = 0$ 退化为标准 CFG，$\tau = 1$ 施加最强引导。

**变量含义**：
- $\tilde{\epsilon}_\theta(x_t, t, b, I)$：标准 CFG 预测（Eq. 3）；
- $\epsilon_\theta(x_t, t, b, \hat{I})$：以伪造上下文 $\hat{I}$ 为修复输入的条件预测；
- 差值 $\epsilon_\theta(x_t, t, b, \hat{I}) - \epsilon_\theta(x_t, t, b, I)$ 表示“如果修复区域看起来更像源纹理，噪声预测应如何调整”；
- $\tau \leq 1$ 的约束确保生成结果保留一定多样性，避免完全复制源纹理。

#### 3.3.3 效果验证

消融实验（Table 1, §5.4）证实：$\tau = 1$ 相比 $\tau = 0$ 在 Pexels 纹理数据集上同时改善了纹理一致性（SWD 降低）和图章多样性（FID 降低），几乎消除了连续笔触中的纹理漂移（Figure 4e）。

### 3.4 3D 绘画空间与渲染函数

在 3D 网格表面绘画时，系统在局部切空间运行修复生成器，再将结果投影回 UV 贴图（§3.3, Algorithm 2）。核心渲染函数为：

$$I_{rgb}, I_{\alpha}, f_{vis} \gets \mathcal{R}(F, P, F_U, U, T, W) \tag{Eq. 1}$$

其中：
- $F$：网格面片；
- $P$：投影后的顶点位置；
- $F_U, U$：面片 UV 索引和 UV 坐标；
- $T$：当前 UV 纹理贴图；
- $W$：画布分辨率；
- $I_{rgb}$：渲染的 RGB 图像；
- $I_{\alpha}$：渲染的 alpha 蒙版（标记哪些像素已被绘制）；
- $f_{vis}$：可见面片索引（用于后续将修复结果写回 UV 贴图的对应区域）。

每次笔触时，系统在网格表面采样点 $p_i$，构造局部相机使其像平面与网格相切（§3.3.1），渲染得到局部画布图像 $I$ 后送入修复生成器，生成结果再通过 $f_{vis}$ 反向投影更新 UV 纹理 $T$。画笔大小参数 $\beta$ 控制局部相机的视场角（FOV），从而调节每次图章覆盖的几何范围（§3.3.3）。

## 实验与关键发现

### 核心实验设置

实验围绕两个关键目标设计：**纹理一致性**（防止漂移）与**生成多样性**（避免单调克隆），分别通过 Sliced Wasserstein Distance（SWD ↓）和 Fréchet Inception Distance（FID ↓）量化。评估采用自动生成的连续笔触，在 5 个重叠图章上取平均（Figure 7a）。数据集包含三类：Describable Textures Dataset（5640 张）、Earth textures dataset（896 训练 / 98 测试），以及从 Pexels 收集的 100 张免版税真实照片以覆盖开放域纹理。

![[assets/figures/papers/paper_list_l20_https_dl_acm_org_doi_pdf_10_1145_3641519_3657458/figures/002_Figure.jpg]]
*Figure: (b) NeuBE brushes [Shugrina et al. 2022]*

![[assets/figures/papers/paper_list_l20_https_dl_acm_org_doi_pdf_10_1145_3641519_3657458/figures/010_Figure.jpg]]
*Figure: (a) Painting missing parts of a photogrammetry texture 𝑇 , given patchwork UV-mapping with seams. Multiple sample brushes 𝑆𝑖 were used. Tree model from Sketchfab by Andrei Alexandrescu*

### 主结果：纹理一致性与多样性的权衡突破

在 Pexels 开放纹理集上，**Diffusion Texture Painting（τ=1）在 FID 和 SWD 两项指标上均显著优于所有近实时基线**（Table 1）：

![[assets/figures/papers/paper_list_l20_https_dl_acm_org_doi_pdf_10_1145_3641519_3657458/figures/008_Table_1.jpg]]
*Table 1: Quantitative results against near real-time baselines (§5.1, §5.2). For each method, we show mean and standard deviation in black and 95% confdence interval in blue*

| 方法 | FID ↓ | SWD ↓ |
|------|-------|-------|
| **Ours (τ=1)** | **1.18 ± 0.921** | **0.311 ± 0.238** |
| Ours (τ=0) | 1.41 ± 0.992 | 0.368 ± 0.283 |
| TextureMixer | 4.02 ± 3.81 | 0.472 ± 0.431 |
| TextureAE | 7.02 ± 5.28 | 0.652 ± 0.507 |
| PatchMatch | 0.86 ± 0.680 | 0.347 ± 0.272 |

关键发现：**PatchMatch 在 FID 上略优（0.86 vs 1.18），但其 SWD 高于 Ours（0.347 vs 0.311），且本质上是确定性克隆画笔，无法产生纹理变体**。TextureMixer 和 TextureAE 作为学习式方法，在两项指标上均大幅落后，暴露了闭域训练方法在开放纹理上的泛化瓶颈。

### 消融实验：纹理引导是抑制漂移的决定性因素

Table 1 中的 **Ours (τ=0) vs Ours (τ=1)** 构成核心消融，直接验证了 Texture Guidance（TG）的因果效应：

- **τ=0 → τ=1**：FID 从 1.41 降至 1.18（↓16.3%），SWD 从 0.368 降至 0.311（↓15.5%）
- 这表明 TG 不仅增强了纹理一致性（SWD 降低），**同时改善了图章多样性（FID 降低）**——这是一个反直觉的双赢结果，因为通常一致性增强会牺牲多样性。

Figure 4 提供了这一消融的定性证据链：(b) 普通条件修复扩散模型在几个图章后即发生严重漂移；(c) 提示词反转无法挽救；(d) 多尺度图像编码器 + LoRA 微调减轻但未消除漂移；(e) 加入 TG（τ>0）后漂移几乎消失。

### 纹理过渡与笔触质量

Figure 7 展示了连续笔触和纹理过渡的定性对比。在纹理过渡任务上，基线方法产生生硬的边界或不自然的混合，而本文方法能**幻觉出自然的过渡区域**（Figure 7b-c）。这一能力源于修复扩散模型在重叠区域的生成式填充，而非简单的 alpha 混合。

### 失败模式与已知局限

尽管定量结果优异，以下场景仍存在可观测的退化：

1. **高曲率与自遮挡区域**：从局部相机投影回 UV 贴图时，极端曲率表面会出现拉伸和伪影（§3.3 的几何约束）。
2. **过渡边界不可控**：艺术家无法指定不同纹理之间幻觉边界的风格或形状，过渡完全由模型隐式决定。
3. **PBR 通道质量不足**：法线、粗糙度等通道的绘画一致性远未达到 RGB 水平（Figure 8 标注为 early exploration）。
4. **非 UV 映射网格**：当前实现仅支持标准 UV 映射，对动态图册或无参数化几何体缺乏直接支持。

### 公平性说明

- 非实时方法 Gcorr 被排除在延迟比较之外；本文系统基于 TensorRT 优化的 Stable Diffusion 推理实现实时交互。
- 所有方法在相同数据集和评估协议下比较，但基线（如 TextureMixer）未针对交互式绘画场景进行特化调参。
- 定量评估使用自动生成的连续笔触，真实绘制质量仍需依赖艺术家主观体验验证。

## 定位与知识库关联

### 问题定位：纹理绘画中的身份漂移

Diffusion Texture Painting 直面一个长期被忽视的核心瓶颈：**预训练扩散模型在连续交互式纹理绘画中无法维持稳定的纹理身份**。当用户用画笔在画布上连续绘制时，每个图章（stamp）都需要与已绘制内容无缝衔接，同时保持与源纹理一致的外观。然而，直接使用条件修复扩散模型（vanilla conditional inpainting DM）作为画笔生成器，会在仅几个图章后发生严重的纹理漂移（identity drift）——生成的纹理逐渐偏离源纹理的视觉特征（Figure 4b）。即使配合提示词反转（prompt inversion）技术，也无法有效遏制这种漂移（Figure 4c）。这一发现将扩散模型的“多样性-一致性”张力暴露在实时交互场景中，构成了本文的核心科学问题。

### 方法谱系：从纹理合成到扩散引导

本文的方法建立在三条技术脉络的交汇点上：

**1. 基于示例的纹理合成（Example-based Texture Synthesis）**

传统纹理合成方法可分为两大流派。一类是经典的基于块匹配（patch-based）方法，如 **PatchMatch**（Barnes et al., ACM TOG 2010），通过从高分辨率示例图像中复制和拼接图像块来生成纹理。这类方法能保持纹理一致性，但缺乏生成多样性，且需要预先准备大规模示例图像。另一类是神经纹理合成方法，如 **Gcorr**（guided correspondence-based neural texture synthesis），利用深度特征对应关系引导生成，但通常无法实时运行。

**2. 可控纹理生成网络（Controllable Texture Generation Networks）**

近年来涌现的深度学习纹理合成方法试图在可控性和多样性之间取得平衡。**TextureMixer**（Yu et al., CVPR 2019）是一个闭域训练的可控纹理合成与插值网络，能够生成多样化的纹理变体，但在开放域纹理上的泛化能力有限。**TextureAE** 基于自编码器架构进行纹理合成，同样受限于训练数据的分布。这些方法在定量评估中（Table 1）的 FID 和 SWD 指标均显著劣于本文方法，根本原因在于它们无法像扩散模型那样利用大规模预训练的先验知识进行开放域生成。

**3. 扩散模型的条件化与引导（Diffusion Model Conditioning and Guidance）**

本文的方法直接继承自潜在扩散模型（Latent Diffusion Models）和修复扩散模型（Inpainting Diffusion Models）的研究脉络。标准做法是使用分类器自由引导（Classifier-Free Guidance, CFG）来增强条件一致性（Eq. 3）。然而，本文揭示了一个关键发现：**仅靠 CFG 和更强的图像条件化（如多尺度 CLIP 编码器配合 LoRA 微调）只能减轻漂移，无法消除漂移**（Figure 4d）。这促使作者引入了一种全新的引导机制——纹理引导（Texture Guidance, TG）。

### 核心创新：纹理引导作为因果旋钮

纹理引导（Eq. 4）是本文最关键的因果旋钮。其核心思想是：在 CFG 的基础上，引入一个由源纹理构造的“伪造上下文” $\hat{I}$ 作为额外的去噪引导项：

$$\hat{\epsilon}_\theta(x_t, t, b, \hat{I}) = \tilde{\epsilon}_\theta(x_t, t, b, I) + \tau \cdot (\epsilon_\theta(x_t, t, b, \hat{I}) - \epsilon_\theta(x_t, t, b, I))$$

其中 $\tau \in [0, 1]$ 控制引导强度。当 $\tau=0$ 时退化为标准 CFG；当 $\tau=1$ 时最大化纹理一致性。消融实验（Table 1）证实了 TG 的关键作用：$\tau=1$ 相比 $\tau=0$ 在 Pexels 数据集上将 SWD 从 0.342 降至 0.311（纹理漂移减少），同时将 FID 从 1.42 降至 1.18（多样性改善）。这一反直觉的结果表明，**更强的纹理约束并未牺牲生成多样性，反而通过稳定身份特征使模型更敢于生成合理的变化**。

### 技术架构的独特性

与现有方法相比，Diffusion Texture Painting 在四个关键维度上进行了系统性重构：

| 维度 | 基线方法 | 本文方法 |
|------|---------|---------|
| 画笔生成器 | 确定性克隆或基于示例的块合成 | 随机条件修复扩散模型（§3.1-3.2） |
| 纹理条件化 | 文本提示词或无特定条件 | 多尺度图像编码器 + LoRA 微调（§4.2） |
| 去噪引导 | 仅使用标准 CFG | CFG + 纹理引导项 TG（§4.3） |
| 绘画空间 | 直接在 2D 画布或 UV 贴图上克隆 | 局部切空间渲染修复后反向投影至 UV（§3.3） |

其中，3D 绘画空间的创新尤为值得关注。通过在网格表面的每个笔触点构造局部切空间相机（Eq. 1），将修复扩散模型的生成结果投影回 UV 贴图，该方法实现了对任意 UV 映射网格的实时纹理绘画，而无需预处理或标注。

### 适用边界与局限

**适用场景：**
- 标准 UV 映射的 3D 网格表面纹理绘画
- 开放域纹理的实时、多样化生成
- 需要纹理过渡和变体的艺术创作场景

**已知局限：**
1. **几何约束**：当前实现仅支持标准 UV 映射网格，对无参数化网格或不规则几何体的直接支持有限。在高曲率或自遮挡区域，从局部相机投影回 UV 贴图时可能出现拉伸和伪影。
2. **过渡控制**：不同纹理之间的过渡边界不可控，艺术家无法精确指定过渡样式或边界形状，这限制了精细艺术创作的需求。
3. **PBR 通道**：对法线、粗糙度等 PBR 材质通道的绘画质量与一致性仍处于早期探索阶段，未达到 RGB 通道的水准。
4. **推理速度**：尽管进行了 TensorRT 优化，扩散模型的生成速度仍受限于 GPU 能力，可能影响极大规模场景或超高分辨率画笔的实时性。
5. **笔触形态**：画笔形状控制较为基础，缺乏对更复杂笔触形态和动态变化的支持。

### 开放问题与未来方向

本文在结论中明确指出了五个关键开放问题，这些问题构成了该方向的潜在研究路径：

1. **可控纹理过渡**：如何允许艺术家交互式地控制或选择不同纹理之间幻觉边界的风格与融合方式？这涉及将用户意图编码为额外的条件信号。

2. **非标准参数化支持**：如何将方法扩展到非 UV 映射的网格表示（如动态图册或局部参数化），以更好地处理复杂拓扑和高曲率表面？

3. **自适应分辨率**：能否根据画笔大小 $\beta$ 动态调整生成器的分辨率，在保持质量的同时进一步提升推理速度？

4. **全 PBR 通道生成**：如何将高质量的全 PBR 通道生成稳定地集成到同一扩散纹理绘画框架中？这需要解决多通道一致性问题。

5. **更大上下文引导**：使用更大的外部源图像 $S^*$ 提供去噪指导能否进一步改善全局一致性和多样性？这涉及在计算开销和生成质量之间寻找新的平衡点。

### 在知识库中的定位

Diffusion Texture Painting 在纹理合成与扩散模型应用的知识谱系中占据了一个独特位置：它既不是纯粹的纹理合成方法（如 TextureMixer 的闭域训练范式），也不是简单的扩散模型应用（如直接使用修复扩散模型作为画笔）。它的核心贡献在于**识别并解决了扩散模型在连续交互场景中的身份漂移问题**，通过纹理引导机制在多样性和一致性之间建立了一个可调节的平衡点。这一工作为扩散模型在交互式内容创作领域的应用开辟了新路径，其提出的“伪造上下文引导”思想可能对更广泛的生成模型控制问题具有启发意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Diffusion_Texture_Painting.pdf]]

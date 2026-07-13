---
title: "Premier: Personalized Preference Modulation with Learnable User Embedding in Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Premier_Personalized_Preference_Modulation_with_Learnable_User_Embedding_in_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- Premier
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 可学习的用户嵌入通过偏好适配器（共享与独立）在 MM-DiT 的调制空间中进行逐文本标记（token）的偏好注入，并配合 dispersion loss 增强嵌入间的可区分性。
primary_logic: 通过流匹配损失与对比式 dispersion loss 联合训练的可学习用户嵌入，能更直接、更准确地编码用户视觉偏好；通过将新用户表示为训练用户嵌入的线性组合，实现了在极少样本下的稳定个性化。
claims:
- Premier 在 ViPer 代理评估下取得最高偏好对齐分数（ViPer Score 0.6889，远超第二名 ViPer 的 0.5159）以及最高偏好率（ViPer Rate 0.876）。
- 移除 dispersion loss 导致 ViPer Score 从 0.6889 剧烈降至 0.4498，证明该损失对区分用户偏好的决定性作用。
- 专家用户研究中，人类评估者显著更偏好 Premier 生成的图像（偏好率高于所有基线）。
- 在 PIP 数据集上，Premier 同样取得最佳 ViPer Score（0.7204）和最低 LPIPS（0.5982），验证了方法的泛化性。
---

# Premier: Personalized Preference Modulation with Learnable User Embedding in Text-to-Image Generation

> [!tip] 核心洞察
> 通过流匹配损失与对比式 dispersion loss 联合训练的可学习用户嵌入，能更直接、更准确地编码用户视觉偏好；通过将新用户表示为训练用户嵌入的线性组合，实现了在极少样本下的稳定个性化。

| 字段 | 内容 |
|------|------|
| 中文题名 | Premier：基于可学习用户嵌入的个性化偏好调制文本到图像生成 |
| 英文题名 | Premier: Personalized Preference Modulation with Learnable User Embedding in Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20725) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Premier |
| Dataset | PIP 数据集偏好对齐, 与 LoRA 个性化方案对比 |

> [!tip] 效果简介
> - 用户偏好对齐评估 (ViPer Proxy Model) 上，ViPer Score↑ 0.6889 vs 0.5159 (ViPer) (+0.1730)；ViPer Rate↑ 0.876 vs 0.676 (ViPer) (+0.200)。
> - PIP 数据集偏好对齐 上，ViPer Score↑ 0.7204 vs 0.6125 (次优方法) (+0.1079)。
> - 与 LoRA 个性化方案对比 (用户偏好对齐与文图一致性) 上，CLIP T2I↑ / LPIPS↓ / 存储/训练效率 CLIP T2I 0.3183, LPIPS 0.5986, 61KB/用户, 30分钟/用户 vs CLIP T2I 0.3033 (LoRA), LPIPS 0.5788 (LoRA), 10.7MB/用户, 1.2小时/用户 (在几乎相同的偏好对齐下，文图一致性更高，存储减小175倍，训练快2.4倍)。

## 概要

文本到图像生成模型在遵循用户文本指令方面已取得显著进展，但如何使生成结果忠实反映用户的**视觉偏好**仍是一个开放挑战。用户的偏好往往是隐性的——例如对特定色调、构图风格或光影氛围的倾向——难以用自然语言精确描述。现有方法通常借助多模态语言模型从用户历史图像中提取偏好表征，然而，这种间接传递路径存在结构性瓶颈：语言模型的隐状态或生成的文本描述在注入生成模型时，不可避免地丢失细粒度视觉信息，导致偏好对齐失败或指令跟随能力下降。此外，当用户历史数据量有限且样本间相关性较弱时，多模态模型更难以捕捉个体间的微妙差异。

针对上述瓶颈，Premier 提出了一种端到端的个性化偏好调制框架。其核心思路是：**用可学习的用户嵌入直接编码视觉偏好，并通过偏好适配器在生成模型的调制空间中实现逐文本标记（token）的条件注入**。具体而言，该方法为每个用户维护一个可训练向量，训练时不再依赖中间语言描述，而是将用户嵌入与文本提示共同送入偏好适配器，适配器通过交叉注意力机制输出针对每个文本标记的调制方向。这些调制方向被叠加到基础文本到图像模型（基于 MM-DiT 架构的 Flux）的原始调制矢量上，从而在去噪过程中精确调控生成内容的视觉属性。为增强不同用户嵌入的可区分性，Premier 进一步引入了基于 InfoNCE 的 **dispersion loss**，强制不同嵌入在调制方向空间中彼此分离。对于新用户（冷启动场景），该方法将新嵌入表示为训练集用户嵌入的线性组合，仅优化组合系数，从而在极少历史样本（≤4 张）下仍能获得稳定的个性化效果。

在 ViPer 代理模型评估下，Premier 取得了 **0.6889 的 ViPer Score** 和 **0.876 的 ViPer Rate**，分别超出次优方法 0.1730 和 0.200。专家用户研究同样证实，人类评估者显著更偏好 Premier 生成的图像。消融实验揭示了两个关键发现：其一，移除 dispersion loss 后 ViPer Score 骤降至 0.4498，生成图像在不同用户间几乎无差异；其二，共享适配器与独立适配器缺一不可，单独移除任一项均导致性能大幅下降。与针对每个用户微调 LoRA 的方案相比，Premier 在保持同等偏好对齐水平的同时，将单用户存储开销从 10.7 MB 压缩至 61 KB（约 175 倍），训练时间缩短 2.4 倍，且文本-图像一致性更高。在 PIP 数据集上的泛化实验（ViPer Score 0.7204，LPIPS 0.5982）进一步验证了方法的鲁棒性。

### 问题背景：文本到图像生成中的个性化需求

文本到图像生成模型近年来取得了显著进展，以 **Flux**（Black Forest Labs et al., 2025）为代表的多模态扩散变换器（MM-DiT）架构能够根据自然语言描述生成高质量、高保真度的图像。然而，在实际应用中，不同用户对同一文本提示的视觉期望往往存在显著差异——某位用户可能偏好“写实摄影风格”，而另一位用户则可能期望“动漫插画风格”。这种个性化的视觉偏好无法仅通过文本提示完整表达，因此需要模型能够从用户的历史偏好数据中学习并复现其独特的审美倾向。

### 现有方法缺口：偏好信息传递的断裂

当前主流的个性化方法通常依赖多模态语言模型（MLLM）来提取用户偏好，其核心路径可归纳为两类：

1. **隐状态传递**：利用 MLLM 的隐层表示作为用户偏好的代理信号，将其注入生成模型。然而，MLLM 的隐状态与文本到图像模型的条件空间之间存在语义鸿沟，偏好信息在跨模型传递中容易丢失或失真。

2. **自然语言描述**：将用户偏好转化为文本描述（如 **ViPer**，Salehi et al., 2024），再以提示工程的方式指导生成。但自然语言对细粒度视觉偏好的表达能力有限，且文本描述的重写过程可能引入语义偏移，导致指令跟随失败。

更深层的问题在于，用户历史数据往往呈现**弱相关性**——同一用户可能在不同场景下偏好不同的风格、色调或构图，这使得 MLLM 难以从有限且弱关联的样本中捕捉到一致且可区分的偏好特征。当不同用户的偏好差异微妙时（例如两位用户都偏好“暖色调”，但一位倾向橙金、另一位倾向玫瑰金），基于文本或隐状态的方法几乎无法做出有效区分。

### 核心动机：从间接描述到直接编码

本文的核心动机在于**绕过偏好描述的中间层，直接在文本到图像模型的调制空间中对用户偏好进行编码与注入**。具体而言，我们提出 **Premier** 方法，其设计理念基于以下观察：

- **可学习嵌入的直连性**：与其依赖外部 MLLM 提取可能失真的偏好表示，不如让用户偏好以可训练向量的形式直接参与生成模型的端到端优化。通过流匹配损失（flow matching loss）的监督，用户嵌入能够在训练过程中自发地收敛到最能影响生成结果的特征方向。

- **调制空间的细粒度注入**：MM-DiT 架构中的调制矢量（modulation vector）控制着每个文本标记（token）在每一层 DiT 块中的条件信息流。在这一空间中进行逐标记、逐层的偏好注入，能够实现上下文感知的细粒度调制，而非粗糙的条件拼接。

- **嵌入可区分性的显式约束**：为使用户嵌入真正编码个体化的偏好差异，我们引入基于 InfoNCE 的 **dispersion loss**，强制不同用户的调制方向在特征空间中保持分离。这一对比式约束弥补了仅靠流匹配损失难以区分微妙偏好差异的不足。

- **冷启动的稳定性需求**：在实际部署中，新用户仅能提供极少量的偏好图像（如 2–4 张）。直接训练用户嵌入极易过拟合，因此我们将新用户嵌入建模为训练集用户嵌入的线性组合，仅优化组合系数，从而在极少样本下获得稳定的偏好表示。

通过上述设计，Premier 旨在实现从“描述偏好”到“编码偏好”的范式转变，使文本到图像生成模型能够更直接、更准确地响应个体用户的视觉偏好。

## 核心方法与创新机理

Premier 的核心创新在于将用户偏好编码从间接的多模态语言模型隐状态或文本描述，转变为**可学习的用户嵌入**，并通过流匹配损失端到端地训练这些嵌入，使其直接捕获用户的视觉偏好信息。这一转变解决了先前方法中偏好信息在传递至文本到图像模型时发生丢失或指令跟随失败的根本瓶颈。

在偏好注入机制上，Premier 引入了**偏好适配器**（Preference Adapter），包含共享适配器（块间共享调制方向）和独立适配器（各 DiT 块产生不同方向）。适配器通过交叉注意力机制将用户嵌入与输入文本标记融合，为每个文本标记生成偏好感知的调制方向，并叠加至 MM-DiT 的原始调制矢量上：

$$y_i^j = y + \Delta_{\mathrm{shared}}(e_u, e_{p_i}) + \Delta_{\mathrm{distinct}}^j(e_u, e_{p_i})$$

这种逐标记（token-level）的调制方式使得偏好信息能够细粒度地影响生成过程，而非简单地拼接条件标记或以文本形式重写提示。

训练目标方面，Premier 在流匹配损失之外引入了基于 InfoNCE 的 **dispersion loss**，强制不同用户嵌入产生的调制方向在特征空间中充分分离：

$$\mathcal{L}_{\mathrm{disp}} = \log \sum_{j} \exp(-\mathcal{D}(\Delta_\theta(e_u, e_p), \Delta_\theta(e_{u'}, e_p)))$$

消融实验（Table 2）表明，移除 dispersion loss 后 ViPer Score 从 0.6889 骤降至 0.4498，且不同用户生成的图像几乎无差异（Figure 8），证实该损失对嵌入区分能力的决定性作用。

针对新用户冷启动问题，Premier 提出将新用户嵌入表示为训练集用户嵌入的**线性组合**，仅优化组合系数而非直接训练嵌入。在历史数据少于 8 张时，该策略在 ViPer Score 和 LPIPS 上均显著优于直接训练嵌入（Figure 6、Figure 7），实现了极少样本下的稳定个性化。

Premier 的核心设计目标是将用户视觉偏好直接编码为可学习的向量表示，并通过与文本提示的细粒度交互，在 MM-DiT 架构的调制空间中实现逐 token 的偏好注入。整个 pipeline 分为两个训练阶段和一个新用户适配阶段，其模块关系与数据流如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2334_https_arxiv_org_abs_2603_20725/figures/002_Figure_2.jpg]]
*Figure 2: Premier training framework. (a) During the training of the preference adapters, the user preference embeddings and the adapters are jointly optimized. The block-shared adapter produces a uniform modulation direction across all DiT blocks, whereas the block-distinct adapter generates different modulation directions for different DiT blocks. (b) Each preference adapter takes the learnable user embedding and the input text tokens as inputs, and outputs a preference modulation direction for every text token, enabling fine-grained and context-aware modulation. (c) Our method obtains the new user’s preference embedding as a linear combination of training-set user preference embeddings. During thi...*

### 两阶段训练流程

**第一阶段：偏好适配器与用户嵌入的联合训练。** 给定训练集中每位用户的偏好图像集合，Premier 为每个用户维护一个可学习的用户嵌入 $e_u$。该嵌入与用户提供的文本提示 token 嵌入 $e_{p_i}$ 一同送入两个偏好适配器——共享适配器（block-shared adapter）和独立适配器（block-distinct adapter）。两个适配器均采用交叉注意力机制，以文本 token 为 Query、用户嵌入为 Key 和 Value，分别输出一个跨所有 DiT 块共享的调制方向 $\Delta_{\mathrm{shared}}$ 和一个逐块不同的调制方向 $\Delta_{\mathrm{distinct}}^j$。最终的逐 token、逐块调制矢量由基础调制矢量 $y$（由 CLIP 文本嵌入和时间步嵌入线性组合得到）与两个偏好调制方向叠加而成：

$$y_i^j = y + \Delta_{\mathrm{shared}}(e_u, e_{p_i}) + \Delta_{\mathrm{distinct}}^j(e_u, e_{p_i})$$

该调制矢量随后注入 MM-DiT 的对应块中，控制生成过程。此阶段同时优化用户嵌入和两个适配器的参数，训练目标为流匹配损失 $\mathcal{L}_{\mathrm{flow}}$ 与 dispersion loss 的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{shared}} \mathcal{L}_{\mathrm{disp}}^{\mathrm{shared}} + \lambda_{\mathrm{distinct}} \mathcal{L}_{\mathrm{disp}}^{\mathrm{distinct}}$$

其中 dispersion loss 基于 InfoNCE 形式的对比损失，强制不同用户嵌入生成的调制方向在特征空间中相互分离，从而增强嵌入的可区分性：

$$\mathcal{L}_{\mathrm{disp}} = \log \sum_{j} \exp(-\mathcal{D}(\Delta_\theta(e_u, e_p), \Delta_\theta(e_{u'}, e_p)))$$

**第二阶段：新用户嵌入的线性组合优化。** 对于训练集中未出现的新用户，直接训练其嵌入容易因历史数据有限而严重过拟合。Premier 的解决方案是将新用户嵌入表示为第一阶段训练好的用户嵌入的线性组合，并固定偏好适配器参数，仅优化线性组合系数。这一策略在用户历史数据少于 8 张时显著优于直接训练嵌入（见 Figure 6 和 Figure 7），在极少样本（≤4 张）下优势尤为突出。

### 输入输出与关键模块

- **输入：** 用户的一组偏好图像（无需文本偏好描述）和一条文本提示。
- **可学习用户嵌入：** 为每位用户存储一个可训练向量，是偏好信息的唯一载体，通过流匹配损失端到端学习。
- **偏好适配器（共享 + 独立）：** 通过交叉注意力实现用户嵌入与文本 token 的交互，输出偏好调制方向。共享适配器提供全局一致的偏好方向，独立适配器则允许不同 DiT 块学习块特定的调制，二者缺一不可（消融实验中分别移除后 ViPer Score 均降至 0.48 左右）。
- **调制方向叠加：** 将共享与独立的偏好调制方向加至基础调制矢量上，实现逐 token、逐块的偏好注入。
- **Dispersion Loss：** 对比式正则项，推动不同用户的调制方向在特征空间中分散，是方法有效性的关键组件（移除后 ViPer Score 从 0.6889 骤降至 0.4498）。
- **输出：** 对齐用户视觉偏好且保持文本一致性的生成图像。

### 1. 问题形式化与流匹配基础

Premier 的目标是：给定用户 $u$ 的 $K$ 张历史偏好图像 $\{x_k\}_{k=1}^K$ 和一条文本提示 $p$，生成一张既忠实于 $p$ 又符合 $u$ 视觉偏好的图像。方法建立在流匹配（Flow Matching）框架之上，基础生成模型采用 Flux 的 MM-DiT 架构。

流匹配的核心是学习一个时变速度场 $\mathbf{v}_\theta$，将噪声逐步转化为数据。在扩散步 $t \in [0, 1]$，对数据样本 $z_0$ 和噪声 $z_1$ 进行线性插值：

$$z_t = (1 - t) \cdot z_0 + t \cdot z_1 \quad \text{(Eq. 1)}$$

模型通过最小化预测速度与真实速度方向之间的 L2 距离来训练：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{z_0,z_1,t} \left[ \| \mathbf{v}_\theta(\mathbf{z}_t, c, t) - (\mathbf{z}_1 - \mathbf{z}_0) \|_2^2 \right] \quad \text{(Eq. 2)}$$

其中 $c$ 为条件信息（文本提示），$t$ 为时间步嵌入。

### 2. MM-DiT 中的调制机制

在 MM-DiT 架构中，文本提示 $p$ 经 CLIP 编码为嵌入 $e_p$，与时间步嵌入 $t$ 共同生成基线调制矢量 $y$：

$$y = \mathcal{M}_p(\mathbf{CLIP}(p)) + \mathcal{M}_t(t) \quad \text{(Eq. 3)}$$

该调制矢量作为全局条件注入 DiT 的各个块。为实现更细粒度的控制，可为每个文本标记 $i$ 添加特定的调制方向 $\Delta_i$，得到逐标记调制矢量：

$$y_i' = y + \Delta_i \quad \text{(Eq. 4)}$$

Premier 正是在这个调制空间中，将用户偏好信息以可学习嵌入的形式注入。

### 3. 可学习用户嵌入与偏好适配器

**核心创新：** 为每个用户 $u$ 维护一个可训练的偏好嵌入 $e_u$，通过偏好适配器（Preference Adapter）与文本标记嵌入 $e_{p_i}$ 交互，生成逐标记、逐 DiT 块的偏好调制方向。

偏好适配器采用交叉注意力机制，以文本标记为 Query，用户偏好嵌入为 Key 和 Value，输出与文本语义上下文相关的调制方向。系统包含两类适配器：

- **共享适配器（Block-Shared Adapter）**：在所有 DiT 块间产生统一的调制方向 $\Delta_{\mathrm{shared}}$，捕捉用户偏好的全局特征。
- **独立适配器（Block-Distinct Adapter）**：为每个 DiT 块 $j$ 生成不同的调制方向 $\Delta_{\mathrm{distinct}}^j$，适应不同层对风格、纹理、构图等要素的分层控制。

两类调制方向叠加到基线调制矢量 $y$ 上，形成第 $j$ 个 DiT 块中第 $i$ 个标记的最终调制矢量：

$$y_i^j = y + \Delta_{\mathrm{shared}}(e_u, e_{p_i}) + \Delta_{\mathrm{distinct}}^j(e_u, e_{p_i}) \quad \text{(Eq. 5)}$$

该设计的因果机制在于：共享适配器确保全局偏好一致性，独立适配器则在不同 DiT 块中实现层次化的细粒度偏好表达，二者协同使偏好信息精确渗透到生成过程的每一层。

### 4. Dispersion Loss：嵌入空间的可区分性约束

仅靠流匹配损失训练用户嵌入，容易导致不同用户的调制方向在特征空间中高度重叠，使生成结果缺乏个性化差异。为此，Premier 引入基于 InfoNCE 的 dispersion loss，强制不同用户嵌入产生的调制方向相互分离。

具体而言，对于用户 $u$ 和另一用户 $u'$，在给定相同文本 $p$ 的条件下，计算其调制方向之间的 L2 距离，并构造对比损失：

$$\mathcal{L}_{\mathrm{disp}} = \log \sum_{j} \exp(-\mathcal{D}(\Delta_\theta(e_u, e_p), \Delta_\theta(e_{u'}, e_p))) \quad \text{(Eq. 6)}$$

其中 $\mathcal{D}(\cdot, \cdot)$ 为 L2 距离，$\Delta_\theta$ 表示适配器输出的调制方向。该损失分别应用于共享适配器和独立适配器的输出，最终的训练损失为流匹配损失与两类 dispersion loss 的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{shared}} \mathcal{L}_{\mathrm{disp}}^{\mathrm{shared}} + \lambda_{\mathrm{distinct}} \mathcal{L}_{\mathrm{disp}}^{\mathrm{distinct}} \quad \text{(Eq. 7)}$$

**消融证据：** 移除 dispersion loss 后，ViPer Score 从 0.6889 骤降至 0.4498（Table 2），且不同用户生成的图像差异显著减小（Figure 8），证实该损失是区分用户偏好的决定性因素。

### 5. 新用户嵌入的线性组合策略

对于训练集中未见的新用户，直接训练其嵌入容易因数据稀疏而过拟合。Premier 采用线性组合策略：将新用户嵌入表示为训练集用户嵌入的线性组合，仅优化组合系数而冻结适配器参数。

该策略的直觉在于：训练集用户嵌入已覆盖丰富的视觉偏好空间，新用户的偏好可近似为该空间中的一个点。当历史数据极少（≤4 张）时，线性组合策略在 ViPer Score 和 LPIPS 上均显著优于直接训练嵌入（Figure 6, Figure 7），且训练效率更高。

### 6. 组件消融与因果链路总结

| 消融项 | ViPer Score | 因果作用 |
|--------|-------------|----------|
| 完整 Premier | 0.6889 | 基准性能 |
| 移除 dispersion loss | 0.4498 | 嵌入空间坍缩，用户间无差异 |
| 移除共享适配器 | 0.4818 | 丢失全局偏好一致性 |
| 移除独立适配器 | 0.4917 | 丢失层次化细粒度控制 |
| 移除提示-偏好调制 | 0.6492 | 偏好注入失去文本上下文感知 |

数据来源：Table 2。这些消融结果共同验证了“可学习嵌入 + 双适配器调制 + dispersion loss”三者协同的因果链路：嵌入编码偏好，适配器实现上下文感知注入，dispersion loss 保障嵌入可区分性。

![[assets/figures/papers/paper_list_l2334_https_arxiv_org_abs_2603_20725/figures/007_Table_2.jpg]]
*Table 2: Quantitative evaluation of preference image generation after ablation. The best results are highlighted in bold, while the second-best is underlined. Ablating the dispersion loss leads to a significant performance drop, while removing the modulation of prompt–preference interaction yields suboptimal results*

![[assets/figures/papers/paper_list_l2334_https_arxiv_org_abs_2603_20725/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative ablation comparison of our method. Ablating either of the two preference adapters leads to a significant performance drop, confirming their necessity. Ablating the text-preference modulation also degrades user-preference-aware image generation*

![[assets/figures/papers/paper_list_l2334_https_arxiv_org_abs_2603_20725/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative dispersion loss ablation comparison of our method. After ablating the dispersion loss, the generated preference images across different users exhibit substantially reduced variation*

## 实验与关键发现

### 主要结果：偏好对齐与文图一致性

Premier 在 ViPer 代理评估下取得了显著领先的个性化偏好对齐性能。如 Table 1 所示，Premier 的 ViPer Score 达到 **0.6889**，远超第二名的 ViPer（0.5159），提升幅度达 +0.1730；ViPer Rate 同样以 **0.876** 大幅领先所有基线（次优为 0.676）。值得注意的是，DrUM、ViPer 和 Premier 均使用 8 张用户历史图片，而 Bagel、Qwen-Image-Edit 和 InstantStyle 仅使用单张历史图片——即使在这种不对等的条件下，Premier 的优势依然稳固。在文图一致性（CLIP T2I）和多样性（LPIPS）指标上，Premier 同样保持竞争力，未出现偏好对齐提升导致文本跟随能力下降的典型权衡。

专家用户研究（Figure 4）进一步验证了这一结论：人类评估者在面对 6 张用户历史偏好图像和同一文本提示下生成的图像对时，显著更偏好 Premier 生成的图像，偏好率高于所有基线方法。

在 PIP 数据集上的泛化测试（Table B）中，Premier 取得最佳 ViPer Score（**0.7204**）和最低 LPIPS（**0.5982**），证明该方法在不同数据分布下依然有效。

### 与 LoRA 个性化方案的效率对比

Table A 揭示了 Premier 相对于逐用户微调 LoRA（Hu et al., 2022）的效率优势。在几乎相同的偏好对齐分数下（ViPer Score 持平），Premier 的文图一致性更高（CLIP T2I 0.3183 vs. 0.3033），而单用户存储需求仅为 **61 KB**，相比 LoRA 的 10.7 MB 减小约 **175 倍**；训练时间从 1.2 小时缩短至 **30 分钟**，加速约 2.4 倍。这一结果表明，可学习用户嵌入方案在个性化效率与生成质量之间取得了更优的权衡。

### 消融实验：各组件的因果贡献

Table 2 的消融实验揭示了三个关键组件的决定性作用：

1. **Dispersion Loss 的核心作用**：移除 dispersion loss 后，ViPer Score 从 0.6889 骤降至 **0.4498**，降幅超过 0.23。Figure 8 的定性结果显示，不同用户生成的偏好图像几乎无差异，证实该损失是维持用户嵌入间可区分性的关键机制。

2. **双适配器的必要性**：分别移除共享适配器（w/o Δshared）和独立适配器（w/o Δdistinct）导致 ViPer Score 降至 0.4818 和 0.4917，表明跨块的统一调制方向与逐块的差异化调制方向缺一不可。Figure 5 的定性对比进一步显示，任一适配器的缺失均导致生成图像偏离用户偏好。

3. **提示-偏好调制机制（PPM）的贡献**：移除逐令牌的偏好调制后，即使保留用户嵌入，ViPer Score 仍降至 0.6492，证明仅靠全局嵌入注入不足以实现精准的偏好对齐，逐文本标记的细粒度交互是必要的。

### 冷启动策略：线性组合 vs. 直接训练

针对新用户的嵌入获取，Premier 采用线性组合系数优化策略。Figure 6 和 Figure 7 分别从 ViPer Score 和 LPIPS 两个维度展示了该策略在不同历史数据长度下的表现：

- 当历史数据 **少于 8 张**时，线性组合策略在 ViPer Score 上显著优于直接训练用户嵌入，优势随数据减少而扩大。
- 在 LPIPS 指标上，线性组合的优势更为持久，在历史数据 **不超过 16 张**时均保持领先。
- Figure 9 的定性结果显示，少量历史数据下直接训练嵌入容易产生不稳定甚至崩溃的生成结果，而线性组合策略能保持稳定的偏好表达。

![[assets/figures/papers/paper_list_l2334_https_arxiv_org_abs_2603_20725/figures/011_Figure_9.jpg]]
*Figure 9: Qualitative comparison of our method across different user history lengths and different training strategy When the amount of user history is limited, training linear combination coefficients yields more stable performance*

这一现象的根本原因在于：直接训练少量样本的用户嵌入易陷入过拟合，而将新用户表示为训练集用户嵌入的线性组合，本质上是利用已有嵌入空间的语义结构进行正则化插值。

### 局限性与失效模式

1. **用户多样性的依赖**：Table C 的缩放分析显示，当训练集用户数从 100 降至 10 时，模型性能明显退化，表明嵌入空间的质量依赖于足够的用户多样性来支撑有效的 dispersion 约束。
2. **冷启动仍需要少量样本**：尽管线性组合策略在极少样本下表现稳健，但方法无法做到零样本个性化，仍需要至少数张偏好图像来优化组合系数。
3. **跨域迁移未验证**：论文未探索当用户偏好涉及跨域场景（如真实照片到卡通风格）时，偏好嵌入的绑定稳定性是否依然成立。

### 开放问题

- Dispersion loss 的超参数 λ_shared 和 λ_distinct 在不同用户群体规模下如何自动调节，目前尚缺乏自适应机制。
- 线性组合策略隐含了对多样化用户社区的近似，能否通过生成合成用户嵌入来直接扩充嵌入空间，值得进一步探索。
- 该方法是否能够与基于文本的偏好反馈（如用户评论）相结合，以进一步提升对齐精度，论文未给出答案。

![[assets/figures/papers/paper_list_l2334_https_arxiv_org_abs_2603_20725/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons of Preference Alignment. We compare the performance of our method with other approaches in user preference-aware image generation. The images generated by our method are closest to the user’s preferences while remaining faithful to the user-provided text prompt*

## 定位与知识库关联

### 1. 与基线方法的对比定位

Premier 的核心定位在于解决**个性化文本到图像生成中偏好信息传递的瓶颈**。现有方法大致可分为三条技术路线，Premier 在每条路线上都做出了差异化的设计选择。

**基于多模态语言模型的偏好提取路线。** 以 **ViPer**（Salehi et al., 2024）和 **DrUM**（Kim et al., 2025）为代表，这类方法依赖多模态语言模型从用户的正/负样本及评论中提取偏好，再以隐状态或自然语言描述的形式注入生成模型。其根本瓶颈在于：多模态模型的隐状态难以忠实地传递到文本到图像模型的生成空间中，造成偏好信息丢失或指令跟随失败。Premier 彻底绕开了这一瓶颈——它不依赖任何偏好描述文本，而是通过流匹配损失端到端训练可学习用户嵌入，使偏好编码直接与生成目标对齐。定量结果表明，Premier 在 ViPer Score 上达到 0.6889，远超 ViPer 的 0.5159 和 DrUM 的 0.5141（Table 1），验证了直接嵌入编码相对于间接语言描述的优势。

**基于参考图像的风格迁移路线。** 以 **InstantStyle**（Wang et al., 2024）和 **Bagel**（Deng et al., 2025）为代表，这类方法仅使用单张历史图片作为条件输入，通过风格迁移或统一预训练模型实现个性化。其局限性在于：单张图片难以捕捉用户偏好的细粒度差异和跨样本的一致性模式。Premier 使用 8 张历史偏好图像进行训练，通过可学习嵌入聚合多样本中的偏好信息。需要指出的是，Table 1 中不同方法使用的历史数据长度并不一致（InstantStyle 和 Bagel 仅用 1 张，而 Premier 用 8 张），这可能对单张历史图片的方法不利，但即使在相同数据长度下，Premier 仍显著领先。

**基于个性化微调的路线。** 以 **LoRA**（Hu et al., 2022）为代表，为每个用户微调低秩适配器。LoRA 在偏好对齐指标（ViPer Score）上与 Premier 基本持平，但代价显著：存储开销为 10.7 MB/用户（Premier 仅 61 KB，减小 175 倍），训练时间为 1.2 小时/用户（Premier 仅 30 分钟，快 2.4 倍），且文本一致性（CLIP T2I）更低（Table A）。这揭示了一个关键的效率-对齐权衡：LoRA 通过大量参数微调实现对齐，而 Premier 通过紧凑的用户嵌入和调制方向叠加实现了更高效的个性化。

### 2. 技术谱系中的创新锚点

Premier 在方法设计上有三个区别于所有基线的独立创新锚点，这些组件共同构成了其技术壁垒。

**锚点一：可学习用户嵌入替代文本偏好描述。** 所有现有方法（ViPer、DrUM、PMG 等）都依赖多模态语言模型提取偏好，Premier 首次将用户偏好建模为通过生成损失直接训练的可学习向量。这一设计使偏好编码与生成目标完全对齐，避免了跨模态信息传递的损失。

**锚点二：逐标记偏好调制机制。** 现有方法通常以条件标记拼接或文本重写的方式注入偏好，信息粒度粗糙。Premier 通过偏好适配器（共享适配器与独立适配器）在 MM-DiT 的调制空间中为每个文本标记施加独立的偏好调制方向（公式 $y_i^j = y + \Delta_{\mathrm{shared}}(e_u, e_{p_i}) + \Delta_{\mathrm{distinct}}^j(e_u, e_{p_i})$），实现了细粒度、上下文感知的偏好注入。消融实验表明，移除提示-偏好调制（w/o PPM）后 ViPer Score 从 0.6889 降至 0.6492，验证了逐标记机制的必要性（Table 2）。

**锚点三：Dispersion Loss 驱动的嵌入空间结构化。** 这是 Premier 最具决定性的创新。基于 InfoNCE 的 dispersion loss（公式 $\mathcal{L}_{\mathrm{disp}} = \log \sum_{j} \exp(-\mathcal{D}(\Delta_\theta(e_u, e_p), \Delta_\theta(e_{u'}, e_p)))$）强制不同用户的调制方向在特征空间中分离。移除该损失后，ViPer Score 从 0.6889 剧烈降至 0.4498（Table 2），且不同用户生成的图像差异显著减小（Figure 8），证明该损失对区分用户偏好的决定性作用。

**锚点四：基于线性组合的新用户嵌入策略。** 针对冷启动场景（新用户仅有少量偏好图像），Premier 将新用户嵌入表示为训练集用户嵌入的线性组合，仅优化组合系数而非直接训练嵌入。这一策略在历史数据少于 8 张时显著优于直接训练，尤其在极少样本（≤4 张）下优势更明显（Figure 6, Figure 7）。

### 3. 适用边界与局限

**用户多样性依赖。** 当训练集用户数量从 100 降至 10 时，模型性能明显退化（Table C）。这表明嵌入空间的质量依赖于足够的用户多样性来构建有意义的偏好流形。在小规模用户群体中，线性组合策略的表达能力受限，dispersion loss 也可能因正负样本不足而失效。

**冷启动仍需少量样本。** 虽然线性组合策略降低了对新用户数据量的要求，但方法仍需要一定数量的偏好图像（至少 2-4 张才能获得稳定性能），无法做到完全的零样本个性化。这与基于文本偏好描述的方法（如 ViPer）形成对比——后者在理论上可以零样本泛化，但代价是对齐精度较低。

**跨域迁移未探索。** 论文未验证当用户偏好涉及跨域迁移（如真实照片→卡通风格）时，偏好嵌入的绑定稳定性。线性组合策略假设新用户的偏好位于训练用户偏好空间的凸包内，如果新用户的偏好域与训练集差异过大，该假设可能不成立。

**基础模型的依赖性。** Premier 基于 **Flux**（Black Forest Labs et al., 2025）的 MM-DiT 架构构建，调制矢量叠加机制深度耦合于该架构的设计。迁移到其他生成架构（如基于 UNet 的扩散模型）需要重新设计适配器结构，泛化性有待验证。

### 4. 开放问题

1. **Dispersion loss 的自适应调节。** 当前 dispersion loss 的权重 $\lambda_{\mathrm{shared}}$ 和 $\lambda_{\mathrm{distinct}}$ 是固定超参数。在不同用户群体规模下，最优权重可能不同——用户越多，需要更强的分散力来避免嵌入坍缩；用户越少，过强的分散力可能导致嵌入空间过于稀疏。如何根据用户规模自动调节这些超参数是一个值得探索的方向。

2. **合成用户扩充的可行性。** 线性组合策略隐含了对用户偏好空间的凸组合近似。是否可以通过对训练用户嵌入进行插值或扰动来生成合成用户，从而扩充训练集并提升嵌入空间的覆盖度？这一思路与数据增强和对比学习中的正样本生成策略有自然联系。

3. **多模态偏好反馈的融合。** 当前方法仅使用偏好图像进行训练，未利用用户可能提供的文本评论或评分。如何将基于文本的偏好反馈（如 ViPer 中的评论分析）与可学习嵌入相结合，以进一步提升对齐精度，是一个自然的扩展方向。这需要设计跨模态的偏好融合机制，而非简单的级联。

4. **偏好嵌入的可解释性。** 可学习用户嵌入是一个黑箱向量，其各维度对应的视觉语义尚不明确。是否可以通过分析嵌入空间的几何结构（如主成分方向对应的生成图像变化）来赋予嵌入维度可解释的语义，从而支持用户主动编辑自己的偏好表示？

5. **隐私与去中心化部署。** 当前方法需要集中训练用户嵌入，涉及用户偏好数据的收集。是否可以通过联邦学习或个性化扩散模型的去中心化训练，在保护用户隐私的前提下实现类似的个性化效果？

## 原文 PDF

![[paperPDFs/CVPR_2026/Premier_Personalized_Preference_Modulation_with_Learnable_User_Embedding_in_Text_to_Image_Generation.pdf]]

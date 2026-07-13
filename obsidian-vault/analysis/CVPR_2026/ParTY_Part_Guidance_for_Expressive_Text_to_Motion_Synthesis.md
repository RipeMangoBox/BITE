---
title: "ParTY: Part-Guidance for Expressive Text-to-Motion Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ParTY_Part_Guidance_for_Expressive_Text_to_Motion_Synthesis.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Heo_ParTY_Part-Guidance_for_Expressive_Text-to-Motion_Synthesis_CVPR_2026_paper.html
project_link: https://visualsciencelab-khu.github.io/ParTY_project/
code_link: null
aliases:
- ParTY
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 部件引导生成（Part-Guided Network）与部件感知文本接地（Part-aware Text Grounding），使模型既能获得细粒度部件指引，又能保持全身协调。
primary_logic: 通过分阶段生成部件运动并将其作为引导信号融入整体运动解码过程，配合多样化的部件文本嵌入选择，可以打破单一整体框架的局限，同时提升部件表达性与连贯性。
claims:
- ParTY在部件对齐和连贯性上均优于传统整体方法和分部件方法（图1）。
- 在HumanML3D和KIT-ML上，ParTY在FID、R-Precision和MM-Dist指标上均超越所有对比方法（表1）。
- 在部分级评估中，ParTY的手臂和腿部R-Precision、FID和MM-Dist显著优于ParCo和MoMask（表2）。
- 在连贯性评估中，ParTY的时空连贯性得分（TC/SC）均高于对比方法（表3）。
---

# ParTY: Part-Guidance for Expressive Text-to-Motion Synthesis

> [!tip] 核心洞察
> 通过分阶段生成部件运动并将其作为引导信号融入整体运动解码过程，配合多样化的部件文本嵌入选择，可以打破单一整体框架的局限，同时提升部件表达性与连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | ParTY：面向表达性文本到动作合成的部件引导框架 |
| 英文题名 | ParTY: Part-Guidance for Expressive Text-to-Motion Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Heo_ParTY_Part-Guidance_for_Expressive_Text-to-Motion_Synthesis_CVPR_2026_paper.html) · [Project](https://visualsciencelab-khu.github.io/ParTY_project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ParTY |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID (↓) 0.035 vs 0.045 (MoMask) (-0.010 (-22.2%))；R-Precision Top-1 (↑) 0.550 vs 0.521 (MoMask) (+0.029 (+5.6%))；MM-Dist (↓) 2.779 vs 2.958 (MoMask) (-0.179 (-6.1%))。
> - KIT-ML 上，FID (↓) 0.155 vs 0.162 (ParCo) (-0.007 (-4.3%))。
> - HumanML3D (部件级-手臂) 上，R-Precision Top-1 (↑) 0.506 vs 0.454 (MoMask) (+0.052 (+11.5%))。

## 概要

文本到动作生成的核心挑战在于**部件级语义对齐**与**全身运动连贯性**之间的根本权衡。整体方法（如 **T2M** (Guo et al., CVPR 2022)、**MoMask** (Guo et al., CVPR 2024)）虽能保持较好的时空连贯性，却难以精准表达手臂、腿部等局部的细粒度语义；分部件方法（如 **AttT2M** (Zhong et al., ICCV 2023)、**ParCo** (Zou et al., arXiv 2024)）虽提升了部件对齐能力，却常以牺牲整体协调性为代价（见图1）。

**ParTY** 通过两项关键设计打破了这一权衡：

1. **部件引导生成网络（Part-Guided Network）**：采用两阶段策略，先生成手臂与腿部的运动令牌作为“引导信号”，再将其融入全身运动生成过程，使模型在获得细粒度部件指引的同时维持全身协调。
2. **部件感知文本接地（Part-aware Text Grounding）**：将单一文本嵌入通过多个MLP转化为多样化嵌入，并由部件门控机制为不同身体部位动态选择最适宜的语义表征，从而增强文本到部件的对齐精度。

在 **HumanML3D** 和 **KIT-ML** 两个标准数据集上，ParTY在FID、R-Precision和MM-Dist等指标上全面超越现有方法（表1）。尤其在部件级评估中，手臂R-Precision Top-1较MoMask提升11.5%，腿部较ParCo提升8.3%（表2）；同时，时空连贯性得分（TC/SC）亦优于对比方法（表3），验证了ParTY在**部件表达性**与**全身连贯性**两个维度上的双重优势。



文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用前景。该任务的核心挑战在于实现**细粒度语义对齐**与**全身运动连贯性**的双重要求：生成的动作既需要准确反映文本中描述的具体身体部件行为（如“左手挥手”或“右腿向前迈步”），又必须保持整体姿态的自然协调。

现有方法在处理这一权衡时存在根本性局限。**整体生成方法**（Holistic Methods）将人体运动视为单一整体进行建模，如 **T2M**（Guo et al., CVPR 2022）、**MoMask**（Guo et al., CVPR 2024）、**MMM**（Pinyoanuntapong et al., CVPR 2024）等，虽然能够较好地维持全身运动的时空连贯性，但由于缺乏对特定身体部件的显式关注，在部件级语义对齐上表现不足——例如，当文本描述涉及手臂和腿部的不同动作时，整体方法容易混淆或忽略部件细节。**分部件方法**（Part-wise Methods）则试图通过独立建模各身体部件来解决对齐问题，如 **AttT2M**（Zhong et al., ICCV 2023）利用部件级注意力机制、**ParCo**（Zou et al., arXiv 2024）采用部件协调策略。然而，这类方法在提升部件表达性的同时，往往以牺牲全身连贯性为代价，导致出现颈部扭曲、手臂与腿部动作不协调等伪影（Figure 1(b)）。

这一困境揭示了文本到运动生成领域的核心瓶颈：**部件级语义对齐与全身运动连贯性之间存在固有的权衡关系**，单一的整体框架或简单的分部件组合均无法同时满足两方面的需求。深入分析其因果机制可以发现，问题的关键在于生成过程中缺乏有效的**部件引导信号**——整体方法缺少细粒度的部件信息来约束局部动作，而分部件方法则缺少全局协调机制来融合独立生成的部件运动。此外，传统的文本嵌入利用方式仅依赖单一的全局语义表示，难以捕捉文本中针对不同身体部件的差异化描述，进一步限制了模型对复杂文本指令的解析能力。

针对上述问题，本文提出 **ParTY**（Part-Guidance for Expressive Text-to-Motion Synthesis），一种面向表达性文本到运动合成的部件引导框架。ParTY 的核心思路是通过**分阶段生成部件运动并将其作为引导信号融入整体运动解码过程**，配合**多样化的部件文本嵌入选择机制**，打破单一整体框架的局限，同时提升部件表达性与全身连贯性。具体而言，ParTY 包含两个关键创新：**部件引导网络**（Part-Guided Network）先生成手臂和腿部的运动令牌作为指引，再在整体运动生成过程中自适应融合这些部件信号；**部件感知文本接地**（Part-aware Text Grounding）则将单一文本嵌入转化为多个多样化嵌入，并为不同身体部件动态选择最适宜的语义表示。通过这一设计，ParTY 在部件对齐和连贯性上均超越了传统整体方法和分部件方法（Figure 1(c)），为文本到运动生成提供了一种新的解决范式。



## 核心方法与创新机理

ParTY 的核心创新在于打破现有方法在部件级语义对齐与全身运动连贯性之间的根本权衡。现有整体方法（如 **T2M** (Guo et al., CVPR 2022)、**MoMask** (Guo et al., CVPR 2024)）虽能维持良好的全身连贯性，但忽略部件细节，导致局部动作与文本描述的对齐不足；而分部件方法（如 **ParCo** (Zou et al., arXiv 2024)）虽增强了部件级文本对齐，却以牺牲整体协调性为代价，常出现颈部扭曲或四肢运动不匹配等问题（Figure 1）。ParTY 通过以下三个相互协同的 changed slots，同时实现了部件表达性与全身连贯性的显著提升。

**生成架构：从直接生成到两阶段部件引导。** 传统方法要么直接生成全身运动，要么独立生成各部件后简单组合。ParTY 提出 Part-Guided Network（Section 3.3），采用两阶段生成范式：首先由 Part Transformers 自回归生成手臂和腿部的运动令牌，并将其融合为部件引导向量 $\mathbf{G}_i$（Eq. 4, 5）；随后，Holistic Transformer 在生成全身运动令牌时，以 $\mathbf{G}_i$ 作为引导信号，并通过 Holistic-Part Fusion (HPF) 自适应融合部件令牌（Eq. 7–9）。这一设计使全身生成器既能获得细粒度的部件指引，又不会因独立生成而破坏全局协调性。消融实验证实，加入 Part Guidance (PG) 使 FID 从 0.063 降至 0.040，R-Precision Top-1 从 0.494 升至 0.520（Table 5）。

**文本嵌入利用：从单一全局嵌入到部件感知多样化嵌入。** 现有方法通常使用单一的全局文本嵌入来驱动整个运动生成，难以捕捉不同部件对文本语义的差异化需求。ParTY 的 Part-aware Text Grounding (PTG) 模块（Section 3.2）通过 $K$ 个 MLP 将单一文本嵌入 $\mathbf{c}$ 映射为 $K$ 个多样化嵌入 $\mathbf{c}_n'$，并利用对比学习损失 $\mathcal{L}_{\mathrm{div}}$ 鼓励嵌入多样性同时保持语义保真度（Eq. 3）。随后，部件门控机制动态地为手臂和腿部选择最适宜的嵌入。这一设计使模型能够根据不同部件的运动特性匹配最相关的文本语义。消融实验表明，PTG 使手臂 R-Precision Top-1 从 0.433 提高到 0.501，腿部从 0.298 提高到 0.337（Table 6）。

**运动量化中的时序信息保留：从普通 VQ-VAE 到时序感知 VQ-VAE。** 传统 VQ-VAE 按固定窗口量化运动序列，导致时序细节严重丢失。ParTY 提出的 Temporal-aware VQ-VAE（Section 3.1）引入局部时序增强 (LTE) 和全局时序增强 (GTE)：LTE 在窗口内对帧级特征进行加权求和（Eq. 1），GTE 则通过图卷积网络捕获组级特征间的全局时序依赖（Eq. 2）。该设计在不增加模型复杂度的前提下，显著提升了时序信息的保留能力。实验表明，在窗口大小为 12 时，时序感知 VQ-VAE 的 FID 仅为 0.011，相比普通 VQ-VAE 的 0.079 降低了 86%（Table 4）。



ParTY 的整体设计围绕一个核心矛盾展开：**如何在不牺牲全身运动连贯性的前提下，实现细粒度的部件级文本-运动对齐**。为此，框架采用“部件先行、整体融合”的两阶段生成范式，将部件运动作为显式引导信号注入全身运动生成过程。整个 pipeline 由四个关键模块串联构成，数据流从文本输入到最终运动序列的路径如图 3 所示。

**文本侧**，输入的文本描述首先经过 T5 编码器提取全局句子嵌入 $\mathbf{c}$。该嵌入并非直接送入生成器，而是进入 **Part-aware Text Grounding（PTG）** 模块：通过 $K$ 个并行的 MLP 将其变换为 $K$ 个多样化的文本嵌入 $\{\mathbf{c}_1', \dots, \mathbf{c}_K'\}$，再经由部件门控（part gating）机制为手臂和腿部各自动态选择最适配的嵌入。这一设计解决了单一全局嵌入无法同时描述不同部件动作的瓶颈。

**运动侧**，生成过程分为两条并行的令牌流。首先，**Part Transformers** 以自回归方式分别生成手臂和腿部的运动令牌序列 $\mathbf{z}^{\text{Arms}}$ 和 $\mathbf{z}^{\text{Legs}}$。这些部件令牌在每个生成周期 $i$ 内被融合为**部件引导向量** $\mathbf{G}_i$：
$$\mathbf{z}_{t}^{\text{fuse}} = \text{MLP}(\mathbf{z}_{t}^{\text{Arms}} + \mathbf{z}_{t}^{\text{Legs}}), \quad \mathbf{G}_i = \sum_{t \in t_i} \mathbf{z}_{t}^{\text{fuse}}$$
随后，**Holistic Transformer** 以原始文本嵌入 $\mathbf{c}$ 和部件引导 $\mathbf{G}_i$ 为条件，自回归生成全身运动令牌：
$$\mathbf{z}_t = f(\mathbf{z}_{1:t-1}, \mathbf{c}, \mathbf{G}_i)$$
在生成过程中，**Holistic-Part Fusion（HPF）** 模块通过交叉注意力机制，使全身令牌自适应地查询已生成的部件令牌，从而在保持整体连贯性的同时注入部件级细节。HPF 的输出由手臂和腿部两条交叉注意力结果相加得到。

**量化与重建**方面，所有运动令牌的离散化均依赖 **Temporal-aware VQ-VAE**。该 VQ-VAE 通过局部时序增强（LTE）和全局时序增强（GTE）保留帧间时序信息，避免了普通 VQ-VAE 按固定窗口量化导致的时序退化。全身 VQ-VAE 和部件 VQ-VAE 共享相同的时序增强架构，仅处理的数据范围不同（全身运动 vs. 部件运动）。

训练时，总损失由四部分加权组成：全身运动损失 $\mathcal{L}_{\text{hol}}$、部件运动损失 $\mathcal{L}_{\text{part}}$、文本多样性对比损失 $\mathcal{L}_{\text{div}}$ 以及辅助损失 $\mathcal{L}_{\text{aux}}$。推理时，只需提供文本描述，框架即可端到端地生成包含丰富部件表达且全身连贯的 3D 人体运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/003_Figure_3.jpg]]
*Figure 3: Overview of ParTY. Text embeddings are processed through Part-aware Text Grounding, then part transformers generate Part Guidance for the holistic transformer to generate motion tokens, with Holistic-Part Fusion applied during generation. The notation {Part} indicates that the process is performed for both arms and legs*



ParTY 围绕三个核心模块构建：**时序感知 VQ-VAE**（保留运动量化中的时序信息）、**部件感知文本接地 (PTG)**（生成多样化文本嵌入并为各部件动态选择）、以及**部件引导网络**（先生成部件运动令牌作为引导，再生成全身运动令牌并自适应融合）。以下逐一展开关键公式与机制。

---

### 时序感知 VQ-VAE

传统 VQ-VAE 按固定窗口对运动序列进行量化，导致帧间时序信息丢失。ParTY 提出**局部时序增强 (LTE)** 与**全局时序增强 (GTE)**，在不增加模型复杂度的前提下保留时序细节。

**局部时序增强 (LTE)** 将帧级特征按窗口大小 $w$ 分组，对每组内帧特征进行加权求和，得到增强的组级特征：

$$
\tilde{\mathcal{N}}_{i} = \sum_{j=1}^{w} \alpha_{ij} \cdot f_{ij}, \quad f_{ij} \in \mathcal{N}_{i}
$$

其中权重 $\alpha_{ij}$ 由 MLP 与 softmax 计算，使模型自适应地关注窗口内的重要帧。

**全局时序增强 (GTE)** 在组级特征之上构建图卷积网络，捕获跨窗口的长程时序依赖：

$$
\tilde{\mathcal{N}}_{i}^{\prime} = \mathrm{GELU}\left(\sum_{k=1}^{t/w} \hat{A}_{ik}(\tilde{\mathcal{N}}_{k} W)\right)
$$

$\hat{A}$ 为归一化邻接矩阵，$W$ 为可学习权重。GTE 使量化后的运动令牌仍保留全局时序结构。

VQ-VAE 总损失为重构损失与近似损失的加权和：

$$
\mathcal{L}_{vq} = \mathcal{L}_{rec} + \lambda_{app} \cdot \mathcal{L}_{app}
$$

其中 $\mathcal{L}_{rec}$ 为 L1 重构损失，$\mathcal{L}_{app}$ 为 L2 近似损失。部件 VQ-VAE 采用相同架构，仅处理部件级运动数据。

---

### 部件感知文本接地 (PTG)

单一全局文本嵌入难以同时描述手臂与腿部的细粒度运动。PTG 通过 $K$ 个 MLP 将同一句嵌入 $\mathbf{c}$ 映射为 $K$ 个多样化嵌入：

$$
\mathbf{c}_{n}^{\prime} = \mathrm{MLP}_{n}(\mathbf{c}), \quad n \in \{1, \dots, K\}
$$

为鼓励嵌入多样性且不丢失语义，引入**文本多样性损失**——一种对比学习目标：

$$
\mathcal{L}_{\mathrm{div}} = \frac{1}{K} \sum_{n=1}^{K} \mathcal{L}^{(n)}, \quad
\mathcal{L}^{(n)} = -\log \frac{\exp(\mathrm{s}(\mathbf{c}_{n}^{\prime}, \mathbf{c})/\tau)}{\exp(\mathrm{s}(\mathbf{c}_{n}^{\prime}, \mathbf{c})/\tau) + \sum_{m\neq n}^{K} \exp(\mathrm{s}(\mathbf{c}_{n}^{\prime}, \mathbf{c}_{m}^{\prime})/\tau)}
$$

其中 $\mathrm{s}(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数。该损失使每个 $\mathbf{c}_{n}^{\prime}$ 与原始嵌入 $\mathbf{c}$ 保持语义一致，同时彼此差异最大化。

随后，**部件门控** 动态为手臂和腿部选择最适宜的嵌入，使不同部件获得差异化的文本指引。

---

### 部件引导网络

部件引导网络是 ParTY 的核心生成架构，包含三个子模块：部件 Transformer、部件引导融合、整体 Transformer 与整体-部件融合 (HPF)。

**部件 Transformer** 自回归生成手臂与腿部运动令牌。**部件引导融合** 将第 $i$ 个生成周期的手臂和腿部令牌融合为引导向量：

$$
\mathbf{z}_{t}^{\mathrm{fuse}} = \mathbf{MLP}(\mathbf{z}_{t}^{\mathrm{Arms}} + \mathbf{z}_{t}^{\mathrm{Legs}}), \quad
\mathbf{G}_{i} = \sum_{t \in t_{i}} \mathbf{z}_{t}^{\mathrm{fuse}}
$$

**整体 Transformer** 以原始文本嵌入 $\mathbf{c}$、先前全身令牌 $\mathbf{z}_{1:t-1}$ 及部件引导 $\mathbf{G}_{i}$ 为条件，生成当前全身运动令牌：

$$
\mathbf{z}_{t} = f(\mathbf{z}_{1:t-1}, \mathbf{c}, \mathbf{G}_{i})
$$

**整体-部件交叉注意力 (HPF)** 在生成过程中自适应融合部件级信息：以全身特征为 Query，分别查询手臂和腿部令牌，输出相加：

$$
\mathbf{z}_{\mathrm{cross}}^{\mathrm{p}} = \mathrm{Attn}(\mathbf{Q}^{\prime}, \mathbf{K}_{\mathrm{p}}, \mathbf{V}_{\mathrm{p}}), \quad p \in \{\mathrm{Arms}, \mathrm{Legs}\}
$$

最终总损失结合整体运动损失、部件运动损失、文本多样性损失及辅助损失：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{hol}} + \mathcal{L}_{\mathrm{part}} + \lambda_{\mathrm{div}} \mathcal{L}_{\mathrm{div}} + \lambda_{\mathrm{aux}} \mathcal{L}_{\mathrm{aux}}
$$

其中 $\mathcal{L}_{\mathrm{hol}}$ 和 $\mathcal{L}_{\mathrm{part}}$ 均为负对数似然损失，分别监督全身与部件运动令牌的分布。

---

**关键机制总结**：PTG 提供多样化的部件级文本嵌入，部件 Transformer 生成细粒度部件运动令牌作为引导信号，HPF 在全身生成过程中自适应融合部件信息——三者协同，打破了部件语义对齐与全身连贯性之间的根本权衡。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of the Temporal-aware VQ-VAE. Part VQ-VAE follows an identical architecture, where the sole distinction lies in processing part-level rather than full-body motion data*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/009_Figure_5.jpg]]
*Figure 5: Visualization of cross attention map of HPF. Rows correspond to body parts and columns represent temporal frames. We visualize the normalized attention weights between the holistic motion token and each part motion token*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/012_Figure_6.jpg]]
*Figure 6: Embedding selection ratios in PTG. Mean and standard deviation of weights are computed over semantically similar text descriptions that share common motion patterns*



## 实验与关键发现

### 核心定量结果

ParTY 在两个主流文本-动作数据集 HumanML3D 和 KIT-ML 上均取得最优性能，验证了部件引导生成框架的有效性。表 1 报告了与整体生成方法和分部件方法的全面比较。

在 HumanML3D 上，ParTY 的 FID 降至 **0.035**，相比此前最优的整体方法 MoMask（0.045）降低 22.2%，相比分部件方法 ParCo（0.042）降低 16.7%。R-Precision Top-1 达到 **0.550**，分别超越 MoMask（0.521）和 ParCo（0.515）5.6% 和 6.8%。MM-Dist 降至 **2.779**，优于所有对比方法。在 KIT-ML 上，ParTY 同样取得最优 FID（0.155）和 R-Precision Top-1（0.456），验证了方法的跨数据集泛化能力。

值得注意的是，ParTY 在 Diversity 和 Multimodality 指标上同样保持竞争力，表明部件引导机制并未牺牲生成动作的多样性和多模态性。所有实验均进行 20 次运行（Multimodality 为 5 次），报告平均值及 95% 置信区间，统计可靠性得到充分保障。

### 部件级评估

为直接衡量部件-文本对齐质量，论文新提出了部件级评估协议，将 R-Precision、FID 和 MM-Dist 分别应用于手臂和腿部动作。表 2 的结果揭示了 ParTY 在细粒度语义对齐上的显著优势。

在手臂 R-Precision Top-1 上，ParTY 达到 **0.506**，相比 MoMask（0.454）提升 11.5%，相比 ParCo（0.468）提升 8.1%。腿部 R-Precision Top-1 为 **0.366**，优于 ParCo（0.338）和 MoMask（0.330）。手臂和腿部的 FID 和 MM-Dist 同样全面领先，表明 Part-aware Text Grounding 和 Part Guidance 机制有效捕捉了文本中针对特定身体部位的语义信息，并将其转化为准确的部件运动。

### 连贯性评估

部件级表达性的提升通常以全身连贯性为代价——分部件方法 ParCo 的 Temporal Coherence（TC）仅为 0.82，低于整体方法 MoMask 的 0.85。ParTY 通过 Holistic-Part Fusion 机制打破了这一权衡：其 TC 达到 **0.88**，Spatial Coherence（SC）达到 **0.84**，均显著优于所有对比方法（表 3）。

图 4 的定性可视化进一步印证了这一结论。在“左腿弓步，右手举过头顶”等复杂描述下，整体方法往往忽略手部细节，分部件方法则出现颈部扭曲和四肢不协调，而 ParTY 同时实现了准确的部件语义执行和流畅的全身运动。

### 消融实验

**组件贡献分析（表 5、表 6）。** 以移除所有新增模块的基线（仅使用整体 Transformer 和普通 VQ-VAE）为起点，逐步添加 Part Guidance（PG）、Part-aware Text Grounding（PTG）和 Temporal-aware VQ-VAE。

- 加入 PG 后，FID 从 0.063 降至 **0.040**，R-Precision Top-1 从 0.494 升至 **0.520**，验证了部件引导信号对整体生成质量的关键作用。
- 进一步加入 PTG 后，手臂 R-Precision Top-1 从 0.433 跃升至 **0.501**，腿部从 0.298 升至 **0.337**（表 6），证明多样化文本嵌入和部件门控机制是部件级语义对齐的核心驱动力。
- 完整模型（含 Temporal-aware VQ-VAE）达到最优 FID（0.035）和 R-Precision（0.550），表明时序感知量化与部件引导存在协同效应。

**时序感知 VQ-VAE 的迁移验证（表 4）。** 将 Temporal-aware VQ-VAE 迁移至 MoMask 框架，在窗口大小 w=12 时，重建 FID 从普通 VQ-VAE 的 0.079 降至 **0.011**（降低 86%），最终生成 FID 从 0.045 降至 0.040。同时，MPJPE 从 42.3mm 降至 32.1mm，平均推理时间仅增加 0.08 秒。这表明时序增强模块具有通用价值，可在不显著增加计算开销的前提下提升现有方法的运动重建精度。

**PTG 嵌入选择分析（图 6）。** 可视化结果显示，不同 MLP 生成的多样化嵌入在语义相似文本上呈现一致的权重分布模式，手臂和腿部各自偏好不同的嵌入子集。这从机制层面解释了 PTG 如何实现部件级语义解耦——模型学会了为不同身体部位动态选择最相关的文本表示，而非依赖单一全局嵌入。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/001_Figure_1.jpg]]
*Figure 1: (a) Holistic methods maintain coherence well but limited part-text alignment. In contrast, (b) Part-wise methods show enhanced part-text alignment (e.g., correctly performing the left leg lunge) but compromised coherence as a trade-off (e.g., neck distortion and misaligned arm and leg movements). (c) Our ParTY resolves this trade-off by achieving superior performance in both part-text alignment and coherence*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on HumanML3D and KIT-ML. Bold indicates the best result, while underlined refers the second-best. The right arrow → indicates that closer values to ground truth are preferred*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison with part-level evaluation metrics on HumanML3D*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison with coherence-level (TC, SC) scores on HumanML3D. We run each evaluation 20 times and report averages with 95% confidence intervals*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/010_Table_5.jpg]]
*Table 5: Ablation studies of the proposed components. PG indicates Part Guidance*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/011_Table_6.jpg]]
*Table 6: Ablation studies with part-level evaluation metrics*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/008_Table_4.jpg]]
*Table 4: Porting Temporal-aware VQ-VAE to MoMask [12]. Reconstruction evaluates VQ-VAE performance, while Generation evaluates final performance including the transformer. Mean Per Joint Position Error (MPJPE) measures positional accuracy, and Average Inference Time (AIT) is averaged over 100 samples on an RTX A5000 GPU*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Heo_ParTY_Part_Guidanc/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on HumanML3D. Colored text in the descriptions corresponds to the colored body parts in the generated motions, with coherence-level (TC, SC) scores displayed for each sample*



## 定位与知识库关联

### 生成范式对比：整体 vs. 分部件 vs. 部件引导

文本到动作生成领域存在两种主流范式及其固有权衡。**整体方法**（Holistic）直接生成全身运动，以 **T2M**（Guo et al., CVPR 2022）、**MoMask**（Guo et al., CVPR 2024）、**MMM**（Pinyoanuntapong et al., CVPR 2024）和 **BAMM** 为代表。这类方法通过单一全局文本嵌入驱动生成，能较好维持全身运动的时空连贯性，但对细粒度部件级语义（如“左手叉腰，右腿弓步”）的响应能力不足——文本嵌入中的部件信息在全局编码过程中被稀释，导致部件-文本对齐度受限（Figure 1a）。

**分部件方法**（Part-wise）将身体拆分为手臂、腿部等独立组件分别生成再组合，以 **AttT2M**（Zhong et al., ICCV 2023）和 **ParCo**（Zou et al., arXiv 2024）为代表。这类方法通过为各部件分配专用生成模块，显著提升了部件-文本对齐精度（Figure 1b），但付出了连贯性代价：独立生成的部件之间缺乏全局协调机制，容易出现颈部扭曲、手臂与腿部运动失配等伪影。

**ParTY** 的核心突破在于打破上述“对齐-连贯”权衡。其部件引导网络（Part-Guided Network）采用两阶段生成策略：先生成手臂和腿部运动令牌作为部件引导信号，再将此信号注入整体运动令牌的自回归生成过程（Eq. 7），通过整体-部件融合（Holistic-Part Fusion, HPF）自适应地整合部件信息。这一设计使得 ParTY 同时继承了整体方法的连贯性优势和分部件方法的细粒度对齐能力，在 HumanML3D 上实现了 FID 0.035（较 MoMask 的 0.045 降低 22.2%）和 R-Precision Top-1 0.550（较 MoMask 提升 5.6%）的双重领先（Table 1）。

### 文本嵌入策略演进：从单一到多样化部件感知

传统方法（T2M、MoMask 等）使用单一全局文本嵌入，无法为不同身体部件提供差异化语义指引。AttT2M 通过注意力机制让各部件关注文本的不同部分，但本质上仍共享同一嵌入空间。ParTY 的部件感知文本接地（Part-aware Text Grounding, PTG）则引入 K 个 MLP 将单一嵌入扩展为多样化嵌入集合，并通过对比学习损失 $\mathcal{L}_{\mathrm{div}}$（Eq. 3）保证嵌入间的语义多样性。在此基础上，部件门控机制动态为手臂和腿部选择最适配的嵌入，实现了从“一对多”到“多对多”的文本-部件映射升级。消融实验证实，PTG 使手臂 R-Precision Top-1 从 0.433 提升至 0.501，腿部从 0.298 提升至 0.337（Table 6），验证了多样化文本嵌入对部件级语义对齐的关键作用。

### 运动量化的时序增强

现有 VQ-VAE 按固定窗口量化运动序列，窗口内帧级特征被简单聚合，导致细粒度时序信息丢失。ParTY 的时序感知 VQ-VAE 通过局部时序增强（LTE, Eq. 1）和全局时序增强（GTE, Eq. 2）双层机制保留时序依赖：LTE 在窗口内对帧级特征加权求和，GTE 则通过图卷积网络建模跨窗口的全局时序关系。将此时序感知 VQ-VAE 迁移至 MoMask 后，在窗口大小为 12 时 FID 从 0.079 降至 0.011（降低 86%，Table 4），证明了该模块的通用价值。

### 适用边界与局限

ParTY 在 HumanML3D 和 KIT-ML 两个标准基准上验证了有效性，但其部件划分目前仅覆盖手臂和腿部，躯干和头部未纳入部件引导框架。此外，PTG 的嵌入多样性依赖于 K 个 MLP 的对比学习，K 值的选取对性能的影响尚未充分探索。时空连贯性度量（TC/SC）虽为针对性评估提供了有效手段，但目前仅在 HumanML3D 上计算参考统计量，跨数据集的泛化性需要进一步验证。

### 开放问题

1. **部件粒度扩展**：将部件引导扩展至手指、面部表情等更细粒度单元，是否能进一步提升表达性动作生成质量？
2. **文本嵌入数量的自适应选择**：当前 K 为固定超参数，能否根据输入文本的语义复杂度动态调整嵌入数量？
3. **跨域迁移**：部件引导框架在舞蹈生成、手语合成等需要强部件协调性的领域是否同样有效？



## 原文 PDF

![[paperPDFs/CVPR_2026/ParTY_Part_Guidance_for_Expressive_Text_to_Motion_Synthesis.pdf]]

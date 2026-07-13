---
title: "UARE: A Unified Vision-Language Model for Image Quality Assessment, Restoration, and Enhancement"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UARE_A_Unified_Vision_Language_Model_for_Image_Quality_Assessment_Restoration_and_Enhancement.pdf
project_link: null
code_link: "https://github.com/lwq20020127/UARE"
aliases:
- UARE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过联合训练 IQA 和恢复专家，并让恢复过程可利用 IQA 生成的文本质量分析，从而将质量信号注入生成过程。
primary_logic: 多任务协同训练中，IQA 能力可以显著提升恢复图像的感知质量，同时保持保真度，实现恢复与评估互相促进。
claims:
- 引入 IQA 数据联合微调 IQA 和恢复专家可显著提升感知质量指标（如 MUSIQ、MANIQA），同时保真度指标（PSNR）基本维持不变。
- 在 RealSR 数据集上，UARE 的 MUSIQ 达到 69.67，MANIQA 达到 0.5260，远超基线（如仅用高阶退化的变体：MUSIQ 57.50，MANIQA 0.3760）。
- UARE 的“分析-然后-恢复”范式使其能有效利用自身 IQA 分析，而外部 Q-Insight 提示则效果较差，证明模型内部对齐的优越性。
- RealSR 上 MUSIQ = 69.67
---

# UARE: A Unified Vision-Language Model for Image Quality Assessment, Restoration, and Enhancement

> [!tip] 核心洞察
> 多任务协同训练中，IQA 能力可以显著提升恢复图像的感知质量，同时保持保真度，实现恢复与评估互相促进。

| 字段 | 内容 |
|------|------|
| 中文题名 | UARE: 面向图像质量评估、复原与增强的统一视觉-语言模型 |
| 英文题名 | UARE: A Unified Vision-Language Model for Image Quality Assessment, Restoration, and Enhancement |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.06750) · [Code](https://github.com/lwq20020127/UARE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UARE |
| Dataset | RealSR, DIV2K, FoundIR, KADID |

> [!tip] 效果简介
> - RealSR 上，MUSIQ 69.67 vs OSEDiff 68.95 (+0.72)。
> - DIV2K 上，MUSIQ 70.45 vs PURE 70.06 / S3Diff 69.31 (+0.39 / +1.14)。
> - FoundIR (Blur+Noise) 上，LPIPS 0.1573 vs DiffUIR 0.1871 (-0.0298)。

## 概要

图像质量评估（IQA）与图像恢复/增强长期作为两个独立领域发展：前者负责诊断失真，后者负责修复图像，但二者始终缺乏有效的统一。这种割裂导致恢复过程难以利用质量信号进行精准引导，而评估模型也无法从恢复反馈中获得改进。UARE 针对这一瓶颈，提出首个统一视觉-语言模型，将 IQA 与恢复/增强整合到单一框架中。

其核心思路可概括为“分析-然后-恢复”：模型首先生成对当前图像质量的文本分析，再基于该分析执行恢复，从而将质量信号注入生成过程。技术上，UARE 采用双专家混合Transformer（Mixture-of-Transformers, MoT）架构，包含一个 IQA 专家和一个恢复专家，二者共享自注意力层；训练采用两阶段策略——先通过由易到难的渐进式退化预训练恢复能力，再联合微调 IQA 与恢复专家，使质量评估与恢复目标对齐。

实验表明，这一设计带来了显著的感知质量提升，同时基本维持保真度。在 RealSR 数据集上，UARE 的 MUSIQ 达到 69.67，MANIQA 达到 0.5260，远超仅使用高阶退化训练的变体（MUSIQ 57.50，MANIQA 0.3760）；在 DIV2K 上，MUSIQ 达到 70.45，优于 PURE（70.06）和 S3Diff（69.31）。在多退化场景 FoundIR 上，UARE 在 LPIPS 和 NIQE 指标上同样表现出竞争力。此外，UARE 在 IQA 任务上也取得了与专用模型可比的结果（如 KADID 上 PLCC 0.878，CSIQ 上 PLCC 0.930），验证了统一模型的可行性。

方法定位上，UARE 区别于仅关注恢复的模型（如 StableSR、DiffBIR、SeeSR、OSEDiff）和仅关注评估的模型（如 Q-Align、DeQA-Score），也与近期尝试统一 IQA 与恢复的 PURE 不同——UARE 通过结构化的“分析-恢复”交错数据和联合训练，实现了更紧密的 IQA-恢复对齐。消融实验进一步证实，仅使用简单指令训练而缺少结构化分析-恢复数据，感知指标显著下降；使用外部 Q-Insight 提示也无法达到 UARE 内部对齐的效果。

主要局限在于训练资源需求极高（64 块 NVIDIA H20 GPU 训练一周），且当前仅探索了 IQA 提升恢复的单向关系，恢复如何反过来改进 IQA 仍待研究。



### 问题域：图像质量评估与恢复的长期割裂

图像质量评估（Image Quality Assessment, IQA）与图像恢复/增强（Image Restoration/Enhancement）是计算机视觉中高度互补的两个领域。IQA 旨在量化或描述图像的感知质量，而恢复/增强则致力于从退化图像中重建高质量输出。然而，这两个领域长期独立发展：IQA 方法通常作为离线评估工具存在，恢复网络则依赖固定的损失函数（如 L1、LPIPS）进行优化，缺乏对感知质量信号的动态利用。这种割裂导致一个关键瓶颈——**恢复过程无法利用质量评估的语义级反馈来指导生成**，使得恢复图像的感知质量提升受限于预定义的损失函数。

### 现有方法的缺口

现有统一框架的尝试存在明显局限。**PURE**（Wei et al., ICCV 2025）虽然尝试将 IQA 与恢复结合，但其 IQA 能力与恢复过程之间缺乏深层对齐，质量信号未能有效转化为恢复增益。另一方面，基于扩散模型的恢复方法（如 **StableSR** (Wang et al., IJCV 2024)、**DiffBIR** (Xia et al., CVPR 2023)、**SeeSR** (Wu et al., CVPR 2024)、**OSEDiff** (Wu et al., NeurIPS 2024)）在感知质量上取得了进展，但它们本质上是纯恢复模型，不具备 IQA 能力，无法形成“评估-恢复”的闭环。在 IQA 侧，**Q-Align**（Wu et al., ICML 2024）和 **DeQA-Score**（You et al., CVPR 2025）等模型专注于评分预测，而 **Q-Insight** 虽能生成质量描述，但这些 IQA 模型与恢复模型之间没有共享的表征空间或训练目标，导致 IQA 分析无法直接驱动恢复过程。

### 核心动机：将质量信号注入生成过程

本文的核心动机是打破上述割裂，构建一个统一的视觉-语言模型，使得 IQA 和恢复能够互相促进。关键洞察在于：**如果 IQA 能力与恢复能力在同一个模型内通过联合训练对齐，IQA 生成的文本质量分析就可以作为条件信号注入恢复过程，从而显著提升恢复图像的感知质量，同时保持保真度**。这一假设在后续消融实验中得到验证——引入 IQA 数据联合微调后，UARE 在 RealSR 上的 MUSIQ 从 57.50 跃升至 69.67，MANIQA 从 0.3760 提升至 0.5260，而 PSNR 基本维持不变（Table 4）。此外，UARE 的“分析-然后-恢复”范式使其能有效利用自身 IQA 分析，而外部 Q-Insight 提示则效果较差，证明模型内部对齐的优越性。

基于以上动机，UARE 被设计为**首个面向图像质量评估、复原与增强的统一视觉-语言模型**，通过双专家 MoT 架构和两阶段训练框架，实现 IQA 与恢复的深度协同。



## 核心方法与创新机理

UARE 的核心创新在于首次将图像质量评估（IQA）与图像复原/增强统一于一个视觉-语言模型框架中，并通过**双专家混合Transformer（Mixture-of-Transformers, MoT）架构**和**两阶段渐进式训练策略**，实现了质量评估信号对恢复过程的有效引导。

### 架构创新：双专家 MoT 设计

传统方法通常采用单一恢复网络处理退化图像（如 **StableSR** (Wang et al., IJCV 2024)、**DiffBIR** (Xia et al., CVPR 2023) 等），而 UARE 采用 MoT 架构，包含两个全容量专家：

- **IQA 专家**：接收文本分词器产生的文本标记和理解视觉编码器产生的图像标记，负责生成质量分析文本（评分、描述、对比）。
- **恢复专家**：接收 VAE 潜在空间标记，负责生成恢复后的图像。

两个专家共享自注意力层，使得 IQA 分析过程中提取的退化特征能够隐式地影响恢复过程。这一设计的关键在于，恢复专家并非孤立地处理退化图像，而是可以通过共享的注意力机制“感知”到 IQA 专家对图像质量的细粒度分析，从而将质量信号注入生成过程。

### 训练策略创新：两阶段渐进式训练

UARE 的训练流程从传统的单阶段恢复训练转变为两阶段框架，这是实现 IQA 与恢复协同的关键：

**第一阶段：由易到难的恢复预训练。** 恢复专家按照“单退化 → 多退化 → 高阶退化”的渐进课程进行训练，逐步提升模型对复杂退化的处理能力。此阶段仅使用 rectified flow 损失 $\mathcal{L}_{RF}$ 训练恢复专家，使模型具备处理多种退化类型的基础能力。

**第二阶段：IQA 与恢复联合微调。** 引入 IQA 数据，同时更新 IQA 专家和恢复专家（除 VAE 和文本分词器外），联合优化目标为：
$$\mathcal{L}_{s2} = \mathcal{L}_{RF} + \lambda\mathcal{L}_{AR}, \quad \lambda=0.25$$
其中 $\mathcal{L}_{AR}$ 为自回归文本预测损失，仅应用于 IQA 响应的 token。这一阶段的消融实验（Table 4）给出了决定性证据：加入 IQA 联合微调后，RealSR 上的 MUSIQ 从 57.50 跃升至 69.67，MANIQA 从 0.3760 提升至 0.5260，而保真度指标 PSNR 基本维持不变（从 24.46 微降至 24.44），验证了“引入 IQA 数据联合微调可显著提升感知质量，同时保持保真度”的核心论断。

### 数据构造创新：结构化“分析-恢复”交错数据

与简单指令-图像对（如“enhance this image”）不同，UARE 在第二阶段使用面向“分析-然后-恢复”范式的交错文本-图像数据，输出遵循四步结构：
1. 用户意图
2. 当前质量分析
3. 增强计划
4. 预期结果

消融实验（Table 5）表明，仅使用简单指令训练而缺少结构化分析-恢复数据时，感知指标显著下降，且外部 Q-Insight 提示的效果远不如 UARE 自身对齐的 IQA 分析，证明模型内部对齐的优越性——这是“分析-然后-恢复”范式有效性的直接证据。

### 与相关工作的本质区别

与最近的统一尝试 **PURE** (Wei et al., ICCV 2025) 相比，UARE 的核心差异在于：PURE 将 IQA 作为辅助任务嵌入恢复网络，而 UARE 通过双专家架构和结构化交错数据，使 IQA 分析显式地参与恢复决策，实现了更深的评估-恢复协同。这一设计使得 UARE 在 RealSR 上以 MUSIQ 69.67 超越 PURE 的 70.06（DIV2K 上）等强基线，同时在多退化场景（FoundIR）上展现出全面的感知-保真度平衡优势。



UARE 的整体设计遵循“分析-然后-恢复”（analyze-then-restore）范式，将图像质量评估（IQA）与图像复原/增强统一于单一模型之中。其核心架构基于 **Mixture-of-Transformers (MoT)** 设计，包含两个全容量专家模块：**IQA 专家**和**恢复专家**（Restoration Expert），二者共享自注意力层以实现信息交互，但各自拥有独立的前馈网络参数。

### 模块组成与数据流

如图 2 所示，UARE 的推理流程分为理解与生成两条路径：

1. **理解路径（IQA 专家）**：输入图像首先经过**理解视觉编码器**（Understanding Visual Encoder）编码为图像 token，同时用户指令经**文本分词器**（Text Tokenizer）转换为文本 token；两者拼接后送入 IQA 专家，生成结构化的质量分析文本，包括当前质量描述、增强计划与预期结果。
2. **生成路径（恢复专家）**：低质量图像经 **VAE** 编码为潜在空间 token，恢复专家在条件信号（来自 IQA 分析文本及原始图像上下文）的引导下，通过 rectified flow 扩散过程生成恢复后的图像潜在表示，再由 VAE 解码器重建为高质量输出图像。

### 两阶段训练框架

UARE 采用两阶段训练策略，逐步赋予模型多退化处理能力与质量感知恢复能力：

- **第一阶段：渐进式由易到难恢复预训练**。仅训练恢复专家，按照退化复杂度递增的顺序进行：首先在单一退化类型（如模糊、噪声、低光照）上训练，随后扩展到多重退化组合，最后处理高阶混合退化。该阶段仅使用 rectified flow 损失 $\mathcal{L}_{s1} = \mathcal{L}_{RF}$，目的是让模型掌握多场景下的图像复原能力。
- **第二阶段：IQA 与恢复联合微调**。解冻 IQA 专家，同时更新除 VAE 和文本分词器外的所有参数。训练数据采用交错文本-图像格式，输出文本遵循四步结构：（1）用户意图识别，（2）当前质量分析，（3）增强计划，（4）预期结果。联合损失为 $\mathcal{L}_{s2} = \mathcal{L}_{RF} + \lambda \mathcal{L}_{AR}$，其中 $\lambda = 0.25$，$\mathcal{L}_{AR}$ 为作用于响应 token 的自回归最大似然损失，$\mathcal{L}_{RF}$ 为 rectified flow 目标。此阶段的关键作用在于将 IQA 生成的质量信号显式对齐到恢复过程中，使模型能够利用自身的质量分析来指导图像生成。

### 关键设计决策

- **内部对齐优于外部提示**：消融实验（Table 5）表明，使用外部 IQA 模型（如 Q-Insight）的文本提示来引导恢复，效果远不如 UARE 自身 IQA 专家生成的分析。这验证了联合微调使 IQA 与恢复能力在模型内部达成有效对齐，从而将质量洞察转化为具体的恢复增益。
- **结构化输出格式**：四步输出结构不仅使模型具备可解释的质量分析能力，也为恢复专家提供了丰富的条件信号，是“分析-恢复”协同的关键纽带。

### 补充图表

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/004_Figure_2.jpg]]
*Figure 2: Illustration of the architecture and two-stage training framework of UARE. Two transformer experts are used to process IQA and restoration, respectively. Training stages include (1) a progressive, easy-to-hard schedule that moves from single-type to high-order degradations. In this stage, only the restoration expert is trained to make UARE handle multiple degradations. (2) Unified fine-tuning of the entire model to strengthen the IQA ability and align the IQA signals with restoration objectives through interleaved data*



### 双专家混合Transformer架构

UARE 基于混合Transformer（Mixture-of-Transformers, MoT）设计，核心思想是将图像质量评估与图像恢复两个任务解耦到两个独立的全容量专家模块中，同时共享自注意力层以实现跨任务信息交互：

- **IQA 专家**：接收来自文本分词器的文本标记和来自理解视觉编码器的图像标记，负责生成质量分析文本（包括质量描述、评分和图像对比）。
- **恢复专家**：接收来自 VAE 编码器的潜在空间标记，负责生成恢复后的图像。

这种双专家设计使得模型能够分别处理理解与生成两种异质任务，同时通过共享的自注意力机制实现 IQA 分析信号向恢复过程的传递。

### 两阶段训练框架

训练分为两个阶段，目标函数逐步叠加：

**第一阶段：渐进式由易到难恢复预训练**

仅训练恢复专家，采用从单退化→多退化→高阶退化的渐进式课程学习策略。该阶段仅使用 rectified flow 损失：

$$\mathcal{L}_{s1} = \mathcal{L}_{RF}$$

其中 rectified flow 损失定义为：

$$\mathcal{L}_{RF}(\theta) = \mathbb{E}_{\mathbf{x}\sim\mathcal{D}_{\mathrm{res}},\mathbf{z}_{0}\sim\mathcal{N}(0,\mathbf{I})}\big[\|v_{\theta}(\mathbf{z}_{t},t|\mathbf{x}_{\mathrm{con}})-(\mathbf{x}_{\mathrm{res}}-\mathbf{z}_{0})\|^{2}\big]$$

这里 $\mathbf{z}_t = t\mathbf{x}_{\mathrm{res}} + (1-t)\mathbf{z}_0$ 为插值后的潜在表示，$v_{\theta}$ 为速度预测网络，$\mathbf{x}_{\mathrm{res}}$ 为目标恢复图像，$\mathbf{x}_{\mathrm{con}}$ 为条件输入（退化图像），$\mathbf{z}_0$ 为标准高斯噪声。该损失使模型学习从噪声到目标图像的直线传输路径。

**第二阶段：IQA 与恢复联合微调**

解冻全部可训练参数（VAE 和文本分词器除外），同时优化 IQA 和恢复任务。IQA 任务采用自回归损失，仅应用于响应 token 部分：

$$\mathcal{L}_{AR}(\theta) = -\mathbb{E}_{\mathbf{x}\sim\mathcal{D}_{\mathrm{IQA}}}\Big[\sum_{i=l_{\mathrm{con}}}^{l-1}\log\mathrm{P}_{\theta}(\mathbf{x}_{i+1}|\mathbf{x}_{1},...,\mathbf{x}_{i})\Big]$$

其中 $l_{\mathrm{con}}$ 为条件 token 长度，$l$ 为序列总长度，模型仅对响应部分的 token 计算最大似然损失。

第二阶段联合损失为两者的加权组合：

$$\mathcal{L}_{s2} = \mathcal{L}_{RF} + \lambda\mathcal{L}_{AR}$$

其中 $\lambda = 0.25$，在所有实验中保持不变。该权重设置使得恢复任务仍为主导，IQA 信号作为辅助引导注入生成过程，实现“分析-然后-恢复”的协同优化。

### 数据构造中的结构化输出

与上述损失函数配合，第二阶段使用的交错文本-图像数据采用四步结构化输出格式：（1）用户意图识别；（2）当前质量分析；（3）增强计划；（4）预期结果描述。这种结构化设计使得 IQA 专家生成的质量分析能够被恢复专家有效利用，形成内部对齐的质量引导信号——论文消融实验证实，使用外部 Q-Insight 提示替代自身 IQA 分析时效果显著下降，证明了模型内部对齐的优越性。



## 实验与关键发现

### 1. 实验设置概览

UARE 基于 Mixture-of-Transformers（MoT）架构，包含 IQA 专家和恢复专家两个全容量 Transformer 模块，共享自注意力层。训练分两阶段进行：

- **阶段一：渐进式恢复预训练。** 采用由易到难的课程学习策略，依次在单退化、多退化和高阶退化数据上训练恢复专家，损失函数仅使用 rectified flow 损失 $\mathcal{L}_{s1} = \mathcal{L}_{RF}$。训练规模为：单退化 9.6B 图像 token，多退化 19.2B 图像 token，高阶退化 1.3B 图像 token。
- **阶段二：IQA 与恢复联合微调。** 更新除 VAE 和 text tokenizer 外的全部参数，联合优化 $\mathcal{L}_{s2} = \mathcal{L}_{RF} + \lambda\mathcal{L}_{AR}$，其中 $\lambda=0.25$。该阶段使用 0.4B IQA 文本 token 和 4.6B 图像 token。

高阶退化数据遵循 RealESRGAN 和 APISR 的退化流程，应用于 LSDIR 和 FoundIR 的高质量图像。训练使用 64 块 NVIDIA H20 GPU，持续约一周。

### 2. 超分辨率任务主结果

Table 1 展示了在 RealSR、DRealSR 和 DIV2K 三个基准上的定量比较。UARE 在感知质量指标上表现突出：

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of different SR methods on RealSR, DRealSR, and DIV2K. Throughout this paper, best, second-best, and third-best results are highlighted in bold red, underlined blue, italic green. ↑ / ↓ indicates higher/lower is better*

- **RealSR：** MUSIQ 达到 69.67，超过 OSEDiff（68.95）和 S3Diff（67.57）；MANIQA 达到 0.5260，显著优于其他方法。保真度指标方面，PSNR 为 24.53，与 SeeSR（24.59）和 OSEDiff（24.93）接近。
- **DIV2K：** MUSIQ 达到 70.45，超过 PURE（70.06）和 S3Diff（69.31）；LPIPS 为 0.2098，优于 DiffBIR（0.2283）和 StableSR（0.2337）。
- **DRealSR：** MUSIQ 为 65.97，仅次于 OSEDiff（66.77），但 MANIQA 达到 0.5072，为所有方法中最高。

关键观察：UARE 在保持保真度（PSNR）基本不降的前提下，显著提升了感知质量（MUSIQ、MANIQA），验证了“分析-然后-恢复”范式的有效性。

### 3. 多退化恢复主结果

Table 2 报告了在 FoundIR 九个多退化子集上的结果。每行第一行为 PSNR/LPIPS，第二行为 NIQE/MANIQA。核心发现：

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on nine multi-degradation subsets of FoundIR. For each method, the first row lists PSNR/LPIPS and the second row lists NIQE/MANIQA. Note that B., N., J., L., and H. denote Blur, Noise, JPEG compression, Low-light, and Haze, respectively*

- **Blur+Noise 子集：** LPIPS 为 0.1573，优于 DiffUIR（0.1871）和 FoundIR（0.1624）；PSNR 为 25.16，与 FoundIR（25.16）持平。
- **Low-light+Noise+JPEG 子集：** NIQE 为 4.5995，优于 FoundIR（4.9494）和 DiffUIR（5.0052），表明感知自然度更高。
- **Blur+JPEG 子集：** PSNR 为 29.55，LPIPS 为 0.0891，在保真度和感知质量上均表现优异。

UARE 在多数子集上取得了最优或次优的 MANIQA 和 NIQE 分数，证明其多退化处理能力具有通用性。但需注意，不同方法的训练数据分布可能存在差异，可能影响比较的公平性；论文未报告多次运行的方差。

### 4. IQA 任务结果

Table 3 展示了在 KADID、CSIQ、LIVE 等标准 IQA 基准上的 PLCC/SRCC 比较。UARE 在 KADID 上 PLCC 达到 0.878，CSIQ 上达到 0.930，与专门的 IQA 方法 Q-Align、DeQA-Score 等具有竞争力。这表明联合训练并未损害 IQA 能力，反而通过多任务学习实现了质量评估与恢复的协同。

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/010_Table_3.jpg]]
*Table 3: PLCC / SRCC comparison on the image quality assessment task between our UARE and other competitive methods*

### 5. 消融实验：两阶段训练框架

Table 4 的消融实验揭示了训练策略的关键作用：

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/009_Table_4.jpg]]
*Table 4: Ablation study of the two-stage training framework*

- **渐进式 vs. 一次性训练：** 将阶段一的渐进式课程替换为一次性混合训练（“all-in-one stage”），RealSR 上 MUSIQ 从 69.67 降至 57.50，MANIQA 从 0.5260 降至 0.3760。这证明由易到难的课程学习对于稳定训练和最终性能至关重要。
- **IQA 联合微调的作用：** 比较“+ high-order deg.”变体（仅使用高阶退化训练，无 IQA 联合微调）与完整 UARE，MUSIQ 从 57.50 提升至 69.67（+12.17），MANIQA 从 0.3760 提升至 0.5260（+0.15）。这是本文最核心的因果证据：引入 IQA 数据联合微调是感知质量大幅提升的直接原因。
- **保真度维持：** 在感知质量大幅提升的同时，PSNR 仅从 24.70 微降至 24.53（-0.17），LPIPS 从 0.2273 改善至 0.2259，说明 IQA 信号引导的恢复并未牺牲保真度。

### 6. 消融实验：IQA 引导机制

Table 5 进一步分析了 IQA 引导的具体形式：

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/011_Table_5.jpg]]
*Table 5: Ablation study of the IQA guidance in restoration*

- **结构化输出 vs. 简单指令：** 将输出替换为简单指令（“enhance this image”）而缺少四步结构化分析（用户意图、质量分析、增强计划、预期结果），感知指标显著下降。这表明结构化的“分析-恢复”数据格式是 IQA 信号有效传递的载体。
- **内部 IQA vs. 外部 IQA 提示：** 使用外部 Q-Insight 生成的文本作为提示替代 UARE 自身的 IQA 分析，效果明显较差。论文明确指出：“Compared with the Q-Insight-prompt setting, UARE aligns its own IQA and restoration capabilities more effectively, thereby turning IQA insights into concrete gains in restoration.” 这证明模型内部对齐的 IQA 信号远优于外部注入的质量描述。

### 7. 失败模式与局限

论文未系统报告失败案例，但可从实验设置和结果中推断以下局限：

- **计算资源需求极高：** 64 块 H20 GPU 训练一周，限制了社区的复现和扩展。
- **特定退化类型可能仍存短板：** 尽管在多退化子集上表现优异，但论文未对极低光照、严重压缩等极端退化进行专门分析，性能边界不明确。
- **IQA 与恢复的双向关系未探索：** 当前仅验证了 IQA 提升恢复的单向因果链，恢复如何反过来改进 IQA 仍是开放问题。
- **公平性存疑：** 不同基线方法使用的训练数据分布可能不同，且缺乏多次运行的误差棒，结论的稳健性需要进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/006_Figure_3.jpg]]
*Figure 3: Visual comparison of super-resolution on images named “Canon 047” from RealSR (top) and “0000065” from DIV2K-Val (bottom). Our UARE accurately understands both image content and degradations, achieving superior visual quality*

![[assets/figures/papers/paper_list_l2351_https_arxiv_org_abs_2512_06750/figures/001_Figure_1.jpg]]
*Figure 1: Showcase of UARE. It supports image quality assessment (image scoring and comparison), image restoration/enhancement (super-resolution, dehazing, and low-light enhancement, etc.), and assessment-guided restoration and enhancement in one unified model*



## 定位与知识库关联

### 1. 与现有工作的关系

#### 1.1 统一 IQA 与恢复的早期探索

在 UARE 之前，图像质量评估（IQA）与图像恢复/增强长期作为两个独立领域发展。少数学者尝试将二者关联，其中最具代表性的是 **PURE**（Wei et al., ICCV 2025），它在单一模型中同时支持 IQA 评分和图像恢复。然而，PURE 的 IQA 能力仅限于输出数值评分，无法生成细粒度的质量描述文本，且其 IQA 信号并未真正融入恢复过程——恢复分支本质上独立运行，未利用质量分析信息。

UARE 在此基础上迈出了关键一步：通过 Mixture-of-Transformers（MoT）架构中的双专家设计，使 IQA 专家不仅能输出评分，还能生成结构化的质量分析文本（包括当前退化诊断、增强计划与预期结果），并将这些文本信号通过共享的自注意力机制传递给恢复专家，实现了“分析-然后-恢复”的闭环范式。消融实验（Table 5）证实，使用 UARE 自身对齐的 IQA 分析比使用外部 **Q-Insight** 提示效果显著更好，验证了内部对齐的优越性。

#### 1.2 与超分辨率方法的比较

在超分辨率（SR）任务上，UARE 与以下代表性方法形成对比：

- **StableSR**（Wang et al., IJCV 2024）：基于扩散模型的 SR 方法，利用预训练 Stable Diffusion 先验。UARE 在 RealSR 上的 MUSIQ（69.67 vs. 63.90）和 LPIPS 均显著优于 StableSR，表明统一 IQA 引导的恢复能产生更符合人类感知的结果。
- **DiffBIR**（Xia et al., CVPR 2023）：面向盲复原的扩散方法。UARE 在 DIV2K 上的 MUSIQ（70.45 vs. 67.01）取得明显优势。
- **SeeSR**（Wu et al., CVPR 2024）：引入语义感知的 SR 方法。UARE 在 RealSR 上 MUSIQ 领先约 3.3 点，在 DRealSR 上 MANIQA 领先约 0.02。
- **OSEDiff**（Wu et al., NeurIPS 2024）：单步扩散 SR 方法，在 RealSR 上 MUSIQ 达到 68.95，是 UARE 最接近的竞争者（UARE 为 69.67）。UARE 的优势虽小（+0.72），但考虑到 OSEDiff 专门针对 SR 优化而 UARE 是通用模型，这一结果仍具说服力。
- **S3Diff**：在 DIV2K 上 MUSIQ 为 69.31，UARE 领先 1.14 点。

值得注意的是，UARE 在保真度指标（PSNR、SSIM）上与上述专用 SR 方法基本持平或略低，但在感知质量指标（MUSIQ、MANIQA、LPIPS）上普遍领先，这与其“质量信号引导生成”的核心设计理念一致——IQA 联合微调主要提升感知质量而非像素级保真度。

#### 1.3 与 IQA 方法的比较

在 IQA 评分任务上，UARE 与以下专用 IQA 模型对比：

- **Q-Align**（Wu et al., ICML 2024）：基于视觉-语言模型的 IQA 评分方法。UARE 在 KADID（PLCC 0.878 vs. 0.872）和 CSIQ（PLCC 0.930 vs. 0.917）上均略优于 Q-Align，同时在多个数据集上保持竞争力。
- **DeQA-Score**（You et al., CVPR 2025）：面向去模糊的 IQA 评分方法。UARE 在多个基准上与 DeQA-Score 互有胜负，整体处于同一水平。

UARE 的关键区分点在于：它并非专门的 IQA 模型，而是一个同时具备 IQA 和恢复能力的统一模型。其 IQA 能力在联合训练中不仅未退化，反而因恢复任务提供的丰富退化先验而保持强劲，这暗示两个任务之间存在正向迁移。

#### 1.4 与多退化恢复方法的比较

在 FoundIR 多退化基准上，UARE 与以下方法对比：

- **DiffUIR**：在 Blur+Noise 子集上，UARE 的 LPIPS 为 0.1573，DiffUIR 为 0.1871，UARE 降低 0.0298，感知质量优势明显。
- **FoundIR**：在 Low-light+Noise+JPEG 子集上，UARE 的 NIQE 为 4.5995，FoundIR 为 4.9494，UARE 降低 0.3499。

UARE 在多退化场景下的优势部分源于其渐进式训练策略——从单退化到多退化再到高阶退化，使模型逐步适应复杂退化组合。

### 2. 适用边界

UARE 的适用边界可从以下维度界定：

1. **退化类型覆盖**：当前支持超分辨率、去模糊、去噪、去雾、低光增强及它们的组合退化。对于训练数据中未充分覆盖的退化类型（如极端低光照、特定传感器噪声模式），性能可能下降，论文未对此进行系统分析。
2. **IQA 能力边界**：IQA 评分在合成失真数据集（KADID、CSIQ）上表现优异，但在真实世界失真数据集上的泛化性未充分验证。质量描述能力受限于训练数据的标注粒度和多样性。
3. **计算资源需求**：训练需 64 块 NVIDIA H20 GPU 持续一周，推理时需同时运行 IQA 和恢复两个专家，对边缘设备部署不友好。
4. **语言限制**：当前仅支持英文指令和质量描述，多语言扩展尚未探索。

### 3. 局限与开放问题

#### 3.1 已明确的局限

1. **单向信息流**：当前仅探索了 IQA 提升恢复的单向关系。恢复过程生成的图像是否反过来改进 IQA 能力，论文明确列为开放问题（"How restoration and enhancement, in turn, can better improve IQA remains an open question"），未进行实验验证。
2. **计算开销**：MoT 双专家架构在推理时需同时激活两个专家，相比专用恢复模型增加了计算负担。论文未提供推理延迟或吞吐量的定量分析。
3. **训练数据依赖性**：IQA 联合微调的效果高度依赖结构化“分析-恢复”数据的质量。消融实验（Table 5）显示，仅使用简单指令训练而缺少结构化分析数据时，感知指标显著下降，说明数据构造是性能的关键瓶颈而非模型架构本身。

#### 3.2 开放问题

1. **双向协同机制**：恢复结果如何反馈改进 IQA？是否可以通过自监督循环（恢复→IQA 评分→再次恢复）实现迭代优化？这需要设计新的训练范式。
2. **退化感知的粒度**：当前 IQA 分析以自然语言描述退化，但描述粒度（如“中度模糊” vs. 精确的模糊核参数）对恢复质量的影响未量化。更结构化的退化表示是否优于自由文本？
3. **跨任务泛化**：UARE 在 SR 和多退化恢复上展示了统一建模的潜力，但能否扩展到更广泛的 low-level 视觉任务（如去摩尔纹、去雨滴、老照片修复）仍待验证。
4. **评估公平性**：不同方法使用不同的训练数据分布，可能导致不公平比较。论文未报告多次运行的方差，结果的统计显著性需要手动验证。
5. **人机对齐**：UARE 生成的“预期结果”描述与最终恢复图像之间的一致性未量化。这种文本-图像对齐度可能是衡量统一模型质量的重要维度，但目前缺乏相应的评估基准。

### 4. 方法论定位总结

UARE 在方法论谱系中的定位可概括为：**首个将 IQA 文本分析信号有效注入图像恢复过程的统一视觉-语言模型**。其核心贡献不在于单项任务的绝对性能突破，而在于证明了以下方法论命题：多任务协同训练中，IQA 能力可以显著提升恢复图像的感知质量，同时基本保持保真度（PSNR 维持不变），实现恢复与评估的互相促进。这一发现为未来统一 low-level 视觉任务的研究提供了新的范式参考——即通过语言作为中间表征桥接质量感知与图像生成。



## 原文 PDF

![[paperPDFs/CVPR_2026/UARE_A_Unified_Vision_Language_Model_for_Image_Quality_Assessment_Restoration_and_Enhancement.pdf]]

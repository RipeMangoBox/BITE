---
title: "FAPE-IR: Frequency-Aware Planning and Execution Framework for All-in-One Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FAPE_IR_Frequency_Aware_Planning_and_Execution_Framework_for_All_in_One_Image_Restoration.pdf
project_link: null
code_link: "https://github.com/Programmergg/FAPE-IR"
aliases:
- FI
- FAPE-IR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 由冻结的多模态大语言模型规划器解析退化并生成频率感知复原计划，通过双端门控（文本路由+FIR谱路由器）驱动扩散执行器中高频与低频LoRA-MoE专家的动态选择与频带专业化。
primary_logic: 利用MLLM理解退化内容，输出可解释的频率感知计划，指导扩散模型通过频带专家分工实现高效复原；同时引入对抗训练和频率正则化，抑制伪影并促进专家专长化，统一了语义理解与像素级重建。
claims:
- FAPE-IR在六个AIO-IR任务系列中取得最佳或次佳性能，尤其在雨天、去雪、去雾等天气相关任务上PSNR提升约6-8 dB
- 在SR任务上，FAPE-IR在所有指标上均超越对比方法，PSNR从26.87 dB提升至28.53 dB
- 消融实验表明，频率感知文本路由(Freq-U)和FIR谱路由器(Freq-G)对性能至关重要，耦合后URHI PSNR从25.03 dB提升至29.71 dB
- 在BSD68-15高频消融中，引入Freq-G后PSNR达到33.57 dB，增益最大
---

# FAPE-IR: Frequency-Aware Planning and Execution Framework for All-in-One Image Restoration

> [!tip] 核心洞察
> 利用MLLM理解退化内容，输出可解释的频率感知计划，指导扩散模型通过频带专家分工实现高效复原；同时引入对抗训练和频率正则化，抑制伪影并促进专家专长化，统一了语义理解与像素级重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | FAPE-IR：面向全合一图像复原的频率感知规划与执行框架 |
| 英文题名 | FAPE-IR: Frequency-Aware Planning and Execution Framework for All-in-One Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.14099) · [Code](https://github.com/Programmergg/FAPE-IR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FAPE-IR |
| Dataset | Deraining, Dehazing, Desnowing, Super-Resolution |

> [!tip] 效果简介
> - Deraining (aggregated) 上，PSNR (dB) 28.30 vs 21.94 (PromptIR) (+6.36)。
> - Dehazing (aggregated) 上，PSNR (dB) 33.85 vs 19.89 (AdaIR) (+13.96)。
> - Desnowing (aggregated) 上，PSNR (dB) 30.29 vs 24.19 (AdaIR) (+6.10)。

## 概要

图像复原任务（去雨、去雾、去雪、去模糊、去噪、低光增强、超分辨率等）长期以来被孤立建模，每种退化类型依赖专用的架构与先验。全合一图像复原（All-in-One Image Restoration, AIO-IR）试图用单一模型处理多种退化，但现有方法面临一个**根本瓶颈**：它们要么采用任务特定的多分支映射，要么依赖固定的手工路由规则，缺乏对不同退化语义的显式理解，更无法在频率维度上实现共享与隔离的自适应机制。这导致跨任务冲突严重，泛化能力不足。

FAPE-IR 的核心洞察在于，图像复原的本质是一个频率感知问题——不同退化类型在频谱上呈现截然不同的能量分布（如去雨、去雪偏高频，去雾、低光增强偏低频），而人类在修复图像时也会自然地“先理解退化类型，再选择修复策略”。基于此，FAPE-IR 提出了一个**理解–生成统一框架**，将图像复原分解为两个协同阶段：

1. **频率感知规划器（Frequency-aware Planner）**：利用冻结的多模态大语言模型 **Qwen2.5-VL** 分析退化图像，结合从像素值直接计算的标签无关低级统计特征，生成结构化的频率感知复原计划——包括退化类型、频带焦点、恢复流水线和推理依据。
2. **频率感知 LoRA-MoE 执行器（Frequency-Aware LoRA-MoE Executor）**：以 FLUX 扩散 Transformer 为骨干，引入双端门控机制——规划器端的**文本路由**与执行器端的**FIR 频谱路由器**——动态选择高频或低频 LoRA 专家进行频带专业化复原。

这一“规划–执行”范式统一了高层语义理解与低层像素重建，并通过**多层次对抗训练**与**频率正则化损失**抑制伪影、强制专家专长化。

在涵盖六类退化任务的统一评估中，FAPE-IR 取得了**最优或次优性能**：在去雨、去雾、去雪等天气相关任务上，PSNR 提升约 6–8 dB（Table 1）；在超分辨率任务上，PSNR 从 26.87 dB 提升至 28.53 dB（Table 2）。消融实验证实，频率感知文本路由（Freq-U）与 FIR 频谱路由器（Freq-G）对性能至关重要——二者耦合后，URHI 基准上的 PSNR 从 25.03 dB 跃升至 29.71 dB（Table 4）。模型同时展现出对混合退化（雾+雨、低光混合等）的强零样本泛化能力。

### 全合一图像复原的演进瓶颈

图像复原旨在从退化的观测中恢复出干净图像，传统方法通常为每种退化类型（去雨、去雾、去模糊、超分辨率等）训练独立模型。然而，现实场景中退化类型往往未知且可能复合出现，这催生了**全合一图像复原（All-in-One Image Restoration, AIO-IR）**——用单一统一模型处理多种退化。

现有AIO-IR方法可大致归为两类范式（Figure 1）：(a) **多分支映射**，依赖任务级先验或提示词将不同退化路由到不同分支，代表工作如 **PromptIR**（NeurIPS 2023）；(b) **任务特定路由/聚类**，通过隐式特征聚类或频域路由实现退化分离，代表工作如 **AdaIR**（ICLR 2025）、**DFPIR**（CVPR 2025）和 **MoCE-IR**（CVPR 2025）。这两类方法存在共同的深层缺陷：

1. **缺乏显式语义理解**：模型无法“理解”图像中发生了什么退化，只能通过固定规则或隐式路由被动响应，导致跨任务冲突和泛化能力差。
2. **频率维度共享与隔离的失衡**：不同退化类型对不同频带的影响截然不同——去雨、去雪等任务以高频细节恢复为主，去雾、低光增强则侧重低频全局校正。现有方法要么全共享参数（导致任务间干扰），要么硬性分支（牺牲参数效率），缺乏**自适应频带专业化**机制。

### 本文动机：从“盲路由”到“理解-规划-执行”

上述瓶颈的根源在于：现有方法将图像复原视为纯像素映射问题，割裂了**语义理解**与**像素重建**。FAPE-IR的核心动机是引入一个“理解-规划-执行”范式：

- **理解**：利用多模态大语言模型（MLLM）分析退化图像，显式识别退化类型和频带受损模式；
- **规划**：生成结构化、可解释的**频率感知复原计划**，指明高频/低频专家的选择策略；
- **执行**：由扩散模型根据规划动态激活频带专家，实现高效且无冲突的复原。

这一设计从根本上解决了“盲路由”问题——模型不再猜测该用什么分支，而是通过语义理解做出可追溯的决策，同时通过频带专家分工实现参数高效的专业化。此外，通过引入对抗训练和频率正则化，FAPE-IR进一步抑制了扩散模型常见的伪影，并强制专家在各自频带内形成专长。

## 核心方法与创新机理

FAPE-IR 的核心创新在于将**多模态大语言模型的语义理解能力**与**扩散模型的频带专业化执行**相耦合，构建了一个“理解—规划—执行”的统一复原范式。与现有 AIO-IR 方法相比，其关键创新体现在三个维度的设计转变上。

### 从任务级提示到频率感知的语义规划

现有 AIO-IR 方法普遍依赖任务特定的提示词或嵌入（task-level prompts/embeddings）来区分退化类型，本质上是一种“查表式”映射。FAPE-IR 用冻结的 **Qwen2.5-VL** 多模态大语言模型替代了这一静态设计：规划器接收退化图像，结合从像素值提取的标签无关低级特征池（Label-free Low-level Feature Pool）中的图像统计量，生成结构化的频率感知复原计划 $FP = (\hat{t}, \hat{f}, \mathcal{R}, \mathcal{E})$——包含退化类型判别、频带焦点定位、复原流水线摘要与推理过程。这一转变使模型具备了对退化语义的显式理解能力，而非仅依赖表面统计特征。

### 从固定路由到双端门控的频带专家选择

FAPE-IR 在 FLUX Transformer 中引入了**频率感知 LoRA-MoE 执行器**，设置高频与低频两个专家，并通过双端门控机制实现动态路由：

- **规划器端文本路由（Freq-U）**：利用频率对齐的理解 token 生成专家选择权重；
- **执行器端 FIR 谱路由器（Freq-G）**：直接检查中间特征的高/低频分量，提供频谱层面的路由信号。

两者融合后驱动 FLUX 投影矩阵的逐专家 LoRA 适配器加权更新 $W' = W + \sum_{i=1}^{N} \alpha_i A_i B_i$。相比 **MoCE-IR**（MoE-based AIO-IR, CVPR 2025）的通用 MoE 路由和 **DFPIR**（Frequency-aware AIO-IR, CVPR 2025）的频域路由，FAPE-IR 的双端门控同时利用了语义线索和频谱结构，实现了更稳定的频带专家分工。

### 从像素级损失到对抗训练与频率正则化的联合优化

FAPE-IR 摒弃了统一模型中常用的 flow-matching 微调目标，转而采用**多层次对抗训练 + 频率正则化**的联合优化策略。具体而言：

- **多层次判别器头**对 SigLIP-v2 的多尺度特征图进行判别，提供多粒度的对抗损失；
- **频率正则化项** $\mathcal{L}_{\mathrm{freq}} = \mathrm{mean}\big[||\mathcal{H}_g(y_{\mathrm{low}})||_2^2 + ||\mathcal{L}_g(y_{\mathrm{high}})||_2^2\big]$ 惩罚低频专家的高频输出和高频专家的低频输出，强制频带专长化。

总损失 $\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{adv}} + \gamma \mathcal{L}_{\mathrm{freq}}$ 将语义级保真度约束与频带专业化约束统一，既抑制了扩散模型常见的伪影，又促进了专家之间的功能分化。消融实验证实，去除任一损失项均导致性能下降（Figure 13），验证了四项损失相互补充的机制。

FAPE-IR 采用**规划–执行**范式，将全合一图像复原分解为两个耦合阶段：**频率感知规划器**与**频带专业化执行器**，如图 2 所示。其核心思想是：先“理解”退化图像的语义与频谱特性，再“执行”针对性的频带复原，从而统一语义理解与像素级重建。

### 规划–执行流水线

1. **输入**：一张任意退化的图像。
2. **频率感知规划器**：由冻结的多模态大语言模型（MLLM）Qwen2.5-VL 构成。规划器接收退化图像和从像素值统计量构建的**标签无关低级特征池** $P_{\mathrm{hints}}$，输出结构化的频率感知复原计划 $FP = (\hat{t}, \hat{f}, \mathcal{R}, \mathcal{E})$，包含退化类型、频带焦点、复原流水线摘要和推理说明。
3. **频带专业化执行器**：基于 FLUX Transformer 构建的扩散模型。其核心是**频率感知 LoRA-MoE 模块**，包含高频和低频两个 LoRA 专家。该模块通过**双端门控机制**动态选择专家：
   - **规划器端门控（文本路由，Freq-U）**：将规划器输出的频率对齐理解 token 作为语义条件，驱动专家选择。
   - **执行器端门控（FIR 谱路由器，Freq-G）**：对中间特征进行高/低频分离，提供频谱层面的路由信号。
4. **输出**：融合路由器系数 $\alpha_i$ 对 FLUX 投影矩阵进行逐专家 LoRA 适配器加权更新：
   $$W' = W + \sum_{i=1}^{N} \alpha_i A_i B_i$$
   最终生成复原图像。

### 训练范式

FAPE-IR 摒弃了统一模型中常用的 flow-matching 微调目标，转而采用**多层次对抗训练**与**频率正则化**相结合的方案：

- **多层次判别器头**：在冻结的 SigLIP-v2 多尺度特征图上施加对抗损失 $\mathcal{L}_{\mathrm{adv}}^{\mathcal{D}}$，生成器复合损失 $\mathcal{L}_{\mathrm{adv}}$ 融合 MSE、LPIPS 感知损失和对抗项。
- **频率正则化项**：惩罚低频专家的高频输出和高频专家的低频输出，强制频带专长化：
  $$\mathcal{L}_{\mathrm{freq}} = \mathrm{mean}\big[\|\mathcal{H}_g(y_{\mathrm{low}})\|_2^2 + \|\mathcal{L}_g(y_{\mathrm{high}})\|_2^2\big]$$
- **总体目标**：
  $$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{adv}} + \gamma \mathcal{L}_{\mathrm{freq}}$$

这一设计源于实验观察：标准 flow-matching 训练在真实世界超分任务中会引入严重伪影和不真实的高频细节（见图 12），而对抗训练配合频率正则化能有效抑制此类问题，同时提升感知指标（LPIPS、FID、DISTS）。

### 与前人范式的本质差异

如图 1 所示，现有 AIO-IR 方法主要分两类：(a) 使用任务特定提示词的多分支映射（如 **PromptIR**, NeurIPS 2023）；(b) 基于任务路由或聚类的方法（如 **MoCE-IR**, CVPR 2025）。FAPE-IR 的独特之处在于：将 MLLM 的语义理解能力引入退化分析，生成显式、可解释的频率感知计划，进而通过频带专家分工实现高效复原——这是首次在 AIO-IR 中实现理解与生成的端到端统一。

![[assets/figures/papers/paper_list_l2485_https_arxiv_org_abs_2511_14099/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed FAPE-IR framework*

![[assets/figures/papers/paper_list_l2485_https_arxiv_org_abs_2511_14099/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of AIO-IR methods: (a) multi-branch mappings with task-level priors; (b) task-specific routing/clustering; (c) our FAPE-IR, unifying understanding and restoration*

![[assets/figures/papers/paper_list_l2485_https_arxiv_org_abs_2511_14099/figures/018_Figure_12.jpg]]
*Figure 12: Qualitative results of training our framework with a standard flow-matching (FM) objective on real-world super-resolution. Although the FM-trained variant can sharpen some structures, it also introduces severe artifacts and unrealistic high-frequency details (e.g., distorted edges and hallucinated textures), which motivates our final design choices for FAPE-IR*

FAPE-IR 采用“规划—执行”范式，将图像复原分解为频率感知规划器（Frequency-aware Planner）与基于扩散的执行器（Diffusion-based Executor）两大核心模块（Figure 2）。规划器负责理解退化语义并生成结构化的频率感知复原计划，执行器则依据该计划动态调度频带专家完成像素级重建。

### 3.1 频率感知规划器

规划器由三个子模块构成：标签无关低级特征池（Label-free Low-level Feature Pool）、指令与规划生成、频率对齐理解令牌编码。

**标签无关低级特征池**从退化图像像素值直接计算一组简单统计量，形成频率视角下的退化模式描述向量 $P_{\mathrm{hints}}$，为多模态大语言模型（MLLM）提供视觉线索，避免依赖任务标签。

**指令与规划生成**以冻结的 Qwen2.5-VL 作为推理核心，接收退化图像与 $P_{\mathrm{hints}}$ 后，输出结构化复原计划：

$$FP = (\hat{t}, \hat{f}, \mathcal{R}, \mathcal{E})$$

其中 $\hat{t}$ 为选定的退化类型，$\hat{f}$ 为频率焦点（高频主导/低频主导/混合），$\mathcal{R}$ 为恢复流水线摘要，$\mathcal{E}$ 为推理过程解释。该计划随后被编码为频率对齐理解令牌，注入执行器。

### 3.2 频率感知 LoRA-MoE 执行器

执行器基于 FLUX Transformer 构建，核心是频率感知 LoRA-MoE 模块（Figure 3），包含高频与低频两个 LoRA 专家，通过双端门控机制实现频带专业化调度。

![[assets/figures/papers/paper_list_l2485_https_arxiv_org_abs_2511_14099/figures/003_Figure_3.jpg]]
*Figure 3: Frequency-Aware LoRA-MoE architecture*

**双端门控机制**由规划器端文本路由器（Freq-U）与执行器端 FIR 频谱路由器（Freq-G）组成。Freq-U 将规划器输出的频率对齐理解令牌映射为专家选择系数；Freq-G 对中间特征图进行高通/低通滤波后产生频谱感知的路由权重。两者融合后经稀疏化处理，得到最终的路由系数 $\alpha_i$。

**FLUX 投影更新**：对于 FLUX 中的任一线性投影 $W$，更新形式为：

$$W' = W + \sum_{i=1}^{N} \alpha_i A_i B_i$$

其中 $N$ 为专家数量（本文 $N=2$），$A_i, B_i$ 为第 $i$ 个专家的低秩适配器矩阵，$\alpha_i$ 为融合路由器输出的该专家权重。该设计使得不同频带的退化通过不同专家组合得到差异化处理。

### 3.3 训练目标

FAPE-IR 摒弃了统一模型中常用的 flow-matching 微调目标，转而采用多层次对抗训练与频率正则化的联合优化策略。

**多层次判别器**以冻结的 SigLIP-v2 为特征提取骨干，在其多尺度特征图 $\mathbf{f}^{(l)}$ 上附加判别器头 $\mathcal{H}_{\psi}^{(l)}$，输出空间分数图 $\mathbf{s}^{(l)}$，同时在全图池化特征 $\mathbf{p}$ 上产生池化分数 $s^{\mathrm{pool}}$。判别器损失为标准对抗形式：

$$\mathcal{L}_{\mathrm{adv}}^{\mathcal{D}} = -\mathbb{E}_{x}[\log D(x)] - \mathbb{E}_{\hat{x}}[\log(1-D(\hat{x}))]$$

生成器复合对抗损失为：

$$\mathcal{L}_{\mathrm{adv}} = \alpha \|\hat{x} - x\|_2^2 + \beta \|\phi(\hat{x}) - \phi(x)\|_2^2 - \lambda \mathbb{E}[D(\hat{x})]$$

其中 $\alpha$ 为 MSE 损失权重，$\beta$ 为 LPIPS 感知损失权重，$\lambda$ 为对抗项权重。

**频率正则化项**强制专家频带专长化，惩罚低频专家的高频输出与高频专家的低频输出：

$$\mathcal{L}_{\mathrm{freq}} = \mathrm{mean}\big[\|\mathcal{H}_g(y_{\mathrm{low}})\|_2^2 + \|\mathcal{L}_g(y_{\mathrm{high}})\|_2^2\big]$$

其中 $\mathcal{H}_g$ 和 $\mathcal{L}_g$ 分别为高通与低通高斯滤波器，$y_{\mathrm{low}}$ 和 $y_{\mathrm{high}}$ 为低频与高频专家的输出分量。

**总损失**为：

$$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{adv}} + \gamma \mathcal{L}_{\mathrm{freq}}$$

其中 $\gamma$ 为频率正则化权重。四项损失（MSE、LPIPS、对抗、频率正则化）相互补充：消融实验（Figure 13）表明，移除任一损失项均导致性能下降，验证了该组合设计的必要性。

## 实验与关键发现

### 主实验结果

FAPE-IR在六个经典退化任务系列上进行了统一评估，与多种AIO-IR基线方法进行了全面比较。Table 1汇总了去雨、去噪、去模糊、去雪、去雾和低光增强任务的五项指标（PSNR↑、SSIM↑、LPIPS↓、FID↓、DISTS↓）。FAPE-IR在去雨、去雪、去雾等天气相关任务上取得了显著领先，PSNR分别达到28.30 dB、30.29 dB和33.85 dB，较次优方法提升约6–8 dB，LPIPS和DISTS等感知指标同样最优。在去噪和去模糊任务上，FAPE-IR的PSNR/SSIM与最优方法可比，而LPIPS/FID/DISTS均达到最佳或次佳水平，表明模型在保真度与感知质量之间取得了有利平衡。在低光增强任务上，PSNR略低于最优方法，但SSIM和感知指标更优。Table 2展示了超分辨率任务的统一比较，FAPE-IR在所有五个指标上均超越对比方法，PSNR从26.87 dB（**PASD**, ECCV 2024）提升至28.53 dB，SSIM从0.82提升至0.85，LPIPS从0.23降至0.19。Table 5和Table 6进一步提供了全基准上的详细全参考指标和无参考IQA指标，FAPE-IR在多数基准上保持最优或可比性能。

在模型复杂度方面，Table 3显示FAPE-IR推理内存占用为38.92G，推理时间1.57s（H200 GPU，512×512输入）。虽然参数量高于轻量级模型，但推理速度远快于**PURE**（201.67s, ICCV 2025），且性能全面领先。

定性结果方面，Figure 5展示了高频主导任务（去雨/去雪/去模糊/去噪）的对比，FAPE-IR能更好地保留精细结构和纹理，抑制振铃和过锐化伪影。Figure 6展示了低频任务与超分结果，FAPE-IR在去雾时能平衡光照并保持色彩，在超分时产生更高保真度和更少伪影。Figure 11与AIO-IR基线模型的定性对比进一步验证了这些优势。

### 消融实验

**规划器与路由机制消融**：Table 4在URHI基准上消融了核心组件。移除Qwen2.5-VL规划器后，PSNR从29.71 dB骤降至25.03 dB，SSIM从0.95降至0.92，验证了语义规划的关键作用。同时移除频率感知文本路由（Freq-U）和FIR谱路由器（Freq-G）时，性能大幅下降；单独引入Freq-U带来适当提升，加入Freq-G后达到最优，表明双端频率感知门控对路由稳定性至关重要。Table 7在BSD68-15高频去噪任务上的消融进一步证实，Freq-G模块带来最大PSNR增益（从30.81 dB提升至33.57 dB），证明显式频带专家选择能有效处理高频退化。

**LoRA秩消融**：Table 4和Table 7均显示，中等LoRA秩（r=8）在模型容量与专家专业化之间取得最佳平衡。过低的秩限制专家表达能力，过高的秩可能导致专家间冗余。

**损失函数消融**：Figure 13展示了四个损失权重（α, β, λ, γ）在URHI和BSD68-15上的超参数敏感性分析。去除任一损失项均导致性能下降，MSE损失（α）、LPIPS感知损失（β）、对抗损失（λ）和频率正则化（γ）四项相互补充。对抗训练与频率正则化的共同作用在Table 1的感知指标（LPIPS/FID/DISTS）上也得到验证。

### 局限性与失败模式

尽管FAPE-IR在多数任务上表现优异，仍存在若干局限性。首先，在去噪和低光增强任务上，PSNR略低于最优方法，但SSIM和感知指标更优，表明模型倾向于保真度与感知质量的平衡而非单纯追求像素误差。其次，在真实世界超分辨率的无参考IQA指标上有时弱于对比方法，推测由于SR真实图像的统计特性与现有NR-IQA模型不匹配。Figure 12展示了使用标准flow-matching目标训练时的失败案例——虽然能锐化部分结构，但引入了严重伪影和不真实的高频细节（如扭曲边缘和幻觉纹理），这验证了对抗训练替换flow-matching的必要性。此外，模型推理内存占用较高（38.92G），部署于资源受限平台存在挑战。现有训练数据未能覆盖所有混合退化类型，零样本泛化能力虽有验证（Figure 9展示了雾+雨/雪、低光混合等复合退化结果），但仍有提升空间。

![[assets/figures/papers/paper_list_l2485_https_arxiv_org_abs_2511_14099/figures/004_Table_1.jpg]]
*Table 1: Unified comparison across six AIO-IR task series. Each series shows five metrics (PSNR↑, SSIM↑, LPIPS↓, FID↓, DISTS↓). The best results are highlighted in red, and the second-best results are shown in blue*

![[assets/figures/papers/paper_list_l2485_https_arxiv_org_abs_2511_14099/figures/005_Table_2.jpg]]
*Table 2: Unified comparison across SR task series. Each series shows five metrics. The best results are marked in red, and the second-best results are shown in blue*

## 定位与知识库关联

### 1. 问题定位与范式演进

全合一图像复原（All-in-One Image Restoration, AIO-IR）的核心瓶颈在于：单一模型需同时处理去雨、去雪、去雾、去模糊、去噪、低光增强、超分辨率等多种退化类型，而这些退化在频域特征上差异显著——例如去雨/去雪/去模糊主要涉及高频细节修复，而去雾/低光增强则侧重低频全局调整。现有方法大致经历了三个范式阶段：

- **多分支映射 + 任务级先验**（如 **PromptIR**, NeurIPS 2023）：为不同任务设计独立分支或嵌入任务特定提示词，但缺乏对退化语义的显式理解，跨任务冲突严重，泛化能力受限。
- **任务特定路由/聚类**（如 **AdaIR**, ICLR 2025；**DFPIR**, CVPR 2025；**MoCE-IR**, CVPR 2025）：通过频域路由或混合专家（MoE）机制实现一定程度的任务自适应，但路由策略多为隐式学习或固定规则，缺乏语义层面的退化理解与可解释的频率感知规划。
- **统一理解-生成框架**（本文 **FAPE-IR**）：首次将冻结的多模态大语言模型（MLLM）引入AIO-IR作为显式规划器，生成结构化、可解释的频率感知复原计划，并通过双端门控（文本路由 + FIR谱路由器）驱动扩散执行器中高频/低频LoRA-MoE专家的动态选择，实现频带专业化分工。

Figure 1 清晰展示了这一范式演进：从任务级先验到任务路由，再到本工作的“理解-规划-执行”统一框架。

### 2. 与基线方法的关键差异

#### 2.1 辅助信息注入方式

| 方法 | 辅助信息形式 | 频率感知 | 可解释性 |
|------|-------------|---------|---------|
| PromptIR | 任务特定提示嵌入 | 无 | 低 |
| AdaIR | 频域自适应路由 | 隐式 | 低 |
| DFPIR | 频域路由 | 显式但固定 | 中 |
| MoCE-IR | MoE门控路由 | 无显式频带分工 | 低 |
| **FAPE-IR** | MLLM生成的频率感知文本计划 + FIR频谱特征 | 显式、语义对齐 | 高 |

FAPE-IR的辅助信息注入包含两个层面：（1）规划器端——由Qwen2.5-VL生成的频率感知复原计划，明确指定退化类型、频带焦点和恢复流水线；（2）执行器端——通过FIR滤波器提取的高低频特征图作为频谱路由器输入。这种双端设计使得专家选择同时受语义理解和频域统计的约束，从根本上区别于现有方法的单一门控机制。

#### 2.2 规划器设计

现有AIO-IR方法普遍缺乏显式规划器，退化处理路径要么由固定架构决定，要么由隐式路由学习得到。FAPE-IR引入冻结的Qwen2.5-VL作为频率感知规划器，其核心创新包括：

- **标签无关低级特征池**：从像素值直接计算图像统计量（均值、方差、梯度能量等），为MLLM提供频率相关的视觉线索，避免依赖任务标签。
- **结构化规划输出**：规划器生成四元组 $FP = (\hat{t}, \hat{f}, \mathcal{R}, \mathcal{E})$，分别表示退化类型、频率焦点、恢复流水线摘要和推理说明，实现了完全可解释的决策过程。
- **频率对齐理解令牌**：将规划输出的文本嵌入与图像频域特征对齐，作为执行器文本路由器的输入。

#### 2.3 训练目标

主流AIO-IR方法通常采用像素级损失（L1/L2）或Flow-matching目标进行训练。FAPE-IR则采用多层次对抗训练 + 频率正则化的组合策略：

- **对抗训练**：替换Flow-matching微调，使用基于SigLIP-v2多尺度特征图的判别器头，有效抑制了Flow-matching训练中出现的伪影和虚假高频细节（见Figure 12的对比）。
- **频率正则化**：$\mathcal{L}_{\mathrm{freq}} = \mathrm{mean}\big[\|\mathcal{H}_g(y_{\mathrm{low}})\|_2^2 + \|\mathcal{L}_g(y_{\mathrm{high}})\|_2^2\big]$，惩罚低频专家的高频输出和高频专家的低频输出，强制专家在各自频带内专长化。

### 3. 适用边界与局限

#### 3.1 性能边界

根据Table 1和Table 2的综合评估，FAPE-IR的优势区间和相对薄弱区间如下：

- **高频退化任务（强项）**：去雨（PSNR 28.30 dB，较PromptIR提升6.36 dB）、去雪（30.29 dB，较AdaIR提升6.10 dB）、去雾（33.85 dB，较AdaIR提升13.96 dB）表现突出，尤其在天气相关退化上优势显著。
- **超分辨率任务（强项）**：在所有对比方法中全面领先，PSNR从26.87 dB（PASD, ECCV 2024）提升至28.53 dB。
- **去噪与低光增强（相对薄弱）**：PSNR略低于最优方法，但SSIM和感知指标（LPIPS/FID/DISTS）更优，表明模型倾向于保真度-感知质量平衡而非单纯追求像素精度。
- **真实世界SR无参考指标（薄弱）**：有时弱于对比方法，推测由于SR真实图像的统计特性与NR-IQA模型不匹配。

#### 3.2 计算资源边界

Table 3显示FAPE-IR推理内存占用为38.92G，推理时间1.57s（H200 GPU）。虽然推理速度远快于PURE（ICCV 2025, 201.67s），但参数量较大，在资源受限平台（如移动端、边缘设备）部署存在明显挑战。

#### 3.3 泛化边界

零样本复合退化泛化实验（Figure 9）验证了模型在雾+雨/雪、低光混合等未见退化组合上的有效性，但论文明确指出“现有训练数据未能覆盖所有混合退化类型”，泛化能力仍有提升空间。

### 4. 开放问题

1. **SR无参考指标失配**：为何真实世界SR图像的统计特性会导致NR-IQA得分下降？这是SR领域普遍存在的问题，还是FAPE-IR特定训练策略导致的？需要更系统的分析。

2. **训练数据覆盖度**：如何构建更高质量、覆盖更多退化类型（特别是复合退化）的训练数据，以提升模型在开放场景下的泛化性？

3. **NR-IQA模型可靠性**：能否设计出与全参考指标和人类感知更一致的NR-IQA模型，从根本上解决评估偏差问题？

4. **效率优化空间**：在保持性能的前提下，探索轻量级MLLM替代Qwen2.5-VL、更高效的MoE路由策略（如top-1稀疏化）、或知识蒸馏方案，以降低推理内存占用。

5. **频带专家数量的可扩展性**：当前设计仅使用两个频带专家（高频/低频），是否可以通过引入更多中间频带专家（如中频纹理专家）进一步提升细粒度复原能力？这需要在专家专业化与路由稳定性之间寻找新的平衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/FAPE_IR_Frequency_Aware_Planning_and_Execution_Framework_for_All_in_One_Image_Restoration.pdf]]

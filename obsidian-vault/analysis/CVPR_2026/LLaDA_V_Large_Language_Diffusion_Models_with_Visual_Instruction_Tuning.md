---
title: "LLaDA-V: Large Language Diffusion Models with Visual Instruction Tuning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LLaDA_V_Large_Language_Diffusion_Models_with_Visual_Instruction_Tuning.pdf
project_link: "https://ml-gsai.github.io/LLaDA-V-demo/"
code_link: "https://github.com/EvolvingLMMs-Lab/lmms-eval</td></tr><tr><td>LLaVA-NeXT</td><td>https://github.com/LLaVA-VL/LLaVA-NeXT</td></tr><tr><td>MAmmoTH-VL</td><td>https://github.com/MAmmoTH-VL/MAmmoTH-VL</td></tr><tr><td>VisualWebInstruct</td><td>https://github.com/TIGER-AI-Lab/VisualWebInstruct</td></tr><tr><td>Data</td><td>URL</td></tr><tr><td>LLaVA-Pretrain"
aliases:
- LV
- LLaDA-V
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 训练时对回答部分进行随机掩码，推理时通过迭代去掩码逐步生成回答；这一掩码扩散机制替代了传统的自回归生成，使得模型能够学习多模态对齐与推理能力。
primary_logic: 即使纯文本语言模型（LLaDA）弱于LLaMA3等自回归模型，通过视觉指令微调，纯扩散MLLM可在多模态任务中展现出与自回归模型相当甚至更优的性能，并具有更好的数据可扩展性，证明了扩散模型在多模态领域的潜力。
claims:
- LLaDA-V在多数多学科知识和数学推理基准（如MMMU, MMMU-Pro）上超越自回归基线LLaMA3-V。
- LLaDA-V在数据扩展性上优于LLaMA3-V，尤其使用1M样本时性能即超过LLaMA3-V的9M样本。
- LLaDA-V在所有现有的混合自回归‑扩散与纯扩散MLLM中取得最优性能。
- 采用双向注意力（无掩码）在12个基准中的7个上优于对话因果注意力。
---

# LLaDA-V: Large Language Diffusion Models with Visual Instruction Tuning

> [!tip] 核心洞察
> 即使纯文本语言模型（LLaDA）弱于LLaMA3等自回归模型，通过视觉指令微调，纯扩散MLLM可在多模态任务中展现出与自回归模型相当甚至更优的性能，并具有更好的数据可扩展性，证明了扩散模型在多模态领域的潜力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 大型语言扩散模型结合视觉指令微调 |
| 英文题名 | LLaDA-V: Large Language Diffusion Models with Visual Instruction Tuning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.16933) · [Project](https://ml-gsai.github.io/LLaDA-V-demo/) · [Code](https://github.com/EvolvingLMMs-Lab/lmms-eval</td></tr><tr><td>LLaVA-NeXT</td><td>https://github.com/LLaVA-VL/LLaVA-NeXT</td></tr><tr><td>MAmmoTH-VL</td><td>https://github.com/MAmmoTH-VL/MAmmoTH-VL</td></tr><tr><td>VisualWebInstruct</td><td>https://github.com/TIGER-AI-Lab/VisualWebInstruct</td></tr><tr><td>Data</td><td>URL</td></tr><tr><td>LLaVA-Pretrain) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | LLaDA-V |
| Dataset | MMMU, MMMU-Pro, MMStar, MME |

> [!tip] 效果简介
> - MMMU (val) 上，准确率 (%) 48.6 vs 45.4 (LLaMA3-V) (+3.2)。
> - MMMU-Pro (standard) 上，准确率 (%) 35.2 vs 28.3 (LLaMA3-V) (+6.9)。
> - MMStar 上，准确率 (%) 60.1 vs 60.7 (Qwen2-VL) ↔ 56.5 (LLaMA3-V) (-0.6 vs. +3.6)。

## 概要

现有多模态大语言模型（MLLM）几乎全部依赖自回归生成范式，而纯扩散模型在多模态理解中的潜力长期未被充分探索。本文提出 **LLaDA-V**，一个完全基于掩码扩散机制的多模态大语言模型，首次在训练和推理两端均摒弃自回归，转而采用扩散去掩码生成。其核心瓶颈在于：自回归模型主导的MLLM生态缺乏对扩散框架能否承载视觉指令微调的实证检验。

LLaDA-V的因果调控旋钮在于**掩码扩散的训练-推理闭环**：训练时仅对回答部分进行随机掩码并预测被掩码token，推理时从全掩码状态出发，通过迭代去掩码与低置信度重掩码策略逐步生成回答。这一机制替代了传统的逐token自回归生成，使模型在双向注意力下学习多模态对齐与推理。

核心洞察是：即使纯文本语言塔 **LLaDA-8B** 弱于 **LLaMA3-8B** 等自回归模型，通过视觉指令微调后，纯扩散MLLM可在多学科知识与数学推理任务上超越自回归基线，并展现出更强的数据可扩展性。决定性证据包括：
- LLaDA-V在 **MMMU**（48.6% vs. 45.4%）和 **MMMU-Pro**（35.2% vs. 28.3%）上显著超越自回归基线 **LLaMA3-V**（Figure 1(a), Table 2）。
- 数据扩展性实验中，LLaDA-V仅用1M样本即超过LLaMA3-V的9M样本性能（Figure 3）。
- 在所有现有混合自回归‑扩散与纯扩散MLLM中，LLaDA-V取得最优性能（Figure 1(b), Tables 2 & 3）。
- 消融实验证实双向注意力（无掩码）在12个基准中的7个上优于对话因果注意力（Table 4）。

方法定位上，LLaDA-V属于**纯扩散多模态理解模型**，区别于 **Show-o**、**MetaMorph** 等混合自回归‑扩散方案。其架构遵循标准视觉指令微调框架（视觉编码器 + MLP投影器 + 语言塔），仅将语言塔替换为掩码扩散模型，并采用双向注意力。训练数据与自回归基线完全一致，确保对比公平。

主要局限性在于：LLaDA-V在图表/文档理解（如AI2D）和真实世界场景（如RealworldQA）上仍落后于自回归基线；扩散推理需多步迭代，效率未与自回归模型对比；训练未引入偏好对齐技术（RLHF/DPO）。开放问题包括：更强扩散语言塔能否进一步提升性能、偏好对齐能否缩小与一流自回归模型的差距、以及扩散MLLM的推理效率优化路径。



### 多模态大语言模型的自回归范式

当前主流的MLLM几乎全部建立在自回归语言模型之上。这些模型将视觉编码器提取的图像特征通过投影层映射到语言空间，随后由自回归Transformer以逐token预测的方式生成文本回答。这一范式在多数视觉理解任务上表现出色，但也内嵌了一个强假设：生成过程必须是因果的、顺序的。该假设是否构成多模态理解的唯一有效路径，始终未被充分检验。

### 扩散模型在多模态理解中的缺位

扩散模型在图像和视频生成领域已展现出强大能力，但在多模态理解任务中，其应用长期局限于两类方案：一是仅将扩散用于视觉编码器或生成辅助，语言推理仍依赖自回归模块；二是采用“混合自回归‑扩散”架构，例如**Show-o**和**MetaMorph**，在生成阶段部分引入扩散机制，但训练或推理仍保留自回归组件。纯扩散MLLM——即训练和推理完全基于扩散机制、不依赖任何自回归模块的模型——在多模态理解中的潜力几乎未被探索。

这一空白的关键瓶颈在于：现有研究缺乏一个端到端的纯扩散框架，能够同时完成多模态对齐和语言推理，并在标准基准上与自回归模型进行公平对比。

### 核心动机与研究问题

本文的核心动机是回答一个根本性问题：**纯扩散模型能否在多模态理解任务中达到与自回归模型相当甚至更优的性能？** 这一问题的因果逻辑链条如下：

- **可控变量**：将语言塔从自回归模型（LLaMA3-8B）替换为掩码扩散模型（LLaDA-8B），保持视觉编码器、MLP投影器、训练数据和训练流程完全一致，从而隔离扩散机制本身的影响。
- **核心洞察**：即使纯文本LLaDA的语言能力弱于LLaMA3等自回归模型，通过视觉指令微调，纯扩散MLLM可在多模态任务中展现出与自回归模型相当甚至更优的性能，并具有更好的数据可扩展性。
- **决定性证据**：LLaDA-V在MMMU（+3.2%）和MMMU-Pro（+6.9%）等多学科知识与数学推理基准上超越自回归基线LLaMA3-V；在使用1M训练样本时，其性能已超过LLaMA3-V使用9M样本的水平。

这一发现挑战了“多模态理解必须依赖自回归生成”的隐含假设，为扩散模型在多模态领域开辟了新的可能空间。



## 核心方法与创新机理

LLaDA-V的核心创新在于**将纯掩码扩散机制完整地引入多模态大语言模型（MLLM）的训练与推理全流程**，替代了传统自回归模型依赖的逐token因果生成范式。这一转变通过四个关键的“changed slots”实现，构成了与自回归基线**LLaMA3-V**的本质差异。

### 1. 语言塔：从自回归模型到掩码扩散模型

LLaDA-V的语言塔采用**LLaDA-8B**，一个基于掩码扩散的大语言模型，而非自回归基线使用的LLaMA3-8B。这一替换是框架级变革的根基：LLaDA-8B本身在纯文本能力上弱于LLaMA3-8B，但其双向注意力机制和掩码预测训练目标为多模态理解提供了不同的归纳偏置。值得注意的是，即使语言塔本身较弱，LLaDA-V在多数多学科知识和数学推理基准上仍超越了LLaMA3-V（Table 2），表明扩散机制在多模态场景中具有独特的适配优势。

### 2. 注意力结构：从因果掩码到双向注意力

自回归模型强制使用因果注意力掩码（tokens只能关注自身及之前的tokens），而LLaDA-V采用**双向注意力（无掩码）**，允许每个token关注序列中的所有token。这一设计使得模型在理解图像-文本多模态序列时，能够同时利用前后文信息进行全局推理。消融实验（Table 4）证实，在12个基准中的7个上，双向注意力优于对话因果注意力，尤其在MMMU、MuirBench等需要深度推理的任务上提升明显。Figure 4直观对比了三种注意力掩码策略：标准因果掩码、对话因果掩码和LLaDA-V的双向注意力。

### 3. 训练目标：从下一个token预测到掩码预测损失

LLaDA-V的训练目标从自回归的“下一个token预测”转变为**掩码预测损失**。具体而言，训练时仅对回答部分的token进行随机掩码，模型需要根据未掩码的图像特征和提示，预测被掩码的token。其训练目标（Eq.(1)）已被证明是负对数似然的上界：

$$- \mathbb { E } _ { \boldsymbol { v } , t , \boldsymbol { p _ { 0 } ^ { 1 } } , \boldsymbol { r } _ { 0 } ^ { 1 } , \boldsymbol { r } _ { t } ^ { 1 } } , \left[ \frac { 1 } { t } \sum _ { i = 1 } ^ { L _ { r 1 } } \sum _ { j = 1 } ^ { L _ { r 2 } } \mathbf { 1 } [ \boldsymbol { r } _ { t } ^ { 1 , i } = [ \mathbf { M } ] \wedge \boldsymbol { r } _ { t } ^ { 2 , j } = [ \mathbf { M } ] ] \log _ { \mathcal { P } _ { \boldsymbol { \theta } } } ( \boldsymbol { r } _ { 0 } ^ { 1 , i } , \boldsymbol { r } _ { 0 } ^ { 2 , j } | \boldsymbol { v } , \boldsymbol { p } _ { 0 } ^ { 1 } , \boldsymbol { r } _ { t } ^ { 1 } , \boldsymbol { p } _ { 0 } ^ { 2 } , \boldsymbol { r } _ { t } ^ { 2 } ) \right]$$

这一目标与双向注意力天然协同：模型可以同时看到完整的图像特征和提示上下文，从而学习更丰富的多模态对齐与推理能力，而非仅依赖单向的因果依赖。

### 4. 推理方式：从自回归逐token生成到迭代去掩码

推理阶段，LLaDA-V从**全掩码的回答序列**出发，通过**迭代去掩码**逐步生成回答。具体过程遵循掩码扩散的反向过程（Eq.(3)）：随时间步 $t$ 从1递减至0，模型在每个时间步预测当前掩码token，并根据置信度选择部分token进行“去掩码”（即替换为预测的真实token），同时采用**低置信度重掩码策略**——将置信度最低的已预测token重新掩码，以在后续步骤中修正。这一机制继承了LLaDA的设计，相比随机重掩码可稳定提升生成质量。Figure 2(c)以一回合对话为例展示了该推理流程。

### 创新本质：机制级替代而非增量改进

LLaDA-V的创新并非在自回归框架上的增量修补，而是**对MLLM核心生成机制的范式级替代**。为验证这一替代的公平性，作者在对比LLaMA3-V时，除语言塔外，所有组件（视觉编码器SigLIP 2、MLP投影器、训练数据、训练阶段和超参数）保持完全一致。实验结果表明，纯扩散MLLM不仅在多数基准上达到或超越自回归基线，还展现出更优的数据可扩展性——使用1M训练样本时，LLaDA-V的性能已超过使用9M样本的LLaMA3-V（Figure 3），尤其在MMMU、MMMU-Pro等多学科知识任务上优势显著。这证明了扩散机制本身是多模态理解的关键赋能因素，而非语言塔能力的附带效应。



LLaDA-V 的整体框架遵循标准的多模态大语言模型（MLLM）视觉指令微调范式，但其核心创新在于将语言塔从传统的自回归模型替换为**纯掩码扩散模型**。整个 pipeline 由三个关键模块串联构成，形成“视觉编码 → 特征投影 → 扩散生成”的信息流。

### 模块构成与数据流

**视觉编码器 (Vision Tower)** 采用 **SigLIP 2**，负责将输入图像转换为视觉特征表示。每张图像被处理为 384×384 分辨率，输出 729 个视觉 token，作为后续模块的输入。

**MLP 投影器 (MLP Connector)** 是一个随机初始化的两层 MLP，其作用是将视觉特征映射到语言塔的 token 嵌入空间，实现模态对齐。在第一阶段训练中，仅该投影器参与训练，视觉编码器和语言塔保持冻结。

**语言塔 (Language Tower)** 使用 **LLaDA-8B-Instruct**，这是一个基于掩码扩散的大语言模型。与自回归模型不同，LLaDA 采用**双向注意力机制**（无因果掩码），使每个 token 能够关注序列中的所有其他 token。该设计摒弃了 KV 缓存，使用标准多头注意力。

### 训练与推理的扩散机制

LLaDA-V 的训练和推理完全基于掩码扩散框架，与自回归模型的逐 token 预测形成根本性差异。

**训练阶段**（图 2b）：给定图像特征和输入提示（prompt），模型仅对**回答部分**（response）的 token 进行随机掩码，然后预测被掩码 token 的真实值。图像特征和提示 token 始终保持完整、不被掩码。训练目标是公式 (1) 所示的负对数似然上界：

$$- \mathbb { E } _ { \boldsymbol { v } , t , \boldsymbol { p _ { 0 } ^ { 1 } } , \boldsymbol { r } _ { 0 } ^ { 1 } , \boldsymbol { r } _ { t } ^ { 1 } } , \left[ \frac { 1 } { t } \sum _ { i = 1 } ^ { L _ { r 1 } } \sum _ { j = 1 } ^ { L _ { r 2 } } \mathbf { 1 } [ \boldsymbol { r } _ { t } ^ { 1 , i } = [ \mathbf { M } ] \wedge \boldsymbol { r } _ { t } ^ { 2 , j } = [ \mathbf { M } ] ] \log _ { \mathcal { P } _ { \boldsymbol { \theta } } } ( \boldsymbol { r } _ { 0 } ^ { 1 , i } , \boldsymbol { r } _ { 0 } ^ { 2 , j } | \boldsymbol { v } , \boldsymbol { p } _ { 0 } ^ { 1 } , \boldsymbol { r } _ { t } ^ { 1 } , \boldsymbol { p } _ { 0 } ^ { 2 } , \boldsymbol { r } _ { t } ^ { 2 } ) \right]$$

其中 $\boldsymbol{v}$ 为图像特征，$\boldsymbol{p}$ 为提示，$\boldsymbol{r}$ 为回答，$[\mathbf{M}]$ 为掩码标记。

前向扩散过程（公式 2）以概率 $1-\alpha_t$ 将 token 替换为掩码标记：

$$q_{t|0}(\pmb{x}_t|\pmb{x}_0) = \prod_{i=0}^{N-1} q_{t|0}(\pmb{x}_t^i|\pmb{x}_0^i) \quad \mathrm{and} \quad q_{t|0}(\pmb{x}_t^i|\pmb{x}_0^i) = \left\{ \begin{array}{ll} \alpha_t, & \pmb{x}_t^i = \pmb{x}_0^i, \\ 1-\alpha_t, & \pmb{x}_t^i = [\pmb{\mathrm{M}}]. \end{array} \right.$$

**推理阶段**（图 2c）：从时间步 $t=1$ 的全掩码回答序列出发，模型通过反向过程（公式 3）逐步去掩码。每一步中，模型预测所有被掩码 token 的取值，并采用**低置信度重掩码策略**——仅保留置信度最高的预测结果，其余 token 在下一轮继续被掩码。随着 $t$ 从 1 递减至 0，回答逐步从全掩码状态演化为完整文本。

$$q_{s|t}(\pmb{x}_s|\pmb{x}_t) = \prod_{i=0}^{N-1} q_{s|t}(\pmb{x}_s^i|\pmb{x}_t) \mathrm{~and~} q_{s|t}(\pmb{x}_s^i|\pmb{x}_t) = \left\{ \begin{array}{ll} 1, & \pmb{x}_t^i \neq [\pmb{\mathrm{M}}], \pmb{x}_s^i = \pmb{x}_t^i, \\ \frac{1-\alpha_s}{1-\alpha_t}, & \pmb{x}_t^i = [\pmb{\mathrm{M}}], \pmb{x}_s^i = [\pmb{\mathrm{M}}], \\ \frac{\alpha_s-\alpha_t}{1-\alpha_t} p_\theta(\pmb{x}_0^i|\pmb{x}_t), & \pmb{x}_t^i = [\pmb{\mathrm{M}}], \pmb{x}_s^i \neq [\pmb{\mathrm{M}}], \\ 0, & \mathrm{otherwise}. \end{array} \right.$$

### 注意力机制选择

LLaDA-V 对比了两种注意力掩码策略（图 4）：
- **对话因果掩码**：允许同一轮对话内 token 相互关注，但保持轮次间的因果性。
- **无掩码（双向注意力）**：所有 token 可关注序列中的任意位置。

消融实验（Table 4）表明，双向注意力在 12 个基准中的 7 个上表现更优，尤其在 MMMU、MuirBench 等多学科知识和多图推理任务上提升显著。因此 LLaDA-V 最终采用无掩码的双向注意力。

### 与自回归基线的关键差异

为进行公平对比，LLaDA-V 与自回归基线 **LLaMA3-V** 保持所有其他组件完全一致——相同的视觉编码器（SigLIP 2）、MLP 投影器、训练数据（MAmmoTH-VL、VisualWebInstruct 等）、多阶段训练流程和超参数。唯一变化的槽位是将语言塔从 LLaMA3-8B（因果注意力、下一个 token 预测、自回归生成）替换为 LLaDA-8B（双向注意力、掩码预测、迭代去掩码生成）。这一受控对比设计使得性能差异可直接归因于扩散机制与自回归机制的差异。

### 补充图表

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Autoregressive Approaches and LLaDA-V. Image representations are generated by an encoder and an MLP projector (not explicitly shown). (a) Autoregressive Training: Given image features and the input prompt, autoregressive models are trained to predict the response through next-token prediction. (b) LLaDA-V’s Training: Image features and the input prompt remain unmasked, while only the response is randomly masked. (c) LLaDA-V’s Inference: As time step t decreases from 1 to 0, generation begins with a fully masked response and iteratively predicts tokens*



### 方法架构概览

LLaDA-V 沿用了经典视觉指令微调的三模块架构，但将核心的语言塔从自回归模型替换为**掩码扩散模型**，形成纯扩散多模态大语言模型。架构由以下模块构成（见 Figure 2）：

1. **视觉编码器 (Vision Tower)**：采用 **SigLIP 2**，将输入图像编码为视觉特征表示，每张图像生成 729 个视觉 token（对应 384×384 分辨率）。
2. **MLP 投影器 (MLP Connector)**：一个随机初始化的两层 MLP，将视觉特征映射到语言塔的词嵌入空间，实现模态对齐。
3. **语言塔 (Language Tower)**：使用 **LLaDA-8B-Instruct**，一个基于掩码扩散的大语言模型。其核心特性是采用**双向注意力机制**（无因果掩码），不依赖 KV 缓存，使用标准多头注意力。

与自回归基线 **LLaMA3-V** 的关键差异在于：LLaDA-V 仅替换了语言塔，其余组件（视觉编码器、MLP 投影器、训练数据、训练阶段和超参数）保持完全一致，确保对比的公平性。

### 核心公式推导

#### 训练目标：掩码预测损失

LLaDA-V 的训练过程只对**回答部分**进行随机掩码，图像特征和提示词保持完整。给定图像 $\boldsymbol{v}$、提示 $\boldsymbol{p}_0^1$ 和原始回答 $\boldsymbol{r}_0^1$，前向过程在时间步 $t$ 将回答中的部分 token 替换为掩码标记 $[\mathbf{M}]$，得到 $\boldsymbol{r}_t^1$。模型需要根据未掩码的上下文预测被掩码的 token。训练目标为：

$$-\mathbb{E}_{\boldsymbol{v}, t, \boldsymbol{p}_0^1, \boldsymbol{r}_0^1, \boldsymbol{r}_t^1}\left[\frac{1}{t}\sum_{i=1}^{L_{r1}}\sum_{j=1}^{L_{r2}}\mathbf{1}[\boldsymbol{r}_t^{1,i}=[\mathbf{M}]\wedge\boldsymbol{r}_t^{2,j}=[\mathbf{M}]]\log_{\mathcal{P}_{\boldsymbol{\theta}}}(\boldsymbol{r}_0^{1,i},\boldsymbol{r}_0^{2,j}|\boldsymbol{v},\boldsymbol{p}_0^1,\boldsymbol{r}_t^1,\boldsymbol{p}_0^2,\boldsymbol{r}_t^2)\right]$$

**变量含义**：
- $\boldsymbol{v}$：图像特征
- $\boldsymbol{p}_0^1, \boldsymbol{p}_0^2$：多轮对话中的提示序列（保持未掩码）
- $\boldsymbol{r}_0^1, \boldsymbol{r}_0^2$：原始回答序列
- $\boldsymbol{r}_t^1, \boldsymbol{r}_t^2$：在时间步 $t$ 被部分掩码后的回答序列
- $[\mathbf{M}]$：掩码标记
- $t$：掩码比例（时间步），$t$ 越大掩码比例越高
- $\mathcal{P}_{\boldsymbol{\theta}}$：模型预测的 token 概率分布

该目标已被证明是**掩码 token 负对数似然的上界**，为扩散模型的训练提供了理论保证。

#### 掩码扩散的前向过程

前向过程独立地对每个 token 进行掩码操作。给定原始序列 $\boldsymbol{x}_0$，在时间步 $t$ 的掩码序列 $\boldsymbol{x}_t$ 的分布为：

$$q_{t|0}(\boldsymbol{x}_t|\boldsymbol{x}_0) = \prod_{i=0}^{N-1} q_{t|0}(\boldsymbol{x}_t^i|\boldsymbol{x}_0^i) \quad \text{且} \quad q_{t|0}(\boldsymbol{x}_t^i|\boldsymbol{x}_0^i) = \begin{cases} \alpha_t, & \boldsymbol{x}_t^i = \boldsymbol{x}_0^i, \\ 1-\alpha_t, & \boldsymbol{x}_t^i = [\mathbf{M}]. \end{cases}$$

**变量含义**：
- $\boldsymbol{x}_0^i$：原始序列中第 $i$ 个 token
- $\boldsymbol{x}_t^i$：时间步 $t$ 时第 $i$ 个 token
- $\alpha_t$：保留概率（随 $t$ 减小而增大）
- $1-\alpha_t$：被掩码的概率

在训练中，$\alpha_t$ 从 1 线性递减到 0，对应掩码比例从 0% 增加到 100%。

#### 掩码扩散的反向过程（推理生成）

推理时从全掩码序列出发（$\alpha_0=0$），逐步去掩码生成回答。反向过程从时间步 $t$ 到 $s$（$s < t$）的转移概率为：

$$q_{s|t}(\boldsymbol{x}_s|\boldsymbol{x}_t) = \prod_{i=0}^{N-1} q_{s|t}(\boldsymbol{x}_s^i|\boldsymbol{x}_t) \quad \text{且} \quad q_{s|t}(\boldsymbol{x}_s^i|\boldsymbol{x}_t) = \begin{cases} 1, & \boldsymbol{x}_t^i \neq [\mathbf{M}], \boldsymbol{x}_s^i = \boldsymbol{x}_t^i, \\ \frac{1-\alpha_s}{1-\alpha_t}, & \boldsymbol{x}_t^i = [\mathbf{M}], \boldsymbol{x}_s^i = [\mathbf{M}], \\ \frac{\alpha_s-\alpha_t}{1-\alpha_t} p_\theta(\boldsymbol{x}_0^i|\boldsymbol{x}_t), & \boldsymbol{x}_t^i = [\mathbf{M}], \boldsymbol{x}_s^i \neq [\mathbf{M}], \\ 0, & \text{otherwise}. \end{cases}$$

**变量含义**：
- $\boldsymbol{x}_t$：当前时间步的序列（部分掩码）
- $\boldsymbol{x}_s$：前一时间步的序列（更少掩码）
- $p_\theta(\boldsymbol{x}_0^i|\boldsymbol{x}_t)$：模型预测第 $i$ 个 token 为原始 token 的概率
- $\frac{\alpha_s-\alpha_t}{1-\alpha_t}$：去掩码概率，控制从掩码到真实 token 的转移

**推理策略**：LLaDA-V 继承 LLaDA 的**低置信度重掩码策略**——在每次迭代中，模型预测所有掩码 token 的概率分布，选择置信度最低的部分 token 保留掩码状态，其余替换为预测值。消融实验表明该策略相比随机重掩码可稳定提升生成质量。

### 注意力机制选择

LLaDA-V 采用**双向注意力**（无掩码），使每个 token 可以关注序列中的所有 token（Figure 4c）。消融实验（Table 4）对比了两种策略：
- **对话因果掩码**：轮次内全注意力，轮次间保持因果性
- **无掩码（双向注意力）**：完全双向注意力

在 12 个基准测试中的 7 个上，双向注意力表现更优，尤其在 MMMU、MuirBench 等需要深度推理的任务上提升明显。因此 LLaDA-V 最终采用无掩码策略。

### 补充图表

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/009_Figure_4.jpg]]
*Figure 4: Overview of Attention Masks. (a) Standard causal mask used in autoregressive models like Qwen2-VL and LLaMA3-V, where tokens attend only to themselves and previous tokens. (b) Dialogue causal mask allowing full attention within turns while maintaining causality between turns. (c) Bidirectional attention in LLaDA-V, enabling tokens to attend to all tokens in the sequence. Note: In the figure, PRM represents prompt and RES represents response*



## 实验与关键发现

### 核心结果：多学科知识与数学推理

LLaDA-V在多学科知识与数学推理任务上展现出显著优势。与自回归基线**LLaMA3-V**（使用相同视觉塔、MLP投影器、训练数据与流程，仅语言塔替换为LLaMA3-8B）相比，LLaDA-V在9个基准中的6个上取得领先（Table 2）。其中，**MMMU**（48.6% vs. 45.4%，+3.2）和**MMMU-Pro**（35.2% vs. 28.3%，+6.9）的增益尤为突出，表明纯扩散机制在需要深度跨学科推理的场景中具有独特优势。在**MME**认知分数上，LLaDA-V同样高出45分（491 vs. 446），但感知分数落后74分（1507 vs. 1581），提示扩散模型在细粒度视觉感知上仍存在短板。

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/005_Table_2.jpg]]
*Table 2: Benchmark Results for Multidisciplinary Knowledge and Mathematical Reasoning Tasks. “Diffusion” here encompasses both continuous and discrete diffusion models. Notably, LLaDA-V outperforms all other hybrid and pure diffusion MLLMs, surpassing LLaMA3-V on 6 of 9 benchmarks despite having a relatively weaker language tower. For comparison, we list each model’s language tower, as this significantly impacts MLLM performance. “-” indicates unavailable data*

与更强大的自回归模型**Qwen2-VL**（语言塔为Qwen2-7B）对比，LLaDA-V在MMStar上仅落后0.6个百分点（60.1% vs. 60.7%），差距已大幅缩小。在扩散模型体系内，LLaDA-V全面超越混合自回归-扩散模型**Show-o**和**MetaMorph**，成为当前纯扩散MLLM中的最优方案（Figure 1(b)）。

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/001_Figure_1.jpg]]
*Figure 1: Benchmark Results. (a) LLaDA-V demonstrates superior performance on more benchmarks compared to LLaMA3-V when trained on the same dataset, particularly excelling in multidisciplinary knowledge and mathematical reasoning tasks. (b) LLaDA-V achieves state-of-the-art performance in multimodal understanding among both hybrid autoregressive-diffusion (such as MetaMorph [31] and Show-o [28]) and purely diffusion-based models*

### 图表、文档、真实场景与多图/视频任务

在图表与文档理解任务上，LLaDA-V与LLaMA3-V表现基本持平（Table 3）：**AI2D**（77.8% vs. 81.1%，-3.3）、**DocVQA**（具体数值未列出但文中描述为“comparable”）。真实世界场景理解是LLaDA-V的相对弱项，**RealworldQA**落后2.8个百分点（63.2% vs. 66.0%），这与MME感知分数偏低的趋势一致。

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/006_Table_3.jpg]]
*Table 3: Benchmark Results for Chart, Document, Real-world Scene, Multi-image, and Video Tasks. “Diffusion” here encompasses both continuous and discrete diffusion models. Compared to LLaMA3-V, LLaDA-V shows comparable performance on chart/document tasks, performs less well on real-world scenes, but excels in multi-image and video tasks. “-” indicates missing data*

然而，在多图与视频任务上，扩散模型的优势再度显现：**MuirBench**（48.3% vs. 47.4%，+0.9）、**MLVU**（59.5% vs. 57.5%，+2.0）。这一现象可能与双向注意力机制有关——在多图对比和视频时序理解中，全局上下文交互比单向因果注意力更具表达力。

### 数据可扩展性

Figure 3揭示了LLaDA-V的关键特性：**数据扩展效率显著优于自回归基线**。在MAmmoTH-VL-SI10M数据集上，随着训练样本从0.1M增至10M，LLaDA-V在多数基准上保持持续增长趋势，而LLaMA3-V在部分任务上出现饱和甚至下降。尤其值得注意的是，LLaDA-V仅使用1M样本时，在MMMU和MMMU-Pro上的性能已超过LLaMA3-V使用9M样本的水平。这一发现暗示，掩码扩散训练目标可能比自回归下一个token预测具有更好的样本效率，对于数据受限的多模态应用场景具有重要实践意义。

### 消融研究：注意力掩码策略

Table 4的消融实验对比了两种注意力掩码策略：**对话因果掩码**（dialogue causal，允许轮次内全注意力但保持轮次间因果性）与**无掩码双向注意力**（no mask）。在12个基准中的7个上，双向注意力取得更优结果，尤其在MMMU、MuirBench等需要跨模态推理的任务上提升明显。这表明，放弃因果约束、允许视觉与文本token完全交互，对扩散MLLM的理解能力有正向贡献。LLaDA-V最终采用无掩码策略。

### 推理机制与效率考量

LLaDA-V的推理采用迭代去掩码生成：从全掩码的响应序列出发，在每个时间步预测所有掩码token的置信度，保留高置信度预测并将低置信度token重新掩码，逐步减少掩码比例直至完全生成。这一**低置信度重掩码策略**继承自LLaDA，相比随机重掩码可稳定提升生成质量，但论文未提供与自回归模型在推理延迟或计算量上的定量对比，效率方面的结论需要手动验证。

### 失败模式与局限性

综合实验结果，LLaDA-V的短板集中在以下方面：
- **细粒度视觉感知**：MME感知分数、RealworldQA等真实场景理解任务持续落后于LLaMA3-V，可能与扩散模型在像素级细节编码上的不足有关。
- **图表与文档理解**：AI2D等结构化视觉任务上存在小幅差距，扩散机制对空间布局和文字定位的建模能力有待加强。
- **语言塔瓶颈**：LLaDA-8B本身的纯文本能力弱于LLaMA3-8B和Qwen2-7B，限制了多模态性能的上限。
- **训练范式缺失**：未使用RLHF/DPO等偏好对齐技术，可能影响对话连贯性和指令跟随的精细度。

### 补充图表

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/004_Figure_3.jpg]]
*Figure 3: Data Scalability of LLaDA-V. Both LLaDA-V and LLaMA3-V were trained on MAmmoTH-VL-SI10M, with performance evaluated across six multimodal benchmarks. Despite having a weaker language tower, LLaDA-V shows superior data scalability across more tasks, especially excelling in multidisciplinary knowledge and mathematical reasoning*

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/007_Table_4.jpg]]
*Table 4: Ablation Studies on Attention Mask. Comparison of LLaDA-8B using different attention masking strategies (dialogue causal vs. no mask) across 12 benchmarks. We adopt the no mask strategy in LLaDA-V as it shows slightly better performance on most benchmarks*

![[assets/figures/papers/paper_list_l2324_https_arxiv_org_abs_2505_16933/figures/003_Table_1.jpg]]
*Table 1: Training Settings. Here M-SI and M-OV represent the single image data and onevision data of MAmmoTH [55], while VW represents the data of VisualWebInstruct [56]. We train LLaDA-V sequentially through the first five datasets (LLaVA-Pretrain [1], M-SI, M-OV, VW, and M-OV+VW), while the last dataset (LLaVA-NeXT [54]) is used for ablation study in Sec. 4.4*



## 定位与知识库关联

### 核心差异与因果机制

LLaDA-V 与现有 MLLM 的根本差异在于**将语言塔从自回归模型置换为掩码扩散模型**，并由此引发训练目标、注意力结构和推理方式的系统性改变。这一置换的因果链条为：训练时对回答部分进行随机掩码并预测（掩码预测损失，见 Eq.(1)），推理时从全掩码序列出发通过迭代去掩码逐步生成回答。该机制使模型在训练阶段即可利用双向注意力（无因果掩码），从而获得更强的上下文建模能力。

- **语言塔**：自回归基线 LLaMA3-V 使用 **LLaMA3-8B**（因果注意力 + 下一个 token 预测）；LLaDA-V 使用 **LLaDA-8B**（双向注意力 + 掩码预测损失）。LLaDA-8B 作为纯文本语言模型整体弱于 LLaMA3-8B，但经视觉指令微调后，LLaDA-V 在多学科知识和数学推理任务上反超自回归基线（Table 2）。
- **注意力结构**：消融实验（Table 4）表明，双向注意力在 12 个基准中的 7 个上优于对话因果注意力，尤其在 MMMU、MuirBench 等任务上提升明显，这为扩散 MLLM 采用无掩码注意力提供了直接证据。
- **推理方式**：LLaDA-V 采用迭代去掩码生成，配合低置信度重掩码策略（继承自 LLaDA ），相比随机重掩码可稳定提升生成质量。

### 与相关工作的关系

LLaDA-V 处于**纯扩散 MLLM**这一新兴方向的前沿位置。现有非自回归 MLLM 主要分为两类：

- **混合自回归‑扩散模型**：如 **Show-o** 和 **MetaMorph**，在框架中同时保留自回归和扩散组件。LLaDA-V 在全部基准上超越这些混合模型（Figure 1 (b), Tables 2 & 3），证明了纯扩散框架在多模态理解中的竞争力。
- **自回归 MLLM**：如 **LLaMA3-V**（自回归基线）、**Qwen2-VL**（强自回归对比方法）。LLaDA-V 在 MMMU、MMMU-Pro 等多学科知识与数学推理基准上超越 LLaMA3-V，但在图表/文档理解（AI2D、DocVQA）和真实世界场景（RealworldQA）上仍落后，显示出扩散模型在不同任务类型上的性能分化。

### 适用边界与局限

1. **任务类型分化**：LLaDA-V 在多学科知识（MMMU +3.2）和数学推理（MMMU-Pro +6.9）上优势明显，但在图表理解（AI2D −3.3）、文档理解和真实场景（RealworldQA −2.8）上落后于自回归基线。这一分化可能与扩散模型的迭代去掩码机制在结构化视觉理解任务中的表现有关，具体原因需进一步验证。
2. **语言塔性能瓶颈**：LLaDA-8B 的整体性能弱于 Qwen2-7B 等先进自回归模型，限制了多模态性能的进一步提升。论文明确指出，更强的扩散语言塔有望进一步缩小与一流自回归 MLLM 的差距。
3. **推理效率**：扩散模型需要多步迭代去掩码，推理速度可能慢于自回归生成，但论文未给出效率对比数据，该点需手动验证。
4. **对齐技术缺失**：训练过程未使用 RLHF/DPO 等偏好对齐技术，可能影响对话和推理能力的细节表现。

### 开放问题

- 能否通过更大规模预训练或更强的扩散语言塔（如未来更强的扩散 LLM）进一步提升纯扩散 MLLM 的性能上限？
- 将偏好对齐（如 RLHF）引入扩散 MLLM 是否会进一步缩小与一流自回归模型的差距？
- 低置信度重掩码策略是否仍可优化，或存在更优的去掩码调度方案？
- 扩散 MLLM 在效率优化（如减少采样步数、引入 KV 缓存等效机制）方面是否能与自回归模型竞争？
- 纯扩散框架能否统一多模态生成（图像+文本）而不依赖自回归模块？



## 原文 PDF

![[paperPDFs/CVPR_2026/LLaDA_V_Large_Language_Diffusion_Models_with_Visual_Instruction_Tuning.pdf]]

---
title: "CigTime: Corrective Instruction Generation Through Inverse Motion Editing"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing.pdf
project_link: null
code_link: null
aliases:
- CigTime
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将纠正指令生成视为运动编辑的逆过程，利用运动编辑管道自动生成三元组训练数据；同时采用运动标记化（VQ-VAE）并结合锚定损失全参数微调大语言模型，使模型能够感知运动差异并输出有效纠正文本。
primary_logic: 纠正指令生成可以看作运动编辑的逆任务，因此可以复用成熟的运动编辑模型来构建大规模训练数据，进而通过针对性微调赋予大语言模型「从运动对推断纠正指令」的能力。
claims:
- 在 HumanML3D 上，CigTime 在所有指令质量指标（BLEU-4 0.24, ROUGE-2 0.35, METEOR 0.52, CLIPScore 0.82）和重建准确性指标（MPJPE 0.13, FID 1.44）上均显著优于 Llama-3-8B、Mistral-7B、MotionGPT 等基线方法。
- 消融实验表明，引入锚定损失的全参数微调策略（Ours）相比于仅扩展词汇表（Ours-Extended）、连续表示（Ours-Continuous）或使用 T5 骨干（Ours-T5），在重建准确性上具有明显优势（MPJPE 0.13 vs. 0.16 ~ 0.33）。
- 在三种不同的运动编辑器（MDM, PriorMDM-LW, PriorMDM-RF）上评估时，CigTime 均取得最低的 MPJPE 和 FID，表明方法对底层编辑器具有良好的泛化性。
- HumanML3D 上 BLEU-4 = 0.24
---

# CigTime: Corrective Instruction Generation Through Inverse Motion Editing

> [!tip] 核心洞察
> 纠正指令生成可以看作运动编辑的逆任务，因此可以复用成熟的运动编辑模型来构建大规模训练数据，进而通过针对性微调赋予大语言模型「从运动对推断纠正指令」的能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | CigTime：通过逆向运动编辑生成纠正指令 |
| 英文题名 | CigTime: Corrective Instruction Generation Through Inverse Motion Editing |
| 会议/期刊 | NEURIPS 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CigTime |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，BLEU-4 0.24 vs 0.15 (Llama-3-8B) (+0.09)；ROUGE-2 0.35 vs 0.30 (Mistral-7B) (+0.05)；METEOR 0.52 vs 0.46 (Mistral-7B) (+0.06)。

## 概要

**问题瓶颈** 在人体运动分析与教学场景中，自动生成精准的纠正性文本指令面临双重困难：其一，缺乏大规模、通用的（源运动，目标运动，纠正指令）三元组训练数据；其二，现有语言模型难以直接理解动态运动序列之间的空间与时间差异，无法可靠地输出“哪里错了、如何改正”的细粒度文本。

**核心思路** CigTime 将纠正指令生成视为运动编辑的逆过程，提出一条“以编辑驱动生成”的闭环流水线：先利用预训练运动编辑器自动构建大规模三元组数据，再通过运动标记化与锚定损失微调大语言模型，使模型具备从运动对推断纠正指令的能力。这一设计的关键因果杠杆在于，复用成熟的运动编辑模型解决了数据匮乏问题，而全参数微调加锚定损失则保证了运动标记与语言空间的稳定对齐。

**方法定位** 在方法谱系上，CigTime 处于运动编辑、运动‑语言对齐与大语言模型微调的交汇点。与通用大语言模型（如 **Llama-3-8B**、**Mistral-7B**）依赖上下文学习生成指令不同，CigTime 通过 VQ-VAE 将运动序列量化为离散标记，并以全参数微调方式将运动差异感知能力注入语言模型；与 **MotionGPT** 等运动‑语言模型相比，CigTime 并非直接描述目标运动，而是显式建模源运动到目标运动的变化，从而输出更具纠正性的指令。

**主要结果** 在 HumanML3D 基准上，CigTime 在指令质量与重建准确性上均显著优于已有方法：BLEU-4 达 0.24，ROUGE-2 达 0.35，METEOR 达 0.52，CLIPScore 达 0.82；同时，重建误差 MPJPE 低至 0.13，FID 降至 1.44，相比 Llama-3-8B 分别降低 0.08 和 1.60（Table 1）。消融实验进一步证实，全参数微调结合锚定损失是性能提升的关键设计选择（Table 2），且方法在三种不同运动编辑器上均保持最低的 MPJPE 和 FID，展现出良好的泛化鲁棒性（Table 3）。



近年来，随着计算机视觉与自然语言处理技术的深度融合，人类运动理解取得了显著进展。然而，现有研究主要聚焦于运动生成与运动描述，即从文本生成运动或从运动生成文本。一个关键但尚未被充分探索的问题是**纠正指令生成（corrective instruction generation）**：给定一段源运动与一段目标运动，自动生成自然语言形式的纠正性反馈，以指导用户如何从源运动改进到目标运动。

该任务面临两个核心瓶颈。其一，**缺乏大规模、通用的（源运动，目标运动，纠正指令）三元组训练数据**。人工标注此类数据成本极高，且难以覆盖多样化的运动类型与纠正意图。其二，**现有语言模型难以理解动态运动序列之间的空间与时间差异**。通用大语言模型（如 Llama-3-8B、Mistral-7B）虽然具备强大的文本生成能力，但将运动序列直接输入时，模型无法有效感知两个运动序列之间的细微偏差，导致生成的纠正文本缺乏针对性与准确性。现有的运动‑语言模型（如 MotionGPT）虽然能够处理运动与文本的联合表示，但其设计目标并非推断运动对之间的差异，因此在纠正指令生成任务上表现不佳。

针对上述瓶颈，本文提出了 **CigTime**，其核心洞察在于：**纠正指令生成可以视为运动编辑的逆任务**。现有的运动编辑模型已经能够根据源运动与纠正指令生成目标运动，那么反过来，我们可以利用运动编辑管道自动构建大规模三元组训练数据，进而通过针对性微调赋予大语言模型“从运动对推断纠正指令”的能力。这一思路绕过了人工标注的困境，同时使模型能够从数据中隐式学习运动差异与语言指令之间的映射关系。



## 核心方法与创新机理

CigTime 的核心创新在于将**纠正指令生成**形式化为**运动编辑的逆过程**，从而绕过了该任务最根本的数据瓶颈：缺乏大规模、高质量的（源运动，目标运动，纠正指令）三元组。传统方法依赖人工标注或少量样本提示，成本高昂且难以规模化。CigTime 则利用成熟的运动编辑管道，以“源运动 + 纠正指令 → 目标运动”的正向编辑能力为基础，反向自动构建训练数据，使大语言模型能够从运动对中推断出精确的纠正文本。

围绕这一核心洞察，方法在三个关键维度上实现了相对基线的根本性改变：

**1. 数据收集方式：从人工标注到运动编辑驱动的自动生成**

基线方法（如 Llama-3-8B、Mistral-7B 的上下文学习变体）直接依赖预训练语言模型的理解能力，缺乏针对性的训练数据。CigTime 则利用预训练运动编辑器（MDM），以源运动与纠正指令为输入生成目标运动，从而自动获得 $(\text{源运动}, \text{目标运动}, \text{纠正指令})$ 三元组（见 3.2 节）。对于仅需编辑特定身体部位（如“举起手臂”）的场景，通过部位掩码 $m$ 将编辑后的局部运动 $x^L$ 与源运动 $x^I$ 进行融合：

$$x^O = m \odot x^L + (1 - m) \odot x^I$$

这一策略使得训练数据的规模与多样性不再受限于人工标注预算，为后续的模型训练提供了基础。

**2. 运动表征：从连续特征到离散运动标记**

基线方法通常将运动序列视为连续特征向量（如 Ours-Continuous 变体），或简单地为运动标记扩展 LLM 词汇表（如 Ours-Extended 变体）。CigTime 则采用 VQ-VAE 网络将运动序列量化为离散标记，通过编码器 $E$、码本 $C$ 和解码器 $D$ 的协同训练，将逐帧特征 $f_i$ 映射到码本中最近邻的离散编码：

$$z_i = Q(f_i) = c_k, \text{ where } k = \arg\min_j \|f_i - c_j\|_2^2$$

这一设计的优势在于：离散标记与语言模型的 token 空间自然对齐，同时保留了原有词汇表的语义完整性，避免了扩展词汇表导致的嵌入空间紊乱。

**3. 语言模型微调策略：从上下文学习/LoRA 到全参数微调 + 锚定损失**

基线方法要么仅通过上下文学习（in-context learning）提示 LLM 生成指令（如 Llama-3-8B、Mistral-7B），要么采用轻量级 LoRA 适配器微调（如 Llama-3-8B-LoRA、Mistral-7B-LoRA）。这些策略对运动标记这一全新模态的适应能力有限。CigTime 则对 Llama-3-8B 进行全参数微调，并引入**锚定损失**（anchor loss）作为关键正则化手段：

$$\mathcal{L}^{Anch} = \lambda \cdot \| W - W_0 \|_2^2$$

该损失约束网络权重 $W$ 不过度偏离预训练值 $W_0$，防止在引入运动标记后语言模型的嵌入空间发生灾难性发散。消融实验（Table 2）证实，这一设计是重建准确性的关键保障：全参数微调 + 锚定损失的 MPJPE 为 0.13，而仅扩展词汇表（Ours-Extended）为 0.33，连续表示（Ours-Continuous）为 0.16，T5 骨干（Ours-T5）为 0.22。

综上，CigTime 的创新并非单一技术点的改进，而是通过“逆运动编辑”这一统一视角，系统性地重构了数据生成、运动表征和模型微调三个环节，使通用大语言模型首次具备了从运动对差异中推断精确纠正指令的能力。



CigTime 的核心思路是将纠正指令生成任务建模为运动编辑的逆过程。给定源运动序列 $x^I \in \mathbb{R}^{T \times D}$ 和目标运动序列 $x^O \in \mathbb{R}^{T \times D}$，模型学习一个映射函数 $\tau$，使得 $\tau(x^I, x^O) = L$，其中 $L$ 为纠正性文本指令。整个 pipeline 由三个关键模块串联构成，形成“数据生成—运动标记化—指令推理”的端到端流程。

**模块一：基于运动编辑的数据收集。** 该模块利用预训练的运动编辑器（如 MDM），以源运动和纠正指令为输入，生成目标运动，从而自动构建大规模（源运动，目标运动，纠正指令）三元组训练数据。这一设计从根本上解决了该任务缺乏标注数据的瓶颈——传统方法依赖人工标注或少量样本提示，难以规模化。生成目标运动时，通过部位掩码 $m$ 将编辑后的运动 $x^L$ 与源运动 $x^I$ 按 $x^O = m \odot x^L + (1 - m) \odot x^I$ 进行融合，确保仅目标身体部位被修改。

**模块二：VQ-VAE 运动标记化。** 源运动与目标运动序列通过 VQ-VAE 网络被量化为离散标记。该网络包含编码器 $E$、码本 $C$ 和解码器 $D$，逐帧特征 $f_i$ 经最近邻查找 $z_i = Q(f_i) = c_k,\ \text{where}\ k = \arg\min_j \|f_i - c_j\|_2^2$ 映射到码本向量。训练时同时优化重构损失 $\mathcal{L}^{recon} = \|x^O - x^{O'}\|_2^2$ 和承诺损失 $\mathcal{L}^{com} = \sum_{i=1}^T \|f_i - sg(z_i)\|_2^2$，在保留运动信息的同时将连续运动转化为大语言模型可理解的离散符号序列。

**模块三：LLM 微调与指令生成。** 将源运动标记 $U^I$ 和目标运动标记 $U^O$ 按预定义模板组织（见图 2），输入大语言模型（Llama-3-8B）进行全参数微调。训练目标为最大化纠正指令标记的对数似然 $\mathcal{L}^{LLM} = -\sum_{j=0}^{U^o} \log p_{\mathcal{L}}(u_j^O | u_{0:j-1}^O, U^I)$，同时引入锚定损失 $\mathcal{L}^{Anch} = \lambda \cdot \| W - W_0 \|_2^2$ 防止模型权重 $W$ 过度偏离预训练值 $W_0$，从而在注入运动理解能力的同时保持语言生成质量。

三个模块形成闭合回路：运动编辑器提供训练信号，VQ-VAE 充当运动与语言之间的桥梁，微调后的 LLM 则从运动对中推断出精准的纠正指令。这一设计使得 CigTime 在无需人工标注的情况下，即能赋予通用大语言模型“从运动差异理解纠正意图”的能力。

### 补充图表

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/001_Figure_1.jpg]]
*Figure 1: Overview of CigTime. Left: We leverage source motion tokens and corrective instructions as input to a motion editor to produce target motion tokens. Right: We then employ a language model to generate precise corrective instructions based on a given source and target motion. We demonstrate in the example generating corrective instructions for lifting weights with the upper body*



CigTime 的核心架构由三个紧密协作的模块构成：运动编辑器、VQ‑VAE 标记化器以及经过锚定损失微调的大语言模型。整个流程将纠正指令生成视为运动编辑的逆过程，从而复用成熟的运动编辑管道自动构建训练三元组，再通过离散运动标记与全参数微调赋予 LLM“从运动对推断纠正指令”的能力。

### 1. 运动编辑与数据生成模块

该模块的核心思想是将函数 $\tau(x^I, x^O) = L$（即将源运动 $x^I$ 与目标运动 $x^O$ 映射到纠正文本指令 $L$）的实现，建立在对运动编辑过程的逆向利用之上。具体而言，论文采用预训练的 **MDM**（Motion Diffusion Model）作为运动编辑器，其前向扩散过程定义为马尔可夫链：

$$q(\boldsymbol{x}_{1:T} | \boldsymbol{x}_0) = \prod_{t \geq 1} q(\boldsymbol{x}_t | \boldsymbol{x}_{t-1})$$

其中每一步为受方差调度 $\alpha_t$ 控制的高斯转移：

$$q(x_t | x_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}, (1 - \alpha_t) \mathbf{I})$$

可学习的反向去噪过程则建模为：

$$p_\theta(x_{0:T}) = p(x_T) \prod_{t \geq 1} p_\theta(x_{t-1} | x_t)$$

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \sigma_t^2 \mathbf{I})$$

在数据收集阶段，给定源运动 $x^I$ 和一条纠正文本指令，运动编辑器生成编辑后的运动 $x^L$。随后，通过一个部位掩码 $m$ 将源运动与编辑后的运动进行混合，得到最终的目标运动 $x^O$：

$$x^O = m \odot x^L + (1 - m) \odot x^I$$

这一混合机制确保仅指定的身体部位被编辑，其余部位保持与源运动一致。通过大规模采样源运动与纠正指令，该管道自动生成海量的（源运动，目标运动，纠正指令）三元组，解决了该领域训练数据匮乏的根本瓶颈。

### 2. VQ‑VAE 运动标记化模块

为了让大语言模型能够理解连续的运动序列，CigTime 引入了一个基于 VQ‑VAE 的标记化网络，包含编码器 $E$、码本 $C$ 和解码器 $D$。对于每一帧运动特征 $f_i$，量化操作将其映射到码本中欧氏距离最近的离散编码：

$$z_i = Q(f_i) = c_k, \text{ where } k = \arg\min_j \|f_i - c_j\|_2^2$$

该模块通过两项损失进行预训练。重构损失保证解码后的运动序列与原始目标运动一致：

$$\mathcal{L}^{recon} = ||x^O - x^{O'}||_2^2$$

承诺损失则鼓励编码器输出靠近选定的码本向量，避免码本空间被浪费：

$$\mathcal{L}^{com} = \sum_{i=1}^T ||f_i - sg(z_i)||_2^2$$

其中 $sg(\cdot)$ 表示停止梯度算子。经过训练后，源运动与目标运动均被量化为离散标记序列，作为 LLM 的输入。

### 3. LLM 微调与锚定损失模块

CigTime 采用 **Llama-3-8B** 作为骨干语言模型，并通过全参数微调使其能够根据源/目标运动标记生成纠正指令文本。输入按照预设模板组织（见 Figure 2），同时包含源运动标记、目标运动标记以及任务描述。模型通过最大化纠正指令标记的对数似然进行优化：

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/002_Figure_2.jpg]]
*Figure 2: Template for LLM fine-tuning. The LLM is required to output the corrective instructions given token lists for the source and target motion sequences (i.e., Action 1 and Action 2) as well as instructions on the expected output*

$$\mathcal{L}^{LLM} = -\sum_{j=0}^{U^o} \log p_{\mathcal{L}}(u_j^O | u_{0:j-1}^O, U^I)$$

其中 $U^I$ 为输入的源/目标运动标记序列，$u_j^O$ 为输出的纠正指令标记。

全参数微调虽然能充分赋予 LLM 运动感知能力，但也可能导致嵌入层权重 $W$ 过度偏离预训练值 $W_0$，从而损害模型原有的语言理解能力。为此，论文引入锚定损失作为正则化约束：

$$\mathcal{L}^{Anch} = \lambda \cdot \| W - W_0 \|_2^2$$

消融实验（Table 2）表明，引入锚定损失的全参数微调策略在重建准确性上显著优于仅扩展词汇表（Ours‑Extended）、连续表示（Ours‑Continuous）或使用 T5 骨干（Ours‑T5）的变体，其中 MPJPE 从 0.16 ~ 0.33 降至 0.13，验证了该模块在保持嵌入语义稳定性方面的关键作用。



## 实验与关键发现

### 核心实验设置

CigTime 的实验主要围绕两个维度展开：**指令文本质量**（BLEU-4、ROUGE-2、METEOR、CLIPScore）和**运动重建准确性**（MPJPE、FID）。数据集采用 HumanML3D，基线方法包括通用大语言模型（Llama-3-8B、Llama-3-8B-LoRA、Mistral-7B、Mistral-7B-LoRA）和运动‑语言模型（MotionGPT、MotionGPT-M2T）。

### 主实验结果

Table 1 汇总了各方法在指令生成与运动重建两个维度上的对比。CigTime 在所有指标上均显著优于基线：

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/003_Table_1.jpg]]
*Table 1: Comparison to the Existing Work. We compare our approach against large language (Llama-3-8B, Llama-3-8B-LoRA, Qwen-7B, Mistral-7B) and motion-language (MotionGPT, MotionGPT-M2T) models. We demonstrate that our approach, CigTime outperforms all the baselines by a large margin for corrective instruction generation for human motion*

- **指令质量**：BLEU-4 达到 0.24（Llama-3-8B 为 0.15，提升 60%），ROUGE-2 达到 0.35（Mistral-7B 为 0.30），METEOR 达到 0.52（Mistral-7B 为 0.46），CLIPScore 达到 0.82（Llama-3-8B 为 0.77）。这表明模型生成的纠正指令在 n‑gram 重叠、语义相似性和视觉‑语言对齐方面均优于基线。
- **运动重建**：MPJPE 降至 0.13（Llama-3-8B 为 0.21，降低 38%），FID 降至 1.44（Llama-3-8B 为 3.04，降低 47%）。这意味着 CigTime 生成的指令能更准确地驱动运动编辑器还原目标运动，验证了“指令‑运动”映射的可靠性。

值得注意的是，通用 LLM 的上下文学习（in-context learning）变体在指令质量上表现尚可，但运动重建指标明显较差，说明**仅靠文本层面的对齐不足以捕捉运动序列间的时空差异**。MotionGPT 及其 M2T 变体虽然具备运动‑语言联合建模能力，但在纠正指令这一特定任务上仍落后于 CigTime，进一步印证了专门化训练数据与微调策略的必要性。

### 网络结构消融

Table 2 展示了不同网络结构变体的消融结果，核心对比包括：

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/004_Table_2.jpg]]
*Table 2: Ablation study with different network structure. We extend the LLMs’ vocabularies with new learnable embeddings for the motion tokens and update the corresponding embeddings during fine-tuning as baselines. We also compare variants that utilizes T5 as the backbone (ours-T5), and continous representaion (Ours-Continuous)*

- **Ours-Extended**：仅扩展 LLM 词汇表，为运动标记添加新的可学习嵌入，并在微调时更新这些嵌入。
- **Ours-Continuous**：使用连续运动特征表示，而非离散标记。
- **Ours-T5**：将骨干网络替换为 T5。
- **Ours**：全参数微调 + 锚定损失（anchor loss）。

结果表明，全参数微调 + 锚定损失的组合在重建准确性上具有明显优势（MPJPE 0.13），显著优于 Ours-Extended（MPJPE 0.16）、Ours-Continuous（MPJPE 0.21）和 Ours-T5（MPJPE 0.33）。这一差距揭示了两个关键机制：

1. **扩展词汇表策略的局限性**：仅新增嵌入而不约束原有语义空间，容易导致嵌入发散，破坏 LLM 预训练获得的语言先验。
2. **锚定损失的作用**：通过 $\mathcal{L}^{Anch} = \lambda \cdot \| W - W_0 \|_2^2$ 约束网络权重不过度偏离预训练值，在引入运动模态的同时保留了语言理解能力。

T5 骨干的较差表现可能源于其编码器‑解码器架构与自回归指令生成任务之间的适配性不足。

### 运动编辑器泛化性

Table 3 评估了不同运动编辑器（MDM、PriorMDM-LW、PriorMDM-RF）下各方法的重建鲁棒性。CigTime 在三种编辑器上均取得最低的 MPJPE 和 FID，表明该方法**不依赖于特定编辑器的实现细节**，具有良好的泛化性。这一特性源于训练数据的生成方式——三元组数据由运动编辑管道自动生成，模型学习的是“运动对→指令”的通用映射，而非特定编辑器的内部表征。

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/005_Table_3.jpg]]
*Table 3: Ablation study with different motion editors. We assess the reconstruction accuracy of various methods employing different motion editors for evaluation*

### 跨数据集泛化与局限

Table 4（Fit3D）和 Table 5（KIT）展示了跨数据集迁移的结果。CigTime 在这些数据集上仍保持相对优势，但指令文本形式出现较大偏差。这暴露了当前方法的一个关键瓶颈：**训练数据分布对指令风格的影响**。HumanML3D 上的纠正指令偏向动作描述，而 Fit3D 等数据集可能需要更精细的形式与动态反馈。

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/008_Table_4.jpg]]
*Table 4: Numeric Results*

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/012_Table_5.jpg]]
*Table 5: Experimental results on KIT dataset. We conduct a comparative analysis of our method against baselines on the KIT dataset*

### 真实场景应用

Figure 6 展示了从真实参与者视频中提取运动并生成纠正指令的端到端流程。使用单目相机采集视频，通过 WHAM 提取运动序列，CigTime 能够生成合理的纠正指令。Table 6 提供了多样化纠正文本的示例，表明模型具备生成**可操作、具体化反馈**的能力，而非简单的动作标签。

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/013_Figure_6.jpg]]
*Figure 6: Real-world application. This figure illustrates the source and target motions collected from real-world participants, alongside the corrective instructions generated by different methods. Left to right: the source motion, target motion, generated corrective instruction, and the corrected motions. We collect the videos with a single camera and extract motions with WHAM*

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/014_Table_6.jpg]]
*Table 6: Examples of corrective instructions*

### 失败模式与风险

综合实验分析与论文自述的局限性，CigTime 存在以下失败模式：

1. **编辑器依赖**：方法假设预训练运动编辑器能够准确执行纠正指令。若编辑器本身误差较大，生成的训练三元组质量下降，会直接传播到指令生成模型。
2. **序列不一致性**：当前方法要求源运动与目标运动序列长度相同、上下文一致，无法处理长度不同或场景切换的情况。
3. **专业场景不足**：尚未针对特定运动项目（如举重、瑜伽）提供针对性的形式与动态反馈，难以满足专业教练的精细化需求。
4. **安全风险**：模型存在被滥用来生成侮辱性或不适当运动指令的潜在风险，需进一步引入安全防护机制。

### 关键图表结论速览

- **Table 1**：CigTime 在所有指令质量与重建准确性指标上全面超越基线，验证了“逆向运动编辑”范式的有效性。
- **Table 2**：全参数微调 + 锚定损失是性能提升的关键，扩展词汇表或连续表示均无法替代。
- **Table 3**：方法对底层运动编辑器具有良好鲁棒性，不依赖特定实现。
- **Figure 6 / Table 6**：真实场景验证了方法的实用性，生成的指令具体且可操作。

### 补充图表

![[assets/figures/papers/paper_list_l5_CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing_motion20v/figures/007_Figure_4.jpg]]
*Figure 4: In-context learning for corrective instruction generation. The prompt for the LLMs in in-context learning includes a task description and several examples. This information is given to the LLMs, instructing them to generate correctional instructions for new motion pairs*



## 定位与知识库关联

### 任务定义与基线谱系

**CigTime** 将纠正指令生成形式化为一个映射函数 $\tau(x^I, x^O) = L$，即给定源运动序列 $x^I$ 和目标运动序列 $x^O$，输出自然语言纠正指令 $L$。这一任务位于运动理解与语言生成的交叉地带，与运动描述生成（motion captioning）和运动编辑（motion editing）均有联系，但核心差异在于：CigTime 要求模型从两个运动序列的**差异**中推断出精准的纠正性文本，而非简单描述单个运动或根据文本编辑运动。

论文将现有方法分为两类基线：

**通用大语言模型基线**：包括 **Llama-3-8B** 和 **Mistral-7B**，通过上下文学习（in-context learning）直接生成纠正指令；以及它们的 LoRA 微调版本 **Llama-3-8B-LoRA** 和 **Mistral-7B-LoRA**。这类方法的根本局限在于：通用 LLM 的预训练语料中缺乏运动序列的结构化表征，模型难以从原始运动数据中感知空间与时间维度的细微差异，因此生成的纠正文本往往泛泛而谈，无法精确对应运动偏差。

**运动‑语言模型基线**：包括 **MotionGPT** 及其变体 **MotionGPT-M2T**。MotionGPT 本身面向运动生成与描述，论文通过特定任务模板将其适配到纠正指令生成任务；MotionGPT-M2T 则直接生成目标运动的文本描述作为纠正指令。这类方法的瓶颈在于：它们的设计目标是“运动到文本”的单向映射，而非“运动对到差异文本”的比较推理，因此缺乏对源‑目标运动差异的显式建模能力。

### 核心创新与差异化机制

CigTime 的核心洞察是将纠正指令生成视为**运动编辑的逆过程**：运动编辑器根据源运动和文本指令生成目标运动，而 CigTime 反向利用这一管道，从源‑目标运动对中推断出驱动编辑的文本指令。这一视角转换带来了三个关键差异化机制：

1. **数据收集范式的转变**：基线方法依赖人工标注或少量样本提示，数据规模受限且成本高昂。CigTime 利用预训练运动编辑器（MDM）自动生成大规模（源运动，目标运动，纠正指令）三元组——只需收集源运动与纠正指令，编辑器即可生成对应的目标运动。这从根本上解决了数据瓶颈问题。

2. **运动表征的离散化与语义保留**：基线方法通常使用连续运动特征或直接扩展 LLM 词汇表来嵌入运动标记。CigTime 采用 VQ-VAE 将运动序列量化为离散标记，同时保留原有词汇表的语义完整性。消融实验（Table 2）表明，仅扩展词汇表（Ours-Extended）会导致嵌入发散，MPJPE 上升至 0.16；连续表示（Ours-Continuous）则完全丢失了离散标记的结构化优势，MPJPE 升至 0.33。

3. **锚定损失引导的全参数微调**：基线方法多用上下文学习或 LoRA 微调，对运动标记的学习能力有限。CigTime 采用全参数微调，并引入锚定损失 $\mathcal{L}^{Anch} = \lambda \cdot \| W - W_0 \|_2^2$ 防止预训练权重过度偏离。这一策略在 Table 2 中得到验证：相比于使用 T5 骨干（Ours-T5，MPJPE 0.19），Llama-3-8B 配合锚定损失在重建准确性上具有明显优势（MPJPE 0.13）。

### 适用边界与泛化性

**已知适用条件**：
- 输入为固定长度的源运动与目标运动对，且两者在时间维度上对齐；
- 纠正指令为通用动作调整（如“抬高膝盖”“放慢速度”），不涉及特定运动项目的专业术语；
- 底层运动编辑器性能可靠，能够根据指令生成高质量的目标运动。

**泛化性证据**：
- 在三种不同的运动编辑器（MDM、PriorMDM-LW、PriorMDM-RF）上，CigTime 均取得最低的 MPJPE 和 FID（Table 3），表明方法对编辑器选择具有良好的鲁棒性。
- 在 KIT 数据集上的对比实验（Table 5）进一步验证了跨数据集的迁移能力。
- 在 Fit3D 数据集上的泛化实验（Table 4）显示，指令文本形式会出现较大偏差，泛化性有待提升——这揭示了当前方法的分布外泛化瓶颈。

### 局限与开放问题

**已知局限**：
1. **分布外泛化不足**：在 HumanML3D 上训练的模型迁移到 Fit3D 时，指令文本风格和准确性均有明显下降，说明模型对训练数据分布有较强依赖。
2. **编辑器依赖**：三元组数据的质量受限于预训练运动编辑器的性能；若编辑器本身误差较大，生成的训练数据将包含噪声，影响最终指令质量。
3. **专业化缺失**：当前方法未针对特定运动或体育项目提供针对性的形式与动态反馈，难以满足专业教练场景的精细化需求。
4. **序列约束**：未处理源运动与目标运动序列长度、上下文或场景不一致的情况，限制了在更复杂应用中的使用。
5. **安全风险**：存在被滥用来生成侮辱性或不适当运动指令的潜在风险，需要进一步的安全防护机制。

**开放问题**：
- 如何为特定动作或体育项目提供针对性的形式与动态反馈？
- 如何处理源与目标运动序列长度、上下文或场景不同的情况？
- 如何有效防止模型被滥用以生成不当或侮辱性的运动指令？
- 能否将该方法扩展到实时交互式教练系统，并保持低延迟？

### 在知识库中的位置

CigTime 在运动‑语言研究谱系中占据一个独特位置：它既不同于传统的运动描述生成（单向映射），也不同于运动编辑（文本到运动），而是开创了“运动对到差异文本”这一新任务方向。其方法论贡献——利用运动编辑的逆过程构建训练数据、VQ-VAE 离散化配合锚定损失微调 LLM——为运动理解与语言生成的交叉领域提供了可复用的技术范式。后续工作可沿着专业化适配、实时交互、安全对齐等方向展开。



## 原文 PDF

![[paperPDFs/NEURIPS_2024/CigTime_Corrective_Instruction_Generation_Through_Inverse_Motion_Editing.pdf]]

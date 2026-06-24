---
title: "Kimodo: Scaling Controllable Human Motion Generation"
type: paper
paper_level: A
venue: Whitepaper
year: 2026
pdf_ref: paperPDFs/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.pdf
project_link: https://research.nvidia.com/labs/sil/projects/kimodo/
aliases:
- Kimodo
tags:
- WHITEPAPER_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "使用 700 小时光学动捕数据训练 + 两阶段去噪器架构（根与身体分解预测） + 平滑根关节表示 + 全局运动表示"
primary_logic: "通过全局运动表示（不规范化朝向、平滑根关节）和交织两阶段 Transformer 去噪器，在大规模高质量光学动捕数据上训练扩散模型，能够同时实现精确的文本遵循和多类型运动学约束（关键帧、末端效应器、2D 路径）的高精度控制。"
claims:
- "两阶段去噪器相比单阶段显著降低脚滑动（7.59 → 3.87 cm/s）及约束误差，证明分解架构对运动质量至关重要。"
- "将训练数据从 10% 增加到 100%，脚滑动从 5.28 降至 4.23 cm/s，约束误差单调下降，说明数据规模对可控精度有决定性作用。"
- "平滑根关节表示替代骨盆投影后，脚滑动从 4.39 降至 3.87 cm/s，验证了该表示对减少运动伪影的必要性。"
- "Rigplay Text-Conditioned (Fine-Grained) 上 R@3 ↑ = 73.6 (L Batch, 16 GPUs)"
---

# Kimodo: Scaling Controllable Human Motion Generation

> [!tip] 核心洞察
> 通过全局运动表示（不规范化朝向、平滑根关节）和交织两阶段 Transformer 去噪器，在大规模高质量光学动捕数据上训练扩散模型，能够同时实现精确的文本遵循和多类型运动学约束（关键帧、末端效应器、2D 路径）的高精度控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Kimodo：大规模可控人体运动生成 |
| 英文题名 | Kimodo: Scaling Controllable Human Motion Generation |
| 会议/期刊 | Whitepaper 2026 |
| Links | [paper](https://arxiv.org/abs/2603.15546); [Project](https://research.nvidia.com/labs/sil/projects/kimodo); [Project](https://research.nvidia.com/labs/sil/projects/kimodo/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Kimodo |
| Dataset | Rigplay Text-Conditioned (Fine-Grained), Rigplay Constraint-Conditioned |

> [!tip] 效果简介
> - Rigplay Text-Conditioned (Fine-Grained) 上，R@3 ↑ 为 73.6 (L Batch, 16 GPUs)，对比 69.4 (S Batch, 4 GPUs)，变化 +4.2。
> - Rigplay Constraint-Conditioned 上，FID ↓ 为 1.61 (L Batch)，对比 2.01 (S Batch)，变化 -0.40。
> - Rigplay Constraint-Conditioned 上，Full-Body Pos (cm) ↓ 为 2.33 (L Batch)，对比 2.97 (S Batch)，变化 -0.64。

## 概述

### 问题瓶颈

当前可控人体运动生成面临的核心瓶颈在于**公开动捕数据规模过小**——诸如 AMASS 和 HumanML3D 等主流基准仅包含数百小时的运动数据，这直接限制了生成运动的质量、控制精度与泛化能力。与此同时，过度饱和的基准评测掩盖了关键设计选择对性能的真实影响，使得领域难以有效区分架构创新与数据红利。

### 核心方案

针对上述瓶颈，Kimodo 提出了一套系统性的解决方案，其核心逻辑链条由三个关键环节构成：

1. **数据规模化**：在 700 小时高质量光学动捕数据（Bones Rigplay 数据集）上训练，从根本上缓解数据稀缺问题。
2. **全局运动表示**：摒弃传统的朝向规范化与骨盆投影做法，转而采用平滑根关节表示与全局关节位置/旋转，为去噪器提供稳定的参考框架。
3. **两阶段去噪器架构**：将运动预测分解为根去噪（全局根轨迹）与身体去噪（以局部根表示为条件的身体关节预测），通过交织式 Transformer 实现分工协作。

这三者形成因果闭环：**大规模数据提供了学习精确约束遵循的基础，全局表示消除了规范化引入的伪影，而分解式去噪器则使模型能够分别优化根轨迹的全局一致性与身体运动的局部细节**。消融实验强有力地验证了这一设计逻辑——两阶段架构相较单阶段基线将脚滑动从 7.59 cm/s 降至 3.87 cm/s；平滑根表示进一步将脚滑动从 4.39 cm/s 压缩至 3.87 cm/s；而数据量从 10% 扩展到 100% 时，脚滑动从 5.28 cm/s 单调下降至 4.23 cm/s，约束误差同步降低。

### 方法谱系与知识库定位

在人体运动生成的方法谱系中，Kimodo 属于**显式运动扩散模型**分支。与基于局部速度表示的经典工作（如 Guo et al., CVPR 2022）不同，Kimodo 的关键差异在于：

- **表示层**：采用全局位置/旋转表示，不进行朝向规范化，并以平滑根关节替代传统的骨盆投影。
- **架构层**：引入两阶段交织式 Transformer 去噪器，将根与身体的预测解耦，并在身体阶段使用局部根表示（角速度、平移速度、高度）而非全局根。
- **训练层**：采用两阶段课程学习——先纯文本预训练 50 万步，再混合约束训练 50 万步——使模型在保持文本遵循能力的同时逐步习得约束精度。

在约束注入机制上，Kimodo 采用基于二值控制掩码的直接覆盖策略（imputation），将目标姿态特征替换到噪声运动上，实现对关键帧、末端效应器和 2D 路径等多种运动学约束的统一处理。

### 主要结果概要

在 Rigplay 测试集上，Kimodo 在文本遵循与约束精度两个维度均展现出显著优势。缩放实验表明，增大批量大小（16 GPU vs. 4 GPU）将文本遵循 R@3 从 69.4 提升至 73.6，约束条件 FID 从 2.01 降至 1.61，全身体位置误差从 2.97 cm 降至 2.33 cm。消融实验进一步确认，两阶段训练课程是约束精度的关键使能因素——移除课程后全身体位置误差从 2.67 cm 急剧上升至 5.80 cm。

值得注意的是，所有消融与缩放实验均**未使用后处理步骤**（如脚步锁定、逆向运动学），且采用中等批量（8 GPU）和 20 fps 训练以保证公平对比。模型在 NVIDIA RTX 3090 上的单次生成耗时约 2–5 秒，定位为离线动作创作工具，不适用于实时交互场景。

## 背景与动机

### 问题背景：数据规模与基准饱和的双重瓶颈

人体运动生成旨在根据文本描述或运动学约束合成自然、多样的人体动作序列，在动画制作、机器人学习和虚拟现实等领域具有广泛应用。近年来，扩散模型在运动生成任务上取得了显著进展，但两个深层瓶颈制约着该领域的实质性突破。

**第一，公开动捕数据的规模严重不足。** 主流的运动生成基准如 HumanML3D 和 AMASS 仅包含数百小时的动捕数据。这种数据稀缺性直接限制了生成模型在三个关键维度上的表现：运动质量（如脚滑动等伪影的抑制）、控制精度（如关键帧约束的满足程度）和泛化能力（对未见行为的覆盖）。当模型只能在有限的行为多样性上训练时，其合成结果往往缺乏真实感，且难以精确响应用户的复合控制信号。

**第二，过度饱和的基准掩盖了关键设计选择的影响。** 现有工作在 HumanML3D 等小规模基准上的指标已趋于饱和，不同方法之间的性能差异被压缩到难以区分的程度。这使得研究者无法可靠地判断哪些架构设计、表示选择和训练策略真正推动了性能提升，哪些仅仅是针对特定基准的过拟合。该领域亟需一个更大规模、更具区分度的评估平台来揭示方法的真实能力边界。

### 现有方法缺口：控制精度与运动质量的权衡

当前可控运动生成方法面临一个核心权衡：在追求精确的运动学约束满足时，往往以牺牲运动自然度为代价。具体而言，现有工作在以下方面存在明显不足：

- **运动表示方面**：多数方法采用局部速度基表示或对全局朝向进行规范化处理。这种设计虽然简化了学习目标，但丢失了全局运动信息，导致在需要精确空间控制（如末端效应器定位、2D 路径跟随）时表现不佳。此外，直接使用骨盆投影作为根关节会引入髋部摆动等高频噪声，使关节位置的参考坐标系不稳定，加剧脚滑动等伪影。

- **去噪器架构方面**：单阶段 Transformer 直接预测全局运动，将根轨迹预测与身体姿态生成耦合在同一网络中。这种耦合使得根运动的误差会传播到全身关节，放大了约束不满足和运动不自然的程度。尽管部分工作尝试了两阶段设计，但各阶段独立训练，无法实现端到端的联合优化。

- **训练策略方面**：现有方法通常直接从混合文本和约束条件开始训练，缺乏对文本理解和约束遵循能力的渐进式培养。这种训练方式可能导致模型在文本语义和运动学精度之间难以达到最优平衡。

### 本文动机：规模化数据与精细化设计的协同

基于上述分析，本文的核心动机在于：**通过大规模高质量光学动捕数据与精心设计的运动表示及去噪器架构的协同，突破可控运动生成的性能瓶颈。** 具体而言，本文提出 Kimodo，在以下三个层面进行系统性改进：

1. **数据规模化**：利用包含 700 小时光学动捕数据的 Bones Rigplay 数据集进行训练，显著提升行为多样性和运动质量的上限。该数据集为每个动捕序列提供了多层次的文本标注（高层概述、细粒度原子动作描述、LLM 改写），为文本条件生成提供了丰富的语义监督。

2. **表示精细化**：采用全局运动表示（不进行朝向规范化），并引入平滑根关节表示替代传统的骨盆投影。平滑根轨迹去除了髋部摆动等高频分量，为关节位置提供了稳定的参考坐标系，从根源上减少运动伪影。

3. **架构分解化**：设计交织两阶段 Transformer 去噪器，将根运动预测与身体姿态生成解耦。第一阶段预测全局根轨迹，第二阶段以局部化的根表示（角速度、平移速度、高度）为条件预测身体关节运动。两阶段端到端联合训练，配合先纯文本预训练再混合约束训练的两阶段课程，实现文本遵循与约束精度的双重提升。

## 核心创新

Kimodo 的核心创新并非单一算法突破，而是围绕**大规模高质量数据**驱动下的一系列表示与架构协同设计，共同解决了可控人体运动生成中长期存在的控制精度不足与运动伪影问题。其关键创新可归纳为以下四个相互耦合的 changed slots：

### 1. 全局运动表示与平滑根关节

传统方法（如 Guo et al., CVPR 2022）普遍采用局部速度基表示，并将关节位置相对于每帧的根朝向进行规范化。Kimodo 做出了两个根本性改变：

- **不进行朝向规范化**：直接使用全局关节位置 $\mathbf{j}^p$，避免了因根朝向跳变（如 ±π 处）导致的表示不连续性问题，使模型能够学习更连贯的全局运动轨迹（Sec. 4.1, Fig. 8）。
- **平滑根关节替代骨盆投影**：将骨盆位置的水平分量 $(x, z)$ 进行重度平滑后作为根位置 $\mathbf{r}^p$，而非直接使用骨盆投影。消融实验表明，这一改变将脚滑动从 4.39 cm/s 降至 3.87 cm/s（Table 1: No Smoothed Root），其机理在于平滑根轨迹消除了髋部摆动引入的高频噪声，为身体关节位置提供了一个稳定的参考系，从而抑制了脚部抖动伪影。

### 2. 交织两阶段 Transformer 去噪器

这是 Kimodo 架构层面最关键的创新。不同于单阶段 Transformer 直接预测全局运动，Kimodo 将去噪过程分解为**根预测**与**身体预测**两个交织的 Transformer Encoder（Fig. 9）：

- **第一阶段（根去噪器）**：接收注入约束后的噪声运动，专门预测全局根运动 $\mathbf{r}^{\text{glob}} = [\mathbf{r}^p, \mathbf{r}^a]$。
- **第二阶段（身体去噪器）**：以第一阶段预测的根运动为条件，但先将全局根转换为局部表示 $\mathbf{r}^{\text{local}} = [\dot{\mathbf{r}}^a, \dot{\mathbf{r}}_{xz}^p, \mathbf{r}_y^p]$（角速度、水平平移速度、绝对高度），再预测身体关节运动。

这一分解架构带来了两个因果收益：
- **大幅降低脚滑动**：单阶段基线脚滑动为 7.59 cm/s，两阶段架构直接降至 3.87 cm/s（Table 1: One-Stage baseline），降幅达 49%。根与身体的解耦预测使模型能分别专注于全局轨迹规划与局部姿态细化，避免了单阶段模型中两类信号的相互干扰。
- **局部根表示进一步优化**：在身体阶段使用局部根表示而非全局根，将脚滑动从 4.17 cm/s 进一步降至 3.87 cm/s（Table 1: Second Stage Global），说明局部速度/高度信息比绝对全局坐标更适合作为身体关节预测的条件信号。

### 3. 约束注入机制

Kimodo 通过简单的**掩码覆盖**实现运动学约束的注入：

$$\tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{x}_{\text{tgt}} + (1 - \mathbf{m}) \odot \mathbf{x}_t$$

其中 $\mathbf{m}$ 为二值控制掩码，$\mathbf{x}_{\text{tgt}}$ 为目标姿态特征。这一机制在训练和推理中保持一致，使去噪器能够原生处理稀疏关键帧、末端效应器位置/旋转、2D 根路径等多种约束类型，无需额外的编码器或适配模块。约束类型覆盖全身边关键帧、末端效应器、2D 路径点及稠密路径（Sec. 2.2），在约束多样性上显著超越先前工作。

### 4. 两阶段训练课程

Kimodo 采用 50 万步纯文本预训练 + 50 万步混合约束训练的课程策略（Sec. 4.3）。消融实验表明，去除该课程后全身体位置误差从 2.67 cm 急剧上升至 5.80 cm（Table 1: No Train Curriculum），证明直接从头联合训练文本与约束条件会导致优化困难——模型难以在早期同时学习语义理解和精确约束遵循，而分阶段训练使模型先建立稳定的文本-运动映射，再逐步适应约束条件。

### 创新协同效应

上述四个 changed slots 并非孤立改进，而是形成正向协同：**平滑根表示**为两阶段去噪器提供了稳定的全局参考；**两阶段架构**通过分解预测放大了平滑根带来的伪影抑制效果；**约束注入**的简洁性使两阶段去噪器无需额外复杂度即可处理多类约束；**训练课程**则为这一复杂系统的稳定收敛提供了保障。最终，在 700 小时光学动捕数据的规模加持下，这些设计共同实现了文本遵循与运动学控制精度的双重提升。

## 整体框架

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_15546/figures/009_Figure_9.jpg]]
*Figure 9: Denoiser Architecture. (Left) Kimodo predicts clean motion given a noisy motion, pose constraints, and a text embedding. Specified pose constraints directly overwrite the noisy motion before it is given to the denoiser. (Right) The two-stage denoiser decomposes root and body motion prediction. The root denoiser first predicts the global root motion, which is transformed into a local representation as input to the body denoiser. The final output of the denoising step is the concatenation of the outputs from the two stages*

Kimodo 是一个显式的运动学运动扩散模型，核心思路是将人体运动生成建模为一个条件去噪过程。给定一段纯噪声运动序列，模型在文本提示和多种运动学约束的共同引导下，通过迭代去噪逐步恢复出干净、可控的运动姿态。整个框架由四个关键环节串联而成：**运动表示**、**约束注入**、**两阶段去噪器**和**训练/推理策略**。

### 输入输出流与模块关系

系统的输入包括三类信号：文本描述、运动学约束（关键帧、末端效应器、2D 路径等）以及一段初始化的高斯噪声运动序列。输出是一段完整的干净运动序列，包含全局根轨迹和身体关节姿态。

**文本编码器 (LLM2Vec)** 首先将输入文本提示编码为 4096 维嵌入向量，作为全局条件信号贯穿整个去噪过程。

**约束注入 (Imputation)** 模块在每一轮去噪之前，根据二值控制掩码将目标姿态特征直接覆盖到当前噪声运动上：

$$\tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{x}_{\mathrm{tgt}} + (1 - \mathbf{m}) \odot \mathbf{x}_t$$

这一硬注入机制确保受约束的帧或关节在去噪过程中始终携带精确的目标信息，成为后续去噪器必须“顺应”的锚点。

**两阶段去噪器** 是 Kimodo 的核心架构（见图 9）。它由两个交织的 Transformer 编码器组成：

1. **根去噪器 (Root Transformer Encoder)**：接收注入约束后的噪声运动、文本嵌入和时间步，首先预测全局根运动——包括平滑后的根位置 $\mathbf{r}^p$ 和根朝向 $\mathbf{r}^a$。
2. **身体去噪器 (Body Transformer Encoder)**：将根去噪器输出的全局根运动转换为局部表示（角速度 $\dot{\mathbf{r}}^a$、水平平移速度 $\dot{\mathbf{r}}_{xz}^p$、绝对高度 $\mathbf{r}_y^p$），并以此为条件预测身体关节的运动特征——包括关节位置 $\mathbf{j}^p$、速度 $\mathbf{j}^v$、角度 $\mathbf{j}^a$ 和足部接触标签 $\mathbf{f}$。

两阶段的输出最终拼接为完整的干净运动预测 $\hat{\mathbf{x}}_0$。这种根与身体分解的设计是降低脚滑动伪影的关键：消融实验表明，单阶段去噪器的脚滑动高达 7.59 cm/s，而两阶段架构将其降至 3.87 cm/s（Table 1）。

### 运动表示的关键抉择

Kimodo 的运动表示在三个维度上做出了与先前工作不同的选择：

- **全局位置而非局部速度**：关节位置 $\mathbf{j}^p$ 直接使用全局坐标，不进行朝向规范化。这避免了因根朝向不连续而导致的位置跳变，但也要求模型具备更强的空间推理能力。
- **平滑根关节**：根位置 $\mathbf{r}^p$ 通过对骨盆投影路径进行重度水平平滑得到，而非直接使用原始骨盆轨迹。这一设计模拟了动画师在创作中绘制的平滑路径，为身体关节提供了一个稳定的参考系（见图 8）。消融实验证实，平滑根表示将脚滑动从 4.39 cm/s 进一步降至 3.87 cm/s（Table 1）。
- **身体阶段的局部根表示**：在身体去噪器中，全局根被转换为局部运动学量（角速度、平移速度、高度），而非直接输入全局坐标。这种局部化处理使身体去噪器能够专注于相对运动模式，将脚滑动从 4.17 cm/s 优化至 3.87 cm/s（Table 1: Second Stage Global）。

### 训练与推理策略

**训练课程** 采用两阶段策略：前 50 万步仅进行纯文本到运动的预训练，使模型先学会基本的运动生成能力；后 50 万步引入混合约束条件进行联合训练。消融实验表明，这一课程设计对约束精度至关重要——缺少课程训练时，全身体位置误差从 2.67 cm 急剧上升至 5.80 cm（Table 1: No Train Curriculum）。

训练损失基于 DDPM 框架的简化损失函数，对根位置、根朝向、关节位置、速度、角度、足部接触标签以及前向运动学一致性分别施加 Smooth L1 惩罚：

$$\mathcal{L} = \gamma_1 ||\hat{\mathbf{j}}_0^p - \mathbf{r}_0^p||_1 + \gamma_2 ||\hat{\mathbf{r}}_0^a - \mathbf{r}_0^a||_1 + \gamma_3 ||\hat{\mathbf{j}}_0^p - \mathbf{j}_0^p||_1 + \gamma_4 ||\hat{\mathbf{j}}_0^v - \mathbf{j}_0^v||_1 + \gamma_5 ||\hat{\mathbf{j}}_0^a - \mathbf{j}_0^a||_1 + \gamma_6 ||\hat{\mathbf{f}}_0 - \mathbf{f}_0||_1 + \gamma_7 ||\mathrm{FK}(\hat{\mathbf{j}}_0^a) - \mathbf{j}_0^p||_1$$

**推理阶段** 采用分类器自由引导，将无条件、纯文本和纯约束三个模型的预测进行组合：

$$\hat{\mathbf{x}}_0 = \mathcal{D}_{\mathcal{Q}} + w_{\mathrm{text}}(\mathcal{D}_{\mathrm{text}} - \mathcal{D}_{\mathcal{Q}}) + w_{\mathrm{constr}}(\mathcal{D}_{\mathrm{constr}} - \mathcal{D}_{\mathcal{Q}})$$

通过调整 $w_{\mathrm{text}}$ 和 $w_{\mathrm{constr}}$ 两个引导权重，用户可以独立控制文本遵循程度和约束满足强度。

**后处理模块**（脚步锁定、逆向运动学）在演示应用中用于进一步提高约束精度，但所有标准化实验评估均未启用这些后处理，以保证方法间比较的公平性（Sec. 6.1）。

## 核心模块与公式推导

Kimodo 的核心是一个显式运动扩散模型，其推理流程可分解为三个关键模块：**约束注入**、**两阶段 Transformer 去噪器**和**分类器自由引导**。以下逐一展开其机理与公式。

### 约束注入：将控制信号融入噪声运动

在每一去噪步开始前，Kimodo 通过一个简单的掩码操作将用户指定的运动学约束直接覆盖到当前噪声运动上：

$$
\tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{x}_{\mathrm{tgt}} + (1 - \mathbf{m}) \odot \mathbf{x}_t
$$

其中 $\mathbf{x}_t$ 为当前步的噪声运动，$\mathbf{x}_{\mathrm{tgt}}$ 为目标姿态特征向量，$\mathbf{m}$ 为二值控制掩码。该操作确保受约束帧的指定关节特征（如位置、旋转）被精确注入，而未约束部分保留噪声状态，为后续去噪提供条件。这种“硬注入”策略使得去噪器在训练时即学会在约束条件下补全其余运动，是实现关键帧、末端效应器和路径控制的基础机制。

### 两阶段去噪器：根与身体的分解预测

约束注入后的噪声运动 $\tilde{\mathbf{x}}_t$ 与文本嵌入 $C$、去噪步 $t$ 一同送入去噪器 $\mathcal{D}_\theta$，预测干净运动 $\hat{\mathbf{x}}_0$：

$$
\hat{\mathbf{x}}_0 = \mathcal{D}_\theta(\tilde{\mathbf{x}}_t, C, t)
$$

$\mathcal{D}_\theta$ 采用**两阶段交织 Transformer 编码器**架构（Fig. 9），将运动预测分解为**根去噪器**和**身体去噪器**：

1. **根去噪器**：首先预测全局根运动 $\mathbf{r}^{\mathrm{glob}} = [\mathbf{r}^p, \mathbf{r}^a]$，即平滑后的根位置 $\mathbf{r}^p \in \mathbb{R}^3$ 和根朝向 $\mathbf{r}^a$。
2. **局部根表示转换**：将预测的全局根转换为局部表示 $\mathbf{r}^{\mathrm{local}} = [\dot{\mathbf{r}}^a, \dot{\mathbf{r}}_{xz}^p, \mathbf{r}_y^p]$，分别对应角速度、水平平移速度和绝对高度。这一转换是消融实验中脚滑动从 4.17 降至 3.87 cm/s 的关键（Table 1: Second Stage Global）。
3. **身体去噪器**：以局部根表示为条件，预测身体关节的运动特征 $[\mathbf{j}^p, \mathbf{j}^v, \mathbf{j}^a, \mathbf{f}]$，即关节位置、速度、角度和足部接触标签。

最终输出为根与身体预测的拼接。两阶段分解使得根轨迹的全局一致性与身体姿态的局部细节可以分别建模，相较单阶段基线，脚滑动从 7.59 大幅降至 3.87 cm/s（Table 1: One-Stage baseline），验证了分解架构对运动质量的因果作用。

### 训练损失：多目标 Smooth L1 约束

去噪器按 DDPM 框架训练，损失函数为对预测干净运动 $\hat{\mathbf{x}}_0$ 与真实运动 $\mathbf{x}_0$ 各分量的 Smooth L1 惩罚：

$$
\begin{aligned}
\mathcal{L} = &\ \gamma_1 \|\hat{\mathbf{r}}_0^p - \mathbf{r}_0^p\|_1 + \gamma_2 \|\hat{\mathbf{r}}_0^a - \mathbf{r}_0^a\|_1 + \gamma_3 \|\hat{\mathbf{j}}_0^p - \mathbf{j}_0^p\|_1 \\
+ &\ \gamma_4 \|\hat{\mathbf{j}}_0^v - \mathbf{j}_0^v\|_1 + \gamma_5 \|\hat{\mathbf{j}}_0^a - \mathbf{j}_0^a\|_1 + \gamma_6 \|\hat{\mathbf{f}}_0 - \mathbf{f}_0\|_1 \\
+ &\ \gamma_7 \|\mathrm{FK}(\hat{\mathbf{j}}_0^a) - \mathbf{j}_0^p\|_1
\end{aligned}
$$

损失项依次对应：根位置误差、根朝向误差、关节位置误差、关节速度误差、关节角度误差、足部接触标签误差，以及**前向运动学一致性误差**——通过 FK 函数将预测的关节角度映射回位置空间并与真实关节位置比较，强制运动学自洽。各 $\gamma$ 为超参数权重。

### 推理：双引导分类器自由策略

推理时，Kimodo 采用**双引导分类器自由**策略，将无条件模型 $\mathcal{D}_{\mathcal{Q}}$、纯文本条件模型 $\mathcal{D}_{\mathrm{text}}$ 和纯约束条件模型 $\mathcal{D}_{\mathrm{constr}}$ 的预测进行线性组合：

$$
\hat{\mathbf{x}}_0 = \mathcal{D}_{\mathcal{Q}} + w_{\mathrm{text}}(\mathcal{D}_{\mathrm{text}} - \mathcal{D}_{\mathcal{Q}}) + w_{\mathrm{constr}}(\mathcal{D}_{\mathrm{constr}} - \mathcal{D}_{\mathcal{Q}})
$$

其中 $w_{\mathrm{text}}$ 控制文本遵循强度，$w_{\mathrm{constr}}$ 控制约束满足精度。这种分解允许用户在生成时独立调节两个维度的控制力，是交互式动作创作界面中灵活性的来源。

## 实验与分析

### 核心瓶颈与实验设计逻辑

Kimodo 的实验设计围绕一个核心诊断展开：公开动捕数据量小（AMASS/HumanML3D 仅数百小时）不仅限制了生成运动的质量，更关键的是使基准过度饱和，掩盖了关键设计选择的影响。为此，所有实验均在 Bones Rigplay 数据集（700 小时光学动捕）上进行，以暴露不同设计决策的真实效果。

实验设置遵循严格的公平性原则：
- 所有消融实验均使用中等批量大小（8 GPU）、20 fps 训练，且**未应用任何后处理**（如脚步锁定、逆向运动学），以保证公平对比（Sec. 6.1）。
- 缩放实验的数据子集保留所有独特行为类型，仅减少每种行为的表演次数，以评估数据多样性而非行为覆盖的影响（Sec. 6.3）。
- 文本评估指标 R-Precision 和 FID 均使用在完整 Rigplay 数据集（含训练与测试分割）上训练的 TMR 模型计算（Sec. 6.1）。
- 约束误差计算取输入约束与生成运动在受约束帧上的平均距离误差（Sec. 6.1）。

---

### 消融实验：架构设计的因果验证

Table 1 系统消融了 Kimodo 的五个关键设计选择，每个消融项都揭示了明确的因果机制。


![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_15546/figures/010_Table_1.jpg]]
*Table 1: Ablation Study. Evaluation of text and constraint-conditioned motion generation on the Rigplay test set. The full model is compared to various baselines to justify key design decisions, including the two-stage denoiser, smoothed root representation, and dual-phase training curriculum. All models are trained using a medium batch size (8 GPU) at 20 fps. FID is multiplied ×100 for readability*

**两阶段去噪器 vs. 单阶段（One-Stage baseline）**

这是最关键的架构消融。将交织两阶段 Transformer 替换为单阶段 Transformer 直接预测全局运动后，脚滑动从 **3.87 cm/s 飙升至 7.59 cm/s**，约束误差也全面恶化。这一差距揭示了分解架构的核心作用：根运动与身体运动的分离预测使模型能够先建立稳定的全局参考系，再在此基础上生成局部关节运动，从而有效抑制脚滑动伪影。单阶段模型被迫同时学习全局轨迹和局部姿态，导致两者耦合产生不自然的足部漂移。

**局部根表示 vs. 全局根（Second Stage Global）**

在身体阶段将局部根表示（角速度、平移速度、高度）替换为全局根后，脚滑动从 3.87 升至 **4.17 cm/s**。这表明局部根表示为身体去噪器提供了更稳定的条件信号——平移速度和角速度直接编码了帧间运动增量，高度则保留了绝对垂直信息，三者共同构成对局部运动生成更友好的输入空间。

**平滑根关节 vs. 骨盆投影（No Smoothed Root）**

使用直接骨盆投影替代平滑根关节后，脚滑动从 3.87 升至 **4.39 cm/s**，约束误差同步上升。平滑根关节通过对水平分量重度平滑，消除了骨盆摆动带来的高频噪声，为关节位置表示提供了稳定的参考系（Fig. 8）。这一设计直接减少了运动伪影，验证了根表示质量对整体运动质量的传导效应。

**额外寄存器标记（No Extra Tokens）**

移除额外寄存器标记后，文本遵循度 R@3 从 63.5 降至 **61.6**，FID 也出现退化。这说明额外的可学习标记为文本条件提供了更丰富的嵌入交互空间，有助于提升文本-运动对齐精度。

**两阶段训练课程（No Train Curriculum）**

跳过纯文本预训练阶段、直接从头训练混合约束任务，导致全身体位置误差从 2.67 飙升至 **5.80 cm**。这一显著差距揭示了课程学习的必要性：纯文本预训练使模型先建立稳定的运动先验，再引入约束条件时模型已具备合理的运动生成能力，从而更有效地学习约束遵循，而非在训练初期被约束信号干扰运动质量的学习。

---

### 缩放分析：数据、模型与批量的规模效应

Table 2 从三个维度系统分析了规模对性能的影响。


![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_15546/figures/011_Table_2.jpg]]
*Table 2: Scaling Analysis. Evaluation of text and constraint-conditioned motion generation on the Rigplay test set. (Top) Increasing the amount of training data improves motion quality and constraint accuracy due to increased diversity. (Middle) Increased model size improves performance on all metrics. (Bottom) Increasing batch size by using more GPUs generally improves performance across the board*

**数据规模**

将训练数据从 10% 逐步增加到 100%，脚滑动从 5.28 单调下降至 **4.23 cm/s**，约束误差（全身体位置误差从 3.79 降至 2.67 cm）持续改善。这一趋势验证了数据多样性对可控精度的决定性作用——更大规模的数据覆盖了更多样的运动模式和约束组合，使模型学会更精确地满足控制条件。

值得注意的是，R-Precision 和 FID 在数据子集实验中未出现显著下降。这可能是因为子集保留了所有行为类型，仅减少每种行为的表演次数，导致文本-运动对齐和整体运动分布未受明显影响。这一现象本身是一个值得关注的开放问题：是否行为类型的覆盖比数据量本身对文本遵循度更为关键？

**模型规模**

增大模型参数量在全部指标上均带来提升，表明 Kimodo 的架构具备良好的可扩展性。但论文指出，继续扩大至 282M 以上可能面临训练不稳定和收益递减，目前尚未探索 5 亿参数量级的稳定训练。

**批量大小**

使用 16 GPU 的大批量训练相比 4 GPU 的小批量，在文本遵循度（R@3 73.6 vs. 69.4）、运动质量（FID 1.61 vs. 2.01）和约束精度（全身体位置误差 2.33 vs. 2.97 cm）上全面领先。大批量训练通常提供更稳定的梯度估计，有利于扩散模型的收敛质量。

---

### 失败模式与局限性

尽管 Kimodo 在可控精度和运动质量上取得了显著进展，其设计存在明确的边界：

1. **实时性不足**：生成一段运动需 2–5 秒（NVIDIA RTX 3090），模型专为离线动作创作设计，不适用于实时控制或反应式交互场景。

2. **数据依赖性**：训练数据限于 700 小时光学动捕，模型仅能合成数据集中存在的动作类型，缺乏对场景和物体交互的泛化能力。如何将视频恢复的噪声数据与高质量动捕数据有效结合，是一个关键的开放问题。

3. **单人限制**：仅支持单人动作生成，不能生成人与物体或人与场景的交互，限制了在复杂环境中的应用。

4. **后处理不一致**：脚步锁定和 IK 等后处理步骤在演示中用于进一步提高约束精度，但未纳入标准化评估，实际部署可能存在精度差异。

5. **扩展瓶颈**：继续扩大模型参数量可能面临训练不稳定和收益递减，如何保持训练稳定性并实现更大的性能增益仍有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_15546/figures/001_Figure_1.jpg]]
*Figure 1: Controllable Motion Generation. Kimodo supports flexible and intuitive control for motion generation through text prompting combined with an extensive suite of kinematic constraints. By training on 700 hours of optical mocap data, the model achieves precise control accuracy for a large variety of behaviors. In each example, constrained joints are indicated with a red color, and generated poses at constrained frames are highlighted in yellow. Time progression is indicated by lighter to darker blue coloring*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_15546/figures/003_Figure_3.jpg]]
*Figure 3: Text-to-Motion Results. (Top) Kimodo enables generating high-quality human motions for a variety of behaviors on the SOMA body skeleton. Time progression is indicated by lighter to darker blue coloring. (Middle) Motions can also be generated directly on the G1 robot to easily collect plausible demonstrations. (Bottom) The same frame is visualized from ten different generated motion samples for the same prompt, demonstrating the diversity of Kimodo outputs*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_15546/figures/005_Figure_5.jpg]]
*Figure 5: Scaling Results. Scaling dataset size, model size, and batch size improves controllability and motion quality. Increased dataset size results in greatly improved constraint following, while model size and batch size are particularly helpful for text following (R-precision) and motion quality (FID). See Tab. 2 for full results*


## 方法谱系与知识库定位

### 1. 核心设计决策的因果链条

Kimodo 的方法论创新并非孤立的技术点，而是围绕“大规模高质量数据 + 全局运动表示 + 分解式去噪架构”形成的一条因果链条。理解这条链条是定位其方法谱系的关键。

**瓶颈识别**：现有文本到运动生成方法普遍在 HumanML3D 等小规模数据集（数百小时）上训练，基准性能已趋于饱和，掩盖了关键设计选择对运动质量和控制精度的真实影响。Kimodo 的作者明确指出，公开动捕数据量小是限制生成运动质量、控制精度和泛化能力的核心瓶颈。

**因果调节变量**：Kimodo 引入三个相互耦合的调节变量来突破上述瓶颈：

1. **数据规模**：使用 Bones Rigplay 数据集中 700 小时光学动捕数据进行训练，远超 HumanML3D 的规模。
2. **全局运动表示**：不进行朝向规范化，采用平滑根关节位置替代传统的骨盆投影，避免因朝向规范化引入的关节位置不连续性。
3. **两阶段交织去噪器**：将运动预测分解为根轨迹预测与身体姿态预测两个阶段，并在第二阶段将全局根转换为局部表示（角速度、平移速度、高度）作为身体预测的条件。

**核心洞见**：这三者的协同作用在于——全局运动表示消除了朝向规范化带来的伪影，为大规模数据训练提供了稳定的表示基础；两阶段去噪器则利用这种稳定表示，将根运动与身体运动解耦，使模型能分别专注于轨迹规划与姿态生成；而 700 小时的高质量光学动捕数据则为这两个组件提供了足够的多样性和精度支撑。

**决定性证据**：

- **两阶段 vs. 单阶段**：消融实验（Table 1）显示，将两阶段去噪器替换为单阶段 Transformer 直接预测全局运动后，脚滑动从 3.87 cm/s 急剧上升至 7.59 cm/s，约束误差也全面恶化。这证明分解架构对运动质量有因果性贡献。
- **数据规模缩放**：将训练数据从 10% 逐步增加到 100%，脚滑动从 5.28 单调下降至 4.23 cm/s，约束误差同步改善（Table 2）。这表明数据规模对可控精度有决定性作用，而非仅靠架构设计。
- **平滑根表示**：消融“No Smoothed Root”（即恢复为骨盆投影）后，脚滑动从 3.87 升至 4.39 cm/s，约束误差也显著增加（Table 1）。这验证了平滑根关节表示对减少运动伪影的必要性。

### 2. 方法谱系中的定位

Kimodo 处于**运动扩散模型**（Motion Diffusion Model）的方法谱系中，其直接技术祖先可追溯至 MDM（Tevet et al., ICLR 2023）等基于 Transformer 的显式运动扩散框架。但与同谱系方法相比，Kimodo 在以下维度做出了差异化贡献：

**运动表示维度**：传统方法普遍采用局部速度基表示（如 Guo et al., CVPR 2022）或在每帧进行朝向规范化。Kimodo 反其道而行之，采用全局关节位置/旋转表示且不进行朝向规范化，这在方法谱系中属于少数派选择。其关键创新在于通过平滑根关节来克服全局表示带来的轨迹不稳定问题——这一设计使得全局表示的连续性与局部表示的稳定性得以兼得。

**去噪器架构维度**：已有的两阶段运动生成方法（如 PriorMDM 等）通常将根预测与身体预测分阶段独立训练。Kimodo 的“交织式”两阶段 Transformer 与之不同：两个阶段共享同一个训练目标并在端到端框架下联合优化。此外，在第二阶段将全局根转换为局部表示（角速度、平移速度、高度）作为条件输入，这一设计在现有工作中较为独特，消融实验证明其将脚滑动从 4.17 进一步降至 3.87 cm/s（Table 1, Second Stage Global）。

**训练策略维度**：Kimodo 采用两阶段训练课程——先进行 50 万步纯文本预训练，再进行 50 万步混合约束训练。消融实验（Table 1, No Train Curriculum）表明，去除该课程后全身体位置误差从 2.67 cm 飙升至 5.80 cm，说明该策略对约束遵循能力至关重要。这与直接从头训练文本+约束条件的常规做法形成对比。

**约束注入机制**：Kimodo 通过简单的插值式注入（$\tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{x}_{\mathrm{tgt}} + (1 - \mathbf{m}) \odot \mathbf{x}_t$）实现运动学约束的施加，而非设计专门的约束编码器或条件模块。这种轻量设计使得模型能同时处理全身边框、末端效应器约束、2D 根路径等多种约束类型，在方法谱系中属于“统一约束接口”路线。

### 3. 适用边界与局限

**计算效率边界**：Kimodo 专为离线动作创作设计，在 NVIDIA RTX 3090 上生成一段运动需 2–5 秒，不适用于实时控制或反应式交互场景。这一延迟主要来自扩散模型的迭代去噪过程，是其方法范式的固有局限。

**数据覆盖边界**：模型仅能合成训练数据中存在的动作类型。700 小时光学动捕虽已远超现有公开数据集，但仍无法覆盖开放世界中的所有人类行为。特别是，模型缺乏对场景和物体交互的泛化能力——它学习的是人体运动学模式，而非物理交互动态。

**交互类型边界**：Kimodo 仅支持单人动作生成，不能生成人与物体或人与场景的交互。这一局限源于其训练数据的性质（纯动捕数据，无场景上下文）以及运动表示的设计（仅包含人体关节信息，不含物体或环境表示）。

**模型规模边界**：当前最大模型参数量为 282M。作者指出继续扩大参数量可能面临训练不稳定和收益递减的问题，尚未探索 5 亿参数量级的稳定训练。这暗示当前架构可能存在规模扩展的隐性上限。

**评估一致性边界**：后处理步骤（脚步锁定、逆向运动学、短时优化）在演示中用于进一步提高约束精度，但未纳入标准化评估以保证公平对比。这意味着实际部署中的性能可能优于论文报告的实验数据，但也引入了部署与评估之间的不一致性。

### 4. 待解决的开放问题

1. **异构数据融合**：如何将视频恢复的噪声运动数据与高质量光学动捕数据有效结合，在不损害运动质量的前提下扩展数据多样性？这是突破数据覆盖边界的关键。

2. **实时化路径**：能否将扩散过程迁移到学习的潜变量空间，并将运动生成重构为自回归问题，以实现实时运动合成？这将直接决定方法在交互式应用中的可行性。

3. **交互数据采集**：如何高效采集包含丰富场景和物体交互的大规模运动数据？这是将可控运动生成从“人体运动学”推向“具身交互”的前提。

4. **多样性评估的敏感性**：在数据子集缩放实验中，R-precision 和 FID 未出现显著下降，是否因为子集保留了所有行为类型而掩盖了真实多样性的损失？这提示现有评估指标可能对数据多样性的变化不够敏感。

5. **大规模训练的稳定性**：进一步扩大模型参数量时，如何保持训练稳定性并实现更大的性能增益？这涉及优化器设计、学习率调度、架构调整等多个维度的探索。

## 原文 PDF

![[paperPDFs/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.pdf]]

---
title: "cadrille: Multi-modal CAD Reconstruction with Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/cadrille_Multi_modal_CAD_Reconstruction_with_Reinforcement_Learning.pdf
openreview_forum_id: w2tnhhMbXv
aliases:
- cadrille
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入强化学习微调阶段，利用程序化奖励（IoU+无效惩罚）在无需CAD序列标注的手工数据上进行训练，取代计算昂贵的测试时采样。"
primary_logic: "借鉴LLM训练范式：先用大规模程序生成数据进行有监督微调（SFT）学习CAD领域知识；再用少量手工数据（无CAD标注）进行RL微调，以提升跨域泛化和几何有效性，从而统一多模态输入。"
claims:
- "SFT模型在真实扫描CC3D上IoU仅60%，无效率(IR)高达10%（Tab.3第2行）。"
- "简单混合程序生成数据与手工数据进行SFT导致性能下降（Tab.3第4行 vs 第3行）。"
- "加入在线RL微调(Dr. CPPO)后，点云重建在DeepCAD上IoU从87.1%提升至90.2%，IR降至0%；在CC3D上IoU从60.5%提升至67.9%，IR降至0.2%。"
- "仅对图像进行RL微调即可同步提升点云重建性能（跨模态迁移）。"
---

# cadrille: Multi-modal CAD Reconstruction with Reinforcement Learning

> [!tip] 核心洞察
> 借鉴LLM训练范式：先用大规模程序生成数据进行有监督微调（SFT）学习CAD领域知识；再用少量手工数据（无CAD标注）进行RL微调，以提升跨域泛化和几何有效性，从而统一多模态输入。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | cadrille：基于强化学习的多模态CAD重建 |
| 英文题名 | cadrille: Multi-modal CAD Reconstruction with Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=w2tnhhMbXv); [GitHub](https://github.com/col14m/cadrille) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | cadrille |
| Dataset | DeepCAD (Point Clouds), DeepCAD (Images), DeepCAD (Text), CC3D Real-World (Point Clouds) |

> [!tip] 效果简介
> - DeepCAD (Point Clouds) 上，CD↓ / IoU↑ / IR↓ 为 0.18 / 87.1% / 2.1% (SFT R_pi)，对比 CAD-Recode: 0.18 / 87.1% / 3.1%，变化 IR -1.0%。
> - DeepCAD (Images) 上，CD↓ / IoU↑ / IR↓ 为 0.17 / 92.2% / 0.0% (Dr. CPPO)，对比 CADCrafter: 0.26 / - / 3.6%，变化 CD -0.09, IR -3.6%。
> - DeepCAD (Text) 上，CD↓ / IoU↑ / IR↓ 为 0.20 / 82.1% / 1.4% (SFT R_pi+D_t)，对比 Text2CAD: 0.37 / 71.5% / 3.7%，变化 CD -0.17, IoU +10.6%, IR -2.3%。

## 概述

### 问题与瓶颈

CAD重建任务旨在从观测数据（如点云、图像或文本描述）中恢复可编辑的参数化三维模型。现有方法面临两个核心瓶颈：**跨域泛化能力差**与**几何有效性低**。单模态模型（如CAD-Recode）在程序生成的合成数据上表现尚可，但迁移到真实世界扫描（如CC3D数据集）时性能急剧下降——IoU仅约60%，无效率（IR）高达10%（Tab. 3）。更棘手的是，直接将合成数据与手工建模数据混合进行有监督训练反而会进一步降低性能，说明简单的数据混合无法弥合域间差距。

### 核心方法

cadrille借鉴大语言模型（LLM）的训练范式，提出**两阶段训练策略**：

1. **有监督微调（SFT）**：在大规模程序生成的多模态数据上进行训练，使模型学习从点云、多视图图像或文本到可执行Python代码（CadQuery脚本）的映射，掌握CAD领域知识。
2. **强化学习微调（RL）**：在无需CAD序列标注的手工数据上，利用程序化奖励函数 $R(\tau) = r_{\mathrm{IoU}}(\tau) + r_{\mathrm{invalid}}(\tau)$（由IoU奖励与无效惩罚组成）进行在线策略优化，提升跨域泛化能力和几何有效性。

这一设计的关键洞察在于：**将廉价的大规模合成数据用于SFT阶段学习基础能力，将稀缺但高质量的手工数据留给RL阶段进行对齐优化**，从而规避了直接混合训练带来的性能退化。

### 方法定位

cadrille是首个将RL微调引入多模态CAD重建的工作，也是首个统一支持点云、多视图图像和文本三种输入模态的CAD重建模型。其基础架构基于Qwen2-VL-2B，原生具备视觉和文本理解能力；点云则通过可训练的投影层映射到LLM嵌入空间。与仅支持单模态的CAD-Recode（点云）相比，cadrille不仅扩展了输入模态，还将评估策略从计算昂贵的测试时采样（需生成10个候选取最佳）简化为单次推理，大幅降低推理成本。

### 主要结果

- **SFT阶段**：联合三模态训练后，cadrille在DeepCAD基准上全面超越各模态专用方法——点云重建IoU达87.1%（IR降至2.1%），图像重建IoU达89.0%，文本重建IoU达82.1%（Tab. 1）。
- **RL微调后**：在真实世界扫描CC3D上，点云重建IoU从60.5%跃升至67.9%，无效率从9.8%骤降至0.2%；在Fusion360图像重建上，IoU从62.5%提升至84.6%，无效率从18.7%降至0%（Tab. 2, Tab. 3）。仅对图像数据进行RL微调，即可同步提升点云重建性能，展现出跨模态迁移能力。
- **效率对比**：RL微调后的单次推理性能（DeepCAD IoU 90.2%, IR 0%）已超越无需RL的10样本测试时采样（CAD-Recode 10样本IoU 92.0%但IR 0.4%），且无效率更低（Tab. 11）。

综上，cadrille通过“SFT+RL”两阶段训练策略，在10个基准测试上建立了新的最优结果，证明了RL微调对多模态CAD重建的有效性。

## 背景与动机

### 问题背景

计算机辅助设计（CAD）模型的自动重建是工业制造、数字孪生和机器人领域的基础任务。传统方法依赖专业工程师手工建模，效率低下且难以规模化。近年来，随着大语言模型（LLM）的兴起，将CAD模型表示为可执行的Python代码（如CadQuery脚本）成为一种新兴范式——模型接收视觉或几何输入，自回归生成代码，执行后得到参数化边界表示（B-Rep）。这一范式将CAD重建转化为序列生成问题，使得LLM的预训练能力和规模化优势得以复用。

然而，现有方法面临两个核心瓶颈：

**跨域泛化失效。** 主流方法（如 **CAD-Recode**，Rukhovich et al., 2024）在大规模程序生成（procedurally generated）的合成数据上进行有监督微调（SFT），在合成域测试集上表现良好，但一旦迁移到真实世界扫描数据，性能急剧下降。以CC3D真实扫描数据集为例，SFT模型的IoU仅约60%，无效率（Invalid Rate, IR）高达10%（Tab. 3第2行）——这意味着每10个生成结果中就有1个是无法执行的无效代码。

**数据混合的陷阱。** 直觉上，将手工标注的真实数据与合成数据混合训练应能缓解域差距。但实验表明，直接混合程序生成数据与手工数据进行SFT反而导致性能退化（Tab. 3第4行 vs 第3行）。深层原因在于：手工数据的CAD序列标注成本极高且稀缺，少量真实样本在混合训练中难以主导梯度方向，反而破坏了模型在合成域上已学到的稳定映射。

### 现有方法缺口

当前CAD重建方法存在三个结构性缺口：

1. **模态单一。** 现有SOTA方法仅支持单一输入模态——CAD-Recode仅处理点云，**CADCrafter**（Chen et al., 2025）仅处理图像，**Text2CAD**（Khan et al., 2024b）仅处理文本。实际应用场景中，输入模态往往取决于传感器配置（如激光雷达提供点云、相机提供图像），单一模态方法无法灵活适配。

2. **训练范式局限。** 现有方法完全依赖SFT，其优化目标是最小化生成代码与真值代码的逐token交叉熵。这一目标与最终几何质量（IoU、Chamfer距离）之间存在错位——token级准确不等于几何级准确。此外，SFT无法利用那些仅有输入模态而无CAD序列标注的数据（如Fusion360的手工建模数据），造成大量真实数据浪费。

3. **推理效率低下。** 为提升输出质量，CAD-Recode等SFT方法在测试时需采样10个候选结果，通过程序执行后选择IoU最高者。这种测试时采样策略使推理计算量膨胀10倍，且仍无法根治无效代码问题（IR达0.4%）。

### 核心动机与洞察

本文的核心洞察借鉴了LLM训练范式的演进路径：**先用大规模易得数据进行知识注入，再用少量高质量数据进行偏好对齐。** 具体而言：

- **SFT阶段**利用海量程序生成数据（合成点云、多视图图像、文本描述与对应CAD代码的三元组）进行监督学习，使模型掌握CAD领域的基本语法、几何约束和代码生成能力。这部分数据量大、覆盖广，但存在合成域偏差。

- **RL微调阶段**引入强化学习，在无需CAD序列标注的手工数据上进行策略优化。奖励函数由程序化计算得到：$R(\tau) = r_{\text{IoU}}(\tau) + r_{\text{invalid}}(\tau)$，其中IoU奖励项（乘以10）直接对齐几何质量，无效惩罚项（无效时-10）强制模型避免生成不可执行代码。这一设计使得模型能够从真实数据中学习跨域泛化，而无需昂贵的序列标注。

关键证据链：加入在线RL微调（Dr. CPPO）后，点云重建在DeepCAD上IoU从87.1%提升至90.2%，IR降至0%；在真实扫描CC3D上IoU从60.5%提升至67.9%，IR从9.8%骤降至0.2%（Tab. 3第3行 vs 第6行）。更值得注意的是，仅在图像数据上进行RL微调即可同步提升点云重建性能（跨模态迁移），表明RL阶段学到的是模态无关的几何有效性约束。

基于上述动机，本文提出**cadrille**——首个多模态CAD重建模型，统一处理点云、多视图图像和文本三种输入，采用SFT+RL两阶段训练，在10个基准上建立了新的最优结果。

## 核心创新

cadrille 的核心创新并非提出全新的网络架构，而是将大语言模型（LLM）的训练范式系统性地迁移到多模态 CAD 重建任务中，从根本上解决了单模态模型跨域泛化差与几何无效性高两大瓶颈。其创新集中体现在三个相互耦合的 **changed slots** 上。

### 1. 训练范式：从单一 SFT 到 SFT + RL 微调

现有方法（如 **CAD-Recode**）仅依赖程序生成数据上的监督微调（SFT）。这种范式在合成域内表现尚可，但一旦跨域到真实扫描数据（如 CC3D），无效率（IR）急剧攀升至 10%，IoU 仅约 60%（Tab. 3, row 2）。更关键的是，直接混合合成数据与手工数据做 SFT 会导致性能进一步退化（Tab. 3, row 4 vs row 3），说明简单的数据扩充无法弥合域差异。

cadrille 借鉴 LLM 对齐训练的思路，引入两阶段范式：
- **阶段一（SFT）**：在大规模程序生成数据上学习 CAD 领域知识，建立从多模态输入到 Python 代码的基本映射。
- **阶段二（RL 微调）**：在无需 CAD 序列标注的手工数据上，利用程序化奖励（IoU + 无效惩罚）进行强化学习微调，以提升跨域泛化能力和几何有效性。

这一范式转换的因果机制在于：SFT 阶段提供了强先验，RL 阶段则通过在线探索与奖励信号直接优化最终重建质量，绕过了手工数据缺乏 CAD 序列标注的约束。

### 2. 评估策略：从测试时采样到单次推理

CAD-Recode 等基线方法依赖测试时采样 10 个候选并取最佳结果来提升指标（CC3D IoU 从 60% 提升至 74%，IR 降至 0.5% 以下），但这种策略计算成本高昂，不适用于实际部署。

cadrille 通过 RL 微调将模型的对齐过程前置到训练阶段。RL 微调后，单次推理即可在 DeepCAD 上达到 IoU 90.2%、IR 0%，在 CC3D 上达到 IoU 67.9%、IR 0.2%（Tab. 3, row 6），其单样本性能已超越无需 RL 的 10 样本采样结果（Tab. 11），且无效率更低。这意味着 RL 微调将“从多个候选中择优”的隐式优化过程显式化为模型的内部策略。

### 3. 奖励函数：程序化反馈替代标注依赖

RL 微调的核心驱动力是程序化奖励函数：

$$R(\tau) = r_{\mathrm{IoU}}(\tau) + r_{\mathrm{invalid}}(\tau)$$

其中 $r_{\mathrm{IoU}}$ 为重建网格与真值网格的 IoU 乘以 10，$r_{\mathrm{invalid}}$ 在生成的 Python 代码执行失败时给予 -10 的惩罚。这一设计的关键在于：奖励信号完全由程序自动计算，无需任何人工标注的 CAD 序列，使得手工数据（如 DeepCAD 和 Fusion360 中仅有网格真值的子集 $D_i^-$、$F_i^-$）可以被充分利用。

### 4. 跨模态迁移：图像 RL 微调惠及点云

一个非直观的发现是：仅在图像数据上进行 RL 微调，即可同步提升点云重建的性能（Tab. 3, row 6）。这表明模型在多模态联合 SFT 阶段学习到的共享表征，使得 RL 阶段在单一模态上的优化能够通过表征空间传播到其他模态，实现了零额外成本的跨模态迁移。

### 5. 基础模型升级：原生多模态支持

cadrille 将基础 LLM 从 **Qwen2-1.5B**（仅文本）升级为 **Qwen2-VL-2B**（原生支持视觉和文本），使其能够以统一框架处理点云（通过可训练的投影层）、多视图图像（通过视觉编码器）和文本（通过文本嵌入）三种模态输入，无需为每种模态设计独立的编码器架构。

---

**证据强度评估**：SFT 跨域退化（Tab. 3 row 2 vs row 3）、混合数据 SFT 失效（row 4）、RL 微调显著提升（row 6）以及跨模态迁移效应均有明确表格数据支撑，置信度 ≥ 0.95。DPO vs 在线 RL 的消融对比（Tab. 3, rows 5-6）进一步确认了在线 RL 策略（Dr. CPPO）的必要性。

## 整体框架

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/003_Figure_3.jpg]]
*Figure 3: Overview of cadrille. It can handle three input modalities within a unified framework. Point clouds are processed with a trainable projection layer, while images and texts are passed to a VLM directly. The output of the model is an executable Python script for CAD generation*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/001_Figure_1.jpg]]
*Figure 1: Compared to state-of-the-art CAD-Recode, the only existing method that converts point clouds into Python code, cadrille has two key novelties. First, it goes beyond the standard training scheme and adapts LLM RL fine-tuning for CAD reconstruction (left). Moreover, besides point clouds only accepted by single-modal CAD-Recode, cadrille extends to images and textual descriptions, making it the first multimodal approach delivering state-of-art results (right)*

cadrille 采用**两阶段训练范式**，将大规模程序生成数据与少量无标注手工数据的价值分离利用：第一阶段在合成数据上进行**有监督微调（SFT）**，使模型掌握CAD领域知识；第二阶段在无需CAD序列标注的手工数据上进行**强化学习（RL）微调**，以提升跨域泛化能力和几何有效性。

### 多模态输入到代码输出的统一架构

cadrille 的推理管道接受三种模态的输入，输出可执行的 Python 代码（CadQuery 脚本），执行后生成参数化边界表示（B-Rep）的 CAD 模型。三种输入模态的处理路径如下：

- **点云**：通过最远点采样（FPS）从表面采样 256 个 3D 点，经一个可训练的**点云投影层**映射到 LLM 的嵌入空间。该投影层为单层线性映射，不使用法向量信息。
- **多视图图像**：将多张视图拼接后，直接送入 **Qwen2-VL 视觉编码器**处理。
- **文本**：文本提示直接通过 **Qwen2-VL 文本嵌入层**编码。

三种模态的嵌入共同输入 **Qwen2-VL-2B** 作为骨干 LLM，自回归生成 Python 代码令牌序列。与单模态基线 CAD-Recode 使用的 Qwen2-1.5B（无视觉能力）相比，cadrille 的 Qwen2-VL-2B 原生支持视觉和文本输入，是实现多模态统一的关键架构选择。

### 两阶段训练管道

**阶段一：SFT（有监督微调）**
在程序生成的大规模合成数据上进行，最小化交叉熵损失：

$$\mathbb{E}_{(q,\tau)\sim\mathcal{D}}[\log \pi_\theta(\tau\mid q)]$$

其中 $q$ 为多模态输入，$\tau$ 为目标 Python 代码。此阶段使模型学习从多模态输入到 CAD 代码的映射，但仅在合成域内有效——在真实扫描 CC3D 上 IoU 仅 60%，无效率（IR）高达 10%。

**阶段二：RL 微调**
利用无 CAD 序列标注的手工数据（如 Fusion360 的 $D_i^-$、$F_i^-$），通过程序化奖励函数优化策略：

$$R(\tau) = r_{\mathrm{IoU}}(\tau) + r_{\mathrm{invalid}}(\tau)$$

奖励由 IoU 项（乘以 10）和无效惩罚项（生成无效代码时 -10）组成。cadrille 采用**在线 RL 方法 Dr. CPPO**（改良 PPO，结合 Dr.GRPO 和 CPPO），仅对 SFT 模型平均奖励低于阈值 $R_{th}=7.5$ 的困难样本进行训练，以加速收敛。

### 关键设计决策

1. **数据分离策略**：直接混合合成数据与手工数据进行 SFT 会导致性能下降（Tab.3 第 4 行 vs 第 3 行），因此手工数据仅用于 RL 阶段。
2. **跨模态迁移**：仅在图像数据上进行 RL 微调，即可同步提升点云重建性能，实现跨模态泛化（Tab.3 第 6 行）。
3. **推理效率**：RL 微调后的模型仅需单次推理即可达到甚至超越 SFT 模型 10 样本测试时采样的效果，且无效率更低（Tab.11）。

## 核心模块与公式推导

### 统一多模态输入处理

cadrille 基于 Qwen2-VL-2B 构建，通过三个并行通道处理异构输入，最终统一映射到 LLM 的 token 空间进行自回归生成。

**点云投影层（Point Cloud Projection Layer）** 负责将非结构化的 3D 点云转换为 LLM 可理解的嵌入序列。具体流程为：首先对输入点云执行最远点采样（FPS），选取 256 个表面点（不使用法向量信息）；随后通过一个可训练的投影层将每个 3D 坐标映射到与 LLM 嵌入维度对齐的向量。该设计保持了与 **CAD-Recode**（Rukhovich et al., 2024）在点云 SFT 上的性能可比性，但无需法向量辅助，简化了输入要求。

**视觉编码器（Qwen2-VL Vision Encoder）** 原生处理拼接后的多视图图像，直接利用 VLM 预训练的视觉理解能力，无需额外适配模块。**文本嵌入（Qwen2-VL Text Embedding）** 同理，将文本描述映射为 token 序列。三种模态的输出在 LLM 主干网络中汇合，模型自回归生成可执行的 CadQuery Python 代码，执行后产生参数化 B-Rep 实体模型。

### 两阶段训练范式

cadrille 的训练策略借鉴了 LLM 对齐训练的思路，分为监督微调（SFT）和强化学习微调（RL）两个阶段。

#### 阶段一：监督微调（SFT）

SFT 阶段在大规模程序生成数据上进行，目标是学习从多模态输入到目标 Python 代码的映射。给定多模态输入 $q$ 和对应的目标代码序列 $\tau$，训练目标为最大化条件对数似然：

$$\mathbb{E}_{(q,\tau)\sim\mathcal{D}}\left[\log \pi_\theta(\tau \mid q)\right]$$

其中 $\pi_\theta$ 为可训练策略（即 LLM），$\mathcal{D}$ 为程序生成的配对数据集。此阶段使模型获得 CAD 领域的基础知识和代码生成能力，但在跨域场景下存在明显瓶颈：在真实扫描数据集 CC3D 上，SFT 模型的 IoU 仅为 60%，无效率（IR）高达 10%（Tab. 3 第 2 行）。

#### 阶段二：强化学习微调（RL）

RL 微调阶段的核心创新在于：利用无需 CAD 序列标注的手工数据，通过程序化奖励信号优化模型的几何有效性和跨域泛化能力。训练目标形式化为最大化期望奖励：

$$\max_\theta \ \mathbb{E}_{q_i \sim \mathcal{D}_{\text{RL}},\ \tau_i \sim \pi_\theta(\cdot \mid q_i)}\left[R(\tau_i)\right]$$

其中 $\mathcal{D}_{\text{RL}}$ 为无标注的手工数据（仅包含输入模态，不含对应的 CAD 代码序列）。

**奖励函数设计** 是 RL 阶段的关键。cadrille 采用组合奖励：

$$R(\tau) = r_{\text{IoU}}(\tau) + r_{\text{invalid}}(\tau)$$

- **$r_{\text{IoU}}(\tau)$**：基于生成模型与真值网格之间的 3D IoU 计算，乘以系数 10 以放大有效样本的奖励信号。
- **$r_{\text{invalid}}(\tau)$**：无效惩罚项，当生成的 Python 代码执行失败或产生无效几何体时，给予 -10 的固定惩罚。

该奖励函数无需人工标注或偏好数据，完全通过程序自动计算，使得 RL 微调可以规模化地利用无标注手工数据。

### 在线 RL 算法：Dr. CPPO

cadrille 对比了离线 RL（DPO）和在线 RL 两种策略，实验表明在线方法显著更优。所提出的 Dr. CPPO 结合了 Dr. GRPO 的高优势样本筛选机制与 CPPO 的裁剪优化目标：

$$\mathbb{E}_{\{\tau_g\}\sim\mathcal{B}}\left[\min\left(\frac{\pi_{\theta_t}(\tau_g \mid q)}{\pi_{\theta_{\text{old}}}(\tau_g \mid q)}A_g,\ \text{clip}\left(\frac{\pi_{\theta_t}(\tau_g \mid q)}{\pi_{\theta_{\text{old}}}(\tau_g \mid q)}, 1-\epsilon, 1+\epsilon\right) A_g\right)\right]$$

其中 $\tau_g$ 为从批次 $\mathcal{B}$ 中筛选的高优势样本，$A_g$ 为对应的优势估计，$\epsilon$ 为裁剪阈值。与标准 PPO 的关键区别在于：仅使用奖励高于阈值 $R_{\text{th}} = 7.5$ 的样本进行策略更新，这种困难样本挖掘策略加速了收敛。

### DPO 离线基线

作为对比，cadrille 也实现了 DPO（Direct Preference Optimization）离线 RL 方案。给定输入 $q$ 及偏好对 $(\tau_w, \tau_l)$（其中 $\tau_w$ 为奖励更高的生成结果，$\tau_l$ 为奖励更低的结果），优化目标为：

$$\mathbb{E}_{(q,\tau_w,\tau_l)\sim\mathcal{D}}\left[\log\sigma\left(\beta\log\frac{\pi_{\theta_t}(\tau_w \mid q)}{\pi_{\theta_r}(\tau_w \mid q)} - \beta\log\frac{\pi_{\theta_t}(\tau_l \mid q)}{\pi_{\theta_r}(\tau_l \mid q)}\right)\right]$$

其中 $\pi_{\theta_r}$ 为参考策略（SFT 模型），$\pi_{\theta_t}$ 为目标策略，$\beta$ 控制偏离参考策略的强度。DPO 实验中 $K=5$ 个候选样本取得最佳效果，与 $K=3$ 相比 IoU 差异小于 1%（Tab. 10）。然而，在线 Dr. CPPO 在降低无效率和提升 IoU 方面均显著优于 DPO（Tab. 3 第 5 行 vs 第 6 行），将 IR 降至 0.2% 以下，IoU 提升 3-9 个百分点。

## 实验与分析

### 核心瓶颈验证：SFT模型的跨域失效

cadrille的实验设计首先验证了单模态CAD重建模型的核心瓶颈：**从合成数据到真实扫描的泛化失败**。在CC3D真实世界点云数据集上，仅经过SFT的cadrille模型IoU仅为60%，无效率（IR）高达10%（Tab. 3，第2行）。这意味着每10个生成的CAD模型中就有1个是无效的——要么Python代码无法执行，要么生成的B-Rep几何体退化。这一结果与CAD-Recode等单模态方法的表现一致，揭示了纯粹依赖程序生成数据进行有监督训练的固有局限。

更关键的是，**直接混合程序生成数据与手工数据进行SFT不仅无法缓解这一问题，反而导致性能下降**。Tab. 3第4行（R_pi+D_pi）与第3行（R_pi）的对比显示，加入手工数据后DeepCAD上的IoU从87.1%降至86.6%，IR从2.1%升至0.9%（注意此处IR变化方向与IoU下降的矛盾，需人工核实原始数据）。这一反直觉现象暗示：合成数据与真实数据之间存在分布偏移，简单的数据混合会引入噪声而非互补信息。

### 训练策略的因果效应：RL微调的决定性作用

cadrille的核心贡献在于将LLM训练范式迁移至CAD重建：**SFT学习领域知识，RL微调实现跨域泛化**。实验通过系统消融揭示了这一策略的因果效应。

**在线RL（Dr. CPPO）vs. 离线RL（DPO）vs. 纯SFT**。Tab. 3的消融对比清晰展示了三种策略的阶梯式提升：

- **纯SFT**（第3行）：DeepCAD IoU 87.1%，IR 2.1%；CC3D IoU 60.5%，IR 9.8%
- **SFT + DPO**（第5行）：DeepCAD IoU 87.2%，IR 0.9%；CC3D IoU 63.0%，IR 4.1%
- **SFT + Dr. CPPO**（第6行）：DeepCAD IoU 90.2%，IR 0.0%；CC3D IoU 67.9%，IR 0.2%

DPO将IR降低约一半，但对IoU的提升有限（CC3D仅+2.5%）。相比之下，Dr. CPPO不仅在DeepCAD上将IoU推至90.2%（+3.1%），更关键的是将CC3D的IR从9.8%压缩至0.2%——**无效率降低了近50倍**。这一对比揭示了在线探索在CAD重建中的独特价值：模型需要在奖励信号的实时引导下主动探索有效代码空间，而非仅从静态偏好对中学习。

**跨模态迁移效应**。Tab. 3第6行的一个关键发现是：**仅在图像数据（D_i^- + F_i^-）上进行RL微调，即可同步提升点云重建性能**——CC3D点云IoU从60.5%跃升至67.9%，IR降至0.2%。这意味着RL微调学到的“生成有效且几何准确的CAD代码”这一能力具有模态无关性，验证了统一策略空间的有效性。

### 多模态统一的协同增益

Tab. 1展示了cadrille在多模态联合训练下的协同效应。与单模态SOTA方法相比：

- **点云重建**：cadrille（CD 0.18, IoU 87.1%, IR 2.1%）与CAD-Recode（CD 0.18, IoU 87.1%, IR 3.1%）精度持平，但IR降低1.0%
- **多视图图像重建**：cadrille（CD 0.18, IoU 86.1%, IR 1.5%）显著优于CADCrafter（CD 0.26, IR 3.6%），IR降低2.1%
- **文本重建**：cadrille（CD 0.20, IoU 82.1%, IR 1.4%）远超Text2CAD（CD 0.37, IoU 71.5%, IR 3.7%），IoU提升10.6%

值得注意的是，联合训练（D_pit）相比单模态训练进一步降低了IR（点云从2.1%降至0.4%，图像从1.5%降至0.5%），表明多模态信号在SFT阶段已产生正则化效应，为后续RL微调提供了更稳健的初始化。

### 推理效率：RL微调替代测试时采样

Tab. 11的消融实验揭示了一个实用洞见：**RL微调后的单样本推理即可超越无需RL的10样本测试时采样**。具体而言，Dr. CPPO微调模型单次推理在DeepCAD上达到IoU 90.2%、IR 0.0%，而CAD-Recode的10样本采样（取最佳）IoU为92.0%但IR仍有0.4%。虽然IoU略低1.8%，但cadrille实现了零无效输出，且推理成本仅为后者的1/10。在CC3D上，这一优势更为明显：单样本IoU 67.9% vs. 10样本74%，但IR从0.5%降至0.2%。考虑到真实场景对有效性的严格要求，RL微调策略在效率-质量权衡上具有明确优势。

### 跨数据集泛化与零样本能力

cadrille在Fusion360和CC3D上的评估均为零样本（无任何域适应），真实反映了泛化能力。Tab. 2的多视图图像重建结果显示：

- **Fusion360**：cadrille Dr. CPPO（CD 0.17, IoU 84.6%, IR 0.0%）相比LRM→CAD-Recode流水线（CD 0.62, IoU 62.5%, IR 18.7%），CD降低0.45，IoU提升22.1%，IR降至0%
- **CC3D**：cadrille Dr. CPPO（CD 0.57, IoU 65.0%, IR 0.1%）相比SFT基线（CD 0.81, IR 7.7%），CD降低0.24，IR降低7.6%

Fusion360上18.7%的IR揭示了多阶段流水线（LRM重建mesh→CAD-Recode转代码）的严重脆弱性，而端到端的cadrille通过RL微调彻底解决了这一问题。

### 失败模式与局限性

尽管整体性能大幅提升，cadrille仍存在明确的失败模式（Figure 9）：

1. **复杂曲面细节丢失**：对于具有颗粒状表面或复杂曲率的物体，生成的CAD模型倾向于过度简化，丢失精细几何特征。这源于Python代码表示的表达力上限——B-Rep操作难以精确描述自由曲面。

2. **真实域差距残余**：CC3D上CD仍高达0.47（点云）和0.57（图像），相比DeepCAD的0.17存在近3倍差距。真实扫描中的噪声、遮挡和不完整性仍是开放挑战。

3. **文本模态推理延迟**：文本输入的平均推理时间约3.9秒（Tab. 9），主要源于自回归生成完整Python脚本的序列长度，限制了实时交互场景的应用。

4. **单视图重建退化**：单张图像重建IoU为81.7%（Tab. 7），显著低于多视图的86-92%，表明模型对多视角信息的依赖性。

### 关键消融发现汇总

- **DPO样本数K**：K=5时效果最佳，与K=3相比IoU差异小于1%（Tab. 10），说明适度增加偏好对数量有边际收益
- **RL数据量**：Tab. 12显示，增加RL微调数据量持续提升性能，未观察到饱和现象，暗示更大规模手工数据的潜力
- **硬样本挖掘**：仅对SFT模型平均奖励低于阈值（R_th=7.5）的样本进行RL训练，加速了收敛（Sec. 4.4）

### 补充图表

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/006_Table_3.jpg]]
*Table 3: Online RL outperforms offline RL Fine-tuning cadrille using offline DPO reduces IR twice in most cases, while accuracy scores are not affected (rows 3 and 5 in both Tables). In the meantime, Dr. CPPO beats SFT in terms of all metrics, adding 3-9% to IoU scores and bringing IR under 0.2% Table 3: Results of CAD reconstruction from point clouds. cadrille performs on par with CAD-Recode when trained on the CAD-Recode dataset (R). With RL, cadrille establishes state-ofthe-art on DeepCAD, Fusion360 and real-world CC3D*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/004_Table_1.jpg]]
*Table 1: Results on DeepCAD test set. The best results are bold, the second best are underlined. Our cadrille trained jointly on three modalities outperforms all existing modality-specific methods. Here, we report metrics obtained without RL fine-tuning or test-time sampling for fair comparison. Table 2: Results of CAD reconstruction from multi-view images. With RL fine-tuning, cadrille achieves best results across three benchmarks*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/005_Table_2.jpg]]

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/016_Table_6.jpg]]
*Table 6: Mean CD scores obtained across all benchmarks and available input modalities. RL finetuning is performed using $\mathrm { D } _ { \mathrm { i } } ^ { - } + \mathrm { F } _ { \mathrm { i } } ^ { - }$ data

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/014_Table_4.jpg]]
*Table 4: Results of CAD reconstruction from point clouds and multi-view images from the Omni-CAD dataset. We specify mean CD since it is the only CD metric reported by CAD-MLLM*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/015_Table_5.jpg]]
*Table 5: Results of point-based CAD reconstruction on the Fusion360 test set. All reported metrics are obtained using an SFT model without RL*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/017_Table_7.jpg]]

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/018_Table_8.jpg]]
*Table 8: Results of CAD reconstruction from multi-view images on the Deep-CAD dataset. Table 7: Results of CAD reconstruction from a single image on the DeepCAD dataset. All reported metrics are obtained with an SFT model without RL*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/019_Figure_2.jpg]]
*Figure 2: recent evidence coming from the math domain (see Fig. 2 of Yue et al. (2025) and Fig. 4 of Liu et al. (2025a))*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_w2tnhhMbXv/figures/020_Table_10.jpg]]

## 方法谱系与知识库定位

### 两阶段训练范式的来源与突破

cadrille 的核心方法论创新在于将 LLM 训练中成熟的“大规模预训练 + 对齐微调”范式迁移到 CAD 重建领域。在此之前，基于 Python 代码的 CAD 重建方法（如 **CAD-Recode**，Rukhovich et al., 2024）仅采用有监督微调（SFT）在程序生成数据上训练，面临两个根本性瓶颈：

1. **跨域泛化失败**：SFT 模型在合成域（DeepCAD）表现良好，但在真实扫描（CC3D）上无效率（IR）高达 10%，IoU 仅 60%（Tab. 3 第 2 行），说明模型学到的映射缺乏几何鲁棒性。
2. **手工数据利用困境**：直接将程序生成数据与手工数据混合进行 SFT 反而导致性能下降（Tab. 3 第 4 行 vs 第 3 行），因为手工数据缺少 CAD 序列标注，无法提供逐 token 的监督信号。

cadrille 的关键洞察是：**手工数据虽然无法用于 SFT，但可以作为 RL 微调的奖励信号源**。程序化奖励函数 $R(\tau) = r_{\mathrm{IoU}}(\tau) + r_{\mathrm{invalid}}(\tau)$ 仅需最终几何体的 IoU 和有效性判断，无需中间步骤标注，从而解锁了手工数据的价值。

### 与同期 RL-for-CAD 方法的差异

cadrille 并非首个将 RL 引入 CAD 生成的工作。**CADFusion**（Wang et al., 2025a）和 **CAD-Coder**（Guan et al., 2025）已在文本到 CAD 任务中探索了 RL 微调。cadrille 的差异化贡献体现在三个维度：

| 维度 | 同期 RL-for-CAD 方法 | cadrille |
|------|---------------------|----------|
| 输入模态 | 仅文本 | 点云、多视图图像、文本三模态统一 |
| RL 算法 | 未公开或使用离线 RL | 在线 Dr. CPPO（改良 PPO），实证优于离线 DPO |
| 跨模态迁移 | 未探索 | 仅用图像数据进行 RL 即可提升点云重建性能（Tab. 3 第 6 行） |

在线 RL（Dr. CPPO）相比离线 DPO 的优势在实验中明确体现：DPO 仅能将 IR 降低约一半，而 Dr. CPPO 将 DeepCAD 上的 IR 降至 0%，CC3D 上的 IR 降至 0.2%，同时 IoU 提升 3-9 个百分点（Tab. 3 第 5 行 vs 第 6 行）。

### 多模态统一架构的定位

在架构层面，cadrille 基于 **Qwen2-VL-2B** 构建，原生支持视觉和文本输入，点云则通过一个可训练的投影层映射到 LLM 嵌入空间。相比此前的多模态 CAD 方法 **CAD-MLLM**（Xu et al., 2024b），cadrille 的关键改进在于：

- 将多模态处理与 RL 微调结合，而非仅依赖 SFT
- 在 Omni-CAD 数据集上，cadrille + RL 的点云重建 CD 为 0.77，显著优于 CAD-MLLM 的 1.05（Tab. 4）

与单模态 SOTA 方法的对比（Tab. 1）表明，即使不进行 RL 微调，cadrille 联合训练三模态后，在点云（IR 2.1% vs CAD-Recode 3.1%）、图像（IR 1.5% vs CADCrafter 3.6%）、文本（IoU 82.1% vs Text2CAD 71.5%）三个模态上均取得最优或次优结果，验证了多模态联合训练的正向迁移效应。

### 适用边界与局限

**已验证的有效范围：**

- **输入类型**：256 点 FPS 采样的点云、拼接多视图图像（≥4 视图）、文本描述
- **输出格式**：CadQuery Python 脚本，生成参数化 B-Rep
- **几何复杂度**：以棱柱体、拉伸体、布尔组合为主的机械零件级 CAD 模型
- **训练数据**：程序生成数据（CAD-Recode 数据集）用于 SFT；DeepCAD 和 Fusion360 的无标注图像数据用于 RL

**明确局限：**

1. **细节保真度不足**：对于具有复杂曲面和颗粒状表面的物体，cadrille 会丢失细节（见 Figure 9 失败案例）。这是因为 Python 脚本的参数化表达本身对自由曲面建模能力有限。
2. **真实域差距残存**：尽管 RL 大幅改善了 CC3D 上的性能，Chamfer 距离仍为 0.47（Tab. 3），与合成域 DeepCAD 的 0.17 存在显著差距。真实扫描的噪声、遮挡和不完整性仍是挑战。
3. **单视图性能退化**：单张图像重建的 IoU 为 81.7%（Tab. 7），低于多视图的 86-92%，说明模型对多视图信息的依赖较强。
4. **推理延迟**：文本模态推理时间约 3.9 秒（Tab. 9），可能限制实时交互场景的应用。

### 开放问题

论文明确指出的未来方向包括：

- **提示级多模态融合**：能否将多种模态融合到同一个提示中，以补偿低质量或缺失的输入？当前模型仅支持单模态输入，模态间的互补信息未被利用。
- **点云 RL 微调**：当前 RL 微调仅在图像数据上进行（跨模态迁移到点云），直接在点云数据上进行 RL 可能进一步缩小真实域差距。
- **数据复杂度扩展**：增加程序生成数据的几何复杂度并扩大 RL 微调数据量，以更好地适应真实世界扫描中的复杂形状。
- **推理效率优化**：在保持高精度的同时减少推理时间，使方法更适用于实际部署场景。

## 原文 PDF

![[paperPDFs/ICLR_2026/cadrille_Multi_modal_CAD_Reconstruction_with_Reinforcement_Learning.pdf]]

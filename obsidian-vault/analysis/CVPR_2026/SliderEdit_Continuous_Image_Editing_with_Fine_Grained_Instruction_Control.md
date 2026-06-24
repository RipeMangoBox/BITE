---
title: "SliderEdit: Continuous Image Editing with Fine-Grained Instruction Control"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SliderEdit_Continuous_Image_Editing_with_Fine_Grained_Instruction_Control.pdf
project_link: null
code_link: null
aliases:
- SSGA
- SliderEdit
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: MMDiT 中每条指令对应的中间 token 嵌入是高度局部化的语义载体；通过引入低秩适配器（STLoRA/GSTLoRA）选择性抑制目标指令 token 的表示，并平滑缩放适配器的权重，即可实现对单条指令编辑效果的连续调制。
primary_logic: 通过 Partial Prompt Suppression (PPS) 损失训练一个轻量级选择式 Token LoRA，使其学会“中和”特定指令的视觉效应；训练后该适配器即成为一条连续滑块，可通过缩放因子实现从完全抑制到完全应用的平滑过渡，为指令级图像编辑提供全局可训练的、解耦的连续控制框架。
claims:
- SliderEdit 为指令式图像编辑首次引入连续、细粒度的指令强度控制，可实现平滑的解耦调节。
- GSTLoRA 在单指令编辑中实现了最高的连续性和较低的身份漂移，显著优于显式/隐式无分类器引导基线。
- STLoRA 在包含2-3条指令的编辑中产生连续、解耦的二维/三维编辑空间，而所有基线方法均无法实现这种逐指令独立控制。
- PPS 损失比简化的 SPPS 在多重指令场景下提供更解耦的潜在空间，实现更独立的编辑方向控制。
---

# SliderEdit: Continuous Image Editing with Fine-Grained Instruction Control

> [!tip] 核心洞察
> 通过 Partial Prompt Suppression (PPS) 损失训练一个轻量级选择式 Token LoRA，使其学会“中和”特定指令的视觉效应；训练后该适配器即成为一条连续滑块，可通过缩放因子实现从完全抑制到完全应用的平滑过渡，为指令级图像编辑提供全局可训练的、解耦的连续控制框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | SliderEdit：具有细粒度指令控制的连续图像编辑框架 |
| 英文题名 | SliderEdit: Continuous Image Editing with Fine-Grained Instruction Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.09715) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SliderEdit (with STLoRA and GSTLoRA adapters) |
| Dataset | Facial Editing Benchmark, Multi-instruction Editing |

> [!tip] 效果简介
> - Facial Editing Benchmark (γ=1, 15 strength steps) 上，Continuity (CLIP score ↑) 0.2998 (GSTLoRA) vs 0.1993 (Explicit CFG) (+0.1005)。
> - Facial Editing Benchmark (γ=1) 上，Identity Preservation (ID ↓, ArcFace cosine distance) 0.2550 (GSTLoRA) vs 0.3415 (Explicit CFG) (-0.0865)。
> - Multi-instruction Editing (γ=2, FLUX-Kontext base) 上，Continuity Avg (↑) 0.2409 (STLoRA) vs N/A (其他方法无法实现逐指令独立控制)。

## 概述

**问题瓶颈**：现有指令式图像编辑模型（如 FLUX-Kontext、Qwen-Image-Edit）以全有或全无的方式施加每条指令，用户无法独立且连续地调节单条指令的编辑强度，导致交互控制粗糙、可解释性不足。

**核心洞察与因果机制**：多模态扩散 Transformer（MMDiT）中每条指令对应的中间 token 嵌入是高度局部化的语义载体。通过引入低秩适配器（STLoRA/GSTLoRA）选择性抑制目标指令 token 的表示，并平滑缩放适配器权重，即可实现对单条指令编辑效果的连续调制。

**方法定位**：SliderEdit 提出 Partial Prompt Suppression (PPS) 损失，训练一个轻量级选择性 Token LoRA 学会“中和”特定指令的视觉效应。训练后，该适配器成为一条连续滑块，通过缩放因子实现从完全抑制到完全应用的平滑过渡，为指令级图像编辑提供全局可训练的、解耦的连续控制框架。

**主要结果**：
- **单指令编辑**：GSTLoRA 在连续性（CLIP score 0.2998 vs. Explicit CFG 0.1993）和身份保持（ID distance 0.2550 vs. 0.3415）上均显著优于显式/隐式无分类器引导基线（Table 1）。
- **多指令编辑**：STLoRA 在 2–3 条指令场景中产生连续、解耦的编辑空间（Continuity Avg: FLUX-Kontext 0.2409, Qwen-Image-Edit 0.4345），而所有基线方法均无法实现逐指令独立控制（Table 2）。
- **训练目标消融**：PPS 损失在多重指令场景下产生比简化版 SPPS 更解耦的潜在空间，提供更独立的编辑方向控制（Figure 12）。

**方法谱系与知识库定位**：SliderEdit 建立在 FLUX-Kontext（Black Forest Labs, 2024）和 Qwen-Image-Edit 等指令式编辑模型之上，通过冻结基础模型、仅训练低秩适配器的方式，将固定强度编辑模型转化为连续可控框架。与文本到图像的属性控制方法（如 Concept Slider、Continuous Attribute Control）不同，SliderEdit 直接面向真实图像编辑任务，避免了反演适配带来的性能损失。其核心贡献在于首次为指令式图像编辑引入细粒度、解耦的连续强度控制机制。

## 背景与动机

### 指令式图像编辑的现状与困境

以 **FLUX-Kontext**（Black Forest Labs, 2024）和 **Qwen-Image-Edit** 为代表的指令式图像编辑模型，已能根据自然语言指令对真实图像进行高质量的局部或全局修改。这些模型普遍采用多模态扩散 Transformer（MM-DiT）架构，将图像潜在 token 与文本指令 token 联合处理，通过流匹配或扩散目标学习编辑映射。然而，其控制范式存在一个根本性局限：**每条指令的编辑强度只能以“全有或全无”的方式施加**——用户要么接受模型对指令的完整诠释，要么完全不执行该指令，无法独立且连续地调节单条指令的编辑强度。

这一“二进制”控制模式带来了两个层面的问题：

1.  **缺乏精细控制**：用户无法在“轻微微笑”与“灿烂笑容”之间平滑过渡，只能得到模型默认的单一强度输出。
2.  **无法解耦多指令**：当提示包含多条指令（如“添加胡子”且“改变发型”）时，现有方法无法让用户独立调节每条指令的强度，导致编辑空间坍塌为不可分解的单一维度。

### 现有可控编辑方法的缺口

在文本到图像（T2I）生成领域，已有工作探索了属性的连续控制。**Concept Slider** 和 **Continuous Attribute Control**（Baumann et al.）等方法通过反演技术将 T2I 模型中的概念滑块适配到真实图像编辑场景，但性能有限——这些方法并非为指令式编辑原生设计，反演过程引入的误差导致编辑质量下降和身份漂移（见 Figure 13）。

在指令式编辑模型内部，**隐式无分类器引导（Implicit CFG）** 仅能通过改变 FLUX-Kontext 内部蒸馏的引导尺度微弱地调节编辑强度，控制范围极窄且不连续。**显式无分类器引导（Explicit CFG）** 虽然可以通过外部引导尺度 $w$ 实现一定程度的连续控制，但存在两个致命缺陷：（1）无法解耦多条指令的独立控制——引导尺度是全局的，作用于所有指令；（2）高引导尺度下身份漂移严重，编辑轨迹呈现突变而非平滑过渡（见 Table 1，Explicit CFG 的身份保持指标 ID 为 0.3415，显著劣于 GSTLoRA 的 0.2550）。

### 核心动机与关键观察

本文的核心动机在于填补上述缺口：**为指令式图像编辑首次引入细粒度、解耦的连续控制框架**，使用户能够像操作滑块一样独立调节每条指令的编辑强度。

实现这一目标的关键观察来自对 MM-DiT 架构内部表示的分析（Figure 2）：**每条指令对应的中间 token 嵌入是高度局部化的语义载体**——在指令 token 与空 token 嵌入之间进行插值，即可产生中间编辑强度。这表明，通过直接操纵目标指令 token 的表示，而非依赖全局引导信号，有可能实现指令级的独立控制。

基于这一洞察，SliderEdit 提出了一种轻量级、可训练的连续控制范式：通过 **Partial Prompt Suppression（PPS）** 损失训练低秩适配器（LoRA），使其学会“中和”特定指令的视觉效应；训练完成后，该适配器即成为一条连续滑块——通过缩放适配器权重，实现从完全抑制到完全应用的平滑过渡，且每条指令拥有独立的控制维度。

## 核心创新

SliderEdit 的核心创新在于为指令式图像编辑首次引入**细粒度、可解耦的连续强度控制**。现有指令编辑模型（如 **FLUX-Kontext**（Black Forest Labs, 2024）、**Qwen-Image-Edit**）以固定的、全有或全无的方式施加每条指令，用户无法独立调节单条指令的编辑强度。SliderEdit 通过三个相互耦合的机制性创新——**选择式 Token LoRA**、**部分提示抑制损失**与**滑块缩放推理**——将冻结的基础编辑模型转化为一个支持逐指令连续调制的框架。

### 关键机制创新

**1. 选择式 Token LoRA（STLoRA/GSTLoRA）—— 指令级语义载体的定向调制**

核心洞察在于：MM-DiT 中每条指令对应的中间 token 嵌入是高度局部化的语义载体。SliderEdit 在冻结基础模型的特定线性层引入可训练低秩矩阵 $\Delta W = BA$，并选择性地将其作用于目标指令 token。对于 STLoRA，更新仅应用于被抑制指令的 token 嵌入：

$$z_{\mathrm{target}}' = (W^{\ell} + \Delta W^{\ell}) z_{\mathrm{target}}, \quad z_{\mathrm{others}}' = W^{\ell} z_{\mathrm{others}}$$

这一选择性机制是**多指令解耦控制的基础**：每条指令拥有独立的适配器，互不干扰。GSTLoRA 则将 LoRA 更新全局应用于所有 token，在单指令场景下提供更强的连续性。

**2. 部分提示抑制损失（PPS）—— 学会“中和”特定指令的视觉效应**

适配器通过 PPS 损失训练，其目标是使带适配器的模型在完整指令下的去噪输出，与冻结基础模型在移除目标指令后的去噪输出一致：

$$\mathcal{L}_{\mathtt{PPS}} = \| \epsilon_{M_{\theta}(\mathcal{P}_i)}(Z, X_{\mathrm{orig}}, \mathcal{P}) - \epsilon(Z, X_{\mathrm{orig}}, \mathcal{P} - \{\mathcal{P}_i\}) \|$$

这一损失函数教会适配器“中和”目标指令 $\mathcal{P}_i$ 的视觉效应，而无需成对的编辑强度标注数据。消融实验证实，在多指令场景下，PPS 比简化的 SPPS 变体产生更解耦的潜在空间，提供更独立的编辑方向控制（Figure 12）。

**3. 滑块缩放推理 —— 从完全抑制到完全应用的平滑过渡**

训练完成后，适配器即成为一条连续滑块。推理时通过单个标量 $\alpha$ 缩放 LoRA 更新量，实现从完全抑制（$\alpha=1$，即 $\beta=0$）到完全应用（$\alpha=0$，即 $\beta=1$）乃至夸张效果（$\alpha<0$）的平滑过渡：

$$\alpha = 1 - \beta$$

每条指令拥有独立的 $\alpha_i$，用户可独立调节各指令强度，形成 $\gamma$ 维连续编辑空间。

### 与基线方法的本质差异

| 控制维度 | **Explicit CFG** | **Implicit CFG** | **Concept Slider** | **SliderEdit** |
|---------|------------------|------------------|-------------------|----------------|
| 控制粒度 | 全局单一尺度 | 全局单一尺度 | 属性级（需反演适配） | 指令级独立控制 |
| 多指令解耦 | 不支持 | 不支持 | 不支持 | 支持（STLoRA） |
| 连续性 | 突变式过渡 | 突变式过渡 | 有限 | 平滑连续 |
| 身份保持 | 漂移显著 | 漂移显著 | 在真实图像上表现差 | 显著优于 CFG 基线 |

定量结果表明，GSTLoRA 在单指令编辑中实现了最高的连续性（CLIP continuity 0.2998 vs Explicit CFG 0.1993）和最低的身份漂移（ID distance 0.2550 vs 0.3415），而 STLoRA 是唯一能在 2-3 条指令场景下实现逐指令独立连续控制的方法（Table 1, Table 2）。

### 设计哲学

SliderEdit 的轻量性是其创新的重要维度：仅需在冻结基础模型上训练少量低秩矩阵（1k–8k 样本，1,000 次迭代），即可将任意指令式编辑模型转化为连续可控框架。这种“即插即用”的设计避免了对大规模重训练或复杂反演技术的依赖，同时保持了基础模型的编辑质量。

## 整体框架

SliderEdit 的目标是在现有指令式图像编辑模型之上，构建一个轻量级、可训练的连续控制框架，使用户能够对每条编辑指令的强度进行独立、平滑的调节。其核心设计思想是：**多模态扩散 Transformer（MMDiT）中每条指令对应的中间 token 嵌入是高度局部化的语义载体，通过选择性抑制目标指令 token 的表示，并平滑缩放抑制强度，即可实现从完全抑制到完全应用的连续编辑轨迹**。

### Pipeline 总览

整个框架由四个核心模块串联构成，如图 Figure 3 所示：

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/005_Figure_3.jpg]]
*Figure 3: Overview of the SliderEdit training pipeline. Learnable low-rank matrices are applied to the intermediate token embeddings corresponding to the target edit instruction. These adapters are trained using the Partial Prompt Suppression (PPS) loss, which encourages the model to suppress or neutralize the visual effect of the selected instruction tokens*

1. **冻结的 MM-DiT 骨干网络**：SliderEdit 以预训练的指令式图像编辑模型（如 **FLUX-Kontext**，Black Forest Labs, 2024；或 **Qwen-Image-Edit**）为基础，保持其全部参数冻结，确保基础编辑能力不被破坏。

2. **指令 Token 定位**：给定一个包含 $K$ 条指令的多指令提示 $\mathcal{P} = \{\mathcal{P}_1, \dots, \mathcal{P}_K\}$，系统根据指令边界在文本 token 序列中定位属于目标指令 $\mathcal{P}_i$ 的 token 索引集合。这一步是实现“逐指令独立控制”的前提。

3. **选择性 Token LoRA（STLoRA / GSTLoRA）**：在 MM-DiT 的特定线性层中插入可训练的低秩矩阵 $\Delta W^\ell = B^\ell A^\ell$。对于 **STLoRA**（面向多指令场景），低秩更新仅作用于目标指令对应的 token 嵌入：
   $$z_{\mathrm{target}}' = (W^{\ell} + \Delta W^{\ell}) \, z_{\mathrm{target}}, \quad z_{\mathrm{others}}' = W^{\ell} \, z_{\mathrm{others}}$$
   这种选择性应用机制从结构上保证了对非目标指令的解耦。对于 **GSTLoRA**（面向单指令场景），LoRA 更新则全局作用于所有 token 嵌入，以更充分的容量学习抑制单一指令的视觉效应。

4. **部分提示抑制（PPS）训练目标**：适配器通过 PPS 损失进行训练，其核心思想是迫使带适配器的模型在完整提示下去噪，输出与冻结基础模型在移除目标指令 $\mathcal{P}_i$ 后的去噪结果一致：
   $$\mathcal{L}_{\mathtt{PPS}} = \| \epsilon_{M_{\theta}(\mathcal{P}_i)}(Z, X_{\mathrm{orig}}, \mathcal{P}) - \epsilon(Z, X_{\mathrm{orig}}, \mathcal{P} - \{\mathcal{P}_i\}) \|$$
   这一目标使适配器学会“中和”目标指令的视觉效应，而无需成对的编辑强度标注数据。训练仅需从 GPT-Image-Edit 数据集中采样 1k–8k 样本，迭代约 1000 步即可收敛。

### 推理阶段的滑块控制

训练完成后，STLoRA/GSTLoRA 适配器即成为一个连续滑块。推理时，通过一个标量缩放因子 $\alpha \in [\alpha_{\min}, \alpha_{\max}]$ 统一缩放所有层的 LoRA 更新量 $\alpha \Delta W^\ell$，其中 $\alpha = 1 - \beta$，$\beta \in [0,1]$ 为指令保留因子：
- $\alpha = 1$（$\beta = 0$）：完全抑制目标指令，等效于该指令被移除；
- $\alpha = 0$（$\beta = 1$）：完全应用目标指令，等效于基础模型的原始编辑；
- $\alpha < 0$：夸张模式，反向增强编辑效果；
- 中间 $\alpha$ 值产生平滑的连续过渡。

在多指令场景下，每条指令拥有独立的缩放因子 $\alpha_i$，用户可独立调节各条指令的强度，从而在 $\gamma$ 维编辑空间中自由导航。这一设计将指令级图像编辑转化为一个**全局可训练的、解耦的连续控制问题**，而无需对基础模型架构做任何侵入式修改。

### 补充图表

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/002_Figure_1.jpg]]
*Figure 1: SliderEdit produces continuous edit trajectories in state-of-the-art instruction-based image editing models. Our method provides fine-grained and disentangled control over the intensity of edit attributes described in an instruction, allowing continuous transitions between editing strengths. Despite its effectiveness, SliderEdit is extremely lightweight and can be trained efficiently to transform a state-of-the-art instruction-based image editing model into a continuously controllable editing framework*

## 核心模块与公式推导

### 问题形式化

给定原始图像 $X_{\mathrm{orig}}$ 和多指令编辑提示 $\mathcal{P} = \{\mathcal{P}_1, \dots, \mathcal{P}_K\}$，其中每条 $\mathcal{P}_i$ 描述一个独立的编辑操作，SliderEdit 的目标是为每条指令 $\mathcal{P}_i$ 引入一个连续的缩放因子 $\beta_i \in [0,1]$，使得用户能够独立且平滑地调节每条指令的编辑强度——$\beta_i=0$ 表示完全抑制该指令，$\beta_i=1$ 表示完全应用该指令。

### 核心洞察：指令 Token 嵌入的局部语义承载

方法设计的起点来自一个关键观察（Figure 2）：在多模态扩散 Transformer（MMDiT）的中间层，直接对目标指令对应的 token 嵌入与空填充 token 嵌入进行线性插值，即可产生中间编辑强度。这表明**每条指令对应的中间 token 嵌入是高度局部化的语义载体**，为后续的适配器设计提供了理论依据。

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/004_Figure_2.jpg]]
*Figure 2: Instruction-token embedding interpolation for strength control. Interpolating between instruction and nulltoken embeddings produces intermediate edit strengths, demonstrating the potential for achieving fine-grained control through direct manipulation of intermediate instruction embeddings*

### 核心模块一：Selective Token LoRA (STLoRA)

STLoRA 是实现指令级解耦控制的核心适配器模块。其关键设计在于**选择性**：低秩更新仅作用于被抑制指令 $\mathcal{P}_i$ 对应的 token 嵌入，而其余 token 保持原始表示不变。

对于 MMDiT 中第 $\ell$ 层的线性投影矩阵 $W^{\ell}$，引入可训练的低秩分解 $\Delta W^{\ell} = B^{\ell}A^{\ell}$，更新规则为：

$$z_{\mathrm{target}}' = (W^{\ell} + \Delta W^{\ell})\, z_{\mathrm{target}}, \quad z_{\mathrm{others}}' = W^{\ell}\, z_{\mathrm{others}}$$

其中 $z_{\mathrm{target}}$ 为属于目标指令 $\mathcal{P}_i$ 的 token 嵌入，$z_{\mathrm{others}}$ 为所有其他 token（包括其他指令 token 和图像 latent token）的嵌入。这一选择性机制确保了每条指令的适配器仅调制自身的语义通道，是实现多指令解耦控制的架构基础。

**GSTLoRA 变体**：在单指令编辑场景下，STLoRA 可简化为 Globally Selective Token LoRA（GSTLoRA），即 LoRA 更新全局应用于所有 token 嵌入（文本和图像），不再区分目标与非目标 token。GSTLoRA 训练更简单，在单指令连续编辑中表现最优。

### 核心模块二：Partial Prompt Suppression (PPS) 损失

PPS 损失是训练 STLoRA/GSTLoRA 适配器的核心目标函数。其设计思想是：**迫使带适配器的模型在完整提示下去噪，与冻结的基础模型在移除目标指令后的去噪输出一致**，从而让适配器学会“中和”该指令的视觉效应。

$$\mathcal{L}_{\mathtt{PPS}} = \left\| \epsilon_{M_{\theta}(\mathcal{P}_i)}(Z, X_{\mathrm{orig}}, \mathcal{P}) - \epsilon(Z, X_{\mathrm{orig}}, \mathcal{P} - \{\mathcal{P}_i\}) \right\|$$

其中：
- $\epsilon_{M_{\theta}(\mathcal{P}_i)}$ 表示加载了针对指令 $\mathcal{P}_i$ 的 STLoRA 适配器的去噪模型；
- $\epsilon$ 表示冻结的基础模型；
- $Z$ 为当前带噪 latent；
- $\mathcal{P}$ 为完整的多指令提示；
- $\mathcal{P} - \{\mathcal{P}_i\}$ 表示从提示中移除目标指令 $\mathcal{P}_i$。

训练时仅更新 LoRA 参数，基础模型完全冻结。该损失使适配器学习到：当完整指令存在时，通过调制目标 token 的表示来抵消 $\mathcal{P}_i$ 的编辑效应，使其等价于该指令被删除时的模型行为。

**简化变体 SPPS**：将整个提示视为单条指令，迫使适配器将提示 $\mathcal{P}_1$ 的效果中和为空提示 $\emptyset$ 下的输出：

$$\mathcal{L}_{\mathtt{SPPS}} = \left\| \epsilon_{M_{\theta}(\mathcal{P}_1)}(Z, X_{\mathrm{orig}}, \mathcal{P}_1) - \epsilon(Z, X_{\mathrm{orig}}, \emptyset) \right\|$$

SPPS 训练更简单，在单指令场景下效果良好，但在多指令编辑中解耦性弱于 PPS（Figure 12 验证）。

### 推理时的连续滑块机制

训练完成后，STLoRA/GSTLoRA 适配器即成为一条连续滑块。推理时引入缩放因子 $\alpha$，控制 LoRA 更新量的强度：

$$\alpha = 1 - \beta$$

其中 $\beta$ 为用户期望的指令保留程度。推理时对每层应用缩放后的更新 $\alpha \Delta W^{\ell}$：
- $\alpha = 1$（$\beta = 0$）：完全抑制，适配器以完整强度中和指令效应；
- $\alpha = 0$（$\beta = 1$）：完全应用，适配器不产生任何调制，等价于原始基础模型；
- $\alpha < 0$（$\beta > 1$）：夸张模式，适配器反向增强指令效应，产生超出原始编辑强度的效果。

在多指令场景下，每条指令 $\mathcal{P}_i$ 拥有独立的缩放因子 $\alpha_i$，生成 $\gamma$ 维连续编辑空间，实现真正解耦的逐指令强度控制。

### 训练效率设计

适配器仅作用于 MMDiT 中所有 transformer block 的一个子集，训练数据仅使用 GPT-Image-Edit 数据集的 1k–8k 子样本，STLoRA 模型训练约 1,000 次迭代即可收敛。这一轻量级设计使得将任意指令式编辑模型转化为连续可控框架的成本极低。

### 补充图表

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/012_Figure_8.jpg]]
*Figure 8: Simplified Partial Prompt Suppression (SPPS). SPPS applies the same suppression objective as PPS but treats the entire edit prompt as a single instruction. During training, a second (bottom-row) forward pass is performed to obtain a neutralized image—either using an empty prompt*

## 实验与分析

### 核心定量结果

SliderEdit 在两个主流指令式图像编辑基础模型（**FLUX-Kontext** 与 **Qwen-Image-Edit**）上均实现了连续、解耦的指令强度控制，这是现有方法无法达成的能力。以下从单指令与多指令两个维度分析其性能优势。

#### 单指令编辑：连续性与身份保真度的双重提升

在单指令编辑场景（γ=1，15 个强度步长）中，**GSTLoRA** 在所有连续性指标上均显著优于显式与隐式 CFG 基线。以 CLIP 分数衡量的连续性为例，GSTLoRA 达到 0.2998，而显式 CFG 仅为 0.1993（提升 +0.1005）。更重要的是，GSTLoRA 在身份保持上同样表现最佳：ArcFace 余弦距离低至 0.2550，显式 CFG 则为 0.3415（降低 0.0865），表明滑块机制在实现平滑编辑轨迹的同时有效抑制了身份漂移。

隐式 CFG 虽然通过调节内部引导尺度可产生微弱的强度变化，但其编辑轨迹呈现突变式跳转，且身份漂移更为严重。显式 CFG 在连续性上优于隐式 CFG，但在高引导尺度下身份退化明显。GSTLoRA 的优势根源在于其训练目标直接优化了“中和指令”的能力，而非依赖推理时的引导尺度外推。

#### 多指令编辑：唯一具备逐指令独立控制能力的方法

在多指令编辑场景（2-3 条指令）中，**STLoRA** 是唯一能够实现逐指令独立连续控制的方法。所有基线方法（包括显式/隐式 CFG 及 Concept Slider 等文本到图像适配方法）均无法构建解耦的多维编辑空间。定量结果（Table 2）显示，STLoRA 在 FLUX-Kontext 基础上于 2 指令与 3 指令设置下分别取得 0.2409 和 0.3691 的平均连续性分数；在 Qwen-Image-Edit 基础上则达到 0.2813 和 0.4345。值得注意的是，Qwen 在多指令场景下连续性更强，而 FLUX 在身份保持上更优，这反映了两类基础模型在表示空间上的固有差异。

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/010_Table_2.jpg]]
*Table 2: Quantitative results for multi-instruction edits. Both models show comparable performance in continuity. FLUX better preserves identity, while Qwen performs better in extrapolation*

### 消融分析：PPS 与 SPPS 的解耦性差异

训练目标的消融实验揭示了 **PPS（Partial Prompt Suppression）** 与 **SPPS（Simplified PPS）** 的关键差异。SPPS 将整个提示视为单条指令，迫使适配器将其效果中和为空提示输出，训练更为简单。PPS 则针对每条目标指令单独训练适配器，要求完整提示下的去噪输出与移除该指令后一致。

在多指令编辑中，PPS 产生的潜在空间明显更解耦、插值轨迹更平滑（Figure 12 定性对比），允许对每条指令方向进行更精细的独立控制。SPPS 在单指令场景下效果相当，但在多指令设置中，由于缺乏对指令间交互的显式建模，其编辑方向会出现一定程度的耦合。这一结果表明，**逐指令的抑制训练是获得解耦连续控制的关键设计选择**。

### 失败模式与局限性

尽管 SliderEdit 在连续控制上表现突出，仍存在以下值得关注的局限：

1. **属性纠缠未彻底消除**：基础模型自身的属性耦合（如修改肤色可能无意中影响头发颜色或光照）会在编辑中传递。这不是滑块方法引入的新问题，而是生成模型固有的表示纠缠。SliderEdit 未加剧此问题，但也未提供显式的解耦机制来消除它。

2. **训练数据规模有限**：所有实验仅使用 GPT-Image-Edit 数据集的 1k–8k 子集进行训练（1,000 次迭代）。对于复杂、未见过的组合指令，方法的泛化能力尚未经过大规模严格测试，极端长尾编辑场景的表现需要进一步验证。

3. **适配器作用范围未充分探索**：当前 LoRA 适配器仅作用于部分 Transformer 块，且未在所有扩散时间步上训练。这些效率设计选择的完整影响——包括是否可通过进一步缩减作用范围来降低计算开销而不显著损害控制质量——仍有待系统调查。

### 与基线的定性对比

与 Concept Slider 及 Continuous Attribute Control 等文本到图像连续控制方法的对比（Figure 13）显示，后者在真实图像编辑上表现较差。这些方法原本设计用于文本到图像生成，需通过反演技术适配到图像编辑任务，间接的适配路径导致编辑质量与控制精度均不及 SliderEdit 的原生指令级适配方案。

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/017_Figure_13.jpg]]
*Figure 13: Qualitative Comparison with Baselines. While SliderEdit (GSTLoRA variant here) and Explicit Guidance produce highquality edits, Concept-Slider and Continuous Attribute Control perform poorly on real image editing, as they are primarily designed for text-to-image generation and rely on indirect inversion-based adaptation*

### 补充图表

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/009_Table_1.jpg]]
*Table 1: Quantitative results for single-instruction edits (γ = 1). SliderEdit yields smoother trajectories and better identity preservation*

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative and quantitative comparison of GST-LoRA with CFG baselines. GSTLoRA shows smooth edit trajectories with gradual similarity changes, unlike Implicit and Explicit CFG, which exhibit abrupt transitions and greater identity drift*

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/015_Figure_10.jpg]]
*Figure 10: Qualitative results of STLoRA on a 3-instruction edit. The model demonstrates smooth and continuous control over the strength of each instruction in a disentangled manner*

![[assets/figures/papers/paper_list_l2029_https_arxiv_org_abs_2511_09715/figures/007_Figure_5.jpg]]
*Figure 5: Controllable zero-shot multi-subject personalization with STLoRA. STLoRA enables smooth adjustment of each instruction’s strength to generate coherent, evolving image sequences, supporting story-like visual editing. (Best viewed from top-left to top-right, then bottom-right to bottom-left)*

## 方法谱系与知识库定位

### 1. 问题脉络与基线关系

SliderEdit 锚定在**指令式图像编辑**（instruction-based image editing）这一新兴范式上。该范式以 **FLUX-Kontext**（Black Forest Labs, 2024）和 **Qwen-Image-Edit** 为代表，允许用户通过自然语言指令直接描述编辑意图，模型在统一的多模态 DiT（MMDiT）架构中联合处理图像和文本 token，一次性执行编辑。然而，现有模型存在一个关键瓶颈：每条指令以“全有或全无”的固定强度施加，用户无法独立、连续地调节单条指令的编辑强度，导致交互控制的粒度粗糙且缺乏可解释性。

SliderEdit 的核心贡献在于将这一**离散的、全局耦合的编辑范式**转化为**连续的、逐指令解耦的编辑框架**。其方法定位与以下几类基线形成清晰对比：

- **显式无分类器引导（Explicit CFG）**：FLUX-Kontext 等模型可通过外部引导尺度 $w$ 对单条指令进行强度调节。该方法虽能产生连续轨迹，但存在两个根本缺陷：(1) 无法解耦多条指令——所有指令共享同一个全局引导尺度；(2) 高引导尺度下引起严重的身份漂移（identity drift）。SliderEdit 的 GSTLoRA 在单指令场景下连续性提升约 50%（CLIP continuity: 0.2998 vs. 0.1993），身份保持显著改善（ArcFace 余弦距离: 0.2550 vs. 0.3415），且这一优势在多指令场景下因 CFG 完全无法独立控制而更加突出。

- **隐式无分类器引导（Implicit CFG）**：FLUX-Kontext 内部蒸馏的隐式引导仅能通过改变内部引导尺度微弱控制编辑强度，编辑轨迹呈现突变而非平滑过渡，无法提供有意义的连续控制。

- **文本到图像的属性连续控制方法**：**Concept Slider** 和 **Continuous Attribute Control**（Baumann et al.）专为文本到图像生成设计，通过反演技术（inversion）适配到真实图像编辑。然而，这种间接适配在真实图像编辑上表现较差，编辑质量明显低于 SliderEdit 和 Explicit CFG（见 Figure 13）。SliderEdit 直接在指令式编辑模型的 token 嵌入空间上操作，无需反演，方法更直接、编辑质量更高。

### 2. 方法谱系中的技术定位

SliderEdit 的技术路线位于以下几条研究脉络的交汇点：

**（1）低秩适配（LoRA）用于生成控制。** LoRA 已被广泛应用于扩散模型的可控生成，但既往工作多聚焦于注入新概念或风格。SliderEdit 的创新在于将 LoRA 定位为**指令效应的“中和器”**：通过 Partial Prompt Suppression（PPS）损失训练，适配器学会抑制特定指令 token 的视觉效应，而非注入新信息。训练后，该适配器即成为一条连续滑块——缩放因子 $\alpha \in [\alpha_{\min}, \alpha_{\max}]$ 从完全抑制（$\alpha=1$）平滑过渡到完全应用（$\alpha=0$），甚至支持夸张效果（$\alpha < 0$）。

**（2）token 级表示干预。** 论文发现 MMDiT 中每条指令对应的中间 token 嵌入是高度局部化的语义载体（Figure 2 的插值实验验证了这一点）。基于此洞察，STLoRA 选择性地仅对目标指令 token 应用低秩更新，保持其他 token 的原始表示不变，这是实现多指令解耦控制的关键设计。与之对比，GSTLoRA 对所有 token 全局应用更新，在单指令场景下连续性更优，但牺牲了多指令的解耦能力。

**（3）训练目标的重新定义。** PPS 损失的核心思想是迫使带适配器的模型在完整指令下的去噪输出，与冻结基础模型在移除目标指令后的去噪输出一致。这一目标本质上是在学习一个“减法”操作——从完整指令的编辑效应中减去目标指令的贡献。简化版 SPPS 将整个提示视为单条指令，迫使适配器将编辑效应中和为空提示下的输出，训练更简单但解耦性弱于 PPS（Figure 12 提供了定性对比证据）。

### 3. 适用边界与局限

**适用场景：**
- SliderEdit 在单指令和多指令（2–3 条）编辑场景下均表现出色，支持从面部属性编辑到全局风格转换的多种编辑类型。
- STLoRA 支持零样本多主体个性化编辑（Figure 5），可生成故事式的连续图像序列。
- 方法极其轻量：仅需 1k–8k 训练样本，1,000 次迭代即可完成训练，适配器参数量远小于基础模型。

**已知局限：**
- **属性纠缠未被彻底消除。** 基础模型自身的属性耦合（如修改肤色可能无意中影响头发颜色或光照）会在编辑中传递。这是生成模型固有的属性耦合问题，SliderEdit 未引入额外纠缠，但也未能完全消除。
- **训练数据规模有限。** 仅使用 GPT-Image-Edit 数据集的 1k–8k 子集进行训练，复杂、未见过的组合指令的泛化能力未经过大规模严格测试。
- **效率设计选择尚未充分探索。** LoRA 适配器仅作用于所有 transformer 块的子集，训练时间步的完全利用也未被充分调查，这些设计选择对控制质量和计算开销的平衡尚待全面研究。

### 4. 开放问题与后续方向

- **计算效率的进一步优化。** 是否可以通过仅训练部分 transformer block 和部分扩散时间步来进一步降低计算开销，而不显著影响控制质量？
- **跨模态扩展。** 滑块机制能否扩展到视频编辑、3D 场景编辑等更具挑战性的生成任务中？这些任务对时序一致性和空间一致性的要求更高。
- **极长多指令提示的鲁棒性。** 在指令数超过 5 条的极端场景下，STLoRA 的解耦能力和连续性是否仍能保持？PPS 损失在这种高维编辑空间中的优化难度值得深入研究。
- **与其他可控编辑技术的融合。** SliderEdit 的连续滑块机制与基于注意力控制、跨注意力引导等方法是否可互补，形成更强大的编辑控制工具箱，是一个开放且有价值的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/SliderEdit_Continuous_Image_Editing_with_Fine_Grained_Instruction_Control.pdf]]

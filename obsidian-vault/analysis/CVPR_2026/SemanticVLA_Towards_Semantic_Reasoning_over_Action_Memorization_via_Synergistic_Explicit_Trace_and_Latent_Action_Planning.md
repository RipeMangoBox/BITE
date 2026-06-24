---
title: "SemanticVLA: Towards Semantic Reasoning over Action Memorization via Synergistic Explicit Trace and Latent Action Planning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_Trace_and_Latent_Action_Planning.pdf
project_link: null
code_link: null
aliases:
- SemanticVLA
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用VLM原生语言接口生成可解释的显式2D空间轨迹（坐标序列）作为中间规划，既重用了其预训练的空间对齐能力，又为下游的潜动作学习提供了时间对齐、语言无关的辅助语义监督。
primary_logic: 显式轨迹推理与隐式潜动作令牌在功能上互补：轨迹提供直观的几何引导但易受坐标精度影响，潜动作令牌融合视觉观察以补偿轨迹的数值不稳定性。通过双路径协同，VLM的推理真正服务于任务规划，而非停留在特征融合层面。
claims:
- SemanticVLA在LIBERO上达到97.0%平均成功率，在SimplerEnv上达到65.1%，显著优于所有基线。
- 在指令改写测试中，SemanticVLA的性能稳定性远优于基线方法。
- 显式轨迹预测自然地与VLM的空间对齐能力吻合，为潜动作学习提供辅助监督。
- LIBERO 上 Average success rate (%) = 97.0
---

# SemanticVLA: Towards Semantic Reasoning over Action Memorization via Synergistic Explicit Trace and Latent Action Planning

> [!tip] 核心洞察
> 显式轨迹推理与隐式潜动作令牌在功能上互补：轨迹提供直观的几何引导但易受坐标精度影响，潜动作令牌融合视觉观察以补偿轨迹的数值不稳定性。通过双路径协同，VLM的推理真正服务于任务规划，而非停留在特征融合层面。

| 字段 | 内容 |
|------|------|
| 中文题名 | SemanticVLA：通过协同显式轨迹与潜动作规划实现超越动作记忆的语义推理 |
| 英文题名 | SemanticVLA: Towards Semantic Reasoning over Action Memorization via Synergistic Explicit Trace and Latent Action Planning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ni_SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SemanticVLA |
| Dataset | LIBERO, SimplerEnv WidowX, Real-world long-horizon & reasoning |

> [!tip] 效果简介
> - LIBERO 上，Average success rate (%) 97.0 vs 95.2 (UniVLA, second best) (+1.8)。
> - SimplerEnv WidowX 上，Success rate (%) 65.1 vs 31.3 (UniVLA, second best) (+33.8)。
> - Real-world long-horizon & reasoning 上，Average success rate (%) 62.3。

## 概述

当前视觉-语言-动作（VLA）模型面临一个核心瓶颈：VLM与动作专家之间通过不透明的潜嵌入通信，这些嵌入缺乏语义可解释性，导致指导信号模糊且不稳定。同时，仅靠动作损失的反向传播会破坏VLM的预训练语义能力，使模型退化为记忆动作模式的参数重融合编码器，而非进行组合推理——这在指令改写和推理密集型任务中尤为突出。

**SemanticVLA** 通过协同**显式轨迹推理**与**隐式潜动作规划**的双路径架构回应这一挑战。其核心洞察在于：利用VLM原生语言接口生成可解释的2D空间轨迹（坐标序列）作为中间规划，既重用了VLM预训练的空间对齐能力，又为下游潜动作学习提供了时间对齐、语言无关的辅助语义监督。显式轨迹提供直观的几何引导，隐式潜动作令牌则融合视觉观察以补偿轨迹的数值不稳定性，二者在功能上互补，使VLM的推理真正服务于任务规划。

方法上，SemanticVLA采用三阶段训练管线：（1）基于轨迹引导的潜令牌预训练，先学几何锚点再对齐视觉；（2）VLM联合预测轨迹坐标与潜令牌索引，建立语义对应；（3）弱正则下微调流匹配动作解码器。实验表明，SemanticVLA在LIBERO上达到97.0%平均成功率，在SimplerEnv WidowX上达到65.1%，显著优于UniVLA等基线；在指令改写测试中性能稳定性远超对比方法，真实世界长序列与推理任务上也展现出强泛化优势。

## 背景与动机

视觉-语言-动作（VLA）模型将视觉语言模型（VLM）的语义理解能力引入机器人操控，使机器人能够根据自然语言指令执行复杂任务。然而，当前VLA架构面临一个关键瓶颈：VLM与下游动作专家之间通过**不透明的潜嵌入（latent embeddings）**进行通信，这些嵌入缺乏语义可解释性，导致指导信号模糊且不稳定。更严重的是，仅依赖动作损失进行端到端反向传播会**破坏VLM预训练获得的语义能力**，使模型退化为记忆动作模式的参数重融合编码器，而非进行真正的组合推理——这正是现有方法在指令改写或推理密集型任务中性能大幅下降的根本原因。

针对上述问题，现有方法存在两类缺口。一类方法完全依赖潜动作令牌（如**UniVLA**将任务语言作为中间模态过滤视觉变化，**VQ-VLA**基于矢量量化构建动作分词器），但潜令牌的训练缺乏显式语义锚定，容易受语言变异性和视觉外观纠缠的影响。另一类方法尝试引入显式推理，如**MolmoAct**将轨迹预测作为辅助推理，**Magma**生成2D路点以条件化低层策略，但这些方法未能将显式空间推理与隐式动作表征有效协同，导致轨迹的几何引导与动作的视觉补偿彼此割裂。

本文的动机源于一个核心洞察：**显式轨迹推理与隐式潜动作令牌在功能上天然互补**。轨迹提供直观的几何引导，自然地与VLM预训练的空间对齐能力吻合，但易受坐标精度影响；潜动作令牌融合视觉观察，能够补偿轨迹的数值不稳定性，但缺乏可解释性。通过构建**双路径协同架构**，让VLM同时生成可解释的2D空间轨迹（坐标序列）和语义丰富的潜动作令牌，使VLM的推理真正服务于任务规划，而非停留在特征融合层面。为此，本文提出SemanticVLA，通过三阶段训练流程——轨迹引导的潜令牌预训练、VLM联合预测轨迹与潜令牌、弱正则下微调动作专家——实现显式推理与隐式规划的深度协同。

## 核心创新

SemanticVLA 的核心创新在于**将VLM的原生语言接口从“不透明特征通信”升级为“可解释的显式轨迹推理”**，并通过与潜动作令牌的协同双路径设计，解决了当前VLA架构中VLM语义能力被动作记忆所侵蚀的根本问题。

### 1. 瓶颈突破：从特征融合到语义推理

当前主流VLA（如 **OpenVLA** 与 **UniVLA**）的架构存在一个隐蔽但致命的缺陷：VLM与动作专家之间通过潜嵌入（latent embeddings）通信，这些嵌入缺乏语义可解释性，导致指导信号模糊且不稳定。更严重的是，仅依赖动作损失的反向传播会破坏VLM的预训练语义能力——模型逐渐退化为记忆动作模式的参数重融合编码器，而非进行组合推理。这正是VLA模型在指令改写或推理密集型任务中性能急剧下降的深层原因。

SemanticVLA 的突破点在于识别出**VLM的空间对齐能力是其预训练阶段天然具备、却未被充分利用的语义资产**。论文提出将2D空间轨迹（坐标序列）作为VLM的中间推理输出，这一设计选择具有三重优势：(1) 轨迹预测与VLM的原生语言接口和空间接地能力自然吻合；(2) 显式坐标序列为下游动作学习提供了时间对齐、语言无关的辅助语义监督；(3) 可解释的中间规划使VLM的推理真正服务于任务规划，而非停留在特征融合层面。

### 2. 关键机制变更（Changed Slots）

相较于基线方法，SemanticVLA 在三个核心设计槽上做出了根本性改变：

| 设计槽 | 基线方案 | SemanticVLA方案 | 机制优势 |
|--------|---------|----------------|---------|
| **VLM输出接口** | 不透明潜嵌入，缺乏语义可解释性 | 显式2D轨迹坐标序列（文本token）+ 潜动作令牌（离散codebook索引） | 轨迹提供直观几何引导，潜令牌融合视觉观察以补偿坐标数值不稳定性 |
| **训练流程** | 端到端微调（VLM + 动作解码器联合优化） | 三阶段训练：轨迹引导潜令牌预训练 → VLM联合预测轨迹与潜令牌 → 弱正则下微调动作专家 | 避免语言污染与VLM语义退化，确保几何基元与视觉特征的对齐 |
| **潜动作令牌学习监督** | 仅视觉重建或语言条件（存在语言变异性和外观纠缠） | 先纯轨迹几何重建（第一阶段），再融合视觉特征的双重重构（第二阶段） | 确保几何不变性与视觉对齐，使潜令牌同时具备空间语义和视觉语义 |

### 3. 双路径协同的互补逻辑

显式轨迹推理与隐式潜动作令牌并非简单叠加，而是在功能上形成精确互补：

- **轨迹路径**：通过VLM自回归生成归一化2D路点序列 $p(\tau \mid o_t, \ell_t) = \prod_{j=1}^L p(p_j \mid o_t, \ell_t, \tau_{<j})$，提供可解释的空间规划。但其性能受限于坐标预测的数值精度。
- **潜动作路径**：在轨迹条件下预测离散潜令牌序列 $p(q_{1:N} \mid o_t, \ell_t, \tau) = \prod_{i=1}^N p(q_i \mid o_t, \ell_t, \tau, q_{<i})$，融合视觉观察以补偿轨迹的数值不稳定性，同时将连续控制动作压缩为紧凑的视觉运动基元。

两路隐藏态共同条件化下游的流匹配动作解码器，实现从语义推理到连续控制的端到端衔接。消融实验证实了这一互补关系的必要性：移除显式轨迹推理后，潜预测准确率从93.6%降至85.6%，任务成功率从87.6%降至79.2%；仅使用轨迹推理（无潜动作令牌）的语言重述成功率为48%，而完整模型达到56%。

### 4. 与相关工作的本质差异

SemanticVLA 的显式轨迹推理与 **MolmoAct**（将轨迹预测作为辅助推理）和 **Magma**（生成2D路点条件化低层策略）存在根本区别：后两者将轨迹仅作为额外的推理输出或条件信号，而 SemanticVLA 通过两阶段VQ-VAE将轨迹几何基元注入潜动作令牌的学习过程——第一阶段从纯轨迹坐标学习稳定的几何锚点，第二阶段将这些锚点扎根于视觉观测——使得轨迹推理与潜动作规划形成双向信息流，而非简单的级联关系。

## 整体框架

SemanticVLA 的整体设计围绕一个核心矛盾展开：当前 VLA（视觉‑语言‑动作）模型中，VLM 与动作专家之间通过**不透明的潜嵌入**进行通信，这些嵌入缺乏语义可解释性，导致指导信号模糊且不稳定；同时，仅靠动作损失的反向传播会破坏 VLM 的预训练语义能力，使模型退化为记忆动作模式的参数重融合编码器，而非进行组合推理。SemanticVLA 的解决方案是引入一条**显式轨迹推理路径**，利用 VLM 原生语言接口生成可解释的 2D 空间坐标序列作为中间规划，从而为下游的潜动作学习提供时间对齐、语言无关的辅助语义监督。

### 双路径协同架构

SemanticVLA 的核心架构由两条互补的推理路径组成（见 Figure 3）：

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/003_Figure_3.jpg]]
*Figure 3: SemanticVLA Architecture Overview. Our dual-path framework synergistically combines explicit trace reasoning and implicit latent action planning. The VLM processes visual observations and language instructions to generate interpretable trace coordinates and latent action tokens, which are then fused to condition the flow matching action decoder for continuous robot control*

- **显式轨迹推理路径**：VLM 以自回归方式生成归一化的 2D 路点坐标序列，作为文本 token 直接输出。这些坐标序列构成可解释的空间规划，自然地重用了 VLM 预训练中获得的视觉‑空间对齐能力。
- **隐式潜动作规划路径**：VLM 同时预测离散的潜动作令牌序列，这些令牌来自一个预训练的语义潜动作码本，承载紧凑的视觉运动基元。

两条路径在功能上互补：显式轨迹提供直观的几何引导，但易受坐标精度影响；潜动作令牌则融合视觉观测信息，补偿轨迹的数值不稳定性。这种协同使得 VLM 的推理真正服务于任务规划，而非停留在特征融合层面。

### 三阶段训练流程

为实现上述双路径协同，SemanticVLA 采用三阶段训练流程（Figure 1 给出概览）：

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/001_Figure_1.jpg]]
*Figure 1: SemanticVLA Overview. Current VLA models struggle with instruction variations and reasoning-intensive tasks, often memorizing patterns rather than understanding semantics. We introduce a dual-path architecture that generates explicit trace reasoning as interpretable spatial waypoints alongside implicit latent action tokens as compact visuomotor primitives. Built on our curated TraceX-240K with trace-annotated trajectories, SemanticVLA demonstrates robust performance and strong generalization across simulation and real-world deployment, maintaining stable success rates under instruction rephrasing where baselines degrade significantly*

1. **语义潜动作令牌预训练**：在不引入语言信号的条件下，通过两阶段 VQ‑VAE 框架学习具备几何与视觉双重语义的潜动作令牌。第一阶段从纯轨迹坐标中学习稳定的几何基元，第二阶段将这些几何基元与视觉观测对齐，形成融合表征。
2. **VLM 联合训练**：VLM 同时预测显式轨迹坐标和潜动作令牌索引，建立二者的语义对应关系。此阶段不涉及动作解码器，仅通过交叉熵损失联合优化文本生成和令牌预测。
3. **流匹配动作解码器微调**：在弱 VLM 正则化约束下，端到端微调基于流匹配的动作解码器。解码器以轨迹隐藏态和潜令牌隐藏态作为双路条件，生成连续控制动作。

### 输入输出流

整个 pipeline 的输入输出关系如下：

- **输入**：单帧视觉观测 $o_t$ 和语言指令 $\ell_t$。
- **VLM 处理**：VLM 接收视觉与语言输入后，同时执行两条生成路径——自回归预测轨迹路点序列 $\tau = \{p_j\}_{j=1}^L$（式 4）和在轨迹条件下预测潜动作令牌序列 $q_{1:N}$（式 5）。
- **动作解码**：流匹配解码器融合轨迹隐藏态与潜令牌隐藏态，输出连续控制动作序列。
- **训练目标**：预训练阶段使用 $\mathcal{L}_{\mathrm{LAT}}$（式 3），VLM 联合训练使用 $\mathcal{L}_{\mathrm{VLM}}$（式 6），微调阶段使用 $\mathcal{L}_{\mathrm{finetune}} = \lambda_{\mathrm{VLM}} \mathcal{L}_{\mathrm{VLM}} + \mathcal{L}_{\mathrm{flow}}$（式 7）。

### 与基线方法的关键差异

相较于现有 VLA 基线，SemanticVLA 在三个关键设计点上做出了改变：

| 设计维度 | 基线方法 | SemanticVLA |
|---------|---------|-------------|
| VLM 输出接口 | 不透明的潜嵌入（如 UniVLA 使用任务语言作为中间模态过滤视觉变化） | 显式 2D 轨迹坐标序列 + 潜动作令牌索引 |
| 训练流程 | 端到端微调 VLM + 动作解码器 | 三阶段训练，避免语言污染并保护 VLM 预训练能力 |
| 潜令牌监督 | 仅视觉重建或语言条件（如 VQ‑VLA 仅依赖视觉，存在外观纠缠） | 先纯轨迹几何重建，再融合视觉特征的双重重构 |

这些设计使得 SemanticVLA 在仿真和真实世界基准上均显著优于强基线——在 LIBERO 上达到 97.0% 平均成功率，在 SimplerEnv 上达到 65.1%，并在指令改写测试中展现出远优于基线的性能稳定性。

## 核心模块与公式推导

SemanticVLA 的核心由三个模块级联构成：**语义潜动作分词器（Semantic Latent Action Tokenizer）**、**VLM 联合训练（VLM Co-training）** 以及 **流匹配动作解码器（Flow Matching Action Decoder）**。三者共同实现了“显式轨迹推理—隐式潜动作规划—连续控制生成”的双路径协同。

---

### 语义潜动作分词器（两阶段 VQ-VAE）

该模块的目标是学习一组紧凑的离散潜动作令牌，使其同时具备几何语义（来自轨迹）和视觉语义（来自观测），为下游 VLM 提供可预测的动作基元。

**第一阶段：纯轨迹几何量化**

首先，将专家轨迹 $\tau$（归一化 2D 坐标序列）通过编码器 $\phi_{\mathrm{enc}}^{\mathrm{trace}}$ 映射为连续隐变量，再在轨迹专属码本 $\{\mathbf{c}_k^{\mathrm{trace}}\}$ 中查找最近邻，得到离散几何基元索引 $q_{\mathrm{trace}}$：

$$z_{\mathrm{trace}} = \phi_{\mathrm{enc}}^{\mathrm{trace}}(\tau), \quad q_{\mathrm{trace}} = \arg \min_k \| \mathbf{z}_{\mathrm{trace}} - \mathbf{c}_k^{\mathrm{trace}} \|^2$$

这一阶段**刻意排除视觉观测**，避免空间结构与外观变化纠缠，确保几何锚点的稳定性。

**第二阶段：视觉-几何融合量化**

获得 $q_{\mathrm{trace}}$ 对应的几何基元 $\mathbf{c}_{q_{\mathrm{trace}}}^{\mathrm{trace}}$ 后，将其与视觉特征 $\mathbf{h}_{\mathrm{visual}}$ 拼接，送入融合编码器 $\phi_{\mathrm{enc}}^{\mathrm{fused}}$，再在动作码本 $\{\mathbf{c}_k^a\}$ 中量化，得到最终潜动作令牌索引 $q_a$：

$$q_a = \arg \min_k \| \phi_{\mathrm{enc}}^{\mathrm{fused}}(\mathbf{c}_{q_{\mathrm{trace}}}^{\mathrm{trace}} \oplus \mathbf{h}_{\mathrm{visual}}) - \mathbf{c}_k^a \|^2$$

两阶段的总训练目标为：

$$\mathcal{L}_{\mathrm{LAT}} = \mathcal{L}_{\mathrm{vq}}^a + \mathcal{L}_{\mathrm{recon}}^{\mathrm{trace}} + \mathcal{L}_{\mathrm{recon}}^{\mathrm{visual}}$$

其中 $\mathcal{L}_{\mathrm{vq}}^a$ 为标准 VQ 损失（含编码器承诺损失与码本更新项），$\mathcal{L}_{\mathrm{recon}}^{\mathrm{trace}}$ 与 $\mathcal{L}_{\mathrm{recon}}^{\mathrm{visual}}$ 分别为轨迹坐标与视觉观测的双重重建损失。这一双重重建监督迫使潜令牌同时保留空间结构与视觉外观信息。

---

### VLM 联合训练：轨迹与潜令牌双路径预测

预训练好的潜动作码本被冻结后，VLM 同时承担两条生成路径。

**显式轨迹推理**

VLM 通过其原生语言接口，以文本令牌形式自回归生成归一化 2D 路点序列 $p_j$：

$$p(\tau \mid o_t, \ell_t) = \prod_{j=1}^L p(p_j \mid o_t, \ell_t, \tau_{<j})$$

其中 $o_t$ 为当前视觉观测，$\ell_t$ 为语言指令。该路径直接输出可解释的空间坐标，重用了 VLM 预训练中习得的空间对齐能力。

**隐式潜动作规划**

在已生成轨迹 $\tau$ 的条件下，VLM 进一步预测潜动作令牌索引序列 $q_i$：

$$p(q_{1:N} \mid o_t, \ell_t, \tau) = \prod_{i=1}^N p(q_i \mid o_t, \ell_t, \tau, q_{<i})$$

VLM 的联合训练损失为两条路径的交叉熵之和：

$$\mathcal{L}_{\mathrm{VLM}} = \mathcal{L}_{\mathrm{trace}} + \mathcal{L}_{\mathrm{latent}}$$

轨迹预测为潜令牌学习提供**时间对齐的辅助语义监督**——显式坐标序列约束了潜令牌应承载的几何意图，从而缓解了仅靠动作损失反向传播时 VLM 预训练语义能力被破坏的问题。

---

### 流匹配动作解码器

下游的动作解码器采用流匹配网络，其条件信号来自双路径的隐藏态：轨迹隐藏态与潜令牌隐藏态。这两路条件在特征层面融合后，驱动流匹配过程生成连续控制动作。

微调阶段，整个系统以弱 VLM 正则化方式端到端优化：

$$\mathcal{L}_{\mathrm{finetune}} = \lambda_{\mathrm{VLM}} \mathcal{L}_{\mathrm{VLM}} + \mathcal{L}_{\mathrm{flow}}$$

其中 $\lambda_{\mathrm{VLM}}$ 控制 VLM 损失的权重，$\mathcal{L}_{\mathrm{flow}}$ 为流匹配损失。VLM 部分使用 LoRA 进行参数高效微调，流匹配解码器则从头训练。这种设计保持了模态分离——VLM 专注于语义规划，动作解码器专注于连续控制——避免跨模态干扰。

### 补充图表

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/002_Figure_2.jpg]]
*Figure 2: Semantic Latent Action Tokenizer. Two-stage architecture for trace-guided latent tokens. Stage 1 learns geometric patterns from traces. Stage 2 grounds them in visual observations, with dual reconstruction of trace and visual representations producing latent actions with both spatial and visual semantics*

## 实验与分析

### 仿真基准评估

SemanticVLA 在 LIBERO 和 SimplerEnv 两个仿真基准上进行了系统评估。LIBERO 包含 LIBERO-Spatial、LIBERO-Object、LIBERO-Goal 和 LIBERO-Long 四个子任务套件，覆盖空间关系理解、物体交互、目标导向和长序列规划等能力维度。SimplerEnv 则基于 WidowX 机器人平台，测试模型在视觉丰富场景下的泛化能力。

**Table 1** 展示了主要对比结果。SemanticVLA 在 LIBERO 上取得了 97.0% 的平均成功率，在 SimplerEnv 上取得了 65.1% 的成功率，在两个基准上均显著优于所有基线方法。在 LIBERO 上，排名第二的 **UniVLA** 达到 95.2%，差距为 +1.8 个百分点。在 SimplerEnv 上，优势更为突出：UniVLA 仅为 31.3%，SemanticVLA 领先 +33.8 个百分点。这一巨大差距揭示了关键瓶颈：SimplerEnv 的视觉场景和任务分布与训练数据差异更大，纯潜动作方法（如 UniVLA）在此条件下泛化能力急剧下降，而 SemanticVLA 的显式轨迹推理提供了更稳定的几何先验，使其在分布外场景中保持鲁棒。

值得注意的是，在 LIBERO-Spatial 子任务上，SemanticVLA 达到 96.7%，UniVLA 为 96.0%，差距较小；但在 LIBERO-Long 上，SemanticVLA 达到 95.7%，而多个基线出现明显下降。这表明长序列任务对语义理解和规划一致性要求更高，双路径设计的优势在任务复杂度上升时更加明显。

### 真实世界机器人实验

**Figure 4** 展示了真实世界实验的任务场景。实验涵盖两大类任务：长序列组合任务（食物准备和桌面整理）和推理密集型任务（数学计算和单词拼写）。食物准备任务要求机器人依次完成多个子步骤（如拿取食材、放置到指定位置），桌面整理涉及多物体分类摆放。数学计算任务要求机器人根据算式结果抓取对应数量的物体，单词拼写则需按字母顺序操作标有字母的方块。

**Table 2** 报告了真实世界实验的成功率。SemanticVLA 在长序列和推理场景下取得了 62.3% 的平均成功率。在食物准备任务上成功率为 68%，桌面整理为 65%，数学计算为 58%，单词拼写为 58%。这些任务对语义理解和多步规划的要求远高于标准抓取任务，62.3% 的整体成功率表明 SemanticVLA 具备初步的语义推理能力，但距离实用仍有提升空间。

### 指令改写鲁棒性

指令改写鲁棒性是衡量 VLA 模型是否真正理解语义而非记忆动作模式的核心指标。**Figure 5** 对比了 SemanticVLA 与基线方法在原始指令和改写指令下的性能变化。在 LIBERO 上，SemanticVLA 的改写指令成功率为 56%（原始指令为 97%，图中以虚线/实心柱区分），而 UniVLA 从 95.2% 骤降至约 30%，OpenVLA 从约 88% 降至约 25%。在 SimplerEnv 上，SemanticVLA 的改写指令成功率为 56%，UniVLA 降至约 10%。

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/006_Figure_5.jpg]]
*Figure 5: Instruction Rephrasing Robustness. Performance on LIBERO and SimplerEnv benchmarks under instruction variations. Dashed bars: success rates with original instructions; Solid bars: rephrased instructions with similar task semantics*

这一对比直接验证了论文的核心论断：仅靠潜嵌入通信的 VLA 模型容易退化为动作模式记忆器，当指令表述发生变化时性能崩溃。SemanticVLA 的显式轨迹推理路径迫使 VLM 在语义层面理解任务目标并生成空间路点，而非简单地将指令模式映射到动作分布，因此在指令改写条件下保持了显著更稳定的性能。

### 消融实验

消融实验围绕三个关键设计选择展开：显式轨迹推理的作用、潜动作令牌的贡献、以及双路径协同的必要性。

**移除显式轨迹推理**（Figure 6）：当仅使用潜动作令牌路径时，潜预测准确率从 93.6% 降至 85.6%，任务成功率从 87.6% 降至 79.2%。这一 8.4 个百分点的成功率下降表明，轨迹推理为潜动作学习提供了关键的辅助监督信号。训练曲线（Figure 6）进一步显示，移除轨迹推理后，潜预测准确率的收敛速度明显变慢，且最终收敛值更低，验证了轨迹预测作为“语义锚点”对潜令牌学习的引导作用。

**仅使用轨迹推理（无潜动作令牌）**（Figure 7）：在真实世界指令改写测试中，纯轨迹推理的成功率为 48%，完整双路径模型为 56%，而 **MolmoAct**（将轨迹预测作为辅助推理的基线）仅为 33%。纯轨迹推理虽然优于 MolmoAct，但低于完整模型，说明轨迹坐标对视觉噪声和数值精度敏感，潜动作令牌融合视觉观察后能有效补偿这一不稳定性。

**双路径协同的不可替代性**：综合以上消融结果，轨迹推理和潜动作令牌在功能上互补——轨迹提供直观的几何引导但受坐标精度限制，潜令牌融合视觉信息以增强鲁棒性。单独使用任一路径都会导致性能显著下降，尤其在指令改写和视觉扰动场景下，双路径协同的优势更加突出。

### 失败模式分析

根据实验结果推断（论文未提供详细的失败案例分类，以下分析基于性能数据和架构特性，需手动验证）：

1. **坐标精度敏感**：纯轨迹推理在指令改写测试中成功率仅为 48%，说明 VLM 生成的 2D 路点坐标存在精度误差，在需要精细操作的任务中可能导致抓取失败。流匹配解码器在一定程度上缓解了这一问题，但无法完全消除。

2. **长序列累积误差**：在 LIBERO-Long 和真实世界长序列任务中，成功率相对较短任务有所下降。自回归生成轨迹和潜令牌序列时，早期步骤的误差可能向后传播，影响后续规划。

3. **推理密集型任务的瓶颈**：数学计算和单词拼写任务的成功率（58%）低于组合操作任务（65-68%），表明 VLM 的符号推理能力在具身场景中仍有局限，可能受限于视觉-语言对齐的精度和训练数据中推理样本的覆盖度。

4. **视觉扰动的鲁棒性**：Figure 7 显示在视觉扰动条件下性能有所下降，潜令牌路径对视觉外观变化存在一定敏感性，尽管双路径设计提供了冗余，但极端视觉变化仍可能影响整体性能。

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/008_Figure_7.jpg]]
*Figure 7: Real-world generalization evaluations under visual perturbation, instruction rephrasing, and task variation*

### 补充图表

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/004_Table_1.jpg]]
*Table 1: Performance comparison on LIBERO and SimplerEnv. Underlined scores show best results excluding SemanticVLA*

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/009_Figure_6.jpg]]
*Figure 6: The analysis of latent learning. Training curves on LIBERO instruction rephrasing. Solid lines: success rate (right yaxis); Dashed lines: latent prediction accuracy (left y-axis)*

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/007_Table_2.jpg]]
*Table 2: Success rate evaluation in real robot experiments in long-horizon and reasoning scenarios*

![[assets/figures/papers/paper_list_l2594_https_openaccess_thecvf_com_content_CVPR2026_html_Ni_SemanticVLA_Towards/figures/005_Figure_4.jpg]]
*Figure 4: Real-world robot experiments. We evaluate SemanticVLA on long-horizon compositional tasks (food preparing and desktop sorting) and reasoning-intensive tasks (math calculation and word spelling), demonstrating robust performance across various scenarios*

## 方法谱系与知识库定位

### 1. 核心瓶颈：从“动作记忆”到“语义推理”的断层

当前视觉-语言-动作（VLA）模型面临一个根本性瓶颈：VLM 与动作专家之间通过不透明的潜嵌入（latent embeddings）进行通信。这些嵌入缺乏语义可解释性，导致指导信号模糊且不稳定。更严重的是，仅靠动作损失的反向传播会破坏 VLM 的预训练语义能力，使模型退化为记忆动作模式的参数重融合编码器，而非进行组合推理。这正是 SemanticVLA 试图突破的核心问题——让 VLM 真正“理解”任务语义，而非简单地拟合动作分布。

### 2. 关键调控变量：显式轨迹推理作为语义桥梁

SemanticVLA 的核心创新在于引入了一个关键调控变量：利用 VLM 原生语言接口生成可解释的显式 2D 空间轨迹（坐标序列）作为中间规划。这一设计同时解决了两个问题：（1）重用了 VLM 预训练的空间对齐能力，使推理过程具有可解释性；（2）为下游的潜动作学习提供了时间对齐、语言无关的辅助语义监督，避免了纯动作损失对 VLM 语义能力的侵蚀。

显式轨迹推理与隐式潜动作令牌在功能上形成互补：轨迹提供直观的几何引导但易受坐标精度影响，潜动作令牌融合视觉观察以补偿轨迹的数值不稳定性。通过双路径协同，VLM 的推理真正服务于任务规划，而非停留在特征融合层面。

### 3. 与基线方法的关系定位

#### 3.1 纯潜动作 VLA 基线：UniVLA 与 VQ-VLA

**UniVLA** 和 **VQ-VLA** 代表了当前主流的潜动作范式：使用任务语言作为中间模态过滤视觉变化，或基于矢量量化进行动作分词。SemanticVLA 与它们的核心差异在于输出接口表示：基线使用不透明的潜嵌入，而 SemanticVLA 同时输出显式 2D 轨迹坐标序列（文本 token）和潜动作令牌（离散 codebook 索引）。在训练流程上，SemanticVLA 采用三阶段训练（轨迹引导的潜令牌预训练 → VLM 联合预测 → 弱正则微调），而非端到端联合优化，从而保护了 VLM 的预训练能力。

在 LIBERO 基准上，UniVLA 以 95.2% 的平均成功率位居第二（SemanticVLA 为 97.0%），但在 SimplerEnv 上仅取得 31.3%，远低于 SemanticVLA 的 65.1%。这一巨大差距揭示了纯潜动作方法在跨平台泛化上的脆弱性。

#### 3.2 轨迹推理基线：MolmoAct

**MolmoAct** 将轨迹预测作为辅助推理，与 SemanticVLA 的显式轨迹路径最为接近。但关键区别在于，MolmoAct 缺乏潜动作令牌路径的协同补偿机制。在指令改写测试中，仅使用轨迹推理的 SemanticVLA 变体成功率为 48%，完整双路径模型为 56%，而 MolmoAct 基线仅为 33%。这验证了“轨迹 + 潜令牌”双路径协同对于指令改写鲁棒性的必要性。

#### 3.3 其他相关工作

- **OpenVLA**：开源自回归 VLA 模型，作为通用基线存在，但缺乏显式推理机制。
- **TraceVLA**：使用历史轨迹作为视觉提示增强空间时序感知，但未将轨迹作为 VLM 的生成目标。
- **Magma**：生成 2D 路点以条件化低层策略，与 SemanticVLA 的轨迹路径思路相似，但缺少潜动作令牌的互补设计。
- **FAST** 和 **Octo**：分别关注高效动作分词化和通用机器人策略，属于动作表示层面的并行工作。
- **CoT-VLA**：视觉思维链推理 VLA，强调推理过程的可解释性，但未引入显式空间轨迹作为中间表示。

### 4. 方法适用边界

#### 4.1 适用场景

SemanticVLA 在以下场景展现出显著优势：
- **指令改写鲁棒性**：在 LIBERO 和 SimplerEnv 的指令变体测试中，性能稳定性远优于基线方法，这得益于显式轨迹推理提供的语言无关语义锚定。
- **长序列组合任务**：真实世界实验中，在食物准备和桌面整理等任务上表现出稳健性能（平均成功率 62.3%），双路径设计有助于分解复杂任务规划。
- **推理密集型任务**：数学计算和单词拼写等需要语义理解的场景，显式轨迹推理使 VLM 的语义能力得以保留和利用。

#### 4.2 潜在局限

- **坐标精度敏感性**：显式轨迹推理依赖 2D 坐标序列的准确性，在需要高精度 3D 操作或动态环境中可能面临挑战。潜动作令牌路径虽能部分补偿，但双路径的协同上限受限于轨迹质量。
- **三阶段训练复杂度**：相比端到端基线，三阶段训练流程增加了工程复杂度，且第一阶段需在无语言污染的条件下预训练潜令牌，对数据质量有额外要求。
- **未见环境的泛化边界**：虽然 SimplerEnv 上的跨平台泛化表现突出，但真实世界实验规模有限，在更广泛的环境多样性下的泛化能力仍需进一步验证。

### 5. 开放问题与知识库定位

SemanticVLA 在 VLA 方法谱系中占据了“显式推理 + 隐式执行”的独特位置，其核心贡献在于证明了 VLM 的语义推理能力可以通过适当的接口设计（轨迹坐标序列）被有效利用，而非被动作损失所破坏。以下问题值得后续工作关注：

1. **轨迹表示的扩展性**：当前使用 2D 坐标序列，能否扩展到 3D 空间轨迹或包含力控信息的更丰富表示？这直接影响方法在精细操作任务上的适用性。
2. **双路径权重的自适应调节**：在不同任务类型（如高精度操作 vs. 语义推理）中，轨迹路径和潜动作路径的相对重要性可能不同，自适应调节机制可能进一步提升性能。
3. **与更大规模 VLM 的兼容性**：SemanticVLA 的轨迹推理能力依赖于 VLM 的空间对齐能力，随着更强 VLM 的出现，该方法是否能线性受益？
4. **训练效率优化**：三阶段训练流程是否可以合并或简化，以降低实际部署的门槛？

在知识库定位上，SemanticVLA 应被归类为“VLA 语义推理增强方法”，与纯潜动作方法（UniVLA、VQ-VLA）、轨迹条件方法（MolmoAct、Magma）、思维链推理方法（CoT-VLA）形成互补对照关系。其核心方法论贡献——利用 VLM 原生语言接口生成可解释中间规划以保护语义能力——为后续 VLA 研究提供了重要的设计原则参考。

## 原文 PDF

![[paperPDFs/CVPR_2026/SemanticVLA_Towards_Semantic_Reasoning_over_Action_Memorization_via_Synergistic_Explicit_Trace_and_Latent_Action_Planning.pdf]]

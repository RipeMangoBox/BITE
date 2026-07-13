---
title: "VL-Eraser: Vacuum Distillation for Machine Unlearning in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VL_Eraser_Vacuum_Distillation_for_Machine_Unlearning_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- VE
- VL-Eraser
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 是否在遗忘过程中保持跨模态对齐不被破坏，从而完整剥离指定知识。
primary_logic: 将遗忘重构为“真空蒸馏→算术删除”两阶段过程：在正交于保留知识的真空空间中把遗忘知识蒸馏到低秩适配器（LoRA），再通过参数减法实现干净删除，从而避免对齐损伤。
claims:
- 传统方法仅通过文本探针或重载投影即可暴露出大量残留知识，说明遗忘主要来自对齐破坏（图1d）
- VL-Eraser 在遗忘集上取得最低分类准确率（如LLaVA Visual-QA 26.2），同时保持模型在保留集和真实分布上的效用（表1）
- 移除真空空间约束后保留集准确率从43.4骤降至36.6，证明正交约束是防止干扰保留知识的关键（表2）
- MLLMU-Bench (LLaVA-1.5-7B, 5% forget ratio) 上 Classification Accuracy (Forget ↓) = 26.2 (Vision-QA), 25.0 (Textual-QA)
---

# VL-Eraser: Vacuum Distillation for Machine Unlearning in Vision-Language Models

> [!tip] 核心洞察
> 将遗忘重构为“真空蒸馏→算术删除”两阶段过程：在正交于保留知识的真空空间中把遗忘知识蒸馏到低秩适配器（LoRA），再通过参数减法实现干净删除，从而避免对齐损伤。

| 字段 | 内容 |
|------|------|
| 中文题名 | VL-Eraser：面向视觉语言模型机器遗忘的真空蒸馏方法 |
| 英文题名 | VL-Eraser: Vacuum Distillation for Machine Unlearning in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_VL-Eraser_Vacuum_Distillation_for_Machine_Unlearning_in_Vision-Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VL-Eraser |
| Dataset | MLLMU-Bench |

> [!tip] 效果简介
> - MLLMU-Bench (LLaVA-1.5-7B, 5% forget ratio) 上，Classification Accuracy (Forget ↓) 26.2 (Vision-QA), 25.0 (Textual-QA) vs Vanilla model (average 24.1% degradation compared to vanilla) (~24.1% reduction from vanilla)；Classification Accuracy (Retain ↑) 43.4 (Vision-QA), 46.2 (Textual-QA) vs Vanilla model (closest utility among all methods) (minimal utility drop compared to vanilla)。

## 概要

视觉语言模型（VLMs）的机器遗忘（Machine Unlearning, MU）旨在从已训练模型中移除指定数据的影响，以满足隐私法规与安全需求。然而，现有的遗忘方法大多沿用反向训练范式——通过最大化预训练损失来“破坏”模型在遗忘集上的表现。在多模态场景下，这一范式暴露出根本性瓶颈：反向训练倾向于破坏跨模态对齐，而非真正消除知识，导致遗忘不彻底并遗留泄漏风险。如图1(d)所示，即使经过遗忘处理，仅通过文本探针或重载原始投影即可暴露大量残留知识，说明模型只是“绕开”了问题，而非真正遗忘了目标信息。

针对上述瓶颈，本文提出 **VL-Eraser**，一种面向视觉语言模型的真空蒸馏遗忘方法。其核心洞察是：**将遗忘重构为“真空蒸馏 → 算术删除”两阶段过程**，在正交于保留知识的真空空间中，将遗忘知识蒸馏到低秩适配器（LoRA），再通过参数减法实现干净删除，从而避免对齐损伤。

具体而言，VL-Eraser 首先利用保留集图像特征进行奇异值分解（SVD），构建真空空间投影矩阵，确保蒸馏过程天然过滤保留知识；随后在冻结原始参数的前提下，仅在 FFN 层插入的 LoRA 上进行蒸馏训练，联合优化蒸馏损失与交叉熵保真度损失，将遗忘知识专一性地转移至 LoRA；最后，将训练好的 LoRA 参数从原始 FFN 权重中减去，得到不包含遗忘知识的安全模型。

在 MLLMU-Bench 基准上，以 LLaVA-1.5-7B 和 Qwen2-VL-7B-Instruct 为骨干、5% 遗忘比例设置下，VL-Eraser 在遗忘集上取得最低分类准确率（如 LLaVA Visual-QA 仅 26.2），同时保持模型在保留集和真实分布上的效用最接近原始模型（保留集 43.4）。消融实验进一步证实，移除真空空间约束后保留集准确率从 43.4 骤降至 36.6，验证了正交约束是防止干扰保留知识的关键机制。

在方法谱系上，VL-Eraser 区别于 **Gradient Ascent**（Thudi et al., EuroS&P 2022）、**KL-based Negative Optimization**（Nguyen et al., NeurIPS 2020）、**NPO**（Zhang et al., CoLM 2024）等反向训练范式，以及 **CLIPErase**（Yang et al., arXiv 2024）、**Multidelete**（Cheng and Amiri, ECCV 2024）等多模态遗忘方法，首次将参数隔离与算术删除引入 VLM 遗忘，为多模态机器遗忘提供了新的范式。



### 视觉语言模型中的遗忘需求

大规模视觉语言模型（VLMs）在预训练过程中不可避免地会接触到包含个人隐私、偏见信息或版权敏感内容的训练数据。随着隐私法规（如GDPR的“被遗忘权”）和AI安全要求的强化，如何从已部署的VLM中干净地移除特定数据的影响——即**机器遗忘**——已成为一个迫切且具有挑战性的问题。

### 传统反向训练范式的根本缺陷

当前主流的机器遗忘方法普遍采用**反向训练**范式：将遗忘过程形式化为对遗忘集 $\mathcal{D}^f$ 上预训练损失的负优化：

$$\mathcal{L}_{unlearn} = -\sum_{(\nu_i,t_i;a_i)\in\mathcal{D}^f} \mathcal{L}_{pre-train}(\mathcal{M}_\theta(\nu_i,t_i,a_i))$$

这一范式在纯文本大语言模型（LLMs）中取得了一定成效，但在多模态场景下暴露出根本性缺陷。VLM的遗忘不仅需要消除LLM解码器中的文本知识，还必须处理跨模态对齐层中存储的视觉-语义关联。**传统反向训练倾向于通过破坏跨模态对齐来降低模型在遗忘集上的表面性能，而非真正消除知识本身。**

Figure 1 清晰地揭示了这一问题：通过对遗忘后的模型分别进行纯文本探针测试和重新加载原始视觉投影，均暴露出大量残留知识，表明知识并未被真正遗忘，而只是被“遮蔽”在对齐损伤之下。这种**对齐破坏-表面遗忘**的机制带来了严重的泄漏风险：攻击者只需绕过受损的对齐路径，即可恢复被“遗忘”的敏感信息。

### 现有方法的系统性缺口

现有的多模态遗忘方法——包括 **Gradient Ascent**（Thudi et al., EuroS&P 2022）、**KL-based Negative Optimization**（Nguyen et al., NeurIPS 2020）、**Negative Preference Optimization**（Zhang et al., CoLM 2024）、**CLIPErase**（Yang et al., arXiv 2024）和 **Multidelete**（Cheng and Amiri, ECCV 2024）——在以下三个维度上存在系统性缺失：

1. **缺乏知识隔离机制**：反向训练不加区分地扰动所有参数，导致遗忘知识与保留知识相互干扰，引发灾难性遗忘。
2. **遗忘不彻底**：表面性能下降来源于对齐破坏而非知识删除，残留知识可通过简单手段恢复。
3. **参数更新范围失控**：全模型或大范围参数更新使得遗忘过程难以精确控制，增加了不可预见的副作用风险。

### 本文动机与核心思路

针对上述缺口，本文提出 **VL-Eraser**，将机器遗忘重新定义为**“真空蒸馏→算术删除”**两阶段过程。核心洞见在于：**如果能在正交于保留知识的真空空间中，将遗忘知识完整蒸馏到低秩适配器（LoRA）中，再通过参数减法实现干净删除，就可以在彻底遗忘的同时保持跨模态对齐不受损伤。** 这一范式从根源上避免了传统反向训练的对齐破坏问题，为VLM的机器遗忘提供了一条可控、彻底且保持模型效用的新路径。



## 核心方法与创新机理

### 瓶颈洞察：反向训练本质上是“对齐破坏”而非“知识删除”

传统机器遗忘（Machine Unlearning, MU）在多模态视觉语言模型（VLM）中的主流范式是反向训练——直接对遗忘集最大化预训练损失，即 $\mathcal{L}_{unlearn} = -\sum_{(\nu_i,t_i;a_i)\in\mathcal{D}^f} \mathcal{L}_{pre-train}(\mathcal{M}_\theta(\nu_i,t_i,a_i))$。然而，VL-Eraser 的作者通过实验揭示了一个关键瓶颈：**反向训练的实际效果并非真正抹除知识，而是破坏了视觉与语言模态之间的跨模态对齐**。如 Figure 1(d) 所示，即使经过遗忘处理，仅通过文本探针提问或重新加载原始视觉投影，模型仍能暴露出大量残留知识，构成严重的泄漏风险。这一发现从根本上动摇了传统 MU 范式在多模态场景下的有效性假设——模型只是“看不到”而非“不知道”。

### 范式转换：从“反向优化”到“蒸馏-删除”两阶段

VL-Eraser 的核心创新在于将遗忘问题**重构**为两个解耦的阶段：

| 维度 | 传统反向训练 | VL-Eraser |
|------|-------------|-----------|
| **遗忘范式** | 直接优化负预训练损失 | 蒸馏-删除两阶段：在正交空间蒸馏遗忘知识到 LoRA，再通过算术删除 |
| **训练损失** | 负的预训练损失（如 $-\mathcal{L}_{pre-train}$） | 组合损失 $\mathcal{L}_{Total} = \lambda \mathcal{L}_{Distill} + (1-\lambda)\mathcal{L}_{CE}$，在真空空间中匹配 FFN 与 LoRA 输出，同时在遗忘集上维持保真度 |
| **参数更新范围** | 全模型参数或特定层进行反向梯度更新 | 仅在 FFN 层插入的低秩适配器（LoRA）上进行蒸馏训练，原始参数冻结 |
| **知识隔离约束** | 无特殊隔离机制 | 在真空空间（左零空间）中执行蒸馏，使 LoRA 参数与保留集表示正交 |

这一范式转换的因果杠杆在于：**是否在遗忘过程中保持跨模态对齐不被破坏，从而完整剥离指定知识**。传统方法因直接扰动原始参数而不可避免地损伤对齐结构；VL-Eraser 则通过冻结原始模型、仅在正交子空间中操作，从根本上规避了这一风险。

### 真空蒸馏：正交约束下的知识解耦

真空蒸馏（Vacuum Distillation）是 VL-Eraser 的第一阶段，也是其最核心的技术创新。其关键思想是：**在正交于保留知识的“真空空间”中，将遗忘知识从原始模型蒸馏到低秩适配器（LoRA）中**。

具体而言，该方法首先利用保留集图像特征进行 SVD 分解 $\{U,\Sigma,(U)^\top\} = \mathrm{SVD}(\mathrm{pooling}(\mathbf{H}_{\mathrm{image}}))$，构建正交投影矩阵 $\mathbf{P}$，定义真空空间（左零空间）。该空间满足约束条件 $Proj_{vacuum}(\mathbf{W}_{\mathrm{LoRA}}) \cdot \mathbf{H}_r = 0$，确保投影后的 LoRA 参数与保留集表示天然正交。随后，在每一层 FFN 上以冻结的原始参数为教师、LoRA 为学生，通过余弦相似度损失 $\mathcal{L}_{\mathrm{Distill}}^{l}$ 将遗忘知识专一性地转移到 LoRA 中，同时联合优化遗忘集上的交叉熵损失 $\mathcal{L}_{CE}$ 以维持知识保真度。

消融实验（Table 2）强有力地验证了这一设计的必要性：**移除真空空间约束后，保留集分类准确率从 43.4 骤降至 36.6**，遗忘质量与模型效用同时退化，证明正交约束是防止干扰保留知识的关键机制。

### 算术删除：干净且可逆的参数减法

第二阶段**算术删除**（Arithmetic Deletion）将训练好的、位于真空空间的 LoRA 参数从原始模型 FFN 权重中直接减去：$\mathbf{W}_{\mathrm{unlearned}} = \mathbf{W}_{\mathrm{FFN}} - \mathbf{W}_{\mathrm{LoRA}} \cdot \mathbf{P}$。由于 LoRA 参数完全位于真空空间内且与保留知识正交，这一减法操作能够干净地移除遗忘知识，同时保持原始模型在保留集上的性能不受影响。与反向训练中不可控的参数扰动相比，算术删除提供了精确、可解释且理论上可逆的遗忘机制。



VL-Eraser 将视觉语言模型（VLM）的机器遗忘重构为一个“蒸馏—删除”两阶段过程，从根本上改变了传统反向训练范式的因果路径。其核心洞察在于：**遗忘的瓶颈并非模型能否在遗忘集上表现变差，而是能否在不破坏跨模态对齐的前提下完整剥离指定知识**。传统方法（如梯度上升、负偏好优化等）通过直接最大化预训练损失来降低遗忘集性能，但这往往只是扰乱了视觉与语言模态之间的对齐关系，而非真正消除模型内部的知识表征（Figure 1d 中仅用文本探针或重载原始投影即可恢复大量残留知识，验证了这一判断）。

为突破这一瓶颈，VL-Eraser 将遗忘操作从“破坏对齐”切换为“先隔离再删除”：首先在正交于保留知识的真空空间中，通过蒸馏将遗忘知识专一性地转移到低秩适配器（LoRA）中；随后通过参数减法实现干净的知识删除，从而天然避免了对保留知识及其跨模态对齐的干扰。

### 两阶段流水线

整个框架由三个紧密耦合的模块串联构成，对应 Figure 2 所示的两个阶段。

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of the proposed method VL-Eraser. VL-Eraser reformulates unlearning as a two-stage process. In stage 1, the undesired knowledge is disentangled from the original VLMs and transferred into the LoRA via distillation. To avoid interference from other knowledge, this process is strictly constrained within a vacuum space, which is orthogonal to the retained knowledge. In stage 2, the LoRA parameters encoding undesired knowledge are subtracted from the pretrained model to form a safe yet useful VLM*

**阶段一：真空蒸馏（Vacuum Distillation）**

*Step 1 — 真空空间估计（Vacuum Space Estimation）*

利用保留集图像特征进行奇异值分解（SVD），构建正交投影矩阵 $P$，定义真空空间（即保留集表示空间的左零空间）。该空间的核心性质是：投影后的任何参数更新与保留集表示正交，满足 $Proj_{vacuum}(\mathbf{W}_{\mathrm{LoRA}}) \cdot \mathbf{H}_r = 0$。这一约束从结构上保证了后续蒸馏过程不会污染保留知识。

*Step 2 — 真空蒸馏（LoRA 训练）*

在 VLM 的每一层 FFN 中插入低秩适配器（LoRA），冻结原始 FFN 参数作为教师，训练 LoRA 作为学生。蒸馏过程受两个损失联合驱动：
- 蒸馏损失 $\mathcal{L}_{\mathrm{Distill}}$：在真空空间中匹配教师 FFN 输出与学生 LoRA 投影输出的余弦相似度，将遗忘知识从原始参数中解耦并转移到 LoRA；
- 交叉熵保真度损失 $\mathcal{L}_{\mathrm{CE}}$：在遗忘集上维持标准下一词预测损失，确保蒸馏过程中知识保持完整。

总优化目标为 $\mathcal{L}_{\mathrm{Total}} = \lambda \mathcal{L}_{\mathrm{Distill}} + (1-\lambda)\mathcal{L}_{\mathrm{CE}}$。由于蒸馏全程在真空投影矩阵 $P$ 的约束下进行，LoRA 仅能捕获与保留知识正交的遗忘知识分量。

**阶段二：算术删除（Arithmetic Deletion）**

将训练完成的 LoRA 参数从原始 FFN 权重中直接减去，得到不含遗忘知识的安全模型：

$$\mathbf{W}_{\mathrm{unlearned}} = \mathbf{W}_{\mathrm{FFN}} - \mathbf{W}_{\mathrm{LoRA}} \cdot \mathbf{P}$$

这一参数算术操作是“干净删除”的关键——因为 LoRA 中的知识已被真空空间严格隔离，减法操作不会对保留知识造成任何干扰。

### 输入输出与数据流

- **输入**：遗忘数据集 $\mathcal{D}_f$（包含待删除的视觉-文本样本对）和保留集图像特征（用于真空空间估计）。
- **参数更新范围**：仅 LoRA 适配器参与训练，原始 VLM 参数全程冻结。
- **输出**：遗忘后的安全模型，其 FFN 权重为 $\mathbf{W}_{\mathrm{unlearned}}$，在遗忘集上性能显著下降，同时在保留集和真实分布上保持与原始模型接近的效用。

### 与传统范式的关键差异

| 维度 | 传统反向训练 | VL-Eraser |
|------|-------------|-----------|
| 遗忘机制 | 破坏对齐以降低性能 | 真空蒸馏 → 参数减法 |
| 参数更新 | 全模型或特定层反向梯度 | 仅 LoRA 适配器，原始参数冻结 |
| 知识隔离 | 无 | 真空空间正交约束 |
| 对保留知识的影响 | 易导致灾难性遗忘 | 结构上天然隔离 |

消融实验（Table 2）为这一框架设计提供了关键支撑：移除真空空间约束后，保留集分类准确率从 43.4 骤降至 36.6，同时遗忘质量也同步退化，证明正交约束是防止干扰保留知识的核心因果开关。单独使用蒸馏损失或交叉熵损失均无法充分释放 VL-Eraser 的性能，二者联合优化是平衡知识转移与保真度的必要条件。



### 问题形式化：传统反向训练的局限

机器遗忘（Machine Unlearning, MU）在视觉语言模型（VLM）中的标准范式是反向训练，其目标函数为最大化预训练损失：

$$
\mathcal{L}_{unlearn} = -\sum_{(\nu_i,t_i;a_i)\in\mathcal{D}^f} \mathcal{L}_{pre-train}(\mathcal{M}_\theta(\nu_i,t_i,a_i))
$$

其中 $\mathcal{D}^f$ 为遗忘数据集，$\nu_i$、$t_i$、$a_i$ 分别表示视觉输入、文本问题与答案，$\mathcal{M}_\theta$ 为待遗忘的原始模型。该范式通过梯度上升故意破坏模型在遗忘集上的表现，但核心瓶颈在于：**反向训练倾向于破坏跨模态对齐，而非真正消除知识**。Figure 1(d) 的证据表明，仅通过纯文本探针或重载原始投影即可暴露大量残留知识，说明遗忘主要来自对齐损伤，而非知识根除。

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/001_Figure_1.jpg]]
*Figure 1: (a-c) Schematic of the traditional unlearning process in VLMs. These methods tend to disrupt modality alignment, hindering genuine knowledge removal. As evidenced in (d), both text-only question probing (- -) and reloading original projection (- -) reveal significant residual knowledge within the LLM, posing a leakage risk. In contrast, our method ensures consistent unlearning in VLMs*

### VL-Eraser 两阶段框架

VL-Eraser 将遗忘重构为“蒸馏-删除”两阶段过程（Figure 2）：

- **阶段一（真空蒸馏）**：在正交于保留知识的真空空间中，将遗忘知识从冻结的原始 FFN 层蒸馏到低秩适配器（LoRA）中。
- **阶段二（算术删除）**：将训练好的 LoRA 参数从原始模型权重中减去，得到安全模型。

### 模块一：真空空间估计（Vacuum Space Estimation）

真空空间的核心约束是：投影后的 LoRA 参数必须与保留集表示正交，确保蒸馏过程不干扰保留知识：

$$
Proj_{vacuum}(\mathbf{W}_{\mathrm{LoRA}}) \cdot \mathbf{H}_r = 0
$$

其中 $\mathbf{H}_r$ 为保留集在 FFN 层的中间表示。为构建这一正交空间，VL-Eraser 对保留集图像特征进行奇异值分解：

$$
\{U,\Sigma,(U)^\top\} = \mathrm{SVD}(\mathrm{pooling}(\mathbf{H}_{\mathrm{image}}))
$$

通过移除对应非零奇异值的特征向量，得到真空空间投影矩阵 $\mathbf{P}$。该矩阵定义了与保留知识正交的子空间，后续所有蒸馏操作均在此空间内进行，天然过滤无关知识的干扰。

### 模块二：真空蒸馏（Vacuum Distillation）

蒸馏阶段冻结原始 FFN 参数作为教师，仅训练插入的 LoRA 作为学生。逐块蒸馏损失计算教师输出与学生投影输出的余弦相似度：

$$
\mathcal{L}_{\mathrm{Distill}}^{l} = \frac{1}{S}\sum_{s=1}^{S} 1-\frac{(\widetilde{\mathbf{W}_{\mathrm{FFN}}^{l,s}})^\top (\widetilde{\mathbf{W}_{\mathrm{LoRA}}^{l}}\mathbf{P}^{l,s})}{\|\mathbf{W}_{\mathrm{FFN}}^{l}\mathbf{H}^{l,s}\|_2\|\mathbf{W}_{\mathrm{LoRA}}^{l}\mathbf{P}^{l}\mathbf{H}^{l,s}\|_2}
$$

其中 $l$ 为 VLM 块索引，$S$ 为序列长度，$\mathbf{H}^{l,s}$ 为第 $l$ 层第 $s$ 个 token 的输入表示。总蒸馏损失为所有块的均值：

$$
\mathcal{L}_{\mathrm{Distill}} = \frac{1}{N} \sum_{l=1}^{N} \mathcal{L}_{\mathrm{Distill}}^{l}
$$

同时，为维持遗忘知识的完整性，引入标准交叉熵保真度损失：

$$
\mathcal{L}_{\mathrm{CE}} = -\frac{1}{|\mathcal{D}_f|}\sum_{(\nu_i,t_i,a_i)}^{\mathcal{D}_f}\sum_{t=0}^{|a_i|}\log P(y_t^i|\nu_i,x_i,y_{<i}^i)
$$

最终优化目标联合二者，通过超参数 $\lambda$ 平衡知识转移与保真度：

$$
\mathcal{L}_{\mathrm{Total}} = \lambda \mathcal{L}_{\mathrm{Distill}} + (1-\lambda)\mathcal{L}_{\mathrm{CE}}
$$

消融实验（Table 2）证实：单独使用任一损失均不能充分释放性能，联合优化是必要条件。

### 模块三：算术删除（Arithmetic Deletion）

蒸馏完成后，LoRA 参数已编码了位于真空空间中的遗忘知识。通过简单的参数减法即可得到安全模型：

$$
\mathbf{W}_{\mathrm{unlearned}} = \mathbf{W}_{\mathrm{FFN}} - \mathbf{W}_{\mathrm{LoRA}} \cdot \mathbf{P}
$$

该操作仅修改 FFN 层权重，其余参数保持原样。由于 LoRA 参数被严格约束在真空空间中，减法操作不会对保留知识产生干扰——移除真空空间约束后，保留集准确率从 43.4 骤降至 36.6（Table 2），直接验证了正交约束是防止保留知识退化的关键机制。



## 实验与关键发现

### 核心瓶颈验证：传统反向训练破坏跨模态对齐

在深入主实验之前，VL-Eraser 首先通过探针实验验证了其核心动机——传统机器遗忘（MU）方法在多模态场景下的失败根源。如图1(d)所示，对经过反向训练“遗忘”后的模型分别使用纯文本探针（text-only probing）和重载原始投影（reloading original projection）进行测试，模型仍能暴露出大量残留知识。这一现象揭示了关键因果机制：传统方法并非真正消除知识，而是通过破坏视觉与语言模态之间的对齐来“掩盖”模型能力。这种对齐损伤导致遗忘不彻底，并留下严重的知识泄漏风险。VL-Eraser 的真空蒸馏-算术删除范式正是针对这一瓶颈设计，其目标是在保持跨模态对齐的前提下实现干净的知识剥离。

### 主实验结果：遗忘质量与模型效用的双重领先

**Table 1** 报告了在 MLLMU-Bench 基准上，5% 遗忘比例下各方法在两个代表性 VLM 骨干（LLaVA-1.5-7B 和 Qwen2-VL-7B-Instruct）上的综合表现。评估覆盖三个遗忘任务，结果按 Vision-QA 和 Textual-QA 分别呈现，并在遗忘集（Forget）、测试集（Test）、保留集（Retain）和名人集（Real）四个维度上进行衡量。

在遗忘质量方面，VL-Eraser 在两个骨干上均取得最低分类准确率。以 LLaVA-1.5 为例，其在 Vision-QA 和 Textual-QA 遗忘集上的分类准确率分别降至 **26.2** 和 **25.0**，相比原始模型平均下降约 24.1%；在完形填空任务上准确率下降 12.8%，ROUGE-L 分数下降 0.369。在 Qwen2-VL 骨干上，分类准确率平均下降 19.6%，ROUGE-L 下降 0.407。这一结果直接证明了 VL-Eraser 的遗忘彻底性远超基线方法。

在模型效用保持方面，VL-Eraser 在保留集和真实分布上的表现最接近原始模型。LLaVA-1.5 在 Vision-QA 和 Textual-QA 保留集上的分类准确率分别为 **43.4** 和 **46.2**，在所有方法中与原始模型差距最小。这表明真空空间约束有效防止了遗忘过程对保留知识的干扰。

**Figure 3** 进一步展示了不同遗忘比例下的遗忘-效用权衡曲线。以 LLaVA 为基座模型，x 轴表示遗忘集上相对于原始模型的性能差异（分类任务用准确率差，完形填空任务用 ROUGE-L 差），y 轴报告保留集和真实集上的模型效用。VL-Eraser 在所有遗忘比例下均位于 Pareto 前沿，在实现深度遗忘的同时维持了最高的保留效用，验证了该方法在不同遗忘强度下的鲁棒性。

### 消融实验：真空空间约束是性能关键

**Table 2** 报告了在 LLaVA-1.5-7B 上 5% 遗忘比例下的消融实验结果，系统验证了 VL-Eraser 各组件的作用。

移除真空空间约束（w/o Vacuum）后，保留集分类准确率从 **43.4 骤降至 36.6**，同时遗忘集性能也出现退化。这一剧烈退化直接证明了真空空间（左零空间）正交投影是防止蒸馏过程干扰保留知识的核心机制。没有这一约束，LoRA 在蒸馏遗忘知识时会不可避免地捕获保留集相关信息，导致参数减法阶段误删有用知识。

在损失函数层面，单独使用蒸馏损失（$L_{\text{Distill}}$ only）或交叉熵损失（$L_{\text{CE}}$ only）均无法充分释放 VL-Eraser 的性能。蒸馏损失负责将遗忘知识从冻结的 FFN 教师转移到 LoRA 学生，而交叉熵损失在遗忘集上维持输出保真度，确保被蒸馏的知识保持完整。二者联合优化（$L_{\text{Total}} = \lambda L_{\text{Distill}} + (1-\lambda) L_{\text{CE}}$）才能在知识转移与保真度之间取得平衡，实现最佳的遗忘-保留权衡。

### 效率与定性分析

**Figure 4** 对比了各方法在 LLaVA-1.5-7B 上 5% 遗忘设置下的训练耗时。由于 VL-Eraser 仅需在冻结的 FFN 层上训练低秩适配器（LoRA），参数量远小于全模型微调，其训练效率显著优于需要更新全部或大量参数的反向训练方法。

**Figure 5** 通过案例分析定性展示了遗忘前后的模型输出变化。在遗忘集样本上，原始模型能够准确回答与目标知识相关的问题，而经过 VL-Eraser 遗忘后的模型则无法给出正确答案，直观验证了知识删除的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/003_Table_1.jpg]]
*Table 1: Overall results of baselines and VL-Eraser on two representative VLMs backbones across three unlearning tasks (5% Forget). Results are presented separately for Vision-QA and Textual-QA and are evaluated on the forget set (Forget), test set (Test), retain set (Retain), and celebrity set (Real). ↓ indicates lower is better, and ↑ indicates higher is better. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/005_Table_2.jpg]]
*Table 2: Ablation study on MLLMU-Bench (5% Forget) using the LLaVA-1.5-7B model. Results are evaluated on the forget set (Forget), test set (Test), retain set (Retain), and celebrity set (Real). ↓ indicates lower is better, and ↑ indicates higher is better*

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/004_Figure_3.jpg]]
*Figure 3: The overall trade-off between unlearning effectiveness and model utility under varying forget ratios, using LLaVA as the base model. The x-axis shows the performance difference in forget set relative to the vanilla model, measured as the accuracy difference for classification tasks and the ROUGE-L difference for cloze tasks. The y-axis reports model utility on the Retained and Real sets*

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/007_Figure_4.jpg]]
*Figure 4: Training time of different unlearning methods on LLaVA-1.5-7B under the 5% forget setting.Q*

![[assets/figures/papers/paper_list_l2712_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_VL_Eraser_Vacuum/figures/006_Figure_5.jpg]]
*Figure 5: Case study on Forget Set before and after unlearning*



## 定位与知识库关联

### 1. 基线对比与范式差异

VL-Eraser 的核心贡献在于从“参数更新范式”跃迁到“知识蒸馏-删除范式”，其与现有机器遗忘基线的方法论差异体现在四个关键维度：

**遗忘范式**：传统方法普遍采用反向训练范式，即直接在遗忘集上最大化预训练损失的负值（**GA**，Thudi et al., EuroS&P 2022）或通过分布差异驱动遗忘（**KL-based Negative Optimization**，Nguyen et al., NeurIPS 2020；**NPO**，Zhang et al., CoLM 2024）。这类范式在多模态场景下的根本缺陷在于：反向梯度更新倾向于破坏视觉-语言跨模态对齐，而非真正消除目标知识。Figure 1(d) 的实验证据直接支撑了这一论断——仅通过纯文本探针或重载原始投影即可暴露出大量残留知识，表明遗忘主要来自对齐损伤而非知识删除。相比之下，VL-Eraser 将遗忘重构为“真空蒸馏→算术删除”两阶段过程，在正交于保留知识的空间中完成知识转移，再通过参数减法实现干净删除，从机制上规避了对齐破坏问题。

**训练损失**：基线方法的损失函数本质上是负的预训练损失 $\mathcal{L}_{unlearn} = -\sum_{(\nu_i,t_i;a_i)\in\mathcal{D}^f} \mathcal{L}_{pre-train}(\mathcal{M}_\theta(\nu_i,t_i,a_i))$，其优化方向与原始训练目标完全相反。VL-Eraser 则采用组合损失 $\mathcal{L}_{Total} = \lambda \mathcal{L}_{Distill} + (1-\lambda)\mathcal{L}_{CE}$，其中 $\mathcal{L}_{Distill}$ 在真空空间中匹配 FFN 教师输出与 LoRA 学生输出，$\mathcal{L}_{CE}$ 在遗忘集上维持下一词预测保真度，二者联合确保知识在蒸馏过程中保持完整且不干扰保留知识。

**参数更新范围**：传统方法通常对全模型参数或特定层进行反向梯度更新，导致遗忘效果与模型效用的耦合难以解耦。VL-Eraser 仅在 FFN 层插入的低秩适配器（LoRA）上进行蒸馏训练，原始参数全程冻结；遗忘通过从 FFN 参数中减去投影后的 LoRA 权重 $\mathbf{W}_{unlearned} = \mathbf{W}_{FFN} - \mathbf{W}_{LoRA} \cdot \mathbf{P}$ 实现，将遗忘操作与模型本体解耦。

**知识隔离约束**：基线方法缺乏专门的隔离机制，反向训练天然会干扰交叉模态对齐及其他知识。VL-Eraser 通过保留集图像特征的 SVD 分解构建真空空间投影矩阵 $\mathbf{P}$，强制满足 $Proj_{vacuum}(\mathbf{W}_{LoRA}) \cdot \mathbf{H}_r = 0$，使 LoRA 参数与保留集表示正交，天然过滤无关知识。消融实验（Table 2）证实，移除真空空间约束后保留集准确率从 43.4 骤降至 36.6，验证了正交约束是防止干扰保留知识的关键。

### 2. 多模态遗忘领域的定位

在多模态机器遗忘这一新兴方向上，VL-Eraser 与同期工作的关系如下：

- **CLIPErase**（Yang et al., arXiv 2024）专注于 CLIP 模型的视觉-文本关联遗忘，其作用域限于双塔架构的对比学习空间，难以泛化到 LLaVA 等基于 LLM 的视觉语言模型。VL-Eraser 通过在 LLM 的 FFN 层操作，天然适配主流 VLM 架构。
- **Multidelete**（Cheng and Amiri, ECCV 2024）面向多模态场景删除视觉-文本数据的影响，但其仍属于反向训练范式，面临对齐破坏的根本性瓶颈。VL-Eraser 的真空蒸馏机制提供了范式层面的替代方案。

从知识库定位角度，VL-Eraser 处于“参数高效微调（LoRA）+ 知识蒸馏 + 子空间投影”三条技术路线的交汇点。其真空空间构建借鉴了子空间方法中通过 SVD 获取正交基的思想，但将其创新性地应用于遗忘知识的隔离蒸馏，而非传统的特征解耦或模型编辑。这一设计使 VL-Eraser 在遗忘-效用权衡上显著优于所有对比基线：在 LLaVA-1.5-7B 上，遗忘集分类准确率降至 26.2（Vision-QA），同时保留集准确率保持 43.4，最接近原始模型效用（Table 1）。

### 3. 适用边界与局限

尽管 VL-Eraser 在实验设定下表现优异，其适用边界需审慎界定：

1. **对保留集质量的依赖**：真空空间的构建依赖保留集图像特征的 SVD 分解。若保留集不能充分覆盖模型应保留的知识分布，投影矩阵 $\mathbf{P}$ 可能无法有效过滤所有保留相关知识，导致遗忘过程中的知识泄漏或过度遗忘。论文未系统分析保留集规模与质量对真空空间完备性的影响，这一点需要手动验证。

2. **遗忘比例的扩展性**：Figure 3 展示了不同遗忘比例下的遗忘-效用权衡曲线，但实验仅覆盖至 5% 的遗忘比例。当遗忘集规模显著增大时，真空空间的维度约束与 LoRA 的表达容量是否构成瓶颈，尚缺乏理论分析或实验证据。

3. **架构泛化性**：实验验证限于 LLaVA-1.5-7B 和 Qwen2-VL-7B-Instruct 两个 VLM 骨干，二者均采用类似的视觉编码器-LLM 架构。对于其他 VLM 架构（如 BLIP-2 的 Q-Former 桥接、Flamingo 的门控交叉注意力），FFN 层的知识定位假设是否仍然成立，需要进一步验证。

4. **遗忘评估的完备性**：当前评估主要依赖分类准确率和 ROUGE-L 等任务指标，缺乏对“知识是否真正从模型参数中消失”的机制性验证。Figure 1(d) 的探针实验虽然揭示了传统方法的残留知识问题，但 VL-Eraser 自身是否在更严格的提取攻击（如模型反演、成员推理攻击）下仍能保证遗忘安全性，论文未涉及。

### 4. 开放问题

1. **真空空间的理论最优性**：当前真空空间通过 SVD 的启发式阈值截断构建，是否存在信息论意义上的最优正交子空间？真空维度与遗忘彻底性、模型效用之间的理论关系尚待建立。

2. **增量遗忘与知识冲突**：当多次执行遗忘操作时，不同遗忘集的真空空间可能存在重叠或冲突。如何设计增量遗忘机制，避免后序遗忘破坏前序遗忘结果，是实际部署中的关键问题。

3. **与模型编辑的关系**：VL-Eraser 的“蒸馏-删除”流程与模型编辑中的“定位-编辑”范式存在结构相似性。能否将真空蒸馏框架推广为通用的知识编辑工具，支持定向知识修改而非仅删除，值得探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/VL_Eraser_Vacuum_Distillation_for_Machine_Unlearning_in_Vision_Language_Models.pdf]]

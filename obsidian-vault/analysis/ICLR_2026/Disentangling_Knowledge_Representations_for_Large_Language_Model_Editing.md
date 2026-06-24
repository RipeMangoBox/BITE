---
title: "Disentangling Knowledge Representations for Large Language Model Editing"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Disentangling_Knowledge_Representations_for_Large_Language_Model_Editing.pdf
aliases:
- DKRLLME
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "通过知识表征解耦（KRD）模块将主题表征分解为目标知识相关与无关的独立成分，并在编辑时仅更新相关部分，同时显式约束无关部分不变。"
primary_logic: "解耦主题表征中不同关系下的语义，将编辑操作限制在与目标关系对应的子空间内，从而保护其他关系下的细粒度知识。"
claims:
- "现有方法在细粒度无关知识上的保持性显著低于粗粒度知识。"
- "DiKE 在 FINE-KED 基准上将细粒度知识保持性（Relational Locality）平均相对提升 8.3%（GPT2-XL）、8.2%（GPT-J）和 6.5%（LLaMA-3）。"
- "消融实验表明，移除 KRD 的对比损失或知识约束损失会显著降低 Relational Locality，验证了解耦组件的有效性。"
- "FINE-KED (GPT2-XL) 上 Relational Locality Avg. = 55.0"
---

# Disentangling Knowledge Representations for Large Language Model Editing

> [!tip] 核心洞察
> 解耦主题表征中不同关系下的语义，将编辑操作限制在与目标关系对应的子空间内，从而保护其他关系下的细粒度知识。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向大语言模型编辑的知识表征解耦 |
| 英文题名 | Disentangling Knowledge Representations for Large Language Model Editing |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PmRBeF2umZ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | DiKE |
| Dataset | FINE-KED (GPT2-XL), FINE-KED (GPT-J), FINE-KED (LLaMA-3), COUNTERFACT (GPT2-XL) |

> [!tip] 效果简介
> - FINE-KED (GPT2-XL) 上，Relational Locality Avg. 为 55.0，对比 50.8 (ROME-C)，变化 +8.3% (relative)。
> - FINE-KED (GPT-J) 上，Relational Locality Avg. 为 71.3，对比 65.9 (MEMIT-C)，变化 +8.2% (relative)。
> - FINE-KED (LLaMA-3) 上，Relational Locality Avg. 为 70.6，对比 66.3 (MEMIT-C)，变化 +6.5% (relative)。

## 概述

当前针对大语言模型（LLM）的知识编辑方法在更新知识时，会意外损害与目标知识共享同一主题但关系不同的**细粒度无关知识**，因为这类知识在模型表征空间中高度纠缠（Figure 1）。为解决这一瓶颈，本文提出 **DiKE（Disentangling Knowledge representations for LLM Editing）**：一种先解耦后编辑的定位—编辑方法。其核心思路是通过**知识表征解耦模块（KRD）**将主题表征分解为与目标知识相关和不相关的独立子空间，并在编辑阶段（DKE）仅对相关子空间施加扰动以注入新知识，同时显式约束不相关分量保持不变，从而保护其他关系下的细粒度知识。

主要结果如下：
- 在细粒度知识编辑基准 **FINE-KED** 上，DiKE 的 Relational Locality（细粒度保持性）平均相对提升 **8.3%**（GPT2-XL）、**8.2%**（GPT-J）和 **6.5%**（LLaMA-3），显著优于包括 MEMIT、ROME 变体及 AlphaEdit 在内的基线方法（Table 2）。
- 在一般编辑基准 **COUNTERFACT** 上，DiKE 仍保持竞争性表现（GPT2-XL 上 Avg. 87.7，与最优 AlphaEdit 接近；Table 3）。
- 消融实验证实：移除对比损失或知识约束损失将导致细粒度保持性骤降；直接编辑原始表征会使其编辑效能崩溃（Figure 3）；显式约束不相关分量不变性可进一步缓解困难关系下的干扰。

DiKE 提供了一种基于闭式秩一更新的高效编辑方式，在不牺牲编辑效果的前提下显著提升对细粒度无关知识的保护，为知识编辑中的“副作用”问题提供了新的解决思路。

## 背景与动机

知识编辑旨在对大型语言模型（LLM）中已存储的事实性知识进行精准修改，同时保持模型在无关知识上的行为不变。然而，现有方法在评估其破坏性时，通常只关注粗粒度的无关知识（例如与编辑目标完全不相关的Wikipedia段落），却忽视了细粒度无关知识——即与目标知识共享同一主题但关系不同的知识（Figure 1所示）。这种忽略造成了重要的安全漏洞：当用户编辑一个主题的某条知识时，可能会意外地改变模型对于同一主题在其他关系下的精细记忆，从而引入新的错误。

我们对当前主流编辑方法的分析证实了这一缺口。如 Figure 1(a) 所展示，所有评估方法在细粒度无关知识上的保持性均显著低于在粗粒度无关知识上的表现。这一差异揭示了现有编辑技术的一个关键瓶颈：**当模型更新某个三元组 (s, r, o) 时，其表征空间中与主题 s 相关联的不同关系语义高度纠缠，导致编辑信号不可避免地泄漏到无关的关系表征中**，从而损害了模型对于 (s, r', o') 等细粒度无关知识的记忆。诸如 ROME、MEMIT、AlphaEdit 等代表性方法，在修改 FFN 权重时，其目标值计算与参数更新均直接作用于原始主题表征，未对不同关系下的语义子空间加以区分。这构成了现有方法的核心能力缺口：**缺乏一种机制，能够在编辑过程中将目标知识相关的表征与无关的表征解耦，并仅对相关部分施加干预**。

正是基于这一观察，我们提出了 **DiKE（Disentangling Knowledge Representations for LLM Editing）** 框架。DiKE 的核心动机在于：**通过在编辑前显式地将主题表征分解为目标知识相关与无关的独立成分，将编辑操作限制在相关子空间，并在更新过程中施加无关成分的不变性约束**，从而实现精准的知识注入与细粒度无关知识保护之间的平衡。具体而言，DiKE 引入了**知识表征解耦模块（KRD）**，利用对比学习与知识一致性损失，将主题和关系表征映射到目标相关向量 $\mathbf{z}_e^r$ 与不相关向量 $\mathbf{z}_e^u$。在后续的**解耦知识编辑阶段（DKE）**，DiKE 仅优化 $\mathbf{z}_e^r$ 上的扰动来编码新知识，并显式要求更新后的 $\mathbf{z}_e^u$ 不变，从而避免对邻居细粒度知识的干扰。这一设计从根本上改变了现有方法“在纠缠空间中操作”的范式，转而**在解耦后的结构化子空间中进行最小化干预**。

综上，本文的动机源于当前知识编辑技术在细粒度无关知识保持上的不足，目标是设计一种能明确分离主题表征中不同关系语义的框架，使得知识更新既高效又具有局部性，为安全可靠的 LLM 编辑提供新的解决路径。

## 核心创新

当前知识编辑方法的根本瓶颈在于，模型表征空间中与目标知识共享同一主题但关系不同的细粒度知识高度纠缠，导致编辑操作在注入新三元组 $(s, r^*, o^*)$ 的同时，意外破坏了其他关系 $r'$ 下关于同一主题 $s$ 的细粒度事实（Figure 1(a)）。这暴露了传统“定位-编辑”范式的核心缺陷：它们仅以主题最终残差流表征为操作单位，缺乏对不同关系下语义的区分能力，从而无法隔离编辑的副作用。

DiKE 的关键认知突破在于**将编辑从粗糙的主题层面下沉到关系条件化的子空间层面**：先解耦（disentangle）主题表征中目标关系相关和无关的成分，再仅对相关成分施加扰动，并显式约束无关成分的不变性。这一思路通过两个互补机制实现，形成了相对于强基线（ROME、MEMIT、AlphaEdit 等）的三个根本性 changed slots。

**Changed Slot 1：目标值 $v_*$ 的计算方式（从表征直接优化到解耦扰动优化）**  
ROME 与 MEMIT 通过直接优化 FFN 的输入键 $k_*$ 对应的期望输出 $v_*$ 来注入知识（Eq. (3)–(4)），其优化目标为最大化编辑后模型在目标对象上的概率。DiKE 则不再直接操作原始表征，而是先利用冻结的 KRD（Knowledge Representation Disentanglement）模块获取主题 $s$ 与目标关系 $r^*$ 的相关表征 $\mathbf{z}_e^r$ 和无关表征 $\mathbf{z}_e^u$；**仅在相关表征上学习一个扰动 $\boldsymbol{\delta}$**，使得通过 Recomposer 恢复出的主题表征 $\mathbf{h}_s^* = \operatorname{Rec}(\mathbf{z}_e^r + \boldsymbol{\delta}, \mathbf{z}_e^u)$ 可准确预测目标对象 $o^*$（Eq. (13)–(15)），再基于残差计算编辑所需的目标值 $v_* = \mathbf{h}_s^* - \mathbf{h}_s^p$。该 slot 的变更将编辑操作**限制在关系特异性子空间内**，从源头避免了对无关关系子空间的扰动。消融实验中移除目标知识编辑（即直接用原始表征计算 $v_*$）会导致编辑成功率（Efficacy）骤降（Figure 3），证实了在解耦相关分量上进行注入的必要性。

**Changed Slot 2：细粒度无关知识保持约束（从粗粒度保持到解耦不变性约束）**  
传统的秩一编辑基线仅通过一个对角加权的键值集合 $(\mathbf{K}_0, \mathbf{V}_0)$（来自 Wikipedia 文本）保持粗粒度无关知识，其约束为 $\min \|\hat{\mathbf{W}} \mathbf{K}_0 - \mathbf{V}_0\|_F^2$（Eq. (4)）。DiKE 在此之上**引入基于解耦无关表征的不变性正则项**（Eq. (16)–(17)），显式要求编辑前后 KRD 的无关分支 $\mathrm{Dis}_u$ 对于所有保留样本 $(\mathbf{h}_{s_i}^p, \mathbf{h}_{r_i})$ 的输出保持一致，即 $\|\mathrm{Dis}_u(\mathbf{h}_{s_i}^p + \hat{\mathbf{W}} \mathbf{k}_i, \mathbf{h}_{r_i}) - \mathrm{Dis}_u(\mathbf{h}_{s_i}^p, \mathbf{h}_{r_i})\|_F^2$。这一约束直接对应了“细粒度无关知识不变量”的语义，比仅维持残差流统计量的方法更能抑制跨关系干扰。消融实验中移除该约束（w/o FIK）尤其使 **Hard** 难度的 Relational Locality 下降（Figure 3），验证了其在困难关系干扰下的关键作用。

**Changed Slot 3：参数更新闭式解的形式（从简单秩一更新到结构化正则注入）**  
在上述新约束下，DiKE 总损失可写为联合目标注入、粗粒度保持和细粒度不变性三项的矩阵最小二乘问题（Eq. (18)）。通过矩阵推导，最终权重更新公式从经典 MEMIT 的 $\Delta_{\text{MEMIT}} = (\mathbf{v}_* - \mathbf{W} \mathbf{k}_*) \mathbf{k}_*^T (\mathbf{K}_0 \mathbf{K}_0^T + \mathbf{k}_* \mathbf{k}_*^T)^{-1}$ 变为 **$\hat{\mathbf{W}} = \mathbf{W} + (\mathbf{W}_3^T \mathbf{W}_3 + \mathbf{E})^{-1} \Delta_{\text{MEMIT}}$**（Eq. (19)）。这里 $\mathbf{W}_3$ 来自 KRD 解耦器的无关分支线性映射，$\mathbf{E}$ 为单位矩阵。该因式相当于在标准秩一更新前施加了一个由解耦器编码的结构化正则项，使得参数修改沿“不破坏无关子空间”的方向进行。此闭式解保证了编辑的高效性（无需对每个样本重新训练解耦器），且使 DiKE 在批量编辑下依然保持领先的细粒度保持性（Figure 4）。

**创新点的因果链与证据汇流**  
上述三个 slots 构成一条紧密的因果链：解耦→子空间扰动→不变性约束→结构化更新。其实证效果汇聚在 **FINE-KED 基准** 上：DiKE 在 GPT2-XL、GPT-J、LLaMA-3 上分别将细粒度保持性指标 Relational Locality 平均相对提升 **8.3%、8.2% 和 6.5%**（Table 2），同时保持编辑成功率（Efficacy）近乎 100%。消融实验进一步将增益归因于解耦组件的核心角色——移除 KRD 的对比损失（w/o CTR）或知识约束损失（w/o KC）会使 Relational Locality 大幅下降（Figure 3），说明无监督解耦与基于关系预测的约束正是实现语义分离、从而避免附带损害的本质驱动因素。同时，DiKE 在传统 COUNTERFACT 基准上保持竞争性能（Avg. 87.7–92.4，与 AlphaEdit 可比，Table 3），证明该创新在提升细粒度保持性的同时未牺牲通用编辑能力。

## 整体框架

![[assets/figures/papers/iclr26_0014_PmRBeF2umZ_Disentangling_Knowledge_Representations_for_Larg/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the DiKE architecture. The framework operates in two distinct phases. (Left) KRD Training: The module extracts subject and relation representations from the LLM and learns to disentangle them into target-knowledge-related and -unrelated components via optimizing disentanglement, constraint, and reconstruction objectives. (Right) DKE Editing: During the editing phase, the pre-trained Disentangler is frozen. The DKE module utilizes the disentangled representations to derive a closed-form rank-one parameter update (Eq. (19)), which injects new knowledge into the target-related component while explicitly constraining the unrelated component to preserve fine-grained irrelevant knowle...*

DiKE 的整体 pipeline 由两个解耦且协同的阶段构成：**知识表征解耦（KRD）训练阶段**和**基于解耦的知识编辑（DKE）执行阶段**，如 图2 所示。其核心设计原则是：将主题表征中被不同关系打结的语义拆分成目标知识相关与目标知识无关的独立分量，从而在更新模型参数时把编辑操作限制在与目标关系对应的子空间内，显式保护其他关系下的细粒度事实。

### 1. 知识表征解耦（KRD）训练阶段
此阶段用于获得可复用的解耦与重构工具，一次训练后即可冷藏在后续任意编辑中直接调用，无需逐样本重训。

- **输入**：从 LLM 中间层提取的**主题表征** $\mathbf{h}_s$ 与**关系表征** $\mathbf{h}_r$。
- **Disentangler（解耦器）**：由两个并行的子模块 $\mathrm{Dis}_r$ 和 $\mathrm{Dis}_u$ 组成，它们分别将 $\mathbf{h}_s$ 和 $\mathbf{h}_r$ 映射为**目标知识相关分量** $\mathbf{z}_e^r$ 和**目标知识无关分量** $\mathbf{z}_e^u$（参见 Eq. (5)）。
- **Recomposer（重构器）** $\mathrm{Rec}$：以 $\mathbf{z}_e^r$ 和 $\mathbf{z}_e^u$ 为输入，重建原始主题表征 $\mathbf{h}_s$（参见 Eq. (6)），保证解耦过程无信息丢失。
- **训练目标**：联合优化三个损失项（Eq. (11)）：
  - **对比损失** $\mathcal{L}_{ctr}$：最大化 $\mathbf{z}_e^r$ 与 $\mathbf{h}_s$ 的互信息，同时将 $\mathbf{z}_e^u$ 与 $\mathbf{z}_e^r$ 推向分离，迫使两个分量各自包含关系特异性语义（Eqs. (7)-(8)）。
  - **知识约束损失** $\mathcal{L}_{con}$：强制 $\mathbf{z}_e^r$ 能独立预测原三元组的客体 $o$，而 $\mathbf{z}_e^u$ 能独立预测与同一主题相关的其他（非目标）关系的客体，从而将关系信号注入分量（参见 Eq. (9)）。
  - **重构损失** $\mathcal{L}_{recon}$：保证解耦‑重构循环的保真度。

完成训练后，$\mathrm{Dis}_r$、$\mathrm{Dis}_u$ 和 $\mathrm{Rec}$ 被冻结，构成后续编辑的固定功能模块。

### 2. 基于解耦的知识编辑（DKE）执行阶段
在此阶段，给定待编辑的知识三元组 $(s, r, o^*)$ 以及需要保持的粗粒度与细粒度无关知识集合，DiKE 通过修改某个临界 FFN 层的输出权重 $\mathbf{W}_{out}$ 来注入新知识，同时最小化对无关事实的扰动。

- **表征前处理**：对于待编辑的主题‑关系对，首先利用冻结的 KRD 解耦器获取当前表征上的相关分量 $\mathbf{z}_e^r$ 与无关分量 $\mathbf{z}_e^u$。
- **目标值计算**（与 MEMIT 系基线的主要差异）：传统方法直接在原始 $\mathbf{h}_s$ 上优化 FFN 输出以得到理想值 $\mathbf{v}^*$；DiKE 改为在解耦后的**相关分量**上学习一个扰动 $\delta$，通过 $\mathbf{h}_s^* = \operatorname{Rec}(\mathbf{z}_e^r + \delta, \mathbf{z}_e^u)$ 获得更新后的主题表征，随后基于 $\mathbf{h}_s^*$ 计算出对应于 $o^*$ 的目标值 $\mathbf{v}^*$（Eqs. (13)-(15)）。这一过程确保新知识仅通过“相关子空间”注入，从结构上阻断对无关语义的干扰。
- **多层级保持约束**：编辑的优化目标（Eq. (18)）同时包含三项约束：
  1. **目标知识注入**：$\|\hat{\mathbf{W}}\mathbf{k}_* - \mathbf{v}_*\|^2$，确保新事实能被正确回忆；
  2. **粗粒度无关知识保持**：$\|\hat{\mathbf{W}}\mathbf{K}_0 - \mathbf{V}_0\|_F^2$，通过 Wikipedia 文本中的键值对维护宏观事实；
  3. **细粒度无关知识保持（FIK）**：$\|\mathbf{W}_3(\hat{\mathbf{W}}\mathbf{k}_* - \mathbf{v}_0)\|_F^2$，这是 DiKE 独有的不变性项，它显式要求编辑前后 $\mathrm{Dis}_u$ 的输出保持一致（Eqs. (16)-(17)），从而保护与目标共享同一主题但不同关系的细粒度知识。
- **闭式参数更新**：通过对上述带约束的最小二乘问题求解析解，DiKE 导出了一个修正的秩一更新公式（Eq. (19)）：
  $$\hat{\mathbf{W}} = \mathbf{W} + (\mathbf{W}_3^T \mathbf{W}_3 + \mathbf{E})^{-1} \Delta_{\text{MEMIT}},$$
  其中 $\Delta_{\text{MEMIT}}$ 为传统 MEMIT 的原始更新量，$(\mathbf{W}_3^T \mathbf{W}_3 + \mathbf{E})^{-1}$ 自动编码了无关分量不变性对参数空间的投影约束。这一闭式解使得 DiKE 在实现编辑的同时，无需对每个样本进行反复迭代优化，保持计算效率。

### 3. 整体数据流与模块关系
从端到端视角，DiKE 的输入为待编辑三元组 $(s, r, o^*)$ 以及冻结的 LLM 和 KRD 模块，输出为修改后的目标层 FFN 权重 $\hat{\mathbf{W}}$。数据流可概括为：

1. **嵌入提取**：LLM 快照后得到主题表征 $\mathbf{h}_s$ 与关系表征 $\mathbf{h}_r$。
2. **解耦**：$\mathbf{h}_s, \mathbf{h}_r \xrightarrow{\mathrm{Dis}_r, \mathrm{Dis}_u} \mathbf{z}_e^r, \mathbf{z}_e^u$。
3. **扰动与重构**：$\mathbf{z}_e^r + \delta \xrightarrow{\mathrm{Rec}} \mathbf{h}_s^*$ ↔ 计算 $\mathbf{v}^*$，同时 $\mathbf{z}_e^u$ 用于 FIK 约束项。
4. **权重更新**：利用 $\mathbf{v}^*$ 和 FIK 约束构造修正方程，通过闭式解一次性更新 $\mathbf{W}_{out}$。

这种设计将知识编辑的因果干预严格限制在与目标关系对应的表征子空间内，从而在保证编辑效力（Efficacy）的同时，显著提升了对细粒度无关知识的保持度（Relational Locality）。

## 核心模块与公式推导

DiKE 框架由两个核心模块构成：**知识表征解耦模块 (KRD)** 的训练阶段，以及在此基础上进行的 **基于解耦的知识编辑模块 (DKE)**。KRD 负责将主题表征分解为目标相关与无关的独立成分；DKE 则利用冻结的 KRD，仅在目标相关子空间施加扰动，并显式约束无关子空间不变，从而在更新知识的同时保护细粒度无关知识。图 2 给出了整体架构。

### 1. 知识表征解耦 (KRD)

给定主题表征 $\mathbf{h}_s$ 与关系表征 $\mathbf{h}_r$（均从 LLM 的指定层抽取），解耦器（Disentangler）将它们映射为两个独立向量：

$$
\mathbf{z}_e^r = \mathrm{Dis}_r(\mathbf{h}_s, \mathbf{h}_r) = f(\mathbf{W}_1 \mathbf{h}_s + \mathbf{W}_2 \mathbf{h}_r),\qquad
\mathbf{z}_e^u = \mathrm{Dis}_u(\mathbf{h}_s, \mathbf{h}_r) = f(\mathbf{W}_3 \mathbf{h}_s + \mathbf{W}_4 \mathbf{h}_r)
\tag{5}
$$

其中 $\mathbf{W}_1,\mathbf{W}_2,\mathbf{W}_3,\mathbf{W}_4$ 为可学习权重，$f$ 为激活函数。$\mathbf{z}_e^r$ 捕获与目标关系（待编辑或待查询的关系）直接相关的语义，$\mathbf{z}_e^u$ 则保留与目标关系无关但属于同一主题的其他关系语义。重构器 (Recomposer) $\operatorname{Rec}(\cdot,\cdot)$ 负责由 $\mathbf{z}_e^r,\mathbf{z}_e^u$ 恢复原始主题表征（见原文 Eq. 6），保证信息无失真。

为保证解耦质量，KRD 通过三项联合损失进行训练：

1. **对比损失** $\mathcal{L}_{ctr}$ 最大化各分量与主题表征的互信息，同时迫使两分量彼此分离：

$$
\mathcal{L}_{ctr} = \mathrm{InfoNCE}(\mathbf{z}_e^r, \mathbf{h}_s, [\mathbf{z}_e^u; \mathbf{H}_s]) \;+\; \mathrm{InfoNCE}(\mathbf{z}_e^u, \mathbf{h}_s, [\mathbf{z}_e^r; \mathbf{H}_s])
\tag{7,8}
$$

其中 $\mathbf{H}_s$ 为同一批次中其他样本的主题表征集合，用于构造负样本。

2. **知识约束损失** $\mathcal{L}_{con}$ 要求 $\mathbf{z}_e^r$ 直接输入 FFN 后能准确预测目标对象，而 $\mathbf{z}_e^u$ 能保持同一主题下其他关系的知识。该损失确保分量语义与关系预测行为对齐。

3. **重构损失** $\mathcal{L}_{recon}$ 要求重构器输出的表征与原始 $\mathbf{h}_s$ 一致，常采用均方误差。

总损失为：

$$
\mathcal{L} = \mathcal{L}_{ctr} + \alpha \mathcal{L}_{con} + \beta \mathcal{L}_{recon}
\tag{11}
$$

其中 $\alpha,\beta$ 为平衡超参数。消融实验表明，移除对比损失或知识约束损失会导致细粒度知识保持性（Relational Locality）大幅下降（Figure 3），验证了该解耦设计的重要性。

### 2. 基于解耦的知识编辑 (DKE)

编辑阶段冻结 KRD 参数，对每条需要注入的新事实 $(s, r, o^*)$，流程如下。

**Step 1: 通过表征扰动编码目标知识。** 保持 $\mathbf{z}_e^u$ 不变，仅在 $\mathbf{z}_e^r$ 上叠加可学习扰动 $\delta$，使得重构后的主题表征能够最大化目标对象的概率：

$$
\mathbf{h}_s^* = \operatorname{Rec}(\mathbf{z}_e^r + \delta,\; \mathbf{z}_e^u)
\tag{13}
$$
$$
\delta = \arg\min_{\delta} -\log P_{F(\mathbf{h}_s:=\mathbf{h}_s^*)}[o^* \mid p(s,r)]
\tag{14,15}
$$

求得最优 $\delta$ 后，对应的 FFN 输出值即为编辑所需的目标向量 $\mathbf{v}_*$。

**Step 2: 编辑 FFN 权重。** 采用与 MEMIT 类似的键值注入范式，但额外引入细粒度无关知识不变约束。设编辑层 FFN 的原始输出权重为 $\mathbf{W}$，待更新的权重为 $\hat{\mathbf{W}}$，$\mathbf{k}_*$ 为键向量，$\mathbf{K}_0,\mathbf{V}_0$ 为模型已存储的粗粒度知识键值矩阵，$\mathbf{v}_0 = \mathbf{W}\mathbf{k}_*$ 为原始输出，则编辑目标为：

$$
\hat{\mathbf{W}} = \arg\min_{\hat{\mathbf{W}}} \left(
\|\hat{\mathbf{W}}\mathbf{k}_* - \mathbf{v}_*\|^2
+ \|\hat{\mathbf{W}}\mathbf{K}_0 - \mathbf{V}_0\|_F^2
+ \|\mathbf{W}_3(\hat{\mathbf{W}}\mathbf{k}_* - \mathbf{v}_0)\|_F^2
\right)
\tag{18}
$$

三项依次表示：
- **目标注入**：确保新事实能在 FFN 输出中体现；
- **粗粒度知识保持**：保持已记忆的大量通用知识；
- **细粒度无关知识保持**：通过解耦器 $\mathrm{Dis}_u$ 中使用的投影矩阵 $\mathbf{W}_3$，强制编辑前后在无关子空间上的投影保持一致，从而保护共享主题的其他关系知识。

**Step 3: 闭式更新。** 通过对 (18) 式求解，得到秩一的权重更新：

$$
\hat{\mathbf{W}} = \mathbf{W} + (\mathbf{W}_3^T \mathbf{W}_3 + \mathbf{E})^{-1} \Delta_{\mathrm{MEMIT}}
\tag{19}
$$

其中

$$
\Delta_{\mathrm{MEMIT}} = (\mathbf{v}_* - \mathbf{W}\mathbf{k}_*) \mathbf{k}_*^T (\mathbf{K}_0 \mathbf{K}_0^T + \mathbf{k}_* \mathbf{k}_*^T)^{-1}
$$

是标准 MEMIT 的秩一更新项；$\mathbf{E}$ 为由细粒度不变约束导出的正则化矩阵。相比 MEMIT，新增的 $(\mathbf{W}_3^T \mathbf{W}_3 + \mathbf{E})^{-1}$ 因子相当于在无关子空间的方向上对更新幅度进行选择性抑制，从而以闭式、高效的方式实现了对细粒度知识的显式保护。消融实验 (Figure 3) 中移除细粒度不变约束后，Hard 级别的 Relational Locality 显著下降，证实了该闭式约束的有效性。

## 实验与分析

DiKE 的核心目标是在保证编辑成功率（Efficacy）的同时，显著提升对被编辑三元组共享主题但关系不同的细粒度无关知识的保持性（Relational Locality）。实验在 FINE-KED（新建的细粒度知识编辑基准）、COUNTERFACT 以及 MQUAKE-3K 上展开，涵盖 GPT2-XL、GPT-J 和 LLaMA-3 三个规模的模型，评测指标包括 Efficacy、Relational Locality（按 Easy/Middle/Hard 等级划分）、Paraphrase 和 Neighborhood 分数。所有基线方法（FT、MEND、ROME、MEMIT、AlphaEdit 及加入关系约束的 ROME-C、MEMIT-C）均按统一协议调参或使用官方实现。

### 主结果：细粒度保持的大幅提升

在 FINE-KED（Table 2）上，DiKE 在三个模型上的 Relational Locality 平均分数均显著优于现有最优方法：
- 在 GPT2-XL 上，Relational Locality 平均达到 55.0%，相对最强基线 ROME-C（50.8%）提升 8.3%；
- 在 GPT-J 上，达到 71.3%，相对 MEMIT-C（65.9%）提升 8.2%；
- 在 LLaMA-3 上，达到 70.6%，相对 MEMIT-C（66.3%）提升 6.5%。

![[assets/figures/papers/iclr26_0014_PmRBeF2umZ_Disentangling_Knowledge_Representations_for_Larg/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on FINE-KED in terms of Efficacy (%) and Relational Locality (%). The best performance is highlighted in boldface, and the second-best is underlined*

与此同时，所有方法的 Efficacy 均维持在 96% 以上，DiKE 的编辑成功率与基线持平甚至更优（如 GPT2-XL 上 97.4%），说明细粒度保持的提升并未牺牲目标知识的正确注入。值得注意的是，困难等级（Hard）的 Relational Locality 普遍较低，但 DiKE 在该等级上仍获得了可观的绝对提升（例如 GPT2-XL 上从 35.6% 到 41.0%），表明解耦编辑机制对高度纠缠的关系干扰具有缓解作用。

在传统的 COUNTERFACT 基准（Table 3）上，DiKE 表现与最优方法 AlphaEdit 接近（GPT2-XL 平均 87.7 vs. 88.3，GPT-J 平均 92.4 vs. 92.7），证明该方法不会损害一般编辑任务的综合性能。

### 消融实验：解耦组件的因果贡献

为验证 Knowledge Representation Disentanglement (KRD) 各模块及编辑约束的实际作用，论文在 Figure 3（GPT2-XL）和 Figure 8（GPT-J）上报告了四项关键消融（原文标记为 w/o CTR、w/o KC、w/o TKE、w/o FIK）：

![[assets/figures/papers/iclr26_0014_PmRBeF2umZ_Disentangling_Knowledge_Representations_for_Larg/figures/005_Figure_3.jpg]]
*Figure 3: Ablation studies on FINE-KED in terms of Efficacy and Relational Locality*

1. **移除对比损失（w/o CTR）**：Relational Locality 出现大幅下降（尤其在 Middle/Hard 等级），验证了对比学习在分离相关与不相关表征子空间中的核心作用。缺乏这一约束时，编辑操作更容易侵入共享主题的其他关系表示。
2. **移除知识约束损失（w/o KC）**：进一步损害细粒度知识的保持性，且 Efficacy 也出现轻微下降，说明仅靠对比损失不足以使不相关表征完全与目标关系解耦，知识约束对确保 Dis\_u 输出正确映射至无关事实至关重要。
3. **移除目标知识编辑（w/o TKE，即直接在原始表征上优化编辑）**：Efficacy 骤降（降幅超过 30 个百分点），Relational Locality 也受损。这直接证明了在解耦后的 *相关分量*（$\mathbf{z}_e^r$）上施加扰动 δ（Eq. 13-15）是成功注入新知识的必要条件——原始表征中的多维纠缠会导致优化方向混乱。
4. **移除细粒度无关知识不变约束（w/o FIK）**：即去掉编辑损失中的 $\|\mathbf{W}_3(\hat{\mathbf{W}}\mathbf{k}_*-\mathbf{v}_0)\|_F^2$ 项（Eq. 18）。该消融导致 Hard 级别的 Relational Locality 进一步降低，表明显式约束不相关表征在编辑前后的输出一致性，能有效压制困难关系（语义高度相近的关系）的潜在泄漏。

### 批量编辑与鲁棒性

在主题一致的批量编辑场景下（Figure 4），DiKE 在不同 batch size（1, 2, 4, 8）下始终保持最高的 Relational Locality，且 Efficacy 接近 100%，而 ROME、MEMIT 等方法的保持性随批量增大呈明显衰减。结合闭式更新公式 $\hat{\mathbf{W}} = \mathbf{W} + (\mathbf{W}_3^T\mathbf{W}_3 + \mathbf{E})^{-1} \Delta_{\mathrm{MEMIT}}$（Eq. 19）的低秩约束，DiKE 能够在不累积过多干扰的前提下同时处理多条编辑，为实际应用中持续更新大模型提供了稳定基础。

![[assets/figures/papers/iclr26_0014_PmRBeF2umZ_Disentangling_Knowledge_Representations_for_Larg/figures/006_Figure_4.jpg]]
*Figure 4: Performance of subject-consistent batch editing on the FINE-KED*

### 失败模式与局限

尽管 DiKE 在细粒度关系保持上取得了显著进展，其设计仍存在固有局限，在实验设计与结论解读中需特别指出：

- **知识形式的依赖**：整个方法建立在知识表示被解构为三元组 $(s, r, o)$ 的前提下；对于非结构化知识或需修改指代、事件链等非关系型知识的编辑任务，KRD 与 DKE 均无法直接适用。这一限制在论文的 Limitations 部分明确提及，且当前实验未覆盖此类场景。
- **无关知识的覆盖范围**：FINE-KED 仅关注“与被编辑知识共享同一主题”的细粒度无关知识，未考虑其他形式的干扰（例如共享同一关系但不同主题的知识、多跳知识链的级联影响）。因此，DiKE 在更广意义上的无关知识保护能力仍有待拓展。
- **数据与评测的规模**：FINE-KED 共包含约 3,000 条编辑样本（Table 4），覆盖关系种类有限；随着基准规模的扩大和更复杂关系的引入，解耦表征的泛化能力及不变约束的有效性还需进一步验证。在 OOD 关系上的初步评估（Table 11）显示 DiKE 在 Rel-ID/Rel-OOD 等设置下仍有优势，但置信度较低，建议研究者参照原文详细检查该表的具体数值与实验条件。

整体而言，实验结果强有力地证明：通过将主题表征显式解耦为目标知识相关与不相关的分量，并仅对相关分量施加编辑、同时约束不相关分量不变，可以从机理上缓解大模型编辑中细粒度知识的灾难性遗忘。该方法的主要代价在于需预先训练 KRD 模块，但其一次训练、多次使用的策略已通过批量编辑和不同模型上的优异表现展示了实际可行性。

### 补充图表

![[assets/figures/papers/iclr26_0014_PmRBeF2umZ_Disentangling_Knowledge_Representations_for_Larg/figures/001_Figure_1.jpg]]
*Figure 1: Knowledge editing can unintentionally affect fine-grained irrelevant knowledge. Figure (a): Preservation performance on fine-grained vs. coarse-grained irrelevant knowledge. Figure (b): Illustration of knowledge editing can unintentionally affect fine-grained irrelevant knowledge*

![[assets/figures/papers/iclr26_0014_PmRBeF2umZ_Disentangling_Knowledge_Representations_for_Larg/figures/013_Table_9.jpg]]
*Table 9: Performance comparison in terms of Efficacy Score (%), Paraphrase Score (%), and Neighborhood Score (%). The Avg. (%) is the harmonic mean of the three evaluation metrics*

## 方法谱系与知识库定位

### 与现有编辑方法的关系与演化路径

当前主流的模型编辑方法（ROME、MEMIT、AlphaEdit 等）均遵循“定位‑编辑”范式，通过在 FFN 中注入键值对来更新单一事实。但这些方法在设计上仅保护粗粒度的无关知识，忽视了表征空间中高度纠缠的**细粒度无关知识**：共享同一主题但关系不同的事实，在更新某一关系时极易被意外覆盖（Figure 1(a)）。这一瓶颈源于现有方法缺乏对主题表征不同语义维度的分离，导致编辑信号的扩散无法控制。

DiKE 在该方法谱系中的定位是**表征解耦增强的定位‑编辑**。它并未推翻原有框架，而是引入两项关键修正：

- **目标值计算方式**：  
  基线（如 MEMIT）直接基于原始主题表征优化 FFN 输出以得到 $\mathbf{v}^*$；  
  DiKE 则先通过知识表征解耦获得目标知识相关分量 $\mathbf{z}_e^r$，并在该子空间内优化扰动 $\delta$，再重构主题表征 $\mathbf{h}_s^*$ 并计算 $\mathbf{v}^*$（Eq. (13)‑(15)）。这一改动将编辑操作限制在与目标关系对应的低维子空间内，从根本上减少了跨关系干扰。

- **细粒度保持约束**：  
  基线仅利用 Wikipedia 中的键值对 $(\mathbf{K}_0,\mathbf{V}_0)$ 保持粗粒度无关知识；  
  DiKE 额外引入基于解耦不相关分量 $\mathbf{z}_e^u$ 的不变性约束（Eq. (16)‑(17)），显式要求编辑前后 $\mathrm{Dis}_u$ 输出一致。这相当于在参数更新中加入了一个“无关语义保持器”，直接压制了对共享主题其他关系的扰动。

在参数更新层面，DiKE 通过对 MEMIT 更新公式的矩阵修正，得出闭式解 $\hat{\mathbf{W}} = \mathbf{W} + (\mathbf{W}_3^\top \mathbf{W}_3 + \mathbf{E})^{-1} \Delta_{\text{MEMIT}}$（Eq. (19)），其中 $\mathbf{W}_3$ 来自解耦模块，$\mathbf{E}$ 为缩放单位阵。该公式使细粒度保持约束能够以极低的秩‑1 更新代价集成，无需迭代优化。

与 DiKE 最接近的基线是 **ROME‑C** 与 **MEMIT‑C**，它们同样尝试在编辑中加入关系约束，但并未解耦主题表征，而是直接在原始表征上施加约束或修正目标值。FINE‑KED 基准上的差距直接反映了**解耦作为瓶颈缓解机制的必要性**：以 GPT‑J 为例，DiKE 的平均 Relational Locality 达 71.3，而 MEMIT‑C 为 65.9，ROME‑C 为 62.5（Table 2）。在关系对语义差异大的“Hard”层级上，该优势更为显著（Table 2 中 Hard 列），说明当原始表征中不同关系高度纠缠时，仅靠表面约束无法有效解耦。

### 适用边界

DiKE 的有效性建立在两个前提之上：

1. **知识可表示为关系三元组** $(s, r, o)$——它天然适用于结构化事实编辑（如 COUNTERFACT、FINE‑KED 所覆盖的场景），并且能在此范围内显著提升细粒度无关知识的保持。
2. **可获取含有多种关系的事实数据来训练 KRD 模块**——模块需要从不同关系中学习分离主题表征的子空间。当知识形式超出三元组（如非结构化陈述、多模态知识、程序性知识），KRD 的训练信号难以构造，方法优势无法直接迁移（Appendix B 明确指出此局限）。

此外，本研究对“细粒度无关知识”的操作性定义严格限定为**与编辑事实共享同一主题但关系不同**的知识。对于“同一关系不同主题”“跨语言干扰”等其他类型的牵连效应，DiKE 的保持能力并未被验证。在极端分布外（OOD）的编辑需求下，解耦表征的泛化性同样属于未知。

### 局限与证据强度

DiKE 的核心创新——**通过子空间解耦保护细粒度知识**——获得了比较充分的实验支撑，但也存在若干未覆盖的风险：

- **支持性证据（可信度较高）**  
  - FINE‑KED 上跨模型、跨难度级别的 Relational Locality 提升稳健，相对增益在 6.5%–8.3% 之间（Table 2，置信度 0.95）。  
  - 消融实验（Figure 3/Figure 8）表明：移除对比损失（w/o CTR）或知识约束损失（w/o KC）均使细粒度保持大幅恶化；移除目标知识相关分量编辑（w/o TKE）则导致效力崩溃——说明解耦与子空间编辑缺一不可。  
  - COUNTERFACT 基准上，DiKE 的总体表现（harmonic mean）与最优基线 AlphaEdit 基本持平（GPT2‑XL 上 87.7 vs 88.3，Table 3），说明约束机制未牺牲一般编辑能力。

- **需手动验证的弱信号与风险**  
  - **解耦泛化对训练数据多样性的敏感性**：Figure 5 显示 KRD 模块尺寸 $k$ 在 1–10 之间性能稳定，但未见对关系类型覆盖度、领域偏移的系统分析，因此当训练关系集稀疏或与目标领域差异较大时，解耦质量可能下降。  
  - **多步编辑下的累积漂移**：闭式更新基于单次秩‑1 导出，批量编辑实验（Figure 4）虽在批大小 1‑8 下保持优势，但长期连续编辑可能造成残差累积，解耦子空间边界是否会逐渐模糊尚不明确。  
  - **非共享主题的干扰**：本方法未涉及同一关系、不同主题的牵连影响，故其在更广泛“知识保真度”上的承诺是有限的，这一点需要后续工作独立验证。

### 开放问题

基于上述边界与局限，以下开放问题标志着未来工作的关键方向：

1. **超越三元组的解耦编辑**：能否将解耦表征的构建推广到非结构化知识（如自然语言条件约束）或多模态知识，通过弱监督或强化学习动态发现解耦维度？  
2. **全维度知识保护**：如何在单次编辑中同时处理同关系‑不同主题、跨主题‑跨关系的复杂牵连，构建更通用的知识编辑安全框架？  
3. **基准的生态升级**：FINE‑KED 目前覆盖 3,085 个样本（Table 4），难度分层具有启发性，但真实世界的多样性（时间敏感知识、多源冲突、长尾关系）需要更系统的基准来捕捉，从而推动方法从原理验证走向部署。  
4. **解耦子空间的鲁棒性与自修复**：在序列编辑、持续学习和分布变化下，解耦子空间是否会发生混合或退化？是否需要引入重训练、正则化或自适应调整机制以维持边界？这些问题的回答将决定“表征解耦增强编辑”这一技术路线的长期可行性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Disentangling_Knowledge_Representations_for_Large_Language_Model_Editing.pdf]]

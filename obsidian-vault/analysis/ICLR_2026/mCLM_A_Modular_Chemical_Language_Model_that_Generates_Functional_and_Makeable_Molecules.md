---
title: "mCLM: A Modular Chemical Language Model that Generates Functional and Makeable Molecules"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/mCLM_A_Modular_Chemical_Language_Model_that_Generates_Functional_and_Makeable_Molecules.pdf
openreview_forum_id: r2HG3xOMJI
aliases:
- mCLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将分子 tokenization 粒度从原子提升至功能构建块（building block）级别，并融合合成友好的自动化组装约束，从而在生成前就保证可合成性，同时通过图神经网络编码构建块以捕获功能信息。"
primary_logic: "通过将分子表示为合成机器人友好的构建块序列，并与自然语言描述联合建模，模型能够实现高效的多目标分子优化，其生成的分子不仅具有改进的功能，而且天生兼容自动化合成平台。"
claims:
- "mCLM 在 122 个 FDA 药物（包含未见过的构建块）上实现 15.0% 的平均 ADMET 性能改进，远超所有基线（包括 GPT-5 和 Gemini-2.5-Flash）。"
- "mCLM 生成的分子的可合成性达到 98.23%，而 MoleculeSTM 仅为 85.39%，且 mCLM 的分子 100% 有效。"
- "消融实验表明，去除 GNN 编码或使用非合成 tokenizer 会导致性能大幅下降，验证了构建块级 tokenization 和 GNN 编码的必要性。"
- "在 QM9 数据集上，mCLM 使用合成保证构建块实现了 100% 可合成性，而基于向量量化的 DGAE 仅为 62%，证明了构建块方法相对于传统 VQ 方法的优势。"
---

# mCLM: A Modular Chemical Language Model that Generates Functional and Makeable Molecules

> [!tip] 核心洞察
> 通过将分子表示为合成机器人友好的构建块序列，并与自然语言描述联合建模，模型能够实现高效的多目标分子优化，其生成的分子不仅具有改进的功能，而且天生兼容自动化合成平台。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | mCLM：一种生成功能性且可合成分子的模块化化学语言模型 |
| 英文题名 | mCLM: A Modular Chemical Language Model that Generates Functional and Makeable Molecules |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=r2HG3xOMJI); [GitHub](https://github.com/blender-nlp/mCLM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | mCLM |
| Dataset | 122 FDA-approved drugs (ADMET properties), 122 FDA-approved drugs, QM9 molecules |

> [!tip] 效果简介
> - 122 FDA-approved drugs (ADMET properties) 上，Average Improvement 为 15.0%，对比 0% (FDA drugs)，变化 +15.0 pp。
> - 122 FDA-approved drugs 上，Synthesizability (Makeability) 为 98.23%，对比 85.39% (MoleculeSTM)，变化 +12.84 pp。
> - QM9 molecules 上，Synthesizability (Makeability) 为 100.0%，对比 62.0% (DGAE)，变化 +38.0 pp。

## 概述

### 问题瓶颈

现有分子生成模型普遍采用基于原子的 tokenization 策略（如 SMILES 或 SELFIES），这种粒度过细的表示方式难以编码分子的功能知识。更关键的是，这些模型生成的分子大多不可合成，导致计算预测与物理世界之间存在巨大鸿沟——即便模型在数字空间中优化出理想的性质，这些分子在实验室中却难以或无法被实际制备。

### 核心思路

mCLM 的核心洞察在于**将分子 tokenization 的粒度从原子提升至功能构建块级别**，并融合合成友好的自动化组装约束。具体而言，mCLM 将分子表示为合成机器人可直接操作的构建块序列，仅允许三种自动化反应类型的键断开：酰胺偶联、Suzuki-Miyaura 偶联和 Buchwald-Hartwig 偶联。通过图神经网络编码每个构建块以捕获其功能信息，并与自然语言描述联合建模，模型在生成前就天然保证了分子的可合成性，同时实现了高效的多目标分子优化。

### 方法定位

在方法谱系中，mCLM 相对于现有工作做出了以下关键改变：

- **分子 tokenization**：从基于原子的 SMILES/SELFIES 转向基于合成友好构建块的表示，使得每个 token 本身即携带功能和合成信息。
- **合成约束**：从后处理或无合成保证的策略，转变为前端约束——仅使用合成保证 tokenizer 输出的构建块，在生成前就锁定可合成性。
- **多模态融合**：从文本和分子独立编码或对齐的方式，转向双语 code-switch 机制——GNN 编码的构建块嵌入通过适配器投影后，与文本嵌入在统一的 Transformer 解码器中联合建模。
- **分子生成策略**：从单步生成转向迭代推理，逐步优化多目标属性，针对未达标的属性反复修改分子。

### 主要结果

在 122 个 FDA 批准药物（包含未见过的构建块）上，mCLM 实现了 **15.0% 的平均 ADMET 性能改进**，远超所有基线方法，包括 GPT-5 和 Gemini-2.5-Flash 等通用大语言模型。在可合成性方面，mCLM 生成的分子的可合成性达到 **98.23%**，而 MoleculeSTM 仅为 85.39%，且 mCLM 的分子 **100% 有效**。消融实验进一步验证了构建块级 tokenization 和 GNN 编码的必要性：移除 GNN 编码器导致平均性能降至 -7.53%，使用非合成 tokenizer（BRICS 算法）则进一步恶化至 -19.0%。在 QM9 数据集上，mCLM 使用合成保证构建块实现了 **100% 可合成性**，而基于向量量化的 DGAE 仅为 62%，充分证明了构建块方法相对于传统 VQ 方法的优势。

## 背景与动机

### 分子生成的计算-物理鸿沟

小分子药物发现的核心挑战在于找到同时满足功能活性与可合成性要求的分子。然而，当前主流的分子生成范式在这两个维度上存在根本性断裂。

一方面，基于原子级 tokenization 的表示方式（如 SMILES、SELFIES）将分子拆解为单个原子或字符，这种粒度虽然通用，却难以编码分子的**功能语义**——一个分子的药理活性往往由其关键子结构（药效团、官能团）决定，而非单个原子。另一方面，生成模型输出的分子大多停留在数字层面，其**可合成性**缺乏保证：计算预测与物理世界的自动化合成平台之间存在巨大鸿沟，大量 AI 设计的分子因合成路线不可行而无法进入实验验证。

这一困境的本质在于：现有方法将功能优化与合成约束视为两个独立的后处理步骤，而非生成过程的内在约束。分子先被生成为抽象的图或字符串，再交由逆合成分析工具评估可合成性——这种“先生成、后筛选”的策略既低效又不可靠。

### 现有方法的局限

当前分子生成与编辑的代表性方法可归为三类，各自存在显著短板：

**文本驱动的分子编辑方法**（如 **MoleculeSTM** (Liu et al., 2022)、**FineMolTex** (Li et al., 2025b)）将分子表示为 SMILES 字符串，通过自然语言指令修改分子结构。然而，SMILES 的原子级 tokenization 使得模型难以建立文本语义与分子功能子结构之间的直接映射，且生成的分子有效性不足——MoleculeSTM 的输出仅有 93.9% 为有效分子，其中仅 90.3% 可合成，整体可合成率（makeability）仅为 85.39%（Table 2）。

**通用大语言模型**（如 GPT-4o、GPT-5、Gemini-2.5-Flash、Claude 3.5 Haiku）虽然具备强大的语言理解能力，但其分子知识来自训练语料中的文本描述，缺乏对分子结构的精确建模，在合成可及性（SA 分数）上表现显著劣于专用方法（Table 3）。

**基于图的生成模型**（如 **HierVAE** (Jin et al., 2020)、**DGAE** (Boget et al., 2024)）直接操作分子图结构，但通常采用向量量化（VQ）等连续-离散转换策略，无法从设计层面保证合成可行性。例如，DGAE 在 QM9 数据集上的可合成性仅为 62%（Table 10）。

### 核心动机：前移合成约束，提升功能粒度

mCLM 的核心动机在于**将合成约束从生成后验证前移至 tokenization 阶段**，同时**将分子表示的粒度从原子提升至功能构建块（building block）级别**。这一设计基于两个关键观察：

1. **合成机器人友好的化学反应类型是有限的**。酰胺偶联、Suzuki 偶联和 Buchwald-Hartwig 反应是自动化模块化合成平台最成熟的三类反应。若将分子沿这些反应键断开为构建块，则生成的分子天然兼容自动化合成，无需事后验证。

2. **功能信息存在于子结构而非原子层面**。构建块作为分子的功能单元，其结构特征可通过图神经网络（GNN）编码为富含化学语义的嵌入向量，与自然语言描述中的功能概念形成直接对齐。

通过这种“双语”建模——自然语言描述功能需求，构建块序列表示可合成分子——mCLM 在生成前就同时保证了功能相关性与合成可行性，从而在数字设计与物理合成之间建立了直接链路。

## 核心创新

mCLM 的核心创新在于将分子生成的重心从“生成后验证可合成性”前移至“生成前保证可合成性”，并通过构建块级别的 tokenization 实现功能知识与合成约束的联合编码。这一设计直接回应了当前分子生成领域的根本瓶颈：原子级表示（如 SMILES）难以捕获功能语义，且生成分子大多不可合成，导致计算预测与物理世界之间存在巨大鸿沟。

### 关键设计转变（Changed Slots）

**1. 分子 tokenization：从原子到合成友好构建块**

传统方法（如 MoleculeSTM、LDMol）依赖基于原子的 SMILES/SELFIES 表示，将分子视为字符序列。mCLM 则将分子 tokenization 粒度提升至**功能构建块（building block）**级别——这些构建块既是功能的基本载体，也是自动化模块化合成的直接单元。具体而言，mCLM 采用双策略 tokenization 管线：
- **合成保证 tokenizer**：仅允许在酰胺偶联、Suzuki-Miyaura 偶联和 Buchwald-Hartwig 偶联三类自动化合成反应对应的键位进行断开（Figure 3），确保输出的构建块天生兼容机器人合成平台。
- **基于规则的 tokenizer**：当合成保证 tokenizer 无法完全覆盖分子结构时作为后备，保证训练数据的多样性。

这一 tokenization 策略的因果效应在消融实验中得到了直接验证：将合成保证 tokenizer 替换为非合成的 BRICS 算法后，平均性能从 +15.0% 骤降至 **-19.0%**（Table 11），表明合成约束的前置不仅是可合成性的保障，更是功能优化的关键使能因素。

**2. 合成约束：从后处理到前端保证**

现有方法通常将合成性作为生成后的过滤条件或后处理步骤，无法从根本上解决生成-合成脱节的问题。mCLM 则将合成约束**前移至生成阶段**：输出词汇表被限定为 582 个合成保证构建块，模型在生成过程中只能选择这些构建块进行组合。这一设计使得 mCLM 生成分子的可合成性（Makeability）达到 **98.23%**，而 MoleculeSTM 仅为 85.39%（Table 2），且在 QM9 数据集上实现了 **100% 可合成性**，远超基于向量量化的 DGAE（62.0%，Table 10）。

**3. 多模态融合：从对齐到双语 code-switch**

传统多模态分子模型（如 MoleculeSTM）通常将文本和分子独立编码后进行对齐。mCLM 则采用**双语 code-switch** 策略：通过 GNN 编码器（MolCLR 初始化）将每个构建块编码为结构感知的嵌入向量，经适配器模块投影后，与自然语言 token 嵌入在统一的 Transformer 解码器（Qwen-2.5-3B）中进行联合建模。训练目标为统一的分类交叉熵损失，其中分子构建块的 logits 通过 GNN 编码和适配器投影得到：

$$\mathcal{L} = H(P(\mathbf{x}), P_{\theta}(\mathbf{x})), \quad \log \mathrm{it}(P_{\theta}(v \mid \mathbf{x}_{1...i-1})) = \begin{cases} \mathbf{c}_i^{\top} \mathbf{e}_v, & v \in \mathcal{V}_{\mathrm{natural\ language}} \\ \mathbf{c}_i^{\top} f_{\psi}(\mathrm{GNN}_{\phi}(v)), & v \in \mathcal{V}_{\mathrm{molecular\ building\ block}} \end{cases}$$

消融实验证实了 GNN 编码的必要性：移除 GNN 编码器（改用 SMILES 表示）导致平均性能下降至 **-7.53%**（Table 11），说明构建块的图结构信息对功能预测至关重要。

**4. 分子生成策略：从单步到迭代推理**

mCLM 采用**迭代推理**策略：针对未达标的 ADMET 属性，逐步修改分子结构，而非一次性生成。这一策略在“fallen angel”药物（如 Evobrutinib 和 TNG348）的案例中展示了实用价值——通过逐步优化 DILI 等属性，在保持其他性质的同时实现靶向改进（Figure 4）。

### 创新本质：构建块作为数字-物理世界的桥梁

mCLM 的根本洞察在于：**构建块既是功能的载体，也是合成的单元**。通过将分子表示为合成机器人友好的构建块序列，并与自然语言描述联合建模，模型在生成前就同时编码了功能知识和合成约束。这一设计使得 mCLM 生成的分子不仅具有改进的功能（在 122 个 FDA 药物上实现 15.0% 的平均 ADMET 性能改进，远超 GPT-5 和 Gemini-2.5-Flash 等通用 LLM），而且天生兼容自动化合成平台——每个由 $n$ 个构建块组成的分子仅需 $2n-3$ 步反应即可完成组装。这种“设计即合成”的范式，为 AI 驱动的自主实验室闭环奠定了方法基础。

> **注意**：mCLM 当前仅在约 1000 个最常用构建块的词汇上进行训练，且合成保证依赖于三种特定反应类型。扩展到更大词汇、更多反应类型以及更复杂的分子骨架（如天然产物）时的泛化能力，尚需进一步验证。

## 整体框架

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/003_Figure_3.jpg]]
*Figure 3: An overview of the tokenization process. A functional molecule is first processed by the synthesis-guaranteed tokenizer to produce a set of building blocks compatible with automated modular synthesis. These blocks are then evaluated via a structure coverage check to determine whether they fully reconstruct the original molecule. If coverage is complete, the blocks are used directly for pretraining. Otherwise, the molecule is reprocessed using a rule-based tokenizer to ensure full representation for training purposes*

mCLM 的核心设计理念是将分子生成从原子级 token 提升到**功能构建块（building block）** 级别，从而在生成阶段就天然保证分子的可合成性。整体 pipeline 由四个关键模块串联而成，形成从分子表示到迭代优化的完整闭环。

### 1. 分子 Tokenization：合成保证优先

mCLM 的 tokenization 流程采用两级策略（Figure 3）。首先，分子经过**合成保证 tokenizer** 处理，该 tokenizer 仅允许在三种自动化合成机器人兼容的化学键处断开分子：酰胺偶联（amide coupling）、Suzuki-Miyaura 偶联和 Buchwald-Hartwig 偶联。若断开后的构建块能完整覆盖原始分子结构（即结构覆盖率检查通过），则直接使用这些构建块进行预训练。若覆盖不完整，则回退至**基于规则的 tokenizer**，以确保训练数据的多样性（Section 2.1）。

这一设计的因果机制在于：将合成约束**前置**到 tokenization 阶段，而非后处理过滤。这意味着模型在生成分子时，其输出词汇表天然被限制在可合成的构建块集合内，从而从根本上规避了“生成不可合成分子的计算预测”这一瓶颈。

### 2. 构建块编码：GNN 捕获功能信息

每个构建块并非简单的文本 token，而是通过**图神经网络（GNN）编码器**转换为稠密嵌入向量。GNN 编码器使用 MolCLR 初始化，能够捕获构建块的结构和功能特征。随后，**适配器模块**将 GNN 嵌入投影到 LLM 的嵌入空间，使其与自然语言 token 的嵌入维度对齐（Section 2.2）。

这一设计的关键在于：GNN 编码赋予了构建块 token 超越简单标识符的语义能力，使得模型能够理解构建块的功能含义，而非仅将其视为离散符号。

### 3. 双语联合建模：Code-Switch 机制

mCLM 采用基于 **Qwen-2.5-3B** 的 Transformer 解码器架构，将自然语言描述和分子构建块序列作为统一的 token 流进行联合建模。在训练过程中，模型通过统一的分类交叉熵损失同时学习自然语言和分子构建块的生成：

$$
\mathcal{L} = H(P(\mathbf{x}), P_{\theta}(\mathbf{x})), \quad \log \mathrm{it}(P_{\theta}(v \mid \mathbf{x}_{1...i-1})) = \begin{cases} \mathbf{c}_i^{\top} \mathbf{e}_v, & v \in \mathcal{V}_{\mathrm{natural\ language}} \\ \mathbf{c}_i^{\top} f_{\psi}(\mathrm{GNN}_{\phi}(v)), & v \in \mathcal{V}_{\mathrm{molecular\ building\ block}} \end{cases}
$$

其中，自然语言 token 的 logits 通过标准嵌入计算，而分子构建块的 logits 则需经过 GNN 编码和适配器投影。这种“双语 code-switch”机制使得模型能够无缝地在文本指令和分子结构之间切换，理解“改进某分子的肝毒性”这类跨模态指令。

### 4. 迭代推理：多目标优化闭环

mCLM 的推理并非单步完成，而是采用**迭代推理模块**（Figure 4）。具体流程为：模型首先生成初始分子候选，随后通过预训练的 ADMET 属性预测器（oracle 模型）评估该分子的 6 项药代动力学和毒性属性。对于未达标的属性，模型根据评估反馈迭代修改分子结构，直至所有属性满足要求或达到最大迭代次数（Section 2.3）。

### 输入输出流总览

整体数据流可概括为：**输入**为自然语言指令（如“降低该分子的 DILI 风险”）和目标分子结构 → **tokenization** 将分子转换为构建块序列 → **GNN 编码**注入结构信息 → **LLM 解码**生成优化后的构建块序列 → **迭代评估**驱动多轮优化 → **输出**为可合成的优化分子。训练数据通过从文献中提取分子的功能描述和合成约束，并将构建块序列嵌入自然语言句子中构建而成（Figure 7）。

## 核心模块与公式推导

### 合成保证 Tokenizer

mCLM 的核心创新在于将分子 tokenization 的粒度从传统的原子级（如 SMILES）提升至合成友好的构建块（building block）级别。该模块采用双轨制 tokenization 策略（Figure 3），以平衡化学空间覆盖与合成可行性：

- **合成保证 tokenizer**：仅允许在三种自动化合成平台兼容的化学键处断开分子——酰胺偶联（amide coupling）、Suzuki-Miyaura 偶联和 Buchwald-Hartwig 偶联。该 tokenizer 输出的构建块可直接用于机器人自动化组装，其所需反应步骤数为 $2n - 3$（其中 $n$ 为构建块数量）。
- **基于规则的 tokenizer**：当合成保证 tokenizer 无法完全覆盖分子结构时作为后备方案，使用 BRICS 等规则算法进行断键，确保预训练数据的多样性。

训练数据中，约 680 万分子可通过完整 tokenization 管线处理，产生约 80 万独特构建块，其中约 20 万为合成保证构建块。

### GNN 编码器与适配器模块

mCLM 并非直接将构建块视为离散 token，而是通过图神经网络（GNN）编码每个构建块的图结构信息，从而捕获功能相关的化学特征：

- **GNN 编码器**：以 MolCLR 预训练权重初始化，将每个构建块 $v$ 映射为稠密嵌入向量 $\text{GNN}_{\phi}(v)$。
- **适配器模块** $f_{\psi}$：将 GNN 输出的嵌入投影到 LLM 的嵌入空间，使得构建块表示可与自然语言 token 嵌入对齐。

### 统一交叉熵损失函数

mCLM 采用 Transformer 解码器架构（Qwen-2.5-3B），在统一序列中对自然语言和分子构建块进行联合建模。训练目标为统一分类交叉熵损失：

$$\mathcal{L} = H(P(\mathbf{x}), P_{\theta}(\mathbf{x}))$$

其中，模型对下一 token $v$ 的 logit 计算方式取决于 token 类型：

$$\log \mathrm{it}(P_{\theta}(v \mid \mathbf{x}_{1...i-1})) = \begin{cases} \mathbf{c}_i^{\top} \mathbf{e}_v, & v \in \mathcal{V}_{\mathrm{natural\ language}} \\ \mathbf{c}_i^{\top} f_{\psi}(\mathrm{GNN}_{\phi}(v)), & v \in \mathcal{V}_{\mathrm{molecular\ building\ block}} \end{cases}$$

**变量含义**：
- $\mathbf{c}_i$：Transformer 解码器在位置 $i$ 的隐藏状态
- $\mathbf{e}_v$：自然语言 token $v$ 的标准嵌入向量
- $\text{GNN}_{\phi}(v)$：构建块 $v$ 的图结构嵌入
- $f_{\psi}$：适配器投影函数
- $\mathcal{V}_{\mathrm{natural\ language}}$ 和 $\mathcal{V}_{\mathrm{molecular\ building\ block}}$：分别为自然语言词汇表和分子构建块词汇表

该公式的核心机制在于：分子构建块的预测并非依赖固定的 token 嵌入表，而是通过 GNN 动态编码其图结构，再经适配器投影至语言模型的语义空间。这种“双语 code-switch”设计使得模型能够同时理解自然语言描述的功能需求与构建块的化学结构信息。

### 迭代推理模块

mCLM 采用逐步优化策略进行多目标分子改进：给定输入分子和需要优化的属性目标，模型评估当前分子的各项属性，针对未达标的属性迭代生成修改后的分子。推理时，输出词汇表被限制在 582 个合成保证构建块内，确保生成的分子 100% 有效且天生兼容自动化合成平台。

## 实验与分析

### 核心实验结果

mCLM 在 122 个 FDA 已批准药物（由合成保证构建块组成）上进行了 6 项 ADMET 属性的多目标优化评估，涵盖 AMES 致突变性、血脑屏障穿透性（BBBP）、CYP3A4 代谢、药物性肝损伤（DILI）、人肠道吸收（HIA）和 P-糖蛋白底物识别（PGP）。**Table 1** 汇总了关键结果：mCLM 生成的分子在全部 6 项指标上均优于原始 FDA 药物，平均改善幅度达到 **15.0%**。作为对比，所有通用大语言模型基线（GPT-4o、GPT-5、Gemini-2.5-Flash、Claude 3.5 Haiku）的平均改善均为负值，表明这些模型无法在保持分子有效性的同时提升功能属性。专门的文本-分子编辑方法 **MoleculeSTM**（Liu et al., 2022）和 **FineMolTex**（Li et al., 2025b）同样表现不佳，平均改善分别为 -17.2% 和 -8.8%。文本到分子生成模型 **LDMol**（Chang and Ye, 2024）的平均改善为 -17.0%。mCLM 是唯一在所有 6 项 ADMET 指标上均实现正向改善的方法。


![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/004_Table_1.jpg]]
*Table 1: Average pharmacokinetic and toxicity properties of FDA drugs composed of synthesisguaranteed blocks, as well as their proposed modifications. (↓: lower is better, ↑: higher is better). Green = better than FDA, Red = worse, Light green bold = best overall per column. The key to expediting the drug creation process is to discover potent molecular candidates that are simultaneously synthesis-friendly. While mCLM shows strong property editing results, its key benefit*

可合成性方面，**Table 2** 给出了决定性证据：mCLM 生成的分子 **100% 有效**（RDKit 验证），其中 **98.23%** 可通过逆合成分析找到合成路线（即 Makeability = 98.23%）。相比之下，MoleculeSTM 的有效率仅为 93.80%，可合成率仅 85.39%；FineMolTex 的可合成率为 86.80%；GPT-5 和 Gemini-2.5-Flash 的可合成率分别仅为 1.67% 和 1.17%。这一差距直接验证了 mCLM 的核心设计理念——将合成约束前置于 tokenization 阶段，而非依赖后处理过滤。


![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/005_Table_2.jpg]]
*Table 2: Synthetic accessibility (SA) (Ertl et al., 2009), validity, and retrosynthetic results across baselines. Synthesizability is the percent of valid molecules where a retrosynthetic route was found. Makeability is the overall percent of generations which can be synthesized (Makeability =Valid × Synth.)*

在 QM9 数据集上的对比实验（**Table 10**）进一步证实了构建块方法的优势：mCLM 使用合成保证构建块实现了 **100%** 的可合成性，而基于向量量化的离散图自编码器 **DGAE**（Boget et al., 2024）仅为 62%。这表明传统的 VQ-based 分子表示方法无法内在地保证合成可行性。


![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/023_Table_10.jpg]]
*Table 10: Synthesizability comparison using Allchemy on QM9 molecules*

### 消融实验

**Table 11** 报告了系统的消融分析，揭示了 mCLM 各组件的因果贡献：


![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/024_Table_11.jpg]]
*Table 11: Comparison of pharmacokinetic and toxicity property scores between using Qwen-2.5-3B and Llama-3.2-3B as backbones*

- **移除 GNN 编码器**（改用 SMILES 字符串表示构建块）：平均 ADMET 改善从 15.0% 骤降至 **-7.53%**。这证明 GNN 编码的分子图结构信息对于功能预测至关重要，单纯的序列化表示无法充分捕获构建块的功能特征。

- **使用非合成 tokenizer**（BRICS 算法替代合成保证 tokenizer）：平均改善进一步降至 **-19.0%**，甚至低于原始 FDA 药物基线。这说明合成保证 tokenizer 不仅保障了可合成性，其断键规则（仅允许酰胺偶联、Suzuki 偶联和 Buchwald-Hartwig 偶联）也隐式编码了化学合理性，对功能优化有正向贡献。

- **替换 backbone 为 Llama-3.2-3B**：平均改善仅为 **2.82%**，远低于 Qwen-2.5-3B 的 15.0%。这表明 backbone 的选择对模型性能有显著影响，Qwen-2.5 的预训练质量或架构特性更适合化学-语言联合建模。

- **无合成保证的扩展实验**（**Table 4**）：当放宽合成保证约束，对包含 3 个及以上构建块的 FDA 药物进行优化时，mCLM 仍能实现 12.3% 的平均改善，但可合成性指标有所下降。这验证了合成保证 tokenizer 在前端约束中的关键作用。


![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/009_Table_4.jpg]]
*Table 4: Average pharmacokinetic and toxicity properties of FDA drugs with 3 or more blocks and their proposed modifications. Note, these molecules do not have synthesis-guarantees. (↓: lower is better, ↑: higher is better*

### 与分层生成方法的对比

**Table 8** 和 **Table 9** 将 mCLM 与分层分子图生成方法 **HierVAE**（Jin et al., 2020）进行了对比。需要注意的是，HierVAE 需要针对每个属性单独微调，而 mCLM 在统一的指令遵循设置下工作。在 ADMET 属性改善上，mCLM 在 6 项指标中的 5 项优于 HierVAE（Table 8）。在可合成性方面，HierVAE 的 Makeability 仅为 66.00%（Table 9），远低于 mCLM 的 98.23%，进一步凸显了构建块级 tokenization 相对于图级生成在合成可行性上的优势。


![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/021_Table_8.jpg]]
*Table 8: Comparison of pharmacokinetic and toxicity property scores between mCLM and HierVAE. Note that HierVAE is fine-tuned separately for each property, whereas mCLM is used in a instructionfollowing setting*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/022_Table_9.jpg]]
*Table 9: Synthetic accessibility (SA) (Ertl et al., 2009), validity, and retrosynthetic results for HierVAE. Synthesizability is the percent of valid molecules where a retrosynthetic route was found. Makeability is the overall percent of generations which can be synthesized (Makeability =Valid × Synth.)*

### 迭代推理与失败模式

mCLM 的迭代推理模块（**Figure 4**）展示了在“fallen angel”药物（因安全性问题终止开发的候选药物）上的逐步优化能力。以 Evobrutinib 为例，mCLM 首先针对 DILI 进行优化，随后依次改善 AMES 和 CYP3A4，每一步都保持已优化属性的同时提升目标属性。相比之下，MoleculeSTM 在相同任务上频繁产生无效分子（**Figure 6**），暴露出其在多步编辑中的稳定性缺陷。

### 评估局限性

当前实验存在以下需注意的边界条件：

1. **动态范围受限**：评估使用的 FDA 药物集合可能偏向结构简单的分子，导致可合成性指标的区分度不足——多数基线方法的 SA 分数集中在较窄区间内。
2. **多目标权衡未充分量化**：mCLM 在迭代优化某一属性时可能在其他属性上做出妥协，当前评估仅报告了各属性的独立改善，缺乏 Pareto 前沿分析。
3. **训练数据偏差**：构建块词汇和训练数据基于现有数据库，在全新分子骨架上的泛化能力尚需独立验证。
4. **合成保证的化学空间限制**：当前仅支持三种反应类型，覆盖的化学空间有限，对于需要其他反应类型的分子优化场景可能不适用。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/008_Table_3.jpg]]
*Table 3: Synthetic Accessibility (SA) scores with RDKit validity percentages across datasets*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/012_Table_5.jpg]]
*Table 5: Dataset categories and their respective sample counts*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/013_Table_6.jpg]]
*Table 6: Breakdown of molecule data by dataset category*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_r2HG3xOMJI/figures/014_Table_7.jpg]]
*Table 7: Performance (AUC) of individual models and the ensemble across six selected ADMET tasks*


## 方法谱系与知识库定位

### 分子生成范式的粒度跃迁

mCLM 的核心贡献在于将分子生成的 tokenization 粒度从原子/字符级（SMILES、SELFIES）提升至功能构建块（building block）级别，并将合成约束前置于生成过程。这一设计使其在方法谱系中处于独特位置：它既不同于传统的基于 SMILES 的分子生成模型，也区别于纯文本驱动的分子编辑方法。

在分子生成领域，现有工作可大致分为三类。第一类是**基于字符串的生成模型**，如 **LDMol**（Chang and Ye, 2024）通过潜在扩散模型生成分子文本表示，**HierVAE**（Jin et al., 2020）采用层次化 VAE 生成分子图，**DGAE**（Boget et al., 2024）则使用离散图自编码器结合向量量化（VQ）进行分子生成。这些方法的共同瓶颈在于：生成的分子在可合成性上缺乏保证。实验证据表明，DGAE 在 QM9 数据集上的可合成性仅为 62%（Table 10），而 mCLM 使用合成保证构建块实现了 100% 的可合成性，差距高达 38 个百分点。这一对比直接验证了构建块级 tokenization 相对于传统 VQ 方法的优势。

第二类是**文本驱动的分子编辑方法**，以 **MoleculeSTM**（Liu et al., 2022）和 **FineMolTex**（Li et al., 2025b）为代表。这些方法试图通过自然语言指令修改分子结构，但其底层仍依赖 SMILES 表示，导致生成分子的有效性和可合成性均不理想。在 122 个 FDA 药物的优化任务中，MoleculeSTM 的分子有效性仅为 93.80%，可合成性为 85.39%（Table 2），而 mCLM 分别达到 100% 和 98.23%。这一差距揭示了原子级 tokenization 的根本局限：模型难以在生成过程中内化合成可行性约束。

第三类是**通用大语言模型**，如 GPT-4o、GPT-5、Gemini-2.5-Flash 和 Claude 3.5 Haiku。尽管这些模型具备强大的语言理解和推理能力，但它们在分子生成任务上表现不佳——mCLM 在 122 个 FDA 药物上实现了 15.0% 的平均 ADMET 性能改进，远超所有通用 LLM 基线（Table 1）。这表明，缺乏专门的分子结构编码和合成约束先验，通用 LLM 难以在化学空间中进行有效的功能优化。

### 关键技术槽位对比

mCLM 在四个关键设计维度上相对于基线方法做出了系统性改变：

1. **分子 tokenization**：从基于原子的 SMILES/SELFIES 转向合成友好的构建块。这一改变不仅提升了生成分子的可合成性，还使得每个 token 天然携带功能信息——构建块本身就是具有特定化学功能的子结构。

2. **合成约束**：从后处理或无合成保证转变为前端约束。mCLM 的输出词汇被限制在 582 个合成保证构建块内（Section 3.2），这意味着模型在生成之前就已经确保了产物的可合成性，而非在生成后进行筛选。

3. **多模态融合**：从文本和分子的独立编码或对齐，转变为“双语 code-switch”机制——GNN 编码的构建块嵌入通过适配器投影后，与自然语言嵌入在同一 Transformer 解码器中联合处理。消融实验（Table 11）表明，移除 GNN 编码器（改用 SMILES）会导致平均性能降至 -7.53%，验证了这一设计的必要性。

4. **分子生成策略**：从单步生成转变为迭代推理。mCLM 在每次迭代中评估当前分子的各项属性，针对未达标的属性进行定向修改（Section 2.3, Algorithm 1），实现了多目标逐步优化。

### 适用边界与局限

mCLM 的适用性受限于以下几个关键因素：

**词汇规模约束**：当前模型仅在约 1000 个最常用的构建块词汇上进行训练。虽然这已覆盖大量药物分子，但对于包含罕见或全新构建块的分子骨架，模型可能无法有效表示。扩展到更大词汇和更大 backbone 的影响尚待验证。

**反应类型限制**：合成保证依赖于三种具体的反应类型——酰胺偶联、Suzuki-Miyaura 偶联和 Buchwald-Hartwig 偶联。这意味着模型可生成的化学空间受限于这三类反应所能构建的分子。未来需要纳入更多自动化反应类型（如 C-H 键活化、光化学等）以扩展可合成的化学空间。

**多目标优化的权衡**：药物发现本质上是多目标优化问题。mCLM 在迭代优化某一属性时，可能会在其他属性上做出妥协。当前的评估主要关注平均性能改进，对各属性间权衡的全面分析尚不充分。

**评估动态范围**：使用的 FDA 药物集合可能偏向于相对简单的分子骨架，使得合成性指标的区分度不足。在更难或更复杂的分子分布（如天然产物）上，模型的合成性和功能优化能力需要进一步验证。

**泛化性风险**：训练数据基于现有数据库，可能偏向已发现的分子骨架。对于训练中未见过的全新分子骨架，mCLM 的泛化能力尚缺乏系统评估。

### 开放问题

mCLM 开辟了若干值得深入探索的方向：

- **多模态知识整合**：如何将 2D/3D 结构、蛋白质-配体复合物、细胞系、核酸序列等多模态知识纳入 mCLM 的框架？当前的构建块表示仅捕获了子图结构信息，更丰富的物理化学上下文可能进一步提升功能预测精度。

- **更长推理链**：能否在迭代推理中实现更长的推理链，覆盖更广泛的药代动力学/毒性属性？当前的工作主要聚焦于 6 个 ADMET 属性，扩展到更多属性并建立因果推理链是一个自然的方向。

- **自主实验室闭环**：mCLM 的设计天然兼容自动化合成平台。将其集成到自主实验室闭环中——从 AI 设计、自动化合成到功能测试的迭代循环——是实现“数字世界到物理世界”直接链接的关键下一步。

- **合成空间扩展**：当前合成保证 tokenizer 仅支持三种反应类型。能否将其扩展以包括更多的自动化反应类型，从而大幅扩展可合成的化学空间？

- **System 2 推理**：如何将化学推理从当前的模式匹配提升到更深层次的因果推理、反事实推理和冲突声明消解？这是通往真正化学智能的重要阶梯。

## 原文 PDF

![[paperPDFs/ICLR_2026/mCLM_A_Modular_Chemical_Language_Model_that_Generates_Functional_and_Makeable_Molecules.pdf]]

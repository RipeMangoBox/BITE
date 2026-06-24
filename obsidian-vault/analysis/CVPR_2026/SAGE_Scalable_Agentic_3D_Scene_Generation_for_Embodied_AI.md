---
title: "SAGE: Scalable Agentic 3D Scene Generation for Embodied AI"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SAGE_Scalable_Agentic_3D_Scene_Generation_for_Embodied_AI.pdf
project_link: "https://nvlabs.github.io/sage/"
code_link: null
aliases:
- SAGE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入基于 MCP 协议的 agentic 框架，结合视觉 critic 与物理 critic 的闭环反馈，使系统能自适应选择和迭代改进生成流程。
primary_logic: 通过将生成器与仿真验证器（Isaac Sim）无缝集成并运行在 Model Context Protocol (MCP) 上，agent 可以像使用工具一样调用生成和批评模块，实现自我纠正和物理稳定的场景生成。
claims:
- SAGE 是一个 agentic 框架，能理解用户意图并自动生成仿真就绪的 3D 场景。
- 通过两个互补的 critic（视觉和物理）提供迭代反馈，agent 能自我改进场景生成。
- 结合物理 critic 的模拟验证，SAGE 生成的场景几乎完美物理稳定（Coll.% 1.9, Stab.% 99.9）。
- Average over Bedroom, Kitchen, Living Room (10 scenes each) 上 Stability (%) = 99.9
---

# SAGE: Scalable Agentic 3D Scene Generation for Embodied AI

> [!tip] 核心洞察
> 通过将生成器与仿真验证器（Isaac Sim）无缝集成并运行在 Model Context Protocol (MCP) 上，agent 可以像使用工具一样调用生成和批评模块，实现自我纠正和物理稳定的场景生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | SAGE: 面向具身 AI 的可扩展智能体 3D 场景生成 |
| 英文题名 | SAGE: Scalable Agentic 3D Scene Generation for Embodied AI |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.10116) · [Project](https://nvlabs.github.io/sage/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SAGE |
| Dataset | Average over Bedroom, Kitchen, Living Room, Mobile Manipulation |

> [!tip] 效果简介
> - Average over Bedroom, Kitchen, Living Room (10 scenes each) 上，Stability (%) 99.9 vs 63.8 (Holodeck) (+36.1)。
> - Average over Bedroom, Kitchen, Living Room 上，Collision (%) 1.9 vs 22.0 (Holodeck) (-20.1)；Realism (GPT-4.1 score, 1-10) 8.8 vs 7.5 (Holodeck) (+1.3)。
> - Mobile Manipulation (Cross-Evaluation on SAGE scenes) 上，Test Success Rate (%) 46.0 (SAGE trained on SAGE scenes) vs 14.4 (Baseline1, mimics SceneWeaver) / 13.1 (Baseline2, mimics Holodeck) (+31.6 / +32.9)。

## 概述

### 问题背景与瓶颈

具身 AI 的训练高度依赖大规模、物理可信的 3D 仿真场景，但现有场景生成方法存在两个根本性瓶颈：**缺乏物理验证**与**缺乏自改进能力**。主流方法（如 **Holodeck**、**SceneWeaver**）通常采用固定流水线或单智能体单次生成，生成后不经过仿真器闭环验证，导致场景物理不稳定、碰撞率高，无法直接部署于具身仿真训练。这一问题在机器人策略学习中尤为突出——不可靠的训练场景会直接损害策略的泛化性与任务成功率。

### 核心方法：SAGE 智能体框架

SAGE（Scalable Agentic 3D Scene Generation）是一个面向具身 AI 的可扩展智能体 3D 场景生成框架。其核心洞察在于：**将生成器与仿真验证器无缝集成，并运行在 Model Context Protocol (MCP) 协议之上，使智能体可以像调用工具一样动态编排生成与批评模块，实现自我纠正和物理稳定的场景生成**。

具体而言，SAGE 通过以下机制打破上述瓶颈：

- **MCP 驱动的智能体编排**：智能体作为 MCP 客户端，各生成工具（场景初始化器、物体放置器/移动器/移除器）和批评模块（视觉 critic、物理 critic）均托管在 MCP 服务器端。智能体根据任务意图动态选择工具组合，而非执行固定流水线。
- **双 critic 闭环反馈**：视觉 critic 评估语义与空间一致性，物理 critic 在 Isaac Sim 仿真器中验证重力与碰撞稳定性。两者协同提供迭代反馈，驱动智能体自我改进生成结果。
- **仿真器在环验证**：物理 critic 对每次物体放置进行仿真验证，拒绝不稳定放置，从根本上保证场景的物理可用性。

### 关键结果概览

在卧室、厨房、客厅三类常见场景的定量评估中（Table 2），SAGE 在多项指标上显著超越基线方法：

- **物理稳定性**：SAGE 稳定性达 99.9%，而 Holodeck 仅为 63.8%（+36.1 个百分点）。
- **碰撞率**：SAGE 碰撞率仅 1.9%，Holodeck 为 22.0%（降低 20.1 个百分点）。
- **视觉真实感**：GPT-4.1 评分 SAGE 达 8.8/10，Holodeck 为 7.5/10。

在下游机器人任务中，SAGE 生成的场景展现出更强的训练价值。在 Mobile Manipulation 跨分布评估中（Table 5），使用 SAGE 场景训练的策略测试成功率达 46.0%，而使用模仿 SceneWeaver 和 Holodeck 的基线方法分别仅为 14.4% 和 13.1%，**提升超过 30 个百分点**。消融实验进一步证实，视觉 critic 与物理 critic 的组合是性能提升的关键——两者结合将碰撞率从 7.8% 降至 1.9%，稳定性提升至 99.6%（Table 3）。

### 方法定位

SAGE 在 3D 场景生成领域的方法谱系中占据独特位置。与 Holodeck 等 LLM 驱动的固定流水线方法相比，SAGE 引入了完整的智能体自改进循环；与 SceneWeaver 等无仿真验证的智能体方法相比，SAGE 首次将仿真器在环物理验证系统性地纳入生成闭环。Table 1 的方法对比清晰展示了这一差异化定位：SAGE 是唯一同时满足“智能体驱动”“仿真验证”“自改进”“可扩展”四项标准的方法。

## 背景与动机

### 具身 AI 对仿真场景的迫切需求

具身 AI 的进步高度依赖大规模、高质量的训练环境。机器人策略学习需要大量交互数据，而真实世界的数据采集成本高昂、耗时且难以覆盖长尾场景。因此，仿真环境成为具身 AI 训练的核心支柱——它能够以极低的成本生成无限多样的交互数据，并支持安全、可重复的策略评估。然而，这一愿景的实现有一个关键前提：**仿真场景必须足够丰富、语义合理且物理稳定**，否则在仿真中训练的策略将无法迁移到真实世界。

当前，3D 场景生成领域的主要瓶颈并非缺乏生成能力，而是**缺乏物理验证和智能体自改进机制**。现有方法虽然能够生成视觉上可接受的场景，但这些场景往往在物理层面不可靠——物体悬浮、相互穿透、轻微碰撞即导致场景崩塌。这使得生成结果无法直接部署于具身仿真训练，需要大量人工后期修复，严重限制了场景生成的规模化应用。

### 现有方法的系统性缺口

主流 3D 场景生成方法可大致分为两类：基于固定流水线的方法和基于单一智能体的方法。

**固定流水线方法**（如 **Holodeck**）依赖预定义的规则和顺序步骤来生成场景。这类方法缺乏对生成结果的反思能力——一旦生成完成，系统无法识别语义不合理或物理不稳定的放置，更无法进行修正。由于没有仿真器在环的验证机制，生成的场景在重力作用下常常出现物体位移、倒塌等问题，碰撞率居高不下。

**单一智能体方法**（如 **SceneWeaver**）引入了一定的智能决策能力，但通常缺乏系统性的物理验证和闭环自改进机制。它们可能在单次生成中表现良好，但无法在发现问题后迭代优化，也无法保证场景在物理仿真中的稳定性。

Table 1 系统对比了现有方法与 SAGE 的能力差异，清晰地揭示了这一缺口：现有方法在“仿真器验证”“智能体自改进”“可扩展生成”等关键维度上均存在缺失。

### 核心动机：从“生成场景”到“生成仿真就绪的场景”

本文的核心动机在于弥合“场景生成”与“仿真就绪”之间的鸿沟。作者提出的关键洞察是：**将生成器与仿真验证器无缝集成，并让智能体像使用工具一样调用它们，可以实现自我纠正和物理稳定的场景生成**。

这一洞察催生了 SAGE 框架的设计目标：
1. **仿真器在环验证**：每次物体放置后，在 Isaac Sim 中实时验证重力稳定性和碰撞情况，拒绝不稳定的放置。
2. **智能体自改进**：通过视觉 critic（评估语义和空间一致性）和物理 critic（评估物理稳定性）的闭环反馈，智能体能够迭代改进场景，直到满足质量要求。
3. **可扩展的智能体编排**：基于 Model Context Protocol (MCP) 协议，智能体可以动态选择和调用多个生成工具与批评模块，支持从单房间到多房间、从常见场景到开放词汇场景的规模化生成。

这一设计使得 SAGE 不仅是一个场景生成器，更是一个能够理解用户意图、自动生成仿真就绪环境的智能体系统，直接服务于具身 AI 的策略学习与评估。

## 核心创新

SAGE 的核心创新在于将 **agentic 自改进机制**与**仿真器闭环物理验证**深度耦合，解决了现有 3D 场景生成方法“好看但不可用”的根本瓶颈。与 Holodeck、SceneWeaver 等基线方法相比，SAGE 在三个关键维度上实现了质性突破（见表 1）。

### 从固定流水线到 Agentic 自改进

现有方法依赖固定的生成流水线或单次 agent 调用，生成结果一旦产出便无法修正。SAGE 基于 **Model Context Protocol (MCP)** 构建了一个完整的 agentic 框架：agent 作为 MCP 客户端，动态调用 Scene Initializer、Asset Placer、Asset Mover、Asset Remover 等生成工具，如同使用工具一般灵活组合生成流程。更关键的是，agent 并非一次性完成场景，而是通过两个互补的 critic 持续获取反馈，迭代改进场景直至满足质量标准——这一自改进闭环是基线方法完全不具备的。

### 仿真器闭环物理验证：从“看起来对”到“物理上对”

这是 SAGE 最具区分度的创新。**Physics Critic** 将 Isaac Sim 仿真器直接嵌入生成流程，对每次物体放置进行重力稳定性和碰撞检测验证，拒绝不稳定的放置并反馈给 agent 进行修正。这一“simulator-in-the-loop”机制使得 SAGE 生成的场景**几乎完美物理稳定**：平均碰撞率仅 1.9%，稳定性达 99.9%，而 Holodeck 的碰撞率高达 22.0%，稳定性仅 63.8%（见表 2）。消融实验进一步揭示了因果机制：仅添加 physics critic 即可将碰撞率从 7.8% 降至 1.9%，稳定性提升至 99.6%（见表 3），证明仿真器闭环验证是物理稳定性的决定性因素。

### Visual Critic 与 Physics Critic 的协同互补

SAGE 的双 critic 设计形成了语义-物理联合质量保障。**Visual Critic** 评估语义合理性、空间布局和视觉完整性，引导 agent 调整物体组合；**Physics Critic** 则确保物理可行性。消融实验表明，两者协同才能达到最优：仅用 visual critic 可改善视觉质量但物理稳定性不足，仅用 physics critic 可保证稳定但视觉质量下降，两者结合则在所有指标上取得最佳结果（见表 3）。这种“语义审美 + 物理约束”的双重反馈机制，是 SAGE 生成的场景既能通过视觉评测（GPT-4.1 Realism 评分 8.8 vs. Holodeck 7.5）又能直接部署于具身仿真训练的根本原因。

### 关键创新总结

| 创新维度 | 基线方法 | SAGE |
|---------|---------|------|
| 生成范式 | 固定流水线 / 单次 agent 调用 | Agentic 自改进闭环（MCP 协议驱动） |
| 物理验证 | 无或非系统化 | Isaac Sim 闭环物理 critic，每次放置验证 |
| 质量保障 | 仅语义/视觉评估 | 视觉 critic + 物理 critic 协同反馈 |
| 部署可用性 | 需人工后处理修正物理问题 | 生成即仿真就绪（Coll. 1.9%, Stab. 99.9%） |

> **注意**：关于 SAGE 与基线方法在“agentic 编排”和“自改进”能力上的具体实现差异，论文仅提供了高层次对比（Table 1），未给出基线方法的详细架构描述。若需精确的技术对比，建议查阅 Holodeck 和 SceneWeaver 的原始论文进行验证。

## 整体框架

SAGE 是一个**基于 MCP 协议的智能体（agentic）框架**，其核心设计思路是将场景生成建模为一个**闭环、自改进的工具调用过程**。系统接收用户指定的具身任务描述（例如“拿起一个碗并放在桌子上”），理解任务意图后，自动生成可在仿真器中直接部署的 3D 场景。

### 架构与信息流

整个框架围绕 **MCP（Model Context Protocol）** 构建。智能体作为 MCP 客户端，而每一个功能模块（生成器、批评器、仿真器）都封装在独立的 MCP 服务器之后。这种设计使得智能体可以像调用工具一样动态选择、组合和切换各个模块，无需硬编码执行流程。

信息流遵循“**生成—评估—修正**”的闭环模式：
1. **用户意图解析**：智能体首先解析输入的任务描述或场景规格，将其分解为房间类型、风格、物体列表和空间约束。
2. **场景初始化**：调用 Scene Initializer 生成空房间模型（仅包含地板和墙壁），并输出建议的物体列表。
3. **物体放置与调整**：智能体迭代调用 Asset Placer、Asset Mover 和 Asset Remover 等工具，逐步构建场景布局。
4. **双重批评反馈**：每轮放置后，Visual Critic 评估语义与空间一致性，Physics Critic 在 Isaac Sim 中进行物理验证（重力稳定性、碰撞检测），将反馈传回智能体。
5. **自修正迭代**：智能体根据批评反馈决定是否需要重新放置、移除或新增物体，直至满足物理稳定性和视觉质量要求。

### 核心模块关系

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| **Scene Initializer** | 生成空房间模型与物体列表 | 场景规格（房间类型、风格、物体描述） | 空房间 3D 模型 + 建议物体列表 |
| **Asset Placer** | 生成并放置 3D 物体 | 文字描述、放置约束（地板/墙壁/叠放） | 更新后的场景文件 |
| **Asset Mover** | 移动已放置物体 | 目标物体描述、新位置 | 更新后的场景文件 |
| **Asset Remover** | 移除场景中物体 | 目标物体描述 | 更新后的场景文件 |
| **Visual Critic** | 评估语义与空间一致性 | 当前场景状态 | 评估分数 + 改进建议（新增/调整物体） |
| **Physics Critic** | 物理稳定性验证 | 场景文件 | 碰撞率、稳定性比率 + 不稳定物体列表 |
| **MCP Client/Server** | 通信协议层 | 工具调用请求 | 工具执行结果 |

### 关键设计决策

**因果机制**：现有方法（如 Holodeck、SceneWeaver）的根本瓶颈在于缺乏物理验证和自改进能力——它们采用固定流水线或单次智能体传递，生成的场景碰撞率高（22.0%）、物理不稳定（稳定性仅 63.8%），无法直接用于具身仿真训练。SAGE 通过引入 **simulator-in-the-loop 物理验证**和**智能体自改进闭环**，将碰撞率降至 1.9%、稳定性提升至 99.9%，使生成场景真正“仿真就绪”（Table 2）。

**工具化设计**：将每个功能模块封装为独立的 MCP 工具，使得智能体可以根据当前场景状态**自适应选择**调用哪些工具，而非遵循预设流程。例如，当 Physics Critic 报告某物体不稳定时，智能体可以选择调用 Asset Mover 调整位置，或调用 Asset Remover 移除后重新放置。

**双重批评互补**：消融实验（Table 3）证实，仅使用 Visual Critic 可改善视觉质量但物理稳定性不足，仅使用 Physics Critic 可大幅降低碰撞率但视觉布局可能欠佳；两者结合才能同时达到最佳视觉质量和物理稳定性。

### 输入输出规范

- **输入**：开放词汇的自然语言任务描述或场景规格，支持文本条件、图像条件（通过 Qwen3-VL 提取风格与物体属性）以及多房间平面图条件。
- **输出**：仿真就绪的 3D 场景文件，包含经过物理验证的物体布局，可直接加载至 Isaac Sim 进行具身任务训练。

### 补充图表

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/003_Figure_2.jpg]]
*Figure 2: Overview of SAGE scene generation. Our system converts open-vocabulary text prompts into simulation-ready 3D scenes by orchestrating multiple generator tools and critics. The agent dynamically calls generators (Scene Init, Asset Placer/Mover/Remover) to construct and refine layouts, while visual and physics critics provide iterative feedback for self-improvement. The visual critic suggests semantic corrections (e.g., missing or misplaced objects), and the physics critic validates stability via Isaac Sim. For example, after applying physics critic in the bottom image, the newly added pillows on the bed fall flat. This self-improvement process ends when the agent considers that the generated...*

## 核心模块与公式推导

SAGE 的生成流程由 **MCP 协议**（Model Context Protocol）驱动，将 LLM 作为中央调度器（MCP Client），各功能模块封装为独立的 MCP Server 工具。Agent 根据用户任务意图动态选择并调用工具，通过视觉与物理双重批评的闭环反馈实现自我纠正。

### 关键模块

**Scene Initializer（场景初始化器）**：接收场景规格说明，生成仅含地板和墙壁的空房间模型，并输出建议放置的物体列表。

**Asset Placer（资产放置器）**：根据文字描述生成 3D 物体并将其放置到场景中，支持地板放置、墙壁附着和叠放三种模式。

**Asset Mover（资产移动器）**：对已放置物体执行“先移除再重新放置”的操作，实现布局调整。

**Asset Remover（资产移除器）**：根据文字指令从场景中移除指定物体。

**Visual Critic（视觉批评器）**：评估场景的语义合理性与空间连贯性，输出改进建议（如新增或调整物体），驱动 Agent 进行下一轮迭代。

**Physics Critic（物理批评器）**：将场景加载至 Isaac Sim 进行仿真验证，检测重力作用下的物体稳定性与碰撞情况，拒绝不稳定的放置方案。该模块是实现“仿真就绪”场景的核心机制——消融实验表明，加入物理批评后碰撞率从 7.8% 降至 1.9%，稳定性提升至 99.6%（见表 3）。

### 公式推导

本文未提出新的数学公式或理论推导。其核心贡献在于工程架构层面：将生成器与仿真验证器通过 MCP 协议无缝集成，使 Agent 能够像调用工具一样组合使用各模块，实现自适应、可自我纠正的场景生成流程。定量评估中涉及的物理有效性指标（碰撞率、稳定性）基于 trimesh 网格碰撞检测与 Isaac Sim 物理引擎仿真，属于工程度量而非公式推导范畴。

## 实验与分析

### 主结果：场景生成质量与物理稳定性

SAGE 在常见场景类型（卧室、厨房、客厅）上与 **Holodeck** 和 **SceneWeaver** 进行了定量对比。Table 2 汇总了每类 10 个场景的平均结果，覆盖视觉质量（Realism、Functionality、Layout、Completeness，由 GPT-4.1 评分，1–10 分）和物理有效度（碰撞率 Coll.%、稳定性 Stab.%）。

**核心发现：**
- **物理稳定性几乎完美**：SAGE 平均稳定性达 99.9%，碰撞率仅 1.9%；相比之下，Holodeck 稳定性仅 63.8%，碰撞率高达 22.0%。这表明 **simulator-in-the-loop 物理 critic** 是消除穿透与重力失稳的瓶颈组件。
- **视觉质量全面领先**：SAGE 在 Realism（8.8 vs. 7.5）、Functionality（9.5 vs. 8.4）、Layout（7.9 vs. 6.5）、Completeness（8.2 vs. 7.4）四项视觉指标上均优于 Holodeck。
- **场景完整度更高**：SAGE 平均生成 48.2 个物体，远超 Holodeck 的 27.9 个，说明 agentic 框架能更充分地理解用户意图并填充场景。

Figure 3 的定性对比进一步印证：SAGE 在常见房间类型上布局更合理、物体摆放更完整；在开放词汇场景（如“赛博朋克游戏室”）中，SAGE 更忠实地遵循风格提示，而基线方法常出现语义漂移或物体缺失。Figure 4 展示了 SAGE 在健身房、办公室、星空卧室等多样化开放词汇场景下的生成能力，验证了框架的通用性。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/005_Figure_3.jpg]]
*Figure 3: Common and open-vocabulary scene generation comparison. Compared with baselines, SAGE produces more complete scenes with more realistic layouts on common room types, while following the style prompts more faithfully on open-vocabulary queries*

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/006_Figure_4.jpg]]
*Figure 4: Additional open-vocabulary generation. SAGE produces diverse, semantically coherent scenes spanning various styles and functionalities, from Gym and Office spaces to creative themes like “Cyberpunk game den” and “Starry-night bedroom”*

Table 1 从方法能力维度对比了各方案：SAGE 是唯一同时具备 **agentic 框架、文本/图像驱动、开放词汇生成、物理验证、可扩展性** 的方法，这是其性能优势的系统性根源。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/002_Table_1.jpg]]
*Table 1: Comparison of scene generation methods. Our agent-based method uniquely fulfills all criteria, enabling scalable generation of simulator-validated data essential for robotic applications*

---

### 消融实验：视觉 Critic 与物理 Critic 的因果作用

Table 3 报告了 critic 组件的消融结果（5 个场景 × 3 种房间类型的平均）。实验设计为：仅生成器（无 critic）、仅加视觉 critic、仅加物理 critic、两者皆加（完整 SAGE）。

**因果链条：**
- **仅生成器**：碰撞率 7.8%，稳定性 93.3%，视觉质量较低——说明未经反馈的生成流程在物理和语义层面均存在缺陷。
- **加视觉 critic**：视觉质量显著提升，但碰撞率（7.7%）和稳定性（93.3%）几乎无改善——视觉 critic 解决的是语义/空间一致性问题，无法感知物理约束。
- **加物理 critic**：碰撞率骤降至 1.9%，稳定性升至 99.6%——物理 critic 是稳定性的决定性因果旋钮。但视觉质量提升有限。
- **两者结合（完整 SAGE）**：碰撞率进一步降至 0.8%，稳定性达 100.0%，同时视觉质量达到最优——视觉与物理 critic 存在 **互补协同效应**：物理 critic 拒绝不稳定放置后，agent 通过视觉 critic 寻找语义上更合理的替代方案，形成自我纠正闭环。

Figure 5 直观展示了物理验证的效果：基线方法生成的场景在 Isaac Sim 物理模拟后物体发生明显位移和倾倒，而 SAGE 场景在仿真前后保持完全稳定。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/007_Figure_5.jpg]]
*Figure 5: Stability verification. Generated scenes are loaded into IsaacSim for physical validation. Both baselines exhibit displaced objects due to instability, whereas SAGE preserves scene stability before and after simulation*

---

### 下游具身任务：扩展性与泛化

#### Pick-and-Place 与 Mobile Manipulation 策略学习

SAGE 的场景被用于训练操作策略，以验证生成数据的下游价值。Figure 10 和 Figure 11 分别展示了 Pick-and-Place 和 Mobile Manipulation 任务上的扩展曲线。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/015_Figure_10.jpg]]
*Figure 10: Examples and scaling curve on Pick-and-Place. Top left: diverse generation. Bottom left: example trajectory. Right: success rate w.r.t. demo/object counts. More diverse object augmentations improve policy success, narrowing the gap to the privileged agent*

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/016_Figure_11.jpg]]
*Figure 11: Examples and scaling curve on Mobile Manipulation. Left: task overview. Mid-top: diverse generation. Mid-bottom: example trajectory. Right: success rate w.r.t. demo/scene counts. Both baselines omit physics critic and replace text-to-3D object synthesis with retrieval: Baseline 1 mimics SceneWeaver [63]; Baseline 2 further replaces the agent with a fixed pipeline, resembling Holodeck [62]. Diverse SAGE-augmented scenes boost the learned policy’s success and close the gap to the privileged agent, while removing physics critic and object synthesis degrades performance (Baseline 1). Replacing the agent with a static pipeline further reduces success rate (Baseline 2)*

**Pick-and-Place（Figure 10）**：
- 随着场景数量和物体多样性（类别/布局增强）增加，策略成功率呈上升趋势，并逐步缩小与特权运动规划（privileged motion planning）的差距。
- 物体增强的多样性是提升策略鲁棒性的关键：更多样的物体几何和放置位置迫使策略学习更泛化的抓取与放置行为。

**Mobile Manipulation（Figure 11）**：
- SAGE 训练的策略在 SAGE 生成场景上测试成功率达 46.0%，而两个基线（Baseline 1 模仿 SceneWeaver，Baseline 2 模仿 Holodeck）分别仅为 14.4% 和 13.1%（Table 5）。
- 消融显示：移除物理 critic 和 text-to-3D 物体合成后性能显著下降（Baseline 1），进一步将 agent 替换为静态流水线后成功率更低（Baseline 2）。这验证了 **agentic 自改进 + 物理验证** 是生成高质量训练场景的必要条件。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/017_Table_5.jpg]]
*Table 5: Cross-Evaluation. SAGE policies generalize better on out-of-distribution scenes. SAGE even achieves higher success rates on baseline-generated scenes*

#### 跨分布泛化（Table 5）

SAGE 策略展现出更强的跨分布泛化能力：
- 在 SAGE 生成的 out-of-distribution 场景上，SAGE 策略成功率达 46.0%，远超基线策略在各自训练分布外的表现。
- 更值得关注的是，SAGE 策略在基线方法生成的场景上也取得更高成功率，说明 SAGE 场景的物理稳定性为策略提供了更干净的学习信号，避免了不稳定场景引入的噪声。

---

### 失败模式与局限性

尽管 SAGE 在物理稳定性上表现优异，仍存在以下不足：

1. **视觉质量受限于底层模型**：场景的材质细节和物体几何精度受限于 TRELLIS 等 text-to-3D 模型的能力，复杂材质（如金属反光、织物纹理）可能不够真实。
2. **运动规划示范存在失败案例**：抓取姿态预测不准或目标不可达会导致示范质量下降，影响策略学习效率。
3. **场景类型受限**：当前框架仅适用于室内静态场景和刚性物体，尚未扩展到室外环境、铰接或变形物体（尽管 Figure 9 展示了铰接物体的初步集成）。
4. **任务多样性有限**：目前仅在 Pick-and-Place 和 Mobile Manipulation 上验证，未覆盖交互式导航、多机器人协作等更复杂的具身任务。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/014_Figure_9.jpg]]
*Figure 9: Articulated Objects: SAGE can be extended with articulated objects using retrieval from PartNet-Mobility [59]. Top: we show two scenes with multiple articulated objects at closed and open states. Bottom: an action sequence generated with grasp pose prediction and motion planning( Sec.3.2.2) for “pick up the bowl, place it in the drawer, and close the drawer”. Please visit website for full video*

> **注意**：关于 SAGE 在更大规模（如 SAGE-10k 数据集，Figure 6）或多房间场景（Figure 7）上的表现，本文未获得详细定量数据，需手动查阅原文验证。

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/010_Figure_7.jpg]]
*Figure 7: Multi-room open-vocabulary generation. SAGE can be extended to generate multi-room scenes at scale easily by generating the floor plan and then calling generator MCP tools to fill in multiple rooms in parallel*

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/008_Figure_6.jpg]]
*Figure 6: SAGE-10k Dataset: We pre-generated a 10k-scene dataset named SAGE-10k Dataset across 50 room types and 50 styles, including 565K uniquely generated 3D objects. We include the statistics of room types, room examples, and objects per scene in the figure as well. The dataset can be accessed via this link*

### 补充图表

![[assets/figures/papers/paper_list_l2159_https_arxiv_org_abs_2602_10116/figures/012_Figure_8.jpg]]
*Figure 8: Image-conditioned scene generation. Using Qwen3- VL [48], SAGE extracts style and object attributes from reference images to enable image-conditioned scene generation without architectural modifications. The generated scenes are not pixel-aligned but remain semantically consistent with the reference images*

## 方法谱系与知识库定位

### 与现有方法的关系

SAGE 的核心突破在于将 **agentic 自改进机制** 与 **仿真器在环物理验证** 引入 3D 场景生成流程，使其生成结果可直接部署于具身智能训练。与现有工作相比，SAGE 在三个关键维度上实现了系统性改变（见表 1）：

**1. 从固定管线到 Agentic 编排。** 以 **Holodeck** 为代表的 LLM 驱动方法采用固定的生成管线，缺乏对生成结果的自我评估和迭代修正能力。**SceneWeaver** 虽引入了 agent 概念，但其工具调用和流程控制仍受限于预设规则。SAGE 则完全运行在 **Model Context Protocol (MCP)** 之上，agent 作为 MCP 客户端可动态选择和调用生成工具（Scene Initializer、Asset Placer/Mover/Remover），并根据 critic 反馈自主决定下一步操作。这种架构使系统具备了真正的“工具使用”能力，而非简单的流程串联。

**2. 从视觉评估到物理-视觉联合验证。** 现有方法通常仅关注场景的语义和视觉质量，缺乏对物理稳定性的系统验证。SAGE 引入两个互补的 critic：**Visual Critic** 评估语义和空间一致性，**Physics Critic** 则在 Isaac Sim 中验证重力下的稳定性和碰撞情况。消融实验（表 3）表明，仅使用物理 critic 可将碰撞率从 7.8% 降至 1.9%，稳定性提升至 99.6%；而视觉 critic 的加入进一步改善了视觉质量。这种“生成-验证-修正”的闭环是 SAGE 区别于所有 baseline 的核心机制。

**3. 从静态生成到仿真就绪。** Holodeck 和 SceneWeaver 生成的场景在加载到物理仿真器后会出现大量物体位移和穿透（见图 5），无法直接用于机器人策略训练。SAGE 通过 physics critic 的仿真器在环验证，确保每个物体放置都经过物理稳定性检查，最终实现平均碰撞率仅 1.9%、稳定性 99.9% 的仿真就绪场景。

### 适用边界与能力范围

SAGE 的当前能力边界可从场景类型、物体属性和任务覆盖三个维度界定：

- **场景类型：** 框架当前适用于室内静态场景（卧室、厨房、客厅等），已扩展至多房间生成（见图 7）和图像条件生成（见图 8），但尚未覆盖室外环境。
- **物体属性：** 主要处理刚性物体，已初步支持铰接物体（通过 PartNet-Mobility 检索，见图 9），但不支持变形物体和流体等复杂物理材质。
- **任务覆盖：** 验证实验聚焦于 Pick-and-Place 和 Mobile Manipulation 两类任务，尚未扩展到交互式导航、多机器人协作等更复杂的具身任务。

### 局限性与待解决问题

SAGE 在以下方面存在明确局限，需要在后续工作中解决：

1. **视觉质量受限于底层生成模型。** 场景的视觉真实感和物体几何细节依赖于 text-to-3D 模型（如 TRELLIS）的能力，复杂材质和精细结构可能不足。这是当前 text-to-3D 技术的共性瓶颈，而非 SAGE 框架本身的设计缺陷。

2. **物理验证的粒度有限。** Physics critic 主要检查重力稳定性和静态碰撞，不涵盖摩擦力、弹性、物体间动态交互等更复杂的物理属性。这可能导致某些场景在静态测试中通过，但在机器人交互时仍出现不期望的物理行为。

3. **运动规划示范存在失败案例。** 论文明确指出运动规划生成的示范存在抓取不准、目标不可达等失败情况，这可能影响策略学习的效率和最终性能。

4. **场景多样性依赖 prompt 工程。** 虽然 SAGE 支持开放词汇场景生成，但生成质量仍受限于 agent 对 prompt 的理解和工具调用的合理性。极端或模糊的场景描述可能导致生成失败或质量下降。

### 开放问题

基于上述局限，以下开放问题值得后续研究关注：

1. **如何将框架扩展到室外环境以及铰接和变形物体的生成与交互？** 这需要引入新的生成工具和物理验证模块，以及更复杂的场景表示。

2. **能否集成在线强化学习，从模拟数据中进一步缩减 sim-to-real 差距？** SAGE 当前生成的是静态场景，若能与在线 RL 结合，根据策略训练反馈动态调整场景难度和分布，可能进一步提升策略的泛化能力。

3. **能否支持更复杂的具身任务定义与自动任务生成？** 例如通过自然语言描述多步操作序列，自动生成对应的场景、物体和任务目标。

4. **如何进一步提升 text-to-3D 和物理属性的预测精度？** 这可能需要在生成流程中引入更细粒度的物理仿真反馈，或采用更先进的 3D 生成模型。

5. **能否通过 real-robot 闭环验证对生成流水线进行自我改进？** 将真实机器人的交互结果反馈到场景生成流程中，实现从 sim 到 real 再到 sim 的闭环优化。

## 原文 PDF

![[paperPDFs/CVPR_2026/SAGE_Scalable_Agentic_3D_Scene_Generation_for_Embodied_AI.pdf]]
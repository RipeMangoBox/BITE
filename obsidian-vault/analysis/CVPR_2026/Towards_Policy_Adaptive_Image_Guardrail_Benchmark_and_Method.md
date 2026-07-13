---
title: "Towards Policy-Adaptive Image Guardrail: Benchmark and Method"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Policy_Adaptive_Image_Guardrail_Benchmark_and_Method.pdf
project_link: null
code_link: "https://github.com/LAION-AI/CLIP-based-NSFW-Detector"
aliases:
- SV
- TPAIGBM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过自重新描述机制注入不安全语义理解，再通过基于可验证奖励的强化学习进行策略条件对齐，从而解耦语义理解与安全识别
primary_logic: 安全标签本质上依赖于策略定义而非图像固有属性，通过RLVR强化学习可以保持模型通用能力的同时实现策略自适应
claims:
- 在极端策略上训练的模型完全无法跨策略泛化（SFT on L1 在L2–L5上为0%）
- QwenGuard-7B在自己的基准上表现极高（84.6），但在其他安全/通用基准上大幅下降，而我们的RL模型均衡提升安全与通用性能
- 移除自重新描述导致安全性能显著下降（53.22 vs 66.96），验证了该方法对学习细粒度有害模式的必要性
- 两阶段训练（SFT+RL）在UnsafeBench上取得最佳性能（72.16）且保持通用能力稳定
---

# Towards Policy-Adaptive Image Guardrail: Benchmark and Method

> [!tip] 核心洞察
> 安全标签本质上依赖于策略定义而非图像固有属性，通过RLVR强化学习可以保持模型通用能力的同时实现策略自适应

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向策略自适应的图像安全护栏：基准与方法 |
| 英文题名 | Towards Policy-Adaptive Image Guardrail: Benchmark and Method |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01228) · [Code](https://github.com/LAION-AI/CLIP-based-NSFW-Detector) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SafeGuard-VL |
| Dataset | UnsafeBench, SafeEditBench, LlavaGuardBench & General VQA |

> [!tip] 效果简介
> - UnsafeBench 上，总体加权F1-score（9类） 72.2 (Ours Full) vs 43.6 (QwenGuard-7B) (+28.6)。
> - SafeEditBench 上，宏观平均F1-score（5级策略） 49.43 (Ours RL+SafeEditTrain) vs 32.76 (QwenGuard-7B) / 48.68 (Qwen2.5-VL-7B) (较SFT基线+16.67；较最强通用模型+0.75)。
> - LlavaGuardBench & General VQA 上，LlavaGuard F1 / UnsafeBench F1 / General Avg 71.78 / 62.39 / 57.02 (Ours RL) vs 84.57 / 43.56 / 35.98 (QwenGuard-7B) (尽管LlavaGuard下降12.79，但UnsafeBench提升18.83，通用能力提升21.04)。

## 概要

安全护栏（guardrail）是视觉语言模型安全部署的关键防线。然而，现有护栏方法普遍隐含一个脆弱假设：安全策略是固定且普适的。**真实瓶颈**在于，传统视觉语言模型护栏仅在单一固定安全策略下训练，严重过拟合，无法泛化到未见策略，且通用指令遵循能力严重退化。这一瓶颈的根源在于：安全标签本质上依赖于策略定义而非图像固有属性——同一张图像在不同策略下可能被判定为“安全”或“不安全”（Figure 5）。

针对上述问题，本文提出 **SafeGuard-VL**，一个面向策略自适应的图像安全护栏方法。其**核心洞察**是：通过自重新描述（self-recaption）机制注入不安全语义理解，再通过基于可验证奖励的强化学习（RLVR）进行策略条件对齐，从而解耦语义理解与安全识别。方法采用两阶段训练范式（Figure 1）：第一阶段通过自重新描述生成的描述数据教导模型识别图像中的不安全元素，而非直接进行安全/不安全二分类；第二阶段使用GRPO强化学习，使模型根据输入的自然语言策略文本做出策略感知的安全判断。

在**方法谱系与知识库定位**上，SafeGuard-VL区别于以下基线路径：

- **固定分类器路线**：如 **Llama Guard** 、**LlavaGuard** 、**ShieldGemma2**  等，依赖预定义的安全类别体系，策略适应灵活性有限。
- **SFT微调路线**：如 **QwenGuard-7B**，在单一策略数据上监督微调，虽在自身基准上表现极高（LlavaGuardBench F1 84.57），但跨策略泛化能力严重不足（UnsafeBench仅43.56），且通用VQA能力大幅退化（Table 4, Figure 6）。
- **通用VLMs零样本路线**：如 **Qwen2.5-VL-7B**、**LLaVA-V1.6-7B**、**GLM-4V-9B**，缺乏策略感知机制，安全判断与策略脱节。

SafeGuard-VL的**关键创新**在于：① 以自然语言策略描述作为条件输入，实现零样本跨策略泛化（Table 1）；② 自重新描述机制利用Qwen2.5-VL生成初始粗略描述，再由Gemma 27B恢复被抑制的不安全细节，为SFT提供丰富语义监督（Figure 3）；③ RLVR阶段使用策略真实标签作为可验证奖励，在保持通用能力的同时实现策略条件对齐。

**主要结果**（Table 2, Table 4, Table 6）：在UnsafeBench跨策略泛化评估中，SafeGuard-VL Full取得72.2的总体加权F1-score，较QwenGuard-7B（43.6）提升28.6个百分点；在SafeEditBench五级策略评估中，RL模型（49.43）较SFT基线（32.76）提升16.67，且超越最强通用模型Qwen2.5-VL-7B（48.68）。更重要的是，SafeGuard-VL在安全能力与通用能力之间取得了均衡——通用VQA平均分57.02，远高于QwenGuard-7B的35.98（Figure 6），避免了过度特化带来的能力退化。

**证据强度**：上述结论由多维度实验支撑——消融实验证实移除自重新描述导致安全性能从66.96降至53.22（Table 5），验证了该方法对学习细粒度有害模式的必要性；单策略训练多策略评估实验显示，在极端策略（L1或L5）上训练的模型完全无法跨策略泛化（SFT on L1在L2–L5上为0%，Table 3），揭示了现有方法的根本缺陷。

**局限与待验证点**：① 图像编辑工具Nano Banana禁止生成有害内容，因此SafeEditBench仅能做单向编辑（不安全→安全），无法生成双向配对；② RL训练仍依赖固定策略层级数据，对完全任意的、未见过的自然语言策略的泛化性可能仍有局限；③ 论文声明将发布代码但未提供具体仓库链接，可复现性待验证。

### 安全护栏的策略依赖性困境

视觉语言模型（VLM）的快速部署使得图像内容安全审核成为关键基础设施。然而，当前的安全护栏（guardrail）方法面临一个根本性瓶颈：**安全标签本质上依赖于策略定义，而非图像的固有属性**。同一张图像在不同安全策略下可能被判定为“安全”或“不安全”——尤其在策略采用反直觉或非常识性定义时（例如，禁止普通亲密行为但允许性暗示内容），这一矛盾尤为突出（Figure 5）。

### 现有方法的双重失败模式

现有安全护栏普遍采用**单一固定安全策略**下的监督微调（SFT），将任务简化为二分类（safe/unsafe）。这种范式导致两类严重失败：

1. **跨策略泛化崩溃**：在某一极端策略上训练的模型完全无法泛化到其他策略。例如，在L1（最宽松）策略上SFT的模型，在L2–L5上的F1-score为0%（Table 3）。这表明模型学到的是特定策略的“捷径”，而非真正的安全语义理解。

2. **通用能力灾难性退化**：以QwenGuard-7B为代表的SFT安全护栏，在其自身基准LlavaGuardBench上表现极高（84.6），但在其他安全基准（UnsafeBench 43.6）和通用VQA基准（平均36.0）上大幅下降（Figure 6）。这种过度特化使得护栏模型丧失了作为通用VLM的指令遵循与推理能力。

### 现有方法谱系与知识库定位

当前安全护栏方法可分为三类（Table 1）：

- **固定分类体系**：如**Llama Guard**（Inan et al., 2023）和**ShieldGemma2**（Zeng et al., 2024），依赖预定义的危险类别列表，适应新策略需重新定义类别并重新训练。
- **视觉安全护栏**：如**LlavaGuard**（Helff et al., 2024），在视觉-语言模型上SFT，但仍绑定单一策略。
- **通用VLM零样本**：如**Qwen2.5-VL-7B**、**LLaVA-V1.6-7B**、**GLM-4V-9B**，虽具备一定安全判断能力，但缺乏策略条件化机制，无法根据策略文本调整判断标准。

这些方法的共同缺陷在于**将安全识别与策略定义耦合**，导致策略变更时必须重新训练。本文的核心动机在于提出一种**策略自适应的安全护栏**，通过解耦语义理解与策略条件对齐，实现零样本跨策略泛化。

### 核心洞察与解决路径

本文的核心洞察是：**安全判断不是常识推理，而是策略条件推理**。基于此，SafeGuard-VL采用两阶段训练范式：

- **第一阶段（SFT）**：通过**自重新描述（self-recaption）机制**注入不安全语义理解，教导模型描述图像中的不安全元素，而非直接分类。
- **第二阶段（RLVR）**：基于可验证奖励的强化学习（GRPO），使模型学会根据自然语言策略文本进行安全/不安全的条件判断。

这一设计使得模型在保持通用VLM能力的同时，实现策略自适应——在UnsafeBench跨策略泛化上达到72.2的总体F1-score，较QwenGuard-7B提升28.6个百分点（Table 2），且通用能力保持稳定（Table 5）。

## 核心方法与创新机理

SafeGuard-VL 的核心创新在于将安全护栏从“固定策略下的二分类任务”重构为“策略条件化的语义理解与对齐任务”，通过两个关键设计突破现有方法的瓶颈。

### 1. 自重新描述机制：解耦语义理解与安全识别

传统护栏模型（如 **QwenGuard-7B**、**LlavaGuard**）直接在单一安全策略下进行 SFT 二分类训练，导致模型将“不安全”视为图像的固有属性，而非策略依赖的判断。SafeGuard-VL 的**自重新描述机制**从根本上改变了这一范式：

- **问题根源**：通用 VLM（如 Qwen2.5-VL）在安全对齐后倾向于抑制对不安全内容的详细描述，导致其生成的标注数据缺乏细粒度的有害语义信息。
- **解决方案**：采用两阶段生成流程——首先由 Qwen2.5-VL 生成粗略的高层描述（不安全细节被抑制），再由 Gemma 27B 进行最小化编辑，恢复被抑制的不安全语义，生成富含有害细节的描述文本（Figure 3）。
- **训练目标转变**：Stage-1 SFT 不再训练模型输出 `safe/unsafe` 标签，而是教导模型**描述图像中的不安全元素**。这一设计将语义理解与安全判断解耦，为后续的策略条件对齐奠定基础。

消融实验验证了这一机制的关键作用：移除自重新描述后，UnsafeBench 性能从 66.96 骤降至 53.22（Table 5），证明细粒度的有害语义描述对模型学习不安全模式不可或缺。

### 2. 策略感知的 RLVR 对齐：从固定分类到条件推理

现有方法的核心缺陷在于**安全标签本质上依赖于策略定义而非图像固有属性**（Figure 5），但在单一策略下训练的模型无法泛化到未见策略。SafeGuard-VL 通过基于可验证奖励的强化学习（RLVR）实现策略条件对齐：

- **策略条件输入**：模型接收图像与自然语言策略描述，要求根据策略文本判断安全性，而非依赖固定的类别体系（Table 1）。
- **GRPO 训练**：采用 Group Relative Policy Optimization（GRPO）进行强化学习，奖励信号直接来源于策略定义的真实标签（可验证奖励），鼓励模型生成与策略一致的安全判断及理由。
- **跨策略泛化**：与需要重新训练以适应新策略的固定分类器（如 **Llama Guard**、**ShieldGemma2**）不同，SafeGuard-VL 通过自然语言策略接口实现零样本跨策略适应。

Table 3 揭示了这一创新的必要性：在极端策略（L1）上 SFT 训练的模型，在 L2–L5 上 F1-score 为 0%，完全丧失跨策略泛化能力。而 SafeGuard-VL 的两阶段训练在 UnsafeBench 上取得 72.16 的总体 F1-score（Table 5），较仅 SFT 提升 5.2 个百分点。

### 3. 安全能力与通用能力的均衡

传统 SFT 护栏模型存在严重的**过度特化**问题：QwenGuard-7B 在其自身基准 LlavaGuardBench 上达到 84.57，但在 UnsafeBench 上仅 43.56，通用 VQA 平均分仅 35.98（Table 4，Figure 6）。SafeGuard-VL 通过 RLVR 训练，在保持通用指令遵循能力（57.02）的同时，将 UnsafeBench 提升至 62.39，实现了安全与通用能力的均衡（Figure 6 右）。这一特性源于 RLVR 的奖励设计仅约束安全判断的策略一致性，而非压缩模型的通用推理空间。

SafeGuard-VL 采用**两阶段训练范式**，从“理解不安全语义”到“策略条件对齐”逐步构建策略自适应的视觉安全护栏。图 1 给出了高层示意图：第一阶段（SFT）通过自重新描述机制让模型学习图像中与不安全相关的视觉和文本语义；第二阶段（RL）利用基于可验证奖励的强化学习（RLVR），使模型根据输入的自然语言策略文本做出安全/不安全的判别，而非依赖单一固定规则集。

### 输入输出流

推理时，模型接收两个输入：
- **图像**：待判别的视觉内容；
- **策略描述**：以自然语言形式给出的安全策略文本（例如“禁止展示任何形式的武器，包括历史或教育场景中的展示”）。

模型输出为该图像在给定策略下的**安全判断**（safe/unsafe），并附有基于策略文本的判别理由。这种设计使同一图像在不同策略下可以产生不同的判断结果——安全标签本质上依赖于策略定义，而非图像的固有属性。

### 模块关系与数据流

整个框架由四个核心模块串联构成：

1. **自重新描述数据生成**（Stage-1 前置）：利用 Qwen2.5-VL 对不安全图像生成初始高层描述（通常抑制了不安全细节），再由 Gemma 27B 对描述进行最小化编辑，**恢复被抑制的不安全语义**，生成含有丰富有害细节的重新描述。该机制的关键在于让模型从自身分布中采样并自我修正，从而获得细粒度的不安全模式标注（图 3）。

2. **Stage-1：安全语义 SFT**：使用上述自重新描述数据对基础 VLM 进行监督微调。与现有方法直接训练二分类（safe/unsafe）不同，该阶段**教导模型描述图像中的不安全元素**，而非直接做出安全判断。这使模型首先建立起对不安全语义的理解能力，为后续策略对齐奠定基础。

3. **Stage-2：策略感知 RLVR**：在 SFT 模型基础上，使用 GRPO（Group Relative Policy Optimization）进行强化学习。奖励信号基于策略定义的真实标签进行验证：模型需根据输入策略文本判断图像安全与否，并生成符合策略逻辑的判别理由。这一阶段使模型学会**将第一阶段学到的语义理解能力与策略条件进行对齐**，实现策略自适应的安全判别。

4. **推理时策略条件输入**：部署时，模型接收图像与任意自然语言策略描述，输出策略相关的安全判断。由于训练中已学习策略条件映射，模型展现出零样本跨策略泛化能力。

### 核心设计逻辑

现有安全护栏（如 **Llama Guard**、**LlavaGuard**、**ShieldGemma2**）的核心瓶颈在于：仅在单一固定安全策略下训练，导致严重过拟合，无法泛化到未见策略，且通用指令遵循能力严重退化。SafeGuard-VL 通过以下因果路径解决这一问题：

- **解耦语义理解与安全识别**：Stage-1 SFT 专注于不安全语义的描述学习，不绑定任何特定策略；Stage-2 RLVR 则专注于策略条件对齐。这种解耦使得模型在适应新策略时无需重新学习视觉语义。
- **RLVR 保持通用能力**：相比 SFT 直接拟合固定标签，RLVR 通过策略条件的奖励机制进行优化，避免了过拟合单一策略导致的通用能力退化。实验表明，RL 训练后的模型在安全基准和通用 VQA 基准上均优于纯 SFT 基线（表 4、图 6）。

> **注意**：关于 GRPO 的具体公式定义和奖励函数的形式化表达，原文未在已分析部分中提供完整数学描述，此部分细节需查阅原文方法章节进行核实。

![[assets/figures/papers/paper_list_l830_https_arxiv_org_abs_2603_01228/figures/001_Figure_1.jpg]]
*Figure 1: High-level illustration of our SafeGuard-VL. Unlike prior guardrails that fit only the fixed safety policy, SafeGuard-VL is designed from the perspective of cross-policy adaptability and robustness. In Stage 1 (SFT), the model learns general unsafe-related visual and textual semantics through data constructed using our self-recaption mechanism. In Stage 2 (RL), the model is optimized to perform policy-aware safe/unsafe discrimination, adapting its decisions to different policy definitions rather than relying on a single fixed rule set. This two-stage framework enables SafeGuard-VL to generalize to unseen or shifting safety policies during testing*

### 2.1 自重新描述数据生成模块（Self-Recaption）

该模块的目标是为第一阶段SFT构造包含丰富不安全语义描述的图文对，从而教会模型“描述”不安全元素，而非直接分类。其流程如下：

1. **初始描述生成**：将不安全图像输入基线模型 **Qwen2.5-VL**，令其生成高层语义描述。由于该模型的安全对齐约束，生成的描述倾向于抑制或省略不安全细节。
2. **不安全语义恢复**：将初始描述送入重描述模型 **Gemma 27B**，该模型执行最小化编辑，恢复被抑制的不安全语义，输出保留原始结构但显式包含有害描述的增强文本。
3. **训练对构造**：最终形成“图像-增强不安全描述”的SFT训练对，使模型学会识别并表述图像中的细粒度有害模式。

该机制的核心洞察在于：安全对齐模型本身具备识别不安全内容的能力，只是输出阶段被抑制；通过自重新描述，可以在不依赖外部标注的情况下释放这一能力。

### 2.2 策略感知强化学习模块（Policy-Aware RLVR）

第二阶段采用基于可验证奖励的强化学习（RLVR），具体使用 **Group Relative Policy Optimization (GRPO)** 算法（Shao et al., 2024），将策略文本作为条件输入，使模型学会根据任意自然语言策略进行安全判断。

**奖励设计**：奖励信号基于模型输出的安全判断与给定策略下的真实标签是否一致。由于安全标签完全由策略定义，该奖励是可验证的，无需人工偏好标注。

**训练目标**：模型被鼓励生成既给出判断又提供策略依据的响应，而非简单输出“safe/unsafe”。这一设计使模型在推理时能够接收策略描述与图像，输出策略相关的安全判断，实现零样本跨策略泛化。

### 2.3 两阶段训练范式

完整训练流程如下：

- **Stage-1：安全语义SFT** — 使用自重新描述数据对基础模型 **Qwen2.5-VL-7B** 进行监督微调，学习识别和描述图像中的不安全元素。
- **Stage-2：策略感知RLVR** — 在SFT模型基础上，使用GRPO进行强化学习，奖励函数基于策略条件的安全判断准确性，使模型将第一阶段学到的语义理解与策略定义对齐。

消融实验（Table 5）验证了该范式的有效性：移除自重新描述导致UnsafeBench性能从66.96降至53.22；在SFT后加入RLVR进一步提升5.2个百分点至72.16。

### 2.4 公式说明

本文未在正文中给出独立的数学公式推导。方法的核心机制通过流程描述和实验验证呈现，而非形式化建模。若需精确的GRPO目标函数或奖励函数形式化定义，需查阅引用源（Shao et al., 2024）或等待代码发布后从实现中提取。

## 实验与关键发现

### 核心瓶颈的实证揭示：单一策略SFT的跨策略泛化灾难

传统安全护栏的根本缺陷并非简单的“性能不足”，而是**策略过拟合**。SafeEditBench的策略适应性分析（Table 3）提供了决定性证据：当模型在某一极端策略（如L1最宽松或L5最严格）下进行SFT训练后，在其余四级策略上的F1-score直接降至**0%**。这意味着模型并未学习到“根据规则判断安全”的元能力，而是机械地记忆了训练策略下的标签分布。一旦策略定义发生翻转（例如L1允许色情但禁止普通亲密行为，而L5则相反），模型完全无法适应。

![[assets/figures/papers/paper_list_l830_https_arxiv_org_abs_2603_01228/figures/009_Table_3.jpg]]
*Table 3: Policy adaptability analysis on our challenging SafeEditBench. The model is trained at a single policy level (L1-L5) and evaluated at all five levels. Training on extreme policies (e.g., L1 or L5) results in a significant performance drop on other policies, revealing a key limitation: current safety guardrail methods lack basic cross-policy generalization ability*

这一发现揭示了问题的本质：**安全标签并非图像的固有属性，而是策略定义的函数**。Figure 5中的示例直观展示了这一悖论——同一张图像在L1下被标记为“Safe”，在L5下却被标记为“Unsafe”。传统方法将安全判断建模为固定的图像分类任务，从根本上违背了这一策略依赖性。

### 主实验结果：安全-通用能力的再平衡

**UnsafeBench跨策略泛化**（Table 2）。SafeGuard-VL-Full在9类有害内容的加权F1-score上达到**72.2**，远超安全专用模型QwenGuard-7B的43.6（+28.6），也显著优于通用模型Qwen2.5-VL-7B的58.1。值得注意的是，仅经过SFT阶段的SafeGuard-VL-SFT已取得67.0，验证了自重新描述机制对不安全语义学习的有效性。

**安全与通用能力的权衡**（Table 4, Figure 6）。QwenGuard-7B在其专属基准LlavaGuardBench上表现极高（84.6），但在UnsafeBench上骤降至43.6，通用VQA平均分仅36.0——这是典型的**灾难性遗忘与基准过拟合**。相比之下，SafeGuard-VL-RL在LlavaGuardBench上虽降至71.8，但UnsafeBench提升至62.4，通用能力大幅回升至57.0。Figure 6将这一权衡可视化：左侧QwenGuard呈现极端的“尖峰”分布，右侧SafeGuard-VL-RL则实现了安全与通用能力的均衡。

**SafeEditBench五级策略评估**（Table 6）。在覆盖从极端宽松到极端严格的五级策略基准上，SafeGuard-VL-RL+SafeEditTrain取得49.43的宏观平均F1，较QwenGuard-7B的32.76提升16.67，甚至略优于最强通用模型Qwen2.5-VL-7B的48.68。这一结果表明，策略感知的RLVR训练使模型能够在不同策略定义间灵活切换，而非固守单一标准。

### 消融实验：自重新描述与RLVR的因果贡献

Table 5的消融实验逐层拆解了两个核心设计的贡献：

1. **自重新描述（Recaption）的因果效应**：移除重新描述后（w/o Recap SFT），UnsafeBench性能从66.96降至53.22（-13.74）。这证实了Gemma 27B恢复的不安全语义描述是模型学习细粒度有害模式的关键——仅靠Qwen2.5-VL的粗略描述不足以建立鲁棒的不安全语义理解。

2. **RLVR的增量收益**：在SFT基础上加入策略感知RLVR（Ours Full），UnsafeBench进一步提升至72.16（+5.2）。这验证了两阶段设计的必要性：SFT赋予模型语义理解，RLVR则通过可验证奖励将这一理解与具体策略定义对齐。

3. **通用能力的稳定性**：所有变体在通用VQA上的表现保持在53.09–56.92的窄区间内，表明自重新描述和RLVR均未损害模型的通用指令遵循能力。这与QwenGuard-7B的急剧退化形成鲜明对比。

### 定性分析：策略感知与指令遵循的双重优势

Figure 7的定性对比揭示了SafeGuard-VL-RL相对于QwenGuard的两个关键优势：

- **策略感知的安全判断**：在L2策略下（明确允许历史/教育性枪支展示），QwenGuard错误地将博物馆展品标记为“unsafe”，忽略了策略上下文的例外条款。SafeGuard-VL-RL则正确识别出教育场景，输出“safe”。
- **鲁棒的指令遵循**：当给定简单的多选题指令时，QwenGuard无视用户意图，输出冗长的JSON格式安全理由。SafeGuard-VL-RL严格遵循格式要求，仅返回正确选项。

Figure 8展示了SafeGuard-VL两阶段的渐进式能力提升：SFT阶段使模型能够详细描述有害语义（“理解”），Full阶段则成功将这一理解转化为精确的拒绝决策（“行动”），而通用模型完全未能检测到风险。

### 失败模式与局限性

尽管SafeGuard-VL在跨策略泛化上取得了显著进展，以下局限性需在解读结果时审慎考虑：

1. **RL训练的策略覆盖局限**：RLVR训练仍依赖于预定义的五级策略数据。虽然模型展示了跨策略泛化能力，但对完全任意的、开放式的自然语言策略（例如用户自定义的复杂规则组合）的泛化性尚未经过充分验证。Table 3中SFT模型的极端失败表明，一旦策略分布超出训练覆盖范围，性能可能急剧下降。

2. **SafeEditBench的单向编辑偏差**：由于图像编辑工具Nano Banana禁止生成有害内容，SafeEditBench的数据构建只能进行“不安全→安全”的单向编辑，无法生成双向配对。这可能使模型对“安全图像被恶意编辑为不安全”的场景缺乏充分训练。

3. **LlavaGuardBench的性能下降**：SafeGuard-VL-RL在LlavaGuardBench上的F1-score（71.8）低于QwenGuard-7B（84.6），下降12.8。这表明策略感知训练可能在一定程度上牺牲了对特定固定策略的极致优化，换取更广泛的策略适应性——这一权衡在实际部署中是否可接受，取决于应用场景对策略固定性的要求。

4. **可复现性待验证**：论文声明将发布代码，但截至分析时仅提供了基于CLIP的NSFW检测器链接，SafeGuard-VL的核心训练代码尚未公开。上述所有实验结论的独立验证需等待完整代码发布。

![[assets/figures/papers/paper_list_l830_https_arxiv_org_abs_2603_01228/figures/007_Table_1.jpg]]
*Table 1: Comparison of policy adaptation mechanisms across existing safety guardrails and benchmarks. Existing methods rely on fixed taxonomies or pre-defined blocks with limited adaptation flexibility, whereas our method supports arbitrary natural language policies with zero-shot cross-policy generalization*

![[assets/figures/papers/paper_list_l830_https_arxiv_org_abs_2603_01228/figures/008_Table_2.jpg]]
*Table 2: Cross-policy generalization performance comparison on UnsafeBench [34] across 9 harmful categories. Results show significant improvements over general-purpose models and the safety-focused Qwen-Guard-7B baseline. Results of other baselines are directly cited*

![[assets/figures/papers/paper_list_l830_https_arxiv_org_abs_2603_01228/figures/010_Table_4.jpg]]
*Table 4: Performance comparison across safety and general VQA benchmarks. QwenGuard-7B achieves high scores on its own LlavaGuardBench but suffers significant degradation on other safety (UnsafeBench) and general benchmarks. In contrast, with the same training data, simply changing to RL training improves performance on both safety and general benchmarks, demonstrating better generalization and avoiding the drawbacks of over-specialization in existing safety models*

![[assets/figures/papers/paper_list_l830_https_arxiv_org_abs_2603_01228/figures/013_Table_5.jpg]]
*Table 5: Ablation study on the effectiveness of recaption and RL training. Removing recaption (w/o Recap) leads to a drop in safety performance, confirming that our carefully designed captions help the model learn fine-grained harmful patterns. Further applying RL after SFT yields the best performance on UnsafeBench (+5.2 over SFT-only), validating our two-stage training strategy. General capability remains stable across variants*

## 定位与知识库关联

### 1. 与现有安全护栏的关系

SafeGuard-VL 的定位是对现有视觉安全护栏范式的根本性修正。传统方法——包括 **Llama Guard** 、**LlavaGuard** 、**QwenGuard-7B** 以及谷歌的 **ShieldGemma2** ——共享一个核心假设：安全标签是图像的内在属性，因此模型只需在单一、固定的安全策略下学习“安全/不安全”的二分类边界即可。这一假设的直接后果是严重的策略过拟合：在 SafeEditBench 上，当模型仅在极端策略（如 L1 最宽松或 L5 最严格）上训练时，其对其他策略的泛化能力降至零（Table 3，SFT on L1 在 L2–L5 上为 0%）。这暴露了现有方法的根本瓶颈：它们学习的是特定策略的判别边界，而非安全语义本身。

SafeGuard-VL 通过两个关键设计打破这一瓶颈。其一，将训练目标从“给定图像判断是否安全”重构为“给定图像和策略，判断在该策略下是否安全”，使策略成为模型输入的一部分而非隐式编码在参数中。其二，通过两阶段训练解耦语义理解与策略对齐：第一阶段 SFT 使用自重新描述机制教导模型描述图像中的不安全元素（而非直接分类），第二阶段 RLVR 基于策略真实标签进行对齐。这种设计使 SafeGuard-VL 在方法谱系中位于“策略条件安全推理”这一新兴范式，区别于现有的“固定策略安全分类”范式。

### 2. 与通用视觉语言模型的关系

SafeGuard-VL 以 **Qwen2.5-VL-7B** 为基座模型，但其训练策略与直接使用通用 VLM（如 **LLaVA-V1.6-7B**、**GLM-4V-9B**）进行安全判断有本质区别。通用 VLM 在安全任务上的核心缺陷在于：它们缺乏对不安全语义的细粒度识别能力，且无法根据策略文本调整判断标准。SafeGuard-VL 的自重新描述机制正是针对这一缺陷设计——它利用 Qwen2.5-VL 生成初始粗略描述，再由 Gemma 27B 恢复被抑制的不安全细节，从而在 SFT 阶段为模型注入通用 VLM 天然缺乏的不安全语义理解能力。

更重要的是，SafeGuard-VL 的 RLVR 阶段解决了 SFT 方法的另一个致命问题：过度特化导致通用能力崩溃。QwenGuard-7B 在自己的基准 LlavaGuardBench 上达到 84.6，但在 UnsafeBench 上仅 43.6，通用 VQA 平均分仅 36.0（Table 4，Figure 6）。相比之下，SafeGuard-VL-RL 在 UnsafeBench 上达到 62.4，通用能力保持 57.0，实现了安全与通用能力的均衡。这表明 RLVR 的奖励机制（基于策略真实标签的可验证奖励）天然具有防止灾难性遗忘的特性，因为模型被鼓励在保持语言能力的前提下学习策略对齐。

### 3. 适用边界与局限

**适用场景**：SafeGuard-VL 适用于需要根据动态、多样化安全策略进行图像内容审核的场景。其策略条件输入机制使其在以下情境中具有优势：（1）平台需要同时服务多个具有不同安全标准的地区或用户群；（2）安全策略频繁更新，无法为每次更新重新训练模型；（3）需要零样本泛化到未见策略。

**已知局限**：

1. **数据构造的单向性**：SafeEditBench 使用 Nano Banana（Gemini 的图像生成器）将不安全图像编辑为安全版本，但该工具禁止生成有害内容，因此无法进行反向编辑（将安全图像转为不安全）。这意味着 SafeEditBench 仅包含“不安全→安全”的单向配对，可能限制了模型对安全图像中潜在风险的识别能力。

2. **策略泛化的边界未充分验证**：虽然 SafeGuard-VL 在 SafeEditBench 的五级策略上展示了跨策略泛化，但这些策略仍然共享相同的类别框架（仅在包含/排除某些类别上变化）。对于完全任意的、开放式的自然语言策略（例如“禁止任何可能引起不适的图像，但允许医学教育用途的解剖图像”），其泛化性尚未得到系统性验证。论文承认 RL 训练仍依赖于固定的策略层级数据，这是一个需要手动验证的开放问题。

3. **自重新描述的偏差风险**：自重新描述机制依赖 Gemma 27B 恢复不安全细节，若该模型本身存在安全语义的认知偏差（例如对某些文化背景下的不安全内容识别不足），这些偏差将通过 SFT 阶段传递至 SafeGuard-VL。论文未对此类偏差进行分析。

4. **可复现性待验证**：论文声明将发布代码，但未提供具体的 GitHub 仓库链接（仅引用了 LAION 的 CLIP-based NSFW Detector 仓库作为相关资源），实验的可复现性需要等待正式发布后验证。

### 4. 开放问题

1. **多模态策略扩展**：当前 SafeGuard-VL 的策略输入为纯文本。如何扩展至多模态策略（例如包含视觉示例的策略，如“禁止类似[示例图像]的内容”）是一个自然且具有实际价值的扩展方向。

2. **开放式策略的泛化保证**：RLVR 是否能在完全脱离预定义类别的、开放式的自然语言策略上保持泛化？当前实验仅在五级预定义策略上验证，这一问题的答案直接影响该方法在实际部署中的可靠性。

3. **SFT 数据偏差的传播与放大**：第一阶段 SFT 的描述数据若包含偏差（例如对特定群体、文化符号的不安全语义过度或不足标注），这些偏差在第二阶段 RLVR 中是被纠正还是被强化？这关系到策略对齐的公平性。

4. **与基于规则系统的混合架构**：SafeGuard-VL 的纯神经网络方法在处理边界清晰、可精确枚举的安全规则时可能不如基于规则的系统可靠。将 SafeGuard-VL 与轻量级规则引擎结合，在保证灵活性的同时提升确定性规则的执行精度，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Policy_Adaptive_Image_Guardrail_Benchmark_and_Method.pdf]]

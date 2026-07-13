---
title: "UniMo: Unified Motion Generation and Understanding with Chain of Thought"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/UniMo:_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought.pdf"
project_link: null
code_link: "https://github.com/GuocunWang/UniMo"
aliases:
- UniMo
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入运动一致的思维链（CoT）推理与组相对策略优化（GRPO），将单步预测转化为结构化推理与多任务联合优化，并按组级施加任务特定奖励。
primary_logic: 通过将运动渲染为视频并利用VLM生成运动一致的CoT，弥合文本-运动语义鸿沟；用GRPO对运动令牌组进行优化，缓解逐令牌预测的累积误差，并使生成与理解任务相互促进。
claims:
- UniMo在T2M任务的Top-1 R-Precision上达到0.539，超过所有对比方法（Table 1）。
- UniMo在M2T任务的BLEU@1、BLEU@4、ROUGE-L、CIDEr、BertScore上全面超越先前最佳方法MotionLLM（Table 2）。
- 引入CoT后，T2M的Top-1 R-Precision从0.384提升至0.460，结合GRPO奖励后FID降至0.177（Table 3）。
- 统一T2M+M2T多任务训练相比单任务T2M，在RL后FID从0.201降至0.177，CIDEr从31.05升至46.69（Table 4, 5）。
---

# UniMo: Unified Motion Generation and Understanding with Chain of Thought

> [!tip] 核心洞察
> 通过将运动渲染为视频并利用VLM生成运动一致的CoT，弥合文本-运动语义鸿沟；用GRPO对运动令牌组进行优化，缓解逐令牌预测的累积误差，并使生成与理解任务相互促进。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniMo：基于思维链的统一运动生成与理解 |
| 英文题名 | UniMo: Unified Motion Generation and Understanding with Chain of Thought |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.12126) · [Code](https://github.com/GuocunWang/UniMo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniMo |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (T2M) 上，R-Precision Top-1 ↑ 0.539 ± 0.003 vs 0.521 ± 0.002 (MoMask) (+0.018)；FID ↓ 0.177 ± 0.004 vs 0.045 ± 0.002 (MoMask) (+0.132 (worse))；Diversity ↑ 10.042 ± 0.076 vs 9.908 ± 0.102 (MotionLLM) (+0.134)。
> - HumanML3D (M2T) 上，BLEU@1 ↑ 63.10 vs 54.53 (MotionLLM) (+8.57)；CIDEr ↑ 46.69 vs 33.74 (MotionLLM) (+12.95)。

## 概要

**问题瓶颈**：现有基于 LLM 的运动生成方法普遍采用 next-token 预测范式，直接逐令牌生成运动序列，导致累积预测误差放大；同时，文本指令与运动之间的语义对应关系弱，难以学习细粒度动作生成。统一运动生成与理解任务面临文本-运动语义鸿沟和序列级优化困境两大核心挑战。

**核心方法与洞察**：UniMo 提出两条关键改进路径。其一，将运动序列渲染为视频，利用视觉语言模型 **Qwen2.5-VL-72B** 生成与运动一致的思维链（CoT）推理注解，弥合文本-运动语义鸿沟。其二，在监督微调（SFT）冷启动后，采用**组相对策略优化（GRPO）**进行强化学习后训练，对运动令牌组施加任务特定奖励（运动相似性、语义相似性、字幕相似性），缓解逐令牌预测的累积误差，并使生成与理解任务相互促进。

**方法定位**：UniMo 属于 LLM-based 统一运动生成与理解框架，与 **MotionGPT**（Jiang et al., 2023）和 **MotionLLM**（Wu et al., 2024a）等同类工作相比，关键区别在于引入结构化 CoT 推理与 GRPO 组级优化，而非仅依赖交叉熵损失的 SFT。与同期 CoT-based 方法 **Motion-R1**（Ouyang et al., 2025）相比，UniMo 进一步将 CoT 与强化学习奖励机制结合，实现多任务联合优化。

**主要结果**：在 HumanML3D 数据集上，UniMo 在文本到运动（T2M）的 Top-1 R-Precision 上达到 **0.539**，超过所有对比方法；在运动到文本（M2T）的 BLEU@1 和 CIDEr 上分别达到 **63.10** 和 **46.69**，全面超越先前最佳方法 MotionLLM。消融实验证实，CoT 推理和 GRPO 奖励组件对性能提升均有显著贡献，统一多任务训练进一步带来协同增益。需注意，T2M 的 FID 指标（0.177）仍落后于 **MoMask**（Guo et al., 2024）的 0.045，表明纯重建保真度并非 UniMo 的绝对优势。



### 问题背景

人类运动生成与理解是计算机视觉与图形学中的核心课题，涵盖文本到运动生成（Text-to-Motion, T2M）和运动到文本描述（Motion-to-Text, M2T）两个互为镜像的任务。前者要求模型根据自然语言指令合成逼真的人体动作序列，后者则需从运动数据中提取语义准确的文本描述。这两个任务在具身智能、虚拟角色动画、人机交互等场景中具有广泛的应用前景。

近年来，大语言模型（LLM）的兴起为统一处理多模态任务提供了新的范式。研究者开始尝试将连续的运动序列离散化为运动令牌（motion tokens），并将T2M和M2T建模为序列到序列的生成问题，从而借助LLM强大的序列建模能力实现运动生成与理解的统一。

### 现有方法缺口

尽管基于LLM的统一运动建模方法取得了初步进展，但现有工作仍面临两个根本性瓶颈：

**瓶颈一：next-token预测范式与运动序列的结构失配。** LLM原生采用逐令牌自回归预测的生成方式，而人体运动序列具有强时空约束——单个关节的微小偏差可能导致整体动作的物理不合理。逐令牌预测缺乏对运动组块的整体规划能力，容易产生累积预测误差，表现为动作抖动、滑步或肢体穿透等现象。现有方法（如**MotionGPT**，Jiang et al., 2023；**MotionLLM**，Wu et al., 2024a）虽然将运动令牌化后接入LLM，但并未从训练范式层面解决这一失配问题。

**瓶颈二：文本指令与运动之间的语义对应弱。** 自然语言描述通常高度概括（如“一个人向前走并挥手”），而运动序列包含精细的时空细节（如关节角度、速度曲线、动作过渡）。这种粒度差异导致模型难以学习细粒度的动作生成能力，尤其在涉及顺序动作组合或空间精确描述时表现不佳。直接使用原始文本描述进行监督微调，无法为模型提供足够的中间推理线索来弥合这一语义鸿沟。

### 本文动机

针对上述瓶颈，本文提出UniMo框架，核心动机包含两个层面：

1. **引入运动一致的思维链（Chain of Thought, CoT）推理。** 不同于直接建立文本到运动令牌的映射，UniMo要求模型先生成结构化的推理链——逐步规划动作类型、身体部位参与、时间顺序和空间关系——再基于文本和CoT共同生成运动令牌。这一设计将单步预测转化为结构化推理过程，为模型提供了弥合文本-运动语义鸿沟的中间表征。CoT数据通过将运动序列渲染为视频并用视觉语言模型（Qwen2.5-VL-72B）自动标注获得，确保推理链与运动内容一致。

2. **采用组相对策略优化（GRPO）进行后训练。** 在监督微调冷启动后，UniMo引入GRPO强化学习阶段，在运动令牌组级别施加任务特定奖励（运动相似性、语义相似性、字幕相似性），而非逐令牌优化。这一策略直接缓解了逐令牌预测的累积误差问题，同时使T2M和M2T任务在统一训练中相互促进——生成任务提升运动表示的语义判别力，理解任务增强模型对运动细节的感知能力。

通过上述设计，UniMo旨在实现运动生成与理解的统一框架，在保持生成多样性和语义准确性的同时，提供可解释的推理过程。



## 核心方法与创新机理

UniMo 的核心创新并非单纯引入更强的骨干网络，而是针对“LLM 直接预测运动令牌”这一范式的两个根本瓶颈进行了系统性改造：**文本-运动语义鸿沟**与**逐令牌预测的累积误差**。其解决方案围绕两条因果主线展开——运动一致的思维链推理与组相对策略优化。

### 1. 运动一致的思维链推理

传统的 T2M/M2T 方法直接从文本映射到运动令牌，或反之。UniMo 引入一个中间推理层：**运动一致的思维链**。其构建方式为：将 HumanML3D 中的运动序列通过 Blender 渲染为视频片段，再使用 Qwen2.5-VL-72B 生成结构化的、按时间顺序描述动作的推理链。这一过程弥合了简短文本描述与复杂运动序列之间的语义鸿沟——CoT 注解扩展了语言空间，引入了更丰富的动作细节和时序逻辑。消融实验证实了 CoT 的关键作用：引入 CoT 后，T2M 的 Top-1 R-Precision 从 0.384 提升至 0.460，M2T 的 BLEU@1 从 58.43 提升至 63.10。

### 2. 组相对策略优化

LLM 的 next-token 预测范式在运动生成中面临累积误差问题——单令牌的微小偏差在长序列中逐级放大。UniMo 采用 GRPO 作为后训练策略，其核心创新在于**在运动令牌组级别**而非单令牌级别进行优化：对同一输入采样 $G=8$ 个完整输出序列，以组内相对优势估计代替传统 critic 网络，从而对结构正确性和语义对齐施加全局约束。

GRPO 的目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = E_c \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)} \hat{A}_i, \mathrm{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)}, 1-\varepsilon, 1+\varepsilon \right) \hat{A}_i \right) \right] - \beta \cdot D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}})$$

其中 $\hat{A}_i$ 由组内奖励标准化计算，$D_{\mathrm{KL}}$ 正则项约束策略不偏离参考模型过远。

### 3. 任务特定的多维度奖励设计

GRPO 的奖励函数由三个组件构成，分别从运动真实度、语义对齐和字幕质量三个维度施加监督：

- **运动相似性奖励**：生成运动 $\hat{\mathbf{m}}$ 与真实运动 $\mathbf{m}$ 在预训练运动编码器空间中的余弦相似度，鼓励逼真的运动动力学。
- **语义相似性奖励**：生成运动 $\hat{\mathbf{m}}$ 与输入文本 $T$ 在共享嵌入空间中的余弦相似度，确保运动与指令语义对齐。
- **字幕相似性奖励**：生成字幕 $\hat{T}$ 与参考字幕 $T$ 的 CLIP 文本嵌入余弦相似度，并乘以 2 以匹配 T2M 奖励的量级。

消融实验表明，三个奖励组件协同作用：结合 CoT 与全部三种奖励后，T2M 的 FID 降至 0.177，M2T 的 CIDEr 达到 46.69，两者均达到最优水平。

### 4. 统一多任务训练的协同效应

UniMo 将 T2M 和 M2T 统一为同一 LLM 的序列生成任务，通过 SFT 冷启动后进行联合 GRPO 优化。消融实验证实了统一建模的协同增益：相比单任务 T2M 训练，统一训练在 RL 后 FID 从 0.203 降至 0.177，Top-1 R-Precision 从 0.529 提升至 0.539；相比单任务 M2T 训练，CIDEr 从 42.13 提升至 46.69。这表明生成与理解任务在共享表示空间中相互促进，而非相互干扰。



UniMo 的整体框架围绕一个核心思路展开：**将运动生成与理解统一为结构化的思维链（Chain-of-Thought, CoT）推理过程**，并通过两阶段训练——监督微调（SFT）冷启动和组相对策略优化（GRPO）强化学习后训练——实现文本与运动模态的深度对齐。图 1 给出了完整的训练流水线概览。

### 模块组成与数据流

系统由四个关键模块构成，形成“离散化→推理→生成→优化”的闭环：

1. **VQ-VAE 运动令牌化器**：作为系统的基础设施，该模块在训练后冻结。它将连续的人体运动序列 $\mathbf{m}_{1:T}$ 编码为潜在向量 $\mathbf{z}_{1:T'}$，再通过码本 $\mathcal{C}$ 的最近邻查找量化为离散的运动令牌 $\hat{\mathbf{z}}_{1:T'}$。解码器则负责将令牌序列重建回运动。其训练目标为：
   $$\mathcal{L}_{\mathrm{VQ}} = \mathcal{L}_{\mathrm{recon}} + \underbrace{\|\mathbf{z}_{1:T'} - \mathrm{sg}[\hat{\mathbf{z}}_{1:T'}]\|_2}_{\mathcal{L}_{\mathrm{embed}}} + \underbrace{\|\mathrm{sg}[\mathbf{z}_{1:T'}] - \hat{\mathbf{z}}_{1:T'}\|_2}_{\mathcal{L}_{\mathrm{commit}}}$$
   该模块将连续的、高维的运动数据转化为 LLM 可处理的离散序列，是整个统一框架的模态桥梁。

2. **CoT 数据构建模块**：这是弥合文本-运动语义鸿沟的关键创新。流程如图 2 所示：首先将 HumanML3D 数据集中的运动序列通过 Blender 渲染为视频片段，然后利用多模态大模型 Qwen2.5-VL-72B 对视频进行结构化推理，生成与运动严格一致的 CoT 注解。这些注解以“动作-时序”结构组织，例如先描述躯干运动、再逐步刻画四肢细节，从而将模糊的文本描述扩展为丰富的推理轨迹。

3. **LLM 骨干（Qwen2.5-3B-Instruct）**：扩展词汇表以容纳运动令牌后，该模型作为统一的序列生成器。在 T2M 任务中，输入为文本指令，模型首先生成 CoT 推理链，再基于文本和 CoT 逐步生成运动令牌；在 M2T 任务中，输入为运动令牌序列，模型同样先输出 CoT 分析，再生成文本描述。这种“先推理、后生成”的范式将单步预测转化为结构化决策过程。

4. **GRPO 强化学习阶段**：在 SFT 冷启动之后，模型进入 RL 后训练阶段。GRPO 对每个输入提示采样 $G=8$ 个完整序列，在组内计算归一化优势函数 $\hat{A}_i$，优化目标为：
   $$\mathcal{I}_{\mathrm{GRPO}}(\theta) = E_c \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)} \hat{A}_i, \mathrm{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)}, 1-\varepsilon, 1+\varepsilon \right) \hat{A}_i \right) \right] - \beta \cdot D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}})$$
   与逐令牌优化不同，GRPO 在运动令牌组级别施加任务特定奖励，有效缓解了 next-token 预测的累积误差问题。奖励信号由三个组件构成：
   - **运动相似性奖励** $r_{\mathrm{motion}}$：生成运动与真实运动在预训练运动编码器空间中的余弦相似度；
   - **语义相似性奖励** $r_{\mathrm{semantic}}$：生成运动与输入文本在共享嵌入空间中的余弦相似度；
   - **字幕相似性奖励** $r_{\mathrm{caption}}$：生成字幕与参考字幕的 CLIP 文本嵌入余弦相似度（放大一倍以匹配 T2M 的奖励量级）。

### 训练流程

整个训练分为两个阶段：
- **SFT 阶段**：先在 T2M 任务上预训练 10 个 epoch，使模型适应运动模态；随后在 T2M 和 M2T 联合任务上微调 10 个 epoch，建立双向的文本-运动映射。
- **RL 阶段**：使用 GRPO 训练 14,000 步，学习率 $5 \times 10^{-5}$，梯度裁剪阈值 1.0。训练在 8×A100 GPU 上进行，全局 batch size 为 8。

这种双阶段设计使模型既获得了 CoT 推理的结构化先验，又通过 RL 的奖励驱动优化实现了语义对齐与生成质量的进一步提升。消融实验证实，SFT 后引入 CoT 即可将 T2M 的 Top-1 R-Precision 从 0.384 提升至 0.460，而结合 GRPO 奖励后 FID 进一步降至 0.177（Table 3），验证了框架各阶段的独立贡献。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/001_Figure_1.jpg]]
*Figure 1: The UniMo is trained in two stages: the SFT stage and the reinforcement learning stage with GRPO. In the SFT stage, the model is teached to perform both T2M and M2T tasks with structured reasoning, i.e. CoT. In the RL stage, the model is further optimized with task-specific rewards, enabling unified and interpretable motion generation and understanding*



UniMo 的核心架构由四个关键模块构成，分别负责运动令牌化、思维链数据构建、统一序列生成与强化学习后训练。

### 运动令牌化：VQ-VAE

将连续运动序列 $\mathbf{m} \in \mathbb{R}^{T \times D}$ 离散化为运动令牌序列，是让 LLM 处理运动模态的前提。UniMo 采用冻结的 VQ-VAE，其训练损失为：

$$\mathcal{L}_{\mathrm{VQ}} = \mathcal{L}_{\mathrm{recon}} + \underbrace{\|\mathbf{z}_{1:T'} - \mathrm{sg}[\hat{\mathbf{z}}_{1:T'}]\|_2}_{\mathcal{L}_{\mathrm{embed}}} + \underbrace{\|\mathrm{sg}[\mathbf{z}_{1:T'}] - \hat{\mathbf{z}}_{1:T'}\|_2}_{\mathcal{L}_{\mathrm{commit}}}$$

其中 $\mathbf{z}_{1:T'}$ 为编码器输出的连续潜在向量，$\hat{\mathbf{z}}_{1:T'}$ 为通过最近邻查找 $\arg\min_{\mathbf{c}_k \in \mathcal{C}} \|\mathbf{z}_t - \mathbf{c}_k\|_2$ 从码本 $\mathcal{C}$ 中获得的量化向量，$\mathrm{sg}[\cdot]$ 为停止梯度算子。三项损失分别对应重建保真度、码本嵌入对齐和编码器承诺约束。训练完成后，该模块被冻结，不再参与后续梯度更新。

### CoT 数据构建

这是弥合文本-运动语义鸿沟的关键环节。流程如下：首先将 HumanML3D 中的运动序列通过 Blender 渲染为视频片段，然后将视频与原始文本描述配对，输入 Qwen2.5-VL-72B，生成具有结构化推理步骤的运动一致 CoT 注解。该过程将模糊的文本指令扩展为包含动作分解、时序顺序和空间关系的推理链，为后续 SFT 提供了更丰富的监督信号。

### LLM 骨干与统一序列生成

UniMo 以 Qwen2.5-3B-Instruct 为骨干，扩展其词汇表以容纳运动令牌。在 SFT 阶段，模型被训练为按特定模板执行双任务：对于 T2M，先输出 CoT 推理链，再基于输入文本和 CoT 生成运动令牌；对于 M2T，同样先输出 CoT，再生成文本描述。这种“先推理、后生成”的范式将单步预测转化为结构化推理过程，有效缓解了逐令牌预测的累积误差。

### GRPO 强化学习后训练

SFT 冷启动后，UniMo 采用 GRPO 进行策略优化。GRPO 的核心思想是对每个输入提示采样 $G$ 个完整输出，利用组内比较估计优势函数，避免了传统 PPO 需要单独价值网络的复杂性。其优化目标为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = E_c \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)} \hat{A}_i, \mathrm{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)}, 1-\varepsilon, 1+\varepsilon \right) \hat{A}_i \right) \right] - \beta \cdot D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}})$$

其中 $\hat{A}_i$ 为组内归一化的优势估计，$\varepsilon$ 控制裁剪范围，KL 散度正则项约束策略偏离参考模型的程度。

GRPO 阶段设计了三个任务特定奖励函数，均在**组级别**计算以优化多个运动令牌：

- **运动相似性奖励**：鼓励生成运动 $\hat{\mathbf{m}}$ 与真实运动 $\mathbf{m}$ 在动力学特征上的逼真度：

$$r_{\mathrm{motion}} = \frac{f_{\mathrm{motion}}(\hat{\mathbf{m}}) \cdot f_{\mathrm{motion}}(\mathbf{m})}{\|f_{\mathrm{motion}}(\hat{\mathbf{m}})\|_2 \cdot \|f_{\mathrm{motion}}(\mathbf{m})\|_2}$$

- **语义相似性奖励**：度量生成运动与输入文本 $T$ 在共享嵌入空间中的语义对齐程度：

$$r_{\mathrm{semantic}} = \frac{f_{\mathrm{motion}}(\hat{\mathbf{m}}) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{motion}}(\hat{\mathbf{m}})\|_2 \cdot \|f_{\mathrm{text}}(T)\|_2}$$

- **字幕相似性奖励**：针对 M2T 任务，用 CLIP 文本编码器计算生成字幕 $\hat{T}$ 与参考字幕 $T$ 的余弦相似度，并放大一倍以匹配 T2M 奖励的量级：

$$r_{\mathrm{caption}} = 2 \cdot \frac{f_{\mathrm{CLIP}}^{\mathrm{text}}(\hat{T}) \cdot f_{\mathrm{CLIP}}^{\mathrm{text}}(T)}{\|f_{\mathrm{CLIP}}^{\mathrm{text}}(\hat{T})\|_2 \cdot \|f_{\mathrm{CLIP}}^{\mathrm{text}}(T)\|_2}$$

这三个奖励函数共同作用，使生成与理解任务在 RL 阶段相互促进：运动相似性保证物理真实度，语义相似性强制文本-运动对齐，字幕相似性提升描述精度。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the CoT annotation process. Human joint sequences are rendered in the Blender and paired with captions, which are further processed by the Qwen2.5-VL-72B to generate reasoning traces*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/011_Figure_5.jpg]]
*Figure 5: Comparative word-clouds highlighting the most frequent textual cues in HumanML3D captions on the left and the corresponding CoT annotations on the right*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/012_Figure_6.jpg]]
*Figure 6: The t-SNE visualization of caption and CoT annotation embeddings. The CoT expands the language space, introducing greater diversity compared to original captions*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/013_Figure_7.jpg]]
*Figure 7: The CoT annotation prompt guides the Qwen2.5-VL-72B to generate action-centered, chronologically ordered reasoning for each motion video*



## 实验与关键发现

### 主实验结果

**文本到运动生成 (T2M)。** UniMo 在 HumanML3D 基准上取得了最优的语义对齐性能。如 Table 1 所示，UniMo 的 Top-1 R-Precision 达到 $0.539 \pm 0.003$，超越了此前最优的 **MoMask**（Guo et al., 2024）的 $0.521 \pm 0.002$，以及基于 LLM 的统一方法 **MotionLLM**（Wu et al., 2024a）的 $0.529 \pm 0.003$。Top-2 和 Top-3 R-Precision 同样取得最优。在多样性指标上，UniMo 达到 $10.042 \pm 0.076$，显著高于 MotionLLM 的 $9.908 \pm 0.102$，表明其生成的运动覆盖了更丰富的语义空间。

然而，在衡量生成运动与真实分布距离的 FID 指标上，UniMo 的 $0.177 \pm 0.004$ 明显落后于 MoMask 的 $0.045 \pm 0.002$。这揭示了一个关键的权衡：UniMo 在语义对齐和多样性上占优，但纯粹的重建保真度并非全面最优。该差距的根源在于 LLM 的 next-token 预测范式天然存在累积预测误差，而扩散/掩码模型在低层运动细节的逐帧重建上更具优势。

**运动到文本描述 (M2T)。** UniMo 在所有自动化指标上均取得最优结果。如 Table 2 所示，BLEU@1 达到 63.10，较此前最优的 MotionLLM（54.53）提升 8.57 分；CIDEr 达到 46.69，较 MotionLLM（33.74）提升 12.95 分。这一全面超越验证了 CoT 推理在运动理解中的关键作用——模型不仅“看到”运动，更通过结构化推理“理解”了动作序列的因果逻辑。

### 消融实验

**CoT 与 GRPO 奖励组件的作用。** Table 3 的消融实验揭示了各组件的贡献链条：

- **CoT 的独立贡献**：在仅使用 SFT 的条件下，引入 CoT 使 T2M 的 Top-1 R-Precision 从 0.384 跃升至 0.460，M2T 的 BLEU@1 从 58.43 提升至 63.10。这表明 CoT 推理本身就能显著弥合文本-运动语义鸿沟。
- **GRPO 奖励的叠加效应**：在 CoT 基础上依次叠加运动相似性奖励 $r_{\text{motion}}$、语义相似性奖励 $r_{\text{semantic}}$ 和字幕相似性奖励 $r_{\text{caption}}$，T2M 的 FID 从 0.460 逐步降至 0.177，M2T 的 CIDEr 从 36.61 提升至 46.69。三个奖励组件协同作用，分别从运动动力学保真度、文本-运动语义对齐和字幕质量三个维度约束模型。

**统一建模的协同效应。** Table 4 和 Table 5 分别考察了 T2M 和 M2T 任务在统一训练框架下的相互增益：

- 对于 T2M 任务，统一训练（T2M+M2T）相比单任务 T2M，在 SFT+RL 后 FID 从 0.203 降至 0.177，Top-1 R-Precision 从 0.529 提升至 0.539。
- 对于 M2T 任务，统一训练相比单任务 M2T，在 SFT+RL 后 CIDEr 从 42.13 提升至 46.69。

这一协同效应的因果机制在于：生成任务迫使模型学习从文本到运动的精确映射，理解任务迫使模型学习从运动到文本的语义抽取，两者共享的运动-语言表示空间在联合优化中相互校准。

### 失败模式与局限性

1. **FID 指标的固有劣势**：UniMo 在 FID 上无法超越 MoMask，这是 LLM-based 方法的结构性瓶颈。next-token 预测的误差累积在长序列运动令牌上尤为显著，而 GRPO 的组级别优化虽能缓解但无法根除这一问题。需要手动验证的是，FID 差距是否主要源于高频运动细节的丢失，还是整体运动分布的偏移。

2. **计算成本与可复现性**：训练需要 8×A100 GPU，CoT 标注依赖 Qwen2.5-VL-72B 和 Blender 渲染，引入的额外计算开销可能限制资源有限的研究者复现。CoT 质量受 VLM 能力约束，存在潜在的模型偏见传播风险。

3. **泛化性未验证**：所有实验仅在 HumanML3D 数据集上进行，该方法在 KIT、BABEL 等其他运动数据集上的性能尚不明确，需要进一步验证。

4. **VQ-VAE 冻结的限制**：运动令牌化器在后续训练中被冻结，可能限制了运动表示的进一步优化空间。若 VQ-VAE 的码本无法充分捕获某些细粒度动作，该误差会传播至整个流水线。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/007_Table_1.jpg]]
*Table 1: Quantitative results of the T2M task on the HumanML3D dataset. Each evaluation is repeated 20 times with average metrics and 95% confidence intervals. The best scores are highlighted in bold, and the second-best scores are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of the M2T task on the HumanML3D dataset. The best scores are highlighted in bold, and the second-best scores are underlined*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the effectiveness of CoT and different GRPO reward components on the HumanML3D dataset*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/009_Table_4.jpg]]
*Table 4: Ablation study of the synergy effect of unified modeling for the T2M task*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/010_Table_5.jpg]]
*Table 5: Ablation study of the synergy effect of unified modeling for the M2T task*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of our method with other open-source SOTAs such as MoMask (Guo et al. 2024) and MotionLLM (Wu et al. 2024a) for the text-to-motion task. Our method presents stronger instruction-following capability and can generate sequential actions. We highly recommend the readers to watch the video comparisons in supplementary materials*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2601_12126/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of our method with other open-source SOTAs such as MotionGPT (Jiang et al. 2023) and MotionLLM (Wu et al. 2024a) for the motion-to-text task. Our method can more precisely describe complex motions*



## 定位与知识库关联

### 1. 基线谱系与定位

UniMo 处于“统一运动生成与理解”这一新兴方向，其直接对话对象包括两类工作：**单任务运动生成模型**和**统一运动-语言模型**。

**单任务基线**方面，扩散模型家族以 **MDM**（Tevet et al., 2022）和 **MotionDiffuse**（Zhang et al., 2024a）为代表，在生成多样性上表现优异；掩码建模方法 **MoMask**（Guo et al., 2024）则在重建保真度（FID）上达到先前最优。UniMo 在语义对齐指标（R-Precision Top-1 0.539 vs MoMask 0.521）上超越了这些单任务专家，但在纯重建指标 FID 上仍存在差距（0.177 vs 0.045），说明基于 LLM 的自回归生成在运动细节保真度上尚未完全匹敌专用扩散或掩码模型。

**统一建模基线**方面，**MotionGPT**（Jiang et al., 2023）和 **MotionLLM**（Wu et al., 2024a）均采用 LLM 骨干将运动令牌化后与文本统一处理。UniMo 与两者的核心分水岭在于：前者直接进行 next-token 预测，而 UniMo 引入了**运动一致的思维链（CoT）推理**作为中间表征，并通过**组相对策略优化（GRPO）**进行后训练。在 M2T 任务上，这一差异体现为 CIDEr 从 MotionLLM 的 33.74 跃升至 46.69（Table 2），表明 CoT 结构化推理显著增强了模型对运动语义的细粒度理解能力。

**同期工作**方面，**Motion-R1**（Ouyang et al., 2025）也探索了 CoT 在运动生成中的应用，但 UniMo 的差异化在于：CoT 数据来源于 VLM 对渲染运动视频的视觉理解（而非纯文本推导），且 GRPO 在组级别对多个令牌同时优化，缓解了逐令牌预测的累积误差。

### 2. 适用边界与局限

UniMo 的适用边界受以下因素制约：

- **FID 瓶颈**：在 T2M 任务上 FID 为 0.177，远高于 MoMask 的 0.045。这意味着当应用场景对运动细节的逐帧重建精度要求极高时（如影视级动作合成），UniMo 可能不是最优选择。其优势在于语义对齐和指令遵循能力（Figure 3 定性展示），适合需要理解复杂文本指令并生成连贯动作序列的场景。

- **数据依赖**：CoT 注解依赖 Qwen2.5-VL-72B 对 Blender 渲染视频的理解。这一流程引入了两个潜在偏差源：VLM 本身的视觉理解偏见，以及 Blender 渲染与真实运动数据之间的域差异。若目标运动类型超出 VLM 的识别能力（如罕见运动或非人物体运动），CoT 质量将下降，进而影响模型性能。

- **计算成本**：训练需要 8×A100 GPU，SFT 阶段 20 个 epoch 加上 GRPO 阶段 14,000 步，资源需求较高。对于资源有限的研究者，复现和扩展存在门槛。

- **数据集泛化性**：所有实验仅在 HumanML3D 上完成。该数据集以单人日常动作为主，UniMo 在更复杂的数据集（如包含多人交互的 BABEL 或长序列的 KIT-ML）上的表现尚不明确。

- **VQ-VAE 冻结**：运动令牌化器在 SFT 和 RL 阶段均被冻结，虽然保证了训练稳定性，但也意味着运动表示无法随下游任务优化而自适应改进，可能限制了性能上限。

### 3. 开放问题

1. **FID 与语义指标的权衡**：如何在保持 CoT 带来的语义理解和多样性优势（Diversity 10.042）的同时，将 FID 降至接近专用生成模型的水平？可能的路径包括改进运动令牌化器、引入扩散解码头，或在 RL 阶段增加针对重建质量的奖励项。

2. **CoT 策略的可扩展性**：当前 CoT 生成依赖单一 VLM 和固定提示词模板（Figure 7）。更强大的 VLM 或更细粒度的运动渲染（如多视角、带骨骼标注）能否进一步提升 CoT 质量？CoT 范式能否扩展到运动预测、运动补全等其他运动理解任务？

3. **GRPO 超参敏感性**：奖励权重（运动相似性、语义相似性、字幕相似性）和组大小（G=8）对最终性能的影响未经过系统消融。是否存在更优的奖励组合或自适应权重策略，使 T2M 和 M2T 两个任务同时达到更优平衡？

4. **长序列与高帧率泛化**：HumanML3D 的运动序列长度和帧率有限。在更长时序（如数分钟动作）或更高帧率场景下，CoT 的结构化推理是否仍然有效，GRPO 的组优化是否会出现计算瓶颈？

5. **多模态扩展**：运动渲染为视频并利用 VLM 生成 CoT 的思路，能否迁移到其他模态（如音频驱动的动作生成、触觉反馈理解），形成更通用的跨模态推理框架？



## 原文 PDF

![[paperPDFs/arxiv_2026/UniMo:_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought.pdf]]

---
title: "HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HybridDriveVLA_Vision_Language_Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_for_Autonomous_Driving.pdf
project_link: null
code_link: null
aliases:
- HybridDriveVLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 视觉链式思维（V-CoT）与思维树评估（ToT-Evaluation）的统一集成。
primary_logic: 通过V-CoT生成未来视觉场景作为目标，再由ToT-Evaluation基于安全性、进度、舒适性三个层面生成并评分多条候选路径点序列，选取综合评分最高的路径作为最优轨迹，从而实现对视觉信息的充分利用与多层面决策评估。
claims:
- HybridDriveVLA集成视觉链式思维（V-CoT）推理和思维树评估（ToT-Evaluation）。
- V-CoT通过预测未来场景为ToT-Evaluation提供目标，ToT-Evaluation生成并基于安全、进度、舒适性对路径点评分。
- 移除V-CoT或跳过SFT阶段会导致碰撞率显著上升（0.23% vs 0.17%），表明V-CoT与SFT对于有效推理至关重要。
- 最终的HybridDriveVLA在nuScenes基准上实现了0.17%的平均碰撞率，优于传统VLA模型。
---

# HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving

> [!tip] 核心洞察
> 通过V-CoT生成未来视觉场景作为目标，再由ToT-Evaluation基于安全性、进度、舒适性三个层面生成并评分多条候选路径点序列，选取综合评分最高的路径作为最优轨迹，从而实现对视觉信息的充分利用与多层面决策评估。

| 字段 | 内容 |
|------|------|
| 中文题名 | HybridDriveVLA：用于自动驾驶的融合视觉链式思维推理与思维树评估的视觉-语言-动作模型 |
| 英文题名 | HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HybridDriveVLA |
| Dataset | nuScenes |

> [!tip] 效果简介
> - nuScenes (ST-P3) 上，Average Collision Rate (%) 0.17 vs 0.23 (HybridDriveVLA w/o V-CoT, ToT-Evaluation only) (-0.06 (26% relative improvement))；L2 Average (m) 0.26 vs N/A (N/A)。

## 概要

端到端自动驾驶系统近年来逐步引入视觉-语言-动作（VLA）模型，以利用大语言模型的推理能力进行规划。然而，现有VLA方案普遍依赖**文本链式思维（Text-CoT）**，将连续的视觉信息转换为离散符号，导致空间信息丢失；同时，这些方法仅预测单一序列路径点，缺乏针对不同驾驶层面的显式评估与抉择。这构成了当前VLA自动驾驶的核心瓶颈。

针对上述问题，本文提出 **HybridDriveVLA**，一个统一集成**视觉链式思维（V-CoT）推理**与**思维树评估（ToT-Evaluation）**的VLA模型。其核心洞察在于：通过V-CoT生成未来视觉场景作为目标，再由ToT-Evaluation基于安全性、进度、舒适性三个层面生成并评分多条候选路径点序列，选取综合评分最高的路径作为最优轨迹，从而实现对视觉信息的充分利用与多层面决策评估。

在nuScenes基准上，HybridDriveVLA实现了**0.17%的平均碰撞率**，相比仅使用ToT-Evaluation（无V-CoT）的变体（0.23%）相对提升26%，优于传统VLA模型。消融实验进一步表明，移除V-CoT或跳过监督微调（SFT）阶段均会导致碰撞率显著上升，验证了视觉预测作为目标以及基础视觉场景理解对于有效推理的关键作用。

自动驾驶的核心任务之一是轨迹规划——根据当前环境状态预测未来路径点序列。近年来，视觉-语言-动作（VLA）模型在自动驾驶中展现出潜力，它们将多模态感知与动作预测统一在一个框架内。然而，现有VLA方案存在两个结构性缺陷，限制了其在复杂场景下的安全决策能力。

**瓶颈一：文本链式思维导致空间信息丢失。** 以 **GPT-Driver**（Mao et al., 2023）和 **DriveVLM**（Tian et al., 2024）为代表的VLA模型，普遍采用文本链式思维（Text-CoT）进行推理——先将连续视觉信息转换为离散文本符号，再基于文本生成驾驶动作。这一“视觉→文本”的转换过程不可避免地丢失了空间细节与几何关系，使模型对环境的理解停留在语义层面，难以捕捉精确的物体位置、相对运动等对安全规划至关重要的信息。

**瓶颈二：单一序列预测缺乏显式评估与抉择。** 传统端到端规划方法（如 **Transfuser**，Chitta et al., 2022；**UniAD**，Hu et al., CVPR 2023）和现有VLA模型（如 **OpenDriveVLA**，Zhou et al., 2025）均直接预测单一路径点序列，缺乏对不同驾驶层面（安全性、行进效率、乘坐舒适性）的显式评估。当面临多车交互、复杂路况时，模型无法在多个候选轨迹间进行权衡与择优，只能“一条路走到黑”，缺乏人类驾驶中“多想一步、多比一条”的审慎决策能力。

**动机：从视觉推理到多层面评估。** 针对上述双重瓶颈，HybridDriveVLA提出两个核心创新：一是**视觉链式思维（V-CoT）**，直接在视觉域内自回归预测未来场景图像，以此作为规划目标，从根本上避免文本转换带来的空间信息损失；二是**思维树评估（ToT-Evaluation）**，基于安全性、进度、舒适性三个层面生成多条候选路径点序列并分别评分，选取综合评分最高的轨迹作为最优动作，实现对驾驶决策的显式多层面评估与择优。这一“视觉预测→多层面评估→择优输出”的推理管线，使模型能够像熟练驾驶员一样，在行动前先“想象”未来场景，再“权衡”不同选择的利弊。

## 核心方法与创新机理

HybridDriveVLA 的核心创新在于将**视觉链式思维（Visual Chain-of-Thought, V-CoT）推理**与**思维树评估（Tree-of-Thought Evaluation, ToT-Evaluation）**统一集成到一个端到端的视觉-语言-动作（VLA）框架中，从而系统性地解决了传统自动驾驶VLA模型的两大瓶颈：**推理过程中的空间信息丢失**和**路径规划中的单一决策盲区**。

### 瓶颈突破：从文本推理到视觉推理

传统VLA模型（如 **GPT-Driver** (Mao et al., 2023)、**DriveVLM** (Tian et al., 2024)）普遍采用文本链式思维（Text-CoT）进行推理——将连续的多视角图像转换为离散的文本描述，再基于文本生成驾驶动作。这一“图像→文本→动作”的信息传递链造成了严重的空间细节损失，因为文本天然无法完整保留三维场景的几何结构、物体间的精确距离关系和动态交互的连续性。

HybridDriveVLA 的 **V-CoT 模块**彻底改变了这一范式：它直接在视觉域内进行推理，以当前多视角图像 $I_t$、自车状态 $(l_t, c_t, o_t)$ 和导航指令为条件，自回归地预测未来场景图像 $\hat{I}_{t+6\alpha}$：

$$\hat{I}_{t+6\alpha} = M(I_t, E, l_t, c_t, o_t)$$

这一设计使模型“看到”即将发生的驾驶场景，而非仅仅“描述”它。预测的未来场景图像作为后续路径规划的**视觉目标**，完整保留了空间拓扑、障碍物分布和道路结构等关键信息，为决策提供了信息无损的感知基础。

### 决策范式升级：从单一预测到多层面评估择优

传统端到端规划方法（如 **Transfuser** (Chitta et al., 2022)、**UniAD** (Hu et al., CVPR 2023)）和现有VLA方法（如 **OpenDriveVLA** (Zhou et al., 2025)）通常直接输出单一序列的路径点，缺乏对不同驾驶层面的显式考量和多方案比较。

HybridDriveVLA 的 **ToT-Evaluation 模块**引入了思维树（Tree-of-Thought）启发的评估机制：以当前状态和V-CoT预测的未来场景 $\hat{I}_{t+6\alpha}$ 为条件，同时生成 $N$ 条候选路径点序列，并对每条序列在**三个独立层面**进行显式评分：

$$\{ (a_{t+k\alpha}^n, S_{t+k\alpha}^n) \}_{n=1}^N = M(I_t, \hat{I}_{t+6\alpha}, E, l_t, c_t, o_t)$$

其中评估层面集合 $E = \{e^{\text{safety}}, e^{\text{progress}}, e^{\text{comfort}}\}$ 分别对应：
- **安全性**：基于路径点到其他物体的最小距离归一化评分
- **进度性**：基于自车速度归一化评分
- **舒适性**：基于转向率归一化评分

每条候选路径点的综合评分 $T_{t+k\alpha}^n$ 为三个层面评分之和，最终选择综合评分最高的路径点序列作为最优动作：

$$n^* = \arg\max_{n \in \{1,\dots,N\}} T_{t+k\alpha}^n$$

这一机制将传统VLA的“预测-执行”模式升级为“预测-生成-评估-选择”的审慎决策模式，使模型能够像人类驾驶员一样在多个可行方案中权衡利弊。

### 创新协同：V-CoT与ToT-Evaluation的因果耦合

V-CoT与ToT-Evaluation并非两个独立模块的简单拼接，而是形成了**因果耦合的协同关系**：V-CoT生成的未来场景图像为ToT-Evaluation提供了具象化的规划目标，使多层面评估能够基于“预见”的场景进行；ToT-Evaluation则通过对多条路径的显式评分和择优，将视觉预测转化为可执行的、经过安全性和舒适性验证的驾驶动作。

消融实验有力地验证了这一协同设计的必要性：
- **移除V-CoT**（仅保留ToT-Evaluation）导致平均碰撞率从 0.17% 显著上升至 0.23%，相对恶化 26%，表明缺乏视觉目标引导的评估机制难以做出安全决策；
- **跳过SFT训练阶段**（v-ToT变体）同样导致碰撞率升至 0.23%，说明基础视觉场景理解能力是有效推理的前提。

### 方法定位

HybridDriveVLA 在方法谱系中处于**视觉世界模型与审慎规划的交汇点**：它既不同于直接预测动作的端到端方法，也不同于仅生成文本解释的VLA方案，而是通过“视觉预测+多层面评估”的混合推理机制，实现了对视觉信息的充分利用与驾驶安全性的显式保障。

HybridDriveVLA 的整体推理流程遵循“视觉感知 → 视觉链式思维预测（V‑CoT）→ 思维树评估（ToT‑Evaluation）→ 动作输出”的级联范式，将未来场景的视觉生成与多层面轨迹评估统一在一个自回归的多模态模型中。

### 输入与编码

系统在时刻 $t$ 接收三类输入：

1. **多视角图像** $I_t = \{ i_t^1, i_t^2, \ldots, i_t^h \}$，由视觉编码器（Vision Encoder）抽取为连续视觉特征；
2. **文本指令与状态**，包括导航命令 $c_t$、自车状态 $o_t$、高层指令 $l_t$，以及评估层面集合 $E = \{ e^{\mathrm{safety}}, e^{\mathrm{progress}}, e^{\mathrm{comfort}} \}$，经文本分词器（Text Tokenizer）转换为离散 token；
3. **当前场景的离散视觉 token**，由 MoVQGAN 编码器将图像压缩为离散码本索引，供后续自回归生成使用。

以上多模态 token 被拼接后送入骨干 VLA 模型——基于 **Qwen2‑VL‑2B**（Section 4.1）——进行统一的自回归推理。

### 视觉链式思维（V‑CoT）

V‑CoT 模块位于感知与规划之间，其核心作用是**在规划之前预测未来的视觉场景**，从而为下游评估提供具象的空间目标。形式上，骨干模型 $M$ 以当前多模态上下文为条件，自回归生成未来时刻 $t+6\alpha$ 的场景图像 $\hat{I}_{t+6\alpha}$：

$$
\hat{I}_{t+6\alpha} = M(I_t, E, l_t, c_t, o_t) \tag{1}
$$

生成过程通过最小化真实视觉 token $q_d$ 的负对数似然进行训练：

$$
\mathcal{L}_{V\text{-}\mathrm{CoT}} = -\sum_{d=1}^{\sigma} \log P_{\theta}(q_d \mid q_{<\sigma}, I_t, E, l_t, c_t, o_t) \tag{2}
$$

这一设计使模型在连续视觉空间内完成推理，避免了传统 Text‑CoT 中将图像转换为离散文本所带来的空间信息损失（Section 2.1）。

### 思维树评估（ToT‑Evaluation）

ToT‑Evaluation 以当前状态 $I_t$ 和 V‑CoT 预测的未来场景 $\hat{I}_{t+6\alpha}$ 共同作为条件，生成 $N$ 条候选路径点序列，并显式地为每条序列在安全性、进度、舒适性三个层面打分：

$$
\{ (a_{t+k\alpha}^n, S_{t+k\alpha}^n) \}_{n=1}^{N} = M(I_t, \hat{I}_{t+6\alpha}, E, l_t, c_t, o_t) \tag{3}
$$

每条路径点的综合评分 $T_{t+k\alpha}^n$ 为三个层面评分的加和：

$$
T_{t+k\alpha}^n = \sum_{j} s_{t+k\alpha}^{n,j} \tag{4}
$$

最终，模型选择综合评分最高的路径点索引 $n^*$ 作为最优动作输出：

$$
n^* = \arg\max_{n \in \{1,\dots,N\}} T_{t+k\alpha}^n \tag{5}
$$

该模块的训练损失 $\mathcal{L}_{\mathrm{ToT\text{-}Eval}}$ 最大化生成真实路径点及其层面评分的对数概率（式 6），从而让模型学会在多个驾驶维度上权衡决策。

### 训练管线与总目标

HybridDriveVLA 的训练分为两个阶段：

1. **监督微调（SFT）**：在视觉预测与路径评估数据上建立基础的多模态理解能力；
2. **指令微调（Instruction Tuning）**：进一步强化模型的可解释性、推理灵活性以及 ToT‑Evaluation 的跨时间一致性（Section 3.5）。

总训练目标为 V‑CoT 损失与 ToT‑Eval 损失的联合优化：

$$
\mathcal{L}_{\mathrm{HybridDriveVLA}} = \mathcal{L}_{V\text{-}\mathrm{CoT}} + \mathcal{L}_{\mathrm{ToT\text{-}Eval}} \tag{7}
$$

消融实验证实，跳过 SFT 阶段或移除 V‑CoT 模块均会导致碰撞率从 0.17% 显著上升至 0.23%（Section 4.2），表明视觉预测与分阶段训练对于有效推理的不可或缺性。

### 输出与解码

推理时，HybridDriveVLA 同时输出两类结果：MoVQGAN 解码器将生成的离散视觉 token 还原为未来场景图像（提供可解释的视觉目标），文本解分词器（Text Detokenizer）则将选出的路径点序列转换为可执行的动作轨迹。图 3 给出了完整的架构交互示意，展示了视觉编码器、语言模型、MoVQGAN 编解码器之间的数据流关系。

![[assets/figures/papers/paper_list_l2215_https_openaccess_thecvf_com_content_CVPR2026_html_Bassole_HybridDriveVLA/figures/001_Figure_1.jpg]]
*Figure 1: HybridDriveVLA is a vision–language–action model for autonomous driving that integrates visual anticipation and deliberative evaluation for selecting actions. During inference, it takes multi-view images, ego vehicle states, and instructions as input, then processes them using a vision encoder and text tokenizer. A Chain-of-Thought reasoning mechanism anticipates driving scene elements, while Treeof-Thought evaluates candidate waypoints based on safety, progress, and comfort to select the optimal trajectory*

![[assets/figures/papers/paper_list_l2215_https_openaccess_thecvf_com_content_CVPR2026_html_Bassole_HybridDriveVLA/figures/002_Figure_2.jpg]]
*Figure 2: Evolution from traditional VLA to our proposed Hybrid-DriveVLA. (a) Direct action prediction. (b) CoT-based reasoning for textual explanations. (c) HybridDriveVLA as an autonomous driving world-model combining V-CoT for visual next scene anticipation/generation and ToT-Evaluation for evaluative trajectory planning on each specific aspect*

HybridDriveVLA 的核心推理管线由两个紧密耦合的模块构成：**视觉链式思维（Visual Chain-of-Thought, V-CoT）** 与 **思维树评估（Tree-of-Thought Evaluation, ToT-Evaluation）**。V-CoT 负责生成未来视觉场景作为目标，ToT-Evaluation 则基于该目标进行多层面路径评估与择优。

---

### 视觉链式思维（V-CoT）

V-CoT 模块的核心功能是在路径规划之前，自回归地预测未来场景图像。给定当前时刻的多视角图像集合 $I_t$、评估层面集合 $E$、自车状态 $l_t$、导航命令 $c_t$ 及其他观测 $o_t$，骨干 VLA 模型 $M$ 预测未来时刻 $t+6\alpha$ 的场景图像：

$$\hat{I}_{t+6\alpha} = M(I_t, E, l_t, c_t, o_t) \tag{1}$$

预测的未来场景 $\hat{I}_{t+6\alpha}$ 随后作为 ToT-Evaluation 的视觉目标，为路径评估提供空间参照。

V-CoT 的训练目标是最小化真实未来场景视觉 token 的负对数似然。设真实场景被量化为 $\sigma$ 个离散视觉 token $q_1, \dots, q_\sigma$，训练损失为：

$$\mathcal{L}_{V\text{-CoT}} = -\sum_{d=1}^{\sigma} \log P_{\theta}(q_d \mid q_{<\sigma}, I_t, E, l_t, c_t, o_t) \tag{2}$$

该损失迫使模型在给定上下文条件下准确还原未来场景的视觉 token 序列，从而建立从当前观测到未来视觉状态的预测能力。

---

### 思维树评估（ToT-Evaluation）

ToT-Evaluation 模块以当前状态和 V-CoT 预测的未来场景 $\hat{I}_{t+6\alpha}$ 为条件，生成 $N$ 条候选路径点序列，并为每条序列在安全性、进度、舒适性三个层面分别评分：

$$\{ (a_{t+k\alpha}^n, S_{t+k\alpha}^n) \}_{n=1}^N = M(I_t, \hat{I}_{t+6\alpha}, E, l_t, c_t, o_t) \tag{3}$$

其中 $a_{t+k\alpha}^n$ 表示第 $n$ 条候选序列在时刻 $t+k\alpha$ 的路径点，$S_{t+k\alpha}^n = \{s_{t+k\alpha}^{n,\text{safety}}, s_{t+k\alpha}^{n,\text{progress}}, s_{t+k\alpha}^{n,\text{comfort}}\}$ 为对应的三维评分向量。

对每条候选路径点 $n$，其综合评分 $T_{t+k\alpha}^n$ 为三个层面评分之和：

$$T_{t+k\alpha}^n = \sum_{j \in \{\text{safety, progress, comfort}\}} s_{t+k\alpha}^{n,j} \tag{4}$$

最终，模型选择综合评分最高的路径点索引 $n^*$ 作为最优动作：

$$n^* = \arg\max_{n \in \{1,\dots,N\}} T_{t+k\alpha}^n \tag{5}$$

ToT-Evaluation 的训练损失最大化生成真实路径点及其层面评分的对数概率：

$$\mathcal{L}_{\text{ToT-Eval}} = -\sum_{n=1}^{N} \sum_{k=1}^{6} \sum_{j} \log P_{\theta}(a_{t+k\alpha}^n, s_{t+k\alpha}^{n,j} \mid I_t, \hat{I}_{t+6\alpha}, E, l_t, c_t, o_t) \tag{6}$$

---

### 联合训练目标

HybridDriveVLA 的总训练目标为 V-CoT 损失与 ToT-Evaluation 损失的联合优化：

$$\mathcal{L}_{\text{HybridDriveVLA}} = \mathcal{L}_{V\text{-CoT}} + \mathcal{L}_{\text{ToT-Eval}} \tag{7}$$

该联合损失确保模型同时学习视觉场景预测能力与多层面路径评估能力，二者相互增强：V-CoT 提供空间信息丰富的视觉目标，ToT-Evaluation 则利用该目标进行显式的多维度决策。

---

### 评分归一化公式

三个评估层面的评分均通过 sigmoid 函数 $\sigma(\cdot)$ 归一化至 $(0, 1)$ 区间。

**安全性评分**：基于路径点到其他物体的最小距离 $d_{t+k\alpha}$ 归一化，距离越大评分越高：

$$s_{t+k\alpha}^{\text{safety}} = \sigma\left(\frac{d_{t+k\alpha} - d^{\min}}{d^{\text{avg}} - d^{\min}}\right) \tag{8}$$

**舒适性评分**：基于转向率 $c_{t+k\alpha}$ 归一化，转向越平缓评分越高：

$$s_{t+k\alpha}^{\text{comfort}} = \sigma\left(1 - \frac{c_{t+k\alpha} - c^{\min}}{c^{\text{avg}} - c^{\min}}\right) \tag{9}$$

**进度评分**：基于自车速度 $v_{t+k\alpha}$ 归一化，速度越接近平均值评分越高：

$$s_{t+k\alpha}^{\text{progress}} = \sigma\left(\frac{v_{t+k\alpha} - v^{\min}}{v^{\text{avg}} - v^{\min}}\right) \tag{10}$$

上述归一化公式中，$d^{\min}$、$c^{\min}$、$v^{\min}$ 分别为对应指标的最小值，$d^{\text{avg}}$、$c^{\text{avg}}$、$v^{\text{avg}}$ 为平均值。该设计使得评分具有可比较的尺度，便于综合评分求和时各维度等权贡献。

![[assets/figures/papers/paper_list_l2215_https_openaccess_thecvf_com_content_CVPR2026_html_Bassole_HybridDriveVLA/figures/003_Figure_3.jpg]]
*Figure 3: HybridDriveVLA architecture integrates a Vision Encoder, Language Model, MoVQGAN encoder-decoder for multimodal reasoning. Inputs include multi-view images, ego states, navigational commands, instructions, and evaluation aspects (Safety, Progress, Comfort) processed in Text Detokenizer. HybridDriveVLA outputs next scene images using MoVQGAN Decoder and sequences of waypoints as actions using a Text Detokenizer*

## 实验与关键发现

### 主结果：nuScenes轨迹规划定量对比

HybridDriveVLA在nuScenes验证集上的轨迹规划性能通过ST-P3和UniAD两套指标进行评估，结果汇总于Table 1。完整版HybridDriveVLA（V-CoT + ToT-Evaluation）在ST-P3指标下取得了**0.26 m的L2平均误差**和**0.16%的平均碰撞率**，在UniAD指标下取得了**0.31 m的L2平均误差**和**0.19%的平均碰撞率**。这一碰撞率水平显著优于传统VLA基线模型，验证了视觉链式思维与思维树评估联合推理的有效性。

与仅使用ToT-Evaluation（无V-CoT）的变体相比，完整模型将ST-P3下的平均碰撞率从**0.23%降至0.17%**，相对提升达**26%**。这表明V-CoT生成的未来场景图像为ToT-Evaluation提供了关键的空间目标信息，单纯依赖评估机制而缺乏视觉预测会导致安全性能显著退化。

### 消融实验：V-CoT与SFT的必要性

消融实验揭示了两个关键训练组件对最终性能的因果贡献：

- **移除V-CoT**：仅保留ToT-Evaluation的模型碰撞率升至0.23%，证明视觉预测作为评估的“目标锚点”不可或缺。V-CoT将连续视觉空间中的未来状态直接作为条件输入，避免了文本化造成的空间信息损失。
- **跳过SFT阶段**：直接进行指令微调（v-ToT变体）同样导致碰撞率上升至0.23%。SFT阶段建立了基础的视觉场景理解能力，是后续ToT-Evaluation有效推理的前提——没有这一预训练基础，模型无法准确评估候选路径点的安全性和舒适性。

### 多层面评估的验证

Table 2展示了在NAVSIM基准上，ToT-Evaluation分别侧重安全、进度、舒适性时的差异化表现：

- 侧重**安全性**时，模型取得最高的TTC评分（98.73），表明其对潜在碰撞风险最为敏感；
- 侧重**舒适性**时，模型取得最优的Comfort评分（97.72），表明其能有效平滑转向行为；
- 侧重**进度**时，模型在速度维持方面表现最佳。

这一结果验证了显式多层面评估机制的有效性：模型能够根据指定的评估侧重调整路径选择策略，而非仅输出单一隐式偏好的轨迹。三个层面的评分通过归一化公式（式8-10）将物理量映射到统一尺度，使跨层面比较和综合评分成为可能。

### 定性分析

Figure 4展示了HybridDriveVLA在nuScenes数据集上的定性结果。红色轨迹为模型预测的最优路径点序列，绿色为真值轨迹。在多车交互场景下，模型通过ToT-Evaluation生成多条候选路径并基于安全、进度、舒适性综合评分选择最优序列，能够有效避开潜在碰撞风险区域，同时保持合理的行驶进度。

### 实验设置简述

HybridDriveVLA基于**Qwen2-VL-2B**骨干模型构建，训练分为SFT和指令微调两个阶段。SFT阶段训练V-CoT的视觉场景预测能力，指令微调阶段进一步优化ToT-Evaluation的评估精度和推理一致性。评估在nuScenes验证集上进行，对比基线包括**Transfuser**（Chitta et al., 2022）、**UniAD**（Hu et al., CVPR 2023）、**GPT-Driver**（Mao et al., 2023）、**DriveVLM**（Tian et al., 2024）和**OpenDriveVLA**（Zhou et al., 2025）。

![[assets/figures/papers/paper_list_l2215_https_openaccess_thecvf_com_content_CVPR2026_html_Bassole_HybridDriveVLA/figures/004_Table_1.jpg]]
*Table 1: Trajectory planning on the nuScenes validation set*

![[assets/figures/papers/paper_list_l2215_https_openaccess_thecvf_com_content_CVPR2026_html_Bassole_HybridDriveVLA/figures/005_Table_2.jpg]]
*Table 2: Testing Results on the NAVSIM Benchmark*

![[assets/figures/papers/paper_list_l2215_https_openaccess_thecvf_com_content_CVPR2026_html_Bassole_HybridDriveVLA/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative analysis of HybridDriveVLA on the nuScenes dataset. The red trajectory is the predicted optimal sequence of waypoints, and the green is the ground truth*

## 定位与知识库关联

### 方法演进与基线对比

HybridDriveVLA 在 VLA（Vision-Language-Action）自动驾驶方法谱系中处于“视觉推理+多层面评估规划”这一新节点。传统端到端规划方法如 **Transfuser**（Chitta et al., 2022）和 **UniAD**（Hu et al., CVPR 2023）直接输出动作或轨迹，缺乏显式的推理与评估环节。VLA 路线中，**GPT-Driver**（Mao et al., 2023）与 **DriveVLM**（Tian et al., 2024）引入文本链式思维（Text-CoT）来生成自然语言解释，但其核心瓶颈在于将连续视觉信息转换为离散符号，造成空间细节丢失。**OpenDriveVLA**（Zhou et al., 2025）等大规模 VLA 模型延续了文本推理范式，同样受限于视觉信息压缩。

HybridDriveVLA 的关键突破在于将推理过程完全保留在视觉域内（Section 2.1），并引入两个耦合的创新模块：

1. **视觉链式思维（V-CoT）**：不再将视觉场景转译为文本，而是直接自回归预测未来场景图像 $\hat{I}_{t+6\alpha}$，为后续规划提供富含空间细节的视觉目标（式 1）。
2. **思维树评估（ToT-Evaluation）**：基于安全性、进度、舒适性三个显式层面，生成 $N$ 条候选路径点序列并逐条评分，选取综合评分最高的序列作为最优轨迹（式 3–5）。

这种“视觉预测→多层面评估→择优输出”的管线，与现有方法形成了清晰的因果差异：传统方法要么跳过推理直接预测（图 2a），要么在文本空间推理（图 2b），而 HybridDriveVLA 构建了一个“自动驾驶世界模型”（图 2c），将视觉预测与评估规划统一在同一个多模态框架内。

### 适用边界

HybridDriveVLA 的设计假设在以下条件下成立：
- **多视角图像输入**：模型依赖同步的多视角图像 $I_t = \{i_t^1, i_t^2, \ldots, i_t^h\}$，其适用性受限于配备多摄像头系统的自动驾驶平台。
- **结构化评估层面**：ToT-Evaluation 的评分函数基于预定义的安全性、进度、舒适性三个维度（式 8–10），这些维度的归一化依赖场景统计数据（$d^{\min}, d^{\mathrm{avg}}, c^{\min}, c^{\mathrm{avg}}, v^{\min}, v^{\mathrm{avg}}$），在分布外场景中评分质量可能下降。
- **两阶段训练依赖**：消融实验表明，跳过 SFT 阶段（v-ToT 变体）会导致碰撞率从 0.17% 升至 0.23%（Section 4.2），说明模型对 SFT 建立的基础视觉场景理解有较强依赖，零样本迁移能力有限。
- **计算开销**：V-CoT 需要额外生成未来场景图像，ToT-Evaluation 需要并行的 $N$ 条路径生成与评分，推理成本高于单路径预测的基线方法。论文未提供推理延迟的定量对比，该点需手动验证。

### 局限与开放问题

论文未在 verified_analysis 中明确列出局限性章节，但可从实验设计与方法边界中推断以下局限：

1. **碰撞率仍非零**：尽管 HybridDriveVLA 将平均碰撞率降至 0.17%（ST-P3 指标），优于 ToT-Evaluation-only 变体的 0.23%，但绝对风险依然存在。在长尾安全关键场景中的表现缺乏专项分析。
2. **评估层面固定**：安全性、进度、舒适性三个维度是预设且静态的，无法动态适应不同驾驶场景的优先级变化（如紧急避障时安全性应压倒进度）。Table 2 展示了不同侧重下的性能分布，但未探索层面权重的自适应机制。
3. **视觉预测质量未独立评估**：V-CoT 生成的未来场景图像质量（如与真实图像的 FID、LPIPS 等）未报告，仅通过下游碰撞率的间接改善（26% 相对提升）来验证其有效性。视觉预测的保真度与规划性能之间的因果关系需进一步解耦。
4. **基准覆盖范围**：实验主要在 nuScenes 验证集和 NAVSIM 基准上进行，缺乏在更复杂交互场景（如 Waymo Open Motion Dataset 的密集交通）或闭环仿真中的验证。
5. **与大规模 VLA 的对比缺失**：论文将 OpenDriveVLA 列为基线，但 Table 1 中未直接对比，无法判断 HybridDriveVLA 的视觉推理范式在更大规模模型上的相对优势。

### 知识库定位

HybridDriveVLA 为 VLA 自动驾驶领域贡献了以下可迁移的知识单元：

- **视觉域内推理范式**：证明了绕过文本瓶颈、直接在视觉空间进行链式推理的可行性，为多模态推理模型的架构设计提供了新方向。
- **多层面显式评估框架**：将“安全性-进度-舒适性”三维评分嵌入规划过程，提供了一种可解释、可调控的决策机制，可被其他规划方法复用。
- **V-CoT 与 ToT 的耦合机制**：视觉预测作为评估目标、评估结果反馈选择最优动作的闭环设计，为“预测-评估-决策”一体化架构提供了模板。

这些贡献在方法谱系中填补了“视觉推理+显式多层面评估”的空白，但其泛化到更大规模模型、更多样化场景的能力仍有待后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/HybridDriveVLA_Vision_Language_Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_for_Autonomous_Driving.pdf]]

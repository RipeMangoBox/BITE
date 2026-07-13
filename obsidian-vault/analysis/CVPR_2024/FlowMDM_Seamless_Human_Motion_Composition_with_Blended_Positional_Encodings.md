---
title: "FlowMDM: Seamless Human Motion Composition with Blended Positional Encodings"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodings.pdf
project_link: https://barquerogerman.github.io/FlowMDM/
code_link: null
aliases:
- FlowMDM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过调控扩散模型去噪过程中位置编码的类型（从绝对位置编码逐步切换到相对位置编码），来平衡运动子序列内部的全局一致性与子序列间的局部平滑性。
primary_logic: 扩散模型在早期去噪阶段重建全局低频结构，后期阶段恢复局部高频细节，这与绝对位置编码提供全局位置信息、相对位置编码提供局部平移不变性的特性高度吻合；因此可设计一种混合位置编码策略，在无额外过渡标注的情况下生成自然平滑的动作组合。
claims:
- 在Babel和HumanML3D数据集上，FlowMDM在子序列FID和过渡AUJ上均达到最优，显著优于现有扩散采样方法DoubleTake等。
- 混合位置编码（BPE）在推理时结合了绝对编码的高准确率和相对编码的高平滑性，消融实验证明BPE在R-prec和AUJ上均优于单一编码。
- 姿态中心交叉注意力（PCCAT）有效解决了训练时单一条件与推理时多条件不一致的问题，提升了过渡质量。
- 提出的峰值加加速度（PJ）和加加速度下面积（AUJ）指标能够检测现有指标无法捕捉的突变过渡，FlowMDM在这些指标上远优于基线。
---

# FlowMDM: Seamless Human Motion Composition with Blended Positional Encodings

> [!tip] 核心洞察
> 扩散模型在早期去噪阶段重建全局低频结构，后期阶段恢复局部高频细节，这与绝对位置编码提供全局位置信息、相对位置编码提供局部平移不变性的特性高度吻合；因此可设计一种混合位置编码策略，在无额外过渡标注的情况下生成自然平滑的动作组合。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlowMDM：基于混合位置编码的无缝人体动作合成 |
| 英文题名 | FlowMDM: Seamless Human Motion Composition with Blended Positional Encodings |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://barquerogerman.github.io/FlowMDM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FlowMDM |
| Dataset | Babel, HumanML3D |

> [!tip] 效果简介
> - Babel 上，FID (Subsequence) 0.99 vs 1.33 (DoubleTake) (-0.34)；AUJ (Transition) 0.13 vs 0.64 (DoubleTake) (-0.51)。
> - HumanML3D 上，FID (Subsequence) 0.29 vs 1.25 (MultiDiffusion) (-0.96)；AUJ (Transition) 0.51 vs 1.06 (MultiDiffusion) (-0.55)。

## 概要

**核心问题**：现有的人体运动生成方法在组合多个不同文本描述的动作时，面临一个根本性矛盾——全局运动语义一致性与局部过渡自然平滑性难以兼得。自回归方法（如 TEACH）依赖事后线性插值来缝合动作片段，破坏了运动动力学；扩散采样方法（如 DoubleTake、DiffCollage、MultiDiffusion）则通过对重叠区域反复去噪或后处理来细化过渡，导致效率低下且真实感不足。

**核心洞察**：扩散模型在去噪过程中天然存在频率分解特性——早期步骤重建全局低频结构，后期步骤恢复局部高频细节。这与位置编码的内在属性高度吻合：绝对位置编码（APE）提供全局位置信息，有利于保持子序列内部的语义一致性；相对位置编码（RPE）具有平移不变性，有利于子序列间的局部平滑过渡。因此，可以通过调控去噪过程中位置编码的类型，在无额外过渡标注的情况下实现自然平滑的动作组合。

**提出方法**：FlowMDM 是首个无需后处理或冗余去噪步骤即可生成无缝人体运动组合的扩散模型。其核心创新包括两项关键技术：
- **混合位置编码（BPE）**：在去噪早期使用绝对位置编码以保持全局一致性，后期切换为相对位置编码（RoPE）以促进局部平滑性，通过调度器控制切换时机。
- **姿态中心交叉注意力（PCCAT）**：将文本条件仅注入注意力机制的查询（Query），而键（Key）和值（Value）仅使用噪声姿态，有效解决了训练时单条件与推理时多条件之间的分布偏移问题。

**主要结果**：在 Babel 和 HumanML3D 两个基准数据集上，FlowMDM 在子序列生成质量（FID）和过渡平滑性（AUJ）两项指标上均达到最优。具体而言，在 Babel 上 FID 降至 0.99（DoubleTake 为 1.33），AUJ 降至 0.13（DoubleTake 为 0.64）；在 HumanML3D 上 FID 降至 0.29（MultiDiffusion 为 1.25），AUJ 降至 0.51（MultiDiffusion 为 1.06）。消融实验进一步验证了 BPE 与 PCCAT 的互补性：二者结合在准确率（R-prec）和平滑性（AUJ）上均优于单一编码方案。此外，所提出的峰值加加速度（PJ）和加加速度下面积（AUJ）指标能够有效检测现有指标无法捕捉的突变过渡伪影。

### 问题背景

人体动作生成（Human Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实、游戏开发和人机交互等领域具有广泛应用。近年来，基于扩散模型（Diffusion Models）的方法在这一任务上取得了显著进展，能够生成高质量、多样化的单段运动序列。

然而，实际应用往往需要生成由多个不同文本描述组合而成的**长时间连续运动**，例如“向前走→转身→坐下”。这一任务被称为**人体动作组合（Human Motion Composition, HMC）**，其核心挑战在于：不仅要保证每段子运动与其文本描述在语义上高度一致，还要确保子序列之间的过渡自然平滑、无突变。

### 现有方法缺口

现有的人体动作组合方法主要分为两类，各自存在明显局限：

**自回归方法**（如 TEACH）使用变分自编码器结合 Transformer 逐段生成运动，再利用线性插值来平滑过渡。这类方法需要连续的标注数据进行训练，且线性插值往往产生不自然的中间姿态，导致过渡区域出现抖动或物理不合理现象。

**扩散采样方法**（如 DoubleTake、DiffCollage、MultiDiffusion）通过修改采样过程来融合相邻运动片段。具体而言，这些方法在推理时对重叠区域进行多次去噪或后处理细化，试图在已有运动片段之间“缝合”出过渡。然而，这种做法存在两个根本性问题：

1. **效率低下**：过渡区域的帧需要经历冗余的去噪步骤，计算开销显著增加。
2. **全局一致性不足**：事后缝合的方式缺乏对全长序列整体语义结构的统一建模，容易导致子序列内部的运动风格不一致，或过渡区域的动作与两端子序列的语义产生冲突。

**核心瓶颈**可归纳为：现有方法无法在**单一生成过程中**同时保证子序列的全局语义一致性和过渡的局部自然平滑性，往往需要在两者之间做出妥协，或依赖低效的后处理手段。

### 本文动机

FlowMDM 的提出源于对扩散模型去噪过程内在特性的深入观察。如 Figure 2 所示，在扩散模型的去噪过程中，早期步骤的注意力分布呈现全局依赖模式（蓝色曲线），模型主要重建运动的低频全局结构；而后期步骤的注意力则呈现明显的局部行为（红色曲线），模型聚焦于恢复高频细节。这一发现暗示：**去噪的不同阶段天然对应着不同尺度的运动结构建模**。

基于此，本文提出一个核心假设：可以利用**位置编码**作为调控杠杆，在去噪过程中动态平衡全局一致性与局部平滑性。具体而言：

- **绝对位置编码（APE）** 为每帧提供唯一的全局位置信息，有助于模型在早期去噪阶段建立子序列内部的整体结构一致性。
- **相对位置编码（RPE）** 具有平移不变性，仅关注帧间相对距离，有助于在后期去噪阶段生成与绝对位置无关的自然局部过渡。

通过将这两种编码方式在去噪时间轴上动态混合——早期使用 APE 保证语义对齐，后期切换到 RPE 实现平滑过渡——FlowMDM 首次实现了**无需任何后处理或冗余去噪步骤**的端到端无缝人体动作组合。这一设计使得全长序列可以一次性生成，每帧仅经历一次去噪，从根本上解决了现有方法的效率与质量矛盾。

## 核心方法与创新机理

FlowMDM 的核心创新在于洞察到扩散模型的去噪过程天然存在“先全局后局部”的频率重建特性，并据此设计了一套无需额外过渡标注、无需事后插值或冗余去噪的一体化动作组合方案。其关键创新点可归纳为三个相互协同的“changed slots”。

### 1. 混合位置编码（BPE）：从全局一致性到局部平滑性的优雅切换

**基线假设**：现有扩散模型（如 MDM）通常仅使用绝对位置编码（APE）或相对位置编码（RPE）中的一种。APE 提供全局位置信息，有利于保持子序列内部的语义一致性，但会阻碍子序列间的平滑过渡；RPE 具有平移不变性，天然适合生成平滑过渡，但缺乏全局结构约束。

**核心洞察**：作者通过可视化分析（Figure 2）发现，扩散模型在早期去噪步骤中，注意力呈现全局依赖模式（蓝色曲线）；随着去噪推进，注意力逐渐收缩为局部行为（红色曲线）。这与 APE 擅长全局结构、RPE 擅长局部平移不变性的特性高度吻合。

**创新机制**：BPE 在推理时动态切换位置编码类型——去噪早期使用 APE，确保各子序列内部语义结构正确；去噪后期切换为 RoPE（旋转位置编码），利用其仅依赖相对距离的特性（Eq. (1)），使相邻子序列的过渡区域自然平滑。切换由调度器控制，训练时则随机交替暴露两种编码，使模型学会适配两种模式。

$$q_m^T k_n = x_m^T W_q R_{n-m}^d W_k x_n$$

这一设计的因果调控变量（causal knob）在于**绝对编码的去噪步数占比**：增加 APE 步数可提高文本-运动匹配度（R-prec），但会牺牲过渡平滑性（FID、AUJ 上升）；最佳平衡点位于约 10% 的绝对编码步数处（Figure 5）。

### 2. 姿态中心交叉注意力（PCCAT）：解决训练-推理条件分布偏移

**基线问题**：在标准自注意力（SAT）或常规交叉注意力（CAT）中，条件信息（文本嵌入）与噪声姿态被拼接后同时输入查询和键。训练时每帧仅对应单一条件，但推理时多条件组合场景下，条件与姿态的分布关系发生偏移，导致过渡质量下降。

**创新机制**：PCCAT 将条件信息**仅注入查询（Query），键（Key）和值（Value）仅使用噪声姿态**。注意力分数计算变为：

$$q_m^T k_n = (W_q E_{x_m,c_m})^T (W_k E_{x_n})$$

这一设计最小化了控制信号与噪声运动之间的纠缠，使模型在推理时面对多条件切换时，仍能保持去噪行为的一致性。消融实验（Table 3, Table 4）证实，PCCAT 与 BPE 结合在 Babel 上取得最佳 FID（0.99）和多样性，同时保持低 AUJ；在 HumanML3D 上，该组合获得最佳 R-prec（0.685）和 FID（0.29）。

### 3. 一次性全长生成：消除冗余去噪与后处理

**基线瓶颈**：自回归方法（如 TEACH）需事后线性插值平滑过渡；扩散采样方法（如 DoubleTake、DiffCollage、MultiDiffusion）需重叠采样和过渡细化，导致部分帧被多次去噪，效率低下且引入伪影。

**创新机制**：FlowMDM 借助 BPE 和 PCCAT 的协同作用，在推理时一次性生成全长序列，每帧仅去噪一次，无需任何后处理或冗余去噪步骤。这一设计直接源于 BPE 对全局-局部频率的分阶段调控能力，以及 PCCAT 对多条件切换的鲁棒性。

### 创新协同逻辑

三项创新并非孤立存在，而是形成因果闭环：BPE 提供了从全局结构到局部平滑的频率调控手段，PCCAT 保证了多条件推理时的分布一致性，两者共同使“一次性全长生成”成为可能。这一闭环的突破口在于对扩散去噪过程频率特性的深刻理解——早期重建低频全局结构，后期恢复高频局部细节——并据此将位置编码从静态超参数升级为可动态调控的生成控制变量。

FlowMDM 的整体流程围绕一个核心设计展开：**利用扩散模型的迭代去噪特性，通过动态切换位置编码来一次性生成包含多个语义子序列的无缝运动长序列**。该流程无需任何后处理或冗余去噪步骤，每帧仅被去噪一次。

### 输入与输出

- **输入**：一组文本描述及其对应的时间区间 $\{ (c_i, [\tau_i, \tau_{i+1})) \}_{i=1}^{M}$，其中 $c_i$ 描述第 $i$ 个子序列的语义（如“向前走”），$[\tau_i, \tau_{i+1})$ 定义该子序列在全局时间轴上的起止帧范围。子序列定义为 $S_i = \{ x_{\tau_i}, ..., x_{\tau_{i+1}-1} \}$。
- **输出**：一个完整的运动序列 $\{ x_1, ..., x_N \}$，在语义上忠实地依次执行每个文本描述的动作，且子序列之间的过渡自然平滑。

### Pipeline 模块与数据流

整个生成过程由三个核心模块协同完成，其关系与数据流如下：

1. **双向扩散 Transformer（Bidirectional Diffusion Transformer）**  
   作为去噪网络的主干，采用基于 MDM 的双向编码器 Transformer 架构。它接收带噪运动序列和条件信息，通过自注意力机制同时建模过去帧与未来帧的依赖关系，为运动先验的学习提供基础能力。

2. **姿态中心交叉注意力（Pose-Centric Cross-Attention, PCCAT）**  
   负责将多个文本条件精确注入到对应帧的噪声姿态中。与将条件与姿态拼接后输入自注意力（SAT）或使用常规交叉注意力（CAT）不同，PCCAT 的核心操作是**将条件信息仅作为查询（Query）注入，而键（Key）和值（Value）仅使用噪声姿态**。其注意力分数计算为：
   $$q_m^T k_n = (W_q E_{x_m,c_m})^T (W_k E_{x_n}) = E_{x_m,c_m}^T W_q^T W_k E_{x_n}$$
   这一设计最小化了控制信号与噪声运动之间的纠缠，使得模型在推理时面对训练中未见过的多条件组合时，仍能为每一帧独立地去噪，从而解决了训练-推理条件分布偏移问题。

3. **混合位置编码（Blended Positional Encodings, BPE）**  
   在去噪过程中动态调控位置编码的类型，这是实现全局语义一致性与局部过渡平滑性之间平衡的关键机制：
   - **去噪早期**：使用**绝对位置编码（APE）**，即经典的正弦位置编码，注入全局位置信息，促使模型建立子序列内部的全局低频结构。
   - **去噪后期**：切换为**相对位置编码（RPE）**，具体采用旋转位置编码（RoPE），使注意力分数仅依赖于帧间相对距离 $n-m$：
     $$q_m^T k_n = x_m^T W_q R_{n-m}^d W_k x_n$$
     这种平移不变性使得模型聚焦于局部帧间关系，从而在子序列边界处生成平滑过渡。
   - **切换调度**：由一个调度器控制 APE 到 RPE 的过渡时机。训练时，模型随机交替暴露于两种编码，以学会在推理时响应编码切换。

### 推理流程总览

1. 从随机噪声初始化全长运动序列。
2. 进入扩散去噪循环。在每一步去噪中：
   - 根据当前去噪步数，由 BPE 调度器决定使用 APE 或 RPE。
   - PCCAT 将各子序列对应的文本条件注入对应帧的噪声姿态查询中。
   - 双向 Transformer 预测噪声，更新运动序列。
3. 去噪完成，输出最终的无缝运动序列。

这一流程的核心因果机制在于：扩散模型的早期去噪步骤天然地重建全局低频结构，而后期步骤恢复局部高频细节——这与 APE 提供全局位置信息、RPE 提供局部平移不变性的特性高度吻合。BPE 正是通过将这两种编码与去噪阶段对齐，实现了在无任何过渡标注训练的情况下，同时保证子序列的语义准确性和过渡的自然平滑性。

### 补充图表

FlowMDM 的核心由三个关键模块构成：**混合位置编码（BPE）**、**姿态中心交叉注意力（PCCAT）** 和 **双向扩散 Transformer**。这三个模块协同工作，使得模型能够在一次去噪过程中生成全长无缝动作序列，无需任何后处理或冗余去噪步骤。

### 混合位置编码（BPE）

BPE 是 FlowMDM 的核心创新，其设计动机源于对扩散模型去噪过程的观察：在早期去噪步骤中，模型注意力呈现全局依赖模式，负责重建运动的低频结构；而在后期步骤中，注意力逐渐收敛为局部行为，专注于恢复高频细节（见 Figure 2）。这一特性与位置编码的性质高度吻合——绝对位置编码（APE）提供全局位置信息，有利于保持子序列内部的一致性；相对位置编码（RPE）则具有平移不变性，有利于子序列间的平滑过渡。

![[assets/figures/papers/paper_list_l1842_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodi/figures/002_Figure_2.jpg]]
*Figure 2: Attention scores of a single query pose (current frame) as a function of the pose attended to (x-axis) in a diffusion-based motion generation model with a sinusoidal absolute positional encoding. Curves show the scores at each denoising step. We observe that, whereas early steps show strong global dependencies (blue), later denoising stages exhibit a clearly local behavior (red)*

BPE 在推理时通过一个调度器动态切换编码方式：**早期去噪步骤使用 APE，后期切换为 RPE**。具体而言，FlowMDM 采用正弦绝对位置编码（经典 sinusoidal encoding），将其加到注意力层的 query、key 和 value 上；相对位置编码则采用旋转位置编码（RoPE），其核心性质是使注意力分数仅取决于 query 和 key 之间的相对距离：

$$q_m^T k_n = (R_m^d W_q x_m)^T (R_n^d W_k x_n) = x_m^T W_q R_{n-m}^d W_k x_n \quad \text{(Eq. 1)}$$

其中 $R_m^d$ 和 $R_n^d$ 是旋转矩阵，$W_q$、$W_k$ 为投影矩阵。该公式表明，经过 RoPE 编码后，注意力分数 $q_m^T k_n$ 仅依赖于相对位置 $n-m$，从而天然支持子序列间的平移不变性。对于 RPE 模式，注意力范围限制在注意力窗口 $H < L < N$ 内，进一步强化局部建模能力。

在训练阶段，模型通过随机交替暴露于 APE 和 RPE 来学习两种编码模式，确保推理时切换编码方式不会引起分布偏移。

### 姿态中心交叉注意力（PCCAT）

PCCAT 旨在解决训练与推理之间的条件注入不一致问题。在标准交叉注意力（CAT）中，条件和噪声姿态同时作为 key 和 value，导致控制信号与运动信息过度纠缠。当推理时存在多个不同条件（即多个文本描述对应不同子序列）时，这种纠缠会引发分布偏移，损害过渡质量。

PCCAT 的核心设计原则是**最小化控制信号与噪声运动之间的纠缠**：将条件信息（如文本嵌入）仅注入 query，而 key 和 value 仅使用噪声姿态。其注意力分数计算为：

$$q_m^T k_n = (W_q E_{x_m,c_m})^T (W_k E_{x_n}) = E_{x_m,c_m}^T W_q^T W_k E_{x_n} \quad \text{(Eq. 3)}$$

其中 $E_{x_m,c_m}$ 是姿态 $x_m$ 与其对应条件 $c_m$ 的联合嵌入（仅用于 query），$E_{x_n}$ 是纯姿态嵌入（用于 key）。对比标准 CAT 的注意力分数 $E_{x_m,c_m}^T W_q^T W_k E_{x_n,c_n}$（key 中也包含条件），PCCAT 使每个帧的去噪仅依赖其自身条件，避免了不同子序列条件之间的相互干扰。Figure 3 展示了这一架构设计。

### 加加速度指标（PJ 和 AUJ）

为定量评估过渡平滑性，FlowMDM 引入了两个基于加加速度（jerk，即加速度的导数）的指标。加加速度能够捕捉现有指标（如 FID）无法检测的运动突变：

$$\mathbf{PJ} = \max_{1 \leq i \leq K} |j_i(\tau)|_1, \quad \mathrm{AUJ} = \sum_{\tau=1}^{L_{tr}} \max_{1 \leq i \leq K} |j_i(\tau) - j_{avg}|_1 \quad \text{(Eq. 4)}$$

其中 $j_i(\tau)$ 是关节 $i$ 在时刻 $\tau$ 的加加速度，$K$ 为关节总数，$L_{tr}$ 为过渡长度，$j_{avg}$ 是数据集中各关节最大加加速度的平均值。**PJ** 衡量整个过渡中任意关节的最大加加速度峰值，**AUJ** 衡量加加速度偏离数据集平均水平的累积程度。这两个指标互补：PJ 捕获瞬时突变，AUJ 反映持续的不自然波动。

## 实验与关键发现

### 瓶颈验证：全局一致性与局部平滑性的冲突

现有的人体运动组合方法面临一个根本性冲突：自回归方法（如 TEACH）依赖线性插值来平滑子序列间的过渡，但插值区域往往偏离真实运动分布，导致动作失真；扩散采样方法（如 DoubleTake、DiffCollage、MultiDiffusion）通过重叠采样和过渡细化来改善平滑性，但需要部分帧经历多次去噪步骤，不仅效率低下，还容易在过渡边界产生高频抖动伪影。FlowMDM 的设计目标正是通过一次性的全长序列生成，在不牺牲全局语义一致性的前提下，消除过渡区域的突变。

### 主实验结果

#### Babel 数据集（Table 1）

在 Babel 数据集上，FlowMDM 在子序列质量和过渡平滑性两个维度均达到最优。子序列 FID 降至 **0.99**，相比最优基线 DoubleTake 的 1.33 降低了 0.34，表明生成的动作片段具有更高的真实感。在过渡评估中，FlowMDM 的 AUJ 仅为 **0.13**，而 DoubleTake 为 0.64，MultiDiffusion 为 2.13，差距超过 4 倍，直观体现了混合位置编码（BPE）在消除过渡突变方面的显著优势。同时，R-precision 达到 0.604，MM-Dist 为 4.04，均处于竞争水平，说明文本-运动匹配度未因平滑性提升而受损。

#### HumanML3D 数据集（Table 2）

![[assets/figures/papers/paper_list_l1842_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodi/figures/006_Table_2.jpg]]
*Table 2: Comparison of FlowMDM with the state of the art in HumanML3D*

在更大规模的 HumanML3D 数据集上，FlowMDM 的优势进一步扩大。子序列 FID 为 **0.29**，相比 MultiDiffusion 的 1.25 降低了 0.96，几乎达到了单段无条件生成的精度水平。过渡 AUJ 为 **0.51**，约为 MultiDiffusion（1.06）的一半。值得注意的是，FlowMDM 在多样性指标（Diversity）上与 TEACH 等自回归方法相当，但无需任何过渡标注数据进行训练，验证了 BPE 策略的泛化能力。

#### 过渡平滑性可视化（Figure 4）

![[assets/figures/papers/paper_list_l1842_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodi/figures/005_Figure_4.jpg]]
*Figure 4: Transitions smoothness. Average maximum jerk over joints at each frame of the transitions for both motion composition (left) and extrapolation (right) tasks. While other methods show severe smoothness artifacts in the beginning and end of their transition refinement processes, FlowMDM’s jerk curve has the shortest peak for composition, and an absence of peaks for extrapolation*

Figure 4 展示了各方法在过渡区域的平均最大加加速度（per-frame average maximum jerk）曲线。在动作组合任务（左）和外推任务（右）中，DoubleTake 和 MultiDiffusion 在过渡起始和结束帧均出现明显的加加速度尖峰，表明存在不自然的运动突变。相比之下，FlowMDM 的加加速度曲线在整个过渡区间内保持平坦且接近零值，说明 BPE 在后期去噪阶段引入的相对位置编码有效地抑制了高频抖动，生成了物理上更合理的平滑过渡。

### 消融实验

#### 条件注入方案与位置编码的协同效应（Table 3, Table 4）

![[assets/figures/papers/paper_list_l1842_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodi/figures/007_Table_3.jpg]]
*Table 3: Ablation study in Babel. Cond. indicates the conditioning scheme, Train./Inf. PE specify the positional encodings (PE) used at training/inference time, and A, R, and B refer to absolute, relative, and blended PE, respectively. ↑, ↓, and → indicate that higher, lower, or values closer to the ground truth (GT) are better, respectively. Evaluation is run 10 times and ± specifies the 95% confidence intervals*

![[assets/figures/papers/paper_list_l1842_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodi/figures/008_Table_4.jpg]]
*Table 4: Ablation study in HumanML3D*

消融实验系统评估了条件注入方案（SAT vs. CAT vs. PCCAT）和训练/推理位置编码（APE vs. RPE vs. BPE）的组合效果。

在 Babel 数据集上（Table 3），**PCCAT + BPE 训练 + BPE 推理**的组合取得了最佳 FID（0.99）和多样性（10.64），同时 AUJ 保持在 0.13 的低水平。关键发现：
- 当使用 PCCAT 训练但推理时仅用 RPE（即放弃绝对编码阶段），AUJ 可进一步降至 0.11，但 R-precision 从 0.604 降至 0.564，证实了绝对编码阶段对维持全局语义一致性的必要性。
- 相比之下，使用 SAT 或 CAT 条件注入时，无论推理阶段采用何种编码，AUJ 均显著升高（0.50–0.55），说明 PCCAT 是 BPE 发挥平滑性优势的前提条件。

在 HumanML3D 数据集上（Table 4），**PCCAT + BPE 训练 + BPE 推理**获得最佳 R-precision（0.685）和 FID（0.29），而**PCCAT + BPE 训练 + RPE 推理**获得最佳 AUJ（0.53）。两种推理策略的互补性直接验证了 BPE 的核心洞察：绝对编码阶段保障语义匹配，相对编码阶段保障过渡平滑。

#### 绝对编码步数的权衡（Figure 5）

Figure 5 展示了绝对编码去噪步数占比对各项指标的影响。随着绝对编码步数从 0% 增加到约 10%，R-precision 显著提升，表明早期全局位置信息对文本-运动对齐至关重要。然而，超过 10% 后，FID 和 AUJ 开始恶化，因为过长的绝对编码阶段抑制了后期相对编码的局部平滑能力。最佳平衡点位于约 **10% 的绝对编码去噪步数**处，此时 R-precision 和 FID 同时达到最优。

#### PCCAT 消除训练-推理分布偏移的机制

标准交叉注意力（CAT）在训练时每帧仅接收单一条件，但推理时多条件组合会导致条件分布偏移——不同子序列的条件信息通过键和值相互干扰。PCCAT 通过将条件信息仅注入查询向量，使键和值仅依赖噪声姿态（见 Eq. (3)），切断了条件信息在注意力计算中的横向传播路径。消融结果（Table 3, Table 4）表明，PCCAT 相比 CAT 在 AUJ 上降低了约 0.3–0.4，证实了这一设计的有效性。

### 失败模式与局限性

尽管 FlowMDM 在标准基准上表现优异，分析揭示了以下边界情况：

1. **复杂连续动作的语义丢失**：对于包含多个精细动作的复杂文本描述（如"先坐下，然后转身拿起杯子，再站起来走向门口"），FlowMDM 偶尔会遗漏中间的部分动作。这可能是因为绝对编码阶段尚未显式建模子序列间的高层语义依赖关系。

2. **空间位置不一致**：由于低频组件（如全局位置和朝向）在早期去噪阶段独立生成，不同子序列之间偶尔会出现轻微的空间偏移。例如，在 Babel-B 场景中，从坐姿过渡到站姿时，身体位置可能发生不自然的漂移。

3. **加加速度指标的局限性**：提出的 PJ 和 AUJ 指标虽然能有效检测突变过渡，但其依赖数据集平均加加速度作为参考基准，对于分布外动作（如极限运动）的平滑性评估可能不够准确。需要人工验证极端场景下的评估可靠性。

### 补充实验结果

#### 注意力视野的影响（Appendix Table D, E）

在 Babel 和 HumanML3D 上，增大注意力视野 H 可略微提升 R-precision，但 FID 和 AUJ 基本保持稳定，说明 FlowMDM 对注意力视野不敏感，具有较强的超参数鲁棒性。

#### 噪声调度策略（Appendix Figure A）

余弦噪声调度相比线性调度能更缓慢、均匀地破坏运动信号，使去噪过程中的低频到高频分解更加充分，从而更好地发挥 BPE 在不同阶段的互补优势。

#### 外推任务（Appendix Table A）

在外推任务中，FlowMDM 同样保持了最低的 AUJ，证明 BPE 策略不仅适用于多段动作组合，也能在周期性运动外推中保持平滑过渡。

### 补充图表

![[assets/figures/papers/paper_list_l1842_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodi/figures/012_Table.jpg]]
*Table: C. Scenario-wise comparison in HumanML3D*

## 定位与知识库关联

### 1. 方法谱系与基线关系

FlowMDM 处于**扩散模型驱动的人体动作生成**脉络中，其直接对标的方法可分为两类：基于自回归的动作组合方法与基于扩散采样的动作组合方法。

**自回归方法**以 TEACH 为代表，其核心思路是利用变分自编码器（VAE）将动作压缩到隐空间后，通过 Transformer 自回归地生成序列动作，并在子序列边界处使用线性插值来平滑过渡。这类方法面临两个结构性瓶颈：（1）线性插值仅能保证一阶连续，无法从根本上消除过渡处的加速度突变（即加加速度尖峰）；（2）自回归生成存在误差累积，长序列的全局语义一致性难以保证。

**扩散采样方法**包括 DoubleTake、DiffCollage 和 MultiDiffusion 三个代表性工作。DoubleTake 通过重叠采样和过渡细化来生成动作组合，但重叠区域的帧需要经历多次去噪，计算冗余且容易引入伪影。DiffCollage 修改采样过程以融合重叠区域的噪声，MultiDiffusion 则同时去噪叠加的动作片段并进行组合。这些方法的共同局限在于：它们将动作组合视为一个**后处理问题**，而非从生成过程本身解决过渡平滑性。FlowMDM 的突破在于将动作组合能力**内化到扩散模型的去噪过程中**，通过混合位置编码（BPE）在生成阶段同时控制全局一致性与局部平滑性，从而无需任何后处理或冗余去噪步骤。

### 2. 核心创新与知识贡献

FlowMDM 的知识贡献可归纳为三个层面：

**第一层：因果机制的发现与利用。** 论文通过可视化分析（Figure 2）揭示了一个关键现象：扩散模型在早期去噪步骤中，注意力呈现全局依赖模式（蓝色曲线），负责重建运动的低频结构；在后期步骤中，注意力收缩为局部行为（红色曲线），负责恢复高频细节。这一发现构成了 BPE 设计的因果基础——早期使用绝对位置编码（APE）提供全局位置信息以维持子序列内语义一致性，后期切换到旋转位置编码（RoPE，一种相对编码）利用其平移不变性来促进子序列间的自然过渡。

**第二层：条件注入机制的重新设计。** 姿态中心交叉注意力（PCCAT）解决了训练-推理的条件分布偏移问题。在标准交叉注意力（CAT）中，条件信息同时注入查询和键，导致训练时（单一条件）与推理时（多条件拼接）的条件分布不一致。PCCAT 将条件仅注入查询，键和值仅使用噪声姿态，从而消除了这一偏移。这一设计与 BPE 形成互补：PCCAT 负责帧级条件的准确注入，BPE 负责帧间关系的全局-局部平衡。

**第三层：评估指标体系的补充。** 现有指标（FID、R-Precision 等）无法有效捕捉过渡处的突变。FlowMDM 引入峰值加加速度（PJ）和加加速度下面积（AUJ）两个新指标，从瞬时峰值和累积偏差两个维度量化过渡平滑性，填补了评估体系的空白。

### 3. 适用边界与局限

FlowMDM 的适用边界受以下因素约束：

**复杂文本描述的覆盖度有限。** 当文本描述包含连续多个不同的精细动作时（例如“先走、再转身、然后蹲下捡东西、最后跳起来”），FlowMDM 可能仅完成部分动作。这一局限的根源在于 BPE 的绝对编码阶段尚未显式建模不同子序列之间的高层语义依赖关系。

**空间一致性的低频偏差。** 由于扩散模型在低频阶段独立生成各子序列的全局结构，偶尔会导致不同子序列间的空间位置轻微不匹配。论文在 Babel-B 场景中观察到这一现象：从“行走”过渡到“坐在长椅上”时，坐姿与站姿之间可能出现空间偏移。这是因为绝对编码阶段缺乏跨子序列的空间约束。

**对极端长序列的泛化能力未经验证。** 论文实验中的序列长度受限于 Babel 和 HumanML3D 数据集的典型时长，对于远超训练分布的超长序列组合，BPE 的全局-局部平衡策略是否仍然有效，尚待验证。

### 4. 开放问题与后续方向

从 FlowMDM 的局限出发，可识别以下开放问题：

1. **意图规划模块的引入。** 能否在绝对编码阶段引入一个轻量级的意图规划模块，显式建模子序列间的语义依赖（如动作的先后顺序、空间位置的衔接约束）？这将直接针对“复杂文本描述覆盖不足”和“空间一致性偏差”两个局限。

2. **运动先验的跨模态泛化。** BPE + PCCAT 构成的运动先验框架，其核心思想（早期全局/后期局部的编码切换 + 条件仅注入查询）是否可以推广到其他控制信号（如音乐节奏、场景几何约束）或其他扩散模型架构（如基于 UNet 的扩散模型）？这决定了该方法的生态影响力。

3. **空间一致性约束的增强。** 如何在不牺牲生成多样性的前提下，进一步减少低频独立生成带来的空间不一致问题？可能的路径包括在绝对编码阶段引入跨子序列的弱空间约束，或设计专门的空间对齐损失函数。

4. **评估体系的完善。** PJ 和 AUJ 虽然能检测现有指标无法捕捉的突变过渡，但它们依赖于数据集平均加加速度的统计，对于分布外动作的评估有效性仍需进一步验证。

> **注意：** 以上涉及的基线方法（TEACH、DoubleTake、DiffCollage、MultiDiffusion）的具体作者、会议和年份信息在提供的分析材料中未明确给出，建议手动查证后补充。

## 原文 PDF

![[paperPDFs/CVPR_2024/FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodings.pdf]]

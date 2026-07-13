---
title: MoST Motion Style Transformer between Diverse Action Contents
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/MoST_Motion_Style_Transformer_between_Diverse_Action_Contents.pdf
project_link: null
code_link: https://github.com/Boeun-Kim/MoST
aliases:
- MMSTBDAC
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Part-Attentive Style Modulator (PSM) 通过跨注意力机制将源风格特征与目标内容动态对齐，同时风格解耦损失（L_D）强制分离风格与内容，使风格迁移不再依赖内容一致性。
primary_logic: 通过基于身体部位的注意力调制（PSM）和风格解耦损失，模型能够在保持内容完整性的前提下，在不同动作类型间迁移风格，并直接生成包含全局平移的合理运动，从而消除后处理。
claims:
- PSM与L_D联合使用将CC从37.4降至8.5，SC++从69.5降至63.0，验证了风格调制的有效性。
- MoST在Xia数据集上实现了最低的内容一致性（CC）和风格一致性（SC++），尤其在内容不同的运动对上显著优于先前方法。
- PSM的跨注意力图显示其能识别激活的身体部位（如从Punch的手臂转移至Kick的腿部），并仅在相应部位迁移风格，避免内容污染。
- 消融实验表明，风格解耦损失L_D使CC从19.7降至9.3，并使风格特征空间得到良好分离（t-SNE可视化）。
---

# MoST Motion Style Transformer between Diverse Action Contents

> [!tip] 核心洞察
> 通过基于身体部位的注意力调制（PSM）和风格解耦损失，模型能够在保持内容完整性的前提下，在不同动作类型间迁移风格，并直接生成包含全局平移的合理运动，从而消除后处理。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoST：不同动作内容间的运动风格Transformer |
| 英文题名 | MoST Motion Style Transformer between Diverse Action Contents |
| 会议/期刊 | CVPR 2024 |
| Links | [Code](https://github.com/Boeun-Kim/MoST) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoST |
| Dataset | Xia dataset |

> [!tip] 效果简介
> - Xia dataset 上，CC (内容一致性，越低越好) 8.5 vs 37.4 (无PSM, 无L_D) (-28.9)；SC++ (风格一致性，越低越好) 63.0 vs 69.5 (无PSM, 无L_D) (-6.5)；CC (同等内容/不同内容设置) 8.0 / 8.7 vs N/A (Table 1数值省略，但显著优于其他方法) (N/A)。

## 概要

### 问题背景

运动风格迁移旨在将源运动（如“老年人行走”）的风格特征迁移到目标运动（如“正常行走”）上，同时保持目标运动的内容（动作类型）不变。现有方法（如 **Aberman et al., TOG 2020** 的 Temporal AdaIN 方法、**MotionPuzzle** (Jang et al., TOG 2022) 的身体部位风格组合方法）在内容相同的运动对之间表现尚可，但当内容不同时——例如将“出拳”的风格迁移到“踢腿”——会频繁失败。典型失败模式包括：复制源运动的内容而丢失目标内容、产生扭曲的运动形态（Figure 1）。其根本瓶颈在于：现有方法无法从内容中清晰地解耦风格，且依赖启发式后处理（如复制全局平移、强制脚部接触），这些后处理在跨内容场景下进一步引入不一致性。

### 核心方法

MoST 提出一种基于 Transformer 的框架，由三个关键模块构成（Figure 2）：

1. **Siamese Motion Encoder**：从单个运动中同时提取内容动态特征 $Y$ 和身体部位特异的风格特征 $S$，并通过 style token 聚合全局风格表示。
2. **Part-Attentive Style Modulator (PSM)**：核心创新模块。利用跨注意力机制，以目标内容特征作为查询，以源运动的内容特征作为键，动态调制源风格特征，实现身体部位级别的风格对齐——例如，自动识别“出拳”风格源自手臂部位，并将其迁移到“踢腿”的对应激活部位，而非污染无关部位。
3. **Motion Generator**：基于内容动态 $Y^C$ 和调制后的风格 $\tilde{S}^S$，通过注入 AdaIN 的 Transformer 解码器生成最终运动，同时直接生成全局平移，消除后处理需求。

训练中引入**风格解耦损失 $L_D$**，最小化相同风格但不同内容风格运动输入下的输出差异，强制风格与内容分离。此外，基于物理的正则化项 $R_{foot}$ 惩罚接地帧的脚部速度，间接促进合理接触。

### 核心结论

- **跨内容风格迁移能力**：MoST 在内容不同的运动对上显著优于先前方法，实现了最低的内容一致性误差（CC）和风格一致性误差（SC++），验证了其在不同动作类型间有效迁移风格的能力（Table 1）。
- **PSM 的关键作用**：消融实验表明，PSM 将 CC 从 37.4 降至 19.7；联合 $L_D$ 后进一步降至 8.5，SC++ 从 69.5 降至 63.0（Table 2）。跨注意力图可视化证实 PSM 能识别激活的身体部位并仅在相应部位迁移风格（Figure 7）。
- **风格解耦的有效性**：$L_D$ 使风格特征空间在 t-SNE 可视化中呈现良好的类别分离，证明其强制解耦的效果（Figure 5）。

### 方法定位

MoST 属于**基于 Transformer 的显式风格解耦与注意力调制**范式。与依赖隐式解耦或全局风格注入的先前方法不同，MoST 通过 PSM 的跨注意力机制实现了细粒度的身体部位级风格对齐，并通过 $L_D$ 提供显式解耦监督。这一设计使其在方法谱系中处于“结构化风格调制 + 显式解耦”的交汇点，为解决跨内容运动风格迁移提供了新路径。

### 主要局限

- 部分生成样本仍可能出现脚部滑动或漂浮，物理损失无法完全强制消除。
- 基于 Transformer 的架构需预设最大运动长度，限制了可变长度的灵活性。
- 仅在小型动捕数据集（Xia、BFA）上验证，未在更大规模或野外数据集上测试。
- 未探索少样本或零样本场景下的风格迁移能力。



### 运动风格迁移的核心挑战

运动风格迁移（Motion Style Transfer）旨在将源运动的“风格”注入目标运动，同时保持目标运动的“内容”（即动作类别）不变。这一任务在角色动画、游戏开发和电影制作中具有重要应用价值。然而，现有方法面临一个根本性瓶颈：**它们无法在不同内容的运动之间有效迁移风格**。当风格运动与内容运动的动作类型不同时（例如，将“出拳”的风格迁移到“踢腿”上），先前方法往往产生严重扭曲或完全失败的结果。

这一瓶颈的成因可从两个层面理解：

1. **风格与内容的纠缠**：现有方法难以从运动内容中清晰地解耦风格。当风格运动的内容特征与目标运动的内容不一致时，风格特征中残留的内容信息会“污染”生成结果，导致目标运动的动作类型发生改变。Figure 1 直观展示了这一现象：(a) **MotionPuzzle**（Jang et al., TOG 2022）在风格迁移时直接复制了风格运动的内容；(b) **Aberman et al.**（TOG 2020）的方法则在内容不同的运动对上产生完全扭曲的运动。

2. **对后处理的依赖**：为弥补生成质量的不足，先前方法普遍依赖启发式后处理步骤，例如从内容运动复制全局平移轨迹、强制脚部接触地面等。这些后处理不仅增加了流程的复杂性，还可能引入物理不一致性（如滑步或漂浮），且无法从根本上解决风格-内容解耦的问题。

### 现有方法的局限性

在 MoST 之前，运动风格迁移领域已涌现出多种技术路线，但均未系统性地解决跨内容风格迁移问题：

- **基于 AdaIN 的方法**（如 Aberman et al., TOG 2020）：通过自适应实例归一化将风格特征注入内容运动，但风格编码器仅提取全局风格特征，缺乏与目标内容的动态对齐能力。当内容不同时，风格注入缺乏针对性，容易导致内容破坏。
- **基于身体部位组合的方法**（如 MotionPuzzle, Jang et al., TOG 2022）：允许任意身体部位的风格组合，但在跨内容迁移时倾向于复制源运动内容，而非仅迁移风格。
- **基于多域生成模型的方法**（如 Park et al., PACMCGIT 2021）和**基于自回归流的方法**（如 Wen et al., CVPR 2021）：这些方法同样未显式建模风格与内容的解耦，在内容不同的运动对上表现不佳。

上述方法的共同缺陷可归纳为三个关键缺失：
- **缺失身体部位级的风格对齐**：风格迁移应仅在激活的身体部位上进行（例如，将“出拳”的手臂风格迁移到“踢腿”的腿部），而非全局均匀注入。
- **缺失显式的风格解耦监督**：网络缺乏明确的训练信号来强制分离风格与内容，导致隐式学习不可靠。
- **缺失端到端的全局运动生成**：全局平移和脚部接触等关键运动属性依赖后处理，而非模型直接输出。

### 本文动机与核心思路

针对上述瓶颈，MoST 的核心动机是：**构建一个能够从内容中彻底解耦风格，并在身体部位级别实现风格与内容动态对齐的框架，从而在保持内容完整性的前提下，在不同动作类型间实现高质量的风格迁移，并消除对后处理的依赖。**

为实现这一目标，MoST 引入了两个关键创新：

- **Part-Attentive Style Modulator (PSM)**：通过跨注意力机制，将源风格特征以目标内容为条件进行调制，使风格仅在相关身体部位上施加影响。这解决了“风格注入缺乏针对性”的问题。
- **风格解耦损失（$L_D$）**：最小化使用相同风格但不同内容风格运动时生成结果的差异，强制网络将风格与内容分离。这解决了“隐式解耦不可靠”的问题。

此外，MoST 在输入嵌入中引入全局平移和速度标记，通过注意力机制与身体部位特征交互，直接生成包含一致全局运动的输出，从而消除了对后处理全局平移的依赖；同时引入基于物理的脚部接触正则项（$R_{foot}$），间接促进合理的脚-地接触，减少滑步和漂浮现象。



## 核心方法与创新机理

MoST 的核心创新在于提出了一套**内容无关的风格迁移机制**，解决了现有方法在源动作与目标动作内容不同时风格迁移失败的根本瓶颈。其关键突破体现在三个紧密耦合的改进槽位上。

**1. 身体部位感知的风格调制器（Part-Attentive Style Modulator, PSM）**

这是 MoST 最关键的结构创新。现有方法（如 **Aberman et al., TOG 2020** 基于 Temporal AdaIN 的方案，或 **MotionPuzzle** (Jang et al., TOG 2022)）通常将源运动的全局风格特征直接注入目标运动，当内容不同时（如从“出拳”迁移风格至“踢腿”），风格信息会错误地注入不相关的身体部位，导致内容扭曲或风格复制（Figure 1）。

PSM 通过**跨注意力机制**从根本上改变了这一范式。它以目标运动的内容特征 $\bar{C}^C$ 作为查询（Query），以源运动的内容特征 $\bar{C}^S$ 作为键（Key），以源运动的风格特征 $\bar{S}^S$ 作为值（Value），动态计算风格应如何从源运动的特定身体部位传输至目标运动的对应部位：

$$\mathsf{crossMHA}(\bar{C}^C, \bar{C}^S, \bar{S}^S) = (\vert\vert_{i=1}^h H_i) W_H$$

其中 $H_i = \mathtt{Attn}(\mathtt{LN}(\bar{C}^C) W_i^Q, \mathtt{LN}(\bar{C}^S) W_i^K, \mathtt{LN}(\bar{S}^S) W_i^V)$。该机制使模型能够自动识别“激活”的身体部位——例如从 Punch 的手臂区域提取风格，并将其调制后注入 Kick 的腿部区域。跨注意力热力图（Figure 7）直接验证了这一能力：最高列指示风格来源部位，最高元素指示风格接收部位，展示了精确的身体部位级对齐。

消融实验（Table 2）提供了决定性证据：移除 PSM 后，内容一致性（CC）从 8.5 急剧恶化至 37.4，表明不相关的身体部位被风格信息严重污染。

**2. 风格解耦损失（Style Disentanglement Loss, $L_D$）**

现有方法缺乏显式的风格-内容解耦监督，网络倾向于将风格与内容纠缠学习。MoST 引入了风格解耦损失，强制模型对同一内容运动、不同风格运动（但风格标签相同）产生尽可能一致的输出：

$$L_D = \mathbb{E}_{M^C, M_a^S, M_b^S \sim \mathbb{M}} \mid\mid \operatorname{MoST}(M^C, M_a^S) - \operatorname{MoST}(M^C, M_b^S) \mid\mid_2$$

这一损失函数从优化目标层面切断了风格特征与内容动态的关联。消融实验（Table 2）表明，单独引入 $L_D$ 即可将 CC 从 19.7 降至 9.3，同时将风格一致性（SC++）从 69.5 降至 63.0。t-SNE 可视化（Figure 5）进一步显示，加入 $L_D$ 后调制风格特征空间按风格标签形成清晰分离的簇，而未加 $L_D$ 时不同风格的特征混杂在一起。

PSM 与 $L_D$ 的联合使用产生了协同效应：PSM 在空间上精确控制风格注入的位置，$L_D$ 在特征空间上强制风格与内容的全局分离，二者共同将 CC 降至 8.5、SC++ 降至 63.0，达到最优性能。

**3. 端到端全局运动生成**

现有方法（Aberman et al., MotionPuzzle）普遍采用**后处理**策略：从内容运动复制全局平移，或通过启发式规则修正脚部接触。当内容运动与风格运动差异较大时，这种复制会导致运动不自然甚至物理上不可能的结果。

MoST 将全局平移和速度作为独立标记嵌入到 Transformer 序列中，使其通过注意力机制与身体部位特征交互，从而**直接生成**与风格化局部姿态相协调的全局运动。同时，基于物理的正则化项 $R_{foot}$ 惩罚接地帧的脚部速度，间接促进合理的脚部接触，替代了显式的启发式后处理：

$$L_{phy} = \lambda_{vel} R_{vel} + \lambda_{acc} R_{acc} + \lambda_{foot} R_{foot}$$

这使得 MoST 能够输出“开箱即用”的完整运动，无需任何后处理步骤。

**需要手动验证的点**：Table 1 中与其他基线方法（Park et al., PACMCGIT 2021; Wen et al., CVPR 2021）的完整定量对比数值在提供的证据中缺失，仅确认 MoST 取得了最低的 CC 和 SC++。建议查阅原文获取精确数值以完善对比论述。



MoST的整体框架由三个核心模块构成：**Siamese运动编码器（E）**、**部位感知风格调制器（PSM）** 和**运动生成器（G）**，三者协同完成从任意内容运动到任意风格运动的迁移，无需任何启发式后处理。

### 输入输出流

给定一个内容运动 $M^C$ 和一个风格运动 $M^S$，框架的目标是生成一个保留 $M^C$ 内容动态、同时体现 $M^S$ 风格特征的新运动 $M^G$：

$$M^G = \mathsf{MoST}(M^C, M^S)$$

整个流程分为三个阶段：

**1. 特征提取阶段**  
Siamese运动编码器 $E$ 以共享权重的方式分别处理 $M^C$ 和 $M^S$，从每个运动中同时提取两类特征：
- **内容动态特征 $Y$**：捕捉运动的时空结构（如关节轨迹模式）
- **身体部位风格特征 $S$**：编码各身体部位的风格信息

$$\mathcal{E}(M^C) = \{S^C, Y^C\}, \quad \mathcal{E}(M^S) = \{S^S, Y^S\}$$

**2. 风格调制阶段**  
PSM接收三个输入——内容运动的内容特征 $C^C$（由 $Y^C$ 经实例归一化得到）、风格运动的内容特征 $C^S$（由 $Y^S$ 经实例归一化得到）以及风格运动的原始风格特征 $S^S$。通过跨注意力机制，PSM以 $C^C$ 为查询、以 $C^S$ 为键，对 $S^S$ 进行调制，生成与目标内容动态对齐的调制风格特征 $\tilde{S}^S$。这一过程的核心在于：跨注意力自动识别风格应从风格运动的哪个身体部位传递到内容运动的对应部位，从而避免无关部位的风格污染。

**3. 运动生成阶段**  
运动生成器 $G$ 以内容动态 $Y^C$ 和调制风格 $\tilde{S}^S$ 为输入，通过多个Transformer块逐层生成最终运动。每个Transformer块内采用自适应实例归一化（AdaIN）将调制风格注入内容特征，最终输出包含局部关节旋转、全局根位移和速度的完整运动序列。

### 关键设计要点

- **统一运动表示**：输入运动被分解为身体部位嵌入和全局运动标记（根位移与速度），使PSM能够在部位级别进行细粒度风格对齐，同时让生成器直接合成全局平移，消除了现有方法中“从内容运动复制全局平移”的后处理步骤。
- **端到端可微**：整个pipeline从特征提取到运动生成完全端到端训练，无需分阶段优化或手工规则介入。
- **无后处理**：MoST直接输出可用运动，不依赖脚部接触修正或全局轨迹复制等启发式后处理——这一特性源于PSM的部位感知调制能力和物理正则化损失的联合作用（详见损失函数部分）。

框架的整体架构如 **Figure 2(a)** 所示，PSM的详细操作见 **Figure 2(b)**。

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overall framework of MoST comprising Siamese motion encoders E, motion generator ${ \mathcal { G } }$ , and part-attentive style modulator (PSM). PSM modulates style feature $S ^ { S }$ under the condition of both contents of content motion and style motion, i.e., $\dot { C } ^ { C }$ and $C ^ { S } . \mathcal { G }$ generates final output motion with content dynamics feature $Y ^ { C }$ and the modulated style feature $\tilde { S } ^ { S }$ . (b) Detailed operations in PSM*



### 整体框架

MoST 框架由三个核心模块组成：Siamese 运动编码器 $E$、部位感知风格调制器 (Part-Attentive Style Modulator, PSM) 和运动生成器 $G$（Figure 2）。给定内容运动 $M^C$ 和风格运动 $M^S$，框架生成风格迁移后的运动 $M^G$：

$$M^G = \text{MoST}(M^C, M^S)$$

编码器 $E$ 从单个运动同时提取内容动态特征 $Y$ 和身体部位特异的风格特征 $S$：

$$\mathcal{E}(M^C) = \{S^C, Y^C\}, \quad \mathcal{E}(M^S) = \{S^S, Y^S\}$$

PSM 以 $C^C$ 和 $C^S$（分别为 $Y^C$ 和 $Y^S$ 经实例归一化后的内容特征）作为条件，对风格特征 $S^S$ 进行调制，生成与目标内容对齐的调制风格 $\tilde{S}^S$。生成器 $G$ 以内容动态 $Y^C$ 和调制风格 $\tilde{S}^S$ 为输入，通过 AdaIN 将风格注入内容，生成最终运动。

### 运动表示与部位嵌入

运动序列 $M$ 定义为 $T$ 帧、$J$ 个关节的局部旋转 $m_t^j \in \mathbb{R}^7$（四元数 + 3D 位移）、全局根位移 $m_t^{root} \in \mathbb{R}^7$ 和全局速度 $v_t \in \mathbb{R}^3$。人体关节按语义划分为 $P$ 个身体部位（如左臂、右腿等），每个部位 $i$ 包含 $J^i$ 个关节。第 $t$ 帧第 $i$ 个部位的嵌入通过拼接部位内关节向量并全连接投影得到：

$$\bar{p}_{(t,i)} = \text{FC}(p_{(t,i)}) \in \mathbb{R}^d, \quad p_{(t,i)} = ||_{j}^{J^i} m_t^j \in \mathbb{R}^{7 N_{J^i}}$$

全局平移嵌入由根位移和速度的嵌入拼接而成：

$$\bar{g}_t = [\bar{m}_t^{root}; \bar{v}_t] \in \mathbb{R}^d, \quad \bar{m}_t^{root} = \text{FC}(m_t^{root}), \quad \bar{v}_t = \text{FC}(v_t)$$

### Siamese 运动编码器

编码器 $E$ 采用 Transformer 架构，包含 $N$ 个编码块。输入为身体部位嵌入 $\bar{p}_{(t,i)}$ 和全局平移嵌入 $\bar{g}_t$。在第 $N-1$ 层输出 $\hat{Z}^{N-1}$ 上应用通道级实例归一化（Instance Normalization, IN）以去除风格特征：

$$\check{Z}_{t,i}^{N-1} = \frac{\hat{Z}_{t,i}^{N-1} - \mu(\hat{Z}^{N-1})}{\sigma(\hat{Z}^{N-1})}$$

经 IN 处理后的特征作为内容特征 $C$，而未归一化的原始特征保留风格信息，经可学习的 style token 聚合为全局风格特征 $S$。这一设计使编码器能从同一运动中同时解耦出内容动态 $Y$ 和风格表示 $S$。

### 部位感知风格调制器 (PSM)

PSM 是 MoST 的核心创新，其关键在于利用跨注意力机制将源风格特征与目标内容动态对齐。具体而言，PSM 以内容运动的内容特征 $\bar{C}^C$ 作为 Query，风格运动的内容特征 $\bar{C}^S$ 作为 Key，风格运动的风格特征 $\bar{S}^S$ 作为 Value，通过多头跨注意力实现部位级风格调制：

$$\text{crossMHA}(\bar{C}^C, \bar{C}^S, \bar{S}^S) = (||_{i=1}^h H_i) W_H$$

$$H_i = \text{Attn}\left(\text{LN}(\bar{C}^C) W_i^Q,\; \text{LN}(\bar{C}^S) W_i^K,\; \text{LN}(\bar{S}^S) W_i^V\right)$$

该机制的本质是：通过内容-内容的注意力匹配，识别风格运动中的哪个身体部位与内容运动中的哪个身体部位在语义上对应，然后将对应部位的风格特征传递过去。例如，从 Punch 动作的手臂部位提取风格，并将其注入 Kick 动作的对应部位（腿部），而非简单地将风格全局复制。Figure 7 的跨注意力热力图验证了这一机制——最高列指示风格来源部位，最高元素指示接收风格的目标部位。

### 运动生成器与 AdaIN 注入

生成器 $G$ 同样基于 Transformer，每个生成块中通过自适应实例归一化（AdaIN）将调制后的风格特征注入内容特征。在第 $n-1$ 层的输出 $U^{n-1}$ 上：

$$\hat{U}_{t,i}^{n-1} = \gamma \left( \frac{U_{t,i}^{n-1} - \mu(U^{n-1})}{\sigma(U^{n-1})} \right) + \beta$$

其中 $\gamma$ 和 $\beta$ 由调制风格 $\tilde{S}^S$ 经全连接层生成，控制风格注入的尺度和偏移。最终输出特征通过全连接层重建为关节旋转、根位移和速度：

$$\{\hat{m}_t^j \in \mathbb{R}^7 | j \in J^i\} = \text{FC}(\hat{U}_{t,i}^N), \quad (i \le P)$$

$$\hat{m}_t^{root} = \text{FC}(\hat{U}_{t,(P+1)}^N) \in \mathbb{R}^7, \quad \hat{v}_t = \text{FC}(\hat{U}_{t,(P+1)}^N)$$

### 关键损失函数

**风格解耦损失** $L_D$ 是强制风格与内容分离的关键。对于相同内容运动 $M^C$，给定两个具有相同风格标签但不同内容的风格运动 $M_a^S$ 和 $M_b^S$，最小化两个生成运动之间的差异：

$$L_D = \mathbb{E}_{M^C, M_a^S, M_b^S \sim \mathbb{M}} \left\| \text{MoST}(M^C, M_a^S) - \text{MoST}(M^C, M_b^S) \right\|_2$$

该损失的因果逻辑是：如果模型真正将风格与内容解耦，那么相同风格（即使来自不同内容）应产生接近的生成结果。消融实验（Table 2）证实，$L_D$ 使 CC 从 19.7 降至 9.3，并使风格特征空间在 t-SNE 可视化中形成良好分离的聚类（Figure 5）。

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/009_Figure_5.jpg]]
*Figure 5: (a-b) Visualization of the modulated style feature ( $\tilde { S } ^ { S }$ ) space of MoST in different loss settings. $L _ { p r e }$ and $L _ { p h y }$ are applied by default in (a). $L _ { D }$ is additionally introduced in (b). All training and testing data are used as style motion, and a single data point in the test set is employed for content motion. The spaces are projected in 2D through t-SNE. The samples are visualized with different shapes according to their content labels and different colors according to their style labels. (c) Space of $S ^ { S }$ before PSM. All loss functions are applied*

**物理正则化损失** $L_{phy}$ 由三项组成，用于提高运动平稳性和接地真实性：

$$L_{phy} = \lambda_{vel} R_{vel} + \lambda_{acc} R_{acc} + \lambda_{foot} R_{foot}$$

其中 $R_{foot}$ 惩罚接地帧的脚部速度，间接促进合理的脚部接触，替代了先前方法中启发式后处理的需求。但需注意，该损失无法完全消除脚部滑动问题（见局限性）。

### 补充图表

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/003_Figure_3.jpg]]
*Figure 3: Description of evaluation metrics, using easy-to-recognize label notations. Note that our model uses only motion data*

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results in Xia [30] and BFA [1] datasets. Please refer to the red indications. (1) Our method better reflects the style of old in comparison to other existing methods, accurately representing both the bent upper body and leg. (2) Other methods fail to preserve the content of punch, instead, they result in peculiar leg movements or body twists. On the other hand, our result accurately depicts strutting punch, where the upper body leans backward. (3) The results of [1] and [14] do not exhibit a kick, instead, their arm moves. [20] yields twisted leg movements. (4) Unlike our method, others fail to preserve the content of punch, resulting in vibrations in static poses or twists*



## 实验与关键发现

### 主实验结果

MoST 在 Xia 数据集 上进行了定量评估，采用内容一致性（CC）和风格一致性++（SC++）作为指标——两者越低表示迁移越成功。**Table 1** 显示，MoST 在同等内容（CC 8.0）和不同内容（CC 8.7）两种设置下均取得最低的内容一致性分数，并在 SC++ 上同样达到最优。这意味着 MoST 不仅成功迁移了风格，还最大程度地保留了原始内容运动的结构完整性。

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/004_Table_1.jpg]]
*Table 1: Motion style transfer results evaluated in content consistency (CC) and style consistency++ (SC++ ) on Xia dataset [30]. The performances are reported in both cases: when $M ^ { C }$ and $M ^ { S }$ have identical content labels and different content labels*

与先前方法的定性对比（**Figure 4**）进一步验证了这一优势。在内容运动为“踢腿”、风格运动为“拳击”的典型案例中，**Aberman et al.** (TOG 2020) 生成的运动完全扭曲，**MotionPuzzle** (Jang et al., TOG 2022) 则直接复制了风格运动的内容，而 MoST 的输出既保持了踢腿的动作内容，又注入了拳击的刚硬风格特征。值得注意的是，MoST 的所有结果均为原始输出，无需任何后处理（如复制全局平移或强制脚部接触），而先前方法普遍依赖此类启发式修正。

### 消融实验

**Table 2** 系统验证了 Part-Attentive Style Modulator (PSM) 和风格解耦损失 $L_D$ 的各自贡献：

**PSM 的消融**：移除 PSM（即直接使用未经调制的风格特征 $S^S$ 注入生成器）导致 CC 从 8.5 急剧上升至 37.4，SC++ 从 63.0 升至 69.5。这表明 PSM 的跨注意力机制有效防止了不相关身体部位的风格污染——没有 PSM 时，风格特征会不加区分地覆盖所有身体部位，严重破坏内容结构。

**$L_D$ 的消融**：移除风格解耦损失后，CC 从 8.5 升至 19.7，SC++ 从 63.0 升至 68.6。**Figure 5** 的 t-SNE 可视化提供了直观解释：加入 $L_D$ 后，调制风格特征 $\tilde{S}^S$ 在空间中按风格类别形成清晰分离的簇，而未加 $L_D$ 时不同风格的特征混杂在一起。这证明 $L_D$ 强制模型将风格信息与内容解耦，使风格迁移更加纯粹。

**联合效果**：PSM 与 $L_D$ 联合使用达到最佳性能（CC 8.5, SC++ 63.0），且 **Figure 6** 显示 PSM 能够根据内容运动的不同将同一风格特征分散到不同方向，验证了其“内容条件化”的调制能力。

### 关键可视化结论

**Figure 7** 的跨注意力热力图揭示了 PSM 的工作机制。在“拳击风格 → 踢腿内容”的迁移中，注意力图显示风格主要源自拳击运动的手臂部位，并被精确映射到踢腿运动的腿部部位。这表明 PSM 学会了识别激活的身体部位，并仅在相应部位进行风格调制，从而在不污染其他部位的前提下完成风格迁移。

### 失败模式与局限性

尽管 MoST 在定量和定性评估中表现优异，仍存在以下局限：

1. **脚部接触问题**：物理正则化项 $R_{foot}$ 虽能惩罚接地帧的脚部速度，但部分生成样本仍可能出现脚部滑动或漂浮现象，无法完全消除。
2. **固定长度限制**：基于 Transformer 的架构需预设最大运动长度，对可变长度运动的灵活性构成约束。
3. **数据集规模**：实验仅在 Xia 和 BFA 两个小型动捕数据集上进行，未在大规模或野外数据集上验证泛化能力。
4. **少样本/零样本未探索**：当前方法依赖完整风格运动作为输入，未测试在少样本或零样本场景下的风格迁移能力。

### 实验公平性说明

所有对比方法均使用相同的运动表示和训练/测试分割。Table 1 中与其他方法的完整数值对比因论文文本省略而部分缺失，但原文明确指出 MoST 在 CC 和 SC++ 上均取得最低值，尤其在内容不同的运动对上优势显著。部分定量结论主要依赖消融实验的内部对比，缺少与所有基线方法在相同指标上的完整数值矩阵，这一点需读者在引用时注意核实。

### 补充图表

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/006_Figure_7.jpg]]
*Figure 7: Cross-attention maps of PSM. The highest column ( ) indicates the body part in the style motion from which the style originates. The highest element ( ) pinpoints the body part in the content motion that will receive the style. Traj. refers to global translation. The symbols and are indicators related to traj*

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/007_Table_2.jpg]]
*Table 2: Ablation study for verifying the proposed $L _ { D }$ , , and PSM on Xia dataset [30]. $L _ { p r e }$ and $L _ { p h y }$ are applied by default*

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/001_Figure_1.jpg]]
*Figure 1: Frequent failure cases in existing methods: (a) A result of MotionPuzzle [14] replicating style motion. (b) A result of Aberman et al. [1] showing complete failure with twisted motion. The character for the visualization is sourced from Mixamo [13]*

![[assets/figures/papers/paper_list_l3_MoST_Motion_Style_Transformer_between_Diverse_Action_Contents/figures/010_Figure_6.jpg]]
*Figure 6: Visualization of $S ^ { S }$ and $\tilde { S } ^ { S }$ spaces projected through t-SNE for all 56 ( $M ^ { C } ) \times$ 5 6 ( $M ^ { S }$ ) motion pairs in the test set*



## 定位与知识库关联

### 1. 在运动风格迁移谱系中的位置

MoST 处于**基于深度学习的运动风格迁移**这一研究脉络中，但其核心贡献在于首次系统性地解决了**跨内容（cross-content）风格迁移**的难题。此前的代表性工作可分为以下几类，均在不同维度上存在局限：

- **基于 Temporal AdaIN 的方法**：以 **Aberman et al.** (TOG 2020) 为典型代表，通过自适应实例归一化在时序维度上注入风格特征。该方法在内容运动与风格运动具有相似动作类型时表现尚可，但当内容差异较大时（如将“拳击”风格迁移至“踢腿”），会出现严重的运动扭曲甚至完全失效（Figure 1b）。其根本原因在于缺乏显式的风格-内容解耦机制，风格特征中不可避免地混杂了源运动的内容信息。

- **基于身体部位任意风格组合的方法**：**MotionPuzzle** (Jang et al., TOG 2022) 允许从不同运动中提取身体部位风格进行组合，但其风格迁移机制本质上依赖于内容运动与风格运动之间的结构对应关系。当内容差异显著时，该方法倾向于直接复制风格运动的姿态，而非将风格特征迁移至目标内容上（Figure 1a），暴露出其缺乏动态对齐能力的弱点。

- **基于多域风格生成模型的方法**：**Park et al.** (PACMCGIT 2021) 通过多域生成框架学习不同风格之间的映射，但同样未显式建模风格与内容的解耦，在跨内容场景下的泛化能力有限。

- **基于自回归生成流的方法**：**Wen et al.** (CVPR 2021) 采用归一化流进行风格迁移，虽然生成质量较高，但其自回归性质导致推理效率较低，且同样未针对跨内容迁移进行专门设计。

MoST 与上述方法的根本分界线在于两点：（1）**Part-Attentive Style Modulator (PSM)** 通过跨注意力机制实现了源风格特征与目标内容特征在身体部位级别的动态对齐，使风格迁移不再依赖于内容的一致性；（2）**风格解耦损失 $L_D$** 显式强制网络将风格与内容分离，从训练信号层面解决了此前方法依赖隐式学习的不足。

### 2. 核心方法差异的因果机制

MoST 相对于基线方法的改进并非简单的模块堆砌，而是针对瓶颈问题的因果性干预：

| 改进槽位 | 基线做法 | MoST 做法 | 解决的因果瓶颈 |
|----------|----------|-----------|----------------|
| 风格与内容特征提取 | 分离的内容/风格编码器，仅提取全局风格特征 | Siamese motion encoder 同时提取内容动态 $Y$ 和身体部位特异的风格特征 $S$，并通过 style token 聚合全局风格 | 统一表示空间使后续的跨注意力调制成为可能 |
| 风格特征注入 | 直接注入原始风格特征（如 AdaIN）或短窗口风格编码 | PSM 利用跨注意力根据目标内容调制源风格特征，实现身体部位级对齐 | 消除风格特征中混杂的内容信息，防止无关身体部位被错误调制 |
| 风格解耦监督 | 无显式解耦损失，依赖网络隐式学习 | $L_D$ 最小化相同风格但不同内容的两个输出差异 | 强制风格与内容在特征空间中的分离（t-SNE 可视化证实，Figure 5） |
| 全局运动生成 | 从内容运动复制全局平移（后处理） | 在输入嵌入中加入全局平移和速度标记，通过注意力与身体部位交互直接生成 | 消除启发式后处理引入的不一致性 |
| 脚部接触处理 | 启发式修正或强制地面接触 | 基于物理的正则化项 $R_{foot}$ 惩罚接地帧的脚部速度 | 间接促进合理接触，避免硬约束带来的运动不自然 |

消融实验（Table 2）为上述因果链条提供了定量证据：PSM 的引入将内容一致性（CC）从 37.4 降至 19.7，表明跨注意力调制有效阻止了不相关身体部位的风格传输；$L_D$ 的加入进一步将 CC 降至 9.3，同时风格一致性（SC++）从 69.5 降至 63.0，证明显式解耦监督能够提升迁移质量。两者联合使用时达到最优性能（CC 8.5, SC++ 63.0）。

### 3. 适用边界与局限

尽管 MoST 在跨内容风格迁移上取得了显著进展，其适用边界仍受以下因素制约：

1. **数据规模与多样性**：研究仅在小型动捕数据集（Xia 数据集、BFA 数据集）上验证，尚未在更大规模或野外采集的运动数据上测试。模型对数据分布外（OOD）的风格-内容组合的泛化能力仍不明确。

2. **物理真实性的不完全保证**：虽然引入了 $R_{foot}$ 正则化项，部分生成样本仍可能出现脚部滑动或漂浮现象。物理损失无法完全强制消除该问题，说明仅靠数据驱动的正则化难以完全替代物理仿真。

3. **固定长度的架构限制**：基于 Transformer 的架构需预设最大运动长度，这限制了处理可变长度运动序列的灵活性。对于需要实时交互或流式处理的场景，该限制可能成为瓶颈。

4. **未探索的少样本/零样本场景**：模型需要充分的风格-内容配对训练数据，未验证在少样本（few-shot）或零样本（zero-shot）条件下的风格迁移能力。考虑到运动捕捉数据的高昂获取成本，这一能力的缺失限制了其在实际应用中的部署灵活性。

### 4. 开放问题与未来方向

基于 MoST 的方法框架和现有局限，以下几个研究方向值得关注：

1. **测试时物理优化**：能否在测试阶段通过优化手段（如强化学习或可微物理仿真）完美消除脚部接触问题，而非仅依赖训练时的正则化损失？这将直接影响生成运动在游戏、动画等应用中的可用性。

2. **少样本风格迁移**：如何将 MoST 的框架扩展为少样本学习范式？一个潜在方向是利用 PSM 的跨注意力机制作为风格适配器，在少量新风格样本上仅微调调制参数，而非重新训练整个网络。

3. **关节级别的细粒度风格控制**：PSM 当前在身体部位粒度上进行注意力调制（Figure 7 展示了 Punch→Kick 时从手臂到腿部的风格转移）。该机制是否能进一步细化为关节级别的风格迁移，以实现更精细的运动编辑？

4. **多模态条件风格控制**：MoST 的框架是否能够结合文本描述、音乐节奏或情感标签等附加条件，实现多模态驱动的风格迁移？这将使模型从“运动到运动”的迁移扩展为“条件到运动”的生成，大幅拓宽应用场景。

5. **与大规模运动生成模型的融合**：随着运动生成基础模型的发展，MoST 的风格解耦与调制机制能否作为插件模块嵌入到更大的预训练模型中，实现零样本风格迁移？这需要验证 PSM 的跨注意力机制在更大规模异构数据上的鲁棒性。



## 原文 PDF

![[paperPDFs/CVPR_2024/MoST_Motion_Style_Transformer_between_Diverse_Action_Contents.pdf]]

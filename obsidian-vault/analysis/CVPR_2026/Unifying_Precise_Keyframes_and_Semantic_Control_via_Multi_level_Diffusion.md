---
title: "Unifying Precise Keyframes and Semantic Control via Multi-level Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unifying_Precise_Keyframes_and_Semantic_Control_via_Multi_level_Diffusion.pdf
project_link: null
code_link: null
aliases:
- MLDFTCMBK
- UPKSCMLD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: "多层级扩散框架中的局部-全局引导机制与推断时的轨迹-姿态精炼策略。局部引导利用单个关键帧细化局部过渡，全局引导整合文本语义与关键帧序列线索以调节整体动态；轨迹精炼按速度比例修正根位移以消除滑动，姿态精炼通过扩散填补强制满足姿态约束。"
primary_logic: "通过分离全局语义控制与局部关键帧对齐，并利用基于速度比例的轨迹精炼在推理时实现硬约束，同时通过多层级引导将文本高层语义与关键帧底层时空线索深度融合，从而生成既严格遵循关键帧又忠实表达语义的运动。"
claims:
- "在 HumanML3D 测试集上实现零关键帧误差，严格满足所有空间约束。"
- "多层级引导（局部+全局）与轨迹精炼共同作用，显著提升了关键帧遵循度与语义一致性。"
- "基于速度比例的轨迹精炼有效避免了脚步滑动伪影，优于均匀误差分配和单纯填补。"
- "HumanML3D 关键帧插补（7个关键帧） 上 关键帧误差 (cm) = 0.000"
---

# Unifying Precise Keyframes and Semantic Control via Multi-level Diffusion

> [!tip] 核心洞察
> 通过分离全局语义控制与局部关键帧对齐，并利用基于速度比例的轨迹精炼在推理时实现硬约束，同时通过多层级引导将文本高层语义与关键帧底层时空线索深度融合，从而生成既严格遵循关键帧又忠实表达语义的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过多层扩散统一精确关键帧与语义控制 |
| 英文题名 | Unifying Precise Keyframes and Semantic Control via Multi-level Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://cvpr.thecvf.com/virtual/2026/poster/38659) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Multi-level Diffusion Framework (text-conditioned motion in-betweening with keyframes) |
| Dataset | HumanML3D 关键帧插补（7个关键帧）, HumanML3D 部分关节控制（根+末端效应器） |

> [!tip] 效果简介
> - HumanML3D 关键帧插补（7个关键帧） 上，关键帧误差 (cm) 0.000 vs 其它方法存在不可忽略的空间偏差 (N/A)；R-Precision (Top 3) 0.803 vs 次优方法 ≤ 0.797 (+0.006)；FID 0.023 vs 次优方法 ≈ 0.028 (-0.005)。
> - HumanML3D 部分关节控制（根+末端效应器） 上，关键帧误差 (cm) 0.000 vs 其它方法存在偏差 (N/A)；R-Precision (Top 3) 0.813 vs 次优方法 ≈ 0.805 (+0.008)。

## 概要

### 问题与瓶颈

文本条件运动插补旨在根据文本描述和稀疏关键帧约束生成连续人体运动序列，在动画制作、游戏开发等领域具有重要应用价值。然而，现有方法面临一个核心瓶颈：**文本语义与关键帧时空约束难以有效对齐**。如图 Figure 2 所示，先前方法存在两类典型缺陷——一方面缺乏低层语义控制，生成的运动在关键帧指定时间点之后仍冗余执行已完成的动作，且无法维持关键帧所规定的姿态；另一方面缺乏精确的关键帧遵循能力，在约束帧处产生显著的空间偏差。这一瓶颈的根源在于，现有方法仅将关键帧作为软条件注入扩散过程，无法保证硬约束的严格满足，同时忽略了关键帧序列本身蕴含的时序语义结构。

### 核心方法

针对上述问题，本文提出**多层扩散框架（Multi-level Diffusion Framework）**，通过分离全局语义控制与局部关键帧对齐，实现文本语义与时空约束的深度融合。框架包含四个关键模块：

- **局部引导（Local Guidance）**：利用单个关键帧的嵌入特征与含噪运动特征融合，通过 U-Net 卷积操作自适应调制关键帧周围的局部过渡，促进精确空间对齐。
- **全局引导（Global Guidance）**：引入关键帧变换器编码器捕获关键帧序列的全局时空模式，将其与文本特征融合后通过交叉注意力注入扩散 U-Net，调节整体运动动态。
- **轨迹精炼（Trajectory Refinement）**：在推理阶段，按根关节速度比例自回归地分配位置误差，修正根轨迹以消除脚步滑动伪影。
- **姿态填补（Pose Refinement）**：通过扩散填补将关键帧指定姿态强制替换到生成运动中，实现硬约束的严格满足。

该方法的核心洞察在于：**通过多层级引导将文本高层语义与关键帧底层时空线索解耦并协同，同时利用基于速度比例的轨迹精炼在推理时实现硬约束**，从而生成既严格遵循关键帧又忠实表达语义的运动。

### 主要结果

在 HumanML3D 测试集上的关键帧插补实验中（Table 1），本方法实现了**零关键帧误差（Keyframe Error = 0.000）**，严格满足所有空间约束，同时语义一致性指标 R-Precision（Top 3）达到 0.803，FID 降至 0.023，均优于现有最优方法。消融实验（Table 4）证实，局部引导与全局引导的协同作用将关键帧误差从仅全局引导时的 3.2 大幅降至 0.667，进一步引入轨迹精炼和姿态填补后实现完全零误差。定性对比（Figure 6）表明，本方法的速度比例轨迹精炼策略有效避免了均匀误差分配导致的滑动伪影和单纯填补引入的抖动，在保证空间精度的同时保持了自然的脚部接触模式。

### 方法谱系与知识库定位

本工作处于**文本条件运动生成与时空控制**的交叉领域。与基于扩散的关键帧插补方法 **Flexible Motion In-betweening**（Cohan et al., SIGGRAPH 2024）相比，本方法将关键帧从软条件升级为多层级硬约束；与掩码扩散控制方法 **MaskControl**（Pinyoanuntapong et al., ICCV 2025）和联合文本-轨迹控制方法 **OmniControl**（Xie et al., ICLR 2024）相比，本方法通过关键帧变换器编码器显式建模关键帧序列的语义结构，而非简单拼接条件；与通用文本条件扩散基线 **MDM**（Tevet et al., ICLR 2023）和稀疏关节控制方法 **Keyjoint Control**（Hwang et al., ICCV 2025）相比，本方法在推理阶段引入了可保证硬约束的轨迹-姿态精炼机制。该方法同时支持语义保持的运动编辑任务，在局部姿态编辑和全局轨迹编辑场景下均展现出优于基于优化的 **DNO** 方法的性能（Table 5）。

### 局限与展望

当前方法在文本语义与关键帧约束严重冲突时可能难以生成满意过渡，需人工调整条件；推理阶段的 DDIM 反演增加了计算开销，限制了实时交互应用；模型仅在 HumanML3D 数据集上验证，对高动态动作（如杂技）的泛化能力尚待检验。未来方向包括自动冲突检测与调解、引入物理模拟约束，以及扩展至多人交互和物体操作场景。



### 问题背景：文本条件运动插补的双重困境

运动生成是计算机视觉与图形学交叉领域的关键任务，其目标是根据用户指定的控制信号合成自然的人体运动序列。在众多控制模态中，**文本条件运动插补**（text-conditioned motion in-betweening）因其直观性和表现力而备受关注：用户通过自然语言描述期望的运动语义（如“捡起箱子后高举过头顶走向目标”），同时以稀疏关键帧（keyframes）指定特定时刻的姿态约束，系统则负责生成连接这些关键帧的平滑过渡运动。

这一任务的核心挑战在于同时满足两个看似矛盾的需求：
- **语义准确性**：生成的过渡运动必须忠实表达文本所描述的高层动作语义；
- **精确空间控制**：生成的运动必须在指定时刻严格匹配关键帧的姿态与位置约束。

### 现有方法缺口：语义与时空约束的失配

当前主流的文本条件运动插补方法（如 **Flexible Motion In-betweening** (Cohan et al., SIGGRAPH 2024)、**MaskControl** (Pinyoanuntapong et al., ICCV 2025)、**OmniControl** (Xie et al., ICLR 2024)）普遍存在两类关键缺陷（如 Figure 2 所示）：

1. **低层语义控制不足**：现有方法通常将文本作为全局条件注入扩散模型，但忽略了关键帧序列本身隐含的时序语义结构。这导致生成的过渡运动可能违背关键帧所指示的动作阶段划分——例如，在关键帧已明确标示“高举过头顶”的姿态后，过渡段仍冗余执行“捡起”动作，破坏了动作的语义连贯性。

2. **关键帧遵循精度缺失**：由于关键帧约束仅作为软条件（通过条件特征拼接或注意力注入）参与生成过程，模型在关键帧处的输出往往存在不可忽略的空间偏差。这种偏差在需要精确空间对齐的应用场景（如游戏动画、电影预演）中是不可接受的。

从因果机制来看，这两类缺陷共享同一个根本瓶颈：**现有框架缺乏将文本高层语义与关键帧底层时空约束进行有效对齐的机制**。文本描述了“做什么”，关键帧规定了“何时处于何种姿态”，但两者的信息流在现有模型中相互孤立，导致语义控制与空间控制无法协同。

### 本文动机：多层级解耦与硬约束精炼

针对上述瓶颈，本文提出一个核心洞察：**全局语义控制与局部关键帧对齐应当被分离处理，并在推理阶段通过物理上可解释的硬约束策略强制执行关键帧遵循**。

具体而言，本文的动机源于以下三个关键设计选择：

- **多层级引导**：训练时，通过局部引导（利用单个关键帧细化其周围局部过渡）与全局引导（利用关键帧序列的时空模式与文本语义联合调节整体动态）的分离，使模型既能精确对齐关键帧，又能保持动作的语义连贯性。
- **轨迹精炼**：推理时，针对根关节位置误差，提出基于速度比例的误差分配策略（而非均匀分配），在消除脚步滑动伪影的同时实现根轨迹与关键帧的精确对齐。
- **姿态填补**：在轨迹精炼之后，通过扩散填补将关键帧指定姿态强制替换到生成运动中，以硬约束形式确保零关键帧误差。

这一框架在 HumanML3D 测试集上实现了关键帧误差为 0.000 的严格遵循（Table 1），同时在语义一致性指标（R-Precision Top 3 达 0.803）上超越现有最优方法，证明了语义表达与空间控制可以兼得。



## 核心方法与创新机理

本工作的核心创新在于提出了一套**多层级扩散框架**，通过训练时的结构化引导与推理时的硬约束精炼，首次在文本条件运动插补任务中同时实现了**零关键帧误差**与**高层语义对齐**，解决了现有方法普遍存在的“关键帧偏差”与“低层语义控制不足”的双重瓶颈（Figure 2）。

### 关键机制创新（Changed Slots）

相较于以 **Flexible Motion In-betweening**（Cohan et al., SIGGRAPH 2024）、**OmniControl**（Xie et al., ICLR 2024）和 **MDM**（Tevet et al., ICLR 2023）为代表的现有方法，本工作在三个核心维度上实现了根本性突破：

**1. 关键帧约束执行：从软条件到硬约束的质变**

现有方法将关键帧仅作为软条件特征注入扩散过程，无法保证生成运动在约束帧处严格匹配目标姿态，导致关键帧误差不可忽略。本方法通过“训练期多层级引导 + 推理期轨迹-姿态联合精炼”的组合策略，将约束执行从概率性软对齐升级为确定性硬满足：
- **训练期**：局部引导（Local Guidance）将单帧关键帧嵌入与含噪运动特征融合，通过U-Net卷积自适应调制关键帧周围的局部过渡；全局引导（Global Guidance）则通过关键帧变换器编码器提取关键帧序列的时空模式，与文本特征融合后经交叉注意力注入U-Net，调节整体运动动态（Figure 3, Figure 4）。
- **推理期**：轨迹精炼（Trajectory Refinement）按根速度比例自回归地分配位置误差，消除根关节的累积漂移；姿态精炼（Pose Refinement）通过扩散填补将生成姿态强制替换为关键帧指定值，最终实现关键帧误差严格归零（Table 1, Keyframe Error = 0.000）。

**2. 全局语义与关键帧时序整合：从单一文本条件到多层级语义融合**

现有方法仅将文本作为全局条件，忽略了关键帧序列本身蕴含的丰富语义结构（如动作的阶段切换、节奏变化）。本方法的关键帧变换器编码器（Figure 4）通过可学习令牌从稀疏关键帧序列中提取紧凑的全局时空表征，并与CLIP文本特征融合，使扩散模型能够同时感知“文本说了什么”和“关键帧序列暗示了什么”。这一设计使得生成的运动既能响应文本的高层语义（如“捡起箱子”），又能精确遵循关键帧指定的低层时空边界（如“何时开始行走”），从根本上解决了Figure 2揭示的低层语义控制缺失问题。

**3. 推理阶段轨迹误差修正：从均匀分配到速度比例精炼**

现有方法在推理阶段要么不修正根轨迹误差，要么采用均匀分配策略，前者导致关键帧位置偏差，后者则引入明显的脚步滑动伪影（Figure 6）。本方法的核心洞察在于：**根位置误差的分配应与各帧的运动强度成正比**——在快速移动的帧分配更多校正量，在静止或慢速帧分配更少，从而在消除累积漂移的同时保持自然的脚部接触模式。具体而言，轨迹精炼通过公式（2）计算各帧在各方向上的速度比例权重 $w_{n,d}$，将关键帧间的根位置误差 $\Delta \mathbf{r}$ 按此权重分配到各帧速度上（公式3），再从上一个关键帧累计重构整段根轨迹（公式4-5）。消融实验（Table 4）证实，仅引入轨迹精炼即可将根位置误差（KRE）消除至0.000；定性对比（Figure 6）则直观展示了比例分配策略相较于均匀分配在避免滑动伪影上的显著优势。

### 创新性总结

上述三个changed slots并非孤立改进，而是存在深层因果关联：**多层级引导**为语义-空间对齐提供了结构化训练信号，使模型在生成阶段就能产出接近约束的运动；**轨迹-姿态精炼**则在推理阶段将“接近”提升为“精确”，通过硬约束操作消除了剩余偏差。这种“训练期软引导 + 推理期硬满足”的协同设计，是本方法在HumanML3D测试集上实现零关键帧误差（Table 1）与最优语义一致性（R-Precision Top 3 = 0.803, FID = 0.023）的根本原因。



本文提出的**多层扩散框架（Multi-level Diffusion Framework）**旨在解决文本条件运动插补中一个核心瓶颈：如何将文本语义与关键帧的时空约束有效对齐，从而同时满足语义准确性和精确空间控制。框架将这一复杂任务解耦为四个协同模块，形成从条件编码、多层引导到推断精炼的完整管线（Figure 3）。

### 输入与输出定义

系统的输入由三部分构成：
- **文本提示**：描述整体运动语义，通过 CLIP 和转换器编码为固定长度的文本特征。
- **关键帧集合**：用户指定的稀疏时空约束，以特征矩阵 $\mathbf{K} \in \mathbb{R}^{\bar{\mathcal{N}} \times D}$ 表示，其中 $\bar{\mathcal{N}}$ 为关键帧数量，$D$ 为关节特征维度。未约束的条目置零。
- **关键帧掩码** $\mathbf{m}_{\mathbf{K}} \in \{0,1\}^{N \times D}$：指示哪些关节特征在哪些帧受到约束。

输出为一段长度为 $N$ 的运动序列，该序列必须严格遵循关键帧的空间约束，同时在过渡区域保持与文本语义一致的动态模式。

### 管线四模块

框架按前向流程包含四个功能模块，其中前三者在训练时协同优化，第四者在推断时独立执行：

#### 1. 条件编码（Condition Encoding）

该模块负责将异构输入转化为统一的特征表示。文本经 CLIP 编码后通过转换器得到文本特征；关键帧约束与掩码拼接后经 MLP 获得关键帧嵌入 $\mathbf{e}_k$。这一双路编码为后续的局部和全局引导提供了结构化的条件信号。

#### 2. 局部引导（Local Guidance）

局部引导聚焦于**单个关键帧周围的过渡质量**。其核心操作是将当前帧的含噪运动特征与对应位置的关键帧嵌入沿特征维度拼接，经 MLP 融合后注入 U-Net 的卷积层。这种帧级别的自适应调制使模型能够在关键帧附近产生平滑且精确的空间过渡，是保证低层语义控制的关键机制。

#### 3. 全局引导（Global Guidance）

全局引导负责**调节整体运动动态**，使生成的运动在宏观层面与文本语义和关键帧序列的隐含结构保持一致。该模块引入了一个**关键帧变换器编码器**（Figure 4）：将关键帧嵌入与一个可学习令牌拼接，加入位置编码以标识时序顺序，经掩码过滤后送入变换器，输出的可学习令牌对应特征作为紧凑的全局关键帧表示。这一全局特征与文本特征沿令牌维度拼接后，通过交叉注意力机制注入 U-Net，从而在扩散去噪过程中持续调节整体动态。

#### 4. 推断精炼（Inference Refinement）

前三个模块在训练时已能生成语义一致的运动，但无法**严格保证**关键帧的硬约束。推断精炼模块在扩散后期通过两步操作强制执行空间约束：

- **轨迹精炼**：计算生成关键帧与目标关键帧之间的根关节位置误差 $\Delta \mathbf{r}$，按各帧在各维度上的根速度比例分配校正权重，自回归地修正整段根轨迹，从而消除脚步滑动伪影。
- **姿态精炼**：利用扩散填补机制，将用户指定的关键帧特征矩阵按掩码直接替换到预测运动中，强制实现关键帧姿态的严格对齐。

### 数据流关系

整个管线的数据流可概括为：**条件编码**将文本和关键帧转化为特征 → **局部引导**与**全局引导**在扩散去噪的每一步分别从帧级和序列级调节运动生成 → 扩散输出预测运动 $\hat{\mathbf{x}}_0$ → **推断精炼**对预测运动进行根轨迹校正和姿态强制替换，输出最终运动 $\bar{\mathbf{x}}_0$。

这种“训练时多层软引导 + 推断时硬约束精炼”的设计，是本方法在关键帧误差上实现 0.000 cm（Table 1）的根本原因，同时也保证了语义一致性指标（R-Precision Top 3 达 0.803）处于最优水平。



本方法的核心是一个**多层级扩散框架**，其设计围绕一个瓶颈：如何将文本高层语义与关键帧的精确时空约束有效对齐。框架通过四个协同模块实现这一目标：条件编码、局部引导、全局引导和推断精炼。

### 条件编码

文本提示通过 CLIP 和转换器编码为固定长度的文本特征。关键帧约束以稀疏特征矩阵 $\mathbf{K} \in \mathbb{R}^{\bar{\mathcal{N}} \times D}$ 表示，其中未约束条目置零，并配以二值掩码 $\mathbf{m}_{\mathbf{K}} \in \{0,1\}^{N \times D}$ 标识哪些帧的哪些关节维度受到约束。关键帧特征与掩码拼接后经 MLP 获得关键帧嵌入 $\mathbf{e}_k$，为后续引导提供结构化的条件信号。

### 局部引导

局部引导的因果机制在于**利用单个关键帧细化其周围的局部过渡**。在 U-Net 的每个时间步，当前帧的含噪运动特征 $\mathbf{x}_t$ 经 MLP 投影后，与对应帧的关键帧嵌入 $\mathbf{e}_k$ 沿特征维度拼接。这一融合操作使卷积层能够自适应地调制关键帧邻近帧的运动模式，促进生成过渡与关键帧姿态之间的精确空间对齐，从而抑制关键帧附近的姿态偏差。

### 全局引导

全局引导解决的是**关键帧序列隐含的语义结构如何与文本语义协同调节整体动态**。其核心是**关键帧变换器编码器**：将关键帧嵌入 $\mathbf{e}_k$ 与一个可学习的紧凑令牌拼接，加入位置编码以指示时序顺序，经掩码过滤后送入变换器。变换器输出的紧凑令牌特征捕获了关键帧序列的全局时空模式。该特征随后与文本特征沿令牌维度拼接，通过交叉注意力注入 U-Net，从而在全局层面协调运动动态与文本语义及关键帧时序结构的一致性。

### 推断精炼

推断精炼是**实现硬约束的关键**，分为轨迹精炼和姿态填补两步，仅在扩散去噪的最后阶段执行。

**轨迹精炼**的目标是消除生成运动在关键帧处的根位置偏差，同时避免脚步滑动伪影。其因果逻辑是：按各帧根速度的比例分配位置误差，而非均匀分配。

给定预测运动 $\hat{\mathbf{x}}_0$，在第 $i$ 个关键帧 $n_i$ 处的根位置误差为：

$$\Delta \mathbf{r} = \mathrm{R}(\mathbf{K}_i) - \mathrm{R}(\hat{\mathbf{x}}_0^{n_i}) \tag{1}$$

其中 $\mathrm{R}(\cdot)$ 提取根关节位置。对于关键帧区间 $(n_{i-1}, n_i)$ 内的每一帧 $n$ 和每个空间维度 $d \in \{x,y,z\}$，校正权重由该帧根速度的绝对值占比决定：

$$w_{n,d} = \frac{|\hat{\mathbf{v}}_{n,d}|}{\sum_{s=n_{i-1}}^{n_i-1} |\hat{\mathbf{v}}_{s,d}|} \tag{2}$$

调整后的速度为：

$$\tilde{\mathbf{v}}_{n,d} = \hat{\mathbf{v}}_{n,d} + w_{n,d} \cdot \Delta \mathbf{r}_d \tag{3}$$

精炼后的根轨迹从上一个关键帧位置开始累计调整后的速度：

$$\tilde{\mathbf{r}}_n = \mathrm{R}(\mathbf{K}_{i-1}) + \sum_{s=n_{i-1}}^{n-1} \tilde{\mathbf{v}}_s \tag{4}$$

最终用精炼根位置替换预测运动中的根：

$$\tilde{\mathbf{x}}_0^n = \mathrm{ReplaceRoot}(\hat{\mathbf{x}}_0^n, \tilde{\mathbf{r}}_n) \tag{5}$$

**姿态精炼**在轨迹精炼之后，通过扩散填补强制满足关键帧的姿态约束。将用户指定的关键帧特征矩阵按掩码直接替换到预测运动中：

$$\bar{\mathbf{x}}_0 = \mathbf{K} \odot \mathbf{m}_{\mathbf{K}} + \tilde{\mathbf{x}}_0 \odot (1 - \mathbf{m}_{\mathbf{K}}) \tag{6}$$

这一操作确保关键帧处的所有受约束关节特征严格等于指定值，从而实现零关键帧误差。

### 关键公式总结

| 公式 | 变量含义 | 功能 |
|------|----------|------|
| $\Delta \mathbf{r}$ | 关键帧根位置误差 | 量化生成与目标之间的空间偏差 |
| $w_{n,d}$ | 按根速度比例分配的校正权重 | 将误差按运动活跃度分配，避免滑动 |
| $\tilde{\mathbf{v}}_{n,d}$ | 调整后的根速度 | 施加加权校正 |
| $\tilde{\mathbf{r}}_n$ | 精炼后的根轨迹 | 从关键帧开始累计调整速度，重构轨迹 |
| $\bar{\mathbf{x}}_0$ | 姿态精炼后的运动 | 用关键帧特征强制替换受约束部分 |

消融实验证实了这一设计的有效性：仅使用局部+全局引导时，关键帧误差为 0.667 cm 且根位置误差非零；加入轨迹精炼后根误差消除至 0.000，但姿态误差仍存；最终加入姿态精炼后，关键帧误差和所有子指标均降至 0.000（Table 4）。定性对比进一步表明，均匀分配根误差会产生滑动伪影，而本方法的比例分配策略在保证空间精度的同时保持了自然的脚部接触模式（Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/001_Figure_1.jpg]]
*Figure 1: Our method enables motion generation (a) and editing (b) interactively with precise spatio-temporal control. (a) Text-conditioned Motion In-betweening: Given textual descriptions, keyframes (orange), and sparse keyjoint signals (orange spheres), our method can generate motions (blue) that strictly satisfy the spatio-temporal constraints and align well with textual semantics. (b) Semantics-preserving Motion Editing: Given the source motion generated from (a) and a keyframe (orange) specifying the local modifications (e.g., placing the character on the ground and lowering the hands in the last frame), our method produces coherent edited motions, comprising modified segments (pink) that satisf...*

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our text-conditioned motion in-betweening method. Given a text prompt, a set of keyframes, and a keyframe mask, our model generates a motion sequence that aligns with spatio-temporal constraints and motion semantics derived from text and keyframes. The framework consists of four components: (a) Condition Encoding encodes text and keyframe inputs; (b) Local Guidance incorporates keyframe embedding with noisy motion feature to guide local transitions around keyframes; (c) Global Guidance integrates text and keyframe features to modulate global motion dynamics; and (d) Inference Refinement enforces precise spatial adherence through trajectory and pose refinement. Here, (cf) and (ct...*

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/004_Figure_4.jpg]]
*Figure 4: Keyframe Transformer Encoder. This module concatenates the keyframe embeddings $\mathbf { e } _ { k }$ with a learnable token and adds positional encoding (PE) to indicate temporal order. The keyframe mask mK is applied to filter out masked embeddings, and the resulting sequence is subsequently processed by the Transformer. The output corresponding to the learnable token serves as the compact keyframe feature for global guidance*

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results of text-conditioned motion in-betweening. We visualize the keyframe constraints as orange frames, the corresponding generated keyframes in pink, and the generated transitions as blue frames. Our method strictly adheres to the constraints, exhibiting perfect overlap between the targets (orange) and generations (pink), whereas other methods display non-negligible spatial deviations (orange boxes) and semantic inconsistencies (blue boxes). Please refer to the supplementary video for the complete motion sequences*



## 实验与关键发现

### 关键帧插补主实验

在 HumanML3D 测试集上，本方法在关键帧插补任务中实现了全面的最优性能。Table 1 报告了使用 7 个关键帧（首尾帧 + 5 个随机中间帧）的定量结果：本方法的关键帧误差（Keyframe Error）为 **0.000 cm**，严格满足所有空间约束，而其他方法均存在不可忽略的空间偏差。在语义对齐方面，本方法的 R-Precision (Top 3) 达到 **0.803**，优于次优方法的 ≤0.797；FID 降至 **0.023**，低于次优方法的约 0.028。这组结果表明，多层级引导机制在实现零误差关键帧遵循的同时，有效保持了生成运动的语义一致性和整体质量。

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of keyframe in-betweening on HumanML3D test set. We select the first and last frames along with five randomly sampled intermediate frames from the ground truth motions as keyframe constraints. Bold denotes the best results*

定性结果（Figure 5）进一步验证了这一优势：本方法生成的关键帧（粉色）与目标约束（橙色）完美重叠，而其他方法在约束帧处存在明显的空间偏差（橙色框标注），且在过渡段出现语义不一致（蓝色框标注）。

### 稀疏度鲁棒性

Table 2 考察了不同关键帧稀疏度（K = 0, 5, 10, 20）下的方法鲁棒性。本方法在所有稀疏度设置下均保持最强的语义对齐能力——即使在极端稀疏条件 K=0 时，R-Precision (Top 3) 仍达 0.796。随着关键帧数量增加，本方法的语义指标和关键帧遵循度保持稳定，而其他方法在稀疏度变化时性能波动较大。这归因于全局引导模块通过关键帧变换器编码器有效捕获了关键帧序列的时空结构，即使在稀疏约束下也能提供可靠的全局动态调节信号。

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/008_Table_2.jpg]]
*Table 2: Robustness evaluation under varying keyframe sparsity on the HumanML3D test set. K = {0, 5, 10, 20} denotes the number of randomly selected intermediate keyframes, excluding the first and last frames*

### 部分关节控制

Table 3 展示了仅约束根关节和末端效应器（头、手、脚）的部分关节控制实验。在 5 个随机帧上约束根关节与随机子集的末端效应器时，本方法的关键帧误差仍为 **0.000 cm**，R-Precision (Top 3) 达到 **0.813**，优于次优方法的约 0.805。这表明局部引导模块能够针对单个关键帧的稀疏关节约束进行精细的局部过渡调制，而全局引导模块则从稀疏关节序列中提取足够的语义线索以维持整体动态一致性。

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison of partial joint control on HumanML3D test set. Constraints consist of the root joint and a random subset of the five end-effectors (head, hands, feet) at five randomly sampled frames*

### 消融实验

Table 4 系统性地量化了各组件的独立贡献，揭示了多层级引导与推断精炼的因果作用链：

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/009_Table_4.jpg]]
*Table 4: Ablation study on the HumanML3D test set. KPE calculates the joint error after aligning to the root coordinate. KRE calculates the root position error in world space. ✓ denotes that the component is enabled in the configuration. We select the first and last frames along with five randomly sampled intermediate frames as keyframe constraints*

**引导机制的贡献。** 移除局部引导后，模型仅依赖全局引导，关键帧误差飙升至 3.2 cm，R-Precision 降至 0.78，表明局部引导对于关键帧周围的精确空间对齐不可或缺。移除全局引导后，语义一致性指标（MM Dist、R-Precision）显著恶化，说明仅靠局部引导无法有效整合文本语义与关键帧序列的全局动态线索。两个引导模块共同作用（LocG+GloG）时，关键帧误差降至 0.667 cm，语义指标恢复至接近完整模型的水平。

**推断精炼的贡献。** 在 LocG+GloG 基础上引入轨迹精炼（TraR），根位置误差（KRE）从非零值降至 **0.000**，但关键帧姿态误差（KPE）仍为 0.667 cm。进一步加入姿态精炼后，KPE 和 Keyframe Error 均降至 **0.000**，实现了对关键帧的完全硬约束满足。这一消融链条验证了推断精炼策略的必要性：轨迹精炼解决根位置偏移，姿态填补解决局部姿态偏差，二者互补才能实现零误差的关键帧遵循。

**轨迹精炼策略的定性消融。** Figure 6 通过具体案例对比了不同轨迹修正策略的效果。无任何精炼时，生成关键帧明显偏离约束；仅使用扩散填补而不进行轨迹精炼，关键帧周围出现抖动伪影；均匀分配根位置误差会产生明显的脚步滑动；而本方法的基于速度比例分配策略在保证根轨迹与关键帧对齐的同时，最大限度地保持了自然的脚部接触模式，避免了滑动伪影。

### 运动编辑实验

Table 5 评估了基于关键帧的运动编辑性能，包括局部姿态编辑和全局轨迹编辑，修改 1–5 个随机关键帧。本方法在空间精度（关键帧误差）、运动质量（FID）和语义保持度（SS Similarity）上均优于基于优化的 DNO 方法。这得益于 DDIM 反演与固定点迭代策略：反演将原始运动映射到扩散模型的隐空间，编辑后的关键帧通过推断精炼强制满足新约束，而未修改段落的语义得以完整保留。

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/010_Table_5.jpg]]
*Table 5: Quantitative evaluation on the keyframe-based motion editing with 1–5 randomly selected keyframe modifications, evaluated on local pose and global trajectory editing*

### 失败模式与局限

尽管本方法在定量指标上表现出色，但仍存在以下局限：

1. **语义-约束冲突**：当文本语义与关键帧约束存在严重冲突时（例如文本描述“跳跃”但关键帧指定蹲姿），模型可能难以生成令人满意的过渡。此时需要用户手动调整条件以消除歧义。
2. **推断效率**：推断精炼过程（特别是运动编辑中的 DDIM 反演和固定点迭代）增加了生成时间，可能不适用于实时交互场景。
3. **数据域泛化**：当前模型仅在 HumanML3D 数据集上验证，其在其他运动风格（如舞蹈、杂技）或高度动态动作上的泛化能力尚未证明，需要进一步评估。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/011_Figure_6.jpg]]
*Figure 6: Ablation results on trajectory refinement. Without refinement, the generated keyframes deviate from the keyframe constraints; imputation alone introduces jitters between transitions (blue) and generated keyframes (pink); and uniformly distributing the root position error across frames leads to drifting artifacts. In contrast, our trajectory refinement aligns the root trajectory with the keyframe constraints while minimizing foot skating artifacts*

![[assets/figures/papers/paper_list_l2_https_cvpr_thecvf_com_virtual_2026_poster_38659/figures/002_Figure_2.jpg]]
*Figure 2: Limitations of previous text-conditioned motion inbetweening methods. The artist specifies the intended motion semantics through text and keyframes (orange), with keyframes 2–4 (from right) indicating three distinct stages: “picking up”, “carrying overhead”, and “walking to the target”. However, existing approaches [9] exhibit two critical limitations: (a) Lacking lowlevel semantic control, as the generated transition (blue) redundantly performs the “picking up” action after the timing set by the keyframe, and fails to maintain the keyframe-specified “carrying overhead” pose while walking. (b) Lacking precise keyframe adherence, demonstrated by the generated motion at the constrained frame...*



## 定位与知识库关联

### 核心瓶颈与因果机制

现有文本条件运动插补方法面临一个根本性瓶颈：**文本语义与关键帧时空约束的有效对齐**。如 Figure 2 所示，先前方法存在双重缺陷——一方面缺乏低层语义控制，生成的过渡动作在关键帧指定时机之后仍冗余执行已完成的动作，且无法维持关键帧指定的姿态；另一方面缺乏精确的关键帧遵循，约束帧上的生成结果与目标存在显著空间偏差。这一瓶颈的根源在于，文本条件仅作为全局语义信号，而关键帧约束仅作为软条件（通过条件特征提供），两者在生成过程中缺乏结构化的协同机制，导致语义准确性与空间精确性难以兼得。

本工作通过一个**多层级扩散框架**解耦并协同这两类控制信号，其因果调节旋钮包含两个层面：
1. **训练阶段的局部-全局引导机制**：局部引导利用单个关键帧的嵌入与含噪运动特征融合，通过 U-Net 卷积操作自适应调制关键帧周围的局部过渡，促进精确空间对齐；全局引导则通过关键帧变换器编码器提取关键帧序列的时空模式，与文本特征融合后经交叉注意力注入 U-Net，以调节整体运动动态。这一设计将文本高层语义与关键帧底层时空线索深度融合，解决了语义与约束分离的问题。
2. **推断阶段的轨迹-姿态精炼策略**：轨迹精炼按根速度比例自回归地分配位置误差，仅在最后去噪步骤执行，避免均匀误差分配导致的脚步滑动伪影；姿态精炼通过扩散填补将关键帧指定值强制替换到生成运动中，实现硬约束满足。这一策略将关键帧遵循从“软条件”提升为“硬约束”。

核心洞察在于：**分离全局语义控制与局部关键帧对齐，并利用基于速度比例的轨迹精炼在推理时实现硬约束**，从而生成既严格遵循关键帧又忠实表达语义的运动。

### 与基线方法的关系

本工作在文本条件运动生成与时空控制两个维度上与多条基线形成对比，其改进可通过以下“变化槽位”精确刻画：

| 变化槽位 | 基线方法及其取值 | 本方法取值 | 证据锚点 |
|---------|----------------|-----------|---------|
| **关键帧约束执行机制** | **Flexible Motion In-betweening** (Cohan et al., SIGGRAPH 2024)、**MaskControl** (Pinyoanuntapong et al., ICCV 2025) 等将关键帧作为软条件，无法保证精确遵循 | 多层级引导（局部+全局）施加结构化约束，推断时轨迹精炼与姿态填补实现硬约束，Keyframe Error = 0.000 | Table 1, Sec. 3.1-3.2 |
| **全局语义与关键帧时序整合** | **MDM** (Tevet et al., ICLR 2023)、**OmniControl** (Xie et al., ICLR 2024) 仅将文本作为全局条件，忽略关键帧序列隐含的语义结构 | 关键帧变换器编码器提取关键帧序列时空模式，与文本特征融合后经交叉注意力调节全局动态 | Sec. 3.1 (Global Guidance), Fig. 4 |
| **推理阶段轨迹误差修正** | 先前方法无修正或采用均匀误差分配，导致脚步滑动和动态不自然 | 按根速度比例自回归分配位置误差，仅在最后去噪步骤执行，保留自然接触模式 | Sec. 3.2 (Trajectory refinement), Eq. 2-4, Figure 6 |

在 **HumanML3D 关键帧插补**（7个关键帧）基准上，本方法实现了 **Keyframe Error = 0.000**，严格满足所有空间约束，而其他方法均存在不可忽略的偏差（Table 1）。同时，语义一致性指标 **R-Precision (Top 3) = 0.803**，优于次优方法（≤ 0.797）；**FID = 0.023**，低于次优方法（≈ 0.028）。在部分关节控制场景（仅约束根与末端效应器）下，本方法同样保持零关键帧误差，且 R-Precision 提升至 0.813（Table 3），表明多层级引导机制在不同约束粒度下均有效。

消融实验（Table 4）进一步揭示了各组件的因果贡献：移除局部引导或全局引导均显著降低语义一致性（仅全局引导时 R-Precision 降至 0.78）并增大关键帧误差（Keyframe Error 高达 3.2 cm）；引入轨迹精炼（LocG+GloG+TraR）可将根位置误差（KRE）消除至 0.000，但关键帧姿态误差（KPE）仍为 0.667；进一步加入姿态精炼后，KPE 和 Keyframe Error 均降至 0.000。Figure 6 的定性对比表明，仅使用扩散填补而不进行轨迹精炼会导致关键帧周围出现抖动，均匀分配根位置误差会产生滑动伪影，而本方法的比例分配策略在保证空间精度的同时保持了自然的脚部接触。

### 适用边界与局限

本方法在以下条件下表现出色，但也存在明确的适用边界：

1. **语义-约束冲突场景**：当文本语义与关键帧约束存在严重冲突时（如文本要求“跳跃”而关键帧指定蹲姿），模型可能难以生成令人满意的过渡。此时需要用户手动调整条件以消除歧义，方法本身缺乏自动检测与调解冲突的机制。

2. **推理效率**：推断精炼过程（特别是运动编辑中的 DDIM 反演与固定点迭代）增加了生成时间，可能不适用于实时交互场景。论文未报告具体推理延迟数据，该点需手动验证。

3. **数据分布泛化**：当前模型仅在 HumanML3D 数据集上验证，该数据集以日常人体动作为主。其泛化到其他风格（如舞蹈、武术）或高度动态动作（如杂技、翻滚）的能力尚未证明。

4. **物理合理性**：虽然轨迹精炼有效避免了脚步滑动，但方法未显式引入物理约束（如接触力、动力学方程），在极端姿态或快速转向场景下可能产生物理上不可行的运动。

### 开放问题

1. **冲突自动调解**：如何自动检测并调解文本高层语义与关键帧低级约束之间的冲突？可能的路径包括引入约束优先级机制、基于置信度的条件加权，或通过交互式反馈让模型主动提示用户存在冲突。

2. **物理模拟集成**：多层级扩散框架是否可以扩展到包含物理模拟或其他显式约束（如接触约束、力矩平衡），以进一步提高运动的物理合理性？这可能需要将物理损失作为扩散引导项或后处理优化步骤。

3. **多人交互与物体操作**：在更复杂的多人交互或物体操作场景中，本方法的严格关键帧遵循策略是否依然适用？多人场景涉及角色间相对约束，物体操作涉及手-物接触约束，这些对轨迹精炼和姿态填补提出了新的挑战。

4. **实时性能优化**：能否通过蒸馏、一步生成或缓存策略将推断精炼过程加速至实时，以支持交互式创作工具？这需要在精度与速度之间寻找新的平衡点。



## 原文 PDF

![[paperPDFs/CVPR_2026/Unifying_Precise_Keyframes_and_Semantic_Control_via_Multi_level_Diffusion.pdf]]

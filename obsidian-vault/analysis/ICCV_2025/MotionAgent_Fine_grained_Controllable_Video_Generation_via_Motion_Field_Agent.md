---
title: "MotionAgent: Fine-grained Controllable Video Generation via Motion Field Agent"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field_Agent.pdf
project_link: null
code_link: https://github.com/leoisufa/MotionAgent
aliases:
- MotionAgent
tags:
- ICCV_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "采用运动场智能体（Motion Field Agent）将文本中的运动描述显式转化为中间表示（物体轨迹和相机外参），并通过3D空间分析光流组合为统一光流，进而用光流适配器控制扩散模型，实现了从文本到细粒度运动的解藕与精确映射。"
primary_logic: "将视频运动解耦为物体运动和相机运动，利用LLM将自然语言转换为可解释的显式运动参数，再通过几何投影组合为统一的光流控制信号，使得无需专门训练数据即可实现文本驱动的精准运动生成。"
claims:
- "在VBench基准上，Video-Text Camera Motion指标达到81.91%，远超其他方法（次优DynamiCrafter为35.81%），证明相机运动控制极为精准。"
- "在自建的细粒度运动控制基准上，Object Movement Q&A得分45.69%，Complex Camera Motion得分77.76%，均以显著优势超过所有对比方法。"
- "用户研究表明，所生成视频在视觉质量和运动语义对齐两个维度均排名第一。"
- "消融实验证实，分析光流组合模块和光流适配器微调是运动控制精度大幅提升的关键所在，移除后指标急剧下降。"
---

# MotionAgent: Fine-grained Controllable Video Generation via Motion Field Agent

> [!tip] 核心洞察
> 将视频运动解耦为物体运动和相机运动，利用LLM将自然语言转换为可解释的显式运动参数，再通过几何投影组合为统一的光流控制信号，使得无需专门训练数据即可实现文本驱动的精准运动生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionAgent：基于运动场智能体的细粒度可控视频生成 |
| 英文题名 | MotionAgent: Fine-grained Controllable Video Generation via Motion Field Agent |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2502.03207) · [GitHub](https://github.com/leoisufa/MotionAgent) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MotionAgent |
| Dataset | VBench, 自建运动控制基准（VBench子集）, 用户调研 |

> [!tip] 效果简介
> - VBench 上，Video-Text Camera Motion 为 81.91%，对比 35.81% (DynamiCrafter, 次优)，变化 +46.10%。
> - 自建运动控制基准（VBench子集） 上，Object Movement Q&A 为 45.69%，对比 30.96% (Pyramid Flow, 次优)，变化 +14.73%。
> - 自建运动控制基准（VBench子集） 上，Complex Camera Motion 为 77.76%，对比 20.62% (CogVideoX, 次优)，变化 +57.14%。

## 概要

现有图像到视频（I2V）生成方法在运动控制上面临一个根本性瓶颈：文本编码器无法将自然语言中的运动描述精确映射为像素级的运动信号，而专用控制模块又依赖轨迹、相机外参等专业输入，且大多无法同时控制物体运动与相机运动。**MotionAgent** 针对这一问题，提出以**运动场智能体（Motion Field Agent）** 为核心，将文本中的运动信息显式转化为可解释的中间表示——物体轨迹与相机外参，再通过几何投影将其组合为统一的光流控制信号，从而在不依赖专门训练数据的前提下，实现文本驱动的细粒度运动生成。

该方法的因果机制可概括为“解耦—转化—组合—控制”四步：首先将视频运动场解耦为物体运动与相机运动；然后利用大语言模型将文本描述转化为结构化的物体轨迹和相机外参；接着通过**分析光流组合模块**在三维空间中整合两类运动，投影为统一的二维光流图；最后由**光流适配器**将该光流注入冻结的预训练扩散模型（Stable Video Diffusion），生成精确受控的视频帧。

实验证据充分支撑了上述设计。在 VBench 基准上，MotionAgent 的 Video-Text Camera Motion 指标达到 **81.91%**，远超次优方法 DynamiCrafter 的 35.81%（Table 1）。在自建的细粒度运动控制基准上，Object Movement Q&A 得分 **45.69%**（次优 Pyramid Flow 为 30.96%），Complex Camera Motion 得分 **77.76%**（次优 CogVideoX 为 20.62%），均以显著优势领先（Table 2）。用户研究进一步表明，该方法在视觉质量和运动语义对齐两个维度均排名第一（Figure 6）。消融实验证实，分析光流组合模块和光流适配器微调是运动控制精度大幅提升的关键所在，移除后指标急剧下降（Table 3）；而可选的**重思考（Rethinking）机制**能纠正初始阶段的相机运动误差，将复杂相机运动指标进一步提升至 89.04%（Table 2, Table 6）。

在方法谱系上，MotionAgent 区别于传统的文本编码器控制范式（如 DynamiCrafter、CogVideoX）和专用模块控制范式（如 Motion-I2V），开创性地将大语言模型作为运动信息解析器，以显式光流作为统一的中间控制表示，实现了对物体和相机运动的同步、精确控制。其局限性主要在于：动态度指标偏低（因未提及的物体被有意保持静止以实现精确控制）、依赖 GPT-4o 等大模型的推理能力、以及需要额外微调光流适配器来弥合域差异。

图像到视频（I2V）生成旨在根据单张静态图像和文本描述生成一段动态视频，其核心挑战在于如何精确地控制视频中的运动。现有I2V方法大致可分为两类：一类将运动控制完全交由文本编码器处理，通过文本嵌入隐式地驱动视频生成；另一类则引入专用控制模块，依赖用户手动提供轨迹、相机外参等专业输入来实现运动引导。

然而，这两条技术路线均存在根本性瓶颈。文本编码器方式虽然使用便捷，但文本嵌入对运动的表征能力有限，难以实现对画面中每个元素的细粒度控制——例如，无法精确指定“画面左侧的红色气球向上移动，同时右侧的蓝色气球向下移动”这类多物体差异化运动。专用控制模块方式虽然能提供更精确的运动引导，但要求用户具备专业知识并手动绘制轨迹或设定相机参数，使用门槛极高；更重要的是，现有方法大多无法同时控制物体运动和相机运动，难以满足真实场景中“物体移动且镜头跟随”的复合控制需求。

上述瓶颈的根源在于，运动信息在文本与控制信号之间缺乏一种显式、可解释且统一的中间表示。文本描述是抽象的、语义层面的，而视频生成模型所需的控制信号是像素级的、几何层面的，两者之间存在巨大的语义鸿沟。如何将自然语言中的运动描述自动、精确地转化为可作用于扩散模型的控制信号，是I2V领域尚未被充分解决的关键问题。

针对这一缺口，本文提出MotionAgent，核心思路是引入**运动场智能体（Motion Field Agent）** 作为文本与视频生成之间的桥梁。该智能体将视频运动解耦为物体运动和相机运动两个分量，利用大语言模型（LLM）将文本中的运动描述显式转化为物体轨迹和相机外参这两种可解释的中间表示；随后通过分析光流组合模块在3D空间中将二者整合为统一光流图，作为扩散模型的控制条件。这一设计使得用户仅需自然语言即可实现对物体运动和相机运动的同步、细粒度控制，无需任何专业输入，且无需针对特定控制信号训练专用生成模型。

## 核心方法与创新机理

MotionAgent 的核心创新在于将视频运动控制从“黑箱文本嵌入”或“手工专业输入”的范式，迁移到一个**文本→显式运动参数→统一光流→扩散模型**的级联解耦框架。其关键改变体现在以下三个层面：

### 1. 运动信息提取：从隐式编码到显式参数化

现有 I2V 方法（如 **DynamiCrafter** (Xing et al., arXiv 2023)、**CogVideoX** (Yang et al., arXiv 2024)）依赖文本编码器直接提取运动语义，无法对单个物体的运动轨迹或相机运动幅度进行精细调控；而专用控制模块方法（如 **Motion-I2V** (Shi et al., arXiv 2024)）虽能接受轨迹或外参，却要求用户手动提供这些专业输入。

MotionAgent 引入**运动场智能体（Motion Field Agent）**，利用大语言模型将自然语言中的运动描述自动解析为两组显式中间表示：
- **物体轨迹**：通过网格选择（grid selection）方式绘制物体在画面中的运动路径；
- **相机外参**：直接生成相机旋转与平移参数，其中平移 $T$ 被约束在 $(-1, 1)$ 区间，后续根据深度图重缩放至合理范围。

这一改变将运动控制从“文本嵌入的隐式空间”拉到了“可解释的几何参数空间”，使非专业用户也能通过自然语言实现细粒度运动指定。

### 2. 运动表示组合：从简单叠加到 3D 空间分析光流组合

当同时存在物体运动和相机运动时，简单地将二者对应的光流直接相加会产生不合理的运动区域（如物体边界处的伪影）。MotionAgent 提出**分析光流组合模块（Analytical Optical Flow Composition）**，在 3D 空间中对两种运动进行统一建模：

- 首先根据物体轨迹移动对应像素的 3D 位置 $P^0$ 得到 $P^1$；
- 再利用相机外参 $E$ 将其重投影到图像坐标系：$I^{1} = \Pi ( E P^{1} )$；
- 最终统一光流由像素偏移量给出：$F = I^{1} - I^{0}$。

这一设计从几何层面保证了物体运动和相机运动在 2D 光流中的一致性，是实现二者同步精确控制的关键机制。

### 3. 控制信号注入：从文本条件到统一光流适配器

基础 I2V 扩散模型（如 **SVD** (Blattmann et al., arXiv 2023)）原生接受文本或图像条件，无法直接理解光流信号。MotionAgent 训练了一个**光流适配器（Optical Flow Adapter）**，将前述模块生成的统一光流图作为控制条件注入冻结的扩散模型。

值得注意的是，适配器并非仅在真实光流数据上训练，而是专门在**统一光流图**上进行微调。这一步骤弥合了“合成光流”与“真实光流”之间的域差异——消融实验表明，若跳过此微调，复杂相机运动指标将从 77.76% 骤降至 48.27%，证明其不可或缺。

### 4. 闭环修正：重思考机制

MotionAgent 还引入了一个可选的**重思考（Rethinking）机制**：智能体在生成视频后，根据结果评估运动执行质量，并自动修正之前的轨迹或外参。这一闭环设计使模型具备了自我纠错能力——在 VBench 上，重思考将 Video-Text Camera Motion 从 81.91% 进一步提升至 87.02%，复杂相机运动从 77.76% 提升至 89.04%。

![[assets/figures/papers/paper_list_l21_MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field/figures/001_Figure_1.jpg]]
*Figure 1: Different frameworks of I2V generation models. (a) Controllable I2V generation via text encoder. (b) Controllable I2V generation via special control module. (c) Our method, controllable I2V generation via motion field agent*

MotionAgent 的整体流水线由三个核心阶段构成：**运动场智能体（Motion Field Agent）** 将文本运动描述显式转换为中间运动表示；**分析光流组合模块（Analytical Optical Flow Composition）** 在3D空间整合物体与相机运动，生成统一光流图；**光流适配器（Optical Flow Adapter）** 将该光流作为控制条件注入冻结的基础扩散模型，驱动视频生成。图2和图3分别展示了智能体与生成模型的完整架构。

### 运动场智能体

智能体接收自然语言文本作为唯一输入，首先将运动信息分解为**物体运动**和**相机运动**两个独立部分（Step 1）。对于物体运动，智能体采用网格选择方式绘制物体轨迹，将图像划分为若干方形子区域并标记整数索引，以此指定物体的起始与终止位置（Step 2）；对于相机运动，智能体直接生成相机外参，其中平移分量 $T$ 被约束在 $(-1, 1)$ 区间，后续由光流组合模块根据深度图将其恢复至合理范围（Step 3）。可选的重思考（Rethinking）步骤允许智能体根据已生成视频对先前动作进行修正（Step 4）。物体识别可借助 Grounded-SAM 等辅助检测工具提升定位精度，也可通过多轮对话实现无检测方案。

### 分析光流组合模块

该模块将智能体输出的物体轨迹和相机外参在3D空间统一整合。给定初始帧像素位置 $I^0$ 及其估计深度，模块首先将像素反投影到3D世界坐标系，施加物体运动偏移得到新3D位置 $P^1$，再通过相机外参 $E$ 和投影操作 $\Pi$ 将其重投影到图像坐标系：

$$I^{1} = \Pi ( E P^{1} )$$

统一光流 $F$ 即为后续帧与初始帧像素位置的偏移量：

$$F = I^{1} - I^{0}$$

这一分析组合方式避免了直接相加物体光流与相机光流所带来的不合理区域，实现了两类运动的同步精确控制。

### 光流适配器与基础扩散模型

统一光流图作为控制条件输入光流适配器。适配器在合成光流上进行了微调，以弥合统一光流与真实光流之间的域差异——训练数据通过 Unimatch 估计真实光流、DROID-SLAM 计算相机外参，并分离出物体运动光流 $\hat{F}_{obj}$ 作为伪标签。基础扩散模型采用冻结的 Stable Video Diffusion（SVD），适配器的控制信号注入其中，最终生成精确受控的视频帧序列。

### 运动场智能体（Motion Field Agent）

MotionAgent 的核心创新在于将视频的运动场显式解耦为**物体运动**和**相机运动**两部分，并通过运动场智能体将自然语言中的运动描述转化为可执行的中间表示。该智能体的工作流程分为四个步骤：

1. **文本解析**：智能体首先解析输入文本，将运动信息分解为描述物体运动和相机运动的两个独立部分。
2. **物体轨迹绘制**：根据物体运动描述，智能体在图像平面上绘制物体的运动轨迹。轨迹绘制采用**网格选择（Grid Selection）**方式——将图像划分为若干方形子区域，每个区域以左上角整数标记，并进一步细分为九宫格子区域（见 Figure 8），从而以离散化方式精确定位物体位置，避免直接生成连续坐标带来的歧义。
3. **相机外参生成**：智能体根据相机运动文本直接生成相机外参。其中平移分量 $T$ 被约束在 $(-1, 1)$ 范围内，后续在光流组合模块中根据估计的深度图将其缩放至合理尺度。
4. **重思考（Rethinking）**（可选）：智能体根据生成视频的结果，对先前的轨迹和外参进行修正，形成闭环反馈。

### 分析光流组合模块（Analytical Optical Flow Composition）

该模块负责将物体轨迹和相机外参在 3D 空间中整合为统一的 2D 光流图，这是实现物体与相机运动同步控制的关键。

核心计算流程如下：

首先，利用深度估计模型获取初始帧的深度图，将像素坐标反投影到 3D 空间。对于物体运动，根据轨迹更新对应物体的 3D 位置；对于相机运动，将相机外参 $E$ 作用于所有 3D 点。最终通过重投影方程获得后续帧的像素坐标：

$$I^{1} = \Pi ( E P^{1} )$$

其中 $P^{1}$ 为移动后的 3D 点，$\Pi$ 为投影操作，$E$ 为相机外参，$I^{1}$ 为后续帧对应的像素位置。

统一光流 $F$ 定义为后续帧与初始帧像素位置的偏移量：

$$F = I^{1} - I^{0}$$

该光流同时编码了物体运动和相机运动的信息，作为后续扩散模型的控制信号。

### 光流适配器（Optical Flow Adapter）

统一光流图需注入基础扩散模型以实现运动控制。由于统一光流与真实光流之间存在域差异，MotionAgent 在统一光流图上对光流适配器进行微调，使其能够有效弥合这一差距。

适配器的训练数据准备过程如下：利用光流估计模型 **Unimatch** 估计真实光流 $\hat{F}$，并利用 SLAM 方法 **DROID-SLAM** 计算相机外参 $\hat{E}$。后续帧像素位置可由真实光流获得：

$$I^{1} = I^{0} + \hat{F}$$

为分离出物体运动光流，将 $I^{1}$ 根据逆相机外参和深度重投影回第一帧坐标系：

$$I_{obj}^{1} = \Pi ( \hat{E}^{-1} \Pi^{-1} ( I^{1} ) )$$

进而得到仅由物体运动引起的光流伪标签：

$$\hat{F}_{obj} = I_{obj}^{1} - I^{0}$$

这些伪标签用于训练适配器，使其学会从统一光流映射到真实光流分布。

### 基础扩散模型

MotionAgent 采用冻结的预训练 **Stable Video Diffusion（SVD）** 作为基础图像到视频扩散模型。光流适配器接收统一光流图作为控制条件，将其注入扩散模型的去噪过程，最终生成精确受控的视频帧序列。

## 实验与关键发现

### 核心实验结果

MotionAgent 在通用视频生成质量和细粒度运动控制两个维度上均展现出显著优势，尤其在相机运动控制方面实现了对现有方法的断层式领先。

**通用 I2V 生成质量（VBench）。** 在 VBench 基准上，MotionAgent 在 Video-Text Camera Motion 指标上达到 **81.91%**，远超次优方法 DynamiCrafter 的 35.81%，提升幅度高达 **+46.10%**（Table 1）。同时，该方法在 Motion Smoothness（98.93%）和 Aesthetic Quality 等指标上也保持领先，说明精细的运动控制并未牺牲生成视频的视觉质量。值得注意的是，MotionAgent 的 Dynamic Degree 指标相对较低，这并非生成能力不足，而是因为模型仅让文本中明确提及的物体发生运动，未提及的物体保持静止，从而实现了更精确的控制（Figure 10）。

![[assets/figures/papers/paper_list_l21_MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field/figures/004_Table_1.jpg]]
*Table 1: Evaluation results of general I2V generation on VBench [26] (all values are in percentage). The best result is indicated in bold, the second-best result is indicated with underlines, and the third-best result is indicated with double underlines*

**细粒度运动控制基准。** 为评估对物体运动和相机运动的精确控制能力，作者构建了基于 VBench 子集的细粒度运动控制基准。结果如 Table 2 所示：
- **物体运动控制**：Object Movement Q&A 得分 **45.69%**，显著高于次优方法 Pyramid Flow 的 30.96%（+14.73%）。
- **复杂相机运动控制**：Complex Camera Motion 得分 **77.76%**，而次优方法 CogVideoX 仅为 20.62%，领先幅度高达 **+57.14%**。

![[assets/figures/papers/paper_list_l21_MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field/figures/005_Table_2.jpg]]
*Table 2: Evaluation results of controllable I2V generation on our benchmark (all values are in percentage). The best result (before rethinking) is indicated in bold, the second-best result is indicated with underlines, and the third-best result is indicated with double underlines*

这一巨大差距的核心原因在于：其他方法依赖文本编码器或手动输入来控制运动，无法精准映射复杂的相机运动语义；而 MotionAgent 通过运动场智能体将文本显式转化为相机外参，再经由分析光流组合模块生成统一光流控制信号，实现了从语义到几何运动的精确转换。

**用户调研。** 主观评价进一步验证了上述结论。用户调研（Figure 6）显示，MotionAgent 在视频视觉质量和运动语义对齐两个维度上均排名第一，显著优于 DynamiCrafter、CogVideoX 和 Pyramid Flow 等对比方法。

### 消融实验

消融实验系统性地验证了各核心模块的贡献（Table 3）。

![[assets/figures/papers/paper_list_l21_MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field/figures/010_Table_3.jpg]]
*Table 3: Ablation study of object identification module, optical flow composition module and adapter tuning on our benchmark (all values are in percentage). The golden gate bridge is lit up by the setting sun, camera zooms in and pans up. Figure 7. Comparison of before and after rethinking process*

**物体识别方式。** 使用 Grounded-SAM 辅助物体识别时，Object Movement Q&A 达到 45.69%；若采用纯多轮对话方式（Detection-free），该指标降至 34.33。这表明借助现成的检测模型辅助定位物体，能显著提升运动场智能体绘制轨迹的精度。

**光流组合模块。** 移除分析光流组合模块（即直接相加物体光流和相机光流）后，Complex Camera Motion 指标急剧下降。分析组合方式在 3D 空间中整合物体轨迹和相机外参，再投影为统一光流，有效消除了直接相加带来的不合理区域，是实现物体与相机运动同步控制的关键。

**光流适配器微调。** 若适配器仅在真实光流上训练、不进行统一光流微调，Complex Camera Motion 指标从 77.76% 骤降至 48.27%。这是因为统一光流与真实光流存在域差异，微调是弥合该差异、使适配器有效响应合成光流信号的不可或缺步骤。

**轨迹绘制策略。** Table 5 对比了网格选择（Grid Selection）与直接偏移生成（Direct Offset）两种轨迹绘制方式。网格选择在 Object Movement Q&A 上更优（45.69 vs 39.29），且 Dynamic Degree 更高，说明网格化轨迹表示更有利于智能体精确描述和模型理解物体的空间运动。

![[assets/figures/papers/paper_list_l21_MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field/figures/012_Table_5.jpg]]
*Table 5: Ablation study of trajectory plotting module (all values are in percentage)*

**基础模型选择。** Table 4 的消融显示，以 SVD 为基础 I2V 扩散模型优于 DynamiCrafter，而 GPT-4o 作为智能体的推理引擎也优于其他 LLM。

![[assets/figures/papers/paper_list_l21_MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field/figures/009_Table_4.jpg]]
*Table 4: Ablation study results on different LLMs and base I2V generation model on our benchmark (all values are in percentage)*

### 重思考机制的效果

重思考（Rethinking）机制允许智能体根据生成视频的质量，对先前的运动参数进行修正。如 Table 2 和 Table 6 所示：
- 在 VBench 上，Video-Text Camera Motion 从 81.91% 进一步提升至 **87.02%**。
- 在细粒度基准上，Complex Camera Motion 从 77.76% 跃升至 **89.04%**，Object Movement Q&A 也从 45.69% 提升至 49.58%。

Figure 7 展示了一个典型案例：智能体在观察到初始生成视频的相机运动幅度不足后，自动放大了 z 轴方向的平移量，从而修正了相机运动。这一闭环反馈机制显著增强了系统对复杂运动描述的鲁棒性。

### 鲁棒性与局限性

**复杂/模糊文本的鲁棒性。** Table 7 评估了 MotionAgent 在复杂和模糊文本提示下的表现。尽管性能相比清晰提示有所下降，但该方法仍以显著优势超过所有对比方法，说明运动场智能体对运动语义的解析具有一定泛化能力。

**主要失败模式与局限。**
1. **动态度偏低**：模型倾向于只移动文本提及的物体，这在实现精确控制的同时导致 Dynamic Degree 指标较低，可能影响生成视频的“生动感”。
2. **对 LLM 的依赖**：运动场智能体依赖 GPT-4o 等大模型的推理能力，面对极端复杂或高度模糊的文本时，解析准确度会下降（Table 7），且推理成本较高。
3. **子模块误差累积**：物体识别依赖 Grounded-SAM，光流估计依赖 Unimatch，深度估计和相机位姿估计依赖 DROID-SLAM，这些子模块的误差会传播并影响最终视频质量。
4. **重思考的代价**：重思考机制引入了额外的推理和生成步骤，增加了整体耗时。

## 定位与知识库关联

### 1. 核心问题与解决路径

现有图像到视频（I2V）生成方法在运动可控性上存在根本性瓶颈：**仅靠文本编码器提取的语义特征无法实现对物体运动和相机运动的精确、细粒度控制**。如图1所示，主流框架可分为两类——

- **文本编码器控制**（Figure 1a）：如 **VideoCrafter**（Chen et al., arXiv 2023）、**ConsistI2V**（Ren et al., arXiv 2024）、**SEINE**（Chen et al., ICLR 2024）、**I2VGen-XL**（Zhang et al., arXiv 2023）、**Animate-Anything**（Dai et al., arXiv 2023）、**DynamiCrafter**（Xing et al., arXiv 2023）等基于UNet的I2V模型，以及 **CogVideoX**（Yang et al., arXiv 2024）、**Pyramid Flow**（He et al., arXiv 2024）等基于DiT的模型。它们将运动信息隐含在文本嵌入中，无法精细控制每个元素的运动轨迹。

- **专用控制模块**（Figure 1b）：如 **Motion-I2V**（Shi et al., arXiv 2024）通过显式光流建模实现运动控制，但依赖用户手动提供轨迹或相机外参等专业输入，且大多无法同时控制多种运动类型。

**MotionAgent** 的因果调节变量在于：**将文本中的运动描述显式转化为中间表示——物体轨迹和相机外参**，再通过3D空间分析光流组合为统一光流，从而用光流适配器控制冻结的扩散模型（Figure 1c）。这一“文本→显式运动参数→统一光流→扩散模型”的解耦路径，使得无需专门训练数据即可实现文本驱动的精准运动生成。

### 2. 方法谱系中的位置：关键设计槽位

以 **SVD**（Blattmann et al., arXiv 2023）为基础I2V扩散模型，MotionAgent在以下五个设计槽位上做出了区别于现有工作的选择：

| 设计槽位 | 基线做法 | MotionAgent做法 | 证据锚点 |
|---------|---------|----------------|---------|
| 运动信息提取方式 | 文本编码器直接提取文本特征，或手动提供轨迹/外参 | 运动场智能体解析文本，自动生成物体轨迹和相机外参 | Section 3.1, Figure 2 |
| 运动表示的组合方式 | 无组合或直接相加光流 | 3D空间分析光流组合（Analytical Optical Flow Composition） | Section 3.2.1, Figure 3(a) |
| 控制信号 | 文本嵌入或手动输入的轨迹/外参 | 统一光流图（由智能体自动生成并组合） | Section 3.2, Figure 3(b) |
| 光流适配器训练 | 仅在真实光流上训练 | 在统一光流图上微调以消除域差异 | Section 3.2.2 |
| 反馈机制 | 无 | 重思考（Rethinking）机制，根据生成视频修正之前的动作 | Section 3.1.4, Section 8 |

**运动场智能体**（Figure 2）是方法的核心创新：它将视频的运动场分解为物体运动和相机运动两个独立分量，利用大语言模型（GPT-4o）将自然语言分别转换为可解释的显式运动参数。物体轨迹绘制采用网格选择方式（Figure 8），相机外参的平移量被约束在 $(-1, 1)$ 并在后续模块中根据深度图重缩放。

**分析光流组合模块**（Figure 3a）是区别于直接相加光流的关键设计。其核心机制是：将物体轨迹和相机外参在3D空间整合，通过重投影方程 $I^{1} = \Pi ( E P^{1} )$ 计算移动后的像素位置，再通过 $F = I^{1} - I^{0}$ 生成统一的2D光流图。这一几何投影方式消除了直接相加光流产生的不合理区域，且实现了物体和相机运动的同步控制。

**光流适配器**（Figure 3b）在统一光流图上进行微调，以弥合合成光流与真实光流之间的域差异。训练数据通过Unimatch估计真实光流，DROID-SLAM计算相机外参，再通过逆投影分离物体运动光流 $\hat{F}_{obj} = I_{obj}^{1} - I^{0}$ 生成伪标签。

### 3. 适用边界与局限

**适用场景**：MotionAgent适用于需要从文本精确控制物体运动和相机运动的I2V生成任务，包括多物体运动控制和复杂相机运动（如缩放、平移、旋转的组合）。

**已知局限**：

1. **动态度指标偏低**：模型倾向于只移动文本中明确提及的对象，未提及的对象保持静止，这导致动态度（Dynamic Degree）指标相对较低，但这是精确控制的代价而非生成能力不足（Figure 10）。

2. **对大语言模型的依赖**：运动场智能体依赖GPT-4o等大规模语言模型的推理能力，面对复杂或模糊文本时性能会下降（Table 7）。消融实验（Table 4）显示，使用GPT-4o mini替换GPT-4o时，Object Movement Q&A从45.69降至42.86，Complex Camera Motion从77.76降至71.46。

3. **子模块误差累积**：物体识别依赖Grounded-SAM等现成工具，可能继承其检测和分割误差。光流估计（Unimatch）和深度估计模块的误差也会影响最终视频质量。

4. **额外训练负担**：需要在统一光流图上微调光流适配器来弥合域差异，增加了训练成本。

5. **推理时间增加**：重思考机制引入了额外的推理和修正步骤，增加了生成时间。

### 4. 开放问题

1. **模型轻量化**：能否将运动场智能体替换为更轻量的本地模型（如开源LLM），以降低对API的依赖和推理成本？Table 4的消融实验已初步探索了GPT-4o mini，但性能有明显下降。

2. **端到端训练**：当前智能体与扩散模型是分离的，是否可以通过联合微调进一步提升运动控制精度？

3. **长视频生成扩展**：如何将该框架扩展到长视频生成中，同时保持对每一段运动的精确控制？

4. **密集交互场景**：对于密集的多人/多物体交互场景，当前轨迹绘制和光流合成方法的鲁棒性尚未验证。

5. **闭环自监督改进**：能否利用更强的多模态模型（如GPT-4V）直接理解视频帧并实现闭环的自监督改进？当前的重思考机制已展示了这一方向的潜力——重思考步骤将Video-Text Camera Motion从81.91提升至87.02，将Complex Camera Motion从77.76提升至89.04（Table 6, Table 2）。

6. **子模块误差的量化分析**：深度估计和光流估计模型的误差对最终视频质量的影响有多大？目前缺乏系统的误差传播分析。

7. **基准覆盖范围**：自建基准的规模有限，对运动控制精度的评估可能无法覆盖所有场景，需要更大规模和更多样化的评测基准。

## 原文 PDF

![[paperPDFs/ICCV_2025/MotionAgent_Fine_grained_Controllable_Video_Generation_via_Motion_Field_Agent.pdf]]

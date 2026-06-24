---
title: "Endowing GPT-4 with a Humanoid Body: Building the Bridge Between Off-the-Shelf VLMs and the Physical World"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Endowing_GPT_4_with_a_Humanoid_Body_Building_the_Bridge_Between_Off_the_Shelf_VLMs_and_the_Physical_World.pdf
openreview_forum_id: aQWSEjcN9V
aliases:
- Endowing_GPT-4_w
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过结构化动作表示与从粗到细的视觉问答过程，使现成VLM能够精确输出可执行的低级命令；利用潜在扩散模型同时结合执行反馈与生成历史，确保动作连续性并适应物理环境。"
primary_logic: "无需大规模数据收集，直接利用现成VLM的通用推理能力，通过结构化指令编译器和扩散动作执行器桥接高级用户指令与低级物理控制，实现多样化的人形交互。"
claims:
- "BiBo在开放环境中实现平均90.2%的单一交互任务成功率。"
- "编译器中的投票机制和基于标签的视觉推理分别提升任务成功率4.1%和22.9%。"
- "BiBo较先前方法将文本引导动作执行的精度提高了16.3%。"
- "执行器中的潜在扩散模型和因果注意力显著减少动作不连续性（平均关节加速度从0.088/0.063降至0.038），并增强对物理反馈的适应性。"
---

# Endowing GPT-4 with a Humanoid Body: Building the Bridge Between Off-the-Shelf VLMs and the Physical World

> [!tip] 核心洞察
> 无需大规模数据收集，直接利用现成VLM的通用推理能力，通过结构化指令编译器和扩散动作执行器桥接高级用户指令与低级物理控制，实现多样化的人形交互。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 赋予GPT-4类人身体：在现成视觉语言模型与物理世界之间搭建桥梁 |
| 英文题名 | Endowing GPT-4 with a Humanoid Body: Building the Bridge Between Off-the-Shelf VLMs and the Physical World |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=aQWSEjcN9V); [GitHub](https://github.com/Shadow-Dream/BiBo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | BiBo |
| Dataset | Randomly Generated Scenes (100 scenes, 1365 single tasks), Randomly Generated Scenes, HumanML3D |

> [!tip] 效果简介
> - Randomly Generated Scenes (100 scenes, 1365 single tasks) 上，Single Interaction Success Rate 为 90.2% (avg.)，对比 prior methods (e.g., UniHSI, HumanVLA, TokenHSI, CLoSD)，变化 average improvement of 12.5% over baselines。
> - Randomly Generated Scenes 上，Composite Task Success Rate 为 41.0% (avg.)，对比 prior methods，变化 average improvement of 29.1% over baselines。
> - HumanML3D 上，FID (motion quality) 为 0.076，对比 other real-time arbitrary-length methods，变化 63.8% relative improvement over prior real-time arbitrary-length methods。

## 概述

赋予通用大模型以物理身体，使其在真实世界中执行复杂交互，是具身智能领域的核心挑战。现有方案通常需要针对特定任务收集大规模示教数据并训练专用模型，不仅成本高昂，且难以泛化至开放场景。本文的核心洞察在于：**现成视觉语言模型（VLM）已具备强大的开放世界推理能力，真正的瓶颈并非模型能力不足，而是高级语义指令与低级物理动作执行之间存在难以跨越的接口鸿沟。**

针对这一问题，本文提出 **BiBo**——一个直接利用现成VLM驱动人形代理的框架。BiBo由两大核心组件构成：**具身指令编译器**（Embodied Instruction Compiler）将用户的自然语言指令通过三阶段视觉问答过程转换为结构化的低级运动命令；**扩散运动执行器**（Diffusion Motion Executor）基于潜在扩散模型，同时结合物理环境中的实际执行反馈与历史生成动作，确保输出动作既精准响应命令，又在物理世界中保持连续与稳定。

实验表明，BiBo在随机生成的100个场景、1365个单一交互任务上取得平均**90.2%**的成功率，较先前方法平均提升12.5%；在复合任务上成功率平均提升29.1%。在文本引导动作执行的精度上，BiBo相较先前方法提高了**16.3%**。消融研究进一步揭示，编译器中的投票机制和基于标签的视觉推理分别贡献了4.1%和22.9%的任务成功率提升，而执行器中的潜在扩散模型与因果注意力机制将动作不连续性（平均关节加速度）从0.088降至0.038。

在方法谱系中，BiBo区别于 **UniHSI**（Xiao et al., 2023）、**HumanVLA**（Xu et al., 2024）、**TokenHSI**（Pan et al., 2025）等依赖真值动作规划或专用模型的基线，以及 **CLoSD**（Tevet et al., 2024）、**MDM**（Tevet et al., 2022）等纯文本-动作生成方法。其关键创新在于将VLM的开放推理与扩散模型的物理适应性结合，无需大规模数据收集即可实现多样化的人形场景交互。

## 背景与动机

人形代理在物理世界中执行复杂交互任务，长期面临一个核心瓶颈：**现成视觉语言模型（VLM）的开放世界推理能力与人形代理的低级物理动作执行之间存在接口鸿沟**。高级用户指令（如“休息一下”）与低级控制信号（如关节角度、末端效应器坐标）之间的语义跨度极大，使得直接将VLM用于物理交互变得异常困难。

现有方法试图弥合这一鸿沟，但各自存在根本性局限。一类方法（如**UniHSI**, Xiao et al., 2023；**HumanVLA**, Xu et al., 2024；**TokenHSI**, Pan et al., 2025）依赖大规模数据收集来训练专用模型，将场景理解与动作生成耦合在单一框架中。这种方式不仅数据采集成本高昂，且模型泛化能力受限于训练数据的分布，难以应对开放世界中多样化的交互场景。另一类方法采用基于规则的有限状态机进行任务规划，虽然可解释性强，但缺乏对自然语言指令的灵活理解，无法处理复杂的组合任务。

在动作生成层面，现有方法同样面临双重挑战。基于MLP或VQ-VAE的生成器（如**MoConVQ**, Yao et al., 2024）在运动多样性上表现受限；标准扩散模型（如**MDM**, Tevet et al., 2022；**CLoSD**, Tevet et al., 2024）虽然能生成高质量运动，但在处理物理环境反馈时存在根本缺陷：仅从已生成的动作序列延伸未来运动，忽略了实际执行过程中因物理交互产生的偏差，导致摔倒或与环境碰撞；而仅从已执行的动作延伸，则会引入严重的不连续性，造成关节抖动（平均关节加速度高达0.088–0.063，见Table 5）。

这些问题的根源在于**缺乏一个统一的框架，既能充分利用现成VLM的通用推理能力，又能在动作执行层面同时兼顾物理适应性与运动连续性**。BiBo正是在这一动机下提出：无需大规模数据收集，直接利用现成VLM，通过结构化指令编译器和扩散动作执行器的协同设计，桥接高级用户指令与低级物理控制，实现多样化的人形交互。

## 核心创新

BiBo的核心突破在于**无需大规模数据收集，直接利用现成视觉语言模型（VLM）的开放世界推理能力，通过两个关键组件的协同设计，桥接了高级用户指令与低级物理控制之间的接口鸿沟**。其创新主要体现在以下三个“changed slots”上。

### 1. 高层次任务规划：从专用模型到现成VLM的结构化指令编译

现有方法通常依赖大规模数据集训练专用模型（如**UniHSI**, Xiao et al., 2023）或基于规则的有限状态机进行任务规划，这严重限制了其在新场景和新任务上的泛化能力。BiBo的创新在于直接使用现成的VLM（如GPT-4）作为“大脑”，通过一个**具身指令编译器（Embodied Instruction Compiler）**将模糊的用户指令（如“休息一下”）转换为包含精确控制参数的结构化低级命令。

该编译器的核心机制是一个**从粗到细的三阶段视觉问答（VQA）过程**（Figure 2）：
- **第一阶段**：分析动作的基本属性，生成运动字幕、识别关键关节与目标物体。
- **第二阶段**：推理交互过程中代理的身体姿态。
- **第三阶段**：为关键关节指定目标位置与朝向。

最终，编译器输出一个结构化的执行器命令 $\mathcal{C} = \{c, l, f, \mathbb{J}\}$，包含运动字幕 $c$、代理位置 $l$、朝向 $f$ 以及关键关节目标集合 $\mathbb{J}$（Section 3.2, Eq. 1）。这一设计将VLM的通用常识推理能力直接转化为可执行的物理指令，摆脱了对特定任务数据的依赖。

消融实验证实了该设计的有效性：编译器中的**投票机制**（多次采样VLM输出并取多数结果）和**基于标签的视觉推理**（在图像上叠加方向描述符和标签网格以增强空间理解）分别将任务成功率提升了4.1%和22.9%（Table 2）。其中，基于标签的推理使姿态推理准确率和关节定位准确率分别相对提升了31.9%和55.9%，是编译器性能增益的主要来源。

### 2. 动作生成器：融合物理反馈的潜在扩散模型

传统动作生成器通常采用基于MLP的生成器、VQ-VAE或标准扩散模型，它们从已规划的“理想”动作序列延伸未来运动，却忽视了物理执行过程中不可避免的偏差（如碰撞、滑步），导致动作漂移甚至摔倒。BiBo的**扩散运动执行器（Diffusion Motion Executor）**通过一个**潜在扩散模型（LDM）**从根本上改变了这一范式。

其关键创新在于**将实际执行的动作反馈引入扩散过程**。具体而言，执行器维护两类运动潜在表示：已执行动作的潜在 $\mathcal{S}_a$ 和已生成动作的潜在 $\mathcal{S}_g$。扩散过程以编译器命令 $\mathcal{C}$ 和 $\mathcal{S}_a$ 为条件，生成未来动作的潜在 $\mathcal{S}_f$（$S_f = \mathrm{Diffusion}(\mathcal{C}, S_a)$），随后通过VAE解码器对拼接后的潜在进行联合解码（$[M_g' : M_f] = \mathrm{Decoder}([S_g : S_f])$）（Section 3.3, Eq. 2-3）。这一“已执行+已生成”双重条件机制，使得模型既能响应物理环境的实时反馈，又能保持与先前规划动作的连续性。

VAE解码器中的**因果注意力（Causal Attention）**是保证运动连续性的另一关键设计。它确保每个运动帧只能关注其之前的帧，从而在数学上保证了联合解码时已生成部分的近似重构（$M_g' \approx M_g$），避免了未来运动与当前运动之间的突变。

消融实验为这一设计提供了强有力的证据（Table 5, Table 7）：
- **移除LDM**：平均关节加速度从0.0379急剧升至0.0879，FID从0.076恶化至0.238，表明LDM是保证运动质量与平滑性的核心。
- **移除因果注意力**：平均关节加速度升至0.0626，运动不连续性显著增加。
- **仅使用已生成动作或仅使用已执行动作**：前者无法适应物理反馈导致摔倒，后者则引入剧烈抖动（Figure 6）。BiBo的双重条件机制同时解决了这两个问题。

### 3. 环境反馈处理：从开环规划到闭环执行

先前方法在执行动作时，通常仅从已生成的“理想”动作序列延伸，形成一个开环系统。当物理执行结果与规划产生偏差时，系统缺乏纠正机制。BiBo通过LDM的“从实际执行动作延伸未来潜在”的设计，构建了一个**隐式的闭环反馈系统**。

这一机制的工作原理是：每一轮执行后，系统将实际执行的动作 $M_a$ 编码为潜在 $S_a$，作为下一轮扩散过程的条件。这意味着未来运动的生成始终扎根于物理世界的真实状态，而非脱离现实的理想规划。Figure 6的定性对比清晰地展示了这一优势：仅从已生成动作延伸的方法在遇到物理干扰后会摔倒，而BiBo的方法能够平稳地适应环境变化。

此外，BiBo引入了**逆运动学（IK）后优化**步骤，使用自定义的FABRIK算法对末端效应器轨迹进行迭代优化，进一步提高了关键关节的控制精度。消融实验表明，移除IK后，Lift任务的成功率从65.42%骤降至6.80%（Table 2），证明了IK在精确关节控制中的不可替代性。

### 创新总结

综上所述，BiBo的核心创新并非提出全新的模型架构，而是**通过结构化表示与闭环反馈机制，创造性地将现成VLM的推理能力与物理世界连接起来**。编译器解决了“理解与规划”问题，执行器解决了“执行与适应”问题，二者的协同使得人形代理能够在开放环境中以平均90.2%的成功率完成多样化交互任务，相比先前方法平均提升12.5%（Table 1），并将文本引导动作执行的精度提高了16.3%。

## 整体框架

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_aQWSEjcN9V/figures/001_Figure_1.jpg]]
*Figure 1: BiBo is a humanoid agent powered by an off-the-shelf VLM. It consists of an embodied instruction compiler (Inst. Compiler) and a diffusion-based motion executor. When the user provides a high-level instruction, the compiler observes the environment and translates it into the structured command for the executor. The executor then generates future motions for the humanoid agent, conditioned on both the command and the physical feedback from the environment. In this way, BiBo is able to perform diverse types of physical scene interactions*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_aQWSEjcN9V/figures/002_Figure_2.jpg]]
*Figure 2: The embodied instruction compiler takes in user instructions and environmental observations, and directs the VLM to generate the next motion command through a structured three-stage visual question–answering process. In the first stage, it analyzes the basic attributes of the motion (e.g., caption, key joints, target object). In the second stage, it reasons about the agent’s pose during the interaction. Finally, it specifies the target positions for the key joints*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_aQWSEjcN9V/figures/003_Figure_3.jpg]]
*Figure 3: The motion executor is a Latent Diffusion Model. When receiving the command (motion caption and control parameters) from the compiler, the Diffusion extends the future latents S _ { f } from the actual executed motion tokens S _ { a } , conditioned on the command tokens s _ { m } and s _ { c } . Then, the previous and newly generated latents are jointly decoded by the VAE decoder. The decoder use casual attention, where each motion frame or latent token can only attend to its preceding tokens or frames. After IK optimization, a tracking policy drive humanoid joints to execute the newly generated motion M _ { f } in physical environment, producing the next execution result*

BiBo 是一个由现成视觉语言模型（VLM）驱动的人形代理系统，其核心设计目标是在不依赖大规模数据收集的前提下，将 VLM 的开放世界推理能力与物理世界的低级动作执行桥接起来。整个系统由两大核心模块构成：**具身指令编译器（Embodied Instruction Compiler）** 和**扩散运动执行器（Diffusion Motion Executor）**。

### 端到端流水线

系统的输入输出流遵循“高级指令→结构化命令→运动序列→物理执行”的级联范式：

1. **用户输入**：系统接收自然语言形式的高级指令（如 “have a rest”），同时获取当前环境的视觉观测。
2. **指令编译**：编译器驱动现成 VLM 通过结构化的三阶段视觉问答（VQA）过程，将高级指令与场景观测转化为结构化的低级命令 $\mathcal{C} = \{c, l, f, \mathbb{J}\}$，其中 $c$ 为运动字幕（如 “sit casually”），$l$ 为代理目标位置，$f$ 为朝向，$\mathbb{J}$ 为关键关节的目标位置集合。
3. **运动生成**：执行器接收结构化命令，采用潜在扩散模型（LDM）生成未来动作的潜在表示。该过程以实际已执行的动作 $M_a$ 和先前已生成的动作 $M_g$ 为条件，通过 VAE 编码器将其分别编码为潜在表示 $\mathcal{S}_a$ 和 $\mathcal{S}_g$，扩散模型根据命令 $\mathcal{C}$ 和 $\mathcal{S}_a$ 扩展出未来潜在 $\mathcal{S}_f$，随后解码器对拼接后的潜在 $[S_g : S_f]$ 进行联合解码，输出最终动作序列。
4. **物理执行**：生成的关节轨迹经过逆运动学（IK）后优化和基于强化学习的追踪策略，驱动人形机器人在物理环境中执行动作，产生下一轮的已执行动作反馈。

### 模块间关系与核心设计

两个模块之间存在紧密的**反馈闭环**。执行器并非简单地根据编译器的命令一次性生成完整动作，而是同时利用**已执行动作**（来自物理环境的实际反馈）和**已生成动作**（来自上一轮扩散模型的输出）作为条件。这一设计解决了两个关键问题：仅从已生成动作延伸会忽略物理反馈，可能导致摔倒；仅从已执行动作延伸则引入运动不连续性，产生抖动。通过潜在扩散模型中的因果注意力机制，解码器在重建已生成动作时保持 $M_g' \approx M_g$，从而在保证运动连续性的同时，使新生成的动作能够适应环境反馈。

编译器内部的三阶段 VQA 流程体现了从粗到细的推理策略：第一阶段分析动作的基本属性（字幕、关键关节、目标物体），第二阶段推理代理在交互过程中的姿态，第三阶段定位关键关节的目标位置。该过程还引入了**投票机制**和**基于标签的视觉推理**（方向描述符、标签网格），以提升 VLM 在空间理解和姿态推理上的鲁棒性。

整体而言，BiBo 的框架实现了“规划与执行的解耦”：编译器承担高层次的任务理解与命令规划，执行器负责低层次的运动生成与物理适应，两者通过结构化的命令接口和基于潜在空间的运动反馈机制协同工作，使现成 VLM 无需微调即可直接驱动人形代理完成多样化的物理场景交互。

## 核心模块与公式推导

BiBo由两个核心模块构成：**具身指令编译器（Embodied Instruction Compiler）** 和**扩散运动执行器（Diffusion Motion Executor）**。编译器负责将高级用户指令转换为结构化的低级命令；执行器则根据该命令生成物理可执行的动作序列，并引入环境反馈以保证运动连续性。

### 2.1 具身指令编译器：三阶段视觉问答

编译器利用现成VLM，通过一个从粗到细的三阶段视觉问答过程，将用户指令和场景观察转化为结构化的运动命令。

**第一阶段：基本属性分析。** VLM首先确定下一步要执行的动作，并分析其基本属性，包括动作字幕、关键关节、目标物体等。此阶段采用投票机制提升属性分析的鲁棒性——消融实验表明，投票机制将基本属性分析准确率相对提升10.3%，任务成功率提升4.1%（Table 2）。

**第二阶段：姿态推理。** VLM推理代理在执行交互动作时的姿态。此阶段引入基于标签的视觉推理策略，包括方向描述符和标签网格，以增强VLM对空间关系的理解。消融实验显示，该策略将姿态推理准确率和关节定位准确率分别相对提升31.9%和55.9%，整体任务成功率提升22.9%（Table 2）。

**第三阶段：关节目标定位。** VLM指定关键关节的目标位置，完成从高级指令到精确空间坐标的映射。

编译器最终输出的结构化命令 $\mathcal{C}$ 定义为：

$$\mathcal{C} = \{c, l, f, \mathbb{J}\}$$

其中 $c$ 为运动字幕（如“sit casually”），$l$ 为代理位置，$f$ 为朝向，$\mathbb{J}$ 为关键关节目标集合（Section 3.2）。该命令作为执行器的输入条件。

### 2.2 扩散运动执行器：潜在扩散模型与因果注意力

执行器采用潜在扩散模型（Latent Diffusion Model, LDM），由变分自编码器（VAE）和扩散模块组成，其核心创新在于同时利用已执行动作和已生成动作进行条件生成，以兼顾环境适应性与运动连续性。

**VAE编码阶段。** 将已执行的动作 $M_a$ 和先前已生成的动作 $M_g$ 分别通过编码器转换为潜在表示：

$$\mathcal{S}_a = \mathrm{Encoder}(M_a), \quad \mathcal{S}_g = \mathrm{Encoder}(M_g)$$

**扩散去噪与联合解码。** 扩散过程根据编译器的命令 $\mathcal{C}$ 和已执行动作的潜在 $\mathcal{S}_a$，生成未来动作的潜在 $\mathcal{S}_f$；随后，解码器对拼接后的潜在 $[S_g : S_f]$ 进行联合解码，输出最终动作序列：

$$S_f = \mathrm{Diffusion}(\mathcal{C}, S_a), \quad [M_g' : M_f] = \mathrm{Decoder}([S_g : S_f])$$

解码器采用因果注意力机制，确保每个运动帧只能关注其之前的帧，从而保证重建的先前运动 $M_g'$ 逼近原始生成运动 $M_g$，即 $M_g' \approx M_g$。这一性质强制了运动过渡的连续性。

**环境反馈的桥接机制。** 传统方法仅从已生成动作延伸未来运动，无法响应物理环境的实际反馈（如碰撞、滑步），可能导致摔倒；而仅从已执行动作延伸则引入不连续性，造成抖动。BiBo通过LDM在扩散过程中以已执行动作的潜在 $S_a$ 为条件，同时保留已生成动作的潜在 $S_g$ 参与联合解码，使生成的运动既反映真实物理状态，又保持平滑过渡（Figure 6）。

消融实验定量验证了这一设计：移除LDM后，平均关节加速度从0.0379升至0.0879；移除因果注意力后升至0.0626（Table 5）；同时移除LDM使FID从0.076恶化至0.238（Table 7）。运动不连续性通过平均关节加速度量化：

$$\bar{a} = \mathbb{E}_j \left(\| \pmb{p}_j^{n+1} + \pmb{p}_j^{n-1} - 2 \pmb{p}_j^n \|_2\right) / \dot{t}^2$$

其中 $\pmb{p}_j^n$ 表示关节 $j$ 在未来运动初始帧 $n$ 处的位置，$\dot{t}$ 为帧间隔。$\bar{a}$ 越小，运动过渡越平滑。

**逆运动学后优化。** 扩散模型输出的关节轨迹经过自定义的FABRIK逆运动学算法进行迭代优化，以提升末端效应器的控制精度。消融实验表明，移除IK后Lift任务成功率从65.42%骤降至6.80%（Table 2），证明IK对精确关节控制至关重要。最终，基于强化学习的追踪策略驱动人形关节在物理环境中执行生成的关节轨迹。

## 实验与分析

### 核心性能：开放环境任务成功率

在100个随机生成的室内场景（含1365个单一交互任务）上，BiBo在全部6类单一交互任务中均取得最高成功率，平均达**90.2%**，较先前方法（UniHSI、HumanVLA、TokenHSI、CLoSD等）平均提升12.5个百分点。在需要多步协调的复合任务上，BiBo平均成功率为**41.0%**，较基线平均提升29.1个百分点（Table 1）。值得注意的是，BiBo采用在线规划，而所有对比方法均使用预先计算的真值动作计划——即便如此，BiBo的单一任务成功率与真值计划仅相差4.38个百分点，表明编译器能够有效替代人工规划。


![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_aQWSEjcN9V/figures/004_Table_1.jpg]]
*Table 1: Comparison of task success rates for different methods under randomly generated scenes and initial poses. A single task involves navigating to the interaction position and performing the interaction, whereas a composite task consists of multiple simultaneous or sequential single interactions. BiBo (our) performs online planning during evaluation, while other methods use ground truth action plan. The bold and underline represent the best and second-best performance, respectively. BiBo achieves the highest success rate across all tasks*

具体到任务类型，BiBo在简单导航交互（Reach 99.18%、Watch 99.62%）上接近饱和；在需要精确位姿控制的任务上表现突出（Sit 95.84%、Sleep 94.89%），而在涉及末端效应器精细操作的Touch（86.05%）和Lift（65.42%）上仍有提升空间。复合任务难度递增时（Simple 58.82% → Medium 36.54% → Hard 27.78%），性能衰减明显，揭示多步协调仍是瓶颈。

### 编译器消融：投票与视觉推理的关键作用

Table 2的消融实验揭示了编译器各组件的贡献层次：


![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_aQWSEjcN9V/figures/008_Table_2.jpg]]
*Table 2: Impact of different components in compiler and executor on the task success rates. Act. and Gen. represents the actual executed motion and previous generated motion. The bold and underline represent the best and second-best performance, respectively. The results demonstrate the effectiveness of designs in BiBo*

- **投票机制**（Voting）：对同一指令进行多次采样并选择多数结果，将基本属性分析准确率相对提升10.3%，整体任务成功率提升4.1%。该机制主要惠及语义歧义较大的任务（如Touch、Lift），对确定性强的导航任务（Reach）影响微弱。
- **基于标签的视觉推理**（Label）：引入方向描述符和物体标签网格后，姿态推理准确率相对提升31.9%，关节定位准确率相对提升55.9%，整体任务成功率提升22.9%——这是编译器内部最关键的单一设计。移除标签后，Sit成功率从95.84%骤降至约73%，说明空间定位对位姿敏感任务至关重要。
- **逆运动学后优化**（IK）：移除IK后，Lift任务成功率从65.42%暴跌至6.80%，证实了在需要末端效应器精确接触的任务中，IK是不可替代的环节。对Reach、Watch等导航型任务影响较小。

### 执行器消融：LDM与因果注意力消除动作不连续性

Table 5以平均关节加速度 $\bar{a}$ 量化运动过渡的不连续性：

$$
\bar{a} = \mathbb{E}_j \left( \| \pmb{p}_j^{n+1} + \pmb{p}_j^{n-1} - 2 \pmb{p}_j^n \|_2 \right) / \dot{t}^2
$$

完整BiBo的 $\bar{a}$ 仅为**0.0379**。移除LDM后，$\bar{a}$ 升至0.0879（恶化132%）；移除因果注意力后，$\bar{a}$ 升至0.0626（恶化65%）。两者共同作用将不连续性控制在极低水平，而单独缺失任一组件的代价显著。

Table 7从运动质量角度补充了证据：移除LDM使FID从0.076恶化至0.238（下降213%），R-Precision Top-1从0.542降至0.498。因果注意力的移除同样造成FID和R-Precision的退化，但幅度小于LDM。

### 动作反馈策略：已执行动作与已生成动作的协同

BiBo在扩散过程中同时条件于已执行动作 $S_a$ 和已生成动作 $S_g$，这一设计同时解决了两个对立问题（Figure 6）：


![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_aQWSEjcN9V/figures/021_Figure_6.jpg]]
*Figure 6: Visual comparison between the executed result of different motion generation method, where the red balls in the image represents the generated motion. Act. and Gen. denotes extending future motion from actual executed motion and previous generated motion, respectively. Extending only from the generated motion fails to account for physical feedback, which may lead to falls. In contrast, extending only from the executed motion introduces discontinuities, resulting in jitter. Our method addresses both issues by incorporating physical feedback while avoiding discontinuities*

- **仅从已生成动作延伸**：无法感知物理环境反馈，在坐下、躺下等需要接触判断的任务中易导致摔倒或穿透。
- **仅从已执行动作延伸**：虽能响应物理反馈，但过渡帧出现严重抖动（jitter），$\bar{a}$ 显著升高。

Table 2的消融数据显示，同时使用两者在Touch（86.05% vs. 仅生成80.23% / 仅执行82.56%）和Lift（65.42% vs. 仅生成57.72% / 仅执行60.47%）上优势明显，证实物理反馈对接触密集型任务的关键性。

### 运动质量与控制精度

在HumanML3D基准上（Table 3），BiBo在实时任意长度生成方法中取得最优FID（**0.076**），相对先前方法提升63.8%；R-Precision Top-1达**0.542**，超过MotionLCM（0.510）和MDM（0.406）。加入物理合理性约束后，穿透率（Phys.Pen.）降至0.19，滑步（Skate）降至0.01。

控制精度方面（Table 4），BiBo在头、手、足三处的MAE分别为**0.0310 / 0.0571 / 0.0335**，全面优于DiP（0.0663 / 0.0830 / 0.0540）等基线，证明结构化命令与IK后优化的组合有效提升了末端效应器的空间定位精度。

### 定性对比与失败模式

Figure 5的定性对比揭示了各方法的典型失效模式：UniHSI生成的动作缺乏自然度（站立倚靠时姿态僵硬）；HumanVLA对初始位姿对齐要求苛刻，偏差稍大即任务失败；MoConVQ运动幅度受限，无法完成大幅度交互；CLoSD控制精度不足，末端效应器常偏离目标。BiBo在这些场景中均展现出更自然的运动过渡和更精确的末端控制。

**失败案例分析**：
1. **VLM空间理解局限**：在复杂多物体场景中，编译器可能错误识别目标物体或混淆空间关系（如将“坐在床边”误判为“坐在椅子上”），导致动作规划错误。
2. **几何建模缺失**：执行器缺乏显式的场景几何感知（如高度图、点云），在狭窄区域易发生碰撞穿透，尤其在Lift任务的抓取阶段。
3. **定位累积误差**：真实机器人部署时，基于里程计的简单定位算法在长时间导航后产生显著漂移，影响Sit等需要精确位姿对齐的任务。

### 用户研究

Table 6的用户偏好统计显示，在动作自然度、交互准确性和整体质量三个维度上，BiBo获得的偏好票数均显著高于对比方法，与定量指标趋势一致。
## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现成视觉语言模型（VLM）具备强大的开放世界推理能力，但将其直接用于人形代理的低级物理动作执行时，存在显著的接口鸿沟：VLM 输出的自然语言指令难以精确映射为关节级控制信号，而传统方法要么依赖大规模数据收集训练专用模型，要么采用基于规则的有限状态机，缺乏通用性和灵活性。BiBo 的核心洞察在于：无需从头训练，直接利用现成 VLM 的通用推理能力，通过结构化指令编译器和扩散动作执行器桥接高级用户指令与低级物理控制，实现多样化的人形交互。

### 方法谱系定位

BiBo 处于“VLM 驱动的人形代理”与“物理合理的人-场景交互”两个研究方向的交叉点。其设计在以下维度上与现有工作形成对比：

| 维度 | 先前方法 | BiBo 的设计 |
|------|----------|-------------|
| 高层次任务规划 | 收集大规模数据集训练专用模型，或基于规则的有限状态机 | 使用现成 VLM 进行结构化命令编译，通过三阶段 VQA 输出低级原语命令 |
| 动作生成器 | 基于 MLP 的生成器、VQ-VAE、标准扩散模型 | 潜在扩散模型（LDM）结合因果注意力，同时利用已执行动作与已生成动作进行条件生成 |
| 环境反馈处理 | 仅从已生成动作延伸，导致摔倒或抖动 | 从实际执行动作延伸未来潜在，并通过 VAE 联合解码确保平滑过渡 |

#### 与直接基线的关系

在任务完成性能上，BiBo 与以下方法进行了直接对比（Table 1）：
- **UniHSI**（Xiao et al., 2023）：人-场景交互基线，生成的动作自然性不足（Figure 5）。
- **HumanVLA**（Xu et al., 2024）：任务完成基线，对初始位姿要求严格，当代理初始朝向与目标不对齐时无法完成任务（Figure 5）。
- **TokenHSI**（Pan et al., 2025）：多技能交互基线。
- **CLoSD**（Tevet et al., 2024）：基于运动扩散的交互方法，控制精度不足（Figure 5）。

在运动质量评测（HumanML3D 数据集）上，BiBo 与以下文本-动作生成方法进行了对比（Table 3）：
- **MDM**（Tevet et al., 2022）：经典文本-动作扩散模型。
- **MotionLCM**（Dai et al., 2024）：高效运动生成方法。
- **MotionStreamer**（Xiao et al., 2025）：流式运动生成方法。
- **MoGenTS**（Yuan et al., 2024）：基于 Transformer 的运动合成方法。
- **MoConVQ**（Yao et al., 2024）：物理运动生成方法，运动活性有限（Figure 5）。
- **DiP**（Tevet et al., 2024）：实时运动扩散方法。
- **Double Take (MDM)**（Shafir et al., 2023）：长时域扩散采样方法。

BiBo 在单交互任务上平均成功率 90.2%，较先前方法平均提升 12.5%；复合任务成功率 41.0%，平均提升 29.1%。在线规划条件下，BiBo 的成功率与使用真值计划仅相差 4.38% 以内。

#### 技术增量与因果机制

BiBo 的技术增量集中体现在两个核心模块的协同设计：

**1. 具身指令编译器**：将 VLM 的推理过程结构化为三阶段 VQA：
- 第一阶段：分析动作基本属性（运动字幕、关键关节、目标物体）。
- 第二阶段：推理交互过程中代理的位姿。
- 第三阶段：定位关键关节的目标位置。
最终输出结构化命令 $\mathcal{C} = \{c, l, f, \mathbb{J}\}$（运动字幕、位置、朝向、关节目标集合）。消融实验表明，投票机制将基本属性分析准确率相对提升 10.3%，任务成功率提升 4.1%；基于标签的视觉推理（方向描述符、标签网格）分别将姿态推理准确率和关节定位准确率相对提升 31.9% 和 55.9%，整体任务成功率提升 22.9%（Table 2）。

**2. 扩散运动执行器**：采用潜在扩散模型（VAE + LDM）架构，其关键创新在于同时利用已执行动作 $M_a$ 和已生成动作 $M_g$ 进行条件生成。VAE 编码器将二者映射为潜在表示 $\mathcal{S}_a$ 和 $\mathcal{S}_g$，扩散过程根据命令 $\mathcal{C}$ 和 $\mathcal{S}_a$ 生成未来动作潜在 $\mathcal{S}_f$，解码器对拼接后的潜在 $[S_g : S_f]$ 进行联合解码，输出最终动作序列。因果注意力机制确保解码时每个帧只能关注其之前的帧，从而保证 $M_g' \approx M_g$，实现运动连续性。

这一设计解决了两个关键问题：
- 仅从已生成动作延伸无法响应物理反馈，可能导致摔倒。
- 仅从已执行动作延伸会引入不连续性，导致抖动。

消融实验验证了该设计的有效性：移除 LDM 使平均关节加速度从 0.0379 升至 0.0879，同时显著恶化 FID（从 0.076 升至 0.238）；移除因果注意力使加速度升至 0.0626（Table 5, Table 7）。逆运动学（IK）后优化对精确关节控制至关重要：移除 IK 后，Lift 任务成功率从 65.42% 骤降至 6.80%（Table 2）。

### 适用边界与局限

尽管 BiBo 在开放环境中取得了 90.2% 的单交互任务成功率，但其设计存在明确的适用边界：

1. **VLM 的空间理解局限**：编译器依赖 VLM 进行场景理解和空间关系推理，在复杂多物体、多层次空间关系中可能出现错误规划。论文明确报告了 VLM 在复杂场景理解上的失败案例。

2. **缺乏显式场景几何建模**：执行器未引入高度图、点云等场景几何表示，在狭窄区域易发生碰撞并导致任务失败。这是一个结构性的设计局限，而非简单的参数调优问题。

3. **真实机器人部署的定位精度**：在真实机器人实验中，简单的里程计算法导致定位不准确，影响坐下等需要精确位姿的任务。这表明 BiBo 从仿真到真实世界的迁移仍需解决感知-控制闭环的精度问题。

4. **运动多样性的上限**：当前运动控制器限制了动作的多样性，尚不能完全发挥 RL 追踪策略的全部潜力。

5. **运动质量评测的泛化性**：主要基于 HumanML3D 等标准数据集，在更复杂的真实世界场景中的泛化性有待进一步验证。

### 开放问题

从 BiBo 的设计局限出发，以下问题值得进一步探索：

- **主动环境感知**：如何为执行器引入场景体素、点云等显式几何表示，以实现精细的动作分解和避障？
- **交互类型扩展**：当前框架主要处理人-场景交互，如何扩展到手-物交互、人-人交互等更复杂的交互类型？
- **多模态对齐与连续性**：是否可以通过更长的运动前缀或更大的模型进一步提升多模态对齐与运动连续性？
- **推理延迟优化**：VLM 推理延迟对实时交互控制的影响如何？能否通过模型蒸馏或压缩进一步降低时延？
- **VLM 空间理解增强**：如何改进 VLM 的空间理解能力，使其更好地处理多物体、多层次的空间关系？

## 原文 PDF

![[paperPDFs/ICLR_2026/Endowing_GPT_4_with_a_Humanoid_Body_Building_the_Bridge_Between_Off_the_Shelf_VLMs_and_the_Physical_World.pdf]]

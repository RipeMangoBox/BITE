---
title: "Motion-Adapter: A Diffusion Model Adapter for Text-to-Motion Generation of Compound Actions"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/Motion-Adapter:_A_Diffusion_Model_Adapter_for_Text-to-Motion_Generation_of_Compound_Actions.pdf"
project_link: null
code_link: null
aliases:
- MA
- Motion-Adapter
tags:
- arxiv_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 从单动作数据自监督训练的适配器中提取解耦的交叉注意力图（decoupled cross-attention maps），并将其转化为结构掩码（structural masks），在去噪过程中有选择地更新特定身体部位所对应的运动，从而引导模型生成多部位协调的复合动作，同时不修改预训练骨干网络。
primary_logic: 通过一个在先验扩散模型之外独立训练的轻量适配器，在去噪的早期阶段（t>750）为每个动作词元（verb token）生成与身体部位对应的注意力图，并将其作为软掩码指导后续的去噪步骤，使得模型能够同时生成多个并行动作，而无需调整骨干模型参数或引入额外标注数据。
claims:
- 提出的Motion-Adapter在用户研究中获得最高的保真度（9.27 vs 第二高4.02）和感知质量（89.67% vs 57.78%），显著优于所有基线方法。
- 消融实验表明，移除Motion-Adapter或去掉掩码施加的时序约束均会导致所有自动评价指标（FID、R-Precision、Diversity等）明显下降，验证了适配器和掩码策略的关键作用。
- 在主观定性比较中，Motion-Adapter成功合成了基线方法无法完成的复合动作（如同时问候与跑步、投掷与跳跃），且动作自然连贯。
- 用户研究（User Study，65名参与者） 上 保真度（Fidelity, 1-10） = 9.27 (Motion-Adapter_MDM)
---

# Motion-Adapter: A Diffusion Model Adapter for Text-to-Motion Generation of Compound Actions

> [!tip] 核心洞察
> 通过一个在先验扩散模型之外独立训练的轻量适配器，在去噪的早期阶段（t>750）为每个动作词元（verb token）生成与身体部位对应的注意力图，并将其作为软掩码指导后续的去噪步骤，使得模型能够同时生成多个并行动作，而无需调整骨干模型参数或引入额外标注数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion-Adapter：面向复合动作文本到动作生成的扩散模型适配器 |
| 英文题名 | Motion-Adapter: A Diffusion Model Adapter for Text-to-Motion Generation of Compound Actions |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.16135) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Motion-Adapter |
| Dataset | 用户研究（User Study，65名参与者）, 用户研究（User Study）, 复合动作数据集（Compound Action Dataset） |

> [!tip] 效果简介
> - 用户研究（User Study，65名参与者） 上，保真度（Fidelity, 1-10） 9.27 (Motion-Adapter_MDM) vs 4.02 (STMC) (+5.25)。
> - 用户研究（User Study） 上，感知质量（Perceptual Quality, PQ） 89.67% (Motion-Adapter_MDM) vs 57.78% (STMC) (+31.89%)。
> - 复合动作数据集（Compound Action Dataset） 上，FID 3.592±.086 (Motion-Adapter_MDM) vs 所有基线方法均获得更高（更差）的FID (显著降低)。

## 概要

文本到动作生成（Text-to-Motion Generation）旨在从自然语言描述中合成三维人体运动序列。现有扩散模型在生成单一动作时表现良好，但在面对**复合动作**（compound actions，即同时执行多个动作，如“一边挥手一边跑步”）时暴露出两个深层瓶颈：**灾难性遗忘**与**注意力坍塌**。灾难性遗忘指早期生成的动作在后续时序融合和去噪过程中被覆盖；注意力坍塌则表现为交叉注意力图失去空间特异性，无法可靠地对应身体部位，导致动作合成失败。

本文提出 **Motion-Adapter**，一个即插即用的轻量适配器模块，无需修改预训练扩散骨干网络即可引导其生成复合动作。其核心机制是：从单动作数据自监督训练中提取**解耦的交叉注意力图**，并将其转化为身体部位对应的**结构掩码**，在去噪过程中有选择地更新特定部位的运动，从而实现多部位协调的复合动作合成。

关键结果如下：

- 在65人用户研究中，Motion-Adapter 的保真度达 **9.27**（第二名 STMC 为 4.02），感知质量达 **89.67%**（第二名 57.78%），显著超越所有基线方法（Table III）。
- 消融实验证实，移除适配器或取消掩码的时序约束均会导致所有自动指标严重退化（Table IV, Figure 12）。
- 定性比较显示，Motion-Adapter 成功合成了基线方法无法完成的复合动作（如同时问候与跑步、投掷与跳跃），且动作自然连贯（Figures 6-8）。

该方法在方法谱系上属于**扩散模型适配器**路线，与基于运动编辑（SALAD, MDM, MotionDiffuse）、运动先验（PriorMDM）或空间运动组合（STMC）等方案形成互补。其独特优势在于仅需单动作数据训练、不依赖复合动作标注或 LLM 文本分解，即可实现多部位并行动作生成。

### 问题背景：文本到动作生成中的复合动作挑战

文本驱动的人体动作生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于扩散模型（Diffusion Models）的方法在这一任务上取得了显著进展，能够生成质量较高且文本对齐良好的单一动作序列。

然而，当面对**复合动作（Compound Actions）**——即同时涉及多个身体部位执行不同动作的文本描述（如“一边挥手问候一边跑步”）时，现有方法暴露出系统性缺陷。复合动作生成的核心难点不在于生成单一动作本身，而在于**协调多个并行动作在时序和空间上的合理融合**。

### 现有方法的两个核心瓶颈

通过对现有文本到动作扩散模型的深入分析，本文识别出导致复合动作生成失败的两个关键瓶颈：

**1. 灾难性遗忘（Catastrophic Neglect）**

在扩散模型的时序融合和解码过程中，早期生成的动作特征往往在后续步骤中被覆盖或稀释。例如，当模型需要同时生成“上半身挥手”和“下半身行走”时，解码器倾向于优先保留某一部位的动作信息，而另一部位的动作特征在迭代去噪中逐渐消失。这导致最终生成的序列只保留了单一动作，无法体现文本中描述的并行行为。

**2. 注意力坍塌（Attention Collapse）**

现有扩散模型中的交叉注意力（Cross-Attention）机制在融合文本和运动特征时，注意力图往往缺乏空间特异性。如图 2 所示，基线方法 **SALAD**（Hong et al., CVPR 2025）的交叉注意力图在所有 Transformer 层上平均后，无法清晰区分不同动作词元对应的身体部位——注意力分布弥散，无法为“挥手”和“行走”分别提供可靠的身体部位对应关系。这种注意力坍塌使得模型无法在生成过程中有针对性地控制特定部位的运动。

### 现有应对方案的局限

针对复合动作生成，已有工作尝试了多种策略，但均存在明显不足：

- **基于文本分解的方法**：借助大语言模型（LLM）将复合动作描述拆解为多个单一动作，再分别生成后拼接。这类方法依赖外部模型且缺乏端到端的协调机制，拼接结果往往动作过渡生硬。
- **基于运动编辑的方法**：如 **PriorMDM**（Shafir et al., ICLR 2024）和 **MotionLab**（Guo et al., ICCV 2025），通过编辑现有运动序列来添加新动作。但这类方法倾向于生成**顺序动作**而非真正并行的复合动作——例如先完成上半身动作再执行下半身动作，而非同时进行。
- **空间运动组合方法**：如 **STMC**（Petrovich et al., CVPRW 2024），试图在空间维度组合不同身体部位的运动，但缺乏精确的身体部位定位机制，组合效果有限。

这些方法的共同缺陷在于：**缺乏一种机制，能够在生成过程中精确识别每个动作词元所对应的身体部位，并据此有针对性地更新运动表示**。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **Motion-Adapter**——一个即插即用的适配器模块，旨在引导预训练的文本到动作扩散模型生成高质量的复合动作，而无需修改骨干网络参数或引入额外的复合动作标注数据。

核心思路源于一个关键观察：**如果能够在去噪过程中获得每个动作词元对应的身体部位掩码，就可以在保持其他部位不变的情况下，仅更新特定部位的运动，从而实现多部位动作的并行合成**。基于此，Motion-Adapter 通过以下机制解决复合动作生成问题：

- **解耦交叉注意力（Decoupled Cross-Attention）**：在扩散模型之外独立训练一个轻量网络，从单动作数据中自监督学习提取每个动词词元对应的身体部位注意力图，避免注意力坍塌。
- **结构掩码引导（Structural Mask Guidance）**：将提取的注意力图转化为二值结构掩码，在去噪过程中有选择地更新特定身体部位的运动表示，防止灾难性遗忘。
- **时序约束策略**：仅在去噪早期（$t > 750$）生成掩码，并在 $t > 250$ 后停止施加掩码，避免干扰后期时空融合和运动协调性。

通过这种“适配器提取掩码 + 掩码引导去噪”的范式，Motion-Adapter 使得预训练扩散模型无需任何微调即可从单动作能力泛化到复合动作生成，为文本到动作生成领域提供了一种新的解决思路。

## 核心方法与创新机理

Motion-Adapter 的核心创新在于**将解耦交叉注意力图转化为结构掩码，以即插即用的方式引导预训练扩散模型生成复合动作**，而无需修改骨干网络参数或引入复合动作标注数据。其关键设计围绕三个 changed slots 展开，直接回应了现有方法在复合动作生成中面临的双重瓶颈——灾难性遗忘与注意力坍塌。

### 瓶颈一：灾难性遗忘的成因与掩码机制的对策

在标准文本到动作扩散模型的去噪过程中，多动作词元的时序特征在后期融合时会发生相互覆盖：早期生成的动作（如下半身行走）往往被后续去噪步骤中占主导的语义特征（如上半身挥手）所淹没。Motion-Adapter 通过**身体部位结构掩码**将不同动作词元的运动预测限制在各自对应的关节区域，从而阻断跨部位的特征干扰。

具体而言，适配器为每个动作词元 $c_i$ 生成一个二值掩码 $Mask^{c_i}$，在去噪步骤中按以下方式更新运动表示：

$$x_{t-1} = x_{t-1} * (1 - Mask_{t-1}^{c_i}) + x_{t-1}^{c_i} * Mask_{t-1}^{c_i}$$

该公式的含义是：仅将动作 $c_i$ 的运动预测 $x_{t-1}^{c_i}$ 注入掩码激活的身体部位，而保持其余部位不变。这一机制使得上半身和下半身的动作可以**并行生成且互不干扰**，从根本上解决了灾难性遗忘问题。

### 瓶颈二：注意力坍塌的成因与解耦交叉注意力的对策

现有扩散模型（如 SALAD）的交叉注意力图在多层 Transformer 中高度耦合，导致不同动作词元的注意力分布趋于同质化，丧失了对特定身体部位的空间特异性——此即“注意力坍塌”。这使得注意力图无法为复合动作提供可靠的身体部位对应关系。

Motion-Adapter 的解法是**在骨干网络之外独立训练一个解耦交叉注意力网络（Decoupled Cross-Attention Network）**。该网络由五级 STEncoder 模块构成，每级包含时空编码层与交叉注意力层，接收文本嵌入和单动作运动序列作为输入，通过自监督重建任务进行训练，损失函数为关节级的均方误差：

$$\mathcal{L}_{\mathrm{recon}} = \frac{1}{N} \sum_{j=1}^{N} \left\| \mathbf{m}_j - \hat{m}_j \right\|_2^2 \quad (m_j \in M, \hat{m}_j \in \hat{M})$$

由于该网络仅处理单动作数据，其交叉注意力层天然地学会了将每个动词词元与对应身体部位对齐。实验表明，选取第三层交叉注意力的注意力图，经过归一化、阈值化和上下肢分组约束后，能够生成高质量的二值结构掩码。与 SALAD 将所有 Transformer 层的注意力图平均化不同，Motion-Adapter 的解耦设计确保了每个动作词元的注意力图具有明确的身体部位对应（见 Figure 2），从而为掩码生成提供了可靠基础。

### 关键设计：掩码施加的时序策略

Motion-Adapter 的另一个关键创新在于**掩码生成与施加的时序约束**。适配器仅在去噪早期（$t > 750$）生成掩码，因为此时运动的大致结构已经形成，注意力图足够可靠；而在去噪后期（$t \leq 250$）停止施加掩码，以避免干扰精细的时空融合和运动协调性。消融实验（Table IV, Figure 12）证实：若在全去噪步长上持续施加掩码，会导致运动过渡不平滑（Transition 指标上升），且过早提取的注意力图不可靠，进一步验证了该时序策略的必要性。

### 训练数据与适配方式的优势

与需要复合动作配对数据或依赖 LLM 分解文本的基线方法（如 STMC）不同，Motion-Adapter **仅在单动作数据上自监督训练**，无需任何复合动作标注。训练完成后，适配器以冻结参数的形式嵌入预训练扩散模型（如 MDM、MotionDiffuse），不微调骨干网络的任何参数。这种即插即用的设计使其能够泛化到不同骨干网络，Figure 11 展示了 Motion-Adapter 在 MotionDiffuse 上同样显著提升了复合动作生成能力。

### 与基线方法的关键差异总结

| 维度 | 基线方法 | Motion-Adapter |
|------|---------|----------------|
| 身体部位掩码来源 | 无显式结构掩码，或依赖人工指定/LLM分解 | 解耦交叉注意力网络自动提取，转化为二值结构掩码 |
| 掩码施加策略 | 无掩码指导，或全步长持续施加 | 仅在 $t > 750$ 生成，$t > 250$ 后停止施加 |
| 训练数据需求 | 需复合动作配对数据或外部语言模型 | 仅需单动作数据，自监督训练，不微调骨干网络 |

用户研究结果（Table III）为上述创新提供了强有力的实证支持：Motion-Adapter_MDM 的保真度达到 9.27，远超第二高的 STMC（4.02）；感知质量达 89.67%，而 STMC 仅为 57.78%。消融实验进一步表明，移除 Motion-Adapter 或取消掩码时序约束均导致所有自动指标显著退化，验证了适配器及其时序策略的不可替代性。

Motion-Adapter 采用“适配器外挂 + 预训练骨干冻结”的范式，在不修改文本到动作扩散模型参数的前提下，通过注入结构掩码引导去噪过程，使模型具备生成复合动作的能力。其整体流水线由三个核心模块串联构成：解耦交叉注意力网络、结构掩码生成模块，以及掩码去噪集成模块。

**输入与输出流。** 系统接收两个输入：(1) 描述复合动作的文本提示（如“greeting and running”），经文本编码器提取词元嵌入；(2) 从预训练扩散模型（如 **MDM** (Tevet et al., ICLR 2023) 或 **MotionDiffuse** (Zhang et al., IEEE TPAMI 2024)）的噪声调度中采样的当前时间步隐变量 $x_t$。输出为经过掩码引导更新后的去噪隐变量 $x_{t-1}$，最终解码为包含多个并行动作的运动序列。

**模块关系与执行时序。** 三个模块在去噪循环中按时间步条件协同工作（见 Figure 3）：

1. **解耦交叉注意力网络（Decoupled Cross-Attention Network）** 仅在时间步 $t > 750$ 时激活。它接收文本嵌入和单动作运动序列，通过五级时空编码器（STEncoder）与交叉注意力层，为每个动词词元生成对关节的注意力图。该网络在单动作数据上以自监督方式独立训练，损失函数为关节级均方误差：
   $$\mathcal{L}_{\mathrm{recon}} = \frac{1}{N} \sum_{j=1}^{N} \left\| \mathbf{m}_j - \hat{m}_j \right\|_2^2 \quad (m_j \in M, \hat{m}_j \in \hat{M})$$
   其中 $M$ 为真实运动，$\hat{M}$ 为重建运动，$N$ 为关节数。

2. **结构掩码生成模块（Structural Mask Generation）** 选取第三层交叉注意力的注意力图，经归一化、阈值化和上下肢骨骼池化（skeletal pooling，见 Figure 4）约束，生成二值化的身体部位结构掩码 $\mathrm{Mask}^{c_i}$。掩码生成同样限定在 $t > 750$，因为过早提取的注意力图尚不可靠。

3. **掩码去噪集成（Masked Denoising Integration）** 在扩散模型的每个去噪步中，利用生成的掩码将对应动作词元 $c_i$ 的局部运动预测 $x_{t-1}^{c_i}$ 与全局运动 $x_{t-1}$ 进行融合：
   $$x_{t-1} = x_{t-1} \cdot (1 - \mathrm{Mask}_{t-1}^{c_i}) + x_{t-1}^{c_i} \cdot \mathrm{Mask}_{t-1}^{c_i}$$
   掩码施加在 $t > 250$ 后停止，以避免干扰后期时空融合和运动协调性。这一时序约束是方法的关键设计——消融实验表明，在全去噪步长上持续施加掩码会导致运动过渡不平滑（Transition 指标上升），且过早提取的注意力图质量下降（见 Table IV, Figure 12）。

**与骨干模型的关系。** Motion-Adapter 作为即插即用模块，不修改预训练扩散模型的权重。实验验证了其跨骨干的泛化性：当适配器分别搭载 **MDM** 和 **MotionDiffuse** 时，均能显著提升复合动作生成质量（见 Figure 11）。这种设计使适配器的训练完全依赖单动作数据，无需复合动作标注，也无需对骨干网络进行任何微调。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_16135/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the Motion-Adapter integrated into the diffusion model at step t*

Motion-Adapter 由两个核心模块构成：**解耦交叉注意力网络**与**结构掩码生成模块**。前者负责从文本词元中提取与身体部位对应的注意力图，后者将这些注意力图转化为可嵌入扩散去噪过程的结构掩码。

### 解耦交叉注意力网络

该网络是一个自监督框架，由五级 **STEncoder** 模块堆叠而成，每级包含一个时空编码器层和一个集成其中的交叉注意力机制。网络接收文本嵌入和单动作运动序列作为输入，通过卷积与交叉注意力操作将语义信息直接映射到关节特征上，从而建立动词词元与身体部位之间的对应关系。

训练时仅使用单动作数据，无需复合动作标注。网络以重建损失进行优化：

$$ \mathcal { L } _ { \mathrm { r e c o n } } = \frac { 1 } { N } \sum _ { j = 1 } ^ { N } \left\| \mathbf { m } _ { j } - \hat { m _ { j } } \right\| _ { 2 } ^ { 2 } \left( m _ { j } \in M , \hat { m } _ { j } \in \hat { M } \right) $$

其中 $M$ 为真实运动序列，$\hat{M}$ 为网络重建的运动序列，$N$ 为关节数量。该损失最小化每个关节位置的重建误差，迫使网络学习将文本语义准确分配到对应身体部位。

**注意图层级选择**：实验发现，第三层交叉注意力的注意力图在定位身体部位时最为可靠，因此后续掩码生成仅使用该层的输出。相比之下，基线方法 **SALAD**（Hong et al., CVPR 2025）的注意力图是所有 Transformer 层的平均值，缺乏空间特异性。

### 结构掩码生成模块

该模块将解耦交叉注意力网络提取的注意力图转化为二值结构掩码，流程如下：

1. **归一化与阈值化**：对选定的注意力图进行归一化，并通过阈值操作将其二值化，得到每个动词词元对应的激活区域。
2. **骨骼池化**：基于 HumanML3D 数据集的骨骼结构，将关节级掩码聚合为上下肢两组区域掩码，确保掩码覆盖语义合理的身体部位群组，而非孤立的单个关节。

生成的掩码 $Mask_{t-1}^{c_i}$ 对应于动作词元 $c_i$ 所激活的身体部位区域。

### 掩码运动更新

在扩散模型的每个去噪步中，利用生成的掩码将各动作词元对应的局部运动预测融合到全局运动表示中：

$$ x _ { t - 1 } = x _ { t - 1 } * ( 1 - M a s k _ { t - 1 } ^ { c _ { i } } ) + x _ { t - 1 } ^ { c _ { i } } * M a s k _ { t - 1 } ^ { c _ { i } } $$

其中 $x_{t-1}$ 为当前去噪步的全局运动表示，$x_{t-1}^{c_i}$ 为仅以动作词元 $c_i$ 为条件预测的运动。该公式的含义是：**仅更新掩码激活的身体部位**，未激活区域保持原有运动不变。通过依次对每个动作词元执行此操作，模型可将多个单动作的运动预测融合为协调的复合动作。

### 时序约束策略

掩码的生成与施加具有严格的时间步约束：

- **掩码生成阶段**：仅在 $t > 750$（扩散过程的早期）提取注意力图并生成掩码。过早提取（$t$ 接近 1000）时噪声过大，注意力图不可靠。
- **掩码施加阶段**：在 $t > 250$ 后停止施加掩码。这是因为去噪后期，模型需要自由进行时空融合以协调各部位运动；若全程施加掩码，会导致运动过渡不平滑，Transition 指标显著上升。

消融实验（Table IV）证实，取消上述时序约束会使所有自动评价指标退化，验证了该策略的关键作用。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_16135/figures/005_Figure_5.jpg]]
*Figure 5: The architecture of the decoupled cross-attention*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_16135/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of attention maps from SALAD [3] and our Motion-Adapter. SALAD’s maps are averaged across all Transformer layers at step 40, while ours are taken from the third cross-attention layer at step 750*

## 实验与关键发现

### 评估基准与设置

为系统评估复合动作生成能力，作者构建了一个专用的复合动作测试集（Table I），包含上半身（如“greet”“throw”“stretch”）与下半身（如“walk”“run”“jump”）动作提示词的组合。该基准覆盖了简单组合（如“greeting + walking”）与需要全身协调的复杂提示（如“jump and turn”），用于检验方法在不同难度层级上的表现。

定量评估沿用文本到动作生成领域的标准指标：FID（衡量生成分布与真实分布的距离）、R-Precision（检索精度）、MM-Dist（多模态距离）、Diversity（多样性）和Transition（过渡平滑度）。作者特别指出，现有评价模型原本针对简单动作训练，因此在复合动作数据上进行了微调以缓解评估偏差，但重训数据仍可能引入分布偏差，这一点需要读者注意。

### 主要定量结果

Table II 报告了 Motion-Adapter 与七个基线方法在复合动作测试集上的全面对比。基线包括 **MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse**（Zhang et al., IEEE TPAMI 2024）、**SALAD**（Hong et al., CVPR 2025）、**STMC**（Petrovich et al., CVPRW 2024）、**MoGenTS**（Yuan et al., NeurIPS 2024）、**PriorMDM**（Shafir et al., ICLR 2024）和 **MotionLab**（Guo et al., ICCV 2025）。

Motion-Adapter 在几乎所有指标上取得最优或次优成绩。以 MDM 为骨干时，Motion-Adapter_MDM 的 FID 降至 3.592±0.086，显著优于所有基线方法。在 R-Precision 和 MM-Dist 上同样领先，表明生成动作与文本描述的语义一致性更强。Diversity 指标接近真实分布，Transition 指标表明动作过渡保持自然平滑。

### 用户研究

作者进行了 65 人参与的用户研究（Table III），从保真度（Fidelity，1-10 分）和感知质量（Perceptual Quality, PQ）两个维度评估。Motion-Adapter_MDM 获得 9.27 分的保真度，而第二高的 STMC 仅 4.02 分，差距达 +5.25 分。感知质量方面，Motion-Adapter_MDM 达到 89.67%，STMC 为 57.78%，提升 +31.89 个百分点。这一悬殊差距表明，现有方法在复合动作生成上存在根本性困难，而 Motion-Adapter 的掩码引导策略有效解决了这一瓶颈。

### 定性分析

定性对比（Figures 6-8）直观展示了各方法在简单复合动作上的表现差异。以“greeting + walking”为例，基线方法普遍出现灾难性遗忘——要么只生成行走而忽略问候动作，要么生成两个动作的顺序拼接而非并行执行。SALAD 的运动编辑结果（Figure 9）进一步证实了这一问题：其倾向于产生“先问候再行走”的顺序动作，而非真正同步的复合动作。相比之下，Motion-Adapter 成功合成了上半身挥手问候与下半身行走同时进行的自然动作，且时间一致性保持良好。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_16135/figures/010_Figure_9.jpg]]
*Figure 9: Motion editing results of SALAD [3]. The black text represents the source content, while the green text indicates the editing instructions*

在复杂提示下（Figure 10），如“jump and turn”这类需要全身协调的动作，基线方法往往丢失其中一个动作或产生不自然的过渡。Motion-Adapter 通过结构掩码在去噪早期有选择地更新各身体部位的运动，使得多个动作能够并行生成且相互协调。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_16135/figures/011_Figure_10.jpg]]
*Figure 10: Qualitative comparison results of compound actions with complex textual prompts. To enhance visual clarity, the later frames are rendered with increased transparency, and arrows indicate the direction of motion*

### 跨骨干泛化

Figure 11 展示了 Motion-Adapter 与 MotionDiffuse 骨干结合的结果。即使更换底层扩散模型，适配器仍能有效提升复合动作生成质量，验证了其即插即用的设计理念——不修改预训练参数，仅通过外部掩码引导即可赋能不同骨干网络。

### 消融实验

Table IV 和 Figure 12 报告了关键消融结果，验证了两个核心设计选择的有效性：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_16135/figures/016_Figure_12.jpg]]
*Figure 12: Attention maps extracted at*

**移除 Motion-Adapter**：当去除适配器、直接使用原始 MDM 或 MotionDiffuse 时，模型完全无法生成有效的复合动作，所有自动指标严重退化。这直接证实了灾难性遗忘和注意力坍塌是现有方法的真实瓶颈，而非简单提示工程可解决的问题。

**取消掩码时序约束**：若在整个去噪过程持续施加掩码（而非在 t>250 后停止），Transition 指标显著上升，表明运动过渡变得不平滑。同时，在 t<750 时提取的注意力图不可靠（Figure 12），过早的掩码生成会引入噪声，破坏运动协调性。这一消融验证了“早期生成掩码、后期释放约束”策略的必要性：掩码仅在去噪早期提供结构引导，后期则让骨干网络自主完成时空融合，确保动作的自然连贯。

### 失败模式与局限性

尽管 Motion-Adapter 在复合动作生成上取得了突破性进展，其能力仍受限于预训练扩散骨干网络本身——适配器无法生成骨干网络能力范围之外的动作类型或质量。此外，当前设计将人体粗略划分为上下两个区域，缺乏对手部、手指等精细部位的控制能力，限制了细腻表现力动作的生成。这些局限性指向了未来改进方向：建立更细粒度的身体部位与文本词元对应关系，以及探索将掩码策略扩展到风格迁移、情感表达等更广泛的运动编辑任务。

## 定位与知识库关联

### 1. 与基线方法的关系

Motion-Adapter 的核心定位是一种**即插即用的适配器**，旨在解决现有文本到动作扩散模型在复合动作生成中的结构性缺陷。与以下基线方法的关系如下：

- **MDM** (Tevet et al., ICLR 2023) 和 **MotionDiffuse** (Zhang et al., IEEE TPAMI 2024)：这两者是 Motion-Adapter 直接适配的预训练骨干网络。原始模型在处理复合动作时面临**灾难性遗忘**（catastrophic neglect）和**注意力坍塌**（attention collapse）问题——早期动作词元在后期时序融合中被覆盖，且交叉注意力图失去空间特异性。Motion-Adapter 不修改这些骨干网络的参数，而是通过外部生成的解耦交叉注意力图作为结构掩码，在去噪过程中引导特定身体部位的运动更新，从而绕过上述瓶颈。

- **SALAD** (Hong et al., CVPR 2025)：SALAD 采用基于 Transformer 的交叉注意力机制进行运动编辑，但其注意力图在空间上高度耦合，无法为不同身体部位提供可分离的定位信息（见 Figure 2 对比）。实验表明，SALAD 倾向于生成**顺序动作**（如先问候再行走），而非真正并行的复合动作（见 Figure 9）。Motion-Adapter 通过解耦交叉注意力和结构掩码生成，实现了动作词元与身体部位的直接对应，从而支持多个动作的同时执行。

- **STMC** (Petrovich et al., CVPRW 2024)：作为空间运动组合基线，STMC 需要人工指定或依赖外部机制（如 LLM 分解文本）来实现多部位合成。Motion-Adapter 则完全自动化——仅从单动作数据自监督训练适配器，无需复合动作标注或外部文本分解。

- **MoGenTS** (Yuan et al., NeurIPS 2024)、**PriorMDM** (Shafir et al., ICLR 2024)、**MotionLab** (Guo et al., ICCV 2025)：这些方法在通用文本到动作生成或运动先验建模上各有贡献，但均未针对复合动作的灾难性遗忘和注意力坍塌问题提出专门的结构掩码引导机制。Motion-Adapter 在复合动作测试集上的定量结果（Table II）和用户研究（Table III，保真度 9.27 vs 次优 4.02，感知质量 89.67% vs 57.78%）均显著领先于这些基线。

### 2. 方法适用边界

Motion-Adapter 的有效性受以下边界条件约束：

- **生成能力上限受限于预训练骨干网络**：适配器本身不增强骨干网络的底层运动生成能力，仅通过掩码引导实现多部位协调。若骨干网络对某类单动作的生成质量本身较差，适配器无法弥补这一缺陷。

- **身体部位划分粒度较粗**：当前设计将人体分为上、下两个大致区域（通过骨骼池化实现，见 Figure 4），缺乏对手部、手指等精细部位的控制。这意味着对细腻和富有表现力的局部动作（如手势、面部表情）的生成能力有限。

- **依赖可靠的注意力图提取**：掩码生成仅在去噪早期（t > 750）进行，且掩码施加在 t > 250 后停止。这一时序策略是基于经验观察——过早提取的注意力图不可靠，过晚施加掩码会干扰时空融合（见 Figure 12 消融可视化）。若扩散模型的时间步调度或噪声水平发生显著变化，该策略可能需要重新校准。

- **复合动作的复杂性边界**：当前评估主要覆盖上下半身各一个动作词的组合（Table I）。对于涉及三个及以上身体部位同时执行不同动作的极端场景，方法的鲁棒性尚未得到系统验证。

### 3. 局限与开放问题

**已知局限**（论文中明确指出的）：

1. **生成能力受限于骨干网络**：如前所述，适配器无法超越预训练扩散模型的固有生成能力。
2. **精细部位控制缺失**：上下半身的粗粒度划分限制了对局部动作（如手部、手指）的精确控制。

**开放问题**（论文中提出或可从方法逻辑中自然延伸的）：

1. **细粒度身体部位-文本对应**：如何建立身体部位与文本词元之间更精细的对应关系？例如，将“挥手”映射到手臂而非整个上半身。这可能需要引入更细粒度的骨骼分组策略或层次化掩码生成机制。

2. **任务泛化能力**：Motion-Adapter 的掩码引导机制是否可扩展到更广泛的运动编辑与生成任务？例如，通过定义特定任务的掩码（如风格迁移掩码、情感表达掩码），适配器可能成为一种通用的运动编辑接口。论文在 Figure 11 中已初步验证了跨骨干网络的即插即用能力（Motion-Adapter MotionDiffuse），但跨任务的泛化仍需进一步探索。

3. **评价偏差的缓解**：论文指出，定量评估中使用的评价模型原本针对简单动作训练，存在偏差。作者通过在复合动作数据集上微调评价模型以缓解该问题，但重训数据仍可能引入分布偏差。如何建立更公正的复合动作评价体系，是一个值得关注的问题。

4. **掩码时序策略的自适应**：当前的掩码生成和停止时间步（t > 750 生成，t > 250 停止施加）是固定阈值。这些阈值是否可自适应地根据文本复杂度或运动长度动态调整，以进一步提升复合动作的连贯性和自然度，是一个值得研究的方向。

## 原文 PDF

![[paperPDFs/arxiv_2026/Motion-Adapter:_A_Diffusion_Model_Adapter_for_Text-to-Motion_Generation_of_Compound_Actions.pdf]]

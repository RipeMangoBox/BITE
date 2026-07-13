---
title: "Learn the Force We Can: Enabling Sparse Motion Control in Multi-Object Video Generation"
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Video_Generation.pdf
project_link: https://araachie.github.io/yoda
code_link: null
aliases:
- LFWCESMCMOVG
tags:
- AAAI_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "稀疏运动控制：通过从光学流场中按运动幅度采样少量像素点（通常5个）作为控制输入，配合受限感受野的网格化编码器（16×16独立MLP），迫使模型学习将局部像素位移关联到完整物体的运动。"
primary_logic: "随机化条件训练（以概率π=0.5随机丢弃上下文帧或控制信号）使模型必须同时利用两种信息，从而隐式地学会了物体分离与交互预测；同时，限制光流编码器的感受野是独立控制不同物体的关键设计。"
claims:
- "YODA在BAIR数据集上以5个控制点超越了所有先前可控视频生成方法，LPIPS 0.112，FID 18.2，FVD 264。"
- "受限感受野的稀疏光流编码器（独立MLP网格）相比卷积编码器显著降低局部误差，且误差分布更集中于小数值，无长尾大误差。"
- "随机化条件训练（π>0）对视频质量至关重要；在CLEVRER上，无随机化时FVD从70剧增至401。"
- "控制向量数量n_c存在权衡，n_c=5在局部误差（控制精度）和全局误差（交互建模）之间达到最佳平衡。"
---

# Learn the Force We Can: Enabling Sparse Motion Control in Multi-Object Video Generation

> [!tip] 核心洞察
> 随机化条件训练（以概率π=0.5随机丢弃上下文帧或控制信号）使模型必须同时利用两种信息，从而隐式地学会了物体分离与交互预测；同时，限制光流编码器的感受野是独立控制不同物体的关键设计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 尽我们所能学习力：实现多物体视频生成中的稀疏运动控制 |
| 英文题名 | Learn the Force We Can: Enabling Sparse Motion Control in Multi-Object Video Generation |
| 会议/期刊 | AAAI 2024 |
| Links | [paper](https://arxiv.org/abs/2306.03988) · [Project](https://araachie.github.io/yoda) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | YODA |
| Dataset | BAIR, CLEVRER |

> [!tip] 效果简介
> - BAIR 上，LPIPS↓ 为 0.112 (YODA, n_c=5)，对比 0.154 (SAVP+)，变化 -0.042。
> - BAIR 上，FID↓ 为 18.2 (YODA, n_c=5)，对比 27.2 (SAVP+)，变化 -9.0。
> - BAIR 上，FVD↓ 为 264 (YODA, n_c=5)，对比 303 (SAVP+)，变化 -39。

## 概要

### 问题与瓶颈

在无监督条件下，对多物体场景中每个物体进行**独立运动控制**并生成真实的物体间交互，是现有视频生成方法的瓶颈。先前可控视频生成工作要么依赖显式标注（如边界框、分割掩码），要么仅限于单物体场景，无法在稀疏用户输入下同时实现精确的局部控制和合理的全局交互建模。

### 核心方法：YODA

本文提出 **YODA**（You Only Direct Actions），一种基于流匹配的稀疏运动控制视频生成方法。其核心思路是**“尽我们所能学习力”**——仅需用户在光流场上按运动幅度采样极少量的像素点（典型值为 5 个）作为控制输入，即可驱动视频中对应物体的运动，同时自动生成物体间的物理交互。

YODA 以 **RIVER**（Davtyan et al., ICCV 2023）为骨干视频预测模型，在其流匹配框架上引入三个关键设计：

1. **稀疏运动控制信号注入**：通过交叉注意力层在 U-ViT 瓶颈处融合运动控制令牌，将像素级位移指令传入生成过程。
2. **受限感受野的光流编码器**：将稀疏光流划分为 $16 \times 16$ 网格，每个网格独立通过 MLP 编码，限制感受野以强制模型将局部像素位移关联到完整物体的运动，而非学习全局相关性。
3. **随机化条件训练**：以概率 $\pi = 0.5$ 随机丢弃上下文帧或控制信号，迫使模型同时利用两种信息，隐式地学会物体分离与交互预测。

### 方法定位

YODA 属于**稀疏运动控制视频生成**方法，在方法谱系中处于无监督像素级控制与流匹配生成模型的交叉点。与需要物体掩码的 **iPOKE**（Blattmann et al., ICCV 2021）和依赖离散动作代码的 **CADDY**（Menapace et al., CVPR 2021）不同，YODA 无需任何物体标注或前景/背景先验。与解耦全局-局部动作的 **GLASS**（Davtyan and Favaro, ECCV 2022）相比，YODA 通过受限感受野和随机化训练实现了更精细的逐物体独立控制。

### 主要结果

在 BAIR 机器人推动数据集上，YODA 仅使用 5 个控制点即超越了所有先前可控视频生成方法：LPIPS 达 0.112，FID 达 18.2，FVD 达 264（Table 2）。消融实验证实了三个关键设计的决定性作用：

- **受限感受野编码器**相比卷积编码器显著降低了局部误差，且误差分布更集中于小数值，消除了大误差长尾（Figure 3）。
- **随机化条件训练**（$\pi > 0$）对视频质量至关重要：在 CLEVRER 数据集上，无随机化时 FVD 从 70 剧增至 401（Table 1）。
- **控制向量数量** $n_c = 5$ 在局部误差（控制精度）和全局误差（非控制区域的运动泄漏）之间达到最佳平衡（Figure 4）。

### 局限与开放问题

YODA 的训练依赖预训练光流估计器提供运动伪标签，控制信号质量受光流精度限制；控制仅支持 2D 平移位移，对旋转、形变等复杂运动难以精确表达。未来方向包括将像素位移控制泛化到语义级控制、在无光流标签条件下自监督学习控制编码，以及探索学到的隐式物体注意力在 zero-shot 分割等下游任务中的应用。



可控视频生成的目标是赋予用户对生成内容的运动行为进行精确操纵的能力。然而，在**多物体场景**中实现这一目标，面临一个根本性瓶颈：如何在不依赖任何物体标注（如边界框、分割掩码）的前提下，使模型能够**独立控制每个物体的运动**，同时生成真实的物体间交互。

现有方法在这一问题上存在明显缺口。以 **iPOKE**（Blattmann et al., ICCV 2021）为代表的像素级控制方法，虽然允许用户通过指定像素位移来引导运动，但其依赖卷积编码器处理稀疏光流信号，导致控制信号在空间上发生泄漏——对某一物体的控制指令会意外地驱动其他物体运动。另一方面，**CADDY**（Menapace et al., CVPR 2021）等基于离散动作代码的方法，以及 **GLASS**（Davtyan and Favaro, ECCV 2022）等解耦全局与局部动作的方法，要么控制粒度粗糙，要么局限于单物体场景。**RIVER**（Davtyan et al., ICCV 2023）作为高效的视频预测骨干，基于流匹配（flow matching）实现了高质量的视频生成，但其本身不接收任何外部运动控制信号，仅条件于历史帧。**MoCoGAN**（Tulyakov et al., CVPR 2018）和 **SAVP**（Lee et al., 2018）等经典方法同样缺乏对多物体独立运动的精细控制能力。

上述方法的共同缺陷揭示了一个深层问题：**在没有物体级监督的情况下，模型难以建立“局部控制信号”与“完整物体运动”之间的正确关联**。当控制信号通过具有大感受野的编码器处理时，网络倾向于将局部像素位移与全局场景变化纠缠在一起，导致“牵一发而动全身”的失控现象。

YODA 的动机正是针对这一瓶颈。其核心思路是：通过**极端的稀疏性**和**受限的感受野**，迫使模型学习将少量像素的位移信号正确地归因到对应的完整物体上。具体而言，YODA 从预训练光流估计器（RAFT）产生的稠密光流场中，按运动幅度仅采样极少量像素点（通常仅 5 个）作为控制输入；同时，将稀疏光流划分为 16×16 网格，每个网格独立通过 MLP 编码，严格限制编码器的感受野。这种设计从信息瓶颈的角度切断了控制信号在空间上的任意传播路径。

此外，YODA 引入**随机化条件训练**策略：以概率 $\pi = 0.5$ 随机丢弃上下文帧或控制信号。这一策略迫使模型必须同时学会利用历史视觉信息和控制信号，从而隐式地实现了物体分离与交互预测的解耦——当控制信号缺失时，模型依赖上下文帧进行自然的视频预测；当控制信号存在时，模型则响应控制指令。这种“条件解耦”机制是 YODA 在无监督设定下实现多物体独立控制的关键。



## 核心方法与创新机理

YODA 的核心创新在于通过**稀疏运动控制**机制，首次在无监督条件下实现了对多物体视频中每个物体的独立运动操控，并保持真实的物体间交互。其关键设计围绕三个紧密耦合的“changed slots”展开，共同解决了现有方法的瓶颈。

### 1. 受限感受野的稀疏光流编码器

这是实现独立物体控制的关键设计。与先前工作 **iPOKE**（Blattmann et al., ICCV 2021）使用卷积编码器处理整个稀疏光流场不同，YODA 将输入的光流场划分为一个 $16 \times 16$ 的网格，每个网格单元内的稀疏光流信息由一个独立的 MLP 进行编码。这一设计强制限制了编码器的感受野，迫使模型将局部的像素位移信号仅与对应空间位置的物体运动相关联。

**因果机制**：卷积编码器的大感受野会导致控制信号“泄漏”——对一个像素点的运动控制会无意中影响其他物体的运动，表现为图 3 中卷积编码器局部误差分布存在明显的长尾大误差。而受限感受野的网格化 MLP 编码器从根源上切断了这种空间信息串扰，使得每个控制令牌仅携带局部运动信息，模型必须学会将这些局部信号与完整物体的运动关联起来，从而实现了对不同物体的解耦控制。

**证据强度**：图 3 的消融实验（置信度 0.95）直接对比了两种编码器的局部误差分布。受限感受野编码器不仅降低了整体平均误差，且误差分布更集中于小数值区域，完全消除了卷积编码器中的大误差长尾。图 9 的定性结果进一步显示，使用卷积编码器时，机械臂的运动与控制输入存在错误的相关性。

### 2. 随机化条件训练策略

YODA 以概率 $\pi = 0.5$ 在每次训练迭代中随机丢弃上下文帧或运动控制信号，这一训练策略是实现物体分离与交互预测的核心。

**因果机制**：当模型无法依赖完整的条件信息时，它被迫学习两种互补的能力：
- 仅给定上下文帧而无控制信号时，模型必须像标准视频预测模型一样，从历史信息中推断所有物体的自然运动，这强化了交互建模能力。
- 仅给定控制信号而无上下文帧时，模型必须仅从稀疏的运动控制中推断场景动态，这强化了控制响应精度。
- 通过随机化，模型在推理时可以利用分类器无关引导（classifier-free guidance）机制，在控制精度和自然交互之间取得平衡。

**证据强度**：表 1 在 CLEVRER 数据集上的消融实验（置信度 0.98）提供了决定性证据。当关闭随机化训练（$\pi = 0.0$）时，FVD 从 70 急剧恶化至 401，证明随机化条件训练对视频质量和时序一致性至关重要。在 $\pi \in \{0.0, 0.25, 0.5, 0.75\}$ 的比较中，$\pi = 0.5$ 在 LPIPS、PSNR、SSIM、FID、FVD 等全部指标上达到综合最优。

### 3. 控制信号注入的架构设计

YODA 以 **RIVER**（Davtyan et al., ICCV 2023）作为骨干视频预测模型，但关键性地修改了其条件机制。RIVER 原本不接收外部运动控制，仅条件于上下文帧。YODA 在 U-ViT 架构的瓶颈处引入交叉注意力层（cross-attention），将稀疏光流编码器输出的控制令牌序列融合到生成过程中（图 8）。

**设计考量**：选择在 U-ViT 瓶颈处而非浅层注入控制信号，使得控制信息能够与经过深层抽象的视觉表征进行交互，既保证了控制信号的全局影响力，又避免了干扰低层纹理细节的生成。这一设计与受限感受野编码器形成协同：编码器保证控制信号的空间局部性，交叉注意力机制则负责将局部控制信号映射到对应物体的完整运动模式。

**与基线的本质差异**：YODA 并非简单地在 RIVER 上添加条件输入，而是通过“受限编码器 + 随机化训练 + 瓶颈交叉注意力”的三位一体设计，实现了从“视频预测”到“多物体可控生成”的质变。这使得 YODA 在 BAIR 数据集上以仅 5 个控制点的稀疏输入，即超越了所有先前可控视频生成方法（LPIPS 0.112, FID 18.2, FVD 264，表 2），且无需任何物体标注或前景/背景先验。

### 4. 控制点数量的权衡

控制向量数量 $n_c$ 的选择揭示了控制精度与交互建模之间的根本权衡（图 4、图 5）。$n_c = 5$ 被证明是最优设置：
- **过少（$n_c = 1$）**：局部误差（控制响应精度）较高，模型对控制的响应不足。
- **过多（$n_c = 100$）**：全局误差（非控制区域的运动泄漏）增大，模型过度关注控制信号，削弱了物体间交互的建模能力，且推理时需要更多控制点以弥合训练-测试分布差异。
- **$n_c = 5$**：在局部误差和全局误差之间达到最佳平衡，既保证了精准的控制响应，又维持了自然的物体交互。

这一发现本身构成了方法设计的重要洞察：稀疏控制不仅是计算效率的考量，更是迫使模型学习解耦物体运动与交互的必要条件。



![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/012_Figure_8.jpg]]
*Figure 8: Overview of YODA’s architecture. The noisy target frame x , the reference frame $x ^ { \tau - 1 }$ and the context frame $x ^ { c }$ are concatenated, reshaped and projected to form a sequence of visual tokens that is augmented with position encodings and embedded relative temporal distance (τ −c) between frames and fed to the U-ViT (Bao et al. 2022) alongside with the embedded time token (t). A sequence of control tokens is fused into the pipeline via cross-attention in the bottleneck of the network*

YODA 的整体 pipeline 围绕一个核心目标构建：在给定当前帧、历史上下文帧以及稀疏运动控制信号的条件下，通过流匹配生成下一帧，从而实现对多物体场景中每个物体的独立运动控制。其架构由四个关键模块串联而成，形成“编码—条件注入—速度场预测—解码”的生成闭环。

**输入与潜在空间压缩。** 原始 RGB 帧首先通过一个预训练的 VQ-GAN 自编码器压缩到离散潜在空间，以降低后续流匹配在高分辨率下的计算开销。VQ-GAN 按数据集独立训练，其损失函数结合了重建损失、码本承诺损失与对抗损失（见附录 B）。压缩后的潜在码 $x$ 作为 YODA 主干网络的输入令牌。

**条件信号的构建与注入。** YODA 同时接收三类条件信息：
1. **视觉上下文**：将带噪目标帧 $x$、参考帧 $x^{\tau-1}$ 和上下文帧 $x^c$ 在通道维拼接，经投影形成视觉令牌序列，并附加位置编码与帧间相对时间间隔 $\tau-c$ 的嵌入。
2. **时间条件**：流匹配的时间步 $t$ 经嵌入后作为时间令牌。
3. **稀疏运动控制**：从预训练的 RAFT 光流估计器中获取密集光流场，按运动幅度采样少量像素点（通常 $n_c=5$）作为控制输入。这些稀疏光流向量被送入一个精心设计的受限感受野编码器——将光流场划分为 $16\times16$ 网格，每个网格独立通过 5 层 MLP 处理，再与可学习的位置编码组合，最终输出 256 维的控制令牌序列。

控制令牌通过交叉注意力层在 U-ViT 的瓶颈处与视觉令牌融合，而非在输入端直接拼接。这一设计使得运动控制信号能够在网络最深层次影响速度场的预测。

**U-ViT 主干与流匹配推理。** 主干网络沿用 RIVER 的 U-ViT 架构，包含 8 个外层自注意力块和 5 个瓶颈交叉注意力块（见 Figure 8）。网络以拼接后的视觉令牌、时间令牌和控制令牌为输入，输出速度场 $v_t$ 的预测值。训练时，速度场通过流匹配目标函数

$$\mathcal{L}_{\mathrm{F}}(\boldsymbol{\theta}) = \| v_t(\boldsymbol{x} | \boldsymbol{x}^{\tau-1}, \boldsymbol{x}^c, \tau-c, a^{\tau-1}; \boldsymbol{\theta}) - u_t(\boldsymbol{x} | \boldsymbol{x}^{\tau}) \|^2$$

进行监督，其中 $u_t$ 为高斯概率路径下的闭合形式目标向量场。推理时，从标准高斯噪声出发，通过 ODE 求解器沿预测速度场逐步积分，生成下一帧的潜在码，再经 VQ-GAN 解码器重建为 RGB 图像。

**随机化条件训练策略。** YODA 的关键训练技巧是以概率 $\pi=0.5$ 随机丢弃上下文帧或控制信号（见 Algorithm 1）。这一策略迫使模型在无法依赖某类条件时仍能生成合理帧，从而隐式地解耦了物体运动与场景上下文，是实现独立物体控制与交互建模的核心机制。消融实验表明，关闭随机化（$\pi=0$）会导致 FVD 从 70 急剧恶化至 401（Table 1），验证了该策略的决定性作用。



### 问题形式化与条件分布

YODA 将可控视频生成建模为从条件分布中采样：

$$p ( x ^ { k + 1 } | x ^ { k } , x ^ { k - 1 } , \ldots , x ^ { 1 } , a ^ { k } )$$

其中 $x^{k+1}$ 为待生成的下一帧，$x^{k}, x^{k-1}, \ldots, x^{1}$ 为当前帧与历史上下文帧，$a^{k}$ 为运动控制输入。核心目标是使模型能够根据稀疏的运动控制信号，独立操纵场景中的不同物体。

### 流匹配基础

YODA 以 **RIVER**（Davtyan et al., ICCV 2023）为骨干，采用条件流匹配（conditional flow matching）框架。其核心思想是通过一个连续归一化流将简单先验分布（标准高斯）逐步推至数据分布：

$$\dot { \phi } _ { t } ( y ) = v _ { t } ( \phi _ { t } ( y ) ) , \quad \phi _ { 0 } ( y ) = y$$

训练目标是让可学习的速度场 $v_t$ 逼近一个解析的目标向量场 $u_t$：

$$\operatorname* { m i n } _ { v _ { t } } \ \mathbb { E } _ { t , p _ { t } ( y \mid y _ { 1 } ) , q ( y _ { 1 } ) } \| v _ { t } ( y ) - u _ { t } ( y \mid y _ { 1 } ) \| ^ { 2 }$$

其中目标向量场在假设高斯概率路径时具有闭合形式：

$$u _ { t } ( y | y _ { 1 } ) = \frac { y _ { 1 } - ( 1 - \sigma _ { \operatorname* { m i n } } ) y } { 1 - ( 1 - \sigma _ { \operatorname* { m i n } } ) t }$$

$\sigma_{\min}$ 是一个小常数，用于保证数值稳定性。

### 骨干网络：RIVER 的条件流匹配

RIVER 的基础训练损失为：

$$\mathcal { L } _ { \mathrm { R } } ( \theta ) = \| v _ { t } ( x | x ^ { \tau - 1 } , x ^ { c } , \tau - c ; \theta ) - u _ { t } ( x | x ^ { \tau } ) \| ^ { 2 }$$

其中 $x^{\tau-1}$ 为参考帧（前一帧），$x^c$ 为上下文帧（从历史帧中采样的一个子集，用于提供记忆），$\tau-c$ 为帧间时间间隔的嵌入。该损失使模型学会从过去帧预测未来帧的速度场。

### YODA 的运动控制损失

YODA 在 RIVER 损失中引入运动控制信号 $a^{\tau-1}$，得到运动控制损失：

$$\mathcal { L } _ { \mathrm { F } } ( \boldsymbol { \theta } ) = \| v _ { t } ( \boldsymbol { x } | \boldsymbol { x } ^ { \tau - 1 } , \boldsymbol { x } ^ { c } , \tau - c , a ^ { \tau - 1 } ; \boldsymbol { \theta } ) - u _ { t } ( \boldsymbol { x } | \boldsymbol { x } ^ { \tau } ) \| ^ { 2 }$$

该损失使速度场预测同时依赖于过去帧和运动控制信号。控制信号的注入方式是在 U-ViT 的瓶颈处，将自注意力层替换为交叉注意力层，使控制令牌与视觉令牌进行交互（见 Figure 8）。

### 稀疏光流编码器：受限感受野设计

控制信号 $a^{\tau-1}$ 的来源是对预训练光流估计器（RAFT）输出的密集光流场进行稀疏采样——仅选取 $n_c$ 个像素位置（典型值 $n_c=5$）的位移向量。这些稀疏光流被编码的方式是 YODA 实现独立物体控制的关键。

编码器设计（见 Figure 2）：
- 将稀疏光流场平铺为 $16 \times 16$ 的网格；
- 每个网格块**独立地**通过一个 5 层 MLP（含批归一化和 GELU 激活）编码；
- 编码后的向量与可学习的位置编码相加，形成 256 维的控制令牌。

**设计动机**：网格化独立 MLP 限制了每个控制令牌的感受野，使其只能感知局部区域的运动信息。这迫使模型将局部像素位移与对应物体的整体运动关联起来，而非依赖全局上下文进行“作弊式”的运动传播。消融实验（Figure 3）表明，相比卷积编码器（大感受野），该设计不仅降低了局部误差的均值，且消除了大误差的长尾分布。

### 随机化条件训练策略

YODA 在训练时以概率 $\pi$ 随机丢弃条件信号（即同时丢弃上下文帧 $x^c$ 和控制信号 $a^{\tau-1}$）。这一策略迫使模型在条件缺失时仍能生成合理的视频，同时在条件存在时充分利用控制信号。实验表明 $\pi=0.5$ 在 LPIPS、PSNR、SSIM、FID、FVD 上综合最优（Table 1），其核心机制是隐式地实现了物体分离与交互预测的解耦学习。

### 潜在空间压缩

为加速高分辨率视频训练，YODA 使用预训练的 VQ-GAN 自编码器将图像压缩到离散潜在空间。VQ-GAN 的训练损失为：

$$\mathcal { L } _ { \mathrm { V Q } } ( E , G , Z ) = \| x - \hat { x } \| ^ { 2 } + \| \mathrm { s g } [ E ( x ) ] - z _ { q } \| ^ { 2 } + \| \mathrm { s g } [ z _ { q } ] - E ( x ) \| ^ { 2 }$$

配合对抗损失 $\mathcal { L } _ { \mathrm { G A N } } ( E , G , Z , D ) = \log D ( x ) + \log ( 1 - D ( \hat { x } ) )$ 以提升感知质量。不同数据集的 VQ-GAN 配置见 Table 5。



## 实验与关键发现

### 主实验结果

YODA 在三个标准数据集上进行了系统评估，并与多个可控视频生成基线进行了定量比较。

**BAIR 数据集**（Table 2）：YODA 以仅 5 个控制点（$n_c=5$）的设置，在所有指标上超越了全部先前方法。具体而言，YODA 取得 LPIPS 0.112、FID 18.2、FVD 264，相比此前最强的随机视频预测方法 SAVP+（LPIPS 0.154, FID 27.2, FVD 303）均有显著提升。值得注意的是，YODA 并未使用任何前景/背景先验或物体标注，而 iPOKE 利用了背景掩码——在此差异下 YODA 仍展现出更强的综合性能。

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/008_Table_2.jpg]]
*Table 2: Evaluation on the BAIR dataset*

**CLEVRER 数据集**（Table 1）：在随机化条件训练（$\pi=0.5$）下，YODA 以 5 个控制点取得 FVD 70。当关闭随机化训练（$\pi=0.0$）时，FVD 剧增至 401，清晰揭示了随机化条件策略对视频质量的因果性影响。

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/004_Table_1.jpg]]
*Table 1: Evaluation of the generated videos on CLEVRER under different input sparsity (nc) and randomization (π)*

**iPER 数据集**（Table 3）：YODA 在人体运动模拟任务上的 FVD 优于除 iPOKE 外的所有基线方法。考虑到 iPOKE 利用了额外的背景先验，YODA 在无先验条件下的表现已具竞争力。

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/010_Table_3.jpg]]
*Table 3: Evaluation on the iPER dataset*

### 消融实验

#### 控制点数量 $n_c$ 的权衡

Figure 4 和 Figure 5 揭示了控制向量数量 $n_c$ 在局部误差（控制响应精度）与全局误差（非控制区域的运动泄漏）之间的核心权衡。在 BAIR 数据集上，$n_c=1$ 时模型对交互建模良好，但缺乏对背景物体的控制；$n_c=100$ 时背景控制能力增强，但交互建模质量下降，且推理时需提供更多控制点以弥合训练-测试分布差异。$n_c=5$ 在两者之间达到最优平衡：局部误差低（控制精度高），同时全局误差维持在较低水平（非目标物体保持静止）。

#### 随机化条件训练的关键作用

Table 1 系统比较了随机条件丢弃概率 $\pi \in \{0.0, 0.25, 0.5, 0.75\}$ 的效果。$\pi=0.5$ 在 LPIPS、PSNR、SSIM、FID、FVD 五项指标上综合最优。该策略迫使模型在训练中同时学会利用上下文帧（用于时序一致性）和控制信号（用于运动响应），从而隐式地实现了物体分离与交互预测。当 $\pi=0.0$ 时，模型过度依赖控制信号，导致视频质量严重退化。

#### 受限感受野光流编码器的设计验证

Figure 3 通过小提琴图对比了卷积编码器（大感受野）与 YODA 网格化独立 MLP 编码器（受限感受野）的局部误差分布。结果表明：受限感受野编码器不仅降低了整体平均误差，且误差分布更集中于小数值区域；相比之下，卷积编码器呈现出明显的大误差长尾。Figure 9 进一步定性展示了差异：使用卷积编码器时，机械臂的运动与控制输入存在不期望的全局相关性，而受限感受野编码器有效隔离了不同物体的运动控制。

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/013_Figure_9.jpg]]
*Figure 9: The effect of our encoder with restricted receptive field. Notice, how the motion of the robotic hand is correlated to the input control in the case of convolutional encoder. To play videos, use Acrobat Reader*

### 可控性分析

Figure 6 展示了 CLEVRER 数据集上控制向量与生成光流之间的平均余弦误差及 95% 置信区间，按控制幅度和方向分组。结果表明 YODA 对不同幅度和方向的控制输入均能准确响应。

Table 4 评估了模型在分布外控制输入下的鲁棒性：YODA 在机械臂场景中的局部控制误差为 3.37 像素，相比基线展现出更强的分布偏移适应能力。

### 失败模式与局限性

1. **光流估计依赖**：控制信号的质量受预训练 RAFT 光流估计器精度限制，在纹理稀疏或运动模糊区域可能出现控制偏差。
2. **控制形式受限**：当前仅支持 2D 平移位移，对于旋转、形变或遮挡等复杂交互难以精确表达。
3. **交互式生成负担**：用户需持续为每个物体逐帧指定运动，自动化程度有限。
4. **计算开销**：训练需约 3 天（4×RTX 3090），BAIR 256×256 分辨率下 GPU 内存需求达 21 GB，限制了更广泛的应用部署。
5. **泛化能力未验证**：模型在训练数据未见过的全新场景或物体上的表现尚不明确，需进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/019_Figure_14.jpg]]
*Figure 14: From left to right: the input image, the optical flow between the input image and the next one, the estimated mask. The red arrows in the images in the first column show the control input*

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/011_Figure_7.jpg]]
*Figure 7: In each column YODA is given the controls indicated as red arrows. Starting from the same frame, YODA generates diverse videos, following accurately the magnitude (1st and 2nd videos) and direction (1st to 3rd videos) of the motion control input, as well as multiple inputs (4th video). Notice that since YODA has memory and was trained also to generate frames without control, it can learn to propagate motion across many frames from a single initial control input. To play videos, use Acrobat Reader. Table 4: Local error in pixels of the control applied to the robot arm. Average of 5 runs is reported*

![[assets/figures/papers/paper_list_l6_Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Vi/figures/016_Table_5.jpg]]
*Table 5: Configurations of VQGAN (Esser, Rombach, and Ommer 2021) for different datasets*



## 定位与知识库关联

### 核心思路与关键设计

YODA 的核心目标是在**无监督条件下实现多物体场景的稀疏运动控制**。现有可控视频生成方法通常依赖物体标注（如边界框、分割掩码）或仅限于单物体场景，这构成了领域的主要瓶颈。YODA 通过三个关键设计突破这一限制：

1. **稀疏运动控制信号**：从预训练光流估计器（RAFT）输出的密集光流场中，按运动幅度采样少量像素点（通常仅 5 个）作为控制输入，用户只需指定这些点的 2D 位移向量即可操控对应物体的运动。
2. **受限感受野的光流编码器**：将稀疏光流场划分为 16×16 网格，每个网格独立通过 5 层 MLP 编码为控制令牌，再与可学习的位置编码融合。这种设计刻意限制了编码器的感受野，迫使模型将局部像素位移关联到完整物体的运动，而非学习全局运动模式。
3. **随机化条件训练**：以概率 π = 0.5 随机丢弃上下文帧或控制信号，使模型必须同时利用两种信息才能生成合理视频。这一策略隐式地实现了物体分离与交互预测的解耦——当控制信号缺失时，模型依赖上下文帧推断运动；当上下文帧缺失时，模型必须严格遵循控制信号。

### 与基线方法的关系

YODA 以 **RIVER**（Davtyan et al., ICCV 2023）为骨干网络。RIVER 是一个基于条件流匹配（conditional flow matching）的视频预测模型，工作在预训练 VQ-GAN 的离散潜在空间中，通过 U-ViT 架构预测速度场。YODA 对 RIVER 的改造体现在三个层面：

- **控制信号注入**：RIVER 仅条件于上下文帧，不接收外部运动控制。YODA 在 U-ViT 瓶颈处引入交叉注意力层，将稀疏光流编码器输出的控制令牌融合到速度场预测中（Figure 8）。
- **光流编码器设计**：与 **iPOKE**（Blattmann et al., ICCV 2021）使用卷积编码器处理整个稀疏光流不同，YODA 采用网格化独立 MLP 编码器。消融实验（Figure 3）表明，卷积编码器因感受野过大导致局部误差分布存在明显长尾（大误差频繁出现），而受限感受野的 MLP 编码器不仅降低了平均局部误差，还消除了大误差长尾，是实现独立物体控制的关键。
- **训练策略**：标准条件训练总是提供上下文帧，YODA 引入随机化丢弃机制（Algorithm 1），在 CLEVRER 数据集上，无随机化训练（π = 0.0）导致 FVD 从 70 剧增至 401（Table 1），证明了随机化对视频质量和时间一致性的决定性作用。

其他对比基线包括：**CADDY**（Menapace et al., CVPR 2021）基于离散动作代码进行控制，**GLASS**（Davtyan and Favaro, ECCV 2022）解耦全局与局部动作，**MoCoGAN**（Tulyakov et al., CVPR 2018）和 **SAVP**（Lee et al., 2018）为经典视频生成/预测方法。这些方法均未实现无标注条件下的稀疏多物体独立控制。

### 关键权衡与消融发现

控制向量数量 $n_c$ 存在根本性权衡（Figure 4, Figure 5）：

- **局部误差（控制精度）**：$n_c$ 过小时，模型对控制信号的响应不足，无法精确操控目标物体。
- **全局误差（非控制区域运动泄漏）**：$n_c$ 过大时，模型倾向于学习全局运动模式，导致非目标物体也被意外移动，且难以建模物体间交互。

$n_c = 5$ 在两个指标之间达到最佳平衡。这一发现揭示了稀疏控制的核心矛盾：控制信号过少则信息不足，过多则破坏物体分离的隐式学习。

### 适用边界与局限

1. **控制形式受限**：YODA 仅支持 2D 平移位移控制，对于旋转、形变、遮挡等复杂交互难以精确表达。控制信号的精度受限于预训练 RAFT 光流估计器的质量。
2. **泛化能力未验证**：模型在训练数据未见过的全新场景或物体类别上的表现尚未评估，可能存在过拟合训练分布的风险。
3. **交互式生成依赖人工**：用户需要持续为每个物体指定逐帧运动，自动化程度低。能否将像素位移控制泛化到语义层面的控制（如文本指令）是重要的开放问题。
4. **计算开销较大**：训练依赖 VQ-GAN 自编码器和 U-ViT 主干网络，在 4 块 RTX 3090 GPU 上需约 3 天完成训练，最大显存需求达 21 GB（BAIR 256×256）。
5. **多控制冲突行为未知**：当多个控制点对同一物体施加相反运动时，模型的行为尚未被系统研究。

### 开放问题与潜在延伸

- **自监督控制编码**：能否在完全没有光流标签的情况下，通过自监督方式学习控制编码，从而摆脱对预训练光流估计器的依赖？
- **隐式物体注意力的显式化**：YODA 学到的交叉注意力图（Figure 13）粗略覆盖了物体区域，能否将其显式用于 zero-shot 分割或跟踪等下游任务？
- **复杂真实场景的可行性**：该方法在自动驾驶、人群视频等更混乱的真实场景中是否仍然有效，需要进一步验证。
- **控制冲突的解析**：模型如何处理多个控制输入之间的冲突（如两个控制点给同一物体相反的运动），其内部决策机制值得深入探索。



## 原文 PDF

![[paperPDFs/AAAI_2024/Learn_the_Force_We_Can_Enabling_Sparse_Motion_Control_in_Multi_Object_Video_Generation.pdf]]

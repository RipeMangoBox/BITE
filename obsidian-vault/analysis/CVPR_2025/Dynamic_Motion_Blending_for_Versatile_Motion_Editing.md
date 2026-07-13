---
title: Dynamic Motion Blending for Versatile Motion Editing
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Dynamic_Motion_Blending_for_Versatile_Motion_Editing.pdf
project_link: https://awfuact.github.io/motionrefit/
code_link: null
aliases:
- DMBVME
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在线动态生成训练三元组的MotionCutMix增强技术，以及带有运动协调器的自回归扩散模型架构。
primary_logic: 通过MotionCutMix利用海量未标注运动数据在线合成多样化训练三元组，有效扩展训练分布并提升模型对未见组合的泛化能力；自回归框架分解长序列降低学习难度，运动协调器解决混合运动合成中的身体不协调问题。
claims:
- MotionCutMix是一种在线数据增强技术，通过依据输入文本动态混合身体部位运动生成训练三元组。
- MotionReFit是一个带有运动协调器的自回归扩散模型。
- 自回归架构通过分解长序列促进学习收敛。
- 运动协调器减轻了运动组合时产生的伪影和不协调。
---

# Dynamic Motion Blending for Versatile Motion Editing

> [!tip] 核心洞察
> 通过MotionCutMix利用海量未标注运动数据在线合成多样化训练三元组，有效扩展训练分布并提升模型对未见组合的泛化能力；自回归框架分解长序列降低学习难度，运动协调器解决混合运动合成中的身体不协调问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 动态运动融合：面向多样化运动编辑 |
| 英文题名 | Dynamic Motion Blending for Versatile Motion Editing |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2025/html/Jiang_Dynamic_Motion_Blending_for_Versatile_Motion_Editing_CVPR_2025_paper.html) · [Project](https://awfuact.github.io/motionrefit/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionReFit |
| Dataset | STANCE Body Part Replacement, STANCE Style Transfer |

> [!tip] 效果简介
> - STANCE Body Part Replacement 上，FID 0.20 (Ours full) vs TMED：更高（质量更差） (显著下降，达到更优自然度)。
> - STANCE Style Transfer 上，FID 0.14 (Ours full) vs TMED：更高（质量更差） (显著下降，风格迁移更接近真实数据分布)。

## 概要

**问题瓶颈**：现有文本引导的运动编辑方法高度依赖预收集的少量三元组（原始运动、编辑后运动、编辑指令），这导致它们在风格迁移、未见组合等多样化编辑场景中泛化能力严重不足。训练数据的有限分布成为制约通用性的核心瓶颈。

**核心方案**：本文提出 **MotionReFit**——一个面向通用运动编辑的自回归扩散框架，并配套提出 **MotionCutMix** 在线数据增强策略。MotionCutMix 利用大规模未标注运动数据库，通过依据输入文本动态混合不同身体部位的运动，在线合成大量训练三元组，从而显著扩展训练分布。MotionReFit 采用自回归架构将长序列分解为滑动窗口逐段生成，降低学习难度；同时引入运动协调器作为判别器，在扩散采样阶段提供分类器引导，消除混合运动中的身体不协调伪影。

**方法定位**：MotionReFit 属于条件扩散生成方法，在架构层面将非自回归扩散推进为自回归范式，在数据层面用在线增强替代固定的三元组训练。与 **MDM**（Tevet et al., ICLR 2022）等基线相比，该方法仅需原始运动序列和文本指令作为输入，无需额外指定编辑部位。

**主要结果**：在 STANCE 数据集的身体部位替换任务上，MotionReFit 的 FID 降至 0.20；在风格迁移任务上 FID 降至 0.14，均显著优于基线方法。消融实验表明，即使不使用 MotionCutMix，自回归架构本身已优于 TMED 和 MDM-BP；增加 MotionCutMix 比例可持续提升指令遵循度而不影响收敛；运动协调器的移除会导致 FID 升高并出现同侧肢体同步前移等不自然模式。

**局限性提示**：该方法对极长序列的长期时间依赖处理能力仍有限，对位置相关指令的空间敏感度不足，且在极端身体部位组合下协调器仍可能出现罕见的协调误差。

### 问题背景

文本引导的运动编辑旨在根据自然语言指令修改人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。然而，这一任务面临两个核心挑战：**运动表示的高维连续性**与**自然语言指令的语义歧义性**。现有方法通常将运动编辑建模为条件生成问题，以原始运动和编辑指令为条件，生成符合语义的编辑后运动。

### 现有方法的瓶颈

当前文本引导运动编辑方法存在一个根本性瓶颈：**严重依赖有限的预收集三元组数据**（原始运动、编辑后运动、编辑指令）。这些三元组的收集成本极高——需要专业动捕设备、人工标注以及运动编辑师反复调整——导致训练数据规模受限，难以覆盖多样化的编辑场景。具体而言：

- **风格编辑泛化不足**：现有数据集（如HumanML3D）主要包含动作类型标注，缺乏对运动风格（如“疲惫地行走”、“优雅地挥手”）的系统覆盖，使得模型在风格迁移任务上表现不佳。
- **未见组合能力薄弱**：当编辑指令涉及训练数据中未出现的身体部位组合（如“左手画圈的同时右脚踢腿”）时，模型往往产生不自然的运动伪影。
- **数据利用效率低下**：大规模未标注运动数据库（如AMASS）包含丰富的运动多样性，但现有方法无法有效利用这些数据来扩展编辑能力。

### 现有方法的架构局限

除数据瓶颈外，现有方法在架构设计上也存在不足。以**MDM**（Tevet et al., ICLR 2022）为代表的非自回归扩散模型一次性生成完整运动序列，在处理长序列编辑时面临学习难度大、收敛缓慢的问题。此外，这些方法缺乏显式的身体协调机制，在混合不同来源的身体部位运动时容易产生肢体同步不自然的伪影（如同侧手臂和腿同时前移）。

### 本文动机

针对上述瓶颈，本文提出两个核心创新：

1. **MotionCutMix在线数据增强**：通过动态混合身体部位运动，利用海量未标注运动数据在线合成多样化训练三元组，有效扩展训练分布并提升模型对未见组合的泛化能力。
2. **MotionReFit自回归扩散架构**：采用自回归框架逐段生成长序列以降低学习难度，并引入运动协调器通过判别器引导消除混合运动中的身体不协调问题。

这一组合策略旨在突破标注数据规模的限制，实现通用且鲁棒的运动编辑。

## 核心方法与创新机理

MotionReFit 的核心创新围绕一个因果性瓶颈展开：**现有文本引导运动编辑方法严重依赖固定的预收集三元组（原始运动、编辑后运动、编辑指令），导致训练分布狭窄，难以泛化到风格迁移、细粒度调整等多样化编辑场景**。为突破这一瓶颈，本文从数据增强策略和模型架构两个维度进行了系统性改造。

### 1. 在线数据增强：MotionCutMix

传统方法（如 **MDM**，Tevet et al., ICLR 2022；**TMED**）仅使用固定预收集的编辑三元组进行训练，数据规模与多样性受限于标注成本。MotionCutMix 将训练模式从“静态三元组学习”转变为“在线动态合成学习”：在训练过程中，依据输入文本指令，从大规模未标注运动数据库中动态选取目标运动，并通过空间运动混合（Spatial Motion Blending）将源运动与目标运动的身体部位进行组合，实时生成新的“原始-编辑后”运动对。

空间混合的核心机制是**硬掩码与软掩码的分层控制**。对于需要完全替换的关节（如“将手臂动作改为挥手”），硬掩码关节直接采用目标运动的旋转参数；对于过渡区域的关节，软掩码关节使用球面线性插值（SLERP）在源旋转与目标旋转之间进行平滑混合，插值系数 $\alpha$ 控制混合程度；其余关节则保留源运动不变。这一规则可形式化表示为：

$$
\left\{ \begin{array} { l l } \mathbf{r}_j^{\mathrm{bld}} = \mathbf{r}_j^{\mathrm{tgt}} & \mathrm{~if~} j \in \mathbf{M}_{\mathrm{hard}} \\ \mathbf{r}_j^{\mathrm{bld}} = \mathrm{SLERP}(\mathbf{r}_j^{\mathrm{src}}, \mathbf{r}_j^{\mathrm{tgt}}, \alpha) & \mathrm{~if~} j \in \mathbf{M}_{\mathrm{soft}} \\ \mathbf{r}_j^{\mathrm{bld}} = \mathbf{r}_j^{\mathrm{src}} & \mathrm{otherwise} \end{array} \right.
$$

混合运动的全局属性（朝向 $\phi^{\mathrm{bld}}$ 和位移 $\mathbf{t}^{\mathrm{bld}}$）由下半身运动决定，以保证整体运动的物理合理性。通过这一机制，MotionCutMix 从 $N_S$ 个标注三元组出发，利用包含 $N_L$ 条运动的大规模数据库，可有效创造出 $N_L \times N_S$ 个增强编辑对，显著扩展了训练分布。

消融实验证实了这一创新的决定性作用：增加 MotionCutMix 的混合比例持续提升编辑指令遵循度（AvgR 指标），且不影响训练收敛；使用 MotionCutMix 的模型在标注数据大幅减少时仍能保持强性能，表明其有效降低了对昂贵标注的依赖。

### 2. 自回归扩散架构与运动协调器

在生成架构层面，MotionReFit 将传统的非自回归扩散（一次性生成完整序列）改为**自回归扩散模型**。长运动序列被分解为滑动窗口片段逐段生成，降低了单次生成的学习难度，促进了训练收敛。消融实验表明，即使不使用 MotionCutMix 增强，自回归架构本身已优于 TMED 和 MDM-BP 等基线方法。滑动窗口的最佳长度经实验确定为 16 帧。

然而，逐段生成和空间混合合成引入了一个新的质量风险：不同来源的身体部位组合后可能出现**不自然的肢体同步**（例如同侧手臂与腿同时前移）。为解决这一问题，MotionReFit 引入了一个**身体部位协调器**——一个训练用于识别“由多个源运动拼接而成”的合成运动片段的判别器。在自回归采样的最后 20 步，该判别器通过分类器引导对扩散模型的输出进行梯度修正：

$$
\tilde{\mathcal{M}}_0 = \hat{\mathcal{M}}_0 + \lambda \nabla_{\hat{\mathcal{M}}_0} D(\hat{\mathcal{M}}_0)
$$

其中 $\hat{\mathcal{M}}_0$ 为模型预测的干净运动，$D$ 为判别器，$\lambda$ 为引导强度。消融实验显示，移除身体部位协调器会导致运动 FID 升高，并出现同侧肢体同步前移等伪影；加入协调器后可有效消除这些不自然模式。

### 3. 输入条件的简化

与需要额外指定编辑部位掩码或行为标签的基线方法不同，MotionReFit **仅需原始运动序列和文本编辑指令作为输入**，无需任何额外的部位指定信息。这一简化降低了使用门槛，同时模型通过多模态条件编码器将关键点运动和文本指令统一编码为条件特征，使编辑过程完全由自然语言驱动。

MotionReFit 的整体设计围绕一个核心矛盾展开：如何仅凭文本指令和原始运动，生成既满足编辑要求又保持身体协调性的高质量运动。为此，框架将任务拆解为三个协同模块，形成一条“条件编码→自回归生成→协调修正”的流水线，如 Figure 4 所示。

**输入与表示。** 系统接收两路输入：原始运动序列和一段自然语言编辑指令。运动在内部以两种可互换的表示形式存在——基于 28 个关键点的表示 $\mathcal{M}^{\kappa} \in \mathbb{R}^{L \times N_K \times 3}$ 和 SMPL‑X 参数表示 $\mathcal{M}^{S} = \{\mathbf{t}, \phi, \mathbf{r}\}$。正向运动学可将 SMPL‑X 参数映射为关键点，反向则通过轻量神经网络加优化的方式完成，保证两个空间之间的信息无损流动。

**多模态条件编码器。** 原始运动的关键点序列和文本编辑指令被分别送入条件编码器，融合为统一的特征表示 $\mathcal{C}$。这一表示贯穿后续所有生成步骤，是模型理解“编辑什么”与“编辑成什么”的唯一信息入口。

**自回归运动扩散模型。** 生成过程采用滑动窗口的自回归范式。对于长运动序列，模型每次处理一个固定长度的片段（消融实验确定最优窗口为 16 帧）。当前窗口以原始运动对应片段和条件表示 $\mathcal{C}$ 为输入，通过 Transformer 骨干的扩散模型逐步去噪，生成编辑后的关键点片段。为保证片段间的运动连续性，每个窗口的前两帧保留上一窗口的生成结果，仅从第三帧开始施加扩散噪声。扩散过程遵循标准的前向加噪马尔可夫链：

$$q(\mathcal{M}_t | \mathcal{M}_{t-1}) = \mathcal{N}(\mathcal{M}_t; \sqrt{1 - \beta_t} \mathcal{M}_{t-1}, \beta_t \mathbf{I})$$

训练时最小化预测噪声与真实噪声的均方误差：

$$\mathcal{L} = \mathbb{E}_{\mathcal{M}_0 \sim q(\mathcal{M}_0 | \mathcal{C}), t \sim [1,T]} \|\epsilon - \epsilon_\theta(\mathcal{M}_t, t, \mathcal{C})\|_2^2$$

推理时采用无分类器引导，通过混合条件预测与无条件预测来强化对编辑指令的遵循度：

$$\tilde{\epsilon}_\theta(\mathcal{M}_t, t, \mathcal{C}) = (1 + w) \epsilon_\theta(\mathcal{M}_t, t, \mathcal{C}) - w \epsilon_\theta(\mathcal{M}_t, t, \mathcal{C}')$$

**身体部位协调器。** 自回归扩散模型生成的关键点序列，在通过 SMPL‑X 优化合并为最终运动之前，还需经过一个专门的判别器修正。该判别器在训练阶段被训练为识别由多个源运动拼接而成的合成运动片段；在推理的最后 20 步采样中，它通过分类器引导对生成结果施加梯度修正：

$$\tilde{\mathcal{M}}_0 = \hat{\mathcal{M}}_0 + \lambda \nabla_{\hat{\mathcal{M}}_0} D(\hat{\mathcal{M}}_0)$$

这一机制的核心作用是消除混合运动中常见的身体不协调伪影——例如同侧手臂与腿同步前移的非自然模式（Figure 7）。消融实验证实，移除该协调器会导致 FID 显著升高。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2025_html_Jiang_Dynamic_Motion_B/figures/009_Figure_7.jpg]]
*Figure 7: Impact of body part coordinator on motion quality. Examples show paired results using identical random seeds, highlighting how coordinator prevents unnatural synchronous movements of same-side limbs (arm and leg moving forward together)*

**输出闭环。** 经协调器修正后的关键点序列最终通过 SMPL‑X 优化还原为完整的参数化运动，输出编辑后的运动序列。整个流程无需额外指定编辑部位掩码或行为标签，仅依赖原始运动与文本指令即可完成从局部替换到全局风格迁移的多样化编辑任务。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2025_html_Jiang_Dynamic_Motion_B/figures/001_Figure_1.jpg]]
*Figure 1: MotionReFit, a universal framework for motion editing that handles various scenarios simply from textual guidance, offering both spatial and temporal editing capabilities. MotionReFit is supercharged with our proposed MotionCutMix training strategy, which leverages large-scale unannotated motion databases to augment the scarce motion editing triplets, enabling robust and generalizable editing*

### 运动表示与空间混合

MotionReFit 采用两种可互换的运动表示。基于关键点的表示 $\mathcal{M}^{\kappa} \in \mathbb{R}^{L \times N_K \times 3}$ 以序列长度 $L$ 和 $N_K=28$ 个身体关键点刻画运动；基于 SMPL-X 参数的表示 $\mathcal{M}^{S} = \{\mathbf{t}, \phi, \mathbf{r}\}$ 则包含根位移 $\mathbf{t}$、全局朝向 $\phi$ 和身体姿态旋转 $\mathbf{r}$。二者通过正向运动学（Forward Kinematics）和轻量神经网络加优化的逆映射实现互转。

空间运动混合是 MotionCutMix 数据增强的核心操作。对于源运动 $\mathcal{M}_{\mathrm{src}}$ 和目标运动 $\mathcal{M}_{\mathrm{tgt}}$，混合后的关节旋转 $\mathbf{r}_j^{\mathrm{bld}}$ 由以下规则决定：

$$
\left\{ \begin{array} { l l } 
\mathbf{r}_j^{\mathrm{bld}} = \mathbf{r}_j^{\mathrm{tgt}} & \mathrm{~if~} j \in \mathbf{M}_{\mathrm{hard}} \\[4pt]
\mathbf{r}_j^{\mathrm{bld}} = \mathrm{SLERP}(\mathbf{r}_j^{\mathrm{src}}, \mathbf{r}_j^{\mathrm{tgt}}, \alpha) & \mathrm{~if~} j \in \mathbf{M}_{\mathrm{soft}} \\[4pt]
\mathbf{r}_j^{\mathrm{bld}} = \mathbf{r}_j^{\mathrm{src}} & \mathrm{otherwise}
\end{array} \right.
$$

其中 $\mathbf{M}_{\mathrm{hard}}$ 为硬掩码关节集合（直接替换为目标运动），$\mathbf{M}_{\mathrm{soft}}$ 为软掩码关节集合（通过球面线性插值 SLERP 以参数 $\alpha$ 平滑过渡），其余关节保留源运动。混合运动的全局属性——朝向 $\phi^{\mathrm{bld}}$ 和位移 $\mathbf{t}^{\mathrm{bld}}$——由下半身运动决定，以确保运动轨迹的物理合理性。

### 自回归运动扩散模型

模型以自回归方式逐段生成编辑后的运动。对于每个滑动窗口内的编辑运动片段 $\mathcal{M}_0$，前向扩散过程通过 $T$ 步马尔可夫链逐步添加高斯噪声：

$$
q(\mathcal{M}_t | \mathcal{M}_{t-1}) = \mathcal{N}(\mathcal{M}_t; \sqrt{1 - \beta_t} \mathcal{M}_{t-1}, \beta_t \mathbf{I})
$$

其中 $\beta_t$ 为噪声调度参数。模型以原始运动关键点和文本编辑指令为条件 $\mathcal{C}$，通过 Transformer 架构的噪声预测网络 $\epsilon_\theta$ 学习逆向去噪。训练损失为预测噪声与真实添加噪声之间的均方误差：

$$
\mathcal{L} = \mathbb{E}_{\mathcal{M}_0 \sim q(\mathcal{M}_0 | \mathcal{C}), t \sim [1,T]} \|\epsilon - \epsilon_\theta(\mathcal{M}_t, t, \mathcal{C})\|_2^2
$$

为保证长序列的片段间连续性，每个窗口的前两帧保留原始运动，噪声仅从第三帧开始施加。推理时采用无分类器引导强化指令遵循度：

$$
\tilde{\epsilon}_\theta(\mathcal{M}_t, t, \mathcal{C}) = (1 + w) \epsilon_\theta(\mathcal{M}_t, t, \mathcal{C}) - w \epsilon_\theta(\mathcal{M}_t, t, \mathcal{C}')
$$

其中 $w$ 为引导强度，$\mathcal{C}'$ 为弱化条件的对照输入。

### 身体部位协调器

运动协调器以判别器 $D$ 的形式实现，专门训练以识别由多个源运动合成的运动片段。在自回归采样的最后 20 步，利用该判别器的梯度对模型输出 $\hat{\mathcal{M}}_0$ 进行修正：

$$
\tilde{\mathcal{M}}_0 = \hat{\mathcal{M}}_0 + \lambda \nabla_{\hat{\mathcal{M}}_0} D(\hat{\mathcal{M}}_0)
$$

其中 $\lambda$ 为引导步长。这一分类器引导机制直接作用于去噪过程中的运动表示，有效抑制了合成运动中间侧手臂与腿同步前移等不自然的身体协调伪影。消融实验证实，移除身体部位协调器（w/o BC）会导致 FID 升高，而加入后可消除此类异常同步模式（参见 Figure 7）。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2025_html_Jiang_Dynamic_Motion_B/figures/004_Figure_4.jpg]]
*Figure 4: Overview of MotionReFit. Our auto-regressive approach processes the original motion through sliding windows, where body keypoints are encoded for input to a transformer-based motion diffusion model. To ensure motion continuity, noise is applied starting from the third frame while preserving the first two frames. The model incorporates an additional token integrating the editing instruction, diffusion step, and progress indicator. The generated keypoints undergo SMPL-X optimization and merging to create the final edited motion. To enhance body part coordination, we employ a discriminator trained to identify motion segments composed of multiple source motions, which guides the denoising proce...*

## 实验与关键发现

### 主实验结果

MotionReFit 在 STANCE 基准测试的两个核心任务——身体部位替换（Body Part Replacement）与风格迁移（Style Transfer）——上均取得最优性能。表 1 报告了以 FID 和 FS 为主要指标的定量对比结果。在身体部位替换任务上，MotionReFit 完整模型（Ours full）的 FID 达到 **0.20 ± 0.025**，FS 达到 **0.97 ± 0.002**，显著优于 TMED 等基线方法。在风格迁移任务上，完整模型的 FID 达到 **0.14**，相比 TMED 有大幅下降，表明生成的运动分布更接近真实数据。

值得注意的是，即使移除 MotionCutMix 增强（Ours w/o MCM），模型性能依然优于 TMED 和 MDM-BP 等基线，这验证了自回归扩散架构本身带来的性能增益。所有结果均基于 10 次独立运行的均值和 95% 置信区间报告，确保统计可靠性。

### 消融实验

#### MotionCutMix 增强比例的影响

图 6(a, e) 展示了 MotionCutMix 混合比例对编辑指令遵循度（AvgR）的影响。结果表明，增加 MotionCutMix 比例持续提升 AvgR 指标，同时不影响训练收敛（图 6(d, h)）。这一趋势在身体部位替换和风格迁移两个任务上一致成立，证实了在线动态增强策略对扩展训练分布的有效性。

#### 标注数据量的敏感性

图 6(b, f) 分析了模型在不同标注数据规模下的性能变化。使用 MotionCutMix 的模型即使在训练数据大幅减少的情况下仍能保持强性能，而不使用该增强的模型性能随数据减少而显著下降。这表明 MotionCutMix 有效降低了对昂贵标注三元组的依赖，通过利用大规模未标注运动数据库（创造 $N_L \times N_S$ 个增强对）弥补了标注数据的稀缺性。

#### 自回归滑动窗口大小

图 6(c, g) 给出了不同时间窗口长度下的 AvgR 指标。实验确定 **16 帧**为最佳窗口大小，过长或过短的窗口均导致性能下降。过短窗口可能丢失必要的时序上下文，而过长窗口则增加了单步生成的学习难度，这与自回归框架“分解长序列以降低学习复杂度”的设计初衷一致。

#### 身体部位协调器的作用

移除身体部位协调器（w/o BC）导致 FID 升高，且生成的运动出现明显的肢体同步不自然模式。图 7 的定性对比显示，无协调器时模型倾向于产生同侧手臂与腿同步前移的伪影，而加入协调器后可有效消除此类不协调。定量上，协调器的判别器引导（在自回归采样最后 20 步施加，更新公式为 $\tilde{\mathcal{M}}_0 = \hat{\mathcal{M}}_0 + \lambda \nabla_{\hat{\mathcal{M}}_0} D(\hat{\mathcal{M}}_0)$）显著改善了运动自然度。

### 失败模式与局限性

尽管 MotionReFit 在主要指标上表现优异，分析揭示了以下局限性：

1. **长期时间依赖**：自回归框架虽然通过滑动窗口分解了长序列，但对极长序列中跨越多窗口的长期依赖关系建模能力仍有限，可能导致窗口边界处的过渡不连贯。

2. **空间敏感度不足**：模型对位置相关指令的空间理解不够精确。例如，“将右臂画圈”这类需要显式空间推理的任务，生成结果可能不完全准确。这源于当前条件编码器缺乏显式的空间关系建模机制。

3. **极端组合下的协调误差**：身体部位协调器虽然缓解了大部分不自然同步问题，但在极端运动组合（如同时替换多个远距离关节群）下，仍可能出现罕见的协调误差。这表明仅依赖判别器引导可能不足以覆盖所有边缘情况。

### 公平性说明

所有基线方法均在同一数据集划分和评估协议下进行对比，置信区间来自 10 次独立运行。需注意：实验评估未涉及不同性别、体型或残障群体的专项测试；SMPL-X 人体模型的默认体形参数可能引入一定偏向，该问题需在实际部署中手动验证。

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2025_html_Jiang_Dynamic_Motion_B/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of text-guided motion editing results. Each sequence shows the original motion alongside edits by MotionReFit and baseline methods. Motion trajectories are visualized with a color gradient from orange (starting position) to blue (ending position), with spatial offsets applied to emphasize motion differences*

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2025_html_Jiang_Dynamic_Motion_B/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison across body part replacement (upper) and style transfer (lower) tasks. Each metric reports mean over 10 evaluations with 95% confidence intervals (±). Arrows (!) indicate metrics where values closer to real data are better. Bold denotes best performance*

![[assets/figures/papers/paper_list_l7_https_openaccess_thecvf_com_content_CVPR2025_html_Jiang_Dynamic_Motion_B/figures/010_Figure_6.jpg]]
*Figure 6: Ablation analyses for body part replacement (a-d) and style transfer (e-h), reporting AvgR metrics. Edited-to-Target AvgR shown only for (d) and (h), with blue dotted lines indicating real data Edited-to-Source AvgR. Parameters studied: (a,e) MotionCutMix ratio, (b,f) annotated data volume, (c,g) temporal window size, and (d,h) convergence patterns at varying MotionCutMix ratios. All training converges within 800k steps. (a) Without body part coordinator*

## 定位与知识库关联

### 与基线方法的关系

MotionReFit 的定位是**文本引导运动编辑**，其直接对比基线为 **MDM**（Tevet et al., ICLR 2022）和 **TMED**。与传统方法相比，MotionReFit 在两个核心维度上做出了实质性改变：

- **训练数据策略**：基线方法（TMED、MDM-BP）依赖固定的预收集三元组（原始运动、编辑后运动、编辑指令），数据规模受标注成本严格限制。MotionReFit 引入 **MotionCutMix** 在线增强技术，通过空间运动混合从 $N_S$ 个标注三元组和大型运动数据库（$N_L$ 个序列）中动态合成 $N_L \times N_S$ 个增强对，从根本上扩展了训练分布。消融实验证实，即使不使用 MotionCutMix（Ours w/o MCM），自回归架构本身已优于 TMED 和 MDM-BP，表明架构改进和数据增强各自独立贡献了性能提升。

- **生成架构**：基线采用非自回归扩散，一次性生成完整运动序列，在长序列编辑场景中学习难度较高。MotionReFit 改用**自回归扩散模型**，通过滑动窗口逐段生成，将长序列分解为短片段以降低学习复杂度（最佳窗口长度经消融确定为16帧）。同时引入**运动协调器**（body part coordinator）——一个训练用于识别多源合成运动片段的判别器，在采样最后20步通过分类器引导修正生成结果，以消除身体部位间的不自然同步（如同侧手臂与腿同时前移的伪影）。

- **输入简化**：MDM-BP 等基线需要额外指定编辑部位掩码或行为标签，而 MotionReFit 仅需原始运动序列和文本编辑指令作为输入，降低使用门槛。

### 适用边界

MotionReFit 在以下场景中展现出显著优势：

- **身体部位替换**（body part replacement）：在 STANCE 数据集上，完整模型（Ours full）的 FID 达到 0.20，FS 达到 0.97，均优于对比基线。MotionCutMix 的空间混合机制天然适合此类任务，因为增强过程本身就是对身体部位的运动组合。
- **风格迁移**（style transfer）：FID 降至 0.14，表明生成运动更接近真实数据分布。MotionCutMix 利用大型未标注运动数据库扩展风格多样性，使模型能处理训练集中未见的风格组合。
- **标注数据受限场景**：消融分析显示，增加 MotionCutMix 比例可持续提升编辑指令遵循度（AvgR），且即使训练数据大幅减少，使用 MotionCutMix 的模型仍能保持较强性能，证明该方法有效降低了对标注数据规模的依赖。

### 局限性与开放问题

尽管 MotionReFit 在多项指标上取得领先，但仍存在以下局限：

- **长期时间依赖**：自回归滑动窗口机制虽然降低了学习难度，但处理极长序列时，跨窗口的过渡连贯性可能不足，模型对长程时间结构的建模能力仍有提升空间。
- **空间敏感度不足**：对位置相关的精细编辑指令（如“将右臂画圈”）的空间理解不够准确，框架尚未显式集成空间推理能力。
- **协调器的边界情况**：身体部位协调器通过判别器引导缓解了不自然同步问题，但在极端运动组合下仍可能出现罕见的协调误差。协调器能否通过物理合理性损失等其他感知约束进一步增强，是一个开放方向。
- **MotionCutMix 的软掩码机制**：软掩码参数 $\alpha$ 的调节目前为固定或启发式设定，其随不同任务和运动类型自动调整的最优策略尚未明确。
- **大规模数据库的负样本过滤**：MotionCutMix 从大型数据库中随机选取目标运动进行混合，缺乏对低质量或冲突运动组合的动态选择与过滤机制，可能引入噪声训练样本。

### 知识库定位

MotionReFit 的核心贡献在于**数据增强驱动的运动编辑泛化**，其方法论处于以下交叉点：

- **扩散模型在运动生成中的应用**：继承 MDM 等工作的扩散范式，但通过自回归分解和判别器引导扩展了扩散模型在运动编辑中的适用性。
- **数据增强与合成训练**：MotionCutMix 借鉴了图像领域 CutMix 的思想，将其适配到结构化人体运动的空间混合场景，利用 SMPL-X 参数表示和球面线性插值（SLERP）实现软掩码混合，保证了合成运动的物理合理性。
- **人体运动先验与协调性**：运动协调器的引入将人体运动学先验（身体部位间的自然协调模式）以判别器形式注入生成过程，为运动生成中的物理合理性约束提供了可扩展的实现路径。

## 原文 PDF

![[paperPDFs/CVPR_2025/Dynamic_Motion_Blending_for_Versatile_Motion_Editing.pdf]]

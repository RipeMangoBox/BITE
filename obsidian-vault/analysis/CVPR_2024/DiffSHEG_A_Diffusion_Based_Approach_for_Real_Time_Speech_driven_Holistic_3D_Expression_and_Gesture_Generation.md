---
title: DiffSHEG A Diffusion Based Approach for Real Time Speech driven Holistic 3D Expression and Gesture Generation
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic_3D_Expression_and_Gesture_Generation.pdf
project_link: https://jeremycjm.github.io/proj/DiffSHEG
code_link: null
aliases:
- DiffSHEG_A_Diffu
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在统一扩散去噪网络中引入单向表情到手势的信息流（UniEG），使表情预测显式地作为手势生成的上下文，从而捕捉联合分布。
primary_logic: 表情传递情感和语言线索，是手势的自然先验；手势极少反向影响表情（尤其是嘴唇），因此单向信息流足以在保持表情准确的同时显著增强手势的合理性与多样性。
claims:
- 定量实验中，DiffSHEG在BEAT和SHOW数据集上的Fréchet距离（FMD/FGD）全面优于所有基线，且消融实验证明单向信息流、梯度截断和残差融合块均有显著贡献。
- 用户研究显示，DiffSHEG在动作真实感、手势-语音同步、表情-语音同步和多样性四个维度上均被显著偏好，验证了整体联合生成的优势。
- 定性比较展示DiffSHEG生成的动作更敏捷、多样且与语音的语义重音对齐（如“journalist”“never”等词对应的强调手势），且无基线中出现的抖动或迟钝问题。
- FOPPAS使扩散模型在单张3090 GPU上达到超30 FPS的实时流式推理，且无需在训练时依赖历史帧，灵活性优于自回归扩散基线。
---

# DiffSHEG A Diffusion Based Approach for Real Time Speech driven Holistic 3D Expression and Gesture Generation

> [!tip] 核心洞察
> 表情传递情感和语言线索，是手势的自然先验；手势极少反向影响表情（尤其是嘴唇），因此单向信息流足以在保持表情准确的同时显著增强手势的合理性与多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffSHEG：基于扩散模型的实时语音驱动整体3D表情与手势生成 |
| 英文题名 | DiffSHEG A Diffusion Based Approach for Real Time Speech driven Holistic 3D Expression and Gesture Generation |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://jeremycjm.github.io/proj/DiffSHEG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DiffSHEG |
| Dataset | BEAT, SHOW |

> [!tip] 效果简介
> - BEAT 上，FMD↓ 324.67 vs LDA (SIGGRAPH'23) 688.25 / CaMN 1055.52 (相比于最强基线LDA降低363.58（52.8%）)。
> - SHOW 上，FMD↓ 0.00184 vs TalkSHOW (Re-train) 0.00278 / LS3DCG* 0.00230 (相比于TalkSHOW降低0.00094（33.8%）)。
> - BEAT (User Study) 上，用户偏好百分比（真实感/同步/多样性） 在BEAT和SHOW上四个指标均获得约60%~80%的显著偏好 vs CaMN, DiffGesture, DSG, LDA (一致领先于所有基线)。

## 概要

语音驱动的共语手势与面部表情生成是虚拟人交互的核心技术，但现有方法面临一个根本性瓶颈：**表情与手势的联合分布被忽视**。主流方案要么将二者分别独立建模（两个独立模型），要么采用多任务学习但解码器间缺乏显式交互，导致生成的动作协调性差、多样性不足。同时，确定性回归模型难以拟合语音到手势的一对多映射关系，进一步限制了生成的自然度与表现力。

DiffSHEG 针对上述瓶颈提出了一个统一的扩散生成框架，核心创新在于**在去噪网络中引入单向表情到手势的信息流（UniEG）**。其核心洞见是：表情承载了情感和语言线索，是手势的自然先验，而手势极少反向影响表情（尤其是唇部），因此单向信息流足以捕捉二者的联合分布，在保持表情准确性的同时显著增强手势的合理性与多样性。此外，DiffSHEG 设计了运动-语音残差融合块以加速训练收敛，并提出了基于外推的部分自回归采样策略（FOPPAS），使扩散模型能够在单张 3090 GPU 上实现超过 30 FPS 的实时流式推理，且无需在训练时依赖历史帧。

定量实验表明，DiffSHEG 在 BEAT 和 SHOW 两个数据集上的 Fréchet 动作距离（FMD/FGD）全面优于所有基线方法——在 BEAT 上 FMD 降至 324.67，相比最强基线 LDA（SIGGRAPH 2023）的 688.25 降低了 52.8%；在 SHOW 上 FMD 为 0.00184，相比重新训练的 TalkSHOW（0.00278）降低了 33.8%。消融实验进一步证实，单向信息流、梯度截断和残差融合块均对性能有显著贡献。用户研究显示，DiffSHEG 在动作真实感、手势-语音同步、表情-语音同步和多样性四个维度上均获得约 60%~80% 的显著偏好，一致领先于 CaMN（Habibie et al., ECCV 2022）、DiffGesture（Zhu et al., CVPR 2023）、DiffuseStyleGesture（Yang et al., IJCAI 2023）和 LDA 等基线方法。定性比较中，DiffSHEG 生成的动作更敏捷、多样，且能与语音的语义重音对齐（如对“journalist”“never”等词产生对应的强调手势），无基线中常见的抖动或迟钝问题。

方法目前仍存在一些局限：生成质量高度依赖训练数据质量，数据中的抖动或异常动作会被复现；尚未在更多样化的说话人、语言或情绪场景下验证泛化能力；扩散生成的固有随机性偶尔可能导致不自然的手势，尤其在数据稀疏区域；当前方案未显式建模物理约束（如穿模），在极端姿态下可能产生不合理的身体交叉。这些方向为后续研究提供了明确的改进空间。

**语音驱动的虚拟人动作生成**是构建沉浸式数字人的核心技术，要求面部表情与身体手势在语义、韵律和情感层面与语音信号高度同步。近年来，该领域从早期的规则驱动系统逐步演进为数据驱动的深度生成范式，但一个根本性问题始终悬而未决：**表情与手势应如何联合生成？**

### 现有方法的缺口：割裂的生成与缺失的联合分布

当前主流方法可大致分为两类：

- **独立生成范式**：将表情和手势视为两个独立任务，分别训练两个互不通信的模型（如 **CaMN**（Habibie et al., ECCV 2022）以多条件LSTM生成手势，再单独处理表情）。这种方式完全忽视了表情与手势之间天然存在的统计依赖关系，导致生成的动作缺乏协调性——面部传达的情绪线索与手部动作在语义上脱节。
- **多任务学习范式**：在共享编码器后使用两个独立的解码器分支分别输出表情和手势（如 **LS3DCG**（Habibie et al., IVA 2021）的CNN多任务架构、**TalkSHOW**（Yi et al., CVPR 2023）的VQ-VAE整体生成框架）。然而，这些方法仅在编码层共享信息，解码过程中两个分支缺乏显式的交互机制，本质上仍未能建模表情与手势的**联合分布**。

更深层的瓶颈在于：语音到动作的映射本质上是**一对多**的——同一段语音可以对应多种合理的手势表达。确定性模型（如回归或VAE）倾向于生成“平均化”的动作，难以捕捉这种多模态分布，导致生成结果多样性不足、动作幅度偏小。

### 核心洞察：表情是手势的自然先验

一个关键的因果观察被现有方法普遍忽视：**表情传递情感和语言线索，是手势生成的天然先验；而手势极少反向影响表情（尤其是嘴唇运动）**。说话时，面部表情（包括嘴唇、眉毛、头部姿态）直接承载着语音的语义重音和情感色彩，手势则是对这些线索的补充与放大。这一不对称的因果关系暗示：只需建立**从表情到手势的单向信息流**，即可在保持表情准确性的同时，显著增强手势的合理性与多样性。

### 扩散模型的机遇与实时性挑战

扩散模型（Diffusion Models）在图像和运动生成领域展现出强大的分布拟合能力，能够自然应对一对多映射问题。已有工作如 **DiffGesture**（Zhu et al., CVPR 2023）和 **DiffuseStyleGesture (DSG)**（Yang et al., IJCAI 2023）将扩散模型引入手势生成，但其设计仅限于单一模态，未涉及表情与手势的联合建模。同时，扩散模型的多步迭代去噪过程与实时流式推理需求之间存在根本矛盾——如何在保持生成质量的同时，使扩散模型达到30 FPS以上的实时性能，是一个尚未解决的工程挑战。

### 本文动机

基于上述分析，本文提出 **DiffSHEG**，旨在回答以下核心问题：**能否设计一个统一的扩散框架，通过显式建模表情到手势的单向信息流，捕捉二者的联合分布，同时实现任意长度的实时流式推理？** 这一问题的解决将推动语音驱动数字人从“可用”走向“自然且富有表现力”的新阶段。

## 核心方法与创新机理

DiffSHEG 的核心创新并非引入全新的生成范式，而是在统一的扩散模型框架内，通过**三个关键设计**系统性地解决了语音驱动整体3D表情与手势生成中长期存在的“联合建模缺失”问题，从而在动作协调性、多样性与实时性上形成突破。

### 1. 单向表情到手势的信息流（UniEG）：联合分布的显式建模

现有方法（如 **CaMN** (Habibie et al., ECCV 2022)、**TalkSHOW** (Yi et al., CVPR 2023)）要么将表情与手势作为两个独立任务分别生成，要么在多任务解码器中仅做浅层共享，忽视了二者的联合分布，导致生成的动作缺乏内在协调性。DiffSHEG 的核心洞察在于：**表情传递情感和语言线索，是手势的自然先验；而手势极少反向影响表情（尤其是嘴唇）**。基于此，作者设计了 UniEG（单向表情-手势生成器），在扩散去噪的每一步，从表情分支计算预测的干净表情 $\hat{\mathbf{x}}_{0(t)}^{E}$，并将其显式传入手势分支的 Transformer 中作为上下文条件，同时**截断梯度**以防止手势分支的损失反向干扰表情编码的质量。这一设计以极简的单向信息流，实现了对表情-手势联合分布的有效捕捉。

消融实验强有力地验证了这一设计的必要性：移除单向信息流（Ours w/o $\hat{x}_E$）导致 BEAT 数据集上的 FGD 从 438.93 升至 477.00，多样性指标 Div 从 0.536 降至 0.504；梯度不截断（Ours w/o Detach）或反向传递梯度均造成指标普遍退化（Table 1）。

### 2. 运动-语音残差融合块：高效的条件注入与收敛加速

传统方法（如 **DiffGesture** (Zhu et al., CVPR 2023)）使用线性投影或交叉注意力将语音条件注入运动特征，融合效率有限。DiffSHEG 提出了 MLP 残差融合块（Motion-Speech Fusion Residual Block），将运动特征与多层语音特征沿通道拼接后，通过 LayerNorm + MLP 残差结构进行融合，保持自然的时间对齐。这一设计不仅增强了语音与运动的耦合，更使训练收敛速度**提升 2~4 倍**，最终损失也更低（Figure 10）。

### 3. FOPPAS：无需训练的外推式实时长序列推理

扩散模型在长序列生成中面临推理效率瓶颈，现有方案或依赖训练时的历史帧（自回归），或固定初始姿态导致多样性受限。DiffSHEG 提出的 **FOPPAS**（Fast Outpainting-based Partial Autoregressive Sampling）是一种纯推理策略：利用 Repaint 外推机制，以前一片段的重叠帧为约束，外推生成当前片段，并结合 DDIM 加速与最后两步线性混合，实现任意长序列的平滑生成。该方法无需在训练时依赖历史帧，在单张 Nvidia 3090 GPU 上即可达到 **超过 30 FPS** 的实时流式推理（Section 4.4），在灵活性与效率上显著优于自回归扩散基线。

### 创新点总结

| 创新维度 | 基线做法 | DiffSHEG 方案 | 核心收益 |
|:---|:---|:---|:---|
| **整体生成方式** | 表情与手势独立生成或多任务无交互 | 统一扩散去噪网络，显式建模联合分布 | 动作协调性、多样性显著提升 |
| **信息交互方向** | 无直接交互或潜在双向融合 | 单向表情→手势（UniEG）+ 梯度截断 | 手势合理性增强，表情质量不受干扰 |
| **运动-语音融合** | 线性投影或交叉注意力 | MLP 残差融合块 | 收敛加速 2~4 倍，最终损失更低 |
| **长序列推理** | 训练时依赖历史帧或固定初始姿态 | FOPPAS：无需训练的外推式部分自回归采样 | 任意长度实时流式推理（>30 FPS） |

> **注意**：FOPPAS 的累积误差在多分钟超长序列中的可控性，以及 UniEG 在极度复杂情感场景下的充分性，仍属于开放问题，需进一步验证。

DiffSHEG 提出了一种**统一的扩散模型框架**，用于从语音中同时生成任意长度的整体 3D 表情与手势。其核心设计动机在于：现有方法通常将表情与手势视为两个独立任务（分别建模或多任务解码器无交互），忽略了二者的联合分布，导致动作不协调且多样性不足；同时，确定性模型难以拟合语音到手势的一对多映射。DiffSHEG 通过在统一扩散去噪网络中引入**单向表情到手势的信息流（UniEG）**，使表情预测显式地成为手势生成的上下文，从而捕捉联合分布。

### 整体流程

框架由两大模块构成：**音频编码器**与 **UniEG Transformer 生成器**（图 2）。

**音频编码器**负责从原始语音中提取多层特征：
- **低层特征**：Mel-spectrogram，捕捉音色、韵律等细粒度声学信息。
- **高层特征**：冻结的 HuBERT 特征，提供语义和语言结构信息。
- **中层特征**：一个可训练的 Transformer 将上述特征融合，学习适合运动生成的中层语音表征。

**UniEG Transformer 生成器**是扩散去噪网络的核心，其名称具有双重含义：既指“统一”的联合表情-手势生成，又指“单向”的表情到手势条件流动。具体而言，扩散过程的每一步，表情去噪分支会先预测当前步的“干净表情” $\hat{\mathbf{x}}_{0(t)}^{E}$（式 5），然后将该预测显式地传入手势去噪分支作为条件输入，同时**截断梯度**以防止手势分支的损失反向干扰表情编码器的优化。这一单向信息流的设计依据在于：表情传递情感和语言线索，是手势的自然先验；而手势极少反向影响表情（尤其是嘴唇），因此单向流动足以在保持表情准确的同时显著增强手势的合理性与多样性。

去噪网络内部，运动特征与语音特征（及其他可选时间条件）沿通道拼接后，通过 **运动-语音融合残差块** 进行融合。该残差块由 LayerNorm 与 MLP 残差连接构成，保持自然的时序对齐，并在实验中证明可将训练收敛速度提升 2~4 倍（图 10）。随后，**风格感知 Transformer 块** 将说话人 ID 和扩散时间步投影后注入 AdaIN，调节 Transformer 中间特征，实现风格化生成。

### 长序列推理：FOPPAS

DiffSHEG 的训练在固定长度片段上进行，不依赖历史帧。为实现任意长度生成，作者提出了 **FOPPAS**（Fast Outpainting-based Partial Autoregressive Sampling，图 3），一种无需训练的外推式部分自回归采样策略：利用 Repaint 外推机制，将前一片段的尾部帧作为当前片段的固定初始帧，仅对剩余帧进行扩散去噪，并结合 DDIM 加速与最后两步线性混合，实现平滑的流式推理。该策略使模型在单张 NVIDIA 3090 GPU 上达到超过 30 FPS 的实时性能，且灵活性优于训练时依赖历史帧的自回归扩散基线。

### 训练目标

总损失由三项加权组合而成（式 8）：
- **噪声预测损失** $\mathcal{L}_t$（权重 10）：标准 DDPM 噪声预测均方误差。
- **速度损失** $\mathcal{L}_v$（权重 1）：惩罚生成动作与真实动作在帧间速度上的差异，增强动作平滑性。
- **Huber 重建损失** $\mathcal{L}_\delta$（权重 1）：在预测的干净动作 $\hat{\mathbf{x}}_0$ 与真实动作 $\mathbf{x}_0$ 之间施加 Huber 损失，提升重建精度。

这一损失设计兼顾了扩散生成的质量、动作的动态平滑性以及最终重建的准确性。

![[assets/figures/papers/paper_list_l1846_DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic/figures/002_Figure_2.jpg]]
*Figure 2: DiffSHEG framework overview. Left: Audio Encoders and UniEG-Transformer Generator. Given an audio clip, we encode the audio into a low-level feature Mel-Spectrogram and a high-level HuBERT feature. An audio encoder learns a mid-level representation of speech. The audio features are concatenated with other optional temporal conditions and then fed into the UniEG Transformer Denoiser. The denoising block fuses the conditions with noisy motion at diffusion step t and feeds it into style-aware transformers to get the predicted noises. The uni-directional condition flow is enforced from expression to gesture for joint distribution learning. Right: The detailed architecture of style-aware Transfo...*

### 扩散先验基础

DiffSHEG 建立在去噪扩散概率模型（DDPM）之上。前向过程逐步向原始运动数据 $\mathbf{x}_0$ 注入高斯噪声，单步转移为：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$

完整的前向扩散过程为各步的乘积：

$$q(\mathbf{x}_{1:T} | \mathbf{x}_0) = \prod_{t=1}^{T} q(\mathbf{x}_t | \mathbf{x}_{t-1})$$

为使模型受额外上下文信息 $\mathbf{c}$（如音频）条件控制，将条件注入噪声预测网络 $\epsilon_\theta(\cdot)$，训练目标为噪声预测损失：

$$\mathcal{L}_t = \mathbb{E}_{\mathbf{x}_0, \epsilon} \left[ \| \epsilon - \epsilon_\theta (\sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, t, \mathbf{c}) \|^2 \right]$$

### 音频编码器

音频编码器负责提取多层语音表征，为后续生成提供条件信号。其结构包含三个层次：

- **低层特征**：Mel-Spectrogram，捕捉语音的短时频谱信息。
- **高层特征**：冻结参数的 HuBERT 特征，提供语义和音素层面的抽象表征。
- **中层可学习编码器**：一个可训练的 Transformer，将 Mel-Spectrogram 和 HuBERT 特征融合为中层语音表征。消融实验表明，移除该中层编码器（w/o Mid）会导致 FGD 从 438.93 急剧上升至 613.86（Table 3），证明多层语音特征融合对生成质量至关重要。

### UniEG 单向表情-手势生成器

UniEG 是 DiffSHEG 的核心创新模块，其名称具有双重含义：统一（Unified）的联合表情-手势生成，以及单向（Uni-directional）的表情到手势信息流。

**设计动机**：表情传递情感和语言线索，是手势的自然先验；手势极少反向影响表情（尤其是嘴唇），因此单向信息流足以在保持表情准确的同时显著增强手势的合理性与多样性。

**工作机制**：在扩散去噪的每一步 $t$，从表情去噪分支根据预测噪声 $\hat{\epsilon}_t^{E}$ 反向估计干净的预测表情 $\hat{\mathbf{x}}_{0(t)}^{E}$：

$$\hat{\mathbf{x}}_{0(t)}^{E} = \frac{\mathbf{x}_t^{E} - \sqrt{1-\bar{\alpha}_t} \hat{\epsilon}_t^{E}}{\sqrt{\bar{\alpha}_t}}$$

该预测的干净表情随后被显式地传入手势 Transformer 分支，作为手势生成的上下文条件。同时，**梯度截断**（Detach）操作阻止手势分支的梯度回传至表情编码器，防止手势生成任务干扰表情特征学习。消融实验（Table 1）证实：移除单向信息流（Ours w/o $\hat{\mathbf{x}}_E$）导致 FGD 从 438.93 升至 477.00，多样性指标 Div 从 0.536 降至 0.504；取消梯度截断或反向传递梯度均造成指标普遍下降。

### 运动-语音融合残差块

该模块将运动特征与语音特征（及其他时间条件）沿通道维度拼接后，通过 LayerNorm + MLP 残差块进行融合，保持自然的时间对齐。其关键优势在于训练效率：使用该残差融合块后，训练收敛速度提升 2~4 倍，且最终损失更低（Figure 10）。

### 风格感知 Transformer 块

为实现风格化生成，该模块将说话人 ID 和扩散时间步 $t$ 投影后注入 AdaIN（自适应实例归一化），调节 Transformer 中间特征。这使得同一音频输入可针对不同说话人生成具有个体风格差异的表情与手势。

### 训练损失函数

总训练损失由三项加权求和构成：

$$\mathcal{L} = \lambda_t \mathcal{L}_t + \lambda_v \mathcal{L}_v + \lambda_\delta \mathcal{L}_\delta$$

其中：

- **$\mathcal{L}_t$**：噪声预测损失（DDPM），权重 $\lambda_t = 10$。
- **$\mathcal{L}_v$**：速度损失，惩罚生成动作与真实动作在帧间速度上的差异，增强动作平滑性：

$$\mathcal{L}_v = \mathbb{E} \left[ \| (\mathbf{x}_0[1:] - \mathbf{x}_0[:-1]) - (\hat{\mathbf{x}}_0[1:] - \hat{\mathbf{x}}_0[:-1]) \|^2 \right]$$

权重 $\lambda_v = 1$。

- **$\mathcal{L}_\delta$**：Huber 重建损失，作用于原始运动 $\mathbf{x}_0$ 与预测运动 $\hat{\mathbf{x}}_0$ 之间的差异，在 $\delta$ 阈值内使用 MSE，之外使用 MAE，以平衡平滑性与鲁棒性。权重 $\lambda_\delta = 1$。

### FOPPAS 实时推理管道

FOPPAS（Fast Outpainting-based Partial Autoregressive Sampling）是 DiffSHEG 实现任意长度实时推理的关键模块，其设计特点包括：

- **无需训练**：仅改变推理时的采样策略，不增加训练负担。
- **外推式部分自回归**：利用 Repaint 外推机制，以前一个片段的重叠帧为锚点，外推生成当前片段的剩余帧，实现片段间的平滑过渡（Figure 3, Algorithm 1）。
- **DDIM 加速**：通过去噪扩散隐式模型（DDIM）减少采样步数，提升推理速度。
- **最后两步线性混合**：对相邻片段的重叠区域进行线性混合，进一步消除边界不连续性。

在单张 Nvidia 3090 GPU 上，FOPPAS 可实现超过 30 FPS 的实时流式推理，且无需在训练时依赖历史帧，灵活性优于自回归扩散基线。

## 实验与关键发现

### 核心定量结果

DiffSHEG 在两个主流数据集上均取得了大幅领先的 Fréchet 距离指标。在 **BEAT** 数据集上，DiffSHEG 的 FMD（Fréchet Motion Distance）为 **324.67**，相比最强基线 LDA（SIGGRAPH'23）的 688.25 降低了约 **52.8%**，相比 CaMN（Habibie et al., ECCV 2022）的 1055.52 降幅更为显著（Table 1）。在 **SHOW** 数据集上，DiffSHEG 的 FMD 为 **0.00184**，显著优于重新训练的 TalkSHOW（Yi et al., CVPR 2023）的 0.00278（降低约 33.8%）以及 LS3DCG（Habibie et al., IVA 2021）预训练模型的 0.00230（Table 1）。这一结果直接支撑了核心论断：统一扩散框架对表情-手势联合分布的显式建模，在动作生成质量上产生了可量化的巨大增益。

除 Fréchet 距离外，平滑度与敏捷度指标揭示了更深层的质量差异。DiffSHEG 在 BEAT 上的加速度误差（AE）为 0.628，与 CaMN 的 0.521 处于同一量级，表明其平滑性良好；而速度指标（Vel）为 0.821，MLVS 为 0.562，均最接近真实动作（GT 的 Vel=0.863, MLVS=0.633），说明生成动作的敏捷度与动态特性明显优于基线。相比之下，DiffGesture（Zhu et al., CVPR 2023）的 AE 高达 5.210，存在严重抖动；CaMN 的 Vel 仅为 0.407，动作过于迟缓（Table 2）。这表明扩散模型的随机性并未引入不可控的抖动，反而在速度损失的约束下实现了更逼真的运动节奏。

![[assets/figures/papers/paper_list_l1846_DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic/figures/011_Table_2.jpg]]
*Table 2: Smoothness and agility metric results. ↓: smaller is better. †: closer to GT is better*

### 用户主观评估

用户研究为定量指标提供了关键的感知验证。在 BEAT 和 SHOW 两个数据集上，评估者对动作真实感、手势-语音同步、表情-语音同步和动作多样性四个维度进行偏好选择，DiffSHEG 在所有维度和数据集上均获得了约 **60%~80%** 的显著偏好（Figure 7）。这一结果尤其值得注意：即使基线方法（如 CaMN、DiffGesture、DSG、LDA）在对比时被独立补全了表情数据，用户仍然一致偏好 DiffSHEG 的整体输出，说明联合建模带来的协调性提升是可被人类清晰感知的。

### 定性分析：语义对齐与动作多样性

定性比较揭示了定量指标无法完全捕捉的细节优势。在 BEAT 数据集上，当语音中出现 "journalist" 一词时，DiffSHEG 生成的虚拟人同时举起双手以强调该词；当说出 "never" 时，右手和手指随两个音节 "ne" 和 "ver" 做出两次上下运动（Figure 4）。这种对语音重音和语义的自觉响应，在 CaMN、DiffGesture 等基线中未被观察到。在 SHOW 数据集上，DiffSHEG 展现出更丰富的头部姿态变化：基线方法（TalkSHOW、LS3DCG）在部分片段中出现不自然的持续低头姿态，而 DiffSHEG 能够产生大幅度的抬头预备动作，并在说出 "five" 时配合扬眉和精确的唇形变化（Figure 5, Figure 6）。这些行为模式表明，单向表情到手势的信息流成功将表情中蕴含的情感与语言线索传递给了手势生成分支。

![[assets/figures/papers/paper_list_l1846_DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic/figures/005_Figure_5.jpg]]
*Figure 5: Motion Comparison on the SHOW [49] Dataset. Our method generates more expressive and diverse motions than Talk-Show [49] and LS3DCG [14] in terms of both gesture and head pose diversity. Our results also show more agile motions than baselines*

![[assets/figures/papers/paper_list_l1846_DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on BEAT [26] Dataset. In comparison to baseline methods, our approach generates a broader range of natural, agile, and diverse gestures that are closely synchronized with the audio input. When saying ”journalist”, the character driven by our motion raises double hands to stress this word; When saying ”never”, our motion shows two times up-and-down right hand and fingers, corresponding to the two syllables “ne” and “ver”. The character is from MetaHuman [55] rendered by Unreal Engine 5 [56]*

![[assets/figures/papers/paper_list_l1846_DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic/figures/007_Figure_6.jpg]]
*Figure 6: Expression and Head Pose Comparison on the SHOW [49] Dataset. (a) With speech audio as input, Talk-Show [49] and LS3DCG [14] may generate unnatural and persistent head-down poses showing limited variation. In contrast, our method produces a wide range of expressive head poses. (b) Prior to the audio input’s emphasis on the word “five”, our approach instinctively raises the head to prepare for highlighting, subsequently producing precise lip movements accompanied by raised eyebrows to emphasize the word “five”*

### 消融实验：单向信息流与梯度截断的关键作用

消融实验系统验证了 UniEG 设计的每个组件。移除单向信息流（Ours w/o x̂E）导致 BEAT 上的 FGD 从 438.93 上升至 477.00，多样性指标（Div）从 0.536 下降至 0.504，直接证明了表情到手势的信息传递对生成质量和多样性的关键贡献（Table 1）。进一步地，取消梯度截断（Ours w/o Detach）或尝试反向传递梯度（Reverse Direction）均造成指标普遍退化，验证了截断手势分支梯度以防止其干扰表情编码的必要性。定性消融（Figure 12）也显示，NoDetach 和 ReverseDirection 变体生成的动作趋于静止或仅产生微小的头部和手部运动，而完整模型则表现出丰富且语义对齐的手势。

![[assets/figures/papers/paper_list_l1846_DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic/figures/016_Figure_12.jpg]]
*Figure 12: Qualitative ablations. We compare our full method with ablations NoDetach, ReverseDirection, NaivePass, and NoX0 as described in Section 4.5. Our full version of DiffSHEG shows more diversified and meaningful gestures aligned with speech, while other ablations remain still or relatively small head and hand motions*

### 音频编码器与融合模块消融

音频编码器的多层特征融合策略对性能影响显著。消融实验显示，移除可学习的中层编码器（w/o Mid）使 BEAT 上的 FGD 从 438.93 骤增至 613.86，退化幅度远超移除 HuBERT（w/o Hubert）或 Mel-spectrogram（w/o Mel）的版本（Table 3）。这表明低层声学特征与高层语义特征的中间融合层是性能瓶颈，而非单一特征的缺失。此外，运动-语音残差融合块在训练效率上带来了 2~4 倍的收敛加速，且最终损失更低（Figure 10），说明该设计不仅改善了最终性能，还显著降低了训练成本。

### 推理效率与实时性

FOPPAS 推理管道在单张 Nvidia 3090 GPU 上实现了超过 30 FPS 的实时流式生成（Section 4.4），且无需在训练时依赖历史帧。与自回归扩散基线相比，这一外推式部分自回归采样策略在灵活性和推理速度之间取得了实用平衡，使扩散模型在实时交互场景中的部署成为可能。

### 已知局限与失败模式

尽管整体性能优异，DiffSHEG 仍存在若干可复现的局限。首先，方法对训练数据质量高度敏感：若训练集包含抖动或异常动作（如 BEAT 女性角色的部分片段），生成结果也会复现类似瑕疵。其次，扩散生成固有的随机性在数据稀疏区域偶尔会导致不自然的手势。此外，当前方案未显式建模物理约束（如身体自交叉），在极端姿态下可能产生不合理的穿模现象。这些失败模式指向了未来工作的直接方向：在保持多样性与表现力的前提下，引入对训练噪声的鲁棒机制和物理合理性约束。

## 定位与知识库关联

### 1. 与现有工作的关系

DiffSHEG 的定位是在语音驱动的3D虚拟人动作生成这一任务中，首次将**表情与手势的联合分布显式建模**引入扩散模型框架。其与现有工作的关系可以从三个维度来理解：

**（1）相对于分治式生成方法的突破**

在 DiffSHEG 之前，语音驱动的整体动作生成（同时包含表情和手势）主要采用两种分治策略：

- **独立模型方案**：分别训练表情生成器和手势生成器，推理时各自独立运行。典型代表包括 **CaMN**（Habibie et al., ECCV 2022）和 **DiffGesture**（Zhu et al., CVPR 2023）等纯手势生成方法，以及 **TalkSHOW**（Yi et al., CVPR 2023）的整体生成方法。这类方案的根本问题在于完全忽视了表情与手势之间的统计依赖关系——人在说话时，表情（尤其是唇部动作和眉毛运动）携带了大量语义和韵律信息，这些信息本应是手势规划的重要上下文。独立生成导致二者在时序和语义上脱节，表现为手势与语音重音不对齐、表情与手势情绪不一致等典型失败模式。

- **多任务学习方案**：通过共享编码器或多任务解码器同时输出表情和手势，如 **LS3DCG**（Habibie et al., IVA 2021）。这类方法虽然共享了部分特征，但两个输出分支之间缺乏显式的信息交互机制，本质上仍是条件独立假设下的并行生成，未能真正捕捉联合分布 $p(\text{gesture}, \text{expression} \mid \text{speech})$。

DiffSHEG 的核心贡献在于打破了这一分治范式：通过在统一扩散去噪网络中引入**单向表情到手势的信息流（UniEG）**，使手势生成分支在每一步去噪时都能显式地访问当前步预测的干净表情 $\hat{\mathbf{x}}_{0(t)}^{E}$（由 Eq. 5 计算），从而将生成过程从条件独立提升为条件联合。消融实验（Table 1）直接验证了这一设计的因果效应：移除单向信息流（Ours w/o $\hat{x}_E$）导致手势 Fréchet 距离（FGD）从 438.93 恶化至 477.00，多样性指标 Div 从 0.536 降至 0.504。

**（2）相对于其他扩散生成方法的改进**

近年来，扩散模型在单一手势生成任务上展现出优于确定性方法（如 LSTM、CNN）的多样性和质量，代表性工作包括 **DiffGesture**（Zhu et al., CVPR 2023）、**DiffuseStyleGesture (DSG)**（Yang et al., IJCAI 2023）和 **LDA**（SIGGRAPH 2023）。DiffSHEG 在继承扩散框架优势的基础上，做出了三项关键改进：

- **从单一模态到联合模态**：上述基线仅生成手势，DiffSHEG 将生成空间扩展为表情+手势的联合空间，且通过 UniEG 机制而非简单的通道拼接来建模模态间依赖。Table 1 中的 "Naive Concat" 消融变体（将表情和手势噪声简单拼接后送入统一 Transformer）性能显著低于完整 UniEG 设计，证实了有向信息流设计优于无结构融合。

- **运动-语音残差融合块**：基线方法通常采用线性投影（如 DiffGesture）或交叉注意力来融合运动特征与语音条件。DiffSHEG 提出的 MLP 残差融合块（Motion-Speech Fusion Residual Block）将运动特征与语音特征沿通道拼接后，通过 LayerNorm + MLP 残差结构进行融合，保持自然的时间对齐。Figure 10 的训练损失曲线显示，该设计使收敛速度提升 2~4 倍，且最终损失更低。

- **无需训练的任意长度推理**：自回归扩散基线（如 DiffGesture 的部分变体）在训练时依赖前一帧作为条件，限制了推理灵活性。DSG 等方法则固定初始姿态生成固定长度片段。DiffSHEG 提出的 **FOPPAS**（Fast Outpainting-based Partial Autoregressive Sampling）利用 Repaint 外推 + DDIM 加速 + 最后两步线性混合，在无需训练修改的情况下支持任意长度序列的实时流式推理（单张 3090 GPU 上超过 30 FPS），且不依赖训练时的历史帧条件。

**（3）对“表情→手势”单向因果假设的实证验证**

DiffSHEG 的一个核心洞察是：在语音驱动的共语动作中，表情（尤其是唇部和眉毛）传递情感和语言线索，是手势的自然先验；而手势极少反向影响表情（尤其是嘴唇运动，它主要由语音内容决定）。因此，单向信息流从表情到手势足以捕捉联合分布中的主要依赖关系。

消融实验系统地验证了这一假设：
- **梯度截断的必要性**：若不截断从手势分支回传至表情编码器的梯度（Ours w/o Detach），指标普遍下降，表明手势分支的梯度会干扰表情编码的优化。
- **反向信息流的有害性**：若将信息流方向反转（Reverse Direction，从手势到表情），性能同样恶化，证实了因果方向的非对称性。
- **直接传递噪声表情的不足**：若传递带噪表情 $\mathbf{x}_t^E$ 而非预测的干净表情 $\hat{\mathbf{x}}_{0(t)}^E$（Naive Pass），效果也显著下降，说明干净表情中的语义信息是手势生成的关键上下文。

### 2. 适用边界与关键局限

尽管 DiffSHEG 在定量和定性评估中均展现出显著优势，但其适用边界和局限同样需要明确认知：

**（1）数据质量依赖性**

方法高度依赖训练数据的质量。论文明确指出，若训练集存在抖动或异常动作（如 BEAT 数据集中女性角色的部分抖动片段），生成结果也会复现类似瑕疵。这是因为扩散模型学习的是训练分布的整体特征，缺乏对离群样本的显式鲁棒性机制。在数据稀疏区域（如某些罕见的手势-语音组合），扩散生成的固有随机性偶尔可能导致不自然的手势。

**（2）泛化能力的未验证边界**

目前的评估仅限于 BEAT 和 SHOW 两个受控数据集。以下场景的泛化能力尚未验证：
- 更多样化的说话人身份、口音和语言
- 极端情绪状态（如愤怒、悲伤、兴奋）下的表情-手势联合生成
- 自然对话（而非独白）中的交替发言和反应性手势
- 不同文化背景下的手势习惯差异

**（3）物理约束的缺失**

当前方案未显式建模物理约束（如身体部件间的穿模检测）。在极端姿态下——尤其是当生成的手势幅度较大或方向异常时——可能产生不合理的身体交叉（如手部穿过躯干、手臂与头部重叠）。这对于需要直接驱动3D角色在物理引擎中渲染的下游应用（如游戏、虚拟现实）是一个实际障碍。

**（4）FOPPAS 的累积误差风险**

FOPPAS 采用部分自回归的外推策略：每个新片段的前若干帧与上一片段的重叠部分通过线性混合进行平滑过渡。虽然论文验证了在常规长度序列上的实时性和平滑性，但在多分钟甚至更长的连续生成中，自回归外推的累积误差是否可控仍是一个开放问题。当前设计缺乏全局一致性约束来纠正长程漂移。

### 3. 开放性研究问题

基于上述分析，DiffSHEG 开启或遗留了以下值得进一步探索的方向：

**问题一：训练数据鲁棒性机制**

如何设计一种机制，使模型对训练数据中的噪声或离群动作具有鲁棒性，而不牺牲多样性与表现力？可能的路径包括：在训练时引入数据增强策略（如对训练动作施加可控噪声并让模型学习去噪）、采用鲁棒的损失函数（如对离群值不敏感的 Huber 损失的变体）、或在推理时引入后处理平滑约束。

**问题二：单向信息流的充分性边界**

单向表情到手势的信息流假设“手势极少反向影响表情”，这在大多数中性演讲场景中成立。但在极度复杂的情感表达或自然对话中，是否存在手势强烈影响表情感知的场景？例如，当说话人做出强调性手势时，眉毛和头部姿态往往会同步响应以增强表达力。这种场景下，是否需要引入受控的双向建模（如稀疏的门控反向连接）？这需要在更多情绪标注数据上进行系统性分析。

**问题三：长序列生成的全局一致性**

FOPPAS 的累积误差在多分钟的长序列生成中是否可控？是否需要额外的全局一致性约束？可能的方向包括：引入周期性的“回顾”机制（每隔若干片段以全局上下文重新采样锚点帧）、或在训练时加入长程时间一致性损失。

**问题四：模态与条件的扩展**

DiffSHEG 是否能无缝扩展到下半身动作或全身交互？如何将文本/语义等额外条件更优雅地融入 UniEG 框架？当前的音频编码器已经融合了低层（Mel-spectrogram）、中层（可学习 Transformer 编码）和高层（HuBERT）特征，但显式的语义条件（如文本转录、对话行为标签）可能进一步提升手势的语义相关性。这需要设计新的条件注入机制，同时保持 UniEG 的单向信息流架构优势。

**问题五：评估指标的生态效度**

当前使用的 Fréchet 距离（FMD/FGD）和用户研究虽然在学术界被广泛接受，但 FMD 基于自动编码器隐空间的高斯假设，可能无法完全捕捉人类对动作质量的感知维度（如语义适当性、社交得体性）。开发更细粒度的、与人类判断更一致的自动评估指标，仍是整个语音驱动动作生成领域的共同挑战。

## 原文 PDF

![[paperPDFs/CVPR_2024/DiffSHEG_A_Diffusion_Based_Approach_for_Real_Time_Speech_driven_Holistic_3D_Expression_and_Gesture_Generation.pdf]]

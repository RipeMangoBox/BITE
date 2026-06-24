---
title: "TEACH: Temporal Action Composition for 3D Humans"
type: paper
paper_level: A
venue: 3DV
year: 2022
pdf_ref: paperPDFs/3DV_2022/TEACH_Temporal_Action_Composition_for_3D_Humans.pdf
aliases:
- TEACH
tags:
- 3DV_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "递归自回归地逐个生成动作，并在生成每个动作时显式条件化上一个动作最后若干帧的姿态信息（过去条件），从而保持动作间连贯过渡。"
primary_logic: "通过设计混合架构，在单个动作内部采用非自回归方式（如Transformer-VAE）保证生成运动的高质量与多样性，而在动作序列层面采用自回归条件化机制，利用过去运动帧作为上下文，既解决了长序列生成的计算扩展问题，又实现了时序动作组合的语义准确性和运动平滑性。"
claims:
- "TEACH 在 BABEL 动作对基准上的平均根关节位置误差显著低于独立和联合基线。"
- "定性示例显示 TEACH 能生成连贯的挥手与抬手组合动作，而基线产生过渡错误或丢失动作。"
- "过渡距离测量显示 TEACH 生成的过渡比独立基线更接近自然过渡，表明过去条件机制有效。"
- "消融实验证实条件化5个过去帧比仅条件化1帧或更多帧取得更佳性能。"
---

# TEACH: Temporal Action Composition for 3D Humans

> [!tip] 核心洞察
> 通过设计混合架构，在单个动作内部采用非自回归方式（如Transformer-VAE）保证生成运动的高质量与多样性，而在动作序列层面采用自回归条件化机制，利用过去运动帧作为上下文，既解决了长序列生成的计算扩展问题，又实现了时序动作组合的语义准确性和运动平滑性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TEACH：面向3D人体的时序动作组合合成 |
| 英文题名 | TEACH: Temporal Action Composition for 3D Humans |
| 会议/期刊 | 3DV 2022 |
| Links | [paper](https://arxiv.org/abs/2209.04066) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TEACH |
| Dataset | BABEL 验证集动作对 |

> [!tip] 效果简介
> - BABEL 验证集动作对 上，Average Positional Error (root joint, 越低越好) 为 0.674，对比 0.729 (Independent) / 0.790 (Joint)，变化 相比Independent降低7.5%，相比Joint降低14.7%。
> - BABEL 验证集动作对 上，Average Variance Error (root joint, 越低越好) 为 0.222，对比 0.255 (Independent) / 0.306 (Joint)，变化 相比Independent降低12.9%，相比Joint降低27.5%。

## 概述

**核心问题**：文本驱动的3D人体运动生成模型长期受限于单动作或单句输入，无法生成由多个动作按时间顺序组成的运动序列。其瓶颈在于缺乏动作序列训练数据，且现有非自回归模型难以扩展到长序列生成。

**核心方法**：TEACH 提出一种混合架构——在单个动作内部采用非自回归方式（基于Transformer-VAE）保证生成质量与多样性，而在动作序列层面采用递归自回归机制，将上一个动作最后若干帧的姿态信息作为“过去条件”，显式输入到当前动作的生成过程中，从而保持动作间的连贯过渡。

**核心结论**：
- 在 BABEL 动作对基准上，TEACH 的平均根关节位置误差（0.674）显著低于独立生成基线 Independent（0.729）和联合生成基线 Joint（0.790），分别降低 **7.5%** 和 **14.7%**（Table 1）。
- 过渡距离测量表明，TEACH 生成的过渡（0.107m）比 Independent 基线（0.151m）更接近自然过渡，证实过去条件机制有效降低了动作间的不连续性（Table 2）。
- 消融实验显示，条件化 **5 个过去帧** 取得最佳性能，优于仅条件化 1 帧或更多帧（Table 3）。
- 定性示例表明，TEACH 能够正确执行“挥手后抬起左手”等未见动作组合，而基线方法则产生过渡错误或丢失第二个动作（Figure 5）。

**方法定位**：TEACH 属于时序动作组合生成方法，通过自回归条件化机制将单动作生成模型扩展为序列生成模型，在文本驱动运动合成领域首次实现了对多动作时序组合的显式建模。

## 背景与动机

### 问题背景

生成逼真且可控的3D人体运动是计算机视觉与图形学领域的核心挑战之一，其应用涵盖动画制作、虚拟现实、人机交互等场景。近年来，文本驱动的运动生成方法取得了显著进展，使得用户可以通过自然语言描述来指定目标动作，极大地降低了运动合成的使用门槛。然而，现有方法普遍存在一个根本性限制：**它们被设计为从单句描述生成单段动作**，无法处理由多个动作按时间顺序组成的运动序列。

现实世界中，人类行为天然具有时序组合性——一个完整的运动过程通常包含若干连续的动作阶段，例如“先挥手，再抬起左手”。这种时序动作组合（temporal action composition）要求模型不仅理解每个独立动作的语义，还需生成动作之间平滑、自然的过渡。现有方法在这一任务上存在明显缺口。

### 现有方法缺口：两大技术瓶颈

**瓶颈一：训练数据的结构性缺失。** 大多数文本-运动数据集仅提供单句描述与对应运动片段的配对，缺乏动作序列级别的标注。虽然 BABEL 数据集提供了逐段标注的动作标签，允许从长序列中提取连续动作对，但现有模型并未利用这种时序结构进行训练。这导致模型从未学习过如何将多个动作连贯地衔接起来。

**瓶颈二：非自回归架构难以扩展到长序列。** 主流的文本驱动运动生成方法（如 TEMOS）采用非自回归（non-autoregressive）的 Transformer-VAE 架构，一次性生成整个运动序列的所有帧。这种设计在单动作生成中表现出色，能够保证运动质量与多样性，但当面对多动作序列时，直接生成全部帧会面临两个问题：一是计算复杂度随序列长度平方增长，无法扩展到长序列；二是模型缺乏显式的动作边界感知，难以在正确的时刻切换动作语义。

### 直接拼接为何不可行

一个直观的思路是：先用现有模型独立生成每个动作，再将它们拼接起来。但这一策略面临严峻挑战。由于单动作训练中每个动作被独立规范化（如朝向正面），拼接时需要对根关节进行平移和旋转对齐，而动作间的过渡区域则缺乏真实数据约束。简单的球面线性插值（Slerp）虽然能消除姿态跳变，但无法保证过渡的自然性——插值生成的中间姿态可能违背物理规律或动作语义，如出现不合理的站立-坐下切换（见 Figure 5）。

另一种思路是将多个动作的文本描述拼接为一句，联合训练生成整个序列。然而，这种“Joint”策略在训练集中未出现的动作组合上会失效：模型可能只执行第一个动作而忽略第二个动作，因为它从未见过这样的组合模式。

### 本文动机

上述分析揭示了一个核心矛盾：**单动作内部需要非自回归生成以保证质量，而动作序列之间需要自回归条件化以保证连贯性**。TEACH 的设计动机正是融合这两种范式的优势——在单个动作内部保持非自回归的生成方式，而在动作序列层面引入递归自回归机制，利用上一个动作的终止姿态作为生成下一个动作的上下文条件。这种“混合架构”既控制了长序列生成的计算开销，又为动作过渡提供了必要的时序约束，从而首次实现了文本驱动的时序动作组合合成。

## 核心创新

TEACH 的核心创新在于通过**递归自回归的动作序列生成机制**，解决了现有文本驱动运动生成模型无法处理多动作时序组合的根本瓶颈。

### 瓶颈突破：从单动作到动作序列

现有方法（如 TEMOS）局限于单动作或单句输入，无法生成由多个动作按时间顺序组成的运动序列。其根本原因有二：一是缺乏动作序列训练数据，二是非自回归模型难以扩展到长序列生成。TEACH 直接针对这一瓶颈，在 BABEL 数据集的动作对上进行训练，首次实现了文本驱动的时序动作组合合成。

### 关键设计：混合生成范式

TEACH 的核心洞察在于设计了**混合生成架构**：在单个动作内部采用非自回归方式（Transformer-VAE）保证生成运动的高质量与多样性，而在动作序列层面采用自回归条件化机制。具体而言，模型递归地逐个生成动作，每个动作的生成显式条件化于上一个动作最后 $P$ 帧的姿态信息（**过去条件机制**），从而在保持动作间连贯过渡的同时，解决了长序列生成的计算扩展问题。

这一设计的三个核心 changed slots 如下：

| 设计维度 | 基线方法 | TEACH 方案 | 证据锚点 |
|---------|---------|-----------|---------|
| **动作间关系建模** | Independent：独立生成后拼接；Joint：文本拼接联合训练 | 递归自回归生成，每个动作基于上一动作的过去姿态条件化 | “we design an iterative model that generates one motion per action at a time, by conditioning on the previous motion” |
| **条件输入** | 仅当前动作文本描述 | 当前文本描述 + 上一动作最后 $P$ 帧姿态特征 | “we combine the features from the previous action... and the current text features along with learnable tokens” |
| **过渡平滑策略** | Independent：仅依赖 Slerp 插值 | 过去条件生成隐式改善过渡，辅以 Slerp 插值修正残余不连续 | “To account for any remaining discontinuities... we apply spherical linear interpolation (Slerp) over a short time window” |

### 过去条件机制的有效性

消融实验证实，条件化 $P=5$ 个过去帧取得最佳性能（Average Positional Error = 0.674），优于 $P=1$（0.725）和 $P=10$（0.681），表明适度的历史信息最利于动作过渡（Table 3）。过渡距离测量进一步显示，TEACH 生成的过渡距离（0.107m）显著低于 Independent 基线（0.151m），证实了过去条件有效降低了动作间的不连续性（Table 2）。

定性示例（Figure 5）直观展示了这一机制的优势：对于“挥动右手，抬起左手”的动作序列，Independent 基线因缺乏过去条件而产生了从站立到坐下的不连贯过渡；Joint 基线因训练集中未见该动作组合而无法正确执行第二个动作；而 TEACH 能够正确且连贯地完成序列中的两个动作。

## 整体框架

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/002_Figure_2.jpg]]
*Figure 2: Method overview: Our TEACH model is a variational encoder-decoder neural network. The current text instruction and the past frames are encoded by the corresponding encoders and are fed to T _ { e n c } along with the additional tokens. T _ { e n c } produces the distribution parameters from which the latent vector is sampled and given to the decoder to generate a sequence of 3D human poses. In this figure, we omit the motion encoder for simplicity*

TEACH 的核心设计目标是在文本驱动下生成由多个动作按时间顺序组合而成的 3D 人体运动序列。其整体框架采用一种混合生成策略：在单个动作内部采用非自回归方式保证运动质量与多样性，而在动作序列层面采用递归自回归机制，利用上一个动作的结尾姿态作为条件输入，实现动作间的连贯过渡。

**输入与输出流**：系统接收一个自然语言描述序列及每个动作的指定持续时间作为输入，输出一段时序连贯的 3D 人体姿态序列。生成过程以递归方式逐动作推进——每次仅生成当前动作的运动，但生成时显式条件化于上一个动作的最后若干帧姿态信息。

**模块组成与数据流**：TEACH 是一个变分编码器-解码器神经网络，其核心模块及数据流如下（对应 **Figure 2**）：

1. **DistilBERT 文本编码器**：冻结的预训练语言模型，将当前动作的自然语言描述编码为文本特征。
2. **Past Encoder (PC)**：一个 Transformer 编码器，接收上一个动作的最后 $P$ 帧姿态，将其转化为运动特征，为当前动作生成提供上下文。
3. **Past-conditioned Text Encoder ($T_{enc}$)**：一个 Transformer 编码器，联合编码来自 PC 的过去运动特征、当前文本特征以及可学习令牌，输出高斯分布的均值 $\mu^i$ 和协方差 $\Sigma^i$。
4. **潜变量采样**：从 $T_{enc}$ 输出的高斯分布中采样潜向量 $z^i$，作为后续解码的条件。
5. **Motion Decoder**：与 TEMOS 结构相同的 Transformer 解码器，从潜向量 $z^i$ 生成指定帧数的 3D 人体姿态序列。
6. **Slerp & Alignment 后处理**：在两个动作之间执行根位置与朝向的对齐，并通过球面线性插值（Slerp）在 8 帧过渡窗口内平滑连接，消除残余不连续性。

**递归生成机制**：TEACH 的递归特性体现在动作序列层面的自回归条件化（对应 **Figure 4 (c)**）。与 Independent 基线（独立生成单动作后通过 Slerp 拼接，Figure 4 (a)）和 Joint 基线（将两个动作描述用逗号拼接后联合训练，Figure 4 (b)）不同，TEACH 在生成第二个及后续动作时，显式依赖上一个动作的结尾姿态作为过去条件。这种设计使得模型能够学习动作间的自然过渡模式，而非仅仅依赖后处理插值或文本拼接来维持连贯性。

**训练策略**：训练时使用 BABEL 数据集中提取的动作对。一次训练迭代包含两次前向传播（每个动作各一次）和一次反向传播，联合优化两个动作片段上的重建损失 $\mathcal{L}_R$ 和 KL 正则化损失 $\mathcal{L}_{KL}$：
$$\mathcal{L}_R = \mathcal{L}(H^1_{1:F_1}, \hat{H}^1_{1:F_1}) + \mathcal{L}(H^2_{1:F_2}, \hat{H}^2_{1:F_2})$$
$$\mathcal{L}_{KL} = KL(\phi^1, \psi) + KL(\phi^2, \psi)$$
其中 $\mathcal{L}$ 为平滑 L1 损失，$\phi^1$、$\phi^2$ 分别为两个动作对应的高斯分布，$\psi$ 为标准正态分布。

## 核心模块与公式推导

TEACH 的整体架构是一个变分编码器-解码器网络，其核心设计在于将**动作内非自回归生成**与**动作间自回归条件化**相结合。模型由四个关键模块串联构成：

1. **DistilBERT 文本编码器**：一个冻结的预训练语言模型，将当前动作的自然语言描述编码为文本特征向量，为后续模块提供语义条件。

2. **Past Encoder（PC）**：一个 Transformer 编码器，接收上一动作的最后 $P$ 帧姿态序列，将其转化为运动上下文特征。该模块是 TEACH 实现时序动作组合的关键——它显式地将“过去运动”编码为条件信号，使当前动作生成能够感知前一个动作的终止状态。

3. **Past-conditioned Text Encoder（T_enc）**：一个 Transformer 编码器，将 Past Encoder 输出的过去运动特征、DistilBERT 输出的当前文本特征以及一组可学习令牌联合编码，输出高斯分布的均值 $\mu^i$ 和协方差 $\Sigma^i$。潜向量 $z^i$ 从该高斯分布中采样得到，作为当前动作的紧凑表示。

4. **Motion Decoder**：与 TEMOS 相同的 Transformer 解码器，以潜向量 $z^i$ 为输入，生成指定帧数的完整姿态序列 $\hat{H}^i$。

5. **Slerp 与对齐后处理**：生成两个连续动作后，对第二个动作的根位置和朝向进行平移旋转对齐，并在两个动作之间插入 8 帧球面线性插值（Slerp），以消除残余的不连续性。

训练时，每次迭代包含两次前向传播（分别对应两个连续动作段），但仅执行一次反向传播，联合优化以下两个损失函数：

**重建损失**（Reconstruction Loss，Eq. 1）：

$$\mathcal{L}_R = \mathcal{L}(H^1_{1:F_1}, \hat{H}^1_{1:F_1}) + \mathcal{L}(H^2_{1:F_2}, \hat{H}^2_{1:F_2})$$

其中 $\mathcal{L}$ 为平滑 L1 损失，$H^i_{1:F_i}$ 和 $\hat{H}^i_{1:F_i}$ 分别表示第 $i$ 个动作段的真实姿态序列和生成姿态序列，$F_i$ 为对应动作的帧数。该损失约束两个动作段的生成质量。

**KL 损失**（KL Loss，Eq. 2）：

$$\mathcal{L}_{KL} = KL(\phi^1, \psi) + KL(\phi^2, \psi)$$

其中 $\phi^i = \mathcal{N}(\mu^i, \Sigma^i)$ 为 T_enc 为第 $i$ 个动作预测的高斯分布，$\psi = \mathcal{N}(0, I)$ 为标准正态分布。该损失作为 VAE 正则化项，约束潜空间的结构化程度。

两个损失联合优化，使模型在保证单动作生成质量的同时，通过过去条件机制学习动作间的自然过渡。

## 实验与分析

### 数据集与评估协议

TEACH 的训练与评估基于 **BABEL** 数据集。该数据集包含 10881 条运动序列，附有 65926 条文本标签，其词汇丰富度显著高于 KIT——在不同词频阈值下，BABEL 的 token 数量至少是 KIT 的两倍（Figure 3）。为训练时序动作组合模型，作者从 BABEL 的连续动作片段中提取动作对（pairs），训练集约 23.4k 对，验证集约 5.7k 对（Table A.1）。所有定量评估均在 BABEL 验证集上进行，测试集未公开，确保了可复现性。


![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/003_Figure_3.jpg]]
*Figure 3: BABEL vs KIT: We provide a comparative analysis of the amount of data and the vocabulary of verbs. On the top, the number of tokens (i.e. different words) in each dataset is plotted against various frequency thresholds, i.e. the number of words that appear at least freq. threshold times. We see that BABEL consistently has at least twice as many tokens as KIT. On the bottom, the verb histogram shows that BABEL has more samples across a wide range of actions. Note that there are differences in how the datasets label actions with generic words like “do” and “perform” being common in KIT and rare in BABEL, which is more specific*

评估指标采用两类根关节误差：
- **Average Positional Error (APE)**：生成运动与真值在根关节位置上的平均欧氏距离，越低越好。
- **Average Variance Error (AVE)**：生成运动与真值在根关节位置方差上的差异，越低越好。

### 基线方法

为验证时序条件化的有效性，作者设计了两种基线：

- **Independent**：基于 TEMOS 架构对单动作独立训练。生成时，两个动作分别生成后，通过根对齐（平移与旋转）和球面线性插值（Slerp）拼接为序列。由于单动作训练中每个动作均被独立规范化至正面朝向，拼接时额外执行了根对齐以保证公平对比。
- **Joint**：将两个动作的文本描述用逗号拼接为单一文本，联合训练生成动作对。该方法试图让模型一次性学习两个动作的组合，但受限于训练集中动作组合的覆盖范围。

TEACH 与上述基线的核心差异在于：TEACH 采用递归自回归策略，逐动作生成，并在生成每个动作时显式条件化上一个动作的最后 5 帧姿态信息（Figure 4）。

### 主实验结果

Table 1 报告了 TEACH 与两种基线在 BABEL 验证集动作对上的定量对比。TEACH 在所有指标上均取得最优结果：


![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/004_Table_1.jpg]]
*Table 1: Comparison against baselines on pairs of actions: We benchmark the 3 different approaches on pairs of BABEL [33]. As we can see TEACH outperforms Joint and Independent baselines in all the metrics*

- **Average Positional Error**：TEACH 为 0.674，相比 Independent（0.729）降低 7.5%，相比 Joint（0.790）降低 14.7%。
- **Average Variance Error**：TEACH 为 0.222，相比 Independent（0.255）降低 12.9%，相比 Joint（0.306）降低 27.5%。

Joint 基线表现最差，表明简单拼接文本描述无法有效建模动作间的时序依赖，尤其当训练集中未出现特定动作组合时，模型难以正确生成第二个动作。Independent 基线虽能保证单动作质量，但缺乏动作间上下文信息，导致过渡不自然。

### 消融实验

**Slerp 平滑的效果（Table 2）**。为量化动作间过渡的自然程度，作者定义了“过渡距离”——将第一个动作的最后一帧与第二个动作的第一帧进行根对齐后，计算关节点位置的欧氏距离。TEACH 生成的过渡距离为 0.107m，显著低于 Independent 基线的 0.151m。这表明过去条件机制在生成阶段已有效降低了动作间的不连续性，Slerp 仅作为后处理修正残余不连续。需注意，Independent 基线若不进行根对齐则无法评估过渡距离，因为其单动作训练使每个动作均面向正面。


![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/007_Table_2.jpg]]
*Table 2: Effect of Slerp: We measure transition distance for generated samples given all the test set pairs. We define transition distance as the Euclidean distance between the last frame of the first action and the first frame of the second action, calculated on joint positions, when the last pose of the first action is aligned with the first pose of the next action and when it is not. TEACH better captures the transition between the two actions compared to the previous-action-agnostic TEMOS. Moreover, the Independent baseline cannot be benchmarked without orienting and aligning the poses as it is trained on single actions that are canonicalized to face in the forward direction*

**过去帧数量 P 的消融（Table 3）**。作者考察了条件化不同数量的过去帧对性能的影响。当 P=5 时，APE 为 0.674，优于 P=1（0.725）和 P=10（0.681）。结果表明，适度的历史信息（5 帧）最利于动作过渡：过少（1 帧）无法提供足够的运动上下文，过多（10 帧）可能引入冗余或过时信息。


![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/008_Table_3.jpg]]
*Table 3: Ablation on the number of past frames: Here, we change the number of past frame, while keeping the other training settings identical and report the different metrics. We observe the best performance when using 5 past frames*

**定性消融（Figure 5）**。以动作序列 [wave the right hand, raise the left hand] 为例：

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison: We show an illustrative example for (a) Independent, (b) Joint and (c) TEACH for the sequence of actions [wave the right hand, raise the left hand]. While the individual waving and raising hand actions are correctly generated, the single-action independent baseline (a) transitions from standing to sitting incoherently as the next action is not conditioned on the past. Joint baseline (b) on the other hand, waves with the right hand but does not raise the left one, probably because such an action combination was not present in the training set. On the other hand, TEACH learns about both single action variation and and autoregressive transitions between actions, and thu...*

- Independent 基线：挥手和抬手动作本身正确，但过渡时从站立错误地变为坐下，因为第二个动作的生成完全独立于前一个动作的终止姿态。
- Joint 基线：能完成挥手，但未能抬起左手，很可能因为该动作组合未出现在训练集中。
- TEACH：正确执行了两个动作，且过渡自然流畅，证明其既保留了单动作的生成多样性，又学会了动作间的自回归过渡。

### 定性结果与泛化能力

Figure 6 展示了更多 TEACH 生成的定性结果。前 3 行显示 TEACH 能生成超越步态的动作对，如“右手触地”等非运动类动作。即使是细粒度序列如 [step forward with the right foot, kick with the left foot] 也能准确生成。最后一行展示了三连动作序列的生成结果，初步验证了模型向更长序列泛化的潜力。

### 失败模式与局限性

尽管 TEACH 在定量指标和定性展示上表现优异，仍存在以下局限：

1. **过渡物理合理性不足**：模型在动作过渡处仍可能出现加速度不连续，依赖后处理 Slerp 进行平滑，未从本质上学习过渡姿态的物理合理性。Table 2 中 TEACH 的过渡距离（0.107m）虽优于基线，但绝对值仍表明存在可感知的不连续性。

2. **已知持续时间的假设**：模型假设每个动作的持续时间已知，实际应用中需单独预测或由用户指定，限制了端到端部署的灵活性。

3. **物理接触建模缺失**：未显式建模身体与环境的接触或物理约束（如足部滑动），可能导致生成的移动缺乏真实物理交互。

4. **长序列累积误差**：训练数据仅为双动作对，向更长序列泛化时可能存在累积误差；对未见动作组合的泛化能力未充分验证。Figure 6 的三连动作仅是初步定性展示，缺乏系统性的长序列定量评估。

5. **仅支持时序组合**：模型当前仅支持前后动作的时序组合，未考虑同一时间执行多个动作（空间组合）的情景。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/011_Figure.jpg]]
*Figure: ise Zise Figure A.1. BABEL vs KIT: Here, we show additional plots regarding the language on BABEL and KIT. We show the token frequency of the two different datasets for different POS tag groups. Verbs (top left), verbs and adverbs (top right), verbs, adverbs and nouns (bottom left) and verbs, adverbs, noun, adjectives (bottom right)*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2209_04066/figures/010_Table.jpg]]
*Table: A.1. Datatype statistics: We show the statistics from different BABEL label types. Sequences are the AMASS [25] motions with a single action label, Segments are the smaller motions that are extracted from longer AMASS sequences. Pairs are the twoaction motions that we extract from consecutive segments. We denote the exclusion of “transition”, “a-pose”, and “t-pose” labels with **


## 方法谱系与知识库定位

### 1. 问题定位：从单动作生成到时序动作组合

TEACH 解决的核心瓶颈在于：现有文本驱动运动生成模型（如 TEMOS）局限于单动作或单句输入，无法生成由多个动作按时间顺序组成的运动序列。这一局限的根源有两方面：一是缺乏动作序列训练数据，二是现有非自回归模型无法直接扩展到长序列生成。

在 TEACH 之前，处理动作序列的两种朴素策略各有致命缺陷：
- **独立生成 + 后拼接（Independent 基线）**：基于 TEMOS 的单动作训练范式，对每个动作独立生成运动片段，再通过根关节对齐和球面线性插值（Slerp）拼接。该策略完全忽视动作间的因果关系，导致过渡处出现语义错误（如从站立突然变为坐下）或物理不连续。
- **文本拼接联合生成（Joint 基线）**：将两个动作的文本描述用逗号拼接，联合训练生成动作对。该策略在训练集中出现过的组合上可工作，但对未见动作组合（如“挥右手”后“抬左手”）完全失效，通常只能生成第一个动作而忽略第二个——这暴露了联合编码无法解耦动作间条件依赖的深层缺陷。

### 2. 核心方法贡献：混合自回归/非自回归架构

TEACH 的核心设计哲学是“在动作内部保持非自回归生成的质量与多样性，在动作序列层面引入自回归条件化以保证过渡连贯性”。这一设计通过三个关键模块实现：

1. **递归自回归生成框架**：逐个生成动作，每个动作的生成显式条件化于上一个动作最后 $P$ 帧的姿态信息（过去条件）。这本质上是一种“滑动窗口自回归”策略，既避免了全序列自回归的计算爆炸，又保留了动作间因果依赖。

2. **过去条件化文本编码器（Past-conditioned Text Encoder）**：通过 Transformer 编码器联合编码当前文本特征、过去运动特征和可学习令牌，输出 VAE 潜空间的高斯分布参数 $\mu^i$ 和 $\Sigma^i$。这是将时序上下文注入生成过程的核心机制。

3. **Slerp 辅助平滑**：在生成后对动作过渡处施加短窗口球面线性插值，修正残余不连续性。需注意这仅是后处理补丁，并非从本质上学习过渡姿态的物理合理性。

### 3. 与基线方法的关系

| 方法 | 动作间关系建模 | 条件输入 | 过渡策略 | 核心局限 |
|------|---------------|---------|---------|---------|
| **Independent**（基于 TEMOS） | 无，独立生成 | 仅当前文本 | 根对齐 + Slerp | 过渡语义错误，动作间无因果约束 |
| **Joint** | 文本拼接，联合生成 | 拼接文本 | 隐式（训练中学习） | 未见组合完全失效，无法解耦动作 |
| **TEACH** | 递归自回归，过去条件化 | 当前文本 + 过去 $P$ 帧姿态 | 过去条件 + Slerp 后处理 | 过渡仍依赖后处理，未端到端学习 |

TEACH 相对于 Independent 基线的平均根关节位置误差降低 7.5%（0.674 vs 0.729），相对于 Joint 基线降低 14.7%（0.674 vs 0.790）（Table 1）。过渡距离测量显示，TEACH 生成的过渡（0.107m）显著优于 Independent 基线（0.151m），证实过去条件机制有效降低了动作间的不连续性（Table 2）。

### 4. 适用边界与局限

**适用场景**：
- 已知动作持续时间的时序动作组合生成
- 训练集中出现过的动作类型（单动作层面）
- 双动作序列（训练数据限制）

**已知局限**（需在应用时注意）：
1. **过渡物理合理性不足**：模型在动作过渡处仍可能出现加速度不连续，依赖 Slerp 后处理进行平滑，未从本质上学习过渡姿态的物理约束。
2. **持续时间需外部给定**：假设已知每个动作的持续时间，实际应用中需单独预测或用户指定，这限制了端到端部署。
3. **缺乏物理接触建模**：未显式建模身体与环境的接触或物理约束（如足部滑动），可能导致生成的移动缺乏真实物理交互。
4. **训练数据仅为双动作对**：向更长序列泛化时可能存在累积误差；对未见动作组合的泛化能力未在实验中充分验证。
5. **仅支持时序组合**：模型当前仅支持前后动作的时序组合，未考虑同一时间执行多个动作（空间组合）的情景。

### 5. 开放问题与后续方向

TEACH 留下的开放问题指向若干值得探索的方向：

- **前向信息引入**：是否可以通过引入未来动作信息（look-ahead）来进一步提升过渡质量？这需要设计双向或预测性条件化机制。
- **端到端过渡学习**：如何将过渡生成完全融入网络，以端到端方式替代 Slerp 后处理？这可能需要在损失函数中显式建模过渡平滑性约束。
- **变长度动作合成**：该方法如何在不依赖已知持续时间的情况下进行非固定长度的动作合成？这涉及持续时间预测与生成的一体化。
- **空间动作组合扩展**：时序动作组合策略能否扩展至空间动作组合（如同步执行多个动作），实现更复杂的行为描述与生成？
- **长序列累积误差控制**：当动作序列变长时，累积错误如何有效控制？是否需要引入长程记忆机制（如记忆网络或层次化条件化）？

### 6. 在知识库中的定位

TEACH 处于**文本驱动人体运动生成**与**时序动作组合**的交叉点。在文本驱动运动生成谱系中，它继承了 TEMOS 的 Transformer-VAE 架构（非自回归单动作生成），但在序列层面引入了自回归条件化机制，将问题从“单句到单动作”扩展到“多句到多动作序列”。这一设计使其区别于纯自回归方法（如 MotionGPT 等将运动离散化为 token 序列逐帧生成）和纯非自回归方法（如 MDM 等基于扩散的并行生成），形成了“混合粒度自回归”的新范式。

在数据层面，TEACH 充分利用了 BABEL 数据集的独特优势——该数据集提供动作片段间的时序标注，使得提取连续动作对成为可能。相比于 KIT 等数据集，BABEL 的词汇量至少为其两倍（Figure 3），这为训练时序条件化模型提供了必要的语言多样性。

## 原文 PDF

![[paperPDFs/3DV_2022/TEACH_Temporal_Action_Composition_for_3D_Humans.pdf]]
